// One-off importer: ../spec_pages.csv + ../spec_api_data.json + ../symptom_pages.json -> data/*.json
// Never invents values: anything TODO/unsourced is stored as value:null, verified:false.
import fs from 'node:fs';
import { parseTires } from './tires.mjs';
const ROOT = new URL('../../', import.meta.url).pathname;
const OUT = new URL('../data/', import.meta.url).pathname;
const TODAY = '2026-10-15'; // data retrieval date of the legacy files

function parseCsv(txt) {
  const rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < txt.length; i++) {
    const c = txt[i];
    if (q) { if (c === '"' && txt[i + 1] === '"') { f += '"'; i++; } else if (c === '"') q = false; else f += c; }
    else if (c === '"') q = true; else if (c === ',') { row.push(f); f = ''; }
    else if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; } else if (c !== '\r') f += c;
  }
  if (f || row.length) { row.push(f); rows.push(row); }
  const [h, ...rest] = rows; return rest.filter(r => r.length > 1).map(r => Object.fromEntries(h.map((k, i) => [k, r[i] ?? ''])));
}
export const isoFromDMY = s => { const m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(s || ''); return m ? `${m[3]}-${m[2]}-${m[1]}` : null; };

// Grade: A = OEM manual / government; B = official third party (e.g. OEM press site); C = mirror / unverified
function sourced(raw, sourceId) {
  let t = (raw || '').trim();
  if (!t || /^(TODO|Not yet verified)/i.test(t)) return { value: null, source: null, sourceGrade: null, verified: false, note: t ? t.replace(/^TODO:?\s*/i, '') : null };
  if (/^N\/A/i.test(t)) return { value: null, source: null, sourceGrade: null, verified: false, notApplicable: true, note: t };
  let grade = 'A', notes = [];
  const flag = t.match(/\[(mirror[^\]]*|verify[^\]]*|search summary[^\]]*)\]/gi);
  if (flag) { grade = flag.some(x => /verify|search summary/i.test(x) && !/mirror/i.test(x)) ? 'C' : 'B'; notes.push(...flag); t = t.replace(/\s*\[[^\]]*\]\s*/g, ' ').trim(); }
  if (/NOT yet confirmed/i.test(t)) { grade = 'B'; notes.push('not confirmed for this model year'); }
  // drop partial TODO segments ("Hybrid: TODO") so no TODO text can ever render
  const segs = t.split(/;\s*/).filter(s => !/TODO/i.test(s));
  if (segs.length < t.split(/;\s*/).length) notes.push('some variants not yet sourced');
  t = segs.join('; ');
  let page = null; const pm = t.match(/\s+—\s+(p\.\s?\d+)\s*$/); if (pm) { page = pm[1]; t = t.slice(0, pm.index); }
  const confirmed = t.match(/\s*\(confirmed by ([^)]+)\)/); if (confirmed) { notes.push('confirmed by ' + confirmed[1]); t = t.replace(confirmed[0], ''); }
  return { value: t, source: sourceId, page, sourceGrade: grade, verified: false, note: notes.join('; ') || null };
}
function towing(r) {
  const t = (r.towing_capacity || '').trim(); if (!t || /^TODO/.test(t)) return { value: null, source: null, sourceGrade: null, verified: false };
  const url = (r.field_sources.match(/towing:\s*(\S+)/) || [])[1] || null;
  let sid = url ? 'towing-' + r.slug : null;
  if (!sid && /OM\w+ pp?\.\d/.test(t) && !/^TODO/.test(r.manual_source)) return { value: t, source: 'manual-' + r.slug, sourceGrade: 'A', verified: false, note: null };
  if (sid) sources[sid] = { name: t.split(' — ')[1] || 'Manufacturer spec sheet', url, type: 'oem-spec-sheet', grade: 'A', retrieved: TODAY };
  return { value: t.split(' — ')[0], source: sid, sourceGrade: sid ? 'A' : null, verified: false, note: null };
}
const tireCsv = fs.existsSync(ROOT + 'tire_rows.csv') ? parseCsv(fs.readFileSync(ROOT + 'tire_rows.csv', 'utf8')) : [];
function tiresFor(r, src, g) {
  const explicit = tireCsv.filter(t => t.slug === r.slug);
  if (explicit.length) return { rows: explicit.map(t => {
    let sid = Object.keys(sources).find(k => sources[k].url === t.source);
    if (!sid) { const code = (t.source.match(/\/(OM\w+)\//) || [])[1]; sid = 'doc-' + (code || r.slug + '-' + Object.keys(sources).length); sources[sid] = { name: `${r.make} owner's manual ${code || ''} (${r.year} ${r.model})`.replace('  ', ' '), url: t.source, type: 'oem', grade: t.grade, retrieved: TODAY, archived: archive[t.source] || null }; }
    return { wheel: t.wheel_in || null, config: t.config || null, tireSize: t.tire_size || null, frontPsi: t.front_psi ? +t.front_psi : null, rearPsi: t.rear_psi ? +t.rear_psi : null,
             page: t.manual_page ? (/^[\d–\-,\/ ]+$/.test(t.manual_page) ? 'p.' + t.manual_page : t.manual_page) : null, source: sid, sourceGrade: t.grade || null }; }), origin: 'tire_rows.csv', note: null };
  const sz = g(r.tire_size), ps = g(r.tire_pressure);
  // free text that embeds psi inside tire_size ("see tire_size") is too ambiguous to parse safely -> needs tire_rows.csv
  if (/see tire_(size|rows)/i.test(r.tire_pressure)) return { rows: [], origin: 'needs tire_rows.csv', note: 'tire rows must be entered in tire_rows.csv' };
  // row grade = weaker of the two fields; unsourced fields contribute nothing
  const rank = { A: 0, B: 1, C: 2 };
  const grade = [sz, ps].filter(x => x.value).map(x => x.sourceGrade).sort((a, b) => rank[b] - rank[a])[0] || null;
  const rows = parseTires(sz.value, ps.value, src, grade, sz.page || ps.page);
  // online manuals have no printed page: fall back to the section name (last part of the path in manual_note)
  const sec = /online|TechInfo/i.test(r.manual_note || '') && ((r.manual_note.match(/\bsection\s+([^.;|]+)/i) || r.manual_note.match(/I?OM\)\s*>\s*([^.;|]+)/) || [])[1]);
  if (sec) rows.forEach(x => { if (!x.page) x.page = sec.split('>').pop().trim(); });
  if (/non-hybrid/i.test(r.manual_note)) rows.forEach(x => { if (!x.config) x.config = 'Non-hybrid'; });
  return { rows, note: [sz.note, ps.note].filter(Boolean).join('; ') || null };
}
const slugify = s => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

const csv = parseCsv(fs.readFileSync(ROOT + 'spec_pages.csv', 'utf8'));
const api = JSON.parse(fs.readFileSync(ROOT + 'spec_api_data.json', 'utf8'));
const sources = {
  'nhtsa-recalls': { name: 'NHTSA Recalls API', url: 'https://www.nhtsa.gov/recalls', type: 'government', grade: 'A', retrieved: TODAY },
  fueleconomy: { name: 'fueleconomy.gov (U.S. EPA / DOE)', url: 'https://www.fueleconomy.gov/', type: 'government', grade: 'A', retrieved: TODAY },
};
const archive = {};
try { for (const l of fs.readFileSync(ROOT + 'manuals/sources.tsv', 'utf8').trim().split('\n').slice(1)) { const [file, url, at] = l.split('\t'); if (/WRONG-YEAR/.test(file) || !fs.existsSync(ROOT + 'manuals/' + file)) continue; archive[url] = { file: 'manuals/' + file, fetchedAt: at }; } } catch {}
for (const r of csv) {
  const a = api.find(x => x.slug === r.slug) || {};
  const [, , makeSlug, modelSlug] = r.url.split('/');
  const ev = (a.fueleconomy || []).some(c => c.fuel === 'Electricity');
  const sid = `manual-${r.slug}`;
  if (!/^TODO/.test(r.manual_source)) sources[sid] = { name: ((m => m ? `${r.make} owner's manual ${m.toUpperCase()} (${r.year} ${r.model})` : `${r.year} ${r.make} ${r.model} owner information`)((r.manual_source.match(/\/(OM\w+)\//) || r.manual_source.match(/\/([a-z0-9]{4,}i?om)\//i) || (r.manual_note || '').match(/\b(A[A-Z0-9]{6,}I?OM)\b/) || [])[1])), url: r.manual_source, type: /carmanualsonline|mirror/.test(r.manual_source) ? 'mirror' : 'oem', grade: /carmanualsonline/.test(r.manual_source) ? 'B' : 'A', retrieved: TODAY, note: r.manual_note || null, archived: archive[r.manual_source] || null };
  const src = sources[sid] ? sid : null;
  const g = v => { const s = sourced(v, src); if (s.value && sources[sid]?.grade !== 'A' && s.sourceGrade === 'A') s.sourceGrade = sources[sid].grade; return s; };
  const v = {
    slug: r.slug, year: +r.year, make: r.make, model: r.model, makeSlug, modelSlug,
    powertrain: ev ? 'ev' : 'ice', vpicConfirmed: !!a.vpic_confirmed,
    manual: { sourceId: src, yearConfirmed: !/edition is not MY|not MY20\d\d|NOT yet confirmed for MY|labelled 20\d\d\+/i.test(r.manual_note + ' ' + r.tire_size + ' ' + r.source_grade), note: r.manual_note || null },
    specs: { oilCapacity: g(r.oil_capacity), oilViscosity: g(r.oil_viscosity), wiperSizes: g(r.wiper_sizes), batteryGroup: g(r.battery_group), towingCapacity: towing(r), tpmsReset: /^(TODO|N\/A)/i.test(r.tpms_reset || 'TODO') ? g('') : g(r.tpms_reset) },
    tires: tiresFor(r, src, g),
    extraManuals: [...new Set((r.manual_note.match(/https:\/\/assets\.sia\.toyota\.com\/\S+?\.pdf/g) || []).filter(u => u !== r.manual_source))].filter(u => !/OM0R100U/.test(u)),
    fuelEconomy: (a.fueleconomy || []).map(c => ({ feId: c.fe_id, model: c.model, option: c.option, engineL: c.engine_l ? +c.engine_l : null, cyl: c.cyl ? +c.cyl : null, trans: c.trans, drive: c.drive, mpgCity: +c.mpg_city, mpgHwy: +c.mpg_hwy, mpgComb: +c.mpg_comb, fuel: c.fuel, url: c.api, source: 'fueleconomy', sourceGrade: 'A' })),
    fuelEconomyFetched: Array.isArray(a.fueleconomy) && a.fueleconomy.length > 0 ? TODAY : null,
    recalls: (a.recalls || []).map(x => ({ campaign: x.campaign, component: x.component, date: isoFromDMY(x.date), summary: x.summary, source: 'nhtsa-recalls', sourceGrade: 'A' })),
    recallsFetched: Array.isArray(a.recalls) ? TODAY : null, recallsUrl: a.recalls_source || r.recalls_source,
    related: { issues: [] },
    publishDate: null, dataUpdated: TODAY,
    signOff: r.signoff === 'yes' && r.reviewed_by && /^\d{4}-\d{2}-\d{2}/.test(r.reviewed_at) ? { by: r.reviewed_by, date: r.reviewed_at.slice(0, 10) } : null,
  };
  if (ev) {
    // ev_range / ev_efficiency: optional columns (tolerate absence); per-variant text rendered as given.
    const feUrl = ((r.ev_source || '') + ' ' + (r.field_sources || '')).match(/https:\/\/www\.fueleconomy\.gov\/\S+/)?.[0]?.replace(/[,;)]+$/, '') || null;
    const ids = [...new Set(((r.ev_source || '') + ' ' + (r.field_sources || '') + ' ' + (r.engine_mpg || '')).match(/\b462\d\d\b/g) || [])];
    const evSid = feUrl ? 'fe-ev-' + r.slug : null;
    if (evSid) sources[evSid] = { name: `fueleconomy.gov (U.S. EPA / DOE), ${r.year} ${r.make} ${r.model}${ids.length ? ` (vehicle ids ${ids.join(', ')})` : ''}`, url: feUrl, type: 'government', grade: 'A', retrieved: TODAY };
    const evField = (col, what) => { const t = (r[col] || '').trim();
      if (!t || /^(TODO|Not yet verified)/i.test(t)) return { value: null, source: null, sourceGrade: null, verified: false, note: col in r ? null : `column ${col} not present yet (${what})` };
      return { value: t, source: evSid, sourceGrade: evSid ? 'A' : null, verified: false, note: evSid ? null : 'no fueleconomy.gov source URL' }; };
    v.specs.evRange = evField('ev_range', 'range');
    v.specs.evEfficiency = evField('ev_efficiency', 'kWh/100 mi, MPGe');
            v.specs.battery12v = { value: null, source: null, sourceGrade: null, verified: false };
            for (const k of ['oilCapacity', 'oilViscosity']) delete v.specs[k]; }
  fs.writeFileSync(`${OUT}vehicles/${r.slug}.json`, JSON.stringify(v, null, 2) + '\n');
}
const EXCLUDED = new Set(['car-jerks-when-accelerating', 'car-shaking-when-accelerating']); // removed from pilot 2026-10-15
for (const f of fs.readdirSync(OUT + 'issues')) fs.unlinkSync(OUT + 'issues/' + f);
const issues = JSON.parse(fs.readFileSync(ROOT + 'symptom_pages.json', 'utf8')).filter(x => !EXCLUDED.has(x.slug));
const scs = JSON.parse(fs.readFileSync(ROOT + 'symptom_code_sources.json', 'utf8'));
const unverified = it => !it || !it.grade || it.grade === '-' || /^not verified/i.test(it.fact || '');
const maker = d => (d.match(/^(?:\d{4} )?(GM|Honda\/Acura|Honda|Mazda|Nissan|Stellantis|Mitsubishi|Ford|VW|Subaru|Toyota|Chevrolet)/) || [])[1] || null;
const kind = d => /EPA|fact sheet/i.test(d) ? 'fact sheet' : /owner'?s manual/i.test(d) ? "owner's manual" : /support/i.test(d) ? 'support page' : /service manual/i.test(d) ? 'service manual' : /tip/i.test(d) ? 'tech tip' : 'service bulletin';
const cited = it => ({ text: it.fact, url: it.url, document: it.document, page: it.page || null, fetched: it.fetched || null, sourceGrade: it.grade, maker: maker(it.document || '') || (/U\.S\. EPA/.test(it.document) ? 'U.S. EPA' : /NHTSA/.test(it.document) && !/Owner/.test(it.document) ? 'NHTSA' : /Toyota|Camry/.test(it.document) ? 'Toyota' : /Ford/.test(it.document) ? 'Ford' : null), docKind: kind(it.document || ''), appliesTo: it.scope || null, quote: it.quote || null });
for (const s of issues) {
  const src = (s.type === 'code' ? scs.codes : scs.symptoms)[s.slug] || {};
  const urg = (src.urgency || []).filter(x => !unverified(x));
  const o = {
    slug: s.slug, type: s.type, code: s.type === 'code' ? s.slug.toUpperCase() : null,
    title: s.type === 'code' ? s.slug.toUpperCase() : s.target_keyword.replace(/\bwont\b/, "won't").replace(/^\w/, c => c.toUpperCase()).replace(/\babs\b/i, 'ABS'),
    targetKeyword: s.target_keyword,
    definition: src.definition && !unverified(src.definition) ? { ...cited(src.definition), value: (src.definition.display_name || src.definition.fact.replace(/^P\d{4}:\s*/, '')).trim(), sourceText: src.definition.fact } : null,
    causes: (src.causes || []).filter(x => !unverified(x)).map(cited),
    urgency: urg.map(cited),                // legacy urgency statements (brand-specific)
    guidancePrimary: src.driving_guidance_primary || null,
    guidance: (src.driving_guidance || []).filter(x => !unverified(x) && x.url && x.quote && !/\$\d|cost|price/i.test(x.quote)).map(x => ({ ...cited({ ...x, fact: x.quote }), answers: x.answers || '', allBrands: /all obd|all vehicles|federal|generic|universal/i.test(x.scope || '') && /EPA|NHTSA/.test(x.document || '') })),
    firstStep: null,                        // "shop vs check yourself first" — needs a cited source, none yet
    safetyCritical: /brak|abs/i.test(s.slug),
    related: { issues: [], vehicles: [] },
    publishDate: null, dataUpdated: TODAY,
    signOff: (() => { const so = typeof src.signoff === 'object' && src.signoff ? src.signoff : src; return so.signoff === 'yes' && so.reviewed_by && /^\d{4}-\d{2}-\d{2}/.test(so.reviewed_at || '') ? { by: so.reviewed_by, date: so.reviewed_at.slice(0, 10) } : null; })(),
  };
  fs.writeFileSync(`${OUT}issues/${s.slug}.json`, JSON.stringify(o, null, 2) + '\n');
}
delete sources.repairpal; // RepairPal banned (ToS)
// "sign one, release one": signed pages go live on their sign-off date, max 10 new pages per day
const MAX_PER_DAY = 10, perDay = {};
const all = [...fs.readdirSync(OUT + 'vehicles').map(f => OUT + 'vehicles/' + f), ...fs.readdirSync(OUT + 'issues').map(f => OUT + 'issues/' + f)]
  .map(f => [f, JSON.parse(fs.readFileSync(f, 'utf8'))]).filter(([, o]) => o.signOff).sort((a, b) => a[1].signOff.date.localeCompare(b[1].signOff.date));
const RO = fs.existsSync(OUT + 'release-order.json') ? JSON.parse(fs.readFileSync(OUT + 'release-order.json', 'utf8')) : {};
// release order (relative days) lives in data/release-order.json and is applied at build time; publishDate here is informational only
for (const [f, o] of all) {
  let d = o.signOff.date;
  while ((perDay[d] || 0) >= MAX_PER_DAY) d = new Date(Date.parse(d) + 864e5).toISOString().slice(0, 10);
  perDay[d] = (perDay[d] || 0) + 1; o.publishDate = d; fs.writeFileSync(f, JSON.stringify(o, null, 2) + '\n');
}
// related-issue groups from site config (all slugs in a group link each other; template shows only live ones)
for (const grp of RO.relatedIssues || []) for (const a of grp) { const f = OUT + 'issues/' + a + '.json'; if (!fs.existsSync(f)) continue;
  const o = JSON.parse(fs.readFileSync(f, 'utf8')); o.related.issues = [...new Set([...(o.related.issues || []), ...grp.filter(b => b !== a)])]; fs.writeFileSync(f, JSON.stringify(o, null, 2) + '\n'); }
fs.writeFileSync(OUT + 'sources.json', JSON.stringify(sources, null, 2) + '\n');
// pilot list = P1 rows of pages.csv (R-U1)
const pages = parseCsv(fs.readFileSync(ROOT + 'pages.csv', 'utf8')).filter(p => p.priority === 'P1').map(p => p.target_url).filter(u => !EXCLUDED.has(u.split('/')[2]));
fs.writeFileSync(OUT + 'pilot-urls.json', JSON.stringify(pages, null, 2) + '\n');
console.log('imported', csv.length, 'vehicles,', issues.length, 'issues,', pages.length, 'pilot urls');

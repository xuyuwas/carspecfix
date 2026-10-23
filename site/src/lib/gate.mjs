// Publish gate shared by Astro pages and Node check scripts.
import fs from 'node:fs';
import path from 'node:path';
const DATA = path.resolve(process.cwd(), 'data');
const rd = f => JSON.parse(fs.readFileSync(f, 'utf8'));
export const SITE = 'https://carspecfix.com';
export const PREVIEW = process.env.PREVIEW === '1';
export const RELEASE_DAY = +(process.env.RELEASE_DAY || 1);
const _ro = JSON.parse(fs.readFileSync(new URL('../../data/release-order.json', import.meta.url), 'utf8'));
export const releaseDayOf = slug => { for (const [d, list] of Object.entries(_ro.days || {})) if (list.includes(slug)) return +d; return null; };
export const TODAY = process.env.BUILD_DATE || new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York' }).format(new Date());

export const sources = rd(path.join(DATA, 'sources.json'));
export const vehicles = fs.readdirSync(path.join(DATA, 'vehicles')).sort().map(f => rd(path.join(DATA, 'vehicles', f)));
export const issues = fs.readdirSync(path.join(DATA, 'issues')).sort().map(f => rd(path.join(DATA, 'issues', f)));
export const pilotUrls = rd(path.join(DATA, 'pilot-urls.json'));
// The corrections log is the single source of truth for "when did this page last change".
// A page's verified `dataUpdated` can be older than the day a display fix shipped, so the
// per-page "last changed" date and the changelog's "last updated" both derive from it.
export const correctionsData = rd(path.join(DATA, 'corrections.json'));
const _corrDates = (correctionsData.entries || []).map(e => e.date).sort();
export const lastCorrection = _corrDates.at(-1) || TODAY;
export function pageChanged(o) {
  const cd = (correctionsData.entries || []).filter(e => (e.pages || []).includes(o.slug)).map(e => e.date).sort().at(-1);
  return [o.dataUpdated, cd].filter(Boolean).sort().at(-1) || o.dataUpdated;
}
export const HUB_MODELS = [['toyota', 'rav4'], ['ford', 'f-150'], ['toyota', 'camry'], ['honda', 'cr-v']];

export const hasVal = f => !!f && f.value != null && f.value !== '' && !/todo/i.test(String(f.value));
const manualGrade = f => hasVal(f) && f.sourceGrade === 'A' && !!f.source;

export function vehicleUrl(v) { return `/specs/${v.makeSlug}/${v.modelSlug}/${v.year}/`; }
export function issueUrl(i) { return `/${i.type === 'code' ? 'codes' : 'symptoms'}/${i.slug}/`; }

function common(o, reasons) {
  if (!o.signOff?.by || !o.signOff?.date) reasons.push('no human sign-off (signOff)');
  const day = releaseDayOf(o.slug);
  if (day == null) reasons.push('not in data/release-order.json');
  else if (day > RELEASE_DAY) reasons.push(`release day ${day} (building day ${RELEASE_DAY})`);
}
export const goodTireRows = v => (v.tires?.rows || []).filter(x => x.tireSize && x.frontPsi && x.rearPsi && x.source && x.sourceGrade === 'A');
// GM/Ford-style manuals print no per-vehicle psi figure at all: they point to the
// Tire and Loading Information label on the door jamb. A page can still ship when it
// carries grade-A tire sizes AND a cited placard note proving the omission is the
// OEM's, not ours (data field tires.psiOnLabel: { source, page, note }).
export const tireSizeRows = v => (v.tires?.rows || []).filter(x => x.tireSize && x.source && x.sourceGrade === 'A');
export const placardNote = v => { const p = v.tires?.psiOnLabel; return p && p.source && p.page ? p : null; };
export const tireLabel = t => [t.config, t.wheel && !(t.config || '').includes(`${t.wheel}-inch`) ? `${t.wheel}-in` : null, t.tireSize].filter(Boolean).join(' · ');
function tireCheck(v, r) {
  const good = goodTireRows(v);
  const placard = placardNote(v);
  const sizes = tireSizeRows(v);
  if (!good.length && !(placard && sizes.length)) r.push('no tire row with size + front/rear psi from grade-A manual');
  const labels = good.map(tireLabel); const dup = labels.filter((l, i) => labels.indexOf(l) !== i);
  const noPsi = (v.tires?.rows || []).filter(x => !(x.frontPsi && x.rearPsi));
  if (noPsi.length && !placard) r.push(`${noPsi.length} of ${(v.tires?.rows || []).length} tire rows lack grade-A front/rear psi`);
  if (dup.length) r.push(`tire rows not distinguishable (duplicate label: ${[...new Set(dup)].join('; ')})`);
}
export function vehicleGate(v) {
  const r = [], s = v.specs;
  if (v.manual?.yearConfirmed === false) r.push('owner manual model year not confirmed');
  if (v.powertrain === 'ev') {
    tireCheck(v, r);
    if (!hasVal(s.evRange)) r.push('EV range (fueleconomy.gov) missing');
    if (!hasVal(s.evEfficiency)) r.push('EV efficiency (fueleconomy.gov) missing');
  } else {
    tireCheck(v, r);
    for (const k of ['oilCapacity', 'oilViscosity'])
      if (!manualGrade(s[k])) r.push(`${k} lacks grade-A manual source`);
    if (!v.fuelEconomyFetched || !v.fuelEconomy.length) r.push('fuel economy not fetched');
  }
  if (!v.recallsFetched) r.push('recalls not fetched');
  const dataReady = r.length === 0;
  common(v, r);
  return { pass: r.length === 0, dataReady, reasons: r };
}
// Only grade-A cited items count toward the gate and are rendered
export const sourcedCauses = i => (i.causes || []).filter(c => c.text && c.url && c.sourceGrade === 'A');
export const sourcedUrgency = i => (i.urgency || []).filter(c => c.text && c.url && c.sourceGrade === 'A' && forThisCode(c, i));
export const guidance = i => (i.guidance || []).filter(g => g.url && g.sourceGrade === 'A');
const isDrive = g => /can_i_keep_driving|flashing|reduce speed|stop/i.test(g.answers);
// Entries tagged onlyCodes are quoted only where they apply (e.g. the flashing-light
// misfire wording stays on misfire codes and is not printed on EVAP or catalyst pages).
const forThisCode = (g, i) => !g.onlyCodes || (!!i.code && g.onlyCodes.includes(i.code));
export const allBrandDrive = i => guidance(i).filter(g => g.allBrands && isDrive(g) && forThisCode(g, i));
export function issueGate(i) {
  const r = [];
  // R-Q1 v2: can-I-drive or severity sourced + >=1 sourced cause; cost optional
  if (allBrandDrive(i).length < 1) r.push((sourcedUrgency(i).length || guidance(i).length) ? 'can-I-drive source is brand-specific only (needs all-brand grade-A source, e.g. EPA/NHTSA)' : 'no grade-A can-I-drive source');
  if (sourcedCauses(i).length < 1) r.push('no grade-A cause');
  const dataReady = r.length === 0;
  common(i, r);
  return { pass: r.length === 0, dataReady, reasons: r };
}
// What gets generated: production = gate pass only; PREVIEW=1 = everything (noindex, banner)
export const MAX_TIRE_ROWS = 10;
export const shownTireRows = v => (v.tires?.rows || []).filter(t => t.source && t.sourceGrade === 'A' && (t.tireSize || t.frontPsi));
export const liveVehicles = vehicles.filter(v => PREVIEW || vehicleGate(v).pass);
export const liveIssues = issues.filter(i => PREVIEW || issueGate(i).pass);
export const isIndexable = o => ('powertrain' in o ? vehicleGate(o) : issueGate(o)).pass;
export const liveIssueHub = type => liveIssues.some(i => i.type === type);
export function liveHubs() {
  return HUB_MODELS.map(([mk, md]) => ({ makeSlug: mk, modelSlug: md, years: liveVehicles.filter(v => v.makeSlug === mk && v.modelSlug === md).sort((a, b) => b.year - a.year) }))
    .filter(h => h.years.length >= 2);
}

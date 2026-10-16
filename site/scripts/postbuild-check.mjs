// Post-build SEO/quality checks (seo-dev-requirements R-Q1/Q3, R-M1/M2, R-S1, R-D4, R-L3/L4, R-U1).
// Writes reports/build-report.md and exits 1 on any P0 failure.
import fs from 'node:fs'; import path from 'node:path';
import { vehicles, issues, vehicleGate, issueGate, vehicleUrl, issueUrl, pilotUrls, PREVIEW, TODAY } from '../src/lib/gate.mjs';
const DIST = 'dist', SITE = 'https://carspecfix.com';
const errors = [], warns = [], out = [];
const files = []; (function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p) : files.push(p); } })(DIST);
const html = files.filter(f => f.endsWith('.html'));
const urlOf = f => '/' + path.relative(DIST, f).replace(/index\.html$/, '').replace(/\\/g, '/');
const pages = {};
const sm = fs.readFileSync(path.join(DIST, 'sitemap.xml'), 'utf8');
for (const f of html) {
  const s = fs.readFileSync(f, 'utf8'), u = urlOf(f);
  if (u === '/404.html') continue;
  pages[u] = { s, title: (s.match(/<title>(.*?)<\/title>/) || [])[1], h1: (s.match(/<h1[\s>]/g) || []).length,
    canonical: (s.match(/rel="canonical" href="([^"]+)"/) || [])[1], noindex: /name="robots" content="noindex/.test(s),
    links: [...s.matchAll(/<a [^>]*href="(\/[^"#?]*)/g)].map(m => m[1]), body: s.replace(/<header[\s\S]*?<\/header>|<footer[\s\S]*?<\/footer>|<nav[\s\S]*?<\/nav>/g, '') };
}
// R-Q3: no TODO anywhere; placeholder marker blocked in production
for (const f of files.filter(f => /\.(html|xml|txt)$/.test(f))) {
  const s = fs.readFileSync(f, 'utf8');
  if (/todo/i.test(s)) errors.push(`R-Q3 "todo" found in ${f}`);
  if (!PREVIEW && /PENDING-队长/.test(s)) warns.push(`placeholder [PENDING-队长] in ${urlOf(f)} — must be filled before deploy`);
}
const descs = {};
// R-M1 / R-M2
const titles = {};
for (const [u, p] of Object.entries(pages)) {
  if (p.canonical !== SITE + u) errors.push(`R-M1 canonical mismatch ${u}: ${p.canonical}`);
  if (p.h1 !== 1) errors.push(`R-M2 ${u} has ${p.h1} H1`);
  (titles[p.title] ||= []).push(u);
  const vis = p.title.replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/&quot;/g, '"');
  { const dm = p.s.match(/<meta name="description" content="([^"]*)"/); const dd = dm ? dm[1].replace(/&amp;|&#38;/g, '&').replace(/&#39;/g, "'").replace(/&quot;/g, '"') : ''; descs[u] = dd; if (dd.length > 160) warns.push(`R-M1 description >160 chars (${dd.length}): ${u}`); }
  if (vis.length > 60) errors.push(`R-M2 title >60 chars (${vis.length}): ${u} "${vis}"`);
  if (/"@type":"(HowTo|Product|Offer|AggregateRating|Review|FAQPage)"/.test(p.s)) errors.push(`R-D3/D4 forbidden schema type on ${u}`);
  if (!/<html lang="en-US">/.test(p.s)) errors.push(`R-M3 lang must be en-US: ${u}`);
  if (/hreflang/.test(p.s)) errors.push(`R-M3 hreflang present: ${u}`);
  if (!PREVIEW && p.noindex) errors.push(`R-Q1 noindex on non-404 page: ${u}`);
  if (/repairpal|repair cost|rough cost|\$\d/i.test(p.s.replace(/<script[\s\S]*?<\/script>/g, ''))) errors.push(`cost/RepairPal wording on ${u}`);
  for (const im of p.s.matchAll(/<img [^>]*>/g)) if (!/width="\d+"/.test(im[0]) || !/height="\d+"/.test(im[0])) errors.push(`R-I1 img without width/height on ${u}`);
}
for (const [t, us] of Object.entries(titles)) if (us.length > 1) errors.push(`R-M2 duplicate title "${t}": ${us.join(', ')}`);
const linkCounts = {};
// Links: broken internal links + orphans (R-L3) + link count (R-L4)
const inbound = {};
for (const [u, p] of Object.entries(pages)) {
  for (const l of new Set(p.links)) {
    if (!pages[l] && !fs.existsSync(path.join(DIST, l))) errors.push(`R-L3 broken link ${u} -> ${l}`);
    else if (pages[l]?.noindex && !PREVIEW) errors.push(`R-L3 link to noindex page ${u} -> ${l}`);
    if (l !== u) (inbound[l] ||= new Set()).add(u);
  }
  // R-L4 v2: count only internal nav/recommendation links (href="/..."); in-page anchors, source citations (external) and image licence links are excluded
  const bodyLinks = (p.body.match(/<a [^>]*href="\/[^"]*"/g) || []).length; linkCounts[u] = bodyLinks;
  if (u !== '/sources/') { if (bodyLinks > 50) errors.push(`R-L4 ${u} has ${bodyLinks} internal links (>50)`); else if (bodyLinks > 30) warns.push(`R-L4 ${u} has ${bodyLinks} internal links (>30)`); } else if (bodyLinks > 100) warns.push(`R-L4 ${u} has ${bodyLinks} links`);
  const ext = [...p.body.replace(/<figcaption[\s\S]*?<\/figcaption>/g, '').matchAll(/<a [^>]*href="(https?:[^"]+)"/g)].map(m => m[1]); const d = ext.filter((x, i) => ext.indexOf(x) !== i);
  if (d.length) errors.push(`R-L5 ${u} links the same source more than once: ${[...new Set(d)].join(', ')}`);
}
const contentUrls = Object.keys(pages).filter(u => /^\/(specs|codes|symptoms)\/.+/.test(u));
for (const u of contentUrls) if ((inbound[u]?.size || 0) < 1) (PREVIEW ? warns : errors).push(`R-L3 orphan: ${u} has no inbound links`);
// R-S1 sitemap
for (const [, loc] of sm.matchAll(/<loc>([^<]+)<\/loc>/g)) {
  const u = loc.replace(SITE, ''); const p = pages[u];
  if (!p) errors.push(`R-S1 sitemap URL not built: ${u}`); else if (p.noindex) errors.push(`R-S1 sitemap URL is noindex: ${u}`);
}
// R-U1 v2: every live URL is in pages.csv P1 (not all must be live)
const liveUrls = Object.keys(pages).filter(u => /^\/(specs\/[^/]+\/[^/]+\/\d{4}|codes\/[^/]+|symptoms\/[^/]+)\/$/.test(u));
const diff = liveUrls.filter(u => !pilotUrls.includes(u));
if (diff.length) errors.push(`R-U1 live URLs not in pages.csv P1: ${diff.join(', ')}`);
// Unsigned/blocked pages must be absent everywhere (files, sitemap, links)
for (const o of [...vehicles.map(v => [vehicleUrl(v), vehicleGate(v)]), ...issues.map(i => [issueUrl(i), issueGate(i)])]) {
  if (o[1].pass || PREVIEW) continue;
  if (pages[o[0]]) errors.push(`blocked page was generated: ${o[0]}`);
  if (sm.includes(SITE + o[0])) errors.push(`blocked page in sitemap: ${o[0]}`);
  if (inbound[o[0]]) errors.push(`blocked page linked from: ${[...inbound[o[0]]].join(', ')}`);
}
const newToday = liveUrls.filter(u => !/^\/specs\/[^/]+\/[^/]+\/$/.test(u)).length; // informational

// Gate report (R-Q1)
out.push(`# Build report (${PREVIEW ? 'PREVIEW' : 'production'}, RELEASE_DAY=${process.env.RELEASE_DAY || 1}, date ${TODAY})`, '', `live URLs outside pages.csv P1: ${diff.length} (pilot list ${pilotUrls.length} URLs, live ${liveUrls.length})`, '', '## Publish gate', '| URL | live | data ready | blocking reasons |', '|---|---|---|---|');
for (const o of [...vehicles.map(v => [vehicleUrl(v), vehicleGate(v)]), ...issues.map(i => [issueUrl(i), issueGate(i)])])
  out.push(`| ${o[0]} | ${o[1].pass ? 'YES' : 'no'} | ${o[1].dataReady ? 'yes' : 'no'} | ${o[1].reasons.join('; ')} |`);
out.push('', '## Meta descriptions', ...Object.entries(descs).map(([u, d]) => `- ${u} [${d.length}] ${d}`));
out.push('', '## Internal link counts (R-L4)', ...Object.entries(linkCounts).map(([u, n]) => `- ${u}: ${n}`));
out.push('', `## Errors (${errors.length})`, ...errors.map(e => '- ' + e), '', `## Warnings (${warns.length})`, ...warns.map(e => '- ' + e));
fs.mkdirSync('reports', { recursive: true }); fs.writeFileSync('reports/build-report.md', out.join('\n') + '\n');
console.log(`pages: ${Object.keys(pages).length}, live content pages: ${contentUrls.length}, errors: ${errors.length}, warnings: ${warns.length} -> reports/build-report.md`);
errors.forEach(e => console.log('ERROR', e));
process.exit(errors.length ? 1 : 0);

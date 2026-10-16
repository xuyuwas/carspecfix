// images/image_sources.csv -> public/img/*.webp + data/images.json. Only rows with signoff=yes are used.
import fs from 'node:fs'; import path from 'node:path'; import sharp from 'sharp';
const ROOT = new URL('../../', import.meta.url).pathname, IMG = ROOT + 'images/';
const OUT = new URL('../public/img/', import.meta.url).pathname, DATA = new URL('../data/images.json', import.meta.url).pathname;
// Strict RFC-4180 parser: throws on unbalanced quotes, stray quotes, or rows whose column count != header.
function parseCsvStrict(txt, file) {
  const rows = []; let row = [], f = '', q = false, line = 1, rowLine = 1;
  for (let i = 0; i < txt.length; i++) {
    const c = txt[i];
    if (q) { if (c === '"') { if (txt[i + 1] === '"') { f += '"'; i++; } else { q = false; if (i + 1 < txt.length && !',\r\n'.includes(txt[i + 1])) throw new Error(`${file}: stray character after closing quote at line ${line}`); } } else { if (c === '\n') line++; f += c; } }
    else if (c === '"') { if (f !== '') throw new Error(`${file}: quote inside unquoted field at line ${line}`); q = true; }
    else if (c === ',') { row.push(f); f = ''; }
    else if (c === '\n') { row.push(f); rows.push({ row, line: rowLine }); row = []; f = ''; line++; rowLine = line; }
    else if (c !== '\r') f += c;
  }
  if (q) throw new Error(`${file}: unterminated quoted field starting near line ${rowLine}`);
  if (f !== '' || row.length) { row.push(f); rows.push({ row, line: rowLine }); }
  const data = rows.filter(r => !(r.row.length === 1 && r.row[0] === ''));
  const [h, ...rest] = data; const bad = rest.filter(r => r.row.length !== h.row.length);
  if (bad.length) throw new Error(`${file}: ${bad.length} of ${rest.length} rows have wrong column count (expected ${h.row.length}): lines ${bad.map(b => `${b.line}(${b.row.length})`).join(', ')}`);
  return rest.map(r => Object.fromEntries(h.row.map((k, i) => [k, r.row[i]])));
}
const REQUIRED = ['slug', 'file', 'commons_page_url', 'author', 'license', 'license_url', 'required_attribution_text', 'reviewed_by', 'reviewed_at', 'signoff'];
const OVERRIDES_ = JSON.parse(fs.readFileSync(new URL('../data/caption-overrides.json', import.meta.url), 'utf8'));
if (process.env.IMAGES === 'skip') { fs.rmSync(OUT, { recursive: true, force: true }); fs.writeFileSync(DATA, '{}\n'); console.log('images: SKIPPED by IMAGES=skip (silhouettes everywhere)'); process.exit(0); }
let rows;
try {
  rows = parseCsvStrict(fs.readFileSync(IMG + 'image_sources.csv', 'utf8'), 'image_sources.csv');
  const miss = REQUIRED.filter(k => !(k in (rows[0] || {}))); if (miss.length) throw new Error(`image_sources.csv: missing columns ${miss.join(', ')}`);
  console.log(`image_sources.csv: ${rows.length} rows parsed`);
} catch (e) { console.error('IMAGE IMPORT FAILED:', e.message, '\n(fix the CSV, or run with IMAGES=skip to build with silhouettes only)'); process.exit(1); }
const WIDTHS = [480, 800, 1200], out = {}, report = [];
fs.rmSync(OUT, { recursive: true, force: true });
for (const r of rows) {
  if (!r.file && !/^\d{4}-/.test(r.slug)) { report.push(`note row skipped: ${r.slug}`); continue; }
  if (out[r.slug]) continue;                       // first signed row per page wins
  if ((r.signoff || '').trim().toLowerCase() !== 'yes') { report.push(`${r.slug}: not signed (${path.basename(r.file)})`); continue; }
  const src = IMG + r.file; if (!fs.existsSync(src)) { report.push(`${r.slug}: file missing ${r.file}`); continue; }
  const meta = await sharp(src).metadata(); // dims of the (possibly cropped) file itself
  const base = path.basename(r.file).replace(/\.[^.]+$/, '').replace(/[^A-Za-z0-9_-]+/g, '-');
  fs.mkdirSync(OUT + r.slug, { recursive: true });
  const set = [];
  for (const w of WIDTHS.filter(w => w <= meta.width)) {
    const file = `${r.slug}/${base}-${w}.webp`; const info = await sharp(src).resize({ width: w }).webp({ quality: 72 }).toFile(OUT + file);
    set.push({ url: '/img/' + file, w, h: info.height });
  }
  const title = ((r.required_attribution_text || '').match(/"([^"]+)"/) || [])[1] || '';
  const shown = title.split(',')[0].replace(/\s+in\s+[A-Z][\w ]*$/, '').replace(/^(\d{4}) Toyota Rav4/i, '$1 Toyota RAV4').trim() || null; // pictured vehicle, e.g. "2024 Toyota RAV4 Hybrid Woodland Edition"
  const yr = (title.match(/^(\d{4}) /) || [])[1] || null;
  const cropped = /crop/i.test(r.file + ' ' + (r.notes || '') + ' ' + (r.cropped || ''));
  out[r.slug] = { cropped, shownOverride: OVERRIDES_[r.slug] || (r.caption ? (/^Shown:/.test(r.caption) ? r.caption : `Shown: ${r.caption}`) : null), set, width: set.at(-1).w, height: set.at(-1).h, author: r.author, license: r.license, licenseUrl: r.license_url,
    sourceUrl: r.commons_page_url, credit: r.required_attribution_text, photoYear: yr ? +yr : null, shown, title, signedBy: r.reviewed_by || null, signedAt: r.reviewed_at || null };
}
fs.writeFileSync(DATA, JSON.stringify(out, null, 2) + '\n');
console.log(`images: ${Object.keys(out).length} signed/rendered, ${report.length} skipped`); report.forEach(x => console.log('  skip', x));

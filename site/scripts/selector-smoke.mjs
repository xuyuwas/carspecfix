// End-to-end smoke test for the "find the numbers for your build" selector.
//
// Why this exists: the panel is the only part of the site where the answer is computed in
// the browser, and a broken selector fails *silently* — the server-rendered fallback stays
// on screen, so the page looks fine and simply answers for the wrong car. That happened
// once already: hiding the tyre-size field on a page with no psi table left `szSel` null,
// the first addEventListener threw, and the drive dropdown was never populated.
//
// Run against a build before publishing:
//   node scripts/selector-smoke.mjs            (uses dist/, http://127.0.0.1:8899)
//   PLAYWRIGHT_CORE=/path/to/playwright-core node scripts/selector-smoke.mjs
//
// Exits non-zero on any failure so it can gate a deploy.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import http from 'node:http';

const require = createRequire(import.meta.url);
const DIST = 'dist';
const PORT = Number(process.env.SMOKE_PORT || 8899);
const CHROME = process.env.CHROME_BIN ||
  `${process.env.HOME}/Library/Caches/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-mac-arm64/chrome-headless-shell`;

function loadPlaywright() {
  const tried = [];
  for (const p of [process.env.PLAYWRIGHT_CORE, 'playwright-core', '/Users/buc0011/.workbuddy/binaries/node/workspace/node_modules/playwright-core'].filter(Boolean)) {
    try { return require(p); } catch (e) { tried.push(p); }
  }
  throw new Error(`playwright-core not found (tried: ${tried.join(', ')}) — set PLAYWRIGHT_CORE`);
}

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.webp': 'image/webp', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  let u = decodeURIComponent(req.url.split('?')[0]);
  let f = path.join(DIST, u);
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!fs.existsSync(f)) { res.writeHead(404); return res.end('nf'); }
  res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});

const pages = [];
(function walk(d) {
  for (const e of fs.readdirSync(d)) {
    const p = path.join(d, e);
    if (fs.statSync(p).isDirectory()) walk(p);
    else if (p.endsWith('index.html') && /[\\/]specs[\\/][^\\/]+[\\/][^\\/]+[\\/]\d{4}[\\/]index\.html$/.test(p)) pages.push(p);
  }
})(DIST);

const withPanel = pages.filter(f => fs.readFileSync(f, 'utf8').includes('data-cfg '));
if (!withPanel.length) { console.log('no vehicle pages with a selector found — nothing to test'); process.exit(0); }

const { chromium } = loadPlaywright();
await new Promise(r => server.listen(PORT, '127.0.0.1', r));
const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });

const fails = [];
const fix = (s) => s.replace(/\s+/g, ' ').trim();

for (const file of withPanel) {
  const url = 'http://127.0.0.1:' + PORT + '/' + path.relative(DIST, file).replace(/index\.html$/, '').replace(/\\/g, '/');
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  // Third-party scripts (gtag, AdSense, Ahrefs) throw "Uncaught (in promise) undefined"
  // when they cannot reach their servers, which is every run of this test off a build
  // machine. They are blocked here so a red result always means our own code.
  await page.route('**/*', r => {
    const u = r.request().url();
    return u.startsWith('http://127.0.0.1:' + PORT) || u.startsWith('data:') ? r.continue() : r.abort();
  });
  page.on('pageerror', e => { if (e.message) errors.push(e.message); });
  await page.goto(url, { waitUntil: 'load' });

  const model = await page.evaluate(() => {
    const el = document.querySelector('[data-cfg-data]');
    return el ? JSON.parse(el.textContent) : null;
  });
  if (!model) { fails.push(`${url}: no config payload`); await page.close(); continue; }

  const out = async () => fix(await page.$eval('[data-cfg-out]', e => e.innerText));

  // (1) the script must run at all: a thrown error leaves the server-rendered fallback
  //     on screen, which answers for every car instead of the reader's.
  if (errors.length) fails.push(`${url}: script threw — ${errors[0]}`);

  // (2) every control the page offers must be populated
  const driveOpts = await page.$$eval('[data-cfg-drive] option', o => o.length);
  const engineOpts = await page.$$eval('[data-cfg-engine] option', o => o.length);
  if (engineOpts < 2) fails.push(`${url}: engine select has ${engineOpts} option(s)`);
  const hasDrives = model.engines.some(e => (e.drives || []).length);
  if (hasDrives && driveOpts < 2) fails.push(`${url}: drive select was never populated (${driveOpts} option)`);

  // (3) every state must be finite, and must never show a number the data does not carry
  const allowed = new Set();
  model.engines.forEach(e => {
    [e.oil, ...(e.oilList || [])].filter(Boolean).forEach(o => {
      if (o.w != null) allowed.add(String(o.w));
      if (o.wo != null) allowed.add(String(o.wo));
    });
    (e.mpg || []).forEach(r => allowed.add(String(r.comb)));
  });
  model.sizes.forEach(s => s.psi.forEach(p => { allowed.add(String(p.front)); allowed.add(String(p.rear)); }));
  let min = Infinity, max = -Infinity;
  [...allowed].forEach(v => { const n = Number(v); if (Number.isFinite(n)) { min = Math.min(min, n); max = Math.max(max, n); } });

  const seen = new Set();
  for (let i = 0; i < engineOpts; i++) {
    await page.selectOption('[data-cfg-engine]', { index: i });
    // The drive list is rebuilt per engine, so its length is read again after every change.
    const n = await page.$$eval('[data-cfg-drive] option', o => o.length);
    for (let d = 0; d < n; d++) {
      try { await page.selectOption('[data-cfg-drive]', { index: d }, { timeout: 2000 }); }
      catch { fails.push(`${url}: drive option #${d} could not be selected for engine #${i}`); continue; }
      const t = await out();
      seen.add(t);
      if (/Infinity|NaN|undefined|null/.test(t)) fails.push(`${url}: non-finite artefact at engine#${i} drive#${d} — ${t.slice(0, 120)}`);
      if (errors.length) { fails.push(`${url}: script threw after a change — ${errors[0]}`); break; }
    }
  }
  // (4) changing a select must actually change something when the data differs
  const oilValues = new Set();
  model.engines.forEach(e => [e.oil, ...(e.oilList || [])].filter(Boolean).forEach(o => { if (o.w != null) oilValues.add(String(o.w)); }));
  if (oilValues.size > 1) {
    await page.selectOption('[data-cfg-engine]', { index: 0 });
    await page.selectOption('[data-cfg-drive]', { index: 0 });
    const a = await out();
    // pick the drive that owns a different oil figure, if the manual splits by drive
    const split = model.engines.some(e => (e.oilList || []).some(o => o.drive));
    if (split) {
      const labs = await page.$$eval('[data-cfg-drive] option', o => o.map(x => x.value));
      for (let d = 1; d < labs.length; d++) {
        await page.selectOption('[data-cfg-drive]', { index: d });
        if (await out() !== a) break;
      }
      const b = await out();
      if (a === b) fails.push(`${url}: drive split exists (${[...oilValues].join(' / ')} qt) but the oil cell does not change with drive`);
    }
  }
  console.log(`${url}  states=${seen.size}  ${errors.length ? 'ERRORS' : 'ok'}`);
  await page.close();
}

await browser.close();
server.close();
if (fails.length) {
  console.log('\nFAILED (' + fails.length + '):');
  fails.forEach(f => console.log(' - ' + f));
  process.exit(1);
}
console.log(`\nselector smoke: ${withPanel.length} pages, no failures`);

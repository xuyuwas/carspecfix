// Find GM owner-manual PDF URLs for a given year/model via the Chevrolet manuals page.
// Usage: NODE_PATH=... node scripts/gm-manual-find.mjs <year> <model-slug>
const _pw = await import('/Users/buc0011/.workbuddy/binaries/node/workspace/node_modules/playwright-core/index.js');
const chromium = _pw.chromium || _pw.default?.chromium;

const EXE = `${process.env.HOME}/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`;
const year = process.argv[2] || '2022';
const model = process.argv[3] || 'Equinox';

const browser = await chromium.launch({ executablePath: EXE, headless: true });
const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' });
const page = await ctx.newPage();

const pdfs = new Set();
page.on('response', r => {
  const u = r.url();
  if (/\.pdf(\?|$)/i.test(u) || /application\/pdf/.test(r.headers()['content-type'] || '')) pdfs.add(u);
});
page.on('request', r => {
  const u = r.url();
  if (/\.pdf(\?|$)/i.test(u)) pdfs.add(u);
});

const url = `https://www.chevrolet.com/support/vehicle/manuals-guides?compIndex=1&make=Chevrolet&model=${encodeURIComponent(model)}&year=${year}`;
await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
await page.waitForTimeout(9000);

// collect anchors
const anchors = await page.$$eval('a', as => as.map(a => ({ t: (a.textContent || '').trim().slice(0, 80), h: a.href })));
for (const a of anchors) if (/\.pdf/i.test(a.h)) pdfs.add(a.h);

console.log('--- pdf-ish urls ---');
for (const p of pdfs) console.log(p);
console.log('--- anchors mentioning manual ---');
for (const a of anchors) if (/manual/i.test(a.t) || /manual/i.test(a.h)) console.log(a.t, '=>', a.h);

await browser.close();

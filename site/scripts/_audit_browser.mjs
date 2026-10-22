// Real-browser measurement of carspecfix.com: request counts, transfer bytes by
// type, LCP/CLS, DOM size, render-blocking assets, mobile overflow, screenshots.
// Read-only; run: node scripts/_audit_browser.mjs [url]
import pw from '/Users/buc0011/.workbuddy/binaries/node/workspace/node_modules/playwright-core/index.js';
const { chromium } = pw;
import fs from 'node:fs';

const EXE = '/Users/buc0011/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const URL = process.argv[2] || 'https://carspecfix.com/';

const browser = await chromium.launch({ executablePath: EXE });

async function run(label, viewport, shots) {
  const ctx = await browser.newContext({ viewport, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const reqs = [];
  page.on('response', async (res) => {
    const req = res.request();
    let len = 0;
    try { len = (await res.body()).length; } catch {}
    reqs.push({ url: res.url(), type: req.resourceType(), status: res.status(), bytes: len });
  });
  const t0 = Date.now();
  await page.goto(URL, { waitUntil: 'load', timeout: 90000 });
  const nav = await page.evaluate(() => {
    const n = performance.getEntriesByType('navigation')[0] || {};
    return {
      ttfb: Math.round(n.responseStart || 0),
      domContentLoaded: Math.round(n.domContentLoadedEventEnd || 0),
      load: Math.round(n.loadEventEnd || 0),
      transferSize: n.transferSize,
      domNodes: document.querySelectorAll('*').length,
      imgs: document.querySelectorAll('img').length,
      lazyImgs: [...document.querySelectorAll('img')].filter(i => i.loading === 'lazy').length,
      widthFixImgs: [...document.querySelectorAll('img')].filter(i => i.width && i.height).length,
      scripts: document.querySelectorAll('script[src]').length,
      inlineScripts: [...document.querySelectorAll('script:not([src])')].map(s => s.textContent.length),
      css: document.querySelectorAll('link[rel=stylesheet]').length,
      fontDisplay: [...document.styleSheets].length,
      overflow: document.documentElement.scrollWidth - window.innerWidth,
      bodyFont: getComputedStyle(document.body).fontFamily,
    };
  });
  // LCP via observer replay
  const lcp = await page.evaluate(() => new Promise(res => {
    const out = { t: 0, el: '' };
    try {
      new PerformanceObserver(list => {
        const e = list.getEntries(); const last = e[e.length - 1];
        out.t = Math.round(last.startTime); out.el = (last.element ? last.element.tagName + '.' + (last.element.className || '') : '') + ' | ' + (last.url || '');
      }).observe({ type: 'largest-contentful-paint', buffered: true });
    } catch {}
    setTimeout(() => res(out), 2500);
  }));
  const cls = await page.evaluate(() => new Promise(res => {
    let v = 0;
    try {
      new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) v += e.value; }).observe({ type: 'layout-shift', buffered: true });
    } catch {}
    setTimeout(() => res(Math.round(v * 1000) / 1000), 2000);
  }));

  const gzip = reqs.filter(r => r.type !== 'document');
  const byType = {};
  for (const r of reqs) { byType[r.type] = byType[r.type] || { n: 0, b: 0 }; byType[r.type].n++; byType[r.type].b += r.bytes; }

  console.log(`\n===== ${label} ${viewport.width}x${viewport.height} =====`);
  console.log('wall ms', Date.now() - t0, '| nav', JSON.stringify(nav));
  console.log('LCP', lcp.t, 'ms |', lcp.el.slice(0, 160));
  console.log('CLS', cls);
  console.log('requests', reqs.length, JSON.stringify(byType));
  console.log('total bytes', reqs.reduce((a, r) => a + r.bytes, 0));
  const big = reqs.filter(r => r.bytes > 60000).sort((a, b) => b.bytes - a.bytes).slice(0, 8);
  console.log('heaviest:'); big.forEach(r => console.log('  ', r.bytes, r.type, r.url.replace('https://carspecfix.com', '')));
  const failed = reqs.filter(r => r.status >= 400);
  if (failed.length) { console.log('failed requests:'); failed.forEach(r => console.log('  ', r.status, r.url)); }

  if (shots) {
    await page.screenshot({ path: `/tmp/shot-${label}.png`, fullPage: false });
    fs.writeFileSync(`/tmp/reqs-${label}.json`, JSON.stringify(reqs, null, 1));
  }
  await ctx.close();
}

await run('mobile', { width: 390, height: 844 }, true);
await run('desktop', { width: 1440, height: 900 }, true);
await browser.close();

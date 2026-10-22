// Pass 2: transfer (compressed) sizes per resource + CLS source attribution.
import pw from '/Users/buc0011/.workbuddy/binaries/node/workspace/node_modules/playwright-core/index.js';
const { chromium } = pw;
const EXE = '/Users/buc0011/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const URL = process.argv[2] || 'https://carspecfix.com/';
const browser = await chromium.launch({ executablePath: EXE });

async function run(label, viewport, target) {
  const ctx = await browser.newContext({ viewport });
  const page = await ctx.newPage();
  await page.goto(target, { waitUntil: 'load', timeout: 90000 });
  await page.waitForTimeout(4000);
  const out = await page.evaluate(() => {
    const res = performance.getEntriesByType('resource').map(r => ({
      name: r.name.replace(location.origin, ''), type: r.initiatorType,
      transfer: r.transferSize, decoded: r.decodedBodySize, ms: Math.round(r.duration),
    }));
    const nav = performance.getEntriesByType('navigation')[0];
    return {
      nav: { ttfb: Math.round(nav.responseStart), dcl: Math.round(nav.domContentLoadedEventEnd), load: Math.round(nav.loadEventEnd), htmlTransfer: nav.transferSize, htmlDecoded: nav.decodedBodySize },
      res,
      totalTransfer: res.reduce((a, r) => a + r.transfer, 0) + nav.transferSize,
    };
  });
  // CLS attribution
  const cls = await page.evaluate(() => new Promise(res => {
    const shifts = [];
    try {
      new PerformanceObserver(l => {
        for (const e of l.getEntries()) {
          if (e.hadRecentInput) continue;
          shifts.push({
            value: Math.round(e.value * 1000) / 1000,
            t: Math.round(e.startTime),
            sources: (e.sources || []).map(s => ({
              node: s.node ? (s.node.tagName + '.' + (s.node.className || '')).slice(0, 90) : '?',
              prev: s.previousRect ? `${Math.round(s.previousRect.y)}h${Math.round(s.previousRect.height)}` : '',
              cur: s.currentRect ? `${Math.round(s.currentRect.y)}h${Math.round(s.currentRect.height)}` : '',
            })),
          });
        }
      }).observe({ type: 'layout-shift', buffered: true });
    } catch {}
    setTimeout(() => res(shifts), 2500);
  }));

  console.log(`\n===== ${label} =====`);
  console.log('nav', JSON.stringify(out.nav), '| total transfer', out.totalTransfer, 'B =', Math.round(out.totalTransfer / 1024), 'KB');
  const g = {};
  for (const r of out.res) { const k = r.type; g[k] = g[k] || { n: 0, transfer: 0, decoded: 0 }; g[k].n++; g[k].transfer += r.transfer; g[k].decoded += r.decoded; }
  console.log('by type (transfer/decoded):', JSON.stringify(g));
  out.res.sort((a, b) => b.transfer - a.transfer).slice(0, 8).forEach(r => console.log('  ', r.transfer, '/', r.decoded, r.type, r.name.slice(0, 90)));
  console.log('CLS events', cls.length, 'sum', cls.reduce((a, c) => a + c.value, 0).toFixed(3));
  cls.slice(0, 6).forEach(c => console.log('  ', c.value, '@', c.t, JSON.stringify(c.sources)));
  await ctx.close();
}
await run('home-mobile', { width: 390, height: 844 }, URL);
await run('rav4-2024-mobile', { width: 390, height: 844 }, URL.replace(/\/$/, '') + '/specs/toyota/rav4/2024/');
await browser.close();
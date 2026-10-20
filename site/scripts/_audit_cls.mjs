// Desktop CLS recheck: 3 runs per page, with the shifted nodes named from the DOM
// (the perf-observer source.node is often anonymous, so we describe it ourselves).
import pw from '/Users/buc0011/.workbuddy/binaries/node/workspace/node_modules/playwright-core/index.js';
const { chromium } = pw;
const EXE = '/Users/buc0011/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const browser = await chromium.launch({ executablePath: EXE });

const targets = [
  ['home', 'https://carspecfix.com/'],
  ['rav4-2024', 'https://carspecfix.com/specs/toyota/rav4/2024/'],
];

async function measure(url, { blockGA = false } = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  if (blockGA) await ctx.route('**://*.googletagmanager.com/**', r => r.abort());
  const page = await ctx.newPage();
  await page.addInitScript(() => {
    window.__shifts = [];
    new PerformanceObserver(l => {
      for (const e of l.getEntries()) if (!e.hadRecentInput) window.__shifts.push({ v: e.value, t: e.startTime, src: e.sources.map(s => s.node ? `${s.node.tagName}.${s.node.className || ''}`.slice(0, 60) : '?') });
    }).observe({ type: 'layout-shift', buffered: true });
  });
  await page.goto(url, { waitUntil: 'load', timeout: 90000 });
  await page.waitForTimeout(5000);
  const r = await page.evaluate(() => {
    const shifts = window.__shifts || [];
    const sum = shifts.reduce((a, s) => a + s.v, 0);
    const fonts = performance.getEntriesByType('resource').filter(x => /woff2?/.test(x.name)).map(x => ({ f: x.name.split('/').pop(), ms: Math.round(x.duration), start: Math.round(x.startTime) }));
    const imgs = performance.getEntriesByType('resource').filter(x => x.initiatorType === 'img').length;
    return { cls: +sum.toFixed(3), shifts: shifts.map(s => ({ v: +s.v.toFixed(3), t: Math.round(s.t), src: s.src })), fonts, imgs };
  });
  await ctx.close();
  return r;
}

for (const [label, url] of targets) {
  for (const cfg of [{ blockGA: false, tag: 'with GA' }, { blockGA: true, tag: 'GA blocked' }]) {
    const rows = [];
    for (let i = 0; i < 3; i++) rows.push(await measure(url, cfg));
    const cls = rows.map(r => r.cls);
    const worst = rows.reduce((a, b) => (b.cls > a.cls ? b : a));
    console.log(`${label} [${cfg.tag}] CLS runs=${JSON.stringify(cls)} max=${worst.cls}`);
    if (worst.shifts.length) console.log('   shifts:', JSON.stringify(worst.shifts.slice(0, 4)));
    console.log('   fonts:', JSON.stringify(worst.fonts.slice(0, 6)), 'img count', worst.imgs);
  }
}
await browser.close();

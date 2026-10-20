// Measures how much wider the system fallback renders than the self-hosted webfont.
// Used to derive size-adjust for a metric-matched fallback @font-face, so the swap
// cannot change line count (which is what produces the desktop CLS on the home grid).
import pw from '/Users/buc0011/.workbuddy/binaries/node/workspace/node_modules/playwright-core/index.js';
const { chromium } = pw;
const EXE = '/Users/buc0011/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const browser = await chromium.launch({ executablePath: EXE });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
await page.goto('https://carspecfix.com/', { waitUntil: 'load', timeout: 90000 });
await page.waitForTimeout(2500);

const r = await page.evaluate(async () => {
  await document.fonts.ready;
  const mk = (fam, size, weight, text) => {
    const s = document.createElement('span');
    s.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;font:' + weight + ' ' + size + 'px ' + fam;
    s.textContent = text;
    document.body.appendChild(s);
    const w = s.getBoundingClientRect().width;
    s.remove();
    return w;
  };
  const capText = document.querySelector('.vcard figcaption').textContent.trim();
  const bodyText = 'Oil \u00b7 Tires \u00b7 Recalls';
  const nameText = 'Chevrolet Silverado 1500';
  const sys = 'system-ui, -apple-system, "Segoe UI", Arial';
  return {
    capText,
    capWeb: mk('"Source Sans 3"', 11, 400, capText),
    capSys: mk(sys, 11, 400, capText),
    bodyWeb: mk('"Source Sans 3"', 13, 400, bodyText),
    bodySys: mk(sys, 13, 400, bodyText),
    nameWeb: mk('"Archivo"', 18, 800, nameText),
    nameSys: mk(sys, 18, 800, nameText),
  };
});

const pct = (web, sys) => ((sys / web) * 100).toFixed(1);
console.log('caption text:', JSON.stringify(r.capText.slice(0, 70)));
console.log('caption  SS3 ' + r.capWeb.toFixed(1) + ' vs sys ' + r.capSys.toFixed(1) + '  -> size-adjust ' + pct(r.capWeb, r.capSys) + '%');
console.log('body     SS3 ' + r.bodyWeb.toFixed(1) + ' vs sys ' + r.bodySys.toFixed(1) + '  -> size-adjust ' + pct(r.bodyWeb, r.bodySys) + '%');
console.log('name     Archivo ' + r.nameWeb.toFixed(1) + ' vs sys ' + r.nameSys.toFixed(1) + ' -> size-adjust ' + pct(r.nameWeb, r.nameSys) + '%');
await browser.close();

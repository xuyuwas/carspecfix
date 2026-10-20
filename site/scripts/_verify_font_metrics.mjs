// Confirms the fallback metric fix: caption line count and grid height must be identical
// before and after the webfont swap. If they match, font-display:swap can no longer
// produce the 89px grid collapse that caused the desktop CLS.
import pw from '/Users/buc0011/.workbuddy/binaries/node/workspace/node_modules/playwright-core/index.js';
const { chromium } = pw;
const EXE = '/Users/buc0011/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const URL = process.argv[2] || 'http://127.0.0.1:8811/';
const browser = await chromium.launch({ executablePath: EXE });

async function probe(blockFonts) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  if (blockFonts) await ctx.route('**/*.{woff,woff2}', r => r.abort());
  const page = await ctx.newPage();
  await page.goto(URL, { waitUntil: 'load', timeout: 60000 });
  await page.waitForTimeout(1200);
  const r = await page.evaluate(() => {
    const caps = [...document.querySelectorAll('.vcard figcaption')].map(f => Math.round(f.getBoundingClientRect().height));
    const g = document.querySelector('.vgrid');
    return { caps, capMax: Math.max(...caps), gridH: g ? Math.round(g.getBoundingClientRect().height) : null, docH: document.body.scrollHeight };
  });
  await ctx.close();
  return r;
}

const on = await probe(false);
const off = await probe(true);
console.log('webfont ON   captionHeights', JSON.stringify(on.caps.slice(12, 18)), 'max', on.capMax, 'gridH', on.gridH, 'docH', on.docH);
console.log('webfont OFF  captionHeights', JSON.stringify(off.caps.slice(12, 18)), 'max', off.capMax, 'gridH', off.gridH, 'docH', off.docH);
console.log(on.gridH === off.gridH && on.docH === off.docH ? 'PASS: 换字前后布局一致' : 'FAIL: 仍存在布局差 ' + (off.gridH - on.gridH) + 'px');
await browser.close();

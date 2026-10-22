// Screenshot a few key templates for visual QA.
import pw from '/Users/buc0011/.workbuddy/binaries/node/workspace/node_modules/playwright-core/index.js';
const { chromium } = pw;
const EXE = '/Users/buc0011/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const browser = await chromium.launch({ executablePath: EXE });
const shots = [
  ['spec-mobile', 'https://carspecfix.com/specs/toyota/rav4/2024/', { width: 390, height: 844 }],
  ['spec-desktop', 'https://carspecfix.com/specs/toyota/rav4/2024/', { width: 1440, height: 900 }],
  ['code-desktop', 'https://carspecfix.com/codes/p0420/', { width: 1440, height: 900 }],
  ['specs-hub-desktop', 'https://carspecfix.com/specs/', { width: 1440, height: 900 }],
];
for (const [name, url, vp] of shots) {
  const ctx = await browser.newContext({ viewport: vp });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  await page.waitForTimeout(1200);
  await page.screenshot({ path: `/tmp/shot-${name}.png` });
  const m = await page.evaluate(() => ({
    h1: document.querySelector('h1')?.innerText,
    textAboveFold: document.body.innerText.slice(0, 260),
    h2s: [...document.querySelectorAll('h2')].map(x => x.innerText.trim()).slice(0, 12),
    tables: document.querySelectorAll('table').length,
    overflow: document.documentElement.scrollWidth - innerWidth,
  }));
  console.log(name, JSON.stringify(m).slice(0, 700));
  await ctx.close();
}
await browser.close();

// Push today's new/changed URLs to IndexNow (Bing/Yandex; Google does not use IndexNow).
// Usage: INDEXNOW_KEY=<key> node scripts/indexnow.mjs [--dry-run]   (key file must be served at /<key>.txt)
// NOT called anywhere yet: activate in .github/workflows/daily-build.yml after launch approval.
import fs from 'node:fs';
const key = process.env.INDEXNOW_KEY, dry = process.argv.includes('--dry-run') || !key;
const sm = fs.readFileSync('dist/sitemap.xml', 'utf8');
const today = process.env.BUILD_DATE || new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York' }).format(new Date());
const urls = [...sm.matchAll(/<loc>([^<]+)<\/loc><lastmod>([^<]+)<\/lastmod>/g)].filter(m => m[2] === today).map(m => m[1]);
const payload = { host: 'carspecfix.com', key, keyLocation: `https://carspecfix.com/${key}.txt`, urlList: urls };
if (dry || !urls.length) { console.log('[dry-run] IndexNow payload:', JSON.stringify({ ...payload, key: key ? '***' : null })); process.exit(0); }
const r = await fetch('https://api.indexnow.org/indexnow', { method: 'POST', headers: { 'Content-Type': 'application/json; charset=utf-8' }, body: JSON.stringify(payload) });
console.log('IndexNow', r.status, urls.length, 'urls'); if (![200, 202].includes(r.status)) process.exit(1);

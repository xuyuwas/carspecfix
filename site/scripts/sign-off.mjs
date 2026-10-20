#!/usr/bin/env node
// Human sign-off: marks a data page as reviewed by a person.
// Usage: node scripts/sign-off.mjs <slug> [<slug> ...] --by "Name"
// Example: node scripts/sign-off.mjs 2021-toyota-rav4 2014-toyota-rav4 --by 队长
// A page only goes live when it is signed AND listed in data/release-order.json
// on a day <= RELEASE_DAY AND passes the gate.
import fs from 'node:fs';
import path from 'node:path';

const argv = process.argv.slice(2);
const byIdx = argv.indexOf('--by');
const by = byIdx >= 0 ? argv[byIdx + 1] : null;
const slugs = argv.filter((a, i) => a !== '--by' && i !== byIdx && i !== byIdx + 1);

if (!slugs.length || !by) {
  console.error('usage: node scripts/sign-off.mjs <slug> [<slug> ...] --by "Name"');
  process.exit(1);
}

const date = new Date().toISOString().slice(0, 10);
const DIRS = ['data/vehicles', 'data/issues'];
let done = 0;

for (const slug of slugs) {
  let file = null;
  for (const d of DIRS) {
    const p = path.join(d, `${slug}.json`);
    if (fs.existsSync(p)) { file = p; break; }
  }
  if (!file) { console.error(`  skip ${slug}: no data file`); continue; }
  const j = JSON.parse(fs.readFileSync(file, 'utf8'));
  j.signOff = { by, date };
  j.dataUpdated = date;
  fs.writeFileSync(file, JSON.stringify(j, null, 2) + '\n');
  console.log(`  signed ${slug} (${file}) by ${by} on ${date}`);
  done++;
}
console.log(`${done} page(s) signed. Rebuild with: npm run build`);

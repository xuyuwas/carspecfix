# CarSpecFix page templates

## Site structure
- `/` home: search by year/make/model + top symptoms + top codes
- `/specs/{make}/{model}/{year}/` spec page (15 at launch)
- `/specs/{make}/` and `/specs/{make}/{model}/` hub pages (list years / models)
- `/symptoms/{slug}/` symptom page; `/codes/{p0xxx}/` OBD code page
- `/codes/` and `/symptoms/` index hubs; `/about/`, `/sources/` (data methodology), `/contact/`, `/privacy/`
- No `TODO` value is ever rendered: hide the row and show "Not yet verified — check your owner's manual".

## Spec page
- Title: `{Year} {Make} {Model} Specs: Oil Capacity, Tire Size & Pressure, Recalls | CarSpecFix`
- H1: `{Year} {Make} {Model} Specs`
- Meta: `Owner's-manual specs for the {Year} {Make} {Model}: oil type & capacity, tire size & PSI, MPG and {N} NHTSA recalls — every number cited.`
- Sections:
  1. Quick spec table (all fields, each row with source + page)
  2. Engine oil (capacity w/ & w/o filter, viscosity) — manual page
  3. Tires (size, pressure, spare) — manual page
  4. Engines & MPG (fueleconomy.gov configs)
  5. Recalls (NHTSA campaign #, component, date, summary, link)
  6. Wipers / battery (only if cited; else hidden)
  7. Common symptoms for this vehicle → links to symptom/code pages
  8. Sources & last updated date
- Internal links: other years of same model, same-make hub, 3–5 symptom/code pages.
- Schema: `BreadcrumbList` + `Dataset`-style table is optional; use `Article` (author = pen name, dateModified) + `Car` (`vehicleModelDate`, `manufacturer`, `fuelEfficiency`). No fake ratings.

## Symptom / code page
- Title (symptom): `{Symptom}: Causes, Is It Safe to Drive & Repair Cost | CarSpecFix`
- Title (code): `{CODE} Code: {Definition} — Causes, Can You Drive & Repair Cost`
- H1: `{Symptom}` / `{CODE}: {Definition}`
- Meta: `What {symptom/code} means, the most likely causes, whether it's safe to keep driving, and typical repair costs (RepairPal national averages).`
- Sections:
  1. Quick answer box (meaning, severity, can I drive, cost range) — 50 words
  2. What it means (code: SAE definition)
  3. Common causes (ordered, each cited)
  4. How serious is it
  5. Can I drive with it (brakes/ABS: conservative safety wording)
  6. How it's diagnosed (what the shop will check)
  7. Repair cost table (repair | range | source | date)
  8. Related codes / symptoms
  9. Vehicles we have specs for → spec pages
  10. Sources + disclaimer ("not professional mechanical advice")
- Schema: `Article` + `BreadcrumbList` + `FAQPage` only for visible Q&A.

## Launch checklist
1. Register carspecfix.com (队长 decides) → Cloudflare DNS, HTTPS, www→apex 301.
2. Static build (e.g. Astro/Next export) from `spec_pages.csv` + `symptom_pages.json`.
3. robots.txt allow all + sitemap.xml with real lastmod; canonical on each page.
4. GSC: add Domain property (DNS TXT), submit sitemap. Bing Webmaster: import from GSC, submit sitemap.
5. IndexNow: host key file at `/{key}.txt`, ping `https://api.indexnow.org/indexnow` on each publish.
6. Release ~10 pages/day (day1: home, about, sources + 7 pages; days 2–3 rest).
7. Week 4–6 review in GSC: impressions vs CTR (see README decision rules).

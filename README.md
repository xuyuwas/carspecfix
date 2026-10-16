# carspecfix.com launch package (for 小码)

Files
- `spec_pages.csv` — 15 spec pages; API data filled, manual fields TODO except 2020 RAV4.
- `spec_api_data.json` — raw NHTSA recalls + fueleconomy.gov configs (fetched 2026-10-15).
- `symptom_pages.json` — 15 symptom/code pages; cost ranges from RepairPal (updated 2026-09-03) with URLs; causes/severity/can-drive TODO (need cited source).
- `templates.md` — URL structure, page templates, schema, launch checklist.
- `fetch.py` — re-run to refresh API data.

Hard rules
- Never publish a number without source. Render TODO fields as hidden, never as guesses.
- 2020 RAV4 manual figures come from Toyota OM0R024U; model year confirmed 2020 (Helm OM0R024U listing + Toyota digital path /rav4/2020/…/om0r024u/; verified 2026-10-15).
- RepairPal ranges are national averages excluding tax/location; always show the source link + date.
- Pen-name author + /sources/ methodology page; disclaimer on symptom pages.

Decision rules (week 4–6, GSC)
- impressions + clicks → scale to 200 spec + 50 symptom pages
- high impressions, very low CTR → AI answers eating clicks; pivot to cost/comparison content
- no impressions → fix indexing first

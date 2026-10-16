# QA build 5 — commit 64c32e1, days 2–3 (visual)

Build: fresh `PREVIEW=1 RELEASE_DAY=2/3 astro build --outDir /tmp/qa5-dayN` from 64c32e1 (0 errors; images.mjs not run). dist-day2/3 were built ~13 s before the commit timestamp, so I rebuilt fresh to be safe.
Screenshots: `qa-build-5/` (full page + top viewport at 1280 and 390). Measurements: `qa-build-5/qa.json`.
Pages: 2022/2024 Camry, 2022 Corolla, 2022 Tacoma, 2022 Accord, Camry hub, P0301, P0442, plus 2022 Civic and 2024 CR-V.

## Result: FAIL (1 blocking issue, on 4 pages)

### B1 — Engine oil card prints raw data strings (Camry 2022, Camry 2024, Corolla 2022, Accord 2022; Tacoma similar)
- Element: quick card › ENGINE OIL › the lines under the big number
- Expected: under the big number, only the without-filter amount for each engine (for example `2.5L A25A-FKS: 4.4 qt without`), in plain text, with no source codes, no pipes and no viscosity repeated.
- Actual:
  - /specs/toyota/camry/2022/ and /2024/: `3.5L V6 2GR-FKS: 5.6 qt without | HYBRID 2.5L: 4.8 qt with filter, 4.4 qt without, SAE 0W-16 (0W-20 allowed), GF-6B [OM06246U p.547]`
  - /specs/toyota/corolla/2022/: the same, plus `| HATCHBACK 2.0L: 4.9 qt with filter, 4.5 qt without, SAE 0W-16 (0W-20 allowed) [OM12Q05U p.516]`. The card ends up 6 lines tall.
  - /specs/honda/accord/2022/: `2.0L turbo: 4.6 US qt without [ATVA2222OM pp.558, 633, 635]`, and the viscosity line reads `0W-20 [ATVA2222OM pp.633, 635]`. Manual codes are showing in body text.
  - /specs/toyota/tacoma/2022/: the third line is a stray `with-filter not stated`. Suggested wording: `3.5L 2GR-FKS: 5.9 qt without (with-filter not stated)` on one line.
- Fix: split the pipe-delimited value into one line per engine/variant (`HYBRID 2.5L: 4.4 qt without`). Strip `[CODE p.x]` (the page reference already goes through [3]). Keep the viscosity line clean.

## Non-blocking
- N1 Tire card "Manual p.…" list: Camry shows 7 pages and Corolla 7 pages, unsorted (`p.558, p.559, p.560, p.513, p.514, p.519, p.520`). The list wraps to 2–3 lines on mobile. Sort it and collapse into ranges (`pp. 513–520, 558–560`).
- N2 Tacoma fuel-economy table is 830 px inside an 810 px column at 1280, so a small horizontal scroll appears on desktop. Let the Engine/transmission column wrap.
- The subnav overflowing at 390 is intended (it's a horizontal scroll container). Page overflow is 0 on every page at both widths.

## Passes
- Sidebar: only the sticky "On this page" TOC (13px, position sticky) on all spec and code pages, and hidden at 390.
- Camry hub: single column, 718 px table, no sidebar.
- Mobile hero: the photo sits below the quick card on every year page (for example Camry 931→947), at 8:3 (2.67). The credit ("Shown: … / Photo: author / license / Source") is present on all 7, and "same generation" is labelled where it applies.
- .pref letter-spacing: normal/0. No ads. Code pages have no hero.
- Quick cards with many tire rows (Camry has 14): 3 rows + "See all 14 →". The 3 columns stay equal height and don't overflow.
- Civic/CR-V "incl. filter": accepted as before.
- **Civic 2022 tire table: 810 px at 1280 (was 857), fits the 810 column. Source column shows "—" for all 4 rows** (waiting on 小站's page numbers). CR-V 2024: 810 px, fits. At 390 both scroll inside `.tbl-scroll` (760/356), as intended.
- P0301/P0442 "Can I keep driving?": rendered as a 13px/700 qa__q label inside the card, the same as day 1, which passed.

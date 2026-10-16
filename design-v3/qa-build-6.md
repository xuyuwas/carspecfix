# QA build 6 — commit 5a62b1d, days 2–3 (visual)
Build: PREVIEW=1 RELEASE_DAY=2/3 into /tmp/qa6-day2 and /tmp/qa6-day3. Both 0 errors; images.mjs not run.
Screenshots and measurements: qa-build-6/ (1280 and 390, full page plus top of page; qa.json).

## Result: FAIL (2 blocking)

### B1 — Tacoma oil card: the lines under the big number are not cleaned up
- URL: /specs/toyota/tacoma/2022/, quick card › ENGINE OIL › .qa__more
- Expected: without-filter only, one line per engine: `2.7L 2TR-FE: 5.8 qt without` / `3.5L 2GR-FKS: 5.9 qt without`.
- Actual: `2.7L 2TR-FE: 6.2 qt with filter, 5.8 qt without` / `3.5L 2GR-FKS: 5.9 qt without filter` / a stray line `with-filter not stated`. Both widths.
- The big number is correct: `5.8–5.9` with "qt without filter" right next to it, 8px gap, 16px (the caption is 12px), shown as a block and visible. There is no "incl. filter".

### B2 — Camry overview: Oil capacity column not clean
- URL: /specs/toyota/camry/, table › Oil capacity column (both year rows)
- Expected: short capacity only, for example `2.5L 4.4 qt · V6 5.6 qt · Hybrid 4.4 qt` (without filter, like the card).
- Actual: the raw string `2.5L A25A-FKS: 4.8 qt with filter, 4.4 qt without; 3.5L V6 2GR-FKS: 5.7 qt with filter, 5.6 qt without; HYBRID 2.5L: 4.8 qt with filter, 4.4 qt without, SAE 0W-16 (0W-20 allowed), GF-6B`. Viscosity and grade are mixed into the capacity column.
- The overview has no 12V battery row. On the year pages the 12V row in the specs table is readable text with no codes, so that passes.

## Fixed / passes
- Oil cards on Camry 2022 and 2024, Corolla 2022 and Accord 2022: one engine per line, without-filter only, no [CODE p.x], no " | ", and the viscosity line is clean. B1 from build 5 is fixed on these 4 pages.
- Tire card page lists are sorted ranges: Corolla `pp. 513–514, 519–520, 558–560`, Camry `pp. 550–551, 584–588`. They wrap cleanly at 390 (37px, 2 lines). Minor: the mono `.pref` makes "pp.  551–552" look loosely spaced, non-blocking.
- Widths at 1280: Tacoma fuel table 810 (was 830), Civic tire table 810, CR-V tire table 810. The Civic and CR-V source column reads "Specifications" on every row.
- "Can I keep driving?" answer on P0301/P0442: 17px / 400. Passes.
- Full checklist: sidebar is only the sticky 13px TOC (hidden at 390). Camry overview is single column (718px). Mobile hero sits below the quick card, at 8:3 (2.67), with the credit. .pref letter-spacing is 0. No ads. Page overflow is 0 on all 10 pages at both widths.

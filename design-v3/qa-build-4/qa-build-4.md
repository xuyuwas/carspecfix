# Design QA: build 4 (site 02d9887, incl. 557053b)

Setup: `PREVIEW=1 RELEASE_DAY=1 astro build --outDir /tmp/qa4` (images.mjs not run), served on :8744, headless Chrome at 1280/390, full page + `-top`. Pages: RAV4 overview, /codes/, /symptoms/, 2020 RAV4, P0420, plus Civic 2022 and CR-V 2024 for the source checks. Source/dist untouched. Measurements: `qa.json`.
/symptoms/ is not in the day-one release order (no symptom pages are on day 1). It was shot from the preview to check the layout only.

## Checks
- **Overview pages, /codes/, /symptoms/:** ✓ `container--narrow` holds a 720px list at 1280 (left 280, centered), and the list fills the row (718px). Full width at 390 (358px), no empty column. (rav4-hub-1280.png, codes-1280.png, symptoms-1280.png)
- **Page numbers:** ✓ "p.671" and "p.1", letter-spacing normal, 39px wide. (rav4-2020-390-top.png, p0420-1280-top.png)
- **Oil card:** ✓ the big "4.8 qt with filter" is followed only by "4.4 qt without". Civic and CR-V use "incl. filter" (accepted).
- **"Seen on:":** ✓ sentence case (P0420).
- **Civic/CR-V Sources:** ✓ "Honda owner's manual AT202222IOM (2022 Civic)" and "A3A02424IOM (2024 CR-V)".
- **Regression checks:** no horizontal overflow, 0 ads, Print visible at both widths, hero 8:3, footer gutter 16px at 390. The preview has no canonical because the page is noindex; that comes from 02d9887 and applies to preview only.

## Remaining issue (minor, not blocking)
- **Civic 2022 / CR-V 2024 tire table, 1280+390:** the "Page" column (`.pref`) now shows the whole manual name, "Honda owner's manual AT202222IOM (2022 Civic)". The cell is about 350px wide and pushes the table to 857px; it scrolls sideways and does not overflow. This is a side effect of the source-name change. Expected: a page number, or "[3]" / "—" when there is no page number. (civic-2022-1280.png, crv-2024-390.png)

## Verdict
Day one passes design. The Honda page column can be fixed with the next batch.

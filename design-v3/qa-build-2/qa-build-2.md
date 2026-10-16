# Design QA: build 2 (site e1f8028; spec pages also checked on 28a37aa) vs design-v3

**Setup:** `PREVIEW=1 RELEASE_DAY=1 astro build --outDir /tmp/qa2` (images.mjs not run), served locally, headless Chrome at 1280×800 and 390×844, full page plus `-top` first-screen shots. Source/dist untouched. Raw measurements: `qa.json`. Note that the preview builds every page, so /codes/ also lists P0301/P0442 and the page JS liveCodes includes them. Production day-1 content is not visible in this preview.
Files: `{rav4-2020,civic-2022,crv-2024,rav4-2024,rav4-hub,p0420,p0171,p0300,p0456,p0455,codes}-{1280,390}[-top].png`, `p0455-390-keepdriving.png`, `p0456-390-h1-meaning.png`, `p0301-390-h1-meaning.png`.

## Blocking
B1. **4 spec pages, 1280+390: quick-answer numbers are not 34–40px.** Tire is the 20px text "Depends on your wheels" and oil is the 20px text "4.8 qt with filter". Only the Recalls count is 40/34px. Expected: big figures, e.g. **33–36** psi and **4.8** qt (unit at 16px). (rav4-2020-390-top.png)
B2. **4 spec pages, 390: quick card shows 4 tire rows.** RAV4 2020/2024 show 4 rows plus See all, and Civic shows 4 rows with no See all. Expected: 3 rows plus "See all N →". (rav4-2020-390-top.png, civic-2022-390-top.png)
B3. **Spec pages, 1280: there is an ad in the sidebar (`.ad--side`).** Expected: sidebar ads only on code pages. (rav4-2020-1280.png)
B4. **Civic, CR-V 2024, RAV4 2020/2024: recall text is still ALL CAPS.** Examples: "AIR BAGS:SENSOR:OCCUPANT CLASSIFICATION", "HYDRAULIC:FOUNDATION COMPONENTS:DISC:CALIPER". Expected: sentence case with ": " separators. (civic-2022-1280.png)
B5. **Code pages, both widths: the brand-specific lines in "Can I keep driving?" are 15px but black (rgb 15,20,25), not gray.** The inline style uses `var(--text-muted)`, which is not defined in the tokens. Expected: `--text-3` #5B6570. (p0455-390-keepdriving.png)
B6. **All pages, 390: footer has 0 horizontal padding.** The logo and text sit flush against the screen edge (`.ftr__in` padding-left 0). Expected: same 16px gutter as `.container`. (codes-390.png, rav4-hub-390.png)
B7. **All pages, 390: still no Print button** (0 visible, `.tools .btn-print{display:none}` under 1023px). Expected: Print stays in the quick answer.

## Minor
M1. **Page numbers:** they are correct in tables (`.pref` JetBrains Mono 500 13px #5B6570). In `.qa__src`, `.kv__src` and "Source wording" they are inside Source Sans 12px 400 text ("Manual p.671…", "…01-013/18, p.1"), so the mono style isn't applied. Expected: the p.xx part uses `.pref`.
M2. **"Source wording" line (P0456, P0301):** 12px #5B6570, but agreed is 13px. It shares a line with "· Wording from … p.1", which reads as two source lines stuck together. Expected: 13px, with the page number in `.pref`. (p0456-390-h1-meaning.png)
M3. **"Keep driving":** the EPA source comes first, but it is a 20px Archivo bold full paragraph, 8 lines per paragraph at 390, and the section is about 900px tall. Suggest 17–18px regular weight. P0420/P0456/P0455 also show the EPA "flashing = severe misfire" line; confirm with 小搜/小数 that it should stay.
M4. **Hero is not 8:3.** The photo is 1200×573 (2.09:1). At 390 the whole `.vart` (photo + credit) is `display:none`, so the photo and credit are invisible on mobile. Need to decide whether mobile shows the hero.
M5. **Sources:** one line per entry with a link and no icons ✓. Civic/CR-V show "2022 Honda Civic owner information" with no document number.
M6. **RAV4 overview, 390:** no spacing between the list and the "What changed between years" heading, and the tire size column is clipped (it does scroll sideways).
M7. **/codes/:** list items show only "P0171 code" with no name. Suggest adding display_name.

## Checks that passed
No horizontal overflow on any page. No cost/RepairPal. Photo credit is Source Sans 3 13px #5B6570 "Photo: author / CC BY-SA 4.0 / Source". Different model year shows "Shown: 2023 Honda CR-V EX-L (same generation)". Tire first, oil second, and every row names the wheel/tire. Oil visible on the first screen at 390 (heading at y≈500–640). P0456 long H1 wraps cleanly at 390 (5 lines, 32px, 358px wide, no overflow). The code page side ad is present.

## qa-build-1 items
1 Civic tire rows ambiguous: **fixed** (with tire size). 2 Mobile Print: **not fixed** (B7). 3 Cause format: **partly fixed** (source line + "Seen on:" present, but source is not the bold first line; P0420 shows "Seen on: Subaru models listed"). 4 Keep-driving scope: **fixed** (EPA first + "Toyota only" tag; color see B5). 5 Big figures: **not fixed** (B1). 6 RAV4 tall card: **partly fixed** (4 rows + See all, about 300px, still not 3 rows). 7 Ad under Recalls: not added (`.ad--below` under tires only); acceptable. 8 ALL CAPS: **not fixed** (B4). 9 Credit component: **fixed**. 10 Art box height: **changed to a photo**, 360×177, aligned. 11 Nav "Data sources": unchanged, acceptable. 12 Oil labels: **fixed** (Civic qa shows "1.5L turbo:" / "2.0L:").

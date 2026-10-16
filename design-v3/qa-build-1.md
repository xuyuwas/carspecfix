# Design QA: build 1 (site commit 2a30b90) vs design-v3

**Setup:** `PREVIEW=1 astro build --outDir /tmp/qa-prev`, served locally and checked in headless Chrome at 1280 and 390. The site source and dist were not touched, and nothing was pushed or deployed. Production `dist/` contains no symptom pages (publish gate), so the symptom page comes from the preview build.
**Screenshots:** `design-v3/qa-build-1/{rav4,civic,crv,symptom}-{1280,390}[-top].png`. Raw measurements: `/tmp/qashots/qa.json`.

**Passes:**
- **Tokens and type:** CSS variables match exactly (`--primary #0B2545`, `--accent-btn #C2410C`, `--text-3 #5B6570`, `--r-md 6px`). Archivo 800 headlines (56/36px), Source Sans 3 16px body.
- **Page and header:** `lang=en-US`, sticky header, no horizontal overflow at either width.
- **Tables:** scroll sideways on mobile (640/760px inside 356px).
- **Copy, feedback, cost:** Copy shows "Copied". Feedback widget and "Report a data error" are present on every page. No cost/RepairPal content.
- **Tab bar:** has the right-edge fade on mobile.

## High
1. **Civic 2022, 1280 + 390: Quick answer tire pressure lines are ambiguous.** "1.5L: 33/33 psi" and "1.5L: 33/32 psi" (same for 2.0L) don't say which wheel/tire each belongs to. **Expected:** each line keyed by wheel size or tire size, as in the tire table, e.g. "17-in (215/50R17): 33/33 psi" and "18-in (235/40R18): 33/32 psi".
2. **All pages, 390: no Print button anywhere on mobile.** The Quick answer shows only Copy, and every section Print is hidden. **Expected:** per design-v3, the Quick answer Print stays visible on mobile; only section-level Print buttons are hidden. Copy and print are a core requirement (PRD S7).
3. **Symptom (brakes-squeaking), 1280 + 390: the cause format doesn't match the spec.** Items render as a cause title plus a source sentence ("Toyota's owner's manual (2022 Toyota Camry Owner's Manual OM06244U …) found this"). **Expected:** `Source bulletin (manufacturer, bulletin no.) — Seen on: model list`. The source is the first line in bold, with manufacturer and document number; "Seen on:" lists the models.
4. **Symptom, 1280 + 390: the Quick answer "Can I keep driving?" is backed only by a Camry-specific manual** ("applies to: Toyota Camry") on a generic, all-vehicles page. **Expected:** the answer is either generic with a generic source, or carries a visible scope label ("For 2022 Toyota Camry") styled as a qualifier, not the headline. Otherwise show "Not yet verified". (A data/content issue, flagged so the design doesn't present a model-specific answer as universal.)

## Medium
5. **RAV4 / Civic / CR-V, 1280 + 390: Quick answer figures aren't in the big-figure style.** Oil and tire answers use 20px headings ("4.8 qt with filter", "Depends on your wheels"). **Expected:** `.qa__a` figure style, 40px desktop / 34px mobile Archivo 800 with tabular numbers, the unit 16px in secondary color (e.g. **4.8** qt with filter). Multi-config tire pressure can lead with the most common value or a range, e.g. **33–36** psi, with the config list below.
6. **RAV4 2020, 390: the Quick answer is about 900px tall** (an 8-line tire list), pushing Recalls and the year chips well below the first screen. **Expected:** show at most 3–4 tire lines, plus "See all 8 configurations →" linking to `#tires`.
7. **RAV4 / Civic / CR-V, all widths: there's no ad under the Recalls table.** The only main-column ad is under Tires. **Expected (design-v3):** an ad slot directly under the Recalls table and under the Tires table. Optional; fewer ads is acceptable. Confirm it was intentional.
8. **Civic / CR-V, 1280 + 390: recall component text is raw NHTSA ALL-CAPS with no spaces** ("AIR BAGS:SENSOR:OCCUPANT CLASSIFICATION:FRONT PASSENGER"). **Expected:** sentence case with ": " separators, as in design-v3 ("Air bags: sensor: occupant classification: front passenger"), keeping the campaign ID in mono.

## Low
9. **Spec pages, all widths: the silhouette placeholder has no caption or credit line.** No figcaption/credit element was found. **Expected:** placeholders get no credit but an `alt=""` plus aria-hidden. When a real photo is imported, a credit line goes under the image (12px, `--text-3`): "Photo: {author}, {license}". Please confirm the credit component exists for photos; it couldn't be verified because no page uses a photo yet.
10. **RAV4 2020, 1280: the SUV silhouette art box (light gray panel) is taller than the title block,** leaving uneven space above the Quick answer. **Expected:** art aligned to the title baseline, max height about 110px, matching design-v3.
11. **All pages: the header nav shows "Data sources" where design-v3 has "Maintenance".** Acceptable, since Maintenance pages don't exist yet; note it for the design file.
12. **Spec pages, 1280: the Engine oil list repeats "Oil capacity" as the label for both engines.** **Expected:** labels "Oil capacity, 1.5L turbo" and "Oil capacity, 2.0L" with the value as the big figure.

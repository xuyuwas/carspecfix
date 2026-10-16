# QA build 7 — commit 5988c05 (visual)
Build: PREVIEW=1 RELEASE_DAY=1 and 3 into /tmp/qa7-day1 and /tmp/qa7-day3. 0 errors; images.mjs not run. Screenshots: qa-build-7/.

## Result: PASS (0 blocking)

Camry and RAV4 overview pages, at 1280 and 390:
- Header reads "Oil capacity (without filter)" and stays on one line (39px row).
- Cells are clean. Camry: `2.5L 4.4 qt · V6 5.6 qt · Hybrid 4.4 qt` (2022) and `… 4.2 …` (2024). RAV4: `4.2 qt` / `4.4 qt`. No SAE, no GF-, no brackets, no '|'.
- Table at 1280 is 718px in the 720 narrow column, no scroll. At 390 it scrolls inside its own box (356/640). Page overflow is 0.
- Single centered column, no sidebar, no ads.

Day-1 spot check (RAV4 2020, Civic 2022, P0420) against 02d9887, nothing regressed:
- Sidebar is only the 13px sticky TOC, hidden at 390.
- .pref letter-spacing is 0.
- No ads, and page overflow is 0 at both widths.

## Non-blocking
- N1: on the Camry overview at 1280, the oil cell wraps and leaves the unit alone on the second line ("Hybrid 4.2 / qt"). Wrap each "engine amount qt" chunk in a nowrap span so the line breaks only at the " · " separators.

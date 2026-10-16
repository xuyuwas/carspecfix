# Design QA: build 3 (site 4b5e22f) vs design-v3 + new decisions

Setup: `PREVIEW=1 RELEASE_DAY=1 astro build --outDir /tmp/qa3` (images.mjs not run), served on :8743, headless Chrome at 1280 and 390, full page + `-top`. Source/dist untouched. Measurements: `qa.json`. The preview shows every page, so /codes/ also lists P0301/P0442 (preview effect).

## Still blocking (new regressions)
N1. **RAV4 overview + /codes/, 1280: not single column.** The container is 1200px wide (left 40), and the list renders in a 2-column grid with an empty right half (rows end at about 510px inside a 920px box). Expected: max 720px, centered, list full width, no empty column. (rav4-hub-1280.png, codes-1280.png)
N2. **All pages with `.pref`, 1280+390: page numbers are letter-spaced as "p . 6 7 1", "p . 2".** The font, size, color and weight are correct (JetBrains Mono 13px 500 #5B6570), but there is extra tracking or a mono fallback in the spacing. Expected: "p.671" set tight (letter-spacing 0). (rav4-2020-390-top.png, p0420-1280-top.png)

## qa-build-2 blocking
B1 big figures: **fixed** (40/34px: 33–36 psi, 4.8 qt). B2 3 rows + See all: **fixed** (RAV4 3 + "See all 8 →"; Civic 3 + "See all 4 →"; CR-V has only 2). B3 spec sidebar ad: **fixed** (no ads anywhere). B4 ALL-CAPS recalls: **fixed**. B5 brand lines color: **fixed** (15px #5B6570). B6 mobile footer gutter: **fixed** (16px). B7 mobile Print: **fixed**.

## qa-build-2 minor
M1 `.pref` page numbers: applied, but see N2. M2 Source wording: **fixed** (`.qa__src--wording` 13px, own line). M3 keep driving: **fixed** (17px regular). M4 hero: **fixed** (8:3, 358×134 at 390, below the quick card at y≈1005 after the card bottom at 989, credit shown; desktop 360×135 2.67). M5 Civic/CR-V Sources without doc number: unchanged. M6 hub spacing: gap fixed, but see N1. M7 /codes/ names: **fixed** (display_name).

## New decisions
- No ads: ✓ (0 `.ad` on all 22 shots).
- Sidebar = sticky "On this page" 13px TOC only: ✓ (`.toc` sticky top 88px while scrolling, links 13px). Single-column pages: ✗ (N1).
- Mobile hero 8:3 below quick card with credit: ✓.
- P0171 H1 "P0171: System Too Lean, causes & can you keep driving?": ✓ (no Bank 1).

## New minor
m1. **Spec pages: the oil quick card repeats itself.** The big "4.8 qt with filter" is followed by "4.8 qt with filter / 4.4 qt without". Suggest showing only "4.4 qt without" under it.
m2. **P0171 Source wording "System too Lean":** this is the source original, so it is correct as is (no change).
m3. **P0171 cause "SEEN ON:"** is shown in caps (label styling). OK if intended; the other pages use "Seen on:".
Pass: no horizontal overflow; no cost/RepairPal; credits 13px #5B6570; no ALL-CAPS recalls.

## Verdict
**Day one does not pass design yet.** Only N1 (hubs: 720px single column) and N2 (`.pref` letter-spacing) remain. Both are CSS-only; after they are fixed, a re-shot of the hubs and one spec/code page is enough.

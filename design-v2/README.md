# CarSpecFix design v2 (spec-sheet style): handoff for 小码 (Astro)

v1 (`../design/`) is kept for reference only. **v2 is the current design.** Open the .html files directly.

## Files
- `tokens.css`: colors, spacing (2–24px scale), 2px radius, fonts, type sizes, layout
- `components.css`: all styles, mobile-first, desktop at `min-width:1024px`, plus print styles
- `components.html`: component reference
- `index.html`, `spec-2020-rav4.html`, `symptom-brakes-squeaking.html`, `code-p0455.html`
- `assets/logo.svg`, `assets/icon-*.svg` (stroke `currentColor`; inlined in the HTML)
- `screenshots/*-1280.png`, `*-390.png`
- `build.py`: generator for the HTML (reference only)

## Tokens
- Navy `#0B2545` (top bar, section rules), navy-2 `#1D3A5F`; accent `#E07B00` (top-bar rule, main button), accent ink `#A34E00` (unverified text), accent tint `#FFF4E0`
- Ink `#16191D` / `#4A5059` / `#7A818B`; rules `#C9CED6` (strong) and `#E3E6EA` (hairline); table head `#EDF0F3`; zebra rows `#F6F7F9`; links `#0B4A8F`
- Severity tags (square, mono caps): low `#2E7D32` on `#E6F2E6`, medium `#8A6200` on `#FFF3C4`, high `#B3261E` on `#FBE4E2`, not rated = dashed gray
- Fonts (Google Fonts): IBM Plex Sans (UI), IBM Plex Sans Condensed (titles, labels, buttons), IBM Plex Mono with tabular-nums (all figures, codes, dates)
- Spacing `--s1..--s7` = 2, 4, 6, 8, 12, 16, 24. Radius 2px everywhere. Figures 24px (mobile) / 28px (desktop) bold mono

## Component → Astro
| Class | Astro component | Notes |
|---|---|---|
| `.topbar` | `Header.astro` | Brand, nav, quick search (code or vehicle). Nav becomes a menu button below 1024px |
| `.foot` | `Footer.astro` | |
| `.crumbs` | `Breadcrumbs.astro` | Always shown; last item has `aria-current` |
| `.toolbar` | `PageToolbar.astro` | Updated date, verified count, Print page |
| `.sec` + `.label` | `Section.astro` (`label`, `tools`) | 2px navy rule with a small-caps label; optional Copy/Print. Print is hidden in sections on mobile |
| `.kv` | `SpecSheet.astro` (`rows: {label, value, unit, source, ref}`) | Big mono figure, footnote `[n]`, source line under every figure; no value → "Not yet verified — check owner's manual". Rows stack below 600px |
| `.dt` in `.scroll` | `DataTable.astro` (`columns, rows, note`) | Hairline grid, zebra rows, right-aligned numbers; min-width 620px and horizontal scroll below 1024px, with scroll hint |
| `.refs` + `sup.ref` | `Sources.astro` | Numbered sources list (`#ref-n`) at the bottom of every page |
| `.sev--low/med/high/na` | `SeverityTag.astro` | |
| `.notice` | `Notice.astro` | e.g. manual model year unconfirmed |
| `.box` | `InfoBox.astro` | Sidebar infobox (key figures, contents, common problems) |
| `.ad--below`, `.ad--side` | `AdSlot.astro` | Only directly below a data table or in the sidebar |
| `.lookup`, `.makes`, `.list` | home: lookup form, browse-by-make index, simple lists | |
| `.grid > .main + .side`, `.m-only` | `PageLayout.astro` | Sidebar hidden below 1024px; its content repeats in `.m-only` |

## Data rules
ISO dates (recalls converted). Metric values marked "metric converted". TODO fields: "Not yet verified — check owner's manual" (symptom/code pages: "source pending"). Never estimate. Every figure has a footnote pointing to the Sources list.

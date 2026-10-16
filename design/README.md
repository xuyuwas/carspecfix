# CarSpecFix — visual design handoff for 小码 (Astro)

This is the final static design. Open any .html file directly. These are design references, not production templates. Content comes from `../prototype/`.

## Files
| Path | What |
|---|---|
| `tokens.css` | CSS variables: colors (primitive + semantic), spacing, radius, type, layout |
| `components.css` | All component and layout styles (mobile-first, desktop at `min-width:1024px`, print styles) |
| `components.html` | Component gallery |
| `index.html`, `spec-2020-rav4.html`, `symptom-brakes-squeaking.html`, `code-p0455.html` | The 4 pages |
| `assets/logo.svg`, `assets/icon-{copy,print,menu,chevron,warning,arrow,swipe}.svg` | Logo + icons (stroke = `currentColor`) |
| `screenshots/*-1280.png`, `*-390.png` | Headless Chrome checks (390 = mobile, DPR 2) |
| `build.py` | Generator used for these HTML files (reference only) |

## Tokens (tokens.css)
- Brand: primary `#0B2545` (navy-900), primary tint `#EEF3FA`, accent `#F97316`, accent text `#C2410C`, accent tint `#FFF7ED`
- Text: `#111827` / secondary `#4B5563` / muted `#9CA3AF`; border `#E5E7EB`; subtle bg `#F9FAFB`; ad bg `#F3F4F6`; page bg `#FFFFFF`
- Severity: low `#DCFCE7`/`#166534`, medium `#FEF3C7`/`#854D0E`, high `#FEE2E2`/`#991B1B`, unrated = subtle bg + secondary text
- Spacing: 4, 8, 12, 16, 24, 32, 48 (`--space-N`)
- Radius: sm 4, md 8, lg 12, full 999
- Type: Inter/system; numbers 32px (mobile) / 36px (desktop) bold; H1 26/34 extrabold; H2 18/22 bold; body 14; small 12
- Layout: container 1280, sidebar 300, breakpoint 1024

## Component → Astro template
| Component (class) | Suggested Astro component | Notes |
|---|---|---|
| `.site-header` | `Header.astro` | Nav collapses to menu button < 1024px |
| `.site-footer` | `Footer.astro` | Sources line + links |
| `.btn--primary/secondary/accent`, `[data-copy]`, `[data-print]` | `Button.astro` | Copy and Print use a small inline script (bottom of each page) |
| `.sev--low/medium/high/unrated` | `SeverityTag.astro` (`level` prop) | "Not yet rated" until a source exists |
| `.num` | `SpecNumber.astro` (`label, value, sub, source, href`) | No value → renders "Not yet verified — check owner's manual"; source always shown |
| `.spec-table` | `SpecTable.astro` (`title, columns, rows, source`) | `.spec-table__scroll` has `overflow-x:auto` and the table has min-width 640px < 1024px; swipe hint shown on mobile; Print hidden in table head on mobile (page-level Print stays) |
| `.ad--below`, `.ad--sidebar` | `AdSlot.astro` (`placement`) | Only directly below a table or in the sidebar. Never between numbers |
| `.alert` | `Alert.astro` | e.g. manual model year unconfirmed |
| `.hero/.lookup`, `.chips`, `.vehicles` | home sections | |
| `.layout > .main + .sidebar`, `.mobile-only` | `PageLayout.astro` | Sidebar hidden < 1024px; its blocks (common problems, TPMS, affected vehicles) repeat in `.mobile-only` |

## Data rules reflected in the design
- Dates in ISO (recall dates converted from DD/MM/YYYY).
- Metric values marked "metric converted".
- TODO fields show "Not yet verified — check owner's manual"; symptom and code fields show "source pending". Never estimate.
- Icons are inlined as SVG in the HTML (CSS `mask` doesn't load over `file://`). In Astro, import the SVGs from `assets/` or inline them.

# CarSpecFix design v3: handoff for 小码 (Astro)

**v3 is the current design.** v1 (`../design/`) and v2 (`../design-v2/`) are kept for reference only. Open the .html files directly.

## Research: 5 takeaways (Edmunds, Car and Driver, CarGurus/KBB design systems; checked 2026-10-15)
1. **The vehicle page leads with the model name.** Car and Driver's "2020 Toyota RAV4" page puts the name first, then a compact spec summary (EPA mpg, seating, powertrain, drivetrain, warranty) before any prose. → We use a big model-name header with year/config chips and a 4-figure key-specs strip.
2. **Specs are scannable label/value pairs and grouped tables** (C/D's spec block: VEHICLE TYPE, ENGINE, DIMENSIONS…; Edmunds' listing rows: "25 City / 33 Hwy MPG"). Numbers are bold, units smaller, labels muted. → Our key-spec figures and spec rows use the same hierarchy.
3. **Lookup is the product.** Edmunds and KBB put a search / year-make-model finder at the top and keep the header sticky with search. → The home page is a finder (By vehicle / By trouble code tabs) on a solid navy band. No marketing hero.
4. **Token-based, restrained color.** CarGurus' Chassis and Cox's Iris (KBB, Autotrader) use semantic tokens. Brand color frames the page, and one accent goes on the calls to action (KBB: blues plus a gold CTA). → Navy frames the page (finder band, footer, primary buttons). Orange is used only for the main CTA, the active-nav underline, eyebrows and "Not yet verified".
5. **Strong display type over a neutral body, flat surfaces.** These sites pair a heavy display face (CarGurus: Rund Display + Graphik) with a clean body sans, on white with light dividers rather than heavy card shadows. → Archivo 800 for headlines and figures, Source Sans 3 for body, 1px borders and a 6px radius, no shadows or gradients.

## Files
- `tokens.css`: primitives plus semantic colors, 4px spacing grid, radius (4/6), font families and type scale (12–72px)
- `components.css`: all styles, mobile-first, desktop at `min-width:1024px`, plus print styles
- `components.html`: component gallery
- `index.html`, `spec-2020-rav4.html`, `symptom-brakes-squeaking.html`, `code-p0455.html`
- `assets/`: `logo.svg`, `car-suv.svg`, `car-sedan.svg`, `car-truck.svg` (silhouette placeholders, `currentColor`), `icon-*.svg` (inlined in the HTML)
- `screenshots/*-1280.png`, `*-390.png`
- `build.py`: generator for the HTML (reference only)

## Tokens
- Navy `#0B2545` (primary), `#1E3D66` (hover/art), `#071A33` (footer), `#F2F5F9` (row hover)
- Orange `#F26B1D` (CTA, accents), `#D9560B` (accent text / Not yet verified), `#FFF2EA` (tint)
- Gray text `#0F1419` / `#3D4752` / `#68737F`; borders `#DDE2E8` / `#C5CCD4`; alt surface `#F7F8FA`; links `#1A56A8`
- Severity: low `#1F7A3D`/`#E8F5EC`, medium `#8A5A00`/`#FFF6D6`, high `#B42318`/`#FDECEA`, not rated = gray; Example tag = orange tint
- Spacing `--sp-1..12` = 4, 8, 12, 16, 20, 24, 32, 40, 48. Radius 4 (tags, ads) and 6 (buttons, tables, cards)
- Type: Archivo 600–800 (display, figures, tabular-nums), Source Sans 3 400–700 (body/UI), JetBrains Mono (codes, campaign IDs, footnote markers). Model name 44 → 72px, key figures 34 → 44px, section titles 20 → 24px

## Component → Astro
| Class | Astro component | Notes |
|---|---|---|
| `.hdr` | `Header.astro` | Sticky, with search; nav and search collapse to icon buttons below 1024px |
| `.ftr` | `Footer.astro` | |
| `.crumbs` | `Breadcrumbs.astro` | |
| `.vhead` (+ `.vtitle`, `.chip`, `.vart`) | `VehicleHeader.astro` (`year, make, model, segment, years[], configs[]`) | Silhouette art on desktop only |
| `.keyspecs > .ks` | `KeySpecs.astro` (4 × `{label, value, unit, source, ref}`) | 2×2 on mobile, 4-up on desktop |
| `.subnav` | `PageTabs.astro` | Sticky under the header, scrolls sideways on mobile |
| `section > .section__head` | `Section.astro` (`title, kicker, tools`) | Copy/Print tools. Print is hidden in sections on mobile; the page-level Print stays |
| `.tbl-wrap .tbl` | `SpecTable.astro` (`columns, rows, foot`) | Right-aligned tabular numbers, row hover, footer note; min-width 640/760px and sideways scroll below 1024px |
| Tire table (`#tires`) | `TireTable.astro` (rows: `wheel, config, tireSize, frontPsi, rearPsi, page, ref, example`) | One row per wheel/config. `example:true` shows the Example tag and "Example" in the source column |
| `.kv` | `SpecList.astro` | Figure + unit + `[n]` + source line; missing → "Not yet verified — check owner's manual" |
| `.facts` | `FactGrid.astro` | Issue pages: when to stop driving / get it checked |
| `.causes` | `CauseList.astro` (`source, manufacturer, bulletinNo, seenOn[]`) | Numbered; bulletin source + seen-on models |
| `.tag--low/med/high/na/example` | `Tag.astro` | |
| `.notice` | `Notice.astro` | |
| `.ad--below`, `.ad--side` | `AdSlot.astro` | Only directly below a table or in the sidebar |
| `.panel` | `SidePanel.astro` | |
| `.refs`, `sup.ref` | `Sources.astro` | Numbered `#ref-n` list at the end of each page |
| `.finder`, `.vgrid/.vcard`, `.makes`, `.links` | home sections | |

## Revision 2026-10-15 (PRD user-needs.md)
- **First screen answers the owner's question.** The spec page leads with a Quick answer card (oil amount, type and pages; cold tire pressure, tire size and page; recall count with the VIN link). Symptom and code pages lead with Can I keep driving? / How urgent? / Shop visit or check it yourself first? (see Revision 2); the code page shows the meaning first. Unsourced values show "Not yet verified". → `QuickAnswer.astro`
- **Spec page order:** quick answer → recalls → tires by config → wipers/battery/fuses/towing → fuel economy → common problems → feedback → sources.
- **Feedback widget** (Yes/No; No opens an optional "what was missing" box with no personal info) and a **Report a data error** link (`#report`) on every page → `Feedback.astro`.
- **Tire table** supports up to 10 rows; repeated tire sizes with different psi per config are expected. The RAV4 page shows 9 rows, **all EXAMPLE data**.
- **Contrast (WCAG AA):** muted text `#5B6570` (≥5.5:1 on white/alt). Accent text `#B8460A` (5.4:1). Orange buttons use `--accent-btn #C2410C` with white text (5.2:1).
- **Script:** Copy uses the Clipboard API with an execCommand fallback and shows "Copied" / "Copy failed" (plus an aria-live message). Print calls `window.print()`. Tested in headless Chrome.
- **Mobile tab bar:** right-edge fade hint plus end padding, so the last tab is reachable and visibly scrollable.

## Revision 2 (2026-10-15): no repair cost
- **All repair cost / price content is removed:** no cost module, no "Rough cost", no RepairPal source or footer mention, no cost wording in titles.
- **Symptom and code first screen** (`QuickAnswer.astro`, issue variant): **Can I keep driving? / How urgent? / Shop visit or check it yourself first?** Unsourced answers show "Not yet verified — source pending". The code page shows "What it means" (SAE J2012) above them.
- **Causes** (`CauseList.astro`, `.causes`): each item is `Source bulletin (manufacturer, bulletin no.) — Seen on: model list`. Only sourced bulletins are published; the Example row shows the format only.
- New titles: "Brakes Squeaking: Causes, Is It Safe to Drive?" and "P0455 Code: Meaning, Causes & Can You Keep Driving?".

## Data rules
ISO dates. Metric values marked "metric converted". TODO fields show "Not yet verified — check owner's manual" (symptom/code pages: "source pending"). Never estimate. Every figure has a `[n]` footnote pointing to Sources. **All 9 tire-table rows are example data for layout only.** The verified tire figure (35 psi, 225/65R17, p.671) is in the Quick answer card.

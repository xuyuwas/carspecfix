# Symptom / code sources (fetched 2026-10-15)
Full detail in `symptom_code_sources.json`.

## RepairPal ToS (https://repairpal.com/terms_of_service)
Verdict: **not allowed.** There's no exception for citing with attribution, and the terms bar anyone from publishing or reproducing "any materials or content accessible on the Service". Whether a bare price range counts as fair use is a legal question we can't settle here. Recommendation: don't use RepairPal prices.

## A-grade causes per page
| Page | A causes | Notes |
|---|---|---|
| p0455 | 6 | GM 21-NA-124, Acura flap-unit TSB |
| p0442 | 3 | GM 21-NA-124 |
| p0456 | 3 | Mazda 01-013/18 (fuel cap), Nissan O-ring, Stellantis software |
| p0171 | 4 (+1 B) | GM PI1307, Ford PIP5549, Mazda M-Tip, VW tech tip; Mitsubishi list = B until fetched directly |
| p0420 | 4 | Subaru SIB, Honda 22-040, Ford 22-2260, 25-2119 |
| p0300 | 2 (+1 guidance) | VW 01-16-13, GM 15-06-01-002M |
| p0301 | 2 | VW 01-16-13 |
| brakes-squeaking | 2 + urgency | 2022 Camry OM p.199, Chevrolet support page |
| grinding-noise-when-braking | 2 + urgency | same |
| car-shakes-when-braking | 2, urgency not verified | Chevrolet sign; Camry p.326 (ABS normal vibration) |
| abs-light-on | 1 + 2 urgency | Camry p.528, p.535 |
| car-cranks-but-wont-start | 3 | Camry p.557 |
| car-wont-start-clicking | 2 (manual doesn't say "clicking") | Camry p.557-558 |
| car-jerks-when-accelerating | 0 | not verified |
| car-shaking-when-accelerating | 0 | not verified |

## Caveats
- Each TSB applies only to the vehicles it lists. On the site, phrase these as "OEM bulletins have identified X on [vehicles]", not as general causes for every car.
- The SAE J2012 text and EPA/CARB documents weren't obtained. Code definitions use OEM wording instead.
- Symptom pages rely on a single Toyota manual plus a GM support page. Before publishing, add a second OEM source or a government page (NHTSA/FTC) for each.

## Driving guidance (Can I keep driving? / How urgent? / Shop or self-check?) — added 2026-10-15 batch 2
Sources (all A): EPA 420-F-97-003 (https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P1009Z15.TXT); 2022 Camry OM06244U pp.247, 528, 533, 557–558; Ford 2023 motorhome manual hosted by NHTSA (https://static.nhtsa.gov/odi/inv/2024/INRD-PE24023-27812.pdf, PDF p.33).
| Page | Keep driving? | Urgency | Self-check first? |
|---|---|---|---|
| p0455/p0442/p0456 | Steady light: yes (EPA p.2 "NOT of the need to stop") | ASAP (EPA p.2); Toyota p.528 says "immediately" | Yes: tighten gas cap (EPA p.3; Camry p.247, p.533) then shop |
| p0171 | Steady: yes (EPA p.2) | ASAP / Toyota "immediately" | Camry p.533 fuel/cap check; else qualified shop (EPA p.4) |
| p0420 | Steady: yes (EPA p.2) | ASAP / Toyota "immediately" | Shop (EPA p.4) |
| p0300/p0301 | If flashing: reduce speed (EPA p.2), drive moderately (Ford PDF p.33) | ASAP | Shop |
| car-cranks-but-wont-start | n/a (car does not run) | — | Yes: fuel, retry start (Camry p.557); dealer if unresolved (p.558) |
| car-wont-start-clicking | n/a | Not yet verified | Battery per Camry p.557 (manual doesn't say "clicking") |
| car-shakes-when-braking | Not yet verified | Not yet verified | Not yet verified (only shop blogs found) |
Caveats: EPA sheet is dated 1997 and mentions repair costs — don't quote that part. Toyota p.528 vs p.533 differ in urgency; show both, Toyota-scoped.

## Scope update (2026-10-15 batch 3)
Every driving_guidance entry now has `scope`: `universal` or `vehicle-specific: <make model year>`.
- Codes (7): primary = universal EPA 420-F-97-003 p.2. Toyota/Ford quotes = vehicle-specific extras.
- abs-light-on, brakes-squeaking, grinding-noise-when-braking, car-shakes-when-braking, car-wont-start-clicking, car-cranks-but-wont-start: **primary = Not yet verified** — no NHTSA/EPA/FTC/US-gov source found that says whether to keep driving. Searched nhtsa.gov, consumer.ftc.gov; eCFR (FMVSS 135) blocked by captcha. Only shop blogs, OEM marketing pages and vehicle-specific TSBs exist. Camry/Chevrolet quotes kept as vehicle-specific extras.

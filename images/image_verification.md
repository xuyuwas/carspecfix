# Image verification — pilot spec pages
Checked 2026-10-15 (UTC+8) by 小站. Method: Commons API (imageinfo extmetadata + categories) for every file page in image_sources.csv, plus visual check of each local image (thumbnails viewed). image_sources.csv NOT edited.

## Important side finding
- **image_sources.csv is malformed CSV**: a standard CSV parser (Python csv) reads only the first 4 rows; everything from the 2024 Camry row on is swallowed by a quoting error. 小码's loader must not trust it until the file's owner fixes quoting.
- **"(2024)" in Flickr-import titles by "Charles from Port Chester, New York" is the PHOTO year, not the model year** (proved by his "Toyota Camry Hybrid XLE (2024)" files, which are the XV80 / 2025 MY car at the 2024 NY Auto Show). That kills the year evidence for the 2024 CR-V primary row.

## Per photo
| # | page | file | verdict | evidence |
|---|---|---|---|---|
| 1 | 2020-toyota-rav4 | 2020 Toyota Rav4 XLE, Front Left, 09-30-2020 | **confirmed** | Desc "2020 Toyota Rav4 XLE"; cat Toyota RAV4 (XA50); shot 2020-09-30; visual XA50 gas XLE. Taken in Ontario, Canada (NA-spec trim). SsmIntrigue, CC BY-SA 4.0 |
| 2 | 2024-toyota-rav4 | 2024 Toyota RAV4 Hybrid Woodland Edition, front right | **confirmed (variant caveat)** | Desc + cat "2024 Toyota automobiles", RAV4 Hybrid (XA50); New Castle PA. It is the HYBRID Woodland (bronze wheels, roof rack); caption must say Hybrid if page is gas. MercurySable99, CC BY-SA 4.0 |
| 3 | 2022-toyota-camry | 2022 Camry SE Std Pkg, Celestial Silver, Front Left | **confirmed** | Desc + cat "2022 Toyota automobiles", Camry (XV70, North America, 2021); visual facelift SE. Ontario. Elise240SX, CC BY-SA 4.0 |
| 4 | 2022-toyota-camry (backup) | 2022 Camry Hybrid XLE, Midnight Black | **confirmed (hybrid)** | Desc incl. "Assembled in Georgetown, Kentucky"; cat 2022 Toyota automobiles. Note a dealer-style red Toyota plate frame on bumper. CC BY-SA 4.0 |
| 5 | 2024-toyota-camry | 2024 Toyota Camry Las Vegas Fall 2025 | **year unclear; not usable as-is** | Desc "A 2024 Toyota Camry at Las Vegas Motor Speedway in 2025" (uploader claim only, no trim/VIN); visual = XV70 facelift SE (correct generation, US). Large EchoPark Automotive / "Speedway Experience" branding and dealer plate in frame; on a display platform. TaurusEmerald, CC BY-SA 4.0 |
| 6 | 2024-toyota-camry (sub) | 2023 Toyota Camry XSE, front right, 08-30-2026 | **confirmed as 2023, same generation** | Desc "2023 Toyota Camry XSE ... New Castle, Pennsylvania"; cat 2023 Toyota automobiles, XV70 NA. Clean background. Caption must say "2023 model, same generation". MercurySable99, CC BY-SA 4.0 |
| 7 | 2022-toyota-corolla | 2021 Toyota Corolla LE, front right, 07-13-2024 | **confirmed as 2021, same generation** | Desc "2021 Toyota Corolla LE ... New Castle, Pennsylvania"; cats 2021 Toyota automobiles, Corolla (E210, North America) sedan. Visual: pre-2023-refresh LE front (2020–2022 US sedan look). NOT 2022 — caption "2021 model, same generation". CC BY-SA 4.0 |
| 8 | 2022-toyota-tacoma | 2023 Toyota Tacoma TRD Off-Road Double Cab in Black, front left | **confirmed as 2023, same generation** | Desc: 2023 Tacoma TRD Off-Road, built Guanajuato MX, completed 2023-10-02, "one of the last N300s"; cat 2023 Toyota trucks, Tacoma (N300). Visual: N300 facelift (2020–2023 body). NOT 2022 — caption "2023 model, same generation". Mr.choppers, CC BY-SA 3.0 (+GFDL) |
| 9 | 2022-toyota-tacoma (backup) | 2021 Toyota Tacoma V6 4x4 | **weak — do not use** | Title says 2021, description only "Toyota Tacoma"; image is a REAR 3/4 view, backlit, other cars/buildings; not a front 3/4. DestinationFearFan, CC BY-SA 4.0 |
| 10 | 2022-honda-cr-v | 2022 Honda CR-V EX-L (facelift), front 3.31.23 | **confirmed** | Desc "A 2022 Honda CR-V EX-L facelift ... Flushing, Queens"; cat CR-V (5th gen); visual 5th-gen facelift. Kevauto, CC BY-SA 4.0 |
| 11 | 2024-honda-cr-v | Honda CR-V EX-L AWD (2024) (53625033461) | **mismatch — do not use** | (a) It is an INTERIOR photo (dashboard/seats), not exterior; cat "Honda automobile interiors". (b) "(2024)" is the photo date (2024-03-29, NY Auto Show), not model year; desc only says 6th gen. CC BY 2.0 |
| 12 | 2024-honda-cr-v (backup) | 2023 Honda CR-V EX-L AWD, front right, 11-13-2022 | **confirmed as 2023, same generation** → should become primary | Desc "2023 Honda CR-V EX-L AWD ... New Castle PA"; cat 2023 Honda automobiles, CR-V (6th gen); gas EX-L. Caption "2023 model, same generation". MercurySable99, CC BY-SA 4.0 |
| 13 | 2022-honda-civic | 2022 Honda Civic LX Sedan, front right | **confirmed** | Desc + cat 2022 Honda automobiles, Civic (2021) sedan; New Castle PA. Background has parked cars only. CC BY-SA 4.0 |
| 14 | 2022-honda-accord | 2022 Honda Accord Sport, Sonic Grey Pearl, Front Left | **confirmed (minor)** | Desc + cat 2022 Honda automobiles, Accord (2017); visual 2021–22 facelift Sport. Ontario. Window stickers visible (dealer-lot look) — no logo signage. Elise240SX, CC BY-SA 4.0 |
| 15 | 2021-ford-f-150 | 2021 Ford F-150 SuperCrew, front 4.28.21 | **confirmed** | Desc "A 2021 Ford F-150 SuperCrew ... Queens"; cats 2021 Ford trucks, 14th gen, F-150 XL. Kevauto, CC BY-SA 4.0 |
| 16 | 2023-ford-f-150 | 2023 Ford F-150 SuperCrew Pick-Up (52810350195) | **mostly confirmed** | Title says 2023 (Flickr uploader); shot Apr 2023 Twin Cities Auto Show; 14th gen visual (gas, not Lightning). Show-floor background: Ford blue banner, window sticker, people. Greg Gjerdingen, CC BY 2.0 |
| 17 | 2022-chevrolet-silverado-1500 | 2022 Silverado 1500 LT, Summit White, Front Left | **confirmed: 2022 REFRESHED (new-body) version, not LTD** | Visual: slim split headlights, new 2022 refresh LT grille. Desc "2022 Chevrolet Silverado 1500 LT"; Ontario. Elise240SX, CC BY-SA 4.0 |
| 18 | 2022-chevrolet-silverado-1500 (backup) | 2022 Silverado K1500 LT-L, front 4.24.23 | **confirmed: 2022 REFRESHED version** | Zoomed: slim headlight with amber, refresh grille (not the 2019–21 / LTD front). Manorville NY. Kevauto, CC BY-SA 4.0 |
| 19 | 2022-chevrolet-equinox | 2022 Chevrolet Equinox LT (facelift), front 6.2.22 | **confirmed** | Desc says 2022 LT facelift, Queens; visual matches 2022 facelift. Kevauto, CC BY-SA 4.0 |
| 20 | 2023-tesla-model-y | 2023 Tesla Model Y, front 11.11.23 | **unclear (uploader claim only)** | Desc "A 2023 Tesla Model Y Long Range ... Queens"; Model Y has no visible MY cues 2020–2024, so year rests only on uploader. Category only "Tesla Model Y". Kevauto, CC BY-SA 4.0 |

### Silverado data flag for 小数
Photos are the refreshed 2022. spec_pages.csv lists the 3.0L Duramax as **LM2**; as far as I know the 2022 refresh got the LZ0 and LM2 stayed in the carryover "LTD" — 未核实, please check the GM manual which version our oil data covers, so photo and data describe the same truck.

## 2024 Camry — new candidate
- **File:24 Toyota Camry Hybrid XLE.jpg** — https://commons.wikimedia.org/wiki/File:24_Toyota_Camry_Hybrid_XLE.jpg
  - Original: https://upload.wikimedia.org/wikipedia/commons/8/85/24_Toyota_Camry_Hybrid_XLE.jpg (4128 px wide)
  - Author: HJUdall · License: CC0 (http://creativecommons.org/publicdomain/zero/1.0/deed.en)
  - Year evidence: title "24 Toyota Camry Hybrid XLE"; description "24 Toyota Camry Hybrid XLE - Shot at Earnhardt Chrysler Dodge Jeep Ram in Gilbert AZ"; cat Toyota Camry Hybrid (XV70, North America, 2021); DateTimeOriginal 2026-09-29. Visual: XV70 facelift XLE hybrid, blue, front-left 3/4, plain white studio + checker floor, **no dealer signage/logos/plates visible**.
  - Caveats: HYBRID XLE (not gas). Studio set at a dealership looks like a listing photo — provenance risk: confirm the uploader is the photographer (CC0 is only valid if they own it). Year is uploader-only.
- Rejected: "Toyota Camry Hybrid XLE (2024)" Flickr files (XV80 = 2025 MY; "(2024)" = photo year); "2024 Toyota Camry HEV Premium Luxury" (Thai-market XV80); AU police 2024 Camry (Australian XV70, non-US, livery); Las Vegas photo (branding).
- Recommendation: primary = row 6 (2023 XSE, clean, caption "2023 model, same generation"); or the CC0 2024 XLE Hybrid if 小数 accepts the provenance and the hybrid caption.

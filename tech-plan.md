# carspecfix.com 技术方案 v1（小码，2026-10-15）

> 依据：README.md、templates.md、keyword_map.xlsx、spec_pages.csv、spec_api_data.json、symptom_pages.json、fetch.py、prototype/（4 个原型、seo-plan.md、notes-for-xiaoma.md）。本文不含任何流量预估。

## 0. 结论一览
| 决策 | 选择 | 理由 |
|---|---|---|
| 生成器 | **Astro（纯静态输出）+ Tailwind 构建期编译** | 默认零 JS、组件化模板、Content Collections 自带 Zod 校验（可强制“无来源不渲染”）、官方 sitemap 插件 |
| 数据 | **Git 仓库内 JSON 文件**，一页一个文件 | 可审计（每次改数据有 commit）、lastmod 可取自数据字段 |
| 托管 | **Cloudflare Pages（免费档）** | 免费、全球 CDN、自动 HTTPS、域名 DNS 同在 Cloudflare 便于做 www→apex 301 和 GSC 域名验证 |
| 发布节奏 | 数据带 `publishDate`，**GitHub Actions 每日 cron 触发构建**，只渲染 publishDate ≤ 今天的页 | 不需要人工每天操作 |
| 统计 | **Cloudflare Web Analytics**（免费、无 cookie）+ GSC + Bing 站长工具 | 零成本，无需 cookie 弹窗 |

备选对比（简）：
- Eleventy：同样轻量，但缺少内建的数据 schema 校验，需自己写；团队规模小，Astro 的类型校验更能防“TODO 漏上线”。
- Next.js 静态导出：能力过剩，默认 JS 体积大，不划算。
- GitHub Pages：免费，但不支持自定义 301/header 规则文件、无边缘重定向；仓库需公开（免费档）。Cloudflare Pages 支持 `_redirects`/`_headers`，私有仓库也行。→ 选 Cloudflare Pages，GitHub Pages 作为降级方案。

## 1. 仓库结构
```
carspecfix-site/
├─ data/
│  ├─ vehicles/2020-toyota-rav4.json      # 规格页，一车一年一文件
│  ├─ symptoms/brakes-squeaking.json
│  ├─ codes/p0455.json
│  ├─ repair-costs/brake-pad-replacement.json   # 费用条目，症状/故障码引用
│  └─ sources.json                        # 来源登记表（id → 名称/URL/抓取日期）
├─ scripts/
│  ├─ fetch.py            # 沿用现有，改为输出到 data/vehicles/*（只更新 API 字段）
│  ├─ import_legacy.py    # 一次性：spec_pages.csv + symptom_pages.json → data/*
│  ├─ validate.ts         # CI：TODO/无来源值禁止进入已发布页
│  └─ indexnow.ts         # 部署后推送当日新/改 URL
├─ src/
│  ├─ content/config.ts   # Zod schema（见 §2）
│  ├─ layouts/Base.astro  # head、canonical、JSON-LD、面包屑
│  ├─ components/         # SpecTable, RecallList, CostTable, QuickAnswer, SourceNote, NotVerified, AdSlot
│  └─ pages/
│     ├─ index.astro
│     ├─ specs/index.astro, specs/[make]/index.astro, specs/[make]/[model]/index.astro, specs/[make]/[model]/[year]/index.astro
│     ├─ symptoms/index.astro, symptoms/[slug]/index.astro
│     ├─ codes/index.astro, codes/[code]/index.astro
│     ├─ repair-cost/index.astro
│     ├─ about/, sources/, authors/[slug]/, privacy/, contact/, 404.astro
│     └─ robots.txt.ts
├─ public/{indexnow-key}.txt, _redirects, _headers, favicon
└─ .github/workflows/daily-build.yml
```

## 2. 数据结构（核心原则：每个数值都带 source + verified）
通用“带来源的值”类型 `SourcedValue`：
```jsonc
{
  "value": "4.8 qt (4.5 L) with filter",   // 原文值，不做推算
  "source": "toyota-om0r024u",              // 指向 sources.json 的 id；无则 null
  "page": "p.666",                          // 手册页码/定位，可空
  "verified": true,                         // 人工核对过才为 true
  "note": "metric converted"                // 可空
}
```
渲染规则：`verified !== true` 或 `source == null` 或 value 以 `TODO` 开头 → 不显示数值，显示 **“Not yet verified — check your owner's manual”**（规格页）/ **“Source pending”**（症状页）；该字段也不进入 JSON-LD 与 meta 描述。CI 校验任何已发布页的可见值里不得出现 `TODO`。

### 2.1 sources.json
```json
{ "toyota-om0r024u": { "name": "Toyota RAV4 Owner's Manual OM0R024U", "url": "https://assets.sia.toyota.com/publications/en/om-s/OM0R024U/pdf/OM0R024U.pdf", "type": "oem-manual", "retrieved": "2026-10-15" },
  "nhtsa-recalls": { "name": "NHTSA Recalls API", "url": "https://api.nhtsa.gov/recalls/recallsByVehicle", "type": "government", "retrieved": "2026-10-15" },
  "fueleconomy": { "name": "fueleconomy.gov", "url": "https://www.fueleconomy.gov/", "type": "government", "retrieved": "2026-10-15" },
  "repairpal": { "name": "RepairPal Estimator", "url": "https://repairpal.com/estimator", "type": "third-party", "retrieved": "2026-09-03", "note": "national avg, excl. tax/location" } }
```

### 2.2 vehicles/{year}-{make}-{model}.json（示例取自现有数据）
```jsonc
{
  "slug": "2020-toyota-rav4", "year": 2020, "make": "Toyota", "model": "RAV4",
  "makeSlug": "toyota", "modelSlug": "rav4",
  "vpicConfirmed": true,
  "publishDate": "2026-11-03", "dataUpdated": "2026-10-15",
  "manual": { "id": "toyota-om0r024u", "yearConfirmed": false,  // 原表注明：发布前须到 toyota.com 车主门户确认
              "note": "OM0R024U, PDF created 2019-07-22" },
  "specs": {
    "oilCapacity":  { "value": "4.8 qt (4.5 L) with filter; 4.4 qt without", "source": "toyota-om0r024u", "page": "p.666", "verified": true },
    "oilViscosity": { "value": "SAE 0W-16 (0W-20 acceptable)", "source": "toyota-om0r024u", "page": "p.667", "verified": true },
    "tireSize":     { "value": "225/65R17 102H (17-in type A)", "source": "toyota-om0r024u", "page": "p.671", "verified": true },
    "tirePressure": { "value": "35 psi front/rear (type A); 36 psi (type B)", "source": "toyota-om0r024u", "page": "p.671", "verified": true },
    "wiperSizes":   { "value": null, "source": null, "verified": false },
    "batteryGroup": { "value": null, "source": null, "verified": false }
  },
  "fuelEconomy": [ { "feId": "42181", "option": "Auto (S8), 4 cyl, 2.5 L, SIDI & PFI", "engineL": 2.5, "cyl": 4,
                     "trans": "Automatic (S8)", "drive": "Front-Wheel Drive", "mpgCity": 27, "mpgHwy": 35, "mpgComb": 30,
                     "fuel": "Regular", "source": "fueleconomy", "url": "https://www.fueleconomy.gov/ws/rest/vehicle/42181", "verified": true } ],
  "recalls": [ { "campaign": "20V682000", "component": "FUEL SYSTEM, GASOLINE:DELIVERY:FUEL PUMP",
                 "date": "2020-11-04",          // 原数据 04/11/2020 (DD/MM/YYYY) → 导入时转 ISO
                 "summary": "…", "source": "nhtsa-recalls", "verified": true } ],
  "relatedSymptoms": ["brakes-squeaking"], "relatedCodes": ["p0455"]
}
```
注：2020 RAV4 的 `manual.yearConfirmed=false` 时，整组手册字段按“未核实”处理（README 说已核实，CSV 备注说未核实——两份资料冲突，请小站以最新为准改数据，代码只认 `yearConfirmed`）。

### 2.3 symptoms/{slug}.json 与 codes/{code}.json（同一 schema，type 区分）
```jsonc
{
  "slug": "brakes-squeaking", "type": "symptom",          // 或 "code"
  "code": null, "title": "Brakes Squeaking", "targetKeyword": "brakes squeaking",
  "definition": { "value": null, "source": null, "verified": false },   // code 页：SAE J2012 定义 + 公开来源
  "quickAnswer": null,                                                  // ≤50 词，所有引用值齐全才显示
  "causes":   [ /* { "text": "...", "source": "...", "url": "...", "verified": true } */ ],
  "severity": { "value": null, "source": null, "verified": false },
  "canIDrive":{ "value": null, "source": null, "verified": false, "safetyDefault": "Have it inspected promptly." }, // 刹车/ABS 页
  "diagnosis": [],
  "costs": [ { "repair": "Brake pad replacement", "rangeUsd": [335, 394], "source": "repairpal",
               "url": "https://repairpal.com/estimator/brake-pad-replacement-cost", "sourceDate": "2026-09-03", "verified": true } ],
  "faq": [],                         // 只放页面上真实可见、有来源的问答
  "related": { "symptoms": ["grinding-noise-when-braking"], "codes": [], "vehicles": ["2020-toyota-rav4"] },
  "publishDate": "2026-11-04", "dataUpdated": "2026-10-15"
}
```
故障码页 P0455 等的 costs 目前是 `TODO`（RepairPal 从共享电脑被 Cloudflare 拦截），按规则整行隐藏，表为空则整段隐藏。

### 2.4 发布门槛（CI 自动判定）
- 规格页：机油、胎压、轮胎、召回、油耗 5 项中缺失项显示“Not yet verified”即可上线（按里程碑 M2）。
- 症状/故障码页：`causes` 至少 1 条有来源，否则 `publishDate` 视为无效、不发布（README：症状页只上有来源的内容）。CI 输出“可发布/阻塞原因”清单给小品。

## 3. 模板映射
| URL | 模板 | 数据 |
|---|---|---|
| `/` | Home（年/品牌/车型选择 + 热门症状/故障码） | vehicles、symptoms、codes 索引 |
| `/specs/` `/specs/{make}/` `/specs/{make}/{model}/` | Hub 列表 | vehicles 聚合 |
| `/specs/{make}/{model}/{year}/` | SpecPage（templates.md 第 1–8 节） | vehicles/*.json |
| `/symptoms/`，`/symptoms/{slug}/` | Hub / IssuePage | symptoms/*.json |
| `/codes/`，`/codes/{p0xxx}/` | Hub / IssuePage(code 变体) | codes/*.json |
| `/repair-cost/` | CostIndex（汇总已有来源的费用条目，P3，先做简单表） | repair-costs/*.json |
| `/about/` `/sources/` `/authors/{pen-name}/` `/privacy/` `/contact/` | StaticPage（Markdown） | 文案由小站/小品给 |
Hub 页只列已发布页，空 hub 不生成。标题/meta/H1 公式完全按 templates.md，由小搜定稿后写进模板常量。

## 4. URL 与 slug 规则
- 全小写、ASCII、连字符；空格和 `/`→`-`，去掉其他符号：`Model Y`→`model-y`，`CR-V`→`cr-v`，`F-150`→`f-150`。
- 车型 slug 以 keyword_map 的 target_url 为准（如 Silverado：数据 slug 是 `2022-chevrolet-silverado-1500`，需与小站确认 URL 用 `silverado` 还是 `silverado-1500`，二选一，另一个 301）。
- 故障码小写：`/codes/p0455/`；大写访问 301 到小写。
- **统一尾斜杠**：Astro `trailingSlash: 'always'` + `build.format: 'directory'`；Cloudflare `_redirects` 把无斜杠 301 到有斜杠；`www`→apex 301（Cloudflare 重定向规则）。
- 每页自引用绝对 canonical：`https://carspecfix.com{path}`。

## 5. Sitemap / robots / IndexNow
- `@astrojs/sitemap` 生成 `sitemap-index.xml`，只含已发布页；`lastmod` = 数据文件的 `dataUpdated`（不是构建时间），与页面上 “Updated YYYY-MM-DD” 同源。
- robots.txt：全部允许 + Sitemap 行。
- IndexNow：`public/{key}.txt` 放密钥；部署成功后 `scripts/indexnow.ts` 对“今天新发布 + dataUpdated 变化”的 URL 批量 POST `https://api.indexnow.org/indexnow`（Bing/Yandex 等支持，谷歌不支持）。
- GSC：域名资源（DNS TXT），上线当天提交 sitemap；Bing 站长工具从 GSC 导入。谷歌没有对应的推送接口，靠 sitemap + 内链。

## 6. 结构化数据（JSON-LD，只标记页面可见内容）
| 页面 | 类型 |
|---|---|
| 全站 | `WebSite`（首页）、`Organization`（首页/About） |
| 规格页 | `BreadcrumbList` + `Article`（author=笔名 Person，datePublished/dateModified）+ `Car`（name、manufacturer、model、vehicleModelDate、fuelEfficiency 仅含已核实值）。不加评分 |
| 症状/故障码页 | `BreadcrumbList` + `Article`；`FAQPage` 仅当页面有可见且有来源的问答（富结果不保证展示） |
| 保养教程（后续） | `HowTo` + `BreadcrumbList`（试点 30 页不含） |
| Hub 页 | `BreadcrumbList` + `CollectionPage` |
| 作者页 | `ProfilePage` + `Person` |
CI 用 schema 校验脚本检查 JSON-LD 不含未核实值；上线前小搜用 Rich Results Test 抽检。

## 7. 每日放量机制
- 每个数据文件带 `publishDate`（YYYY-MM-DD，美东时区判断）。构建时过滤 `publishDate <= today && 通过发布门槛`。
- `.github/workflows/daily-build.yml`：`cron: '0 13 * * *'`（UTC 13:00 = 北京时间 21:00 / 美东上午）+ 手动触发 + push 触发 → `npm ci && validate && astro build` → `wrangler pages deploy` → `indexnow`。
- 排期由 `scripts/schedule.ts` 生成：读 30 页优先级，按每天 ~10 页填 publishDate；推迟某页只改日期即可。
- 试点 30 页 = 15 规格页 + 8 症状页 + 7 故障码页（现有数据文件刚好 30）；另有首页、hub、About/Sources/Author/Privacy/Contact 第一天上线，不计入 30。按 templates.md：第 1 天首页+支撑页+7 页，第 2–3 天其余。

## 8. 性能预算
- 每页 HTML ≤ 50 KB（gzip 前），CSS ≤ 20 KB（构建期 Tailwind 裁剪），**默认 0 KB JS**；首页车型选择器为唯一交互岛，≤ 10 KB。
- 字体用系统字体栈；图片（如有）AVIF/WebP + 宽高属性；无第三方脚本（统计脚本除外）。
- 目标：手机 Lighthouse 性能 ≥ 95，LCP < 2.0s，CLS < 0.05，INP < 200ms；CI 跑 Lighthouse CI 对 4 类模板各抽 1 页，不达标构建失败。
- 广告位（后期 AdSense）预留固定高度容器，放表格下方/侧栏，不插在数字之间，防 CLS。

## 9. 统计（零成本）
Cloudflare Web Analytics（无 cookie）看访问；GSC 看曝光/点击/CTR（复盘决策用）；Bing 站长工具。复盘阈值由小搜在 seo-plan 定稿，代码侧不埋任何流量假设。

## 10. 需要队长决定/提供
1. **Cloudflare 账号**：把 carspecfix.com 的 DNS 托管到 Cloudflare（或告诉我注册商，若已在 Cloudflare 注册则跳过）。
2. **GitHub 账号/组织**：建一个仓库（建议私有）；在仓库 Secrets 里放 Cloudflare API Token（Pages 编辑权限）和 Account ID——需队长本人登录生成，我不碰凭据之外的东西。
3. **Google Search Console / Bing 站长工具**：用队长的 Google/Microsoft 账号添加域名资源（DNS TXT 验证可由我在 Cloudflare 里加，如果授权）。
4. **笔名作者**的名字与简介、**联系邮箱**（Contact/Privacy 必需；可用 Cloudflare Email Routing 免费转发）。
5. 上线日期（M4 起点）——上线属于需要队长拍板的事项。
6. 托管二选一确认：Cloudflare Pages（推荐）/ GitHub Pages（仓库须公开）。

## 11. 风险
| 风险 | 对策 |
|---|---|
| 手册数据缺失（14 款车目前全 TODO） | 规格页按“Not yet verified”上线；CI 阻止 TODO 外泄 |
| 2020 RAV4 手册年款核实结论两份资料矛盾 | 以 `manual.yearConfirmed` 为准，确认前按未核实显示 |
| 症状页无来源 → 发布门槛不过，30 页可能凑不齐 | CI 每日输出阻塞清单；缺口由小站补，排期顺延 |
| RepairPal 在共享电脑被 Cloudflare 拦截 | 由小站浏览器手工采集并记录来源日期；代码不抓取 |
| NHTSA 日期格式 DD/MM/YYYY | 导入脚本统一转 ISO，加单测 |
| 薄内容/模板化页面被判低质 | 每页至少有已核实的独特数据才发布；hub 不生成空页 |
| 免费档限额（Cloudflare Pages 每月构建次数有上限） | 每日 1 次 + 少量手动，远低于上限；具体额度上线前在官网核实 |
| GitHub Actions cron 有延迟、长期无提交的仓库会停用定时任务 | 允许数小时延迟；保持定期提交或手动触发 |

## 12. v2 决策更新（2026-10-15 群内确认，优先于上文）
1. **Silverado**：slug `silverado-1500`（URL `/specs/chevrolet/silverado-1500/2022/`），1500 与 2500HD 视为不同车型；Title/H1 用 “Chevrolet Silverado 1500”。数据字段 `modelSlug`=`silverado-1500`，`model`=`Silverado 1500`。
2. **2020 RAV4**：手册年款未确认 → `manual.yearConfirmed=false`，页面标记“未确认”，**不进第一批收录**；确认后再排期。
3. **试点 30 页 = pages.csv 中 P1**（15 年款 + 8 症状 + 7 故障码），构建脚本与 pages.csv 比对 0 差异（R-U1）。不做单属性页，年款页用锚点 `#oil #tires #mpg #recalls #problems`（R-L6）。
   - **年款页闸门**：机油（容量+粘度）和轮胎（尺寸+胎压）均有手册出处，且召回、油耗已抓取。
   - **症状/码页闸门**（采用 SEO 定稿）：≥3 条带来源的原因 + 至少 1 条带来源的修理费区间。（取代 §2.4 中“≥1 条原因”。）
   - **不达标 = 不生成页面**（延后上线），不以 noindex 发布。
4. **车型汇总页 4 个**：RAV4、F-150、Camry、CR-V，M3 做模板，M4 随第一批上线，不计入 30。试点不生成品牌页 `/specs/{make}/`、`/specs/` 和 `/repair-cost/`（访问 404；面包屑品牌层只显示文字不链接）。（取代 §3 中品牌 hub 与 /repair-cost/。）
5. **电车（2023 Model Y）闸门**：轮胎尺寸+胎压（手册）、续航+电耗（fueleconomy.gov）、召回（NHTSA）。电车专属可选字段 `battery12v`，不作门槛。schema 用 `powertrain: "ev"` 切换闸门和模板区块（隐藏机油区）。
6. **RepairPal 引用规则**：只展示价格区间；标 “Source: RepairPal” + 链接 + 数据日期；每页只放相关几项；注明 “National average, excludes tax; varies by location”。服务条款待小站核实——在核实前 `sources.json` 中 `repairpal.tosCleared=false`，构建对引用 RepairPal 的页面给出警告（不阻断本地构建，阻断正式发布）。
7. **新增数据字段**：每个来源值带 `sourceGrade`（A=OEM 手册/政府数据，B=第三方，C=二手资料，C 级不过闸门）；每页带 `signOff: {by, date}`（人工核对签字，SEO 定稿要求试点 100% 核对），无签字不发布。
8. **schema.org 调整**：按 R-D4 禁用 HowTo/Product/Offer/AggregateRating/Review（取代 §6 中 HowTo 行）。
9. **性能指标**：验收以 R-P2 为准（Performance ≥90、SEO=100、A11y ≥90、LCP<2.5s、CLS<0.1、TBT<200ms）；§8 的 95 分作为内部目标。
10. **占位文案**：因 R-Q3 要求 `dist/` 中 grep "todo" 为 0，作者名/邮箱占位用 `[PENDING-队长]` 标记，正式发布前 CI 拦截该标记。

### 与 SEO 需求的冲突/待定
- **R-Q1 vs 决定 3**：R-Q1 写“不达标→noindex”，团队决定“不达标→不生成”。按团队决定实现（更严格，同样满足“不进 sitemap、不被链接”）；请小搜把 R-Q1 文案改一下。
- **R-U2 一跳 301**：`http://www.…/Specs/…/2020` 一跳到规范 URL。Cloudflare 的 “Always Use HTTPS” 会先跳一次，变成两跳；Pages `_redirects` 也做不了大小写转换。方案：关闭 Always Use HTTPS，改用一条 Cloudflare Single Redirect 动态规则（`lower()` + 拼接 https 主域 + 补斜杠）一次完成；如免费档表达式不够用，用 Pages Function 兜底。需上线前实测，暂列风险。
- **RAV4 汇总页 vs 2020 RAV4 延后**：SEO 定稿要求汇总页“已上线年款 ≥2 个”。2020 RAV4 延后后，RAV4 第一批只有 2024 一个年款 → 建议 RAV4 汇总页随 2020 RAV4 一起上线（或小品/小搜同意放宽）。实现上做成自动判断：已发布年款 <2 的汇总页不生成。
- **R-L3 每页至少 2 个入链**：试点页之间可链接的已发布页少（如 Equinox 只有 1 个年款、无汇总页），入链要靠首页 + 症状/码页的“Vehicles we cover”补；构建报告会列出孤立页。

## 13. M3 任务拆分（v2，整合 seo-dev-requirements P0/P1）
| # | 任务 | 覆盖需求 | 估时 |
|---|---|---|---|
| 1 | Astro 初始化、Tailwind 构建期编译、Base 布局、lang=en、canonical、OG | R-M1 R-M3 R-M4 R-P1 R-U5 | 0.5 天 |
| 2 | 数据 schema（sourceGrade、signOff、publishDate、powertrain）+ 导入脚本（ISO 日期）| R-C4 | 1 天 |
| 3 | 闸门 + 校验报告（index/阻塞原因、TODO 扫描、pages.csv 比对、title/H1 唯一性、相似度、孤立页/坏链、内链数）| R-Q1–Q4 R-M2 R-L3 R-L4 R-U1 | 1.5 天 |
| 4 | 年款页模板（锚点目录、按配置分行、出处、Updated、Report a wrong spec、EV 变体）| R-C1–C6 R-L6 R-D2 | 1.5 天 |
| 5 | 症状/故障码模板（RepairPal 引用规则、免责声明）| R-D3 R-C1 | 1 天 |
| 6 | 首页、4 个车型汇总页、/symptoms/、/codes/ 索引、404 | R-U3 R-U4 R-O2 R-L1 R-L2 | 1 天 |
| 7 | About / Sources / Author / Privacy / Contact | R-O1 | 0.5 天 |
| 8 | JSON-LD + 面包屑 + 禁用类型检查 | R-D1–D4 | 0.5 天 |
| 9 | sitemap（只含已发布 index 页、真实 lastmod）、robots、IndexNow 脚本 | R-S1–S3 | 0.5 天 |
| 10 | GitHub Actions 每日构建 + 部署 + 排期 | R-Q4 | 0.5 天 |
| 11 | 重定向规则（一跳 301）+ 缓存头 + 上线前实测 | R-U2 R-P4 | 0.5 天（需 Cloudflare 账号） |
| 12 | 性能/移动端（390px、表格横滑）+ Lighthouse 检查 | R-P2 R-P3 R-P5 R-C7 | 0.5 天 |
| 13 | 按视觉稿调样式 + SEO 检查返工 | — | 1.5 天 |
| | **合计** | | **约 11 个工作日**（原 9 天；增加闸门/报告、EV 变体、重定向实测） |

## 14. 开发进度（2026-10-15 20:20）
- 代码在 `/workspace/carspecfix/site`（本地 git，4 个提交，未推送、未部署）。`npm run build` = 构建 + 发布门槛 + SEO 自检，报告在 `site/reports/build-report.md`；`PREVIEW=1` 生成含全部 30 页的 noindex 预览版（`dist-preview/`）。
- 签核：读取 spec_pages.csv 的 `reviewed_by / reviewed_at / signoff=yes`；签一页放一页，签核当天的夜间构建上线，每天最多 10 页（导入脚本自动排期）。
- 视觉：已接入小图 `design/` 的 tokens.css + components.css（原样复制，改动只放在 `src/styles/site.css`：系统字体、对比度修正、手机菜单）。
- **轮胎改为多行（v3）**：`specs.tires.rows[] = { wheel, config, tireSize, frontPsi, rearPsi, page, source, sourceGrade }`，模板渲染多行表；闸门 = 至少 1 行同时有尺寸、前/后胎压、A 级手册来源。旧 CSV 自由文本由 `scripts/tires.mjs` 保守解析（解析不了的不显示），以后建议小站/小数直接按行录入。
- 已签核：2022 Civic、2024 CR-V（仅燃油版，混动显示 Not yet verified）——两页均通过闸门。`manuals/sources.tsv` 中的存档 PDF 已关联到 sources.json 的 `archived` 字段。
- 小图 v2 到位前样式不再打磨；样式集中在 `src/styles/`，换 v2 只需替换该目录 + 少量 class。

## 15. v4 更新（2026-10-15 20:40）
- 按 seo-dev-requirements v2 + user-needs.md：标题 ≤60 字符（构建报错）、lang=en-US、无 FAQPage、无 noindex（未达标页直接不生成）、内链只按数据关系、入链 ≥1。
- 维修费用模块和 RepairPal 数据全部删除（服务条款禁止）；症状/故障码页门槛 = A 级“能否继续开/紧急程度” + ≥1 条 A 级原因 + 签字。原因来自 symptom_code_sources.json，按“厂家文档 + 适用车型”展示。
- 采用 design-v3 Revision 2；字体自托管（@fontsource），不请求 Google Fonts。
- 轮胎数据以 tire_rows.csv 为准；配图以 images/image_sources.csv 为准（严格解析，格式错误则构建失败；只渲染已签字行，否则显示轮廓占位图）。
- 反馈按钮和纠错表单已做 UI 和前端逻辑，存储走 public/feedback.js 可插拔桩（目前存本地 localStorage），事件统计工具待队长定。

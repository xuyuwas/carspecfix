# CarSpecFix SEO 方案（定稿 v1，2026-10-15，小搜）

> 基于小站初稿 `prototype/seo-plan.md` 审核重写。
> **数据声明**：目前唯一核实过的数据是 `car specs`（Semrush，队长提供：US 1.0K/月、KD 28%、CPC $1.81；UK 4.4K）。`keyword_map.xlsx`（48,461 个词 / 780 页）来自谷歌搜索联想，**没有搜索量**；`pages.csv` 里的 `n_secondary` 是**联想变体的数量，不代表搜索量**，不能当流量估算用。下文所有阈值都标了核实方式：**[Semrush]** = 上线前用 Semrush 核实；**[GSC]** = 上线后用 GSC 实测数据校准；**[经验值]** = 没有依据的起始值，试点后按 GSC 调整。

---

## 0. 和初稿相比的主要改动
1. **试点 30 页范围按 `pages.csv` 的 P1 定死**：15 个年款规格页、8 个症状页、7 个故障码页（清单见第 3 节）。初稿写的是“15 款车”加笼统的 30 页。
2. **新增“差异化与 scaled content 风险”专章（第 2 节）**：竞品是同样的批量生成模式，我们靠逐条出处、按发动机/配置拆分、修正入口、人工抽检来拉开差距，并设定“不达标不收录”的质量闸门。
3. **薄页规则改成可执行的**：初稿要求“3 个已核实模块”，但对试点会卡死（14 款车目前只有 MPG 和召回）。改成**核心字段**闸门（机油容量+规格、轮胎尺寸+胎压，两项都得有手册出处），跟小品里程碑 M2 的“机油、胎压、轮胎、召回、油耗齐了就上线”对齐。
4. **舍弃 HowTo schema**（谷歌已不再展示 HowTo 富结果），FAQPage 降级为可选；Vehicle/Car schema 只填已核实字段。
5. **统一模板冲突**：templates.md 和初稿的 Title/H1 不一致，这里给出唯一版本；数据来源页统一用 `/sources/`（初稿写 `/data-sources/`）。
6. **第 4–6 周判断规则全部改成带核实方式的阈值**，并且拆分成收录、曝光、CTR 三步判断；“曝光高 CTR 低就是被 AI 截流”这一推断改成需要先排除排名和 Title 因素。
7. **AdSense 申请时机后移**：从“试点有点击就申请”改成“收录和流量稳定后再申请”，和小品里程碑 M5 一致。
8. 开发相关需求全部拆到 `seo-dev-requirements.md`，写成可验收条目。
9. 删掉“90 天里程碑”章节，进度以小品的里程碑为准，避免两套时间表。

---

## 1. 关键词与页面对应规则
| 页面类型 | URL | 主词 | 副词 / 归属 |
|---|---|---|---|
| 首页 | `/` | car specs（已核实） | car specs by year make model、vehicle specs lookup **[Semrush] 核实量和意图** |
| 品牌页 | `/specs/{make}/` | {make} specs | 试点期不上线（见 3.3） |
| 车型汇总页 | `/specs/{make}/{model}/` | {model} specs by year | 试点期只有已上线年款 ≥2 个的车型才上（RAV4、F-150、Camry、CR-V） |
| 年款页 | `/specs/{make}/{model}/{year}/` | {year} {model} specs | 同一年款的所有属性词：oil capacity / oil type / tire size / tire pressure / recalls / mpg / towing / fuse box… |
| 症状页 | `/symptoms/{slug}/` | 症状词 | 原因、能不能开、修理费变体 |
| 故障码页 | `/codes/{code}/` | {code} code | {code} {make}、{code} meaning（不按品牌拆页） |
| 保养教程 / 修车费 | `/maintenance/` `/repair-cost/` | — | P2/P3，试点不做 |

规则：
1. 一个词只分配给 keyword_map 里的一个页面（keyword_map 已满足，新增词也必须先登记）。
2. **不做单属性页**（如 `/2020-rav4-oil-capacity/`）。这是和竞品最大的结构差异，也是规避 scaled content 的关键：属性页 = 同一模板换一个字段，正是批量站的典型形态。年款页用锚点（`#oil`、`#tires`）承接属性词。
   - 例外条件：GSC 中某属性词持续落到年款页但排名长期在第 2 页以后，且该属性有足够独立内容（如按发动机拆分的机油表），再评估拆页。阈值：**[GSC] 连续 4 周平均排名 > 20 且曝光量排该页前 3 的查询**，[经验值]。
3. 「年款+车型+症状」词归年款页的 Common problems 区块，链到通用症状页。
4. 首页不放具体年款、故障码或症状词作为主词（可以作为入口链接）。
5. 抢词处理：每周看 GSC，同一查询 2 个 URL 轮流排名 → 优先调整内链锚文本和页面主题；仍无效再 301 合并。判定：**[GSC] 同一查询 2 周内出现 2 个以上 URL**，[经验值]。

**上线前要用 Semrush 核实的词**（我们没有任何量的数据）：
- 15 个试点年款的 `{year} {model} specs` 与 `{year} {model} oil capacity`、`tire pressure` 的相对量 —— 决定 Title 里属性词的排序。**[Semrush]**
- 7 个故障码、8 个症状主词的量和 KD。`abs light on`、`p0301 code` 在 pages.csv 里 n_secondary=0，说明联想没挖到变体，不代表没量，必须核实。**[Semrush]**
- 竞品（oilcapacity411.com 等）的自然词分布：看它们流量主要来自 oil capacity 还是 specs。**[Semrush]**

## 2. 差异化与 scaled content 风险
### 2.1 竞品观察（2026-10-15）
- **oilcapacity411.com**：首页宣称 78,416 条规格、3,835 款车、2000–2026 年款、“Human-verified OEM data, not AI-generated”，属于 “The 411 network”（同一团队多个站）。首页卡片每车只给一个数值或区间（如 2024 F-150 “6.0–8.0 qt”），不按发动机拆分，首页看不到手册页码出处。（具体年款页尚未抓取，单页结构待补查。）
- **oilcapacitycheck.com**：抓取时返回 Cloudflare 1033 错误（站点不可用），本次无法分析，稍后复查。
- 两个都是 2026 年新站且已进 2020 rav4 oil capacity 首页（队长/小站观察）—— 说明这个词的竞争门槛不高，但同模式的站会越来越多，谷歌对这类站的打击风险也同样落在我们身上。

### 2.2 我们的差异化（每条都要在页面上看得见）
1. **逐值出处**：每个数字旁边写手册文件号+页码 / NHTSA 召回编号 / fueleconomy.gov 链接。竞品只在首页口号上说“verified”，我们在每一格里证明。
2. **按配置拆分**：机油容量、MPG 按发动机/驱动方式分行（例：2024 F-150 不同发动机的容量分别列，而不是“6–8 qt”区间）。这是用户真正需要、AI 一句话答不全的信息。
3. **规格 + 故障的双栏目闭环**：年款页 → 该车相关召回、常见症状、故障码；症状/码页 → 受影响年款。单一属性站做不到。
4. **缺失就说缺失**：没有来源的字段显示 “Not yet verified — check your owner's manual”，不估算、不用同平台车型替代。
5. **更正机制**：每页 “Report a wrong spec”，更正记录在 `/sources/` 公开。
6. **数量克制**：试点 30 页、第二批 200 页，都低于竞品数量级。我们不和它们比页数。

### 2.3 规避 scaled content abuse（质量闸门）
谷歌的 scaled content abuse 政策针对的是“主要为操纵排名、对用户价值很低的批量页面”，与是否用模板或程序生成无关。所以闸门是按**价值**设的：
- **收录闸门（年款页）**：机油（容量+粘度）与轮胎（尺寸+胎压）两项都有手册出处，**并且**召回、MPG 已抓取 → 允许 index。否则 `noindex` 且不进 sitemap。这是 [经验值]，试点后看 GSC“已抓取 - 尚未编入索引”的比例调整 **[GSC]**。
- **收录闸门（症状/码页）**：至少 3 个原因，每个都有可引用来源，且有修理费区间（带来源和日期）→ index；否则 noindex。[经验值]
- **页面差异度**：同类页面去掉模板文字后，独有内容（数值+文本）必须占主体。构建时算两两相似度，同模板任意两页的正文相似度超过阈值就报警（阈值：**[经验值] 80%**，见开发需求 R-Q2）。
- **人工抽检**：每批上线前人工核对至少 20% 页面的数值与出处（试点 30 页要 100% 核对）。[经验值]
- **放量节奏**：每天约 10 页，不一次性推送几百页；第二批 200 页必须在试点通过第 6 节判断后才放。
- **不使用 AI 生成的原因/建议文本却不标来源**：症状页的文字可以辅助撰写，但每个事实性陈述都要对应来源，并由人工过一遍。

## 3. 试点 30 页（= pages.csv 中 P1）
### 3.1 年款页（15）
2022 Tacoma、2022 Silverado 1500、2023 F-150、2021 F-150、2022 Corolla、2024 RAV4、2022 Civic、2022 Accord、2020 RAV4、2022 Camry、2024 Camry、2022 Equinox、2024 CR-V、2022 CR-V、2023 Model Y。
- 风险：2023 Model Y 是电车，没有机油，收录闸门要换成“轮胎+续航/电池（fueleconomy.gov）+召回”。**需要小站确认 Model Y 的数据字段**。
### 3.2 症状页（8）
car shaking when accelerating、car cranks but wont start、brakes squeaking、car jerks when accelerating、car shakes when braking、grinding noise when braking、car wont start clicking、abs light on。
### 3.3 故障码页（7）
p0420、p0171、p0300、p0455、p0442、p0456、p0301。
### 3.4 配套页（不计入 30）
首页、`/codes/`、`/symptoms/`、4 个车型汇总页（RAV4、F-150、Camry、CR-V）、`/about/`、`/sources/`、`/authors/{name}/`、`/contact/`、`/privacy/`。试点期**不上品牌页**（每个品牌只有 1–4 款车，太薄）；面包屑里的品牌层可以显示文字但不链接，或链接到首页的品牌锚点（由小码定）。

## 4. 页面模板（唯一版本，以此为准）
- **首页**　Title：`Car Specs by Year, Make & Model – Oil, Tires, Recalls & Fixes | CarSpecFix`；H1：`Car Specs by Year, Make & Model`；H2：Look up a trouble code / What's wrong with my car? / Popular vehicles。
- **年款页**　Title：`{Year} {Make} {Model} Specs: Oil Capacity, Tire Size & Pressure, Recalls | CarSpecFix`（属性词排序在 Semrush 核实后调整 **[Semrush]**）。
  H1：`{Year} {Make} {Model} Specs`。
  Meta：`Owner's-manual specs for the {Year} {Make} {Model}: oil {oil}, tires {size} at {psi} psi, MPG and {N} NHTSA recalls — every number cited.` 缺值的片段整段删除，不写占位符。
  H2 顺序：Quick specs / Engine oil / Tires / Engines & MPG / Recalls / Common problems / Sources。没有数据的模块整块隐藏（不显示空 H2）。
- **症状页**　Title：`{Symptom}: Causes, Is It Safe to Drive & Repair Cost | CarSpecFix`；H1：`{Symptom}`；H2：Quick answer / Common causes / How serious is it / Can I still drive / How it's diagnosed / Repair cost / Vehicles we cover / Sources。
- **故障码页**　Title：`{CODE} Code: {Definition} – Causes, Can You Drive & Repair Cost`（超长时去掉“Can You Drive”）；H1：`{CODE}: {Definition}`；H2 同症状页，开头加 What it means（SAE 定义）。
- Title 长度：目标不超过约 60 字符，超出由模板自动降级（去掉末尾属性词，品牌名保留）。[经验值]

## 5. 结构化数据
- 全站：`Organization` + `WebSite`（站内搜索可用后再加 `SearchAction`）。
- 年款页：`Car`（brand、model、vehicleModelDate，只填已核实字段）+ `BreadcrumbList` + `Article`/`WebPage` 的 dateModified 和 author。
- 症状/码页：`Article` + `BreadcrumbList`；`FAQPage` 只标记页面上真实可见的问答，且只是可选——谷歌目前基本只对权威政府/健康站展示 FAQ 富结果，不要期待展示。
- 不用：`HowTo`（富结果已停止展示）、`Product`/`Offer`/`AggregateRating`（不卖东西、没有真实评分）。
- 验收：Rich Results Test 无错误；schema 中的数值与页面可见数值一致。

## 6. 收录、衡量与第 4–6 周判断规则
工具：GSC（主）、Bing Webmaster、Cloudflare Web Analytics。上线当天提交 GSC、Bing、IndexNow（谷歌不支持 IndexNow，只靠 sitemap 和内链）。

**判断按顺序走，前一步不过不看后一步**（所有阈值都是 [经验值] 起始值，用 GSC 实测校准）：
1. **收录**（上线后第 2 周看）：GSC 页面报告中 30 页收录 < 50% → 不加新页，先查 canonical、robots、内链、是否被判重复/低质。核实：**[GSC] 页面编入索引报告 + 网址检查**。
2. **曝光**（第 4 周看）：收录页中有曝光的页面 < 50% → 查主词匹配度、Title、内链；不加页。核实：**[GSC] 效果报告按网页筛选**。
3. **点击 / CTR**（第 4–6 周看）：
   - CTR 先和**同排名区间**对比，不和全站平均比。我们没有行业基准，基准用自己的数据：试点页按平均排名分组（1–3 / 4–10 / 11–20）后算组内中位 CTR，低于组内中位一半的页面列为“CTR 异常”。**[GSC]**
   - 有曝光也有点击，且多数页面排名在前 20 → 放第二批 200 页（P2），每天约 10 页。**[GSC]**
   - 排名前 10 但 CTR 异常 → 先改 Title/Meta 测 2 周；仍低，再结合 SERP 是否出现 AI Overview（人工搜索确认）判断是否被 AI 截流，再考虑转向修车费、配置对比内容。**[GSC] + 人工查 SERP**
   - 几乎没有曝光 → 回到第 1 步。
4. **竞品对照**：每两周用 Semrush 看 oilcapacity411.com 的自然流量趋势和排名词变化，如它们大幅下滑（可能被算法处理），我们放量要更保守。**[Semrush]**
5. **AdSense**：收录和流量稳定后再申请（判断“稳定”：**[GSC] 连续 4 周日点击无明显下滑趋势**，[经验值]）。Ezoic/Mediavine 门槛会变，申请前查官网。

## 7. 内链规则
- 层级：首页 → （车型汇总页）→ 年款页，全部有面包屑。
- 年款页：同车型其他已上线年款、该车常见症状和故障码 3–5 个、`/sources/`。
- 症状/码页：受影响的已上线年款页、相关症状/码 3–5 个。
- 锚文本用目标页主词的自然写法（如 “2020 RAV4 specs”、“P0420 code”），不要全站堆完全相同的精确匹配锚文本。
- 每个可收录页至少有 2 条来自其他可收录页的链接；不链接到 noindex 页或未上线页（不能有指向 404 的链接）。
- 正文内链上限约 30 条/页，[经验值]，GSC 里没有直接指标，主要防止页面变成链接农场。

## 8. E-E-A-T
- `/sources/`：列出每个来源（车主手册文件号、NHTSA、fueleconomy.gov、修理费来源），写明抓取日期和更新频率，以及公开的更正记录。
- 每个数字后标出处；单位换算标 “converted”。
- 每页显示 “Updated YYYY-MM-DD”，与 sitemap lastmod、schema dateModified 一致，只在数据真实变化时更新。
- 作者页：笔名可以，但如实写身份（数据整理者，不是持证技师）和编辑流程。刹车、ABS、安全气囊类页面统一用保守安全提示。
- 修理费数据来源（初稿提到 RepairPal）：**需要小站确认是否可以引用、是否有使用条款限制**。

## 9. 英国流量与单位
- 所有数字双单位：qt/L、psi/kPa/bar、lb/kg。MPG 统一标 “US mpg”，不换算英制 mpg（避免误导）。
- 不做 en-GB 页面：英国车型配置不同，误导风险高。首页主词 UK 量（4.4K，Semrush）虽然高于 US，但我们的数据是美规车，英国流量只当附带。

## 10. 外链（零成本，第 3 周起）
1. Reddit / 车型论坛：以回答问题为主，只在确实有用时放具体页面链接，遵守各版块自推规则。
2. 有人工审核的汽车/工具目录。
3. 数据资产页：基于 NHTSA 公开数据的召回统计（第二批再做）。
4. 嵌入组件（规格卡片 iframe + 署名链接）：第二批再做，避免试点期分散精力。
- 不买链接、不做链接交换。

## 11. 需要决定的问题
| # | 问题 | 谁决定 | 建议 |
|---|---|---|---|
| 1 | 是否用 Semrush 核实第 1 节列出的约 45 个词（试点主词 + 属性词）？会占用队长的 Semrush 查询额度 | 队长 | 建议核实，上线前一次做完 |
| 2 | 年款页收录闸门用“机油+轮胎都有手册出处”，数据补不齐的年款先 noindex 上线还是延后上线？ | 队长 / 小站 | 建议延后上线，不放 noindex 薄页占爬取 |
| 3 | 2023 Model Y（电车）的字段与闸门 | 小站 | 换成轮胎+续航+召回 |
| 4 | 修理费数据来源及引用许可（RepairPal 等） | 小站 | 确认条款后再写进症状/码页 |
| 5 | 2020 RAV4 手册 OM0R024U 年款未确认 | 小站 | 发布前在 toyota.com 车主门户核对 |
| 6 | 试点期是否上线车型汇总页（4 个） | 小品 / 小站 | 建议上，用来承接内链 |

## 补充决定（10/15，群内确认）
- 2023 Model Y（电车）收录门槛：轮胎尺寸和胎压（手册出处）、续航和电耗（fueleconomy.gov）、召回（NHTSA）。12V 电池为可选字段，不作为门槛，没有出处时显示“尚未核实”。
- RepairPal 修理费数据：只引用价格区间，标明“来源 RepairPal”并附链接和数据日期；每页只引用相关几项；注明是全美平均价、不含税、各地有差异。服务条款待小站在上线前核实。
- 数据不齐的年款页推迟到数据补齐后再上线，不先用 noindex 上线。
- 4 个车型汇总页（RAV4、F-150、Camry、CR-V）在 M4 和第一批年款页一起上线，不占试水的 30 页名额。
- Silverado 网址用 silverado-1500。2020 RAV4 等手册年款确认后再放进首批收录。

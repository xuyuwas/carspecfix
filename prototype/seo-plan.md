# CarSpecFix SEO 方案（2026-10-15）

> 标注「未核实」的内容都没有数据支撑。目前唯一核实过的数据：Semrush 中 `car specs` 美国月搜索 1.0K、KD 28%、CPC $1.81、英国 4.4K（数据由队长提供）。词表来自谷歌搜索联想（`../keyword_map.*`，共 48,461 个词、780 页），**没有搜索量**。

## 1. 关键词与页面对应规则（防止页面互相抢词）
| 页面类型 | URL | 主词 | 副词来源 |
|---|---|---|---|
| 首页 | `/` | car specs | car specs lookup、vehicle specs by year make model |
| 品牌页 | `/specs/{make}/` | {make} specs | {make} models list |
| 车型汇总页 | `/specs/{make}/{model}/` | {model} specs by year | 各年款都适用的词 |
| 年款页 | `/specs/{make}/{model}/{year}/` | {year} {make} {model} specs | 同一年款的所有属性词：oil capacity、tire pressure、fuse box、towing、recalls、TPMS reset… |
| 症状页 | `/symptoms/{slug}/` | 症状词（brakes squeaking） | 原因、能不能开、修理费的变体 |
| 故障码页 | `/codes/{code}/` | {code} code | {code} {make}（同一个码不按品牌拆页） |
| 保养教程 | `/maintenance/{slug}/` | how to … | — |
| 修车费 | `/repair-cost/{part}/` | {part} replacement cost | — |

规则：
1. 一个词只分配给 keyword_map 里的一个页面。「年款+属性」词只归年款页，不单独做属性页（比如不做 /2020-rav4-oil-capacity/）。
2. 「年款+车型+症状」词归年款页的 Common problems 区块，同时链到通用症状页。等 GSC 显示有独立需求后再考虑拆页。
3. 首页不放具体年款、故障码或症状词。
4. 每周看一次 GSC：同一个查询如果有两个 URL 在轮流排名，就把弱的那页 301 跳到强的那页，或者调整锚文本。

## 2. 页面模板（title / meta / H1 / H2）
- **首页**　Title：`Car Specs by Year, Make & Model – Oil, Tires, Fuses & Fixes | CarSpecFix`；H1：Car Specs by Year, Make & Model；H2：Look up a trouble code / What's wrong with my car? / Popular vehicles。
- **年款页**　Title：`{Year} {Make} {Model} Specs: Oil Capacity, Tire Pressure, Fuses & Recalls | CarSpecFix`
  Meta：`{Year} {Make} {Model} oil capacity ({oil}), tire size, tire pressure, MPG and {n} NHTSA recalls — each value with its source.`（只用已核实的数值；值缺失时去掉对应片段，不要写占位符）
  H1：`{Year} {Make} {Model} Specs: Oil, Tires, Fuses & Recalls`；H2：Oil capacity & type / Tire size & pressure / Wipers / Battery / Fuse box / Towing / Fuel economy / Recalls / Common problems / TPMS reset。
  例：2020 Toyota RAV4，4.8 qt（手册第 666 页，年款待确认），6 条召回。
- **症状页**　Title：`{Symptom}: Causes, Can You Drive & Repair Cost | CarSpecFix`；H2：Possible causes / How serious / Can I still drive? / Repair cost / Affected vehicles。
- **故障码页**　Title：`{CODE} Code: Meaning, Causes & Repair Cost | CarSpecFix`；H1 同 Title；H2：Definition / Causes / Severity / Can I drive / Repair cost / By make。
- **修车费页**　Title：`{Part} Replacement Cost (US Average) | CarSpecFix`。

## 3. 结构化数据（schema.org）
- 全站：Organization + WebSite（加 SearchAction，对应故障码搜索框）。
- 年款页：Vehicle（brand、model、vehicleModelDate，只填已核实的属性）+ BreadcrumbList。
- 症状页、故障码页：BreadcrumbList；FAQPage 只用来标记页面上真实可见的问答。谷歌已经收紧了 FAQ 富结果的展示，加上不保证会显示（未核实当前政策细节）。
- 保养教程：HowTo + BreadcrumbList（谷歌对 HowTo 富结果的支持也已缩减，加上主要是帮助理解页面）。
- 修车费页：BreadcrumbList。不要用 Product/Offer，因为我们不卖东西。

## 4. 收录
- 上线当天在 GSC 和 Bing Webmaster 验证站点并提交 sitemap.xml。Bing 支持直接导入 GSC 的站点。
- 开启 IndexNow（Bing、Yandex 等支持，谷歌不支持），每次发布新页时推送 URL。
- sitemap 的 lastmod 只写数据或内容真实修改的日期，不写构建时间。
- 每天放约 10 页：先放 30 页试点，P2 和 P3 按效果再放。
- 防止页面太薄：
  - 年款页至少要有 3 个已核实的数据模块，否则 `noindex` 并且不进 sitemap。按现有数据，只有 2020 RAV4 满足，另外 14 款试点车目前只有 MPG 和召回，**需要先补手册数据**。
  - 症状页和故障码页的原因、能不能开等内容没有可引用的来源前，同样先 noindex。
  - 没有内容的品牌页和车型汇总页不上线。
- 每页都设置自引用 canonical，URL 统一用小写并以斜杠结尾。

## 5. 内链规则
- 层级：首页 → 品牌页 → 车型汇总页 → 年款页，每层都有面包屑。
- 年款页链接：同车型的上一年和下一年、该车的常见症状和故障码、对应的保养教程。
- 症状页和故障码页链接：受影响的年款页（反向链接）、相关修车费页、相关症状。
- 锚文本用目标页的主词（比如 “2020 RAV4 oil capacity”），每页最多约 30 条正文内链（经验值，未核实）。
- 不能有孤立页：每个上线页面至少有 2 条站内链接指向它。构建时检查一遍。

## 6. E-E-A-T（可信度）
- `/data-sources/`：列出每个来源，包括车主手册（文件号）、NHTSA、fueleconomy.gov、RepairPal，写明抓取日期和更新频率。
- 每个数字后面都标出处、页码或链接；单位换算要注明 “converted”。
- 每页显示 “Updated YYYY-MM-DD”，和 lastmod 保持一致。
- 作者页：用笔名可以，但要如实写明作者身份（数据整理者，不是持证技师）和编辑方法。安全类内容（刹车、安全气囊）统一提示 “have it inspected promptly”。
- 提供更正入口：联系页加上 “Report a wrong spec”。

## 7. 零成本外链
1. **目录站**：汽车和工具类目录、AI 工具目录（如果后面加了查询工具），只挑有人工审核的。
2. **Reddit 和论坛**（r/MechanicAdvice、r/cars、各车型论坛）：先认真回答问题，只在确实有用时放一条具体页面链接。不要群发，注意各版块的自推规则。
3. **免费嵌入组件**：比如「某车机油容量卡片」iframe，加一条署名链接，给车友博客和车型论坛用。
4. **HARO 类平台**（Qwoted、Featured、Help a B2B Writer 等）：回答记者关于用车成本和召回的提问。这些平台是否免费、是否还在运营，未核实。
5. **数据资产**：比如「2015–2025 召回最多的车型」（来自 NHTSA 公开数据），做成可引用的图表页，用来吸引自然链接。

## 8. 英国流量（英制 + 公制）
- 所有数字同时显示两种单位：qt/L、psi/kPa/bar、lb/kg、mpg（US）。注意英制 mpg 和美制 mpg 不一样，换算时要标明 “US mpg”。
- 页面不按英国车型做本地化。英国车型配置不同，会有误导风险，所以暂不做 en-GB 页面，只用双单位接住英国的通用词搜索。

## 9. 降低被 AI 回答取代的风险
- 一页给出整车全表加多个配置差异（按发动机和驱动方式），AI 一句话答不全。
- 提供可交互的东西：年款、品牌、车型选择器，故障码查询，复制和打印按钮。
- 准确的出处和页码，加上召回编号，可信度高于 AI 摘要。
- 修车费、多年款对比这类需要表格的内容放在前面。
- 衡量方法：如果曝光高但点击率明显偏低，就判断为被 AI 回答截流（阈值见下一节）。

## 10. 衡量和第 4–6 周的判断规则
工具：GSC（曝光、点击、CTR、排名、收录）、Bing Webmaster、Cloudflare Web Analytics（免费，不用 cookie）。
以下阈值是**建议初值，没有行业依据**，跑完试点后再调：
- **收录**：上线 2 周后，30 页里收录少于一半 → 先查技术问题和内容是否太薄，不加新页。
- **有曝光也有点击**（试点页大多有曝光，CTR 不明显低于同排名的常见水平）→ 放出 P2 的 200 页（每天约 10 页），并申请 AdSense。
- **曝光高、CTR 很低** → 认定被 AI 截流，转向修车费、对比、多配置差异等内容。
- **几乎没有曝光** → 查收录、canonical 和内链，不加页。

## 11. 90 天里程碑
- **第 0–2 周**：注册域名，查商标；补齐 15 款车的手册数据和症状页来源；30 页试点上线；GSC、Bing、IndexNow 配置好；做好 data-sources、作者、关于、隐私、联系页。
- **第 3–6 周**：每周复查 GSC，处理抢词；做 5–10 个目录提交和社区回答；按上一节规则做决定。
- **第 7–12 周**：如果决定放量，按每天约 10 页放出 P2，上线一个嵌入组件和一个数据资产页，申请 AdSense。Ezoic、Mediavine 等广告平台的流量门槛会变，**未核实**，申请前查官网。

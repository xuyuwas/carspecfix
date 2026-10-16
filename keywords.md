# carspecfix 关键词池（2026-10-15，零成本口径）

> 无搜索量。所有"量"均为 autosuggest 存在性证明或组合数，不是月搜。Google Trends（vs gpts）本轮 9 次批量全部 429 限流，**无趋势数据**。

## 文件
- keywords.csv：8,132 条真实 Google 自动补全词（美国、英文），一行一词，可直接贴 Semrush。已粗过滤非汽车噪音，仍有少量残留（如 Tacoma 城市、Accord 法律词）。
- suggest.json / suggest_ymm.json：原始补全；serp_lt.json：8 个长尾 SERP。

## 模板与组合规模（组合数，非搜索量）
| 模板 | 组合假设 | 组合数 | 补全验证 |
|---|---|---:|---|
| {year} {make} {model} {spec}（oil capacity/oil type/tire size/tire pressure/wiper size/battery size/fuse box/recalls/towing capacity/mpg） | 40 车型×15 年×10 属性 | 6,000 | 6 款测试车×10 属性：58/60 组合都有 10 条补全（只有 civic/camry towing 偏少） |
| {model} {symptom} / {year} {model} {symptom} | 40×30 症状 | 1,200（加年份×15 = 18,000） | 带年份很薄：grinding noise 0/6，shaking when braking 3/6，cranks but wont start 4/6 |
| {code} {make/model} | 50 码×20 品牌（+车型） | 1,000+ | p0420/p0300/p0171 补全满是 acura/acura mdx… ；2015 silverado p0420 有 10 条 |
| {part} replacement cost {make model} | 40 部件×40 车型 | 1,600 | "alternator replacement cost jeep wrangler" 等大量存在 |
| {symptom} cost to fix / {code} cost to fix | 30+50 | 80 | "cost to fix a cylinder misfire / coolant leak" 存在 |

## 需求表观排序（依据：补全密度+SERP，非量）
1. 年款规格（oil capacity/type、tire size/pressure、fuse box diagram、towing、mpg、recalls）— 每个组合都被补全，且自带配置细分（"2018 camry oil capacity v6"、"2019 cr v tire size 235 65r17 lx"、"2017 f150 towing capacity 3.5 ecoboost"）。
2. 部件更换费用 {part} replacement cost {make model}。
3. 故障码×品牌/车型。
4. 症状×车型（只到车型级；年款级基本无补全）。

## 长尾 SERP（Brave）
- 2020 rav4 oil capacity：amsoil、costaoils、**oilcapacitycheck.com（2026-01 注册）**、**oilcapacity411.com（2026-04 注册）**、rav4world、geargan(2023)、engineoiljournal(2024)、autopadre → 新站可进，且有人已在做同款程序化站。
- 2018 camry tire pressure：tirepressure.org(2020)、autozone、toyotanation、经销商站×3、reddit、tirepressures.co、repairpal。
- 2017 f150 fuse box diagram：startmycar×2、scribd、fuse-box.info、pinterest、f150forum、福特官方。
- 2015 silverado p0420：justanswer、论坛×4、autocodes×2、engine-codes、reddit — 论坛主导。
- f150 p0455：f150forum、justanswer、mechai.app(2024, AI 站)、ford-trucks、reddit×2、go-parts×2 — 论坛+AI 站。
- 2018 camry shakes when braking：reddit×2、repairpal、stackexchange、quora、经销商×2、toyotanation×2 — 全是论坛/UGC。
- 2016 honda civic battery size：autozone、reddit、firestone、walmart、oreilly、optima — 零售商主导。
- alternator replacement cost honda accord：repairpal×4、autozone、yourmechanic、reddit、justanswer — repairpal 垄断。

# carspecfix 关键词地图（2026-10-15）
脚本：kwmap.py（可重跑）。无搜索量：只有 Google 自动补全存在性 + 8 个 SERP 抽样；Trends 本轮未重试（之前 9 次全 429）。

## 清洗
原始 8,132 → 保留 4,232 个补全词（+163 个补的页面主词，标 source=seed）。
删除：无汽车意图 2,447；规格词没有车型 1,026；修车费非汽车（iPhone、房屋保险等）364；噪音词（for sale、dome、interior、release date、发电机/摩托型号等）56；归一化后重复 7。
归一化：f150/f 150→f-150，cr v→cr-v，chevy→chevrolet，wont/won't 统一。

## URL 结构：一个年款车型一页，页内分块
/specs/{make}/{model}/{year}/（机油、胎压、轮胎、保险丝、拖重、电瓶、雨刮、油耗、召回都在同一页的不同区块）
/specs/{make}/{model}/ 车型汇总页（接没有年份的词）；/symptoms/{slug}/；/codes/{p0xxx}/；/repair-cost/{part}/
理由：单个属性的词量很小，而且很多属于「AI 一句话就答完」的类型，拆成 10 页会变薄、互相抢词。合在一页就是「整车全表」，正好是 AI 给不全的东西。属性用锚点（#oil-capacity）承接。症状和故障码的「品牌/车型」变体先作为副词并入主页面，跑通后再拆。

## 统计（关键词数 / 页面数）


## 统计（关键词数 / 页面数）

| section            |   P1 |   P2 |   P3 |   All |
|:-------------------|-----:|-----:|-----:|------:|
| codes              | 1296 |    0 |    1 |  1297 |
| maintenance how-to |    8 |   65 |    0 |    73 |
| repair cost        |    0 |    0 |  180 |   180 |
| specs              |   90 |  596 |  450 |  1136 |
| symptoms           |  961 |  746 |    2 |  1709 |
| All                | 2355 | 1407 |  633 |  4395 |

| section            |   P1 |   P2 |   P3 |   All |
|:-------------------|-----:|-----:|-----:|------:|
| codes              |    7 |    0 |    1 |     8 |
| maintenance how-to |    0 |    1 |    0 |     1 |
| repair cost        |    0 |    0 |   23 |    23 |
| specs              |   15 |   21 |   91 |   127 |
| symptoms           |    8 |    7 |    1 |    16 |
| All                |   30 |   29 |  116 |   175 |

## P1 页面

| target_url                               | section   | primary_keyword               |   n_secondary | priority   |
|:-----------------------------------------|:----------|:------------------------------|--------------:|:-----------|
| /codes/p0420/                            | codes     | p0420 code                    |           291 | P1         |
| /codes/p0171/                            | codes     | p0171 code                    |           257 | P1         |
| /codes/p0300/                            | codes     | p0300 code                    |           255 | P1         |
| /codes/p0455/                            | codes     | p0455 code                    |           247 | P1         |
| /codes/p0442/                            | codes     | p0442 code                    |           238 | P1         |
| /symptoms/brakes-squeaking/              | symptoms  | brakes squeaking              |           231 | P1         |
| /symptoms/grinding-noise-when-braking/   | symptoms  | grinding noise when braking   |           162 | P1         |
| /symptoms/car-shaking-when-accelerating/ | symptoms  | car shaking when accelerating |           150 | P1         |
| /symptoms/car-shakes-when-braking/       | symptoms  | car shakes when braking       |           135 | P1         |
| /symptoms/car-jerks-when-accelerating/   | symptoms  | car jerks when accelerating   |           135 | P1         |
| /symptoms/car-cranks-but-wont-start/     | symptoms  | car cranks but wont start     |           130 | P1         |
| /specs/toyota/rav4/2020/                 | specs     | 2020 rav4 specs               |            83 | P1         |
| /symptoms/car-wont-start-clicking/       | symptoms  | car wont start clicking noise |            10 | P1         |
| /codes/p0456/                            | codes     | p0456 code                    |             1 | P1         |
| /specs/honda/cr-v/2024/                  | specs     | 2024 cr-v specs               |             0 | P1         |
| /specs/ford/f-150/2023/                  | specs     | 2023 f-150 specs              |             0 | P1         |
| /specs/honda/accord/2022/                | specs     | 2022 accord specs             |             0 | P1         |
| /specs/toyota/tacoma/2022/               | specs     | 2022 tacoma specs             |             0 | P1         |
| /specs/chevrolet/equinox/2022/           | specs     | 2022 equinox specs            |             0 | P1         |
| /specs/toyota/corolla/2022/              | specs     | 2022 corolla specs            |             0 | P1         |
| /specs/toyota/camry/2024/                | specs     | 2024 camry specs              |             0 | P1         |
| /specs/toyota/camry/2022/                | specs     | 2022 camry specs              |             0 | P1         |
| /specs/honda/cr-v/2022/                  | specs     | 2022 cr-v specs               |             0 | P1         |
| /specs/honda/civic/2022/                 | specs     | 2022 civic specs              |             0 | P1         |
| /specs/ford/f-150/2021/                  | specs     | 2021 f-150 specs              |             0 | P1         |
| /symptoms/abs-light-on/                  | symptoms  | abs light on                  |             0 | P1         |
| /specs/toyota/rav4/2024/                 | specs     | 2024 rav4 specs               |             0 | P1         |
| /specs/chevrolet/silverado-1500/2022/    | specs     | 2022 silverado 1500 specs     |             0 | P1         |
| /codes/p0301/                            | codes     | p0301 code                    |             0 | P1         |
| /specs/tesla/model-y/2023/               | specs     | 2023 model y specs            |             0 | P1         |

## P2 页面

| target_url                             | section            | primary_keyword                     |   n_secondary | priority   |
|:---------------------------------------|:-------------------|:------------------------------------|--------------:|:-----------|
| /symptoms/check-engine-light/          | symptoms           | check engine light                  |           249 | P2         |
| /symptoms/engine-ticking-noise/        | symptoms           | engine ticking noise                |           175 | P2         |
| /symptoms/burning-smell/               | symptoms           | burning smell                       |           138 | P2         |
| /symptoms/car-ac-not-blowing-cold/     | symptoms           | car ac not blowing cold             |           121 | P2         |
| /specs/ford/f-150/2017/                | specs              | 2017 ford f 150 specs               |            91 | P2         |
| /specs/toyota/camry/2018/              | specs              | 2018 toyota camry specs             |            87 | P2         |
| /specs/honda/civic/2016/               | specs              | 2016 honda civic specs              |            83 | P2         |
| /specs/honda/cr-v/2019/                | specs              | 2019 honda cr v specs               |            77 | P2         |
| /specs/chevrolet/silverado-1500/2015/  | specs              | 2015 chevrolet silverado 1500 specs |            75 | P2         |
| /symptoms/tire-pressure-light/         | symptoms           | tire pressure light                 |            42 | P2         |
| /specs/toyota/rav4/                    | specs              | toyota rav4 specs                   |            31 | P2         |
| /specs/ford/f-150/                     | maintenance how-to | ford f 150 specs                    |            24 | P2         |
| /specs/toyota/camry/                   | specs              | toyota camry specs                  |            23 | P2         |
| /specs/tesla/model-y/                  | specs              | tesla model y specs                 |            21 | P2         |
| /specs/honda/hr-v/2019/                | specs              | 2019 honda hr v specs               |            16 | P2         |
| /specs/toyota/corolla/                 | specs              | toyota corolla specs                |            16 | P2         |
| /specs/chevrolet/silverado-1500/       | specs              | chevrolet silverado 1500 specs      |            15 | P2         |
| /specs/toyota/tacoma/                  | specs              | toyota tacoma specs                 |            14 | P2         |
| /specs/honda/accord/                   | specs              | honda accord specs                  |            13 | P2         |
| /specs/ram/ram-1500/                   | specs              | ram ram 1500 specs                  |            11 | P2         |
| /specs/honda/civic/                    | specs              | honda civic specs                   |            10 | P2         |
| /specs/honda/cr-v/                     | specs              | honda cr v specs                    |            10 | P2         |
| /specs/jeep/wrangler/                  | specs              | jeep wrangler specs                 |             9 | P2         |
| /symptoms/car-vibration-at-high-speed/ | symptoms           | car vibration at high speed         |             8 | P2         |
| /specs/chevrolet/silverado-1500/2014/  | specs              | 2014 chevrolet silverado 1500 specs |             6 | P2         |
| /symptoms/car-wont-start/              | symptoms           | car wont start                      |             6 | P2         |
| /specs/chevrolet/silverado-1500/2018/  | specs              | 2018 chevrolet silverado 1500 specs |             3 | P2         |
| /specs/hyundai/elantra/2013/           | specs              | 2013 hyundai elantra specs          |             2 | P2         |
| /specs/toyota/rav4/2019/               | specs              | 2019 toyota rav4 specs              |             2 | P2         |

## 注意事项
- P2 只有 29 页，不到 200：词池按 6 款测试车加少量车型拉的，补全只覆盖这些车。要凑到 200 页，得按「40 车型 × 近 10 年」再拉一轮补全，用同样的规则归类。
- 优先级依据：P1 = 已定的 30 页试水；P2 = 补全词 ≥3 的 2012 年以后年款页、补全词 ≥10 的车型汇总页、补全词 ≥5 的症状和故障码页；P3 = 修车费（RepairPal 垄断）、品牌汇总页、补全很薄的页。
- 11 页 P1 规格页（2022/2023/2024 年款）在词池里一个补全词都没有，主词是补的。原因是词池拉的是 2015–2020 年款，不代表这些年款没人搜。
- 分类是规则匹配，大约有几个百分点的错分，主要是症状页里混进了非汽车或摩托车的副词。上线前人工扫一遍 P1 和 P2 的副词。
- 规格词剔除了引擎/设备型号（gx270、d13），品牌汇总页里还可能有残留。

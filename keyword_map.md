# carspecfix 关键词地图（2026-10-15）
脚本：kwmap.py（可重跑）。无搜索量：只有 Google 自动补全存在性 + 8 个 SERP 抽样；Trends 本轮未重试（之前 9 次全 429）。

## 清洗（第二轮扩词后）
原始 54,403（第一轮 8,132 + 新补全 46,810，合并去重；新补全来自 5,625 次查询：45 车型×2015–2025×10 属性 + 45 车型×15 症状/故障码，限速 4 线程、每次间隔 0.4–0.9 秒，0 次被封，其中 199 次查询没有返回联想词）→ 保留 47,705 个补全词 + 756 个补的主词。
删除：无汽车意图 4,459；规格词没写车型 1,460；噪音 391；修车费非汽车 364；重复 24。

## URL 结构：一个年款车型一页，页内分块
/specs/{make}/{model}/{year}/（机油、胎压、轮胎、保险丝、拖重、电瓶、雨刮、油耗、召回都在同一页的不同区块）
/specs/{make}/{model}/ 车型汇总页（接没有年份的词）；/symptoms/{slug}/；/codes/{p0xxx}/；/repair-cost/{part}/
理由：单个属性的词量很小，而且很多属于「AI 一句话就答完」的类型，拆成 10 页会变薄、互相抢词。合在一页就是「整车全表」，正好是 AI 给不全的东西。属性用锚点（#oil-capacity）承接。症状和故障码的「品牌/车型」变体先作为副词并入主页面，跑通后再拆。

## 统计（关键词数 / 页面数）

| section            |   P1 |    P2 |    P3 |   All |
|:-------------------|-----:|------:|------:|------:|
| codes              | 3427 |     0 |    15 |  3442 |
| maintenance how-to |  117 |  1563 |  1658 |  3338 |
| repair cost        |    0 |     0 |   533 |   533 |
| specs              | 1153 | 16181 | 18187 | 35521 |
| symptoms           | 2438 |  3156 |    33 |  5627 |
| All                | 7135 | 20900 | 20426 | 48461 |

| section            |   P1 |   P2 |   P3 |   All |
|:-------------------|-----:|-----:|-----:|------:|
| codes              |    7 |    0 |    3 |    10 |
| maintenance how-to |    0 |    2 |   21 |    23 |
| repair cost        |    0 |    0 |   25 |    25 |
| specs              |   15 |  193 |  498 |   706 |
| symptoms           |    8 |    5 |    3 |    16 |
| All                |   30 |  200 |  550 |   780 |

## P1 页面

| target_url                               | section   | primary_keyword               |   n_secondary | priority   |
|:-----------------------------------------|:----------|:------------------------------|--------------:|:-----------|
| /codes/p0420/                            | codes     | p0420 code                    |           669 | P1         |
| /codes/p0171/                            | codes     | p0171 code                    |           648 | P1         |
| /codes/p0300/                            | codes     | p0300 code                    |           634 | P1         |
| /codes/p0455/                            | codes     | p0455 code                    |           606 | P1         |
| /symptoms/car-shaking-when-accelerating/ | symptoms  | car shaking when accelerating |           544 | P1         |
| /codes/p0442/                            | codes     | p0442 code                    |           530 | P1         |
| /symptoms/car-cranks-but-wont-start/     | symptoms  | car cranks but wont start     |           492 | P1         |
| /symptoms/brakes-squeaking/              | symptoms  | brakes squeaking              |           424 | P1         |
| /symptoms/car-jerks-when-accelerating/   | symptoms  | car jerks when accelerating   |           419 | P1         |
| /codes/p0456/                            | codes     | p0456 code                    |           333 | P1         |
| /symptoms/car-shakes-when-braking/       | symptoms  | car shakes when braking       |           320 | P1         |
| /symptoms/grinding-noise-when-braking/   | symptoms  | grinding noise when braking   |           204 | P1         |
| /specs/toyota/tacoma/2022/               | specs     | 2022 tacoma specs             |            95 | P1         |
| /specs/chevrolet/silverado-1500/2022/    | specs     | 2022 silverado 1500 specs     |            93 | P1         |
| /specs/ford/f-150/2023/                  | specs     | 2023 f-150 specs              |            92 | P1         |
| /specs/ford/f-150/2021/                  | specs     | 2021 f-150 specs              |            90 | P1         |
| /specs/toyota/corolla/2022/              | specs     | 2022 corolla specs            |            90 | P1         |
| /specs/toyota/rav4/2024/                 | specs     | 2024 rav4 specs               |            90 | P1         |
| /specs/honda/civic/2022/                 | specs     | 2022 civic specs              |            88 | P1         |
| /specs/honda/accord/2022/                | specs     | 2022 accord specs             |            87 | P1         |
| /specs/toyota/rav4/2020/                 | specs     | 2020 rav4 specs               |            86 | P1         |
| /specs/toyota/camry/2022/                | specs     | 2022 toyota camry specs       |            84 | P1         |
| /specs/toyota/camry/2024/                | specs     | 2024 camry specs              |            84 | P1         |
| /specs/chevrolet/equinox/2022/           | specs     | 2022 equinox specs            |            83 | P1         |
| /specs/honda/cr-v/2024/                  | specs     | 2024 cr-v specs               |            73 | P1         |
| /specs/honda/cr-v/2022/                  | specs     | 2022 cr-v specs               |            70 | P1         |
| /specs/tesla/model-y/2023/               | specs     | 2023 model y specs            |            50 | P1         |
| /symptoms/car-wont-start-clicking/       | symptoms  | car wont start clicking noise |            27 | P1         |
| /symptoms/abs-light-on/                  | symptoms  | abs light on                  |             0 | P1         |
| /codes/p0301/                            | codes     | p0301 code                    |             0 | P1         |

## P2 页面

| target_url                            | section            | primary_keyword                     |   n_secondary | priority   |
|:--------------------------------------|:-------------------|:------------------------------------|--------------:|:-----------|
| /symptoms/tire-pressure-light/        | symptoms           | tire pressure light                 |          1467 | P2         |
| /symptoms/check-engine-light/         | symptoms           | check engine light                  |           662 | P2         |
| /symptoms/car-ac-not-blowing-cold/    | symptoms           | car ac not blowing cold             |           549 | P2         |
| /symptoms/engine-ticking-noise/       | symptoms           | engine ticking noise                |           335 | P2         |
| /specs/honda/civic/2016/              | specs              | 2016 honda civic specs              |           154 | P2         |
| /symptoms/burning-smell/              | symptoms           | burning smell                       |           138 | P2         |
| /specs/honda/cr-v/2019/               | specs              | 2019 honda cr v specs               |           118 | P2         |
| /specs/ford/explorer/2020/            | specs              | 2020 ford explorer specs            |           100 | P2         |
| /specs/gmc/sierra/2024/               | specs              | 2024 gmc sierra specs               |            99 | P2         |
| /specs/ford/ranger/2021/              | specs              | 2021 ford ranger specs              |            98 | P2         |
| /specs/gmc/sierra/2022/               | specs              | 2022 gmc sierra specs               |            98 | P2         |
| /specs/ford/ranger/2024/              | specs              | 2024 ford ranger specs              |            98 | P2         |
| /specs/gmc/sierra/2025/               | specs              | 2025 gmc sierra specs               |            98 | P2         |
| /specs/ford/edge/2020/                | specs              | 2020 ford edge specs                |            97 | P2         |
| /specs/ford/ranger/2020/              | specs              | 2020 ford ranger specs              |            97 | P2         |
| /specs/chevrolet/silverado-1500/2021/ | specs              | 2021 chevrolet silverado 1500 specs |            97 | P2         |
| /specs/nissan/rogue/2021/             | specs              | 2021 nissan rogue specs             |            97 | P2         |
| /specs/gmc/sierra/2023/               | specs              | 2023 gmc sierra specs               |            97 | P2         |
| /specs/kia/sportage/2023/             | specs              | 2023 kia sportage specs             |            97 | P2         |
| /specs/ford/ranger/2019/              | specs              | 2019 ford ranger specs              |            96 | P2         |
| /specs/chevrolet/equinox/2020/        | specs              | 2020 chevrolet equinox specs        |            96 | P2         |
| /specs/nissan/rogue/2023/             | specs              | 2023 nissan rogue specs             |            96 | P2         |
| /specs/honda/odyssey/2016/            | specs              | 2016 honda odyssey specs            |            95 | P2         |
| /specs/gmc/sierra/2018/               | specs              | 2018 gmc sierra specs               |            95 | P2         |
| /specs/gmc/sierra/2021/               | specs              | 2021 gmc sierra specs               |            95 | P2         |
| /specs/chevrolet/silverado-1500/2024/ | specs              | 2024 chevrolet silverado 1500 specs |            95 | P2         |
| /specs/nissan/rogue/2015/             | specs              | 2015 nissan rogue specs             |            94 | P2         |
| /specs/ford/explorer/2017/            | specs              | 2017 ford explorer specs            |            94 | P2         |
| /specs/nissan/rogue/2017/             | specs              | 2017 nissan rogue specs             |            94 | P2         |
| /specs/toyota/tacoma/2019/            | specs              | 2019 toyota tacoma specs            |            94 | P2         |
| /specs/gmc/sierra/2020/               | specs              | 2020 gmc sierra specs               |            94 | P2         |
| /specs/chevrolet/silverado-1500/2020/ | specs              | 2020 chevrolet silverado 1500 specs |            94 | P2         |
| /specs/toyota/tacoma/2023/            | specs              | 2023 toyota tacoma specs            |            94 | P2         |
| /specs/toyota/corolla/2024/           | specs              | 2024 toyota corolla specs           |            94 | P2         |
| /specs/toyota/highlander/2024/        | maintenance how-to | 2024 toyota highlander specs        |            94 | P2         |
| /specs/toyota/corolla/2025/           | maintenance how-to | 2025 toyota corolla specs           |            94 | P2         |
| /specs/ford/escape/2016/              | specs              | 2016 ford escape specs              |            93 | P2         |
| /specs/chevrolet/equinox/2018/        | specs              | 2018 chevrolet equinox specs        |            93 | P2         |
| /specs/nissan/rogue/2018/             | specs              | 2018 nissan rogue specs             |            93 | P2         |
| /specs/chevrolet/silverado-1500/2019/ | specs              | 2019 chevrolet silverado 1500 specs |            93 | P2         |
| /specs/toyota/highlander/2019/        | specs              | 2019 toyota highlander specs        |            93 | P2         |
| /specs/nissan/rogue/2020/             | specs              | 2020 nissan rogue specs             |            93 | P2         |
| /specs/subaru/crosstrek/2021/         | specs              | 2021 subaru crosstrek specs         |            93 | P2         |
| /specs/toyota/tacoma/2021/            | specs              | 2021 toyota tacoma specs            |            93 | P2         |
| /specs/ford/escape/2022/              | specs              | 2022 ford escape specs              |            93 | P2         |
| /specs/subaru/crosstrek/2024/         | specs              | 2024 subaru crosstrek specs         |            93 | P2         |
| /specs/toyota/rav4/2025/              | specs              | 2025 toyota rav4 specs              |            93 | P2         |
| /specs/ford/edge/2015/                | specs              | 2015 ford edge specs                |            92 | P2         |
| /specs/ford/explorer/2016/            | specs              | 2016 ford explorer specs            |            92 | P2         |
| /specs/chevrolet/equinox/2019/        | specs              | 2019 chevrolet equinox specs        |            92 | P2         |
| /specs/ford/edge/2019/                | specs              | 2019 ford edge specs                |            92 | P2         |
| /specs/ford/escape/2019/              | specs              | 2019 ford escape specs              |            92 | P2         |
| /specs/nissan/rogue/2019/             | specs              | 2019 nissan rogue specs             |            92 | P2         |
| /specs/honda/civic/2020/              | specs              | 2020 honda civic specs              |            92 | P2         |
| /specs/ford/escape/2020/              | specs              | 2020 ford escape specs              |            92 | P2         |
| /specs/toyota/tacoma/2020/            | specs              | 2020 toyota tacoma specs            |            92 | P2         |
| /specs/ford/escape/2021/              | specs              | 2021 ford escape specs              |            92 | P2         |
| /specs/toyota/corolla/2023/           | specs              | 2023 toyota corolla specs           |            92 | P2         |
| /specs/ford/escape/2024/              | specs              | 2024 ford escape specs              |            92 | P2         |
| /specs/ford/f-150/2024/               | specs              | 2024 ford f 150 specs               |            92 | P2         |
| /specs/honda/civic/2025/              | specs              | 2025 honda civic specs              |            92 | P2         |
| /specs/ford/ranger/2025/              | specs              | 2025 ford ranger specs              |            92 | P2         |
| /specs/ford/escape/2015/              | specs              | 2015 ford escape specs              |            91 | P2         |
| /specs/nissan/rogue/2016/             | specs              | 2016 nissan rogue specs             |            91 | P2         |
| /specs/ford/escape/2017/              | specs              | 2017 ford escape specs              |            91 | P2         |
| /specs/ford/f-150/2017/               | specs              | 2017 ford f 150 specs               |            91 | P2         |
| /specs/chevrolet/silverado-1500/2018/ | specs              | 2018 chevrolet silverado 1500 specs |            91 | P2         |
| /specs/ford/edge/2018/                | specs              | 2018 ford edge specs                |            91 | P2         |
| /specs/hyundai/elantra/2018/          | specs              | 2018 hyundai elantra specs          |            91 | P2         |
| /specs/ford/escape/2018/              | specs              | 2018 ford escape specs              |            91 | P2         |
| /specs/subaru/outback/2018/           | specs              | 2018 subaru outback specs           |            91 | P2         |
| /specs/ford/bronco/2021/              | specs              | 2021 ford bronco specs              |            91 | P2         |
| /specs/ford/explorer/2021/            | specs              | 2021 ford explorer specs            |            91 | P2         |
| /specs/ford/ranger/2022/              | specs              | 2022 ford ranger specs              |            91 | P2         |
| /specs/nissan/rogue/2022/             | specs              | 2022 nissan rogue specs             |            91 | P2         |
| /specs/hyundai/elantra/2023/          | specs              | 2023 hyundai elantra specs          |            91 | P2         |
| /specs/toyota/highlander/2023/        | specs              | 2023 toyota highlander specs        |            91 | P2         |
| /specs/kia/sportage/2024/             | specs              | 2024 kia sportage specs             |            91 | P2         |
| /specs/chevrolet/equinox/2025/        | specs              | 2025 chevrolet equinox specs        |            91 | P2         |
| /specs/ford/explorer/2015/            | specs              | 2015 ford explorer specs            |            90 | P2         |
| /specs/ford/f-150/2016/               | specs              | 2016 ford f 150 specs               |            90 | P2         |
| /specs/honda/accord/2017/             | specs              | 2017 honda accord specs             |            90 | P2         |
| /specs/ford/edge/2017/                | specs              | 2017 ford edge specs                |            90 | P2         |
| /specs/kia/sportage/2017/             | specs              | 2017 kia sportage specs             |            90 | P2         |
| /specs/ford/explorer/2018/            | specs              | 2018 ford explorer specs            |            90 | P2         |
| /specs/ford/f-150/2019/               | specs              | 2019 ford f 150 specs               |            90 | P2         |
| /specs/honda/pilot/2019/              | specs              | 2019 honda pilot specs              |            90 | P2         |
| /specs/ford/f-150/2020/               | specs              | 2020 ford f 150 specs               |            90 | P2         |
| /specs/subaru/forester/2020/          | specs              | 2020 subaru forester specs          |            90 | P2         |
| /specs/toyota/highlander/2021/        | specs              | 2021 toyota highlander specs        |            90 | P2         |
| /specs/honda/pilot/2021/              | specs              | 2021 honda pilot specs              |            90 | P2         |
| /specs/jeep/wrangler/2021/            | specs              | 2021 jeep wrangler specs            |            90 | P2         |
| /specs/subaru/outback/2021/           | specs              | 2021 subaru outback specs           |            90 | P2         |
| /specs/ford/explorer/2022/            | specs              | 2022 ford explorer specs            |            90 | P2         |
| /specs/ford/f-150/2022/               | specs              | 2022 ford f 150 specs               |            90 | P2         |
| /specs/toyota/highlander/2022/        | specs              | 2022 toyota highlander specs        |            90 | P2         |
| /specs/ford/explorer/2023/            | specs              | 2023 ford explorer specs            |            90 | P2         |
| /specs/toyota/tundra/2023/            | specs              | 2023 toyota tundra specs            |            90 | P2         |
| /specs/hyundai/tucson/2024/           | specs              | 2024 hyundai tucson specs           |            90 | P2         |
| /specs/ford/edge/2016/                | specs              | 2016 ford edge specs                |            89 | P2         |
| /specs/hyundai/elantra/2016/          | specs              | 2016 hyundai elantra specs          |            89 | P2         |
| /specs/ford/f-150/2018/               | specs              | 2018 ford f 150 specs               |            89 | P2         |
| /specs/toyota/highlander/2018/        | specs              | 2018 toyota highlander specs        |            89 | P2         |
| /specs/ford/fusion/2020/              | specs              | 2020 ford fusion specs              |            89 | P2         |
| /specs/kia/sportage/2020/             | specs              | 2020 kia sportage specs             |            89 | P2         |
| /specs/ford/bronco/2022/              | specs              | 2022 ford bronco specs              |            89 | P2         |
| /specs/toyota/rav4/2023/              | specs              | 2023 toyota rav4 specs              |            89 | P2         |
| /specs/honda/civic/2024/              | specs              | 2024 honda civic specs              |            89 | P2         |
| /specs/toyota/tundra/2024/            | specs              | 2024 toyota tundra specs            |            89 | P2         |
| /specs/ford/escape/2025/              | specs              | 2025 ford escape specs              |            89 | P2         |
| /specs/ford/explorer/2025/            | specs              | 2025 ford explorer specs            |            89 | P2         |
| /specs/ford/f-150/2025/               | specs              | 2025 ford f 150 specs               |            89 | P2         |
| /specs/honda/accord/2015/             | specs              | 2015 honda accord specs             |            88 | P2         |
| /specs/chevrolet/tahoe/2015/          | specs              | 2015 chevrolet tahoe specs          |            88 | P2         |
| /specs/chevrolet/silverado-1500/2015/ | specs              | 2015 chevrolet silverado 1500 specs |            88 | P2         |
| /specs/ford/f-150/2015/               | specs              | 2015 ford f 150 specs               |            88 | P2         |
| /specs/honda/accord/2016/             | specs              | 2016 honda accord specs             |            88 | P2         |
| /specs/honda/pilot/2016/              | specs              | 2016 honda pilot specs              |            88 | P2         |
| /specs/honda/pilot/2017/              | specs              | 2017 honda pilot specs              |            88 | P2         |
| /specs/honda/accord/2018/             | specs              | 2018 honda accord specs             |            88 | P2         |
| /specs/toyota/camry/2018/             | specs              | 2018 toyota camry specs             |            88 | P2         |
| /specs/jeep/wrangler/2018/            | specs              | 2018 jeep wrangler specs            |            88 | P2         |
| /specs/gmc/sierra/2019/               | specs              | 2019 gmc sierra specs               |            88 | P2         |
| /specs/chevrolet/traverse/2020/       | specs              | 2020 chevrolet traverse specs       |            88 | P2         |
| /specs/toyota/corolla/2020/           | specs              | 2020 toyota corolla specs           |            88 | P2         |
| /specs/hyundai/elantra/2020/          | specs              | 2020 hyundai elantra specs          |            88 | P2         |
| /specs/jeep/wrangler/2020/            | specs              | 2020 jeep wrangler specs            |            88 | P2         |
| /specs/subaru/outback/2020/           | specs              | 2020 subaru outback specs           |            88 | P2         |
| /specs/chevrolet/tahoe/2021/          | specs              | 2021 chevrolet tahoe specs          |            88 | P2         |
| /specs/honda/civic/2021/              | specs              | 2021 honda civic specs              |            88 | P2         |
| /specs/hyundai/tucson/2022/           | specs              | 2022 hyundai tucson specs           |            88 | P2         |
| /specs/subaru/outback/2022/           | specs              | 2022 subaru outback specs           |            88 | P2         |
| /specs/ford/bronco/2023/              | specs              | 2023 ford bronco specs              |            88 | P2         |
| /specs/ford/ranger/2023/              | specs              | 2023 ford ranger specs              |            88 | P2         |
| /specs/toyota/tacoma/2024/            | specs              | 2024 toyota tacoma specs            |            88 | P2         |
| /specs/kia/sportage/2025/             | specs              | 2025 kia sportage specs             |            88 | P2         |
| /specs/toyota/tacoma/2025/            | specs              | 2025 toyota tacoma specs            |            88 | P2         |
| /specs/jeep/wrangler/2016/            | specs              | 2016 jeep wrangler specs            |            87 | P2         |
| /specs/nissan/altima/2016/            | specs              | 2016 nissan altima specs            |            87 | P2         |
| /specs/subaru/outback/2016/           | specs              | 2016 subaru outback specs           |            87 | P2         |
| /specs/ford/explorer/2019/            | specs              | 2019 ford explorer specs            |            87 | P2         |
| /specs/honda/odyssey/2019/            | specs              | 2019 honda odyssey specs            |            87 | P2         |
| /specs/toyota/camry/2020/             | specs              | 2020 toyota camry specs             |            87 | P2         |
| /specs/toyota/camry/2021/             | specs              | 2021 toyota camry specs             |            87 | P2         |
| /specs/toyota/rav4/2022/              | specs              | 2022 toyota rav4 specs              |            87 | P2         |
| /specs/toyota/camry/2023/             | specs              | 2023 toyota camry specs             |            87 | P2         |
| /specs/chevrolet/tahoe/2023/          | specs              | 2023 chevrolet tahoe specs          |            87 | P2         |
| /specs/honda/civic/2023/              | specs              | 2023 honda civic specs              |            87 | P2         |
| /specs/ford/escape/2023/              | specs              | 2023 ford escape specs              |            87 | P2         |
| /specs/nissan/rogue/2024/             | specs              | 2024 nissan rogue specs             |            87 | P2         |
| /specs/chevrolet/silverado-1500/2025/ | specs              | 2025 chevrolet silverado 1500 specs |            87 | P2         |
| /specs/chevrolet/malibu/2016/         | specs              | 2016 chevrolet malibu specs         |            86 | P2         |
| /specs/chevrolet/colorado/2016/       | specs              | 2016 chevrolet colorado specs       |            86 | P2         |
| /specs/chevrolet/silverado-1500/2016/ | specs              | 2016 chevrolet silverado 1500 specs |            86 | P2         |
| /specs/chevrolet/equinox/2017/        | specs              | 2017 chevrolet equinox specs        |            86 | P2         |
| /specs/honda/civic/2018/              | specs              | 2018 honda civic specs              |            86 | P2         |
| /specs/subaru/forester/2018/          | specs              | 2018 subaru forester specs          |            86 | P2         |
| /specs/toyota/tundra/2018/            | specs              | 2018 toyota tundra specs            |            86 | P2         |
| /specs/toyota/camry/2019/             | specs              | 2019 toyota camry specs             |            86 | P2         |
| /specs/honda/civic/2019/              | specs              | 2019 honda civic specs              |            86 | P2         |
| /specs/hyundai/elantra/2019/          | specs              | 2019 hyundai elantra specs          |            86 | P2         |
| /specs/honda/accord/2020/             | specs              | 2020 honda accord specs             |            86 | P2         |
| /specs/toyota/corolla/2021/           | specs              | 2021 toyota corolla specs           |            86 | P2         |
| /specs/jeep/wrangler/2022/            | specs              | 2022 jeep wrangler specs            |            86 | P2         |
| /specs/ford/edge/2024/                | specs              | 2024 ford edge specs                |            86 | P2         |
| /specs/jeep/wrangler/2024/            | specs              | 2024 jeep wrangler specs            |            86 | P2         |
| /specs/subaru/outback/2024/           | specs              | 2024 subaru outback specs           |            86 | P2         |
| /specs/toyota/camry/2025/             | specs              | 2025 toyota camry specs             |            86 | P2         |
| /specs/hyundai/tucson/2025/           | specs              | 2025 hyundai tucson specs           |            86 | P2         |
| /specs/honda/civic/2015/              | specs              | 2015 honda civic specs              |            85 | P2         |
| /specs/ford/fusion/2015/              | specs              | 2015 ford fusion specs              |            85 | P2         |
| /specs/jeep/grand-cherokee/2015/      | specs              | 2015 jeep grand cherokee specs      |            85 | P2         |
| /specs/jeep/wrangler/2015/            | specs              | 2015 jeep wrangler specs            |            85 | P2         |
| /specs/chevrolet/equinox/2016/        | specs              | 2016 chevrolet equinox specs        |            85 | P2         |
| /specs/honda/civic/2017/              | specs              | 2017 honda civic specs              |            85 | P2         |
| /specs/toyota/highlander/2017/        | specs              | 2017 toyota highlander specs        |            85 | P2         |
| /specs/subaru/outback/2017/           | specs              | 2017 subaru outback specs           |            85 | P2         |
| /specs/honda/pilot/2018/              | specs              | 2018 honda pilot specs              |            85 | P2         |
| /specs/hyundai/tucson/2018/           | specs              | 2018 hyundai tucson specs           |            85 | P2         |
| /specs/toyota/tacoma/2018/            | specs              | 2018 toyota tacoma specs            |            85 | P2         |
| /specs/subaru/crosstrek/2019/         | specs              | 2019 subaru crosstrek specs         |            85 | P2         |
| /specs/toyota/4runner/2020/           | specs              | 2020 toyota 4runner specs           |            85 | P2         |
| /specs/honda/accord/2021/             | specs              | 2021 honda accord specs             |            85 | P2         |
| /specs/honda/pilot/2022/              | specs              | 2022 honda pilot specs              |            85 | P2         |
| /specs/chevrolet/silverado-1500/2023/ | specs              | 2023 chevrolet silverado 1500 specs |            85 | P2         |
| /specs/jeep/wrangler/2023/            | specs              | 2023 jeep wrangler specs            |            85 | P2         |
| /specs/subaru/outback/2023/           | specs              | 2023 subaru outback specs           |            85 | P2         |
| /specs/toyota/tundra/2025/            | specs              | 2025 toyota tundra specs            |            85 | P2         |
| /specs/chevrolet/tahoe/2016/          | specs              | 2016 chevrolet tahoe specs          |            84 | P2         |
| /specs/ford/fusion/2016/              | specs              | 2016 ford fusion specs              |            84 | P2         |
| /specs/ford/mustang/2016/             | specs              | 2016 ford mustang specs             |            84 | P2         |
| /specs/chevrolet/silverado-1500/2017/ | specs              | 2017 chevrolet silverado 1500 specs |            84 | P2         |
| /specs/toyota/rav4/2018/              | specs              | 2018 toyota rav4 specs              |            84 | P2         |
| /specs/honda/accord/2019/             | specs              | 2019 honda accord specs             |            84 | P2         |
| /specs/toyota/rav4/2019/              | specs              | 2019 toyota rav4 specs              |            84 | P2         |
| /specs/toyota/highlander/2020/        | specs              | 2020 toyota highlander specs        |            84 | P2         |
| /specs/honda/pilot/2020/              | specs              | 2020 honda pilot specs              |            84 | P2         |
| /specs/toyota/tundra/2020/            | specs              | 2020 toyota tundra specs            |            84 | P2         |
| /specs/toyota/rav4/2021/              | specs              | 2021 toyota rav4 specs              |            84 | P2         |
| /specs/subaru/forester/2022/          | specs              | 2022 subaru forester specs          |            84 | P2         |

## 注意事项
- 仍然没有搜索量。补全词的多少只说明有人这么搜，不代表量大。P2 内部的排序基本就是补全条数（规格页大多在 84–154 条之间，彼此差距很小）。
- P2 的 200 页里 193 页是年款规格页。故障码没有 P2：码页的副词都已经并进 P1 的 7 个故障码页。
- 2025 年款和部分 2015 年款的补全较薄，部分车型的拖重、电瓶这类属性补全很少。
- 分类按规则匹配，有少量错分；tire pressure light 页吸收了 1,467 个「年款+车型+胎压灯/重置」类的词，后续可能要拆成车型页的一个区块。
- maintenance how-to 里很多是「年款+车型+重置/更换」类，已经并到对应的年款规格页。

# carspecfix.com SEO 开发需求（给小码）v2

> v2（2026-10-15）按队长最高原则（对车主有用、数据有官方出处并经小数签字、不做没有独特价值的模板页）修订，并与 `user-needs.md` 对齐。标 **[v2]** 的是新增或修改的条目。

> 来自 `seo-plan-final.md`。每条都写了验收方式，技术实现由小码定。优先级：**P0 = 试点上线前必须完成**，P1 = 试点期内完成，P2 = 第二批前完成。

## A. URL 与路由
- **R-U1 (P0)** 路由：`/`、`/specs/{make}/{model}/{year}/`、`/specs/{make}/{model}/`（按 R-U6 的条件生成）、`/symptoms/{slug}/`、`/codes/{code}/`、`/symptoms/`、`/codes/`、`/about/`、`/sources/`、`/authors/{slug}/`、`/contact/`、`/privacy/`。
  验收：已上线页面的 URL 都在 `pages.csv` 的 `target_url` 里（脚本比对 0 差异）。**[v2] 不要求 30 页全部上线，以签字进度为准。**
- **R-U2 (P0) [v2]** 全部小写、连字符、以 `/` 结尾。不带斜杠、大写、`www`、`http` 的版本一次 301 到规范 URL（不允许 302、不允许跳转链 >1 跳）。**用 Cloudflare 跳转规则实现**（不在应用层多跳）；有 Cloudflare 账号后上线前实测。
  验收（上线前，Cloudflare 配好后）：`curl -I` 抽测 `http://www.carspecfix.com/Specs/Toyota/RAV4/2020` → 一跳 301 到 `https://carspecfix.com/specs/toyota/rav4/2020/`。
- **R-U3 (P0)** 不存在的 URL 返回真 404 状态码（不是 200 的“软 404”），有自定义 404 页带首页和搜索入口。
- **R-U4 (P0)** 试点期不生成品牌页 `/specs/{make}/`；访问返回 404（或 301 到首页的品牌区域，二选一，写进技术方案）。面包屑不得链接到不存在的页面。
- **R-U6 (P0) [v2]** 车型汇总页 `/specs/{make}/{model}/`：同一车型至少有 2 个**已上线**的年款才生成，**这条不放宽**。页面内容：已上线年款的列表，加上各年款之间关键规格的差异（只用已签字的数据，没有差异数据就不显示这一块）。未上线的年款不加链接。
  验收：构建报告列出每个车型的已上线年款数，<2 的车型没有汇总页，访问返回 404；汇总页里没有指向未上线页面的链接。
- **R-U5 (P0)** URL 参数（如 `?ref=`、`?utm_`）的页面 canonical 指向无参数版本。

## B. 收录控制与质量闸门
- **R-Q1 (P0) [v2]** 发布条件 = 小数签字（`reviewed_by / reviewed_at / signoff=yes`），并且满足最低内容要求：
  - 年款页：至少有机油（容量+粘度）或 1 行完整轮胎数据（尺寸 + 前/后胎压），都来自 A 级来源，且这个年款能被手册证明；
  - 电车（Model Y）：轮胎 + 召回（字段待小站/小数确认）；
  - 症状页、故障码页：“能不能开 / 严重程度”有出处，且至少 1 个有出处的原因。
  **不满足的页面不生成、不上线、不进 sitemap，也不被任何页面链接。不使用“先上线再 noindex”的做法。** 单个字段缺 A 级来源时，只隐藏这个字段（见 R-Q3），页面其他已签字的部分照常上线。
  验收：构建报告列出每页“已发布 / 未发布 + 原因”；`dist/` 里没有未签字的页面；全站不出现 `noindex`（404 页除外）。
- **R-Q2 (P1)** 构建时计算同模板页面两两正文相似度（去掉导航、页脚、模板固定文字），>80% 的页面对输出警告（[经验值]）。警告页由小数或小站决定是补内容还是不上线。验收：报告文件存在，已上线页面没有警告，或已人工确认。
- **R-Q3 (P0)** 任何 `TODO` 值不得渲染到 HTML、title、meta、schema 中；缺值显示 “Not yet verified — check your owner's manual”，整块无数据则隐藏整个模块（含 H2）。
  验收：构建后 `grep -ri "todo" dist/` 为 0。
- **R-Q4 (P0) [v2]** 签一页放一页：签字后下一次构建就上线，**每天最多 10 页**，超出的顺延到第二天；没有“凑批次”的逻辑。未发布页面不生成、不进 sitemap、不被链接。验收：发布日志里每天的新页 ≤10，每页都有对应的签字记录。

## C. Canonical、meta 与模板
- **R-M1 (P0)** 每个可收录页有自引用绝对 canonical（`https://carspecfix.com/.../`）。
- **R-M2 (P0) [v2]** Title、H1、Meta 按 `seo-plan-final.md` 第 4 节的模板生成，**Title ≤ 60 字符**（按解码后的可见字符计）。超长时按顺序降级：先去掉 `| CarSpecFix`，再去掉末尾的模块词；不用省略号截断。Title 和 Meta 只能写页面上真有、已签字的模块和数值（比如没有召回数据，Title 里就不写 Recalls）；Meta 缺值的片段整段删掉。
  - 首页 Title：`Car Specs by Year, Make & Model: Oil, Tires, Recalls`（52 字符）
  - `/codes/` Title：`OBD-II Codes: Meaning & Can You Still Drive? | CarSpecFix`（57 字符）
  - 年款页：`{Year} {Make} {Model} Specs: Oil, Tires & Recalls | CarSpecFix`；症状页：`{Symptom}: Is It Safe to Drive? Causes & Fixes | CarSpecFix`；故障码页：`{CODE}: {Definition} | CarSpecFix`
  验收：构建脚本输出 Title 超过 60 字符的页面数 = 0、Title 重复数 = 0、H1 数量不等于 1 的页面数 = 0、Title 或 Meta 里含未签字模块的页面数 = 0。
- **R-M3 (P0)** `<html lang="en">`；不加 hreflang（不做多语言）。
- **R-M4 (P1)** Open Graph / Twitter card 基本标签（title、description、url、一张默认图）。

## D. Sitemap、robots、提交
- **R-S1 (P0)** `/sitemap.xml` 只包含：已发布 + index + 200 状态 + canonical 等于自身的 URL。`lastmod` 取数据/内容真实修改日期（不是构建时间）。
  验收：脚本检查 sitemap 中所有 URL 返回 200、无 noindex、canonical 自指；连续两次无改动构建，lastmod 不变。
- **R-S2 (P0)** `robots.txt` 允许全部抓取，声明 `Sitemap: https://carspecfix.com/sitemap.xml`；不屏蔽 CSS/JS。
- **R-S3 (P0)** IndexNow：在根目录放 key 文件；每次发布新页或数据变更时推送对应 URL 到 `https://api.indexnow.org/indexnow`。验收：发布日志里有推送记录且返回 200/202。
- **R-S4 (P0)** GSC（Domain 属性，DNS TXT 验证）和 Bing 站长工具验证需要的 DNS 记录/文件。注：GSC 和 Bing 账号登录由队长本人操作。

## E. 结构化数据（JSON-LD）
- **R-D1 (P0)** 全站：`Organization`（name、url、logo）+ `WebSite`。
- **R-D2 (P0)** 年款页：`Car`（brand、model、vehicleModelDate，以及已核实的 fuelEfficiency 等字段；缺值字段不输出）+ `BreadcrumbList` + `WebPage`/`Article`（dateModified、author 指向作者页）。
- **R-D3 (P0) [v2]** 症状页、故障码页：`Article` + `BreadcrumbList`。**不输出 `FAQPage`**，页面上也不为 schema 专门加 FAQ 区块。
- **R-D4 (P0)** 禁止输出：`FAQPage`、`HowTo`、`Product`、`Offer`、`AggregateRating`、`Review`。
  验收（D 全部）：试点每类模板各抽 2 页过 Google Rich Results Test 和 validator.schema.org，0 错误；schema 数值与页面可见值一致。

## F. 内链与面包屑
- **R-L1 (P0)** 面包屑：可见 + `BreadcrumbList`，层级 首页 → 车型汇总（若存在）→ 年款；症状/码页 首页 → `/symptoms/` 或 `/codes/` → 当前页。
- **R-L2 (P0) [v2]** 年款页链接：同车型其他**已上线**年款、这款车**有出处**的相关症状和故障码、`/sources/`。症状页、故障码页链接：数据里标为相关的症状和代码，以及我们有数据的受影响车型。**没有相关数据就不放链接块，不按固定数量凑链接。** 相关关系来自数据字段（由小站或小数维护），不由模板自动拼。
- **R-L3 (P0) [v2]** 构建检查：每个已上线页面至少有 1 条入链（来自索引页或相关页），全站没有指向 404 或未上线页面的内部链接。验收：构建报告显示 0 孤立页、0 坏链。
- **R-L4 (P1)** 正文内链不超过约 30 条/页（导航和页脚不计），超出时报警。
- **R-L5 (P0)** 内链使用普通 `<a href>`（不靠 JS 点击跳转），锚文本用自然描述（比如车型名、症状名），不刻意堆精确匹配的关键词。
- **R-L6 (P0)** 年款页属性区块加锚点 id：`#oil`、`#tires`、`#mpg`、`#recalls`、`#problems`，页首有跳转目录。

## G. 页面内容渲染
- **R-C1 (P0)** 每个数值旁显示出处（手册文件号+页码 / NHTSA 召回编号链接 / fueleconomy.gov 链接）；换算值标 “converted”；MPG 标 “US mpg”。
- **R-C2 (P0) [v2]** 机油容量、MPG 按发动机/配置分行显示；**轮胎和胎压按 `tires.rows[]` 分行显示（每款车最多 10 行）**，每行带轮毂/配置、尺寸、前后胎压、出处和页码，不合并成区间。解析不了的行不显示。验收：抽查已上线的多配置车型，行数与签字数据一致，并且 ≤10 行。
- **R-C3 (P0)** 每页显示 “Updated YYYY-MM-DD”，与 sitemap lastmod、schema dateModified 同一数据源。
- **R-C4 (P0)** 召回日期统一 ISO 格式（数据里是 DD/MM/YYYY）。
- **R-C5 (P0)** 每页有 “Report a wrong spec” 入口（链接到联系页并带上当前 URL）。
- **R-C6 (P0)** 核心内容（数值表、原因列表）在初始 HTML 中（静态生成或 SSR），不依赖客户端 JS 渲染。验收：`curl` 拿到的 HTML 中能找到机油容量数值。
- **R-C8 (P0) [v2] 答案优先布局**：
  - 年款页首屏（390px 手机，不滚动）就能看到速查卡：机油容量（含/不含滤芯）+ 粘度、前后胎压、轮胎规格，每项带出处；如果机油量因发动机而不同，先显示发动机选择。
  - 症状页、故障码页首屏是快速答案框：能不能开、严重程度、费用区间（没有出处就显示 Not yet verified），然后才是原因列表。
  - 顺序按 user-needs §2.1–2.4。
  验收：4 类模板各截一张 390px 首屏图，速查卡或答案框完整出现在首屏。
- **R-C9 (P0) [v2]** 不渲染凑字数的内容：通用科普段落、FAQ 区块、假评分，以及没有数据的空 H2。
- **R-C7 (P1)** 广告位只在表格下方或侧边栏，不插在数值中间；广告位预留固定高度避免布局偏移；首屏的速查卡和答案框区域内不放广告。

## H. 站速与移动端
- **R-P1 (P0)** CSS 构建时编译（不用 Tailwind CDN），只输出用到的样式。
- **R-P2 (P0)** 移动端 PageSpeed Insights（Lighthouse 实验室数据）：Performance ≥ 90、SEO = 100、Accessibility ≥ 90；LCP < 2.5s、CLS < 0.1、TBT < 200ms。按 4 类模板各测 1 页。（Core Web Vitals 的真实用户数据要等有流量后在 GSC 看。）
- **R-P3 (P0)** 图片用 WebP/AVIF、带 width/height、首屏外 lazy-load；字体用系统字体或 `font-display: swap`。
- **R-P4 (P0)** HTTPS、HTTP/2 或以上、HTML 设置合理缓存，静态资源长缓存带 hash。
- **R-P5 (P0)** 移动端无横向滚动（390px 宽），点击区域不过小；表格在手机上可横向滚动或改为卡片。

## I. 其他页面
- **R-O1 (P0)** `/about/`、`/sources/`（数据来源、抓取日期、更新频率、更正记录）、`/authors/{slug}/`（`Person` schema，如实写身份）、`/contact/`、`/privacy/`，均可被收录、在页脚链接。
- **R-O2 (P1)** `/codes/` 和 `/symptoms/` 索引页列出全部已发布页面。

## J. 用户价值信号 [v2]
- **R-A1 (P0)** 页内反馈：“Did this page answer your question? Yes / No”，选 No 后可以填“缺什么”。不收集个人信息、不用 cookie；记录 URL、选项、文本和日期。
- **R-A2 (P1)** 事件统计：速查卡的复制和打印点击、从年款页跳到症状页或故障码页的点击、“Report a wrong spec”的提交数。Cloudflare Web Analytics 不支持事件，需要另选方案（用什么工具待队长定，见方案第 13 节 #2）。
- **R-A3 (P0)** 纠错表单：带上当前 URL 和字段名，提交后进小数的核实队列。
  验收：在测试环境提交 1 条反馈和 1 条纠错，能在后台或导出文件里看到。

## 验收汇总（上线前 SEO 检查我来做）
上线前我会按本清单逐条检查，并跑：sitemap/canonical/状态码脚本、Rich Results Test、PageSpeed Insights、`grep TODO`、孤立页/坏链报告。不通过的条目会在群里列给小码。

## [v2] R-I1 配图（P1）
- 首屏主图 eager 加载并加 fetchpriority=high，其余图片 loading=lazy，所有图片写 width 和 height。验收：Lighthouse 中 LCP 不变差，CLS < 0.1。
- ImageObject 的 license、creator、creditText 与页面上的署名组件一致。验收：Rich Results Test 没有报错。
- sitemap 里包含 image:image。验收：sitemap 里每张已上线图片都有对应条目。

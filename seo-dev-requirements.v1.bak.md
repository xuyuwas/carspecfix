# carspecfix.com SEO 开发需求（给小码）

> 来自 `seo-plan-final.md`。每条都写了验收方式，技术实现由小码定。优先级：**P0 = 试点上线前必须完成**，P1 = 试点期内完成，P2 = 第二批前完成。

## A. URL 与路由
- **R-U1 (P0)** 路由：`/`、`/specs/{make}/{model}/{year}/`、`/specs/{make}/{model}/`、`/symptoms/{slug}/`、`/codes/{code}/`、`/symptoms/`、`/codes/`、`/about/`、`/sources/`、`/authors/{slug}/`、`/contact/`、`/privacy/`。
  验收：试点 30 页 URL 与 `pages.csv` 中 P1 的 `target_url` 完全一致（脚本比对 0 差异）。
- **R-U2 (P0)** 全部小写、连字符、以 `/` 结尾。不带斜杠、大写、`www`、`http` 的版本一次 301 到规范 URL（不允许 302、不允许跳转链 >1 跳）。
  验收：`curl -I` 抽测 `http://www.carspecfix.com/Specs/Toyota/RAV4/2020` → 一跳 301 到 `https://carspecfix.com/specs/toyota/rav4/2020/`。
- **R-U3 (P0)** 不存在的 URL 返回真 404 状态码（不是 200 的“软 404”），有自定义 404 页带首页和搜索入口。
- **R-U4 (P0)** 试点期不生成品牌页 `/specs/{make}/`；访问返回 404（或 301 到首页的品牌区域，二选一，写进技术方案）。面包屑不得链接到不存在的页面。
- **R-U5 (P0)** URL 参数（如 `?ref=`、`?utm_`）的页面 canonical 指向无参数版本。

## B. 收录控制与质量闸门
- **R-Q1 (P0)** 构建时按闸门判断 index/noindex：
  - 年款页：机油（容量+粘度）与轮胎（尺寸+胎压）都有出处字段非空且不是 TODO，且召回和 MPG 已有数据 → index；
  - 电车（Model Y）：轮胎 + 续航 + 召回（字段待小站确认）；
  - 症状/码页：≥3 个带来源的原因 + 修理费区间（带来源） → index。
  不满足的页：`<meta name="robots" content="noindex,follow">`，**不进 sitemap，也不被任何可收录页链接**。
  验收：构建输出一份报告（每页 index/noindex + 原因），人工抽查 5 页一致。
- **R-Q2 (P1)** 构建时计算同模板页面两两正文相似度（去掉导航、页脚、模板固定文字），>80% 的页面对输出警告。验收：报告文件存在，试点 30 页无警告或已人工确认。
- **R-Q3 (P0)** 任何 `TODO` 值不得渲染到 HTML、title、meta、schema 中；缺值显示 “Not yet verified — check your owner's manual”，整块无数据则隐藏整个模块（含 H2）。
  验收：构建后 `grep -ri "todo" dist/` 为 0。
- **R-Q4 (P0)** 发布控制：支持按日期/批次发布（每天约 10 页），未发布页面不生成、不进 sitemap、不被链接。

## C. Canonical、meta 与模板
- **R-M1 (P0)** 每个可收录页有自引用绝对 canonical（`https://carspecfix.com/.../`）。
- **R-M2 (P0)** Title / H1 / Meta 按 `seo-plan-final.md` 第 4 节模板生成；每页唯一 title、唯一 H1（每页只有 1 个 H1）。Title 超过 60 字符时自动降级（去掉末尾属性词）。Meta 中缺值片段整段删除。
  验收：构建脚本输出 title 重复数 = 0、H1 数量 ≠ 1 的页面数 = 0、title >60 字符的页面列表。
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
- **R-D3 (P0)** 症状/码页：`Article` + `BreadcrumbList`；`FAQPage` 仅在页面有可见问答时输出，且问答文本与页面一致。
- **R-D4 (P0)** 禁止输出：`HowTo`、`Product`、`Offer`、`AggregateRating`、`Review`。
  验收（D 全部）：试点每类模板各抽 2 页过 Google Rich Results Test 和 validator.schema.org，0 错误；schema 数值与页面可见值一致。

## F. 内链与面包屑
- **R-L1 (P0)** 面包屑：可见 + `BreadcrumbList`，层级 首页 → 车型汇总（若存在）→ 年款；症状/码页 首页 → `/symptoms/` 或 `/codes/` → 当前页。
- **R-L2 (P0)** 年款页自动链接：同车型其他已发布年款、该车相关症状/故障码 3–5 个、`/sources/`。症状/码页链接受影响的已发布年款页和 3–5 个相关症状/码。只链接已发布且 index 的页面。
- **R-L3 (P0)** 构建时检查：每个 index 页至少被 2 个其他 index 页链接（孤立页报错）；全站无指向 404/noindex 页的内部链接。验收：构建报告 0 孤立页、0 坏链。
- **R-L4 (P1)** 正文内链不超过约 30 条/页（导航和页脚不计），超出时报警。
- **R-L5 (P0)** 内链使用普通 `<a href>`（不靠 JS 点击跳转），锚文本由数据生成（如 “2020 RAV4 specs”），不全站同一精确锚文本。
- **R-L6 (P0)** 年款页属性区块加锚点 id：`#oil`、`#tires`、`#mpg`、`#recalls`、`#problems`，页首有跳转目录。

## G. 页面内容渲染
- **R-C1 (P0)** 每个数值旁显示出处（手册文件号+页码 / NHTSA 召回编号链接 / fueleconomy.gov 链接）；换算值标 “converted”；MPG 标 “US mpg”。
- **R-C2 (P0)** 机油容量、MPG 按发动机/配置分行显示，不合并成区间。
- **R-C3 (P0)** 每页显示 “Updated YYYY-MM-DD”，与 sitemap lastmod、schema dateModified 同一数据源。
- **R-C4 (P0)** 召回日期统一 ISO 格式（数据里是 DD/MM/YYYY）。
- **R-C5 (P0)** 每页有 “Report a wrong spec” 入口（链接到联系页并带上当前 URL）。
- **R-C6 (P0)** 核心内容（数值表、原因列表）在初始 HTML 中（静态生成或 SSR），不依赖客户端 JS 渲染。验收：`curl` 拿到的 HTML 中能找到机油容量数值。
- **R-C7 (P1)** 广告位只在表格下方或侧边栏，不插在数值中间；广告位预留固定高度避免布局偏移。

## H. 站速与移动端
- **R-P1 (P0)** CSS 构建时编译（不用 Tailwind CDN），只输出用到的样式。
- **R-P2 (P0)** 移动端 PageSpeed Insights（Lighthouse 实验室数据）：Performance ≥ 90、SEO = 100、Accessibility ≥ 90；LCP < 2.5s、CLS < 0.1、TBT < 200ms。按 4 类模板各测 1 页。（Core Web Vitals 的真实用户数据要等有流量后在 GSC 看。）
- **R-P3 (P0)** 图片用 WebP/AVIF、带 width/height、首屏外 lazy-load；字体用系统字体或 `font-display: swap`。
- **R-P4 (P0)** HTTPS、HTTP/2 或以上、HTML 设置合理缓存，静态资源长缓存带 hash。
- **R-P5 (P0)** 移动端无横向滚动（390px 宽），点击区域不过小；表格在手机上可横向滚动或改为卡片。

## I. 其他页面
- **R-O1 (P0)** `/about/`、`/sources/`（数据来源、抓取日期、更新频率、更正记录）、`/authors/{slug}/`（`Person` schema，如实写身份）、`/contact/`、`/privacy/`，均可被收录、在页脚链接。
- **R-O2 (P1)** `/codes/` 和 `/symptoms/` 索引页列出全部已发布页面。

## 验收汇总（上线前 SEO 检查我来做）
上线前我会按本清单逐条检查，并跑：sitemap/canonical/状态码脚本、Rich Results Test、PageSpeed Insights、`grep TODO`、孤立页/坏链报告。不通过的条目会在群里列给小码。

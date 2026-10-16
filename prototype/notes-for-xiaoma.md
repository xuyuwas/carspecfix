# 给小码的备注（仅供参考，技术方案由小码定）
- 原型页面由 `gen.py` 从 `../spec_api_data.json`、`../spec_pages.csv`、`../symptom_pages.json` 生成，Tailwind 用的是 CDN，只用于预览，正式站点建议在构建时编译 CSS。
- 遇到 TODO 字段，页面统一显示 “Not yet verified — check owner's manual”，症状页显示 “source pending”，不要用估计值填空。
- 公制单位是按英制数值换算的（35 psi ≈ 241 kPa ≈ 2.4 bar；4.8 qt 对应手册给出的 4.5 L），页面上要注明“metric converted”。
- NHTSA 召回日期在数据文件里是 DD/MM/YYYY 格式，上线前建议统一改成 ISO 格式。
- 2020 RAV4 的车主手册 OM0R024U 还没确认对应年款，发布前要到 toyota.com 车主门户核对。
- 广告位只放在表格下方或侧边栏，不要插在数字中间。
- 建议（未决定）：用静态站生成器把 JSON 转成页面，部署到免费静态托管（比如 Cloudflare Pages），sitemap 的 lastmod 取数据的真实修改时间。

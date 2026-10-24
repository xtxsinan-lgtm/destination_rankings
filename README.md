# 🗺️ Destination Atlas · 全球硬核旅行目的地发现与决策平台 (`destination_rankings`)

一个零构建依赖（Zero-Build）、兼顾**硬核量化参数**与**大众实用出行决策**、可直接部署于 GitHub Pages / Vercel / Cloudflare Pages 的全球 11 大垂直领域（共 **745 处**殿堂级目的地与水陆航线）交互式排名与筛选系统。

---

## 🌐 十一大核心主题榜单矩阵（前端全交互接入）

1. 🏖️ **[`beaches.html`](./beaches.html) — 全球海滨与海岛度假胜地 Top 145（真热带 Top 100 + 季节性 Top 45）**
2. 🎢 **[`themeparks.html`](./themeparks.html) — The Thrill & Magic Index · 全球主题游乐园 Top 100 & 水上乐园 Top 15（含过山车数 / 年客流 / 面积 / 门票与快通）**
3. 🐋 **[`aquariums.html`](./aquariums.html) — The Abyss Index · 全球顶级水族馆 Top 35（含全馆总水体 / 最大单池水体 / 主视窗尺寸 / 物种数 / 生物总数）**
4. 🦁 **[`zoos.html`](./zoos.html) — Field Notes · 全球顶级动物园 Top 30 & 全美野生动物园 Top 10（含总面积 / 物种数 / 生物总数 / 体力强度）**
5. ⛷️ **[`ski.html`](./ski.html) — The Alpine & Powder Index · 全球滑雪度假村 Top 100（含垂直落差 / 雪道总长 / 年降雪量 / 最高海拔 / 雪票价）**
6. 🎭 **[`shows.html`](./shows.html) — The Grand Stage Index · 全球商业驻场秀 Top 100 & 中国/维加斯 Top 20（含一票一词条 / 0台词重工优先 / 黄金选座与湾区巡演日历）**
7. 🚀 **[`museums.html`](./museums.html) — Heavy Metal Index · 全球科技、工业与军事重器博物馆 Top 100（含免费场馆筛选 / 镇馆真机巨物 / 门票与时长）**
8. 🛥️ **[`cruises.html`](./cruises.html) — The Grand Fleet Index · 全球奢华邮轮、内河河轮与加拉帕戈斯游艇 Top 50（含 $/㎡/晚 空间单价 / 巨轮双层复式 vs 六星船 / 14家主流底价矩阵）**
9. ⛵ **[`sailing.html`](./sailing.html) — The Windward Odyssey · 全球双体帆船跳岛路线 Top 20（含 6 项全包账单拆解 / 26座停靠古镇52张实景图鉴 / 2027年26艘4卧真船跨月比价）**
10. 🚐 **[`rv.html`](./rv.html) — The Overland Odyssey · 全球殿堂级房车自驾路线 Top 20 & 五大洲 16 城比价中心（含位置特权评分 / 2大3小全包底价 / 30尺大车窄路劝退黑名单）**
11. ⚜️ **[`canals.html`](./canals.html) — Waterway Lockkeeper's Log · 全球运河与内河自驾房船路线 Top 20（含免船牌水闸指南 / 3卧4卧2027精确报价 / 176张实景图匹配的8天7晚逐日路书）**

---

## 🎯 面向普通大众的实用决策与留存功能

- **🖼️ 全站 Wikimedia 实景封面图鉴 (`images.js` + `images_themed.js`)**：为海岛、水族馆、动物园、博物馆、游乐园、雪场与驻场秀配备实景高光图与 CC 授权署名。
- **📅 1–12 月全球当季最佳旅行日历 (`index.html#seasonal-calendar`)**：点击任意月份，一键查看当月水温最暖海岛、粉雪巅峰雪场与室内全天候乐园/水秀推荐。
- **🎒 8 大王牌城市「一程多刷」组合包 (`index.html#city-combos`)**：精选奥兰多、拉斯维加斯、阿布扎比&迪拜、新加坡、东京&关东、大湾区（广州/珠海/澳门）、南加州、瓦伦西亚&马德里 8 条跨榜单联游路线与人均预算参考。
- **🧭 跨榜单「周边 100km 顺路玩」推荐 (`shared_widgets.js`)**：基于全站 585 个目的地的精确经纬度（Haversine），自动在卡片上提示 100km 半径内的其他上榜景点。
- **✈️ 全站通用「从你的城市出发」飞行时长估算 (`shared_widgets.js`)**：在底部悬浮栏切换出发城市（北上广深、港澳台、东京、新加坡、伦敦、纽约、洛杉矶等），全站所有榜单卡片实时显示预计直飞/转机耗时。
- **❤️ 「想去 / 去过」足迹打卡与一键生成分享海报 (`shared_widgets.js`)**：纯前端 `localStorage` 记录心愿单与足迹，一键渲染高颜值 Canvas PNG 旅行成就海报保存至手机相册。
- **📱 PWA 离线访问与 SEO 结构化数据 (`manifest.json` + `sw.js` + `sitemap.xml` + `JSON-LD`)**：支持添加至手机主屏幕离线查阅，每页内置 `Schema.org ItemList` 结构化数据。

---

## ✨ 海滨与海岛榜核心方法论与三大铁律

1. **🌡️ 生理体感温度硬指标（不按死板纬度线切分）**
   - **🔥 365天真热带榜 (Top 100)**：基于 WMO / NOAA / JMA / BOM 30年气候统计基准，必须同时满足：
     - 全年最冷月**夜间平均低温 ≥ 18.0°C**（确保晚间海风吹拂无需穿厚外套）
     - 全年最冷月**表层海水温度 (SST) ≥ 21.0°C**（确保全年365天随时可裸泳下海）
   - **☀️ 季节性/亚热带/地中海榜 (Top 45)**：不满足上述全年双达标条件（如大加那利岛、毛里求斯、冲绳、圣灵群岛、撒丁岛、埃及红海、洛斯卡沃斯等），但在其**最佳暖季（连续3–9个月适泳期）**拥有世界顶级海滨体验。

2. **🧭 45分钟一日游圈独立拆分原则**
   - 严禁将相距数小时车程或需乘飞机中转的不同城市强行合并！
   - 例如：夏威夷拆分为茂宜岛、可爱岛、欧胡岛、大岛 4 个独立词条；泰国拆分为普吉、苏梅、甲米、丽贝、斯米兰、芭堤雅 6 个独立词条；斯里兰卡拆分为南岸与东岸；越南芽庄与富国岛各自独立。
   - 仅当主城与离岛处于 **≤45分钟快艇/轮渡一日游圈**（如芭堤雅+20分钟快艇格兰岛、三亚+蜈支洲岛、那霸+35分钟快船渡嘉敷岛）时允许作为同一度假目的地评估。

3. **📏 统一 76.5 分准入底线与 8 维量化模型**
   - **海沙水质 (25%)**：海水透明度、松石绿层次、白沙细腻度
   - **自然风景 (15%)**：火山峰、花岗岩巨石、泻湖航拍、悬崖海岸
   - **玩水体验 (15%)**：浮潜珊瑚礁生态、深潜大货（鲸鲨/魔鬼鱼/海龟）、跳岛
   - **风浪舒适 (10%)**：外堡礁遮蔽度、全年平静可安全下水游泳天数
   - **酒店硬件 (10%)**：水屋/悬崖泳池别墅美学、一岛一酒店私密性
   - **餐饮美食 (10%)**：海鲜品质、当地菜系丰富度、米其林与海滩酒吧
   - **陆地不无聊 (10%)**：历史古迹、火山雨林徒步、野生动物、逛街夜市
   - **安全省心 (5%)**：社会治安、少推销宰客、卫生医疗与免签便利
   - **守门员同分对齐**：真热带榜第 100 名（芭堤雅+格兰岛 **76.5分**）与季节性榜第 45 名（广西北海涠洲岛 **76.5分**）严格同分对齐；低于 76.5 分的佛罗里达 Key West (73.5分)、新加坡圣淘沙 (72.0分)、佛得角萨尔岛 (71.5分)、槟城 (69.5分) 均收入底部“淘汰区守门员对标参考表”。

---

## 🚀 交互功能一览

- **🎛️ 个性化权重实时算分引擎**：提供 6 大一键预设（标准综合、潜水果冻海控、蜜月颜值水屋、亲子平浪省心、吃货陆地探险、纯海滩自然硬实力）及 8 个维度的独立滑块，实时重算 145 个目的地的百分制得分并动态重排。
- **🖼️ 145 处实景封面图鉴**：每处海岛均配有 Wikimedia Commons 实景海滩封面图（含作者与 CC 授权署名）与数据驱动的海景插画底图。
- **✈️ 「从你的城市出发」零 AI 纯前端距离引擎**：内置全球 100+ 出发城市坐标与浏览器地理定位，利用球面大圆距离（Haversine）实时换算飞行时间，按短途（≤5h）、中程（5–9h）、远行（9–14h）自动选出当前权重下的最佳海岸，仅保留全球通用的双人 5 晚 4★ 海景房价格基准。
- **⚔️ 海岛 8 维雷达图与实时优势对比**：任意勾选最多 3 个海岛，基于各目的地结构化评分、气候底线、房价、距离与详细评语，实时生成各自的核心胜出项、专属亮点与妥协提示。
- **📥 一键导出 CSV**：支持将当前自定义权重与筛选结果导出为 UTF-8 BOM 编码的 `.csv` 表格，直接用 Excel / Numbers 打开。

---

## 💻 本地运行与部署

本项目采用纯静态架构（`index.html` + `data.js` + `data_part2.js` + `app.js`），无需任何编译步骤：

```bash
# 本地启动预览服务器
python3 -m http.server 8080
# 浏览器访问 http://localhost:8080
```

---

## 📚 六大专项主题目的地硬核榜单库（水族馆 / 动物园 / 游乐园 / 滑雪场 / 驻场秀 / 科技重器博物馆）

除海滨度假胜地交互系统外，本仓库收录了六大按**纯粹展陈硬实力、硬件震撼度与大众实用指标**严格校准的全球专项榜单文档与结构化数据集，并已全部作为同站独立页面接入前端（每页采用各自独立的视觉风格，8 页顶部切换栏互通）：

- 🐋 [`aquariums.html`](./aquariums.html)：**The Abyss Index**，深海沉浸风（含全馆总水体、最大单池水体、主视窗尺寸、物种数、生物总数、门票与多维排序）
- 🦁 [`zoos.html`](./zoos.html)：**Field Notes**，博物学野外手记风（含园区总面积、物种数、动物总数、步行强度与全美 10 大自驾游猎园）
- 🎢 [`themeparks.html`](./themeparks.html)：**The Thrill & Magic Index**，全球主题游乐园 Top 100 ＆ 水上乐园 Top 15（6 维滑块重算、过山车数量、年客流、门票与快通比价）
- ⛷️ [`ski.html`](./ski.html)：**The Alpine & Powder Index**，全球滑雪度假村 Top 100（6 维滑块重算、垂直落差、雪道总长、年均降雪量、雪票与粉雪季筛选）
- 🎭 [`shows.html`](./shows.html)：**The Grand Stage Index**，全球商业驻场秀 Top 50（舞台重工硬件规格、剧场座位数、语言友好度筛选、黄金选座避坑与停演备忘）
- 🚀 [`museums.html`](./museums.html)：**Heavy Metal Index**，工业档案风（A-List 前十、免费场馆一键筛选、门类/国别构成图、100 座总表搜索）

1. 🐋 **[全球顶级水族馆 Top 35（纯水下展陈视觉统治力榜）](./rankings/aquariums_top35.md)**
   - **核心标准**：剥离过山车与海豚剧场加分，100% 聚焦单缸水体体量（万立方米级巨缸）、全馆总水体、亚克力主视窗无接缝通透度、物种数、生物总数与镇馆巨物（鲸鲨、双髻鲨、翻车鱼、海牛、儒艮、巨藻林）。

2. 🦁 **[全球顶级动物园 Top 30 & 美国野生动物园 (Safari Parks) Top 10](./rankings/zoos_top30.md)**
   - **核心标准**：破除“古老历史”与“免费情怀”滤镜，按园区总面积（公顷）、超级温室穹顶、地形高差戏剧性、物种总数与动物群落规模排名。

3. 🎢 **[全球主题游乐园 Top 100 & 水上乐园 Top 15](./rankings/themeparks_top100.md)**
   - **核心标准**：按镇园大作与过山车水准 (25%)、造景沉浸感与 IP 还原度 (25%)、运营效率与排队友好度 (15%)、全龄亲子友好度 (15%)、餐饮周边与夜间大秀 (10%)、门票与快通性价比 (10%) 六维量化评分。

4. ⛷️ **[全球滑雪度假村 Top 100](./rankings/ski_resorts_top100.md)**
   - **核心标准**：按粉雪质量与年均降雪量 (25%)、垂直落差与可滑面积 (25%)、缆车系统与滑进滑出便利度 (15%)、全水平道型配比 (15%)、小镇氛围与温泉餐饮 (10%)、雪票住宿性价比 (10%) 六维量化评分。

5. 🎭 **[全球商业驻场秀 Top 50](./rankings/shows_top50.md)**
   - **核心标准**：仅收录专门定制剧场/实景舞台、每周固定排期、普通游客随时可买票入场的常驻大秀（剔除短期演唱会巡演），标注语言门槛、最佳选座区域与已停演传奇名单。

6. 🚀 **[全球科技、工业与军事重器博物馆 Top 100（100% 纯重器硬件版）](./rankings/industrial_tech_museums_top100.md)**
   - **核心标准**：彻底清退以声光互动、光学错觉和儿童科普为主的科学中心，100% 聚焦**人类历史真机孤品、万吨级工业/军事巨物（航母、核潜艇、土星五号、航天飞机、高炉矿井、万吨巨轮）与特种空间压迫感**。

7. 🗂️ **结构化数据源**
   - [`data_aquariums_zoos_museums.js`](./data_aquariums_zoos_museums.js)：导出 `window.AQUARIUMS_TOP35`、`window.ZOOS_TOP30`、`window.US_SAFARI_PARKS_TOP10` 与 `window.INDUSTRIAL_MUSEUMS_TOP100`。
   - [`data_themeparks.js`](./data_themeparks.js)：导出 `window.THEMEPARKS_TOP100` 与 `window.WATERPARKS_TOP15`。
   - [`data_ski.js`](./data_ski.js)：导出 `window.SKI_RESORTS_TOP100`。
   - [`data_shows.js`](./data_shows.js)：导出 `window.SHOWS_TOP50`。

---

## 🛳️ 全球邮轮与顶奢游艇全梯队硬核调研库（暂未接入前端网页，供直接查阅与后续扩展）

收录从顶奢酒店跨界超级游艇、印尼传统双桅帆船（Phinisi）、三大六星传统顶奢邮轮，到全球 14 大主流大众/轻奢/特色邮轮品牌的实测底价、套房分级与深度对比（全部附带具体起航日期与官网/权威系统可验证直达链接）：

1. 🛳️ **[全球邮轮与顶奢游艇全梯队硬核调研档案 (`rankings/cruises_global_guide.md`)](./rankings/cruises_global_guide.md)**
   - **第一部分**：三大传统顶奢邮轮（**Seabourn 世邦** `$3,798/人`、**Silversea 银海** `$3,900/人`、**Regent Seven Seas 丽晶七海** `$5,299/人`）未来一年最便宜 7 晚私人阳台套房（Veranda Suite）实测与逐日行程。
   - **第二部分**：更高档次的顶奢酒店跨界超级游艇（**The Ritz-Carlton Yacht Collection 丽思卡尔顿游艇** `$7,300–$7,900/人`、**Four Seasons Yachts 四季游艇** `$20,700/套房`、**Orient Express Sailing Yachts 东方快车帆船游艇** `€36,400–€81,900/套房`、**Aman at Sea 安缦游艇**）与新创顶奢邮轮（**Explora Journeys 意铂奢华邮轮** `$4,655/人`）最便宜 7 晚航次。
   - **第三部分**：**安缦（Aman）**与**阿丽拉（Alila）**印尼传统双桅帆船（Phinisi）与巡航游艇深度调查（*Amandira* 整船包船 `$17,000++/晚`、*Amanikan / Mahodaya* 全船 3 间阳台房整船包船 `$9,500+/晚`、*Alila Purnama* 按间散订唯一带私人阳台主卧 *Sriwijaya Master Suite* 科莫多 7 晚 `$15,565/人` & 四王群岛 7 晚 `$19,070/人`）。
   - **第四部分**：**每人每晚 `$500` 美元黄金预算线**——皇家加勒比（RCI）皇家套房三级制（`Sea Class` vs `Sky Class` vs `Star Class`）各船系（绿洲系、量子系、25万吨标志系、经典船系）实测可订套房梯度，以及同预算直上精致游轮（Celebrity）Edge 系列全包套房专区 **The Retreat**（`$499–$503/晚`）横向对比。
   - **第五部分**：**主流各大邮轮“最便宜的海上双层复式套房（Loft / Duplex / 2-Story Suites）”全网底价排行榜（时间不限）**——涵盖皇家加勒比（量子系 `SL` 天际复式最低总价 `$1,373/人`、最低每晚 `$351/晚`；`GL/OL` Star Class 复式 `$569–$605/晚`；绿洲系 `CL` 皇冠复式 `$362–$387/晚`；标志系 `IL` Icon Loft）、地中海邮轮（MSC 传奇系/世欧系带私人按摩浴缸的 `SLJ` 奥睿复式与 `YJD` 游艇会复式）、精致游轮（Celebrity Edge 系列带私人深水泡池的 `EV` Edge Villa 双层别墅）、诺唯真邮轮（NCL *Norwegian Aqua/Luna* 195㎡ 三卧双层复式 `H1`）与迪士尼邮轮（愿望级双层皇室套房与烟囱塔楼套房）。
   - **第六 & 第七部分**：**全球 14 大主流、轻奢与特色邮轮品牌**（RCI、MSC、Carnival、NCL、Costa、Princess、Holland America、Celebrity、Cunard、Virgin Voyages、Azamara、Disney、Oceania、Windstar）未来一年最便宜 7 晚航次全榜单（含内舱/海景/阳台/套房四档含税价），以及 **Azamara vs. Oceania（同款 3 万吨 R-Class 姊妹船身世揭秘）** 与 **Celebrity vs. Holland America（新老船代差与风格对比）** 深度解析。

2. 🗂️ **[邮轮与游艇结构化数据源 (`data_cruises.js`)](./data_cruises.js)**
   - 导出 `window.ULTRA_LUXURY_CRUISES_7N`、`window.INDONESIA_PHINISI_YACHTS`、`window.RCI_SUITE_TIERS`、`window.RCI_500_PER_NIGHT_SUITES`、`window.CHEAPEST_DUPLEX_SUITES`、`window.MAINSTREAM_AND_SPECIALTY_7N_CHEAPEST` 与 `window.CRUISE_BRAND_COMPARISONS` 七组结构化数据，预留后续前端接入。


5. 🚐 **[全球 10 大殿堂级房车自驾线路 & 五大洲 16 城（2大3小）全包价格硬核数据库](./rankings/rv_motorhome_routes_top10_and_pricing.md)**
   - **核心标准**：针对 2大3小（6–7 铺位大型 C 型/鹅头房车，≥3 张独立床位与卫浴）、7～9 天黄金闭环，按“位置特权（对标景区天价酒店的降维打击力）”、“大车驾驶友好度”、“单周里程合理性（650–1,450km）”与“营地亲子/温泉/生态体验”独立严选全球 Top 10 线路，并明确列出为何清退加州 1 号公路 Big Sur 段与爱尔兰/康沃尔窄路。
   - **实时结账页价格数据库**：完整收录美国（安克雷奇、丹佛、洛杉矶、拉斯维加斯）、加拿大（卡尔加里、温哥华、多伦多）、欧洲大陆（马德里、米兰、巴黎、慕尼黑、法兰克福）、北欧与北大西洋（挪威奥斯陆/卑尔根 + 瑞典/德国汉堡跨国提车方案、冰岛凯夫拉维克、爱尔兰都柏林）及澳新（布里斯班、墨尔本、悉尼、奥克兰、基督城）共 16 座核心城市的 2026–2027 实时裸车价、零起赔全险、里程包、5人床品厨具包与全落地总价。

6. 🗂️ **[房车线路与跨城比价结构化数据源 (`data_rv_routes.js`)](./data_rv_routes.js)**
   - 导出 `window.RV_ROUTES_TOP10`、`window.RV_ELIMINATED_ROUTES` 与 `window.RV_CITY_CHECKOUT_DB` 结构化数据对象。


---

## 🐘 非洲野生动物猎游（Safari）全景指南与 2026–2027 官方精确牌价库（纯文档与数据版，暂未接入前端网页）

本仓库新增收录了全非洲 10 大野生动物猎游目的地（南非、纳米比亚、博茨瓦纳、坦桑尼亚、肯尼亚、津巴布韦、赞比亚、乌干达、卢旺达、马达加斯加）的全维度对比、家庭适老化与疟疾/路况评估、自驾 vs 参团分项精算账单，以及奥卡万戈三角洲 7 大顶奢品牌 16 座营地与亲民营地的 2026–2027 官方精确牌价库（所有数据均锚定具体日期并附官方核验直链）：

1. 🌍 **[非洲 10 大 Safari 国家综合对比、自驾 vs 参团实测账单与家庭出行指南 (`rankings/african_safari_countries_and_budgets.md`)](./rankings/african_safari_countries_and_budgets.md)**
   - **全景对比与成本天梯**：南非、纳米比亚、肯尼亚、坦桑尼亚、博茨瓦纳、津巴布韦、赞比亚、乌干达、卢旺达、马达加斯加 10 国看动物王牌、成本天梯、年龄门槛、路况与疟疾/黄热病疫苗分布、非动物旅游资源对比。
   - **山地大猩猩省钱方案**：对比卢旺达（1,500 USD）、乌干达（800 USD）、刚果金（400 USD 但高危关闭）2026 官方许可证牌价，详解“飞卢旺达基加利 → 4小时陆路进乌干达布温迪南部”人均立省 1,000+ USD 走法。
   - **纳米比亚 vs 南非深度对比**：70% 碎石搓板路爆胎风险 vs 95% 高等级柏油路、两国无疟疾区与旱季埃托沙/克鲁格防蚊实测。
   - **多国自驾 vs 参团精确分项账单**：
     - **南非克鲁格（2大3小，3晚4天）**：锚定 `2026.11.09–11.12`，含约堡机场 SUV 租车（147.00 USD）+ SANParks 园内住宿（Olifants 468.93 USD / Skukuza 6人家庭别墅 607.50 USD）+ 保护费（165.37 USD）+ 精确油费与 N4 过路费（70.54 USD），全家总计 **851.84 USD**。
     - **纳米比亚、乌干达、马达加斯加、津巴布韦、坦桑尼亚（2大2小，4天3晚）**：逐项对比纯自驾 vs 当地参团/雇佣 Roadtrip Africa 官方包吃住司导（乌干达仅 +40 EUR/天、马达加斯加仅 +30 EUR/天）精确总价。
     - **肯尼亚与坦桑尼亚参团全拆解**：肯尼亚马赛马拉露营团 vs 舒适木屋团底价；坦桑尼亚北环线 6晚7天 舒适型“拼车不拼房”参团 vs 2人独立包车全拆解。

2. 🦁 **[博茨瓦纳奥卡万戈三角洲 7 大顶奢品牌与高性价比亲民营地 2026–2027 官方精确牌价全集 (`rankings/okavango_delta_camps_pricing_2026_2027.md`)](./rankings/okavango_delta_camps_pricing_2026_2027.md)**
   - **7 大顶奢猎游集团 16 座核心营地**：完整收录 **Wilderness**（`Mombo`、`Vumbura Plains`、`Little Vumbura`、`Qorokwe`、`Jacana`）、**&Beyond**（`Sandibe`、`Nxabega`）、**Great Plains Conservation**（`Duba Plains`、`Sitatunga Private Island`）、**Natural Selection**（`Tuludi`、`Tawana`、`Hyena Pan`）、**Singita**（2026年12月11日全新开业 `Singita Elela` 单卧/双卧/四卧及三项固定税费）、**A&K Sanctuary [原 Sanctuary Retreats]**（`Chief's Camp`、`Baines' Lodge`、`Stanley's Camp` 含 1–3晚 / 4–6晚 / 7+晚阶梯连住折扣）、**Belmond [LVMH 集团]**（`Eagle Island Lodge`）2026–2027 各季精确单价与 2人3晚总价。
   - **亲民底线与含小飞机全包套餐**：收录 **Oddballs' Camp**（含马翁往返轻型小飞机 3晚全包特惠价：2人1间平季 **2,150 USD** / 旺季 **2,670 USD**）、**Crocodile Camp**、**Khwai Bush Camp** 与 **Moremi Crossing**。

3. 🗂️ **[非洲猎游结构化数据源 (`data_african_safari.js`)](./data_african_safari.js)**
   - 导出 `window.AFRICAN_SAFARI_COUNTRIES`、`window.AFRICAN_SAFARI_2A2C_4D3N_BUDGETS`、`window.OKAVANGO_LUXURY_CAMPS`、`window.OKAVANGO_VALUE_CAMPS` 与 `window.GORILLA_PERMITS_2026` 五个结构化数组，供后续扩展使用。


---

## ⛵ 全球船宿、河轮、科考游艇与运河自驾游船专题档案库（Markdown 精确报价与行程库）

本仓库在 [`rankings/`](./rankings/) 目录下完整收录了**非洲/南美河轮船屋、加拉帕戈斯科考游艇、印尼潜水船宿、以及欧美加内河/运河自驾游船**的实测精确单一报价（无模糊区间）、每晚/每潜折算单价、逐日停泊攻略与 172 张地标实景配图（暂不接入前端网页，供直接查阅）：

1. 🦛 **[乔贝河（博茨瓦纳/纳米比亚）与亚马逊河（巴西/秘鲁/厄瓜多尔）船屋及河轮淡季精确报价指南](./rankings/chobe_amazon_houseboats.md)**
   - **涵盖范围**：非洲乔贝河 4 艘船屋（*Pangolin Voyager*、*Chobe Princess*、*Pride of the Zambezi*、*Zambezi Queen*）、巴西马瑙斯/黑河 4 艘船屋与河轮（*Amazonita*、*Amazon Clipper Traditional/Premium*、*Katerre*）、秘鲁伊基托斯/帕卡亚-萨米里亚保护区全部 11 艘河轮及水上木屋（*Amazon Oasis*、*Yaku*、*Amatista*、*La Perla*、*La Turmalina*、*Ayapua*、*Zafiro*、*Delfin I/II/III*、*Aria Amazon*）以及厄瓜多尔纳波河 2 艘河轮（*Manatee Amazon Explorer*、*Anakonda Amazon Cruise*），全部按 **2人1间（Double Occupancy）最实惠淡季/早鸟** 拆分为精确单一报价。

2. 🐢 **[加拉帕戈斯群岛（Galapagos）游艇巡航（散客拼船/按舱预订）全档位性价比与 5晚/6天 精确报价指南](./rankings/galapagos_cruises_guide.md)**
   - **涵盖范围**：`galapagosislands.com` 全档位（经济档 Budget ★★、中端舒适档 Mid-Range ★★★、一等头等舱 First-Class ★★★★、五星豪华档 Luxury ★★★★★）性价比之王横向对比、5晚/6天（6D/5N）主流双体船与单壳游艇精确报价、必付政府税费（\$200 国家公园门票 + \$20 INGALA 卡 + 往返机票）明细，以及全部 **12 艘五星豪华单壳游艇**逐一核查报告。

3. 🤿 **[印尼潜水船宿（科莫多 / 四王群岛 / 班达海）4大档次划分、3晚精确总价与全经典航线「每晚/每潜」精确折算全表](./rankings/indonesia_liveaboards_guide.md)**
   - **涵盖范围**：基于 `liveaboard.com` 全印尼 82 艘潜水船宿实测，梳理 4 大档次划分、科莫多 11 艘 3晚/4天（4D/3N）船宿在适宜平季（4–6月、10–11月）的 2人1间精确总价，以及全印尼 3 晚至 12 晚经典航程（科莫多、四王群岛、班达海）在 **① 纯船票口径** 与 **② 含必付税费全包落地口径** 下的精确 **「每晚价格」** 与 **「每潜价格」**。

4. 🚤 **[法国四大运河 & 英美加三大运河自驾游船深度对比（6大3小9人团 3卧/4卧 6月初精确报价与北威尔士/里多运河7晚停泊攻略）](./rankings/canal_boating_french_uk_north_america.md)**
   - **涵盖范围**：针对 **6大3小（共9人）6月初出行**，收录法国四大经典运河线（米迪运河、勃艮第、阿尔萨斯、卢瓦尔河/夏朗德河）四大船司（Le Boat、Locaboat、Nicols、Les Canalous）3卧室与4卧室整周/短租精确报价；**英国传统窄船（UK Narrowboat）、加拿大里多运河（Rideau Canal）、美国伊利运河（Erie Canal）** 三大运河横向评测与精确报价；北威尔士兰戈伦运河与加拿大里多运河 7 晚逐日停泊酒馆/国家公园营地推荐；以及体验过米迪运河后的下一次进阶选线指南。

5. ⛵ **[欧洲 10 大经典运河/内河自驾游船全攻略：2027年6月初3卧室精确报价 & 8天7晚逐日双图精确匹配行程（80天·160张实景地标图）](./rankings/european_10_canals_master_guide.md)**
   - **涵盖范围**：完整收录 **1. 法国米迪运河（Canal du Midi）**、**2. 法国阿尔萨斯（Alsace-Lorraine）**、**3. 英国北威尔士兰戈伦窄船（Llangollen Canal）**、**4. 苏格兰喀里多尼亚运河与尼斯湖（Caledonian Canal & Loch Ness）**、**5. 意大利威尼斯泻湖（Venetian Lagoon）**、**6. 英国泰晤士河（River Thames）**、**7. 荷兰风车与湖区（Netherlands）**、**8. 法国洛特河（River Lot）**、**9. 比利时根特与布鲁日（Belgium Ghent & Bruges）**、**10. 法国勃艮第（Burgundy — 尼维尔内运河与索恩河双线）** 的 **2027年6月初 8天7晚 3卧室精确单一报价总表**，以及 **全部 10 条航线 Day 1 至 Day 8 逐日停泊行程与每天 2 张 100% 精确匹配地标实景图（共 80 天、160 张实景图，图片存放于 [`rankings/images/canals/`](./rankings/images/canals/)）**。



---

## 🚂🚢 全球豪华火车、各国卧铺与内河/运河/日本豪华游轮全景指南库（纯文档与数据版，暂未建网页）

本仓库新增两大深度价格调研、空间性价比（`$/㎡/晚`）与分级避坑指南文档，以及对应的结构化 JS 数据集：

1. 🚂 **[全球豪华观光火车、夜火车与各国卧铺全景指南与性价比排行榜 (`rankings/luxury_and_sleeper_trains_global.md`)](./rankings/luxury_and_sleeper_trains_global.md)**
   - **全球 14 大豪华火车性价比与每平米单价排行**：涵盖南非《蓝色列车 Blue Train》（$102/㎡/晚）、《非洲之傲 Rovos Rail》（$112/㎡/晚）、西班牙国铁 Renfe 四大专列（《坎塔布里亚大豪华号》《安达卢西亚之星》《绿海岸快车》及全包仅 $190/晚的《拉罗夫拉快车 El Expreso de La Robla》）、印度《王公快车》、加拿大《The Canadian Prestige》、澳洲《The Ghan》、秘鲁《Andean Explorer》、苏格兰《Royal Scotsman》与欧洲《VSOE 东方快车》。
   - **日本“御三家”顶奢卧铺与定期寝台**：《九州七星号》《四季岛号》《瑞风号》（含 35㎡ 独占整节车厢套房价格倒挂分析）、《The Royal Express》及平民定期寝台《Sunrise 出云/濑户号》。
   - **美铁 Amtrak 热门风景线 vs. 俄铁 RZD 2人包间卧铺**：扣除恶劣天气季后的 Amtrak 最低档（Low Bucket）实测底价（双人同行立省 40% 机制，Roomette vs. Bedroom），以及俄铁一等 2人平铺软卧 `СВ`（低至 $22–$43/㎡/晚）与独立淋浴大床高包 `Люкс VIP` 全路线价格表。
   - **除中俄外全球 6 大“干净整洁且实惠”的卧铺体系**：芬兰 `VR Santa Claus Express` 北极双层独卫夜车（人均 $65 住独卫）、泰国国铁 `SRT` 中车长客造不锈钢红丝绒新车、乌兹别克斯坦 & 哈萨克斯坦 `Talgo`、奥地利 `ÖBB 新一代 Nightjet` 太空舱 & 中欧 `EuroNight`/`RegioJet`、高加索 `Stadler` 新车。
   - **全球「夜间停车过夜（Overnight Stabling）」火车全盘点**：区分“每晚 100% 停站睡觉的观光专列”与“早登车+晚下车在站台睡饱的平价定期夜车”（瑞典 `SJ` 马尔默夜车、英国 `Night Riviera`）。
   - **中国近年 8 大豪华旅游专列红黑榜与新疆线 PK**：《丝路梦享号》《呼伦贝尔号》《星光·澜湄号》《熊猫专列·成都号》《新东方快车（金钻 vs. 蓝钻无独卫陷阱）》《林都号》《大河之南号》每晚单价、大巴时长、夜间赶路过夜实况，以及**中国普通卧铺「双层纵向动卧 CRH2E-NG / 智能动卧 CR400AF-AE」vs.「假动卧绿巨人 CR200J」vs.「Z字头 25T」平稳度终极排行与选铺防晃指南**。

2. 🚢 **[全球内河游轮、欧洲运河船与日本豪华邮轮全景指南与价格分档榜 (`rankings/river_canal_and_luxury_cruises_global.md`)](./rankings/river_canal_and_luxury_cruises_global.md)**
   - **欧洲运河游船（Canal Cruise）最低价对比**：全包式奢华酒店驳船（CroisiEurope 法国佩尼什船、European Waterways、Belmond Afloat in France）vs. 自驾运河船（Le Boat / Nicols / Locaboat）。
   - **全球 6 大传奇内河顶奢河轮横向对标**：中国三峡《长江探索号 Yangzi Explorer》（31㎡全阳台套房仅 $323/晚、$10.4/㎡/晚，性价比全球第一）对标多瑙河、莱茵河、尼罗河、美国密西西比河（PVSA 法案保护下最低 $571/晚）与缅甸伊洛瓦底江。
   - **维京河轮（Viking）中美官网实时底价实测**：美国英文官网（`vikingrivercruises.com` 11月最低 $1,999/7晚）vs. 中国官网（`vikingcruises.cn` 全中文一价全包实时价及旺季价格倒挂彩蛋）。
   - **埃及尼罗河游轮 5 大档次全船司实时底价总表**：揭秘 10 年前 $30/晚历史真相，完整收录从第 1 档本土五星船（$85/晚全包）、第 2 档德资 Jaz/Steigenberger、第 3 档 Mövenpick/Sonesta、第 4 档 Historia/Kazazian/Viking 到第 5 档顶奢 **The Oberoi Zahra/Philae** 与 **A&K Sanctuary (Sun Boat III/IV & 2026新船 Nile Seray)** 的官方实时价格表。
   - **中国长江三峡游轮 5 大档次全船司分级表**：从 ¥800 平价世代船到总统/黄金、华夏神女/美维凯悦、世纪绿洲/长江叁号，直至顶奢《长江探索号》。
   - **日本本土 5 大豪华邮轮与海上旅馆**：濑户内海漂浮木造旅馆 `guntû（ガンツウ）`、日本邮船 2025 全新旗舰 `飞鸟 III (Asuka III)` 与 `飞鸟 II`、商船三井全套房船 `三井海洋富士 (Mitsui Ocean Fuji)` & `樱花号`（原世邦顶奢船，全包酒水岸上游性价比冠军），以及外资母港对照 `钻石公主号`。

3. 🗂️ **[火车与游轮结构化数据源 (`data_trains_and_cruises.js`)](./data_trains_and_cruises.js)**
   - 导出 `window.GLOBAL_LUXURY_TRAINS_RANKING`、`window.JAPAN_LUXURY_AND_SLEEPER_TRAINS`、`window.AMTRAK_POPULAR_SLEEPER_ROUTES`、`window.RUSSIA_RZD_2BERTH_SLEEPERS`、`window.CLEAN_AFFORDABLE_SLEEPERS_EX_CN_RU`、`window.CHINA_LUXURY_TRAINS_RANKING`、`window.CHINA_SLEEPER_STABILITY_RANKING` 与 `window.GLOBAL_RIVER_AND_LUXURY_CRUISES` 八大结构化数据集。

---

## ⛵ 全球与欧洲双体帆船（4卧 Catamaran + 船长）航线规划与实时报价库（纯文档与数据版，暂未建网页）

本仓库新增针对 **4 卧双体帆船（40–45 英尺，如 Lagoon 42 / Bali 4.2 / FP Astrea 42 / Bali Catspace）+ 雇佣专业船长（Skipper）+ 必选基地杂费 + 港口/浮球费 + 燃油费** 的 **7 天全包实时报价拆解与全球航线库**：

1. 🏆 **[全球 5 大最值得体验的双体帆船航线规划书 (`rankings/sailing_top5_routes.md`)](./rankings/sailing_top5_routes.md)**
   - **核心内容**：针对已体验过克罗地亚航线的进阶玩家，精选全球 **5 条殿堂级双体帆船航线**——**1. 希腊·爱奥尼亚群岛南线 (Lefkada)**、**2. 意大利撒丁岛北 + 法国科西嘉 (La Maddalena & Bonifacio)**、**3. 意大利西西里·伊奥利亚七大火山群岛 (Aeolian Islands)**、**4. 加勒比海英属维尔京群岛 (BVI)**、**5. 法属波利尼西亚·大溪地顺风群岛 (Raiatea $\rightarrow$ Taha'a $\rightarrow$ Bora Bora)**，包含 **7 天全包落地总价六维拆解总表**、实时可验证船源链接及 **Day 1 至 Day 7 每日航程、锚地玩水与岸上餐饮停泊攻略**。

2. 🌍 **[全球与欧洲双体帆船硬核指南与航线百科全书 (`rankings/sailing_routes_global_guide.md`)](./rankings/sailing_routes_global_guide.md)**
   - **完整收录 7 大板块**：
     - **全球 Top 5 航线规划与全包报价拆解**；
     - **欧洲媲美/超越克罗地亚的 4 大神仙替代航线深度对比**（及为何排除基克拉泽斯 Meltemi 强北风区的排雷说明）；
     - **希腊莱夫卡达（Lefkada）南爱奥尼亚海 7 天环线沿途 8 大古镇/海湾详解**（每站配 2 张 Wikimedia 实景图）；
     - **撒丁岛北+科西嘉（Bonifacio）、土耳其戈杰克（Göcek & Fethiye）、西西里火山群岛（Aeolian Islands）三条 7 天航线共 18 个核心停靠站点详解**（每站配 2 张实景图）；
     - **加勒比海 BVI vs. 欧洲地中海航线六大维度正面 PK** 与三大标志性站点实景；
     - **除欧洲与 BVI 外的全球 6 大世界级帆船圣地全览**（大溪地 Bora Bora、塞舌尔群岛、巴哈马 Exumas 猪岛与护士鲨、格林纳丁斯 Tobago Cays、泰国普吉攀牙湾喀斯特峰林+随船泰厨、澳洲大堡礁圣灵群岛白天堂流沙海滩与观鲸）；
     - **欧洲夏季（6–9月）7 大热门海区全包价格横向对比、主流比价平台（Boataround / SamBoat / Click&Boat / GlobeSailor）与直营船队名录，以及 26 艘代表性 4 卧双体帆船 2027 年 6/7/8/9 月实时价格核验总表**。

3. 🗂️ **[双体帆船航线与实时报价结构化数据源 (`data_sailing_routes.js`)](./data_sailing_routes.js)**
   - 导出 `window.SAILING_TOP5_ROUTES`、`window.SAILING_GLOBAL_DESTINATIONS`、`window.SAILING_BVI_VS_EUROPE`、`window.SAILING_EUROPEAN_PRICE_BENCHMARKS`、`window.SAILING_PLATFORMS_AND_FLEETS`、`window.SAILING_VERIFIED_BOATS_2027` 与 `window.SAILING_ROUTE_STOPS_GALLERY` 七大结构化数据集。


---

## 🚐 全球 10 大殿堂级房车自驾线路 & 五大洲 16 城（2大3小）全包价格硬核数据库（纯文档与数据版，暂未建网页）

本仓库新增针对 **2大3小（五口之家，需 6–7 铺位大型 C 型/鹅头房车，标配 ≥3 张独立床位与独立卫浴）**、**7～9 天黄金闭环**、**气候适宜月份** 的全球房车自驾选线与 16 城实时结账页全包价格数据库：

1. 🏆 **[全球 10 大殿堂级房车自驾线路 & 五大洲 16 城全包价格硬核数据库 (`rankings/rv_motorhome_routes_top10_and_pricing.md`)](./rankings/rv_motorhome_routes_top10_and_pricing.md)**
   - **独立严选全球 Top 10 房车自驾线路**：按“位置特权（对标景区天价酒店的降维打击力）”、“大车驾驶友好度”、“单周黄金里程（650–1,450km）”与“营地亲子/温泉/生态体验”四大硬指标，评选出 **1. 美国·阿拉斯加（基奈半岛+荷马角+迪纳利）**、**2. 加拿大·落基山脉（班夫+冰原大道+贾斯珀）**、**3. 新西兰·南岛大环线（含哈斯特通道与西海岸雨林冰川）**、**4. 美国·大黄石生态圈（大提顿+黄石+熊牙公路）**、**5. 日本·北海道（富良野美瑛+道东三湖+知床森林野天温泉线）**、**6. 挪威·罗弗敦群岛午夜阳光线 / 双峡湾线**、**7. 美国·犹他州“Mighty 5”红岩峡谷+12号景观公路+鲍威尔湖**、**8. 澳大利亚·昆士兰阳光与黄金海岸亲子线 / 塔斯马尼亚环岛**、**9. 德奥意·多洛米蒂与阿尔卑斯五星奢华营地环线**、**10. 冰岛·黄金圈与南岸冰火奇观线 / 苏格兰高地天空岛线**，并附带为何清退加州 1 号公路 Big Sur 段与爱尔兰/康沃尔窄路的排雷说明。
   - **五大洲 16 城 2026–2027 实时结账页（Step 1 Checkout）全包价格拆解**：基于 Camper Champ 及各大主流车行（Maui、Britz、Apollo、Star RV、Mighty、JUCY、Freedom、Cruise America/Canada、Road Bear、El Monte、CanaDream、Fraserway、McRent、Indie Campers、Touring Cars、Europcar/Holdur）实时数据，完整收录美国（安克雷奇、丹佛、洛杉矶、拉斯维加斯）、加拿大（卡尔加里、温哥华、多伦多）、欧洲大陆（马德里、米兰、巴黎、慕尼黑、法兰克福）、北欧与北大西洋（挪威奥斯陆/卑尔根 + 瑞典斯德哥尔摩/德国汉堡跨国提车立省 37%–47% 方案、冰岛 6 月极昼季 Indie 半价彩蛋、爱尔兰都柏林/北爱自提方案）及澳新（布里斯班、墨尔本、悉尼、奥克兰、基督城）的 **7 晚裸车价 + 零起赔全险 + 5人床品厨具包 + 里程包/柴油税 + 7晚营地与燃油费** 全落地总表。

2. 🗂️ **[房车线路与 16 城跨季比价结构化数据源 (`data_rv_routes.js`)](./data_rv_routes.js)**
   - 导出 `window.RV_ROUTES_TOP10`、`window.RV_ELIMINATED_ROUTES` 与 `window.RV_CITY_CHECKOUT_DB` 三大结构化数据集。

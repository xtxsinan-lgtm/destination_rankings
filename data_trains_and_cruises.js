// Global Luxury Trains, Sleeper Trains, River Cruises, Canal Barges & Japan Luxury Cruises Structured Dataset (2026-2027 Verified)
// Corresponding full documentation:
//   - ./rankings/luxury_and_sleeper_trains_global.md
//   - ./rankings/river_canal_and_luxury_cruises_global.md

// 1. 全球 14 大豪华火车「每平米价格（$/㎡/晚 & $/㎡/全程）」从低到高全排名
window.GLOBAL_LUXURY_TRAINS_RANKING = [
  { rank: 1, name: "The Blue Train (蓝色列车)", country: "南非", operator: "PRASA", route: "比勒陀利亚 ↔ 开普敦 (3天2晚)", cabin: "De Luxe (8㎡) / Luxury (10.26㎡, 含浴缸)", areaSqm: 8.0, totalPriceUsd: 1625, perNightUsd: 813, pricePerSqmPerNightUsd: 102, pricePerSqmTotalUsd: 203, stablingMode: "部分低速夜行/停靠", allInclusive: true, url: "https://www.bluetrain.co.za/" },
  { rank: 2, name: "El Transcantábrico Gran Lujo (坎塔布里亚大豪华号)", country: "西班牙", operator: "Renfe", route: "圣塞瓦斯蒂安 ↔ 圣地亚哥 (8天7晚)", cabin: "Deluxe Suite 三居室大套房 (14㎡)", areaSqm: 14.0, totalPriceUsd: 10000, perNightUsd: 1429, pricePerSqmPerNightUsd: 102, pricePerSqmTotalUsd: 714, stablingMode: "100% 每晚停站过夜", allInclusive: true, url: "https://www.renfe.com/es/en/experiencias/viajes-de-lujo/el-transcantabrico-gran-lujo" },
  { rank: 3, name: "Rovos Rail (非洲之傲)", country: "南非", operator: "Rovos Rail", route: "比勒陀利亚 ↔ 开普敦/维多利亚瀑布 (2–15晚)", cabin: "Pullman (7㎡) / Deluxe (10㎡) / Royal (16㎡, 含浴缸)", areaSqm: 16.0, totalPriceUsd: 4060, perNightUsd: 2030, pricePerSqmPerNightUsd: 112, pricePerSqmTotalUsd: 254, stablingMode: "多数夜晚停靠非洲原野小站过夜", allInclusive: true, url: "https://rovos.com/" },
  { rank: 4, name: "Tren Al Ándalus (安达卢西亚之星号)", country: "西班牙", operator: "Renfe", route: "塞维利亚 ↔ 格拉纳达/科尔多瓦/隆达 (7天6晚)", cabin: "Grand Class (6.5㎡) / Deluxe Suite (8.5–10㎡)", areaSqm: 9.25, totalPriceUsd: 7600, perNightUsd: 1267, pricePerSqmPerNightUsd: 137, pricePerSqmTotalUsd: 822, stablingMode: "100% 每晚停站过夜", allInclusive: true, url: "https://www.renfe.com/es/en/experiencias/viajes-de-lujo/tren-al-andalus" },
  { rank: 5, name: "Deccan Odyssey / Golden Chariot (德干奥德赛/金色战车)", country: "印度", operator: "IRCTC", route: "孟买/德里/班加罗尔环线 (7晚8天)", cabin: "Deluxe Cabin (8.8㎡, 独立卫浴)", areaSqm: 8.8, totalPriceUsd: 8330, perNightUsd: 1190, pricePerSqmPerNightUsd: 135, pricePerSqmTotalUsd: 947, stablingMode: "夜间转场 + 核心站停靠过夜", allInclusive: true, url: "https://www.irctctourism.com/" },
  { rank: 6, name: "El Expreso de La Robla (拉罗夫拉快车)", country: "西班牙", operator: "Renfe", route: "毕尔巴鄂 ↔ 莱昂 (3天2晚 / 6天5晚)", cabin: "Standard Compartment (约3.8㎡含独立干湿分离卫浴, 卧区2.1㎡)", areaSqm: 3.8, totalPriceUsd: 1245, perNightUsd: 622, pricePerSqmPerNightUsd: 164, pricePerSqmTotalUsd: 328, stablingMode: "100% 每晚停站过夜", allInclusive: true, url: "https://www.renfe.com/es/en/experiencias/viajes-de-lujo/expreso-de-la-robla" },
  { rank: 7, name: "Maharajas' Express (王公快车)", country: "印度", operator: "IRCTC", route: "德里 ↔ 阿格拉 ↔ 斋浦尔/孟买 (3晚/6晚)", cabin: "Deluxe Cabin (10.4㎡) / Presidential Suite (41.6㎡)", areaSqm: 10.4, totalPriceUsd: 5450, perNightUsd: 1817, pricePerSqmPerNightUsd: 175, pricePerSqmTotalUsd: 524, stablingMode: "夜间转场 + 名城停站", allInclusive: true, url: "https://www.the-maharajas.com/" },
  { rank: 8, name: "Costa Verde Express (绿海岸快车)", country: "西班牙", operator: "Renfe", route: "毕尔巴鄂 ↔ 圣地亚哥 (6天5晚)", cabin: "Grand Class Suite (5.5㎡, 独立卫浴)", areaSqm: 5.5, totalPriceUsd: 5100, perNightUsd: 1020, pricePerSqmPerNightUsd: 185, pricePerSqmTotalUsd: 927, stablingMode: "100% 每晚停站过夜", allInclusive: true, url: "https://www.renfe.com/es/en/experiencias/viajes-de-lujo/costa-verde-express" },
  { rank: 9, name: "VIA Rail The Canadian (加拿大人号 Prestige 舱)", country: "加拿大", operator: "VIA Rail", route: "温哥华 ↔ 多伦多 (5天4晚)", cabin: "Prestige Sleeper (7.6㎡, 大窗+独立淋浴卫浴+酒水管家)", areaSqm: 7.6, totalPriceUsd: 6500, perNightUsd: 1625, pricePerSqmPerNightUsd: 214, pricePerSqmTotalUsd: 855, stablingMode: "全程夜间行驶", allInclusive: true, url: "https://www.viarail.ca/" },
  { rank: 10, name: "The Ghan / Indian Pacific (甘号 / 印度洋太平洋号)", country: "澳大利亚", operator: "Journey Beyond", route: "阿德莱德 ↔ 达尔文 / 悉尼 ↔ 珀斯 (2–3晚)", cabin: "Gold Twin (3.6㎡) / Platinum (6.5㎡)", areaSqm: 6.5, totalPriceUsd: 4950, perNightUsd: 1650, pricePerSqmPerNightUsd: 254, pricePerSqmTotalUsd: 762, stablingMode: "全程夜间行驶(白天下车游览)", allInclusive: true, url: "https://www.journeybeyondrail.com.au/" },
  { rank: 11, name: "Eastern & Oriental Express (亚洲东方快车)", country: "新加坡/马来西亚", operator: "Belmond", route: "新加坡 ↔ 槟城/兰卡威/国家公园 (4天3晚)", cabin: "Pullman (5.8㎡) / State (7.8㎡) / Presidential (11.6㎡)", areaSqm: 5.8, totalPriceUsd: 5150, perNightUsd: 1717, pricePerSqmPerNightUsd: 296, pricePerSqmTotalUsd: 888, stablingMode: "夜间行驶 + 站点停靠", allInclusive: true, url: "https://www.belmond.com/trains/asia/eastern-and-oriental-express/" },
  { rank: 12, name: "Belmond Andean Explorer (安第斯探险家号)", country: "秘鲁", operator: "Belmond", route: "库斯科 ↔ 的的喀喀湖 ↔ 阿雷基帕 (1–2晚)", cabin: "Bunk (5.5㎡) / Twin (7.5㎡) / Suite (13.1㎡)", areaSqm: 7.5, totalPriceUsd: 4600, perNightUsd: 2300, pricePerSqmPerNightUsd: 307, pricePerSqmTotalUsd: 613, stablingMode: "100% 每晚停站过夜(高原湖畔/侧线)", allInclusive: true, url: "https://www.belmond.com/trains/south-america/peru/belmond-andean-explorer/" },
  { rank: 13, name: "Royal Scotsman (皇家苏格兰人号)", country: "英国·苏格兰", operator: "Belmond", route: "爱丁堡 ↔ 苏格兰高地环线 (2–7晚)", cabin: "Twin/Double (5.5㎡) / Grand Suite (8㎡)", areaSqm: 5.5, totalPriceUsd: 5800, perNightUsd: 2900, pricePerSqmPerNightUsd: 527, pricePerSqmTotalUsd: 1055, stablingMode: "100% 每晚停靠高地无人小站过夜", allInclusive: true, url: "https://www.belmond.com/trains/europe/scotland/belmond-royal-scotsman/" },
  { rank: 14, name: "Venice Simplon-Orient-Express (VSOE 威尼斯辛普朗东方快车)", country: "欧洲跨国", operator: "Belmond", route: "巴黎 ↔ 威尼斯 (2天1晚)", cabin: "Historic Twin (3.6㎡, 公卫) / Suite (7.2㎡, 独卫)", areaSqm: 3.6, totalPriceUsd: 4850, perNightUsd: 4850, pricePerSqmPerNightUsd: 1347, pricePerSqmTotalUsd: 1347, stablingMode: "全程夜间行驶", allInclusive: false, url: "https://www.belmond.com/trains/europe/venice-simplon-orient-express/" }
];

// 2. 日本 5 大豪华及定期过夜卧铺列车
window.JAPAN_LUXURY_AND_SLEEPER_TRAINS = [
  { name: "ななつ星 in 九州 (九州七星号 Seven Stars in Kyushu)", operator: "JR九州", route: "九州周游 1晚2天 / 3晚4天", cabin: "Suite (10㎡) / DX Suite B (17㎡) / DX Suite A (21㎡)", areaSqm: "10–21", pricePerNightUsd: "2556–6000", pricePerSqmPerNightUsd: "164–433", stablingMode: "深夜常停靠阿苏站/由布院站过夜", bookingMode: "抽签制 (中签率 <5%)" },
  { name: "TRAIN SUITE 四季島 (Shiki-shima)", operator: "JR东日本", route: "东日本/北海道 1–3晚", cabin: "Suite (9㎡) / Deluxe (15㎡) / 四季岛复式套房 (20㎡)", areaSqm: "9–20", pricePerNightUsd: "1890–4330", pricePerSqmPerNightUsd: "128–274", stablingMode: "夜间行驶 + 清晨观景站(如姨舍站)停靠", bookingMode: "抽签制" },
  { name: "TWILIGHT EXPRESS 瑞風 (Mizukaze)", operator: "JR西日本", route: "山阴/山阳 1晚2天 / 2晚3天", cabin: "Royal Twin (10.5㎡) / The Suite 独占整节车厢 (35㎡)", areaSqm: "10.5–35", pricePerNightUsd: "2165–6400", pricePerSqmPerNightUsd: "133–229", stablingMode: "夜间行驶 + 凌晨东滨站等观景停靠", bookingMode: "抽签制" },
  { name: "THE ROYAL EXPRESS (皇家快车)", operator: "东急 × JR", route: "伊豆/北海道/四国 3晚4天", cabin: "白天奢华餐车 + 晚间住三养庄/坐忘林等顶级温泉名宿", areaSqm: 60, pricePerNightUsd: "1667–2556", pricePerSqmPerNightUsd: "30–45", stablingMode: "晚间下车住顶级温泉旅馆", bookingMode: "预约/抽签" },
  { name: "サンライズ瀬戸・出雲 (Sunrise Seto / Izumo)", operator: "JR西日本 / JR东海", route: "东京 ↔ 高松 / 出云市 (定期每晚1班)", cabin: "Nobi-nobi通铺 / Solo / Single / Sunrise Twin / Single Deluxe", areaSqm: "1.8–4.8", pricePerNightUsd: "98–195", pricePerSqmPerNightUsd: "40–75", stablingMode: "夕发朝至定期夜车", bookingMode: "提前1个月10:00抢票" }
];

// 3. 美国 Amtrak 热门风景卧铺线路（扣除恶劣天气季后 Low Bucket 最低价）
window.AMTRAK_POPULAR_SLEEPER_ROUTES = [
  { route: "California Zephyr 加州微风号 (精华段: 旧金山 ↔ 丹佛)", nights: 1, bestSeason: "4–6月、9–10月金秋", roomette1pUsd: 480, roomette2pPerPersonUsd: 305, bedroom1pUsd: 980, bedroom2pPerPersonUsd: 555, pricePerSqmPerNightUsd: "132–169" },
  { route: "California Zephyr 加州微风号 (全程: 旧金山 ↔ 芝加哥)", nights: 2, bestSeason: "4–6月、9–10月", roomette1pUsd: 809, roomette2pPerPersonUsd: 556, bedroom1pUsd: 2229, bedroom2pPerPersonUsd: 1266, pricePerSqmPerNightUsd: "132–151" },
  { route: "Coast Starlight 海岸星光号 (洛杉矶 ↔ 西雅图)", nights: 1, bestSeason: "4–10月全季", roomette1pUsd: 540, roomette2pPerPersonUsd: 345, bedroom1pUsd: 1150, bedroom2pPerPersonUsd: 650, pricePerSqmPerNightUsd: "155–164" },
  { route: "Empire Builder 帝国建造者号 (芝加哥 ↔ 西雅图/冰川公园)", nights: 2, bestSeason: "5月中–6月、9月 (日照长且避开7-8月高价桶)", roomette1pUsd: 809, roomette2pPerPersonUsd: 556, bedroom1pUsd: 2229, bedroom2pPerPersonUsd: 1266, pricePerSqmPerNightUsd: "132–151" },
  { route: "Southwest Chief 西南酋长号 (芝加哥 ↔ 洛杉矶)", nights: 2, bestSeason: "4–5月、9–10月 (避开盛夏沙漠酷暑)", roomette1pUsd: 809, roomette2pPerPersonUsd: 555, bedroom1pUsd: 2229, bedroom2pPerPersonUsd: 1266, pricePerSqmPerNightUsd: "132–151" },
  { route: "Crescent / Silver Meteor 新月号/银星号 (纽约 ↔ 新奥尔良/迈阿密)", nights: 1, bestSeason: "3–5月、10–11月", roomette1pUsd: 657, roomette2pPerPersonUsd: 474, bedroom1pUsd: 1502, bedroom2pPerPersonUsd: 896, pricePerSqmPerNightUsd: "213–226" }
];

// 4. 俄罗斯国铁 (RZD) 2人包间卧铺 (СВ 一等平铺 vs. Люкс VIP 独立卫浴高包)
window.RUSSIA_RZD_2BERTH_SLEEPERS = [
  { route: "莫斯科 ↔ 圣彼得堡 (普通夜车)", nights: 1, cabinType: "СВ 一等2人平铺 (3.6㎡, 公卫)", rubPrice: "7,500–11,000 ₽/人", usdPerPersonPerNight: "79–116", usdPerSqmPerNight: "22–32" },
  { route: "莫斯科 ↔ 圣彼得堡 (旗舰《红箭号》/《Grand Express》)", nights: 1, cabinType: "СВ 一等2人平铺 (3.8–4㎡) / Люкс VIP 独立淋浴大床包厢 (5.5–7㎡)", rubPrice: "СВ: 13,500–22,000 ₽/人 | Люкс: 38,000–65,000 ₽/整间(可住2人)", usdPerPersonPerNight: "СВ: 142–230 | Люкс双人分摊: 200–342", usdPerSqmPerNight: "33–58" },
  { route: "莫斯科 ↔ 喀山 / 索契 / 摩尔曼斯克", nights: 1, cabinType: "СВ (3.8㎡) / Люкс VIP (5.5㎡, 独卫)", rubPrice: "СВ: 9,500–18,000 ₽/人 | Люкс: 35,000–55,000 ₽/整间", usdPerPersonPerNight: "СВ: 100–140 | Люкс双人分摊: 185–265", usdPerSqmPerNight: "26–48" },
  { route: "西伯利亚大铁路精华段: 莫斯科 ↔ 伊尔库茨克/贝加尔湖 (《001/002 俄罗斯号》)", nights: 4, cabinType: "СВ 一等2人平铺 (3.8㎡, 新车厢带免费淋浴间)", rubPrice: "42,000–62,000 ₽/人 (全程)", usdPerPersonPerNight: "110–165", usdPerSqmPerNight: "29–43" },
  { route: "西伯利亚大铁路全程: 莫斯科 ↔ 符拉迪沃斯托克/海参崴 (《001/002 俄罗斯号》)", nights: 7, cabinType: "СВ 一等2人平铺 (3.8㎡, 新车厢带免费淋浴间)", rubPrice: "75,000–110,000 ₽/人 (全程7晚)", usdPerPersonPerNight: "113–165", usdPerSqmPerNight: "30–43" }
];

// 5. 除中俄外全球“干净整洁且价格实惠”的 6 大卧铺火车体系
window.CLEAN_AFFORDABLE_SLEEPERS_EX_CN_RU = [
  { country: "芬兰", train: "VR Santa Claus Express (圣诞老人特快双层夜车)", route: "赫尔辛基 ↔ 罗瓦涅米 (1晚)", cleanliness: "★★★★★", cabin: "下层2人包厢(公卫) / 上层2人包厢(标配独立淋浴卫生间)", usdPerPersonPerNight: "下层: $42–$65 | 上层独卫: $65–$90", highlight: "北欧极简洁净，不到$70住进带独立淋浴的双层铝合金包厢" },
  { country: "泰国", train: "SRT 中车长客造 CNR 不锈钢红丝绒新列车 (9/10/25/26/31/32次)", route: "曼谷 ↔ 清迈 / 合艾 / 廊开 (1晚)", cleanliness: "★★★★☆", cabin: "一等2人独立软卧(车厢带热水淋浴) / 二等空调帘幕卧铺", usdPerPersonPerNight: "一等2人: $43–$49 (单人包整间$72) | 二等: $25–$31", highlight: "全车禁烟禁酒、乘务员当面拆封雪白消杀床品现铺" },
  { country: "乌兹别克斯坦 & 哈萨克斯坦", train: "乌铁宽轨软卧 & 哈铁 Talgo 摆式高速卧铺", route: "塔什干 ↔ 布哈拉 / 希瓦；阿拉木图 ↔ 阿斯塔纳 (1晚)", cleanliness: "★★★★☆", cabin: "一等2人平铺 СВ / Talgo Luxe", usdPerPersonPerNight: "乌铁СВ: $28–$48 | 哈铁Talgo: $38–$65", highlight: "完整继承俄铁一车一乘务员保洁制度，票价仅俄铁1/3" },
  { country: "奥地利 / 捷克 / 中欧", train: "ÖBB 新一代 Nightjet & 中欧 EuroNight / RegioJet", route: "维也纳/慕尼黑 ↔ 罗马/阿姆斯特丹；布拉格 ↔ 布达佩斯/华沙", cleanliness: "★★★★★", cabin: "单人太空舱 Mini Cabin / 新一代独卫2人包厢 / EuroNight Double", usdPerPersonPerNight: "RegioJet: $27–$49 | 胶囊: $64–$96 | 独卫包厢: $90–$180", highlight: "2024–2026全新西门子科技车厢，含次日现泡咖啡与欧陆早餐" },
  { country: "阿塞拜疆 & 格鲁吉亚", train: "Stadler 瑞士造豪华卧铺 & 南高加索铁路", route: "第比利斯 ↔ 巴统 / 埃里温 / 巴库", cleanliness: "★★★★☆", cabin: "一等2人软卧 SV", usdPerPersonPerNight: "$35–$55", highlight: "瑞士 Stadler 定制新车，直接对标瑞铁与俄铁最高标准" },
  { country: "日本", train: "Sunrise 出云 / 濑户号 (サンライズ出雲・瀬戸)", route: "东京 ↔ 出云市 / 高松 (1晚)", cleanliness: "★★★★★+", cabin: "Nobi-nobi木地板平躺位 / Solo & Single & Twin 独立木质包厢", usdPerPersonPerNight: "通铺: $98 | 独立包厢: $145–$155", highlight: "住宅级木质静谧包厢，洁癖级卫生水准" }
];

// 6. 中国近年 8 大豪华旅游专列价格、配置与口碑排行
window.CHINA_LUXURY_TRAINS_RANKING = [
  { name: "《丝路梦享号》 (Silk Road Express)", launchYear: 2024, operator: "复星旅文 / 星景旅游 (HBA+清华美院设计)", route: "青甘线(西宁↔敦煌 4晚5天) / 南疆塔里木环线(5–7晚)", cabinAreaSqm: "11㎡(长乐居) / 22㎡(锦绣未央套房)", allEnSuiteBathroom: true, totalPriceRmb: "24,999–35,999", perNightRmb: "6,250–9,000", perNightUsd: "880–1265", stablingMode: "70%夜间赶路 + 30%凌晨到站静止补觉", rating: "★★★★☆", verdict: "国内硬件、审美与Fine Dining服务天花板，全程睡火车+VIP考斯特短驳，免去北疆大巴拉练" },
  { name: "《呼伦贝尔号》 (Hulunbuir Express)", launchYear: 2022, operator: "星景旅游", route: "海拉尔 ↔ 阿尔山 / 根河 / 漠河 (4晚5天)", cabinAreaSqm: "8.5–13.5㎡", allEnSuiteBathroom: true, totalPriceRmb: "21,999–29,999", perNightRmb: "5,500–7,500", perNightUsd: "775–1055", stablingMode: "夜间常停靠原始森林安静小站过夜", rating: "★★★★☆", verdict: "全车仅22间房限44人，私密性最佳，国内最接近“夜间停站睡觉”的森林慢火车" },
  { name: "《星光·澜湄号》 (Starlight Lancang-Mekong)", launchYear: 2024, operator: "中国旅游集团 CTG (中旅星光)", route: "昆明 ↔ 西双版纳 ↔ 老挝琅勃拉邦/万象 (5–6晚)", cabinAreaSqm: "10–20㎡+", allEnSuiteBathroom: true, totalPriceRmb: "26,800–39,800", perNightRmb: "4,500–6,600", perNightUsd: "630–930", stablingMode: "夜间行驶 + 跨境站点停靠", rating: "★★★★☆", verdict: "唯一中老铁路跨境顶奢专列，通关免排队，法餐与滇味融合" },
  { name: "第三代《熊猫专列·成都号》", launchYear: 2025, operator: "成都铁路局 + 高星酒店管理", route: "新疆南北疆全景大环线 (15晚16天)", cabinAreaSqm: "8–10㎡ (悠然居/诗意居)", allEnSuiteBathroom: true, totalPriceRmb: "55,999–69,999", perNightRmb: "3,730–4,660", perNightUsd: "525–655", stablingMode: "住火车的6晚100%夜间赶路，其余9晚住陆地酒店(配2+1航空座椅大巴)", rating: "★★★★★", verdict: "全车54间房100%标配独立干湿分离卫浴，目前跑16天南北疆全景线综合口碑第一" },
  { name: "《新东方快车》· 金钻包厢", launchYear: 2020, operator: "乌鲁木齐局车底 + 多旅行社切包", route: "新疆南北疆大环线 (12–14晚)", cabinAreaSqm: "10㎡ (大床+独立卫浴)", allEnSuiteBathroom: true, totalPriceRmb: "48,999–69,999", perNightRmb: "3,800–5,000", perNightUsd: "535–705", stablingMode: "住火车的4–5晚夜间赶路，其余8–10晚住陆地酒店", rating: "★★★☆☆", verdict: "金钻包厢硬件优秀，但因多旅行社切包分销，地接大巴与团餐水准需挑高端包舱社" },
  { name: "《新东方快车》· 蓝钻/银钻包厢 (避坑重点)", launchYear: 2020, operator: "乌鲁木齐局车底 + 多旅行社切包", route: "新疆南北疆大环线 (12–14晚)", cabinAreaSqm: "4.8㎡ (上下铺，无独立卫生间！)", allEnSuiteBathroom: false, totalPriceRmb: "29,999–42,999", perNightRmb: "2,300–3,300", perNightUsd: "325–465", stablingMode: "同上", rating: "★★☆☆☆", verdict: "花三四万块钱仍需去走廊两端排队用公用卫生间和淋浴间，高低混编槽点重灾区" },
  { name: "《林都号》 (Lindu Express)", launchYear: 2023, operator: "伊春森工集团 + 哈尔滨局", route: "哈尔滨 ↔ 伊春小兴安岭森林环线 (4–6晚)", cabinAreaSqm: "10–12㎡", allEnSuiteBathroom: true, totalPriceRmb: "15,999–25,999", perNightRmb: "3,200–4,500", perNightUsd: "450–635", stablingMode: "夜间常停靠小兴安岭林区车站过夜", rating: "★★★☆☆", verdict: "全车30间房100%独立卫浴，配中医馆与乐队酒吧车，夜间停站睡眠好" },
  { name: "《中原铁道·大河之南号》", launchYear: 2025, operator: "郑州铁路局", route: "河南/云贵/新疆适老化轻奢线 (8–14晚)", cabinAreaSqm: "6–10㎡", allEnSuiteBathroom: true, totalPriceRmb: "18,000–32,000", perNightRmb: "2,000–3,200", perNightUsd: "280–450", stablingMode: "夕发朝至 + 站点停靠", rating: "★★★☆☆", verdict: "2025新下线全车独立卫浴适老化专列，适合带长辈出行" }
];

// 7. 中国普通卧铺火车平稳度与舒适度终极排行
window.CHINA_SLEEPER_STABILITY_RANKING = [
  { rank: 1, model: "双层「纵向动卧」 CRH2E-NG (250 km/h)", sampleTrains: "D901 / D902 / D903 / D904 (北京西 ↔ 深圳北)", trackType: "高铁无砟无缝轨道", summary: "床位顺着铁轨方向纵向布置，加减速与过弯身体完全不滚晃，每铺独立拉帘小单间，全国防晃防晕第1名" },
  { rank: 2, model: "复兴号高速智能动卧 CR400AF-AE (250 km/h)", sampleTrains: "D909 / D910 (北京西 ↔ 香港西九龙)、D913 / D914 (上海虹桥 ↔ 香港)", trackType: "高铁无砟无缝轨道", summary: "2024–2025全新投运，气密隔音降噪与减震再升级，启停0顿挫" },
  { rank: 3, model: "常规横向高铁动卧 CRH1E / CRH2E (250 km/h)", sampleTrains: "D9xx 次京广深港、沪深线", trackType: "高铁无砟无缝轨道", summary: "动力分散式0前后冲动；CRH1E配有国内唯一带独立沙发与房内独卫的2人高级动卧包厢" },
  { rank: 4, model: "Z字头 · 庞巴迪合资车底 BSP 25T (160 km/h)", sampleTrains: "部分京沪(Z1–Z22)、京哈、进藏Z字头软卧/高包", trackType: "既有线有砟轨道", summary: "采用进口空气弹簧转向架，在所有机车牵引Z字头里平稳度最佳" },
  { rank: 5, model: "普通国产 Z字头 (25T) & 三代白绿动集 (CR200J3-C)", sampleTrains: "全国大多数Z字头及2024后新款D字头动集", trackType: "既有线有砟轨道", summary: "匀速尚可，但进出站加减速纵向顿挫与过道岔左右甩尾明显" },
  { rank: 6, model: "初代“绿巨人”假动卧 (CR200J 1.0) & T/K字头 (25K/25G)", sampleTrains: "普通两位数/三位数D字头绿皮动集、特快/快速", trackType: "既有线有砟轨道", summary: "机车牵引改装普速车底，减震偏硬、过弯摇晃与轮轨噪音明显" }
];

// 8. 全球内河游轮、运河游船与日本本土豪华邮轮核心汇总
window.GLOBAL_RIVER_AND_LUXURY_CRUISES = {
  sixRiversTopTierBenchmark: [
    { river: "中国长江三峡", ship: "长江探索号 (Yangzi Explorer, 2025新船)", cabinSqm: 31, nights: 3, lowSeasonTotalUsd: 970, perNightUsd: 323, pricePerSqmPerNightUsd: 10.4, note: "全船100% 31㎡起阳台套房+1:1配比+一价全包，价格仅为全球同级顶奢河轮的1/3" },
    { river: "欧洲多瑙河 / 莱茵河", ship: "Viking (维京长船) / AmaWaterways / Riverside", cabinSqm: "13–25", nights: 7, lowSeasonTotalUsd: 1999, perNightUsd: 285, pricePerSqmPerNightUsd: "18–22", note: "Viking美国官网11月低至$1,999/7晚($285/晚)；维京中国官网全中文一价全包低至¥19,888/7晚($397/晚)；真顶奢Riverside/Tauck约$600–$850/晚" },
    { river: "埃及尼罗河 (5大档次)", ship: "本土5星船($85/晚) → Mövenpick($260/晚) → A&K Sun Boat IV($631/晚) → Oberoi Zahra/Philae($819/晚)", cabinSqm: "18–36", nights: 4, lowSeasonTotalUsd: "340–3275", perNightUsd: "85–819", pricePerSqmPerNightUsd: "5–23", note: "尼罗河淡旺季差价高达2.5倍；Oberoi 5–8月淡季36㎡大舱含税仅$819/晚，10–4月旺季跳至$1,797/晚" },
    { river: "美国密西西比河", ship: "Viking Mississippi / American Cruise Lines (ACL)", cabinSqm: "25–30", nights: 7, lowSeasonTotalUsd: 3999, perNightUsd: 571, pricePerSqmPerNightUsd: "20–23", note: "受美国《客船服务法(PVSA)》保护无廉价外籍船，全球门槛最高的内河游轮($571–$725/晚起)" },
    { river: "缅甸伊洛瓦底江", ship: "Sanctuary Ananda / Pandaw", cabinSqm: "24–28", nights: 4, lowSeasonTotalUsd: 2200, perNightUsd: 550, pricePerSqmPerNightUsd: "20–23", note: "全阳台柚木套房，受局势影响航次极少" }
  ],
  japanDomesticLuxuryCruises: [
    { tier: "T1 濑户内海顶奢漂浮旅馆", ship: "guntû (ガンツウ)", tonnage: 3200, pax: 38, cabinSqm: "50–90", perNightUsd: "1667–3500", pricePerSqmPerNightUsd: "33–39", note: "堀部安嗣设计全桧木19间套房，一价全包米其林级寿司怀石与酒水，免抽签" },
    { tier: "T2 日本邮船全新旗舰 (2025.7首航)", ship: "飛鳥III (Asuka III)", tonnage: 52200, pax: 740, cabinSqm: "22–114.8", perNightUsd: "630–3330", pricePerSqmPerNightUsd: "24–39", note: "100%全阳台套房，设6家餐厅与顶层露天温泉" },
    { tier: "T2 商船三井全套房船 (原Seabourn世邦顶奢船)", ship: "MITSUI OCEAN FUJI (三井海洋富士) & SAKURA (樱花)", tonnage: 32477, pax: 458, cabinSqm: "28–110", perNightUsd: "631–1742", pricePerSqmPerNightUsd: "20–28", note: "28㎡全套房起跳，船票已全包酒水畅饮、免小费及半日岸上观光，日本本土豪船性价比冠军" },
    { tier: "T2 日本邮船经典王牌", ship: "飛鳥II (Asuka II)", tonnage: 50444, pax: 872, cabinSqm: "18.4–88.2", perNightUsd: "450–2127", pricePerSqmPerNightUsd: "24–29", note: "免费注册My ASUKA CLUB享9折，叠加日本邮船股东优待券可再享9折" },
    { tier: "T3 外资日本母港平价大船对照", ship: "Diamond Princess (钻石公主号)", tonnage: 115875, pax: 2670, cabinSqm: "15–50", perNightUsd: "100–220", pricePerSqmPerNightUsd: "6–10", note: "三菱重工造，配海上最大日式露天温泉Izumi" }
  ]
};

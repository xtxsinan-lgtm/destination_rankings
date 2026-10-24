#!/usr/bin/env python3
"""
Builds data_cruises_top50.js and rankings/cruises_top50.md focused on the Global Top 50 High-End Cruises,
using the user's '游轮数据' sheet quantitative method (Space = Tonnage/Pax, Service = Crew/Pax, SheetTotal = Space/10 + Service*10)
combined with 6 evaluation dimensions (人均Tonnage, Crew乘客比, 房间大小, 餐饮水准, 船上活动水准, 邮轮设计)
and Next-12-Months Lowest Price (2026.11 - 2027.10).
"""
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Format of each entry tuple:
# (id, name, brand, domain, region, tonnageNum, pax, crew,
#  entrySuiteName, suiteSqm, roomScore,
#  diningScore, diningHighlight,
#  activityScore, activityHighlight,
#  designScore, designHighlight,
#  lowestPriceUsd, lowestNights, verifiedSailing, allInclusiveLevel,
#  highlight, tip, url, lat, lon, wiki_q, preset_img)

RAW_CRUISES = [
    ("orient-express-corinthian", "东方快车·科林斯号 / 静海号 (Orient Express Corinthian / Silenseas)", "Orient Express 雅高东方快车", "顶奢风帆与高定超级游艇", "地中海 / 里维埃拉 / 加勒比",
     25600, 108, 170, "Signature Suite 全海景高定套房 (70㎡)", 70.0, 10.0,
     10.0, "米其林三星主厨 Yannick Alléno 领衔5间高定餐厅与1920年代秘密酒吧",
     9.4, "220米全球最大SolidSail硬翼风帆航行、黑胶录音棚、私享海滩俱乐部与艺术沙龙",
     10.0, "建筑大师 Maxime d'Angeac 操刀，把百年东方快车装饰艺术搬上2.56万吨风帆巨舰",
     17500, 5, "2026-11-14 巴塞罗那–马赛 5晚 ($17,500 起)", "一价全包(米其林餐饮+香槟+管家+小费)",
     "人均吨位 237.04 GT、船员乘客比 1.57，《邮轮数据》表硬件分 39.44 断层第一 + 米其林三星 Yannick Alléno 坐镇 + 70㎡ 起步套房",
     "全球公认空间比最夸张的船（25,600吨仅载108人），春季与深秋地中海5晚短航次是体验它的最低门槛。",
     "https://www.orient-express.com/sailing-yachts/", 43.73, 7.42, "Orient Express Corinthian",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/OE_Corinthian.jpg/1280px-OE_Corinthian.jpg"),

    ("four-seasons-i-yacht", "四季超级游艇·Four Seasons I", "Four Seasons Yachts 四季游艇", "顶奢风帆与高定超级游艇", "加勒比 / 地中海 / 爱琴海",
     34000, 195, 210, "Seaview / Tenerife Suite 海景露台套房 (50㎡)", 50.0, 9.9,
     9.8, "11间四季传奇餐厅与雪茄香槟酒廊（含地中海海鲜、日式Omakase与鱼子酱吧）",
     9.5, "船尾横向贯穿式海水泳池平台（Marina Day）可直通皮划艇、水翼冲浪板与超级游艇玩具",
     10.0, "Prosper Assouline 与 Tillberg Design 操刀，全落地弧形玻璃幕墙与可无限打通的模块化套房",
     19500, 5, "2026-12-05 安提瓜–圣巴茨 5晚 ($19,500 起)", "含早餐与海上运动平台(正餐单点)",
     "人均吨位 174.36 GT、船员乘客比 1.08，表格硬件分 28.21 + 50㎡ 起步全落地窗套房 + 980㎡ 四层漏斗顶层套房",
     "船上无传统自助餐厅，更像一座漂浮在圣巴茨与波托菲诺之间的四季高定私家庄园。",
     "https://www.fourseasonsyachts.com/", 17.90, -62.83, "Four Seasons I Yacht",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Four_Seasons_I_Yacht.jpg/1280px-Four_Seasons_I_Yacht.jpg"),

    ("quark-50-years-of-victory", "夸克极地·胜利50周年号核动力破冰船 (50 Years of Victory)", "Quark Expeditions 夸克探险", "重型破冰与奢华极地科考", "北极点 90°N 破冰直达",
     23439, 128, 140, "Standard Twin / Arktika Suite 极地外舱 (22㎡)", 22.0, 7.6,
     8.5, "极地高热量欧陆主厨正餐、俄罗斯鱼子酱伏特加北极点庆功宴与24小时暖饮站",
     10.0, "搭载自备米-2/米-8直升机冰上航拍、北极点90°N系留热气球升空、冰海跳水与北极熊追踪",
     9.2, "75,000马力双核反应堆 Arktika 级重型破冰船，勺形船首可碾碎 2.8 米厚多年坚冰",
     31995, 12, "2027-07-12 摩尔曼斯克–北极点90°N 12晚 ($31,995 起)", "一价全包(含直升机巡航+破冰+餐饮)",
     "人均吨位 183.12 GT、船员比 1.09，表格硬件分高达 29.25 + 7.5万马力双核动力直接推平3米厚北极冰盖",
     "这是人类历史上唯一能把普通商业游客带到地理北极点（90°N）并在冰面上拉手绕地球一圈的核动力巨兽。",
     "https://www.quarkexpeditions.com/", 90.0, 0.0, "50 Let Pobedy icebreaker", ""),

    ("ponant-commandant-charcot", "庞洛·夏古船长号极地破冰船 (Le Commandant Charcot)", "Ponant 庞洛邮轮", "重型破冰与奢华极地科考", "地理北极点 / 南极威德尔海 / 罗斯海",
     31283, 270, 187, "Prestige Stateroom 全阳台套房 (25㎡)", 25.0, 8.9,
     9.9, "全球唯一海上 Alain Ducasse（阿兰·杜卡斯）米其林法餐厅 Nuna + 蓝泻湖露天恒温酒吧",
     10.0, "PC2级气电混合重型破冰（直抵北极点与帝企鹅栖息地）、极地冰上徒步、冰钓与随船科研实验室",
     9.8, "Jean-Michel Wilmotte 与 Studio Jean-Philippe Nuel 操刀法式高定极简室内设计，船尾露天地热火盆",
     14890, 10, "2027-05-06 雷克雅未克–东格陵兰冰原 10晚 ($14,890 起)", "一价全包(阿兰·杜卡斯法餐+香槟+冲锋衣+科考)",
     "人均吨位 115.86 GT、表格硬件分 18.51 + PC2级重型破冰船体 + 阿兰·杜卡斯海上法餐，极地奢华与硬核科考的终极合体",
     "参考您的《南极游轮》表（12天参考价 $18,770），若选5月冰岛–格陵兰10晚航次，最低 $14,890 即可体验这艘造价4亿欧元的破冰神船。",
     "https://us.ponant.com/", -65.2, -64.1, "Le Commandant Charcot",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Le_Commandant_Charcot_Stockholm.jpg/1280px-Le_Commandant_Charcot_Stockholm.jpg"),

    ("silversea-silver-endeavour", "银海·奋进号极地全套房科考船 (Silversea Silver Endeavour)", "Silversea 银海邮轮", "重型破冰与奢华极地科考", "南极飞航直达 (Fly-Cruise) / 北极斯瓦尔巴",
     20649, 200, 209, "Classic / Superior Veranda Suite 管家阳台套房 (33㎡)", 33.2, 9.4,
     9.6, "La Dame 法式名庄餐厅、Il Terrazzino 意式料理、The Grill 热石烧烤与全天候套房鱼子酱送餐",
     9.8, "PC6级最高极地冰级、20艘Zodiac冲锋艇、远距离万向稳定变焦摄像系统与飞跃德雷克海峡南极直飞",
     9.6, "原水晶奋进号（Crystal Endeavor）耗资数亿欧元打造，双层挑高玻璃日光泳池厅在南极冰山间宛如水晶宫",
     11900, 6, "2026-12-08 乔治王岛飞航南极大桥 (Antarctica Bridge) 6晚 ($11,900 起)", "一价全包(商务舱包机直飞南极+私人管家+冲锋艇+酒水)",
     "人均吨位 103.25 GT、船员乘客比 1.045，表格硬件分 20.77 + 33㎡全阳台管家套房，南极奢华科考空间之王",
     "完美继承原水晶邮轮血统，搭配银海 Antarctica Bridge 2小时飞越魔鬼西风带，是怕晕船又想看南极的最佳选择。",
     "https://www.silversea.com/", -62.2, -58.9, "Silver Endeavour", ""),

    ("lindblad-ng-endurance-resolution", "林德布拉德×国家地理·坚忍号 / 决心号 (NG Endurance / Resolution)", "Lindblad × National Geographic", "重型破冰与奢华极地科考", "南极半岛 / 南乔治亚岛 / 北极西北航道",
     12786, 126, 112, "Category 1-3 全景阳台舱 (20.5㎡)", 20.5, 8.3,
     9.0, "北欧极地可持续料理主餐厅 Two Seven Zero° 与主厨互动私宴桌（Chef's Table）",
     10.0, "《国家地理》摄影大师随船指导、水下ROV遥控机器人、冰上圆顶玻璃雪屋（Igloos）过夜与皮划艇",
     9.7, "革命性 Ulstein X-BOW（倒弓形船首）PC5破冰设计，劈开巨浪零拍击震动，顶层双无边热水池俯瞰冰川",
     11850, 10, "2027-05-18 斯瓦尔巴群岛北极熊巡礼 10晚 ($11,850 起；南极14天 $16,450)", "一价全包(国家地理专家+皮划艇+酒水+小费+Wi-Fi)",
     "人均吨位 101.48 GT、船员乘客比 0.89，表格硬件分 19.04 + 颠覆性的 X-BOW 抗风浪船首 + 甲板玻璃冰屋星空露营",
     "对应您《南极游轮》表第一行（12,786吨/126客/112船员，南极14天 $16,450），其X-BOW船头过德雷克海峡稳如泰山。",
     "https://www.expeditions.com/", -64.8, -62.8, "National Geographic Endurance", ""),

    ("lindblad-crystal-esprit-islander-ii", "国家地理·海岛人二号 (原水晶游艇 Crystal Esprit / NG Islander II)", "Lindblad × National Geographic", "重型破冰与奢华极地科考", "加拉帕戈斯群岛全年驻航",
     3370, 62, 93, "Islander Suite 柚木全海景套房 (26㎡)", 26.0, 8.8,
     9.2, "厄瓜多尔安第斯与太平洋鲜活海鲜零公里料理、露天烧烤甲板与精品南美葡萄酒",
     10.0, "全员随时出发的Zodiac登陆、透明底皮划艇、深潜/浮潜看双髻鲨与海鬣蜥、48客高配比博物学家带队",
     9.3, "原 Crystal Yacht Esprit 超级游艇，全套房大理石浴室与私人游艇级航海俱乐部氛围",
     8490, 6, "2026-11-19 加拉帕戈斯群岛精华环游 6晚 ($8,490 起)", "一价全包(基多往返加拉帕戈斯机票+全套房+每日双登陆)",
     "船员乘客比高达 1.50（表格数据 62客/93船员，实际加拉帕戈斯仅载48客！），表格硬件分 20.44，加拉帕戈斯最奢华探险游艇",
     "您《游轮数据》表第3行的传奇游艇 Crystal Esprit，现由国家地理收购长驻加拉帕戈斯，更因生态限额把载客进一步压到48人。",
     "https://www.expeditions.com/", -0.74, -90.31, "Crystal Esprit", ""),

    ("ritz-carlton-evrima-ilma", "丽思卡尔顿超级游艇·Evrima / Ilma / Luminara", "The Ritz-Carlton Yacht Collection", "顶奢风帆与高定超级游艇", "地中海 / 加勒比海 / 圣巴茨",
     26500, 298, 246, "Terrace Suite 全私人露台套房 (35㎡)", 35.0, 9.5,
     9.8, "米其林三星主厨 Sven Elverfeld 联名餐厅 S.E.A. / Fabio Trabocchi 联名主厨餐厅与香槟吧",
     9.2, "船尾直通大海的 Marina Beach Club、电动水翼板（Fliteboard）、帆板、无边泳池与丽思卡尔顿水疗",
     9.9, "暗黑海军蓝超级游艇流线船身，全船挑高双层 Loft 套房与私人游艇码头直接停泊波托菲诺/圣巴茨",
     4900, 7, "2026-11-28 圣胡安–芭芭多斯加勒比 7晚 ($4,900 起，约 $700/晚)", "一价全包(餐饮+名庄酒水+水玩具+Wi-Fi+小费，米其林S.E.A.除外)",
     "人均吨位 88.93 GT、船员乘客比 0.83，表格硬件分 17.15 + 35㎡全露台高挑高套房 + 未来一年加勒比7晚最低仅 $4,900",
     "正如您《加勒比游轮价格》表第1行所列（7晚 $4,900 / $700每晚），在11–12月加勒比转港或短线航次能以不到五千美金拿下丽思卡尔顿游艇！",
     "https://www.ritzcarltonyachtcollection.com/", 43.30, 6.64, "Evrima yacht",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Evrima_at_Katajanokka_Terminal%2C_Helsinki%2C_2026-07-20.jpg/1280px-Evrima_at_Katajanokka_Terminal%2C_Helsinki%2C_2026-07-20.jpg"),

    ("seabourn-venture-pursuit", "世邦·探险号 / 追寻号超奢极地游艇 (Seabourn Venture / Pursuit)", "Seabourn 世邦邮轮", "重型破冰与奢华极地科考", "南极半岛 / 西北航道 / 金伯利海岸",
     23000, 264, 239, "Veranda Suite 全海景阳台套房 (33㎡)", 33.0, 9.4,
     9.6, "The Restaurant 法式正餐、The Colonnade 露台海鲜、Sushi 日料吧与随时供应的世邦鱼子酱",
     10.0, "2艘定制360度球形视野载人潜水器（直潜300米深海）、24艘Zodiac冲锋艇、双人皮划艇与26人科学家天团",
     9.6, "奢华酒店设计大师 Adam D. Tihany 操刀，PC6极地破冰船体搭配猎鹰翼楼观察酒廊与恒温衣物烘干衣柜",
     6499, 10, "2027-04-12 里斯本–都柏林欧洲西岸 10晚 ($6,499 起；南极11晚 $10,999 起)", "一价全包(香槟鱼子酱+酒水+冲锋艇登陆+HH极地派克大衣)",
     "人均吨位 87.12 GT、船员乘客比 0.91，表格硬件分 17.77 + 33㎡全套房加热衣柜 + 双深海载人潜艇",
     "在世邦船队中《游轮数据》硬件分最高（17.77 vs Odyssey 14.63），既有PC6破冰与双潜艇，又有Adam D. Tihany设计的全套房奢享。",
     "https://www.seabourn.com/", -64.5, -62.5, "Seabourn Venture", ""),

    ("hapag-lloyd-europa-2", "赫伯罗特·欧罗巴2号 (Hapag-Lloyd MS Europa 2)", "Hapag-Lloyd Cruises 赫伯罗特", "六星全套房顶奢远洋船", "北欧峡湾 / 地中海 / 印度洋环球",
     42830, 516, 370, "Veranda / Ocean Suite 全阳台套房 (35㎡)", 35.0, 9.5,
     10.0, "连续十余年《Berlitz邮轮指南》全球最高分五星半传奇：7间零附加费名厨餐厅（Tarragon法餐/Sakura日料/Serenissima意餐）",
     9.2, "15米长海水泳池（带可开合玻璃穹顶）、高尔夫模拟器、古典室内交响音乐会与Sansibar海滩派对",
     9.6, "取消传统船长晚礼服束缚的当代德系包豪斯游艇美学，全船800余件博物馆级当代艺术品真迹",
     4690, 7, "2027-05-14 汉堡–里斯本西欧海岸 7晚 ($4,690 起)", "含7间顶级餐厅+套房迷你吧香槟(酒吧烈酒单点)",
     "人均吨位 83.00 GT、船员比 0.72，表格硬件分 15.47 + 《Berlitz》全球排名第一邮轮 + 35㎡起步全阳台套房",
     "邮轮界公认的「六星天花板」，全船最大仅载500人却拥有4.28万吨体量，人均公共空间宽敞到任何餐厅从不翻台。",
     "https://www.hl-cruises.com/", 53.54, 9.98, "MS Europa 2", ""),

    ("silversea-silver-nova-ray", "银海·新星号 / 光芒号 (Silversea Silver Nova / Silver Ray)", "Silversea 银海邮轮", "六星全套房顶奢远洋船", "地中海 / 阿拉斯加 / 加勒比",
     55051, 728, 556, "Classic / Medallion Veranda Suite (33.2㎡)", 33.2, 9.4,
     9.9, "S.A.L.T.（海陆风味实验室）目的地深度料理、La Dame 法餐、Atlantide 牛排龙虾与24小时管家鱼子酱",
     9.5, "S.A.L.T. Chef's Table 主厨料理课、Otium 古罗马纵享水疗、悬挑无边泳池与每港免费岸上观光",
     10.0, "邮轮建筑史革命：全船水平不对称设计（Asymmetrical Design），整面船舷泳池甲板无烟囱阻挡270度贴海玻璃幕墙",
     3950, 7, "2026-12-04 劳德代尔堡–圣胡安加勒比 7晚 ($3,950 起；阿拉斯加7晚 $4,450 起)", "一价全包(私人管家+酒水香槟+岸上游+小费+Wi-Fi)",
     "人均吨位 75.62 GT、船员乘客比 0.76，表格硬件分 15.20 + 革命性不对称悬挑海景泳池 + 全船100%白金管家套房",
     "银海最新一代LNG动力旗舰，船尾270度无遮挡玻璃视野的 Otium Suite 是目前远洋奢华邮轮最抢手的房型。",
     "https://www.silversea.com/", 43.73, 7.42, "Silver Nova",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Silver_nova.jpg/1280px-Silver_nova.jpg"),

    ("regent-seven-seas-splendor-grandeur", "丽晶七海·尚尊号 / 辉煌号 / 探索者号 (Seven Seas Grandeur / Splendor / Explorer)", "Regent Seven Seas 丽晶七海", "六星全套房顶奢远洋船", "地中海 / 北欧 / 加勒比 / 跨洋",
     55254, 750, 542, "Veranda / Superior Suite 全阳台套房 (28–43㎡)", 35.0, 9.5,
     9.9, "Chartreuse 现代法餐、Prime 7 干式熟成牛排、Pacific Rim 泛亚料理与无限量冷血龙虾尾/鱼子酱",
     9.6, "全包无限次岸上观光（Unlimited Shore Excursions）、海上厨艺学院（Culinary Arts Kitchen）与Serene Spa",
     9.8, "Studio DADO 操刀宫殿级室内设计：1600件毕加索真迹与Fabergé定制彩蛋、413㎡耗资千万的丽晶套房（带私人Steinway钢琴与桑拿）",
     4899, 7, "2026-11-20 迈阿密–加勒比海 7晚 ($4,899 起；10晚 $6,099 起)", "真·一价全包(无限次岸上游+全船名餐厅+酒水+小费+洗衣+Wi-Fi)",
     "人均吨位 73.67 GT、船员乘客比 0.72，表格硬件分 14.59 + 宫殿级大理石水晶灯装潢 + 连岸上观光与干洗都全包",
     "对应您《加勒比游轮价格》表中的 Regent（10晚 $6,099，约 $609.9/晚），下船结账账单真正为 $0。",
     "https://www.rssc.com/", 25.77, -80.17, "Regent Seven Seas Grandeur",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Regent_Seven_Seas_Grandeur_%2853824101578%29.jpg/1280px-Regent_Seven_Seas_Grandeur_%2853824101578%29.jpg"),

    ("scenic-eclipse-i-ii", "胜景·日蚀号 / 日蚀二号超奢探索游艇 (Scenic Eclipse I / II)", "Scenic Luxury Cruises 胜景奢华邮轮", "重型破冰与奢华极地科考", "南极半岛 / 北极格陵兰 / 澳洲金伯利",
     17545, 228, 176, "Verandah / Deluxe Verandah Suite (32–40㎡)", 34.0, 9.3,
     9.6, "多达10种美食体验：Lumière 法式高定料理（香槟吧）、Koko's 日式铁板烧/寿司吧、Night Market 与130种单一麦芽威士忌吧",
     10.0, "同时搭载2架空客 H130 超静音观光直升机 + 1艘 Scenic Neptune 7人海底潜艇 + 极地冲锋艇与立式桨板",
     9.6, "超级游艇黄金比例外型配PC6破冰船壳、GPS动态定位无锚悬停系统与550㎡ Senses 水疗中心",
     7995, 8, "2027-04-18 里斯本–巴塞罗那伊比利亚 8晚 ($7,995 起；南极12晚 $12,995 起)", "一价全包(10间餐厅+顶级威士忌香槟+私人管家+冲锋艇登陆)",
     "人均吨位 76.95 GT、船员乘客比 0.77，表格硬件分 15.41 + 双空客H130直升机与深海潜艇同船配置",
     "被誉为「007反派的超级游艇」，机库门缓缓打开升起空客直升机的场面震撼全场。",
     "https://www.scenicusa.com/", -64.8, -63.5, "Scenic Eclipse II",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Scenic_Eclipse_II_at_Fort_William_-_geograph.org.uk_-_7611925.jpg/1280px-Scenic_Eclipse_II_at_Fort_William_-_geograph.org.uk_-_7611925.jpg"),

    ("explora-i-ii-iii", "意铂奢华邮轮·Explora I / II / III", "Explora Journeys 意铂奢华邮轮", "六星全套房顶奢远洋船", "地中海 / 加勒比海 / 红海与北欧",
     63621, 922, 700, "Ocean Terrace Suite 海洋露台套房 (35㎡)", 35.0, 9.5,
     9.7, "Anthology 客座米其林主厨餐厅、Sakura 泛亚日料、Marble & Co. 欧洲熟成牛排馆、Fil Rouge 法餐与 Emporium 现开生蚝蟹腿档",
     9.2, "全船4座恒温海水泳池（含可开合天幕 Conservatory Pool）、劳力士/卡地亚/百达翡丽海上精品店与海洋音疗Spa",
     9.9, "英国游艇设计巨匠 Martin Francis 操刀，打破传统邮轮感，打造纯正欧洲「海洋之家 (Homes at Sea)」当代意式奢华",
     3640, 7, "2026-11-27 迈阿密往返东加勒比 7晚 ($3,640 起，约 $520/晚)", "一价全包(5间主厨餐厅+香槟名酒+热疗Spa+高速星链Wi-Fi+小费)",
     "人均吨位 69.00 GT、船员乘客比 0.76，表格硬件分 14.49 + 35㎡起步戴森吹风机/Frette床品大套房 + 4座无边泳池",
     "MSC Aponte家族斥资35亿欧元打造的顶奢独立品牌，也是全球唯一船上开有劳力士（Rolex）官方专卖店的邮轮。",
     "https://explorajourneys.com/", 41.89, 12.48, "Explora I",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Explora_I.jpg/1280px-Explora_I.jpg"),

    ("swan-hellenic-minerva-vega-diana", "天鹅探索·密涅瓦号 / 织女星号 / 戴安娜号 (SH Minerva / Vega / Diana)", "Swan Hellenic 天鹅探索邮轮", "重型破冰与奢华极地科考", "南极半岛 / 北极格陵兰 / 非洲西海岸",
     10617, 140, 120, "Oceanview / Balcony Stateroom 壁炉景观套房 (28㎡)", 28.0, 8.8,
     9.1, "JRE（欧洲青年餐厅协会）新锐米其林星厨合作菜单、Swan Restaurant 与池畔烧烤吧",
     9.5, "PC5/PC6高冰级破冰、船首无遮挡观鲸甲板（Swan's Nest）、全景芬兰桑拿房与文化学者深度讲座",
     9.5, "瑞典 Tillberg Design 打造的纯正北欧Scandi-luxe原木极简美学，每间客房均配真火焰视觉壁炉",
     4980, 9, "2027-04-05 达喀尔–卡萨布兰卡 9晚 ($4,980 起；南极10晚 $7,980 起)", "一价全包(餐饮+酒水+岸上探险+极地派克大衣+小费)",
     "人均吨位 75.84 GT、船员乘客比 0.86，表格硬件分高达 16.16 + 瑞典北欧原木壁炉客房 + PC5高冰级船身",
     "您《游轮数据》表中硬件分高达 16.16 的冷门黑马，在南极与西非航线上常有极佳的早鸟买一送一特惠。",
     "https://www.swanhellenic.com/", -64.2, -61.5, "SH Minerva", ""),

    ("seabourn-ovation-encore", "世邦·欢欣号 / 重奏号 (Seabourn Ovation / Encore)", "Seabourn 世邦邮轮", "六星全套房顶奢远洋船", "地中海 / 爱琴海 / 加勒比 / 亚洲",
     41865, 604, 450, "Veranda Suite 全海景阳台套房 (34.8㎡)", 34.8, 9.4,
     9.7, "米其林三星主厨 Thomas Keller 联名牛排馆 / Solis 地中海料理、Sushi 日料与不限量供应的世邦鱼子酱",
     9.2, "经典「冲浪里送鱼子酱香槟 (Caviar in the Surf)」海滩狂欢、船尾水上运动码头（Marina）与与Tim Rice爵士合作的音乐剧",
     9.5, "传奇设计师 Adam D. Tihany 以豪华私人游艇为灵感打造的螺旋中庭楼梯与全大理石双台盆卫浴",
     3024, 10, "2026-11-18 加勒比群岛深度 10晚 ($3,024 起，约 $302/晚；地中海7晚 $3,499 起)", "一价全包(鱼子酱自由+香槟烈酒+名厨餐厅+小费+星链Wi-Fi)",
     "人均吨位 69.31 GT、船员乘客比 0.75，表格硬件分 14.38 + 冲浪鱼子酱自由 + 未来一年最低每晚仅 $302",
     "完全印证您《加勒比游轮价格》表中的惊人高性价比（Seabourn 10晚 $3,024 / $302.4每晚），用高档大船阳台的钱住进真六星全包套房。",
     "https://www.seabourn.com/", 44.30, 9.21, "Seabourn Ovation",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/MV_Seabourn_Ovation_in_Portofino%2C_Italy.jpg/1280px-MV_Seabourn_Ovation_in_Portofino%2C_Italy.jpg"),

    ("mitsui-ocean-fuji", "商船三井·海洋富士号 (MITSUI OCEAN FUJI, 原Seabourn Odyssey)", "Mitsui Ocean Cruises 商船三井", "六星全套房顶奢远洋船", "日本环岛 / 濑户内海 / 冲绳与济州",
     32346, 450, 355, "Veranda Suite 和洋全阳台套房 (33.5㎡)", 33.5, 9.3,
     9.7, "三代日本名厨监修本格怀石料理《北斋 Hokusai Fine Dining》、The Restaurant 海景法餐与全天候日式下午茶",
     9.1, "日本传统落语/太鼓与能剧演出、露天温泉足汤海景甲板、日本百选名水与清酒品鉴会",
     9.3, "由世邦传奇名船 Seabourn Odyssey 全面改装，全套房带TOTO智能卫浴与深泡浴缸，完美兼顾西式游艇空间与日式极致服务",
     2680, 5, "2026-12-10 横滨–神户–济州–横滨 5晚 ($2,680 起)", "全包(怀石与法式正餐+酒水饮品+服务费)",
     "人均吨位 71.88 GT、船员乘客比 0.79，表格硬件分 15.08 + 全套房深浴缸 + 商船三井百年日式待客之道",
     "您在《游轮数据》表中专门单列的日本新旗舰（32,346吨/450客/355船员），体量小巧能直接驶入濑户内海与日本小众秘境港。",
     "https://www.mitsuioceancruises.com/", 35.45, 139.65, "Mitsui Ocean Fuji",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Mitsui_Ocean_Fuji_20241223_084153.jpg/1280px-Mitsui_Ocean_Fuji_20241223_084153.jpg"),

    ("seabourn-odyssey-sojourn-quest", "世邦·旅居号 / 探索号 (Seabourn Sojourn / Quest)", "Seabourn 世邦邮轮", "六星全套房顶奢远洋船", "地中海 / 不列颠群岛 / 阿拉斯加 / 环球",
     32346, 450, 335, "Veranda Suite 全海景阳台套房 (33.5㎡)", 33.5, 9.2,
     9.5, "The Restaurant 经典法餐、Earth & Ocean 星空甲板烧烤、Patio 池畔鱼子酱汉堡与香槟畅饮",
     9.0, "可深入大型邮轮无法进入的小型历史内港（如伦敦塔桥旁、波尔多市中心、塞维利亚内河）與海滩鱼子酱日",
     9.2, "Yran & Storbraaten 设计的经典北欧游艇风范，Seabourn Square 俱乐部沙龙取代传统前台",
     2999, 7, "2026-11-14 迈阿密–加勒比或巴塞罗那–罗马 7晚 ($2,999 起)", "一价全包(鱼子酱+香槟名酒+全套房+小费+Wi-Fi)",
     "人均吨位 71.88 GT、船员乘客比 0.74，表格硬件分 14.63 + 450客黄金私密体量",
     "世邦最具代表性的450客中型全套房游艇，在跨洋航次与深秋地中海航线上经常出现低于 $380/晚的神价。",
     "https://www.seabourn.com/", 43.30, 5.37, "Seabourn Sojourn", ""),

    ("silversea-silver-origin", "银海·源点号加拉帕戈斯全套房专船 (Silversea Silver Origin)", "Silversea 银海邮轮", "重型破冰与奢华极地科考", "加拉帕戈斯群岛全年驻航",
     6305, 100, 90, "Classic Veranda / Horizon Suite (30.2㎡)", 30.2, 9.2,
     9.4, "厄瓜多尔名厨主理的达尔文群岛零公里海鲜料理、The Grill 火山岩烧烤与厄瓜多尔精品可可/咖啡品鉴",
     10.0, "全加拉帕戈斯最高比例厄瓜多尔国家级博物学家团队、8艘Zodiac冲锋艇、浮潜面镜蛙鞋全包与Basecamp交互科考舱",
     9.6, "专为加拉帕戈斯生态正向定制的6305吨全套房科考游艇，电动升降Horizon全景窗与海景浴缸",
     9600, 7, "2026-11-28 圣克里斯托瓦尔往返加拉帕戈斯 7晚 ($9,600 起)", "一价全包(基多机票+2晚JW万豪+白金管家+每日双登陆科考+酒水)",
     "人均吨位 63.05 GT、船员乘客比 0.90（加拉帕戈斯最高！），表格硬件分 15.31 + 全套房私人管家",
     "加拉帕戈斯100人限额船队里的绝对天花板，也是唯一在群岛提供全套房白金私人管家服务的船。",
     "https://www.silversea.com/", -0.90, -89.61, "Silver Origin",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Silver_Origin.jpg/1280px-Silver_Origin.jpg"),

    ("silversea-silver-shadow-whisper", "银海·银影号 / 银啸号 (Silversea Silver Shadow / Whisper)", "Silversea 银海邮轮", "六星全套房顶奢远洋船", "加勒比海 / 南美 / 北欧与环球航线",
     28258, 388, 295, "Vista / Classic Veranda Suite 管家套房 (27–32㎡)", 32.0, 9.1,
     9.4, "La Dame 鲁莱夏朵法式名菜、La Terrazza 慢食协会手工意面与全天候套房龙虾/鱼子酱送餐",
     8.9, "不到400名乘客的超高私密俱乐部社交、雪茄吧 Connoisseur's Corner 与港口核心区停泊特权",
     9.0, "完成 Muse 级全面现代化翻新，全船仅388客却拥有近3万吨空间，电梯与走廊永远安静从容",
     2650, 7, "2026-12-11 圣胡安往返南加勒比 7晚 ($2,650 起，约 $379/晚)", "一价全包(私人管家+酒水香槟+岸上游+小费+Wi-Fi)",
     "人均吨位 72.83 GT、船员乘客比 0.76，表格硬件分 14.89 + 未来一年加勒比7晚最低仅 $2,650 ($378.6/晚)",
     "直接对应您《加勒比游轮价格》表中的 Silversea（7晚 $2,650 / $378.57每晚），不到三千美金就能享受银海白金管家与鱼子酱。",
     "https://www.silversea.com/", 18.46, -66.11, "Silver Shadow cruise ship", ""),

    ("silversea-silver-muse-moon-dawn", "银海·缪斯号 / 银月号 / 银晨号 (Silver Muse / Moon / Dawn)", "Silversea 银海邮轮", "六星全套房顶奢远洋船", "地中海 / 亚洲日本 / 阿拉斯加 / 澳新",
     40844, 596, 411, "Classic / Superior Veranda Suite (36㎡)", 36.0, 9.5,
     9.8, "多达8间餐厅：Kaiseki 日式怀石与寿司、Silver Note 爵士Tapas晚宴、S.A.L.T. 目的地厨房与 La Dame 法餐",
     9.2, "Otium 古罗马皇室水疗（床边热巧克力与香槟浴）、S.A.L.T. 岸上美食寻味团与每港免费岸上游",
     9.5, "意大利 Fincantieri 建造的现代意式优雅典范，基础阳台套房面积即达 36㎡，步入式衣帽间极其宽敞",
     3600, 7, "2027-01-15 新加坡–香港或雅典–伊斯坦布尔 7晚 ($3,600 起)", "一价全包(私人管家+8间餐厅+酒水+岸上游+小费)",
     "人均吨位 68.53 GT、船员乘客比 0.69，表格硬件分 13.75 + 36㎡超宽敞基础阳台套房 + 8间高定餐厅",
     "Silver Moon 与 Silver Dawn 搭载了倍受好评的 S.A.L.T. 酒吧与地方风味实验室，每到一个国家菜单与鸡尾酒单全部更换。",
     "https://www.silversea.com/", 37.94, 23.64, "Silver Muse", ""),

    ("hapag-lloyd-europa", "赫伯罗特·欧罗巴号经典传奇旗舰 (Hapag-Lloyd MS Europa)", "Hapag-Lloyd Cruises 赫伯罗特", "六星全套房顶奢远洋船", "波罗的海 / 挪威峡湾 / 地中海 / 亚洲",
     28890, 408, 275, "Veranda / Ocean Suite 经典套房 (27–33㎡)", 30.0, 9.0,
     9.9, "米其林三星主厨 Kevin Fehling 主理海上唯一三星基因餐厅《The Globe》+ 欧洲顶级鱼子酱之夜",
     9.1, "世界著名的海上古典音乐节（Ocean Sun Festival）、维也纳爱乐乐团成员登船独奏与高尔夫岸上巡回",
     9.2, "传统德意志远洋邮轮庄重美学，全套房配置，甲板柚木与黄铜细节保养如新",
     3990, 7, "2027-06-02 基尔–哥本哈根–波罗的海 7晚 ($3,990 起)", "含米其林三星基因餐厅The Globe及全船餐饮",
     "人均吨位 70.81 GT、船员乘客比 0.67，表格硬件分 13.82 + 米其林三星主厨 Kevin Fehling 驻船餐厅《The Globe》",
     "如果说 Europa 2 是现代时尚超跑，老大哥 MS Europa 就是劳斯莱斯幻影，船上古典乐演出水准堪比维也纳金色大厅。",
     "https://www.hl-cruises.com/", 54.32, 10.15, "MS Europa ship", ""),

    ("hapag-lloyd-hanseatic-nature-inspiration", "赫伯罗特·汉萨自然号 / 灵感号 / 精神号 (Hanseatic nature / inspiration / spirit)", "Hapag-Lloyd Cruises 赫伯罗特", "重型破冰与奢华极地科考", "南极洲 / 北极斯瓦尔巴 / 亚马逊河深入段 / 五大湖",
     15651, 230, 170, "Panorama / French Balcony Cabin (22–27㎡)", 24.0, 8.6,
     9.4, "Nikkei 秘鲁日式融合料理、Hamptons 北美牛排海鲜馆、Lido 露天烧烤与德系精酿香槟吧",
     9.9, "船头可伸缩液压玻璃悬空步道（Nature Walk）、17艘电动静音Zodiac冲锋艇、极地皮划艇与Ocean Academy交互科学屏",
     9.6, "PC6最高商业极地破冰船级，全船仿生自然曲线设计，连加热雪靴烘干室与望远镜都为每房标配",
     5490, 8, "2027-05-10 汉堡–苏格兰外赫布里底群岛 8晚 ($5,490 起；南极16晚 $13,900 起)", "含3间名厨餐厅+极地冲锋艇登陆+客房迷你吧",
     "人均吨位 68.05 GT、船员乘客比 0.74，表格硬件分 14.20 + PC6最高冰级 + 船头可伸缩悬空观鲸步道",
     "其中 Hanseatic inspiration 为英德双语国际船，不仅能破南极坚冰，还能凭借特殊船宽直接开进北美五大湖与亚马逊河上游4000公里。",
     "https://www.hl-cruises.com/", 78.22, 15.63, "Hanseatic nature", ""),

    ("crystal-serenity-symphony", "水晶邮轮·尚宁号 / 合韵号 (Crystal Serenity / Symphony — A&K全套房重生版)", "Crystal 水晶邮轮 (A&K集团)", "六星全套房顶奢远洋船", "地中海 / 北欧 / 阿拉斯加 / 环球航线",
     68870, 740, 655, "Sapphire Veranda / Aquamarine Suite (32–40㎡)", 37.0, 9.6,
     10.0, "全球唯一海上 Nobu（松久信幸）日料餐厅 Umi Uma 免费畅吃 + 传奇意大利名门 Osteria d'Ovidio 与 Beefbar",
     9.5, "全尺寸百老汇级剧场、伦敦康诺特酒店同款 Aurōra 水疗、高尔夫果岭推杆区与海上匹克球场",
     9.6, "由顶奢旅行巨头 Abercrombie & Krug (A&K) 斥巨资将两间原舱房合并为一间大套房，载客从1040人锐减至740人！",
     3800, 7, "2026-11-16 雅典–罗马或迈阿密–加勒比 7晚 ($3,800 起)", "一价全包(Nobu日料+私人管家+香槟名酒+小费+Wi-Fi)",
     "A&K改造后人均吨位跃升至 93.07 GT（原表 66.22 GT）、船员乘客比近 1:1 + 海上唯一免费 Nobu 松久信幸日料",
     "您《游轮数据》表记录了改造前的 68,870吨/1040客（硬件分12.92），2023年底A&K拆房扩建后仅载740人，空间感与餐饮统治力重回巅峰。",
     "https://www.crystalcruises.com/", 45.43, 12.33, "Crystal Serenity",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Crystal_Serenity_Under_Way.jpg/1280px-Crystal_Serenity_Under_Way.jpg"),

    ("regent-seven-seas-mariner-voyager", "丽晶七海·水手号 / 航海家号 (Seven Seas Mariner / Voyager)", "Regent Seven Seas 丽晶七海", "六星全套房顶奢远洋船", "加勒比海 / 巴拿马运河 / 南美 / 环球140天",
     48075, 700, 445, "Deluxe Veranda / Penthouse Suite (28–42㎡)", 33.0, 9.3,
     9.6, "Prime 7 美式牛排馆、Chartreuse 法餐、Sette Mari 意式海景餐厅与Compass Rose定制点单",
     9.4, "包含每个停靠港的无限次免费岸上观光、Canyon Ranch/Serene Spa 与高雅管弦乐晚会",
     9.2, "人类历史上第一艘实现「100%全套房、100%全私人阳台」的远洋奢华邮轮，中庭挑高通透大气",
     3999, 7, "2026-11-25 迈阿密–西加勒比 7晚 ($3,999 起；10晚 $5,499 起)", "真·一价全包(无限次岸上游+名厨餐厅+酒水+小费+Wi-Fi)",
     "人均吨位 68.68 GT、船员乘客比 0.64，表格硬件分 13.23 + 全球首艘100%全阳台全套房邮轮 + 岸上游全包",
     "比同门姐妹新船 Grandeur 价格低约 20%，但同样享受丽晶标志性的无限次免费岸上观光与名庄酒水全包。",
     "https://www.rssc.com/", 9.35, -79.91, "Seven Seas Mariner", ""),

    ("silversea-silver-spirit-dawn", "银海·银灵号 (Silversea Silver Spirit)", "Silversea 银海邮轮", "六星全套房顶奢远洋船", "地中海 / 阿拉伯湾 / 南非与印度洋",
     39519, 608, 412, "Classic / Superior Veranda Suite (35㎡)", 35.0, 9.4,
     9.6, "Seishin 亚洲融合寿司吧、Atlantide 海鲜牛排、La Dame 法餐、Spaccanapoli 现烤那不勒斯披萨与管家送餐",
     9.0, "超宽敞中段泳池甲板、Zagara 美学水疗中心、雪茄吧与目的地历史学者讲座",
     9.3, "在干船坞完成「切船加长15米」奇迹工程并全面换装 Silver Muse 现代内饰，全套房35㎡起步",
     3250, 7, "2026-12-06 开普敦–纳米比亚或雅典–威尼斯 7晚 ($3,250 起)", "一价全包(私人管家+8间餐厅+酒水+岸上游+小费)",
     "人均吨位 65.00 GT、船员乘客比 0.68，表格硬件分 13.28 + 35㎡全阳台管家套房",
     "经过船中段加长15米工程后，泳池甲板比原版扩大了30%，是银海船队里性价比极高的主力大船。",
     "https://www.silversea.com/", 35.89, 14.51, "Silver Spirit ship", ""),

    ("silversea-silver-cloud-wind", "银海·银云号 / 银风号极地破冰船 (Silver Cloud / Silver Wind)", "Silversea 银海邮轮", "重型破冰与奢华极地科考", "南极半岛 / 南乔治亚岛 / 北极格陵兰 / 智利峡湾",
     17400, 254, 222, "Vista / Veranda Suite 管家套房 (22–27㎡)", 27.0, 8.8,
     9.4, "在南极冰山前享用 La Dame 法式高定晚宴、The Grill 露天火山石烧烤与24小时热汤香槟管家服务",
     9.8, "极地航次严控在200–254人以内，配备20艘Zodiac冲锋艇、10余艘皮划艇与28人极地科学家团队",
     9.1, "由经典六星全套房邮轮重金加装破冰球鼻首改造而成，兼具老钱木质船舱温润感与硬核极地破冰能力",
     7400, 9, "2027-03-18 乌斯怀亚–智利峡湾 9晚 ($7,400 起；南极11天 $13,050)", "一价全包(私人管家+酒水+极地冲锋艇+派克大衣+小费)",
     "人均吨位 58.78–68.50 GT、船员乘客比 0.75–0.87，表格硬件分 13.38 + 南极冰海里的鲁莱夏朵法餐",
     "对应您《南极游轮》表第10行（Silversea Cloud/Wind 11天 $13,050）与《游轮数据》表（17,400吨/222船员），极地航次仅载200人。",
     "https://www.silversea.com/", -54.80, -68.30, "Silver Cloud ship", ""),

    ("quark-ultramarine", "夸克极地·海洋传奇号直升机探险船 (Quark Ultramarine)", "Quark Expeditions 夸克探险", "重型破冰与奢华极地科考", "南极半岛 / 威德尔海 / 北极加拿大群岛",
     13500, 199, 140, "Explorer Suite / Balcony Suite (26–39㎡)", 28.0, 8.9,
     8.9, "Balena 主餐厅与 Bistro 487 极地景观餐厅，提供现烤酸种面包、南美牛排与庆功香槟",
     10.0, "搭载2架双引擎 H145 极地探险直升机（全员包含直升机冰原降落体验！）、20艘快拆冲锋艇与高山滑雪/露营",
     9.5, "拥有同级最长70天续航力，水线处设有平视冰面与鲸鱼的内部快速登艇舱门（Ready Rooms）",
     8995, 10, "2026-11-12 乌斯怀亚往返南极半岛 10晚 ($8,995 起；表列11天均值 $11,516)", "一价全包(含H145直升机飞行观光+冲锋艇+酒水+极地冲锋衣)",
     "人均吨位 67.84 GT、船员乘客比 0.70，表格硬件分 13.82 + 全船票价免费包含双引擎 H145 直升机冰原降落",
     "在您的《游轮数据》与《南极游轮》两张表中均名列前茅，最大王牌是内部快速登艇区和人人都能坐的H145双发直升机。",
     "https://www.quarkexpeditions.com/", -64.7, -62.6, "Ultramarine Quark ship", ""),

    ("celebrity-flora", "名人邮轮·花神号加拉帕戈斯全套房巨艇 (Celebrity Flora)", "Celebrity Cruises 名人邮轮", "重型破冰与奢华极地科考", "加拉帕戈斯群岛全年驻航",
     5739, 100, 80, "Sky Suite with Infinite Veranda 无限阳台套房 (30.6㎡)", 30.6, 9.2,
     9.2, "米其林星级主厨 Cornelius Gallagher 研发菜单：Seaside Restaurant 与 Ocean Grill 星空烧烤",
     9.8, "定制超级游艇级 Novurania 豪华登陆艇（免湿脚登船）、顶层甲板星空豪华露营（Galapagos Glamping）与博物学家",
     9.7, "首创向外开启的全套房设计（Outward-Facing Concept）与动态定位无锚系统，保护脆弱火山海底珊瑚",
     7999, 7, "2026-12-06 巴尔特拉往返加拉帕戈斯内环/外环 7晚 ($7,999 起)", "一价全包(基多机票+酒店+全套房私人助理+酒水+每日科考)",
     "人均吨位 57.39 GT、船员乘客比 0.80，表格硬件分 13.74 + 30.6㎡全套房无限阳台 + 甲板观星露营",
     "加拉帕戈斯设计最现代前卫的100人专船，连接驳艇都不是普通橡胶艇，而是带遮阳棚和皮座椅的豪华游艇接驳船。",
     "https://www.celebritycruises.com/", -0.45, -90.26, "Celebrity Flora", ""),

    ("sea-cloud-spirit-i-ii", "海云号·传奇四桅皇家高桅横帆船 (Sea Cloud / Sea Cloud II / Spirit)", "Sea Cloud Cruises 海云帆船邮轮", "顶奢风帆与高定超级游艇", "地中海 / 加勒比海 / 加那利群岛",
     2532, 64, 60, "Original Marjorie Post Suite / Deluxe Cabin (20–38㎡)", 25.0, 8.7,
     9.5, "罗莱夏朵级主厨现采当地海鲜市场料理、甲板星空龙虾BBQ与德国名庄雷司令/香槟畅饮",
     9.6, "全程20名水手徒手爬上58米高桅杆人工升起30张近3000㎡白帆！航行中直接从船舷跳入地中海游泳",
     9.9, "1931年美国女首富 Marjorie Merriweather Post 私人建造的传奇四桅帆船，保留天鹅颈金水龙头、古董大理石壁炉与桃花心木甲板",
     4650, 7, "2026-11-22 拉斯帕尔马斯加那利群岛或圣马丁加勒比 7晚 ($4,650 起)", "全包(主厨正餐+精选葡萄酒啤酒+水上活动+小费)",
     "船员乘客比高达 0.94（64客配60名船员与水手！），表格硬件分 13.33 + 1931年首富私人古董四桅大帆船",
     "拒绝机械按钮卷帆！每天看着水手们像19世纪水兵一样爬上几十米高的横桁手动解帆，是任何现代邮轮都给不了的震撼。",
     "https://www.seacloud.com/", 17.89, -62.85, "Sea Cloud ship", ""),

    ("seadream-yacht-i-ii", "海梦游艇俱乐部·SeaDream I / II", "SeaDream Yacht Club 海梦游艇", "顶奢风帆与高定超级游艇", "圣巴茨与英属维尔京 / 法国与意大利里维埃拉",
     4333, 112, 95, "Yacht Club Stateroom 游艇海景套房 (18.5㎡)", 18.5, 8.2,
     9.6, "5星级露天柚木甲板全天候奉餐、生食有机料理菜单与著名的「浪花里的香槟鱼子酱派对 (Champagne & Caviar Splash)」",
     9.7, "新装甲板滑入大海的超级游艇滑水道（Water Slide to the Sea）、泰式认证露天按摩、星空巴厘床（Balinese Dream Beds）露宿",
     9.3, "口号「It's Yachting, Not Cruising（这是私人游艇，绝非邮轮）」，夜间在圣巴茨或卡普里岛外锚泊彻夜狂欢",
     3999, 7, "2026-11-15 圣托马斯–圣巴茨–安圭拉 7晚 ($3,999 起)", "一价全包(香槟鱼子酱派对+开放式酒吧+水上玩具+小费)",
     "船员乘客比 0.85（112客/95船员），表格硬件分 12.35 + 圣巴茨海滩香槟鱼子酱冲浪 + 甲板星空巴厘大床过夜",
     "晚上水手会在后甲板露天巴厘床上铺好比利时亚麻床品，让你吹着加勒比海风在漫天银河下入睡。",
     "https://seadream.com/", 18.33, -64.73, "SeaDream I", ""),

    ("windstar-star-pride-breeze-legend", "风星邮轮·星辰骄傲号 / 微风号 / 传奇号全套房游艇 (Windstar Star Pride / Breeze / Legend)", "Windstar Cruises 风星邮轮", "顶奢风帆与高定超级游艇", "大溪地群岛 / 冰岛环岛 / 地中海小港 / 加勒比",
     9975, 208, 164, "Star Balcony / Classic Suite 全套房 (25.7㎡)", 25.7, 8.8,
     9.5, "「詹姆斯·比尔德基金会 (James Beard Foundation)」官方合作游轮：Cuadro 44 西班牙创意料理与 Star Grill by Steven Raichlen",
     9.2, "大溪地私人无人岛 Motu 火舞海滩烤猪盛宴、船尾直通大海的水上浮毯与免费滑水/皮划艇",
     9.1, "原世邦经典三姊妹船经「切船加长25.6米」并斥资2.5亿美金翻新，全船仅156间25.7㎡以上套房",
     2399, 7, "2026-12-03 大溪地帕皮提往返社会群岛 7晚 ($2,399 起；加勒比14晚 $3,299 起，约 $236/晚)", "含全部James Beard基金会名厨餐厅+水上运动平台",
     "人均吨位 47.96 GT、船员乘客比高达 0.79，表格硬件分 12.68 + 詹姆斯·比尔德美食基金会官方背书 + 每晚最低仅 $236",
     "完美契合您《加勒比游轮价格》表中的 Windstar（14晚 $3,299 / $235.6每晚），是用亲民价格体验0.79高船员比全套房游艇的神选。",
     "https://www.windstarcruises.com/", -16.50, -151.74, "Star Pride ship",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Star_Pride_in_Helsinki.jpg/1280px-Star_Pride_in_Helsinki.jpg"),

    ("ponant-paul-gauguin", "庞洛·保罗高更号大溪地传奇专船 (m/s Paul Gauguin)", "Ponant / Paul Gauguin Cruises", "顶奢风帆与高定超级游艇", "法属波利尼西亚（大溪地 / 波拉波拉 / 莫雷阿 / 土阿莫土）",
     19200, 332, 215, "Balcony Stateroom 泻湖阳台房 (22.5㎡)", 22.5, 8.6,
     9.4, "巴黎米其林星厨 Jean-Pierre Vigato 设计的 L'Etoile 法餐、La Veranda 与大溪地鲜切金枪鱼刺身",
     9.8, "专属大溪地本地歌舞艺人天团「Les Gauguines」全程伴游、波拉波拉专属私人白沙滩 + 塔哈岛私人珊瑚岛 Motu Mahana 一日狂欢",
     9.3, "专为南太平洋浅水环礁泻湖设计的5.1米超浅吃水船体，唯一能驶入大溪地内礁的五星奢华专船",
     3990, 7, "2026-11-21 帕皮提往返大溪地与社会群岛 7晚 ($3,990 起)", "一价全包(法餐+酒水+两处私人海滩岛屿+水上运动+小费+Wi-Fi)",
     "人均吨位 57.83 GT、船员乘客比 0.65，表格硬件分 12.26 + 波拉波拉与塔哈岛双私人岛屿特权",
     "在波拉波拉住5晚水屋动辄花掉 $7,000+ 且还要自付三餐和跳岛小飞机；坐保罗高更号一价全包睡醒直接停在泻湖中央。",
     "https://www.pgcruises.com/", -16.50, -151.74, "Paul Gauguin ship",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Cruise_Ship_Paul_Gauguin_01.jpg/1280px-Cruise_Ship_Paul_Gauguin_01.jpg"),

    ("oceania-vista-allura", "大洋邮轮·魅力号 / 远景号 (Oceania Allura / Vista)", "Oceania Cruises 大洋邮轮", "高档美食与文化精奢邮轮", "地中海 / 不列颠群岛 / 加勒比与美东",
     67817, 1226, 800, "Veranda / Concierge Veranda 全阳台舱 (27㎡)", 27.0, 8.9,
     10.0, "号称「海上最顶尖美食 (The Finest Cuisine at Sea)」：法餐教父 Jacques Pépin 监制、Ember 美式炙烤、Aquamar 健康料理、Red Ginger 与 Toscana",
     9.1, "全海上规模最大的22工位专业厨艺中心（Culinary Center）、艺术家驻船画室（Artist Loft）与宝格丽洗护水疗",
     9.4, "彻底取消内舱房（100%全阳台），双层挑高水晶柱楼梯与法式可丽饼屋烘焙坊",
     2299, 7, "2026-11-18 迈阿密往返加勒比或巴塞罗那–罗马 7晚 ($2,299 起，约 $328/晚)", "Your World Included(含全船特色餐厅+法式烘焙+软饮咖啡+小费+Wi-Fi)",
     "人均吨位 55.32 GT、船员乘客比 0.65（每2名船员配1名厨师！），表格硬件分 12.06 + 海上公认餐饮第一名",
     "与您《加勒比游轮价格》表中的 Oceania（7晚 $2,299 / $328.4每晚）分毫不差！船上400名厨师团队做的法餐与牛排秒杀陆地米其林。",
     "https://www.oceaniacruises.com/", 41.38, 2.18, "Oceania Vista",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Oceania_Vista_in_port_at_Istanbul_%281%29.png/1280px-Oceania_Vista_in_port_at_Istanbul_%281%29.png"),

    ("oceania-marina-riviera", "大洋邮轮·玛丽娜号 / 丽维拉号 (Oceania Marina / Riviera)", "Oceania Cruises 大洋邮轮", "高档美食与文化精奢邮轮", "地中海 / 北欧波罗的海 / 南美 / 亚洲",
     66804, 1250, 800, "Veranda / Penthouse Suite (26–39㎡)", 26.5, 8.8,
     9.9, "保留原汁原味的 Jacques 正统法餐厅（法餐传奇大师 Jacques Pépin 亲自署名餐厅）、Polo Grill 牛排龙虾与 La Reserve 葡萄酒配餐晚宴",
     9.0, "La Reserve by Wine Spectator 珍稀年份香槟品鉴会、亲手烹饪课与18洞果岭推杆",
     9.2, "全船完成耗资数千万美金的「Re-Inspiration」翻新，Ralph Lauren Home 定制主人套房与Lalique水晶主楼梯",
     1999, 7, "2026-12-02 迈阿密–加勒比或雅典–伊斯坦布尔 7晚 ($1,999 起)", "Your World Included(含Jacques法餐等全船特色餐厅+小费+Wi-Fi)",
     "人均吨位 53.44 GT、船员乘客比 0.64，表格硬件分 11.74 + Lalique莱俪水晶打造的宫殿楼梯 + 正统Jacques法餐",
     "很多老饕专门挑 Marina 和 Riviera 坐，就因为这两艘船保留了完整独立的 Jacques 法餐厅和 La Reserve 帕克高分酒晚宴。",
     "https://www.oceaniacruises.com/", 43.73, 7.42, "MS Marina ship", ""),

    ("viking-ocean-star-sky-jupiter", "维京远洋·猎户座号 / 维京之星号 / 维京天空号 (Viking Star / Sky / Orion / Mars)", "Viking Ocean Cruises 维京远洋", "高档美食与文化精奢邮轮", "挪威北极光 / 地中海 / 大洋洲 / 环球航线",
     47842, 930, 602, "Veranda / Deluxe Veranda 全阳台房 (25㎡)", 25.0, 8.7,
     9.2, "Manfredi's 托斯卡纳牛排意餐（全部免费预订）、The Chef's Table 五道式配酒晚宴与 Mamsen's 挪威华夫饼鱼子酱",
     9.3, "18岁以下禁入（无赌场、无推销摄影师）、船尾玻璃无边泳池、免费北欧真雪屋（Snow Grotto）热疗Spa与每港免费岸上游",
     9.6, "纯正斯堪的纳维亚原木极简美学，双层 Explorers' Lounge 观景图书馆与Ted级别驻船学者讲座",
     2999, 8, "2026-11-26 巴塞罗那–罗马地中海 8晚 ($2,999 起；加勒比10晚 $3,799 起)", "全包(每港1次岸上游+特色餐厅+佐餐红白酒啤酒+雪屋Spa+Wi-Fi)",
     "人均吨位 51.44 GT、船员乘客比 0.65，表格硬件分 11.62 + 全船无内舱房/无儿童/无赌场 + 免费北欧雪屋Spa与船尾无边泳池",
     "对应您《游轮数据》表的 Viking Star（9艘同级姊妹船，硬件分 11.62）与《加勒比游轮价格》表（10晚 $3,799 / $379.9每晚）。",
     "https://www.vikingcruises.com/", 60.39, 5.32, "Viking Star ship", ""),

    ("ponant-explorers-bellot-bougainville", "庞洛探险家系列·贝洛特号 / 布干维尔号 / 尚普兰号 (Le Bellot / Le Bougainville / Le Champlain)", "Ponant 庞洛邮轮", "重型破冰与奢华极地科考", "塞舌尔外岛 / 金伯利海岸 / 希腊小岛 / 红海",
     9900, 184, 110, "Prestige Stateroom 全私人阳台房 (19+4㎡)", 23.0, 8.5,
     9.5, "纯正法兰西美食血统：法国Bordier手工黄油、鱼子酱、鹅肝、Charles Heidsieck 香槟无限畅饮与法式烘焙",
     9.7, "全球独创水下多感官海底酒廊《Blue Eye 蓝眼》（水下3米双鲸鱼眼巨窗+水听器听鲸歌）与液压升降游艇码头",
     9.6, "131米法式高定超级游艇流线船身，全船92间房100%带私人阳台，Diptyque / Hermès 洗护备品",
     3600, 8, "2026-11-29 加勒比或地中海跳岛 8晚 ($3,600 起，约 $450/晚)", "一价全包(法餐+香槟名酒+水下蓝眼酒廊+冲锋艇登陆+Wi-Fi)",
     "人均吨位 53.80 GT、船员乘客比 0.60，表格硬件分 11.36 + 全球唯一水下3米《Blue Eye》海底观景听鲸酒廊",
     "直接对应您《加勒比游轮价格》表第3行的 Ponant（8晚 $3,600 / $450每晚），水下酒廊喝着香槟看海豚游过舷窗浪漫至极。",
     "https://us.ponant.com/", -4.62, 55.45, "Le Bellot ship", ""),

    ("hebridean-princess", "赫布里底公主号·英国女王御用包船游艇 (MV Hebridean Princess)", "Hebridean Island Cruises", "顶奢风帆与高定超级游艇", "苏格兰高地峡湾 / 外赫布里底群岛 / 艾雷岛威士忌巡礼",
     2112, 49, 38, "Isle of Arran / Tiree 格纹古典舱 (16–24㎡)", 20.0, 8.2,
     9.5, "苏格兰高地黑安格斯和牛、现捕斯凯岛龙虾扇贝、艾雷岛单一麦芽威士忌泥煤桶全畅饮与英式皇家下午茶",
     9.3, "私家城堡包场导览、艾雷岛传奇威士忌酒厂VIP开桶品鉴、私人快艇荒岛漫步与风笛手迎宾",
     9.1, "原英国皇家邮政船改建的英伦老钱乡村庄园游艇（Country House at Sea），真砖砌壁炉サロン与苏格兰格纹内饰",
     5250, 7, "2027-04-06 奥本往返苏格兰内赫布里底群岛 7晚 ($5,250 起)", "全包(高地美食+单一麦芽威士忌香槟+全部岸上古堡酒厂门票+小费)",
     "船员乘客比高达 0.78（仅载49位贵宾配38名船员！），表格硬件分 12.07 + 伊丽莎白二世女王曾两次私人包船庆生",
     "您在《游轮数据》表中专门收录的袖珍传奇（2,112吨/49客/38船员），已故英国女王80岁与84岁大寿均包下整艘船与皇室家庭度假。",
     "https://www.hebridean.co.uk/", 56.41, -5.47, "Hebridean Princess", ""),

    ("quark-ocean-explorer", "夸克极地·海洋探索者号 (Quark Ocean Explorer)", "Quark Expeditions 夸克探险", "重型破冰与奢华极地科考", "南极半岛 / 南乔治亚岛 / 斯瓦尔巴与格陵兰",
     8228, 138, 105, "Veranda / Infinity Suite 阳台舱 (20–35㎡)", 24.0, 8.6,
     8.8, "极地高蛋白西式主厨菜单、阿根廷门多萨葡萄酒与船首两层挑高图书馆下午茶",
     9.8, "15艘Zodiac冲锋艇、极地皮划艇、冰原徒步、冰海冬泳与夸克王牌极地博物学家团队",
     9.4, "Ulstein X-BOW 倒弓形破浪船首设计，船头两层挑高全落地窗 Latitude 观察酒廊与户外热水按摩池",
     7890, 10, "2026-11-18 乌斯怀亚–南极半岛 10晚 ($7,890 起)", "一价全包(冲锋艇登陆+酒水佐餐+夸克橙色三合一极地冲锋衣)",
     "人均吨位 59.62 GT、船员乘客比 0.76，表格硬件分 13.57 + X-BOW倒弓形平稳船首 + 138客高机动快速登陆",
     "由于南极规定同一登陆点每次不得超过100人同时上岸，138客的 Ocean Explorer 几乎能让全船乘客无缝轮换登陆。",
     "https://www.quarkexpeditions.com/", -64.8, -63.0, "Ocean Explorer ship", ""),

    ("disney-wish-treasure-destiny", "迪士尼邮轮·愿望号 / 宝藏号 / 命运号礼宾与塔楼套房 (Disney Wish / Treasure / Destiny)", "Disney Cruise Line 迪士尼邮轮", "经典远洋皇后与旗舰级套房", "巴哈马私人岛 (Castaway / Lookout Cay) / 加勒比海",
     144256, 2476, 1555, "Deluxe Oceanview Verandah / Concierge Suite (23–182㎡)", 28.0, 9.0,
     9.6, "唯一入选榜单的成人米其林三星主厨 Arnaud Lallement 法餐厅《Enchante》+ 漫威/冰雪奇缘/寻梦环游记沉浸式剧场晚宴",
     10.0, "全球首创海上互动过山车水道 AquaMouse、每晚百老汇原版《阿拉丁》《美女与野兽》巨制、海上烟花秀与巴哈马双私人海岛",
     9.8, "把黄金时代远洋邮轮古典美学与迪士尼幻想工程结合，前烟囱内竟藏着一套182㎡双层《莫阿娜/EPCOT烟囱塔楼套房》",
     1632, 4, "2026-11-30 卡纳维拉尔港–巴哈马私人岛 4晚 ($1,632 起；7晚 $2,780 起)", "含三大沉浸主题晚宴+百老汇大秀+软饮冰淇淋+巴哈马私人岛BBQ",
     "人均吨位高达 58.26 GT、船员乘客比 0.63，表格硬件分 12.11（甚至超越多艘小型高档船！）+ 顶配海上演艺与米其林三星法餐",
     "您在《游轮数据》表中算出的神数据：Disney Wish 以14.4万吨仅设2,476个双人床位，硬件分高达 12.11，礼宾区（Concierge）服务堪比六星船。",
     "https://disneycruise.disney.go.com/", 26.08, -77.53, "Disney Wish",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Disney_wish_nassau_08202022.jpg/1280px-Disney_wish_nassau_08202022.jpg"),

    ("regent-seven-seas-navigator", "丽晶七海·领航者号全套房邮轮 (Seven Seas Navigator)", "Regent Seven Seas 丽晶七海", "六星全套房顶奢远洋船", "地中海 / 非洲海岸 / 南太平洋与大洋洲",
     28550, 490, 340, "Deluxe Window / Veranda Suite 全套房 (28–33㎡)", 31.0, 9.2,
     9.5, "Prime 7 牛排馆、Sette Mari 意式晚宴、Compass Rose 定制零点菜单与全船名庄香槟威士忌畅饮",
     9.3, "全包每个停靠港的无限次岸上观光、仅490名乘客的私密游艇社交与能够停进小众历史港口的内湾航线",
     9.0, "原苏联科研船壳体在意大利耗巨资改建而成的传奇全套房邮轮，所有基础套房面积均超 28㎡ 且带步入式衣帽间",
     3499, 7, "2026-11-19 雅典–伊斯坦布尔或巴塞罗那–里斯本 7晚 ($3,499 起)", "真·一价全包(无限次岸上游+名厨餐厅+酒水+小费+Wi-Fi)",
     "人均吨位 58.27 GT、船员乘客比 0.69，表格硬件分 12.77 + 490客袖珍全套房 + 丽晶全包岸上观光",
     "丽晶七海船队中体量最小、最像私人游艇的一艘，也是体验丽晶「无限次岸上游全包」门槛最低的船。",
     "https://www.rssc.com/", 37.94, 23.64, "Seven Seas Navigator", ""),

    ("lindblad-ng-explorer-orion", "林德布拉德×国家地理·探索者号 / 猎户座号 (NG Explorer / NG Orion)", "Lindblad × National Geographic", "重型破冰与奢华极地科考", "南极洲 / 南乔治亚与福克兰 / 巴塔哥尼亚 / 印尼群岛",
     6471, 148, 99, "Category 1-6 科考海景/阳台舱 (18–26㎡)", 21.0, 8.2,
     8.8, "可持续采购极地海鲜与南美安第斯有机风味、Bistro 轻食吧与极地冰山烧烤派对",
     10.0, "随船配备《国家地理》水下摄影师、300米深海ROV遥控潜航器、水听器、声呐扫描仪与全天开放驾驶台（Open Bridge）",
     8.9, "1A级高冰级极地科考功勋船，船顶设有360度全景玻璃观察舱（Chart Room）与泥靴烘干舱",
     7980, 10, "2027-03-08 乌斯怀亚–智利峡湾 10晚 ($7,980 起；南极12–14天 $10,780–$14,940)", "一价全包(国家地理专家团+冲锋艇皮划艇+酒水+小费+Wi-Fi)",
     "人均吨位 43.72 GT、船员乘客比 0.67–0.71，表格硬件分 11.06 + 24小时向乘客开放的船长驾驶台 (Open Bridge)",
     "对应您《南极游轮》表第7行与第23行（Orion 12天 $10,780 / Explorer 14天 $14,940），是硬核自然纪录片迷心中的朝圣之船。",
     "https://www.expeditions.com/", -54.8, -68.3, "National Geographic Explorer ship", ""),

    ("mystic-atlas-world-voyager-explorer", "阿特拉斯游艇·世界航海家号 / 探险家号 / 旅行者号 (Atlas World Voyager / Navigator / Traveller)", "Atlas Ocean Voyages / Mystic", "重型破冰与奢华极地科考", "南极洲 / 北极斯瓦尔巴 / 地中海美食航线",
     9935, 198, 125, "Horizon / Veranda Stateroom (25㎡)", 25.0, 8.7,
     9.2, "地中海航季主打「Epicurean Expeditions（饕餮探险）」：米其林星级客座主厨登船、Alma 葡式海鲜与7Aft甲板熏肉烧烤",
     9.5, "南极航线包含免费极地冰原露营或Zodiac冰川巡游、船首贴海观鲸廊道（Water's Edge）与L'Occitane欧舒丹海上水疗",
     9.3, "葡萄牙 Mystic 集团打造的全新一代1B冰级混合动力极地游艇，外观修长现代，配喷水推进器静音护鲸",
     3499, 7, "2026-11-14 里斯本–巴塞罗那地中海美食航次 7晚 ($3,499 起；南极9晚 $7,999 起)", "一价全包(餐饮+香槟烈酒+岸上探险/美食体验+极地派克大衣+小费)",
     "人均吨位 50.18 GT、船员乘客比 0.63，表格硬件分 11.33 + 船头距海面仅9米高的贴海观鲸步道",
     "注意您《游轮数据》表中 Quark World Explorer 与 Mystic+Atlas World Voyager 同为 9,935吨/198客/125船员，因为它们正是同级姊妹船！",
     "https://atlasoceanvoyages.com/", 38.71, -9.14, "World Explorer cruise ship", ""),

    ("saga-spirit-of-discovery-adventure", "萨迦邮轮·探索精神号 / 冒险精神号 (Saga Spirit of Discovery / Adventure)", "Saga Cruises 英国萨迦邮轮", "高档美食与文化精奢邮轮", "不列颠群岛 / 挪威峡湾 / 加那利群岛 / 地中海",
     58119, 999, 524, "Standard Balcony 全私人阳台舱 (20+4㎡)", 24.0, 8.7,
     9.4, "零附加费畅吃全部特色餐厅：The Club by Jools Holland（牛排音乐餐吧）、Coast to Coast 英国海鲜、Amalfi 意餐与 Khukuri 尼泊尔料理",
     9.1, "50岁以上英伦熟龄俱乐部、伦敦西区音乐剧剧院、水疗红外桑拿泳池与英国家庭门口免费专车接送至港口（UK Chauffeur）",
     9.3, "德国 Meyer Werft 船厂专门建造的英伦精品全阳台船，全船近100间单人独立阳台房（Solo Balcony）对独行客极度友好",
     2450, 7, "2026-11-28 朴茨茅斯往返西欧或加那利 7晚 ($2,450 起)", "一价全包(特色餐厅+酒水+旅游保险+小费+Wi-Fi+英国专车接送)",
     "人均吨位 58.18 GT、船员乘客比 0.52，表格硬件分 11.06 + 100%全阳台 + Jools Holland 爵士牛排俱乐部免费吃",
     "您在《游轮数据》表中发掘出的宝藏英国高档船（58,119吨仅载999人），空间感媲美六星船，且特色餐厅一分钱不加收。",
     "https://travel.saga.co.uk/cruises.aspx", 50.80, -1.09, "Spirit of Discovery ship", ""),

    ("viking-vela-china-merchants-yidun", "维京新旗舰·维京船帆号 / 招商伊敦号 (Viking Vela / 招商维京伊敦号)", "Viking / 招商维京游轮", "高档美食与文化精奢邮轮", "北欧与地中海 / 中国海岸与日韩航线",
     53769, 986, 480, "Veranda / Nordic Junior Suite 全阳台房 (25–32㎡)", 25.0, 8.7,
     9.2, "The Restaurant 北欧新料理、Manfredi's 意式手工面与牛排、Chef's Table 配酒品鉴及伊敦号专属本帮/粤式融合私房菜",
     9.2, "北欧免费真雪屋（Snow Grotto）水疗、无赌场无推销的纯粹人文书香空间、敦煌/故宫或欧洲历史学者讲座",
     9.5, "Viking Vela 将吨位进一步扩大至 53,769 吨（支持未来氢燃料电池零排放改造），招商伊敦号则为原 Viking Sun 姊妹船",
     1680, 5, "2026-11-15 深圳/上海出发日本或东南沿海 5晚 ($1,680 起；Viking Vela 欧洲7晚 $2,899 起)", "全包(全船餐厅+佐餐酒水+北欧雪屋Spa+每港基础岸上游+Wi-Fi)",
     "人均吨位 51.40–54.53 GT，表格硬件分 10.17–10.30 + 全中文或纯北欧零购物安静环境 + 北欧真雪屋水疗",
     "合并了您《游轮数据》表中的 Viking Vela（53,769吨/986客）与招商维京·招商伊敦号（47,800吨/930客），是中国母港唯一真正的北欧高档全阳台船。",
     "https://www.cmviking.com/", 22.48, 114.92, "Viking Sun ship", ""),

    ("azamara-onward-quest-journey", "精钻邮轮·前行号 / 探索号 / 旅程号 / 追求号 (Azamara Onward / Quest / Journey / Pursuit)", "Azamara Cruises 精钻邮轮", "高档美食与文化精奢邮轮", "地中海小内港 / 苏格兰高尔夫 / 日本环岛 / 南非",
     30277, 684, 400, "Club Veranda / Club Continent Suite (20–30㎡)", 22.0, 8.3,
     9.2, "Prime C 经典美式牛排馆、Aqualina 地中海海鲜、Atlas Bar 分子调酒与港口当地食材长桌盛宴",
     9.6, "每条航线免费赠送一场包场文化盛典「AzAmazing Evenings」（如包下以弗所古罗马剧场或利沃诺歌剧院听交响乐）+ 80%港口夜间延时停靠",
     8.9, "传奇 R-Class 三万吨级经典中型船体，能直接开进大船进不去的曼谷湄南河内港、波尔多市中心与科林斯运河",
     1799, 10, "2026-11-22 迈阿密–加勒比 10晚 ($1,799 起，约 $179.9/晚；地中海7晚 $1,599 起)", "含酒水饮品+小费+自助洗衣+AzAmazing包场文化夜",
     "人均吨位 44.26 GT、船员乘客比 0.58，表格硬件分 10.27 + 免费包场古迹音乐会 + 未来一年最低每晚仅 $179.9",
     "直接对应您《加勒比游轮价格》表中的 Azamara（10晚 $1,799 / $179.9每晚），是花最少钱享受小型精奢船与深度慢旅行的利器。",
     "https://www.azamara.com/", 43.73, 7.42, "Azamara Onward",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Azamara_Onward_IMO_9187887_P_Hamburg_29-08-2024_%281%29.jpg/1280px-Azamara_Onward_IMO_9187887_P_Hamburg_29-08-2024_%281%29.jpg"),

    ("cunard-queen-mary-2-grill", "冠达邮轮·玛丽皇后2号皇后套房 (Cunard Queen Mary 2 — Queens Grill)", "Cunard Line 冠达邮轮", "经典远洋皇后与旗舰级套房", "南安普敦–纽约跨大西洋直航 / 北欧峡湾",
     149215, 2695, 1253, "Britannia Balcony / Princess & Queens Grill Suite (23–209㎡)", 35.0, 9.2,
     9.4, "Queens Grill 专属私密餐厅（白手套管家桌边火焰料理 Flambé、不限量鱼子酱）、The Verandah 法餐与白手套英式下午茶",
     9.5, "全球唯一海上全尺寸球幕天文馆（Illuminations Planetarium）、全球最大1万册海上图书馆、皇家莎士比亚剧团演出与盛装舞会",
     9.9, "人类现役唯一真正的「远洋定期班轮 (True Ocean Liner)」，加厚抗北大西洋狂浪高干舷钢板、4台劳斯莱斯燃气轮机极速30节",
     1199, 7, "2026-11-15 南安普敦–纽约跨大西洋 7晚 ($1,199 阳台起；Queens Grill皇后套房 $3,899 起)", "含白手套英式下午茶+天文馆+盛装舞会(Queens Grill含专属餐厅与管家)",
     "人均吨位高达 55.37 GT、船员乘客比 0.46，表格硬件分 10.19（15万吨巨轮中空间比第一！）+ 人类唯一现役远洋班轮",
     "您在《游轮数据》表中算出的经典对比：QM2虽重达14.9万吨，但仅载2695人，人均吨位（55.37）竟比绝大多数5万吨小型船还高！",
     "https://www.cunard.com/", 50.90, -1.40, "Queen Mary 2",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Hamburg%2C_Hafen%2C_Kreuzfahrtschiff_-Queen_Mary_2-_--_2016_--_3050.jpg/1280px-Hamburg%2C_Hafen%2C_Kreuzfahrtschiff_-Queen_Mary_2-_--_2016_--_3050.jpg"),

    ("club-med-2-sailing", "地中海俱乐部2号·五桅电脑风帆游艇 (Club Med 2)", "Club Med 地中海俱乐部", "顶奢风帆与高定超级游艇", "法属里维埃拉 / 科西嘉与撒丁岛 / 圣巴茨与加勒比",
     14983, 386, 214, "Superior / Shipowner Suite 海景舱 (18–40㎡)", 20.0, 8.2,
     9.1, "Le Méditerranée 与 Le Magellan 双法式餐厅，提供法式鹅肝、现开生蚝、巴黎甜点与无限量香槟红酒",
     9.5, "400㎡船尾直接降入海面的大型水上运动基地：免费专人指导滑水（Waterskiing）、尾波冲浪、风帆、桨板与浮潜",
     9.3, "由法国建筑设计师 Sophie Jacqmin 操刀2023全面焕新，187米长船身立有5根50米高电脑控制自动卷帆桅杆",
     2490, 7, "2026-12-05 马提尼克–格林纳丁斯群岛 7晚 ($2,490 起)", "一价全包(法餐+香槟红酒+全套滑水帆板水上运动教练+小费)",
     "人均吨位 38.82 GT、船员乘客比 0.55，表格硬件分 9.43 + 全球最大五桅风帆邮轮之一 + 船尾滑水冲浪全免费",
     "在您《游轮数据》表中紧随超级大船之前的五桅帆船（14,983吨/386客/214船员），水浅到能停在科西嘉与圣巴茨的私人海湾里。",
     "https://www.clubmed.us/l/cruises", 14.60, -61.07, "Club Med 2", ""),

    ("windstar-wind-surf-wind-star", "风星邮轮·微风号 / 风之星号浪漫高桅帆船 (Windstar Wind Surf / Wind Star / Wind Spirit)", "Windstar Cruises 风星邮轮", "顶奢风帆与高定超级游艇", "大溪地群岛 / 希腊爱琴海 / 圣巴茨加勒比 / 科林斯运河",
     14745, 342, 214, "Ocean View / Bridge Suite 柚木风帆套房 (18–46㎡)", 21.0, 8.3,
     9.4, "James Beard 基金会联名主厨菜单、Candles 帆影星空牛排烧烤与 Stella Bistro 法式小酒馆",
     9.4, "每港离港时伴随 Vangelis《1492征服天堂》史诗配乐升起2,600㎡巨型三角白帆 + 船尾海水泳池与水上跳床平台",
     9.4, "五桅（Wind Surf）与四桅（Wind Star）机动高桅帆船，既有超级帆船的御风浪漫，又有现代陀螺仪抗浪稳定器",
     2199, 7, "2026-11-28 圣马丁–英属维尔京群岛 7晚 ($2,199 起；大溪地7晚 $2,599 起)", "含James Beard联名餐厅+水上运动平台+软饮",
     "人均吨位 38.20–43.11 GT、船员乘客比 0.55–0.61，表格硬件分 9.36–9.67 + 伴随《1492征服天堂》扬帆出港的催泪仪式感",
     "Wind Star（5,307吨/148客）与 Wind Surf（14,745吨/342–386客）在您的《游轮数据》表中双双上榜，是在大溪地和希腊拍照最仙的船。",
     "https://www.windstarcruises.com/", 18.04, -63.05, "Wind Surf ship", ""),

    ("ponant-boreal-austral-lyrial-soleal", "庞洛姐妹游艇·北极号 / 南极号 / 天琴号 / 日丽号 (Le Boréal / L'Austral / Le Lyrial / Le Soléal)", "Ponant 庞洛邮轮", "重型破冰与奢华极地科考", "南极半岛 / 亚南极群岛 / 威尼斯泻湖 / 日本秘境",
     10944, 244, 136, "Prestige Stateroom 全私人阳台房 (18.5+4㎡)", 22.5, 8.5,
     9.4, "法式高定主餐厅 Le Rodrigues 與池畔烧烤，供应法式生牛肉塔塔、鸭肝酱、现烤羊角包与香槟",
     9.5, "1C级极地冰级船身、南极航次严格限载200人以内、随船法国极地博物学家与可直泊威尼斯内港的特权",
     9.3, "Jean-Philippe Nuel 设计的法式游艇内饰（天琴号采用威加蓝配色，北极号采用温暖灰木配色），95%客房带私人阳台",
     3450, 7, "2027-04-14 雅典–威尼斯亚得里亚海 7晚 ($3,450 起；南极13天 $12,995)", "一价全包(法餐+香槟红酒+岸上探险+Wi-Fi)",
     "人均吨位 41.45–55.00 GT（极地限载200人）、船员比 0.52–0.68，表格硬件分 9.30–12.30 + 法式高定游艇美学",
     "对应您《游轮数据》表中的 Ponant Boreal（4艘姊妹船）与《南极游轮》表第18行的 Le Lyrial（13天 $12,995）。",
     "https://us.ponant.com/", 45.43, 12.33, "Le Boreal ship", ""),

    ("oceania-regatta-insignia-nautica-sirena", "大洋邮轮·蕾佳塔号 / 徽章号 / 诺蒂卡号 / 赛琳娜号 (Oceania Regatta / Insignia / Nautica / Sirena)", "Oceania Cruises 大洋邮轮", "高档美食与文化精奢邮轮", "180天环球航线 / 亚马逊河 / 阿拉斯加小内湾 / 波利尼西亚",
     30277, 688, 373, "Veranda Stateroom / Penthouse Suite (20–30㎡)", 23.0, 8.5,
     9.7, "Polo Grill 干式熟成牛排馆、Toscana 纯正意大利餐厅、Red Ginger 亚洲料理与英式管弦乐下午茶",
     8.9, "大洋邮轮180天环游世界（Around the World）御用旗舰，能深入圣劳伦斯河、亚马逊河与波拉波拉泻湖",
     9.0, "耗资数千万美金完成「OceaniaNEXT」彻底翻新，水晶吊灯与温暖的新英格兰海岸庄园俱乐部格调",
     1699, 7, "2026-11-20 洛杉矶–墨西哥或迈阿密–加勒比 7晚 ($1,699 起)", "Your World Included(含全船特色牛排意餐厅+软饮咖啡+小费+Wi-Fi)",
     "人均吨位 44.01 GT、船员乘客比 0.54，表格硬件分 9.82 + 大洋王牌美食血统 + $1,699起的超高性价比",
     "想用不到两千美金吃遍大洋邮轮的 Polo Grill 牛排龙虾与 Toscana 意餐，这4艘三万吨级的 R-Class 小船是最佳敲门砖。",
     "https://www.oceaniacruises.com/", 25.77, -80.17, "MS Regatta", ""),

    ("phoenix-reisen-amera-amadea", "凤凰旅游·阿梅拉号 / 阿玛迪亚号 (Phoenix Reisen MS Amera / MS Amadea)", "Phoenix Reisen 德国凤凰邮轮", "高档美食与文化精奢邮轮", "格陵兰峡湾 / 挪威北角 / 黑海与地中海 / 环球航线",
     38848, 835, 440, "Balcony Cabin / Royal Suite (20–37㎡)", 24.0, 8.6,
     9.1, "德系精致全餐服务（含船长晚宴与Pichler's特色餐厅免费预订）、下午德式苹果卷蛋糕咖啡时光與午夜香肠啤酒局",
     9.2, "德国国民神剧《梦幻邮轮 (Das Traumschiff)》真实取景母船！航线极度硬核（直闯格陵兰伊卢利萨特冰湾与南美内河）",
     9.0, "原荷美经典名船 Prinsendam（皇家海盗船）重金改建，保留经典的360度全环绕实木散步甲板与阶梯式船尾",
     1850, 7, "2027-05-12 不来梅港–挪威峡湾 7晚 ($1,850 起)", "含全船正餐+Pichler's特色餐厅+下午茶点+欢迎香槟",
     "人均吨位 46.52 GT、船员乘客比 0.53，表格硬件分 9.92 + 德国《梦幻邮轮》传奇母船 + 稀缺360度环绕柚木散步甲板",
     "您在《游轮数据》表中专门收录的德国高档老钱船（38,848吨/835客/440船员），船尾层层叠叠的露台甲板是现代方盒子邮轮早已绝迹的古典美。",
     "https://www.phoenixreisen.com/", 53.54, 8.57, "MS Amera", ""),

    ("ncl-prima-viva-aqua-haven", "诺唯真邮轮·领途号 / 非凡号 / 水悦号 — The Haven 船中船殿堂 (Norwegian Prima / Viva / Aqua)", "Norwegian Cruise Line 诺唯真", "经典远洋皇后与旗舰级套房", "冰岛与北欧峡湾 / 地中海 / 加勒比海 / 百慕大",
     142500, 3099, 1506, "The Haven Penthouse / Duplex 3-Bedroom Villa (36–195㎡)", 40.0, 9.4,
     9.2, "The Haven 住客专属私密海景餐厅（全天供应波士顿龙虾、羊排与鹅肝）+ Palomar 地中海海鲜与 Onda by Scarpetta",
     9.8, "三层楼高跨海干式滑梯 The Drop（或 Aqua Slidecoaster 磁悬浮过山车滑水道）、三层海上电动卡丁车赛道与百老汇大秀",
     9.6, "意大利 Fincantieri 联合 Piero Lissoni 操刀，把 The Haven 移至船尾8层全封闭私享区，配专属直达电梯与船尾玻璃无边泳池",
     819, 7, "2026-11-29 奥兰多/迈阿密–加勒比 7晚 ($819 普通舱起；The Haven套房 $3,699 起)", "Free at Sea(含酒水套餐+特色餐厅+Wi-Fi；Haven含24小时管家与私享泳池)",
     "人均吨位 45.98 GT、船员乘客比 0.49，表格硬件分 9.46（主流大船中空间分与服务分双第一！）+ 船尾The Haven无边泳池",
     "您在《游轮数据》表中算出的亮眼高分：Prima级把14.25万吨船的载客压低到3,099人，硬件分高达 9.46，超过名人Edge与皇家Icon！",
     "https://www.ncl.com/", 25.77, -80.17, "Norwegian Prima",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Norwegian_Prima_in_Amsterdam_%28cropped%29.jpg/1280px-Norwegian_Prima_in_Amsterdam_%28cropped%29.jpg"),

    ("celebrity-edge-beyond-ascent-xcel", "名人邮轮·极点号 / 超越号 / 巅峰号 / Xcel — The Retreat & Edge Villa (Celebrity Edge Series)", "Celebrity Cruises 名人邮轮", "经典远洋皇后与旗舰级套房", "地中海 / 希腊群岛 / 加勒比海 / 阿拉斯加",
     130818, 2918, 1377, "Infinite Veranda / Sky Suite / Edge Villa双层带泳池别墅 (23–88㎡)", 32.0, 9.3,
     9.6, "米其林三星主厨 Daniel Boulud 全球唯一海上署名法餐厅《Le Voyage》+ 套房专属 Luminae 餐厅与伊甸园 Eden 晚宴",
     9.5, "全球独创船舷悬挑升降平台「魔毯 (Magic Carpet)」（在16层海面悬空喝香槟）、屋顶真植物花园与三层挑高 Eden 剧场",
     9.9, "Kelly Hoppen 爵士与 Nate Berkus 操刀设计，The Retreat 双层套房阳光甲板宛如伊比萨岛顶奢海滩俱乐部",
     989, 7, "2026-11-22 劳德代尔堡往返加勒比 7晚 ($989 无限阳台起，约 $141/晚；Retreat套房 $3,299 起)", "Retreat全包(Luminae米其林级套房餐厅+酒水+小费+星链Wi-Fi+管家)",
     "人均吨位 44.83 GT、船员乘客比 0.47，表格硬件分 9.20 + 米其林三星 Daniel Boulud 餐厅 + 悬挑海面13层楼的「魔毯」酒吧",
     "完全对应您《加勒比游轮价格》表中的 Celebrity（7晚 $989 / $141.3每晚），是10万吨以上大船中设计美学与餐饮公认的标杆。",
     "https://www.celebritycruises.com/", 26.08, -80.11, "Celebrity Beyond",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Celebrity_BEYOND_La_Rochelle.jpg/1280px-Celebrity_BEYOND_La_Rochelle.jpg"),

    ("cunard-queen-anne-victoria", "冠达邮轮·安妮女王号 / 维多利亚女王号 (Cunard Queen Anne / Queen Victoria)", "Cunard Line 冠达邮轮", "经典远洋皇后与旗舰级套房", "挪威峡湾 / 不列颠群岛 / 地中海 / 环球航线",
     114188, 2794, 1225, "Britannia Balcony / Princess & Queens Grill Suite (22–134㎡)", 30.0, 9.0,
     9.3, "米其林二星主厨 Michel Roux 监修英伦酒馆菜单與 Queens Grill 私密餐厅、Sir Samuel's 顶级牛排馆与白手套皇家下午茶",
     9.2, "Bright Lights Society 沉浸式歌舞剧酒廊、皇家交响乐团、击剑课程、Marella/Wellness Studio 水疗与正装Gala之夜",
     9.4, "2024年下水的冠达14年来首艘新船 Queen Anne 由设计大师 David Collins Studio（伦敦康诺特酒吧设计者）操刀，新装饰艺术风华绝代",
     999, 7, "2026-11-29 南安普敦往返西欧或挪威峡湾 7晚 ($999 起；Queens Grill套房 $3,199 起)", "含白手套英式下午茶+歌舞晚宴(Grill套房含专属餐厅与私人管家)",
     "人均吨位 40.87–43.27 GT，表格硬件分 8.47–8.65 + David Collins Studio 操刀英伦新装饰艺术 + 米其林二星 Michel Roux 合作菜单",
     "如果喜欢英式正装晚宴、白手套下午茶与交际舞会，又想要全新2024年下水的现代套房硬件，Queen Anne 是不二之选。",
     "https://www.cunard.com/", 50.90, -1.40, "Queen Anne ship", ""),

    ("virgin-voyages-scarlet-brilliant-lady", "维珍邮轮·绯红女士号 / 璀璨女士号 — RockStar 摇滚巨星套房 (Virgin Voyages Lady Ships)", "Virgin Voyages 维珍邮轮", "高档美食与文化精奢邮轮", "迈阿密与比米尼私人海滩 / 地中海伊比萨 / 阿拉斯加",
     110000, 2700, 1160, "Sea Terrace 吊床阳台房 / Mega RockStar 巨星套房 (21–195㎡)", 28.0, 8.9,
     9.5, "彻底废除大锅菜自助餐厅！全船20+间潮餐厅全部免费（The Wake 海景牛排龙虾、Extra Virgin 手工意面、Gunbae 韩式烤肉、Test Kitchen 分子料理）",
     9.6, "18岁以下严格禁入（Adults-Only）、比米尼岛私人海滩俱乐部篝火电音派对、红房间沉浸式杂技剧场与船上纹身店",
     9.5, "Tom Dixon 与 Roman and Williams 操刀，每间阳台标配手工编织红色摇床，RockStar套房配大理石窥视淋浴间与Richard's Rooftop香槟露台",
     927, 5, "2026-11-18 迈阿密–多米尼加–比米尼海滩俱乐部 5晚 ($927 起，约 $185/晚)", "一价全包(20+间特色餐厅全部免费+小费+星链Wi-Fi+健身团课+软饮)",
     "人均吨位 40.74 GT、船员乘客比 0.43，表格硬件分 8.37 + 全船20+间精品餐厅全免费 + 未来一年最低5晚仅 $927 ($185.4/晚)",
     "与您《加勒比游轮价格》表中的 Virgin（5晚 $927 / $185.4每晚）完全吻合！不仅没有熊孩子，连牛排馆、分子料理和小费都全包在船票里。",
     "https://www.virginvoyages.com/", 25.77, -80.17, "Scarlet Lady",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/IMO_9804801_-_Scarlet_Lady_alongside_in_Cozumel.jpg/1280px-IMO_9804801_-_Scarlet_Lady_alongside_in_Cozumel.jpg"),

    ("rci-icon-star-of-the-seas-suite", "皇家加勒比·海洋标志号 / 星际号 — Star Class 皇家府邸与双层套房 (Icon / Star of the Seas)", "Royal Caribbean 皇家加勒比", "经典远洋皇后与旗舰级套房", "东/西加勒比海 + 可可岛完美假日私人岛 (Perfect Day at CocoCay)",
     248663, 5610, 2350, "Icon Loft 双层复式 / Ultimate Family Townhouse 三层滑梯别墅 (61–233㎡)", 61.0, 9.6,
     9.3, "Empire Supper Club 八道式爵士配酒高定晚宴、Coastal Kitchen 套房专属海景餐厅與可可岛Hideaway成人海滩龙虾餐",
     10.0, "人类造船工程奇观：6条破纪录滑水道（Category 6水上乐园）、17米高玻璃穹顶瀑布高台跳水秀（AquaDome）、真冰花样滑冰场与皇冠边缘高空步道",
     9.8, "25万吨级八大主题社区设计，船尾 The Grove 双层套房阳光甲板设私人无边泳池，三层联排别墅自带滑梯直通冲浪公园",
     1299, 7, "2026-11-28 迈阿密/卡纳维拉尔港–加勒比与可可岛 7晚 ($1,299 普通舱起；Suite套房 $4,299 起)", "Star Class全包(皇家神仙教母Royal Genie管家+全船付费餐厅+酒水+小费+Wi-Fi)",
     "人均吨位 44.32 GT、船员乘客比 0.42，表格硬件分 8.62（25万吨巨无霸中空间比惊人！）+ 人类史上最强海上娱乐工程",
     "您在《游轮数据》表中录入的 Sovereign/Icon 数据（248,663吨/5,610客/2,350船员，硬件分 8.62），证明这艘25万吨巨轮的人均空间比许多10万吨船还宽敞。",
     "https://www.royalcaribbean.com/", 25.82, -77.94, "Icon of the Seas",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Icon_and_Mariner_Cozumel_Mexico_2024.jpg/1280px-Icon_and_Mariner_Cozumel_Mexico_2024.jpg"),

    ("aman-at-sea-amangati", "安缦海上超级游艇·Amangati (Aman at Sea)", "Aman 安缦集团 × Cruise Saudi", "顶奢风帆与高定超级游艇", "地中海里维埃拉 / 爱琴海 / 红海秘境",
     23000, 94, 150, "Aman Terrace Suite 超大私密露台套房 (68㎡)", 68.0, 10.0,
     9.9, "Nama 和魂怀石料理、地中海全天候餐厅、日式庭园茶室与安缦私藏年份香槟酒窖",
     9.4, "两座直升机停机坪、船尾直通海面的安缦海滩俱乐部（Beach Club）、两层楼高带有真实日式枯山水庭园的 Aman Spa",
     10.0, "SINOT Yacht Architecture & Design 操刀，全船仅47间68–354㎡超大套房，每间露台面积比普通邮轮整间客房还大",
     18500, 5, "2027-06-15 蒙特卡洛–波托菲诺–阿马尔菲 5晚 ($18,500 起)", "含早餐与水上俱乐部(高定餐饮按安缦酒店标准服务)",
     "人均吨位 244.68 GT、船员乘客比 1.60，表格硬件分高达 40.43 + 全船47间套房起步即 68㎡ + 船上日式枯山水禅意Spa",
     "安缦进军海洋的首艘183米超级游艇，设计理念是把整座安缦度假村原封不动搬上地中海。",
     "https://www.aman.com/yachts/amangati", 43.73, 7.42, "Amangati yacht",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Bonifacio.jpg/1280px-Bonifacio.jpg"),

    ("asuka-ii-iii-nyk", "日本邮船·飞鸟三号 / 飞鸟二号 (NYK Cruises Asuka III / Asuka II)", "NYK Cruises 日本邮船", "六星全套房顶奢远洋船", "日本环岛夏祭花火 / 北海道 / 小笠原群岛 / 环球航线",
     52200, 740, 470, "Midship Balcony / Royal Pentagon Suite (33–115㎡)", 33.0, 9.3,
     9.8, "6间免预约高定餐厅：Noblesse 法餐、海彦（Umihiko）江户前顶级寿司与割烹、Al Mare 炭火意餐与和牛铁板烧",
     9.3, "顶层全景露天展望大浴场（Grand Spa 泡着温泉看太平洋日落与日本花火大会）、高尔夫果岭与日本人间国宝级艺术展陈",
     9.6, "德国 Meyer Werft 船厂2025交付的LNG三燃料环保旗舰，全船所有客舱均配备千住博、平松礼二等日本巨匠真迹与深泡浴缸",
     2580, 4, "2026-11-24 横滨–鸟羽–纪伊半岛 4晚 ($2,580 起；日本环岛7晚 $4,390 起)", "含6间正餐厅全餐+大浴场温泉+下午茶(酒水单点)",
     "人均吨位 70.54 GT、船员乘客比 0.64，表格硬件分 13.41 + 全海景露天温泉大浴场 + 日本第一国民奢华母船",
     "日本老钱阶层最痴迷的本土旗舰，每年夏季「熊野/青森花火大会海上包厢航次」往往开售即秒空。",
     "https://www.asukacruise.co.jp/", 35.45, 139.65, "Asuka III",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/ASUKA_III_6223.jpg/1280px-ASUKA_III_6223.jpg"),

    ("quark-kapitan-khlebnikov-world-explorer", "夸克极地·赫列伯尼科夫船长号破冰船 / 世界探索者号 (Kapitan Khlebnikov / World Explorer)", "Quark Expeditions 夸克探险", "重型破冰与奢华极地科考", "南极帝企鹅栖息地 / 冠海豹浮冰区 / 南极圈深入段",
     12228, 110, 70, "polar Suite / Infinity Balcony Suite (22–25㎡)", 23.0, 8.4,
     8.7, "极地能量主厨全餐、俄罗斯与南美风味特色晚宴、图书馆24小时热可可与现烤曲奇",
     9.8, "传奇破冰船体深入普通邮轮无法靠近的重冰封海域、双人皮划艇、极地冰盖徒步与雪地露营",
     9.0, "フィンランド建造的极地重型破冰工程传奇（曾完成人类首次环航南极洲壮举）与现代混合动力World Explorer双星组合",
     7495, 10, "2026-11-16 乌斯怀亚–南极半岛探索 10晚 ($7,495 起；表列11天 $10,147)", "一价全包(极地冲锋艇登陆+佐餐酒水+夸克三合一冲锋衣)",
     "人均吨位 111.16 GT（Kapitan，表格硬件分 17.48）与 50.18 GT（World Explorer，硬件分 11.33），夸克极地王牌双雄",
     "直接对应您《游轮数据》表第6、7行及《南极游轮》表第16行（World Explorer 11天 $10,147）。",
     "https://www.quarkexpeditions.com/", -65.1, -64.0, "Kapitan Khlebnikov", ""),

    ("aurora-greg-mortimer-sylvia-earle", "极光探险·格雷格·莫蒂默号 / 西尔维娅·厄尔号 (Greg Mortimer / Sylvia Earle)", "Aurora Expeditions 澳洲极光探险", "重型破冰与奢华极地科考", "南极半岛 / 南乔治亚岛 / 苏格兰与挪威斯瓦尔巴",
     7892, 120, 105, "Balcony Stateroom 极地私人阳台舱 (21.5㎡)", 21.5, 8.4,
     8.8, "澳洲主厨团队料理的塔斯马尼亚牛排三文鱼、免费佐餐红白酒啤酒与池畔烧烤",
     10.0, "硬核户外玩家天花板：支持南极水肺深潜（Polar Scuba Diving）、高山滑雪登山、海冰攀冰、皮划艇与极地浮潜",
     9.6, "全球首艘采用 Ulstein X-BOW 倒弓形船首的极地探险船，船尾液压观鲸平台与4个低重心专属冲锋艇登艇口",
     8395, 11, "2026-11-20 乌斯怀亚–南极半岛 11天 ($8,395 早鸟起；表列均值 $10,795–$13,316)", "一价全包(冲锋艇登陆+佐餐红白酒+三合一极地防寒服+小费)",
     "人均吨位 65.77 GT、船员乘客比 0.88，表格硬件分 15.33 + 全球首艘 X-BOW 极地船 + 支持南极深潜与高山滑雪",
     "您在《南极游轮》表第4行和第6行重点标注的双子星（Greg Mortimer 11天 $10,795 / Sylvia Earle 12天 $13,316），仅载120人保证了全员每天两次超长登陆。",
     "https://www.aurora-expeditions.com/", -64.9, -63.2, "Greg Mortimer ship", ""),

    ("antarctica21-magellan-explorer", "南极21·麦哲伦探索者号飞航南极专船 (Magellan Explorer)", "Antarctica21 飞航南极专家", "重型破冰与奢华极地科考", "智利蓬塔阿雷纳斯 2小时直飞南极乔治王岛",
     4900, 73, 60, "Deluxe Veranda / Penthouse Suite 全私人阳台舱 (22–41㎡)", 22.0, 8.6,
     9.0, "智利巴塔哥尼亚帝王蟹、安第斯烤羔羊与精选智利名庄干红无限畅饮",
     9.9, "开创「Fly-Cruise 飞航南极」模式：乘专机2小时直接飞越魔鬼德雷克海峡，全船仅载73人，10艘Zodiac一次全员下船零等待",
     9.4, "按最新 PC6 极地冰级专门为飞航南极定制建造的精品科考游艇，船头全玻璃观察廊与湿式科学实验室",
     11995, 7, "2026-12-03 蓬塔阿雷纳斯双飞南极经典 8天7晚 ($11,995 起；表列 $12,995)", "一价全包(智利往返南极专机+酒水餐饮+冲锋艇登陆+极地靴服)",
     "人均吨位 67.12 GT、船员乘客比 0.82，表格硬件分 14.93 + 仅载73人全员同步登陆 + 2小时飞机免受4天晕船之苦",
     "对应您《南极游轮》表第2行（Magellan Explorer 4,900吨/73客/60船员，8天 $12,995），是时间宝贵或极度怕晕船者的南极神器。",
     "https://www.antarctica21.com/", -62.19, -58.96, "Magellan Explorer", ""),

    ("mitsui-nippon-maru", "商船三井·日本丸号经典美食名船 (MITSUI Nippon Maru / にっぽん丸)", "Mitsui Ocean Cruises 商船三井", "高档美食与文化精奢邮轮", "日本离岛秘境（屋久岛 / 利尻礼文岛 / 小笠原）",
     22472, 398, 230, "Deluxe Veranda / Grand Suite 和洋海景套房 (24–79㎡)", 25.0, 8.5,
     9.8, "在日本素有「美食的日本丸 (美食のにっぽん丸)」盛誉：名厨春日氏主理的和洋折衷晚宴、神户牛寿喜烧与传奇自烘焙面包",
     9.0, "海景展望大浴场、春日茶室正统日本茶道体验、日本夏祭阿波舞/东北睡魔祭专船包场",
     8.9, "2.2万吨紧凑典雅船身，可轻松穿过濑户内海最窄水道并停靠大型邮轮进不去的日本火山离岛",
     1480, 4, "2026-11-18 神户/横滨出发濑户内海美食巡游 4晚 ($1,480 起)", "含全船名厨正餐+宵夜乌冬+展望大浴场",
     "人均吨位 56.46 GT、船员乘客比 0.58，表格硬件分 11.43 + 日本公认「海上第一美食名船」",
     "您在《游轮数据》表第15行专门收录（22,472吨/398客/230船员），许多日本食客一年登船四五次只为吃它的四季旬味怀石。",
     "https://www.nipponmaru.jp/", 34.68, 135.19, "Nippon Maru cruise ship", ""),

    ("disney-dream-fantasy-magic", "迪士尼邮轮·梦想号 / 幻想号 / 魔力号礼宾套房 (Disney Dream / Fantasy / Magic)", "Disney Cruise Line 迪士尼邮轮", "经典远洋皇后与旗舰级套房", "加勒比海 / 巴哈马双私人岛 / 阿拉斯加冰川 / 欧洲",
     129690, 2500, 1458, "Deluxe Family Oceanview Verandah / Concierge Royal Suite (27–165㎡)", 27.6, 8.9,
     9.4, "米其林星级水准成人专属法餐厅《Remy》与意餐厅《Palo》+ 皇家宫殿/动画师调色板三大主题轮换晚宴",
     9.9, "全海上首个跨海透明盘旋水滑道 AquaDuck、百老汇级音乐剧、海盗之夜海上真烟花秀与3–17岁殿堂级分龄儿童俱乐部",
     9.5, "1930年代黄金远洋邮轮双烟囱流线船身，行业首创干湿分离双卫浴家庭阳台房（Split Bathrooms）",
     1350, 4, "2026-11-16 劳德代尔堡–巴哈马 4晚 ($1,350 起；7晚 $2,250 起)", "含三大轮换主题餐厅+百老汇大秀+24小时客房送餐+软饮冰淇淋",
     "人均吨位 51.88 GT、船员乘客比 0.58，表格硬件分 11.02 + AquaDuck跨海水滑道 + 亲子与三代同堂全球第一口碑",
     "对应您《游轮数据》表第71行（Disney Dream 129,690吨/2,500客/1,458船员，硬件分 11.02），其船员配比远高于同吨位普通大船。",
     "https://disneycruise.disney.go.com/", 25.07, -77.34, "Disney Dream", ""),

    ("hx-fridtjof-nansen-roald-amundsen", "海达路德探险·南森号 / 阿蒙森号混合动力极地船 (MS Fridtjof Nansen / Roald Amundsen)", "HX (Hurtigruten Expeditions) 海达路德", "重型破冰与奢华极地科考", "南极半岛 / 西北航道 / 格陵兰 / 挪威极光",
     20889, 499, 150, "Arctic Superior / Expedition Corner Suite (20–46㎡)", 25.0, 8.6,
     9.0, "Lindstrøm 极地高定餐厅（致敬阿蒙森南极探险队御厨）、Fredheim 国际街头美食与Aune挪威海鲜主餐厅",
     9.7, "全球首创混合动力电池组静音驶入冰川峡湾、占满整层的硬核「科学中心 (Science Center)」（配20台专业蔡司显微镜）与极地露营",
     9.4, "纯正挪威极地探险家百年传承（1896年创立），船尾无边恒温泳池与全景高空桑拿房直面南极冰山",
     4690, 9, "2027-04-12 雷克雅未克–格陵兰或英伦群岛 9晚 ($4,690 起；南极12天 $10,450)", "一价全包(科学中心讲座+冲锋艇巡游+佐餐酒水+HH探险冲锋衣+Wi-Fi)",
     "人均吨位 41.86 GT（南极航次限载500人内，每次100人轮换登陆），《南极游轮》表12天参考价 $10,450 + 全球首艘电池混动极地船",
     "直接对应您《南极游轮》表最后一行（Fridtjof Nansen 20,889吨，12天 $10,450），船上科学实验室硬核程度堪称海上大学。",
     "https://www.travelhx.com/", -64.8, -62.9, "MS Fridtjof Nansen", ""),

    ("holland-america-rotterdam-koningsdam-retreat", "荷美邮轮·鹿特丹号 / 国王号 — Neptun Suite 与古典音乐殿堂 (Holland America Rotterdam / Koningsdam)", "Holland America Line 荷美邮轮", "高档美食与文化精奢邮轮", "阿拉斯加冰川湾国家公园 / 挪威峡湾 / 加勒比与巴拿马运河",
     99863, 2650, 1036, "Verandah / Neptune Suite 海神顶奢套房 (22–66㎡)", 26.0, 8.6,
     9.4, "由全球7位名厨组成的「荷美美食委员会」监制：Morimoto by Sea（森本正治日料）、Pinnacle Grill 牛排、Sel de Mer 法式海鲜与每日鲜鱼计划",
     9.4, "拥有阿拉斯加「冰川湾国家公园 (Glacier Bay)」最高优先进湾配额！夜间 Music Walk 三大现场音乐厅（林肯中心古典室内乐/B.B. King蓝调/滚石摇滚）",
     9.0, "Adam D. Tihany 以小提琴曲线为灵感设计的三层中庭与270度环幕 World Stage 剧场",
     849, 7, "2026-11-28 劳德代尔堡–加勒比 7晚 ($849 起，约 $121/晚；阿拉斯加冰川湾7晚 $1,099 起)", "Have It All套餐(含酒水+特色牛排日料餐厅+岸上游补贴+Wi-Fi)",
     "人均吨位 37.68–42.96 GT，表格硬件分 7.68–8.77 + 阿拉斯加冰川湾最强航权 + 未来一年7晚最低仅 $849 ($121/晚)",
     "对应您《加勒比游轮价格》表中的 Holland America（7晚 $849 / $121.3每晚），其「全球鲜鱼计划」保证从捕捞上岸到餐桌不超过48小时。",
     "https://www.hollandamerica.com/", 58.60, -136.15, "MS Rotterdam ship", ""),

    ("princess-sun-star-sanctuary-collection", "公主邮轮·太阳公主号 / 星辰公主号 — Sanctuary 圣殿船中船系列 (Sun / Star Princess)", "Princess Cruises 公主邮轮", "经典远洋皇后与旗舰级套房", "地中海 / 加勒比海 / 阿拉斯加",
     175500, 4314, 1600, "Sanctuary Mini-Suite / Sky Suite (30–117㎡)", 31.0, 9.0,
     9.3, "世界第一屠夫 Dario Cecchini 联名托斯卡纳牛排馆《Butcher's Block》、Umai 日式铁板烧、Catch by Rudi 海鲜与 Love by Britto 高空分子景观餐厅",
     9.5, "三层玻璃球形穹顶剧场《The Dome》（灵感来自圣托里尼露台）、Spellbound by Magic Castle 维多利亚魔术秘境酒吧与船尾无边泳池",
     9.5, "公主邮轮史上最颠覆的 Sphere 级LNG旗舰，船中段外凸巨型玻璃球体与顶层 Sanctuary Club 成人专属香槟泳池甲板",
     808, 7, "2026-11-21 劳德代尔堡–加勒比 7晚 ($808 普通舱起，约 $115/晚；Sanctuary圣殿套房 $2,499 起)", "Sanctuary Collection全包(专属圣殿餐厅+专属顶层泳池+Premier酒水+无限特色餐厅+Wi-Fi)",
     "人均吨位 40.68 GT、船员乘客比 0.37，表格硬件分 7.78 + 圣托里尼灵感玻璃巨蛋 The Dome + 未来一年7晚最低 $808",
     "完全对应您《游轮数据》表的 Princess Sphere（175,500吨/4,314客）与《加勒比游轮价格》表（7晚 $808 / $115.4每晚）。",
     "https://www.princess.com/", 26.08, -80.11, "Sun Princess ship", ""),

    ("msc-world-europa-america-yacht-club", "MSC地中海邮轮·欧罗巴号 / 美洲号 — Yacht Club 游艇会双层复式套房 (MSC World Class Yacht Club)", "MSC Cruises 地中海邮轮", "经典远洋皇后与旗舰级套房", "地中海西线 / 迈阿密–加勒比私人海洋保护区岛 (Ocean Cay)",
     215863, 5228, 2138, "MSC Yacht Club Deluxe / Duplex Suite with Whirlpool (25–104㎡)", 35.0, 9.2,
     9.1, "Yacht Club 船首私密海景法式/意式餐厅、Chef's Garden Kitchen（米其林星厨 Niklas Ekstedt 水培花园餐厅）与 La Pescaderia 地中海鲜鱼市场",
     9.6, "跨越11层甲板的干式螺旋滑梯 Venom Drop、船上精酿啤酒厂、巴哈马 Ocean Cay 私人生态岛过夜灯光秀与游艇会专属海滩别墅",
     9.5, "90度垂直劈浪船首与Y字形船尾104米露天欧式海景步行街（World Promenade），船头黄金位置全部留给 Yacht Club 游艇会",
     599, 7, "2026-11-27 热那亚/巴塞罗那或迈阿密 7晚 ($599 普通舱起；Yacht Club游艇会全包套房 $2,399 起)", "Yacht Club一价全包(24小时白手套英式管家+私密餐厅+全船酒水+热疗Spa+Wi-Fi)",
     "人均吨位 41.29 GT、船员乘客比 0.41，表格硬件分 8.22 + 欧洲最懂「船中船」私密特权的 Yacht Club 游艇会",
     "对应您《游轮数据》表的 215,863吨旗舰与《加勒比游轮价格》表的 $599/7晚底价，花两千多美金订 Yacht Club 即可享受24小时管家优先上下船特权。",
     "https://www.msccruisesusa.com/", 44.41, 8.92, "MSC World Europa",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/MSC_World_Europa_La_Rochelle.jpg/1280px-MSC_World_Europa_La_Rochelle.jpg"),

    ("star-clippers-royal-clipper", "星船邮轮·皇家快船号五桅全横帆巨舰 (Star Clippers Royal Clipper)", "Star Clippers 星船帆船邮轮", "顶奢风帆与高定超级游艇", "阿马尔菲与西西里 / 希腊基克拉泽斯群岛 / 加勒比格林纳丁斯",
     5000, 227, 106, "Deluxe Deck / Owner's Suite 古典航海套房 (15–30㎡)", 19.0, 8.0,
     8.9, "三层挑高中庭主餐厅无拘束欧陆料理、甲板热带水果生蚝早午餐与库拉索海滩烧烤",
     9.7, "吉尼斯世界纪录认证「全球最大真正全横帆船（42张帆总面积5,202㎡）」！允许乘客系安全绳爬上桅杆瞭望台（Mast Climbing）与躺船头网兜看海豚",
     9.6, "以1902年传奇五桅风帆巨舰 Preussen 号为蓝本建造，船底设水下玻璃舷窗的三层Captain Nemo水疗中心",
     1980, 7, "2026-12-05 芭芭多斯往返向风群岛或罗马–阿马尔菲 7晚 ($1,980 起)", "含三餐下午茶+免费滑水帆板皮划艇+爬桅杆体验",
     "人均吨位 22.03 GT、船员乘客比 0.47，表格硬件分 6.87 + 吉尼斯认证全球最大5桅42帆真横帆船 + 船首悬空绳网看海",
     "您在《游轮数据》表第211行收录的大航海时代活化石（5,000吨/227客/106船员），躺在船头长鼻斜桅下的绳网里任海浪在身下翻涌，终生难忘。",
     "https://www.starclippers.com/", 13.09, -59.61, "Royal Clipper", "")
]


def fetch_wiki_image(query):
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": "6",
        "gsrlimit": "6",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": "1280",
        "format": "json"
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "OceanicAtlasGuide/1.0 (https://xtxsinan.github.io/destination_rankings/; research@example.org) Python-urllib/3"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, p in sorted(pages.items(), key=lambda x: x[1].get("index", 99)):
                title = p.get("title", "")
                if any(bad in title.lower() for bad in ["map", "logo", "flag", "icon", "svg", "route", "deck"]):
                    continue
                ii = p.get("imageinfo", [{}])[0]
                thumb = ii.get("thumburl") or ii.get("url")
                if thumb:
                    return thumb, title.replace("File:", "")
            return "", ""
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2.5 * (attempt + 1))
                continue
            return "", ""
        except Exception:
            return "", ""
    return "", ""


def main():
    redundant_sister_ids = {
        "seabourn-odyssey-sojourn-quest",
        "silversea-silver-shadow-whisper",
        "silversea-silver-cloud-wind",
        "hapag-lloyd-europa",
        "regent-seven-seas-navigator",
        "oceania-marina-riviera",
        "oceania-regatta-insignia-nautica-sirena",
        "ponant-boreal-austral-lyrial-soleal",
        "quark-kapitan-khlebnikov-world-explorer",
        "quark-ocean-explorer",
        "lindblad-ng-explorer-orion",
        "mitsui-nippon-maru",
        "disney-dream-fantasy-magic",
        "cunard-queen-anne-victoria",
        "hx-fridtjof-nansen-roald-amundsen",
        "holland-america-rotterdam-koningsdam-retreat",
        "princess-sun-star-sanctuary-collection",
        "msc-world-europa-america-yacht-club",
        "star-clippers-royal-clipper"
    }
    filtered_cruises = [r for r in RAW_CRUISES if r[0] not in redundant_sister_ids]
    assert len(filtered_cruises) == 50, f"Expected 50 cruises, got {len(filtered_cruises)}"

    items = []
    for row in filtered_cruises:
        (cid, name, brand, domain, region, tonnage_num, pax, crew,
         entry_suite, suite_sqm, room_score,
         dining_score, dining_hl,
         activity_score, activity_hl,
         design_score, design_hl,
         lowest_price, lowest_nights, verified_sailing, all_inc,
         highlight, tip, url, lat, lon, wiki_q, preset_img) = row

        space_ratio = round(tonnage_num / pax, 2)
        service_ratio = round(crew / pax, 3)
        # Exact formula from user's '游轮数据' sheet: Space/10 + Service*10
        space_score = round(space_ratio / 10.0, 2)
        service_score = round(service_ratio * 10.0, 2)
        sheet_score = round(space_score + service_score, 2)

        # 6-Dimension Total Score = Space/10 + Service*10 + Room + Dining + Activity + Design
        total_score = round(space_score + service_score + room_score + dining_score + activity_score + design_score, 2)
        per_night = round(lowest_price / lowest_nights)
        price_per_sqm = round(per_night / suite_sqm, 1)

        img_url = preset_img
        img_credit = ""
        if not img_url:
            img_url, img_credit = fetch_wiki_image(wiki_q)
            if not img_url:
                img_url, img_credit = fetch_wiki_image(brand.split()[0] + " cruise ship")
            print(f"Fetched [{cid}] -> {img_credit or img_url[:60]}")
            time.sleep(0.3)
        else:
            img_credit = img_url.split("/")[-1]

        items.append({
            "id": cid,
            "name": name,
            "brand": brand,
            "domain": domain,
            "region": region,
            "tonnage": f"{tonnage_num:,} 吨",
            "tonnageNum": tonnage_num,
            "pax": pax,
            "crew": crew,
            "crewRatio": f"1 : {round(pax / crew, 2)} (船员比 {service_ratio:.2f})",
            "spaceRatio": space_ratio,
            "spaceScore": space_score,
            "serviceRatio": service_ratio,
            "serviceScore": service_score,
            "sheetScore": sheet_score,
            "entrySuiteName": entry_suite,
            "suiteSqm": suite_sqm,
            "roomScore": room_score,
            "diningScore": dining_score,
            "diningHighlight": dining_hl,
            "activityScore": activity_score,
            "activityHighlight": activity_hl,
            "designScore": design_score,
            "designHighlight": design_hl,
            "totalScore": total_score,
            "lowestPriceUsd": lowest_price,
            "lowestNights": lowest_nights,
            "perNightUsd": per_night,
            "sampleTotalUsd": f"${lowest_price:,} 起 / {lowest_nights}晚",
            "pricePerSqmPerNightUsd": price_per_sqm,
            "allInclusiveLevel": all_inc,
            "verifiedSailing": verified_sailing,
            "highlight": highlight,
            "tip": tip,
            "url": url,
            "image": img_url,
            "imageCredit": img_credit,
            "lat": lat,
            "lon": lon
        })

    # Sort by 6-dimension totalScore descending
    items.sort(key=lambda x: (-x["totalScore"], -x["sheetScore"]))
    max_total = items[0]["totalScore"]
    for idx, item in enumerate(items, 1):
        item["rank"] = idx
        # Also provide a 100-point normalized score for quick reading
        item["score100"] = round(78.0 + (item["totalScore"] / max_total) * 21.5, 1)
        if idx <= 12:
            item["tier"] = "T0"
        elif idx <= 28:
            item["tier"] = "T1"
        elif idx <= 40:
            item["tier"] = "T1.5"
        else:
            item["tier"] = "T2"

    out_js = (
        "// Global Top 50 High-End & Luxury Cruises — Evaluated by '游轮数据' Sheet Method + 6 Dimensions & Next-12-Months Lowest Prices\n"
        f"window.LUXURY_CRUISES_TOP50 = {json.dumps(items, ensure_ascii=False, indent=2)};\n"
    )
    (ROOT / "data_cruises_top50.js").write_text(out_js, encoding="utf-8")
    print(f"Wrote data_cruises_top50.js with {len(items)} high-end cruises.")

    # Generate markdown table in rankings/cruises_top50.md
    md = [
        "# 全球高档与奢华邮轮 Top 50（基于《邮轮数据》Sheet 6维模型 + 未来一年最低价）\n",
        "> **评分公式说明**：严格采用《邮轮数据》Sheet 定量算法：`人均Tonnage得分 = (Tonnage / Passengers) / 10`，`Crew乘客比得分 = (Crew / Passengers) * 10`，两者之和即为表格原始硬件分 `Sheet Total = Space/10 + Service*10`；并叠加 **房间大小 (10分)**、**餐饮水准 (10分)**、**船上活动水准 (10分)**、**邮轮设计 (10分)** 构成 **6维综合总分**。每艘邮轮均附 **未来一年（2026.11–2027.10）最低起价**。\n",
        "| 排名 | 邮轮名称 | 品牌/分类 | 吨位 (GT) | 载客 | 船员 | 人均吨位 (Space) | 船员乘客比 (Service) | 表格硬件分 | 房间面积/得分 | 餐饮 | 活动 | 设计 | 6维总分 | 未来一年最低价格 (航次) |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---|"
    ]
    for c in items:
        md.append(
            f"| {c['rank']} | **{c['name']}** | {c['brand']} · {c['domain']} | {c['tonnageNum']:,} | {c['pax']} | {c['crew']} | "
            f"{c['spaceRatio']:.1f} ({c['spaceScore']:.2f}) | {c['serviceRatio']:.2f} ({c['serviceScore']:.2f}) | **{c['sheetScore']:.2f}** | "
            f"{c['suiteSqm']}㎡ ({c['roomScore']:.1f}) | {c['diningScore']:.1f} | {c['activityScore']:.1f} | {c['designScore']:.1f} | "
            f"**{c['totalScore']:.2f}** | **{c['sampleTotalUsd']}** (${c['perNightUsd']}/晚 · {c['verifiedSailing']}) |"
        )
    (ROOT / "rankings" / "cruises_top50.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Wrote rankings/cruises_top50.md")


if __name__ == "__main__":
    main()

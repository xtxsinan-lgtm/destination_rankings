#!/usr/bin/env python3
"""
Expands Aquariums from 35 to 50 and Zoos from 30 to 50 in data_aquariums_zoos_museums.js,
fetches Wikimedia Commons photos into images_themed.js, and updates markdown rankings.
"""
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NEW_AQUARIUMS = [
    {
        "rank": 36,
        "name": "热那亚水族馆 (Acquario di Genova)",
        "country": "意大利",
        "city": "热那亚",
        "tier": "T2",
        "highlight": "建筑大师伦佐·皮亚诺设计的旧港巨舰，欧洲历史最悠久、物种最全的70个生态大缸与海牛、地中海海豚半水下馆",
        "id": "aq-genoa",
        "lat": 44.410,
        "lon": 8.926,
        "totalVolumeML": 6000,
        "mainTankML": 1200,
        "windowSize": "伦佐·皮亚诺设计的双层地中海宽吻海豚露天+水下全景长廊",
        "speciesCount": 400,
        "animalCount": 12000,
        "ticketUsd": 32,
        "durationHours": "3–4 小时",
        "bestFor": ["建筑美学控", "欧洲亲子", "海牛与海豚迷"],
        "tip": "由普利兹克奖得主 Renzo Piano 为1992年世博会设计，海豚馆分上下两层：上层听海豚呼吸声，下层透过24米长亚克力窗看海豚水下翻滚。",
        "search_q": "Acquario di Genova aquarium"
    },
    {
        "rank": 37,
        "name": "东京墨田水族馆＋池袋阳光水族馆 (Sumida & Sunshine Aquarium)",
        "country": "日本",
        "city": "东京（押上 / 池袋）",
        "tier": "T2",
        "highlight": "晴空塔下小笠原群岛深海巨缸与宫崎骏式「天空企鹅」悬挑屋顶水池，把沙虎鲨、企鹅与高空城市天际线融为一体",
        "id": "aq-sumida-sunshine",
        "lat": 35.710,
        "lon": 139.810,
        "totalVolumeML": 1200,
        "mainTankML": 350,
        "windowSize": "阳光城60米高空「天空企鹅」悬挑弧形顶棚＋墨田350吨开放式企鹅池",
        "speciesCount": 550,
        "animalCount": 15000,
        "ticketUsd": 18,
        "durationHours": "3–4 小时",
        "bestFor": ["情侣出片", "水母与企鹅控", "都市夜游"],
        "tip": "池袋阳光水族馆屋顶的「天空企鹅（Sky Penguins）」让非洲企鹅在东京摩天大楼顶上飞翔；墨田水族馆则拥有日本最大的室内开放式企鹅池与万花筒水母隧道。",
        "search_q": "Sumida Aquarium Tokyo penguin"
    },
    {
        "rank": 38,
        "name": "新江之岛水族馆 (Enoshima Aquarium)",
        "country": "日本",
        "city": "神奈川藤泽（镰仓湘南海岸）",
        "tier": "T2",
        "highlight": "正对富士山与江之岛海景，8000尾沙丁鱼银色龙卷风「相模湾大水槽」与全球最具艺术感的球形梦幻水母厅",
        "id": "aq-enoshima",
        "lat": 35.309,
        "lon": 139.480,
        "totalVolumeML": 2200,
        "mainTankML": 1000,
        "windowSize": "高8米×宽12米相模湾波浪大水槽（8000尾沙丁鱼风暴）",
        "speciesCount": 500,
        "animalCount": 20000,
        "ticketUsd": 19,
        "durationHours": "2.5–3.5 小时",
        "bestFor": ["情侣出片", "水母控", "镰仓一日游"],
        "tip": "逛完镰仓高校前站步行即达。海豚表演场背后的背景不是幕布，而是真实的湘南海岸、江之岛与远处的富士山（晴天傍晚绝美）。",
        "search_q": "Enoshima Aquarium Sagami Bay tank"
    },
    {
        "rank": 39,
        "name": "鸟羽水族馆 (Toba Aquarium)",
        "country": "日本",
        "city": "三重县鸟羽",
        "tier": "T2",
        "highlight": "全日本饲养物种数第一（1200种）！亚洲唯一能看到美人鱼原型「儒艮 (Dugong)」Serena、非洲海牛与网红海獭的活化石殿堂",
        "id": "aq-toba",
        "lat": 34.482,
        "lon": 136.846,
        "totalVolumeML": 3500,
        "mainTankML": 800,
        "windowSize": "美人鱼之海（儒艮专属海草床深水窗）＋珊瑚礁潜水长廊",
        "speciesCount": 1200,
        "animalCount": 30000,
        "ticketUsd": 19,
        "durationHours": "3–4 小时",
        "bestFor": ["稀有物种控", "自然科普迷", "海獭与儒艮粉丝"],
        "tip": "没有固定参观路线，全馆12个生态区自由探索。镇馆之宝是雌性儒艮 Serena（自1987年饲养至今）以及会捧脸卖萌的明星海獭 Mei 与 Kira。",
        "search_q": "Toba Aquarium dugong"
    },
    {
        "rank": 40,
        "name": "墨尔本＋悉尼达令港海洋生物馆 (SEA LIFE Melbourne & Sydney)",
        "country": "澳大利亚",
        "city": "墨尔本 / 悉尼",
        "tier": "T2",
        "highlight": "220万升南大洋360度环形深海鲨鱼隧道、5米长巨型咸水鳄 Pinjarra 水下视窗与悉尼大堡礁儒艮岛",
        "id": "aq-melbourne-sydney",
        "lat": -37.821,
        "lon": 144.958,
        "totalVolumeML": 4800,
        "mainTankML": 2200,
        "windowSize": "220万升南大洋360度环形深海观景厅＋大堡礁双海底隧道",
        "speciesCount": 650,
        "animalCount": 18000,
        "ticketUsd": 34,
        "durationHours": "2.5–4 小时",
        "bestFor": ["巨物深海控", "南半球特有物种", "带娃亲子"],
        "tip": "墨尔本馆的真冰雪南极企鹅馆（国王企鹅+巴布亚企鹅）与巨型澳洲锯鳐极具震撼力；悉尼馆则拥有大堡礁昼夜变化剧场与憨态可掬的儒艮 Pig。",
        "search_q": "Sea Life Sydney Aquarium tunnel"
    },
    {
        "rank": 41,
        "name": "珀斯西澳水族馆 (AQWA - Aquarium of Western Australia)",
        "country": "澳大利亚",
        "city": "珀斯（希拉里斯船港）",
        "tier": "T2",
        "highlight": "南半球最长98米水下海底步行隧道，浓缩西澳12000公里狂野海岸线，看4米沙虎鲨、红代鳐与仙气飘飘的叶海龙",
        "id": "aq-aqwa-perth",
        "lat": -31.827,
        "lon": 115.738,
        "totalVolumeML": 4000,
        "mainTankML": 3000,
        "windowSize": "98米长全透明海底传送带隧道（300万升沉船海岸大缸）",
        "speciesCount": 400,
        "animalCount": 8000,
        "ticketUsd": 22,
        "durationHours": "2–3 小时",
        "bestFor": ["海底隧道控", "浮潜体验", "西澳生态迷"],
        "tip": "不仅能走过98米海底隧道，持证潜水员或普通游客还可以报名「Dive/Snorkel with Sharks」，直接下潜进300万升主缸与沙虎鲨、海龟同游。",
        "search_q": "AQWA Aquarium of Western Australia"
    },
    {
        "rank": 42,
        "name": "波士顿新英格兰水族馆 (New England Aquarium)",
        "country": "美国",
        "city": "波士顿",
        "tier": "T2",
        "highlight": "现代中庭水族馆鼻祖：四层楼高76万升360度圆柱形「巨型加勒比珊瑚礁海塔 (Giant Ocean Tank)」，螺旋步道环绕看千年绿海龟 Myrtle",
        "id": "aq-new-england",
        "lat": 42.359,
        "lon": -71.049,
        "totalVolumeML": 3200,
        "mainTankML": 760,
        "windowSize": "四层楼高×直径12米360度全透明圆柱珊瑚礁海塔",
        "speciesCount": 600,
        "animalCount": 20000,
        "ticketUsd": 34,
        "durationHours": "2.5–3.5 小时",
        "bestFor": ["建筑空间迷", "海龟与企鹅控", "观鲸联游"],
        "tip": "底层被80多只非洲企鹅与跳岩企鹅的开放式礁石岛包围，顺着螺旋坡道盘旋而上，可以从海床一直看到海面550磅重的明星绿海龟 Myrtle。",
        "search_q": "New England Aquarium Giant Ocean Tank"
    },
    {
        "rank": 43,
        "name": "得州州立水族馆 (Texas State Aquarium)",
        "country": "美国",
        "city": "得州科珀斯克里斯蒂",
        "tier": "T2",
        "highlight": "斥资5000万美金建成《加勒比秘境 (Caribbean Journey)》，拥有21米长全亚克力尤卡坦蓝洞沉船巨幕与墨西哥湾海上钻井平台鲨鱼缸",
        "id": "aq-texas-state",
        "lat": 27.814,
        "lon": -97.392,
        "totalVolumeML": 4500,
        "mainTankML": 1500,
        "windowSize": "宽21米×高3.8米加勒比H.M.S.沉船长卷窗＋钻井平台钢柱深海窗",
        "speciesCount": 460,
        "animalCount": 9000,
        "ticketUsd": 40,
        "durationHours": "3–4 小时",
        "bestFor": ["沉船巨幕控", "带娃亲子", "航母联游"],
        "tip": "紧邻列克星敦号航空母舰博物馆（USS Lexington），一天可同时打卡二战航母与全美最惊艳的加勒比蓝洞沉船大缸。",
        "search_q": "Texas State Aquarium Corpus Christi"
    },
    {
        "rank": 44,
        "name": "密苏里奇观与野生动物国家博物馆水族馆 (Wonders of Wildlife)",
        "country": "美国",
        "city": "密苏里州斯普林菲尔德",
        "tier": "T2",
        "highlight": "Bass Pro创始人历时10年耗资3亿美金打造的史诗级水下迷宫，2.4公里沉浸动线穿越深海沉船、大西洋蓝鳍金枪鱼风暴与亚马逊雨林",
        "id": "aq-wonders-wildlife",
        "lat": 37.181,
        "lon": -93.297,
        "totalVolumeML": 5700,
        "mainTankML": 1900,
        "windowSize": "190万升开阔大洋环形剧场＋深海二战沉船穹顶隧道",
        "speciesCount": 800,
        "animalCount": 35000,
        "ticketUsd": 45,
        "durationHours": "4–5 小时",
        "bestFor": ["沉浸造景控", "海钓与巨鱼迷", "全天深度游"],
        "tip": "多次力压乔治亚水族馆被《今日美国》评为全美第一水族馆，内部造景堪比迪士尼环球影城，连罕见的巨型大西洋大海鲢与蓝鳍金枪鱼都能近距离仰视。",
        "search_q": "Wonders of Wildlife Aquarium Springfield"
    },
    {
        "rank": 45,
        "name": "犹他州洛夫兰活体星球水族馆 (Loveland Living Planet Aquarium)",
        "country": "美国",
        "city": "犹他州盐湖城（德雷珀）",
        "tier": "T2",
        "highlight": "在落基山脉内陆荒原造出114万升深海鲨鱼大缸与12米无框架海底隧道，户外矗立U2演唱会同款巨型「生态爪」地标",
        "id": "aq-loveland-living-planet",
        "lat": 40.531,
        "lon": -111.894,
        "totalVolumeML": 3800,
        "mainTankML": 1140,
        "windowSize": "12米长无拼接缝亚克力深海鲨鱼与绿海龟隧道",
        "speciesCount": 550,
        "animalCount": 4500,
        "ticketUsd": 29,
        "durationHours": "2.5–3.5 小时",
        "bestFor": ["海底隧道控", "雨林生态迷", "盐湖城亲子"],
        "tip": "除了深海大缸和巴布亚企鹅馆，馆内还把云豹、水獭、树懒与巨骨舌鱼融进了四层楼高的南美云雾雨林步道。",
        "search_q": "Loveland Living Planet Aquarium Utah"
    },
    {
        "rank": 46,
        "name": "大加那利岛海之诗水族馆 (Poema del Mar)",
        "country": "西班牙",
        "city": "大加那利岛拉斯帕尔马斯",
        "tier": "T2",
        "highlight": "鹦鹉公园 (Loro Parque) 家族巅峰力作：拥有宽36米×高7.35米、厚达39厘米的全球最大曲面亚克力深海巨幕《Deep Sea》",
        "id": "aq-poema-del-mar",
        "lat": 28.144,
        "lon": -15.428,
        "totalVolumeML": 8500,
        "mainTankML": 5500,
        "windowSize": "宽36米×高7.35米全球最大单片曲面亚克力深海观景窗（140吨重）",
        "speciesCount": 350,
        "animalCount": 15000,
        "ticketUsd": 30,
        "durationHours": "2.5–3.5 小时",
        "bestFor": ["巨幕深海控", "加那利海岛游", "视觉震撼"],
        "tip": "分丛林、珊瑚礁（圆柱形360度大缸）与深海三部曲。走进最后的大洋厅，36米长的弯曲巨幕把双髻鲨、沙虎鲨与魔鬼鱼像IMAX电影一样包裹在眼前。",
        "search_q": "Poema del Mar aquarium Gran Canaria"
    },
    {
        "rank": 47,
        "name": "马略卡岛帕尔马水族馆 (Palma Aquarium)",
        "country": "西班牙",
        "city": "马略卡岛帕尔马",
        "tier": "T2",
        "highlight": "拥有欧洲最深的8.5米鲨鱼主缸《Big Blue》（350万升水体），欧洲规模最大的活体造礁珊瑚群落与地中海海龟救援中心",
        "id": "aq-palma",
        "lat": 39.531,
        "lon": 2.729,
        "totalVolumeML": 5000,
        "mainTankML": 3500,
        "windowSize": "水深8.5米×长33米《Big Blue》深渊鲨鱼窗＋透明过顶隧道",
        "speciesCount": 700,
        "animalCount": 8000,
        "ticketUsd": 31,
        "durationHours": "3–4 小时",
        "bestFor": ["地中海度假联游", "活体珊瑚迷", "深潜体验"],
        "tip": "马略卡岛海滨度假必去。游客可以乘透明底小船「Shark Vision Boat」漂浮在8.5米深的鲨鱼大缸正上方俯瞰11条沙虎鲨与沙洲鲨。",
        "search_q": "Palma Aquarium Mallorca Big Blue"
    },
    {
        "rank": 48,
        "name": "施特拉尔松德海洋博物馆 (Ozeaneum Stralsund)",
        "country": "德国",
        "city": "施特拉尔松德（波罗的海沿岸）",
        "tier": "T2",
        "highlight": "荣膺欧洲年度最佳博物馆：260万升大西洋公海鱼群风暴大缸、顶层洪堡企鹅海景露台与1:1全尺寸蓝鲸/抹香鲸战巨型乌贼展厅",
        "id": "aq-stralsund-ozeaneum",
        "lat": 54.315,
        "lon": 13.097,
        "totalVolumeML": 6000,
        "mainTankML": 2600,
        "windowSize": "水深9米大西洋公海沉船大窗＋波罗的海至北海50个冷水水族箱",
        "speciesCount": 400,
        "animalCount": 7000,
        "ticketUsd": 22,
        "durationHours": "3–4 小时",
        "bestFor": ["冷水海洋控", "建筑与巨鲸迷", "科普硬核玩家"],
        "tip": "建筑外观如波罗的海被风吹鼓的白色船帆。躺在最后一厅《1:1海洋巨兽》的懒人沙发上，头顶悬吊着26米真尺寸蓝鲸、座头鲸和抹香鲸搏斗大王乌贼，配合深海鲸歌极其震撼。",
        "search_q": "Ozeaneum Stralsund aquarium"
    },
    {
        "rank": 49,
        "name": "里约热内卢海洋水族馆 (AquaRio)",
        "country": "巴西",
        "city": "里约热内卢（奇迹港）",
        "tier": "T2",
        "highlight": "南美洲规模最大的海洋水族馆：由港口百年冷库改建，350万升《Recinto Oceânico》大洋主缸与全透明海底隧道",
        "id": "aq-aqua-rio",
        "lat": -22.893,
        "lon": -43.192,
        "totalVolumeML": 4500,
        "mainTankML": 3500,
        "windowSize": "水深7米×350万升南大西洋主观景巨幕＋海底过顶隧道",
        "speciesCount": 350,
        "animalCount": 10000,
        "ticketUsd": 26,
        "durationHours": "2–3 小时",
        "bestFor": ["海底隧道控", "南美旅行打卡", "带娃亲子"],
        "tip": "位于里约奥运复兴区 Porto Maravilha，轻轨 VLT 直达，馆内允许预约夜宿海底隧道（Dormindo no AquaRio）。",
        "search_q": "AquaRio Rio de Janeiro aquarium"
    },
    {
        "rank": 50,
        "name": "杭州长乔极地海洋公园 (Hangzhou Polar Ocean Park)",
        "country": "中国",
        "city": "浙江杭州（湘湖）",
        "tier": "T2",
        "highlight": "长三角规模最大的极地与深海双栖馆：国内罕见的领航鲸与白鲸水下剧场、北极熊冰海视窗及千吨级珊瑚礁圆形穹顶",
        "id": "aq-hangzhou-polar",
        "lat": 30.132,
        "lon": 120.221,
        "totalVolumeML": 12000,
        "mainTankML": 3200,
        "windowSize": "领航鲸与白鲸深水全景巨幕＋360度海底隧道与水母梦幻宫",
        "speciesCount": 500,
        "animalCount": 25000,
        "ticketUsd": 48,
        "durationHours": "4–5 小时",
        "bestFor": ["江浙沪亲子", "白鲸与极地迷", "周末度假"],
        "tip": "紧邻杭州湘湖景区，全馆19个主题展区，其中白鲸海的水下弧形大窗与极地企鹅岛是江浙沪带娃出片的首选。",
        "search_q": "Beluga whale aquarium underwater"
    }
]

NEW_ZOOS = [
    {
        "rank": 31,
        "name": "维也纳美泉宫动物园 (Tiergarten Schönbrunn)",
        "country": "奥地利",
        "city": "维也纳",
        "tier": "T2",
        "highlight": "创立于1752年的全球最古老动物园，在哈布斯堡皇室巴洛克庭院周围看大熊猫、北极熊水下冰海世界与婆罗洲雨林温室",
        "id": "zoo-vienna-schonbrunn",
        "lat": 48.182,
        "lon": 16.302,
        "areaHa": 17,
        "areaNote": "17 公顷世界遗产美泉宫皇家园林",
        "speciesCount": 700,
        "animalCount": 8500,
        "ticketUsd": 29,
        "durationHours": "4–5 小时",
        "walkingIntensity": "低（古典放射状林荫步道＋山坡林道）",
        "bestFor": ["历史建筑控", "大熊猫与北极熊迷", "情侣与亲子"],
        "tip": "中心八角形的巴洛克皇帝早餐亭（Kaiserpavillon）如今是咖啡厅，坐在皇室圆亭喝维也纳咖啡，四周环绕着长颈鹿、河马与大熊猫馆，连续6次蝉联欧洲最佳动物园。",
        "search_q": "Tiergarten Schönbrunn Vienna zoo"
    },
    {
        "rank": 32,
        "name": "圣路易斯动物园 (Saint Louis Zoo)",
        "country": "美国",
        "city": "密苏里州圣路易斯",
        "tier": "T2",
        "highlight": "全美最不可思议的免费世界级动物园！1904年世博会步入式巨型飞禽笼、北极熊水下海岸、企鹅海鹦冰川馆与红毛猩猩森林",
        "id": "zoo-st-louis",
        "lat": 38.635,
        "lon": -90.290,
        "areaHa": 36,
        "areaNote": "36 公顷森林公园核心区",
        "speciesCount": 500,
        "animalCount": 14000,
        "ticketUsd": 0,
        "durationHours": "4–5 小时",
        "walkingIntensity": "中（园区缓坡，可搭乘环园小火车 Zooline Railroad）",
        "bestFor": ["高性价比白嫖党", "极地动物控", "亲子遛娃"],
        "tip": "门票完全免费（靠市政税收与捐赠维持顶级水准）！必看耗资数千万美金的《Polar Bear Point》水下北极熊玻璃隧洞，以及全美最大的真冰雪企鹅与海鹦（Puffin）馆。",
        "search_q": "Saint Louis Zoo Polar Bear Point"
    },
    {
        "rank": 33,
        "name": "辛辛那提动物园与植物园 (Cincinnati Zoo & Botanical Garden)",
        "country": "美国",
        "city": "俄亥俄州辛辛那提",
        "tier": "T2",
        "highlight": "全球顶流网红河马 Fiona 与 Fritz 故乡，拥有全美最震撼的猎豹100米全速冲刺秀、大猩猩世界与新建5英亩《大象林地》",
        "id": "zoo-cincinnati",
        "lat": 39.144,
        "lon": -84.508,
        "areaHa": 30,
        "areaNote": "30 公顷百年植物园动物园",
        "speciesCount": 400,
        "animalCount": 2000,
        "ticketUsd": 26,
        "durationHours": "4–5 小时",
        "walkingIntensity": "中（百年树荫覆盖，夏季清凉）",
        "bestFor": ["河马Fiona粉丝", "猫科猎豹控", "花园漫步"],
        "tip": "一定要去《Hippo Cove》水下大玻璃窗前看早产奇迹河马 Fiona 和弟弟 Fritz 在水里像芭蕾舞者一样翻滚，上午还有猎豹在草坪追逐机械诱饵的时速100公里冲刺展示。",
        "search_q": "Cincinnati Zoo Hippo Cove Fiona"
    },
    {
        "rank": 34,
        "name": "芝加哥布鲁克菲尔德＋林肯公园动物园 (Brookfield & Lincoln Park Zoo)",
        "country": "美国",
        "city": "芝加哥",
        "tier": "T2",
        "highlight": "北美无栏杆壕沟设计鼻祖：87公顷布鲁克菲尔德《大熊荒野》（灰熊/北极熊/野牛）＋密歇根湖畔免费开放的林肯公园猿类中心",
        "id": "zoo-brookfield-lincoln",
        "lat": 41.832,
        "lon": -87.833,
        "areaHa": 87,
        "areaNote": "布鲁克菲尔德 87 公顷 ＋ 林肯公园 14 公顷",
        "speciesCount": 510,
        "animalCount": 4500,
        "ticketUsd": 30,
        "durationHours": "5–6 小时",
        "walkingIntensity": "中高（布鲁克菲尔德园区极大）",
        "bestFor": ["北美巨兽控", "灵长类迷", "芝加哥城际游"],
        "tip": "布鲁克菲尔德的《Great Bear Wilderness》与即将揭幕的《热带森林》大猩猩新馆极具压迫感；市中心的林肯公园动物园则365天免费，拍狮子背景就是芝加哥摩天大楼群。",
        "search_q": "Brookfield Zoo Chicago Great Bear Wilderness"
    },
    {
        "rank": 35,
        "name": "丹佛动物园＋夏延山动物园 (Denver Zoo & Cheyenne Mountain Zoo)",
        "country": "美国",
        "city": "科罗拉多州丹佛 / 科泉市",
        "tier": "T2",
        "highlight": "海拔2000米落基山悬崖奇观：全球最大17头罗氏长颈鹿群平视喂食、亚洲象跨桥「Toyota象园」与悬崖缆车俯瞰北美大平原",
        "id": "zoo-denver-cheyenne",
        "lat": 39.750,
        "lon": -104.950,
        "areaHa": 32,
        "areaNote": "丹佛 32 公顷 ＋ 夏延山 59 公顷悬崖",
        "speciesCount": 600,
        "animalCount": 4000,
        "ticketUsd": 28,
        "durationHours": "5–7 小时",
        "walkingIntensity": "中高（夏延山建在海拔2000米山腰，坡度较大）",
        "bestFor": ["长颈鹿投喂控", "高山悬崖视野", "大象与红毛猩猩迷"],
        "tip": "科泉市的 Cheyenne Mountain Zoo 建在落基山脉半山腰，买一捆生菜就能在木栈道上同时被十几头长颈鹿伸长紫黑色舌头包围；丹佛动物园的亚洲象高空步道桥更是建筑杰作。",
        "search_q": "Cheyenne Mountain Zoo giraffe"
    },
    {
        "rank": 36,
        "name": "沃斯堡动物园＋达拉斯动物园 (Fort Worth & Dallas Zoo)",
        "country": "美国",
        "city": "得州达拉斯 / 沃斯堡",
        "tier": "T2",
        "highlight": "得州双雄：沃斯堡斥资1亿美金升级非洲草原、猎手与猎物区及全美最强两栖爬行馆 MOLA；达拉斯则以11英亩《草原巨兽》象群与长颈鹿混养闻名",
        "id": "zoo-fort-worth-dallas",
        "lat": 32.723,
        "lon": -97.356,
        "areaHa": 26,
        "areaNote": "沃斯堡 26 公顷 ＋ 达拉斯 43 公顷",
        "speciesCount": 540,
        "animalCount": 7000,
        "ticketUsd": 20,
        "durationHours": "4–6 小时",
        "walkingIntensity": "中（林荫道完善，有园区小火车）",
        "bestFor": ["爬行动物控", "非洲巨兽迷", "得州亲子"],
        "tip": "沃斯堡动物园长期稳居全美前五，其《Museum of Living Art (MOLA)》拥有6米长咸水鳄、全美最多品种的巨蜥与毒蛇，新建的《Elephant Springs》还能看亚洲象跳进瀑布大水池。",
        "search_q": "Fort Worth Zoo Elephant Springs"
    },
    {
        "rank": 37,
        "name": "孟菲斯动物园 (Memphis Zoo)",
        "country": "美国",
        "city": "田纳西州孟菲斯",
        "tier": "T2",
        "highlight": "把非洲尚比西河与北美黄石国家公园搬进森林：《Zambezi River Hippo Camp》水下河马尼罗鳄同框＋《Teton Trek》灰熊瀑布与麋鹿狼群",
        "id": "zoo-memphis",
        "lat": 35.150,
        "lon": -89.994,
        "areaHa": 31,
        "areaNote": "31 公顷奥弗顿森林公园",
        "speciesCount": 500,
        "animalCount": 4500,
        "ticketUsd": 25,
        "durationHours": "3.5–4.5 小时",
        "walkingIntensity": "低中（平坦开阔，主题造景极强）",
        "bestFor": ["主题造景控", "水下河马迷", "北美荒野控"],
        "tip": "孟菲斯动物园的造景水准极高：走进《Teton Trek》就像直接迈入怀俄明州大提顿国家公园，复制了老忠实间歇泉与黄石木屋，灰熊就在木屋旁的水池里抓鱼。",
        "search_q": "Memphis Zoo Teton Trek"
    },
    {
        "rank": 38,
        "name": "多伦多动物园 (Toronto Zoo)",
        "country": "加拿大",
        "city": "多伦多",
        "tier": "T2",
        "highlight": "占地287公顷的北美巨无霸生物地理区动物园：按七大洲建造5座巨型热带温室展馆与10公顷非洲稀树草原，拥有北极熊、独角犀与大猩猩雨林",
        "id": "zoo-toronto",
        "lat": 43.820,
        "lon": -79.182,
        "areaHa": 287,
        "areaNote": "287 公顷红河谷（加拿大最大动物园）",
        "speciesCount": 450,
        "animalCount": 5000,
        "ticketUsd": 23,
        "durationHours": "5–7 小时",
        "walkingIntensity": "高（步道总长10公里，冬季有5大巨型恒温热带馆）",
        "bestFor": ["暴走自然派", "温室雨林迷", "极地苔原控"],
        "tip": "面积大到惊人（287公顷），即使在加拿大零下20度的寒冬，也能钻进非洲雨林馆（看西部低地大猩猩与倭河马）、印度马来馆（看红毛猩猩）和澳洲馆。",
        "search_q": "Toronto Zoo Gorilla Rainforest"
    },
    {
        "rank": 39,
        "name": "蒙特利尔生态穹顶＋格兰比动物园 (Montreal Biodôme & Zoo de Granby)",
        "country": "加拿大",
        "city": "魁北克蒙特利尔 / 格兰比",
        "tier": "T2",
        "highlight": "1976年奥运会自行车馆改建的殿堂级室内生态模拟器：一馆无缝穿越美洲热带雨林（水豚/金刚鹦鹉/树懒）、极地企鹅冰岛与圣劳伦斯海湾",
        "id": "zoo-granby-biodome",
        "lat": 45.559,
        "lon": -73.549,
        "areaHa": 60,
        "areaNote": "生态穹顶室内4大生态系统 ＋ 格兰比动物园 60 公顷",
        "speciesCount": 380,
        "animalCount": 4800,
        "ticketUsd": 22,
        "durationHours": "3–5 小时",
        "walkingIntensity": "低（Biodôme全室内环形高空栈道）",
        "bestFor": ["温室建筑迷", "全天候不受天气影响", "极地企鹅与海鹦控"],
        "tip": "蒙特利尔 Biodôme 耗资数千万加元完成大改造，站在纯白流线型夹层天桥上，左边是湿热难耐的亚马逊雨林，推开隔热门走两步就是零下真冰雪的国王企鹅与海鹦悬崖。",
        "search_q": "Montreal Biodome tropical rainforest"
    },
    {
        "rank": 40,
        "name": "都柏林动物园 (Dublin Zoo)",
        "country": "爱尔兰",
        "city": "都柏林（凤凰公园）",
        "tier": "T2",
        "highlight": "坐落在欧洲最大城市公园（凤凰公园）内的1831年湖景动物园，13公顷《非洲平原》湖畔长颈鹿犀牛混养与《卡齐兰加森林》亚洲象大家族",
        "id": "zoo-dublin",
        "lat": 53.356,
        "lon": -6.305,
        "areaHa": 28,
        "areaNote": "28 公顷天然湖泊草甸（位于707公顷凤凰公园内）",
        "speciesCount": 400,
        "animalCount": 600,
        "ticketUsd": 26,
        "durationHours": "3.5–4.5 小时",
        "walkingIntensity": "低（环绕两座天然湖泊漫步，风景如画）",
        "bestFor": ["自然栖息地派", "大象与大猩猩迷", "欧洲城市漫游"],
        "tip": "整个动物园围绕两座天然冰川湖展开，完全没有铁笼感。看完动物园出门在凤凰公园草地上还能偶遇数百头野生黇鹿群（Fallow Deer）。",
        "search_q": "Dublin Zoo African Plains"
    },
    {
        "rank": 41,
        "name": "爱丁堡动物园＋苏格兰高地野生动物园 (Edinburgh Zoo & Highland Wildlife Park)",
        "country": "英国",
        "city": "苏格兰爱丁堡 / 金克雷格",
        "tier": "T2",
        "highlight": "全球「企鹅巡游 (Penguin Parade)」发源地（3种企鹅百余只）＋凯恩戈姆雪山脚下自驾穿越北极熊、野马、雪豹与欧洲野牛冰原",
        "id": "zoo-edinburgh-highland",
        "lat": 55.942,
        "lon": -3.269,
        "areaHa": 138,
        "areaNote": "爱丁堡科斯托芬山 33 公顷 ＋ 高地野生动物园 105 公顷",
        "speciesCount": 350,
        "animalCount": 3000,
        "ticketUsd": 31,
        "durationHours": "4–6 小时",
        "walkingIntensity": "中（爱丁堡建在山坡上，高地可开私家车游猎）",
        "bestFor": ["企鹅死忠粉", "极地高寒物种控", "自驾苏格兰高地"],
        "tip": "爱丁堡动物园拥有闻名世界的授衔皇家企鹅爵士「尼尔斯·奥拉夫准将（Sir Nils Olav）」，周末下午企鹅们会走出围栏在游客脚边摇摆巡游；高地园则有英国唯一的北极熊家族。",
        "search_q": "Edinburgh Zoo Penguin Rock"
    },
    {
        "rank": 42,
        "name": "伦敦动物园＋惠普斯奈德野生动物园 (ZSL Whipsnade & London Zoo)",
        "country": "英国",
        "city": "伦敦摄政公园 / 贝德福德郡",
        "tier": "T2",
        "highlight": "现代动物学鼻祖 ZSL 双璧：240公顷惠普斯奈德白垩悬崖草原让亚洲象群、白犀牛与棕熊在英格兰乡野自由漫步，可开私家车入园",
        "id": "zoo-whipsnade-london",
        "lat": 51.852,
        "lon": -0.544,
        "areaHa": 255,
        "areaNote": "惠普斯奈德 240 公顷（英国最大）＋ 伦敦摄政公园 15 公顷",
        "speciesCount": 650,
        "animalCount": 15000,
        "ticketUsd": 38,
        "durationHours": "5–6 小时",
        "walkingIntensity": "低至中（惠普斯奈德允许付费将私家车直接开进园区）",
        "bestFor": ["自驾旷野派", "建筑古迹迷", "犀牛与大象控"],
        "tip": "伦敦摄政公园动物园拥有1934年现代主义建筑遗产企鹅池与斯诺登勋爵鸟笼；而北郊45分钟车程的 Whipsnade 面积是伦敦园的16倍，站在悬崖边看白犀牛群和三郡平原风光极其壮阔。",
        "search_q": "Whipsnade Zoo elephants"
    },
    {
        "rank": 43,
        "name": "科隆动物园＋法兰克福动物园 (Kölner Zoo & Zoo Frankfurt)",
        "country": "德国",
        "city": "科隆 / 法兰克福",
        "tier": "T2",
        "highlight": "2公顷旗舰级亚洲象繁育公园、360度水下河马与尼罗鳄海牛雨林穹顶《Hippodom》，以及传奇园长格齐梅克打造的夜行动物馆",
        "id": "zoo-koln-frankfurt",
        "lat": 50.958,
        "lon": 6.974,
        "areaHa": 31,
        "areaNote": "科隆 20 公顷 ＋ 法兰克福 11 公顷",
        "speciesCount": 850,
        "animalCount": 12000,
        "ticketUsd": 25,
        "durationHours": "4–5 小时",
        "walkingIntensity": "低（莱茵河畔平坦花园步道，可乘过河缆车）",
        "bestFor": ["水下河马控", "大象家族迷", "温室雨林控"],
        "tip": "科隆动物园的《Hippodom》还原了整条非洲大河剖面：隔着巨型亚克力窗，左边是成群河马与尼罗鳄水下同游，右边是西非海牛吃生菜，头顶还有冕鹤飞过。",
        "search_q": "Kölner Zoo Hippodom"
    },
    {
        "rank": 44,
        "name": "慕尼黑海拉布伦地球动物园 (Tierpark Hellabrunn)",
        "country": "德国",
        "city": "慕尼黑",
        "tier": "T2",
        "highlight": "1928年创立的全球第一座「地理分区动物园 (Geozoo)」，伊萨尔河清澈活水溪流纵横40公顷古老河谷森林，用活水河道代替铁丝网",
        "id": "zoo-munich-hellabrunn",
        "lat": 48.098,
        "lon": 11.554,
        "areaHa": 40,
        "areaNote": "40 公顷伊萨尔河湿地森林保护区",
        "speciesCount": 750,
        "animalCount": 18000,
        "ticketUsd": 22,
        "durationHours": "4–5 小时",
        "walkingIntensity": "低（全园平坦森林水道与木桥，推婴儿车极度舒适）",
        "bestFor": ["自然栖息地派", "森林漫步", "极地与有蹄类控"],
        "tip": "全园几乎看不到围栏，全部利用伊萨尔河分流出的天然水道作为动物边界。百年穹顶象屋完成翻新后通透宏伟，北极熊、西伯利亚虎与非洲狮都在森林活水边生活。",
        "search_q": "Tierpark Hellabrunn Munich elephant house"
    },
    {
        "rank": 45,
        "name": "巴塞尔动物园 (Zoo Basel / Zolli)",
        "country": "瑞士",
        "city": "巴塞尔",
        "tier": "T2",
        "highlight": "瑞士人昵称「Zolli」的殿堂级园林动物园：全球印度独角犀与倭河马谱系繁育大本营，拥有纳米比亚《Etosha》沙漠馆与《Tembea》大象草原",
        "id": "zoo-basel",
        "lat": 47.547,
        "lon": 7.579,
        "areaHa": 13,
        "areaNote": "13 公顷高密度山水园林（从巴塞尔火车站步行8分钟即达）",
        "speciesCount": 600,
        "animalCount": 7000,
        "ticketUsd": 25,
        "durationHours": "3.5–4.5 小时",
        "walkingIntensity": "低（精致紧凑，曲径通幽如日本庭园）",
        "bestFor": ["神兽繁育控", "景观设计迷", "轻松少走路"],
        "tip": "虽然只有13公顷，但通过高低错落的岩石、溪流与植被把人类视线完美隐藏，从巴塞尔SBB主火车站出站步行8分钟直接进园，是全欧洲交通最丝滑的名园。",
        "search_q": "Zoo Basel Tembea elephant"
    },
    {
        "rank": 46,
        "name": "马德里动物园＋Faunia自然主题公园 (Zoo Aquarium de Madrid & Faunia)",
        "country": "西班牙",
        "city": "马德里",
        "tier": "T2",
        "highlight": "欧洲极少数同时集齐大熊猫、考拉、大猩猩、印度犀、宽吻海豚与4米沙虎鲨水族馆的全能王＋Faunia南极企鹅冰川与亚马逊雷暴馆",
        "id": "zoo-madrid-faunia",
        "lat": 40.409,
        "lon": -3.762,
        "areaHa": 36,
        "areaNote": "马德里田园之家 22 公顷 ＋ Faunia 14 公顷",
        "speciesCount": 600,
        "animalCount": 6000,
        "ticketUsd": 28,
        "durationHours": "5–6 小时",
        "walkingIntensity": "中（田园之家松林环绕）",
        "bestFor": ["神兽收集控", "极地与雨林温室迷", "全年龄亲子"],
        "tip": "马德里动物园一套门票包含陆地巨兽、水下海龟鲨鱼隧道与海豚馆；而东郊的 Faunia 则拥有欧洲最大的极地冰川企鹅生态馆（7种企鹅）和每20分钟下一场真热带暴雨的亚马逊丛林馆。",
        "search_q": "Zoo Aquarium de Madrid panda"
    },
    {
        "rank": 47,
        "name": "和歌山冒险大世界＋神户动物王国 (Adventure World & Kobe Animal Kingdom)",
        "country": "日本",
        "city": "和歌山白滨 / 兵库神户",
        "tier": "T2",
        "highlight": "关西双绝：白滨乘小火车穿越非洲肉食与草食游猎区、拥有日本最强的帝企鹅繁育群；神户则是零距离摸水豚、看鲸头鹳飞掠头顶的生态花房",
        "id": "zoo-kobe-adventure",
        "lat": 33.671,
        "lon": 135.376,
        "areaHa": 80,
        "areaNote": "和歌山白滨 80 公顷 ＋ 神户港岛全天候大温室",
        "speciesCount": 300,
        "animalCount": 2500,
        "ticketUsd": 35,
        "durationHours": "5–7 小时",
        "walkingIntensity": "低（白滨有游猎列车，神户全平地室内恒温鲜花温室）",
        "bestFor": ["零距离撸动物", "鲸头鹳与兔狲控", "关西温泉联游"],
        "tip": "神户动物王国把动物园做成了无笼子的室内大花园：水豚、袋鼠、环尾狐猴就在你脚边散步，史前巨鸟鲸头鹳（Shoebill）隔着小溪盯着你，还有雪地风格的兔狲展区。",
        "search_q": "Kobe Animal Kingdom shoebill"
    },
    {
        "rank": 48,
        "name": "北海道旭山动物园＋东京上野动物园 (Asahiyama & Ueno Zoo)",
        "country": "日本",
        "city": "北海道旭川 / 东京上野",
        "tier": "T2",
        "highlight": "改写全球动物园设计的「行动展示 (Action Display)」圣地：斑海豹垂直玻璃圆柱穿梭管、北极熊跳水视窗、冬日雪地国王企鹅大散步与上野指猴森林",
        "id": "zoo-asahiyama-ueno",
        "lat": 43.768,
        "lon": 142.479,
        "areaHa": 29,
        "areaNote": "旭山 15 公顷 ＋ 上野不忍池 14 公顷",
        "speciesCount": 420,
        "animalCount": 3500,
        "ticketUsd": 10,
        "durationHours": "4–5 小时",
        "walkingIntensity": "中（旭山建在山坡上，冬季需穿防滑冰爪靴）",
        "bestFor": ["行动展示迷", "冬季企鹅散步", "超高性价比"],
        "tip": "旭山动物园门票仅约 $7（1000日元），每年12月下旬至3月积雪期，国王企鹅群每天两次摇摇摆摆走过雪道，从游客脚尖前20厘米走过，海豹馆的垂直圆柱管更是必打卡经典。",
        "search_q": "Asahiyama Zoo penguin walk"
    },
    {
        "rank": 49,
        "name": "塔龙加西部平原野生动物园 (Taronga Western Plains Zoo Dubbo)",
        "country": "澳大利亚",
        "city": "新南威尔士州达博 (Dubbo)",
        "tier": "T2",
        "highlight": "占地300公顷的澳洲内陆红土旷野：全程自驾、骑自行车或开高尔夫球车穿越5公里环形林道，在无围栏壕沟前看黑犀牛、白犀牛、非洲野犬与猎豹",
        "id": "zoo-dubonga-western-plains",
        "lat": -32.272,
        "lon": 148.586,
        "areaHa": 300,
        "areaNote": "300 公顷澳洲内陆灌木旷野（单程环道5公里）",
        "speciesCount": 100,
        "animalCount": 4000,
        "ticketUsd": 36,
        "durationHours": "4–6 小时（或住园内 Zoofari Lodge 一晚）",
        "walkingIntensity": "极低（全程开自己私家车、租电动车或骑单车游览）",
        "bestFor": ["自驾游猎", "骑行看兽群", "犀牛保育迷"],
        "tip": "悉尼塔龙加动物园的300公顷姐妹园，拥有全球最成功的黑犀牛繁育中心。强烈推荐住一晚园区内的《Zoofari Lodge》帐篷别墅，清晨推开阳台直接看长颈鹿和斑马在窗前吃草。",
        "search_q": "Taronga Western Plains Zoo Dubbo"
    },
    {
        "rank": 50,
        "name": "比勒陀利亚国家动物园＋约翰内斯堡动物园 (Pretoria National Zoo & Joburg Zoo)",
        "country": "南非",
        "city": "比勒陀利亚 / 约翰内斯堡",
        "tier": "T2",
        "highlight": "非洲大陆规模最大的85公顷山体与河谷动物园：阿apies河将园区一分为二，乘山顶缆车俯瞰紫薇花城，看珍稀白狮、南非剑羚、黑犀牛与倭河马",
        "id": "zoo-johannesburg-pretoria",
        "lat": -25.738,
        "lon": 28.189,
        "areaHa": 140,
        "areaNote": "比勒陀利亚 85 公顷 ＋ 约翰内斯堡 55 公顷",
        "speciesCount": 700,
        "animalCount": 9000,
        "ticketUsd": 8,
        "durationHours": "4–5 小时",
        "walkingIntensity": "中（可租高尔夫球车巡游平坦区与山坡区）",
        "bestFor": ["非洲本土神兽", "白狮与猛禽控", "高性价比旷野"],
        "tip": "创立于1899年的比勒陀利亚国家动物园是非洲最大的动物园，一半在平原、一半在马加利斯堡山麓，10月至11月满园紫色蓝花楹（Jacaranda）盛开时美得不像话。",
        "search_q": "National Zoological Gardens of South Africa Pretoria"
    }
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
        "iiurlwidth": "960",
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
                if any(bad in title.lower() for bad in ["map", "logo", "flag", "icon", "svg", "sign", "ticket", "stamp"]):
                    continue
                ii = p.get("imageinfo", [{}])[0]
                thumb = ii.get("thumburl") or ii.get("url")
                if thumb:
                    ext = ii.get("extmetadata", {})
                    artist = re.sub(r"<[^>]+>", "", ext.get("Artist", {}).get("value", "Wikimedia Commons")).strip()[:100]
                    lic = ext.get("LicenseShortName", {}).get("value", "CC BY-SA")
                    return {
                        "src": thumb,
                        "page": ii.get("descriptionurl", ""),
                        "artist": artist,
                        "license": lic,
                        "title": title
                    }
            return None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2.5 * (attempt + 1))
                continue
            print(f"Warning fetching {query}: {e}")
            return None
        except Exception as e:
            print(f"Warning fetching {query}: {e}")
            return None
    return None


def main():
    js_path = ROOT / "data_aquariums_zoos_museums.js"
    text = js_path.read_text(encoding="utf-8")

    # Parse existing arrays
    m_aq = re.search(r"window\.AQUARIUMS_TOP(?:35|50)\s*=\s*(\[.*?\]);", text, re.S)
    m_zoo = re.search(r"window\.ZOOS_TOP(?:30|50)\s*=\s*(\[.*?\]);", text, re.S)
    m_safari = re.search(r"window\.US_SAFARI_PARKS_TOP10\s*=\s*(\[.*?\]);", text, re.S)
    m_mus = re.search(r"window\.INDUSTRIAL_MUSEUMS_TOP100\s*=\s*(\[.*?\]);", text, re.S)

    aquariums = json.loads(m_aq.group(1))[:35]
    zoos = json.loads(m_zoo.group(1))[:30]
    safaris = json.loads(m_safari.group(1))
    museums = json.loads(m_mus.group(1))

    # Append new aquariums and zoos (strip search_q before saving to JS)
    for item in NEW_AQUARIUMS:
        clean = {k: v for k, v in item.items() if k != "search_q"}
        aquariums.append(clean)

    for item in NEW_ZOOS:
        clean = {k: v for k, v in item.items() if k != "search_q"}
        zoos.append(clean)

    print(f"Aquariums count: {len(aquariums)}, Zoos count: {len(zoos)}")

    # Write updated data_aquariums_zoos_museums.js
    out_js = (
        "// Global Top 50 Aquariums, Top 50 Zoos + 10 US Safari Parks, and Top 100 Tech/Industrial/Military Museums\n"
        f"window.AQUARIUMS_TOP50 = {json.dumps(aquariums, ensure_ascii=False, indent=2)};\n"
        "window.AQUARIUMS_TOP35 = window.AQUARIUMS_TOP50;\n\n"
        f"window.ZOOS_TOP50 = {json.dumps(zoos, ensure_ascii=False, indent=2)};\n"
        "window.ZOOS_TOP30 = window.ZOOS_TOP50;\n\n"
        f"window.US_SAFARI_PARKS_TOP10 = {json.dumps(safaris, ensure_ascii=False, indent=2)};\n\n"
        f"window.INDUSTRIAL_MUSEUMS_TOP100 = {json.dumps(museums, ensure_ascii=False, indent=2)};\n"
    )
    js_path.write_text(out_js, encoding="utf-8")
    print("Updated data_aquariums_zoos_museums.js")

    # Fetch images for new items into images_themed.js
    img_path = ROOT / "images_themed.js"
    img_text = img_path.read_text(encoding="utf-8")
    m_img = re.search(r"window\.THEMED_IMAGES\s*=\s*(\{.*\})", img_text, re.S)
    themed_images = json.loads(m_img.group(1).rstrip().rstrip(";"))

    for item in NEW_AQUARIUMS + NEW_ZOOS:
        iid = item["id"]
        if iid in themed_images and themed_images[iid].get("src"):
            continue
        q = item["search_q"]
        info = fetch_wiki_image(q)
        if not info:
            # Fallback broader query
            info = fetch_wiki_image(q.split()[0] + " " + ("aquarium" if iid.startswith("aq-") else "zoo"))
        if info:
            themed_images[iid] = info
            print(f"Image [{iid}] -> {info['title']}")
        else:
            print(f"WARNING: No image found for {iid} ({q})")
        time.sleep(0.25)

    img_out = (
        "// Cover photos for Aquariums, Zoos, Safari Parks, Museums, Theme Parks, Ski Resorts & Shows from Wikimedia Commons\n"
        "window.THEMED_IMAGES = " + json.dumps(themed_images, ensure_ascii=False, indent=1) + ";\n"
    )
    img_path.write_text(img_out, encoding="utf-8")
    print(f"Updated images_themed.js ({len(themed_images)} entries)")

    # Update markdown files in rankings/
    aq_md_lines = [
        "# 全球 50 座顶级水族馆硬核榜单 (The Abyss Index · Top 50)\n",
        "> 不算过山车和海豚表演，只看**总水体吨位、主大洋缸亚克力巨幕尺寸与深海镇馆活体**。\n",
        "| 排名 | 水族馆 | 国家/城市 | 梯队 | 总水体 (万升) | 主缸 (万升) | 门票 ($) | 核心看点与主窗规格 |",
        "|---:|---|---|---|---:|---:|---:|---|"
    ]
    for a in aquariums:
        aq_md_lines.append(
            f"| {a['rank']} | **{a['name']}** | {a['country']}·{a['city']} | {a['tier']} | {a['totalVolumeML']:,} | {a['mainTankML']:,} | ${a['ticketUsd']} | {a['highlight']}（主窗：{a['windowSize']}） |"
        )
    (ROOT / "rankings" / "aquariums_top35.md").write_text("\n".join(aq_md_lines) + "\n", encoding="utf-8")

    zoo_md_lines = [
        "# 全球 50 座顶级动物园 ＋ 10 大美国自驾游猎园 (Field Notes · Top 50 + 10)\n",
        "> 拒绝铁笼式展陈，只看**栖息地自然尺度、跨洲群落沉浸感与镇园珍稀神兽**。\n",
        "## 一、全球动物园 Top 50\n",
        "| 排名 | 动物园 | 国家/城市 | 梯队 | 占地 (公顷) | 物种数 | 门票 ($) | 镇园看点与栖息地设计 |",
        "|---:|---|---|---|---:|---:|---:|---|"
    ]
    for z in zoos:
        zoo_md_lines.append(
            f"| {z['rank']} | **{z['name']}** | {z['country']}·{z['city']} | {z['tier']} | {z['areaHa']} ha | {z['speciesCount']} | ${z['ticketUsd']} | {z['highlight']} |"
        )
    zoo_md_lines.append("\n## 二、美国自驾/敞篷车游猎园 Top 10 (US Safari Parks)\n")
    zoo_md_lines.append("| 排名 | 游猎园 | 所在州 | 占地 (公顷) | 游览方式 | 门票 ($) | 兽群规模与核心体验 |")
    zoo_md_lines.append("|---:|---|---|---:|---|---:|---|")
    for s in safaris:
        zoo_md_lines.append(
            f"| {s['rank']} | **{s['name']}** | {s['state']} | {s['areaHa']} ha | {s['mode']} | ${s['ticketUsd']} | {s['highlight']} |"
        )
    (ROOT / "rankings" / "zoos_top30.md").write_text("\n".join(zoo_md_lines) + "\n", encoding="utf-8")
    print("Updated rankings/aquariums_top35.md and rankings/zoos_top30.md")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Enrich data_aquariums_zoos_museums.js with hardcore metrics (volume, area, species, animals, window size)
and mass-audience practical fields (ticketUsd, durationHours, bestFor, tip, lat, lon, id)."""
import json

AQUARIUMS_EXTRA = {
  1: {
    "id": "aq-chimelong", "lat": 22.098, "lon": 113.536,
    "totalVolumeML": 12500, "mainTankML": 3100, "windowSize": "39.6m × 8.3m 鲸鲨巨幕 + 虎鲸深水巨幕",
    "speciesCount": 1200, "animalCount": 150000, "ticketUsd": 62, "durationHours": "1–2 天（双馆）",
    "bestFor": ["巨物深海控", "低龄亲子", "全天候室内"],
    "tip": "海洋王国偏重鲸鲨巨幕与户外夜秀，隔壁《长隆飞船乐园》全室内恒温且拥有全球最大活体珊瑚缸与虎鲸池，带娃建议买两日联票。"
  },
  2: {
    "id": "aq-seaworld-abudhabi", "lat": 24.491, "lon": 54.613,
    "totalVolumeML": 5800, "mainTankML": 2500, "windowSize": "20m 高三维深海巨球 SeaSphere + 跨层全透明扶梯",
    "speciesCount": 680, "animalCount": 100000, "ticketUsd": 102, "durationHours": "5–7 小时",
    "bestFor": ["巨物深海控", "情侣出片", "全天候室内"],
    "tip": "全馆 18.3 万㎡全室内冷气充足，夏季去阿联酋必排；下午 15:00 在 Endless Ocean 巨球前看万鱼风暴视角最佳。"
  },
  3: {
    "id": "aq-georgia", "lat": 33.763, "lon": -84.395,
    "totalVolumeML": 4200, "mainTankML": 2400, "windowSize": "18.5m × 7.9m 巨幕 + 30m 穿心海底隧道",
    "speciesCount": 700, "animalCount": 100000, "ticketUsd": 53, "durationHours": "4–5 小时",
    "bestFor": ["巨物深海控", "低龄亲子", "全天候室内"],
    "tip": "早鸟票（9:00 前入场）人最少且便宜约 $10；入馆直奔 Ocean Voyager 巨幕，海豚与海狮剧场需在 App 免费预约场次。"
  },
  4: {
    "id": "aq-churaumi", "lat": 26.694, "lon": 127.878,
    "totalVolumeML": 1000, "mainTankML": 750, "windowSize": "22.5m × 8.2m × 60cm《黑潮之海》巨幕",
    "speciesCount": 710, "animalCount": 21000, "ticketUsd": 15, "durationHours": "3–4 小时",
    "bestFor": ["巨物深海控", "情侣出片", "自然生态迷"],
    "tip": "15:00 和 17:00 有鲸鲨垂直进食秀；紧贴黑潮大水槽右侧的 Ocean Blue 咖啡厅卡座需提前现场取号，人均一杯饮料即可独享巨幕窗景。"
  },
  5: {
    "id": "aq-singapore-oceanarium", "lat": 1.258, "lon": 103.819,
    "totalVolumeML": 4500, "mainTankML": 1800, "windowSize": "36m × 8.3m 超宽无框深海巨幕",
    "speciesCount": 1000, "animalCount": 100000, "ticketUsd": 38, "durationHours": "3–5 小时",
    "bestFor": ["低龄亲子", "情侣出片", "全天候室内"],
    "tip": "位于圣淘沙名胜世界内，和环球影城相邻；建议上午 10 点开门即进，先冲正中央 36 米鬼蝠魟主巨幕再慢逛水母厅。"
  },
  6: {
    "id": "aq-lisbon", "lat": 38.763, "lon": -9.094,
    "totalVolumeML": 750, "mainTankML": 500, "windowSize": "双层 4 面各 49㎡ 环绕无边界中央大池 + 40m 水草缸",
    "speciesCount": 500, "animalCount": 15000, "ticketUsd": 27, "durationHours": "2.5–3.5 小时",
    "bestFor": ["自然生态迷", "情侣出片", "低龄亲子"],
    "tip": "进门先看天野尚大师遗作《水下森林》自然水草造景，主馆设计极其精巧，二楼俯瞰与一楼仰视体验完全不同。"
  },
  7: {
    "id": "aq-valencia", "lat": 39.453, "lon": -0.348,
    "totalVolumeML": 4200, "mainTankML": 700, "windowSize": "70m 欧洲最长沙虎鲨隧道 + 北极冰屋白鲸馆",
    "speciesCount": 500, "animalCount": 45000, "ticketUsd": 40, "durationHours": "4–6 小时",
    "bestFor": ["情侣出片", "低龄亲子", "巨物深海控"],
    "tip": "位于艺术科学城建筑群内，园区是半露天多馆结构，夏天注意防晒；水下环形鱼群餐厅 Submarino 需提前两周在官网订位。"
  },
  8: {
    "id": "aq-nausicaa", "lat": 50.731, "lon": 1.594,
    "totalVolumeML": 1700, "mainTankML": 1000, "windowSize": "20m × 5m 深海无框巨幕 + 18m 全透明隧道",
    "speciesCount": 1600, "animalCount": 58000, "ticketUsd": 34, "durationHours": "3.5–4.5 小时",
    "bestFor": ["巨物深海控", "自然生态迷", "全天候室内"],
    "tip": "以哥斯达黎加科科斯岛公海为主题的 1000 万升主缸极具深海压迫感，不要漏掉最底层的深渊阶梯剧场。"
  },
  9: {
    "id": "aq-kenting-nmmba", "lat": 22.046, "lon": 120.699,
    "totalVolumeML": 1500, "mainTankML": 570, "windowSize": "84m 三段式阳光珊瑚沉船隧道 + 10m 高巨藻森林",
    "speciesCount": 600, "animalCount": 35000, "ticketUsd": 15, "durationHours": "3.5–5 小时（可夜宿）",
    "bestFor": ["低龄亲子", "情侣出片", "自然生态迷"],
    "tip": "华人圈最火的「夜宿海生馆」需提前 2–3 个月在官网抢海底隧道或巨藻区铺位，早上阳光洒进沉船隧道时美到失语。"
  },
  10: {
    "id": "aq-dubai-mall", "lat": 25.197, "lon": 55.279,
    "totalVolumeML": 1050, "mainTankML": 1000, "windowSize": "51m × 11m 超宽巨幕 + 48m 鲨鱼隧道",
    "speciesCount": 300, "animalCount": 33000, "ticketUsd": 45, "durationHours": "1.5–2.5 小时",
    "bestFor": ["巨物深海控", "情侣出片", "全天候室内"],
    "tip": "省钱秘籍：51 米宽的主巨幕一面墙直接朝向迪拜 Mall 商场中庭，不买票站在商场一楼/二楼就能免费看 300 条沙虎鲨巡游！"
  },
  11: {
    "id": "aq-atlantis-dubai", "lat": 25.131, "lon": 55.117,
    "totalVolumeML": 1150, "mainTankML": 1100, "windowSize": "1100万升亚特兰蒂斯神庙遗迹环景巨幕",
    "speciesCount": 250, "animalCount": 65000, "ticketUsd": 38, "durationHours": "1.5–2 小时",
    "bestFor": ["情侣出片", "低龄亲子", "全天候室内"],
    "tip": "入住棕榈岛亚特兰蒂斯酒店可无限次免费刷馆；非住客建议购买水世界冒险乐园+失落的空间联票更划算。"
  },
  12: {
    "id": "aq-atlantis-sanya", "lat": 18.338, "lon": 109.744,
    "totalVolumeML": 1750, "mainTankML": 1350, "windowSize": "16.5m × 8.3m 超高透单片巨幕",
    "speciesCount": 280, "animalCount": 86000, "ticketUsd": 28, "durationHours": "2–3 小时",
    "bestFor": ["情侣出片", "低龄亲子", "全天候室内"],
    "tip": "在大使环礁湖大堂吧侧边即可免费看到部分巨幕；买票入内可近距离看两头白鲸与美人鱼水下表演。"
  },
  13: {
    "id": "aq-nagoya", "lat": 35.091, "lon": 136.878,
    "totalVolumeML": 2400, "mainTankML": 1340, "windowSize": "29m × 7m 虎鲸水下巨幕 + 3000座剧场看台",
    "speciesCount": 500, "animalCount": 50000, "ticketUsd": 14, "durationHours": "4–5 小时",
    "bestFor": ["巨物深海控", "低龄亲子", "自然生态迷"],
    "tip": "进门就是北馆水下巨幕，能平视虎鲸与白鲸深潜；必看南馆黑潮大水槽 3.5 万条沙丁鱼龙卷风灯光秀。"
  },
  14: {
    "id": "aq-monterey", "lat": 36.618, "lon": -121.901,
    "totalVolumeML": 850, "mainTankML": 450, "windowSize": "27m × 5m 外海巨幕 + 8.5m 高活体巨藻森林",
    "speciesCount": 600, "animalCount": 80000, "ticketUsd": 65, "durationHours": "3.5–5 小时",
    "bestFor": ["自然生态迷", "情侣出片", "低龄亲子"],
    "tip": "门票只在线上预售（现场不卖票）；水母厅、巨藻林和二楼深海生物特展（Into the Deep）都是全球独一档的美学标杆。"
  },
  15: {
    "id": "aq-kaiyukan", "lat": 34.654, "lon": 135.429,
    "totalVolumeML": 1100, "mainTankML": 540, "windowSize": "9m 深 × 34m 长跨 4 层螺旋环绕太平洋主缸",
    "speciesCount": 620, "animalCount": 30000, "ticketUsd": 18, "durationHours": "2.5–3.5 小时",
    "bestFor": ["低龄亲子", "情侣出片", "全天候室内"],
    "tip": "动线从 8 楼坐长扶梯一口气登顶再螺旋往下走，可以从水面、中层、海底不同高度反复看两条鲸鲨；17:00 后入场为深海夜光模式。"
  },
  16: {
    "id": "aq-loro-parque", "lat": 28.408, "lon": -16.564,
    "totalVolumeML": 1200, "mainTankML": 220, "windowSize": "8.5m 高真冰企鹅雪山缸 + 鲨鱼隧道 + 水母光影厅",
    "speciesCount": 400, "animalCount": 25000, "ticketUsd": 46, "durationHours": "5–7 小时（含动物园）",
    "bestFor": ["低龄亲子", "自然生态迷", "情侣出片"],
    "tip": "一张票同时包含世界顶尖的鹦鹉动物园与水下展区；Planet Penguin 室内每天下 12 吨真雪，视觉效果冠绝全球企鹅馆。"
  },
  17: {
    "id": "aq-jeju", "lat": 33.424, "lon": 126.928,
    "totalVolumeML": 1080, "mainTankML": 600, "windowSize": "23m × 8.5m 双层深海巨幕 + 80m 隧道",
    "speciesCount": 500, "animalCount": 48000, "ticketUsd": 30, "durationHours": "2.5–3.5 小时",
    "bestFor": ["低龄亲子", "情侣出片", "全天候室内"],
    "tip": "紧邻涉地可支与城山日出峰，济州岛雨天首选；主巨幕每天有济州传统海女不背氧气瓶深潜喂食表演。"
  },
  18: {
    "id": "aq-shanghai-haichang", "lat": 30.913, "lon": 121.908,
    "totalVolumeML": 3500, "mainTankML": 750, "windowSize": "7度倾斜火山鲨鱼巨幕 + 南极企鹅双层水下穹顶",
    "speciesCount": 450, "animalCount": 40000, "ticketUsd": 48, "durationHours": "5–7 小时",
    "bestFor": ["低龄亲子", "巨物深海控"],
    "tip": "地铁 16 号线临港大道站直达；重点逛南极企鹅馆一楼抬头看企鹅从半球形玻璃顶游过，以及火山鲨鱼馆与虎鲸剧场。"
  },
  19: {
    "id": "aq-rizhao", "lat": 35.424, "lon": 119.552,
    "totalVolumeML": 1200, "mainTankML": 500, "windowSize": "自然天光银色风暴巨幕 + 阳光珊瑚沉船隧道",
    "speciesCount": 380, "animalCount": 30000, "ticketUsd": 30, "durationHours": "3–4 小时",
    "bestFor": ["低龄亲子", "情侣出片", "自然生态迷"],
    "tip": "由设计过屏东海生馆的团队操刀，晴天中午 11:00–14:00 去，自然阳光穿过水面照亮珊瑚隧道和银色鱼群风暴最出片。"
  },
  20: {
    "id": "aq-shedd", "lat": 41.867, "lon": -87.614,
    "totalVolumeML": 1900, "mainTankML": 1100, "windowSize": "亚马逊雨季泛滥森林水下长廊 + 极地海洋巨窗",
    "speciesCount": 1500, "animalCount": 32000, "ticketUsd": 40, "durationHours": "3–4 小时",
    "bestFor": ["自然生态迷", "低龄亲子", "全天候室内"],
    "tip": "位于密歇根湖畔博物馆园区，买 Chicago CityPASS 可免排队；亚马逊泛滥森林展区的水陆剖面造景是教科书级别。"
  },
  21: {
    "id": "aq-tennessee", "lat": 35.056, "lon": -85.311,
    "totalVolumeML": 450, "mainTankML": 230, "windowSize": "跨 4 层北美温带巨鱼深水缸 + 珊瑚海巨窗",
    "speciesCount": 800, "animalCount": 12000, "ticketUsd": 40, "durationHours": "3–4 小时",
    "bestFor": ["自然生态迷", "低龄亲子", "全天候室内"],
    "tip": "分为淡水馆（River Journey）与海洋馆（Ocean Journey）两栋大楼，淡水馆里的数米长湖鲟、匙吻鲟与鳄雀鳝比海洋馆更震撼。"
  },
  22: {
    "id": "aq-baltimore", "lat": 39.285, "lon": -76.608,
    "totalVolumeML": 850, "mainTankML": 100, "windowSize": "360度环形鲨鱼回廊 Shark Alley + 35m 澳洲峡谷温室",
    "speciesCount": 800, "animalCount": 20000, "ticketUsd": 50, "durationHours": "3–4 小时",
    "bestFor": ["自然生态迷", "低龄亲子", "全天候室内"],
    "tip": "每周五晚 17:00 后半价（Fridays After Five）；走进环形鲨鱼池正中央被数十条鲨鱼 360 度包围的体验独一无二。"
  },
  23: {
    "id": "aq-seaworld-orlando", "lat": 28.411, "lon": -81.461,
    "totalVolumeML": 2800, "mainTankML": 400, "windowSize": "百万升珊瑚泻湖浮潜池 + 鲨鱼长隧道 + Manta深海艺廊",
    "speciesCount": 400, "animalCount": 25000, "ticketUsd": 95, "durationHours": "1 整天",
    "bestFor": ["巨物深海控", "低龄亲子", "情侣出片"],
    "tip": "即使不坐 Manta 过山车，也可以直接走非乘骑通道（Non-rider Queue）免费进入 Manta 水族馆看鬼蝠魟与海龙！"
  },
  24: {
    "id": "aq-seaworld-sandiego", "lat": 32.764, "lon": -117.226,
    "totalVolumeML": 2200, "mainTankML": 350, "windowSize": "零下真冰帝企鹅馆 + 鲨鱼隧道 + 虎鲸水下观景窗",
    "speciesCount": 350, "animalCount": 20000, "ticketUsd": 75, "durationHours": "5–7 小时",
    "bestFor": ["低龄亲子", "巨物深海控"],
    "tip": "Penguin Encounter 是整个北美唯一能看到真实帝企鹅群（Emperor Penguin）的地方，记得去 Dine with Orcas 旁的水下观景窗平视虎鲸。"
  },
  25: {
    "id": "aq-epcot-seabase", "lat": 28.375, "lon": -81.551,
    "totalVolumeML": 2160, "mainTankML": 2160, "windowSize": "直径 62m 圆柱深海池 + 圆心双层海底空间站",
    "speciesCount": 200, "animalCount": 6000, "ticketUsd": 119, "durationHours": "1–1.5 小时（含在EPCOT内）",
    "bestFor": ["低龄亲子", "全天候室内"],
    "tip": "包含在奥兰多迪士尼 EPCOT 门票内；不坐海底总动员小车也能直接从出口侧门走进水族馆，二楼有西非海牛康复池。"
  },
  26: {
    "id": "aq-hk-oceanpark", "lat": 22.246, "lon": 114.176,
    "totalVolumeML": 1200, "mainTankML": 520, "windowSize": "13m 宽巨幕 + 5.5m 直径水下透明穹顶",
    "speciesCount": 400, "animalCount": 15000, "ticketUsd": 50, "durationHours": "5–7 小时（含全园）",
    "bestFor": ["低龄亲子", "情侣出片"],
    "tip": "入园先逛山下《海洋奇观》看锤头鲨与蓝鳍金枪鱼，再坐跨海登山缆车上高峰乐园看《冰极天地》王企鹅与太平洋海象。"
  },
  27: {
    "id": "aq-shanghai-lujiazui", "lat": 31.241, "lon": 121.502,
    "totalVolumeML": 450, "mainTankML": 320, "windowSize": "155m 五段式全球最长自动步道海底隧道",
    "speciesCount": 450, "animalCount": 15000, "ticketUsd": 22, "durationHours": "2–3 小时",
    "bestFor": ["低龄亲子", "全天候室内", "自然生态迷"],
    "tip": "就在东方明珠脚下，纯水下鱼类馆无动物表演；站在自动扶梯步道上缓慢穿过 155 米珊瑚、鲨鱼与海湾隧道非常省腿。"
  },
  28: {
    "id": "aq-ripleys-toronto", "lat": 43.642, "lon": -79.386,
    "totalVolumeML": 570, "mainTankML": 290, "windowSize": "96m 北美最长沙虎鲨/绿锯鳐自动步道隧道",
    "speciesCount": 450, "animalCount": 20000, "ticketUsd": 33, "durationHours": "2–3 小时",
    "bestFor": ["低龄亲子", "情侣出片", "全天候室内"],
    "tip": "位于多伦多 CN 塔正下方，晚间 17:00 后入场有 Sharks After Dark 门票优惠，Dangerous Lagoon 隧道里的巨型绿锯鳐必看。"
  },
  29: {
    "id": "aq-den-bla-planet", "lat": 55.638, "lon": 12.656,
    "totalVolumeML": 700, "mainTankML": 410, "windowSize": "16m × 8m 大洋池巨幕 + 16m 鲨鱼隧道",
    "speciesCount": 450, "animalCount": 20000, "ticketUsd": 31, "durationHours": "2–3 小时",
    "bestFor": ["情侣出片", "自然生态迷", "全天候室内"],
    "tip": "距离哥本哈根机场仅 1 站地铁（Kastrup 站），建筑外观如海面漩涡，非常适合下飞机或返程前顺路打卡。"
  },
  30: {
    "id": "aq-vancouver", "lat": 49.300, "lon": -123.131,
    "totalVolumeML": 950, "mainTankML": 260, "windowSize": "北太平洋巨藻冷海池 + 户外海獭与海狮湾",
    "speciesCount": 600, "animalCount": 65000, "ticketUsd": 38, "durationHours": "2.5–3.5 小时",
    "bestFor": ["低龄亲子", "自然生态迷"],
    "tip": "坐落在斯坦利公园森林深处，这里的救援海獭群（手拉手漂浮睡觉）是全馆最大萌点，逛完可顺路骑行斯坦利海堤。"
  },
  31: {
    "id": "aq-tokyo-sealife", "lat": 35.640, "lon": 139.862,
    "totalVolumeML": 500, "mainTankML": 220, "windowSize": "220万升 360度环形《太平洋蓝鳍金枪鱼狂飙大水槽》",
    "speciesCount": 600, "animalCount": 25000, "ticketUsd": 5, "durationHours": "2–3 小时",
    "bestFor": ["自然生态迷", "低龄亲子", "情侣出片"],
    "tip": "东京迪士尼舞滨站往西仅 1 站（葛西临海公园站），谷口吉生设计的玻璃穹顶建筑，门票仅 700 日元（约 $5），性价比无敌。"
  },
  32: {
    "id": "aq-long-beach", "lat": 33.762, "lon": -118.197,
    "totalVolumeML": 550, "mainTankML": 140, "windowSize": "三层楼高加州蓝洞巨藻缸 + 热带珊瑚礁隧道",
    "speciesCount": 500, "animalCount": 12000, "ticketUsd": 45, "durationHours": "2.5–3.5 小时",
    "bestFor": ["低龄亲子", "自然生态迷"],
    "tip": "进门左手边三层楼高的 Honda Blue Cavern 巨藻大缸完美还原南加州卡塔利娜岛海底，周末需提前在官网预约入场时段。"
  },
  33: {
    "id": "aq-istanbul", "lat": 40.966, "lon": 28.798,
    "totalVolumeML": 680, "mainTankML": 350, "windowSize": "1.2公里 17大海域电影级主题展线 + 鲨鱼主池",
    "speciesCount": 1500, "animalCount": 17000, "ticketUsd": 28, "durationHours": "2.5–3.5 小时",
    "bestFor": ["低龄亲子", "情侣出片", "全天候室内"],
    "tip": "不要和论坛商场里的 Sea Life 混淆，这家在 Florya 海滨（Marmaray 火车直达），每个海域展厅都有潜艇或沉船实景装修。"
  },
  34: {
    "id": "aq-two-oceans", "lat": -33.908, "lon": 18.417,
    "totalVolumeML": 450, "mainTankML": 200, "windowSize": "9m × 4m 沙虎鲨巨窗 + 10m 全透明无框弧形隧道",
    "speciesCount": 300, "animalCount": 8000, "ticketUsd": 14, "durationHours": "2–2.5 小时",
    "bestFor": ["自然生态迷", "低龄亲子", "情侣出片"],
    "tip": "就在开普敦维多利亚阿尔弗雷德码头（V&A Waterfront）核心区，活体巨藻林有阳光直射，持 PADI 潜水证可报名下沙虎鲨池深潜。"
  },
  35: {
    "id": "aq-ushaka", "lat": -29.867, "lon": 31.045,
    "totalVolumeML": 1750, "mainTankML": 380, "windowSize": "1920年代蒸汽沉船内部全包裹鲨鱼与巨型石斑深水窗",
    "speciesCount": 400, "animalCount": 10000, "ticketUsd": 13, "durationHours": "2.5–4 小时",
    "bestFor": ["巨物深海控", "情侣出片", "低龄亲子"],
    "tip": "沉船主题餐厅 Cargo Hold 直接将整面鲨鱼大缸作为餐厅背景墙，点一份海鲜主菜就能边吃边看三米长的沙虎鲨从桌旁游过。"
  }
}

ZOOS_EXTRA = {
  1: {
    "id": "zoo-san-diego", "lat": 32.735, "lon": -117.149,
    "areaHa": 770, "areaNote": "本部 40ha + 游猎园 730ha",
    "speciesCount": 1100, "animalCount": 15000, "ticketUsd": 74, "durationHours": "2 天（双园各1天）",
    "walkingIntensity": "中（本部含免费高空缆车 Skyfari 与双层观光巴士）",
    "bestFor": ["神兽收集控", "亲子遛娃", "自驾游猎"],
    "tip": "巴尔博亚公园本部看考拉、北极熊与立体峡谷，北郊 Safari Park 看非洲大草原兽群与美洲外唯一鸭嘴兽；两园相距 45 分钟车程。"
  },
  2: {
    "id": "zoo-pairi-daiza", "lat": 50.585, "lon": 3.887,
    "areaHa": 75, "areaNote": "75 公顷修道院古迹园林",
    "speciesCount": 800, "animalCount": 7500, "ticketUsd": 46, "durationHours": "1–2 天",
    "walkingIntensity": "中高（园区造景极密集，可乘蒸汽小火车环园）",
    "bestFor": ["温室建筑迷", "摄影出片", "神兽收集控"],
    "tip": "从布鲁塞尔乘火车约 1 小时至 Cambron-Casteau 站即达；园内北极熊/海象水下客房酒店需提前半年预订。"
  },
  3: {
    "id": "zoo-omaha", "lat": 41.225, "lon": -95.928,
    "areaHa": 65, "areaNote": "65 公顷（含三大世界级巨型室内馆）",
    "speciesCount": 960, "animalCount": 35000, "ticketUsd": 32, "durationHours": "1 整天（6–8 小时）",
    "walkingIntensity": "中（有 Skyfari 吊椅缆车与蒸汽火车代步）",
    "bestFor": ["温室建筑迷", "神兽收集控", "亲子遛娃"],
    "tip": "沙漠巨蛋（一楼沙漠二楼地下夜行馆）和 Lied 室内热带雨林哪怕在冬天暴雪天也四季如春，绝对值得专程飞一趟内布拉斯加。"
  },
  4: {
    "id": "zoo-mandai-singapore", "lat": 1.404, "lon": 103.793,
    "areaHa": 126, "areaNote": "日间28ha + 夜间35ha + 河川12ha + 飞禽17ha + 雨林33ha",
    "speciesCount": 1000, "animalCount": 24000, "ticketUsd": 37, "durationHours": "1–2 天（日+夜联玩）",
    "walkingIntensity": "低至中（日间与夜间园均有导览电瓶车，河川园含乘船）",
    "bestFor": ["亲子遛娃", "轻松少走路", "神兽收集控"],
    "tip": "最推荐「下午河川生态园（看海牛与巨骨舌鱼）+ 傍晚日间动物园 + 19:15 夜间野生动物园首班导览车」的一日丝滑组合。"
  },
  5: {
    "id": "zoo-animal-kingdom", "lat": 28.358, "lon": -81.590,
    "areaHa": 235, "areaNote": "235 公顷（全球面积最大迪士尼主题乐园）",
    "speciesCount": 300, "animalCount": 2000, "ticketUsd": 139, "durationHours": "1 整天",
    "walkingIntensity": "中（全平路无陡坡，含吉普车游猎与小火车）",
    "bestFor": ["亲子遛娃", "摄影出片", "自驾游猎"],
    "tip": "入园先冲阿凡达飞行（Flight of Passage），紧接着趁早上凉爽去坐 Kilimanjaro Safaris 吉普车，早晨动物活跃度是下午的两倍。"
  },
  6: {
    "id": "zoo-chimelong-guangzhou", "lat": 23.005, "lon": 113.321,
    "areaHa": 530, "areaNote": "广州番禺 133ha + 清远森林王国 400ha",
    "speciesCount": 500, "animalCount": 50000, "ticketUsd": 48, "durationHours": "1–2 天",
    "walkingIntensity": "低（含私家车自驾/免费小火车 + 全程三角形高空缆车）",
    "bestFor": ["亲子遛娃", "轻松少走路", "自驾游猎"],
    "tip": "广州园从北门进先坐免费半敞篷小火车穿越自驾区，下午一定要坐「天鹅湖线」高空缆车俯瞰百鸟飞歌与东非大草原。"
  },
  7: {
    "id": "zoo-leipzig", "lat": 51.349, "lon": 12.369,
    "areaHa": 27, "areaNote": "27 公顷（含 2.7ha 冈瓦纳室内雨林）",
    "speciesCount": 650, "animalCount": 8000, "ticketUsd": 24, "durationHours": "5–6 小时",
    "walkingIntensity": "低（全园平坦紧凑，冈瓦纳温室可乘小船游览）",
    "bestFor": ["温室建筑迷", "亲子遛娃", "轻松少走路"],
    "tip": "离莱比锡中央火车站步行仅 10 分钟；进门直奔 Gondwanaland 巨型热带雨林馆，花 €2 坐室内河道游船穿过雨林树冠与倭河马。"
  },
  8: {
    "id": "zoo-beauval", "lat": 47.248, "lon": 1.353,
    "areaHa": 45, "areaNote": "45 公顷（含 38m 高赤道玻璃穹顶）",
    "speciesCount": 800, "animalCount": 35000, "ticketUsd": 43, "durationHours": "1 整天",
    "walkingIntensity": "中（免费高空透明底缆车 Nuage de Beauval 连接南北两区）",
    "bestFor": ["温室建筑迷", "神兽收集控", "亲子遛娃"],
    "tip": "位于卢瓦尔河谷城堡群中心，强烈建议把舍农索城堡/香波堡和博瓦勒动物园排成两天一夜自驾行程。"
  },
  9: {
    "id": "zoo-doue", "lat": 47.190, "lon": -0.301,
    "areaHa": 17, "areaNote": "17 公顷地下千万年海洋贝壳砂岩采石场峡谷",
    "speciesCount": 130, "animalCount": 1900, "ticketUsd": 29, "durationHours": "4–5 小时",
    "walkingIntensity": "中（穿行在地下采石场峡谷与石洞隧道间，冬季阴凉）",
    "bestFor": ["摄影出片", "温室建筑迷", "神兽收集控"],
    "tip": "动物园界的隐秘天花板：凿穿整座山体形成的南美大峡谷鸟舍与喜马拉雅雪豹悬崖，拍出来的照片完全像在野外探险。"
  },
  10: {
    "id": "zoo-burgers", "lat": 52.001, "lon": 5.899,
    "areaHa": 45, "areaNote": "45 公顷（四大巨型室内生态系统群落）",
    "speciesCount": 500, "animalCount": 10000, "ticketUsd": 31, "durationHours": "5–6 小时",
    "walkingIntensity": "中（室内生态馆占比极高，完全不怕刮风下雨）",
    "bestFor": ["温室建筑迷", "亲子遛娃", "轻松少走路"],
    "tip": "从阿纳姆火车站坐 3 路公交直达；1.5 公顷 Bush 热带雨林与 800 万升 Ocean 活体珊瑚礁无缝连通，按生态群落混养而非按动物分类。"
  },
  11: {
    "id": "zoo-loro-parque", "lat": 28.408, "lon": -16.564,
    "areaHa": 13.5, "areaNote": "13.5 公顷高密度亚热带植物园",
    "speciesCount": 400, "animalCount": 4500, "ticketUsd": 46, "durationHours": "5–7 小时",
    "walkingIntensity": "中（山坡花园步道，树荫极茂密）",
    "bestFor": ["亲子遛娃", "摄影出片", "神兽收集控"],
    "tip": "可在普埃尔托德拉克鲁斯海滨免费搭乘黄色观光小火车直达园区大门；步入式树冠鸟舍 Katandra Treetops 必体验。"
  },
  12: {
    "id": "zoo-taronga", "lat": -33.843, "lon": 151.241,
    "areaHa": 28, "areaNote": "28 公顷悉尼港面海山坡",
    "speciesCount": 350, "animalCount": 5000, "ticketUsd": 34, "durationHours": "4–5 小时",
    "walkingIntensity": "低（坐渡轮到山脚，从山顶入口一路下坡走到码头最省力）",
    "bestFor": ["摄影出片", "神兽收集控", "轻松少走路"],
    "tip": "从环形码头（Circular Quay）坐 12 分钟渡轮直达，到岸后坐公交到山顶正门，一路往下逛完全不用爬坡；长颈鹿与悉尼歌剧院同框机位无敌。"
  },
  13: {
    "id": "zoo-prague", "lat": 50.117, "lon": 14.406,
    "areaHa": 58, "areaNote": "58 公顷伏尔塔瓦河谷与悬崖",
    "speciesCount": 670, "animalCount": 5300, "ticketUsd": 14, "durationHours": "5–6 小时",
    "walkingIntensity": "中高（上下两层有陡峭岩壁，强烈建议花 $2 坐园区吊椅缆车上山）",
    "bestFor": ["摄影出片", "神兽收集控", "亲子遛娃"],
    "tip": "欧洲性价比最高的世界级大园（门票仅约 $14），夏季可从布拉格市中心坐伏尔塔瓦河游船直达动物园旁。"
  },
  14: {
    "id": "zoo-bronx", "lat": 40.850, "lon": -73.877,
    "areaHa": 107, "areaNote": "107 公顷都市原始森林与布朗克斯河谷",
    "speciesCount": 700, "animalCount": 11000, "ticketUsd": 42, "durationHours": "5–7 小时",
    "walkingIntensity": "中高（园区极大，建议买含 Wild Asia 单轨列车与穿梭车的通票）",
    "bestFor": ["神兽收集控", "亲子遛娃"],
    "tip": "刚果大猩猩森林（Congo Gorilla Forest）和亚洲单轨列车（Wild Asia Monorail）是全园精华，周三有提前预约的免费基础票。"
  },
  15: {
    "id": "zoo-zurich", "lat": 47.385, "lon": 8.574,
    "areaHa": 27, "areaNote": "27 公顷（含 1.1万㎡马达加斯加雨林温室）",
    "speciesCount": 380, "animalCount": 4000, "ticketUsd": 33, "durationHours": "4–5 小时",
    "walkingIntensity": "中（山顶森林公园，6 路有轨电车直达门口）",
    "bestFor": ["温室建筑迷", "亲子遛娃", "摄影出片"],
    "tip": "Masoala 温室完全没有笼舍，红领狐猴和变色龙就在头顶树枝上自由活动；Kaeng Krachan 大象馆有全透明水下潜泳池。"
  },
  16: {
    "id": "zoo-chester", "lat": 53.226, "lon": -2.884,
    "areaHa": 51, "areaNote": "51 公顷（含 6ha 东南亚群岛乘船区）",
    "speciesCount": 500, "animalCount": 37000, "ticketUsd": 42, "durationHours": "5–7 小时",
    "walkingIntensity": "中（全平地园林，Islands 展区含免费懒人河游船）",
    "bestFor": ["温室建筑迷", "亲子遛娃", "神兽收集控"],
    "tip": "英国第一大动物园，距离利物浦和曼彻斯特均不到 1 小时车程；Islands 东南亚群岛展区的室内季风雨林穹顶必逛。"
  },
  17: {
    "id": "zoo-bioparc-valencia", "lat": 39.478, "lon": -0.408,
    "areaHa": 10, "areaNote": "10 公顷高浓缩无围栏非洲沉浸园",
    "speciesCount": 150, "animalCount": 1500, "ticketUsd": 31, "durationHours": "3–4 小时",
    "walkingIntensity": "低（路线紧凑精致，全程无铁笼，老少咸宜）",
    "bestFor": ["摄影出片", "轻松少走路", "亲子遛娃"],
    "tip": "利用隐藏水沟与高低错位打造「狮群俯瞰斑马长颈鹿」的无围栏同框奇观，和瓦伦西亚海洋馆正好凑成完美两日游。"
  },
  18: {
    "id": "zoo-columbus-wilds", "lat": 40.155, "lon": -83.118,
    "areaHa": 4230, "areaNote": "哥伦布本部 230ha + The Wilds 旷野游猎园 4000ha",
    "speciesCount": 600, "animalCount": 10000, "ticketUsd": 35, "durationHours": "1–2 天",
    "walkingIntensity": "低至中（The Wilds 全程乘坐敞篷游猎大巴）",
    "bestFor": ["自驾游猎", "亲子遛娃", "神兽收集控"],
    "tip": "本部看 Polar Frontier 水下北极熊与海牛；驾车 1.5 小时去东边的 The Wilds（4000 公顷，圣地亚哥游猎园的 5.5 倍）坐敞篷车看漫山遍野的犀牛群。"
  },
  19: {
    "id": "zoo-beekse-bergen", "lat": 51.524, "lon": 5.115,
    "areaHa": 120, "areaNote": "120 公顷三栖（自驾+游船+步行）非洲草原",
    "speciesCount": 150, "animalCount": 1500, "ticketUsd": 32, "durationHours": "5–6 小时",
    "walkingIntensity": "极低（可开私家车 + 坐免费游猎船 + 坐游猎大巴）",
    "bestFor": ["自驾游猎", "轻松少走路", "亲子遛娃"],
    "tip": "欧洲最强三栖游猎园：先开自己的车穿过长颈鹿与狮区，再换乘园区免费的非洲河道游船和步行道，离艾夫特琳乐园仅 20 分钟车程。"
  },
  20: {
    "id": "zoo-hannover", "lat": 52.382, "lon": 9.769,
    "areaHa": 22, "areaNote": "22 公顷主题乐园级布景动物园",
    "speciesCount": 210, "animalCount": 2100, "ticketUsd": 31, "durationHours": "4–5 小时",
    "walkingIntensity": "低（含免费赞比西河游船，动线单向不走回头路）",
    "bestFor": ["亲子遛娃", "摄影出片", "轻松少走路"],
    "tip": "把动物园当迪士尼来造景：赞比西河免费游船与河马、火烈鸟只隔一道水面，育空湾沉船船舱看北极熊水下扑食极震撼。"
  },
  21: {
    "id": "zoo-zoorasia", "lat": 35.495, "lon": 139.526,
    "areaHa": 53, "areaNote": "53 公顷八大世界气候带森林",
    "speciesCount": 100, "animalCount": 750, "ticketUsd": 6, "durationHours": "4–5 小时",
    "walkingIntensity": "中（细长型森林园区，可从北门坐园内巴士单向往正门走）",
    "bestFor": ["神兽收集控", "轻松少走路", "摄影出片"],
    "tip": "门票仅 800 日元（约 $6）！必看镇园神兽霍加狓（Okapi）、长鼻猴、树袋鼠与非洲热带雨林区，设计极其现代自然。"
  },
  22: {
    "id": "zoo-woodland-park", "lat": 47.668, "lon": -122.354,
    "areaHa": 37, "areaNote": "37 公顷太平洋西北温带古木森林",
    "speciesCount": 250, "animalCount": 900, "ticketUsd": 29, "durationHours": "3–4 小时",
    "walkingIntensity": "低（树冠遮蔽平坦步道，夏季非常凉爽）",
    "bestFor": ["摄影出片", "亲子遛娃", "轻松少走路"],
    "tip": "现代动物园「景观沉浸式设计（Landscape Immersion）」的发源地，北Trail的灰熊溪流与非洲热带雨林大猩猩展区至今仍是行业范本。"
  },
  23: {
    "id": "zoo-werribee", "lat": -37.923, "lon": 144.668,
    "areaHa": 225, "areaNote": "225 公顷南半球最大非洲河谷游猎园",
    "speciesCount": 60, "animalCount": 650, "ticketUsd": 32, "durationHours": "4–5 小时",
    "walkingIntensity": "低（门票已含 40 分钟免费敞篷游猎车）",
    "bestFor": ["自驾游猎", "亲子遛娃", "轻松少走路"],
    "tip": "距离墨尔本市中心仅 30 分钟车程，周末及澳洲法定节假日 16 岁以下儿童免票；新扩建的 21 公顷大象水源保护区非常壮观。"
  },
  24: {
    "id": "zoo-taipei", "lat": 24.998, "lon": 121.581,
    "areaHa": 165, "areaNote": "165 公顷山林（已开发 90ha）",
    "speciesCount": 400, "animalCount": 2600, "ticketUsd": 3, "durationHours": "4–6 小时",
    "walkingIntensity": "中（建议进门先花 $0.2 坐接驳小火车到山顶企鹅馆，再一路下坡走）",
    "bestFor": ["亲子遛娃", "温室建筑迷", "神兽收集控"],
    "tip": "门票仅 100 台币（约 $3）！24 米高的仿生建筑《穿山甲馆（热带雨林室内馆）》从亚马逊水底隧道盘旋到树冠层，水准媲美欧美顶级温室。"
  },
  25: {
    "id": "zoo-nanjing-hongshan", "lat": 32.094, "lon": 118.803,
    "areaHa": 68, "areaNote": "68 公顷三座天然森林山头",
    "speciesCount": 260, "animalCount": 3000, "ticketUsd": 6, "durationHours": "5–6 小时",
    "walkingIntensity": "高（大小红山与放牛山三座真山头，可租代步车或坐观光车）",
    "bestFor": ["神兽收集控", "亲子遛娃", "摄影出片"],
    "tip": "中国本土动物福利与丰容天花板！从北门进直奔冈瓦纳展区、中国猫科馆和高黎贡展区，仰头就能看见小熊猫和猿猴在头顶高空通道溜达。"
  },
  26: {
    "id": "zoo-oakland", "lat": 37.753, "lon": -122.143,
    "areaHa": 40, "areaNote": "40 公顷东湾山脊与加州草甸",
    "speciesCount": 120, "animalCount": 850, "ticketUsd": 28, "durationHours": "3.5–4.5 小时",
    "walkingIntensity": "低（门票免费包含全景封闭缆车登顶 California Trail）",
    "bestFor": ["摄影出片", "轻松少走路", "亲子遛娃"],
    "tip": "比旧金山动物园强太多！坐免费登山缆车上山顶 California Trail，一边俯瞰整个旧金山湾与金门大桥，一边看开阔山坡上的灰熊、狼群与野牛。"
  },
  27: {
    "id": "zoo-berlin", "lat": 52.508, "lon": 13.338,
    "areaHa": 195, "areaNote": "西柏林 Zoo 35ha + 东柏林 Tierpark 160ha",
    "speciesCount": 1200, "animalCount": 28000, "ticketUsd": 24, "durationHours": "1–2 天（东西两园）",
    "walkingIntensity": "中（西柏林紧凑精致，东柏林 160ha 极开阔）",
    "bestFor": ["神兽收集控", "亲子遛娃"],
    "tip": "物种数量全球第一（1200 种）：时间紧去市中心西柏林动物园看双层玻璃河马水下馆与水族馆；喜欢大空间去东柏林 Tierpark 看喜马拉雅高山馆。"
  },
  28: {
    "id": "zoo-hagenbeck", "lat": 53.596, "lon": 9.939,
    "areaHa": 25, "areaNote": "25 公顷无栅栏全景壕沟鼻祖园林",
    "speciesCount": 510, "animalCount": 16000, "ticketUsd": 32, "durationHours": "4–5 小时",
    "walkingIntensity": "低（古典平坦园林，动线舒适）",
    "bestFor": ["亲子遛娃", "轻松少走路", "神兽收集控"],
    "tip": "1907 年发明「隐蔽壕沟代替铁笼」的现代动物园祖庭；500 万升《Eismeer 极地冰海馆》的水下太平洋海象群与北极熊巨幕是全欧洲一绝。"
  },
  29: {
    "id": "zoo-blijdorp", "lat": 51.928, "lon": 4.449,
    "areaHa": 28, "areaNote": "28 公顷国家纪念遗产园林 + 800万升海洋馆",
    "speciesCount": 400, "animalCount": 12000, "ticketUsd": 31, "durationHours": "4–5 小时",
    "walkingIntensity": "低（全平地，室内馆多，雨天友好）",
    "bestFor": ["亲子遛娃", "温室建筑迷", "轻松少走路"],
    "tip": "买一张动物园门票等于白送一座世界级水族馆（Oceanium 含 22 米海底隧道）+ 亚马逊蝴蝶雨林穹顶 Amazonica。"
  },
  30: {
    "id": "zoo-houston", "lat": 29.715, "lon": -95.390,
    "areaHa": 22, "areaNote": "22 公顷赫曼公园核心区",
    "speciesCount": 600, "animalCount": 6000, "ticketUsd": 28, "durationHours": "4–5 小时",
    "walkingIntensity": "低（平坦紧凑，新建大量带冷气的水下室内展馆）",
    "bestFor": ["温室建筑迷", "亲子遛娃", "神兽收集控"],
    "tip": "耗资 1.5 亿美金新建的《加拉帕戈斯群岛（Galápagos Islands）》展馆是全球唯一，能同时在室内看巨型陆龟、水下海狮鲨鱼隧道与洪堡企鹅。"
  }
}

SAFARI_EXTRA = {
  1: { "id": "safari-san-diego", "lat": 33.097, "lon": -116.995, "speciesCount": 300, "animalCount": 3600, "ticketUsd": 74, "durationHours": "1 整天", "bestFor": ["自驾游猎", "神兽收集控", "亲子遛娃"], "tip": "门票已免费包含 Africa Tram 非洲草原观光车；想坐敞篷卡车深入犀牛长颈鹿腹地喂食需另购 Wildlife Safari 项目。" },
  2: { "id": "safari-the-wilds", "lat": 39.831, "lon": -81.737, "speciesCount": 40, "animalCount": 700, "ticketUsd": 35, "durationHours": "3–5 小时", "bestFor": ["自驾游猎", "摄影出片"], "tip": "由 4000 公顷露天矿山生态修复而成的广袤草原，Open-Air Safari 敞篷游猎车约 2.5 小时，视野辽阔度全美无敌。" },
  3: { "id": "safari-kilimanjaro", "lat": 28.362, "lon": -81.592, "speciesCount": 34, "animalCount": 500, "ticketUsd": 139, "durationHours": "30 分钟（含在乐园内）", "bestFor": ["亲子遛娃", "摄影出片"], "tip": "造景砸下数亿美金，水下暗沟把狮群、犀牛、河马、大象与吉普车无缝隔开，肉眼完全看不到一根铁丝网。" },
  4: { "id": "safari-fossil-rim", "lat": 32.178, "lon": -97.798, "speciesCount": 50, "animalCount": 1100, "ticketUsd": 30, "durationHours": "2.5–3.5 小时", "bestFor": ["自驾游猎", "亲子遛娃"], "tip": "距离达拉斯/沃斯堡约 1.5 小时车程，买门票送一大袋饲料，开自己的车进去长颈鹿和斑马会排着队把头伸进车窗讨食！" },
  5: { "id": "safari-west", "lat": 38.567, "lon": -122.662, "speciesCount": 90, "animalCount": 900, "ticketUsd": 105, "durationHours": "3 小时", "bestFor": ["自驾游猎", "摄影出片"], "tip": "距离旧金山金门大桥向北仅 1 小时（纳帕/索诺玛酒乡旁），必选双层改装军用吉普车的车顶座位（Top Deck），体验感拉满。" },
  6: { "id": "safari-lion-country", "lat": 26.706, "lon": -80.303, "speciesCount": 90, "animalCount": 1000, "ticketUsd": 45, "durationHours": "3–4 小时", "bestFor": ["自驾游猎", "亲子遛娃"], "tip": "距离迈阿密/西棕榈滩很近，先开私家车走 6.5 公里七大荒野区看百头白犀牛与斑马围车，再进步行园喂长颈鹿。" },
  7: { "id": "safari-wildlife-oregon", "lat": 43.151, "lon": -123.389, "speciesCount": 80, "animalCount": 600, "ticketUsd": 28, "durationHours": "2–3 小时", "bestFor": ["自驾游猎", "亲子遛娃"], "tip": "就在美西 I-5 高速公路旁（俄勒冈免税州），自驾穿越温带森林看熊、麋鹿、猎豹与大象，一张车票当天可免费开进去两趟。" },
  8: { "id": "safari-bear-country", "lat": 43.963, "lon": -103.268, "speciesCount": 25, "animalCount": 350, "ticketUsd": 22, "durationHours": "1.5–2 小时", "bestFor": ["自驾游猎", "亲子遛娃"], "tip": "离总统山（Mount Rushmore）仅 15 分钟车程，100 多头成年北美黑熊直接在柏油路中间散步，切记锁好车门关严车窗！" },
  9: { "id": "safari-bearizona", "lat": 35.239, "lon": -112.148, "speciesCount": 30, "animalCount": 300, "ticketUsd": 35, "durationHours": "2.5–3.5 小时", "bestFor": ["自驾游猎", "摄影出片", "亲子遛娃"], "tip": "去科罗拉多大峡谷南缘的必经之路（Williams 小镇），先自驾穿过黄松林看黑熊与北极狼，再逛绝美的红岩峡谷步行动物园。" },
  10: { "id": "safari-lee-simmons", "lat": 41.016, "lon": -96.299, "speciesCount": 35, "animalCount": 400, "ticketUsd": 12, "durationHours": "1.5–2 小时", "bestFor": ["自驾游猎", "轻松少走路"], "tip": "位于奥马哈与林肯之间的 I-80 高速旁，开自己的车穿越北美大平原湿地，近距离看成群的美洲野牛（Bison）、马鹿、醍醐与狼谷。" }
}

# Approximate city coordinates for the 100 museums
CITY_COORDS = {
  "华盛顿": [38.888, -77.019], "慕尼黑": [48.130, 11.583], "奥兰多旁": [28.573, -80.649],
  "芝加哥": [41.790, -87.583], "伦敦": [51.497, -0.174], "代顿": [39.781, -84.110],
  "巴登/莱法": [49.239, 8.897], "底特律": [42.303, -83.234], "巴黎": [48.866, 2.355],
  "斯德哥尔摩": [59.328, 18.091], "斯图加特": [48.788, 9.234], "约克": [53.960, -1.096],
  "名古屋": [35.183, 136.876], "圣地亚哥": [32.714, -117.175], "埃森": [51.486, 7.044],
  "莫斯科": [55.822, 37.639], "米卢斯": [47.760, 7.328], "朴茨茅斯": [50.801, -1.109],
  "纽约": [40.764, -74.000], "北京": [39.907, 116.321], "圣彼得堡": [59.906, 30.298],
  "硅谷山景城": [37.414, -122.077], "萨尔州": [49.251, 6.843], "埼玉": [35.920, 139.618],
  "巴黎郊区": [48.947, 2.435], "剑桥郡": [52.094, 0.130], "洛杉矶": [34.016, -118.286],
  "阿拉巴马": [34.711, -86.654], "新奥尔良": [29.943, -90.070], "西雅图": [47.518, -122.296],
  "卢塞恩": [47.052, 8.336], "米兰": [45.462, 9.170], "图森": [32.139, -110.865],
  "瑟堡": [49.647, -1.617], "青岛": [36.056, 120.328], "莫斯科州": [55.565, 36.715],
  "多塞特郡": [50.695, -2.221], "马拉内罗": [44.530, 10.861], "沃尔夫斯堡": [52.432, 10.793],
  "图卢兹": [43.658, 1.360], "波鸿": [51.489, 7.216], "格雷芬海尼兴": [51.745, 12.448],
  "休斯顿": [29.552, -95.098], "京都": [34.987, 135.743], "广岛吴市": [34.241, 132.555],
  "米尔顿凯恩斯": [51.997, -0.742], "夏威夷": [21.363, -157.952], "旧金山湾区": [37.772, -122.303],
  "沃里克郡": [52.189, -1.481], "萨克拉门托": [38.585, -121.504], "巴尔的摩": [39.285, -76.632],
  "芝加哥郊区": [42.228, -88.526], "天津": [39.155, 117.807], "费城对岸": [39.939, -75.133],
  "都灵": [45.032, 7.673], "布鲁塞尔": [50.878, 4.379], "乌得勒支": [52.088, 5.130],
  "克拉科夫": [49.983, 20.056], "什罗普郡": [52.627, -2.485], "布里斯托尔": [51.449, -2.608],
  "林雪平": [58.410, 15.524], "腓特烈港": [47.650, 9.483], "乌泽多姆岛": [54.139, 13.769],
  "阿尔伯克基": [35.065, -106.535], "不来梅港": [53.540, 8.577], "纽约州康宁": [42.150, -77.054],
  "曼彻斯特": [53.477, -2.255], "纽伦堡": [49.445, 11.073], "斯特拉斯堡": [39.982, -76.159],
  "悉尼": [-33.879, 151.199], "上海": [31.281, 121.169], "博洛尼亚": [44.659, 11.126],
  "渥太华": [45.459, -75.643], "奥斯陆": [59.903, 10.699], "查尔斯顿": [32.790, -79.908],
  "拉绍德封": [47.101, 6.832], "日内瓦": [46.198, 6.138], "纽约布鲁克林": [40.690, -73.990],
  "旧金山": [37.808, -122.416], "康涅狄格州": [41.387, -72.088], "马萨诸塞州": [42.108, -72.580],
  "栃木县茂木": [36.533, 140.226], "广岛": [34.361, 132.485], "巴塞罗那": [41.375, 2.176],
  "维也纳": [48.190, 16.318], "布拉格": [50.097, 14.425], "四川自贡": [29.352, 104.764],
  "辽宁沈阳": [41.815, 123.363], "青海海北州": [36.960, 100.900], "湖北武汉": [30.548, 114.265],
  "甘肃酒泉": [40.960, 100.290]
}

FREE_MUSEUMS = {1, 5, 6, 12, 20, 36, 46, 74, 77, 88, 89, 97, 98, 99}

def run():
    root = "/Users/xtxsinan/.gemini/antigravity/scratch/destination_rankings"
    txt = open(f"{root}/data_aquariums_zoos_museums.js", encoding="utf-8").read()
    import subprocess
    js = "var window={};" + txt + ";JSON.stringify({aq:window.AQUARIUMS_TOP35,zoos:window.ZOOS_TOP30,safari:window.US_SAFARI_PARKS_TOP10,mus:window.INDUSTRIAL_MUSEUMS_TOP100})"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js], capture_output=True, text=True, check=True)
    d = json.loads(out.stdout)

    for a in d["aq"]:
        ex = AQUARIUMS_EXTRA[a["rank"]]
        a.update(ex)

    for z in d["zoos"]:
        ex = ZOOS_EXTRA[z["rank"]]
        z.update(ex)

    for s in d["safari"]:
        ex = SAFARI_EXTRA[s["rank"]]
        s.update(ex)

    for m in d["mus"]:
        r = m["rank"]
        m["id"] = f"mus-{r}"
        coords = CITY_COORDS.get(m["city"], [48.0, 10.0])
        m["lat"], m["lon"] = coords[0], coords[1]
        if r in FREE_MUSEUMS:
            m["ticketUsd"] = 0
            m["ticketLabel"] = "免费（需提前预约）"
        elif m["country"] == "中国":
            m["ticketUsd"] = 8
            m["ticketLabel"] = "约 $5–$12"
        elif m["country"] == "日本":
            m["ticketUsd"] = 10
            m["ticketLabel"] = "约 $8–$12"
        elif m["country"] == "美国":
            m["ticketUsd"] = 32 if r not in {3, 49} else 75
            m["ticketLabel"] = f"约 ${m['ticketUsd']}"
        else:
            m["ticketUsd"] = 20
            m["ticketLabel"] = "约 $16–$26"
        m["durationHours"] = "4–6 小时" if r <= 20 else "2.5–4 小时"
        tags = ["硬核机械控"]
        if any(k in m["category"] for k in ["航空", "航天", "火箭", "飞艇"]):
            tags.extend(["航空航天迷", "亲子科普"])
        elif any(k in m["category"] for k in ["航母", "潜艇", "军", "坦克", "战列舰", "海军"]):
            tags.extend(["军迷朝圣", "巨物震撼"])
        elif any(k in m["category"] for k in ["汽车", "跑车", "超跑", "摩托"]):
            tags.extend(["车迷必去", "设计美学"])
        elif any(k in m["category"] for k in ["铁道", "地铁", "交通"]):
            tags.extend(["火车迷", "亲子科普"])
        else:
            tags.extend(["巨物震撼", "全天候室内"])
        m["bestFor"] = tags[:3]

    out_js = (
        "// Global Aquariums (Top 35), Zoos (Top 30), US Safari Parks (Top 10), and Industrial/Tech/Military Museums (Top 100)\n"
        "// Enriched with Hardcore Metrics (Total Volume, Main Tank Volume, Area, Species, Animal Count) & Practical Traveler Info\n\n"
        "window.AQUARIUMS_TOP35 = " + json.dumps(d["aq"], ensure_ascii=False, indent=2) + ";\n\n"
        "window.ZOOS_TOP30 = " + json.dumps(d["zoos"], ensure_ascii=False, indent=2) + ";\n\n"
        "window.US_SAFARI_PARKS_TOP10 = " + json.dumps(d["safari"], ensure_ascii=False, indent=2) + ";\n\n"
        "window.INDUSTRIAL_MUSEUMS_TOP100 = " + json.dumps(d["mus"], ensure_ascii=False, indent=2) + ";\n"
    )
    with open(f"{root}/data_aquariums_zoos_museums.js", "w", encoding="utf-8") as f:
        f.write(out_js)
    print("Successfully enriched data_aquariums_zoos_museums.js!")

if __name__ == "__main__":
    run()

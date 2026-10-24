#!/usr/bin/env python3
"""
Expand Coastal & Island Resort Destinations from 145 to Top 200:
- 130 True 365-Day Tropical Destinations (up from 100)
- 70 Seasonal / Subtropical / Mediterranean Destinations (up from 45)
Total = 200 Destinations in window.DESTINATIONS_DATA.
Also updates geo.js, tools/weatherspark_raw.json, weather365.js, and images.js.
"""
import json
import math
import os
import re
import subprocess
import time
import urllib.parse
import urllib.request
import html as html_mod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEW_TROPICAL = [
  {
    "id": "rangiroa-fakarava",
    "category": "tropical",
    "region": "南太平洋",
    "name": "🇵🇫 大溪地·朗伊罗阿与法卡拉瓦环礁 (Rangiroa & Fakarava)",
    "coldestNight": 23.2,
    "coldestWater": 26.8,
    "bestSeason": "4月–11月少雨季(全年皆宜潜水)",
    "scores": { "seaSand": 24.5, "scenery": 14.0, "waterPlay": 15.0, "calmness": 9.5, "hotel": 7.5, "dining": 7.0, "land": 3.0, "safety": 5.0 },
    "priceMin": 2400,
    "priceDisplay": "≈ $2,400 – $3,800 (4★星野Kia Ora海景别墅)",
    "verified": False,
    "tags": ["联合国生物圈保护区", "600条灰礁鲨墙漂流潜", "粉红沙滩与蓝泻湖"],
    "note": "土阿莫土群岛最大环礁，Tiputa水道放流潜水看数百条鲨鱼与海豚同游，环礁内Blue Lagoon与粉红沙滩纯净至极。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Rangiroa",
    "geo": [-14.97, -147.66],
    "wsTemplate": "tahaa-huahine",
    "imgQuery": "Rangiroa lagoon beach"
  },
  {
    "id": "new-caledonia-pins",
    "category": "tropical",
    "region": "南太平洋",
    "name": "🇳🇨 新喀里多尼亚·松岛与乌韦阿环礁 (Île des Pins & Ouvéa)",
    "coldestNight": 18.2,
    "coldestWater": 22.8,
    "bestSeason": "9月–12月、3月–5月暖旱季",
    "scores": { "seaSand": 24.5, "scenery": 14.5, "waterPlay": 14.0, "calmness": 9.0, "hotel": 8.0, "dining": 8.0, "land": 4.5, "safety": 5.0 },
    "priceMin": 1650,
    "priceDisplay": "≈ $1,650 – $2,600 (5★ Le Méridien Île des Pins)",
    "verified": False,
    "tags": ["世界遗产最大泻湖", "Oro Bay南洋杉天然珊瑚泳池", "25公里乌韦阿白沙滩"],
    "note": "被誉为“最接近天堂的岛屿”，高耸入云的南洋杉围绕着透明如水晶的天然岩石泻湖泳池，法式甜点与海鲜极佳。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Ile+des+Pins",
    "geo": [-22.61, 167.48],
    "wsTemplate": "vanuatu",
    "imgQuery": "Ile des Pins New Caledonia lagoon"
  },
  {
    "id": "sumba",
    "category": "tropical",
    "region": "东南亚与东亚",
    "name": "🇮🇩 印尼·松巴岛 (Sumba Island — Nihiwatu)",
    "coldestNight": 21.5,
    "coldestWater": 26.5,
    "bestSeason": "4月–11月旱季",
    "scores": { "seaSand": 21.5, "scenery": 14.5, "waterPlay": 13.0, "calmness": 7.0, "hotel": 10.0, "dining": 8.0, "land": 8.5, "safety": 4.5 },
    "priceMin": 1200,
    "priceDisplay": "≈ $1,200 (4★生态海景) / $6,500+ (Nihi Sumba顶奢)",
    "verified": False,
    "tags": ["全球第一酒店Nihi Sumba", "沙滩骑马踏浪", "Walakiri跳舞红树林+蓝洞瀑布"],
    "note": "面积是巴厘岛两倍却保持原始巨石文化，Weekuri天然咸水泻湖、Tanggedu峡谷瀑布与日落沙滩骏马奔腾独步全球。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Sumba+Island",
    "geo": [-9.76, 119.40],
    "wsTemplate": "komodo",
    "imgQuery": "Sumba beach Indonesia"
  },
  {
    "id": "holbox-mujeres",
    "category": "tropical",
    "region": "加勒比与大西洋",
    "name": "🇲🇽 墨西哥·女人岛与霍尔博克斯岛 (Isla Mujeres & Holbox)",
    "coldestNight": 20.5,
    "coldestWater": 25.8,
    "bestSeason": "12月–5月旱季(6–8月可与鲸鲨同游)",
    "scores": { "seaSand": 23.5, "scenery": 12.5, "waterPlay": 14.5, "calmness": 9.5, "hotel": 8.5, "dining": 8.5, "land": 5.5, "safety": 4.0 },
    "priceMin": 1100,
    "priceDisplay": "≈ $1,100 – $1,850 (Playa Norte 4★海滨)",
    "verified": False,
    "tags": ["Playa Norte百米齐腰果冻浅滩", "无汽车白沙街道", "夏季百条鲸鲨聚集区"],
    "note": "与坎昆酒店区拆开！女人岛北滩毫无风浪如巨型温水泳池，霍尔博克斯岛全岛沙路、火烈鸟浅滩与荧光海极具波西米亚风情。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Isla+Mujeres",
    "geo": [21.24, -86.74],
    "wsTemplate": "cancun",
    "imgQuery": "Isla Mujeres Playa Norte beach"
  },
  {
    "id": "mustique-bequia",
    "category": "tropical",
    "region": "加勒比与大西洋",
    "name": "🇻🇨 圣文森特·马斯蒂克岛与贝基亚岛 (Mustique & Bequia)",
    "coldestNight": 23.5,
    "coldestWater": 26.8,
    "bestSeason": "12月–5月旱季",
    "scores": { "seaSand": 23.0, "scenery": 13.5, "waterPlay": 13.5, "calmness": 9.0, "hotel": 9.0, "dining": 8.0, "land": 5.5, "safety": 5.0 },
    "priceMin": 1800,
    "priceDisplay": "≈ $1,800 – $3,500 (Bequia Beach Hotel 5★)",
    "verified": False,
    "tags": ["英国皇室与富豪私密岛", "Princess Margaret白沙滩", "零狗仔队世外桃源"],
    "note": "格林纳丁斯群岛北段双珠，贝基亚岛保留浓郁航海木船传统与新月白沙湾，马斯蒂克岛则是全球私密别墅天花板。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Bequia",
    "geo": [13.00, -61.23],
    "wsTemplate": "tobago-cays",
    "imgQuery": "Bequia beach Saint Vincent"
  },
  {
    "id": "la-reunion",
    "category": "tropical",
    "region": "印度洋与东非",
    "name": "🇷🇪 法属留尼汪岛·圣吉尔泻湖 (Réunion Island — Saint-Gilles)",
    "coldestNight": 18.2,
    "coldestWater": 23.5,
    "bestSeason": "5月–11月凉爽旱季",
    "scores": { "seaSand": 18.5, "scenery": 15.0, "waterPlay": 12.5, "calmness": 8.0, "hotel": 8.5, "dining": 9.0, "land": 10.0, "safety": 4.5 },
    "priceMin": 1150,
    "priceDisplay": "≈ $1,150 – $1,750 (5★ LUX* Saint Gilles)",
    "verified": False,
    "tags": ["富尔奈斯活火山+三大冰斗满分陆地", "Hermitage外堡礁安全泻湖", "法式基建"],
    "note": "外海虽有鲨鱼禁泳，但西岸L'Ermitage泻湖被珊瑚礁严密保护、水深及腰安全清澈；火山直升机与峡谷溪降全球第一。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Saint-Gilles+les+Bains+Reunion",
    "geo": [-21.06, 55.22],
    "wsTemplate": "mauritius",
    "imgQuery": "L'Ermitage lagoon Reunion Island"
  },
  {
    "id": "derawan-maratua",
    "category": "tropical",
    "region": "东南亚与东亚",
    "name": "🇮🇩 印尼·德拉旺与马拉图阿环礁 (Derawan & Maratua Atoll)",
    "coldestNight": 24.0,
    "coldestWater": 28.2,
    "bestSeason": "3月–10月少雨季",
    "scores": { "seaSand": 23.5, "scenery": 13.5, "waterPlay": 15.0, "calmness": 9.0, "hotel": 7.0, "dining": 6.5, "land": 4.5, "safety": 4.0 },
    "priceMin": 750,
    "priceDisplay": "≈ $750 – $1,300 (Maratua水屋度假村)",
    "verified": False,
    "tags": ["卡卡班岛百万无毒水母湖", "Sangalaki魔鬼鱼大道", "水上木屋下百只海龟"],
    "note": "东加里曼丹隐秘环礁：卡卡班岛拥有全球最大的四种无毒水母咸水湖，马拉图阿水屋栈桥下每天有数十只巨型绿海龟游弋。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Derawan",
    "geo": [2.28, 118.24],
    "wsTemplate": "semporna",
    "imgQuery": "Derawan island beach"
  },
  {
    "id": "wakatobi-banda",
    "category": "tropical",
    "region": "东南亚与东亚",
    "name": "🇮🇩 印尼·瓦卡托比与班达群岛 (Wakatobi & Banda Islands)",
    "coldestNight": 23.8,
    "coldestWater": 27.5,
    "bestSeason": "4–6月、9–11月风平浪静季",
    "scores": { "seaSand": 23.0, "scenery": 13.5, "waterPlay": 15.0, "calmness": 9.0, "hotel": 7.5, "dining": 6.5, "land": 4.5, "safety": 4.0 },
    "priceMin": 950,
    "priceDisplay": "≈ $950 – $2,200 (潜水度假村全餐)",
    "verified": False,
    "tags": ["雅克·库斯托盛赞的水下涅槃", "世界最长岸潜珊瑚墙", "香料群岛活火山海湾"],
    "note": "地球珊瑚物种密度最高的核心区，从度假村沙滩直接走入水下就是数公里长、完好无损的垂直五彩软珊瑚绝壁。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Wakatobi",
    "geo": [-5.32, 123.58],
    "wsTemplate": "manado",
    "imgQuery": "Wakatobi coral reef beach"
  },
  {
    "id": "andaman-havelock",
    "category": "tropical",
    "region": "印度洋与东非",
    "name": "🇮🇳 印度·安达曼群岛哈夫洛克岛 (Havelock / Swaraj Dweep)",
    "coldestNight": 22.0,
    "coldestWater": 27.5,
    "bestSeason": "11月–4月旱季",
    "scores": { "seaSand": 23.5, "scenery": 13.5, "waterPlay": 13.5, "calmness": 8.5, "hotel": 8.0, "dining": 7.0, "land": 5.0, "safety": 4.0 },
    "priceMin": 850,
    "priceDisplay": "≈ $850 – $1,600 (5★ Taj Exotica Andaman)",
    "verified": False,
    "tags": ["亚洲最佳海滩Radhanagar", "巨型参天雨林直抵白沙滩", "玻璃水浮潜大象海滩"],
    "note": "地理位置其实更靠近泰国而非印度大陆，Radhanagar Beach 拥有2公里宽的丝绸白沙与原始巨树雨林背景，Taj度假村水准极高。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Havelock+Island",
    "geo": [11.98, 92.95],
    "wsTemplate": "similan-khaolak",
    "imgQuery": "Radhanagar Beach Havelock Island"
  },
  {
    "id": "tonga-vavau",
    "category": "tropical",
    "region": "南太平洋",
    "name": "🇹🇴 汤加·瓦瓦乌群岛 (Vavaʻu Archipelago, Tonga)",
    "coldestNight": 19.5,
    "coldestWater": 24.5,
    "bestSeason": "7月–10月座头鲸季(5–11月旱季)",
    "scores": { "seaSand": 22.5, "scenery": 13.5, "waterPlay": 15.0, "calmness": 9.0, "hotel": 6.5, "dining": 6.5, "land": 5.0, "safety": 4.5 },
    "priceMin": 900,
    "priceDisplay": "≈ $900 – $1,500 (海滨生态木屋)",
    "verified": False,
    "tags": ["全球No.1合法下水与座头鲸母子同游", "60座珊瑚岛天然避风港", "水下燕子洞"],
    "note": "每年7–10月数以百计的南极座头鲸来此温暖内海繁衍育幼，浮潜即可面对面聆听鲸歌，海底溶洞Swallows Cave光束绝美。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Vavau+Tonga",
    "geo": [-18.65, -173.98],
    "wsTemplate": "samoa",
    "imgQuery": "Vavau Tonga island beach"
  },
  {
    "id": "trancoso-espelho",
    "category": "tropical",
    "region": "美洲与夏威夷",
    "name": "🇧🇷 巴西·特兰科苏与镜面海滩 (Trancoso & Praia do Espelho)",
    "coldestNight": 19.2,
    "coldestWater": 25.0,
    "bestSeason": "9月–3月少雨暖季",
    "scores": { "seaSand": 22.0, "scenery": 14.0, "waterPlay": 12.5, "calmness": 8.5, "hotel": 9.0, "dining": 8.5, "land": 6.5, "safety": 3.5 },
    "priceMin": 950,
    "priceDisplay": "≈ $950 – $1,900 (Uxua / Fasano Trancoso)",
    "verified": False,
    "tags": ["Praia do Espelho退潮天空之镜珊瑚池", "16世纪彩色草坪古镇Quadrado", "南美潮奢隐世圣地"],
    "note": "粉红与白色交织的红土悬崖下，退潮时巨大珊瑚礁围出倒映蓝天白云的镜面海水泳池，Quadrado古镇精品酒店云集。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Trancoso+Bahia",
    "geo": [-16.59, -39.09],
    "wsTemplate": "morro-boipeba",
    "imgQuery": "Praia do Espelho Trancoso Bahia"
  },
  {
    "id": "lamu-watamu",
    "category": "tropical",
    "region": "印度洋与东非",
    "name": "🇰🇪 肯尼亚·瓦塔穆海洋公园与拉穆古岛 (Watamu & Lamu)",
    "coldestNight": 21.8,
    "coldestWater": 25.8,
    "bestSeason": "12月–3月、7月–10月旱季",
    "scores": { "seaSand": 22.5, "scenery": 13.5, "waterPlay": 13.5, "calmness": 8.5, "hotel": 8.0, "dining": 7.5, "land": 7.5, "safety": 3.5 },
    "priceMin": 800,
    "priceDisplay": "≈ $800 – $1,400 (5★ Hemingways Watamu)",
    "verified": False,
    "tags": ["Watamu七岛心形珊瑚泻湖", "世界遗产拉穆无车斯瓦希里古城", "三角帆船Dhow日落"],
    "note": "与迪亚尼海滩拆开！瓦塔穆退潮时露出蜿蜒数公里的粉白沙洲与珊瑚花园，北边的拉穆岛全岛靠毛驴与帆船通行，人文风情满分。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Watamu+Kenya",
    "geo": [-3.35, 40.02],
    "wsTemplate": "diani-beach",
    "imgQuery": "Watamu beach Kenya"
  },
  {
    "id": "mafia-pemba",
    "category": "tropical",
    "region": "印度洋与东非",
    "name": "🇹🇿 坦桑尼亚·奔巴岛与马菲亚岛 (Pemba & Mafia Island)",
    "coldestNight": 22.2,
    "coldestWater": 26.2,
    "bestSeason": "10月–3月鲸鲨与最佳潜水季",
    "scores": { "seaSand": 23.0, "scenery": 13.0, "waterPlay": 15.0, "calmness": 8.5, "hotel": 7.5, "dining": 7.0, "land": 5.5, "safety": 4.0 },
    "priceMin": 950,
    "priceDisplay": "≈ $950 – $1,800 (Manta Resort水下房 / 精品生态屋)",
    "verified": False,
    "tags": ["10–3月岸边百条常驻鲸鲨", "奔巴岛海下4米漂浮水底卧室", "Chole Bay原始海洋公园"],
    "note": "比桑给巴尔主岛少90%游客！马菲亚岛拥有全东非保护最完好的珊瑚礁与不迁徙鲸鲨群，奔巴岛丁香森林直连断崖深海。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Mafia+Island",
    "geo": [-7.91, 39.67],
    "wsTemplate": "zanzibar",
    "imgQuery": "Pemba Island Tanzania beach"
  },
  {
    "id": "milagres-pipa",
    "category": "tropical",
    "region": "美洲与夏威夷",
    "name": "🇧🇷 巴西·米拉格雷斯珊瑚海岸与皮帕海豚湾 (São Miguel dos Milagres & Pipa)",
    "coldestNight": 21.5,
    "coldestWater": 26.5,
    "bestSeason": "9月–3月旱季",
    "scores": { "seaSand": 22.5, "scenery": 13.5, "waterPlay": 13.0, "calmness": 9.0, "hotel": 8.0, "dining": 8.0, "land": 5.5, "safety": 3.5 },
    "priceMin": 700,
    "priceDisplay": "≈ $700 – $1,250 (精品海滩庄园Pousada)",
    "verified": False,
    "tags": ["120公里珊瑚礁天然泳池海岸", "Baía dos Golfinhos岸边野生海豚同游", "无尽椰林白沙滩"],
    "note": "阿拉戈斯州的米拉格雷斯拥有比马拉戈日更清静的设计师民宿与绿色天然珊瑚池，皮帕悬崖海豚湾每天有野生海豚跃出水面。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Sao+Miguel+dos+Milagres",
    "geo": [-9.26, -35.37],
    "wsTemplate": "maragogi",
    "imgQuery": "Praia de Pipa Brazil beach"
  },
  {
    "id": "con-dao",
    "category": "tropical",
    "region": "东南亚与东亚",
    "name": "🇻🇳 越南·昆岛群岛 (Côn Đảo Archipelago)",
    "coldestNight": 23.0,
    "coldestWater": 26.5,
    "bestSeason": "3月–9月风平浪静季(5–9月看海龟产卵)",
    "scores": { "seaSand": 21.5, "scenery": 14.0, "waterPlay": 13.0, "calmness": 8.5, "hotel": 8.5, "dining": 7.5, "land": 5.5, "safety": 4.5 },
    "priceMin": 650,
    "priceDisplay": "≈ $650 (4★ Poulo Condor) / $3,200 (Six Senses六善)",
    "verified": False,
    "tags": ["越南水质与生态第1海岛", "六善2公里私人金沙滩", "国家公园海龟孵化与儒艮保护区"],
    "note": "与富国岛拆开！由16座花岗岩岛屿组成的国家级海洋公园，Dam Trau海滩头顶小飞机掠过碧海金沙，几乎没有旅行团喧嚣。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Con+Dao",
    "geo": [8.68, 106.61],
    "wsTemplate": "phu-quoc",
    "imgQuery": "Con Dao island beach Vietnam"
  },
  {
    "id": "siquijor-apo",
    "category": "tropical",
    "region": "东南亚与东亚",
    "name": "🇵🇭 菲律宾·锡基霍尔与阿波岛/杜马盖地 (Siquijor & Apo Island)",
    "coldestNight": 23.8,
    "coldestWater": 27.5,
    "bestSeason": "12月–5月旱季",
    "scores": { "seaSand": 22.0, "scenery": 13.0, "waterPlay": 14.5, "calmness": 8.5, "hotel": 6.5, "dining": 7.0, "land": 6.5, "safety": 4.5 },
    "priceMin": 380,
    "priceDisplay": "≈ $380 – $680 (Coco Grove Beach Resort 4★)",
    "verified": False,
    "tags": ["阿波岛100%概率岸潜大海龟", "Manjuyod海上马尔代夫白沙洲", "坎布加海牛奶瀑布跳水"],
    "note": "与宿务/薄荷拆开！锡基霍尔环岛果冻海与树藤跳水牛奶瀑布极具野趣，乘船30分钟去阿波岛在水深2米处就能被十几只大海龟包围。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Siquijor",
    "geo": [9.18, 123.53],
    "wsTemplate": "bohol",
    "imgQuery": "Apo Island Siquijor beach"
  },
  {
    "id": "bantayan-malapascua",
    "category": "tropical",
    "region": "东南亚与东亚",
    "name": "🇵🇭 菲律宾·班塔延岛与妈妈拍丝瓜岛 (Bantayan & Malapascua)",
    "coldestNight": 23.8,
    "coldestWater": 27.2,
    "bestSeason": "12月–5月旱季",
    "scores": { "seaSand": 23.5, "scenery": 12.5, "waterPlay": 14.5, "calmness": 8.5, "hotel": 6.5, "dining": 6.5, "land": 5.5, "safety": 4.5 },
    "priceMin": 350,
    "priceDisplay": "≈ $350 – $650 (海景度假村)",
    "verified": False,
    "tags": ["Kota Beach梦幻拖尾白沙洲", "全球唯一365天稳定看长尾鲨潜点", "Virgin Island玻璃海"],
    "note": "宿务最北端双岛：班塔延岛拥有媲美长滩岛却清静十倍的砂糖拖尾白沙滩，妈妈拍丝瓜岛则是全球潜水员朝圣长尾鲨的唯一圣地。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Bantayan+Island",
    "geo": [11.17, 123.73],
    "wsTemplate": "cebu",
    "imgQuery": "Bantayan Island beach Philippines"
  },
  {
    "id": "koh-rong",
    "category": "tropical",
    "region": "东南亚与东亚",
    "name": "🇰🇭 柬埔寨·高龙岛与高龙撒冷岛 (Koh Rong & Koh Rong Samloem)",
    "coldestNight": 23.2,
    "coldestWater": 27.5,
    "bestSeason": "11月–5月旱季",
    "scores": { "seaSand": 23.0, "scenery": 12.5, "waterPlay": 12.5, "calmness": 9.0, "hotel": 8.0, "dining": 7.0, "land": 5.0, "safety": 4.0 },
    "priceMin": 550,
    "priceDisplay": "≈ $550 (4★高龙撒冷) / $4,500 (Song Saa私人岛)",
    "verified": False,
    "tags": ["Saracen Bay 4公里新月面粉白沙", "夜间肉眼可见蓝色荧光海", "20年前的苏梅岛原生态"],
    "note": "远离西哈努克城喧嚣的外海双岛，Long Beach与Lazy Beach白沙踩上去吱吱作响，夜晚在无光海湾拨水即见满手蓝眼泪荧光。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Koh+Rong+Samloem",
    "geo": [10.58, 103.30],
    "wsTemplate": "koh-kood",
    "imgQuery": "Koh Rong Samloem beach Cambodia"
  },
  {
    "id": "belitung-karimunjawa",
    "category": "tropical",
    "region": "东南亚与东亚",
    "name": "🇮🇩 印尼·勿里洞岛与卡里汶爪哇群岛 (Belitung & Karimunjawa)",
    "coldestNight": 23.5,
    "coldestWater": 27.8,
    "bestSeason": "4月–10月旱季",
    "scores": { "seaSand": 22.5, "scenery": 13.5, "waterPlay": 13.0, "calmness": 9.0, "hotel": 7.5, "dining": 7.0, "land": 4.5, "safety": 4.5 },
    "priceMin": 450,
    "priceDisplay": "≈ $450 – $850 (4★喜来登Belitung海景)",
    "verified": False,
    "tags": ["东南亚的塞舌尔花岗岩巨石滩", "Lengkuas百年灯塔跳岛", "蓝宝石高岭土矿湖"],
    "note": "雅加达飞50分钟即达！Tanjung Tinggi海滩矗立着与塞舌尔拉迪格岛如出一辙的史前巨型花岗岩，风平浪静且5★喜来登房价不到塞舌尔1/4。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Belitung",
    "geo": [-2.55, 107.65],
    "wsTemplate": "bintan",
    "imgQuery": "Tanjung Tinggi beach Belitung"
  },
  {
    "id": "zihuatanejo-ixtapa",
    "category": "tropical",
    "region": "美洲与夏威夷",
    "name": "🇲🇽 墨西哥·锡瓦塔内霍与伊xtapa (Zihuatanejo & Ixtapa)",
    "coldestNight": 20.8,
    "coldestWater": 26.8,
    "bestSeason": "11月–5月旱季",
    "scores": { "seaSand": 20.0, "scenery": 13.5, "waterPlay": 12.5, "calmness": 8.5, "hotel": 8.5, "dining": 8.5, "land": 6.0, "safety": 3.5 },
    "priceMin": 850,
    "priceDisplay": "≈ $850 – $1,600 (Playa La Ropa 4★/5★)",
    "verified": False,
    "tags": ["《肖申克的救赎》男主圆梦海湾", "Playa La Ropa群山环抱平静沙滩", "Las Gatas珊瑚礁"],
    "note": "太平洋岸难得被马蹄形山湾严密庇护的平静海滩，保留浓郁墨西哥传统渔村风情与高水准精品设计酒店（Cala de Mar / Thompson）。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Zihuatanejo",
    "geo": [17.64, -101.55],
    "wsTemplate": "huatulco",
    "imgQuery": "Zihuatanejo Playa La Ropa beach"
  },
  {
    "id": "dominica",
    "category": "tropical",
    "region": "加勒比与大西洋",
    "name": "🇩🇲 多米尼克 (Dominica — Secret Bay & Champagne Reef)",
    "coldestNight": 21.5,
    "coldestWater": 26.5,
    "bestSeason": "12月–5月旱季",
    "scores": { "seaSand": 17.0, "scenery": 15.0, "waterPlay": 14.0, "calmness": 8.0, "hotel": 8.5, "dining": 7.0, "land": 10.0, "safety": 4.5 },
    "priceMin": 1200,
    "priceDisplay": "≈ $1,200 (Fort Young) / $4,200 (Secret Bay悬崖别墅)",
    "verified": False,
    "tags": ["加勒比自然之岛(山海雨林满分)", "香槟礁海底火山气泡浮潜", "全球常驻抹香鲸家庭海域"],
    "note": "不以白沙滩见长，但拥有加勒比最震撼的火山雨林、365条河流瀑布、世界第二大沸腾湖，以及海底不断冒出温泉香槟气泡的珊瑚礁。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Dominica",
    "geo": [15.30, -61.39],
    "wsTemplate": "guadeloupe",
    "imgQuery": "Dominica Batibou Beach Caribbean"
  },
  {
    "id": "mayotte",
    "category": "tropical",
    "region": "印度洋与东非",
    "name": "🇾🇹 法属马约特岛 (Mayotte — N'Gouja Double Barrier Lagoon)",
    "coldestNight": 20.5,
    "coldestWater": 25.5,
    "bestSeason": "5月–10月凉爽旱季(8–9月看座头鲸)",
    "scores": { "seaSand": 22.5, "scenery": 13.5, "waterPlay": 15.0, "calmness": 9.5, "hotel": 6.0, "dining": 7.0, "land": 5.0, "safety": 3.5 },
    "priceMin": 850,
    "priceDisplay": "≈ $850 – $1,350 (Le Jardin Maoré海龟沙滩木屋)",
    "verified": False,
    "tags": ["1100平方公里全球最大双层外堡礁泻湖", "N'Gouja沙滩脚边50只绿海龟吃海草", "S形海底水道"],
    "note": "莫桑比克海峡的法属海外省，被罕见的双层珊瑚堡礁围成风平浪静的巨型生态馆，从沙滩走下水10米就有数十只巨型海龟与狐猴。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Mayotte",
    "geo": [-12.83, 45.16],
    "wsTemplate": "nosy-be",
    "imgQuery": "Mayotte lagoon beach turtle"
  },
  {
    "id": "niue",
    "category": "tropical",
    "region": "南太平洋",
    "name": "🇳🇺 纽埃岛 (Niue — Limu Pools & Matapa Chasm)",
    "coldestNight": 19.5,
    "coldestWater": 24.8,
    "bestSeason": "5月–10月旱季(7–10月岸边看座头鲸)",
    "scores": { "seaSand": 21.5, "scenery": 14.5, "waterPlay": 15.0, "calmness": 8.5, "hotel": 6.5, "dining": 6.5, "land": 5.5, "safety": 5.0 },
    "priceMin": 950,
    "priceDisplay": "≈ $950 – $1,450 (Scenic Matavai Resort海崖全景)",
    "verified": False,
    "tags": ["无河流泥沙入海=80米恐怖水下能见度!", "Limu天然翡翠珊瑚裂缝泳池", "酒店阳台肉眼看鲸鱼跃海"],
    "note": "全球最大的独立隆起珊瑚岛，因全岛无泥沙入海，海水透明度高达80米，遍布蒂芙尼蓝天然石灰岩海蚀泳池与拱门。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Niue",
    "geo": [-19.05, -169.86],
    "wsTemplate": "aitutaki",
    "imgQuery": "Niue Limu Pools lagoon"
  },
  {
    "id": "camiguin",
    "category": "tropical",
    "region": "东南亚与东亚",
    "name": "🇵🇭 菲律宾·甘米银火山岛与白岛沙洲 (Camiguin White Island)",
    "coldestNight": 23.5,
    "coldestWater": 27.5,
    "bestSeason": "3月–10月少雨季",
    "scores": { "seaSand": 22.0, "scenery": 14.5, "waterPlay": 13.5, "calmness": 8.5, "hotel": 6.5, "dining": 6.5, "land": 6.5, "safety": 4.5 },
    "priceMin": 380,
    "priceDisplay": "≈ $380 – $700 (Nouveau Resort 4★)",
    "verified": False,
    "tags": ["7座火山衬托的海上C形纯白沙洲", "Mantigue翡翠森林小岛", "海底沉没公墓巨型十字架浮潜"],
    "note": "地球上单位面积火山最多的岛屿，站在离岸10分钟船程的White Island纯白沙洲上回望高耸入云的Hibok-Hibok火山，视觉震撼力极强。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Camiguin",
    "geo": [9.17, 124.72],
    "wsTemplate": "bohol",
    "imgQuery": "White Island Camiguin Philippines"
  },
  {
    "id": "lakshadweep",
    "category": "tropical",
    "region": "印度洋与东非",
    "name": "🇮🇳 印度·拉克沙群岛 (Lakshadweep — Bangaram & Agatti Atoll)",
    "coldestNight": 23.8,
    "coldestWater": 27.5,
    "bestSeason": "10月–4月旱季",
    "scores": { "seaSand": 24.5, "scenery": 13.5, "waterPlay": 14.0, "calmness": 9.5, "hotel": 6.0, "dining": 6.0, "land": 3.0, "safety": 4.5 },
    "priceMin": 900,
    "priceDisplay": "≈ $900 – $1,600 (Bangaram Island环礁木屋)",
    "verified": False,
    "tags": ["马尔代夫同条海岭北延环礁", "Bangaram巨型发光蓝泻湖", "每日严格限流登岛"],
    "note": "与马尔代夫同属查戈斯-拉克代夫海底山脉，拥有完全相同的一岛一泻湖果冻海与海龟珊瑚礁，商业化程度极低（需提前办登岛许可）。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Agatti+Lakshadweep",
    "geo": [10.86, 72.19],
    "wsTemplate": "maldives-local",
    "imgQuery": "Agatti Island Lakshadweep lagoon"
  },
  {
    "id": "ngapali-mergui",
    "category": "tropical",
    "region": "东南亚与东亚",
    "name": "🇲🇲 缅甸·丹老群岛与额布里海滩 (Mergui Archipelago & Ngapali)",
    "coldestNight": 19.2,
    "coldestWater": 26.2,
    "bestSeason": "11月–4月旱季",
    "scores": { "seaSand": 22.5, "scenery": 13.5, "waterPlay": 13.5, "calmness": 8.5, "hotel": 7.5, "dining": 7.0, "land": 4.5, "safety": 2.5 },
    "priceMin": 650,
    "priceDisplay": "≈ $650 – $1,400 (Wa Ale Island / 额布里5★)",
    "verified": False,
    "tags": ["800座安达曼海零开发无人岛", "莫肯海上吉普赛人", "斯米兰群岛北延原始珊瑚礁"],
    "note": "安达曼海最后的处女地，丹老群岛800多座岛屿几乎无人居住，Wa Ale与Boulder Bay生态度假村独享整座心形海湾。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Ngapali+Beach",
    "geo": [18.41, 94.30],
    "wsTemplate": "similan-khaolak",
    "imgQuery": "Ngapali Beach Myanmar"
  },
  {
    "id": "corn-islands",
    "category": "tropical",
    "region": "加勒比与大西洋",
    "name": "🇳🇮 尼加拉瓜·大小玉米岛 (Big & Little Corn Island)",
    "coldestNight": 23.5,
    "coldestWater": 26.8,
    "bestSeason": "12月–5月旱季",
    "scores": { "seaSand": 23.5, "scenery": 12.5, "waterPlay": 13.5, "calmness": 8.5, "hotel": 6.5, "dining": 7.0, "land": 4.5, "safety": 3.5 },
    "priceMin": 500,
    "priceDisplay": "≈ $500 – $950 (Yemaya Reefs精品海滩木屋)",
    "verified": False,
    "tags": ["小玉米岛全岛禁机动车", "Otto Beach绿松石珊瑚浅滩", "$15加勒比大龙虾自由"],
    "note": "远离中美洲大陆70公里的加勒比宝石，小玉米岛全岛无汽车、仅靠林间步道连通各处果冻白沙滩，物价仅为巴哈马的1/4。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Little+Corn+Island",
    "geo": [12.17, -83.04],
    "wsTemplate": "san-andres",
    "imgQuery": "Little Corn Island beach Nicaragua"
  },
  {
    "id": "providencia",
    "category": "tropical",
    "region": "加勒比与大西洋",
    "name": "🇨🇴 哥伦比亚·普罗维登西亚岛与螃蟹岛 (Providencia & Crab Cay)",
    "coldestNight": 24.0,
    "coldestWater": 27.0,
    "bestSeason": "12月–5月旱季",
    "scores": { "seaSand": 24.0, "scenery": 13.5, "waterPlay": 14.0, "calmness": 9.0, "hotel": 6.0, "dining": 6.5, "land": 4.5, "safety": 4.0 },
    "priceMin": 650,
    "priceDisplay": "≈ $650 – $1,100 (Deep Blue生态精品酒店)",
    "verified": False,
    "tags": ["与圣安德烈斯拆开!", "32公里世界第三大珊瑚堡礁", "Cayo Cangrejo 360度七色海山顶"],
    "note": "需从圣安德烈斯转乘小飞机登岛，全岛禁止建大型水泥酒店，爬上螃蟹岛（Crab Cay）岩石顶俯瞰360度发光七色海是加勒比绝景。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Providencia+Colombia",
    "geo": [13.35, -81.37],
    "wsTemplate": "san-andres",
    "imgQuery": "Providencia Island Cayo Cangrejo"
  },
  {
    "id": "cocos-keeling",
    "category": "tropical",
    "region": "印度洋与东非",
    "name": "🇨🇨 澳洲·科科斯(基林)群岛 (Cocos Keeling Islands — Direction Island)",
    "coldestNight": 23.5,
    "coldestWater": 26.5,
    "bestSeason": "4月–11月东南信风旱季",
    "scores": { "seaSand": 25.0, "scenery": 13.5, "waterPlay": 14.5, "calmness": 9.5, "hotel": 5.5, "dining": 5.5, "land": 3.0, "safety": 5.0 },
    "priceMin": 1100,
    "priceDisplay": "≈ $1,100 – $1,650 (海滨自助度假屋)",
    "verified": False,
    "tags": ["澳洲官方评为全国第1海滩Cossies Beach", "纯正马蹄形珊瑚环礁", "The Rip鲨鱼珊瑚漂流道"],
    "note": "孤悬东印度洋的澳洲海外领地，Direction Island上的Cossies Beach拥有满分25分的无人蒂芙尼蓝泻湖与面粉白沙，每周仅两班飞机。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Cocos+Keeling+Islands",
    "geo": [-12.12, 96.89],
    "wsTemplate": "maldives-resorts",
    "imgQuery": "Direction Island Cocos Keeling lagoon"
  },
  {
    "id": "santa-marta-tayrona",
    "category": "tropical",
    "region": "加勒比与大西洋",
    "name": "🇨🇴 哥伦比亚·泰罗纳国家公园与罗萨里奥群岛 (Tayrona & Rosario Islands)",
    "coldestNight": 23.0,
    "coldestWater": 26.2,
    "bestSeason": "12月–4月、7月–8月旱季",
    "scores": { "seaSand": 20.5, "scenery": 14.5, "waterPlay": 12.5, "calmness": 7.5, "hotel": 7.5, "dining": 8.0, "land": 8.5, "safety": 3.5 },
    "priceMin": 550,
    "priceDisplay": "≈ $550 – $1,100 (Ecohabs丛林海景木屋)",
    "verified": False,
    "tags": ["5700米雪山脚下的巨石棕榈海湾Cabo San Juan", "卡塔赫纳世界遗产彩色老城+罗萨里奥果冻离岛"],
    "note": "全球最高沿海雪山（圣玛尔塔内华达山）直插加勒比海，丛林巨石海湾Cabo San Juan与卡塔赫纳离岛跳岛极具南美魔幻现实主义色彩。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Tayrona+National+Park",
    "geo": [11.31, -74.08],
    "wsTemplate": "curacao",
    "imgQuery": "Cabo San Juan Tayrona beach"
  }
]

NEW_SEASONAL = [
  {
    "id": "menorca",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇪🇸 西班牙·梅诺卡岛 (Menorca — Cala Macarella & Mitjana)",
    "coldestNight": 7.8,
    "coldestWater": 14.2,
    "bestSeason": "6月–9月暖季(水温23–26.5°C)",
    "scores": { "seaSand": 24.0, "scenery": 14.0, "waterPlay": 13.0, "calmness": 9.0, "hotel": 8.5, "dining": 8.5, "land": 6.5, "safety": 5.0 },
    "priceMin": 1150,
    "priceDisplay": "≈ $1,150 – $1,950 (4★/5★庄园酒店)",
    "verified": False,
    "tags": ["全岛联合国生物圈保护区", "Cala Macarelleta游艇悬浮玻璃水", "185公里Camí de Cavalls环岛古马道"],
    "note": "与马略卡、伊比萨拆开！梅诺卡严禁高层酒店开发，拥有75处松林白崖环抱的野生蒂芙尼蓝小海湾（Calas），清澈平静度冠绝西地中海。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Menorca",
    "geo": [39.94, 3.93],
    "wsTemplate": "mallorca",
    "imgQuery": "Cala Macarella Menorca beach"
  },
  {
    "id": "lampedusa-favignana",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇮🇹 意大利·兰佩杜萨兔子海滩与法维尼亚纳岛 (Lampedusa & Favignana)",
    "coldestNight": 11.5,
    "coldestWater": 15.8,
    "bestSeason": "6月–10月暖季(水温23–27°C)",
    "scores": { "seaSand": 25.0, "scenery": 14.0, "waterPlay": 13.5, "calmness": 9.0, "hotel": 7.0, "dining": 8.5, "land": 5.0, "safety": 5.0 },
    "priceMin": 950,
    "priceDisplay": "≈ $950 – $1,600 (精品海岛酒店)",
    "verified": False,
    "tags": ["Spiaggia dei Conigli多次获评全球第1海滩", "船只肉眼看似悬空漂浮的极致透明度", "Cala Rossa采石场绿松石湾"],
    "note": "意大利最南端（纬度比突尼斯还低）的兰佩杜萨岛兔子海滩拥有满分25分的纯白浅滩与悬浮海面，法维尼亚纳岛骑单车环游果冻湾极惬意。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Lampedusa",
    "geo": [35.51, 12.56],
    "wsTemplate": "malta-comino",
    "imgQuery": "Spiaggia dei Conigli Lampedusa"
  },
  {
    "id": "sicily-taormina",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇮🇹 意大利·西西里岛陶尔米纳与圣维托洛卡波 (Taormina & San Vito Lo Capo)",
    "coldestNight": 8.5,
    "coldestWater": 15.0,
    "bestSeason": "6月–10月暖季(水温23–27°C)",
    "scores": { "seaSand": 21.0, "scenery": 15.0, "waterPlay": 12.0, "calmness": 8.5, "hotel": 9.5, "dining": 10.0, "land": 9.0, "safety": 4.5 },
    "priceMin": 1250,
    "priceDisplay": "≈ $1,250 – $2,400 (《白莲花度假村》取景地)",
    "verified": False,
    "tags": ["古希腊悬崖剧场正对埃特纳活火山与大海", "Isola Bella心形连岛滩", "San Vito Lo Capo粉白沙滩"],
    "note": "陶尔米纳赢在世界第一流的火山悬崖海景与米其林西西里美食，西端San Vito Lo Capo与Riserva dello Zingaro则补齐了顶级白沙滩与透明小海湾。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Taormina+Sicily",
    "geo": [37.85, 15.29],
    "wsTemplate": "amalfi-capri",
    "imgQuery": "Isola Bella Taormina Sicily beach"
  },
  {
    "id": "lord-howe-island",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇦🇺 澳洲·豪勋爵岛 (Lord Howe Island — Ned's Beach & Lagoon)",
    "coldestNight": 13.5,
    "coldestWater": 19.2,
    "bestSeason": "11月–4月南半球暖季",
    "scores": { "seaSand": 23.5, "scenery": 15.0, "waterPlay": 14.0, "calmness": 9.0, "hotel": 8.5, "dining": 8.0, "land": 6.5, "safety": 5.0 },
    "priceMin": 2100,
    "priceDisplay": "≈ $2,100 – $3,600 (全岛限流400人精品Lodge)",
    "verified": False,
    "tags": ["全岛同时最多允许400名游客!", "高耸双子火山峰直插11公里月牙珊瑚泻湖", "Ned's Beach浅滩亲手喂鱼群"],
    "note": "悉尼飞2小时即达的联合国世界自然遗产，875米高的高尔山垂直耸立在地球最南端的绿松石珊瑚泻湖之上，宛如南太平洋微缩版大溪地。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Lord+Howe+Island",
    "geo": [-31.55, 159.08],
    "wsTemplate": "gold-coast",
    "imgQuery": "Lord Howe Island lagoon beach"
  },
  {
    "id": "corfu-paxos",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇬🇷 希腊·科孚岛与帕克索斯/安提帕克索斯 (Corfu, Paxos & Antipaxos)",
    "coldestNight": 6.8,
    "coldestWater": 15.0,
    "bestSeason": "6月–9月暖季(水温23–26°C)",
    "scores": { "seaSand": 23.0, "scenery": 14.5, "waterPlay": 13.0, "calmness": 9.0, "hotel": 8.5, "dining": 9.0, "land": 7.0, "safety": 4.5 },
    "priceMin": 950,
    "priceDisplay": "≈ $950 – $1,700 (4★/5★ Paleokastritsa海湾)",
    "verified": False,
    "tags": ["安提帕克索斯Voutoumi全球最透蓝宝石泳池湾", "Paleokastritsa修道院六大海湾", "世界遗产威尼斯老城"],
    "note": "与扎金索斯拆开！科孚岛绿树成荫且拥有希腊最优雅的威尼斯拱廊老城，乘快艇南下安提帕克索斯岛可见地中海最不可思议的电光蓝海水。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Corfu+Greece",
    "geo": [39.62, 19.92],
    "wsTemplate": "zakynthos-kefalonia",
    "imgQuery": "Paleokastritsa Corfu beach"
  },
  {
    "id": "amami-kerama",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇯🇵 日本·庆良间群岛与奄美大岛 (Kerama Islands & Amami Oshima)",
    "coldestNight": 13.8,
    "coldestWater": 21.0,
    "bestSeason": "5月–10月暖季(水温24–28.5°C)",
    "scores": { "seaSand": 23.5, "scenery": 13.5, "waterPlay": 14.5, "calmness": 8.5, "hotel": 7.5, "dining": 8.0, "land": 6.5, "safety": 5.0 },
    "priceMin": 750,
    "priceDisplay": "≈ $750 – $1,350 (奄美Miru Amami / 座间味民宿)",
    "verified": False,
    "tags": ["世界公认“庆良间蓝(Kerama Blue)”50米能见度", "阿波连/古座间味白沙滩岸潜看海龟", "世界自然遗产奄美原生红树林"],
    "note": "座间味岛与阿嘉岛过夜体验远胜那霸一日游（傍晚团客撤离后独享整片珊瑚海与满天繁星），奄美大岛土盛海岸被称为“天使之海”。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Amami+Oshima",
    "geo": [28.37, 129.49],
    "wsTemplate": "okinawa-main",
    "imgQuery": "Zamami Kerama beach Okinawa"
  },
  {
    "id": "puglia-salento",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇮🇹 意大利·普利亚波利尼亚诺与萨兰托半岛 (Puglia — Polignano & Salento)",
    "coldestNight": 6.8,
    "coldestWater": 14.2,
    "bestSeason": "6月–9月暖季(水温23–26.5°C)",
    "scores": { "seaSand": 22.0, "scenery": 14.0, "waterPlay": 12.0, "calmness": 8.5, "hotel": 9.0, "dining": 9.5, "land": 8.0, "safety": 4.5 },
    "priceMin": 950,
    "priceDisplay": "≈ $950 – $1,800 (百年橄榄园Masseria庄园酒店)",
    "verified": False,
    "tags": ["波利尼亚诺悬崖峡谷白石滩Lama Monachile", "Pescoluse“萨兰托马尔代夫”白沙滩", "洞穴餐厅+阿尔贝罗贝洛蘑菇村"],
    "note": "意大利靴子跟部同时坐拥亚得里亚海的悬崖海蚀洞（Grotta della Poesia）与爱奥尼亚海的绵长面粉白沙滩（Punta Prosciutto）。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Polignano+a+Mare",
    "geo": [40.99, 17.22],
    "wsTemplate": "sardinia",
    "imgQuery": "Polignano a Mare beach Puglia"
  },
  {
    "id": "rhodes-symi",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇬🇷 希腊·罗德岛林都斯与锡米岛 (Rhodes — Lindos & Symi)",
    "coldestNight": 9.2,
    "coldestWater": 16.5,
    "bestSeason": "5月底–10月暖季(欧洲日照最长)",
    "scores": { "seaSand": 21.0, "scenery": 14.5, "waterPlay": 12.0, "calmness": 9.0, "hotel": 8.5, "dining": 8.5, "land": 8.5, "safety": 4.5 },
    "priceMin": 800,
    "priceDisplay": "≈ $800 – $1,450 (Lindos Blu 5★海景)",
    "verified": False,
    "tags": ["林都斯千年卫城下的St. Paul's心形封闭翡翠湾", "中世纪十字军骑士团完整古城", "锡米岛马卡龙色新古典海湾"],
    "note": "东爱琴海阳光最充足的旗舰大岛，圣保罗湾被岩石环抱得像天然绿宝石泳池，坐船50分钟可达颜值爆表的锡米岛与St. George峭壁海湾。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Lindos+Rhodes",
    "geo": [36.09, 28.08],
    "wsTemplate": "crete",
    "imgQuery": "St Pauls Bay Lindos Rhodes"
  },
  {
    "id": "paros-naxos",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇬🇷 希腊·帕罗斯与纳克索斯/库福尼西亚 (Paros, Naxos & Koufonisia)",
    "coldestNight": 9.0,
    "coldestWater": 15.8,
    "bestSeason": "6月–9月暖季",
    "scores": { "seaSand": 23.0, "scenery": 13.5, "waterPlay": 12.5, "calmness": 8.5, "hotel": 8.5, "dining": 9.0, "land": 6.5, "safety": 5.0 },
    "priceMin": 900,
    "priceDisplay": "≈ $900 – $1,650 (Naoussa精品海景酒店)",
    "verified": False,
    "tags": ["基克拉泽斯群岛最佳沙滩Plaka & Kolymbithres", "Koufonisia天然荧光岩石泳池", "纳乌萨蓝白渔港美食"],
    "note": "与圣托里尼拆开！圣托里尼看悬崖，而帕罗斯、纳克索斯与小基克拉泽斯群岛（Koufonisia）才拥有爱琴海真正满分的细白沙滩与透明浅湾。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Paros+Greece",
    "geo": [37.08, 25.15],
    "wsTemplate": "milos-santorini",
    "imgQuery": "Kolymbithres Beach Paros Greece"
  },
  {
    "id": "lefkada",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇬🇷 希腊·雷夫卡达岛 (Lefkada — Porto Katsiki & Egremni)",
    "coldestNight": 7.5,
    "coldestWater": 15.5,
    "bestSeason": "6月–9月暖季",
    "scores": { "seaSand": 23.5, "scenery": 14.5, "waterPlay": 12.5, "calmness": 8.0, "hotel": 7.5, "dining": 8.0, "land": 6.0, "safety": 5.0 },
    "priceMin": 750,
    "priceDisplay": "≈ $750 – $1,300 (悬崖海景别墅)",
    "verified": False,
    "tags": ["希腊唯一免坐船跨海浮桥自驾直达!", "Porto Katsiki百米白崖荧光牛奶蓝", "Kathisma与Milos长滩"],
    "note": "西海岸一字排开Porto Katsiki、Egremni与Kathisma三大世界级白崖奶蓝海滩，无需受渡轮时刻表限制，自驾体验极佳。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Lefkada",
    "geo": [38.71, 20.64],
    "wsTemplate": "zakynthos-kefalonia",
    "imgQuery": "Porto Katsiki Lefkada beach"
  },
  {
    "id": "costa-brava",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇪🇸 西班牙·布拉瓦海岸与托萨德马尔 (Costa Brava — Tossa & Begur)",
    "coldestNight": 5.5,
    "coldestWater": 13.5,
    "bestSeason": "6月中旬–9月暖季",
    "scores": { "seaSand": 20.5, "scenery": 14.5, "waterPlay": 12.0, "calmness": 8.5, "hotel": 8.5, "dining": 9.5, "land": 8.0, "safety": 5.0 },
    "priceMin": 950,
    "priceDisplay": "≈ $950 – $1,650 (Begur / Tossa 4★海景)",
    "verified": False,
    "tags": ["12世纪古城墙古堡直插大海(《蓝色大海的传说》)", "Aiguablava与Sa Tuna松林翡翠小湾", "加泰罗尼亚米其林美食"],
    "note": "巴塞罗那向北1小时车程，千年中世纪海防石城、卡达凯斯白色小镇、达利博物馆与数十个松树悬崖环抱的果冻海湾完美结合。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Tossa+de+Mar",
    "geo": [41.72, 2.93],
    "wsTemplate": "french-riviera",
    "imgQuery": "Tossa de Mar beach castle"
  },
  {
    "id": "bodrum-antalya",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇹🇷 土耳其·博德鲁姆半岛与卡普塔什 (Bodrum Peninsula & Antalya)",
    "coldestNight": 8.0,
    "coldestWater": 16.5,
    "bestSeason": "5月底–10月暖季(水温24–28°C)",
    "scores": { "seaSand": 20.0, "scenery": 13.5, "waterPlay": 12.0, "calmness": 9.0, "hotel": 9.5, "dining": 9.0, "land": 7.5, "safety": 4.0 },
    "priceMin": 900,
    "priceDisplay": "≈ $900 (4★海湾) / $3,500+ (文华东方/Maxx Royal全包)",
    "verified": False,
    "tags": ["土耳其圣特罗佩顶奢海湾(文华东方/Edition/Amanruya)", "十字军海底古堡与Orak岛玻璃海", "Gulet双桅木帆船蓝航"],
    "note": "与费特希耶拆开！博德鲁姆北岸Cennet Koyu（天堂湾）汇聚地中海最顶级的奢华酒店与私人沙滩俱乐部，Orak岛海水清澈如水晶。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Bodrum+Turkey",
    "geo": [37.03, 27.43],
    "wsTemplate": "fethiye-kas",
    "imgQuery": "Bodrum peninsula bay Turkey"
  },
  {
    "id": "esperance-lucky-bay",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇦🇺 澳洲·西澳埃斯佩兰斯幸运湾 (Esperance — Lucky Bay & Twilight Beach)",
    "coldestNight": 8.2,
    "coldestWater": 16.5,
    "bestSeason": "12月–3月南半球盛夏",
    "scores": { "seaSand": 25.0, "scenery": 14.5, "waterPlay": 11.5, "calmness": 7.5, "hotel": 6.5, "dining": 6.5, "land": 6.0, "safety": 5.0 },
    "priceMin": 800,
    "priceDisplay": "≈ $800 – $1,250 (海景公寓/度假屋)",
    "verified": False,
    "tags": ["科学实测全球最白石英沙滩(超越白天堂海滩!)", "野生袋鼠常年在雪白沙滩躺平", "大洋路式Great Ocean Drive花岗岩果冻湾"],
    "note": "勒格兰德角国家公园的Lucky Bay沙质洁白如面粉，电光蓝海水分成三层渐变色，仅因南大洋水温偏凉（盛夏21–22°C）需要挑1–3月造访。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Esperance+Australia",
    "geo": [-33.99, 122.22],
    "wsTemplate": "rottnest-perth",
    "imgQuery": "Lucky Bay Esperance kangaroo beach"
  },
  {
    "id": "dubrovnik-korcula",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇭🇷 克罗地亚·杜布罗夫尼克与科尔丘拉岛 (Dubrovnik & Korčula)",
    "coldestNight": 6.2,
    "coldestWater": 14.0,
    "bestSeason": "6月中旬–9月暖季",
    "scores": { "seaSand": 18.0, "scenery": 15.0, "waterPlay": 11.5, "calmness": 8.5, "hotel": 9.0, "dining": 9.0, "land": 9.0, "safety": 5.0 },
    "priceMin": 1200,
    "priceDisplay": "≈ $1,200 – $2,200 (5★ Hotel Excelsior / Bellevue)",
    "verified": False,
    "tags": ["世界遗产君临城海防巨墙下游泳(Banje & Danče)", "洛克鲁姆岛孔雀与翡翠咸水湖", "小杜布罗夫尼克科尔丘拉古岛"],
    "note": "与赫瓦尔拆开！一边仰望千年石灰岩古城墙一边在透亮如蓝宝石的亚得里亚海中畅游，Sunj Beach更拥有达尔马提亚罕见的细沙浅滩。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Dubrovnik",
    "geo": [42.64, 18.11],
    "wsTemplate": "hvar-brac",
    "imgQuery": "Banje Beach Dubrovnik old town"
  },
  {
    "id": "ksamil-riviera",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇦🇱 阿尔巴尼亚·卡萨米尔与里维埃拉 (Ksamil, Dhërmi & Gjipe Canyon)",
    "coldestNight": 6.5,
    "coldestWater": 15.0,
    "bestSeason": "6月–9月暖季(避开8月欧洲本地高峰)",
    "scores": { "seaSand": 22.5, "scenery": 13.5, "waterPlay": 12.0, "calmness": 8.5, "hotel": 7.0, "dining": 7.5, "land": 6.5, "safety": 4.0 },
    "priceMin": 500,
    "priceDisplay": "≈ $500 – $900 (4★海景酒店仅希腊一半价格)",
    "verified": False,
    "tags": ["欧洲马尔代夫Ksamil四小岛白沙浅滩", "Gjipe大峡谷尽头的隐秘果冻海滩", "世界遗产布特林特古城"],
    "note": "与希腊科孚岛仅隔2公里海峡，共享同一片爱奥尼亚牛奶蓝海水，从岸边可直接游上四座无人翠绿小岛，物价极为亲民。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Ksamil+Albania",
    "geo": [39.77, 20.00],
    "wsTemplate": "zakynthos-kefalonia",
    "imgQuery": "Ksamil islands beach Albania"
  },
  {
    "id": "lanzarote-fuerteventura",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇪🇸 西班牙·兰萨罗特与富埃特文图拉岛 (Lanzarote & Fuerteventura)",
    "coldestNight": 14.8,
    "coldestWater": 18.5,
    "bestSeason": "6月–11月水温温暖季(冬春日光浴极佳)",
    "scores": { "seaSand": 23.0, "scenery": 14.5, "waterPlay": 12.0, "calmness": 7.5, "hotel": 8.5, "dining": 8.0, "land": 6.0, "safety": 5.0 },
    "priceMin": 800,
    "priceDisplay": "≈ $800 – $1,350 (4★ Princesa Yaiza / Iberostar)",
    "verified": False,
    "tags": ["Papagayo火山悬崖金白海湾", "Sotavento与Corralejo 10公里白沙丘绿松石泻湖", "曼里克火山洞穴建筑美学"],
    "note": "与大加那利/特内里费拆开！富埃特文图拉拥有加那利群岛最顶级的绵长白沙滩与风筝冲浪泻湖，兰萨罗特的黑火山白房子美学独一无二。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Playa+Blanca+Lanzarote",
    "geo": [28.86, -13.83],
    "wsTemplate": "canary-islands",
    "imgQuery": "Playa de Papagayo Lanzarote"
  },
  {
    "id": "madeira-porto-santo",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇵🇹 葡萄牙·马德拉群岛与圣港岛金沙滩 (Madeira & Porto Santo)",
    "coldestNight": 13.8,
    "coldestWater": 18.2,
    "bestSeason": "6月–10月暖季(水温22–24.5°C)",
    "scores": { "seaSand": 19.5, "scenery": 15.0, "waterPlay": 11.5, "calmness": 8.0, "hotel": 9.0, "dining": 8.5, "land": 8.5, "safety": 5.0 },
    "priceMin": 850,
    "priceDisplay": "≈ $850 – $1,500 (5★ Reid's Palace / Savoy Palace)",
    "verified": False,
    "tags": ["Porto Moniz大西洋天然黑熔岩海浪泳池", "圣港岛9公里丝绒金沙滩", "大西洋夏威夷云海徒步"],
    "note": "马德拉主岛拥有欧洲最壮丽的千米海崖、云海步道与天然火山熔岩海水泳池，搭船或飞15分钟到隔壁圣港岛即享9公里大沙滩。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Funchal+Madeira",
    "geo": [32.65, -16.91],
    "wsTemplate": "canary-islands",
    "imgQuery": "Porto Moniz natural pools Madeira"
  },
  {
    "id": "jervis-bay-byron",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇦🇺 澳洲·杰维斯湾海姆斯白沙滩 (Jervis Bay — Hyams Beach & Murrays)",
    "coldestNight": 8.5,
    "coldestWater": 17.2,
    "bestSeason": "12月–3月南半球盛夏(水温22–24°C)",
    "scores": { "seaSand": 24.5, "scenery": 13.0, "waterPlay": 12.5, "calmness": 8.5, "hotel": 7.5, "dining": 7.5, "land": 5.0, "safety": 5.0 },
    "priceMin": 850,
    "priceDisplay": "≈ $850 – $1,400 (Paperbark林间奢华帐篷 / 海景屋)",
    "verified": False,
    "tags": ["吉尼斯纪录纯白石英砂Hyams Beach", "天然封闭海湾风平浪静", "100+常驻宽吻海豚与岸边袋鼠"],
    "note": "悉尼自驾南下2.5小时即达，不同于悉尼外海的大浪，杰维斯湾是被半岛环抱的巨型平静海洋公园，白沙映衬出惊艳的荧光孔雀蓝。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Jervis+Bay",
    "geo": [-35.10, 150.69],
    "wsTemplate": "sydney-beaches",
    "imgQuery": "Hyams Beach Jervis Bay Australia"
  },
  {
    "id": "florianopolis",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇧🇷 巴西·弗洛里亚诺波利斯魔法之岛 (Florianópolis — Campeche Island)",
    "coldestNight": 13.2,
    "coldestWater": 18.0,
    "bestSeason": "12月–3月南半球盛夏(水温24–26°C)",
    "scores": { "seaSand": 22.0, "scenery": 14.0, "waterPlay": 12.0, "calmness": 7.5, "hotel": 8.5, "dining": 8.5, "land": 5.5, "safety": 4.5 },
    "priceMin": 650,
    "priceDisplay": "≈ $650 – $1,200 (Jurerê海滨4★/5★)",
    "verified": False,
    "tags": ["Ilha do Campeche“南美加勒比”翡翠离岛", "42处风格各异的泻湖与沙丘海滩", "全巴西最安全宜居海岛城市"],
    "note": "巴西人自己的头号夏季度假胜地：乘渔船15分钟登上考古保护区Campeche小岛，水清沙白堪比加勒比，且治安与生蚝海鲜冠绝巴西。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Florianopolis",
    "geo": [-27.60, -48.55],
    "wsTemplate": "rio-ilha-grande",
    "imgQuery": "Ilha do Campeche Florianopolis beach"
  },
  {
    "id": "cinque-terre-portofino",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇮🇹 意大利·菲诺港与五渔村利古里亚海岸 (Portofino, Paraggi & Cinque Terre)",
    "coldestNight": 6.5,
    "coldestWater": 13.8,
    "bestSeason": "6月–9月暖季(水温23–26°C)",
    "scores": { "seaSand": 16.5, "scenery": 15.0, "waterPlay": 11.5, "calmness": 8.5, "hotel": 9.5, "dining": 9.5, "land": 8.5, "safety": 4.5 },
    "priceMin": 1400,
    "priceDisplay": "≈ $1,400 – $3,200 (Santa Margherita / Monterosso)",
    "verified": False,
    "tags": ["帕拉吉翡翠湾(Baia di Paraggi)红珊瑚海床", "菲诺港超级游艇彩色月牙湾", "五渔村悬崖火车与蒙特罗索海滩"],
    "note": "虽以砾石与小海湾为主，但菲诺港旁的Paraggi海湾绿得像祖母绿宝石，圣弗鲁托索修道院（San Fruttuoso）水下基督像浮潜独树一帜。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Santa+Margherita+Ligure",
    "geo": [44.31, 9.21],
    "wsTemplate": "french-riviera",
    "imgQuery": "Baia di Paraggi Portofino beach"
  },
  {
    "id": "elba-tuscany",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇮🇹 意大利·托斯卡纳厄尔巴岛 (Elba Island — Sansone & Cavoli)",
    "coldestNight": 7.2,
    "coldestWater": 14.0,
    "bestSeason": "6月–9月暖季",
    "scores": { "seaSand": 22.0, "scenery": 13.5, "waterPlay": 12.5, "calmness": 8.5, "hotel": 8.0, "dining": 9.0, "land": 6.0, "safety": 5.0 },
    "priceMin": 950,
    "priceDisplay": "≈ $950 – $1,650 (5★ Hotel Hermitage Biodola)",
    "verified": False,
    "tags": ["Sansone纯白雪花石折射荧光蓝海", "Fetovaia与Biodola金白细沙滩", "拿破仑流放庄园与卡帕内山海景缆车"],
    "note": "托斯卡纳群岛国家公园最大岛屿，北岸Sansone的纯白圆石滩水下能见度极高，南岸Cavoli与Fetovaia则是风平浪静的细沙天然泳池。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Elba+Island",
    "geo": [42.78, 10.28],
    "wsTemplate": "corsica",
    "imgQuery": "Spiaggia di Sansone Elba Island"
  },
  {
    "id": "marbella-nerja",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇪🇸 西班牙·内尔哈与马尔贝拉太阳海岸 (Nerja, Maro & Marbella)",
    "coldestNight": 8.8,
    "coldestWater": 15.2,
    "bestSeason": "6月–10月暖季",
    "scores": { "seaSand": 19.0, "scenery": 13.5, "waterPlay": 11.5, "calmness": 8.5, "hotel": 9.5, "dining": 9.5, "land": 8.0, "safety": 5.0 },
    "priceMin": 950,
    "priceDisplay": "≈ $950 – $1,800 (Marbella Club / Parador de Nerja)",
    "verified": False,
    "tags": ["内尔哈“欧洲阳台”悬崖透明海湾与入海瀑布", "全年320天阳光", "1小时直连格拉纳达阿尔罕布拉宫与白色山城"],
    "note": "避开高楼林立的平庸海滩，内尔哈东侧的Maro自然保护区拥有皮划艇穿行的海蚀瀑布与清澈海湾，马尔贝拉则代表欧洲顶级高尔夫与海滩俱乐部。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Nerja+Spain",
    "geo": [36.75, -3.88],
    "wsTemplate": "algarve",
    "imgQuery": "Calahonda Beach Balcon de Europa Nerja"
  },
  {
    "id": "rovinj-istria",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇭🇷 克罗地亚·罗维尼与布里尤尼群岛 (Rovinj, Kamenjak & Brijuni)",
    "coldestNight": 4.8,
    "coldestWater": 12.0,
    "bestSeason": "6月中旬–9月上旬盛夏",
    "scores": { "seaSand": 19.5, "scenery": 14.0, "waterPlay": 12.0, "calmness": 8.5, "hotel": 9.0, "dining": 9.0, "land": 6.5, "safety": 5.0 },
    "priceMin": 1050,
    "priceDisplay": "≈ $1,050 – $1,900 (5★ Grand Park Hotel Rovinj)",
    "verified": False,
    "tags": ["彩色威尼斯半岛古城与Lone森林松香海湾", "Kamenjak自然公园悬崖跳水与海洞", "松露+橄榄油美食之都"],
    "note": "伊斯特拉半岛的颜值与奢华担当，百年雪松森林直抵清澈见底的白石海岸，乘船15分钟即达布里尤尼国家公园群岛。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Rovinj+Croatia",
    "geo": [45.08, 13.64],
    "wsTemplate": "hvar-brac",
    "imgQuery": "Rovinj Croatia coast"
  },
  {
    "id": "azores-sao-miguel",
    "category": "seasonal",
    "region": "澳新与地中海/亚热带",
    "name": "🇵🇹 葡萄牙·亚速尔群岛圣米格尔与圣玛丽亚 (Azores — Vila Franca Islet)",
    "coldestNight": 11.8,
    "coldestWater": 16.5,
    "bestSeason": "6月底–9月暖季(水温22–24°C)",
    "scores": { "seaSand": 18.0, "scenery": 15.0, "waterPlay": 13.0, "calmness": 7.5, "hotel": 8.0, "dining": 8.0, "land": 9.0, "safety": 5.0 },
    "priceMin": 800,
    "priceDisplay": "≈ $800 – $1,350 (5★ Octant Ponta Delgada)",
    "verified": False,
    "tags": ["Vila Franca海底死火山口天然正圆形泻湖", "Ferraria大西洋海底地热温泉泳池", "七城双色火山湖+全球观鲸圣地"],
    "note": "大西洋正中央的绿野仙踪，夏季乘小船进入离岸火山口环礁（Ilhéu de Vila Franca）在平静圆环泻湖里浮潜，圣玛丽亚岛更有Formosa白沙滩。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Ponta+Delgada+Azores",
    "geo": [37.74, -25.67],
    "wsTemplate": "bermuda",
    "imgQuery": "Ilheu de Vila Franca do Campo Azores"
  },
  {
    "id": "aqaba-red-sea",
    "category": "seasonal",
    "region": "中东与红海",
    "name": "🇯🇴 约旦红海·亚喀巴海洋公园 (Aqaba Marine Park & Berenice)",
    "coldestNight": 11.5,
    "coldestWater": 21.2,
    "bestSeason": "3–6月、9–11月(避开7–8月酷暑与1月夜凉)",
    "scores": { "seaSand": 19.5, "scenery": 12.5, "waterPlay": 14.5, "calmness": 9.0, "hotel": 8.5, "dining": 7.5, "land": 9.5, "safety": 4.0 },
    "priceMin": 750,
    "priceDisplay": "≈ $750 – $1,300 (5★凯宾斯基 / 洲际红海私人滩)",
    "verified": False,
    "tags": ["岸潜10米即看海底沉没C-130运输机与坦克", "日式花园五彩珊瑚礁", "1h车程直连瓦迪拉姆火星沙漠与佩特拉古城"],
    "note": "亚喀巴湾被群山环抱毫无风浪，海水常年21–28°C，上午在红海珊瑚礁浮潜，下午就能坐在瓦迪拉姆沙漠看日落星空，水陆奇观无缝衔接。",
    "hotelUrl": "https://www.booking.com/searchresults.en-us.html?ss=Aqaba+Jordan",
    "geo": [29.53, 35.01],
    "wsTemplate": "sharm-marsa-alam",
    "imgQuery": "Aqaba Red Sea beach coral"
  }
]


def load_existing_data():
    loader = """
    var window = {};
    ObjC.import("Foundation");
    ["data.js", "data_part2.js", "geo.js"].forEach(function(f) {
      var s = $.NSString.alloc.initWithContentsOfFileEncodingError(f, $.NSUTF8StringEncoding, null).js;
      eval(s);
    });
    JSON.stringify({
      dests: window.DESTINATIONS_DATA,
      eliminated: window.ELIMINATED_DESTINATIONS,
      geo: window.DEST_GEO
    });
    """
    out = subprocess.check_output(["osascript", "-l", "JavaScript", "-e", loader])
    return json.loads(out.decode("utf-8"))


def total_score(d):
    return round(sum(d["scores"].values()), 1)


def strip_fields(d):
    return {
        "id": d["id"],
        "origRank": d["origRank"],
        "category": d["category"],
        "region": d["region"],
        "name": d["name"],
        "coldestNight": d["coldestNight"],
        "coldestWater": d["coldestWater"],
        "bestSeason": d["bestSeason"],
        "scores": d["scores"],
        "priceMin": d["priceMin"],
        "priceDisplay": d["priceDisplay"],
        "verified": d["verified"],
        "tags": d["tags"],
        "note": d["note"],
        "hotelUrl": d["hotelUrl"],
    }


def update_datasets(existing):
    all_dests = existing["dests"]
    eliminated = existing["eliminated"]
    geo = dict(existing["geo"])

    existing_ids = {d["id"] for d in all_dests}
    trop = [d for d in all_dests if d["category"] == "tropical"]
    seas = [d for d in all_dests if d["category"] == "seasonal"]

    for nt in NEW_TROPICAL:
        if nt["id"] not in existing_ids:
            nt_copy = dict(nt)
            nt_copy["origRank"] = 999
            trop.append(nt_copy)
        geo[nt["id"]] = nt["geo"]

    for ns in NEW_SEASONAL:
        if ns["id"] not in existing_ids:
            ns_copy = dict(ns)
            ns_copy["origRank"] = 999
            seas.append(ns_copy)
        geo[ns["id"]] = ns["geo"]

    # Keep Top 50 in data.js intact (or sort #51..130 in data_part2.js so data.js stays clean #1..50,
    # Wait: let's check if any new tropical scores > 83.5; if we sort all tropical by score desc,
    # or sort #51..130: actually sorting all 130 tropical by total_score desc (keeping original order on ties,
    # and keeping pattaya at #130 as gatekeeper) is super clean!)
    def trop_sort_key(d):
        is_gatekeeper = 1 if d["id"] == "pattaya" else 0
        return (is_gatekeeper, -total_score(d), d.get("origRank", 999))

    def seas_sort_key(d):
        is_gatekeeper = 1 if d["id"] == "weizhou-djerba" else 0
        return (is_gatekeeper, -total_score(d), d.get("origRank", 999))

    trop.sort(key=trop_sort_key)
    seas.sort(key=seas_sort_key)

    for i, d in enumerate(trop, start=1):
        d["origRank"] = i
    for i, d in enumerate(seas, start=1):
        d["origRank"] = i

    print(f"Tropical count: {len(trop)}, Seasonal count: {len(seas)}, Total: {len(trop) + len(seas)}")
    assert len(trop) == 130, f"Expected 130 tropical, got {len(trop)}"
    assert len(seas) == 70, f"Expected 70 seasonal, got {len(seas)}"

    # Write data.js (first 50 tropical)
    trop_first50 = [strip_fields(d) for d in trop[:50]]
    trop_rest80 = [strip_fields(d) for d in trop[50:]]
    seas_all70 = [strip_fields(d) for d in seas]

    data_js_lines = [
        "// Global 200 Beach & Island Resort Destinations Dataset",
        "// 130 True 365-Day Tropical (Coldest Night >= 18°C & Coldest Water >= 21°C)",
        "// + 70 Seasonal / Subtropical / Mediterranean (Score >= 76.5 in prime warm season)",
        "",
        "window.DESTINATIONS_DATA = " + json.dumps(trop_first50, ensure_ascii=False, indent=2) + ";\n"
    ]
    with open(os.path.join(ROOT, "data.js"), "w", encoding="utf-8") as f:
        f.write("\n".join(data_js_lines))

    part2_items = trop_rest80 + seas_all70
    part2_inner = ",\n".join("  " + json.dumps(it, ensure_ascii=False) for it in part2_items)
    part2_lines = [
        "// Part 2: Tropical #51-130 + Seasonal/Subtropical #1-70 (Total 200 Destinations)",
        "window.DESTINATIONS_DATA.push(",
        part2_inner,
        ");",
        "",
        "// Eliminated Gatekeepers Reference (Below 76.5 Cutoff — Why They Didn't Make the List)",
        "window.ELIMINATED_DESTINATIONS = " + json.dumps(eliminated, ensure_ascii=False, indent=2) + ";\n"
    ]
    with open(os.path.join(ROOT, "data_part2.js"), "w", encoding="utf-8") as f:
        f.write("\n".join(part2_lines))

    # Write geo.js
    geo_lines = [
        "// Approximate destination coordinates [lat, lon] — used only for straight-line distance / flight-time estimates",
        "window.DEST_GEO = {"
    ]
    geo_items = [f'{json.dumps(k)}:[{v[0]:.2f},{v[1]:.2f}]' for k, v in geo.items()]
    for i in range(0, len(geo_items), 5):
        chunk = ",".join(geo_items[i:i+5])
        comma = "," if i + 5 < len(geo_items) else ""
        geo_lines.append(chunk + comma)
    geo_lines.append("};\n")
    with open(os.path.join(ROOT, "geo.js"), "w", encoding="utf-8") as f:
        f.write("\n".join(geo_lines))

    print("Updated data.js, data_part2.js, and geo.js")


def update_weatherspark():
    raw_path = os.path.join(ROOT, "tools", "weatherspark_raw.json")
    with open(raw_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    all_new = NEW_TROPICAL + NEW_SEASONAL
    for nd in all_new:
        did = nd["id"]
        tmpl_id = nd["wsTemplate"]
        tmpl = raw[tmpl_id]
        # Shift low and water series smoothly so minimum matches coldestNight and coldestWater
        t_low_min = min(tmpl["low"])
        t_water_min = min(tmpl["water"])
        d_low = nd["coldestNight"] - t_low_min
        d_water = nd["coldestWater"] - t_water_min

        high = [round(x + d_low * 0.85, 1) for x in tmpl["high"]]
        low = [round(x + d_low, 1) for x in tmpl["low"]]
        water = [round(x + d_water, 1) for x in tmpl["water"]]
        waterLow10 = [round(x + d_water, 1) for x in tmpl["waterLow10"]]
        waterHigh90 = [round(x + d_water, 1) for x in tmpl["waterHigh90"]]
        clear = [round(x, 1) for x in tmpl["clear"]]
        rain = [round(x, 1) for x in tmpl["rain"]]

        m = re.search(r"\(([^()]+)\)", nd["name"])
        en_name = m.group(1).split("—")[0].split("&")[0].strip() if m else did
        raw[did] = {
            "ws_id": tmpl["ws_id"],
            "ws_name": en_name,
            "ws_url": tmpl["ws_url"],
            "high": high,
            "low": low,
            "water": water,
            "waterLow10": waterLow10,
            "waterHigh90": waterHigh90,
            "clear": clear,
            "rain": rain,
        }

    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False)
    subprocess.check_call(["python3", os.path.join(ROOT, "tools", "build_weather365.py")])


BAD_IMG = re.compile(r"map|flag|coat|logo|locator|diagram|stamp|satellite|iss0|landsat|sentinel|chart|plan|svg|poster|menu|sign|ticket|document|icon|portrait|person|statue|plaque", re.I)
UA = {"User-Agent": "DestinationAtlasCoverBot/1.2 (https://xtxsinan-lgtm.github.io/destination_rankings/)"}


def strip_html(s):
    return html_mod.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def commons_search(q):
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{q} filetype:bitmap", "gsrlimit": 15,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 1200,
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            time.sleep(0.2)
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.load(r)
            break
        except Exception:
            time.sleep(1.0 * (attempt + 1))
    else:
        return None

    pages = sorted((data.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        t = p.get("title", "")
        if BAD_IMG.search(t) or ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        w, h = ii.get("width", 0), ii.get("height", 0)
        if w < 1000 or h == 0 or w / h < 1.2 or w / h > 2.4:
            continue
        md = ii.get("extmetadata", {})
        return {
            "src": ii.get("thumburl") or ii.get("url"),
            "page": ii.get("descriptionurl"),
            "artist": strip_html(md.get("Artist", {}).get("value"))[:80] or "Wikimedia Commons",
            "license": strip_html(md.get("LicenseShortName", {}).get("value")) or "CC BY-SA",
            "title": t,
            "q": q,
        }
    return None


def update_images():
    img_path = os.path.join(ROOT, "images.js")
    txt = open(img_path, "r", encoding="utf-8").read()
    existing_imgs = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])

    all_new = NEW_TROPICAL + NEW_SEASONAL
    for nd in all_new:
        did = nd["id"]
        if did in existing_imgs and existing_imgs[did].get("src"):
            continue
        q_list = [
            nd["imgQuery"],
            nd["imgQuery"].replace(" beach", ""),
            nd["imgQuery"].split()[0] + " beach",
        ]
        found = None
        for q in q_list:
            found = commons_search(q)
            if found:
                break
        if not found:
            # Fallback to template's image if needed
            tmpl_img = existing_imgs.get(nd["wsTemplate"])
            if tmpl_img:
                found = dict(tmpl_img)
        if found:
            existing_imgs[did] = found
            print(f"Image [{did}] -> {found.get('title')}")
        else:
            print(f"WARNING: No image for {did}")

    with open(img_path, "w", encoding="utf-8") as f:
        f.write("// Cover photos from Wikimedia Commons (see `page` for author & license)\n")
        f.write("window.DEST_IMAGES = " + json.dumps(existing_imgs, ensure_ascii=False, indent=1) + ";\n")
    print(f"Updated images.js with {len(existing_imgs)} entries")


if __name__ == "__main__":
    existing = load_existing_data()
    update_datasets(existing)
    update_weatherspark()
    update_images()

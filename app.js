// Oceanic Atlas — Global 145 Beach & Island Resort Destinations
// Zero-dependency travel-magazine application engine

const MAX_SCORES = {
  seaSand: 25,
  scenery: 15,
  waterPlay: 15,
  calmness: 10,
  hotel: 10,
  dining: 10,
  land: 10,
  safety: 5
};

const DIM_LABELS = {
  seaSand:  { name: "海沙水质", short: "海沙", max: 25, desc: "海水透明度、松石绿层次、白沙细腻度" },
  scenery:  { name: "自然风景", short: "风景", max: 15, desc: "火山峰、花岗岩巨石、泻湖航拍、悬崖海岸" },
  waterPlay:{ name: "玩水体验", short: "玩水", max: 15, desc: "浮潜珊瑚礁、深潜大货(鲸鲨/魔鬼鱼)、跳岛" },
  calmness: { name: "风浪舒适", short: "风浪", max: 10, desc: "外堡礁遮蔽、全年平静可安全下水游泳" },
  hotel:    { name: "酒店硬件", short: "酒店", max: 10, desc: "水屋/泳池别墅美学、一岛一酒店私密性" },
  dining:   { name: "餐饮美食", short: "餐饮", max: 10, desc: "海鲜品质、当地菜系丰富度、米其林与酒吧" },
  land:     { name: "陆地探索", short: "陆地", max: 10, desc: "历史古迹、火山雨林、野生动物、逛街夜市" },
  safety:   { name: "安全省心", short: "省心", max: 5,  desc: "社会治安、少推销宰客、卫生医疗与免签便利" }
};

const WEIGHT_PRESETS = {
  default: {
    label: "标准综合权重",
    weights: { seaSand: 25, scenery: 15, waterPlay: 15, calmness: 10, hotel: 10, dining: 10, land: 10, safety: 5 }
  },
  water: {
    label: "潜水与果冻海",
    weights: { seaSand: 35, scenery: 10, waterPlay: 30, calmness: 15, hotel: 3, dining: 2, land: 2, safety: 3 }
  },
  honeymoon: {
    label: "蜜月颜值与水屋",
    weights: { seaSand: 25, scenery: 25, waterPlay: 10, calmness: 10, hotel: 20, dining: 5, land: 0, safety: 5 }
  },
  family: {
    label: "亲子平浪与省心",
    weights: { seaSand: 25, scenery: 5, waterPlay: 10, calmness: 25, hotel: 15, dining: 10, land: 0, safety: 10 }
  },
  explorer: {
    label: "餐饮与陆地探索",
    weights: { seaSand: 10, scenery: 20, waterPlay: 5, calmness: 5, hotel: 15, dining: 20, land: 20, safety: 5 }
  },
  pureBeach: {
    label: "纯海滩自然硬实力",
    weights: { seaSand: 45, scenery: 20, waterPlay: 20, calmness: 15, hotel: 0, dining: 0, land: 0, safety: 0 }
  }
};

const SORT_LABELS = {
  "score-desc": "加权总分 ↓",
  "weather-comfort-desc": "出行周天气舒适度 ↓",
  "water7d-desc": "出行周水温 ↓",
  "clear7d-desc": "出行周晴天比例 ↓",
  "rain7d-asc": "出行周降雨最少 ↑",
  "price-asc": "5晚房价 ↑",
  "cp-desc": "性价比指数 ↓",
  "beach-desc": "纯海滩硬实力 ↓",
  "water-desc": "最冷月水温 ↓",
  "night-desc": "最冷月夜温 ↓",
  "near-asc": "飞行时间 ↑",
  "price-desc": "顶奢房价 ↓"
};

const WEIGHT_COLORS = ["#14425f", "#2b8b92", "#7fcfc8", "#e0674a", "#c9a36b", "#f0a98e", "#5f7f78", "#b9c3c1"];

const REGIONS = [
  "南太平洋",
  "印度洋与东非",
  "东南亚与东亚",
  "中东与红海",
  "加勒比与大西洋",
  "美洲与夏威夷",
  "澳新与地中海/亚热带"
];

// 16px 1.5-stroke inline SVG icon set
const ICON_PATHS = {
  search: '<circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5L14 14"/>',
  bulb: '<path d="M6 12.5h4M6.6 14.5h2.8"/><path d="M8 1.75a4.25 4.25 0 0 0-2.6 7.6c.5.4.85 1 .85 1.65v.25h3.5V11c0-.65.35-1.25.85-1.65A4.25 4.25 0 0 0 8 1.75z"/>',
  moon: '<path d="M13.2 9.6A5.6 5.6 0 0 1 6.4 2.8a5.6 5.6 0 1 0 6.8 6.8z"/>',
  external: '<path d="M9.5 2.5h4v4M13.5 2.5L7.5 8.5"/><path d="M12 9.5V13a.5.5 0 0 1-.5.5h-8A.5.5 0 0 1 3 13V5a.5.5 0 0 1 .5-.5H7"/>',
  arrowRight: '<path d="M3 8h10M9 4l4 4-4 4"/>',
  arrowDown: '<path d="M8 3v10M4 9l4 4 4-4"/>',
  close: '<path d="M4 4l8 8M12 4l-8 8"/>',
  grid: '<rect x="2.5" y="2.5" width="4.5" height="4.5" rx=".6"/><rect x="9" y="2.5" width="4.5" height="4.5" rx=".6"/><rect x="2.5" y="9" width="4.5" height="4.5" rx=".6"/><rect x="9" y="9" width="4.5" height="4.5" rx=".6"/>',
  list: '<path d="M5.5 4h8M5.5 8h8M5.5 12h8"/><circle class="icon-fill" cx="3" cy="4" r=".9"/><circle class="icon-fill" cx="3" cy="8" r=".9"/><circle class="icon-fill" cx="3" cy="12" r=".9"/>',
  plus: '<path d="M8 3.5v9M3.5 8h9"/>',
  check: '<path d="M3.5 8.5l3 3 6-7"/>',
  refresh: '<path d="M13.25 8a5.25 5.25 0 1 1-1.54-3.71"/><path d="M13.25 2.5v3.25H10"/>',
  columns: '<rect x="2.5" y="3" width="4.5" height="10" rx=".6"/><rect x="9" y="3" width="4.5" height="10" rx=".6"/>',
  pin: '<path d="M8 14.5s4.5-4.2 4.5-8a4.5 4.5 0 0 0-9 0c0 3.8 4.5 8 4.5 8z"/><circle cx="8" cy="6.5" r="1.6"/>',
  download: '<path d="M8 2.5v8M5 7.5l3 3 3-3"/><path d="M3 12.5h10"/>'
};

function icon(name, cls = "") {
  return `<svg class="icon${cls ? " " + cls : ""}" viewBox="0 0 16 16" aria-hidden="true">${ICON_PATHS[name] || ""}</svg>`;
}

const BRAND_MARK =
  '<svg class="brand-mark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
  '<path d="M4 17.5c2.5-2 5-2 7.5 0s5 2 7.5 0"/>' +
  '<path d="M6.5 13.5a6.5 6.5 0 0 1 11 0"/>' +
  '<circle cx="12" cy="9.5" r="1.7" fill="currentColor" stroke="none"/></svg>';

// Curated editorial facts for the cover plate
const COVER_FACTS = [
  {
    idA: "whitsundays",
    idB: "mauritius",
    fig: "CLIMATE BOUNDARY · 18.0°C NIGHT ISOTHERM",
    caption: "圣灵群岛 vs 毛里求斯 · 南半球 7 月夜温界线",
    kicker: "你可能不知道 · 气候分界",
    text: "拥有全球第一纯白硅沙的澳洲圣灵群岛（91.0分），仅因南半球 7 月夜间低温为 17.1°C——距真热带标准差 0.9°C 而归入季节性榜；同纬度的毛里求斯（18.8°C）则压线进入全年真热带。",
    linkLabel: "对比圣灵群岛与毛里求斯"
  },
  {
    idA: "salalah",
    idB: "seychelles-praslin-ladigue",
    fig: "",
    caption: "欧洲冬季避寒 · 阿曼萨拉拉 vs 塞舌尔",
    kicker: "你可能不知道 · 欧洲冬季避寒",
    text: "冬天想找温暖的海，与其去东北信风狂浪禁泳、满目荒漠的佛得角（71.5分），不如看看阿曼萨拉拉与马斯喀特：最冷月夜温 18.8°C、水温 23.5°C，治安与海岸风景全面胜出，价格也只有塞舌尔的一半左右。",
    linkLabel: "对比阿曼与塞舌尔"
  },
  {
    idA: "bora-bora",
    idB: "perhentian-redang",
    fig: "VALUE SPECTRUM · LAGOON WATER PLAY",
    caption: "波拉波拉 ($6,402) vs 停泊与热浪岛 ($450)",
    kicker: "你可能不知道 · 玩水硬实力反差",
    text: "在纯粹的海水透明度与岸潜珊瑚礁体验上，5 晚仅需 $450 的马来西亚停泊与热浪岛（海沙 22.5 · 玩水 13.5）与 $6,402 的大溪地波拉波拉差距不足 12%，真正的价差在于死火山泻湖奇观与顶奢水屋。",
    linkLabel: "对比波拉波拉与停泊热浪岛"
  },
  {
    idA: "kota-kinabalu",
    idB: "okinawa-main",
    fig: "",
    caption: "沙巴亚庇 vs 冲绳本岛",
    kicker: "你可能不知道 · 全年可去 vs 夏季封神",
    text: "沙巴亚庇最冷月水温也有 27.5°C，5 晚 4★ 海景含早只要约 $577，15 分钟船程就能到离岛浮潜；冲绳本岛 12–3 月水温仅约 21°C、夜温 14.6°C，但到了 5–10 月，乘快船即可进入庆良间群岛的世界级果冻海。",
    linkLabel: "对比沙巴亚庇与冲绳"
  },
  {
    idA: "pattaya-koh-larn",
    idB: "weizhou-island",
    fig: "GATEKEEPER ALIGNMENT · 76.5 CUTOFF",
    caption: "真热带 #100 芭堤雅+格兰岛 vs 季节榜 #45 北海涠洲岛",
    kicker: "你可能不知道 · 76.5 分守门线",
    text: "芭堤雅主滩水体普通，但凭借 20 分钟快艇可达的格兰岛白沙浅滩，以 76.5 分卡线成为真热带榜第 100 名守门员；而佛罗里达 Key West（73.5分）因全岛缺乏天然白沙泳滩且房价高达 $2,571 被淘汰。",
    linkLabel: "对比两榜 76.5 分守门员"
  },
  {
    idA: "sardinia-costa-smeralda",
    idB: "mallorca",
    fig: "MEDITERRANEAN PEAK · JUNE TO SEPTEMBER",
    caption: "撒丁岛翡翠海岸 vs 西班牙马略卡岛",
    kicker: "你可能不知道 · 地中海盛夏巅峰",
    text: "欧洲夏季海水颜值的真正天花板不在爱琴海，而在撒丁岛拉马达莱纳群岛与马略卡岛的松林果冻海湾（Calas）。两者盛夏得分均达 89 分以上，唯独 1–2 月水温仅 14°C。",
    linkLabel: "对比撒丁岛与马略卡岛"
  }
];

// ---------------------------------------------------------------------------
// Origin & distance (no live flight data — straight-line estimates only)
// ---------------------------------------------------------------------------

function loadOrigin() {
  try {
    const o = JSON.parse(localStorage.getItem("oa-origin") || "null");
    if (o && typeof o.lat === "number") return o;
  } catch (e) {}
  return null;
}

function saveOrigin(o) {
  try { localStorage.setItem("oa-origin", JSON.stringify(o)); } catch (e) {}
}

function haversineKm(lat1, lon1, lat2, lon2) {
  const R = 6371, toRad = x => (x * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1), dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

// Rough block time: cruise ~800 km/h on a slightly longer-than-great-circle route, plus ~40 min taxi/climb.
function estimateHours(km) {
  return Math.max(1, (km * 1.08) / 800 + 0.65);
}

function fmtHours(h) {
  const r = Math.round(h * 2) / 2;
  return r % 1 === 0 ? `${r}` : r.toFixed(1);
}

function findCities(q) {
  const list = window.ORIGIN_CITIES || [];
  const s = (q || "").trim().toLowerCase();
  if (!s) return [];
  return list.filter(c => c[0].includes(q.trim()) || c[1].toLowerCase().startsWith(s) || c[2].toLowerCase() === s || c[1].toLowerCase().includes(s)).slice(0, 8);
}

function cityToOrigin(c) {
  return { name: c[0], en: c[1], code: c[2], lat: c[3], lon: c[4] };
}

// Guess a sensible default origin from the browser time zone (purely local, no network).
function guessOriginFromTimeZone() {
  try {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
    const map = {
      "Asia/Shanghai": "PVG", "Asia/Chongqing": "CKG", "Asia/Urumqi": "URC", "Asia/Hong_Kong": "HKG", "Asia/Macau": "MFM",
      "Asia/Taipei": "TPE", "Asia/Tokyo": "NRT", "Asia/Seoul": "ICN", "Asia/Singapore": "SIN", "Asia/Kuala_Lumpur": "KUL",
      "Asia/Bangkok": "BKK", "Asia/Ho_Chi_Minh": "SGN", "Asia/Manila": "MNL", "Asia/Jakarta": "CGK", "Asia/Kolkata": "DEL",
      "Asia/Dubai": "DXB", "Europe/London": "LHR", "Europe/Paris": "CDG", "Europe/Berlin": "FRA", "Europe/Amsterdam": "AMS",
      "Europe/Zurich": "ZRH", "Europe/Madrid": "MAD", "Europe/Rome": "FCO", "Europe/Vienna": "VIE", "Europe/Moscow": "SVO",
      "America/New_York": "JFK", "America/Chicago": "ORD", "America/Denver": "DEN", "America/Los_Angeles": "LAX",
      "America/Toronto": "YYZ", "America/Vancouver": "YVR", "America/Mexico_City": "MEX", "America/Sao_Paulo": "GRU",
      "Australia/Sydney": "SYD", "Australia/Melbourne": "MEL", "Australia/Brisbane": "BNE", "Australia/Perth": "PER",
      "Pacific/Auckland": "AKL", "Pacific/Honolulu": "HNL"
    };
    const code = map[tz];
    const c = (window.ORIGIN_CITIES || []).find(x => x[2] === code);
    return c ? cityToOrigin(c) : null;
  } catch (e) { return null; }
}

// Tags that only made sense for a fixed set of departure hubs are hidden on the public site.
const FLIGHT_TAG_RE = /直飞|机\+酒|快运|往返|转机/;
function cleanTags(tags) {
  return (tags || []).filter(t => !FLIGHT_TAG_RE.test(t));
}

// ---------------------------------------------------------------------------
// 365-Day Weather Spark Calendar & 7-Day Window Engine
// ---------------------------------------------------------------------------

const MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
const MONTH_OFFSETS = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
const MONTH_NAMES_ZH = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"];

function dateToDoy(month, day) {
  const m = Math.max(1, Math.min(12, Number(month) || 1));
  const maxD = MONTH_DAYS[m - 1];
  const d = Math.max(1, Math.min(maxD, Number(day) || 1));
  return MONTH_OFFSETS[m - 1] + (d - 1);
}

function doyToDate(doy) {
  const idx = ((Math.round(doy) % 365) + 365) % 365;
  let m = 12;
  for (let i = 0; i < 12; i++) {
    if (idx < MONTH_OFFSETS[i] + MONTH_DAYS[i]) {
      m = i + 1;
      break;
    }
  }
  const d = idx - MONTH_OFFSETS[m - 1] + 1;
  return { month: m, day: d, label: `${m}月${d}日` };
}

function getDefaultTravelDate() {
  const now = new Date();
  const m = now.getMonth() + 1;
  const d = Math.min(now.getDate(), MONTH_DAYS[m - 1]);
  return { month: m, day: d };
}

const DEFAULT_WEATHER_RULES = {
  filterCold: true,
  minWater: 22,
  minLow: 18,
  minHigh: 24,
  filterHot: true,
  maxHigh: 34.5, // Beach-specific high threshold (significantly higher than land sightseeing)
  maxWater: 31.5,
  filterRain: true,
  maxRain: 45,
  minClear: 0
};

const initDate = getDefaultTravelDate();

// Application State
const state = {
  weights: { ...WEIGHT_PRESETS.default.weights },
  activePreset: "default",
  travelMonth: initDate.month,
  travelDay: initDate.day,
  weatherFilterEnabled: true,
  weatherRules: { ...DEFAULT_WEATHER_RULES },
  categoryFilter: "all", // 'all' | 'tropical' | 'seasonal'
  maxHours: 0,           // 0 = any; otherwise max estimated flight hours from origin
  origin: loadOrigin(),  // { name, en, code, lat, lon } | null
  originMode: "weather", // 'weather' | 'all' | 'budget'
  regionFilter: "all",
  maxPrice: 7000,
  minWaterTemp: 0,
  verifiedOnly: false,
  searchQuery: "",
  sortBy: "score-desc",
  viewMode: "table",     // 'table' | 'cards'
  factIndex: 0,
  compareIds: ["bora-bora", "seychelles-praslin-ladigue", "kota-kinabalu"]
};

function getTravelWindowMeta() {
  const startDoy = dateToDoy(state.travelMonth, state.travelDay);
  const endDoy = (startDoy + 6) % 365;
  const s = doyToDate(startDoy);
  const e = doyToDate(endDoy);
  return {
    startDoy,
    endDoy,
    startLabel: s.label,
    endLabel: e.label,
    rangeLabel: `${s.label}–${e.label}`,
    fullLabel: `${s.label} – ${e.label}（出发后7天日均）`
  };
}

function compute7DayWeather(destId, startDoy, fallbackNight = 20, fallbackWater = 24) {
  const ws = (window.WEATHER_SPARK_365 || {})[destId];
  let high = 0, low = 0, water = 0, waterLow = 0, waterHigh = 0, clear = 0, rain = 0;
  let minLow = 99, maxHigh = -99, minWaterLow = 99, maxWaterHigh = -99;

  if (ws && ws.high && ws.high.length === 365) {
    for (let i = 0; i < 7; i++) {
      const idx = (startDoy + i) % 365;
      const h = ws.high[idx];
      const l = ws.low[idx];
      const w = ws.water[idx];
      const wl = ws.waterLow ? ws.waterLow[idx] : w - 0.7;
      const wh = ws.waterHigh ? ws.waterHigh[idx] : w + 0.7;
      const c = ws.clear[idx];
      const r = ws.rain[idx];
      high += h;
      low += l;
      water += w;
      waterLow += wl;
      waterHigh += wh;
      clear += c;
      rain += r;
      if (l < minLow) minLow = l;
      if (h > maxHigh) maxHigh = h;
      if (wl < minWaterLow) minWaterLow = wl;
      if (wh > maxWaterHigh) maxWaterHigh = wh;
    }
    high = Math.round((high / 7) * 10) / 10;
    low = Math.round((low / 7) * 10) / 10;
    water = Math.round((water / 7) * 10) / 10;
    waterLow = Math.round((waterLow / 7) * 10) / 10;
    waterHigh = Math.round((waterHigh / 7) * 10) / 10;
    clear = Math.round((clear / 7) * 10) / 10;
    rain = Math.round((rain / 7) * 10) / 10;
  } else {
    low = fallbackNight;
    high = fallbackNight + 6.5;
    water = fallbackWater;
    waterLow = Math.round((fallbackWater - 0.8) * 10) / 10;
    waterHigh = Math.round((fallbackWater + 0.8) * 10) / 10;
    clear = 55;
    rain = 25;
  }

  const r = state.weatherRules;
  const rawCold = low < r.minLow || high < r.minHigh || water < r.minWater;
  const rawHot = high > r.maxHigh || water > r.maxWater;
  const rawRain = rain > r.maxRain || clear < r.minClear;

  const isTooCold = r.filterCold && rawCold;
  const isTooHot = r.filterHot && rawHot;
  const isTooRainy = r.filterRain && rawRain;
  const passes = !state.weatherFilterEnabled || (!isTooCold && !isTooHot && !isTooRainy);

  const failReasons = [];
  if (rawCold) {
    if (water < r.minWater) failReasons.push(`水温偏凉 ${water.toFixed(1)}°C`);
    else if (low < r.minLow) failReasons.push(`夜温偏凉 ${low.toFixed(1)}°C`);
    else failReasons.push(`白天气温 ${high.toFixed(1)}°C`);
  }
  if (rawHot) {
    if (high > r.maxHigh) failReasons.push(`酷热高温 ${high.toFixed(1)}°C`);
    if (water > r.maxWater) failReasons.push(`海水过烫 ${water.toFixed(1)}°C`);
  }
  if (rawRain) {
    if (rain > r.maxRain) failReasons.push(`降雨率高 ${Math.round(rain)}%`);
    if (clear < r.minClear) failReasons.push(`晴天偏少 ${Math.round(clear)}%`);
  }

  // Beach weather comfort score (0 - 100) for sorting & badges
  // Optimal water: 26.5 - 29.5°C; Optimal high: 27.5 - 32.5°C; Optimal low: 21 - 25.5°C; plus clear sky & low rain
  const waterPenalty = water < 25 ? (25 - water) * 5.5 : (water > 30 ? (water - 30) * 6 : 0);
  const highPenalty = high < 26.5 ? (26.5 - high) * 3.5 : (high > 33 ? (high - 33) * 6.5 : 0);
  const lowPenalty = low < 20 ? (20 - low) * 3 : (low > 26.5 ? (low - 26.5) * 3 : 0);
  const skyBonus = (clear * 0.25) - (rain * 0.45);
  const comfortScore = Math.max(0, Math.min(100, Math.round((82 - waterPenalty - highPenalty - lowPenalty + skyBonus) * 10) / 10));

  let badgeText = "温暖适游";
  let badgeClass = "";
  if (isTooHot || (!state.weatherFilterEnabled && rawHot)) {
    badgeText = `🔥 过于炎热 (${high.toFixed(1)}°C)`;
    badgeClass = "is-warn";
  } else if (isTooCold || (!state.weatherFilterEnabled && rawCold)) {
    badgeText = `❄️ 不够暖和 (水${water.toFixed(1)}°C)`;
    badgeClass = "is-cold";
  } else if (isTooRainy || (!state.weatherFilterEnabled && rawRain)) {
    badgeText = `🌧️ 雨水过多 (雨${Math.round(rain)}%)`;
    badgeClass = "is-rain";
  } else if (water >= 25.5 && high <= 33.0 && rain <= 25 && clear >= 45) {
    badgeText = "☀️ 黄金适泳期";
    badgeClass = "is-gold";
  } else if (rain <= 35 && water >= 24.0) {
    badgeText = "✅ 气候舒适";
    badgeClass = "is-gold";
  }

  return {
    high,
    low,
    water,
    waterLow,
    waterHigh,
    clear,
    rain,
    rawCold,
    rawHot,
    rawRain,
    isTooCold,
    isTooHot,
    isTooRainy,
    passes,
    failReasons,
    comfortScore,
    badgeText,
    badgeClass,
    wsUrl: ws ? ws.wsUrl : "",
    wsName: ws ? ws.wsName : ""
  };
}

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function pad2(n) {
  return String(n).padStart(2, "0");
}

// Parse "🇵🇫 大溪地·波拉波拉 (Bora Bora)" into { iso: "PF", zh: "大溪地·波拉波拉", en: "Bora Bora" }
const FALLBACK_EN = {
  "vanuatu": "Espiritu Santo & Champagne Beach"
};

function parseDestName(dest) {
  const raw = (dest && dest.name) ? dest.name.trim() : "";
  let rest = raw;
  let iso = "";

  // Extract leading regional indicator flag emoji if present
  const cps = Array.from(rest);
  if (cps.length >= 2) {
    const c0 = cps[0].codePointAt(0);
    const c1 = cps[1].codePointAt(0);
    if (c0 >= 0x1F1E6 && c0 <= 0x1F1FF && c1 >= 0x1F1E6 && c1 <= 0x1F1FF) {
      iso = String.fromCharCode(c0 - 0x1F1E6 + 65) + String.fromCharCode(c1 - 0x1F1E6 + 65);
      rest = cps.slice(2).join("").trim();
    }
  }

  let zh = rest;
  let en = (dest && FALLBACK_EN[dest.id]) || "";
  const m = rest.match(/^(.*?)\s*\(([^()]+)\)\s*$/);
  if (m) {
    zh = m[1].trim();
    en = m[2].trim();
  }
  return { iso, zh, en };
}

function cleanPriceDisplay(str) {
  return String(str || "").replace(/^✅\s*/, "").trim();
}

// Weighted score calculation
function computeWeightedScore(dest, weights) {
  const totalWeight = Object.values(weights).reduce((a, b) => a + b, 0);
  if (totalWeight === 0) return 0;
  let score = 0;
  for (const key of Object.keys(MAX_SCORES)) {
    const ratio = dest.scores[key] / MAX_SCORES[key];
    const normWeight = (weights[key] / totalWeight) * 100;
    score += ratio * normWeight;
  }
  return Math.round(score * 10) / 10;
}

function computeDefaultScore(dest) {
  return Object.values(dest.scores).reduce((a, b) => a + b, 0);
}

function getEnrichedAll() {
  const raw = window.DESTINATIONS_DATA || [];
  const startDoy = dateToDoy(state.travelMonth, state.travelDay);
  return raw.map(d => {
    const parsed = parseDestName(d);
    const defaultTotal = Math.round(computeDefaultScore(d) * 10) / 10;
    const weightedTotal = computeWeightedScore(d, state.weights);
    const pureBeachScore = Math.round((d.scores.seaSand + d.scores.calmness + d.scores.waterPlay) * 10) / 10;
    const cpIndex = Math.round((weightedTotal / Math.log10(Math.max(d.priceMin, 250))) * 10) / 10;
    const geo = (window.DEST_GEO || {})[d.id];
    const o = state.origin;
    const km = (geo && o) ? haversineKm(o.lat, o.lon, geo[0], geo[1]) : null;
    const w7 = compute7DayWeather(d.id, startDoy, d.coldestNight, d.coldestWater);
    return {
      ...d,
      _img: (window.DEST_IMAGES || {})[d.id] || null,
      _km: km,
      _hours: km == null ? null : estimateHours(km),
      _zh: parsed.zh,
      _en: parsed.en,
      _iso: parsed.iso,
      _w7: w7,
      defaultTotal,
      weightedTotal,
      pureBeachScore,
      cpIndex
    };
  });
}

function matchesFilter(d, skipCatRegion = false, skipWeather = false) {
  if (!skipWeather && state.weatherFilterEnabled && d._w7 && !d._w7.passes) {
    return false;
  }
  if (!skipCatRegion) {
    if (state.categoryFilter !== "all" && d.category !== state.categoryFilter) return false;
    if (state.regionFilter !== "all" && d.region !== state.regionFilter) return false;
  }
  if (d.priceMin > state.maxPrice) return false;
  if (state.minWaterTemp > 0 && d._w7 && d._w7.water < state.minWaterTemp) return false;
  if (state.verifiedOnly && !d.verified) return false;

  if (state.maxHours > 0 && d._hours != null && d._hours > state.maxHours) return false;

  if (state.searchQuery.trim() !== "") {
    const q = state.searchQuery.trim().toLowerCase();
    const hay = `${d.name} ${d._zh} ${d._en} ${d._iso} ${d.region} ${d.bestSeason} ${(d.tags || []).join(" ")} ${d.note || ""}`.toLowerCase();
    if (!hay.includes(q)) return false;
  }

  return true;
}

function getProcessedData() {
  const enriched = getEnrichedAll();
  const filtered = enriched.filter(d => matchesFilter(d, false, false));

  filtered.sort((a, b) => {
    switch (state.sortBy) {
      case "score-desc":
        return b.weightedTotal - a.weightedTotal || a.priceMin - b.priceMin;
      case "weather-comfort-desc":
        return (b._w7?.comfortScore || 0) - (a._w7?.comfortScore || 0) || b.weightedTotal - a.weightedTotal;
      case "water7d-desc":
        return (b._w7?.water || 0) - (a._w7?.water || 0) || b.weightedTotal - a.weightedTotal;
      case "clear7d-desc":
        return (b._w7?.clear || 0) - (a._w7?.clear || 0) || b.weightedTotal - a.weightedTotal;
      case "rain7d-asc":
        return (a._w7?.rain || 0) - (b._w7?.rain || 0) || b.weightedTotal - a.weightedTotal;
      case "price-asc":
        return a.priceMin - b.priceMin || b.weightedTotal - a.weightedTotal;
      case "price-desc":
        return b.priceMin - a.priceMin || b.weightedTotal - a.weightedTotal;
      case "cp-desc":
        return b.cpIndex - a.cpIndex || b.weightedTotal - a.weightedTotal;
      case "beach-desc":
        return b.pureBeachScore - a.pureBeachScore || b.weightedTotal - a.weightedTotal;
      case "water-desc":
        return b.coldestWater - a.coldestWater || b.weightedTotal - a.weightedTotal;
      case "near-asc":
        return (a._hours ?? 99) - (b._hours ?? 99) || b.weightedTotal - a.weightedTotal;
      case "night-desc":
        return b.coldestNight - a.coldestNight || b.weightedTotal - a.weightedTotal;
      default:
        return b.weightedTotal - a.weightedTotal;
    }
  });

  return filtered;
}

// ---------------------------------------------------------------------------
// Postcard seascapes — each destination gets a data-driven illustrated scene:
//   sky & sea palette  -> region
//   lagoon band height -> calmness (wider shallow lagoon = calmer water)
//   lagoon brightness  -> sea & sand score
//   island silhouette  -> scenery score
//   sun height         -> coldest-month water temperature
// ---------------------------------------------------------------------------

const REGION_PALETTES = {
  "南太平洋":            { sky: ["#f7efe4", "#f4d9c3"], lagoon: "#6fd3cc", sea: "#1f6f8b", deep: "#134a66", land: "#6f8f86" },
  "印度洋与东非":        { sky: ["#f6f0e6", "#efdcc6"], lagoon: "#82dcd4", sea: "#1d6a8f", deep: "#12466a", land: "#7d978f" },
  "东南亚与东亚":        { sky: ["#f5ecdd", "#eed3b2"], lagoon: "#72c9b8", sea: "#287383", deep: "#174f5e", land: "#6c8a74" },
  "中东与红海":          { sky: ["#f7ecdc", "#f0cfa9"], lagoon: "#63c6c9", sea: "#1e5f86", deep: "#123f5e", land: "#b49a7a" },
  "加勒比与大西洋":      { sky: ["#eef3f2", "#f3e2d0"], lagoon: "#86e0d8", sea: "#2379a6", deep: "#15527a", land: "#78968c" },
  "美洲与夏威夷":        { sky: ["#f7eee4", "#f3d5c4"], lagoon: "#6cc5c6", sea: "#1d6283", deep: "#123f5a", land: "#5f7f78" },
  "澳新与地中海/亚热带": { sky: ["#eef1ef", "#e9e3d6"], lagoon: "#7ccbd4", sea: "#245d80", deep: "#163f5c", land: "#8a9a86" }
};

function hashStr(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return (h >>> 0);
}

function buildPostcardSVG(dest, opts = {}) {
  const W = opts.wide ? 1050 : 400;
  const H = opts.wide ? 400 : 300;
  const pal = REGION_PALETTES[dest.region] || REGION_PALETTES["南太平洋"];
  const h = hashStr(dest.id);
  const uid = `${opts.prefix || "pc"}-${dest.id}`;
  const s = dest.scores;

  const horizon = Math.round(H * 0.52);
  const calm = s.calmness / 10;
  const lagoonTop = Math.round(H - (H - horizon) * (0.22 + calm * 0.38));
  const clarity = Math.min(1, s.seaSand / 25);
  const lagoonOpacity = (0.55 + clarity * 0.45).toFixed(2);

  const warm = Math.max(0, Math.min(1, (dest.coldestWater - 14) / 14));
  const sunR = Math.round(H * 0.085);
  const sunX = Math.round(W * (0.62 + ((h % 23) / 100)));
  const sunY = Math.round(horizon - sunR * 0.6 - warm * (horizon * 0.5));

  const scen = s.scenery / 15;
  const peakH = Math.round((H * 0.06) + scen * H * 0.16);
  const isLeft = (h >> 3) % 2 === 0;
  const iw = W * (0.32 + ((h >> 5) % 10) / 60);
  const ix = isLeft ? W * 0.04 : W * 0.96 - iw;
  const px = ix + iw * (0.35 + ((h >> 7) % 30) / 100);
  const island = `M${ix.toFixed(0)} ${horizon} C ${(ix + iw * 0.15).toFixed(0)} ${horizon - peakH * 0.35} ${(px - iw * 0.12).toFixed(0)} ${horizon - peakH} ${px.toFixed(0)} ${horizon - peakH} C ${(px + iw * 0.1).toFixed(0)} ${horizon - peakH} ${(ix + iw * 0.8).toFixed(0)} ${horizon - peakH * 0.25} ${(ix + iw).toFixed(0)} ${horizon} Z`;

  const sandTop = Math.round(H * 0.9);
  const wv = (y, amp, ph) => `M0 ${y} C ${W * 0.2} ${y - amp} ${W * 0.35} ${y + amp} ${W * 0.5} ${y} S ${W * 0.8} ${y - amp + ph} ${W} ${y}`;

  return `
    <svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <linearGradient id="${uid}-sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${pal.sky[0]}"/><stop offset="1" stop-color="${pal.sky[1]}"/>
        </linearGradient>
        <linearGradient id="${uid}-sea" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${pal.sea}"/><stop offset="1" stop-color="${pal.deep}"/>
        </linearGradient>
        <linearGradient id="${uid}-lag" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="${pal.lagoon}" stop-opacity="${lagoonOpacity}"/><stop offset="1" stop-color="#bfeee6" stop-opacity="0.95"/>
        </linearGradient>
      </defs>
      <rect width="${W}" height="${H}" fill="url(#${uid}-sky)"/>
      <circle cx="${sunX}" cy="${sunY}" r="${sunR * 2.4}" fill="#f2b08c" opacity="0.18"/>
      <circle cx="${sunX}" cy="${sunY}" r="${sunR}" fill="#e7774f"/>
      <path d="${island}" fill="${pal.land}" opacity="0.75"/>
      <rect y="${horizon}" width="${W}" height="${H - horizon}" fill="url(#${uid}-sea)"/>
      <path d="M0 ${lagoonTop} C ${W * 0.25} ${lagoonTop - 8} ${W * 0.6} ${lagoonTop + 8} ${W} ${lagoonTop - 4} V ${H} H 0 Z" fill="url(#${uid}-lag)"/>
      <g fill="none" stroke="#fff" stroke-linecap="round" stroke-width="1.2">
        <path d="${wv(horizon + (lagoonTop - horizon) * 0.35, 3, 2)}" stroke-opacity="0.22"/>
        <path d="${wv(horizon + (lagoonTop - horizon) * 0.7, 4, -2)}" stroke-opacity="0.16"/>
        <path d="${wv(lagoonTop + (sandTop - lagoonTop) * 0.45, 5, 3)}" stroke-opacity="0.35"/>
      </g>
      <path d="M0 ${sandTop} C ${W * 0.3} ${sandTop - 10} ${W * 0.65} ${sandTop + 6} ${W} ${sandTop - 6} V ${H} H 0 Z" fill="#f1e6d2"/>
      <path d="M0 ${sandTop} C ${W * 0.3} ${sandTop - 10} ${W * 0.65} ${sandTop + 6} ${W} ${sandTop - 6}" fill="none" stroke="#fff" stroke-width="2" stroke-opacity="0.8"/>
    </svg>
  `;
}

function snapWikiSize(size) {
  if (size <= 250) return 250;
  if (size <= 330) return 330;
  if (size <= 500) return 500;
  if (size <= 960) return 960;
  return 1280;
}

function photoTag(d, size = 960, cls = "pc-photo") {
  const im = d._img;
  if (!im || !im.src) return "";
  const step = snapWikiSize(size);
  const src = im.src.replace(/\/\d+px-/, `/${step}px-`);
  const fallback = im.src !== src ? `if(!this.dataset.fb){this.dataset.fb='1';this.src='${esc(im.src)}';}else{this.remove();}` : "this.remove()";
  return `<img class="${cls}" src="${esc(src)}" alt="${esc(d._zh)}" loading="lazy" decoding="async" onerror="${fallback}">`;
}

function photoCredit(d) {
  const im = d._img;
  if (!im) return "";
  const who = im.artist ? esc(im.artist) : "Wikimedia Commons";
  return `<a class="photo-credit" href="${esc(im.page)}" target="_blank" rel="noopener noreferrer">图片：${who}${im.license ? " · " + esc(im.license) : ""}</a>`;
}

function postcardHTML(d, rank, opts = {}) {
  const isCompared = state.compareIds.includes(d.id);
  const compact = opts.compact;
  const g = (window.DEST_GEO && window.DEST_GEO[d.id]) || [];
  const w7 = d._w7 || compute7DayWeather(d.id, dateToDoy(state.travelMonth, state.travelDay), d.coldestNight, d.coldestWater);
  const isWarn = w7.rawCold || w7.rawHot || w7.rawRain;
  return `
    <article class="postcard" data-dest-id="${esc(d.id)}" data-lat="${g[0] != null ? g[0] : ""}" data-lon="${g[1] != null ? g[1] : ""}" data-name="${esc(d._zh)}">
      <div class="pc-scene" onclick="openDestModal('${d.id}')">
        ${buildPostcardSVG(d, { prefix: opts.prefix || "pc" })}
        ${photoTag(d)}
        ${rank ? `<span class="pc-rank">No. ${rank}</span>` : ""}
        <span class="pc-badge${isWarn ? " is-seasonal" : ""}">${esc(w7.badgeText)}</span>
        <span class="pc-score"><b>${d.weightedTotal.toFixed(1)}</b><small>/100</small></span>
      </div>
      <div class="pc-body">
        <p class="pc-meta">${esc(d.region)}</p>
        <h3 class="pc-title" onclick="openDestModal('${d.id}')">${esc(d._zh)}</h3>
        ${d._en ? `<p class="pc-en">${esc(d._en)}</p>` : ""}
        <div class="pc-facts" style="flex-wrap:wrap;gap:6px 12px">
          <span title="出行后7天日均最低~最高气温">🌡️ <b>${w7.low.toFixed(1)}°~${w7.high.toFixed(1)}°C</b></span>
          <span title="出行后7天日均水温 (10%~90%区间: ${w7.waterLow.toFixed(1)}°~${w7.waterHigh.toFixed(1)}°C)">🌊 水 <b>${w7.water.toFixed(1)}°C</b> <small>(${w7.waterLow.toFixed(1)}°~${w7.waterHigh.toFixed(1)}°)</small></span>
          <span title="出行后7天日均晴天比例与下雨概率">☀️ 晴 <b>${Math.round(w7.clear)}%</b> · 🌧️ 雨 <b>${Math.round(w7.rain)}%</b></span>
          ${d._hours != null ? `<span>✈️ 约 <b>${fmtHours(d._hours)}h</b></span>` : ""}
        </div>
        ${compact ? "" : `
          <p class="pc-summary">${esc(d.note || "")}</p>
          <div class="pc-foot">
            <span class="pc-price"><b>$${d.priceMin.toLocaleString()}</b><small>5 晚起</small></span>
            <span class="pc-actions">
              <a class="text-link" href="${d.hotelUrl}" target="_blank" rel="noopener noreferrer">房价 ${icon("external")}</a>
              <button type="button" class="compare-toggle" aria-pressed="${isCompared}" onclick="toggleCompare('${d.id}')">
                ${icon(isCompared ? "check" : "plus")}<span>${isCompared ? "已选" : "对比"}</span>
              </button>
            </span>
          </div>`}
      </div>
    </article>
  `;
}

// ---------------------------------------------------------------------------
// Editor's Note (cover feature)
// ---------------------------------------------------------------------------

function renderCoverFeature() {
  const el = document.getElementById("feature");
  if (!el) return;
  const all = getEnrichedAll();
  const f = COVER_FACTS[state.factIndex % COVER_FACTS.length];
  const dA = all.find(d => d.id === f.idA) || all[0];
  const dB = all.find(d => d.id === f.idB) || all[1];
  if (!dA || !dB) return;

  el.innerHTML = `
    <div class="feature-copy">
      <span class="eyebrow">编辑手记 · ${esc(f.kicker.replace(/^你可能不知道\s*·\s*/, ""))}</span>
      <blockquote class="feature-quote">${esc(f.text)}</blockquote>
      <div class="feature-foot">
        <button type="button" class="btn btn-solid" onclick="comparePair('${dA.id}', '${dB.id}')">
          <span>${esc(f.linkLabel)}</span>${icon("arrowRight")}
        </button>
        <button type="button" class="feature-next" onclick="nextCoverFact()">${icon("refresh")}<span>下一则</span></button>
        <span class="feature-count">${state.factIndex + 1} / ${COVER_FACTS.length}</span>
      </div>
    </div>
    <div class="feature-pair">
      ${postcardHTML(dA, 0, { compact: true, prefix: "fa" })}
      ${postcardHTML(dB, 0, { compact: true, prefix: "fb" })}
      <p class="vs-caption">${esc(f.caption)}</p>
    </div>
  `;
}

window.nextCoverFact = function() {
  state.factIndex = (state.factIndex + 1) % COVER_FACTS.length;
  renderCoverFeature();
};

window.comparePair = function(idA, idB) {
  state.compareIds = [idA, idB];
  renderApp();
  openCompareModal();
};

// ---------------------------------------------------------------------------
// Weather Spark 7-Day Travel Date Planner UI & Controls
// ---------------------------------------------------------------------------

function getQuickDatesList() {
  const td = getDefaultTravelDate();
  return [
    { label: `今日 (${td.month}/${td.day})`, m: td.month, d: td.day },
    { label: "元旦 1/1", m: 1, d: 1 },
    { label: "春节 2/15", m: 2, d: 15 },
    { label: "清明 4/5", m: 4, d: 5 },
    { label: "五一 5/1", m: 5, d: 1 },
    { label: "端午 6/10", m: 6, d: 10 },
    { label: "暑假 7/15", m: 7, d: 15 },
    { label: "八月 8/10", m: 8, d: 10 },
    { label: "国庆 10/1", m: 10, d: 1 },
    { label: "深秋 11/15", m: 11, d: 15 },
    { label: "圣诞 12/25", m: 12, d: 25 }
  ];
}

function populateTravelDateSelects() {
  const mSel = document.getElementById("travel-month");
  const dSel = document.getElementById("travel-day");
  if (!mSel || !dSel) return;

  if (!mSel.options.length) {
    mSel.innerHTML = MONTH_NAMES_ZH.map((name, idx) =>
      `<option value="${idx + 1}">${name}</option>`
    ).join("");
  }
  mSel.value = String(state.travelMonth);

  const maxDay = MONTH_DAYS[state.travelMonth - 1] || 31;
  if (state.travelDay > maxDay) state.travelDay = maxDay;

  dSel.innerHTML = Array.from({ length: maxDay }, (_, i) => i + 1).map(day =>
    `<option value="${day}">${day}日</option>`
  ).join("");
  dSel.value = String(state.travelDay);
}

window.onTravelDateChange = function() {
  const mSel = document.getElementById("travel-month");
  const dSel = document.getElementById("travel-day");
  if (!mSel || !dSel) return;
  const newM = Number(mSel.value) || 1;
  const maxD = MONTH_DAYS[newM - 1] || 31;
  const newD = Math.min(Number(dSel.value) || 1, maxD);
  state.travelMonth = newM;
  state.travelDay = newD;
  populateTravelDateSelects();
  renderApp();
  renderEliminatedSection();
};

window.pickQuickTravelDate = function(m, d) {
  state.travelMonth = Number(m);
  state.travelDay = Number(d);
  populateTravelDateSelects();
  renderApp();
  renderEliminatedSection();
};

window.toggleWeatherFilterMaster = function(checked) {
  state.weatherFilterEnabled = !!checked;
  const el = document.getElementById("wp-enable-filter");
  if (el) el.checked = state.weatherFilterEnabled;
  renderApp();
};

window.onWeatherRuleChange = function() {
  const r = state.weatherRules;
  const fc = document.getElementById("wp-filter-cold");
  const fh = document.getElementById("wp-filter-hot");
  const fr = document.getElementById("wp-filter-rain");
  if (fc) r.filterCold = fc.checked;
  if (fh) r.filterHot = fh.checked;
  if (fr) r.filterRain = fr.checked;

  const mw = document.getElementById("wp-min-water");
  const ml = document.getElementById("wp-min-low");
  const mh = document.getElementById("wp-min-high");
  const xh = document.getElementById("wp-max-high");
  const xw = document.getElementById("wp-max-water");
  const xr = document.getElementById("wp-max-rain");
  const mc = document.getElementById("wp-min-clear");

  if (mw) r.minWater = Number(mw.value);
  if (ml) r.minLow = Number(ml.value);
  if (mh) r.minHigh = Number(mh.value);
  if (xh) r.maxHigh = Number(xh.value);
  if (xw) r.maxWater = Number(xw.value);
  if (xr) r.maxRain = Number(xr.value);
  if (mc) r.minClear = Number(mc.value);

  renderApp();
};

window.resetWeatherThresholds = function() {
  state.weatherFilterEnabled = true;
  state.weatherRules = { ...DEFAULT_WEATHER_RULES };
  syncWeatherRuleInputs();
  renderApp();
};

function syncWeatherRuleInputs() {
  const r = state.weatherRules;
  const master = document.getElementById("wp-enable-filter");
  if (master) master.checked = state.weatherFilterEnabled;

  const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = String(val); };
  const setChk = (id, val) => { const el = document.getElementById(id); if (el) el.checked = !!val; };

  setChk("wp-filter-cold", r.filterCold);
  setChk("wp-filter-hot", r.filterHot);
  setChk("wp-filter-rain", r.filterRain);
  setVal("wp-min-water", r.minWater);
  setVal("wp-min-low", r.minLow);
  setVal("wp-min-high", r.minHigh);
  setVal("wp-max-high", r.maxHigh);
  setVal("wp-max-water", r.maxWater);
  setVal("wp-max-rain", r.maxRain);
  setVal("wp-min-clear", r.minClear);
}

function renderWeatherPlanner(allEnriched) {
  populateTravelDateSelects();
  const win = getTravelWindowMeta();

  const badgeEl = document.getElementById("wp-window-badge");
  if (badgeEl) {
    badgeEl.textContent = `📅 ${win.fullLabel}`;
  }

  const thCol = document.getElementById("th-weather-col");
  if (thCol) {
    thCol.innerHTML = `${esc(win.rangeLabel)} (7天均值)<small>最高最低气温 / 水温 / 晴天 / 降雨</small>`;
  }

  const quickRow = document.getElementById("wp-quick-dates");
  if (quickRow) {
    const qList = getQuickDatesList();
    quickRow.innerHTML = `<span class="wp-quick-lbl">热门出行档期：</span>` + qList.map(q => {
      const active = state.travelMonth === q.m && state.travelDay === q.d;
      return `<button type="button" class="wp-quick-btn" aria-pressed="${active}" onclick="pickQuickTravelDate(${q.m}, ${q.d})">${esc(q.label)}</button>`;
    }).join("");
  }

  const r = state.weatherRules;
  document.getElementById("wp-card-cold")?.classList.toggle("is-off", !state.weatherFilterEnabled || !r.filterCold);
  document.getElementById("wp-card-hot")?.classList.toggle("is-off", !state.weatherFilterEnabled || !r.filterHot);
  document.getElementById("wp-card-rain")?.classList.toggle("is-off", !state.weatherFilterEnabled || !r.filterRain);

  const coldList = allEnriched.filter(d => d._w7.rawCold);
  const hotList = allEnriched.filter(d => d._w7.rawHot);
  const rainList = allEnriched.filter(d => d._w7.rawRain);
  const passList = allEnriched.filter(d => d._w7.passes);

  const coldBadge = document.getElementById("wp-cold-count");
  const hotBadge = document.getElementById("wp-hot-count");
  const rainBadge = document.getElementById("wp-rain-count");

  if (coldBadge) coldBadge.textContent = `${r.filterCold && state.weatherFilterEnabled ? "已筛除" : "不达标"} ${coldList.length} 处`;
  if (hotBadge) hotBadge.textContent = `${r.filterHot && state.weatherFilterEnabled ? "已筛除" : "超上限"} ${hotList.length} 处`;
  if (rainBadge) rainBadge.textContent = `${r.filterRain && state.weatherFilterEnabled ? "已筛除" : "多雨"} ${rainList.length} 处`;

  const sumEl = document.getElementById("wp-filtered-summary");
  if (sumEl) {
    const sampleCold = coldList.slice(0, 3).map(d => `${d._zh}(水${d._w7.water.toFixed(1)}°/低${d._w7.low.toFixed(1)}°)`).join("、");
    const sampleHot = hotList.slice(0, 3).map(d => `${d._zh}(高${d._w7.high.toFixed(1)}°/水${d._w7.water.toFixed(1)}°)`).join("、");
    const sampleRain = rainList.slice(0, 3).map(d => `${d._zh}(雨${Math.round(d._w7.rain)}%)`).join("、");

    const parts = [];
    if (coldList.length) parts.push(`❄️ <strong>不够暖和 ${coldList.length} 处</strong>：${esc(sampleCold)}${coldList.length > 3 ? " 等" : ""}`);
    if (hotList.length) parts.push(`🔥 <strong>过于炎热 ${hotList.length} 处</strong>：${esc(sampleHot)}${hotList.length > 3 ? " 等" : ""}`);
    if (rainList.length) parts.push(`🌧️ <strong>雨水过多 ${rainList.length} 处</strong>：${esc(sampleRain)}${rainList.length > 3 ? " 等" : ""}`);

    const toggleBtn = state.weatherFilterEnabled
      ? `<button type="button" class="text-link" onclick="toggleWeatherFilterMaster(false)">临时查看全部 145 处 (含天气劝退项)</button>`
      : `<button type="button" class="text-link" style="color:var(--coral)" onclick="toggleWeatherFilterMaster(true)">重新开启 7 天天气自动过滤 (当前显示全部 145 处)</button>`;

    sumEl.innerHTML = `
      <div>
        <span><strong>${esc(win.rangeLabel)} 统计：</strong>共 <strong>${passList.length} / 145</strong> 处通过当前天气筛选。</span>
        ${parts.length ? `<span style="margin-left:6px">${parts.join(" ； ")}</span>` : ""}
      </div>
      <div>${toggleBtn}</div>
    `;
  }
}

// ---------------------------------------------------------------------------
// Category & Region Chips
// ---------------------------------------------------------------------------

function renderChipBar() {
  const bar = document.getElementById("chip-bar");
  if (!bar) return;
  const allUnfilteredWeather = getEnrichedAll().filter(d => matchesFilter(d, true, true));
  const allWeatherFiltered = allUnfilteredWeather.filter(d => !state.weatherFilterEnabled || d._w7.passes);

  const win = getTravelWindowMeta();
  const passCount = allUnfilteredWeather.filter(d => d._w7 && !d._w7.rawCold && !d._w7.rawHot && !d._w7.rawRain).length;

  const modeChips = [
    `<button type="button" class="chip" aria-pressed="${state.weatherFilterEnabled && state.categoryFilter === 'all'}" onclick="state.categoryFilter='all';toggleWeatherFilterMaster(true)">✨ ${esc(win.startLabel)}后7天适游<span class="count">${passCount}</span></button>`,
    `<button type="button" class="chip" aria-pressed="${!state.weatherFilterEnabled && state.categoryFilter === 'all'}" onclick="state.categoryFilter='all';toggleWeatherFilterMaster(false)">全部 145 处 (不限天气)<span class="count">${allUnfilteredWeather.length}</span></button>`
  ].join("");

  const poolForRegion = allWeatherFiltered.filter(d => state.categoryFilter === "all" || d.category === state.categoryFilter);
  const regChips = [
    `<button type="button" class="chip" aria-pressed="${state.regionFilter === 'all'}" onclick="setRegionChip('all')">全部海域<span class="count">${poolForRegion.length}</span></button>`
  ].concat(
    REGIONS.map(r => {
      const cnt = poolForRegion.filter(d => d.region === r).length;
      return `<button type="button" class="chip" aria-pressed="${state.regionFilter === r}" onclick="setRegionChip('${r}')">${esc(r)}<span class="count">${cnt}</span></button>`;
    })
  ).join("");

  bar.innerHTML = `${modeChips}<span class="chip-sep" aria-hidden="true"></span>${regChips}`;
}

window.setCategoryChip = function(cat) {
  state.categoryFilter = cat;
  const sel = document.getElementById("filter-category");
  if (sel) sel.value = cat;
  renderApp();
};

window.setRegionChip = function(reg) {
  state.regionFilter = reg;
  const sel = document.getElementById("filter-region");
  if (sel) sel.value = reg;
  renderApp();
};

// ---------------------------------------------------------------------------
// Flight Badges & Tag Buttons
// ---------------------------------------------------------------------------

function renderTravelBadge(dest) {
  if (!state.origin || dest._hours == null) return "";
  return `<div class="t-flights"><span class="flight-code" title="按直线距离 ${Math.round(dest._km).toLocaleString()} km 估算，不含转机">从${esc(state.origin.name)} 约 ${fmtHours(dest._hours)} 小时</span></div>`;
}

function renderTags(rawTags) {
  const tags = cleanTags(rawTags);
  if (!tags.length) return "";
  return `<div class="t-tags">${tags.map(t =>
    `<button type="button" class="tag-btn" data-tag="${esc(t)}" onclick="searchTag(this.dataset.tag)">${esc(t)}</button>`
  ).join("")}</div>`;
}

function renderDimCell(val, max) {
  const pct = Math.min(100, Math.round((val / max) * 100));
  const isHigh = pct >= 92;
  return `
    <div class="dim-cell">
      <span class="dim-val${isHigh ? " is-high" : ""}">${val.toFixed(1)}</span>
      <span class="dim-bar${isHigh ? " is-high" : ""}"><i style="width:${pct}%"></i></span>
    </div>
  `;
}

// ---------------------------------------------------------------------------
// Main Render
// ---------------------------------------------------------------------------

function renderApp() {
  const allEnriched = getEnrichedAll();
  renderWeatherPlanner(allEnriched);

  const data = getProcessedData();

  renderChipBar();

  const totalCountEl = document.getElementById("kpi-total-count");
  const tropicalCountEl = document.getElementById("kpi-tropical-count");
  const seasonalCountEl = document.getElementById("kpi-seasonal-count");
  const avgPriceEl = document.getElementById("kpi-avg-price");
  const topDestEl = document.getElementById("kpi-top-dest");

  if (totalCountEl) totalCountEl.textContent = data.length;
  if (tropicalCountEl) {
    if (data.length) {
      const avgL = (data.reduce((s, d) => s + d._w7.low, 0) / data.length).toFixed(1);
      const avgH = (data.reduce((s, d) => s + d._w7.high, 0) / data.length).toFixed(1);
      tropicalCountEl.innerHTML = `<span class="mono" style="font-size:24px">${avgL}° ~ ${avgH}°C</span>`;
    } else {
      tropicalCountEl.textContent = "—";
    }
  }
  if (seasonalCountEl) {
    if (data.length) {
      const avgW = (data.reduce((s, d) => s + d._w7.water, 0) / data.length).toFixed(1);
      const avgC = Math.round(data.reduce((s, d) => s + d._w7.clear, 0) / data.length);
      seasonalCountEl.innerHTML = `<span class="mono" style="font-size:24px">${avgW}°C</span> <small>· 晴 ${avgC}%</small>`;
    } else {
      seasonalCountEl.textContent = "—";
    }
  }

  if (avgPriceEl) {
    const cheapest = data.length ? [...data].sort((a, b) => a.priceMin - b.priceMin)[0] : null;
    avgPriceEl.innerHTML = cheapest ? `<span class="mono">$${cheapest.priceMin.toLocaleString()}</span> <small>${esc(cheapest._zh)}</small>` : "—";
  }
  if (topDestEl) {
    topDestEl.innerHTML = data.length ? `${esc(data[0]._zh)} <small>${data[0].weightedTotal.toFixed(1)}分</small>` : "无匹配结果";
  }

  const summaryEl = document.getElementById("results-summary");
  if (summaryEl) {
    const win = getTravelWindowMeta();
    const presetName = state.activePreset === "custom" ? "自定义权重" : (WEIGHT_PRESETS[state.activePreset]?.label || "");
    const wMode = state.weatherFilterEnabled ? `已按 ${win.rangeLabel} 自动过滤不适游天气` : `显示全部（未过滤 ${win.rangeLabel} 天气）`;
    summaryEl.textContent = `共 ${data.length} 处 · ${wMode} · ${SORT_LABELS[state.sortBy] || ""} · 权重：${presetName}${state.origin ? ` · 出发地：${state.origin.name}` : ""}`;
  }

  const tableContainer = document.getElementById("table-view-container");
  const cardsContainer = document.getElementById("cards-view-container");

  if (state.viewMode === "table") {
    tableContainer.hidden = false;
    cardsContainer.hidden = true;
    renderTable(data);
  } else {
    tableContainer.hidden = true;
    cardsContainer.hidden = false;
    renderCards(data);
  }

  renderCompareBar();
  renderCoverFeature();
  renderOriginFinder();
  if (window.SharedWidgets && window.SharedWidgets.enhance) window.SharedWidgets.enhance();
}

function emptyStateHTML() {
  return `
    <div class="empty-state">
      <h3>没有匹配当前出行日期与筛选条件的海滨目的地</h3>
      <p>可尝试调整出行日期、放宽未来7天水温/降雨阈值、或点击下方重置。</p>
      <button type="button" class="btn" onclick="resetFilters()">重置全部筛选</button>
    </div>
  `;
}

function renderTable(data) {
  const tbody = document.getElementById("destinations-tbody");
  if (!tbody) return;

  if (data.length === 0) {
    tbody.innerHTML = `<tr><td colspan="13">${emptyStateHTML()}</td></tr>`;
    return;
  }

  tbody.innerHTML = data.map((d, idx) => {
    const rank = idx + 1;
    const isCompared = state.compareIds.includes(d.id);
    const w7 = d._w7;

    const diff = Math.round((d.weightedTotal - d.defaultTotal) * 10) / 10;
    const diffHtml = diff !== 0
      ? `<span class="t-delta ${diff > 0 ? "up" : ""}">${diff > 0 ? "+" : ""}${diff.toFixed(1)}</span>`
      : "";

    const dimCells = Object.entries(DIM_LABELS).map(([k, meta]) =>
      `<td class="num">${renderDimCell(d.scores[k], meta.max)}</td>`
    ).join("");

    return `
      <tr class="${isCompared ? "is-compared" : ""}">
        <td class="num">
          <span class="t-rank ${rank <= 3 ? "is-top" : ""}">${rank}</span>
        </td>
        <td style="min-width:340px;max-width:440px">
          <div class="t-dest-cell">
            <div class="t-thumb" onclick="openDestModal('${d.id}')" title="查看 ${esc(d._zh)} 完整档案与 365 天气候图">
              ${buildPostcardSVG(d, { prefix: "tb" })}
              ${photoTag(d, 330, "t-photo")}
            </div>
            <div class="t-dest-info">
              <div class="t-dest-head">
                <a class="t-title" href="#dest-${d.id}" onclick="event.preventDefault();openDestModal('${d.id}')">${esc(d._zh)}</a>
                ${d._en ? `<span class="t-en">${esc(d._en)}</span>` : ""}
              </div>
              <div class="t-meta">
                <span>${esc(d.region)}</span>
                <span>·</span>
                <span>最佳窗口：${esc(d.bestSeason)}</span>
              </div>
              ${renderTravelBadge(d)}
              ${renderTags(d.tags)}
              <p class="t-note">${esc(d.note || "")}</p>
            </div>
          </div>
        </td>
        <td class="num">
          <div class="t-weather-box">
            <span class="t-w-line" title="出发后7天日均最低气温 ~ 日均最高气温">🌡️ 气温 <b>${w7.low.toFixed(1)}° ~ ${w7.high.toFixed(1)}°C</b></span>
            <span class="t-w-line" title="出发后7天日均水温（括弧内为10%~90%最低~最高水温区间）">🌊 水温 <b>${w7.water.toFixed(1)}°C</b> <small>(${w7.waterLow.toFixed(1)}°~${w7.waterHigh.toFixed(1)}°C)</small></span>
            <span class="t-w-line" title="出发后7天日均晴天比例与下雨概率">☀️ 晴 <b>${Math.round(w7.clear)}%</b> · 🌧️ 雨 <b>${Math.round(w7.rain)}%</b></span>
            <span class="t-w-pill ${w7.badgeClass}">${esc(w7.badgeText)}</span>
          </div>
        </td>
        <td class="num">
          <span class="t-total ${d.weightedTotal >= 90 ? "is-elite" : ""}">${d.weightedTotal.toFixed(1)}</span>
          ${diffHtml}
        </td>
        ${dimCells}
        <td class="right" style="white-space:nowrap">
          <div class="t-price">$${d.priceMin.toLocaleString()}</div>
          <div class="t-price-note" title="${esc(cleanPriceDisplay(d.priceDisplay))}">
            ${d.verified ? '<span class="v-dot" title="已实测核验"></span>' : ""}${esc(cleanPriceDisplay(d.priceDisplay))}
          </div>
          <div class="t-actions">
            <button type="button" class="text-link" style="font-size:12px" onclick="openDestModal('${d.id}')">365天气候与详单</button>
            <a class="text-link" style="font-size:12px" href="${d.hotelUrl}" target="_blank" rel="noopener noreferrer">核验房价 ${icon("external")}</a>
            <button type="button" class="compare-toggle" aria-pressed="${isCompared}" onclick="toggleCompare('${d.id}')">
              ${icon(isCompared ? "check" : "plus")}<span>${isCompared ? "已选" : "对比"}</span>
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join("");
}

function renderCards(data) {
  const container = document.getElementById("cards-view-container");
  if (!container) return;

  if (data.length === 0) {
    container.innerHTML = emptyStateHTML();
    return;
  }

  container.innerHTML = data.map((d, idx) => postcardHTML(d, idx + 1)).join("");
}

// ---------------------------------------------------------------------------
// Eliminated Gatekeepers Section
// ---------------------------------------------------------------------------

function renderEliminatedSection() {
  const tbody = document.getElementById("eliminated-tbody");
  if (!tbody || !window.ELIMINATED_DESTINATIONS) return;
  const startDoy = dateToDoy(state.travelMonth, state.travelDay);

  tbody.innerHTML = window.ELIMINATED_DESTINATIONS.map(d => {
    const parsed = parseDestName(d);
    const w7 = compute7DayWeather(d.id, startDoy, d.coldestNight, d.coldestWater);
    const dimText = Object.entries(DIM_LABELS).map(([k, meta]) => {
      const weak = d.scores[k] / meta.max < 0.6;
      return `<span class="mono" style="${weak ? 'color:var(--coral);font-weight:600' : 'color:var(--ink-2)'}">${meta.short} ${d.scores[k]}</span>`;
    }).join(" · ");

    return `
      <tr>
        <td style="min-width:190px">
          <span class="t-title" style="cursor:default;font-size:15px">${esc(parsed.zh)}</span>
          ${parsed.en ? `<span class="t-en" style="display:block">${esc(parsed.en)}</span>` : ""}
        </td>
        <td class="num" style="white-space:nowrap">
          <div class="t-weather-box">
            <span class="t-w-line">🌡️ <b>${w7.low.toFixed(1)}°~${w7.high.toFixed(1)}°C</b> · 🌊 <b>${w7.water.toFixed(1)}°C</b> <small>(${w7.waterLow.toFixed(1)}°~${w7.waterHigh.toFixed(1)}°)</small></span>
            <span class="t-w-line">☀️ 晴 <b>${Math.round(w7.clear)}%</b> · 🌧️ 雨 <b>${Math.round(w7.rain)}%</b></span>
          </div>
        </td>
        <td class="num"><span class="t-total" style="font-size:24px;color:var(--ink-3)">${d.total.toFixed(1)}</span></td>
        <td style="font-size:12px;min-width:260px">${dimText}</td>
        <td class="mono" style="font-size:12.5px;white-space:nowrap">${esc(cleanPriceDisplay(d.priceDisplay))}</td>
        <td style="font-size:13px;color:var(--ink-2);min-width:280px;line-height:1.8">${esc(d.reason)}</td>
      </tr>
    `;
  }).join("");
}

// ---------------------------------------------------------------------------
// Weight Calibration Sliders
// ---------------------------------------------------------------------------

function renderWeightSliders() {
  const container = document.getElementById("weight-sliders-container");
  if (!container) return;

  container.innerHTML = Object.entries(DIM_LABELS).map(([key, meta]) => {
    const val = state.weights[key];
    return `
      <div class="weight-cell">
        <div class="weight-cell-head">
          <span class="weight-cell-name">${meta.name}</span>
          <span class="weight-cell-max">/${meta.max}</span>
        </div>
        <div class="weight-cell-val">
          <span class="weight-cell-num" data-weight-val="${key}">${val}</span>
          <span class="weight-cell-pct" data-weight-pct="${key}"></span>
        </div>
        <input
          type="range"
          min="0"
          max="50"
          step="5"
          value="${val}"
          data-weight-input="${key}"
          oninput="updateWeight('${key}', this.value)"
          style="--pct:${(val / 50) * 100}%"
          aria-label="${meta.name} 权重"
        />
        <p class="weight-cell-desc">${meta.desc}</p>
      </div>
    `;
  }).join("");

  syncWeightUI();
}

function syncWeightUI() {
  const totalWeight = Object.values(state.weights).reduce((a, b) => a + b, 0);

  Object.entries(DIM_LABELS).forEach(([key]) => {
    const val = state.weights[key];
    const normPct = totalWeight > 0 ? Math.round((val / totalWeight) * 100) : 0;
    const valEl = document.querySelector(`[data-weight-val="${key}"]`);
    const pctEl = document.querySelector(`[data-weight-pct="${key}"]`);
    const inputEl = document.querySelector(`[data-weight-input="${key}"]`);
    if (valEl) valEl.textContent = val;
    if (pctEl) pctEl.textContent = `${normPct}%`;
    if (inputEl) {
      if (Number(inputEl.value) !== val) inputEl.value = val;
      inputEl.style.setProperty("--pct", `${(val / 50) * 100}%`);
    }
  });

  const distBar = document.getElementById("weight-distribution-bar");
  if (distBar) {
    distBar.innerHTML = totalWeight > 0
      ? Object.entries(DIM_LABELS).map(([key, meta], i) => {
          const w = (state.weights[key] / totalWeight) * 100;
          const bg = WEIGHT_COLORS[i % WEIGHT_COLORS.length];
          return w > 0 ? `<div class="weight-dist-seg" style="width:${w}%;background:${bg}" title="${meta.name} ${Math.round(w)}%"></div>` : "";
        }).join("")
      : "";
  }

  const legend = document.getElementById("weight-legend");
  if (legend) {
    legend.innerHTML = Object.entries(DIM_LABELS).map(([key, meta], i) =>
      `<span><i style="background:${WEIGHT_COLORS[i]}"></i>${meta.short} ${totalWeight > 0 ? Math.round((state.weights[key] / totalWeight) * 100) : 0}%</span>`
    ).join("");
  }

  document.querySelectorAll("[data-preset]").forEach(btn => {
    const p = btn.getAttribute("data-preset");
    btn.setAttribute("aria-pressed", String(p === state.activePreset));
  });
}

window.updateWeight = function(key, value) {
  state.weights[key] = Number(value);
  state.activePreset = "custom";
  syncWeightUI();
  renderApp();
};

window.applyPreset = function(presetKey) {
  if (!WEIGHT_PRESETS[presetKey]) return;
  state.weights = { ...WEIGHT_PRESETS[presetKey].weights };
  state.activePreset = presetKey;
  syncWeightUI();
  renderApp();
};

// ---------------------------------------------------------------------------
// Compare Tray & Dialog
// ---------------------------------------------------------------------------

window.toggleCompare = function(id) {
  const idx = state.compareIds.indexOf(id);
  if (idx >= 0) {
    state.compareIds.splice(idx, 1);
  } else {
    if (state.compareIds.length >= 3) state.compareIds.shift();
    state.compareIds.push(id);
  }
  renderApp();
};

window.clearCompare = function() {
  state.compareIds = [];
  renderApp();
};

function renderCompareBar() {
  const bar = document.getElementById("compare-floating-bar");
  const listEl = document.getElementById("compare-selected-pills");
  const headerLbl = document.getElementById("header-compare-label");
  if (headerLbl) headerLbl.textContent = `对比 (${state.compareIds.length})`;
  if (!bar || !listEl) return;

  if (state.compareIds.length === 0) {
    bar.classList.remove("is-visible");
    return;
  }

  bar.classList.add("is-visible");
  const allData = getEnrichedAll();
  const items = state.compareIds.map(id => allData.find(d => d.id === id)).filter(Boolean);

  listEl.innerHTML = items.map(d => `
    <span class="tray-item">
      <span>${esc(d._zh)}</span>
      <button type="button" onclick="toggleCompare('${d.id}')" aria-label="移除">${icon("close")}</button>
    </span>
  `).join("");
}

window.openCompareModal = function() {
  const modal = document.getElementById("compare-modal");
  const content = document.getElementById("compare-modal-body");
  if (!modal || !content) return;

  const allData = getEnrichedAll();
  const items = state.compareIds.map(id => allData.find(d => d.id === id)).filter(Boolean);

  if (items.length === 0) {
    content.innerHTML = `<div class="empty-state"><h3>还没有选择要比较的目的地</h3><p>在榜单中点击「对比」，最多可以选三处放在一起看。</p></div>`;
    modal.classList.add("is-open");
    document.body.style.overflow = "hidden";
    return;
  }

  const strokes = ["#14425f", "#e0674a", "#2b8b92"];
  const fills = ["rgba(20,66,95,0.14)", "rgba(224,103,74,0.14)", "rgba(43,139,146,0.14)"];

  const bestMark = (vals, higherBetter = true) => {
    if (items.length < 2) return vals.map(() => false);
    const target = higherBetter ? Math.max(...vals) : Math.min(...vals);
    return vals.map(v => v === target);
  };

  const tdCell = (html, isBest) =>
    `<td>${html}${isBest ? '<span class="best-mark">★</span>' : ""}</td>`;

  const win = getTravelWindowMeta();
  const weighted = items.map(d => d.weightedTotal);
  const pureBeach = items.map(d => d.pureBeachScore);
  const cpVals = items.map(d => d.cpIndex);
  const prices = items.map(d => d.priceMin);
  const w7Comfort = items.map(d => d._w7.comfortScore);
  const w7Water = items.map(d => d._w7.water);
  const w7Clear = items.map(d => d._w7.clear);
  const w7Rain = items.map(d => d._w7.rain);
  const hasHours = state.origin && items.every(d => d._hours != null);
  const hours = hasHours ? items.map(d => Math.round(d._hours * 10) / 10) : [];

  const presetBar = `
    <div class="compare-preset-bar">
      <span class="compare-preset-lbl">按偏好重算对比：</span>
      ${Object.entries(WEIGHT_PRESETS).map(([k, p]) =>
        `<button type="button" class="chip" aria-pressed="${state.activePreset === k}" onclick="applyPreset('${k}');openCompareModal()">${esc(p.label)}</button>`
      ).join("")}
    </div>
  `;

  content.innerHTML = `
    ${presetBar}
    ${compareSummaryBannerHTML(items)}
    ${advantagesHTML(items, strokes)}
    <div class="compare-layout">
      <div>
        <div class="radar-wrap">${buildMultiRadarSVG(items, strokes, fills)}</div>
        <div class="radar-legend">
          ${items.map((d, i) => `<span><i style="background:${strokes[i]}"></i>${esc(d._zh)} · ${d.weightedTotal.toFixed(1)}</span>`).join("")}
        </div>
      </div>

      <div class="table-wrap">
        <table class="data-table compare-table">
          <thead>
            <tr>
              <th></th>
              ${items.map((d, i) => `<th><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${strokes[i]};margin-right:6px"></span><span style="font-family:var(--serif);font-size:15px;color:var(--ocean-deep)">${esc(d._zh)}</span><small style="font-family:var(--display);font-style:italic;font-size:13px">${esc(d._en)}</small></th>`).join("")}
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>综合得分</td>
              ${bestMark(weighted).map((b, i) => tdCell(`<span class="t-total" style="font-size:24px">${weighted[i].toFixed(1)}</span>`, b)).join("")}
            </tr>
            <tr>
              <td>${esc(win.rangeLabel)} 日均气温</td>
              ${bestMark(w7Comfort).map((b, i) => tdCell(`<strong>${items[i]._w7.low.toFixed(1)}° ~ ${items[i]._w7.high.toFixed(1)}°C</strong> <span class="t-w-pill ${items[i]._w7.badgeClass}" style="margin-left:4px">${esc(items[i]._w7.badgeText)}</span>`, b)).join("")}
            </tr>
            <tr>
              <td>${esc(win.rangeLabel)} 日均水温</td>
              ${bestMark(w7Water).map((b, i) => tdCell(`<strong>${items[i]._w7.water.toFixed(1)}°C</strong> <span style="font-size:11.5px;color:var(--ink-3)">(${items[i]._w7.waterLow.toFixed(1)}°~${items[i]._w7.waterHigh.toFixed(1)}°C)</span>`, b)).join("")}
            </tr>
            <tr>
              <td>${esc(win.rangeLabel)} 晴天比例</td>
              ${bestMark(w7Clear).map((b, i) => tdCell(`☀️ <strong>${Math.round(items[i]._w7.clear)}%</strong>`, b)).join("")}
            </tr>
            <tr>
              <td>${esc(win.rangeLabel)} 下雨概率</td>
              ${bestMark(w7Rain, false).map((b, i) => tdCell(`🌧️ <strong>${Math.round(items[i]._w7.rain)}%</strong>`, b)).join("")}
            </tr>
            <tr>
              <td>纯海滩硬实力 <span style="color:var(--ink-3);font-size:11.5px">/ 50</span></td>
              ${bestMark(pureBeach).map((b, i) => tdCell(`<strong>${pureBeach[i].toFixed(1)}</strong> <span style="font-size:11.5px;color:var(--ink-3)">(海沙+玩水+风浪)</span>`, b)).join("")}
            </tr>
            <tr>
              <td>5 晚参考价</td>
              ${bestMark(prices, false).map((b, i) => tdCell(`<strong style="color:var(--ocean-deep)">$${items[i].priceMin.toLocaleString()}</strong><div style="font-size:11.5px;color:var(--ink-3);margin-top:2px">${esc(cleanPriceDisplay(items[i].priceDisplay))}</div>`, b)).join("")}
            </tr>
            <tr>
              <td>性价比指数</td>
              ${bestMark(cpVals).map((b, i) => tdCell(`${cpVals[i].toFixed(1)}`, b)).join("")}
            </tr>
            ${hasHours ? `
              <tr>
                <td>从${esc(state.origin.name)}出发航时</td>
                ${bestMark(hours, false).map((b, i) => tdCell(`约 <strong>${fmtHours(items[i]._hours)} 小时</strong> <span style="font-size:11.5px;color:var(--ink-3)">(${Math.round(items[i]._km).toLocaleString()} km)</span>`, b)).join("")}
              </tr>
            ` : ""}
            ${Object.entries(DIM_LABELS).map(([k, meta]) => {
              const vals = items.map(d => d.scores[k]);
              return `
                <tr>
                  <td>${meta.name} <span style="color:var(--ink-3);font-size:11.5px">/ ${meta.max}</span></td>
                  ${bestMark(vals).map((b, i) => tdCell(`${vals[i]}`, b)).join("")}
                </tr>
              `;
            }).join("")}
            <tr>
              <td>最佳季节</td>
              ${items.map(d => `<td style="font-size:12.5px">${esc(d.bestSeason)}</td>`).join("")}
            </tr>
            <tr>
              <td>实时房价</td>
              ${items.map(d => `<td><a class="text-link" href="${d.hotelUrl}" target="_blank" rel="noopener noreferrer">Booking ${icon("external")}</a></td>`).join("")}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;

  modal.classList.add("is-open");
  document.body.style.overflow = "hidden";
};

window.closeCompareModal = function() {
  const modal = document.getElementById("compare-modal");
  if (modal) modal.classList.remove("is-open");
  document.body.style.overflow = "";
};

function buildMultiRadarSVG(items, strokes, fills) {
  const size = 380;
  const cx = size / 2;
  const cy = size / 2;
  const radius = 116;
  const keys = Object.keys(MAX_SCORES);
  const n = keys.length;

  const pointFor = (i, ratio) => {
    const a = (Math.PI * 2 * i) / n - Math.PI / 2;
    const r = radius * ratio;
    return [Math.round((cx + r * Math.cos(a)) * 10) / 10, Math.round((cy + r * Math.sin(a)) * 10) / 10];
  };

  const rings = [0.25, 0.5, 0.75, 1.0].map(r =>
    `<circle cx="${cx}" cy="${cy}" r="${radius * r}" fill="${r === 1 ? "#fbf8f2" : "none"}" stroke="#d9cdb8" stroke-width="${r === 1 ? 1.2 : 0.8}" ${r === 1 ? "" : 'stroke-dasharray="2 4"'}/>`
  ).reverse().join("");

  const axes = keys.map((k, i) => {
    const [x, y] = pointFor(i, 1.0);
    const [lx, ly] = pointFor(i, 1.28);
    return `
      <line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="#e3dacb" stroke-width="0.8"/>
      <text x="${lx}" y="${ly}" text-anchor="middle" dominant-baseline="middle" font-size="12" font-family="Noto Sans SC, sans-serif" fill="#4b5a63">${DIM_LABELS[k].name}</text>
    `;
  }).join("");

  const polygons = items.map((d, idx) => {
    const pts = keys.map((k, i) => pointFor(i, Math.min(1, d.scores[k] / MAX_SCORES[k])));
    const dots = pts.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3" fill="#fbf8f2" stroke="${strokes[idx]}" stroke-width="1.8"/>`).join("");
    return `<polygon points="${pts.map(p => p.join(",")).join(" ")}" fill="${fills[idx]}" stroke="${strokes[idx]}" stroke-width="1.8" stroke-linejoin="round"/>${dots}`;
  }).join("");

  return `
    <svg viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="八项得分雷达图">
      ${rings}${axes}${polygons}
    </svg>
  `;
}

// ---------------------------------------------------------------------------
// 365-Day Weather Spark Interactive Chart & Destination Dossier (#dest-modal)
// ---------------------------------------------------------------------------

function buildWeatherSpark365SVG(destId, startDoy) {
  const ws = (window.WEATHER_SPARK_365 || {})[destId];
  if (!ws || !ws.high || ws.high.length !== 365) return "";

  const W = 760, H = 264;
  const padL = 38, padR = 16;
  const plotW = W - padL - padR;

  // Top panel: Temperatures (Air High/Low + Water High/Low/Avg)
  const tTop = 18, tBot = 148, tH = tBot - tTop;
  const allTemps = [...ws.high, ...ws.low, ...ws.waterLow, ...ws.waterHigh];
  const minT = Math.floor(Math.min(...allTemps, 12) / 5) * 5;
  const maxT = Math.ceil(Math.max(...allTemps, 36) / 5) * 5;
  const yTemp = v => Math.round((tBot - ((v - minT) / (maxT - minT)) * tH) * 10) / 10;
  const xDay = i => Math.round((padL + (i / 364) * plotW) * 10) / 10;

  // Bottom panel: Sky Clear % & Rain Probability %
  const pTop = 172, pBot = 236, pH = pBot - pTop;
  const yPct = v => Math.round((pBot - (Math.max(0, Math.min(100, v)) / 100) * pH) * 10) / 10;

  const linePath = (arr, yFn) =>
    arr.map((v, i) => `${i === 0 ? "M" : "L"}${xDay(i)},${yFn(v)}`).join(" ");

  const bandPath = (lowArr, highArr, yFn) => {
    const fwd = lowArr.map((v, i) => `${i === 0 ? "M" : "L"}${xDay(i)},${yFn(v)}`).join(" ");
    const rev = [];
    for (let i = highArr.length - 1; i >= 0; i--) {
      rev.push(`L${xDay(i)},${yFn(highArr[i])}`);
    }
    return `${fwd} ${rev.join(" ")} Z`;
  };

  const areaPath = (arr, yFn, baseY) => {
    const fwd = arr.map((v, i) => `${i === 0 ? "M" : "L"}${xDay(i)},${yFn(v)}`).join(" ");
    return `${fwd} L${xDay(364)},${baseY} L${xDay(0)},${baseY} Z`;
  };

  const tempTicks = [];
  for (let t = minT; t <= maxT; t += 5) {
    const y = yTemp(t);
    tempTicks.push(`
      <line x1="${padL}" y1="${y}" x2="${W - padR}" y2="${y}" stroke="#e6decb" stroke-width="0.8" ${t === 22 || t === 35 ? 'stroke-dasharray="3 3"' : ""}/>
      <text x="${padL - 5}" y="${y + 3.5}" text-anchor="end" font-size="10" fill="#87918f">${t}°</text>
    `);
  }

  const pctTicks = [0, 50, 100].map(p => {
    const y = yPct(p);
    return `
      <line x1="${padL}" y1="${y}" x2="${W - padR}" y2="${y}" stroke="#e6decb" stroke-width="0.8" ${p === 50 ? 'stroke-dasharray="2 3"' : ""}/>
      <text x="${padL - 5}" y="${y + 3.5}" text-anchor="end" font-size="10" fill="#87918f">${p}%</text>
    `;
  }).join("");

  const monthLines = MONTH_OFFSETS.map((off, idx) => {
    const x = xDay(off);
    const midX = xDay(off + Math.floor(MONTH_DAYS[idx] / 2));
    return `
      <line x1="${x}" y1="${tTop}" x2="${x}" y2="${pBot}" stroke="#ece4d5" stroke-width="0.8"/>
      <text x="${midX}" y="${H - 6}" text-anchor="middle" font-size="10.5" fill="#4b5a63">${idx + 1}月</text>
    `;
  }).join("");

  // Selected 7-day travel window highlight
  const winX1 = xDay(startDoy);
  const winW = Math.max(8, (7 / 365) * plotW);
  const winMeta = getTravelWindowMeta();

  return `
    <svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Weather Spark 365天逐日气温、水温、晴天与降雨率曲线" onclick="clickModalWeatherChart(event, '${esc(destId)}', ${padL}, ${plotW}, ${W})">
      <rect x="${padL}" y="${tTop}" width="${plotW}" height="${tH}" fill="#fbf8f2" rx="2"/>
      <rect x="${padL}" y="${pTop}" width="${plotW}" height="${pH}" fill="#fbf8f2" rx="2"/>
      ${monthLines}
      ${tempTicks.join("")}
      ${pctTicks}
      <!-- Water 10th-90th percentile band & daily average water temp -->
      <path d="${bandPath(ws.waterLow, ws.waterHigh, yTemp)}" fill="rgba(43, 139, 146, 0.22)"/>
      <path d="${linePath(ws.water, yTemp)}" fill="none" stroke="#2b8b92" stroke-width="2.2"/>
      <!-- Air High & Low daily averages -->
      <path d="${linePath(ws.high, yTemp)}" fill="none" stroke="#e0674a" stroke-width="2.0"/>
      <path d="${linePath(ws.low, yTemp)}" fill="none" stroke="#14425f" stroke-width="1.7" stroke-dasharray="3 2"/>
      <!-- Clear sky % and Rain probability % -->
      <path d="${areaPath(ws.clear, yPct, pBot)}" fill="rgba(235, 168, 52, 0.16)"/>
      <path d="${linePath(ws.clear, yPct)}" fill="none" stroke="#d9921e" stroke-width="1.8"/>
      <path d="${areaPath(ws.rain, yPct, pBot)}" fill="rgba(52, 112, 168, 0.18)"/>
      <path d="${linePath(ws.rain, yPct)}" fill="none" stroke="#3470a8" stroke-width="1.8"/>
      <!-- 7-day travel window highlight -->
      <rect x="${winX1}" y="${tTop}" width="${winW}" height="${pBot - tTop}" fill="rgba(224, 103, 74, 0.18)" stroke="#e0674a" stroke-width="1.2"/>
      <text x="${Math.min(W - padR - 55, Math.max(padL + 4, winX1))}" y="${tTop - 4}" font-size="10.5" font-weight="600" fill="#e0674a">▼ ${esc(winMeta.rangeLabel)}</text>
      <text x="${padL + 6}" y="${tTop + 13}" font-size="10.5" font-weight="600" fill="#4b5a63">气温与海水温度 (365天逐日曲线 · 点击图表任意位置可切换出行日期)</text>
      <text x="${padL + 6}" y="${pTop + 13}" font-size="10.5" font-weight="600" fill="#4b5a63">晴天比例 vs 下雨概率 (%)</text>
    </svg>
  `;
}

window.clickModalWeatherChart = function(evt, destId, padL, plotW, viewW) {
  const svg = evt.currentTarget;
  if (!svg) return;
  const rect = svg.getBoundingClientRect();
  const relX = ((evt.clientX - rect.left) / rect.width) * viewW;
  const ratio = Math.max(0, Math.min(1, (relX - padL) / plotW));
  const doy = Math.round(ratio * 364);
  const dt = doyToDate(doy);
  state.travelMonth = dt.month;
  state.travelDay = dt.day;
  populateTravelDateSelects();
  renderApp();
  renderEliminatedSection();
  openDestModal(destId);
};

window.openDestModal = function(id) {
  const modal = document.getElementById("dest-modal");
  const body = document.getElementById("dest-modal-body");
  if (!modal || !body) return;

  const all = getProcessedData();
  const fallbackAll = getEnrichedAll();
  const d = all.find(x => x.id === id) || fallbackAll.find(x => x.id === id);
  if (!d) return;

  const rank = all.findIndex(x => x.id === id) + 1;
  const isCompared = state.compareIds.includes(d.id);
  const win = getTravelWindowMeta();
  const w7 = d._w7;

  const travelBlock = state.origin && d._hours != null
    ? `<div class="flight-row"><span>从${esc(state.origin.name)}出发</span><span class="ok">约 ${fmtHours(d._hours)} 小时<br><small style="font-weight:400;color:var(--ink-3)">直线 ${Math.round(d._km).toLocaleString()} km · 不含转机</small></span></div>`
    : `<p style="font-size:13px;color:var(--ink-3)">在「从你的城市出发」里设置出发地后，这里会显示估算飞行时间。</p>`;

  const chartSvg = buildWeatherSpark365SVG(d.id, win.startDoy);

  body.innerHTML = `
    <div class="dossier-hero">
      ${buildPostcardSVG(d, { wide: true, prefix: "dm" })}
      ${photoTag(d, 1280, "dossier-photo")}
      ${photoCredit(d)}
      <button type="button" class="dialog-close" onclick="closeDestModal()" aria-label="关闭">${icon("close")}</button>
    </div>
    <div class="dossier-head">
      <span class="eyebrow">${esc(d.region)} · ${esc(win.rangeLabel)} <span class="t-w-pill ${w7.badgeClass}" style="margin-left:6px">${esc(w7.badgeText)}</span></span>
      <h2 id="dest-modal-title">${esc(d._zh)}${d._en ? `<span>${esc(d._en)}</span>` : ""}</h2>
      <dl class="dossier-stats">
        <div><dt>当前排名</dt><dd>${rank > 0 ? `No. ${rank}` : "天气已筛除"}</dd></div>
        <div><dt>综合得分</dt><dd>${d.weightedTotal.toFixed(1)}</dd></div>
        <div><dt>${esc(win.rangeLabel)} 水温</dt><dd>${w7.water.toFixed(1)}°C</dd></div>
        <div><dt>5 晚参考价</dt><dd>$${d.priceMin.toLocaleString()}</dd></div>
      </dl>
    </div>
    <div class="dialog-body">
      <div class="ws-dossier-section">
        <div class="ws-dossier-head">
          <div>
            <p class="block-h" style="margin-bottom:2px">Weather Spark · 365天逐日气候与出行周天气报告</p>
            <p style="font-size:13px;color:var(--ink-2)">所选出行窗口：<strong>${esc(win.fullLabel)}</strong> ${w7.failReasons.length ? `<span style="color:var(--coral);margin-left:8px">⚠️ 留意：${esc(w7.failReasons.join("、"))}</span>` : `<span style="color:var(--lagoon);margin-left:8px">✓ 符合海滨温暖适泳、防暑与少雨标准</span>`}</p>
          </div>
          ${w7.wsUrl ? `<a class="text-link" style="font-size:12px" href="${esc(w7.wsUrl)}" target="_blank" rel="noopener noreferrer">数据源：Weather Spark (${esc(w7.wsName.split(",")[0])}) ${icon("external")}</a>` : ""}
        </div>
        <dl class="ws-dossier-cards">
          <div class="ws-d-card">
            <dt>日均最低 ~ 最高气温</dt>
            <dd>${w7.low.toFixed(1)}° ~ ${w7.high.toFixed(1)}°C<small>海滨上限阈值 ≤${state.weatherRules.maxHigh}°C · 夜温底线 ≥${state.weatherRules.minLow}°C</small></dd>
          </div>
          <div class="ws-d-card">
            <dt>日均水温 (最低~最高水温)</dt>
            <dd>${w7.water.toFixed(1)}°C<small>10%–90% 区间：${w7.waterLow.toFixed(1)}° ~ ${w7.waterHigh.toFixed(1)}°C</small></dd>
          </div>
          <div class="ws-d-card">
            <dt>7天日均晴天比例</dt>
            <dd>☀️ ${w7.clear.toFixed(1)}%<small>碧空 / 少云晴好天气占比</small></dd>
          </div>
          <div class="ws-d-card">
            <dt>7天日均下雨概率</dt>
            <dd>🌧️ ${w7.rain.toFixed(1)}%<small>有效降水日概率（过滤上限 ≤${state.weatherRules.maxRain}%）</small></dd>
          </div>
        </dl>
        ${chartSvg ? `
          <div class="ws-chart-wrap">${chartSvg}</div>
          <div class="ws-chart-legend">
            <div class="ws-legend-items">
              <span><i style="background:#e0674a"></i>日均最高气温</span>
              <span><i style="background:#14425f"></i>日均最低气温</span>
              <span><i style="background:#2b8b92"></i>日均水温 (含最低~最高水温带)</span>
              <span><i style="background:#d9921e"></i>晴天比例 (%)</span>
              <span><i style="background:#3470a8"></i>下雨概率 (%)</span>
            </div>
            <span>💡 点击上方全年曲线任意月份/日期，可即时切换出行日期</span>
          </div>
        ` : ""}
      </div>

      <div class="dossier-grid">
        <div>
          <p class="block-h">八项得分</p>
          ${Object.entries(DIM_LABELS).map(([k, meta]) => {
            const pct = Math.min(100, Math.round((d.scores[k] / meta.max) * 100));
            return `
              <div class="dim-row">
                <div class="dim-row-head"><span><strong>${meta.name}</strong><small>${meta.desc}</small></span><span>${d.scores[k]} / ${meta.max}</span></div>
                <div class="dim-row-bar"><i style="width:${pct}%"></i></div>
              </div>
            `;
          }).join("")}
        </div>
        <div>
          <p class="block-h">最佳季节参考</p>
          <p style="font-size:14px;color:var(--ink)">${esc(d.bestSeason)} <span style="color:var(--ink-3);font-size:12.5px">（全年最冷月夜温 ${d.coldestNight}°C / 水温 ${d.coldestWater}°C）</span></p>
          <p class="block-h" style="margin-top:24px">路程</p>
          ${travelBlock}
          <p class="dossier-note">${esc(d.note || "")}</p>
          ${renderTags(d.tags)}
          <p style="margin-top:14px;font-size:12.5px;color:var(--ink-3)">房价说明：${esc(cleanPriceDisplay(d.priceDisplay))}</p>
          <div class="dossier-actions">
            <a class="btn btn-solid" href="${d.hotelUrl}" target="_blank" rel="noopener noreferrer">在 Booking 查看实时房价 ${icon("external")}</a>
            <button type="button" class="btn" onclick="toggleCompare('${d.id}');openDestModal('${d.id}')">
              ${icon(isCompared ? "check" : "plus")}<span>${isCompared ? "已加入对比" : "加入对比"}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  `;

  modal.classList.add("is-open");
  document.body.style.overflow = "hidden";
};

window.closeDestModal = function() {
  const modal = document.getElementById("dest-modal");
  if (modal) modal.classList.remove("is-open");
  document.body.style.overflow = "";
};

// ---------------------------------------------------------------------------
// Command Palette (#palette-backdrop)
// ---------------------------------------------------------------------------

window.openPalette = function() {
  const bd = document.getElementById("palette-backdrop");
  const inp = document.getElementById("palette-input");
  if (!bd || !inp) return;
  bd.classList.add("is-open");
  document.body.style.overflow = "hidden";
  inp.value = "";
  renderPaletteResults("");
  setTimeout(() => inp.focus(), 40);
};

window.closePalette = function() {
  const bd = document.getElementById("palette-backdrop");
  if (bd) bd.classList.remove("is-open");
  document.body.style.overflow = "";
};

function renderPaletteResults(q) {
  const box = document.getElementById("palette-results");
  if (!box) return;
  const query = (q || "").trim().toLowerCase();
  const all = getEnrichedAll();
  const matches = query
    ? all.filter(d => `${d.name} ${d._zh} ${d._en} ${d.region} ${(d.tags || []).join(" ")} ${d.note || ""}`.toLowerCase().includes(query)).slice(0, 20)
    : all.slice(0, 12);

  if (!matches.length) {
    box.innerHTML = `<div style="padding:28px;text-align:center;color:var(--ink-3);font-size:13px">未找到匹配的目的地</div>`;
    return;
  }

  box.innerHTML = matches.map(d => `
    <button type="button" class="palette-item" onclick="closePalette();openDestModal('${d.id}')">
      <span class="palette-thumb">${buildPostcardSVG(d, { prefix: "pl" })}${photoTag(d, 250, "palette-photo")}</span>
      <span class="code" style="min-width:34px">${d.weightedTotal.toFixed(1)}</span>
      <span><strong style="font-family:var(--serif);font-weight:500;color:var(--ocean-deep)">${esc(d._zh)}</strong> <span style="font-family:var(--display);font-style:italic;color:var(--ink-3)">${esc(d._en)}</span></span>
      <span class="sub">🌡️${d._w7.low.toFixed(0)}°~${d._w7.high.toFixed(0)}° · 🌊${d._w7.water.toFixed(1)}° · $${d.priceMin.toLocaleString()}</span>
    </button>
  `).join("");
}

// ---------------------------------------------------------------------------
// Theme Toggle
// ---------------------------------------------------------------------------

function currentTheme() {
  return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
}

function syncThemeBtn() {
  const btn = document.getElementById("theme-toggle");
  if (!btn) return;
  const isLight = currentTheme() === "light";
  btn.innerHTML = `${icon(isLight ? "moon" : "bulb")}<span class="label">${isLight ? "关灯" : "开灯"}</span>`;
  btn.title = isLight ? "切换为夜间海图模式" : "切换为日间纸本模式";
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = isLight ? "#f3efe6" : "#0d0c0b";
}

window.toggleTheme = function() {
  const next = currentTheme() === "light" ? "dark" : "light";
  if (next === "light") document.documentElement.setAttribute("data-theme", "light");
  else document.documentElement.removeAttribute("data-theme");
  try { localStorage.setItem("oa-theme", next); } catch (e) {}
  syncThemeBtn();
};

// ---------------------------------------------------------------------------
// Export CSV & Filter Helpers
// ---------------------------------------------------------------------------

window.exportCSV = function() {
  const data = getProcessedData();
  const win = getTravelWindowMeta();
  const headers = [
    "当前排名", "目的地名称", "英文名", "所属区域",
    `${win.rangeLabel}日均最低温(°C)`, `${win.rangeLabel}日均最高温(°C)`,
    `${win.rangeLabel}日均水温(°C)`, `${win.rangeLabel}最低水温(°C)`, `${win.rangeLabel}最高水温(°C)`,
    `${win.rangeLabel}晴天比例(%)`, `${win.rangeLabel}下雨概率(%)`,
    "最佳季节", "加权总分", "默认总分",
    "海沙(25)", "风景(15)", "玩水(15)", "风浪(10)", "酒店(10)", "餐饮(10)", "陆地(10)", "省心(5)",
    "5晚4★海景最低价(USD)", "房价说明", "亮点与避坑备注",
    state.origin ? `从${state.origin.name}估算飞行(小时)` : "估算飞行(小时)"
  ];

  const rows = data.map((d, idx) => [
    idx + 1,
    `"${d._zh.replace(/"/g, '""')}"`,
    `"${d._en.replace(/"/g, '""')}"`,
    `"${d.region}"`,
    d._w7.low.toFixed(1),
    d._w7.high.toFixed(1),
    d._w7.water.toFixed(1),
    d._w7.waterLow.toFixed(1),
    d._w7.waterHigh.toFixed(1),
    d._w7.clear.toFixed(1),
    d._w7.rain.toFixed(1),
    `"${d.bestSeason.replace(/"/g, '""')}"`,
    d.weightedTotal.toFixed(1),
    d.defaultTotal.toFixed(1),
    d.scores.seaSand,
    d.scores.scenery,
    d.scores.waterPlay,
    d.scores.calmness,
    d.scores.hotel,
    d.scores.dining,
    d.scores.land,
    d.scores.safety,
    d.priceMin,
    `"${cleanPriceDisplay(d.priceDisplay).replace(/"/g, '""')}"`,
    `"${(d.note || "").replace(/"/g, '""')}"`,
    d._hours != null ? fmtHours(d._hours) : ""
  ]);

  const csvContent = "\uFEFF" + [headers.join(","), ...rows.map(r => r.join(","))].join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `oceanic_atlas_145_${state.travelMonth}_${state.travelDay}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

window.resetFilters = function() {
  state.categoryFilter = "all";
  state.maxHours = 0;
  state.regionFilter = "all";
  state.maxPrice = 7000;
  state.minWaterTemp = 0;
  state.verifiedOnly = false;
  state.searchQuery = "";
  state.sortBy = "score-desc";
  state.weatherFilterEnabled = true;
  state.weatherRules = { ...DEFAULT_WEATHER_RULES };
  syncWeatherRuleInputs();

  document.getElementById("filter-category").value = "all";
  const hrs = document.getElementById("filter-hours");
  if (hrs) hrs.value = "0";
  document.getElementById("filter-region").value = "all";
  document.getElementById("filter-price").value = 7000;
  updatePriceSliderUI();
  const wt = document.getElementById("filter-water-temp");
  if (wt) wt.value = "0";
  document.getElementById("filter-verified").checked = false;
  document.getElementById("filter-search").value = "";
  updateSearchClearBtn();
  document.getElementById("filter-sort").value = "score-desc";

  applyPreset("default");
};

function updatePriceSliderUI() {
  const input = document.getElementById("filter-price");
  const label = document.getElementById("price-slider-label");
  if (!input) return;
  const min = Number(input.min), max = Number(input.max), val = Number(input.value);
  input.style.setProperty("--pct", `${((val - min) / (max - min)) * 100}%`);
  if (label) {
    label.textContent = val >= 7000 ? "不限" : `≤ $${val.toLocaleString()}`;
  }
}

function updateSearchClearBtn() {
  const btn = document.getElementById("filter-search-clear");
  if (btn) btn.hidden = !state.searchQuery;
}

window.searchTag = function(tag) {
  const input = document.getElementById("filter-search");
  state.searchQuery = state.searchQuery === tag ? "" : tag;
  if (input) input.value = state.searchQuery;
  updateSearchClearBtn();
  renderApp();
};

window.clearSearch = function() {
  state.searchQuery = "";
  const input = document.getElementById("filter-search");
  if (input) { input.value = ""; input.focus(); }
  updateSearchClearBtn();
  renderApp();
};


function setViewMode(mode) {
  state.viewMode = mode;
  document.getElementById("btn-view-table")?.setAttribute("aria-pressed", String(mode === "table"));
  document.getElementById("btn-view-cards")?.setAttribute("aria-pressed", String(mode === "cards"));
  renderApp();
}

// ---------------------------------------------------------------------------
// "从你的城市出发" — origin finder (pure client-side, no AI / no live flight API)
// ---------------------------------------------------------------------------

const DISTANCE_BANDS = [
  { min: 0, max: 5, title: "短途周游", sub: "5 小时以内 · 周末/小长假" },
  { min: 5, max: 9, title: "中程度假", sub: "5 – 9 小时 · 一周舒适圈" },
  { min: 9, max: 14, title: "远行大洋", sub: "9 – 14 小时 · 跨洲海岛" },
  { min: 14, max: 99, title: "跨洋朝圣", sub: "14 小时以上 · 终极泻湖" }
];

const QUICK_ORIGINS = ["PVG", "PEK", "CAN", "TFU", "HKG", "SIN", "NRT", "LHR", "FRA", "JFK", "LAX", "SYD"];

window.setOriginMode = function(mode) {
  state.originMode = mode;
  renderOriginFinder();
};

function setOrigin(o) {
  state.origin = o;
  saveOrigin(o);
  const input = document.getElementById("origin-input");
  if (input) input.value = o ? o.name : "";
  hideOriginSuggest();
  const hrs = document.getElementById("filter-hours");
  if (hrs) hrs.disabled = !o;
  const nearOpt = document.querySelector('#filter-sort option[value="near-asc"]');
  if (nearOpt) nearOpt.disabled = !o;
  renderApp();
}

window.pickOrigin = function(code) {
  const c = (window.ORIGIN_CITIES || []).find(x => x[2] === code);
  if (c) setOrigin(cityToOrigin(c));
};

window.clearOrigin = function() {
  try { localStorage.removeItem("oa-origin"); } catch (e) {}
  state.origin = null;
  if (state.sortBy === "near-asc") {
    state.sortBy = "score-desc";
    const sel = document.getElementById("filter-sort");
    if (sel) sel.value = "score-desc";
  }
  state.maxHours = 0;
  const hrs = document.getElementById("filter-hours");
  if (hrs) { hrs.value = "0"; hrs.disabled = true; }
  const input = document.getElementById("origin-input");
  if (input) input.value = "";
  renderApp();
};

window.locateMe = function() {
  const btn = document.getElementById("origin-locate");
  if (!navigator.geolocation) return;
  if (btn) btn.textContent = "定位中…";
  navigator.geolocation.getCurrentPosition(pos => {
    const { latitude: lat, longitude: lon } = pos.coords;
    let nearest = null, best = Infinity;
    (window.ORIGIN_CITIES || []).forEach(c => {
      const km = haversineKm(lat, lon, c[3], c[4]);
      if (km < best) { best = km; nearest = c; }
    });
    const name = nearest && best < 150 ? nearest[0] : "我的位置";
    setOrigin({ name, en: nearest ? nearest[1] : "", code: best < 150 && nearest ? nearest[2] : "", lat, lon });
    if (btn) btn.innerHTML = `${icon("pin")}<span>使用我的位置</span>`;
  }, () => {
    if (btn) btn.innerHTML = `${icon("pin")}<span>无法获取位置</span>`;
  }, { timeout: 8000, maximumAge: 600000 });
};

function hideOriginSuggest() {
  const box = document.getElementById("origin-suggest");
  if (box) box.hidden = true;
}

function renderOriginSuggest(q) {
  const box = document.getElementById("origin-suggest");
  if (!box) return;
  const list = findCities(q);
  if (!list.length) {
    box.hidden = !q.trim();
    box.innerHTML = q.trim() ? `<div class="origin-suggest-empty">暂未收录这座城市，试试附近的大城市或机场代码</div>` : "";
    return;
  }
  box.hidden = false;
  box.innerHTML = list.map(c =>
    `<button type="button" onmousedown="event.preventDefault()" onclick="pickOrigin('${c[2]}')"><strong>${esc(c[0])}</strong><span>${esc(c[1])}</span><em>${c[2]}</em></button>`
  ).join("");
}

function renderOriginFinder() {
  const quick = document.getElementById("origin-quick");
  const out = document.getElementById("origin-results");
  if (!quick || !out) return;

  const win = getTravelWindowMeta();
  const cities = window.ORIGIN_CITIES || [];
  const modeChips = [
    { k: "weather", label: `只看 ${win.rangeLabel} 天气适游` },
    { k: "all", label: "全部 145 处 (不限天气)" },
    { k: "budget", label: "适游且 5晚房价 ≤ $1,200" }
  ].map(m =>
    `<button type="button" class="chip" aria-pressed="${state.originMode === m.k}" onclick="setOriginMode('${m.k}')">${esc(m.label)}</button>`
  ).join("");

  quick.innerHTML = QUICK_ORIGINS.map(code => {
    const c = cities.find(x => x[2] === code);
    if (!c) return "";
    const on = state.origin && state.origin.code === code;
    return `<button type="button" class="chip" aria-pressed="${!!on}" onclick="pickOrigin('${code}')">${esc(c[0])}</button>`;
  }).join("")
    + `<span class="chip-sep" aria-hidden="true"></span>`
    + modeChips
    + (state.origin ? `<button type="button" class="reset-btn" onclick="clearOrigin()">清除出发地</button>` : "");

  const input = document.getElementById("origin-input");
  if (input && document.activeElement !== input) input.value = state.origin ? state.origin.name : "";

  if (!state.origin) {
    out.innerHTML = `<div class="origin-empty">选择或输入你的出发城市，我们会按估算飞行时间与所选出行日期的未来7天天气，把近处与远方最值得去的海岸分组列出来。</div>`;
    return;
  }

  const all = getEnrichedAll().filter(d => {
    if (d._hours == null) return false;
    if (state.originMode === "weather" && (d._w7.rawCold || d._w7.rawHot || d._w7.rawRain)) return false;
    if (state.originMode === "budget" && ((d._w7.rawCold || d._w7.rawHot || d._w7.rawRain) || d.priceMin > 1200)) return false;
    return true;
  });
  out.innerHTML = DISTANCE_BANDS.map(b => {
    const picks = all
      .filter(d => d._hours >= b.min && d._hours < b.max)
      .sort((x, y) => y.weightedTotal - x.weightedTotal)
      .slice(0, 4);
    return `
      <div class="band">
        <div class="band-head"><h3>${b.title}</h3><span>${b.sub}</span></div>
        ${picks.length ? picks.map((d, i) => {
          const w7 = d._w7;
          return `
          <button type="button" class="band-item" onclick="openDestModal('${d.id}')">
            <span class="band-thumb">
              ${buildPostcardSVG(d, { prefix: "bd" })}
              ${photoTag(d, 330, "band-photo")}
            </span>
            <span class="band-text">
              <strong>${esc(d._zh)}</strong>
              <small>${esc(d.region)} · <b>${d.weightedTotal.toFixed(1)}分</b> · $${d.priceMin.toLocaleString()} 起</small>
              <em class="band-reason">🌡️ ${w7.low.toFixed(0)}°~${w7.high.toFixed(0)}°C · 🌊 水${w7.water.toFixed(1)}°C · ☀️晴${Math.round(w7.clear)}% · 🌧️雨${Math.round(w7.rain)}%</em>
            </span>
            <span class="band-hours">${fmtHours(d._hours)}<small>h</small></span>
          </button>
        `;}).join("") : `<p class="band-none">该航程内暂无符合当前出行周天气标准的海岸。</p>`}
      </div>
    `;
  }).join("");
}

window.sortByNearest = function() {
  if (!state.origin) return;
  state.sortBy = "near-asc";
  const sel = document.getElementById("filter-sort");
  if (sel) sel.value = "near-asc";
  renderApp();
  document.getElementById("index")?.scrollIntoView({ behavior: "smooth" });
};

// ---------------------------------------------------------------------------
// Compare: rule-based + profile-enriched synthesis — computed live from each
// destination's 8-dim scores, 7-day travel weather, price, origin distance & note.
// ---------------------------------------------------------------------------

const DIM_KEYWORDS = {
  seaSand:  /白沙|果冻|松石|潟湖|泻湖|能见度|水清|硅沙|粉红沙|蓝洞|玻璃海/,
  scenery:  /火山|花岗岩|悬崖|海蚀|航拍|瀑布|山海|日落|奇观|沙丘/,
  waterPlay:/浮潜|深潜|珊瑚|鲸鲨|魔鬼鱼|海龟|儒艮|跳岛|冲浪|海豚|蓝鲸|沙丁鱼/,
  calmness: /外堡礁|平浪|浅滩|泻湖|平静|内海|亲子|泳池/,
  hotel:    /水屋|顶奢|一岛一酒店|全包|别墅|度假村|高星|五星|六星/,
  dining:   /美食|米其林|海鲜|夜市|法餐|餐厅|酒吧|料理/,
  land:     /古镇|古堡|古城|雨林|金字塔|遗迹|动物|国家公园|博物馆|火山徒步/,
  safety:   /免签|治安|省心|零时差|直达|成熟/
};

function extractDimSnippet(d, dimKey) {
  const re = DIM_KEYWORDS[dimKey];
  if (!re) return "";
  const clauses = `${(cleanTags(d.tags)).join("，")}，${d.note || ""}`
    .split(/[，。；！!]+/)
    .map(s => s.trim())
    .filter(Boolean);
  const hit = clauses.find(c => re.test(c) && !/⚠️|偏弱|普通|一般|禁泳/.test(c));
  return hit ? `（${hit}）` : "";
}

function extractCaveatsFromNote(d) {
  const out = [];
  (d.tags || []).forEach(t => {
    if (t.includes("⚠️")) out.push(t.replace(/^⚠️\s*/, "").trim());
  });
  const clauses = String(d.note || "").split(/[，。；！!]+/).map(s => s.trim()).filter(Boolean);
  clauses.forEach(c => {
    if (/^(唯|但|不过|缺点|注意|仅因)|禁泳|浪大|水体普通|水质中等/.test(c)) {
      out.push(c.replace(/^(唯|但|不过)\s*/, ""));
    }
  });
  return [...new Set(out)].slice(0, 2);
}

function buildAdvantages(items) {
  const win = getTravelWindowMeta();
  return items.map(a => {
    const others = items.filter(x => x !== a);
    const pros = [];
    const cons = [];
    const nameOf = list => list.map(x => x._zh).join("、");

    Object.entries(DIM_LABELS).forEach(([k, meta]) => {
      const otherBest = Math.max(...others.map(o => o.scores[k]));
      const otherWorst = Math.min(...others.map(o => o.scores[k]));
      const diff = a.scores[k] - otherBest;
      const snippet = extractDimSnippet(a, k);
      if (diff >= Math.max(0.5, meta.max * 0.06)) {
        pros.push({
          w: (diff / meta.max) * (state.weights[k] || 0.1) * 4 + 2,
          dim: meta.name,
          title: `${meta.name}全场最佳 (+${diff.toFixed(1)})`,
          detail: `${a.scores[k]} vs ${otherBest} / ${meta.max}${snippet || ` · ${meta.desc}`}`
        });
      } else if (diff === 0 && a.scores[k] > otherWorst && a.scores[k] >= meta.max * 0.85) {
        pros.push({
          w: ((a.scores[k] - otherWorst) / meta.max) * (state.weights[k] || 0.1) * 2.5,
          dim: meta.name,
          title: `${meta.name}并列第一 (${a.scores[k]}/${meta.max})`,
          detail: `与榜首同分，领先${nameOf(others.filter(o => o.scores[k] < a.scores[k]))}${snippet || ` · ${meta.desc}`}`
        });
      } else if (others.length >= 2 && a.scores[k] - otherWorst >= meta.max * 0.16 && a.scores[k] >= meta.max * 0.85) {
        const weaker = others.filter(o => a.scores[k] - o.scores[k] >= meta.max * 0.12);
        pros.push({
          w: ((a.scores[k] - otherWorst) / meta.max) * (state.weights[k] || 0.1) * 1.8,
          dim: meta.name,
          title: `${meta.name}高分梯队 (${a.scores[k]}/${meta.max})`,
          detail: `明显优于${nameOf(weaker)}${snippet || ` · ${meta.desc}`}`
        });
      }
      const lag = otherWorst - a.scores[k];
      if (lag >= Math.max(1, meta.max * 0.1)) {
        cons.push({ w: lag / meta.max, text: `${meta.name}相对偏弱（${a.scores[k]}/${meta.max}）` });
      }
    });

    const clearGap = a._w7.clear - Math.max(...others.map(o => o._w7.clear));
    if (clearGap >= 10) {
      pros.push({ w: 14.5, title: `${win.rangeLabel} 阳光最充足`, detail: `7天日均晴天比例 ${Math.round(a._w7.clear)}%，比对手高 ${Math.round(clearGap)}%` });
    }
    const rainGap = Math.min(...others.map(o => o._w7.rain)) - a._w7.rain;
    if (rainGap >= 10) {
      pros.push({ w: 14, title: `${win.rangeLabel} 降雨最少`, detail: `7天日均下雨概率仅 ${Math.round(a._w7.rain)}%，比对手低 ${Math.round(rainGap)}%` });
    }
    const waterGap = a._w7.water - Math.max(...others.map(o => o._w7.water));
    if (waterGap >= 1.2 && a._w7.water <= 31.0) {
      pros.push({ w: 13.5, title: `${win.rangeLabel} 海水更温暖`, detail: `7天日均水温 ${a._w7.water.toFixed(1)}°C (${a._w7.waterLow.toFixed(1)}°~${a._w7.waterHigh.toFixed(1)}°C)` });
    }
    if (a._w7.failReasons.length) {
      cons.push({ w: 0.9, text: `${win.rangeLabel} 天气留意：${a._w7.failReasons.join("、")}` });
    }

    const cheapestOther = Math.min(...others.map(o => o.priceMin));
    const priciestOther = Math.max(...others.map(o => o.priceMin));
    const priciestObj = others.find(o => o.priceMin === priciestOther);
    if (a.priceMin <= cheapestOther * 0.8) {
      const save = cheapestOther - a.priceMin;
      pros.push({ w: 13, title: "酒店预算更友好", detail: `5 晚 4★ 海景约 $${a.priceMin.toLocaleString()}，比次低价再省 $${save.toLocaleString()}（-${Math.round((save / cheapestOther) * 100)}%）` });
    } else if (priciestObj && a.priceMin <= priciestOther * 0.45 && a.weightedTotal >= priciestObj.weightedTotal - 3.5) {
      const save = priciestOther - a.priceMin;
      pros.push({ w: 13.5, title: "顶配体验甜点价", detail: `总分迫近${priciestObj._zh}（${a.weightedTotal.toFixed(1)} vs ${priciestObj.weightedTotal.toFixed(1)}），5 晚房价却立省 $${save.toLocaleString()}` });
    }
    if (a.priceMin >= priciestOther * 1.5) {
      cons.push({ w: 0.6, text: `住宿成本显著更高（5 晚 $${a.priceMin.toLocaleString()} 起）` });
    }

    if (state.origin && a._hours != null && others.every(o => o._hours != null)) {
      const nearestOther = Math.min(...others.map(o => o._hours));
      if (a._hours <= nearestOther - 1.5) {
        pros.push({ w: 12, title: "飞行路程更近", detail: `从${state.origin.name}出发约 ${fmtHours(a._hours)}h，少飞约 ${fmtHours(nearestOther - a._hours)} 小时` });
      }
    }

    extractCaveatsFromNote(a).forEach(cv => {
      if (!cons.some(c => c.text.includes(cv))) {
        cons.push({ w: 0.5, text: cv });
      }
    });

    pros.sort((x, y) => y.w - x.w);
    cons.sort((x, y) => y.w - x.w);
    const dimWins = pros.filter(p => p.dim).slice(0, 2).map(p => p.dim);
    return {
      d: a,
      pros: pros.slice(0, 4),
      cons: cons.slice(0, 3).map(c => c.text),
      tags: cleanTags(a.tags).filter(t => !t.includes("⚠️")).slice(0, 4),
      verdict: dimWins.length
        ? `更看重${dimWins.join("与")}，选它`
        : (pros[0] ? `主打「${pros[0].title}」，选它` : "各项指标均衡，按海域与眼缘决定")
    };
  });
}

function compareSummaryBannerHTML(items) {
  if (items.length < 2) return "";
  const win = getTravelWindowMeta();
  const byScore = [...items].sort((a, b) => b.weightedTotal - a.weightedTotal);
  const byWeather = [...items].sort((a, b) => b._w7.comfortScore - a._w7.comfortScore);
  const byPrice = [...items].sort((a, b) => a.priceMin - b.priceMin);
  const byWater = [...items].sort((a, b) => b._w7.water - a._w7.water);
  const hasOrigin = state.origin && items.every(d => d._hours != null);
  const byNear = hasOrigin ? [...items].sort((a, b) => a._hours - b._hours) : null;

  const pills = [
    `<span>🏆 <strong>当前偏好最高分：</strong>${esc(byScore[0]._zh)}（${byScore[0].weightedTotal.toFixed(1)}分）</span>`,
    `<span>☀️ <strong>${esc(win.rangeLabel)}天气最佳：</strong>${esc(byWeather[0]._zh)}（晴 ${Math.round(byWeather[0]._w7.clear)}% · 雨 ${Math.round(byWeather[0]._w7.rain)}%）</span>`,
    `<span>🌊 <strong>${esc(win.rangeLabel)}水温最高：</strong>${esc(byWater[0]._zh)}（${byWater[0]._w7.water.toFixed(1)}°C）</span>`,
    `<span>💰 <strong>5晚房价最省：</strong>${esc(byPrice[0]._zh)}（$${byPrice[0].priceMin.toLocaleString()}）</span>`
  ];
  if (byNear) {
    pills.push(`<span>✈️ <strong>离${esc(state.origin.name)}最近：</strong>${esc(byNear[0]._zh)}（约 ${fmtHours(byNear[0]._hours)}h）</span>`);
  }
  return `<div class="compare-summary-banner">${pills.join("")}</div>`;
}

function advantagesHTML(items, strokes) {
  if (items.length < 2) return "";
  const adv = buildAdvantages(items);
  return `
    <div class="adv-grid" style="grid-template-columns:repeat(${items.length}, minmax(0, 1fr))">
      ${adv.map((x, i) => `
        <section class="adv-col" style="--c:${strokes[i]}">
          <div class="adv-hero" onclick="closeCompareModal();openDestModal('${x.d.id}')">
            ${buildPostcardSVG(x.d, { prefix: "av" })}
            ${photoTag(x.d, 500, "adv-photo")}
            <span class="adv-score">${x.d.weightedTotal.toFixed(1)}<small>分</small></span>
          </div>
          <div class="adv-body">
            <p class="adv-verdict">${esc(x.verdict)}</p>
            <h3>${esc(x.d._zh)} <small>${esc(x.d.region)}</small></h3>
            ${x.pros.length ? `<ul class="adv-pros">${x.pros.map(p => `<li><strong>${esc(p.title)}</strong><span>${esc(p.detail)}</span></li>`).join("")}</ul>`
              : `<p class="adv-none">单项得分与对手接近，胜在综合均衡度。</p>`}
            <div class="adv-detail">
              <span class="adv-detail-label">海岛详单介绍</span>
              <p>${esc(x.d.note || "")}</p>
            </div>
            ${x.tags.length ? `<p class="adv-tags">${x.tags.map(t => `<span>${esc(t)}</span>`).join("")}</p>` : ""}
            ${x.cons.length ? `<p class="adv-cons"><strong>行前留意：</strong>${x.cons.map(esc).join("；")}</p>` : ""}
          </div>
        </section>
      `).join("")}
    </div>
  `;
}

// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
  // Hydrate static [data-brand] and [data-icon] placeholders
  document.querySelectorAll("[data-brand]").forEach(el => { el.innerHTML = BRAND_MARK; });
  document.querySelectorAll("[data-icon]").forEach(el => { el.innerHTML = icon(el.getAttribute("data-icon")); });

  const params = new URLSearchParams(window.location.search);
  const qSearch = params.get("q");
  if (qSearch) {
    state.searchQuery = qSearch;
    const si = document.getElementById("filter-search");
    if (si) si.value = qSearch;
    updateSearchClearBtn();
  }
  const qView = params.get("view");
  if (qView === "cards" || qView === "table") {
    state.viewMode = qView;
  }
  const qDate = params.get("date");
  if (qDate && /^\d{1,2}-\d{1,2}$/.test(qDate)) {
    const [qm, qd] = qDate.split("-").map(Number);
    if (qm >= 1 && qm <= 12 && qd >= 1 && qd <= 31) {
      state.travelMonth = qm;
      state.travelDay = Math.min(qd, MONTH_DAYS[qm - 1]);
    }
  }
  syncWeatherRuleInputs();

  const qFrom = params.get("from");
  if (qFrom) {
    const c = (window.ORIGIN_CITIES || []).find(x => x[2] === qFrom.toUpperCase() || x[0] === qFrom || x[1].toLowerCase() === qFrom.toLowerCase());
    if (c) state.origin = cityToOrigin(c);
  }
  if (!state.origin) {
    const g = guessOriginFromTimeZone();
    if (g) state.origin = g;
  }
  const hrsSel = document.getElementById("filter-hours");
  if (hrsSel) hrsSel.disabled = !state.origin;
  const nearOpt = document.querySelector('#filter-sort option[value="near-asc"]');
  if (nearOpt) nearOpt.disabled = !state.origin;

  const originInput = document.getElementById("origin-input");
  if (originInput) {
    originInput.addEventListener("input", e => renderOriginSuggest(e.target.value));
    originInput.addEventListener("focus", e => { e.target.select(); renderOriginSuggest(e.target.value); });
    originInput.addEventListener("blur", () => setTimeout(hideOriginSuggest, 120));
    originInput.addEventListener("keydown", e => {
      if (e.key === "Enter") {
        const first = findCities(e.target.value)[0];
        if (first) { pickOrigin(first[2]); e.target.blur(); }
      }
    });
  }
  const loc = document.getElementById("origin-locate");
  if (loc) loc.innerHTML = `${icon("pin")}<span>使用我的位置</span>`;

  syncThemeBtn();
  renderWeightSliders();
  renderEliminatedSection();
  updatePriceSliderUI();
  setViewMode(state.viewMode);

  if (params.get("compare") === "1") {
    openCompareModal();
  } else if (params.get("dest")) {
    openDestModal(params.get("dest"));
  }

  // Pointer-following radial light pool on the cover
  const cover = document.getElementById("cover");
  if (cover) {
    cover.addEventListener("pointermove", e => {
      const r = cover.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 100;
      const y = ((e.clientY - r.top) / r.height) * 100;
      cover.style.setProperty("--mx", `${x.toFixed(1)}%`);
      cover.style.setProperty("--my", `${y.toFixed(1)}%`);
    });
  }

  document.getElementById("filter-hours")?.addEventListener("change", e => {
    state.maxHours = Number(e.target.value);
    renderApp();
  });

  document.getElementById("filter-price")?.addEventListener("input", e => {
    state.maxPrice = Number(e.target.value);
    updatePriceSliderUI();
    renderApp();
  });

  document.getElementById("filter-water-temp")?.addEventListener("change", e => {
    state.minWaterTemp = Number(e.target.value);
    renderApp();
  });

  document.getElementById("filter-verified")?.addEventListener("change", e => {
    state.verifiedOnly = e.target.checked;
    renderApp();
  });

  document.getElementById("filter-search")?.addEventListener("input", e => {
    state.searchQuery = e.target.value;
    updateSearchClearBtn();
    renderApp();
  });

  document.getElementById("filter-sort")?.addEventListener("change", e => {
    state.sortBy = e.target.value;
    renderApp();
  });

  document.getElementById("btn-view-table")?.addEventListener("click", () => setViewMode("table"));
  document.getElementById("btn-view-cards")?.addEventListener("click", () => setViewMode("cards"));

  document.getElementById("palette-input")?.addEventListener("input", e => {
    renderPaletteResults(e.target.value);
  });

  // Global keyboard shortcuts
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      closePalette();
      closeCompareModal();
      closeDestModal();
      return;
    }
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      openPalette();
      return;
    }
    if (/^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement?.tagName)) return;
    if (e.key === "/") {
      e.preventDefault();
      openPalette();
    }
  });
});

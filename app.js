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
  "price-asc": "5晚房价 ↑",
  "cp-desc": "性价比指数 ↓",
  "beach-desc": "纯海滩硬实力 ↓",
  "water-desc": "最冷月水温 ↓",
  "night-desc": "最冷月夜温 ↓",
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
    idA: "oman-salalah",
    idB: "seychelles-praslin-ladigue",
    fig: "WINTER FLIGHT · FRA 6H30M NONSTOP",
    caption: "法兰克福冬春避寒航线 · 阿曼 vs 塞舌尔",
    kicker: "你可能不知道 · 欧洲冬春直飞",
    text: "从法兰克福直飞避寒，与其去冬春东北信风狂浪禁泳、满目荒漠的佛得角（71.5分），不如直飞 6.5 小时抵达阿曼萨拉拉或马斯喀特：最冷月夜温 18.8°C、水温 23.5°C，治安与海岸风景全面胜出。",
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
    idB: "okinawa-naha-kerama",
    fig: "EAST ASIA HUB · SUB-5H NONSTOP",
    caption: "沙巴亚庇 ($976) vs 冲绳那霸与庆良间 ($1,053)",
    kicker: "你可能不知道 · 东亚短途直飞",
    text: "从上海或香港出发 5 小时航程内，沙巴亚庇双人机票加 5 晚 4★ 海景含早实测仅 $976（全年 27.5°C 暖水）；而 2 小时直达的冲绳那霸乘快船 35 分钟即可进入庆良间群岛的世界级果冻海。",
    linkLabel: "对比沙巴亚庇与冲绳庆良间"
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

// Application State
const state = {
  weights: { ...WEIGHT_PRESETS.default.weights },
  activePreset: "default",
  categoryFilter: "all", // 'all' | 'tropical' | 'seasonal'
  hubFilter: "all",      // 'all' | 'SHA' | 'HKG' | 'FRA'
  nonstopOnly: false,
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
  return raw.map(d => {
    const parsed = parseDestName(d);
    const defaultTotal = Math.round(computeDefaultScore(d) * 10) / 10;
    const weightedTotal = computeWeightedScore(d, state.weights);
    const pureBeachScore = Math.round((d.scores.seaSand + d.scores.calmness + d.scores.waterPlay) * 10) / 10;
    const cpIndex = Math.round((weightedTotal / Math.log10(Math.max(d.priceMin, 250))) * 10) / 10;
    return {
      ...d,
      _zh: parsed.zh,
      _en: parsed.en,
      _iso: parsed.iso,
      defaultTotal,
      weightedTotal,
      pureBeachScore,
      cpIndex
    };
  });
}

function matchesFilter(d, skipCatRegion = false) {
  if (!skipCatRegion) {
    if (state.categoryFilter !== "all" && d.category !== state.categoryFilter) return false;
    if (state.regionFilter !== "all" && d.region !== state.regionFilter) return false;
  }
  if (d.priceMin > state.maxPrice) return false;
  if (d.coldestWater < state.minWaterTemp) return false;
  if (state.verifiedOnly && !d.verified) return false;

  if (state.hubFilter !== "all") {
    const f = d.flights && d.flights[state.hubFilter];
    if (state.nonstopOnly && (!f || !f.nonstop)) return false;
  } else if (state.nonstopOnly) {
    const hasAnyNonstop = d.flights && (
      (d.flights.SHA && d.flights.SHA.nonstop) ||
      (d.flights.HKG && d.flights.HKG.nonstop) ||
      (d.flights.FRA && d.flights.FRA.nonstop)
    );
    if (!hasAnyNonstop) return false;
  }

  if (state.searchQuery.trim() !== "") {
    const q = state.searchQuery.trim().toLowerCase();
    const hay = `${d.name} ${d._zh} ${d._en} ${d._iso} ${d.region} ${d.bestSeason} ${(d.tags || []).join(" ")} ${d.note || ""}`.toLowerCase();
    if (!hay.includes(q)) return false;
  }

  return true;
}

function getProcessedData() {
  const enriched = getEnrichedAll();
  const filtered = enriched.filter(d => matchesFilter(d, false));

  filtered.sort((a, b) => {
    switch (state.sortBy) {
      case "score-desc":
        return b.weightedTotal - a.weightedTotal || a.priceMin - b.priceMin;
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

function postcardHTML(d, rank, opts = {}) {
  const isCompared = state.compareIds.includes(d.id);
  const isTrop = d.category === "tropical";
  const compact = opts.compact;
  return `
    <article class="postcard">
      <div class="pc-scene" onclick="openDestModal('${d.id}')">
        ${buildPostcardSVG(d, { prefix: opts.prefix || "pc" })}
        ${rank ? `<span class="pc-rank">No. ${rank}</span>` : ""}
        <span class="pc-badge${isTrop ? "" : " is-seasonal"}">${isTrop ? "全年可游" : "季节性"}</span>
        <span class="pc-score"><b>${d.weightedTotal.toFixed(1)}</b><small>/100</small></span>
      </div>
      <div class="pc-body">
        <p class="pc-meta">${esc(d.region)}</p>
        <h3 class="pc-title" onclick="openDestModal('${d.id}')">${esc(d._zh)}</h3>
        ${d._en ? `<p class="pc-en">${esc(d._en)}</p>` : ""}
        <div class="pc-facts">
          <span>夜 <b>${d.coldestNight.toFixed(1)}°</b></span>
          <span>水 <b>${d.coldestWater.toFixed(1)}°</b></span>
          <span>$<b>${d.priceMin.toLocaleString()}</b></span>
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
// Category & Region Chips
// ---------------------------------------------------------------------------

function renderChipBar() {
  const bar = document.getElementById("chip-bar");
  if (!bar) return;
  const all = getEnrichedAll().filter(d => matchesFilter(d, true));

  const totalCount = all.length;
  const tropCount = all.filter(d => d.category === "tropical").length;
  const seasCount = all.filter(d => d.category === "seasonal").length;

  const catChips = [
    { key: "all", label: "全部榜单", count: totalCount },
    { key: "tropical", label: "全年真热带", count: tropCount },
    { key: "seasonal", label: "季节性海岸", count: seasCount }
  ].map(c =>
    `<button type="button" class="chip" aria-pressed="${state.categoryFilter === c.key}" onclick="setCategoryChip('${c.key}')">${esc(c.label)}<span class="count">${c.count}</span></button>`
  ).join("");

  const poolForRegion = all.filter(d => state.categoryFilter === "all" || d.category === state.categoryFilter);
  const regChips = [
    `<button type="button" class="chip" aria-pressed="${state.regionFilter === 'all'}" onclick="setRegionChip('all')">全部海域</button>`
  ].concat(
    REGIONS.map(r => {
      const cnt = poolForRegion.filter(d => d.region === r).length;
      return `<button type="button" class="chip" aria-pressed="${state.regionFilter === r}" onclick="setRegionChip('${r}')">${esc(r)}<span class="count">${cnt}</span></button>`;
    })
  ).join("");

  bar.innerHTML = `${catChips}<span class="chip-sep" aria-hidden="true"></span>${regChips}`;
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

function renderFlightBadge(dest) {
  const f = dest.flights || {};
  const badges = [];

  if (state.hubFilter !== "all") {
    const hubData = f[state.hubFilter];
    const hubName = state.hubFilter === "SHA" ? "上海" : state.hubFilter === "HKG" ? "香港" : "法兰克福";
    if (hubData && hubData.nonstop) {
      const pkgText = hubData.total2p ? ` · 双人机酒 $${hubData.total2p.toLocaleString()}` : "";
      return `<div class="t-flights"><span class="flight-code" style="border-color:var(--lagoon);color:var(--lagoon)">${hubName}直飞 ${esc(hubData.duration)}${pkgText}</span></div>`;
    }
    return `<div class="t-flights"><span style="font-size:11.5px;color:var(--ink-3)">该城市需转机</span></div>`;
  }

  const pushHub = (code, label) => {
    const fd = f[code];
    if (!fd || !fd.nonstop) return;
    const dur = fd.duration.split(" ")[0];
    const tip = `${fd.airline || label} (${fd.duration}) · 点击筛选该枢纽直飞`;
    badges.push(`<button type="button" class="flight-code" onclick="filterByHub('${code}')" title="${esc(tip)}">${label} ${esc(dur)}</button>`);
  };

  pushHub("SHA", "沪直飞");
  pushHub("HKG", "港直飞");
  pushHub("FRA", "德直飞");

  return badges.length ? `<div class="t-flights">${badges.join("")}</div>` : "";
}

function renderTags(tags) {
  if (!tags || !tags.length) return "";
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
  const data = getProcessedData();

  renderChipBar();

  const totalCountEl = document.getElementById("kpi-total-count");
  const tropicalCountEl = document.getElementById("kpi-tropical-count");
  const seasonalCountEl = document.getElementById("kpi-seasonal-count");
  const avgPriceEl = document.getElementById("kpi-avg-price");
  const topDestEl = document.getElementById("kpi-top-dest");

  if (totalCountEl) totalCountEl.textContent = data.length;
  if (tropicalCountEl) tropicalCountEl.textContent = data.filter(d => d.category === "tropical").length;
  if (seasonalCountEl) seasonalCountEl.textContent = data.filter(d => d.category === "seasonal").length;

  if (avgPriceEl) {
    const cheapest = data.length ? [...data].sort((a, b) => a.priceMin - b.priceMin)[0] : null;
    avgPriceEl.innerHTML = cheapest ? `<span class="mono">$${cheapest.priceMin.toLocaleString()}</span> <small>${esc(cheapest._zh)}</small>` : "—";
  }
  if (topDestEl) {
    topDestEl.innerHTML = data.length ? `${esc(data[0]._zh)} <small>${data[0].weightedTotal.toFixed(1)}分</small>` : "无匹配结果";
  }

  const summaryEl = document.getElementById("results-summary");
  if (summaryEl) {
    const presetName = state.activePreset === "custom" ? "自定义权重" : (WEIGHT_PRESETS[state.activePreset]?.label || "");
    summaryEl.textContent = `共 ${data.length} 处 · ${SORT_LABELS[state.sortBy] || ""} · 权重：${presetName}`;
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
}

function emptyStateHTML() {
  return `
    <div class="empty-state">
      <h3>没有匹配当前筛选条件的海滨目的地</h3>
      <p>请尝试放宽水温、预算或直飞限制，或清空搜索关键词。</p>
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
    const catMark = d.category === "tropical"
      ? `<span class="t-cat-mark" title="全年最冷月夜温≥18°C 且 水温≥21°C">真热带 No.${d.origRank}</span>`
      : `<span class="t-cat-mark is-seasonal" title="季节性/亚热带/地中海">季节性 No.${d.origRank}</span>`;

    const diff = Math.round((d.weightedTotal - d.defaultTotal) * 10) / 10;
    const diffHtml = diff !== 0
      ? `<span class="t-delta ${diff > 0 ? "up" : ""}">${diff > 0 ? "+" : ""}${diff.toFixed(1)}</span>`
      : "";

    const isSeasonal = d.coldestNight < 18 || d.coldestWater < 21;
    const dimCells = Object.entries(DIM_LABELS).map(([k, meta]) =>
      `<td class="num">${renderDimCell(d.scores[k], meta.max)}</td>`
    ).join("");

    return `
      <tr class="${isCompared ? "is-compared" : ""}">
        <td class="num">
          <span class="t-rank ${rank <= 3 ? "is-top" : ""}">${rank}</span>
        </td>
        <td style="min-width:280px;max-width:390px">
          <div class="t-dest-head">
            <a class="t-title" href="#dest-${d.id}" onclick="event.preventDefault();openDestModal('${d.id}')">${esc(d._zh)}</a>
            ${d._en ? `<span class="t-en">${esc(d._en)}</span>` : ""}
          </div>
          <div class="t-meta">
            ${catMark}
            <span>·</span>
            <span>${esc(d.region)}</span>
            <span>·</span>
            <span>最佳 ${esc(d.bestSeason)}</span>
          </div>
          ${renderFlightBadge(d)}
          ${renderTags(d.tags)}
          <p class="t-note">${esc(d.note || "")}</p>
        </td>
        <td class="num">
          <div class="t-climate">
            <div>夜 ${d.coldestNight.toFixed(1)}°C</div>
            <div>水 ${d.coldestWater.toFixed(1)}°C</div>
          </div>
          <div class="t-climate-sub ${isSeasonal ? "is-seasonal" : ""}">
            <span class="dot"></span>
            <span>${isSeasonal ? "分季节" : "365天适泳"}</span>
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
            <button type="button" class="text-link" style="font-size:12px" onclick="openDestModal('${d.id}')">详单</button>
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

  tbody.innerHTML = window.ELIMINATED_DESTINATIONS.map(d => {
    const parsed = parseDestName(d);
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
        <td class="num mono" style="white-space:nowrap">夜 ${d.coldestNight}°C / 水 ${d.coldestWater}°C</td>
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

  const weighted = items.map(d => d.weightedTotal);
  const prices = items.map(d => d.priceMin);
  const waters = items.map(d => d.coldestWater);

  content.innerHTML = `
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
              <td>最冷月夜温 / 水温</td>
              ${bestMark(waters).map((b, i) => tdCell(`${items[i].coldestNight}° / ${items[i].coldestWater}°C`, b)).join("")}
            </tr>
            <tr>
              <td>5 晚参考价</td>
              ${bestMark(prices, false).map((b, i) => tdCell(`<strong style="color:var(--ocean-deep)">$${items[i].priceMin.toLocaleString()}</strong><div style="font-size:11.5px;color:var(--ink-3);margin-top:2px">${esc(cleanPriceDisplay(items[i].priceDisplay))}</div>`, b)).join("")}
            </tr>
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
// Destination dossier dialog (#dest-modal)
// ---------------------------------------------------------------------------

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
  const isTrop = d.category === "tropical";

  const f = d.flights || {};
  const flightRows = [
    ["上海", f.SHA],
    ["香港", f.HKG],
    ["法兰克福", f.FRA]
  ].map(([hub, info]) => {
    if (info && info.nonstop) {
      const extra = [info.airline, info.total2p ? `双人机酒 $${info.total2p.toLocaleString()}` : ""].filter(Boolean).join(" · ");
      return `<div class="flight-row"><span>从${hub}</span><span class="ok">直飞 ${esc(info.duration)}${extra ? `<br><small style="font-weight:400;color:var(--ink-3)">${esc(extra)}</small>` : ""}</span></div>`;
    }
    return `<div class="flight-row"><span>从${hub}</span><span class="no">需转机</span></div>`;
  }).join("");

  body.innerHTML = `
    <div class="dossier-hero">
      ${buildPostcardSVG(d, { wide: true, prefix: "dm" })}
      <button type="button" class="dialog-close" onclick="closeDestModal()" aria-label="关闭">${icon("close")}</button>
    </div>
    <div class="dossier-head">
      <span class="eyebrow">${esc(d.region)} · ${isTrop ? "全年真热带" : "季节性海岸"} 原榜第 ${d.origRank} 名</span>
      <h2 id="dest-modal-title">${esc(d._zh)}${d._en ? `<span>${esc(d._en)}</span>` : ""}</h2>
      <dl class="dossier-stats">
        <div><dt>当前排名</dt><dd>${rank > 0 ? `No. ${rank}` : "—"}</dd></div>
        <div><dt>综合得分</dt><dd>${d.weightedTotal.toFixed(1)}</dd></div>
        <div><dt>最冷月夜温 / 水温</dt><dd>${d.coldestNight}° / ${d.coldestWater}°</dd></div>
        <div><dt>5 晚参考价</dt><dd>$${d.priceMin.toLocaleString()}</dd></div>
      </dl>
    </div>
    <div class="dialog-body">
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
          <p class="block-h">最佳季节</p>
          <p style="font-size:14px;color:var(--ink)">${esc(d.bestSeason)}</p>
          <p class="block-h" style="margin-top:24px">直飞航线</p>
          ${flightRows}
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
  const all = getProcessedData();
  const matches = query
    ? all.filter(d => `${d.name} ${d._zh} ${d._en} ${d.region} ${(d.tags || []).join(" ")} ${d.note || ""}`.toLowerCase().includes(query)).slice(0, 20)
    : all.slice(0, 12);

  if (!matches.length) {
    box.innerHTML = `<div style="padding:28px;text-align:center;color:var(--ink-3);font-size:13px">未找到匹配的目的地</div>`;
    return;
  }

  box.innerHTML = matches.map(d => `
    <button type="button" class="palette-item" onclick="closePalette();openDestModal('${d.id}')">
      <span class="code" style="min-width:34px">${d.weightedTotal.toFixed(1)}</span>
      <span><strong style="font-family:var(--serif);font-weight:500;color:var(--ocean-deep)">${esc(d._zh)}</strong> <span style="font-family:var(--display);font-style:italic;color:var(--ink-3)">${esc(d._en)}</span></span>
      <span class="sub">$${d.priceMin.toLocaleString()}</span>
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
  const headers = [
    "当前排名", "原榜分类", "原榜排名", "目的地名称", "英文名", "所属区域",
    "最冷月夜温(°C)", "最冷月水温(°C)", "最佳季节",
    "加权总分", "默认总分",
    "海沙(25)", "风景(15)", "玩水(15)", "风浪(10)", "酒店(10)", "餐饮(10)", "陆地(10)", "省心(5)",
    "5晚4★海景最低价(USD)", "房价说明", "亮点与避坑备注"
  ];

  const rows = data.map((d, idx) => [
    idx + 1,
    d.category === "tropical" ? "365天真热带Top100" : "季节性/亚热带Top45",
    d.origRank,
    `"${d._zh.replace(/"/g, '""')}"`,
    `"${d._en.replace(/"/g, '""')}"`,
    `"${d.region}"`,
    d.coldestNight,
    d.coldestWater,
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
    `"${(d.note || "").replace(/"/g, '""')}"`
  ]);

  const csvContent = "\uFEFF" + [headers.join(","), ...rows.map(r => r.join(","))].join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `oceanic_atlas_145_${state.categoryFilter}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

window.resetFilters = function() {
  state.categoryFilter = "all";
  state.hubFilter = "all";
  state.nonstopOnly = false;
  state.regionFilter = "all";
  state.maxPrice = 7000;
  state.minWaterTemp = 0;
  state.verifiedOnly = false;
  state.searchQuery = "";
  state.sortBy = "score-desc";

  document.getElementById("filter-category").value = "all";
  document.getElementById("filter-hub").value = "all";
  document.getElementById("filter-nonstop").checked = false;
  document.getElementById("filter-region").value = "all";
  document.getElementById("filter-price").value = 7000;
  updatePriceSliderUI();
  document.getElementById("filter-water-temp").value = "0";
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

window.filterByHub = function(hub) {
  state.hubFilter = hub;
  state.nonstopOnly = true;
  document.getElementById("filter-hub").value = hub;
  document.getElementById("filter-nonstop").checked = true;
  renderApp();
  document.getElementById("index")?.scrollIntoView({ behavior: "smooth" });
};

function setViewMode(mode) {
  state.viewMode = mode;
  document.getElementById("btn-view-table")?.setAttribute("aria-pressed", String(mode === "table"));
  document.getElementById("btn-view-cards")?.setAttribute("aria-pressed", String(mode === "cards"));
  renderApp();
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

  document.getElementById("filter-hub")?.addEventListener("change", e => {
    state.hubFilter = e.target.value;
    renderApp();
  });

  document.getElementById("filter-nonstop")?.addEventListener("change", e => {
    state.nonstopOnly = e.target.checked;
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

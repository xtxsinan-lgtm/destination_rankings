// Global 145 Beach & Island Resort Destinations — Interactive Application Engine

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
  seaSand: { name: "海沙水质", short: "海沙", max: 25, icon: "🏖️", color: "#06b6d4", desc: "海水透明度、松石绿层次、白沙细腻度" },
  scenery: { name: "自然风景", short: "风景", max: 15, icon: "⛰️", color: "#10b981", desc: "火山峰、花岗岩巨石、泻湖航拍、悬崖海岸" },
  waterPlay: { name: "玩水体验", short: "玩水", max: 15, icon: "🤿", color: "#3b82f6", desc: "浮潜珊瑚礁、深潜大货(鲸鲨/魔鬼鱼)、跳岛" },
  calmness: { name: "风浪舒适", short: "风浪", max: 10, icon: "🌊", color: "#14b8a6", desc: "外堡礁遮蔽、全年平静可安全下水游泳" },
  hotel: { name: "酒店硬件", short: "酒店", max: 10, icon: "🏨", color: "#8b5cf6", desc: "水屋/泳池别墅美学、一岛一酒店私密性" },
  dining: { name: "餐饮美食", short: "餐饮", max: 10, icon: "🦞", color: "#f59e0b", desc: "海鲜品质、当地菜系丰富度、米其林与酒吧" },
  land: { name: "陆地不无聊", short: "陆地", max: 10, icon: "🌋", color: "#f97316", desc: "古迹、火山雨林、野生动物、逛街夜市" },
  safety: { name: "安全省心", short: "省心", max: 5, icon: "🛡️", color: "#475569", desc: "社会治安、少推销宰客、卫生医疗与免签便利" }
};

const SORT_LABELS = {
  "score-desc": "加权总分",
  "price-asc": "房价从低到高",
  "cp-desc": "性价比指数",
  "beach-desc": "纯海滩硬实力",
  "water-desc": "最冷月水温",
  "night-desc": "最冷月夜温",
  "price-desc": "房价从高到低"
};

// Escape user-facing strings used inside HTML attributes / inline handlers
function escAttr(s) {
  return String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/'/g, "&#39;").replace(/</g, "&lt;");
}

// Visual tier for the weighted total score
function scoreTierClass(s) {
  if (s >= 90) return "bg-gradient-to-br from-amber-400 to-orange-500 text-white shadow-sm shadow-orange-200";
  if (s >= 85) return "bg-gradient-to-br from-emerald-500 to-teal-600 text-white shadow-sm shadow-emerald-200";
  if (s >= 80) return "bg-gradient-to-br from-sky-500 to-cyan-600 text-white shadow-sm shadow-sky-200";
  return "bg-slate-100 text-slate-700";
}

// Rank badge styling (medals for top 3)
function rankBadgeClass(rank) {
  if (rank === 1) return "bg-gradient-to-br from-amber-300 to-amber-500 text-white ring-2 ring-amber-100 shadow-sm";
  if (rank === 2) return "bg-gradient-to-br from-slate-300 to-slate-500 text-white ring-2 ring-slate-100 shadow-sm";
  if (rank === 3) return "bg-gradient-to-br from-orange-300 to-orange-600 text-white ring-2 ring-orange-100 shadow-sm";
  if (rank <= 10) return "bg-sky-50 text-sky-700 ring-1 ring-sky-100";
  return "text-slate-400";
}

const WEIGHT_PRESETS = {
  default: {
    label: "⚖️ 标准综合权重 (默认)",
    weights: { seaSand: 25, scenery: 15, waterPlay: 15, calmness: 10, hotel: 10, dining: 10, land: 10, safety: 5 }
  },
  water: {
    label: "🤿 潜水与果冻海控",
    weights: { seaSand: 35, scenery: 10, waterPlay: 30, calmness: 15, hotel: 3, dining: 2, land: 2, safety: 3 }
  },
  honeymoon: {
    label: "💎 蜜月颜值与顶奢水屋",
    weights: { seaSand: 25, scenery: 25, waterPlay: 10, calmness: 10, hotel: 20, dining: 5, land: 0, safety: 5 }
  },
  family: {
    label: "👶 亲子平浪泻湖与省心",
    weights: { seaSand: 25, scenery: 5, waterPlay: 10, calmness: 25, hotel: 15, dining: 10, land: 0, safety: 10 }
  },
  explorer: {
    label: "🌋 吃货与陆地探险不无聊",
    weights: { seaSand: 10, scenery: 20, waterPlay: 5, calmness: 5, hotel: 15, dining: 20, land: 20, safety: 5 }
  },
  pureBeach: {
    label: "🏖️ 纯海滩自然硬实力",
    weights: { seaSand: 45, scenery: 20, waterPlay: 20, calmness: 15, hotel: 0, dining: 0, land: 0, safety: 0 }
  }
};

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
  compareIds: ["bora-bora", "seychelles-praslin-ladigue", "kota-kinabalu"] // pre-populated 3 classic benchmarks
};

// Calculate weighted score out of 100 based on current user weights
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

// Prepare enriched & sorted dataset
function getProcessedData() {
  const raw = window.DESTINATIONS_DATA || [];

  // 1. Enrich with dynamic scores
  const enriched = raw.map(d => {
    const defaultTotal = Math.round(computeDefaultScore(d) * 10) / 10;
    const weightedTotal = computeWeightedScore(d, state.weights);
    const pureBeachScore = Math.round((d.scores.seaSand + d.scores.calmness + d.scores.waterPlay) * 10) / 10;
    const cpIndex = Math.round((weightedTotal / Math.log10(Math.max(d.priceMin, 250))) * 10) / 10;
    return {
      ...d,
      defaultTotal,
      weightedTotal,
      pureBeachScore,
      cpIndex
    };
  });

  // 2. Filter
  const filtered = enriched.filter(d => {
    if (state.categoryFilter !== "all" && d.category !== state.categoryFilter) return false;
    if (state.regionFilter !== "all" && d.region !== state.regionFilter) return false;
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
      const hay = `${d.name} ${d.region} ${d.bestSeason} ${(d.tags || []).join(" ")} ${d.note || ""}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }

    return true;
  });

  // 3. Sort
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

// Render helper for flight badge
function renderFlightBadge(dest) {
  const f = dest.flights || {};
  const badges = [];

  if (state.hubFilter !== "all") {
    const hubData = f[state.hubFilter];
    const hubName = state.hubFilter === "SHA" ? "上海" : state.hubFilter === "HKG" ? "香港" : "法兰克福";
    if (hubData && hubData.nonstop) {
      const pkgText = hubData.total2p ? ` · 机+酒 $${hubData.total2p.toLocaleString()}` : "";
      return `<div class="mt-1.5 inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold bg-emerald-50 text-emerald-700 ring-1 ring-inset ring-emerald-200 tnum">
        ✈️ ${hubName}直飞 ${hubData.duration}${pkgText}
      </div>`;
    } else {
      return `<div class="mt-1.5 text-[11px] text-slate-400">需转机</div>`;
    }
  }

  const hubBadge = (hub, label, cls) => {
    const fd = f[hub];
    if (!fd || !fd.nonstop) return;
    badges.push(`<button type="button" onclick="filterByHub('${hub}')" class="inline-flex items-center px-1.5 py-0.5 rounded-md text-[11px] font-medium ring-1 ring-inset transition hover:brightness-95 tnum ${cls}" title="${escAttr((fd.airline || '') + ' (' + fd.duration + ') · 点击仅看该出发地直飞')}">✈️ ${label} ${fd.duration.split(' ')[0]}</button>`);
  };
  hubBadge("SHA", "沪直飞", "bg-blue-50 text-blue-700 ring-blue-200");
  hubBadge("HKG", "港直飞", "bg-purple-50 text-purple-700 ring-purple-200");
  hubBadge("FRA", "德直飞", "bg-amber-50 text-amber-800 ring-amber-200");

  return badges.length > 0 ? `<div class="flex flex-wrap gap-1 mt-1.5">${badges.join("")}</div>` : "";
}

// Render clickable tag chips (click = search by tag)
function renderTags(tags, cls = "bg-slate-100 text-slate-600 hover:bg-sky-100 hover:text-sky-800") {
  return (tags || []).map(t =>
    `<button type="button" onclick="searchTag(this.dataset.tag)" data-tag="${escAttr(t)}" class="px-1.5 py-0.5 rounded-md text-[11px] transition ${cls}" title="筛选包含「${escAttr(t)}」的目的地">${t}</button>`
  ).join("");
}

// Render score progress pill
function renderScoreCell(val, max, color = "#0ea5e9") {
  const pct = Math.min(100, Math.round((val / max) * 100));
  const isTop = pct >= 95;
  return `
    <div class="flex flex-col items-center gap-1">
      <span class="text-xs tnum ${isTop ? 'font-bold text-slate-900' : 'font-medium text-slate-600'}">${val.toFixed(1)}</span>
      <div class="w-10 h-1 bg-slate-100 rounded-full overflow-hidden">
        <div class="h-full rounded-full" style="width:${pct}%;background:${color};opacity:${(0.35 + 0.65 * pct / 100).toFixed(2)}"></div>
      </div>
    </div>
  `;
}

// Main Render Function
function renderApp() {
  const data = getProcessedData();

  // Update summary KPIs
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
    avgPriceEl.textContent = cheapest ? `$${cheapest.priceMin.toLocaleString()} (${cheapest.name.split(" ")[1] || cheapest.name})` : "—";
  }
  if (topDestEl) {
    topDestEl.textContent = data.length ? `${data[0].name.replace(/^[^\s]+\s/, "")} (${data[0].weightedTotal.toFixed(1)}分)` : "无匹配结果";
    topDestEl.title = topDestEl.textContent;
  }

  const summaryEl = document.getElementById("results-summary");
  if (summaryEl) {
    const presetName = state.activePreset === "custom" ? "自定义权重" : (WEIGHT_PRESETS[state.activePreset]?.label || "");
    summaryEl.innerHTML = `共 <strong class="text-slate-900 tnum">${data.length}</strong> 个目的地 · 按 <strong class="text-slate-700">${SORT_LABELS[state.sortBy] || ""}</strong> 排序 · <span class="text-slate-400">${presetName}</span>`;
  }

  // Render View
  const tableContainer = document.getElementById("table-view-container");
  const cardsContainer = document.getElementById("cards-view-container");

  if (state.viewMode === "table") {
    tableContainer.classList.remove("hidden");
    cardsContainer.classList.add("hidden");
    renderTable(data);
  } else {
    tableContainer.classList.add("hidden");
    cardsContainer.classList.remove("hidden");
    renderCards(data);
  }

  renderCompareBar();
}

function emptyStateHTML(colspanAttr = "") {
  return `
    <div class="py-16 flex flex-col items-center text-center">
      <div class="w-14 h-14 rounded-2xl bg-slate-100 flex items-center justify-center text-2xl">🏝️</div>
      <div class="mt-3 text-sm font-semibold text-slate-700">没有符合当前筛选条件的海滨目的地</div>
      <div class="mt-1 text-xs text-slate-400">请尝试放宽筛选条件</div>
      <button onclick="resetFilters()" class="mt-4 px-4 py-2 rounded-xl text-xs font-semibold bg-sky-600 hover:bg-sky-700 text-white shadow-sm transition">重置全部筛选</button>
    </div>`;
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
    const catBadge = d.category === "tropical"
      ? `<span class="inline-flex items-center px-1.5 py-0.5 rounded-md text-[10.5px] font-semibold bg-rose-50 text-rose-700 ring-1 ring-inset ring-rose-200" title="最冷月夜温≥18°C & 水温≥21°C (原真热带榜 #${d.origRank})">🔥 真热带 #${d.origRank}</span>`
      : `<span class="inline-flex items-center px-1.5 py-0.5 rounded-md text-[10.5px] font-semibold bg-sky-50 text-sky-700 ring-1 ring-inset ring-sky-200" title="季节性/亚热带/地中海 (原季节榜 #${d.origRank})">☀️ 季节性 #${d.origRank}</span>`;

    const diff = Math.round((d.weightedTotal - d.defaultTotal) * 10) / 10;
    const diffBadge = diff !== 0
      ? `<div class="mt-1 text-[10.5px] font-semibold tnum ${diff > 0 ? 'text-emerald-600' : 'text-rose-500'}">${diff > 0 ? '▲' : '▼'} ${Math.abs(diff).toFixed(1)}</div>`
      : "";

    const tempWarn = d.coldestNight < 18 || d.coldestWater < 21;
    const dimCells = Object.entries(DIM_LABELS).map(([k, meta]) =>
      `<td class="py-3.5 px-1.5 text-center">${renderScoreCell(d.scores[k], meta.max, meta.color)}</td>`
    ).join("");

    return `
      <tr class="border-b border-slate-100 transition-colors ${isCompared ? 'bg-amber-50/50 hover:bg-amber-50' : 'hover:bg-slate-50/80'}">
        <td class="py-3.5 px-2.5 text-center whitespace-nowrap align-middle">
          <div class="inline-flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold tnum ${rankBadgeClass(rank)}">
            ${rank}
          </div>
        </td>
        <td class="py-3.5 px-3 min-w-[260px] max-w-[340px]">
          <div class="font-bold text-slate-900 text-[13.5px] leading-snug flex items-center gap-1.5 flex-wrap">
            <span>${d.name}</span>
            ${catBadge}
          </div>
          <div class="text-[11.5px] text-slate-500 mt-1 flex items-center gap-1.5 flex-wrap">
            <span class="text-slate-600 font-medium">${d.region}</span>
            <span class="text-slate-300">•</span>
            <span>📅 ${d.bestSeason}</span>
          </div>
          ${renderFlightBadge(d)}
          <div class="flex flex-wrap gap-1 mt-1.5">
            ${renderTags(d.tags)}
          </div>
          <p class="text-[11.5px] text-slate-500 mt-1.5 leading-relaxed">${d.note || ""}</p>
        </td>
        <td class="py-3.5 px-2 text-center whitespace-nowrap">
          <div class="text-xs font-semibold tnum ${d.coldestNight >= 18 ? 'text-emerald-700' : 'text-amber-600'}">🌙 ${d.coldestNight.toFixed(1)}°C</div>
          <div class="text-xs font-semibold tnum ${d.coldestWater >= 21 ? 'text-sky-700' : 'text-indigo-600'} mt-0.5">🌊 ${d.coldestWater.toFixed(1)}°C</div>
          ${tempWarn
            ? `<span class="inline-block mt-1 text-[10px] font-medium text-amber-700 bg-amber-50 ring-1 ring-inset ring-amber-200 px-1.5 rounded">分季节</span>`
            : `<span class="inline-block mt-1 text-[10px] font-medium text-emerald-700 bg-emerald-50 ring-1 ring-inset ring-emerald-200 px-1.5 rounded">365天适泳</span>`}
        </td>
        <td class="py-3.5 px-2.5 text-center whitespace-nowrap bg-sky-50/40">
          <div class="inline-flex items-center justify-center min-w-[52px] px-2 py-1 rounded-lg text-[15px] font-extrabold tnum ${scoreTierClass(d.weightedTotal)}">${d.weightedTotal.toFixed(1)}</div>
          ${diffBadge}
        </td>
        ${dimCells}
        <td class="py-3.5 px-3 text-right whitespace-nowrap">
          <div class="font-extrabold text-slate-900 text-[15px] tnum">$${d.priceMin.toLocaleString()}</div>
          <div class="text-[11px] ${d.verified ? 'text-emerald-700 font-medium' : 'text-slate-500'} max-w-[180px] ml-auto truncate" title="${escAttr(d.priceDisplay)}">
            ${d.priceDisplay}
          </div>
          <div class="mt-2 flex items-center justify-end gap-1.5">
            <a href="${d.hotelUrl}" target="_blank" rel="noopener noreferrer" class="px-2.5 py-1 text-[11px] font-semibold bg-sky-600 hover:bg-sky-700 text-white rounded-lg shadow-sm transition">
              查实时房价 ↗
            </a>
            <button onclick="toggleCompare('${d.id}')" class="px-2.5 py-1 text-[11px] font-semibold rounded-lg ring-1 ring-inset transition ${isCompared ? 'bg-amber-500 text-white ring-amber-500' : 'bg-white text-slate-700 ring-slate-200 hover:bg-slate-50 hover:ring-slate-300'}">
              ${isCompared ? '✓ 已选PK' : '+ PK'}
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
    container.innerHTML = `<div class="col-span-full bg-white rounded-2xl ring-1 ring-slate-200/80">${emptyStateHTML()}</div>`;
    return;
  }

  container.innerHTML = data.map((d, idx) => {
    const rank = idx + 1;
    const isCompared = state.compareIds.includes(d.id);
    const catBadge = d.category === "tropical"
      ? `<span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-rose-50 text-rose-700 ring-1 ring-inset ring-rose-200">🔥 真热带 #${d.origRank}</span>`
      : `<span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-sky-50 text-sky-700 ring-1 ring-inset ring-sky-200">☀️ 季节性 #${d.origRank}</span>`;

    const dimBars = Object.entries(DIM_LABELS).map(([k, meta]) => {
      const pct = Math.min(100, Math.round((d.scores[k] / meta.max) * 100));
      return `
        <div class="flex items-center gap-2" title="${meta.name} ${d.scores[k]} / ${meta.max}">
          <span class="w-8 shrink-0 text-[10.5px] text-slate-500">${meta.short}</span>
          <div class="flex-1 h-1.5 rounded-full bg-slate-100 overflow-hidden">
            <div class="h-full rounded-full" style="width:${pct}%;background:${meta.color}"></div>
          </div>
          <span class="w-9 shrink-0 text-right text-[10.5px] font-semibold text-slate-700 tnum">${d.scores[k]}<span class="font-normal text-slate-400">/${meta.max}</span></span>
        </div>`;
    }).join("");

    return `
      <div class="anim-fade-up group bg-white rounded-2xl ring-1 ${isCompared ? 'ring-amber-300' : 'ring-slate-200/80'} shadow-soft hover:shadow-lift hover:-translate-y-0.5 transition duration-200 p-5 flex flex-col justify-between" style="animation-delay:${Math.min(idx, 12) * 25}ms">
        <div>
          <div class="flex items-start justify-between gap-2">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="inline-flex items-center justify-center w-8 h-8 rounded-full text-xs font-bold tnum ${rank <= 10 ? rankBadgeClass(rank) : 'bg-slate-100 text-slate-600'}">${rank}</span>
              ${catBadge}
              <span class="text-[11px] text-slate-500">${d.region}</span>
            </div>
            <div class="shrink-0 text-right">
              <div class="inline-flex items-baseline gap-0.5 px-2 py-1 rounded-lg tnum ${scoreTierClass(d.weightedTotal)}">
                <span class="text-lg font-extrabold leading-none">${d.weightedTotal.toFixed(1)}</span>
              </div>
            </div>
          </div>

          <h3 class="font-bold text-slate-900 text-[15px] leading-snug mt-3">${d.name}</h3>
          <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-slate-600 mt-1.5">
            <span>🌙 最冷夜温 <strong class="tnum">${d.coldestNight.toFixed(1)}°C</strong></span>
            <span>🌊 最冷水温 <strong class="tnum">${d.coldestWater.toFixed(1)}°C</strong></span>
          </div>
          <div class="text-xs text-slate-500 mt-1">📅 最佳季节: ${d.bestSeason}</div>
          ${renderFlightBadge(d)}

          <div class="grid grid-cols-2 gap-x-4 gap-y-1.5 mt-4 p-3 rounded-xl bg-slate-50/80 ring-1 ring-inset ring-slate-100">
            ${dimBars}
          </div>

          <div class="flex flex-wrap gap-1 mt-3">
            ${renderTags(d.tags, "bg-sky-50 text-sky-800 hover:bg-sky-100")}
          </div>
          <p class="text-xs text-slate-600 mt-2.5 leading-relaxed">${d.note || ""}</p>
        </div>

        <div class="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between gap-2">
          <div class="min-w-0">
            <div class="text-[11px] text-slate-400">5晚4★海景</div>
            <div class="text-base font-extrabold text-slate-900 tnum leading-tight">$${d.priceMin.toLocaleString()}</div>
            <div class="text-[11px] ${d.verified ? 'text-emerald-700' : 'text-slate-500'} truncate max-w-[180px]" title="${escAttr(d.priceDisplay)}">${d.priceDisplay}</div>
          </div>
          <div class="flex items-center gap-1.5 shrink-0">
            <a href="${d.hotelUrl}" target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 text-xs font-semibold bg-sky-600 hover:bg-sky-700 text-white rounded-lg shadow-sm transition">
              查房价 ↗
            </a>
            <button onclick="toggleCompare('${d.id}')" class="px-3 py-1.5 text-xs font-semibold rounded-lg ring-1 ring-inset transition ${isCompared ? 'bg-amber-500 text-white ring-amber-500' : 'bg-white text-slate-700 ring-slate-200 hover:bg-slate-50'}">
              ${isCompared ? '✓ 已选PK' : '+ PK'}
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// Render Eliminated Gatekeepers Section
function renderEliminatedSection() {
  const tbody = document.getElementById("eliminated-tbody");
  if (!tbody || !window.ELIMINATED_DESTINATIONS) return;

  tbody.innerHTML = window.ELIMINATED_DESTINATIONS.map(d => `
    <tr class="border-b border-slate-100 last:border-0 hover:bg-rose-50/30 transition-colors align-top">
      <td class="py-3 px-4 font-bold text-slate-800 text-xs min-w-[180px]">${d.name}</td>
      <td class="py-3 px-2 text-center text-xs text-slate-600 whitespace-nowrap tnum">🌙 ${d.coldestNight}°C<br/>🌊 ${d.coldestWater}°C</td>
      <td class="py-3 px-2 text-center">
        <span class="inline-flex px-2 py-0.5 rounded-lg bg-rose-50 text-rose-600 ring-1 ring-inset ring-rose-200 font-extrabold text-sm tnum">${d.total.toFixed(1)}</span>
      </td>
      <td class="py-3 px-2">
        <div class="flex flex-wrap gap-1 justify-center max-w-[300px] mx-auto">
          ${Object.entries(DIM_LABELS).map(([k, meta]) => {
            const weak = d.scores[k] / meta.max < 0.6;
            return `<span class="px-1.5 py-0.5 rounded text-[10.5px] tnum ${weak ? 'bg-rose-100 text-rose-700 font-semibold' : 'bg-slate-100 text-slate-600'}">${meta.short} ${d.scores[k]}</span>`;
          }).join("")}
        </div>
      </td>
      <td class="py-3 px-2 text-xs text-slate-700 whitespace-nowrap">${d.priceDisplay}</td>
      <td class="py-3 px-4 text-xs text-slate-600 leading-relaxed min-w-[260px]">${d.reason}</td>
    </tr>
  `).join("");
}

// Weight Sliders UI (built once; values updated in place so dragging is never interrupted)
function renderWeightSliders() {
  const container = document.getElementById("weight-sliders-container");
  if (!container) return;

  container.innerHTML = Object.entries(DIM_LABELS).map(([key, meta]) => {
    const val = state.weights[key];
    return `
      <div class="rounded-xl p-3 bg-slate-50/80 ring-1 ring-inset ring-slate-200/70 hover:bg-white hover:ring-slate-300 transition" title="${escAttr(meta.desc)}">
        <div class="flex items-center justify-between text-xs mb-2">
          <span class="font-semibold text-slate-700 flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full" style="background:${meta.color}"></span>${meta.icon} ${meta.name}
          </span>
        </div>
        <div class="flex items-baseline gap-1 mb-2">
          <span data-weight-val="${key}" class="text-lg font-extrabold text-slate-900 tnum leading-none">${val}</span>
          <span data-weight-pct="${key}" class="text-[11px] font-medium text-slate-400 tnum"></span>
        </div>
        <input
          type="range"
          min="0"
          max="50"
          step="5"
          value="${val}"
          data-weight-input="${key}"
          oninput="updateWeight('${key}', this.value)"
          class="range"
          style="--c:${meta.color};--pct:${(val / 50) * 100}%"
          aria-label="${meta.name} 权重"
        />
        <div class="text-[10px] text-slate-400 mt-1.5 truncate">${meta.desc}</div>
      </div>
    `;
  }).join("");

  syncWeightUI();
}

// Sync slider values, percentages, distribution bar and preset buttons with state
function syncWeightUI() {
  const totalWeight = Object.values(state.weights).reduce((a, b) => a + b, 0);

  Object.entries(DIM_LABELS).forEach(([key, meta]) => {
    const val = state.weights[key];
    const normPct = totalWeight > 0 ? Math.round((val / totalWeight) * 100) : 0;
    const valEl = document.querySelector(`[data-weight-val="${key}"]`);
    const pctEl = document.querySelector(`[data-weight-pct="${key}"]`);
    const inputEl = document.querySelector(`[data-weight-input="${key}"]`);
    if (valEl) valEl.textContent = val;
    if (pctEl) pctEl.textContent = `占 ${normPct}%`;
    if (inputEl) {
      if (Number(inputEl.value) !== val) inputEl.value = val;
      inputEl.style.setProperty("--pct", `${(val / 50) * 100}%`);
    }
  });

  const distBar = document.getElementById("weight-distribution-bar");
  if (distBar) {
    distBar.innerHTML = totalWeight > 0
      ? Object.entries(DIM_LABELS).map(([key, meta]) => {
          const w = (state.weights[key] / totalWeight) * 100;
          return w > 0 ? `<div class="h-full transition-all duration-300" style="width:${w}%;background:${meta.color}" title="${meta.name} ${Math.round(w)}%"></div>` : "";
        }).join("")
      : "";
  }

  // Update preset buttons active state
  document.querySelectorAll("[data-preset]").forEach(btn => {
    const p = btn.getAttribute("data-preset");
    if (p === state.activePreset) {
      btn.className = "px-3 py-1.5 rounded-xl text-xs font-semibold bg-white text-sky-700 shadow-sm ring-1 ring-slate-200 transition";
    } else {
      btn.className = "px-3 py-1.5 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-white/60 transition";
    }
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

// PK Comparison Logic & SVG Radar Chart
window.toggleCompare = function(id) {
  const idx = state.compareIds.indexOf(id);
  if (idx >= 0) {
    state.compareIds.splice(idx, 1);
  } else {
    if (state.compareIds.length >= 3) {
      state.compareIds.shift(); // keep max 3
    }
    state.compareIds.push(id);
  }
  renderApp();
};

window.clearCompare = function() {
  state.compareIds = [];
  renderApp();
};

const COMPARE_COLORS = [
  { stroke: "#0284c7", fill: "rgba(2, 132, 199, 0.18)", text: "text-sky-600", badge: "bg-sky-50 text-sky-800 ring-1 ring-inset ring-sky-200" },
  { stroke: "#e11d48", fill: "rgba(225, 29, 72, 0.16)", text: "text-rose-600", badge: "bg-rose-50 text-rose-800 ring-1 ring-inset ring-rose-200" },
  { stroke: "#059669", fill: "rgba(5, 150, 105, 0.16)", text: "text-emerald-600", badge: "bg-emerald-50 text-emerald-800 ring-1 ring-inset ring-emerald-200" }
];

function renderCompareBar() {
  const bar = document.getElementById("compare-floating-bar");
  const listEl = document.getElementById("compare-selected-pills");
  if (!bar || !listEl) return;

  if (state.compareIds.length === 0) {
    bar.classList.add("hidden");
    return;
  }

  bar.classList.remove("hidden");
  const allData = window.DESTINATIONS_DATA || [];
  const items = state.compareIds.map(id => allData.find(d => d.id === id)).filter(Boolean);

  const pills = items.map((d, i) => `
    <span class="inline-flex items-center gap-1.5 pl-2 pr-1 py-1 rounded-full text-xs font-medium bg-white/10 ring-1 ring-inset ring-white/15">
      <span class="w-2 h-2 rounded-full" style="background:${COMPARE_COLORS[i].stroke}"></span>
      <span class="max-w-[110px] sm:max-w-[160px] truncate">${d.name.split(" (")[0]}</span>
      <button onclick="toggleCompare('${d.id}')" class="w-4 h-4 rounded-full text-slate-400 hover:text-white hover:bg-white/15 flex items-center justify-center leading-none" aria-label="移除">×</button>
    </span>
  `);
  for (let i = items.length; i < 3; i++) {
    pills.push(`<span class="hidden sm:inline-flex items-center px-3 py-1 rounded-full text-xs text-slate-500 border border-dashed border-white/20">+ 空位</span>`);
  }
  listEl.innerHTML = pills.join("");
}

window.openCompareModal = function() {
  const modal = document.getElementById("compare-modal");
  const content = document.getElementById("compare-modal-body");
  if (!modal || !content) return;

  const allData = window.DESTINATIONS_DATA || [];
  const items = state.compareIds.map(id => allData.find(d => d.id === id)).filter(Boolean);

  if (items.length === 0) {
    content.innerHTML = `
      <div class="py-14 flex flex-col items-center text-center">
        <div class="w-14 h-14 rounded-2xl bg-amber-50 flex items-center justify-center text-2xl">⚔️</div>
        <div class="mt-3 text-sm font-semibold text-slate-700">还没有选择对比目的地</div>
        <div class="mt-1 text-xs text-slate-400">在榜单中点击「+ PK」按钮，最多可选 3 个海岛进行雷达图对比</div>
      </div>`;
    openModalShell(modal);
    return;
  }

  const colors = COMPARE_COLORS;
  const radarSvg = buildRadarChartSVG(items, colors);

  // Highlight the best value in each row (only meaningful when comparing 2+)
  const bestMark = (values, higherIsBetter = true) => {
    if (items.length < 2) return values.map(() => false);
    const target = higherIsBetter ? Math.max(...values) : Math.min(...values);
    return values.map(v => v === target);
  };
  const cell = (content, isBest, extra = "") =>
    `<td class="py-2 px-3 ${extra} ${isBest ? 'bg-emerald-50/70' : ''}">${content}${isBest ? ' <span class="text-emerald-600 text-[10px] font-bold">★</span>' : ''}</td>`;

  const weighted = items.map(d => computeWeightedScore(d, state.weights));
  const prices = items.map(d => d.priceMin);
  const waters = items.map(d => d.coldestWater);

  content.innerHTML = `
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <div class="lg:col-span-5 flex flex-col items-center rounded-2xl bg-gradient-to-b from-slate-50 to-white ring-1 ring-slate-100 p-5">
        <h4 class="text-xs font-bold text-slate-500 tracking-wide mb-3">8维硬核实力雷达图 (归一化百分比)</h4>
        ${radarSvg}
        <div class="flex flex-wrap justify-center gap-2 mt-4">
          ${items.map((d, i) => `
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${colors[i].badge}">
              <span class="w-2.5 h-2.5 rounded-full" style="background:${colors[i].stroke}"></span>
              ${d.name.split(" (")[0]} <span class="tnum">(${weighted[i].toFixed(1)}分)</span>
            </span>
          `).join("")}
        </div>
      </div>

      <div class="lg:col-span-7 overflow-x-auto rounded-2xl ring-1 ring-slate-100">
        <table class="w-full text-xs text-left border-collapse">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50">
              <th class="py-2.5 px-3 text-slate-500 font-semibold">对比维度</th>
              ${items.map((d, i) => `<th class="py-2.5 px-3 font-bold ${colors[i].text}">${d.name.split(" (")[0]}</th>`).join("")}
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 tnum">
            <tr>
              <td class="py-2 px-3 font-semibold text-slate-700">🏆 当前加权总分</td>
              ${bestMark(weighted).map((b, i) => cell(`<span class="font-extrabold text-sm text-slate-900">${weighted[i].toFixed(1)}</span> <span class="text-slate-400">/ 100</span>`, b)).join("")}
            </tr>
            <tr>
              <td class="py-2 px-3 font-semibold text-slate-700">🌡️ 最冷月夜温 / 水温</td>
              ${bestMark(waters).map((b, i) => cell(`🌙 ${items[i].coldestNight}°C · 🌊 ${items[i].coldestWater}°C`, b)).join("")}
            </tr>
            <tr>
              <td class="py-2 px-3 font-semibold text-slate-700">💰 5晚4★海景房价</td>
              ${bestMark(prices, false).map((b, i) => cell(`<span class="font-bold text-slate-800">$${items[i].priceMin.toLocaleString()}</span><span class="block text-[10px] font-normal text-slate-500">${items[i].priceDisplay}</span>`, b)).join("")}
            </tr>
            ${Object.entries(DIM_LABELS).map(([k, meta]) => {
              const vals = items.map(d => d.scores[k]);
              return `
              <tr>
                <td class="py-1.5 px-3 text-slate-600 whitespace-nowrap"><span class="inline-block w-1.5 h-1.5 rounded-full mr-1 align-middle" style="background:${meta.color}"></span>${meta.icon} ${meta.name} <span class="text-slate-400">(满分${meta.max})</span></td>
                ${bestMark(vals).map((b, i) => cell(`<span class="font-semibold text-slate-800">${vals[i]}</span> <span class="text-slate-400">/ ${meta.max}</span>`, b, "py-1.5")).join("")}
              </tr>`;
            }).join("")}
            <tr>
              <td class="py-2 px-3 font-semibold text-slate-700">📅 最佳季节</td>
              ${items.map(d => `<td class="py-2 px-3 text-slate-600">${d.bestSeason}</td>`).join("")}
            </tr>
            <tr>
              <td class="py-2 px-3 font-semibold text-slate-700">🔗 预订验证</td>
              ${items.map(d => `<td class="py-2 px-3"><a href="${d.hotelUrl}" target="_blank" rel="noopener noreferrer" class="inline-flex px-2.5 py-1 rounded-lg bg-sky-600 hover:bg-sky-700 text-white font-semibold transition">查看实时房价 ↗</a></td>`).join("")}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;

  openModalShell(modal);
};

function openModalShell(modal) {
  modal.classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

window.closeCompareModal = function() {
  const modal = document.getElementById("compare-modal");
  if (modal) modal.classList.add("hidden");
  document.body.style.overflow = "";
};

function buildRadarChartSVG(items, colors) {
  const size = 300;
  const cx = size / 2;
  const cy = size / 2;
  const radius = 100;
  const keys = Object.keys(MAX_SCORES);
  const n = keys.length;

  const angleFor = (i) => (Math.PI * 2 * i) / n - Math.PI / 2;
  const pointFor = (i, ratio) => {
    const a = angleFor(i);
    const r = radius * ratio;
    return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  };

  // Grid rings (alternating fill for readability)
  const rings = [1.0, 0.75, 0.5, 0.25].map((r, ri) => {
    const pts = keys.map((_, i) => pointFor(i, r).join(",")).join(" ");
    return `<polygon points="${pts}" fill="${ri % 2 === 0 ? '#f8fafc' : '#ffffff'}" stroke="#e2e8f0" stroke-width="1" />`;
  }).join("");

  const ringLabels = [0.5, 1.0].map(r => {
    const [x, y] = pointFor(0, r);
    return `<text x="${x + 4}" y="${y + 3}" font-size="8" fill="#94a3b8">${Math.round(r * 100)}%</text>`;
  }).join("");

  // Axes & labels
  const axes = keys.map((k, i) => {
    const [x, y] = pointFor(i, 1.0);
    const [lx, ly] = pointFor(i, 1.24);
    return `
      <line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="#e2e8f0" stroke-width="1" />
      <text x="${lx}" y="${ly}" text-anchor="middle" dominant-baseline="middle" font-size="10.5" font-weight="600" fill="#475569">${DIM_LABELS[k].name}</text>
    `;
  }).join("");

  // Data polygons + vertex dots
  const polygons = items.map((d, idx) => {
    const c = colors[idx % colors.length];
    const pts = keys.map((k, i) => pointFor(i, Math.min(1, d.scores[k] / MAX_SCORES[k])));
    const dots = pts.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3" fill="#fff" stroke="${c.stroke}" stroke-width="1.8" />`).join("");
    return `<polygon points="${pts.map(p => p.join(",")).join(" ")}" fill="${c.fill}" stroke="${c.stroke}" stroke-width="2" stroke-linejoin="round" />${dots}`;
  }).join("");

  return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" class="overflow-visible max-w-full h-auto">${rings}${axes}${ringLabels}${polygons}</svg>`;
}

// Export CSV Function
window.exportCSV = function() {
  const data = getProcessedData();
  const headers = [
    "当前排名", "原榜分类", "原榜排名", "目的地名称", "所属区域",
    "最冷月夜温(°C)", "最冷月水温(°C)", "最佳季节",
    "加权总分", "默认总分",
    "海沙(25)", "风景(15)", "玩水(15)", "风浪(10)", "酒店(10)", "餐饮(10)", "陆地(10)", "省心(5)",
    "5晚4★海景最低价(USD)", "房价说明", "亮点与避坑备注"
  ];

  const rows = data.map((d, idx) => [
    idx + 1,
    d.category === "tropical" ? "365天真热带Top100" : "季节性/亚热带Top45",
    d.origRank,
    `"${d.name.replace(/"/g, '""')}"`,
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
    `"${d.priceDisplay.replace(/"/g, '""')}"`,
    `"${(d.note || "").replace(/"/g, '""')}"`
  ]);

  const csvContent = "\uFEFF" + [headers.join(","), ...rows.map(r => r.join(","))].join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `global_145_beach_destinations_${state.categoryFilter}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

// Reset all filters
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

// Price slider label + filled track
function updatePriceSliderUI() {
  const input = document.getElementById("filter-price");
  const label = document.getElementById("price-slider-label");
  if (!input) return;
  const min = Number(input.min), max = Number(input.max), val = Number(input.value);
  input.style.setProperty("--pct", `${((val - min) / (max - min)) * 100}%`);
  if (label) {
    label.textContent = val >= 7000 ? "不限 ($7,000+)" : `≤ $${val.toLocaleString()}`;
  }
}

function updateSearchClearBtn() {
  const btn = document.getElementById("filter-search-clear");
  if (btn) btn.classList.toggle("hidden", !state.searchQuery);
}

// Click a tag chip → search by that tag
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

// Click a nonstop flight badge → switch to that hub's nonstop view
window.filterByHub = function(hub) {
  state.hubFilter = hub;
  state.nonstopOnly = true;
  document.getElementById("filter-hub").value = hub;
  document.getElementById("filter-nonstop").checked = true;
  renderApp();
};

// View toggle (segmented control)
function setViewMode(mode) {
  state.viewMode = mode;
  const active = "view-btn px-3 py-1.5 rounded-lg text-xs font-semibold bg-white text-sky-700 shadow-sm ring-1 ring-slate-200 transition";
  const idle = "view-btn px-3 py-1.5 rounded-lg text-xs font-medium text-slate-500 hover:text-slate-800 transition";
  document.getElementById("btn-view-table").className = mode === "table" ? active : idle;
  document.getElementById("btn-view-cards").className = mode === "cards" ? active : idle;
  renderApp();
}

// Initialize Event Listeners on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  renderWeightSliders();
  renderEliminatedSection();
  updatePriceSliderUI();
  setViewMode(state.viewMode);

  document.getElementById("filter-category")?.addEventListener("change", e => {
    state.categoryFilter = e.target.value;
    renderApp();
  });

  document.getElementById("filter-hub")?.addEventListener("change", e => {
    state.hubFilter = e.target.value;
    renderApp();
  });

  document.getElementById("filter-nonstop")?.addEventListener("change", e => {
    state.nonstopOnly = e.target.checked;
    renderApp();
  });

  document.getElementById("filter-region")?.addEventListener("change", e => {
    state.regionFilter = e.target.value;
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

  // Keyboard: Esc closes modal, "/" focuses search
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") closeCompareModal();
    if (e.key === "/" && !/^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement?.tagName)) {
      e.preventDefault();
      document.getElementById("filter-search")?.focus();
    }
  });

  // Back-to-top visibility
  const backBtn = document.getElementById("back-to-top");
  const onScroll = () => {
    const show = window.scrollY > 600;
    backBtn?.classList.toggle("opacity-0", !show);
    backBtn?.classList.toggle("pointer-events-none", !show);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
});

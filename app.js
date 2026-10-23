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
  seaSand: { name: "海沙水质", max: 25, icon: "🏖️", desc: "海水透明度、松石绿层次、白沙细腻度" },
  scenery: { name: "自然风景", max: 15, icon: "⛰️", desc: "火山峰、花岗岩巨石、泻湖航拍、悬崖海岸" },
  waterPlay: { name: "玩水体验", max: 15, icon: "🤿", desc: "浮潜珊瑚礁、深潜大货(鲸鲨/魔鬼鱼)、跳岛" },
  calmness: { name: "风浪舒适", max: 10, icon: "🌊", desc: "外堡礁遮蔽、全年平静可安全下水游泳" },
  hotel: { name: "酒店硬件", max: 10, icon: "🏨", desc: "水屋/泳池别墅美学、一岛一酒店私密性" },
  dining: { name: "餐饮美食", max: 10, icon: "🦞", desc: "海鲜品质、当地菜系丰富度、米其林与酒吧" },
  land: { name: "陆地不无聊", max: 10, icon: "🌋", desc: "古迹、火山雨林、野生动物、逛街夜市" },
  safety: { name: "安全省心", max: 5, icon: "🛡️", desc: "社会治安、少推销宰客、卫生医疗与免签便利" }
};

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
      return `<div class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
        ✈️ ${hubName}直飞 ${hubData.duration}${pkgText}
      </div>`;
    } else {
      return `<span class="text-xs text-slate-400">需转机</span>`;
    }
  }

  if (f.SHA && f.SHA.nonstop) {
    badges.push(`<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-200" title="${f.SHA.airline || ''} (${f.SHA.duration})">✈️ 沪直飞 ${f.SHA.duration.split(' ')[0]}</span>`);
  }
  if (f.HKG && f.HKG.nonstop) {
    badges.push(`<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[11px] font-medium bg-purple-50 text-purple-700 border border-purple-200" title="${f.HKG.airline || ''} (${f.HKG.duration})">✈️ 港直飞 ${f.HKG.duration.split(' ')[0]}</span>`);
  }
  if (f.FRA && f.FRA.nonstop) {
    badges.push(`<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-800 border border-amber-200" title="${f.FRA.airline || ''} (${f.FRA.duration})">✈️ 德直飞 ${f.FRA.duration.split(' ')[0]}</span>`);
  }

  return badges.length > 0 ? `<div class="flex flex-wrap gap-1 mt-1">${badges.join("")}</div>` : "";
}

// Render score progress pill
function renderScoreCell(val, max, colorClass = "bg-sky-500") {
  const pct = Math.min(100, Math.round((val / max) * 100));
  return `
    <div class="flex flex-col items-center">
      <span class="font-semibold text-slate-700 text-xs">${val.toFixed(1)}</span>
      <div class="w-10 h-1 bg-slate-100 rounded-full overflow-hidden mt-0.5">
        <div class="${colorClass} h-full rounded-full" style="width:${pct}%"></div>
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

function renderTable(data) {
  const tbody = document.getElementById("destinations-tbody");
  if (!tbody) return;

  if (data.length === 0) {
    tbody.innerHTML = `<tr><td colspan="15" class="py-12 text-center text-slate-400 text-sm">没有符合当前筛选条件的海滨目的地，请尝试放宽筛选或点击“重置筛选”。</td></tr>`;
    return;
  }

  tbody.innerHTML = data.map((d, idx) => {
    const rank = idx + 1;
    const isCompared = state.compareIds.includes(d.id);
    const catBadge = d.category === "tropical"
      ? `<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[11px] font-semibold bg-rose-50 text-rose-700 border border-rose-200" title="最冷月夜温≥18°C & 水温≥21°C (原真热带榜 #${d.origRank})">🔥 真热带 #${d.origRank}</span>`
      : `<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[11px] font-semibold bg-sky-50 text-sky-700 border border-sky-200" title="季节性/亚热带/地中海 (原季节榜 #${d.origRank})">☀️ 季节性 #${d.origRank}</span>`;

    const diff = Math.round((d.weightedTotal - d.defaultTotal) * 10) / 10;
    const diffBadge = diff !== 0
      ? `<span class="ml-1 text-[11px] font-medium ${diff > 0 ? 'text-emerald-600' : 'text-rose-500'}">(${diff > 0 ? '+' : ''}${diff.toFixed(1)})</span>`
      : "";

    const tempWarn = d.coldestNight < 18 || d.coldestWater < 21;

    return `
      <tr class="hover:bg-sky-50/60 transition-colors border-b border-slate-100 group">
        <td class="py-3 px-2.5 text-center font-bold text-slate-700 text-sm whitespace-nowrap">
          <div class="inline-flex items-center justify-center w-6 h-6 rounded-full ${rank <= 3 ? 'bg-amber-400 text-white shadow-sm' : rank <= 10 ? 'bg-sky-100 text-sky-800' : 'text-slate-500'}">
            ${rank}
          </div>
        </td>
        <td class="py-3 px-3 min-w-[250px] max-w-[330px]">
          <div class="flex items-start justify-between gap-2">
            <div>
              <div class="font-bold text-slate-900 text-sm leading-snug flex items-center gap-1.5 flex-wrap">
                <span>${d.name}</span>
                ${catBadge}
              </div>
              <div class="text-xs text-slate-500 mt-0.5 flex items-center gap-1.5 flex-wrap">
                <span class="text-slate-600 font-medium">${d.region}</span>
                <span>·</span>
                <span>最佳: ${d.bestSeason}</span>
              </div>
              ${renderFlightBadge(d)}
              <div class="flex flex-wrap gap-1 mt-1.5">
                ${(d.tags || []).map(t => `<span class="px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded text-[11px]">${t}</span>`).join("")}
              </div>
              <p class="text-xs text-slate-500 mt-1 leading-relaxed">${d.note || ""}</p>
            </div>
          </div>
        </td>
        <td class="py-3 px-2 text-center whitespace-nowrap">
          <div class="text-xs font-semibold ${d.coldestNight >= 18 ? 'text-emerald-700' : 'text-amber-600'}">🌙 ${d.coldestNight.toFixed(1)}°C</div>
          <div class="text-xs font-semibold ${d.coldestWater >= 21 ? 'text-sky-700' : 'text-indigo-600'} mt-0.5">🌊 ${d.coldestWater.toFixed(1)}°C</div>
          ${tempWarn ? `<span class="text-[10px] text-amber-600 bg-amber-50 px-1 rounded">分季节</span>` : `<span class="text-[10px] text-emerald-600 bg-emerald-50 px-1 rounded">365天适泳</span>`}
        </td>
        <td class="py-3 px-2.5 text-center whitespace-nowrap bg-sky-50/40">
          <div class="text-base font-extrabold text-sky-700">${d.weightedTotal.toFixed(1)}</div>
          ${diffBadge}
        </td>
        <td class="py-3 px-1.5 text-center">${renderScoreCell(d.scores.seaSand, 25, "bg-cyan-500")}</td>
        <td class="py-3 px-1.5 text-center">${renderScoreCell(d.scores.scenery, 15, "bg-emerald-500")}</td>
        <td class="py-3 px-1.5 text-center">${renderScoreCell(d.scores.waterPlay, 15, "bg-blue-500")}</td>
        <td class="py-3 px-1.5 text-center">${renderScoreCell(d.scores.calmness, 10, "bg-teal-500")}</td>
        <td class="py-3 px-1.5 text-center">${renderScoreCell(d.scores.hotel, 10, "bg-purple-500")}</td>
        <td class="py-3 px-1.5 text-center">${renderScoreCell(d.scores.dining, 10, "bg-amber-500")}</td>
        <td class="py-3 px-1.5 text-center">${renderScoreCell(d.scores.land, 10, "bg-orange-500")}</td>
        <td class="py-3 px-1.5 text-center">${renderScoreCell(d.scores.safety, 5, "bg-slate-600")}</td>
        <td class="py-3 px-3 text-right whitespace-nowrap">
          <div class="font-bold text-slate-900 text-sm">$${d.priceMin.toLocaleString()}</div>
          <div class="text-[11px] ${d.verified ? 'text-emerald-700 font-medium' : 'text-slate-500'} max-w-[175px] truncate" title="${d.priceDisplay}">
            ${d.priceDisplay}
          </div>
          <div class="mt-1.5 flex items-center justify-end gap-1.5">
            <a href="${d.hotelUrl}" target="_blank" rel="noopener noreferrer" class="px-2 py-0.5 text-[11px] font-medium bg-sky-600 hover:bg-sky-700 text-white rounded transition">
              查实时房价 ↗
            </a>
            <button onclick="toggleCompare('${d.id}')" class="px-2 py-0.5 text-[11px] font-medium rounded border transition ${isCompared ? 'bg-amber-500 text-white border-amber-500' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}">
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
    container.innerHTML = `<div class="col-span-full py-12 text-center text-slate-400">没有符合当前筛选条件的目的地。</div>`;
    return;
  }

  container.innerHTML = data.map((d, idx) => {
    const rank = idx + 1;
    const isCompared = state.compareIds.includes(d.id);
    const catBadge = d.category === "tropical"
      ? `<span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">🔥 真热带 #${d.origRank}</span>`
      : `<span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-sky-50 text-sky-700 border border-sky-200">☀️ 季节性 #${d.origRank}</span>`;

    return `
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition p-4 flex flex-col justify-between">
        <div>
          <div class="flex items-start justify-between gap-2">
            <div class="flex items-center gap-2">
              <span class="inline-flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold ${rank <= 3 ? 'bg-amber-400 text-white' : 'bg-slate-100 text-slate-700'}">#${rank}</span>
              ${catBadge}
              <span class="text-xs text-slate-500">${d.region}</span>
            </div>
            <div class="text-right">
              <span class="text-xl font-extrabold text-sky-700">${d.weightedTotal.toFixed(1)}</span>
              <span class="text-xs text-slate-400">/100</span>
            </div>
          </div>

          <h3 class="font-bold text-slate-900 text-base mt-2">${d.name}</h3>
          <div class="flex items-center gap-3 text-xs text-slate-600 mt-1">
            <span>🌙 最冷夜温: <strong>${d.coldestNight.toFixed(1)}°C</strong></span>
            <span>🌊 最冷水温: <strong>${d.coldestWater.toFixed(1)}°C</strong></span>
          </div>
          <div class="text-xs text-slate-500 mt-0.5">📅 最佳季节: ${d.bestSeason}</div>
          ${renderFlightBadge(d)}

          <div class="grid grid-cols-4 gap-1.5 mt-3 bg-slate-50 p-2 rounded-lg text-center text-xs">
            <div><span class="text-slate-400 block text-[10px]">海沙/25</span><strong class="text-slate-700">${d.scores.seaSand}</strong></div>
            <div><span class="text-slate-400 block text-[10px]">风景/15</span><strong class="text-slate-700">${d.scores.scenery}</strong></div>
            <div><span class="text-slate-400 block text-[10px]">玩水/15</span><strong class="text-slate-700">${d.scores.waterPlay}</strong></div>
            <div><span class="text-slate-400 block text-[10px]">风浪/10</span><strong class="text-slate-700">${d.scores.calmness}</strong></div>
            <div><span class="text-slate-400 block text-[10px]">酒店/10</span><strong class="text-slate-700">${d.scores.hotel}</strong></div>
            <div><span class="text-slate-400 block text-[10px]">餐饮/10</span><strong class="text-slate-700">${d.scores.dining}</strong></div>
            <div><span class="text-slate-400 block text-[10px]">陆地/10</span><strong class="text-slate-700">${d.scores.land}</strong></div>
            <div><span class="text-slate-400 block text-[10px]">省心/5</span><strong class="text-slate-700">${d.scores.safety}</strong></div>
          </div>

          <div class="flex flex-wrap gap-1 mt-2.5">
            ${(d.tags || []).map(t => `<span class="px-1.5 py-0.5 bg-sky-50 text-sky-800 rounded text-[11px]">${t}</span>`).join("")}
          </div>
          <p class="text-xs text-slate-600 mt-2 leading-relaxed">${d.note || ""}</p>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
          <div>
            <div class="text-sm font-bold text-slate-900">5晚4★海景: $${d.priceMin.toLocaleString()}</div>
            <div class="text-[11px] text-slate-500 truncate max-w-[180px]" title="${d.priceDisplay}">${d.priceDisplay}</div>
          </div>
          <div class="flex items-center gap-1.5">
            <a href="${d.hotelUrl}" target="_blank" rel="noopener noreferrer" class="px-2.5 py-1 text-xs font-medium bg-sky-600 hover:bg-sky-700 text-white rounded-lg transition">
              查房价 ↗
            </a>
            <button onclick="toggleCompare('${d.id}')" class="px-2.5 py-1 text-xs font-medium rounded-lg border transition ${isCompared ? 'bg-amber-500 text-white border-amber-500' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}">
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
    <tr class="border-b border-slate-100 hover:bg-rose-50/30">
      <td class="py-2.5 px-3 font-bold text-slate-800 text-xs">${d.name}</td>
      <td class="py-2.5 px-2 text-center text-xs text-slate-600">🌙 ${d.coldestNight}°C / 🌊 ${d.coldestWater}°C</td>
      <td class="py-2.5 px-2 text-center font-bold text-rose-600 text-sm">${d.total.toFixed(1)}</td>
      <td class="py-2.5 px-2 text-center text-xs text-slate-600">
        海沙 ${d.scores.seaSand} · 风景 ${d.scores.scenery} · 玩水 ${d.scores.waterPlay} · 风浪 ${d.scores.calmness} · 酒店 ${d.scores.hotel} · 餐饮 ${d.scores.dining} · 陆地 ${d.scores.land} · 省心 ${d.scores.safety}
      </td>
      <td class="py-2.5 px-2 text-xs text-slate-700">${d.priceDisplay}</td>
      <td class="py-2.5 px-3 text-xs text-slate-600">${d.reason}</td>
    </tr>
  `).join("");
}

// Weight Sliders UI
function renderWeightSliders() {
  const container = document.getElementById("weight-sliders-container");
  if (!container) return;

  const totalWeight = Object.values(state.weights).reduce((a, b) => a + b, 0);

  container.innerHTML = Object.entries(DIM_LABELS).map(([key, meta]) => {
    const val = state.weights[key];
    const normPct = totalWeight > 0 ? Math.round((val / totalWeight) * 100) : 0;
    return `
      <div class="bg-slate-50 rounded-lg p-2.5 border border-slate-200/80">
        <div class="flex items-center justify-between text-xs mb-1">
          <span class="font-semibold text-slate-700">${meta.icon} ${meta.name}</span>
          <span class="font-bold text-sky-700">${val} <span class="text-[10px] font-normal text-slate-400">(${normPct}%)</span></span>
        </div>
        <input
          type="range"
          min="0"
          max="50"
          step="5"
          value="${val}"
          oninput="updateWeight('${key}', this.value)"
          class="w-full accent-sky-600 cursor-pointer h-1.5 bg-slate-200 rounded-lg"
        />
        <div class="text-[10px] text-slate-400 mt-0.5 truncate" title="${meta.desc}">${meta.desc}</div>
      </div>
    `;
  }).join("");

  // Update preset buttons active state
  document.querySelectorAll("[data-preset]").forEach(btn => {
    const p = btn.getAttribute("data-preset");
    if (p === state.activePreset) {
      btn.className = "px-3 py-1.5 rounded-full text-xs font-semibold bg-sky-600 text-white shadow-sm transition";
    } else {
      btn.className = "px-3 py-1.5 rounded-full text-xs font-medium bg-white text-slate-700 border border-slate-200 hover:bg-slate-50 transition";
    }
  });
}

window.updateWeight = function(key, value) {
  state.weights[key] = Number(value);
  state.activePreset = "custom";
  renderWeightSliders();
  renderApp();
};

window.applyPreset = function(presetKey) {
  if (!WEIGHT_PRESETS[presetKey]) return;
  state.weights = { ...WEIGHT_PRESETS[presetKey].weights };
  state.activePreset = presetKey;
  renderWeightSliders();
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

  listEl.innerHTML = items.map(d => `
    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-800 text-white border border-slate-600">
      ${d.name.split(" (")[0]}
      <button onclick="toggleCompare('${d.id}')" class="text-slate-400 hover:text-white font-bold">×</button>
    </span>
  `).join("");
}

window.openCompareModal = function() {
  const modal = document.getElementById("compare-modal");
  const content = document.getElementById("compare-modal-body");
  if (!modal || !content) return;

  const allData = window.DESTINATIONS_DATA || [];
  const items = state.compareIds.map(id => allData.find(d => d.id === id)).filter(Boolean);

  if (items.length === 0) return;

  const colors = [
    { stroke: "#0284c7", fill: "rgba(2, 132, 199, 0.2)", text: "text-sky-600", badge: "bg-sky-100 text-sky-800" },
    { stroke: "#e11d48", fill: "rgba(225, 29, 72, 0.2)", text: "text-rose-600", badge: "bg-rose-100 text-rose-800" },
    { stroke: "#059669", fill: "rgba(5, 150, 105, 0.2)", text: "text-emerald-600", badge: "bg-emerald-100 text-emerald-800" }
  ];

  const radarSvg = buildRadarChartSVG(items, colors);

  content.innerHTML = `
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
      <div class="lg:col-span-5 flex flex-col items-center">
        <h4 class="text-sm font-bold text-slate-700 mb-2">8维硬核实力雷达图 (归一化百分比)</h4>
        ${radarSvg}
        <div class="flex flex-wrap justify-center gap-3 mt-3">
          ${items.map((d, i) => `
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold ${colors[i].badge}">
              <span class="w-2.5 h-2.5 rounded-full" style="background:${colors[i].stroke}"></span>
              ${d.name.split(" (")[0]} (${computeWeightedScore(d, state.weights).toFixed(1)}分)
            </span>
          `).join("")}
        </div>
      </div>

      <div class="lg:col-span-7 overflow-x-auto">
        <table class="w-full text-xs text-left border-collapse">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50">
              <th class="py-2 px-3 text-slate-500 font-semibold">对比维度</th>
              ${items.map((d, i) => `<th class="py-2 px-3 font-bold ${colors[i].text}">${d.name.split(" (")[0]}</th>`).join("")}
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr>
              <td class="py-2 px-3 font-semibold text-slate-700">🏆 当前加权总分</td>
              ${items.map(d => `<td class="py-2 px-3 font-extrabold text-sm text-slate-900">${computeWeightedScore(d, state.weights).toFixed(1)} / 100</td>`).join("")}
            </tr>
            <tr>
              <td class="py-2 px-3 font-semibold text-slate-700">🌡️ 最冷月夜温 / 水温</td>
              ${items.map(d => `<td class="py-2 px-3">🌙 ${d.coldestNight}°C · 🌊 ${d.coldestWater}°C</td>`).join("")}
            </tr>
            <tr>
              <td class="py-2 px-3 font-semibold text-slate-700">💰 5晚4★海景房价</td>
              ${items.map(d => `<td class="py-2 px-3 font-bold text-slate-800">$${d.priceMin.toLocaleString()} <span class="block text-[10px] font-normal text-slate-500">${d.priceDisplay}</span></td>`).join("")}
            </tr>
            ${Object.entries(DIM_LABELS).map(([k, meta]) => `
              <tr>
                <td class="py-1.5 px-3 text-slate-600">${meta.icon} ${meta.name} (满分${meta.max})</td>
                ${items.map(d => `<td class="py-1.5 px-3 font-semibold text-slate-800">${d.scores[k]} / ${meta.max}</td>`).join("")}
              </tr>
            `).join("")}
            <tr>
              <td class="py-2 px-3 font-semibold text-slate-700">📅 最佳季节</td>
              ${items.map(d => `<td class="py-2 px-3 text-slate-600">${d.bestSeason}</td>`).join("")}
            </tr>
            <tr>
              <td class="py-2 px-3 font-semibold text-slate-700">🔗 预订验证</td>
              ${items.map(d => `<td class="py-2 px-3"><a href="${d.hotelUrl}" target="_blank" class="text-sky-600 hover:underline font-medium">查看实时房价 ↗</a></td>`).join("")}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;

  modal.classList.remove("hidden");
};

window.closeCompareModal = function() {
  const modal = document.getElementById("compare-modal");
  if (modal) modal.classList.add("hidden");
};

function buildRadarChartSVG(items, colors) {
  const size = 280;
  const cx = size / 2;
  const cy = size / 2;
  const radius = 98;
  const keys = Object.keys(MAX_SCORES);
  const n = keys.length;

  const angleFor = (i) => (Math.PI * 2 * i) / n - Math.PI / 2;
  const pointFor = (i, ratio) => {
    const a = angleFor(i);
    const r = radius * ratio;
    return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  };

  // Grid rings
  const rings = [0.25, 0.5, 0.75, 1.0].map(r => {
    const pts = keys.map((_, i) => pointFor(i, r).join(",")).join(" ");
    return `<polygon points="${pts}" fill="none" stroke="#e2e8f0" stroke-width="1" />`;
  }).join("");

  // Axes & labels
  const axes = keys.map((k, i) => {
    const [x, y] = pointFor(i, 1.0);
    const [lx, ly] = pointFor(i, 1.22);
    return `
      <line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="#cbd5e1" stroke-width="1" />
      <text x="${lx}" y="${ly}" text-anchor="middle" dominant-baseline="middle" class="text-[10px] fill-slate-600 font-semibold">
        ${DIM_LABELS[k].name}
      </text>
    `;
  }).join("");

  // Data polygons
  const polygons = items.map((d, idx) => {
    const pts = keys.map((k, i) => {
      const ratio = Math.min(1, d.scores[k] / MAX_SCORES[k]);
      return pointFor(i, ratio).join(",");
    }).join(" ");
    const c = colors[idx % colors.length];
    return `<polygon points="${pts}" fill="${c.fill}" stroke="${c.stroke}" stroke-width="2.2" />`;
  }).join("");

  return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" class="overflow-visible">${rings}${axes}${polygons}</svg>`;
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
  document.getElementById("price-slider-label").textContent = "不限 ($7,000+)";
  document.getElementById("filter-water-temp").value = "0";
  document.getElementById("filter-verified").checked = false;
  document.getElementById("filter-search").value = "";
  document.getElementById("filter-sort").value = "score-desc";

  applyPreset("default");
};

// Initialize Event Listeners on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  renderWeightSliders();
  renderEliminatedSection();
  renderApp();

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
    const label = document.getElementById("price-slider-label");
    if (label) {
      label.textContent = state.maxPrice >= 7000 ? "不限 ($7,000+)" : `≤ $${state.maxPrice.toLocaleString()}`;
    }
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
    renderApp();
  });

  document.getElementById("filter-sort")?.addEventListener("change", e => {
    state.sortBy = e.target.value;
    renderApp();
  });

  document.getElementById("btn-view-table")?.addEventListener("click", () => {
    state.viewMode = "table";
    document.getElementById("btn-view-table").className = "px-3 py-1.5 rounded-lg text-xs font-semibold bg-sky-600 text-white";
    document.getElementById("btn-view-cards").className = "px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 text-slate-600 hover:bg-slate-200";
    renderApp();
  });

  document.getElementById("btn-view-cards")?.addEventListener("click", () => {
    state.viewMode = "cards";
    document.getElementById("btn-view-cards").className = "px-3 py-1.5 rounded-lg text-xs font-semibold bg-sky-600 text-white";
    document.getElementById("btn-view-table").className = "px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 text-slate-600 hover:bg-slate-200";
    renderApp();
  });
});

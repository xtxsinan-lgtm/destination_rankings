/**
 * Destination Atlas — Universal Shared Widgets (shared_widgets.js)
 * Provides:
 * 1. LocalStorage Wishlist (❤️ 想去) & Visited Tracker (✅ 去过) + Shareable Poster Generator
 * 2. Universal Departure City Selector & Haversine Flight Time Estimator (✈️ 距你约 Xh)
 * 3. Cross-Ranking "Nearby Within 100km" Discovery (🧭 周边100km顺路玩)
 * 4. Data Verification Badge & One-Click Feedback Modal
 */
(function () {
  "use strict";

  var STORAGE_WISH = "atlas_wishlist_v1";
  var STORAGE_VISIT = "atlas_visited_v1";
  var STORAGE_ORIGIN = "atlas_origin_v1";

  var ORIGINS = [
    { name: "上海", lat: 31.23, lon: 121.47 },
    { name: "北京", lat: 39.90, lon: 116.40 },
    { name: "广州/深圳", lat: 22.80, lon: 113.60 },
    { name: "香港", lat: 22.32, lon: 114.17 },
    { name: "成都", lat: 30.57, lon: 104.06 },
    { name: "台北", lat: 25.03, lon: 121.56 },
    { name: "东京", lat: 35.68, lon: 139.76 },
    { name: "新加坡", lat: 1.35, lon: 103.82 },
    { name: "伦敦", lat: 51.51, lon: -0.13 },
    { name: "纽约", lat: 40.71, lon: -74.01 },
    { name: "洛杉矶", lat: 34.05, lon: -118.24 },
    { name: "悉尼", lat: -33.87, lon: 151.21 }
  ];

  function loadMap(key) {
    try { return JSON.parse(localStorage.getItem(key) || "{}"); } catch (e) { return {}; }
  }
  function saveMap(key, obj) {
    try { localStorage.setItem(key, JSON.stringify(obj)); } catch (e) {}
  }

  var wishMap = loadMap(STORAGE_WISH);
  var visitMap = loadMap(STORAGE_VISIT);
  var currentOriginName = "上海";
  try {
    var savedOrig = localStorage.getItem(STORAGE_ORIGIN);
    if (savedOrig) currentOriginName = savedOrig;
  } catch (e) {}

  function getOrigin() {
    for (var i = 0; i < ORIGINS.length; i++) {
      if (ORIGINS[i].name === currentOriginName) return ORIGINS[i];
    }
    return ORIGINS[0];
  }

  function haversineKm(lat1, lon1, lat2, lon2) {
    var R = 6371;
    var dLat = (lat2 - lat1) * Math.PI / 180;
    var dLon = (lon2 - lon1) * Math.PI / 180;
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  }

  function estimateFlightHours(km) {
    if (km < 80) return "同城/1h车程";
    if (km < 300) return "约 " + Math.max(1, Math.round(km / 90)) + "h 车程/高铁";
    var hrs = km / 780 + 0.6;
    return "✈️ 约 " + hrs.toFixed(1) + "h 航程";
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // Inject CSS for shared widgets
  function injectStyles() {
    if (document.getElementById("atlas-shared-css")) return;
    var st = document.createElement("style");
    st.id = "atlas-shared-css";
    st.textContent = [
      ".sw-bar{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;margin-top:8px;padding-top:8px;border-top:1px dashed rgba(150,165,180,0.2);font-size:12px;line-height:1.4}",
      ".sw-btn{display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border-radius:999px;border:1px solid rgba(150,165,180,0.35);background:rgba(128,128,128,0.08);color:inherit;font-size:11.5px;cursor:pointer;transition:all .18s}",
      ".sw-btn:hover{border-color:#f5b301;transform:translateY(-1px)}",
      ".sw-btn.is-wish{background:rgba(224,103,74,0.18);border-color:#e0674a;color:#ff8b70;font-weight:600}",
      ".sw-btn.is-visit{background:rgba(63,185,80,0.18);border-color:#3fb950;color:#56d364;font-weight:600}",
      ".sw-dist{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:6px;background:rgba(88,166,255,0.1);color:inherit;opacity:0.86;font-size:11.5px}",
      ".sw-nearby{width:100%;display:flex;flex-wrap:wrap;align-items:center;gap:5px;margin-top:4px;font-size:11.5px;opacity:0.9}",
      ".sw-nearby-label{opacity:0.7;font-weight:500}",
      ".sw-near-pill{display:inline-flex;align-items:center;gap:3px;padding:2px 8px;border-radius:999px;background:rgba(245,179,1,0.12);border:1px solid rgba(245,179,1,0.32);font-size:11px;transition:all .15s}",
      ".sw-near-pill:hover{background:rgba(245,179,1,0.25);transform:translateY(-1px)}",
      ".sw-dock{position:fixed;right:18px;bottom:18px;z-index:90;display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;background:rgba(13,17,23,0.92);color:#f0f6fc;border:1px solid rgba(255,255,255,0.18);box-shadow:0 16px 36px rgba(0,0,0,0.55);backdrop-filter:blur(12px);font-family:system-ui,-apple-system,sans-serif;font-size:12.5px}",
      ".sw-dock select{background:rgba(255,255,255,0.1);color:#fff;border:1px solid rgba(255,255,255,0.2);border-radius:999px;padding:3px 8px;font-size:12px;cursor:pointer;outline:none}",
      ".sw-dock select option{background:#161c24;color:#fff}",
      ".sw-dock-btn{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:999px;background:linear-gradient(135deg,#f5b301,#e0674a);color:#111;font-weight:600;font-size:12px;cursor:pointer;border:0}",
      ".sw-modal-bg{position:fixed;inset:0;z-index:120;background:rgba(4,8,14,0.82);backdrop-filter:blur(8px);display:none; place-items:center;padding:20px}",
      ".sw-modal-bg.open{display:grid}",
      ".sw-modal{width:min(760px,100%);max-height:88vh;overflow-y:auto;background:#121720;color:#f0f6fc;border:1px solid rgba(255,255,255,0.16);border-radius:20px;padding:24px;font-family:system-ui,-apple-system,sans-serif;box-shadow:0 30px 70px rgba(0,0,0,0.75)}",
      ".sw-modal-head{display:flex;justify-content:space-between;align-items:center;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.1)}",
      ".sw-modal-head h3{margin:0;font-size:19px}",
      ".sw-close{color:#8b949e;font-size:20px;cursor:pointer;background:none;border:0;padding:4px 8px}",
      ".sw-tabs{display:flex;gap:8px;margin:14px 0}",
      ".sw-tab{padding:6px 14px;border-radius:999px;border:1px solid rgba(255,255,255,0.15);background:transparent;color:#8b949e;font-size:13px;cursor:pointer}",
      ".sw-tab.active{background:#f5b301;color:#111;border-color:#f5b301;font-weight:600}",
      ".sw-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-top:12px}",
      ".sw-card{padding:10px 12px;border-radius:10px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.09);display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:13px}",
      ".sw-card a{color:#f0f6fc;text-decoration:none;font-weight:500}",
      ".sw-card small{display:block;color:#8b949e;font-size:11px;margin-top:2px}",
      ".sw-del{color:#8b949e;cursor:pointer;background:none;border:0;font-size:14px}",
      ".sw-poster-wrap{margin-top:18px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.1);text-align:center}",
      ".sw-poster-wrap canvas{max-width:100%;height:auto;border-radius:12px;border:1px solid rgba(255,255,255,0.15);margin-top:12px}",
      "@media(max-width:640px){.sw-dock{left:12px;right:12px;bottom:10px;justify-content:space-between}}"
    ].join("\n");
    document.head.appendChild(st);
  }

  // Collect all points across loaded datasets
  var allPoints = [];
  function rebuildAllPoints() {
    var pts = [];
    var geo = window.DEST_GEO || {};
    (window.DESTINATIONS_DATA || []).forEach(function (d) {
      var g = geo[d.id];
      if (g) pts.push({ id: d.id, name: d.name.replace(/\s*\(.*?\)/, ""), cat: "🏖️ 海岸", url: "beaches.html", lat: g[0], lon: g[1] });
    });
    (window.AQUARIUMS_TOP35 || []).forEach(function (a) {
      if (a.lat != null) pts.push({ id: a.id || ("aq-" + a.rank), name: a.name.replace(/\s*\(.*?\)/, ""), cat: "🐋 水族馆", url: "aquariums.html", lat: a.lat, lon: a.lon });
    });
    (window.ZOOS_TOP30 || []).forEach(function (z) {
      if (z.lat != null) pts.push({ id: z.id || ("zoo-" + z.rank), name: z.name.replace(/\s*\(.*?\)/, ""), cat: "🦁 动物园", url: "zoos.html", lat: z.lat, lon: z.lon });
    });
    (window.US_SAFARI_PARKS_TOP10 || []).forEach(function (s) {
      if (s.lat != null) pts.push({ id: s.id || ("safari-" + s.rank), name: s.name, cat: "🚙 游猎园", url: "zoos.html#safari", lat: s.lat, lon: s.lon });
    });
    (window.INDUSTRIAL_MUSEUMS_TOP100 || []).forEach(function (m) {
      if (m.lat != null) pts.push({ id: m.id || ("mus-" + m.rank), name: m.name.replace(/\s*[（(].*?[)）]/, ""), cat: "⚙️ 重器馆", url: "museums.html", lat: m.lat, lon: m.lon });
    });
    (window.THEMEPARKS_TOP100 || []).forEach(function (p) {
      if (p.lat != null) pts.push({ id: p.id || ("tp-" + p.rank), name: p.name.replace(/\s*\(.*?\)/, ""), cat: "🎢 游乐园", url: "themeparks.html", lat: p.lat, lon: p.lon });
    });
    (window.SKI_RESORTS_TOP100 || []).forEach(function (s) {
      if (s.lat != null) pts.push({ id: s.id || ("ski-" + s.rank), name: s.name.replace(/\s*\(.*?\)/, ""), cat: "🎿 雪场", url: "ski.html", lat: s.lat, lon: s.lon });
    });
    (window.SHOWS_TOP50 || []).forEach(function (s) {
      if (s.lat != null) pts.push({ id: s.id || ("show-" + s.rank), name: s.name.replace(/\s*\(.*?\)/, ""), cat: "🎭 驻场秀", url: "shows.html", lat: s.lat, lon: s.lon });
    });
    (window.CANAL_ROUTES_TOP20 || []).forEach(function (c) {
      if (c.lat != null) pts.push({ id: "canal-" + c.id, name: c.name, cat: "⚜️ 运河房船", url: "canals.html#route-" + c.id, lat: c.lat, lon: c.lon });
    });
    (window.SAILING_ROUTES_TOP20 || []).forEach(function (s) {
      var nm = typeof s.name === "string" ? s.name : ((s.name && s.name.zh) || s.id);
      if (s.lat != null) pts.push({ id: "sail-" + s.id, name: String(nm).replace(/\s*\(.*?\)/, ""), cat: "⛵ 帆船航线", url: "sailing.html#r-" + s.id, lat: s.lat, lon: s.lon });
    });
    (window.RV_ROUTES_TOP20 || []).forEach(function (r) {
      if (r.lat != null) pts.push({ id: r.id, name: r.name, cat: "🚐 房车路线", url: "rv.html#" + r.id, lat: r.lat, lon: r.lon });
    });
    allPoints = pts;
  }

  function findNearby(id, lat, lon) {
    if (!lat && !lon) return [];
    var res = [];
    for (var i = 0; i < allPoints.length; i++) {
      var p = allPoints[i];
      if (p.id === id) continue;
      var d = haversineKm(lat, lon, p.lat, p.lon);
      if (d <= 105) {
        res.push({ p: p, km: Math.round(d) });
      }
    }
    res.sort(function (a, b) { return a.km - b.km; });
    return res.slice(0, 3);
  }

  function enhance() {
    injectStyles();
    rebuildAllPoints();
    var orig = getOrigin();
    var cards = document.querySelectorAll("[data-dest-id]");
    cards.forEach(function (el) {
      var id = el.getAttribute("data-dest-id");
      var lat = parseFloat(el.getAttribute("data-lat"));
      var lon = parseFloat(el.getAttribute("data-lon"));
      var name = el.getAttribute("data-name") || id;
      var slot = el.querySelector(".shared-slot");
      if (!slot) {
        slot = document.createElement("div");
        slot.className = "shared-slot";
        el.appendChild(slot);
      }
      var isW = !!wishMap[id];
      var isV = !!visitMap[id];
      var distHtml = "";
      var nearHtml = "";
      if (!isNaN(lat) && !isNaN(lon)) {
        var km = haversineKm(orig.lat, orig.lon, lat, lon);
        distHtml = '<span class="sw-dist" title="从' + esc(orig.name) + '出发直线距离约 ' + Math.round(km) + ' km">' + esc(orig.name) + '出发 ' + estimateFlightHours(km) + '</span>';
        var nears = findNearby(id, lat, lon);
        if (nears.length) {
          nearHtml = '<div class="sw-nearby"><span class="sw-nearby-label">🧭 周边100km顺路玩：</span>' +
            nears.map(function (n) {
              return '<a class="sw-near-pill" href="' + esc(n.p.url) + '" title="距离约 ' + n.km + ' km">' + esc(n.p.cat + " " + n.p.name) + " (" + (n.km < 5 ? "同城" : n.km + "km") + ")</a>";
            }).join("") + '</div>';
        }
      }
      slot.innerHTML =
        '<div class="sw-bar">' +
          '<button type="button" class="sw-btn' + (isW ? " is-wish" : "") + '" data-act="wish" data-id="' + esc(id) + '" data-name="' + esc(name) + '">' + (isW ? "❤️ 已在心愿单" : "🤍 想去") + '</button>' +
          '<button type="button" class="sw-btn' + (isV ? " is-visit" : "") + '" data-act="visit" data-id="' + esc(id) + '" data-name="' + esc(name) + '">' + (isV ? "✅ 已去过" : "⬜ 打卡去过") + '</button>' +
          distHtml +
          nearHtml +
        '</div>';
    });
    updateDockCount();
  }

  // Event delegation for wish/visit clicks
  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".sw-btn[data-act]");
    if (!btn) return;
    e.stopPropagation();
    var act = btn.getAttribute("data-act");
    var id = btn.getAttribute("data-id");
    var name = btn.getAttribute("data-name");
    var page = location.pathname.split("/").pop() || "index.html";
    if (act === "wish") {
      if (wishMap[id]) delete wishMap[id];
      else wishMap[id] = { id: id, name: name, page: page, t: Date.now() };
      saveMap(STORAGE_WISH, wishMap);
    } else if (act === "visit") {
      if (visitMap[id]) delete visitMap[id];
      else visitMap[id] = { id: id, name: name, page: page, t: Date.now() };
      saveMap(STORAGE_VISIT, visitMap);
    }
    enhance();
  });

  // Floating Dock & Modal
  var dockEl, modalBgEl, activeTab = "visit";
  function createDock() {
    if (document.getElementById("sw-dock")) return;
    injectStyles();
    dockEl = document.createElement("div");
    dockEl.id = "sw-dock";
    dockEl.className = "sw-dock";
    dockEl.innerHTML =
      '<span>🛫 出发地:</span>' +
      '<select id="sw-origin-sel" aria-label="选择出发城市">' +
        ORIGINS.map(function (o) {
          return '<option value="' + esc(o.name) + '"' + (o.name === currentOriginName ? " selected" : "") + '>' + esc(o.name) + '</option>';
        }).join("") +
      '</select>' +
      '<button type="button" class="sw-dock-btn" id="sw-open-modal">🎒 我的足迹 (<span id="sw-cnt">0</span>)</button>';
    document.body.appendChild(dockEl);

    modalBgEl = document.createElement("div");
    modalBgEl.className = "sw-modal-bg";
    modalBgEl.innerHTML =
      '<div class="sw-modal" role="dialog" aria-modal="true" aria-label="我的全球旅行足迹与心愿单">' +
        '<div class="sw-modal-head">' +
          '<h3>🎒 我的全球目的地足迹 & 心愿单</h3>' +
          '<button type="button" class="sw-close" id="sw-close-modal">✕</button>' +
        '</div>' +
        '<div class="sw-tabs">' +
          '<button type="button" class="sw-tab active" data-t="visit">✅ 已去过打卡 (<span id="sw-v-cnt">0</span>)</button>' +
          '<button type="button" class="sw-tab" data-t="wish">❤️ 想去心愿单 (<span id="sw-w-cnt">0</span>)</button>' +
          '<button type="button" class="sw-tab" data-t="poster">✨ 生成分享海报</button>' +
        '</div>' +
        '<div id="sw-modal-body"></div>' +
      '</div>';
    document.body.appendChild(modalBgEl);

    document.getElementById("sw-origin-sel").addEventListener("change", function (ev) {
      currentOriginName = ev.target.value;
      try { localStorage.setItem(STORAGE_ORIGIN, currentOriginName); } catch (e) {}
      enhance();
      if (window.onAtlasOriginChange) window.onAtlasOriginChange(getOrigin());
    });
    document.getElementById("sw-open-modal").addEventListener("click", function () {
      modalBgEl.classList.add("open");
      renderModalBody();
    });
    document.getElementById("sw-close-modal").addEventListener("click", function () {
      modalBgEl.classList.remove("open");
    });
    modalBgEl.addEventListener("click", function (ev) {
      if (ev.target === modalBgEl) modalBgEl.classList.remove("open");
    });
    modalBgEl.querySelectorAll(".sw-tab").forEach(function (tb) {
      tb.addEventListener("click", function () {
        activeTab = tb.getAttribute("data-t");
        modalBgEl.querySelectorAll(".sw-tab").forEach(function (x) { x.classList.toggle("active", x === tb); });
        renderModalBody();
      });
    });
  }

  function updateDockCount() {
    createDock();
    var vKeys = Object.keys(visitMap), wKeys = Object.keys(wishMap);
    var cntEl = document.getElementById("sw-cnt");
    if (cntEl) cntEl.textContent = vKeys.length + "去过 · " + wKeys.length + "想去";
    var vEl = document.getElementById("sw-v-cnt"), wEl = document.getElementById("sw-w-cnt");
    if (vEl) vEl.textContent = vKeys.length;
    if (wEl) wEl.textContent = wKeys.length;
  }

  function renderModalBody() {
    updateDockCount();
    var body = document.getElementById("sw-modal-body");
    if (!body) return;
    if (activeTab === "poster") {
      body.innerHTML =
        '<div class="sw-poster-wrap">' +
          '<p style="color:#8b949e;font-size:13.5px;margin:0 0 10px">基于你打卡的目的地自动生成专属长图海报，右键或长按图片即可保存分享到小红书/朋友圈：</p>' +
          '<button type="button" class="sw-dock-btn" id="sw-dl-poster">📥 下载高清 PNG 海报</button><br/>' +
          '<canvas id="sw-canvas" width="720" height="920"></canvas>' +
        '</div>';
      drawPoster();
      document.getElementById("sw-dl-poster").addEventListener("click", function () {
        var cv = document.getElementById("sw-canvas");
        var a = document.createElement("a");
        a.download = "destination-atlas-footprint.png";
        a.href = cv.toDataURL("image/png");
        a.click();
      });
      return;
    }
    var map = activeTab === "visit" ? visitMap : wishMap;
    var items = Object.keys(map).map(function (k) { return map[k]; });
    if (!items.length) {
      body.innerHTML = '<p style="padding:40px 0;text-align:center;color:#8b949e">还没有记录，浏览任意榜单卡片时点击「🤍 想去」或「⬜ 打卡去过」即可收入此处（保存在浏览器本地，无需注册登录）。</p>';
      return;
    }
    body.innerHTML = '<div class="sw-list">' + items.map(function (it) {
      return '<div class="sw-card">' +
        '<div><a href="' + esc(it.page || "index.html") + '">' + esc(it.name) + '</a><small>' + esc(it.page || "") + '</small></div>' +
        '<button type="button" class="sw-del" data-del="' + esc(it.id) + '" title="移除">✕</button>' +
      '</div>';
    }).join("") + '</div>';
    body.querySelectorAll("[data-del]").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-del");
        if (activeTab === "visit") { delete visitMap[id]; saveMap(STORAGE_VISIT, visitMap); }
        else { delete wishMap[id]; saveMap(STORAGE_WISH, wishMap); }
        renderModalBody();
        enhance();
      });
    });
  }

  function drawPoster() {
    var cv = document.getElementById("sw-canvas");
    if (!cv) return;
    var ctx = cv.getContext("2d");
    var grad = ctx.createLinearGradient(0, 0, 720, 920);
    grad.addColorStop(0, "#0b1320");
    grad.addColorStop(0.5, "#111b2a");
    grad.addColorStop(1, "#090d14");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 720, 920);

    // Border frame
    ctx.strokeStyle = "rgba(245, 179, 1, 0.45)";
    ctx.lineWidth = 2;
    ctx.strokeRect(28, 28, 664, 864);

    // Header
    ctx.fillStyle = "#f5b301";
    ctx.font = "600 15px sans-serif";
    ctx.fillText("DESTINATION ATLAS · 全球硬核目的地旅行成绩单", 56, 78);

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 36px sans-serif";
    var vList = Object.keys(visitMap).map(function (k) { return visitMap[k]; });
    var wList = Object.keys(wishMap).map(function (k) { return wishMap[k]; });
    ctx.fillText("我已解锁全球 " + vList.length + " 处标杆目的地", 56, 130);

    ctx.fillStyle = "#8b949e";
    ctx.font = "18px sans-serif";
    ctx.fillText("心愿单待解锁：" + wList.length + " 处  |  常驻出发地：" + currentOriginName, 56, 166);

    // Stats boxes
    var boxes = [
      { label: "✅ 已打卡去过", val: vList.length + " 处", c: "#3fb950" },
      { label: "❤️ 心愿单想去", val: wList.length + " 处", c: "#e0674a" },
      { label: "🌍 全站收录总量", val: "570 处", c: "#5ef2e6" }
    ];
    boxes.forEach(function (b, i) {
      var bx = 56 + i * 208, by = 196;
      ctx.fillStyle = "rgba(255,255,255,0.05)";
      ctx.fillRect(bx, by, 192, 92);
      ctx.strokeStyle = "rgba(255,255,255,0.12)";
      ctx.strokeRect(bx, by, 192, 92);
      ctx.fillStyle = "#8b949e";
      ctx.font = "14px sans-serif";
      ctx.fillText(b.label, bx + 16, by + 32);
      ctx.fillStyle = b.c;
      ctx.font = "bold 28px sans-serif";
      ctx.fillText(b.val, bx + 16, by + 70);
    });

    // List of visited / wishlisted
    ctx.fillStyle = "#f5b301";
    ctx.font = "bold 18px sans-serif";
    ctx.fillText("📌 我的代表足迹与心愿清单：", 56, 336);

    var combined = vList.map(function (x) { return "✅ " + x.name; }).concat(wList.map(function (x) { return "❤️ " + x.name; }));
    if (!combined.length) combined = ["🌟 正在探索 Destination Atlas 七大全球硬核榜单..."];
    ctx.fillStyle = "#e6edf3";
    ctx.font = "16px sans-serif";
    combined.slice(0, 18).forEach(function (txt, idx) {
      var col = idx % 2;
      var row = Math.floor(idx / 2);
      var x = 56 + col * 310;
      var y = 376 + row * 44;
      ctx.fillStyle = "rgba(255,255,255,0.04)";
      ctx.fillRect(x, y - 24, 294, 34);
      ctx.fillStyle = "#f0f6fc";
      ctx.fillText(txt.slice(0, 17), x + 10, y - 2);
    });

    // Footer
    ctx.fillStyle = "#8b949e";
    ctx.font = "14px sans-serif";
    ctx.fillText("涵盖：145 海岸 · 35 水族馆 · 40 动物园 · 100 重器馆 · 100 游乐园 · 100 雪场 · 50 驻场秀", 56, 845);
    ctx.fillStyle = "#f5b301";
    ctx.fillText("Destination Atlas · 2026 硬核旅行图鉴", 56, 870);
  }

  // Lazy-load other data scripts in idle time so cross-ranking 100km discovery works everywhere
  function lazyLoadCrossData() {
    var scripts = [
      { check: "DEST_GEO", src: "geo.js" },
      { check: "DESTINATIONS_DATA", src: "data.js" },
      { check: "AQUARIUMS_TOP35", src: "data_aquariums_zoos_museums.js" },
      { check: "THEMEPARKS_TOP100", src: "data_themeparks.js" },
      { check: "SKI_RESORTS_TOP100", src: "data_ski.js" },
      { check: "SHOWS_TOP50", src: "data_shows.js" },
      { check: "CANAL_ROUTES_TOP20", src: "data_canals_top20.js" },
      { check: "SAILING_ROUTES_TOP20", src: "data_sailing_top20.js" },
      { check: "RV_ROUTES_TOP20", src: "data_rv_top20.js" }
    ];
    var loadedAny = false;
    var pending = 0;
    scripts.forEach(function (s) {
      if (window[s.check]) return;
      pending++;
      var el = document.createElement("script");
      el.src = s.src;
      el.async = true;
      el.onload = function () {
        loadedAny = true;
        pending--;
        if (pending <= 0 && loadedAny) enhance();
      };
      el.onerror = function () {
        pending--;
      };
      document.body.appendChild(el);
    });
  }

  window.SharedWidgets = {
    enhance: enhance,
    getOrigin: getOrigin,
    haversineKm: haversineKm
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      createDock();
      enhance();
      setTimeout(lazyLoadCrossData, 600);
    });
  } else {
    createDock();
    enhance();
    setTimeout(lazyLoadCrossData, 600);
  }
})();

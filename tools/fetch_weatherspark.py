#!/usr/bin/env python3
"""
Scrape 365-day daily weather statistics from WeatherSpark for all 145 beach destinations:
- Daily average high temperature (°C, 365 days)
- Daily average low temperature (°C, 365 days)
- Daily average water temperature + 10th/90th percentile low & high water temperature (°C, 365 days)
- Daily clearer/sunny sky percentage (%, 365 days)
- Daily precipitation / wet day probability (%, 365 days)
"""
import json
import math
import os
import re
import subprocess
import time
from playwright.sync_api import sync_playwright

# Load 145 destinations and geo
LOADER_JS = """
var window = {};
ObjC.import("Foundation");
["data.js", "data_part2.js", "geo.js"].forEach(function(f) {
  var s = $.NSString.alloc.initWithContentsOfFileEncodingError(f, $.NSUTF8StringEncoding, null).js;
  eval(s);
});
JSON.stringify(window.DESTINATIONS_DATA.map(function(d) {
  return {id: d.id, name: d.name, coldestNight: d.coldestNight, coldestWater: d.coldestWater, geo: window.DEST_GEO[d.id]};
}));
"""
out = subprocess.check_output(["osascript", "-l", "JavaScript", "-e", LOADER_JS])
DESTS = json.loads(out.decode("utf-8"))

SEARCH_QUERIES = {
    "bora-bora": ["Bora-Bora", "Vaitape"],
    "moorea": ["Afareaitu", "Moorea", "Papeete"],
    "seychelles-praslin-ladigue": ["Victoria", "Praslin"],
    "maui": ["Lahaina", "Kihei", "Kahului", "Wailea"],
    "mauritius": ["Grand Baie", "Port Louis", "Mahebourg"],
    "usvi": ["Charlotte Amalie", "Cruz Bay", "Christiansted"],
    "bvi": ["Road Town", "Spanish Town"],
    "kauai": ["Lihue", "Kapaa", "Poipu"],
    "cancun": ["Cancún", "Cancun", "Isla Mujeres"],
    "tahaa-huahine": ["Uturoa", "Fare", "Bora-Bora"],
    "st-barts": ["Gustavia"],
    "st-lucia": ["Castries", "Vieux Fort", "Soufrière"],
    "turks-caicos": ["Providenciales", "Cockburn Town", "Five Cays"],
    "seychelles-mahe": ["Victoria"],
    "maldives-resorts": ["Male", "Malé"],
    "krabi-phiphi": ["Krabi", "Ao Nang", "Phuket"],
    "aitutaki": ["Aitutaki", "Arutanga", "Avarua"],
    "oahu-waikiki": ["Honolulu", "Waikiki", "Kailua"],
    "seychelles-outer": ["Victoria"],
    "guadeloupe": ["Pointe-à-Pitre", "Le Gosier", "Sainte-Anne", "Basse-Terre"],
    "martinique": ["Fort-de-France", "Le Lamentin", "Sainte-Anne"],
    "anguilla": ["The Valley", "Anguilla"],
    "grand-cayman": ["George Town", "West Bay"],
    "fiji-yasawa": ["Lautoka", "Nadi", "Ba"],
    "fiji-mamanuca": ["Nadi", "Lautoka"],
    "big-island": ["Kailua-Kona", "Hilo"],
    "tulum-cozumel": ["San Miguel de Cozumel", "Cozumel", "Tulum", "Playa del Carmen"],
    "aruba": ["Oranjestad", "Noord", "Sint Nicolaas"],
    "fernando-de-noronha": ["Fernando de Noronha", "Natal"],
    "el-nido": ["El Nido", "Taytay", "Coron", "Puerto Princesa"],
    "phuket": ["Phuket", "Patong", "Kathu"],
    "curacao": ["Willemstad", "Sint Michiel"],
    "antigua": ["Saint John’s", "Saint John's", "All Saints", "Liberta"],
    "boracay": ["Malay", "Boracay", "Kalibo", "Ibajay"],
    "fiji-taveuni-savusavu": ["Labasa", "Savusavu", "Suva"],
    "komodo": ["Labuan Bajo", "Ruteng", "Bima"],
    "tobago-cays": ["Kingstown", "Port Elizabeth"],
    "st-maarten": ["Philipsburg", "Marigot", "Simpson Bay", "Cul de Sac"],
    "barbados": ["Bridgetown", "Speightstown", "Oistins"],
    "bohol": ["Tagbilaran City", "Panglao"],
    "sanya": ["Sanya", "Lingshui"],
    "samana": ["Samaná", "Santa Bárbara de Samaná", "ánchez", "Las Terrenas", "Nagua"],
    "raja-ampat": ["Sorong", "Manokwari"],
    "saipan": ["Saipan", "Garapan", "Capitol Hill"],
    "lombok-gili": ["Mataram", "Praya", "Senggigi", "Tanjung"],
    "manuel-antonio": ["Quepos", "Parrita", "Jacó", "Puntarenas"],
    "negril": ["Savanna-la-Mar", "Negril", "Lucea", "Montego Bay"],
    "vanuatu": ["Luganville", "Port-Vila", "Port Vila"],
    "koh-kood": ["Trat", "Ko Chang", "Laem Ngop"],
    "st-kitts-nevis": ["Basseterre", "Charlestown"],
    "palau": ["Koror", "Koror Town", "Melekeok"],
    "coron": ["Coron", "Busuanga", "Culion"],
    "culebra-vieques": ["Culebra", "Vieques", "Fajardo", "Ceiba"],
    "koh-samui": ["Ko Samui", "Koh Samui", "Nathon", "Surat Thani"],
    "papagayo": ["Liberia", "Sardinal", "Tamarindo", "Santa Cruz"],
    "grenada": ["Saint George's", "St. George's", "Gouyave"],
    "belize": ["San Pedro", "Belize City"],
    "samoa": ["Apia", "Vaitele"],
    "guam": ["Tamuning", "Hagåtña", "Dededo", "Guam"],
    "roatan": ["Roatán", "Roatan", "Coxen Hole", "Guanaja"],
    "siargao": ["Dapa", "General Luna", "Surigao", "Del Carmen"],
    "koh-lipe": ["Satun", "La-ngu", "Kuah", "Langkawi"],
    "san-andres": ["San Andrés", "San Andres"],
    "la-romana": ["La Romana", "San Rafael del Yuma", "Higüey"],
    "koh-tao-phangan": ["Ko Samui", "Ko Pha Ngan", "Ko Tao", "Chumphon"],
    "tobago": ["Scarborough", "Crown Point", "Roxborough"],
    "san-blas": ["El Porvenir", "Colón", "Cartí", "Nombre de Dios"],
    "zanzibar": ["Zanzibar", "Nungwi", "Chake Chake"],
    "diani-beach": ["Gazi", "Ukunda", "Mombasa", "Kwale"],
    "bali": ["Denpasar", "Kuta", "Jimbaran", "Nusa Dua"],
    "bonaire": ["Kralendijk", "Dorp Rincon", "Willemstad"],
    "maragogi": ["Maragogi", "Tamandaré", "Maceió", "Barreiros"],
    "redang-perhentian": ["Kuala Terengganu", "Jertih", "Kuala Besut", "Kota Bharu"],
    "similan-khaolak": ["Takua Pa", "Thai Mueang", "Phang Nga", "Phuket"],
    "kota-kinabalu": ["Kota Kinabalu", "Putatan"],
    "montego-bay": ["Montego Bay", "Falmouth", "Ocho Rios"],
    "jericoacoara": ["Acaraú", "Jijoca de Jericoacoara", "Camocim"],
    "langkawi": ["Kuah", "Langkawi", "Padang Matsirat"],
    "bocas-del-toro": ["Bocas del Toro", "Changuinola"],
    "huatulco": ["Crucecita", "Santa María Huatulco", "Puerto Escondido", "San Pedro Pochutla"],
    "morro-boipeba": ["Valença", "Cairu", "Ituberá", "Salvador"],
    "san-juan": ["San Juan", "Carolina"],
    "nosy-be": ["Andoany", "Hell-Ville", "Nosy Be", "Ambanja"],
    "tioman": ["Mersing", "Kuala Rompin"],
    "punta-cana": ["Punta Cana", "Bávaro", "Higüey"],
    "phu-quoc": ["Dương Đông", "Phú Quốc", "Hà Tiên"],
    "da-nang": ["Da Nang", "Đà Nẵng", "Hội An"],
    "bintan": ["Tanjung Pinang", "Kijang", "Batam", "Singapore"],
    "cebu": ["Lapu-Lapu City", "Cebu City", "Mandaue City", "Moalboal"],
    "manado": ["Manado", "Bitung", "Tomohon"],
    "puerto-plata": ["Puerto Plata", "San Felipe de Puerto Plata", "Sosúa"],
    "sri-lanka-east": ["Trincomalee", "Batticaloa", "Kalmunai"],
    "hua-hin": ["Hua Hin", "Cha-am", "Pran Buri"],
    "maldives-local": ["Male", "Malé", "Maafushi"],
    "semporna": ["Semporna", "Tawau", "Kunak", "Lahad Datu"],
    "salalah": ["Salalah", "Taqah", "Mirbat"],
    "fiji-main": ["Nadi", "Lautoka", "Suva"],
    "nha-trang": ["Nha Trang", "Cam Ranh", "Ninh Hòa"],
    "sri-lanka-sw": ["Galle", "Bentota", "Hikkaduwa", "Matara"],
    "pattaya": ["Pattaya", "Phatthaya", "Sattahip", "Si Racha"],
    "whitsundays": ["Airlie Beach", "Proserpine", "Bowen", "Mackay"],
    "mallorca": ["Palma", "Palma de Mallorca", "Alcúdia", "Manacor"],
    "sardinia": ["Olbia", "La Maddalena", "Arzachena", "Sassari"],
    "ibiza-formentera": ["Ibiza", "Santa Eulària des Riu", "Sant Antoni de Portmany"],
    "crete": ["Chania", "Rethymno", "Heraklion", "Kissamos"],
    "zakynthos-kefalonia": ["Zákynthos", "Zakynthos", "Argostoli", "Lixouri"],
    "miyakojima": ["Miyakojima", "Hirara"],
    "exuma-harbour": ["George Town", "Dunmore Town", "Rock Sound", "Nassau"],
    "ningaloo": ["Exmouth", "Carnarvon"],
    "corsica": ["Porto-Vecchio", "Bonifacio", "Sartène", "Ajaccio"],
    "rarotonga": ["Avarua"],
    "milos-santorini": ["Firá", "Thira", "Mílos", "Mykonos", "Naxos"],
    "bermuda": ["Hamilton", "Saint George"],
    "ishigaki": ["Ishigaki"],
    "nassau": ["Nassau"],
    "okinawa-main": ["Naha", "Okinawa", "Nago", "Chatan"],
    "saadiyat-dubai": ["Abu Dhabi", "Dubai"],
    "cairns-port-douglas": ["Port Douglas", "Cairns", "Mossman"],
    "bazaruto": ["Vilankulo", "Inhassoro", "Inhambane"],
    "rio-ilha-grande": ["Rio de Janeiro", "Angra dos Reis", "Mangaratiba"],
    "algarve": ["Lagos", "Portimão", "Albufeira", "Faro"],
    "amalfi-capri": ["Amalfi", "Sorrento", "Capri", "Salerno", "Naples"],
    "sharm-marsa-alam": ["Sharm el-Sheikh", "Dahab", "Hurghada"],
    "clearwater-siesta": ["Clearwater", "St. Petersburg", "Sarasota", "Bradenton"],
    "wanning": ["Wanning", "Qionghai", "Lingshui", "Sanya"],
    "hvar-brac": ["Hvar", "Supetar", "Makarska", "Split"],
    "fethiye-kas": ["Fethiye", "Kaş", "Dalaman", "Kalkan"],
    "miami-beach": ["Miami Beach", "Miami"],
    "french-riviera": ["Nice", "Antibes", "Cannes", "Saint-Tropez"],
    "hurghada-el-gouna": ["Hurghada", "Safaga"],
    "destin": ["Destin", "Fort Walton Beach", "Miramar Beach"],
    "la-paz-balandra": ["La Paz"],
    "kotor-budva": ["Budva", "Kotor", "Tivat", "Herceg Novi"],
    "ayia-napa": ["Ayia Napa", "Paralimni", "Protaras", "Larnaca"],
    "los-cabos": ["Cabo San Lucas", "San José del Cabo"],
    "gold-coast": ["Gold Coast", "Surfers Paradise", "Tweed Heads", "Byron Bay"],
    "rottnest-perth": ["Perth", "Fremantle", "Rockingham"],
    "canary-islands": ["Maspalomas", "Las Palmas de Gran Canaria", " Mogán", "Arona", "Adeje"],
    "pvr": ["Puerto Vallarta", "Bucerías"],
    "varadero": ["Varadero", "Cárdenas", "Matanzas"],
    "malta-comino": ["Valletta", "San Pawl il-Baħar", "Mellieħa", "Victoria"],
    "sydney-beaches": ["Sydney", "Manly", "Bondi"],
    "cape-town": ["Cape Town"],
    "jeju": ["Jeju City", "Seogwipo"],
    "weizhou-djerba": ["Beihai", "Zhanjiang", "Haikou"]
}

def extract_iso(name):
    cps = list(name.strip())
    if len(cps) >= 2:
        c0, c1 = ord(cps[0]), ord(cps[1])
        if 0x1F1E6 <= c0 <= 0x1F1FF and 0x1F1E6 <= c1 <= 0x1F1FF:
            return chr(c0 - 0x1F1E6 + 65) + chr(c1 - 0x1F1E6 + 65)
    return ""

ISO_EQUIV = {
    "VI": {"VI", "US"},
    "PR": {"PR", "US"},
    "MP": {"MP", "US"},
    "GU": {"GU", "US"},
    "BL": {"BL", "FR", "GP", "MF", "SX"},
    "SX": {"SX", "MF", "NL", "FR", "GP"},
    "GP": {"GP", "FR"},
    "MQ": {"MQ", "FR"},
    "BQ": {"BQ", "NL", "CW", "AW"},
    "CW": {"CW", "NL"},
    "AW": {"AW", "NL"},
    "KY": {"KY", "GB", "UK"},
    "VG": {"VG", "GB", "UK", "VI"},
    "TC": {"TC", "GB", "UK"},
    "AI": {"AI", "GB", "UK", "SX", "MF"},
    "BM": {"BM", "GB", "UK"},
    "CK": {"CK", "NZ"},
}

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def parse_svg_ticks(svg):
    lines = [float(m.group(1)) for m in re.finditer(r'<line y1="([\d.]+)" x1="72" y2="[\d.]+" x2="681"', svg)]
    texts = [(float(m.group(1)), m.group(2).strip()) for m in re.finditer(r'<text text-anchor="end" x="71" y="([\d.]+)">([^<]+)</text>', svg)]
    pairs = []
    for yt, label in texts:
        val_m = re.search(r"(-?[\d.]+)", label)
        if not val_m:
            continue
        val = float(val_m.group(1))
        is_f = "°F" in label
        if lines:
            yl = min(lines, key=lambda l: abs((yt - 5.2) - l))
            if abs((yt - 5.2) - yl) > 2.0:
                yl = yt - 5.2
        else:
            yl = yt - 5.2
        pairs.append((yl, val, is_f))
    if len(pairs) < 2:
        return None
    y0, v0, is_f = pairs[0]
    y1, v1, _ = pairs[-1]
    if abs(y1 - y0) < 1e-6:
        return None
    a = (v1 - v0) / (y1 - y0)
    b = v0 - a * y0
    return a, b, is_f

def decode_path_y(d_str):
    pts = re.findall(r"([Ml])(-?\d+),(-?\d+)", d_str)
    ys = []
    cx, cy = 0, 0
    for cmd, dx, dy in pts:
        if cmd == "M":
            cx, cy = int(dx), int(dy)
        else:
            cx += int(dx)
            cy += int(dy)
        ys.append(cy / 10.0)
    return ys

def to_c(vals, is_f):
    if is_f:
        return [round((v - 32.0) * 5.0 / 9.0, 1) for v in vals]
    return [round(v, 1) for v in vals]

def parse_weatherspark_html(html):
    out = {}
    t_m = re.search(r"<title>(.*?)</title>", html, re.S)
    out["title"] = t_m.group(1).strip() if t_m else ""

    coord_m = re.search(r"geographical coordinates of .*? are (-?[\d.]+) deg latitude,\s*(-?[\d.]+) deg longitude", html)
    if coord_m:
        out["lat"] = float(coord_m.group(1))
        out["lon"] = float(coord_m.group(2))

    # 1. Figures-Temperature
    idx = html.find('id="Figures-Temperature"')
    if idx != -1:
        svg_m = re.search(r"<svg.*?</svg>", html[idx:idx+120000], re.S)
        if svg_m:
            svg = svg_m.group(0)
            ticks = parse_svg_ticks(svg)
            if ticks:
                a, b, is_f = ticks
                for m in re.finditer(r"<path([^>]*)>", svg):
                    attrs = m.group(1)
                    if "stroke-dasharray" in attrs:
                        continue
                    d_m = re.search(r'd="([^"]+)"', attrs)
                    if not d_m:
                        continue
                    ys = decode_path_y(d_m.group(1))
                    if len(ys) == 365 and 'fill="none"' in attrs:
                        vals = to_c([a * y + b for y in ys], is_f)
                        if "#4646b9" in attrs:
                            out["low"] = vals
                        elif "#ba4545" in attrs:
                            out["high"] = vals

    # 2. Figures-CloudCover
    idx = html.find('id="Figures-CloudCover"')
    if idx != -1:
        svg_m = re.search(r"<svg.*?</svg>", html[idx:idx+120000], re.S)
        if svg_m:
            svg = svg_m.group(0)
            ticks = parse_svg_ticks(svg)
            if ticks:
                a, b, _ = ticks
                for m in re.finditer(r"<path([^>]*)>", svg):
                    attrs = m.group(1)
                    d_m = re.search(r'd="([^"]+)"', attrs)
                    if not d_m:
                        continue
                    ys = decode_path_y(d_m.group(1))
                    if len(ys) == 365 and 'fill="none"' in attrs:
                        out["clear"] = [round(max(0.0, min(100.0, a * y + b)), 1) for y in ys]

    # 3. Figures-PrecipitationProbability
    idx = html.find('id="Figures-PrecipitationProbability"')
    if idx != -1:
        svg_m = re.search(r"<svg.*?</svg>", html[idx:idx+120000], re.S)
        if svg_m:
            svg = svg_m.group(0)
            ticks = parse_svg_ticks(svg)
            if ticks:
                a, b, _ = ticks
                for m in re.finditer(r"<path([^>]*)>", svg):
                    attrs = m.group(1)
                    d_m = re.search(r'd="([^"]+)"', attrs)
                    if not d_m:
                        continue
                    ys = decode_path_y(d_m.group(1))
                    if len(ys) == 365 and 'fill="none"' in attrs:
                        out["rain"] = [round(max(0.0, min(100.0, a * y + b)), 1) for y in ys]

    # 4. Figures-WaterTemperature
    idx = html.find('id="Figures-WaterTemperature"')
    if idx != -1:
        svg_m = re.search(r"<svg.*?</svg>", html[idx:idx+120000], re.S)
        if svg_m:
            svg = svg_m.group(0)
            ticks = parse_svg_ticks(svg)
            if ticks:
                a, b, is_f = ticks
                band_idx = 0
                for m in re.finditer(r"<path([^>]*)>", svg):
                    attrs = m.group(1)
                    d_m = re.search(r'd="([^"]+)"', attrs)
                    if not d_m:
                        continue
                    ys = decode_path_y(d_m.group(1))
                    if len(ys) == 730:
                        low_ys = ys[:365]
                        high_ys = list(reversed(ys[365:]))
                        if band_idx == 0:
                            out["waterLow10"] = to_c([a * y + b for y in low_ys], is_f)
                            out["waterHigh90"] = to_c([a * y + b for y in high_ys], is_f)
                        elif band_idx == 1:
                            out["waterLow25"] = to_c([a * y + b for y in low_ys], is_f)
                            out["waterHigh75"] = to_c([a * y + b for y in high_ys], is_f)
                        band_idx += 1
                    elif len(ys) == 365 and 'fill="none"' in attrs:
                        out["water"] = to_c([a * y + b for y in ys], is_f)

    return out

def refresh_waf(page):
    print("  [WAF] Refreshing AWS WAF token...")
    for attempt in range(3):
        try:
            page.goto("https://weatherspark.com/y/149048/x", timeout=30000)
            page.wait_for_selector("h1", timeout=20000)
            time.sleep(0.5)
            return
        except Exception as e:
            print(f"  [WAF] Retry {attempt+1}: {e}")
            time.sleep(2.0)

def safe_search(page, q):
    for _ in range(3):
        res = page.evaluate(
            """async (q) => {
                try {
                    const r = await fetch(`/search?q=${encodeURIComponent(q)}&ic=true&p=0`, {
                        headers: {"X-Requested-With": "XMLHttpRequest"}
                    });
                    if (r.status === 202 || r.status === 403 || r.status === 429) return {waf: true, status: r.status};
                    if (r.status !== 200) return {error: r.status};
                    const text = await r.text();
                    if (!text || text.includes("awsWafCookieDomainList")) return {waf: true};
                    return JSON.parse(text);
                } catch (e) {
                    return {waf: true, err: String(e)};
                }
            }""",
            q
        )
        if res and res.get("waf"):
            refresh_waf(page)
            continue
        return res
    return None

def safe_fetch_report(page, ws_id):
    for _ in range(3):
        res = page.evaluate(
            """async (ws_id) => {
                try {
                    const r = await fetch(`/y/${ws_id}/x`);
                    if (r.status === 202 || r.status === 403 || r.status === 429) return {waf: true, status: r.status};
                    if (r.status !== 200) return {error: r.status};
                    const html = await r.text();
                    if (!html || html.length < 5000 || html.includes("awsWafCookieDomainList")) return {waf: true};
                    return {url: r.url, html: html};
                } catch (e) {
                    return {waf: true, err: String(e)};
                }
            }""",
            ws_id
        )
        if res and res.get("waf"):
            refresh_waf(page)
            continue
        return res
    return None

def main():
    cache_path = os.path.join(os.path.dirname(__file__), "weatherspark_raw.json")
    existing = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                raw_ex = json.load(f)
            # Clean out any bad matches (dist > 260km or missing water)
            for k, v in raw_ex.items():
                if (
                    all( key in v for key in ("high", "low", "clear", "rain", "water") )
                    and v.get("dist_km", 999) <= 260.0
                ):
                    existing[k] = v
        except Exception:
            existing = {}

    print(f"Loaded {len(existing)} valid cached destinations.")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.route(
            "**/*",
            lambda route: route.abort()
            if any(
                x in route.request.url
                for x in [
                    "doubleclick", "googlesyndication", "googletagmanager",
                    "pubmatic", "criteo", "anonymised", "bydata", "panxo",
                    "idsequoia", "confiant", "crwdcntrl", "imganalytics", "fundingchoices"
                ]
            )
            else route.continue_()
        )

        refresh_waf(page)

        for idx, d in enumerate(DESTS, start=1):
            did = d["id"]
            if did in existing:
                print(f"[{idx:3d}/145] {did:26s} -> CACHED WS#{existing[did]['ws_id']} {existing[did]['ws_name'][:35]} (dist={existing[did]['dist_km']}km)")
                continue

            iso = extract_iso(d["name"])
            valid_isos = ISO_EQUIV.get(iso, {iso})
            target_lat, target_lon = d["geo"]
            queries = SEARCH_QUERIES.get(did, [did.replace("-", " ")])

            candidates = []
            seen_ws_ids = set()
            for q in queries:
                res_json = safe_search(page, q)
                if not res_json or "results" not in res_json:
                    continue
                for item in res_json["results"]:
                    m_id = re.search(r"/y/(\d+)/", item.get("url", ""))
                    if not m_id:
                        continue
                    ws_id = m_id.group(1)
                    if ws_id in seen_ws_ids:
                        continue
                    seen_ws_ids.add(ws_id)
                    cc = item.get("countryCode", "")
                    loc_type = item.get("reportLocationTypeCode", 0)
                    full_name = item.get("fullNameTr", "")
                    is_airport = "Airport" in full_name or loc_type == 1
                    iso_match = cc in valid_isos
                    if not iso_match:
                        continue
                    candidates.append({
                        "ws_id": ws_id,
                        "cc": cc,
                        "iso_match": iso_match,
                        "is_airport": is_airport,
                        "full_name": full_name
                    })

            candidates.sort(key=lambda c: c["is_airport"])

            best_parsed = None
            best_dist = 999999.0

            for cand in candidates[:6]:
                ws_id = cand["ws_id"]
                resp = safe_fetch_report(page, ws_id)
                if not resp or not resp.get("html"):
                    continue
                parsed = parse_weatherspark_html(resp["html"])
                parsed["ws_id"] = ws_id
                parsed["ws_url"] = resp["url"]
                parsed["ws_name"] = cand["full_name"]
                parsed["cc"] = cand["cc"]
                if "lat" in parsed and "lon" in parsed:
                    dist = haversine_km(target_lat, target_lon, parsed["lat"], parsed["lon"])
                else:
                    dist = 999.0
                parsed["dist_km"] = round(dist, 1)

                has_all = all(k in parsed for k in ("high", "low", "clear", "rain", "water"))
                if has_all and dist <= 180.0:
                    best_parsed = parsed
                    best_dist = dist
                    break
                if dist <= 300.0:
                    score_curr = (0 if has_all else 500) + dist
                    score_best = (0 if (best_parsed and all(k in best_parsed for k in ("high", "low", "clear", "rain", "water"))) else 500) + best_dist
                    if score_curr < score_best:
                        best_parsed = parsed
                        best_dist = dist

            if best_parsed:
                existing[did] = best_parsed
                has_water = "water" in best_parsed
                print(
                    f"[{idx:3d}/145] {did:26s} -> WS#{best_parsed['ws_id']} {best_parsed['ws_name'][:38]:38s} "
                    f"(dist={best_parsed['dist_km']}km, water={has_water})"
                )
            else:
                print(f"[{idx:3d}/145] {did:26s} -> FAILED TO MATCH (candidates={len(candidates)})")

            if idx % 5 == 0:
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(existing, f, ensure_ascii=False)

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False)
        browser.close()
        print(f"Done! Total matched: {len(existing)}/145. Saved to {cache_path}")

if __name__ == "__main__":
    main()

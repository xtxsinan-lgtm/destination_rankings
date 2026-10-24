#!/usr/bin/env python3
"""Fetch real Wikimedia Commons photos for canal routes whose images were missing/hallucinated,
save them locally under rankings/images/canals/, and rewrite data_canals_top20.js in place.

- Rank 11 (Rideau) itinerary referenced non-existent canada_rideau_1..6.jpg -> r11_d{day}_{n}.jpg
- Ranks 12-20 covers referenced non-existent local files / 404 Wikimedia URLs -> r{rank}_cover.jpg
- Also adds approximate base-port lat/lon to every route (for shared_widgets.js).
Usage: python3 tools/fetch_canal_images.py
"""
import hashlib, json, os, re, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data_canals_top20.js")
IMG_DIR = os.path.join(ROOT, "rankings/images/canals")
UA = {"User-Agent": "DestinationAtlasCoverBot/1.1 (https://xtxsinan-lgtm.github.io/destination_rankings/)"}
BAD = re.compile(r"map|flag|coat|logo|locator|diagram|stamp|satellite|chart|plan|svg|poster|menu|sign|ticket|document|icon|portrait|statue|plaque|drawing|engraving|postcard|watercolou?r|painting|sketch|aquarelle|snow|winter|insect|mayfly|ephem|1[89]\d\d", re.I)

RIDEAU = {
    1: ["Smiths Falls Rideau Canal", "Poonamalie lock Rideau"],
    2: ["Merrickville lock Rideau", "Merrickville blockhouse"],
    3: ["Big Rideau Lake", "Westport Ontario", "Rideau Lakes Ontario boat"],
    4: ["Newboro lock Rideau", "Chaffeys Lock Rideau"],
    5: ["Jones Falls lock Rideau", "Jones Falls dam Rideau Canal"],
    6: ["Seeleys Bay Rideau", "Beveridges Locks Tay"],
    7: ["Perth Ontario Tay Basin", "Perth Ontario Stewart Park"],
    8: ["Smiths Falls lock Rideau Canal", "Ottawa Locks Rideau Canal Parliament"],
}
COVERS = {
    12: ["Charente river Cognac boat", "Charente Jarnac river", "Charente river Saintes"],
    13: ["Pont-canal de Briare Loire", "Briare aqueduct canal boat", "Canal latéral à la Loire Briare"],
    14: ["Lockport Erie Canal locks", "Erie Canal lock boat"],
    15: ["River Shannon cruiser boat", "Carrick-on-Shannon river", "River Shannon"],
    16: ["Rheinsberg Schloss Grienericksee", "Mecklenburgische Seenplatte Hausboot", "Müritz Sommer Boot"],
    17: ["Kennet and Avon Canal Bath narrowboat", "Dundas Aqueduct canal", "Kennet and Avon Canal"],
    18: ["Aigues-Mortes canal boat", "Aigues-Mortes remparts canal", "Camargue flamants roses"],
    19: ["Murray River houseboat", "Murray River cliffs South Australia"],
    20: ["Kerala backwaters houseboat", "Alappuzha houseboat"],
}
COORDS = {  # approx. base port
    1: (43.268, 2.719), 2: (48.736, 7.247), 3: (52.970, -3.170), 4: (57.145, -4.680),
    5: (45.440, 12.330), 6: (51.484, -0.604), 7: (52.090, 5.121), 8: (44.447, 1.441),
    9: (51.054, 3.725), 10: (47.213, 4.874), 11: (44.904, -76.020), 12: (45.696, -0.329),
    13: (47.640, 2.739), 14: (43.170, -78.690), 15: (53.946, -8.090), 16: (53.430, 12.700),
    17: (51.381, -2.359), 18: (43.567, 4.191), 19: (-34.430, 139.620), 20: (9.498, 76.338),
}


def api(query):
    q = urllib.parse.urlencode({
        "action": "query", "generator": "search", "gsrnamespace": 6, "gsrsearch": query + " filetype:bitmap",
        "gsrlimit": 12, "prop": "imageinfo", "iiprop": "url|size|mime", "iiurlwidth": 1280, "format": "json"})
    req = urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    pages = sorted((data.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    out = []
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("mime") != "image/jpeg" or BAD.search(p["title"]):
            continue
        w, h = ii.get("width", 0), ii.get("height", 0)
        if w < 1000 or w < h:
            continue
        out.append(ii.get("thumburl") or ii["url"])
    return out


HASHES = set()


def download(url, dest):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                blob = r.read()
            if len(blob) > 20000:
                h = hashlib.md5(blob).hexdigest()
                if h in HASHES:  # identical photo already used elsewhere
                    return False
                HASHES.add(h)
                open(dest, "wb").write(blob)
                return True
            return False
        except Exception as e:  # 429 etc.
            print("   retry", attempt, e)
            time.sleep(4 + attempt * 4)
    return False


def fetch(queries, dest, used):
    if os.path.exists(dest) and os.path.getsize(dest) > 20000:
        return True
    for q in queries:
        try:
            cands = api(q)
        except Exception as e:
            print("  api fail", q, e); time.sleep(3); continue
        for u in cands:
            if u in used:
                continue
            if download(u, dest):
                used.add(u); print("  ok", os.path.basename(dest), "<-", q, u[-70:]); time.sleep(1.5)
                return True
        time.sleep(1)
    print("  FAILED", dest)
    return False


def main():
    src = open(DATA, encoding="utf-8").read()
    b = src.index("window.CANAL_BOAT_TIERS_DB")
    routes = json.loads(src[src.index("["):b].strip().rstrip(";"))
    tail = src[b:]
    used = set()
    for fn in os.listdir(IMG_DIR):
        if fn.endswith(".jpg"):
            HASHES.add(hashlib.md5(open(os.path.join(IMG_DIR, fn), "rb").read()).hexdigest())
    for r in routes:
        rank = r["rank"]
        lat, lon = COORDS[rank]
        r["lat"], r["lon"] = lat, lon
        if rank == 11:
            for d in r["itinerary8Days"]:
                for i, p in enumerate(d["photos"][:2]):
                    qs = RIDEAU[d["day"]]
                    order = qs[i:] + qs[:i]
                    fn = f"r11_d{d['day']}_{i+1}.jpg"
                    if fetch(order, os.path.join(IMG_DIR, fn), used):
                        p["src"] = "rankings/images/canals/" + fn
            r["coverImage"] = "rankings/images/canals/r11_d5_1.jpg"
        if rank in COVERS:
            fn = f"r{rank}_cover.jpg"
            if fetch(COVERS[rank], os.path.join(IMG_DIR, fn), used):
                r["coverImage"] = "rankings/images/canals/" + fn
    head = "// Auto-generated Global Top 20 Canal & Waterway Houseboat Routes\nwindow.CANAL_ROUTES_TOP20 = "
    open(DATA, "w", encoding="utf-8").write(head + json.dumps(routes, ensure_ascii=False, indent=2) + ";\n\n" + tail)
    print("data updated")


if __name__ == "__main__":
    main()

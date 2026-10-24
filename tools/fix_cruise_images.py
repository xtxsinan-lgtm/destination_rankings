#!/usr/bin/env python3
"""Fix data_cruises_top50.js: replace hallucinated/404 Wikimedia cover URLs with real Commons photos
(searched per ship -> sister ship / brand -> relevant scenery fallback) and add base-port lat/lon.

Usage: python3 tools/fix_cruise_images.py            # search + write
       python3 tools/fix_cruise_images.py --dry      # print picks only
"""
import json, re, sys, time, urllib.parse, urllib.request, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data_cruises_top50.js")
UA = {"User-Agent": "DestinationAtlasCoverBot/1.1 (https://xtxsinan-lgtm.github.io/destination_rankings/)"}
BAD = re.compile(r"map|flag|coat|logo|locator|diagram|stamp|chart|plan\b|\.svg|\.tif|\.pdf|poster|menu|ticket|document|icon of|portrait|plaque|model|drawing|interior|cabin|crew|deck plan", re.I)

# id -> (queries in order of preference, (lat, lon) of base port / start point)
Q = {
    "seabourn-ovation": (["Seabourn Ovation", "Seabourn Encore", "Seabourn ship"], (41.90, 12.50)),
    "silversea-silver-nova": (["Silver Nova ship", "Silver Ray ship", "Silversea Silver Dawn"], (37.94, 23.64)),
    "regent-seven-seas-grandeur": (["Seven Seas Grandeur", "Seven Seas Splendor", "Seven Seas Explorer"], (41.38, 2.18)),
    "explora-i-ii": (["Explora I ship", "Explora I", "Explora Journeys"], (43.70, 7.27)),
    "ponant-commandant-charcot": (["Le Commandant Charcot", "Commandant Charcot icebreaker"], (78.22, 15.65)),
    "ritz-carlton-ilma": (["Evrima yacht", "Ritz-Carlton Yacht Collection Evrima", "Ilma ship"], (43.55, 7.02)),
    "four-seasons-i-yacht": (["Four Seasons I yacht", "Superyacht Mediterranean harbour"], (18.03, -63.05)),
    "orient-express-corinthian": (["Orient Express Corinthian", "Silenseas sailing", "Portofino harbour"], (43.12, 6.36)),
    "aman-at-sea-sama": (["Bonifacio harbour", "Bonifacio port"], (41.39, 9.16)),
    "scenic-eclipse-ii": (["Scenic Eclipse II", "Scenic Eclipse ship"], (-54.80, -68.30)),
    "crystal-serenity": (["Crystal Serenity", "Crystal Symphony"], (25.77, -80.17)),
    "guntu-setouchi": (["guntû ship", "Guntu Setouchi", "Onomichi Seto Inland Sea"], (34.40, 133.20)),
    "paul-gauguin-tahiti": (["Paul Gauguin cruise ship", "m/s Paul Gauguin", "Bora Bora lagoon"], (-17.54, -149.57)),
    "oceania-vista-allura": (["Oceania Vista ship", "Oceania Allura", "Oceania Marina ship"], (41.38, 2.18)),
    "azamara-onward": (["Azamara Onward", "Azamara Quest", "Azamara Journey"], (45.44, 12.32)),
    "windstar-star-pride": (["Star Pride ship", "Windstar Star Pride", "Wind Surf ship"], (18.47, -66.11)),
    "cunard-qm2-queens-grill": (["Queen Mary 2", "Queen Mary 2 ship"], (50.90, -1.40)),
    "asuka-iii-japan": (["Asuka III ship", "飛鳥III", "Asuka II ship Yokohama"], (35.45, 139.65)),
    "mitsui-ocean-fuji": (["Mitsui Ocean Fuji", "Seabourn Sojourn", "Seabourn Odyssey"], (35.45, 139.65)),
    "rci-icon-loft-townhouse": (["Icon of the Seas", "Star of the Seas Royal Caribbean"], (25.78, -80.17)),
    "celebrity-ascent-edge-villa": (["Celebrity Beyond", "Celebrity Ascent", "Celebrity Edge ship"], (43.30, 5.37)),
    "rci-oasis-quantum-star-loft": (["Symphony of the Seas", "Ovation of the Seas", "Oasis of the Seas"], (26.09, -80.12)),
    "msc-yacht-club-duplex": (["MSC World Europa", "MSC Meraviglia", "MSC World America"], (25.29, 51.53)),
    "ncl-haven-duplex-aqua": (["Norwegian Prima ship", "Norwegian Viva", "Norwegian Aqua ship"], (25.78, -80.17)),
    "disney-treasure-wish-tower": (["Disney Wish ship", "Disney Treasure ship", "Disney Wish"], (28.41, -80.62)),
    "virgin-voyages-rockstar": (["Scarlet Lady ship", "Valiant Lady ship", "Virgin Voyages"], (25.78, -80.17)),
    "yangzi-explorer-2025": (["Yangzi Explorer", "Qutang Gorge", "Three Gorges Yangtze cruise ship"], (29.56, 106.58)),
    "riverside-mozart-danube": (["Riverside Mozart", "Crystal Mozart river ship", "Wachau Danube river cruise"], (48.21, 16.37)),
    "amamagna-danube": (["AmaMagna", "AmaWaterways river ship", "Dürnstein Danube"], (48.62, 12.97)),
    "uniworld-la-venezia": (["S.S. La Venezia", "Uniworld river ship", "Venice lagoon Giudecca canal"], (45.43, 12.33)),
    "oberoi-zahra-philae-nile": (["Oberoi Philae Nile", "Oberoi Zahra", "Nile cruise ship Aswan"], (25.69, 32.64)),
    "ak-sanctuary-nile-seray": (["Sanctuary Sun Boat", "Sun Boat IV Nile", "Nile cruise boat Luxor"], (25.69, 32.64)),
    "historia-nile-boutique": (["Nile cruise ship Kom Ombo", "Kom Ombo temple Nile", "Nile cruise boat"], (25.69, 32.64)),
    "belmond-afloat-in-france": ([], (47.02, 4.84)),
    "aria-amazon-delfin-i": (["Aria Amazon", "Delfin Amazon cruise", "Amazon river Peru Iquitos boat"], (-3.75, -73.25)),
    "zambezi-queen-chobe": (["Zambezi Queen", "Chobe River boat", "Chobe River elephants"], (-17.80, 25.15)),
    "viking-longships-rhine-danube": (["Viking longship river cruise", "Viking River Cruises Rhine", "Viking River Cruises ship"], (47.56, 7.59)),
    "century-oasis-yangtze-3": (["Century Legend cruise Yangtze", "Yangtze River cruise ship", "Three Gorges Dam"], (29.56, 106.58)),
    "aqua-mekong-vietnam-cambodia": (["Aqua Mekong", "Mekong river cruise ship", "Mekong Phnom Penh boat"], (11.56, 104.93)),
    "viking-mississippi-usa": (["Viking Mississippi", "Mississippi riverboat New Orleans", "American Queen steamboat"], (29.95, -90.06)),
    "aman-amandira-indonesia": (["Amandira", "Phinisi Komodo", "Pinisi Labuan Bajo"], (-8.50, 119.88)),
    "alila-purnama-indonesia": (["Alila Purnama", "Phinisi Raja Ampat", "Pinisi Raja Ampat"], (-0.88, 131.25)),
    "galapagos-hermes-mega-catamaran": (["Galapagos catamaran", "Kicker Rock Galapagos", "León Dormido"], (-0.90, -89.61)),
    "galapagos-grace-yacht": (["M/Y Grace Galapagos", "Galapagos yacht", "Gardner Bay Española"], (-0.74, -90.31)),
    "silversea-silver-origin": (["Silver Origin ship", "Silversea Silver Origin", "Bartolomé Galápagos"], (-0.90, -89.61)),
    "galapagos-cormorant-ii-elite": (["Galapagos Elite catamaran", "Galapagos cruise catamaran", "Marine iguana Galapagos"], (-0.90, -89.61)),
    "galapagos-infinity-yacht": (["Galapagos cruise yacht", "Blue-footed booby Galapagos"], (-0.74, -90.31)),
    "galapagos-eco-galaxy-catamaran": (["Galapagos catamaran Santa Cruz", "Galapagos giant tortoise Santa Cruz"], (-0.74, -90.31)),
    "galapagos-cachalote-explorer": (["Cachalote Explorer", "Galapagos schooner", "Galapagos penguin Isabela"], (-0.95, -90.97)),
    "aqua-blu-indonesia-spice-islands": (["Aqua Blu yacht", "Banda Neira", "Gunung Api Banda"], (-4.52, 129.90)),
}


def http_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def search(q):
    url = ("https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrlimit=10"
           "&prop=imageinfo&iiprop=url|size|mime&iiurlwidth=1280&format=json&gsrsearch=" + urllib.parse.quote(q))
    try:
        d = http_json(url)
    except Exception as e:
        print("  ! search failed", q, e)
        return []
    pages = sorted((d.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    out = []
    for p in pages:
        t = p.get("title", "")
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("mime") not in ("image/jpeg", "image/png", "image/webp"):
            continue
        if BAD.search(t):
            continue
        if ii.get("width", 0) < 900 or ii.get("width", 0) < ii.get("height", 1):  # landscape, decent size
            continue
        out.append((t, ii.get("thumburl") or ii.get("url")))
    return out


def head_ok(url):
    try:
        req = urllib.request.Request(url, headers=UA, method="GET")
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status == 200 and r.headers.get("Content-Type", "").startswith("image")
    except Exception:
        return False


def main():
    dry = "--dry" in sys.argv
    src = open(DATA, encoding="utf-8").read()
    a = src.index("[", src.index("LUXURY_CRUISES_TOP50"))
    b = src.index("\n];", a) + 2
    arr = json.loads(src[a:b + 1].rstrip(";").rstrip())
    used = set()
    for c in arr:
        qs, (lat, lon) = Q[c["id"]]
        c["lat"], c["lon"] = lat, lon
        img = c.get("image", "")
        if img.startswith("rankings/"):
            print(f"{c['rank']:>2} keep local {img}")
            continue
        if img.startswith("http") and "/commons/thumb/" in img and head_ok(img) and img not in used and c.get("_imgOk"):
            used.add(img)
            continue
        pick = None
        for q in qs:
            for t, u in search(q):
                if u in used:
                    continue
                if head_ok(u):
                    pick = (q, t, u)
                    break
                time.sleep(0.3)
            if pick:
                break
            time.sleep(0.4)
        if pick:
            used.add(pick[2])
            c["image"] = pick[2]
            c["imageCredit"] = pick[1].replace("File:", "")
            print(f"{c['rank']:>2} {c['id']:<36} [{pick[0]}] -> {pick[1]}")
        else:
            print(f"{c['rank']:>2} {c['id']:<36} !! NO PICK")
        time.sleep(0.3)
    if dry:
        return
    body = json.dumps(arr, ensure_ascii=False, indent=2)
    new = src[:a] + body + src[b:]
    open(DATA, "w", encoding="utf-8").write(new)
    print("written", DATA)


if __name__ == "__main__":
    main()

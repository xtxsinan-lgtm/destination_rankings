"""Repair sailing photos: verify each Wikimedia file via Commons API (batch imageinfo); keep real ones (as 1280px thumburl),
replace missing/hallucinated ones with real Commons search results for the place.
Usage: python3 tools/fix_sailing_images.py [--dry]"""
import json, re, sys, time, urllib.parse, urllib.request, os
sys.path.insert(0, os.path.dirname(__file__))
from sailing_data_io import load, save
from sailing_check_images import collect

UA = {"User-Agent": "DestinationAtlasCoverBot/1.1 (https://xtxsinan-lgtm.github.io/destination_rankings/)"}
API = "https://commons.wikimedia.org/w/api.php?"
BAD = re.compile(r"map|flag|coat|logo|locator|diagram|stamp|satellite|landsat|sentinel|chart|plan\b|svg|poster|menu|sign|ticket|document|icon|portrait|statue|plaque|stub|book|page", re.I)
CACHE_P = os.path.join(os.path.dirname(__file__), "sailing_image_cache.json")
cache = json.load(open(CACHE_P)) if os.path.exists(CACHE_P) else {}


def get(params):
    url = API + urllib.parse.urlencode(params)
    for a in range(5):
        try:
            time.sleep(0.4)
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(3 * (a + 1)); continue
            raise
    return {}


def title_from_url(u):
    u = urllib.parse.unquote(u)
    m = re.search(r"/commons/(?:thumb/)?[0-9a-f]/[0-9a-f]{2}/([^/?]+)", u)
    return ("File:" + m.group(1).replace("_", " ")) if m else None


def batch_info(titles):
    out = {}
    titles = list(dict.fromkeys(t for t in titles if t))
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        d = get({"action": "query", "format": "json", "titles": "|".join(chunk), "prop": "imageinfo",
                 "iiprop": "url|size|mime", "iiurlwidth": 1280})
        q = d.get("query", {})
        norm = {n["to"]: n["from"] for n in q.get("normalized", [])}
        for p in q.get("pages", {}).values():
            t = norm.get(p["title"], p["title"])
            if "missing" in p or not p.get("imageinfo"):
                out[t] = None
            else:
                ii = p["imageinfo"][0]
                out[t] = ii.get("thumburl") or ii.get("url")
    return out


def search(q, exclude=()):
    key = "S:" + q
    if key in cache:
        res = cache[key]
    else:
        d = get({"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
                 "gsrsearch": f"{q} filetype:bitmap", "gsrlimit": 20, "prop": "imageinfo",
                 "iiprop": "url|size|mime", "iiurlwidth": 1280})
        pages = sorted((d.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
        res = []
        for p in pages:
            ii = (p.get("imageinfo") or [{}])[0]
            t = p.get("title", "")
            if BAD.search(t) or ii.get("mime") not in ("image/jpeg", "image/png"):
                continue
            w, h = ii.get("width", 0), ii.get("height", 0)
            if w < 900 or not h or w / h < 1.15 or w / h > 2.6:
                continue
            res.append([t, ii.get("thumburl") or ii.get("url")])
        cache[key] = res
        json.dump(cache, open(CACHE_P, "w"), ensure_ascii=False, indent=0)
    for t, u in res:
        if u not in exclude:
            return t, u
    return None


# Search queries per photo key (route id / stop group:index) -> list of queries per photo slot
ROUTE_Q = {
    "greece-lefkada-ionian": ["Fiskardo harbour", "Kioni Ithaca"],
    "sardinia-bonifacio": ["Bonifacio cliffs", "La Maddalena archipelago"],
    "sicily-aeolian-islands": ["Stromboli island", "Lipari Marina Corta"],
    "caribbean-bvi": ["The Baths Virgin Gorda", "Jost Van Dyke White Bay"],
    "tahiti-bora-bora": ["Bora Bora lagoon Otemanu", "Taha'a lagoon"],
    "turkey-gocek-fethiye": ["Göcek bay", "Fethiye gulf"],
    "croatia-split-dalmatia": ["Hvar harbour", "Vis island Croatia"],
    "croatia-dubrovnik-korcula": ["Korčula old town", "Dubrovnik old port"],
    "seychelles-inner-islands": ["Anse Source d'Argent La Digue", "Praslin Seychelles"],
    "bahamas-exumas-cays": ["Staniel Cay Exuma", "Exuma Cays Land and Sea Park"],
    "grenadines-tobago-cays": ["Tobago Cays", "Bequia Admiralty Bay"],
    "thailand-phuket-phang-nga": ["Phang Nga Bay karst", "Phi Phi islands"],
    "australia-whitsundays-reef": ["Whitehaven Beach Hill Inlet", "Whitsunday Islands"],
    "spain-mallorca-menorca": ["Cala Macarella Menorca", "Mallorca cala"],
    "greece-saronic-gulf": ["Hydra harbour Greece", "Poros Greece harbour"],
    "italy-amalfi-pontine-islands": ["Positano", "Ponza harbour"],
    "greece-sporades-mammamia": ["Skopelos town harbour", "Skiathos harbour"],
    "usvi-st-john-national-park": ["Trunk Bay St. John", "Cruz Bay St. John"],
    "caribbean-martinique-st-lucia": ["Pitons Saint Lucia", "Martinique Sainte-Anne"],
    "belize-barrier-reef-cays": ["Belize barrier reef caye", "Caye Caulker"],
}


def stop_queries(title):
    """Derive a place query from the stop title: Latin text inside （） or ()."""
    m = re.search(r"[（(]([^（）()]*[A-Za-z][^（）()]*)[）)]", title)
    s = m.group(1) if m else title
    s = re.sub(r"\$\\rightarrow\$", "", s)
    parts = [p.strip() for p in re.split(r"\s*(?:&|—|-|,|/|\+|→)\s*", s) if p.strip() and re.search(r"[A-Za-z]", p)]
    return parts or [s]


def main(dry=False):
    d, order = load()
    items = collect(d)
    info = batch_info([title_from_url(u) for _, _, u in items])
    used = set()
    changes = []
    # pass 1: real ones
    for key, cap, u in items:
        t = title_from_url(u)
        if t and info.get(t):
            used.add(info[t])
    def setp(key, url):
        kind, *rest = key.split(":")
        if kind == "route":
            rid, i = rest
            r = next(x for x in d["SAILING_ROUTES_TOP20"] if x["id"] == rid)
            r["photos"][int(i)]["url"] = url
            for t5 in d["SAILING_TOP5_ROUTES"]:
                if t5["id"] == rid and len(t5.get("photos", [])) > int(i):
                    t5["photos"][int(i)]["url"] = url
        else:
            g, si, i = rest
            d["SAILING_ROUTE_STOPS_GALLERY"][g][int(si)]["photos"][int(i)]["url"] = url
    for key, cap, u in items:
        t = title_from_url(u)
        real = info.get(t) if t else None
        if real:
            if real != u:
                setp(key, real)
            print("KEEP", key, t)
            continue
        kind, *rest = key.split(":")
        if kind == "route":
            qs = ROUTE_Q.get(rest[0], [])
            i = int(rest[1])
            qs = qs[i:] + qs[:i]
        else:
            g, si, i = rest
            title = d["SAILING_ROUTE_STOPS_GALLERY"][g][int(si)]["title"]
            qs = stop_queries(title)
            i = int(i)
            qs = qs[i % len(qs):] + qs[:i % len(qs)]
        hit = None
        for q in qs:
            hit = search(q, used)
            if hit:
                break
        if hit:
            used.add(hit[1])
            setp(key, hit[1])
            changes.append((key, hit[0]))
            print("FIX ", key, qs, "->", hit[0])
        else:
            print("MISS", key, qs)
    if not dry:
        save(d, order)
    print("replaced", len(changes))


if __name__ == "__main__":
    main("--dry" in sys.argv)

#!/usr/bin/env python3
"""Find better Wikimedia Commons covers for theme parks / water parks whose THEMED_IMAGES entry is
missing or off-theme (construction cranes, nebulae, airports, cruise ships, gift shops ...).

Step 1 (search):  python3 tools/fetch_themepark_covers.py search  -> writes tools/themepark_cover_candidates.json
Step 2 (apply):   python3 tools/fetch_themepark_covers.py apply '{"id": idx, ...}'
                  -> writes `image: {src, page, artist, license, title}` into data_themeparks.js
themeparks.html resolves covers as: item.image -> THEMED_IMAGES[id] -> themed inline SVG placeholder.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "DestinationAtlasCoverBot/1.1 (static ranking site)"
ROOT = __file__.rsplit("/tools/", 1)[0]
CAND = ROOT + "/tools/themepark_cover_candidates.json"
QUERIES = {
    "universal-epic-universe": ["Epic Universe Stardust Racers", "Epic Universe Celestial Park", "Epic Universe Orlando 2025"],
    "europa-park": ["Europa-Park Silver Star", "Europa-Park Blue Fire", "Europa-Park Wodan"],
    "cedar-point": ["Cedar Point Millennium Force", "Cedar Point Steel Vengeance", "Cedar Point skyline coasters"],
    "disney-hollywood-studios": ["Hollywood Studios Tower of Terror", "Galaxy's Edge Millennium Falcon Hollywood Studios"],
    "shanghai-disneyland": ["Shanghai Disneyland Enchanted Storybook Castle", "Shanghai Disneyland castle"],
    "disney-animal-kingdom": ["Tree of Life Animal Kingdom", "Expedition Everest Animal Kingdom"],
    "puy-du-fou": ["Puy du Fou spectacle", "Puy du Fou Vikings", "Puy du Fou Signe du Triomphe"],
    "dollywood": ["Dollywood Lightning Rod", "Dollywood Wild Eagle", "Dollywood Thunderhead"],
    "busch-gardens-tampa": ["Busch Gardens Tampa SheiKra", "Busch Gardens Tampa Montu", "Iron Gwazi"],
    "fuji-q-highland": ["Fuji-Q Highland Fujiyama roller coaster", "Fuji-Q Highland Eejanaika", "Fuji-Q Highland Mount Fuji coaster"],
    "busch-gardens-williamsburg": ["Busch Gardens Williamsburg Griffon", "Busch Gardens Williamsburg Apollo's Chariot", "Busch Gardens Williamsburg Alpengeist"],
    "nagashima-spa-land": ["Steel Dragon 2000", "Nagashima Spa Land roller coaster"],
    "alton-towers": ["Alton Towers Nemesis", "Alton Towers Oblivion", "Alton Towers Smiler"],
    "liseberg": ["Liseberg Helix", "Liseberg Balder", "Liseberg Valkyria"],
    "warner-bros-world-abu-dhabi": ["Warner Bros. World Abu Dhabi", "Warner Bros World Yas Island"],
    "ferrari-world-abu-dhabi": ["Ferrari World Abu Dhabi roof", "Ferrari World Formula Rossa", "Ferrari World Yas Island"],
    "seaworld-orlando": ["SeaWorld Orlando Mako", "SeaWorld Orlando Manta", "SeaWorld Orlando Kraken"],
    "six-flags-great-adventure": ["Kingda Ka", "Six Flags Great Adventure El Toro", "Six Flags Great Adventure Nitro"],
    "gardaland": ["Gardaland Blue Tornado", "Gardaland Raptor", "Gardaland Oblivion"],
    "parque-warner-madrid": ["Parque Warner Madrid Superman", "Parque Warner Stunt Fall", "Parque Warner Madrid montaña rusa"],
    "xcaret-park": ["Xcaret park Mexico", "Xcaret Mexico Espectacular", "Xcaret Riviera Maya"],
    "kolmarden-wildlife-park": ["Wildfire Kolmården", "Kolmården Wildfire roller coaster", "Kolmården djurpark"],
    "six-flags-great-america": ["Six Flags Great America Goliath", "Six Flags Great America Raging Bull", "Six Flags Great America X-Flight"],
    "six-flags-over-georgia": ["Six Flags Over Georgia Goliath", "Six Flags Over Georgia Twisted Cyclone", "Six Flags Over Georgia"],
    "lagoon-park": ["Lagoon amusement park Farmington", "Lagoon Cannibal roller coaster", "Lagoon Farmington Utah roller coaster"],
    "seaworld-san-antonio": ["SeaWorld San Antonio Steel Eel", "SeaWorld San Antonio Great White", "SeaWorld San Antonio Wave Breaker"],
    "seaworld-san-diego": ["SeaWorld San Diego Manta", "SeaWorld San Diego Journey to Atlantis", "SeaWorld San Diego Electric Eel"],
    "shanghai-haichang-ocean-park": ["Shanghai Haichang Ocean Park", "Haichang Ocean Park Shanghai"],
    "fantawild-oriental-heritage": ["Fantawild Oriental Heritage", "Fantawild Adventure", "Fantawild theme park"],
    "hong-kong-ocean-park": ["Ocean Park Hong Kong Hair Raiser", "Ocean Park Hong Kong cable car", "Ocean Park Hong Kong Summit"],
    "suzuka-circuit-park": ["Suzuka Circuit Motopia", "Suzuka Circuit amusement park", "Suzuka Circuit Ferris wheel"],
    "parque-espana-shima": ["Parque España Shima", "Shima Spain Village Pyrenees coaster", "志摩スペイン村 パルケエスパーニャ"],
    "genting-skyworlds": ["Genting SkyWorlds", "Genting Highlands theme park"],
    "motiongate-dubai": ["Motiongate Dubai", "Dubai Parks and Resorts Motiongate"],
    "beto-carrero-world": ["Beto Carrero World castelo", "Beto Carrero World Fire Whip", "Beto Carrero World Penha"],
    "six-flags-mexico": ["Six Flags México Medusa", "Six Flags Mexico roller coaster", "Six Flags México"],
    "legoland-billund": ["Legoland Billund Miniland", "Legoland Billund Nyhavn", "Legoland Billund park"],
    "chessington-world-of-adventures": ["Chessington Dragon's Fury", "Chessington World of Adventures ride", "Chessington Vampire ride"],
    "aquaventure-dubai": ["Aquaventure Atlantis The Palm", "Atlantis The Palm water park Ziggurat"],
    "chimelong-water-park": ["Chimelong Water Park Guangzhou", "Chimelong Waterpark"],
    "yas-waterworld-abu-dhabi": ["Yas Waterworld", "Yas Waterworld Abu Dhabi slides"],
    "aquaventure-bahamas": ["Atlantis Paradise Island Mayan Temple slide", "Aquaventure Atlantis Bahamas", "Atlantis Paradise Island water park"],
    "beach-park-brazil": ["Beach Park Fortaleza Aquiraz", "Beach Park Insano", "Beach Park Ceará"],
    "caribbean-bay-korea": ["Caribbean Bay Everland", "Caribbean Bay Yongin water park"],
    "disney-magic-kingdom": ["Cinderella Castle Magic Kingdom", "Cinderella Castle Walt Disney World"],
    "phantasialand": ["Phantasialand Taron", "Phantasialand Black Mamba", "Phantasialand F.L.Y."],
    "disney-epcot": ["Spaceship Earth Epcot", "Epcot Spaceship Earth night"],
    "universal-studios-japan": ["Universal Studios Japan globe", "Universal Studios Japan Flying Dinosaur", "Super Nintendo World Osaka"],
    "chimelong-ocean-kingdom": ["Chimelong Ocean Kingdom", "Chimelong Ocean Kingdom Parrot Coaster"],
    "hong-kong-disneyland": ["Hong Kong Disneyland Castle of Magical Dreams", "Hong Kong Disneyland castle"],
    "silver-dollar-city": ["Silver Dollar City Outlaw Run", "Silver Dollar City Time Traveler", "Silver Dollar City Wildfire coaster"],
    "hansa-park": ["Hansa-Park Kärnan", "Hansa-Park Schwur des Kärnan", "Hansa-Park Fluch von Novgorod"],
    "everland": ["Everland T Express", "Everland Yongin"],
    "happy-valley-shenzhen": ["Happy Valley Shenzhen roller coaster", "深圳欢乐谷"],
    "dreamworld-gold-coast": ["Dreamworld Gold Coast", "Dreamworld Steel Taipan"],
}
BAD = re.compile(r"(map|logo|svg|diagram|plan|chart|ticket|construction|parking|portrait|interior)", re.I)


def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception:  # 429 backoff
            time.sleep(6 * (attempt + 1))
    return {}


def search(q, n=6):
    data = api({
        "action": "query", "generator": "search", "gsrnamespace": "6", "gsrsearch": q,
        "gsrlimit": str(n), "prop": "imageinfo", "iiprop": "url|extmetadata|mime|size",
        "iiurlwidth": "960", "format": "json",
    })
    out = []
    for p in (data.get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("mime") not in ("image/jpeg",) or BAD.search(p.get("title", "")):
            continue
        if (ii.get("width") or 0) < 800:
            continue
        md = ii.get("extmetadata") or {}
        artist = re.sub(r"<[^>]+>", "", (md.get("Artist") or {}).get("value", "")).strip()
        out.append({
            "src": ii.get("thumburl"), "page": ii.get("descriptionurl"), "title": p.get("title"),
            "artist": artist[:80], "license": (md.get("LicenseShortName") or {}).get("value", ""),
        })
    return out


def do_search(only=None):
    try:
        res = json.load(open(CAND))
    except Exception:
        res = {}
    for rid, qs in QUERIES.items():
        if only and rid not in only:
            continue
        if not only and res.get(rid):
            continue
        cands = []
        for q in qs:
            cands += search(q)
            time.sleep(2)
        seen, uniq = set(), []
        for c in cands:
            if c["src"] and c["src"] not in seen:
                seen.add(c["src"]); uniq.append(c)
        res[rid] = uniq[:12]
        print(rid, len(uniq), flush=True)
        json.dump(res, open(CAND, "w"), ensure_ascii=False, indent=1)


def do_apply(choices):
    """choices: {id: index into candidates}"""
    cands = json.load(open(CAND))
    path = ROOT + "/data_themeparks.js"
    js = open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in js else "\n"
    for rid, idx in choices.items():
        c = cands[rid][idx]
        img = {k: c[k] for k in ("src", "page", "artist", "license", "title")}
        line = "    image: " + json.dumps(img, ensure_ascii=False) + "," + nl
        pat = re.compile(r'(\n\s*id: "' + re.escape(rid) + r'",\r?\n)(\s*image: .*\r?\n)?')
        js, n = pat.subn(lambda m: m.group(1) + line, js, count=1)
        print(rid, "OK" if n else "NOT FOUND")
    open(path, "w", encoding="utf-8", newline="").write(js)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "apply":
        do_apply(json.loads(sys.argv[2]))
    else:
        do_search(sys.argv[2:] if len(sys.argv) > 2 else None)

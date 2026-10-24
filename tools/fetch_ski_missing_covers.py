#!/usr/bin/env python3
"""Find better Wikimedia Commons covers for ski resorts whose THEMED_IMAGES entry is
missing or off-theme (cows, church paintings, train stations ...).

Step 1 (search):  python3 tools/fetch_ski_missing_covers.py search  -> writes candidates JSON
Step 2 (apply):   python3 tools/fetch_ski_missing_covers.py apply   -> writes the chosen
                  `image: {src, page, artist, license, title}` fields into data_ski.js
ski.html resolves covers as: item.image -> THEMED_IMAGES[id] -> inline SVG placeholder.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "DestinationAtlasCoverBot/1.1 (static ranking site)"
ROOT = __file__.rsplit("/tools/", 1)[0]
CAND = ROOT + "/tools/ski_cover_candidates.json"
QUERIES = {
    "banff-sunshine-lake-louise": ["Lake Louise 2018-03 ski", "Sunshine Village ski Banff"],
    "obergurgl-hochgurgl": ["Obergurgl winter", "Obergurgl Skigebiet"],
    "monterosa-ski": ["Monte Rosa Colle Bettaforca", "Gressoney ski"],
    "hemu-jikepulin": ["Hemu Village in the snow"],
    "koktokay": ["Koktokay", "Altay ski Xinjiang"],
    "st-anton-arlberg": ["St. Anton am Arlberg Skigebiet winter", "St Anton Arlberg ski slope"],
    "revelstoke": ["Revelstoke Mountain Resort", "Revelstoke ski"],
    "portes-du-soleil": ["Avoriaz ski", "Avoriaz winter"],
    "jungfrau-region": ["Kleine Scheidegg winter ski", "Grindelwald ski winter"],
    "laax": ["Laax ski", "Flims Laax winter"],
    "davos-klosters": ["Davos Parsenn ski", "Davos Jakobshorn winter"],
    "myoko-kogen": ["Myoko Akakura ski", "Myoko ski"],
    "lotte-arai": ["Arai ski resort", "Lotte Arai"],
    "madonna-di-campiglio": ["Madonna di Campiglio sci inverno", "Madonna di Campiglio winter"],
    "grandvalira": ["Grandvalira ski", "Pas de la Casa ski"],
    "valle-nevado": ["Valle Nevado ski", "Valle Nevado"],
    "arosa-lenzerheide": ["Arosa winter ski", "Lenzerheide ski"],
    "sierra-nevada-spain": ["Sierra Nevada ski resort Pradollano", "Estación de esquí Sierra Nevada"],
    "levi-finland": ["Levi ski resort", "Levi Kittilä ski"],
    "garmisch-partenkirchen": ["Garmisch Classic ski", "Kandahar Garmisch-Partenkirchen ski"],
    "hoshino-tomamu": ["Tomamu ski", "Hoshino Resorts Tomamu winter"],
    "queenstown-wanaka": ["Coronet Peak ski", "Remarkables ski field", "Cardrona ski"],
    "vail": ["Vail ski resort slopes", "Vail Colorado ski"],
}
BAD = re.compile(r"(map|logo|svg|diagram|plan|chart|sign|church|museum|cow|train|station|portrait)", re.I)


def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # 429 backoff
            time.sleep(6 * (attempt + 1))
    return {}


def search(q, n=6):
    data = api({
        "action": "query", "generator": "search", "gsrnamespace": "6", "gsrsearch": q,
        "gsrlimit": str(n), "prop": "imageinfo", "iiprop": "url|extmetadata|mime",
        "iiurlwidth": "960", "format": "json",
    })
    out = []
    for p in (data.get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("mime") not in ("image/jpeg",) or BAD.search(p.get("title", "")):
            continue
        md = ii.get("extmetadata") or {}
        artist = re.sub(r"<[^>]+>", "", (md.get("Artist") or {}).get("value", "")).strip()
        out.append({
            "src": ii.get("thumburl"), "page": ii.get("descriptionurl"), "title": p.get("title"),
            "artist": artist[:80], "license": (md.get("LicenseShortName") or {}).get("value", ""),
        })
    return out


def do_search():
    res = {}
    for rid, qs in QUERIES.items():
        cands = []
        for q in qs:
            cands += search(q)
            time.sleep(3)
        seen, uniq = set(), []
        for c in cands:
            if c["src"] and c["src"] not in seen:
                seen.add(c["src"]); uniq.append(c)
        res[rid] = uniq[:8]
        print(rid, len(uniq), flush=True)
    json.dump(res, open(CAND, "w"), ensure_ascii=False, indent=1)


def do_apply(choices):
    """choices: {id: index into candidates}"""
    cands = json.load(open(CAND))
    path = ROOT + "/data_ski.js"
    js = open(path, encoding="utf-8").read()
    for rid, idx in choices.items():
        c = cands[rid][idx]
        img = {k: c[k] for k in ("src", "page", "artist", "license", "title")}
        line = "    image: " + json.dumps(img, ensure_ascii=False) + ",\n"
        # drop an existing image line for this id, then insert after `id: "rid",`
        pat = re.compile(r'(\n\s*id: "' + re.escape(rid) + r'",\r?\n)(\s*image: .*\r?\n)?')
        js, n = pat.subn(lambda m: m.group(1) + line, js, count=1)
        print(rid, "OK" if n else "NOT FOUND")
    open(path, "w", encoding="utf-8").write(js)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "apply":
        do_apply(json.loads(sys.argv[2]))
    else:
        do_search()

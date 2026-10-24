#!/usr/bin/env python3
"""Fetch a landscape cover photo per destination from Wikimedia Commons.
Outputs images.js: window.DEST_IMAGES = { id: {src, page, artist, license} }"""
import json, re, sys, html, urllib.parse, urllib.request, concurrent.futures as cf, subprocess, os

ROOT = "/Users/xtxsinan/.gemini/antigravity/scratch/destination_rankings"
OVERRIDES = json.load(open(sys.argv[1])) if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else {}

# load data via node-less parse: eval JS with a tiny JS->JSON shim using osascript JavaScriptCore
js = open(f"{ROOT}/data.js", encoding="utf-8").read() + "\n" + open(f"{ROOT}/data_part2.js", encoding="utf-8").read()
js = "var window={};" + js + ";JSON.stringify(window.DESTINATIONS_DATA.map(d=>({id:d.id,name:d.name,region:d.region})))"
out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js], capture_output=True, text=True)
dests = json.loads(out.stdout)

BAD = re.compile(r"map|flag|coat|logo|locator|diagram|stamp|satellite|iss0|landsat|sentinel|chart|plan|svg|poster|menu|sign|ticket|document|panorama|360", re.I)
UA = {"User-Agent": "OceanicAtlasCoverBot/1.0 (https://xtxsinan-lgtm.github.io/destination_rankings/)"}

def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

def search(q):
    data = api({
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{q} filetype:bitmap", "gsrlimit": 20,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 1200,
    })
    pages = sorted((data.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        t = p.get("title", "")
        if BAD.search(t) or ii.get("mime") != "image/jpeg":
            continue
        w, h = ii.get("width", 0), ii.get("height", 0)
        if w < 1600 or h == 0 or w / h < 1.3 or w / h > 2.2:
            continue
        md = ii.get("extmetadata", {})
        lic = strip(md.get("LicenseShortName", {}).get("value"))
        return {
            "src": ii.get("thumburl"),
            "page": ii.get("descriptionurl"),
            "artist": strip(md.get("Artist", {}).get("value"))[:80],
            "license": lic,
            "title": t,
        }
    return None

def queries(d):
    if d["id"] in OVERRIDES:
        return [OVERRIDES[d["id"]]]
    m = re.search(r"\(([^()]+)\)\s*$", d["name"])
    en = m.group(1) if m else ""
    parts = [p.strip() for p in re.split(r"[/&+,]| and ", en) if p.strip()]
    qs = []
    if en:
        qs.append(f"{parts[0]} beach")
        if len(parts) > 1: qs.append(f"{parts[1]} beach")
        qs.append(parts[0])
    return qs

def run(d):
    for q in queries(d):
        try:
            r = search(q)
        except Exception as e:
            r = None
        if r:
            r["q"] = q
            return d["id"], r
    return d["id"], None

existing = {}
if os.path.exists(f"{ROOT}/images.js") and OVERRIDES:
    txt = open(f"{ROOT}/images.js", encoding="utf-8").read()
    existing = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])

todo = [d for d in dests if not existing or d["id"] in OVERRIDES]
res = dict(existing)
with cf.ThreadPoolExecutor(6) as ex:
    for i, r in ex.map(run, todo):
        if r: res[i] = r
        print(i, "->", (r or {}).get("title"), file=sys.stderr)

missing = [d["id"] for d in dests if d["id"] not in res]
print("missing:", missing, file=sys.stderr)
with open(f"{ROOT}/images.js", "w", encoding="utf-8") as f:
    f.write("// Cover photos from Wikimedia Commons (see `page` for author & license)\n")
    f.write("window.DEST_IMAGES = " + json.dumps(res, ensure_ascii=False, indent=1) + ";\n")

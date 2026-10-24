#!/usr/bin/env python3
"""Repair data_rv_top20.js:
  1. verify every coverImage URL (browser UA); replace 404s with real Wikimedia Commons thumbnails
     found via the Commons search API (thumburl, 1280px);
  2. add numeric lat/lon (pickup hub coordinates) to each route for shared_widgets.js.
Idempotent: re-running only touches URLs that fail or lat/lon that are missing."""
import json, re, urllib.parse, urllib.request

ROOT = "/Users/xtxsinan/.gemini/antigravity/scratch/destination_rankings"
PATH = ROOT + "/data_rv_top20.js"
UA = {"User-Agent": "DestinationAtlasCoverBot/1.1 (https://xtxsinan-lgtm.github.io/destination_rankings/)"}
BAD = re.compile(r"map|flag|coat|logo|locator|diagram|stamp|satellite|chart|plan|\.svg|poster|menu|sign|ticket|document|icon|portrait|statue|plaque|\.tif|\.pdf", re.I)

QUERIES = {
    "rv-01-alaska": ["Homer Spit Alaska", "Kenai Fjords National Park", "Seward Alaska Resurrection Bay"],
    "rv-02-canadian-rockies": ["Moraine Lake Banff", "Lake Louise Banff"],
    "rv-03-nz-south-island": ["Lake Tekapo lupins", "Lake Tekapo", "Lake Pukaki Mount Cook"],
    "rv-04-yellowstone-teton": ["Grand Prismatic Spring"],
    "rv-05-hokkaido-onsen": ["Farm Tomita Furano lavender", "Furano lavender field", "Biei Hokkaido"],
    "rv-06-norway-lofoten": ["Reine Lofoten"],
    "rv-07-utah-mighty-5": ["Bryce Canyon amphitheater"],
    "rv-08-queensland-gold-coast": ["Surfers Paradise beach Gold Coast", "Gold Coast Queensland beach"],
    "rv-09-dolomites-alps": ["Santa Maddalena Val di Funes", "Val di Funes Dolomites", "Tre Cime di Lavaredo"],
    "rv-10-iceland-south-coast": ["Skogafoss waterfall", "Seljalandsfoss"],
    "rv-11-norway-western-fjords": ["Geirangerfjord", "Geirangerfjorden"],
    "rv-12-tasmania-circle": ["Cradle Mountain Dove Lake", "Cradle Mountain Tasmania"],
    "rv-13-scottish-highlands-skye": ["Glenfinnan Viaduct"],
    "rv-14-vancouver-island-tofino": ["Long Beach Pacific Rim National Park", "Tofino beach"],
    "rv-15-great-ocean-road-grampians": ["Twelve Apostles Victoria", "Great Ocean Road Twelve Apostles"],
    "rv-16-olympic-peninsula-oregon-coast": ["Haystack Rock Cannon Beach", "Cannon Beach Oregon"],
    "rv-17-nz-north-island-geothermal": ["Champagne Pool Wai-O-Tapu", "Wai-O-Tapu"],
    "rv-18-france-loire-brittany": ["Mont-Saint-Michel"],
    "rv-19-blue-ridge-smoky-mountains": ["Blue Ridge Parkway autumn", "Blue Ridge Parkway", "Great Smoky Mountains"],
    "rv-20-south-africa-garden-route": ["Storms River suspension bridge Tsitsikamma", "Tsitsikamma", "Garden Route South Africa"],
}

COORDS = {  # pickup hub (first listed city)
    "rv-01-alaska": (61.2181, -149.9003),
    "rv-02-canadian-rockies": (51.0447, -114.0719),
    "rv-03-nz-south-island": (-43.5321, 172.6362),
    "rv-04-yellowstone-teton": (40.7608, -111.8910),
    "rv-05-hokkaido-onsen": (42.7752, 141.6923),
    "rv-06-norway-lofoten": (67.2804, 14.4049),
    "rv-07-utah-mighty-5": (36.1699, -115.1398),
    "rv-08-queensland-gold-coast": (-27.4698, 153.0251),
    "rv-09-dolomites-alps": (45.4642, 9.1900),
    "rv-10-iceland-south-coast": (64.1466, -21.9426),
    "rv-11-norway-western-fjords": (60.3913, 5.3221),
    "rv-12-tasmania-circle": (-42.8821, 147.3272),
    "rv-13-scottish-highlands-skye": (55.9533, -3.1883),
    "rv-14-vancouver-island-tofino": (49.2827, -123.1207),
    "rv-15-great-ocean-road-grampians": (-37.8136, 144.9631),
    "rv-16-olympic-peninsula-oregon-coast": (47.6062, -122.3321),
    "rv-17-nz-north-island-geothermal": (-36.8485, 174.7633),
    "rv-18-france-loire-brittany": (48.8566, 2.3522),
    "rv-19-blue-ridge-smoky-mountains": (33.7490, -84.3880),
    "rv-20-south-africa-garden-route": (-33.9249, 18.4241),
}


def ok(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh) " + UA["User-Agent"]}, method="GET")
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status == 200 and r.headers.get("Content-Type", "").startswith("image")
    except Exception:
        return False


def search(q):
    api = ("https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrlimit=10"
           "&prop=imageinfo&iiprop=url|size|mime&iiurlwidth=1280&format=json&gsrsearch=" + urllib.parse.quote(q))
    with urllib.request.urlopen(urllib.request.Request(api, headers=UA), timeout=30) as r:
        data = json.load(r)
    pages = sorted((data.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        if BAD.search(p["title"]):
            continue
        if ii.get("width", 0) < ii.get("height", 1):  # want landscape
            continue
        if ii.get("thumburl"):
            return ii["thumburl"], p["title"]
    return None, None


def main():
    src = open(PATH, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in src else "\n"
    blocks = re.split(r'(?=\n    id: "rv-)', src)
    out = []
    for b in blocks:
        m = re.match(r'\n    id: "(rv-[^"]+)"', b)
        if not m:
            out.append(b); continue
        rid = m.group(1)
        cm = re.search(r'coverImage: "([^"]*)"', b)
        if cm and not ok(cm.group(1)):
            for q in QUERIES.get(rid, []):
                url, title = search(q)
                if url and ok(url):
                    print(f"{rid}: {title} -> {url}")
                    b = b.replace(cm.group(0), f'coverImage: "{url}"')
                    break
            else:
                print(f"{rid}: NO REPLACEMENT FOUND")
        else:
            print(f"{rid}: ok")
        if "lat:" not in b and rid in COORDS:
            la, lo = COORDS[rid]
            b = re.sub(r'(\n    pickupCity: "[^"]*",)', lambda mm: f"{mm.group(1)}{nl}    lat: {la},{nl}    lon: {lo},", b, count=1)
        out.append(b)
    open(PATH, "w", encoding="utf-8", newline="").write("".join(out))


if __name__ == "__main__":
    main()

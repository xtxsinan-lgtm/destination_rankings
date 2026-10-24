#!/usr/bin/env python3
"""Second pass for data_cruises_top50.js: hand-picked Commons overrides for ships where the automatic
search (tools/fix_cruise_images.py) landed on an irrelevant file, plus URL normalisation
(thumb.wikimedia.org?utm... -> upload.wikimedia.org) and a final HTTP check of every cover."""
import json, os, re, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data_cruises_top50.js")
UA = {"User-Agent": "Mozilla/5.0 DestinationAtlasCoverBot/1.1"}
C = "https://upload.wikimedia.org/wikipedia/commons/thumb/"
OVR = {
    "paul-gauguin-tahiti": ("Cruise Ship Paul Gauguin 01.jpg", C + "c/c2/Cruise_Ship_Paul_Gauguin_01.jpg/1280px-Cruise_Ship_Paul_Gauguin_01.jpg"),
    "uniworld-la-venezia": ("River Countess in Venice.JPG (Uniworld)", C + "a/a2/River_Countess_in_Venice.JPG/1280px-River_Countess_in_Venice.JPG"),
    "aria-amazon-delfin-i": ("Peruvian Amazon river scene.jpg", C + "4/43/Peruvian_Amazon_river_scene.jpg/1280px-Peruvian_Amazon_river_scene.jpg"),
    "aqua-mekong-vietnam-cambodia": ("Mekong Sun river cruise ship in Luang Prabang.jpg", C + "8/80/Mekong_Sun_river_cruise_ship_in_Luang_Prabang.jpg/1280px-Mekong_Sun_river_cruise_ship_in_Luang_Prabang.jpg"),
    "viking-mississippi-usa": ("American Queen at the Mississippi River front, New Orleans.jpg", C + "1/15/New_Orleans_Feb_2017_-_American_Queen_at_the_Mississippi_River_front.jpg/1280px-New_Orleans_Feb_2017_-_American_Queen_at_the_Mississippi_River_front.jpg"),
    "aman-amandira-indonesia": ("Pinisi, Komodo, 2016 (01).jpg", C + "1/1b/Pinisi%2C_Komodo%2C_2016_%2801%29.jpg/1280px-Pinisi%2C_Komodo%2C_2016_%2801%29.jpg"),
    "alila-purnama-indonesia": ("Phinisi, Penjelajah Pulau di Labuan Bajo.jpg", C + "8/8e/Phinisi%2C_Penjelajah_Pulau_di_Labuan_Bajo.jpg/1280px-Phinisi%2C_Penjelajah_Pulau_di_Labuan_Bajo.jpg"),
    "galapagos-grace-yacht": ("Galapagos Islands - Ecuador (4870398009).jpg", C + "c/cd/Galapagos_Islands_-_Ecuador_%284870398009%29.jpg/1280px-Galapagos_Islands_-_Ecuador_%284870398009%29.jpg"),
}


def ok(url):
    if not url.startswith("http"):
        return os.path.exists(os.path.join(ROOT, url))
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
            return r.status == 200 and r.headers.get("Content-Type", "").startswith("image")
    except Exception as e:
        print("   ", e)
        return False


src = open(DATA, encoding="utf-8").read()
a = src.index("[", src.index("LUXURY_CRUISES_TOP50"))
b = src.index("\n];", a) + 2
arr = json.loads(src[a:b + 1].rstrip(";").rstrip())
bad = 0
for c in arr:
    if c["id"] in OVR:
        c["imageCredit"], c["image"] = OVR[c["id"]]
    c["image"] = re.sub(r"^https://thumb\.wikimedia\.org/", "https://upload.wikimedia.org/", c["image"]).split("?utm_")[0]
    good = ok(c["image"])
    bad += not good
    print(f"{c['rank']:>2} {'OK ' if good else 'BAD'} {c['image'][-70:]}")
open(DATA, "w", encoding="utf-8").write(src[:a] + json.dumps(arr, ensure_ascii=False, indent=2) + src[b:])
print("bad:", bad)

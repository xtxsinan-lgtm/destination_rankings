"""Enrich data_sailing_top20.js: add lat/lon (base port) to each route, clean Wikimedia thumb URLs,
fix obvious price typos in SAILING_VERIFIED_BOATS_2027. Idempotent. Usage: python3 tools/sailing_enrich.py"""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sailing_data_io import load, save

COORDS = {
    "greece-lefkada-ionian": (38.833, 20.711),
    "sardinia-bonifacio": (41.033, 9.533),
    "sicily-aeolian-islands": (38.128, 15.105),
    "caribbean-bvi": (18.425, -64.620),
    "tahiti-bora-bora": (-16.733, -151.440),
    "turkey-gocek-fethiye": (36.750, 28.940),
    "croatia-split-dalmatia": (43.503, 16.433),
    "croatia-dubrovnik-korcula": (42.670, 18.127),
    "seychelles-inner-islands": (-4.640, 55.470),
    "bahamas-exumas-cays": (25.020, -77.270),
    "grenadines-tobago-cays": (13.130, -61.200),
    "thailand-phuket-phang-nga": (8.170, 98.340),
    "australia-whitsundays-reef": (-20.270, 148.720),
    "spain-mallorca-menorca": (39.565, 2.630),
    "greece-saronic-gulf": (37.910, 23.710),
    "italy-amalfi-pontine-islands": (40.660, 14.790),
    "greece-sporades-mammamia": (39.163, 23.490),
    "usvi-st-john-national-park": (18.333, -64.930),
    "caribbean-martinique-st-lucia": (14.470, -60.870),
    "belize-barrier-reef-cays": (16.513, -88.370),
}


def clean_url(u):
    return re.sub(r"\?utm_source=.*$", "", u)


def main():
    d, order = load()
    for key in ("SAILING_ROUTES_TOP20", "SAILING_TOP5_ROUTES"):
        for r in d[key]:
            if r["id"] in COORDS:
                r["lat"], r["lon"] = COORDS[r["id"]]
            for p in r.get("photos", []):
                p["url"] = clean_url(p["url"])
    for stops in d["SAILING_ROUTE_STOPS_GALLERY"].values():
        for s in stops:
            for p in s.get("photos", []):
                p["url"] = clean_url(p["url"])
    # Price typo: Relax Planet July listed as 56515/66100 (decimal slip) -> 5652/6610
    for b in d["SAILING_VERIFIED_BOATS_2027"]:
        for m, v in b["monthly"].items():
            if v.get("now", 0) > 30000:
                v["now"] = round(v["now"] / 10)
                v["list"] = round(v["list"] / 10)
                print("fixed typo", b["slug"], m, v)
    save(d, order)


if __name__ == "__main__":
    main()

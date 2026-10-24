"""Check every image URL in data_sailing_top20.js; print status. Usage: python3 tools/sailing_check_images.py"""
import json, sys, urllib.request, concurrent.futures as cf
sys.path.insert(0, __import__("os").path.dirname(__file__))
from sailing_data_io import load

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36 DestinationAtlasCoverBot/1.1"


def collect(d):
    items = []
    for r in d["SAILING_ROUTES_TOP20"]:
        for i, p in enumerate(r.get("photos", [])):
            items.append((f"route:{r['id']}:{i}", p.get("caption", ""), p["url"]))
    for g, stops in d["SAILING_ROUTE_STOPS_GALLERY"].items():
        for si, s in enumerate(stops):
            for i, p in enumerate(s.get("photos", [])):
                items.append((f"stop:{g}:{si}:{i}", s["title"][:50] + " | " + p.get("caption", ""), p["url"]))
    return items


def check(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
        with urllib.request.urlopen(req, timeout=20) as r:
            ct = r.headers.get("Content-Type", "")
            return r.status if ct.startswith("image") else f"{r.status}-{ct}"
    except Exception as e:
        return str(getattr(e, "code", e))[:40]


if __name__ == "__main__":
    d, _ = load()
    items = collect(d)
    with cf.ThreadPoolExecutor(6) as ex:
        res = list(ex.map(lambda it: check(it[2]), items))
    bad = 0
    for (k, cap, u), s in zip(items, res):
        ok = s == 200
        bad += not ok
        print("OK " if ok else "BAD", s, k, cap[:70], u[-70:] if not ok else "")
    print("total", len(items), "bad", bad)

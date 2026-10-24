"""Read/write helpers for data_sailing_top20.js (window.* = JSON; blocks)."""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data_sailing_top20.js")

HEADER = ("// Global & European 4-Cabin Catamaran Sailing Routes, Cost Breakdowns, Itineraries & Verified 2027 Listings\n"
          "// Generated from real-time charter platform benchmarks (Boataround, SamBoat, Croatia Yachting)\n")


def load():
    src = open(PATH, encoding="utf-8").read()
    out = {}
    order = []
    for m in re.finditer(r"^window\.(\w+)\s*=\s*", src, re.M):
        name = m.group(1)
        dec = json.JSONDecoder()
        val, end = dec.raw_decode(src, m.end())
        out[name] = val
        order.append(name)
    return out, order


def save(data, order):
    parts = [HEADER]
    for k in order:
        parts.append(f"\nwindow.{k} = " + json.dumps(data[k], ensure_ascii=False, indent=2) + ";\n")
    open(PATH, "w", encoding="utf-8").write("".join(parts))


if __name__ == "__main__":
    d, o = load()
    for k in o:
        v = d[k]
        print("==", k, type(v).__name__, len(v))

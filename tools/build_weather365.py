#!/usr/bin/env python3
"""
Build weather365.js from tools/weatherspark_raw.json.
Provides 365-day daily Weather Spark series for all 145 ranked beach destinations
plus 4 eliminated destinations (149 total):
- high: 365 daily average high air temperatures (°C)
- low: 365 daily average low air temperatures (°C)
- water: 365 daily average water temperatures (°C)
- waterLow: 365 daily low water temperatures (10th percentile band, °C)
- waterHigh: 365 daily high water temperatures (90th percentile band, °C)
- clear: 365 daily clearer/sunny sky ratios (%)
- rain: 365 daily precipitation / wet day probabilities (%)
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(ROOT, "tools", "weatherspark_raw.json")
OUT_PATH = os.path.join(ROOT, "weather365.js")


def main():
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    lines = [
        "// Auto-generated from Weather Spark (weatherspark.com) 365-day daily climate vectors",
        "// Contains 365-day daily averages for all 145 ranked beach resorts + 4 eliminated destinations:",
        "// high (°C), low (°C), water (°C avg), waterLow (°C 10th pct), waterHigh (°C 90th pct), clear (%), rain (%)",
        "window.WEATHER_SPARK_365 = {"
    ]

    keys = sorted(raw.keys())
    for idx, k in enumerate(keys):
        d = raw[k]
        entry = {
            "wsId": d["ws_id"],
            "wsName": d["ws_name"],
            "wsUrl": d["ws_url"],
            "high": [round(x, 1) for x in d["high"]],
            "low": [round(x, 1) for x in d["low"]],
            "water": [round(x, 1) for x in d["water"]],
            "waterLow": [round(x, 1) for x in d["waterLow10"]],
            "waterHigh": [round(x, 1) for x in d["waterHigh90"]],
            "clear": [round(x, 1) for x in d["clear"]],
            "rain": [round(x, 1) for x in d["rain"]],
        }
        comma = "," if idx < len(keys) - 1 else ""
        lines.append(f'  {json.dumps(k)}: {json.dumps(entry, ensure_ascii=False, separators=(",", ":"))}{comma}')

    lines.append("};")
    content = "\n".join(lines) + "\n"

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    size_kb = os.path.getsize(OUT_PATH) / 1024.0
    print(f"Generated {OUT_PATH} ({len(keys)} destinations, {size_kb:.1f} KB)")


if __name__ == "__main__":
    main()

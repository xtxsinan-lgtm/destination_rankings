#!/usr/bin/env python3
"""
Generate sitemap.xml, robots.txt, and inject PWA manifest link + Schema.org JSON-LD
ItemList structured data into all 8 HTML pages of Destination Atlas.
"""
import json
import os
import re
import subprocess
from datetime import date

BASE_URL = "https://destination-atlas.example.com"
TODAY = date.today().isoformat()

PAGES = [
    {
        "file": "index.html",
        "title": "Destination Atlas · 全球硬核旅行目的地总控台 (11大榜单·835处地标与航线)",
        "desc": "涵盖全球200大海岛与海岸度假地、50大水族馆、50大动物园与10大游猎园、115大主题与水上乐园、100大滑雪场、100大商业驻场秀、100大重器博物馆、50艘高档奢华邮轮的零广告硬核量化决策平台。",
        "priority": "1.0",
        "js_files": [],
        "js_expr": None,
    },
    {
        "file": "beaches.html",
        "title": "全球 200 大海滨与海岛度假胜地硬核排行榜 · Destination Atlas",
        "desc": "基于WMO/NOAA 30年气候统计基准与45分钟一日游圈独立拆分原则，涵盖130处常年真热带与70处季节性海岸，支持8维个性化滑块实时算分、飞行时长换算与3岛雷达图PK。",
        "priority": "0.9",
        "js_files": ["data.js", "data_part2.js"],
        "js_expr": "(window.DESTINATIONS_DATA || []).slice(0, 25)",
    },
    {
        "file": "aquariums.html",
        "title": "The Abyss Index · 全球顶级水族馆 Top 50 硬核榜 (水体/视窗/物种全参数)",
        "desc": "剥离过山车与杂技表演，纯按水下展陈统治力排名。完整收录全球50大水族馆全馆总水体、最大单池水体、主视窗尺寸、物种数、生物总数与避坑贴士。",
        "priority": "0.9",
        "js_files": ["data_aquariums_zoos_museums.js"],
        "js_expr": "(window.AQUARIUMS_TOP50 || window.AQUARIUMS_TOP35 || []).slice(0, 25)",
    },
    {
        "file": "zoos.html",
        "title": "Field Notes · 全球顶级动物园 Top 50 & 全美野生动物园 Top 10",
        "desc": "破除百年历史与免费滤镜，按栖息地空间尺度、巨型生态温室、总面积、物种数、生物总数与无笼舍沉浸感硬核排名全球50大动物园。",
        "priority": "0.9",
        "js_files": ["data_aquariums_zoos_museums.js"],
        "js_expr": "(window.ZOOS_TOP50 || window.ZOOS_TOP30 || []).slice(0, 25)",
    },
    {
        "file": "themeparks.html",
        "title": "The Thrill & Magic Index · 全球主题游乐园 Top 100 & 水上乐园 Top 15",
        "desc": "涵盖全球100座顶级主题乐园与过山车圣地、15座殿堂级水上乐园，支持6维权重实时重算、过山车数量与客流排序及快通攻略。",
        "priority": "0.9",
        "js_files": ["data_themeparks.js"],
        "js_expr": "(window.THEMEPARKS_TOP100 || []).slice(0, 25)",
    },
    {
        "file": "ski.html",
        "title": "The Alpine & Powder Index · 全球滑雪度假村 Top 100 硬核榜",
        "desc": "横跨阿尔卑斯、北美落基山、日本粉雪与南半球反季的全球百大滑雪场排名，收录垂直落差、雪道总长、年降雪量、最高海拔与雪票比价。",
        "priority": "0.9",
        "js_files": ["data_ski.js"],
        "js_expr": "(window.SKI_RESORTS_TOP100 || []).slice(0, 25)",
    },
    {
        "file": "shows.html",
        "title": "The Grand Stage Index · 全球商业驻场秀 Top 100 观演指南",
        "desc": "严选全球100部拥有定制剧场与顶级声光电重工舞台的常驻商业大秀，标注语言友好度、剧场座位数、最佳选座区域与停演避坑名单。",
        "priority": "0.9",
        "js_files": ["data_shows_top100.js"],
        "js_expr": "(window.SHOWS_TOP100 || []).slice(0, 25)",
    },
    {
        "file": "museums.html",
        "title": "Heavy Metal Index · 全球科技、工业与军事重器博物馆 Top 100",
        "desc": "100%纯真机与重器硬件标准，收录全球航空母舰、核潜艇、航天飞机、蒸汽巨兽与工业遗产殿堂，支持免费场馆一键筛选。",
        "priority": "0.9",
        "js_files": ["data_aquariums_zoos_museums.js"],
        "js_expr": "(window.INDUSTRIAL_MUSEUMS_TOP100 || []).slice(0, 25)",
    },
    {
        "file": "cruises.html",
        "title": "The Grand Fleet Index · 全球 50 大高档与奢华邮轮权威图鉴 (6维测评 + 未来一年最低价)",
        "desc": "采用《游轮数据》Sheet量化方法，按人均Tonnage、Crew乘客比、房间大小、餐饮水准、船上活动水准、邮轮设计6大维度评判全球50艘高档奢华邮轮，并附未来一年实测最低价格。",
        "priority": "0.9",
        "js_files": ["data_cruises_top50.js"],
        "js_expr": "(window.LUXURY_CRUISES_TOP50 || []).slice(0, 25)",
    },
]


def eval_js_items(js_files, js_expr):
    if not js_files or not js_expr:
        return []
    for f in js_files:
        if not os.path.exists(f):
            return []
    loader = "var window = {}; ObjC.import('Foundation');\n"
    for f in js_files:
        loader += (
            f"var s = $.NSString.alloc.initWithContentsOfFileEncodingError('{f}', $.NSUTF8StringEncoding, null).js;\n"
            "eval(s);\n"
        )
    loader += f"JSON.stringify({js_expr});"
    try:
        out = subprocess.check_output(["osascript", "-l", "JavaScript", "-e", loader])
        return json.loads(out.decode("utf-8"))
    except Exception as e:
        print(f"Warning: could not evaluate {js_expr}: {e}")
        return []


def build_json_ld(page, items):
    if not items:
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": page["title"],
            "description": page["desc"],
            "url": f"{BASE_URL}/{page['file']}",
        }
    elements = []
    for idx, it in enumerate(items, start=1):
        rank = it.get("rank") or idx
        name = it.get("name") or ""
        country = it.get("country") or it.get("region") or ""
        city = it.get("city") or ""
        highlight = it.get("highlight") or it.get("summary") or ""
        elem = {
            "@type": "ListItem",
            "position": rank,
            "item": {
                "@type": "TouristAttraction",
                "name": name,
                "description": f"{country} {city} · {highlight}".strip(" ·"),
            },
        }
        if "lat" in it and "lon" in it:
            elem["item"]["geo"] = {
                "@type": "GeoCoordinates",
                "latitude": it["lat"],
                "longitude": it["lon"],
            }
        elements.append(elem)
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": page["title"],
        "description": page["desc"],
        "numberOfItems": len(elements),
        "itemListElement": elements,
    }


def main():
    # 1. Generate sitemap.xml
    sm_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for p in PAGES:
        sm_lines.extend([
            "  <url>",
            f"    <loc>{BASE_URL}/{p['file']}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            "    <changefreq>weekly</changefreq>",
            f"    <priority>{p['priority']}</priority>",
            "  </url>",
        ])
    sm_lines.append("</urlset>\n")
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(sm_lines))

    # 2. Generate robots.txt
    robots = f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n"
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots)

    # 3. Inject manifest, OpenGraph, and JSON-LD into each HTML page
    for p in PAGES:
        fname = p["file"]
        if not os.path.exists(fname):
            print(f"Skipping {fname} (not found)")
            continue
        with open(fname, "r", encoding="utf-8") as f:
            html = f.read()

        # Remove previous injected block if present
        html = re.sub(
            r"\s*<!-- BEGIN AUTO-SEO -->.*?<!-- END AUTO-SEO -->",
            "",
            html,
            flags=re.DOTALL,
        )

        items = eval_js_items(p["js_files"], p["js_expr"])
        json_ld = build_json_ld(p, items)
        json_ld_str = json.dumps(json_ld, ensure_ascii=False, indent=2)

        seo_block = f"""
  <!-- BEGIN AUTO-SEO -->
  <meta name="description" content="{p['desc']}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{p['title']}" />
  <meta property="og:description" content="{p['desc']}" />
  <meta property="og:url" content="{BASE_URL}/{fname}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{p['title']}" />
  <meta name="twitter:description" content="{p['desc']}" />
  <link rel="manifest" href="manifest.json" />
  <meta name="theme-color" content="#0b132b" />
  <script type="application/ld+json">
{json_ld_str}
  </script>
  <!-- END AUTO-SEO -->
</head>"""

        if "</head>" in html:
            html = html.replace("</head>", seo_block, 1)
            with open(fname, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Injected SEO + JSON-LD ({len(items)} items) into {fname}")


if __name__ == "__main__":
    main()

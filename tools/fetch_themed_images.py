#!/usr/bin/env python3
"""Fetch Wikimedia Commons cover photos for all themed rankings (Aquariums, Zoos, Safari, Museums, Theme Parks, Ski, Shows).
Outputs images_themed.js: window.THEMED_IMAGES = { id: {src, page, artist, license, title} }"""
import json, re, html, time, urllib.parse, urllib.request, concurrent.futures as cf, subprocess, os, sys

ROOT = "/Users/xtxsinan/.gemini/antigravity/scratch/destination_rankings"
BAD = re.compile(r"map|flag|coat|logo|locator|diagram|stamp|satellite|iss0|landsat|sentinel|chart|plan|svg|poster|menu|sign|ticket|document|icon|portrait|person|statue|plaque", re.I)
UA = {"User-Agent": "DestinationAtlasCoverBot/1.1 (https://xtxsinan-lgtm.github.io/destination_rankings/)"}

CUSTOM_QUERIES = {
    "aq-chimelong": ["Chimelong Ocean Kingdom whale shark", "Chimelong Ocean Kingdom aquarium"],
    "aq-seaworld-abudhabi": ["SeaWorld Abu Dhabi", "Yas Island SeaWorld", "whale shark aquarium"],
    "aq-georgia": ["Georgia Aquarium whale shark", "Georgia Aquarium Ocean Voyager"],
    "aq-churaumi": ["Okinawa Churaumi Aquarium Kuroshio", "Churaumi Aquarium whale shark"],
    "aq-singapore-oceanarium": ["S.E.A. Aquarium Singapore", "SEA Aquarium Sentosa"],
    "aq-lisbon": ["Oceanario de Lisboa main tank", "Oceanario de Lisboa"],
    "aq-valencia": ["Oceanografic Valencia tunnel", "Oceanografic Valencia"],
    "aq-nausicaa": ["Nausicaa Boulogne aquarium", "Nausicaa grand bassin"],
    "aq-kenting-nmmba": ["National Museum of Marine Biology and Aquarium Taiwan", "Kenting aquarium"],
    "aq-dubai-mall": ["Dubai Mall Aquarium tank", "Dubai Aquarium and Underwater Zoo"],
    "aq-atlantis-dubai": ["The Lost Chambers Aquarium Dubai", "Atlantis The Palm aquarium"],
    "aq-atlantis-sanya": ["Atlantis Sanya aquarium", "The Lost Chambers Aquarium"],
    "aq-nagoya": ["Port of Nagoya Public Aquarium", "Nagoya Aquarium orca"],
    "aq-monterey": ["Monterey Bay Aquarium kelp forest", "Monterey Bay Aquarium jellyfish"],
    "aq-kaiyukan": ["Osaka Aquarium Kaiyukan whale shark", "Osaka Kaiyukan"],
    "aq-loro-parque": ["Loro Parque Penguin", "Loro Parque aquarium"],
    "aq-jeju": ["Aqua Planet Jeju", "Jeju aquarium"],
    "aq-shanghai-haichang": ["Shanghai Haichang Ocean Park", "orca aquarium"],
    "aq-rizhao": ["Rizhao Ocean Park", "aquarium underwater tunnel shark"],
    "aq-shedd": ["Shedd Aquarium Chicago", "Shedd Aquarium Wild Reef"],
    "aq-tennessee": ["Tennessee Aquarium Chattanooga", "Tennessee Aquarium"],
    "aq-baltimore": ["National Aquarium Baltimore", "Baltimore Aquarium"],
    "aq-seaworld-orlando": ["SeaWorld Orlando shark encounter", "Discovery Cove Orlando"],
    "aq-seaworld-sandiego": ["SeaWorld San Diego penguin", "SeaWorld San Diego"],
    "aq-epcot-seabase": ["The Seas with Nemo and Friends aquarium", "EPCOT aquarium"],
    "aq-hk-oceanpark": ["Grand Aquarium Ocean Park Hong Kong", "Ocean Park Hong Kong aquarium"],
    "aq-shanghai-lujiazui": ["Shanghai Ocean Aquarium tunnel", "Shanghai Ocean Aquarium"],
    "aq-ripleys-toronto": ["Ripley's Aquarium of Canada shark", "Ripley's Aquarium Toronto"],
    "aq-den-bla-planet": ["Den Bla Planet Copenhagen", "National Aquarium Denmark"],
    "aq-vancouver": ["Vancouver Aquarium sea otter", "Vancouver Aquarium"],
    "aq-tokyo-sealife": ["Tokyo Sea Life Park", "Kasai Rinkai Aquarium"],
    "aq-long-beach": ["Aquarium of the Pacific Long Beach", "Aquarium of the Pacific"],
    "aq-istanbul": ["Istanbul Akvaryum", "Istanbul Aquarium"],
    "aq-two-oceans": ["Two Oceans Aquarium Cape Town", "Two Oceans Aquarium"],
    "aq-ushaka": ["uShaka Marine World Durban", "uShaka Sea World"],
    "zoo-san-diego": ["San Diego Zoo koala", "San Diego Zoo"],
    "zoo-pairi-daiza": ["Pairi Daiza elephant", "Pairi Daiza"],
    "zoo-omaha": ["Henry Doorly Zoo Desert Dome", "Omaha Henry Doorly Zoo"],
    "zoo-mandai-singapore": ["Singapore Zoo orangutan", "Singapore Zoo River Wonders"],
    "zoo-animal-kingdom": ["Disney's Animal Kingdom Kilimanjaro Safaris", "Disney's Animal Kingdom"],
    "zoo-chimelong-guangzhou": ["Chimelong Safari Park Guangzhou", "Chimelong Safari Park"],
    "zoo-leipzig": ["Zoo Leipzig Gondwanaland", "Zoo Leipzig"],
    "zoo-beauval": ["ZooParc de Beauval dome", "ZooParc de Beauval"],
    "zoo-doue": ["Bioparc de Doue-la-Fontaine", "Zoo de Doue"],
    "zoo-burgers": ["Burgers Zoo Bush", "Burgers Zoo Arnhem"],
    "zoo-loro-parque": ["Loro Parque Tenerife", "Loro Parque"],
    "zoo-taronga": ["Taronga Zoo giraffe Sydney", "Taronga Zoo"],
    "zoo-prague": ["Prague Zoo", "Zoo Praha"],
    "zoo-bronx": ["Bronx Zoo", "Bronx Zoo gorilla"],
    "zoo-zurich": ["Zoo Zurich Masoala", "Zoo Zurich elephant"],
    "zoo-chester": ["Chester Zoo", "Chester Zoo Islands"],
    "zoo-bioparc-valencia": ["Bioparc Valencia", "Bioparc Valencia giraffe"],
    "zoo-columbus-wilds": ["Columbus Zoo polar bear", "The Wilds Ohio rhino"],
    "zoo-beekse-bergen": ["Safaripark Beekse Bergen", "Beekse Bergen giraffe"],
    "zoo-hannover": ["Erlebnis-Zoo Hannover", "Zoo Hannover Sambesi"],
    "zoo-zoorasia": ["Yokohama Zoological Gardens Zoorasia", "Zoorasia Okapi"],
    "zoo-woodland-park": ["Woodland Park Zoo Seattle", "Woodland Park Zoo"],
    "zoo-werribee": ["Werribee Open Range Zoo", "Werribee Zoo giraffe"],
    "zoo-taipei": ["Taipei Zoo Pangolin Dome", "Taipei Zoo"],
    "zoo-nanjing-hongshan": ["Nanjing Hongshan Forest Zoo", "Red Panda zoo"],
    "zoo-oakland": ["Oakland Zoo gondola", "Oakland Zoo"],
    "zoo-berlin": ["Berlin Zoological Garden hippo", "Zoo Berlin"],
    "zoo-hagenbeck": ["Tierpark Hagenbeck Eismeer", "Tierpark Hagenbeck"],
    "zoo-blijdorp": ["Diergaarde Blijdorp Oceanium", "Blijdorp Zoo Rotterdam"],
    "zoo-houston": ["Houston Zoo", "Houston Zoo sea lion"],
    "mus-13": ["Toyota Commemorative Museum of Industry and Technology", "Toyota Museum Nagoya"],
    "mus-17": ["Cite de l'Automobile Mulhouse", "Musée National de l'Automobile Mulhouse"],
    "mus-20": ["Military Museum of the Chinese People's Revolution", "Beijing Military Museum"],
    "mus-26": ["Musee de l'Air et de l'Espace Le Bourget", "Le Bourget Air and Space Museum"],
    "mus-33": ["Museo Nazionale Scienza e Tecnologia Leonardo da Vinci", "Enrico Toti submarine Milan"],
    "mus-34": ["Pima Air and Space Museum", "Titan Missile Museum"],
    "mus-36": ["Chinese Navy Museum Qingdao", "PLA Navy Museum Qingdao"],
    "mus-37": ["Kronstadt Naval Museum submarine K-3", "K-3 Leninsky Komsomol submarine"],
    "mus-38": ["Kubinka Tank Museum", "Patriot Park Kubinka"],
    "mus-39": ["The Tank Museum Bovington", "Bovington Tank Museum"],
    "mus-40": ["Porsche Museum Stuttgart", "Porsche Museum"],
    "mus-41": ["BMW Museum Munich", "BMW Welt Munich"],
    "mus-42": ["Museo Ferrari Maranello", "Museo Enzo Ferrari Modena"],
    "mus-43": ["Autostadt Wolfsburg", "Volkswagen Autostadt"],
    "mus-44": ["Aeroscopia Toulouse", "Airbus Museum Toulouse"],
    "mus-45": ["China Railway Museum Beijing", "Beijing Railway Museum"],
    "mus-46": ["Chinese Aviation Museum Datangshan", "China Aviation Museum Beijing"],
    "mus-47": ["Deutsches Bergbau-Museum Bochum", "Bergbau Museum Bochum"],
    "mus-48": ["Ferropolis", "Ferropolis Bagger"],
    "mus-49": ["Space Center Houston", "Saturn V Houston"],
    "mus-50": ["Kyoto Railway Museum", "Umekoji Steam Locomotive Museum"],
    "mus-51": ["Yamato Museum Kure", "JMSDF Kure Museum"],
    "mus-52": ["Bletchley Park", "The National Museum of Computing Bletchley"],
    "mus-53": ["Battleship Missouri Memorial Pearl Harbor", "USS Missouri Pearl Harbor"],
    "mus-71": ["National Museum of Nuclear Science & History", "Nuclear Museum Albuquerque"],
    "mus-72": ["Wilhelm Bauer submarine Bremerhaven", "Deutsches Schiffahrtsmuseum"],
    "mus-74": ["Science and Industry Museum Manchester", "Museum of Science and Industry Manchester"],
    "mus-78": ["Shanghai Auto Museum", "Anting Auto Museum"],
    "mus-79": ["Museo Lamborghini", "Lamborghini Museum Sant'Agata"],
    "mus-80": ["Canada Aviation and Space Museum Ottawa", "Canada Science and Technology Museum"],
    "mus-81": ["Fram Museum Oslo", "Norwegian Petroleum Museum Stavanger"],
    "mus-82": ["Patriots Point USS Yorktown", "USS Yorktown Charleston"],
    "mus-87": ["SS Jeremiah O'Brien San Francisco", "San Francisco Maritime National Historical Park"],
    "mus-96": ["Zigong Salt History Museum", "Shenhai Well Zigong"],
    "mus-97": ["Industrial Museum of China Shenyang", "Shenyang Industrial Museum"],
    "mus-98": ["Qinghai Atomic City", "China nuclear weapon museum"],
    "mus-99": ["Wuhan Yangtze River Bridge", "Wuhan Bridge Museum"],
    "mus-100": ["Jiuquan Satellite Launch Center", "Long March rocket launch pad"],
    "are-sweden": ["Are ski resort Sweden", "Åreskutan ski"],
}

def strip_html(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

def api_search(q):
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{q} filetype:bitmap", "gsrlimit": 15,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 960,
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            time.sleep(0.18)
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(1.5 * (attempt + 1))
                continue
            return None
        except Exception:
            return None
    else:
        return None

    pages = sorted((data.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        t = p.get("title", "")
        if BAD.search(t) or ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        w, h = ii.get("width", 0), ii.get("height", 0)
        if w < 640 or h == 0 or w / h < 1.1 or w / h > 2.8:
            continue
        md = ii.get("extmetadata", {})
        lic = strip_html(md.get("LicenseShortName", {}).get("value"))
        return {
            "src": ii.get("thumburl") or ii.get("url"),
            "page": ii.get("descriptionurl"),
            "artist": strip_html(md.get("Artist", {}).get("value"))[:70] or "Wikimedia Commons",
            "license": lic or "CC",
            "title": t,
        }
    return None

def build_queries(item):
    iid = item["id"]
    if iid in CUSTOM_QUERIES:
        return CUSTOM_QUERIES[iid]
    name = item.get("name", "")
    m = re.search(r"[（(]([^()（）]*[A-Za-z][^()（）]*)[)）]", name)
    en = m.group(1).strip() if m else ""
    if not en and re.match(r"^[A-Za-z]", name):
        en = name
    zh = re.sub(r"\s*[（(].*?[)）]", "", name).strip()
    city = item.get("city") or item.get("state") or ""
    qs = []
    if en:
        clean_en = re.sub(r"\s*[&+＋/].*$", "", en).strip()
        qs.append(en)
        if clean_en != en:
            qs.append(clean_en)
    if item.get("venue"):
        v_en = re.search(r"[A-Za-z][A-Za-z0-9\s'&-]+", item["venue"])
        if v_en:
            qs.append(v_en.group(0).strip())
    qs.append(f"{zh} {city}".strip())
    qs.append(zh)
    if en and city:
        qs.append(f"{clean_en if en else zh} {item.get('country', '')}")
    return [q for q in qs if q]

def fetch_one(item):
    for q in build_queries(item):
        r = api_search(q)
        if r:
            return item["id"], r
    return item["id"], None

def main():
    existing = {}
    out_path = f"{ROOT}/images_themed.js"
    if os.path.exists(out_path):
        txt = open(out_path, encoding="utf-8").read()
        if "{" in txt and "}" in txt:
            try:
                existing = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])
            except Exception:
                existing = {}

    files = ["data_aquariums_zoos_museums.js", "data_themeparks.js", "data_ski.js", "data_shows.js"]
    js_code = "var window={};\n"
    for fn in files:
        p = f"{ROOT}/{fn}"
        if os.path.exists(p):
            js_code += open(p, encoding="utf-8").read() + "\n"
    js_code += """
    var all = [].concat(
      window.AQUARIUMS_TOP35 || [],
      window.ZOOS_TOP30 || [],
      window.US_SAFARI_PARKS_TOP10 || [],
      window.INDUSTRIAL_MUSEUMS_TOP100 || [],
      window.THEMEPARKS_TOP100 || [],
      window.WATERPARKS_TOP15 || [],
      window.SKI_RESORTS_TOP100 || [],
      window.SHOWS_TOP50 || []
    );
    JSON.stringify(all.map(function(x){return {id:x.id, name:x.name, city:x.city||x.state||'', country:x.country||'', venue:x.venue||'', category:x.category||''};}));
    """
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js_code], capture_output=True, text=True, check=True)
    items = [x for x in json.loads(out.stdout) if x.get("id")]
    todo = [x for x in items if x["id"] not in existing]
    print(f"Total items: {len(items)}, already cached: {len(existing)}, to fetch: {len(todo)}", file=sys.stderr)

    res = dict(existing)
    if todo:
        done_count = 0
        with cf.ThreadPoolExecutor(4) as ex:
            for iid, r in ex.map(fetch_one, todo):
                done_count += 1
                if r:
                    res[iid] = r
                    print(f"[{done_count}/{len(todo)} OK] {iid} -> {r['title']}", file=sys.stderr)
                else:
                    print(f"[{done_count}/{len(todo)} MISS] {iid}", file=sys.stderr)
                if done_count % 25 == 0:
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write("// Cover photos for Aquariums, Zoos, Safari Parks, Museums, Theme Parks, Ski Resorts & Shows from Wikimedia Commons\n")
                        f.write("window.THEMED_IMAGES = " + json.dumps(res, ensure_ascii=False, indent=1) + ";\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("// Cover photos for Aquariums, Zoos, Safari Parks, Museums, Theme Parks, Ski Resorts & Shows from Wikimedia Commons\n")
        f.write("window.THEMED_IMAGES = " + json.dumps(res, ensure_ascii=False, indent=1) + ";\n")
    print(f"Saved {len(res)}/{len(items)} images to images_themed.js", file=sys.stderr)

if __name__ == "__main__":
    main()

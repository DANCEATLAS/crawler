"""Source fetchers: Wikipedia, Wikidata, Wikimedia Commons, UNESCO ICH, MusicBrainz.

Every fetcher returns plain dicts and never raises on a missing page (returns None).
All fetched text is cached per run under pipeline_state/cache so the QC stage can
verify quotes against exactly what the research stage saw.
"""
import re, json, time, urllib.parse, os
from .common import http, get_json, HttpError, norm, warn, log, jload, jsave, state_path, sha1

WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_REST = "https://en.wikipedia.org/api/rest_v1"
WIKIDATA_API = "https://www.wikidata.org/w/api.php"
WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
UNESCO_API = "https://data.unesco.org/api/explore/v2.1/catalog/datasets/ich001/records"
MB_API = "https://musicbrainz.org/ws/2"

CACHE_DIR = state_path("cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def cached(key, fn, ttl_days=14):
    p = os.path.join(CACHE_DIR, sha1(key) + ".json")
    c = jload(p)
    if c and (time.time() - c.get("_t", 0)) < ttl_days * 86400:
        return c.get("v")
    v = fn()
    jsave(p, {"_t": time.time(), "k": key[:200], "v": v})
    return v

def _title_from_url(url):
    if not url:
        return None
    m = re.search(r"wikipedia\.org/wiki/([^#?]+)", url)
    return urllib.parse.unquote(m.group(1)).replace("_", " ") if m else None

# ----------------------------------------------------------------- Wikipedia
def wiki_page(title_or_url):
    """Full plain-text extract + metadata of an English Wikipedia article."""
    title = _title_from_url(title_or_url) or title_or_url
    if not title:
        return None
    def fetch():
        params = {"action": "query", "prop": "extracts|pageprops|categories|info|pageimages", "explaintext": "1",
                  "redirects": "1", "titles": title, "format": "json", "cllimit": "50", "inprop": "url",
                  "piprop": "original", "formatversion": "2"}
        j = get_json(WIKI_API + "?" + urllib.parse.urlencode(params))
        pages = (j.get("query") or {}).get("pages") or []
        if not pages or pages[0].get("missing"):
            return None
        p = pages[0]
        txt = p.get("extract") or ""
        cats = [c.get("title", "").replace("Category:", "") for c in p.get("categories") or []]
        return {"title": p.get("title"), "url": p.get("fullurl") or ("https://en.wikipedia.org/wiki/" + urllib.parse.quote(p.get("title", "").replace(" ", "_"))),
                "pageid": p.get("pageid"), "qid": (p.get("pageprops") or {}).get("wikibase_item"),
                "disambiguation": "disambiguation" in (p.get("pageprops") or {}),
                "text": txt, "categories": cats, "image": (p.get("original") or {}).get("source"),
                "length": len(txt)}
    try:
        return cached("wiki:" + title, fetch)
    except HttpError as e:
        warn("wiki_page", title, e.code)
        return None

def wiki_search(query, limit=5):
    params = {"action": "query", "list": "search", "srsearch": query, "srlimit": str(limit), "format": "json", "formatversion": "2"}
    try:
        j = get_json(WIKI_API + "?" + urllib.parse.urlencode(params))
        return [{"title": r.get("title"), "snippet": re.sub(r"<[^>]+>", "", r.get("snippet", "")), "pageid": r.get("pageid")} for r in (j.get("query") or {}).get("search") or []]
    except Exception as e:
        warn("wiki_search", query, e)
        return []

def wiki_category_members(category, limit=500, cmtype="page"):
    """Titles in a category (follows continuation)."""
    out, cont = [], None
    while len(out) < limit:
        params = {"action": "query", "list": "categorymembers", "cmtitle": "Category:" + category, "cmlimit": "500",
                  "cmtype": cmtype, "format": "json", "formatversion": "2"}
        if cont:
            params["cmcontinue"] = cont
        try:
            j = get_json(WIKI_API + "?" + urllib.parse.urlencode(params))
        except Exception as e:
            warn("wiki_category_members", category, e)
            break
        for m in (j.get("query") or {}).get("categorymembers") or []:
            out.append(m.get("title"))
        cont = (j.get("continue") or {}).get("cmcontinue")
        if not cont:
            break
    return out[:limit]

def wiki_links_from_page(title):
    """All wiki links of a page (used for 'List of ... dances' pages)."""
    out, cont = [], None
    while True:
        params = {"action": "query", "prop": "links", "titles": title, "pllimit": "500", "plnamespace": "0", "format": "json", "formatversion": "2"}
        if cont:
            params["plcontinue"] = cont
        try:
            j = get_json(WIKI_API + "?" + urllib.parse.urlencode(params))
        except Exception as e:
            warn("wiki_links", title, e)
            break
        for p in (j.get("query") or {}).get("pages") or []:
            out += [l.get("title") for l in p.get("links") or []]
        cont = (j.get("continue") or {}).get("plcontinue")
        if not cont:
            break
    return out

# ----------------------------------------------------------------- Wikidata
PROPS = {"P31": "instance_of", "P279": "subclass_of", "P495": "country_of_origin", "P17": "country", "P571": "inception",
         "P18": "image", "P373": "commons_category", "P1435": "heritage_designation", "P2578": "studies", "P136": "genre",
         "P1705": "native_label", "P1449": "nickname", "P460": "said_to_be_the_same_as", "P737": "influenced_by",
         "P941": "inspired_by", "P2283": "uses", "P1535": "used_by", "P276": "location", "P625": "coordinates", "P910": "main_category"}

def wikidata_entity(qid):
    if not qid:
        return None
    def fetch():
        j = get_json(f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json")
        ent = (j.get("entities") or {}).get(qid)
        if not ent:
            return None
        out = {"qid": qid, "labels": {k: v.get("value") for k, v in (ent.get("labels") or {}).items() if k in ("en", "es", "fr", "pt", "de", "it", "ar", "hi", "ja", "zh", "ru")},
               "aliases": [a.get("value") for a in (ent.get("aliases") or {}).get("en", [])],
               "description": ((ent.get("descriptions") or {}).get("en") or {}).get("value"),
               "sitelinks": {k: v.get("title") for k, v in (ent.get("sitelinks") or {}).items() if k.endswith("wiki") and k in ("enwiki", "eswiki", "frwiki", "ptwiki", "dewiki", "itwiki")},
               "claims": {}}
        for pid, name in PROPS.items():
            vals = []
            for c in (ent.get("claims") or {}).get(pid, []):
                dv = ((c.get("mainsnak") or {}).get("datavalue") or {}).get("value")
                if dv is None:
                    continue
                if isinstance(dv, dict):
                    if "id" in dv:
                        vals.append(dv["id"])
                    elif "time" in dv:
                        vals.append(dv["time"])
                    elif "latitude" in dv:
                        vals.append({"lat": dv["latitude"], "lng": dv["longitude"]})
                    elif "text" in dv:
                        vals.append(dv["text"])
                else:
                    vals.append(dv)
            if vals:
                out["claims"][name] = vals
        return out
    try:
        return cached("wd:" + qid, fetch)
    except HttpError as e:
        warn("wikidata_entity", qid, e.code)
        return None

def wikidata_labels(qids):
    """Batch labels for QIDs (en)."""
    qids = [q for q in dict.fromkeys(qids) if q and re.match(r"^Q\d+$", q)]
    out = {}
    for i in range(0, len(qids), 50):
        batch = qids[i:i + 50]
        params = {"action": "wbgetentities", "ids": "|".join(batch), "props": "labels", "languages": "en", "format": "json"}
        try:
            j = get_json(WIKIDATA_API + "?" + urllib.parse.urlencode(params))
            for q, e in (j.get("entities") or {}).items():
                out[q] = ((e.get("labels") or {}).get("en") or {}).get("value")
        except Exception as e:
            warn("wikidata_labels", e)
    return out

def sparql(query):
    u = WIKIDATA_SPARQL + "?" + urllib.parse.urlencode({"query": query, "format": "json"})
    j = get_json(u, headers={"Accept": "application/sparql-results+json"}, timeout=120)
    rows = []
    for b in (j.get("results") or {}).get("bindings") or []:
        rows.append({k: v.get("value") for k, v in b.items()})
    return rows

DANCE_CLASS_LABELS = ("dance style", "folk dance", "dance genre", "social dance", "ritual dance", "traditional dance",
                      "ceremonial dance", "partner dance", "street dance", "circle dance", "line dance", "couple dance",
                      "war dance", "sword dance", "court dance", "classical dance", "type of dance", "dance form", "group dance",
                      "solo dance", "ballroom dance", "religious dance", "national dance", "regional dance", "dance move",
                      "Latin dance", "African dance", "folk dance of India", "Indian classical dance", "masked dance", "fan dance")

def wikidata_dance_classes():
    """QIDs of the classes dances are usually instances of (looked up by English label, cached for the run)."""
    def fetch():
        out = {}
        for label in DANCE_CLASS_LABELS:
            params = {"action": "wbsearchentities", "search": label, "language": "en", "type": "item", "limit": "5", "format": "json"}
            try:
                j = get_json(WIKIDATA_API + "?" + urllib.parse.urlencode(params))
            except Exception as e:
                warn("wikidata class search", label, e)
                continue
            hits = j.get("search") or []
            exact = [h for h in hits if (h.get("label") or "").lower() == label.lower()]
            for h in (exact or hits[:1]):
                if h.get("id"):
                    out[h["id"]] = h.get("label")
        return out
    try:
        return cached("wd:dance-classes", fetch, ttl_days=30) or {}
    except Exception as e:
        warn("wikidata_dance_classes", e)
        return {}

def wikidata_dances(limit=5000):
    """Items that are a kind of dance with an English Wikipedia article.

    Pass 1: instances of the usual dance classes (dance style, folk dance, social dance, ...; class ids looked up by label).
    Pass 2: the strict subclass walk from 'dance' (Q11639). A global label scan over all classes was tried first
    and times out on the query service (504), so the class list is bounded on purpose."""
    classes = wikidata_dance_classes()
    rows, seen = [], set()
    queries = []
    if classes:
        values = " ".join("wd:" + q for q in classes)
        queries.append(("classes", f"""
    SELECT DISTINCT ?item ?itemLabel ?article ?countryLabel WHERE {{
      VALUES ?cls {{ {values} }}
      ?item wdt:P31 ?cls .
      ?article schema:about ?item ; schema:isPartOf <https://en.wikipedia.org/> .
      OPTIONAL {{ ?item wdt:P495 ?country . }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }} LIMIT {int(limit)}"""))
    queries.append(("strict", f"""
    SELECT DISTINCT ?item ?itemLabel ?article ?countryLabel WHERE {{
      ?item wdt:P31/wdt:P279* wd:Q11639 .
      ?article schema:about ?item ; schema:isPartOf <https://en.wikipedia.org/> .
      OPTIONAL {{ ?item wdt:P495 ?country . }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }} LIMIT {int(limit)}"""))
    for name, q in queries:
        try:
            got = sparql(q)
            log(f"wikidata_dances: {name} query -> {len(got)} rows (classes={len(classes)})")
        except Exception as e:
            warn("wikidata_dances", name, e)
            continue
        for r in got:
            k = r.get("item")
            if k and k not in seen:
                seen.add(k); rows.append(r)
    return rows[:limit]

# ----------------------------------------------------------------- Wikimedia Commons (licensed images)
FREE_LICENSES = ("cc0", "cc by", "cc-by", "public domain", "pd-", "pd ", "gfdl", "attribution")

def commons_images_for_page(wiki_title, limit=12):
    """Images used on the Wikipedia article, with license metadata. Keeps only free licenses."""
    if not wiki_title:
        return []
    def fetch():
        params = {"action": "query", "prop": "images", "titles": wiki_title, "imlimit": "50", "format": "json", "formatversion": "2", "redirects": "1"}
        j = get_json(WIKI_API + "?" + urllib.parse.urlencode(params))
        files = []
        for p in (j.get("query") or {}).get("pages") or []:
            files += [im.get("title") for im in p.get("images") or []]
        files = [f for f in files if re.search(r"\.(jpe?g|png|webp)$", f or "", re.I) and not re.search(r"(icon|logo|flag of|map of|wiki|symbol|commons-|edit-|question|ambox|padlock|stub|crystal|nuvola|speaker)", f, re.I)]
        return commons_file_info(files[:limit])
    try:
        return cached("commons:" + wiki_title, fetch)
    except Exception as e:
        warn("commons_images_for_page", wiki_title, e)
        return []

def commons_file_info(file_titles):
    out = []
    for i in range(0, len(file_titles), 20):
        batch = file_titles[i:i + 20]
        params = {"action": "query", "prop": "imageinfo", "titles": "|".join(batch), "iiprop": "url|extmetadata|size|mime",
                  "iiurlwidth": "1280", "format": "json", "formatversion": "2"}
        try:
            j = get_json(COMMONS_API + "?" + urllib.parse.urlencode(params))
        except Exception as e:
            warn("commons_file_info", e)
            continue
        for p in (j.get("query") or {}).get("pages") or []:
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata") or {}
            lic = (em.get("LicenseShortName") or {}).get("value") or (em.get("License") or {}).get("value") or ""
            if not any(k in lic.lower() for k in FREE_LICENSES):
                continue
            w, h = ii.get("width") or 0, ii.get("height") or 0
            if w < 600 or h < 400:
                continue
            artist = re.sub(r"<[^>]+>", "", (em.get("Artist") or {}).get("value") or "").strip()
            desc = re.sub(r"<[^>]+>", "", (em.get("ImageDescription") or {}).get("value") or "").strip()
            out.append({"title": p.get("title"), "url": ii.get("url"), "thumb": ii.get("thumburl") or ii.get("url"),
                        "width": w, "height": h, "license": lic, "license_url": (em.get("LicenseUrl") or {}).get("value"),
                        "artist": artist[:200], "description": desc[:400],
                        "source_page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote((p.get("title") or "").replace(" ", "_")),
                        "attribution": (artist + " / Wikimedia Commons / " + lic).strip(" /")})
    return out

# ----------------------------------------------------------------- UNESCO ICH
# Field names verified against the live dataset (data.unesco.org, dataset ich001, Oct 2026):
# uuid, ich_public_ref, inscription_year, title_en, description_en, type_of_element_en, type_acronym,
# countries (ISO-2 list), http_url_en, concepts_primary_names, main_image_url, ...
UNESCO_FIELDS = "ich_public_ref,inscription_year,title_en,description_en,type_of_element_en,type_acronym,countries,http_url_en,concepts_primary_names"

def _iso_names():
    from .taxonomy import COUNTRIES
    out = {}
    for name, (iso, _) in COUNTRIES.items():
        out.setdefault(iso, name.title().replace("'S", "'s"))
    return out

def unesco_ich_index():
    """Every ICH inscription: ref, title, countries (names), year, url, description, type, concepts."""
    def fetch():
        idx, off, iso = [], 0, _iso_names()
        while True:
            u = UNESCO_API + "?" + urllib.parse.urlencode({"limit": "100", "offset": str(off), "select": UNESCO_FIELDS})
            try:
                d = get_json(u)
            except Exception as e:
                warn("unesco", e)
                break
            res = d.get("results") or []
            if not res:
                break
            for r in res:
                cs = r.get("countries") or []
                if isinstance(cs, str):
                    cs = [c.strip() for c in cs.split(",") if c.strip()]
                names = [iso.get(c, c) for c in cs]
                idx.append({"ref": r.get("ich_public_ref"), "title": r.get("title_en"), "countries": ", ".join(names), "country_codes": cs,
                            "year": r.get("inscription_year"), "url": r.get("http_url_en") or f"https://ich.unesco.org/en/RL/{r.get('ich_public_ref')}",
                            "description": r.get("description_en") or "", "type": r.get("type_of_element_en"), "list": r.get("type_acronym"),
                            "concepts": r.get("concepts_primary_names") or []})
            off += 100
            if off >= (d.get("total_count") or 0) or off > 5000:
                break
        if not idx:
            raise RuntimeError("UNESCO index empty (API unreachable?)")
        return idx
    try:
        return cached("unesco:index", fetch, ttl_days=30) or []
    except Exception as e:
        warn("unesco_ich_index", e)
        return []

# ----------------------------------------------------------------- MusicBrainz (album verification)
def mb_search_release_group(artist, title):
    """Return the best-matching release group (album) or None. Respects MB rate limit (1 req/s)."""
    q = f'releasegroup:"{title}" AND artist:"{artist}"'
    u = MB_API + "/release-group/?" + urllib.parse.urlencode({"query": q, "fmt": "json", "limit": "5"})
    def fetch():
        time.sleep(1.05)
        j = get_json(u, headers={"User-Agent": "DancingAtlasPipeline/3.0 (edan@dancingatlas; contact via github.com/DANCEATLAS)"})
        best = None
        for rg in j.get("release-groups") or []:
            score = rg.get("score") or 0
            arts = ", ".join(a.get("name", "") for a in [c.get("artist", {}) for c in rg.get("artist-credit") or []])
            if score >= 85 and (norm(title) in norm(rg.get("title", "")) or norm(rg.get("title", "")) in norm(title)):
                cand = {"mbid": rg.get("id"), "title": rg.get("title"), "artist": arts, "type": rg.get("primary-type"),
                        "first_release_date": rg.get("first-release-date"), "score": score,
                        "url": "https://musicbrainz.org/release-group/" + str(rg.get("id"))}
                if best is None or score > best["score"]:
                    best = cand
        return best
    try:
        return cached("mb:" + norm(artist) + "|" + norm(title), fetch, ttl_days=60)
    except Exception as e:
        warn("mb_search", artist, title, e)
        return None

def mb_search_recording(artist, title):
    q = f'recording:"{title}" AND artist:"{artist}"'
    u = MB_API + "/recording/?" + urllib.parse.urlencode({"query": q, "fmt": "json", "limit": "3"})
    try:
        time.sleep(1.05)
        j = get_json(u)
        for r in j.get("recordings") or []:
            if (r.get("score") or 0) >= 85:
                return {"mbid": r.get("id"), "title": r.get("title"), "url": "https://musicbrainz.org/recording/" + str(r.get("id"))}
    except Exception as e:
        warn("mb_search_recording", e)
    return None

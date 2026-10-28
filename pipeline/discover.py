"""Discovery: find dances the Atlas does not have yet.

Sources: Wikidata (instances of dance / folk dance with an enwiki article),
Wikipedia "Dances by country" categories and list pages, and UNESCO ICH titles.
Candidates are de-duplicated against the catalogue (slug, name, aliases, QID,
fuzzy name) and queued in pipeline_state/candidates.json for the research stage.
"""
import re, os
from .common import log, warn, norm, slugify, load_state, save_state, now_iso, Report, Supabase
from .catalog import load_catalog, NameIndex
from .taxonomy import country_lookup
from . import sources as S

BAD_TITLE = re.compile(r"\b(film|movie|album|song|single|ep|band|company|troupe|school|festival|competition|championship|tv series|season|episode|discography|list of|category:|template:|\(.*?(film|album|song|band|novel|book|game|musical)\))\b", re.I)
BAD_CATS = re.compile(r"(births|deaths|living people|films|albums|songs|singles|companies|television|video games|novels|people|dancers|choreographers|musicians|bands|record labels|studios|stubs?$)", re.I)
GOOD_CATS = re.compile(r"(dance|dances|dancing|choreograph|folklore|traditional music|ceremon|ritual|intangible cultural heritage)", re.I)
DANCE_WORDS = re.compile(r"(dance|danza|danse|dans|baile|bailes|tanz|folk|ballet|choreo|raqs|odori|mai\b|nritya|natyam|attam|kolattam|tari\b|tarian|ngoma|bal\b|waltz|polka|mazurka|samba|rumba|cumbia|tango|hula|haka)", re.I)

def _candidate(name, url=None, qid=None, country=None, via=None):
    return {"name": name.strip(), "wikipedia_url": url, "wikidata_qid": qid, "country": country, "via": [via] if via else [],
            "status": "queued", "found_at": now_iso()}

def harvest_wikidata(limit):
    out = []
    for r in S.wikidata_dances(limit=limit):
        name = r.get("itemLabel") or ""
        qid = (r.get("item") or "").rsplit("/", 1)[-1]
        if not name or name == qid or BAD_TITLE.search(name):
            continue
        out.append(_candidate(name, r.get("article"), qid, r.get("countryLabel"), "wikidata"))
    log(f"discover: wikidata {len(out)} items")
    return out

CATEGORY_ROOTS = ["Dances by country", "Folk dances", "Dance by genre", "Dance in Africa", "Dance in Asia", "Dance in Europe",
                  "Dance in South America", "Dance in North America", "Dance in Oceania", "Latin dances", "Partner dances",
                  "Street dance", "Ritual dances", "Indian classical dance", "Sword dances", "Circle dances"]
LIST_PAGES = ["List of folk dances by country", "List of dances", "List of dance style categories", "List of ethnic, regional, and folk dances by origin",
              "List of Indian folk dances", "List of African dances", "List of Latin American dances", "List of Philippine folk dances"]

def harvest_wikipedia(max_cats=120):
    titles = {}
    cats = []
    for root in CATEGORY_ROOTS:
        subs = S.wiki_category_members(root, limit=300, cmtype="subcat")
        cats += [c.replace("Category:", "") for c in subs if GOOD_CATS.search(c) and not BAD_CATS.search(c)]
        for t in S.wiki_category_members(root, limit=300, cmtype="page"):
            titles.setdefault(t, "cat:" + root)
    for c in list(dict.fromkeys(cats))[:max_cats]:
        for t in S.wiki_category_members(c, limit=300, cmtype="page"):
            titles.setdefault(t, "cat:" + c)
    for lp in LIST_PAGES:
        for t in S.wiki_links_from_page(lp):
            titles.setdefault(t, "list:" + lp)
    out = []
    for t, via in titles.items():
        if not t or BAD_TITLE.search(t) or t.startswith(("List of", "Category:", "Template:", "Portal:", "Wikipedia:")):
            continue
        out.append(_candidate(t, "https://en.wikipedia.org/wiki/" + t.replace(" ", "_"), None, None, via))
    log(f"discover: wikipedia {len(out)} titles from {len(cats)} categories + lists")
    return out

def harvest_unesco():
    out = []
    for e in S.unesco_ich_index():
        t = e.get("title") or ""
        if DANCE_WORDS.search(t):
            out.append(_candidate(t, None, None, (e.get("countries") or "").split(",")[0].strip() or None, "unesco:" + str(e.get("ref"))))
    log(f"discover: unesco {len(out)} dance-related inscriptions")
    return out

def run(max_new=60, wikidata_limit=4000, do_wikipedia=True, do_unesco=True):
    rep = Report("discover")
    sb = Supabase()
    catalog = load_catalog(sb)
    idx = NameIndex(catalog)
    qids = {d.get("wikidata_qid") for d in catalog if d.get("wikidata_qid")}
    state = load_state("candidates.json", {})
    seen_slugs = set(state.keys())
    raw = harvest_wikidata(wikidata_limit)
    if do_wikipedia:
        raw += harvest_wikipedia()
    if do_unesco:
        raw += harvest_unesco()
    rep.inc("harvested", len(raw))
    # merge by normalized name
    merged = {}
    for c in raw:
        k = norm(c["name"])
        if not k:
            continue
        m = merged.setdefault(k, c)
        if m is not c:
            m["via"] = list(dict.fromkeys(m["via"] + c["via"]))
            for f in ("wikipedia_url", "wikidata_qid", "country"):
                if not m.get(f) and c.get(f):
                    m[f] = c[f]
    added = 0
    for k, c in merged.items():
        slug = slugify(c["name"])
        if not slug or slug in seen_slugs or slug in idx.by_slug:
            rep.inc("already_known"); continue
        if c.get("wikidata_qid") and c["wikidata_qid"] in qids:
            rep.inc("dup_qid"); continue
        found, score = idx.find(c["name"])
        if found:
            rep.inc("dup_name" if score >= 0.999 else "dup_fuzzy")
            if score < 0.999:
                state[slug] = dict(c, slug=slug, status="duplicate_of", duplicate_of=found, score=round(score, 3))
            continue
        # must look like a dance: wikidata-sourced is trusted; others need a dance word in title or via a dance category
        trusted = any(v.startswith("wikidata") or v.startswith("unesco") for v in c["via"])
        if not trusted and not DANCE_WORDS.search(c["name"]) and not any("dance" in v.lower() for v in c["via"]):
            rep.inc("not_dance_like"); continue
        if added >= max_new:
            rep.inc("deferred"); continue
        iso, region = country_lookup(c.get("country") or "")
        state[slug] = dict(c, slug=slug, country_code=iso, region=region)
        seen_slugs.add(slug); added += 1
    rep.inc("queued_new", added)
    save_state("candidates.json", state)
    queued = sum(1 for v in state.values() if v.get("status") == "queued")
    rep.note(f"candidate queue: {queued} queued, {len(state)} tracked")
    return rep.finish()

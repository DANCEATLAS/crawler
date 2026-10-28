"""Research: build a source-grounded, citation-verified profile for one dance.

Evidence (Wikipedia en + up to two other languages, Wikidata, UNESCO, Commons)
is fetched first; the model may only write what the evidence supports and must
attach a verbatim quote to every claim.  Quotes are then checked mechanically
against the fetched text, so hallucinated facts are caught before QC.
"""
import re, os, json
from .common import LLM, log, warn, norm, slugify, now_iso, jsave, jload, state_path, sha1, Report, load_state, save_state, Supabase
from .catalog import load_catalog, NameIndex, completeness
from .taxonomy import FAMILIES, REGIONS, country_lookup, sacred_hint
from . import sources as S

RESULTS_DIR = os.environ.get("RESEARCH_DIR", "research_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

EDITORIAL = """You are the senior editor of the Dancing Atlas, an encyclopedia of every living dance tradition, written to the standard of a major documentary studio.
RULES
1. Write ONLY what the provided sources support. Never invent dates, names, places, numbers or claims. If the sources are thin, write less and list the gaps.
2. Every factual sentence must be traceable: produce a `claims` list where each claim carries the source URL and a VERBATIM quote (6-30 words, copied exactly) from that source's text that supports it.
3. Honour the culture: describe people and communities with respect and precision; name the people and places; no exoticising, no stereotypes, no "mysterious East" language. Where a dance is sacred or restricted, say so plainly and note what outsiders should not do.
4. Voice: vivid, concrete, documentary. One specific image per paragraph (a person, a place, an object, a year, a sound). Avoid academic filler ("foundational", "codified", "rich heritage", "communal spirit"), hedging adverbs ("arguably", "often") and generic dates without context.
5. The `insight` is the gate: ONE sentence (max 220 characters) carrying one startling fact, contradiction, precise moment or concrete image that makes a stranger want to stay. Not literary criticism.
6. `how_it_is_danced` must be usable for teaching later: formation, who dances, basic footwork or body movement, rhythm/meter, typical tempo, key gestures, how a beginner would start. Only what sources support; if technique is not described in the sources, say "technique not described in sources".
7. Albums: list recordings or artists that the sources name as central to this dance's music. Mark each with the source. Do not guess.
8. Taxonomy: region must be one of {regions}; family one of {families}.
Output JSON with keys: name, tagline (<=90 chars), insight (<=220 chars), profile (3-5 sentences), profile_long (600-1200 words of continuous prose using the sections), sections{{origins_and_history, how_it_is_danced, music_and_instruments, costume_and_setting, occasions_and_meaning, notable_figures, regional_variants, lineage}}, era (short, e.g. "19th century"), country, region, family, aliases[], related[] (names of other dances), is_sacred (bool), sacred_note, unesco (bool), teaching{{basic_steps[] (ordered, each one movement), rhythm, formation, level_notes}}, albums[] ({{title, artist, source}}), claims[] ({{text, source, quote}}), confidence (0-1), gaps[]."""

def _trim(txt, n):
    txt = re.sub(r"\n{3,}", "\n\n", txt or "")
    return txt[:n]

def gather_evidence(d):
    """d: catalogue entry or candidate. Returns evidence dict with fetched texts."""
    ev = {"fetched_at": now_iso(), "sources": []}
    name = d.get("name") or d.get("slug")
    wp = None
    if d.get("wikipedia_url"):
        wp = S.wiki_page(d["wikipedia_url"])
    if (not wp or wp.get("disambiguation") or (wp.get("length") or 0) < 400):
        for q in (name + " dance", name):
            for r in S.wiki_search(q, limit=4):
                cand = S.wiki_page(r["title"])
                if cand and not cand.get("disambiguation") and (cand.get("length") or 0) >= 400 and re.search(r"danc", (cand.get("text") or "")[:3000], re.I):
                    wp = cand; break
            if wp and not wp.get("disambiguation"):
                break
    if wp and not wp.get("disambiguation"):
        ev["wikipedia"] = {"title": wp["title"], "url": wp["url"], "qid": wp.get("qid"), "categories": wp.get("categories", [])[:30],
                           "text": _trim(wp["text"], 16000), "image": wp.get("image")}
        ev["sources"].append(wp["url"])
    qid = d.get("wikidata_qid") or (wp or {}).get("qid")
    wd = S.wikidata_entity(qid) if qid else None
    if wd:
        labels = S.wikidata_labels([v for k in ("country_of_origin", "country", "heritage_designation", "instance_of", "subclass_of", "genre", "influenced_by", "location") for v in wd["claims"].get(k, []) if isinstance(v, str)])
        facts = {}
        for k, vals in wd["claims"].items():
            facts[k] = [labels.get(v, v) if isinstance(v, str) else v for v in vals]
        ev["wikidata"] = {"qid": qid, "description": wd.get("description"), "aliases": wd.get("aliases"), "labels": wd.get("labels"), "facts": facts, "url": "https://www.wikidata.org/wiki/" + qid}
        ev["sources"].append(ev["wikidata"]["url"])
        # other-language articles for depth
        extra = []
        for lang in ("es", "fr", "pt", "de", "it"):
            t = (wd.get("sitelinks") or {}).get(lang + "wiki")
            if t and len(extra) < 2:
                try:
                    api = f"https://{lang}.wikipedia.org/w/api.php"
                    from urllib.parse import urlencode
                    from .common import get_json
                    j = get_json(api + "?" + urlencode({"action": "query", "prop": "extracts", "explaintext": "1", "titles": t, "format": "json", "formatversion": "2", "redirects": "1"}))
                    p = ((j.get("query") or {}).get("pages") or [{}])[0]
                    if p.get("extract") and len(p["extract"]) > 600:
                        url = f"https://{lang}.wikipedia.org/wiki/" + t.replace(" ", "_")
                        extra.append({"lang": lang, "title": t, "url": url, "text": _trim(p["extract"], 6000)})
                        ev["sources"].append(url)
                except Exception as e:
                    warn("other-lang wiki", lang, t, e)
        if extra:
            ev["wikipedia_other"] = extra
    # UNESCO
    try:
        idx = S.unesco_ich_index()
        nn = norm(name)
        hits = [e for e in idx if nn and (nn in norm(e.get("title")) or norm(e.get("title")) in nn) and len(nn) >= 5]
        if hits:
            h = hits[0]
            ev["unesco"] = {"ref": h.get("ref"), "title": h.get("title"), "countries": h.get("countries"), "year": h.get("year"),
                            "url": f"https://ich.unesco.org/en/RL/{h.get('ref')}"}
            ev["sources"].append(ev["unesco"]["url"])
    except Exception as e:
        warn("unesco match", e)
    # Commons images (licensed)
    if ev.get("wikipedia"):
        ev["images"] = S.commons_images_for_page(ev["wikipedia"]["title"], limit=12)[:8]
    ev["text_hash"] = sha1(json.dumps([ev.get("wikipedia", {}).get("text", ""), [x["text"] for x in ev.get("wikipedia_other", [])]]))
    return ev

def _source_texts(ev):
    texts = {}
    if ev.get("wikipedia"):
        texts[ev["wikipedia"]["url"]] = ev["wikipedia"]["text"]
    for x in ev.get("wikipedia_other", []):
        texts[x["url"]] = x["text"]
    if ev.get("wikidata"):
        texts[ev["wikidata"]["url"]] = json.dumps(ev["wikidata"]["facts"], ensure_ascii=False) + " " + str(ev["wikidata"].get("description") or "") + " " + " ".join(ev["wikidata"].get("aliases") or [])
    if ev.get("unesco"):
        texts[ev["unesco"]["url"]] = json.dumps(ev["unesco"], ensure_ascii=False)
    return texts

def verify_claims(claims, ev):
    """Check each claim's quote against the fetched source text. Returns (verified_claims, stats)."""
    texts = {u: norm(t) for u, t in _source_texts(ev).items()}
    out, ok = [], 0
    for c in claims or []:
        q = norm(c.get("quote") or "")
        src = c.get("source") or ""
        t = texts.get(src)
        if t is None:  # tolerate URL variants (mobile, trailing slash)
            for u, tt in texts.items():
                if src and (u.rstrip("/") == src.rstrip("/") or norm(u) == norm(src)):
                    t = tt; break
        supported = False
        if t and len(q.split()) >= 4:
            if q in t:
                supported = True
            else:  # fuzzy: 5-gram overlap
                grams = [" ".join(q.split()[i:i + 5]) for i in range(max(1, len(q.split()) - 4))]
                hit = sum(1 for g in grams if g in t)
                supported = hit / max(1, len(grams)) >= 0.6
        c = dict(c, supported=supported)
        ok += 1 if supported else 0
        out.append(c)
    n = len(out)
    return out, {"claims": n, "supported": ok, "rate": round(ok / n, 3) if n else 0.0}

def verify_albums(albums, max_n=8):
    verified, unverified = [], []
    for a in (albums or [])[:max_n]:
        t, ar = (a.get("title") or "").strip(), (a.get("artist") or "").strip()
        if not t or not ar:
            continue
        rg = S.mb_search_release_group(ar, t)
        if rg:
            verified.append({"title": rg["title"], "artist": rg["artist"] or ar, "year": (rg.get("first_release_date") or "")[:4] or None,
                             "mbid": rg["mbid"], "musicbrainz_url": rg["url"], "type": rg.get("type"), "source": a.get("source"), "verified": True})
        else:
            unverified.append(dict(a, verified=False))
    return verified, unverified

def _s(v, sep="\n\n"):
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return sep.join(_s(x, sep) for x in v if x not in (None, ""))
    if isinstance(v, dict):
        return sep.join(f"{k}: {_s(x, sep)}" for k, x in v.items())
    return str(v)

def normalize(comp):
    """Coerce the model output into the shapes the rest of the pipeline expects."""
    if not isinstance(comp, dict):
        return None
    c = dict(comp)
    for k in ("name", "tagline", "insight", "profile", "profile_long", "era", "country", "region", "family", "sacred_note"):
        c[k] = _s(c.get(k), " ").strip() if k != "profile_long" else _s(c.get(k)).strip()
    secs = c.get("sections") if isinstance(c.get("sections"), dict) else {}
    c["sections"] = {k: _s(v).strip() for k, v in secs.items()}
    if not c["profile_long"] and c["sections"]:
        c["profile_long"] = "\n\n".join(v for v in c["sections"].values() if v)
    for k in ("aliases", "related", "gaps"):
        v = c.get(k)
        c[k] = [str(x).strip() for x in v if str(x).strip()] if isinstance(v, list) else ([str(v).strip()] if v else [])
    c["claims"] = [x for x in (c.get("claims") or []) if isinstance(x, dict)]
    c["albums"] = [x for x in (c.get("albums") or []) if isinstance(x, dict)]
    t = c.get("teaching") if isinstance(c.get("teaching"), dict) else {}
    steps = t.get("basic_steps")
    t["basic_steps"] = [str(x).strip() for x in steps if str(x).strip()] if isinstance(steps, list) else ([str(steps)] if steps else [])
    for k in ("rhythm", "formation", "level_notes"):
        t[k] = _s(t.get(k), " ").strip()
    c["teaching"] = t
    c["is_sacred"] = bool(c.get("is_sacred"))
    c["unesco"] = bool(c.get("unesco"))
    try:
        c["confidence"] = float(c.get("confidence") or 0)
    except Exception:
        c["confidence"] = 0.0
    return c

def compose(d, ev, llm):
    """Ask the model for the structured profile. Returns dict or None."""
    src_blocks = []
    if ev.get("wikipedia"):
        src_blocks.append(f"SOURCE: {ev['wikipedia']['url']}\n{ev['wikipedia']['text']}")
    for x in ev.get("wikipedia_other", []):
        src_blocks.append(f"SOURCE: {x['url']} (language: {x['lang']})\n{x['text']}")
    if ev.get("wikidata"):
        src_blocks.append(f"SOURCE: {ev['wikidata']['url']}\nWikidata facts: {json.dumps(ev['wikidata']['facts'], ensure_ascii=False)}\nDescription: {ev['wikidata'].get('description')}\nAliases: {ev['wikidata'].get('aliases')}")
    if ev.get("unesco"):
        src_blocks.append(f"SOURCE: {ev['unesco']['url']}\nUNESCO Intangible Cultural Heritage inscription: {json.dumps(ev['unesco'], ensure_ascii=False)}")
    if not src_blocks:
        return None
    existing = {k: d.get(k) for k in ("name", "country", "region", "era", "tagline", "insight", "profile", "aliases", "related") if d.get(k)}
    user = (f"DANCE: {d.get('name') or d.get('slug')}\nSLUG: {d.get('slug')}\nEXISTING CATALOGUE ENTRY (may be thin or partly wrong; prefer the sources): {json.dumps(existing, ensure_ascii=False)[:1500]}\n\n"
            + "\n\n".join(src_blocks))
    system = EDITORIAL.format(regions=", ".join(REGIONS), families=", ".join(FAMILIES.keys()))
    return normalize(llm.json(system, user, strong=True, temperature=0.3, max_tokens=6000))

def research_one(d, llm, sb=None):
    slug = d.get("slug") or slugify(d.get("name"))
    out_path = os.path.join(RESULTS_DIR, slug + ".json")
    ev = gather_evidence(d)
    rec = {"slug": slug, "name": d.get("name"), "researched_at": now_iso(), "evidence": {k: v for k, v in ev.items() if k not in ("images",)},
           "images": ev.get("images", []), "status": "no_sources"}
    # keep the evidence texts out of the committed result (they are in the cache) but keep hashes + urls
    for k in ("wikipedia", "wikipedia_other"):
        if k in rec["evidence"]:
            if k == "wikipedia":
                rec["evidence"][k] = {kk: vv for kk, vv in rec["evidence"][k].items() if kk != "text"}
            else:
                rec["evidence"][k] = [{kk: vv for kk, vv in x.items() if kk != "text"} for x in rec["evidence"][k]]
    if not ev.get("wikipedia") and not ev.get("wikidata"):
        jsave(out_path, rec)
        return rec
    comp = compose(d, ev, llm)
    if not comp:
        rec["status"] = "llm_failed" if llm.enabled else "dry_run"
        jsave(out_path, rec)
        return rec
    claims, cstats = verify_claims(comp.get("claims"), ev)
    verified_albums, unverified_albums = verify_albums(comp.get("albums"))
    iso, region_guess = country_lookup(comp.get("country") or d.get("country") or "")
    region = comp.get("region") if comp.get("region") in REGIONS else (region_guess or d.get("region"))
    fam = comp.get("family") if comp.get("family") in FAMILIES else None
    sacred_cue, cues = sacred_hint((comp.get("profile_long") or "") + " " + json.dumps(comp.get("sections") or {}))
    rec.update({
        "status": "researched",
        "profile": {k: comp.get(k) for k in ("name", "tagline", "insight", "profile", "profile_long", "sections", "era", "country", "aliases", "related", "is_sacred", "sacred_note", "unesco", "teaching", "confidence", "gaps")},
        "country_code": iso or d.get("country_code"), "region": region, "family": fam,
        "claims": claims, "citation": cstats,
        "albums": verified_albums, "album_candidates": unverified_albums,
        "sources": list(dict.fromkeys(ev.get("sources", []))),
        "sacred_cues": cues, "sacred_cue_flag": sacred_cue,
        "wikipedia_url": (ev.get("wikipedia") or {}).get("url") or d.get("wikipedia_url"),
        "wikidata_qid": (ev.get("wikidata") or {}).get("qid") or d.get("wikidata_qid"),
        "unesco_ref": (ev.get("unesco") or {}).get("ref"),
        "coords": next(iter((ev.get("wikidata") or {}).get("facts", {}).get("coordinates", [])), None),
        "llm_calls": llm.calls,
    })
    jsave(out_path, rec)
    return rec

def pick_enrichment_targets(catalog, n):
    """Lowest completeness first, skipping ones researched in the last 60 days."""
    done = load_state("research_index.json", {})
    gone = {k for k, v in load_state("audit.json", {}).items() if v.get("decision") in ("retire", "merge")}
    scored = []
    for d in catalog:
        if d["slug"] in gone:
            continue
        last = (done.get(d["slug"]) or {}).get("researched_at", "")
        if last and last[:10] >= _days_ago(60):
            continue
        scored.append((completeness(d), d))
    scored.sort(key=lambda x: x[0])
    return [d for _, d in scored[:n]]

def _days_ago(n):
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) - timedelta(days=n)).strftime("%Y-%m-%d")

def run(budget_new=20, budget_enrich=20, only=None):
    rep = Report("research")
    llm = LLM()
    sb = Supabase()
    catalog = load_catalog(sb)
    index = load_state("research_index.json", {})
    cands = load_state("candidates.json", {})
    targets = []
    if only:
        by = {d["slug"]: d for d in catalog}
        for s in only:
            targets.append(("enrich", by.get(s) or cands.get(s) or {"slug": s, "name": s.replace("-", " ")}))
    else:
        queued = [c for c in cands.values() if c.get("status") == "queued"]
        queued.sort(key=lambda c: (0 if c.get("wikidata_qid") else 1, c.get("found_at", "")))
        targets += [("new", c) for c in queued[:budget_new]]
        targets += [("enrich", d) for d in pick_enrichment_targets(catalog, budget_enrich)]
    rep.note(f"targets: {len(targets)} (llm enabled={llm.enabled})")
    for kind, d in targets:
        slug = d.get("slug")
        try:
            rec = research_one(d, llm, sb)
            index[slug] = {"researched_at": rec["researched_at"], "status": rec["status"], "kind": kind,
                           "citation_rate": (rec.get("citation") or {}).get("rate"), "albums": len(rec.get("albums") or []), "images": len(rec.get("images") or [])}
            rep.inc("researched_" + rec["status"])
            if kind == "new" and slug in cands:
                cands[slug]["status"] = "researched" if rec["status"] == "researched" else ("no_sources" if rec["status"] == "no_sources" else "queued")
                cands[slug]["researched_at"] = rec["researched_at"]
            log(f"RESEARCH {kind} {slug}: {rec['status']} claims={(rec.get('citation') or {}).get('claims')} rate={(rec.get('citation') or {}).get('rate')} albums={len(rec.get('albums') or [])} images={len(rec.get('images') or [])}")
        except Exception as e:
            rep.error(f"{slug}: {e}")
            index[slug] = {"researched_at": now_iso(), "status": "error", "error": str(e)[:200]}
        save_state("research_index.json", index)
        save_state("candidates.json", cands)
    rep.inc("llm_calls", llm.calls); rep.inc("llm_failures", llm.failures)
    return rep.finish()

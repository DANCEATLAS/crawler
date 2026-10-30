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
RESEARCH_SCHEMA = 4   # 4 = movie-ready fields (music_profile, movement_profile, episode_brief, connections); bump to re-deepen every record
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
9. MOVIE-READY DEPTH. The profile will later drive a studio-quality film episode and a dance lesson, so capture the DNA of the music and of the movement as precisely as the sources allow:
   music_profile = what a composer needs to recreate the sound without copying any recording (tempo, meter, rhythm pattern, instruments, vocal style, form, mood, a 2-4 sentence sound description of what makes it recognisable);
   movement_profile = what a choreographer or instructor needs (posture, footwork with counts, arms and hands, hips and torso, formation and spatial path, partnering, tempo feel, named signature moves with one-line descriptions, levels and jumps, difficulty, what to avoid for cultural or safety reasons);
   episode_brief = how a 5-minute introduction episode would run (a title hook, a one-sentence logline, 5-8 ordered story beats that are concrete scenes, a 3-level lesson ladder with 3-5 drills each, visual motifs to show, a credible instructor persona, the music cue the soundtrack must follow);
   connections = named links to other dances with a relation (parent, child, sibling, variant, influence, shares_music, same_region) and a short note.
   Where the sources do not describe a detail, write "not described in sources" for that field rather than inventing it. Numbers (tempo, counts) only when a source gives them or the meter makes them unambiguous.
Output JSON with keys: name, tagline (<=90 chars), insight (<=220 chars), profile (3-5 sentences), profile_long (600-1200 words of continuous prose using the sections), sections{{origins_and_history, how_it_is_danced, music_and_instruments, costume_and_setting, occasions_and_meaning, notable_figures, regional_variants, lineage}}, era (short, e.g. "19th century"), country, region, family, aliases[], related[] (names of other dances), is_sacred (bool), sacred_note, unesco (bool), teaching{{basic_steps[] (ordered, each one movement), rhythm, formation, level_notes}}, music_profile{{tempo_bpm, meter, rhythm_pattern, instruments[], vocal_style, musical_form, mood_keywords[], reference_recordings[] ({{title, artist}}), sound_description}}, movement_profile{{posture, footwork, arms_and_hands, hips_and_torso, formation_and_space, partnering, tempo_feel, signature_moves[] ({{name, description}}), levels_and_jumps, difficulty (beginner|intermediate|advanced), what_to_avoid}}, episode_brief{{title_hook, logline, beats[], lesson_ladder[] ({{level, goal, drills[]}}), visual_motifs[], instructor_persona, music_cue}}, connections[] ({{name, relation, note}}), albums[] ({{title, artist, source}}), claims[] ({{text, source, quote}}), confidence (0-1), gaps[]."""

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
        for lang in ("es", "fr", "pt", "de", "it", "ru", "ja", "id", "tr", "ar", "hi", "pl", "nl", "fa", "zh", "ko", "vi", "th", "el", "he", "uk", "sv", "cs", "ro", "hu", "sw", "ta", "bn"):
            t = (wd.get("sitelinks") or {}).get(lang + "wiki")
            if t and len(extra) < 3:
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
    # UNESCO: exact (or near-exact) title match = the inscription itself; a whole-word hit = related inscription (evidence only)
    try:
        from .common import similarity
        idx = S.unesco_ich_index()
        nn = norm(name)
        best = None
        for e in idx:
            tt = norm(e.get("title"))
            if not tt or not nn:
                continue
            if tt == nn or similarity(tt, nn) >= 0.85:
                best = (e, True); break
            if len(nn) >= 5 and re.search(r"\b" + re.escape(nn) + r"\b", tt) and best is None:
                best = (e, False)
        if best:
            h, exact = best
            ev["unesco"] = {"ref": h.get("ref"), "title": h.get("title"), "countries": h.get("countries"), "year": h.get("year"),
                            "url": h.get("url") or f"https://ich.unesco.org/en/RL/{h.get('ref')}", "description": h.get("description") or "",
                            "type": h.get("type"), "exact": exact}
            ev["sources"].append(ev["unesco"]["url"])
    except Exception as e:
        warn("unesco match", e)
    # digitised books (Internet Archive): passages around the dance's name, for depth beyond the encyclopedias
    try:
        aliases = list(d.get("aliases") or []) + list(((ev.get("wikidata") or {}).get("aliases") or [])[:3])
        books = S.archive_passages(name, aliases=aliases) if len(norm(name)) >= 4 else []
        if books:
            ev["books"] = books
            ev["sources"] += [b["url"] for b in books]
    except Exception as e:
        warn("archive passages", name, e)
    # Commons images (licensed)
    if ev.get("wikipedia"):
        ev["images"] = S.commons_images_for_page(ev["wikipedia"]["title"], limit=12)[:8]
    ev["text_hash"] = sha1(json.dumps([ev.get("wikipedia", {}).get("text", ""), [x["text"] for x in ev.get("wikipedia_other", [])], [b.get("passages") for b in ev.get("books", [])]]))
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
        u = ev["unesco"]
        texts[u["url"]] = " ".join(str(x) for x in (u.get("title"), u.get("countries"), u.get("year"), u.get("type"), u.get("description")) if x)
    for b in ev.get("books", []):
        texts[b["url"]] = "\n".join(b.get("passages") or [])
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
    # movie-ready structures: keep dicts/lists in a predictable shape, strings trimmed, nothing invented
    mp = c.get("music_profile") if isinstance(c.get("music_profile"), dict) else {}
    for k in ("tempo_bpm", "meter", "rhythm_pattern", "vocal_style", "musical_form", "sound_description"):
        mp[k] = _s(mp.get(k), " ").strip()
    for k in ("instruments", "mood_keywords"):
        v = mp.get(k); mp[k] = [str(x).strip() for x in v if str(x).strip()] if isinstance(v, list) else ([str(v).strip()] if v else [])
    mp["reference_recordings"] = [x for x in (mp.get("reference_recordings") or []) if isinstance(x, dict)]
    c["music_profile"] = mp
    mv = c.get("movement_profile") if isinstance(c.get("movement_profile"), dict) else {}
    for k in ("posture", "footwork", "arms_and_hands", "hips_and_torso", "formation_and_space", "partnering", "tempo_feel", "levels_and_jumps", "difficulty", "what_to_avoid"):
        mv[k] = _s(mv.get(k), " ").strip()
    mv["signature_moves"] = [x for x in (mv.get("signature_moves") or []) if isinstance(x, dict)]
    c["movement_profile"] = mv
    eb = c.get("episode_brief") if isinstance(c.get("episode_brief"), dict) else {}
    for k in ("title_hook", "logline", "instructor_persona", "music_cue"):
        eb[k] = _s(eb.get(k), " ").strip()
    for k in ("beats", "visual_motifs"):
        v = eb.get(k); eb[k] = [str(x).strip() for x in v if str(x).strip()] if isinstance(v, list) else ([str(v).strip()] if v else [])
    eb["lesson_ladder"] = [x for x in (eb.get("lesson_ladder") or []) if isinstance(x, dict)]
    c["episode_brief"] = eb
    c["connections"] = [x for x in (c.get("connections") or []) if isinstance(x, dict) and x.get("name")]
    c["is_sacred"] = bool(c.get("is_sacred"))
    c["unesco"] = bool(c.get("unesco"))
    try:
        c["confidence"] = float(c.get("confidence") or 0)
    except Exception:
        c["confidence"] = 0.0
    return c

def compose(d, ev, llm, prev_gaps=None):
    """Ask the model for the structured profile. Returns dict or None."""
    src_blocks = []
    if ev.get("wikipedia"):
        src_blocks.append(f"SOURCE: {ev['wikipedia']['url']}\n{ev['wikipedia']['text']}")
    for x in ev.get("wikipedia_other", []):
        src_blocks.append(f"SOURCE: {x['url']} (language: {x['lang']})\n{x['text']}")
    if ev.get("wikidata"):
        src_blocks.append(f"SOURCE: {ev['wikidata']['url']}\nWikidata facts: {json.dumps(ev['wikidata']['facts'], ensure_ascii=False)}\nDescription: {ev['wikidata'].get('description')}\nAliases: {ev['wikidata'].get('aliases')}")
    if ev.get("unesco"):
        u = ev["unesco"]
        kind = "this dance's own inscription" if u.get("exact") else "a RELATED inscription (not this dance itself; do not claim this dance is inscribed)"
        src_blocks.append(f"SOURCE: {u['url']}\nUNESCO Intangible Cultural Heritage, {kind}: {u.get('title')} ({u.get('countries')}, {u.get('year')}, {u.get('type')})\n{u.get('description')}")
    for b in ev.get("books", []):
        head = f"SOURCE: {b['url']}\nDigitised book: {b.get('title')} ({b.get('year') or 'year unknown'}); passages that mention the dance (quote only from these passages):"
        src_blocks.append(head + "\n" + "\n[...]\n".join(b.get("passages") or []))
    if not src_blocks:
        return None
    existing = {k: d.get(k) for k in ("name", "country", "region", "era", "tagline", "insight", "profile", "aliases", "related") if d.get(k)}
    gaps_note = ""
    if prev_gaps:
        gaps_note = "\nGAPS LEFT BY THE PREVIOUS PASS (fill them if, and only if, the sources now allow it): " + "; ".join(str(g) for g in prev_gaps[:12])
    user = (f"DANCE: {d.get('name') or d.get('slug')}\nSLUG: {d.get('slug')}\nEXISTING CATALOGUE ENTRY (may be thin or partly wrong; prefer the sources): {json.dumps(existing, ensure_ascii=False)[:1500]}{gaps_note}\n\n"
            + "\n\n".join(src_blocks))
    system = EDITORIAL.format(regions=", ".join(REGIONS), families=", ".join(FAMILIES.keys()))
    return normalize(llm.json(system, user, strong=True, temperature=0.3, max_tokens=9000))

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
    if "books" in rec["evidence"]:
        rec["evidence"]["books"] = [{kk: vv for kk, vv in b.items() if kk != "passages"} for b in rec["evidence"]["books"]]
    if not ev.get("wikipedia") and not ev.get("wikidata"):
        jsave(out_path, rec)
        return rec
    prev = jload(out_path) or {}
    prev_gaps = list(((prev.get("profile") or {}).get("gaps") or [])[:8]) + [("class is missing: " + m) for m in ((prev.get("class_checklist") or {}).get("missing") or [])[:8]]
    comp = compose(d, ev, llm, prev_gaps=prev_gaps)
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
    # the UNESCO flag needs the inscription itself or a verified claim that says so
    unesco_exact = bool((ev.get("unesco") or {}).get("exact"))
    comp["unesco"] = unesco_exact or (bool(comp.get("unesco")) and any(c.get("supported") and "unesco" in norm(c.get("text") or "") for c in claims))
    rec.update({
        "status": "researched",
        "profile": {k: comp.get(k) for k in ("name", "tagline", "insight", "profile", "profile_long", "sections", "era", "country", "aliases", "related", "is_sacred", "sacred_note", "unesco", "teaching",
                                             "music_profile", "movement_profile", "episode_brief", "connections", "confidence", "gaps")},
        "schema": RESEARCH_SCHEMA, "movie_ready": movie_ready(comp), "class_checklist": class_checklist(comp, ev.get("images", []), verified_albums),
        "books": [{k: b.get(k) for k in ("identifier", "title", "year", "url")} for b in ev.get("books", [])],
        "country_code": iso or d.get("country_code"), "region": region, "family": fam,
        "claims": claims, "citation": cstats,
        "albums": verified_albums, "album_candidates": unverified_albums,
        "sources": list(dict.fromkeys(ev.get("sources", []))),
        "sacred_cues": cues, "sacred_cue_flag": sacred_cue,
        "wikipedia_url": (ev.get("wikipedia") or {}).get("url") or d.get("wikipedia_url"),
        "wikidata_qid": (ev.get("wikidata") or {}).get("qid") or d.get("wikidata_qid"),
        "unesco_ref": (ev.get("unesco") or {}).get("ref") if (ev.get("unesco") or {}).get("exact") else None,
        "unesco_related": None if (ev.get("unesco") or {}).get("exact", True) else {k: (ev.get("unesco") or {}).get(k) for k in ("ref", "title", "url")},
        "coords": next(iter((ev.get("wikidata") or {}).get("facts", {}).get("coordinates", [])), None),
        "llm_calls": llm.calls,
    })
    jsave(out_path, rec)
    return rec

CHECKLIST = ("footwork_with_counts", "posture", "arms_and_hands", "formation", "tempo_or_meter", "instruments", "sound_description",
             "signature_moves", "lesson_ladder", "story_beats", "hooks", "costume", "occasions", "notable_figures", "recordings", "images", "connections")

def class_checklist(comp, rec_images=(), albums=()):
    """What a fun, teachable class still lacks for this dance. Missing items steer the next deepening pass."""
    mp, mv, eb = comp.get("music_profile") or {}, comp.get("movement_profile") or {}, comp.get("episode_brief") or {}
    secs = comp.get("sections") or {}
    have = {
        "footwork_with_counts": _said(mv.get("footwork")) and bool(re.search(r"\b(count|beat|1-2|one-two|step[s]?)\b", mv.get("footwork") or "", re.I)),
        "posture": _said(mv.get("posture")), "arms_and_hands": _said(mv.get("arms_and_hands")), "formation": _said(mv.get("formation_and_space")),
        "tempo_or_meter": bool((mp.get("tempo_bpm") or "").strip() or (mp.get("meter") or "").strip()) and not _said_not(mp.get("tempo_bpm")) ,
        "instruments": bool(mp.get("instruments")), "sound_description": _said(mp.get("sound_description")),
        "signature_moves": bool(mv.get("signature_moves")), "lesson_ladder": len(eb.get("lesson_ladder") or []) >= 3,
        "story_beats": len(eb.get("beats") or []) >= 5, "hooks": _said(comp.get("insight")) and _said(eb.get("title_hook")),
        "costume": _said(secs.get("costume_and_setting")), "occasions": _said(secs.get("occasions_and_meaning")),
        "notable_figures": _said(secs.get("notable_figures")), "recordings": bool(albums) or bool(mp.get("reference_recordings")),
        "images": len(rec_images or []) >= 3, "connections": bool(comp.get("connections")),
    }
    missing = [k for k in CHECKLIST if not have.get(k)]
    return {"have": sum(1 for k in CHECKLIST if have.get(k)), "of": len(CHECKLIST), "missing": missing}

def _said_not(v):
    s = (v or "").strip().lower()
    return "not described" in s or "not in sources" in s or s in ("", "null", "none", "unknown")

def _said(v):
    """True when a movie-ready field carries real content rather than a 'not described' placeholder."""
    s = (v or "").strip().lower()
    return len(s) >= 25 and "not described" not in s and "not in sources" not in s

def movie_ready(comp):
    """A profile can drive an episode and a lesson when the music and movement DNA are both described from sources."""
    mp, mv, eb = comp.get("music_profile") or {}, comp.get("movement_profile") or {}, comp.get("episode_brief") or {}
    music = _said(mp.get("sound_description")) and (bool(mp.get("instruments")) or _said(mp.get("rhythm_pattern")))
    move = _said(mv.get("footwork")) and (_said(mv.get("posture")) or _said(mv.get("arms_and_hands")) or bool(mv.get("signature_moves")))
    story = len(eb.get("beats") or []) >= 5 and len(eb.get("lesson_ladder") or []) >= 2
    return bool(music and move and story)

def pick_enrichment_targets(catalog, n):
    """Lowest completeness first. A record researched in the last 60 days is skipped unless it predates the current
    research schema (then it is re-deepened so every page reaches movie-ready depth once)."""
    done = load_state("research_index.json", {})
    gone = {k for k, v in load_state("audit.json", {}).items() if v.get("decision") in ("retire", "merge")}
    scored = []
    for d in catalog:
        if d["slug"] in gone:
            continue
        prev = done.get(d["slug"]) or {}
        last = prev.get("researched_at", "")
        if last and last[:10] >= _days_ago(60) and int(prev.get("schema") or 0) >= RESEARCH_SCHEMA:
            continue
        if prev.get("status") == "no_sources" and last and last[:10] >= _days_ago(60):
            continue   # nothing to read yet; try again in two months
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
            index[slug] = {"researched_at": rec["researched_at"], "status": rec["status"], "kind": kind, "schema": rec.get("schema"), "movie_ready": rec.get("movie_ready"),
                           "class_have": (rec.get("class_checklist") or {}).get("have"), "class_missing": (rec.get("class_checklist") or {}).get("missing"),
                           "citation_rate": (rec.get("citation") or {}).get("rate"), "albums": len(rec.get("albums") or []), "images": len(rec.get("images") or [])}
            rep.inc("researched_" + rec["status"])
            if kind == "new" and slug in cands:
                cands[slug]["status"] = "researched" if rec["status"] == "researched" else ("no_sources" if rec["status"] == "no_sources" else "queued")
                cands[slug]["researched_at"] = rec["researched_at"]
            log(f"RESEARCH {kind} {slug}: {rec['status']} claims={(rec.get('citation') or {}).get('claims')} rate={(rec.get('citation') or {}).get('rate')} albums={len(rec.get('albums') or [])} images={len(rec.get('images') or [])} movie_ready={rec.get('movie_ready')}")
        except Exception as e:
            rep.error(f"{slug}: {e}")
            index[slug] = {"researched_at": now_iso(), "status": "error", "error": str(e)[:200]}
        save_state("research_index.json", index)
        save_state("candidates.json", cands)
    rep.inc("llm_calls", llm.calls); rep.inc("llm_failures", llm.failures)
    return rep.finish()

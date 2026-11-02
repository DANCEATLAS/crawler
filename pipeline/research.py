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
from .discover import move_like
from . import sources as S

RESULTS_DIR = os.environ.get("RESEARCH_DIR", "research_results")
RESEARCH_SCHEMA = 5   # 4 = movie-ready fields (music_profile, movement_profile, episode_brief, connections); 5 = tradition_status, adaptations for seniors and children, reference footage; bump to re-deepen every record
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
   Where the sources do not describe a detail, write exactly "not described in sources" for that field rather than inventing it (that exact phrase; never "the provided sources", never a sentence about the sources inside prose). Numbers (tempo, counts) only when a source gives them or the meter makes them unambiguous.
10. LIVING OR HISTORICAL. tradition_status = "living" (practised today by a community), "revived" (reconstructed or kept alive by folklore groups after a break), "historical" (documented but no longer practised) or "unknown" — from the sources, with the deciding sentence quoted in claims.
11. ADAPTATIONS FOR SENIORS AND CHILDREN (the owner's long-term audiences). These are teaching material you DERIVE from the movement_profile and teaching fields, not facts about the dance, so they are allowed to go beyond the sources — but only as cautious, generic, physically safe adjustments of what the sources describe: for seniors a seated or supported version, reduced tempo and range, what to avoid (balance, knees, spine, jumps); for children a game version, a shorter duration, simplified counts, what to avoid. Be concrete (counts, body parts), never medical. If movement_profile.footwork is "not described in sources", write "not derivable yet" for every adaptation field. Never adapt a sacred or restricted dance: write "withheld (sacred or restricted dance)".
Output JSON with keys: name, tagline (<=90 chars), insight (<=220 chars), profile (3-5 sentences), profile_long (600-1200 words of continuous prose using the sections), sections{{origins_and_history, how_it_is_danced, music_and_instruments, costume_and_setting, occasions_and_meaning, notable_figures, regional_variants, lineage}}, era (short, e.g. "19th century"), country, region, family, aliases[], related[] (names of other dances), is_sacred (bool), sacred_note, unesco (bool), teaching{{basic_steps[] (ordered, each one movement), rhythm, formation, level_notes}}, music_profile{{tempo_bpm, meter, rhythm_pattern, instruments[], vocal_style, musical_form, mood_keywords[], reference_recordings[] ({{title, artist}}), sound_description}}, movement_profile{{posture, footwork, arms_and_hands, hips_and_torso, formation_and_space, partnering, tempo_feel, signature_moves[] ({{name, description}}), levels_and_jumps, difficulty (beginner|intermediate|advanced), what_to_avoid}}, episode_brief{{title_hook, logline, beats[], lesson_ladder[] ({{level, goal, drills[]}}), visual_motifs[], instructor_persona, music_cue}}, connections[] ({{name, relation, note}}), tradition_status (living|revived|historical|unknown), adaptations{{seniors{{seated_version, standing_version, tempo_and_range, counts, avoid[]}}, children{{game_version, duration_minutes, counts, avoid[]}}}}, albums[] ({{title, artist, source}}), claims[] ({{text, source, quote}}), confidence (0-1), gaps[]."""

def _trim(txt, n):
    txt = re.sub(r"\n{3,}", "\n\n", txt or "")
    return txt[:n]

LIST_TITLE = re.compile(r"^(lists? of|category:|index of|outline of|glossary of|timeline of)\b", re.I)

def page_fits(wp, name):
    """A fetched article is evidence for this dance only when it is an article about it: not a disambiguation page,
    not a list/overview page, and the dance's name is in the title or in the opening of the text. (A catalogue entry whose
    wikipedia_url points at 'List of European folk music traditions' used to be 'researched' from that list page.)"""
    if not wp or wp.get("disambiguation") or (wp.get("length") or 0) < 400:
        return False
    title = wp.get("title") or ""
    if LIST_TITLE.search(title.strip()):
        return False
    nn = norm(name)
    if not nn:
        return True
    from .common import similarity
    nt = norm(title)
    if nn in nt or nt in nn or similarity(nt, nn) >= 0.6:
        return True
    head = norm((wp.get("text") or "")[:8000])
    return nn in head or (len(nn.split()) > 1 and nn.split()[0] in head.split() and len(nn.split()[0]) >= 5)

PLACEHOLDER = "not described in sources"
_PH_WHOLE = re.compile(r"^\s*(?:not|no|none|nothing|unknown|n/?a)\b[^.;]{0,90}\b(?:sources?|evidence|texts?|material|documentation|passages?)\b[^.;]{0,40}[.;]?\s*$", re.I)
_PH_PHRASE = re.compile(r"\b(?:based on |in |from |within |according to |per )?the (?:(?:provided|given|available|supplied|cited|above|present) (?:sources?|evidence|texts?|material)|(?:sources?|evidence|texts?|material) (?:provided|given|available|supplied|cited|above))\b", re.I)

def _reduce_source_talk(s):
    """'based on the sources provided' -> 'based on the sources'; 'in the provided evidence' -> 'in the sources'."""
    if not isinstance(s, str) or not s or not re.search(r"source|evidence|text|material", s, re.I):
        return s
    return _PH_PHRASE.sub(lambda m: m.group(0)[:m.group(0).lower().find("the ")] + "the sources", s)

def canon_placeholder(s):
    """The composer is told to write exactly "not described in sources" where the sources are silent; models still write
    "Not detailed in the provided sources." and similar. Whole-field placeholders become the canonical phrase and
    source-talk inside prose ("the provided sources") is reduced to "the sources", so QC's AI-tell gate (which rejects a
    profile that talks about its prompt) is not tripped by an honest gap."""
    if not isinstance(s, str) or not s:
        return s
    if _PH_WHOLE.match(s):
        return PLACEHOLDER
    return _reduce_source_talk(s)

def gather_evidence(d):
    """d: catalogue entry or candidate. Returns evidence dict with fetched texts."""
    ev = {"fetched_at": now_iso(), "sources": []}
    name = d.get("name") or d.get("slug")
    wp = None
    own_page_rejected = False
    if d.get("wikipedia_url"):
        wp = S.wiki_page(d["wikipedia_url"])
        if wp and not page_fits(wp, name):
            log(f"evidence {d.get('slug')}: own page '{wp.get('title')}' is not an article about the dance; searching instead")
            own_page_rejected, wp = True, None
    if not page_fits(wp, name):
        wp = None
        queries = [name + " dance", name] + [a for a in (d.get("aliases") or [])[:3] if isinstance(a, str) and norm(a) != norm(name)]
        for q in queries:
            for r in S.wiki_search(q, limit=4):
                cand = S.wiki_page(r["title"])
                if page_fits(cand, name) and re.search(r"danc", (cand.get("text") or "")[:3000], re.I):
                    wp = cand; break
            if wp:
                break
    if wp:
        ev["wikipedia"] = {"title": wp["title"], "url": wp["url"], "qid": wp.get("qid"), "categories": wp.get("categories", [])[:30],
                           "text": _trim(wp["text"], 16000), "image": wp.get("image")}
        ev["sources"].append(wp["url"])
    # the entry's own QID is trusted unless its own page was rejected (then it probably points at the same wrong subject)
    qid = ((wp or {}).get("qid") or d.get("wikidata_qid")) if own_page_rejected else (d.get("wikidata_qid") or (wp or {}).get("qid"))
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
    # sources an editor added by hand (pipeline_state/sources_extra.json): {slug: [{url, tier, note}]} — fetched as plain text
    try:
        extra = (load_state("sources_extra.json", {}) or {}).get(d.get("slug") or "", []) or []
        got = []
        for x in extra[:6]:
            u = (x.get("url") or "").strip()
            if not u or not u.startswith("http"):
                continue
            txt = S.page_text(u)
            if txt and len(txt) > 300:
                got.append({"url": u, "tier": (x.get("tier") or "other"), "note": (x.get("note") or "")[:200], "text": txt})
                ev["sources"].append(u)
        if got:
            ev["extra"] = got
    except Exception as e:
        warn("sources_extra", d.get("slug"), e)
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
    for x in ev.get("extra", []):
        texts[x["url"]] = x["text"]
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
    # honest gaps in one canonical wording, everywhere a string can carry prose
    for k in ("tagline", "insight", "profile", "profile_long", "sacred_note"):
        c[k] = canon_placeholder(c[k])
    c["sections"] = {k: canon_placeholder(v) for k, v in c["sections"].items()}
    for k in ("rhythm", "formation", "level_notes"):
        t[k] = canon_placeholder(t[k])
    t["basic_steps"] = [canon_placeholder(x) for x in t["basic_steps"]]
    def _clean_list(v):
        out = []
        for x in v:
            if isinstance(x, str):
                x = canon_placeholder(x)
                if x and x != PLACEHOLDER:
                    out.append(x)
            elif isinstance(x, dict):
                x = {kk: canon_placeholder(vv) if isinstance(vv, str) else vv for kk, vv in x.items()}
                if (x.get("name") or x.get("title") or x.get("level") or "x") != PLACEHOLDER:
                    out.append(x)
            else:
                out.append(x)
        return out
    for dct in (mp, mv, eb):
        for k, v in list(dct.items()):
            if isinstance(v, str):
                dct[k] = canon_placeholder(v)
            elif isinstance(v, list):
                dct[k] = _clean_list(v)
    c["connections"] = _clean_list(c["connections"])
    c["gaps"] = [_reduce_source_talk(x) for x in c["gaps"]]   # gaps keep their wording (they steer the next pass)
    ts = str(c.get("tradition_status") or "").strip().lower()
    c["tradition_status"] = ts if ts in ("living", "revived", "historical", "unknown") else "unknown"
    ad = c.get("adaptations") if isinstance(c.get("adaptations"), dict) else {}
    out_ad = {}
    for who, keys in (("seniors", ("seated_version", "standing_version", "tempo_and_range", "counts")), ("children", ("game_version", "duration_minutes", "counts"))):
        sub = ad.get(who) if isinstance(ad.get(who), dict) else {}
        o = {k: canon_placeholder(_s(sub.get(k), " ").strip()) for k in keys}
        o["avoid"] = _clean_list(sub.get("avoid") or []) if isinstance(sub.get("avoid"), list) else ([str(sub.get("avoid")).strip()] if sub.get("avoid") else [])
        out_ad[who] = o
    out_ad["derived"] = True   # teaching material derived from the movement profile, not a fact about the dance
    if c["is_sacred"]:
        out_ad = {"withheld": "sacred or restricted dance: no teaching adaptations", "derived": True}
    c["adaptations"] = out_ad
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
    for x in ev.get("extra", []):
        tier = x.get("tier") or "other"
        trust = {"scholarly": "peer-reviewed or academic: trust for facts and history", "archive": "museum, library or archive: trust for facts and history",
                 "practitioner": "a teacher's or dance school's page: best for technique, counts, music and feel; weigh its history claims against the encyclopedias",
                 "press": "journalism: good for people, dates and events; weigh its technique claims"}.get(tier, "unverified web page: use with care")
        src_blocks.append(f"SOURCE: {x['url']}\nAdded by the editor ({tier} — {trust}). {x.get('note') or ''}\n{x['text']}")
    if not src_blocks:
        return None
    existing = {k: d.get(k) for k in ("name", "country", "region", "era", "tagline", "insight", "profile", "aliases", "related") if d.get(k)}
    gaps_note = ""
    if prev_gaps:
        gaps_note = "\nGAPS LEFT BY THE PREVIOUS PASS (fill them if, and only if, the sources now allow it): " + "; ".join(str(g) for g in prev_gaps[:12])
    note = ((load_state("editor_notes.json", {}) or {}).get(d.get("slug") or "") or {}).get("note")
    if note:
        gaps_note += "\nEDITOR'S NOTE ON THE PREVIOUS VERSION (correct this; it overrides the existing entry): " + str(note)[:800]
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
    if "extra" in rec["evidence"]:
        rec["evidence"]["extra"] = [{kk: vv for kk, vv in x.items() if kk != "text"} for x in rec["evidence"]["extra"]]
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
    try:   # licensed reference footage for the future generator (links only; nothing is downloaded)
        footage = S.footage_for(comp.get("name") or d.get("name") or slug, aliases=(comp.get("aliases") or [])[:3])
    except Exception as e:
        warn("footage", slug, e); footage = []
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
                                             "music_profile", "movement_profile", "episode_brief", "connections", "tradition_status", "adaptations", "confidence", "gaps")},
        "footage": footage,
        "schema": RESEARCH_SCHEMA, "movie_ready": movie_ready(comp), "class_checklist": class_checklist(comp, ev.get("images", []), verified_albums, footage),
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
             "signature_moves", "lesson_ladder", "story_beats", "hooks", "costume", "occasions", "notable_figures", "recordings", "images", "connections", "footage")

def class_checklist(comp, rec_images=(), albums=(), footage=()):
    """What a fun, teachable class still lacks for this dance. Missing items steer the next deepening pass."""
    mp, mv, eb = comp.get("music_profile") or {}, comp.get("movement_profile") or {}, comp.get("episode_brief") or {}
    secs = comp.get("sections") or {}
    have = {
        "footwork_with_counts": _said(mv.get("footwork")) and bool(re.search(r"\b(count|beat|1-2|one-two|step[s]?)\b", mv.get("footwork") or "", re.I)),
        "posture": _said(mv.get("posture")), "arms_and_hands": _said(mv.get("arms_and_hands")), "formation": _said(mv.get("formation_and_space")),
        "tempo_or_meter": (not _said_not(mp.get("tempo_bpm"))) or (not _said_not(mp.get("meter"))),
        "instruments": bool(mp.get("instruments")), "sound_description": _said(mp.get("sound_description")),
        "signature_moves": bool(mv.get("signature_moves")), "lesson_ladder": len(eb.get("lesson_ladder") or []) >= 3,
        "story_beats": len(eb.get("beats") or []) >= 5, "hooks": _said(comp.get("insight")) and _said(eb.get("title_hook")),
        "costume": _said(secs.get("costume_and_setting")), "occasions": _said(secs.get("occasions_and_meaning")),
        "notable_figures": _said(secs.get("notable_figures")), "recordings": bool(albums) or bool(mp.get("reference_recordings")),
        "images": len(rec_images or []) >= 3, "connections": bool(comp.get("connections")), "footage": bool(footage),
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
    notes = load_state("editor_notes.json", {}) or {}
    extra = load_state("sources_extra.json", {}) or {}
    def flagged(slug):
        """An open editor note, or an extra source added after the last research pass, puts a page first in the queue."""
        prev = done.get(slug) or {}
        last = prev.get("researched_at", "")
        n = notes.get(slug) or {}
        if n.get("note") and not n.get("done_at"):
            return True
        return any((x.get("added") or "") > last[:10] for x in (extra.get(slug) or []) if isinstance(x, dict))
    scored = []
    for d in catalog:
        if d["slug"] in gone:
            continue
        prev = done.get(d["slug"]) or {}
        last = prev.get("researched_at", "")
        if flagged(d["slug"]):
            scored.append((-1, d)); continue
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
        picked = []
        for c in queued:
            if len(picked) >= budget_new:
                break
            # screen: a dance move/step/figure (by article disambiguator or Wikidata description) is not researched
            desc = c.get("description")
            if not desc and c.get("wikidata_qid"):
                try:
                    desc = (S.wikidata_entity(c["wikidata_qid"]) or {}).get("description")
                except Exception as e:
                    warn("screen wikidata", c.get("slug"), e)
            lead = None
            if not move_like(c.get("name") or "", c.get("wikipedia_url"), desc) and c.get("wikipedia_url"):
                try:   # the article is fetched anyway for research (cached); its first sentence settles most of the rest
                    lead = ((S.wiki_page(c["wikipedia_url"]) or {}).get("text") or "")[:600]
                except Exception as e:
                    warn("screen wiki lead", c.get("slug"), e)
            if move_like(c.get("name") or "", c.get("wikipedia_url"), desc, lead):
                c["status"], c["screened_out"], c["screened_at"] = "screened_out", "dance move/step/figure: " + str(desc or (lead or "")[:100] or c.get("wikipedia_url"))[:120], now_iso()
                rep.inc("screened_out_move")
                log(f"RESEARCH screen {c.get('slug')}: not researched ({c['screened_out']})")
                continue
            picked.append(c)
        save_state("candidates.json", cands)
        targets += [("new", c) for c in picked]
        targets += [("enrich", d) for d in pick_enrichment_targets(catalog, budget_enrich)]
    rep.note(f"targets: {len(targets)} (llm enabled={llm.enabled})")
    for kind, d in targets:
        slug = d.get("slug")
        try:
            rec = research_one(d, llm, sb)
            index[slug] = {"researched_at": rec["researched_at"], "status": rec["status"], "kind": kind, "schema": rec.get("schema"), "movie_ready": rec.get("movie_ready"),
                           "class_have": (rec.get("class_checklist") or {}).get("have"), "class_of": (rec.get("class_checklist") or {}).get("of"), "class_missing": (rec.get("class_checklist") or {}).get("missing"),
                           "tradition_status": (rec.get("profile") or {}).get("tradition_status"), "footage": len(rec.get("footage") or []),
                           "citation_rate": (rec.get("citation") or {}).get("rate"), "albums": len(rec.get("albums") or []), "images": len(rec.get("images") or [])}
            rep.inc("researched_" + rec["status"])
            if rec["status"] == "researched":
                notes = load_state("editor_notes.json", {}) or {}
                if (notes.get(slug) or {}).get("note") and not (notes.get(slug) or {}).get("done_at"):
                    notes[slug]["done_at"] = rec["researched_at"]
                    save_state("editor_notes.json", notes)
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

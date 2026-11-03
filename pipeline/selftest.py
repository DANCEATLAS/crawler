"""Offline self-test (no network, no secrets). Run: python -m pipeline.run selftest"""
import json
from .common import norm, slugify, similarity, LLM
from .catalog import NameIndex, completeness
from .research import verify_claims
from .qc import deterministic_gates, decide
from .sync import build_payload
from .hero_qc import check_video
from .taxonomy import country_lookup, sacred_hint

def run():
    fails = []
    def check(name, cond, detail=""):
        print(("ok   " if cond else "FAIL ") + name + ("" if cond else "  " + str(detail)))
        if not cond:
            fails.append(name)
    # text utils
    check("norm accents", norm("Bharatanāṭyam  (dance)") == "bharatanatyam dance", norm("Bharatanāṭyam  (dance)"))
    check("slugify", slugify("Són Cubano!") == "son-cubano", slugify("Són Cubano!"))
    check("country lookup", country_lookup("Côte d'Ivoire") == ("CI", "Africa"), country_lookup("Côte d'Ivoire"))
    check("country lookup multi", country_lookup("Lebanon, Syria")[0] == "LB")
    # index + duplicates
    cat = [{"slug": "tango", "name": "Tango", "aliases": ["tango argentino"]}, {"slug": "son-cubano", "name": "Son Cubano", "aliases": ["son"]}, {"slug": "hora-israeli", "name": "Hora (Israeli)", "aliases": []}]
    idx = NameIndex(cat)
    check("index exact alias", idx.find("Tango Argentino")[0] == "tango")
    check("index fuzzy", idx.find("Son cubano dance")[0] in ("son-cubano",) or idx.find("Son Cubanos")[0] == "son-cubano", idx.find("Son Cubanos"))
    check("index miss", idx.find("Kecak")[0] is None)
    # claims verification
    ev = {"wikipedia": {"url": "https://en.wikipedia.org/wiki/Tango", "text": "Tango is a partner dance and social dance that originated in the 1880s along the Río de la Plata, the natural border between Argentina and Uruguay."}}
    claims = [{"text": "Tango began in the 1880s on the Río de la Plata.", "source": "https://en.wikipedia.org/wiki/Tango", "quote": "originated in the 1880s along the Río de la Plata"},
              {"text": "It was invented in Paris.", "source": "https://en.wikipedia.org/wiki/Tango", "quote": "the dance was invented in Paris by French nobles"}]
    vc, st = verify_claims(claims, ev)
    check("claims verified", vc[0]["supported"] and not vc[1]["supported"] and st["rate"] == 0.5, st)
    # QC gates on a good synthetic record
    long = ("Tango took shape in the port districts of Buenos Aires and Montevideo in the 1880s. " * 25).strip()
    rec = {"slug": "tango", "profile": {"name": "Tango", "tagline": "Close-embrace dance born on the Río de la Plata.",
           "insight": "In 1913 Paris went tango-mad: the dance crossed from the Buenos Aires waterfront to the ballrooms of Europe within a single season.",
           "profile": "Tango is a partner dance that began along the Río de la Plata in the 1880s, danced in a close embrace with improvised walking steps to bandoneón-led orchestras.",
           "profile_long": long, "sections": {"origins_and_history": long[:400], "how_it_is_danced": long[:400], "music_and_instruments": long[:300], "occasions_and_meaning": long[:300]},
           "country": "Argentina", "aliases": ["tango argentino"], "is_sacred": False},
           "citation": {"claims": 8, "supported": 7, "rate": 0.875}, "sources": ["https://en.wikipedia.org/wiki/Tango", "https://www.wikidata.org/wiki/Q1"], "wikipedia_url": "https://en.wikipedia.org/wiki/Tango",
           "region": "South America", "country_code": "AR"}
    gates, dup, sacred = deterministic_gates(rec, idx, {d["slug"]: d for d in cat})
    bad = [g["gate"] for g in gates if not g["ok"]]
    check("gates pass on good record", not bad, bad)
    jd = {"accuracy": 9, "respect": 9, "specificity": 8, "teaching_value": 7, "insight_ok": True, "verdict": "publish", "factual_doubt": []}
    gate, score, reasons = decide(gates, jd, dup, sacred)
    check("decision publish", gate == "publish" and score > 7.5, (gate, score, reasons))
    gate2, _, _ = decide(gates, None, dup, sacred)
    check("decision review without judge", gate2 == "review")
    rec_bad = json.loads(json.dumps(rec)); rec_bad["citation"] = {"claims": 3, "supported": 1, "rate": 0.33}; rec_bad["profile"]["profile_long"] += " As an AI I cannot verify this."
    g3, d3, s3 = deterministic_gates(rec_bad, idx, {})
    gate3, _, r3 = decide(g3, jd, d3, s3)
    check("decision reject on AI tells", gate3 == "reject", (gate3, r3))
    # new candidate duplicate of existing
    rec_dup = json.loads(json.dumps(rec)); rec_dup["slug"] = "tango-argentino"
    g4, d4, _ = deterministic_gates(rec_dup, idx, {d["slug"]: d for d in cat})
    check("duplicate detected", d4 and d4["slug"] == "tango", d4)
    # sacred cue
    sh, cues = sacred_hint("A sacred temple ritual performed by priests as an offering to the deity")
    check("sacred cue", sh, cues)
    # sync payload: existing content_ready keeps card text; needs_curation upgrades
    qc = {"publish_gate": "publish", "qc_score": 8.2, "reasons": [], "gates": gates, "judge": jd, "qc_at": "2026-10-26T00:00:00Z", "is_sacred": False}
    p1 = build_payload(rec, qc, {"tier": "content_ready", "profile": "x", "era": "1880s"})
    check("no overwrite of curated card", "tagline" not in p1 and "profile_long" in p1 and "research" in p1, list(p1))
    p2 = build_payload(rec, qc, {"tier": "needs_curation", "profile": ""})
    check("upgrade thin entry", p2.get("tagline") and p2.get("tier") == "content_ready" and p2.get("region") == "South America", {k: p2.get(k) for k in ("tagline", "tier", "region")})
    # completeness ordering
    c1 = completeness({"slug": "a", "profile": "x" * 3000, "insight": "i", "hero_video_youtube_id": "v", "albums": [1, 2, 3], "images": [1, 2], "sources": ["a", "b"], "wikipedia_url": "w", "country": "c", "region": "r"})
    c2 = completeness({"slug": "b", "profile": "short"})
    check("completeness ordering", c1 > c2, (c1, c2))
    # hero checks without vision
    meta = {"v1": {"title": "Tango performance at the milonga", "channel": "Milonga TV", "desc": "", "category": "22", "live": "none", "tags": [], "duration": 180, "hd": True, "dimension": "2d", "embeddable": True, "privacy": "public", "views": 1000, "likes": 50, "thumb": None},
            "v2": {"title": "Tango (Official Music Video)", "channel": "Vevo", "desc": "", "category": "10", "live": "none", "tags": [], "duration": 200, "hd": True, "dimension": "2d", "embeddable": True, "privacy": "public", "views": 1000, "likes": 50, "thumb": None}}
    llm = LLM(); llm.dry = True
    r1 = check_video("v1", {"name": "Tango", "aliases": []}, meta, llm, use_vision=False)
    r2 = check_video("v2", {"name": "Tango", "aliases": []}, meta, llm, use_vision=False)
    r3 = check_video("v3", {"name": "Tango", "aliases": []}, meta, llm, use_vision=False)
    check("hero pass", r1["verdict"] == "pass", r1)
    check("hero music video fails", r2["verdict"] == "fail", r2)
    check("hero missing fails", r3["verdict"] == "fail", r3)
    print("SELFTEST", "PASSED" if not fails else "FAILED: " + ", ".join(fails))
    # episode packs and the teaching playbook (movie phase)
    try:
        from .episodes import build_pack, render_md as _epmd, verify_polish
        from .pedagogy import render_playbook, _aggregate
        rec = {"slug": "test-dance", "name": "Test Dance", "researched_at": "2026-11-03T00:00:00Z", "citation": {"claims": 5, "supported": 5}, "sources": ["https://en.wikipedia.org/wiki/Test"],
               "images": [{"url": "u1", "thumb": "t1", "attribution": "a", "license": "CC BY-SA 4.0"}] * 3, "footage": [{"url": "f1", "title": "Test Dance 1950", "license": "CC BY"}],
               "albums": [{"title": "Album", "artist": "Band", "year": "1960"}], "region": "Europe",
               "profile": {"name": "Test Dance", "country": "Testland", "era": "19th century", "insight": "A hook with a year 1880 in it for the cold open.", "tagline": "tag", "aliases": ["Tanz"],
                           "sections": {k: "This is a long enough section sentence about the dance. It continues with Dr. Smith of St. Louis in 1880. A third sentence ends it." for k in ("origins_and_history", "how_it_is_danced", "music_and_instruments", "costume_and_setting", "occasions_and_meaning", "notable_figures", "regional_variants", "lineage")},
                           "teaching": {"basic_steps": ["Step forward on the left foot on count one", "Close the right foot on count two", "Step back on three", "Close on four", "Turn a quarter on five and six"]},
                           "music_profile": {"tempo_bpm": "about 120 bpm", "meter": "2/4 time signature", "rhythm_pattern": "oompah with syncopation on the and", "instruments": ["banjo", "violin"], "sound_description": "A bright march with a bouncing oompah bass under syncopated melody lines."},
                           "movement_profile": {"posture": "Upright torso, chest lifted, weight slightly forward over the balls of the feet.", "footwork": "Walk on counts 1-2-3-4 with a kick on 4, strut on 5-6-7-8.", "arms_and_hands": "Arms swing freely from the shoulder, elbows soft.", "formation_and_space": "Couples in a procession around the room.", "signature_moves": [{"name": "The Strut", "description": "A high step with the knee lifted."}, {"name": "The Kick", "description": "A low kick on count four."}], "what_to_avoid": "Do not lock the knees or lean back from the waist.", "difficulty": "beginner"},
                           "episode_brief": {"title_hook": "The dance that won the cake", "logline": "A walk that became a strut.", "beats": ["a", "b", "c", "d", "e"], "lesson_ladder": [{"level": "Beginner", "goal": "walk the basic in time", "drills": ["walk and count", "add the kick"]}, {"level": "Intermediate", "goal": "add the strut"}, {"level": "Advanced", "goal": "dance it with a partner"}], "instructor_persona": "A precise vernacular jazz dancer.", "music_cue": "bright 2/4"},
                           "connections": [{"name": "Ragtime", "relation": "sibling", "note": "shares the music."}, {"name": "Lindy Hop", "relation": "descendant"}], "tradition_status": "revived", "is_sacred": False,
                           "adaptations": {"seniors": {"seated_version": "Seated: tap the counts with the feet and swing the arms.", "counts": "1-2-3-4"}, "children": {"game_version": "Walk-freeze game: freeze on count 8.", "counts": "1-8"}, "derived": True}}}
        pack = build_pack(rec, {"qc_score": 9.9, "is_sacred": False}, {"hero_video_youtube_id": "abc", "hero_qc": {"verdict": "pass"}}, {})
        check("episode pack complete", pack["status"] == "complete" and not pack["gaps"], pack["gaps"])
        check("episode pack scenes", len(pack["episode_1"]["scenes"]) == 10 and len(pack["chapters"]) == 3 and all(len(c["scenes"]) == 9 for c in pack["chapters"]))
        check("episode tempo parsed", pack["music_brief"]["tempo_bpm"] == 120 and pack["music_brief"]["meter"] == "2/4", pack["music_brief"].get("meter"))
        check("episode sentences keep initials", any("Dr. Smith of St. Louis" in n for n in pack["episode_1"]["scenes"][1]["narration"]), pack["episode_1"]["scenes"][1]["narration"])
        md = _epmd(pack)
        check("episode markdown", "## Episode 1" in md and "## Chapter 3" in md and "Music brief" in md and "Narrator's wardrobe" in md)
        check("narrator dressed from sources", pack["visual_brief"]["wardrobe"]["dress_the_narrator"] is True and not pack["visual_brief"]["wardrobe"]["restricted_attire"])
        kept = verify_polish(pack, {"episode_1": [{"code": "hook", "narration": ["In 1880 a walk became a strut."]}, {"code": "where", "narration": ["Founded by Napoleon in 1799."]}]}, rec)
        check("polish verified (keeps true, drops invented)", kept == 1 and pack["episode_1"]["scenes"][0]["narration"] == ["In 1880 a walk became a strut."] and "Napoleon" not in " ".join(pack["episode_1"]["scenes"][1]["narration"]), kept)
        sacred = dict(rec); sacred["profile"] = dict(rec["profile"], is_sacred=True, sacred_note="Restricted to initiates; we do not teach it.")
        sp = build_pack(sacred, {}, {}, {})
        check("sacred pack withholds chapters", sp["status"] == "withheld-chapters" and not sp["chapters"] and "Restricted" in " ".join(sp["episode_1"]["scenes"][8]["narration"]))
        check("sacred pack keeps the narrator in neutral dress", sp["visual_brief"]["wardrobe"]["restricted_attire"] is True and not sp["visual_brief"]["wardrobe"]["dress_the_narrator"])
        agg = _aggregate([{"status": "ok", "slug": "a", "dance": "A", "youtube_id": "x", "extraction": {"counting_scheme": "5-6-7-8", "cues": ["and one", "from the top"], "common_mistakes": ["rushing the count"], "absorbability": {"what_works": ["slow first"], "what_hinders": []}, "demonstration": {"angles": ["front", "back"], "tempo_progression": ["slow", "full"], "repetitions_per_step": 3}, "lesson_structure": [{"t": "0:00", "segment": "intro"}, {"t": "1:00", "segment": "breakdown"}, {"t": "4:00", "segment": "music_practice"}], "quotes": [{"t": "0:10", "text": "hi"}]}}])
        check("pedagogy aggregate", agg["videos"] == 1 and agg["counting"] == "5-6-7-8" and agg["segment_order"] == ["intro", "breakdown", "music_practice"], agg)
        check("playbook renders", "ULTIMATE TEACHER" in render_playbook({"videos_ok": 1, "videos_total": 1, "global": agg, "by_family": {}, "by_slug": {"a": agg}}))
        from .translate import verify as _tv, episode1_ready
        check("translation keeps numbers and names", _tv(["Count 1-2-3-4 with Cakewalk."], ["Cuenta 1-2-3-4 con Cakewalk."], ["Cakewalk"]) and not _tv(["Count 1-2-3-4 with Cakewalk."], ["Cuenta 1-2-3 con Cakewalk."], ["Cakewalk"]) and not _tv(["Count 1-2-3-4 with Cakewalk."], ["Cuenta 1-2-3-4 con el paseo."], ["Cakewalk"]))
        check("episode 1 ready", episode1_ready(pack) and not episode1_ready({"episode_1": {"scenes": [{"needs": ["tempo"]}]}}))
    except Exception as e:
        check("movie phase selftest", False, repr(e))
    return {"counters": {"failures": len(fails)}}

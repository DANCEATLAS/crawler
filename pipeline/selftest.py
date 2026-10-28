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
    return {"counters": {"failures": len(fails)}}

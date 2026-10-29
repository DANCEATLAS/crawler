"""Quality control for researched profiles.

Deterministic gates first (schema, citations, taxonomy, duplicates, sacred
handling, banned phrasing, AI tells), then an independent model-judge with a
rubric.  The result is a publish gate: publish / review / reject, with the
reasons recorded so the review queue is actionable.
"""
import re, os, json
from .common import LLM, log, warn, norm, now_iso, jsave, jload, Report, load_state, save_state, Supabase, PIPELINE_VERSION
from .catalog import load_catalog, NameIndex
from .taxonomy import REGIONS, FAMILIES, country_lookup
from .research import RESULTS_DIR

QC_DIR = os.environ.get("QC_DIR", "qc_results")
os.makedirs(QC_DIR, exist_ok=True)

BANNED = ["foundational", "codified", "crystallised", "crystallized", "rich heritage", "communal spirit", "rich tapestry", "vibrant tapestry",
          "arguably", "it is often said", "testament to", "deeply rooted", "steeped in", "time-honored", "time-honoured", "mesmerizing", "mesmerising",
          "exotic", "primitive", "tribal rhythms", "mystical east", "oriental", "savage", "uncivilized", "delve", "tapestry"]
AI_TELLS = ["as an ai", "i cannot", "i can't", "i do not have access", "language model", "as of my knowledge", "the provided sources", "based on the sources provided", "in the sources provided"]
MIN_CLAIMS = 6          # or 4 claims at >= 90 % verified
MIN_LONG = 1200         # characters of profile_long

RUBRIC = """You are the fact-checker and cultural reviewer of the Dancing Atlas. Review the profile against the evidence claims.
Score 1-10 on each: accuracy (every statement supported by the claims/quotes; penalise anything not traceable), respect (no exoticising, stereotyping or appropriation framing; sacred/restricted practices handled correctly), specificity (concrete people, places, dates, objects; no filler), teaching_value (the how_it_is_danced and teaching fields could guide a beginner).
Also return is_a_dance (bool: the subject is a dance tradition or style, not a country, show, group, person, song or category), factual_doubt (list of sentences you believe unsupported or wrong), harm_or_disrespect (list), duplicate_suspicion (another dance name this seems to be the same as, or null), insight_ok (bool: the insight is one concrete hook, not abstract), album_doubt (list of album titles from ALBUMS that are not credibly central recordings of this dance's own music — a pop, film or fusion album that merely features or mentions the dance belongs here), overall (1-10), verdict ("publish" | "review" | "reject"), notes (<= 60 words).
Return ONE FLAT JSON object with exactly these keys at the top level (no nested "flags" object): accuracy, respect, specificity, teaching_value, is_a_dance, factual_doubt, harm_or_disrespect, duplicate_suspicion, insight_ok, album_doubt, overall, verdict, notes."""

def flat_judge(jd):
    """Older judge outputs nested the flag fields under "flags"; read them from either place."""
    if isinstance(jd, dict) and isinstance(jd.get("flags"), dict):
        jd = dict(jd)
        for k, v in jd.pop("flags").items():
            jd.setdefault(k, v)
    return jd

def _gate(name, ok, detail=""):
    return {"gate": name, "ok": bool(ok), "detail": str(detail)[:200]}

def deterministic_gates(rec, idx, catalog_by_slug):
    p = rec.get("profile") or {}
    gates = []
    tag, ins, prof, long = (p.get("tagline") or ""), (p.get("insight") or ""), (p.get("profile") or ""), (p.get("profile_long") or "")
    sections = p.get("sections") or {}
    nonempty = [k for k, v in sections.items() if v and len(str(v).strip()) > 120]
    gates.append(_gate("has_name", bool(p.get("name")), p.get("name")))
    gates.append(_gate("tagline_len", 10 <= len(tag) <= 110, len(tag)))
    gates.append(_gate("insight_len", 40 <= len(ins) <= 260, len(ins)))
    concrete = bool(re.search(r"\b(1[0-9]{3}|20[0-2][0-9])\b", ins)) or len(re.findall(r"\b[A-Z][a-z]+", ins)) >= 2 or bool(re.search(r"\d", ins))
    gates.append(_gate("insight_concrete", concrete, ins[:80]))
    gates.append(_gate("profile_len", len(prof) >= 150, len(prof)))
    gates.append(_gate("profile_long_len", len(long) >= MIN_LONG, len(long)))
    gates.append(_gate("sections_filled", len(nonempty) >= 4, ",".join(nonempty)))
    cit = rec.get("citation") or {}
    n_cl, rate = (cit.get("claims") or 0), (cit.get("rate") or 0)
    gates.append(_gate("citations", (n_cl >= MIN_CLAIMS and rate >= 0.75) or (n_cl >= 4 and rate >= 0.9), f"{cit.get('supported')}/{cit.get('claims')} rate={cit.get('rate')}"))
    gates.append(_gate("sources", len(rec.get("sources") or []) >= 2 and bool(rec.get("wikipedia_url")), len(rec.get("sources") or [])))
    iso, _ = country_lookup(p.get("country") or "")
    gates.append(_gate("country", bool(p.get("country")) and bool(iso or rec.get("country_code")), p.get("country")))
    gates.append(_gate("region", rec.get("region") in REGIONS, rec.get("region")))
    text_all = " ".join([tag, ins, prof, long] + [str(v) for v in sections.values()]).lower()
    banned_hits = [b for b in BANNED if b in text_all]
    gates.append(_gate("banned_phrasing", len(banned_hits) <= 1, ",".join(banned_hits)))
    tells = [t for t in AI_TELLS if t in text_all]
    gates.append(_gate("ai_tells", not tells, ",".join(tells)))
    # repetition: identical paragraphs
    paras = [norm(x) for x in re.split(r"\n\s*\n", long) if len(x) > 80]
    gates.append(_gate("no_repetition", len(paras) == len(set(paras)), f"{len(paras)} paras"))
    # duplicates against catalogue (for new dances) and alias collisions
    slug = rec.get("slug")
    dup = None
    if slug not in catalog_by_slug:
        found, score = idx.find(p.get("name") or slug)
        if found and found != slug:
            dup = {"slug": found, "score": round(score, 3)}
        for a in (p.get("aliases") or []):
            f2, s2 = idx.find(a, threshold=0.97)
            if f2 and f2 != slug and not dup:
                dup = {"slug": f2, "score": round(s2, 3), "via_alias": a}
    gates.append(_gate("not_duplicate", dup is None, json.dumps(dup) if dup else ""))
    sacred = bool(p.get("is_sacred")) or bool(rec.get("sacred_cue_flag"))
    gates.append(_gate("sacred_handled", (not sacred) or bool(p.get("sacred_note")), f"sacred={sacred} cues={rec.get('sacred_cues')}"))
    return gates, dup, sacred

def judge(rec, llm):
    p = rec.get("profile") or {}
    claims = [{"text": c.get("text"), "quote": c.get("quote"), "supported": c.get("supported")} for c in (rec.get("claims") or [])][:40]
    user = ("PROFILE JSON:\n" + json.dumps({k: p.get(k) for k in ("name", "tagline", "insight", "profile", "profile_long", "sections", "is_sacred", "sacred_note", "teaching", "country", "era")}, ensure_ascii=False)[:14000]
            + "\n\nALBUMS (verified to exist in MusicBrainz; judge their relevance):\n" + json.dumps([{"title": a.get("title"), "artist": a.get("artist"), "year": a.get("year")} for a in (rec.get("albums") or [])], ensure_ascii=False)[:1500]
            + "\n\nEVIDENCE CLAIMS (quote verified mechanically where supported=true):\n" + json.dumps(claims, ensure_ascii=False)[:8000])
    return flat_judge(llm.json(RUBRIC, user, strong=False, temperature=0.1, max_tokens=1500))

def decide(gates, jd, dup, sacred):
    jd = flat_judge(jd)
    hard_fail = [g["gate"] for g in gates if not g["ok"] and g["gate"] in ("has_name", "citations", "sources", "country", "ai_tells", "not_duplicate")]
    soft_fail = [g["gate"] for g in gates if not g["ok"] and g["gate"] not in hard_fail]
    score = 0.0
    if jd:
        score = round(0.35 * float(jd.get("accuracy") or 0) + 0.25 * float(jd.get("respect") or 0) + 0.25 * float(jd.get("specificity") or 0) + 0.15 * float(jd.get("teaching_value") or 0), 2)
    harm = bool((jd or {}).get("harm_or_disrespect"))
    doubts = (jd or {}).get("factual_doubt") or []
    not_dance = bool(jd) and (jd.get("is_a_dance") is False)
    if harm or not_dance or ("ai_tells" in hard_fail) or (jd and (jd.get("verdict") == "reject" or score < 4.5)):
        gate = "reject"
    elif hard_fail or (not jd) or score < 7.5 or len(doubts) > 2 or dup:
        gate = "review"
    elif soft_fail and not (len(soft_fail) <= 1 and score >= 8.5):   # one soft miss is tolerated when the judge is clearly happy
        gate = "review"
    elif jd.get("insight_ok") is False and score < 8.5:
        gate = "review"
    else:
        gate = "publish"
    reasons = hard_fail + soft_fail + ([f"judge_score={score}"] if jd else ["no_judge"]) + ([f"doubts={len(doubts)}"] if doubts else []) + (["harm"] if harm else []) + (["not_a_dance"] if not_dance else []) + (["sacred"] if sacred else [])
    return gate, score, reasons

def qc_one(rec, idx, catalog_by_slug, llm):
    gates, dup, sacred = deterministic_gates(rec, idx, catalog_by_slug)
    jd = judge(rec, llm) if llm.enabled else None
    reused = False
    if llm.enabled and not jd:
        # the model is unavailable (quota, outage): an earlier judge reading of the SAME research is still valid, reuse it
        prev = jload(os.path.join(QC_DIR, rec["slug"] + ".json"))
        if prev and prev.get("judge") and prev.get("researched_at") == rec.get("researched_at"):
            jd, reused = flat_judge(prev["judge"]), True
    gate, score, reasons = decide(gates, jd, dup, sacred)
    out = {"slug": rec["slug"], "qc_at": now_iso(), "version": PIPELINE_VERSION, "publish_gate": gate, "qc_score": score,
           "gates": gates, "judge": jd, "judge_reused": reused, "duplicate_of": dup, "is_sacred": sacred, "reasons": reasons,
           "citation": rec.get("citation"), "researched_at": rec.get("researched_at")}
    jsave(os.path.join(QC_DIR, rec["slug"] + ".json"), out)
    return out

def run(only=None, max_n=200):
    rep = Report("qc")
    llm = LLM()
    sb = Supabase()
    catalog = load_catalog(sb)
    idx = NameIndex(catalog)
    by_slug = {d["slug"]: d for d in catalog}
    qindex = load_state("qc_index.json", {})
    rindex = load_state("research_index.json", {})
    todo = []
    for slug, meta in rindex.items():
        if only and slug not in only:
            continue
        if meta.get("status") != "researched":
            continue
        q = qindex.get(slug)
        if q and q.get("researched_at") == meta.get("researched_at") and q.get("version") == PIPELINE_VERSION:
            continue
        todo.append(slug)
    todo = todo[:max_n]
    rep.note(f"qc targets: {len(todo)} (judge enabled={llm.enabled})")
    for slug in todo:
        rec = jload(os.path.join(RESULTS_DIR, slug + ".json"))
        if not rec or rec.get("status") != "researched":
            continue
        try:
            out = qc_one(rec, idx, by_slug, llm)
            # a record judged while the model was unavailable (quota, outage) is not locked in: it is re-judged on the next run
            ver = PIPELINE_VERSION if (out.get("judge") or not llm.enabled) else "nojudge"
            qindex[slug] = {"qc_at": out["qc_at"], "publish_gate": out["publish_gate"], "qc_score": out["qc_score"], "researched_at": rec.get("researched_at"), "version": ver, "reasons": out["reasons"][:8]}
            rep.inc("gate_" + out["publish_gate"])
            log(f"QC {slug}: {out['publish_gate']} score={out['qc_score']} reasons={out['reasons']}")
        except Exception as e:
            rep.error(f"{slug}: {e}")
        save_state("qc_index.json", qindex)
    rep.inc("llm_calls", llm.calls)
    return rep.finish()

"""Catalogue audit: find entries that should not be in the Atlas (doubles, non-dances) and merge/retire them.

Deterministic signals (certain → retire/merge automatically):
  * research notes marked "NOT A DANCE" / `duplicate_of` in danceworld_final_622.json
  * two slugs sharing the same Wikidata id or the same Wikipedia article
  * the entry's name is a country
  * exact normalised name/alias collision between two slugs
Model signal (batched, cheap): "is this a dance tradition?" with a category; a confident
"no" retires the entry and it is listed in QC_REPORT.md.  Decisions live in
pipeline_state/audit.json; put manual overrides in audit_overrides.json ({slug: "keep"|"retire"}).
"""
import os, json
from collections import defaultdict
from .common import LLM, log, warn, norm, similarity, now_iso, jload, load_state, save_state, Report

MAX_JUDGE_RETIRE = int(os.environ.get("MAX_JUDGE_RETIRE", "25"))
from .catalog import load_app_catalog, completeness
from .taxonomy import COUNTRIES_N

JUDGE = """You classify catalogue entries for an encyclopedia of dance traditions. For each entry decide whether it is a DANCE TRADITION OR STYLE (a named way of dancing practised by people: folk, social, ritual, classical, street, partner, stage genres and specific named dances) — as opposed to a country, a place, a TV show, a company or troupe, a person, a song, a festival, an instrument, a music genre with no dance of its own, or a generic category page.
Return JSON: {"results": [{"slug": str, "is_dance": bool, "category": "dance|country|place|tv_show|group_or_company|person|song_or_album|festival|instrument|music_genre_only|category_page|other", "confidence": 0-1, "note": "<=15 words"}]}"""

def deterministic(styles, research):
    decisions = {}
    def mark(slug, decision, reason, into=None):
        if slug not in decisions:
            decisions[slug] = {"decision": decision, "reason": reason, "into": into, "by": "rule"}
    # research notes
    for slug, r in research.items():
        if slug not in styles:
            continue
        notes = (r.get("notes") or "").upper()
        if "NOT A DANCE" in notes or "MISLABEL" in notes:
            mark(slug, "retire", "research notes: not a dance")
        if r.get("duplicate_of") and r["duplicate_of"] in styles and r["duplicate_of"] != slug:
            mark(slug, "merge", "research notes: duplicate", r["duplicate_of"])
    # country names
    for slug, s in styles.items():
        if norm(s.get("name")) in COUNTRIES_N and norm(s.get("name")) == norm(s.get("country") or ""):
            mark(slug, "retire", "name is a country")
    # shared ids
    for key in ("wikidata_qid", "wikipedia_url"):
        groups = defaultdict(list)
        for slug, s in styles.items():
            v = (s.get(key) or "").strip().rstrip("/")
            if v:
                groups[v.lower()].append(slug)
        for v, slugs in groups.items():
            live = [x for x in slugs if x not in decisions]
            if len(live) < 2:
                continue
            targets = {d.get("into") for d in decisions.values() if d.get("into")}
            keep = max(live, key=lambda x: (x in targets, completeness(styles[x]), -len(x)))
            for other in live:
                if other == keep:
                    continue
                sim = similarity(styles[other].get("name") or other, styles[keep].get("name") or keep)
                # a shared Wikidata item is strong evidence, a shared article weaker; very different names need a human either way
                if (key == "wikidata_qid" and sim >= 0.5) or sim >= 0.75:
                    mark(other, "merge", f"shares {key} with {keep} (name similarity {sim:.2f})", keep)
                else:
                    mark(other, "review", f"shares {key} with {keep} but names differ ({sim:.2f}) — check the data", keep)
    # exact name collisions
    names = defaultdict(list)
    for slug, s in styles.items():
        names[norm(s.get("name"))].append(slug)
    for n, slugs in names.items():
        live = [x for x in slugs if x not in decisions]
        if len(live) > 1 and n:
            targets = {d.get("into") for d in decisions.values() if d.get("into")}
            keep = max(live, key=lambda x: (x in targets, completeness(styles[x]), -len(x)))
            for other in live:
                if other != keep:
                    mark(other, "merge", f"same name as {keep}", keep)
    # never retire a merge target
    for slug, d in list(decisions.items()):
        if d.get("into") and decisions.get(d["into"], {}).get("decision") in ("merge", "retire"):
            decisions.pop(d["into"], None)
    return decisions

def run(llm_budget=300):
    rep = Report("audit")
    styles = {s["slug"]: s for s in load_app_catalog()}
    if not styles:
        rep.error("app_catalog.json missing"); return rep.finish()
    research = {r.get("slug"): r for r in (jload("danceworld_final_622.json", []) or []) if isinstance(r, dict)}
    audit = load_state("audit.json", {})
    overrides = jload("audit_overrides.json", {}) or {}
    rules = deterministic(styles, research)
    for slug, d in rules.items():
        if audit.get(slug, {}).get("by") == "override":
            continue
        if audit.get(slug, {}).get("decision") != d["decision"]:
            audit[slug] = dict(d, at=now_iso())
            rep.inc("rule_" + d["decision"])
    # model pass over entries not yet judged
    llm = LLM()
    todo = [s for s in styles if s not in audit or (audit[s].get("by") == "rule" and audit[s].get("decision") == "keep" and not audit[s].get("judge"))]
    todo = [s for s in todo if s not in rules][:llm_budget]
    if llm.enabled and todo:
        for i in range(0, len(todo), 20):
            batch = todo[i:i + 20]
            items = [{"slug": s, "name": styles[s].get("name"), "country": styles[s].get("country"), "tagline": styles[s].get("tagline"),
                      "profile": (styles[s].get("profile") or "")[:300], "wikipedia_url": styles[s].get("wikipedia_url")} for s in batch]
            res = llm.json(JUDGE, json.dumps(items, ensure_ascii=False), strong=False, temperature=0.0, max_tokens=2500)
            results = {r.get("slug"): r for r in ((res or {}).get("results") or []) if isinstance(r, dict)}
            for s in batch:
                r = results.get(s)
                if not r:
                    continue
                conf = float(r.get("confidence") or 0)
                if (not r.get("is_dance")) and conf >= 0.8:
                    # safety valve: a judge that wants to retire more than MAX_JUDGE_RETIRE entries in one run is sent to a human
                    if rep.counters.get("judge_retire", 0) >= MAX_JUDGE_RETIRE:
                        audit[s] = {"decision": "review", "reason": f"judge (over daily retire cap): {r.get('category')} — {r.get('note')}", "by": "judge", "judge": r, "at": now_iso()}
                        rep.inc("judge_review_capped")
                        continue
                    audit[s] = {"decision": "retire", "reason": f"judge: {r.get('category')} — {r.get('note')}", "by": "judge", "judge": r, "at": now_iso()}
                    rep.inc("judge_retire")
                else:
                    audit[s] = {"decision": "keep", "reason": "judge: dance" if r.get("is_dance") else f"judge unsure ({conf})", "by": "judge", "judge": r, "at": now_iso()}
                    rep.inc("judge_keep")
            save_state("audit.json", audit)
    elif todo:
        rep.note(f"judge disabled; {len(todo)} entries not judged")
    for slug, dec in overrides.items():
        if dec in ("keep", "retire"):
            audit[slug] = {"decision": dec, "reason": "manual override", "by": "override", "at": now_iso()}
    save_state("audit.json", audit)
    n_retire = sum(1 for v in audit.values() if v.get("decision") in ("retire", "merge"))
    rep.inc("retired_or_merged_total", n_retire)
    rep.note(f"audit: {n_retire} entries retired/merged of {len(styles)}; judged so far {sum(1 for v in audit.values() if v.get('judge'))}")
    return rep.finish()

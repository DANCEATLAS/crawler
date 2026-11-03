"""The owner's weekly report: how the library grew, how deep each published profile is, what the filters kept out,
whether the machine ran — this week, the last four weeks, and since the start. Deterministic: no model calls.

Comparisons use the repository's own history (every daily run is a commit): the same measurement is taken on the
tree as it was 7 days ago, 28 days ago and at the start of the year (or the first commit), with `git archive`.

Writes  WEEKLY_REPORT.md (latest), reports/weekly/<date>.md (+ .html), pipeline_state/weekly_history.json.
Run:    python -m pipeline.weekly_report            # in the repo root, needs full git history (fetch-depth: 0)
        python -m pipeline.weekly_report --root DIR # measure one tree only (used internally; no git)
The levels and the film-grade standard are defined in STANDARD.md; the code here is the authority for the numbers.
"""
import os, re, sys, json, glob, html, shutil, subprocess, tempfile, datetime as dt
from collections import Counter

try:
    from .research import class_checklist, movie_ready, CHECKLIST, _said, _said_not
except ImportError:  # pragma: no cover
    from research import class_checklist, movie_ready, CHECKLIST, _said, _said_not

REPO = "DANCEATLAS/crawler"
FILM_SCORE = 9.5          # judge score a film-grade page must reach (QC runs it under the current judge version)
PLACEHOLDER_WORDS = ("not described", "not in sources", "not derivable", "not derivable yet", "withheld")

# ---------------------------------------------------------------- what a profile contains, topic by topic
SECTIONS = [("origins_and_history", "Origins & history", "history"), ("how_it_is_danced", "How it is danced", "danced"), ("music_and_instruments", "Music & instruments", "music"),
            ("costume_and_setting", "Costume & setting", "costume"), ("occasions_and_meaning", "Occasions & meaning", "occasions"), ("notable_figures", "Notable figures", "figures"),
            ("regional_variants", "Regional variants", "variants"), ("lineage", "Lineage", "lineage")]

# (label, short code, group, required for film-grade)
TOPICS = [
    *[(lab, code, "Story", True) for key, lab, code in SECTIONS],
    ("Teaching: basic steps written out (3+)", "steps", "Teaching", True),
    ("Teaching: lesson ladder, 3 levels", "ladder", "Teaching", True),
    ("Teaching: what to avoid / safety", "avoid", "Teaching", True),
    ("Music DNA: tempo or meter", "tempo|meter", "Music", False),
    ("Music DNA: tempo and meter", "tempo+meter", "Music", True),
    ("Music DNA: rhythm pattern", "rhythm", "Music", True),
    ("Music DNA: instruments", "instruments", "Music", True),
    ("Music DNA: sound described", "sound", "Music", True),
    ("Music DNA: verified recording", "recording", "Music", True),
    ("Movement DNA: footwork with counts", "footwork", "Movement", True),
    ("Movement DNA: posture", "posture", "Movement", True),
    ("Movement DNA: arms & hands", "arms", "Movement", True),
    ("Movement DNA: formation & space", "formation", "Movement", True),
    ("Movement DNA: signature moves", "signature", "Movement", True),
    ("Episode: hook & insight", "hook", "Episode", True),
    ("Episode: story beats (5+)", "beats", "Episode", True),
    ("Episode: instructor persona", "persona", "Episode", True),
    ("Episode: music cue", "cue", "Episode", True),
    ("Media: hero video passed the vision check", "hero", "Media", True),
    ("Media: licensed images (3+)", "images", "Media", True),
    ("Media: tutorial videos (1+)", "tutorials", "Media", True),
    ("Media: reference footage (1+)", "footage", "Media", True),
    ("Context: tradition status known", "status", "Context", True),
    ("Context: seniors & children versions", "adaptations", "Context", True),
    ("Context: typed connections (2+)", "connections", "Context", True),
    ("Accuracy: every claim verified, 8+ claims", "claims", "Accuracy", True),
    ("Accuracy: 3+ sources incl. a book, archive or scholar", "sources", "Accuracy", True),
    ("Editorial: no open editor note", "note", "Editorial", True),
    ("Editorial: not a suspected double", "double", "Editorial", True),
    ("Editorial: read and approved by the editor", "editor", "Editorial", True),
]
TOPIC_BY_LABEL = {t[0]: t for t in TOPICS}
FILM_REQUIRED = [t[0] for t in TOPICS if t[3]]

def said(v, n=60):
    s = (v or "").strip() if isinstance(v, str) else ""
    return len(s) >= n and not any(w in s.lower() for w in PLACEHOLDER_WORDS)

def _real(v):
    return isinstance(v, str) and len(v.strip()) >= 12 and not any(w in v.lower() for w in PLACEHOLDER_WORDS)

def adaptations_ok(p):
    """Seniors and children versions present with real content — or withheld on purpose because the dance is sacred."""
    a = p.get("adaptations") or {}
    if p.get("is_sacred") and (not a or a.get("withheld")):
        return True
    se, ch = a.get("seniors") or {}, a.get("children") or {}
    s_ok = _real(se.get("seated_version")) or _real(se.get("standing_version"))
    c_ok = _real(ch.get("game_version"))
    return bool(s_ok and c_ok and (se.get("counts") or ch.get("counts")))

def eval_record(slug, rec, qc, st, approvals, notes, extra):
    p = rec.get("profile") or {}
    secs, teach = p.get("sections") or {}, p.get("teaching") or {}
    mp, mv, eb = p.get("music_profile") or {}, p.get("movement_profile") or {}, p.get("episode_brief") or {}
    ck = class_checklist(p, rec.get("images") or [], rec.get("albums") or [], rec.get("footage") or [])
    have = set(CHECKLIST) - set(ck.get("missing") or [])
    cit = rec.get("citation") or {}
    sources = rec.get("sources") or []
    scholarly = bool(rec.get("books")) or bool(rec.get("unesco_ref")) or any((x.get("tier") in ("scholarly", "archive")) for x in (extra.get(slug) or []) if isinstance(x, dict))
    n = notes.get(slug) or {}
    t = {}
    for key, lab, _code in SECTIONS:
        t[lab] = said(secs.get(key))
    t["Teaching: basic steps written out (3+)"] = len([s for s in (teach.get("basic_steps") or []) if _real(s)]) >= 3
    t["Teaching: lesson ladder, 3 levels"] = "lesson_ladder" in have
    t["Teaching: what to avoid / safety"] = _said(mv.get("what_to_avoid"))
    t["Music DNA: tempo or meter"] = "tempo_or_meter" in have
    t["Music DNA: tempo and meter"] = (not _said_not(mp.get("tempo_bpm"))) and (not _said_not(mp.get("meter")))
    t["Music DNA: rhythm pattern"] = _said(mp.get("rhythm_pattern"))
    t["Music DNA: instruments"] = "instruments" in have
    t["Music DNA: sound described"] = "sound_description" in have
    t["Music DNA: verified recording"] = bool(rec.get("albums"))
    t["Movement DNA: footwork with counts"] = "footwork_with_counts" in have
    t["Movement DNA: posture"] = "posture" in have
    t["Movement DNA: arms & hands"] = "arms_and_hands" in have
    t["Movement DNA: formation & space"] = "formation" in have
    t["Movement DNA: signature moves"] = "signature_moves" in have
    t["Episode: hook & insight"] = "hooks" in have
    t["Episode: story beats (5+)"] = "story_beats" in have
    t["Episode: instructor persona"] = _said(eb.get("instructor_persona"))
    t["Episode: music cue"] = _said(eb.get("music_cue"))
    t["Media: hero video passed the vision check"] = ((st or {}).get("hero_qc") or {}).get("verdict") == "pass"
    t["Media: licensed images (3+)"] = "images" in have
    t["Media: tutorial videos (1+)"] = bool((st or {}).get("tutorials"))
    t["Media: reference footage (1+)"] = "footage" in have
    t["Context: tradition status known"] = p.get("tradition_status") in ("living", "revived", "historical")
    t["Context: seniors & children versions"] = adaptations_ok(p)
    t["Context: typed connections (2+)"] = len(p.get("connections") or []) >= 2
    t["Accuracy: every claim verified, 8+ claims"] = (cit.get("claims") or 0) >= 8 and (cit.get("supported") or 0) == (cit.get("claims") or 0)
    t["Accuracy: 3+ sources incl. a book, archive or scholar"] = len(sources) >= 3 and scholarly
    t["Editorial: no open editor note"] = not (n.get("note") and not n.get("done_at"))
    t["Editorial: not a suspected double"] = not (qc or {}).get("duplicate_of")
    # an approval counts only for the text the editor read: a page re-researched after the approval must be read again
    t["Editorial: read and approved by the editor"] = ((approvals.get(slug) or {}).get("at") or "") >= (rec.get("researched_at") or "")[:10] and slug in approvals
    score = (qc or {}).get("qc_score") or 0
    missing = [lab for lab in FILM_REQUIRED if not t.get(lab)]
    if score < FILM_SCORE:
        missing.append(f"judge score {score} < {FILM_SCORE}")
    return {"topics": t, "class_have": ck.get("have", 0), "class_of": ck.get("of", len(CHECKLIST)), "movie_ready": movie_ready(p),
            "film_missing": missing, "score": score}

# ---------------------------------------------------------------- measuring one tree
def _j(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def measure(root):
    """Everything the report needs, from one checkout of the repository (current or historical)."""
    P = lambda *a: os.path.join(root, *a)
    cat = _j(P("public", "catalog", "dances.app.json"), {}) or {}
    styles = cat.get("styles") or {}
    if not styles:  # before the pipeline existed the catalogue lived in other files
        for name in ("app_catalog.json", "dance_list.json", "danceworld_final_622.json"):
            old = _j(P(name), None)
            if isinstance(old, dict) and old.get("styles"):
                styles = old["styles"]; break
            if isinstance(old, list) and old:
                styles = {(d.get("slug") or str(i)): d for i, d in enumerate(old) if isinstance(d, dict)}; break
    stats = _j(P("public", "catalog", "stats.json"), {}) or {}
    retired = {r.get("slug") for r in ((_j(P("public", "catalog", "retired.json"), {}) or {}).get("retired") or []) if isinstance(r, dict)}
    ridx = _j(P("pipeline_state", "research_index.json"), {}) or {}
    qidx = _j(P("pipeline_state", "qc_index.json"), {}) or {}
    audit = _j(P("pipeline_state", "audit.json"), {}) or {}
    cands = _j(P("pipeline_state", "candidates.json"), {}) or {}
    notes = _j(P("pipeline_state", "editor_notes.json"), {}) or {}
    extra = _j(P("pipeline_state", "sources_extra.json"), {}) or {}
    approvals = _j(P("pipeline_state", "editor_approvals.json"), {}) or {}
    runs = _j(P("pipeline_state", "runs.json"), []) or []
    epi_idx = _j(P("public", "catalog", "episodes.json"), {}) or {}
    epi = epi_idx.get("packs") or {}
    ped = _j(P("pedagogy", "teaching_patterns.json"), {}) or {}
    live = {s for s in styles if s not in retired}
    m = {"dances_live": len(live) if styles else int(stats.get("count") or 0),
         "with_hero": sum(1 for s in live if (styles[s].get("hero_video_youtube_id") or "").strip()) if styles else int(stats.get("with_hero") or 0),
         "hero_checked": sum(1 for s in live if (styles[s].get("hero_qc") or {}).get("verdict") == "pass") if styles else int(stats.get("hero_qc_pass") or 0),
         "with_tutorials": sum(1 for s in live if styles[s].get("tutorials")) if styles else int(stats.get("with_tutorials") or 0),
         "retired": len(retired) or sum(1 for v in audit.values() if v.get("decision") in ("retire", "merge")),
         "retired_doubles": sum(1 for v in audit.values() if v.get("decision") == "merge"),
         "screened_moves": sum(1 for v in cands.values() if v.get("status") == "screened_out"),
         "candidates_queued": sum(1 for v in cands.values() if v.get("status") == "queued"),
         "judged": sum(1 for s, v in qidx.items() if v.get("publish_gate")),
         "gate_publish": 0, "gate_review": 0, "gate_reject": 0,
         "researched": 0, "published": 0, "movie_ready": 0, "class_complete": 0, "film_grade": 0,
         "claims": 0, "claims_verified": 0, "schema5": 0,
         "episode_packs": len(epi), "episode_complete": sum(1 for v in epi.values() if v.get("status") == "complete"), "episode_polished": sum(1 for v in epi.values() if v.get("polished")),
         "lessons_studied": int(ped.get("videos_ok") or 0), "teachers_dances": int(((ped.get("global") or {}).get("dances")) or 0),
         "translations": int(epi_idx.get("translations") or 0), "languages": len(epi_idx.get("languages") or []),
         "topics": {lab: 0 for lab, *_ in TOPICS}, "published_slugs": [], "film_slugs": [], "closest": [], "movie_slugs": [], "names": {}}
    for s, v in qidx.items():
        g = v.get("publish_gate")
        if g in ("publish", "review", "reject"):
            m["gate_" + g] += 1
    for s, v in ridx.items():
        if v.get("status") != "researched" or s in retired:
            continue
        rec = _j(P("research_results", s + ".json"), None)
        if not rec or rec.get("status") != "researched":
            continue
        m["researched"] += 1
        if (rec.get("schema") or 0) >= 5:
            m["schema5"] += 1
        if (qidx.get(s) or {}).get("publish_gate") != "publish":
            continue
        qc = _j(P("qc_results", s + ".json"), {}) or {}
        ev = eval_record(s, rec, qc, styles.get(s) or {}, approvals, notes, extra)
        m["published"] += 1
        m["published_slugs"].append(s)
        m["names"][s] = (rec.get("profile") or {}).get("name") or (styles.get(s) or {}).get("name") or s
        m["claims"] += int((rec.get("citation") or {}).get("claims") or 0)
        m["claims_verified"] += int((rec.get("citation") or {}).get("supported") or 0)
        for lab, ok in ev["topics"].items():
            if ok:
                m["topics"][lab] += 1
        if ev["movie_ready"]:
            m["movie_ready"] += 1; m["movie_slugs"].append(s)
        if ev["class_have"] >= len(CHECKLIST):
            m["class_complete"] += 1
        if not ev["film_missing"]:
            m["film_grade"] += 1; m["film_slugs"].append(s)
        m["closest"].append((len(ev["film_missing"]), -ev["score"], (rec.get("profile") or {}).get("name") or s, s, ev["film_missing"], ev["score"], f"{ev['class_have']}/{ev['class_of']}"))
    m["closest"].sort()
    m["closest"] = m["closest"][:10]
    m["runs"] = runs
    return m

# ---------------------------------------------------------------- history through git
def sh(*a, **k):
    return subprocess.run(a, check=True, capture_output=True, text=True, **k).stdout.strip()

def rev_before(when):
    try:
        r = sh("git", "rev-list", "-1", f"--before={when.strftime('%Y-%m-%dT%H:%M:%SZ')}", "HEAD")
    except subprocess.CalledProcessError:
        r = ""
    return r or None

def first_rev():
    return sh("git", "rev-list", "--max-parents=0", "HEAD").splitlines()[-1]

def rev_date(rev):
    return sh("git", "show", "-s", "--format=%cI", rev)[:10]

def measure_rev(rev, cache):
    if rev in cache:
        return cache[rev]
    d = tempfile.mkdtemp(prefix="atlas_rev_")
    try:
        tar = subprocess.run(["git", "archive", "--format=tar", rev], check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", d], input=tar, check=True)
        m = measure(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    m["rev"], m["rev_date"] = rev[:7], rev_date(rev)
    cache[rev] = m
    return m

# ---------------------------------------------------------------- rendering
def delta(now, then, pct=False):
    if then is None:
        return "—"
    d = now - then
    if d == 0:
        return "±0"
    return f"+{d}" if d > 0 else f"−{abs(d)}"

def pc(n, of):
    return f"{(100.0 * n / of):.0f}%" if of else "–"

def health(runs, since):
    days, errors, calls, quota = set(), 0, 0, False
    for r in runs:
        if (r.get("finished") or "") < since:
            continue
        if r.get("stage") == "report":
            days.add((r.get("finished") or "")[:10])
        errors += len(r.get("errors") or [])
        calls += int((r.get("counters") or {}).get("llm_calls") or 0)
        if any("insufficient_quota" in str(e) for e in (r.get("errors") or [])):
            quota = True
    return {"days": len(days), "errors": errors, "calls": calls, "quota": quota}

def verdict(now, week, h):
    bits = []
    bits.append(f"The machine ran on {h['days']} of the last 7 days" + (" without errors." if not h["errors"] else f" and logged {h['errors']} error(s) — the pipeline kept going; the weekly editor session reads them."))
    if week:
        np = now["published"] - week["published"]; nm = now["movie_ready"] - week["movie_ready"]; nd = now["dances_live"] - week["dances_live"]; nr = now["retired"] - week["retired"]
        parts = []
        if np > 0: parts.append(f"published {np} new deep profile{'s' if np != 1 else ''}")
        if nm > 0: parts.append(f"lifted {nm} to movie-ready")
        if nd > 0: parts.append(f"added {nd} dance{'s' if nd != 1 else ''} to the atlas")
        if nr > 0: parts.append(f"retired {nr} double{'s' if nr != 1 else ''} or non-dance{'s' if nr != 1 else ''}")
        if parts:
            bits.append("This week it " + ", ".join(parts) + ".")
        else:
            bits.append("This week nothing new passed the filters — the research queue and the judges are still running; a quiet week is normal when model quotas are tight.")
    need = []
    if h["quota"]:
        need.append("the OpenAI balance is spent (`insufficient_quota` in the run log) — growth continues on Gemini alone; a top-up is your call")
    if h["days"] <= 2:
        need.append("the daily run fired on only " + str(h["days"]) + " day(s) — check the Actions page if this repeats next week")
    bits.append(("**Needs you:** " + "; ".join(need) + ".") if need else "**Nothing needs you.**")
    return " ".join(bits)

def render_md(now, week, month, start, labels, hist, when):
    L = []
    date = when.strftime("%a %d %b %Y")
    L.append(f"# Dance Atlas — weekly report · {date}")
    L.append("")
    L.append(f"**{now['dances_live']:,} dances live** ({delta(now['dances_live'], week and week['dances_live'])} this week) · "
             f"**{now['published']} deep profiles published** ({delta(now['published'], week and week['published'])}) · "
             f"**{now['movie_ready']} movie-ready** ({delta(now['movie_ready'], week and week['movie_ready'])}) · "
             f"**{now['film_grade']} film-grade ★** ({delta(now['film_grade'], week and week['film_grade'])})")
    L.append("")
    h = health(now["runs"], (when - dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ"))
    L.append("> " + verdict(now, week, h))
    L.append("")
    # 1 growth
    L.append("## 1 · Growth")
    L.append("")
    L.append(f"| | Now | This week | Last 4 weeks | {labels['start']} |")
    L.append("|---|---:|---:|---:|---:|")
    rows = [("Dances live on the site", "dances_live"), ("…with a hero video", "with_hero"), ("…hero video passed the vision check", "hero_checked"),
            ("…with tutorial videos", "with_tutorials"), ("Deep profiles researched", "researched"), ("Deep profiles published (passed QC)", "published"),
            ("Movie-ready profiles", "movie_ready"), ("Class-complete profiles (18 of 18)", "class_complete"), ("Film-grade ★ profiles", "film_grade"),
            ("Verified claims in published profiles", "claims_verified"), ("Doubles / non-dances retired (total)", "retired"),
            ("Episode packs written (intro + 3 chapters)", "episode_packs"), ("…complete, no gaps", "episode_complete"), ("…narration polished and verified", "episode_polished"),
            ("…translated into other languages (pack × language)", "translations"), ("Tutorial lessons studied for the teaching playbook", "lessons_studied")]
    for lab, k in rows:
        L.append(f"| {lab} | **{now[k]:,}** | {delta(now[k], week and week[k])} | {delta(now[k], month and month[k])} | {delta(now[k], start and start[k])} |")
    L.append("")
    # 2 ladder
    L.append("## 2 · The ladder — how far the dances have climbed")
    L.append("")
    L.append("| Level | Dances | This week | Last 4 weeks |")
    L.append("|---|---:|---:|---:|")
    ladder = [("0 · Listed in the atlas", "dances_live"), ("1 · Deep profile researched from sources", "researched"),
              ("2 · Published — passed every QC gate and the judge", "published"), ("3 · Movie-ready — music DNA, movement DNA and an episode brief", "movie_ready"),
              ("4 · Class-complete — all 18 things a class needs", "class_complete"), ("5 · Film-grade ★ — every line of STANDARD.md, editor included", "film_grade")]
    for lab, k in ladder:
        L.append(f"| {lab} | **{now[k]:,}** | {delta(now[k], week and week[k])} | {delta(now[k], month and month[k])} |")
    L.append("")
    # 3 topics
    pub = now["published"]
    L.append(f"## 3 · Inside the profiles — of the {pub} published, how many have each piece")
    L.append("")
    L.append("| Piece | Have it | This week | Last 4 weeks |")
    L.append("|---|---:|---:|---:|")
    group = None
    for lab, code, grp, req in TOPICS:
        if grp != group:
            group = grp
            L.append(f"| **{grp}** | | | |")
        n = now["topics"].get(lab, 0)
        w = week["topics"].get(lab) if week else None
        mo = month["topics"].get(lab) if month else None
        short = lab.split(": ", 1)[1] if ": " in lab else lab
        L.append(f"| {short[0].upper() + short[1:]}{'' if req else ' *(info)*'} | {n} ({pc(n, pub)}) | {delta(n, w)} | {delta(n, mo)} |")
    L.append("")
    # 4 filtering
    L.append("## 4 · The filters — what was kept out")
    L.append("")
    L.append("| | Now | This week | Last 4 weeks |")
    L.append("|---|---:|---:|---:|")
    for lab, k in [("Profiles judged by QC", "judged"), ("…passed (published)", "gate_publish"), ("…held for review (an editor decides)", "gate_review"), ("…rejected", "gate_reject"),
                   ("Doubles merged into another entry", "retired_doubles"), ("Doubles and non-dances retired (total)", "retired"), ("Dance moves screened out before research", "screened_moves"),
                   ("Candidates waiting in the research queue", "candidates_queued")]:
        L.append(f"| {lab} | **{now[k]:,}** | {delta(now[k], week and week[k])} | {delta(now[k], month and month[k])} |")
    rate = pc(now["claims_verified"], now["claims"]) if now["claims"] else "–"
    L.append("")
    L.append(f"Every published profile carries claims with a verbatim quote checked against the fetched source: **{now['claims_verified']:,} of {now['claims']:,} claims verified ({rate})**.")
    L.append("")
    # 5 new this week
    if week:
        new_pub = [s for s in now["published_slugs"] if s not in set(week["published_slugs"])]
        new_movie = [s for s in now["movie_slugs"] if s not in set(week["movie_slugs"])]
        if new_pub or new_movie:
            L.append("## 5 · New this week")
            L.append("")
            nm = lambda s: now["names"].get(s) or s.replace("-", " ")
            if new_pub:
                L.append("**Published:** " + ", ".join(nm(s) for s in new_pub[:30]) + (f" … and {len(new_pub) - 30} more" if len(new_pub) > 30 else ""))
                L.append("")
            if new_movie:
                L.append("**Now movie-ready:** " + ", ".join(nm(s) for s in new_movie[:30]) + (f" … and {len(new_movie) - 30} more" if len(new_movie) > 30 else ""))
                L.append("")
    # 6 closest to film grade
    L.append("## 6 · Closest to film-grade ★")
    L.append("")
    if now["film_slugs"]:
        L.append("**Film-grade now:** " + ", ".join(now["names"].get(s) or s for s in now["film_slugs"]))
        L.append("")
    L.append("| Dance | Judge | Checklist | Still missing |")
    L.append("|---|---:|---:|---|")
    for nmiss, _, name, slug, missing, score, cls in now["closest"][:8]:
        codes = [TOPIC_BY_LABEL[x][1] if x in TOPIC_BY_LABEL else x for x in missing]
        L.append(f"| {name} | {score} | {cls} | {nmiss}: {', '.join(codes)} |")
    L.append("")
    # 7 trend
    if len(hist) >= 2:
        L.append("## 7 · Week by week")
        L.append("")
        L.append("| Week | Dances live | Published | Movie-ready | Class-complete | Film-grade | Episode packs |")
        L.append("|---|---:|---:|---:|---:|---:|---:|")
        for r in hist[-10:]:
            L.append(f"| {r['date']} | {r.get('dances_live', 0):,} | {r.get('published', 0)} | {r.get('movie_ready', 0)} | {r.get('class_complete', 0)} | {r.get('film_grade', 0)} | {r.get('episode_packs', 0)} |")
        L.append("")
    # 8 where the machine is stuck — and what would help most (from pipeline_state/lessons_learned.json and tuning.json)
    lessons = _j(os.path.join("pipeline_state", "lessons_learned.json"), {}) or {}
    tuning = _j(os.path.join("pipeline_state", "tuning.json"), {}) or {}
    L.append("## 8 · Where the machine is stuck — and what would help most")
    L.append("")
    hm = lessons.get("help_most") or []
    if hm:
        L.append("| What the scripts lack most | Pages | What would fix it |")
        L.append("|---|---:|---|")
        for x in hm[:6]:
            L.append(f"| {x.get('gap')} | {x.get('pages')} | {x.get('what_helps')} |")
        L.append("")
    if lessons.get("avoid"):
        L.append("The judge's most frequent objections in the last 30 days, now handed to the writer before every page: " + "; ".join(lessons["avoid"][:3]) + ".")
        L.append("")
    if tuning.get("reason"):
        L.append(f"Self-tuning: {tuning['reason']}." + ((" **Alerts:** " + "; ".join(tuning.get("alerts") or [])) if tuning.get("alerts") else ""))
        L.append("")
    # 9 health
    L.append("## 9 · The machine")
    L.append("")
    L.append(f"Daily run fired on **{h['days']} of 7** days · model calls this week **{h['calls']:,}** · errors logged **{h['errors']}** · "
             f"OpenAI balance {'**spent**' if h['quota'] else 'fine'} · {now['schema5']} of {now['researched']} profiles already at research schema 5 (the re-deepening finishes when this reaches all) · "
             f"teaching playbook built from {now['lessons_studied']} lessons across {now['teachers_dances']} dances (`ULTIMATE_TEACHER.md`).")
    L.append("")
    L.append("---")
    L.append("*How to read this.* **Published** = passed every QC gate (sources, verified quotes, country, no AI tells, not a double) and a judge score; "
             "**movie-ready** = music DNA + movement DNA + an episode brief, all from sources; **class-complete** = all 18 things a teachable class needs; "
             "**film-grade ★** = every line of `STANDARD.md`, including an editor's read — the bar is meant to be nearly impossible; "
             "**episode packs** = the scene-by-scene scripts (Episode 1 + three chapters, music and visual briefs) in `episodes/`, written from the profile only (`MOVIE_PHASE.md`). "
             f"Deltas compare the repository as it was 7 days ago, 28 days ago and at {labels['start_long']}. Files: `WEEKLY_REPORT.md`, `STATUS.md`, `QC_REPORT.md` in github.com/{REPO}.*")
    return "\n".join(L) + "\n"

def next_steps(now, lessons_path, when):
    """NEXT_STEPS.md — maintained by the machine for whoever works on it next (the owner, an AI session): the bottlenecks
    the data shows, ranked, with the concrete lever for each; the decisions still open; what not to touch."""
    lessons = _j(lessons_path, {}) or {}
    L = [f"# NEXT STEPS — written by the machine on {when.strftime('%Y-%m-%d')}", "",
         "*Regenerated every Monday by the weekly report from the library's own numbers. Read `AI_BRIEF.md` first; this file says where to push.*", "",
         "## What the numbers say to do first", ""]
    i = 0
    for x in (lessons.get("help_most") or [])[:5]:
        i += 1
        L.append(f"{i}. **{x.get('gap')}** is missing on {x.get('pages')} published pages — {x.get('what_helps')}.")
    if now.get("with_hero", 0) < now.get("dances_live", 0):
        i += 1
        L.append(f"{i}. **{now['dances_live'] - now['with_hero']} dances have no hero video** — the crawler retries them every 21 days; an editor note with a channel or search phrase helps the stubborn ones.")
    if now.get("gate_review"):
        i += 1
        L.append(f"{i}. **{now['gate_review']} pages wait in review** — each needs one decision in `audit_overrides.json` or one editor note (`WEEKLY_PASS.md`).")
    if not now.get("film_grade"):
        i += 1
        L.append(f"{i}. **No page is film-grade yet** — the closest ones and what they lack are in `WEEKLY_REPORT.md` §6; the editor's approval is the last item on every one of them.")
    L += ["", "## Decisions still open (the owner's)", "",
          "- Video platform for the episodes (the packs are platform-neutral; one exporter when named).",
          "- Music generator and voice-over tool (briefs and narration are ready; licences and cost are the owner's call).",
          "- Showing the deep profiles and the episodes on the website (one Lovable paste, `LOVABLE_UI_PROMPT.md`).",
          "- OpenAI top-up when the prepaid balance is spent (the run says so in `STATUS.md` and here).", "",
          "## What not to touch", "",
          "- The QC gates (`pipeline/qc.py`): fewer true pages beat more doubtful ones. The sacred rule. The no-invention rule in the scripts.",
          "- The budgets in the workflow: the machine lowers them itself when the models fail and raises them back; raising them above the defaults costs quota, not quality.",
          "- Lovable: content never goes through it; its AI is for layout only, once, with the prepared prompt.", ""]
    return "\n".join(L)

NUMCELL = re.compile(r"[\*\s]*[+−±]?[\d,\.%–—/]+(\s*\([\d\.%–]+\))?[\*\s]*")

def md_to_html(md):
    """Enough Markdown for this report: headings, tables, paragraphs, blockquote, bold, code, links, rules."""
    def inline(s):
        s = html.escape(s, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
        s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
        return s
    out, table = [], []
    def flush():
        nonlocal table
        if table:
            head = table[0]; body = table[2:] if len(table) > 1 and set(table[1].replace("|", "").strip()) <= set("-: ") else table[1:]
            cells = lambda row: [c.strip() for c in row.strip().strip("|").split("|")]
            out.append("<table>")
            out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells(head)) + "</tr>")
            for r in body:
                tds = []
                for c in cells(r):
                    cls = " class=num" if NUMCELL.fullmatch(c or "-") else ""
                    tds.append(f"<td{cls}>{inline(c)}</td>")
                out.append("<tr>" + "".join(tds) + "</tr>")
            out.append("</table>")
            table = []
    for line in md.splitlines():
        if line.startswith("|"):
            table.append(line); continue
        flush()
        if line.startswith("# "): out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("## "): out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("> "): out.append(f"<blockquote>{inline(line[2:])}</blockquote>")
        elif line.strip() == "---": out.append("<hr>")
        elif line.strip(): out.append(f"<p>{inline(line)}</p>")
    flush()
    css = ("body{font:15px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#1a1a1a;max-width:860px;margin:24px auto;padding:0 16px;background:#fff}"
           "h1{font-size:24px;margin:0 0 8px}h2{font-size:17px;margin:28px 0 8px;border-bottom:1px solid #e5e5e5;padding-bottom:4px}"
           "table{border-collapse:collapse;width:100%;margin:8px 0 16px;font-size:14px}th,td{border:1px solid #e5e5e5;padding:6px 8px;text-align:left;vertical-align:top}"
           "th{background:#f6f6f6}td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}blockquote{margin:12px 0;padding:10px 14px;background:#f3f7f2;border-left:4px solid #4a7c59}"
           "code{background:#f2f2f2;padding:1px 4px;border-radius:3px;font-size:13px}hr{border:0;border-top:1px solid #e5e5e5;margin:24px 0}")
    return f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Dance Atlas weekly report</title><style>{css}</style></head><body>" + "\n".join(out) + "</body></html>"

# ---------------------------------------------------------------- optional direct e-mail
def send_email(md_path, html_path):
    """Sends the report as an e-mail when the three secrets exist (REPORT_SMTP_USER, REPORT_SMTP_PASSWORD, REPORT_TO);
    otherwise does nothing — the GitHub issue thread (see .github/workflows/weekly_report.yml) is the delivery that needs no secret."""
    user, pw, to = os.environ.get("REPORT_SMTP_USER"), os.environ.get("REPORT_SMTP_PASSWORD"), os.environ.get("REPORT_TO")
    if not (user and pw and to):
        print("[weekly_report] no SMTP secrets set; delivery is the GitHub issue thread", file=sys.stderr); return False
    import smtplib
    from email.message import EmailMessage
    md = open(md_path, encoding="utf-8").read()
    head = md.splitlines()[2] if len(md.splitlines()) > 2 else "Dance Atlas weekly report"
    subject = "Dance Atlas weekly report · " + re.sub(r"[*_]|\s*\([^)]*\)", "", head).replace(" · ", " · ")[:120]
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, user, to
    msg.set_content(md)
    msg.add_alternative(open(html_path, encoding="utf-8").read(), subtype="html")
    host, port = os.environ.get("REPORT_SMTP_HOST", "smtp.gmail.com"), int(os.environ.get("REPORT_SMTP_PORT", "587"))
    with smtplib.SMTP(host, port, timeout=60) as smtp:
        smtp.starttls(); smtp.login(user, pw); smtp.send_message(msg)
    print(f"[weekly_report] e-mailed the report to {to.split('@')[0][:2]}…@{to.split('@')[-1]}", file=sys.stderr)
    return True

# ---------------------------------------------------------------- main
def main(argv):
    if "--send" in argv:
        send_email("WEEKLY_REPORT.md", os.path.join("reports", "weekly", "latest.html")); return
    if "--root" in argv:
        root = argv[argv.index("--root") + 1]
        m = measure(root); m.pop("runs", None); m.pop("closest", None); m.pop("names", None)
        print(json.dumps(m, ensure_ascii=False, indent=1)); return
    when = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    if "--as-of" in argv:
        when = dt.datetime.fromisoformat(argv[argv.index("--as-of") + 1]).replace(tzinfo=dt.timezone.utc)
    cache = {}
    now = measure("."); now["rev"] = sh("git", "rev-parse", "--short", "HEAD")
    first = first_rev()
    year0 = dt.datetime(when.year, 1, 1, tzinfo=dt.timezone.utc)
    r_week = rev_before(when - dt.timedelta(days=7))
    r_month = rev_before(when - dt.timedelta(days=28))
    r_start = rev_before(year0) or first
    week = measure_rev(r_week, cache) if r_week else None
    month = measure_rev(r_month, cache) if r_month else None
    start = measure_rev(r_start, cache)
    start_label = f"Since 1 Jan {when.year}" if rev_before(year0) else f"Since the start ({start['rev_date']})"
    labels = {"start": start_label, "start_long": (f"1 January {when.year}" if rev_before(year0) else f"the first commit ({start['rev_date']})")}
    # weekly history: one row per report; back-fill past Mondays from git the first time
    hist_path = os.path.join("pipeline_state", "weekly_history.json")
    hist = _j(hist_path, []) or []
    keys = ("dances_live", "researched", "published", "movie_ready", "class_complete", "film_grade", "retired", "claims_verified", "episode_packs", "episode_complete", "lessons_studied", "translations")
    if not hist:
        monday = (when - dt.timedelta(days=when.weekday())).replace(hour=0, minute=0, second=0)
        for i in range(8, 0, -1):
            d = monday - dt.timedelta(days=7 * i)
            r = rev_before(d)
            if not r:
                continue
            m = measure_rev(r, cache)
            hist.append({"date": d.strftime("%Y-%m-%d"), **{k: m[k] for k in keys}, "rev": m["rev"], "backfilled": True})
    row = {"date": when.strftime("%Y-%m-%d"), **{k: now[k] for k in keys}, "rev": now["rev"]}
    hist = [h for h in hist if h.get("date") != row["date"]] + [row]
    os.makedirs("pipeline_state", exist_ok=True); os.makedirs(os.path.join("reports", "weekly"), exist_ok=True)
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=1)
    md = render_md(now, week, month, start, labels, hist, when)
    with open("WEEKLY_REPORT.md", "w", encoding="utf-8") as f:
        f.write(md)
    with open("NEXT_STEPS.md", "w", encoding="utf-8") as f:
        f.write(next_steps(now, lessons_path=os.path.join("pipeline_state", "lessons_learned.json"), when=when))
    stem = os.path.join("reports", "weekly", when.strftime("%Y-%m-%d"))
    with open(stem + ".md", "w", encoding="utf-8") as f:
        f.write(md)
    with open(stem + ".html", "w", encoding="utf-8") as f:
        f.write(md_to_html(md))
    with open(os.path.join("reports", "weekly", "latest.html"), "w", encoding="utf-8") as f:
        f.write(md_to_html(md))
    print(md)
    print(f"[weekly_report] wrote WEEKLY_REPORT.md, {stem}.md/.html; compared with week={r_week and r_week[:7]} month={r_month and r_month[:7]} start={r_start[:7]}", file=sys.stderr)

if __name__ == "__main__":
    main(sys.argv[1:])

"""The owner's weekly report: how the library grew, how deep each published profile is, what the filters kept out,
whether the machine ran — this week, the last four weeks, and since the start. Deterministic: no model calls.

Comparisons use the repository's own history (every daily run is a commit): the same measurement is taken on the
tree as it was 7 days ago, 28 days ago and at the start of the year (or the first commit), with `git archive`.

Writes  WEEKLY_REPORT.md (latest), NEXT_STEPS.md, reports/weekly/<date>.md (+ .html = the e-mail), pipeline_state/weekly_history.json.
E-mail: `--send` mails reports/weekly/latest.html (table layout, inline styles) when the SMTP secrets exist — see send_email().
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

def mdbar(n, of, width=12):
    """A progress bar in text, for the Markdown report (GitHub renders it in monospace inside backticks)."""
    full = 0 if not of or n <= 0 else max(1, int(round(width * min(1.0, n / of))))
    return "`" + "█" * full + "░" * (width - full) + "`"

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
    if h["days"] <= 2:
        bits.append(f"GitHub ran the daily job on only {h['days']} day(s) this week; the watchdog restarts dropped runs and NEXT_STEPS.md flags it for the next session.")
    need = []  # only what the owner alone can do: money and keys
    if h["quota"]:
        need.append("the OpenAI balance is spent (`insufficient_quota` in the run log) — growth continues on Gemini alone; a top-up is your call")
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
    L.append("| Level | Share of all dances | Dances | This week | Last 4 weeks |")
    L.append("|---|---|---:|---:|---:|")
    ladder = [("0 · Listed in the atlas", "dances_live"), ("1 · Deep profile researched from sources", "researched"),
              ("2 · Published — passed every QC gate and the judge", "published"), ("3 · Movie-ready — music DNA, movement DNA and an episode brief", "movie_ready"),
              ("4 · Class-complete — all 18 things a class needs", "class_complete"), ("5 · Film-grade ★ — every line of STANDARD.md, editor included", "film_grade")]
    for lab, k in ladder:
        L.append(f"| {lab} | {mdbar(now[k], now['dances_live'])} {pc(now[k], now['dances_live'])} | **{now[k]:,}** | {delta(now[k], week and week[k])} | {delta(now[k], month and month[k])} |")
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

# ---------------------------------------------------------------- the e-mail (and reports/weekly/*.html)
# Table layout, every style inline, no scripts, no background images: the only HTML that Hotmail/Outlook, Gmail and
# the phone apps all render the same way. Progress first — the four numbers and their week-on-week change — then the
# ladder, the week-by-week strip, every piece of every profile, the filters, and what would help most.
INK, MUTED, LINE, PALE, GREEN, GREEN_PALE, RED, AMBER = "#1a1a1a", "#6b6b6b", "#e3e3e3", "#f4f6f3", "#2f6b3a", "#dcebdf", "#9b2f2f", "#8a6d1e"
FONT = "font-family:Helvetica,Arial,sans-serif;"

def _inline(s):
    """Bold, code and italics from the Markdown strings this module already writes."""
    s = html.escape(str(s), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code style='font-family:Menlo,Consolas,monospace;font-size:12px;background:#f1f1f1;padding:1px 4px;border-radius:3px'>\1</code>", s)
    s = re.sub(r"(?<![\w*])\*(?!\*)(.+?)\*(?![\w*])", r"<em>\1</em>", s)
    return s

def _chip(now_v, then_v, suffix=""):
    """The change since a past measurement, coloured: green up, red down, grey flat, dash when there is no past tree."""
    if then_v is None:
        return f"<span style='color:{MUTED}'>—</span>"
    d = now_v - then_v
    if d == 0:
        return f"<span style='color:{MUTED}'>±0{suffix}</span>"
    col, sign = (GREEN, "+") if d > 0 else (RED, "−")
    return f"<span style='color:{col};font-weight:bold'>{sign}{abs(d):,}{suffix}</span>"

def _bar(n, of, width=140, color=GREEN, height=10):
    """A horizontal bar as a two-cell table: works in every client, including Outlook."""
    pct = 0 if not of else max(0.0, min(100.0, 100.0 * n / of))
    fill = 0 if n <= 0 else max(2, int(round(pct)))
    rest = 100 - fill
    cells = f"<td width='{fill}%' bgcolor='{color}' style='width:{fill}%;height:{height}px;line-height:{height}px;font-size:1px;background:{color}'>&nbsp;</td>" if fill else ""
    if rest:
        cells += f"<td width='{rest}%' bgcolor='#ececec' style='width:{rest}%;height:{height}px;line-height:{height}px;font-size:1px;background:#ececec'>&nbsp;</td>"
    return f"<table role='presentation' cellpadding='0' cellspacing='0' border='0' width='{width}' style='width:{width}px;border-collapse:collapse'><tr>{cells}</tr></table>"

def _h2(title, sub=None):
    return (f"<tr><td style='padding:28px 0 8px;{FONT}'><div style='font-size:17px;font-weight:bold;color:{INK};border-bottom:1px solid {LINE};padding-bottom:6px'>{html.escape(title)}</div>"
            + (f"<div style='font-size:13px;color:{MUTED};padding-top:6px'>{_inline(sub)}</div>" if sub else "") + "</td></tr>")

def _p(text, size=14, color=INK, pad="6px 0"):
    return f"<tr><td style='padding:{pad};{FONT}font-size:{size}px;line-height:1.5;color:{color}'>{_inline(text)}</td></tr>"

def _table(headers, rows, aligns=None, widths=None):
    """A data table; `rows` are lists of already-rendered HTML cells. aligns: 'l'/'r' per column."""
    aligns = aligns or ["l"] * len(headers)
    th = "".join(f"<th align='{'right' if a == 'r' else 'left'}' style='padding:7px 5px;{FONT}font-size:11px;color:{MUTED};font-weight:normal;text-transform:uppercase;letter-spacing:.03em;border-bottom:1px solid {LINE};text-align:{'right' if a == 'r' else 'left'}"
                 + (f";width:{widths[i]}" if widths and widths[i] else "") + f"'>{html.escape(h)}</th>" for i, (h, a) in enumerate(zip(headers, aligns)))
    trs = []
    for r in rows:
        if isinstance(r, str):  # a group row
            trs.append(f"<tr><td colspan='{len(headers)}' style='padding:12px 8px 4px;{FONT}font-size:12px;font-weight:bold;color:{GREEN};text-transform:uppercase;letter-spacing:.04em'>{html.escape(r)}</td></tr>")
            continue
        tds = "".join(f"<td align='{'right' if a == 'r' else 'left'}' style='padding:6px 5px;{FONT}font-size:13px;color:{INK};border-bottom:1px solid #f0f0f0;vertical-align:middle;text-align:{'right' if a == 'r' else 'left'}'>{c}</td>"
                      for c, a in zip(r, aligns))
        trs.append(f"<tr>{tds}</tr>")
    return (f"<tr><td style='padding:4px 0 0'><table role='presentation' cellpadding='0' cellspacing='0' border='0' width='100%' style='width:100%;border-collapse:collapse'>"
            f"<tr>{th}</tr>{''.join(trs)}</table></td></tr>")

def _num(n):
    return f"<strong>{n:,}</strong>" if isinstance(n, int) else f"<strong>{n}</strong>"

def week_label(when):
    """'2 – 8 November 2026' for the seven days that end on the run's date (the Sunday-night run covers Monday to Sunday)."""
    a, b = when - dt.timedelta(days=6), when
    if a.year != b.year:
        return f"{a.day} {a.strftime('%B %Y')} – {b.day} {b.strftime('%B %Y')}"
    if a.month != b.month:
        return f"{a.day} {a.strftime('%B')} – {b.day} {b.strftime('%B %Y')}"
    return f"{a.day} – {b.day} {b.strftime('%B %Y')}"

def email_subject(now, week, when):
    return (f"Dancing Atlas · week to {when.day} {when.strftime('%b')} · {now['dances_live']:,} dances ({delta(now['dances_live'], week and week['dances_live'])}) · "
            f"{now['published']} published ({delta(now['published'], week and week['published'])}) · {now['movie_ready']} movie-ready ({delta(now['movie_ready'], week and week['movie_ready'])})")

def render_email_html(now, week, month, start, labels, hist, when):
    date = "Week of " + week_label(when)
    h = health(now["runs"], (when - dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ"))
    R = []  # rows of the 640px content table
    # masthead
    R.append(f"<tr><td style='padding:0 0 4px;{FONT}font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:{GREEN};font-weight:bold'>Dancing Atlas · weekly report</td></tr>")
    R.append(f"<tr><td style='padding:0 0 14px;{FONT}font-size:24px;font-weight:bold;color:{INK}'>{html.escape(date)}</td></tr>")
    R.append(f"<tr><td style='padding:12px 14px;background:{PALE};border-left:4px solid {GREEN};{FONT}font-size:14px;line-height:1.5;color:{INK}'>{_inline(verdict(now, week, h))}</td></tr>")
    # at a glance: four tiles
    tiles = [("Dances live on the site", "dances_live"), ("Deep profiles published", "published"), ("Movie-ready", "movie_ready"), ("Film-grade ★", "film_grade")]
    tds = []
    for lab, k in tiles:
        tds.append(f"<td class='tile' width='25%' valign='top' style='width:25%;padding:14px 10px;background:#fff;border:1px solid {LINE};{FONT}'>"
                   f"<div style='font-size:30px;font-weight:bold;color:{INK};line-height:1.1'>{now[k]:,}</div>"
                   f"<div style='font-size:12px;color:{MUTED};padding:4px 0 6px'>{html.escape(lab)}</div>"
                   f"<div style='font-size:13px;line-height:1.5'>{_chip(now[k], week and week[k])} <span style='color:{MUTED}'>this week</span><br>{_chip(now[k], month and month[k])} <span style='color:{MUTED}'>in 4 weeks</span></div></td>")
    R.append(f"<tr><td style='padding:16px 0 0'><table role='presentation' cellpadding='0' cellspacing='6' border='0' width='100%' style='width:100%;border-collapse:separate'><tr>{''.join(tds)}</tr></table></td></tr>")
    R.append(f"<tr><td style='padding:8px 2px 0;{FONT}font-size:13px;line-height:1.5;color:{MUTED}'>{html.escape(labels['start'])}: {_chip(now['dances_live'], start and start['dances_live'])} dances, "
             f"{_chip(now['published'], start and start['published'])} published profiles, {_chip(now['movie_ready'], start and start['movie_ready'])} movie-ready, {_chip(now['film_grade'], start and start['film_grade'])} film-grade.</td></tr>")
    # 1 the ladder with bars
    R.append(_h2("1 · The ladder — how far the dances have climbed", "Each bar is the share of all dances live that has reached that level. The top of the ladder is meant to be nearly impossible (STANDARD.md)."))
    ladder = [("0 · Listed in the atlas", "dances_live"), ("1 · Deep profile researched from sources", "researched"), ("2 · Published — passed every QC gate and the judge", "published"),
              ("3 · Movie-ready — music DNA, movement DNA, episode brief", "movie_ready"), ("4 · Class-complete — all 18 things a class needs", "class_complete"), ("5 · Film-grade ★ — every line of the standard, editor included", "film_grade")]
    rows = [[html.escape(lab), _bar(now[k], now["dances_live"], width=96), _num(now[k]), _chip(now[k], week and week[k]), _chip(now[k], month and month[k])] for lab, k in ladder]
    R.append(_table(["Level", "", "Dances", "This week", "4 weeks"], rows, ["l", "l", "r", "r", "r"], [None, "96px", None, None, None]))
    # 2 week by week
    if len(hist) >= 2:
        R.append(_h2("2 · Week by week", "One row per Monday. The bar is the number of published profiles, relative to the best week shown. Episode packs, translations and lessons are in section 3."))
        top = max(int(r.get("published", 0) or 0) for r in hist[-8:]) or 1
        def wk(d):
            try:
                return dt.datetime.strptime(d, "%Y-%m-%d").strftime("%d %b")
            except Exception:
                return d
        rows = [[f"<span style='white-space:nowrap'>{html.escape(wk(r['date']))}</span>", f"{int(r.get('dances_live', 0) or 0):,}", _bar(int(r.get("published", 0) or 0), top, width=52), _num(int(r.get("published", 0) or 0)),
                 f"{int(r.get('movie_ready', 0) or 0)}", f"{int(r.get('film_grade', 0) or 0)}"] for r in hist[-8:]]
        R.append(_table(["Week", "Dances", "", "Published", "Movie-ready", "Film-grade"], rows, ["l", "r", "l", "r", "r", "r"], [None, None, "52px", None, None, None]))
    # 3 growth detail
    R.append(_h2("3 · Growth in detail"))
    growth = [("Dances live on the site", "dances_live"), ("…with a hero video", "with_hero"), ("…hero video passed the vision check", "hero_checked"), ("…with tutorial videos", "with_tutorials"),
              ("Deep profiles researched", "researched"), ("Deep profiles published (passed QC)", "published"), ("Movie-ready profiles", "movie_ready"), ("Class-complete profiles", "class_complete"),
              ("Film-grade ★ profiles", "film_grade"), ("Verified claims in published profiles", "claims_verified"), ("Doubles / non-dances retired (total)", "retired"),
              ("Episode packs written (intro + 3 chapters)", "episode_packs"), ("…complete, no gaps", "episode_complete"), ("…narration polished and verified", "episode_polished"),
              ("…translated (pack × language)", "translations"), ("Tutorial lessons studied for the teaching playbook", "lessons_studied")]
    rows = [[html.escape(lab), _num(now[k]), _chip(now[k], week and week[k]), _chip(now[k], month and month[k]), _chip(now[k], start and start[k])] for lab, k in growth]
    R.append(_table(["", "Now", "This week", "4 weeks", labels["start"].replace("Since the start", "Since start")], rows, ["l", "r", "r", "r", "r"]))
    # 4 inside the profiles
    pub = now["published"]
    R.append(_h2(f"4 · Inside the profiles — of the {pub} published, how many have each piece", "Grouped the way a film and a class need them. Pieces marked (info) are not required for film-grade."))
    rows, group = [], None
    for lab, code, grp, req in TOPICS:
        if grp != group:
            group = grp; rows.append(grp)
        n = now["topics"].get(lab, 0)
        short = lab.split(": ", 1)[1] if ": " in lab else lab
        short = short[0].upper() + short[1:] + ("" if req else " (info)")
        rows.append([html.escape(short), _bar(n, pub, width=90), f"<strong>{n}</strong> <span style='color:{MUTED};white-space:nowrap'>({pc(n, pub)})</span>", _chip(n, week["topics"].get(lab) if week else None), _chip(n, month["topics"].get(lab) if month else None)])
    R.append(_table(["Piece", "", "Have it", "This week", "4 weeks"], rows, ["l", "l", "r", "r", "r"], [None, "90px", None, None, None]))
    # 5 filters
    R.append(_h2("5 · The filters — what was kept out", f"Every published profile carries claims with a verbatim quote checked against the fetched source: **{now['claims_verified']:,} of {now['claims']:,} claims verified ({pc(now['claims_verified'], now['claims']) if now['claims'] else '–'})**."))
    filt = [("Profiles judged by QC", "judged"), ("…passed (published)", "gate_publish"), ("…held for review (an editor decides)", "gate_review"), ("…rejected", "gate_reject"),
            ("Doubles merged into another entry", "retired_doubles"), ("Doubles and non-dances retired (total)", "retired"), ("Dance moves screened out before research", "screened_moves"), ("Candidates waiting in the research queue", "candidates_queued")]
    rows = [[html.escape(lab), _num(now[k]), _chip(now[k], week and week[k]), _chip(now[k], month and month[k])] for lab, k in filt]
    R.append(_table(["", "Now", "This week", "4 weeks"], rows, ["l", "r", "r", "r"]))
    # 6 new this week
    if week:
        nm = lambda s: now["names"].get(s) or s.replace("-", " ")
        new_pub = [s for s in now["published_slugs"] if s not in set(week["published_slugs"])]
        new_movie = [s for s in now["movie_slugs"] if s not in set(week["movie_slugs"])]
        if new_pub or new_movie:
            R.append(_h2("6 · New this week"))
            if new_pub:
                R.append(_p("**Published:** " + ", ".join(nm(s) for s in new_pub[:30]) + (f" … and {len(new_pub) - 30} more" if len(new_pub) > 30 else "")))
            if new_movie:
                R.append(_p("**Now movie-ready:** " + ", ".join(nm(s) for s in new_movie[:30]) + (f" … and {len(new_movie) - 30} more" if len(new_movie) > 30 else "")))
    # 7 closest to film-grade
    R.append(_h2("7 · Closest to film-grade ★", ("**Film-grade now:** " + ", ".join(now["names"].get(s) or s for s in now["film_slugs"])) if now["film_slugs"] else "No page is film-grade yet — these are the nearest, with what each still lacks."))
    rows = [[html.escape(name), f"{score}", f"{cls}", html.escape(f"{nmiss}: " + ", ".join(TOPIC_BY_LABEL[x][1] if x in TOPIC_BY_LABEL else x for x in missing))] for nmiss, _, name, slug, missing, score, cls in now["closest"][:8]]
    R.append(_table(["Dance", "Judge", "Checklist", "Still missing"], rows, ["l", "r", "r", "l"]))
    # 8 stuck
    lessons = _j(os.path.join("pipeline_state", "lessons_learned.json"), {}) or {}
    tuning = _j(os.path.join("pipeline_state", "tuning.json"), {}) or {}
    R.append(_h2("8 · Where the machine is stuck — and what would help most", "What the scripts lack most across the published pages, and the one thing that would fix each."))
    hm = lessons.get("help_most") or []
    if hm:
        R.append(_table(["What the scripts lack", "Pages", "What would fix it"], [[html.escape(str(x.get("gap"))), f"<strong>{x.get('pages')}</strong>", html.escape(str(x.get("what_helps")))] for x in hm[:6]], ["l", "r", "l"]))
    if lessons.get("avoid"):
        R.append(_p("The judge's most frequent objections in the last 30 days, now handed to the writer before every page: " + "; ".join(lessons["avoid"][:3]) + ".", size=13, color=MUTED))
    if tuning.get("reason"):
        R.append(_p(f"Self-tuning: {tuning['reason']}." + ((" **Alerts:** " + "; ".join(tuning.get("alerts") or [])) if tuning.get("alerts") else ""), size=13, color=MUTED))
    # 9 the machine
    R.append(_h2("9 · The machine"))
    R.append(_p(f"Daily run fired on **{h['days']} of 7** days · model calls this week **{h['calls']:,}** · errors logged **{h['errors']}** · OpenAI balance {'**spent**' if h['quota'] else 'fine'} · "
                f"{now['schema5']} of {now['researched']} profiles at research schema 5 · teaching playbook built from {now['lessons_studied']} lessons across {now['teachers_dances']} dances.", size=13))
    # footer
    R.append(f"<tr><td style='padding:28px 0 0;border-top:1px solid {LINE};{FONT}font-size:12px;line-height:1.5;color:{MUTED}'>"
             + _inline("**How to read this.** **Published** = passed every QC gate (sources, verified quotes, country, no AI tells, not a double) and a judge score; **movie-ready** = music DNA + movement DNA + an episode brief, all from sources; "
                       "**class-complete** = all 18 things a teachable class needs; **film-grade ★** = every line of STANDARD.md, including an editor's read — the bar is meant to be nearly impossible; **episode packs** = the scene-by-scene scripts (Episode 1 + three chapters) written from the profile only. "
                       f"Changes compare the repository as it was 7 days ago, 28 days ago and at {labels['start_long']}.")
             + f"<br><br>Full report and history: <a href='https://github.com/{REPO}/blob/main/WEEKLY_REPORT.md' style='color:{GREEN}'>WEEKLY_REPORT.md</a> · "
             f"<a href='https://github.com/{REPO}/blob/main/NEXT_STEPS.md' style='color:{GREEN}'>NEXT_STEPS.md</a> · <a href='https://github.com/{REPO}/blob/main/STANDARD.md' style='color:{GREEN}'>STANDARD.md</a> · "
             f"<a href='https://github.com/{REPO}/actions' style='color:{GREEN}'>the machine's runs</a>. Sent by the repository's weekly workflow; nothing to reply to.</td></tr>")
    body = "".join(R)
    return (f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta name='x-apple-disable-message-reformatting'>"
            f"<title>{html.escape(email_subject(now, week, when))}</title>"
            "<style>@media only screen and (max-width:520px){.tile{display:block!important;width:100%!important;box-sizing:border-box}.wrap{padding:10px 6px!important}.pad{padding:18px 14px 16px!important}}</style></head>"
            f"<body style='margin:0;padding:0;background:#efefef'>"
            f"<table role='presentation' cellpadding='0' cellspacing='0' border='0' width='100%' style='width:100%;background:#efefef'><tr><td align='center' class='wrap' style='padding:24px 12px'>"
            "<!--[if mso]><table role='presentation' cellpadding='0' cellspacing='0' border='0' width='640'><tr><td><![endif]-->"
            f"<table role='presentation' cellpadding='0' cellspacing='0' border='0' width='100%' style='width:100%;max-width:640px;background:#ffffff;border-radius:6px'><tr><td class='pad' style='padding:28px 28px 24px'>"
            f"<table role='presentation' cellpadding='0' cellspacing='0' border='0' width='100%' style='width:100%'>{body}</table>"
            "</td></tr></table><!--[if mso]></td></tr></table><![endif]-->"
            "</td></tr></table></body></html>")

# ---------------------------------------------------------------- optional direct e-mail
def _outcome(**kv):
    """Tell the workflow what happened (step outputs `configured` and `sent`), when running in GitHub Actions."""
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            for k, v in kv.items():
                f.write(f"{k}={'true' if v else 'false'}\n")

def send_email(md_path, html_path, attempts=3):
    """Sends the designed report (HTML, with the Markdown as the plain-text part) when the secrets exist:
    REPORT_SMTP_USER + REPORT_SMTP_PASSWORD (a Gmail address and its app password), REPORT_TO (optional, defaults to the
    user), REPORT_SMTP_HOST / REPORT_SMTP_PORT (optional, default Gmail 587 with STARTTLS). Without them it does nothing
    and the workflow posts the report to the GitHub issue thread instead. Transient errors are retried; a wrong password
    is not. A failed send exits non-zero so the run is red and visible. Addresses and passwords are never printed."""
    import time
    user, pw = (os.environ.get("REPORT_SMTP_USER") or "").strip(), (os.environ.get("REPORT_SMTP_PASSWORD") or "").strip()
    to = (os.environ.get("REPORT_TO") or user).strip()
    pw = pw.replace(" ", "")  # Google shows app passwords in groups of four; the spaces are not part of it
    if not (user and pw and to):
        _outcome(configured=False, sent=False)
        print("[weekly_report] the e-mail secrets are not set (REPORT_SMTP_USER, REPORT_SMTP_PASSWORD); the GitHub issue thread delivers this week", file=sys.stderr)
        return False
    import smtplib
    from email.message import EmailMessage
    from email.utils import formataddr, make_msgid, formatdate
    md = open(md_path, encoding="utf-8").read()
    htm = open(html_path, encoding="utf-8").read()
    m = re.search(r"<title>(.*?)</title>", htm, re.S)
    subject = html.unescape(m.group(1)) if m else "Dancing Atlas — weekly report"
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, formataddr(("Dancing Atlas", user)), to
    msg["Date"], msg["Message-ID"] = formatdate(localtime=False), make_msgid(domain=user.split("@")[-1] if "@" in user else None)
    msg.set_content(md)
    msg.add_alternative(htm, subtype="html")
    host = (os.environ.get("REPORT_SMTP_HOST") or "").strip() or "smtp.gmail.com"   # an unset secret arrives as an empty string
    port = int((os.environ.get("REPORT_SMTP_PORT") or "").strip() or "587")
    last = None
    for i in range(attempts):
        try:
            if port == 465:
                with smtplib.SMTP_SSL(host, port, timeout=60) as smtp:
                    smtp.login(user, pw); smtp.send_message(msg)
            else:
                with smtplib.SMTP(host, port, timeout=60) as smtp:
                    smtp.starttls(); smtp.login(user, pw); smtp.send_message(msg)
            _outcome(configured=True, sent=True)
            print(f"[weekly_report] e-mailed the designed report (attempt {i + 1}) via {host}", file=sys.stderr)
            return True
        except smtplib.SMTPAuthenticationError as e:
            last = e
            print(f"[weekly_report] e-mail FAILED: the mail server refused the login ({e.smtp_code}). For Gmail this means the app password in "
                  f"REPORT_SMTP_PASSWORD is wrong or was revoked, or REPORT_SMTP_USER is not the Gmail it belongs to.", file=sys.stderr)
            break
        except Exception as e:
            last = e
            print(f"[weekly_report] e-mail attempt {i + 1} failed via {host}:{port} — {type(e).__name__}: {str(e)[:160]}", file=sys.stderr)
            if i + 1 < attempts:
                time.sleep(30 * (i + 1))
    _outcome(configured=True, sent=False)
    print(f"[weekly_report] e-mail FAILED after {attempts if not isinstance(last, smtplib.SMTPAuthenticationError) else 1} attempt(s); the GitHub issue thread delivers this week", file=sys.stderr)
    sys.exit(1)

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
    page = render_email_html(now, week, month, start, labels, hist, when)
    with open(stem + ".html", "w", encoding="utf-8") as f:
        f.write(page)
    with open(os.path.join("reports", "weekly", "latest.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print(md)
    print(f"[weekly_report] wrote WEEKLY_REPORT.md, {stem}.md/.html; compared with week={r_week and r_week[:7]} month={r_month and r_month[:7]} start={r_start[:7]}", file=sys.stderr)

if __name__ == "__main__":
    main(sys.argv[1:])

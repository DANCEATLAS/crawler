"""The owner's weekly report: how the library grew, how deep each published profile is, what the filters kept out,
whether the machine ran — this week, the last four weeks, and since the start. Deterministic: no model calls.

Comparisons use the repository's own history (every daily run is a commit): the same measurement is taken on the
tree as it was 7 days ago, 28 days ago and at the start of the year (or the first commit), with `git archive`.

Writes  WEEKLY_REPORT.md (latest), NEXT_STEPS.md, reports/weekly/<date>.md (+ .html = the e-mail), pipeline_state/weekly_history.json.
E-mail: `--send` mails reports/weekly/latest.html (table layout, inline styles) when the SMTP secrets exist — see send_email().
Run:    python -m pipeline.weekly_report            # in the repo root, needs full git history (fetch-depth: 0)
        python -m pipeline.weekly_report --root DIR # measure one tree only (used internally; no git)
The email is a plain-language whole-vision digest; reports/weekly/details.md holds the deeper measures. Counts are not release approval.
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
    all_epi = epi_idx.get("packs") or {}
    ped = _j(P("pedagogy", "teaching_patterns.json"), {}) or {}
    live = {s for s in styles if s not in retired}
    # QC history can retain removed/merged entries. Report the catalogue actually offered.
    epi = {s: v for s, v in all_epi.items() if s in live and (qidx.get(s) or {}).get("publish_gate") == "publish"}
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
         "translations": 0, "languages": 0, "translations_current": 0, "translations_reviewed": 0,
         "languages_configured": len(epi_idx.get("languages") or []),
         "episode_stored": len(all_epi), "episode_withheld": sum(v.get("status") == "withheld-chapters" for v in epi.values()),
         "catalogue_at": cat.get("generated_at"),
         "vision": _j(P("pipeline_state", "vision_status.json"), {}) or {},
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
        if s not in live or (qidx.get(s) or {}).get("publish_gate") != "publish":
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
    langs = set()
    for path in glob.glob(P("episodes", "i18n", "*", "*.json")):
        tr = _j(path, {}) or {}
        slug = tr.get("slug")
        if slug not in epi:
            continue
        m["translations"] += 1
        langs.add(tr.get("lang") or os.path.basename(os.path.dirname(path)))
        current = bool(tr.get("master_built_at")) and tr["master_built_at"] == epi[slug].get("built_at") and bool(tr.get("master_polished")) == bool(epi[slug].get("polished"))
        if current:
            m["translations_current"] += 1
            if tr.get("reviewed_by_native_speaker") is True and not tr.get("scenes_master_kept"):
                m["translations_reviewed"] += 1
    m["languages"] = len(langs)
    viral = _j(P("viral_challenges_verified.json"), None)
    m["viral_entries"] = len({v.get("slug") for v in viral if isinstance(v, dict) and v.get("slug")}) if isinstance(viral, list) else None
    # This is a seed-library count, not a fresh observation of the database or chart.
    status = open(P("STATUS.md"), encoding="utf-8").read() if os.path.isfile(P("STATUS.md")) else ""
    stamp = re.search(r"Generated (\d{4}-\d\d-\d\dT[0-9:]+Z)", status)
    db = re.search(r"Dances: \*\*(\d+)\*\*", status)
    m["database_at"] = stamp.group(1) if stamp and db else None
    m["database_dances"] = int(db.group(1)) if stamp and db else None
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

def health(runs, since, until=None):
    days, errors, calls, quota, retries, unanswered = set(), 0, 0, False, 0, 0
    for r in runs:
        finished = r.get("finished") or ""
        if finished < since or (until and finished > until):
            continue
        if r.get("stage") == "report":
            days.add((r.get("finished") or "")[:10])
        errors += len(r.get("errors") or [])
        calls += int((r.get("counters") or {}).get("llm_calls") or 0)
        retries += int((r.get("counters") or {}).get("llm_failures") or 0)
        unanswered += int((r.get("counters") or {}).get("llm_unanswered") or 0)
        if any("insufficient_quota" in str(e) for e in (r.get("errors") or [])):
            quota = True
    return {"days": len(days), "errors": errors, "calls": calls, "quota": quota, "retries": retries, "unanswered": unanswered}

def verdict(now, week, h):
    return (f"The logs record completed daily reports on {h['days']} dates in the last seven days, "
            f"{h['errors']} recorded errors and {h['unanswered']} unanswered model requests. "
            "These logs do not establish Viral chart health, account balances or release readiness.")

def render_detail_md(now, week, month, start, labels, hist, when):
    """Optional depth; the owner email and fallback remain the short digest."""
    lines = [f"# Dance Atlas — progress evidence · {when:%d %b %Y}", "",
             "[Simple weekly overview](../../WEEKLY_REPORT.md) · [Editorial decisions](../../EDITORIAL_LOG.md) · [Full vision](../../PRODUCT_VISION.md)", "",
             f"Catalogue exported: {now.get('catalogue_at') or 'not recorded'}. Counts come from saved repository data; website rendering is not re-tested by this report.", "",
             "## Growth and preparation", "", "| Measure | Now | 7-day change | 28-day change |", "| --- | ---: | ---: | ---: |"]
    measures = [("Atlas entries", "dances_live"), ("Published deep profiles in the Atlas", "published"),
                ("Researched profiles, including unpublished", "researched"), ("Dances with tutorial references", "with_tutorials"),
                ("Dances with a hero video", "with_hero"), ("Hero videos with automated pass", "hero_checked"),
                ("Profiles with script ingredients", "movie_ready"), ("Profiles passing structural class checks", "class_complete"),
                ("Script packs for published Atlas profiles", "episode_packs"), ("Packs without recorded content gaps", "episode_complete"),
                ("Packs with teaching chapters withheld", "episode_withheld"), ("Tutorials studied for teaching methods", "lessons_studied"),
                ("Translation files for these packs", "translations"), ("Translations matching current master", "translations_current"),
                ("Current complete translations with native review recorded", "translations_reviewed"),
                ("Languages with translation files", "languages"), ("Viral entries in saved seed collection", "viral_entries"),
                ("Source-quote matches in published profiles", "claims_verified"), ("Retired/merged catalogue entries", "retired")]
    for label, key in measures:
        value = now.get(key)
        lines.append(f"| {label} | {value if value is not None else 'Unknown'} | {delta(value, week.get(key)) if value is not None and week else '—'} | {delta(value, month.get(key)) if value is not None and month else '—'} |")
    lines += ["", "Historical trees are measured again using the same definitions. Changes are net counts, not the number of individual edits. A dash means comparison unavailable, not zero.", "",
              f"Stored script index: {now['episode_stored']} packs, of which {now['episode_packs']} correspond to currently published Atlas profiles. Historical/removed entries do not count as current growth.", "",
              f"Configured translation targets: {now['languages_configured']}; actual languages with files: {now['languages']}. A configuration is not completed translation. Old master versions and untranslated scenes prevent a current-complete claim.", "",
              "**Readiness definitions:** publication means the automated editorial gate passed and the profile is present in the Atlas export. Script ingredients, populated fields, quote matches and model scores do not establish factual truth, practitioner review, musical rights or release approval. A script without structural gaps still needs the product release gates. Legacy movie-ready/film-grade fields are internal content checks only.", "",
              "## Every content check", "", "These are structural signals on published profiles. They are not proof of teaching quality or cultural authenticity. Older three-level/count templates are not a universal rule for dance.", "",
              "| Content signal | Profiles |", "| --- | ---: |"]
    lines += [f"| {lab} | {now['topics'].get(lab, 0)} / {now['published']} |" for lab, *_ in TOPICS]
    lines += ["", "## Evidence behind the whole-vision overview", "",
              "Capability descriptions come from [the dated register](../../pipeline_state/vision_status.json), reviewed against the [implementation ledger](../../IMPLEMENTATION_LEDGER.md). After 30 days they display as needing recheck. A missing record never implies success.", "",
              "| Vision area | Requirement IDs | Next work |", "| --- | --- | --- |"]
    for area in (now.get('vision') or {}).get('areas') or []:
        lines.append(f"| {area['title']} | {', '.join(area.get('vision_ids') or [])} | {area.get('next', '')} |")
    lines += ["", "## Reliability and cost evidence", "",
              "Run logs cover the content pipeline, not every crawler/scorer, website, database policy or delivery result. Inspect internal steps in Actions; a green parent can hide ignored failures. Failed model attempts can be recovered by retries/fallbacks. No invoice, current account balance or exact monetary saving is inferred from call counts.", "",
              "| Stage | Latest recorded completion | Errors | Unanswered requests |", "| --- | --- | ---: | ---: |"]
    last = {}
    cutoff = when.strftime('%Y-%m-%dT%H:%M:%SZ')
    for r in now.get('runs') or []:
        if r.get('finished', '') <= cutoff and r.get('finished', '') > last.get(r.get('stage'), {}).get('finished', ''):
            last[r.get('stage')] = r
    for stage, r in sorted(last.items()):
        lines.append(f"| {stage} | {r.get('finished')} | {len(r.get('errors') or [])} | {(r.get('counters') or {}).get('llm_unanswered', 0)} |")
    lines += ["", "[Run history](https://github.com/DANCEATLAS/crawler/actions) · [Database and platform limits](../../IMPLEMENTATION_LEDGER.md) · [Next work](../../NEXT_STEPS.md)", ""]
    return "\n".join(lines)


def next_steps(now, lessons_path, when):
    from .progress_digest import owner_action, priorities
    lessons = _j(lessons_path, {}) or {}
    action = owner_action(now, when)
    lines = [f"# Next work — {when:%Y-%m-%d}", "", "Read PRODUCT_VISION.md, AI_BRIEF.md, IMPLEMENTATION_LEDGER.md and NEXT_RUN_PLAN.md first. Continue independently within existing limits.", "",
             "## Current priorities", ""] + ["- " + x for x in priorities(now, when)]
    lines += ["", "## Specific research gaps", ""]
    for gap in (lessons.get('help_most') or [])[:5]:
        lines.append(f"- {gap.get('gap')}: {gap.get('pages')} pages — {gap.get('what_helps')}.")
    lines += ["", "## Owner-only action", "", action['title'] + ". " + action['reason'], "",
              "Do not ask the owner to select production vendors, buy credits or copy files when independent preparation can continue. Present only one necessary action, in large plain language.", "",
              "## Keep the whole vision current", "",
              "- Update pipeline_state/vision_status.json after verified capability/access changes, with date and evidence in the ledger. Resolve an owner action promptly; do not leave an old sign-in request active.",
              "- Preserve BDF, Viral creation/distribution, multilingual teaching, life stages, community, music rights and future AR in every review. Specified is not implemented; generated is not validated.",
              "- Reconcile Atlas export, database mirror and script indexes; check scorer/crawler internal outcomes and stale translations.",
              "- Use free/prepaid limits and capped jobs; no new purchases, higher budgets, Lovable build or launch without authorization.", ""]
    return "\n".join(lines)


def render_md(now, week, month, start, labels, hist, when):
    from .progress_digest import render_md as digest
    h = health(now['runs'], (when - dt.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ'), when.strftime('%Y-%m-%dT%H:%M:%SZ'))
    return digest(now, week, month, start, labels, hist, when, h)


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
    from .progress_digest import subject
    return subject(now, week, when)


def render_email_html(now, week, month, start, labels, hist, when):
    from .progress_digest import render_html
    h = health(now['runs'], (when - dt.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ'), when.strftime('%Y-%m-%dT%H:%M:%SZ'))
    return render_html(now, week, month, start, labels, hist, when, h)


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
    row = {"date": when.strftime("%Y-%m-%d"), **{k: now[k] for k in keys}, "rev": now["rev"], "metric_version": 2}
    hist = [h for h in hist if h.get("date") != row["date"]] + [row]
    os.makedirs("pipeline_state", exist_ok=True); os.makedirs(os.path.join("reports", "weekly"), exist_ok=True)
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=1)
    md = render_md(now, week, month, start, labels, hist, when)
    with open("WEEKLY_REPORT.md", "w", encoding="utf-8") as f:
        f.write(md)
    detail = render_detail_md(now, week, month, start, labels, hist, when)
    with open(os.path.join("reports", "weekly", "details.md"), "w", encoding="utf-8") as f:
        f.write(detail)
    with open(os.path.join("reports", "weekly", when.strftime("%Y-%m-%d") + "-details.md"), "w", encoding="utf-8") as f:
        f.write(detail)
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

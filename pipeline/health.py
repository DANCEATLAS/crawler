"""The machine adjusts itself (AI_BRIEF.md §5, "Adaptive loops").

Runs first in every daily run and writes two small files the other stages read:

pipeline_state/tuning.json — budgets scaled to what the models could deliver recently. When more than 40 % of the
  questions asked of the models went unanswered over the last runs (every model failed: quota, 503s), the model-hungry
  budgets drop to 60 %; when unanswered questions stay under 10 % for three runs they climb back by 20 % a run, never
  above the workflow's defaults. A fallback that succeeded is not a failure: only questions nobody answered count.
  The machine never spends more than the owner set; it only spends less when spending would fail. `alerts` carries
  what needs a human (OpenAI balance gone).

pipeline_state/lessons_learned.json — what the QC judge keeps objecting to (soft-fail gates and the judge's recurring
  notes over the last 30 days). pipeline/research.py hands the top faults to the composer as "recent faults to avoid",
  so the writer adapts to the judge instead of repeating the same mistake. Also: the gaps the episode packs report most,
  the dances the crawlers keep failing on — the weekly report turns these into "where the machine is stuck".
"""
import os, re, json, glob, datetime as dt
from collections import Counter
from .common import jload, jsave, load_state, save_state, log, Report, now_iso
from .qc import QC_DIR

FLOOR, STEP_UP, DROP = 0.6, 0.2, 0.6
FAIL_HIGH, FAIL_LOW = 0.40, 0.10
# what each QC gate failure means for the writer, in the writer's terms
GATE_ADVICE = {"insight_concrete": "the insight line was vague — put a person, a place, a year or a number in it",
               "citations": "too few claims had an exact quote from a source — give 6 or more claims, each with its verbatim quote",
               "sections_filled": "fewer than four sections had real content — fill every section the sources allow; say 'not described in sources' only when they truly do not",
               "profile_long_len": "profile_long was too short — 600 to 1200 words of continuous prose from the sections",
               "banned_phrasing": "banned phrasing slipped in — no hype, no 'the sources say', no AI talk",
               "ai_tells": "first-person AI phrasing — never write as an assistant",
               "no_repetition": "paragraphs were repeated — every paragraph says something new",
               "tagline_len": "tagline length wrong — 10 to 110 characters", "insight_len": "insight length wrong — 40 to 260 characters",
               "profile_len": "profile too short — 3 to 5 full sentences", "sacred_handled": "a sacred dance had no sacred_note — add one",
               "sources": "too few sources — every claim must point to a fetched source"}
# what a script gap or a crawler failure needs, for the weekly report's "what would help most"
GAP_ADVICE = {"tempo (bpm)": "a source that states the tempo — a teacher's page or a music reference, added via pipeline_state/sources_extra.json",
              "meter": "a source that states the time signature", "instruments": "a source that names the instruments",
              "a verified recording to listen to": "a recording title the composer can verify in MusicBrainz (an album or single named in a source)",
              "a hero video": "the crawler found no usable video — a different search phrase or a channel to trust, via an editor note",
              "the hero video's vision check": "the vision model has not reached it yet — it will (60 a day)",
              "licensed images (3 needed)": "a Wikimedia Commons category or file link in an editor note",
              "licensed reference footage": "a Commons video or an Internet Archive film naming the dance in its title",
              "posture, arms and hands": "a teaching source that describes the body (a teacher's page or a tutorial studied by the pedagogy stage)",
              "signature moves": "a source that names the characteristic moves", "teaching steps written out": "a teaching source with the basic steps",
              "what to avoid / common mistakes": "a teaching source or a studied tutorial that names mistakes", "two or more connections": "sources that relate the dance to its relatives"}

STAGES = ("research", "qc", "hero_qc", "pedagogy", "episodes", "translate")

def _runs_by_day(runs, stage, n):
    out = []
    for r in reversed(runs):
        if r.get("stage") == stage and (r.get("counters") or {}).get("llm_calls") is not None:
            out.append(r)
        if len(out) >= n:
            break
    return out

def _asked_unanswered(r):
    """(questions, unanswered) for a run record; older records only know attempts, and count a failed attempt as unanswered."""
    c = r.get("counters") or {}
    if c.get("llm_requests") is not None:
        return int(c.get("llm_requests") or 0), int(c.get("llm_unanswered") or 0)
    return int(c.get("llm_calls") or 0), int(c.get("llm_failures") or 0)

def tune():
    runs = load_state("runs.json", []) or []
    prev = load_state("tuning.json", {}) or {}
    scale = float(prev.get("scale") or 1.0)
    # unanswered rate over the last two runs of every model-using stage
    recent = [r for st in STAGES for r in _runs_by_day(runs, st, 2)]
    pairs = [_asked_unanswered(r) for r in recent]
    calls = sum(a for a, _ in pairs)
    fails = sum(u for _, u in pairs)
    rate = (fails / calls) if calls else 0.0
    streak = int(prev.get("good_streak") or 0)
    reason = ""
    if calls and rate >= FAIL_HIGH:
        new = max(FLOOR, round(scale * DROP, 2)); streak = 0
        reason = f"{fails} of {calls} questions went unanswered by every model in the last runs ({rate:.0%}): budgets scaled to {new:.0%}"
    elif calls and rate <= FAIL_LOW:
        streak += 1
        new = min(1.0, round(scale + STEP_UP, 2)) if streak >= 3 and scale < 1.0 else scale
        reason = (f"models healthy for {streak} run(s): budgets back to {new:.0%}" if new != scale else f"models healthy ({fails} of {calls} questions unanswered); budgets at {scale:.0%}")
    else:
        new = scale
        reason = f"{fails} of {calls} questions unanswered ({rate:.0%}); budgets stay at {scale:.0%}"
    alerts = []
    for r in runs[-40:]:
        for e in (r.get("errors") or []) + (r.get("notes") or []):
            if "insufficient_quota" in str(e):
                alerts.append("OpenAI balance is spent (insufficient_quota): research continues on Gemini alone; a top-up is the owner's call")
                break
    out = {"updated_at": now_iso(), "scale": new, "good_streak": streak, "failure_rate": round(rate, 3), "calls_considered": calls, "reason": reason,
           "applies_to": ["RESEARCH_NEW", "RESEARCH_ENRICH", "HERO_QC_BUDGET", "PEDAGOGY_BUDGET", "EPISODE_POLISH", "TRANSLATE_BUDGET"], "alerts": sorted(set(alerts))}
    save_state("tuning.json", out)
    return out

def scaled(name, default):
    """Budget for this run: the workflow's value scaled by tuning.json (never above it)."""
    try:
        base = int(os.environ.get(name, default))
    except Exception:
        base = default
    t = load_state("tuning.json", {}) or {}
    s = float(t.get("scale") or 1.0)
    if name not in (t.get("applies_to") or []):
        return base
    return max(1, int(round(base * min(1.0, s)))) if base > 0 else 0

def lessons():
    """What the judge objects to most, from the last 30 days of QC records."""
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    gates, notes, reasons = Counter(), Counter(), Counter()
    n = 0
    for f in glob.glob(os.path.join(QC_DIR, "*.json")):
        q = jload(f, None)
        if not q or (q.get("qc_at") or "") < since:
            continue
        n += 1
        for g in q.get("gates") or []:
            if not g.get("ok"):
                gates[g.get("gate")] += 1
        for r in q.get("reasons") or []:
            if not str(r).startswith("judge_score"):
                reasons[str(r)] += 1
        jd = q.get("judge") or {}
        for d in (jd.get("factual_doubt") or [])[:3]:
            if isinstance(d, str) and len(d) > 12:
                notes["doubt: " + d[:120]] += 1
        note = jd.get("notes")
        if isinstance(note, str):
            for kw in ("vague", "generic", "repetit", "placeholder", "unsupported", "thin", "promotional", "stereotyp", "inaccura", "missing"):
                if kw in note.lower():
                    notes[f"judge notes mention '{kw}'"] += 1
    epi_gaps = load_state("episode_gaps.json", {}) or {}
    gap_counts = Counter(g for v in epi_gaps.values() for g in v if isinstance(g, str))
    out = {"updated_at": now_iso(), "qc_records_considered": n,
           "gate_failures": gates.most_common(10), "reasons": reasons.most_common(10), "judge_notes": notes.most_common(10),
           "episode_gaps_top": gap_counts.most_common(12),
           "avoid": [f"{GATE_ADVICE.get(g, g)} ({c} pages in 30 days)" for g, c in gates.most_common(6) if g not in ("not_duplicate", "country", "region")][:5],
           "help_most": [{"gap": g, "pages": c, "what_helps": GAP_ADVICE.get(g, "a source that covers it, via sources_extra.json")} for g, c in gap_counts.most_common(6)]}
    save_state("lessons_learned.json", out)
    return out

def run():
    rep = Report("health")
    t = tune()
    rep.note("tuning: " + t["reason"])
    for a in t["alerts"]:
        rep.note("ALERT " + a)
    l = lessons()
    rep.note(f"lessons: {l['qc_records_considered']} QC records in 30 days; top gate failures {l['gate_failures'][:3]}; top script gaps {l['episode_gaps_top'][:3]}")
    rep.inc("scale_pct", int(round(t["scale"] * 100)))
    return rep.finish()

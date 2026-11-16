"""Active-ready: the starting line. Offline, no model calls, runs every day.

The owner's definition (16 November 2026): a profile is ACTIVE-READY when the machine has gathered and checked
everything an AI teaching service needs to turn it into a lesson document for that dance — the story, how it is
danced, how it sounds, how it is taught, and video to learn from — so the profile can become active the day such a
service is chosen. The goal is many thousands of them.

It is deliberately not "activated". The human reviews, music rights and platform tests of ACTIVE_PROFILE_STANDARD.md
come after this line, per pilot, when the owner decides. Evidence classes stay apart so an observation is never
mistaken for a verified fact:
  text         written from fetched sources, every claim quote-checked (research + QC)
  lesson       seen and heard in a tutorial the machine studied (pedagogy/videos)
  performance  seen in the dance's own hero video (pedagogy/performances); never enough for counts
Sacred or restricted dances are never taught: they are counted apart as story-ready.

Writes pipeline_state/active_ready.json (every profile, what it still lacks: research, the video stages and the
weekly report read it), public/catalog/active_ready.json (the list), pipeline_state/active_ready_history.json
(one line a day) and ACTIVE_READY.md (the page a person reads).
"""
import datetime as dt
import glob
import json
import os
from collections import Counter
from .research import _said, _said_not, has_count_sequence

STANDARD = "AR-1"
ITEMS = (("published", "passed every quality gate and the independent judge"),
         ("story", "origins, meaning and occasions, dress and setting — written from sources"),
         ("status", "known to be living, revived or historical"),
         ("footwork_counts", "the steps with their counts"),
         ("posture", "posture"),
         ("arms", "arms and hands"),
         ("formation", "formation and use of space"),
         ("signature_moves", "two or more signature moves"),
         ("rhythm", "tempo, meter or the teacher's count"),
         ("sound", "the instruments and what the music sounds like"),
         ("lesson_plan", "ordered basic steps or a lesson ladder"),
         ("mistakes", "what to avoid: common mistakes or safety"),
         ("hero_video", "a hero video that passed the vision check"),
         ("study_video", "a lesson or performance the machine studied, with timestamps"),
         ("picture", "a licensed picture or licensed footage"))
LABEL = dict(ITEMS)
TEACHING = ("footwork_counts", "posture", "arms", "formation", "signature_moves", "lesson_plan", "mistakes", "study_video")
STORY = ("published", "story", "status", "sound", "hero_video", "picture")


def _load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _by_slug(folder):
    out = {}
    for f in glob.glob(os.path.join(folder, "*.json")):
        r = _load(f, {})
        if isinstance(r, dict) and r.get("status") == "ok" and r.get("slug"):
            out.setdefault(r["slug"], []).append(r)
    return out


def evaluate(style, rec, qc, lessons=(), shows=()):
    """One profile against the line. Returns {have, missing, via, state}; via says which evidence class filled an item
    when it was not the text ('lesson' or 'performance')."""
    rec, qc, style = rec or {}, qc or {}, style or {}
    p = rec.get("profile") or {}
    secs, teach = p.get("sections") or {}, p.get("teaching") or {}
    mp, mv, eb = p.get("music_profile") or {}, p.get("movement_profile") or {}, p.get("episode_brief") or {}
    L = [(x.get("extraction") or {}) for x in lessons]
    S = [(x.get("observation") or {}) for x in shows]
    got, via = {}, {}

    def put(item, text, lesson=False, performance=False):
        got[item] = bool(text or lesson or performance)
        if not text and (lesson or performance):
            via[item] = "lesson" if lesson else "performance"

    put("published", rec.get("status") == "researched" and qc.get("publish_gate") == "publish")
    put("story", _said(secs.get("origins_and_history")) and _said(secs.get("occasions_and_meaning"))
        and (_said(secs.get("costume_and_setting")) or any(_said(s.get("costume_and_props")) for s in S)))
    put("status", p.get("tradition_status") in ("living", "revived", "historical"))
    steps = [str(s) for s in (teach.get("basic_steps") or []) if len(str(s).strip()) >= 12 and not _said_not(str(s))]
    put("footwork_counts", (_said(mv.get("footwork")) and has_count_sequence(mv.get("footwork"))) or has_count_sequence(" ".join(steps)),
        lesson=any(len([s for s in (x.get("steps_taught") or []) if s.get("counts")]) >= 2 for x in L))
    put("posture", _said(mv.get("posture")), performance=any(_said(s.get("posture")) for s in S))
    put("arms", _said(mv.get("arms_and_hands")), performance=any(_said(s.get("arms_and_hands")) for s in S))
    put("formation", _said(mv.get("formation_and_space")) or _said(teach.get("formation")), performance=any(_said(s.get("formation_and_space")) for s in S))
    put("signature_moves", len(mv.get("signature_moves") or []) >= 2,
        lesson=any(len(x.get("steps_taught") or []) >= 2 for x in L), performance=any(len(s.get("signature_moments") or []) >= 2 for s in S))
    put("rhythm", (not _said_not(mp.get("tempo_bpm"))) or (not _said_not(mp.get("meter"))),
        lesson=any(x.get("counting_scheme") for x in L), performance=any((s.get("music_heard") or {}).get("meter_feel") for s in S))
    heard = any((s.get("music_heard") or {}).get("instruments") for s in S)
    put("sound", bool(mp.get("instruments")) and (_said(mp.get("sound_description")) or _said(mp.get("rhythm_pattern"))),
        performance=(bool(mp.get("instruments")) or heard) and (_said(mp.get("sound_description")) or _said(mp.get("rhythm_pattern")) or heard))
    put("lesson_plan", len(steps) >= 3 or len(eb.get("lesson_ladder") or []) >= 3,
        lesson=any(len(x.get("lesson_structure") or []) >= 3 and len(x.get("steps_taught") or []) >= 2 for x in L))
    put("mistakes", _said(mv.get("what_to_avoid")), lesson=any((x.get("common_mistakes") or x.get("safety")) for x in L))
    put("hero_video", (style.get("hero_qc") or {}).get("verdict") == "pass")
    put("study_video", False, lesson=bool(L), performance=bool(S))
    put("picture", bool(rec.get("images") or rec.get("footage") or style.get("images")))
    # Teaching is withheld when the writer, reading the sources, called the dance sacred or restricted, or the original
    # catalogue marked it so. A bare keyword hit ("ceremony" in a page about court ballet) is not a restriction: it is
    # recorded as ritual_context so the lesson carries the cultural note and a reviewer looks first.
    sacred = bool(p.get("is_sacred") or (style.get("_is_sacred") and style.get("origin") != "pipeline"))
    ritual = bool(rec.get("sacred_cue_flag")) and not sacred
    need = STORY if sacred else tuple(k for k, _ in ITEMS)
    missing = [k for k in need if not got.get(k)]
    if not got["published"]:
        state = "not_published"
    elif sacred:
        state = "story_ready_teaching_withheld" if not missing else "teaching_withheld"
    else:
        state = "active_ready" if not missing else "building"
    out = {"have": len(need) - len(missing), "of": len(need), "missing": missing, "via": via, "state": state}
    if ritual:
        out["ritual_context"] = True
    return out


def run(root=".", today=None):
    P = lambda *a: os.path.join(root, *a)
    today = today or dt.date.today()
    styles = (_load(P("public", "catalog", "dances.app.json"), {}) or {}).get("styles") or {}
    retired = {x.get("slug") for x in (_load(P("public", "catalog", "retired.json"), {}) or {}).get("retired", []) if isinstance(x, dict)}
    qidx = _load(P("pipeline_state", "qc_index.json"), {}) or {}
    ridx = _load(P("pipeline_state", "research_index.json"), {}) or {}
    lessons, shows = _by_slug(P("pedagogy", "videos")), _by_slug(P("pedagogy", "performances"))
    profiles, names = {}, {}
    for slug in sorted(styles):
        if slug in retired:
            continue
        names[slug] = styles[slug].get("name") or slug
        if (ridx.get(slug) or {}).get("status") != "researched":
            continue
        rec = _load(P("research_results", slug + ".json"), {})
        profiles[slug] = evaluate(styles[slug], rec, qidx.get(slug), lessons.get(slug, ()), shows.get(slug, ()))
    listed = len(names)
    states = Counter(v["state"] for v in profiles.values())
    teachable = {s: v for s, v in profiles.items() if v["state"] in ("active_ready", "building")}
    short = Counter(len(v["missing"]) for v in teachable.values())
    blockers = Counter(k for v in teachable.values() for k in v["missing"])
    ready = sorted(s for s, v in profiles.items() if v["state"] == "active_ready")
    story = sorted(s for s, v in profiles.items() if v["state"] == "story_ready_teaching_withheld")
    counts = {"listed": listed, "researched": len(profiles), "published": sum(1 for v in profiles.values() if v["state"] != "not_published"),
              "active_ready": len(ready), "one_short": short.get(1, 0), "two_short": short.get(2, 0), "three_to_five_short": sum(short.get(i, 0) for i in (3, 4, 5)),
              "story_ready_teaching_withheld": len(story), "lessons_studied": sum(len(v) for v in lessons.values()), "performances_observed": sum(len(v) for v in shows.values())}
    os.makedirs(P("pipeline_state"), exist_ok=True)
    os.makedirs(P("public", "catalog"), exist_ok=True)
    def save(path, obj):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
            f.write("\n")
    save(P("pipeline_state", "active_ready.json"), {"standard": STANDARD, "evaluated_on": today.isoformat(), "items": [k for k, _ in ITEMS], "counts": counts, "profiles": profiles})
    save(P("public", "catalog", "active_ready.json"), {"contract": "da_active_ready_v1", "standard": STANDARD, "evaluated_on": today.isoformat(), "counts": counts,
                                                       "active_ready": ready, "story_ready_teaching_withheld": story,
                                                       "note": "Machine-complete and source-checked; not human-reviewed, rights-cleared or platform-tested. See ACTIVE_READY.md."})
    hist = [h for h in (_load(P("pipeline_state", "active_ready_history.json"), []) or []) if isinstance(h, dict) and h.get("date") != today.isoformat()]
    hist.append(dict(counts, date=today.isoformat()))
    hist = sorted(hist, key=lambda h: h["date"])[-800:]
    save(P("pipeline_state", "active_ready_history.json"), hist)
    with open(P("ACTIVE_READY.md"), "w", encoding="utf-8") as f:
        f.write(render(counts, short, blockers, teachable, names, hist, today))
    return {"counters": dict(counts)}


def pace(hist, key, days=14):
    """Change a day over the last `days` days of history (None when the history is shorter than a week)."""
    if len(hist) < 2:
        return None
    last = hist[-1]
    first = next((h for h in hist if h["date"] >= (dt.date.fromisoformat(last["date"]) - dt.timedelta(days=days)).isoformat()), hist[0])
    span = (dt.date.fromisoformat(last["date"]) - dt.date.fromisoformat(first["date"])).days
    return None if span < 7 else (last.get(key, 0) - first.get(key, 0)) / span


def render(counts, short, blockers, teachable, names, hist, today):
    L = ["# Active-ready — the starting line", "",
         f"_Measured {today.isoformat()} by `pipeline/readiness.py` (standard {STANDARD}); no model calls. The goal: many thousands._", "",
         f"## {counts['active_ready']:,} profile{' is' if counts['active_ready'] == 1 else 's are'} active-ready", "",
         "Active-ready means the machine has gathered and source-checked everything an AI teaching service needs to write the lesson for that dance. "
         "It is not human-reviewed, rights-cleared or platform-tested: that comes after this line (ACTIVE_PROFILE_STANDARD.md).", "",
         "| Step | Profiles |", "|---|---:|",
         f"| In the atlas | {counts['listed']:,} |", f"| Researched from sources (in the atlas) | {counts['researched']:,} |", f"| Published (passed every gate) | {counts['published']:,} |",
         f"| **Active-ready** | **{counts['active_ready']:,}** |", f"| One item short | {counts['one_short']:,} |", f"| Two items short | {counts['two_short']:,} |",
         f"| Three to five short | {counts['three_to_five_short']:,} |", f"| Story-ready, teaching withheld (sacred or restricted) | {counts['story_ready_teaching_withheld']:,} |", "",
         f"Video studied so far: {counts['lessons_studied']:,} lessons, {counts['performances_observed']:,} performances.", ""]
    for key, label in (("active_ready", "active-ready"), ("published", "published")):
        rate = pace(hist, key)
        if rate is not None:
            L.append(f"Pace over the last two weeks: {rate * 7:+.0f} {label} a week.")
    L += ["", "## What holds profiles back most", "", "| Missing item | Profiles |", "|---|---:|"]
    L += [f"| {LABEL[k]} | {n:,} |" for k, n in blockers.most_common()]
    L += ["", "## Closest to the line", ""]
    close = sorted(((len(v["missing"]), s) for s, v in teachable.items() if v["missing"]))[:40]
    L += [f"- **{names.get(s, s)}** — needs: " + "; ".join(LABEL[k] for k in teachable[s]["missing"]) for _, s in close]
    L += ["", "## The fifteen items", ""] + [f"{i}. {label}" for i, (_, label) in enumerate(ITEMS, 1)]
    L += ["", "Evidence may come from quote-checked text, from a lesson the machine studied, or (never for counts) from the dance's own performance video. "
          "`pipeline_state/active_ready.json` records which, per profile.", ""]
    return "\n".join(L)

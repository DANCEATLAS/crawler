"""Teacher intelligence — the machine studies how the best online teachers teach (MOVIE_PHASE.md).

The tutorial crawler finds lesson videos per dance and ranks them by what viewers say (tutorial_results.json). This stage
watches the best of them — a few a day, through Gemini's video understanding of the public YouTube URL (nothing is
downloaded; first 8 minutes, low resolution; free tier) — and extracts HOW the teacher teaches: the lesson's structure with
timestamps, the counting scheme, the cues and metaphors, demonstration angles and tempo progression, the mistakes the
teacher names, safety advice, the steps as taught with their counts, what makes the lesson easy to absorb — with short
verbatim quotes so every extraction can be checked against the video.

Per-video records accumulate in pedagogy/videos/<youtube_id>.json. pedagogy/teaching_patterns.json aggregates them
(overall, per dance family, per dance) and ULTIMATE_TEACHER.md is rendered from the aggregate: the cumulative playbook
of how the best teachers teach. pipeline/episodes.py follows it when it writes the chapter scripts, so every lesson in the
atlas is built on the same evidence rather than on one teacher's habits. The playbook grows a little every day; nothing is
ever extracted twice; a video that cannot be read is retried after 30 days.
"""
import os, re, json, glob, time, math
from collections import Counter, defaultdict
from .common import jload, jsave, load_state, log, warn, Report, LLM, now_iso, norm

PEDAGOGY_DIR = "pedagogy"
VIDEOS_DIR = os.path.join(PEDAGOGY_DIR, "videos")
PATTERNS = os.path.join(PEDAGOGY_DIR, "teaching_patterns.json")
PLAYBOOK = "ULTIMATE_TEACHER.md"
RETRY_DAYS = 30
SEGMENTS = ["intro", "context", "warmup", "full_demo", "breakdown", "count_in", "slow_practice", "follow_along", "layering", "mistakes", "music_practice", "recap", "other"]
SEGMENT_LABEL = {"intro": "welcome and what you will learn", "context": "where the dance comes from", "warmup": "warm-up", "full_demo": "the whole step at full speed, once",
                 "breakdown": "breakdown, one movement at a time", "count_in": "the count, out loud", "slow_practice": "slow practice", "follow_along": "follow-along with the teacher",
                 "layering": "adding the next layer (arms, turns, partner)", "mistakes": "common mistakes and corrections", "music_practice": "practice with the music, full tempo", "recap": "recap and homework", "other": "other"}

EXTRACT_SYSTEM = """You are studying HOW a dance teacher teaches, from a public tutorial video. Report only what is seen or heard in the video.
Output a single JSON object:
{"dance_confirmed": true|false  (the video teaches the named dance or a close variant of it; false for performances, vlogs, music videos),
 "teacher_style": "<two sentences on how this teacher works>", "language": "<spoken language>", "level": "beginner|intermediate|advanced|mixed",
 "lesson_structure": [{"t": "m:ss", "segment": "<one of: """ + ", ".join(SEGMENTS) + """>", "note": "<what happens>"}],
 "counting_scheme": "<how the teacher counts, e.g. 5-6-7-8 / quick-quick-slow / 1-2-3 / and-1-and-2>",
 "cues": ["<short verbal cue the teacher repeats (<= 8 words)>"], "metaphors": ["<image or comparison the teacher uses>"],
 "demonstration": {"angles": ["front"|"back"|"side"|"mirror"|"overhead"], "tempo_progression": ["slow"|"half"|"full"], "repetitions_per_step": <integer or null>},
 "common_mistakes": ["<mistake the teacher names and corrects>"], "safety": ["<body or safety advice given>"],
 "steps_taught": [{"name": "<step as the teacher calls it>", "counts": "<counts>", "description": "<one line>"}],
 "absorbability": {"what_works": ["<what makes this lesson easy to absorb>"], "what_hinders": ["<what gets in the way>"]},
 "quotes": [{"t": "m:ss", "text": "<verbatim quote, at most 15 words>"}],
 "evidence_segments": [{"start_s": 0, "end_s": 10, "topic": "movement|teaching",
   "observation": "<specific observed movement or teaching method; describe, do not transcribe>",
   "viewpoint": "<angle and whether the image is mirrored; unknown if unclear>",
   "cannot_infer": "<occlusion, weight transfer, fast movement or other uncertainty>"}],
 "distinctive_method": "<a specific unusual approach worth comparing, not a claim it is best>"}
Rules: 3 to 6 quotes; every list item must come from the video; empty lists when the video shows nothing of the kind;
never invent timestamps; if dance_confirmed is false, keep every list empty. Only the first 480 seconds are supplied.
Give at most 6 evidence_segments. A sampled frame does not establish continuous motion or weight transfer.
Separate what the teacher says from what you can observe. Never infer teaching effectiveness from views/likes.
The extraction is an unreviewed candidate. Describe uncertainty; do not invent corrections or missing counts."""


def evidence_segments(items):
    out = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        start, end = item.get("start_s"), item.get("end_s")
        if (type(start) not in (int, float) or type(end) not in (int, float)
                or not math.isfinite(start) or not math.isfinite(end) or not 0 <= start < end <= 480
                or item.get("topic") not in ("movement", "teaching") or not item.get("observation")):
            continue
        out.append({"start_s": start, "end_s": end, "topic": item["topic"],
                    **{k: str(item.get(k) or "")[:400] for k in ("observation", "viewpoint", "cannot_infer")},
                    "verification": "model_candidate"})
    return out[:6]

def _norm_cue(s):
    return re.sub(r"[^a-z0-9' -]", "", (s or "").lower()).strip()

def _norm_count(s):
    s = (s or "").lower().replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s).strip(" .")
    return s[:60]

# ------------------------------------------------------------------ candidate selection
def pick_targets(budget, only=None):
    tut = jload("tutorial_results.json", {}) or {}
    qidx = load_state("qc_index.json", {}) or {}
    ridx = load_state("research_index.json", {}) or {}
    done = {os.path.basename(f)[:-5]: jload(f, {}) or {} for f in glob.glob(os.path.join(VIDEOS_DIR, "*.json"))}
    today = time.time()
    def retry_ok(v):
        if (v.get("status") == "ok" and v.get("evidence_version") == 2) or v.get("status") == "not_a_lesson":
            return False
        t = v.get("analysed_at") or ""
        try:
            return today - time.mktime(time.strptime(t[:10], "%Y-%m-%d")) >= RETRY_DAYS * 86400
        except Exception:
            return True
    cands = []
    for slug, v in tut.items():
        if only and slug not in only:
            continue
        pub = (qidx.get(slug) or {}).get("publish_gate") == "publish"
        movie = bool((ridx.get(slug) or {}).get("movie_ready"))
        for i, l in enumerate((v.get("lessons") or [])[:4]):
            yid = l.get("youtube_id")
            if not yid or (yid in done and not retry_ok(done[yid])):
                continue
            # the best teachers first: published dances, movie-ready ones, the lesson viewers liked most, one video per dance per day
            cands.append(((0 if pub else 1), (0 if movie else 1), i, -(float(l.get("ratio") or 0)), slug, yid, l))
    cands.sort(key=lambda c: c[:4])
    out, seen = [], set()
    for c in cands:
        if c[4] in seen:
            continue
        seen.add(c[4]); out.append((c[4], c[5], c[6]))
        if len(out) >= budget:
            break
    return out

# ------------------------------------------------------------------ extraction
def analyse(slug, yid, lesson, dance_name, llm):
    url = f"https://www.youtube.com/watch?v={yid}"
    user = (f"DANCE: {dance_name}\nVIDEO TITLE: {lesson.get('title')}\nCHANNEL: {lesson.get('channel')}\n"
            f"Watch the video (first minutes) and extract how the teacher teaches, as specified.")
    jd = llm.json(EXTRACT_SYSTEM, user, strong=False, temperature=0.1, max_tokens=3000, video_url=url, video_seconds=480)
    rec = {"youtube_id": yid, "slug": slug, "dance": dance_name, "title": lesson.get("title"), "channel": lesson.get("channel"), "viewer_ratio": lesson.get("ratio"),
           "analysed_at": now_iso(), "url": url, "evidence_version": 2,
           "observation_window": {"start_s": 0, "end_s": 480, "resolution": "low",
                                  "sampling": "provider default; not continuous motion capture",
                                  "human_verified": False}}
    if not jd:
        rec["status"] = "failed"; return rec
    if jd.get("dance_confirmed") is False:
        rec["status"] = "not_a_lesson"; rec["extraction"] = {"teacher_style": jd.get("teacher_style")}; return rec
    ex = {}
    ex["teacher_style"] = str(jd.get("teacher_style") or "")[:400]
    ex["language"] = str(jd.get("language") or "")[:40]
    ex["level"] = str(jd.get("level") or "")[:20]
    ex["lesson_structure"] = [{"t": str(x.get("t") or "")[:8], "segment": x.get("segment") if x.get("segment") in SEGMENTS else "other", "note": str(x.get("note") or "")[:160]}
                              for x in (jd.get("lesson_structure") or []) if isinstance(x, dict)][:24]
    ex["counting_scheme"] = _norm_count(jd.get("counting_scheme"))
    ex["cues"] = [str(c)[:80] for c in (jd.get("cues") or []) if isinstance(c, str) and c.strip()][:12]
    ex["metaphors"] = [str(c)[:120] for c in (jd.get("metaphors") or []) if isinstance(c, str) and c.strip()][:8]
    d = jd.get("demonstration") if isinstance(jd.get("demonstration"), dict) else {}
    ex["demonstration"] = {"angles": [a for a in (d.get("angles") or []) if a in ("front", "back", "side", "mirror", "overhead")],
                           "tempo_progression": [a for a in (d.get("tempo_progression") or []) if a in ("slow", "half", "full")],
                           "repetitions_per_step": d.get("repetitions_per_step") if isinstance(d.get("repetitions_per_step"), int) else None}
    ex["common_mistakes"] = [str(c)[:160] for c in (jd.get("common_mistakes") or []) if isinstance(c, str) and c.strip()][:10]
    ex["safety"] = [str(c)[:160] for c in (jd.get("safety") or []) if isinstance(c, str) and c.strip()][:6]
    ex["steps_taught"] = [{"name": str(x.get("name") or "")[:80], "counts": str(x.get("counts") or "")[:60], "description": str(x.get("description") or "")[:200]}
                          for x in (jd.get("steps_taught") or []) if isinstance(x, dict) and x.get("name")][:12]
    ab = jd.get("absorbability") if isinstance(jd.get("absorbability"), dict) else {}
    ex["absorbability"] = {"what_works": [str(c)[:160] for c in (ab.get("what_works") or []) if isinstance(c, str)][:6],
                           "what_hinders": [str(c)[:160] for c in (ab.get("what_hinders") or []) if isinstance(c, str)][:6]}
    ex["quotes"] = [{"t": str(q.get("t") or "")[:8], "text": str(q.get("text") or "")[:160]} for q in (jd.get("quotes") or []) if isinstance(q, dict) and q.get("text")][:6]
    ex["evidence_segments"] = evidence_segments(jd.get("evidence_segments"))
    ex["distinctive_method"] = str(jd.get("distinctive_method") or "")[:400]
    rec["status"] = "ok"; rec["extraction"] = ex
    return rec

# ------------------------------------------------------------------ aggregation
def _top(counter, n, min_count=1):
    return [k for k, c in counter.most_common(n) if c >= min_count]

def _segment_order(structs):
    """Canonical order: each segment's average relative position across lessons; segments seen in fewer than 15 % of lessons are dropped."""
    pos, seen = defaultdict(list), Counter()
    for st in structs:
        n = len(st)
        if n < 2:
            continue
        for i, x in enumerate(st):
            pos[x["segment"]].append(i / (n - 1)); seen[x["segment"]] += 1
    total = max(1, len([s for s in structs if len(s) >= 2]))
    order = sorted((sum(v) / len(v), k) for k, v in pos.items() if seen[k] / total >= 0.15 and k != "other")
    return [k for _, k in order]

def _aggregate(records):
    oks = [r for r in records if r.get("status") == "ok" and r.get("extraction")]
    counting = Counter(r["extraction"]["counting_scheme"] for r in oks if r["extraction"].get("counting_scheme"))
    cues = Counter(_norm_cue(c) for r in oks for c in r["extraction"].get("cues") or [] if _norm_cue(c))
    mistakes = Counter(c.strip().rstrip(".").lower() for r in oks for c in r["extraction"].get("common_mistakes") or [])
    works = Counter(c.strip().rstrip(".").lower() for r in oks for c in (r["extraction"].get("absorbability") or {}).get("what_works") or [])
    hinders = Counter(c.strip().rstrip(".").lower() for r in oks for c in (r["extraction"].get("absorbability") or {}).get("what_hinders") or [])
    angles = Counter(a for r in oks for a in (r["extraction"].get("demonstration") or {}).get("angles") or [])
    tempos = Counter(a for r in oks for a in (r["extraction"].get("demonstration") or {}).get("tempo_progression") or [])
    reps = sorted(x for x in ((r["extraction"].get("demonstration") or {}).get("repetitions_per_step") for r in oks) if isinstance(x, int) and 0 < x < 20)
    safety = Counter(c.strip().rstrip(".").lower() for r in oks for c in r["extraction"].get("safety") or [])
    metaphors = [c for r in oks for c in r["extraction"].get("metaphors") or []][:12]
    quotes = [{"dance": r.get("dance"), "t": q.get("t"), "text": q.get("text"), "video": r.get("youtube_id")} for r in oks for q in (r["extraction"].get("quotes") or [])[:2]][:16]
    demo = []
    if angles:
        demo.append("views used by most teachers: " + ", ".join(k for k, _ in angles.most_common(3)))
    if tempos:
        demo.append("tempo progression: " + " → ".join(k for k in ("slow", "half", "full") if tempos.get(k)))
    if reps:
        demo.append(f"repetitions per step: about {reps[len(reps) // 2]}")
    return {"videos": len(oks), "dances": len({r.get("slug") for r in oks}), "counting": counting.most_common(1)[0][0] if counting else None, "counting_all": counting.most_common(6),
            "cues": _top(cues, 12), "mistakes": _top(mistakes, 12), "what_works": _top(works, 10), "what_hinders": _top(hinders, 8), "safety": _top(safety, 8),
            "demonstration": demo, "segment_order": _segment_order([r["extraction"].get("lesson_structure") or [] for r in oks]),
            "metaphors": metaphors, "quotes": quotes}

def aggregate():
    records = [jload(f, {}) or {} for f in glob.glob(os.path.join(VIDEOS_DIR, "*.json"))]
    ridx = load_state("research_index.json", {}) or {}
    fam_of = {}
    for r in records:
        s = r.get("slug")
        if s and s not in fam_of:
            rec = jload(os.path.join("research_results", s + ".json"), None)
            fam_of[s] = (rec or {}).get("family") or ((jload(os.path.join("public", "catalog", "dances.app.json"), {}) or {}).get("styles") or {}).get(s, {}).get("family")
    by_family, by_slug = {}, {}
    for fam in sorted({f for f in fam_of.values() if f}):
        by_family[fam] = _aggregate([r for r in records if fam_of.get(r.get("slug")) == fam])
    for slug in sorted({r.get("slug") for r in records if r.get("slug")}):
        rs = [r for r in records if r.get("slug") == slug]
        a = _aggregate(rs)
        a["steps_as_taught"] = [x for r in rs if r.get("status") == "ok" for x in (r["extraction"].get("steps_taught") or [])][:10]
        a["videos_list"] = [{"youtube_id": r.get("youtube_id"), "title": r.get("title"), "channel": r.get("channel"), "status": r.get("status")} for r in rs]
        by_slug[slug] = a
    out = {"generated_at": now_iso(), "videos_total": len(records), "videos_ok": sum(1 for r in records if r.get("status") == "ok"),
           "videos_not_lessons": sum(1 for r in records if r.get("status") == "not_a_lesson"), "videos_failed": sum(1 for r in records if r.get("status") == "failed"),
           "global": _aggregate(records), "by_family": by_family, "by_slug": by_slug}
    jsave(PATTERNS, out)
    with open(PLAYBOOK, "w", encoding="utf-8") as f:
        f.write(render_playbook(out))
    return out

# ------------------------------------------------------------------ the playbook
def render_playbook(pt):
    g = pt.get("global") or {}
    L = ["# THE ULTIMATE TEACHER — how the best online dance teachers teach", "",
         f"*Built by the machine from {pt.get('videos_ok', 0)} tutorial lessons across {g.get('dances', 0)} dances and {len(pt.get('by_family') or {})} dance families "
         f"(studied: {pt.get('videos_total', 0)} videos; {pt.get('videos_not_lessons', 0)} were not lessons; {pt.get('videos_failed', 0)} could not be read). "
         f"Updated {pt.get('generated_at', '')[:10]}. It grows every day. The chapter scripts in `episodes/` follow it. See `MOVIE_PHASE.md`.*", ""]
    if not g.get("videos"):
        L += ["No lesson has been studied yet. Until the first ones land, the scripts use the built-in formula: count out loud, demonstrate front and back,",
              "three slow repetitions before tempo, one correction at a time, then dance it to the music.", ""]
        return "\n".join(L)
    L += ["## The lesson skeleton the best teachers share", ""]
    order = g.get("segment_order") or []
    for i, seg in enumerate(order, 1):
        L.append(f"{i}. **{SEGMENT_LABEL.get(seg, seg)}**")
    L += ["", "## How they count", "", f"Most common: **{g.get('counting')}**" + (" — also: " + "; ".join(f"{k} ({c})" for k, c in (g.get("counting_all") or [])[1:5]) if len(g.get("counting_all") or []) > 1 else ""), ""]
    L += ["## How they demonstrate", ""] + [f"- {d}" for d in (g.get("demonstration") or [])] + [""]
    L += ["## The cues they repeat", ""] + [f"- {c}" for c in (g.get("cues") or [])] + [""]
    if g.get("metaphors"):
        L += ["## Images they use", ""] + [f"- {m}" for m in g["metaphors"][:8]] + [""]
    L += ["## Mistakes they name most", ""] + [f"- {m}" for m in (g.get("mistakes") or [])] + [""]
    if g.get("safety"):
        L += ["## Body and safety advice", ""] + [f"- {m}" for m in g["safety"]] + [""]
    L += ["## What makes a lesson absorbable", ""] + [f"- {w}" for w in (g.get("what_works") or [])] + ["", "## What gets in the way", ""] + [f"- {w}" for w in (g.get("what_hinders") or [])] + [""]
    if g.get("quotes"):
        L += ["## In their words", ""] + [f"- \"{q['text']}\" — {q['dance']} lesson, {q['t']} (youtube {q['video']})" for q in g["quotes"][:10]] + [""]
    fams = sorted(((v.get("videos") or 0, k) for k, v in (pt.get("by_family") or {}).items()), reverse=True)[:8]
    if fams:
        L += ["## By dance family", ""]
        for n, fam in fams:
            v = pt["by_family"][fam]
            L.append(f"**{fam}** ({n} lesson{'s' if n != 1 else ''}): counting {v.get('counting') or '—'}; order: " + " → ".join(SEGMENT_LABEL.get(s, s) for s in (v.get("segment_order") or [])[:8]) + (("; cues: " + ", ".join(v.get("cues")[:5])) if v.get("cues") else ""))
        L.append("")
    L += ["## By dance", ""]
    for slug, v in sorted((pt.get("by_slug") or {}).items()):
        if not v.get("videos"):
            continue
        steps = "; ".join(f"{s.get('name')} ({s.get('counts')})" if s.get("counts") else s.get("name") for s in (v.get("steps_as_taught") or [])[:4])
        L.append(f"- **{slug}** — {v['videos']} lesson{'s' if v['videos'] != 1 else ''}; counting {v.get('counting') or '—'}" + (f"; steps as taught: {steps}" if steps else "") + (f"; mistakes: {', '.join(v['mistakes'][:3])}" if v.get("mistakes") else ""))
    L += ["", "## Method", "", "Each lesson is watched once by a vision-language model (first eight minutes, public YouTube URL, nothing downloaded) and reduced to a fixed form: structure with timestamps, counting, cues, demonstration, mistakes, safety, steps with counts, absorbability, verbatim quotes. The lists above are frequencies across all lessons; a line appears only when at least one teacher did it. Per-video records: `pedagogy/videos/`. Aggregate: `pedagogy/teaching_patterns.json`.", ""]
    return "\n".join(L)

# ------------------------------------------------------------------ run
def run(budget=6, only=None):
    rep = Report("pedagogy")
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    llm = LLM()
    if not llm.gemini_key and not llm.dry:
        rep.note("no GEMINI_API_KEY: video understanding needs Gemini; aggregate only")
        targets = []
    else:
        targets = pick_targets(budget, only=only)
    rep.note(f"lessons to study: {len(targets)} (budget {budget})")
    cat = (jload(os.path.join("public", "catalog", "dances.app.json"), {}) or {}).get("styles") or {}
    for slug, yid, lesson in targets:
        name = (cat.get(slug) or {}).get("name") or slug.replace("-", " ")
        try:
            if llm.dry:
                rep.inc("dry_run"); continue
            rec = analyse(slug, yid, lesson, name, llm)
            jsave(os.path.join(VIDEOS_DIR, yid + ".json"), rec)
            rep.inc("video_" + rec["status"])
            log(f"PEDAGOGY {slug} {yid}: {rec['status']}" + (f" counting={rec['extraction'].get('counting_scheme')} steps={len(rec['extraction'].get('steps_taught') or [])}" if rec.get("status") == "ok" else ""))
        except Exception as e:
            rep.error(f"pedagogy {slug} {yid}: {e}")
    pt = aggregate()
    llm.record(rep)
    rep.note(f"playbook: {pt.get('videos_ok')} lessons across {(pt.get('global') or {}).get('dances')} dances")
    return rep.finish()

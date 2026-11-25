"""The door: one documented way into the library, for the website and for any agent. Offline, no model calls.

The owner's direction (21 November 2026): the product will be an agent that holds a full conversation and draws on
the whole library and on the education of how to teach. Until that technology arrives the knowledge is kept ready,
so that every profile can be activated overnight. Ready means readable through one door:

  public/catalog/manifest.json   da_manifest_v1   where to start: every file, its contract, the standing rules
  public/catalog/index.json      da_index_v1      every dance in a few fields, with the address and fingerprint of its file
  public/catalog/d/<slug>.json   da_dance_v1      everything about one dance
  public/catalog/machine.json    da_machine_v1    how the machine is doing: nights, pace, what holds pages back

A dance file changes only when the dance does. It carries no clock, so an unchanged dance costs no commit, and an
agent that kept yesterday's fingerprints fetches only what moved. Sacred or restricted dances carry their story and
no teaching material: what must not be taught is not in the door.
"""
import datetime as dt
import glob
import hashlib
import json
import os
import re
from collections import Counter
from .common import norm, now_iso
from .readiness import LABEL, STANDARD, _by_slug, _given, _load
from .taxonomy import COUNTRIES_N, FAMILIES, ISO_TO_REGION, REGIONS

BASE = "https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/"
LIGHT = ("slug", "name", "aliases", "tagline", "country", "country_code", "flag_emoji", "region", "family", "era", "hero_video_youtube_id",
         "tier", "publish_gate", "research_gate", "unesco", "lat", "lng", "tradition_status")
WITHHELD = ("teaching", "movement_profile", "adaptations")          # never in the door for a sacred or restricted dance
WITHHELD_STATES = ("story_ready_teaching_withheld", "teaching_withheld")
EMPTY = (None, "", [], {})
TEACHES = re.compile(r"\b(tutorial|lessons?|how to|learn(?:ing)?|step by step|basic steps?|beginners?|class(?:es)?|master ?class|workshop|teach(?:ing|es)?"
                     r"|instruction(?:al)?|aprende|paso a paso|clases?|c[oó]mo bailar|pasos b[aá]sicos|cours|apprendre|lernen|урок)\b", re.I)   # a video title that offers to teach
RENAMED = {"how_is_danced": "how_it_is_danced"}                    # a key the writing model misspelt
NOTE = "Gathered and written by a machine from public sources and checked against them. Not reviewed by a person, not rights-cleared, not tested on learners. The rules are in manifest.json."
RULES = [
    "Everything here was gathered and written by a machine from public sources and checked against them: quotes, links, timestamps. It has not been reviewed by a person, cleared for rights or tested on learners. Say so when you use it.",
    "A dance with teaching_withheld is sacred or restricted. Tell its story with care. Never teach it, and never rebuild its steps from other sources.",
    "Never invent steps, counts, origins, credits or rankings. What is missing is missing: readiness.missing names it.",
    "What a machine saw in a video is a candidate, not a verified fact (verification: model_candidate). A performance never supplies counts.",
    "Teach from bdf_teaching_system.json: dna is the default behaviour, adjustments and mentor.feelings answer a difficulty or a feeling, learner_model is what to keep in mind about one person. It is evidence, not a verdict. mentor_brief.json holds the same in a few thousand words, sized to sit beside one dance in a conversation.",
    "Atlas (traditions) and Viral (challenges and dance culture) are separate collections.",
    "Videos, pictures and music are linked, never copied. A link is not a licence to reuse.",
    "The state active_ready means the machine has gathered everything a teaching service needs for that dance. Activation still needs human review, music rights and platform tests (ACTIVE_PROFILE_STANDARD.md).",
]
FILES = (("manifest.json", "da_manifest_v1", "where to start: every file, its contract and the standing rules"),
         ("index.json", "da_index_v1", "every dance in a few fields, with the address and fingerprint of its own file"),
         ("bdf_teaching_system.json", "da_bdf_teaching_v1", "how to teach anyone to dance: the teaching DNA, how to adjust, the mentor, what to remember about a learner, with the evidence"),
         ("active_ready.json", "da_active_ready_v1", "the starting line: which dances have everything a teaching service needs"),
         ("machine.json", "da_machine_v1", "how the machine is doing: the last nights, the pace, what holds pages back"),
         ("site.json", "da_site_v1", "the words of the website's newer screens"),
         ("viral.json", "da_viral_v1", "the viral dance challenges: who made each, when, the song and the sources; in order of date, not a ranking"),
         ("research.json", "da_research_v1", "the mentor's reading list: every research topic and where it stands, what was found with its checked quotes, the papers of the open search"),
         ("mentor_brief.json", "da_mentor_brief_v1", "the mentor in a few thousand words, sized for an agent's context: the default behaviour, the six moments, what to do when it is hard"),
         ("retired.json", "", "entries that were removed or merged, and where they went"),
         ("episodes.json", "dw_episodes_v1", "draft scripts per dance (a presentation asset, not proof of readiness)"),
         ("dances.app.json", "dw_app_v1", "the older single file the website loaded before the index; kept for compatibility"),
         ("profiles_v2.json", "dw_profiles_v2", "the older single file of deep profiles; the same content is in d/<slug>.json"))
SECTIONS = {"card": "identity and the short story: names, places, era, family, hero video, pictures, sources",
            "profile": "the deep profile of a published dance: story sections, music, movement, connections, footage, checked claims",
            "readiness": "the dance against the starting line: how many of the items it has and which are missing",
            "lessons": "lessons the machine studied: parts with their time, steps with counts, cues, common mistakes, what works",
            "performances": "what the machine saw in the dance's own performance video",
            "episodes": "the state of the draft scripts and where they are",
            "teaching_withheld": "present on a sacred or restricted dance: why nothing is taught"}
PREFIXES = ("the ", "republic of ", "kingdom of ", "state of ", "federal republic of ", "people s republic of ")
ONE_COUNTRY_WITH_AND = {norm(x) for x in ("Antigua and Barbuda", "Bosnia and Herzegovina", "Saint Kitts and Nevis", "Saint Vincent and the Grenadines",
                                          "Sao Tome and Principe", "Trinidad and Tobago")}


def places(text, first=None):
    """Every country a free-text origin names, in order, as ISO codes: 'France and Italy' is two places, not a third country."""
    out = [first] if first else []

    def find(piece):
        n = norm(piece)
        hit = COUNTRIES_N.get(n) if n else None
        if n and not hit:
            hit = next((COUNTRIES_N[n[len(p):]] for p in PREFIXES if n.startswith(p) and n[len(p):] in COUNTRIES_N), None)
        return hit[0] if hit else None

    for chunk in re.split(r",|/|;|\(|\)|:|–|—|→", str(text or "")):
        chunk = chunk.replace("&", " and ")
        pieces = [chunk] if norm(chunk) in ONE_COUNTRY_WITH_AND else re.split(r"\band\b", chunk)
        for piece in pieces:
            code = find(piece)
            if code and code not in out:
                out.append(code)
    return out


def _sacred(style, ready):
    """Is teaching withheld? The readiness measure decides for a dance the writer has researched and the gates passed:
    it read the sources, and a bare keyword such as "ceremony" is ritual context, not a restriction (LEDGER rule 3).
    Until then the catalogue's broader flags decide, on the careful side."""
    state = (ready or {}).get("state")
    if state in WITHHELD_STATES:
        return True
    if state in ("active_ready", "building"):
        return False
    return bool(style.get("is_sacred") or style.get("_is_sacred"))


def _full(d):
    return {k: v for k, v in d.items() if v not in EMPTY}


def _tidy(obj):
    """Keys as the contract names them: no stray spaces, a known misspelling put right. A correctly named key wins."""
    if isinstance(obj, list):
        return [_tidy(x) for x in obj]
    if not isinstance(obj, dict):
        return obj
    out = {}
    for k, v in obj.items():
        key = RENAMED.get(k.strip(), k.strip())
        if key == k or out.get(key) in EMPTY:
            out[key] = _tidy(v)
    return out


def _secs(t):
    """'1:13' -> 73; None when the mark is not a time."""
    try:
        parts = [int(p) for p in str(t).strip().split(":")]
    except ValueError:
        return None
    return sum(p * 60 ** i for i, p in enumerate(reversed(parts)))


def _said(rows):
    return [r for r in rows or [] if _given(r)]


def lesson(rec):
    """One studied lesson, as the door shows it: what the teacher does, described. The teacher's own words stay out."""
    e, w = rec.get("extraction") or {}, rec.get("observation_window") or {}
    steps = []
    for s in e.get("steps_taught") or []:
        if isinstance(s, dict) and s.get("name"):
            steps.append(_full({"name": s.get("name"), "counts": s.get("counts") if _given(s.get("counts")) else None, "description": s.get("description")}))
    parts = [_full({"t": p.get("t"), "seconds": _secs(p.get("t")), "segment": p.get("segment"), "note": p.get("note")})
             for p in e.get("lesson_structure") or [] if isinstance(p, dict)]
    return _full({"youtube_id": rec.get("youtube_id"), "url": rec.get("url"), "title": rec.get("title"), "channel": rec.get("channel"),
                  "analysed_on": str(rec.get("analysed_at") or "")[:10], "level": e.get("level"), "language": e.get("language"),
                  "counting_scheme": e.get("counting_scheme") if _given(e.get("counting_scheme")) else None,
                  "parts": parts, "steps": steps, "cues": _said(e.get("cues")), "images": _said(e.get("metaphors")),
                  "common_mistakes": _said(e.get("common_mistakes")), "safety": _said(e.get("safety")),
                  "teacher_style": e.get("teacher_style"), "distinctive_method": e.get("distinctive_method"),
                  "what_works": _said((e.get("absorbability") or {}).get("what_works")), "what_hinders": _said((e.get("absorbability") or {}).get("what_hinders")),
                  "evidence": [_full(x) for x in e.get("evidence_segments") or [] if isinstance(x, dict)],
                  "seen": _full({"from_s": w.get("start_s"), "to_s": w.get("end_s"), "checked_by_a_person": bool(w.get("human_verified"))})})


def show(rec):
    w = rec.get("observation_window") or {}
    return _full({"youtube_id": rec.get("youtube_id"), "url": rec.get("url"), "analysed_on": str(rec.get("analysed_at") or "")[:10],
                  "observation": _full(rec.get("observation") or {}),
                  "seen": _full({"from_s": w.get("start_s"), "to_s": w.get("end_s"), "checked_by_a_person": bool(w.get("human_verified"))})})


def light(style, ready, lessons):
    """The few fields a list, a map or a search needs. Same names as dw_app_v1 where the field existed."""
    e = {k: style[k] for k in LIGHT if style.get(k) not in EMPTY and style.get(k) is not False}
    if e.get("aliases"):
        e["aliases"] = [a for a in e["aliases"] if isinstance(a, str)][:8]
    cs = places(style.get("country"), style.get("country_code"))
    if cs:
        e["countries"] = cs
    sacred = _sacred(style, ready)
    if sacred:
        e["is_sacred"] = True
    if (style.get("hero_qc") or {}).get("verdict") == "pass":
        e["hero_ok"] = True
    e["state"] = (ready or {}).get("state") or "listed"
    if ready:
        e["have"], e["of"] = ready["have"], ready["of"]
    if lessons and not sacred:
        e["lessons"] = len(lessons)
    return e


def dance(slug, style, deep, ready, lessons, shows, pack):
    """Everything about one dance. No clock inside: the content alone decides whether the file changes."""
    sacred = _sacred(style, ready)
    out = {"contract": "da_dance_v1", "slug": slug, "name": style.get("name") or slug, "state": (ready or {}).get("state") or "listed", "note": NOTE}
    cs = places(style.get("country"), style.get("country_code"))
    if cs:
        out["countries"] = cs
    card = _full(style)
    if sacred:
        card.pop("tutorials", None)
        if isinstance(card.get("video_stack"), list):      # the hero passed the vision check as a performance and stays
            card["video_stack"] = [v for v in card["video_stack"]
                                   if not (isinstance(v, dict) and v.get("role") != "hero" and TEACHES.search(str(v.get("title") or "")))]
    out["card"] = card
    if deep:
        prof = _full(_tidy(deep))
        if sacred:
            for k in WITHHELD:
                prof.pop(k, None)
            if isinstance(prof.get("episode_brief"), dict):
                prof["episode_brief"] = {k: v for k, v in prof["episode_brief"].items() if k not in ("lesson_ladder", "instructor_persona")}
        out["profile"] = prof
    if ready:
        out["readiness"] = _full({"standard": STANDARD, "have": ready["have"], "of": ready["of"],
                                  "missing": [{"key": k, "label": LABEL.get(k, k)} for k in ready.get("missing") or []],
                                  "via": ready.get("via"), "ritual_context": bool(ready.get("ritual_context")) or None})
    if sacred:
        out["teaching_withheld"] = str(style.get("sacred_note") or "").strip() or "Sacred or restricted: the story is told, the dance is not taught."
    else:
        if lessons:
            out["lessons"] = [lesson(x) for x in sorted(lessons, key=lambda x: str(x.get("youtube_id")))]
        if shows:
            out["performances"] = [show(x) for x in sorted(shows, key=lambda x: str(x.get("youtube_id")))]
    if pack:
        out["episodes"] = dict(_full({k: pack.get(k) for k in ("status", "chapters", "scenes", "gaps", "runtime_min", "polished", "languages")}), file=f"episodes/{slug}.json")
    return out


def facets(index):
    """What a list page needs to count, so that no page has to guess: the dances of each country (a dance counts under every
    country it belongs to), the regions that hold them, each family, and how many dances have no place or no family yet."""
    places, fam = {}, Counter()
    for e in index.values():
        for code in e.get("countries") or []:
            places.setdefault(code, {"region": ISO_TO_REGION.get(code) or "Other", "dances": 0})["dances"] += 1
        fam[e.get("family") if e.get("family") in FAMILIES else ""] += 1
    held = {p["region"] for p in places.values()}
    return {"regions": [r for r in REGIONS + ["Other"] if r in held],
            "places": {k: places[k] for k in sorted(places)},
            "no_place": sum(1 for e in index.values() if not e.get("countries")),
            "families": {k: {"name": name, "dances": fam[k]} for k, name in FAMILIES.items() if fam.get(k)},
            "no_family": fam.get("", 0)}


def fingerprint(obj):
    return hashlib.sha1(json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, path)


def _save_index(path, head, dances, retired):
    """The index with one dance on a line: light, and a nightly diff stays readable."""
    one = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    rows = ",\n".join(f"  {one(k)}:{one(v)}" for k, v in dances.items())
    body = ",\n".join(f" {one(k)}:{one(v)}" for k, v in head.items())
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("{\n" + body + ",\n \"dances\":{\n" + rows + "\n },\n \"retired\":" + one(retired) + "\n}\n")
    os.replace(tmp, path)


def write_dance(path, obj, today):
    """Write the file only when the dance changed. Returns (fingerprint, day it last changed, written?)."""
    fp = fingerprint(obj)
    old = _load(path, None)
    if isinstance(old, dict) and old.get("fingerprint") == fp and old.get("updated"):
        return fp, old["updated"], False
    _save(path, dict(obj, fingerprint=fp, updated=today.isoformat()))
    return fp, today.isoformat(), True


def _time(s):
    try:
        return dt.datetime.strptime(str(s)[:19], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None


def nights(runs, gap_hours=6):
    """The stage records of pipeline_state/runs.json, joined into runs: a new one starts after a pause of `gap_hours`."""
    out, last = [], None
    for r in runs or []:
        t = _time(r.get("started")) if isinstance(r, dict) else None
        if t is None:
            continue
        if not out or (t - last).total_seconds() > gap_hours * 3600:
            out.append({"date": r["started"][:10], "started": r["started"], "stages": [], "errors": [], "questions": 0, "unanswered": 0, "trouble": []})
        n = out[-1]
        n["finished"] = r.get("finished") or r["started"]
        n["stages"].append(r.get("stage"))
        n["errors"] += [f"{r.get('stage')}: {e}" for e in r.get("errors") or []]
        c = r.get("counters") or {}
        n["questions"] += int(c.get("llm_requests") or 0)
        n["unanswered"] += int(c.get("llm_unanswered") or 0)
        n["trouble"] += [f"{r.get('stage')}: {x}" for x in r.get("notes") or [] if str(x).startswith("model trouble")]
        last = _time(n["finished"]) or t
    for n in out:
        a, b = _time(n["started"]), _time(n["finished"])
        n["minutes"] = round((b - a).total_seconds() / 60) if a and b else None
        # a nightly run, not one stage tried by hand. The door is built before the night's last two stages (sync, report):
        # a run that has reached both video stages is tonight's run, or the page would always show the night before.
        n["whole"] = "research" in n["stages"] and ("report" in n["stages"] or {"pedagogy", "teaching"} <= set(n["stages"]))
    return out


def _rate(hist, key, days=14):
    """Change a day over the last `days` days of the readiness history; None with less than two days."""
    if len(hist) < 2:
        return None
    end = dt.date.fromisoformat(hist[-1]["date"])
    first = next((h for h in hist if dt.date.fromisoformat(h["date"]) >= end - dt.timedelta(days=days)), hist[0])
    span = (end - dt.date.fromisoformat(first["date"])).days
    return None if span < 1 else round((hist[-1].get(key, 0) - first.get(key, 0)) / span, 1)


def study(root, today=None, budget=None):
    """The mentor's study in a few numbers, for the owner's page: how much of the reading list is read, what is read next,
    and how far the topics of the owner's direction of 21 November have come. No model, no network."""
    from . import teaching as T
    notes = {}
    for f in glob.glob(os.path.join(root, "pedagogy", "science", "*.json")):
        r = _load(f, {})
        if isinstance(r, dict) and r.get("key"):
            notes[r["key"]] = r
    keys = [item[0] for item in T.SCIENCE]
    read = lambda k: (notes.get(k) or {}).get("status") == "ok"
    n = int(os.environ.get("SCIENCE_BUDGET", "3")) if budget is None else budget
    c = (_load(os.path.join(root, "public", "catalog", "bdf_teaching_system.json"), {}) or {}).get("counts") or {}
    return _full({"topics": len(keys), "topics_read": sum(1 for k in keys if read(k)),
                  "first": {"topics": len(T.FIRST_TOPICS), "read": sum(1 for k in T.FIRST_TOPICS if read(k))},
                  "next": [item[0] for item in T.pick_science(notes, n, today)],
                  "papers_read": sum(1 for k, r in notes.items() if k.startswith("paper-") and r.get("status") == "ok"),
                  "lessons_studied": c.get("lessons_studied_for_method"), "teachers_studied": c.get("teachers_studied"),
                  "findings_checked": c.get("science_findings_checked"),
                  "practices": c.get("practices_total"), "practices_in_dna": c.get("practices_with_two_or_more_kinds")})


def mentor_brief(system):
    """The mentor in a few thousand words, for an agent that is about to teach: the same lines as bdf_teaching_system.json,
    the strongest first and a few of each, so that it fits beside one dance in a conversation. Nothing is written here that
    the study did not write. None when the study has no teaching DNA yet."""
    if not isinstance(system, dict) or not system.get("dna"):
        return None
    words = lambda rows, key, n: [str(r[key]).strip() for r in (rows or []) if isinstance(r, dict) and str(r.get(key) or "").strip()][:n]
    mentor, c = system.get("mentor") or {}, system.get("counts") or {}
    return _full({
        "contract": "da_mentor_brief_v1",
        "what_this_is": "How to teach anyone to dance, as far as the nightly study has come. Use 'default' as the way to teach, 'moments' at the points that decide "
                        "whether a learner stays, 'when_it_is_hard' and 'when_a_feeling_shows' to answer the person, and 'remember' over time. It is evidence, "
                        "not a verdict: watched and read by a machine, not checked by a person, not tested on learners. The whole study with its proof is in bdf_teaching_system.json.",
        "stands_on": _full({k: c.get(k) for k in ("teachers_studied", "lessons_studied_for_method", "comments_read", "science_findings_checked", "practices_with_two_or_more_kinds", "practices_total")}),
        "default": [_full({"theme": r.get("theme"), "do": r.get("do"), "kinds_of_evidence": r.get("evidence_kinds")}) for r in system["dna"] if isinstance(r, dict) and r.get("do")],
        "moments": [_full({"moment": m.get("moment"), "title": m.get("title"), "seen": m.get("seen"), "teachers_do": words(m.get("examples"), "says", 3)})
                    for m in mentor.get("moments") or [] if isinstance(m, dict)],
        "when_it_is_hard": [_full({"about": a.get("tag"), "learners_say": [str(x) for x in (a.get("learners_say") or [])[:2]],
                                   "teachers_offer": words(a.get("teachers_offer"), "adjustment", 3), "research_adds": [str(x) for x in (a.get("research") or [])[:2]]})
                            for a in system.get("adjustments") or [] if isinstance(a, dict)],
        "when_a_feeling_shows": [_full({"feeling": f.get("feeling"), "seen": f.get("seen"), "teachers_answer": words(f.get("responses"), "response", 2)})
                                 for f in mentor.get("feelings") or [] if isinstance(f, dict)],
        "what_teachers_believe": [_full({"about": b.get("title"), "teachers": b.get("teachers"), "in_their_words": words(b.get("beliefs"), "belief", 2)})
                                  for b in mentor.get("creed") or [] if isinstance(b, dict)],
        "how_they_sound": [v[0] for v in (mentor.get("voice") or [])[:5] if isinstance(v, (list, tuple)) and v],
        "remember": [str(x["remember"]) for x in system.get("learner_model") or [] if isinstance(x, dict) and x.get("remember")]})


PAPERS_SHOWN = 120   # the newest papers in research.json; all of them stay in pedagogy/science/ and in bdf_teaching_system.json


def library(root, today=None, budget=None):
    """The mentor's reading list as one open file, for the owner and for any agent: every research topic and where it stands
    (read, read next, waiting, or tried without a usable result), first by the three strands of the owner's direction of
    21 November 2026 and then by the themes of the teaching vocabulary; what each reading found, with the quotes that were
    checked against the source; and the papers of the open search. No model, no network. None when no note exists yet."""
    from . import teaching as T
    notes = {}
    for f in glob.glob(os.path.join(root, "pedagogy", "science", "*.json")):
        r = _load(f, {})
        if isinstance(r, dict) and r.get("key"):
            notes[r["key"]] = r
    if not notes:
        return None
    n = int(os.environ.get("SCIENCE_BUDGET", "3")) if budget is None else budget
    nxt = [item[0] for item in T.pick_science(notes, n, today)]
    STATE = {"ok": "read", "thin": "thin", "no_sources": "no_sources", "failed": "unanswered"}

    def found(r):
        """What a reading found. Only a note that stands on two or more checked quotes is used; nothing else is shown as a finding."""
        srcs = {s.get("url"): s for s in r.get("sources") or [] if isinstance(s, dict)}
        cited = [u for u in dict.fromkeys(f.get("source") for f in r.get("findings") or []) if u in srcs]
        return _full({"principle": r.get("principle"), "for_the_teacher": r.get("for_the_teacher"), "when_it_does_not_apply": r.get("when_it_does_not_apply"),
                      "findings": [_full({k: f.get(k) for k in ("finding", "quote", "source")}) for f in r.get("findings") or []],
                      "sources": [_full({k: srcs[u].get(k) for k in ("url", "title", "authors", "year", "journal")}) for u in cited]})

    def topic(item):
        key, _, _, tags = item
        r = notes.get(key) or {}
        state = STATE.get(r.get("status"), "waiting")
        if state != "read" and key in nxt:
            state = "next"
        out = {"key": key, "name": key.replace("_", " "), "state": state, "tags": [t for t in tags if t in T.PRACTICES],
               "on": str(r.get("written_at") or "")[:10]}
        return _full(dict(out, **found(r)) if state == "read" else out)

    by_key = {item[0]: item for item in T.SCIENCE}
    theme_of = {t: name for name, tags in T.THEMES for t in tags}
    mine = {k for _, _, keys in T.STRANDS for k in keys}
    groups = [{"key": key, "name": name, "owner": True, "topics": [topic(by_key[k]) for k in keys if k in by_key]} for key, name, keys in T.STRANDS]
    for name, _ in T.THEMES:
        rows = [topic(item) for item in T.SCIENCE if item[0] not in mine and theme_of.get((item[3] or [""])[0]) == name]
        if rows:
            groups.append({"key": re.sub(r"[^a-z]+", "-", name.lower()).strip("-"), "name": name, "owner": False, "topics": rows})
    placed = {t["key"] for g in groups for t in g["topics"]}
    rest = [topic(item) for item in T.SCIENCE if item[0] not in placed]
    if rest:
        groups.append({"key": "other", "name": "Other", "owner": False, "topics": rest})
    papers = sorted((r for k, r in notes.items() if k.startswith("paper-") and r.get("status") == "ok"), key=lambda r: str(r.get("written_at") or ""), reverse=True)
    shown = []
    for r in papers[:PAPERS_SHOWN]:
        src = (r.get("sources") or [{}])[0]
        shown.append(_full(dict({"key": r["key"], "title": r.get("topic"), "on": str(r.get("written_at") or "")[:10], "tags": [t for t in r.get("tags") or [] if t in T.PRACTICES],
                                  "authors": src.get("authors"), "year": src.get("year"), "journal": src.get("journal"), "url": src.get("url"), "cited_by": src.get("cited_by")}, **found(r))))
    topics = [t for g in groups for t in g["topics"]]
    states = Counter(t["state"] for t in topics)
    search = _load(os.path.join(root, "pedagogy", "research_state.json"), {}) or {}
    return {"contract": "da_research_v1",
            "what_this_is": "The reading list of the mentor's study. A finding is shown only when the words quoted for it were found in the source. Most studies are about learning movement in general, not dance. Read by a machine, not yet checked by a person.",
            "counts": {"topics": len(topics), **{k: states.get(k, 0) for k in ("read", "next", "waiting", "thin", "no_sources", "unanswered")},
                       "owner_topics": len(mine), "owner_read": sum(1 for t in topics if t["key"] in mine and t["state"] == "read"),
                       "papers": len(papers), "papers_shown": len(shown),
                       "findings_checked": sum(len(r.get("findings") or []) for r in notes.values() if r.get("status") == "ok"),
                       "searches": len(T.PAPER_QUERIES), "searches_asked": min(len(T.PAPER_QUERIES), int(search.get("paper_first") or 0) + int(search.get("paper_search") or 0))},
            "a_night": {"topics": n, "papers": int(os.environ.get("PAPER_BUDGET", "2"))},
            "next": nxt, "groups": groups, "papers": shown}


VIRAL_ORDER = "by when each challenge began, newest first. This is not a ranking: no popularity is known or claimed."


def viral(root):
    """The viral dance challenges as one open file, built from this repository alone: the verified facts, the category, the
    videos found. No rank and no view counts: none is known, and the list is in order of date. None when the list is missing."""
    P = lambda *a: os.path.join(root, *a)
    facts = _load(P("viral_challenges_verified.json"), None)
    if not isinstance(facts, list) or not facts:
        return None
    found = _load(P("viral_results.json"), {})
    found = found if isinstance(found, dict) else {}
    cats = (_load(P("viral_categories.json"), {}) or {}).get("categories") or {}
    rows = []
    for f in facts:
        if not isinstance(f, dict) or not f.get("slug"):
            continue
        r = found.get(f["slug"]) if isinstance(found.get(f["slug"]), dict) else {}
        date = str(f.get("origin_date") or "").strip()
        year = re.match(r"\d{4}", date) or re.match(r"\d{4}", str(r.get("origin_year") or ""))
        stack = [_full({k: v.get(k) for k in ("youtube_id", "role", "title", "channel")}) for v in r.get("video_stack") or [] if isinstance(v, dict) and v.get("youtube_id")]
        rows.append(_full({"slug": f["slug"], "name": f.get("name"), "category": cats.get(f["slug"]), "song": f.get("song"),
                           "origin_date": date, "origin_year": int(year.group(0)) if year else None,
                           "originator": f.get("originator"), "originator_story": f.get("originator_story"), "timeline": f.get("timeline"), "peak_period": f.get("peak_period"),
                           "fun_facts": f.get("fun_facts"),
                           "celebrity_performances": [c for c in (_full(x) for x in f.get("celebrity_performances") or [] if isinstance(x, dict)) if c],
                           "platform": r.get("platform"), "hero_video_youtube_id": r.get("hero_video_youtube_id"), "hero_title": r.get("hero_brief"), "hero_channel": r.get("channel"),
                           "video_stack": stack, "original_video_url": f.get("original_video_url") if str(f.get("original_video_url") or "").startswith("http") else None,
                           "sources": [u for u in f.get("sources") or [] if isinstance(u, str) and u.startswith("http")]}))
    rows.sort(key=lambda x: str(x.get("name") or "").lower())
    rows.sort(key=lambda x: (x.get("origin_year") or 0, x.get("origin_date") or ""), reverse=True)      # stable: names stay in order within a date
    return {"contract": "da_viral_v1", "count": len(rows), "order": VIRAL_ORDER,
            "categories": dict(sorted(Counter(x["category"] for x in rows if x.get("category")).items())), "challenges": rows}


def crawl_notes(crawl, gen):
    """What the crawl said about itself (pipeline_state/crawl_report.json, written by crawler.py), as notes for the machine's
    page: every part that ended before its work was done, and silence for two days. Without these a crawl that found
    almost nothing looks like any other: its run is green and only its log knows (24 November 2026)."""
    if not isinstance(crawl, dict) or not crawl.get("at"):
        return []
    notes = ["crawl: " + str(x)[:160] for x in crawl.get("stops") or []]
    a, b = _time(crawl.get("at")), _time(gen)
    if a and b and (b - a).total_seconds() > 48 * 3600:
        notes.append(f"crawl: no report since {str(crawl['at'])[:10]}")
    return notes


def machine(runs, hist, state, names, owner, gen, study=None, crawl=None):
    """How the machine is doing, for one page in large type."""
    whole = [n for n in nights(runs) if n["whole"]]
    brief = lambda n: {k: n[k] for k in ("date", "started", "finished", "minutes", "questions", "unanswered")} | {"stages": len(n["stages"]), "errors": n["errors"][:10], "trouble": n["trouble"][:10]}
    profiles = (state or {}).get("profiles") or {}
    building = {s: v for s, v in profiles.items() if v.get("state") == "building"}
    blockers = Counter(k for v in building.values() for k in v.get("missing") or [])
    close = sorted((len(v["missing"]), s) for s, v in building.items() if v.get("missing"))[:40]
    hist = sorted((h for h in hist or [] if isinstance(h, dict) and h.get("date")), key=lambda h: h["date"])
    out = {"contract": "da_machine_v1", "generated_at": gen,
            "last_night": brief(whole[-1]) if whole else None,
            "nights": [{k: n[k] for k in ("date", "minutes", "questions", "unanswered")} | {"errors": len(n["errors"])} for n in whole[-30:]],
            "counts": (state or {}).get("counts") or {},
            "line": [{k: h.get(k) for k in ("date", "listed", "researched", "published", "active_ready", "lessons_studied", "performances_observed")} for h in hist[-400:]],
            "pace": {"days": min(14, (dt.date.fromisoformat(hist[-1]["date"]) - dt.date.fromisoformat(hist[0]["date"])).days) if len(hist) > 1 else 0,
                     "per_night": {k: _rate(hist, k) for k in ("listed", "published", "active_ready")}},
            "blockers": [{"key": k, "label": LABEL.get(k, k), "profiles": n} for k, n in blockers.most_common()],
            "closest": [{"slug": s, "name": names.get(s, s), "needs": [LABEL.get(k, k) for k in building[s]["missing"]], "need_keys": list(building[s]["missing"])} for _, s in close],
            "owner": _full({"status": (owner or {}).get("status"), "text": (owner or {}).get("reason"), "verified_at": (owner or {}).get("verified_at")})}
    if study:
        out["study"] = study
    if isinstance(crawl, dict) and crawl.get("at"):
        out["last_crawl"] = {k: crawl.get(k) for k in ("at", "hero", "lessons", "viral", "stops")}
        if out["last_night"]:
            out["last_night"]["trouble"] = (crawl_notes(crawl, gen) + out["last_night"]["trouble"])[:10]
    return out


def run(root=".", today=None):
    P = lambda *a: os.path.join(root, *a)
    C = lambda *a: P("public", "catalog", *a)
    today = today or dt.date.today()
    gen = now_iso()
    styles = (_load(C("dances.app.json"), {}) or {}).get("styles") or {}
    if not styles:
        return {"error": "public/catalog/dances.app.json is missing or empty: run build first", "counters": {}}
    gone = [x for x in (_load(C("retired.json"), {}) or {}).get("retired", []) if isinstance(x, dict) and x.get("slug")]
    retired = {x["slug"]: x.get("merged_into") or x.get("duplicate_of") for x in gone}
    deep = (_load(C("profiles_v2.json"), {}) or {}).get("profiles") or {}
    state = _load(P("pipeline_state", "active_ready.json"), {}) or {}
    ready = state.get("profiles") or {}
    packs = (_load(C("episodes.json"), {}) or {}).get("packs") or {}
    lessons, shows = _by_slug(P("pedagogy", "videos")), _by_slug(P("pedagogy", "performances"))
    index, written, names = {}, 0, {}
    for slug in sorted(styles):
        if slug in retired:
            continue
        st = styles[slug]
        names[slug] = st.get("name") or slug
        doc = dance(slug, st, deep.get(slug), ready.get(slug), lessons.get(slug), shows.get(slug), packs.get(slug))
        fp, updated, new = write_dance(C("d", slug + ".json"), doc, today)
        written += new
        index[slug] = dict(light(st, ready.get(slug), lessons.get(slug)), fp=fp, updated=updated)
    removed = 0
    for f in glob.glob(C("d", "*.json")):
        if os.path.basename(f)[:-5] not in index:
            os.remove(f)
            removed += 1
    states = Counter(e["state"] for e in index.values())
    _save_index(C("index.json"), {"contract": "da_index_v1", "generated_at": gen, "count": len(index), "states": dict(sorted(states.items())), "file": "d/{slug}.json", **facets(index)},
                index, {k: retired[k] for k in sorted(retired)})
    owner = (_load(P("pipeline_state", "vision_status.json"), {}) or {}).get("owner_action")
    _save(C("machine.json"), machine(_load(P("pipeline_state", "runs.json"), []), _load(P("pipeline_state", "active_ready_history.json"), []), state, names, owner, gen,
                                     study(root, today), crawl=_load(P("pipeline_state", "crawl_report.json"), None)))
    chart = viral(root)
    if chart:
        write_dance(C("viral.json"), chart, today)        # like a dance file: no clock inside, rewritten only when it changed
    shelf = library(root, today)
    if shelf:
        write_dance(C("research.json"), shelf, today)
    brief = mentor_brief(_load(C("bdf_teaching_system.json"), {}) or {})
    if brief:
        write_dance(C("mentor_brief.json"), brief, today)
    files, total = [], 0
    for name, contract, holds in FILES:
        if name != "manifest.json" and not os.path.exists(C(name)):
            continue
        size = os.path.getsize(C(name)) if os.path.exists(C(name)) else None
        total += size or 0
        files.append(_full({"file": name, "contract": contract, "holds": holds, "bytes": size}))
    d_bytes = sum(os.path.getsize(f) for f in glob.glob(C("d", "*.json")))
    teaching = _load(C("bdf_teaching_system.json"), {}) or {}
    _save(C("manifest.json"), {"contract": "da_manifest_v1", "generated_at": gen, "library": "Dance Atlas",
                               "what_this_is": "The whole Dance Atlas library, readable by a website or by any agent. Start here, read the rules, then index.json, then one file per dance.",
                               "base": BASE, "rules": RULES, "files": files,
                               "dance_file": {"pattern": "d/{slug}.json", "contract": "da_dance_v1", "count": len(index), "bytes": d_bytes, "sections": SECTIONS,
                                              "changes": "A dance file carries no clock. Compare the fingerprint in index.json (fp) with the one you kept and fetch only what moved."},
                               "counts": dict(state.get("counts") or {}, in_the_door=len(index)),
                               "teaching": _full({"file": "bdf_teaching_system.json", "how_to_use": teaching.get("how_to_use")}),
                               "whole_library": {"bytes_behind_this_door": total + d_bytes,
                                                 "copy": "A dated copy of the whole repository is published every month: https://github.com/DANCEATLAS/crawler/releases",
                                                 "note": "Small enough to keep on a phone or to load into an agent that works without a connection."},
                               "read_more": {"vision": "https://github.com/DANCEATLAS/crawler/blob/main/PRODUCT_VISION.md", "state": "https://github.com/DANCEATLAS/crawler/blob/main/LEDGER.md",
                                             "starting_line": "https://github.com/DANCEATLAS/crawler/blob/main/ACTIVE_READY.md"}})
    return {"counters": {"dances": len(index), "written": written, "removed": removed, "bytes": d_bytes, "viral": (chart or {}).get("count", 0), "research_topics": ((shelf or {}).get("counts") or {}).get("topics", 0),
                         **{"state_" + k: v for k, v in states.items()}}}

"""Offline Active Profile dossiers and gap queues; no model calls.

Candidate evidence is never approval. ACTIVE_PROFILE_STANDARD.md defines review.
Runtime activation is a separate, currently unbuilt capability.
"""
import datetime as dt
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from . import readiness_research as RR

SCHEMA = "da_active_profile_v1"
REVIEW_ROLES = ("practitioner", "teaching", "learner_outcomes", "language", "rights", "social_accessibility")
MUSIC_USES = ("interactive_lesson", "group_session", "recording", "social_export", "tempo_edit")
FIELDS = {
    "movement": ("movement_profile", ("footwork", "posture", "formation_and_space", "what_to_avoid")),
    "music_structure": ("music_profile", ("meter", "rhythm_pattern", "sound_description")),
    "interaction": ("interaction_profile", ("learning_units", "feedback_rules", "social_formats", "prerequisites")),
}


def read(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {} if default is None else default


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def write_changed(path, value):
    path = Path(path)
    body = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == body:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return True


def real(value):
    if isinstance(value, dict):
        return any(real(v) for v in value.values())
    if isinstance(value, list):
        return any(real(v) for v in value)
    return isinstance(value, str) and bool(value.strip()) and not re.search(
        r"not described|not derivable|unknown|withheld|not provided|not documented|^n/?a$|^none$", value.strip(), re.I)


def date_valid(start, end, today):
    try:
        return dt.date.fromisoformat(start) <= today <= dt.date.fromisoformat(end)
    except (TypeError, ValueError):
        return False


def music_cleared(track, today):
    """Validate the recorded review, not the legal substance of its evidence."""
    return (track.get("status") == "reviewed" and real(track.get("asset_id"))
            and real(track.get("composition_evidence")) and real(track.get("recording_evidence"))
            and real(track.get("reviewer")) and real(track.get("quality_review"))
            and real(track.get("territories")) and real(track.get("conditions"))
            and date_valid(track.get("reviewed_on"), track.get("recheck_on"), today)
            and date_valid(track.get("valid_from"), "9999-12-31" if track.get("valid_until") == "perpetual" else track.get("valid_until"), today)
            and all((track.get("uses") or {}).get(k) is True for k in MUSIC_USES))


def build_profile(kind, slug, entry, research, videos, supplement, approvals, today, discovered_questions=None):
    profile = research.get("profile") or {}
    material = {"entry": entry, "research": research, "videos": videos, "supplement": supplement}
    open_questions = RR.questions(profile.get("activation_questions"), allowed_sources=set(research.get("sources") or []))
    open_questions += discovered_questions or []
    fingerprint = digest({"schema": SCHEMA, "material": material, "open_questions": open_questions})
    gaps = {"research": [], "video": [], "rights": [], "review": [], "platform": [
        "Validated voice/movement feedback and accessible controls",
        "Human BDF consent/matching, moderation and measured session synchronization",
        "Tested camera/split-screen delivery; AR remains an optional future adapter"]}
    sources = list(dict.fromkeys(research.get("sources") or entry.get("sources") or []))
    if not sources or not any(c.get("supported") for c in research.get("claims", [])):
        gaps["research"].append("Cited identity, community/variant and living-status evidence")
    for label, (field, required) in FIELDS.items():
        block = supplement.get(field) or profile.get(field) or {}
        missing = [k for k in required if not real(block.get(k))]
        if missing:
            gaps["research"].append(label + ": " + ", ".join(missing))
    from .pedagogy import evidence_segments
    teaching = [v for v in videos if isinstance(v, dict) and v.get("status") == "ok"
                and re.fullmatch(r"[A-Za-z0-9_-]{11}", str(v.get("youtube_id") or ""))
                and v.get("url") == "https://www.youtube.com/watch?v=" + v["youtube_id"]]
    topics = {s["topic"] for v in teaching for s in evidence_segments((v.get("extraction") or {}).get("evidence_segments"))}
    if not {"movement", "teaching"} <= topics:
        gaps["video"].append("Timestamped movement and teaching evidence with observation limits")
    if len({v.get("channel") for v in teaching if v.get("channel")}) < 2:
        gaps["video"].append("Compare independent teachers/variants; preserve unique methods")
    tracks = [t for t in supplement.get("music_options", []) if isinstance(t, dict) and music_cleared(t, today)]
    if len({t["asset_id"] for t in tracks}) < 2:
        gaps["rights"].append("Two musically reviewed choices with composition AND recording rights for intended uses")
    for role in REVIEW_ROLES:
        valid = any(a.get("role") == role and a.get("human_review") is True
                    and a.get("fingerprint") == fingerprint and real(a.get("reviewer"))
                    and real(a.get("evidence")) and a.get("decision") == "approved"
                    and date_valid(a.get("reviewed_on"), a.get("recheck_on"), today)
                    for a in approvals if isinstance(a, dict))
        if not valid:
            gaps["review"].append(role + ": current human review with evidence and scope")
    scope = supplement.get("scope") or {}
    if not all(real(scope.get(k)) for k in ("languages", "audiences", "session_modes", "territories")):
        gaps["review"].append("Declare languages, audiences, session modes and territories covered by review")
    for question in open_questions:
        gaps[question["domain"]].append("Investigate: " + question["question"] + " Evidence needed: " + question["next_evidence"])
    restricted = bool(profile.get("is_sacred") or entry.get("is_sacred") or research.get("sacred_cue_flag")
                      or supplement.get("teaching_withheld"))
    # Research and contextual appreciation continue; a flag cannot override the
    # existing sacred/restricted-teaching policy.
    if restricted:
        state = "teaching_withheld"
    elif any(gaps[k] for k in ("research", "video", "rights")):
        state = "researching"
    elif gaps["review"]:
        state = "awaiting_review"
    else:
        state = "ready_for_activation"
    return {"contract": SCHEMA, "id": kind + ":" + slug, "kind": kind, "slug": slug,
            "name": entry.get("name") or profile.get("name") or slug, "fingerprint": fingerprint,
            "state": state, "runtime_active": False, "gaps": gaps, "sources": sources, "open_questions": open_questions,
            "research_file": ("research_results/" + slug + ".json" if kind == "atlas" else "pipeline_state/activation_inputs.json") if research else None,
            "video_evidence": [{"url": v.get("url"), "file": "pedagogy/videos/" + v.get("youtube_id", "") + ".json",
                                "status": "candidate_unreviewed"} for v in teaching],
            "candidate_material": {k: supplement.get(k) or profile.get(k) or {} for k in
                                   ("movement_profile", "music_profile", "interaction_profile", "teaching", "adaptations")},
            "music_options": supplement.get("music_options") or [],
            "scope": supplement.get("scope") or {"languages": ["unreviewed"], "audiences": [], "session_modes": []},
            "limitations": ["Presence of data does not establish teaching accuracy or permission.",
                            "Video model observations are candidates, not motion capture or expert verification."]}


def run(root=".", today=None):
    root = Path(root)
    today = today or dt.date.today()
    styles = read(root / "public/catalog/dances.app.json").get("styles") or {}
    virals = read(root / "viral_results.json")
    retired = {x.get("slug") for x in read(root / "public/catalog/retired.json").get("retired", [])}
    supplements = read(root / "pipeline_state/activation_inputs.json").get("profiles") or {}
    approvals = read(root / "pipeline_state/activation_approvals.json").get("profiles") or {}
    registry = RR.read(root / "pipeline_state/readiness_findings.json", {})
    findings = RR.open_findings(registry, today)
    question_counts = Counter()
    by_slug = defaultdict(list)
    for path in sorted((root / "pedagogy/videos").glob("*.json")):
        rec = read(path)
        by_slug[rec.get("slug")].append(rec)
    summaries, queue = {}, {}
    written = 0
    for kind, entries in (("atlas", styles), ("viral", virals)):
        for slug, entry in sorted(entries.items()):
            if kind == "atlas" and slug in retired:
                continue
            if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", slug) or not isinstance(entry, dict):
                raise ValueError("Invalid profile identity: " + str(slug))
            pid = kind + ":" + slug
            # Research files lack namespaces. Never attach Atlas evidence to a
            # same-named Viral entry without explicit typed linkage.
            supplement = supplements.get(pid, {})
            research = read(root / "research_results" / (slug + ".json")) if kind == "atlas" else supplement.get("research", {})
            videos = by_slug.get(slug, []) if kind == "atlas" else supplement.get("videos", [])
            dossier = build_profile(kind, slug, entry, research, videos, supplement, approvals.get(pid, []), today,
                                    RR.for_profile(findings, pid))
            question_counts.update(q["domain"] for q in dossier["open_questions"])
            path = "active_profiles/" + kind + "/" + slug + ".json"
            written += write_changed(root / path, dossier)
            summaries[pid] = {k: dossier[k] for k in ("name", "state", "fingerprint", "runtime_active")}
            summaries[pid]["path"] = path
            queue[pid] = {"kind": kind, "slug": slug, "region": entry.get("region"), "gaps": dossier["gaps"]}
    counts = dict(Counter(v["state"] for v in summaries.values()))
    index = {"contract": SCHEMA, "evaluated_on": today.isoformat(), "count": len(summaries), "states": counts,
             "runtime_active": 0, "profiles": summaries}
    write_changed(root / "public/catalog/active_profiles.json", index)
    write_changed(root / "pipeline_state/activation_gaps.json", {"evaluated_on": today.isoformat(), "profiles": queue})
    RR.write_agenda(root, summaries, today, registry, question_counts)
    lines = ["# Active Profile readiness", "", "Evaluated " + today.isoformat() + ". No model calls; existing budgets unchanged.", "",
             f"{len(summaries):,} dossiers; {counts.get('ready_for_activation', 0):,} ready for activation; 0 running interactive experiences.", "",
             "## Missing work across the catalogue", "", "| Work stream | Profiles with gaps |", "|---|---:|"]
    for group in ("research", "video", "rights", "review", "platform"):
        lines.append(f"| {group} | {sum(bool(q['gaps'][group]) for q in queue.values())} |")
    technology = read(root / "pipeline_state/technology_watch.json").get("capabilities") or []
    due = [c["id"] for c in technology if not date_valid(c.get("checked_on"), c.get("recheck_on"), today)]
    lines += ["", "Technology evidence needing recheck: " + (", ".join(due) if due else "none in the recorded watchlist" if technology else "watchlist unavailable"),
              "", "Read ACTIVE_PROFILE_STANDARD.md and MUSIC_STRATEGY.md. Detailed gaps: pipeline_state/activation_gaps.json.",
              "Only research gaps enter the existing capped enrichment queue. Rights, human review and platform work need their own evidence; model retries cannot clear them.",
              "Atlas and Viral IDs are separate. Retired Atlas identities are absent from the current index; archived dossier files are not current entries."]
    (root / "ACTIVE_PROFILE_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"counters": {"profiles": len(summaries), "dossiers_changed": written, "ready": counts.get("ready_for_activation", 0), "active": 0}}

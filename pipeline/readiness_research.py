"""Evolving activation questions and a bounded external-research agenda.

This module is offline. Source research happens in the existing capped composer
and the separately scheduled research task, never by claiming a queue is research.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

REVISION = 1
DOMAINS = ("research", "video", "rights", "review", "platform")
AREAS = ("movement_and_teaching", "learning_and_access", "music_and_rights",
         "ai_interaction", "human_connection", "viral_creation", "technology_and_cost")


def read(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def write_changed(path, value):
    path = Path(path)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def questions(items, allowed_sources=None, limit=6):
    """Keep grounded questions, not model-authored approval or new fetched URLs."""
    if not isinstance(items, list) or limit <= 0:
        return []
    out, seen = [], set()
    for item in items:
        if not isinstance(item, dict) or item.get("domain") not in DOMAINS:
            continue
        fields = ("question", "why_needed", "next_evidence", "source")
        if not all(isinstance(item.get(k), str) and item[k].strip() for k in fields):
            continue
        source = item["source"].strip()
        try:
            url = urlsplit(source)
            if url.scheme != "https" or not url.hostname or url.username or url.password:
                continue
        except ValueError:
            continue
        if allowed_sources is not None and source not in allowed_sources:
            continue
        q = {k: item[k].strip()[:1200] for k in fields}
        q["domain"] = item["domain"]
        key = hashlib.sha256(json.dumps(q, sort_keys=True).encode()).hexdigest()[:16]
        if key in seen:
            continue
        seen.add(key)
        out.append(dict(q, id=key, status="candidate_unreviewed"))
        if len(out) >= limit:
            break
    return out


def valid_date(value, today):
    try:
        return dt.date.fromisoformat(value) <= today
    except (TypeError, ValueError):
        return False


def open_findings(registry, today):
    """A bare 'resolved' flag cannot erase a requirement; stale closures reopen."""
    result = []
    for item in registry.get("findings", []):
        if not isinstance(item, dict) or not questions([item]):
            continue
        resolution = item.get("resolution") or {}
        try:
            current = today <= dt.date.fromisoformat(resolution.get("recheck_on", ""))
        except (TypeError, ValueError):
            current = False
        closed = (item.get("status") == "resolved" and resolution.get("evidence")
                  and resolution.get("reviewer") and valid_date(resolution.get("reviewed_on"), today) and current)
        if not closed:
            result.append(item)
    return result


def for_profile(findings, profile_id):
    # No wildcard/substring matching: Atlas and Viral remain separate identities.
    return questions([f for f in findings if isinstance(f.get("profile_ids"), list)
                      and profile_id in f["profile_ids"]], limit=12)


def review_age(record, today, fingerprint=None):
    record = record if isinstance(record, dict) else {}
    if (not valid_date(record.get("checked_on"), today)
            or fingerprint is not None and record.get("fingerprint") != fingerprint):
        return "0000-00-00"
    return record["checked_on"]


def write_agenda(root, profiles, today, registry, question_counts):
    """Pick actual research work; evaluation dates never advance research dates."""
    root = Path(root)
    reviews = registry.get("area_reviews") or {}
    focus = min(AREAS, key=lambda a: (review_age(reviews.get(a), today), AREAS.index(a)))
    profile_reviews = registry.get("profile_reviews") or {}
    samples = []
    for kind in ("atlas", "viral"):
        candidates = [pid for pid in profiles if pid.startswith(kind + ":")]
        if candidates:
            samples.append(min(candidates, key=lambda pid: (
                review_age(profile_reviews.get(pid), today, profiles[pid]["fingerprint"]), pid)))
    findings = open_findings(registry, today)
    global_findings = [f for f in findings if f.get("scope") == "platform"]
    agenda = {"contract": "da_readiness_research_v1", "evaluated_on": today.isoformat(),
              "next_focus": focus, "profile_sample": samples,
              "profile_questions_by_domain": dict(question_counts),
              "open_external_findings": len(findings), "platform_findings": global_findings,
              "last_external_research": registry.get("last_external_research"),
              "limits": {"profiles_per_external_pass": 2, "external_source_pages": 6,
                         "additional_pipeline_model_calls": 0},
              "execution_note": "Offline agenda only. External research requires the scheduled task or an authorized researcher. Pending integration is not publication."}
    write_changed(root / "pipeline_state/readiness_research_agenda.json", agenda)
    lines = ["# Continuing research toward Active Profiles", "",
             "Agenda evaluated " + today.isoformat() + "; this date is not a research completion date.", "",
             "Next focus: **" + focus.replace("_", " ") + "**.",
             "Rotating sample: " + (", ".join(samples) or "no current profiles") + ".",
             "Source-backed profile questions: " + str(sum(question_counts.values())) + ".",
             "Open external findings: " + str(len(findings)) + ".", "",
             "The daily pipeline re-evaluates all dossiers. Its existing research calls now ask what requirements may have been overlooked.",
             "The separate daily research task searches fresh primary/practitioner sources, tests the completeness of the requirements, and records the next evidence or experiment.",
             "Neither a queued question nor a provider demonstration is validated teaching or activation approval.", "",
             "## Current platform investigations", ""]
    for finding in global_findings[:12]:
        lines += ["- " + finding["question"], "  Evidence to obtain: " + finding["next_evidence"],
                  "  Source: " + finding["source"]]
    lines += ["", "Read CONTINUOUS_RESEARCH.md for the update/closure contract and access limits."]
    (root / "CONTINUOUS_RESEARCH_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return agenda

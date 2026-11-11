"""Plain-language weekly progress. No model calls, external requests or email delivery.

Capabilities come from a dated, evidence-linked register; counts come from repository files.
Unknown, stale and missing are deliberate states, never silently converted to success.
"""
import datetime as dt
import html
import re

BASE = "https://github.com/DANCEATLAS/crawler"
DETAIL = BASE + "/blob/main/reports/weekly/details.md"


def age_days(value, when):
    try:
        return (when.date() - dt.date.fromisoformat(str(value)[:10])).days
    except (TypeError, ValueError):
        return None


def fresh(value, when, limit):
    age = age_days(value, when)
    return age is not None and 0 <= age <= limit


def change(now, before):
    if before is None:
        return "earlier comparison unavailable"
    d = now - before
    return "no change this week" if d == 0 else f"{abs(d):,} {'more' if d > 0 else 'fewer'} this week"


def safe_url(value):
    # Register links must be project HTTPS links, never executable or credential URLs.
    return value if isinstance(value, str) and value.startswith((BASE + "/", "https://supabase.com/dashboard/")) else BASE + "/blob/main/IMPLEMENTATION_LEDGER.md"


def owner_action(now, when):
    state = now.get("vision") or {}
    action = state.get("owner_action") or {}
    if action.get("status") == "open" and fresh(action.get("verified_at"), when, action.get("valid_days", 7)):
        return {"title": action.get("title") or "One action needs you", "reason": action.get("reason") or "See the project ledger.", "url": safe_url(action.get("url"))}
    if action.get("status") == "resolved" and fresh(action.get("verified_at"), when, action.get("valid_days", 7)):
        return {"title": "Nothing needs you this week", "reason": "No owner-only action is currently recorded.", "url": None}
    return {"title": "No current request for you", "reason": "The access/decision record needs a fresh check before asking you to act.", "url": None}


def vision_rows(now, when):
    state = now.get("vision") or {}
    current = fresh(state.get("reviewed_at"), when, state.get("review_due_days", 30))
    rows = []
    for area in state.get("areas") or []:
        row = dict(area)
        if not current:
            row["status"] = "Needs recheck"
            row["text"] = "Last recorded: " + row.get("text", "Status unavailable.")
        live = {
            "atlas": f"{now['dances_live']:,} entries; {now['published']:,} published deep profiles.",
            "teaching": f"{now['episode_packs']:,} script packs; {now['episode_complete']:,} without recorded content gaps.",
            "language": f"{now['translations_current']:,} current translation drafts; {now['translations_reviewed']:,} complete, native-reviewed translations recorded.",
            "viral": f"{now['viral_entries']:,} entries in the saved collection." if now.get("viral_entries") is not None else "Collection count unavailable."
        }.get(row.get("id"))
        if live:
            row["text"] = live + " " + row.get("text", "")
        rows.append(row)
    if not rows:
        rows.append({"id": "missing", "title": "Whole-vision review", "status": "Not recorded", "text": "The capability register is missing. Do not infer that BDF, Viral, music, social or AR features are complete."})
    return rows


def highlights(now, week):
    result = []
    for key, label in [("published", "Published deep profiles"), ("with_tutorials", "Dances with tutorial references"), ("episode_packs", "Draft script packs")]:
        result.append(f"{label}: {now[key]:,} — {change(now[key], week.get(key) if week else None)}.")
    if week and now["dances_live"] < week["dances_live"]:
        result.append("The catalogue is smaller this week. Removals and merges can improve quality; see the editorial log for the reasons.")
    return result


def operating_notes(now, h, when):
    latest = max((r.get("finished", "") for r in now.get("runs", []) if r.get("stage") == "report" and r.get("finished", "") <= when.isoformat().replace("+00:00", "Z")), default="")
    recent = fresh(latest, when, 2)
    run = (f"Content growth: {h['days']} daily reports recorded this week. "
           f"{h['unanswered']} AI requests remained unanswered.")
    if h['errors']:
        run += f" {h['errors']} other errors need checking."
    if not recent:
        run += " No recent completed report is recorded; check the jobs."
    if h["retries"]:
        run += " Some requests also needed retries or an alternative model; details are linked below."
    budget = "Budget: this report uses no paid AI calls. Existing free/prepaid limits are unchanged. Actual spending and remaining balance are not measured by this report."
    if h["quota"]:
        budget += " A quota refusal was recorded; its provider balance needs checking. No top-up is assumed."
    database = "Database: no dated mirror count is available."
    if now.get("database_dances") is not None:
        comparison = "match" if now["database_dances"] == now["dances_live"] else "differ"
        database = f"Platform support: the Atlas and database counts {comparison} (checked {str(now.get('database_at'))[:10]})."
        if comparison == "differ":
            database += " Check which records still need syncing; the Atlas uses its own catalogue."
        if not fresh(now.get("database_at"), when, 2):
            database += " The database observation is old."
    notes = [run, budget, database]
    support = (now.get("vision") or {}).get("platform_observation") or {}
    if support.get("text"):
        age = "" if fresh(support.get("verified_at"), when, support.get("valid_days", 14)) else " Needs recheck."
        notes.append(f"Platform check ({support.get('verified_at', 'undated')}): {support['text']}{age}")
    return notes


def priorities(now, when):
    rows = vision_rows(now, when)
    if any(r["status"] == "Needs recheck" for r in rows):
        return ["Refresh the capability evidence before claiming progress.", "Fill evidenced teaching gaps within existing limits.", "Recheck Viral rankings, permissions and platform support."]
    areas = {r["id"]: r for r in rows}
    return [areas[k]["next"] for k in ("teaching", "viral", "music") if areas.get(k, {}).get("next")]


def render_md(now, week, month, start, labels, hist, when, h):
    action = owner_action(now, when)
    lines = [f"# Dance Atlas — weekly report · {when.strftime('%a %d %b %Y')}", "",
             "## Your week at a glance", "", *["- " + x for x in highlights(now, week)], "",
             "**Draft scripts and automated checks are preparation, not validated classes.**", "",
             "## " + action["title"], "", action["reason"]]
    if action["url"]:
        lines += ["", f"[Open the page]({action['url']})"]
    lines += ["", "## The whole vision", ""]
    for row in vision_rows(now, when):
        lines += [f"**{row['title']} · {row['status']}**", "", row["text"], ""]
    lines += ["Capability review: " + str((now.get("vision") or {}).get("reviewed_at") or "not recorded") + ". Counts are measured from saved project files, not a live test of every feature.", "", "## Cost & reliability", ""]
    lines += ["- " + x for x in operating_notes(now, h, when)]
    lines += ["", "## Next work", ""] + ["- " + x for x in priorities(now, when)]
    lines += ["", f"[Explore the evidence and detailed numbers]({DETAIL}) · [Full vision]({BASE}/blob/main/PRODUCT_VISION.md) · [Platform ledger]({BASE}/blob/main/IMPLEMENTATION_LEDGER.md)", ""]
    return "\n".join(lines)


def subject(now, week, when):
    return "Dance Atlas · your weekly progress · " + when.strftime("%d %b")


def render_html(now, week, month, start, labels, hist, when, h):
    esc = html.escape
    action = owner_action(now, when)
    font = "font-family:Arial,Helvetica,sans-serif;"
    ink, muted, green = "#17372d", "#52635d", "#245c47"
    def p(text, size=17):
        return f"<p style='margin:0 0 12px;{font}font-size:{size}px;line-height:1.55;color:{ink}'>{esc(text)}</p>"
    def title(text):
        return f"<h2 style='margin:30px 0 14px;{font}font-size:24px;line-height:1.25;color:{ink}'>{esc(text)}</h2>"
    body = f"<p style='margin:0 0 9px;{font}font-size:16px;font-weight:bold;letter-spacing:1px;color:{green}'>DANCE ATLAS</p>"
    body += f"<h1 style='margin:0 0 10px;{font}font-size:34px;line-height:1.15;color:{ink}'>Your weekly progress</h1>"
    body += p(when.strftime("%d %B %Y") + " · A clear view of the whole vision", 16)
    body += "<table role='presentation' width='100%' cellpadding='0' cellspacing='0' style='width:100%;margin-top:20px;border-collapse:collapse'><tr>"
    for key, label in [("published", "deep profiles"), ("episode_packs", "draft scripts")]:
        body += (f"<td class='metric' width='50%' style='vertical-align:top;background:#edf4ee;padding:18px;border:4px solid white;{font}'>"
                 f"<div style='font-size:36px;line-height:1.15;font-weight:bold;color:{ink}'>{now[key]:,}</div>"
                 f"<div style='font-size:18px;color:{ink};margin-top:6px'>{label}</div>"
                 f"<div style='font-size:15px;line-height:1.4;color:{muted};margin-top:8px'>{esc(change(now[key], week.get(key) if week else None))}</div></td>")
    body += "</tr></table>"
    body += p(f"{now['dances_live']:,} Atlas entries · {now['with_tutorials']:,} dances with tutorial references", 16)
    body += p("Draft scripts are preparation. They are not yet validated classes.")
    body += f"<div style='background:#fff3db;border-left:5px solid #a87613;padding:18px 20px;margin:22px 0'>"
    body += f"<h2 style='margin:0 0 8px;{font}font-size:23px;line-height:1.25;color:{ink}'>{esc(action['title'])}</h2>" + p(action["reason"])
    if action["url"]:
        body += f"<a href='{esc(action['url'], quote=True)}' style='{font}font-size:18px;font-weight:bold;color:{green};text-decoration:underline'>Open the page →</a>"
    body += "</div>"
    if week and now['dances_live'] < week['dances_live']:
        body += p("The catalogue is smaller this week. Removals and merges can improve quality; the detailed report links to the editorial reasons.")
    body += title("The whole vision")
    body += p("What exists, what needs work, and what comes later.", 16)
    for row in vision_rows(now, when):
        body += f"<div style='padding:15px 0;border-top:1px solid #dce5de'>"
        body += f"<h3 style='margin:0 0 6px;{font}font-size:19px;line-height:1.35;color:{ink}'>{esc(row['title'])}</h3>"
        body += f"<p style='margin:0 0 7px;{font}font-size:15px;font-weight:bold;color:{green}'>{esc(row['status'])}</p>" + p(row["text"]) + "</div>"
    reviewed = (now.get("vision") or {}).get("reviewed_at") or "not recorded"
    body += p(f"Capability review: {reviewed}. Counts come from saved project files; they are not a live test of every feature.", 15)
    body += title("Cost & reliability")
    for note in operating_notes(now, h, when):
        body += p(note, 16)
    body += title("Next work")
    for i, item in enumerate(priorities(now, when), 1):
        body += p(f"{i}. {item}")
    body += f"<p style='margin:26px 0'><a href='{DETAIL}' style='{font}font-size:18px;font-weight:bold;color:{green}'>Explore the evidence and detailed numbers →</a></p>"
    body += (f"<p style='{font}font-size:15px;line-height:1.7;border-top:1px solid #dce5de;padding-top:18px'>"
             f"<a href='{BASE}/blob/main/PRODUCT_VISION.md' style='color:{green}'>Full vision</a> · "
             f"<a href='{BASE}/blob/main/IMPLEMENTATION_LEDGER.md' style='color:{green}'>Platform ledger</a> · "
             f"<a href='{BASE}/actions' style='color:{green}'>Run history</a></p>")
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{esc(subject(now, week, when))}</title>"
            "<style>@media only screen and (max-width:520px){.pad{padding:24px 18px!important}.wrap{padding:0!important}.metric{padding:14px!important}}</style></head>"
            f"<body style='margin:0;padding:0;background:#f1f4ef'><table role='presentation' width='100%' cellpadding='0' cellspacing='0' style='width:100%'><tr><td class='wrap' align='center' style='padding:28px 12px'>"
            "<!--[if mso]><table role='presentation' width='640'><tr><td><![endif]-->"
            f"<table role='presentation' width='100%' cellpadding='0' cellspacing='0' style='width:100%;max-width:640px;background:white'><tr><td class='pad' style='padding:34px 32px'>{body}</td></tr></table>"
            "<!--[if mso]></td></tr></table><![endif]--></td></tr></table></body></html>")

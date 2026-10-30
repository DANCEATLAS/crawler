"""Daily status + review queue, committed to the repo (STATUS.md, QC_REPORT.md) and pushed to Supabase when the tables exist."""
import os, json
from collections import Counter
from .common import Supabase, log, warn, now_iso, today, jload, Report, load_state, save_state, PIPELINE_VERSION
from .qc import QC_DIR

def _db_stats(sb):
    s = {}
    if not sb.enabled:
        return s
    try:
        rows = sb.select("dances", select=sb.safe_select("dances", "slug,hero_video_youtube_id,tier,publish_gate,is_sacred,ich_ref,wikipedia_url,profile"), order="slug.asc")
        s["dances"] = len(rows)
        s["with_hero"] = sum(1 for r in rows if (r.get("hero_video_youtube_id") or "").strip())
        s["content_ready"] = sum(1 for r in rows if r.get("tier") == "content_ready")
        s["gate_publish"] = sum(1 for r in rows if r.get("publish_gate") == "publish")
        s["sacred"] = sum(1 for r in rows if r.get("is_sacred"))
        s["unesco"] = sum(1 for r in rows if r.get("ich_ref"))
        s["profile_over_1500"] = sum(1 for r in rows if len(r.get("profile") or "") > 1500)
        cols = sb.columns("dances")
        if "profile_long" in cols:
            rows2 = sb.select("dances", select="slug,profile_long,albums,images,research_gate", order="slug.asc")
            s["profile_long"] = sum(1 for r in rows2 if (r.get("profile_long") or "").strip())
            s["albums"] = sum(1 for r in rows2 if r.get("albums"))
            s["images"] = sum(1 for r in rows2 if r.get("images"))
            s["research_published"] = sum(1 for r in rows2 if r.get("research_gate") == "publish")
        try:
            v = sb.select("viral_challenges", select="slug", order="slug.asc")
            s["viral_challenges"] = len(v)
        except Exception:
            pass
    except Exception as e:
        warn("db stats", e)
    return s

def run():
    rep = Report("report")
    sb = Supabase()
    runs = load_state("runs.json", [])
    cands = load_state("candidates.json", {})
    rindex = load_state("research_index.json", {})
    qindex = load_state("qc_index.json", {})
    hq = load_state("hero_qc.json", {})
    heroes = jload("hero_results.json", {}) or {}
    audit = load_state("audit.json", {})
    db = _db_stats(sb)
    cstat = Counter(v.get("status") for v in cands.values())
    rstat = Counter(v.get("status") for v in rindex.values())
    qstat = Counter(v.get("publish_gate") for v in qindex.values())
    hstat = Counter(v.get("verdict") for v in hq.values())
    last = {}
    for r in runs[-60:]:
        last[r["stage"]] = r
    lines = [f"# Dancing Atlas pipeline status", f"_Generated {now_iso()} · pipeline {PIPELINE_VERSION}_", "",
             "## Catalogue (Supabase)"]
    if db:
        lines += [f"- Dances: **{db.get('dances')}** · with hero video: **{db.get('with_hero')}** · content_ready: {db.get('content_ready')} · publish gate: {db.get('gate_publish')} · sacred: {db.get('sacred')} · UNESCO refs: {db.get('unesco')}"]
        if "profile_long" in db:
            lines += [f"- Deep profiles (profile_long): **{db.get('profile_long')}** · research published: {db.get('research_published')} · with verified albums: {db.get('albums')} · with licensed images: {db.get('images')}"]
        if "viral_challenges" in db:
            lines += [f"- Viral challenges: {db.get('viral_challenges')}"]
    else:
        lines += ["- (database not reachable in this run)"]
    lines += ["", "## Catalogue audit", f"- Retired/merged: {sum(1 for v in audit.values() if v.get('decision') in ('retire','merge'))} · judged: {sum(1 for v in audit.values() if v.get('judge'))} of {len(styles_total) if (styles_total := (jload('app_catalog.json', {}) or {}).get('styles') or {}) else '?'}"]
    lines += ["", "## Crawler", f"- Hero results on file: {len(heroes)} · statuses: {dict(Counter((v or {}).get('status') for v in heroes.values()))}",
              f"- Hero QC verdicts: {dict(hstat)} (checked {len(hq)})", "",
              "## Discovery → research → QC", f"- Candidates: {dict(cstat)}", f"- Research index: {dict(rstat)}",
              f"- Movie-ready (music DNA + movement DNA + episode brief from sources): {sum(1 for v in rindex.values() if v.get('movie_ready'))} of {sum(1 for v in rindex.values() if v.get('status') == 'researched')} researched",
              f"- QC gates: {dict(qstat)}", "",
              "## Last runs"]
    for stage in ("audit", "discover", "research", "qc", "hero_qc", "build", "sync", "report"):
        r = last.get(stage)
        if r:
            lines += [f"- **{stage}** {r['finished']} · {json.dumps(r['counters'])}" + (f" · errors: {len(r['errors'])}" if r.get("errors") else "")]
    errs = [e for r in runs[-12:] for e in (r.get("errors") or [])]
    if errs:
        lines += ["", "## Recent errors (last 12 runs)"] + [f"- {e}" for e in errs[-25:]]
    open("STATUS.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    # review queue
    q = ["# QC review queue", f"_Generated {now_iso()}_", "", "| slug | gate | score | reasons | duplicate of |", "|---|---|---|---|---|"]
    items = []
    for slug, v in qindex.items():
        if v.get("publish_gate") in ("review", "reject"):
            full = jload(os.path.join(QC_DIR, slug + ".json")) or {}
            items.append((slug, v.get("publish_gate"), v.get("qc_score"), ", ".join(v.get("reasons") or [])[:160], ((full.get("duplicate_of") or {}).get("slug") or "")))
    items.sort(key=lambda x: (x[1] != "reject", -(x[2] or 0)))
    for it in items[:300]:
        q.append("| " + " | ".join(str(x) for x in it) + " |")
    gone = [(s, v) for s, v in audit.items() if v.get("decision") in ("retire", "merge")]
    arev = [(s, v) for s, v in audit.items() if v.get("decision") == "review"]
    if arev:
        q += ["", f"## Audit: possible duplicates kept live, need a human ({len(arev)})", "", "| slug | other | reason |", "|---|---|---|"] + [f"| {s} | {v.get('into') or ''} | {str(v.get('reason') or '')[:110]} |" for s, v in sorted(arev)[:300]]
    if gone:
        q += ["", f"## Retired or merged by the catalogue audit ({len(gone)})", "", "| slug | decision | into | reason |", "|---|---|---|---|"] + [f"| {s} | {v.get('decision')} | {v.get('into') or ''} | {str(v.get('reason') or '')[:100]} |" for s, v in sorted(gone)[:400]]
    dups = [(s, v) for s, v in cands.items() if v.get("status") == "duplicate_of"]
    if dups:
        q += ["", "## Possible duplicates found in discovery", "", "| candidate | existing | score |", "|---|---|---|"] + [f"| {s} | {v.get('duplicate_of')} | {v.get('score')} |" for s, v in dups[:200]]
    open("QC_REPORT.md", "w", encoding="utf-8").write("\n".join(q) + "\n")
    # push to Supabase if the tables exist
    if sb.enabled:
        try:
            if sb.columns("pipeline_runs"):
                sb.insert("pipeline_runs", [{"run_date": today(), "stage": r["stage"], "started_at": r["started"], "finished_at": r["finished"], "counters": r["counters"], "errors": r["errors"], "version": PIPELINE_VERSION} for r in runs[-8:]], ignore_duplicates=True)
            if sb.columns("qc_queue"):
                sb.upsert("qc_queue", [{"slug": s, "gate": g, "score": sc, "reasons": rs, "duplicate_of": d or None, "updated_at": now_iso()} for s, g, sc, rs, d in items[:500]], on_conflict="slug")
        except Exception as e:
            rep.error(f"push report tables: {e}")
    rep.inc("review_items", len(items))
    log("\n".join(lines))
    return rep.finish()

"""Sync QC'd research into Supabase.

Rules (so curated work is never clobbered):
* Existing dances: the researched material is ADDED (profile_long, research
  sections, teaching, albums, images, sources, aliases, lineage edges, qc).
  Card text (tagline/insight/profile) is replaced only when the dance was not
  yet content_ready AND the QC gate is "publish".  Null facts (era, region,
  coordinates, wikipedia/wikidata ids, UNESCO ref) are filled, never overwritten.
  A sacred detection sets is_sacred/needs_eyes_on to true, never back to false.
* New dances (from discovery): inserted with publish_gate = QC gate
  ("publish" → live; "review" → stored but gated); "reject" is not inserted.
* Hero video ids are never touched here (push_videos.yml owns them).
Columns that do not exist yet in the database are dropped silently, so the
sync works before and after the SQL migration in pipeline/sql/.
"""
import os, json
from .common import Supabase, log, warn, norm, now_iso, jload, Report, load_state, save_state, PIPELINE_VERSION
from .catalog import load_catalog, NameIndex, completeness
from .taxonomy import country_lookup
from .research import RESULTS_DIR
from .qc import QC_DIR

def _fill(row, key, val):
    if val not in (None, "", [], {}) and row.get(key) in (None, "", [], {}):
        return {key: val}
    return {}

def build_payload(rec, qc, existing):
    p = rec.get("profile") or {}
    gate = qc.get("publish_gate")
    sacred = bool(qc.get("is_sacred"))
    research = {"sections": p.get("sections"), "teaching": p.get("teaching"), "gaps": p.get("gaps"), "confidence": p.get("confidence"),
                "claims": [{"text": c.get("text"), "source": c.get("source"), "supported": c.get("supported")} for c in (rec.get("claims") or [])][:60],
                "citation": rec.get("citation"), "researched_at": rec.get("researched_at"), "version": PIPELINE_VERSION}
    images = [{"url": i.get("url"), "thumb": i.get("thumb"), "width": i.get("width"), "height": i.get("height"), "license": i.get("license"),
               "license_url": i.get("license_url"), "attribution": i.get("attribution"), "source_page": i.get("source_page"), "description": i.get("description")} for i in (rec.get("images") or [])]
    # verdict + evidence are always recorded; reader-facing text, albums and images only when QC says publish
    payload = {
        "research": research, "research_gate": gate, "qc": {"score": qc.get("qc_score"), "gate": gate, "reasons": qc.get("reasons"), "gates": [g for g in (qc.get("gates") or []) if not g.get("ok")], "judge": (qc.get("judge") or {}), "at": qc.get("qc_at"), "version": PIPELINE_VERSION},
        "qc_score": qc.get("qc_score"), "last_researched_at": rec.get("researched_at"), "pipeline_version": PIPELINE_VERSION,
    }
    if gate == "publish":
        payload.update({"profile_long": p.get("profile_long"), "albums": rec.get("albums") or [], "album_candidates": rec.get("album_candidates") or [], "images": images})
        upgrade = (existing is None) or (existing.get("tier") != "content_ready") or not (existing.get("profile") or "").strip()
        if upgrade:
            payload.update({"tagline": p.get("tagline"), "insight": p.get("insight"), "profile": p.get("profile"), "tier": "content_ready"})
            if existing is None or existing.get("publish_gate") in (None, "", "review"):
                payload["publish_gate"] = "publish"
        ex = existing or {}
        iso, region_guess = country_lookup(p.get("country") or ex.get("country") or "")
        for k, v in (("era", p.get("era")), ("country", p.get("country")), ("country_code", rec.get("country_code") or iso),
                     ("region", rec.get("region") or region_guess), ("wikipedia_url", rec.get("wikipedia_url")), ("wikidata_qid", rec.get("wikidata_qid")),
                     ("ich_ref", rec.get("unesco_ref")), ("name", p.get("name"))):
            payload.update(_fill(ex, k, v))
        if rec.get("coords") and ex.get("lat") in (None, ""):
            payload["lat"], payload["lng"] = rec["coords"].get("lat"), rec["coords"].get("lng")
        if rec.get("unesco_ref") or p.get("unesco"):
            payload["unesco"] = True
        if rec.get("family") and not ex.get("form_id"):
            payload["form_id"] = rec["family"]
    if sacred:
        payload["is_sacred"] = True
        payload["needs_eyes_on"] = True
        if p.get("sacred_note"):
            payload["sacred_note"] = p.get("sacred_note")
    return payload

def run(only=None, max_n=300):
    rep = Report("sync")
    sb = Supabase()
    if not sb.enabled:
        rep.error("SUPABASE_URL/SUPABASE_SERVICE_KEY missing")
        return rep.finish()
    cols = sb.columns("dances")
    rep.note(f"dances columns known: {len(cols)}; pipeline columns present: {[c for c in ('profile_long','research','albums','images','qc','research_gate') if c in cols]}")
    catalog = load_catalog(sb)
    idx = NameIndex(catalog)
    db_rows = {r["slug"]: r for r in sb.select("dances", select=sb.safe_select("dances", "id,slug,name,tier,publish_gate,profile,lat,era,country,country_code,region,wikipedia_url,wikidata_qid,form_id,is_sacred"), order="slug.asc")}
    qindex = load_state("qc_index.json", {})
    sindex = load_state("sync_index.json", {})
    todo = [s for s, q in qindex.items() if (not only or s in only) and (sindex.get(s, {}).get("qc_at") != q.get("qc_at"))][:max_n]
    rep.note(f"sync targets: {len(todo)}")
    for slug in todo:
        rec = jload(os.path.join(RESULTS_DIR, slug + ".json"))
        qc = jload(os.path.join(QC_DIR, slug + ".json"))
        if not rec or not qc:
            continue
        gate = qc.get("publish_gate")
        existing = db_rows.get(slug)
        try:
            if existing is None and gate == "reject":
                rep.inc("skipped_reject_new"); sindex[slug] = {"qc_at": qc["qc_at"], "action": "skipped_reject"}; continue
            payload = build_payload(rec, qc, existing)
            if existing is None:
                p = rec.get("profile") or {}
                row = dict(payload, slug=slug, name=p.get("name") or rec.get("name") or slug, country=p.get("country"), tagline=p.get("tagline"), insight=p.get("insight"),
                           profile=p.get("profile"), era=p.get("era"), region=rec.get("region"), country_code=rec.get("country_code"), wikipedia_url=rec.get("wikipedia_url"),
                           wikidata_qid=rec.get("wikidata_qid"), publish_gate=("publish" if gate == "publish" else "review"), tier=("content_ready" if gate == "publish" else "needs_curation"),
                           source_profile="pipeline_" + PIPELINE_VERSION, confidence=(p.get("confidence") or 0.5), is_sacred=bool(qc.get("is_sacred")), needs_eyes_on=bool(qc.get("is_sacred")) or gate != "publish")
                if rec.get("coords"):
                    row["lat"], row["lng"] = rec["coords"].get("lat"), rec["coords"].get("lng")
                sb.upsert("dances", [row], on_conflict="slug")
                rep.inc("inserted_" + row["publish_gate"]); action = "inserted"
                got = sb.select("dances", select="id,slug", filters=["slug=eq." + slug], limit=1)
                existing = got[0] if got else None
                if existing:
                    db_rows[slug] = existing
            else:
                n = sb.patch("dances", {"slug": slug}, payload)
                rep.inc("patched" if n else "patch_nomatch"); action = "patched"
            # children
            did = (existing or {}).get("id")
            if did:
                p = rec.get("profile") or {}
                aliases = [{"dance_id": did, "alias": a.strip()} for a in (p.get("aliases") or []) if a and a.strip() and norm(a) != norm(p.get("name") or "")][:20]
                if aliases:
                    try: sb.upsert("dance_aliases", aliases, on_conflict="dance_id,alias")
                    except Exception as e: rep.error(f"aliases {slug}: {e}")
                srcs = [{"dance_id": did, "url": u, "label": ("Wikipedia" if "wikipedia.org" in u else "Wikidata" if "wikidata.org" in u else "UNESCO" if "unesco.org" in u else "")} for u in (rec.get("sources") or [])][:12]
                if srcs:
                    try: sb.upsert("dance_sources", srcs, on_conflict="dance_id,url")
                    except Exception as e: rep.error(f"sources {slug}: {e}")
                edges = []
                for rel in (p.get("related") or [])[:12]:
                    f, score = idx.find(rel, threshold=0.93)
                    tid = (db_rows.get(f) or {}).get("id") if f else None
                    if tid and tid != did:
                        edges.append({"src_id": did, "dst_id": tid, "relation": "related"})
                if edges:
                    try: sb.upsert("dance_edges", edges, on_conflict="src_id,dst_id,relation")
                    except Exception as e: rep.error(f"edges {slug}: {e}")
            sindex[slug] = {"qc_at": qc["qc_at"], "action": action, "gate": gate, "at": now_iso()}
            log(f"SYNC {slug}: {action} gate={gate}")
        except Exception as e:
            rep.error(f"{slug}: {e}")
        save_state("sync_index.json", sindex)
    # hero QC verdicts
    hq = load_state("hero_qc.json", {})
    if "hero_qc" in cols and hq:
        n = 0
        for slug, e in list(hq.items())[:400]:
            if sindex.get("hero:" + slug) == e.get("checked_at"):
                continue
            try:
                payload = {"hero_qc": {"verdict": e.get("verdict"), "checked_at": e.get("checked_at"), "hero": e.get("hero"), "soft_fail": e.get("soft_fail"), "hard_fail": e.get("hard_fail")}}
                if e.get("remove_from_db"):
                    payload["hero_video_youtube_id"] = None
                sb.patch("dances", {"slug": slug}, payload)
                sindex["hero:" + slug] = e.get("checked_at"); n += 1
            except Exception as ex:
                rep.error(f"hero_qc {slug}: {ex}")
        rep.inc("hero_qc_synced", n)
        save_state("sync_index.json", sindex)
    return rep.finish()

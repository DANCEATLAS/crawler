"""Seed/refresh Supabase `dances` from the app catalogue (app_catalog.json, dw_app_v1).

Fill-only semantics: rows that exist keep every non-null value they already
have (heroes, UNESCO refs, sacred flags, curated text); only empty columns are
filled.  Slugs missing from the database are inserted in full.  Aliases,
sources and related-dance edges are upserted into the child tables.
Run: python -m pipeline.seed_catalog [--dry]
"""
import sys, json, re
from .common import Supabase, log, warn, norm, now_iso, jload, Report
from .catalog import load_app_catalog, NameIndex
from .taxonomy import country_lookup

COLS = ["name", "country", "country_code", "region", "era", "tagline", "profile", "insight", "wikipedia_url", "wikidata_qid", "unesco",
        "lat", "lng", "tier", "publish_gate", "is_sacred", "hero_video_youtube_id", "video_stack", "form_id", "source_profile", "confidence", "updated_at"]

def app_row(s):
    cc = s.get("country_code")
    if not (isinstance(cc, str) and len(cc) == 2):
        cc, _ = country_lookup(s.get("country") or "")
    region = s.get("region")
    if not region and cc:
        _, region = country_lookup(s.get("country") or "")
    row = {"slug": s["slug"], "name": s.get("name"), "country": s.get("country") or None, "country_code": cc or None, "region": region or None,
           "era": s.get("era") or None, "tagline": s.get("tagline") or None, "profile": s.get("profile") or None, "insight": s.get("insight") or None,
           "wikipedia_url": s.get("wikipedia_url") or None, "wikidata_qid": s.get("wikidata_qid") or None, "unesco": bool(s.get("unesco")),
           "lat": s.get("lat"), "lng": s.get("lng"), "tier": s.get("tier") or None, "publish_gate": s.get("publish_gate") or None,
           "is_sacred": bool(s.get("is_sacred") or s.get("_is_sacred")), "hero_video_youtube_id": s.get("hero_video_youtube_id") or None,
           "video_stack": s.get("video_stack") or None, "form_id": s.get("family") or s.get("form_id") or None,
           "source_profile": "app_catalog_1014", "confidence": 0.7 if s.get("tier") == "content_ready" else 0.5, "updated_at": s.get("updated_at") or None}
    return row

def run(dry=False):
    rep = Report("seed_catalog")
    sb = Supabase()
    styles = load_app_catalog()
    if not styles:
        rep.error("app_catalog.json missing or empty"); return rep.finish()
    rep.note(f"app catalogue: {len(styles)} styles")
    if not sb.enabled:
        rep.error("no Supabase credentials"); return rep.finish()
    cols = sb.columns("dances")
    rep.note(f"db columns: {len(cols)}")
    existing = {r["slug"]: r for r in sb.select("dances", select="*", order="slug.asc")}
    rep.note(f"db rows before: {len(existing)}")
    inserts, patches = [], 0
    for s in styles:
        row = {k: v for k, v in app_row(s).items() if (not cols or k in cols or k == "slug")}
        ex = existing.get(s["slug"])
        if ex is None:
            inserts.append(row)
            continue
        fill = {k: v for k, v in row.items() if k != "slug" and v not in (None, "", [], {}) and ex.get(k) in (None, "", [], {})}
        # never overwrite booleans that are already true; never set unesco false over true
        for b in ("is_sacred", "unesco"):
            if b in fill and ex.get(b) is True:
                fill.pop(b)
        if fill:
            if dry:
                log("PATCH", s["slug"], list(fill)); patches += 1
            else:
                try:
                    n = sb.patch("dances", {"slug": s["slug"]}, fill); patches += 1 if n else 0
                except Exception as e:
                    rep.error(f"patch {s['slug']}: {e}")
    rep.inc("patched", patches)
    if inserts:
        rep.note(f"inserting {len(inserts)} new rows")
        if not dry:
            try:
                sb.upsert("dances", inserts, on_conflict="slug")
                rep.inc("inserted", len(inserts))
            except Exception as e:
                rep.error(f"insert batch: {e}")
                # fall back to one-by-one to isolate bad rows
                for r in inserts:
                    try: sb.upsert("dances", [r], on_conflict="slug"); rep.inc("inserted")
                    except Exception as e2: rep.error(f"insert {r['slug']}: {e2}")
    # children
    rows = {r["slug"]: r for r in sb.select("dances", select="id,slug,name", order="slug.asc")}
    rep.note(f"db rows after: {len(rows)}")
    idx = NameIndex([{"slug": r["slug"], "name": r.get("name"), "aliases": []} for r in rows.values()] + [{"slug": s["slug"], "name": s.get("name"), "aliases": s.get("aliases") or []} for s in styles])
    aliases, sources, edges = [], [], []
    for s in styles:
        did = (rows.get(s["slug"]) or {}).get("id")
        if not did:
            continue
        for a in (s.get("aliases") or [])[:20]:
            if isinstance(a, str) and a.strip() and norm(a) != norm(s.get("name") or ""):
                aliases.append({"dance_id": did, "alias": a.strip()})
        for u in (s.get("sources") or [])[:12]:
            url = u.get("url") if isinstance(u, dict) else u
            if isinstance(url, str) and url.startswith("http"):
                sources.append({"dance_id": did, "url": url, "label": (u.get("title") if isinstance(u, dict) else ("Wikipedia" if "wikipedia.org" in url else "")) or ""})
        for rel in (s.get("related") or [])[:12]:
            name = rel.get("name") if isinstance(rel, dict) else rel
            f, score = idx.find(name or "", threshold=0.93)
            tid = (rows.get(f) or {}).get("id") if f else None
            if tid and tid != did:
                edges.append({"src_id": did, "dst_id": tid, "relation": "related"})
    def dedupe(lst, keys):
        seen, out = set(), []
        for r in lst:
            k = tuple(r[x] for x in keys)
            if k not in seen:
                seen.add(k); out.append(r)
        return out
    aliases, sources, edges = dedupe(aliases, ("dance_id", "alias")), dedupe(sources, ("dance_id", "url")), dedupe(edges, ("src_id", "dst_id", "relation"))
    rep.note(f"children: aliases={len(aliases)} sources={len(sources)} edges={len(edges)}")
    if not dry:
        for table, lst, oc in (("dance_aliases", aliases, "dance_id,alias"), ("dance_sources", sources, "dance_id,url"), ("dance_edges", edges, "src_id,dst_id,relation")):
            try:
                sb.upsert(table, lst, on_conflict=oc); rep.inc(table, len(lst))
            except Exception as e:
                rep.error(f"{table}: {e}")
    return rep.finish()

if __name__ == "__main__":
    sys.exit(0 if run(dry="--dry" in sys.argv) else 1)

"""Publish the QC-gated catalogue the website loads (served from raw.githubusercontent.com).

Inputs
  app_catalog.json        the website's current dataset (dw_app_v1; downloaded by `bootstrap`)
  hero_results.json       crawler hero picks (+ hero QC replacements)
  pipeline_state/hero_qc.json
  tutorial_results.json   crawler tutorial picks
  research_results/*.json + qc_results/*.json   researched profiles and their gates

Outputs (public/catalog/)
  dances.app.json   dw_app_v1 — same contract the app reads today, plus the new fields
  profiles_v2.json  rich sections / teaching / claims per slug (only research_gate == publish)
  stats.json        counts for the status page
  retired.json      slugs the app must hide (rejected after review)

Policy: nothing researched reaches the site unless QC says "publish"; a dance already
published by the app keeps its card text unless it was still "needs_curation".
Refuses to publish if the catalogue would shrink by more than 10 % (ALLOW_SHRINK=true overrides).
"""
import os, json
from collections import Counter
from .common import log, warn, norm, now_iso, jload, jsave, load_state, Report, PIPELINE_VERSION
from .catalog import load_app_catalog, NameIndex
from .taxonomy import country_lookup, FAMILIES
from .research import RESULTS_DIR
from .qc import QC_DIR
from .sync import build_payload

CATALOG_DIR = os.environ.get("CATALOG_DIR", "public/catalog")
SACRED_SLUGS = set()

def _flag(cc):
    if not cc or len(cc) != 2 or not cc.isalpha():
        return None
    return "".join(chr(0x1F1E6 + ord(c.upper()) - ord("A")) for c in cc)

def run(include_review=False):
    rep = Report("build")
    app = {s["slug"]: dict(s) for s in load_app_catalog()}
    if not app:
        rep.error("app_catalog.json missing — run bootstrap first"); return rep.finish()
    heroes = jload("hero_results.json", {}) or {}
    hq = load_state("hero_qc.json", {})
    tutorials = jload("tutorial_results.json", {}) or {}
    qindex = load_state("qc_index.json", {})
    styles = {}
    v2 = {}
    retired = []
    counters = Counter()
    audit = load_state("audit.json", {})
    gone = {k: v for k, v in audit.items() if v.get("decision") in ("retire", "merge")}
    # 1. existing app dances
    for slug, s in app.items():
        if slug in gone:
            retired.append({"slug": slug, "reason": gone[slug].get("reason"), "merged_into": gone[slug].get("into")}); counters["retired_by_audit"] += 1
            continue
        st = dict(s)
        # aliases of entries merged into this one
        for other, g in gone.items():
            if g.get("into") == slug and other in app:
                for a in [app[other].get("name")] + list(app[other].get("aliases") or []):
                    if a and norm(a) != norm(st.get("name") or "") and norm(a) not in {norm(x) for x in (st.get("aliases") or [])}:
                        st["aliases"] = list(st.get("aliases") or []) + [a]
        # hero: crawler wins; a QC-removed hero is dropped
        h = heroes.get(slug) or {}
        e = hq.get(slug) or {}
        if h.get("hero_video_youtube_id"):
            st["hero_video_youtube_id"] = h["hero_video_youtube_id"]
            if h.get("video_stack"):
                st["video_stack"] = h["video_stack"]
            st["hero_source"] = "crawler:" + str(h.get("status") or "")
        elif e.get("remove_from_db"):
            st["hero_video_youtube_id"] = None
        if e:
            st["hero_qc"] = {"verdict": e.get("verdict"), "checked_at": e.get("checked_at"), "soft_fail": e.get("soft_fail")}
        t = tutorials.get(slug) or {}
        if isinstance(t, dict) and t.get("lessons") and not (s.get("_is_sacred") or s.get("is_sacred")):
            st["tutorials"] = t["lessons"]
        styles[slug] = st
    # 2. researched profiles (existing or new)
    for slug, q in qindex.items():
        gate = q.get("publish_gate")
        rec = jload(os.path.join(RESULTS_DIR, slug + ".json"))
        qc = jload(os.path.join(QC_DIR, slug + ".json"))
        if not rec or not qc:
            continue
        p = rec.get("profile") or {}
        existing = styles.get(slug)
        if slug in gone:
            continue
        if existing is None and gate == "reject":
            counters["new_rejected_hidden"] += 1; continue
        if existing is None and gate == "review" and not include_review:
            counters["new_review_hidden"] += 1; continue
        if existing is not None and gate == "reject":
            counters["existing_research_rejected"] += 1
        payload = build_payload(rec, qc, {"tier": (existing or {}).get("tier"), "profile": (existing or {}).get("profile"), "publish_gate": (existing or {}).get("publish_gate"),
                                          "era": (existing or {}).get("era"), "country": (existing or {}).get("country"), "country_code": (existing or {}).get("country_code"),
                                          "region": (existing or {}).get("region"), "wikipedia_url": (existing or {}).get("wikipedia_url"), "wikidata_qid": (existing or {}).get("wikidata_qid"),
                                          "lat": (existing or {}).get("lat"), "form_id": (existing or {}).get("family"), "is_sacred": (existing or {}).get("_is_sacred")} if existing is not None else None)
        if existing is None:
            iso, region_guess = country_lookup(p.get("country") or "")
            st = {"slug": slug, "name": p.get("name") or rec.get("name") or slug, "country": p.get("country"), "country_code": rec.get("country_code") or iso,
                  "region": rec.get("region") or region_guess, "family": rec.get("family"), "flag_emoji": _flag(rec.get("country_code") or iso), "era": p.get("era"),
                  "tagline": p.get("tagline"), "profile": p.get("profile"), "insight": p.get("insight"), "aliases": p.get("aliases") or [], "related": p.get("related") or [],
                  "sources": rec.get("sources") or [], "wikipedia_url": rec.get("wikipedia_url"), "wikidata_qid": rec.get("wikidata_qid"), "unesco": bool(p.get("unesco") or rec.get("unesco_ref")),
                  "hero_video_youtube_id": (heroes.get(slug) or {}).get("hero_video_youtube_id"), "video_stack": (heroes.get(slug) or {}).get("video_stack") or [],
                  "image_significance": None, "lat": (rec.get("coords") or {}).get("lat"), "lng": (rec.get("coords") or {}).get("lng"),
                  "tier": "content_ready" if gate == "publish" else "needs_curation", "publish_gate": "publish" if gate == "publish" else "review",
                  "_is_sacred": bool(qc.get("is_sacred")), "is_sacred": bool(qc.get("is_sacred")), "updated_at": rec.get("researched_at", "")[:10], "origin": "pipeline"}
            counters["new_" + gate] += 1
        else:
            st = existing
            counters["existing_" + gate] += 1
        # apply additive payload (no hero fields in payload)
        for k, v in payload.items():
            if k in ("research", "qc"):  # keep heavy stuff out of the app contract; it goes to profiles_v2 / qc_results
                continue
            if k == "form_id":
                st["family"] = v; continue
            st[k] = v
        st["research_gate"] = gate
        if gate == "publish":
            st["sources"] = list(dict.fromkeys(list(st.get("sources") or []) + list(rec.get("sources") or [])))
            merged_aliases = list(st.get("aliases") or [])
            for a in (p.get("aliases") or []):
                if a and norm(a) not in {norm(x) for x in merged_aliases} and norm(a) != norm(st.get("name") or ""):
                    merged_aliases.append(a)
            st["aliases"] = merged_aliases[:20]
            if not st.get("flag_emoji") and st.get("country_code"):
                st["flag_emoji"] = _flag(st["country_code"])
            v2[slug] = {"sections": p.get("sections"), "teaching": p.get("teaching"), "claims": [{"text": c.get("text"), "source": c.get("source")} for c in (rec.get("claims") or []) if c.get("supported")][:60],
                        "citation": rec.get("citation"), "albums": rec.get("albums"), "images": rec.get("images"), "gaps": p.get("gaps"), "confidence": p.get("confidence"),
                        "researched_at": rec.get("researched_at"), "qc_score": qc.get("qc_score")}
        styles[slug] = st
    # retired: existing app dances whose research+QC concluded duplicate/reject AND judge says reject (conservative: only explicit duplicates)
    for slug, q in qindex.items():
        qc = jload(os.path.join(QC_DIR, slug + ".json")) or {}
        d = qc.get("duplicate_of")
        if d and slug in app and qc.get("publish_gate") == "reject":
            retired.append({"slug": slug, "duplicate_of": d.get("slug"), "score": d.get("score")})
    # resolve related names -> slugs where possible (app uses names today; keep names, add related_slugs)
    idx = NameIndex([{"slug": s, "name": st.get("name"), "aliases": st.get("aliases") or []} for s, st in styles.items()])
    for slug, st in styles.items():
        rs = []
        for r in (st.get("related") or [])[:14]:
            name = r.get("name") if isinstance(r, dict) else r
            f, sc = idx.find(name or "", threshold=0.93)
            if f and f != slug and f not in rs:
                rs.append(f)
        st["related_slugs"] = rs
    # shrink guard
    prev = jload(os.path.join(CATALOG_DIR, "stats.json"), {}) or {}
    prev_n = int(prev.get("count") or 0)
    if prev_n and len(styles) < 0.9 * prev_n and os.environ.get("ALLOW_SHRINK") != "true":
        rep.error(f"refusing to publish: catalogue would shrink {prev_n} -> {len(styles)}"); return rep.finish()
    gen = now_iso()
    jsave(os.path.join(CATALOG_DIR, "dances.app.json"), {"contract": "dw_app_v1", "count": len(styles), "generated_at": gen, "pipeline": PIPELINE_VERSION, "styles": styles})
    jsave(os.path.join(CATALOG_DIR, "profiles_v2.json"), {"schema": "dw_profiles_v2", "count": len(v2), "generated_at": gen, "profiles": v2})
    jsave(os.path.join(CATALOG_DIR, "retired.json"), {"generated_at": gen, "retired": retired})
    stats = {"generated_at": gen, "count": len(styles), "with_hero": sum(1 for s in styles.values() if s.get("hero_video_youtube_id")),
             "hero_qc_pass": sum(1 for s in styles.values() if (s.get("hero_qc") or {}).get("verdict") == "pass"),
             "deep_profiles": len(v2), "with_albums": sum(1 for s in styles.values() if s.get("albums")), "with_images": sum(1 for s in styles.values() if s.get("images")),
             "with_tutorials": sum(1 for s in styles.values() if s.get("tutorials")), "content_ready": sum(1 for s in styles.values() if s.get("tier") == "content_ready"),
             "new_from_pipeline": sum(1 for s in styles.values() if s.get("origin") == "pipeline"), "retired": len(retired), "counters": dict(counters), "pipeline": PIPELINE_VERSION}
    jsave(os.path.join(CATALOG_DIR, "stats.json"), stats)
    for k, v in counters.items():
        rep.inc(k, v)
    rep.note(f"catalogue built: {stats}")
    return rep.finish()

def regen_dance_list():
    """Hand every catalogue dance (incl. new ones) to the crawler; reset slugs whose hero was removed."""
    cat = jload(os.path.join(CATALOG_DIR, "dances.app.json"), {}) or {}
    styles = cat.get("styles") or {}
    if not styles:
        warn("no catalogue to build dance_list from"); return 0
    cache = jload("crawler_cache.json", {}) or {}
    hq = load_state("hero_qc.json", {})
    rows, reset = [], 0
    for slug, s in sorted(styles.items()):
        has_hero = bool(s.get("hero_video_youtube_id"))
        rows.append({"slug": slug, "name": s.get("name") or slug, "aliases": [a for a in (s.get("aliases") or []) if isinstance(a, str)][:8],
                     "wikipedia": s.get("wikipedia_url") or "", "country": s.get("country") or "", "publish": s.get("publish_gate") != "reject",
                     "has_hero": has_hero, "is_sacred": bool(s.get("_is_sacred") or s.get("is_sacred"))})
        if not has_hero and (hq.get(slug) or {}).get("remove_from_db") and slug in cache:
            cache.pop(slug, None); reset += 1
    jsave("dance_list.json", rows)
    if reset:
        jsave("crawler_cache.json", cache)
    log(f"dance_list.json: {len(rows)} entries, {sum(1 for r in rows if not r['has_hero'])} without hero, cache reset {reset}")
    return len(rows)

def bootstrap():
    """Make sure app_catalog.json exists (download from the app when missing)."""
    from .catalog import APP_CATALOG
    if os.path.exists(APP_CATALOG):
        return True
    url = os.environ.get("APP_CATALOG_URL", "").strip()
    if not url:
        warn("app_catalog.json missing and APP_CATALOG_URL not set"); return False
    try:
        from .common import http
        st, txt, _ = http(url, timeout=120)
        j = json.loads(txt)
        n = len(j.get("styles") or {}) if isinstance(j, dict) else len(j)
        if n < 500:
            warn("downloaded catalogue looks wrong", n); return False
        open(APP_CATALOG, "w", encoding="utf-8").write(txt)
        log(f"bootstrap: downloaded app catalogue ({n} styles)")
        return True
    except Exception as e:
        warn("bootstrap download failed", e); return False

"""The canonical catalogue: Supabase `dances` first, the app JSON (app_catalog.json) as fallback/overlay.

Also computes the completeness score that drives the enrichment queue and
builds the name/alias index used for duplicate detection.
"""
import os, json
from .common import Supabase, norm, slugify, similarity, log, warn, jload

APP_CATALOG = os.environ.get("APP_CATALOG", "app_catalog.json")

DANCE_COLS = ("slug,name,country,country_code,region,era,tagline,profile,insight,wikipedia_url,wikidata_qid,unesco,ich_ref,"
              "is_sacred,needs_eyes_on,lat,lng,hero_video_youtube_id,video_stack,tutorials,form_id,tier,publish_gate,"
              "confidence,updated_at")

def load_app_catalog():
    j = jload(APP_CATALOG)
    if not j:
        return []
    styles = j.get("styles") if isinstance(j, dict) else j
    if isinstance(styles, dict):
        styles = list(styles.values())
    return [s for s in (styles or []) if isinstance(s, dict) and s.get("slug")]

def load_catalog(sb=None, prefer_db=True):
    """Return list of dance dicts keyed by slug (db rows overlaid on app rows)."""
    sb = sb or Supabase()
    app = {d["slug"]: d for d in load_app_catalog()}
    rows = {}
    if prefer_db and sb.enabled:
        try:
            sel = sb.safe_select("dances", DANCE_COLS)
            try:
                db = sb.select("dances", select=sel + ",dance_aliases(alias)", order="slug.asc")
            except Exception as e:
                warn("alias embed failed, loading without aliases:", e)
                db = sb.select("dances", select=sel, order="slug.asc")
            for r in db:
                r["aliases"] = [a.get("alias") for a in (r.pop("dance_aliases", None) or []) if a.get("alias")]
                rows[r["slug"]] = r
            log(f"catalog: {len(rows)} dances from Supabase, {len(app)} in app json")
        except Exception as e:
            warn("catalog db load failed; falling back to app json:", e)
            rows = {}
    if not rows:
        return list(app.values())
    out = []
    for slug, r in rows.items():
        a = app.get(slug) or {}
        merged = dict(a)
        merged.update({k: v for k, v in r.items() if v not in (None, "", [], {})})
        merged.setdefault("aliases", a.get("aliases") or [])
        if not merged.get("aliases") and a.get("aliases"):
            merged["aliases"] = a["aliases"]
        out.append(merged)
    for slug, a in app.items():
        if slug not in rows:
            a = dict(a); a["_db_missing"] = True
            out.append(a)
    return out

class NameIndex:
    """Exact + fuzzy lookup over names and aliases of the catalogue."""
    def __init__(self, catalog):
        self.by_slug = {d["slug"]: d for d in catalog}
        self.exact = {}
        for d in catalog:
            for nm in [d.get("name")] + list(d.get("aliases") or []):
                k = norm(nm)
                if k:
                    self.exact.setdefault(k, d["slug"])
            self.exact.setdefault(norm(d["slug"].replace("-", " ")), d["slug"])
        self.names = [(norm(d.get("name")), d["slug"]) for d in catalog if d.get("name")]

    def find(self, name, threshold=0.92):
        k = norm(name)
        if not k:
            return None, 0.0
        if k in self.exact:
            return self.exact[k], 1.0
        sk = slugify(name)
        if sk in self.by_slug:
            return sk, 1.0
        best, bs = None, 0.0
        for n, slug in self.names:
            if abs(len(n) - len(k)) > 12:
                continue
            s = similarity(n, k)
            if s > bs:
                best, bs = slug, s
        if bs >= threshold:
            return best, bs
        return None, bs

def completeness(d, research=None):
    """0..100. Higher = richer, better verified profile. Drives the enrichment queue."""
    r = research or d.get("research") or {}
    s = 0.0
    prof = (d.get("profile_long") or r.get("profile_long") or d.get("profile") or "")
    s += min(20, len(prof) / 150.0)                       # up to 20 for ~3000 chars
    s += 6 if d.get("insight") else 0
    s += 4 if d.get("tagline") else 0
    s += 6 if d.get("wikipedia_url") else 0
    s += 3 if d.get("wikidata_qid") else 0
    s += 5 if d.get("country") else 0
    s += 3 if d.get("region") else 0
    s += 3 if d.get("era") else 0
    s += 3 if (d.get("lat") is not None) else 0
    s += 8 if d.get("hero_video_youtube_id") else 0
    s += 4 if (d.get("hero_qc") or {}).get("verdict") == "pass" else 0
    s += min(8, 2.0 * len(d.get("albums") or r.get("albums") or []))
    s += min(8, 2.0 * len(d.get("images") or r.get("images") or []))
    s += min(6, 2.0 * len(d.get("sources") or []))
    s += min(4, 1.0 * len(d.get("related") or []))
    s += 3 if (d.get("aliases")) else 0
    s += 3 if (d.get("tutorials") or []) else 0
    sections = r.get("sections") or {}
    s += min(10, 1.5 * sum(1 for v in sections.values() if v and len(str(v)) > 200))
    return round(min(100.0, s), 1)

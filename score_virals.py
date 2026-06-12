#!/usr/bin/env python3
# DanceWorld viral scoring v1 - windows all/year/month.
# Signals v1: log-views (external) + decayed crowd votes. v2 adds participation/velocity/trends.
# Pipeline: z-score -> window decay (H=none/90d/10d) -> IMDb shrinkage -> blend -> rank.
# Runs in GitHub Actions with SUPABASE_URL + SUPABASE_SERVICE_KEY.
import os, math, json, urllib.request
from datetime import datetime, timezone

URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
H = {"all": None, "year": 90.0, "month": 10.0}
W_EXT, W_CROWD = 0.55, 0.45
M_PRIOR = 3.0

def api(path, method="GET", body=None, prefer=None):
    req = urllib.request.Request(URL + path, method=method)
    req.add_header("apikey", KEY)
    req.add_header("Authorization", "Bearer " + KEY)
    req.add_header("Content-Type", "application/json")
    if prefer:
        req.add_header("Prefer", prefer)
    data = json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(req, data, timeout=30) as r:
        t = r.read().decode()
        return json.loads(t) if t else None

def decay(ts, h):
    if not ts:
        return 1.0 if h is None else 0.0
    if len(ts) == 10:
        ts = ts + "T00:00:00+00:00"
    if h is None or not ts:
        return 1.0
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(ts.replace("Z", "+00:00"))).total_seconds() / 86400.0
    return 0.5 ** (age / h)

def zs(vals):
    n = len(vals)
    m = sum(vals) / n
    v = sum((x - m) ** 2 for x in vals) / n
    s = v ** 0.5 or 1.0
    return [(x - m) / s for x in vals]

def main():
    ch = api("/rest/v1/viral_challenges?select=slug,views,origin_date,is_dance,danger_flag")
    ch = [c for c in ch if c.get("is_dance") and not c.get("danger_flag")]
    votes = api("/rest/v1/votes?select=target_slug,created_at&target_kind=eq.viral") or []
    today = datetime.now(timezone.utc).date().isoformat()
    for w, h in H.items():
        ext = [math.log1p(c.get("views") or 0) for c in ch]
        crowd = []
        for c in ch:
            vs = [v for v in votes if v["target_slug"] == c["slug"]]
            crowd.append(sum(decay(v["created_at"], h) for v in vs))
        rec = [decay(c.get("origin_date") or "", h) for c in ch]
        ez, cz = zs(ext), zs(crowd)
        raw = [W_EXT * e * rc + W_CROWD * c for e, c, rc in zip(ez, cz, rec)]
        gm = sum(raw) / len(raw)
        scored = []
        for c, r, cr in zip(ch, raw, crowd):
            v = cr + 1.0
            wr = (v / (v + M_PRIOR)) * r + (M_PRIOR / (v + M_PRIOR)) * gm
            scored.append((c["slug"], wr))
        scored.sort(key=lambda x: -x[1])
        prev = {r["slug"]: r for r in api("/rest/v1/viral_scores?select=slug,rank,peak_rank,weeks_on&chart_window=eq." + w)}
        rows = []
        for i, (slug, sc) in enumerate(scored, 1):
            p = prev.get(slug, {})
            rows.append({"slug": slug, "chart_window": w, "score": round(sc, 4), "rank": i,
                         "prev_rank": p.get("rank"), "peak_rank": min(i, p.get("peak_rank") or i),
                         "weeks_on": (p.get("weeks_on") or 0) + 1})
        api("/rest/v1/viral_scores", method="POST", body=rows, prefer="resolution=merge-duplicates")
        api("/rest/v1/viral_chart_history", method="POST",
            body=[{"slug": r["slug"], "chart_window": w, "period_date": today, "rank": r["rank"], "score": r["score"]} for r in rows],
            prefer="resolution=merge-duplicates")
        print(w, "->", scored[0][0], "is no.1 of", len(scored))

if __name__ == "__main__":
    main()

"""Hero-video quality gate (the "shaky-cam / dance not visible" problem).

For every hero the crawler picked (hero_results.json) we check, within a daily
budget: YouTube metadata (embeddable, public, HD, sane duration, not a music
video / movie / lyric clip), the title/description naming the dance, and a
vision check of the actual frame (maxresdefault thumbnail) by a multimodal
model.  Failing heroes go to hero_blocklist.json (which crawler.py already
respects) and the best passing challenger is promoted in place.
Dead or unembeddable heroes are evicted from crawler_cache.json so the daily
crawl searches again.
"""
import os, re, json, base64, subprocess, shutil, time
from .common import LLM, log, warn, norm, now_iso, jload, jsave, Report, load_state, save_state, http, get_bytes, HttpError

YT_KEYS = [k.strip() for k in os.environ.get("YT_API_KEYS", "").split(",") if k.strip()]
SONGHARD = re.compile(r"(official\s*(video|audio|music)|\blyric|vevo|-\s*topic|\bremix\b|karaoke|instrumental|full\s*song|\bcover\b|prod\.|\bft\.|feat\.)", re.I)
MOVIE = re.compile(r"(movieclips|netflix|\bmovie\b|\bfilm\b|trailer|full\s*episode|cartoon)", re.I)
VISION_PROMPT = """You check a video thumbnail for an encyclopedia of dance. Dance: "{name}" ({country}). Video title: "{title}".
Answer JSON: dance_visible (bool: people clearly dancing or in a dance pose, bodies visible), people_count (int), talking_head (bool), text_poster_or_graphic (bool: mostly text, logo, poster, lyric card, album art), music_video_or_concert_crowd (bool), vertical_phone_video (bool: tall phone framing / black side bars), camera_quality ("professional"|"steady_amateur"|"shaky_or_blurry"|"unclear"), traditional_or_authentic_context (bool), unsafe_or_explicit (bool), looks_like_named_dance ("yes"|"no"|"unsure"), quality (1-10), reason (<=20 words)."""

def _api(path, params):
    import urllib.parse
    last = None
    for k in YT_KEYS or [""]:
        if not k:
            break
        p = dict(params, key=k)
        try:
            st, txt, _ = http("https://www.googleapis.com/youtube/v3/" + path + "?" + urllib.parse.urlencode(p), retries=1)
            return json.loads(txt)
        except HttpError as e:
            last = e
            if e.code in (403, 429):
                continue
            raise
    if last:
        raise last
    return {}

def _isodur(s):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    if not m:
        return 0
    h, mi, se = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + se

def video_meta(ids):
    out = {}
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        try:
            j = _api("videos", {"part": "snippet,contentDetails,statistics,status", "id": ",".join(batch), "maxResults": "50"})
        except Exception as e:
            warn("video_meta", e)
            continue
        for it in j.get("items", []):
            sn, cd, st, stt = it.get("snippet", {}), it.get("contentDetails", {}), it.get("statistics", {}), it.get("status", {})
            out[it["id"]] = {"title": sn.get("title", ""), "channel": sn.get("channelTitle", ""), "desc": (sn.get("description") or "")[:500],
                             "category": str(sn.get("categoryId", "")), "live": sn.get("liveBroadcastContent"), "tags": sn.get("tags") or [],
                             "duration": _isodur(cd.get("duration")), "hd": cd.get("definition") == "hd", "dimension": cd.get("dimension"),
                             "embeddable": bool(stt.get("embeddable")), "privacy": stt.get("privacyStatus"), "made_for_kids": stt.get("madeForKids"),
                             "views": int(st.get("viewCount", 0) or 0), "likes": int(st.get("likeCount", 0) or 0),
                             "thumb": ((sn.get("thumbnails") or {}).get("maxres") or (sn.get("thumbnails") or {}).get("high") or {}).get("url")}
    return out

def ytdlp_dims(vid):
    if not shutil.which("yt-dlp"):
        return None
    try:
        out = subprocess.run(["yt-dlp", "--skip-download", "--no-warnings", "--print", "%(width)s|%(height)s|%(fps)s", "https://www.youtube.com/watch?v=" + vid],
                             capture_output=True, text=True, timeout=60)
        w, h, fps = (out.stdout.strip().split("|") + ["", "", ""])[:3]
        return {"width": int(w) if w.isdigit() else None, "height": int(h) if h.isdigit() else None, "fps": float(fps) if fps.replace(".", "", 1).isdigit() else None}
    except Exception as e:
        return None

def thumbnail_b64(vid):
    for u in (f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg", f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"):
        try:
            raw, ct = get_bytes(u, timeout=30)
            if raw and len(raw) > 2000:
                return base64.b64encode(raw).decode("ascii"), u
        except Exception:
            continue
    return None, None

def name_in(text, names):
    t = norm(text)
    for nm in names:
        n = norm(nm)
        if len(n) <= 4:
            if re.search(r"\b" + re.escape(n) + r"\b", t):
                return True
        elif n and n in t:
            return True
    return False

def check_video(vid, dance, meta, llm, use_vision=True):
    """Returns dict with verdict pass/fail/unknown and the individual checks."""
    checks = {}
    m = meta.get(vid)
    if not m:
        return {"verdict": "fail", "reason": "video_missing", "checks": {"exists": False}}
    names = [dance.get("name") or dance.get("slug")] + list(dance.get("aliases") or [])
    checks["exists"] = True
    checks["embeddable"] = m["embeddable"] and m["privacy"] == "public"
    checks["duration_ok"] = 15 <= m["duration"] <= 2400
    checks["hd"] = m["hd"]
    checks["not_music_video"] = not (m["category"] == "10" and not re.search(r"danc|choreo|baile|danza", m["title"], re.I)) and not SONGHARD.search(m["title"] + " " + m["channel"])
    checks["not_movie"] = not MOVIE.search(m["title"] + " " + m["channel"])
    checks["not_live"] = m["live"] in (None, "none")
    checks["named"] = name_in(m["title"], names) or name_in(m["desc"], names) or name_in(" ".join(m["tags"]), names)
    dims = ytdlp_dims(vid) if os.environ.get("HERO_QC_DIMS") == "1" else None
    if dims and dims.get("width") and dims.get("height"):
        checks["landscape"] = dims["width"] >= dims["height"]
        checks["min_720p"] = dims["height"] >= 720
    vision = None
    if use_vision and llm.enabled:
        b64, url = thumbnail_b64(vid)
        if b64:
            vision = llm.json(VISION_PROMPT.format(name=dance.get("name"), country=dance.get("country") or "", title=m["title"][:120]),
                              "Classify this thumbnail.", strong=False, temperature=0.0, max_tokens=400, image_b64=b64, prefer="gemini")
    if vision:
        checks["dance_visible"] = bool(vision.get("dance_visible"))
        checks["not_talking_head"] = not vision.get("talking_head")
        checks["not_poster"] = not vision.get("text_poster_or_graphic")
        checks["not_vertical"] = not vision.get("vertical_phone_video")
        checks["camera_ok"] = vision.get("camera_quality") in ("professional", "steady_amateur")
        checks["safe"] = not vision.get("unsafe_or_explicit")
        checks["looks_like_dance"] = vision.get("looks_like_named_dance") != "no"
        checks["vision_quality"] = vision.get("quality")
    hard = ["exists", "embeddable", "duration_ok", "not_music_video", "not_movie", "not_live", "safe", "dance_visible", "not_poster", "looks_like_dance"]
    soft = ["hd", "named", "landscape", "min_720p", "not_talking_head", "not_vertical", "camera_ok"]
    hard_fail = [k for k in hard if k in checks and checks[k] is False]
    soft_fail = [k for k in soft if k in checks and checks[k] is False]
    if hard_fail:
        verdict = "fail"
    elif len(soft_fail) >= 3 or ("camera_ok" in soft_fail and "hd" in soft_fail):
        verdict = "fail"
    elif vision is None and len(soft_fail) >= 2:
        verdict = "weak"
    else:
        verdict = "pass"
    return {"verdict": verdict, "hard_fail": hard_fail, "soft_fail": soft_fail, "checks": checks, "vision": vision, "meta": {k: m[k] for k in ("title", "channel", "duration", "hd", "views", "likes")}}

def run(budget=80, recheck_days=120, use_vision=True, only=None):
    rep = Report("hero_qc")
    llm = LLM()
    if not YT_KEYS:
        rep.error("YT_API_KEYS missing; hero QC needs the YouTube Data API")
        return rep.finish()
    heroes = jload("hero_results.json", {}) or {}
    cache = jload("crawler_cache.json", {}) or {}
    block = jload("hero_blocklist.json", {}) or {}
    hq = load_state("hero_qc.json", {})
    dances = {d.get("slug"): d for d in (jload("dance_list.json", []) or [])}
    from .catalog import load_app_catalog
    for d in load_app_catalog():
        dances.setdefault(d["slug"], d)
    # queue: never-checked first, then oldest checks
    slugs = [s for s in heroes if (heroes[s] or {}).get("hero_video_youtube_id")]
    if only:
        slugs = [s for s in slugs if s in only]
    def age_key(s):
        return (hq.get(s) or {}).get("checked_at", "")
    slugs.sort(key=age_key)
    cutoff = _days_ago(recheck_days)
    slugs = [s for s in slugs if not (hq.get(s) or {}).get("checked_at") or (hq.get(s) or {}).get("checked_at", "")[:10] < cutoff][:budget]
    rep.note(f"hero qc targets: {len(slugs)} of {len(heroes)} heroes (vision={use_vision and llm.enabled})")
    # prefetch metadata for heroes + challengers
    ids = []
    for s in slugs:
        h = heroes[s]
        ids.append(h["hero_video_youtube_id"])
        ids += [x.get("youtube_id") for x in (h.get("video_stack") or []) if x.get("youtube_id")]
        ids += list(h.get("challengers") or [])
    meta = video_meta(list(dict.fromkeys(i for i in ids if i)))
    rep.inc("videos_fetched", len(meta))
    for s in slugs:
        h = heroes[s]
        d = dances.get(s) or {"slug": s, "name": s.replace("-", " ")}
        vid = h["hero_video_youtube_id"]
        try:
            res = check_video(vid, d, meta, llm, use_vision)
        except Exception as e:
            rep.error(f"{s}/{vid}: {e}")
            continue
        entry = {"checked_at": now_iso(), "hero": vid, "verdict": res["verdict"], "hard_fail": res.get("hard_fail"), "soft_fail": res.get("soft_fail"), "checks": res["checks"], "vision": res.get("vision"), "history": (hq.get(s) or {}).get("history", [])[-5:]}
        rep.inc("verdict_" + res["verdict"])
        if res["verdict"] == "fail":
            block.setdefault(s, {})[vid] = {"reason": ",".join(res.get("hard_fail") or res.get("soft_fail") or ["fail"]), "at": now_iso()}
            # try challengers
            cands = [x.get("youtube_id") for x in (h.get("video_stack") or []) if x.get("youtube_id") and x.get("youtube_id") != vid] + [c for c in (h.get("challengers") or []) if c != vid]
            replacement = None
            for c in dict.fromkeys(cands):
                if c in (block.get(s) or {}):
                    continue
                r2 = check_video(c, d, meta, llm, use_vision)
                if r2["verdict"] == "pass":
                    replacement = (c, r2); break
                elif r2["verdict"] == "fail":
                    block[s][c] = {"reason": ",".join(r2.get("hard_fail") or r2.get("soft_fail") or ["fail"]), "at": now_iso()}
            if replacement:
                c, r2 = replacement
                entry["history"].append({"replaced": vid, "with": c, "at": now_iso(), "reason": entry["hard_fail"] or entry["soft_fail"]})
                m = meta.get(c, {})
                heroes[s] = dict(h, hero_video_youtube_id=c, title=m.get("title", ""), channel=m.get("channel", ""), status="qc_replaced", qc_at=now_iso(),
                                 video_stack=[x for x in (h.get("video_stack") or []) if x.get("youtube_id") not in (block.get(s) or {})])
                for x in heroes[s]["video_stack"]:
                    x["role"] = "hero" if x.get("youtube_id") == c else "rendition"
                entry.update({"hero": c, "verdict": "pass", "checks": r2["checks"], "vision": r2.get("vision"), "replaced_from": vid})
                rep.inc("replaced")
                log(f"HERO-QC {s}: {vid} FAILED ({entry['history'][-1]['reason']}) -> replaced with {c}")
            else:
                # evict so the crawler searches again tomorrow (with the blocklist applied)
                cache.pop(s, None)
                dead = any(k in (res.get("hard_fail") or []) for k in ("exists", "embeddable", "not_live", "safe", "not_music_video"))
                heroes[s] = dict(h, status="qc_failed_pending_recrawl", qc_at=now_iso(), failed_hero=vid,
                                 hero_video_youtube_id=(None if dead else vid))
                entry["remove_from_db"] = dead
                rep.inc("evicted_for_recrawl" + ("_removed" if dead else ""))
                log(f"HERO-QC {s}: {vid} FAILED ({res.get('hard_fail') or res.get('soft_fail')}), no passing challenger -> re-crawl" + (" (hero removed)" if dead else ""))
        else:
            log(f"HERO-QC {s}: {vid} {res['verdict']} soft={res.get('soft_fail')}")
        hq[s] = entry
        save_state("hero_qc.json", hq)
    jsave("hero_results.json", heroes)
    jsave("crawler_cache.json", cache)
    jsave("hero_blocklist.json", block)
    rep.inc("llm_calls", llm.calls)
    return rep.finish()

def _days_ago(n):
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) - timedelta(days=n)).strftime("%Y-%m-%d")

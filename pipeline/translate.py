"""Languages — the atlas speaks to the whole world (MOVIE_PHASE.md, decision 2).

One narrator for the whole atlas, one look, a native voice per language. The master narration of every episode pack is
English (assembled from the sources, optionally polished and verified); this stage translates it, scene by scene, into
the languages in TRANSLATE_LANGS, a few packs a day (TRANSLATE_BUDGET model calls), and keeps the result in
episodes/i18n/<lang>/<slug>.json with exactly the master's structure so a player can switch language on any scene.
What is translated: narration lines only. Dance names, people, places and counts are kept as in the master (the model
is told so and the result is checked: every number and every name in the pronunciation list must survive; a scene that
fails the check keeps the master line, marked). A pack is translated once its Episode 1 has no gaps; when the master is
rebuilt the translations are redone. Everything is marked machine_translated for the day a native reviewer reads it.
"""
import os, re, json, glob
from .common import jload, jsave, log, warn, Report, LLM, now_iso

EPISODE_DIR = "episodes"
I18N_DIR = os.path.join(EPISODE_DIR, "i18n")
DEFAULT_LANGS = "es,fr,de,pt,it,ja,zh,ko,ar,hi,ru,id"
LANG_NAMES = {"es": "Spanish", "fr": "French", "de": "German", "pt": "Portuguese", "it": "Italian", "ja": "Japanese", "zh": "Chinese (Simplified)", "ko": "Korean", "ar": "Arabic",
              "hi": "Hindi", "ru": "Russian", "id": "Indonesian", "tr": "Turkish", "nl": "Dutch", "pl": "Polish", "sv": "Swedish", "vi": "Vietnamese", "th": "Thai", "el": "Greek", "he": "Hebrew",
              "sw": "Swahili", "bn": "Bengali", "ur": "Urdu", "fa": "Persian", "uk": "Ukrainian", "ro": "Romanian", "hu": "Hungarian", "cs": "Czech", "fi": "Finnish", "da": "Danish", "no": "Norwegian"}

SYSTEM = """You translate the narration of a documentary and dance-class script into {lang}, for a studio voice-over read by a native speaker.
Rules: translate ONLY the narration lines, keep every scene code and the number of lines per scene; keep dance names, people's names, place
names, step names and all numbers and counts exactly as written (counts like "1-2-3-4" stay as digits); natural spoken {lang}, present tense,
short sentences, no additions, no omissions, no explanations. Output JSON: {{"scenes": [{{"code": "<code>", "narration": ["..."]}}]}}"""

def _langs():
    return [l.strip().lower() for l in os.environ.get("TRANSLATE_LANGS", DEFAULT_LANGS).split(",") if l.strip()]

def _nums(s):
    return set(re.findall(r"\d+", s))

def _scenes(pack):
    out = [("e1", s) for s in pack["episode_1"]["scenes"]]
    for c in pack.get("chapters") or []:
        out += [(f"c{c['chapter']}", s) for s in c["scenes"]]
    return out

def verify(master_lines, lines, names):
    """A translated scene is accepted when it has the same number of lines, keeps every number, and keeps every proper name
    from the pronunciation list that the master used."""
    if not isinstance(lines, list) or len(lines) != len(master_lines) or not all(isinstance(l, str) and l.strip() for l in lines):
        return False
    m, t = " ".join(master_lines), " ".join(lines)
    if _nums(m) != _nums(t):
        return False
    for n in names:
        if n and n.lower() in m.lower() and n.lower() not in t.lower():
            return False
    return True

def translate_pack(pack, lang, llm):
    scenes = _scenes(pack)
    names = [n for n in (pack.get("voice") or {}).get("pronunciation") or [] if isinstance(n, str)]
    payload = {"language": LANG_NAMES.get(lang, lang), "keep_as_is": names, "scenes": [{"code": f"{where}:{s['code']}", "narration": s["narration"]} for where, s in scenes if s.get("narration")]}
    jd = llm.json(SYSTEM.format(lang=LANG_NAMES.get(lang, lang)), json.dumps(payload, ensure_ascii=False)[:40000], strong=False, temperature=0.2, max_tokens=8000)
    if not jd:
        return None
    got = {x.get("code"): x.get("narration") for x in (jd.get("scenes") or []) if isinstance(x, dict)}
    out, ok_n, fail = [], 0, 0
    for where, s in scenes:
        key = f"{where}:{s['code']}"
        if not s.get("narration"):
            out.append({"where": where, "code": s["code"], "narration": [], "status": "empty"}); continue
        lines = got.get(key)
        if verify(s["narration"], lines, names):
            out.append({"where": where, "code": s["code"], "narration": lines, "status": "translated"}); ok_n += 1
        else:
            out.append({"where": where, "code": s["code"], "narration": s["narration"], "status": "master_kept"}); fail += 1
    return {"slug": pack["slug"], "name": pack["name"], "lang": lang, "language": LANG_NAMES.get(lang, lang), "master_built_at": pack.get("built_at"), "master_polished": bool(pack.get("polished")),
            "translated_at": now_iso(), "machine_translated": True, "reviewed_by_native_speaker": False, "scenes_translated": ok_n, "scenes_master_kept": fail, "scenes": out}

def episode1_ready(pack):
    """Episode 1 without gaps (sacred packs included: their Episode 1 is the whole series)."""
    return not any(s.get("needs") for s in (pack.get("episode_1") or {}).get("scenes") or [])

def pick(budget, langs, only=None):
    """Packs whose Episode 1 is gap-free, complete packs first; for each, the first language still missing or stale."""
    cands = []
    for f in sorted(glob.glob(os.path.join(EPISODE_DIR, "*.json"))):
        pack = jload(f, None)
        if not pack or not pack.get("slug") or (only and pack["slug"] not in only):
            continue
        if not episode1_ready(pack):
            continue
        rank = 0 if pack.get("status") == "complete" else (1 if pack.get("polished") else 2)
        for lang in langs:
            cur = jload(os.path.join(I18N_DIR, lang, pack["slug"] + ".json"), None)
            if cur and cur.get("master_built_at") == pack.get("built_at"):
                continue
            cands.append((rank, langs.index(lang), pack["slug"], lang, pack))
    cands.sort(key=lambda c: (c[0], c[1], c[2]))
    return cands[:budget]

def run(budget=6, only=None):
    rep = Report("translate")
    langs = _langs()
    llm = LLM()
    targets = pick(budget, langs, only=only) if llm.enabled else []
    rep.note(f"languages: {','.join(langs)} · translations to make: {len(targets)} (budget {budget})")
    for rank, _, slug, lang, pack in targets:
        try:
            tr = translate_pack(pack, lang, llm)
            if not tr:
                rep.inc("failed"); continue
            jsave(os.path.join(I18N_DIR, lang, slug + ".json"), tr)
            rep.inc("translated"); rep.inc("scenes_translated", tr["scenes_translated"]); rep.inc("scenes_master_kept", tr["scenes_master_kept"])
            log(f"TRANSLATE {slug} → {lang}: {tr['scenes_translated']} scenes, {tr['scenes_master_kept']} kept in English")
        except Exception as e:
            rep.error(f"translate {slug} {lang}: {e}")
    # index: which languages each pack has (current master only)
    idx_path = os.path.join("public", "catalog", "episodes.json")
    idx = jload(idx_path, None)
    if idx and idx.get("packs"):
        for slug, v in idx["packs"].items():
            have = []
            for lang in langs:
                cur = jload(os.path.join(I18N_DIR, lang, slug + ".json"), None)
                if cur and cur.get("master_built_at") == v.get("built_at"):
                    have.append(lang)
            v["languages"] = have
        idx["languages"] = langs
        idx["translations"] = sum(len(v.get("languages") or []) for v in idx["packs"].values())
        jsave(idx_path, idx)
        rep.note(f"translations on file for the current masters: {idx['translations']} across {len(langs)} languages")
    rep.inc("llm_calls", llm.calls); rep.inc("llm_failures", llm.failures)
    return rep.finish()

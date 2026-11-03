"""Episode packs — the script layer of the atlas (MOVIE_PHASE.md).

For every published profile the machine writes a scene-by-scene pack in ONE formula shared by every style, so a viewer
can jump from dance to dance and always know where they are:
  Episode 1 · Meet the dance        hook · where & when · the occasion · watch it · listen · costume & setting · the people · family tree · one step · close
  Chapter 1 · First steps           welcome · body · count · step A · step B · put it together · mistakes · to the music · close
  Chapter 2 · Building the dance    (same nine scenes, next layer of material)
  Chapter 3 · Dancing it fully      (same nine scenes, the full dance)
Every narration line is assembled from the profile's own source-backed text (sections, music DNA, movement DNA, episode
brief, claims) — the pack never invents a fact; what the sources do not say becomes a gap, not a sentence. A model may
polish the narration (EPISODE_POLISH calls a day); polished text is kept only when it introduces no year, number or
capitalised name that the profile does not contain, otherwise the assembled text stands.
Each pack also carries: the music brief (for an AI composer: original, copyright-free, the same DNA), the visual brief
(licensed images, footage links, the checked hero video, motifs, costume notes), the voice (one narrator for the atlas,
an instructor persona per style), the teaching formula taken from pedagogy/teaching_patterns.json (what the best online
teachers do, see pipeline/pedagogy.py), and the gaps that keep the pack from being complete — they are handed back to the
research queue through pipeline_state/episode_gaps.json.
Outputs: episodes/<slug>.json, episodes/<slug>.md, public/catalog/episodes.json (index), pipeline_state/episode_gaps.json.
Sacred or restricted dances get Episode 1 only (story, music, costume); the chapters are withheld.
"""
import os, re, json, glob
from .common import jload, jsave, load_state, save_state, log, warn, Report, LLM, now_iso, PIPELINE_VERSION
from .research import _said, _said_not, CHECKLIST
from .qc import QC_DIR

EPISODE_DIR = "episodes"
RESEARCH_DIR = "research_results"
PACK_VERSION = "e1"
PLACEHOLDER = ("not described", "not in sources", "not derivable", "withheld", "unknown")

NARRATOR = {"role": "narrator", "name": "The Atlas narrator", "voice": "warm, unhurried, curious; a documentary voice that never oversells; speaks the dance's own words (names, counts) clearly",
            "rule": "The narrator only says what the profile says. Every sentence can be traced to a section, a claim or the music/movement DNA.",
            "identity": "one narrator for the whole atlas: the same face and animation everywhere; a native-speaker voice of the same character per language (studio-grade); the viewer chooses the language",
            "wardrobe": "in each episode the narrator wears the traditional apparel associated with the dance, reconstructed with meticulous care from the profile's costume notes and the licensed images — genuine and respectful, never a caricature; sacred, ceremonial or restricted attire is never worn (the narrator stays in neutral dress with a respectful nod in colour and fabric); the pack's visual_brief.wardrobe says which",
            "languages": "master narration in English; translations per language in episodes/i18n/<lang>/<slug>.json with the same scene structure (pipeline/translate.py); names, places and counts are never translated"}
GAP_LABEL = {"origins_and_history": "the origins & history section", "occasions_and_meaning": "the occasions & meaning section", "how_it_is_danced": "the how-it-is-danced section",
    "music_and_instruments": "the music & instruments section", "costume_and_setting": "the costume & setting section", "notable_figures": "notable figures", "lineage": "lineage",
    "signature_moves": "signature moves", "tempo": "tempo (bpm)", "meter": "meter", "images": "licensed images (3 needed)", "connections": "two or more connections",
    "teaching steps": "teaching steps written out", "posture": "posture, arms and hands", "posture / arms": "posture, arms and hands", "what_to_avoid": "what to avoid / common mistakes", "signature moves": "signature moves"}

INSTRUCTOR_DEFAULT = "a patient, precise instructor who counts out loud, demonstrates from the front and the back, repeats every step slowly three times before speeding up, names mistakes kindly and never rushes"

# ------------------------------------------------------------------ text helpers
def ok(v, n=20):
    s = v.strip() if isinstance(v, str) else ""
    return len(s) >= n and not any(w in s.lower() for w in PLACEHOLDER)

def sentences(text, n=3, max_chars=520):
    """First n sentences of a section (source-backed prose), trimmed for a narration line."""
    if not ok(text):
        return []
    t = text.strip()
    # protect initials and common abbreviations so "Charles E. Johnson" or "St. Louis" is not cut in two
    t = re.sub(r"\b([A-Z])\.\s+(?=[A-Z])", "\\1\u2024 ", t)
    t = re.sub(r"\b(St|Mr|Mrs|Ms|Dr|Prof|Sr|Jr|No|ca|cf|vs)\.\s+", lambda m: m.group(1) + "\u2024 ", t)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(À-ɏ])", t)
    out, total = [], 0
    for p in parts:
        p = p.strip().replace("\u2024", ".")
        if not p:
            continue
        if total + len(p) > max_chars and out:
            break
        out.append(p); total += len(p)
        if len(out) >= n:
            break
    return out

def tempo_bpm(mp):
    m = re.search(r"(\d{2,3})(?:\s*[-–]\s*(\d{2,3}))?", str(mp.get("tempo_bpm") or ""))
    if not m:
        return None
    a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
    v = (a + b) // 2
    return v if 40 <= v <= 240 else None

def counting_for(meter, patterns):
    """Counting scheme: what the studied teachers of this dance/family use; else derived from the meter."""
    if patterns and patterns.get("counting"):
        return patterns["counting"]
    m = (meter or "").strip()
    if re.match(r"^\s*3\s*/\s*4", m) or "waltz" in m.lower():
        return "1-2-3, 2-2-3 (three counts a bar)"
    if re.match(r"^\s*6\s*/\s*8", m):
        return "1-2-3-4-5-6, or quick-quick-slow across the bar"
    if re.match(r"^\s*(2|4)\s*/\s*4", m) or not m or not ok(m, 1):
        return "1-2-3-4 then 5-6-7-8 (eight counts, two bars)"
    return f"count the {m} bar out loud, then in pairs of bars"

def clean_list(xs, n=8):
    out = []
    for x in xs or []:
        s = x if isinstance(x, str) else (x.get("name") or x.get("description") or "") if isinstance(x, dict) else str(x)
        if ok(s, 3) and s not in out:
            out.append(s.strip())
    return out[:n]

# ------------------------------------------------------------------ the pack
def build_pack(rec, qc, st, patterns):
    """One episode pack from a research record (dict), its QC record, its catalogue entry and the pedagogy patterns."""
    p = rec.get("profile") or {}
    slug, name = rec.get("slug"), p.get("name") or rec.get("name") or rec.get("slug")
    secs, teach = p.get("sections") or {}, p.get("teaching") or {}
    mp, mv, eb = p.get("music_profile") or {}, p.get("movement_profile") or {}, p.get("episode_brief") or {}
    sacred = bool(p.get("is_sacred"))   # the sources' verdict; QC's cue flag only asks for a sacred note
    images = [i for i in (rec.get("images") or []) if isinstance(i, dict) and i.get("url")]
    footage = [f for f in (rec.get("footage") or []) if isinstance(f, dict) and f.get("url")]
    albums = [a for a in (rec.get("albums") or []) if isinstance(a, dict)]
    hero = st.get("hero_video_youtube_id") or ""
    hero_ok = ((st.get("hero_qc") or {}).get("verdict") == "pass")
    conns = [c for c in (p.get("connections") or []) if isinstance(c, dict) and c.get("name")]
    moves = [m for m in (mv.get("signature_moves") or []) if isinstance(m, dict) and m.get("name")]
    steps = [s for s in (teach.get("basic_steps") or []) if ok(s, 8)]
    ladder = [l for l in (eb.get("lesson_ladder") or []) if isinstance(l, dict)]
    gaps = []
    def need(what, where=None):
        if what not in gaps:
            gaps.append(what)
    bpm = tempo_bpm(mp)
    meter = re.sub(r"\s*\(?time signature\)?", "", mp.get("meter")).strip() if ok(mp.get("meter"), 2) else None
    pat = patterns or {}
    counting = counting_for(meter, pat)
    persona = eb.get("instructor_persona") if ok(eb.get("instructor_persona")) else INSTRUCTOR_DEFAULT
    pron = [name] + [a for a in (p.get("aliases") or []) if isinstance(a, str)][:4]

    # ---------- music brief (for an AI composer; never a copy)
    instruments = clean_list(mp.get("instruments"))
    moods = clean_list(mp.get("mood_keywords"))
    refs = [f"{r.get('title')} — {r.get('artist')}" for r in (mp.get("reference_recordings") or []) if isinstance(r, dict) and r.get("title")]
    refs += [f"{a.get('title')} — {a.get('artist')} ({a.get('year') or 'year unknown'})" for a in albums if a.get("title")]
    music_prompt = " ".join(x for x in [
        f"Original instrumental composition in the musical world of {name}" + (f" ({p.get('country')})" if p.get("country") else "") + ".",
        f"Meter {meter}." if meter else "", f"Tempo about {bpm} bpm." if bpm else "",
        f"Rhythm pattern: {mp.get('rhythm_pattern')}." if ok(mp.get("rhythm_pattern")) else "",
        f"Instruments: {', '.join(instruments)}." if instruments else "",
        f"Vocal style: {mp.get('vocal_style')}." if ok(mp.get("vocal_style")) else "",
        f"Form: {mp.get('musical_form')}." if ok(mp.get("musical_form")) else "",
        f"Mood: {', '.join(moods)}." if moods else "",
        f"It should sound like this: {mp.get('sound_description')}" if ok(mp.get("sound_description")) else "",
        "New melody, new arrangement: do not quote or imitate any specific recorded song; keep the idiom, the instruments, the pulse and the proportions.",
    ] if x)
    music = {"purpose": "copyright-free soundtrack with the same DNA as the tradition's music — an original creation, not a reproduction",
             "tempo_bpm": bpm, "meter": meter, "rhythm_pattern": mp.get("rhythm_pattern") if ok(mp.get("rhythm_pattern")) else None,
             "instruments": instruments, "vocal_style": mp.get("vocal_style") if ok(mp.get("vocal_style")) else None,
             "musical_form": mp.get("musical_form") if ok(mp.get("musical_form")) else None, "mood": moods,
             "sound_description": mp.get("sound_description") if ok(mp.get("sound_description")) else None,
             "listen_before_composing": refs[:6],
             "prompt": music_prompt,
             "tracks": [{"id": "theme", "use": "cold open and closing", "length_s": 30},
                        {"id": "underscore", "use": "narration bed, low dynamics", "length_s": 180},
                        {"id": "lesson_slow", "use": "chapters: step practice", "length_s": 240, "tempo_bpm": int(bpm * 0.7) if bpm else None},
                        {"id": "lesson_full", "use": "chapters: dance it to the music", "length_s": 240, "tempo_bpm": bpm}],
             "rules": ["Original composition only — no sampling, no melody of any existing recording, no lyrics from any song.",
                       "Traditional public-domain tunes may be used only when the profile names them and a public-domain source is on file; otherwise compose new material in the idiom.",
                       "Keep the proportions true: the meter, the tempo range and the instrument roles the sources describe.",
                       "Label every generated track with the tool, the date and this brief, so provenance is always clear."]}
    if not bpm: need("tempo (bpm)")
    if not meter: need("meter")
    if not instruments: need("instruments")
    if not refs: need("a verified recording to listen to")

    # ---------- visual brief
    costume_text = secs.get("costume_and_setting") if ok(secs.get("costume_and_setting")) else ""
    restricted = sacred or bool(re.search(r"sacred|ritual|ceremon|initiat|restricted|priest|shaman|mask|regalia|sanctif|holy|temple|funer|mourning|military uniform", (costume_text + " " + (secs.get("occasions_and_meaning") or "")).lower()))
    wardrobe = {"policy": "the narrator wears the dance's traditional apparel, reconstructed meticulously and respectfully from the sources" if costume_text and not restricted
                          else ("neutral dress with a respectful nod (palette and fabric only): the sources describe sacred, ceremonial or restricted attire, or the dance is sacred" if restricted else "neutral dress: the sources do not describe the costume yet"),
                "dress_the_narrator": bool(costume_text) and not restricted, "restricted_attire": restricted,
                "from_sources": costume_text or None, "reference_images": [i.get("source_page") or i.get("url") for i in images[:3]],
                "care": ["every element traceable to the costume notes or a licensed image; nothing added for effect", "no caricature, no exaggeration, no mixing of regions or eras",
                         "a culture bearer reviews the wardrobe before production; the review is recorded in the pack", "credits name the tradition and the sources of the reconstruction"]}
    visual = {"hero_video": {"youtube_id": hero, "checked_by_vision_model": hero_ok, "title": next((v.get("title") for v in (st.get("video_stack") or []) if v.get("role") == "hero"), None)} if hero else None,
              "wardrobe": wardrobe,
              "images": [{"url": i.get("url"), "thumb": i.get("thumb"), "attribution": i.get("attribution"), "license": i.get("license"), "source_page": i.get("source_page"), "description": i.get("description")} for i in images[:12]],
              "footage": [{"title": f.get("title"), "url": f.get("url"), "year": f.get("year"), "license": f.get("license"), "attribution": f.get("attribution")} for f in footage[:8]],
              "motifs": clean_list(eb.get("visual_motifs")),
              "costume_notes": secs.get("costume_and_setting") if ok(secs.get("costume_and_setting")) else None,
              "setting_notes": secs.get("occasions_and_meaning") if ok(secs.get("occasions_and_meaning")) else None,
              "map": {"country": p.get("country"), "region": rec.get("region"), "coords": rec.get("coords")},
              "generation_rules": ["Generated imagery reconstructs costume and setting ONLY from the costume notes above and the licensed images; it is labelled 'reconstruction' on screen.",
                                   "No likeness of a real, named person. No sacred objects or ceremonies beyond what the sources describe.",
                                   "Licensed images and footage are shown with their attribution and licence text."]}
    if not hero: need("a hero video")
    elif not hero_ok: need("the hero video's vision check")
    if len(images) < 3: need("licensed images (3 needed)")
    if not footage: need("licensed reference footage")

    # ---------- teaching formula (from the studied teachers)
    formula = {"source": pat.get("source") or "built-in defaults (no tutorial studied yet for this dance or family)",
               "videos_studied": pat.get("videos") or 0, "counting": counting,
               "demonstration": pat.get("demonstration") or ["front view, then back view (student's perspective)", "slow, then half tempo, then full tempo", "three repetitions of every step before moving on"],
               "cues": pat.get("cues") or ["say the count before the move", "name the body part, then the direction", "one correction at a time"],
               "common_mistakes": pat.get("mistakes") or [], "segment_order": pat.get("segment_order") or ["welcome", "body", "count", "step", "step", "combine", "mistakes", "music", "recap"],
               "steps_as_taught": pat.get("steps_as_taught") or []}

    # ---------- Episode 1 · Meet the dance
    E = []
    def scene(code, title, dur, narration, on_screen, music_cue, extra=None, needs=None):
        s = {"code": code, "title": title, "duration_s": dur, "narration": [n for n in narration if n], "on_screen": [o for o in on_screen if o], "music": music_cue}
        if extra: s.update(extra)
        if needs: s["needs"] = needs
        return s
    hook = eb.get("title_hook") if ok(eb.get("title_hook")) else (p.get("insight") if ok(p.get("insight")) else p.get("tagline"))
    E.append(scene("hook", "Cold open", 35, [hook, f"This is {name}." + (f" {p.get('era')}." if ok(p.get('era'), 3) else "")],
                   [f"Hero video, first 10 seconds ({hero})" if hero else "Hero video — MISSING", f"Title card: {name} · {p.get('country') or ''} · {p.get('era') or ''}"], "theme (30 s)"))
    E.append(scene("where", "Where and when", 70, sentences(secs.get("origins_and_history"), 3), ["Map: " + (p.get("country") or "country unknown") + (f" · {rec.get('region')}" if rec.get("region") else ""), "Image 1 with attribution" if images else "Image — MISSING"], "underscore",
                   needs=None if ok(secs.get("origins_and_history")) else ["origins_and_history"]))
    E.append(scene("occasion", "When it is danced", 60, sentences(secs.get("occasions_and_meaning"), 3) + ([f"Today it is a {p.get('tradition_status')} tradition."] if p.get("tradition_status") in ("living", "revived", "historical") else []),
                   [f"Footage: {footage[0].get('title')} ({footage[0].get('url')})" if footage else "Footage — MISSING (use images)"], "underscore",
                   needs=None if ok(secs.get("occasions_and_meaning")) else ["occasions_and_meaning"]))
    E.append(scene("watch", "Watch it", 75, sentences(secs.get("how_it_is_danced"), 3) + ([("Watch for " + ", ".join(m.get("name") for m in moves[:3]) + ".")] if moves else []),
                   [f"Hero video full screen, 30–45 s ({hero})" if hero else "Hero video — MISSING", "Captions name each signature move as it appears" if moves else "Signature moves — MISSING", f"Formation: {mv.get('formation_and_space')}" if ok(mv.get("formation_and_space")) else ""], "diegetic (the video's own sound), underscore under narration",
                   needs=[x for x, c in (("how_it_is_danced", ok(secs.get("how_it_is_danced"))), ("signature_moves", bool(moves))) if not c] or None))
    music_lines = sentences(secs.get("music_and_instruments"), 2) + [x for x in [
        f"Listen for the {', '.join(instruments[:4])}." if instruments else "",
        f"The pulse is {meter}" + (f" at about {bpm} beats a minute." if bpm else ".") if meter else (f"The tempo sits around {bpm} beats a minute." if bpm else ""),
        mp.get("sound_description") if ok(mp.get("sound_description")) else ""] if x]
    E.append(scene("music", "Listen", 70, music_lines, ["Instrument names on screen as each is mentioned", ("Listen later: " + "; ".join(refs[:3])) if refs else "Verified recording — MISSING", "Waveform or rhythm-pattern graphic: " + (mp.get("rhythm_pattern") if ok(mp.get("rhythm_pattern")) else "")],
                   "the music brief's underscore at its own tempo; drop narration under the hook of a verified recording if licensed, else original",
                   needs=[x for x, c in (("music_and_instruments", ok(secs.get("music_and_instruments"))), ("tempo", bool(bpm)), ("meter", bool(meter))) if not c] or None))
    E.append(scene("costume", "The costume and the setting", 60, sentences(secs.get("costume_and_setting"), 3), [f"Image gallery: {len(images)} licensed images with attribution" if images else "Images — MISSING", "Reconstruction imagery allowed only from the costume notes, labelled 'reconstruction'"], "underscore",
                   needs=[x for x, c in (("costume_and_setting", ok(secs.get("costume_and_setting"))), ("images", len(images) >= 3)) if not c] or None))
    E.append(scene("people", "The people", 60, sentences(secs.get("notable_figures"), 2) + sentences(secs.get("regional_variants"), 1) + sentences(secs.get("lineage"), 1), ["Names on screen as they are spoken", "Variant names as a small list" if ok(secs.get("regional_variants")) else ""], "underscore",
                   needs=[x for x, c in (("notable_figures", ok(secs.get("notable_figures"))), ("lineage", ok(secs.get("lineage")))) if not c] or None))
    fam_lines = [f"{name} is {str(c.get('relation') or 'related').replace('_', ' ')} of {c.get('name')}" + (f": {str(c.get('note')).rstrip('.')}" if c.get('note') else "") + "." for c in conns[:4]]
    E.append(scene("family", "Family tree", 40, fam_lines, ["Graph: the connections with their relation labels" if conns else "Connections — MISSING"], "underscore",
                   needs=None if len(conns) >= 2 else ["connections"]))
    if sacred:
        E.append(scene("first_step", "A respectful note", 30, [p.get("sacred_note") if ok(p.get("sacred_note")) else f"{name} is a sacred or restricted dance. We watch, listen and learn its story; we do not teach its steps."], ["Calm wide shot, no demonstration"], "underscore"))
    else:
        E.append(scene("first_step", "Try one step", 60, ([f"Before we go, one step. {steps[0]}"] + ([steps[1]] if len(steps) > 1 else []) + [f"Count it: {counting}.", "Chapter 1 takes it slowly from here."]) if steps else [], ["Instructor, front view, slow", "Count on screen"], "lesson_slow",
                       needs=None if steps else ["teaching steps"]))
    E.append(scene("close", "Until next time", 25, [eb.get("logline") if ok(eb.get("logline")) else "", f"Sources: {len(rec.get('sources') or [])} references, every claim checked against its source."], ["Credits: sources, image and footage licences, music provenance"], "theme (20 s)"))

    # ---------- Chapters
    chapters = []
    if sacred:
        chapters_note = "withheld: sacred or restricted dance — Episode 1 only"
    else:
        chapters_note = None
        lv = (ladder + [{}, {}, {}])[:3]
        tiers = [
            {"n": 1, "title": "First steps", "steps": steps[:4] or [], "moves": [], "extra": [mv.get("posture"), mv.get("arms_and_hands")]},
            {"n": 2, "title": "Building the dance", "steps": steps[4:8] or steps[:4], "moves": moves[:2], "extra": [mv.get("formation_and_space"), mv.get("partnering"), mv.get("hips_and_torso")]},
            {"n": 3, "title": "Dancing it fully", "steps": steps[8:12] or steps[-2:], "moves": moves[2:5] or moves[:2], "extra": [mv.get("levels_and_jumps"), mv.get("tempo_feel"), secs.get("regional_variants")]},
        ]
        for t, L in zip(tiers, lv):
            C = []
            goal = L.get("goal") if ok(L.get("goal"), 8) else f"the {t['title'].lower()} of {name}"
            drills = clean_list(L.get("drills"), 6)
            nd = []
            C.append(scene("welcome", "Welcome", 45, [f"Chapter {t['n']} — {t['title']}. Today: {goal}.", f"Level: {L.get('level') or ['beginner', 'intermediate', 'advanced'][t['n'] - 1]}. " + (f"Difficulty of the dance overall: {mv.get('difficulty')}." if ok(mv.get('difficulty'), 4) else ""), f"Your instructor: {persona}"],
                           ["Instructor front view, name of the chapter, the three things you will learn"], "theme (10 s) then silence"))
            body = [x for x in [mv.get("posture") if ok(mv.get("posture")) else "", mv.get("arms_and_hands") if ok(mv.get("arms_and_hands")) else "", mv.get("hips_and_torso") if ok(mv.get("hips_and_torso")) else ""] if x]
            if not body: nd.append("posture / arms")
            C.append(scene("body", "Body and posture", 60, body or ["Posture notes are not in the sources yet — the instructor demonstrates neutral posture and the arm position seen in the hero video."], ["Instructor front then side view; freeze-frame on posture", "Overlay: the hero video's posture for comparison" if hero else ""], "silence", needs=["posture"] if not body else None))
            C.append(scene("count", "Count and rhythm", 60, [f"Count: {counting}." + (f" The meter is {meter}." if meter else ""), (f"Rhythm pattern: {mp.get('rhythm_pattern')}." if ok(mp.get('rhythm_pattern')) else ""), "Clap it first, then step it in place."], ["Counts on screen, flashing on the beat", f"Metronome at {int(bpm * 0.7)} bpm" if bpm else "Metronome — tempo MISSING, use a slow comfortable pulse"], "lesson_slow (clicks only until the step lands)",
                           needs=[x for x, c in (("tempo", bool(bpm)), ("meter", bool(meter))) if not c] or None))
            sa = t["steps"][:2]; sb = t["steps"][2:4]
            fw = mv.get("footwork") if ok(mv.get("footwork")) else ""
            C.append(scene("step_a", "Step A — slowly", 150, ([f"Step {i + 1}: {s}" for i, s in enumerate(sa)] + ([f"Footwork from the sources: {fw}"] if fw and t["n"] == 1 else []) + ([f"Drill: {drills[0]}"] if drills else [])) or [], [f"Instructor front view, then back view (student's perspective); {formula['demonstration'][2] if len(formula['demonstration']) > 2 else 'three repetitions'}", "Counts on screen"], "lesson_slow",
                           {"counts": counting, "repetitions": 3}, needs=["teaching steps"] if not sa else None))
            mv_lines = [f"{m.get('name')}: {m.get('description')}" for m in t["moves"] if m.get("description")]
            C.append(scene("step_b", "Step B — the next layer", 150, ([f"Step {i + 3}: {s}" for i, s in enumerate(sb)] + mv_lines + ([f"Drill: {drills[1]}"] if len(drills) > 1 else [])) or [], ["Instructor front and back view; slow, then half tempo", "Name of the signature move on screen" if t["moves"] else ""], "lesson_slow",
                           {"counts": counting, "repetitions": 3}, needs=["signature moves" if t["n"] > 1 else "teaching steps"] if not (sb or mv_lines) else None))
            C.append(scene("combine", "Put it together", 120, ["Step A, then Step B, without stopping. Slow first.", "Now half tempo. Now full tempo.", "Mirror: the instructor faces you and mirrors, so your right is your right."] + ([f"Drill: {drills[2]}"] if len(drills) > 2 else []), ["Split screen: front view / back view", "Tempo label changes: slow → half → full"], "lesson_slow then lesson_full"))
            mistakes = ([mv.get("what_to_avoid")] if ok(mv.get("what_to_avoid")) else []) + [f"Teachers of this dance warn against: {m}" for m in (formula["common_mistakes"] or [])[:3]]
            adapt = p.get("adaptations") or {}
            se, ch = adapt.get("seniors") or {}, adapt.get("children") or {}
            opts = [x for x in [f"Seated or supported option: {se.get('seated_version')}" if ok(se.get('seated_version'), 12) else "", f"For children: {ch.get('game_version')}" if ok(ch.get('game_version'), 12) else ""] if x]
            C.append(scene("mistakes", "Common mistakes and what to avoid", 60, mistakes or ["The sources do not list common mistakes yet; the instructor names the two most visible ones from the hero video."], ["Side-by-side: wrong / right", "Options card: " + " · ".join(opts) if opts else ""], "silence",
                           {"options": opts, "derived_note": "options are derived teaching suggestions, not facts from the sources"}, needs=["what_to_avoid"] if not mistakes else None))
            C.append(scene("music_run", "Dance it to the music", 120, [f"Count-in: {counting}.", "Full tempo, the whole sequence, twice." + (f" Formation: {mv.get('formation_and_space')}" if ok(mv.get("formation_and_space")) and t["n"] >= 2 else "")], ["Wide shot, instructor and two students", f"Track: lesson_full at {bpm} bpm" if bpm else "Track: lesson_full (tempo MISSING)"], "lesson_full"))
            culture = sentences(secs.get(["occasions_and_meaning", "notable_figures", "lineage"][t["n"] - 1]), 1)
            C.append(scene("close", "Recap", 40, [f"You can now: {goal}."] + culture + ([f"Next: Chapter {t['n'] + 1}."] if t["n"] < 3 else ["You know the dance. Go and dance it with people."]), ["Recap card with the counts", "Next chapter card"], "theme (10 s)"))
            for x in nd: need(GAP_LABEL.get(x, x))
            chapters.append({"chapter": t["n"], "title": t["title"], "goal": goal, "level": L.get("level"), "scenes": C})

    # ---------- gaps across scenes (canonical names the research pass understands)
    for s in E:
        for n in s.get("needs") or []:
            need(GAP_LABEL.get(n, n))
    for c in chapters:
        for s in c["scenes"]:
            for n in s.get("needs") or []:
                need(GAP_LABEL.get(n, n))
    gaps = list(dict.fromkeys(gaps))
    status = "withheld-chapters" if sacred else ("complete" if not gaps else "draft")
    pack = {"slug": slug, "name": name, "pack_version": PACK_VERSION, "built_at": now_iso(), "researched_at": rec.get("researched_at"), "qc_score": (qc or {}).get("qc_score"),
            "status": status, "sacred": sacred, "chapters_note": chapters_note,
            "formula": {"episode_1": [s["code"] for s in E], "chapter": ["welcome", "body", "count", "step_a", "step_b", "combine", "mistakes", "music_run", "close"]},
            "voice": {"narrator": NARRATOR, "instructor": {"persona": persona, "rule": "counts out loud; demonstrates front and back; three slow repetitions before tempo; one correction at a time"}, "pronunciation": pron},
            "episode_1": {"title": f"Meet {name}", "scenes": E, "runtime_s": sum(s["duration_s"] for s in E)},
            "chapters": chapters, "music_brief": music, "visual_brief": visual, "teaching_formula": formula,
            "gaps": gaps, "sources": rec.get("sources") or [], "claims_verified": (rec.get("citation") or {}).get("supported"), "claims": (rec.get("citation") or {}).get("claims"),
            "polished": False}
    return pack

# ------------------------------------------------------------------ polish (optional model pass, verified)
POLISH_SYSTEM = """You are the script editor of a documentary and class series about dance traditions. You receive a scene-by-scene pack whose narration
lines were assembled mechanically from a verified profile. Rewrite ONLY the "narration" arrays so they read as spoken, warm, concrete documentary
narration (short sentences, present tense, no filler, no hype), keeping every fact, name, number, count and date exactly as given and adding NONE.
Keep the same scene codes and the same number of scenes. Do not touch on_screen, music or any other field. Output JSON: {"episode_1": [{"code":..., "narration":[...]}, ...], "chapters": [{"chapter": n, "scenes": [{"code":..., "narration":[...]}]}]}"""

def _facts(text):
    years = set(re.findall(r"\b(1[0-9]{3}|20[0-2][0-9])\b", text))
    nums = set(re.findall(r"\b\d+\b", text))
    caps = set(w for w in re.findall(r"\b[A-Z][a-zA-ZÀ-ɏ'-]{2,}\b", text))
    return years, nums, caps

def verify_polish(pack, new, rec):
    """Polished narration may not introduce a year, a number or a capitalised name that the profile does not contain."""
    corpus = json.dumps(rec.get("profile") or {}, ensure_ascii=False) + " " + json.dumps(pack.get("music_brief"), ensure_ascii=False) + " " + " ".join(pack.get("voice", {}).get("pronunciation") or [])
    cy, cn, cc = _facts(corpus)
    cc |= {"Chapter", "Episode", "Step", "Count", "Level", "Today", "Watch", "Listen", "Now", "Mirror", "Slow", "Full", "Half", "Drill", "Sources", "The", "This", "Your", "Before", "Next", "Instructor", "Atlas"}
    def okay(lines):
        y, n, c = _facts(" ".join(lines))
        return y <= cy and n <= (cn | {"1", "2", "3", "4", "5", "6", "7", "8"}) and all(w in cc or w.lower() in corpus.lower() for w in c)
    out_e = {s["code"]: s["narration"] for s in (new.get("episode_1") or []) if isinstance(s, dict) and isinstance(s.get("narration"), list)}
    kept = 0
    for s in pack["episode_1"]["scenes"]:
        lines = [l for l in (out_e.get(s["code"]) or []) if isinstance(l, str) and l.strip()]
        if lines and okay(lines):
            s["narration"] = lines; kept += 1
    for ch in pack["chapters"]:
        nc = next((c for c in (new.get("chapters") or []) if isinstance(c, dict) and c.get("chapter") == ch["chapter"]), None) or {}
        out_c = {s["code"]: s["narration"] for s in (nc.get("scenes") or []) if isinstance(s, dict) and isinstance(s.get("narration"), list)}
        for s in ch["scenes"]:
            lines = [l for l in (out_c.get(s["code"]) or []) if isinstance(l, str) and l.strip()]
            if lines and okay(lines):
                s["narration"] = lines; kept += 1
    return kept

def polish(pack, rec, llm):
    user = json.dumps({"name": pack["name"], "episode_1": [{"code": s["code"], "title": s["title"], "narration": s["narration"]} for s in pack["episode_1"]["scenes"]],
                       "chapters": [{"chapter": c["chapter"], "scenes": [{"code": s["code"], "title": s["title"], "narration": s["narration"]} for s in c["scenes"]]} for c in pack["chapters"]]}, ensure_ascii=False)[:30000]
    jd = llm.json(POLISH_SYSTEM, user, strong=False, temperature=0.4, max_tokens=6000)
    if not jd:
        return 0
    kept = verify_polish(pack, jd, rec)
    pack["polished"] = kept > 0
    pack["polish_kept_scenes"] = kept
    return kept

# ------------------------------------------------------------------ rendering
def render_md(pack):
    L = [f"# {pack['name']} — episode pack", "", f"*Status: {pack['status']} · built {pack['built_at'][:10]} · judge {pack.get('qc_score')} · {pack.get('claims_verified')}/{pack.get('claims')} claims verified · narration {'polished by the model and verified' if pack.get('polished') else 'assembled from the profile'}*", ""]
    if pack.get("gaps"):
        L += ["**Gaps** (handed to the research queue): " + "; ".join(pack["gaps"]), ""]
    L += [f"**Narrator:** {pack['voice']['narrator']['voice']}", f"**Instructor:** {pack['voice']['instructor']['persona']}", f"**Say it:** {', '.join(pack['voice']['pronunciation'])}", ""]
    def block(title, scenes, runtime=None):
        L.append(f"## {title}" + (f" · {runtime // 60} min" if runtime else ""))
        L.append("")
        for i, s in enumerate(scenes, 1):
            L.append(f"### {i}. {s['title']} ({s['duration_s']} s) · `{s['code']}`")
            for n in s["narration"]:
                L.append(f"NARRATION: {n}")
            for o in s["on_screen"]:
                L.append(f"ON SCREEN: {o}")
            L.append(f"MUSIC: {s['music']}")
            if s.get("counts"):
                L.append(f"COUNTS: {s['counts']} · repetitions: {s.get('repetitions')}")
            if s.get("options"):
                L.append("OPTIONS: " + " · ".join(s["options"]) + f" ({s.get('derived_note')})")
            if s.get("needs"):
                L.append("NEEDS: " + ", ".join(s["needs"]))
            L.append("")
    block(f"Episode 1 · {pack['episode_1']['title']}", pack["episode_1"]["scenes"], pack["episode_1"]["runtime_s"])
    if pack.get("chapters_note"):
        L += [f"## Chapters — {pack['chapters_note']}", ""]
    for c in pack["chapters"]:
        block(f"Chapter {c['chapter']} · {c['title']} — {c['goal']}", c["scenes"], sum(s["duration_s"] for s in c["scenes"]))
    m = pack["music_brief"]
    L += ["## Music brief (original, copyright-free)", "", m["prompt"], "", "Tracks: " + "; ".join(f"{t['id']} ({t['use']}, {t['length_s']} s" + (f", {t['tempo_bpm']} bpm" if t.get('tempo_bpm') else "") + ")" for t in m["tracks"]), ""]
    if m.get("listen_before_composing"):
        L += ["Listen before composing (never copy): " + "; ".join(m["listen_before_composing"]), ""]
    L += ["Rules: " + " ".join(m["rules"]), ""]
    v = pack["visual_brief"]
    w = v.get("wardrobe") or {}
    L += ["## Visual brief", "", f"Narrator's wardrobe: {w.get('policy')}" + (f" — from the sources: {w.get('from_sources')}" if w.get("dress_the_narrator") else ""), "Care: " + "; ".join(w.get("care") or []), "",
          f"Hero video: {v['hero_video']}" if v.get("hero_video") else "Hero video: MISSING",
          f"Images: {len(v['images'])} licensed" + (" — " + "; ".join(f"{i.get('attribution') or ''} ({i.get('license') or ''})" for i in v["images"][:5]) if v["images"] else ""),
          f"Footage: " + ("; ".join(f"{f['title']} — {f['url']}" for f in v["footage"]) if v["footage"] else "MISSING"),
          f"Motifs: {', '.join(v['motifs'])}" if v["motifs"] else "", f"Costume notes: {v['costume_notes']}" if v.get("costume_notes") else "", "", "Rules: " + " ".join(v["generation_rules"]), ""]
    f = pack["teaching_formula"]
    L += ["## Teaching formula", "", f"Source: {f['source']} · videos studied: {f['videos_studied']}", f"Counting: {f['counting']}", "Demonstration: " + "; ".join(f["demonstration"]), "Cues: " + "; ".join(f["cues"])]
    if f.get("common_mistakes"):
        L.append("Common mistakes the studied teachers name: " + "; ".join(f["common_mistakes"]))
    L += ["", f"Sources ({len(pack['sources'])}): " + "; ".join(pack["sources"][:8]), ""]
    return "\n".join(L)

# ------------------------------------------------------------------ run
def patterns_for(slug, family, patterns):
    if not patterns:
        return {}
    by_slug = (patterns.get("by_slug") or {}).get(slug)
    if by_slug and by_slug.get("videos"):
        return {"source": f"{by_slug['videos']} tutorial(s) of this dance studied", "videos": by_slug["videos"], "counting": by_slug.get("counting"), "cues": by_slug.get("cues"), "mistakes": by_slug.get("mistakes"), "demonstration": by_slug.get("demonstration"), "segment_order": by_slug.get("segment_order"), "steps_as_taught": by_slug.get("steps_as_taught")}
    fam = (patterns.get("by_family") or {}).get(family or "")
    if fam and fam.get("videos"):
        return {"source": f"{fam['videos']} tutorial(s) of the {family} family studied", "videos": fam["videos"], "counting": fam.get("counting"), "cues": fam.get("cues"), "mistakes": [], "demonstration": fam.get("demonstration"), "segment_order": fam.get("segment_order")}
    g = patterns.get("global") or {}
    if g.get("videos"):
        return {"source": f"{g['videos']} tutorials across the atlas studied", "videos": g["videos"], "counting": None, "cues": g.get("cues"), "mistakes": [], "demonstration": g.get("demonstration"), "segment_order": g.get("segment_order")}
    return {}

def run(polish_budget=0, only=None):
    rep = Report("episodes")
    qidx = load_state("qc_index.json", {}) or {}
    cat = (jload(os.path.join("public", "catalog", "dances.app.json"), {}) or {}).get("styles") or {}
    retired = {r.get("slug") for r in ((jload(os.path.join("public", "catalog", "retired.json"), {}) or {}).get("retired") or []) if isinstance(r, dict)}
    patterns = jload(os.path.join("pedagogy", "teaching_patterns.json"), {}) or {}
    index = jload(os.path.join("public", "catalog", "episodes.json"), {}) or {}
    packs = index.get("packs") or {}
    gaps_all = {}
    llm = LLM() if polish_budget > 0 else None
    polished = 0
    targets = [s for s, v in qidx.items() if v.get("publish_gate") == "publish" and s not in retired and (not only or s in only)]
    for slug in sorted(targets):
        rec = jload(os.path.join(RESEARCH_DIR, slug + ".json"), None)
        if not rec or rec.get("status") != "researched":
            continue
        qc = jload(os.path.join(QC_DIR, slug + ".json"), {}) or {}
        prev = jload(os.path.join(EPISODE_DIR, slug + ".json"), None)
        fresh = prev and prev.get("researched_at") == rec.get("researched_at") and prev.get("pack_version") == PACK_VERSION and prev.get("hero_checked") == ((cat.get(slug) or {}).get("hero_qc") or {}).get("verdict")
        try:
            if fresh:
                pack = prev
                rep.inc("unchanged")
            else:
                pack = build_pack(rec, qc, cat.get(slug) or {}, patterns_for(slug, rec.get("family"), patterns))
                pack["hero_checked"] = ((cat.get(slug) or {}).get("hero_qc") or {}).get("verdict")
                rep.inc("built")
            if llm and not pack.get("polished") and polished < polish_budget and not pack.get("sacred"):
                kept = polish(pack, rec, llm)
                polished += 1
                rep.inc("polished" if kept else "polish_rejected")
            if not fresh or (llm and pack.get("polished")):
                jsave(os.path.join(EPISODE_DIR, slug + ".json"), pack)
                with open(os.path.join(EPISODE_DIR, slug + ".md"), "w", encoding="utf-8") as f:
                    f.write(render_md(pack))
            packs[slug] = {"name": pack["name"], "status": pack["status"], "built_at": pack["built_at"], "scenes": len(pack["episode_1"]["scenes"]) + sum(len(c["scenes"]) for c in pack["chapters"]),
                           "chapters": len(pack["chapters"]), "gaps": len(pack["gaps"]), "polished": bool(pack.get("polished")), "runtime_min": round((pack["episode_1"]["runtime_s"] + sum(s["duration_s"] for c in pack["chapters"] for s in c["scenes"])) / 60),
                           "music_tempo": pack["music_brief"].get("tempo_bpm"), "hero_checked": pack.get("hero_checked") == "pass"}
            if pack["gaps"]:
                gaps_all[slug] = pack["gaps"]
            rep.inc("status_" + pack["status"])
        except Exception as e:
            rep.error(f"episodes {slug}: {e}")
    for s in list(packs):
        if s not in targets:
            packs.pop(s, None)   # no longer published
    jsave(os.path.join("public", "catalog", "episodes.json"), {"schema": "dw_episodes_v1", "pack_version": PACK_VERSION, "generated_at": now_iso(), "count": len(packs),
                                                              "complete": sum(1 for v in packs.values() if v["status"] == "complete"), "polished": sum(1 for v in packs.values() if v["polished"]),
                                                              "formula": {"episode_1": ["hook", "where", "occasion", "watch", "music", "costume", "people", "family", "first_step", "close"], "chapter": ["welcome", "body", "count", "step_a", "step_b", "combine", "mistakes", "music_run", "close"]},
                                                              "packs": packs})
    save_state("episode_gaps.json", gaps_all)
    if llm:
        llm.record(rep)
    rep.note(f"episode packs: {len(packs)} ({sum(1 for v in packs.values() if v['status'] == 'complete')} complete, {sum(1 for v in packs.values() if v['polished'])} polished); gaps for {len(gaps_all)} packs")
    return rep.finish()

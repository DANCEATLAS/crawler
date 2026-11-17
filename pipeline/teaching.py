"""Teaching research — how to teach anyone to dance, for the Best Dance Friend (BDF).

A standing research mission, separate from the atlas of dances (owner direction, 17 November 2026): find, filter and join
everything that shows how dancing is best taught, so that BDF's way of teaching rests on evidence and keeps deepening.
Every night, on free allowances only (Gemini free tier, YouTube Data API units, Europe PMC, Wikipedia, yt-dlp):

1. FIND LESSONS      beside the lessons the crawler finds for each dance, the lessons that teach what every dance shares
                     (the beat, groove, balance, confidence, first steps), in several languages   → pedagogy/foundation_lessons.json
2. RANK TEACHERS     every lesson is grouped by teacher (channel) and ranked by what learners wrote under the lessons:
                     crowd wisdom, not views                                                       → pedagogy/teachers.json
3. STUDY THE METHOD  the best lessons of the best-ranked teachers are watched with one question: HOW does this teacher
                     teach (screen, sequence, cues, encouragement, what is offered when a step is hard). The public
                     comments are read in the same call: what learners find hard, what clicked, what they ask for
                                                                                                   → pedagogy/methods/<video>.json
4. READ THE RESEARCH a list of topics (how movement is learned, what keeps people coming back, what is universal in
                     music and dance) and an open search that never ends: the most cited papers on dance and learning,
                     a few a night. A finding is kept only when its quote is found in the source     → pedagogy/science/<key>.json
5. JOIN (no model)   the three kinds of evidence meet on one vocabulary of teaching practices     → BDF_TEACHING_SYSTEM.md,
                     pedagogy/bdf_system.json, public/catalog/bdf_teaching_system.json (for the AI teaching service)

Breadth first (one lesson from every ranked teacher), then depth (up to METHOD_PER_TEACHER lessons of the best), so the
mission never runs dry. Every observation is an unreviewed machine reading with a timestamp, so a person can check it;
the ranking counts learners' own words and is not a verdict on a teacher.
"""
import os, re, glob, math, time, datetime as dt, urllib.parse
from collections import Counter
from .common import jload, jsave, log, warn, now_iso, slugify, get_json, LLM, Report

PED = "pedagogy"
TEACHERS = os.path.join(PED, "teachers.json")
METHODS_DIR = os.path.join(PED, "methods")
SCIENCE_DIR = os.path.join(PED, "science")
FOUNDATION_LESSONS = os.path.join(PED, "foundation_lessons.json")
STATE = os.path.join(PED, "research_state.json")
SYSTEM_JSON = os.path.join(PED, "bdf_system.json")
PUBLIC_JSON = os.path.join("public", "catalog", "bdf_teaching_system.json")
DOC = "BDF_TEACHING_SYSTEM.md"
LESSONS = "tutorial_results.json"
METHOD_SECONDS = 600
RETRY_DAYS, SCIENCE_REFRESH_DAYS = 30, 180
BASICS = "basics-"   # slug prefix of the lessons that teach what every dance shares

# One vocabulary for all three kinds of evidence (teachers, learners, research): the join is on these keys.
# key: (what it is, what a teacher does about it)
PRACTICE = {
    "mirror_view": ("a mirrored or back view, so the learner copies without flipping left and right", "Show the step from behind or mirrored, so it can be copied directly."),
    "split_screen": ("two views at once: feet and whole body, front and back, or two speeds", "Show two views at once when feet and body both matter."),
    "on_screen_counts": ("counts, step names or arrows written on the screen", "Put the counts and the step names on the screen."),
    "demo_first": ("the whole step or phrase shown once at speed before it is broken down", "Show the whole thing once at speed before breaking it down."),
    "chunking": ("small pieces, each practised before the next one is added", "Teach one small piece at a time and practise it before adding the next."),
    "layering": ("feet first, then arms, styling, turns or a partner on top", "Feet first; add arms, styling and turns only when the feet are steady."),
    "tempo_ramp": ("slow first, then faster, then full speed", "Start slow and speed up in steps to full tempo."),
    "counts_and_rhythm": ("counting, or the rhythm spoken or clapped (quick-quick-slow, boom-cha)", "Count out loud or speak the rhythm."),
    "music_early": ("practice with the music early and often", "Bring in the music early, not only at the end."),
    "repetition": ("many repetitions, loops and follow-along rounds", "Repeat more than feels necessary, with follow-along rounds."),
    "recap_and_practice_plan": ("a recap, homework or a practice routine to take away", "End with a recap and one small practice to take away."),
    "imagery": ("an image or comparison instead of anatomy (\"paint the floor with your toe\")", "Give an image to aim at instead of a muscle to control."),
    "feel_and_groove": ("the feeling, bounce, weight and musicality before precision", "Teach the feeling and the bounce before precision."),
    "culture_and_meaning": ("where the dance comes from and what it means, inside the lesson", "Say where the dance comes from and what it means."),
    "play_and_variation": ("improvise, vary, make it yours", "Invite the learner to vary it and make it their own."),
    "quick_win": ("the learner is dancing something real within the first minutes", "Get the learner dancing something real in the first minutes."),
    "praise_and_expectancy": ("telling learners they can do it and celebrating small wins", "Tell learners they can do it, and name each small win."),
    "normalise_mistakes": ("mistakes are expected; the teacher makes light of them or shows their own", "Treat mistakes as normal, and show your own."),
    "fun_and_energy": ("humour, play and the teacher's own visible joy", "Bring humour and visible joy."),
    "autonomy": ("the learner chooses: pause, pick a tempo, pick a variation, own style", "Offer choices: the tempo, the variation, when to pause."),
    "social_connection": ("community, challenges, dancing with others, sharing", "Connect the learner with others: a partner, a challenge, something to share."),
    "reason_to_return": ("a reason to come back: the next lesson, a series, a challenge, a daily routine", "Give a reason to come back: the next step, a series, a routine."),
    "error_correction": ("the common mistake is named and its fix is shown", "Name the common mistake and show the fix."),
    "regression": ("an easier version is offered when the step is hard", "Offer an easier version the moment a step is hard."),
    "progression": ("a harder version, styling or speed for those who are ready", "Offer a harder version to those who are ready."),
    "body_adaptation": ("options for knees, balance, age, a small room or no partner", "Give options for different bodies, small rooms and no partner."),
    "self_check": ("how to check yourself: a mirror, filming, landmarks, questions to ask", "Teach learners how to check themselves."),
}
PRACTICES = {k: v[0] for k, v in PRACTICE.items()}
THEMES = [("See it", ["mirror_view", "split_screen", "on_screen_counts", "demo_first"]),
          ("Build it", ["chunking", "layering", "tempo_ramp", "counts_and_rhythm", "music_early", "repetition", "recap_and_practice_plan"]),
          ("Feel it", ["imagery", "feel_and_groove", "culture_and_meaning", "play_and_variation"]),
          ("Stay with it", ["quick_win", "praise_and_expectancy", "normalise_mistakes", "fun_and_energy", "autonomy", "social_connection", "reason_to_return"]),
          ("Fit the person", ["error_correction", "regression", "progression", "body_adaptation", "self_check"])]
VIEWS = ("front", "back", "mirror", "side", "overhead", "feet_closeup", "split_screen", "picture_in_picture")
ON_SCREEN = ("counts", "step_names", "arrows_or_diagrams", "captions", "timer_or_progress")
EDITING = ("slow_motion", "loop_replay", "freeze_frame", "speed_labels")
ENTRY = ("watch_first", "count_first", "rhythm_first", "feet_first", "feel_first", "story_first")
ADAPT_KINDS = {"easier": "regression", "harder": "progression", "slower": "tempo_ramp", "different_body": "body_adaptation",
               "no_partner": "body_adaptation", "small_space": "body_adaptation", "mindset": "normalise_mistakes", "other": None}
TAG_LIST = "\n".join(f"- {k}: {v}" for k, v in PRACTICES.items())

METHOD_SYSTEM = """You are studying HOW an online dance class teaches, for the design of an AI dance teacher. Two sources, kept apart:
(A) the VIDEO: report only what is seen or heard in it. (B) the LEARNER COMMENTS written under it: report only what the comments say.
Output a single JSON object:
{"is_lesson": true|false  (false for performances, vlogs, music videos, trailers),
 "teacher_system": "<two or three sentences: what this teacher does, in order, to get a beginner dancing>",
 "signature": "<the one thing this teacher does that most teachers do not; empty if nothing stands out>",
 "screen": {"views": [<any of: """ + ", ".join(VIEWS) + """>], "on_screen": [<any of: """ + ", ".join(ON_SCREEN) + """>], "editing": [<any of: """ + ", ".join(EDITING) + """>]},
 "practices": [{"tag": "<one tag from the list below>", "t": "m:ss", "what": "<what the teacher does, at most 25 words; describe, do not transcribe>"}],
 "adaptations": [{"t": "m:ss", "difficulty": "<what a learner may find hard, as the teacher frames it>", "adjustment": "<what the teacher offers instead>",
                  "kind": "<one of: """ + ", ".join(ADAPT_KINDS) + """>"}],
 "entry_points": [<any of: """ + ", ".join(ENTRY) + """>],
 "pace": {"talk_vs_move": "mostly_talk|balanced|mostly_move", "seconds_before_first_movement": <integer or null>, "pieces_taught": <integer or null>},
 "learner_voice": {"struggles": [{"theme": "<what learners say they find hard, at most 12 words>", "tag": "<a tag from the list, or other>", "count": <comments saying it>}],
                   "clicked": [{"theme": "<what learners say made it work for them>", "tag": "<tag or other>", "count": <integer>}],
                   "requests": [{"theme": "<what learners ask the teacher for>", "tag": "<tag or other>", "count": <integer>}]},
 "limits": "<what the video cannot show, or what you could not tell>"}
Tags:
""" + TAG_LIST + """
Rules: at most 12 practices and 6 adaptations, each with a real timestamp from the video; never invent a timestamp.
An adaptation is only what the teacher actually offers ("if this is hard, do this", "you can also"), never your own advice.
learner_voice comes ONLY from the comments: no names, no quotations, themes in your own words; empty lists when the comments
say nothing of the kind or none are supplied. Do not judge how good the teacher is. If is_lesson is false, keep every list empty.
Only the first """ + str(METHOD_SECONDS) + """ seconds of the video are supplied."""

SCIENCE_SYSTEM = """You are writing a research note for the designers of an AI dance teacher. Use ONLY the SOURCES given.
Output a single JSON object:
{"relevant": true|false  (false when the sources are not about learning or teaching movement, music, or the wish to keep practising),
 "principle": "<one sentence: what the research says, in plain words>",
 "findings": [{"finding": "<one plain sentence>", "quote": "<words copied exactly from the source, 8 to 30 words>", "source": "<that source's url, exactly as given>"}],
 "for_the_teacher": ["<one concrete instruction for an online dance teacher that follows from the findings>"],
 "when_it_does_not_apply": "<limits, populations or disagreement stated in the sources; empty if none>",
 "tags": [<up to 3 tags from the list below that the findings bear on>]}
Tags:
""" + TAG_LIST + """
Rules: 2 to 6 findings; every quote is copied character for character from the source it cites; nothing from memory.
Most sources study movement learning in general: never write that they studied dance unless the source says so.
At most 4 instructions, each one something a teacher can do in a lesson."""

# key, English Wikipedia title ("" = none), Europe PMC query ("" = none), the practices it bears on
SCIENCE = [
    ("external_focus", "", 'ABSTRACT:"external focus" AND ABSTRACT:"motor learning"', ["imagery"]),
    ("expectancies_and_autonomy", "", 'ABSTRACT:"enhanced expectancies" AND ABSTRACT:"motor learning"', ["praise_and_expectancy", "autonomy"]),
    ("autonomy_support", "Self-determination theory", 'ABSTRACT:"autonomy support" AND ABSTRACT:"motor learning"', ["autonomy"]),
    ("self_efficacy", "Self-efficacy", 'ABSTRACT:"self-efficacy" AND ABSTRACT:"motor skill" AND ABSTRACT:feedback', ["praise_and_expectancy", "normalise_mistakes"]),
    ("early_success", "", 'ABSTRACT:success AND ABSTRACT:expectancies AND ABSTRACT:"motor learning"', ["quick_win", "praise_and_expectancy"]),
    ("enjoyment_and_staying_with_it", "", 'ABSTRACT:enjoyment AND ABSTRACT:adherence AND ABSTRACT:dance', ["fun_and_energy", "reason_to_return"]),
    ("basic_needs", "", 'ABSTRACT:"basic psychological needs" AND ABSTRACT:dance', ["autonomy", "praise_and_expectancy", "social_connection"]),
    ("habit_formation", "Habit", 'ABSTRACT:"habit formation" AND ABSTRACT:"physical activity"', ["reason_to_return", "recap_and_practice_plan"]),
    ("music_and_reward", "", 'ABSTRACT:music AND ABSTRACT:pleasure AND ABSTRACT:dopamine', ["music_early", "fun_and_energy", "quick_win"]),
    ("observational_learning", "Observational learning", 'ABSTRACT:"observational learning" AND ABSTRACT:"motor skill"', ["demo_first", "mirror_view"]),
    ("action_observation_in_dance", "Mirror neuron", 'ABSTRACT:"action observation" AND ABSTRACT:dance', ["demo_first", "mirror_view"]),
    ("chunking", "Chunking (psychology)", 'ABSTRACT:chunking AND ABSTRACT:"motor sequence"', ["chunking", "layering"]),
    ("part_and_whole_practice", "", 'ABSTRACT:"part practice" AND ABSTRACT:motor', ["chunking", "layering", "demo_first"]),
    ("spacing", "Distributed practice", 'ABSTRACT:"distributed practice" AND ABSTRACT:motor', ["recap_and_practice_plan", "repetition"]),
    ("varied_practice", "Varied practice", 'ABSTRACT:"contextual interference" AND ABSTRACT:"motor learning"', ["play_and_variation", "repetition"]),
    ("challenge_point", "Desirable difficulty", 'ABSTRACT:"challenge point" AND ABSTRACT:motor', ["regression", "progression"]),
    ("adaptive_difficulty", "", 'ABSTRACT:adaptive AND ABSTRACT:difficulty AND ABSTRACT:"motor learning"', ["regression", "progression", "autonomy"]),
    ("individual_differences", "", 'ABSTRACT:"individual differences" AND ABSTRACT:"motor learning"', ["regression", "progression", "body_adaptation"]),
    ("errorless_learning", "Errorless learning", 'ABSTRACT:"errorless learning" AND ABSTRACT:motor', ["regression", "normalise_mistakes"]),
    ("feedback", "Knowledge of results", 'ABSTRACT:"augmented feedback" AND ABSTRACT:"motor learning"', ["error_correction", "self_check"]),
    ("self_controlled_practice", "", 'ABSTRACT:"self-controlled" AND ABSTRACT:"motor learning"', ["autonomy", "self_check"]),
    ("video_feedback", "", 'ABSTRACT:"video feedback" AND ABSTRACT:"motor skill"', ["self_check", "split_screen"]),
    ("motor_imagery", "Motor imagery", 'ABSTRACT:"motor imagery" AND ABSTRACT:dance', ["imagery", "recap_and_practice_plan"]),
    ("analogy_learning", "Implicit learning", 'ABSTRACT:"analogy learning" AND ABSTRACT:motor', ["imagery"]),
    ("rhythm_entrainment", "Entrainment (biomusicology)", 'ABSTRACT:"sensorimotor synchronization" AND ABSTRACT:rhythm', ["counts_and_rhythm", "music_early", "feel_and_groove"]),
    ("groove", "", 'ABSTRACT:groove AND ABSTRACT:music AND ABSTRACT:movement', ["music_early", "feel_and_groove"]),
    ("universals_of_music_and_dance", "", 'ABSTRACT:universal AND ABSTRACT:music AND ABSTRACT:dance AND ABSTRACT:societies', ["feel_and_groove", "culture_and_meaning", "counts_and_rhythm"]),
    ("infants_move_to_rhythm", "", 'ABSTRACT:infants AND ABSTRACT:rhythmic AND ABSTRACT:movement AND ABSTRACT:music', ["feel_and_groove", "counts_and_rhythm"]),
    ("speed_and_accuracy", "", 'ABSTRACT:"speed-accuracy" AND ABSTRACT:"motor learning"', ["tempo_ramp"]),
    ("cognitive_load", "Cognitive load", 'ABSTRACT:"cognitive load" AND ABSTRACT:"motor learning"', ["chunking", "on_screen_counts", "split_screen"]),
    ("words_and_pictures", "Dual-coding theory", 'ABSTRACT:"multimedia learning" AND ABSTRACT:"motor skill"', ["on_screen_counts", "split_screen"]),
    ("mirrors_in_dance", "", 'ABSTRACT:mirror AND ABSTRACT:dance AND ABSTRACT:learning', ["mirror_view", "self_check"]),
    ("online_dance_learning", "", 'ABSTRACT:online AND ABSTRACT:dance AND ABSTRACT:teaching', ["split_screen", "mirror_view", "social_connection"]),
    ("dance_pedagogy", "Dance education", 'ABSTRACT:"dance education" AND ABSTRACT:pedagogy', ["culture_and_meaning", "play_and_variation"]),
    ("beginners", "", 'ABSTRACT:novice AND ABSTRACT:dance AND ABSTRACT:learning', ["quick_win", "chunking"]),
    ("scaffolding", "Instructional scaffolding", 'ABSTRACT:scaffolding AND ABSTRACT:"motor skill"', ["regression", "progression", "layering"]),
    ("zone_of_proximal_development", "Zone of proximal development", "", ["regression", "progression"]),
    ("mastery_learning", "Mastery learning", "", ["repetition", "progression"]),
    ("growth_mindset", "Mindset", 'ABSTRACT:"growth mindset" AND ABSTRACT:sport', ["normalise_mistakes", "praise_and_expectancy"]),
    ("flow", "Flow (psychology)", 'ABSTRACT:flow AND ABSTRACT:dance AND ABSTRACT:experience', ["feel_and_groove", "progression"]),
    ("play", "Play (activity)", 'ABSTRACT:playfulness AND ABSTRACT:adults AND ABSTRACT:learning', ["fun_and_energy", "play_and_variation"]),
    ("overlearning", "Overlearning", "", ["repetition"]),
    ("retrieval_practice", "Testing effect", "", ["self_check", "recap_and_practice_plan"]),
    ("moving_together", "Social learning theory", 'ABSTRACT:dance AND ABSTRACT:synchrony AND ABSTRACT:"social bonding"', ["social_connection"]),
    ("older_learners", "", 'ABSTRACT:dance AND ABSTRACT:"older adults" AND ABSTRACT:balance AND ABSTRACT:intervention', ["body_adaptation"]),
    ("children", "", 'ABSTRACT:dance AND ABSTRACT:children AND ABSTRACT:"motor skill"', ["body_adaptation", "play_and_variation"]),
    ("dance_across_life", "Dance and health", 'ABSTRACT:dance AND ABSTRACT:lifespan', ["body_adaptation", "reason_to_return"]),
    ("embodied_cognition", "Embodied cognition", "", ["feel_and_groove", "culture_and_meaning"]),
    ("gamification", "Gamification of learning", 'ABSTRACT:gamification AND ABSTRACT:"physical activity" AND ABSTRACT:motivation', ["social_connection", "reason_to_return"]),
]
# The open search: one of these a night, in turn; the most cited papers not yet read get a note each. It never ends.
PAPER_QUERIES = [
    'ABSTRACT:dance AND ABSTRACT:teaching AND ABSTRACT:learning', 'ABSTRACT:dance AND ABSTRACT:"motor learning"', 'ABSTRACT:dance AND ABSTRACT:motivation AND ABSTRACT:enjoyment',
    'ABSTRACT:dance AND ABSTRACT:adherence', 'ABSTRACT:dance AND ABSTRACT:beginners', 'ABSTRACT:dance AND ABSTRACT:feedback AND ABSTRACT:learning', 'ABSTRACT:dance AND ABSTRACT:imagery',
    'ABSTRACT:dance AND ABSTRACT:rhythm AND ABSTRACT:synchronization', 'ABSTRACT:dance AND ABSTRACT:"older adults" AND ABSTRACT:cognition', 'ABSTRACT:dance AND ABSTRACT:children AND ABSTRACT:learning',
    'ABSTRACT:dance AND ABSTRACT:"virtual reality" AND ABSTRACT:learning', 'ABSTRACT:dance AND ABSTRACT:"augmented reality"', 'ABSTRACT:dance AND ABSTRACT:online AND ABSTRACT:learning',
    'ABSTRACT:dance AND ABSTRACT:video AND ABSTRACT:instruction', 'ABSTRACT:dance AND ABSTRACT:"self-efficacy"', 'ABSTRACT:dance AND ABSTRACT:creativity AND ABSTRACT:improvisation',
    'ABSTRACT:dance AND ABSTRACT:wellbeing AND ABSTRACT:intervention', 'ABSTRACT:dance AND ABSTRACT:expertise AND ABSTRACT:observation', 'ABSTRACT:music AND ABSTRACT:movement AND ABSTRACT:pleasure',
    'ABSTRACT:"motor learning" AND ABSTRACT:motivation AND ABSTRACT:autonomy', 'ABSTRACT:"skill acquisition" AND ABSTRACT:"augmented feedback"', 'ABSTRACT:dance AND ABSTRACT:"cross-cultural"',
    'ABSTRACT:exergame AND ABSTRACT:dance', 'ABSTRACT:dance AND ABSTRACT:pedagogy AND ABSTRACT:inclusive', 'ABSTRACT:dance AND ABSTRACT:memory AND ABSTRACT:choreography',
    'ABSTRACT:dance AND ABSTRACT:partner AND ABSTRACT:coordination', 'ABSTRACT:dance AND ABSTRACT:anxiety AND ABSTRACT:confidence', 'ABSTRACT:dance AND ABSTRACT:"social bonding"',
]
# What every dance shares. Lessons for people who believe they cannot dance: slug, title, searches (free, yt-dlp).
FOUNDATIONS = [
    ("first-steps", "First steps", [   # for people who believe they cannot dance
        "how to dance for absolute beginners", "learn to dance at home for beginners step by step", "two step dance tutorial for beginners",
        "como aprender a bailar desde cero principiantes", "como dançar para iniciantes passo a passo", "apprendre à danser débutant pas de base",
        "tanzen lernen für anfänger grundschritt", "как научиться танцевать с нуля", "ダンス 初心者 基礎 練習", "डांस कैसे सीखें शुरुआत से", "belajar dance dasar untuk pemula", "零基础 学跳舞 教学"]),
    ("finding-the-beat", "Finding the beat", ["how to find the beat in music for dancing", "how to dance on beat for beginners", "rhythm training for beginner dancers", "cómo encontrar el ritmo para bailar"]),
    ("groove-and-bounce", "Groove and bounce", ["how to groove dance basics for beginners", "bounce and rock basic dance groove tutorial"]),
    ("weight-and-balance", "Weight transfer and balance", ["weight transfer dance tutorial for beginners", "balance exercises for dancers beginners"]),
    ("musicality", "Musicality", ["musicality for dancers tutorial", "how to dance to the music musicality for beginners"]),
    ("confidence", "Confidence and letting go", ["how to dance with confidence for beginners", "how to stop being awkward when dancing"]),
    ("coordination", "Coordination", ["dance coordination exercises for beginners", "arms and legs coordination dance tutorial"]),
    ("isolations", "Isolations", ["body isolations dance tutorial for beginners"]),
    ("partner-connection", "Partner connection", ["lead and follow basics for beginners partner dance", "connection in partner dancing tutorial"]),
    ("freestyle", "Freestyle and improvisation", ["how to freestyle dance for beginners", "dance improvisation exercises for beginners"]),
    ("turns", "Turns and spins", ["how to spin without getting dizzy dance tutorial", "how to turn dance tutorial for beginners"]),
    ("remembering", "Remembering choreography", ["how to remember choreography faster"]),
    ("children", "Teaching children", ["dance lesson for kids beginners follow along", "creative movement dance class for kids"]),
    ("older-beginners", "Older beginners", ["dance lesson for seniors beginners", "chair dance for seniors beginners follow along"]),
    ("party", "Dancing at a party", ["how to dance at a party for beginners", "simple dance moves for weddings beginners"]),
]
# In a paper database "dance" is also the honeybee's waggle dance, and those papers are cited most: keep the search on people.
PEOPLE = (" AND (ABSTRACT:participants OR ABSTRACT:students OR ABSTRACT:dancers OR ABSTRACT:learners OR ABSTRACT:adults OR ABSTRACT:children)"
          " NOT ABSTRACT:bees NOT ABSTRACT:honeybee NOT ABSTRACT:honeybees")
PRAISE = ["finally clicked", "best teacher", "so clear", "i learned so much", "wish i had this earlier", "made it simple", "thank you so much", "understand now", "perfect breakdown",
          "amazing instructor", "patient teacher", "easy to follow", "changed my life", "this works", "helped me a lot", "great teacher", "well explained", "makes sense now",
          "muchas gracias", "muito obrigad", "merci beaucoup", "vielen dank", "спасибо", "ありがとう", "谢谢", "謝謝", "धन्यवाद", "شكرا", "terima kasih", "grazie mille", "teşekkür", "감사합니다"]
COMPLAINT = ["too fast", "confusing", "wrong", "misleading", "inappropriate", "incorrect", "hard to follow", "can't keep up", "muy rápido", "muito rápido", "trop vite", "zu schnell", "слишком быстро", "速すぎ"]

# ------------------------------------------------------------------ small helpers
def channel_key(name):
    return slugify(name or "") or "unknown"

def wilson(pos, n, z=1.64):
    """Lower bound of the share of praise: 9 of 10 counts for less than 90 of 100."""
    if n <= 0:
        return 0.0
    p = pos / n
    return max(0.0, (p + z * z / (2 * n) - z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n)) / (1 + z * z / n))

def _records(folder):
    return {os.path.basename(f)[:-5]: (jload(f, {}) or {}) for f in glob.glob(os.path.join(folder, "*.json"))}

def _secs(t):
    m = re.match(r"^(?:(\d+):)?(\d{1,2}):(\d{2})$", str(t or "").strip())
    return (int(m.group(1) or 0) * 3600 + int(m.group(2)) * 60 + int(m.group(3))) if m else None

def _enum(v, allowed):
    return [x for x in dict.fromkeys(v or []) if x in allowed] if isinstance(v, list) else []

def _days_since(stamp, today=None):
    try:
        return ((today or dt.date.today()) - dt.date.fromisoformat(str(stamp or "")[:10])).days
    except Exception:
        return 10 ** 6

def basics_name(slug):
    return next((title for s, title, _ in FOUNDATIONS if BASICS + s == slug), slug.replace("-", " ")) + " (basics)"

def all_lessons(per_dance, foundations):
    """One list: the crawler's lessons per dance, and the lessons that teach what every dance shares."""
    out = dict(per_dance or {})
    for slug, v in ((foundations or {}).get("topics") or {}).items():
        out[BASICS + slug] = {"lessons": v.get("lessons") or []}
    return out

# ------------------------------------------------------------------ 1. find the lessons every dance shares (free search, comments decide)
def praise(comments):
    low = " \n ".join(comments).lower()
    return sum(low.count(s) for s in PRAISE), sum(low.count(s) for s in COMPLAINT)

def ytdlp_search(q, n=15):
    import shutil, subprocess
    if not shutil.which("yt-dlp"):
        return []
    try:
        out = subprocess.run(["yt-dlp", f"ytsearch{n}:{q}", "--flat-playlist", "--no-warnings", "--print", "id"], capture_output=True, text=True, timeout=90)
        return list(dict.fromkeys(x.strip() for x in out.stdout.splitlines() if x.strip()))[:n]
    except Exception as e:
        warn("yt-dlp search failed:", type(e).__name__)
        return []

def fetch_comments(yid, n=60):
    """The public comments under a lesson (YouTube Data API, one quota unit). Text only: no author is read or kept."""
    try:
        from .hero_qc import _api, YT_KEYS
        if not YT_KEYS:
            return []
        j = _api("commentThreads", {"part": "snippet", "videoId": yid, "order": "relevance", "maxResults": "100", "textFormat": "plainText"})
        out = [re.sub(r"\s+", " ", (((it.get("snippet") or {}).get("topLevelComment") or {}).get("snippet") or {}).get("textDisplay") or "")[:240] for it in j.get("items") or []]
        return [c for c in out if len(c) > 15][:n]
    except Exception as e:
        warn("comments", yid, type(e).__name__)
        return []

def video_facts(ids):
    """Title, channel, length, views and comment count for up to 50 videos (one quota unit). Music videos and films are left out."""
    from .hero_qc import _api, _isodur, SONGHARD, MOVIE
    out = []
    for it in (_api("videos", {"part": "snippet,statistics,contentDetails,status", "id": ",".join(ids[:50])}) or {}).get("items") or []:
        sn, st = it.get("snippet") or {}, it.get("statistics") or {}
        title, ch = sn.get("title") or "", sn.get("channelTitle") or ""
        d = _isodur((it.get("contentDetails") or {}).get("duration"))
        if (120 <= d <= 3600 and int(st.get("commentCount") or 0) > 0 and int(st.get("viewCount") or 0) >= 1500 and (it.get("status") or {}).get("embeddable")
                and str(sn.get("categoryId")) != "10" and not SONGHARD.search(title + " " + ch) and not MOVIE.search(title + " " + ch)):
            out.append({"youtube_id": it["id"], "title": title[:140], "channel": ch, "comments": int(st.get("commentCount") or 0)})
    return sorted(out, key=lambda c: -c["comments"])

def discover_foundations(store, state, searches, per_search=4, today=None):
    """A few searches a night, in turn through FOUNDATIONS. A video becomes a lesson only when learners praise it."""
    flat = [(slug, q) for slug, _, qs in FOUNDATIONS for q in qs]
    seen, added = set(state.get("videos_seen") or []), 0
    topics = store.setdefault("topics", {})
    for _ in range(max(0, searches)):
        i = int(state.get("foundation_search") or 0)
        slug, q = flat[i % len(flat)]
        state["foundation_search"] = i + 1
        new = [x for x in ytdlp_search(q) if x not in seen]
        seen.update(new)
        if not new:
            continue
        have = topics.setdefault(slug, {"lessons": []})["lessons"]
        for c in video_facts(new)[:per_search]:
            pos, neg = praise(fetch_comments(c["youtube_id"], n=100))
            if pos >= 2 and pos > neg and len(have) < 40:
                have.append({"youtube_id": c["youtube_id"], "title": c["title"], "channel": c["channel"], "pos": pos, "neg": neg, "ratio": round(pos / (neg + 1.0), 2),
                             "lesson_status": "foundation", "found_by": q, "found_at": (today or dt.date.today()).isoformat()})
                added += 1
    state["videos_seen"] = sorted(seen)[-6000:]
    return added

# ------------------------------------------------------------------ 2. teachers (crowd wisdom, no model)
def build_teachers(lessons, studied=None, methods=None):
    """lessons: all_lessons(); studied: pedagogy/videos records; methods: pedagogy/methods records (both by video id)."""
    studied, methods, by = studied or {}, methods or {}, {}
    for slug, v in sorted((lessons or {}).items()):
        for l in (v or {}).get("lessons") or []:
            ch, yid = str(l.get("channel") or "").strip(), l.get("youtube_id")
            if not ch or not yid or (studied.get(yid) or {}).get("status") == "not_a_lesson":
                continue
            t = by.setdefault(channel_key(ch), {"key": channel_key(ch), "teacher": ch, "lessons": [], "dances": set(), "praise": 0, "complaints": 0})
            pos, neg = int(l.get("pos") or 0), int(l.get("neg") or 0)
            t["lessons"].append({"youtube_id": yid, "slug": slug, "title": str(l.get("title") or "")[:140], "pos": pos, "neg": neg})
            t["dances"].add(slug); t["praise"] += pos; t["complaints"] += neg
    out = []
    for t in by.values():
        n = t["praise"] + t["complaints"]
        # how sure the praise is, times how much of it there is (100 praising comments = full weight)
        score = round(100 * wilson(t["praise"], n) * min(1.0, math.log10(1 + t["praise"]) / 2), 1)
        ok = sorted((m for m in methods.values() if m.get("teacher_key") == t["key"] and m.get("status") == "ok"), key=lambda m: m.get("analysed_at") or "")
        t["lessons"].sort(key=lambda l: (-l["pos"], l["youtube_id"]))
        out.append({"key": t["key"], "teacher": t["teacher"], "score": score, "praise": t["praise"], "complaints": t["complaints"],
                    "lessons_found": len(t["lessons"]), "dances": sorted(t["dances"]), "lessons": t["lessons"][:12],
                    "methods_studied": len(ok), "system": (ok[-1]["method"].get("teacher_system") if ok else ""),
                    "signature": next((m["method"]["signature"] for m in reversed(ok) if m["method"].get("signature")), "")})
    out.sort(key=lambda t: (-t["score"], -t["lessons_found"], t["key"]))
    for i, t in enumerate(out):
        t["rank"] = i + 1
    return out

# ------------------------------------------------------------------ 3. method study (video + comments, one call)
def _due(rec, today=None):
    """A studied video is done; a failed read waits two days (twice), then a month."""
    if not rec:
        return True
    if rec.get("status") in ("ok", "not_a_lesson"):
        return False
    wait = 2 if (rec.get("status") == "failed" and int(rec.get("attempts") or 1) < 3) else RETRY_DAYS
    return _days_since(rec.get("attempted_at") or rec.get("analysed_at"), today) >= wait

def pick_methods(teachers, methods, budget, per_teacher=3, today=None, want=None, skip=()):
    """Breadth before depth: the best unstudied lesson of every teacher in rank order, then a second, then a third."""
    picked, taken = [], Counter()
    for depth in range(per_teacher):
        for t in teachers:
            if len(picked) >= budget:
                return picked
            if t["methods_studied"] + taken[t["key"]] != depth:
                continue
            for l in t["lessons"]:
                if (want is None or want(l)) and l["youtube_id"] not in skip and _due(methods.get(l["youtube_id"]), today) and all(l["youtube_id"] != p[1]["youtube_id"] for p in picked):
                    picked.append((t, l)); taken[t["key"]] += 1
                    break
    return picked

def _voice(v):
    out = []
    for x in (v or []) if isinstance(v, list) else []:
        if isinstance(x, dict) and str(x.get("theme") or "").strip():
            try:
                c = max(1, min(60, int(x.get("count") or 1)))
            except Exception:
                c = 1
            out.append({"theme": str(x["theme"]).strip()[:120], "tag": x.get("tag") if x.get("tag") in PRACTICES else "other", "count": c})
    return out[:8]

def normalise_method(jd):
    """Keep only what fits the vocabulary; an item without a real timestamp or a known tag is dropped, not guessed."""
    sc = jd.get("screen") if isinstance(jd.get("screen"), dict) else {}
    pc = jd.get("pace") if isinstance(jd.get("pace"), dict) else {}
    lv = jd.get("learner_voice") if isinstance(jd.get("learner_voice"), dict) else {}
    return {
        "teacher_system": str(jd.get("teacher_system") or "").strip()[:500],
        "signature": str(jd.get("signature") or "").strip()[:300],
        "screen": {"views": _enum(sc.get("views"), VIEWS), "on_screen": _enum(sc.get("on_screen"), ON_SCREEN), "editing": _enum(sc.get("editing"), EDITING)},
        "practices": [{"tag": p["tag"], "t": str(p.get("t"))[:8], "what": str(p.get("what") or "").strip()[:220]}
                      for p in (jd.get("practices") or []) if isinstance(p, dict) and p.get("tag") in PRACTICES and _secs(p.get("t")) is not None and str(p.get("what") or "").strip()][:12],
        "adaptations": [{"t": str(a.get("t"))[:8], "difficulty": str(a.get("difficulty") or "").strip()[:200], "adjustment": str(a.get("adjustment") or "").strip()[:240],
                         "kind": a.get("kind") if a.get("kind") in ADAPT_KINDS else "other"}
                        for a in (jd.get("adaptations") or []) if isinstance(a, dict) and _secs(a.get("t")) is not None and str(a.get("difficulty") or "").strip() and str(a.get("adjustment") or "").strip()][:6],
        "entry_points": _enum(jd.get("entry_points"), ENTRY),
        "pace": {"talk_vs_move": pc.get("talk_vs_move") if pc.get("talk_vs_move") in ("mostly_talk", "balanced", "mostly_move") else None,
                 "seconds_before_first_movement": pc.get("seconds_before_first_movement") if isinstance(pc.get("seconds_before_first_movement"), int) and 0 <= pc["seconds_before_first_movement"] <= METHOD_SECONDS else None,
                 "pieces_taught": pc.get("pieces_taught") if isinstance(pc.get("pieces_taught"), int) and 0 < pc["pieces_taught"] < 60 else None},
        "learner_voice": {k: _voice(lv.get(k)) for k in ("struggles", "clicked", "requests")},
        "limits": str(jd.get("limits") or "").strip()[:300]}

def study(teacher, lesson, dance_name, llm, comments=()):
    yid = lesson["youtube_id"]
    url = f"https://www.youtube.com/watch?v={yid}"
    user = (f"DANCE OR TOPIC: {dance_name}\nVIDEO TITLE: {lesson.get('title')}\nTEACHER (channel): {teacher['teacher']}\n\n"
            f"LEARNER COMMENTS ({len(comments)} supplied):\n" + ("\n".join("- " + c for c in comments) if comments else "(none supplied)"))
    jd = llm.json(METHOD_SYSTEM, user, strong=False, temperature=0.1, max_tokens=3500, video_url=url, video_seconds=METHOD_SECONDS)
    rec = {"youtube_id": yid, "slug": lesson.get("slug"), "dance": dance_name, "title": lesson.get("title"), "teacher": teacher["teacher"],
           "teacher_key": teacher["key"], "teacher_score": teacher["score"], "analysed_at": now_iso(), "url": url, "comments_read": len(comments),
           "window": {"start_s": 0, "end_s": METHOD_SECONDS, "resolution": "low", "human_verified": False}}
    if not isinstance(jd, dict):
        rec["status"] = "failed"
    elif jd.get("is_lesson") is False:
        rec["status"] = "not_a_lesson"
    else:
        rec["method"] = normalise_method(jd)
        rec["status"] = "ok" if (rec["method"]["practices"] or rec["method"]["teacher_system"]) else "failed"
    return rec

def save_method(rec):
    """A failed read never replaces a studied one (the same rule as the lesson study)."""
    path = os.path.join(METHODS_DIR, rec["youtube_id"] + ".json")
    prev = jload(path, {}) or {}
    rec["attempts"] = int(prev.get("attempts") or (1 if prev else 0)) + 1
    if rec["status"] != "ok" and prev.get("status") == "ok":
        prev["attempted_at"], prev["attempts"] = rec["analysed_at"], rec["attempts"]
        jsave(path, prev)
        return "kept"
    jsave(path, rec)
    return rec["status"]

# ------------------------------------------------------------------ 4. research (open sources, checked quotes)
def europe_pmc(query, n=4):
    """The most cited papers whose ABSTRACT matches; abstracts are open to read. No key, no cost."""
    if not query:
        return []
    u = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(
        {"query": query + (PEOPLE if "ABSTRACT:dance" in query else "") + " AND HAS_ABSTRACT:y", "format": "json", "resultType": "core", "pageSize": str(max(12, min(60, 3 * n))), "sort": "CITED desc"})
    out = []
    for r in ((get_json(u, timeout=60, retries=2) or {}).get("resultList") or {}).get("result") or []:
        ab = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.get("abstractText") or "")).strip()
        if len(ab) < 400 or not r.get("id"):
            continue
        out.append({"url": f"https://europepmc.org/article/{r.get('source') or 'MED'}/{r['id']}", "kind": "paper",
                    "title": str(r.get("title") or "").strip().rstrip("."), "authors": str(r.get("authorString") or "")[:160], "year": str(r.get("pubYear") or ""),
                    "journal": (((r.get("journalInfo") or {}).get("journal") or {}).get("title") or ""), "cited_by": int(r.get("citedByCount") or 0), "text": ab[:4000]})
        if len(out) >= n:
            break
    return out

def science_sources(item):
    key, wiki, query, _ = item
    src = []
    if wiki:
        try:
            from .sources import wiki_page
            wp = wiki_page(wiki)
            if wp and not wp.get("disambiguation") and len(wp.get("text") or "") > 800:
                src.append({"url": wp["url"], "kind": "encyclopedia", "title": wp["title"], "authors": "Wikipedia contributors", "year": "", "journal": "Wikipedia", "cited_by": 0, "text": wp["text"][:9000]})
        except Exception as e:
            warn("science wiki", key, type(e).__name__)
    try:
        src += europe_pmc(query)
    except Exception as e:
        warn("science europe pmc", key, type(e).__name__)
    return src

def science_note(item, llm, sources=None, topic=None):
    """item = (key, wikipedia title, query, tags). With no tags given (a paper from the open search) the model proposes up to three."""
    from .research import _vnorm, _quote_in
    key, _, _, tags = item
    src = science_sources(item) if sources is None else sources
    rec = {"key": key, "topic": topic or key.replace("_", " "), "tags": [t for t in tags if t in PRACTICES], "written_at": now_iso(),
           "sources": [{k: s[k] for k in ("url", "kind", "title", "authors", "year", "journal", "cited_by")} for s in src]}
    if not src:
        rec["status"] = "no_sources"; return rec
    user = f"TOPIC: {rec['topic']}\n\nSOURCES:\n" + "\n\n".join(f"[{s['url']}] {s['title']} ({s['authors']}, {s['year']}) {s['journal']}\n{s['text']}" for s in src)
    jd = llm.json(SCIENCE_SYSTEM, user, strong=False, temperature=0.1, max_tokens=2500)
    if not isinstance(jd, dict):
        rec["status"] = "failed"; return rec
    texts = {s["url"]: _vnorm(s["text"]) for s in src}
    good = []
    for f in (jd.get("findings") or []) if isinstance(jd.get("findings"), list) else []:
        if not isinstance(f, dict):
            continue
        q, u = _vnorm(f.get("quote")), str(f.get("source") or "").strip()
        if u in texts and len(q.split()) >= 6 and _quote_in(q, texts[u]) and str(f.get("finding") or "").strip():
            good.append({"finding": str(f["finding"]).strip()[:300], "quote": str(f["quote"]).strip()[:320], "source": u})
    rec["quotes_offered"], rec["findings"] = len(jd.get("findings") or []), good[:6]
    rec["principle"] = str(jd.get("principle") or "").strip()[:400]
    rec["for_the_teacher"] = [str(x).strip()[:260] for x in (jd.get("for_the_teacher") or []) if isinstance(x, str) and x.strip()][:4]
    rec["when_it_does_not_apply"] = str(jd.get("when_it_does_not_apply") or "").strip()[:400]
    if not rec["tags"]:
        rec["tags"] = _enum(jd.get("tags"), PRACTICES)[:3]
    # a note stands only on quotes that are really in the sources: fewer than two, and it is not used
    rec["status"] = "ok" if (jd.get("relevant") is not False and len(good) >= 2 and rec["principle"] and rec["tags"]) else "thin"
    return rec

def pick_science(notes, n, today=None):
    due = []
    for item in SCIENCE:
        rec = notes.get(item[0])
        if not rec:
            due.append((0, item))
        elif _days_since(rec.get("written_at"), today) >= (SCIENCE_REFRESH_DAYS if rec.get("status") == "ok" else RETRY_DAYS):
            due.append((1, item))
    due.sort(key=lambda x: x[0])
    return [item for _, item in due[:max(0, n)]]

def paper_key(p):
    return "paper-" + re.sub(r"[^A-Za-z0-9]+", "-", p["url"].split("/article/")[-1]).strip("-").lower()

def discover_papers(state, notes, n, search=None):
    """The open search: tonight's query, its most cited papers that have no note yet."""
    if n <= 0:
        return []
    i = int(state.get("paper_search") or 0)
    state["paper_search"] = i + 1
    seen = set(state.get("papers_seen") or [])
    fresh = [p for p in (search or europe_pmc)(PAPER_QUERIES[i % len(PAPER_QUERIES)], n=20) if paper_key(p) not in seen and paper_key(p) not in notes][:n]
    state["papers_seen"] = sorted(seen | {paper_key(p) for p in fresh})[-8000:]
    return fresh

# ------------------------------------------------------------------ 5. the join (no model)
def _link(m, t):
    s = _secs(t)
    return m["url"] + (f"&t={s}s" if s else "")

def fuse(teachers, methods, notes, family_of=None, today=None):
    family_of = family_of or {}
    fam = lambda m: "the basics" if str(m.get("slug") or "").startswith(BASICS) else (family_of.get(m.get("slug")) or "other")
    oks = sorted((m for m in methods.values() if m.get("status") == "ok" and m.get("method")), key=lambda m: (-(m.get("teacher_score") or 0), m["youtube_id"]))
    score = {t["key"]: t["score"] for t in teachers}
    keys = sorted({m["teacher_key"] for m in oks}, key=lambda k: (-score.get(k, 0), k))
    top = set(keys[:len(keys) // 3]) if len(keys) >= 6 else set()   # the best-ranked third, once there are enough to compare
    sci = [n for n in notes.values() if n.get("status") == "ok"]
    cites = lambda n: max([int(s.get("cited_by") or 0) for s in n.get("sources") or []] or [0])
    practices = []
    for tag, meaning in PRACTICES.items():
        using = [m for m in oks if any(p["tag"] == tag for p in m["method"]["practices"])]
        who = sorted({m["teacher_key"] for m in using})
        voice = {k: sum(v["count"] for m in oks for v in m["method"]["learner_voice"][k] if v["tag"] == tag) for k in ("struggles", "clicked", "requests")}
        themes = Counter()
        for m in oks:
            for k in ("struggles", "clicked", "requests"):
                for v in m["method"]["learner_voice"][k]:
                    if v["tag"] == tag:
                        themes[(k, v["theme"].lower())] += v["count"]
        ns = sorted((n for n in sci if tag in (n.get("tags") or [])), key=lambda n: (n["key"].startswith("paper-"), -len(n.get("findings") or []), -cites(n), n["key"]))
        seen, examples = set(), []
        for m in using:   # one example per teacher, best-ranked first
            for p in m["method"]["practices"]:
                if p["tag"] == tag and m["teacher"] not in seen:
                    seen.add(m["teacher"])
                    examples.append({"teacher": m["teacher"], "dance": m.get("dance"), "t": p["t"], "what": p["what"], "url": _link(m, p["t"])})
        share = lambda group: (round(sum(1 for m in group if any(p["tag"] == tag for p in m["method"]["practices"])) / len(group), 2) if group else None)
        practices.append({"tag": tag, "meaning": meaning, "do": PRACTICE[tag][1], "lessons": len(using), "teachers": len(who), "families": len({fam(m) for m in using}),
                          "share_of_lessons": share(oks),
                          "share_best_ranked": share([m for m in oks if m["teacher_key"] in top]) if top else None,
                          "share_others": share([m for m in oks if m["teacher_key"] not in top]) if top else None,
                          "learner_voice": voice, "learner_themes": [{"kind": k, "theme": th, "count": c} for (k, th), c in themes.most_common(4)],
                          "science": [{"key": n["key"], "topic": n.get("topic"), "principle": n.get("principle"), "for_the_teacher": n.get("for_the_teacher") or [],
                                       "sources": [s["url"] for s in n.get("sources") or []][:4]} for n in ns[:4]],
                          "science_notes": len(ns), "examples": examples[:4],
                          # three kinds of evidence: several teachers do it, learners talk about it, research supports it
                          "evidence_kinds": int(len(who) >= 3) + int(sum(voice.values()) >= 3) + int(bool(ns))})
    by_tag = {p["tag"]: p for p in practices}
    practices.sort(key=lambda p: (-p["evidence_kinds"], -p["teachers"], -sum(p["learner_voice"].values()), p["tag"]))
    adapt = []
    for m in oks:
        for a in m["method"]["adaptations"]:
            adapt.append({"kind": a["kind"], "tag": ADAPT_KINDS.get(a["kind"]), "difficulty": a["difficulty"], "adjustment": a["adjustment"],
                          "teacher": m["teacher"], "dance": m.get("dance"), "url": _link(m, a["t"])})
    struggles = Counter()
    for m in oks:
        for v in m["method"]["learner_voice"]["struggles"]:
            struggles[(v["tag"], v["theme"].lower())] += v["count"]
    # how BDF adjusts: what learners say is hard → what the teachers offer for it → what the research adds
    adjust = []
    weight = lambda tag: sum(c for (x, _), c in struggles.items() if x == tag)
    for tag in sorted({t for t, _ in struggles if t in by_tag}, key=lambda t: (-weight(t), t)):
        offers = [a for a in adapt if a["tag"] == tag][:3] or [{"difficulty": "", "adjustment": e["what"], "teacher": e["teacher"], "dance": e["dance"], "url": e["url"]} for e in by_tag[tag]["examples"][:2]]
        adjust.append({"tag": tag, "comments": weight(tag), "learners_say": [th for (x, th), _ in struggles.most_common() if x == tag][:3],
                       "teachers_offer": [{k: o[k] for k in ("difficulty", "adjustment", "teacher", "dance", "url")} for o in offers],
                       "research": [x for n in by_tag[tag]["science"][:2] for x in n["for_the_teacher"][:1]]})
    dna = [{"theme": theme, "tag": t, "do": PRACTICE[t][1], "evidence_kinds": by_tag[t]["evidence_kinds"], "teachers": by_tag[t]["teachers"], "families": by_tag[t]["families"],
            "learner_comments": sum(by_tag[t]["learner_voice"].values()), "research_notes": by_tag[t]["science_notes"]}
           for theme, tags in THEMES for t in tags if by_tag[t]["evidence_kinds"] >= 2]
    count = lambda field, allowed: [[k, c] for k, c in Counter(x for m in oks for x in (m["method"]["screen"][field] if field in ("views", "on_screen", "editing") else m["method"][field])).most_common() if k in allowed]
    waits = sorted(m["method"]["pace"]["seconds_before_first_movement"] for m in oks if m["method"]["pace"]["seconds_before_first_movement"] is not None)
    week = [m for m in oks if _days_since(m.get("analysed_at"), today) < 7]
    note_out = lambda n: {"key": n["key"], "topic": n.get("topic"), "tags": n.get("tags"), "principle": n.get("principle"), "findings": n.get("findings"),
                          "for_the_teacher": n.get("for_the_teacher"), "when_it_does_not_apply": n.get("when_it_does_not_apply"), "cited_by": cites(n),
                          "sources": [{k: s.get(k) for k in ("url", "title", "authors", "year", "journal")} for s in n.get("sources") or []]}
    topics = sorted((n for n in sci if not n["key"].startswith("paper-")), key=lambda n: n["key"])
    papers = sorted((n for n in sci if n["key"].startswith("paper-")), key=lambda n: (-cites(n), n["key"]))
    return {"contract": "da_bdf_teaching_v1", "generated_at": now_iso(),
            "counts": {"teachers_ranked": len(teachers), "teachers_studied": len(keys), "lessons_studied_for_method": len(oks),
                       "dances_covered": len({m.get("slug") for m in oks if not str(m.get("slug") or "").startswith(BASICS)}),
                       "basics_lessons_studied": sum(1 for m in oks if str(m.get("slug") or "").startswith(BASICS)),
                       "families_covered": len({fam(m) for m in oks}), "adaptations_seen": len(adapt),
                       "comments_read": sum(int(m.get("comments_read") or 0) for m in oks),
                       "science_notes": len(topics), "science_topics_total": len(SCIENCE), "paper_notes": len(papers),
                       "science_findings_checked": sum(len(n.get("findings") or []) for n in sci),
                       "practices_total": len(PRACTICES), "practices_with_two_or_more_kinds": sum(1 for p in practices if p["evidence_kinds"] >= 2),
                       "practices_with_all_three": sum(1 for p in practices if p["evidence_kinds"] == 3)},
            "new_in_7_days": {"lessons": len(week), "teachers": sorted({m["teacher"] for m in week})[:12],
                              "research_notes": sum(1 for n in sci if _days_since(n.get("written_at"), today) < 7)},
            "dna": dna, "adjustments": adjust, "practices": practices, "adaptations": adapt[:400],
            "struggles": [{"tag": t, "theme": th, "count": c} for (t, th), c in struggles.most_common(40)],
            "screen": {"views": count("views", VIEWS), "on_screen": count("on_screen", ON_SCREEN), "editing": count("editing", EDITING)},
            "entry_points": count("entry_points", ENTRY),
            "pace": {"median_seconds_before_first_movement": waits[len(waits) // 2] if waits else None,
                     "talk_vs_move": Counter(m["method"]["pace"]["talk_vs_move"] for m in oks if m["method"]["pace"]["talk_vs_move"]).most_common()},
            "teachers": [{k: t[k] for k in ("rank", "teacher", "score", "praise", "complaints", "lessons_found", "methods_studied", "system", "signature")} | {"dances": t["dances"][:8]}
                         for t in teachers if t["methods_studied"]][:80],
            "science": [note_out(n) for n in topics], "papers": [note_out(n) for n in papers[:300]]}

def render(s):
    c, L = s["counts"], []
    stars = {0: "—", 1: "●", 2: "●●", 3: "●●●"}
    name = lambda tag: tag.replace("_", " ").capitalize()
    pl = lambda n, one, many=None: f"{n:,} {one if n == 1 else (many or one + 's')}"
    L += ["# How to teach anyone to dance — the evidence behind the Best Dance Friend", "",
          f"_Rebuilt {s['generated_at'][:10]} by `pipeline/teaching.py`. It grows every night at no cost. These are machine readings, not yet reviewed by a person: every line links to the moment in the video or to the source. The first three sections are the summary; everything after them is the evidence._", "",
          "## Where the research stands", "", "| | |", "|---|---:|",
          f"| Teachers ranked by what learners wrote under their lessons | {c['teachers_ranked']:,} |",
          f"| Teachers whose method has been studied | {c['teachers_studied']:,} |",
          f"| Lessons watched for teaching method | {c['lessons_studied_for_method']:,} ({c['basics_lessons_studied']:,} of them teach the basics every dance shares) |",
          f"| Dances and dance families those lessons cover | {c['dances_covered']:,} dances, {c['families_covered']:,} families |",
          f"| Learner comments read (kept as themes, no names) | {c['comments_read']:,} |",
          f"| Moments where a teacher adapts to a difficulty | {c['adaptations_seen']:,} |",
          f"| Research notes with checked quotes | {c['science_notes']} of {c['science_topics_total']} topics, and {pl(c['paper_notes'], 'paper')} from the open search ({c['science_findings_checked']:,} findings) |",
          f"| Teaching practices backed by two or more kinds of evidence | {c['practices_with_two_or_more_kinds']} of {c['practices_total']} ({c['practices_with_all_three']} by all three) |", "",
          "Three kinds of evidence are joined for every practice: **teachers** (at least three ranked teachers do it), **learners** (their comments speak of it) and **research** (a note with checked quotes). ●●● means all three.", ""]
    n7 = s["new_in_7_days"]
    L += [f"New in the last seven days: {n7['lessons']} lessons studied" + (f" ({', '.join(n7['teachers'][:8])})" if n7["teachers"] else "") + f", {n7['research_notes']} research notes.", ""]
    L += ["## The teaching DNA so far", "", "What a teacher does, wherever two or more kinds of evidence agree. This list grows and changes as the evidence does.", ""]
    if not s["dna"]:
        L += ["Nothing has two kinds of evidence yet. The first rules appear after a few nights of study.", ""]
    for theme, _ in THEMES:
        rows = [d for d in s["dna"] if d["theme"] == theme]
        if rows:
            L.append(f"**{theme}**")
            L += [f"- {d['do']} {stars[d['evidence_kinds']]} ({pl(d['teachers'], 'teacher')} in {pl(d['families'], 'dance family', 'dance families')}; {pl(d['learner_comments'], 'learner comment')}; {pl(d['research_notes'], 'research note')})" for d in rows]
            L.append("")
    L += ["## How the Best Dance Friend adjusts", "", "What learners say is hard, what the teachers offer for it, and what the research adds. Built only from the evidence below.", ""]
    if not s["adjustments"]:
        L += ["No learner difficulty has been matched to a teacher's answer yet.", ""]
    for a in s["adjustments"][:14]:
        L.append(f"**{name(a['tag'])}** ({pl(a['comments'], 'comment')})")
        L.append("- Learners say: " + "; ".join(a["learners_say"]))
        L += [f"- A teacher's answer: {(o['difficulty'] + ' → ') if o['difficulty'] else ''}{o['adjustment']} ([{o['teacher']}, {o['dance']}]({o['url']}))" for o in a["teachers_offer"][:2]]
        L += [f"- Research: {x}" for x in a["research"][:1]]
        L.append("")
    L += ["## The teaching practices, strongest evidence first", ""]
    for p in s["practices"]:
        if not (p["lessons"] or p["science"] or sum(p["learner_voice"].values())):
            continue
        L.append(f"### {name(p['tag'])} {stars[p['evidence_kinds']]}")
        L.append(f"_{p['meaning']}._")
        bits = [f"{pl(p['teachers'], 'teacher')} in {pl(p['lessons'], 'lesson')} and {pl(p['families'], 'dance family', 'dance families')}" + (f" ({p['share_of_lessons']:.0%} of lessons studied)" if p["share_of_lessons"] is not None else "")]
        if p["share_best_ranked"] is not None:
            bits.append(f"best-ranked third {p['share_best_ranked']:.0%}, the others {p['share_others']:.0%}")
        v = p["learner_voice"]
        if sum(v.values()):
            bits.append(f"learners: {v['clicked']} say it made the lesson work, {v['struggles']} struggle here, {v['requests']} ask for it")
        L.append("- Evidence: " + "; ".join(bits) + ".")
        L += [f"- {e['teacher']} ({e['dance']}, [{e['t']}]({e['url']})): {e['what']}" for e in p["examples"][:3]]
        L += [f"- Learners ({ {'struggles': 'find hard', 'clicked': 'say it clicked', 'requests': 'ask for'}[th['kind']] }, {th['count']}): {th['theme']}" for th in p["learner_themes"][:2]]
        L += [f"- Research ({str(n['topic'])[:70]}): {n['principle']}" + (" → " + n["for_the_teacher"][0] if n["for_the_teacher"] else "") for n in p["science"][:2]]
        L.append("")
    L += ["## When a learner struggles: what the teachers offer", "",
          "Only what a teacher actually says or shows as an alternative; the link opens the video at that moment.", ""]
    by = {}
    for a in s["adaptations"]:
        by.setdefault(a["kind"], []).append(a)
    for kind in ADAPT_KINDS:
        if by.get(kind):
            L.append(f"**{name(kind)}** ({len(by[kind])} seen)")
            L += [f"- When: {a['difficulty']} → {a['adjustment']} ([{a['teacher']}, {a['dance']}]({a['url']}))" for a in by[kind][:8]]
            L.append("")
    if s["struggles"]:
        L += ["## What learners say they find hard", ""] + [f"- {x['theme']} ({x['count']} comments; {x['tag'].replace('_', ' ')})" for x in s["struggles"][:20]] + [""]
    sc = s["screen"]
    if sc["views"] or s["entry_points"]:
        fmt = lambda rows: ", ".join(f"{k.replace('_', ' ')} {n}" for k, n in rows) or "nothing recorded yet"
        L += ["## The screen and the way in", "", f"- Views used (lessons): {fmt(sc['views'])}", f"- Written on screen: {fmt(sc['on_screen'])}", f"- Editing: {fmt(sc['editing'])}",
              f"- Ways into the dance: {fmt(s['entry_points'])}"]
        if s["pace"]["median_seconds_before_first_movement"] is not None:
            L.append(f"- Typical wait before the learner first moves: {s['pace']['median_seconds_before_first_movement']} seconds; talk and movement: {fmt(s['pace']['talk_vs_move'])}")
        L.append("")
    if s["teachers"]:
        L += ["## The teachers studied so far, by learners' praise", "", "The score is how sure and how plentiful the praise in the comments is (0 to 100). It ranks who to study next; it is not a verdict.", ""]
        for t in s["teachers"][:40]:
            L.append(f"**{t['rank']}. {t['teacher']}** (score {t['score']}; {t['lessons_found']} lessons found; {', '.join(d.replace(BASICS, 'basics: ').replace('-', ' ') for d in t['dances'][:4])})")
            if t["system"]:
                L.append(f"- System: {t['system']}")
            if t["signature"]:
                L.append(f"- What stands out: {t['signature']}")
            L.append("")
    def notes(rows, limit):
        out = []
        for n in rows[:limit]:
            out.append(f"### {str(n['topic']).capitalize()[:110]}")
            out.append(n["principle"] or "")
            out += [f"- {f['finding']} — \"{f['quote']}\" ([source]({f['source']}))" for f in (n["findings"] or [])[:4]]
            out += [f"- For the teacher: {x}" for x in (n["for_the_teacher"] or [])[:3]]
            if n["when_it_does_not_apply"]:
                out.append(f"- Limits: {n['when_it_does_not_apply']}")
            out.append("")
        return out
    if s["science"] or s["papers"]:
        L += ["## What the research says", "", "Each finding stands on words copied from the source and checked against it. Most studies are about learning movement in general, not dance.", ""]
        L += notes(s["science"], 80)
        if s["papers"]:
            L += [f"## Papers found by the open search ({len(s['papers'])}; the most cited first)", ""] + notes(s["papers"], 40)
    L += ["## How to read this", "",
          "- The ranking uses learners' comments only. Views and likes are not used.",
          "- A machine watched the first ten minutes of each lesson at low resolution. It can miss or misread a moment: open the link before relying on a line.",
          "- Nothing here is medical or safety advice, and nothing here has been tested on learners by Dance Atlas yet.", ""]
    return "\n".join(L)

# ------------------------------------------------------------------ the stage
def run(budget=8, science=None, only=None):
    rep = Report("teaching")
    for d in (METHODS_DIR, SCIENCE_DIR):
        os.makedirs(d, exist_ok=True)
    env = lambda k, v: int(os.environ.get(k, v))
    state, store = jload(STATE, {}) or {}, jload(FOUNDATION_LESSONS, {}) or {}
    studied, methods, notes = _records(os.path.join(PED, "videos")), _records(METHODS_DIR), _records(SCIENCE_DIR)
    llm = LLM()
    cat = (jload(os.path.join("public", "catalog", "dances.app.json"), {}) or {}).get("styles") or {}
    deadline = time.time() + 60 * env("TEACHING_MAX_MINUTES", "40")
    live = bool(llm.enabled and llm.gemini_key)
    if live and not only:
        try:
            rep.inc("basics_lessons_found", discover_foundations(store, state, env("FOUNDATION_SEARCHES", "3")))
            jsave(FOUNDATION_LESSONS, store); jsave(STATE, state)
        except Exception as e:
            rep.error(f"foundation search: {e}")
    lessons = all_lessons(jload(LESSONS, {}) or {}, store)
    teachers = build_teachers(lessons, studied, methods)
    per, n = env("METHOD_PER_TEACHER", "3"), (budget if live else 0)
    basics = pick_methods(teachers, methods, min(n, env("BASICS_SHARE", "3")), per, want=lambda l: l["slug"].startswith(BASICS))
    targets = basics + pick_methods(teachers, methods, n - len(basics), per, skip={l["youtube_id"] for _, l in basics})
    if only:
        targets = [(t, l) for t, l in targets if l["slug"] in only or l["youtube_id"] in only]
    rep.note(f"teachers ranked: {len(teachers)}; lessons to study for method: {len(targets)} (budget {budget}, {len(basics)} on the basics); engine {'on' if live else 'off: tables only'}")
    misses = 0
    for t, l in targets:
        if time.time() > deadline or misses >= 3:   # three unreadable videos in a row: the model or the day's quota is gone
            rep.inc("stopped_early"); break
        try:
            name = basics_name(l["slug"]) if l["slug"].startswith(BASICS) else ((cat.get(l["slug"]) or {}).get("name") or l["slug"].replace("-", " "))
            rec = study(t, l, name, llm, fetch_comments(l["youtube_id"]))
            rep.inc("method_" + save_method(rec))
            misses = misses + 1 if rec["status"] == "failed" else 0
            log(f"TEACHING {t['teacher']} / {l['slug']} {l['youtube_id']}: {rec['status']}" + (f" practices={len(rec['method']['practices'])} adaptations={len(rec['method']['adaptations'])}" if rec["status"] == "ok" else ""))
        except Exception as e:
            rep.error(f"teaching {l.get('youtube_id')}: {e}")
    todo = []
    if live and misses < 3:
        todo = [(item, None, None) for item in pick_science(notes, env("SCIENCE_BUDGET", "3") if science is None else science)]
        try:
            todo += [((paper_key(p), "", "", []), [p], p["title"]) for p in discover_papers(state, notes, env("PAPER_BUDGET", "2") if science is None else 0)]
            jsave(STATE, state)
        except Exception as e:
            rep.error(f"open paper search: {e}")
    for item, sources, topic in todo:
        if time.time() > deadline:
            rep.inc("stopped_early"); break
        try:
            note = science_note(item, llm, sources=sources, topic=topic)
            prev = notes.get(item[0]) or {}
            if note["status"] != "ok" and prev.get("status") == "ok":   # a failed refresh never replaces a good note
                rep.inc("science_kept"); continue
            jsave(os.path.join(SCIENCE_DIR, item[0] + ".json"), note)
            rep.inc(("paper_" if sources else "science_") + note["status"])
            log(f"SCIENCE {item[0]}: {note['status']} ({len(note.get('findings') or [])} checked of {note.get('quotes_offered', 0)} quotes)")
        except Exception as e:
            rep.error(f"science {item[0]}: {e}")
    methods, notes = _records(METHODS_DIR), _records(SCIENCE_DIR)
    teachers = build_teachers(lessons, studied, methods)
    jsave(TEACHERS, {"generated_at": now_iso(), "ranked_by": "learners' comments under the lessons (praise and complaints counted in the comments)", "teachers": teachers[:400]})
    s = fuse(teachers, methods, notes, family_of={k: v.get("family") for k, v in cat.items() if isinstance(v, dict)})
    jsave(SYSTEM_JSON, s)
    os.makedirs(os.path.dirname(PUBLIC_JSON), exist_ok=True)
    jsave(PUBLIC_JSON, s)
    with open(DOC, "w", encoding="utf-8") as f:
        f.write(render(s))
    llm.record(rep)
    c = s["counts"]
    rep.note(f"teaching research: {c['lessons_studied_for_method']} lessons of {c['teachers_studied']} teachers studied, {c['science_notes']} topic notes and {c['paper_notes']} paper notes, "
             f"{c['practices_with_two_or_more_kinds']} practices with two or more kinds of evidence")
    return rep.finish()

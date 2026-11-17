"""Offline checks for 17 November 2026: a patient model client (the first full night's lesson) and the teaching research mission."""
import datetime as dt
import json
import os
import unittest
from unittest.mock import patch
from . import common, spending, teaching
from .common import jload, jsave
from .test_engine import LISTED, Project, free_policy

ANSWER = (200, json.dumps({"candidates": [{"content": {"parts": [{"text": "{\"ok\": true}"}]}}]}), {})
EMPTY = (200, json.dumps({"candidates": [{"finishReason": "OTHER"}]}), {})
BUSY = common.HttpError(503, '{"error": {"status": "UNAVAILABLE", "message": "high demand"}}', "https://example.org")
ONE_MODEL = {"models": [{"name": "models/gemini-3.5-flash-lite", "supportedGenerationMethods": ["generateContent"]}]}


class PatientClientTests(unittest.TestCase):
    def setUp(self):
        common.LLM.WAITED = 0.0
        self.clock = [1000.0]

    def llm(self):
        with patch.object(spending, "_ALLOWANCE", spending.ModelAllowance(free_policy())), patch.dict("os.environ", {"GEMINI_API_KEY": "fixture"}):
            return common.LLM()

    def running(self, listed, answers, env=None):
        """The provider's model list, its answers in order, and a clock that only moves when the client sleeps."""
        return (patch.object(common, "get_json", return_value=listed), patch.object(common, "http", side_effect=answers),
                patch.object(common.time, "time", side_effect=lambda: self.clock[0]),
                patch.object(common.time, "sleep", side_effect=lambda s: self.clock.__setitem__(0, self.clock[0] + s)),
                patch.dict("os.environ", env or {}))

    def test_a_question_waits_for_the_resting_model_instead_of_being_dropped(self):
        llm = self.llm()
        a, b, c, d, e = self.running(ONE_MODEL, [BUSY, ANSWER])
        with a, b as http, c, d, e:
            self.assertEqual(llm.json("system", "user"), {"ok": True})
            self.assertEqual(http.call_count, 2)
        self.assertEqual((llm.unanswered, llm.why.get("overloaded")), (0, 1))
        self.assertTrue(40 <= common.LLM.WAITED <= 60, common.LLM.WAITED)        # the first rest is short: 45 seconds
        self.assertNotIn("gemini-3.5-flash-lite", llm.dead)

    def test_the_waiting_is_bounded_for_the_whole_run(self):
        llm = self.llm()
        a, b, c, d, e = self.running(ONE_MODEL, [BUSY, ANSWER], {"LLM_WAIT_BUDGET_SECONDS": "30"})
        with a, b as http, c, d, e:
            self.assertIsNone(llm.json("system", "user"))
            self.assertEqual(http.call_count, 1)
        self.assertEqual((llm.unanswered, common.LLM.WAITED), (1, 0.0))

    def test_a_model_that_stays_overloaded_rests_longer_each_time_up_to_the_cap(self):
        llm = self.llm()
        a, b, c, d, e = self.running(ONE_MODEL, [BUSY, BUSY, BUSY, ANSWER], {"LLM_REST_SECONDS": "100"})
        with a, b, c, d, e:
            self.assertIsNone(llm.json("system", "user"))         # 45 s, 90 s: two waits, then the question is given up
            rests = llm._rest["gemini-3.5-flash-lite"] - self.clock[0]
            self.assertEqual(rests, 100)                           # the third rest is capped
            self.clock[0] += 101
            self.assertEqual(llm.json("system", "user"), {"ok": True})
        self.assertEqual(llm._busy["gemini-3.5-flash-lite"], 0)

    def test_an_unreadable_video_costs_two_calls_and_no_model(self):
        llm = self.llm()
        a, b, c, d, e = self.running(LISTED, [EMPTY, EMPTY, ANSWER])
        with a, b as http, c, d, e:
            self.assertIsNone(llm.json("system", "user", video_url="https://www.youtube.com/watch?v=private"))
            self.assertEqual(http.call_count, 2)
            self.assertEqual((llm.dead, [m for m, t in llm._rest.items() if t > self.clock[0]], llm.why.get("unusable_answer")), (set(), [], 2))
            self.assertEqual(llm.json("system", "user"), {"ok": True})

    def test_two_timeouts_rest_a_model_they_do_not_retire_it(self):
        llm = self.llm()
        a, b, c, d, e = self.running(LISTED, [TimeoutError("slow"), ANSWER, TimeoutError("slow"), ANSWER])
        with a, b, c, d, e:
            self.assertEqual(llm.json("system", "user"), {"ok": True})
            self.assertEqual(llm.json("system", "user"), {"ok": True})
        self.assertNotIn("gemini-3.5-flash-lite", llm.dead)
        self.assertEqual(llm._rest["gemini-3.5-flash-lite"] - self.clock[0], 600)

    def test_a_minute_limit_is_not_mistaken_for_a_spent_day(self):
        llm = self.llm()
        minute = common.HttpError(429, '{"error": {"message": "You exceeded your current quota, please check your plan and billing details.", "details": [{"quotaId": "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"}]}}', "https://example.org")
        a, b, c, d, e = self.running(LISTED, [minute, minute, ANSWER])
        with a, b, c, d, e:
            self.assertEqual(llm.json("system", "user"), {"ok": True})
        self.assertEqual((llm.dead, llm.why.get("rate_limited")), (set(), 1))

    def test_the_run_record_says_what_went_wrong_without_the_log(self):
        llm = self.llm()
        a, b, c, d, e = self.running(LISTED, [BUSY, ANSWER])
        with a, b, c, d, e:
            llm.json("system", "user")
        rep = common.Report("fixture")
        with patch.object(common, "log"):
            llm.record(rep)
        self.assertEqual(rep.notes, ["model trouble: overloaded 1"])


LESSONS = {"salsa": {"lessons": [{"youtube_id": "A1", "channel": "Ana Dance", "title": "Salsa basics", "pos": 30, "neg": 1},
                                 {"youtube_id": "B1", "channel": "Bo", "title": "Salsa in ten minutes", "pos": 3, "neg": 0}]},
           "bachata": {"lessons": [{"youtube_id": "A2", "channel": "Ana Dance", "title": "Bachata basics", "pos": 25, "neg": 0},
                                   {"youtube_id": "C1", "channel": "Cy", "title": "Bachata", "pos": 2, "neg": 6},
                                   {"youtube_id": "X9", "channel": "Clips", "title": "Bachata show", "pos": 9, "neg": 0}]}}
METHOD = {"is_lesson": True, "kind": "lesson",
          "mentor": {"voice": ["warm", "playful", "robotic"],
                     "beliefs": [{"t": "0:05", "belief": "Anyone who can walk can dance."}, {"t": "", "belief": "no timestamp, dropped"}],
                     "feelings": [{"t": "2:40", "feeling": "awkward", "response": "Says she felt silly in her first class too, and laughs with the camera."},
                                  {"t": "3:00", "feeling": "hungry", "response": "not a feeling in the list"}]},
          "teacher_system": "Shows the whole step, then three small pieces, then the music.", "signature": "Counts in the rhythm's own words.",
          "screen": {"views": ["mirror", "feet_closeup", "hologram"], "on_screen": ["counts"], "editing": ["slow_motion"]},
          "practices": [{"tag": "mirror_view", "t": "0:20", "what": "turns her back so learners copy directly"},
                        {"tag": "chunking", "t": "1:05", "what": "three pieces, one at a time"},
                        {"tag": "made_up_tag", "t": "2:00", "what": "not in the vocabulary"},
                        {"tag": "tempo_ramp", "t": "soon", "what": "no real time given"}],
          "adaptations": [{"t": "3:10", "difficulty": "the turn feels too fast", "adjustment": "walk it without turning first", "kind": "easier"},
                          {"t": "", "difficulty": "no timestamp", "adjustment": "dropped", "kind": "easier"}],
          "entry_points": ["feet_first", "by_magic"], "pace": {"talk_vs_move": "balanced", "seconds_before_first_movement": 40, "pieces_taught": 3},
          "learner_voice": {"struggles": [{"theme": "The turn is too fast", "tag": "tempo_ramp", "count": 4}],
                            "clicked": [{"theme": "the back view", "tag": "mirror_view", "count": 6, "author": "someone"}],
                            "requests": [{"theme": "a slower version", "tag": "nonsense", "count": 2}],
                            "meant": [{"theme": "First time I felt I could dance", "tag": "quick_win", "count": 5}]},
          "limits": "the feet leave the frame"}
PAPER = {"url": "https://europepmc.org/article/MED/1", "kind": "paper", "title": "Focus of attention", "authors": "W", "year": "2001", "journal": "J", "cited_by": 5,
         "text": "Learners who directed attention to the effect of the movement learned the skill faster than learners who attended to their own limbs. "
                 "The advantage remained in a retention test one day later."}
NOTE = {"relevant": True, "principle": "Attending to the effect of a movement helps learning.",
        "findings": [{"finding": "An outward focus speeds learning.", "quote": "directed attention to the effect of the movement learned the skill faster", "source": PAPER["url"]},
                     {"finding": "The gain lasts.", "quote": "The advantage remained in a retention test one day later", "source": PAPER["url"]},
                     {"finding": "Invented.", "quote": "dancers improved by forty percent in every study ever made", "source": PAPER["url"]}],
        "for_the_teacher": ["Give an image for the foot, not a muscle to tense."], "when_it_does_not_apply": ""}


class Model:
    """Stands in for the model client: answers by the kind of question, counts the questions."""
    def __init__(self, enabled=True, method=METHOD, note=NOTE):
        self.enabled, self.gemini_key, self.method, self.note, self.asked = enabled, "fixture" if enabled else "", method, note, []

    def json(self, system, user, **kw):
        self.asked.append("method" if kw.get("video_url") else "science")
        return self.method if kw.get("video_url") else self.note

    def record(self, rep):
        pass


class TeachingResearchTests(Project):
    def test_teachers_are_ranked_by_learners_words_and_a_clip_that_is_not_a_lesson_is_left_out(self):
        t = teaching.build_teachers(LESSONS, studied={"X9": {"status": "not_a_lesson"}})
        self.assertEqual([x["teacher"] for x in t], ["Ana Dance", "Bo", "Cy"])
        self.assertEqual([x["rank"] for x in t], [1, 2, 3])
        self.assertTrue(t[0]["score"] > t[1]["score"] > t[2]["score"] >= 0)
        self.assertEqual((t[0]["praise"], t[0]["complaints"], t[0]["dances"]), (55, 1, ["bachata", "salsa"]))
        self.assertGreater(teaching.wilson(90, 100), teaching.wilson(9, 10))

    def test_breadth_before_depth_and_a_studied_or_recently_failed_video_is_not_asked_again(self):
        today = dt.date(2026, 11, 17)
        pick = lambda methods, n: [l["youtube_id"] for _, l in teaching.pick_methods(teaching.build_teachers(LESSONS, {"X9": {"status": "not_a_lesson"}}, methods), methods, n, today=today)]
        self.assertEqual(pick({}, 4), ["A1", "B1", "C1", "A2"])
        done = {"A1": {"status": "ok", "schema": teaching.SCHEMA, "teacher_key": "ana-dance", "method": teaching.normalise_method(METHOD)},
                "B1": {"status": "failed", "analysed_at": "2026-11-16T22:00:00Z", "attempts": 1}}
        self.assertEqual(pick(done, 4), ["C1", "A2"])
        done["B1"]["analysed_at"] = "2026-11-14T22:00:00Z"
        self.assertEqual(pick(done, 4), ["B1", "C1", "A2"])
        self.assertFalse(teaching._due({"status": "not_a_lesson", "analysed_at": "2020-01-01T00:00:00Z"}, today))
        # a lesson watched before the mentor reading existed is watched once more, in its teacher's turn
        before = {"A1": {"status": "ok", "teacher_key": "ana-dance", "method": teaching.normalise_method(METHOD)}}
        self.assertEqual(pick(before, 2), ["A1", "B1"])

    def test_a_teachers_talk_is_studied_first_each_night_when_one_is_waiting(self):
        today, out = dt.date(2026, 11, 17), {"X9": {"status": "not_a_lesson"}}
        lessons = dict(LESSONS, **{teaching.BASICS + "first-steps": {"lessons": [{"youtube_id": "F1", "channel": "Ana Dance", "title": "Your first steps", "pos": 20, "neg": 0}]},
                                   teaching.BASICS + teaching.TALKS: {"lessons": [{"youtube_id": "T1", "channel": "Quiet Teacher", "title": "How I teach adults", "pos": 2, "neg": 0}]}})
        ids = lambda r: [l["youtube_id"] for _, l in r[0]]
        got = teaching.tonight(teaching.build_teachers(lessons, out, {}), {}, 4, today=today)
        # the talk first although its teacher ranks low, then the basics, then the dances
        self.assertEqual((ids(got), got[1], got[2]), (["T1", "F1", "A1", "B1"], 2, 1))
        done = {"T1": {"status": "ok", "schema": teaching.SCHEMA, "teacher_key": teaching.channel_key("Quiet Teacher"), "method": teaching.normalise_method(METHOD)}}
        again = teaching.tonight(teaching.build_teachers(lessons, out, done), done, 4, today=today)
        # no talk waiting: its place goes back to the basics and the dances
        self.assertEqual((ids(again), again[1], again[2]), (["F1", "A1", "B1", "C1"], 1, 0))
        # a lesson read before beliefs were kept apart from step technique is read once more
        self.assertTrue(teaching._due(dict(done["T1"], schema=2), today))

    def test_only_the_vocabulary_real_timestamps_and_nameless_themes_are_kept(self):
        m = teaching.normalise_method(METHOD)
        self.assertEqual(m["screen"]["views"], ["mirror", "feet_closeup"])
        self.assertEqual([p["tag"] for p in m["practices"]], ["mirror_view", "chunking"])
        self.assertEqual([a["adjustment"] for a in m["adaptations"]], ["walk it without turning first"])
        self.assertEqual(m["entry_points"], ["feet_first"])
        self.assertEqual(m["learner_voice"]["clicked"], [{"theme": "the back view", "tag": "mirror_view", "count": 6}])
        self.assertEqual(m["learner_voice"]["requests"][0]["tag"], "other")
        # the mentor reading: only listed voices and feelings, only beliefs and feelings with a real moment in the video
        self.assertEqual((m["mentor"]["voice"], [b["belief"] for b in m["mentor"]["beliefs"]], [f["feeling"] for f in m["mentor"]["feelings"]]),
                         (["warm", "playful"], ["Anyone who can walk can dance."], ["awkward"]))
        self.assertEqual(m["learner_voice"]["meant"], [{"theme": "First time I felt I could dance", "tag": "quick_win", "count": 5}])
        self.assertEqual((teaching._secs("1:05"), teaching._secs("1:02:03"), teaching._secs("soon")), (65, 3723, None))

    def test_a_research_note_stands_only_on_quotes_that_are_in_the_source(self):
        item = teaching.SCIENCE[0]
        note = teaching.science_note(item, Model(), sources=[PAPER])
        self.assertEqual((note["status"], len(note["findings"]), note["quotes_offered"]), ("ok", 2, 3))
        self.assertNotIn("text", note["sources"][0])
        thin = teaching.science_note(item, Model(note=dict(NOTE, findings=NOTE["findings"][1:])), sources=[PAPER])
        self.assertEqual((thin["status"], len(thin["findings"])), ("thin", 1))
        self.assertEqual(teaching.science_note(item, Model(), sources=[])["status"], "no_sources")
        self.assertEqual(teaching.science_note(item, Model(note=None), sources=[PAPER])["status"], "failed")
        for key, _, _, tags in teaching.SCIENCE:
            self.assertTrue(tags and all(t in teaching.PRACTICES for t in tags), key)
        self.assertEqual(len({s[0] for s in teaching.SCIENCE}), len(teaching.SCIENCE))

    def test_three_kinds_of_evidence_are_joined_per_practice(self):
        methods = {}
        for yid, who in (("A1", "Ana Dance"), ("B1", "Bo"), ("C1", "Cy")):
            methods[yid] = {"youtube_id": yid, "status": "ok", "schema": teaching.SCHEMA, "kind": "teacher_talk" if yid == "C1" else "lesson",
                            "teacher": who, "teacher_key": teaching.channel_key(who), "teacher_score": 50, "slug": "salsa", "dance": "Salsa",
                            "url": "https://www.youtube.com/watch?v=" + yid, "comments_read": 60, "method": teaching.normalise_method(METHOD)}
        notes = {"mirrors_in_dance": {"key": "mirrors_in_dance", "status": "ok", "topic": "mirrors in dance", "tags": ["mirror_view"], "principle": "A mirror view helps copying.",
                                      "findings": [{"finding": "f", "quote": "q", "source": PAPER["url"]}], "for_the_teacher": ["Turn your back."], "when_it_does_not_apply": "",
                                      "sources": [{"url": PAPER["url"], "title": "t", "authors": "a", "year": "2001", "journal": "j"}]}}
        s = teaching.fuse(teaching.build_teachers(LESSONS, {}, methods), methods, notes, family_of={"salsa": "latin"}, today=dt.date(2026, 11, 17))
        first = s["practices"][0]
        self.assertEqual((first["tag"], first["evidence_kinds"], first["teachers"], first["families"], first["learner_voice"]["clicked"]), ("mirror_view", 3, 3, 1, 18))
        # the DNA is only what two or more kinds of evidence agree on; the adjustment table starts from what learners find hard
        self.assertEqual([(d["theme"], d["tag"]) for d in s["dna"]], [("See it", "mirror_view")])
        self.assertEqual((s["adjustments"][0]["tag"], s["adjustments"][0]["comments"], s["adjustments"][0]["learners_say"]), ("tempo_ramp", 12, ["the turn is too fast"]))
        self.assertEqual(set(t for _, tags in teaching.THEMES for t in tags), set(teaching.PRACTICES))
        # two teachers show the practice in a lesson, one says it in a talk
        self.assertEqual((first["show_it"], first["say_it"], first["lessons"], first["talks"], s["counts"]["talks_studied"]), (2, 1, 2, 1, 1))
        # the mentor: voice, beliefs (said once, kept once), feelings met, what the lessons meant; and what to remember about a learner
        mentor = s["mentor"]
        self.assertEqual((dict(mentor["voice"]), len(mentor["beliefs"]), mentor["feelings"][0]["feeling"], mentor["feelings"][0]["seen"]), ({"warm": 3, "playful": 3}, 1, "awkward", 3))
        self.assertEqual(mentor["meant_to_learners"][0], {"theme": "first time i felt i could dance", "count": 15})
        self.assertEqual((s["learner_model"][0]["seen_most"], s["learner_model"][1]["seen_most"], s["learner_model"][2]["seen_most"]), ([("tempo_ramp", 12)], [("mirror_view", 18)], [["awkward", 3]]))
        self.assertEqual((s["counts"]["feelings_answered"], s["counts"]["lessons_with_mentor_reading"], len(s["how_to_use"])), (3, 3, 5))
        # a feeling that is named and answered counts as evidence for the practice of naming the feeling
        named = next(p for p in s["practices"] if p["tag"] == "names_the_feeling")
        self.assertEqual((named["teachers"], named["examples"][0]["t"]), (3, "2:40"))
        self.assertEqual(next(p for p in s["practices"] if p["tag"] == "chunking")["evidence_kinds"], 1)
        self.assertEqual((s["counts"]["lessons_studied_for_method"], s["counts"]["adaptations_seen"], s["counts"]["practices_with_two_or_more_kinds"]), (3, 3, 1))
        self.assertEqual(s["struggles"][0], {"tag": "tempo_ramp", "theme": "the turn is too fast", "count": 12})
        page = teaching.render(s)
        for must in ("### Mirror view ●●●", "&t=20s", "walk it without turning first", "Turn your back.", "## The teachers studied so far",
                     "## The teaching DNA so far", "Show the step from behind or mirrored, so it can be copied directly. ●●●", "## How the Best Dance Friend adjusts",
                     "## The mentor: voice, beliefs and how feelings are met", "When the learner feels **awkward** (met 3 times)", "Anyone who can walk can dance.",
                     "## What the Best Dance Friend should remember about each learner", "# The evidence", "1 teacher say it in talks"):
            self.assertIn(must, page)
        self.assertNotIn("someone", json.dumps(s))
        # a lesson watched before the mentor reading existed still counts as evidence and breaks nothing
        early = json.loads(json.dumps(methods["A1"]))
        early.update(youtube_id="Z9", teacher="Zed", teacher_key="zed"); early.pop("schema"); early.pop("kind"); early["method"].pop("mentor"); early["method"]["learner_voice"].pop("meant")
        s2 = teaching.fuse(teaching.build_teachers(LESSONS, {}, methods), dict(methods, Z9=early), notes)
        self.assertEqual((s2["counts"]["lessons_studied_for_method"], s2["counts"]["lessons_with_mentor_reading"]), (4, 3))
        self.assertIn("the earlier ones are watched once more", teaching.render(s2))

    def test_the_stage_studies_writes_the_page_and_never_loses_a_studied_lesson(self):
        jsave("tutorial_results.json", LESSONS)
        model = Model()
        with patch.object(teaching, "LLM", return_value=model), patch.object(teaching, "fetch_comments", return_value=["the back view finally made it click"]), \
                patch.object(teaching, "science_sources", return_value=[PAPER]), patch.object(teaching, "ytdlp_search", return_value=[]), patch.object(common, "log"):
            rec = teaching.run(budget=2, science=1)
        self.assertEqual((rec["counters"].get("method_ok"), rec["counters"].get("science_ok"), model.asked), (2, 1, ["method", "method", "science"]))
        self.assertEqual([jload("pedagogy/methods/A1.json")[k] for k in ("comments_read", "schema", "kind")], [1, teaching.SCHEMA, "lesson"])
        self.assertEqual(jload("public/catalog/bdf_teaching_system.json")["contract"], "da_bdf_teaching_v1")
        with open("BDF_TEACHING_SYSTEM.md", encoding="utf-8") as f:
            self.assertIn("Ana Dance", f.read())
        self.assertEqual(jload("pedagogy/teachers.json")["teachers"][0]["methods_studied"], 1)
        broken = Model(method=None, note=None)
        with patch.object(teaching, "LLM", return_value=broken), patch.object(teaching, "fetch_comments", return_value=[]), patch.object(teaching, "ytdlp_search", return_value=[]), \
                patch.object(teaching, "science_sources", return_value=[PAPER]), patch.object(common, "log"), patch.object(common, "warn"):
            rec = teaching.run(budget=5, science=2)
        self.assertEqual(jload("pedagogy/methods/A1.json")["status"], "ok")
        # three unreadable videos in a row: the stage stops asking (no research note is attempted either) and keeps what it has
        self.assertEqual((rec["counters"].get("method_failed"), broken.asked), (3, ["method"] * 3))
        self.assertEqual(jload("pedagogy/bdf_system.json")["counts"]["lessons_studied_for_method"], 2)

    def test_basics_lessons_come_from_a_free_search_and_stay_only_when_learners_praise_them(self):
        store, state = {}, {}
        facts = [{"youtube_id": "F1", "title": "How to find the beat", "channel": "Beat Coach", "comments": 90}, {"youtube_id": "F2", "title": "Rhythm", "channel": "Other", "comments": 50}]
        said = {"F1": ["This finally clicked for me", "Best teacher ever, so clear"], "F2": ["too fast", "confusing"]}
        with patch.object(teaching, "ytdlp_search", return_value=["F1", "F2"]), patch.object(teaching, "video_facts", return_value=facts), \
                patch.object(teaching, "fetch_comments", side_effect=lambda yid, n=60: said[yid]):
            self.assertEqual(teaching.discover_foundations(store, state, 1, today=dt.date(2026, 11, 17)), 1)
            self.assertEqual(teaching.discover_foundations(store, state, 1), 0)          # the same videos are never judged twice
        self.assertEqual((state["foundation_search"], [l["channel"] for l in store["topics"]["first-steps"]["lessons"]]), (2, ["Beat Coach"]))
        lessons = teaching.all_lessons(LESSONS, store)
        teachers = teaching.build_teachers(lessons)
        self.assertIn("Beat Coach", [t["teacher"] for t in teachers])
        basics = teaching.pick_methods(teachers, {}, 3, want=lambda l: l["slug"].startswith(teaching.BASICS))
        self.assertEqual([(l["youtube_id"], l["slug"]) for _, l in basics], [("F1", "basics-first-steps")])
        self.assertEqual(teaching.basics_name("basics-first-steps"), "First steps (basics)")
        self.assertEqual(teaching.praise(["Muchas gracias, easy to follow", "trop vite"]), (2, 1))
        # with two or more searches a night, the last one looks for a teacher explaining how they teach
        asked, state2 = [], {}
        with patch.object(teaching, "ytdlp_search", side_effect=lambda q, n=15: asked.append(q) or []):
            teaching.discover_foundations({}, state2, 3)
        talk_phrases = [q for slug, _, qs in teaching.FOUNDATIONS if slug == teaching.TALKS for q in qs]
        self.assertEqual((asked[2], asked[0] in talk_phrases, state2["foundation_search"], state2["talk_search"]), (talk_phrases[0], False, 2, 1))

    def test_the_open_search_never_reads_a_paper_twice_and_the_model_proposes_its_tags(self):
        papers = [dict(PAPER, url="https://europepmc.org/article/MED/%d" % i, title="Paper %d" % i) for i in (1, 2, 3)]
        state, search = {}, (lambda q, n=20: papers)
        self.assertEqual([teaching.paper_key(p) for p in teaching.discover_papers(state, {}, 2, search=search)], ["paper-med-1", "paper-med-2"])
        self.assertEqual([teaching.paper_key(p) for p in teaching.discover_papers(state, {}, 2, search=search)], ["paper-med-3"])
        self.assertEqual((teaching.discover_papers(state, {}, 2, search=search), state["paper_search"]), ([], 3))
        item = (teaching.paper_key(papers[0]), "", "", [])
        note = teaching.science_note(item, Model(note=dict(NOTE, tags=["imagery", "nonsense", "quick_win"])), sources=[papers[0]], topic=papers[0]["title"])
        self.assertEqual((note["status"], note["tags"], note["topic"]), ("ok", ["imagery", "quick_win"], "Paper 1"))
        self.assertEqual(teaching.science_note(item, Model(), sources=[papers[0]])["status"], "thin")       # no practice named: it cannot be joined
        self.assertEqual(len(set(teaching.PAPER_QUERIES)), len(teaching.PAPER_QUERIES))
        # in a paper database "dance" is also the honeybee's dance: a dance query is kept on people, other queries are left alone
        asked = []
        with patch.object(teaching, "get_json", side_effect=lambda u, **kw: asked.append(u) or {}):
            teaching.europe_pmc('ABSTRACT:dance AND ABSTRACT:learning'); teaching.europe_pmc('ABSTRACT:"external focus"')
        self.assertEqual(["honeybee" in u and "participants" in u for u in asked], [True, False])

    def test_a_night_of_reading_topic_notes_and_papers_from_the_open_search(self):
        jsave("tutorial_results.json", LESSONS)
        papers = [dict(PAPER, url="https://europepmc.org/article/MED/%d" % i, title="Paper %d" % i) for i in (1, 2)]
        model = Model(note=dict(NOTE, tags=["imagery"]))
        with patch.object(teaching, "LLM", return_value=model), patch.object(teaching, "ytdlp_search", return_value=[]), patch.object(teaching, "science_sources", return_value=[PAPER]), \
                patch.object(teaching, "europe_pmc", return_value=papers), patch.object(common, "log"):
            rec = teaching.run(budget=0)
        # three topics and two papers; the second paper's quotes are not in its own abstract, so its note is not used
        self.assertEqual((rec["counters"].get("science_ok"), rec["counters"].get("paper_ok"), rec["counters"].get("paper_thin"), model.asked), (3, 1, 1, ["science"] * 5))
        counts = jload("pedagogy/bdf_system.json")["counts"]
        self.assertEqual((counts["science_notes"], counts["paper_notes"], counts["practices_total"]), (3, 1, 34))
        with open("BDF_TEACHING_SYSTEM.md", encoding="utf-8") as f:
            self.assertIn("## Papers found by the open search (1;", f.read())

    def test_with_the_engine_off_nothing_is_asked_and_the_tables_are_still_rebuilt(self):
        jsave("tutorial_results.json", LESSONS)
        model = Model(enabled=False)
        with patch.object(teaching, "LLM", return_value=model), patch.object(teaching, "fetch_comments", side_effect=AssertionError("no network when off")), \
                patch.object(teaching, "ytdlp_search", side_effect=AssertionError("no network when off")), patch.object(teaching, "europe_pmc", side_effect=AssertionError("no network when off")), \
                patch.object(teaching, "science_sources", side_effect=AssertionError("no network when off")), patch.object(common, "log"):
            rec = teaching.run(budget=5, science=3)
        self.assertEqual((model.asked, rec["errors"]), ([], []))
        self.assertEqual(len(jload("pedagogy/teachers.json")["teachers"]), 4)
        self.assertTrue(os.path.exists("BDF_TEACHING_SYSTEM.md"))


if __name__ == "__main__":
    unittest.main()

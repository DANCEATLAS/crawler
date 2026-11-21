"""The door (pipeline/door.py): offline tests on a small library in a temporary folder."""
import datetime as dt
import json
import os
import tempfile
import unittest
from . import door

DAY1, DAY2 = dt.date(2026, 11, 21), dt.date(2026, 11, 22)

STYLES = {
    "salsa": {"slug": "salsa", "name": "Salsa", "country": "United States and Cuba", "country_code": "US", "tagline": "A partner dance.", "aliases": ["salsa dance"],
              "family": "latin-caribbean", "research_gate": "publish", "publish_gate": "publish", "hero_video_youtube_id": "HERO1", "hero_qc": {"verdict": "pass"},
              "tutorials": [{"youtube_id": "LESSON1"}], "profile": "Short story.", "sources": ["https://example.org/salsa"]},
    "holy": {"slug": "holy", "name": "Holy dance", "country": "France (term origin), Italy", "is_sacred": True, "sacred_note": "Danced only inside the rite.",
             "research_gate": "publish", "publish_gate": "publish", "tutorials": [{"youtube_id": "LESSON2"}],
             "video_stack": [{"youtube_id": "RITE1", "role": "hero", "title": "The rite, filmed"}, {"youtube_id": "RITE2", "role": "rendition", "title": "Basic Steps - Holy dance"},
                             {"youtube_id": "RITE3", "role": "rendition", "title": "Holy dance at the classical festival"}]},
    "newcomer": {"slug": "newcomer", "name": "Newcomer", "country": "Balkans/Roma", "unesco": False, "lat": None},
    "gone": {"slug": "gone", "name": "Gone", "country": "Spain"},
}
DEEP = {
    "salsa": {"sections": {"origins_and_history": "Born in New York."}, "teaching": {"basic_steps": ["Step forward on one"]}, "movement_profile": {"posture": "upright"},
              "music_profile": {"meter": "4/4"}, "adaptations": {"derived": True}, "episode_brief": {"logline": "A story.", "lesson_ladder": [{"level": "basic"}]}, "claims": []},
    "holy": {"sections": {"origins_and_history": "Old."}, "teaching": {"basic_steps": ["A secret step"]}, "movement_profile": {"posture": "bowed"},
             "adaptations": {"derived": True}, "episode_brief": {"logline": "A rite.", "lesson_ladder": [{"level": "basic"}], "instructor_persona": "x"}},
}
READY = {"standard": "AR-1", "counts": {"listed": 3, "published": 2, "active_ready": 0},
         "profiles": {"salsa": {"have": 14, "of": 15, "missing": ["mistakes"], "via": {"rhythm": "lesson"}, "state": "building"},
                      "holy": {"have": 6, "of": 6, "missing": [], "via": {}, "state": "story_ready_teaching_withheld"}}}
LESSON = {"youtube_id": "LESSON1", "slug": "salsa", "status": "ok", "title": "Salsa basics", "channel": "A teacher", "url": "https://www.youtube.com/watch?v=LESSON1",
          "analysed_at": "2026-11-17T21:18:26Z", "observation_window": {"start_s": 0, "end_s": 480, "human_verified": False},
          "extraction": {"level": "beginner", "language": "English", "counting_scheme": "1-2-3, 5-6-7",
                         "lesson_structure": [{"t": "0:06", "segment": "intro", "note": "Says hello."}, {"t": "1:13", "segment": "count_in", "note": "Explains the count."}],
                         "steps_taught": [{"name": "Basic", "counts": "1-2-3, 5-6-7", "description": "In place."}, {"name": "Turn", "counts": "null", "description": "A turn."}],
                         "cues": ["shift your weight"], "common_mistakes": ["looking down"], "safety": ["none"], "quotes": [{"t": "0:10", "text": "the teacher's own words"}],
                         "evidence_segments": [{"start_s": 36, "end_s": 45, "observation": "Shows the basic step.", "verification": "model_candidate"}]}}
SACRED_LESSON = dict(LESSON, youtube_id="LESSON2", slug="holy")
SHOW = {"youtube_id": "HERO1", "slug": "salsa", "status": "ok", "kind": "performance", "url": "https://www.youtube.com/watch?v=HERO1", "analysed_at": "2026-11-17T21:30:10Z",
        "observation_window": {"start_s": 0, "end_s": 300}, "observation": {"setting": "a club", "posture": "upright", "empty": ""}}
RUNS = [{"stage": "research", "started": "2026-11-19T18:00:00Z", "finished": "2026-11-19T19:00:00Z", "counters": {"llm_requests": 60, "llm_unanswered": 1}, "notes": ["model trouble: overloaded 3"], "errors": []},
        {"stage": "report", "started": "2026-11-19T19:00:00Z", "finished": "2026-11-19T19:01:00Z", "counters": {}, "notes": [], "errors": []},
        {"stage": "teaching", "started": "2026-11-20T05:00:00Z", "finished": "2026-11-20T05:10:00Z", "counters": {"llm_requests": 5}, "notes": [], "errors": []},
        {"stage": "research", "started": "2026-11-20T18:00:00Z", "finished": "2026-11-20T20:00:00Z", "counters": {"llm_requests": 70}, "notes": [], "errors": ["one profile failed"]},
        {"stage": "report", "started": "2026-11-20T20:00:00Z", "finished": "2026-11-20T20:02:00Z", "counters": {}, "notes": [], "errors": []}]
HISTORY = [{"date": "2026-11-16", "listed": 100, "published": 10, "active_ready": 1}, {"date": "2026-11-20", "listed": 140, "published": 30, "active_ready": 9}]


def library(root, styles=STYLES):
    def put(rel, obj):
        path = os.path.join(root, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f)
    put("public/catalog/dances.app.json", {"contract": "dw_app_v1", "styles": styles})
    put("public/catalog/retired.json", {"retired": [{"slug": "gone", "merged_into": "salsa"}]})
    put("public/catalog/profiles_v2.json", {"profiles": DEEP})
    put("public/catalog/episodes.json", {"packs": {"salsa": {"status": "draft", "chapters": 3, "scenes": 37, "gaps": 8, "languages": []}}})
    put("public/catalog/bdf_teaching_system.json", {"contract": "da_bdf_teaching_v1", "how_to_use": ["dna: the default"]})
    put("pipeline_state/active_ready.json", READY)
    put("pipeline_state/active_ready_history.json", HISTORY)
    put("pipeline_state/runs.json", RUNS)
    put("pipeline_state/vision_status.json", {"owner_action": {"status": "resolved", "reason": "Nothing needs you.", "verified_at": "2026-11-21"}})
    put("pedagogy/videos/LESSON1.json", LESSON)
    put("pedagogy/videos/LESSON2.json", SACRED_LESSON)
    put("pedagogy/performances/HERO1.json", SHOW)


def read(root, rel):
    with open(os.path.join(root, "public", "catalog", *rel.split("/")), encoding="utf-8") as f:
        return json.load(f)


class Door(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        library(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_joined_origin_is_several_places_not_a_new_country(self):
        self.assertEqual(door.places("France and Italy"), ["FR", "IT"])
        self.assertEqual(door.places("France (term origin), Russia (19th-century codification)"), ["FR", "RU"])
        self.assertEqual(door.places("Trinidad and Tobago"), ["TT"])
        self.assertEqual(door.places("Trinidad & Tobago"), ["TT"])
        self.assertEqual(door.places("United States and Canada", "US"), ["US", "CA"])
        self.assertEqual(door.places("Balkans/Roma"), [])
        self.assertEqual(door.places(None), [])

    def test_the_index_lists_every_dance_once_with_its_file(self):
        out = door.run(self.root, DAY1)
        idx = read(self.root, "index.json")
        self.assertEqual((idx["contract"], idx["count"], sorted(idx["dances"])), ("da_index_v1", 3, ["holy", "newcomer", "salsa"]))
        self.assertEqual(idx["retired"], {"gone": "salsa"})
        self.assertEqual(idx["states"], {"building": 1, "listed": 1, "story_ready_teaching_withheld": 1})
        s = idx["dances"]["salsa"]
        self.assertEqual((s["countries"], s["state"], s["have"], s["of"], s["lessons"], s["hero_ok"]), (["US", "CU"], "building", 14, 15, 1, True))
        self.assertNotIn("profile", s)                      # the long text is in the dance's own file, not in the list
        self.assertNotIn("lat", idx["dances"]["newcomer"])  # an empty value is left out
        for slug, e in idx["dances"].items():
            self.assertEqual(e["fp"], read(self.root, f"d/{slug}.json")["fingerprint"])
        self.assertEqual(out["counters"]["dances"], 3)
        self.assertFalse(os.path.exists(os.path.join(self.root, "public", "catalog", "d", "gone.json")))

    def test_a_dance_file_holds_the_whole_dance(self):
        door.run(self.root, DAY1)
        d = read(self.root, "d/salsa.json")
        self.assertEqual((d["contract"], d["state"], d["countries"]), ("da_dance_v1", "building", ["US", "CU"]))
        self.assertEqual(d["card"]["profile"], "Short story.")
        self.assertEqual(d["profile"]["teaching"]["basic_steps"], ["Step forward on one"])
        self.assertEqual(d["readiness"]["missing"], [{"key": "mistakes", "label": "what to avoid: common mistakes or safety"}])
        self.assertEqual(d["episodes"]["file"], "episodes/salsa.json")
        self.assertEqual(d["performances"][0]["observation"], {"setting": "a club", "posture": "upright"})
        self.assertNotIn("generated_at", d)                 # no clock inside a dance file

    def test_a_lesson_is_described_and_the_teacher_is_not_transcribed(self):
        door.run(self.root, DAY1)
        l = read(self.root, "d/salsa.json")["lessons"][0]
        self.assertEqual([p["seconds"] for p in l["parts"]], [6, 73])
        self.assertEqual(l["steps"], [{"name": "Basic", "counts": "1-2-3, 5-6-7", "description": "In place."}, {"name": "Turn", "description": "A turn."}])
        self.assertNotIn("safety", l)                       # "none" is not a safety note
        self.assertNotIn("quotes", l)
        self.assertNotIn("the teacher's own words", json.dumps(l))
        self.assertEqual(l["evidence"][0]["verification"], "model_candidate")
        self.assertEqual(l["seen"], {"from_s": 0, "to_s": 480, "checked_by_a_person": False})

    def test_a_sacred_dance_keeps_its_story_and_nothing_that_teaches(self):
        door.run(self.root, DAY1)
        d = read(self.root, "d/holy.json")
        self.assertEqual(d["teaching_withheld"], "Danced only inside the rite.")
        self.assertEqual(d["profile"]["sections"], {"origins_and_history": "Old."})
        for key in ("teaching", "movement_profile", "adaptations"):
            self.assertNotIn(key, d["profile"])
        self.assertEqual(d["profile"]["episode_brief"], {"logline": "A rite."})
        self.assertNotIn("lessons", d)
        self.assertNotIn("performances", d)
        self.assertNotIn("tutorials", d["card"])
        self.assertEqual([v["youtube_id"] for v in d["card"]["video_stack"]], ["RITE1", "RITE3"])     # the video that offers to teach is not in the door
        self.assertNotIn("A secret step", json.dumps(d))
        e = read(self.root, "index.json")["dances"]["holy"]
        self.assertTrue(e["is_sacred"])
        self.assertNotIn("lessons", e)
        self.assertEqual(e["countries"], ["FR", "IT"])

    def test_a_keyword_flag_alone_does_not_withhold_a_dance_the_writer_found_teachable(self):
        styles = json.loads(json.dumps(STYLES))
        styles["salsa"].update(is_sacred=True, sacred_note="Not applicable.")       # the catalogue's broad flag
        styles["newcomer"]["_is_sacred"] = True                                    # not researched yet: the careful side
        library(self.root, styles)
        door.run(self.root, DAY1)
        d, idx = read(self.root, "d/salsa.json"), read(self.root, "index.json")["dances"]
        self.assertNotIn("teaching_withheld", d)
        self.assertEqual(len(d["lessons"]), 1)
        self.assertNotIn("is_sacred", idx["salsa"])
        self.assertTrue(idx["newcomer"]["is_sacred"])
        self.assertIn("teaching_withheld", read(self.root, "d/newcomer.json"))

    def test_a_video_that_offers_to_teach_stays_with_a_dance_that_is_taught(self):
        styles = json.loads(json.dumps(STYLES))
        styles["salsa"]["video_stack"] = [{"youtube_id": "S1", "role": "rendition", "title": "Salsa tutorial for beginners"}]
        library(self.root, styles)
        door.run(self.root, DAY1)
        self.assertEqual(len(read(self.root, "d/salsa.json")["card"]["video_stack"]), 1)

    def test_a_misspelt_key_is_put_right_and_the_right_key_wins(self):
        self.assertEqual(door._tidy({"sections": {"how_is_danced": "In lines."}}), {"sections": {"how_it_is_danced": "In lines."}})
        self.assertEqual(door._tidy({"movement_profile": {" what_to_avoid": "stray", "what_to_avoid": "locking the knees"}}), {"movement_profile": {"what_to_avoid": "locking the knees"}})
        self.assertEqual(door._tidy({"movement_profile": {"what_to_avoid": "locking the knees", " what_to_avoid": "stray"}}), {"movement_profile": {"what_to_avoid": "locking the knees"}})
        self.assertEqual(door._tidy({"a": [{" b ": 1}], "c": "text"}), {"a": [{"b": 1}], "c": "text"})

    def test_an_unchanged_dance_is_not_written_again(self):
        self.assertEqual(door.run(self.root, DAY1)["counters"]["written"], 3)
        self.assertEqual(door.run(self.root, DAY2)["counters"]["written"], 0)
        self.assertEqual(read(self.root, "d/salsa.json")["updated"], "2026-11-21")
        before = read(self.root, "d/salsa.json")["fingerprint"]
        changed = json.loads(json.dumps(STYLES))
        changed["salsa"]["tagline"] = "A partner dance, born in New York."
        library(self.root, changed)
        self.assertEqual(door.run(self.root, DAY2)["counters"]["written"], 1)
        after = read(self.root, "d/salsa.json")
        self.assertEqual(after["updated"], "2026-11-22")
        self.assertNotEqual(after["fingerprint"], before)
        self.assertEqual(read(self.root, "index.json")["dances"]["salsa"]["updated"], "2026-11-22")
        self.assertEqual(read(self.root, "index.json")["dances"]["holy"]["updated"], "2026-11-21")

    def test_a_file_of_a_dance_that_left_the_catalogue_is_removed(self):
        door.run(self.root, DAY1)
        stale = os.path.join(self.root, "public", "catalog", "d", "old-name.json")
        with open(stale, "w", encoding="utf-8") as f:
            f.write("{}")
        self.assertEqual(door.run(self.root, DAY1)["counters"]["removed"], 1)
        self.assertFalse(os.path.exists(stale))

    def test_stage_records_join_into_nights(self):
        n = door.nights(RUNS)
        self.assertEqual([(x["date"], x["whole"], x["minutes"], x["questions"], x["unanswered"]) for x in n],
                         [("2026-11-19", True, 61, 60, 1), ("2026-11-20", False, 10, 5, 0), ("2026-11-20", True, 122, 70, 0)])
        self.assertEqual(n[2]["errors"], ["research: one profile failed"])
        self.assertEqual(n[0]["trouble"], ["research: model trouble: overloaded 3"])

    def test_the_machine_page_shows_the_last_whole_night_and_the_pace(self):
        door.run(self.root, DAY1)
        m = read(self.root, "machine.json")
        self.assertEqual((m["contract"], m["last_night"]["date"], m["last_night"]["minutes"], m["last_night"]["errors"]), ("da_machine_v1", "2026-11-20", 122, ["research: one profile failed"]))
        self.assertEqual([x["date"] for x in m["nights"]], ["2026-11-19", "2026-11-20"])
        self.assertEqual(m["pace"], {"days": 4, "per_night": {"listed": 10.0, "published": 5.0, "active_ready": 2.0}})
        self.assertEqual(m["blockers"], [{"key": "mistakes", "label": "what to avoid: common mistakes or safety", "profiles": 1}])
        self.assertEqual(m["closest"], [{"slug": "salsa", "name": "Salsa", "needs": ["what to avoid: common mistakes or safety"], "need_keys": ["mistakes"]}])
        self.assertEqual(m["owner"]["text"], "Nothing needs you.")

    def test_the_machine_page_says_how_far_the_mentors_study_has_come(self):
        from . import teaching
        first, plain = teaching.FIRST_TOPICS[0], teaching.SCIENCE[0][0]
        for key, status in ((first, "ok"), (plain, "ok"), (teaching.FIRST_TOPICS[1], "failed"), ("paper-med-1", "ok"), ("paper-med-2", "thin")):
            path = os.path.join(self.root, "pedagogy", "science", key + ".json")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"key": key, "status": status, "written_at": "2026-11-21T20:00:00Z"}, f)
        with open(os.path.join(self.root, "public", "catalog", "bdf_teaching_system.json"), "w", encoding="utf-8") as f:
            json.dump({"contract": "da_bdf_teaching_v1", "counts": {"lessons_studied_for_method": 51, "teachers_studied": 45, "practices_total": 37, "practices_with_two_or_more_kinds": 23}}, f)
        door.run(self.root, DAY2)
        s = read(self.root, "machine.json")["study"]
        self.assertEqual((s["topics"], s["topics_read"], s["first"], s["papers_read"]), (len(teaching.SCIENCE), 2, {"topics": len(teaching.FIRST_TOPICS), "read": 1}, 1))
        # what is read next: the owner's unread topics, in their order; a topic that failed today waits its month
        self.assertEqual(s["next"], list(teaching.FIRST_TOPICS[2:5]))
        self.assertEqual((s["lessons_studied"], s["practices"], s["practices_in_dna"]), (51, 37, 23))
        self.assertEqual(door.study(self.root, DAY2, budget=0)["next"] if "next" in door.study(self.root, DAY2, budget=0) else [], [])

    def test_the_words_file_names_every_readiness_item_and_research_topic_in_hebrew(self):
        from . import readiness, teaching
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "catalog", "site.json")
        if not os.path.exists(path):
            self.skipTest("the words file is not in this copy")
        with open(path, encoding="utf-8") as f:
            site = json.load(f)
        self.assertEqual(site["contract"], "da_site_v1")
        he = site.get("he") or {}
        self.assertEqual(sorted(set(k for k, _ in readiness.ITEMS) - set(he.get("items") or {})), [])        # the owner reads Hebrew: add the name with the item
        self.assertEqual(sorted(set(item[0] for item in teaching.SCIENCE) - set(he.get("topics") or {})), [])

    def test_the_manifest_names_only_files_that_exist(self):
        door.run(self.root, DAY1)
        m = read(self.root, "manifest.json")
        self.assertEqual(m["contract"], "da_manifest_v1")
        self.assertGreaterEqual(len(m["rules"]), 6)
        for f in m["files"]:
            self.assertTrue(os.path.exists(os.path.join(self.root, "public", "catalog", f["file"])), f["file"])
        self.assertEqual({f["file"] for f in m["files"]} & {"index.json", "manifest.json", "machine.json", "bdf_teaching_system.json"},
                         {"index.json", "manifest.json", "machine.json", "bdf_teaching_system.json"})
        self.assertNotIn("site.json", {f["file"] for f in m["files"]})          # not in this small library
        self.assertEqual((m["dance_file"]["pattern"], m["dance_file"]["count"]), ("d/{slug}.json", 3))
        self.assertEqual(m["teaching"]["how_to_use"], ["dna: the default"])
        self.assertNotIn(self.root, json.dumps(m))

    def test_without_a_catalogue_nothing_is_written(self):
        with tempfile.TemporaryDirectory() as empty:
            out = door.run(empty, DAY1)
            self.assertIn("error", out)
            self.assertFalse(os.path.exists(os.path.join(empty, "public")))


if __name__ == "__main__":
    unittest.main()

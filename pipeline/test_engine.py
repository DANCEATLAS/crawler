"""Offline checks for the 16 November 2026 engine restart: the free lane, no lost profiles, the starting line."""
import datetime as dt
import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch
from . import build_catalog, common, readiness, research, spending
from .common import jload, jsave


def free_policy(**over):
    p = {"schema": 2, "llm_enabled": True, "expires_on": dt.date.today().isoformat(), "authorization_reference": "offline fixture",
         "models": {}, "free_tier_families": {"gemini": ["flash-lite", "flash"]},
         "max_http_attempts_per_process": 50, "max_output_tokens_per_request": 9000, "max_reserved_output_tokens_per_process": 400000}
    p.update(over)
    return p


LISTED = {"models": [{"name": "models/" + n, "supportedGenerationMethods": ["generateContent"]} for n in (
    "gemini-3.8-flash", "gemini-3.8-flash-001", "gemini-3.6-flash", "gemini-3-flash-preview", "gemini-3.5-flash-lite", "gemini-3.5-flash-lite-preview-06-17", "gemini-3.1-flash-lite",
    "gemini-3.1-pro-preview", "gemini-3.1-flash-live-preview", "gemini-3.8-flash-tts", "gemini-flash-latest", "gemma-4")]}


class FreeLaneTests(unittest.TestCase):
    def test_families_open_only_in_schema_two_and_never_for_paid_or_pro(self):
        a = spending.ModelAllowance(free_policy())
        self.assertTrue(a.permitted("gemini"))
        self.assertFalse(a.permitted("openai"))
        self.assertTrue(a.allows("gemini", "gemini-3.5-flash-lite"))
        for name in ("gemini-3.1-pro-preview", "gemini-flash-latest", "gemini-3.8-flash-tts", "gpt-4.1-mini", "gemma-4"):
            self.assertFalse(a.allows("gemini", name), name)
            with self.assertRaises(spending.SpendingBlocked):
                a.reserve("gemini", name, 100)
        self.assertEqual(spending.ModelAllowance(free_policy(schema=1)).families("gemini"), [])
        self.assertFalse(spending.ModelAllowance(free_policy(expires_on="2000-01-01")).permitted("gemini"))
        self.assertFalse(spending.ModelAllowance(free_policy(llm_enabled=False)).permitted("gemini"))

    def llm(self, allowance):
        with patch.object(spending, "_ALLOWANCE", allowance), patch.dict("os.environ", {"GEMINI_API_KEY": "fixture", "OPENAI_API_KEY": "fixture"}):
            return common.LLM()

    def test_writer_gets_flash_first_judges_start_on_flash_lite(self):
        llm = self.llm(spending.ModelAllowance(free_policy()))
        self.assertEqual(llm.openai_key, "")
        with patch.object(common, "get_json", return_value=LISTED):
            strong, fast = llm.gemini_models(True), llm.gemini_models(False)
        self.assertEqual(strong, ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3-flash-preview", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite"])
        self.assertEqual(fast[:2], ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"])

    def test_one_models_day_quota_does_not_stop_the_provider(self):
        a = spending.ModelAllowance(free_policy())
        llm = self.llm(a)
        answer = (200, json.dumps({"candidates": [{"content": {"parts": [{"text": "{\"ok\": true}"}]}}]}), {})
        quota = common.HttpError(429, '{"error": {"details": [{"quotaId": "GenerateRequestsPerDayPerProjectPerModel-FreeTier"}]}}', "https://example.org")
        with patch.object(common, "get_json", return_value=LISTED), patch.object(common, "http", side_effect=[quota, answer]), patch.object(common.time, "sleep"):
            self.assertEqual(llm.json("system", "user"), {"ok": True})
        self.assertIn("gemini-3.5-flash-lite", llm.dead)
        self.assertTrue(a.permitted("gemini"))
        self.assertEqual(llm.unanswered, 0)

    def test_overloaded_model_rests_and_is_not_retired_for_the_run(self):
        llm = self.llm(spending.ModelAllowance(free_policy()))
        answer = (200, json.dumps({"candidates": [{"content": {"parts": [{"text": "{\"ok\": true}"}]}}]}), {})
        busy = common.HttpError(503, '{"error": {"status": "UNAVAILABLE", "message": "high demand"}}', "https://example.org")
        with patch.object(common, "get_json", return_value=LISTED), patch.object(common, "http", side_effect=[busy, answer, answer]), patch.object(common.time, "sleep"):
            self.assertEqual(llm.json("system", "user", strong=True), {"ok": True})
            self.assertNotIn("gemini-3.8-flash", llm.dead)
            self.assertNotIn("gemini-3.8-flash", llm.gemini_models(True)[:0])
            llm._rest["gemini-3.8-flash"] = 0   # five minutes later
            self.assertEqual(llm.json("system", "user", strong=True), {"ok": True})
        self.assertEqual(llm.strikes.get("gemini-3.8-flash"), 0)


class Project(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.previous = os.getcwd()
        os.chdir(self.directory.name)
        self.addCleanup(self.directory.cleanup)
        self.addCleanup(os.chdir, self.previous)


class NothingIsLostTests(Project):
    def test_failed_or_switched_off_writer_never_erases_a_profile(self):
        prev = {"slug": "a", "status": "researched", "schema": 4, "researched_at": "2026-01-01T00:00:00Z", "profile": {"name": "A"}}
        jsave("research_results/a.json", prev)
        ev = {"wikipedia": {"url": "https://example.org", "text": "Evidence"}, "sources": ["https://example.org"]}
        for enabled in (True, False):
            with patch.object(research, "gather_evidence", return_value=ev), patch.object(research, "compose", return_value=None):
                self.assertEqual(research.research_one({"slug": "a"}, Mock(enabled=enabled)), prev)
            self.assertEqual(jload("research_results/a.json"), prev)
            self.assertEqual(research.KEPT.get("a"), "llm_failed")
        with patch.object(research, "gather_evidence", return_value={"sources": []}):
            self.assertEqual(research.research_one({"slug": "a"}, Mock(enabled=True)), prev)
        self.assertEqual(jload("research_results/a.json"), prev)
        # a page that was never written leaves no stub behind when the engine is off
        with patch.object(research, "gather_evidence", return_value=ev), patch.object(research, "compose", return_value=None):
            research.research_one({"slug": "new"}, Mock(enabled=False))
        self.assertFalse(os.path.exists("research_results/new.json"))

    def test_engine_off_run_touches_nothing_and_says_so(self):
        jsave("pipeline_state/candidates.json", {"x": {"slug": "x", "name": "X", "status": "queued"}})
        with patch.object(spending, "_ALLOWANCE", spending.ModelAllowance({})), patch.object(research, "research_one") as one, \
                patch.object(research, "load_catalog") as catalogue:
            rec = research.run(budget_new=5, budget_enrich=0)
        one.assert_not_called()
        catalogue.assert_not_called()
        self.assertEqual(jload("pipeline_state/candidates.json")["x"]["status"], "queued")
        self.assertEqual(rec["counters"].get("engine_off"), 1)
        self.assertTrue(any("ENGINE OFF" in n for n in rec["notes"]))

    def test_slow_day_stops_at_the_time_budget_without_touching_the_rest(self):
        jsave("pipeline_state/candidates.json", {"x": {"slug": "x", "name": "X", "status": "queued", "description": "a folk dance"}})
        with patch.object(spending, "_ALLOWANCE", spending.ModelAllowance(free_policy())), patch.object(research, "research_one") as one, \
                patch.object(research, "load_catalog", return_value=[]), patch.dict("os.environ", {"GEMINI_API_KEY": "fixture", "RESEARCH_MAX_MINUTES": "-1"}):
            rec = research.run(budget_new=1, budget_enrich=0)
        one.assert_not_called()
        self.assertEqual(rec["counters"].get("time_budget_reached"), 1)

    def test_quotes_in_other_scripts_are_checked_not_waved_through(self):
        ev = {"wikipedia_other": [{"url": "https://ru.wikipedia.org/wiki/X", "text": "Барыня — русская народная пляска и музыка, под которую она исполняется."},
                                  {"url": "https://ja.wikipedia.org/wiki/Y", "text": "阿波踊りは、徳島県を発祥とする盆踊りである。"}]}
        claims = [{"source": "https://ru.wikipedia.org/wiki/X", "quote": "русская народная пляска и музыка, под которую она исполняется"},
                  {"source": "https://ru.wikipedia.org/wiki/X", "quote": "французский придворный танец семнадцатого века"},
                  {"source": "https://ja.wikipedia.org/wiki/Y", "quote": "徳島県を発祥とする盆踊りである"},
                  {"source": "https://ja.wikipedia.org/wiki/Y", "quote": "東京都で生まれた新しい舞踊である"}]
        self.assertEqual([c["supported"] for c in research.verify_claims(claims, ev)[0]], [True, False, True, False])

    def test_a_tradition_is_read_in_its_own_language_first(self):
        self.assertEqual(research.lang_order({"country": "Hungary"})[0], "hu")
        self.assertEqual(research.lang_order({"country_code": "GE"})[0], "ka")
        self.assertEqual(research.lang_order({})[:2], ["es", "fr"])
        self.assertIn("ca", research.lang_order({}))   # unknown country: the smaller Wikipedias still get a turn

    def test_a_failed_video_read_never_replaces_a_studied_one_and_is_retried_soon(self):
        from . import pedagogy
        good = {"status": "ok", "slug": "a", "analysed_at": "2026-10-01T00:00:00Z", "extraction": {"counting_scheme": "1-2-3"}}
        jsave("v.json", good)
        self.assertEqual(pedagogy.keep_or_save("v.json", {"status": "failed", "analysed_at": "2026-11-16T00:00:00Z"}), "kept")
        self.assertEqual(jload("v.json")["extraction"], good["extraction"])
        self.assertEqual(pedagogy.keep_or_save("w.json", {"status": "failed", "analysed_at": "2026-11-16T00:00:00Z"}), "failed")
        self.assertEqual((pedagogy.wait_days(jload("w.json")), pedagogy.wait_days({"status": "failed", "attempts": 3}), pedagogy.wait_days({"status": "ok"})), (2, 30, 30))

    def test_unconfirmed_and_rejected_lessons_stay_off_the_site(self):
        lessons = {"a": {"lessons": [{"youtube_id": "praised", "lesson_status": "in_review"}, {"youtube_id": "cand", "lesson_status": "candidate"},
                                     {"youtube_id": "seen", "lesson_status": "candidate"}, {"youtube_id": "bad", "lesson_status": "in_review"}]}}
        style = {}
        build_catalog.attach_media("a", style, {}, {}, lessons, {"seen": "ok", "bad": "not_a_lesson"})
        self.assertEqual([l["youtube_id"] for l in style["tutorials"]], ["praised", "seen"])


def full_record():
    long = "A sourced sentence that is clearly long enough to count as real content."
    return {"status": "researched", "images": [{"url": "u"}],
            "profile": {"tradition_status": "living", "sections": {"origins_and_history": long, "occasions_and_meaning": long, "costume_and_setting": long},
                        "teaching": {"basic_steps": ["Step forward on the left foot", "Close the right foot beside it", "Step back on the left foot"]},
                        "music_profile": {"meter": "2/4", "instruments": ["drum"], "sound_description": long},
                        "movement_profile": {"footwork": "Walk on counts 1-2-3-4 with a small kick on 4.", "posture": long, "arms_and_hands": long, "formation_and_space": long,
                                             "signature_moves": [{"name": "a"}, {"name": "b"}], "what_to_avoid": long}}}


class StartingLineTests(unittest.TestCase):
    style = {"hero_qc": {"verdict": "pass"}}
    qc = {"publish_gate": "publish"}
    lesson = {"extraction": {"steps_taught": [{"name": "basic", "counts": "1-2"}, {"name": "turn", "counts": "3-4"}], "counting_scheme": "1-2-3-4",
                             "lesson_structure": [{}, {}, {}], "common_mistakes": ["rushing"]}}
    show = {"observation": {"posture": "Upright torso, knees soft, weight forward.", "arms_and_hands": "Arms swing freely from the shoulder.",
                            "formation_and_space": "Two facing lines travelling sideways.", "footwork": "small steps", "costume_and_props": "Embroidered vests and long skirts.",
                            "signature_moments": [{"what": "a"}, {"what": "b"}], "music_heard": {"instruments": ["drum"], "meter_feel": "duple"}}}

    def test_complete_profile_with_a_studied_lesson_is_active_ready(self):
        out = readiness.evaluate(self.style, full_record(), self.qc, [self.lesson], [])
        self.assertEqual((out["state"], out["missing"]), ("active_ready", []))

    def test_no_video_study_no_checked_video_or_unpublished_is_not_ready(self):
        self.assertEqual(readiness.evaluate(self.style, full_record(), self.qc)["missing"], ["study_video"])
        self.assertEqual(readiness.evaluate({}, full_record(), self.qc, [self.lesson])["missing"], ["hero_video"])
        self.assertEqual(readiness.evaluate(self.style, full_record(), {"publish_gate": "review"}, [self.lesson])["state"], "not_published")

    def test_a_performance_shows_the_body_but_never_supplies_counts(self):
        rec = full_record()
        rec["profile"]["movement_profile"] = {}
        rec["profile"]["teaching"] = {}
        out = readiness.evaluate(self.style, rec, self.qc, [], [self.show])
        self.assertIn("footwork_counts", out["missing"])
        self.assertNotIn("posture", out["missing"])
        self.assertEqual(out["via"]["posture"], "performance")
        with_lesson = readiness.evaluate(self.style, rec, self.qc, [self.lesson], [self.show])
        self.assertEqual((with_lesson["state"], with_lesson["via"]["footwork_counts"]), ("active_ready", "lesson"))

    def test_sacred_is_story_only_and_a_keyword_alone_is_not_a_restriction(self):
        rec = full_record()
        rec["profile"]["is_sacred"] = True
        self.assertEqual(readiness.evaluate(self.style, rec, self.qc)["state"], "story_ready_teaching_withheld")
        cue = full_record()
        cue["sacred_cue_flag"] = True
        out = readiness.evaluate(self.style, cue, self.qc, [self.lesson])
        self.assertEqual((out["state"], out.get("ritual_context")), ("active_ready", True))

    def test_run_writes_the_list_history_and_page(self):
        with tempfile.TemporaryDirectory() as root:
            jsave(os.path.join(root, "public/catalog/dances.app.json"), {"styles": {"a": dict(self.style, name="A"), "b": {"name": "B"}}})
            jsave(os.path.join(root, "pipeline_state/qc_index.json"), {"a": self.qc})
            jsave(os.path.join(root, "pipeline_state/research_index.json"), {"a": {"status": "researched"}})
            jsave(os.path.join(root, "research_results/a.json"), full_record())
            jsave(os.path.join(root, "pedagogy/videos/v.json"), dict(self.lesson, status="ok", slug="a"))
            out = readiness.run(root, dt.date(2026, 11, 16))["counters"]
            self.assertEqual((out["listed"], out["published"], out["active_ready"]), (2, 1, 1))
            self.assertEqual(jload(os.path.join(root, "public/catalog/active_ready.json"))["active_ready"], ["a"])
            self.assertEqual(len(jload(os.path.join(root, "pipeline_state/active_ready_history.json"))), 1)
            with open(os.path.join(root, "ACTIVE_READY.md"), encoding="utf-8") as page:
                self.assertIn("1 profile is active-ready", page.read())


if __name__ == "__main__":
    unittest.main()

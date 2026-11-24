"""Offline checks for the footage check of 24 November 2026: a clip found by a dance's name is footage only once its
list was read and the reader said it shows the dance; an unknown licence is not a licence."""
import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from . import build_catalog, common, footage, readiness
from .common import jload
from .test_foundation import TemporaryProject, record

PONY_RALLY = {"title": "File:Regional Pony Rally.webm", "url": "https://example.org/rally.webm", "license": "CC BY-SA 4.0", "source": "commons",
              "description": "Regional Pony Rally, 2016"}
PONY_DANCE = {"title": "File:The Pony, a 1960s dance.webm", "url": "https://example.org/pony-dance.webm", "license": "CC BY 4.0", "source": "commons",
              "description": "Two dancers show the Pony."}
PONY_FILM = {"title": "Learn to dance the Pony (VHS)", "url": "https://example.org/details/pony-vhs", "license": "unknown (Internet Archive)",
             "source": "archive", "description": "A dance lesson."}


def with_footage(slug, clips):
    rec = record(slug)
    rec["footage"] = clips
    return rec


def read(slug, rec, keep):
    """A check as the stage writes it."""
    return {slug: {"key": footage.key_of(footage.clips_of(rec)), "keep": keep}}


class ConfirmedTests(unittest.TestCase):
    def test_an_unread_list_is_no_footage(self):
        rec = with_footage("pony", [PONY_RALLY, PONY_DANCE])
        self.assertEqual(footage.confirmed("pony", rec, {}), [])
        self.assertEqual(footage.confirmed("pony", rec, None), [])
        self.assertEqual(footage.confirmed("pony", record("pony"), read("pony", rec, [PONY_DANCE["url"]])), [])   # no list at all

    def test_only_the_clips_the_reader_kept_and_in_their_order(self):
        rec = with_footage("pony", [PONY_RALLY, PONY_DANCE, PONY_FILM])
        kept = footage.confirmed("pony", rec, read("pony", rec, [PONY_FILM["url"], PONY_DANCE["url"]]))
        self.assertEqual([f["url"] for f in kept], [PONY_DANCE["url"], PONY_FILM["url"]])

    def test_a_list_that_changed_since_it_was_read_is_unread_again(self):
        old = with_footage("pony", [PONY_RALLY, PONY_DANCE])
        new = with_footage("pony", [PONY_DANCE, PONY_FILM])           # research found other clips
        self.assertEqual(footage.confirmed("pony", new, read("pony", old, [PONY_DANCE["url"]])), [])

    def test_an_unknown_licence_is_not_a_licence(self):
        self.assertEqual([f["url"] for f in footage.licensed([PONY_DANCE, PONY_FILM, {"url": "u", "license": ""}, {"url": "v"}])], [PONY_DANCE["url"]])


class AskTests(unittest.TestCase):
    def ask(self, answer, clips=(PONY_RALLY, PONY_DANCE, PONY_FILM)):
        llm = Mock()
        llm.json.return_value = answer
        out = footage.ask(llm, with_footage("pony", list(clips)), list(clips))
        return out, llm

    def test_one_question_carries_the_dance_and_every_clip(self):
        out, llm = self.ask({"clips": [{"n": 1, "verdict": "no"}, {"n": 2, "verdict": "YES"}, {"n": 3, "verdict": "unsure"}]})
        self.assertEqual(out, ["no", "yes", "unsure"])
        asked = json.loads(llm.json.call_args.args[1])
        self.assertEqual((asked["dance"]["name"], [c["n"] for c in asked["clips"]]), ("pony", [1, 2, 3]))
        self.assertIn("Regional Pony Rally", asked["clips"][0]["title"])

    def test_a_clip_the_answer_leaves_out_or_words_oddly_is_unsure(self):
        out, _ = self.ask({"clips": [{"n": 2, "verdict": "yes"}, {"n": 3, "verdict": "probably"}, {"n": 9, "verdict": "yes"}, {"n": True, "verdict": "yes"}]})
        self.assertEqual(out, ["unsure", "yes", "unsure"])

    def test_no_usable_answer_is_no_reading(self):
        for answer in (None, [], {"clips": "yes"}, {"clips": []}, {"verdict": "yes"}):
            self.assertIsNone(self.ask(answer)[0], answer)


class StageTests(TemporaryProject):
    def project(self, slugs):
        self.save("pipeline_state/research_index.json", {s: {"status": "researched"} for s in slugs})
        for s in slugs:
            self.save(f"research_results/{s}.json", with_footage(s, [dict(PONY_RALLY, url=f"https://example.org/{s}/rally"),
                                                                         dict(PONY_DANCE, url=f"https://example.org/{s}/dance")]))

    def night(self, answers, budget=150, served=True):
        llm = Mock(enabled=True, unserved=0, why={})

        def one(system, user, **kw):
            answer = answers.pop(0)
            if answer is None and not served:
                llm.unserved += 1
            return answer
        llm.json.side_effect = one
        with patch.object(common, "LLM", return_value=llm):
            result = footage.run(budget=budget)
        return result, llm

    def test_a_reading_is_written_down_and_not_asked_twice(self):
        self.project(["a", "b"])
        yes_second = {"clips": [{"n": 1, "verdict": "no"}, {"n": 2, "verdict": "yes"}]}
        result, llm = self.night([yes_second, {"clips": [{"n": 1, "verdict": "no"}, {"n": 2, "verdict": "unsure"}]}])
        checks = jload("pipeline_state/footage_checks.json")
        self.assertEqual((checks["a"]["keep"], checks["b"]["keep"]), (["https://example.org/a/dance"], []))
        self.assertEqual((checks["b"]["no"], checks["b"]["unsure"]), (1, 1))
        self.assertEqual({k: result["counters"].get(k) for k in ("lists_read", "clips_kept", "clips_left_out", "lists_with_nothing_kept", "lists_waiting")},
                         {"lists_read": 2, "clips_kept": 1, "clips_left_out": 3, "lists_with_nothing_kept": 1, "lists_waiting": 0})
        again, llm2 = self.night([])
        self.assertEqual((llm2.json.call_count, again["counters"].get("lists_read")), (0, None))
        kept = footage.confirmed("a", jload("research_results/a.json"), checks)
        self.assertEqual([f["url"] for f in kept], ["https://example.org/a/dance"])

    def test_the_budget_and_the_starting_line_decide_which_lists_are_read_first(self):
        self.project(["a", "b", "c"])
        self.save("pipeline_state/active_ready.json", {"profiles": {"c": {"state": "active_ready"}, "a": {"state": "not_published"}}})
        self.save("pipeline_state/qc_index.json", {"b": {"publish_gate": "publish"}})
        result, llm = self.night([{"clips": [{"n": 2, "verdict": "yes"}]}, {"clips": [{"n": 2, "verdict": "yes"}]}], budget=2)
        self.assertEqual(sorted(jload("pipeline_state/footage_checks.json")), ["b", "c"])     # the one on the line, then the published one
        self.assertEqual(json.loads(llm.json.call_args_list[0].args[1])["dance"]["name"], "c")
        self.assertEqual(result["counters"]["lists_waiting"], 1)

    def test_an_answer_nobody_can_use_is_skipped_and_the_stage_goes_on(self):
        self.project(["a", "b"])
        result, _ = self.night([{"oops": 1}, {"clips": [{"n": 1, "verdict": "yes"}]}])
        self.assertEqual(sorted(jload("pipeline_state/footage_checks.json")), ["b"])
        self.assertEqual((result["counters"]["unanswered"], result["counters"].get("stopped_early")), (1, None))

    def test_the_stage_stops_after_three_lists_in_a_row_no_model_answered(self):
        self.project(["a", "b", "c", "d", "e"])
        result, llm = self.night([None, None, None, {"clips": [{"n": 1, "verdict": "yes"}]}], served=False)
        self.assertEqual((llm.json.call_count, result["counters"]["stopped_early"], result["counters"]["lists_waiting"]), (3, 1, 5))
        self.assertIsNone(jload("pipeline_state/footage_checks.json", None))

    def test_an_engine_that_is_off_reads_nothing(self):
        self.project(["a"])
        with patch.object(common, "LLM", return_value=Mock(enabled=False)):
            result = footage.run()
        self.assertEqual(result["counters"], {"engine_off": 1})


class WhatIsPublishedTests(TemporaryProject):
    def build(self, checks):
        rec = with_footage("new", [PONY_RALLY, PONY_DANCE])
        q = {"publish_gate": "publish", "qc_score": 9, "is_sacred": False}
        self.save("app_catalog.json", {"styles": {"old": {"slug": "old", "name": "old"}}})
        self.save("pipeline_state/qc_index.json", {"new": q})
        self.save("research_results/new.json", rec)
        self.save("qc_results/new.json", q)
        if checks:
            self.save("pipeline_state/footage_checks.json", read("new", rec, checks))
        build_catalog.run()
        return jload("public/catalog/dances.app.v2.json", None) or jload("public/catalog/dances.app.json")

    def published_footage(self, checks):
        self.build(checks)
        found = []
        for path in Path("public/catalog").glob("*.json"):
            text = path.read_text(encoding="utf-8")
            if "example.org/rally.webm" in text or "example.org/pony-dance.webm" in text:
                found.append((path.name, "example.org/rally.webm" in text, "example.org/pony-dance.webm" in text))
        return found

    def test_the_catalogue_carries_no_clip_from_an_unread_list(self):
        self.assertEqual(self.published_footage(None), [])

    def test_the_catalogue_carries_the_kept_clip_and_not_the_other(self):
        found = self.published_footage([PONY_DANCE["url"]])
        self.assertTrue(found)
        self.assertTrue(all(dance and not rally for _, rally, dance in found), found)

    def test_readiness_counts_a_clip_only_when_it_was_kept_and_declares_a_licence(self):
        rec = with_footage("pony", [PONY_RALLY, PONY_FILM])
        count = lambda checks: bool(footage.licensed(footage.confirmed("pony", rec, checks)))
        self.assertFalse(count({}))                                                        # unread
        self.assertFalse(count(read("pony", rec, [PONY_FILM["url"]])))                     # kept, licence unknown
        self.assertTrue(count(read("pony", rec, [PONY_RALLY["url"], PONY_FILM["url"]])))   # kept, licence declared
        self.assertIn("footage_licensed(footage_confirmed(", Path(readiness.__file__).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

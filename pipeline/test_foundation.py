"""Offline regressions for catalogue delivery, completion cost and pack freshness."""
import hashlib
import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

from . import build_catalog, episodes, research, run
from .common import jload, jsave


def record(slug):
    return {"slug": slug, "name": slug, "status": "researched", "schema": 5,
            "researched_at": "2026-01-01T00:00:00Z", "sources": ["https://example.org/source"],
            "profile": {"name": slug, "country": "France", "profile": "A sourced description.",
                        "is_sacred": False, "sections": {}, "music_profile": {}, "movement_profile": {}}}


class TemporaryProject(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.previous = os.getcwd()
        os.chdir(self.directory.name)

    def tearDown(self):
        os.chdir(self.previous)
        self.directory.cleanup()

    def save(self, path, data):
        jsave(path, data)


class CatalogueTests(TemporaryProject):
    def build(self):
        self.save("app_catalog.json", {"styles": {"old": {"slug": "old", "name": "old"}}})
        q = {"publish_gate": "publish", "qc_score": 9, "is_sacred": False}
        self.save("pipeline_state/qc_index.json", {"new": q, "old": q})
        for slug in ("old", "new"):
            self.save(f"research_results/{slug}.json", record(slug))
            self.save(f"qc_results/{slug}.json", dict(q, is_sacred=(slug == "old")))
        self.save("tutorial_results.json", {s: {"lessons": [{"youtube_id": s + "-lesson"}]} for s in ("old", "new")})
        self.save("hero_results.json", {"new": {"hero_video_youtube_id": "new-hero", "status": "ok"}})
        self.save("pipeline_state/hero_qc.json", {"new": {"verdict": "pass", "checked_at": "today"}})
        build_catalog.run()
        return jload("public/catalog/dances.app.json")["styles"]

    def test_new_tutorials_and_hero_metadata_reach_export(self):
        styles = self.build()
        self.assertEqual(styles["new"]["tutorials"], [{"youtube_id": "new-lesson"}])
        self.assertEqual(styles["new"]["hero_qc"]["verdict"], "pass")
        self.assertEqual(jload("public/catalog/stats.json")["research_gates"], {"publish": 2})

    def test_new_restriction_blocks_teaching_on_original_entry(self):
        self.assertNotIn("tutorials", self.build()["old"])

    def test_existing_links_preserved_unless_restricted(self):
        style = {"tutorials": [{"youtube_id": "bundled"}]}
        build_catalog.attach_media("a", style, {}, {}, {})
        self.assertEqual(len(style["tutorials"]), 1)
        style["_is_sacred"] = True
        build_catalog.attach_media("a", style, {}, {}, {})
        self.assertNotIn("tutorials", style)


class ReadinessTests(unittest.TestCase):
    def test_generic_steps_and_unverified_recording_do_not_complete_fields(self):
        comp = {"movement_profile": {"footwork": "Take small steps forward and back while staying relaxed."},
                "music_profile": {"reference_recordings": [{"title": "Unverified recommendation"}]}}
        missing = research.class_checklist(comp)["missing"]
        self.assertIn("footwork_with_counts", missing)
        self.assertIn("recordings", missing)

    def test_explicit_counts_are_recognised(self):
        for text in ("Walk on counts 1-2-3-4 and close on 4.", "Left on count one; right on count two."):
            self.assertTrue(research.has_count_sequence(text), text)
        self.assertFalse(research.has_count_sequence("Count the beats and repeat the steps."))

    def test_no_invented_default_count_or_family_count(self):
        self.assertEqual(episodes.counting_for(None, {}), "")
        self.assertIn("two beats a bar", episodes.counting_for("2/4", {}))
        self.assertNotIn("quick", episodes.counting_for("6/8", {}))
        self.assertIsNone(episodes.patterns_for("a", "family", {"by_family": {"family": {"videos": 4, "counting": "1-8"}}})["counting"])

    def test_missing_posture_and_mistakes_do_not_instruct_renderer_to_invent(self):
        pack = episodes.build_pack(record("a"), {}, {}, {})
        scenes = {s["code"]: s for s in pack["chapters"][0]["scenes"]}
        self.assertEqual(scenes["body"]["narration"], [])
        self.assertEqual(scenes["mistakes"]["narration"], [])
        self.assertTrue(scenes["body"]["needs"])
        self.assertEqual(pack["release_status"], "not_validated")
        self.assertEqual(pack["music_brief"]["rights_status"], "not_assessed")

    def test_failed_selftest_exits_nonzero(self):
        with patch("pipeline.selftest.run", return_value={"counters": {"failures": 1}}):
            self.assertEqual(run.main(["selftest"]), 1)


class CompletionTests(TemporaryProject):
    def setup_queue(self):
        items = [{"slug": s, "name": s, "region": region} for s, region in
                 (("a", "Europe"), ("b", "Europe"), ("c", "Africa"), ("d", "Asia"), ("thin", "Europe"))]
        done = {d["slug"]: {"status": "researched", "schema": 5, "researched_at": "2026-11-01", "class_have": 17} for d in items[:-1]}
        self.save("pipeline_state/research_index.json", done)
        self.save("pipeline_state/qc_index.json", {s: {"publish_gate": "publish"} for s in done})
        self.save("pipeline_state/episode_gaps.json", {s: ["tempo (bpm)"] for s in done})
        return items

    def pick(self, items, n):
        with patch.object(research, "_days_ago", side_effect=lambda days: "2026-11-02" if days == 7 else "2026-09-10"):
            return research.pick_enrichment_targets(items, n)

    def test_completion_share_is_bounded_and_diverse(self):
        chosen = self.pick(self.setup_queue(), 6)
        completion = [d for d in chosen if d.get("_completion_retry")]
        self.assertEqual({d["region"] for d in completion}, {"Europe", "Africa"})
        self.assertEqual(len(completion), 2)
        self.assertIn("thin", {d["slug"] for d in chosen})
        self.assertLessEqual(len(chosen), 6)

    def test_editor_work_first_cooldown_retirement_and_zero_budget(self):
        items = self.setup_queue()
        self.save("pipeline_state/editor_notes.json", {"d": {"note": "Fix an evidence mismatch"}})
        self.save("pipeline_state/completion_followups.json", {"a": {"checked_at": "2026-11-08"}})
        self.save("pipeline_state/audit.json", {"b": {"decision": "retire"}})
        chosen = self.pick(items, 3)
        self.assertEqual(chosen[0]["slug"], "d")
        self.assertFalse({"a", "b"} & {d["slug"] for d in chosen})
        self.assertEqual(self.pick(items, 0), [])
        self.assertFalse(any(d.get("_completion_retry") for d in self.pick(items, 1)))

    def test_media_only_gaps_do_not_spend_research_budget(self):
        items = self.setup_queue()
        self.save("pipeline_state/episode_gaps.json", {s: ["a hero video"] for s in ("a", "b", "c", "d")})
        self.assertEqual([d["slug"] for d in self.pick(items, 6)], ["thin"])

    def test_unchanged_evidence_skips_model(self):
        ev = {"wikipedia": {"url": "https://example.org", "text": "Unchanged evidence"}}
        prev = record("a")
        prev["evidence_fingerprint"] = hashlib.sha256(json.dumps(research._source_texts(ev), sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
        prev["readiness_question_revision"] = 1
        self.save("research_results/a.json", prev)
        with patch.object(research, "gather_evidence", return_value=ev), patch.object(research, "compose") as compose:
            result = research.research_one({"slug": "a", "_completion_retry": True}, Mock())
        compose.assert_not_called()
        self.assertEqual(result, prev)
        self.assertIn("a", jload("pipeline_state/completion_followups.json"))

    def test_failed_refresh_preserves_good_research(self):
        prev = record("a")
        self.save("research_results/a.json", prev)
        ev = {"wikipedia": {"url": "https://example.org", "text": "New evidence"}}
        with patch.object(research, "gather_evidence", return_value=ev), patch.object(research, "compose", return_value=None):
            self.assertEqual(research.research_one({"slug": "a", "_completion_retry": True}, Mock()), prev)
        self.assertEqual(jload("research_results/a.json"), prev)


class EpisodeTests(TemporaryProject):
    def test_fingerprint_tracks_inputs_not_check_timestamps(self):
        rec, qc, style, patterns = record("a"), {"qc_score": 9}, {"hero_qc": {"verdict": "pass", "checked_at": "old"}}, {}
        original = episodes.input_fingerprint(rec, qc, style, patterns)
        style["hero_qc"]["checked_at"] = "new"
        self.assertEqual(original, episodes.input_fingerprint(rec, qc, style, patterns))
        for key, value in (("tutorials", [{"youtube_id": "lesson"}]), ("hero_video_youtube_id", "new-hero")):
            modified = dict(style, **{key: value})
            self.assertNotEqual(original, episodes.input_fingerprint(rec, qc, modified, patterns))
        self.assertNotEqual(original, episodes.input_fingerprint(rec, qc, style, {"counting": "1-2"}))

    def test_targeted_build_retains_other_packs_and_gaps_and_rebuilds_changed_teaching(self):
        self.save("pipeline_state/qc_index.json", {s: {"publish_gate": "publish"} for s in ("a", "b")})
        self.save("public/catalog/dances.app.json", {"styles": {"a": {}, "b": {}}})
        for s in ("a", "b"):
            self.save(f"research_results/{s}.json", record(s))
        episodes.run(polish_budget=0)
        before = jload("episodes/a.json")["input_fingerprint"]
        self.save("pedagogy/teaching_patterns.json", {"by_slug": {"a": {"videos": 1, "counting": "1-2-3"}}})
        episodes.run(polish_budget=0, only=["a"])
        self.assertEqual(set(jload("public/catalog/episodes.json")["packs"]), {"a", "b"})
        self.assertIn("b", jload("pipeline_state/episode_gaps.json"))
        self.assertNotEqual(before, jload("episodes/a.json")["input_fingerprint"])
        self.assertEqual(jload("episodes/a.json")["teaching_formula"]["counting"], "1-2-3")


if __name__ == "__main__":
    unittest.main()

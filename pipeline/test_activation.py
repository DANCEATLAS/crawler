"""Safety of readiness gates, evidence windows, namespaces and offline rebuilding."""
import copy
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest
from . import activation as A
from .pedagogy import evidence_segments

TODAY = dt.date(2026, 11, 11)


class ActiveProfileTests(unittest.TestCase):
    def fixture(self):
        profile = {field: {k: "Evidence from a reviewed source" for k in required}
                   for field, required in A.FIELDS.values()}
        research = {"profile": profile, "sources": ["https://example.org/source"], "claims": [{"supported": True}]}
        videos = [{"channel": channel, "youtube_id": "abcdefghij" + str(i), "url": "https://www.youtube.com/watch?v=abcdefghij" + str(i),
                   "status": "ok", "extraction": {"evidence_segments": [
            {"start_s": 10, "end_s": 20, "topic": topic, "observation": "Teacher demonstrates a step"}]}}
            for i, (channel, topic) in enumerate((("Teacher A", "movement"), ("Teacher B", "teaching")))]
        track = {"asset_id": "recording-one", "status": "reviewed", "reviewer": "Human rights reviewer",
                 "composition_evidence": "https://example.org/composition", "recording_evidence": "https://example.org/master",
                 "quality_review": "https://example.org/musician-review", "territories": ["Global scope"],
                 "conditions": "Attribution recorded", "reviewed_on": "2026-11-10", "recheck_on": "2026-12-10",
                 "valid_from": "2026-01-01", "valid_until": "2026-12-31",
                 "uses": {k: True for k in A.MUSIC_USES}}
        supplement = {"music_options": [track, dict(track, asset_id="recording-two")],
                      "scope": {"languages": ["English"], "audiences": ["Adults"], "session_modes": ["Solo practice"], "territories": ["Global scope"]}}
        return research, videos, supplement

    def build(self, research=None, videos=None, supplement=None, approvals=None):
        return A.build_profile("atlas", "test", {"name": "Test Dance"}, research or {}, videos or [],
                               supplement or {}, approvals or [], TODAY)

    def test_no_false_readiness_from_legacy_flag(self):
        self.assertEqual(self.build({"movie_ready": True})["state"], "researching")
        self.assertFalse(self.build()["runtime_active"])

    def test_review_requires_current_human_evidence(self):
        r, v, s = self.fixture()
        first = self.build(r, v, s)
        self.assertEqual(first["state"], "awaiting_review")
        approvals = [{"role": role, "human_review": True, "fingerprint": first["fingerprint"],
                      "reviewer": "Reviewer name", "evidence": "https://example.org/review",
                      "decision": "approved", "reviewed_on": "2026-11-10", "recheck_on": "2026-12-10"}
                     for role in A.REVIEW_ROLES]
        self.assertEqual(self.build(r, v, s, approvals)["state"], "ready_for_activation")
        self.assertFalse(self.build(r, v, s, approvals)["runtime_active"])
        r["profile"]["movement_profile"]["footwork"] = "A different instruction"
        self.assertEqual(self.build(r, v, s, approvals)["state"], "awaiting_review")

    def test_music_requires_both_rights_all_uses_and_date(self):
        r, v, s = self.fixture()
        for key in ("recording_evidence", "composition_evidence", "quality_review"):
            changed = copy.deepcopy(s)
            changed["music_options"][0][key] = ""
            self.assertTrue(self.build(r, v, changed)["gaps"]["rights"])
        for value in (False, "true"):
            changed = copy.deepcopy(s)
            changed["music_options"][0]["uses"]["social_export"] = value
            self.assertTrue(self.build(r, v, changed)["gaps"]["rights"])
        changed = copy.deepcopy(s)
        changed["music_options"][0]["reviewed_on"] = "2027-01-01"
        self.assertTrue(self.build(r, v, changed)["gaps"]["rights"])
        changed = copy.deepcopy(s)
        changed["music_options"][0]["valid_until"] = "2026-11-01"
        self.assertTrue(self.build(r, v, changed)["gaps"]["rights"])
        s["music_options"][1] = s["music_options"][0]
        self.assertTrue(self.build(r, v, s)["gaps"]["rights"])

    def test_restrictions_preserved(self):
        r, v, s = self.fixture()
        r["profile"]["is_sacred"] = True
        self.assertEqual(self.build(r, v, s)["state"], "teaching_withheld")

    def test_video_bounds_and_independence(self):
        self.assertTrue(A.real("4/4"))
        self.assertTrue(A.real(["en"]))
        valid = {"start_s": 1, "end_s": 30, "topic": "movement", "observation": "Observed"}
        self.assertEqual(len(evidence_segments([valid])), 1)
        for bad in (-1, 481, float("nan"), True, "10"):
            self.assertEqual(evidence_segments([dict(valid, start_s=bad)]), [])
        r, v, s = self.fixture()
        v[1]["channel"] = v[0]["channel"]
        self.assertTrue(self.build(r, v, s)["gaps"]["video"])

    def test_namespaces_retirement_idempotency_and_no_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            A.write_changed(root / "public/catalog/dances.app.json", {"styles": {"test": {"name": "Atlas"}, "retired": {"name": "Old"}}})
            A.write_changed(root / "public/catalog/retired.json", {"retired": [{"slug": "retired"}]})
            A.write_changed(root / "viral_results.json", {"test": {"name": "Viral"}})
            self.assertEqual(A.run(root, TODAY)["counters"]["profiles"], 2)
            self.assertEqual(A.run(root, TODAY)["counters"]["dossiers_changed"], 0)
            index = A.read(root / "public/catalog/active_profiles.json")
            self.assertEqual(set(index["profiles"]), {"atlas:test", "viral:test"})
            self.assertNotEqual(index["profiles"]["atlas:test"]["path"], index["profiles"]["viral:test"]["path"])

    def test_malformed_input_does_not_silently_erase_inventory(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "broken.json"
            path.write_text("{")
            with self.assertRaises(json.JSONDecodeError):
                A.read(path)

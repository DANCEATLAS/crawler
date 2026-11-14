"""Dynamic gaps, source provenance, expiry, fair review and no false completion."""
import copy
import datetime as dt
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import Mock, patch
from . import readiness_research as R, activation as A, research
from .test_foundation import TemporaryProject, record

TODAY = dt.date(2026, 11, 11)
Q = {"domain": "research", "question": "Which partner-role transitions need separate instruction?",
     "why_needed": "The documented roles differ.", "next_evidence": "Compare role-specific practitioner demonstrations.",
     "source": "https://example.org/practitioner"}


class ReadinessResearchTests(unittest.TestCase):
    def test_only_supplied_sources_and_no_self_approval(self):
        self.assertEqual(R.questions([Q], allowed_sources=set()), [])
        self.assertEqual(R.questions([dict(Q, source="http://localhost/x")]), [])
        self.assertEqual(R.questions([dict(Q, source="https://name:secret@example.org/")]), [])
        result = R.questions([dict(Q, status="approved"), Q], {Q["source"]})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["status"], "candidate_unreviewed")

    def test_closure_needs_evidence_and_reopens_on_expiry(self):
        q = dict(Q, status="resolved")
        self.assertEqual(len(R.open_findings({"findings": [q]}, TODAY)), 1)
        q["resolution"] = {"evidence": "https://example.org/test", "reviewer": "Reviewer",
                           "reviewed_on": "2026-11-10", "recheck_on": "2026-12-10"}
        self.assertEqual(R.open_findings({"findings": [q]}, TODAY), [])
        self.assertEqual(len(R.open_findings({"findings": [q]}, dt.date(2026, 12, 11))), 1)
        q["resolution"]["reviewed_on"] = "2027-01-01"
        self.assertEqual(len(R.open_findings({"findings": [q]}, TODAY)), 1)

    def test_exact_typed_identity(self):
        finding = dict(Q, profile_ids=["viral:same"])
        self.assertFalse(R.for_profile([finding], "atlas:same"))
        self.assertTrue(R.for_profile([finding], "viral:same"))
        self.assertFalse(R.for_profile([dict(Q, profile_ids="viral:same")], "viral:same"))

    def test_new_question_changes_fingerprint_and_routes_gap(self):
        args = ("atlas", "test", {"name": "Test"}, {}, [], {}, [], TODAY)
        before = A.build_profile(*args)
        after = A.build_profile(*args, discovered_questions=R.questions([Q]))
        self.assertNotEqual(before["fingerprint"], after["fingerprint"])
        self.assertIn(Q["question"], " ".join(after["gaps"]["research"]))
        self.assertFalse(after["runtime_active"])

    def test_rotating_research_dates_are_not_evaluation_dates(self):
        profiles = {"atlas:a": {"fingerprint": "a"}, "atlas:b": {"fingerprint": "b"},
                    "viral:a": {"fingerprint": "v"}}
        registry = {"area_reviews": {R.AREAS[0]: {"checked_on": "2026-11-10"}},
                    "profile_reviews": {"atlas:a": {"checked_on": "2026-11-10", "fingerprint": "a"}}}
        original = copy.deepcopy(registry)
        with tempfile.TemporaryDirectory() as temp:
            agenda = R.write_agenda(temp, profiles, TODAY, registry, Counter())
            self.assertEqual(agenda["next_focus"], R.AREAS[1])
            self.assertEqual(agenda["profile_sample"], ["atlas:b", "viral:a"])
            self.assertIsNone(agenda["last_external_research"])
            self.assertEqual(registry, original)
            registry["profile_reviews"]["atlas:a"]["fingerprint"] = "old"
            self.assertEqual(R.write_agenda(temp, profiles, TODAY, registry, Counter())["profile_sample"][0], "atlas:a")


class ResearchIntegrationTests(TemporaryProject):
    def test_new_questions_reach_prompt_before_legacy_gaps(self):
        prev = record("a")
        prev["profile"]["gaps"] = ["old " + str(i) for i in range(8)]
        prev["class_checklist"] = {"missing": ["legacy " + str(i) for i in range(8)]}
        self.save("research_results/a.json", prev)
        self.save("pipeline_state/activation_gaps.json", {"profiles": {"atlas:a": {
            "gaps": {"research": ["fixed " + str(i) for i in range(4)] + ["Investigate: new requirement"]}}}})
        with patch.object(research, "gather_evidence", return_value={"wikipedia": {"url": "https://example.org", "text": "Evidence"}}), \
                patch.object(research, "compose", return_value=None) as compose:
            research.research_one({"slug": "a", "_completion_retry": True}, Mock())
        hints = compose.call_args.kwargs["prev_gaps"][:12]
        self.assertTrue(any("new requirement" in q for q in hints))

    def test_existing_evidence_gets_one_requirements_review(self):
        import hashlib
        prev = record("a")
        ev = {"wikipedia": {"url": "https://example.org", "text": "Unchanged evidence"}}
        prev["evidence_fingerprint"] = hashlib.sha256(json.dumps(research._source_texts(ev), sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        self.save("research_results/a.json", prev)
        with patch.object(research, "gather_evidence", return_value=ev), patch.object(research, "compose", return_value=None) as compose:
            research.research_one({"slug": "a", "_completion_retry": True}, Mock())
        compose.assert_called_once()
        self.assertEqual(json.loads(Path("research_results/a.json").read_text()), prev)


if __name__ == "__main__":
    unittest.main()

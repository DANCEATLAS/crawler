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


class ResearchNightTests(TemporaryProject):
    """A night on which the models do not answer (23 November 2026) is the provider's night, not the dances'."""

    def night(self, outcomes):
        """One queued dance per outcome, oldest first: "ok" (written), "failed" (the writer answered and the profile
        was not usable), "nobody" (a question got no answer of any kind from any model). Returns the dances tried, the queue
        and the run record."""
        cands = {f"d{i}": {"slug": f"d{i}", "name": f"Dance {i}", "status": "queued", "description": "a folk dance of somewhere",
                           "found_at": f"2026-11-{i + 1:02d}"} for i in range(len(outcomes))}
        self.save("pipeline_state/candidates.json", cands)
        llm, tried = Mock(enabled=True, why={}, unserved=0), []

        def one(d, llm_, sb):
            outcome = outcomes[len(tried)]
            tried.append(d["slug"])
            if outcome == "nobody":
                llm.unserved += 1
            return {"slug": d["slug"], "researched_at": "2026-11-24T00:00:00Z", "status": "researched" if outcome == "ok" else "llm_failed"}

        with patch.object(research, "LLM", return_value=llm), patch.object(research, "Supabase"), patch.object(research, "load_catalog", return_value=[]), \
                patch.object(research, "pick_enrichment_targets", return_value=[]), patch.object(research, "research_one", side_effect=one):
            result = research.run(budget_new=len(outcomes), budget_enrich=0)
        return tried, json.loads(Path("pipeline_state/candidates.json").read_text()), result

    def test_a_write_that_no_model_answered_is_not_counted_against_the_dance(self):
        tried, cands, _ = self.night(["nobody", "failed", "ok"])
        self.assertEqual(tried, ["d0", "d1", "d2"])
        self.assertEqual([(cands[s]["status"], cands[s].get("attempts")) for s in tried], [("queued", None), ("queued", 1), ("researched", None)])

    def test_research_stops_after_three_dances_in_a_row_were_lost_to_the_provider(self):
        tried, cands, result = self.night(["ok", "nobody", "nobody", "ok", "nobody", "nobody", "nobody", "ok", "ok"])
        self.assertEqual(tried, ["d0", "d1", "d2", "d3", "d4", "d5", "d6"])        # two in a row do not stop it; the third in a row does
        self.assertEqual([cands[s]["status"] for s in ("d7", "d8")], ["queued", "queued"])   # the queue keeps its place
        self.assertTrue(all(cands[s].get("attempts") is None for s in cands))
        self.assertEqual(result["counters"].get("stopped_early"), 1)

    def test_a_kept_profile_counts_only_when_no_model_answered(self):
        self.assertTrue(research.lost_to_provider("researched", True, 2, 3))     # a deepening nobody answered: the existing profile stands
        self.assertFalse(research.lost_to_provider("researched", True, 2, 2))    # the writer answered and the profile was not usable
        self.assertFalse(research.lost_to_provider("researched", False, 2, 3))   # written in the end, although one question got no answer
        self.assertFalse(research.lost_to_provider("llm_failed", False, 2, 2))   # the writer answered and failed: that is counted


if __name__ == "__main__":
    unittest.main()

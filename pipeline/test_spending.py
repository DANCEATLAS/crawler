"""Offline checks: credentials alone cannot spend; all HTTP retries share a cap."""
import copy
import datetime as dt
import json
import unittest
from unittest.mock import patch
from . import common, spending


def policy():
    return {"schema": 1, "llm_enabled": True, "expires_on": dt.date.today().isoformat(),
            "authorization_reference": "offline fixture only", "models": {"openai": ["test-mini"], "gemini": ["test-flash"]},
            "max_http_attempts_per_process": 2, "max_output_tokens_per_request": 100,
            "max_reserved_output_tokens_per_process": 200}


class SpendingTests(unittest.TestCase):
    def test_missing_malformed_expired_policy_fails_closed(self):
        for p in ({}, [], {"llm_enabled": "true"}, dict(policy(), expires_on="2000-01-01")):
            a = spending.ModelAllowance(p)
            self.assertFalse(a.permitted("openai"))
            with self.assertRaises(spending.SpendingBlocked): a.reserve("openai", "test-mini", 40)

    def test_disabled_policy_even_with_credentials_cannot_make_network_requests(self):
        with patch.object(spending, "_ALLOWANCE", spending.ModelAllowance({})), \
                patch.dict("os.environ", {"OPENAI_API_KEY": "fixture", "GEMINI_API_KEY": "fixture"}), \
                patch.object(common, "http") as http:
            llm = common.LLM()
            self.assertFalse(llm.enabled)
            self.assertIsNone(llm.json("system", "user"))
            for fn in (llm._openai, llm._gemini):
                with self.assertRaises(spending.SpendingBlocked): fn("test-mini", "system", "user")
            http.assert_not_called()

    def test_pinned_allowlist_no_upgrade_or_model_discovery(self):
        with patch.object(spending, "_ALLOWANCE", spending.ModelAllowance(policy())), patch.object(common, "http") as http:
            llm = common.LLM()
            self.assertEqual(llm.openai_models(True), ["test-mini"])
            self.assertEqual(llm.gemini_models(True), ["test-flash"])
            http.assert_not_called()

    def test_http_retry_and_second_stage_share_attempt_allowance(self):
        a = spending.ModelAllowance(policy())
        result = (200, json.dumps({"choices": [{"message": {"content": "{}"}}]}), {})
        with patch.object(spending, "_ALLOWANCE", a), patch.object(common, "http", side_effect=[common.HttpError(400, "max_tokens", "https://example.org"), result]) as http:
            first = common.LLM(); first._openai("test-mini", "s", "u", max_tokens=100)
            second = common.LLM()
            with self.assertRaises(spending.SpendingBlocked): second._openai("test-mini", "s", "u", max_tokens=100)
            self.assertEqual(http.call_count, 2)
            self.assertEqual(a.reserved_output_tokens, 200)
            self.assertEqual(first.calls, 2)

    def test_invalid_limits_and_unlisted_models_block(self):
        for field in ("max_http_attempts_per_process", "max_output_tokens_per_request", "max_reserved_output_tokens_per_process"):
            p = policy(); p[field] = "100"
            with self.assertRaises(spending.SpendingBlocked): spending.ModelAllowance(p).reserve("openai", "test-mini", 40)
        with self.assertRaises(spending.SpendingBlocked): spending.ModelAllowance(policy()).reserve("openai", "costly-new", 40)

    def test_quota_stop_is_shared_between_stages(self):
        a = spending.ModelAllowance(policy())
        a.stopped.add("gemini")
        self.assertEqual(a.models("gemini"), [])
        self.assertEqual(a.models("openai"), ["test-mini"])

    def test_error_does_not_print_key_in_url(self):
        self.assertNotIn("private-key", str(common.HttpError(401, "denied", "https://example.org?key=private-key")))


if __name__ == "__main__":
    unittest.main()

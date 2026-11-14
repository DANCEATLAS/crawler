"""Fail-closed model permission and process-wide request limits; no network.

These limits are not a billing-account dollar cap. All model calls are currently
disabled. A later authorization must name exact models and a dated allowance.
"""
import datetime as dt
import json
from pathlib import Path


class SpendingBlocked(RuntimeError):
    pass


class ModelAllowance:
    def __init__(self, policy=None):
        self.policy = policy if isinstance(policy, dict) else {}
        self.attempts = 0
        self.reserved_output_tokens = 0
        self.stopped = set()

    def permitted(self, provider):
        p = self.policy
        try:
            valid = (p.get("schema") == 1 and p.get("llm_enabled") is True
                     and dt.date.today() <= dt.date.fromisoformat(p["expires_on"])
                     and bool(p.get("authorization_reference"))
                     and isinstance(p["models"][provider], list)
                     and all(isinstance(m, str) and m and "latest" not in m
                             for m in p["models"][provider]))
            return bool(valid and p["models"][provider] and provider not in self.stopped)
        except (KeyError, TypeError, ValueError):
            return False

    def models(self, provider):
        return self.policy["models"][provider][:] if self.permitted(provider) else []

    def reserve(self, provider, model, tokens):
        """Reserve before EACH HTTP attempt, including retries and malformed replies."""
        if model not in self.models(provider):
            raise SpendingBlocked("Model API calls are not authorized by the spending policy")
        try:
            p = self.policy
            limits = [p[k] for k in ("max_http_attempts_per_process", "max_output_tokens_per_request",
                                    "max_reserved_output_tokens_per_process")]
            if any(type(n) is not int or n <= 0 for n in limits) or type(tokens) is not int or tokens <= 0:
                raise ValueError("invalid limits")
            attempts, per_request, total = limits
            cap = min(tokens, per_request)
            if self.attempts >= attempts or self.reserved_output_tokens + cap > total:
                raise ValueError("allowance exhausted")
        except (KeyError, TypeError, ValueError):
            raise SpendingBlocked("Model request allowance is missing or exhausted") from None
        self.attempts += 1
        self.reserved_output_tokens += cap
        return cap


_ALLOWANCE = None


def allowance():
    global _ALLOWANCE
    if _ALLOWANCE is None:
        # Repository policy only: missing/malformed policy blocks calls, even with credentials.
        try:
            policy = json.loads(Path("pipeline_state/spending_policy.json").read_text())
        except (OSError, ValueError):
            policy = {}
        _ALLOWANCE = ModelAllowance(policy)
    return _ALLOWANCE

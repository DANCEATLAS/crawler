"""Fail-closed model permission and process-wide request limits; no network.

Schema 1 names exact models. Schema 2 (16 Nov 2026) adds a zero-cost lane:
``free_tier_families`` lets a provider whose key has NO billing attached use
whole model families (Gemini flash / flash-lite), so a retired model name does
not silently stop the library for months. Paid providers still need exact
names and stay off unless listed. These limits are not a billing-account
dollar cap: the free lane costs nothing only while the key stays unbilled.
"""
import datetime as dt
import json
from pathlib import Path

FAMILIES = ("flash-lite", "flash")          # never "pro": not part of the free lane
SKIP = ("image", "tts", "live", "audio", "embedding", "thinking", "exp", "dialog", "computer-use", "robotics",
        "deep-research", "veo", "imagen", "learnlm", "gemma", "aqa", "nano", "vision", "8b", "omni", "lyria", "pro")


class SpendingBlocked(RuntimeError):
    pass


def family_of(model):
    """'flash-lite' | 'flash' | None for a Gemini model name; None for anything outside the free lane."""
    low = str(model or "").lower()
    if not low.startswith("gemini-") or "latest" in low or any(k in low for k in SKIP):
        return None
    return "flash-lite" if "flash-lite" in low else ("flash" if "flash" in low else None)


class ModelAllowance:
    def __init__(self, policy=None):
        self.policy = policy if isinstance(policy, dict) else {}
        self.attempts = 0
        self.reserved_output_tokens = 0
        self.stopped = set()

    def _base_ok(self):
        p = self.policy
        try:
            return bool(p.get("schema") in (1, 2) and p.get("llm_enabled") is True
                        and dt.date.today() <= dt.date.fromisoformat(p["expires_on"])
                        and p.get("authorization_reference"))
        except (KeyError, TypeError, ValueError):
            return False

    def _exact(self, provider):
        try:
            names = self.policy["models"][provider]
        except (KeyError, TypeError):
            return []
        if not isinstance(names, list) or not all(isinstance(m, str) and m and "latest" not in m for m in names):
            return []
        return names[:]

    def families(self, provider):
        """Free-lane families for this provider (schema 2 only); [] when the lane is closed."""
        if not self._base_ok() or self.policy.get("schema") != 2 or provider in self.stopped:
            return []
        fams = (self.policy.get("free_tier_families") or {}).get(provider) if isinstance(self.policy.get("free_tier_families"), dict) else None
        if provider != "gemini" or not isinstance(fams, list):
            return []
        return [f for f in fams if f in FAMILIES]

    def permitted(self, provider):
        return bool(self._base_ok() and provider not in self.stopped and (self._exact(provider) or self.families(provider)))

    def models(self, provider):
        return self._exact(provider) if self.permitted(provider) else []

    def allows(self, provider, model):
        return bool(self.permitted(provider) and (model in self._exact(provider) or family_of(model) in self.families(provider)))

    def reserve(self, provider, model, tokens):
        """Reserve before EACH HTTP attempt, including retries and malformed replies."""
        if not self.allows(provider, model):
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

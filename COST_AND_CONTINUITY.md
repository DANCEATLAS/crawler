# Spending and durable research

## 16 November 2026 — the free lane

The 14 November pause below went live on 16 November and switched the writing engine off. Two things followed that nobody intended: the library stopped growing (it had been adding about 128 published profiles a week), and the research stage would have replaced six to ten existing profiles a day with empty stubs, because a failed writer overwrote the page it was deepening. Both are fixed.

- **Free tier only.** Verified in Google AI Studio on 16 November: project Default Gemini Project, billing tier Free, no billing attached. Those calls cannot be charged. `pipeline_state/spending_policy.json` (schema 2) opens only the Gemini flash and flash-lite families; OpenAI has no model listed and its key is not passed to any workflow. The OpenAI balance was not inspected.
- **Sized to the free limits** seen that day: flash 20 requests a day per model (kept for the writer), flash-lite 500 a day per model (judges, video). One model's day quota retires that model for the run, not the provider.
- **Names are not pinned** inside the free lane: the model list is read at run time and filtered to the allowed families, so a retired model name cannot stop the library for months. Paid providers still need exact names.
- **The policy ends on 31 December 2027.** The weekly e-mail warns 45 days before. If billing is ever attached to that Google project, switch `llm_enabled` off first.
- **Nothing is lost:** a failed or switched-off writer keeps the existing profile; an engine-off run changes nothing and says ENGINE OFF in `STATUS.md` and the weekly e-mail.
- **Database:** the video, tutorial and Viral push jobs now write only rows that changed (they rewrote about 1,600 unchanged rows a day into the audit log). The existing log of about 541 MB still needs the owner's decision.

The sections below are the 14 November record; where they say generation is paused, this section governs.

## 14 November 2026

The full mission remains V01–V18: every living dance and meaningful variant, Atlas and Viral, an AI BDF leading into consenting human dance friendships, adaptive voice/movement teaching, shared rhythm/camera/split-screen and optional AR, multilingual accessible life-stage teaching, cultural care, creation, music/rights and independent continuity. Better technology can accelerate delivery; it cannot replace permissions, qualified review or demonstrated learning.

## Controls implemented in this change

- Automatic OpenAI/Gemini generation is paused. The two scheduled workflows no longer receive model keys. `pipeline/spending.py` also blocks calls when the repository policy is disabled, missing, malformed or expired; credentials alone never permit spending.
- Any future allowance must name exact models and expire. No discovery of more expensive fallback models. Every HTTP attempt, including compatibility retries, reserves output allowance; stages share the same process budget. Quota exhaustion stops that provider for the process. These are request/output safeguards, not a complete input-token meter or an account-wide dollar cap.
- The existing external requirements task is weekly, Sunday 16:00 Asia/Tokyo, at most two profiles and six external source pages. It still uses ChatGPT plan capacity. Routine results stay in research records and the normal weekly overview. No extra email.
- The watchdog recovers a missed daily schedule only after a successful previous attempt. It does not repeatedly restart failed/cancelled jobs or enable a disabled workflow. Daily stage exceptions and commit/push failures must be visible rather than reported as success.
- Existing valid research survives failed refreshes. Evidence fingerprints and the capped question queue avoid repeated composition. All eleven findings from the 11–13 November research work are preserved, with source dates, uncertainty and exact profile namespaces. No human review or readiness gate is auto-approved.

These controls become operational only when the complete change is on main. Check Git history and the dated ledger for publication/readback. Tests do not prove live execution.

## What continues, and what is paused

Scheduled source collection, deterministic validation, catalogue/queue preparation and the weekly email remain. The weekly external research pass can investigate new evidence and requirements within ChatGPT plan capacity. Model-written enrichment, video-model analysis and translation wait for an explicitly recorded allowance. This trades slower generated-content growth for owner control of money; existing research is retained.

No new subscription, purchase, production generation, Lovable build or workflow budget increase is authorized. GitHub, YouTube, Supabase, hosting and existing subscriptions may still consume their own allowances. Their actual invoices, balances, renewal settings and account-wide caps have not been verified. Never report these unknowns as zero cost. A future model allowance needs a verified billing plan, maximum spend, expiry, metering and a stopping mechanism; the output-reservation limit alone is insufficient for a dollar promise.

## Unresolved reliability work

1. **Database growth:** 11 November inspection found about 541 MiB of audit history and repeated full-row auditing. Measure and suppress unchanged producer updates, preserving genuine change auditing; no history purge or paid upgrade is authorized.
2. **Viral truthfulness:** the current date-ordered view is not a measured popularity chart; scorer/schema differences remain. Repair with bounded observations and an explicit insufficient-data state. Preserve the Viral namespace.
3. **Delivery evidence:** a generated weekly report is not proof of an email reaching the owner. The legacy duplicate guard still uses report date. Add durable provider acceptance/fallback receipts and bounded recovery before claiming exactly-once delivery; do not force-send a test email.
4. **Failure visibility:** the daily command now returns nonzero for uncaught stage exceptions. Some stages still catch their own errors; each requires a meaningful success contract. One green workflow never proves the whole system healthy.
5. **Independent continuity:** Git history and public evidence remain portable. The external research service depends on ChatGPT plan availability and authenticated write access. Verify independent backup restoration, dependencies, mirror freshness, stale evidence and future provider changes; do not promise perpetual availability.

The next external pass retains the longest-unreviewed area, AI interaction/controllable memory. This operational review does not advance that scientific review date or falsely claim another external research pass.

## Owner communication

Keep the existing large-type weekly email: what improved, what remains, what happens next and spending status. Begin a verified owner-only request with **ACTION NEEDED — one simple action**. Use **PLEASE NOTE — important problem** only when awareness matters. Otherwise say **NO ACTION NEEDED**. Research questions are work for the system/reviewer, not implied tasks for the owner. Do not send routine separate findings or a repeated setup request.

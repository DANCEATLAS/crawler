# Instructions for any AI working on Dance Atlas

**Read `LEDGER.md` first. It is short and current (21 November 2026). Then `STATUS.md` and `ACTIVE_READY.md`.** Open `PRODUCT_VISION.md`, `AI_BRIEF.md` and `IMPLEMENTATION_LEDGER.md` only for the section a task needs: the owner pays for every page an AI reads.

## Current direction — owner, 16 November 2026

The mission is the starting line: many thousands of **active-ready** profiles, reached by the machine alone over the coming months, at no cost. Keep the automatic updates strong, the filtering strict and the monitoring honest. The 14 November spending pause is lifted: the writing engine runs on Google Gemini's free tier only (`pipeline_state/spending_policy.json`); OpenAI stays off; no purchases, subscriptions, billing, paid models or Lovable builds without the owner's explicit yes.

**Owner, 21 November 2026.** The product is not a phone app of profiles that people click through: the destination is BDF as an agent in a full, virtual-reality conversation that draws on the whole library and on the education of how to teach. Until that technology arrives: leading-edge knowledge of dance and of teaching it, kept ready so that all profiles can be activated overnight; an extremely robust app; no payment, trial, sign-in or e-mail capture anywhere. The Lovable credits that expire on 28 November are used through the prepared batches of `LOVABLE_BATCHES.md`. Write to the owner in Hebrew.

## Standing rules

- The destination is BDF (Best Dance Friend): the lifelong personal dance mentor across Atlas, Viral, creation, human dance friendships and future AR. All of V01–V18 in `PRODUCT_VISION.md` stay in force. Never drop Viral or apply tradition-only exclusions to its valid challenges. Atlas and Viral identities stay separate.
- Active-ready is measured by `pipeline/readiness.py` and is not activation. Human review, music rights and platform tests come after it (`ACTIVE_PROFILE_STANDARD.md`, `MUSIC_STRATEGY.md`). Scripts, model scores and translations never prove readiness.
- Preserve evidence, cultural restrictions and uncertainty. Never invent mechanics, origins, counts, rights or popularity. Never loosen a quality gate to publish more. A failed writer never replaces a written profile.
- Work independently within authorization. Involve the owner only when access, a secret, money or an irreducible decision needs him: one simple action, large plain words. Never request secrets in chat. In reports, mark a verified owner-only request **ACTION NEEDED** and necessary awareness **PLEASE NOTE**.
- Content changes belong in this repository. Lovable credits are for one prepared, scoped UI batch the owner approves; saving the instructions mirror there must not trigger a build. No two-way Lovable–GitHub sync, no launch, no promotion.
- For code changes run Python 3.11 compilation and `python -m pipeline.run selftest`. Tests are offline; they do not prove deployment. Never expose credentials.
- Publish through supported authenticated tools or the normal signed-in browser UI, on a branch, then merge. Do not execute scripts that send network calls from inside browser pages.
- After substantive work: update the numbers and the open list in `LEDGER.md`, add a dated entry to `IMPLEMENTATION_LEDGER.md`, keep `pipeline_state/vision_status.json` true for the weekly e-mail, and refresh the Lovable instructions mirror (`LOVABLE_KNOWLEDGE.md`). Do not add new ledger files. Private learner or BDF memory never belongs in this public repository.
- Do not force-send an e-mail to test a layout. The existing Dance Atlas Supabase project is `maojpsywvbksrwkrxmjx`; Sunfeld is a separate project and out of scope.

Continuous research into what profiles still need is a standing requirement (`CONTINUOUS_RESEARCH.md`). A queue or a scheduled task is not completed research; record dated evidence.

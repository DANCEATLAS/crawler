# LEDGER — start here (any AI, any platform)

_Last written 16 November 2026 by Claude. Keep this file under two pages. Read this, `STATUS.md` and `ACTIVE_READY.md`; open the long documents only for the section you need. That is the token rule: the owner pays for every page you read._

## The mission now (owner, 16 November 2026)

Reach the **starting line**: many thousands of **active-ready** profiles, built by the machine alone while the owner is away for months. A profile is active-ready when everything an AI teaching service needs to write the lesson for that dance has been gathered and source-checked (`pipeline/readiness.py`, fifteen items, measured daily, no model calls). After the line come the things a machine cannot grant: human review, music rights, platform tests (`ACTIVE_PROFILE_STANDARD.md`). The long vision is unchanged: BDF, the best dance teacher in the world, a search engine for dance, a social tool that matches dancers, AR (`PRODUCT_VISION.md`, V01–V18).

## State on 16 November 2026 (measured)

- 1,140 dances in the atlas, 345 published deep profiles (+128 in the last week), **1 active-ready**, 16 within two items, 75 within five. What holds pages back most: steps with counts, a studied video, a checked hero video.
- The other AI's 14 November spending pause went live on 16 November and switched the writing engine off. It was lifted the same day on the owner's direction: the engine runs on **Google Gemini's free tier only**. Checked in Google AI Studio: billing tier Free, no billing attached, so it cannot charge. OpenAI is off and its key is not passed to any workflow.
- Free limits seen that day: flash models 20 requests a day each (kept for the writer), flash-lite 500 a day each (judges and video). Budgets are sized to that.
- Proven live the same day in two small test runs: run 33 wrote three profiles (every claim quote-checked, nothing unanswered); run 34 studied two lessons and observed two hero performances. The first full nightly run with the new budgets had not happened when this was written.

## What runs by itself (GitHub Actions, no Claude, no Lovable, $0)

| When (UTC) | Job | Does |
|---|---|---|
| 08:15 daily | `crawl` | hero videos; lessons searched in English and the tradition's own language, retried every 45 days |
| 08:45–08:55 | `push_*` | mirror to Supabase, only rows that changed |
| 09:20 daily | `atlas_daily` | audit → discover (60) → research (40 new + 30 deeper) → QC → hero check (120) → build → video study (24 lessons + 30 performances) → scripts → translate → activation → **readiness** → sync → report |
| every 6 h | `watchdog` | restarts a schedule GitHub dropped |
| Sunday 23:23 | `weekly_report` | the owner's e-mail: active-ready first, engine status, one action at most |
| 1st of month | `monthly_snapshot` | a dated safety copy of everything |

Everything the site shows comes from `public/catalog/` in this repository. Lovable is only the shell.

## Rules that bind

1. **Money.** Free tiers only. No purchases, subscriptions, billing, paid models or Lovable builds without the owner's explicit yes. If billing is ever attached to the Google project, switch `llm_enabled` off first (`pipeline_state/spending_policy.json`).
2. **Truth over volume.** Every claim carries a quote checked against the fetched source, in any script. Never loosen a QC gate to publish more. A model's observation of a video is a candidate, never a verified fact, and a performance never supplies counts.
3. **Respect.** Sacred or restricted dances are never taught: story only. A bare keyword ("ceremony") is not a restriction; it is recorded as ritual context.
4. **Nothing is lost.** A failed or switched-off writer never replaces a written profile. No doubles: one identity, variants inside it. Atlas and Viral stay separate.
5. **No launch.** The site is a private demonstration.
6. **The owner.** Not a developer. Do everything yourself. Ask only for what truly needs him, one simple action, large plain words. Never ask for secrets.
7. **Publish** through the signed-in GitHub web editor (or git when access exists), on a branch, tests green (`python -m pipeline.run selftest`, Python 3.11), then merge. Never run scripts that send network calls from inside a page.

## Where things are

`pipeline/` code · `research_results/`, `qc_results/` profiles and verdicts · `pedagogy/videos/`, `pedagogy/performances/` video study · `pipeline_state/` state (`spending_policy.json`, `active_ready.json`, `runs.json`) · `public/catalog/` what the site reads · `STATUS.md` daily page · `ACTIVE_READY.md` the line · `IMPLEMENTATION_LEDGER.md` dated record of every change · `AI_BRIEF.md` system detail · `PRODUCT_VISION.md` the whole vision.
Platforms: GitHub `DANCEATLAS/crawler` (source of truth) · Lovable project `f79f3666-564d-4799-befe-8b48d1f0a007` (UI and an instructions mirror) · Supabase project `maojpsywvbksrwkrxmjx` (mirror, Viral, accounts) · site `dancingatlas.lovable.app`.

## Open, in order

1. **Watch the first full runs after 16 November.** `STATUS.md` must say "Writing engine: on" and a non-zero number written. If it says OFF, read the research note in `pipeline_state/runs.json`. Google's models answered "high demand" several times in the test: a model now rests five minutes instead of leaving the run, and research stops taking new pages after 180 minutes so the judge, the build and the report always run.
2. **Lessons are the lever.** Active-ready needs steps with counts, and those come from lessons. If the count stalls, improve lesson finding (`crawler.py`, `lesson_eval`) before anything else.
3. **Sacred flags.** About half of the withheld pages are judgment calls by the writer. A second opinion from the QC judge, quoting the source sentence that restricts teaching, is the next refinement.
4. **Database size.** The Supabase audit log held about 541 MB on 11 November (free limit 500 MB). The cause, daily rewrites of unchanged rows, is fixed. The old log still needs the owner's yes to clear, from the Supabase account that owns the project.
5. **Viral chart.** It orders by date, not popularity (`IMPLEMENTATION_LEDGER.md`, Viral findings). Not on the path to the starting line.
6. **Discovery breadth.** Present sources reach roughly 2,500 dances. Thousands more need dances that have no English article: harvest Wikidata items by their other-language articles (`pipeline/discover.py`).
7. **Mirrors.** Lovable Project instructions carry a short copy of this file. The Supabase `ai_context` copy is from 11 November.

## When you finish a session

Update the numbers and the open list above, add a dated entry to `IMPLEMENTATION_LEDGER.md`, keep this file short. Do not create new ledger files.

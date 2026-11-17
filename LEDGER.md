# LEDGER — start here (any AI, any platform)

_Last written 17 November 2026 by Claude. Keep this file under two pages. Read this, `STATUS.md`, `ACTIVE_READY.md` and the first three sections of `BDF_TEACHING_SYSTEM.md`; open the long documents only for the section you need. That is the token rule: the owner pays for every page you read._

## The two missions now (owner, 16 and 17 November 2026)

1. **The starting line.** Many thousands of **active-ready** profiles, built by the machine alone while the owner is away for months. A profile is active-ready when everything an AI teaching service needs to write the lesson for that dance has been gathered and source-checked (`pipeline/readiness.py`, fifteen items, measured daily, no model calls). After the line come the things a machine cannot grant: human review, music rights, platform tests (`ACTIVE_PROFILE_STANDARD.md`).
2. **Teaching research for the Best Dance Friend (BDF).** A standing, endless study of how to teach anyone to dance, the core of BDF's way of teaching (`pipeline/teaching.py`). It finds lessons (for each dance, and for what every dance shares: the beat, groove, balance, confidence), ranks their teachers by learners' praise, watches the best lessons for method and reads their comments, reads the research (a list of topics and an open search of the most cited papers), and joins the three kinds of evidence per teaching practice. `BDF_TEACHING_SYSTEM.md` opens with the summary: where the research stands, the teaching DNA so far, how BDF adjusts to a difficulty.

The long vision is unchanged: BDF, the best dance teacher in the world, a search engine for dance, a social tool that matches dancers, AR (`PRODUCT_VISION.md`, V01–V18).

## State on 17 November 2026 (measured after the first full night)

- 1,155 dances in the atlas, 359 published deep profiles, **5 active-ready** (1 the day before), 26 within two items, 74 within five. What holds pages back most: steps with counts, a studied video, a checked hero video.
- First full night on the free lane (run 35, 16 November, 2 h 44 min, no stage error): 47 profiles written of 70 tried, 50 judged, 120 hero videos checked, 22 lessons studied (91 in all). The wider lesson search took the list from 303 lessons on 164 dances to 427 on 228.
- That night 71 of 312 model questions went unanswered and no performance was observed. One flash-lite model carried most of the work, answered "overloaded" 46 times, and each question that arrived while it rested was dropped; one unreadable video put a strike on six models. Fixed 17 November: a question waits for a resting model (at most 40 minutes a run), rests are short, an unusable answer is the question's fault. Each stage writes `model trouble: …` into `pipeline_state/runs.json`: no log reading needed.
- Engine: **Google Gemini's free tier only** (AI Studio, 16 November: tier Free, no billing attached). OpenAI is off; its key is not passed to any workflow. Free limits seen: flash 20 requests a day per model; only the newest flash-lite model has a large day quota.
- Database jobs, proven live 16 November: 16 rows written where the old jobs wrote 1,191 a day.
- Teaching research, first live run (run 36, 17 November, 6 minutes): 270 teachers ranked from 423 lessons, 3 lessons studied for method with 180 comments read, 3 research notes with 12 checked findings, no question unanswered although the model answered "overloaded" three times.

## What runs by itself (GitHub Actions, no Claude, no Lovable, $0)

| Set for (UTC) | Job | Does |
|---|---|---|
| 08:15 daily | `crawl` | hero videos; lessons searched in English and the tradition's own language, retried every 45 days |
| 08:45–08:55 | `push_*` | mirror to Supabase, only rows that changed |
| 09:20 daily | `atlas_daily` | audit → discover (60) → research (40 new + 30 deeper) → QC → hero check (120) → build → video study (24 lessons + 30 performances) → **teaching research** (3 free searches for basics lessons, 10 lessons watched for method, 3 research topics + 2 papers) → scripts → translate → activation → **readiness** → sync → report |
| every 6 h | `watchdog` | restarts a schedule GitHub dropped |
| Sunday 23:23 | `weekly_report` | the owner's e-mail: active-ready first, engine status, teaching research, one action at most |
| 1st of month | `monthly_snapshot` | a dated safety copy of everything |

GitHub starts these hours late (on 16 November: crawl 18:28, pushes 18:56, nightly 19:40 to 22:24 UTC). The order holds, so nothing depends on the clock. Everything the site shows comes from `public/catalog/` in this repository. Lovable is only the shell.

## Rules that bind

1. **Money.** Free tiers only. No purchases, subscriptions, billing, paid models or Lovable builds without the owner's explicit yes. If billing is ever attached to the Google project, switch `llm_enabled` off first (`pipeline_state/spending_policy.json`).
2. **Truth over volume.** Every claim carries a quote checked against the fetched source, in any script. Never loosen a QC gate to publish more. A model's observation of a video is a candidate, never a verified fact, and a performance never supplies counts.
3. **Respect.** Sacred or restricted dances are never taught: story only. A bare keyword ("ceremony") is not a restriction; it is recorded as ritual context.
4. **Nothing is lost.** A failed or switched-off writer never replaces a written profile, a studied video or a research note. No doubles: one identity, variants inside it. Atlas and Viral stay separate.
5. **Teaching research is evidence, not a verdict.** Teachers are ranked by learners' comments only, never by views. Comments are kept as themes: no names, no quotations. Every observation carries a timestamp; every research finding carries a quote checked against its source. Nothing there has been tested on learners by Dance Atlas.
6. **No launch.** The site is a private demonstration.
7. **The owner.** Not a developer. Do everything yourself. When something truly needs him, prepare it fully in his browser first, then give one simple step in large plain words and wait for his word before the next. Never ask for secrets.
8. **Publish** through the signed-in GitHub web editor (or git when access exists), on a branch, tests green (`python -m pipeline.run selftest`, Python 3.11), then merge. Never run scripts that send network calls from inside a page.

## Where things are

`pipeline/` code · `research_results/`, `qc_results/` profiles and verdicts · `pedagogy/videos/`, `pedagogy/performances/` video study of each dance · `pedagogy/teachers.json`, `pedagogy/foundation_lessons.json`, `pedagogy/methods/`, `pedagogy/science/`, `pedagogy/bdf_system.json` teaching research · `pipeline_state/` state (`spending_policy.json`, `active_ready.json`, `runs.json`) · `public/catalog/` what the site and a teaching service read (`active_ready.json`, `bdf_teaching_system.json`) · `STATUS.md` daily page · `ACTIVE_READY.md` the line · `BDF_TEACHING_SYSTEM.md` how the best classes teach · `IMPLEMENTATION_LEDGER.md` dated record of every change · `AI_BRIEF.md` system detail · `PRODUCT_VISION.md` the whole vision.
Platforms: GitHub `DANCEATLAS/crawler` (source of truth) · Lovable project `f79f3666-564d-4799-befe-8b48d1f0a007` (UI and an instructions mirror) · Supabase project `maojpsywvbksrwkrxmjx` (mirror, Viral, accounts) · site `dancingatlas.lovable.app`.

## Open, in order

1. **Watch the unanswered share** (`llm_unanswered` of `llm_requests` per stage in `runs.json`). It should fall well under the first night's 23 %, and performances should be observed. If `waited_seconds` reaches 2,400 night after night, the free lane is too small for the budgets: lower `HERO_QC_BUDGET` first.
2. **Lessons are the lever.** Active-ready needs steps with counts, and those come from lessons. If the count stalls, improve lesson finding (`crawler.py`, `lesson_eval`) first.
3. **Teaching research, next.** (a) Follow the best-ranked teachers to their other lessons; today a teacher is seen only through lessons found by a search. (b) A person checks a sample of timestamps before the page is used to build BDF. (c) Widening is one line each in `pipeline/teaching.py`: a research topic (`SCIENCE`), a query of the open paper search (`PAPER_QUERIES`), a basics topic or a search phrase in another language (`FOUNDATIONS`), a teaching practice (`PRACTICE`, then add it to a theme).
4. **Sacred flags.** Half of the withheld pages are the writer's judgment calls; a second opinion from the QC judge, quoting the restricting sentence, is the next refinement.
5. **Database size.** The Supabase audit log held about 541 MB on 11 November (free limit 500 MB); writes still worked on 16 November and the cause is fixed. Clearing the old log needs the owner's yes and the Supabase account that owns the project.
6. **Discovery breadth.** Present sources reach roughly 2,500 dances; more need Wikidata items with no English article (`pipeline/discover.py`).
7. **Viral chart** orders by date, not popularity (`IMPLEMENTATION_LEDGER.md`). Not on the path to the starting line.
8. **Mirrors.** Lovable Project instructions hold a short copy of this file from 16 November; the Supabase `ai_context` copy is from 11 November.

## When you finish a session

Update the numbers and the open list above, add a dated entry to `IMPLEMENTATION_LEDGER.md`, keep this file short. Do not create new ledger files.

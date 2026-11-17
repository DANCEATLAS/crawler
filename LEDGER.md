# LEDGER — start here (any AI, any platform)

_Last written 17 November 2026 by Claude. Keep this file under two pages. Read this, `STATUS.md`, `ACTIVE_READY.md` and `BDF_TEACHING_SYSTEM.md` down to the heading "The evidence"; open the long documents only for the section you need. That is the token rule: the owner pays for every page you read._

## The two missions now (owner, 16 and 17 November 2026)

1. **The starting line.** Many thousands of **active-ready** profiles, built by the machine alone while the owner is away for months. A profile is active-ready when everything an AI teaching service needs to write the lesson for that dance has been gathered and source-checked (`pipeline/readiness.py`, fifteen items, measured daily, no model calls). After the line come the things a machine cannot grant: human review, music rights, platform tests (`ACTIVE_PROFILE_STANDARD.md`).
2. **The DNA of the Best Dance Friend (BDF): the mentor.** BDF's core is a mentor with the deepest understanding of how to teach anyone to dance, in practice and in philosophy: dancing as a universal language, rewarding at once, important to the learner, exciting to return to; a lifelong partner who fits each person better the longer they stay. That understanding is built from evidence by a standing, free, growing study (`pipeline/teaching.py`): it finds lessons and teachers' talks, ranks teachers by learners' praise, watches the best for method, then takes a second, narrower look at the mentor alone (what the teacher says at the moments that decide whether a learner stays: the opening, before a hard part, after a mistake, after a success, checking in, the close; what they believe, sorted; how a feeling is met), reads the comments and the research (including the science of mentoring and of adaptive tutors), and joins the three kinds of evidence per teaching practice. Built to be used: `BDF_TEACHING_SYSTEM.md` opens with the summary (the teaching DNA, how BDF adjusts, the mentor, what to remember about each learner); `public/catalog/bdf_teaching_system.json` carries the same as data.

The long vision is unchanged: BDF, the best dance teacher in the world, a search engine for dance, a social tool that matches dancers, AR (`PRODUCT_VISION.md`, V01–V18).

## State on 17 November 2026 (measured)

- Atlas: 1,155 dances, 359 published deep profiles, **5 active-ready** (1 the day before), 26 within two items. What holds pages back most: steps with counts, a studied video, a checked hero video.
- First full night on the free lane (run 35, 16 November, 2 h 44 min): 47 profiles written of 70 tried, 120 hero videos checked, 22 lessons studied; the lesson list grew from 303 to 427. But 71 of 312 model questions went unanswered: one free model carried most of the work and each question that arrived while it rested was dropped. Fixed 17 November: a question waits (at most 40 minutes a run). In the live runs since, nothing went unanswered. Each stage writes `model trouble: …` into `pipeline_state/runs.json`: no log reading needed.
- Engine: **Google Gemini's free tier only** (AI Studio, 16 November: tier Free, no billing attached). OpenAI is off; its key is not passed to any workflow. Seen: flash 20 requests a day per model; only the newest flash-lite model has a large day quota.
- Database jobs: 16 rows written where the old jobs wrote 1,191 a day.
- The mentor's DNA after five live runs on 17 November (runs 36 to 40): 291 teachers ranked, 35 basics lessons and talks found, 14 lessons of 12 teachers studied, 840 comments read, 10 lessons with the mentor look (46 moments, 12 feelings met, beliefs under four headings), 12 research topics and 5 papers with 53 checked findings, 7 practices with two or more kinds of evidence, 2 with all three. The vocabulary: 34 practices in six themes, 6 mentor moments, 4 headings of belief, 66 research topics, 40 open-search queries, 16 basics topics (one of them teachers' talks: searched every night, and one talk is studied first each night when one is waiting).
- The free engine's day is about 400 model calls (16 November, Pacific day: 328 by the night, 84 by five live tests, then the quota was spent). The mentor research therefore runs after the stages that grow the library and takes what is left; when no model can be asked it stops, and no lesson is marked as failed for it.

## What runs by itself (GitHub Actions, no Claude, no Lovable, $0)

| Set for (UTC) | Job | Does |
|---|---|---|
| 08:15 daily | `crawl` | hero videos; lessons searched in English and the tradition's own language, retried every 45 days |
| 08:45–08:55 | `push_*` | mirror to Supabase, only rows that changed |
| 09:20 daily | `atlas_daily` | audit → discover (60) → research (40 new + 30 deeper) → QC → hero check (120) → build → video study (24 lessons + 30 performances) → scripts → translate → activation → **teaching research** (3 free searches for basics lessons and teachers' talks, 10 lessons watched for method, 12 mentor looks, 3 research topics + 2 papers) → **readiness** → sync → report |
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

1. **Watch the unanswered share** (`llm_unanswered` of `llm_requests` per stage in `runs.json`): it should stay far under the first night's 23 %, and performances should be observed. If `waited_seconds` reaches 2,400 night after night, lower `HERO_QC_BUDGET` first.
2. **Lessons are the lever.** Active-ready needs steps with counts, and those come from lessons. If the count stalls, improve lesson finding (`crawler.py`, `lesson_eval`) first.
3. **The mentor's DNA, next.** (a) Whoever builds BDF starts from `public/catalog/bdf_teaching_system.json`: `dna` is the default behaviour, `adjustments` and `mentor.feelings` say what to do when a learner struggles or shows a feeling, `learner_model` is what BDF's memory of a person should hold (vision V04). (b) A person checks a sample of timestamps first. (c) Follow the best-ranked teachers to their other lessons. (d) Widening is one line each in `pipeline/teaching.py`: `SCIENCE`, `PAPER_QUERIES`, `FOUNDATIONS`, `PRACTICE` (then add it to a theme). (e) Every lesson studied gets the mentor look in its teacher's turn (12 a night); a later reading adds to an earlier one and never replaces what was learned about the mentor.
4. **Sacred flags.** Half of the withheld pages are the writer's judgment calls; a second opinion from the QC judge is the next refinement.
5. **Database size.** The Supabase audit log held about 541 MB on 11 November (free limit 500 MB); writes still worked on 17 November. Clearing it needs the owner's yes and the Supabase login that owns the project (the GitHub login is an empty account).
6. **Discovery breadth.** Present sources reach roughly 2,500 dances; more need Wikidata items with no English article (`pipeline/discover.py`).
7. **Viral chart** orders by date, not popularity. Not on the path to the starting line.
8. **Mirrors.** Lovable Project instructions hold a short copy of this file (17 November); the Supabase `ai_context` copy is from 11 November.

## When you finish a session

Update the numbers and the open list above, add a dated entry to `IMPLEMENTATION_LEDGER.md`, keep this file short. Do not create new ledger files.

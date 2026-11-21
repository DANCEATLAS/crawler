# LEDGER — start here (any AI, any platform)

_Last written 21 November 2026 by Claude. Keep this file under two pages. Read this, `STATUS.md`, `ACTIVE_READY.md` and `BDF_TEACHING_SYSTEM.md` down to the heading "The evidence"; open the long documents only for the section you need. That is the token rule: the owner pays for every page you read._

## The two missions now (owner, 16 and 17 November 2026)

1. **The starting line.** Many thousands of **active-ready** profiles, built by the machine alone while the owner is away for months. A profile is active-ready when everything an AI teaching service needs to write the lesson for that dance has been gathered and source-checked (`pipeline/readiness.py`, fifteen items, measured daily, no model calls). After the line come the things a machine cannot grant: human review, music rights, platform tests (`ACTIVE_PROFILE_STANDARD.md`).
2. **The DNA of the Best Dance Friend (BDF): the mentor.** BDF's core is a mentor with the deepest understanding of how to teach anyone to dance, in practice and in philosophy: dancing as a universal language, rewarding at once, important to the learner, exciting to return to; a lifelong partner who fits each person better the longer they stay. That understanding is built from evidence by a standing, free, growing study (`pipeline/teaching.py`): it finds lessons and teachers' talks, ranks teachers by learners' praise, watches the best for method, then takes a second, narrower look at the mentor alone (six moments that decide whether a learner stays, beliefs, feelings met), reads the comments and the research (including the science of mentoring and of adaptive tutors), and joins the three kinds of evidence per teaching practice. Built to be used: `BDF_TEACHING_SYSTEM.md` opens with the summary (the teaching DNA, how BDF adjusts, the mentor, what to remember about each learner); `public/catalog/bdf_teaching_system.json` carries the same as data.

The long vision is unchanged: BDF, the best dance teacher in the world, a search engine for dance, a social tool that matches dancers, AR (`PRODUCT_VISION.md`, V01–V18).

## The owner's direction of 21 November 2026

- **Not a phone app of profiles that people click through** ("people are not going to enjoy learning to dance like that"). The destination is BDF as an agent in a consistent virtual-reality interaction: a full conversation that draws on the whole dance library and on the education of how to teach it; later, augmented reality, shared lessons and a community that dances together.
- **Until that technology arrives:** leading-edge knowledge of dance and of teaching it (the two missions), kept ready so that all profiles can be activated overnight: complete, source-checked and readable by any agent on any platform, with or without a connection (`public/catalog/manifest.json` is the door).
- **No payment.** "The concept of the payment should be completely erased now." No price, trial, membership, referral, sign-in or e-mail capture on the site, and no pricing design until he reopens it. Erased from the site on 21 November.
- **The app: extremely robust.** It is the window where he reads the materials comfortably, the proof that a machine can read the library and, later, a possible beta for a dance and music community. No effort goes into a click-to-learn experience.
- **Platform.** Nothing has to move: the library never lived in Lovable. It is 79 MB of open, versioned files here, small enough for a phone and for an AI without a connection. Lovable is a replaceable window.
- **The mentor's research, widened that day on his words:** the greatest ease and openness to learning, an experience that inspires ("perhaps even spiritual"), learning joined with movement, knowledge and other people, and learners who learn to teach: "once we teach people to teach in the best way, they become better people". New in `pipeline/teaching.py`: the theme **Pass it on**, the practice *a moment of presence*, 14 research topics, 10 open searches, 2 basics topics. The research is endless and must be embedded: a finding becomes a rule only through the nightly fusion of the three kinds of evidence.
- **The 90.9 Lovable credits that expire on 28 November are used in full** (`LOVABLE_BATCHES.md`: the batches, their checks and their cost).
- **Write to the owner in Hebrew**: he reads it faster than English.

## State on 21 November 2026 (measured)

- Atlas: 1,244 dances, 476 published deep profiles, **32 active-ready** (5 on 16 November), 80 more within two items. What holds pages back most: the steps with their counts (279 pages), a studied lesson or performance (207), common mistakes (176).
- Five nights in a row without an error (16 to 20 November). Since the patient model client (17 November) 2 questions of 1,128 went unanswered; a night takes between 2 h 20 min and 3 h 35 min (limit 5 h 10 min). Each stage writes `model trouble: …` into `pipeline_state/runs.json`: no log reading needed.
- **The pace, said plainly:** a night adds about 22 dances to the atlas, 30 published profiles and 5 active-ready profiles. On 21 November 326 lessons and 501 performances were waiting to be studied and the free day had room, so the nightly video study was raised from 24 + 30 to 40 + 50. Thousands of active-ready profiles need more dances with a lesson on the web than are known today (open items 3 and 7).
- Engine: **Google Gemini's free tier only** (AI Studio, 16 November: tier Free, no billing attached). OpenAI is off; its key is not passed to any workflow. The free day has carried 405 answered questions in one night (17 November); a usual night now asks about 240. The mentor research runs after the stages that grow the library and takes what is left; when no model can be asked it stops, and no lesson is marked as failed for it.
- Database: **38 MB of the free 500** since the change log was cleaned on 21 November (627 MB before).
- The mentor's DNA after the night of 20 November: 549 teachers ranked, 51 lessons of 45 teachers studied, every one with the mentor look, 4 of them teachers' talks; 236 moments (the opening 47, before a hard part 84, after a mistake 31, after a success 31, checking in 23, the close 20); 48 feelings met; beliefs of 15 teachers on who can dance and of 19 on how people learn; 2,991 learner comments read; 24 research topics and 9 papers with 106 checked findings; **23 of 34 practices with two or more kinds of evidence, 12 with all three**. The vocabulary since 21 November: 37 practices in seven themes, 6 mentor moments, 4 headings of belief, 80 research topics, 50 open-search queries, 18 basics topics (one of them teachers' talks: searched every night, and one talk is studied first each night when one is waiting).

## What runs by itself (GitHub Actions, no Claude, no Lovable, $0)

| Set for (UTC) | Job | Does |
|---|---|---|
| 08:15 daily | `crawl` | hero videos; lessons searched in English and the tradition's own language, retried every 45 days |
| 08:45–08:55 | `push_*` | mirror to Supabase, only rows that changed |
| 09:20 daily | `atlas_daily` | audit → discover (60) → research (40 new + 30 deeper) → QC → hero check (120) → build → video study (40 lessons + 50 performances) → scripts → translate → activation → **teaching research** (3 free searches for basics lessons and teachers' talks, 10 lessons watched for method, 12 mentor looks, 3 research topics + 2 papers) → **readiness** → **door** (manifest, index, one file per dance, machine page; no model calls) → sync → report |
| every 6 h | `watchdog` | restarts a schedule GitHub dropped |
| Sunday 23:23 | `weekly_report` | the owner's e-mail: active-ready first, engine status, teaching research, one action at most |
| 1st of month | `monthly_snapshot` | a dated safety copy of everything |

GitHub starts these hours late (on 16 November: crawl 18:28, pushes 18:56, nightly 19:40 to 22:24 UTC). The order holds, so nothing depends on the clock. Everything the site shows comes from `public/catalog/` in this repository. Lovable is only the shell.

## Rules that bind

1. **Money.** Free tiers only. No purchases, subscriptions, billing, paid models or Lovable builds without the owner's explicit yes. On 21 November he ordered the expiring Lovable credits used through the prepared batches of `LOVABLE_BATCHES.md`; nothing else is built there. If billing is ever attached to the Google project, switch `llm_enabled` off first (`pipeline_state/spending_policy.json`).
2. **Truth over volume.** Every claim carries a quote checked against the fetched source, in any script. Never loosen a QC gate to publish more. A model's observation of a video is a candidate, never a verified fact, and a performance never supplies counts.
3. **Respect.** Sacred or restricted dances are never taught: story only. A bare keyword ("ceremony") is not a restriction; it is recorded as ritual context.
4. **Nothing is lost.** A failed or switched-off writer never replaces a written profile, a studied video or a research note. No doubles: one identity, variants inside it. Atlas and Viral stay separate.
5. **Teaching research is evidence, not a verdict.** Teachers are ranked by learners' comments only, never by views. Comments are kept as themes: no names, no quotations. Every observation carries a timestamp; every research finding carries a quote checked against its source. Nothing there has been tested on learners by Dance Atlas.
6. **No launch, no payment.** The site is a private demonstration: no price, trial, sign-in or e-mail capture.
7. **The owner.** Not a developer. Do everything yourself. When something truly needs him, prepare it fully in his browser first, then give one simple step in large plain words, in Hebrew, and wait for his word before the next. Never ask for secrets.
8. **Publish** through the signed-in GitHub web editor (or git when access exists), on a branch, tests green (`python -m pipeline.run selftest`, Python 3.11), then merge. Never run scripts that send network calls from inside a page.

## Where things are

`pipeline/` code · `research_results/`, `qc_results/` profiles and verdicts · `pedagogy/videos/`, `pedagogy/performances/` video study of each dance · `pedagogy/teachers.json`, `pedagogy/foundation_lessons.json`, `pedagogy/methods/`, `pedagogy/science/`, `pedagogy/bdf_system.json` teaching research · `pipeline_state/` state (`spending_policy.json`, `active_ready.json`, `runs.json`) · `public/catalog/` the door, what the site and any agent read (`manifest.json` first; `index.json`; `d/<slug>.json`, one complete file per dance; `bdf_teaching_system.json`; `active_ready.json`; `machine.json`; `site.json`, the words of the newer screens) · `LOVABLE_BATCHES.md` the website batches and what each cost · `STATUS.md` daily page · `ACTIVE_READY.md` the line · `BDF_TEACHING_SYSTEM.md` how the best classes teach · `IMPLEMENTATION_LEDGER.md` dated record of every change · `AI_BRIEF.md` system detail · `PRODUCT_VISION.md` the whole vision.
Platforms: GitHub `DANCEATLAS/crawler` (source of truth) · Lovable project `f79f3666-564d-4799-befe-8b48d1f0a007` (UI and an instructions mirror) · Supabase project `maojpsywvbksrwkrxmjx` (mirror, Viral, accounts) · site `dancingatlas.lovable.app`.

## Open, in order

1. **The door for an agent, and a robust window** (owner, 21 November). (a) Machine side, free, live since 21 November (`pipeline/door.py`, stage `door`): `manifest.json`, `index.json` (0.6 MB against the 5.2 MB list), one file per dance that changes only when the dance does, `machine.json`; sacred dances carry no teaching material there. Still to add: the Viral list (`viral.json`), families for the 774 dances that have none. (b) Lovable, with the expiring credits (`LOVABLE_BATCHES.md`: order, checks, the cost of each batch). Published on 21 November: payment and accounts erased; the mentor page (`/mentor`); loading through the door with the last good copy in the browser's database and `/health`. Next: the whole profile on the dance page, the starting line, the machine room in Hebrew, the direction page, truth repairs, speed and access.
2. **Watch the unanswered share** (`llm_unanswered` of `llm_requests` per stage in `runs.json`): it should stay far under the first night's 23 %, and performances should be observed. If `waited_seconds` reaches 2,400 night after night, lower `HERO_QC_BUDGET` first.
3. **Lessons are the lever.** Active-ready needs steps with counts, and those come from lessons. The nightly video study was raised on 21 November; watch whether active-ready grows faster than 5 a night. If the count stalls, improve lesson finding (`crawler.py`, `lesson_eval`) first.
4. **The mentor's DNA, next.** (a) Whoever builds BDF starts from `public/catalog/bdf_teaching_system.json`: `dna` is the default behaviour, `adjustments` and `mentor.feelings` say what to do when a learner struggles or shows a feeling, `learner_model` is what BDF's memory of a person should hold (vision V04). (b) A person checks a sample of timestamps first. (c) Follow the best-ranked teachers to their other lessons. (d) Widening is one line each in `pipeline/teaching.py`: `SCIENCE`, `PAPER_QUERIES`, `FOUNDATIONS`, `PRACTICE` (then add it to a theme). (e) Every lesson studied gets the mentor look in its teacher's turn (12 a night); a later reading adds to an earlier one and never replaces what was learned about the mentor.
5. **Sacred flags.** Half of the withheld pages are the writer's judgment calls; a second opinion from the QC judge is the next refinement. The door follows the readiness measure; 85 dances the writer found teachable are still flagged by keyword in the catalogue, which hides their lesson links on the site.
6. **Database size.** Done on 21 November: 38 MB of 500. Look at `audit_log` again only if the nightly jobs start rewriting unchanged rows (they wrote about 1,000 such rows a night before 16 November, about 7 since). The Supabase project belongs to the owner's e-mail sign-in; the GitHub sign-in opens an empty account.
7. **Discovery breadth.** Present sources reach roughly 2,500 dances; more need Wikidata items with no English article (`pipeline/discover.py`).
8. **Viral chart** orders by date, not popularity. Not on the path to the starting line.
9. **Mirrors.** Lovable Project instructions hold a short copy of this file (21 November); the Supabase `ai_context` copy is from 21 November. The weekly e-mail is still written in English.
10. **Repository size.** The files are 79 MB, but the history grows about 3 MB a night; GitHub recommends staying under 1 GB, some ten months away. When it nears: compact the history (the monthly safety copies keep the past) or keep generated files on a branch of their own. No move is needed.

## When you finish a session

Update the numbers and the open list above, add a dated entry to `IMPLEMENTATION_LEDGER.md`, keep this file short. Do not create new ledger files.

# THE STANDARD — what "finished" means for a Dance Atlas profile

**Superseded destination, 11 November 2026:** Active Profile is the current goal. Read ACTIVE_PROFILE_STANDARD.md and PRODUCT_VISION.md. The historical movie/script metrics below remain for compatibility and useful presentation assets; they do not establish interactive readiness.

*The aim is the best dance atlas ever made: every tradition researched to the depth a film crew and a teacher need, true to its
sources, respectful of its culture, no doubles. This file defines the ladder every page climbs and the top rung, **film-grade ★**,
which is meant to be nearly impossible. `pipeline/weekly_report.py` measures all of it every Monday; the code is the authority
for the numbers, this file is the authority for the intent. Change them together.*

## The ladder

The owner's current release standard is `PRODUCT_VISION.md`. The ladder below measures research and structural preparation only. It does not certify instructional correctness, cultural approval, asset rights, native-language review or learning outcomes. Those require separate recorded validation before product release. Quote occurrence is distinct from claim support and complete sentence coverage; the current claim verifier does not prove all three.

| Level | Name | What it means | Who moves a page up |
|---|---|---|---|
| 0 | **Listed** | The dance is in the atlas: name, country, region, a hero video when one was found. | the discovery stage, the video crawlers |
| 1 | **Researched** | A deep profile was written from fetched sources (Wikipedia in up to four languages, Wikidata, UNESCO, digitised books, editor-added sources) with every claim carrying a verbatim quote. | the daily research stage |
| 2 | **Published** | Passed every QC gate (sources, verified quotes, country, no AI tells, no banned phrasing, not a double, sacred handled) and the model judge (accuracy, respect, specificity, teaching value, safe adaptations). Only published pages reach the website. | the daily QC stage |
| 3 | **Movie-ready** | Music DNA (what it sounds like, instruments or rhythm pattern) + movement DNA (footwork with posture, arms or signature moves) + an episode brief (five story beats, a lesson ladder) — all from sources. | the deepening pass (it re-researches the thinnest pages first) |
| 4 | **Class-complete** | All 18 things a fun, teachable class needs (`class_checklist`: footwork with counts, posture, arms, formation, tempo or meter, instruments, sound, signature moves, lesson ladder, story beats, hooks, costume, occasions, notable figures, recordings, 3 licensed images, connections, footage). | the deepening pass, the crawlers, the editor's extra sources |
| 5 | **Film-grade ★** | Every item below. Nothing is waived. | the whole machine plus the weekly editor |

## Film-grade ★ — every item, no exceptions

**Story** — all eight sections carry real text from sources (never the placeholder "not described in sources"): origins & history, how it is danced, music & instruments, costume & setting, occasions & meaning, notable figures, regional variants, lineage.

**Teaching** — basic steps written out as an ordered list (3 or more); a lesson ladder with three levels; what to avoid / safety notes.

**Music DNA** — tempo **and** meter (not one or the other); the rhythm pattern; the instruments; the sound described; at least one recording verified in MusicBrainz.

**Movement DNA** — footwork with counts; posture; arms & hands; formation & space; signature moves.

**Episode** — hook & insight; five or more story beats; an instructor persona; a music cue.

**Media** — a hero video that passed the vision check (public, embeddable, HD, the dance is visible, it is not a music video); three or more licensed images; at least one tutorial video; at least one licensed reference footage link (Wikimedia Commons or the Internet Archive).

**Context** — tradition status known (living, revived or historical — not "unknown"); seniors and children versions present with real content (or withheld on purpose because the dance is sacred or restricted); two or more typed connections to other dances.

**Accuracy** — eight or more claims and every one of them verified against its quoted source; three or more sources including at least one book, archive or scholarly source (a digitised book, a UNESCO inscription, or an editor-added source of tier `scholarly` or `archive`).

**Editorial** — no open editor note; not a suspected double (the QC duplicate check is clear or an editor decided `keep`); **read and approved by the editor** (`pipeline_state/editor_approvals.json`, see below) *after* the page's latest research — a page re-researched later must be read again.

**Judge** — score ≥ 9.5 under the current judge version.

Why it is nearly impossible on purpose: a page only gets there when the sources are rich, the crawlers found the right videos, the images are licensed, the music is in MusicBrainz and a reader has sat with it. That is a strong research-preparation target; production and teaching still require the separate evidence, practitioner, rights and learner validation in `PRODUCT_VISION.md`. Counting them honestly is the point; a small number that is true beats a large number that is not.

## Editor approval

The weekly editor pass (`WEEKLY_PASS.md`, step 1) reads the week's new pages. A page it finds true (two claims spot-checked), respectful, concrete and teachable is approved:

```
pipeline_state/editor_approvals.json
{"<slug>": {"at": "YYYY-MM-DD", "by": "weekly pass", "note": "one line: what was checked"}}
```

The approval counts only for the text the editor read: if the daily run re-researches the page afterwards, the approval lapses until the next read. An approval never overrides a QC gate — a page that fails QC is not published whatever the editor wrote.

## What the standard refuses

- Text written by hand into the JSON (it would carry no verified quotes). Fix a page with an editor note or an extra source and let the machine re-research it.
- Loosening a QC gate to publish more. Fewer true pages beat more doubtful ones.
- Teaching material for a sacred or restricted dance. Those pages can be published and movie-ready for their story and music; the teaching and the adaptations stay withheld.
- Doubles. Two entries for one tradition are merged (`audit_overrides.json`: `merge:<slug>`), variants become sections, not pages.
- In the Atlas tradition catalogue, moves, songs, festivals, companies and people are not automatically traditions. This exclusion does not apply blindly to Viral challenges/trends; use the separate taxonomy and relationships in `PRODUCT_VISION.md`.

## The script layer

Packs carry `release_status: not_validated`; music briefs carry `rights_status: not_assessed`. These are deliberately separate from structural `status: complete`. Explicit footwork counts are required by the checklist; 'step' or 'beat' alone does not qualify. Its recordings check uses verified album records, not unverified recommendations. These checks remain conservative proxies and do not replace practitioner review.

Every published page also gets an episode pack (`episodes/<slug>.json`, `MOVIE_PHASE.md`): Episode 1 and three chapters written from the profile only. A pack is **complete** when it has no gaps — the same items as film-grade's media, music and movement lines plus teaching steps and what to avoid. Packs do not change a page's level; the weekly report counts them separately (packs, complete, polished), and their gaps feed the research queue.

## Where the numbers come from

`WEEKLY_REPORT.md` (and `reports/weekly/<date>.md`) lists, for every level and every item above, how many published pages have it now and how that changed over the last week, the last four weeks and since the start of the year. The "Closest to film-grade" table names the pages a few items short and what each still lacks, so the editor pass and the deepening pass know where to push. `STATUS.md` has the daily view; `QC_REPORT.md` the review queue.

# Dancing Atlas content pipeline (v3)

The pipeline turns this repository into a self-running system that **grows** the catalogue,
**deepens** every profile over time and **gates** everything behind quality control before
the website shows it. It runs every morning in GitHub Actions right after the crawlers.

```
08:15  crawl            hero videos / tutorials / viral renditions from YouTube          (existing)
08:45  push_videos      heroes → Supabase                                              (existing)
08:50  push_tutorials   tutorials → Supabase                                           (existing)
08:55  push_viral       viral renditions → Supabase                                    (existing)
09:20  atlas_daily      bootstrap → discover → research → qc → hero_qc → build → sync → report   (new)
```

## What the daily run does

| stage | what it does | budget (workflow input / env) |
|---|---|---|
| bootstrap | downloads the website's current dataset (`app_catalog.json`) if it is missing | — |
| discover | finds dances the Atlas does not have: Wikidata (every item that is a kind of dance with an English article), Wikipedia "Dances by country" categories and list pages, UNESCO ICH titles; de-duplicates by slug, name, alias, Wikidata id and fuzzy name; queues candidates in `pipeline_state/candidates.json` | `DISCOVER_MAX_NEW=40` |
| research | for N new candidates + N thinnest existing profiles: fetches Wikipedia (English + up to two other languages), Wikidata facts, UNESCO inscription, licensed Wikimedia Commons images; the model writes a structured profile (history, how it is danced, music, costume, occasions, figures, variants, lineage, teaching steps, albums) and must attach a verbatim quote to every claim; quotes are verified mechanically against the fetched text; albums are kept only if they resolve in MusicBrainz | `RESEARCH_NEW=15`, `RESEARCH_ENRICH=15` |
| qc | deterministic gates (schema, lengths, concrete insight, ≥6 claims with ≥75 % verified, ≥2 sources, country/region taxonomy, banned filler phrasing, AI tells, repetition, duplicates vs catalogue, sacred handling) + an independent model judge (accuracy, respect, specificity, teaching value) → `publish` / `review` / `reject` | — |
| hero_qc | every hero video within budget: still public and embeddable, HD, sane duration, not a music video/movie/lyric clip, title names the dance, and a vision check of the actual frame (people dancing, not a talking head / poster / vertical phone clip, camera steady). Failing heroes are blocklisted for the crawler and replaced by the best passing challenger; dead ones are removed and re-crawled | `HERO_QC_BUDGET=60` |
| build | publishes `public/catalog/` — exactly what the website loads: `dances.app.json` (dw_app_v1 contract + new fields), `profiles_v2.json` (rich sections, teaching, verified claims, albums, images), `stats.json`, `retired.json`; refuses to publish if the catalogue would shrink by >10 %; regenerates `dance_list.json` (the crawler's work list, including new dances and heroes to re-crawl) so the crawler picks them up the next morning | `INCLUDE_REVIEW=false` |
| sync | mirrors researched/QC'd material into Supabase (`dances` + aliases/sources/edges); only columns that exist are written (`pipeline/sql/001_pipeline_columns.sql` adds the rest) | — |
| report | `STATUS.md` (coverage, counts, last runs, errors) and `QC_REPORT.md` (everything in review/reject and why, possible duplicates) | — |

## Editorial standard enforced by QC
* Only what the sources support; every claim carries a verbatim quote that is checked.
* Concrete over abstract: the insight is one hook (a person, a place, a year, an object); filler
  ("foundational", "rich heritage", "arguably") is counted and blocks auto-publish.
* Cultures are described with respect and precision; sacred or restricted dances are flagged
  (`is_sacred`, `needs_eyes_on`), carry a cultural-context note and get no tutorials.
* Duplicates are caught before insertion (exact, alias and fuzzy name match, Wikidata id).
* A profile that passes everything is published automatically; anything uncertain goes to
  `QC_REPORT.md` for a human.

## Where to look
* `STATUS.md` — one page: catalogue size, hero coverage, research/QC counts, last runs, errors
* `QC_REPORT.md` — the review queue
* `public/catalog/` — what the website loads (`https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/dances.app.json`)
* `research_results/<slug>.json`, `qc_results/<slug>.json` — full evidence and verdicts per dance
* `pipeline_state/` — candidate queue, indexes, hero QC verdicts, run history

## Running by hand
Actions → **atlas_daily** → Run workflow: choose a stage (`daily`, `discover`, `research`, `qc`,
`hero_qc`, `build`, `sync`, `report`, `selftest`), budgets, and optionally `only=slug,slug`.
Locally: `python -m pipeline.run selftest` (offline), `python -m pipeline.run <stage>` with the
environment variables `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `YT_API_KEYS`.

## Why the records are richer than the site needs today
Every profile is written so it can later drive generated episodes (history → narration,
teaching steps → lessons by level, verified albums → soundtrack research, licensed images →
visuals) and, further out, movement teaching. The data model is the product; the website is
its first reader.

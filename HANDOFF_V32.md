# DANCING ATLAS — HANDOFF V32 (26 Oct 2026)
*(delta on V31: the content pipeline v3 — growth, depth and quality control as a daily, self-running system; the website now reads the published catalogue.)*

## What changed
- **Pipeline v3** lives in `pipeline/` and runs daily as the `atlas_daily` workflow (09:20 UTC, after the crawlers). See `PIPELINE.md` for every stage and budget.
- **The website reads the published catalogue** (`public/catalog/dances.app.json` on raw GitHub) with the bundled file as fallback, hides retired slugs, and shows the new sections (story, how it is danced, learn the basics, essential recordings, gallery, sources) for dances whose research passed QC. Lovable change applied 26 Oct; not yet published to dancingatlas.lovable.app (owner's call).
- **Catalogue audit** retires non-dances and merges doubles (deterministic rules + model judge). On the 622-dance research file alone the rules found 13 non-dances (e.g. "Brazil", "Dancing Brasil", "Haiti") and ~50 doubles (e.g. candombe-uruguay/candombe, rumba/cuban-rumba, tap-dance/tap-dance-usa). Decisions: `pipeline_state/audit.json`; manual overrides: `audit_overrides.json` (`{slug: "keep"|"retire"}`).
- **Hero QC** (T8 from V31) is built: metadata gates + a vision check of the frame; failures are blocklisted (`hero_blocklist.json`, respected by `crawler.py`) and replaced by the best challenger or re-crawled.
- **Research is grounded and verified**: every claim carries a verbatim quote that is checked against the fetched source text; albums are kept only when MusicBrainz confirms them; images only with free licences and attribution.
- **Reports**: `STATUS.md` (one page) and `QC_REPORT.md` (review queue, audit decisions, possible duplicates) are rewritten every run.

## Daily flow (UTC)
```
08:15 crawl → 08:45 push_videos → 08:50 push_tutorials → 08:55 push_viral → 09:20 atlas_daily
atlas_daily: bootstrap → audit → discover → research → qc → hero_qc → build → sync → report → commit
```
Budgets per day (workflow inputs): research 15 new + 15 deepened, hero QC 60 videos, discovery 40 candidates, audit 300 judged.
At that pace the whole catalogue is audited in ~4 days, every hero is checked in ~17 days, and every existing profile is deepened once in ~70 days while new dances arrive continuously.

## Supabase
- `seed_catalog` workflow: fill-only seed of all 1,014 app dances into `dances` (never overwrites values already there).
- `pipeline/sql/001_pipeline_columns.sql`: optional migration adding `profile_long`, `research`, `albums`, `images`, `qc`, `hero_qc`, … plus a `dances_public` view. Until it is run, `sync` writes only the columns that exist.
- `schema_dump` workflow prints tables/columns/counts to the run log (no secrets).

## Open items / next
1. Run `atlas_daily` once with small budgets and read the log (first run proves the keys, models and APIs).
2. Review `QC_REPORT.md` after the first audit pass; add overrides where the audit is wrong.
3. Publish the Lovable app when ready (Publish button) — the catalogue URL will then feed it daily.
4. Optional: run the SQL migration so Supabase carries the deep profiles too.
5. Future (the vision): the per-dance `research` record (sections, teaching steps, verified albums, licensed images, claims with sources) is the input for generated episodes and, later, movement teaching. Next step for that road: a per-dance `episode_brief` (narration beats drawn from the sections) and step-level movement notation in `teaching`.

— end V32 —

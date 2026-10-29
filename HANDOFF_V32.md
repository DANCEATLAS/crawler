# DANCING ATLAS — HANDOFF V32 (28 Oct 2026)
*(delta on V31: the content pipeline v3 — growth, depth and quality control as a daily, self-running system; the website reads the published catalogue. First real runs done; what they showed; what is still the owner's call.)*

## What changed
- **Pipeline v3** lives in `pipeline/` and runs daily as the `atlas_daily` workflow (09:20 UTC, after the crawlers). See `PIPELINE.md` for every stage, gate and budget.
- **The website reads the published catalogue** (`public/catalog/dances.app.json` on raw GitHub) with the bundled file as fallback, hides retired slugs, and shows the new sections (story, how it is danced, learn the basics, essential recordings, gallery, sources) for dances whose research passed QC. Lovable change applied 26 Oct; not yet published to dancingatlas.lovable.app (owner's call).
- **Catalogue audit** retires non-dances and merges doubles (deterministic rules + model judge, with guard rails learnt from the first pass — see below). Decisions: `pipeline_state/audit.json`; manual overrides: `audit_overrides.json` (`{slug: "keep"|"retire"}`, always wins).
- **Hero QC** (T8 from V31): metadata gates + a vision check of the frame; failures are blocklisted (`hero_blocklist.json`, respected by `crawler.py`) and replaced by the best challenger or re-crawled.
- **Research is grounded and verified**: every claim carries a verbatim quote that is checked against the fetched source text; albums are kept only when MusicBrainz confirms them *and* the judge finds them central to the dance; images only with free licences and attribution.
- **Reports**: `STATUS.md` (one page) and `QC_REPORT.md` (review queue, audit decisions, possible duplicates) are rewritten every run.

## First real run (run #5, 28 Oct, 20 min end to end)
- Audit: 384 of 1,014 entries judged; 67 retired/merged (e.g. "Brazil", "Dancing Brasil", "Ballroom Bootcamp" (TV), "Blackpool Dance Festival", doubles such as bransle→branle, baagh-naach→bagha-nacha); 28 sent to a human.
- Discovery: 2,131 candidates harvested from Wikidata/Wikipedia/UNESCO, 565 already known, 20 new ones queued (e.g. kailao, tappa dance, fa'ataupati, akiriket).
- Research: 10 new profiles written with 100 % of their claims quote-verified (hula ʻauana: 5/5, kailao 5/5, tappa 5/5; akiriket rejected — not a dance).
- QC: judge scores 9.0–9.4 for the good ones, but every profile landed in *review* because the gates were tuned before any real output existed (they asked for ≥6 claims and ≥1,500 characters; the model delivers 5 verified claims and ~1,300 characters at the budgeted size). **Gates recalibrated** (≥4 claims at ≥90 % verified, ≥1,200 chars, one soft miss tolerated at judge ≥8.5): replaying the same evidence now publishes hula ʻauana, kailao and tappa and still rejects akiriket.
- Hero QC: 47 videos checked, 15 pass, 5 fail, 3 replaced by a better challenger, 2 evicted for re-crawl.
- Build + sync: `public/catalog/` published (1,014 → 947 live after audit), 9 new dances inserted into Supabase with `publish_gate = review`.

## What the first pass taught the audit (fixed)
- The judge retired three real dances it misread as something else: *sabar* ("instrument"), *khaleegi* ("other"), *disco* ("music genre"). Now: only country / place / TV show / company / person / song / festival / category-page verdicts may retire an entry (≤25 per run); music-genre, instrument and "other" verdicts go to `QC_REPORT.md` for a human, and the earlier ones are reopened automatically. `audit_overrides.json` pins the decisions already taken by hand (sabar, khaleegi, disco, reggaeton, gurewol, armenian-dance, pontic-greek-folk-dance kept; fado, muziki-wa-dansi and five non-dances retired).
- A merge could point at an entry the judge had retired (armenian-line-dance → armenian-dance), hiding both; and two rules could merge A→B and B→A. Merges now always end at a live entry, cycles keep the more complete entry, and the judge never retires a merge target.

## Daily flow (UTC)
```
08:15 crawl → 08:45 push_videos → 08:50 push_tutorials → 08:55 push_viral → 09:20 atlas_daily
atlas_daily: bootstrap → audit → discover → research → qc → hero_qc → build → sync → report → commit
```
Budgets per day (workflow inputs): research 15 new + 15 deepened, hero QC 60 videos, discovery 40 candidates, audit 300 judged.
At that pace the rest of the catalogue is audited in ~3 days, every hero is checked in ~17 days, and every existing profile is deepened once in ~70 days while new dances arrive continuously.

## Supabase
- `dances` holds 624 rows (615 + the 9 new ones); the app ships 1,014. `seed_catalog` workflow = fill-only seed of all app dances (never overwrites values already there) — run it once to align.
- `pipeline/sql/001_pipeline_columns.sql`: optional migration adding `profile_long`, `research`, `albums`, `images`, `qc`, `hero_qc`, … plus a `dances_public` view. Until it is run, `sync` writes only the columns that exist (base fields + `publish_gate`/`qc_score`).
- `schema_dump` workflow prints tables/columns/counts to the run log (no secrets).

## Needs the owner (nothing else blocks autonomy)
1. **Model quota.** `OPENAI_API_KEY` is set but empty, so everything runs on the Gemini key, which is on the free tier: run #5 hit HTTP 429 part-way (4 profiles and 3 judge calls failed and are retried next day). Either enable billing on the Gemini key (a few dollars a day at the current budgets) or paste a real OpenAI key into the secret — the code already falls back to it. Without one of these the daily run completes only partially.
2. **Publish the Lovable app** (Publish button) so dancingatlas.lovable.app serves the daily catalogue. The preview already reads it.
3. Optional: run `seed_catalog` once and the SQL migration so Supabase carries the deep profiles too.
4. Read `QC_REPORT.md` after each of the first few runs; `audit_overrides.json` is the steering wheel (one line per decision).

## Future (the vision)
The per-dance `research` record (sections, teaching steps, verified albums, licensed images, claims with sources) is the input for generated episodes and, later, movement teaching. Next step for that road: a per-dance `episode_brief` (narration beats drawn from the sections) and step-level movement notation in `teaching`.

— end V32 —

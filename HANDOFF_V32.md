# DANCING ATLAS — HANDOFF V32 (29 Oct 2026)
**Any AI continuing this work: read `AI_BRIEF.md` first — the vision, the rules, the system map and how to operate without the owner.**

*(delta on V31: the content pipeline v3 — growth, depth and quality control as a daily, self-running system; the website reads the published catalogue. First real runs done; what they showed; what is still the owner's call.)*

## What changed
- **Pipeline v3** lives in `pipeline/` and runs daily as the `atlas_daily` workflow (09:20 UTC, after the crawlers). See `PIPELINE.md` for every stage, gate and budget.
- **The website reads the published catalogue** (`public/catalog/dances.app.json` on raw GitHub) with the bundled file as fallback, hides retired slugs, and shows the new sections (story, how it is danced, learn the basics, essential recordings, gallery, sources) for dances whose research passed QC. Lovable change applied 26 Oct; **published to https://dancingatlas.lovable.app on 29 Oct** (first publish of the site). Daily updates never go through Lovable, so they cost no Lovable credits.
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

## Runs #6–#8 (28–29 Oct) and what they fixed
- #6 (first scheduled run; GitHub fired the 09:20 UTC cron almost seven hours late — that happens, the run is idempotent so it does not matter): 22 more profiles researched, but still 0 published under the old gates and 33 of 55 model calls lost to free-tier 429s.
- #7 (recalibrated gates, v3.1): **17 profiles published** (hula ʻauana 10.0, zonaradiko, kailao, jatjatin, mbende-jerusarema, marchas populares, al-razfa, veerabhadra, kapa haka, luddi, taualuga, xibelani, country swing, bruckins, fa'ataupati, matachines, the Freddie), 8 review, 8 reject (raffaella, hotty-toddy, akiriket … not dances). `public/catalog/profiles_v2.json` carries their sections, teaching steps, verified claims and licensed images; the preview site shows "Catalogue updated".
- Fixed after #6/#7: free-tier 429s are now read by quota type (per-minute → wait once and retry the same model; per-day → retire that model for the run, the next one has its own quota); a hero that passed without the vision check is re-queued instead of counting as checked for 120 days; a QC pass while the judge is unavailable reuses the earlier judge reading of the same research instead of carrying an old verdict; the judge's flag fields (harm, duplicate, insight, album doubt) were nested under "flags" by the model and silently ignored — flattened on read, rubric demands a flat object, every record re-judged (v3.2).
- #8 (v3.2): all 34 researched records re-decided with the flags honoured — **20 published**, 6 review, 8 rejected; Elvis's *Blue Hawaii* dropped from hula ʻauana by the album check. Catalogue live at 941 dances, 20 with deep profiles. Still open: the research composer's pro-model quota — fixed right after (#8) by letting strong calls fall through to flash models.
- #9 (29 Oct, first run with the OpenAI key): every Gemini quota was already spent by the day's runs, so OpenAI carried the whole run (`openai models available: 134; fast gpt-5.4-mini, strong gpt-5-mini`): 9 of 10 research targets written, all 10 judged, hero vision checks back (2 heroes replaced, 2 sent to re-crawl). 3 more profiles published (passinho do Jamal 10.0, kaze no bon, baalan dance) → 942 dances live, 23 with deep profiles. Audit: 962 of 1,014 judged.

## What the first pass taught the audit (fixed)
- The judge retired three real dances it misread as something else: *sabar* ("instrument"), *khaleegi* ("other"), *disco* ("music genre"). Now: only country / place / TV show / company / person / song / festival / category-page verdicts may retire an entry (≤25 per run); music-genre, instrument and "other" verdicts go to `QC_REPORT.md` for a human, and the earlier ones are reopened automatically. `audit_overrides.json` pins the decisions already taken by hand (sabar, khaleegi, disco, reggaeton, gurewol, armenian-dance, pontic-greek-folk-dance kept; fado, muziki-wa-dansi and five non-dances retired).
- A merge could point at an entry the judge had retired (armenian-line-dance → armenian-dance), hiding both; and two rules could merge A→B and B→A. Merges now always end at a live entry, cycles keep the more complete entry, and the judge never retires a merge target.

## Daily flow (UTC)
```
08:15 crawl → 08:45 push_videos → 08:50 push_tutorials → 08:55 push_viral → 09:20 atlas_daily
atlas_daily: bootstrap → audit → discover → research → qc → hero_qc → build → sync → report → commit
```
Budgets per day (workflow inputs): research 15 new + 15 deepened, hero QC 60 videos, discovery 40 candidates, audit 150 judged.
At that pace the rest of the catalogue is audited in ~2 days, every hero is checked in ~17 days, and every existing profile is deepened once in ~70 days while new dances arrive continuously.

## Supabase
- `dances` holds 624 rows (615 + the 9 new ones); the app ships 1,014. `seed_catalog` workflow = fill-only seed of all app dances (never overwrites values already there) — run it once to align.
- `pipeline/sql/001_pipeline_columns.sql`: optional migration adding `profile_long`, `research`, `albums`, `images`, `qc`, `hero_qc`, … plus a `dances_public` view. Until it is run, `sync` writes only the columns that exist (base fields + `publish_gate`/`qc_score`).
- `schema_dump` workflow prints tables/columns/counts to the run log (no secrets).

## Owner items — state on 29 Oct
1. **Model quota — done, no monthly bill.** Gemini stays on the free tier; the `OPENAI_API_KEY` secret now holds a key on a prepaid OpenAI balance (about $5, auto-recharge off). OpenAI is used only when Gemini is out of quota, mini models only (`OPENAI_STRONG_MODELS`). Worst case (Gemini fully out, every call on OpenAI) is roughly $0.50 a day; a normal day is a fraction of that. When the balance is gone nothing breaks — the run logs `insufficient_quota`, retires OpenAI for the run and continues on Gemini alone (slower growth). Top-ups are the owner's call.
2. **Site published — done** (29 Oct). The public site reads the daily catalogue.
3. Optional: run `seed_catalog` once and the SQL migration so Supabase carries the deep profiles too.
4. `QC_REPORT.md` is the review queue; `audit_overrides.json` is the steering wheel (one line per decision). The owner asked to be involved only when something cannot be done without him.

## 30 Oct — the mission, as the owner stated it
Data-building, in perpetuity: keep finding dances everywhere (and keep finding *more* about the ones we have), filter harshly (no doubles, no junk), research each to movie-ready depth, connect them, store everything free on GitHub so nothing is lost whatever happens to credits, never spend Lovable credits, and have the whole library ready to hand to an AI video/music generator the day the owner decides — no video work now, no launch (the site is reachable to show the vision; that is not a launch).
Built for it on 30 Oct: research schema v4 (music DNA, movement DNA, episode brief, connections, class checklist), digitised books as a source, three extra-language articles, gaps carried into the next pass, merge overrides, 25 new dances a day, the 45 audit doubts decided by hand (overrides).
Open dials (asked, awaiting answers): variants as separate pages or sections; teaching steps for sacred dances; breadth vs depth split.

— end V32 —

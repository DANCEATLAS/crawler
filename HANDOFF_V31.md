# DANCING ATLAS — HANDOFF V31
*(delta on V30; folds in this session: viral section fix, hero 93.5%, sacred/UNESCO verified, + answers to two Edan questions: crawler impact & ingest-readiness.)*

## VERIFIED STATE (this session, proven on screen)
- **Hero coverage: 575/615 (93.5%)** — crawl→push_videos auto-synced +6 since last run; pipeline self-runs.
- **Sacred flags: 178** (needs_eyes_on bool). **UNESCO: 15** (ich_ref). **Duplicate slugs: 0**.
- **VIRAL SECTION: FIXED & LIVE.** Root cause: the app queried a Supabase view `viral_chart` that did not exist → 404 → empty. FIX: created `viral_chart` view mapping `viral_challenges` (154 rows) into the exact 26-column shape the app selects, + pulls each challenge's hero from `dances` via dance_id. Now ALL 154 challenges show, across 7 categories (Song Dance 62, Dance Challenge 47, Pre-Internet 17, Meme 10, Regional 8, Dance Trend 6, K-pop 4) and 3 windows (month/year/all). Verified live. Windows values are 'month'/'year'/'all'; category values are snake_case (dance_challenge, song_dance, kpop_challenge, meme_dance, regional_wave, dance_trend, flashmob_irl, pre_internet_craze).
- **App:** Share button EXISTS (details panel); **BACK ARROW still missing** (pending Lovable). /atlas catalog still served from STATIC JSON (not DB).

## ⭐ CRAWLER ANALYSIS — "are the crawlers really doing the big difference?"
**VERDICT: YES, decisively — and it's near saturation for the current catalog.**
- The crawler is the ENTIRE reason hero coverage exists: it found **979 heroes** (886 high-confidence crowd-wisdom picks). **575** are synced live (93.5%).
- Latest triggered run added **+6** to the holdouts → it's still chipping, but the curve has flattened.
- The remaining **40 heroless** dances are NOT in hero_results under any slug — they are genuinely obscure styles with no good YouTube video. More crawl runs won't move them much.
- **Therefore the crawler's FUTURE value is for NEW dances** (the next 3 research chats), not the current 615. The daily pipeline (gen_dance_list 0815 → crawl → push_videos 0845) is healthy and hands-off.
- Bottleneck was NEVER yield — it was sync (fixed) + slug-mismatch (fixed). Crawler is at high yield. Single YouTube key is sufficient; multi-key is an optional future lever, not a blocker.

## ⭐ INGEST-READINESS AUDIT — "is app/DB ready to ingest the next 3 chats?"
**DB: READY.** `dances` requires only **slug + name** (every other column nullable → full research profiles insert cleanly). **UNIQUE constraint on slug** (upsert-safe). slug indexed. Child tables populated (aliases 2000, sources 1149, edges 958).
**seed.yml: SAFE idempotent upsert.** POST + `Prefer: resolution=merge-duplicates` keyed on slug; loads aliases/sources/edges; **does NOT touch hero_video_youtube_id / ich_ref / needs_eyes_on** → re-ingest PRESERVES heroes, UNESCO refs, and sacred flags. New slugs insert; existing slugs fill/merge.
**CAVEAT 1 (source file):** seed.yml reads `danceworld_final_622.json`. The next 3 chats' verified batches must be MERGED into that file (slug-collision check first) — or seed.yml re-pointed at the canonical running file.
**CAVEAT 2 (VISIBILITY — important):** ingested dances land in the DB but are **INVISIBLE in /atlas until the OVERLAY FLIP (T10)**. The viral section (DB-backed) shows; the catalog/atlas is still static JSON. So ingest works, but users won't see new dances until the flip ships.
**POST-INGEST PIPELINE (run after each batch, all slug-keyed/idempotent):** 1) seed.yml (load) → 2) gen_dance_list.yml (DB→dance_list.json) → 3) crawl.yml (find heroes for new) → 4) push_videos.yml (sync heroes) → 5) unesco_ich.yml (UNESCO refs for new) → 6) re-run the needs_eyes_on sacred-flag UPDATE. Then (eventually) the overlay flip surfaces them.

## TASK STATUS (easiest→hardest; "next" advances)
DONE this session: T1 hero recovery (575), T2 sacred flag (178), T3 dup audit (0), **viral_chart view (T16 data layer)**.
PENDING LOVABLE (Edan paste partially applied — Share yes, back-arrow no): **T11** back-stack fix + back arrow, **T14** share on profiles.
NEXT QUEUE: **T7** citation-resolve Action · **T8** hero quality gate (crawler.py — Edan's shaky-cam/dance-not-visible bug) · **T10 OVERLAY FLIP** (biggest unlock — surfaces all DB work without 1014 regression) · then SEO + share-previews (T13), feed perf (T15), viral ranking upgrade, a11y (T18), monetization (T19).
TIER 5 ongoing: **T20** catalog DEPTH (RAG multi-pass) — fed by the next 3 chats.

## BEST-PRACTICES CONFIRMATION (all session fixes match the research reports)
- viral_chart shape is Bayesian-ranking-READY; currently ranked origin_date desc (newest=#1, all "NEW"). Per Report A, upgrade to time-decay/Wilson score once heart-vote data exists. Attribution discipline preserved in the data (creator≠song-artist; "no single creator"; uncredited Black creators noted).
- Ingest = idempotent slug-keyed upsert (Report A data pipeline).
- UNESCO exact-match only (no wrong badges); sacred flag over-inclusive (safer for review); hero slug-recovery skipped wrong-dance matches (hora-israeli≠hora-romania). All conservative per best practice.

— end V31 —

# Dancing Atlas pipeline status
_Generated 2026-11-24T00:47:05Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 41** · one item short: 45 · two short: 50 · published: 545 · in the atlas: 1300. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 56 profiles (2026-11-24).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 570 · method studied: 98 lessons of 88 teachers · research notes with checked quotes: 45 of 80 topics and 19 papers · practices with two or more kinds of evidence: 29. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1426** · with hero video: **1086** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 21
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1417 · statuses: {'qc_replaced': 239, 'crowd_wisdom_confident': 876, 'qc_failed_pending_recrawl': 207, 'crowd_wisdom_weak': 95}
- Hero QC verdicts: {'pass': 1209, 'fail': 208} (checked 1417)

## Discovery → research → QC
- Candidates: {'researched': 739, 'duplicate_of': 21, 'queued': 528, 'screened_out': 38}
- Research index: {'researched': 1032, 'no_sources': 69, 'llm_failed': 9}
- Legacy presentation fields complete (not interactive readiness): 220 of 1032 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 930, recordings 854, images 754, tempo_or_meter 686, lesson_ladder 653, posture 611, arms_and_hands 525, footage 511
- QC gates: {'reject': 233, 'publish': 556, 'review': 250}
- Active Profile dossiers: 1483; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 553 (1 complete, 7 polished) · translations 6 across 12 languages · teaching playbook from 262 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- indonesian-dance (16/18): missing footwork_with_counts, recordings
- assamese-folk-dance (15/18): missing footwork_with_counts, recordings, footage
- father-daughter-dance (15/18): missing footwork_with_counts, lesson_ladder, images
- finger-tutting (15/18): missing footwork_with_counts, recordings, images
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- gnawa (15/18): missing footwork_with_counts, posture, recordings
- hand-jive (15/18): missing footwork_with_counts, lesson_ladder, images
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- oleg (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- pungmul (15/18): missing footwork_with_counts, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- serbian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings

- Tradition status (schema 5 records): {'living': 781, 'historical': 51, 'unknown': 69, 'revived': 20} · pages with reference footage links: 410

## Last runs
- **audit** 2026-11-23T21:30:31Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-23T21:31:39Z · {"harvested": 3708, "already_known": 1854, "dup_qid": 116, "dup_name": 134, "not_dance_like": 10, "deferred": 555, "dup_fuzzy": 1, "queued_new": 60}
- **research** 2026-11-24T00:13:43Z · {"screened_out_move": 1, "researched_researched": 56, "researched_llm_failed": 8, "kept_existing": 2, "researched_no_sources": 4, "llm_calls": 120, "llm_failures": 63, "llm_requests": 66, "llm_unanswered": 9}
- **qc** 2026-11-24T00:19:59Z · {"gate_publish": 13, "gate_review": 40, "gate_reject": 3, "llm_calls": 37, "llm_failures": 19, "llm_requests": 56, "llm_unanswered": 39}
- **hero_qc** 2026-11-24T00:25:19Z · {"videos_fetched": 55, "verdict_pass": 15, "vision_pending": 1, "verdict_fail": 10, "evicted_for_recrawl": 8, "replaced": 2, "llm_calls": 45, "llm_failures": 12, "llm_requests": 33, "llm_unanswered": 1}
- **build** 2026-11-24T00:25:54Z · {"retired_by_audit": 122, "new_rejected_hidden": 180, "new_publish": 408, "new_review_hidden": 148, "existing_research_rejected": 53, "existing_reject": 53, "existing_publish": 137, "existing_review": 92}
- **sync** 2026-11-24T00:47:03Z · {"patched": 7, "patch_nomatch": 3, "skipped_reject_new": 3, "inserted_publish": 6, "inserted_review": 37}
- **report** 2026-11-22T20:27:29Z · {"review_items": 440}

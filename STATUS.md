# Dancing Atlas pipeline status
_Generated 2026-11-24T22:56:09Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 33** · one item short: 63 · two short: 56 · published: 607 · in the atlas: 1345. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 63 profiles (2026-11-24).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 574 · method studied: 107 lessons of 95 teachers · research notes with checked quotes: 51 of 80 topics and 23 papers · practices with two or more kinds of evidence: 29. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1464** · with hero video: **1109** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 21
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1429 · statuses: {'qc_replaced': 241, 'crowd_wisdom_confident': 880, 'qc_failed_pending_recrawl': 210, 'crowd_wisdom_weak': 98}
- Hero QC verdicts: {'pass': 1218, 'fail': 211} (checked 1429)

## Discovery → research → QC
- Candidates: {'researched': 775, 'duplicate_of': 21, 'queued': 551, 'screened_out': 39}
- Research index: {'researched': 1083, 'no_sources': 70, 'llm_failed': 5}
- Legacy presentation fields complete (not interactive readiness): 234 of 1083 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 982, recordings 902, images 797, tempo_or_meter 725, lesson_ladder 692, posture 642, arms_and_hands 550, footage 544
- QC gates: {'reject': 252, 'publish': 618, 'review': 220}
- Active Profile dossiers: 1528; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 615 (0 complete, 6 polished) · translations 6 across 12 languages · teaching playbook from 293 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

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

- Tradition status (schema 5 records): {'living': 824, 'historical': 56, 'unknown': 73, 'revived': 22} · pages with reference footage links: 431

## Last runs
- **audit** 2026-11-24T20:13:43Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-24T20:16:04Z · {"harvested": 3708, "already_known": 1915, "dup_name": 133, "dup_qid": 117, "not_dance_like": 10, "deferred": 495, "queued_new": 60}
- **research** 2026-11-24T22:06:55Z · {"screened_out_move": 1, "researched_researched": 63, "researched_llm_failed": 4, "kept_existing": 2, "researched_no_sources": 1, "llm_calls": 114, "llm_failures": 53, "llm_requests": 63, "llm_unanswered": 2, "llm_unserved": 2}
- **qc** 2026-11-24T22:11:55Z · {"gate_review": 6, "gate_publish": 39, "gate_reject": 12, "llm_calls": 65, "llm_failures": 7, "llm_requests": 57, "llm_unanswered": 0}
- **hero_qc** 2026-11-24T22:13:18Z · {"videos_fetched": 34, "verdict_fail": 5, "evicted_for_recrawl": 3, "replaced": 2, "verdict_pass": 8, "llm_calls": 18, "llm_failures": 1, "llm_requests": 16, "llm_unanswered": 0}
- **build** 2026-11-24T22:13:55Z · {"retired_by_audit": 122, "new_rejected_hidden": 195, "new_publish": 453, "new_review_hidden": 128, "existing_research_rejected": 57, "existing_reject": 57, "existing_publish": 154, "existing_review": 82}
- **sync** 2026-11-24T22:56:07Z · {"patch_nomatch": 13, "patched": 36, "inserted_publish": 34, "skipped_reject_new": 9, "inserted_review": 4}
- **report** 2026-11-24T00:47:05Z · {"review_items": 483}

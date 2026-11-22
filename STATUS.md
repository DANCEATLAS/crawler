# Dancing Atlas pipeline status
_Generated 2026-11-22T20:27:29Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 40** · one item short: 47 · two short: 51 · published: 540 · in the atlas: 1295. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 59 profiles (2026-11-22).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 561 · method studied: 68 lessons of 60 teachers · research notes with checked quotes: 30 of 80 topics and 12 papers · practices with two or more kinds of evidence: 28. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1383** · with hero video: **1057** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 21
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1392 · statuses: {'qc_replaced': 237, 'crowd_wisdom_confident': 866, 'qc_failed_pending_recrawl': 199, 'crowd_wisdom_weak': 90}
- Hero QC verdicts: {'pass': 1192, 'fail': 200} (checked 1392)

## Discovery → research → QC
- Candidates: {'researched': 706, 'duplicate_of': 20, 'queued': 502, 'screened_out': 37}
- Research index: {'researched': 984, 'no_sources': 65, 'llm_failed': 5}
- Legacy presentation fields complete (not interactive readiness): 203 of 984 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 883, recordings 811, images 711, tempo_or_meter 656, lesson_ladder 621, posture 580, arms_and_hands 503, footage 480
- QC gates: {'reject': 230, 'publish': 551, 'review': 210}
- Active Profile dossiers: 1478; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 548 (1 complete, 6 polished) · translations 6 across 12 languages · teaching playbook from 237 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- indonesian-dance (16/18): missing footwork_with_counts, recordings
- assamese-folk-dance (15/18): missing footwork_with_counts, recordings, footage
- father-daughter-dance (15/18): missing footwork_with_counts, lesson_ladder, images
- finger-tutting (15/18): missing footwork_with_counts, recordings, images
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- gnawa (15/18): missing footwork_with_counts, posture, recordings
- hand-jive (15/18): missing footwork_with_counts, lesson_ladder, images
- jurit-ampil-kridha-warastra-dance (15/18): missing footwork_with_counts, recordings, footage
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- oleg (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- pungmul (15/18): missing footwork_with_counts, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images

- Tradition status (schema 5 records): {'living': 745, 'historical': 44, 'unknown': 66, 'revived': 18} · pages with reference footage links: 393

## Last runs
- **audit** 2026-11-22T17:13:07Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-22T17:14:19Z · {"harvested": 3708, "already_known": 1794, "dup_qid": 117, "dup_name": 130, "not_dance_like": 10, "deferred": 619, "queued_new": 60}
- **research** 2026-11-22T19:58:32Z · {"screened_out_move": 1, "researched_researched": 59, "researched_llm_failed": 4, "kept_existing": 2, "researched_no_sources": 5, "llm_calls": 93, "llm_failures": 28, "llm_requests": 65, "llm_unanswered": 0}
- **qc** 2026-11-22T20:03:47Z · {"gate_publish": 36, "gate_review": 11, "gate_reject": 12, "llm_calls": 73, "llm_failures": 13, "llm_requests": 59, "llm_unanswered": 0}
- **hero_qc** 2026-11-22T20:05:24Z · {"videos_fetched": 43, "verdict_pass": 16, "verdict_fail": 1, "evicted_for_recrawl": 1, "llm_calls": 22, "llm_failures": 1, "llm_requests": 20, "llm_unanswered": 0}
- **build** 2026-11-22T20:05:48Z · {"retired_by_audit": 122, "new_rejected_hidden": 177, "new_publish": 403, "new_review_hidden": 121, "existing_research_rejected": 53, "existing_reject": 53, "existing_publish": 137, "existing_review": 79}
- **sync** 2026-11-22T20:27:27Z · {"patched": 9, "patch_nomatch": 2, "skipped_reject_new": 10, "inserted_publish": 30, "inserted_review": 8}
- **report** 2026-11-21T19:44:03Z · {"review_items": 417}

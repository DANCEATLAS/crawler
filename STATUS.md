# Dancing Atlas pipeline status
_Generated 2026-11-28T19:20:05Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 46** · one item short: 78 · two short: 74 · published: 734 · in the atlas: 1439. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 63 profiles (2026-11-28).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 729 · method studied: 146 lessons of 132 teachers · research notes with checked quotes: 69 of 80 topics and 28 papers · practices with two or more kinds of evidence: 32. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1622** · with hero video: **1205** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 22
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1489 · statuses: {'qc_replaced': 252, 'crowd_wisdom_confident': 912, 'qc_failed_pending_recrawl': 217, 'crowd_wisdom_weak': 108}
- Hero QC verdicts: {'pass': 1271, 'fail': 218} (checked 1489)

## Discovery → research → QC
- Candidates: {'researched': 925, 'duplicate_of': 21, 'queued': 641, 'screened_out': 39}
- Research index: {'researched': 1293, 'no_sources': 76, 'llm_failed': 6}
- Legacy presentation fields complete (not interactive readiness): 288 of 1293 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 1195, recordings 1100, images 963, tempo_or_meter 868, lesson_ladder 838, posture 774, footage 687, arms_and_hands 665
- QC gates: {'reject': 291, 'publish': 745, 'review': 264}
- Active Profile dossiers: 1622; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 742 (0 complete, 9 polished) · translations 7 across 12 languages · teaching playbook from 433 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

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
- molly-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- oleg (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- pungmul (15/18): missing footwork_with_counts, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images

- Tradition status (schema 5 records): {'living': 996, 'unknown': 92, 'historical': 73, 'revived': 31} · pages with reference footage links: 505

## Last runs
- **audit** 2026-11-28T17:38:02Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-28T17:38:35Z · {"harvested": 3624, "already_known": 2147, "dup_qid": 117, "dup_name": 137, "not_dance_like": 10, "deferred": 175, "queued_new": 60}
- **research** 2026-11-28T18:47:13Z · {"researched_researched": 63, "researched_llm_failed": 5, "kept_existing": 2, "llm_calls": 112, "llm_failures": 49, "llm_requests": 63, "llm_unanswered": 0}
- **qc** 2026-11-28T18:51:13Z · {"gate_publish": 38, "gate_review": 11, "gate_reject": 7, "llm_calls": 57, "llm_failures": 0, "llm_requests": 56, "llm_unanswered": 0}
- **hero_qc** 2026-11-28T18:52:48Z · {"videos_fetched": 58, "verdict_pass": 13, "verdict_fail": 4, "replaced": 2, "evicted_for_recrawl": 2, "llm_calls": 23, "llm_failures": 0, "llm_requests": 22, "llm_unanswered": 0}
- **build** 2026-11-28T18:53:29Z · {"retired_by_audit": 122, "new_rejected_hidden": 230, "new_publish": 547, "existing_research_rejected": 61, "existing_reject": 61, "existing_publish": 187, "new_review_hidden": 165, "existing_review": 89}
- **sync** 2026-11-28T19:20:04Z · {"patched": 5, "inserted_review": 11, "inserted_publish": 33, "skipped_reject_new": 7}
- **report** 2026-11-27T21:10:54Z · {"review_items": 537}

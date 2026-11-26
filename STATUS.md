# Dancing Atlas pipeline status
_Generated 2026-11-26T21:11:48Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 41** · one item short: 68 · two short: 60 · published: 664 · in the atlas: 1388. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 64 profiles (2026-11-26).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 712 · method studied: 126 lessons of 113 teachers · research notes with checked quotes: 61 of 80 topics and 28 papers · practices with two or more kinds of evidence: 29. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1537** · with hero video: **1154** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 22
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1454 · statuses: {'qc_replaced': 245, 'crowd_wisdom_confident': 890, 'qc_failed_pending_recrawl': 215, 'crowd_wisdom_weak': 104}
- Hero QC verdicts: {'pass': 1238, 'fail': 216} (checked 1454)

## Discovery → research → QC
- Candidates: {'researched': 850, 'duplicate_of': 21, 'queued': 596, 'screened_out': 39}
- Research index: {'researched': 1186, 'no_sources': 76, 'llm_failed': 4}
- Legacy presentation fields complete (not interactive readiness): 257 of 1186 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 1088, recordings 1002, images 882, tempo_or_meter 799, lesson_ladder 772, posture 708, footage 621, arms_and_hands 609
- QC gates: {'reject': 278, 'publish': 675, 'review': 240}
- Active Profile dossiers: 1571; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 672 (0 complete, 6 polished) · translations 6 across 12 languages · teaching playbook from 374 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

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

- Tradition status (schema 5 records): {'living': 906, 'unknown': 87, 'historical': 64, 'revived': 27} · pages with reference footage links: 463

## Last runs
- **audit** 2026-11-26T19:07:25Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-26T19:07:58Z · {"harvested": 3619, "already_known": 2027, "dup_qid": 117, "dup_name": 135, "not_dance_like": 10, "deferred": 293, "queued_new": 60}
- **research** 2026-11-26T20:36:23Z · {"researched_researched": 64, "researched_llm_failed": 3, "researched_no_sources": 3, "llm_calls": 118, "llm_failures": 57, "llm_requests": 61, "llm_unanswered": 0}
- **qc** 2026-11-26T20:40:36Z · {"gate_reject": 14, "gate_publish": 37, "gate_review": 8, "llm_calls": 60, "llm_failures": 0, "llm_requests": 59, "llm_unanswered": 0}
- **hero_qc** 2026-11-26T20:41:51Z · {"videos_fetched": 28, "verdict_fail": 4, "evicted_for_recrawl": 3, "verdict_pass": 7, "replaced": 1, "llm_calls": 17, "llm_failures": 0, "llm_requests": 16, "llm_unanswered": 0}
- **build** 2026-11-26T20:42:11Z · {"retired_by_audit": 122, "new_rejected_hidden": 218, "new_publish": 496, "new_review_hidden": 144, "existing_research_rejected": 60, "existing_reject": 60, "existing_publish": 168, "existing_review": 86}
- **sync** 2026-11-26T21:11:46Z · {"patch_nomatch": 5, "patched": 7, "skipped_reject_new": 10, "inserted_publish": 30, "inserted_review": 7}
- **report** 2026-11-25T21:48:53Z · {"review_items": 501}

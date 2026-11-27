# Dancing Atlas pipeline status
_Generated 2026-11-27T21:10:54Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 45** · one item short: 73 · two short: 68 · published: 697 · in the atlas: 1415. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 60 profiles (2026-11-27).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 723 · method studied: 136 lessons of 122 teachers · research notes with checked quotes: 65 of 80 topics and 28 papers · practices with two or more kinds of evidence: 31. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1578** · with hero video: **1181** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 22
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1472 · statuses: {'qc_replaced': 250, 'crowd_wisdom_confident': 899, 'qc_failed_pending_recrawl': 215, 'crowd_wisdom_weak': 108}
- Hero QC verdicts: {'pass': 1256, 'fail': 216} (checked 1472)

## Discovery → research → QC
- Candidates: {'researched': 889, 'duplicate_of': 21, 'queued': 617, 'screened_out': 39}
- Research index: {'researched': 1238, 'no_sources': 76, 'llm_failed': 8}
- Legacy presentation fields complete (not interactive readiness): 278 of 1238 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 1141, recordings 1050, images 922, tempo_or_meter 833, lesson_ladder 801, posture 734, footage 650, arms_and_hands 632
- QC gates: {'reject': 284, 'publish': 708, 'review': 253}
- Active Profile dossiers: 1598; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 705 (0 complete, 7 polished) · translations 6 across 12 languages · teaching playbook from 406 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

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

- Tradition status (schema 5 records): {'living': 951, 'unknown': 89, 'historical': 68, 'revived': 29} · pages with reference footage links: 487

## Last runs
- **audit** 2026-11-27T19:03:24Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-27T19:03:56Z · {"harvested": 3624, "already_known": 2087, "dup_qid": 117, "dup_name": 137, "not_dance_like": 10, "deferred": 235, "queued_new": 60}
- **research** 2026-11-27T20:12:44Z · {"researched_researched": 60, "researched_llm_failed": 7, "kept_existing": 3, "llm_calls": 80, "llm_failures": 16, "llm_requests": 64, "llm_unanswered": 0}
- **qc** 2026-11-27T20:16:37Z · {"gate_publish": 34, "gate_review": 14, "gate_reject": 6, "llm_calls": 55, "llm_failures": 0, "llm_requests": 54, "llm_unanswered": 0}
- **hero_qc** 2026-11-27T20:18:17Z · {"videos_fetched": 43, "verdict_pass": 13, "verdict_fail": 5, "replaced": 5, "llm_calls": 24, "llm_failures": 0, "llm_requests": 23, "llm_unanswered": 0}
- **build** 2026-11-27T20:18:52Z · {"retired_by_audit": 122, "new_rejected_hidden": 223, "new_publish": 523, "existing_research_rejected": 61, "existing_reject": 61, "existing_publish": 174, "new_review_hidden": 156, "existing_review": 87}
- **sync** 2026-11-27T21:10:52Z · {"patched": 6, "inserted_publish": 30, "inserted_review": 11, "skipped_reject_new": 6, "patch_nomatch": 1}
- **report** 2026-11-26T21:11:48Z · {"review_items": 518}

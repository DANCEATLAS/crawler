# Dancing Atlas pipeline status
_Generated 2026-11-20T20:13:43Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 32** · one item short: 41 · two short: 39 · published: 476 · in the atlas: 1244. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 67 profiles (2026-11-20).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 549 · method studied: 51 lessons of 45 teachers · research notes with checked quotes: 24 of 66 topics and 9 papers · practices with two or more kinds of evidence: 23. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1302** · with hero video: **1005** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1357 · statuses: {'qc_replaced': 235, 'crowd_wisdom_confident': 844, 'qc_failed_pending_recrawl': 196, 'crowd_wisdom_weak': 82}
- Hero QC verdicts: {'pass': 1160, 'fail': 197} (checked 1357)

## Discovery → research → QC
- Candidates: {'researched': 632, 'duplicate_of': 20, 'queued': 458, 'screened_out': 35}
- Research index: {'researched': 881, 'no_sources': 54, 'llm_failed': 2}
- Legacy presentation fields complete (not interactive readiness): 163 of 881 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 779, recordings 714, images 630, tempo_or_meter 592, lesson_ladder 566, posture 525, arms_and_hands 457, footage 419
- QC gates: {'reject': 210, 'publish': 487, 'review': 191}
- Active Profile dossiers: 1427; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 484 (1 complete, 5 polished) · translations 6 across 12 languages · teaching playbook from 170 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- indonesian-dance (16/18): missing footwork_with_counts, recordings
- assamese-folk-dance (15/18): missing footwork_with_counts, recordings, footage
- father-daughter-dance (15/18): missing footwork_with_counts, lesson_ladder, images
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- hand-jive (15/18): missing footwork_with_counts, lesson_ladder, images
- jurit-ampil-kridha-warastra-dance (15/18): missing footwork_with_counts, recordings, footage
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- pungmul (15/18): missing footwork_with_counts, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- serbian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, instruments
- the-running-man (15/18): missing lesson_ladder, hooks, images

- Tradition status (schema 5 records): {'living': 660, 'historical': 39, 'unknown': 56, 'revived': 12} · pages with reference footage links: 348

## Last runs
- **audit** 2026-11-20T17:52:43Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-20T17:53:35Z · {"harvested": 3707, "already_known": 1674, "dup_qid": 117, "dup_name": 126, "not_dance_like": 10, "deferred": 742, "queued_new": 60}
- **research** 2026-11-20T19:45:30Z · {"researched_researched": 67, "researched_llm_failed": 1, "researched_no_sources": 2, "llm_calls": 103, "llm_failures": 35, "llm_requests": 68, "llm_unanswered": 0}
- **qc** 2026-11-20T19:50:20Z · {"gate_publish": 44, "gate_review": 17, "gate_reject": 6, "llm_calls": 68, "llm_failures": 0, "llm_requests": 67, "llm_unanswered": 0}
- **hero_qc** 2026-11-20T19:52:01Z · {"videos_fetched": 40, "verdict_fail": 3, "replaced": 3, "verdict_pass": 12, "llm_calls": 19, "llm_failures": 0, "llm_requests": 18, "llm_unanswered": 0}
- **build** 2026-11-20T19:52:22Z · {"retired_by_audit": 122, "new_rejected_hidden": 161, "new_publish": 352, "new_review_hidden": 110, "existing_research_rejected": 49, "existing_reject": 49, "existing_publish": 124, "existing_review": 71}
- **sync** 2026-11-20T20:13:41Z · {"patched": 11, "patch_nomatch": 4, "inserted_publish": 33, "skipped_reject_new": 6, "inserted_review": 13}
- **report** 2026-11-19T20:57:05Z · {"review_items": 379}

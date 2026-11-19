# Dancing Atlas pipeline status
_Generated 2026-11-19T20:57:05Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 28** · one item short: 37 · two short: 30 · published: 442 · in the atlas: 1215. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 62 profiles (2026-11-19).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 529 · method studied: 41 lessons of 36 teachers · research notes with checked quotes: 21 of 66 topics and 8 papers · practices with two or more kinds of evidence: 22. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1256** · with hero video: **985** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1342 · statuses: {'qc_replaced': 232, 'crowd_wisdom_confident': 833, 'qc_failed_pending_recrawl': 196, 'crowd_wisdom_weak': 81}
- Hero QC verdicts: {'pass': 1145, 'fail': 197} (checked 1342)

## Discovery → research → QC
- Candidates: {'researched': 593, 'duplicate_of': 20, 'queued': 437, 'screened_out': 35}
- Research index: {'researched': 825, 'no_sources': 52, 'llm_failed': 9}
- Legacy presentation fields complete (not interactive readiness): 144 of 825 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 723, recordings 662, images 581, tempo_or_meter 560, lesson_ladder 528, posture 491, arms_and_hands 426, footage 383
- QC gates: {'reject': 204, 'publish': 453, 'review': 175}
- Active Profile dossiers: 1398; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 450 (0 complete, 6 polished) · translations 6 across 12 languages · teaching playbook from 151 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

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

- Tradition status (schema 5 records): {'living': 612, 'historical': 35, 'unknown': 51, 'revived': 11} · pages with reference footage links: 326

## Last runs
- **audit** 2026-11-19T18:22:46Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-19T18:23:53Z · {"harvested": 3707, "dup_qid": 117, "already_known": 1612, "dup_name": 126, "dup_fuzzy": 2, "deferred": 802, "not_dance_like": 10, "queued_new": 60}
- **research** 2026-11-19T20:22:52Z · {"researched_researched": 62, "researched_llm_failed": 8, "llm_calls": 115, "llm_failures": 45, "llm_requests": 70, "llm_unanswered": 0}
- **qc** 2026-11-19T20:28:14Z · {"gate_publish": 42, "gate_reject": 14, "gate_review": 6, "llm_calls": 64, "llm_failures": 1, "llm_requests": 62, "llm_unanswered": 0}
- **hero_qc** 2026-11-19T20:29:50Z · {"videos_fetched": 28, "verdict_pass": 5, "verdict_fail": 7, "replaced": 4, "evicted_for_recrawl": 3, "llm_calls": 19, "llm_failures": 0, "llm_requests": 18, "llm_unanswered": 0}
- **build** 2026-11-19T20:30:17Z · {"retired_by_audit": 122, "new_rejected_hidden": 156, "new_publish": 323, "new_review_hidden": 101, "existing_research_rejected": 48, "existing_reject": 48, "existing_publish": 119, "existing_review": 64}
- **sync** 2026-11-19T20:57:03Z · {"patched": 14, "patch_nomatch": 1, "inserted_publish": 29, "skipped_reject_new": 13, "inserted_review": 5}
- **report** 2026-11-18T21:44:57Z · {"review_items": 361}

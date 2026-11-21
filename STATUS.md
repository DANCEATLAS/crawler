# Dancing Atlas pipeline status
_Generated 2026-11-21T19:44:03Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 37** · one item short: 45 · two short: 46 · published: 512 · in the atlas: 1272. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 62 profiles (2026-11-21).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 553 · method studied: 60 lessons of 53 teachers · research notes with checked quotes: 24 of 80 topics and 9 papers · practices with two or more kinds of evidence: 24. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1345** · with hero video: **1029** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 21
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1375 · statuses: {'qc_replaced': 237, 'crowd_wisdom_confident': 854, 'qc_failed_pending_recrawl': 198, 'crowd_wisdom_weak': 86}
- Hero QC verdicts: {'pass': 1176, 'fail': 199} (checked 1375)

## Discovery → research → QC
- Candidates: {'researched': 670, 'duplicate_of': 20, 'queued': 479, 'screened_out': 36}
- Research index: {'researched': 933, 'no_sources': 60, 'llm_failed': 3}
- Legacy presentation fields complete (not interactive readiness): 180 of 933 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 832, recordings 767, images 669, tempo_or_meter 624, lesson_ladder 593, posture 553, arms_and_hands 481, footage 455
- QC gates: {'reject': 218, 'publish': 523, 'review': 199}
- Active Profile dossiers: 1455; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 520 (1 complete, 5 polished) · translations 6 across 12 languages · teaching playbook from 203 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

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
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- pungmul (15/18): missing footwork_with_counts, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- serbian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings

- Tradition status (schema 5 records): {'living': 703, 'historical': 42, 'unknown': 62, 'revived': 14} · pages with reference footage links: 366

## Last runs
- **audit** 2026-11-21T16:50:57Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-21T16:52:05Z · {"harvested": 3708, "already_known": 1734, "dup_qid": 117, "dup_name": 128, "not_dance_like": 10, "deferred": 681, "queued_new": 60}
- **research** 2026-11-21T19:15:37Z · {"screened_out_move": 1, "researched_researched": 62, "researched_llm_failed": 2, "researched_no_sources": 6, "llm_calls": 104, "llm_failures": 40, "llm_requests": 64, "llm_unanswered": 0}
- **qc** 2026-11-21T19:20:18Z · {"gate_publish": 46, "gate_review": 8, "gate_reject": 8, "llm_calls": 64, "llm_failures": 1, "llm_requests": 62, "llm_unanswered": 0}
- **hero_qc** 2026-11-21T19:21:44Z · {"videos_fetched": 41, "verdict_fail": 4, "evicted_for_recrawl": 2, "verdict_pass": 14, "replaced": 2, "llm_calls": 21, "llm_failures": 0, "llm_requests": 20, "llm_unanswered": 0}
- **build** 2026-11-21T19:22:08Z · {"retired_by_audit": 122, "new_rejected_hidden": 168, "new_publish": 380, "new_review_hidden": 114, "existing_research_rejected": 50, "existing_reject": 50, "existing_publish": 132, "existing_review": 75}
- **sync** 2026-11-21T19:44:01Z · {"patched": 10, "inserted_review": 7, "inserted_publish": 36, "skipped_reject_new": 8, "patch_nomatch": 1}
- **report** 2026-11-20T20:13:43Z · {"review_items": 401}

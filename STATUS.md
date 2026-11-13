# Dancing Atlas pipeline status
_Generated 2026-11-13T18:30:33Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **1072** · with hero video: **875** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1269 · statuses: {'qc_replaced': 166, 'crowd_wisdom_confident': 867, 'qc_failed_pending_recrawl': 138, 'crowd_wisdom_weak': 98}
- Hero QC verdicts: {'pass': 858, 'fail': 138} (checked 996)

## Discovery → research → QC
- Candidates: {'researched': 415, 'duplicate_of': 17, 'queued': 296, 'screened_out': 34}
- Research index: {'researched': 580, 'llm_failed': 3, 'no_sources': 49}
- Legacy presentation fields complete (not interactive readiness): 102 of 580 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 453, recordings 408, images 382, tempo_or_meter 381, lesson_ladder 343, posture 324, arms_and_hands 277, formation 215
- QC gates: {'reject': 134, 'publish': 315, 'review': 138}
- Active Profile dossiers: 1291; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 312 (0 complete, 6 polished) · translations 8 across 12 languages · teaching playbook from 58 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- pungmul (16/18): missing footwork_with_counts, recordings
- assamese-folk-dance (15/18): missing footwork_with_counts, recordings, footage
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- humppa (15/17): missing lesson_ladder, images
- iranian-dance (15/18): missing formation, lesson_ladder, recordings
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- serbian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, instruments
- the-running-man (15/18): missing lesson_ladder, hooks, images
- twist (15/18): missing footwork_with_counts, lesson_ladder, images
- zambra (15/18): missing footwork_with_counts, lesson_ladder, images

- Tradition status (schema 5 records): {'living': 364, 'unknown': 34, 'historical': 24, 'revived': 5} · pages with reference footage links: 220

## Last runs
- **audit** 2026-11-13T17:15:42Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-13T17:16:42Z · {"harvested": 3682, "already_known": 1309, "dup_qid": 117, "dup_name": 118, "deferred": 1119, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-13T18:15:04Z · {"researched_researched": 40, "llm_calls": 51, "llm_failures": 11, "llm_requests": 40, "llm_unanswered": 0}
- **qc** 2026-11-13T18:17:49Z · {"gate_publish": 25, "gate_review": 6, "gate_reject": 9, "llm_calls": 50, "llm_failures": 10, "llm_requests": 40, "llm_unanswered": 0}
- **hero_qc** 2026-11-13T18:24:21Z · {"videos_fetched": 116, "verdict_pass": 42, "verdict_fail": 18, "evicted_for_recrawl": 13, "replaced": 5, "llm_calls": 85, "llm_failures": 11, "llm_requests": 74, "llm_unanswered": 0}
- **build** 2026-11-13T18:24:37Z · {"retired_by_audit": 122, "new_rejected_hidden": 104, "new_publish": 216, "new_review_hidden": 79, "existing_research_rejected": 30, "existing_reject": 30, "existing_publish": 88, "existing_review": 49}
- **sync** 2026-11-13T18:30:31Z · {"patched": 5, "inserted_publish": 20, "inserted_review": 6, "skipped_reject_new": 9}
- **report** 2026-11-12T19:01:21Z · {"review_items": 257}

# Dancing Atlas pipeline status
_Generated 2026-11-14T17:48:39Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **1097** · with hero video: **892** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1282 · statuses: {'qc_replaced': 171, 'crowd_wisdom_confident': 868, 'qc_failed_pending_recrawl': 147, 'crowd_wisdom_weak': 96}
- Hero QC verdicts: {'pass': 909, 'fail': 147} (checked 1056)

## Discovery → research → QC
- Candidates: {'researched': 440, 'duplicate_of': 17, 'queued': 311, 'screened_out': 34}
- Research index: {'researched': 615, 'llm_failed': 3, 'no_sources': 49}
- Legacy presentation fields complete (not interactive readiness): 107 of 615 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 490, recordings 445, images 410, tempo_or_meter 406, lesson_ladder 347, posture 342, arms_and_hands 295, footage 230
- QC gates: {'reject': 144, 'publish': 332, 'review': 146}
- Active Profile dossiers: 1303; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 329 (0 complete, 5 polished) · translations 8 across 12 languages · teaching playbook from 64 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- pungmul (16/18): missing footwork_with_counts, recordings
- assamese-folk-dance (15/18): missing footwork_with_counts, recordings, footage
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- humppa (15/17): missing lesson_ladder, images
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- serbian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, instruments
- the-running-man (15/18): missing lesson_ladder, hooks, images
- twist (15/18): missing footwork_with_counts, lesson_ladder, images
- zambra (15/18): missing footwork_with_counts, lesson_ladder, images
- australian-dance (14/18): missing posture, tempo_or_meter, lesson_ladder, images

- Tradition status (schema 5 records): {'living': 399, 'unknown': 35, 'historical': 24, 'revived': 5} · pages with reference footage links: 233

## Last runs
- **audit** 2026-11-14T15:52:05Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-14T15:52:49Z · {"harvested": 3687, "dup_qid": 117, "already_known": 1349, "dup_name": 119, "deferred": 1081, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-14T17:21:17Z · {"researched_researched": 40, "llm_calls": 53, "llm_failures": 13, "llm_requests": 40, "llm_unanswered": 0}
- **qc** 2026-11-14T17:28:05Z · {"gate_publish": 22, "gate_reject": 10, "gate_review": 8, "llm_calls": 47, "llm_failures": 7, "llm_requests": 40, "llm_unanswered": 0}
- **hero_qc** 2026-11-14T17:42:56Z · {"videos_fetched": 131, "verdict_fail": 14, "evicted_for_recrawl": 9, "verdict_pass": 46, "replaced": 5, "llm_calls": 81, "llm_failures": 8, "llm_requests": 73, "llm_unanswered": 0}
- **build** 2026-11-14T17:43:08Z · {"retired_by_audit": 122, "new_rejected_hidden": 112, "new_publish": 228, "new_review_hidden": 84, "existing_research_rejected": 32, "existing_reject": 32, "existing_publish": 93, "existing_review": 52}
- **sync** 2026-11-14T17:48:38Z · {"patched": 5, "skipped_reject_new": 12, "inserted_publish": 17, "inserted_review": 8}
- **report** 2026-11-13T18:30:33Z · {"review_items": 272}

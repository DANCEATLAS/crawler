# Dancing Atlas pipeline status
_Generated 2026-11-11T18:56:02Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **1020** · with hero video: **844** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1249 · statuses: {'qc_replaced': 152, 'crowd_wisdom_confident': 876, 'qc_failed_pending_recrawl': 120, 'crowd_wisdom_weak': 101}
- Hero QC verdicts: {'pass': 756, 'fail': 120} (checked 876)

## Discovery → research → QC
- Candidates: {'researched': 365, 'duplicate_of': 17, 'queued': 266, 'screened_out': 34}
- Research index: {'researched': 512, 'llm_failed': 3, 'no_sources': 47}
- Legacy presentation fields complete (not interactive readiness): 101 of 512 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 381, recordings 343, images 337, tempo_or_meter 329, lesson_ladder 279, posture 264, arms_and_hands 233, formation 172
- QC gates: {'reject': 118, 'publish': 282, 'review': 119}
- Active Profile dossiers: 1265; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 279 (0 complete, 5 polished) · translations 8 across 12 languages · teaching playbook from 48 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- pungmul (16/18): missing footwork_with_counts, recordings
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- humppa (15/17): missing lesson_ladder, images
- iranian-dance (15/18): missing formation, lesson_ladder, recordings
- line-dance (15/18): missing posture, arms_and_hands, lesson_ladder
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- moshing (15/18): missing tempo_or_meter, lesson_ladder, hooks
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, lesson_ladder
- the-running-man (15/18): missing lesson_ladder, hooks, images
- zambra (15/18): missing footwork_with_counts, lesson_ladder, images
- australian-dance (14/18): missing posture, tempo_or_meter, lesson_ladder, images
- danza-de-los-diablos (14/18): missing tempo_or_meter, lesson_ladder, recordings, images

- Tradition status (schema 5 records): {'living': 303, 'unknown': 29, 'historical': 21, 'revived': 4} · pages with reference footage links: 195

## Last runs
- **audit** 2026-11-11T17:15:10Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-11T17:16:28Z · {"harvested": 3682, "already_known": 1229, "dup_qid": 116, "dup_name": 118, "deferred": 1200, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-11T18:28:55Z · {"researched_researched": 36, "researched_no_sources": 4, "llm_calls": 45, "llm_failures": 9, "llm_requests": 36, "llm_unanswered": 0}
- **qc** 2026-11-11T18:40:38Z · {"gate_publish": 27, "gate_review": 8, "gate_reject": 1, "llm_calls": 47, "llm_failures": 11, "llm_requests": 36, "llm_unanswered": 0}
- **hero_qc** 2026-11-11T18:48:54Z · {"videos_fetched": 151, "verdict_pass": 34, "verdict_fail": 26, "replaced": 18, "evicted_for_recrawl": 8, "llm_calls": 98, "llm_failures": 13, "llm_requests": 85, "llm_unanswered": 0}
- **build** 2026-11-11T18:49:18Z · {"retired_by_audit": 122, "new_rejected_hidden": 93, "new_publish": 190, "new_review_hidden": 66, "existing_research_rejected": 25, "existing_reject": 25, "existing_publish": 81, "existing_review": 43}
- **sync** 2026-11-11T18:56:01Z · {"patched": 5, "inserted_publish": 22, "inserted_review": 8, "skipped_reject_new": 1}
- **report** 2026-11-10T19:28:55Z · {"review_items": 228}

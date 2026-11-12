# Dancing Atlas pipeline status
_Generated 2026-11-12T19:01:20Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **1046** · with hero video: **862** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1262 · statuses: {'qc_replaced': 161, 'crowd_wisdom_confident': 876, 'qc_failed_pending_recrawl': 125, 'crowd_wisdom_weak': 100}
- Hero QC verdicts: {'pass': 811, 'fail': 125} (checked 936)

## Discovery → research → QC
- Candidates: {'researched': 390, 'duplicate_of': 17, 'queued': 281, 'screened_out': 34}
- Research index: {'researched': 545, 'llm_failed': 3, 'no_sources': 49}
- Legacy presentation fields complete (not interactive readiness): 103 of 545 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 416, recordings 373, images 360, tempo_or_meter 356, lesson_ladder 310, posture 292, arms_and_hands 255, formation 193
- QC gates: {'reject': 125, 'publish': 295, 'review': 132}
- Active Profile dossiers: 1274; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 292 (0 complete, 5 polished) · translations 8 across 12 languages · teaching playbook from 53 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- pungmul (16/18): missing footwork_with_counts, recordings
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- humppa (15/17): missing lesson_ladder, images
- iranian-dance (15/18): missing formation, lesson_ladder, recordings
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, lesson_ladder
- the-running-man (15/18): missing lesson_ladder, hooks, images
- zambra (15/18): missing footwork_with_counts, lesson_ladder, images
- australian-dance (14/18): missing posture, tempo_or_meter, lesson_ladder, images
- danza-de-los-diablos (14/18): missing tempo_or_meter, lesson_ladder, recordings, images
- debaa (14/18): missing footwork_with_counts, tempo_or_meter, recordings, images

- Tradition status (schema 5 records): {'living': 334, 'unknown': 31, 'historical': 22, 'revived': 4} · pages with reference footage links: 210

## Last runs
- **audit** 2026-11-12T17:38:18Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-12T17:39:28Z · {"harvested": 3682, "already_known": 1269, "dup_name": 119, "dup_qid": 116, "deferred": 1159, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-12T18:32:34Z · {"researched_researched": 38, "researched_no_sources": 2, "llm_calls": 47, "llm_failures": 9, "llm_requests": 38, "llm_unanswered": 0}
- **qc** 2026-11-12T18:37:17Z · {"gate_publish": 18, "gate_reject": 7, "gate_review": 13, "llm_calls": 50, "llm_failures": 12, "llm_requests": 38, "llm_unanswered": 0}
- **hero_qc** 2026-11-12T18:51:08Z · {"videos_fetched": 151, "verdict_pass": 46, "verdict_fail": 14, "replaced": 9, "evicted_for_recrawl": 5, "llm_calls": 91, "llm_failures": 19, "llm_requests": 72, "llm_unanswered": 0}
- **build** 2026-11-12T18:51:32Z · {"retired_by_audit": 122, "new_rejected_hidden": 99, "new_publish": 199, "new_review_hidden": 76, "existing_research_rejected": 26, "existing_reject": 26, "existing_publish": 85, "existing_review": 46}
- **sync** 2026-11-12T19:01:18Z · {"patched": 5, "skipped_reject_new": 7, "inserted_review": 13, "inserted_publish": 13}
- **report** 2026-11-11T18:56:02Z · {"review_items": 237}

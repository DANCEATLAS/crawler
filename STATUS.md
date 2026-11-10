# Dancing Atlas pipeline status
_Generated 2026-11-10T19:28:55Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **991** · with hero video: **823** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1236 · statuses: {'qc_replaced': 134, 'crowd_wisdom_confident': 884, 'qc_failed_pending_recrawl': 112, 'crowd_wisdom_weak': 106}
- Hero QC verdicts: {'pass': 704, 'fail': 112} (checked 816)

## Discovery → research → QC
- Candidates: {'researched': 340, 'duplicate_of': 17, 'queued': 251, 'screened_out': 34}
- Research index: {'researched': 481, 'llm_failed': 3, 'no_sources': 43}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 104 of 481 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 348, images 314, recordings 310, tempo_or_meter 306, lesson_ladder 246, posture 236, arms_and_hands 212, formation 156
- QC gates: {'reject': 117, 'publish': 260, 'review': 111}
- Editor notes open: 0 · pages with editor-added sources: 6
- Movie phase: episode packs 257 (0 complete, 8 polished) · translations 7 across 12 languages · teaching playbook from 42 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to movie-ready (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- pungmul (16/18): missing footwork_with_counts, recordings
- daggering (15/18): missing footwork_with_counts, tempo_or_meter, images
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

- Tradition status (schema 5 records): {'living': 270, 'unknown': 29, 'historical': 20, 'revived': 4} · pages with reference footage links: 180

## Last runs
- **audit** 2026-11-10T17:07:18Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-10T17:08:42Z · {"harvested": 3682, "already_known": 1189, "dup_qid": 116, "dup_name": 118, "deferred": 1240, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-10T18:57:25Z · {"screened_out_move": 1, "researched_researched": 39, "researched_no_sources": 1, "llm_calls": 55, "llm_failures": 16, "llm_requests": 39, "llm_unanswered": 0}
- **qc** 2026-11-10T19:07:12Z · {"gate_publish": 31, "gate_review": 8, "llm_calls": 51, "llm_failures": 12, "llm_requests": 39, "llm_unanswered": 0}
- **hero_qc** 2026-11-10T19:16:09Z · {"videos_fetched": 137, "verdict_pass": 41, "verdict_fail": 19, "evicted_for_recrawl": 8, "replaced": 11, "llm_calls": 92, "llm_failures": 14, "llm_requests": 78, "llm_unanswered": 0}
- **build** 2026-11-10T19:16:33Z · {"retired_by_audit": 122, "new_rejected_hidden": 92, "new_publish": 172, "new_review_hidden": 60, "existing_research_rejected": 25, "existing_reject": 25, "existing_publish": 77, "existing_review": 41}
- **sync** 2026-11-10T19:28:53Z · {"patched": 5, "inserted_review": 8, "inserted_publish": 26}
- **report** 2026-11-09T21:56:24Z · {"review_items": 220}

# Dancing Atlas pipeline status
_Generated 2026-11-08T17:31:28Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **938** · with hero video: **795** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1213 · statuses: {'qc_replaced': 115, 'crowd_wisdom_confident': 894, 'qc_failed_pending_recrawl': 97, 'crowd_wisdom_weak': 107}
- Hero QC verdicts: {'pass': 599, 'fail': 97} (checked 696)

## Discovery → research → QC
- Candidates: {'researched': 290, 'duplicate_of': 17, 'queued': 223, 'screened_out': 32}
- Research index: {'researched': 422, 'llm_failed': 3, 'no_sources': 42}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 87 of 422 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 277, images 273, tempo_or_meter 261, recordings 248, lesson_ladder 216, posture 203, arms_and_hands 187, formation 136
- QC gates: {'reject': 109, 'publish': 218, 'review': 102}
- Editor notes open: 0 · pages with editor-added sources: 0
- Movie phase: episode packs 217 (0 complete, 28 polished) · translations 36 across 12 languages · teaching playbook from 34 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to movie-ready (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- chinelos (16/18): missing tempo_or_meter, lesson_ladder
- circassian-dance (15/18): missing footwork_with_counts, tempo_or_meter, instruments
- daggering (15/18): missing footwork_with_counts, tempo_or_meter, images
- hand-jive (15/18): missing footwork_with_counts, lesson_ladder, images
- humppa (15/17): missing lesson_ladder, images
- iranian-dance (15/18): missing formation, lesson_ladder, recordings
- line-dance (15/18): missing posture, arms_and_hands, lesson_ladder
- moshing (15/18): missing tempo_or_meter, lesson_ladder, hooks
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- pungmul (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- semah-alevi-bektasi-ritual (15/18): missing posture, lesson_ladder, recordings
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, lesson_ladder
- the-running-man (15/18): missing lesson_ladder, hooks, images
- vallenato (15/18): missing lesson_ladder, images, footage

- Tradition status (schema 5 records): {'living': 207, 'unknown': 26, 'historical': 17, 'revived': 3} · pages with reference footage links: 136

## Last runs
- **audit** 2026-11-08T16:02:09Z · {"retired_or_merged_total": 110}
- **discover** 2026-11-08T16:03:29Z · {"harvested": 3682, "dup_qid": 116, "already_known": 1109, "dup_name": 115, "deferred": 1323, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-08T16:58:46Z · {"researched_researched": 32, "researched_no_sources": 8, "llm_calls": 42, "llm_failures": 10, "llm_requests": 32, "llm_unanswered": 0}
- **qc** 2026-11-08T17:13:00Z · {"gate_publish": 18, "gate_reject": 7, "gate_review": 7, "llm_calls": 44, "llm_failures": 12, "llm_requests": 32, "llm_unanswered": 0}
- **hero_qc** 2026-11-08T17:22:35Z · {"videos_fetched": 149, "verdict_pass": 47, "verdict_fail": 13, "replaced": 7, "evicted_for_recrawl": 6, "llm_calls": 88, "llm_failures": 10, "llm_requests": 78, "llm_unanswered": 0}
- **build** 2026-11-08T17:22:54Z · {"retired_by_audit": 110, "new_rejected_hidden": 84, "new_publish": 150, "new_review_hidden": 55, "existing_research_rejected": 25, "existing_reject": 25, "existing_publish": 67, "existing_review": 47}
- **sync** 2026-11-08T17:31:26Z · {"inserted_publish": 18, "skipped_reject_new": 7, "inserted_review": 7}
- **report** 2026-11-07T17:45:27Z · {"review_items": 197}

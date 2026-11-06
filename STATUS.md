# Dancing Atlas pipeline status
_Generated 2026-11-06T19:04:22Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **883** · with hero video: **754** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 19
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1186 · statuses: {'qc_replaced': 96, 'crowd_wisdom_confident': 896, 'qc_failed_pending_recrawl': 85, 'crowd_wisdom_weak': 109}
- Hero QC verdicts: {'pass': 491, 'fail': 85} (checked 576)

## Discovery → research → QC
- Candidates: {'researched': 240, 'duplicate_of': 17, 'queued': 193, 'screened_out': 32}
- Research index: {'researched': 354, 'llm_failed': 3, 'no_sources': 30}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 72 of 354 researched
- What classes still lack most (count of researched pages missing it): images 224, footwork_with_counts 217, tempo_or_meter 207, recordings 195, lesson_ladder 167, posture 156, arms_and_hands 146, formation 104
- QC gates: {'reject': 96, 'publish': 177, 'review': 88}
- Editor notes open: 0 · pages with editor-added sources: 0
- Movie phase: episode packs 176 (0 complete, 20 polished) · translations 24 across 12 languages · teaching playbook from 23 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to movie-ready (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- chinelos (16/18): missing tempo_or_meter, lesson_ladder
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
- zambra (15/18): missing footwork_with_counts, lesson_ladder, images
- fleckerl (14/17): missing sound_description, recordings, images

- Tradition status (schema 5 records): {'living': 153, 'unknown': 15, 'historical': 14, 'revived': 3} · pages with reference footage links: 106

## Last runs
- **audit** 2026-11-06T16:50:05Z · {"retired_or_merged_total": 110}
- **discover** 2026-11-06T16:51:02Z · {"harvested": 3682, "already_known": 1029, "dup_name": 112, "dup_qid": 114, "deferred": 1408, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-06T18:34:39Z · {"researched_researched": 38, "researched_no_sources": 2, "llm_calls": 49, "llm_failures": 11, "llm_requests": 38, "llm_unanswered": 0}
- **qc** 2026-11-06T18:39:43Z · {"gate_publish": 25, "gate_review": 3, "gate_reject": 10, "llm_calls": 45, "llm_failures": 7, "llm_requests": 38, "llm_unanswered": 0}
- **hero_qc** 2026-11-06T18:54:37Z · {"videos_fetched": 148, "verdict_pass": 45, "verdict_fail": 15, "replaced": 10, "evicted_for_recrawl": 5, "llm_calls": 92, "llm_failures": 10, "llm_requests": 82, "llm_unanswered": 0}
- **build** 2026-11-06T18:54:55Z · {"retired_by_audit": 110, "new_rejected_hidden": 75, "new_publish": 119, "new_review_hidden": 45, "existing_research_rejected": 21, "existing_reject": 21, "existing_publish": 57, "existing_review": 43}
- **sync** 2026-11-06T19:04:20Z · {"skipped_reject_new": 12, "inserted_publish": 25, "inserted_review": 3}
- **report** 2026-11-05T19:37:53Z · {"review_items": 171}

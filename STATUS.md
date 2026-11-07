# Dancing Atlas pipeline status
_Generated 2026-11-07T17:45:27Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **913** · with hero video: **776** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 19
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1201 · statuses: {'qc_replaced': 108, 'crowd_wisdom_confident': 894, 'qc_failed_pending_recrawl': 91, 'crowd_wisdom_weak': 108}
- Hero QC verdicts: {'pass': 545, 'fail': 91} (checked 636)

## Discovery → research → QC
- Candidates: {'researched': 265, 'duplicate_of': 17, 'queued': 208, 'screened_out': 32}
- Research index: {'researched': 390, 'llm_failed': 3, 'no_sources': 34}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 82 of 390 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 248, images 248, tempo_or_meter 233, recordings 220, lesson_ladder 190, posture 178, arms_and_hands 167, formation 118
- QC gates: {'reject': 102, 'publish': 200, 'review': 95}
- Editor notes open: 0 · pages with editor-added sources: 0
- Movie phase: episode packs 199 (0 complete, 24 polished) · translations 30 across 12 languages · teaching playbook from 28 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to movie-ready (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
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

- Tradition status (schema 5 records): {'living': 181, 'unknown': 21, 'historical': 16, 'revived': 3} · pages with reference footage links: 124

## Last runs
- **audit** 2026-11-07T15:43:56Z · {"retired_or_merged_total": 110}
- **discover** 2026-11-07T15:45:06Z · {"harvested": 3682, "dup_qid": 115, "already_known": 1069, "dup_name": 114, "deferred": 1365, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-07T17:26:17Z · {"researched_researched": 36, "researched_no_sources": 4, "llm_calls": 49, "llm_failures": 13, "llm_requests": 36, "llm_unanswered": 0}
- **qc** 2026-11-07T17:30:20Z · {"gate_publish": 23, "gate_review": 7, "gate_reject": 6, "llm_calls": 41, "llm_failures": 5, "llm_requests": 36, "llm_unanswered": 0}
- **hero_qc** 2026-11-07T17:41:56Z · {"videos_fetched": 154, "verdict_pass": 42, "verdict_fail": 18, "replaced": 12, "evicted_for_recrawl": 6, "llm_calls": 88, "llm_failures": 5, "llm_requests": 83, "llm_unanswered": 0}
- **build** 2026-11-07T17:42:17Z · {"retired_by_audit": 110, "new_rejected_hidden": 79, "new_publish": 135, "new_review_hidden": 50, "existing_research_rejected": 23, "existing_reject": 23, "existing_publish": 64, "existing_review": 45}
- **sync** 2026-11-07T17:45:26Z · {"inserted_publish": 23, "inserted_review": 7, "skipped_reject_new": 6}
- **report** 2026-11-06T19:04:22Z · {"review_items": 184}

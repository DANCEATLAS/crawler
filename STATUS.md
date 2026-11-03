# Dancing Atlas pipeline status
_Generated 2026-11-03T18:45:04Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **797** · with hero video: **690** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 19
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1148 · statuses: {'qc_replaced': 71, 'crowd_wisdom_confident': 917, 'qc_failed_pending_recrawl': 53, 'crowd_wisdom_weak': 107}
- Hero QC verdicts: {'pass': 343, 'fail': 53} (checked 396)

## Discovery → research → QC
- Candidates: {'researched': 165, 'duplicate_of': 17, 'queued': 149, 'screened_out': 31}
- Research index: {'researched': 243, 'llm_failed': 3, 'no_sources': 21}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 45 of 243 researched
- What classes still lack most (count of researched pages missing it): images 142, tempo_or_meter 133, footwork_with_counts 130, recordings 123, lesson_ladder 99, posture 92, arms_and_hands 81, formation 58
- QC gates: {'reject': 71, 'publish': 107, 'review': 72}
- Editor notes open: 0 · pages with editor-added sources: 0
- Movie phase: episode packs 106 (0 complete, 8 polished) · translations 6 across 12 languages · teaching playbook from 7 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to movie-ready (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- daggering (15/18): missing footwork_with_counts, tempo_or_meter, images
- humppa (15/17): missing lesson_ladder, images
- line-dance (15/18): missing posture, arms_and_hands, lesson_ladder
- moshing (15/18): missing tempo_or_meter, lesson_ladder, hooks
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- pungmul (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- semah-alevi-bektasi-ritual (15/18): missing posture, lesson_ladder, recordings
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, lesson_ladder
- the-running-man (15/18): missing lesson_ladder, hooks, images
- fleckerl (14/17): missing sound_description, recordings, images
- kurdish-dance (14/18): missing footwork_with_counts, tempo_or_meter, recordings, images
- los-voladores (14/18): missing footwork_with_counts, tempo_or_meter, lesson_ladder, recordings
- malaguenas (14/17): missing footwork_with_counts, arms_and_hands, images
- morna (14/18): missing footwork_with_counts, lesson_ladder, costume, images
- nightclub-two-step (14/18): missing lesson_ladder, costume, images, footage

- Tradition status (schema 5 records): {'living': 62, 'unknown': 4, 'historical': 6, 'revived': 2} · pages with reference footage links: 49

## Last runs
- **audit** 2026-11-03T17:08:39Z · {"retired_or_merged_total": 110}
- **discover** 2026-11-03T17:09:48Z · {"harvested": 3681, "already_known": 909, "dup_qid": 112, "dup_name": 110, "deferred": 1532, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-03T18:16:23Z · {"screened_out_move": 24, "researched_researched": 36, "researched_no_sources": 4, "llm_calls": 48, "llm_failures": 12, "llm_requests": 36, "llm_unanswered": 0}
- **qc** 2026-11-03T18:20:54Z · {"gate_publish": 20, "gate_reject": 11, "gate_review": 5, "llm_calls": 49, "llm_failures": 13, "llm_requests": 36, "llm_unanswered": 0}
- **hero_qc** 2026-11-03T18:30:50Z · {"videos_fetched": 141, "verdict_pass": 47, "verdict_fail": 13, "replaced": 6, "evicted_for_recrawl": 7, "llm_calls": 75, "llm_failures": 8, "llm_requests": 67, "llm_unanswered": 0}
- **build** 2026-11-03T18:31:08Z · {"retired_by_audit": 110, "new_rejected_hidden": 59, "new_publish": 69, "new_review_hidden": 36, "existing_research_rejected": 12, "existing_reject": 12, "existing_publish": 37, "existing_review": 36}
- **sync** 2026-11-03T18:45:02Z · {"inserted_publish": 20, "skipped_reject_new": 11, "inserted_review": 5}
- **report** 2026-11-02T21:19:33Z · {"review_items": 127}

# Dancing Atlas pipeline status
_Generated 2026-11-04T19:24:43Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **825** · with hero video: **710** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 19
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1159 · statuses: {'qc_replaced': 80, 'crowd_wisdom_confident': 910, 'qc_failed_pending_recrawl': 61, 'crowd_wisdom_weak': 108}
- Hero QC verdicts: {'pass': 395, 'fail': 61} (checked 456)

## Discovery → research → QC
- Candidates: {'researched': 190, 'duplicate_of': 17, 'queued': 163, 'screened_out': 32}
- Research index: {'researched': 279, 'llm_failed': 3, 'no_sources': 25}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 58 of 279 researched
- What classes still lack most (count of researched pages missing it): images 167, footwork_with_counts 159, tempo_or_meter 155, recordings 151, posture 109, lesson_ladder 106, arms_and_hands 98, costume 73
- QC gates: {'reject': 79, 'publish': 126, 'review': 81}
- Editor notes open: 0 · pages with editor-added sources: 0
- Movie phase: episode packs 125 (0 complete, 12 polished) · translations 12 across 12 languages · teaching playbook from 13 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

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

- Tradition status (schema 5 records): {'living': 93, 'unknown': 6, 'historical': 9, 'revived': 2} · pages with reference footage links: 67

## Last runs
- **audit** 2026-11-04T17:20:59Z · {"retired_or_merged_total": 110}
- **discover** 2026-11-04T17:22:03Z · {"harvested": 3681, "dup_qid": 112, "already_known": 949, "dup_name": 112, "deferred": 1490, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-04T18:35:12Z · {"screened_out_move": 1, "researched_researched": 36, "researched_no_sources": 4, "llm_calls": 48, "llm_failures": 12, "llm_requests": 36, "llm_unanswered": 0}
- **qc** 2026-11-04T18:45:18Z · {"gate_review": 9, "gate_reject": 8, "gate_publish": 19, "llm_calls": 51, "llm_failures": 15, "llm_requests": 36, "llm_unanswered": 0}
- **hero_qc** 2026-11-04T19:16:43Z · {"videos_fetched": 145, "verdict_pass": 43, "verdict_fail": 17, "replaced": 9, "evicted_for_recrawl": 8, "llm_calls": 87, "llm_failures": 13, "llm_requests": 74, "llm_unanswered": 0}
- **build** 2026-11-04T19:17:03Z · {"retired_by_audit": 110, "new_rejected_hidden": 66, "new_publish": 84, "new_review_hidden": 39, "existing_research_rejected": 13, "existing_reject": 13, "existing_publish": 41, "existing_review": 42}
- **sync** 2026-11-04T19:24:41Z · {"inserted_review": 9, "skipped_reject_new": 8, "inserted_publish": 19}
- **report** 2026-11-03T18:45:04Z · {"review_items": 143}

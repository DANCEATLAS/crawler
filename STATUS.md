# Dancing Atlas pipeline status
_Generated 2026-11-05T19:37:53Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **855** · with hero video: **732** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 19
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1172 · statuses: {'qc_replaced': 86, 'crowd_wisdom_confident': 899, 'qc_failed_pending_recrawl': 80, 'crowd_wisdom_weak': 107}
- Hero QC verdicts: {'pass': 436, 'fail': 80} (checked 516)

## Discovery → research → QC
- Candidates: {'researched': 215, 'duplicate_of': 17, 'queued': 178, 'screened_out': 32}
- Research index: {'researched': 316, 'llm_failed': 3, 'no_sources': 28}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 65 of 316 researched
- What classes still lack most (count of researched pages missing it): images 195, footwork_with_counts 188, tempo_or_meter 179, recordings 173, lesson_ladder 136, posture 135, arms_and_hands 121, costume 89
- QC gates: {'reject': 86, 'publish': 152, 'review': 85}
- Editor notes open: 0 · pages with editor-added sources: 0
- Movie phase: episode packs 151 (0 complete, 16 polished) · translations 18 across 12 languages · teaching playbook from 18 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to movie-ready (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- chinelos (16/18): missing tempo_or_meter, lesson_ladder
- daggering (15/18): missing footwork_with_counts, tempo_or_meter, images
- humppa (15/17): missing lesson_ladder, images
- line-dance (15/18): missing posture, arms_and_hands, lesson_ladder
- moshing (15/18): missing tempo_or_meter, lesson_ladder, hooks
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- pungmul (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- semah-alevi-bektasi-ritual (15/18): missing posture, lesson_ladder, recordings
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, lesson_ladder
- the-running-man (15/18): missing lesson_ladder, hooks, images
- vallenato (15/18): missing lesson_ladder, images, footage
- fleckerl (14/17): missing sound_description, recordings, images
- kurdish-dance (14/18): missing footwork_with_counts, tempo_or_meter, recordings, images
- los-voladores (14/18): missing footwork_with_counts, tempo_or_meter, lesson_ladder, recordings
- malaguenas (14/17): missing footwork_with_counts, arms_and_hands, images

- Tradition status (schema 5 records): {'living': 122, 'unknown': 11, 'historical': 11, 'revived': 3} · pages with reference footage links: 88

## Last runs
- **audit** 2026-11-05T17:27:53Z · {"retired_or_merged_total": 110}
- **discover** 2026-11-05T17:28:55Z · {"harvested": 3681, "already_known": 989, "dup_qid": 114, "dup_name": 111, "deferred": 1449, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-05T19:05:29Z · {"researched_researched": 37, "researched_no_sources": 3, "llm_calls": 47, "llm_failures": 10, "llm_requests": 37, "llm_unanswered": 0}
- **qc** 2026-11-05T19:11:41Z · {"gate_publish": 26, "gate_review": 4, "gate_reject": 7, "llm_calls": 49, "llm_failures": 12, "llm_requests": 37, "llm_unanswered": 0}
- **hero_qc** 2026-11-05T19:21:36Z · {"videos_fetched": 143, "verdict_pass": 35, "verdict_fail": 25, "replaced": 6, "evicted_for_recrawl": 19, "llm_calls": 100, "llm_failures": 16, "llm_requests": 84, "llm_unanswered": 0}
- **build** 2026-11-05T19:21:50Z · {"retired_by_audit": 110, "new_rejected_hidden": 70, "new_publish": 102, "new_review_hidden": 42, "existing_research_rejected": 16, "existing_reject": 16, "existing_publish": 49, "existing_review": 43}
- **sync** 2026-11-05T19:37:51Z · {"inserted_publish": 26, "inserted_review": 4, "skipped_reject_new": 7}
- **report** 2026-11-04T19:24:43Z · {"review_items": 160}

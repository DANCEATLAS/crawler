# Dancing Atlas pipeline status
_Generated 2026-11-09T21:56:24Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **957** · with hero video: **810** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1223 · statuses: {'qc_replaced': 123, 'crowd_wisdom_confident': 889, 'qc_failed_pending_recrawl': 104, 'crowd_wisdom_weak': 107}
- Hero QC verdicts: {'pass': 652, 'fail': 104} (checked 756)

## Discovery → research → QC
- Candidates: {'researched': 315, 'duplicate_of': 17, 'queued': 237, 'screened_out': 33}
- Research index: {'researched': 447, 'llm_failed': 3, 'no_sources': 42}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 96 of 447 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 309, images 295, tempo_or_meter 279, recordings 277, lesson_ladder 221, posture 218, arms_and_hands 202, formation 146
- QC gates: {'reject': 117, 'publish': 234, 'review': 103}
- Editor notes open: 0 · pages with editor-added sources: 6
- Movie phase: episode packs 231 (0 complete, 4 polished) · translations 6 across 12 languages · teaching playbook from 40 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to movie-ready (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- pungmul (16/18): missing footwork_with_counts, recordings
- daggering (15/18): missing footwork_with_counts, tempo_or_meter, images
- humppa (15/17): missing lesson_ladder, images
- iranian-dance (15/18): missing formation, lesson_ladder, recordings
- line-dance (15/18): missing posture, arms_and_hands, lesson_ladder
- moshing (15/18): missing tempo_or_meter, lesson_ladder, hooks
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- semah-alevi-bektasi-ritual (15/18): missing posture, lesson_ladder, recordings
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, lesson_ladder
- the-running-man (15/18): missing lesson_ladder, hooks, images
- zambra (15/18): missing footwork_with_counts, lesson_ladder, images
- australian-dance (14/18): missing posture, tempo_or_meter, lesson_ladder, images
- danza-de-los-diablos (14/18): missing tempo_or_meter, lesson_ladder, recordings, images

- Tradition status (schema 5 records): {'living': 236, 'unknown': 29, 'historical': 18, 'revived': 3} · pages with reference footage links: 155

## Last runs
- **audit** 2026-11-09T19:53:33Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-09T19:55:16Z · {"harvested": 3682, "already_known": 1149, "dup_qid": 116, "dup_name": 116, "deferred": 1282, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-09T21:16:15Z · {"screened_out_move": 1, "researched_researched": 40, "llm_calls": 54, "llm_failures": 14, "llm_requests": 40, "llm_unanswered": 0}
- **qc** 2026-11-09T21:24:39Z · {"gate_publish": 25, "gate_reject": 8, "gate_review": 7, "llm_calls": 50, "llm_failures": 10, "llm_requests": 40, "llm_unanswered": 0}
- **hero_qc** 2026-11-09T21:46:41Z · {"videos_fetched": 147, "verdict_pass": 45, "verdict_fail": 15, "evicted_for_recrawl": 7, "replaced": 8, "llm_calls": 81, "llm_failures": 8, "llm_requests": 73, "llm_unanswered": 0}
- **build** 2026-11-09T21:46:56Z · {"retired_by_audit": 122, "new_rejected_hidden": 92, "new_publish": 155, "new_review_hidden": 52, "existing_research_rejected": 25, "existing_reject": 25, "existing_publish": 68, "existing_review": 41}
- **sync** 2026-11-09T21:56:22Z · {"patched": 14, "patch_nomatch": 1, "skipped_reject_new": 7, "inserted_publish": 12, "inserted_review": 7}
- **report** 2026-11-08T17:31:28Z · {"review_items": 211}

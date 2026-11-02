# Dancing Atlas pipeline status
_Generated 2026-11-02T21:19:33Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **772** · with hero video: **674** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 19
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1139 · statuses: {'qc_replaced': 65, 'crowd_wisdom_confident': 922, 'qc_failed_pending_recrawl': 46, 'crowd_wisdom_weak': 106}
- Hero QC verdicts: {'pass': 290, 'fail': 46} (checked 336)

## Discovery → research → QC
- Candidates: {'researched': 140, 'duplicate_of': 17, 'queued': 158, 'screened_out': 7}
- Research index: {'researched': 207, 'llm_failed': 3, 'no_sources': 17}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 42 of 207 researched
- What classes still lack most (count of researched pages missing it): images 121, tempo_or_meter 108, footwork_with_counts 99, recordings 99, lesson_ladder 71, posture 69, arms_and_hands 63, sound_description 49
- QC gates: {'reject': 60, 'publish': 87, 'review': 67}
- Editor notes open: 0 · pages with editor-added sources: 0

## Closest to movie-ready (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- humppa (15/17): missing lesson_ladder, images
- moshing (15/18): missing tempo_or_meter, lesson_ladder, hooks
- pungmul (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- semah-alevi-bektasi-ritual (15/18): missing posture, lesson_ladder, recordings
- fleckerl (14/17): missing sound_description, recordings, images
- kurdish-dance (14/18): missing footwork_with_counts, tempo_or_meter, recordings, images
- malaguenas (14/17): missing footwork_with_counts, arms_and_hands, images
- morna (14/18): missing footwork_with_counts, lesson_ladder, costume, images
- nightclub-two-step (14/18): missing lesson_ladder, costume, images, footage
- schafflertanz (14/18): missing posture, tempo_or_meter, lesson_ladder, images
- zafin (14/18): missing posture, arms_and_hands, lesson_ladder, recordings
- azerbaijani-folk-dance (13/17): missing footwork_with_counts, tempo_or_meter, lesson_ladder, recordings
- danza-de-la-botella (13/17): missing tempo_or_meter, sound_description, recordings, images
- korean-dance (13/18): missing footwork_with_counts, arms_and_hands, tempo_or_meter, lesson_ladder, recordings
- melbourne-shuffle (13/17): missing posture, instruments, lesson_ladder, images

- Tradition status (schema 5 records): {'living': 29, 'unknown': 4, 'historical': 4, 'revived': 1} · pages with reference footage links: 27

## Last runs
- **audit** 2026-11-02T19:34:11Z · {"retired_or_merged_total": 110}
- **discover** 2026-11-02T19:35:38Z · {"harvested": 3681, "dup_qid": 112, "already_known": 869, "dup_name": 107, "deferred": 1575, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-02T21:07:58Z · {"screened_out_move": 7, "researched_researched": 34, "researched_no_sources": 6, "llm_calls": 44, "llm_failures": 10}
- **qc** 2026-11-02T21:14:15Z · {"gate_review": 13, "gate_reject": 8, "gate_publish": 13, "llm_calls": 45}
- **hero_qc** 2026-11-02T21:18:26Z · {"videos_fetched": 134, "verdict_pass": 39, "verdict_fail": 21, "evicted_for_recrawl": 10, "replaced": 11, "llm_calls": 87}
- **build** 2026-11-02T21:18:44Z · {"retired_by_audit": 110, "new_rejected_hidden": 50, "new_publish": 55, "new_review_hidden": 34, "existing_research_rejected": 10, "existing_reject": 10, "existing_publish": 31, "existing_review": 33}
- **sync** 2026-11-02T21:19:31Z · {"inserted_review": 13, "skipped_reject_new": 8, "inserted_publish": 13}
- **report** 2026-11-02T14:53:45Z · {"review_items": 110}

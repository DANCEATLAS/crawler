# Dancing Atlas pipeline status
_Generated 2026-11-02T14:53:45Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **746** · with hero video: **646** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 18
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1119 · statuses: {'qc_replaced': 54, 'crowd_wisdom_confident': 917, 'qc_failed_pending_recrawl': 36, 'crowd_wisdom_weak': 112}
- Hero QC verdicts: {'pass': 240, 'fail': 36} (checked 276)

## Discovery → research → QC
- Candidates: {'researched': 115, 'duplicate_of': 17, 'queued': 150}
- Research index: {'researched': 183, 'llm_failed': 3, 'no_sources': 11}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 35 of 183 researched
- What classes still lack most (count of researched pages missing it): images 97, tempo_or_meter 94, recordings 90, footwork_with_counts 84, posture 57, arms_and_hands 55, lesson_ladder 53, sound_description 47
- QC gates: {'reject': 56, 'publish': 74, 'review': 54}
- Editor notes open: 0 · pages with editor-added sources: 0

## Closest to movie-ready (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- humppa (15/17): missing lesson_ladder, images
- pungmul (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- fleckerl (14/17): missing sound_description, recordings, images
- kurdish-dance (14/18): missing footwork_with_counts, tempo_or_meter, recordings, images
- malaguenas (14/17): missing footwork_with_counts, arms_and_hands, images
- azerbaijani-folk-dance (13/17): missing footwork_with_counts, tempo_or_meter, lesson_ladder, recordings
- danza-de-la-botella (13/17): missing tempo_or_meter, sound_description, recordings, images
- melbourne-shuffle (13/17): missing posture, instruments, lesson_ladder, images
- american-tribal-style-belly-dance (12/17): missing footwork_with_counts, arms_and_hands, tempo_or_meter, recordings, images
- clogging (12/17): missing footwork_with_counts, arms_and_hands, tempo_or_meter, lesson_ladder, recordings
- intore (12/17): missing tempo_or_meter, lesson_ladder, recordings, images, connections
- pangalay (12/17): missing footwork_with_counts, formation, tempo_or_meter, costume, images
- right-and-left-grand (12/17): missing instruments, sound_description, notable_figures, recordings, images
- sekete (12/17): missing footwork_with_counts, arms_and_hands, tempo_or_meter, costume, recordings
- singkil (12/17): missing footwork_with_counts, posture, tempo_or_meter, lesson_ladder, recordings

- Tradition status (schema 5 records): {'living': 4} · pages with reference footage links: 3

## Last runs
- **audit** 2026-11-02T14:31:57Z · {"retired_or_merged_total": 110}
- **discover** 2026-11-02T14:33:48Z · {"harvested": 3681, "already_known": 864, "dup_name": 107, "dup_qid": 112, "deferred": 1615, "not_dance_like": 10, "queued_new": 5}
- **research** 2026-11-02T14:46:59Z · {"researched_researched": 4, "researched_no_sources": 1, "llm_calls": 13, "llm_failures": 9}
- **qc** 2026-11-02T14:51:34Z · {"gate_reject": 55, "gate_publish": 74, "gate_review": 54, "llm_calls": 10}
- **hero_qc** 2026-11-02T14:51:59Z · {"videos_fetched": 11, "verdict_fail": 2, "replaced": 2, "verdict_pass": 3, "llm_calls": 14}
- **build** 2026-11-02T14:52:18Z · {"retired_by_audit": 110, "new_rejected_hidden": 44, "new_publish": 45, "new_review_hidden": 25, "existing_research_rejected": 12, "existing_reject": 12, "existing_publish": 28, "existing_review": 29}
- **sync** 2026-11-02T14:53:44Z · {"skipped_reject_new": 52, "patched": 89, "patch_nomatch": 32, "inserted_review": 6, "inserted_publish": 4}
- **report** 2026-11-01T18:03:27Z · {"review_items": 113}

## Recent errors (last 12 runs)
- edges wheelchair-dancesport: HTTP 500 https://maojpsywvbksrwkrxmjx.supabase.co/rest/v1/dance_edges?on_conflict=src_id,dst_id,relation :: {"code":"21000","details":null,"hint":"Ensure that no rows proposed for insertion within the same command have duplicate constrained values.","message":"ON CONF
- edges zapin: HTTP 500 https://maojpsywvbksrwkrxmjx.supabase.co/rest/v1/dance_edges?on_conflict=src_id,dst_id,relation :: {"code":"21000","details":null,"hint":"Ensure that no rows proposed for insertion within the same command have duplicate constrained values.","message":"ON CONF

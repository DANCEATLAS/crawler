# Dancing Atlas pipeline status
_Generated 2026-11-01T18:03:27Z · pipeline v3.2_

## Catalogue (Supabase)
- Dances: **736** · with hero video: **646** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 17
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1119 · statuses: {'qc_replaced': 52, 'crowd_wisdom_confident': 919, 'qc_failed_pending_recrawl': 36, 'crowd_wisdom_weak': 112}
- Hero QC verdicts: {'pass': 235, 'fail': 36} (checked 271)

## Discovery → research → QC
- Candidates: {'researched': 112, 'duplicate_of': 17, 'queued': 148}
- Research index: {'researched': 181, 'llm_failed': 3, 'no_sources': 10}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 34 of 181 researched
- What classes still lack most (count of researched pages missing it): images 96, tempo_or_meter 93, recordings 89, footwork_with_counts 83, posture 57, arms_and_hands 55, lesson_ladder 54, sound_description 47
- QC gates: {'reject': 62, 'publish': 68, 'review': 51}

## Last runs
- **audit** 2026-11-01T16:06:35Z · {"retired_or_merged_total": 110}
- **discover** 2026-11-01T16:07:34Z · {"harvested": 3766, "dup_qid": 111, "already_known": 887, "dup_name": 106, "deferred": 1630, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-01T17:37:50Z · {"researched_researched": 38, "researched_no_sources": 2, "llm_calls": 48, "llm_failures": 10}
- **qc** 2026-11-01T17:49:35Z · {"gate_review": 13, "gate_publish": 18, "gate_reject": 7, "llm_calls": 48}
- **hero_qc** 2026-11-01T18:02:16Z · {"videos_fetched": 132, "verdict_fail": 14, "replaced": 8, "verdict_pass": 46, "evicted_for_recrawl": 6, "llm_calls": 77}
- **build** 2026-11-01T18:02:29Z · {"retired_by_audit": 110, "new_rejected_hidden": 47, "new_publish": 39, "existing_research_rejected": 15, "existing_reject": 15, "existing_publish": 28, "existing_review": 26, "new_review_hidden": 25}
- **sync** 2026-11-01T18:03:26Z · {"skipped_reject_new": 8, "inserted_review": 13, "inserted_publish": 18} · errors: 2
- **report** 2026-10-31T16:46:46Z · {"review_items": 93}

## Recent errors (last 12 runs)
- edges wheelchair-dancesport: HTTP 500 https://maojpsywvbksrwkrxmjx.supabase.co/rest/v1/dance_edges?on_conflict=src_id,dst_id,relation :: {"code":"21000","details":null,"hint":"Ensure that no rows proposed for insertion within the same command have duplicate constrained values.","message":"ON CONF
- edges zapin: HTTP 500 https://maojpsywvbksrwkrxmjx.supabase.co/rest/v1/dance_edges?on_conflict=src_id,dst_id,relation :: {"code":"21000","details":null,"hint":"Ensure that no rows proposed for insertion within the same command have duplicate constrained values.","message":"ON CONF

# Dancing Atlas pipeline status
_Generated 2026-10-29T17:37:53Z · pipeline v3.2_

## Catalogue (Supabase)
- Dances: **665** · with hero video: **615** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 16
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 81 · judged: 962 of 1014

## Crawler
- Hero results on file: 1103 · statuses: {'qc_replaced': 15, 'crowd_wisdom_confident': 963, 'qc_failed_pending_recrawl': 9, 'crowd_wisdom_weak': 116}
- Hero QC verdicts: {'pass': 86, 'fail': 9} (checked 95)

## Discovery → research → QC
- Candidates: {'researched': 37, 'duplicate_of': 17, 'queued': 103}
- Research index: {'researched': 70, 'llm_failed': 8, 'no_sources': 8}
- QC gates: {'reject': 22, 'publish': 33, 'review': 15}

## Last runs
- **audit** 2026-10-29T16:14:21Z · {"retired_or_merged_total": 81}
- **discover** 2026-10-29T16:15:45Z · {"harvested": 3766, "already_known": 767, "dup_name": 102, "dup_qid": 106, "deferred": 1759, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-10-29T16:40:16Z · {"researched_researched": 27, "researched_no_sources": 3, "llm_calls": 41, "llm_failures": 14}
- **qc** 2026-10-29T17:04:44Z · {"gate_publish": 10, "gate_review": 9, "gate_reject": 8, "llm_calls": 35}
- **hero_qc** 2026-10-29T17:37:09Z · {"videos_fetched": 140, "verdict_pass": 48, "verdict_fail": 12, "evicted_for_recrawl": 5, "replaced": 7, "llm_calls": 87}
- **build** 2026-10-29T17:37:17Z · {"retired_by_audit": 81, "new_rejected_hidden": 14, "new_publish": 15, "existing_research_rejected": 8, "existing_reject": 8, "existing_publish": 18, "existing_review": 8, "new_review_hidden": 7}
- **sync** 2026-10-29T17:37:52Z · {"skipped_reject_new": 9, "inserted_publish": 10, "inserted_review": 9} · errors: 1
- **report** 2026-10-29T02:46:56Z · {"review_items": 20}

## Recent errors (last 12 runs)
- aliases urban-kiz: HTTP 500 https://maojpsywvbksrwkrxmjx.supabase.co/rest/v1/dance_aliases?on_conflict=dance_id,alias :: {"code":"21000","details":null,"hint":"Ensure that no rows proposed for insertion within the same command have duplicate constrained values.","message":"ON CONF

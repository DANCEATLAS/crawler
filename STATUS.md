# Dancing Atlas pipeline status
_Generated 2026-10-30T18:22:07Z · pipeline v3.2_

## Catalogue (Supabase)
- Dances: **683** · with hero video: **625** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 16
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1107 · statuses: {'qc_replaced': 28, 'crowd_wisdom_confident': 946, 'qc_failed_pending_recrawl': 21, 'crowd_wisdom_weak': 112}
- Hero QC verdicts: {'pass': 130, 'fail': 21} (checked 151)

## Discovery → research → QC
- Candidates: {'researched': 62, 'duplicate_of': 17, 'queued': 118}
- Research index: {'researched': 103, 'llm_failed': 3, 'no_sources': 8}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 9 of 103 researched
- What classes still lack most (count of researched pages missing it): tempo_or_meter 35, recordings 32, images 32, footwork_with_counts 28, lesson_ladder 27, posture 25, arms_and_hands 20, instruments 18
- QC gates: {'reject': 37, 'publish': 40, 'review': 26}

## Last runs
- **audit** 2026-10-30T15:59:43Z · {"retired_or_merged_total": 110}
- **discover** 2026-10-30T16:00:59Z · {"harvested": 3766, "already_known": 807, "dup_qid": 107, "dup_name": 103, "deferred": 1717, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-10-30T17:52:50Z · {"researched_researched": 40, "llm_calls": 56, "llm_failures": 16}
- **qc** 2026-10-30T18:07:43Z · {"gate_review": 11, "gate_publish": 7, "gate_reject": 22, "llm_calls": 49}
- **hero_qc** 2026-10-30T18:21:24Z · {"videos_fetched": 133, "verdict_fail": 25, "replaced": 13, "verdict_pass": 35, "evicted_for_recrawl": 12, "llm_calls": 89}
- **build** 2026-10-30T18:21:32Z · {"retired_by_audit": 110, "new_rejected_hidden": 29, "new_publish": 19, "existing_research_rejected": 8, "existing_reject": 8, "existing_publish": 20, "existing_review": 13, "new_review_hidden": 13}
- **sync** 2026-10-30T18:22:06Z · {"skipped_reject_new": 22, "inserted_publish": 7, "inserted_review": 11}
- **report** 2026-10-29T17:37:53Z · {"review_items": 37}

## Recent errors (last 12 runs)
- aliases urban-kiz: HTTP 500 https://maojpsywvbksrwkrxmjx.supabase.co/rest/v1/dance_aliases?on_conflict=dance_id,alias :: {"code":"21000","details":null,"hint":"Ensure that no rows proposed for insertion within the same command have duplicate constrained values.","message":"ON CONF

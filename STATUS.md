# Dancing Atlas pipeline status
_Generated 2026-10-28T06:41:40Z · pipeline v3.0_

## Catalogue (Supabase)
- Dances: **624** · with hero video: **593** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 15
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 67 · judged: 384 of 1014

## Crawler
- Hero results on file: 1008 · statuses: {'crowd_wisdom_confident': 903, 'crowd_wisdom_weak': 100, 'qc_replaced': 3, 'qc_failed_pending_recrawl': 2}
- Hero QC verdicts: {'pass': 33, 'fail': 2} (checked 35)

## Discovery → research → QC
- Candidates: {'queued': 36, 'researched': 4, 'duplicate_of': 16}
- Research index: {'llm_failed': 4, 'researched': 10, 'no_sources': 2}
- QC gates: {'reject': 1, 'review': 9}

## Last runs
- **audit** 2026-10-28T06:22:42Z · {"judge_retire": 25, "judge_keep": 206, "judge_review_capped": 17, "retired_or_merged_total": 67}
- **discover** 2026-10-28T06:32:20Z · {"harvested": 2131, "already_known": 565, "dup_qid": 2, "dup_name": 113, "deferred": 1371, "dup_fuzzy": 9, "not_dance_like": 10, "queued_new": 20}
- **research** 2026-10-28T06:35:26Z · {"researched_llm_failed": 2, "researched_researched": 10, "llm_calls": 28, "llm_failures": 18}
- **qc** 2026-10-28T06:35:57Z · {"gate_reject": 1, "gate_review": 9, "llm_calls": 27}
- **hero_qc** 2026-10-28T06:41:15Z · {"videos_fetched": 47, "verdict_pass": 15, "verdict_fail": 5, "replaced": 3, "evicted_for_recrawl": 2, "llm_calls": 43}
- **build** 2026-10-28T06:41:27Z · {"retired_by_audit": 67, "new_rejected_hidden": 1, "new_review_hidden": 3, "existing_review": 6}
- **sync** 2026-10-28T06:41:39Z · {"skipped_reject_new": 1, "inserted_review": 9}
- **report** 2026-10-28T03:54:19Z · {"review_items": 0}

## Recent errors (last 12 runs)
- app_catalog.json missing — run bootstrap first

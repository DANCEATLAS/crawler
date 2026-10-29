# Dancing Atlas pipeline status
_Generated 2026-10-29T02:46:56Z · pipeline v3.2_

## Catalogue (Supabase)
- Dances: **646** · with hero video: **596** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 16
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 81 · judged: 962 of 1014

## Crawler
- Hero results on file: 1088 · statuses: {'qc_replaced': 8, 'crowd_wisdom_confident': 961, 'qc_failed_pending_recrawl': 4, 'crowd_wisdom_weak': 115}
- Hero QC verdicts: {'pass': 91, 'fail': 4} (checked 95)

## Discovery → research → QC
- Candidates: {'researched': 22, 'duplicate_of': 17, 'queued': 78}
- Research index: {'researched': 43, 'llm_failed': 8, 'no_sources': 5}
- QC gates: {'reject': 14, 'publish': 23, 'review': 6}

## Last runs
- **audit** 2026-10-29T02:35:18Z · {"judge_keep": 74, "judge_review_category": 2, "judge_retire": 2, "retired_or_merged_total": 81}
- **discover** 2026-10-29T02:36:27Z · {"harvested": 3764, "dup_qid": 107, "already_known": 757, "deferred": 1797, "dup_name": 101, "not_dance_like": 10, "queued_new": 10}
- **research** 2026-10-29T02:42:30Z · {"researched_researched": 9, "researched_no_sources": 1, "llm_calls": 15, "llm_failures": 6}
- **qc** 2026-10-29T02:43:22Z · {"gate_reject": 6, "gate_publish": 3, "gate_review": 1, "llm_calls": 14}
- **hero_qc** 2026-10-29T02:46:34Z · {"videos_fetched": 27, "verdict_fail": 4, "replaced": 2, "verdict_pass": 6, "evicted_for_recrawl": 2, "llm_calls": 18}
- **build** 2026-10-29T02:46:45Z · {"retired_by_audit": 81, "new_rejected_hidden": 10, "new_publish": 9, "existing_research_rejected": 4, "existing_reject": 4, "existing_publish": 14, "existing_review": 4, "new_review_hidden": 2}
- **sync** 2026-10-29T02:46:55Z · {"patched": 1, "skipped_reject_new": 6, "inserted_publish": 2, "inserted_review": 1}
- **report** 2026-10-29T02:04:28Z · {"review_items": 14}

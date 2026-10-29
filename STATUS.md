# Dancing Atlas pipeline status
_Generated 2026-10-29T01:46:46Z · pipeline v3.1_

## Catalogue (Supabase)
- Dances: **642** · with hero video: **596** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 16
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 78 · judged: 742 of 1014

## Crawler
- Hero results on file: 1088 · statuses: {'crowd_wisdom_confident': 966, 'crowd_wisdom_weak': 115, 'qc_replaced': 5, 'qc_failed_pending_recrawl': 2}
- Hero QC verdicts: {'pass': 93, 'fail': 2} (checked 95)

## Discovery → research → QC
- Candidates: {'queued': 68, 'researched': 17, 'duplicate_of': 17}
- Research index: {'llm_failed': 9, 'researched': 33, 'no_sources': 4}
- QC gates: {'reject': 8, 'review': 8, 'publish': 17}

## Last runs
- **audit** 2026-10-29T01:42:48Z · {"judge_retire_reopened": 19, "judge_keep": 278, "judge_review_category": 6, "judge_retire": 8, "retired_or_merged_total": 78}
- **discover** 2026-10-29T01:44:07Z · {"harvested": 3764, "already_known": 746, "deferred": 1814, "dup_name": 100, "dup_qid": 106, "dup_fuzzy": 1, "not_dance_like": 10, "queued_new": 5}
- **research** 2026-10-29T01:44:42Z · {"researched_llm_failed": 3, "researched_researched": 1, "llm_calls": 15, "llm_failures": 14}
- **qc** 2026-10-29T01:45:43Z · {"gate_reject": 8, "gate_review": 8, "gate_publish": 17, "llm_calls": 49}
- **hero_qc** 2026-10-29T01:45:51Z · {"vision_pending_requeued": 78, "videos_fetched": 15, "verdict_pass": 5, "vision_pending": 4, "llm_calls": 18}
- **build** 2026-10-29T01:46:08Z · {"retired_by_audit": 78, "new_rejected_hidden": 7, "new_review_hidden": 5, "existing_research_rejected": 1, "existing_reject": 1, "existing_publish": 13, "existing_review": 3, "new_publish": 4}
- **sync** 2026-10-29T01:46:44Z · {"patched": 21, "patch_nomatch": 2, "skipped_reject_new": 5, "inserted_publish": 2}
- **report** 2026-10-28T16:33:47Z · {"review_items": 32}

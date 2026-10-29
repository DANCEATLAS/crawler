# Dancing Atlas pipeline status
_Generated 2026-10-29T02:04:28Z · pipeline v3.2_

## Catalogue (Supabase)
- Dances: **643** · with hero video: **596** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 16
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 79 · judged: 884 of 1014

## Crawler
- Hero results on file: 1088 · statuses: {'crowd_wisdom_confident': 965, 'qc_replaced': 6, 'crowd_wisdom_weak': 115, 'qc_failed_pending_recrawl': 2}
- Hero QC verdicts: {'pass': 93, 'fail': 2} (checked 95)

## Discovery → research → QC
- Candidates: {'queued': 73, 'researched': 17, 'duplicate_of': 17}
- Research index: {'llm_failed': 10, 'researched': 34, 'no_sources': 4}
- QC gates: {'reject': 8, 'review': 6, 'publish': 20}

## Last runs
- **audit** 2026-10-29T01:58:54Z · {"judge_keep": 140, "judge_retire": 1, "judge_review_category": 1, "retired_or_merged_total": 79}
- **discover** 2026-10-29T01:59:41Z · {"harvested": 3764, "already_known": 752, "deferred": 1808, "dup_qid": 106, "dup_name": 101, "not_dance_like": 10, "queued_new": 5}
- **research** 2026-10-29T01:59:57Z · {"researched_llm_failed": 3, "researched_researched": 1, "llm_calls": 13, "llm_failures": 12}
- **qc** 2026-10-29T02:01:34Z · {"gate_reject": 8, "gate_review": 6, "gate_publish": 20, "llm_calls": 42}
- **hero_qc** 2026-10-29T02:03:57Z · {"videos_fetched": 15, "verdict_pass": 4, "vision_pending": 2, "verdict_fail": 1, "replaced": 1, "llm_calls": 15}
- **build** 2026-10-29T02:04:05Z · {"retired_by_audit": 79, "new_rejected_hidden": 7, "new_review_hidden": 3, "new_publish": 6, "existing_research_rejected": 1, "existing_reject": 1, "existing_publish": 14, "existing_review": 3}
- **sync** 2026-10-29T02:04:27Z · {"skipped_reject_new": 6, "patched": 25, "patch_nomatch": 2, "inserted_publish": 1}
- **report** 2026-10-29T01:46:46Z · {"review_items": 16}

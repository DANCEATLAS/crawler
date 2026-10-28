# Dancing Atlas pipeline status
_Generated 2026-10-28T16:33:47Z · pipeline v3.0_

## Catalogue (Supabase)
- Dances: **640** · with hero video: **596** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 15
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 85 · judged: 464 of 1014

## Crawler
- Hero results on file: 1088 · statuses: {'crowd_wisdom_confident': 966, 'crowd_wisdom_weak': 115, 'qc_replaced': 5, 'qc_failed_pending_recrawl': 2}
- Hero QC verdicts: {'pass': 93, 'fail': 2} (checked 95)

## Discovery → research → QC
- Candidates: {'queued': 63, 'researched': 17, 'duplicate_of': 16}
- Research index: {'llm_failed': 8, 'researched': 32, 'no_sources': 4}
- QC gates: {'reject': 7, 'review': 25}

## Last runs
- **audit** 2026-10-28T16:11:21Z · {"judge_retire": 18, "judge_keep": 62, "retired_or_merged_total": 85}
- **discover** 2026-10-28T16:21:45Z · {"harvested": 2131, "already_known": 594, "dup_qid": 2, "dup_name": 114, "deferred": 1330, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-10-28T16:30:24Z · {"researched_llm_failed": 6, "researched_researched": 22, "researched_no_sources": 2, "llm_calls": 55, "llm_failures": 33}
- **qc** 2026-10-28T16:32:16Z · {"gate_reject": 6, "gate_review": 16, "llm_calls": 42}
- **hero_qc** 2026-10-28T16:33:01Z · {"videos_fetched": 142, "verdict_pass": 58, "verdict_fail": 2, "replaced": 2, "llm_calls": 33}
- **build** 2026-10-28T16:33:17Z · {"retired_by_audit": 85, "new_rejected_hidden": 7, "new_review_hidden": 9, "existing_review": 16}
- **sync** 2026-10-28T16:33:46Z · {"skipped_reject_new": 6, "inserted_review": 16}
- **report** 2026-10-28T06:41:40Z · {"review_items": 10}

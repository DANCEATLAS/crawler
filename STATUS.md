# Dancing Atlas pipeline status
_Generated 2026-10-31T16:46:46Z · pipeline v3.2_

## Catalogue (Supabase)
- Dances: **705** · with hero video: **634** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 16
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 110 · judged: 929 of 1014

## Crawler
- Hero results on file: 1113 · statuses: {'qc_replaced': 44, 'crowd_wisdom_confident': 926, 'qc_failed_pending_recrawl': 30, 'crowd_wisdom_weak': 113}
- Hero QC verdicts: {'pass': 181, 'fail': 30} (checked 211)

## Discovery → research → QC
- Candidates: {'researched': 87, 'duplicate_of': 17, 'queued': 133}
- Research index: {'researched': 143, 'llm_failed': 3, 'no_sources': 8}
- Movie-ready (music DNA + movement DNA + episode brief from sources): 24 of 143 researched
- What classes still lack most (count of researched pages missing it): images 65, recordings 64, tempo_or_meter 62, footwork_with_counts 54, sound_description 38, instruments 36, posture 35, arms_and_hands 35
- QC gates: {'reject': 55, 'publish': 50, 'review': 38}

## Last runs
- **audit** 2026-10-31T15:23:20Z · {"retired_or_merged_total": 110}
- **discover** 2026-10-31T15:24:50Z · {"harvested": 3766, "already_known": 847, "dup_qid": 108, "dup_name": 104, "deferred": 1675, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-10-31T16:24:21Z · {"researched_researched": 40, "llm_calls": 53, "llm_failures": 13}
- **qc** 2026-10-31T16:29:15Z · {"gate_reject": 18, "gate_publish": 10, "gate_review": 12, "llm_calls": 51}
- **hero_qc** 2026-10-31T16:46:04Z · {"videos_fetched": 159, "verdict_pass": 35, "verdict_fail": 25, "evicted_for_recrawl": 9, "replaced": 16, "llm_calls": 102}
- **build** 2026-10-31T16:46:21Z · {"retired_by_audit": 110, "new_rejected_hidden": 44, "new_publish": 24, "existing_research_rejected": 11, "existing_reject": 11, "existing_publish": 25, "existing_review": 20, "new_review_hidden": 18}
- **sync** 2026-10-31T16:46:45Z · {"skipped_reject_new": 18, "inserted_publish": 10, "inserted_review": 12}
- **report** 2026-10-30T18:22:07Z · {"review_items": 63}

# Dancing Atlas pipeline status
_Generated 2026-11-16T22:24:06Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 5** · one item short: 9 · two short: 17 · published: 359 · in the atlas: 1155. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 47 profiles (2026-11-16).

## Catalogue (Supabase)
- Dances: **1160** · with hero video: **926** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1302 · statuses: {'qc_replaced': 201, 'crowd_wisdom_confident': 844, 'qc_failed_pending_recrawl': 171, 'crowd_wisdom_weak': 86}
- Hero QC verdicts: {'pass': 1065, 'fail': 171} (checked 1236)

## Discovery → research → QC
- Candidates: {'researched': 489, 'duplicate_of': 17, 'queued': 361, 'screened_out': 35}
- Research index: {'researched': 686, 'no_sources': 51, 'llm_failed': 20}
- Legacy presentation fields complete (not interactive readiness): 119 of 686 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 567, recordings 514, images 468, tempo_or_meter 451, lesson_ladder 406, posture 385, arms_and_hands 337, footage 281
- QC gates: {'reject': 152, 'publish': 370, 'review': 171}
- Active Profile dossiers: 1338; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 367 (0 complete, 4 polished) · translations 6 across 12 languages · teaching playbook from 91 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- indonesian-dance (16/18): missing footwork_with_counts, recordings
- pungmul (16/18): missing footwork_with_counts, recordings
- assamese-folk-dance (15/18): missing footwork_with_counts, recordings, footage
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- humppa (15/17): missing lesson_ladder, images
- jurit-ampil-kridha-warastra-dance (15/18): missing footwork_with_counts, recordings, footage
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- serbian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, instruments
- the-running-man (15/18): missing lesson_ladder, hooks, images
- twist (15/18): missing footwork_with_counts, lesson_ladder, images

- Tradition status (schema 5 records): {'living': 470, 'unknown': 37, 'historical': 29, 'revived': 6} · pages with reference footage links: 261

## Last runs
- **audit** 2026-11-16T19:40:54Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-16T19:41:42Z · {"harvested": 3690, "dup_qid": 116, "already_known": 1430, "dup_name": 122, "deferred": 980, "not_dance_like": 10, "queued_new": 60}
- **research** 2026-11-16T21:50:17Z · {"screened_out_move": 1, "researched_researched": 47, "researched_llm_failed": 19, "kept_existing": 2, "researched_no_sources": 2, "llm_calls": 96, "llm_failures": 40, "llm_requests": 68, "llm_unanswered": 12}
- **qc** 2026-11-16T21:54:13Z · {"gate_publish": 23, "gate_review": 23, "gate_reject": 4, "llm_calls": 45, "llm_failures": 9, "llm_requests": 50, "llm_unanswered": 15}
- **hero_qc** 2026-11-16T22:06:48Z · {"videos_fetched": 345, "verdict_fail": 32, "replaced": 22, "verdict_pass": 88, "evicted_for_recrawl": 9, "evicted_for_recrawl_removed": 1, "vision_pending": 40, "llm_calls": 129, "llm_failures": 11, "llm_requests": 157, "llm_unanswered": 40}
- **build** 2026-11-16T22:07:02Z · {"retired_by_audit": 122, "new_rejected_hidden": 118, "new_publish": 263, "new_review_hidden": 94, "existing_research_rejected": 34, "existing_reject": 34, "existing_publish": 96, "existing_review": 67}
- **sync** 2026-11-16T22:24:04Z · {"patch_nomatch": 4, "patched": 12, "inserted_publish": 14, "skipped_reject_new": 2, "inserted_review": 18}
- **report** 2026-11-15T18:07:00Z · {"review_items": 301}

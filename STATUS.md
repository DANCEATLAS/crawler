# Dancing Atlas pipeline status
_Generated 2026-11-15T18:07:00Z · pipeline v3.3_

## Catalogue (Supabase)
- Dances: **1128** · with hero video: **906** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1290 · statuses: {'qc_replaced': 179, 'crowd_wisdom_confident': 857, 'qc_failed_pending_recrawl': 161, 'crowd_wisdom_weak': 93}
- Hero QC verdicts: {'pass': 955, 'fail': 161} (checked 1116)

## Discovery → research → QC
- Candidates: {'researched': 465, 'duplicate_of': 17, 'queued': 326, 'screened_out': 34}
- Research index: {'researched': 650, 'llm_failed': 3, 'no_sources': 49}
- Legacy presentation fields complete (not interactive readiness): 111 of 650 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 525, recordings 477, images 438, tempo_or_meter 430, lesson_ladder 374, posture 363, arms_and_hands 315, footage 253
- QC gates: {'reject': 149, 'publish': 356, 'review': 152}
- Active Profile dossiers: 1323; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 353 (0 complete, 6 polished) · translations 6 across 12 languages · teaching playbook from 69 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

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

- Tradition status (schema 5 records): {'living': 431, 'unknown': 36, 'historical': 26, 'revived': 6} · pages with reference footage links: 246

## Last runs
- **audit** 2026-11-15T16:26:14Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-15T16:27:10Z · {"harvested": 3687, "already_known": 1389, "dup_name": 121, "dup_qid": 116, "deferred": 1040, "not_dance_like": 10, "queued_new": 40}
- **research** 2026-11-15T17:52:51Z · {"researched_researched": 40, "llm_calls": 51, "llm_failures": 11, "llm_requests": 40, "llm_unanswered": 0}
- **qc** 2026-11-15T17:54:51Z · {"gate_publish": 29, "gate_reject": 5, "gate_review": 6, "llm_calls": 45, "llm_failures": 5, "llm_requests": 40, "llm_unanswered": 0}
- **hero_qc** 2026-11-15T18:01:05Z · {"videos_fetched": 151, "verdict_pass": 38, "verdict_fail": 22, "replaced": 8, "evicted_for_recrawl": 14, "llm_calls": 87, "llm_failures": 9, "llm_requests": 78, "llm_unanswered": 0}
- **build** 2026-11-15T18:01:31Z · {"retired_by_audit": 122, "new_rejected_hidden": 116, "new_publish": 248, "new_review_hidden": 85, "existing_research_rejected": 33, "existing_reject": 33, "existing_publish": 97, "existing_review": 57}
- **sync** 2026-11-15T18:06:58Z · {"patched": 5, "skipped_reject_new": 4, "inserted_publish": 25, "inserted_review": 6}
- **report** 2026-11-14T17:48:39Z · {"review_items": 290}

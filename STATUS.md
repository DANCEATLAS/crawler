# Dancing Atlas pipeline status
_Generated 2026-11-18T21:44:57Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 24** · one item short: 30 · two short: 21 · published: 412 · in the atlas: 1192. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 63 profiles (2026-11-18).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 455 · method studied: 32 lessons of 28 teachers · research notes with checked quotes: 18 of 66 topics and 8 papers · practices with two or more kinds of evidence: 17. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1222** · with hero video: **966** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1330 · statuses: {'qc_replaced': 228, 'crowd_wisdom_confident': 829, 'qc_failed_pending_recrawl': 193, 'crowd_wisdom_weak': 80}
- Hero QC verdicts: {'pass': 1136, 'fail': 194} (checked 1330)

## Discovery → research → QC
- Candidates: {'researched': 561, 'duplicate_of': 18, 'queued': 409, 'screened_out': 35}
- Research index: {'researched': 777, 'no_sources': 52, 'llm_failed': 7}
- Legacy presentation fields complete (not interactive readiness): 132 of 777 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 671, recordings 611, images 544, tempo_or_meter 523, lesson_ladder 493, posture 458, arms_and_hands 402, footage 346
- QC gates: {'reject': 191, 'publish': 423, 'review': 170}
- Active Profile dossiers: 1375; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 420 (0 complete, 5 polished) · translations 6 across 12 languages · teaching playbook from 131 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- indonesian-dance (16/18): missing footwork_with_counts, recordings
- pungmul (16/18): missing footwork_with_counts, recordings
- assamese-folk-dance (15/18): missing footwork_with_counts, recordings, footage
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- hand-jive (15/18): missing footwork_with_counts, lesson_ladder, images
- jurit-ampil-kridha-warastra-dance (15/18): missing footwork_with_counts, recordings, footage
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- serbian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, instruments
- the-running-man (15/18): missing lesson_ladder, hooks, images
- twist (15/18): missing footwork_with_counts, lesson_ladder, images

- Tradition status (schema 5 records): {'living': 571, 'unknown': 42, 'historical': 34, 'revived': 9} · pages with reference footage links: 310

## Last runs
- **audit** 2026-11-18T18:10:19Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-18T18:11:01Z · {"harvested": 3691, "already_known": 1550, "dup_qid": 116, "dup_name": 126, "deferred": 855, "not_dance_like": 10, "dup_fuzzy": 1, "queued_new": 60}
- **research** 2026-11-18T21:17:26Z · {"researched_llm_failed": 6, "researched_researched": 63, "researched_no_sources": 1, "llm_calls": 135, "llm_failures": 66, "llm_requests": 69, "llm_unanswered": 0}
- **qc** 2026-11-18T21:22:07Z · {"gate_publish": 33, "gate_review": 12, "gate_reject": 18, "llm_calls": 65, "llm_failures": 1, "llm_requests": 63, "llm_unanswered": 0}
- **hero_qc** 2026-11-18T21:23:38Z · {"videos_fetched": 40, "verdict_fail": 6, "evicted_for_recrawl": 3, "verdict_pass": 10, "replaced": 3, "llm_calls": 22, "llm_failures": 0, "llm_requests": 21, "llm_unanswered": 0}
- **build** 2026-11-18T21:23:52Z · {"retired_by_audit": 122, "new_rejected_hidden": 148, "new_publish": 300, "new_review_hidden": 99, "existing_research_rejected": 43, "existing_reject": 43, "existing_publish": 112, "existing_review": 61}
- **sync** 2026-11-18T21:44:55Z · {"patched": 19, "patch_nomatch": 1, "skipped_reject_new": 18, "inserted_publish": 17, "inserted_review": 9}
- **report** 2026-11-17T21:51:28Z · {"review_items": 339}

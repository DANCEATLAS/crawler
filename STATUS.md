# Dancing Atlas pipeline status
_Generated 2026-11-17T21:51:28Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 18** · one item short: 15 · two short: 13 · published: 391 · in the atlas: 1178. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 68 profiles (2026-11-17).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 376 · method studied: 22 lessons of 19 teachers · research notes with checked quotes: 15 of 66 topics and 6 papers · practices with two or more kinds of evidence: 10. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1196** · with hero video: **947** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 20
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1314 · statuses: {'qc_replaced': 225, 'crowd_wisdom_confident': 819, 'qc_failed_pending_recrawl': 190, 'crowd_wisdom_weak': 80}
- Hero QC verdicts: {'pass': 1123, 'fail': 191} (checked 1314)

## Discovery → research → QC
- Candidates: {'researched': 527, 'duplicate_of': 17, 'queued': 383, 'screened_out': 35}
- Research index: {'researched': 734, 'no_sources': 51, 'llm_failed': 3}
- Legacy presentation fields complete (not interactive readiness): 132 of 734 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 622, recordings 561, images 508, tempo_or_meter 487, lesson_ladder 443, posture 416, arms_and_hands 364, footage 317
- QC gates: {'reject': 173, 'publish': 402, 'review': 166}
- Active Profile dossiers: 1361; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 399 (0 complete, 5 polished) · translations 6 across 12 languages · teaching playbook from 112 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- indonesian-dance (16/18): missing footwork_with_counts, recordings
- pungmul (16/18): missing footwork_with_counts, recordings
- assamese-folk-dance (15/18): missing footwork_with_counts, recordings, footage
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- hand-jive (15/18): missing footwork_with_counts, lesson_ladder, images
- humppa (15/17): missing lesson_ladder, images
- jurit-ampil-kridha-warastra-dance (15/18): missing footwork_with_counts, recordings, footage
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- serbian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- siva-tau (15/18): missing footwork_with_counts, tempo_or_meter, instruments
- the-running-man (15/18): missing lesson_ladder, hooks, images

- Tradition status (schema 5 records): {'living': 525, 'unknown': 40, 'historical': 31, 'revived': 6} · pages with reference footage links: 285

## Last runs
- **audit** 2026-11-17T18:39:07Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-17T18:40:49Z · {"harvested": 3691, "dup_qid": 117, "already_known": 1490, "dup_name": 122, "deferred": 919, "not_dance_like": 10, "queued_new": 60}
- **research** 2026-11-17T20:48:03Z · {"researched_researched": 68, "researched_llm_failed": 2, "llm_calls": 132, "llm_failures": 62, "llm_requests": 70, "llm_unanswered": 0}
- **qc** 2026-11-17T20:54:19Z · {"gate_review": 20, "gate_reject": 21, "gate_publish": 42, "llm_calls": 88, "llm_failures": 4, "llm_requests": 83, "llm_unanswered": 0}
- **hero_qc** 2026-11-17T21:15:00Z · {"videos_fetched": 346, "verdict_fail": 44, "evicted_for_recrawl": 20, "verdict_pass": 74, "replaced": 24, "llm_calls": 182, "llm_failures": 18, "llm_requests": 163, "llm_unanswered": 0}
- **build** 2026-11-17T21:15:24Z · {"retired_by_audit": 122, "new_rejected_hidden": 131, "new_publish": 286, "new_review_hidden": 96, "existing_research_rejected": 42, "existing_reject": 42, "existing_publish": 105, "existing_review": 60}
- **sync** 2026-11-17T21:51:26Z · {"patch_nomatch": 11, "patched": 24, "inserted_publish": 24, "skipped_reject_new": 12, "inserted_review": 12}
- **report** 2026-11-16T22:24:06Z · {"review_items": 323}

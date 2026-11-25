# Dancing Atlas pipeline status
_Generated 2026-11-25T21:48:53Z · pipeline v3.3_

## The starting line
- **Active-ready profiles: 39** · one item short: 67 · two short: 59 · published: 631 · in the atlas: 1365. See ACTIVE_READY.md.
- Writing engine: on. Last research run wrote 65 profiles (2026-11-25).

## Teaching research (for the Best Dance Friend)
- Teachers ranked by learners' words: 673 · method studied: 117 lessons of 104 teachers · research notes with checked quotes: 57 of 80 topics and 24 papers · practices with two or more kinds of evidence: 29. See BDF_TEACHING_SYSTEM.md.

## Catalogue (Supabase)
- Dances: **1500** · with hero video: **1134** · content_ready: 0 · publish gate: 0 · sacred: 0 · UNESCO refs: 21
- Viral challenges: 154

## Catalogue audit
- Retired/merged: 137 · judged: 919 of 1014

## Crawler
- Hero results on file: 1443 · statuses: {'qc_replaced': 244, 'crowd_wisdom_confident': 885, 'qc_failed_pending_recrawl': 212, 'crowd_wisdom_weak': 102}
- Hero QC verdicts: {'pass': 1230, 'fail': 213} (checked 1443)

## Discovery → research → QC
- Candidates: {'researched': 813, 'duplicate_of': 21, 'queued': 573, 'screened_out': 39}
- Research index: {'researched': 1136, 'no_sources': 73, 'llm_failed': 3}
- Legacy presentation fields complete (not interactive readiness): 245 of 1136 researched
- What classes still lack most (count of researched pages missing it): footwork_with_counts 1036, recordings 955, images 840, tempo_or_meter 760, lesson_ladder 732, posture 679, arms_and_hands 585, footage 582
- QC gates: {'reject': 265, 'publish': 642, 'review': 236}
- Active Profile dossiers: 1548; ready for activation: 0; runtime active: 0. See ACTIVE_PROFILE_REPORT.md.
- Editor notes open: 0 · pages with editor-added sources: 6
- Presentation assets: episode packs 639 (0 complete, 6 polished) · translations 6 across 12 languages · teaching playbook from 341 lessons (`ULTIMATE_TEACHER.md`, `MOVIE_PHASE.md`)

## Closest to legacy presentation completeness (for the weekly editor pass: find the missing items, add sources to pipeline_state/sources_extra.json)

- neo-burlesque (17/18): missing footwork_with_counts
- indonesian-dance (16/18): missing footwork_with_counts, recordings
- assamese-folk-dance (15/18): missing footwork_with_counts, recordings, footage
- father-daughter-dance (15/18): missing footwork_with_counts, lesson_ladder, images
- finger-tutting (15/18): missing footwork_with_counts, recordings, images
- georgian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings
- gnawa (15/18): missing footwork_with_counts, posture, recordings
- hand-jive (15/18): missing footwork_with_counts, lesson_ladder, images
- mitote (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- oleg (15/18): missing footwork_with_counts, tempo_or_meter, recordings
- para-para (15/18): missing footwork_with_counts, lesson_ladder, images
- partner-dance (15/18): missing lesson_ladder, hooks, recordings
- pungmul (15/18): missing footwork_with_counts, hooks, recordings
- robot (15/18): missing footwork_with_counts, tempo_or_meter, images
- serbian-folk-dance (15/18): missing footwork_with_counts, lesson_ladder, recordings

- Tradition status (schema 5 records): {'living': 864, 'historical': 62, 'unknown': 81, 'revived': 23} · pages with reference footage links: 448

## Last runs
- **audit** 2026-11-25T19:24:13Z · {"retired_or_merged_total": 137}
- **discover** 2026-11-25T19:24:54Z · {"harvested": 3708, "already_known": 1975, "dup_qid": 117, "dup_name": 133, "not_dance_like": 10, "deferred": 435, "queued_new": 60}
- **research** 2026-11-25T20:46:33Z · {"researched_researched": 65, "researched_llm_failed": 2, "researched_no_sources": 3, "llm_calls": 115, "llm_failures": 55, "llm_requests": 60, "llm_unanswered": 0}
- **qc** 2026-11-25T20:58:15Z · {"gate_review": 17, "gate_publish": 28, "gate_reject": 13, "llm_calls": 71, "llm_failures": 12, "llm_requests": 58, "llm_unanswered": 1, "llm_unserved": 1}
- **hero_qc** 2026-11-25T21:00:44Z · {"videos_fetched": 37, "verdict_pass": 9, "verdict_fail": 5, "replaced": 3, "evicted_for_recrawl": 2, "llm_calls": 22, "llm_failures": 2, "llm_requests": 19, "llm_unanswered": 0}
- **build** 2026-11-25T21:01:22Z · {"retired_by_audit": 122, "new_rejected_hidden": 207, "new_publish": 473, "new_review_hidden": 138, "existing_research_rejected": 58, "existing_reject": 58, "existing_publish": 158, "existing_review": 88}
- **sync** 2026-11-25T21:48:51Z · {"patch_nomatch": 4, "patched": 5, "skipped_reject_new": 13, "inserted_review": 12, "inserted_publish": 24}
- **report** 2026-11-24T22:56:09Z · {"review_items": 472}

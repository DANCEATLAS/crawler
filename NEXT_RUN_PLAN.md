# Dance Atlas — next run, reconciled 11 November 2026

Start with `PRODUCT_VISION.md`, `AI_BRIEF.md` and `IMPLEMENTATION_LEDGER.md`. The owner asked to recover all earlier requests, find the existing backend and carry the complete vision into the next run. This checkpoint replaces the obsolete sign-in blocker; it does not replace the full V01–V18 requirements.

## Correct project map

| Service | Existing project | Verified purpose |
| --- | --- | --- |
| Supabase | https://supabase.com/dashboard/project/maojpsywvbksrwkrxmjx | Existing Dance Atlas backend; dashboard accessible and Healthy on 11 November. The confusing email-derived default name was changed to Dance Atlas on 11 November; project ID and connections are unchanged. |
| Lovable | https://lovable.dev/projects/f79f3666-564d-4799-befe-8b48d1f0a007 | Dance Atlas UI and instruction mirror. |
| GitHub | https://github.com/DANCEATLAS/crawler | Source of truth, content, scripts, capped workflows and weekly email. |
| Demonstration | https://dancingatlas.lovable.app | Existing demonstration, not launch authorization. |

Sunfeld is a separate project and is on hold. Do not create a replacement Dance Atlas project, reconnect the UI, enable billing, alter Sunfeld, or repeat the resolved sign-in request. Match project IDs rather than assuming display names are authoritative. Do not publish account email addresses or credentials in this repository.

## What the database inspection established

Read-only SQL in the owning dashboard on 11 November found 991 `dances`, 154 `viral_challenges`, and zero `viral_chart_rankings`. Counts are a dated snapshot, not all website content: Atlas reads its GitHub export.

The `viral_chart` view repeats the same catalogue across `all`, `year` and `month`, assigning `row_number()` by `origin_date DESC NULLS LAST, name`. Its `views` field is NULL. These are origin-date positions, not popularity measurements. `viral_scores`, `viral_chart_history` and `votes`, expected by `score_virals.py`, are absent. The real challenge table also lacks that script's `views`, `is_dance` and `danger_flag` columns. Do not describe a successful parent workflow as a healthy popularity chart.

`audit_log` occupies 567,517,184 bytes (about 541 MiB); `pg_database_size` was 586,517,651 bytes. Dashboard organization usage showed 601 / 500 MB, a different usage measure. The audit trigger runs after every insert, update and delete of `dances`; its function writes full old/new rows without a no-change condition. Existing video/tutorial push jobs PATCH saved results repeatedly. This is evidence of a growth risk; measure actual no-op proportions before claiming a fix or savings.

## Ordered work — Active Profile mission

1. **Continue Active Profile preparation.** Run the offline activation stage; read ACTIVE_PROFILE_REPORT.md and the per-profile research/video/rights/review/platform queues. Research missing mechanics and teaching units within existing enrichment caps. Preserve practitioner variants and sacred holds. Build the missing bounded Viral research adapter separately; never treat a challenge as an Atlas tradition just to reuse the research path.
2. **Operate the video and learning laboratory.** Compare independent teachers, record timestamped movement and distinctive methods, identify uncertainty and test a small representative set with qualified reviewers before expanding production. Review native language, accessibility and learner outcomes separately. No model certifies its own evidence.
3. **Solve the music pilot.** Follow MUSIC_STRATEGY.md: reference masterpieces, two distinct cleared/credible practice choices, permissions per intended use, musician review and costs. Identify candidates/owners without sending unsolicited messages. Purchases, outreach and contracts need their applicable authorization. Do not imply recreating music or an AI subscription clears rights.
4. **Track delivery technology and human BDF needs.** Primary-source recheck due 25 November in pipeline_state/technology_watch.json. Prepare modular voice/movement feedback, consented human matching, camera/split-screen shared practice, measured synchronization and optional AR. Benchmark real learning/latency/privacy/cost; no speculative delivery promises.
5. **Prevent unnecessary database growth.** Audit log is ~541 MiB. Measure and skip unchanged producer PATCH operations without purging history or weakening legitimate auditing. Retention/deletion or paid capacity is a separate decision.
6. **Repair Viral popularity end to end.** Current date-ordered view is not a popularity chart and scorer schema mismatches remain. Inspect UI/fallbacks, keep all records, expose insufficient-data states, design bounded observations and surface errors before altering consumers.
7. **Keep progress simple and ledgers synchronized.** The report code now includes the complete vision and separates readiness from scripts. Preserve the scheduled weekly email and duplicate guard; do not force-send. Update the dated status register, GitHub ledger, Lovable instructions and Supabase private AI context with verified outcomes after substantive work.

Current preparation uses 1,064 Atlas entries and 183 saved Viral entries (1,247 dossiers); Supabase's 154 Viral rows are a different, lagging mirror. There are zero approved interactive-ready profiles, zero cleared music choices and no deployed interactive runtime. The daily job generates dossiers, not those missing capabilities.

## Complete request coverage

| Vision IDs | Required continuation |
| --- | --- |
| V01–V02 | Welcoming discovery; regional, purpose, sacred/traditional, preservation, solo/pair/group and learning filters. |
| V03–V04 | BDF: chosen speaking style, personality, language and controllable private continuity; reviewed teaching responsive to voice and movement. |
| V05–V06 | Caregiver-led infancy, appropriate life stages and abilities; global classes, screen sharing, groups, consent, cultural preferences, schedules and reminders. |
| V07 | Future AR teachers, virtual dancers, stages and large formations built on validated instruction. |
| V08–V09 | First-class Viral culture, correct creator/music credit and honest measured rankings with bounded refresh. |
| V10–V11 | BDF-assisted practice, original challenges, outfits/backgrounds, group video creation, collaborator review and explicitly approved distribution. |
| V12–V14 | Deep sourced culture/history/spirituality, reusable movement and teaching assets, credible original music with documented rights. |
| V15–V16 | Minimal cost, independent scheduled growth, reusable assets, truthful monitoring, dated technology benchmarks and a simple full-vision weekly email. |
| V17–V18 | Exhaust useful independent work; ask only one simple unavoidable owner action. Keep GitHub, Lovable and Supabase responsibilities clear. |

## Run boundaries

The GitHub daily job grows content; the weekly job sends the report; the editorial playbook guides an AI maintenance session. These jobs do not autonomously implement new BDF/social/AR features just because this plan lists them. There is no verified Dance Atlas ChatGPT automation in the inspected task list. Do not invent a new schedule or claim an external Claude schedule was changed. Make progress within existing authorization, record verified results and the next concrete task, and leave purchases and launch under owner control.

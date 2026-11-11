# Dance Atlas — next run, reconciled 11 November 2026

Start with `PRODUCT_VISION.md`, `AI_BRIEF.md` and `IMPLEMENTATION_LEDGER.md`. The owner asked to recover all earlier requests, find the existing backend and carry the complete vision into the next run. This checkpoint replaces the obsolete sign-in blocker; it does not replace the full V01–V18 requirements.

## Correct project map

| Service | Existing project | Verified purpose |
| --- | --- | --- |
| Supabase | https://supabase.com/dashboard/project/maojpsywvbksrwkrxmjx | Existing Dance Atlas backend; dashboard accessible and Healthy on 11 November. The project still has an email-derived default display name, which caused the confusion. |
| Lovable | https://lovable.dev/projects/f79f3666-564d-4799-befe-8b48d1f0a007 | Dance Atlas UI and instruction mirror. |
| GitHub | https://github.com/DANCEATLAS/crawler | Source of truth, content, scripts, capped workflows and weekly email. |
| Demonstration | https://dancingatlas.lovable.app | Existing demonstration, not launch authorization. |

Sunfeld is a separate project and is on hold. Do not create a replacement Dance Atlas project, reconnect the UI, enable billing, alter Sunfeld, or repeat the resolved sign-in request. Match project IDs rather than assuming display names are authoritative. Do not publish account email addresses or credentials in this repository.

## What the database inspection established

Read-only SQL in the owning dashboard on 11 November found 991 `dances`, 154 `viral_challenges`, and zero `viral_chart_rankings`. Counts are a dated snapshot, not all website content: Atlas reads its GitHub export.

The `viral_chart` view repeats the same catalogue across `all`, `year` and `month`, assigning `row_number()` by `origin_date DESC NULLS LAST, name`. Its `views` field is NULL. These are origin-date positions, not popularity measurements. `viral_scores`, `viral_chart_history` and `votes`, expected by `score_virals.py`, are absent. The real challenge table also lacks that script's `views`, `is_dance` and `danger_flag` columns. Do not describe a successful parent workflow as a healthy popularity chart.

`audit_log` occupies 567,517,184 bytes (about 541 MiB); `pg_database_size` was 586,517,651 bytes. Dashboard organization usage showed 601 / 500 MB, a different usage measure. The audit trigger runs after every insert, update and delete of `dances`; its function writes full old/new rows without a no-change condition. Existing video/tutorial push jobs PATCH saved results repeatedly. This is evidence of a growth risk; measure actual no-op proportions before claiming a fix or savings.

## Ordered work

1. **Publish and verify the simpler report.** Use the tested digest and dated capability register. Preserve the existing Monday morning delivery, recipients, budget caps and duplicate guard. A preview is not proof of email delivery. Do not force-send an extra email for layout testing. Old generated report dates/history must stay intact until the real scheduled report runs.
2. **Prevent unnecessary database growth.** Inspect actual triggers and producer writes; compare relevant payload fields and avoid unchanged PATCH operations while preserving legitimate updates and audit evidence. Test empty, changed and unchanged payloads. Do not purge audit history or weaken auditing. Prepare any retention/archive proposal with a recoverable copy and explicit owner approval before permanent deletion or paid capacity.
3. **Repair Viral honestly, end to end.** Inspect the actual Lovable consumer and fallbacks before changing the view. Preserve all challenge records. Distinguish catalogue browsing from measured charts, expose dated coverage/insufficient-data states, and stop pretending origin dates measure this month. Design bounded observation snapshots, idempotent period counters and refresh retries within existing caps. Match code to the real schema; use a small reviewed migration only after compatibility is demonstrated. Surface scorer failures instead of swallowing them.
4. **Continue rigorous content and teaching preparation.** Target sourced gaps and underrepresented communities; preserve meaningful variants and sacred holds. Validate a small contrasting set of learning units before expensive production. Scripts, machine translation, quote matches and scores are not practitioner, language, rights or release approval.
5. **Carry every part of the vision forward.** Check the full table below on each editorial pass and maintain `pipeline_state/vision_status.json` with dated evidence. Resolve owner actions immediately when completed. Read back any Lovable instructions update without starting a build.

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

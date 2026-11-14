# Dance Atlas — implementation and platform ledger

Vision revision: **DA-VISION-2026-11-09-BDF**. Evidence baseline: repository `40e1154`, local review and Chrome inspection on 9 November 2026. Requirements are in `PRODUCT_VISION.md`; operations are in `AI_BRIEF.md`. Counts are dated snapshots. BDF means **Best Dance Friend**, the lifelong personal dance mentor at the center of the expanded vision.

## Platform responsibilities

| Platform | Responsibility | Rules |
| --- | --- | --- |
| [GitHub](https://github.com/DANCEATLAS/crawler) | Canonical vision, code, research, published catalogue, scripts, audit history and reports | Update this ledger with substantive changes; preserve contracts and reversible history |
| [GitHub Actions](https://github.com/DANCEATLAS/crawler/actions) | Content, video, Viral, report, watchdog and snapshot jobs | Keep budgets; inspect internal outcomes, not only parent status |
| [Lovable](https://lovable.dev/projects/f79f3666-564d-4799-befe-8b48d1f0a007) | UI and Project instructions mirror | No two-way GitHub sync without approval; no routine content changes through paid prompts |
| [Atlas](https://dancingatlas.lovable.app/atlas) | Demonstration catalogue and profiles | Published GitHub content with bundled fallback; no launch implied |
| [Viral](https://dancingatlas.lovable.app/viral) | Challenge/trend collection and chart interface | First-class branch; tradition-only exclusions must not erase valid challenges |
| [Supabase](https://supabase.com/dashboard/project/maojpsywvbksrwkrxmjx) | Catalogue mirror, Viral data/scores/history/votes and existing account features | Inspect actual schema/policies before migrations. No new sensor, child or social-data collection is authorized merely by a vision document |
| Configured model/source services | Research and media support | Secrets in GitHub Actions; existing free/prepaid limits; replaceable providers |

## Verified baseline and limitations

- Reviewed catalogue: **1,054 entries**, **217 published deep profiles**. Broader research also includes profiles not approved for publication.
- Reviewed scripts: **217 packs**, **zero gap-free packs**. Automated publication, quote matching and script assembly are not practitioner or release approval.
- Viral live UI: **154 entries**, eight category tabs, month/year/all-time tabs, creator text, music/context details, save/share and embedded media. This establishes that Viral exists, not that rankings or attributions are accurate.
- Latest displayed daily, weekly, crawler and push runs succeeded. The crawler workflow permits the score step to fail without failing its parent; inspect the scoring result itself before claiming chart health.
- Supabase dashboard required sign-in during this session. Dashboard-only schema, permissions and usage were not newly verified. No database changes were made.
- BDF memory/personality, evaluated movement feedback, validated personalized animation, global classrooms, collaborative video production/distribution and AR have not been established as implemented by this review.

## Requirements mapped to current work

| Vision IDs | Current evidence | Next useful work |
| --- | --- | --- |
| V01–V02 discovery | Atlas browsing and Viral categories exist; complete conversational/filter model does not | Validate taxonomy for purposes, communities, multiple origins, preservation and participation format |
| V03 responsive teaching | Research and draft script ingredients | Learning-unit contract and benchmark before bounded adaptive planning |
| V04 BDF/languages | Narrator briefs and translation pipeline; no implemented lifelong personal mentor established | Define private preference/progress memory, controls, native review and configurable presentation independently of knowledge |
| V05–V06 life stages/community | Expanded requirements | Caregiver-led design for infancy; age-specific instruction, consent, scheduling and moderation before launch |
| V07 AR | Destination only in this review | Spatial metadata and task-based device evaluation after instruction is sound |
| V08–V11 Viral creation/distribution | Live collection, crawler and score job; complete studio is not built | Correct ranking/freshness, credit/music records; then reviewed practice and co-creation/export contracts |
| V12 research/culture | Discovery, audit, quote checks, independent judge and sacred holds | Claim-to-sentence support and teaching coverage; evidence-led alias/geography corrections |
| V13 assets/units | Schema 5 profiles and e1 packs at baseline | Trial reusable motion/teaching/creative asset contracts on contrasting forms |
| V14 music | Musical briefs and reference checks | Permissions register and tradition-specific music evaluation before production |
| V15–V16 economics/evolution | Capped jobs, weekly reports, watchdog and snapshots | Cost per accepted unit, stage-level health and honest Viral freshness; dated benchmark-driven technology reviews |
| V17–V18 owner/continuity | Expanded direction recorded here | Keep GitHub and Lovable aligned; one simple owner action only when unavoidable |

## Foundation changes merged and tested

Merged through [pull request 2](https://github.com/DANCEATLAS/crawler/pull/2), commit `36f5e5c`, on 9 November 2026. Code and documentation are on main. Generated catalogue/episode output from the next scheduled run has not yet been verified; local replay results below are not claims about the live site.

1. Attach hero/QC/tutorial media consistently after both catalogue merge paths, preserving sacred/restricted tutorial holds.
2. e2 packs fingerprint meaningful profile/media/teaching inputs. Check timestamps alone do not trigger rebuilds; targeted builds preserve unrelated packs/gaps.
3. Reserve at most one third of the existing enrichment allowance, capped at five, for relevant completion gaps. Seven-day cooldown; unchanged evidence skips repeat composition; failed retries retain good research.
4. Explicit count sequences and verified albums improve structural checks. Missing posture/mistakes remain gaps; no invented universal eight-counts or family-derived dance-specific counts.
5. Explicit `release_status: not_validated` and `rights_status: not_assessed` separate assembly from approval.
6. Failed offline selftests return failure to the workflow.

**Validation:** Python 3.11; 15 regression tests plus existing selftest passed. Full offline replay with HTTP/model calls blocked retained all 1,054 slugs, restored 48 tutorial records across 24 dances (67 to 91 tutorial-bearing entries), found zero tutorial leaks on the checked restricted entries, rebuilt 217 packs, and rebuilt none on the unchanged second pass. Results remained 166 drafts and 51 packs with teaching chapters withheld. The replay did not deploy generated catalogue/scripts/research. No paid calls or raised budgets.

## Viral findings and correction order

These code findings do not prove every displayed rank is wrong. Confirm database inputs and UI fallbacks before a production migration.

1. **P0 — Ranking meaning.** `score_virals.py` combines cumulative views and votes with decay based on `origin_date`; year/month half-lives are 540/120 days. These do not measure activity within those windows. Define dated, reproducible observation windows; snapshot comparable metrics before velocity ranks; label stale/missing data honestly.
2. **P0 — Data flow/counters.** `push_viral.yml` sends hero ID and video stack, not the crawler's `views`; inspect other refresh paths for database score inputs. `weeks_on` increments per run, not per week. Use explicit observation periods and idempotent counters/history.
3. **P0 — Failure/empty data.** Parent workflow ignores scorer failure. Empty eligible sets can fail in `zs([])`, averages and `scored[0]`. Add meaningful empty/stale behavior and visible stage health.
4. **P1 — Refresh.** `crawler.py` sets permanent boolean Viral cache entries even for unsuccessful searches, and its database target query only requests missing heroes. Replace with attempt/success/retry dates and bounded refresh inside existing caps.
5. **P1 — Coverage/identity.** Separate discovery, enrichment and refresh; reconcile aliases, creators and song versions with stable IDs. Challenge and tradition identity remain separate. Do not claim global popularity without adequate coverage.
6. **P1 — Teaching/assets.** Record original versus popularizer credits, sequence, exact track/edit, evidence date and permissions. Prepare practice, costume/background, collaborative-edit and export assets with review status. Public hero footage is not a reusable production asset.

New-chart acceptance: deterministic fixtures, stable ties, no false ranks on insufficient data, explicit data age/window, idempotent same-period runs, correct week counters, manipulation checks and no excluded entries left as apparently current. Preview against the real schema before deployment. Do not keep a “This Month” label attached to an unrelated proxy without explanation.

## Next work

1. Completed: publish the vision/foundation batch and verify matching Lovable instructions. All 17 prepared remote branch files matched local files byte-for-byte before merge.
2. Inspect the next existing capped job's outputs after foundation deployment; do not trigger paid research merely to prove documentation changed.
3. Repair Viral ranking/freshness using schema and UI evidence.
4. Strengthen evidence coverage and targeted sources; correct demonstrated origin/country issues without collapsing distinct cultures.
5. Validate teaching, BDF memory, creative assets and permission contracts on a small contrasting set. Keep private user records outside the public repo.
6. Prepare one intentional Lovable UI batch for validated needs. Do not spend credits creating speculative AR/social/sensor screens now.

## Publication record

- Foundation: Python 3.11 compilation and selftest passed; all 17 prepared files matched the uploaded branch exactly before merge.
- GitHub: full vision committed as `c5f9af8` and exact file match verified. Remaining foundation/docs merged to main through [PR 2](https://github.com/DANCEATLAS/crawler/pull/2), commit `36f5e5c`; GitHub confirmed successful merge and closure. This ledger update records the result.
- Lovable Project instructions: saved DA-VISION-2026-11-09-BDF; navigated away and reopened the settings, then verified the complete 8,286-character text persisted. No Lovable build prompt was sent.
- Database, live UI, workflow budgets/schedules, paid services and public video distribution: no changes in this batch. Supabase sign-in is needed for dashboard-only work, but was not needed for these documentation/code changes.

Update after observed results. Never report “implemented across all platforms” when only prose was saved or a patch prepared.

## 10 November 2026 — simpler weekly progress and support checks

**Publication state:** changes below are prepared and tested locally; they have not been committed to GitHub main or mirrored to Lovable. Chrome access was interrupted during the normal upload flow, before any commit confirmation was observed. Do not describe the next email as updated until the code is published and verified.

Owner direction: the old weekly email was too complicated. Present the full vision in plain language, large type, a quick overview and optional depth. Ask for one unavoidable owner action at a time.

Prepared changes:
- `pipeline/progress_digest.py` provides an approximately 500-word overview with 34px title, 24px headings, readable 16–18px body text, two main progress numbers, one necessary owner action at most, all V01–V18 requirements, cost/reliability and next priorities. The short Markdown version also supplies the existing fallback email.
- `reports/weekly/details.md` carries evidence, 7/28-day comparisons, structural checks and stage history. The subject is shorter. Existing recipients, weekly schedule, budgets and duplicate guard are unchanged; no test email was sent.
- `pipeline_state/vision_status.json` records dated capabilities, next work and owner actions. Capability descriptions become “Needs recheck” after 30 days; old or future-dated owner requests are not repeated as current instructions. Weekly editor and AI instructions require maintaining this record after verified changes.
- Measurements now exclude removed profiles/scripts from published growth; translation files, current master matches, native review and configured target languages are distinct. Saved Viral seed counts are explicitly not live popularity measurements. Account balances, exact costs and release approval are not inferred from logs or scores.

Observed foundation output on main `b961607` (9 November run, inspected 10 November): 1,047 Atlas entries; 223 deep profiles present in the Atlas export; 90 entries with tutorial references; 231 stored script packs, of which 223 match currently published Atlas profiles; no gap-free packs. Translation inventory for these packs: 29 files across 9 languages, 5 matching current masters, 0 complete native-reviewed translations recorded. The 12 configured language targets are not 12 completed languages. These are repository measurements, not a fresh visual test of every website profile.

Support checks:
- Latest daily workflow #25 succeeded; its committed e2 scripts and restored tutorial attachment are present. The latest counts differ from the earlier offline replay because a later editorial pass retired/merged entries and daily research added others.
- Owner signed into Supabase. This account's dashboard denied access to the project. No new organization/project, permission or billing changes were made by this session. Further dashboard-only checks still need the owning account or authorized membership.
- Existing, already-configured GitHub `schema_dump` workflow was run read-only via the normal UI: [run 42757948733](https://github.com/DANCEATLAS/crawler/actions/runs/42757948733). It succeeded using the existing connection. Initial displayed schema output was read; full schema, security policies and usage are not yet reviewed. No model calls or data writes are in that workflow. The pipeline's dated status reports 957 database dances and 154 Viral entries; Atlas export has 1,047. Do not treat database totals as website totals.
- Viral ranking-window, refresh and failure-handling defects remain open; a successful metadata connection does not fix them. BDF, native teaching/rights validation, social creation and AR remain preparation/future work as recorded.

Validation: Python 3.11 compilation; existing selftest plus 27 regression tests passed (15 foundation, 12 reporting). Report generation completed using full Git history without model calls or email delivery. Checks cover removed entries, stale translations, configured-vs-real language counts, unknown counts, missing/stale/future capability/action records, HTML escaping, full vision coverage and the existing weekly duplicate-guard date format. HTML email rendering in actual email clients remains unverified; browser preview was unavailable. No raised budgets, purchases, Lovable build or database migration.

Next session: reconnect the originating Chrome; inspect upload state before retrying; refresh main and compare changed paths to avoid overwriting concurrent work; publish the complete tested batch, verify exact content, update this publication record, and save/read back the Lovable instructions mirror. Then finish reviewing the successful schema output to plan Viral repairs. Do not ask the owner to redo copying or file edits.


## 11 November 2026 — correct backend found; complete next-run reconciliation

The owner is now in the owning Supabase organization. The existing project `maojpsywvbksrwkrxmjx` is visible under its original generic default display name and reports Healthy. Read-only dashboard inspection verified 991 dances and 154 Viral challenges. No replacement project or reconnection is needed. Sunfeld is a separate paused project, outside scope. `NEXT_RUN_PLAN.md` contains the exact platform map, complete V01–V18 request coverage, concrete findings and ordered continuation. Old sign-in blockers above are historical and resolved.

The actual Viral implementation differs from the previously inferred scorer path: `viral_chart` assigns origin-date row numbers and repeats them for all/month/year; views are NULL. `viral_chart_rankings` is empty. `viral_scores`, `viral_chart_history` and `votes` do not exist, and expected scorer input columns are absent. Correct the UI/database contract before presenting these as popularity rankings. The read-only inspection did not change data, views or policies.

Database audit history is 567,517,184 bytes (about 541 MiB), while the database-size query returned 586,517,651 bytes; the organization dashboard reports 601 / 500 MB under its usage measure. The audit trigger stores whole old/new dance rows on every UPDATE without an unchanged-row check. Preventing unnecessary producer writes is the first reversible investigation; existing history has not been deleted and no billing has been enabled.

Latest repository baseline is `851e84b` (10 November daily output): 1,064 offered Atlas entries, 249 published deep profiles, 90 tutorial-bearing entries, 249 current script packs and zero gap-free packs. There are 30 translation files in 9 languages, 6 current master matches and zero complete native-reviewed translations recorded. These are repository measurements, not approval of teaching or a fresh test of every live profile.

This change carries forward the interrupted report batch, with two additional reporting safeguards: equal database/catalogue totals are not called a mismatch, and platform observations retain their evidence date and expire. The weekly renderer covers V01–V18 in large readable text with optional detailed evidence. Existing report artifacts/delivery dates and weekly history are preserved until the scheduled run; no extra email has been sent. Report build uses no model calls.

Validation: Python 3.11.18 compilation and existing selftest plus 29 regression tests passed on the current baseline. Python 3.12 also passed. Publication is complete only when this change is merged into main and the remote files match. Check Git history for that outcome; do not infer email delivery from code publication. The tracked Lovable instructions include the updated checkpoint; saving them in Lovable itself requires a separately observed readback. Its existing tab was owned by another active browser session during initial inspection, so no build was started or connection changed.

## 11 November 2026 — Active Profile mission and preparation system

Owner revision: DA-VISION-2026-11-11-ACTIVE. The destination is interactive readiness, including the initial AI BDF, multiple human BDF friendships matched by chosen musical/social preferences, shared learning, synchronized movement, split-screen/on-camera and optional AR. Every living dance and meaningful variant is the long-term coverage ambition; scripts are supporting assets. Masterpiece references and usable music choices need separate quality and rights evidence.

Implemented source changes: offline activation stage, versioned per-profile dossiers, namespaced Atlas/Viral index, separate gap queues, budget-limited research feedback, timestamped video extraction with observation limits/distinctive methods, fingerprint-bound dated human-review gates, use-specific music gate, technology source/due-date register, current standard/music strategy and simpler weekly digest. Existing data contracts, research caps, free/prepaid paths, weekly send guard and historical report delivery records are preserved. No model calls, music/video generations, purchases or Lovable build were used for this preparation.

Local validation on Python 3.11: compilation and 37 regression tests pass; full offline generation produced 1,247 dossiers (1,064 Atlas + 183 saved Viral), zero ready and zero active. Repeated generation changed zero dossiers. The 154 Viral rows in Supabase are not the same inventory as the 183 saved crawler entries. Tests cover stale approvals, missing/composition/recording rights, missing use permissions, future review dates, duplicate music assets, sacred holds, evidence bounds, independent-teacher checks, retirement, namespace collision and malformed input. These tests validate preparation logic, not teaching efficacy or legal rights.

Still required: source and practitioner review, current video evidence, real learning trials, native/ability review, rights acquisition and musician vetting, bounded Viral deep research, human BDF/social runtime, measured synchronization, sensor/voice/AR validation. Popularity-view/schema defects and database audit growth remain open. They are in NEXT_RUN_PLAN.md; no unsupported fix or launch claim. Publication and cross-platform save/readback are recorded below when completed.

### Publication and platform readback — completed 11 November 2026

PR https://github.com/DANCEATLAS/crawler/pull/3 merged as a1fdf3072d0fd5b832cdf758768cab65c804cdf7. All 29 remotely saved source/handoff files matched the tested local files; a separate checkout of the remote branch passed Python 3.11 compilation and all 37 regression tests. The merged tree matched that source tree. No email was force-sent and historical delivery records were not advanced.

The existing atlas_daily workflow was dispatched on main with stage=activation and research/enrichment/hero/discovery inputs all zero. Run https://github.com/DANCEATLAS/crawler/actions/runs/42954416404 succeeded in 19 seconds and committed 0b830f5 (pipeline: activation 2026-11-11). The published index/report and 1,247 dossier files were fetched and verified: 1,064 Atlas + 183 saved Viral, zero ready and zero active. The daily workflow now includes activation automatically. No paid model calls occur in this stage.

Supabase maojpsywvbksrwkrxmjx is now visibly named **Dance Atlas**, verified in the dashboard; ID, region and connections did not change. Sunfeld was untouched. The private schema/table dance_atlas_internal.ai_context now contains project_handoff at revision DA-VISION-2026-11-11-ACTIVE, with canonical links and the complete condensed instruction mirror. RLS=true; anon and authenticated have neither schema usage nor table SELECT. This does not expose a new app API or store learner data. No dance records were changed by the ledger migration.

Lovable Project instructions saved successfully within its 10,000-character limit and were reopened to verify the current revision/name. No build was triggered. The final 9,443-character mirror is LOVABLE_KNOWLEDGE.md, SHA-256 2d329941f4ce1ad80a9b7d894743de2ebb516bc621c5c7cb2c666b8e6e0419cb; Supabase readback records the same revision, length and checksum. Full requirements are linked, not discarded to meet the UI limit. GitHub, Lovable and Supabase now share the current vision. An unrelated external AI account/schedule was not modified or claimed synchronized.

Next evidence and implementation tasks remain in NEXT_RUN_PLAN.md and ACTIVE_PROFILE_REPORT.md. The system prepares and routes gaps; it does not itself prove optimal teaching, clear rights, approve human reviewers, deploy BDF/social/AR or repair the separately documented Viral ranking/audit-growth defects.


## 11 November 2026 — continuing research into missing activation requirements

Owner correction: a saved vision and fixed checklist do not meet the requirement for constant research into what more makes profiles active. CONTINUOUS_RESEARCH.md now defines three distinct loops: daily dossier reassessment, requirement discovery inside existing profile research calls, and a separately scheduled external evidence/research pass. All V01–V18 scope and budget rules remain.

Implemented in this batch: source-linked activation questions beyond the existing schema; exact Atlas/Viral routing; question-sensitive approval fingerprints; evidence/date-bound closure and reopening; oldest-reviewed focus/sample agenda; dated external findings register; and a fix for the existing hint truncation that could prevent new questions from reaching the composer. Existing model-call counts and token caps are unchanged. Completion slots and cooldowns remain capped. The first bounded requirements pass on an older record is allowed once; unchanged reviewed evidence skips recomposition. Missing question output is not counted as a completed requirements pass.

The ChatGPT task **Dance Atlas readiness research** was created/enabled on 11 November, first scheduled for 12 November at 16:00 Asia/Tokyo, then daily. It investigates at most two profiles and six external source pages per pass, rotates through the seven full-vision areas, and reports only material findings/decisions. Future execution and private write access are not yet observed. If writes are unavailable, exact findings remain in the task result as pending integration; they are not reported as committed or mirrored. No duplicate weekly email or outreach was sent.

Initial primary-source research recorded two platform investigations in pipeline_state/readiness_findings.json: targeted video coverage within budget, and stable partner identities/recovery in group feedback. These are proposed benchmarks inferred from documented controls and the product requirements, not validated product capability. No individual profile was falsely marked reviewed.

Validation: Python 3.11 compilation and all 44 regression tests passed. Full activation replay with sockets disabled retained 1,247 dossiers (1,064 Atlas + 183 Viral), zero ready and zero active; the unchanged second pass changed zero dossiers. Generated research agenda selects the oldest-reviewed area and a typed Atlas/Viral sample without advancing research dates. Tests cover source allowlists, candidate-only status, identity separation, expiry/future dates, fingerprint invalidation, review rotation and new-question delivery ahead of legacy hints. No paid model call, production generation, billing change or Lovable build.

Publication: prepared/tested local source; GitHub working branch dance-atlas-continuous-readiness-20261111 currently contains research.py, activation.py and readiness_research.py only. Browser control stopped responding while filling selftest.py. Nothing from this batch has been merged to main. Lovable/Supabase mirrors remain at the previous verified 9,443-character version. Complete and verify the branch before merge; do not run its partial code. The daily external research task is independently enabled. Existing daily/weekly GitHub schedules remain unchanged.

## 14 November 2026 — spending control and durable research

Owner requested clearly marked actions, control of OpenAI/other platform spending, automatic issue detection and a simple weekly overview. Reviewed the current V01–V18 mission against actual code and prior successful research results. Full vision is retained; no fixed checklist or vendor announcement replaces evolving requirements research.

Verified risks: configured model names were preferences rather than an allowlist; the provider client could select other/newer models and fall back to paid OpenAI. The watchdog used last success, so a persistent failure could trigger another full run every six hours. Daily exceptions and push failures could leave a green-looking job. Report date still does not prove email delivery. Existing database audit growth and Viral schema/ranking mismatches remain unresolved, not silently reported fixed.

Prepared safeguards: disabled model API policy and no model-key injection in daily/crawler workflows; strict exact-model/expiry authorization for any future allowance; shared process request/output reservations including retries; provider stop on quota exhaustion; secret query strings removed from HTTP exception URLs; no automatic failed-job replay; nonzero daily exception/push failures. The fixed limits are not an account-wide dollar cap or complete input-token measurement. No balances or invoices were inspected, no paid model calls made, no subscription/billing changed.

The existing ChatGPT task was updated and read back on 14 November: weekly Sunday 16:00 Asia/Tokyo (next 15 November), replacing daily. Two profiles/six sources, all seven rotation areas and V01–V18 remain. Routine findings stay in saved records/weekly overview; exceptional messages start ACTION NEEDED or PLEASE NOTE. The task still consumes plan capacity. It does not send an additional email.

Recovered the complete unpublished continuous-research implementation and all eleven findings from successful 11–13 November work. The registry retains learning/accessibility and music/source-clock/export questions with dates, sources, exact profile namespaces and pending validation. The next oldest-unreviewed area remains AI interaction/memory. This operational review is not a fabricated external research pass and does not advance its review dates.

Validation: Python compilation and offline selftest, including 51 regression tests, passed. Checks cover disabled/malformed/expired spending policy, direct-call bypass, pinned model selection, retry accounting shared across stages, provider stop, URL-key redaction, namespace separation, candidate-only findings, stale approvals, culturally restricted content and no false activation. No production generation, outreach, force-sent email, purchase, Lovable build or gate weakening.

Publication status at preparation: complete source is isolated on dance-atlas-cost-continuity-20261114. Main/mirror publication and queue readback require separately observed confirmation; the final publication entry below is authoritative. COST_AND_CONTINUITY.md lists controls and unresolved next work, including safe no-op database updates, truthful Viral charts, delivery receipts, restoration tests and verified future spending authority.

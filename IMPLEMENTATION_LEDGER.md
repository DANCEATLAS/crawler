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

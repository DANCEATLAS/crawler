# THE WEEKLY PASS — playbook for the AI that runs it (Mondays)

*One session a week on the owner's Claude plan. No money is spent, nothing touches Lovable, the owner is not involved.
Read `AI_BRIEF.md` first if you have never worked here: it holds the vision, the non-negotiables and the system map.
Everything below is reachable without credentials at `https://raw.githubusercontent.com/DANCEATLAS/crawler/main/<path>`
(add `?nc=<random>` to dodge the cache). Writing back needs the owner's Chrome (signed in to GitHub) — see step 5.*

The pass has one purpose: **make the daily machine produce better pages than it would alone.** It does that by reading
like an editor, deciding what the machine cannot decide, and finding what the machine cannot find.

## 0. Health (5 minutes)
- Read PRODUCT_VISION.md and IMPLEMENTATION_LEDGER.md; refresh pipeline_state/vision_status.json only after evidence-based review. Cover V01–V18, including BDF and Viral creation/distribution. Resolve completed owner actions. A dated capability description is not an automated feature test. Keep weekly email plain, brief and readable; detailed measurements belong in reports/weekly/details.md.
- `STATUS.md`: `_Generated` should be within the last 36 hours (the cron fires 6–8 h late, that is normal). "Recent errors" empty or harmless.
- `pipeline_state/runs.json`: the last `research`/`qc`/`build`/`sync` entries finished without `errors`.
- If the daily run is broken: open the run log (Chrome → github.com/DANCEATLAS/crawler/actions → latest `atlas_daily` → job → raw log),
  fix the code locally, run `python3.11 -m py_compile` and `python3.11 -m pipeline.run selftest`, commit (step 5). Fixing the machine beats everything else in this pass.
- `WEEKLY_REPORT.md`: its date should be today or yesterday (the `weekly_report` workflow fires Sunday 23:23 UTC and posts the report to the issue
  "📬 Weekly library report", which e-mails the owner). If it is older than 6 days, GitHub dropped the schedule: run it by hand
  (Chrome → Actions → `weekly_report` → Run workflow). Read it: the "Closest to film-grade" table is your gap-hunt list (step 2).

## 1. Editor's read (the heart of it, ~30 minutes)
- Targets: this week's newly published pages. `pipeline_state/qc_index.json` → entries with `publish_gate == "publish"` and `qc_at` in the last 7 days;
  read each `research_results/<slug>.json` (profile_long, sections, music_profile, movement_profile, episode_brief, claims).
- Read like the owner's editor-in-chief: Is it true (spot-check two claims against their quoted source)? Is it respectful and precise about the culture?
  Is it concrete (people, places, years, objects) or filler? Would a beginner learn the first steps from `teaching` and `movement_profile`?
  Is it a dance *style/tradition* at all, or a move, a song, a festival, a company, a person (the judge misses some)?
  That test is for the Atlas catalogue only. Viral challenges and trends are a separate, first-class collection (`viral_challenges_verified.json`,
  `PRODUCT_VISION.md`): retiring or merging a move in the Atlas does not touch Viral, and a valid challenge is never erased — name it in the log as a Viral candidate.
- Decide, one line each:
  - true (two claims spot-checked), respectful, concrete, teachable → **approve it**: `pipeline_state/editor_approvals.json`:
    `{"slug": {"at": "YYYY-MM-DD", "by": "weekly pass", "note": "what was checked"}}`. Approval is the last item of the film-grade standard
    (`STANDARD.md`); it lapses when the page is re-researched, so re-read pages whose `researched_at` is newer than your approval.
    It is a research-preparation check, not practitioner, rights or release approval (`STANDARD.md`, `PRODUCT_VISION.md`).
  - not a dance / a double / hopeless → `audit_overrides.json`: `"slug": "retire"` or `"slug": "merge:<other-slug>"`.
  - a page with a fixable fault → `pipeline_state/editor_notes.json`: `{"slug": {"note": "<what is wrong and what the page must say instead>", "at": "YYYY-MM-DD"}}`.
    The next daily run re-researches that page first and hands your note to the composer as an order; the note is marked `done_at` afterwards.
  - the same fault on several pages → it is a rule problem: change `EDITORIAL` in `pipeline/research.py` or the gates in `pipeline/qc.py`, selftest, commit.
- Also skim the `review` items in `QC_REPORT.md` (top table): rescue the good ones with an editor note that says exactly what to fix; retire the hopeless.

## 2. Gap hunt (~30 minutes, the biggest lever for the mid-term product)
- `STATUS.md` → "Closest to movie-ready" lists pages one or two items short, with what each lacks (tempo/meter, footwork with counts, recordings, images…).
- `pipeline_state/episode_gaps.json` lists, per published page, what its episode script could not fill (tempo, meter, instruments, a recording, images, footage, steps, what to avoid…); the same sources fix both.
- For 8–10 of them, search the web for a source that actually contains the missing thing: a dance teacher's page with the counts, a conservatory or university
  page, a museum or archive, an ethnomusicology article, a reputable newspaper feature. Prefer pages that *describe* (text) over pages that only embed video.
- Add them to `pipeline_state/sources_extra.json`:
  `{"slug": [{"url": "https://…", "tier": "scholarly|archive|practitioner|press|other", "note": "what it covers (e.g. the basic step with counts, 2/4 at ~120 bpm)", "added": "YYYY-MM-DD"}]}`
  The daily run fetches each page as text, hands it to the composer labelled with its trust tier, lets claims quote from it (quotes are still verified
  mechanically), and re-researches that page first. Licensed images: a Wikimedia Commons category or file URL in `note` helps too.
- Never add: pages behind logins, copyrighted lyrics/sheet music sites, forums, anything that reads as promotion.

## 3. Doubles and connections (10 minutes)
- `QC_REPORT.md` → "Audit: possible duplicates kept live, need a human": decide them (`keep` / `retire` / `merge:<slug>`) in `audit_overrides.json`.
- New pages held in `review` as `not_duplicate` (QC found a live entry with the same name or alias — e.g. a regional name for a dance already listed):
  `merge:<slug>` if it is the same tradition, `keep` if it is genuinely another dance — `keep` also clears the QC double flag at the next run.
- Spot-check `connections` on the pages you read: a connection to a dance that is a double of an existing entry is a merge waiting to happen.

## 4. Editorial log (5 minutes)
- Append this week's entry to `EDITORIAL_LOG.md` (root): date, pages read, decisions made (counts and the notable ones), rule changes, sources added, what the next pass should look at first. Short.

## 5. Commit (the only mechanical part)
Publish through GitHub's normal upload page in the owner's signed-in Chrome — no injected scripts (`AGENTS.md`). One folder per commit.
1. Keep the edited copies in your scratchpad under the repo's relative paths. Just before uploading, fetch each live file
   (`https://raw.githubusercontent.com/DANCEATLAS/crawler/main/<path>?nc=<random>`) and make sure your copy was made from it: the upload
   replaces the whole file, so if someone changed it meanwhile, redo your edit on the new version. For code: `python3.11 -m py_compile` and
   `python3.11 -m pipeline.run selftest` first.
2. Chrome tools: `tabs_context_mcp` → `navigate` to `https://github.com/DANCEATLAS/crawler/upload/main/<folder>` (`pipeline_state`, `pipeline`,
   or nothing for root files) → `find` the file input ("Choose your files") → `file_upload` with that ref and the absolute paths of your files.
3. `form_input` the commit summary ("weekly pass <date>: …") and the description, ending with the attribution lines your session was given;
   leave "Commit directly to the main branch"; click "Commit changes" by its ref.
4. Verify: open `https://github.com/DANCEATLAS/crawler/commits/main`, take the new commit's id and compare
   `curl -s https://raw.githubusercontent.com/DANCEATLAS/crawler/<commit-id>/<path> | sha1sum` with `sha1sum` of your copy
   (the `main` address lags several minutes; the commit id does not).
`tools/upload_payload.py` is legacy: do not run its payloads. If no browser is signed in to GitHub, do not sign in or type any password;
put your decisions verbatim in your final message instead.

## 6. Tell the owner (1 minute)
One short message, bold headers, five lines at most: the best new page of the week in one sentence, what you fixed or decided (numbers: approved,
retired, merged, notes, sources), and — only if it exists — the one thing that needs him. The counts are already in his weekly report e-mail;
do not repeat them. If nothing needs him, say so in four words.

## What not to do
- Do not run the Lovable AI, change the website, add dependencies, enable billing, or create accounts (`AI_BRIEF.md` §3).
- Do not rewrite pages by hand in the JSON — write an editor note and let the machine re-research with sources; hand-written text would carry no verified quotes.
- Do not loosen the QC gates to publish more. Fewer true pages beat more doubtful ones.
- Do not spend more than one session; what is left waits for next Monday.

## Resume checkpoint — 11 November 2026

Read `NEXT_RUN_PLAN.md` before the next substantive pass. The existing Dance Atlas Supabase project is accessible; do not repeat account creation or sign-in requests. Keep Sunfeld outside this work. Preserve all V01–V18 requirements and update measured state rather than treating the vision as implemented.

## Active Profile continuation — 11 November 2026

Read ACTIVE_PROFILE_STANDARD.md, MUSIC_STRATEGY.md, ACTIVE_PROFILE_REPORT.md and NEXT_RUN_PLAN.md. Active Profile replaces movie readiness as the destination. Review every gap stream, including video teaching methods, human BDF relationships, shared/split-screen/camera experiences, AR readiness and music choices. Recheck due primary sources in pipeline_state/technology_watch.json; record actual checks, not just a new date. Keep all caps unchanged. Maintain matching revision DA-VISION-2026-11-11-ACTIVE in GitHub, Lovable instructions and the Supabase private AI context; linked current ledgers are authoritative. Do not represent this playbook change as proof that an external Claude schedule was changed.

# THE WEEKLY PASS — playbook for the AI that runs it (Mondays)

*One session a week on the owner's Claude plan. No money is spent, nothing touches Lovable, the owner is not involved.
Read `AI_BRIEF.md` first if you have never worked here: it holds the vision, the non-negotiables and the system map.
Everything below is reachable without credentials at `https://raw.githubusercontent.com/DANCEATLAS/crawler/main/<path>`
(add `?nc=<random>` to dodge the cache). Writing back needs the owner's Chrome (signed in to GitHub) — see step 5.*

The pass has one purpose: **make the daily machine produce better pages than it would alone.** It does that by reading
like an editor, deciding what the machine cannot decide, and finding what the machine cannot find.

## 0. Health (5 minutes)
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
- Decide, one line each:
  - true (two claims spot-checked), respectful, concrete, teachable → **approve it**: `pipeline_state/editor_approvals.json`:
    `{"slug": {"at": "YYYY-MM-DD", "by": "weekly pass", "note": "what was checked"}}`. Approval is the last item of the film-grade standard
    (`STANDARD.md`); it lapses when the page is re-researched, so re-read pages whose `researched_at` is newer than your approval.
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
```
# from the folder where the edited copies live (same relative paths as the repo)
python3 tools/upload_payload.py --dir ""             --summary "weekly pass <date>: …" --description "…" --out p1.js audit_overrides.json EDITORIAL_LOG.md
python3 tools/upload_payload.py --dir pipeline_state --summary "weekly pass <date>: editor notes, sources, approvals" --out p2.js editor_notes.json sources_extra.json editor_approvals.json
python3 tools/upload_payload.py --dir pipeline       --summary "…" --out p3.js research.py        # only if you changed code
```
Each run prints the GitHub upload URL to open in Chrome (`tabs_context_mcp` first; `navigate`; then `javascript_tool` with the payload text).
The payload stages the files, fills the commit form, waits for the upload and submits. It fetches the live file at commit time and refuses to
stage anything if the live file no longer matches the hunks, so it cannot overwrite a newer change. Verify afterwards:
`curl -s "https://raw.githubusercontent.com/DANCEATLAS/crawler/main/<path>?nc=1" | sha1sum` matches the tail the tool printed.
End every commit description with the attribution lines your session was given.

## 6. Tell the owner (1 minute)
One short message, bold headers, five lines at most: the best new page of the week in one sentence, what you fixed or decided (numbers: approved,
retired, merged, notes, sources), and — only if it exists — the one thing that needs him. The counts are already in his weekly report e-mail;
do not repeat them. If nothing needs him, say so in four words.

## What not to do
- Do not run the Lovable AI, change the website, add dependencies, enable billing, or create accounts (`AI_BRIEF.md` §3).
- Do not rewrite pages by hand in the JSON — write an editor note and let the machine re-research with sources; hand-written text would carry no verified quotes.
- Do not loosen the QC gates to publish more. Fewer true pages beat more doubtful ones.
- Do not spend more than one session; what is left waits for next Monday.

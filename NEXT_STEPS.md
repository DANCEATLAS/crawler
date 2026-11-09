# NEXT STEPS — written by the machine on 2026-11-09

*Regenerated every Monday by the weekly report from the library's own numbers. Read `AI_BRIEF.md` first; this file says where to push.*

## What the numbers say to do first

1. **tempo (bpm)** is missing on 179 published pages — a source that states the tempo — a teacher's page or a music reference, added via pipeline_state/sources_extra.json.
2. **licensed images (3 needed)** is missing on 147 published pages — a Wikimedia Commons category or file link in an editor note.
3. **a verified recording to listen to** is missing on 129 published pages — a recording title the composer can verify in MusicBrainz (an album or single named in a source).
4. **meter** is missing on 128 published pages — a source that states the time signature.
5. **licensed reference footage** is missing on 127 published pages — a Commons video or an Internet Archive film naming the dance in its title.
6. **132 dances have no hero video** — the crawler retries them every 21 days; an editor note with a channel or search phrase helps the stubborn ones.
7. **102 pages wait in review** — each needs one decision in `audit_overrides.json` or one editor note (`WEEKLY_PASS.md`).
8. **No page is film-grade yet** — the closest ones and what they lack are in `WEEKLY_REPORT.md` §6; the editor's approval is the last item on every one of them.

## Decisions still open (the owner's)

- Video platform for the episodes (the packs are platform-neutral; one exporter when named).
- Music generator and voice-over tool (briefs and narration are ready; licences and cost are the owner's call).
- Showing the deep profiles and the episodes on the website (one Lovable paste, `LOVABLE_UI_PROMPT.md`).
- OpenAI top-up when the prepaid balance is spent (the run says so in `STATUS.md` and here).

## What not to touch

- The QC gates (`pipeline/qc.py`): fewer true pages beat more doubtful ones. The sacred rule. The no-invention rule in the scripts.
- The budgets in the workflow: the machine lowers them itself when the models fail and raises them back; raising them above the defaults costs quota, not quality.
- Lovable: content never goes through it; its AI is for layout only, once, with the prepared prompt.

# Music choices for Active Profiles

Revision DA-VISION-2026-11-11-ACTIVE. Primary sources checked 11 November 2026. This is an acquisition and vetting strategy; **no tracks have been cleared by this work**.

The goal is outstanding music that makes people want to move, with real choices. A generic royalty-free loop is not an acceptable substitute for musical credibility. An admired recording is a listening/reference candidate until rights for the actual product use are documented.

## Four workable routes

| Route | What it provides | Work and cost decision |
|---|---|---|
| Existing masterpiece, directly licensed | Exact composition/performance the tradition values | Identify composition and master owners; request relevant app, synchronized lesson, group, recording and user-export rights when outreach is authorized. Quote before commitment; reserve expensive catalogue deals for proven demand |
| Public-domain composition plus cleared performance | Recognizable repertoire with a documented recording chain | Verify public-domain status in target territories and any protected arrangement; use a genuinely cleared recording or a newly commissioned performance. Old composition does not make every recording free |
| Openly licensed composition AND recording | Potential low-cost production-ready choice | Verify licensor authority, exact licence/version, attribution, territory and derivative/commercial permissions. Exclude NC for commercial scope and ND where synchronization/adaptation requires permission; BY-SA needs product-specific review |
| Original music with expert musicians, optionally assisted by AI | Reusable practice choices with control over tempo, phrase length, stems and rights | Commission original compositions/performances or acquire written reuse permissions when budget authorized. Brief style, groove, instrumentation and function, never imitate an identifiable artist or copy a melody. AI terms and originality still need review |

These routes may coexist in one profile. Offer a reference/masterpiece lane, a clearly labeled cleared practice lane, and an export-allowed lane. A user who picks a reference song must not accidentally gain permission to reuse it. Platform music licences may apply only within that platform; do not assume a song can be embedded in exported files. A replacement practice track is labeled a replacement and never presented as the original challenge song.

## What must be collected

For each candidate: recording identity and hash, composition and arrangement, performers and owners, source URL, exact licence/contract evidence, reviewer/date/recheck, territories, term, attribution, cost, restrictions, revocation process, and permissions for interactive lessons, group playback, synchronization, tempo edits, stems, recording, social export and any sublicensing. Store no confidential contracts or personal contact data in the public repository.

Musical review records: tradition/variant and occasion, pulse and accents, tempo range rather than a forced number, phrase/cycle structure, instrumentation/timbre, vocals and meaning, groove, performance quality, cultural suitability and what must remain invariant. Blind comparisons and practitioner/musician comments are stronger than a model's adjective or popularity count. Do not call music a masterpiece without meaningful evidence of excellence and cultural fit.

The machine-readable initial gate is music_options[] in pipeline_state/activation_inputs.json. Required fields: asset_id, status=reviewed, composition_evidence, recording_evidence, reviewer, quality_review, territories, conditions, reviewed_on, recheck_on, valid_from, valid_until (ISO date or explicit perpetual), uses={interactive_lesson,group_session,recording,social_export,tempo_edit}, with each use explicitly true. It currently requires two distinct assets. Narrower-use tracks can be retained as candidates but do not pass this full-use gate. Expiry or missing evidence blocks readiness. Full contracts and conditions still require qualified review; passing a JSON check is not a legal opinion.

## Current findings that change the decision

- The US Copyright Office distinguishes the underlying musical work and sound recording. Re-recording the performance alone therefore does not establish rights to the composition or all intended uses. [Official guidance](https://www.copyright.gov/engage/musicians/).
- Creative Commons treats music synchronized with moving images as adaptation. Exact licence conditions matter; “free online” is insufficient. [Official FAQ](https://creativecommons.org/faq/).
- ElevenLabs Music terms, updated 9 October 2026, restrict creating/contributing to a Music Library without express written authorization, with stated exceptions. This makes its standard commercial-use offer insufficient evidence for Dance Atlas's reusable user-facing music collection. Keep it conditional; obtain a written scope determination before selection. No subscription or generation is authorized here. [Official terms §4.2](https://elevenlabs.io/music-terms).

## Economical order of work

First reuse existing verified recording references and music descriptions to assemble candidate shortlists. Check rights and artistic fit before generating or commissioning audio. Choose a small, diverse pilot with at least two musically credible options per dance. Reuse recording sessions, stems and cleared assets only where culturally appropriate; never flatten different traditions into one interchangeable loop. Cache legal/quality evidence, recheck due dates, and stop a route when rights or cost cannot support the required product use. Store links/metadata now; bulk audio production waits for validated demand, permissions and an approved budget.

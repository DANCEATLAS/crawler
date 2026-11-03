# The one Lovable prompt — making the website show everything the machine produces

*For the owner, and for any AI he brings into Lovable.*

**How the content reaches the website (no credits, no action).** The site at dancingatlas.lovable.app loads its catalogue from this
repository every time a visitor opens it: `public/catalog/dances.app.json` (every dance) and `public/catalog/retired.json` (what to
hide). The daily run (`atlas_daily`, GitHub Actions) rewrites those files after research and QC, so every page the machine publishes
appears on the site by itself, usually the same evening. Nobody has to open Lovable for content. Lovable's AI — and its credits — are
needed for one thing only: when the site should **display a kind of content it has no layout for yet**. That is a UI change, done once.

**"Check the content growers"** (the owner's phrase) means: look at what the machine now produces — `STATUS.md`, `WEEKLY_REPORT.md`,
`public/catalog/profiles_v2.json` — and make sure the website shows all of it. The prompt below does exactly that in one batch.
Rules from `AI_BRIEF.md` §4 still hold: one precise prompt, verify the data first, check the preview, publish; never "look into"
things in Lovable chat, never fix data there (data is fixed in GitHub), never iterate on small things.

**How to use it.** When you decide the site should show the deep profiles: open this file on GitHub, copy everything below the line,
paste it into the Lovable chat as one message, wait for the preview, check two dances (e.g. passacaglia and western swing), publish.
Expect one prompt's worth of credits; if Lovable asks a question, answer it from this file rather than starting a new prompt.

---

Add the deep "research profile" to the dance page. Make no other change: same design language, same navigation, no new dependencies,
no backend, nothing stored except a session cache. All data is public static JSON in the GitHub repository DANCEATLAS/crawler, read
exactly the way the app already reads `dances.app.json` and `retired.json` from raw.githubusercontent.com (keep that code as it is).

DATA
1. `https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/profiles_v2.json` — `{ "profiles": { "<slug>": {...} } }`.
   It only contains dances whose `research_gate` is `"publish"` in `dances.app.json`. Fetch it once per session, lazily, the first time
   a dance page for such a dance opens; cache it in sessionStorage under `da_profiles_v2_session_v1` (same pattern as the catalogue
   cache); if the fetch fails or the slug is missing, the page simply shows what it shows today — never an error.
2. Each profile has: `sections` {origins_and_history, how_it_is_danced, music_and_instruments, costume_and_setting, occasions_and_meaning,
   notable_figures, regional_variants, lineage} (strings); `teaching` {basic_steps[] (strings), rhythm, formation, level_notes};
   `music_profile` {tempo_bpm, meter, rhythm_pattern, instruments[], vocal_style, musical_form, mood_keywords[], reference_recordings[] ({title, artist}),
   sound_description}; `movement_profile` {posture, footwork, arms_and_hands, hips_and_torso, formation_and_space, partnering, tempo_feel,
   signature_moves[] ({name, description}), levels_and_jumps, difficulty, what_to_avoid}; `episode_brief` {title_hook, logline, beats[],
   lesson_ladder[] ({level, goal, drills[]}), visual_motifs[], instructor_persona, music_cue}; `connections[]` ({name, relation, note});
   `adaptations` {seniors {seated_version, standing_version, tempo_and_range, counts, avoid[]}, children {game_version, duration_minutes, counts, avoid[]},
   derived: true} or {withheld: "<reason>"}; `footage[]` ({title, url, year, license, license_url, attribution, description});
   `images[]` ({title, url, thumb, width, height, license, license_url, artist, description, source_page, attribution});
   `albums[]` ({title, artist, year, musicbrainz_url, type}); `claims[]` ({text, source}); `citation` {claims, supported, rate};
   `tradition_status` ("living" | "revived" | "historical" | "unknown" | null); `movie_ready` (bool); `qc_score`; `researched_at`.
3. From `dances.app.json` the dance already has `profile_long`, `albums`, `images`, `movie_ready`, `qc_score`, `is_sacred`, `sources`,
   `related_slugs`, `video_stack`, `tutorials`.

PLACEHOLDERS — the rule that matters most
A field whose text is empty, "not described in sources", "Not described in sources.", "not in sources", "not derivable yet", "unknown"
or "null" is NOT shown: no heading, no empty card, no "n/a". A card whose fields are all placeholders is not rendered at all. Lists of
length 0 are not rendered.

LAYOUT (below the existing content of the dance page, in this order; each block is a titled section in the current style)
A. Badges next to the dance name: "Movie-ready" when `movie_ready` is true; "Living tradition" / "Revived" / "Historical" from
   `tradition_status` when it is one of those three; nothing for unknown.
B. "The story" — the eight `sections`, each with its heading (Origins & history; How it is danced; Music & instruments; Costume & setting;
   Occasions & meaning; Notable figures; Regional variants; Lineage). If `profile_long` is already shown on the page, keep it and put
   these sections after it.
C. "Learn it" — only when `is_sacred` is false: `teaching.basic_steps` as a numbered list, then rhythm, formation, level_notes as short
   labelled lines. When `is_sacred` is true, show one calm line instead: "Teaching material is withheld for this sacred or restricted dance."
D. "Music DNA" — a card: tempo (`tempo_bpm`), meter, rhythm pattern, instruments as chips, vocal style, musical form, mood keywords as chips,
   `sound_description` as a paragraph, `reference_recordings` as "title — artist" lines; then the verified albums with a link to
   `musicbrainz_url` (label "MusicBrainz").
E. "Movement DNA" — a card: posture, footwork, arms & hands, hips & torso, formation & space, partnering, tempo feel, levels & jumps,
   a difficulty chip (beginner / intermediate / advanced), signature moves as a list "name — description", and "What to avoid" as its
   own highlighted line. Omit this whole card when `is_sacred` is true.
F. "Film & class brief" — `title_hook` as a pull-quote, `logline`, `beats` as a numbered list, `lesson_ladder` as three small cards
   (level, goal, drills as bullets), `visual_motifs` as chips, instructor persona and music cue as labelled lines.
G. "For seniors · For children" — two small cards from `adaptations`, only when `derived` is true, not withheld, and the fields are not
   placeholders. Under the cards, one line in a muted style: "Derived teaching suggestions, not facts from the sources — adapt with a
   qualified instructor." Omit entirely when `is_sacred` is true or `adaptations.withheld` exists.
H. "Reference footage" — each `footage` item as a link (title, year, attribution, licence text) opening in a new tab. These are links only;
   do not embed or download anything.
I. "Images" — a small gallery from `images` (use `thumb`, link to `source_page`, show `attribution` and `license`). If the page already has
   an image gallery, extend it instead of adding a second one.
J. "Connected dances" — `connections` as lines "relation · name — note"; when the name matches a dance in the catalogue (compare lower-case
   name and aliases), make the name a link to that dance page.
K. "Sources & verification" — one line "N of M claims verified against their sources" from `citation`, the `sources` links, and a collapsed
   "Show the claims" list (claim text + a link to its source).

BEHAVIOUR
- Everything is read-only. No edits, no forms, no login, no analytics.
- The page must render exactly as today for dances with no profile in `profiles_v2.json`, and if the fetch fails.
- Headings and chips use the existing typography and colours; no new colour scheme, no icons library.
- Keep the page fast: fetch `profiles_v2.json` only when needed, once per session.
- Do not change anything in the catalogue loading, the atlas list, the map, the search, or the home page.

When done, show me the preview of the pages for "passacaglia" and "western swing".

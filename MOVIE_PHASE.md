# THE MOVIE PHASE — turning the library into films and classes

*For the owner and for any AI that continues this. Written 3 Nov 2026, the day the owner described the vision below and asked for it to
run on its own, without Claude or Lovable credits. Everything in this file that says "built" runs inside the free daily GitHub run.*

## The vision, in the owner's terms

An atlas where every important dance tradition in the world becomes a small series: **Episode 1** introduces the style — its story, the
most beautiful footage and costumes, its music explained well — and **Chapters 1, 2 and 3** teach it, basic to advanced, the way the best
teachers in the world teach, in one familiar formula so a viewer can jump between styles and always feel at home. The music under it is
original and copyright-free but true to the tradition's sound. The teaching is not copied from one video: it is distilled from many of
the best online teachers into one "ultimate teacher". Converting the library into scripts also tells the research what it still lacks.
The whole thing is for mind, body and community — people learning the world's dances and becoming better for it.

## The ecosystem — every piece, where it lives, what it costs

| Piece | What it is | Where | State | Cost to run |
|---|---|---|---|---|
| **The library** | deep, source-verified profiles, filtered by QC (`STANDARD.md`) | `research_results/`, `qc_results/`, the website | built, growing daily | free (Gemini free tier; OpenAI prepaid as fallback) |
| **Episode packs (scripts)** | for every published profile: Episode 1 + Chapters 1–3, scene by scene, in one formula; narration, on-screen directions, counts, music cues | `pipeline/episodes.py` → `episodes/<slug>.json` + `.md`, index `public/catalog/episodes.json` | **built** · rebuilt whenever a profile changes · narration assembled from the profile, optionally polished by the model and verified (`EPISODE_POLISH` a day) | free |
| **Teacher intelligence** | the best tutorial videos are watched and reduced to how the teacher teaches; aggregated into the playbook the chapter scripts follow | `pipeline/pedagogy.py` → `pedagogy/videos/`, `pedagogy/teaching_patterns.json`, `ULTIMATE_TEACHER.md` | **built** · `PEDAGOGY_BUDGET` videos a day (Gemini watches the public YouTube URL; nothing downloaded) | free |
| **Music brief** | per pack: tempo, meter, rhythm, instruments, mood, sound description, verified recordings to listen to, a composer prompt, the tracks needed, the copyright rules | inside each pack (`music_brief`) | **built** | free |
| **Visual brief** | per pack: the checked hero video, licensed images with attribution, footage links, motifs, costume notes from the sources, generation rules | inside each pack (`visual_brief`) | **built** | free |
| **Voice** | one narrator for the whole atlas — one face and animation; a native-speaker voice of the same character in every language; in each episode the narrator wears the dance's traditional apparel, reconstructed meticulously and respectfully from the sources (never sacred or restricted attire); an instructor persona per style; pronunciation list | inside each pack (`voice`, `visual_brief.wardrobe`) | **built** (text; the decision is the owner's, 3 Nov) | — |
| **Languages** | the master narration (English) translated scene by scene into every language the atlas offers, same structure, names and counts untouched, checked, marked machine-translated until a native speaker reads it | `pipeline/translate.py` → `episodes/i18n/<lang>/<slug>.json`; `TRANSLATE_LANGS` | **built** · `TRANSLATE_BUDGET` packs×languages a day, gap-free Episode 1 first | free |
| **The feedback loop** | what a script could not fill (tempo, images, footage, steps…) is asked of the next research pass on that page | `pipeline_state/episode_gaps.json` → `pipeline/research.py` | **built** | free |
| **The weekly report** | counts episode packs, complete packs, polished packs, lessons studied — week by week | `WEEKLY_REPORT.md` (e-mail) | **built** | free |
| AI composer | turning each music brief into tracks (theme, underscore, slow lesson track, full-tempo lesson track) | — | **not started**: needs the owner to choose a music generator and its licence terms | the generator's own pricing |
| Voice-over | reading the narration (narrator + instructor) | — | **not started**: needs a text-to-speech choice | the TTS pricing |
| Picture | assembling hero video, footage, images, reconstruction imagery and captions into the episode | — | **not started**: needs the owner's video platform | the platform's pricing |
| Exporter | writing each pack in the exact format the chosen platform imports | one small file, `pipeline/export_<platform>.py` | **not started**: waits for the platform decision; the packs are platform-neutral JSON + Markdown so this is a day's work | free |
| The episodes on the website | a page per dance showing its script, the lesson chapters, the music brief | `LOVABLE_UI_PROMPT.md` (add a section for `episodes.json`) | not started on purpose — one Lovable paste when the owner decides | Lovable credits, once |

Nothing in the first eight rows needs anyone. The last five are decisions, not work: once the owner names a platform, a composer and a
voice, the exporter is a small file and the briefs are already written.

## The formula — the same scenes for every dance

**Episode 1 · Meet the dance** (about 9 minutes)
`hook` cold open (the hook line, the hero video) · `where` where and when (origins, a map) · `occasion` when it is danced (and whether it is living,
revived or historical) · `watch` watch it (the hero video full screen, signature moves named) · `music` listen (instruments, meter, tempo, what it
sounds like, recordings to listen to) · `costume` the costume and the setting (licensed images) · `people` the people (notable figures, variants,
lineage) · `family` family tree (connections) · `first_step` try one step (or a respectful note for a sacred dance) · `close` until next time.

**Chapters 1 · First steps, 2 · Building the dance, 3 · Dancing it fully** (about 13 minutes each, the same nine scenes)
`welcome` goal and level · `body` posture, arms, torso · `count` the count and the rhythm (clap it, then step it) · `step_a` the first steps, slowly,
front and back view, three repetitions · `step_b` the next layer (next steps, a signature move) · `combine` put it together: slow, half, full tempo,
mirrored · `mistakes` common mistakes and what to avoid (with seated / children options, labelled as derived) · `music_run` dance it to the music,
twice · `close` recap, one culture note, the next chapter.

The material climbs: Chapter 1 takes the first four teaching steps and posture; Chapter 2 the next steps, the first signature moves, formation and
partnering; Chapter 3 the rest, levels and jumps, the tempo feel, the variants, the full dance. Every scene carries its narration lines, the
on-screen directions, the music cue, the counts and repetitions, and `needs` when the sources left it short.

## The rules a script lives by

1. **Nothing invented.** Narration is assembled from the profile's sections, music DNA, movement DNA, episode brief and connections — all of them
   source-backed with verified quotes. A model may rewrite the narration for flow; the result is kept only when it adds no year, number or
   capitalised name the profile does not contain (`verify_polish`). What the sources do not say becomes a gap, never a sentence.
2. **Sacred or restricted dances get Episode 1 only** — the story, the music, the costume — and a respectful note instead of a first step. No chapters.
3. **Seated and children's options are labelled** as derived teaching suggestions, never as facts about the dance.
4. **Music is original.** The brief carries the DNA (meter, tempo, rhythm pattern, instruments, mood, sound) and names recordings to listen to —
   never to copy. Generated tracks must be labelled with the tool, the date and the brief. Traditional tunes are used only when the profile names them
   and a public-domain source is on file.
5. **Pictures are licensed or labelled.** Hero videos must have passed the vision check; images and footage carry their attribution and licence;
   reconstruction imagery is generated only from the costume notes and labelled "reconstruction"; no likeness of a real named person.
   The narrator's wardrobe follows the same rule (`visual_brief.wardrobe`): dressed from the sources, or neutral when the attire is sacred,
   ceremonial or restricted, or when the sources are silent.
7. **Every language, the same script.** Translations keep the scene structure, every number and every name; a scene whose translation fails the
   check keeps the English line and says so; everything is marked machine-translated until a native speaker has read it.
6. **A pack is complete** when it has no gaps: tempo and meter, instruments, a verified recording, a checked hero video, three licensed images,
   footage, posture and arms, signature moves, teaching steps, what to avoid, two connections, every story section. Packs with gaps are drafts and
   are still written in full — the gaps are listed at the top and sent to the research queue.

## The teacher intelligence

The tutorial crawler already finds lesson videos per dance and ranks them by what viewers say. Each day the machine watches a few of the best
(published dances first, movie-ready ones first, the lesson viewers liked most, one per dance per day) and reduces each to a fixed form: the lesson's
structure with timestamps, the counting scheme, the cues the teacher repeats, the metaphors, demonstration angles and tempo progression, repetitions
per step, the mistakes named, safety advice, the steps as taught with their counts, what made it absorbable, and three to six verbatim quotes so
every extraction can be checked against the video. `ULTIMATE_TEACHER.md` is rendered from all of them: the lesson skeleton most teachers share,
how they count, how they demonstrate, the cues, the mistakes named most, what works and what hinders, per family and per dance. The chapter
scripts take their counting, cues and mistakes from the dance's own studied teachers when there are any, from the family otherwise, from the whole
atlas otherwise, and from a built-in default before the first lesson has been studied. The playbook grows a little every day and is never copied
from one teacher: it is frequencies across many.

## What runs by itself every day (free)

`atlas_daily`: … → build → **pedagogy** (`PEDAGOGY_BUDGET` = 6 videos) → **episodes** (every published pack rebuilt when its profile changed;
`EPISODE_POLISH` = 4 narrations polished and verified) → **translate** (`TRANSLATE_BUDGET` = 6 pack×language translations of gap-free packs) → sync → report. Budgets live in `.github/workflows/atlas_daily.yml`. `STATUS.md` shows the
counts daily; the weekly e-mail shows them week by week. The monthly snapshot keeps every pack and every lesson record.

## Decisions for the owner — nothing needed now; the defaults are in force

1. **Video platform** — decided 3 Nov: **platform-neutral** packs (JSON + Markdown) until the platforms and their needs are known; an exporter is
   written when one is named.
2. **Voice** — decided 3 Nov: **one narrator for the whole atlas**, the same face and animation everywhere, a studio-grade native voice of the same
   character in **every language the user can choose** — the atlas is for the whole world, not for one language. In each episode the narrator
   **wears the traditional apparel associated with the dance**, reconstructed with meticulous care to be genuine and respectful (from the
   profile's costume notes and licensed images only; never sacred, ceremonial or restricted attire — then neutral dress with a respectful nod; a
   culture bearer reviews the wardrobe before production). Languages in force: Spanish, French, German, Portuguese, Italian, Japanese, Chinese,
   Korean, Arabic, Hindi, Russian, Indonesian — `TRANSLATE_LANGS` in the workflow adds more.
3. **Episode length**: Episode 1 about 9 min, chapters about 13 min. Default in force; scene durations are fields in each pack.
4. **Which dances first**: packs exist for every published dance; complete packs first, then movie-ready, then the rest. The weekly report lists them.
5. **Music generator** and **text-to-speech**: the briefs are ready; the choice of tools, their licences and their cost are the owner's.
6. **Show the scripts on the website**: one Lovable paste, when wanted (add an "Episodes" section fed by `public/catalog/episodes.json`).

## When the owner returns — the next steps, in order

1. Read `WEEKLY_REPORT.md` and `ULTIMATE_TEACHER.md`; open two packs in `episodes/` (a complete one and a draft) and judge the formula on them.
2. Name the platform → an AI session writes `pipeline/export_<platform>.py` from the pack JSON (one day), runs it on the complete packs.
3. Name the composer → run the music briefs of the complete packs; keep the provenance labels.
4. Name the voice → generate the narration for one episode; watch it; adjust the narrator rule in `pipeline/episodes.py` (`NARRATOR`) if needed.
5. Only then, the website: the Lovable paste for an Episodes section.

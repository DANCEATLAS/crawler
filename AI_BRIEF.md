# DANCING ATLAS — BRIEF FOR ANY AI THAT CONTINUES THIS WORK

*Read this whole file before touching anything. It is written so that the owner never has to explain the project again. Written 30 Oct 2026 by the AI that built the content machine (Claude, working with the owner through Chrome). Keep it current: when you change the system, change this file in the same commit.*

---

## 1. The owner, in one paragraph

A DJ and dance educator building **Dancing Atlas**: an encyclopedia of every living dance tradition on Earth, researched to a depth no site has. He is not a developer and has ADHD. He wants to be involved **only when something cannot be done without him** (a payment, a login, a decision only an owner can make). When you do need him: one mission at a time, in a large short message with bold headers, exact steps, nothing else. He will not read long technical explanations. He decides launches and money; you decide everything else and tell him what you did.

## 2. The product and the vision (what we are actually making)

The **content is the product**. Each dance page is being built so that, on the day the technology is ready and the owner decides, the whole library can be handed to an AI video + music generator and come out as studio-quality episodes and dance classes — original characters as instructors, original copyright-free music in each style, original images and costumes — without anyone going back to redo the research. Later still: VR and dancing with humanoid robots (seniors, children, brain-body coordination). We are **not** building any of that now. AI video is too expensive and too slow for mass output today. **Now is a data-building mission.**

So every profile must carry, from sources, what a film and a class would need:
- the story and the facts, with hooks (one startling concrete fact per page),
- how it is danced (posture, footwork with counts, arms, hips, formation, partnering, signature moves, difficulty, what to avoid),
- how the music is built (tempo, meter, rhythm pattern, instruments, vocal style, form, mood, a sound description a composer could work from, verified reference recordings — so new music *in the style* can be made without copying any recording),
- costume and setting, occasions and meaning, notable figures, variants, lineage,
- a lesson ladder (3 levels, drills), story beats for a 5-minute episode, an instructor persona, visual motifs,
- licensed images, a good hero video, tutorials, typed connections to other dances,
- and every factual sentence traceable to a quote in a source that was fetched and checked.

"Complete" is never final: pages keep improving as more is found. The library must **keep growing forever on its own**: find more dances (different cultures name the same dance differently — no doubles), find more about the dances we have, filter harshly, deepen, connect.

## 3. Non-negotiables

1. **Minimal expenses.** No monthly subscriptions. Gemini stays on the free tier. OpenAI is a small prepaid balance used only as a fallback. Lovable credits are precious: **the content machine must never spend them** (it never does — see §4). Never buy anything or enable billing; that is the owner's decision.
2. **No launch.** The website is published only so the owner can show the vision privately. Do not promote it, submit it anywhere, or add anything that turns it into a public launch. The first product (AI-generated classes) launches only when the owner says so.
3. **No credentials.** Never type passwords, passkeys, API keys or tokens anywhere. Secrets live in GitHub Actions and are never printed. If a key is needed, ask the owner to paste it himself (one short mission).
4. **Never connect Lovable to GitHub** (two-way sync) without the owner's explicit yes; it would create a second repo and sync surprises.
5. **Truth over volume.** A page with less, all verified, beats a page with more, some invented. Fields the sources do not cover say "not described in sources".
6. **Respect.** Cultures are described precisely and with dignity; sacred or restricted dances are flagged and handled as the sources ask.

## 4. The system map (where everything lives)

| piece | where | role | cost |
|---|---|---|---|
| **The brain and the library** | GitHub repo `DANCEATLAS/crawler` (branch `main`) | all code (`pipeline/`), all research (`research_results/`, `qc_results/`), the published catalogue the website reads (`public/catalog/`), state (`pipeline_state/`), reports (`STATUS.md`, `QC_REPORT.md`), steering (`audit_overrides.json`) | free |
| **The daily runs** | GitHub Actions, workflow `atlas_daily` (`.github/workflows/atlas_daily.yml`), cron 09:20 UTC (GitHub may delay it by hours; harmless) | runs the whole content machine and commits results back | free |
| **Models** | Gemini (free tier, key `GEMINI_API_KEY`) first; OpenAI (prepaid balance, key `OPENAI_API_KEY`, mini models only) only when Gemini is out of quota | research composer, QC judge, audit judge, hero-video vision check | ≈ $0 normal day, ≤ $0.50 worst day |
| **Video metadata** | YouTube Data API (`YT_API_KEYS`), yt-dlp | hero/tutorial/viral crawlers (older workflows `crawl`, `push_videos`, `push_tutorials`, `push_viral`) and hero QC | free |
| **Sources** | Wikipedia (en + 28 other languages), Wikidata (incl. SPARQL), UNESCO ICH dataset, Wikimedia Commons (licensed images), MusicBrainz (album verification), Internet Archive (digitised books) | evidence; quotes are verified against exactly what was fetched | free |
| **Database** | Supabase project `maojpsywvbksrwkrxmjx` (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`) | mirror of the catalogue for the app (`dances` table + edges); the pipeline writes only columns that exist; `pipeline/sql/001_pipeline_columns.sql` adds the deep ones when the owner runs it | free tier |
| **The website shell** | Lovable project "Dance Atlas" (`lovable.dev/projects/f79f3666-564d-4799-befe-8b48d1f0a007`), published at **https://dancingatlas.lovable.app** | reads `public/catalog/dances.app.json` and `retired.json` from raw GitHub at load (falls back to its bundled copy), hides retired slugs, shows the deep sections for dances that passed QC | credits only when you prompt its AI |

**Lovable credit rule.** Content never touches Lovable. The site updates itself every day from GitHub with zero credits. Lovable's AI is used only for UI changes, and only like this: (1) collect everything the UI needs into one precise specification, (2) verify the data it will show is already correct and published, (3) send **one** well-written prompt that does the whole batch, (4) check the preview, (5) publish. Never iterate on Lovable chat for small things; never ask it to "look into" something; never use it to fix data (data is fixed in GitHub).

## 5. The daily process (the living organism)

```
bootstrap → audit → discover → research → qc → hero_qc → build → sync → report → commit
```
- **audit** — cleans what is already in the catalogue: deterministic rules (shared Wikidata id / article, country names, exact name collisions, research notes) + a model judge in batches of 8. The judge may only *retire* clear non-dances (country, place, TV show, company, person, song, festival, category page, ≤ 25 per run); music genres, instruments and "other" go to `QC_REPORT.md` for a human. Merges always end at a live entry; cycles are resolved. `audit_overrides.json` (`keep` / `retire` / `merge:<slug>`) always wins.
- **discover** — harvests candidates from Wikidata (dance classes), Wikipedia dance categories and list pages, UNESCO titles; de-duplicates by slug, name, alias, Wikidata id and fuzzy name; queues `DISCOVER_MAX_NEW` a day (thousands remain deferred — breadth is not the bottleneck, research depth is).
- **research** — for `RESEARCH_NEW` new candidates + `RESEARCH_ENRICH` thinnest existing pages: fetches the evidence (above), hands it to the model with the editorial rules (`pipeline/research.py`, `EDITORIAL`), gets the structured profile including the movie-ready layer, verifies every claim's quote mechanically, verifies albums in MusicBrainz, computes `movie_ready` and the `class_checklist` (17 things a fun class needs; the missing ones are handed to the next pass as "gaps to fill"). Records carry `schema` (currently 4); older records are re-deepened once.
- **qc** — deterministic gates (claims ≥ 6 at ≥ 75 % verified or ≥ 4 at ≥ 90 %, long profile ≥ 1,200 chars, concrete insight, sources, taxonomy, banned filler and AI tells, duplicates, sacred handling) + an independent model judge (accuracy, respect, specificity, teaching value, album relevance, harm, duplicate suspicion). Verdicts: `publish` / `review` / `reject`. One soft miss is tolerated when the judge scores ≥ 8.5. If the judge is unavailable, an earlier judge reading of the same research is reused.
- **hero_qc** — checks hero videos (public, embeddable, HD, not a music video, title names the dance) and the frame itself with a vision model; failures are blocklisted and replaced by the best challenger or sent for re-crawl. A pass without the vision check is not a check (re-queued).
- **build** — writes `public/catalog/` (what the website loads) and `dance_list.json` (what the crawlers work from); refuses to publish if the catalogue would shrink by > 10 %.
- **sync** — mirrors to Supabase. **report** — rewrites `STATUS.md` and `QC_REPORT.md`.

Budgets (workflow env): `RESEARCH_NEW=25`, `RESEARCH_ENRICH=15`, `HERO_QC_BUDGET=60`, `DISCOVER_MAX_NEW=40`, `AUDIT_LLM_BUDGET=150`. ≈ 170 model calls a day.

## 6. Quality standard (what "harshly filtered" means here)

- Every claim has a verbatim quote from a fetched source and is checked by code before any model judges it.
- No filler ("rich heritage", "arguably"), no AI tells, no exoticising, one concrete hook per page.
- Doubles are caught at discovery (name, alias, fuzzy, Wikidata id), at audit (shared ids, overrides) and at QC (duplicate suspicion).
- Anything uncertain goes to `QC_REPORT.md`. The AI operating this is expected to **decide those itself** where knowledge allows (write the decision into `audit_overrides.json`), and ask the owner only about taste, money or policy.
- Open policy dials asked of the owner on 30 Oct (set them in the code once answered): variants as separate pages or sections; teaching steps for sacred dances (currently withheld); breadth vs depth split (currently 25 new / 15 deepened).

## 7. How to work on this without the owner (practical)

- **Read first**: `STATUS.md` (one page), `QC_REPORT.md` (the queue), `HANDOFF_V32.md` (history and decisions), `PIPELINE.md` (stages), this file.
- **Change code**: the owner's Chrome is signed in to GitHub; commits are made through GitHub's "Upload files" page (`/upload/main/pipeline`), fetching the live file, applying exact text replacements, checking the SHA-1 of the result, then "Commit changes". Always `python3.11 -m py_compile` and run `python -m pipeline.run selftest` (offline) before committing — the runner is Python 3.11. Verify after commit by fetching `https://raw.githubusercontent.com/DANCEATLAS/crawler/<commit>/…`.
- **Run by hand**: Actions → `atlas_daily` → Run workflow (stage `daily` or one stage; small budgets for tests). Logs: run page → job → raw log.
- **Steer**: one line in `audit_overrides.json`. **Re-judge everything**: bump `PIPELINE_VERSION` in `pipeline/common.py`. **Re-deepen everything**: bump `RESEARCH_SCHEMA` in `pipeline/research.py`.
- **Quota**: free-tier 429s are read by type (per-minute → wait and retry; per-day → retire the model for the run); the model list is discovered at run time; two models per tier. If OpenAI logs `insufficient_quota`, the balance is gone: nothing breaks, growth slows; tell the owner once, do not nag.
- **Website**: after a build, the live site shows "Catalogue updated <date> · N dances". If the site needs a UI change, follow the Lovable credit rule in §4.
- **Reporting to the owner**: only when needed; otherwise silence is correct. Never recap every step.

## 8. The hand-over to video, when the day comes

Everything needed is in `public/catalog/profiles_v2.json` (+ `research_results/*.json`): sections, teaching, `music_profile`, `movement_profile`, `episode_brief`, `connections`, verified albums, licensed images, claims with sources, `movie_ready` flag. The job then is to feed these records — not re-research them — into whatever generator the owner chooses, with original music made *in the style* (never copies), original characters, and the lesson ladders as the class scripts. Until that day: grow the library, deepen it, keep it true.

— end of brief —

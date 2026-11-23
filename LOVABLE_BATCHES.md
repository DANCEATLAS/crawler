# Lovable credits — the plan to use every expiring credit well

_Written 21 November 2026 by Claude, on the owner's direction of that day. This file is where website batches are prepared and where the cost of each is recorded. It supersedes `LOVABLE_UI_PROMPT.md`._

Owner, 21 November 2026, on the credits: _"if they expire - we need to use them to the max best most economical but use all. devise the most effective plan to ensure this happens to support vision, so learn vision to its deepest level."_

Owner, 21 November 2026, on the direction, after seeing a first plan: _"the concept of the payment should be completely erased now to not confuse matters. What we want right now are an extreme robust app. … I thought at the beginning to represent it as a profiles that people click on their phone, but … people are not going to enjoy learning to dance like that. We need to be cutting edge with our knowledge of the dance and the education of it, and be ready for the breakthrough in the technology that will allow us to create this interactive and then just overnight basically activate all the profiles. So whatever needs to happen that you've researched into the Lovable app, this is the vision that you must follow."_

**Status.** Erasing payment and making the app robust are the owner's explicit orders. The other batches follow from his order to use every expiring credit in support of this direction; he can stop or reorder them at any time.

## 1. The facts (measured 21 November 2026)

- Lovable balance **93.6 credits**: **90.9 rollover credits expire on 28 November 2026** (the grant of 28 September); 2.70 top-up credits last until 15 May 2027.
- Order of spending (Lovable's documentation and the balance window agree): the 5 free build credits of the day first, then the credits closest to expiry. The top-up credits are touched last.
- 237.6 credits have already expired unused (3.30 on 28 July, 100 on 28 August, 55.3 on 28 September, 79 on 28 October).
- The yardstick: the last build message (26 October) cost **6.20 credits** and ran 5 min 43 s. 90.9 credits are about fourteen batches of that size. A message pauses with a question when it passes 20 credits.
- The workspace plan is "Lite", €5 a month, renewing 28 November. Not changed by this plan; the owner has been told.

## 2. What the direction asks of the website

1. **The site is a window, not the product.** The product will be BDF as an agent in a full, virtual-reality conversation that draws on the whole library and on the education of how to teach. No credit goes into a click-to-learn experience.
2. **No payment, no accounts.** Nothing that sells, signs in, collects e-mail or presses.
3. **Extremely robust.** Loading that cannot break and does not slow when the atlas is ten times larger; no blank screen; one source of data; a page that shows the health of every data file.
4. **The knowledge on display, truthfully.** The mentor's DNA, the whole profile of each dance, the starting line: what the future agent will draw on. Placeholders hidden, counts from data, machine readings labelled, sacred dances story only, no ranking that pretends to be popularity.
5. **Ready for the breakthrough.** The site reads the library through the same documented door a future agent will use (`public/catalog/`: manifest, index, one complete file per dance, the teaching DNA). The site working is the proof that the door works.
6. **Bought once.** A screen fills itself from GitHub every night; words live in `site.json`. Later changes need no credits. Nothing costs money to run: no Lovable Cloud, no AI calls, no backend.
7. **The owner sees the machine in large type, in Hebrew,** without asking an AI.

## 3. What the site shows today against what the machine makes

| The machine has (public files) | On the site today |
|---|---|
| 1,244 dances, short story, pictures, lesson links | shown |
| 476 deep profiles: eight story sections, music, movement, connections, footage, checked claims | not shown |
| Steps with counts, cues, common mistakes from 170 studied lessons of 108 dances | not shown |
| The starting line: 32 active-ready, 80 within two items | not shown |
| The mentor's DNA: 549 teachers ranked, 51 lessons studied, 236 moments, 106 research findings | not shown |
| The direction itself (BDF, the two missions) | not shown |

Also measured: the whole catalogue (5.2 MB, growing 0.16 MB a night) is loaded for every visitor and kept in the browser's session store, which holds 5.24 million characters; 4.93 million are used. In about two nights the store is full; the site keeps working but then loads the full file on every page load, slower every night. The site offers paid membership ($3.60 a month, $36 a year, $180 lifetime), a 14-day trial with pop-ups, an e-mail pop-up, an influencer call, referral codes and a sign-in that opens when a heart is tapped. The Viral page shows rank numbers although the order is by date. The Atlas page counts 213 "countries" because joined names count as their own; the tree puts 977 of 1,244 dances into one family.

## 4. Rules of every batch

1. One prepared, complete batch per message. The data it reads is live on GitHub before the message is sent. No small iterations; if Lovable is unsure it takes the simplest reading and says so.
2. Read-only screens. No backend, no Lovable Cloud, no AI gateway, no analytics, no new dependency unless named. No payment, no sign-in, no e-mail field.
3. Every visible word of a new screen comes from `public/catalog/site.json` (`da_site_v1`) through the shared helper `t(path, fallback)`. Machine keys are shown with underscores replaced by spaces and the first letter capitalised, so new keys need no build.
4. Empty, "not described in sources", "unknown" and "null" are never rendered: no heading, no empty card.
5. Sacred or restricted dances: story only, one calm line where teaching material would be.
6. Machine readings are labelled as such, with the link to the video moment or the source. No number is typed into the code.
7. Every data request has a timeout and a calm fallback. No screen may go blank.
8. After the build: check the preview against the data, run the fixed check of the old pages (home count, atlas, one dance page, viral, a retired slug, a saved heart), publish, record the cost here.
9. A batch changes what a component shows, not what it is built on: a working sheet, chip or tile keeps its present component unless the batch says otherwise (learned with batch 8).
10. Every check is made on the built preview (`preview--dancingatlas.lovable.app`), which is what gets published. Lovable's own check runs on its dev server and can pass while the built page is wrong; the built preview follows a change by a minute or two (the name of the stylesheet in the page changes when it has).

## 5. The batches, in order of value

| # | Batch | What changes | From the direction | Data | Est. credits |
|---|---|---|---|---|---:|
| 1 | **Payment and accounts erased** | Membership, prices, trial, pop-ups, e-mail capture, influencer call, referral codes and sign-in are removed from code and screens. Hearts save on the device at once. "Profile" becomes "Saved" | "completely erased now" | `site.json` | 6 |
| 2 | **Loading that cannot break** | One door: a light index and one file per dance. The last good copy is kept in the browser's own database instead of the full session store. Timeouts, fallbacks, no blank screen. `/health` shows every data file and its contract | "extreme robust app"; thousands of profiles | `manifest.json`, `index.json`, `d/<slug>.json` (built 21 November; live with the first run of the stage `door`) | 11 |
| 3 | **The mentor** (`/mentor`) | The teaching DNA with its evidence, what a teacher does when a learner struggles, the six moments, beliefs, feelings, what BDF keeps in mind about a person, the teachers and the research | "cutting edge … the education of it"; mission 2 | `bdf_teaching_system.json` (live) | 6 |
| 4 | **The whole profile** | On the dance page: story in eight parts, music, movement, what the machine has gathered for teaching (steps with counts, cues, common mistakes, each with the lesson it came from), connections, footage, pictures, "N of M claims checked", and the meter "15 of 15: ready to activate" or what is missing. Shown as knowledge, not as a class | "drawing from all the database"; V12, V13 | `d/<slug>.json` | 9 |
| 5 | **The starting line** (`/starting-line`, and on Home) | How many profiles are ready to be activated, the ladder from listed to ready, the closest ones with what each needs, what holds pages back, growth over time | "overnight activate all the profiles"; mission 1 | `active_ready.json` (live), `machine.json` (to make) | 6 |
| 6 | **The machine room** (`/machine`), in Hebrew | For the owner, large type, right to left: did last night work, how fast it grows, how far the mentor's study has come (topics read, what is read next, his topics of 21 November), what needs him | V16, V17; he reads Hebrew faster; "endless research … embedded" | `machine.json` (with `study`), `site.json` (`pages.machine`, `he.items`, `he.topics`) | 5 |
| 7 | **The direction, in the owner's words** (`/vision`, and on Home) | What Dance Atlas prepares: BDF as an agent in conversation and virtual reality; now, next (a beta for people of dance culture and music), later; why a mentor; the two missions; why there is no course and no price; the door for any AI (the link to the manifest and to `/health`) | owner, 21 November, morning and afternoon; gate 10 | `site.json` (`pages.vision`) | 5 |
| 8 | **Truth repairs: the Viral list** | Read from `viral.json` on GitHub; the database client leaves the app, which then has no backend at all; the three identical "charts", every rank number and "How ranking works" go; the order is named for what it is; who made each, how it spread and the sources are shown | V02, V08; "extreme robust app" | `viral.json` (the stage `door`, from the repository's verified list, `viral_categories.json`) | 7 |
| 9 | **Truth repairs: countries and families** | Atlas and Flags by ISO country from the index (a dance under every country it belongs to; no joined name as a country; 153 countries, not 213); the tree shows dances without a family as "Family not yet known" (774), not inside "Folk & circle"; Home no longer promises a map; an address that does not exist says so. (The door page that had this number was folded into batches 4 and 7) | V02, V09 | `index.json` head: `regions`, `places`, `no_place`, `families`, `no_family` | 6 |
| 10 | **Speed and access** | A smaller first load (pages on demand; the old bundled catalogue goes once the browser keeps its own copy), lazy pictures, keyboard and screen-reader use, reduced motion, text size | robust; V03, gate 4 | none | 7 |
| | Fixes found in the checks | | | | 9 |
| | **Planned** | | | | **75** |
| R1 | The teachers' hall | Each studied teacher: system, signature, lessons, moments | mission 2 | `bdf_teaching_system.json` | 5 |
| R2 | The research library | Every research note and paper, with its quotes, by teaching practice | mission 2 | `bdf_teaching_system.json` | 5 |
| R3 | How the atlas is made | The filter, what was rejected and why, why some dances are story only | V12 | `stats.json` (live) | 4 |
| R4 | Search that knows other names | Aliases, native names, countries, "ready to activate" | V02 | `index.json` | 4 |
| R5 | The window works without a connection | After a first visit the site opens and browses offline | robust | none | 8 |
| R6 | Episode scripts on screen | Episode 1 and three chapters per dance, as drafts | movie phase | `episodes/<slug>.json` (live) | 7 |
| | Small finishing items | Sized 0.5 to 2 credits, to land on zero | | | as needed |

Left out on purpose, because they belong to the click-to-learn app the owner ruled out: a practice player, a printable lesson sheet, a guided "find a dance" chooser, a camera mirror, two dances side by side, the shell translated into other languages.

Batches are sent in the order their data is ready: 1 and 3 need nothing new; 2 and 4 wait for the machine-side files of section 7.

Changed on the afternoon of 21 November, on the owner's words of that afternoon (`PRODUCT_VISION.md`, points 8 and 9): the site is where he looks at the material comfortably and, later, a possible beta; what he cares about most is the mentor's research. So the machine room (6) also shows how far that research has come, in Hebrew; the direction page (7) carries why a mentor and the beta as the next stage; the separate door page (9) is folded into 4 and 7.

The reserve is longer than the budget on purpose: estimates can be wrong in both directions, and the free 5 credits of each working day are spent before the expiring ones.

## 6. The meter: how every credit gets used

- After each batch: read "Credits used" under the answer and the rollover line in the balance window; write both into the record below.
- Targets for the rollover credits spent (Japan time), as replanned on 23 November: Sat 21 Nov 71.7 (done) · Mon 23 Nov about 81 · Tue 24 Nov about 90 · Wed 25 Nov 90.9. Thursday 26 and Friday 27 November are spare days. Expiry is Saturday 28 November.
- More than 10 behind a target: the next two batches go in one working session, or a reserve item is moved up. A batch far over its estimate: the last reserve items fall away.
- The last credits go to small finishing items until the rollover line reads 0. The 2.70 top-up credits are left alone.
- A message that passes 20 credits pauses with a card: continue only when the work shown is on the batch.

**The pace, corrected on 21 November at 17:30.** That afternoon I planned one batch a day so that each would use the day's 5 free credits first, and told the owner so. The arithmetic was wrong for the goal: a batch of about 8 credits then takes only about 3 from the expiring ones, and about 40 would have expired unused. The free credits are extra capacity, not a reason to slow down. The owner the same evening: the main thing is that the Lovable credits are used, within the coming week, with the most meaningful effect on the project's future. So: **two batches a day**, at least one every day (to take that day's free 5), front-loaded when Chrome is open. With 57.5 expiring credits and five free credits on each of five days, about 82 credits of building remain, which is the six planned batches and the reserve.

| Day (Japan) | Batches | For the project's future | Expiring left after |
|---|---|---|---:|
| Sat 21 Nov (done) | 1, 3, 2, 4 · 5 The starting line · 6 The machine room in Hebrew · 7 The direction · 8 The Viral list, with three repairs · 9 Countries and families | no payment; a window that cannot break; the whole profile; mission 1 visible; the founder sees the machine and the study in Hebrew; the direction in his words; a truthful window with no backend at all | 19.2 |
| Sun 22 Nov | none: no browser was connected that day, and its 5 free credits were not used | | 19.2 |
| Mon 23 Nov | C The research library, in Hebrew, the owner's three strands first · B The mentor in Hebrew | he sees the research he asked for being read, and reads the teaching DNA in his own language | about 10 |
| Tue 24 Nov | A What an agent receives, on every dance page (with: no family chip where the family is not known) · 10 Speed and access (with: no flash of the old grouping, an unknown dance address says so) | the bridge to BDF made visible; ready for a beta | about 1 |
| Wed 25 Nov | D Search that knows other names, sized to what is left plus the day's free 5 | the material is easy to find | 0 |
| Thu 26 and Fri 27 Nov | spare days: E (the window works without a connection) only as far as the free credits of the day carry it | the expiring line at zero; the 2.70 top-up credits untouched | 0 |

**Found while checking batch 9, for the next batches.** (1) The dance page shows the chip "Folk" for a dance that has no family: 372 published pages say so untruly; batch A removes the chip where `family` is missing. (2) On a first visit, until the index arrives, the Atlas pages show the old grouping from the copy bundled with the site (Lovable's choice, so that no screen is blank): batch 10 shows a calm loading line instead. (3) An address of a dance that does not exist shows only "Back to Atlas": batch 10 says that the dance is not in the atlas. (4) Machine side: one card (`american-smooth`) carries a one-line description that belongs to a list, not to the dance.

Batch 8 was split in two when it was written: 8 is the Viral list (read from GitHub, the database client removed, no rank), and the number 9, free since the door page was folded away, is countries and families. A, B, C, D and E are prepared in that order (messages below as they are written). A: the episode and the activation dossier of a dance, shown as what a teaching agent would be handed (`d/<slug>.json`, `active_profiles.json`). B: the mentor page read in Hebrew (`/mentor?lang=he`): its fixed words and its vocabulary from `site.json`, the evidence left in English and marked as such. C: the research notes and papers by the founder's three strands, what is read and what waits (R2). D: R4. E: R5. The teachers' hall (R1), how the atlas is made (R3) and the episode scripts (R6) follow if credits remain.

## 7. Free work on the machine side: the door

All of it is GitHub work, tested, merged by pull request, no model calls, no cost. It is also the foundation of the owner's direction, with or without a website: any agent on any platform reads the library through these files.

| File in `public/catalog/` | Contract | Holds | Made by |
|---|---|---|---|
| `site.json` | `da_site_v1` | every word of the newer screens | written by hand (live with this file) |
| `manifest.json` | `da_manifest_v1` | the one address to start from: every file, its contract and size; eight standing rules for any agent; where the safety copy is | stage `door`, after `readiness` (built 21 November) |
| `index.json` | `da_index_v1` | every dance in a few fields: names, places, family, status, state from listed to active-ready, the address and fingerprint of its file | stage `door` |
| `d/<slug>.json` | `da_dance_v1` | everything about one dance: identity, story, music, movement, what was gathered for teaching with its sources, readiness, media, connections, limits | stage `door` |
| `viral.json` | `da_viral_v1` | the Viral list (today read from Supabase at run time) | an export in the stage `sync` (to build, before batch 8) |
| `machine.json` | `da_machine_v1` | nightly history, pace, what holds pages back, the closest dances, the owner's lines | stage `door` |
| `bdf_teaching_system.json` | `da_bdf_teaching_v1` | the mentor's DNA (live) | stage `teaching` |

## 8. Risks

- **A batch breaks an old page.** Each message says "change nothing else"; the fixed check runs before publishing; Lovable's history restores the earlier version at no cost.
- **Costs differ from the estimate.** The first batch is the measurement; the meter adapts.
- **The browser is closed.** The work runs through the owner's Chrome. On working days the Mac stays awake with Chrome open.
- **Running costs.** None: no screen calls a paid service.
- **Knowledge shown before a person checked it.** Every such block says so, sacred dances are excluded, nothing is promoted.

## 9. For the owner

- **PLEASE NOTE:** Lovable charges €5 a month for the plan "Lite"; the next charge is 28 November.
- **PLEASE NOTE:** the rows of the Supabase tables for memberships, influencers and referral codes, and any sign-up e-mail addresses, stay in Supabase until he says they may be deleted.

## 10. Record

| Date | Batch | Credits used | Rollover left | Checked | Published |
|---|---|---:|---:|---|---|
| 21 Nov | (start) | | 90.9 | | |
| 21 Nov | 1 Payment and accounts erased | 7.90 | 88.0 | In the preview: the old addresses (`/membership`, `/c/…`, `/auth/callback`, `/terms`) redirect; the Saved page and the privacy text come from `site.json`; a heart saves at once with no prompt; Viral 154; Atlas 1,244; no payment or sign-in wording left in the interface code | yes |
| 21 Nov | 3 The mentor page (`/mentor`, "BDF" in the navigation) | 7.30 | 80.7 | In the preview against the data file: 23 of 23 rules, 8 cards, 6 moments, the six numbers equal, 87 outside links all open in a new tab, nothing stored in the browser, the proof panels open | yes |
| 21 Nov | 2 Loading that cannot break | 15.7 | 65.0 | In the preview: only `index.json` is loaded at start (0.6 MB in place of 5.2 MB), a dance page fetches its own file and the next one, the two large session-store entries are gone, the browser database `da_library_v1` holds the last good copy, a retired address redirects, `/health` reads "Health: OK" for six files, Atlas 1,244, Viral 154, saved hearts kept, a dance page identical to the live one before | yes |
| 21 Nov | 4 The whole profile on the dance page | 7.30 | 57.5 (balance page, 15:55) | In the preview against the dance files: `/style/hustle` (chips "Ready to activate" and "Living"; the story in eight parts; music with three album links; movement; six basic steps; two lesson panels and one performance panel, closed, 11 links to the moment in the video; "15 of 15"; adaptations closed; five connections, four of them linked; three footage links, no embed; three lesson links in place of "Tutorials coming soon"; "8 of 8 claims checked"; the link to the dance's own file; all 16 outside links open in a new tab), `/style/ahwash` (story only: no movement, teaching, adaptations or lesson links; the reason; "6 of 6" under "How complete is the story?"), `/style/salsa` (listed: one lesson panel, lesson links, no chip), `/style/country-swing-dance` ("In the making · 13 of 15", two items missing). Old pages: home 1,244, atlas, viral 154, `/style/rumba` to `/style/cuban-rumba`, `/health` OK, `/mentor`. **Two repairs found**, sent with batch 5: the browser database keeps trimmed copies of files, so a dance opened before this batch showed no profile until its copy was removed; and signature moments of a performance are objects, which my message described as texts, so their label shows without values | yes |
| 21 Nov | 5 The starting line, with two repairs | 7.20 | 50.3 | 6 min 47 s. In the preview against `machine.json` and the index: 32 ready, "+6.8 a night, measured over the last 4 days", the ladder 1,244 / 589 / 476 / 87 / 39 / 41 / 32, 32 cards, 12 closest rows, 14 bars with their numbers, three charts (5 to 32, 359 to 476, 91 to 170), one new request (`machine.json`); Home strip "32 dances ready to activate · The starting line →" with no new request. Repairs: only the database `da_library_v2` exists and the stored Hustle file is whole (14 keys); the signature moments of the Hustle performance show at 0:23, 0:36 and 1:53 with links to the moment. Old pages: home 1,244, atlas, viral 154, the retired address, `/health` OK with the new database, `/mentor`, a saved heart kept. Live: the page, the strip, a dance that had a trimmed copy | yes |
| 21 Nov | 6 The machine room, in Hebrew | 5.70 | 44.6 | 3 min 28 s. In the preview against `machine.json`: the page reads right to left (`lang="he"`, body 20 px, titles 28 px), dance names and English notes left to right; "לא צריך ממך כלום…" in the green card; the last night 20.11.2026 "הלילה עבד", 141 minutes, 242 questions, 0 unanswered, 13 stages; the library numbers; the pace +6.8 / +29.2 / +22.2 over 4 days; the study: 24 of 80 topics, 0 of the owner's 14, 9 papers, 51 lessons, 45 teachers, 106 findings, 23 of 34 practices, and the six topics read next under their Hebrew names; 14 bars and the closest dances with Hebrew item names; 14 nights; the links to `/starting-line`, `/mentor`, `/health`, and the link to `/machine` at the end of `/starting-line` and `/health`. Old pages unchanged. Live: the page opens in Hebrew | yes |
| 21 Nov | 7 The direction, in the founder's words | 3.10 | 40.3 (balance page, 17:50; 1.2 less than the three "Credits used" figures of the evening add up to) | 1 min 56 s. In the preview: `/vision` with the title, two pull quotes (the second marked as translated from Hebrew), Now / Next / Later, why a mentor, what is not here, sacred dances, open to any AI with the link to the manifest (new tab) and to `/health`, "32 / 1,244" after Mission 1, the honesty line; no new request. Home strip: "32 dances ready to activate · The starting line → · Where this is going →". Old pages unchanged. Live: the page opens | yes |
| 21 Nov | 8 Truth repairs: the Viral list | 7.70 | | 4 min 55 s. On the built preview against `viral.json`: "All 154" and seven category chips with the file's numbers (the empty "Flashmob IRL" is gone); 154 cards in the file's order (first: KPop Demon Hunters — Soda Pop / Golden, Anxiety, Bad Bunny; last: The Woah); no tabs, no rank, no "NEW", no "How ranking works", no "Tutorials coming soon"; the line "In order of when each began, newest first. This is not a ranking."; the page head without "top", "chart" or "ranked"; the details in order (story, Watch, how it spread, at its height, also danced by, the song, more videos as links, sources by host name); two cards without a video and two without a year show nothing in their place; data requests go to `raw.githubusercontent.com` only, no database host; `/health` lists `viral.json` (304,915 bytes); a saved challenge shows on Home and on the Saved page (`/profile`). Old pages unchanged. **One fault:** the details sheet was off the screen (next row) | after the repairs |
| 21 Nov | 8a, 8b, 8c Repairs of that sheet | 2.10 + 1.60 + 3.00 | 25.8 (balance page, 18:40; 28.5 in all) | 1 min 48 s, 50 s, 4 min 8 s. Batch 8 rebuilt the working sheet on the shared Dialog, whose Tailwind classes move it by half its size (`translate: -50% -50%`); the box sat at left -700 px, top -232 px in a 1400 × 724 window. 8a and 8b each passed Lovable's own check and failed on the built preview: the production build lowers a hand-written `translate: none` into `transform`, which does not cancel the separate `translate` property. 8c named that cause and gave a build-safe repair (`translate-x-0 translate-y-0` on the element, and the two `--tw-translate` variables in the rule). On the built preview and live: the sheet at left 0, top 127 px, full width, `translate` 0, Close button, Escape closes, the sources reachable by scrolling | yes, 18:38; live checked: the page, the sheet, no database host |
| 21 Nov | 9 Truth repairs: countries and families | 6.60 | 19.2 (balance page, 19:05; 21.9 in all) | 13 min 25 s. On the built preview against the head of `index.json`: Atlas "1244 DANCES · 153 COUNTRIES"; twelve regions in the file's order with 35, 14, 34, 11, 4, 3, 10, 7, 6, 9, 5 and 15 countries; "Place not yet known 33" with 33 dances; France 45 dances "· EUROPE", Japan 21 "· EAST ASIA", each list sorted and without doubles; Flags 153 tiles, no flag twice, a tile opens its country's list (Albania 4); Tree: 34, 203, 2, 23, 40, 14, 137, 17 and "Family not yet known" 774; Home "1244 traditions still danced today. By country · By flag · By family"; `/map` reads "This page does not exist" with the way back; `/saved` leads to the Saved page. Old pages: Viral 154 with its sheet in place, a dance page, a retired address, `/health` OK, `/mentor` | yes, 19:03; live checked: Atlas, Flags, Tree, Home, `/map` |

### How a message is sent (learned on 21 November)

The chat field of Lovable is a rich-text editor. Put the text in with `document.execCommand('insertText', false, text)` on the focused field: the page can fetch the text of a batch straight from this file on main. A synthetic paste event turns the text into an attachment, and typing it key by key would send it at the first line break. Check that the field holds the whole message and that the mode is Build, then press Send. The cost is in the menu "More options" under the answer (it opens on the second click). Of the free 5 build credits of the day, the first batch uses them all.

**The built preview, not the dev server (learned with batch 8).** `preview--dancingatlas.lovable.app` serves a production build, the same kind that is published; it follows the agent's last change by a minute or two (compare the name of the stylesheet in the page, or look for the change itself, before judging). Lovable's own check runs on its dev server. The two can differ: the build minifies the CSS and rewrote a hand-written `translate: none` into `transform: translate(0px)`. A repair that depends on CSS is written with Tailwind utilities on the element or with Tailwind's own variables, and is accepted only on the built preview. A repair message says what was measured, in which window, and what the accepted measurement is.

## Batch 1 — the message

```
BATCH 1 — PAYMENT AND ACCOUNTS ERASED. Ordered by the owner on 21 November 2026: "the concept of the payment should be completely erased now". Read the Project instructions first. Do exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

REMOVE COMPLETELY — code, routes, components, hooks, styles, texts, storage keys and database calls, not only the visible parts:
1. Membership and prices: the /membership page, every plan, price, renewal or refund text, every Stripe or checkout reference, every link or button that leads there.
2. Trials and entitlements: the trial start, the "Trial: N" pill, "free days left", "Extend my trial", "Last chance", "Claim my month", every entitlement or tier check, and anything that locks, limits, blurs or times any content. After this batch every screen is open to everyone, always.
3. E-mail capture: the e-mail pop-up and every form that asks for an e-mail address.
4. Influencers and referrals: the "Are you an influencer?" block, influencer accounts, referral codes, "courtesy of your creator", the route /c/$code.
5. Accounts: the magic-link sign-in, "Continue with Email", the sign-in sheet that opens when a heart is tapped, /auth/callback, every auth listener and session check. No sign-in exists anywhere after this batch.
6. The Supabase tables entitlements, influencer_accounts and referral_codes are no longer read or written by the app. Do not delete or change anything in Supabase. The Viral page keeps reading viral_chart exactly as today: keep the anonymous Supabase client for that only.
7. The browser storage keys that only served the above (dw_trial_start, dw_trial_extended, dw_last_chance, dw_entitlement, dw_email_popup_seen, dw_influencer_app, dw_referral, dw_supabase_auth and any Supabase auth token key): no longer read or written; remove them once at app start if present.

KEEP WORKING, UNCHANGED
- Hearts: saving a dance or a viral challenge works at once, on the device, with no prompt of any kind. "My styles" and "Fav viral" on Home keep working with what is already saved.
- The catalogue loading, the atlas, the tree, the flags, the dance pages, search, the Viral page and its data.

WORDS
Make one small shared helper, t(path, fallback): it fetches https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/site.json (contract "da_site_v1", a few KB) once per session (memory, plus sessionStorage key da_site_words_v1) with a 6-second timeout, and returns the string at a dotted path, or the fallback when the file, the path or the fetch is missing. Later batches reuse it. Use it for the words below.

REPLACE
- /profile becomes a simple page of saved items and nothing else: title t("pages.saved.title","Saved"), lead t("pages.saved.lead","The dances you saved, kept in this browser only."), then the saved dances under t("pages.saved.dances","Dances") and the saved viral challenges under t("pages.saved.viral","Viral"), with the empty lines t("pages.saved.empty_dances","Tap the heart on any dance to keep it here.") and t("pages.saved.empty_viral","Tap the heart on any viral dance to keep it here."). The navigation item is renamed from "Profile" to t("nav.saved","Saved") in the top bar and the bottom bar; the route stays /profile.
- /membership, /auth/callback and /c/<anything> redirect to the home page, so an old link never shows an error.
- /terms is removed and redirects to /privacy. /privacy shows only: title t("pages.privacy.title","Privacy") and the text t("pages.privacy.body","Dancing Atlas is a private demonstration. It has no accounts and asks for no personal information. The dances you save stay in this browser only. Videos are played by YouTube; the dance library is read from GitHub and the Viral list from Supabase. Like any website, these services and the host of this site receive the technical information a browser sends when it loads a page.").
- Remove every link to Terms and to Membership from footers and menus.

ALSO
- Remove dependencies that nothing uses after this (for example a Stripe package). Do not remove the Supabase client.
- Search the project's own code and interface texts (not the bundled dance data) for these words and leave none: membership, member, trial, entitlement, founding, lifetime, renew, refund, checkout, stripe, influencer, referral, creator code, magic link, sign in, sign up.

WHEN DONE
Report: the files deleted, the files changed, the dependencies removed, the result of the word search. Confirm in the preview that (a) tapping a heart saves without any prompt, (b) /membership and /c/test go to the home page, (c) /profile shows the saved items only, (d) Home, Atlas, a dance page and Viral look and work as before, (e) no console error.
```

## Batch 3 — the message

```
BATCH 3 — THE MENTOR PAGE (new route /mentor). Read the Project instructions first. Build exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHAT IT IS
A read-only page that shows what the nightly research has learned about how to teach anyone to dance. All content comes from one public JSON file. All words come through the helper t(path, fallback) made in batch 1 (site.json), with the fallbacks written here. No backend, no Lovable Cloud, no AI calls, no analytics, no new npm dependency. Do not change any existing page or the catalogue loading.

DATA
Content: https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/bdf_teaching_system.json — contract "da_bdf_teaching_v1", about 320 KB, rebuilt every night. Fetch it only when /mentor opens, with a 10-second timeout. Keep it in memory for the session. Do NOT write it to sessionStorage or localStorage (that store is nearly full). If the fetch fails or "contract" differs, show the page header and one calm line t("pages.mentor.unavailable","The mentor's notes could not be loaded just now. Please try again in a moment."). Never an error screen.
Keys such as "feel_and_groove" or "self_doubt" are shown by replacing underscores with spaces and capitalising the first letter, unless site.json has tags.<key>. Never keep a list of known keys: new ones arrive without a build.

FIELDS USED
counts {teachers_ranked, teachers_studied, lessons_studied_for_method, comments_read, science_findings_checked, practices_total, practices_with_two_or_more_kinds, practices_with_all_three, mentor_moments}; generated_at; new_in_7_days {lessons, teachers[], research_notes};
dna[] {theme, tag, do, evidence_kinds (2 or 3), teachers, families, learner_comments, research_notes};
practices[] {tag, meaning, do, share_of_lessons (0–1), learner_themes[] {kind, theme, count}, science[] {topic, principle, for_the_teacher[], sources[] (urls)}, examples[] {teacher, dance, t, what, url}};
adjustments[] {tag, comments, learners_say[], teachers_offer[] {difficulty, adjustment, teacher, dance, url}, research[]};
mentor {voice[] [word, count]; moments[] {moment, title, seen, teachers, examples[] {says, teacher, dance, url}}; creed[] {about, title, teachers, beliefs[] {belief, teacher, dance, url}}; feelings[] {feeling, seen, responses[] {response, teacher, dance, url}}; what_stays[] {says, teacher, url}; meant_to_learners[] {theme, count}};
learner_model[] {remember, seen_most[] [key, count]};
teachers[] {rank, teacher, score, praise, complaints, lessons_found, methods_studied, system, signature, dances[]};
science[] and papers[] {topic, principle, findings[] {finding, quote, source}, for_the_teacher[], when_it_does_not_apply, sources[] {url, title, authors, year, journal}}.
Any array may be missing or empty: then its block is not rendered at all (no heading, no empty card). Unknown extra fields are ignored.

THE PAGE, top to bottom (mobile first; the existing fonts, colours and spacing; accent #CC785C; body text never smaller than 16px on this page)
A. Header. Eyebrow t("pages.mentor.eyebrow","BEST DANCE FRIEND"). H1 t("pages.mentor.title","A mentor that can teach anyone to dance"). Lead t("pages.mentor.lead","BDF is not built yet. First it has to learn how the best teachers teach. Every night, at no cost, a machine watches the lessons that learners praise most, reads what learners write and reads the research. This page shows what it has learned so far."). Under it a muted line: "Rebuilt <date of generated_at> · new in the last seven days: <new_in_7_days.lessons> lessons, <new_in_7_days.research_notes> research notes".
B. t("pages.mentor.stands.title","Where the study stands"): six large numbers with short labels from counts: teachers ranked; teachers studied; lessons watched; learner comments read; research findings checked; "<practices_with_two_or_more_kinds> of <practices_total>" teaching practices with two or more kinds of evidence.
C. t("pages.mentor.dna.title","The teaching DNA") with lead t("pages.mentor.dna.lead","What a great teacher does. A rule appears here only when two or more kinds of evidence agree: teachers, learners, research."). Group dna[] by theme, themes in the order they first appear. Each rule: the "do" sentence in large type; three dots filled for evidence_kinds 3, two for 2 (aria-label "all three kinds of evidence agree" / "two kinds of evidence agree"); a small line "<teachers> teachers · <learner_comments> learner comments · <research_notes> research notes". Each rule is a button that opens "The proof" from the practices[] entry with the same tag: meaning; "seen in <share_of_lessons as %> of the lessons studied"; learner_themes as chips with their counts; each science principle with its source links; examples as lines "<teacher> · <dance> · <t> — <what>" linking to url ("watch the moment").
D. t("pages.mentor.adjust.title","When a learner struggles") with lead t("pages.mentor.adjust.lead","What learners say is hard, what teachers offer for it, and what the research adds."). One card per adjustments[] entry: the tag as title; "Learners say" chips; "A teacher's answer" lines (adjustment, or "difficulty → adjustment" when difficulty is not empty; then teacher · dance, linking to url); "Research adds" lines.
E. t("pages.mentor.mentor.title","The mentor") with lead t("pages.mentor.mentor.lead","Who is teaching, beyond what is taught."):
   E1 "How they sound": mentor.voice as chips, word and count, largest count first.
   E2 "Six moments that decide whether a learner stays": mentor.moments, each an opening panel: title; "seen <seen> times with <teachers> teachers"; the examples as lines (says; teacher · dance; link). These lines describe what a teacher does: plain text, never in quotation marks.
   E3 "What they believe": mentor.creed, each heading with "<teachers> teachers" and the beliefs under it (belief; teacher · dance; link).
   E4 "When a feeling shows": mentor.feelings, each: the feeling, "met <seen> times", the responses (response; teacher · dance; link).
   E5 "What stays with the learner": mentor.what_stays as calm single lines with the teacher and link.
   E6 "What it meant to learners": mentor.meant_to_learners as lines with counts.
F. t("pages.mentor.learner.title","What BDF keeps in mind about a person") with lead t("pages.mentor.learner.lead","So that the teaching fits them better the longer they stay."): learner_model as cards: "remember" as the title, seen_most as chips.
G. t("pages.mentor.teachers.title","The teachers it learns from") with lead t("pages.mentor.teachers.lead","Ranked by what learners wrote under their lessons, never by views."): the first 10 of teachers[] (rank, teacher, "<praise> praising comments", system, signature), then a button "Show all <n>". No photos, no avatars.
H. t("pages.mentor.research.title","The research") with lead t("pages.mentor.research.lead","Findings with a quote checked against the source."): science[] then papers[], closed by default: topic; principle; "For the teacher" bullets; findings (finding, the quote in a muted block, source link); "When it does not apply" when not empty; sources (title, authors, year, journal) as links.
I. A line at the end of the page, always visible: t("pages.mentor.honesty","Machine readings, not yet checked by a person. Nothing here has been tested on learners by Dance Atlas. Every line links to the moment in the video or to the source.").
J. A sticky in-page index for the sections B to H (chips that scroll to the section); each section has an id so /mentor#dna, #struggles, #mentor, #learner, #teachers and #research work.

NAVIGATION
Add one item before "Saved" in the top bar and in the bottom bar: label t("nav.bdf","BDF"), route /mentor, an icon from the icon set already installed. Page title "Best Dance Friend — Dancing Atlas".

RULES
Read-only. External links open in a new tab with rel="noopener noreferrer". All opening panels are real buttons, usable with the keyboard, with aria-expanded. No number is typed into the code: every number comes from the file. Nothing is rendered for an empty value. Keep the page fast: render closed panels lazily.

WHEN DONE
Open /mentor in the preview and report: the number of rules under "The teaching DNA", the number of cards under "When a learner struggles", the number of moments, whether the six numbers in B equal the file, and any console error. Do not change anything else.
```

## Batch 2 — the message

Send only after `manifest.json`, `index.json` and `d/` are on main (first run of the stage `door`), and after batch 1.

```
BATCH 2 — LOADING THAT CANNOT BREAK. Ordered by the owner on 21 November 2026: "an extreme robust app". Read the Project instructions first. This batch replaces the catalogue loading described there; everything a visitor sees stays the same. Do exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHY
Today the app downloads one 5.2 MB file with every dance, grows with it every night, and keeps a copy in sessionStorage, which is now full. The library now has a door: a light index, and one small file per dance.

THE DOOR (all public, all under https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/ )
1. index.json — contract "da_index_v1", about 0.6 MB. Shape: { contract, generated_at, count, states, file: "d/{slug}.json", dances: { "<slug>": {…} }, retired: { "<slug>": "<slug it was merged into>" or null } }. Each dance entry has, under the same names the app already uses: slug, name, aliases[], tagline, country, country_code, flag_emoji, region, family, era, hero_video_youtube_id, tier, publish_gate, research_gate, unesco, lat, lng, tradition_status. New fields: countries[] (ISO codes), is_sacred (true when teaching is withheld), hero_ok, state, have, of, lessons, fp (fingerprint of the dance's file), updated. A field that is empty or false is simply absent.
2. d/<slug>.json — contract "da_dance_v1", a few KB each. Shape: { contract, slug, name, state, note, countries[], card: {…}, profile?, readiness?, lessons?, performances?, episodes?, teaching_withheld?, fingerprint, updated }. "card" is the complete entry the app used to find in dances.app.json for that dance, with the same field names (profile, insight, sources, images, albums, tutorials, video_stack, related, related_slugs, wikipedia_url, hero_qc and so on). This batch uses only "card"; the other parts are for a later batch.
3. manifest.json — contract "da_manifest_v1": files[] { file, contract, holds, bytes } and dance_file { pattern, count }.

A. THE LIST
At start, load index.json instead of dances.app.json and retired.json. Every list, count, map, tree, flag view, search and the swipe feed read the index entries. Counts on screen come from the index. Retired slugs come from index.retired: hidden everywhere, and /style/<retired slug> redirects to the slug it was merged into, or to /atlas when there is none — as today.
Stop fetching hero_results.json and remove the hero overrides: the index already carries the hero video chosen each night.

B. ONE DANCE
The dance page (/style/<slug>) shows at once what the index has (flag, name, country, era, family, tagline, hero video), fetches d/<slug>.json, and renders the rest from "card" exactly as it renders today. While it loads, a quiet placeholder; never a jump of the layout. In the swipe feed, fetch the next and the previous dance in advance.
If the dance file cannot be loaded: keep what the index gave, and show one calm line with a "Try again" button. Never an error screen.

C. THE LAST GOOD COPY
Keep the index and every dance file that was fetched in the browser's own database (IndexedDB or the Cache Storage API, whichever is simpler here), never in sessionStorage or localStorage. Browser only: guard for server rendering.
- Start: if a stored index exists, show it at once, then fetch the fresh one in the background and swap it in quietly when it is valid.
- A fresh index is valid when its contract is "da_index_v1" and its count is at least 90 % of the stored one. An invalid or unreachable index never replaces a good stored copy; then show a small muted line "Showing the library as of <date of the stored generated_at>".
- A stored dance file is used without any request when its fingerprint equals index.dances[slug].fp; otherwise fetch it again.
- No stored copy and no network: fall back to the bundled catalogue as today.
- If the browser's database is not available (private mode), work from memory; nothing breaks.
- On start, remove the old sessionStorage keys da_catalogue_session_v1 and hero_overrides_v1 once.

D. EVERY REQUEST
Every data request (the index, a dance file, site.json, the mentor file, the Viral list from Supabase) has a 10-second timeout, one retry, then a calm fallback in place. The Viral page shows one calm line with "Try again" when its list cannot be loaded.

E. NO BLANK SCREEN
One error boundary around the whole app and one around each route: a calm message, a "Back to the atlas" button and a "Try again" button. No white page, no raw error text.

F. /health (a plain page, not in the navigation; add a small "Health" link in the footer)
Load manifest.json. For index.json, site.json, active_ready.json, machine.json, bdf_teaching_system.json and the dance file of the first slug in the index: one row each with the file name, what it holds (from the manifest), reachable or not, contract as expected or not, its date (generated_at, evaluated_on or updated when present) and its size. Above the table: where this visit's library came from (network, stored copy or bundled copy), the number of dances, and whether the browser's database is available. Set document.title to "Health: OK" when every row is fine, otherwise "Health: N problems", and put the same on the page's root element as data-health="ok" or data-health="problems". Skip files larger than 1 MB.

KEEP
The look and behaviour of every page. Saved hearts. The mentor page. The words helper t(). The bundled catalogue as the last fallback.

WHEN DONE
Report, from the preview: (1) the requests made on first load of the home page and their sizes; (2) the requests made when a dance page opens; (3) that sessionStorage no longer holds da_catalogue_session_v1 or hero_overrides_v1; (4) that with the network switched off a reload still shows the atlas, with the muted "as of" line; (5) that a dance whose file fails shows the calm line and not an error; (6) what /health shows; (7) the number of dances on the Atlas page and that it equals index.count; (8) any console error.
```

## Batch 4 — the message

Send only after batch 2 is published and the words of `pages.dance` are in `site.json` on main.

```
BATCH 4 — THE WHOLE PROFILE ON THE DANCE PAGE. Read the Project instructions first. Build exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHAT IT IS
The dance page (/style/<slug>) already loads d/<slug>.json (batch 2) and shows the parts that come from "card". This batch shows the rest of that same file below the existing ABOUT section and above TUTORIALS: knowledge on display, read-only. It is not a class: no player, no speed or loop controls, no step-by-step mode. No new request, no new dependency. All words go through t(path, fallback) with the fallbacks written here. Change nothing else.

THE FILE (already in memory for the page)
state: "active_ready" | "building" | "story_ready_teaching_withheld" | "teaching_withheld" | "not_published" | "listed".
profile? { sections {origins_and_history, how_it_is_danced, music_and_instruments, costume_and_setting, occasions_and_meaning, notable_figures, regional_variants, lineage}; teaching? {basic_steps[], rhythm, formation, level_notes}; music_profile {tempo_bpm, meter, rhythm_pattern, instruments[], vocal_style, musical_form, mood_keywords[], sound_description, reference_recordings[] {title, artist}}; movement_profile? {posture, footwork, arms_and_hands, hips_and_torso, formation_and_space, partnering, tempo_feel, levels_and_jumps, difficulty, signature_moves[] {name, description}, what_to_avoid}; adaptations? {derived, seniors {seated_version, standing_version, tempo_and_range, counts, avoid[]}, children {game_version, duration_minutes, counts, avoid[]}}; connections[] {name, relation, note}; footage[] {title, url, year, license, attribution}; images[] {url, thumb, attribution, license, source_page}; albums[] {title, artist, year, musicbrainz_url}; claims[] {text, source}; citation {claims, supported}; tradition_status }.
readiness? { have, of, missing[] {key, label}, via {<item>: "lesson" | "performance"}, ritual_context? }.
lessons?[] { url, title, channel, level, language, counting_scheme, parts[] {t, seconds, segment, note}, steps[] {name, counts, description}, cues[], images[], common_mistakes[], safety[], teacher_style, distinctive_method, what_works[], what_hinders[], seen {from_s, to_s, checked_by_a_person} }.
performances?[] { url, observation {<key>: a text, a list of texts, or (music_heard) an object of texts and lists}, seen {…} }.
teaching_withheld? (a sentence). fingerprint, updated.
Every part may be absent. A value that is empty, "not described in sources", "Not described in sources.", "not in sources", "not derivable yet", "unknown" or "null" is not shown: no label, no heading, no empty card; a section whose values are all like that is not rendered. Fields not named in the sections below are not shown.

THE SECTIONS, in this order (each a titled section in the page's present style; a key such as "origins_and_history" is shown with underscores replaced by spaces and the first letter capitalised)
A. Under the name: one chip from state. "active_ready" → t("pages.dance.state.active_ready","Ready to activate"); "building" → t("pages.dance.state.building","In the making") followed by "<have> of <of>"; the two withheld states → t("pages.dance.state.story_only","Story only"); nothing for "not_published" and "listed". A second chip for profile.tradition_status when it is living, revived or historical.
B. t("pages.dance.story.title","The story"): the profile.sections, each under its own small heading.
C. t("pages.dance.music.title","Music"): the music_profile as labelled lines, instruments and mood_keywords as chips, sound_description as a paragraph, reference_recordings as "title — artist", then albums with a link to musicbrainz_url.
D. t("pages.dance.movement.title","Movement"): the movement_profile as labelled lines, difficulty as a chip, signature_moves as "name — description", what_to_avoid on its own line.
E. t("pages.dance.teaching.title","What has been gathered for teaching") with the lead t("pages.dance.teaching.lead","Gathered by a machine from the sources and from lessons it studied. Not yet checked by a person."):
   E1 from profile.teaching: basic_steps as a numbered list, then rhythm, formation and level_notes as labelled lines.
   E2 t("pages.dance.teaching.from_lessons","From lessons the machine studied"): one closed panel per lesson, titled "<title> — <channel>". Inside: level · language · counting_scheme; the parts as lines "<t> · <segment> — <note>", each a link to the lesson's url with "&t=<seconds>s" added, opening in a new tab; the steps as "name — counts — description"; cues and images as chips; common_mistakes, safety, what_works and what_hinders as short lists; teacher_style and distinctive_method as labelled lines; then the muted line t("pages.dance.teaching.seen","Seen by a machine in this video, not checked by a person.").
   E3 t("pages.dance.teaching.from_performance","From the performance the machine watched"): one closed panel per performance with its observation as labelled lines (a list as chips; an object such as music_heard as its own labelled lines, never as raw JSON), a link to its url, and the same muted line.
F. Only when readiness is present. The title is t("pages.dance.ready.title","Ready to activate?"), or for the two withheld states t("pages.dance.ready.story_title","How complete is the story?"). Then a simple bar "<have> of <of>". Then one of: state "active_ready" → t("pages.dance.ready.complete","Everything a teaching service needs for this dance has been gathered and source-checked. Not yet reviewed by a person."); state "story_ready_teaching_withheld" → t("pages.dance.ready.story_complete","The story of this dance is gathered and source-checked. Its teaching material is withheld."); any other state, when readiness.missing has entries → t("pages.dance.ready.missing","Still missing") and their labels as a list. When ritual_context is true and teaching_withheld is absent: t("pages.dance.ready.ritual","This dance has a ritual context. Carry its cultural note whenever it is taught.").
G. When teaching_withheld is present: sections D, E and H are not rendered at all; in their place one calm block titled t("pages.dance.withheld.title","Story only") with the teaching_withheld sentence.
H. t("pages.dance.adaptations.title","For seniors and for children"), closed by default, only when adaptations.derived is true: the two groups as labelled lines, then the muted line t("pages.dance.adaptations.note","Derived suggestions, not facts from the sources.").
I. t("pages.dance.connections.title","Connected dances"): "relation · name — note"; the name links to that dance when the index has a dance with that name or alias (compare in lower case).
J. t("pages.dance.footage.title","Reference footage"): links only (title, year, attribution, license), opening in a new tab. Do not embed.
K. Pictures from profile.images that the existing gallery does not already show are added to that gallery, with attribution and license.
K2. The existing TUTORIALS block shows "Tutorials coming soon" for every dance. Replace that: when card.tutorials has entries, list them as links (title — channel · level, to https://www.youtube.com/watch?v=<youtube_id>, opening in a new tab); when it has none, or when teaching_withheld is present, do not render the TUTORIALS block at all.
L. t("pages.dance.checks.title","Sources and checks"): "<citation.supported> of <citation.claims> " + t("pages.dance.checks.claims","claims checked against their sources"), then a closed panel t("pages.dance.checks.show","Show the claims") with each claim and a link to its source. The existing source links stay.
M. Last, one muted line: a link t("pages.dance.agent.link","The file an agent receives for this dance") to https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/d/<slug>.json, and t("pages.dance.agent.changed","Last changed") with the file's "updated" date.

RULES
Read-only. Panels are real buttons with aria-expanded, closed panels render lazily. Links to other sites open in a new tab with rel="noopener noreferrer". No number is typed into the code. When the dance file could not be loaded, none of these sections appears and the page shows what it shows today, with the calm line from batch 2.

WHEN DONE
In the preview open /style/hustle (ready to activate, with a studied lesson), /style/ahwash (story only) and /style/salsa (listed, with a lesson). Report for each which of the sections A to M are shown, and any console error.
```

## Batch 5 — the message

Send after batch 4 is published. Needs `pages.starting_line` in `site.json` on main (machine.json is live). It opens with two repairs found in the check of batch 4.

```
BATCH 5 — THE STARTING LINE (new route /starting-line, and one strip on Home). Read the Project instructions first. Build exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHAT IT IS
A read-only page that shows how many dances are ready to be activated, how the rest climb towards that, and how fast the library grows. It is a status page, not a feature. All words go through t(path, fallback) with the fallbacks written here. No backend, no Lovable Cloud, no AI calls, no analytics, no new npm dependency (the two small charts are plain inline SVG). Change no existing page except the two repairs and the one strip on Home described below.

TWO REPAIRS FIRST (found when batch 4 was checked)
R1. The browser database keeps trimmed copies of the files: a dance file stored before batch 4 holds only its card, so that dance shows no profile until its fingerprint changes, and the stored index has no "states". From now on every file is stored whole, exactly as it was fetched, and read whole. Use a new database name, da_library_v2, with the same rules as before (a stored dance file is reused only when its fingerprint equals index.dances[slug].fp; the index is refreshed in the background), and delete da_library_v1 once at app start. /health reports the new database.
R2. On the dance page, in a performance panel, observation.signature_moments is a list of objects {start_s, end_s, what}, not of texts. Show each as a line "<m:ss> — <what>" that links to the performance's url with "&t=<start_s>s" added (new tab), and show the label only when the list has entries.

DATA
1. The index already in memory (index.json): count, states {active_ready, building, …}, dances{slug: {name, flag_emoji, state, …}}.
2. One new request when /starting-line opens: https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/machine.json — contract "da_machine_v1", about 12 KB, rebuilt every night. 10-second timeout, one retry, kept in memory for the session, never in sessionStorage or localStorage. If it fails or "contract" differs: show the header, sections D and (from the index) the big number, and one calm line t("pages.starting_line.unavailable","The numbers could not be loaded just now. Please try again in a moment."). Never an error screen.
Fields used from machine.json: generated_at; counts {listed, researched, published, three_to_five_short, two_short, one_short, active_ready, story_ready_teaching_withheld}; pace {days, per_night {active_ready}}; line[] {date, published, active_ready, lessons_studied}; blockers[] {key, label, profiles}; closest[] {slug, name, needs[]}. Any of them may be missing: then its block is not rendered.

THE PAGE, top to bottom (mobile first; the existing fonts, colours and spacing; accent #CC785C)
A. Header. Eyebrow t("pages.starting_line.eyebrow","MISSION 1"). H1 t("pages.starting_line.title","The starting line"). Lead t("pages.starting_line.lead","Dance Atlas is preparing every dance so that, when the technology is ready, all of them can be switched on at once. A dance stands at the starting line when a machine has gathered everything a teaching service needs for it and checked it against its sources."). A muted line: t("pages.starting_line.counted","Counted") + " <date of generated_at>".
B. One very large number: counts.active_ready (from the index's states.active_ready when machine.json is missing), with the label t("pages.starting_line.ready.label","dances ready to activate"). Under it, when pace.per_night.active_ready is a number: "+<pace.per_night.active_ready> " + t("pages.starting_line.ready.pace","a night, measured over the last") + " <pace.days> " + t("pages.starting_line.ready.days","days").
C. t("pages.starting_line.ladder.title","From a name to the starting line"): seven steps in this order, each a row with its number from counts, a bar whose length is the number relative to counts.listed, and a short note where one is given:
   listed — t("pages.starting_line.ladder.listed","Listed") — t("pages.starting_line.ladder.listed_note","a real dance, named and placed")
   researched — t("pages.starting_line.ladder.researched","Researched") — t("pages.starting_line.ladder.researched_note","its sources read and its story written")
   published — t("pages.starting_line.ladder.published","Published") — t("pages.starting_line.ladder.published_note","passed every quality gate and an independent judge")
   three_to_five_short — t("pages.starting_line.ladder.three_to_five_short","Three to five items short")
   two_short — t("pages.starting_line.ladder.two_short","Two items short")
   one_short — t("pages.starting_line.ladder.one_short","One item short")
   active_ready — t("pages.starting_line.ladder.active_ready","Ready to activate") — t("pages.starting_line.ladder.active_ready_note","everything a teaching service needs, gathered and source-checked") (this row in the accent colour)
   Then, set apart and muted: counts.story_ready_teaching_withheld — t("pages.starting_line.ladder.story_only","Story only") — t("pages.starting_line.ladder.story_only_note","sacred or restricted: the story is told, the dance is not taught").
D. t("pages.starting_line.ready_list.title","Ready to activate"): every dance of the index whose state is "active_ready", sorted by name, shown with the dance card the Atlas already uses, linking to /style/<slug>.
E. t("pages.starting_line.closest.title","Closest to the line"): the first 12 of closest[], each a row: the name (link to /style/<slug>), then t("pages.starting_line.closest.needs","still needs") and its needs as chips. A button t("pages.starting_line.closest.all","Show all") reveals the rest.
F. t("pages.starting_line.blockers.title","What holds the others back") with the lead t("pages.starting_line.blockers.lead","How many published dances are waiting for each item."): blockers[] as horizontal bars, longest first: label, bar relative to the largest, "<profiles> " + t("pages.starting_line.blockers.dances","dances").
G. t("pages.starting_line.growth.title","Growth"): three small inline-SVG line charts side by side (stacked on a phone), each on its own scale, from line[]: active_ready — t("pages.starting_line.growth.active_ready","Ready to activate"); published — t("pages.starting_line.growth.published","Published"); lessons_studied — t("pages.starting_line.growth.lessons_studied","Lessons studied"). Each chart shows its first and its last value as text and the first and last date under the axis, and has an aria-label that says the same. With fewer than two points a chart is not rendered.
H. Always visible at the end: t("pages.starting_line.honesty","Ready means machine-complete and source-checked. No dance here has been reviewed by a person, cleared for rights or tested on a platform; activation still needs all three.").
Page title "The starting line — Dancing Atlas".

HOME
Directly under the Home hero, one slim strip that is a single link to /starting-line: "<states.active_ready from the index> " + t("pages.starting_line.home.ready","dances ready to activate") + " · " + t("pages.starting_line.home.link","The starting line") + " →". It uses the index only: no new request on Home. When states.active_ready is missing the strip is not rendered.

RULES
Read-only. No number is typed into the code: every number comes from the files. Nothing is rendered for an empty value. Buttons are real buttons, usable with the keyboard. Numbers of four digits and more are shown with a thousands separator.

WHEN DONE
Open /starting-line in the preview and report: the big number, the seven numbers of the ladder, the number of cards under "Ready to activate", the number of bars under "What holds the others back", whether the three charts render, and any console error. Then open Home and report the strip's text. For the repairs: the name of the browser database after a reload and the keys of one stored dance file, and the signature moments shown in the performance panel of /style/hustle.
```


## Batch 6 — the message

Send after batch 5 is published (it shares the loader of `machine.json` and the small chart). Needs `pages.machine`, `he.items` and `he.topics` in `site.json` on main, and `study` and `need_keys` in `machine.json` (the stage `door` after the change of 21 November).

```
BATCH 6 — THE MACHINE ROOM (new route /machine, in Hebrew, for the owner). Read the Project instructions first. Build exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHAT IT IS
One read-only page in Hebrew, right to left, in large type, where the owner sees at a glance whether last night's run worked, how fast the library grows, how far the mentor's study has come and whether anything needs him. Every Hebrew word comes from site.json through t(path, fallback); the fallbacks below are the same Hebrew. No backend, no Lovable Cloud, no AI calls, no analytics, no new npm dependency, no new font file. Change no existing page except the two links named at the end.

DATA
One request when /machine opens: https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/machine.json (contract "da_machine_v1", about 12 KB; the same file /starting-line reads: share its loader). 10-second timeout, one retry, memory only. If it fails or "contract" differs: the header and one calm line t("pages.machine.unavailable","לא הצלחתי לטעון את הנתונים כרגע. נסה שוב בעוד רגע.").
Fields: generated_at; owner {status, text, verified_at}; last_night {date, minutes, questions, unanswered, stages, errors[], trouble[]}; counts {active_ready, one_short, two_short, published, researched, listed, lessons_studied, performances_observed, story_ready_teaching_withheld}; pace {days, per_night {active_ready, published, listed}}; line[] {date, active_ready}; study {topics, topics_read, first {topics, read}, next[], papers_read, lessons_studied, teachers_studied, findings_checked, practices, practices_in_dna}; blockers[] {key, label, profiles}; closest[] {slug, name, needs[], need_keys[]}; nights[] {date, minutes, questions, unanswered, errors}. Any field may be missing: then its line or block is not rendered.
Hebrew names: a readiness item key is shown as t("he.items.<key>", <the English label from the file>); a research topic key as t("he.topics.<key>", <the key with underscores as spaces>).

LAYOUT
The page container has dir="rtl" and lang="he". Font family for this page only: system-ui, "Arial Hebrew", "Noto Sans Hebrew", sans-serif. Body text at least 20px, section titles at least 28px, the big numbers at least 44px, generous spacing, one column, cards with the site's present colours (accent #CC785C). English fragments from the file (dance names, error texts, trouble notes) are wrapped in dir="ltr" spans so they read correctly. Dates are shown as day.month.year; generated_at also with its local time.

THE PAGE, top to bottom
A. H1 t("pages.machine.title","חדר המכונות"). Lead t("pages.machine.lead","מה המכונה עשתה הלילה, כמה מהר הספרייה גדלה, ומה צריך ממך."). Muted: t("pages.machine.updated","עודכן") + " <generated_at>".
B. Card t("pages.machine.owner.title","מה צריך ממך"). When owner.status is "resolved": a calm green card with t("pages.machine.owner.none","לא צריך ממך כלום. המכונה רצה כל לילה, בלי עלות."). Otherwise an amber card: t("pages.machine.owner.needed","צריך אותך:") and owner.text as it is (dir="ltr"). Under it, muted: t("pages.machine.owner.checked","נבדק") + " <owner.verified_at>".
C. Card t("pages.machine.night.title","הלילה האחרון") with last_night.date. When last_night.errors is empty: a green tick and t("pages.machine.night.ok","הלילה עבד"); otherwise a red mark, t("pages.machine.night.errors","היו שגיאות בלילה") and the errors listed (dir="ltr"). Then four numbers with labels: minutes — t("pages.machine.night.minutes","דקות"); questions — t("pages.machine.night.questions","שאלות למודל"); unanswered — t("pages.machine.night.unanswered","בלי תשובה"); stages — t("pages.machine.night.stages","שלבים"). Then a closed panel t("pages.machine.night.notes","הערות מהלילה") with the trouble lines (dir="ltr", small).
D. t("pages.machine.library.title","הספרייה"): big numbers from counts, in this order, each with its label: active_ready — t("pages.machine.library.active_ready","מוכנים להפעלה") (accent colour, largest); one_short — t("pages.machine.library.one_short","חסר להם פריט אחד"); two_short — t("pages.machine.library.two_short","חסרים להם שני פריטים"); published — t("pages.machine.library.published","פורסמו"); researched — t("pages.machine.library.researched","נחקרו"); listed — t("pages.machine.library.listed","ברשימה"); lessons_studied — t("pages.machine.library.lessons_studied","שיעורים שנלמדו"); performances_observed — t("pages.machine.library.performances_observed","הופעות שנצפו"); story_ready_teaching_withheld — t("pages.machine.library.story_only","סיפור בלבד, לא מלמדים").
E. t("pages.machine.pace.title","הקצב") with the lead t("pages.machine.pace.lead","בממוצע בכל לילה"): three numbers with a plus sign: per_night.active_ready — t("pages.machine.pace.active_ready","מוכנים להפעלה"); per_night.published — t("pages.machine.pace.published","פורסמו"); per_night.listed — t("pages.machine.pace.listed","נוספו לרשימה"). Muted: "<pace.days> " + t("pages.machine.pace.days","ימים נמדדו"). Under it the small inline-SVG line chart of line[].active_ready (the chart of /starting-line; drawn left to right, inside a dir="ltr" box).
F. t("pages.machine.study.title","המחקר של המנטור") with the lead t("pages.machine.study.lead","איך ללמד כל אדם לרקוד: המכונה קוראת מחקרים, לומדת שיעורים ומקשיבה ללומדים."). Lines, each a large number phrase: "<study.topics_read> " + t("pages.machine.of","מתוך") + " <study.topics> " + t("pages.machine.study.topics","נושאי מחקר נקראו"); "<study.first.read> " + t("pages.machine.of","מתוך") + " <study.first.topics> " + t("pages.machine.study.first","מהנושאים שביקשת ב-21 בנובמבר נקראו"); "<study.papers_read> " + t("pages.machine.study.papers","מאמרים נקראו"); "<study.lessons_studied> " + t("pages.machine.study.lessons","שיעורים נצפו כדי ללמוד איך מלמדים"); "<study.teachers_studied> " + t("pages.machine.study.teachers","מורים שהמכונה למדה מהם"); "<study.findings_checked> " + t("pages.machine.study.findings","ממצאים נבדקו מול המקור"); "<study.practices_in_dna> " + t("pages.machine.of","מתוך") + " <study.practices> " + t("pages.machine.study.dna","דרכי הוראה נכנסו ל-DNA של המנטור"). Then t("pages.machine.study.next","בתור ללילה הבא") and study.next as chips with their Hebrew names. Then a link t("pages.machine.study.link","לדף המנטור") to /mentor.
G. t("pages.machine.blockers.title","מה מעכב את הדפים") with the lead t("pages.machine.blockers.lead","כמה דפים מחכים לכל פריט"): blockers[] as horizontal bars, longest first, each with its Hebrew name and its number.
H. t("pages.machine.closest.title","הקרובים ביותר לקו הזינוק"): the first 10 of closest[]: the name (dir="ltr", link to /style/<slug>), then t("pages.machine.closest.needs","חסר") and the Hebrew names of need_keys as chips (the needs texts when need_keys is missing). A button t("pages.machine.closest.all","הצג הכול") reveals the rest.
I. t("pages.machine.nights.title","הלילות האחרונים"): a simple table of nights[], newest first, at most 14 rows, with the column titles t("pages.machine.nights.date","תאריך"), t("pages.machine.nights.minutes","דקות"), t("pages.machine.nights.questions","שאלות"), t("pages.machine.nights.unanswered","בלי תשובה"), t("pages.machine.nights.errors","שגיאות"); a row whose errors is 0 shows a green tick in that column.
J. At the end, three links in one row: t("pages.machine.links.starting_line","קו הזינוק") to /starting-line, t("pages.machine.links.mentor","המנטור") to /mentor, t("pages.machine.links.health","בריאות הקבצים") to /health; and one muted line t("pages.machine.note","הדף נבנה מקובץ אחד שהמכונה כותבת כל לילה. שום דבר כאן לא עולה כסף.").
Page title "חדר המכונות — Dancing Atlas".

THE TWO LINKS ELSEWHERE
At the end of /starting-line and at the end of /health add one small muted link t("pages.machine.title","חדר המכונות") to /machine. No item in the top bar or the bottom bar.

RULES
Read-only. No number is typed into the code. Nothing is rendered for an empty value. Panels and buttons are real buttons, usable with the keyboard, with aria-expanded.

WHEN DONE
Open /machine in the preview and report: the text of card B, the text and the four numbers of card C, the first number of D, the three numbers of E, the first two lines of F and the chips under "בתור ללילה הבא", the number of bars in G, the number of rows in I, and any console error. Confirm that the page reads right to left and that dance names read left to right.
```


## Batch 7 — the message

Send after batch 5 is published (it adds a link to the Home strip made there). Needs `pages.vision` in `site.json` on main.

```
BATCH 7 — THE DIRECTION (new route /vision, and one link on Home). Read the Project instructions first. Build exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHAT IT IS
One calm, read-only page that says in the founder's words what Dance Atlas is preparing, so that nobody mistakes this site for the product. Text only, in the site's present style. Every word comes from site.json through t(path, fallback) with the fallbacks written here, so the founder can change any sentence without a build. No new request except the words already loaded, no backend, no Lovable Cloud, no AI calls, no analytics, no new npm dependency. Change no existing page except the one link on Home.

DATA
Only what is already in memory: the words (site.json) and the index head (index.json: count, states.active_ready).

THE PAGE, top to bottom (mobile first; one readable column, at most 70 characters wide; body text at least 18px; accent #CC785C)
A. Header. Eyebrow t("pages.vision.eyebrow","WHERE THIS IS GOING"). H1 t("pages.vision.title","What Dance Atlas is preparing"). Lead t("pages.vision.lead","Dance Atlas is the library being prepared for BDF, the Best Dance Friend: a mentor you talk with and move with, who draws on everything known about a dance and on everything known about how to teach it. BDF is not built yet. What you see on this site is the knowledge it will stand on.").
B. t("pages.vision.words.title","In the founder's words"): two large pull quotes, each in a block with an accent bar: t("pages.vision.words.one","We need to be cutting edge with our knowledge of the dance and the education of it, and be ready for the breakthrough in the technology, and then just overnight activate all the profiles.") and t("pages.vision.words.two","Once we teach people to teach in the best way, they become better people, because they can teach. Not only dance: through learning movement we can instil the foundations of mentoring, and they take that with them into life."); under the second, muted: t("pages.vision.words.two_note","translated from Hebrew").
C. Three cards in a row (stacked on a phone), each with a title and a body:
   t("pages.vision.now.title","Now") — t("pages.vision.now.body","Gather the knowledge. Every night, at no cost, a machine researches the world's dances, studies lessons and performances, and reads how the best teachers teach."). Under the body two lines: t("pages.vision.now.mission1","Mission 1: thousands of dances at the starting line, ready to be switched on.") followed by "<states.active_ready> / <count>" and a link t("pages.vision.now.mission1_link","The starting line") to /starting-line; then t("pages.vision.now.mission2","Mission 2: the mentor's DNA, an endless study of how to teach anyone to dance.") and a link t("pages.vision.now.mission2_link","The mentor") to /mentor.
   t("pages.vision.next.title","Next") — t("pages.vision.next.body","A beta for people who live dance culture and music: to look, to check and to correct, together with the founder.").
   t("pages.vision.later.title","Later") — t("pages.vision.later.body","BDF itself: a full conversation, in virtual and augmented reality. Seeing the other friends who are learning the same dance, lessons taken together, practising together, a community built on dance.").
D. t("pages.vision.mentor.title","Why a mentor") — t("pages.vision.mentor.body","The mentor has to come out of the most serious research into how to teach: how to create ease and openness, and an experience that inspires, because it joins learning with movement, with knowledge and with other people. The research does not end, and what it finds becomes knowledge the mentor uses.").
E. t("pages.vision.not_here.title","What you will not find here") — t("pages.vision.not_here.body","No course, no price, no sign-in. Nothing is for sale and nothing asks for your details. There are no click-through lessons either: that is not how people will enjoy learning to dance.").
F. t("pages.vision.sacred.title","Sacred and restricted dances") — t("pages.vision.sacred.body","Their story is told with care. They are not taught.").
G. t("pages.vision.agents.title","Open to any AI") — t("pages.vision.agents.body","The whole library is a set of open files that any agent can read through one documented door: where to start, the rules, an index, and one complete file for every dance."). Two links: t("pages.vision.agents.link","The door: manifest.json") to https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/manifest.json (new tab, rel="noopener noreferrer") and t("pages.vision.agents.health","The health of every file") to /health.
H. Always visible at the end, muted: t("pages.vision.honesty","Everything here was gathered and written by a machine from public sources and checked against them. It has not been reviewed by a person.").
Page title "Where this is going — Dancing Atlas".

HOME
In the slim strip under the Home hero (made in batch 5) add, after the starting-line link, a second link: " · " + t("pages.vision.home.link","Where this is going") + " →" to /vision. If that strip does not exist, add the link alone in its place.

RULES
Read-only. Nothing is rendered for an empty value: a card or section whose words are empty in site.json is not shown. No number is typed into the code.

WHEN DONE
Open /vision in the preview and report: the H1, the number of pull quotes, the three card titles, the numbers shown after Mission 1, and any console error. Then open Home and report the strip's text.
```

## Batch 8 — the message

Send when `viral.json` is live in `public/catalog/` and `pages.viral` is in `site.json` on main. After it is published, change the sentence about the Viral list in `pages.privacy.body` of `site.json` (the list is then read from GitHub, not from Supabase).

```
BATCH 8 — TRUTH REPAIRS: THE VIRAL LIST (the page /viral). Read the Project instructions first. Do exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHY
The Viral page reads a database view whose three "charts" (this month, this year, all time) are the same list in order of date, with rank numbers that look like popularity. No popularity is known. The same list, with more verified facts and its sources, is now an open file on GitHub. After this batch the page tells the truth and the app has no backend at all.

DATA
https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/viral.json — contract "da_viral_v1", about 300 KB, rebuilt when it changes. Fields: count; order (a sentence); categories {<key>: number}; fingerprint; updated; challenges[] in the order to show them, each { slug, name, category?, song?, origin_date?, origin_year?, originator?, originator_story?, timeline?, peak_period?, fun_facts? (one text), celebrity_performances?[] {performer, platform?}, platform?, hero_video_youtube_id?, hero_title?, hero_channel?, video_stack?[] {youtube_id, role ("hero" or "rendition"), title?, channel?}, original_video_url?, sources?[] (addresses) }. Every field after name may be missing: then nothing is rendered for it, and no label either.
Load it the way the other files of the library are loaded: fetched when /viral opens (and on Home only when there are saved viral challenges to show), 10-second timeout, one retry, stored whole in the browser database da_library_v2 under "viral.json". A stored copy is shown at once; the file is fetched again in the background and, when its fingerprint differs, the stored copy is replaced for the next opening of the page. If it cannot be loaded and no copy is stored: the page header and one calm line t("pages.viral.unavailable","The Viral list could not be loaded just now. Please try again in a moment."). Add viral.json to the files /health checks.

REMOVE
1. Supabase, completely: every import and call, the client module, the npm package @supabase/supabase-js, the project address and the key. If Lovable itself manages a file of that integration that cannot be deleted, leave the file, make sure nothing imports it, and name it in your report. If anything other than the Viral list still reads from Supabase, do not remove that call: name it in your report. After this batch the app's only data requests go to raw.githubusercontent.com.
2. The three tabs THIS MONTH / THIS YEAR / ALL TIME.
3. Every rank: the "#1" numbers on the cards and in the details, the "NEW" badge, rank arrows, weeks on a chart, view counts, and the "How ranking works" button with what it opens. Nothing on this page may suggest popularity.
4. In the details: the "TUTORIALS" block with "Tutorials coming soon…".
5. The head of the page: the title becomes "Viral dance challenges · Dancing Atlas"; the description becomes "The viral dance challenges: who made each, when it began, the song and the sources. In order of date, not a ranking."; the og and twitter titles become "Viral dance challenges" and their descriptions the same sentence. The words "top", "chart", "ranked" and "biggest" leave the page and its head.

SHOW
A. Where the three tabs are today, one small muted line: t("pages.viral.order","In order of when each began, newest first. This is not a ranking."). The page heading is t("pages.viral.title","Viral dance challenges").
B. Category chips as today: t("pages.viral.all","All") with count, then one chip per key of categories with its number, in the order the page uses today for the keys it knows. A key the page does not know is shown with its underscores as spaces, styled as the others. A category that is not in the file is not shown (today "Flashmob IRL 0" is shown).
C. The cards in the file's order, with the same look and video behaviour as today: the small line "category · origin_year" without rank and without "NEW"; the name; under it originator, as today; Save, Share and Details as today. The video is hero_video_youtube_id; a challenge without one shows its card without a video.
D. The details sheet, in this order, each part only when its value is present:
1. "category · origin_year" (no rank), the name and the originator line, as today.
2. originator_story (the paragraph shown today).
3. The Watch button t("pages.viral.watch","Watch") as today.
4. t("pages.viral.timeline","How it spread"): timeline.
5. t("pages.viral.peak","At its height"): peak_period.
6. t("pages.viral.fact","Worth knowing"): fun_facts.
7. t("pages.viral.also","Also danced by"): celebrity_performances, one line each: performer · platform.
8. t("pages.viral.song","The song") with the song, as today.
9. t("pages.viral.more","More videos"): the entries of video_stack whose role is not "hero", each a row "title · channel" that opens https://www.youtube.com/watch?v=<youtube_id> in a new tab (rel="noopener noreferrer"). No embedded players in the sheet.
10. t("pages.viral.sources","Sources"): sources as a numbered list of links, each showing the host name of its address (new tab, rel="noopener noreferrer").
E. Saved viral challenges keep working with the same slugs and the same browser storage: the heart on a card, and wherever saved viral challenges are listed today (the "Fav viral" block on Home, the Saved page), their names and pictures now come from viral.json. A saved slug that is not in the file is not shown and not deleted.

RULES
Read-only. No number is typed into the code. Nothing is rendered for an empty value. Change nothing else on other pages.

WHEN DONE
Open /viral in the preview and report: the number on "All"; every category chip with its number; the first three names; the title and the description of the page; every label and value shown in the details of the first card; the hosts the page requested data from; whether @supabase/supabase-js is gone from package.json; the rows of /health. Then save one viral challenge, open Home and the Saved page, and report that it shows there.
```


## Batch 8 — the three repairs, as sent

Sent on 21 November between 18:25 and 18:32, each put into the chat field as written here. What they repaired and what they cost is in the record.

```
REPAIR 8a — the details sheet on /viral is off the screen. Read the Project instructions first. Do exactly this and nothing else.

WHAT IS WRONG (measured in the preview at 1400 x 724)
Since Batch 8 the details sheet is the shared Dialog with the class "viral-details". The Dialog's base classes translate-x-[-50%] translate-y-[-50%] set the CSS property translate to "-50% -50%" (Tailwind v4 uses the translate property, not transform). The viral-details rule sets left 0, right 0, bottom 0 and a top of 12vh, but does not reset translate. Result: the sheet's box is at left -700px, top -232px, so three quarters of it lie outside the window and its text cannot be read. Before Batch 8 the sheet was a plain element with role="dialog" at left 0, top 153px, full width, translate none.

REPAIR
1. When open, the sheet is a bottom sheet inside the window: left edge 0, full width, bottom edge at the bottom of the window, top edge below the category chips, scrolling inside itself. Its computed translate is "none" (or 0), also during and after the opening animation. No part of it is outside the window at any width from 320px up.
2. The sheet has a visible Close button at its top right, as before Batch 8.
3. Keep everything else of Batch 8 as it is: the content and order of the sheet, focus moving into it, Escape closing it, the page behind not scrolling.
4. Correct only this sheet. Do not change how the shared Dialog looks on other pages.

WHEN DONE
In the preview open /viral, open the details of the first card, and report for a 1400 x 724 window and for a 390 x 844 window: the sheet's left, top, width and height from getBoundingClientRect(), and its computed translate. Scroll the sheet to its end and confirm that the Sources list is visible.
```

```
REPAIR 8b — the Viral details sheet is still off the screen in Chrome. Read the Project instructions first. Do exactly this and nothing else.

MEASURED after Repair 8a, in Chrome, in the preview, window 1400 x 724, details of the first card open: getBoundingClientRect() gives left -700, top -171, width 1400, height 597, and getComputedStyle(sheet).translate is "-50% -50%". The rule .viral-details sets "transform: translate(0px) !important" and the rule .viral-details[data-state] sets "transform: none !important". Neither sets the property "translate". The Dialog's Tailwind v4 classes translate-x-[-50%] translate-y-[-50%] set exactly that property (translate: -50% -50%), not transform, so the sheet is still moved half its width to the left and half its height up. A browser that does not know the separate translate property hides the fault, which is probably why your check passed.

REPAIR
In the CSS rule .viral-details add this declaration: translate: none !important;
Nothing else changes.

WHEN DONE
Report the full text of the .viral-details rule, and the computed translate and the left edge of the open sheet, measured in a current Chrome or Chromium (version 110 or later). Say which browser and version you measured in.
```

```
REPAIR 8c — the cause found: the production build rewrites the hand-written translate declaration. Read the Project instructions first. Do exactly this and nothing else.

WHAT HAPPENS
Your check runs on the dev server, where the sheet is right. The address https://preview--dancingatlas.lovable.app/viral serves the production bundle (styles-*.css, index-*.css). There the CSS minifier lowers the hand-written "translate: none !important" into "transform: translate(0px) !important": in the built stylesheet the rule .viral-details has no translate property at all. Tailwind's own classes translate-x-[-50%] translate-y-[-50%] survive the build because they use variables (translate: var(--tw-translate-x) var(--tw-translate-y)), so in the built page the open sheet still computes translate "-50% -50%" and sits at left -700px, top -171px in a 1400 x 724 window. The published site is built the same way.

REPAIR (both steps)
1. In the component that renders the Viral details sheet, add the utilities translate-x-0 translate-y-0 to the className given to the Dialog content, so that tailwind-merge drops translate-x-[-50%] translate-y-[-50%] for this sheet only.
2. In the CSS rule .viral-details replace the declaration "translate: none !important;" by these two declarations, which no minifier can lower: --tw-translate-x: 0 !important; --tw-translate-y: 0 !important;
Nothing else changes. The shared Dialog stays as it is for other pages.

WHEN DONE
Run the production build and check the BUILT result, not the dev server: (a) quote the .viral-details rule as it stands in the built stylesheet; (b) on the built page, with the details of the first card open in a 1400 x 724 window, report getComputedStyle(sheet).translate and the left and top of getBoundingClientRect(). The left must be 0 and the top must be positive.
```

## Batch 9 — the message

Send when the index on main carries `places` and `families` (the stage `door` after the change of 21 November, evening) and the words `pages.atlas`, `pages.tree`, `pages.home`, `pages.notfound` are in `site.json`.

```
BATCH 9 — TRUTH REPAIRS: COUNTRIES AND FAMILIES (the pages /atlas, /flags and /tree, one sentence on Home, unknown addresses). Read the Project instructions first. Do exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHY
The Atlas counts 213 "countries" because a joined name such as "France and Italy" or "Albania/Kosovo" counts as a country of its own; the Flags page shows the same flag several times for the same reason; the tree puts every dance without a family into "Folk & Circle" (977, of which 774 have no family); Home promises a map that does not exist; an address that does not exist shows a loading-error message. The index now carries the real counts.

DATA (already loaded: index.json, contract "da_index_v1")
Head: count; regions[] (names, in the order to show them); places {<ISO code>: {region, dances}}; no_place (number); families {<key>: {name, dances}}; no_family (number).
Per dance: countries?[] (ISO codes: a dance belongs to EVERY code in this list), family? (a key of families), name, era, region, slug and the fields used today.
A country's name is new Intl.DisplayNames(["en"], {type: "region"}).of(code); its flag is the emoji made from the two letters of the code. Do not use a dance's own "country" or "region" text for grouping or counting any more (they are free text: 213 different country strings, hundreds of region strings); they may still be shown as text on a dance page. A country's region is places[code].region.

ATLAS (/atlas)
1. Header: "<count> DANCES · <number of keys in places> COUNTRIES".
2. One section per name in regions, in that order; under it the countries whose places[code].region is that name, sorted by name, each a chip as today: flag, name, places[code].dances.
3. After the regions, when no_place is above zero, one chip without a flag: t("pages.atlas.no_place","Place not yet known") with the number no_place; it lists the dances that have no countries.
4. The sheet a chip opens stays as it is, with the heading "<name>" and the line "<n> DANCES · <places[code].region>", listing every dance whose countries include that code, sorted by name.

FLAGS (/flags)
One tile per key of places: no flag appears twice. Sorted by country name. A tile opens what it opens today, for the dances whose countries include that code.

TREE (/tree)
1. The families are the keys of families, each with its name and its number from the file; a dance sits in the family named by its own family field.
2. Dances without a family field are shown as one separate group t("pages.tree.no_family","Family not yet known") with the number no_family. They are never placed inside "Folk & circle" or any other family.
3. Everything else on the page (zoom, layout, flags) stays as it is.

HOME
The sentence under the hero ("<count> traditions still danced today — wander by flag, map, or family tree.") becomes "<count> " + t("pages.home.lead","traditions still danced today.") followed by three text links: t("pages.home.by_country","By country") to /atlas, t("pages.home.by_flag","By flag") to /flags, t("pages.home.by_family","By family") to /tree. There is no map: the word goes. The "Start exploring" button and the strip under it stay.

AN ADDRESS THAT DOES NOT EXIST
An address that matches no route (for example /map) shows t("pages.notfound.title","This page does not exist") and a link t("pages.notfound.back","Back to the atlas") to /atlas. The "could not be loaded" message stays for real loading failures only. A retired dance address keeps redirecting as today. The address /saved redirects to /profile (the Saved page).

RULES
Read-only. No number is typed into the code: every number comes from the index. No new request, no new npm dependency. Change no other page. Keep the present components (the sheet a chip opens, the chips, the tiles, the tree): change what they show, not what they are built on. Check the result on the built preview (https://preview--dancingatlas.lovable.app), not only on the dev server.

WHEN DONE
Report from the preview: the Atlas header; the regions shown, in order, with the number of countries under each; the number on the "Place not yet known" chip; the number of dances in the sheet of France and of Japan; the number of tiles on /flags; every family on /tree with its number, and the number of the group without a family; the Home sentence with its three links; the text shown at /map; where /saved leads.
```

## Batch C — the message

Send when `research.json` is live in `public/catalog/` (the stage `door` after the change of 23 November) and `pages.research` and `he.strands` are in `site.json` on main. The page is in Hebrew, like `/machine`: it is the owner's own view of the reading list. What it should show is counted from `research.json` at the time (on 23 November: 30 of 80 topics read, 6 of the owner's 14, 12 papers, 131 findings).

```
BATCH C — THE RESEARCH LIBRARY (new route /research, in Hebrew, for the owner). Read the Project instructions first. Build exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHAT IT IS
One read-only page in Hebrew, right to left, in large type: the reading list of the mentor's study. The owner sees which research topics have been read, what each reading found, and what waits, with his own three strands first. It follows the page /machine in layout and type. Every Hebrew word comes from site.json through t(path, fallback); the fallbacks below are the same Hebrew. No backend, no Lovable Cloud, no AI calls, no analytics, no new npm dependency, no new font file. Change no existing page except the two links named at the end.

DATA
One request when /research opens: https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/research.json — contract "da_research_v1", about 130 KB today and growing with every reading, rewritten only when it changes. Load it the way the other files of the library are loaded: 10-second timeout, one retry, kept whole in the browser database da_library_v2 under "research.json"; a stored copy is shown at once and replaced in the background when its fingerprint differs. If it cannot be loaded and no copy is stored: the header and one calm line t("pages.research.unavailable","לא הצלחתי לטעון את רשימת הקריאה כרגע. נסה שוב בעוד רגע."). Add research.json to the files /health checks.
Fields: updated (a date); counts {topics, read, owner_topics, owner_read, papers, findings_checked}; a_night {topics, papers}; groups[] {key, name, owner (true or false), topics[]}; a topic {key, name, state ("read", "next", "waiting", "thin", "no_sources" or "unanswered"), on? (a date), and only when state is "read": principle?, for_the_teacher?[], when_it_does_not_apply?, findings?[] {finding, quote, source (an address)}, sources?[] {url, title, authors?, year?, journal?}}; papers[] {key, title, on?, authors?, year?, journal?, url?, cited_by?, principle?, for_the_teacher?[], when_it_does_not_apply?, findings?[], sources?[]}. A field marked ? may be missing: then nothing is rendered for it, and no label either.
Hebrew names: a topic is shown as t("he.topics.<key>", <name>), with its English name (the name field, first letter capitalised) beside it in small muted type; a group as t("he.strands.<key>", <name>).

LAYOUT
As on /machine: the page container has dir="rtl" and lang="he"; font family for this page only: system-ui, "Arial Hebrew", "Noto Sans Hebrew", sans-serif; body text at least 20px, section titles at least 28px, the big numbers at least 44px; one column; cards in the site's present colours (accent #CC785C). Everything the file gives in English (names, principles, findings, quotes, titles of sources and papers) sits in dir="ltr" blocks or spans, aligned left, so it reads correctly. Dates are shown as day.month.year.

THE PAGE, top to bottom
A. Eyebrow t("pages.research.eyebrow","המחקר של המנטור"). H1 t("pages.research.title","ספריית המחקר"). Lead t("pages.research.lead","כל לילה המכונה קוראת מחקרים על איך אנשים לומדים ואיך מלמדים אותם. כאן רואים מה כבר נקרא, מה נמצא, ומה מחכה בתור."). Muted: t("pages.research.updated","עודכן") + " <updated>".
B. Four big numbers, each with its label: "<counts.read> " + t("pages.research.of","מתוך") + " <counts.topics>" — t("pages.research.counts.read","נושאים נקראו"); "<counts.owner_read> " + t("pages.research.of","מתוך") + " <counts.owner_topics>" — t("pages.research.counts.owner","מהנושאים שביקשת נקראו") (accent colour); counts.papers — t("pages.research.counts.papers","מאמרים מהחיפוש הפתוח"); counts.findings_checked — t("pages.research.counts.findings","ממצאים עם ציטוט שנבדק מול המקור"). Under them one muted line: t("pages.research.counts.tonight","בכל לילה נקראים") + " <a_night.topics> " + t("pages.research.counts.tonight_topics","נושאים") + " · <a_night.papers> " + t("pages.research.counts.tonight_papers","מאמרים").
C. Section (id "yours") t("pages.research.yours.title","הנושאים שביקשת") with the lead t("pages.research.yours.lead","שלושת הכיוונים שנתת ב-21 בנובמבר. הם נקראים לפני כל השאר."). The groups whose owner is true, in the file's order, all open: the group's Hebrew name as a sub-title (its id is the group key), beside it "<number of its topics whose state is read> " + t("pages.research.of","מתוך") + " <number of its topics>"; then its topics in the file's order.
D. Section (id "rest") t("pages.research.rest.title","שאר רשימת הקריאה") with the lead t("pages.research.rest.lead","לפי הנושאים של אוצר המילים של המנטור."). The groups whose owner is false, in the file's order, each a panel with the same sub-title line, closed by default (a real button with aria-expanded).
E. A topic row, the same in C and D: the Hebrew name in large type, the English name small and ltr, and one state chip: "read" — t("pages.research.state.read","נקרא") + " <on>" (calm green); "next" — t("pages.research.state.next","ייקרא הלילה") (accent); "waiting" — t("pages.research.state.waiting","מחכה בתור") (muted); "thin" — t("pages.research.state.thin","נקרא, ולא נמצאו שני ציטוטים שאפשר לבדוק"); "no_sources" — t("pages.research.state.no_sources","לא נמצא מקור. ייחפש שוב"); "unanswered" — t("pages.research.state.unanswered","המודל לא ענה. יישאל שוב") (the last three in muted amber). A topic whose state is "read" is a button (aria-expanded) that opens what was found, in this order, each part only when present: one small muted Hebrew line t("pages.research.found.english","הטקסט באנגלית, כפי שהמכונה כתבה אותו מתוך המקור."); t("pages.research.found.principle","העיקרון") and principle; t("pages.research.found.teacher","מה זה אומר למורה") and the for_the_teacher lines as bullets; t("pages.research.found.findings","הממצאים, עם הציטוט שנבדק"): each finding, under it its quote in a muted block, and a link showing the host name of its source address (new tab, rel="noopener noreferrer"); t("pages.research.found.limits","מתי זה לא חל") and when_it_does_not_apply; t("pages.research.found.sources","המקורות"): sources as links (title; then authors, year, journal in muted type). A topic in any other state opens nothing.
F. Section (id "papers") t("pages.research.papers.title","מאמרים מהחיפוש הפתוח") with the lead t("pages.research.papers.lead","כל לילה חיפוש אחד במאגר המאמרים. המצוטטים ביותר נקראים ראשונים."). The papers in the file's order, the first 10 visible and a button t("pages.research.papers.all","הצג הכול") for the rest. Each paper: its title (ltr; a link to url in a new tab), a muted ltr line "journal · year · <cited_by> " + t("pages.research.papers.cited","ציטוטים"), and it opens the same blocks as a read topic.
G. One line, always visible: t("pages.research.honesty","נקרא על ידי מכונה, ועדיין לא נבדק על ידי אדם. ממצא מוצג רק כשהמילים שצוטטו נמצאו במקור. רוב המחקרים עוסקים בלמידת תנועה באופן כללי, לא בריקוד."). Then two links in one row: t("pages.research.links.mentor","המנטור: מה נכנס ל-DNA") to /mentor, t("pages.research.links.machine","חדר המכונות") to /machine.
Page title "ספריית המחקר — Dancing Atlas".

THE TWO LINKS ELSEWHERE
1. On /machine, at the end of the block "המחקר של המנטור": a link t("pages.research.link","ספריית המחקר") to /research.
2. On /mentor, at the top of the section "The research": one link t("pages.mentor.research.library","The whole reading list, strand by strand (in Hebrew)") to /research.
No item in the top bar or the bottom bar.

RULES
Read-only. No number is typed into the code: every number comes from the file or is counted from it. Nothing is rendered for an empty value. Panels and buttons are real buttons, usable with the keyboard. Render closed panels lazily. Keep the present components of /machine and /mentor: add the links, change nothing else in them. Check the result on the built preview (https://preview--dancingatlas.lovable.app), not only on the dev server.

WHEN DONE
Open /research on the built preview and report: the four numbers of B and the line under them; the three groups of C with their "<read> מתוך <number>"; the number of panels in D; the text of the state chip of the first topic of C; the labels shown when the first read topic is opened; the number of papers visible before "הצג הכול"; the rows of /health; and confirm that the page reads right to left and that English text reads left to right.
```

## Batch B — the message

Send after batch C (it names the link to `/research` that C puts on `/mentor`). Everything Hebrew is already in `site.json`: the page's 55 fixed words (`pages.mentor_he`), and the vocabulary (`he.strands`, `he.practices` with a name, a sentence and a meaning for each of the 37 practices, `he.moments`, `he.creed`, `he.voice`, `he.feelings`, `he.entry`, `he.adapt`, `he.kinds`, `he.learner`). The Hebrew of the vocabulary is a translation of the fixed list in `pipeline/teaching.py`, kept beside the site's other words and guarded by a test; what the machine wrote from the videos and the sources stays in English on the page, and the page says so. The language lives in the address (`/mentor?lang=he`) and is stored nowhere.

```
BATCH B — THE MENTOR IN HEBREW (the page /mentor, a second reading). Read the Project instructions first. Do exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHAT IT IS
The owner reads Hebrew. /mentor gets a second reading: the same page, the same components and the same data, with its fixed words and its vocabulary in Hebrew, right to left. The site translates nothing and calls no AI: every Hebrew word is already in site.json and is read through t(path, fallback). What the machine wrote from the videos and the sources (examples, beliefs, findings, quotes, names) stays in English. Keep every component of /mentor as it is built: this batch changes which words the components show, not what they are made of. No backend, no Lovable Cloud, no analytics, no new npm dependency, no new font file. No other page changes, except the links named near the end.

THE SWITCH
The language lives in the address and is stored nowhere: /mentor is the English reading, exactly as today; /mentor?lang=he is the Hebrew reading. Any other value of lang is read as English. Under the lead, two small real links side by side: t("pages.mentor.lang.he","עברית") to /mentor?lang=he and t("pages.mentor.lang.en","English") to /mentor; the current one has aria-current="true" and the accent colour. The chips of the in-page index and every other link inside the page keep the current reading.

THE HEBREW READING (only when lang=he)
The page container gets dir="rtl" and lang="he"; font family for this reading: system-ui, "Arial Hebrew", "Noto Sans Hebrew", sans-serif; body text at least 18px. Dates are shown as day.month.year. Every text that stays in English (see ENGLISH STAYS) sits in a dir="ltr" block or span, aligned left, so it reads correctly. The top bar and the bottom bar do not change.

1. THE FIXED WORDS. Each fixed word of the page is read from pages.mentor_he in site.json. The fallback of each t() is the English shown today, so nothing can come out empty. The paths below are all under pages.mentor_he.
Header: eyebrow, title (the H1), lead. The muted line under them becomes: t(rebuilt) + " <date> · " + t(new) + " <lessons> " + t(lessons) + ", <research notes> " + t(research_notes). Under it one more muted line: t(english_note).
Where the study stands: stands.title; the six labels, in today's order: stands.teachers_ranked, stands.teachers_studied, stands.lessons, stands.comments, stands.findings, stands.practices; the sixth number reads "<two or more> " + t(of) + " <total>".
The teaching DNA: dna.title, dna.lead; the aria-labels of the dots: dna.three and dna.two; the small line of a rule: "<teachers> " + t(teachers) + " · <learner comments> " + t(learner_comments) + " · <research notes> " + t(research_notes); the title of the proof: dna.proof; "seen in <n>% of the lessons studied" becomes "<n>% " + t(dna.seen_in); "watch the moment" becomes t(dna.watch).
When a learner struggles: adjust.title, adjust.lead; the three labels: adjust.learners_say, adjust.teacher_answer, adjust.research_adds.
The mentor: mentor.title, mentor.lead; the six sub-titles: mentor.sound, mentor.moments, mentor.believe, mentor.feeling, mentor.stays, mentor.meant; "seen <n> times with <m> teachers" becomes t(mentor.seen) + " <n> " + t(mentor.times_with) + " <m> " + t(teachers); "<m> teachers" becomes "<m> " + t(teachers); "met <n> times" becomes t(mentor.met) + " <n> " + t(mentor.times).
What BDF keeps in mind about a person: learner.title, learner.lead.
The teachers it learns from: the_teachers.title, the_teachers.lead; "<n> praising comments" becomes "<n> " + t(the_teachers.praise); "Show all <n>" becomes t(the_teachers.show_all) + " (<n>)".
The research: research.title, research.lead; "For the teacher" becomes t(research.for_teacher); "When it does not apply" becomes t(research.not_apply); the link to /research becomes t(research.library).
The closing line: honesty. The line shown when the file cannot be loaded: unavailable. The chips of the in-page index: the seven section titles above.

2. THE VOCABULARY. A key of the file gets its Hebrew from site.json; where a key has none, the page shows what it shows today.
A theme of the DNA: t("he.strands.<the theme in lower case, spaces replaced by hyphens>", <theme>); "See it" is he.strands.see-it.
The sentence of a rule: t("he.practices.<tag>.do", <do>). The meaning inside its proof: t("he.practices.<tag>.meaning", <meaning>).
The title of a card under "When a learner struggles": t("he.practices.<tag>.name", <the title shown today>).
A word of "How they sound": t("he.voice.<word>", <word>).
A moment: t("he.moments.<moment>", <title>). A heading of belief: t("he.creed.<about>", <title>). A feeling: t("he.feelings.<feeling>", <the name shown today>).
The title of a card under "What BDF keeps in mind about a person": the value in site.json he.learner whose key equals the "remember" text of the file (look it up in that object itself: its keys are whole sentences).
A chip on such a card: the first that exists of he.practices.<key>.name, he.feelings.<key>, he.entry.<key>, he.adapt.<key>.
The kind of a learner theme inside a proof: t("he.kinds.<kind>", <the label shown today>).

ENGLISH STAYS
Everything else that comes from the file: the examples and what a teacher says or does, the adjustments, what learners say, the beliefs, the responses to a feeling, what stays with the learner, what it meant to learners, the principles, findings, quotes and sources of the research, the names of teachers and dances, a teacher's system and signature. Shown exactly as today, left to right.

LINKS ELSEWHERE
Every link to /mentor on the Hebrew pages /machine, /research and /vision now leads to /mentor?lang=he. Nothing else changes on those pages.

RULES
Read-only. No Hebrew word is typed into the code except the two fallbacks given above. The English reading (/mentor without lang) must come out exactly as it is today. Check the result on the built preview (https://preview--dancingatlas.lovable.app), not only on the dev server.

WHEN DONE
On the built preview open /mentor?lang=he and report: the H1; the seven section titles; the six labels of "Where the study stands"; the first rule of the DNA with its small line; the title of the first card under "When a learner struggles"; the six titles of the moments; the first three words of "How they sound"; the titles of the cards under "What BDF keeps in mind about a person"; and confirm that an example line reads left to right. Then open /mentor and report its H1 and the first rule of the DNA.
```

## Batch A — the message

Send when `mentor_brief.json` is live in `public/catalog/` (the stage `door` after the change of 23 November); the words are in `site.json` (`pages.dance.agent`). On the data of 23 November the text for one dance is about 7,100 words for `hustle` (active-ready) and 3,700 for `ahwash` (story only): the library's 8 rules, the mentor's brief (17 KB) and the dance file without its pictures, video lists and claim list. The message also carries the repair found while checking batch 9: no family chip where the index has no family (762 dances; the page shows "Folk" for each of them today).

```
BATCH A — WHAT AN AI TEACHER RECEIVES (the dance page /style/<slug>). Read the Project instructions first. Do exactly this and nothing else. If something is unclear, take the simplest reading and tell me what you chose; do not ask.

WHY
The destination of this library is a mentor that teaches in conversation: an agent, not this website. The last line of the dance page (the link "The file an agent receives for this dance") becomes a small section that shows what such an agent is handed for the dance and lets a person copy it as one text, to paste into any AI assistant. It is material for an agent, not a lesson: no player, no steps to click through, and no AI call from the site.

DATA
1. The dance file d/<slug>.json: already in memory for the page.
2. https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/manifest.json — contract "da_manifest_v1", about 6 KB. Fields used: base (an address), rules[] (texts).
3. https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/mentor_brief.json — contract "da_mentor_brief_v1", about 17 KB, rewritten only when it changes. Fields: what_this_is, stands_on {…}, default[] {theme, do, kinds_of_evidence}, moments[], when_it_is_hard[], when_a_feeling_shows[], what_teachers_believe[], how_they_sound[], remember[]; also contract, fingerprint, updated.
Files 2 and 3 are fetched only when the section's panel is opened or its button is pressed, the way the other files of the library are loaded (10-second timeout, one retry, kept whole in the browser database da_library_v2; a stored copy is used at once and replaced in the background when it differs). Add mentor_brief.json to the files /health checks.

THE SECTION (the last section of the details; it takes the place of the present last line)
Title t("pages.dance.agent.title","What an AI teacher receives"). Lead t("pages.dance.agent.lead","Dance Atlas is preparing for a mentor that teaches in conversation. This is what such an agent is handed for this dance: the rules of the library, how good teachers teach, and everything gathered about the dance. It is material, not a lesson.").
1. Three short lines, each with a tick: t("pages.dance.agent.rules","The rules of the library"); t("pages.dance.agent.mentor","How to teach, from the mentor's study"); t("pages.dance.agent.dance","Everything gathered about this dance").
2. When the dance file has teaching_withheld: the calm line t("pages.dance.agent.withheld","This dance is story only. An agent receives its story and nothing that teaches it.").
3. A button t("pages.dance.agent.copy","Copy for an AI"). It loads files 2 and 3 if needed, builds THE TEXT below and puts it on the clipboard with navigator.clipboard.writeText. When the clipboard is refused, it opens the panel of point 5 with the text selected and shows t("pages.dance.agent.manual","Select the text and copy it."). After a successful copy the button reads t("pages.dance.agent.copied","Copied. Paste it into any AI assistant and start talking.") for five seconds; the same sentence is announced in an aria-live="polite" region. When file 2 or 3 cannot be loaded: one calm line t("pages.dance.agent.unavailable","The briefing could not be put together just now. Please try again in a moment."), and nothing is copied.
4. Under the button, once the text has been built: one muted line "<number of words in the text> " + t("pages.dance.agent.words","words").
5. A closed panel t("pages.dance.agent.show","Show the text") (a real button with aria-expanded; opening it loads files 2 and 3 if needed): THE TEXT in a read-only, scrollable box, at most 60vh high, left to right, in the page's ordinary font.
6. Under the section, as today: the link t("pages.dance.agent.link","The file an agent receives for this dance") with t("pages.dance.agent.changed","Last changed") and the file's updated date; and beside it one more link t("pages.dance.agent.brief","The mentor's brief") to the address of file 3 (new tab, rel="noopener noreferrer").

THE TEXT (plain text, in exactly this order; a blank line between blocks)
Line: t("pages.dance.agent.text.heading","BRIEFING FOR AN AI DANCE MENTOR") + " — " + <the dance's name>
Line: t("pages.dance.agent.text.from","From the Dance Atlas open library:") + " " + <manifest.base>
Block: t("pages.dance.agent.text.frame","You are about to talk with one person about this dance, as their mentor. Follow the rules in part 1. Teach the way part 2 describes. Use only what part 3 holds about the dance, and say plainly what is not known.")
Block: t("pages.dance.agent.text.part1","PART 1 — THE RULES OF THE LIBRARY"), then the texts of manifest.rules, numbered "1. ", "2. " and so on, one per line.
Block: t("pages.dance.agent.text.part2","PART 2 — HOW TO TEACH (THE MENTOR'S STUDY)"), then JSON.stringify(<file 3 without its keys contract, fingerprint and updated>, null, 1).
Block: t("pages.dance.agent.text.part3","PART 3 — THE DANCE"), then JSON.stringify(<a copy of the dance file without these keys: fingerprint; card.images, card.video_stack, card.albums, card.album_candidates, card.hero_qc; profile.images, profile.albums, profile.claims, profile.citation>, null, 1).
Nothing else is added to the text and nothing in the two files is reworded.

ALSO ON THE DANCE PAGE: NO FAMILY IS CLAIMED WHERE NONE IS KNOWN
In the line under the dance's name (country · era · family), the family chip (the span with the class fam-chip) is shown only when the dance's entry in index.json has a family. Its text stays as it is today. A dance whose entry has no family shows no chip and no separator before it; this holds for every slide of the page. Today such a dance shows "Folk", which nobody has established (762 dances).

RULES
Read-only. No AI call, no new npm dependency, no analytics. No number is typed into the code. Keep the present components of the dance page: add this section and the rule for the chip, change nothing else on the page. Check the result on the built preview (https://preview--dancingatlas.lovable.app), not only on the dev server.

WHEN DONE
On the built preview open /style/hustle and /style/ahwash, open the details and report for each: the texts of the section; after pressing the button, the number of words shown, the first two lines of the text, the number of rules in part 1, whether part 3 of /style/ahwash holds a key "lessons" or a key "teaching" (it must hold neither), and the requests made when the button was pressed. Then open /style/bugg and report the line under the name (it must show no family chip), and the same line on /style/hustle (its chip as today). Report the rows of /health.
```


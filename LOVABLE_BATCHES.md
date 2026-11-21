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

## 5. The batches, in order of value

| # | Batch | What changes | From the direction | Data | Est. credits |
|---|---|---|---|---|---:|
| 1 | **Payment and accounts erased** | Membership, prices, trial, pop-ups, e-mail capture, influencer call, referral codes and sign-in are removed from code and screens. Hearts save on the device at once. "Profile" becomes "Saved" | "completely erased now" | `site.json` | 6 |
| 2 | **Loading that cannot break** | One door: a light index and one file per dance. The last good copy is kept in the browser's own database instead of the full session store. Timeouts, fallbacks, no blank screen. `/health` shows every data file and its contract | "extreme robust app"; thousands of profiles | `manifest.json`, `index.json`, `d/<slug>.json` (built 21 November; live with the first run of the stage `door`) | 11 |
| 3 | **The mentor** (`/mentor`) | The teaching DNA with its evidence, what a teacher does when a learner struggles, the six moments, beliefs, feelings, what BDF keeps in mind about a person, the teachers and the research | "cutting edge … the education of it"; mission 2 | `bdf_teaching_system.json` (live) | 6 |
| 4 | **The whole profile** | On the dance page: story in eight parts, music, movement, what the machine has gathered for teaching (steps with counts, cues, common mistakes, each with the lesson it came from), connections, footage, pictures, "N of M claims checked", and the meter "15 of 15: ready to activate" or what is missing. Shown as knowledge, not as a class | "drawing from all the database"; V12, V13 | `d/<slug>.json` | 9 |
| 5 | **The starting line** (`/starting-line`, and on Home) | How many profiles are ready to be activated, the ladder from listed to ready, the closest ones with what each needs, what holds pages back, growth over time | "overnight activate all the profiles"; mission 1 | `active_ready.json` (live), `machine.json` (to make) | 6 |
| 6 | **The machine room** (`/machine`), in Hebrew | For the owner, large type: did last night work, how fast it grows, what needs him | V16, V17; he reads Hebrew faster | `machine.json`, `site.json` | 5 |
| 7 | **The direction, in the owner's words** (`/vision`, and on Home) | What Dance Atlas prepares: BDF as an agent in conversation and virtual reality; now, next, later; the two missions with live numbers; why there is no course and no price | owner, 21 November; gate 10 | `site.json` | 5 |
| 8 | **Truth repairs** | Viral: read from GitHub like everything else (no database at run time), the order named for what it is, no rank that looks like popularity, credits by role. Atlas: a dance listed under every country it belongs to; a dance without a family shown as such; unknown shown as unknown | V02, V08, V09 | `index.json`; `viral.json` (to make) | 7 |
| 9 | **The door for a future agent** (`/library`) | A plain page: how any AI reads the whole library (the manifest, the contracts, the rules, the size, the safety copy), and on each dance page a link to the file an agent receives | "be ready for the breakthrough" | `manifest.json` | 4 |
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

The reserve is longer than the budget on purpose: estimates can be wrong in both directions, and the free 5 credits of each working day are spent before the expiring ones.

## 6. The meter: how every credit gets used

- After each batch: read "Credits used" under the answer and the rollover line in the balance window; write both into the record below.
- Targets for the rollover credits spent (Japan time): Sat 21 Nov 8 · Sun 22 Nov 30 · Mon 23 Nov 52 · Tue 24 Nov 72 · Wed 25 Nov 85 · Thu 26 Nov 90.9. Friday 27 November is a spare day. Expiry is Saturday 28 November.
- More than 10 behind a target: the next two batches go in one working session, or a reserve item is moved up. A batch far over its estimate: the last reserve items fall away.
- The last credits go to small finishing items until the rollover line reads 0. The 2.70 top-up credits are left alone.
- A message that passes 20 credits pauses with a card: continue only when the work shown is on the batch.

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

### How a message is sent (learned on 21 November)

The chat field of Lovable is a rich-text editor. Put the text in with `document.execCommand('insertText', false, text)` on the focused field: the page can fetch the text of a batch straight from this file on main. A synthetic paste event turns the text into an attachment, and typing it key by key would send it at the first line break. Check that the field holds the whole message and that the mode is Build, then press Send. The cost is in the menu "More options" under the answer (it opens on the second click). Of the free 5 build credits of the day, the first batch uses them all.

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
performances?[] { url, observation {<key>: text or list}, seen {…} }.
teaching_withheld? (a sentence). fingerprint, updated.
Every part may be absent. A value that is empty, "not described in sources", "Not described in sources.", "not in sources", "not derivable yet", "unknown" or "null" is not shown: no label, no heading, no empty card; a section whose values are all like that is not rendered.

THE SECTIONS, in this order (each a titled section in the page's present style; a key such as "origins_and_history" is shown with underscores replaced by spaces and the first letter capitalised)
A. Under the name: one chip from state. "active_ready" → t("pages.dance.state.active_ready","Ready to activate"); "building" → t("pages.dance.state.building","In the making") followed by "<have> of <of>"; the two withheld states → t("pages.dance.state.story_only","Story only"); nothing for "not_published" and "listed". A second chip for profile.tradition_status when it is living, revived or historical.
B. t("pages.dance.story.title","The story"): the profile.sections, each under its own small heading.
C. t("pages.dance.music.title","Music"): the music_profile as labelled lines, instruments and mood_keywords as chips, sound_description as a paragraph, reference_recordings as "title — artist", then albums with a link to musicbrainz_url.
D. t("pages.dance.movement.title","Movement"): the movement_profile as labelled lines, difficulty as a chip, signature_moves as "name — description", what_to_avoid on its own line.
E. t("pages.dance.teaching.title","What has been gathered for teaching") with the lead t("pages.dance.teaching.lead","Gathered by a machine from the sources and from lessons it studied. Not yet checked by a person."):
   E1 from profile.teaching: basic_steps as a numbered list, then rhythm, formation and level_notes as labelled lines.
   E2 t("pages.dance.teaching.from_lessons","From lessons the machine studied"): one closed panel per lesson, titled "<title> — <channel>". Inside: level · language · counting_scheme; the parts as lines "<t> · <segment> — <note>", each a link to the lesson's url with "&t=<seconds>s" added, opening in a new tab; the steps as "name — counts — description"; cues and images as chips; common_mistakes, safety, what_works and what_hinders as short lists; teacher_style and distinctive_method as labelled lines; then the muted line t("pages.dance.teaching.seen","Seen by a machine in this video, not checked by a person.").
   E3 t("pages.dance.teaching.from_performance","From the performance the machine watched"): one closed panel per performance with its observation as labelled lines, a link to its url, and the same muted line.
F. t("pages.dance.ready.title","Ready to activate?"): a simple bar "<have> of <of>". When state is "active_ready": t("pages.dance.ready.complete","Everything a teaching service needs for this dance has been gathered and source-checked. Not yet reviewed by a person."). Otherwise t("pages.dance.ready.missing","Still missing") and the labels of readiness.missing as a list. When ritual_context is true: t("pages.dance.ready.ritual","This dance has a ritual context. Carry its cultural note whenever it is taught.").
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

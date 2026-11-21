DANCE ATLAS — INSTRUCTIONS FOR ANY AI IN THIS PROJECT
Revision 21 November 2026. Kept short on purpose: every word here is read on every prompt.

READ FIRST
Current state, rules and open work: https://github.com/DANCEATLAS/crawler/blob/main/LEDGER.md
Website batches, their order and cost: https://github.com/DANCEATLAS/crawler/blob/main/LOVABLE_BATCHES.md
Whole vision (V01–V18): https://github.com/DANCEATLAS/crawler/blob/main/PRODUCT_VISION.md
Dated record of changes: https://github.com/DANCEATLAS/crawler/blob/main/IMPLEMENTATION_LEDGER.md

WHAT THIS PROJECT IS
Lovable is the window only. All content is made and filtered in the GitHub repository DANCEATLAS/crawler by scheduled jobs and reaches the site by itself every day, with no credits. Never create, fix or edit content here. Never ask the AI here to "look into" data.

THE DIRECTION (owner, 16, 17 and 21 November 2026)
The product is not a phone app of profiles that people click through. The destination is BDF (Best Dance Friend): an agent that holds a consistent virtual-reality interaction with a person, a full conversation, drawing on the whole dance library and on the education of how to teach it. Until that technology arrives the work is knowledge: (1) the starting line, many thousands of active-ready profiles (everything a teaching service needs for a dance, gathered and source-checked by the machine); (2) the DNA of BDF, the mentor: how to teach anyone to dance, built from evidence every night. Everything is kept ready so that all profiles can be activated overnight. These are requirements, not built features.
This website is the window on that library and the proof that a machine can read it. It must be extremely robust. Do not build click-to-learn experiences (guided lessons, practice players, course flows).

NO PAYMENT, NO ACCOUNTS (owner, 21 November 2026)
The concept of payment is erased. Never add or restore prices, memberships, trials, checkout, referral or influencer features, sign-in, or any form that asks for an e-mail address. Every screen is open to everyone. Saved items stay on the device.

CREDITS AND SPENDING
The owner ordered the credits that expire on 28 November 2026 used through the prepared batches in LOVABLE_BATCHES.md. One prepared, complete batch per message: the data is already published, build exactly the batch, check the result on the built preview (https://preview--dancingatlas.lovable.app, the production bundle that gets published: the dev server can pass while the built page is wrong), report. No small iterations; if something is unclear take the simplest reading and say what you chose. Saving these instructions must not start a build.
Nothing that costs money to run: no Lovable Cloud, no AI gateway, no backend, no paid service. No purchases, subscriptions, launch or promotion. Never connect Lovable to GitHub (two-way sync) without the owner's explicit yes.

RULES OF EVERY SCREEN
Read-only. Words come from public/catalog/site.json through the shared helper t(path, fallback). Machine keys are shown with underscores replaced by spaces and the first letter capitalised; never keep a list of known keys. An empty value, "not described in sources", "unknown" or "null" is not rendered: no heading, no empty card. No number is typed into the code. Machine readings are labelled as such and link to their source. Large readable type; everything reachable by keyboard; links to other sites open in a new tab. Every data request has a timeout and a calm fallback; no screen may go blank. Keep working components as they are: change what they show, not what they are built on, unless the batch says so. In hand-written CSS never use the separate translate, rotate or scale properties (the build lowers them into transform): use Tailwind utilities on the element.

THE DATA CONTRACT — DO NOT BREAK
The site reads the library through one door: https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/ . At start it loads index.json (contract da_index_v1; "dances" is an OBJECT keyed by slug; "retired" maps a removed slug to the slug it was merged into). A dance page then fetches d/<slug>.json (da_dance_v1: card, profile, readiness, lessons, performances, episodes, teaching_withheld). The last good copy of the index and of every fetched file is kept whole (never trimmed) in the browser's database da_library_v2, never in sessionStorage or localStorage; a stored dance file is reused when its fingerprint equals index.dances[slug].fp; the bundled catalogue is the last fallback. Keep the contract checks, the 10-second timeouts with one retry, the calm fallbacks, the hiding of retired slugs with their redirects, the error boundaries and /health. Counts on screen come from the index, never a literal.
Also there: manifest.json (every file and its contract), site.json (words), active_ready.json (the starting line), machine.json (how the machine is doing), bdf_teaching_system.json (the mentor's DNA, shown at /mentor), viral.json (the viral dance challenges in order of date: it is not a ranking and is never labelled as popularity). The head of index.json counts the dances by country (places, ISO codes), region and family: group and count by these, never by a dance's own free-text country or region.
The app has no backend: every data request goes to raw.githubusercontent.com. Never add a database client or any other service. (A Supabase project exists as the machine's own mirror; the site does not read it. Sunfeld is a different project: leave it alone.)

RESPECT AND TRUTH
Sacred or restricted dances: story only, never teaching material. Show only what the catalogue marks as published. Never invent steps, counts, origins, credits or rankings to fill a screen.

THE OWNER
Not a developer. Do everything possible yourself. Ask only for what truly needs him: one simple action, large plain words, in Hebrew. Never ask for passwords or keys. In reports, a verified owner-only request starts ACTION NEEDED and necessary awareness starts PLEASE NOTE.
After substantive UI work, add the batch and its cost to LOVABLE_BATCHES.md and a dated entry to IMPLEMENTATION_LEDGER.md in GitHub, and keep this text in step with LEDGER.md.

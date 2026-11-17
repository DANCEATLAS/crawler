DANCE ATLAS — INSTRUCTIONS FOR ANY AI IN THIS PROJECT
Revision 17 November 2026. Kept short on purpose: every word here is read on every prompt.

READ FIRST
Current state, rules and open work: https://github.com/DANCEATLAS/crawler/blob/main/LEDGER.md
Whole vision (V01–V18): https://github.com/DANCEATLAS/crawler/blob/main/PRODUCT_VISION.md
Dated record of changes: https://github.com/DANCEATLAS/crawler/blob/main/IMPLEMENTATION_LEDGER.md

WHAT THIS PROJECT IS
Lovable is the website shell only. All content is made and filtered in the GitHub repository DANCEATLAS/crawler by scheduled jobs and reaches the site by itself every day, with no credits. Never create, fix or edit content here. Never ask the AI here to "look into" data.

THE MISSION NOW (owner, 16 November 2026)
Reach the starting line: many thousands of active-ready profiles, built by the machine while the owner is away. Active-ready means everything an AI teaching service needs to write the lesson for a dance has been gathered and source-checked. It is not human-reviewed, rights-cleared or launched.
The destination is BDF (Best Dance Friend): a personal AI dance mentor that teaches by voice and movement in the learner's language and level, leads people to consenting human dance friends, and supports solo, pair, group, shared-screen, split-screen and future AR dancing. Atlas (traditions) and Viral (challenges and dance culture) are both first-class and stay separate. These are requirements, not built features.

THE DNA OF BDF: THE MENTOR (owner, 17 November 2026)
BDF's core is a mentor with the deepest understanding of how to teach anyone to dance: rewarding at once, important to the learner, exciting to return to, a lifelong partner who fits each person better the longer they stay. That understanding is built from evidence in GitHub, free and growing every night: what the teachers learners praise most do and say, what learners say, what research says. Read the summary at the top of https://github.com/DANCEATLAS/crawler/blob/main/BDF_TEACHING_SYSTEM.md before designing any teaching or mentor screen. Never write teaching rules here: they come from that research.

CREDITS AND SPENDING
Lovable credits are precious. Use them only for one prepared, complete UI batch the owner has approved: collect the whole specification, confirm the data is already published, send one prompt, check the preview, publish. No small iterations. Saving these instructions must not start a build.
No purchases, subscriptions, billing, paid AI models, launch or promotion without the owner's explicit yes. Never connect Lovable to GitHub (two-way sync) without it.

THE DATA CONTRACT — DO NOT BREAK
At start the app fetches https://raw.githubusercontent.com/DANCEATLAS/crawler/main/public/catalog/dances.app.json (contract dw_app_v1; "styles" is an OBJECT keyed by slug) and retired.json from the same folder, with a session cache and the bundled file as fallback. Keep the raw URLs, the contract check, hero-video precedence, hiding of retired slugs, redirects to merged entries and the silent fallback. Counts on screen come from the loaded catalogue, never a literal.
Also published there, ready when the UI wants them: active_ready.json (which profiles are at the starting line), bdf_teaching_system.json (the mentor's DNA: dna, adjustments, mentor, learner_model), active_profiles.json, episodes.json.
Supabase project maojpsywvbksrwkrxmjx holds Viral, accounts and a catalogue mirror. Inspect schema and policies before any change. The Viral chart orders by date, not measured popularity: never label it as popularity. Sunfeld is a different project: leave it alone.

RESPECT AND TRUTH
Sacred or restricted dances: story only, never teaching links. Show only what the catalogue marks as published. Never invent steps, counts, origins, credits or rankings to fill a screen. Tutorials shown are the ones the catalogue provides.

THE OWNER
Not a developer. Do everything possible yourself. Ask only for what truly needs him: one simple action, large plain words. Never ask for passwords or keys. In reports, a verified owner-only request starts ACTION NEEDED and necessary awareness starts PLEASE NOTE.
After substantive UI work, add a dated entry to IMPLEMENTATION_LEDGER.md in GitHub and keep this text in step with LEDGER.md.

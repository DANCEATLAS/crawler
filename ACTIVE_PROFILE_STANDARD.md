# Active Profile standard

Revision **DA-VISION-2026-11-11-ACTIVE**. Owner direction, 11 November 2026. Read with PRODUCT_VISION.md; this changes the destination from movie production to interactive readiness. A movie/script is one possible output, not the product or a readiness certificate.

An **Active Profile** is a versioned body of dance knowledge prepared to power excellent interaction when a delivery platform meets the standard. The ambition is many thousands of profiles: every living dance, meaningful local variants and new forms. Preserve historical/revived context and distinct Viral identities. There is no verified total of all living dances; never report percentage-of-the-world coverage from catalogue size.

## What the experience must enable

The first BDF is the personal AI platform guide. It must also help people find multiple **human Best Dance Friends**, through consented musical tastes, dance interests, language, experience, availability and preferred social experience. People learn together, share movement and music, develop friendships and belong. Human friendships are an objective, not merely another AI persona.

Prepare solo, pair and group learning; split-screen, shared-screen and live on-camera practice; shared playback with a common beat; and optional future augmented reality. AR can place a teacher, friends or formation in the learner's space. Each delivery mode needs its own testing. Internet video conferencing alone does not prove dancers are synchronized. Preserve the full Viral response/original-creation/distribution vision and the earlier global, multilingual, age/ability, cultural and music requirements.

## The information every profile needs

| Work stream | Evidence or material to acquire | Validation and unresolved questions |
|---|---|---|
| Identity and living practice | Community and native name, aliases, local variants, region(s), practitioner testimony, lineage, latest practice evidence, tradition/Viral links | Separate creator, popularizer and community; do not merge meaningful variants or confuse online rarity with endangerment |
| Movement | Named units, stance, weight transfer, foot contact, paths, timing, arms/torso/head/hands, transitions, partner roles, formation, essential vs expressive variation | Timestamped examples and practitioner review; label invisible mechanics and conflicting schools |
| Teaching | Objectives, prerequisites, demonstrations, count systems, cues, imagery, slow/full tempo, progression, corrections, learner checks and adaptations | Compare teachers and retain distinctive methods; frequent/popular does not mean optimal; test actual learning and retention |
| Interaction | Repeat/slow/pause/change-view intents, unit dependencies, correction branches, confidence/abstention rules, self-check fallback | Never invent count tolerances or feedback from unobservable motion; every branch needs evidence and a reviewed purpose |
| Music | Masterpiece references, musical form, rhythm, accents, tempo flexibility, phrase boundaries, instrumentation and culturally acceptable alternatives | Keep artistic quality, authenticity, licensing and intended use as separate reviews; see MUSIC_STRATEGY.md |
| Social experience | Solo/duo/group possibilities, contact/formation, shared rhythm, collaborative goals, preferred energy/social intent, turn-taking | Human BDF matching uses voluntary preferences; joining, contact, recording and publication are separate consents |
| Language and access | Native terminology and pronunciation, captions/counts, equivalent cues, space/equipment, seated/low-impact alternatives | Native and ability-specific reviewers; an English review does not approve every translation or life stage |
| Rights and cultural permission | Sources, instructor/performer consent, composition/recording/choreography/likeness/voice/footage rights, allowed uses and expiry | Reference/embedding permission is not permission to train, copy, distribute or impersonate; sacred/restricted teaching remains withheld |
| Deployment | Runtime format, camera calibration, timing measurements, device limits, offline/low-bandwidth fallback, cost per useful session | Content readiness is separate from runtime acceptance; no delivery date is assumed |

## Implemented preparation machinery

`python -m pipeline.run activation` is deterministic and offline. It creates:

- `active_profiles/atlas/<slug>.json` and `active_profiles/viral/<slug>.json`: existing candidate knowledge, references, exact missing work and a source fingerprint.
- `public/catalog/active_profiles.json`: additive versioned index. Existing `dw_app_v1` contracts and live UI remain intact.
- `pipeline_state/activation_gaps.json`: separate research, video, rights, human-review and platform queues.
- `ACTIVE_PROFILE_REPORT.md`: counts and technology evidence due for recheck.

The daily workflow runs this after translation. Only research gaps join the existing completion slots (at most one third of enrichment, maximum five; seven-day cooldown). Unchanged evidence avoids recomposition. Video study keeps its six-per-day budget, first eight-minute window and free-tier path; old extractions can be revisited after the existing 30-day cooldown to add timestamped evidence. New extraction records preserve viewpoint, observation limits and distinctive teaching methods. Existing low-resolution sampled video is not sufficient to validate fast footwork or weight transfer.

The queues expose work; they do not autonomously hire reviewers, clear music rights, acquire teacher permissions, search every language or implement social/AR features. Viral dossiers have a separate namespace and explicit input channel; the Atlas enrichment loop must not ingest Viral challenges as traditions. A dedicated bounded Viral research adapter remains to build.

## States and review contract

| State | Meaning |
|---|---|
| researching | One or more evidence/video/music prerequisites are missing |
| awaiting_review | Minimum candidate materials exist; current human review or scope is missing |
| teaching_withheld | Existing cultural/restriction policy blocks instruction; contextual research continues |
| ready_for_activation | Candidate prerequisites plus current, scoped human approvals exist; delivery platform still must pass its tests |
| runtime_active | Separate deployed, verified feature state; currently false for all profiles |

No legacy `movie_ready`, class checklist, generated script, model score or translation is mapped automatically to `ready_for_activation`. Compatibility fields stay available for old consumers and historical comparisons.

`pipeline_state/activation_inputs.json` is a public, editorial input registry keyed by `atlas:<slug>` or `viral:<slug>`. Each value may contain movement_profile, music_profile, interaction_profile, music_options and scope. Scope must declare languages, audiences, session_modes and territories. Viral research and videos may be supplied explicitly under their typed identity; do not reuse an Atlas record just because the slug matches. Never put private learner records, contact details, signed contracts, raw sessions or secrets here; store only appropriate public metadata and evidence references.

`interaction_profile` contains learning_units, prerequisites, feedback_rules and social_formats. New model research returns source-linked candidate entries, not approval. Unknown fields remain missing. Editors must resolve source conflicts and unobserved mechanics before approval.

`pipeline_state/activation_approvals.json` has a profiles object mapping each identity to review records. Required roles: practitioner, teaching, learner_outcomes, language, rights, social_accessibility. Each record requires role, human_review=true, exact current fingerprint, reviewer, evidence, decision=approved, reviewed_on and recheck_on (ISO dates). Evidence must document the actual methods, population, languages, modes and territories reviewed. Dates must include today. Changed source material invalidates approval. These structural checks cannot verify an attestation's truth; trusted editorial review and repository history are required. Never fabricate a reviewer or let a model self-certify.

Two distinct cleared, musically reviewed recording options are the initial selection gate. If a tradition legitimately permits only one piece or format, record the cultural reason and revise the gate through reviewed policy; do not manufacture a second option. All current music approvals are empty.

## Research and vetting arms to operate

1. **Coverage:** maintain a region/community/language/variant coverage matrix, prioritize underserved living traditions without claiming a complete denominator. Discovery stays capped at 40 new candidates per run. Use practitioner and local-language institutional sources alongside existing reference sources.
2. **Video laboratory:** compare at least two independent teachers per pilot; log exact movements and timestamps, teaching approach, uncertainty, accessibility and rights. Review disagreements rather than averaging them away. Learner trials compare comprehension, successful movement, retention, comfort and enjoyment; views/likes only select candidates.
3. **Learning-unit editor:** turn verified methods into reusable units and branching interactions. Start with several contrasting forms: solo rhythm, partner, line/circle and fast Viral movement. The specific representative sample depends on available evidence and permission, not a claim these are the best cultures.
4. **Music desk:** build reference and usable-asset lanes, musician listening reviews, rights evidence and use restrictions. Acquire permission before production or distribution. No music purchase is authorized by this standard.
5. **Human/community review:** find credible practitioners and teachers, document disagreement and consent, recruit voluntary trials when authorized. Researching possible reviewers is allowed; contacting them needs explicit messaging authorization.
6. **Technology and economics:** recheck primary documentation on the recorded due date; run a small permitted benchmark only when it can resolve a real gap. Record accuracy, abstention, latency, device coverage, rights, vendor dependency and full cost including retries, storage, egress and review.
7. **Continuity:** every substantive AI session updates GitHub's vision/implementation ledger, Lovable Project instructions and the Supabase AI context mirror or records an exact access blocker. Use matching revisions and canonical links. Do not claim that unrelated AI accounts automatically received an update.

## Acceptance before a pilot is activated

A practitioner and teaching reviewer agree which variations are acceptable. Learners can stop, repeat and recover from confusion; corrections demonstrably help on the tested devices. Native-language cues retain timing and meaning. Music fits the dance and every intended use is cleared. Users control camera/audio, matching, contact and recording; blocking/reporting, age separation and caregiver modes are tested. A network test covers jitter, drift, dropped connections and recovery with local beat playback or turn-taking fallback. AR must be optional with calibration, boundaries and accessible alternatives. Costs are measured against an approved ceiling; no quality target is quietly weakened to hit a budget.

Do not scale production to thousands until these pilot gates work. Scale research and reusable evidence now; defer expensive generation and storage until their contribution is proven.

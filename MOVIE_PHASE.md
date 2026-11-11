# Script and production preparation for Dance Atlas

**Superseded destination, 11 November 2026:** Active Profile is the current goal. Read ACTIVE_PROFILE_STANDARD.md and PRODUCT_VISION.md. The historical movie/script metrics below remain for compatibility and useful presentation assets; they do not establish interactive readiness.

**Current direction: DA-VISION-2026-11-09-BDF.** Read `PRODUCT_VISION.md` in full. Batch episodes remain useful, but the destination is the lifelong Best Dance Friend mentor connecting Atlas, Viral learning/creation, music discovery, global community and future spatial experiences. `IMPLEMENTATION_LEDGER.md` distinguishes what is built, tested, published and still required.

## Existing preparation system

| Component | Files / behavior | Actual meaning |
| --- | --- | --- |
| Research | `research_results/`, `qc_results/`, `public/catalog/` | Structured evidence and automated quality review, not independent practitioner approval |
| Episode packs | `pipeline/episodes.py` → `episodes/<slug>.json` + `.md`, `public/catalog/episodes.json` | Introduction and three draft chapters where allowed, with gaps. The e2 foundation uses meaningful input fingerprints |
| Teaching analysis | `pipeline/pedagogy.py`, `pedagogy/teaching_patterns.json`, `ULTIMATE_TEACHER.md` | Extracted patterns from selected public tutorials; frequency or model extraction is not proof of best teaching |
| Music and visual briefs | `music_brief`, `visual_brief` in packs | Preparation for production, not rights clearance or validated output |
| Voice/wardrobe briefs | Pack `voice` and `visual_brief.wardrobe` | Default recognizable narrator and sourced wardrobe notes, with neutral fallback for restrictions |
| Translation | `pipeline/translate.py`, `episodes/i18n/`, `TRANSLATE_LANGS` | Machine-translated preparations until native review; existing checks do not establish equivalent teaching meaning |
| Gap feedback | `pipeline_state/episode_gaps.json` → research queue | Missing evidence prioritized within existing caps; repeated unchanged evidence should not trigger repeat composition |
| Reporting | Existing daily/weekly reports | Structural progress. Do not equate a complete script with a release-approved lesson |

The current daily workflow budgets remain `PEDAGOGY_BUDGET=6`, `EPISODE_POLISH=4`, `TRANSLATE_BUDGET=6`, alongside research/media caps in `AI_BRIEF.md`. The normal workflow uses free tiers and a prepaid fallback; production, hosting, review and future services are not costless. No new generation service is activated by this document.

## Current scene structure, and its limits

An introductory episode has hook, place/history, occasion, demonstration, music, costume, people, family/related dances, first step where permitted, and close. Existing chapters cover objective, posture, rhythm, layered steps, combination, mistakes, music run and recap. Historical defaults are about nine minutes for the introduction and thirteen for a chapter. These are editable preparation defaults, not mandatory durations for every culture or learner.

An ordered list of steps split among three chapters does not prove a progression. Different traditions require different rhythmic frameworks, forms and teaching structures. Do not infer that all dances have an eight-count, a uniform beginner/intermediate/advanced ladder or interchangeable posture. The intended reusable learning unit has an objective, prerequisites, evidence, motion/timing, demonstration, cues, practice, correction, adaptation limits and an observable progression test.

The e2 foundation preserves missing posture/mistakes as gaps, avoids dance-specific counts derived from generic family teaching patterns, and exposes `release_status: not_validated` and music `rights_status: not_assessed`. Exact source support, movement accuracy, practitioner review and actual learning outcomes remain separate work.

## Cultural and evidence rules

- Sacred/restricted teaching remains withheld under current policy. Cultural context that is appropriate to share can still be presented. A public video is not permission to teach or reproduce ceremonial attire.
- Separate sourced fact, reconstructed presentation, derived teaching and reviewed adaptation. Do not invent mechanics to fill a scene.
- Quote occurrence and checks for added names/numbers do not establish full semantic accuracy. Narration polish must ultimately be checked against supported claims and instruction coverage.
- Images, footage, music, voice, likeness and motion each need documented permitted uses. Embedding/reference permission is not production reuse permission. Label synthetic reconstruction.
- Native dance names, pronunciation, counts and movement meaning must survive localization. Machine-translated and native-reviewed remain distinct statuses.
- A familiar editorial narrator remains a default; the expanded BDF vision permits individually chosen voice, tone, pace and instructor presentation. Changing personality must not change factual or movement content.

## Assets for BDF and Viral

Prepare shared knowledge and reviewed units for discovery, explanation, practice, feedback and creativity. BDF may select and explain approved material, repeat or slow it, change viewpoint and support a learner's goals. Movement feedback, memory/consent and age-specific interaction are not created by a script exporter.

Viral requires its own challenge identity, credited sequence, original track/version and context, linked to Atlas traditions where supported. Its creative workflow includes practice, tips, capture, costumes/outfits, backgrounds, synchronized/group or split-screen edits, credit/permission review and platform-specific exports. A new original dance must distinguish its creator's work and cultural influences from an authentic traditional form. A remix cannot silently become a ritual or community-endorsed performance.

Track collaborator contributions and permissions. Capture, editing, synthetic alteration, account connection and public distribution are separate uses/actions. Public sharing needs user-authorized destination and audience; no present publication is authorized by this future feature specification. Exact challenge music and independently composed practice music are not interchangeable. Asset generation should be staged and budgeted, with reuse prioritized.

## What still needs substantive work

1. Validate the learning-unit/asset contract against contrasting traditions and challenges, including irregular rhythms and solo/partner/group formats.
2. Establish claim-to-instruction coverage and culture-bearer/qualified teacher review. Source additional evidence when the reviewed lesson needs it.
3. Benchmark controllable motion, foot/contact/weight behavior, viewpoints, timing, speed changes and feedback confidence. A plausible video is not precise instruction.
4. Produce and evaluate original music under documented terms; tradition-specific musicians assess fit and credibility. Clear the actual assets before release.
5. Establish native-language equivalence, speech usability and tested accessible alternatives.
6. Implement BDF's controllable private memory, transparent AI identity and life-stage design; infant/toddler experiences are caregiver-led.
7. Build social creation/distribution and AR only with appropriate consent, moderation, age protection, timing and spatial checks for the offered mode.
8. Measure learner outcomes and total cost, including failures, review and serving. Obtain the owner's launch decision only after an actual reviewable result.

An exporter is an interface implementation after a platform/contract is demonstrated. Do not promise it will take one day or that choosing a generator eliminates research, validation or licensing work. Preserve vendor-independent JSON/Markdown and reusable assets. Technology changes should make the same rigorous content more useful, not force the atlas to be rebuilt.

# Technology readiness for Dance Atlas

Assessment date: 9 November 2026. This is a decision record, not an installed tool list or a purchase authorization.

## Conclusion

Do not assume the complete vision is either impossible or already solved. Relevant capabilities exist. Their documented capabilities and limitations do not establish Dance Atlas's required accuracy, cultural coverage, teaching effectiveness, multilingual consistency or unit economics. Those must be demonstrated on our own tasks.

| Component | Primary evidence checked | Decision for this phase |
| --- | --- | --- |
| Generated video | [Google Veo](https://deepmind.google/models/veo/) documents reference conditioning, extensions and consistency controls. Its published preference/visual benchmarks do not measure correct instruction across dance traditions. | Candidate for later benchmark; no bulk generation or purchase now |
| Interactive motion | [NVIDIA ARDY research](https://research.nvidia.com/labs/sil/projects/ardy/) demonstrates streaming text and pose-constrained motion. The [publisher's model card](https://huggingface.co/nvidia/ARDY-G1-RP-25FPS-Horizon52) reports foot skating, prompt failures, missing actions and limited environment awareness. The cited variant uses a robot skeleton; human-avatar variants require their own evaluation. | Evaluate constrained/approved motion plus a controllable renderer; no claim that it teaches a tradition correctly |
| Generated music | [Lyria 3.5 documentation](https://ai.google.dev/gemini-api/docs/music-generation?hl=en) describes music generation; its [model card](https://deepmind.google/models/model-cards/lyria-3-5/) evaluates audio quality and prompt adherence. These do not establish cultural authenticity or rights clearance for our outputs. | Prepare detailed musical briefs and a tradition-specific evaluation set; defer paid production |
| Copyright | The [US Copyright Office's output report](https://www.copyright.gov/newsnet/2025/1060.html) distinguishes sufficient human authorship from prompting alone. That US conclusion is not a worldwide rights guarantee. | Track contractual reuse rights, human contributions and provenance separately; assess production assets before release |

Architecture recommendation (an inference from these capabilities and the owner's requirements): separate knowledge, teaching units, motion, narration/music, rendering and assessment. Reuse reviewed motion and audio rather than regenerate a whole film for every learner. Allow an interactive planner to change pacing, explanation and sequence within validated boundaries. Benchmark a newer model only when it can improve a measured bottleneck at an acceptable cost.

Use several contrasting, non-restricted traditions to expose different requirements: different rhythms, solo/partner formations, movement complexity and language needs. Do not choose only examples that a vendor already demonstrates well. Freeze the source bundle, evaluation tasks and acceptance criteria; record failures as well as successes. A provider demonstration is a candidate signal, not a pass.

No new subscriptions, model deployments, training runs, music generations, video generations or recurring technology-watch schedules were created by this assessment.

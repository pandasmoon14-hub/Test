# Myravant — #493 installed-action coverage discovery baseline

Status: **executable author-curated discovery sample**, not a certified human-play or blind Set A/B acceptance report. Source of current runtime truth is the specific CI commit that generates `action-coverage-evidence.json`; this document cannot assert post-execution classifications in advance.

## Playable need

After larger vertical trials #524–#526, the remaining question is whether a player can *actually attempt* ordinary novel actions across multiple methods and families, rather than merely use well-rehearsed goal-shaped phrases. The next implementation must be chosen from executable evidence, not from synonyms, repository line count, or extra doctrine.

## Instrumentation (existing owners only)

`scripts/report_myravant_action_coverage.py` runs 39 author-curated, content-independent player attempts through the **installed `myravant-play` entrypoint**. Every attempt starts its own fresh fixture campaign, with a bounded setup context; the tool records the exact input, action route, result type, failure class, player-visible output, authoritative pre/post digests and checkpoint/trace hashes. It explicitly restores the real checkpoint and checks the authoritative digest against the trace. The attached evidence JSON is generated during Linux CI and uploaded without replacing the preexisting feedback-conditioned synthetic-play artifact.

The corpus spans 12 semantic families: self-perception, posture, traversal method, local observation, object placement, object operation, structure/transformation, projected placement, environmental improvisation, nonviolent interaction, time/duration and sequencing. The movement quartet deliberately holds goal, context, direction and target constant while varying **walk / sprint / sneak / crawl**. Results must not collapse those into equivalent mechanics merely because a verb is present.

Each case preserves an **authored** representable/novelty/ambiguous hypothesis with goal, method, target, modifier, and setup context. These labels are pressure hypotheses, not final gold truths. Output categories distinguish actual owner-executed state changes, read-only observations, specific contextual refusals, unsupported novelty, possible false-unsupported cases, and requests needing clarification. An explicit, qualified refusal does not count as successful execution. An unsupported request does not prove the physical act should have succeeded. Outcomes cannot be counted as a 95% Set A pass without independently authored gold labels.

## Guardrails

- No new state authority, parser, rule, universal attempt resolver, NPC planner, skill, arbitrary material or new fictional place was added.
- A synthetic pressure description is not permission to fabricate anatomy, force, social acceptance or environmental affordances.
- Source trace/receipt evidence identifies where work actually succeeded, failed lawfully, or was unrecognized; the evaluator itself does not rewrite runtime truth.
- Each case is an isolated session. It is a cross-family **baseline**, not a claim to have explored a complete sustained campaign or independent 500-case unseen Set A/B dataset.
- Existing #489/#491 sessions remain an independent source of feedback-conditioned multi-turn pressure; do not replace those with the cleaner isolated-case score.
- No human-play gate or #493 closure is authorized by producing this file.

## Decision rule after the first report

Group observed gaps by **underlying missing mechanic or interpretation**, rather than by the name of the target or verb. Prioritize families where the same ordinary intent is represented by several methods but only one is truly executable. Selection candidates likely include posture plus movement method, spatial manipulation beyond one declared direction, and local sensory alternatives. Select only after reading the CI trace rows and checking which existing owners could lawfully support the behavior. The first implementation must add at least one new *executable* behavior, not only add a lexical alias.

CI invocation:

```bash
python scripts/report_myravant_action_coverage.py --output action-coverage-evidence.json
```

The `action-coverage-evidence.json` artifact is the version-specific evidence. It must report zero invented mechanics, preserve source inputs, and state the limits of its authored labels. A future independently held-out Set A/B evaluation may use the same evidence schema, but must not recycle these authored cases as unseen.

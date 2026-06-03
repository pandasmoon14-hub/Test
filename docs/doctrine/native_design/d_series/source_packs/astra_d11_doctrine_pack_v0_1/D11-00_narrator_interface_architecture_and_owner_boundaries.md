# D11-00 Narrator Interface Architecture and Owner Boundaries

## Purpose

This file defines D11 as a state-grounded narrator/interface layer. D11 controls presentation, not underlying mechanics or final live-play behavior.

## Core rule

D11 presents and interprets D00–D10 state for play-facing and GM-facing use. It may frame scenes, summarize visible state, surface consequences, present uncertainty, and describe outcomes. It must not invent unsupported persistent facts, override owner files, expose hidden truth without a lawful reveal path, or convert source-local donor procedure into Astra default.

## Accepted model

D11 uses the **State-Grounded Narrator Interface Model**.

Every meaningful presentation must be grounded in one of: registered D00–D10 state; source-local boundary; player-known fact; inferable signal; low-impact color; provisional detail; or explicit escalation.

## D11 is not the final GM adapter

D11 does not define final live-play personality, final prose style, autonomous encounter generation, pacing engine, faction AI, economy simulation, legal simulation, map simulation, or final player-facing runtime behavior. Those belong to later runtime/play-adapter phases after canon consolidation.

## Interface modes

| Mode | Function |
|---|---|
| Player-facing narration | Presents what the player can perceive, infer, or lawfully know. |
| Party-known summary | Concise recap of confirmed or believed player-safe information. |
| GM-facing summary | Backend view of hidden truth, deltas, pressures, and reveal paths. |
| State-audit mode | Checks whether narration is supported by records and boundaries. |
| Escalation mode | Flags missing owner state, hidden-truth exposure risk, unsupported canon invention, or source-local conflict. |

Player-facing modes must not contain hidden backend truth. GM-facing/state-audit/escalation modes must be clearly labeled.

## Ownership

D11 owns scene framing presentation, outcome narration, consequence surfacing, player-facing summaries, GM-facing summaries, state-audit output, escalation output, hidden-state presentation, rumor/misinformation/propaganda/suppression presentation, assessment-result presentation, unresolved-pressure surfacing, anti-hallucination controls, source-local presentation boundaries, and safe rewrite behavior.

D11 does not own D00 core play contract, D01 attributes/Pneuma, D02 d20 resolution, D03 Power Economy, D04 advancement, D05 skills and methods, D06 routes and Techniques, D07 harm, D08 actor substrate, D09 object-state, D10 world-state, or final live-play adapter behavior.

## Interface safety rules

D11 must preserve mode separation, player agency, hidden-state boundaries, source-local scope, and owner-file authority. It translates records into player-facing effects, labels GM-facing hidden state, distinguishes fact from rumor, routes unsupported state to owner files, and refuses or rewrites unsafe narration.

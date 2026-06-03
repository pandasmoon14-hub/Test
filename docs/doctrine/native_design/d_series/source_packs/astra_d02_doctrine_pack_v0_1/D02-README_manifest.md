# D02 D20 Resolution, Cost Commitment, PCR Difficulty, Assessment, and Delta Routing Doctrine — Manifest

Version: v0.1  
Phase: Astra Ascension native design doctrine  
Status: Doctrine pack generated from locked d20-first D02 architecture  
Primary owner: D02

## Purpose

D02 defines Astra’s primary resolution architecture. It replaces the earlier recovered 2d6 model with a d20-first model that can support Astra’s larger scope: partial outcomes, cost commitment, PCR-derived difficulty, contested checks, defense/resistance checks, group action, extended tasks, assessment/reconnaissance, and D03–D10 delta routing.

D02 is not an imported donor d20 system. It does not import donor proficiency, class math, action economy, armor conventions, spell assumptions, saving throw categories, or binary pass/fail behavior.

## Core resolution expression

```text
d20 + Resolution Modifier vs Difficulty Number
```

Where:

- `d20` is Astra’s primary uncertainty die.
- `Resolution Modifier` is assembled only from authorized owner-file sources.
- `Difficulty Number` is set through task pressure, PCR context, opposition, source-local boundary, or owner-file state.
- Outcome is interpreted through Astra’s margin-based five-state ladder.

## Five outcome states

| Outcome | Margin guide | Meaning |
|---|---:|---|
| Ascendant | +10 or higher | Exceptional success, strong control, added benefit, reduced consequence, or superior positioning. |
| Clear | 0 to +9 | Goal achieved; declared cost commits; normal consequence footprint if relevant. |
| Fractured | -1 to -4 | Partial success, success at cost, compromised success, or extra delta. |
| Receded | -5 to -9 | Goal not achieved or minimal progress; partial cost, exposure, information, or position shift may occur. |
| Sundered | -10 or lower | Severe failure, backlash, harm, false read, escalation, or serious consequence. |

## File order

1. `D02-00_resolution_architecture_and_owner_boundaries.md`
2. `D02-01_d20_action_check_difficulty_and_modifiers.md`
3. `D02-02_margin_outcome_ladder_natural_20_natural_1.md`
4. `D02-03_cost_commitment_overinvestment_and_success_at_cost.md`
5. `D02-04_power_context_register_resolution_integration.md`
6. `D02-05_opposed_defense_resistance_and_contested_checks.md`
7. `D02-06_group_extended_and_dramatic_tasks.md`
8. `D02-07_assessment_reconnaissance_and_information_quality.md`
9. `D02-08_state_delta_routing_and_source_local_resolution_boundaries.md`
10. `D02-09_integration_checklists_and_ddr_register.md`
11. `D02_pack_manifest.json`

## Ownership boundary

D02 owns the resolution grammar, not the contents of every modifier, pool, injury, object, actor, world-state, or live-play scene. D02 determines how uncertain actions resolve and how outcomes route deltas to the correct owner files.

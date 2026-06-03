# D08-08 Runtime Records, UI, and Owner Handoffs

## Purpose

This file defines how D08 actor-state information is recorded without forcing every NPC, pet, summon, swarm unit, drone, spirit, temporary construct, or background creature to receive a full character sheet. It is doctrine-shape work, not final database schema.

## Core rule

D08 records actor-state only at the depth needed to preserve continuity, function, agency, personhood, bond, harm, advancement, source-local boundaries, and owner-file validation. It supports deep records for meaningful actors and lightweight records for disposable, temporary, or low-impact entities.

## Record depth grades

| Depth grade | Meaning |
| --- | --- |
| Ephemeral entity | exists only for moment/action/scene; no durable record unless promoted |
| Simplified actor | basic category, body, function, and immediate state |
| Functional actor | enough state for recurring use, conflict, travel, utility, or bounded interaction |
| Persistent actor | durable identity, continuity, body-state, harm, and relation records |
| Major actor | memory, goals, agency/personhood profile, continuity, world relevance, owner handoffs |
| Companion-grade actor | bond record, permissions, limits, harm, growth posture, continuity |
| Route-bearing actor | can hold D06 Routes, Techniques, Principles, or Route Features |
| Source-local actor | uses bounded donor/campaign actor rules requiring boundary record |
| Escalated actor | current doctrine cannot classify safely |

## Record families

D08 record families are actor-state header, continuity/personhood/agency, body/kinform/form-state, companion/bond, summon/construct/bound entity, distributed actor, actor advancement/evolution, and source-local actor conversion. Durable actors receive only the record families they need.

## Durable thresholds

A durable D08 record is required when an actor persists beyond the scene, has meaningful identity/name, has personhood or contested personhood, has agency that matters, has companion/bond interface, has route-bearing or advancement posture, has nonstandard body/form/source-local physiology, has meaningful harm or recovery, has memory/goals/social/faction state, is a persistent summon/construct/AI/spirit/swarm/bound entity, has source-local rules, requires owner handoff, or may return later.

No durable D08 record is required for pure action effects, disposable summons with no persistence, unnamed extras with no consequence, background animals without bonds, swarm units that do not matter individually, object functions without actor-state, or flavor-only transformations with no system consequence.

## Visibility states

Accepted states: visible, identified, partially identified, misidentified, hidden, obscured, disguised, dormant, transformed, source-local, retired. Hidden, obscured, disguised, or misidentified actor-state should be discoverable through appropriate assessment, investigation, D05 knowledge, D06 route sense, D07 symptoms, D09 scan, D10 inquiry, or source-local method.

## UI grouping

Future UI groups actors by function: Player Characters, Major NPCs, Companions & Bonds, Summons & Bound Entities, Creatures & Opposition, Forms & Transformations, Distributed Actors, Source-local Actors, Retired/Historical Actors, and Hidden/Unknown Actors. D10 later may add relational grouping by faction, valence, kinship, enmity, territory, and social memory.

## Promotion, demotion, retirement, history

Actor record depth can change. Promotion examples: unnamed guard becomes recurring rival, temporary summon gains memory, pet becomes bonded companion, AI assistant develops personhood, monster is spared and joins a faction, swarm develops collective cognition, source-local creature becomes important, enemy survives death and becomes nemesis-grade, companion evolves. Demotion examples: temporary actor dismissed with no consequence, minor NPC no longer relevant, companion bond severed, summon expires, swarm disperses, actor dies with no continuation.

Historical retention is required when the actor had bond, personhood, proof relevance, route relevance, terminal harm, D10 social memory, source-local boundary relevance, possible return, scar, inheritance, successor, copy, faction consequence, or world consequence.

## Handoff states

Handoff states are none, pending, resolved, blocked, dangerous, source-local, and escalated.


## Owner boundary

D08 owns actor-state substrate. It does not own every system attached to an actor. D03 owns Power Economy, carriers, reservoirs, costs, and sustainment. D04 owns advancement proof, tiers, breakthroughs, and capstones. D05 owns training, handling, research, diagnosis, medicine, and command methods. D06 owns Routes, Paths, Principles, Techniques, and Route Features. D07 owns harm, injury, corruption, mutation harm, recovery, and terminal outcomes. D09 owns items, relics, tools, implants, prosthetics, platforms, ships, mechs, drone hardware, and anchors. D10 owns factions, culture, law, reputation, social recognition, relationship graphs, territory, and world-state. D11 and later runtime adapters own presentation and live-play behavior.


## Record header shape

```yaml
d08_actor_record_header:
  actor_ref: string
  display_name: string
  source_ref: string
  record_depth: ephemeral_entity | simplified_actor | functional_actor | persistent_actor | major_actor | companion_grade_actor | route_bearing_actor | source_local_actor | escalated_actor
  actor_categories: [person, creature, kinform, companion, summon, spirit_nonmaterial, ai_machine, swarm_hive_colony, avatar_projection, anchor_bound, possession_adjacent, source_local, mixed]
  persistence: instant | scene | session | task_bound | duration_bound | relationship_bound | persistent | source_local
  visibility_state: visible | identified | partially_identified | misidentified | hidden | obscured | disguised | dormant | transformed | source_local | retired
  record_families:
    actor_state_header: string
    continuity_personhood_agency: string | null
    body_kinform_form_state: string | null
    companion_bond: string | null
    summon_construct_bound_entity: string | null
    distributed_actor: string | null
    actor_advancement_evolution: string | null
    source_local_actor_conversion: string | null
  active_status_summary: string
  handoff_state:
    D03: none | pending | resolved | blocked | dangerous | source_local | escalated
    D04: none | pending | resolved | blocked | dangerous | source_local | escalated
    D05: none | pending | resolved | blocked | dangerous | source_local | escalated
    D06: none | pending | resolved | blocked | dangerous | source_local | escalated
    D07: none | pending | resolved | blocked | dangerous | source_local | escalated
    D09: none | pending | resolved | blocked | dangerous | source_local | escalated
    D10: none | pending | resolved | blocked | dangerous | source_local | escalated
  history_retention_required: boolean
```

## Safeguards

D08 records interfaces but does not duplicate D03, D06, or D07. Source-local actor records must visibly preserve allowed use, prohibited generalization, normalized outputs, rejected assumptions, handoffs, and promotion requirements. Source-local vampire rules do not imply all Astra undead share those traits.

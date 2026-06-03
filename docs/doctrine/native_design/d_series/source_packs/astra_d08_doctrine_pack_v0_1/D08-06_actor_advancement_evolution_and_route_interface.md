# D08-06 Actor Advancement, Evolution, and Route Interface

## Purpose

This file defines how actors can grow, evolve, transform, or remain static without making every actor use full player-character progression. It routes progression fantasy, LitRPG, cultivation, monster evolution, companion growth, AI emergence, construct upgrading, spirit maturation, distributed growth, bloodlines, body cultivation, and source-local evolution systems.

## Core rule

D08 defines whether and how an actor can grow as an actor. It records actor-state evolution, form-state change, body/kinform shift, continuity alteration, companion growth, construct upgrade, AI emergence, swarm expansion, or source-local transformation state. It does not independently grant Route Features, advancement proof, Power Economy changes, harm consequences, equipment effects, or social status.

## Advancement postures

Accepted postures include non-advancing, full advancement, limited advancement, track advancement, evolutionary advancement, bond advancement, route-bearing advancement, training advancement, construct/upgrade advancement, distributed growth, source-local advancement, and escalated advancement. This allows pack mules, bonded wolves, evolving dragons, ship AIs, fungal colonies, summoned eidolons, and undead dual-state actors to use appropriate growth models.

## Advancement, evolution, transformation, conversion

Advancement is durable increase in capability, access, stage, proof, authority, or development state. Evolution is durable actor-state change. Transformation is state/form change that may be temporary, permanent, physical, spiritual, conceptual, hybrid, harmful, beneficial, controlled, uncontrolled, source-local, or terminal. Conversion is change from one actor-state, body-state, route-state, Power Economy, faction identity, source-local state, or metaphysical condition into another.

## Trigger taxonomy

Triggers include accumulation threshold, comprehension breakthrough, external catalyst, trauma/near-death, ritual/practice, multipath convergence, inherited awakening, accidental confluence, and source-local trigger. D08 records the actor-state trigger; D03/D04/D05/D06/D07/D09/D10/source-local own their domains.

## Process phases

Phases include preparation, dissolution, remolding, validation/tribulation, integration, vulnerability window, stabilized state, and source-local process. D08 owns the record of what the actor becomes, not all gates, resources, harms, or rewards.

## Evolution aspects

When relevant, records classify domain, scale, direction, reversibility, and origin:

- Domain: physical/body, spiritual/soul/energy, conceptual/Principle, hybrid, source-local.
- Scale: minor, major, existential, source-local.
- Direction: ascending, divergent, descending/corrupting, balanced/partitioned, source-local.
- Reversibility: permanent, temporary, cyclical, conditional, source-local.
- Origin: self-directed, imposed, inherited, accidental, ritualized, source-local.

## Outputs, affordances, and constraints

D08 records actor-state outputs: body substrate change, kinform evolution, species-state change, form-state gain, alternate form, dual-state condition, scale change, physiology, senses, maintenance need, vulnerability, resistance, communication, movement, lifespan, cognition/personhood change, agency/control change, continuity change, companion/bond change, swarm/colony node change, source-local template, D03 carrier interface, D06 route pressure, D07 harm/mutation/scar, and D10 social recognition change.

Evolution is not pure upgrade by default. Affordances may include new senses, movement, body capabilities, environmental access, continuity options, or route eligibility. Constraints may include vulnerabilities, social alienation, maintenance needs, equipment incompatibility, loss of prior body functions, altered cognition, personhood dispute, resource dependency, vulnerability window, route incompatibility, carrier instability, faction attention, or source-local limits.

## Actor-type guidance

Player and major characters may use full, limited, route-bearing, evolutionary, or source-local advancement. Companions may use bond, training, evolutionary, track, route-linked, or source-local advancement. Momentary summons usually do not advance. Persistent summons may. Constructs may upgrade through D09 or emergent personhood. Spirits may mature through memory, oath, domain, worship, bond, route, or source-local spiritual rules. AI may learn, fork, merge, expand networks, or upgrade hardware. Swarms/hives/colonies may grow via units, nodes, memory, cohesion, or territory. Creatures/monsters may evolve through age, mutation, environment, bloodline, resource ingestion, source-local advancement, or proof.


## Owner boundary

D08 owns actor-state substrate. It does not own every system attached to an actor. D03 owns Power Economy, carriers, reservoirs, costs, and sustainment. D04 owns advancement proof, tiers, breakthroughs, and capstones. D05 owns training, handling, research, diagnosis, medicine, and command methods. D06 owns Routes, Paths, Principles, Techniques, and Route Features. D07 owns harm, injury, corruption, mutation harm, recovery, and terminal outcomes. D09 owns items, relics, tools, implants, prosthetics, platforms, ships, mechs, drone hardware, and anchors. D10 owns factions, culture, law, reputation, social recognition, relationship graphs, territory, and world-state. D11 and later runtime adapters own presentation and live-play behavior.


## Record shape

```yaml
actor_advancement_evolution_record:
  actor_ref: string
  advancement_posture: non_advancing | full | limited | track | evolutionary | bond | route_bearing | training | construct_upgrade | distributed_growth | source_local | escalated
  evolution_event_type: body_evolution | kinform_evolution | form_state_gain | alternate_form | dual_state | companion_growth | summon_persistence_growth | construct_upgrade | spirit_maturation | ai_learning | swarm_colony_growth | source_local_transformation | mixed
  trigger_type: accumulation_threshold | comprehension_breakthrough | external_catalyst | trauma_near_death | ritual_practice | multipath_convergence | inherited_awakening | accidental_confluence | source_local
  process_phase: preparation | dissolution | remolding | validation_tribulation | integration | vulnerability_window | stabilized | source_local
  transformation_aspects:
    domain: physical_body | spiritual_energy | conceptual_principle | hybrid | source_local
    scale: minor | major | existential | source_local
    direction: ascending | divergent | descending_corrupting | balanced_partitioned | source_local
    reversibility: permanent | temporary | cyclical | conditional | source_local
    origin: self_directed | imposed | inherited | accidental | ritualized | source_local
  actor_state_outputs: []
  benefits: []
  constraints: []
  owner_handoffs:
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D09: []
    D10: []
    source_local: []
```

## Examples

A bonded wolf becomes a dire guardian through shared trial: D08 records body scale/physiology change, D05 training, D07 vulnerability, D06 only if a route feature is authorized, and D10 social reaction. An AI co-pilot becomes emergent person: D08 changes personhood/agency, D09 owns platform, D10 owns legal recognition. A donor monster evolution table is retained or normalized by function, not imported.

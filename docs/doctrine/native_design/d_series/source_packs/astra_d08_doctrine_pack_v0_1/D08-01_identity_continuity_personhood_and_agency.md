# D08-01 Identity, Continuity, Personhood, and Agency

## Purpose

This file defines how Astra decides whether an actor remains the same actor over time and how it distinguishes personhood, cognition, agency, control, possession-adjacent states, and playability grade. It exists because body change, resurrection, undeath, cloning, AI copying, memory alteration, reincarnation, possession, swarm fragmentation, and source-local respawn systems cannot be resolved by one identity rule.

## Core rule

Actor continuity is a recorded relation across multiple anchors, not an assumption. Same body, same memory, same soul, same route, same legal identity, or same player-facing record may provide evidence, but no single anchor universally proves continuity.

## Continuity anchors

| Anchor | Meaning |
| --- | --- |
| Body continuity | same body, vessel, chassis, swarm body, or physical substrate persists |
| Memory continuity | actor retains remembered experience |
| Identity continuity | actor retains coherent selfhood, values, name, and I-relation |
| Agency continuity | actor remains the decision-maker controlling action |
| Soul / spirit continuity | same soul, animus, ghost, spirit, essence, or local equivalent persists if relevant |
| Route continuity | same D06 Path, Route, Principle, or route identity continues |
| Carrier continuity | same D03 Power Economy carrier, reservoir, or resource structure persists |
| Bond continuity | same companion, pact, kinship, summon, or relation links persist |
| Social continuity | D10 society, law, faction, or relationship memory recognizes continuity |
| Source-local continuity | donor/campaign rule defines continuity inside a bounded source-local frame |

## Continuity states

Continuous, altered, partitioned, copied, inhabited, replaced, severed, merged, fragmentary, dormant, source-local, and escalated are accepted continuity states. A clone may preserve memory but not body. A resurrected actor may preserve identity but alter body. A possessed host may preserve body but lose agency. An AI copy may preserve memory and create a disputed second actor. A reincarnated actor may preserve soul but not memory or social continuity.

## Personhood

Personhood is separate from actor status. An actor can be valid without full personhood. States include full, limited, emergent, fragmentary, contested, none, and source-local personhood. D08 does not solve moral philosophy universally; it provides recordable states and escalation paths for AI, spirits, constructs, animals, summons, swarms, bound entities, clones, and source-local beings.

## Cognition profiles

Cognition describes how an actor processes information and remains separate from personhood and agency. Accepted profiles include sapient, sentient, instinctive, trained, programmed, ritualized, collective, fragmentary, foreign, and source-local.

## Agency and control

Agency describes who chooses action. Control describes who directs or constrains action. Accepted states include full agency, limited agency, instinctive, commanded, bond-guided, programmed, ritual-bound, summoned-bound, possession-contested, external-controlled, dormant, fragmentary, and source-local. Commanded does not mean no personhood. A loyal soldier, trained mount, bound spirit, programmed AI, and enslaved person are not the same actor-state.

## Possession-adjacent states

D08 supports possession-adjacent states without treating all influence as full possession: none, influence, mark, rider, co-inhabitation, contest, override, possession-equivalent, integration, severed, and source-local. D07 owns harm from foreign will pressure. D08 owns actor-state/personhood/control. D06 owns route/Principle effects. D10 owns social, legal, factional, or cultural reaction.

## Playability and control grade

Accepted grades include player-character, companion, major NPC, minor NPC, creature, summon, hazard, object-actor, source-local, and escalated. This prevents every actor from requiring PC-grade state while preserving continuity for significant non-PC actors.


## Owner boundary

D08 owns actor-state substrate. It does not own every system attached to an actor. D03 owns Power Economy, carriers, reservoirs, costs, and sustainment. D04 owns advancement proof, tiers, breakthroughs, and capstones. D05 owns training, handling, research, diagnosis, medicine, and command methods. D06 owns Routes, Paths, Principles, Techniques, and Route Features. D07 owns harm, injury, corruption, mutation harm, recovery, and terminal outcomes. D09 owns items, relics, tools, implants, prosthetics, platforms, ships, mechs, drone hardware, and anchors. D10 owns factions, culture, law, reputation, social recognition, relationship graphs, territory, and world-state. D11 and later runtime adapters own presentation and live-play behavior.


## Record shape

```yaml
actor_continuity_personhood_record:
  actor_id: string
  continuity_state: continuous | altered | partitioned | copied | inhabited | replaced | severed | merged | fragmentary | dormant | source_local | escalated
  continuity_anchors:
    body: present | changed | absent | disputed | source_local
    memory: continuous | altered | partial | copied | absent | disputed | source_local
    identity: continuous | altered | fragmented | replaced | disputed | source_local
    agency: continuous | limited | contested | external_controlled | absent | source_local
    soul_spirit: present | changed | absent | disputed | not_applicable | source_local
    route: continuous | altered | severed | mutated | absent | source_local
    carrier: continuous | altered | partitioned | collapsed | absent | source_local
    bond: continuous | altered | severed | inherited | absent | source_local
    social: recognized | disputed | rejected | unknown | source_local
  personhood_state: full | limited | emergent | fragmentary | contested | none | source_local
  cognition_profile: sapient | sentient | instinctive | trained | programmed | ritualized | collective | fragmentary | foreign | source_local
  agency_control_state: full_agency | limited_agency | instinctive | commanded | bond_guided | programmed | ritual_bound | summoned_bound | possession_contested | external_controlled | dormant | fragmentary | source_local
  possession_adjacent_state: none | influence | mark | rider | co_inhabitation | contest | override | possession_equivalent | integration | severed | source_local
  playability_grade: player_character | companion | major_npc | minor_npc | creature | summon | hazard | object_actor | source_local | escalated
```

## Examples

A clone with copied memories while the original survives is usually copied continuity, not automatically the same actor. A living/undead survivor is usually altered or partitioned continuity. A possessed host may preserve body and memory while agency is contested. A ship AI fork may be copied or partitioned, with D09 platform and D10 legal recognition handoffs. A fungal colony person may have collective cognition and continuity across fragments, while D10 may dispute social recognition.

# D08-02 Body, Kinform, Form-State, and Nonhuman Physiology

## Purpose

This file defines how Astra represents what an actor structurally is. It separates body, kinform, species, ancestry, form-state, and physiology so donor race/species packages, creature templates, monster types, undead states, machine bodies, spirits, swarms, constructs, fungal bodies, body cultivation, cyberware, and transformations can be routed without importing bundled donor assumptions.

## Core rule

An actor’s body-state is not a single race/species tag. It is a layered record describing substrate, kinform, physiology, form-states, vulnerabilities, senses, movement, maintenance needs, D03 carrier interfaces, D07 harm interfaces, D06 route interactions, D10 social recognition, and source-local boundaries.

## Core terms

Body is the actor’s current structural substrate for presence, action, harm, perception, movement, and interaction. Kinform is a body-lineage or structural category by origin, inheritance, creation, transformation, design, cultivation, ecology, metaphysics, or source-local rule. Species is biological or ecology-facing kinform, not universal actor terminology. Ancestry describes inherited or historical origin lines. Form-state is a distinct current or possible body/presence state.

## Body substrate categories

| Substrate | Meaning |
| --- | --- |
| Flesh / organic | biological body with organs, tissue, metabolism, or equivalents |
| Undead | animated, altered, or sustained by death, memory, hunger, spirit, curse, or source-local rule |
| Construct | built, engineered, assembled, ritualized, or artificial vessel |
| Machine / synthetic | mechanical, cybernetic, robotic, AI-linked, synthetic, or platform body |
| Spirit / nonmaterial | ghost, ancestor, domain spirit, oath spirit, psychic presence |
| Swarm / hive / colony | distributed body made of many units or linked organisms |
| Plant / fungal | plantlike, fungal, mycelial, rooted, spore-bearing, ecological body |
| Mineral / crystalline | stone, crystal, metal, mineralized, or pressure-body |
| Elemental / energetic | fire, water, storm, shadow, light, force, plasma, or energy-body |
| Hybrid | multiple substrates meaningfully apply |
| Anchor-bound | body depends on relic, vessel, platform, shrine, weapon, ship, or object |
| Projection / avatar | projected, remote, temporary, representative, or interface body |
| Source-local | body follows bounded donor/campaign rule |

## Physiology profile

D08 describes physiology by function rather than fixed anatomy. Relevant fields include structure, scale, locomotion, manipulation, senses, communication, maintenance needs, respiration or equivalent need, sleep/rest or equivalent cycle, reproduction/replication/creation if relevant, lifespan/durability, repair/healing mode, vulnerability profile, resistance profile, carrier interface, route/body interactions, form-state compatibility, and source-local rules.

## Kinform boundaries

Kinform does not automatically determine culture, faction, morality, language, profession, Path, Route, Principle, Power Economy, social rank, world-state role, or advancement posture. A dragon kinform does not automatically imply a Dragon Route. An undead body does not automatically imply an undead Path. A machine body does not automatically imply AI personhood or machine-current Power Economy.

## Form-state doctrine

Form-states include current, alternate, dual-state, triggered, uncontrolled, projected, source-local, and retired forms. A form-state should be recorded when it changes function, harm interface, perception, route access, Power Economy, social recognition, or source-local behavior. Records identify source, control, stability, triggers, duration, costs, permissions, restrictions, vulnerabilities, D03 carrier interface, D06 route interface, D07 harm/recovery interface, D10 social/world interface, and source-local boundary.

## Dual-state handling

Dual-state actors are supported but owner-validated. A dual-state record must state whether this is one actor with two form-states, two linked bodies, or a source-local case; whether states are partitioned, balanced, leaking, or unstable; whether each form has distinct physiology, Power Economy, route permission, and social recognition; whether transition is voluntary; what happens if one form is harmed; and which owner files validate effects.

## Nonhuman physiology

Nonhuman physiology may affect injury, healing, vulnerability, tool use, environment, social recognition, Power Economy interface, and treatment/training. Crystal-bodied actors fracture and are annealed. Spirit actors may suffer name, memory, oath, anchor, or manifestation harm. Swarms lose units or cohesion. Fungal actors may suffer dry-air memory damage. Ship AIs require hardware repair and continuity review.

## Special substrate cautions

Undead is a body/form-state category, not a universal moral state. Undead actors are not automatically evil, mindless, contagious, route-bearing, or socially doomed. Construct or machine body does not automatically mean no personhood. Spirit/nonmaterial body does not automatically imply full personhood or cosmic authority. Source-local body templates must be decomposed by function.


## Owner boundary

D08 owns actor-state substrate. It does not own every system attached to an actor. D03 owns Power Economy, carriers, reservoirs, costs, and sustainment. D04 owns advancement proof, tiers, breakthroughs, and capstones. D05 owns training, handling, research, diagnosis, medicine, and command methods. D06 owns Routes, Paths, Principles, Techniques, and Route Features. D07 owns harm, injury, corruption, mutation harm, recovery, and terminal outcomes. D09 owns items, relics, tools, implants, prosthetics, platforms, ships, mechs, drone hardware, and anchors. D10 owns factions, culture, law, reputation, social recognition, relationship graphs, territory, and world-state. D11 and later runtime adapters own presentation and live-play behavior.


## Record shape

```yaml
body_kinform_form_state_record:
  actor_ref: string
  body_substrate: flesh_organic | undead | construct | machine_synthetic | spirit_nonmaterial | swarm_hive_colony | plant_fungal | mineral_crystalline | elemental_energetic | hybrid | anchor_bound | projection_avatar | source_local
  kinform_refs: []
  ancestry_refs: []
  form_state:
    current_form: string
    available_forms: []
    form_state_type: current | alternate | dual_state | triggered | uncontrolled | projected | source_local | retired
    control_state: string
    stability_state: string
    triggers: []
    duration: string
    costs: []
    vulnerabilities: []
    permissions: []
    restrictions: []
  physiology_profile:
    structure: string
    scale: string
    locomotion: []
    manipulation: []
    senses: []
    communication: []
    maintenance_needs: []
    repair_or_healing_mode: []
    vulnerability_profile: []
    resistance_profile: []
  interfaces:
    d03_carrier_refs: []
    d06_route_refs: []
    d07_harm_refs: []
    d09_anchor_platform_refs: []
    d10_social_world_refs: []
  source_local_boundary_refs: []
```

## Examples

A crystal-bodied miner is mineral/crystalline, fractures instead of bleeds, and may require mineral infusion or ritual annealing. A living/undead survivor is flesh/organic plus undead dual-state, with D07 corruption conversion, D03 carrier partition, D06 route boundary, and D10 social recognition. A source-local vampire template becomes undead form-state plus source-local boundary rather than universal undead law.

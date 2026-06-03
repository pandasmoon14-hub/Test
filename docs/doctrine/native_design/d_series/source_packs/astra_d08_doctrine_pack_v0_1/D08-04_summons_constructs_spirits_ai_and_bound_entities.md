# D08-04 Summons, Constructs, Spirits, AI, and Bound Entities

## Purpose

This file defines actors that are created, called, built, bound, programmed, hosted, anchored, summoned, or sustained by another system. It prevents summons, constructs, spirits, AI, and bound entities from being flattened into effects, items, or full characters by default.

## Core rule

A summoned, constructed, spirit, AI, or bound entity becomes a D08 actor only when it has meaningful persistence, agency, personhood, bond-state, harm-state, memory, route relevance, advancement relevance, or world consequence. Otherwise, it may remain a momentary effect, simplified temporary entity, item function, platform function, hazard, source-local construct, or owner-file handoff.

## Summon types and persistence

Summon types include momentary effect, temporary entity, persistent summon, bound servitor, pact entity, companion summon, source-local summon, and escalated summon. Persistence states include instant, scene, session, task-bound, duration-bound, anchor-bound, contract-bound, relationship-bound, persistent, and source-local.

A summoned blade-spark that strikes once is not an actor. A recurring crow familiar is. A summoned wolf for one scene may be temporary with simplified state. A source-local eidolon may be persistent companion-grade.

## Control, sustainment, and dismissal

Summons and bound entities may be commanded, instinctive, bond-guided, programmed, ritual-bound, contract-bound, negotiated, autonomous, hostile-bound, possession-contested, external-controlled, or source-local. Sustainment may come from D03 Power Economy cost, sustained focus, carrier burden, ritual maintenance, anchor object, contract terms, environment, faction/world permission, Route Feature, companion bond, or source-local rule. Dismissal may occur by voluntary release, duration end, cost failure, contract breach, harm, banishment, severance, anchor destruction, Route Feature loss, or source-local trigger.

## Constructs

A construct actor has a built, engineered, animated, assembled, programmed, grown, ritualized, or artificial body. Constructs include golems, animated armor, clockwork actors, biotech bodies, engineered organisms, drone bodies, artificial shells, magical servants, skeletal constructs, and source-local created beings. A construct may be no-personhood tool, limited actor, programmed actor, emergent person, companion, platform, source-local creature, or route-bearing actor. Construct body does not automatically mean no personhood.

## Spirits and nonmaterial actors

Spirit actors include ghosts, ancestors, domain spirits, oath spirits, dead memories, place spirits, summoned elemental intelligences, relic-bound echoes, shrine guardians, psychic imprints, and source-local spirits. They may be anchor-bound, place-bound, name-bound, oath-bound, memory-bound, ritual-bound, pact-bound, summoned, companion-grade, hostile, fragmentary, or source-local. Harm may affect name, memory, oath, anchor, manifestation, bond, domain relation, route, or identity coherence.

## AI and machine actors

AI/machine actors include ship AIs, drone minds, mech co-pilots, synthetic people, tactical assistants, artifact intelligences, digital ghosts, source-local machine spirits, swarm controllers, and uploaded actor copies. AI is not automatically item, tool, person, companion, or property. D08 records personhood, cognition, continuity, agency, body/chassis/platform relation, owner/controller, bond interface, and source-local limits.

## Bound entities and anchors

A bound entity is constrained by pact, oath, summoning, contract, ritual, programming, imprisonment, anchor, possession, faction law, debt, curse, or source-local rule. Records track binding source, voluntariness, terms, controller, escape conditions, breach consequences, agency limits, harm consequences, legality/social recognition, and source-local boundary. Binding does not erase personhood by default.

Anchor-bound actors may exist through relics, weapons, armor, talismans, shrines, corpses, vessels, platforms, ships, mechs, implants, books, memory archives, places, faction standards, or source-local objects.


## Owner boundary

D08 owns actor-state substrate. It does not own every system attached to an actor. D03 owns Power Economy, carriers, reservoirs, costs, and sustainment. D04 owns advancement proof, tiers, breakthroughs, and capstones. D05 owns training, handling, research, diagnosis, medicine, and command methods. D06 owns Routes, Paths, Principles, Techniques, and Route Features. D07 owns harm, injury, corruption, mutation harm, recovery, and terminal outcomes. D09 owns items, relics, tools, implants, prosthetics, platforms, ships, mechs, drone hardware, and anchors. D10 owns factions, culture, law, reputation, social recognition, relationship graphs, territory, and world-state. D11 and later runtime adapters own presentation and live-play behavior.


## Record shape

```yaml
summon_construct_bound_entity_record:
  entity_ref: string
  entity_category: momentary_effect | temporary_summon | persistent_summon | bound_servitor | pact_entity | construct_actor | spirit_nonmaterial_actor | ai_machine_actor | anchor_bound_actor | companion_summon | source_local | escalated
  persistence: instant | scene | session | task_bound | duration_bound | anchor_bound | contract_bound | relationship_bound | persistent | source_local
  agency_control_state: commanded | instinctive | bond_guided | programmed | ritual_bound | contract_bound | negotiated | autonomous | hostile_bound | possession_contested | external_controlled | source_local
  personhood_state: full | limited | emergent | fragmentary | contested | none | source_local
  binding_or_sustainment:
    source: string
    controller_refs: []
    terms: []
    duration: string
    sustainment_cost_refs: []
    anchor_refs: []
    breach_outputs: []
    dismissal_conditions: []
    escape_conditions: []
```

## Examples

A momentary flame hawk is a Technique effect, not D08 actor. A bound demon scholar is pact entity with full or contested personhood and contract-bound agency. A stone golem laborer may be construct actor, tool, or emergent person. A ship AI co-pilot is AI/machine actor plus D09 platform and possible companion. A shrine-bound ancestor is spirit/nonmaterial actor plus place/anchor handoff. A donor eidolon is persistent summon/companion and source-local unless normalized.

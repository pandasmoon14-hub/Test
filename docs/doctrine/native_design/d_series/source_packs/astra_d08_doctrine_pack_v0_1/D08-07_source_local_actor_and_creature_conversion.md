# D08-07 Source-local Actor and Creature Conversion

## Purpose

This file defines how Astra converts donor creatures, ancestries, species, monsters, NPC templates, companions, summons, constructs, spirits, AI entities, swarms, undead templates, transformation templates, and source-local actor systems without importing donor taxonomy as canon.

## Core rule

D08 does not import donor actor taxonomy as canon. It decomposes donor actor constructs into Astra-native actor-state functions, assigns lawful outcomes, preserves source-local boundaries when needed, and escalates missing doctrine rather than silently absorbing donor metaphysics, biology, morality, advancement, or social assumptions.

## Lawful outcomes

Every donor actor construct receives one outcome: direct Astra mapping, normalized Astra mapping, source-local retained construct, quarantined construct, or escalated doctrine problem. No donor construct is converted by vibe or name alone.

## Conversion questions

Ask whether the construct is actor, effect, item, hazard, faction, environment, route feature, or source-local construct; whether it needs persistence; what body substrate it uses; whether kinform/species/ancestry/template/form-state applies; whether it has personhood, agency, continuity complications, companion/summon/bound/construct/spirit/AI/swarm/anchor-bound status, advancement/evolution, donor-specific rules, and owner handoffs.

## Decomposition routing

| Pressure | Route to |
| --- | --- |
| Body, species, physiology, form-state, actor continuity | D08 |
| Damage, immunities, corruption, mutation, recovery, death | D07 |
| Power pools, innate energy, resource cost, summon sustainment | D03 |
| Advancement, evolution gate, proof, breakthrough, tier | D04 |
| Skills, training, handling, medicine, research, profession | D05 |
| Routes, Techniques, Principles, innate active abilities | D06 |
| Items, natural weapons as gear, implants, relics, platforms | D09 |
| Culture, faction, ecology, territory, reputation, law | D10 |
| Donor-specific taxonomy, cosmology, summon list, template logic | Source-local / quarantine |
| Missing Astra framework | Escalation |

## Ancestry/species/race conversion

Donor ancestry packages decompose into D08 body/kinform/senses/lifespan/movement, D10 culture/language/homeland/status, D03 innate Power Economy, D06 innate techniques or magical abilities, D04 bloodline awakening or advancement gates, D05 training traditions, D07 vulnerabilities and mutation risks, D09 equipment compatibility, and source-local cosmology/alignment assumptions. A donor ancestry does not enter Astra as one package unless source-local retention is explicitly chosen.

## Monster and NPC conversion

A donor monster stat block is decomposed into actor category, body substrate, cognition/personhood, agency, role, physiology, senses, movement, harm interface, route/power abilities, ecology, social role, and source-local assumptions. XP/CR/encounter math belongs to later balance/runtime, not D08 canon. Donor NPC templates decompose into actor-state, D05 profession/training, D06 abilities, D03 power, D10 faction/rank, D07 scars/corruption, and source-local assumptions.

## Companion, summon, construct, AI, swarm, and template conversion

Animal companions become companion actor plus care/training/bond. Familiars become companion/summon/spirit/animal actors depending source. Eidolons become persistent summon/companion with source-local boundary unless normalized. AI companions become AI/machine actors plus D09 platform if hardware-bound. Drone swarms become distributed actor plus D09/D03 handoffs. Undead, lycanthropy, vampirism, and transformation templates decompose across D08 body/form-state, D07 curse/hunger/corruption/recovery, D03 feeding/resource if any, D06 techniques if authorized, D04 evolution/gate if any, D10 social consequence, and source-local rules.

## Required source-local boundary record

Retained donor actor rules require a boundary record stating source or source family, retained actor rules, allowed use, prohibited generalization, normalized Astra outputs, assumptions rejected, owner handoffs, promotion requirements, and quarantine/escalation notes.

## Prohibited generalizations

- all undead are evil;
- all constructs lack souls;
- all familiars deliver spells;
- all swarms are mindless;
- all AI are property;
- all vampires share fixed weaknesses;
- all summoned beings vanish without consequence;
- all monster evolutions follow level thresholds;
- all playable ancestries bundle culture, morality, language, and innate magic.


## Owner boundary

D08 owns actor-state substrate. It does not own every system attached to an actor. D03 owns Power Economy, carriers, reservoirs, costs, and sustainment. D04 owns advancement proof, tiers, breakthroughs, and capstones. D05 owns training, handling, research, diagnosis, medicine, and command methods. D06 owns Routes, Paths, Principles, Techniques, and Route Features. D07 owns harm, injury, corruption, mutation harm, recovery, and terminal outcomes. D09 owns items, relics, tools, implants, prosthetics, platforms, ships, mechs, drone hardware, and anchors. D10 owns factions, culture, law, reputation, social recognition, relationship graphs, territory, and world-state. D11 and later runtime adapters own presentation and live-play behavior.


## Record shape

```yaml
source_local_actor_conversion_record:
  source_construct_ref: string
  donor_label: string
  donor_construct_type: ancestry_species | monster | npc_template | companion | summon | construct | spirit | ai_machine | intelligent_item | swarm_hive_colony | undead_template | transformation_template | monster_evolution | source_local_actor_model | mixed
  astra_actor_mapping:
    outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained | quarantined | escalated
    actor_categories: []
    body_substrate_refs: []
    kinform_refs: []
    form_state_refs: []
    continuity_notes: []
    agency_personhood_notes: []
    companion_bond_refs: []
    summon_bound_refs: []
    distributed_actor_refs: []
    advancement_posture_refs: []
  decomposed_components:
    d03_power_economy: []
    d04_advancement: []
    d05_training_research: []
    d06_route_technique: []
    d07_harm_recovery: []
    d08_actor_state: []
    d09_anchor_item_platform: []
    d10_social_world: []
    source_local: []
  prohibited_generalizations: []
  retained_source_local_rules: []
  normalization_requirements: []
```

## Examples

A donor playable ancestry with darkvision, language, culture, innate spell, weapon training, and faction hatred splits across D08, D10, D06/D03, D05, and source-local. A donor familiar becomes D08 companion/summon actor, D03 channel if present, D06 Technique only if authorized, D07 bond harm, and source-local spell-delivery unless normalized. A donor vampire template is source-local unless decomposed functionally.

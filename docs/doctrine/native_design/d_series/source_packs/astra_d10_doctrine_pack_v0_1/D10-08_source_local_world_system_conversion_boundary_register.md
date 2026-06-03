# D10-08 Source-local World-System Conversion and Boundary Register

## Purpose

This file defines how Astra absorbs donor world-facing systems without importing their kingdom rules, faction clocks, law levels, heat tracks, settlement stat blocks, market ratings, clue webs, rumor tables, travel systems, or domain actions as canon.

## Core rule

Every donor world-facing construct must receive a lawful outcome: direct D10 mapping, normalized D10 register mapping, source-local retained system, quarantine, or escalation. Donor world systems are decomposed by function before conversion. A donor label such as kingdom, faction clock, settlement score, law level, heat, market rating, influence, or domain turn does not become Astra doctrine by label alone.

## Lawful outcomes

| Outcome | Meaning |
|---|---|
| Direct D10 Mapping | Construct fits an existing D10 register with minimal change. |
| Normalized D10 Register Mapping | Construct is decomposed and rebuilt through D10 register fields. |
| Source-local Retained System | Donor rule remains bounded to its source/campaign context. |
| Quarantined Construct | Construct is unsafe or underspecified until later doctrine exists. |
| Escalated Doctrine Problem | Construct reveals missing Astra framework. |

## Conversion routing questions

For each donor world construct, ask whether it is fact, event, consequence, territory, location, faction, institution, law, ownership claim, economy pressure, reputation, relationship, information-state, or source-local subsystem; whether it affects persistent world memory; whether it has scope, visibility, persistence, resolution, decay, or retention; whether it bundles systems that must be split; whether it imports donor math, turns, tracks, ratings, ranks, clocks, prices, or tables; which D10 register receives state; what remains source-local; what assumptions are prohibited; what D03–D09 handoffs apply; and what lawful outcome applies.

## Donor kingdom/domain systems

Donor kingdoms/domains may include ruler legitimacy, settlement loyalty, taxation, armies, resources, domain turns, events, unrest, law, faction claims, war, diplomacy, building projects, market access, reputation, and source-local economy.

Routing:
- ruler legitimacy → Law / Authority;
- territory/borders → Territory / Location;
- domain events → Event / Consequence;
- courts/factions → Faction / Institution;
- unrest/loyalty → Reputation / Relationship;
- tax/supply/resource pressure → Economy / Scarcity;
- laws/edicts → Law / Authority;
- rumors/public belief → Information-State;
- turn mechanics → Source-local unless normalized.

A donor kingdom turn system is not Astra domain management by default.

## Donor settlement/city systems

Components include settlement stat blocks, law level, market rating, danger rating, district control, faction influence, crime heat, rumors, black markets, travel access, public order, corruption, and supply state.

Routing:
- districts/sites → Territory / Location;
- public order/unrest → Reputation / Relationship or Event / Consequence;
- law level → Law / Authority;
- market rating → Economy / Scarcity;
- faction influence → Faction / Institution;
- danger rating → Hazard / Location or source-local;
- rumors → Information-State;
- heat/wanted pressure → Law / Authority and Reputation.

Settlement ratings are signals, not universal Astra stats.

## Donor faction/influence/diplomacy systems

Reputation ranks, favor points, influence scores, faction clocks, diplomacy tracks, patron systems, loyalty scores, faction turns, and war moves route to faction identity, faction-state, reputation, favor/debt/obligation, faction influence, event/consequence pressure, faction relationships, patronage, and source-local turn/action economy. Faction clocks and influence scores do not become Astra faction AI.

## Donor law/heat/wanted/enforcement systems

Wanted levels, heat, bounty ratings, law levels, contraband tables, warrants, exile, docking denial, cyberware licensing, black-market penalties, and stigma route to enforcement pressure, law pressure, faction attention, reputation, jurisdiction, restriction, platform registration, economy/scarcity, and source-local enforcement tables. Heat and wanted levels are not universal Astra tracks.

## Donor economy/treasure/market/requisition systems

Gold prices, wealth-by-level, treasure parcels, market ratings, availability rolls, requisition ratings, crafting costs, salvage tables, cargo prices, trade goods, and domain production route to scarcity, strategic resources, market access, requisition pressure, treasure pressure, salvage value, crafting economy boundary, supply chain, and source-local wealth assumptions.

Donor wealth assumptions do not define Astra economy.

## Donor rumor/clue/intelligence/information systems

Rumor tables, clue webs, secret clocks, revelation lists, library research tracks, prophecy records, surveillance systems, faction intelligence ratings, map discovery, and investigation nodes route to information-state, D05 discovery handoff, map knowledge, law if surveillance is restricted, and source-local procedure.

D10 records information-state. It does not import investigation procedure.

## Donor hex/travel/map/region systems

Hex maps, travel times, encounter rates, terrain modifiers, weather, danger ratings, foraging, navigation, route access, hidden sites, landmarks, and region clocks route to territory/location, access/route state, hidden site, hazard profile, travel restriction, environmental state if persistent, map knowledge, source-local encounters/travel/survival, and later exploration doctrine.

D10 records place-state, not travel procedure.

## Donor corruption/apocalypse/war-front/clocks

Corruption clocks, doom tracks, invasion tracks, war-front progress, plague spread, faction countdowns, instability meters, cosmic pressure clocks, and disaster escalation route to territory/hazard/environmental state, event/consequence pressure, faction goals/conflict, public knowledge, D07 handoffs, and source-local clock mechanics.

Donor clocks are not default Astra timers.

## Boundary record requirements

Every retained donor world system needs source name/family, donor construct label, donor system type, retained rules, allowed use, prohibited generalization, normalized D10 outputs, owner handoffs, conversion notes, promotion requirements, quarantine/escalation notes.

Prohibited generalizations include: all factions use donor reputation ranks; all cities use donor law levels; all kingdoms use donor domain turns; all hex maps use donor travel rules; all markets use donor ratings; all rumors use donor tables; all clocks use donor countdown mechanics; all wanted systems use donor heat tracks; all treasure uses donor wealth assumptions; all settlements use donor stat blocks; all corruption zones use donor mechanics; all faction clocks become Astra AI; all domain actions become Astra runtime turns.

## Record doctrine shape

```yaml
d10_source_local_world_system_conversion_record:
  source_construct_ref: string
  donor_label: string
  donor_system_type:
    - kingdom_domain_system
    - settlement_city_system
    - faction_influence_system
    - law_heat_wanted_system
    - economy_market_treasure_system
    - rumor_clue_information_system
    - hex_travel_region_system
    - corruption_clock_apocalypse_system
    - war_front_conflict_system
    - downtime_event_system
    - source_local_adventure_state
    - mixed
  astra_mapping:
    lawful_outcome: [direct_d10_mapping, normalized_d10_register_mapping, source_local_retained, quarantined, escalated]
    mapped_registers:
      - event_consequence
      - territory_location
      - faction_institution
      - law_authority
      - economy_scarcity
      - reputation_relationship
      - information_state
      - source_local_boundary
  decomposed_components:
    world_state_facts: []
    event_consequence_components: []
    territory_location_components: []
    faction_institution_components: []
    law_authority_components: []
    economy_scarcity_components: []
    reputation_relationship_components: []
    information_state_components: []
    retained_source_local_components: []
  prohibited_generalizations: []
  owner_handoffs:
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    source_local: []
  source_local_boundary:
    retained_rules: []
    allowed_use: []
    normalization_outputs: []
    promotion_requirements: []
  quarantine_reason: string
  escalation_reason: string
  validation_state: [authorized, source_local, pending_owner_file, quarantined, escalated]
```

## Acceptance criteria

A source-local world-system conversion is valid when it identifies donor system type; decomposes bundled components into D10 registers; assigns lawful outcome; states retained local rules; states prohibited generalizations; records D03–D09 handoffs; and quarantines/escalates missing frameworks instead of inventing social/economy/faction lore.

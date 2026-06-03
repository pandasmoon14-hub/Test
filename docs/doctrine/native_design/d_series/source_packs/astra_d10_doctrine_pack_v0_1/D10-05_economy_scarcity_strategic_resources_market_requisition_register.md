# D10-05 Economy, Scarcity, Strategic Resources, Market Access, and Requisition Pressure Register

## Purpose

This file defines economy-facing world state without becoming a pricing engine, vendor simulator, crafting economy, trade simulator, or donor wealth system.

## Core rule

D10 records economy-facing state: what is scarce, who controls it, where it can be accessed, what restrictions apply, what supply pressure exists, what markets or institutions handle it, what factions care, and what unresolved economic consequence persists. D10 does not define final prices, vendor inventories, production math, or donor wealth assumptions.

## Scarcity signal

Scarcity signal indicates availability pressure without price math.

| State | Meaning |
|---|---|
| Abundant | Readily available in relevant context. |
| Common | Available through normal access. |
| Local | Available only in certain places, cultures, ecosystems, factions, or routes. |
| Specialized | Requires trained producers, facilities, guilds, sects, clinics, shipyards, or toolchains. |
| Limited | Supply exists but cannot meet broad demand. |
| Rare | Difficult to acquire; likely tracked. |
| Strategic | Control changes faction, military, advancement, route, platform, or world-state power. |
| Restricted | Access controlled by law, rank, taboo, license, treaty, or faction. |
| Forbidden | Possession, trade, harvesting, or production prohibited. |
| Monopolized | One faction/institution controls practical access. |
| Embargoed | Trade or transfer blocked. |
| Depleted | Supply exhausted or damaged. |
| Unstable | Supply fluctuates unpredictably. |
| Source-local | Donor/campaign scarcity rule. |

Scarcity is not price.

## Strategic resources

A strategic resource is a resource whose control meaningfully affects faction power, route access, advancement, platform operation, territory control, law, social status, or world-state conflict.

Examples include monster cores, concept-bearing materials, transformation catalysts, rare ores, starship fuel, reactor cores, cyberware-grade components, biotech tissue lines, alchemical reagents, spirit springs, relic shards, AI cores, shipyard access, drone production capacity, food under siege, medicine during plague, and source-local strategic materials.

D10 records control, scarcity, access, law, faction interest, unresolved pressure. D09 owns object/material records.

## Market access

Market access states include open market, restricted market, guild market, sect/order supply, corporate supply, military supply, black market, barter/favor market, auction/patronage, emergency rationing, closed, and source-local.

D10 records access state. It does not generate inventory or prices.

## Supply chain and trade route state

Supply states include stable, strained, disrupted, blockaded, embargoed, captured, sabotaged, corrupted, contaminated, depleted, rationed, monopolized, illegal, secret, and source-local.

Supply-chain records include resource/object category, source territory, transit route, controlling faction, chokepoints, legal restrictions, disruption, affected markets/factions, consequences, and resolution.

## Black markets

Black-market records may include market location/network, controlled object/resource category, controlling faction, risk state, law-zone interaction, access requirements, reputation/favor requirements, known/hidden state, enforcement pressure, and source-local boundary.

D10 owns illegality, access pressure, faction control, and enforcement state. D09 owns objects. D07/D08 own harm/personhood issues.

## Requisition pressure

Requisition is institutional acquisition, not purchase.

Requisition states include routine, limited, emergency, restricted, denied, substituted, debt-bearing, monitored, recallable, illegal diversion, and source-local.

D09 records issued object-state. D10 records authority, scarcity, obligation, monitoring, and institutional consequence.

## Treasure pressure

Treasure is not automatically spendable wealth. Treasure pressure types include currency-like wealth, trade good, strategic material, relic/artifact, contraband, salvage, catalyst, social gift, and source-local treasure.

D09 owns object-state. D10 owns economic/social pressure.

## Salvage value

Salvage-value signals include worthless, common scrap, reusable component, repairable subsystem, strategic salvage, illegal salvage, contaminated salvage, sacred/taboo salvage, actor-remains salvage, relic salvage, and source-local salvage.

D09 records recovered objects/materials. D10 records market access, legal claim, taboo, faction interest, and strategic value.

## Crafting economy boundary

D10 tracks access and scarcity of crafting inputs, not crafting procedure. It may record material scarcity, facility access, guild monopoly, licensed production, sect-controlled alchemy furnace, shipyard booking, clinic availability, strategic component shortage, embargoed reagent, black-market recipe, or source-local crafting economy.

D05 owns method. D09 owns object work.

## Exchange modes and perception

Astra supports currency, barter, favor, debt, oath, service, faction standing, requisition, ration allocation, strategic allocation, sacred offering, patronage, auction, black-market exchange, and source-local economy without choosing one universal exchange rate.

D10 separates actual scarcity from perceived scarcity. Knowledge states include public price pressure, hidden shortage, rumored discovery, suppressed market panic, false scarcity, faction-only knowledge, black-market rumor, disputed value, secret buyer, and source-local market rumor.

## Source-local economy systems

Donor gold prices, wealth-by-level, treasure tables, rarity economies, settlement market ratings, requisition ratings, availability rolls, faction favor points, domain production, kingdom income, trade goods, starship fuel costs, cyberware pricing, crafting costs, salvage tables, auction systems, and source-local currencies normalize by function or remain source-local.

## Record doctrine shape

```yaml
d10_economy_scarcity_state_record:
  economy_record_ref: string
  record_type: string
  subject_refs:
    object_refs: []
    material_refs: []
    resource_site_refs: []
    territory_refs: []
    location_refs: []
    faction_refs: []
    platform_refs: []
    actor_refs: []
    source_local_refs: []
  scarcity_state: string
  access_state: string
  supply_state: string
  controlling_faction_refs: []
  claimant_refs: []
  legal_restriction_refs: []
  market_visibility: string
  exchange_modes: []
  requisition_profile:
    requisition_state: string
    authority_refs: []
    return_or_debt_terms: []
    monitoring_terms: []
  consequence_links:
    event_refs: []
    consequence_refs: []
    unresolved_pressure_refs: []
  owner_handoffs:
    D03: []
    D04: []
    D05: []
    D07: []
    D08: []
    D09: []
    source_local: []
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [active, hidden, disputed, resolved, depleted, source_local, escalated]
```

## Acceptance criteria

An economy/scarcity record is valid when it treats scarcity as signal, not price; distinguishes actual scarcity from perceived scarcity; records market access without inventory generation; treats requisition as authority-pressure, not purchase; classifies treasure/salvage by pressure type; routes object/material/crafting/power concerns to owners; and blocks donor wealth systems from default import.

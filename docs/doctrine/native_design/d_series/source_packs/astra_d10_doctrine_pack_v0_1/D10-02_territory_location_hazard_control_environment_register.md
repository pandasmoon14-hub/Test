# D10-02 Territory, Location, Hazard, Control, and Environmental State Register

## Purpose

This file defines how Astra records places as persistent world-state: territories, locations, route access, hazards, corruption zones, sanctified zones, resource sites, control claims, public/secret maps, local laws, and platform-scale places.

## Core rule

D10 records persistent state about places. A place record says what the place is, where it sits in world-state, who controls or claims it, what conditions or hazards apply, what routes connect to it, what resources matter, what laws or restrictions apply, what is publicly known, and what source-local boundaries exist. D10 does not decide how exploration scenes are narrated or how travel checks are resolved.

## Territory vs. location

A territory is an area of control, claim, influence, hazard, jurisdiction, environment, or strategic importance. A location is a more specific place, site, structure, settlement, vessel, room-scale point, node, or platform.

A territory may contain many locations. A location may exist inside a territory. A platform may function as a location. A location may itself be contested or faction-controlled.

## Place records

A territory record may include territory reference, name, scale, parent region, child locations, controller/claimants, contested status, jurisdiction, environmental profile, hazard profile, corruption/sanctification/instability state, resource sites, strategic value, route connections, access restrictions, visibility/knowledge, public reputation, unresolved consequences, and source-local boundary.

A location record may include location reference, name, type, parent territory, physical/metaphysical status, condition, controller/claimant, access state, hidden/known state, hazards, notable objects/actors, resource or strategic value, law/permission state, public knowledge/rumor state, unresolved consequences, and source-local boundary.

## Place scales

Scales include micro-zone, site, settlement district, settlement, local region, regional domain, faction domain, world-scale territory, cosmic/multiversal region, and source-local scale.

## Control and claim

Control states include controlled, claimed, contested, occupied, liberated, abandoned, hidden control, fragmented control, autonomous, lawless, restricted, and source-local.

Control is not legitimacy. Legitimacy is not effective control. Public belief may differ from both.

## Access and route state

D10 tracks persistent access state; it does not own travel procedure.

Access states include open, restricted, blocked, dangerous, hidden, secret, sealed, contested, occupied, unstable, conditional, and source-local.

## Environmental and altered-zone state

D10 records persistent environmental state when it matters: normal, damaged, ruined, fortified, unstable, depleted, enriched, polluted, corrupted, sanctified, cursed, haunted, plague-bearing, radioactive, flooded, burning, frozen, starved, besieged, occupied, quarantined, sealed, or source-local.

D07 owns harm from exposure. D03 may own energy/resource environmental behavior. D06 may own route/domain/Principle resonance. D10 records place-state.

## Hazard register

Hazard types include physical, biological, energetic, spiritual, conceptual, social/legal, faction, corruption, and source-local hazards. Hazard records should include location/territory, type, severity signal, visibility, source, persistence, spread/containment, D07 handoff, and source-local boundary.

## Corruption, sanctification, and alteration zones

D10 supports altered places without making any donor metaphysics canon. Alteration states include corrupted, purified, sanctified, cursed, consecrated, haunted, reality-thinned, dimensionally unstable, spiritually saturated, conceptually aligned, dead zone, overgrown/living zone, machine-controlled zone, or source-local altered zone.

D10 records origin, scope, visibility, spread/containment, affected factions/actors, and consequences. D07 validates harm. D08 validates actor changes. D03/D06 validate power/route interactions.

## Resource and strategic sites

D10 owns resource-site world state, not extracted object mechanics. Resource site types include mine, spirit spring, monster nesting ground, fuel depot, salvage field, relic vault, cultivation garden, starship wreck field, leyline node, factory, sacred grove, data archive, and source-local resource site.

D09 owns extracted material/object records. D10 owns place control, claim, scarcity, secrecy, access, and faction pressure.

## Discovery and map knowledge

D10 separates actual place-state from map knowledge. Discovery states include known, known to faction, known to actor, rumored, mislocated, hidden, secret, lost, suppressed, disputed, and source-local.

A secret city can exist without being on public maps. A public map can be wrong.

## Law zones and platform locations

Place records may include law zones: weapons prohibited, cyberware illegal, relic possession restricted, undead forms forbidden, AI personhood recognized, salvage belongs to crown, sacred ground prohibitions, faction rank requirements, quarantine, black-market tolerance, source-local law.

D09 platforms may also be D10 locations when they have persistent place-state. D09 owns platform object-state; D10 owns place-state, inhabitants, law, faction control, registry/docking, public knowledge, and consequences.

## Source-local place systems

Donor hex maps, settlement stat blocks, kingdom domains, danger ratings, travel tables, law zones, market ratings, resource nodes, corruption clocks, encounter areas, and source-local maps normalize by function or remain source-local. They are not Astra defaults.

## Record doctrine shape

```yaml
d10_territory_location_state_record:
  place_ref: string
  place_kind: [territory, location, route, platform_location, resource_site, hazard_zone, law_zone, source_local]
  name_or_label: string
  parent_refs: []
  child_refs: []
  scale: string
  control_state:
    current_controller_refs: []
    claimant_refs: []
    control_status: string
    legitimacy_notes: string
  access_state:
    route_refs: []
    access_status: string
    access_requirements: []
  environmental_state:
    condition_tags: []
    alteration_state: string
  hazard_profile:
    hazard_refs: []
    hazard_types: []
    severity_signal: string
    spread_or_containment_state: string
    d07_handoff_refs: []
  resource_profile:
    resource_site_type: string
    resource_refs: []
    strategic_value: string
    depletion_or_enrichment_state: string
    d09_material_object_refs: []
  knowledge_state:
    discovery_state: string
    public_map_state: string
    secret_map_refs: []
  law_jurisdiction:
    law_zone_refs: []
    restrictions: []
    jurisdiction_refs: []
  consequence_links:
    event_refs: []
    consequence_refs: []
    unresolved_pressure_refs: []
  owner_handoffs:
    D03: []
    D06: []
    D07: []
    D08: []
    D09: []
    source_local: []
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [active, pending, resolved, hidden, source_local, escalated]
```

## Acceptance criteria

A place record is valid when it distinguishes territory/location/route/platform-location/resource/hazard/law-zone; separates control, claim, legitimacy, and public belief; tracks access without defining travel procedure; records hazards/altered zones with owner handoffs; distinguishes actual location state from map/discovery knowledge; and blocks donor hex/domain/travel systems from default import.

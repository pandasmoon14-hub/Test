# Astra Ascension D10 Doctrine Pack v0.1

Generated: 2026-06-02

This combined export contains the full D10 doctrine pack in file order.


---

<!-- FILE: D10-README_manifest.md -->

# D10 World-State, Faction, Law, Economy, Reputation, Information, and Source-local World-System Architecture — Manifest

Version: v0.1  
Phase: Astra Ascension native design doctrine  
Status: Doctrine pack generated from accepted D10 DDR decisions  
Primary owner: D10

## Purpose

D10 defines the persistent world-facing state architecture for Astra Ascension. It records what the world remembers, who controls or claims what, what factions know or want, what laws apply, what resources are scarce, what reputations and relationships persist, what rumors or hidden truths exist, and what consequences remain unresolved.

D10 exists because Astra must absorb a mixed donor corpus at the scale of roughly 200–400 sources. That corpus will include kingdoms, city districts, hex maps, star sectors, sect domains, faction systems, reputation systems, domain turns, law levels, wanted tracks, heat systems, market ratings, treasure tables, rumors, clue systems, apocalypse clocks, corruption clocks, war fronts, diplomacy tracks, resource sites, strategic economies, and adventure-state structures. D10 therefore uses layered registers, source-local boundaries, tiered record depth, unresolved pressure queues, and explicit handoffs.

## File order

1. `D10-00_layered_world_state_register_architecture.md`
2. `D10-01_world_state_event_consequence_persistence.md`
3. `D10-02_territory_location_hazard_control_environment_register.md`
4. `D10-03_faction_institution_rank_claim_goal_conflict_register.md`
5. `D10-04_law_ownership_custody_rights_legitimacy_authority_register.md`
6. `D10-05_economy_scarcity_strategic_resources_market_requisition_register.md`
7. `D10-06_reputation_relationship_social_memory_register.md`
8. `D10-07_information_state_public_knowledge_rumor_secrecy_records_register.md`
9. `D10-08_source_local_world_system_conversion_boundary_register.md`
10. `D10-09_runtime_records_ui_register_links_owner_handoffs.md`
11. `D10-10_integration_checklists_and_ddr_register.md`
12. `D10_pack_manifest.json`

## Core doctrine statement

D10 records persistent world-facing state. It records world-state facts, events, consequences, territories, locations, factions, institutions, law, ownership, rights, legitimacy, economy-facing scarcity, market access, requisition pressure, reputation, relationships, public knowledge, secrets, rumors, archives, intelligence, source-local world-system boundaries, unresolved pressures, and historical memory.

D10 does not own the mechanical substrates that generate those consequences. It does not define Power Economy mechanics, advancement, skill/research procedure, Techniques, harm mechanics, actor substrate, object-state, live-play narration, faction AI, legal simulation, economy simulation, travel procedure, investigation procedure, or final runtime UI.

## What D10 owns

D10 owns persistent world-facing state; world-state facts; event records; consequence records; timeline entries; consequence scope, visibility, persistence, decay, resolution, and historical retention; territory/location state; control, claim, occupation, access, routes, hazards, altered zones, strategic terrain, and discovery/map knowledge; faction/institution identity, ranks, authority, claims, goals, memory, subfactions, alliances, conflicts, sanctions, and debts; law/authority state; ownership, possession, custody, rights, legitimacy, restrictions, warrants, bounties, personhood recognition, platform registration, salvage rights, inheritance, and requisition authority; economy/scarcity state; scarcity signals, strategic resources, market access, supply-chain pressure, black markets, requisition pressure, treasure pressure, and salvage value; reputation/relationship/social memory state; trust, fear, respect, favor, debt, obligation, grudge, kinship, betrayal, reconciliation, and inherited memory; information-state; truth-state, knowledge-state, rumor, secrecy, propaganda, records, archives, intelligence, surveillance, map knowledge, false attribution, and suppressed knowledge; source-local world-system conversion boundaries; runtime record depth, register links, unresolved pressure queues, visibility grouping, promotion/demotion/retirement, and owner handoff states.

## What D10 does not own

| Not owned by D10 | Owner |
|---|---|
| Power pools, fuel mechanics, charges, reservoirs, overdraw, power instability | D03 |
| Advancement gates, proof, breakthroughs, transformations, tier progression | D04 |
| Skill methods, crafting procedure, research procedure, investigation methods, social technique use | D05 |
| Routes, Techniques, Principles, Feature Ledgers, domain powers, oath mechanics | D06 |
| Harm, injury, curse effects, corruption injury, backlash, death/disaster mechanics | D07 |
| Actor body-state, personhood substrate, companion substrate, AI continuity, spirit state, clone state | D08 |
| Object-state, relic object-side records, platform object-side records, cyberware object records, salvage objects | D09 |
| Live-play narration, scene presentation, dialogue, clue delivery, GM behavior | D11 / later play adapter |
| Full economy simulator, legal simulator, diplomacy simulator, faction AI, map simulator | Later runtime/backend doctrine |
| Donor world systems as canon | Source-local / canon promotion |

## Embedded safeguards

This pack embeds these safeguards: D10 must not become a full simulator too early; D10 must not become prose-only lore; minor details must not overload the register; hidden consequences must not disappear; donor world systems must not leak into canon; D10 must not absorb D03–D09 mechanics; consequence persistence must remain explicit; reputation must not collapse into one score; economy must not collapse into price; law must not collapse into legal/illegal; territory must not become map simulation; information-state must not become clue procedure.

## Corpus-scale rule

Every donor world-facing construct must receive a lawful outcome: direct D10 mapping, normalized D10 register mapping, source-local retained system, quarantined construct pending later doctrine, or escalated doctrine problem. Donor world systems are decomposed by function before conversion. A donor label such as kingdom, faction clock, settlement score, law level, heat, market rating, influence, hex, clue web, or domain turn does not become Astra doctrine by label alone.


---

<!-- FILE: D10-00_layered_world_state_register_architecture.md -->

# D10-00 Layered World-State Register Architecture

## Purpose

This file establishes D10’s opening architecture. It defines world-state as persistent consequence-bearing state rather than narration, lore flavor, faction AI, economy simulation, legal simulation, map simulation, or investigation procedure.

## Core rule

D10 owns persistent world-facing state: who knows what, who controls what, who claims what, who owes what, who hates or trusts whom, what laws apply, what resources are scarce, what territories are changed, what factions are responding, and what consequences remain unresolved.

D10 does not own live-play narration, final economy math, combat consequences, actor substrate, object substrate, route powers, Power Economy behavior, exploration procedure, clue procedure, faction AI, or legal procedure.

## Layered registers

| Register | Purpose |
|---|---|
| World-State / Event / Consequence | Facts, events, persistent deltas, timeline, consequence persistence. |
| Territory / Location | Places, routes, hazards, control, claims, discovery, altered zones, strategic terrain. |
| Faction / Institution | Factions, institutions, ranks, goals, claims, conflicts, assets, memory, subfactions. |
| Law / Authority | Jurisdiction, ownership, custody, rights, legitimacy, restrictions, enforcement pressure. |
| Economy / Scarcity | Scarcity signals, strategic resources, market access, black markets, requisition pressure. |
| Reputation / Relationship | Trust, fear, respect, favor, debt, grudge, kinship, betrayal, reconciliation, social memory. |
| Information-State | Truth, belief, secrets, rumors, propaganda, records, archives, intelligence, map knowledge. |
| Source-local World-System Conversion | Donor world systems, lawful outcomes, retained local rules, prohibited generalization. |
| Runtime / Register Links | Record depth, visibility, unresolved pressure, links, handoffs, promotion/retirement. |

Registers are separate but linked. D10 should avoid megarecords by placing state in the correct register and linking related records.

## D10 receives deltas

D10 receives world-facing deltas from D03–D09:

| Source | D10 intake examples |
|---|---|
| D03 | fuel shortage, reactor crisis, reservoir rupture, energy scarcity, overdraw disaster. |
| D04 | breakthrough recognition, failed transformation scandal, proof event, tier status change. |
| D05 | research discovery, public professional success/failure, institutional knowledge, clue acquisition result. |
| D06 | forbidden Technique revealed, Principle violation, oath consequence, domain-altering act. |
| D07 | death, injury memory, corruption outbreak, plague, disaster, curse spread, collateral damage. |
| D08 | personhood dispute, AI emergence, companion death, clone legitimacy, form-state exposure. |
| D09 | relic theft, platform destruction, cyberware illegality, strategic material discovery, salvage dispute. |

D10 records the world-facing state generated by these deltas; it does not absorb their mechanics.

## Relational engine pressure

The adversarial/kinship model enters D10 as structured state, not live AI. D10 may record grudge, favor, trust, fear, respect, kinship, debt, betrayal, reconciliation, and inherited social memory. It does not choose encounter timing, generate dialogue, or simulate faction psychology turn-by-turn.

## Source-local restraint

D10 must not import donor world systems as canon by default. Donor kingdom turns, faction clocks, heat/wanted tracks, reputation ranks, law levels, market ratings, settlement stat blocks, rumor tables, hex procedures, domain actions, travel rules, clue webs, and economy tables remain source-local unless deliberately normalized and canon-promoted.

## Acceptance criteria

A D10 ruling is valid when it identifies the correct D10 register or source-local boundary; separates world-facing state from owner mechanics; records scope, visibility, persistence, and resolution when consequence matters; links records instead of creating megarecords; preserves hidden/public/information-state distinctions; blocks donor world-system leakage; and escalates missing frameworks instead of inventing filler.


---

<!-- FILE: D10-01_world_state_event_consequence_persistence.md -->

# D10-01 World-State Register, Event Ledger, and Consequence Persistence

## Purpose

This file defines how Astra records that something happened, what changed because of it, who knows, how long it persists, whether it can decay or resolve, and when it must remain historically retained.

## Core rule

D10 records world-facing facts and consequences created by actions, events, systems, actors, objects, routes, harm, resources, factions, and source-local constructs. An event is not automatically a consequence. A consequence is not automatically public. A consequence is not automatically permanent. D10 must record scope, visibility, affected parties, persistence state, resolution state, and historical retention.

## World-state fact

A world-state fact is a persistent assertion about the world that may be true, false, disputed, hidden, outdated, partial, or source-local.

Examples include a destroyed gate, a relic claim, an unstable reactor, a corruption zone, an AI personhood petition, a broken treaty, or a vanished monster-core shipment.

A fact may be hidden, public, disputed, wrong, or historically retained.

## Event record

An event record captures that something happened. It should include event reference, label, source owner file, trigger, timeline entry, location, participating actors, affected objects/factions/territories, immediate outcome, consequence candidates, visibility state, and validation state.

An event record by itself is not enough. It must either produce consequences, remain as historical record, or be retired if non-consequential.

## Consequence record

A consequence record captures what changed because an event happened. It should include consequence reference, parent event, consequence type, affected register, affected entity or group, scope, visibility, severity, persistence state, decay/expiration, resolution conditions, owner-file references, source-local boundary, and historical retention requirement.

## Consequence types

| Consequence type | Examples |
|---|---|
| Territory | border shift, damaged settlement, corruption zone, closed route. |
| Faction | hostility, alliance shift, sanction, debt, war footing, internal split. |
| Legal | warrant, restricted status, ownership dispute, inheritance claim. |
| Reputation | trust gain/loss, fear, betrayal memory, local gratitude. |
| Relationship | bond, grudge, favor, debt, kinship, rivalry, reconciliation. |
| Economy/scarcity | shortage, embargo, strategic resource discovery, price-pressure signal. |
| Public knowledge | rumor, false report, concealed truth, propaganda. |
| Object | relic claim, theft report, platform loss, illegal implant discovery. |
| Actor/personhood | citizenship dispute, AI recognition, clone legitimacy. |
| Source-local | retained donor/campaign world-state effect. |

## Timeline entry

D10 supports precise timestamp, relative sequence, session marker, age/era marker, source-local chronology, unknown/disputed timing, recurring events, future scheduled consequence, and unresolved pending consequence. D10 does not need a full calendar system now.

## Promotion from event to consequence

An event promotes to consequence when it changes location, faction, law, ownership, economy, relationship, reputation, public knowledge, or resource state; creates future pressure; affects socially recognized actor or object state; creates rumor, secrecy, propaganda, or misinformation; creates debt, favor, grudge, kinship, obligation, warrant, sanction, or claim; creates territory, hazard, corruption, or route change; involves relics, artifacts, platforms, strategic materials, intelligent objects, or actor-remains; affects source-local systems that must persist; or may plausibly matter later at corpus scale.

## Scope and visibility

Scope may be personal, party/group, local, settlement, regional, factional, cross-factional, world-scale, cosmic/multiversal, or source-local. Scope is not severity.

Visibility may be public, known to faction, known to actor, witnessed, hidden, secret, misreported, rumored, disputed, forgotten, suppressed, or source-local. Reality and knowledge must remain separate.

## Persistence states

Persistence states include immediate, short-term, ongoing, decaying, conditional, permanent, historical, and source-local. D10 must not make every consequence permanent, and must not erase important history because active pressure ends.

## Resolution, decay, expiration, retirement

A consequence may resolve when active pressure is addressed, decay through time or lack of reinforcement, expire through condition/deadline, retire when no longer active, or remain historical when contradiction risk or canon value remains.

Historical retention is required for faction history, law/ownership, personhood recognition, relationship history, relic/artifact history, territory history, source-local continuity, advancement proof, route history, major disaster memory, public myth, or campaign canon.

## Hidden consequences and delayed revelation

D10 supports consequences that are true but not visible: secret faction marks, hidden corruption, delayed favor returns, concealed humiliation, quiet AI copying, or late-discovered relic theft. D10 records state. D11/later runtime decides presentation.

## Record doctrine shape

```yaml
d10_event_consequence_record:
  event_ref: string
  event_label: string
  source_owner: [D03, D04, D05, D06, D07, D08, D09, D10, source_local]
  timeline_entry:
    timestamp: string
    sequence_marker: string
    source_local_chronology: string
  event_context:
    location_refs: []
    actor_refs: []
    faction_refs: []
    object_refs: []
    territory_refs: []
    source_local_refs: []
  immediate_outcome: string
  consequence_records:
    - consequence_ref: string
      consequence_type: string
      affected_registers: []
      affected_refs: []
      scope: string
      visibility: string
      severity: string
      persistence_state: string
      decay_or_expiration: string
      resolution_conditions: []
      historical_retention_required: boolean
      owner_handoffs: []
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [active, pending, resolved, decayed, expired, retired, historical, source_local, escalated]
```

## Acceptance criteria

An event/consequence record is valid when it distinguishes fact, event, consequence, and timeline; promotes events only when future-facing pressure exists; records scope, visibility, severity, persistence, and resolution; supports hidden and false public consequences; preserves owner handoffs; and assigns lawful outcome for source-local constructs.


---

<!-- FILE: D10-02_territory_location_hazard_control_environment_register.md -->

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


---

<!-- FILE: D10-03_faction_institution_rank_claim_goal_conflict_register.md -->

# D10-03 Faction, Institution, Rank, Claim, Goal, and Conflict Register

## Purpose

This file defines factions as persistent world-state actors without turning them into full runtime AIs, diplomacy simulators, encounter engines, or live-play personalities.

## Core rule

D10 records persistent state about factions and institutions: who they are, what authority they claim, what they control, what they want, what they remember, what relationships they hold, what debts or sanctions exist, and what unresolved conflicts remain. D10 does not decide how faction leaders speak in scenes, how diplomacy is narrated, or how faction AI acts turn-by-turn.

## Faction vs. institution

A faction is an organized actor-group with identity, goals, membership, memory, claims, and capacity to create world-facing consequences. An institution is a structured organization with recognized authority, procedure, office, jurisdiction, or social function.

A faction may contain institutions. An institution may operate as faction. A hidden faction may infiltrate an institution.

## Faction types

| Type | Examples |
|---|---|
| State / polity | kingdom, republic, empire, city-state, planetary government. |
| House / lineage | noble house, clan, bloodline, family office. |
| Guild / profession | merchant guild, adventurer guild, artificer guild, healer order. |
| Sect / school | cultivation sect, martial school, mystical academy, doctrine order. |
| Corporation | megacorp, trade company, mining charter, biotech firm. |
| Military | army, navy, knight order, warband, fleet command. |
| Religious / sacred | church, temple, cult, shrine network, oracle order. |
| Criminal / covert | syndicate, smuggler ring, spy cell, conspiracy. |
| Tribe / people | tribe, nomad band, kin-group, diaspora authority. |
| Crew / company | ship crew, mercenary company, expedition, adventuring company. |
| Machine / AI collective | machine network, AI polity, distributed intelligence institution. |
| Hidden faction | front organization, conspiracy, infiltrator cell. |
| Source-local | Donor/campaign faction model. |

## Faction record fields

A faction record should include faction reference, name, faction type, public identity, hidden identity, parent faction, subfactions, leadership, ranks/offices, membership rules, authority claims, controlled territories/locations/objects/resources, goals, active conflicts, alliances/treaties, debts/obligations, sanctions/warrants, reputation/relationship state, public/hidden knowledge, and source-local boundary.

## Subfactions and internal splits

D10 supports loyalists, reformists, extremists, splinters, hidden cells, regional branches, rival branches, ideological wings, noble lines, military wings, research wings, and source-local subfactions.

Internal states include stable, tense, factionalized, splitting, civil conflict, purge, hidden infiltration, leadership crisis, and source-local.

D10 records internal split state; it does not simulate all internal politics.

## Rank, office, membership, and authority

| Concept | Meaning |
|---|---|
| Membership | Actor belongs to faction. |
| Rank | Actor’s standing within hierarchy. |
| Office | Actor holds specific role or position. |
| Authority | Actor can issue orders, requisition assets, judge law, grant access, or represent faction. |
| Recognition | Faction accepts actor’s status publicly or privately. |
| Obligation | Duty, service, payment, secrecy, loyalty, or compliance owed. |
| Expulsion | Actor removed or disowned. |
| Source-local status | Donor/campaign membership/rank rule. |

Rank does not always equal authority.

## Claims

D10 tracks faction claims over territory, locations, objects, relics, platforms, strategic resources, actor custody, personhood jurisdiction, legal authority, inheritance, sacred right, route/domain authority, and source-local constructs.

Claim states include asserted, recognized, disputed, secret, enforced, symbolic, legal, sacred/taboo, conquest, broken, and source-local.

Claims are separate from effective control.

## Goals and agendas

Faction goals are persistent pressure, not full AI plans. Goal types include territorial expansion, resource acquisition, relic recovery, law enforcement, revenge, containment, secrecy, recruitment, conversion, research, profit, survival, purification, corruption spread, political legitimacy, treaty enforcement, debt collection, and source-local objective.

Goal states include dormant, active, opportunistic, blocked, escalating, resolved, failed, secret, and source-local.

## Resources and assets

D10 tracks faction-controlled assets as world-state: territory, settlement, platform, fleet, army, relic, strategic material, production site, market access, legal authority, social legitimacy, skilled labor, archives, intelligence network, monster-core supply, cyberware clinic, spirit spring, and source-local resource.

D09 owns object records. D10 owns control/access/scarcity/faction pressure.

## Faction relationships

Relationship states include allied, friendly, neutral, suspicious, rival, hostile, at war, treaty-bound, tributary/patron, sanctioned, infiltrated, secret relation, and source-local.

Public relationship and hidden relationship may differ.

## Treaties, debts, obligations, sanctions

D10 tracks alliances, non-aggression pacts, trade pacts, salvage rights, relic custody agreements, prisoner exchanges, debts, favors, oaths, taboos, sanctions, embargoes, warrants, bounties, bans, blockades, and source-local agreements.

Each should record parties, terms, scope, visibility, enforcement authority, breach condition, consequence, persistence, and source-local boundary.

## Faction memory

Faction memory records events and interpretations: aid, betrayal, relic theft, returned heirloom, oath breach, public humiliation, strategic loss, AI recognition, forbidden Technique exposure, settlement saved/abandoned, or source-local reputation event.

Faction memory includes emotional/political valence, intensity, decay, retention, and misinformation state. It is not live-play dialogue.

## Adversarial / kinship pressure

D10 records faction-readable relational axes: valence, intensity, trust, fear, respect, debt/favor, grudge, kinship/solidarity, betrayal, reconciliation, and source-local. This can apply to faction-to-faction, faction-to-actor, faction-to-party, and faction-to-object-symbol relations.

## Hidden factions and covert control

D10 supports unknown existence, rumored existence, public front, infiltrating institution, puppet controller, false-flag actor, masked leadership, suppressed record, and source-local secrecy.

D10 separates actual control, public belief, evidence, and hidden influence.

## Source-local faction systems

Donor reputation ranks, favor points, faction clocks, influence scores, kingdom factions, domain actions, settlement loyalty, guild standing, cult secrecy, law levels, faction turns, war moves, diplomacy tracks, patron systems, and source-local faction resources normalize by function or remain source-local.

## Record doctrine shape

```yaml
d10_faction_state_record:
  faction_ref: string
  name_or_label: string
  faction_type: string
  public_identity: string
  hidden_identity: string
  structure:
    parent_faction_refs: []
    subfaction_refs: []
    leadership_refs: []
    rank_office_refs: []
    membership_rules: []
    internal_state: string
  authority:
    jurisdiction_refs: []
    claim_refs: []
    law_zone_refs: []
    recognized_authority: string
    contested_authority: string
  controlled_assets:
    territory_refs: []
    location_refs: []
    object_refs: []
    platform_refs: []
    resource_site_refs: []
    strategic_material_refs: []
  goals:
    active_goal_refs: []
    dormant_goal_refs: []
    secret_goal_refs: []
    blocked_goal_refs: []
  relations:
    faction_relation_refs: []
    actor_relation_refs: []
    party_relation_refs: []
    object_symbol_relation_refs: []
  agreements_pressures:
    treaty_refs: []
    debt_refs: []
    obligation_refs: []
    sanction_refs: []
    warrant_bounty_refs: []
  memory:
    remembered_event_refs: []
    interpretation_notes: []
    valence_state: string
    intensity_state: string
    decay_or_retention: string
  knowledge_visibility:
    public_knowledge_state: string
    hidden_knowledge_state: string
    rumor_refs: []
    suppressed_record_refs: []
  source_local_boundary:
    retained_rules: []
    prohibited_generalizations: []
    promotion_requirements: []
  owner_handoffs:
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    source_local: []
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [active, hidden, dissolved, split, merged, source_local, escalated]
```

## Acceptance criteria

A faction record is valid when it distinguishes faction/institution/subfaction; separates rank, office, membership, authority, recognition, obligation; separates claim from control; records goals as pressure, not AI plans; records faction memory without becoming live-play behavior; supports hidden factions; and preserves source-local boundaries.


---

<!-- FILE: D10-04_law_ownership_custody_rights_legitimacy_authority_register.md -->

# D10-04 Law, Ownership, Custody, Rights, Legitimacy, and Authority Register

## Purpose

This file defines how Astra tracks law-facing consequence without becoming a legal simulator, courtroom engine, enforcement AI, market simulator, or punishment mechanic.

## Core rule

D10 records persistent legal, ownership, custody, rights, legitimacy, and authority state. It records who claims what, who is recognized, who is restricted, what is legal or illegal, what authority applies, what enforcement pressure exists, and what disputes remain unresolved. It does not simulate full legal proceedings or define final economy.

## Jurisdiction

A jurisdiction is a law-facing authority zone or authority relationship. It may belong to state, city, sect, guild, corporation, temple, military command, ship captaincy, station authority, noble house, tribal council, AI collective, hidden faction, or source-local authority.

Jurisdiction fields include authority holder, territory/location scope, actor scope, object scope, law-zone rules, recognition status, contested status, enforcement capacity, and source-local boundary.

Jurisdiction is not physical control.

## Legal relation states

| State | Meaning |
|---|---|
| Ownership | Recognized claim over object, place, resource, platform, asset, or right. |
| Possession | Physical holding or practical control. |
| Custody | Temporary legal, sacred, institutional, or protective responsibility. |
| Use Right | Permission to use something without owning it. |
| Access Right | Permission to enter, inspect, dock, cross, operate, or approach. |
| Stewardship | Duty-bound holding for faction, office, lineage, spirit, deity, public, or heir. |
| Loan | Temporary use under terms. |
| Issuance | Faction/institution grants object or authority for role. |
| Requisition | Authorized acquisition through rank, office, emergency, or institutional demand. |
| Seizure | Authority or force takes possession. |
| Theft | Possession violates recognized ownership/custody. |
| Salvage Claim | Claim from recovery from wreck, ruin, battlefield, corpse, abandoned site, source-local context. |
| Inheritance | Claim based on lineage, office, will, oath, tradition, source-local rule. |
| Sacred Claim | Claim based on taboo, religion, metaphysical authority, ritual office, ancestor, or oath. |
| Source-local | Donor/campaign legal relation. |

Ownership, possession, custody, and use rights must remain distinct.

## Legitimacy and recognition

Legal status, legitimacy, and recognition are separate. States include legal, illegal, tolerated, contested, illegitimate, legitimate, sacredly legitimate, socially legitimate, faction-recognized, publicly recognized, secretly recognized, and source-local.

This matters for rulers, heirs, relic bearers, AI citizens, undead survivors, clone successors, spirit vessels, ship captains, sect disciples, and faction officers.

## Restricted objects, forms, and statuses

D10 tracks restrictions without owning object or actor mechanics. Restrictions may apply to weapons, armor, relics, artifacts, strategic materials, monster cores, catalysts, cyberware, biotech, grafts, living gear, AI cores, spirit vessels, necromantic objects, cursed items, platforms, starships, drones, military gear, undead forms, transformed states, clone bodies, forbidden Techniques, and source-local contraband.

D09 owns object-state. D08 owns actor/body/personhood. D06 owns Techniques. D10 owns law, license, taboo, and enforcement pressure.

## Contraband and black-market status

States include legal, licensed, restricted, contraband, taboo, black-market, tolerated, protected, confiscatable, destroy-on-sight, and source-local. Black-market status is not economy math. It is legal and access pressure.

## Enforcement pressure

Enforcement records may include warrant, bounty, arrest order, kill order, exile, banishment, interdiction, seizure order, customs hold, docking denial, travel ban, restricted trade, embargo, sanction, quarantine order, religious condemnation, military pursuit, and source-local enforcement clock.

Each record should include authority, target, scope, visibility, basis, severity, capacity, expiration/decay, resolution, and source-local boundary. D10 does not run enforcement AI.

## Personhood recognition and rights

D10 tracks legal/social recognition while D08 owns actor substrate.

Subjects may include AI, spirit, undead, clone, construct, awakened animal, symbiote, living ship, uploaded mind, summoned being, bound entity, transformed actor, split self, and source-local being.

Recognition states include recognized person, non-person property, protected non-person, ward/dependent, contested personhood, conditional personhood, secret personhood, illegal existence, sacred status, and source-local.

D08 owns whether the subject has actor/personhood substrate. D10 owns whether society/law recognizes it.

## Custody over actors and actor-adjacent entities

Custody targets may include prisoner, ward, child/heir, bound spirit, summoned being, AI core, clone body, undead actor, companion creature, symbiote, construct, and source-local actor.

Custody types include legal custody, protective custody, sacred custody, faction custody, medical custody, military custody, contractual custody, enslavement claim, guardianship, unlawful detention, and source-local custody.

## Platform registration and travel authority

D10 tracks ship registration, transponder identity, docking rights, customs status, cargo inspection, military restriction, lane permission, platform ownership, fleet command status, salvage title, piracy designation, quarantine flag, AI captain recognition, and source-local vehicle law.

D09 owns platform object-state. D10 owns registry/law/permission/enforcement.

## Salvage rights, inheritance, requisition

Salvage law applies to abandoned property, battlefield salvage, wreck salvage, corpse salvage, monster-part harvesting, relic recovery, sacred remains, AI core recovery, ship salvage title, state-seized salvage, forbidden salvage, and source-local salvage.

D10 supports inheritance of title, office, territory, faction rank, relic, platform, estate, debt, obligation, curse, sacred duty, AI custody, and source-local inheritance.

D10 tracks who can requisition issued assets and under what authority. D09 records issued object-state. D10 records authority, terms, debt, return obligation, monitoring, and legal/faction consequence.

## Source-local law systems

Donor law levels, wanted ratings, bounty systems, legal codes, ownership models, salvage law, starship registry, cyberware licensing, contraband tables, reputation-based access, noble legitimacy, inheritance law, sanctuary laws, domain edicts, and source-local courts normalize by function or remain source-local.

## Record doctrine shape

```yaml
d10_law_authority_state_record:
  law_record_ref: string
  record_type: string
  authority_refs: []
  jurisdiction_scope:
    territory_refs: []
    location_refs: []
    faction_refs: []
    actor_refs: []
    object_refs: []
    platform_refs: []
    source_local_refs: []
  legal_relation:
    owner_refs: []
    possessor_refs: []
    custodian_refs: []
    claimant_refs: []
    recognized_user_refs: []
    disputed_party_refs: []
  legitimacy_state: string
  restriction_state: string
  enforcement_profile:
    enforcement_type: string
    severity: string
    visibility: string
    enforcement_capacity: string
    expiration_or_decay: string
    resolution_conditions: []
  personhood_rights_profile:
    subject_refs: []
    recognition_state: string
    rights_notes: string
  requisition_profile:
    issued_asset_refs: []
    authority_basis: []
    return_terms: []
    debt_or_obligation_refs: []
    monitoring_terms: []
  source_local_boundary:
    retained_rules: []
    prohibited_generalizations: []
    promotion_requirements: []
  owner_handoffs:
    D06: []
    D07: []
    D08: []
    D09: []
    source_local: []
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [active, disputed, resolved, expired, suppressed, source_local, escalated]
```

## Acceptance criteria

A law/authority record is valid when it separates jurisdiction from control; separates ownership, possession, custody, use, access, requisition, salvage, inheritance, sacred claim; separates legal status, legitimacy, and recognition; supports personhood recognition without taking over D08; treats enforcement as pressure, not AI; and blocks donor law levels/wanted tracks from default import.


---

<!-- FILE: D10-05_economy_scarcity_strategic_resources_market_requisition_register.md -->

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


---

<!-- FILE: D10-06_reputation_relationship_social_memory_register.md -->

# D10-06 Reputation, Relationship, Favor, Debt, Grudge, Kinship, Betrayal, and Social Memory Register

## Purpose

This file defines relational world-state. It absorbs adversarial and kinship pressure as structured state without becoming live-play AI, dialogue behavior, romance system, or social encounter mechanics.

## Core rule

D10 records persistent relational memory: who remembers what, how they interpret it, how strongly it matters, whether it is public or hidden, whether it decays, what obligations or grudges exist, and what relationship state may influence future access, faction response, law, social standing, or narrative consequence. D10 does not decide live dialogue or simulate all social behavior.

## Reputation vs relationship

A reputation is a general belief or social standing held by an actor, faction, institution, community, public, or source-local audience. A relationship is a specific persistent connection between entities.

Reputation may exist without direct relationship. Relationship may be private and unknown to public reputation.

## Subject and holder

The subject is the actor, party, faction, object-symbol, location, lineage, route, form-state, or event being judged. The holder is the actor, faction, community, institution, public, hidden faction, family, crew, or source-local system holding the memory or opinion.

The same subject can have different reputations with different holders.

## Relationship axes

D10 uses multiple axes rather than one score: valence, intensity, trust, fear, respect, affection/kinship, obligation, grudge, rivalry, resentment, loyalty, suspicion, and source-local axis.

“High respect, high fear, low trust” is different from simple hostility.

## Summary relational states

States may include unknown, recognized, friendly, trusted, allied, protected, patron/client, kin/oath-bonded, indebted, respected rival, suspicious, resentful, betrayed, grudge-bearing, feared, hostile, vendetta, reconciled, publicly hostile/privately allied, and source-local.

## Social memory record

A social memory record includes memory reference, remembered event, subject, holder, interpretation, valence, intensity, visibility, truth status, decay/permanence, obligations, grudges, rumors, source-local boundary.

Interpretation matters. The same event can produce gratitude in one community, humiliation in a rival, and useful destabilization in a hidden faction.

## Favor, debt, obligation, reciprocity

D10 distinguishes favor, debt, life debt, oath debt, contract debt, patronage, protection, reciprocal expectation, unpaid debt, and source-local favor.

Debt can be positive or coercive. Favor can become resentment if ignored. Patronage can become support, leverage, hierarchy, or control.

## Grudge, rivalry, revenge, vendetta

Grudge sources include harm, humiliation, betrayal, theft, relic desecration, oath breach, killing kin, public insult, faction defeat, loss of territory, corruption spread, sabotage, abandonment, and source-local trigger.

States include minor grievance, active grudge, rivalry, revenge intent, vendetta, inherited grudge, dormant grudge, reconciled grudge, and source-local.

D10 records adversarial memory; it does not choose ambushes.

## Kinship, loyalty, reconciliation

Kinship sources include rescue, shared danger, sacrifice, oath, adoption, crew membership, lineage, faction initiation, spiritual bond, companion bond, patronage, mutual secrecy, restored honor, and source-local bond.

States include affinity, gratitude, shared trial, oath-bond, crew-bond, family/lineage bond, companion bond, patronage bond, protective loyalty, reconciled bond, and source-local.

Reconciliation does not erase history.

## Betrayal, jealousy, resentment

Damage states include strained, resentful, jealous, distrustful, betrayed, alienated, hostile turn, recoverable, irreparable, and source-local. Triggers include broken promise, unpaid debt, favoritism, abandonment, public humiliation, revealed secret, collateral harm, conflicting obligation, taboo violation, object theft, or unauthorized restricted form/power use.

## Public/private/hidden/false reputation

D10 distinguishes public reputation, private reputation, hidden relation, secret alliance, false reputation, rumored reputation, misattributed reputation, propaganda-shaped reputation, suppressed memory, disputed reputation, and source-local.

A false reputation can create real consequences.

## Scope, persistence, and inheritance

Scope may be personal, household/family, crew/party, community, institution, faction, settlement, region, cross-factional, public/world-scale, or source-local.

Persistence modes include immediate, short-term, decaying, reinforced, escalating, dormant, ongoing, permanent, historical, and source-local.

Relationships can pass through family, lineage, house, clan, crew, guild, sect, faction, companion group, patron-client network, religious order, AI collective, or source-local institution. D10 records inherited memory but does not simulate all individual beliefs.

## Source-local reputation systems

Donor reputation ranks, faction favor points, influence scores, bond tracks, loyalty tracks, relationship clocks, nemesis systems, patron favor, honor, infamy, heat/wanted levels, attitude categories, social standing, kingdom loyalty, romance/companion affinity normalize by function or remain source-local.

## Record doctrine shape

```yaml
d10_reputation_relationship_state_record:
  relation_ref: string
  record_type: string
  subject_refs:
    actor_refs: []
    party_refs: []
    faction_refs: []
    institution_refs: []
    object_symbol_refs: []
    place_refs: []
    source_local_refs: []
  holder_refs:
    actor_refs: []
    faction_refs: []
    institution_refs: []
    community_refs: []
    public_refs: []
    hidden_faction_refs: []
    source_local_refs: []
  relationship_axes:
    valence: string
    intensity: string
    trust: string
    fear: string
    respect: string
    affection_kinship: string
    obligation: string
    grudge: string
    rivalry: string
    resentment: string
    loyalty: string
    suspicion: string
  summary_state: string
  memory_profile:
    remembered_event_refs: []
    interpretation: string
    truth_state: string
    visibility: string
  obligation_profile:
    favor_refs: []
    debt_refs: []
    oath_refs: []
    patronage_refs: []
    protection_refs: []
    unpaid_obligation_refs: []
  damage_profile:
    betrayal_refs: []
    resentment_refs: []
    jealousy_refs: []
    alienation_refs: []
    reconciliation_refs: []
  inheritance_profile:
    inheritance_paths: []
    inheriting_group_refs: []
    inherited_from_refs: []
  persistence:
    mode: string
    decay_conditions: []
    reinforcement_conditions: []
    resolution_conditions: []
    historical_retention_required: boolean
  source_local_boundary:
    retained_rules: []
    prohibited_generalizations: []
    promotion_requirements: []
  owner_handoffs:
    D07: []
    D08: []
    D09: []
    source_local: []
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [active, hidden, decayed, resolved, historical, source_local, escalated]
```

## Acceptance criteria

A relational record is valid when it separates reputation from relationship; uses multiple axes rather than one score; distinguishes favor, debt, obligation, patronage, protection; supports grudge/vendetta without combat AI; supports kinship/reconciliation without narration behavior; separates public/private/hidden/false/rumored states; supports inherited memory; and blocks donor reputation systems from default import.


---

<!-- FILE: D10-07_information_state_public_knowledge_rumor_secrecy_records_register.md -->

# D10-07 Public Knowledge, Rumor, Secrecy, Records, Intelligence, and Information-State Register

## Purpose

This file defines information-state: who knows what, who believes what, what is false, what is hidden, what is suppressed, what is recorded, what is rumored, and what can later be revealed.

## Core rule

D10 records information-state: what is true, what is believed, who knows it, how reliable it is, how visible it is, where it is recorded, whether it is spreading, whether it is suppressed, and what future consequence depends on it. D10 does not decide how the player discovers it or how the narrator presents it.

## Truth-state vs. knowledge-state

Truth-state records whether information corresponds to underlying world-state. Knowledge-state records who knows, believes, suspects, records, hides, distorts, or disputes it.

Truth states include true, false, partial, outdated, misleading, unknown, disputed, and source-local.

Knowledge states include public knowledge, private knowledge, faction knowledge, actor knowledge, witness knowledge, secret, hidden truth, rumor, misinformation, propaganda, suppressed, forgotten, archived, and source-local.

A fact can be true and hidden. A rumor can be false and public. A record can be outdated.

## Information subjects

Information may concern actor, faction, location, territory, object, relic, platform, law, ownership, resource, route, Technique, Principle, corruption zone, event, relationship, personhood status, or source-local construct.

Owner substrates remain outside D10.

## Holder and audience

Holder types include actor, party/crew, faction, subfaction, institution, community, public audience, hidden faction, archive, AI memory, spirit memory, legal record, map, rumor network, and source-local holder.

Audience scopes include personal, household, crew, community, institution, faction, settlement, regional, cross-factional, world-scale, hidden network, and source-local.

## Records and archives

Record/archive types include public record, faction archive, secret archive, personal record, legal record, object-bound record, map record, rumor record, suppressed record, and source-local record.

D09 owns record objects when relevant. D10 owns information-state.

## Rumor, misinformation, propaganda

Rumor states include emerging, spreading, widespread, fading, replaced, confirmed, disproven, weaponized, and source-local.

Misinformation is false or misleading belief spread without necessarily deliberate intent. Propaganda is deliberate belief-shaping.

Propaganda records include originator, audience, subject, claim, truth-state, channel, intended effect, current reach, counter-claims, and source-local boundary.

## Witness memory and testimony

Witness records track witness actor/group, witnessed event, interpretation, confidence, reliability, bias, fear/coercion, willingness to testify, public/private status, decay/distortion, and source-local rule.

D08 owns actor memory substrate when mechanically relevant. D10 owns social/legal information consequence.

## Intelligence and surveillance

Intelligence sources may include spy report, surveillance record, intercepted message, hacked archive, divination report, scout map, informant claim, faction dossier, sensor log, AI analysis, spirit vision, and source-local intelligence system.

States include raw, verified, unverified, contradictory, compromised, forged, planted, outdated, classified, leaked, and source-local.

D10 records who has it and reliability. D05/later runtime owns collection.

## Discovery and revelation

Discovery states include undiscovered, discovered privately, discovered by faction, publicly revealed, partially revealed, misrevealed, reconcealed, leaked, exposed, and source-local.

Revelation can create reputation shifts, legal action, faction conflict, resource rush, panic, treaty collapse, or reconciliation.

## Decay and persistence

Information may be immediate, short-term, ongoing, decaying, distorted, archived, suppressed, forgotten, mythologized, permanent, historical, or source-local.

Persistence anchors include public record, oath memory, legal record, faction archive, sacred tradition, propaganda campaign, inherited grievance, relic memory, AI archive, immortal witness, and source-local permanence.

## False attribution and disputed accounts

D10 supports wrong credit, wrong blame, framed events, misattributed disasters, false relic theft accusations, suppressed evidence, and competing histories.

Disputed accounts should record claim holders, evidence state, public leaning, suppressed evidence, faction interest, resolution conditions, and historical retention.

## Propagation without full simulation

Propagation states include contained, leaking, circulating, institutionalized, suppressed, countered, saturated, fragmented, and source-local.

D10 tracks spread state and scope; it does not simulate every conversation.

## Source-local information systems

Donor rumor tables, clue webs, revelation lists, secret clocks, library research tracks, faction intelligence ratings, surveillance systems, wanted posters, prophecy records, map discovery rules, knowledge skill categories, mystery scenario nodes, and source-local truth/rumor mechanics normalize by function or remain source-local.

## Record doctrine shape

```yaml
d10_information_state_record:
  information_ref: string
  record_type: string
  subject_refs:
    actor_refs: []
    faction_refs: []
    location_refs: []
    territory_refs: []
    object_refs: []
    platform_refs: []
    route_refs: []
    event_refs: []
    law_refs: []
    resource_refs: []
    source_local_refs: []
  truth_state: string
  knowledge_state: string
  holder_refs:
    actor_refs: []
    faction_refs: []
    institution_refs: []
    community_refs: []
    public_scope_refs: []
    archive_refs: []
    source_local_refs: []
  visibility_scope: string
  reliability_profile:
    confidence: string
    evidence_refs: []
    source_bias: string
    contradiction_refs: []
    verification_state: string
  propagation_state: string
  discovery_state: string
  persistence:
    mode: string
    decay_conditions: []
    persistence_anchors: []
    resolution_conditions: []
    historical_retention_required: boolean
  consequence_links:
    event_refs: []
    reputation_refs: []
    law_refs: []
    faction_refs: []
    territory_refs: []
    economy_refs: []
  source_local_boundary:
    retained_rules: []
    prohibited_generalizations: []
    promotion_requirements: []
  owner_handoffs:
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    source_local: []
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [active, hidden, disputed, disproven, confirmed, suppressed, forgotten, historical, source_local, escalated]
```

## Acceptance criteria

An information-state record is valid when it separates truth-state from knowledge-state; identifies subject, holder, audience, reliability, propagation, discovery, persistence; supports false, rumored, suppressed, archived, and disputed information; routes discovery/research to D05 or later runtime; and blocks donor rumor/clue systems from default import.


---

<!-- FILE: D10-08_source_local_world_system_conversion_boundary_register.md -->

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


---

<!-- FILE: D10-09_runtime_records_ui_register_links_owner_handoffs.md -->

# D10-09 Runtime Records, UI, Register Links, and Owner Handoffs

## Purpose

This file defines how D10 records persistent world-state at the right depth, links register records together, preserves visibility, queues unresolved pressure, retains history, and routes owner handoffs without turning into a cluttered memory dump or full simulator.

## Core rule

D10 records world-facing state only at the depth needed to preserve consequence, contradiction prevention, future pressure, visibility, register linkage, source-local boundaries, and owner-file validation. Minor world details do not automatically become full D10 records.

## Tiered World-State Record and Register-Link Model

Record depth grades:

| Depth grade | Meaning |
|---|---|
| Background Note | Low-consequence setting note; no active mechanical or continuity pressure. |
| Ephemeral State | Temporary state expected to expire quickly. |
| Simple Fact | Persistent fact that may matter but has limited linkage. |
| Tracked Fact | Fact with visibility, owner, scope, or future relevance. |
| Event Record | Something happened and may generate consequence. |
| Consequence Record | Persistent world-facing change or pressure. |
| Register Record | Full D10 register entry. |
| Linked Register Cluster | Multiple D10 records connected by event/consequence. |
| Unresolved Pressure | Active unresolved consequence needing attention/resolution. |
| Historical Record | No longer active but retained for canon/contradiction prevention. |
| Source-local Record | Donor/campaign-local world system retained under boundary. |
| Escalated Record | Current doctrine cannot safely classify or resolve. |

## Durable D10 record thresholds

A durable record is required when a fact/event/consequence changes territory, location, route access, hazard, corruption, law, faction control, resource state, faction memory, debt, grudge, treaty, claim, warrant, obligation, sanction, ownership, custody, legitimacy, personhood recognition, market access, scarcity, strategic-resource control, requisition pressure, supply-chain state, public knowledge, secret knowledge, rumor, propaganda, suppression, map knowledge, archives, relics, artifacts, platforms, strategic materials, actor-remains, intelligent objects, source-local systems, or hidden consequences likely to surface later.

No durable record is required for trivial local chatter, ordinary purchases, momentary travel descriptions, background NPC opinions, minor insults without future pressure, routine legal norms, ordinary market availability, one-scene weather, non-consequential route notes, or flavor-only lore.

## Register families

D10 register families are world-state fact, event/consequence, territory/location, faction/institution, law/authority, economy/scarcity, reputation/relationship, information-state, source-local conversion, and mixed.

## Register links

Link types include caused by, causes, refers to, depends on, contradicts, conceals, reveals, misattributes, claims, controls, restricts, escalates, resolves, and source-local.

A relic theft may link event/consequence, D09 object reference, law/authority, faction, reputation, information-state, economy, and territory records.

## Visibility and UI grouping

Visibility groups include public world-state, party-known state, actor-known state, faction-known state, hidden truth, secret state, rumor/misinformation, source-local state, retired/historical state, and escalated/quarantined state.

Recommended UI groups:
- Active Consequences;
- Unresolved Pressures;
- Territories & Locations;
- Factions & Institutions;
- Law, Claims & Enforcement;
- Economy, Scarcity & Requisition;
- Reputation & Relationships;
- Knowledge, Rumors & Secrets;
- Source-local Systems;
- Historical Records;
- Quarantined / Escalated Records.

## Unresolved pressure queues

D10 accepts unresolved pressure queues for active warrants, bounties, sanctions, grudges, unpaid debts, treaty breaches, corruption zones, hidden infiltrations, strategic shortages, embargoes, black-market demand, personhood disputes, relic claims, salvage rights, and source-local clocks.

Queue fields include pressure reference, linked register records, severity, scope, visibility, active holder/controller, escalation conditions, decay conditions, resolution conditions, historical retention requirement, and source-local boundary.

D10 records pressure. It does not force immediate scenes.

## Promotion and demotion

Promotion triggers include hidden fact becoming public, minor rumor causing faction consequence, petty grudge becoming vendetta, local shortage becoming strategic crisis, object theft becoming legal/faction conflict, local hazard spreading, source-local clock becoming campaign-defining, background faction becoming active, private debt becoming scandal, or law note becoming enforcement pressure.

Demotion triggers include consequence resolving, rumor fading, law restriction expiring, faction conflict cooling, market disruption stabilizing, location returning to normal, record becoming historical, or source-local system retiring.

Demotion must not delete history when contradiction risk remains.

## Record lifecycle

States include active, pending, dormant, escalating, decaying, resolved, expired, retired, historical, quarantined, escalated, and source-local.

Historical retention is required for faction memory, law/ownership, personhood recognition, relationship history, territory history, relic/artifact history, source-local continuity, advancement proof, route history, major harm/disaster memory, public myth, or campaign canon.

## Owner handoff states

Handoff states are none, pending, resolved, blocked, dangerous, source-local, and escalated.

| Trigger | Required owner |
|---|---|
| Resource shortage, fuel, charge, reactor, overdraw, energy scarcity, power disaster | D03 |
| Breakthrough recognition, proof, tier transition, transformation catalyst, advancement scandal | D04 |
| Research, investigation, crafting discovery, professional credibility, clue acquisition | D05 |
| Route taboo, forbidden Technique, domain effect, Principle revelation, oath consequence | D06 |
| Harm, death, corruption, curse, plague, environmental danger, disaster, injury memory | D07 |
| Actor personhood, AI, spirit, clone, undead, companion, form-state, body continuity | D08 |
| Relic, object, platform, cyberware, salvage, strategic material, object ownership | D09 |
| Donor world system retained locally | Source-local |
| Missing doctrine | Escalation |

## Source-local runtime records

Retained donor world systems must have D10 boundary records stating what source-local system exists, where it applies, what it may affect, what D10 outputs it produces, what assumptions cannot generalize, and when it should retire, promote, quarantine, or escalate.

## Record doctrine shape

```yaml
d10_runtime_world_state_record:
  world_state_ref: string
  record_depth:
    - background_note
    - ephemeral_state
    - simple_fact
    - tracked_fact
    - event_record
    - consequence_record
    - register_record
    - linked_register_cluster
    - unresolved_pressure
    - historical_record
    - source_local_record
    - escalated_record
  register_family:
    - world_state_fact
    - event_consequence
    - territory_location
    - faction_institution
    - law_authority
    - economy_scarcity
    - reputation_relationship
    - information_state
    - source_local_conversion
    - mixed
  subject_refs:
    actor_refs: []
    faction_refs: []
    institution_refs: []
    location_refs: []
    territory_refs: []
    object_refs: []
    platform_refs: []
    resource_refs: []
    law_refs: []
    event_refs: []
    source_local_refs: []
  visibility_group: string
  link_profile:
    caused_by_refs: []
    causes_refs: []
    refers_to_refs: []
    depends_on_refs: []
    contradicts_refs: []
    conceals_refs: []
    reveals_refs: []
    misattributes_refs: []
    claims_refs: []
    controls_refs: []
    restricts_refs: []
    escalates_refs: []
    resolves_refs: []
    source_local_links: []
  pressure_profile:
    is_unresolved_pressure: boolean
    severity: string
    scope: string
    escalation_conditions: []
    decay_conditions: []
    resolution_conditions: []
  persistence_state: string
  ui_group: string
  owner_handoffs:
    D03: string
    D04: string
    D05: string
    D06: string
    D07: string
    D08: string
    D09: string
  source_local_boundary:
    retained_rules: []
    allowed_use: []
    prohibited_generalizations: []
    normalized_outputs: []
    promotion_requirements: []
  historical_retention_required: boolean
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [authorized, pending_owner_file, active, resolved, retired, historical, source_local, quarantined, escalated]
```

## Acceptance criteria

A runtime D10 record is valid when it assigns appropriate depth; avoids durable records for minor details; promotes hidden/important consequences when thresholds apply; uses explicit register links; preserves visibility; uses unresolved pressure queues when needed; records D03–D09 handoff states; and supports lifecycle transitions.


---

<!-- FILE: D10-10_integration_checklists_and_ddr_register.md -->

# D10-10 Integration Checklists and DDR Register

## Purpose

This file is the control ledger for the D10 doctrine pack. It consolidates accepted decisions, validates D10 register boundaries, preserves owner handoffs, and lists safeguards to preserve during conversion, canon consolidation, and later runtime design.

## Accepted decision register

### D10-LWSR — Layered World-State Register Architecture

D10 uses Layered World-State Register Architecture; owns persistent world-facing consequence state; separates territory/location, faction/institution, law/ownership, reputation/relation, economy/scarcity, public knowledge/rumor, and event/consequence registers; treats adversarial/kinship pressure as structured relationship-state rather than live-play AI; tracks ownership, custody, theft, requisition, inheritance, restricted possession, sacred claim, black-market status, and strategic-resource control without final economy math; normalizes source-local world systems by function; and quarantines or escalates missing world-state frameworks.

### D10-ECP — World-State Register, Event Ledger, and Consequence Persistence

D10 uses Event-to-Consequence Persistence Model; distinguishes world-state facts, event records, consequence records, and timeline entries; promotes events only when future-facing pressure exists; requires scope, visibility, severity, persistence, resolution, decay/expiration, and historical retention; separates knowledge states; accepts deltas from D03–D09 without taking over mechanics; and normalizes source-local event/world systems by function.

### D10-TLH — Territory, Location, Hazard, Control, and Environmental State Register

D10 uses Territory and Location State Register Model; distinguishes territory and location; separates control, claim, occupation, hidden control, legitimacy, and public belief; tracks access/route state without travel procedure; treats hazards and altered places as persistent place-state; separates discovery/map knowledge states; and normalizes source-local map/domain systems by function.

### D10-FAC — Faction, Institution, Rank, Claim, Goal, and Conflict Register

D10 uses Faction-State Register Model; distinguishes factions and institutions; tracks subfactions and internal splits; separates rank, office, membership, authority, recognition, obligation, and expulsion; separates claims from control; treats faction memory and adversarial/kinship pressure as structured state; and normalizes source-local faction systems by function.

### D10-LAW — Law, Ownership, Custody, Rights, Legitimacy, and Authority Register

D10 uses Law and Authority State Register Model; separates jurisdiction from physical control and public legitimacy; distinguishes ownership, possession, custody, use rights, access rights, stewardship, loan, issuance, requisition, seizure, theft, salvage claim, inheritance, and sacred claim; tracks restricted objects/forms/personhood recognition as law-facing records; treats enforcement pressure without simulation; and normalizes source-local law systems by function.

### D10-ECO — Economy, Scarcity, Strategic Resources, Market Access, and Requisition Pressure Register

D10 uses Economy and Scarcity State Register Model; tracks scarcity as signal rather than price; treats strategic resources broadly; records market access and supply pressure; treats requisition as institutional acquisition; classifies treasure and salvage by pressure type; and normalizes source-local economy systems by function.

### D10-REL — Reputation, Relationship, Favor, Debt, Grudge, Kinship, Betrayal, and Social Memory Register

D10 uses Relational Memory and Reputation State Register Model; distinguishes reputation and relationship; tracks multi-axis relationships; separates favor, debt, obligation, patronage, and protection; supports adversarial states without combat AI; separates visibility states; and normalizes source-local reputation systems by function.

### D10-INFO — Public Knowledge, Rumor, Secrecy, Records, Intelligence, and Information-State Register

D10 uses Information-State Register Model; separates truth-state and knowledge-state; requires subject, holder, audience scope, reliability, propagation, discovery, persistence, and consequence links; distinguishes public/private/faction/actor/witness knowledge, secrets, hidden truths, rumors, misinformation, propaganda, suppressed records, forgotten information, and archives; supports false information as world-state; and normalizes source-local information systems by function.

### D10-SLC — Source-local World-System Conversion and Boundary Register

D10 uses Source-local World-System Conversion and Boundary Model; requires lawful outcome for every donor world-facing construct; decomposes donor world systems before conversion; requires boundary records for retained systems; blocks donor mechanics from becoming Astra defaults; normalizes world-system families by function; and quarantines or escalates missing frameworks.

### D10-RUNTIME — Runtime Records, UI, Register Links, and Owner Handoffs

D10 uses Tiered World-State Record and Register-Link Model; accepts D10 record depth grades and register families; uses explicit links; accepts unresolved pressure queues; supports record promotion, demotion, resolution, expiration, retirement, historical retention, source-local retention, quarantine, and escalation; and requires D03–D09 handoff states when relevant.

## D10 ownership checklist

D10 owns persistent world-facing state, facts, events, consequences, timeline entries, territories, locations, factions, institutions, law, authority, economy-facing scarcity, reputation, relationships, information-state, source-local world-system boundaries, unresolved pressures, record depth, register links, and historical retention.

D10 does not own D03 Power Economy; D04 advancement; D05 methods/procedure; D06 Routes/Techniques/Principles; D07 harm/disaster mechanics; D08 actor/personhood substrate; D09 object-state; D11 live-play narration; later economy/legal/faction/map/full runtime simulation; or donor world systems as canon.

## World-state / event / consequence checklist

Ask: Is this fact, event, consequence, timeline entry, or source-local construct? Is it true, false, partial, hidden, disputed, outdated, or source-local? Who knows it? Who is affected? What scope and visibility apply? Is there persistent consequence? Does it create future-facing pressure? Does it require resolution, decay, expiration, or history? What register links apply? Which owner generated it? What lawful outcome applies?

## Territory / location checklist

Ask: Is this territory, location, route, platform-location, resource site, hazard zone, law zone, source-local place, or mixed? What scale applies? Who controls and claims it? Is legitimacy/public belief different from control? What access/route state applies? What environment/hazard/altered-zone state applies? What discovery/map state applies? What D03/D06/D07/D08/D09 handoffs apply? Does source-local map/hex/domain/travel doctrine apply?

## Faction / institution checklist

Ask: Is this faction, institution, subfaction, hidden faction, source-local faction, or mixed? What type and public/hidden identity apply? What ranks/offices/membership/authority/recognition/obligations apply? What claims and controlled assets exist? What goals/conflicts/treaties/debts/sanctions/warrants exist? What internal split state applies? What faction memory/adversarial/kinship pressure applies? What source-local faction system is retained or normalized?

## Law / authority checklist

Ask: What jurisdiction applies and is it separate from control? What legal relation applies? What legitimacy/recognition state applies? What restriction/contraband/taboo/protected status applies? What enforcement pressure applies? Does personhood recognition/custody apply? Does platform registration, docking, salvage, inheritance, or requisition apply? What D08/D09 handoff is needed? What source-local law system applies?

## Economy / scarcity checklist

Ask: Is this scarcity, strategic resource, market access, supply chain, black market, requisition, treasure, salvage, crafting boundary, exchange mode, or source-local economy? What scarcity signal applies? Is this price, availability, access, faction control, legal restriction, or perceived scarcity? Who controls/claims it? What market/supply/requisition state applies? What treasure/salvage pressure type applies? Is actual scarcity different from perceived scarcity? What D03/D04/D05/D07/D08/D09 handoff applies?

## Reputation / relationship checklist

Ask: Is this reputation, relationship, memory, favor, debt, obligation, grudge, rivalry, kinship, betrayal, reconciliation, rumor reputation, inherited memory, or source-local relation? Who is subject and holder? What axes apply? Is it public, private, hidden, secret, false, rumored, misattributed, propaganda-shaped, suppressed, disputed, or source-local? What remembered event and interpretation apply? What decay, escalation, dormancy, inheritance, or resolution applies?

## Information-state checklist

Ask: Is this fact, hidden truth, secret, rumor, misinformation, propaganda, record, archive, witness memory, intelligence, surveillance, intercepted message, map knowledge, revelation, or source-local information? What truth-state and knowledge-state apply? Who holds it and what audience scope applies? What reliability/verification state applies? What propagation and discovery state applies? What persistence/decay/suppression/archive/history applies? What false attribution or disputed account applies? Does D05 discovery/research handoff apply?

## Source-local world-system conversion checklist

Ask: What is the donor label and system type? Which D10 registers does it touch? What components must be decomposed? What donor assumptions are rejected? What rules are retained source-locally? What normalized outputs are produced? What D03–D09 handoffs are required? What lawful outcome applies?

Required prohibitions: donor reputation ranks, law levels, domain turns, travel rules, market ratings, rumor tables, countdown mechanics, heat tracks, wealth assumptions, settlement stat blocks, corruption mechanics, faction AI clocks, and domain action sequences cannot become Astra defaults by import.

## Runtime / UI / register-link checklist

Ask: What record depth is justified? What register family applies? What visibility/UI group applies? Does it need register links? Does it cause, depend on, contradict, conceal, reveal, misattribute, claim, control, restrict, escalate, or resolve another record? Is it unresolved pressure? What escalation, decay, and resolution conditions apply? Can it demote, retire, or become historical? Does source-local boundary apply? Are owner handoffs recorded? Is the record too heavy or too thin?

## D03–D09 handoff matrix

| Trigger | Required handoff |
|---|---|
| Resource shortage, fuel crisis, charge scarcity, reactor instability, reservoir rupture, overdraw, energy disaster | D03 |
| Breakthrough recognition, proof event, tier transition, transformation catalyst, public advancement scandal | D04 |
| Research discovery, clue acquisition, crafting discovery, professional reputation, institutional knowledge, investigation procedure | D05 |
| Forbidden Technique, route taboo, Principle revelation, domain effect, oath consequence, route-linked public consequence | D06 |
| Death, harm, injury memory, corruption outbreak, curse, plague, disaster, environmental danger, collateral damage | D07 |
| Actor personhood, AI, spirit, clone, undead, companion, transformed actor, body/form-state, actor continuity | D08 |
| Relic, object, platform, cyberware, salvage, strategic material, object ownership, source-local item | D09 |
| Retained donor world system | Source-local boundary |
| Missing world-state framework | Escalation |

## Unresolved pressure checklist

Queue unresolved pressure when warrants, bounties, sanctions, embargoes, enforcement orders, grudges, debts, oaths, vendettas, obligations, hidden infiltrations, secret alliances, false reputations, suppressed records, rumors, corruption zones, hazards, plagues, war fronts, blockades, territory conflicts, strategic shortages, closed markets, black-market demand, requisition debts, supply disruptions, personhood disputes, custody claims, inheritance conflicts, relic claims, platform registration issues, salvage rights, source-local clocks, or expected future events remain active.

## Pre-generation risk queue

Embed these safeguards in every relevant file: D10 must not become full simulator too early; D10 must not become prose-only lore; minor details must not overload the register; hidden consequences must not disappear; donor world systems must not leak into canon; D10 must not absorb D03–D09 mechanics; consequence persistence must remain explicit; reputation must not collapse into one score; economy must not collapse into price; law must not collapse into legal/illegal; territory must not become map simulation; information-state must not become clue procedure.


---

<!-- FILE: D10_pack_manifest.json -->

```json
{
  "pack": "D10 World-State, Faction, Law, Economy, Reputation, Information, and Source-local World-System Architecture",
  "version": "v0.1",
  "generated_date": "2026-06-02",
  "status": "generated",
  "phase": "Astra Ascension native design doctrine",
  "primary_owner": "D10",
  "doctrine_files": [
    {
      "path": "D10-README_manifest.md",
      "purpose": "manifest and scope"
    },
    {
      "path": "D10-00_layered_world_state_register_architecture.md",
      "purpose": "layered world-state register architecture"
    },
    {
      "path": "D10-01_world_state_event_consequence_persistence.md",
      "purpose": "world-state facts, events, consequences, persistence, timelines"
    },
    {
      "path": "D10-02_territory_location_hazard_control_environment_register.md",
      "purpose": "territories, locations, hazards, control, environmental state"
    },
    {
      "path": "D10-03_faction_institution_rank_claim_goal_conflict_register.md",
      "purpose": "factions, institutions, ranks, claims, goals, conflicts"
    },
    {
      "path": "D10-04_law_ownership_custody_rights_legitimacy_authority_register.md",
      "purpose": "law, ownership, custody, rights, legitimacy, authority"
    },
    {
      "path": "D10-05_economy_scarcity_strategic_resources_market_requisition_register.md",
      "purpose": "economy, scarcity, strategic resources, market access, requisition"
    },
    {
      "path": "D10-06_reputation_relationship_social_memory_register.md",
      "purpose": "reputation, relationships, favor, debt, grudge, kinship, social memory"
    },
    {
      "path": "D10-07_information_state_public_knowledge_rumor_secrecy_records_register.md",
      "purpose": "public knowledge, rumor, secrecy, records, intelligence, information-state"
    },
    {
      "path": "D10-08_source_local_world_system_conversion_boundary_register.md",
      "purpose": "source-local world-system conversion and boundaries"
    },
    {
      "path": "D10-09_runtime_records_ui_register_links_owner_handoffs.md",
      "purpose": "runtime records, UI grouping, register links, owner handoffs"
    },
    {
      "path": "D10-10_integration_checklists_and_ddr_register.md",
      "purpose": "integration checklists and DDR register"
    }
  ],
  "core_rule": "D10 records persistent world-facing state and consequences, not the mechanical substrates or runtime procedures that generate them.",
  "register_families": [
    "world_state_fact",
    "event_consequence",
    "territory_location",
    "faction_institution",
    "law_authority",
    "economy_scarcity",
    "reputation_relationship",
    "information_state",
    "source_local_conversion",
    "runtime_register_links"
  ],
  "record_depth_grades": [
    "background_note",
    "ephemeral_state",
    "simple_fact",
    "tracked_fact",
    "event_record",
    "consequence_record",
    "register_record",
    "linked_register_cluster",
    "unresolved_pressure",
    "historical_record",
    "source_local_record",
    "escalated_record"
  ],
  "owner_boundaries": {
    "D10_owns": [
      "persistent world-facing state",
      "world-state facts",
      "event records",
      "consequence records",
      "timeline entries",
      "territory and location state",
      "faction and institution state",
      "law and authority state",
      "economy and scarcity state",
      "reputation and relationship state",
      "information-state",
      "source-local world-system conversion boundaries",
      "runtime record depth",
      "register links",
      "unresolved pressure queues",
      "historical retention"
    ],
    "D10_does_not_own": {
      "D03": "Power Economy, fuel mechanics, charges, reservoirs, overdraw, power instability",
      "D04": "advancement gates, proof, breakthroughs, transformations, tier progression",
      "D05": "skill methods, crafting/research/investigation procedure, social technique use",
      "D06": "Routes, Techniques, Principles, Feature Ledgers, domain powers, oath mechanics",
      "D07": "harm, injury, curses, corruption injury, backlash, death/disaster mechanics",
      "D08": "actor body-state, personhood substrate, companions, AI/spirit/clone continuity",
      "D09": "object-state, relic object-side records, platforms, cyberware, salvage objects",
      "D11": "live-play narration, scene presentation, dialogue, clue delivery, GM behavior"
    }
  },
  "risk_fixes_embedded": [
    "D10 does not become full simulator too early",
    "D10 does not become prose-only lore",
    "minor details do not overload the register",
    "hidden consequences are preserved",
    "donor world systems are blocked from canon leakage",
    "D10 does not absorb D03-D09 mechanics",
    "consequence persistence fields remain explicit",
    "reputation does not collapse into one score",
    "economy does not collapse into price",
    "law does not collapse into legal/illegal",
    "territory does not become map simulation",
    "information-state does not become clue procedure"
  ],
  "lawful_outcomes": [
    "direct_d10_mapping",
    "normalized_d10_register_mapping",
    "source_local_retained",
    "quarantined",
    "escalated"
  ],
  "file_count_excluding_combined_export": 13
}
```

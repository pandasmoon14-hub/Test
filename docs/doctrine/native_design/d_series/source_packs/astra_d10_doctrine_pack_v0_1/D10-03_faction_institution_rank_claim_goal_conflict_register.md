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

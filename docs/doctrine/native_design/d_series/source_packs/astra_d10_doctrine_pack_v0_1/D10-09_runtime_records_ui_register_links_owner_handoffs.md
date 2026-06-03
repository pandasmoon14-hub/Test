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

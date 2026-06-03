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

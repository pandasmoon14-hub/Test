---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-09 Runtime Records, UI, and Owner Handoffs

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

D07 uses tiered harm records: ephemeral, session-relevant, and durable. D07 record families are doctrine shapes, not final database schemas. The goal is to preserve consequence, recovery, risk, source-local boundaries, and owner-file validation without turning play into raw condition bookkeeping.


## Record tiers

Ephemeral harm lasts only during a moment or immediate scene and does not require durable storage unless it escalates. Session-relevant harm matters for the current scene or play unit but may clear. Durable harm changes the actor record or creates future obligations: injury, scar, persistent condition, degenerative harm, transformative harm, corruption, mutation, dual-state, carrier injury, route harm, identity harm, bond/anchor harm, recovery project, terminal harm, source-local boundary, proof-relevant harm, or owner-file handoff.


## Record families

Record families include Harm Event, Condition, Injury, Scar, Corruption, Mutation/Transformation, Identity/Mental/Principle Harm, Power-Strain Harm, Recovery, Terminal Harm, and Source-local Harm Boundary.


## Durable thresholds

Durable record required when harm persists beyond scene/session; requires recovery/treatment/project/maintenance; affects route/principle/technique/feature; affects Power Economy; causes corruption/mutation/dual-state/transformation; affects identity/memory/agency; affects companion/bond/anchor; creates faction/legal/social/world consequence; creates proof pressure; reaches severe or worse; creates source-local state; or requires owner validation.


## Visibility states and fairness

Visibility states include Visible, Diagnosed, Discovered, Obscured, Hidden, Dangerous, Source-local, Stabilized, Dormant, and Retired. Hidden or obscured harm must surface through symptoms, assessment, diagnosis, failed action, recovery attempt, teacher feedback, route response, carrier behavior, companion behavior, anchor behavior, environmental response, or source-local trigger. It must not be arbitrary surprise punishment.


## UI grouping

Future UI should group harm by Current Conditions, Injuries, Scars, Corruption/Instability, Mutations/Forms, Mind/Identity, Carrier/Power Strain, Recovery Projects, Dangerous States, Source-local Harm, and History/Retired. Player-facing display may simplify severity and persistence.


## Consolidation and retirement

A condition may retire when it heals, becomes injury, becomes scar, is purged, externalized, source-local resolved, or superseded. An injury may retire when healed, transformed into scar, folded into mutation, stabilized as permanent limitation, externalized, source-local resolved, or terminalized. Scars retire only when canonically removed, severed, overwritten, externalized, boundary closes, or archived inactive.


## Pool-state interaction

D07 records should not duplicate pool state unless harm persists beyond pool loss. Vitality loss alone, stamina depletion alone, Power pool depletion alone, platform integrity loss alone, or source-local stress pool loss alone does not create durable D07 harm unless condition/injury/scar or owner impact results.


## Shared record header

```yaml
d07_harm_record_header:
  record_id: string
  actor_or_target_ref: string
  record_family: harm_event | condition | injury | scar | corruption | mutation_transformation | identity_mental_principle_harm | power_strain | recovery | terminal_harm | source_local_boundary
  record_tier: ephemeral | session_relevant | durable
  visibility_state: visible | diagnosed | discovered | obscured | hidden | dangerous | source_local | stabilized | dormant | retired
  severity: trace | minor | moderate | severe | critical | catastrophic | lethal_terminal | not_applicable
  persistence: instant | scene | session | short_recovery | long_recovery | persistent | degenerative | transformative | permanent | source_local | not_applicable
  source_ref: string
  source_owner: D02 | D03 | D04 | D05 | D06 | D07 | D08 | D09 | D10 | source_local | unknown
  owner_handoff_state: {}
  active_effect_summary: string
  recovery_or_resolution_summary: string
  history_retention_required: boolean
  validation_state: authorized | pending_owner_file | dangerous | source_local | blocked | escalated | retired
```

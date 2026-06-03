---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-01 Damage, Injury, Conditions, Severity, and Persistence

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

D07 distinguishes Damage, Condition, Injury, and Scar. Damage is immediate harmful pressure. A Condition is an active named state. An Injury is persistent harm that affects function beyond the immediate event. A Scar is lasting integrated harm that becomes part of body, identity, route, carrier, bond, anchor, history, or source-local state.


## Damage

Damage may be physical, energetic, cognitive, conceptual, corruptive, biological, technological, environmental, social/obligation-based, spiritual, source-local, or mixed. Damage may reduce a pool, trigger a condition, create an injury, expose corruption, destabilize a carrier, or do nothing durable if absorbed. Damage alone is not necessarily durable D07 state.


## Conditions

A Condition is a named active state affecting function. Examples include Bleeding, Burned, Fractured, Winded, Exhausted, Disoriented, Memory Flooded, Self-Dissonant, Tainted, Spore Bloom, Overdrawn, Oath-Strained, Sync-Fractured, Feedback-Burned, Debt-Crushed, Pressure-Sick, False Sky Sick. A condition should define family, severity, persistence, impairment, recovery, escalation, and handoffs if durable.


## Injuries

An Injury is harm that persists beyond the immediate condition stage. Injuries can affect body, mind, identity, carrier, route, bond, anchor, social position, or source-local state. Examples include Pierced Thigh, Torn Carrier Channel, Foreign Memory Intrusion, Broken Speech Injury, Neural Feedback Burn, Spore Memory Fracture, and Star-Map Disorientation.


## Scars

A Scar is lasting integrated harm. Scars may be negative, mixed, adaptive, proof-bearing, route-shaping, mutation-seeding, source-local, or externalized. Scars are not automatically benefits. Any feature or advancement implication requires D04/D06 validation.


## Escalation and transition

A condition may become an injury when severity is moderate or higher and untreated, persistence exceeds scene/session, the condition recurs, a core structure is affected, route/carrier/bond/identity state changes, failed recovery worsens it, breakthrough failure creates lasting harm, or source-local rules require tracking. An injury may become a scar when it heals incompletely, the actor adapts, it becomes proof-bearing, route identity absorbs it, mutation stabilizes around it, or externalization leaves residue.


## Functional stacking

Multiple harms interact by functional overlap, not simple additive stacking. If two conditions impair the same function, one may dominate, combine into higher severity, become a complication trigger, remain latent, form mixed-family injury, or require owner escalation.


## Pool thresholds

Pool loss alone should not create durable D07 records unless it crosses a consequence threshold. Vitality loss alone may remain pool-state. Vitality loss past wound threshold may create injury. Power pool depletion remains D03. Overdraw may create Overdrawn or Carrier-Torn. Platform integrity remains D09 unless actor harm occurs.


## Record shape

```yaml
condition_or_injury_record:
  record_id: string
  actor_ref: string
  record_type: condition | injury | scar
  harm_family: physical | fatigue | cognitive | identity | corruption | mutation | carrier | route | bond | anchor | social_obligation | environmental | conceptual_resource | source_local | mixed
  severity: trace | minor | moderate | severe | critical | catastrophic | lethal_terminal
  persistence: instant | scene | session | short_recovery | long_recovery | persistent | degenerative | transformative | permanent | source_local
  impaired_functions: []
  worsens_when: []
  stabilizes_when: []
  recovery_options: []
  escalation_outputs: []
  owner_handoffs: {}
  validation_state: authorized | pending_owner_file | dangerous | source_local | blocked | escalated
```

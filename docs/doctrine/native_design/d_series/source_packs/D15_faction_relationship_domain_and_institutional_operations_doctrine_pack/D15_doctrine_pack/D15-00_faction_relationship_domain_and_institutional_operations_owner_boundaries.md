# D15-00 — Faction, Relationship, Domain, and Institutional Operations Owner Boundaries

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Core question

How does Astra handle organized actors, relationships, obligations, institutional power, faction pressure, diplomacy, domain control, law, reputation, and social campaigns over time without turning factions into arbitrary AI, universal clocks, or donor kingdom-turn systems?

D15 is the doctrine layer for organized social operation. It governs how factions, institutions, relationships, debts, obligations, territorial claims, law authorities, guilds, sects, corporations, kingdoms, patron networks, player organizations, and domains act or respond through procedure.

## 2. Why this file exists

D10 records what the world remembers: factions, law, economy, relationships, reputation, hidden truth, rumors, unresolved pressure, and world-state queues. D12 defines scene cadence. D13 defines Projects and long-task intervals. D14 defines travel, territory crossing, route pressure, site entry, and discovery.

D15 defines how organized social structures operate on those records and pressures. Without D15, institutional behavior can drift into arbitrary model narration, faction clocks as hidden law, kingdom turns as campaign structure, or donor reputation scores as social truth.

## 3. Primary architecture

D15 uses a Standing–Pressure–Operation Architecture.

```text
social or institutional state exists in D10
  -> D15 identifies relevant organized actor or relationship structure
  -> standing / posture / obligation / pressure is reviewed
  -> operation trigger is identified
  -> operation scope and scale are set
  -> method, leverage, cost, and risk are declared
  -> D02 / D05 / D10 / D13 / D17 handoffs occur as needed
  -> result changes standing, pressure, obligation, access, treaty, law, or domain posture
  -> D10 records the world-state delta
```

## 4. What D15 owns

D15 owns the procedure by which organized social structures act or react.

D15 owns:

- faction action procedure;
- institutional operation procedure;
- relationship operation procedure;
- standing and posture changes as procedure;
- debts, favors, obligations, and claims as procedural objects;
- diplomacy and negotiation at institutional scale;
- treaties, pacts, accords, and agreements as institutional procedures;
- law authority operation;
- guild, sect, corporation, kingdom, order, agency, domain, and player-organization procedure;
- domain and territory operation;
- influence campaigns;
- social campaigns;
- faction conflict posture;
- institutional response;
- pressure decay and escalation procedure;
- D10 unresolved pressure operation;
- source-local faction and institutional systems.

## 5. What D15 must not own

D15 must not own:

- D02 resolution math;
- D03 resource pool definitions;
- D04 advancement gates or breakthroughs;
- D05 full method / skill taxonomy;
- D06 Technique, Principle, oath, or domain-expression mechanics;
- D07 harm, corruption, or injury consequences;
- D08 actor personhood and substrate doctrine;
- D09 object, relic, platform, or tool state;
- D10 world-state contents, hidden truth, public belief, rumor, or relationship records as stored facts;
- D11 presentation and hidden-state narration;
- D12 scene cadence;
- D13 Project interval procedure;
- D14 travel, territory crossing, discovery, or site entry;
- D16 opposition, encounter, hazard, patrol, raid, army, or war construction;
- D17 economy, acquisition, reward, requisition, licensing, ownership, market, value, and debt-value procedure;
- D18 campaign arcs, seasons, long-horizon pacing, state aging, state pruning, and domain evolution;
- runtime implementation;
- final faction, relationship, law, domain, or institution schema.

D15 may call or affect these owner files. It must not absorb them.

## 6. Donor-family pressures

D15 must survive pressure from many donor families.

D20/class-level donors pressure Astra toward reputation scores, faction ranks, downtime faction benefits, strongholds, patron rules, renown, guild access, and adventure faction rewards.

OSR/domain donors pressure Astra toward stronghold turns, domain income, hirelings, morale, reaction rolls, rulership, tax, law, wilderness claims, and faction-level consequences.

Narrative/tag donors pressure Astra toward clocks, fronts, threats, influence tracks, relationship tags, compels, player-authored facts, and faction moves.

Cyberpunk/skill-pool donors pressure Astra toward contacts, heat, legal exposure, corporate response, black markets, licenses, favors, reputation, surveillance, and institutional retaliation.

Lifepath/career donors pressure Astra toward service history, rank, patrons, debts, career institutions, mustering-out benefits, ship shares, legal status, and institutional obligations.

Cultivation/sect donors pressure Astra toward sect standing, contribution systems, master/disciple ties, clan politics, territory control, duels, sanctions, domain claims, and resource access.

Sci-fi/space donors pressure Astra toward polities, corporations, navies, stations, trade guilds, colonies, licenses, docking rights, fleet authority, and jurisdiction conflicts.

Horror/investigation donors pressure Astra toward secret societies, hidden cults, law suppression, rumor control, conspiracy pressure, institutional denial, and social paranoia.

Faction/kingdom games pressure Astra toward faction turns, asset turns, kingdom phases, domain actions, armies, projects, treaties, wars, and multi-scale political operation.

## 7. Core terms

### Organized Actor

An organized actor is a faction, institution, domain authority, guild, sect, corporation, polity, order, law office, patron network, crew organization, clan, cult, agency, movement, or player-created organization.

An organized actor is not automatically intelligent in the same way as an individual person. D08 owns actor/personhood. D15 owns institutional behavior and procedure.

### Standing

Standing is the relationship posture between an actor and another actor, faction, institution, domain, public, or legal body. Standing may include trust, respect, hostility, fear, debt, favor, scrutiny, legal status, access, patronage, obligation, rivalry, alliance, neutrality, reputation, and source-local standing.

Standing is multi-axis. It is not a single reputation score.

### Pressure

Pressure is unresolved social, institutional, legal, reputational, territorial, or factional force that may escalate, decay, surface, or transform.

D10 records pressure. D15 defines how it operates.

### Operation

An Operation is a faction, relationship, or institutional procedure that attempts to change social state.

Operations may be scene-scale, project-scale, institutional-scale, source-local, or campaign-scale. D15 defines operation grammar and hands off timing to D12, D13, or D18 as appropriate.

### Domain

A Domain is a controlled, claimed, administered, protected, contested, or symbolically bound social/institutional territory. D15 domain control must remain distinct from D06 domain-expression mechanics.

## 8. Anti-drift controls embedded in this file

- D15 does not become arbitrary faction AI. Significant institutional action requires a lawful trigger, initiator, target, goal, scale, method, leverage, cost/risk, and owner-file handoff.
- Organized actors are not giant NPCs. D08 owns personhood and actor substrate.
- Standing is multi-axis relational posture, not a single score.
- D10 owns stored world-state, public belief, hidden truth, rumor, law records, relationship records, and unresolved pressure queues.
- D15 domain control is not D06 domain expression.
- D15 may create conflict posture, but D12 owns immediate scene cadence, D16 later owns opposition/encounter construction, and D18 owns campaign-scale war pressure.

## 9. Acceptance criteria for D15-00

D15-00 is acceptable if it preserves clear owner boundaries, establishes Standing–Pressure–Operation as the architecture, rejects donor faction-law defaults, and gives every institutional construct a lawful path to mapping, source-local retention, quarantine, or escalation.

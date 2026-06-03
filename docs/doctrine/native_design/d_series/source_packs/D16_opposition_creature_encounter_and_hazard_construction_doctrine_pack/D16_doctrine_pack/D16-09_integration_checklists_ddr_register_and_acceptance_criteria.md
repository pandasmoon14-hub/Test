# D16-09 — Integration Checklists, DDR Register, and Acceptance Criteria

Status: `doctrine-pack`
Version: `v0.1`
Layer: D16 / operational procedure doctrine
Primary scope: Opposition, creature, encounter, and hazard construction
Authority posture: Doctrine-facing and conversion-facing. Not final runtime schema, not final statblock schema, not encounter-balance math.

D16 is part of the D12–D18 operational procedure layer. It assumes D00–D15 are active doctrine dependencies and must preserve their owner boundaries.


## Purpose

This file provides the D16 integration checklist, DDR register, anti-drift controls, and acceptance criteria. It is the final control file for the D16 pack.

## Integration checklist

A D16 construct is not ready unless it passes these checks:

```text
opposition source identified
threat function identified before donor stat labels
scale and role declared
objective and posture defined where relevant
pressure profile declared
capability pressure identified without final ability list
constraints / vulnerabilities / resistance routed to owner files
Threat Weight reviewed qualitatively
encounter purpose declared when composing an encounter
primary pressure declared
independent opposition elements separated
state-delta targets routed to owner files
source-local boundary recorded where needed
donor math rejected or preserved as evidence only
readiness state assigned
quarantine/escalation used when support is missing
```

## Owner-file handoff checklist

D16 must hand off:

```text
D02 — uncertainty, contests, defense/resistance checks
D03 — resource drain, overdraw, recharge, instability pressure
D05 — method, competency, tactics, investigation
D06 — Techniques, domains, Principles, oaths, power expression
D07 — harm, injury, corruption, conditions, exposure, resistance, vulnerability
D08 — actor substrate, creature/NPC/personhood/companion/summon
D09 — objects, weapons, armor, platforms, vehicles, tools, security systems
D10 — faction/world-state, hidden truth, law, territory, information
D11 — presentation and hidden-state boundaries
D12 — encounter cadence and action windows
D14 — travel/site-entry pressure if opposition appears through exploration
D15 — institutional pressure, faction operation, social/legal opposition
D17 — rewards, salvage, ownership, requisition, economy
D18 — recurring threat continuity and campaign-scale arc pressure
```

## Source-local boundary checklist

Source-local retention requires:

```text
source-local boundary named
donor assumptions recorded
mechanical finality denied
canon promotion not implied
proper nouns/lore/cosmology contained
owner-file gaps identified
quarantine/escalation used if boundary is unclear
```

## Anti-drift rules

Do not convert CR, level, HP, armor, attack, damage, saves, action economy, morale, reaction rolls, or encounter budgets into Astra math.

Do not treat creature type as Astra metaphysics.

Do not make combat the default form of opposition.

Do not reduce social, legal, institutional, object, platform, or environmental opposition to skill-check obstacles.

Do not turn boss, elite, minion, swarm, legendary, lair, hull, hardpoint, or platform labels into default mechanics.

Do not define final harm, resistance, vulnerability, immunity, condition, or damage math.

Do not define final creature, hazard, encounter, vehicle, platform, or reward schemas.

Do not let recurring opposition survive by fiat.

Do not let donor monster ecology become canon without review.

Do not let random encounter tables become encounter construction law.

Do not let D16 become D12 cadence, D07 harm, D08 actor substrate, D09 object/platform, D15 faction operation, D17 reward/economy, or D18 campaign pacing doctrine.

Do not let source-local opposition systems become Astra law through repetition alone.

## Acceptance criteria

D16 is accepted only if it can:

```text
construct opposition by function, pressure, scale, role, objective, posture, and owner-file handoff
treat creatures, NPCs, hazards, social antagonists, security systems, swarms, bosses, platforms, summons/companions, and institutional proxies as supported opposition types
compose encounters by objective and pressure rather than encounter budget
support noncombat and mixed opposition as first-class
use qualitative Threat Weight without CR, level, balance, or budget math
identify capability pressure without creating unsupported power lists
route resistance, vulnerability, immunity, protection, threshold, and bypass pressure to owner files
represent behavior, morale, retreat, surrender, and posture changes without universal morale tables
support recurring opposition only with continuity support
map donor opposition systems by function, not label
preserve bounded source-local opposition systems
quarantine unsupported opposition constructs
escalate repeated or high-impact missing doctrine
route consequences to owner files without stealing ownership
```

## DDR register

```yaml
D16_decision_register:
  D16-00:
    decision: Threat Role–Pressure–Profile Architecture
    rationale: supports broad opposition without donor statblock math
  D16-01:
    decision: opposition anatomy uses source, function, scale, role, objective, posture, pressure, routing, handoffs, boundary
    rationale: prevents creature-only or combat-only flattening
  D16-02:
    decision: qualitative threat construction with Threat Weight and readiness
    rationale: creates usable profiles without CR/level/budget math
  D16-03:
    decision: Objective–Pressure–Composition encounter model
    rationale: supports mixed and noncombat encounters without budgets
  D16-04:
    decision: Opposition Type Profiles
    rationale: guides conversion across common threat families without subsystems
  D16-05:
    decision: qualitative scaling, morale as persistence pressure, recurrence gates
    rationale: prevents hidden CR, morale tables, and recurrence by fiat
  D16-06:
    decision: functional donor opposition mapping ladder
    rationale: maps donor systems by function and lawful outcome
  D16-07:
    decision: lightweight not-final-schema record pack
    rationale: enables audit and conversion handoff without final runtime schema
```

## Open risk queue

```yaml
open_risks:
  - exact quantitative threat math remains intentionally undefined
  - final creature/hazard/encounter schemas remain Batch C or later schema work
  - D07 harm/resistance doctrine must remain authoritative for mechanical effects
  - D09 platform/object doctrine must define final platform threat mechanics
  - D18 must later control long-horizon recurring threat pacing
  - high-volume bestiary conversion may expose need for additional threat-band doctrine
```

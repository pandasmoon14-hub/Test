# D19-06 — Mixed Donor-Routing Stress Tests, Conversion-Readiness Trials, and Corpus-Scale Failure Detection

> **Status:** Phase 1 capstone doctrine. This file is a control-layer artifact for Astra Ascension doctrine integration. It is not final sourcebook prose, not a live-play GM adapter, not a runtime/backend schema, and not a donor conversion output. Any record shapes in this pack are lightweight doctrine-facing / conversion-facing / audit-facing shapes only and may be replaced or formalized later by Batch C schema doctrine, Runtime Gate B, canon consolidation, or playtest calibration.


## Core question

How does Astra test whether D00–D18 can route complex donor constructs across owner files without collapsing into donor assumptions, blended rulings, fake certainty, unsupported normalization, or uncontrolled source-local sprawl?

## Scenario–Construct–Route–Outcome Test Model

D19 uses this procedure:

```text
1. Select a mixed donor-style scenario.
2. Identify all embedded constructs.
3. Split mixed constructs into subconstructs.
4. Assign owner files and handoffs.
5. Assign lawful outcomes.
6. Identify source-local boundaries.
7. Identify quarantine points.
8. Identify escalation triggers.
9. Identify deferred math/schema/runtime/canon dependencies.
10. Score the test for conversion readiness.
```

A stress test is not a full conversion. Passing requires lawful routing, not full conversion or direct mapping.

## Readiness states

```text
passes_cleanly
passes_with_source_local_boundary
passes_with_quarantine
passes_with_escalation
passes_with_deferred_schema_note
fails_due_to_owner_conflict
fails_due_to_missing_handoff
fails_due_to_donor_leakage
fails_due_to_unowned_construct
fails_due_to_runtime_or_canon_confusion
```

A test can pass with quarantine or escalation if the blocker and route are clear.

## Leakage risks

Each stress test tracks:

```text
donor_math_leakage
donor_metaphysics_leakage
donor_action_economy_leakage
donor_progression_leakage
donor_economy_leakage
donor_harm_model_leakage
donor_inventory_leakage
donor_faction_clock_leakage
donor_campaign_structure_leakage
donor_runtime_behavior_leakage
```

## Required stress scenarios

### Stress Test 1 — D20 Adventure Path Chapter

Pressure profile: level band, scripted chapter order, treasure parcel, monster statblocks, boss phase, magic items, quest rewards, faction NPCs, regional law, milestone advancement.

Primary risks: adventure path becomes campaign doctrine; level band becomes campaign phase; monster math becomes D16; treasure parcel becomes D17 reward law; magic item rarity becomes D09/D17 canon; boss phase becomes default encounter structure.

Expected routing: D02 resolution only; D04 advancement implications; D09 magic item/object state; D10 region/world/faction state; D15 faction authority; D16 opposition construction; D17 treasure/reward/value-entry; D18 chapter/arc/season/horizon; source-local for adventure path sequence.

### Stress Test 2 — Cultivation Sect Advancement Arc

Pressure profile: spirit stones, contribution points, sect rank, auction house, rare pill, realm breakthrough, elder patronage, territory claim, training hall, rival disciple, seasonal tournament.

Primary risks: spirit stones become Astra currency; realm ladder becomes advancement law; sect rank becomes campaign phase; contribution points become universal faction credit; breakthrough pill becomes required advancement currency; tournament arc becomes default season model.

Expected routing: D03 for power-resource pressure only if involved; D04 advancement/breakthrough; D06 route/domain expression; D08 actor/personhood/form implications; D10 sect/world state; D13 training/project access; D15 sect institution/rank/standing; D16 rival/opposition; D17 spirit stones/contribution/auction/value; D18 arc/season/horizon placement; source-local for sect economy and realm ladder unless canonized.

### Stress Test 3 — Cyberpunk Corporate Extraction Mission

Pressure profile: restricted cyberware, licenses, black market, corporate heat, debt, contact favors, timed mission, stealth/infiltration cadence, social engineering, evidence custody, extraction reward.

Primary risks: license model becomes universal legality; black market becomes guaranteed shop; corporate heat becomes universal faction clock; cyberware capacity becomes D09 canon prematurely; debt becomes only money; stealth procedure imports donor action economy.

Expected routing: D05 methods/competency; D09 cyberware/object/implant state; D10 law/public belief/hidden truth; D12 stealth/timed cadence; D13 preparation Projects; D15 corporate/institutional pressure; D16 guards/security opposition; D17 black market/debt/licenses/rewards; D18 arc pressure and recurring corporate consequences.

### Stress Test 4 — OSR Hexcrawl to Domain Play

Pressure profile: hex turns, random encounter checks, treasure extraction, coin weight, hirelings, stronghold construction, domain income, faction reaction, downtime months, travel attrition.

Primary risks: hex turns become D14 default; coin weight becomes D17 inventory law; treasure-as-XP becomes D04 law; random encounters become D14/D16 default; domain turns become D15/D18 universal; stronghold procedure steals D13/D15/D17 ownership.

Expected routing: D04 advancement only if supported; D10 world/domain/faction state; D13 construction/downtime Projects; D14 travel/exploration route pressure; D15 domain/faction operation; D16 random encounter opposition; D17 treasure/coin/inventory/domain income; D18 domain phase/time skip/seasonal structure; source-local for hex/domain cadence unless adopted later.

### Stress Test 5 — Sci-Fi Ship Campaign

Pressure profile: ship fuel, cargo capacity, crew injury, platform damage, salvage rights, docking fees, faction law, restricted technology, long travel time, refit season, recurring pirate threat.

Primary risks: fuel becomes universal travel resource; cargo becomes default inventory model; ship hull math becomes D09/D16 law; salvage becomes free wealth; refit season becomes mandatory campaign phase; faction law becomes D10/D15 overreach.

Expected routing: D07 crew harm; D08 crew/AI/personhood if relevant; D09 ship/platform/cargo/object state; D10 law/world-state; D13 repair/refit Projects; D14 travel; D15 faction law/claims; D16 pirate/opposition/platform threats; D17 fuel/cargo/salvage/docking fees; D18 long travel, refit season, recurrence.

### Stress Test 6 — Horror Investigation Campaign

Pressure profile: hidden truth, clue gates, evidence custody, recurring dread, sanity-like pressure, corrupted location, NPC instability, limited supplies, conspiracy clock, campaign fatigue.

Primary risks: sanity becomes D07 default; clue gating becomes D05/D14 default; conspiracy clock becomes D18/D15 universal; hidden truth leaks through D11; horror attrition becomes universal campaign pacing.

Expected routing: D05 investigation methods; D07 harm/corruption/condition only if supported; D08 NPC instability/personhood; D10 hidden truth/public belief/rumor; D11 hidden-state presentation; D14 discovery/site entry; D15 conspiracy institution/faction if applicable; D16 hazards/opposition; D17 supplies/evidence custody; D18 recurring dread, arc/season fatigue, continuity; source-local for sanity/conspiracy clocks unless adopted.

### Stress Test 7 — Vehicle / Mech War Scenario

Pressure profile: mech hardpoints, ammo, repair cycles, pilot injury, morale, battlefield salvage, requisition, faction command, territory control, campaign front, refit downtime.

Primary risks: hardpoints become universal platform schema; ammo becomes universal sink; morale table becomes D16 default; campaign front becomes D18 law; requisition becomes free supply; battlefield salvage becomes automatic ownership.

Expected routing: D07 pilot harm; D08 pilot/AI/companion substrate if relevant; D09 mech/platform/hardpoint state; D12 battle cadence; D13 repair/refit Projects; D15 command/requisition/faction/domain; D16 opposition/encounter role; D17 ammo/requisition/salvage/value; D18 campaign front/refit season/territory continuity.

### Stress Test 8 — Narrative-Tag Relationship Season

Pressure profile: relationship debt, player-authored flashback, aspect/tag invocation, season finale, shared truth, social conflict, clocks, retcon pressure, spotlight rotation.

Primary risks: player-authored truth bypasses D10/D18 continuity; flashbacks become unrestricted retcon; tags/aspects become universal mechanics; season finale becomes mandatory structure; relationship debt becomes only narrative flavor; spotlight rotation becomes live-play adapter behavior.

Expected routing: D02 resolution if checks occur; D05 method/competency; D10 relationship/world-state/truth; D11 presentation; D12 social cadence if structured; D15 relationship/obligation operations; D17 debt/value if applicable; D18 flashback reconciliation, season, continuity, payoff scale; source-local for tag/aspect mechanics unless canonized.

## Optional scenarios

D19 may also test post-scarcity utopia, generational legacy campaign, apocalypse survival season, isekai/LitRPG system interface, political kingdom campaign, and mythic realm travel.

## Stress-test principles

```text
A stress test is not a full conversion.
Passing does not require every construct to map directly.
Passing requires every construct to have a lawful route.
Quarantine is acceptable if blocker and unlock condition are clear.
Escalation is acceptable if missing doctrine is real and named.
Source-local retention is acceptable if boundary and rejected imports are explicit.
A test fails if it requires loose conversion, donor default adoption, hidden owner conflict, unsupported schema, or runtime/canon collapse.
Repeated failures across donor families become escalation pressure.
```

## Acceptance criteria

D19-06 is accepted if it defines robust mixed-donor stress tests, requires construct splitting, tracks leakage risks, scores readiness, and routes follow-up without performing full donor conversion.

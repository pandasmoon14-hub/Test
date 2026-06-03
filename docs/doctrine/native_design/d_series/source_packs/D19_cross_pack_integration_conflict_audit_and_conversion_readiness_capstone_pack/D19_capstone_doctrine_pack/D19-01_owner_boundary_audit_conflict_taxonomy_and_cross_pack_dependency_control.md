# D19-01 — Owner-Boundary Audit, Conflict Taxonomy, and Cross-Pack Dependency Control

> **Status:** Phase 1 capstone doctrine. This file is a control-layer artifact for Astra Ascension doctrine integration. It is not final sourcebook prose, not a live-play GM adapter, not a runtime/backend schema, and not a donor conversion output. Any record shapes in this pack are lightweight doctrine-facing / conversion-facing / audit-facing shapes only and may be replaced or formalized later by Batch C schema doctrine, Runtime Gate B, canon consolidation, or playtest calibration.


## Core question

How does Astra verify that D00–D18 each own the correct layer, do not duplicate or contradict one another, and hand off state cleanly when a construct touches multiple doctrine files?

## Owner–Handoff–Conflict Audit Model

D19 uses this procedure:

```text
1. Identify the construct or rule.
2. Identify primary owner file.
3. Identify secondary owner-file handoffs.
4. Identify what each file may lawfully decide.
5. Identify what each file must not decide.
6. Classify overlap status.
7. Assign fix route if needed.
```

D19 may recommend owner patches, handoff notes, record registry notes, source-local boundaries, quarantine, escalation, or no action. D19 must not rewrite owner-file doctrine inside the capstone unless the issue is purely cross-pack integration.

## Conflict taxonomy

Every audited overlap receives one status:

| Status | Meaning |
|---|---|
| `clean_boundary` | Primary owner and handoffs are clear; no overreach. |
| `minor_clarification_needed` | Doctrine is probably correct but wording could prevent drift. |
| `handoff_missing` | Primary owner is clear but a necessary secondary handoff is absent. |
| `boundary_conflict` | Two files appear to claim the same decision authority. |
| `duplicate_ownership` | Two files maintain overlapping records or procedures without clear distinction. |
| `doctrine_gap` | No existing file clearly owns the construct. |
| `escalation_required` | The issue exposes missing doctrine, canon conflict, repeated donor pressure, or unstable architecture. |

## Fix routes

Allowed fix routes:

```text
owner_patch
handoff_note
record_registry_note
source_local_boundary
quarantine
escalation
no_action
```

D19 does not use “convert loosely,” “let GM decide,” or “handle narratively” as fix routes for state-bearing constructs.

## High-risk audit pairs

### D02 vs D12

Risk: resolution math and outcome states could blend with action cadence, initiative, reactions, and turn procedure.

Boundary: D02 owns check math and outcome interpretation. D12 owns when actions occur and how structured time proceeds.

### D02 vs D16

Risk: opposition construction could import hit/miss, difficulty, save, attack, or CR math.

Boundary: D02 owns resolution. D16 owns threat profile, pressure, role, encounter composition, and readiness.

### D03 vs D17

Risk: power resources could collapse into economy resources, or currency/resources could become power pools.

Boundary: D03 owns power economy, pools, overdraw, recharge, and carrier resource behavior. D17 owns value flow, acquisition, reward, inventory, requisition, sinks, custody, and ownership.

### D04 vs D18

Risk: campaign pacing could define advancement mechanics, or advancement mechanics could dictate campaign structure.

Boundary: D04 owns advancement payloads and breakthrough mechanics. D18 owns campaign-scale spacing, trajectory, phase, horizon promise, and transformation placement.

### D06 vs D16

Risk: threat capabilities could become Technique/power rules, or Technique doctrine could define monster abilities.

Boundary: D06 owns route, Technique, Principle, oath, and domain expression. D16 owns opposition capability pressure and routes exact power expression to D06 where needed.

### D07 vs D16

Risk: harm pressure could become harm math.

Boundary: D16 identifies harm, condition, vulnerability, resistance, corruption, and exposure pressure. D07 defines actual harm, condition, resistance, vulnerability, corruption, and backlash consequences.

### D08 vs D16

Risk: creature/opposition profiles could define actor substrate, personhood, control, or companion identity.

Boundary: D16 constructs opposition. D08 owns actor identity, personhood, substrate, companion/summon identity, form-state, and control boundaries.

### D09 vs D17

Risk: item value and item state could collapse.

Boundary: D09 owns object, relic, platform, material, tool, vehicle, implant, and item state. D17 owns value, acquisition, custody, ownership, sale, burden, storage, reward, salvage, and requisition procedure.

### D10 vs D18

Risk: world-state records could become structural-time records, or D18 could overwrite D10 history.

Boundary: D10 owns world-state facts. D18 owns continuity lifecycle, half-life, salience, retrieval, arc/season/horizon placement, and aging/pruning classification.

### D11 vs D18

Risk: structural-time controls could become presentation advice, or presentation could mutate campaign state.

Boundary: D11 owns player/GM-facing presentation and hidden-state surfacing. D18 owns campaign-scale structural time and persistence relevance.

### D13 vs D17

Risk: resource gathering, crafting, salvage, repair, and maintenance Projects could merge with value-flow procedure.

Boundary: D13 owns interval-scale Project procedure. D17 owns value-entry, acquisition, exchange, custody, burden, and sinks generated by those Projects.

### D15 vs D17

Risk: faction stores, claims, licenses, obligations, debts, requisition, and law access could blur.

Boundary: D15 owns institutional operation, claim, law, standing, enforcement, obligations, and domain authority. D17 owns value/access/economy side of acquisition, requisition, debt payment, custody, and reward.

### D15 vs D18

Risk: faction cycles could become seasons, or seasons could run faction operations.

Boundary: D15 owns faction/institution operations. D18 owns campaign-scale classification, time skips, season seams, phase transitions, and structural-time reclassification.

### D16 vs D17

Risk: encounter rewards, monster parts, loot, and salvage could become automatic value-entry.

Boundary: D16 owns encounter/opposition construction and reward pressure triggers. D17 owns value-entry, loot, salvage, custody, ownership, burden, reward, and sink procedure.

### D18 vs runtime

Risk: D18 runtime persistence notes could become final memory/context schema.

Boundary: D18 may define capture/retrieval/salience/handoff requirements. Runtime Gate B or later schema doctrine owns implementation.

## Required audit entry

Use the `owner_boundary_audit_entry` shape from D19-08. Each entry must identify construct, primary owner, secondary handoffs, lawful decision boundary, non-decision boundary, status, risk, fix route, affected files, and notes.

## Acceptance criteria

D19-01 is accepted if high-risk overlaps are audited with explicit owner, handoff, decision, non-decision, conflict status, risk, and fix route, and if D19 remains an audit layer rather than a rewrite layer.

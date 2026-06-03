# D13-02 — Project Creation, Requirement Discovery, Commitment, and Interval Setup

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

How does Astra start a Project lawfully?

D13-02 defines the procedure for turning actor or world intent into a valid interval-scale Project without guessing missing requirements, skipping costs, revealing hidden state, or letting donor downtime procedure decide Astra law.

## Project setup procedure

A Project begins through eight setup checkpoints:

1. Intent checkpoint
2. Goal checkpoint
3. Project family checkpoint
4. Scope checkpoint
5. Requirement discovery checkpoint
6. Cost / risk preview checkpoint
7. Commitment checkpoint
8. Interval setup checkpoint

This setup procedure applies to all Project families, including recovery, training, research, crafting, salvage, repair, social work, faction support, maintenance, and special/source-local Projects.

## 1. Intent checkpoint

The actor declares what they want to accomplish over interval-scale time.

Examples:

- “I want to repair the damaged skiff.”
- “I want to recover from the corruption backlash.”
- “I want to study the relic inscriptions.”
- “I want to train under the sect’s blade elder.”
- “I want to craft a stabilizing housing for this core.”
- “I want to rebuild my reputation with the harbor guild.”
- “I want to salvage the crashed platform.”

At this checkpoint, D13 captures intent. It does not yet decide feasibility or success.

## 2. Goal checkpoint

The goal must be clarified enough to know what success would change.

A valid goal identifies at least one intended state change or delayed consequence:

- actor state;
- condition / injury / corruption state;
- competency / training posture;
- information state;
- object state;
- resource/material state;
- relationship state;
- faction or institutional state;
- location/facility state;
- campaign pressure state;
- source-local state.

If the goal has no possible state change, it may remain ordinary narration or free play.

## 3. Project family checkpoint

D13 assigns one primary Project family and any secondary pressure families.

Example:

```yaml
project_family_classification:
  primary_family: repair
  secondary_families:
    - salvage
    - resource_gathering
    - technical_research
  likely_owner_files:
    - D05
    - D09
    - D17
```

A mixed Project should not be flattened. If it contains distinct goals requiring different owner files, D13 should split it into linked Projects.

## 4. Scope checkpoint

Assign a provisional scope band:

- minor;
- standard;
- major;
- extended;
- transformational.

Scope is based on:

- intended state change;
- risk;
- rarity of requirements;
- number of owner files involved;
- source-local complexity;
- campaign impact;
- whether identity, faction, object, route, or world-state changes are possible.

Scope may change after requirement discovery.

## 5. Requirement discovery checkpoint

Determine what is known, unknown, missing, blocked, or protected.

Requirement status vocabulary:

| Status | Meaning |
|---|---|
| `met` | Requirement is available and usable. |
| `missing` | Requirement is known but absent. |
| `unknown` | Requirement may exist but has not been discovered. |
| `protected_hidden` | Requirement exists or may exist, but revealing it would violate hidden-state boundaries. |
| `blocked_by_owner_file` | Requirement cannot be resolved without another doctrine owner. |
| `source_local` | Requirement is valid only inside a bounded source-local procedure. |
| `quarantined` | Requirement cannot be handled safely with current evidence or doctrine. |

D13 may mark a requirement as `protected_hidden` without revealing it. Discovery of protected requirements requires appropriate D05/D10/D11-supported procedure.

## 6. Cost / risk preview checkpoint

Before commitment, the actor should receive visible costs and risks when knowable.

Possible visible previews:

- time required;
- materials likely required;
- resource or wealth pressure;
- facility occupation;
- assistant or crew requirement;
- risk of worsening condition;
- risk of object damage;
- risk of social scrutiny;
- risk of faction attention;
- risk of corruption / instability;
- chance of incomplete result;
- need for further owner-file review.

Hidden risks remain protected by D10/D11 or the relevant owner file.

## 7. Commitment checkpoint

The actor commits to the Project.

Commitment may include:

- time block;
- materials reserved;
- facility claimed;
- assistant assigned;
- resource cost paid or reserved;
- exposure accepted;
- opportunity cost accepted;
- relationship/faction obligation accepted;
- object placed under work;
- actor enters recovery/training/research posture.

Time, materials, facility claims, assistant assignment, resource cost, exposure, and opportunity cost commit before interval progress begins unless an owner file or source-local rule says otherwise.

D13 should not allow “wait to see if the Project succeeds before paying” unless another owner file explicitly permits it.

## 8. Interval setup checkpoint

The Project enters its first interval.

D13 records:

- interval scale;
- next progress check or condition for progress check;
- active requirements;
- open unknowns;
- owner-file handoffs;
- interruption risks;
- Project status;
- state affected if abandoned;
- source-local boundaries.

## Setup outcomes

Requirement discovery and setup produce one of five outcomes.

| Outcome | Meaning |
|---|---|
| `ready_to_begin` | Requirements, cost preview, and owner-file support are sufficient to enter interval handling. |
| `ready_with_risk` | Project can begin, but incomplete information, unstable conditions, poor facilities, insufficient materials, scrutiny, or similar risk is declared. |
| `blocked_pending_requirement` | Project cannot begin until a missing requirement is satisfied. |
| `quarantined_pending_doctrine_or_evidence` | Project cannot begin because evidence or doctrine cannot support it safely. |
| `escalated_owner_file_problem` | Project exposes a missing doctrine area requiring owner-file action. |

## Blocked pending requirement examples

- no safe recovery location;
- missing material;
- no relevant access tag;
- facility unavailable;
- object too damaged to work safely;
- information insufficient;
- faction permission absent;
- assistant required but unavailable.

## Quarantine examples

- donor cyberware surgery system before installation doctrine exists;
- broken crafting table with missing material rows;
- ritual Project dependent on unsupported metaphysics;
- time-loop training procedure with no causality doctrine;
- unclear donor recovery procedure from damaged extraction.

## Escalation examples

- D07 lacks recovery distinction needed for repeated donor injury systems;
- D09 lacks object-state rules for repair/refit conversion;
- D15 lacks institutional Project operation needed for faction-scale work;
- D17 lacks requisition/access procedure for recurring military, sect, or corporate supply systems;
- D18 lacks long-horizon state-aging rules for decade-scale cultivation Projects.

## Hidden requirement rule

D13 may record that a hidden requirement is present, suspected, or protected without revealing it. A player-facing view should not receive hidden backend facts simply because a Project setup procedure exists.

D11 presentation and D10 information-state boundaries control what is surfaced.

## Anti-drift controls

- Do not start vague Projects that lack intended state change.
- Do not reveal protected hidden requirements.
- Do not bypass owner-file prerequisites.
- Do not commit only after success unless permitted.
- Do not normalize donor setup costs into Astra without owner-file support.

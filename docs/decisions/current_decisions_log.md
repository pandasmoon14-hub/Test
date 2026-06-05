# Current Decisions Log

> Cross-reference: For extraction-lane and pipeline-operational decisions, see `docs/operations/current_decisions_log_v0_1.md`.
> Scope note: this file tracks project-level decision records across governance, handoff contract, and program direction; it is not the operations lane log.

This file records project decisions that are not obvious from code alone. Its purpose is to prevent re-litigating settled pilot choices across ChatGPT, Claude, Claude Code, Grok, Codex, and manual PowerShell sessions.

## Current working repo and run layout

- Active repo path: `C:\Dev\Test-main-git`
- Active Step 10 run path: `C:\AetherForgeRuns\_active\handoff_step10_conversion_intake_run_v0_1`
- Step 10B final frozen snapshot: `C:\AetherForgeRuns\handoff_step10b_12_packet_conversion_intake_run_20260513_153357.zip`
- Step 10C final snapshot should be created after under-parsed packet repair and final strict validation.

## Handoff contract principles

- Extraction truth is not conversion permission.
- Conversion permission is not canon permission.
- Canon permission requires review and promotion.
- Donor content is not live-play authority.
- Donor constructs must receive one lawful outcome:
  - direct Astra mapping
  - normalized Astra mapping
  - source-local retained construct
  - quarantined construct pending later doctrine
  - escalated doctrine problem

## Local extraction and handoff decisions

- Lane A is accepted as the safe local default for the pilot cycle.
- AUTO / higher lanes may fall back to Lane A when external dependencies are unavailable.
- Missing Marker/Docling-style local dependencies are not blockers for this pilot.
- OCR may be attempted/applied, but OCR output is not automatically higher authority than native text.
- Page truth, manifest data, defects, queues, and conversion permissions must be preserved separately.
- `OCR_MODE=skip` remains the safe pilot default unless a targeted OCR repair pass is explicitly being tested.

## Step 10B packet selection rationale

The 12-packet Step 10B selection was intentionally broad. It tested:
- Fate mechanics/procedure
- Fate worksheet/character setup
- Random tables/list material
- Pathfinder adventure-site/dungeon/statblock pressure
- GURPS Bio-Tech biotechnology/body modification/living-platform pressure
- Cities Without Number urban/cyberpunk/combat/gear pressure
- CthulhuTech vehicle/platform/horror/investigation pressure
- Numenera/Jade Colossus procedural ruin/random-table/anomaly pressure
- Anima character options/combat modules/statblock pressure
- Colostle credits/backmatter false-positive pressure
- Heroines of the Last Age macro-region/travel/threat-hook pressure
- Sword World replay/character-sheet/party/crafting pressure

## Step 10B / Step 10C findings

- Step 10B produced 12 drafted packets and 0 placeholders.
- Two Markdown memos were rich but under-parsed in JSON because section headings were escaped as `1\.` instead of `1.`:
  - Pathfinder Dungeons of Golarion pages 19-37
  - Book of Random Tables Fantasy Space pages 8-17
- The scaffolder should tolerate escaped numbered headings.
- Report tooling should detect fallback-level parses.
- Colostle was a low-value but useful negative-control packet. It should be retained as a credits/backmatter false-positive case.
- Credits, backer names, acknowledgements, supporter lists, and publication backmatter should be classified as non-convertible source-local material.
- Dense name lists should not be treated as random tables, statblocks, factions, NPCs, or setting canon.

## Final Step 10B aggregate result before Step 10C repair

- packets_total: 12
- drafted: 12
- placeholder: 0
- source-local retained construct: 113
- normalized Astra mapping: 328
- direct Astra mapping: 6
- quarantined construct pending later doctrine: 40
- escalated doctrine problem: 10
- doctrine_escalation_count: 118
- source_local_retention_count: 148
- rejected_import_count: 157
- canon_candidate_note_count: 10

## Step 11 purpose

Step 11 applies Step 10C findings to the repo:
- add escaped-heading parser tolerance
- add under-parsed result detection
- add false-positive/backmatter classification notes
- add tests for the known Step 10C failure cases
- update handoff docs so future runs do not repeat these manual fixes

## 2026-05-26 decision log - pre-A01 control layer patch

- Decision ID: PREA01-001
- Decision date: 2026-05-26
- Decision type: control/governance patch

### Summary
- A00 is introduced as a pre-A01 control file: `A00_mechanical_posture_and_ruleset_non_adoption.md`.
- A01 remains `A01_cosmology_and_dimensional_architecture.md` with no rename.
- K01 remains `K01_lexicon_governance_and_reserved_terms.md`; lexicon governance is not moved into A01.

### Governance effect
- Establishes explicit mechanical non-adoption posture during doctrine bootstrap.
- Confirms extraction/conversion progress does not imply donor-ruleset adoption.
- Adds registry tracking for PREA01-001 and A00 control-layer records.

### Guardrails reaffirmed
- Control layer patch is non-mechanical and non-runtime.
- No phase-order or dependency-lock bypass is authorized.
- Any doctrine file that treats donor rules as default Astra authority must be escalated.
- Stage 5 lexicon-control entries route to K01/pre-A01 ledgers/work orders, not direct A01 renumbering.
- State-change digest is a report from committed backend events and is never authority by itself.
- Registry entries are tracking/work-order records, not canon or accepted terms.


## 2026-06-05 decision log - current-state reconciliation after PR #204

- Decision ID: CTRL-CURRENT-STATE-RECONCILIATION-001
- Decision date: 2026-06-05
- Decision type: documentation/control reconciliation

### Summary
- PR #204 is treated as merged for current-state control purposes.
- Astra Ascension remains the project identity; Aether Forge is subordinate extraction/handoff developer tooling.
- Backend-first model interchangeability, persistence ownership, generated-content lifecycle, knowledge/dialogue distinction, and narration validation remain planning/control posture unless future owner files implement them.

### Governance effect
- Supersedes stale roadmap-bootstrap instructions to create ROADMAP-001/REGISTRY-001 and redraft A01-A05 as immediate next actions.
- Directs near-term work toward current-state reconciliation, registry hygiene, dependency/test repair, and preparation for a later Runtime Boundary + Generator Ownership Audit.
- Preserves existing Batch A/B/C/D/control content unless a later audit explicitly authorizes changes.

### Guardrails reaffirmed
- This reconciliation is not runtime implementation.
- It does not create database schemas, persistence writers, generated-content records, generators, live-play adapters, training sets, donor content, or canon promotion.
- The Runtime Boundary + Generator Ownership Audit remains planned but not performed by this decision.
- Registry and roadmap test results must be reported honestly, including missing PyYAML or other dependency failures.

## 2026-06-05 decision log - Runtime Boundary + Generator Ownership Audit protocol scaffold

- Decision ID: CTRL-RUNTIME-GENERATOR-AUDIT-PROTOCOL-001
- Decision date: 2026-06-05
- Decision type: documentation/control scaffold

### Summary
- Added `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md` as the protocol for a future Runtime Boundary + Generator Ownership Audit.
- The protocol fixes the future audit scope, allowed classification labels, input-source precedence, output schema, review process, and non-goals.
- The protocol requires the later audit to evaluate whether each subsystem can eventually be executed by backend code without relying on the LLM to improvise missing mechanics, state, validation, memory, persistence, generators, or consequences.

### Governance effect
- Converts the roadmap's future audit placeholder into repeatable review instructions without performing the audit.
- Preserves the backend-first model-interchangeability invariant and the distinction between backend authority and LLM narration/proposal.
- Requires future findings to cite actual repo paths and to avoid donor-PDF/direct-donor-content auditing.

### Guardrails reaffirmed
- This scaffold is not a runtime implementation.
- It does not classify subsystems, rewrite Batch A/B/C/D-series/SM doctrine, create generators, create validators, create persistence writers, promote canon, authorize live play, or create training material.
- Runtime/training layers remain planned future layers unless actual repo files exist when the later audit is performed.

## 2026-06-05 decision log - Runtime Boundary + Generator Ownership Audit Wave 1 report

- Decision ID: AUDIT-WAVE1-001
- Decision date: 2026-06-05
- Decision type: limited audit report

### Summary
- Added `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md` as the first limited application of AUDIT-001.
- The report audits 10 representative subsystem records only and proves the output schema, classifications, LLM-overreach analysis, and next-wave scoping approach before any full-corpus audit.
- The report cites actual repo paths and records substitutions only where needed; no requested Wave 1 target required substitution.

### Governance effect
- Establishes a repeatable Wave 1 report pattern for later Runtime Boundary + Generator Ownership Audit waves.
- Keeps audit findings separate from remediation, runtime implementation, generator implementation, validator implementation, canon promotion, live-play authorization, and training authorization.

### Guardrails reaffirmed
- Wave 1 audit report only.
- No doctrine rewrite.
- No runtime implementation.
- No generator implementation.
- No validator implementation.
- No canon promotion.
- No live-play/training authorization.

## 2026-06-05 decision log - Runtime Boundary + Generator Ownership Remediation Priority Ledger

- Decision ID: REMEDIATION-PRIORITY-LEDGER-001
- Decision date: 2026-06-05
- Decision type: remediation-priority planning ledger

### Summary
- Added `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` as a planning-only consolidation of AUDIT-001, AUDIT-WAVE1-001, and AUDIT-WAVE2-001 findings.
- The ledger pauses audit expansion after Waves 1-2 and ranks recurring critical/high-risk seams into ordered remediation tracks and a recommended separate-PR sequence.
- The ledger does not change the accepted audit findings or add remediation implementation.

### Governance effect
- Converts accepted audit findings into owner-track planning without performing Wave 3.
- Keeps remediation planning separate from doctrine rewrite, runtime implementation, schema implementation, command IR implementation, generator implementation, validator implementation, persistence writer implementation, context-packet compiler implementation, canon promotion, live-play/training authorization, and donor-content audit.
- Requires future remediation to occur through separate scoped PRs.

### Guardrails reaffirmed
- Remediation-priority planning ledger only.
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No generator implementation.
- No validator implementation.
- No persistence writer implementation.
- No context-packet compiler implementation.
- No canon promotion.
- No live-play/training authorization.
- No donor-content audit.
- Future remediation requires separate PRs.

## 2026-06-05 decision log - PR-A RT-001 and RT-011 remediation owner scaffolds

- Decision ID: REMEDIATION-PR-A-OWNER-SCAFFOLDS-001
- Decision date: 2026-06-05
- Decision type: remediation owner-scaffold planning

### Summary
- Added `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` for RT-001 command lifecycle, action legality, and cost commitment owner-boundary planning.
- Added `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` for RT-011 validation/readiness tooling owner-boundary planning.
- PR-A follows `REMEDIATION-PRIORITY-LEDGER-001` by creating owner scaffolds only and not implementing remediation.

### Governance effect
- Establishes planning/control owner boundaries for RT-001 and RT-011 so later remediation can proceed through separate scoped PRs.
- Reaffirms that prose readiness, owner scaffolds, and model assertions are not executable validation, runtime gates, command IR, approval automation, live-play authorization, training authorization, or canon promotion.

### Guardrails reaffirmed
- Owner scaffold only.
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No persistence writer implementation.
- No context-packet compiler implementation.
- No canon promotion.
- No live-play/training authorization.
- No donor-content audit.

## 2026-06-05 decision log - PR-B RT-002 and RT-003 remediation owner scaffolds

- Decision ID: REMEDIATION-PR-B-OWNER-SCAFFOLDS-001
- Decision date: 2026-06-05
- Decision type: remediation owner-scaffold planning

### Summary
- Added `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` for RT-002 resource, backlash, corruption, strain, and consequence math owner-boundary planning.
- Added `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md` for RT-003 combat, hazard exposure, damage, injury, and recovery owner-boundary planning.
- PR-B follows `REMEDIATION-PRIORITY-LEDGER-001` by creating owner scaffolds only and not implementing remediation.

### Governance effect
- Establishes planning/control owner boundaries for RT-002 and RT-003 so later remediation can proceed through separate scoped PRs.
- Reaffirms that owner scaffolds and model assertions are not formulas, damage tables, schemas, command IR, validators, runtime gates, generators, persistence writers, context-packet compilers, live-play authorization, training authorization, or canon promotion.

### Guardrails reaffirmed
- Owner scaffold only.
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No math implementation.
- No damage table implementation.
- No validator implementation.
- No generator implementation.
- No persistence writer implementation.
- No context-packet compiler implementation.
- No canon promotion.
- No live-play/training authorization.
- No donor-content audit.

## 2026-06-05 — PR-C RT-005 context-packet / hidden-information owner scaffold

Decision: Add PR-C as owner-scaffold planning only for `REMEDIATION-RT005-CONTEXT-PACKET-HIDDEN-INFORMATION-OWNER-SCAFFOLD-001`, covering RT-005 scene/activity orchestration and hidden-information/context-packet boundaries.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no narration validator implementation, no live-play prompt implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

## 2026-06-05 — PR-D RT-008 generated-content and RT-012 D-series promotion-boundary owner scaffolds

Decision: Add PR-D as owner-scaffold planning only for `REMEDIATION-RT008-GENERATED-CONTENT-PROVENANCE-RECURRENCE-OWNER-SCAFFOLD-001` and `REMEDIATION-RT012-D-SERIES-PROMOTION-BOUNDARY-OWNER-SCAFFOLD-001`, covering RT-008 generated-content provenance/recurrence/durable-record eligibility and RT-012 D-series/native-design source-pack promotion boundaries.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no generated-record creation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no source-pack promotion, no sourcebook inclusion, no canon promotion, no live-play/training authorization, and no donor-content audit.

## 2026-06-05 — PR-E RT-004 ability/effect and RT-007 social/faction owner scaffolds

Decision: Add PR-E as owner-scaffold planning only for `REMEDIATION-RT004-ABILITY-EFFECT-SKILL-BINDING-OWNER-SCAFFOLD-001` and `REMEDIATION-RT007-SOCIAL-FACTION-KNOWLEDGE-STATE-OWNER-SCAFFOLD-001`, covering RT-004 ability/effect/cost/cooldown/skill/advancement binding boundaries and RT-007 social/faction/relationship/actor-knowledge/institutional-state boundaries.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no generated ability creation, no advancement award, no relationship mutation, no faction action commitment, no actor-knowledge database implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

## 2026-06-05 — PR-F RT-006 mission/reward/clue and RT-009 RNG/table/oracle owner scaffolds

Decision: Add PR-F as owner-scaffold planning only for `REMEDIATION-RT006-MISSION-REWARD-CLUE-ROUTING-OWNER-SCAFFOLD-001` and `REMEDIATION-RT009-RUNTIME-RNG-TABLE-ORACLE-OWNER-SCAFFOLD-001`, covering RT-006 mission/reward/clue/hidden-truth/consequence routing boundaries and RT-009 runtime RNG/table/oracle/seed/replay/hidden-result boundaries.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no mission generation, no reward commitment, no clue reveal, no hidden-truth database implementation, no RNG implementation, no oracle/table roll implementation, no random table data creation, no persistence writer implementation, no replay verifier implementation, no retrieval index implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

## 2026-06-05 — PR-G RT-010 inventory/item/vehicle persistent asset owner scaffold

Decision: Add PR-G as owner-scaffold planning only for `REMEDIATION-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SCAFFOLD-001`, covering RT-010 inventory, item, gear, vehicle, platform, installable, custody, and persistent asset-state boundaries.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no inventory implementation, no item instance creation, no durable asset record creation, no item effect implementation, no vehicle/platform runtime implementation, no cargo or crew system implementation, no repair/salvage/crafting implementation, no ownership/custody mutation, no charge/ammo/fuel/durability/cooldown spend, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

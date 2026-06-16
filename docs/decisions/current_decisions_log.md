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

Decision: Add PR-G as owner-scaffold planning only for `REMEDIATION-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SCAFFOLD-001`, covering RT-010 inventory, item, gear, vehicle, platform, installable, and persistent asset state boundaries. PR-G follows `REMEDIATION-PRIORITY-LEDGER-001` by creating the owner scaffold after command, cost, provenance, and consequence scaffolds (PR-A through PR-F) exist.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no inventory implementation, no item instance creation, no durable asset record creation, no item effect implementation, no vehicle/platform runtime implementation, no cargo or crew system implementation, no repair/salvage/crafting implementation, no ownership/custody mutation, no charge/ammo/fuel/durability/cooldown spend, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

## 2026-06-06 — Scaffold completion review and Stage 2 planning ledger

Decision: Add completion-review and Stage 2 planning tracking for `REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001`, covering `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`. This artifact verifies the RT-001 through RT-012 owner-scaffold pass, identifies gaps, overlaps, readiness classifications, and Stage 2 PR sequence, and recommends exactly one next PR.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no live-play prompt implementation, no training authorization, no donor-content audit, and no canon promotion.

## 2026-06-06 — Stage 2 PR-A RT-001 command lifecycle owner specification

Decision: Add Stage 2 owner-specification planning for `REMEDIATION-STAGE2-RT001-COMMAND-LIFECYCLE-OWNER-SPEC-001`, covering `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`. This artifact is STAGE2-PR-A owner-specification planning only. It upgrades the RT-001 scaffold into owner-spec planning for command lifecycle, action legality, cost commitment timing, command/event boundaries, validation handoffs, context/narration handoffs, and downstream dependency obligations.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no RNG/dice/table implementation, no event ledger implementation, no database schema, no live-play prompt implementation, no training authorization, no donor-content audit, and no canon promotion.

## 2026-06-06 — Stage 2 PR-B RT-011 validation/readiness owner specification

Decision: Add Stage 2 owner-specification planning for `REMEDIATION-STAGE2-RT011-VALIDATION-READINESS-OWNER-SPEC-001`, covering `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`. This artifact is STAGE2-PR-B owner-specification planning only. It upgrades the RT-011 scaffold into owner-spec planning for validation/readiness governance, prose-vs-executable validation boundaries, readiness classifications, future validator requirement inventory, reviewer decision records, non-implementation guardrail checks, registry/file tracking expectations, and RT-001 through RT-012 dependency handoffs.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no RNG/dice/table implementation, no event ledger implementation, no database schema, no live-play prompt implementation, no training authorization, no donor-content audit, no sourcebook inclusion authorization, no pilot conversion authorization, and no canon promotion.

## 2026-06-06 — Stage 2 PR-C RT-002 resource/consequence math owner specification

Decision: Add Stage 2 owner-specification planning for `REMEDIATION-STAGE2-RT002-RESOURCE-CONSEQUENCE-MATH-OWNER-SPEC-001`, covering `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`. This artifact is STAGE2-PR-C owner-specification planning only. It upgrades the RT-002 scaffold into owner-spec planning for resource/consequence math governance, cost/backlash/corruption/strain/reward/loss boundaries, failed-command cost outcome requirements, downstream handoffs, future math artifact inventory, validation requirements, and LLM non-authority rules.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no RNG/dice/table implementation, no event ledger implementation, no database schema, no resource formula, no resource pool list, no cost table, no damage table, no reward economy, no live-play prompt implementation, no training authorization, no donor-content audit, no sourcebook inclusion authorization, no pilot conversion authorization, and no canon promotion.

## 2026-06-06 — Stage 2 PR-D RT-005 context-packet/hidden-information owner specification

Decision: Add Stage 2 owner-specification planning for `REMEDIATION-STAGE2-RT005-CONTEXT-PACKET-HIDDEN-INFORMATION-OWNER-SPEC-001`, covering `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md`. This artifact is STAGE2-PR-D owner-specification planning only. It upgrades the RT-005 scaffold into owner-spec planning for context-packet projection, visible/hidden/redacted/derived/reviewer-only information partitions, player-known and actor/faction-known fact boundaries, rumor/false-claim/dialogue-summary separation, hidden-result routing, narrator allowed/forbidden fact sets, downstream handoffs, future context/visibility artifact inventory, validation requirements, and LLM non-authority rules.

Guardrails: This decision authorizes no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no redaction algorithm implementation, no narration validator implementation, no hidden-state database, no actor-knowledge database, no memory system, no RNG/dice/table implementation, no event ledger implementation, no database schema, no live-play prompt implementation, no training authorization, no donor-content audit, no canon promotion, no sourcebook inclusion authorization, and no pilot conversion authorization.

## 2026-06-06 — Stage 2 PR-E RT-008 generated-content provenance/recurrence owner specification

Decision: Add Stage 2 owner-specification planning for `REMEDIATION-STAGE2-RT008-GENERATED-CONTENT-PROVENANCE-RECURRENCE-OWNER-SPEC-001`, covering `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md`. This artifact is STAGE2-PR-E owner-specification planning only. It upgrades the RT-008 scaffold into owner-spec planning for generated-content provenance, source-local status, recurrence eligibility, durable-record eligibility, stable identifier requirements, review requirements, generator-disablement posture, provenance handoffs, context-packet projection handoffs, downstream consumer obligations, auditability requirements, and no-canon-promotion guardrails.

Guardrails: This decision authorizes no doctrine rewrite, no runtime code, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no procedural generation engine, no generated content records, no durable generated records, no stable ID allocator, no recurrence engine, no content writer, no persistence writer, no persistence writer implementation, no retrieval index, no retrieval index implementation, no context-packet compiler, no context-packet compiler implementation, no RNG/dice/table implementation, no event ledger implementation, no database schema, no live-play prompt, no live-play prompt implementation, no training data, no training authorization, no donor-content audit, no sourcebook inclusion authorization, no pilot conversion authorization, and no canon promotion.

## 2026-06-06 — Stage 2 PR-F RT-009 runtime RNG/table/oracle owner specification

Decision: Add Stage 2 owner-specification planning for `REMEDIATION-STAGE2-RT009-RNG-TABLE-ORACLE-OWNER-SPEC-001`, covering `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md`. This artifact is STAGE2-PR-F owner-specification planning only. It upgrades the RT-009 scaffold into owner-spec planning for backend-owned random authority, table/oracle invocation ownership, seed/replay reference requirements, result-domain validation, table-weight validation, hidden-result redaction handoffs, random-result commitment boundaries, oracle/table outcome narration projection, random dependency disclosure, and downstream owner obligations.

Guardrails: This decision authorizes no doctrine rewrite, no runtime code, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no RNG implementation, no dice roller, no table roller, no oracle engine, no table data, no table schema, no result-domain schema, no seed service, no replay verifier, no table-weight validator, no random-result event schema, no persistence writer, no persistence writer implementation, no retrieval index, no retrieval index implementation, no context-packet compiler, no context-packet compiler implementation, no redaction algorithm, no redaction algorithm implementation, no event ledger implementation, no database schema, no live-play prompt, no live-play prompt implementation, no training data, no training authorization, no donor-content audit, no sourcebook inclusion authorization, no pilot conversion authorization, and no canon promotion.

## 2026-06-06 — Stage 2 PR-G1 RT-003 combat/hazard/damage/recovery owner specification

Decision: Add Stage 2 owner-specification planning for `REMEDIATION-STAGE2-RT003-COMBAT-HAZARD-DAMAGE-RECOVERY-OWNER-SPEC-001`, covering `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md`. This artifact is STAGE2-PR-G1 owner-specification planning only, split from the original STAGE2-PR-G downstream-domain bundle for review safety. It upgrades the RT-003 scaffold into owner-spec planning for combat/hazard/damage/recovery ownership boundaries, active-threat and hazard-contact boundary requirements, damage-family and injury-family requirement boundaries, recovery/mitigation/exposure/ongoing-harm requirement boundaries, combat/hazard consequence handoff requirements, encounter-state pressure boundaries, and downstream owner handoffs.

Guardrails: This decision authorizes no doctrine rewrite, no runtime code, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no combat rules, no hazard rules, no damage formulas, no injury tables, no condition system, no healing/recovery formulas, no mitigation math, no exposure clocks, no active-threat runtime, no initiative/action economy, no encounter runtime, no vehicle/platform damage system, no item durability system, no armor/resistance/soak rules, no death/dying rules, no monster/NPC combat schema, no hazard schema, no RNG/dice/table implementation, no event ledger implementation, no database schema, no persistence writer, no persistence writer implementation, no retrieval index, no retrieval index implementation, no context-packet compiler, no context-packet compiler implementation, no live-play prompt, no live-play prompt implementation, no training data, no training authorization, no donor-content audit, no sourcebook inclusion authorization, no pilot conversion authorization, and no canon promotion.

## 2026-06-06 — Stage 2 PR-G2 RT-004 ability/effect/skill binding owner specification

Decision: Add Stage 2 owner-specification planning for `REMEDIATION-STAGE2-RT004-ABILITY-EFFECT-SKILL-BINDING-OWNER-SPEC-001`, covering `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md`. This artifact is STAGE2-PR-G2 owner-specification planning only, split from the original STAGE2-PR-G downstream-domain bundle for review safety. It upgrades the RT-004 scaffold into owner-spec planning for ability/effect/skill binding ownership boundaries, capability binding requirements, effect-family and effect-output requirement boundaries, skill/proficiency/competency/access binding boundaries, prerequisite and eligibility boundaries, targeting/range/area/duration/cooldown/recharge/sustain/interrupt/resistance/scaling/advancement-linked binding boundaries, item/relic/implant/vehicle/asset effect handoffs, generated ability/effect provenance handoffs, hidden prerequisite visibility handoffs, effect resolution handoffs, and downstream owner obligations.

Guardrails: This decision authorizes no doctrine rewrite, no runtime code, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no ability system, no effect taxonomy, no skill system, no proficiency/competency system, no prerequisite system, no targeting rules, no range/area rules, no duration rules, no cooldown/recharge/sustain rules, no interrupt/counter rules, no resistance/save/check rules, no scaling/rank/tier rules, no advancement unlock rules, no item/relic/implant effect rules, no companion/summon effect rules, no vehicle/platform effect rules, no ability schema, no skill schema, no effect schema, no condition schema, no damage formulas, no resource formulas, no RNG/dice/table implementation, no event ledger implementation, no database schema, no persistence writer, no persistence writer implementation, no retrieval index, no retrieval index implementation, no context-packet compiler, no context-packet compiler implementation, no live-play prompt, no live-play prompt implementation, no training data, no training authorization, no donor-content audit, no sourcebook inclusion authorization, no pilot conversion authorization, and no canon promotion.

## 2026-06-06 — Stage 2 PR-G3 RT-006 mission/reward/clue routing owner specification

Decision: Add Stage 2 owner-specification planning for `REMEDIATION-STAGE2-RT006-MISSION-REWARD-CLUE-ROUTING-OWNER-SPEC-001`, covering `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md`. This artifact is STAGE2-PR-G3 owner-specification planning only, split from the original STAGE2-PR-G downstream-domain bundle for review safety. It upgrades the RT-006 scaffold into owner-spec planning for mission/reward/clue routing ownership boundaries, mission/scenario/adventure/objective/branch/route/escalation/reward/penalty/success/failure/clue/hidden-truth routing requirement boundaries, objective-state and scenario-branch requirement boundaries, clue visibility and hidden-truth handoffs, reward/penalty/loss/consequence routing, generated mission provenance, random mission/clue/reward dependencies, and downstream owner obligations.

Guardrails: This decision authorizes no doctrine rewrite, no runtime code, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no mission system, no quest system, no scenario engine, no adventure runtime, no objective state machine, no branch engine, no clue reveal algorithm, no investigation rules, no hidden-truth reveal procedure, no reward economy, no mission reward tables, no failure/success tables, no route planner, no escalation clocks, no campaign clocks, no mission schema, no clue schema, no reward schema, no objective schema, no scenario state schema, no RNG/dice/table implementation, no event ledger implementation, no database schema, no persistence writer, no persistence writer implementation, no retrieval index, no retrieval index implementation, no context-packet compiler, no context-packet compiler implementation, no live-play prompt, no live-play prompt implementation, no training data, no training authorization, no donor-content audit, no sourcebook inclusion authorization, no pilot conversion authorization, and no canon promotion.

## 2026-06-06 — Stage 2 PR-G4 RT-007 social/faction/actor-knowledge owner specification

Decision: Add Stage 2 owner-specification planning for `REMEDIATION-STAGE2-RT007-SOCIAL-FACTION-ACTOR-KNOWLEDGE-OWNER-SPEC-001`, covering `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md`. This artifact is STAGE2-PR-G4 owner-specification planning only, split from the original STAGE2-PR-G downstream-domain bundle for review safety. It upgrades the RT-007 scaffold into owner-spec planning for social/faction/actor-knowledge ownership boundaries, actor knowledge, belief, rumor, false claim, verified fact, witness state, institutional knowledge routing, faction standing, reputation, relationship, influence, contact, patron, rival, obligation, debt, favor, oath, threat, blackmail, social consequence, faction response, institutional response, and downstream owner obligations.

Guardrails: This decision authorizes no doctrine rewrite, no runtime code, no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no social system, no faction system, no reputation system, no relationship engine, no influence system, no contact system, no dialogue system, no actor-knowledge database, no faction-knowledge database, no rumor system, no belief-state engine, no deception rules, no witness system, no obligation/debt economy, no favor economy, no faction clocks, no institutional clocks, no patron/rival system, no social schema, no faction state schema, no actor-knowledge schema, no reputation schema, no relationship schema, no contact schema, no RNG/dice/table implementation, no event ledger implementation, no database schema, no persistence writer, no persistence writer implementation, no retrieval index, no retrieval index implementation, no context-packet compiler, no context-packet compiler implementation, no live-play prompt, no live-play prompt implementation, no training data, no training authorization, no donor-content audit, no sourcebook inclusion authorization, no pilot conversion authorization, and no canon promotion.

## 2026-06-06 decision log - STAGE2-PR-H RT-010 / RT-012 deferred convergence plan

- Decision ID: REMEDIATION-STAGE2-RT010-RT012-DEFERRED-CONVERGENCE-PLAN-001
- Decision date: 2026-06-06
- Decision type: runtime-boundary/deferred-convergence-planning

### Summary
- Added STAGE2-PR-H deferred convergence planning for RT-010 and RT-012 at `docs/doctrine/reviews/runtime_boundary_generator_ownership_stage2_rt010_rt012_deferred_convergence_plan.md`.
- This is a Stage 2 deferred convergence plan only; it covers RT-010 and RT-012 and recommends separate future owner-specification sequencing for RT-010 inventory/item/vehicle/asset planning and RT-012 D-series/native-design promotion-boundary planning.
- This record does not create RT-010 owner specification and does not create RT-012 owner specification.

### Guardrails reaffirmed
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No inventory system.
- No item system.
- No vehicle system.
- No asset system.
- No durability system.
- No repair system.
- No salvage system.
- No crafting system.
- No requisition system.
- No cargo/custody system.
- No ownership system.
- No persistent asset state.
- No persistent ID allocator.
- No D-series promotion system.
- No native-design promotion system.
- No canon promotion procedure.
- No sourcebook inclusion procedure.
- No training policy.
- No RNG/dice/table implementation.
- No event ledger implementation.
- No database schema.
- No persistence writer implementation.
- No retrieval index implementation.
- No context-packet compiler implementation.
- No live-play prompt implementation.
- No training authorization.
- No donor-content audit.
- No sourcebook inclusion authorization.
- No pilot conversion authorization.
- No canon promotion.

## 2026-06-06 decision log - STAGE2-CLOSURE-REVIEW completion review and closure ledger

- Decision ID: REMEDIATION-STAGE2-COMPLETION-REVIEW-CLOSURE-LEDGER-001
- Decision date: 2026-06-06
- Decision type: runtime-boundary/stage2-completion-review-closure-ledger

### Summary
- Added the Stage 2 completion review and remediation closure ledger at `docs/doctrine/reviews/runtime_boundary_generator_ownership_stage2_completion_review_and_closure_ledger.md`.
- This is a Stage 2 completion review / closure ledger only. It verifies RT-001 through RT-009 and RT-011 owner-spec planning and records RT-010 and RT-012 as deferred through the STAGE2-PR-H convergence plan.
- It does not create RT-010 owner specification and does not create RT-012 owner specification.

### Guardrails reaffirmed
- No doctrine rewrite.
- No RT-010 owner specification.
- No RT-012 owner specification.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No inventory system.
- No item system.
- No vehicle system.
- No asset system.
- No D-series promotion system.
- No native-design promotion system.
- No canon promotion procedure.
- No sourcebook inclusion procedure.
- No training policy.
- No RNG/dice/table implementation.
- No event ledger implementation.
- No database schema.
- No persistence writer implementation.
- No retrieval index implementation.
- No context-packet compiler implementation.
- No live-play prompt implementation.
- No training authorization.
- No donor-content audit.
- No sourcebook inclusion authorization.
- No pilot conversion authorization.
- No canon promotion.

## 2026-06-06 decision log - STAGE2-PR-H1 RT-010 inventory/item/vehicle/asset owner specification

- Decision ID: REMEDIATION-STAGE2-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SPEC-001
- Decision date: 2026-06-06
- Decision type: runtime-boundary/stage2-owner-specification-planning

### Summary
- Added the STAGE2-PR-H1 RT-010 inventory/item/vehicle/asset owner specification at `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md`.
- This is STAGE2-PR-H1 owner-specification planning only, resolves RT-010 deferred owner-specification gap identified by STAGE2-PR-H and STAGE2-CLOSURE-REVIEW, and repeats the no-implementation guardrails.
- It upgrades the RT-010 scaffold into owner-spec planning for inventory, items, gear, relics, implants, installables, vehicles, ships, platforms, companions, summons, cargo, maps/routes, custody, ownership, ammo, fuel, charges, durability, degradation, repair, salvage, crafting, requisition, loadout, storage, transfer, hidden properties, asset rewards, asset losses, generated asset provenance, random loot/salvage dependencies, and persistent asset-state handoffs.

### Guardrails reaffirmed
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No inventory system.
- No item system.
- No gear system.
- No relic/implant/installable system.
- No vehicle/ship/platform system.
- No companion/summon asset system.
- No cargo/custody system.
- No ownership system.
- No loadout/storage/transfer system.
- No ammo/fuel/charge system.
- No durability/degradation system.
- No repair/salvage system.
- No crafting/requisition system.
- No asset economy.
- No price/value/salvage/requisition tables.
- No persistent asset state.
- No persistent ID allocator.
- No asset event schema.
- No item schema.
- No vehicle schema.
- No cargo schema.
- No crafting schema.
- No RNG/dice/table implementation.
- No event ledger implementation.
- No database schema.
- No persistence writer implementation.
- No retrieval index implementation.
- No context-packet compiler implementation.
- No live-play prompt implementation.
- No training authorization.
- No donor-content audit.
- No sourcebook inclusion authorization.
- No pilot conversion authorization.
- No canon promotion.

## 2026-06-06 decision log - STAGE2-PR-H2 RT-012 D-series/native-design promotion-boundary owner specification

- Decision ID: REMEDIATION-STAGE2-RT012-D-SERIES-PROMOTION-BOUNDARY-OWNER-SPEC-001
- Decision date: 2026-06-06
- Decision type: runtime-boundary/stage2-owner-specification-planning

### Summary
- Added the STAGE2-PR-H2 RT-012 D-series/native-design promotion-boundary owner specification at `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md`.
- This is STAGE2-PR-H2 owner-specification planning only, resolves RT-012 deferred owner-specification gap identified by STAGE2-PR-H and STAGE2-CLOSURE-REVIEW, and repeats the no-implementation guardrails.
- It upgrades the RT-012 scaffold into owner-spec planning for D-series/native-design promotion-boundary ownership requirements, source-pack material as pressure, native-design claim routing, doctrine-to-sourcebook promotion handoffs, canon/sourcebook candidate separation, runtime-owner handoffs, rejection/quarantine of unpromoted content, reviewer decision requirements, conflict routing, no-automatic-promotion boundaries, live-play/training exclusion, and auditability.

### Guardrails reaffirmed
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No D-series promotion system.
- No native-design promotion system.
- No canon promotion procedure.
- No sourcebook inclusion procedure.
- No training policy.
- No live-play policy.
- No doctrine rewrite procedure.
- No source-pack ingestion procedure.
- No example-pack promotion procedure.
- No converted-content promotion procedure.
- No generated-content promotion procedure.
- No promotion records.
- No canon records.
- No sourcebook records.
- No reviewer workflow implementation.
- No RNG/dice/table implementation.
- No event ledger implementation.
- No database schema.
- No persistence writer implementation.
- No retrieval index implementation.
- No context-packet compiler implementation.
- No live-play prompt implementation.
- No training authorization.
- No donor-content audit.
- No sourcebook inclusion authorization.
- No pilot conversion authorization.
- No canon promotion.

## 2026-06-07 decision log - RUNTIME-SEQ-PR-F implementation-readiness review and first executable-kernel authorization gate

- Decision ID: RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001
- Decision date: 2026-06-07
- Decision type: implementation-readiness-review-and-authorization-gate

### Summary
- Added `docs/doctrine/reviews/runtime_seq_pr_f_implementation_readiness_executable_kernel_authorization_gate.md` as a planning-only implementation-readiness review and first executable-kernel authorization gate.
- This is RUNTIME-SEQ-PR-F planning/review only. It confirms owner-spec (RT-001 through RT-012) and RUNTIME-SEQ-PR-A through PR-E coverage is sufficient for a future minimum backend kernel implementation-plan PR.
- Incorporates the backend-first/model-interchangeability invariant: the LLM is not the game engine; the backend runtime kernel owns truth.
- Includes readiness criteria matrix (19 criteria), implementation authorization gate finding, first executable kernel target definition (14 plan items), runtime stack decision review, storage and persistence decision review, minimum viable implementation sequence (RUNTIME-IMPL-PR-0 through PR-7), guardrail integrity review, blocked-until ledger, risk review (14 risks), future implementation test strategy (17 test families), and authorization boundary for RUNTIME-IMPL-PR-0.
- Gate finding: implementation readiness for planning is ready; executable runtime implementation is not authorized by this PR; next step authorized is RUNTIME-IMPL-PR-0 (minimum backend kernel executable implementation plan).
- Recommends RUNTIME-IMPL-PR-0 as the next step.

### Governance effect
- Establishes the implementation-readiness gate for the transition from planning-only runtime sequence into future implementation planning.
- Reaffirms the backend-first model-interchangeability invariant: the LLM is not the game engine; the backend runtime kernel owns truth.
- Confirms all 12 owner specifications and all 5 runtime sequencing plans provide sufficient planning depth.
- Identifies blocked-until conditions for runtime, schemas, validators, generators, domain services, live-play, training, conversion, sourcebook inclusion, and canon promotion.

### Guardrails reaffirmed
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No state store.
- No state delta model.
- No event ledger.
- No transaction system.
- No invariant validator.
- No correction event schema.
- No deterministic RNG service.
- No table/oracle service.
- No persistence writer.
- No database schema.
- No context-packet compiler.
- No redaction algorithm.
- No hidden-state database.
- No domain service.
- No model evaluation code.
- No benchmark runner.
- No prompt templates.
- No live-play adapter.
- No training authorization.
- No donor-content audit.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

## 2026-06-06 decision log - RUNTIME-SEQ-PR-E model evaluation, structured-output, and adversarial-command plan

- Decision ID: RUNTIME-SEQ-PR-E-MODEL-EVALUATION-STRUCTURED-OUTPUT-ADVERSARIAL-COMMAND-PLAN-001
- Decision date: 2026-06-06
- Decision type: model-evaluation-structured-output-adversarial-command-plan

### Summary
- Added `docs/doctrine/reviews/runtime_seq_pr_e_model_evaluation_structured_output_adversarial_command_plan.md` as a planning-only model evaluation, structured-output, and adversarial-command plan.
- This is RUNTIME-SEQ-PR-E planning only. It defines model role taxonomy, ModelBehaviorFingerprint contract, role qualification contract, structured-output contract, SchemaKeyBehaviorEvaluationPolicy, TruncationSafeStructuredOutputPolicy, AdversarialPlayerCommandCorpus plan, MetamorphicRuntimeNarrationTestPlan, local/cloud model comparison contract, FailureModeRoutingContract, evaluation packet and trace requirements, and ModelRoleEligibilityLedger.
- Incorporates the backend-first/model-interchangeability invariant: the LLM is not the game engine; the backend runtime kernel owns truth.
- No model is trusted because it is powerful, fluent, or aesthetically good. A model is eligible for a role only if future evaluation proves it can obey the role's packet contract, output contract, hidden-information limits, structured-output constraints, and non-authority boundaries.
- Recommends RUNTIME-SEQ-PR-F (implementation-readiness review and first executable-kernel authorization gate) as the next planning step.

### Governance effect
- Establishes the planning framework for model evaluation, structured-output validation, and adversarial-command testing without performing implementation.
- Reaffirms the backend-first model-interchangeability invariant and all non-implementation guardrails from prior planning artifacts.

### Guardrails reaffirmed
- No doctrine rewrite.
- No model evaluation code.
- No benchmark runner.
- No prompt templates.
- No model routing.
- No model adapter.
- No structured-output schema.
- No schema-key validator.
- No adversarial test harness.
- No metamorphic test runner.
- No model behavior fingerprint implementation.
- No role eligibility ledger implementation.
- No training data.
- No fine-tuning.
- No runtime implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No state store implementation.
- No event ledger implementation.
- No context-packet compiler implementation.
- No redaction algorithm.
- No live-play adapter.
- No donor-content audit.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

## 2026-06-06 decision log - RUNTIME-SEQ-PR-D story-capable structure and playable-content plan

- Decision ID: RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001
- Decision date: 2026-06-06
- Decision type: story-capable-structure-playable-content-plan

### Summary
- Added `docs/doctrine/reviews/runtime_seq_pr_d_story_capable_structure_playable_content_plan.md` as a planning-only story-capable structure and playable-content plan.
- This is RUNTIME-SEQ-PR-D planning only. It defines the story-capable structure principle, playable-content boundary (PlayableSceneStructure, NarrativeSubstrate, SceneObjectContract, StoryletContract, ScenarioNodeContract, QuestScenarioDependencyDAG, PlayabilityProofContract, PlayerAgencyAffordanceSet, ConsequenceRouteContract, FailurePartialSuccessContract, EscalationHookContract, ClueRoutePlayableContract, RewardRoutePlayableContract, SocialContactPlayableContract, HazardPressurePlayableContract, SourceLocalCapsulePlayableBoundary), playability proof contract, narrative substrate contract, storylet contract, quest/scenario dependency DAG contract, NPC goal stack and actor-intent planning contract (NPCGoalStack, ActorIntentContract), DialogueActIR planning contract, content ecology contract (ContentEcologyContract), source-local capsule boundary expansion, generator-to-validate-to-commit pipeline, minimum viable scene object contract (MinimumViableSceneObject), runtime/narration handoff, runtime/event handoff, and domain handoff crosswalk (RT-001 through RT-012).
- Primary owner tracks: RT-006 (mission/scenario/clue/reward routing), RT-007 (social/faction/actor knowledge), RT-008 (generated-content provenance/recurrence), RT-011 (validation/readiness tooling), and RT-012 (D-series/native-design promotion boundary).
- Recommends RUNTIME-SEQ-PR-E (model evaluation, structured-output, and adversarial-command plan) as the next planning step.

### Governance effect
- Establishes the planning framework for story-capable structure and playable-content contracts without performing implementation.
- Reaffirms the backend-first model-interchangeability invariant: the LLM is not the game engine; the backend runtime kernel owns truth.
- Defines that playable content must be backend-owned structure before it is narrated; the LLM may propose or render but must not create durable story truth, decide quest state, mutate NPC goals, create clues, assign rewards, promote source-local content, or commit scenario consequences.

### Guardrails reaffirmed
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No storylet system.
- No narrative substrate schema.
- No playable-content validator.
- No quest engine.
- No scenario engine.
- No dependency DAG engine.
- No NPC AI.
- No behavior tree.
- No dialogue system.
- No DialogueActIR implementation.
- No content ecology engine.
- No generator implementation.
- No repair loop.
- No evaluator/judge implementation.
- No command IR implementation.
- No validator implementation.
- No state store implementation.
- No event ledger implementation.
- No context-packet compiler implementation.
- No prompt templates.
- No live-play adapter.
- No training authorization.
- No donor-content audit.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

## 2026-06-06 decision log - RUNTIME-SEQ-PR-C state/event/invariant/transaction plan

- Decision ID: RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001
- Decision date: 2026-06-06
- Decision type: state-event-invariant-transaction-plan

### Summary
- Added `docs/doctrine/reviews/runtime_seq_pr_c_state_event_invariant_transaction_plan.md` as a planning-only state/event/invariant/transaction plan.
- This is RUNTIME-SEQ-PR-C planning only. It defines the state/event boundary (BackendStateStore, StateProjection, TransactionPreview, StateDeltaEnvelope, EventLedgerEntry, RuntimeTrace, NarrationDisplayOutput, SummaryArtifact, CorrectionEvent), transaction lifecycle contract (18 normal stages, 7 rejection/quarantine stages), transaction preview contract, StateDeltaEnvelope planning contract (15 field families), EventLedgerEntry planning contract (16 field families, 11 event-family categories), event-channel boundaries (9 channels), WorldInvariantRegistry planning contract (13 invariant categories), rollback-safe validation order (14 validation stages), CorrectionEventProtocol planning principles, replay/hash/audit requirements (11 requirement families), RuntimeTrace requirements (17 per-turn trace fields), LLM non-authority rules, and domain handoff crosswalk (RT-001 through RT-012).
- Primary owner tracks: RT-001 (command lifecycle/event commitment boundary) and RT-011 (validation/readiness tooling).
- Recommends RUNTIME-SEQ-PR-D (story-capable structure and playable-content plan) as the next planning step.

### Governance effect
- Establishes the planning framework for state/event/invariant/transaction contracts without performing implementation.
- Reaffirms the backend-first model-interchangeability invariant: the LLM is not the game engine; the backend runtime kernel owns truth.
- Defines that only backend-owned systems may create durable truth; narration, summaries, and model outputs are not committed state.

### Guardrails reaffirmed
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No state store implementation.
- No state delta model implementation.
- No event ledger implementation.
- No transaction preview implementation.
- No rollback implementation.
- No invariant validator.
- No correction event schema.
- No replay/hash service.
- No runtime trace implementation.
- No persistence writer implementation.
- No database schema.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No context-packet compiler implementation.
- No redaction algorithm.
- No RNG/table/oracle implementation.
- No domain runtime service.
- No live-play adapter.
- No training authorization.
- No donor-content audit.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

## 2026-06-06 decision log - RUNTIME-SEQ-PR-B narration/context packet contract plan

- Decision ID: RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001
- Decision date: 2026-06-06
- Decision type: narration-context-packet-contract-plan

### Summary
- Added `docs/doctrine/reviews/runtime_seq_pr_b_narration_context_packet_contract_plan.md` as a planning-only narration/context packet contract plan.
- This is RUNTIME-SEQ-PR-B planning only. It defines the narration/context packet contract layer including packet layer separation (7 packet families), NarrationRenderPacket and ContextPacket planning contracts, visibility tiers, local 8B packet budget policy, narrator output contract, soft-state mutation detection requirements, missing-information policy, canonical silence and source-local/canon boundary notices, model role contracts, and packet assembly trace requirements.
- Primary owner tracks: RT-005 (context-packet/hidden-information) and RT-011 (validation/readiness tooling).
- Recommends RUNTIME-SEQ-PR-C (state/event/invariant/transaction plan) as the next planning step.

### Governance effect
- Establishes the planning framework for narration/context packet contracts without performing implementation.
- Reaffirms the backend-first model-interchangeability invariant: the LLM is not the game engine; the backend runtime kernel owns truth.
- Defines hidden information leakage as a hard failure.

### Guardrails reaffirmed
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No context-packet compiler implementation.
- No narration render packet schema implementation.
- No narrator output schema implementation.
- No redaction algorithm.
- No hidden-state database.
- No packet budget enforcement.
- No soft-state mutation validator.
- No model routing implementation.
- No prompt templates.
- No live-play adapter.
- No training authorization.
- No donor-content audit.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

## 2026-06-06 decision log - RUNTIME-SEQ-PR-A minimum backend kernel + runtime quality contract plan

- Decision ID: RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001
- Decision date: 2026-06-06
- Decision type: minimum-backend-kernel-runtime-quality-contract-plan

### Summary
- Added `docs/doctrine/reviews/runtime_seq_pr_a_minimum_backend_kernel_runtime_quality_contract_plan.md` as a planning-only bridge from runtime/schema implementation sequencing review toward future minimum backend kernel planning.
- This is RUNTIME-SEQ-PR-A planning only. It defines the minimum backend kernel spine (16 future artifact families) and the runtime-quality contract layer (15 future artifact families).
- Incorporates the backend-first/model-interchangeability invariant: the LLM is not the game engine; the backend runtime kernel owns truth.
- Includes local 8B reliability requirements, transaction preview and correction policy, world invariant and canonical silence requirements, observability and replay/debug requirements, minimum backend kernel target boundary, implementation wave alignment (Waves 0–6), and blocked-until ledger.
- Recommends staged follow-up PRs: RUNTIME-SEQ-PR-B through RUNTIME-SEQ-PR-E, then a separately authorized implementation-readiness review.

### Governance effect
- Establishes the planning framework for the minimum backend kernel spine and runtime-quality contracts without performing implementation.
- Reaffirms the backend-first model-interchangeability invariant and all non-implementation guardrails from prior planning artifacts.

### Guardrails reaffirmed
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No state store.
- No state delta model.
- No event ledger.
- No deterministic RNG service.
- No table/oracle service.
- No persistence writer implementation.
- No retrieval index implementation.
- No context-packet compiler implementation.
- No redaction algorithm.
- No hidden-state database.
- No domain runtime service.
- No campaign memory system.
- No live-play prompt implementation.
- No training authorization.
- No donor-content audit.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

## 2026-06-07 decision log - RUNTIME-IMPL-PR-0 Minimum Backend Kernel Executable Implementation Plan

- Decision ID: RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
- Decision date: 2026-06-07
- Decision type: minimum-backend-kernel-executable-implementation-plan

### Summary
- Added `docs/doctrine/reviews/runtime_impl_pr_0_minimum_backend_kernel_executable_implementation_plan.md` as a planning-only minimum backend kernel executable implementation plan.
- This plan defines the future implementation stack recommendation (Python/pytest), proposed package/module layout (src/astra_runtime/kernel/), minimum backend kernel target (14 interface skeletons), interface boundary plan (14 interfaces), RUNTIME-IMPL-PR-1 through PR-8 implementation sequence, RUNTIME-IMPL-PR-1 authorization boundary, kernel skeleton invariants, storage-neutral persistence plan, testing strategy, and implementation risk controls.
- Recommends RUNTIME-IMPL-PR-1 (Schema Registry and Record Identity Skeleton) as the next step.

### Governance effect
- Establishes the concrete implementation plan for the future minimum backend kernel without performing implementation.
- Reaffirms the backend-first model-interchangeability invariant: the LLM is not the game engine; the backend runtime kernel owns truth.
- Defines authorization boundary for RUNTIME-IMPL-PR-1 (schema registry and record identity skeleton only).

### Guardrails reaffirmed
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No state store.
- No state delta model.
- No event ledger.
- No transaction system.
- No invariant validator.
- No correction event schema.
- No deterministic RNG service.
- No table/oracle service.
- No persistence writer.
- No database schema.
- No context-packet compiler.
- No redaction algorithm.
- No hidden-state database.
- No domain service.
- No model evaluation code.
- No benchmark runner.
- No prompt templates.
- No live-play adapter.
- No training authorization.
- No donor-content audit.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

## 2026-06-06 decision log - Runtime/Schema Implementation Sequencing Review

- Decision ID: RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001
- Decision date: 2026-06-06
- Decision type: implementation-sequencing-review

### Summary
- Added `docs/doctrine/reviews/runtime_schema_implementation_sequencing_review.md` as a planning-only runtime/schema implementation sequencing review.
- This review confirms that RT-001 through RT-012 owner-specification planning is complete, defines an implementation dependency map, recommends twelve future implementation-planning waves (Wave 0 through Wave 11), and recommends RUNTIME-SEQ-PR-A (minimum backend kernel implementation plan) as the next planning step.
- Owner-boundary planning is not implementation readiness by itself; the project is ready for implementation sequencing, not immediate full runtime implementation.

### Governance effect
- Establishes the sequencing framework for future runtime/schema implementation without performing implementation.
- Reaffirms the backend-first model-interchangeability invariant: the LLM is not the game engine; the backend runtime kernel owns truth.
- Identifies blocked-until conditions for runtime, schemas, validators, generators, domain services, live-play, training, conversion, sourcebook inclusion, and canon promotion.

### Guardrails reaffirmed
- No doctrine rewrite.
- No runtime implementation.
- No schema implementation.
- No command IR implementation.
- No validator implementation.
- No generator implementation.
- No state store.
- No state delta model.
- No event ledger.
- No deterministic RNG service.
- No table/oracle service.
- No persistence writer implementation.
- No retrieval index implementation.
- No context-packet compiler implementation.
- No redaction algorithm.
- No hidden-state database.
- No domain runtime service.
- No campaign memory system.
- No live-play prompt implementation.
- No training authorization.
- No donor-content audit.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

## 2026-06-07 decision — RUNTIME-IMPL-PR-1 schema registry and record identity skeleton

- Decision ID: RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001
- Decision date: 2026-06-07
- Decision type: implementation/executable skeleton

### Summary

First narrow runtime code PR. Implements only schema registry and record identity skeletons under `src/astra_runtime/kernel/`. Follows RUNTIME-IMPL-PR-0 authorization. Preserves backend-first invariant. LLM is not the game engine.

### Reason

RUNTIME-IMPL-PR-0 authorized RUNTIME-IMPL-PR-1 as the first executable code step. The scope is narrowed to schema registry (in-memory type-key registry with immutability-safe copies) and record identity (deterministic `astra:<type>:<local_id>` format with strict character policy). No other kernel systems are implemented.

### Implication

- `src/astra_runtime/kernel/` package now exists with two modules.
- `pyproject.toml` added for editable install and pytest import resolution.
- 40 focused tests pass.
- No command/event/state/RNG/persistence/domain/model/live-play artifacts created.

### Revisit trigger

- If record ID format needs namespacing beyond `astra:<type>:<local_id>`.
- If schema registry needs file-backed loading for later PRs.
- If RUNTIME-IMPL-PR-2 (command envelope and transaction preview skeleton) is authorized.

### Classification block

```yaml
runtime_impl_pr_1:
  implementation_id: RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001
  artifact_type: executable_kernel_skeleton
  implementation_status: narrow_executable_skeleton
  derives_from:
    - RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
    - RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001
  implements_minimal_package_structure: true
  implements_schema_registry_skeleton: true
  implements_record_identity_skeleton: true
  authorizes_command_ir: false
  authorizes_transaction_preview: false
  authorizes_state_store: false
  authorizes_state_delta_model: false
  authorizes_event_ledger: false
  authorizes_rng_service: false
  authorizes_table_oracle_service: false
  authorizes_validation_pipeline: false
  authorizes_context_packet_compiler: false
  authorizes_hidden_information_partition: false
  authorizes_persistence_writer: false
  authorizes_database_schema: false
  authorizes_domain_services: false
  authorizes_generators: false
  authorizes_live_play: false
  authorizes_model_integration: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-IMPL-PR-2 command envelope and transaction preview skeleton, pending review
```

### No-implementation guardrails

- No command envelope module exists yet.
- No transaction preview module exists yet.
- No state delta module exists yet.
- No event ledger module exists yet.
- No RNG/table module exists yet.
- No persistence/database module exists yet.
- No context projection or hidden-information module exists yet.
- No domain service package exists yet.

## 2026-06-07 decision — RUNTIME-IMPL-PR-2 command envelope and transaction preview skeleton

- Decision ID: RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
- Decision date: 2026-06-07
- Decision type: implementation/executable skeleton

### Summary

Second narrow runtime code PR. Implements only command envelope and transaction preview skeletons under `src/astra_runtime/kernel/`. Follows RUNTIME-IMPL-PR-0 and PR-1 authorization. Preserves backend-first invariant. LLM is not the game engine.

### Reason

RUNTIME-IMPL-PR-1 authorized RUNTIME-IMPL-PR-2 as the next executable code step. The scope is narrowed to command envelope (immutable frozen dataclass with validation, copy-safe payload/metadata, `to_dict` conversion) and transaction preview (immutable frozen dataclass with restricted status set, message normalization, no state deltas, no event commitment). No other kernel systems are implemented.

### Implication

- `src/astra_runtime/kernel/command_envelope.py` now exists.
- `src/astra_runtime/kernel/transaction_preview.py` now exists.
- `src/astra_runtime/kernel/__init__.py` exports both modules.
- 60 focused tests pass (34 command envelope + 26 transaction preview).
- No state/event/RNG/persistence/domain/model/live-play artifacts created.

### Revisit trigger

- If command envelope needs additional fields for command lifecycle engine (PR-3+).
- If transaction preview needs state delta references (PR-3).
- If RUNTIME-IMPL-PR-3 (state delta and event ledger envelope skeleton) is authorized.

### Classification block

```yaml
runtime_impl_pr_2:
  implementation_id: RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
  artifact_type: executable_kernel_skeleton
  implementation_status: narrow_executable_skeleton
  derives_from:
    - RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
    - RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001
    - RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001
  implements_command_envelope_skeleton: true
  implements_transaction_preview_skeleton: true
  authorizes_command_lifecycle_engine: false
  authorizes_action_legality_engine: false
  authorizes_command_execution: false
  authorizes_state_store: false
  authorizes_state_delta_model: false
  authorizes_event_ledger: false
  authorizes_event_commitment: false
  authorizes_transaction_system: false
  authorizes_rollback: false
  authorizes_invariant_validator: false
  authorizes_correction_event_schema: false
  authorizes_rng_service: false
  authorizes_table_oracle_service: false
  authorizes_validation_pipeline: false
  authorizes_context_packet_compiler: false
  authorizes_hidden_information_partition: false
  authorizes_persistence_writer: false
  authorizes_database_schema: false
  authorizes_domain_services: false
  authorizes_generators: false
  authorizes_live_play: false
  authorizes_model_integration: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-IMPL-PR-3 state delta and event ledger envelope skeleton, pending review
```

### No-implementation guardrails

- No state delta module exists yet.
- No event ledger module exists yet.
- No RNG/table module exists yet.
- No persistence/database module exists yet.
- No context projection or hidden-information module exists yet.
- No domain service package exists yet.
- No model integration package exists yet.
- No prompt template package exists yet.

## 2026-06-07 decision — RUNTIME-IMPL-PR-3 state delta and event ledger envelope skeleton

- Decision ID: RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
- Decision date: 2026-06-07
- Decision type: implementation/executable skeleton

### Summary

Third narrow runtime code PR. Implements only state delta envelope and event ledger entry envelope skeletons under `src/astra_runtime/kernel/`. Follows RUNTIME-IMPL-PR-0 through PR-2 authorization. Preserves backend-first invariant. LLM is not the game engine.

### Reason

RUNTIME-IMPL-PR-2 authorized RUNTIME-IMPL-PR-3 as the next executable code step. The scope is narrowed to state delta envelope (immutable frozen dataclass with validation, allowed change types, affected record IDs, copy-safe payload/metadata, `to_dict` conversion) and event ledger entry (immutable frozen dataclass with allowed event types, non-negative sequence, state delta ID references, actor/target record ID validation, copy-safe metadata, `to_dict` conversion). No other kernel systems are implemented.

### Implication

- `src/astra_runtime/kernel/state_delta.py` now exists.
- `src/astra_runtime/kernel/event_ledger.py` now exists.
- `src/astra_runtime/kernel/__init__.py` exports both modules.
- 97 focused new tests pass (46 state delta + 51 event ledger).
- No state store/replay/RNG/persistence/domain/model/live-play artifacts created.

### Revisit trigger

- If state delta envelope needs additional fields for state application engine (PR-4+).
- If event ledger entry needs hash/replay fields for event store (PR-4+).
- If RUNTIME-IMPL-PR-4 (deterministic RNG and table/oracle interface skeleton) is authorized.

### Classification block

```yaml
runtime_impl_pr_3:
  implementation_id: RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
  artifact_type: executable_kernel_skeleton
  implementation_status: narrow_executable_skeleton
  derives_from:
    - RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
    - RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001
    - RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
    - RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001
  implements_state_delta_envelope_skeleton: true
  implements_event_ledger_entry_skeleton: true
  authorizes_mutable_state_store: false
  authorizes_state_application_engine: false
  authorizes_command_execution: false
  authorizes_command_lifecycle_engine: false
  authorizes_transaction_lifecycle_engine: false
  authorizes_rollback: false
  authorizes_event_store_persistence: false
  authorizes_database_schema: false
  authorizes_replay_hash_service: false
  authorizes_rng_service: false
  authorizes_table_oracle_service: false
  authorizes_validation_pipeline: false
  authorizes_invariant_validator: false
  authorizes_correction_event_schema: false
  authorizes_context_packet_compiler: false
  authorizes_hidden_information_partition: false
  authorizes_persistence_writer: false
  authorizes_domain_services: false
  authorizes_generators: false
  authorizes_live_play: false
  authorizes_model_integration: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-IMPL-PR-4 deterministic RNG and table/oracle interface skeleton, pending review
```

### No-implementation guardrails

- No RNG/table module exists yet.
- No validation pipeline module exists yet.
- No persistence/database module exists yet.
- No context projection or hidden-information module exists yet.
- No replay/audit module exists yet.
- No runtime trace module exists yet.
- No domain service package exists yet.
- No model integration package exists yet.
- No prompt template package exists yet.

## 2026-06-07 decision — RUNTIME-IMPL-PR-4 deterministic RNG and table/oracle interface skeleton

- Decision ID: RUNTIME-IMPL-PR-4-DETERMINISTIC-RNG-TABLE-ORACLE-INTERFACE-SKELETON-001
- Decision date: 2026-06-07
- Decision type: implementation/executable skeleton

### Summary

Fourth narrow runtime code PR. Implements only deterministic RNG interface and table/oracle interface skeletons under `src/astra_runtime/kernel/`. Follows RUNTIME-IMPL-PR-0 through PR-3 authorization. Preserves backend-first invariant. LLM is not the game engine.

### Reason

RUNTIME-IMPL-PR-3 authorized RUNTIME-IMPL-PR-4 as the next executable code step. The scope is narrowed to deterministic RNG interface (immutable frozen dataclass invocation/result envelopes with validation, deterministic integer helper using SHA-256, no global random state, no dice expression parser) and table/oracle interface (immutable frozen dataclass invocation/result envelopes with validation, deterministic table selection helper using sorted keys and modular index, no weighted tables, no content library). No other kernel systems are implemented.

### Implication

- `src/astra_runtime/kernel/rng_interface.py` now exists.
- `src/astra_runtime/kernel/table_oracle.py` now exists.
- `src/astra_runtime/kernel/__init__.py` exports both modules.
- 105 focused new tests pass (55 RNG interface + 50 table/oracle).
- Prior PR-1 through PR-3 guardrail tests updated to no longer forbid `rng_interface.py`.
- No full RNG service/table library/replay/persistence/domain/model/live-play artifacts created.

### Revisit trigger

- If RNG interface needs session/replay fields for event store (PR-5+).
- If table/oracle interface needs weighted table support for domain services (PR-5+).
- If RUNTIME-IMPL-PR-5 (validation pipeline and invariant precheck skeleton) is authorized.

### Classification block

```yaml
runtime_impl_pr_4:
  implementation_id: RUNTIME-IMPL-PR-4-DETERMINISTIC-RNG-TABLE-ORACLE-INTERFACE-SKELETON-001
  artifact_type: executable_kernel_skeleton
  implementation_status: narrow_executable_skeleton
  derives_from:
    - RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
    - RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001
    - RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
    - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
    - RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001
  implements_deterministic_rng_interface_skeleton: true
  implements_table_oracle_interface_skeleton: true
  authorizes_full_rng_service: false
  authorizes_global_random_state: false
  authorizes_non_deterministic_randomness: false
  authorizes_dice_expression_parser: false
  authorizes_rng_session_store: false
  authorizes_weighted_table_engine: false
  authorizes_encounter_table_library: false
  authorizes_oracle_content_library: false
  authorizes_event_store_persistence: false
  authorizes_database_schema: false
  authorizes_replay_hash_service: false
  authorizes_validation_pipeline: false
  authorizes_invariant_validator: false
  authorizes_correction_event_schema: false
  authorizes_state_store: false
  authorizes_state_mutation: false
  authorizes_command_execution: false
  authorizes_context_packet_compiler: false
  authorizes_hidden_information_partition: false
  authorizes_persistence_writer: false
  authorizes_domain_services: false
  authorizes_generators: false
  authorizes_live_play: false
  authorizes_model_integration: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-IMPL-PR-5 validation pipeline and invariant precheck skeleton, pending review
```

### No-implementation guardrails

- No validation pipeline module exists yet.
- No persistence/database module exists yet.
- No context projection or hidden-information module exists yet.
- No replay/audit module exists yet.
- No runtime trace module exists yet.
- No domain service package exists yet.
- No model integration package exists yet.
- No prompt template package exists yet.
- No live-play adapter package exists yet.

## 2026-06-07 decision — RUNTIME-IMPL-PR-5 validation pipeline and invariant precheck skeleton

- Decision ID: RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
- Decision date: 2026-06-07
- Decision type: implementation/executable skeleton

### Summary

Fifth narrow runtime code PR. Implements only validation pipeline and invariant precheck skeletons under `src/astra_runtime/kernel/`. Follows RUNTIME-IMPL-PR-0 through PR-4 authorization. Preserves backend-first invariant. LLM is not the game engine.

### Reason

RUNTIME-IMPL-PR-4 authorized RUNTIME-IMPL-PR-5 as the next executable code step. The scope is narrowed to validation issue/result envelopes (immutable frozen dataclasses with validation, copy-safe metadata, `to_dict` conversion), validation pipeline skeleton (`run_validation_checks` helper that runs local check callables and determines pass/fail by severity), required-keys check helper (`required_keys_check` factory for mapping-shaped subjects), and invariant precheck descriptor/skeleton (immutable frozen dataclass descriptor with `run_invariant_prechecks` delegating to `run_validation_checks`). No other kernel systems are implemented.

### Implication

- `src/astra_runtime/kernel/validation_pipeline.py` now exists.
- `src/astra_runtime/kernel/__init__.py` exports validation pipeline and invariant precheck symbols.
- 110 focused new tests pass.
- Prior PR-3 through PR-4 guardrail tests updated to no longer forbid `validation_pipeline.py`.
- No full validation framework/domain validation/hidden-info/context projection/persistence/replay/domain/model/live-play artifacts created.

### Revisit trigger

- If validation pipeline needs domain-specific check registries for domain services (PR-6+).
- If invariant precheck needs state-aware invariant checking for state application engine (PR-6+).
- If RUNTIME-IMPL-PR-6 (hidden-information partition and context projection skeleton) is authorized.

### Classification block

```yaml
runtime_impl_pr_5:
  implementation_id: RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
  artifact_type: executable_kernel_skeleton
  implementation_status: narrow_executable_skeleton
  derives_from:
    - RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
    - RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001
    - RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
    - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
    - RUNTIME-IMPL-PR-4-DETERMINISTIC-RNG-TABLE-ORACLE-INTERFACE-SKELETON-001
    - RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001
  implements_validation_issue_result_skeleton: true
  implements_validation_pipeline_skeleton: true
  implements_required_keys_check_helper: true
  implements_invariant_precheck_skeleton: true
  authorizes_full_validation_framework: false
  authorizes_domain_validation_rules: false
  authorizes_command_legality_engine: false
  authorizes_action_legality_engine: false
  authorizes_resource_cost_validation: false
  authorizes_combat_validation: false
  authorizes_mission_validation: false
  authorizes_social_faction_validation: false
  authorizes_inventory_validation: false
  authorizes_hidden_information_partition: false
  authorizes_context_projection: false
  authorizes_context_packet_compiler: false
  authorizes_full_invariant_validator: false
  authorizes_correction_event_schema: false
  authorizes_mutable_state_store: false
  authorizes_state_mutation: false
  authorizes_command_execution: false
  authorizes_event_commitment: false
  authorizes_event_store_persistence: false
  authorizes_database_schema: false
  authorizes_replay_hash_service: false
  authorizes_persistence_writer: false
  authorizes_domain_services: false
  authorizes_generators: false
  authorizes_live_play: false
  authorizes_model_integration: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-IMPL-PR-6 hidden-information partition and context projection skeleton, pending review
```

### No-implementation guardrails

- No hidden-information module exists yet.
- No context projection module exists yet.
- No persistence/database module exists yet.
- No replay/audit module exists yet.
- No runtime trace module exists yet.
- No invariant validator module exists yet.
- No domain service package exists yet.
- No model integration package exists yet.
- No prompt template package exists yet.
- No live-play adapter package exists yet.

## 2026-06-07 decision — RUNTIME-IMPL-PR-6 hidden-information partition and context projection skeleton

- Decision ID: RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
- Decision date: 2026-06-07
- Decision type: implementation/executable skeleton

### Summary

Sixth narrow runtime code PR. Implements only hidden-information partition and context projection skeletons under `src/astra_runtime/kernel/`. Follows RUNTIME-IMPL-PR-0 through PR-5 authorization. Preserves backend-first invariant. LLM is not the game engine.

### Reason

RUNTIME-IMPL-PR-5 authorized RUNTIME-IMPL-PR-6 as the next executable code step. The scope is narrowed to hidden-information record/partition skeleton (immutable frozen dataclass with validation, allowed visibility tiers, deep-copy-safe payload/metadata, `to_dict` conversion, explicit `is_visible_to_tiers` helper, explicit `redacted_copy` helper that strips payload) and context projection skeleton (immutable frozen dataclass item/projection with validation, `project_hidden_records` helper that includes payload for allowed tiers and redacts for disallowed tiers). No other kernel systems are implemented.

### Implication

- `src/astra_runtime/kernel/hidden_information.py` now exists.
- `src/astra_runtime/kernel/context_projection.py` now exists.
- `src/astra_runtime/kernel/__init__.py` exports both modules.
- 109 focused new tests pass.
- Prior PR-3 through PR-5 guardrail tests updated to no longer forbid `hidden_information.py` or `context_projection.py`.
- No hidden-state database/durable store/context-packet compiler/prompt template/model-facing packet/narration render packet/live-play/UI/full redaction engine/access-control policy/reveal mechanics/social-faction knowledge/clue engine/persistence/replay/domain/model/live-play artifacts created.

### Revisit trigger

- If hidden-information record needs access-control policy or reveal mechanics for domain services (PR-7+).
- If context projection needs packet budget or prioritization for context-packet compiler (PR-7+).
- If RUNTIME-IMPL-PR-7 (persistence boundary, replay/hash audit, and runtime trace skeleton) is authorized.

### Classification block

```yaml
runtime_impl_pr_6:
  implementation_id: RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
  artifact_type: executable_kernel_skeleton
  implementation_status: narrow_executable_skeleton
  derives_from:
    - RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
    - RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001
    - RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
    - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
    - RUNTIME-IMPL-PR-4-DETERMINISTIC-RNG-TABLE-ORACLE-INTERFACE-SKELETON-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001
  implements_hidden_information_partition_skeleton: true
  implements_context_projection_skeleton: true
  implements_visible_redacted_projection_helper: true
  authorizes_hidden_state_database: false
  authorizes_durable_hidden_state_store: false
  authorizes_context_packet_compiler: false
  authorizes_prompt_templates: false
  authorizes_model_facing_packet_assembly: false
  authorizes_narration_render_packet_compiler: false
  authorizes_live_play: false
  authorizes_ui_projection_layer: false
  authorizes_full_redaction_engine: false
  authorizes_access_control_policy_engine: false
  authorizes_reveal_mechanics: false
  authorizes_social_faction_knowledge_engine: false
  authorizes_clue_engine: false
  authorizes_state_store: false
  authorizes_state_mutation: false
  authorizes_command_execution: false
  authorizes_event_commitment: false
  authorizes_event_store_persistence: false
  authorizes_database_schema: false
  authorizes_replay_hash_service: false
  authorizes_persistence_writer: false
  authorizes_runtime_trace: false
  authorizes_domain_services: false
  authorizes_generators: false
  authorizes_model_integration: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-IMPL-PR-7 persistence boundary replay/hash audit and runtime trace skeleton, pending review
```

### No-implementation guardrails

- No persistence/database module exists yet.
- No replay/audit module exists yet.
- No runtime trace module exists yet.
- No context-packet compiler module exists.
- No domain service package exists yet.
- No model integration package exists yet.
- No prompt template package exists yet.
- No live-play adapter package exists yet.
- No UI/client package exists yet.

## 2026-06-07 decision — RUNTIME-IMPL-PR-7 persistence boundary, replay/hash audit, and runtime trace skeleton

- Decision ID: RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
- Decision date: 2026-06-07
- Decision type: implementation/executable skeleton

### Summary

Seventh narrow runtime code PR. Implements only persistence boundary, replay/hash audit, and runtime trace skeletons under `src/astra_runtime/kernel/`. Follows RUNTIME-IMPL-PR-0 through PR-6 authorization. Preserves backend-first invariant. LLM is not the game engine.

### Reason

RUNTIME-IMPL-PR-6 authorized RUNTIME-IMPL-PR-7 as the next executable code step. The scope is narrowed to persistence boundary (immutable frozen dataclass request/result envelopes with validation, allowed operation types record_snapshot_prepare/event_append_prepare/trace_capture_prepare/audit_snapshot_prepare, allowed result statuses prepared/rejected/quarantined, no durable persistence), replay/hash audit (immutable frozen dataclass records with validation, deterministic canonical_payload_hash using json.dumps sort_keys + hashlib.sha256, no replay engine, no hash-chain enforcement), and runtime trace (immutable frozen dataclass entries with validation, allowed operation types covering all 14 kernel modules, no trace store, no telemetry). No other kernel systems are implemented.

### Implication

- `src/astra_runtime/kernel/persistence_boundary.py` now exists.
- `src/astra_runtime/kernel/replay_audit.py` now exists.
- `src/astra_runtime/kernel/runtime_trace.py` now exists.
- `src/astra_runtime/kernel/__init__.py` exports all three modules.
- 123 focused new tests pass.
- Prior PR-3 through PR-6 guardrail tests updated to no longer forbid `persistence_boundary.py`, `replay_audit.py`, or `runtime_trace.py`.
- No durable persistence/file I/O/database/replay engine/state store/trace store/domain/model/live-play artifacts created.

### Revisit trigger

- If persistence boundary needs storage-backend selection for durable persistence (PR-8+).
- If replay/hash audit needs hash-chain enforcement or event replay for event store (PR-8+).
- If runtime trace needs telemetry backend or trace store (PR-8+).
- If RUNTIME-IMPL-PR-8 (post-kernel skeleton review and domain-service readiness gate) is authorized.

### Classification block

```yaml
runtime_impl_pr_7:
  implementation_id: RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
  artifact_type: executable_kernel_skeleton
  implementation_status: narrow_executable_skeleton
  derives_from:
    - RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
    - RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001
    - RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
    - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
    - RUNTIME-IMPL-PR-4-DETERMINISTIC-RNG-TABLE-ORACLE-INTERFACE-SKELETON-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
    - RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001
  implements_persistence_boundary_skeleton: true
  implements_replay_hash_audit_skeleton: true
  implements_canonical_payload_hash_helper: true
  implements_runtime_trace_skeleton: true
  authorizes_durable_persistence: false
  authorizes_file_writer: false
  authorizes_file_reader: false
  authorizes_database_schema: false
  authorizes_database_connection: false
  authorizes_sqlite_integration: false
  authorizes_migrations: false
  authorizes_object_store: false
  authorizes_event_store_persistence: false
  authorizes_state_store: false
  authorizes_state_restoration: false
  authorizes_replay_engine: false
  authorizes_event_replay: false
  authorizes_hash_chain_enforcement_engine: false
  authorizes_trace_store: false
  authorizes_telemetry_backend: false
  authorizes_logging_service: false
  authorizes_command_execution: false
  authorizes_state_mutation: false
  authorizes_event_commitment: false
  authorizes_transaction_lifecycle_engine: false
  authorizes_domain_services: false
  authorizes_context_packet_compiler: false
  authorizes_prompt_templates: false
  authorizes_model_integration: false
  authorizes_live_play: false
  authorizes_ui_client: false
  authorizes_generators: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-IMPL-PR-8 post-kernel skeleton review and domain-service readiness gate, pending review
```

### No-implementation guardrails

- No context-packet compiler module exists.
- No domain service package exists yet.
- No model integration package exists yet.
- No prompt template package exists yet.
- No live-play adapter package exists yet.
- No UI/client package exists yet.
- No database package exists yet.
- No durable store package exists yet.

---

## RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001

**Date:** 2026-06-08

### Decision

RUNTIME-IMPL-PR-8 is a review/gate-only artifact. It confirms that the minimum backend kernel skeleton (PR-1 through PR-7) is complete enough to proceed to a future domain-service implementation-planning PR.

### Reason

All 14 kernel skeleton modules exist with passing tests, frozen dataclasses, backend-owned validation, and no domain logic, persistence side effects, or LLM authority. The kernel interface surface is sufficient for domain services to plan their consumption patterns.

### Implication

- Authorizes only RUNTIME-DOMAIN-PR-0 (domain service implementation sequencing plan), a future planning-only PR.
- Does not authorize domain-service code, command execution, state store, state mutation, event commitment, durable persistence, database schema, replay engine, context-packet compiler, prompt templates, model integration, live-play adapter, UI/client, training, donor-content audit, pilot conversion, sourcebook inclusion, or canon promotion.
- Domain services remain blocked until RUNTIME-DOMAIN-PR-0 defines order, boundaries, allowed dependencies, tests, and guardrails.

### Revisit trigger

- If RUNTIME-DOMAIN-PR-0 (domain service implementation sequencing plan) is authorized.
- If kernel skeleton modules require interface changes during domain-service planning.

### Classification block

```yaml
runtime_impl_pr_8:
  implementation_id: RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001
  artifact_type: post_kernel_skeleton_review_and_domain_service_readiness_gate
  implementation_status: non_executable_review_gate
  confirms_minimum_backend_kernel_skeleton_complete: true
  confirms_ready_for_domain_service_planning: true
  authorizes_domain_service_code_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_state_store_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_event_commitment_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_prompt_templates_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-0 domain service implementation sequencing plan, pending review
```

### No-implementation guardrails

- No domain service package exists yet.
- No model integration package exists yet.
- No prompt template package exists yet.
- No live-play adapter package exists yet.
- No UI/client package exists yet.
- No database package exists yet.
- No durable store package exists yet.
- No context-packet compiler module exists.

---

## RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001

**Date:** 2026-06-08

### Decision

RUNTIME-DOMAIN-PR-0 is a planning-only domain service implementation sequencing plan. It defines the domain-service implementation order, dependency rules, kernel dependency matrix, blocked-until ledger, risk review, and future integration test plan. It authorizes only RUNTIME-DOMAIN-PR-1 planning.

### Reason

RUNTIME-IMPL-PR-8 confirmed the minimum backend kernel skeleton sequence is complete and authorized RUNTIME-DOMAIN-PR-0 as a planning-only next step. Domain services require a sequencing plan before any implementation can begin.

### Implication

- Defines 14 domain-service families and their dependency order.
- Defines RUNTIME-DOMAIN-PR-1 through PR-15 planning sequence.
- Defines strict dependency rules for all future domain services.
- Defines kernel dependency matrix connecting service families to kernel modules.
- Does not authorize domain-service code, command execution, action legality engine, state store, state mutation, transaction lifecycle, event commitment, durable persistence, context-packet compiler, prompt templates, model integration, live-play adapter, UI/client, training, pilot conversion, sourcebook inclusion, or canon promotion.

### Revisit trigger

- If RUNTIME-DOMAIN-PR-1 (command lifecycle and action legality service plan) is authorized.
- If kernel skeleton interfaces require changes during domain-service planning.

### Classification block

```yaml
runtime_domain_pr_0:
  implementation_id: RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001
  artifact_type: domain_service_implementation_sequencing_plan
  implementation_status: non_executable_plan
  defines_domain_service_family_inventory: true
  defines_domain_service_pr_sequence: true
  defines_dependency_rules: true
  defines_kernel_dependency_matrix: true
  defines_blocked_until_ledger: true
  defines_risk_review: true
  defines_future_integration_test_plan: true
  authorizes_domain_service_code_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_action_legality_engine_by_this_pr: false
  authorizes_state_store_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_transaction_lifecycle_by_this_pr: false
  authorizes_event_commitment_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_prompt_templates_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-1 command lifecycle and action legality service plan, pending review
```

### No-implementation guardrails

- No domain service package exists yet.
- No model integration package exists yet.
- No prompt template package exists yet.
- No live-play adapter package exists yet.
- No UI/client package exists yet.
- No database package exists yet.
- No durable store package exists yet.
- No context-packet compiler module exists.

---

## RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001

**Date:** 2026-06-08

### Decision

RUNTIME-DOMAIN-PR-1 is a planning-only command lifecycle and action legality service plan. It defines the future service's scope, ownership, command lifecycle state model, action legality decision model, kernel interface consumption plan, dependency and handoff boundaries, future implementation architecture, future data shapes, test requirements, corpus-scale command pressure review, guardrail review, and risk review. It authorizes only RUNTIME-DOMAIN-PR-1A skeleton implementation pending review.

### Reason

RUNTIME-DOMAIN-PR-0 confirmed that command lifecycle and action legality is the first domain-service family and that RUNTIME-DOMAIN-PR-1 is the next allowed planning step. The service plan must be defined before any skeleton implementation can begin.

### Implication

- Defines RT-001 as primary service owner with RT-011, RT-002, RT-005, RT-009, and RT-012 as secondary dependencies.
- Defines 12 command lifecycle states and 12 action legality decision categories.
- Defines kernel interface consumption matrix for all 14 kernel modules.
- Defines handoff boundaries to 13 future downstream services.
- Defines future implementation architecture (3 modules, 8 proposed symbols).
- Defines 6 future data shapes.
- Defines 17 test families for future implementation.
- Defines corpus-scale command pressure review covering 16 command categories.
- Does not authorize command lifecycle code, action legality engine, command execution, command parser, state store, state mutation, transaction lifecycle, event commitment, resource math, combat resolution, ability resolution, inventory mutation, mission/social mutation, context-packet compiler, prompt templates, model integration, live-play adapter, UI/client, training, pilot conversion, sourcebook inclusion, or canon promotion.

### Revisit trigger

- If RUNTIME-DOMAIN-PR-1A (command lifecycle and action legality skeleton implementation) is authorized.
- If kernel interfaces require changes during domain-service implementation.
- If command lifecycle state model or action legality decision model requires revision after downstream service planning.

### Classification block

```yaml
runtime_domain_pr_1:
  implementation_id: RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001
  artifact_type: command_lifecycle_action_legality_service_plan
  implementation_status: non_executable_plan
  defines_service_ownership: true
  defines_command_lifecycle_state_model: true
  defines_action_legality_decision_model: true
  defines_kernel_interface_consumption_plan: true
  defines_handoff_boundaries: true
  defines_future_implementation_architecture: true
  defines_future_data_shapes: true
  defines_future_test_requirements: true
  defines_corpus_scale_command_pressure_review: true
  authorizes_command_lifecycle_code_by_this_pr: false
  authorizes_action_legality_engine_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_command_parser_by_this_pr: false
  authorizes_state_store_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_transaction_lifecycle_by_this_pr: false
  authorizes_event_commitment_by_this_pr: false
  authorizes_resource_math_by_this_pr: false
  authorizes_combat_resolution_by_this_pr: false
  authorizes_ability_resolution_by_this_pr: false
  authorizes_inventory_mutation_by_this_pr: false
  authorizes_mission_mutation_by_this_pr: false
  authorizes_social_faction_mutation_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_prompt_templates_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-1A command lifecycle and action legality skeleton implementation, pending review
```

### No-implementation guardrails

- Domain service package exists with authorized skeleton modules only (command_lifecycle.py, action_legality.py).
- No model integration package exists yet.
- No prompt template package exists yet.
- No live-play adapter package exists yet.
- No UI/client package exists yet.
- No database package exists yet.
- No durable store package exists yet.
- No context-packet compiler module exists.

## 2026-06-08 — PR-1A command lifecycle and action legality skeleton implementation

Decision: Implement RUNTIME-DOMAIN-PR-1A as the first narrow domain-service skeleton, creating `src/astra_runtime/domain/` with `command_lifecycle.py` and `action_legality.py`.

Implementation ID: `RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001`

Reason: RUNTIME-DOMAIN-PR-1 confirmed command lifecycle/action legality as the first domain-service implementation target. PR-1A implements only immutable result surfaces and stateless wrapper helpers.

Implication: The domain package now exists with exactly three files (`__init__.py`, `command_lifecycle.py`, `action_legality.py`). Kernel guardrail tests updated to assert only authorized modules exist rather than asserting the package is absent.

Revisit trigger: When RUNTIME-DOMAIN-PR-1B review or RUNTIME-DOMAIN-PR-2 state store planning begins.

### Scope confirmation

- Narrow skeleton implementation only.
- Implements immutable `CommandLifecycleResult` and `ActionLegalityResult` surfaces.
- Implements stateless `CommandLifecycleService` and `ActionLegalityService` wrappers.
- Does not execute commands, mutate state, commit events, parse player prose, compute resources, resolve combat/abilities/items/missions/social state, call models, create prompts, run live play, execute conversion, include sourcebook content, or promote canon.

## 2026-06-08 — PR-1B command lifecycle and action legality skeleton review

Decision ID: RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001

Decision: Complete RUNTIME-DOMAIN-PR-1B as a review/gate-only artifact assessing the PR-1A command lifecycle/action legality skeleton implementation.

Decision type: command_lifecycle_action_legality_skeleton_review_gate

Reason: PR-1A created the first authorized domain package. Before proceeding to state store/state projection planning, the skeleton implementation must be reviewed for scope compliance, guardrail safety, kernel dependency correctness, and corpus-scale readiness.

### Summary

- Review/gate only; no code changes.
- Confirms PR-1A stayed within skeleton-only scope.
- Confirms guardrail transition from "no domain package" to "authorized modules only" is safe.
- Confirms command lifecycle and action legality skeletons are stable dependencies for future services.
- Identifies future hardening candidates (terminal stage/status consistency, hidden-info-safe block reason enforcement, dependency declaration normalization, etc.) — none required before PR-2.
- Authorizes RUNTIME-DOMAIN-PR-2 (state store and state projection service plan) as the next planning step.

### Implication

- PR-1A scope confirmed: no blockers, no violations.
- Guardrail transition is safe.
- Future hardening items are low-risk and belong to their respective RT owners.
- PR-2 planning can proceed as planning-only.

### Revisit trigger

- When RUNTIME-DOMAIN-PR-2 planning begins.
- If future hardening items are promoted to blocking.
- If kernel interfaces require changes during domain-service planning.

### No-implementation guardrails reaffirmed

- No runtime code.
- No domain-service code.
- No command execution.
- No command parser.
- No state store.
- No state projection.
- No state mutation.
- No transaction lifecycle.
- No event commitment.
- No resource math.
- No combat resolution.
- No ability resolution.
- No inventory mutation.
- No mission/social mutation.
- No context-packet compiler.
- No prompt templates.
- No model integration.
- No live-play adapter.
- No UI/client.
- No training authorization.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

---

## RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001

**Date:** 2026-06-09

### Decision

Created RUNTIME-DOMAIN-PR-2: a planning-only state store and state projection service plan. Defines future state ownership model, state projection model, state lifecycle model, kernel interface consumption plan, dependency/handoff boundaries, future implementation architecture, future data shapes, future test requirements, corpus-scale state pressure review, and future hardening ledger.

### Reason

RUNTIME-DOMAIN-PR-1B confirmed the command lifecycle/action legality skeleton is stable and authorized PR-2 as the next planning step. The state store/state projection service is the second domain-service family in the sequencing plan (RUNTIME-DOMAIN-PR-0) and blocks all downstream domain services that consume state projections.

### Implication

- State store and state projection service boundaries are defined.
- Authorizes only a future narrow skeleton implementation PR (RUNTIME-DOMAIN-PR-2A) after review.
- All downstream domain services (resource math, combat, abilities, inventory, mission, social/faction, generated-content) depend on this plan.
- PR-2A planning can proceed as skeleton-only.

### Revisit trigger

- When RUNTIME-DOMAIN-PR-2A skeleton implementation begins.
- If state ownership model requires revision during implementation.
- If kernel interfaces require changes during state store/projection implementation.
- If hidden-information safety requirements need strengthening.

### No-implementation guardrails reaffirmed

- No state-store code.
- No state-projection code.
- No mutable runtime state.
- No state mutation.
- No state delta application.
- No transaction lifecycle.
- No event commitment.
- No event sourcing.
- No durable persistence.
- No database schema.
- No replay engine.
- No command execution.
- No command parser.
- No resource math.
- No combat resolution.
- No ability resolution.
- No inventory mutation.
- No mission/social mutation.
- No context-packet compiler.
- No prompt templates.
- No model integration.
- No live-play adapter.
- No UI/client.
- No training authorization.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

---

## RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001

**Date:** 2026-06-09

### Decision

Narrow skeleton implementation only. Implements immutable state record/snapshot/projection request/projection result surfaces and stateless wrappers. Follows RUNTIME-DOMAIN-PR-2.

### Reason

RUNTIME-DOMAIN-PR-2 authorized RUNTIME-DOMAIN-PR-2A as the next skeleton implementation step. PR-2A is constrained to skeleton surfaces only: immutable frozen dataclasses representing state record refs, state snapshot refs, state visibility descriptors, state projection dependencies, state projection rejections, state projection requests, and state projection results; plus stateless service wrapper classes.

### Implication

The domain package now exports state store and state projection skeleton surfaces. No mutable runtime state, no state mutation, no state delta application, no transaction lifecycle, no event commitment, no event sourcing, no durable persistence, no database schema, no replay engine, no command execution, no command parser, no action legality expansion, no resource math, no combat resolution, no ability resolution, no inventory mutation, no mission/social mutation, no generated-content persistence, no context-packet compiler, no prompt templates, no model integration, no live-play adapter, no UI/client, no training authorization, no pilot conversion authorization, no sourcebook inclusion authorization, no canon promotion.

### Revisit trigger

- When RUNTIME-DOMAIN-PR-2B skeleton review begins.
- When RUNTIME-DOMAIN-PR-3 transaction lifecycle service plan begins.
- If state ownership model requires revision.
- If hidden-information safety requirements need strengthening.

### Classification

```yaml
runtime_domain_pr_2a:
  implementation_id: RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001
  artifact_type: state_store_state_projection_skeleton_implementation
  implementation_status: narrow_executable_skeleton
  derives_from:
  - RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001
  - RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001
  - RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001
  - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
  - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
  - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
  - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
  - RT-005
  - RT-011
  implements_state_store_skeleton: true
  implements_state_projection_skeleton: true
  implements_stateless_service_wrappers: true
  implements_immutable_state_reference_surfaces: true
  implements_immutable_projection_surfaces: true
  authorizes_mutable_runtime_state_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_state_delta_application_by_this_pr: false
  authorizes_transaction_lifecycle_by_this_pr: false
  authorizes_event_commitment_by_this_pr: false
  authorizes_event_sourcing_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_database_schema_by_this_pr: false
  authorizes_replay_engine_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_command_parser_by_this_pr: false
  authorizes_action_legality_expansion_by_this_pr: false
  authorizes_resource_math_by_this_pr: false
  authorizes_combat_resolution_by_this_pr: false
  authorizes_ability_resolution_by_this_pr: false
  authorizes_inventory_mutation_by_this_pr: false
  authorizes_mission_mutation_by_this_pr: false
  authorizes_social_faction_mutation_by_this_pr: false
  authorizes_generated_content_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_prompt_templates_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-2B state store/state projection skeleton review or RUNTIME-DOMAIN-PR-3 transaction lifecycle and event commitment service plan, pending review
```

---

## RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001

**Date:** 2026-06-09

### Decision

Review/gate only. Reviews and confirms RUNTIME-DOMAIN-PR-2A state store/state projection skeleton implementation scope, guardrail transition safety, validator surface adequacy, and kernel dependency posture. Authorizes RUNTIME-DOMAIN-PR-3 transaction lifecycle and event commitment service plan as the next step.

### Reason

RUNTIME-DOMAIN-PR-2A delivered the state store and state projection skeleton implementation. PR-2B reviews that implementation before transaction lifecycle and event commitment planning can proceed. This follows the established gate pattern from RUNTIME-DOMAIN-PR-1B.

### Implication

PR-2A scope is confirmed as skeleton-only. Guardrail transition from 3 to 5 authorized domain files is safe. Validator surfaces mirror factory constraints with full parity. No PR-2C hardening pass is required before PR-3 planning. The next authorized step is RUNTIME-DOMAIN-PR-3 (transaction lifecycle and event commitment service plan, planning only).

### Revisit trigger

- When RUNTIME-DOMAIN-PR-3 transaction lifecycle and event commitment service plan begins.
- If future hardening items from the PR-2B ledger need to be addressed before PR-3.
- If hidden-information safety requirements need strengthening before transaction lifecycle planning.

### No-implementation guardrails reaffirmed

- No runtime code.
- No domain-service code.
- No state-store implementation changes.
- No state-projection implementation changes.
- No mutable runtime state.
- No state mutation.
- No state delta application.
- No transaction lifecycle.
- No event commitment.
- No event sourcing.
- No durable persistence.
- No database schema.
- No replay engine.
- No command execution.
- No command parser.
- No action legality expansion.
- No resource math.
- No combat resolution.
- No ability resolution.
- No inventory mutation.
- No mission/social mutation.
- No generated-content persistence.
- No context-packet compiler.
- No prompt templates.
- No model integration.
- No live-play adapter.
- No UI/client.
- No training authorization.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

### Classification

```yaml
runtime_domain_pr_2b:
  review_id: RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001
  artifact_type: state_store_state_projection_skeleton_review_gate
  implementation_status: non_executable_review_gate
  derives_from:
  - RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001
  - RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001
  - RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001
  - RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001
  - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
  - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
  - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
  - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
  - RT-005
  - RT-011
  reviews_state_store_skeleton: true
  reviews_state_projection_skeleton: true
  reviews_validator_parity: true
  reviews_guardrail_transition: true
  reviews_kernel_dependency_usage: true
  reviews_corpus_scale_state_pressure: true
  defines_future_hardening_ledger: true
  authorizes_code_by_this_pr: false
  authorizes_mutable_runtime_state_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_state_delta_application_by_this_pr: false
  authorizes_transaction_lifecycle_by_this_pr: false
  authorizes_event_commitment_by_this_pr: false
  authorizes_event_sourcing_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_database_schema_by_this_pr: false
  authorizes_replay_engine_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_command_parser_by_this_pr: false
  authorizes_action_legality_expansion_by_this_pr: false
  authorizes_resource_math_by_this_pr: false
  authorizes_combat_resolution_by_this_pr: false
  authorizes_ability_resolution_by_this_pr: false
  authorizes_inventory_mutation_by_this_pr: false
  authorizes_mission_mutation_by_this_pr: false
  authorizes_social_faction_mutation_by_this_pr: false
  authorizes_generated_content_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_prompt_templates_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-3 transaction lifecycle and event commitment service plan, pending review
```

---

## RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001

**Date:** 2026-06-09

### Decision

Planning-only transaction lifecycle and event commitment service plan. Defines future transaction lifecycle ownership, event commitment ownership, transaction lifecycle model, event commitment model, transaction/event boundary, kernel interface consumption plan, domain service handoff boundaries, future implementation architecture, future data shapes, commit-readiness invariants, corpus-scale transaction pressure review, risk review, future hardening ledger, and implementation PR authorization boundary. Follows RUNTIME-DOMAIN-PR-2B. Authorizes only RUNTIME-DOMAIN-PR-3A (transaction lifecycle and event commitment skeleton implementation) pending review.

### Reason

RUNTIME-DOMAIN-PR-2B confirmed the state store/state projection skeleton is stable and authorized PR-3 as the next planning step. The transaction lifecycle and event commitment service is the third domain-service family in the sequencing plan (RUNTIME-DOMAIN-PR-0) and is the future backend-owned boundary where validated command outcomes become committed runtime facts.

### Implication

- Transaction lifecycle and event commitment service boundaries are defined.
- Authorizes only a future narrow skeleton implementation PR (RUNTIME-DOMAIN-PR-3A) after review.
- Defines 18 transaction lifecycle stages and 12 event commitment decisions.
- Defines kernel interface consumption matrix for all 14 kernel modules.
- Defines handoff boundaries to 16 future downstream services.
- No code is implemented by this PR.

### Revisit trigger

- When RUNTIME-DOMAIN-PR-3A skeleton implementation begins.
- If transaction lifecycle model requires revision during implementation.
- If event commitment model requires revision during implementation.
- If kernel interfaces require changes during transaction lifecycle/event commitment implementation.

### No-implementation guardrails reaffirmed

- No transaction lifecycle code.
- No event commitment code.
- No event sourcing.
- No mutable runtime state.
- No state mutation.
- No state delta application.
- No event ledger append.
- No durable persistence.
- No database schema.
- No replay engine.
- No command execution.
- No command parser.
- No action legality expansion.
- No resource math.
- No combat resolution.
- No ability resolution.
- No inventory mutation.
- No mission/social mutation.
- No generated-content persistence.
- No context-packet compiler.
- No prompt templates.
- No model integration.
- No live-play adapter.
- No UI/client.
- No training authorization.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

### Classification

```yaml
runtime_domain_pr_3:
  plan_id: RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001
  artifact_type: transaction_lifecycle_event_commitment_service_plan
  implementation_status: non_executable_plan
  derives_from:
  - RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001
  - RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001
  - RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001
  - RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001
  - RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001
  - RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
  - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
  - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
  - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
  - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
  - RT-001
  - RT-005
  - RT-011
  defines_transaction_lifecycle_model: true
  defines_event_commitment_model: true
  defines_transaction_event_boundary: true
  defines_kernel_interface_consumption_plan: true
  defines_domain_service_handoffs: true
  defines_future_implementation_architecture: true
  defines_future_data_shapes: true
  defines_commit_readiness_invariants: true
  defines_corpus_scale_transaction_pressure_review: true
  defines_future_hardening_ledger: true
  authorizes_transaction_lifecycle_code_by_this_pr: false
  authorizes_event_commitment_code_by_this_pr: false
  authorizes_event_sourcing_by_this_pr: false
  authorizes_mutable_runtime_state_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_state_delta_application_by_this_pr: false
  authorizes_event_ledger_append_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_database_schema_by_this_pr: false
  authorizes_replay_engine_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_command_parser_by_this_pr: false
  authorizes_action_legality_expansion_by_this_pr: false
  authorizes_resource_math_by_this_pr: false
  authorizes_combat_resolution_by_this_pr: false
  authorizes_ability_resolution_by_this_pr: false
  authorizes_inventory_mutation_by_this_pr: false
  authorizes_mission_mutation_by_this_pr: false
  authorizes_social_faction_mutation_by_this_pr: false
  authorizes_generated_content_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_prompt_templates_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-3A transaction lifecycle and event commitment skeleton implementation, pending review
```

---

## RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001

**Date:** 2026-06-10

### Decision

Narrow executable skeleton implementation only. Creates transaction lifecycle and event commitment skeleton modules under `src/astra_runtime/domain/`. Follows RUNTIME-DOMAIN-PR-3.

### Reason

RUNTIME-DOMAIN-PR-3 defined the transaction lifecycle and event commitment service plan and authorized RUNTIME-DOMAIN-PR-3A as the next skeleton implementation step. PR-3A is constrained to skeleton surfaces only: immutable frozen dataclasses representing transaction dependencies, preconditions, requests, plans, and results; event commitment dependencies, rejections, requests, and results; plus stateless service wrapper classes.

### Implication

The domain package now exports transaction lifecycle and event commitment skeleton surfaces. No actual transaction execution, no actual event commitment, no event sourcing, no mutable runtime state, no state mutation, no state delta application, no event ledger append, no durable persistence, no database schema, no replay engine, no command execution, no parser, no action legality expansion, no resource math, no combat, no ability resolution, no inventory mutation, no mission/social mutation, no generated-content persistence, no context-packet compiler, no prompts, no model integration, no live play, no UI, no training, no pilot conversion, no sourcebook inclusion, no canon promotion.

### Revisit trigger

- When RUNTIME-DOMAIN-PR-3B skeleton review begins.
- When RUNTIME-DOMAIN-PR-4 planning begins.
- If transaction lifecycle or event commitment model requires revision.
- If kernel interfaces require changes during implementation.

### Classification

```yaml
runtime_domain_pr_3a:
  implementation_id: RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001
  artifact_type: transaction_lifecycle_event_commitment_skeleton_implementation
  implementation_status: narrow_executable_skeleton
  derives_from:
  - RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001
  - RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001
  - RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001
  implements_transaction_lifecycle_skeleton: true
  implements_event_commitment_skeleton: true
  implements_stateless_service_wrappers: true
  authorizes_transaction_execution_by_this_pr: false
  authorizes_actual_event_commitment_by_this_pr: false
  authorizes_event_sourcing_by_this_pr: false
  authorizes_mutable_runtime_state_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_state_delta_application_by_this_pr: false
  authorizes_event_ledger_append_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_database_schema_by_this_pr: false
  authorizes_replay_engine_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_command_parser_by_this_pr: false
  authorizes_action_legality_expansion_by_this_pr: false
  authorizes_resource_math_by_this_pr: false
  authorizes_combat_resolution_by_this_pr: false
  authorizes_ability_resolution_by_this_pr: false
  authorizes_inventory_mutation_by_this_pr: false
  authorizes_mission_mutation_by_this_pr: false
  authorizes_social_faction_mutation_by_this_pr: false
  authorizes_generated_content_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_prompt_templates_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-3B transaction lifecycle and event commitment skeleton review gate or RUNTIME-DOMAIN-PR-4 planning, pending review
```

---

## RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001

**Date:** 2026-06-10

### Decision

Review/gate-only artifact. Reviews PR-3A transaction lifecycle and event commitment skeleton implementation. Confirms readiness for PR-4 planning.

### Reason

RUNTIME-DOMAIN-PR-3A created transaction lifecycle and event commitment skeleton modules. PR-3B reviews that implementation for scope compliance, validator parity, anti-mutation/anti-append guardrails, domain-package guardrails, kernel dependency posture, corpus-scale pressure coverage, and risk assessment. The review found no blockers and no required PR-3C hardening.

### Implication

PR-3A's transaction lifecycle and event commitment skeletons are confirmed as scope-compliant skeleton-only implementations. The gate authorizes RUNTIME-DOMAIN-PR-4 planning as the next step. No PR-3C hardening is required.

### Revisit trigger

- When RUNTIME-DOMAIN-PR-4 planning begins.
- If transaction lifecycle or event commitment model requires revision during future implementation.
- If kernel interfaces require changes during future domain service implementation.

### No-implementation guardrails reaffirmed

- No runtime code.
- No domain-service code.
- No transaction lifecycle implementation changes.
- No event commitment implementation changes.
- No transaction execution.
- No actual event commitment.
- No event sourcing.
- No mutable runtime state.
- No state mutation.
- No state delta application.
- No event ledger append.
- No durable persistence.
- No database schema.
- No replay engine.
- No rollback engine.
- No command execution.
- No command parser.
- No action legality expansion.
- No resource math.
- No combat resolution.
- No ability resolution.
- No inventory mutation.
- No mission/social mutation.
- No generated-content persistence.
- No context-packet compiler.
- No prompt templates.
- No model integration.
- No live-play adapter.
- No UI/client.
- No training authorization.
- No pilot conversion authorization.
- No sourcebook inclusion authorization.
- No canon promotion.

### Classification

```yaml
runtime_domain_pr_3b:
  review_id: RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001
  artifact_type: transaction_lifecycle_event_commitment_skeleton_review_gate
  implementation_status: non_executable_review_gate
  derives_from:
  - RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001
  - RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001
  - RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001
  - RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001
  reviews_transaction_lifecycle_skeleton: true
  reviews_event_commitment_skeleton: true
  reviews_validator_parity: true
  reviews_anti_mutation_guardrails: true
  reviews_anti_append_guardrails: true
  reviews_domain_package_guardrails: true
  reviews_kernel_dependency_usage: true
  reviews_corpus_scale_transaction_pressure: true
  defines_future_hardening_ledger: true
  authorizes_runtime_code_by_this_pr: false
  authorizes_domain_code_by_this_pr: false
  authorizes_transaction_execution_by_this_pr: false
  authorizes_actual_event_commitment_by_this_pr: false
  authorizes_event_sourcing_by_this_pr: false
  authorizes_mutable_runtime_state_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_state_delta_application_by_this_pr: false
  authorizes_event_ledger_append_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_database_schema_by_this_pr: false
  authorizes_replay_engine_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_command_parser_by_this_pr: false
  authorizes_resource_math_by_this_pr: false
  authorizes_combat_resolution_by_this_pr: false
  authorizes_ability_resolution_by_this_pr: false
  authorizes_inventory_mutation_by_this_pr: false
  authorizes_mission_mutation_by_this_pr: false
  authorizes_social_faction_mutation_by_this_pr: false
  authorizes_generated_content_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-4 planning, pending review
```

---

## RUNTIME-DOMAIN-PR-4A-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-IMPLEMENTATION-001

**Date:** 2026-06-10

### Decision

Narrow executable skeleton implementation for validation integration and invariant enforcement domain surfaces. Creates validation integration skeleton, invariant declaration skeleton surfaces, validation result/failure route reference surfaces. Updates domain exports. Adds focused skeleton tests. Follows RUNTIME-DOMAIN-PR-4 plan.

### Reason

RUNTIME-DOMAIN-PR-4 authorized RUNTIME-DOMAIN-PR-4A as the next executable step. The scope is narrowed to immutable frozen dataclass surfaces for validation integration dependency, invariant declaration, failure route, request, and result; constant sets for stages, decisions, invariant families, failure routes, dependency types, and subject types; factory/validator helpers; and a stateless service wrapper. No validation rules, no invariant enforcement, no state mutation, no delta application, no event append, no persistence, no replay, no command execution, no model/live-play behavior.

### Implication

- `src/astra_runtime/domain/validation_integration.py` now exists.
- `src/astra_runtime/domain/__init__.py` exports all new symbols.
- Focused skeleton tests pass.
- Domain package guardrail tests updated to authorize `validation_integration.py`.
- No validation rules, invariant enforcement, state mutation, event append, persistence, replay, command execution, resource math, combat, abilities/effects, inventory, mission/social, generated-content persistence, context-packet compiler, model, live-play, UI, conversion, sourcebook, or canon behavior created.

### Revisit trigger

- When RUNTIME-DOMAIN-PR-4B review gate begins.
- If validation integration model, decision model, or invariant family model requires revision during review.
- If kernel validation pipeline interfaces change during later integration.

### Classification

```yaml
runtime_domain_pr_4a:
  implementation_id: RUNTIME-DOMAIN-PR-4A-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-IMPLEMENTATION-001
  artifact_type: executable_domain_skeleton
  implementation_status: narrow_executable_skeleton
  derives_from:
    - RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001
  implements_validation_integration_skeleton: true
  implements_invariant_declaration_skeleton: true
  implements_validation_result_skeleton: true
  implements_failure_route_skeleton: true
  authorizes_domain_validation_rules_by_this_pr: false
  authorizes_actual_invariant_enforcement_by_this_pr: false
  authorizes_validation_pipeline_execution_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_delta_application_by_this_pr: false
  authorizes_event_append_by_this_pr: false
  authorizes_persistence_by_this_pr: false
  authorizes_replay_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_resource_math_by_this_pr: false
  authorizes_combat_by_this_pr: false
  authorizes_abilities_effects_by_this_pr: false
  authorizes_inventory_mutation_by_this_pr: false
  authorizes_mission_social_mutation_by_this_pr: false
  authorizes_generated_content_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-4B validation integration and invariant enforcement skeleton review gate, pending review
```

---

## RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001

**Date:** 2026-06-10

### Decision

Planning-only validation integration and invariant enforcement service plan. Defines validation integration ownership, invariant enforcement ownership, validation integration model (20 stages), validation decision model (16 decisions), invariant family model (21 families), validation failure routing (12 routes), hidden-information and provenance validation safety, kernel interface consumption plan, domain service handoff boundaries with command lifecycle / action legality / state store / state projection / transaction lifecycle / event commitment and future domain services, future implementation architecture, future data shapes, commit-readiness validation invariants, corpus-scale validation pressure review, risk review, future hardening ledger, and implementation PR authorization boundary. Follows RUNTIME-DOMAIN-PR-3B. Authorizes only RUNTIME-DOMAIN-PR-4A (validation integration and invariant enforcement skeleton implementation) pending review.

### Reason

RUNTIME-DOMAIN-PR-3B confirmed the transaction lifecycle and event commitment skeletons are scope-compliant, that validator surfaces are acceptable for later services, and that the next authorized step is RUNTIME-DOMAIN-PR-4 planning. RUNTIME-DOMAIN-PR-0 sequences validation integration / invariant enforcement as the fourth foundation domain service. Validation is a backend-owned authority layer: the LLM is not the game engine, the backend owns truth, and narration, model output, UI text, donor assumptions, source-local content, and generated content cannot validate themselves or override backend validation.

### Implication

- Validation integration and invariant enforcement service boundaries are defined.
- Authorizes only a future narrow skeleton implementation PR (RUNTIME-DOMAIN-PR-4A) after review.
- Validation failures route to block, reject, quarantine, or doctrine escalation; no silent passes.
- Hidden information may be referenced internally but never exposed in player/model-facing validation summaries.
- Generated content cannot become durable without provenance validation; source-local content cannot become canon by passing runtime validation.
- No code is implemented by this PR.

### Revisit trigger

- When RUNTIME-DOMAIN-PR-4A skeleton implementation begins.
- If the validation integration model, decision model, or invariant family model requires revision during implementation.
- If kernel validation pipeline interfaces change during validation integration implementation.
- If a doctrine gap escalation reveals a missing invariant family.

### No-implementation guardrails reaffirmed

- No validation integration code.
- No invariant enforcement code.
- No domain validation rules.
- No executable validators.
- No runtime mutation.
- No command execution.
- No action resolution.
- No transaction execution.
- No event commitment.
- No state delta application.
- No event ledger append.
- No persistence writes.
- No replay engine.
- No resource math.
- No combat rules.
- No ability/effect rules.
- No inventory behavior.
- No mission/social behavior.
- No generated-content persistence.
- No context-packet compiler.
- No prompt templates.
- No model integration.
- No model routing.
- No live-play adapter.
- No UI/client.
- No donor conversion.
- No sourcebook inclusion.
- No canon promotion.

### Classification

```yaml
runtime_domain_pr_4:
  plan_id: RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001
  artifact_type: validation_integration_invariant_enforcement_service_plan
  implementation_status: non_executable_plan
  defines_validation_integration_model: true
  defines_invariant_enforcement_model: true
  defines_validation_decision_model: true
  defines_invariant_family_model: true
  defines_validation_failure_routing: true
  defines_hidden_information_validation_safety: true
  defines_generated_content_provenance_validation: true
  authorizes_validation_integration_code_by_this_pr: false
  authorizes_invariant_enforcement_code_by_this_pr: false
  authorizes_domain_validation_rules_by_this_pr: false
  authorizes_runtime_code_by_this_pr: false
  authorizes_domain_code_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_event_ledger_append_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-4A validation integration and invariant enforcement skeleton implementation, pending review
```

---

## RUNTIME-DOMAIN-PR-4B-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-REVIEW-001

**Date:** 2026-06-11

### Decision

Review/gate-only status recorded for PR-4B. The review confirms PR-4A stayed within its authorized validation integration skeleton scope and did not add validation execution, invariant enforcement, mutation, event append, persistence, replay, model, live-play, conversion, or canon behavior.

### Findings

Primary findings: constants and reference-only kernel posture are acceptable; anti-authority guardrails are acceptable; domain package guardrail transition is safe. Semantic and traceability gaps were found: successful validation can omit `validation_result_ref_id` and `trace_id`, can remain `blocking=True`, can use loose final-stage combinations, and can pass generated-content paths without result-side provenance linkage. Terminal failure, quarantine, escalation, unsupported-scope, and failure-route semantics lack sufficient cross-field compatibility and trace linkage. Hidden-information flags exist, but player-visible route safety needs a future sanitized reason-code boundary.

### Implication

PR-4C is required before PR-5 planning. The selected next step is RUNTIME-DOMAIN-PR-4C validation integration skeleton hardening, pending review. PR-4B authorizes no runtime code, no domain-service code, no validation rule execution, no invariant enforcement, no validation pipeline execution, no state mutation, no state delta application, no event ledger append, no transaction execution, no actual event commitment, no persistence, no replay, no command execution, no resource math, no combat, no ability/effect resolution, no inventory mutation, no mission/social mutation, no generated-content persistence, no context-packet compiler, no model integration, no live-play adapter, no UI/client, no conversion, no sourcebook inclusion, and no canon promotion.

### Revisit trigger

- When RUNTIME-DOMAIN-PR-4C begins.
- If validation result, failure-route, trace, provenance, or hidden-information compatibility rules change before PR-5 planning.

### Classification

```yaml
runtime_domain_pr_4b_decision:
  artifact_type: review_gate_only
  reviews_pr_4a: true
  semantic_gaps_found: true
  traceability_gaps_found: true
  pr_4c_required_before_pr_5: true
  selected_next_step: RUNTIME-DOMAIN-PR-4C validation integration skeleton hardening, pending review
  full_non_implementation_boundary: true
```

---

## RUNTIME-DOMAIN-PR-4C-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-001

**Date:** 2026-06-11

### Decision

PR-4B required PR-4C before PR-5 Resource / Consequence Math planning. This entry records narrow executable skeleton hardening for the validation integration and invariant enforcement surface.

### Hardening recorded

- Decision/stage compatibility is now enforced.
- Successful results require non-blocking posture, a validation result reference, a trace reference, and the correct final stage.
- Terminal failures require failure routes and traceability.
- Quarantine and escalation semantics are aligned with their route types and decisions.
- Generated-content success requires result-side provenance linkage.
- Player-visible failure routes use sanitized public reason codes and safe public serialization.
- Request stages cannot claim terminal outcomes.
- No validation execution or runtime authority is added.

### Implication

PR-5 remains blocked pending PR-4D review. PR-4C adds no validation rule execution, invariant enforcement, validation pipeline execution, state mutation, state delta application, event append, persistence, replay, command execution, resource math, model integration, live-play behavior, UI behavior, conversion behavior, sourcebook inclusion, or canon promotion.

### Next step

RUNTIME-DOMAIN-PR-4D validation integration skeleton hardening review gate

### Classification

```yaml
runtime_domain_pr_4c_decision:
  artifact_type: executable_skeleton_hardening
  implementation_status: narrow_executable_skeleton_hardening
  pr_4b_required_pr_4c: true
  decision_stage_compatibility_enforced: true
  successful_results_require_non_blocking_result_ref_trace_and_correct_stage: true
  terminal_failures_require_routes_and_traceability: true
  quarantine_and_escalation_semantics_aligned: true
  generated_content_success_requires_provenance_linkage: true
  player_visible_routes_use_sanitized_reason_codes: true
  request_stages_cannot_claim_terminal_outcomes: true
  adds_validation_execution: false
  adds_runtime_authority: false
  pr_5_blocked_pending_pr_4d: true
  selected_next_step: RUNTIME-DOMAIN-PR-4D validation integration skeleton hardening review gate
```

---

## RUNTIME-DOMAIN-PR-4D-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-REVIEW-001

**Date:** 2026-06-11

### Decision

Review/gate-only status recorded for PR-4D. The review confirms PR-4C remained within its authorized hardening scope and added no validation execution, invariant evaluation, mutation, event append, persistence, replay, command execution, resource math, model integration, live-play behavior, UI behavior, conversion behavior, sourcebook inclusion, or canon promotion.

### Findings

PR-4B blockers are partially closed. PR-4C closes the focused blocker set for successful-result references and traces, blocking posture, decision/final-stage compatibility, terminal routes, rejected-route matching, quarantine/escalation compatibility, trace-required linkage, generated-content success provenance linkage, sanitized public reason codes, unsupported-scope routing, request-stage restrictions, invariant-precheck references, failure-route blocking, and factory/validator parity.

Material residual findings remain: route `subject_ref_id` can differ from result `subject_ref_id`; result subjects are not linked to request subjects; trace and validation-result references are shape-only; generated-content provenance references are untyped and can be unrelated-looking; `validation_ready` can carry hidden-information-unsafe posture; and stage/flag contradictions remain possible for ready intermediate states.

### Implication

PR-4E is required before PR-5 planning. PR-5 planning is not authorized by this decision. The selected next step is RUNTIME-DOMAIN-PR-4E validation integration residual skeleton hardening, pending review.

PR-4D preserves the full non-implementation boundary: no runtime code, no domain-service code, no validation implementation changes, no validation execution, no invariant evaluation, no state mutation, no state-delta application, no event append, no transaction execution, no actual event commitment, no persistence, no replay, no command execution, no resource math, no combat, no abilities/effects, no inventory mutation, no mission/social mutation, no generated-content persistence, no context-packet compiler, no model integration, no live-play adapter, no UI/client, no conversion, no sourcebook inclusion, and no canon promotion.

### Classification

```yaml
runtime_domain_pr_4d_decision:
  artifact_type: review_gate_only
  reviews_pr_4c: true
  pr_4b_blockers_closed: partially
  material_residual_findings: true
  pr_4e_required_before_pr_5: true
  pr_5_planning_authorized: false
  selected_next_step: RUNTIME-DOMAIN-PR-4E validation integration residual skeleton hardening, pending review
  full_non_implementation_boundary: true
```

---

## RUNTIME-DOMAIN-PR-4E-VALIDATION-INTEGRATION-RESIDUAL-SKELETON-HARDENING-001

**Date:** 2026-06-11

### Decision

PR-4D required PR-4E before PR-5 Resource / Consequence Math planning. PR-4E is narrow executable skeleton hardening for validation integration residual object-shape and identity-linkage defects.

### Hardening recorded

- Cross-subject routes now require explicit typed relationships.
- Same-subject routes must match the result subject.
- Result subjects are bound structurally to request subjects.
- Result request, trace, validation-result, and provenance references are linked through typed dependencies.
- Dependency uniqueness is enforced.
- `validation_ready` cannot be hidden-information unsafe.
- Intermediate checked stages align with their flags.
- No validation execution or runtime authority is added.

### Implication

PR-5 remains blocked pending PR-4F review. PR-4E adds no validation execution, invariant execution, state mutation, state delta application, event append, persistence, replay, command execution, resource or consequence math, model behavior, live-play behavior, UI behavior, conversion behavior, sourcebook inclusion, or canon promotion.

### Next step

RUNTIME-DOMAIN-PR-4F validation integration residual hardening review gate

### Classification

```yaml
runtime_domain_pr_4e_decision:
  artifact_type: executable_skeleton_hardening
  implementation_status: narrow_residual_skeleton_hardening
  pr_4d_required_pr_4e: true
  explicit_typed_cross_subject_relationships_required: true
  same_subject_routes_match_result_subject: true
  result_subjects_bound_to_request_subjects: true
  typed_request_trace_result_and_provenance_dependencies: true
  dependency_uniqueness_enforced: true
  validation_ready_hidden_information_safe_required: true
  intermediate_checked_stages_align_with_flags: true
  adds_validation_execution: false
  adds_runtime_authority: false
  pr_5_blocked_pending_pr_4f: true
  selected_next_step: RUNTIME-DOMAIN-PR-4F validation integration residual hardening review gate
```

---

## RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001

**Date:** 2026-06-11

### Decision

PR-4F is a review/gate-only artifact. It reviews PR-4E residual validation-integration hardening and records that PR-4D blockers are closed for PR-5 planning. PR-4F adds no runtime code, no domain-service code, and no validation implementation changes.

### Findings

Material PR-4D blockers are closed for planning: subject relations are explicit; same-subject and cross-subject route semantics are shape-checked; result/request subject declarations are bound; validation request, runtime trace, validation result, and generated-content provenance dependencies are typed and exact; dependency IDs and bindings are unique; `validation_ready` is hidden-information safe; intermediate checked stages are consistent; and factory/validator parity is acceptable.

Residual findings remain but do not require PR-4G before PR-5 planning: route-type/relation compatibility, cross-subject route dependency binding, primary subject dependency binding, request/trace/result dereference, provenance-object linkage, duplicate route IDs, route priority, request trace policy, dependency hidden-info posture, recursive metadata immutability, and typed identity grammar are implementation or executable-validation concerns.

### Implication

PR-4G is not required before PR-5 planning. PR-5 planning is authorized. The selected next step is RUNTIME-DOMAIN-PR-5 resource and consequence math service planning, pending review.

Full non-implementation boundary: no runtime code, no domain-service code, no validation implementation changes, no validation execution, no invariant evaluation, no state mutation, no state-delta application, no event append, no transaction execution, no actual event commitment, no persistence, no replay, no command execution, no resource math, no consequence application, no combat, no abilities/effects, no inventory mutation, no mission/social mutation, no generated-content persistence, no context-packet compiler, no model integration, no live-play adapter, no UI/client, no conversion, no sourcebook inclusion, and no canon promotion.

### Classification

```yaml
runtime_domain_pr_4f_decision:
  artifact_type: review_gate_only
  reviews_pr_4e: true
  pr_4d_blockers_closed_for_pr_5_planning: true
  material_residual_findings_before_planning: false
  residual_findings_deferred_to_implementation_or_execution: true
  pr_4g_required_before_pr_5: false
  pr_5_planning_authorized: true
  selected_next_step: RUNTIME-DOMAIN-PR-5 resource and consequence math service planning, pending review
  full_non_implementation_boundary: true
```

---

## RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001

**Date:** 2026-06-11

### Decision

planning-only status recorded for PR-5. PR-5 follows PR-4F authorization and records a resource and consequence math service plan for roughly 200-400 mixed donor sources. It creates no runtime/domain module and does not create `src/astra_runtime/domain/resource_consequence_math.py`.

### Findings

The plan records the backend-first invariant that the LLM is not the game engine. It assigns RT-002 ownership for future resource quantity, cost bundle, consequence quantity, deterministic numeric representation, unit/dimension, rounding, audit-lineage, and settlement-proposal math boundaries while preserving explicit non-ownership for RT-001 through RT-012 handoffs. It separates declaration, calculation, affordability, reservation proposal, settlement proposal, commitment, persistence, replay, and audit. It records that validation_ready is not validation_passed.

The corrected plan adds exact proposed stage, decision, family, policy, quantity-kind, atomicity, and dependency vocabularies; dataclass field contracts; factory/validator invariants; decision/stage compatibility; bundle, term, subject, unit, provenance, trace, validation, and dependency linkage; and false-only mutation, commitment, persistence, RNG/table, and model-authority flags. It also adds detailed resource/cost/consequence family matrices and a decision ledger separating work required before PR-5A, before executable calculation, and before settlement or commitment.

The plan is sufficient to select one next step. PR-5B must be planning-only and non-implementing.

### Implication

The selected next step is RUNTIME-DOMAIN-PR-5B Resource and Consequence Math Planning Hardening, pending review. PR-5B may only harden planning prose, registry tracking, decision logging, and focused tests; it may not create runtime/domain modules or reference-only skeleton surfaces. PR-5A remains blocked until PR-5B hardening is reviewed.

PR-5 preserves the full non-implementation boundary: no runtime code, no domain-service code, no resource math, no consequence application, no formulas or values, no final resource names or pools, no final currencies or economies, no affordability execution, no reservation or settlement, no expression parsing or evaluation, no RNG/table execution, no state mutation, no state-delta application, no event append or commitment, no persistence or replay, no combat, no abilities/effects, no inventory mutation, no mission/social mutation, no generated-content persistence, no model integration, no live-play adapter, no UI/client, no conversion, no sourcebook inclusion, and no canon promotion.

### Classification

```yaml
runtime_domain_pr_5_decision:
  artifact_type: service_plan_only
  implementation_status: planning_only
  follows_pr_4f: true
  backend_first_invariant: true
  llm_is_not_game_engine: true
  rt_002_ownership_recorded: true
  explicit_non_ownership_recorded: true
  validation_ready_is_not_validation_passed: true
  corpus_scale_donor_pressure_review: true
  lawful_donor_outcomes_recorded: true
  selects_exactly_one_next_step: true
  selected_next_step: RUNTIME-DOMAIN-PR-5B Resource and Consequence Math Planning Hardening, pending review
  pr_5b_must_be_planning_only_and_non_implementing: true
  exact_vocabularies_added: true
  field_contracts_added: true
  factory_validator_invariants_added: true
  decision_stage_compatibility_added: true
  linkage_requirements_added: true
  false_only_authority_flags_added: true
  family_matrices_added: true
  decision_ledger_separates_required_before_pr_5a_executable_calculation_and_settlement_commitment: true
  full_non_implementation_boundary: true
```
---

## RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001

**Date:** 2026-06-11

### Decision

Planning hardening only is recorded for PR-5B. PR-5B follows PR-5 and defines exact contracts for future resource/consequence math constant surfaces, stage and decision compatibility, dataclass fields, defaults, validation rules, dependency rules, authority boundaries, serialization behavior, family matrices, numeric/unit/conversion ledgers, validation handoffs, and unresolved risk classifications.

### Findings

PR-5B preserves the backend-first invariant that the LLM is not the game engine. It records that RT-002 produces reference-only planning contracts at this stage, no resource truth changes because a request/result/proposal exists, validation_ready is not validation_passed, settlement proposals are not committed state, and donor terminology is not Astra authority. It hardens all PR-5 proposal surfaces without creating `src/astra_runtime/domain/resource_consequence_math.py` or any runtime/domain implementation module.

### Implication

PR-5A remains blocked. The sole next step is **RUNTIME-DOMAIN-PR-5C resource and consequence math planning hardening review gate**. PR-5B authorizes no implementation, runtime code, domain code, resource calculation, consequence calculation, affordability execution, reservation, settlement, mutation, event commitment, persistence, RNG execution, model integration, conversion, or canon promotion.

### Classification

```yaml
runtime_domain_pr_5b_decision:
  artifact_type: planning_hardening_only
  follows_pr_5: true
  exact_contracts_defined: true
  pr_5a_remains_blocked: true
  pr_5c_is_sole_next_step: true
  no_implementation_authority: true
  gate_finding: ready_for_pr_5c_review_gate
  next_step_authorized: RUNTIME-DOMAIN-PR-5C resource and consequence math planning hardening review gate
  next_step_status: review_gate_only
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  resource_calculation_authorized_by_this_pr: false
  consequence_calculation_authorized_by_this_pr: false
  affordability_execution_authorized_by_this_pr: false
  reservation_authorized_by_this_pr: false
  settlement_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  persistence_authorized_by_this_pr: false
  rng_execution_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
```

---

## RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001

**Date:** 2026-06-11

### Decision

Review-gate-only status is recorded for PR-5C. The review evaluates PR-5B resource/consequence math planning hardening and selects exactly one next step: **RUNTIME-DOMAIN-PR-5D resource and consequence math final planning hardening**.

### Major findings

PR-5B stayed within its planning-only scope and preserved the backend-first invariant that the LLM is not the game engine. The review also finds material shape/contract defects that would force PR-5A to invent behavior: validation posture is not a controlled vocabulary or typed validation dependency; subject references are not paired with subject types; some defaults do not clearly belong to governing constant surfaces; ConsequenceTerm timing/outcome defaults need hardening; quarantine and escalation must be blocking/terminal rather than non-blocking planning; dependency references need structural linkage; bundle minimum/maximum semantics need exact rules; proposal validation linkage needs exact rules; public serialization ownership must route through RT-005 or remain explicitly internal-only.

### Implication

PR-5D is required before PR-5A. PR-5A is not authorized by this gate. The sole next step is PR-5D final planning hardening. This review authorizes no implementation, runtime code, domain code, resource calculation, consequence calculation, affordability execution, reservation, settlement, state mutation, state-delta application, transaction execution, event commitment, event append, persistence, replay, RNG/table execution, model integration, live-play/UI behavior, conversion, sourcebook inclusion, or canon promotion.

### Classification

```yaml
runtime_domain_pr_5c_decision:
  artifact_type: resource_consequence_math_planning_hardening_review_gate
  implementation_status: non_executable_review_gate
  reviews_pr_5b: true
  pr_5d_required_before_pr_5a: true
  pr_5a_authorized: false
  next_step_authorized: RUNTIME-DOMAIN-PR-5D resource and consequence math final planning hardening
  next_step_status: planning_hardening_pending_review
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  resource_calculation_authorized_by_this_pr: false
  consequence_calculation_authorized_by_this_pr: false
  affordability_execution_authorized_by_this_pr: false
  reservation_authorized_by_this_pr: false
  settlement_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  persistence_authorized_by_this_pr: false
  rng_execution_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
```

---

## RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001

**Date:** 2026-06-11

### Decision

Planning-hardening-only status is recorded for PR-5D. PR-5D follows PR-5C, closes the PR-5C contract defects, keeps PR-5A blocked, and selects exactly one next step: **RUNTIME-DOMAIN-PR-5E resource and consequence math final planning hardening review gate**.

### Implication

PR-5D authorizes no implementation, runtime code, domain code, calculation, affordability execution, consequence application, settlement, state mutation, event commitment, persistence, RNG execution, model integration, conversion, or canon promotion. PR-5A remains blocked until PR-5E accepts the final planning contracts.

### Classification

```yaml
runtime_domain_pr_5d_decision:
  artifact_type: final_planning_hardening
  planning_hardening_only: true
  follows_pr_5c: true
  closes_pr_5c_contract_defects: true
  pr_5a_remains_blocked: true
  pr_5e_is_sole_next_step: true
  no_implementation_authority: true
  next_step_authorized: RUNTIME-DOMAIN-PR-5E resource and consequence math final planning hardening review gate
  next_step_status: review_gate_only
```

---

## RUNTIME-DOMAIN-PR-5E-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-REVIEW-001

**Date:** 2026-06-11

### Decision

review-only status is recorded for PR-5E. PR-5E reviews PR-5D closure claims and selects exactly one next step: **RUNTIME-DOMAIN-PR-5F resource and consequence math residual planning hardening**. PR-5A is not authorized.

### Findings

PR-5D scope is confirmed as planning/tracking only: no runtime/domain implementation, no kernel changes, no `src/astra_runtime/domain/resource_consequence_math.py`, and PR-5A remained blocked. PR-5D closes many PR-5C defects, including free-string validation posture, typed subject identity, quarantine/escalation blocking, consequence policy ownership, serialization ownership, and false-only authority.

Residual blockers remain before PR-5A: external subject/unit/dimension reference fields lack typed dependency categories or exact exemptions; optional unsatisfied dependencies cannot be safely evaluated against those missing categories; precision, source-literal control-character/multiline behavior, and negative-value policy validator results are not exact; CostTerm and ConsequenceTerm optional resource/quantity combinations are incomplete; `maximum_allowed_terms` needs clarification under the declaration-bound rule; SettlementProposal-to-result validation equality and blocked/quarantined/escalated/validation-ready result exclusion rules are incomplete; and event-only consequence proposal handling needs an exact state-delta or event-route decision.

### Implication

PR-5F is required before PR-5A. The sole next step is **RUNTIME-DOMAIN-PR-5F resource and consequence math residual planning hardening**. This review authorizes no implementation, runtime code, domain code, calculation, affordability execution, consequence application, settlement, state mutation, event commitment, persistence, RNG execution, model integration, conversion, or canon promotion.

### Classification

```yaml
runtime_domain_pr_5e_decision:
  artifact_type: final_planning_hardening_review_gate
  implementation_status: review_only
  reviews_pr_5d: true
  pr_5d_scope_confirmed: true
  pr_5c_blockers_closed: partially
  residual_blockers_exist: true
  pr_5f_required_before_pr_5a: true
  pr_5a_authorized: false
  exactly_one_next_step: true
  next_step_authorized: RUNTIME-DOMAIN-PR-5F resource and consequence math residual planning hardening
  next_step_status: planning_hardening_pending_review
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  calculation_authorized_by_this_pr: false
  affordability_execution_authorized_by_this_pr: false
  consequence_application_authorized_by_this_pr: false
  settlement_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  persistence_authorized_by_this_pr: false
  rng_execution_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
```

---

## RUNTIME-DOMAIN-PR-5F-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-001

**Date:** 2026-06-11

### Decision

planning-hardening-only status is recorded for PR-5F. PR-5F follows PR-5E, closes PR-5E residual blockers, keeps PR-5A blocked, and selects exactly one next step: **RUNTIME-DOMAIN-PR-5G resource and consequence math residual planning hardening review gate**.

### Implication

PR-5G is the sole next step. PR-5F records residual planning corrections for subject/unit/dimension dependencies, optional dependency semantics, precision, source literals, negative policies, blocked numeric choice, term value modes, term policy routes, bundle bounds, inherited atomicity literal alignment, result/request aggregate validation, proposal/result compatibility, event-only routing, internal/external reference integrity, and factory/validator parity. It grants no implementation authority.

### Classification

```yaml
runtime_domain_pr_5f_decision:
  artifact_type: residual_planning_hardening
  planning_hardening_only: true
  follows_pr_5e: true
  closes_pr_5e_residual_blockers: true
  pr_5a_remains_blocked: true
  pr_5g_is_sole_next_step: true
  no_implementation_authority: true
  ready_for_pr_5g_review_gate: true
  ready_for_pr_5a_implementation: false
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  calculation_authorized_by_this_pr: false
  affordability_execution_authorized_by_this_pr: false
  consequence_application_authorized_by_this_pr: false
  settlement_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  persistence_authorized_by_this_pr: false
  rng_execution_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-5G resource and consequence math residual planning hardening review gate
  next_step_status: review_gate_only
```

---

## RUNTIME-DOMAIN-PR-5G-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-REVIEW-001

**Date:** 2026-06-11

### Decision

review-only status is recorded for PR-5G. PR-5G reviews PR-5F closure claims and selects exactly one next step: **RUNTIME-DOMAIN-PR-5H resource and consequence math final residual planning hardening**. PR-5A is not authorized.

### Findings

PR-5F scope is confirmed as planning/tracking only: four-file footprint, no runtime/domain implementation changes, no `src/astra_runtime/domain/resource_consequence_math.py`, consistent registry and decision tracking, PR-5A remained blocked, and PR-5G was the sole next step.

PR-5E blockers are partially closed. PR-5F closes subject/unit/dimension dependency types, term value modes, policy-only routes, blocked numeric choice routing, proposal/result equality, event-only routing, and much of the quantity and aggregate-validation surface. PR-5H is required because remaining material defects would force PR-5A to invent behavior: one final effective contract matrix, complete inherited atomicity/ordering/partial-settlement compatibility, unsatisfied binding dependency lifecycle, empty typed-scope legality, simultaneous blocker precedence, source-supported negative literal character posture, proposal/request validation prerequisite, and final factory/validator parity.

### Implication

PR-5H is required before PR-5A. PR-5A is not authorized. The sole next step is **RUNTIME-DOMAIN-PR-5H resource and consequence math final residual planning hardening**. This review authorizes no implementation, runtime code, domain code, calculation, affordability execution, consequence application, settlement, state mutation, event commitment, persistence, RNG execution, model integration, conversion, or canon promotion.

### Classification

```yaml
runtime_domain_pr_5g_decision:
  artifact_type: residual_planning_hardening_review_gate
  implementation_status: review_only
  reviews_pr_5f: true
  pr_5f_scope_confirmed: true
  pr_5e_blockers_closed: partially
  pr_5h_required_before_pr_5a: true
  pr_5a_authorized: false
  exactly_one_next_step: true
  next_step_authorized: RUNTIME-DOMAIN-PR-5H resource and consequence math final residual planning hardening
  next_step_status: planning_hardening_pending_review
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  calculation_authorized_by_this_pr: false
  affordability_execution_authorized_by_this_pr: false
  consequence_application_authorized_by_this_pr: false
  settlement_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  persistence_authorized_by_this_pr: false
  rng_execution_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
```

---

## RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001

**Date:** 2026-06-11

### Decision

PR-5H is recorded as planning-only final residual hardening for RT-002 resource and consequence math. It closes the eight remaining PR-5G defects: consolidated effective contract inventory; complete CostBundle compatibility surface; exact dependency lifecycle; exact typed-result-scope cardinality and closure; simultaneous blocker precedence; universal source-literal consistency; request/result/proposal validation architecture; and factory/validator parity.

### Implication

PR-5A remains blocked and unauthorized. PR-5H grants no implementation authority, runtime code, domain code, calculation, affordability execution, consequence application, settlement, state mutation, event commitment, persistence, RNG execution, model integration, conversion, or canon promotion. The only next step authorized by PR-5H is **RUNTIME-DOMAIN-PR-5I: Resource and Consequence Math Final Residual Planning Hardening Review Gate**.

PRs #278 and #279 were abandoned, not merged, and are non-authoritative. They are not a base, precedent, doctrine source, or test source for PR-5H.

### Classification

```yaml
runtime_domain_pr_5h_decision:
  artifact_type: final_residual_planning_hardening
  planning_only: true
  closes_eight_pr_5g_defects: true
  pr_5a_blocked: true
  pr_5a_authorized: false
  pr_5i_only_next_step: true
  no_implementation_authority: true
  abandoned_prs_278_279_non_authoritative: true
```

---

## RUNTIME-DOMAIN-PR-5I-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-REVIEW-001

**Date:** 2026-06-12

### Decision

PR-5I is recorded as a review-only final residual planning hardening review gate for RT-002 resource and consequence math. It reviews **RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001** on current main and does not use abandoned PRs #278 or #279 as authority.

PR-5I finds all eight PR-5G defects closed by PR-5H: consolidated effective contract inventory; complete CostBundle compatibility surface; exact dependency lifecycle; exact typed-result-scope cardinality and closure; simultaneous blocker precedence; universal source-literal consistency; request/result/proposal validation architecture; and factory/validator parity.

### Implication

Selected gate outcome: **AUTHORIZE_PR_5A**. PR-5A is authorized as the sole next step only for the future narrow reference-only skeleton: immutable frozen keyword-only shapes, exact constants, exact factories and validators, internal defensive serialization, domain exports, and focused tests.

PR-5I itself creates no runtime/domain code and authorizes no formulas, arithmetic, expression parsing or evaluation, final resource pools or values, currencies or economies, affordability, reservation, settlement, consequence application, state mutation or delta application, transaction execution, event append or commitment, persistence, replay, RNG/table execution, combat, abilities, inventory, mission or social mechanics, public projection or redaction, model/live-play/UI behavior, conversion, sourcebook inclusion, or canon promotion. No owner boundary is expanded.

### Classification

```yaml
runtime_domain_pr_5i_decision:
  date: '2026-06-12'
  artifact_type: final_residual_planning_hardening_review_gate
  implementation_status: review_only
  reviewed_pr_5h_artifact: RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001
  reviewed_pr_5h_file: docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md
  closure_findings:
    consolidated effective contract inventory: closed
    complete CostBundle compatibility surface: closed
    exact dependency lifecycle: closed
    exact typed-result-scope cardinality and closure: closed
    simultaneous blocker precedence: closed
    universal source-literal consistency: closed
    request/result/proposal validation architecture: closed
    factory/validator parity: closed
  selected_gate_outcome: AUTHORIZE_PR_5A
  pr_5h_accepted: true
  pr_5a_authorized_as_sole_next_step: true
  pr_5a_status: narrow_reference_only_skeleton_authorized
  exactly_one_next_step: true
  next_step_authorized: RUNTIME-DOMAIN-PR-5A Resource and Consequence Math Skeleton Implementation
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  calculation_authorized_by_this_pr: false
  affordability_execution_authorized_by_this_pr: false
  reservation_authorized_by_this_pr: false
  settlement_authorized_by_this_pr: false
  consequence_application_authorized_by_this_pr: false
  mutation_authorized_by_this_pr: false
  state_delta_application_authorized_by_this_pr: false
  transaction_execution_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  event_append_authorized_by_this_pr: false
  persistence_authorized_by_this_pr: false
  replay_authorized_by_this_pr: false
  rng_execution_authorized_by_this_pr: false
  table_oracle_execution_authorized_by_this_pr: false
  model_authority_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  ui_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  sourcebook_inclusion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
  no_canon_or_conversion_authority: true
```

---

## RUNTIME-DOMAIN-PR-5A-RESOURCE-CONSEQUENCE-MATH-SKELETON-IMPLEMENTATION-001

**Date:** 2026-06-12

### Decision

RUNTIME-DOMAIN-PR-5A — Resource and Consequence Math Skeleton Implementation is recorded as implemented on branch `runtime-gate-b/pr-5a-resource-consequence-math-skeleton`.

Authority: PR-5H effective contract, authorized by PR-5I / PR #281.

Scope: narrow RT-002 reference-only skeleton.

### Implemented

- All ten frozen keyword-only shapes: `ResourceMathSubjectReference`, `ResourceReference`, `QuantitySpecification`, `ResourceMathDependency`, `CostTerm`, `ConsequenceTerm`, `CostBundle`, `ResourceMathRequest`, `ResourceMathResult`, `SettlementProposal`.
- Exact controlled constants from the PR-5H effective contract.
- Factory/validator parity: one `create_*` and one `validate_*` helper per shape.
- Defensive internal serialization (`to_dict()`) on every shape.
- Package exports from `astra_runtime.domain`.
- Focused skeleton tests (273 passing).
- Updated obsolete domain-module guardrails in 15 runtime guardrail tests so the new `resource_consequence_math.py` module is recognized in the runtime domain-module allowlist.

### Explicit non-authorities preserved

- No formulas or arithmetic.
- No affordability, reservation, settlement execution, or consequence application.
- No state mutation or state-delta application.
- No transaction execution or event commitment/append.
- No persistence or replay.
- No RNG, dice, tables, or oracle execution.
- No combat, ability, inventory, mission, or social mechanics.
- No public projection or hidden-information release.
- No model/live-play/UI behavior.
- No conversion/sourcebook/canon promotion.

### Next step

Review/merge PR-5A before starting PR-6.

### Classification

```yaml
runtime_domain_pr_5a_decision:
  date: '2026-06-12'
  artifact_type: executable_domain_skeleton
  implementation_status: narrow_reference_only_skeleton
  derives_from:
    - RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001
    - RUNTIME-DOMAIN-PR-5I-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-REVIEW-001
  implements_resource_consequence_math_skeleton: true
  implements_all_ten_shapes: true
  implements_exact_controlled_constants: true
  implements_factory_validator_parity: true
  implements_defensive_internal_serialization: true
  implements_domain_exports: true
  implements_focused_skeleton_tests: true
  updates_runtime_guardrail_allowlists: true
  calculation_executed: false
  affordability_executed: false
  reservation_authorized: false
  settlement_authorized: false
  consequence_application_authorized: false
  mutation_authorized: false
  state_delta_application_authorized: false
  transaction_execution_authorized: false
  event_commitment_authorized: false
  event_append_authorized: false
  persistence_authorized: false
  replay_authorized: false
  rng_execution_authorized: false
  table_oracle_execution_authorized: false
  model_authority_authorized: false
  model_integration_authorized: false
  live_play_authorized: false
  ui_authorized: false
  conversion_authorized: false
  sourcebook_inclusion_authorized: false
  canon_promotion_authorized: false
  public_projection_authorized: false
  redaction_authorized: false
  hidden_information_release_authorized: false
  next_step_authorized: review/merge PR-5A before starting PR-6
  no_canon_or_conversion_authority: true
```

---

## RUNTIME-DOMAIN-PR-6 — Context Packet Compiler v0.1 Scope Alignment

**Date:** 2026-06-12

### Decision

RUNTIME-DOMAIN-PR-6 is realigned from its original PR-0 sequencing assignment (combat/hazard/damage/recovery service planning) to **Context Packet Compiler v0.1**.

PR-5A has been merged and unlocks PR-6 for this workstream.

### Authoritative PR-6 scope (current workstream)

- Single-event narration packet (`SingleEventNarrationPacket`).
- No-commit intent packet (`NoCommitIntentPacket`).
- Visible-summary packet (`VisibleSummaryPacket`).
- Backend-owned deterministic packet assembly.
- Visibility-safe packet contracts (no hidden information).
- Compact narrator-facing packet contracts suitable for constrained 8B models.

### Superseded scope

The older PR-0 sequencing plan (`runtime_domain_pr_0_domain_service_implementation_sequencing_plan.md`) that assigned PR-6 to combat/hazard/damage/recovery service planning is superseded for the current runtime workstream. Combat/hazard/damage/recovery service work is deferred/renumbered and not authorized by this PR-6 track.

### Authority sources

- Merged PR-5A (branch `runtime-gate-b/pr-5a-resource-consequence-math-skeleton`).
- `docs/doctrine/reviews/runtime_seq_pr_b_narration_context_packet_contract_plan.md` (RUNTIME-SEQ-PR-B).
- Current decision-log entry.

### Authorized work

This alignment entry authorizes only planning and implementation of context-packet skeleton shapes, constants, factories, validators, focused tests, and domain exports. It does not authorize live-play behavior.

### Explicit non-authorities

- No model authority.
- No narration generation.
- No live-play behavior.
- No hidden-information release.
- No state mutation.
- No state-delta application.
- No transaction execution.
- No event commitment.
- No persistence or replay.
- No RNG, dice, tables, or oracle execution.
- No combat, ability, inventory, mission, or social mechanics.
- No conversion, sourcebook inclusion, or canon promotion.

---

## RUNTIME-DOMAIN-PR-9-POST-PR8-RUNTIME-GENERALIZATION-PLANNING-001

**Date:** 2026-06-14

### Decision

RUNTIME-DOMAIN-PR-9 is a planning-only artifact that decides how to generalize the proof delivered by RUNTIME-DOMAIN-PR-8 (`Tiny Vertical Slice`, merged via PR #302) into a reusable, backend-owned runtime execution path. It selects a narrow "scene command execution skeleton" or "runtime transaction assembly" as the candidate next implementation and defines the constraints and gating tests for that implementation PR.

### Reason

PR #302 proved that a deterministic, backend-owned tiny vertical slice can be assembled end-to-end using the existing kernel skeletons, without collapsing authority into the LLM. PR #303 cleaned up the guardrail baseline after the rebase. Before broadening into live play, model integration, or full domain services, the project needs a planning gate that records what PR-8 proved, what it deliberately did not prove, and what narrow generalization seam comes next.

### Implication

- Authorizes only planning for the next narrow runtime generalization PR (tentatively RUNTIME-DOMAIN-PR-9A: Scene Command Execution Skeleton / Runtime Transaction Assembly).
- Does not authorize implementation code, expansion of `tiny_vertical_slice.py`, live-play behavior, LLM narration authority, persistence implementation, RNG/table/oracle execution, arbitrary state mutation, settlement, broad consequence application, PR-5 arithmetic execution, conversion, sourcebook inclusion, or canon promotion.
- Records PR-8 proofs, PR-8 non-proofs, generalization targets, candidate modules, backend-owned boundaries, forbidden LLM boundaries, gating tests, allowed touch surfaces, forbidden touch surfaces, and lawful escalation points to RT-001 through RT-012.
- Supersedes the PR-0 sequencing plan assignment of RUNTIME-DOMAIN-PR-9 to mission/reward/clue routing for the current runtime workstream; that assignment is deferred/renumbered and not authorized by this PR-9 track.

### Revisit trigger

- If RUNTIME-DOMAIN-PR-9A (scene command execution skeleton / runtime transaction assembly implementation) is authorized.
- If PR-8's proof assumptions are invalidated by new kernel interface changes.
- If generalization requires new doctrine beyond RT-001 through RT-012, triggering Astra Doctrine Council review.

### Classification block

```yaml
runtime_domain_pr_9:
  implementation_id: RUNTIME-DOMAIN-PR-9-POST-PR8-RUNTIME-GENERALIZATION-PLANNING-001
  artifact_type: post_pr8_runtime_generalization_planning
  implementation_status: non_executable_plan
  pr_8_proved_backend_owned_deterministic_assembly: true
  pr_8_did_not_prove_generalization: true
  defines_next_runtime_generalization_seam: true
  defines_implementation_constraints: true
  defines_required_tests_before_implementation: true
  next_implementation_candidate: scene_command_execution_skeleton_or_runtime_transaction_assembly
  authorizes_implementation_by_this_pr: false
  authorizes_tiny_vertical_slice_expansion_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_llm_narration_authority_by_this_pr: false
  authorizes_persistence_implementation_by_this_pr: false
  authorizes_rng_table_oracle_execution_by_this_pr: false
  authorizes_arbitrary_state_mutation_by_this_pr: false
  authorizes_settlement_authorization_by_this_pr: false
  authorizes_broad_consequence_application_by_this_pr: false
  authorizes_pr5_arithmetic_execution_by_this_pr: false
  authorizes_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-9A scene command execution skeleton or runtime transaction assembly implementation, pending review
```

### No-implementation guardrails

- `tiny_vertical_slice.py` remains a closed proof-of-concept.
- No live-play adapter package exists yet.
- No model integration package exists yet.
- No prompt template package exists yet.
- No UI/client package exists yet.
- No database package exists yet.
- No durable store package exists yet.
- No RNG/table/oracle execution module exists yet.

---

## RUNTIME-DOMAIN-PR-9A-SCENE-COMMAND-EXECUTION-SKELETON-001

**Date:** 2026-06-14

### Decision

RUNTIME-DOMAIN-PR-9A implements a narrow backend-owned typed scene command execution skeleton, generalizing the PR-8 tiny vertical slice into a reusable runtime transaction assembly path.

### Reason

PR #302 proved that a deterministic, backend-owned tiny vertical slice can be assembled end-to-end without collapsing authority into the LLM. PR #304 planned the next narrow generalization seam. This PR realizes that seam as a typed skeleton that consumes existing kernel and domain skeleton interfaces.

### Implication

- Adds `src/astra_runtime/domain/scene_command_execution_skeleton.py` as the sole new implementation module.
- Exports frozen dataclasses, factories, validators, and serializers through `src/astra_runtime/domain/__init__.py`.
- Adds focused tests in `tests/test_runtime_domain_pr_9a_scene_command_execution_skeleton.py`.
- Does not expand `tiny_vertical_slice.py`.
- Does not authorize live play, model calls, prompt execution, prose parsing, narration generation, persistence writes, RNG/table/oracle execution, state mutation, event append, settlement, PR-5 arithmetic execution, broad consequence application, conversion, sourcebook inclusion, or canon promotion.
- All authority flags on `SceneCommandExecutionAssemblyAuthorityFlags` remain explicitly `False`.

### Revisit trigger

- If the skeleton needs to expand beyond typed assembly into execution engines.
- If new kernel interfaces invalidate the assembly assumptions.
- If generalization requires doctrine beyond RT-001 through RT-012.

### Classification block

```yaml
runtime_domain_pr_9a:
  implementation_id: RUNTIME-DOMAIN-PR-9A-SCENE-COMMAND-EXECUTION-SKELETON-001
  artifact_type: scene_command_execution_skeleton
  implementation_status: skeleton_implementation
  follows_pr_9_planning: true
  generalizes_pr_8_tiny_vertical_slice: true
  backend_owned_typed_assembly: true
  authorizes_implementation_beyond_skeleton: false
  authorizes_live_play: false
  authorizes_model_calls: false
  authorizes_prompt_rendering: false
  authorizes_prose_parsing: false
  authorizes_narration_generation: false
  authorizes_persistence_writes: false
  authorizes_rng_table_oracle_execution: false
  authorizes_state_mutation: false
  authorizes_event_append: false
  authorizes_settlement: false
  authorizes_pr5_arithmetic_execution: false
  authorizes_consequence_application: false
  authorizes_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  touched_files:
    - src/astra_runtime/domain/scene_command_execution_skeleton.py
    - src/astra_runtime/domain/__init__.py
    - tests/test_runtime_domain_pr_9a_scene_command_execution_skeleton.py
    - docs/doctrine/astra_doctrine_registry_v0_1.yaml
    - docs/decisions/current_decisions_log.md
    - tests/test_runtime_domain_pr_0_domain_service_implementation_sequencing_plan.py
    - tests/test_runtime_domain_pr_1_command_lifecycle_action_legality_service_plan.py
    - tests/test_runtime_domain_pr_1b_command_lifecycle_action_legality_skeleton_review.py
    - tests/test_runtime_domain_pr_2_state_store_state_projection_service_plan.py
    - tests/test_runtime_domain_pr_2b_state_store_state_projection_skeleton_review.py
    - tests/test_runtime_domain_pr_3_transaction_lifecycle_event_commitment_service_plan.py
    - tests/test_runtime_domain_pr_3b_transaction_lifecycle_event_commitment_skeleton_review.py
    - tests/test_runtime_domain_pr_4_validation_integration_invariant_enforcement_service_plan.py
    - tests/test_runtime_domain_pr_4b_validation_integration_invariant_enforcement_skeleton_review.py
    - tests/test_runtime_domain_pr_4d_validation_integration_invariant_enforcement_skeleton_hardening_review.py
    - tests/test_runtime_domain_pr_4f_validation_integration_residual_hardening_review.py
    - tests/test_runtime_domain_pr_5_resource_consequence_math_service_plan.py
    - tests/test_runtime_domain_pr_5e_resource_consequence_math_final_planning_hardening_review.py
    - tests/test_runtime_domain_pr_5g_resource_consequence_math_residual_planning_hardening_review.py
    - tests/test_runtime_impl_pr_8_post_kernel_skeleton_review_domain_service_readiness_gate.py
    - tests/runtime/test_command_envelope_skeleton.py
    - tests/runtime/test_context_projection_skeleton.py
    - tests/runtime/test_domain_event_commitment_skeleton.py
    - tests/runtime/test_domain_state_store_skeleton.py
    - tests/runtime/test_domain_transaction_lifecycle_skeleton.py
    - tests/runtime/test_domain_validation_integration_skeleton.py
    - tests/runtime/test_event_ledger_skeleton.py
    - tests/runtime/test_hidden_information_skeleton.py
    - tests/runtime/test_persistence_boundary_skeleton.py
    - tests/runtime/test_replay_audit_skeleton.py
    - tests/runtime/test_rng_interface_skeleton.py
    - tests/runtime/test_runtime_trace_skeleton.py
    - tests/runtime/test_state_delta_skeleton.py
    - tests/runtime/test_table_oracle_skeleton.py
    - tests/runtime/test_validation_pipeline_skeleton.py
  next_allowed_step: review/merge of PR-9A, then planning for PR-9B or authorized runtime generalization implementation
```

### Non-implementation reaffirmation

- `tiny_vertical_slice.py` remains a closed proof-of-concept and was not modified.
- No live-play adapter, model integration, prompt template, UI/client, database, or durable store package was added.
- No RNG/table/oracle execution, state mutation, event append, settlement, conversion, or canon promotion behavior was implemented.

---

## RUNTIME-DOMAIN-PR-9B: Scene Command Execution Skeleton Hardening Review

**Date:** 2026-06-15
**Artifact ID:** RUNTIME-DOMAIN-PR-9B-SCENE-COMMAND-EXECUTION-HARDENING-REVIEW-001

### Decision

PR-9B is a review/hardening gate for PR-9A (scene command execution skeleton).
It audits, validates, and tightens the PR-9A skeleton before any new runtime
behavior is built on top of it. PR-9B adds no new runtime behavior.

### Reason

The PR-9A skeleton introduced a large new module (~1304 lines, 16 frozen
dataclasses) that generalizes the PR-8 tiny vertical slice into a reusable
backend-owned runtime transaction assembly path. Before building on it
(PR-9C or later), we need independent validation that:
- No names imply real execution or live-play behavior
- Hidden-info contracts don't leak into visible serialization
- PersistenceBoundaryRequest is treated as prepare-only
- Authority flags cover all denied authorities from PR-9
- No forbidden paths were introduced
- Guardrail allowlist updates are narrow
- tiny_vertical_slice.py was not modified

### Implication

PR-9C and subsequent runtime generalization work is blocked until PR-9B
is reviewed and merged.

### Revisit trigger

Revisit if PR-9A is discovered to have structural issues that require
a different skeleton shape, or if the authority flag set needs expansion
for newly identified denied authorities.

```yaml
classification:
  pr_id: RUNTIME-DOMAIN-PR-9B
  type: review-hardening-gate
  follows: RUNTIME-DOMAIN-PR-9A (merged as PR #305)
  audit_criteria_count: 12
  audit_findings: all 12 criteria passed
  hardening_actions:
    - review artifact added
    - focused hardening tests added
    - registry entry added
    - decision-log entry added
    - guardrail allowlists updated narrowly
  new_runtime_behavior: false
  authorized_live_play: false
  authorized_model_calls: false
  authorized_prompt_execution: false
  authorized_persistence_writes: false
  authorized_rng_execution: false
  authorized_state_mutation: false
  authorized_event_append: false
  authorized_settlement: false
  authorized_conversion: false
  authorized_canon_promotion: false
  authorized_command_kind_routing: false
  authorized_validation_bridge: false
  authorized_packet_bridge: false
  files_touched:
    - docs/doctrine/reviews/runtime_domain_pr_9b_scene_command_execution_hardening_review.md
    - docs/doctrine/astra_doctrine_registry_v0_1.yaml
    - docs/decisions/current_decisions_log.md
    - tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py
    - tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py
  next_allowed_step: review/merge of PR-9B, then planning for PR-9C or authorized runtime generalization implementation
```

### Non-implementation reaffirmation

- `tiny_vertical_slice.py` remains a closed proof-of-concept and was not modified.
- `scene_command_execution_skeleton.py` was not modified — only audited and validated.
- No live-play adapter, model integration, prompt template, UI/client, database, or durable store package was added.
- No RNG/table/oracle execution, state mutation, event append, settlement, conversion, or canon promotion behavior was implemented.
- No new runtime behavior was added.

## RUNTIME-DOMAIN-PR-9C: Command-Kind Routing Skeleton

**Date:** 2026-06-15
**Artifact ID:** RUNTIME-DOMAIN-PR-9C-COMMAND-KIND-ROUTING-SKELETON-001

### Decision

PR-9C implements a narrow backend-owned command-kind routing skeleton that
classifies command intent/envelope data into known command families and produces
dispatch-shell references to intended owner surfaces. It follows PR-9B (merged
as PR #306) and does not implement legality resolution, command execution,
runtime mutation, persistence, RNG, settlement, consequence application, model
calls, prompt execution, narration generation, or live play.

### Reason

The PR-9A scene command execution skeleton accepts arbitrary `command_type`
strings from `CommandEnvelope` but has no classification or routing layer. Before
building the PR-9D validation integration bridge, the runtime needs a declared
vocabulary of command families and a deterministic routing mechanism that maps
command types to intended owner surfaces without executing them.

### Implication

PR-9D (validation integration bridge) is unblocked but not implemented by PR-9C.
The routing skeleton provides classification metadata that PR-9D and later PRs
can consume, but the skeleton itself does not call, execute, or authorize any
owner surface.

### Revisit trigger

Revisit if new command families are needed for corpus-scale donor pressure
beyond the initial 14 families, or if the prefix-match classification mode
proves insufficient for complex multi-token command types.

```yaml
classification:
  pr_id: RUNTIME-DOMAIN-PR-9C
  type: implementation-skeleton
  follows: RUNTIME-DOMAIN-PR-9B (merged as PR #306)
  command_families_defined: 14
  authority_flags_denied: 20
  dataclasses_added: 6
  factory_functions_added: 7
  validator_functions_added: 6
  routing_functions_added: 3
  serialization_functions_added: 2
  new_runtime_behavior: false
  authorized_legality_resolution: false
  authorized_command_execution: false
  authorized_runtime_action_execution: false
  authorized_state_mutation: false
  authorized_event_append: false
  authorized_persistence_write: false
  authorized_rng_execution: false
  authorized_settlement: false
  authorized_pr5_arithmetic_execution: false
  authorized_consequence_application: false
  authorized_model_authority: false
  authorized_prompt_rendering: false
  authorized_prompt_execution: false
  authorized_prose_parsing: false
  authorized_narration_generation: false
  authorized_live_play: false
  authorized_ui_client: false
  authorized_conversion: false
  authorized_sourcebook_inclusion: false
  authorized_canon_promotion: false
  files_touched:
    - src/astra_runtime/domain/command_kind_routing_skeleton.py
    - src/astra_runtime/domain/__init__.py
    - tests/test_runtime_domain_pr_9c_command_kind_routing_skeleton.py
    - docs/doctrine/astra_doctrine_registry_v0_1.yaml
    - docs/decisions/current_decisions_log.md
    - guardrail allowlist updates across multiple test files
  next_allowed_step: review/merge of PR-9C, then PR-9D validation integration bridge
```

## RUNTIME-DOMAIN-PR-9D: Validation Integration Bridge Skeleton

**Date:** 2026-06-15

**Artifact ID:** RUNTIME-DOMAIN-PR-9D-VALIDATION-INTEGRATION-BRIDGE-SKELETON-001

PR-9D implements a narrow backend-owned validation integration bridge skeleton that
ties together PR-9A scene command execution assembly surfaces, PR-9C command-kind
routing results, and existing validation pipeline / validation integration skeleton
surfaces.

PR-9D follows merged PR #307 (PR-9C). It consumes PR-9C `CommandKindRoutingResult`
objects by reference without reclassifying commands. It references validation surfaces
without executing legality or validation rules.

Key implementation details:

- Creates `src/astra_runtime/domain/validation_integration_bridge_skeleton.py` with:
  - 7 error classes (`ValidationIntegrationBridgeSkeletonError`, `InvalidValidationBridgeRequestError`,
    `InvalidValidationBridgeSubjectRefError`, `InvalidValidationBridgeRequirementRefError`,
    `InvalidValidationBridgeResultRefError`, `InvalidValidationBridgeOwnerRouteRefError`,
    `InvalidValidationBridgeAuthorityFlagsError`, `InvalidValidationBridgeResultError`)
  - 4 reference dataclasses (`ValidationBridgeSubjectRef`, `ValidationBridgeRequirementRef`,
    `ValidationBridgeOwnerRouteRef`, `ValidationBridgeResultRef`)
  - Bridge request/result types (`ValidationIntegrationBridgeRequest`, `ValidationIntegrationBridgeResult`)
  - Authority flags (`ValidationIntegrationBridgeAuthorityFlags`) with 22 denied authorities
  - Factory functions, validator functions, deterministic serializer functions
- Bridge accepts: `CommandEnvelope` + `CommandKindRoutingResult` + optional `SceneCommandExecutionAssemblyRequest`,
  `SceneCommandExecutionValidationRef`, or kernel `ValidationResult`
- Bridge validates command references match between envelope and routing result
- Bridge produces pending `ValidationBridgeResultRef` when no `ValidationResult` is supplied
- Bridge carries command family/kind/owner route from PR-9C without reclassifying
- All authority flags default to False; constructing with any True flag raises an error
- Deterministic serialization with `MappingProxyType` for metadata immutability

Does not authorize:
+ legality resolution
+ validation rule execution
+ command execution
+ runtime action execution
+ state mutation
+ event append
+ persistence write
+ RNG/table/oracle execution
+ settlement authorization
+ PR-5 arithmetic execution
+ consequence application
+ packet compilation
+ model authority
+ prompt rendering
+ prompt execution
+ prose parsing
+ narration generation
+ live-play/session authority
+ UI/client authority
+ conversion
+ sourcebook inclusion
+ canon promotion

Unblocks later PR-9E transaction preview packet bridge but does not implement PR-9E.

### Summary statistics

```
  pr_id: RUNTIME-DOMAIN-PR-9D
  type: implementation-skeleton
  base_main_sha: ceeeffb15979596871441a0ec1a5d516f5941823
  branch: runtime-gate-b/pr-9d-validation-integration-bridge-skeleton
  files_added:
    - src/astra_runtime/domain/validation_integration_bridge_skeleton.py
    - tests/test_runtime_domain_pr_9d_validation_integration_bridge_skeleton.py
  files_modified:
    - src/astra_runtime/domain/__init__.py
    - docs/doctrine/astra_doctrine_registry_v0_1.yaml
    - docs/decisions/current_decisions_log.md
  error_classes_added: 8
  reference_dataclasses_added: 4
  request_result_dataclasses_added: 4
  authority_flags_denied: 22
  factory_functions_added: 7
  validator_functions_added: 8
  serialization_functions_added: 2
  new_runtime_behavior: false
  authorized_legality_resolution: false
  authorized_validation_rule_execution: false
  authorized_command_execution: false
  authorized_runtime_action_execution: false
  authorized_state_mutation: false
  authorized_event_append: false
  authorized_persistence_write: false
  authorized_rng_execution: false
  authorized_settlement: false
  authorized_pr5_arithmetic_execution: false
  authorized_consequence_application: false
  authorized_packet_compilation: false
  authorized_model_authority: false
  authorized_prompt_rendering: false
  authorized_prompt_execution: false
  authorized_prose_parsing: false
  authorized_narration_generation: false
  authorized_live_play: false
  authorized_ui_client: false
  authorized_conversion: false
  authorized_sourcebook_inclusion: false
  authorized_canon_promotion: false
  files_touched:
    - src/astra_runtime/domain/validation_integration_bridge_skeleton.py
    - src/astra_runtime/domain/__init__.py
    - tests/test_runtime_domain_pr_9d_validation_integration_bridge_skeleton.py
    - docs/doctrine/astra_doctrine_registry_v0_1.yaml
    - docs/decisions/current_decisions_log.md
  next_allowed_step: review/merge of PR-9D, then PR-9E transaction preview packet bridge
```

### Non-implementation reaffirmation

   - `tiny_vertical_slice.py` remains a closed proof-of-concept and was not modified.
   - `scene_command_execution_skeleton.py` was not modified.
   - `command_kind_routing_skeleton.py` was not modified.
   - No live-play adapter, model integration, prompt template, UI/client, database, or durable store package was added.
   - No legality resolution, validation rule execution, command execution, runtime action execution, state mutation, event append, persistence write, RNG/table/oracle execution, settlement authorization, PR-5 arithmetic execution, consequence application, packet compilation, conversion, sourcebook inclusion, or canon promotion behavior was implemented.
   - Bridge is reference-only — no owner surface is called or executed.

- `tiny_vertical_slice.py` remains a closed proof-of-concept and was not modified.
- `scene_command_execution_skeleton.py` was not modified.
- No live-play adapter, model integration, prompt template, UI/client, database, or durable store package was added.
- No legality resolution, command execution, state mutation, event append, persistence write, RNG/table/oracle execution, settlement, consequence application, conversion, sourcebook inclusion, or canon promotion behavior was implemented.
- Routing is classification and dispatch-shell reference only — no owner surface is called or executed.

## RUNTIME-DOMAIN-PR-9E: Transaction Preview Packet Bridge Skeleton

- **Status**: implemented (pending merge)
- **Date**: 2026-06-15
- **PR**: RUNTIME-DOMAIN-PR-9E
- **Purpose**: Creates a narrow backend-owned transaction preview packet bridge skeleton that compiles PR-9A assembly, PR-9C routing, PR-9D validation bridge, and kernel TransactionPreview surfaces into deterministic packet descriptor / packet reference shells.
- **Follows**: PR-9D (validation integration bridge skeleton)
- **Consumes**: PR-9A scene command execution assembly result, PR-9C command kind routing result, PR-9D validation integration bridge result, kernel TransactionPreview
- **Produces**: TransactionPreviewPacketBridgeResult with:
  - context packet descriptor (single_event_context_packet)
  - narration packet descriptor (single_event_narration_packet)
  - visible summary packet descriptor (visible_summary_packet)
  - no-commit intent packet descriptor (no_commit_intent_packet)
- **Files added**:
  - src/astra_runtime/domain/transaction_preview_packet_bridge_skeleton.py
  - tests/test_runtime_domain_pr_9e_transaction_preview_packet_bridge_skeleton.py
- **Files modified**:
  - src/astra_runtime/domain/__init__.py (exports)
  - docs/decisions/current_decisions_log.md (this entry)
  - tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py (domain allowlist)
  - tests/runtime/* guardrail test files (domain module allowlists)
- **Packet roles supported**: single_event_context_packet, single_event_narration_packet, visible_summary_packet, no_commit_intent_packet
- **Completions**:
  - Completes the PR-9A–9E post-PR-8 generalization seam
  - Enables a later decision on RT-001, RT-002, RT-009, persistence/replay, or further hardening
- **Authoritative denials**:
  - No packet delivery
  - No prompt rendering or prompt execution
  - No model authority or prose parsing
  - No narration generation
  - No legality resolution
  - No validation rule execution
  - No command execution or runtime action execution
  - No state mutation or event append
  - No persistence write or RNG/table/oracle execution
  - No settlement authorization, PR-5 arithmetic execution, or consequence application
  - No packet compilation execution
  - No live-play/session authority, UI/client authority, conversion, sourcebook inclusion, or canon promotion
- **tiny_vertical_slice.py**: not modified
- **scene_command_execution_skeleton.py**: not modified
- **command_kind_routing_skeleton.py**: not modified
- **validation_integration_bridge_skeleton.py**: not modified

## 2026-06-15 decision — RUNTIME-DOMAIN-RT-001A Action Legality Service Plan and Execution Boundary Review

- **Decision ID**: RUNTIME-DOMAIN-RT-001A-ACTION-LEGALITY-SERVICE-PLAN-001
- **Date**: 2026-06-15
- **PR**: RUNTIME-DOMAIN-RT-001A
- **Purpose**: Planning/review-only artifact that defines the backend-owned action legality boundary before any execution behavior is implemented. Defines legality status vocabulary, blocker class taxonomy, hidden-information containment rules, player-visible versus backend-only separation, source-local/donor-specific handling, corpus-scale command-family pressure analysis, and future implementation sequence.
- **Follows**: PR-9E (transaction preview packet bridge skeleton / authority flag hardening, merged as PR #310). Completes the post-PR-8 command-path reference seam and establishes the legality boundary as the next domain-service planning step.
- **Files added**:
  - docs/doctrine/reviews/runtime_domain_rt_001a_action_legality_service_plan.md
- **Files modified**:
  - docs/decisions/current_decisions_log.md (this entry)
  - docs/doctrine/astra_doctrine_registry_v0_1.yaml (changelog and file record)
- **Legality status vocabulary defined**: legal, illegal, blocked, deferred, quarantined, unknown, escalated
- **Blocker classes defined**: 18 classes covering actor existence/reference, actor authority/capability, access/permission, target existence/reference, target reachability/scope, scene/location boundary, command-kind routing, validation integration, resource prerequisite (without affordability), timing/cooldown/phase (without clocks), hidden-information, ambiguity/clarification, unsupported command-family, source-local/donor-specific, doctrine gap, schema gap, runtime owner handoff, policy/safety/meta-action, anti-authority
- **Hidden-information containment**: denial messages must not reveal hidden entity existence, secret passages, concealed traps, hidden social state, future events, or differential information through error specificity
- **Next allowed step**: RT-001B — action legality skeleton dataclasses/constants/validators/serializers
- **Authoritative denials**:
  - No action legality engine implementation
  - No command execution
  - No state mutation or event append
  - No persistence or replay writes
  - No RNG/table/oracle execution
  - No resource/consequence math execution
  - No affordability calculation, reservation, or settlement
  - No consequence application
  - No model calls, prompt rendering, prompt execution, or prose parsing
  - No narration generation
  - No live-play/session authority, UI/client authority
  - No conversion, sourcebook inclusion, or canon promotion

## 2026-06-16 decision — RUNTIME-DOMAIN-RT-001F Action Legality Service Interface Contract Hardening Review

- **Decision ID**: RUNTIME-DOMAIN-RT-001F-ACTION-LEGALITY-SERVICE-INTERFACE-CONTRACT-HARDENING-REVIEW-001
- **Date**: 2026-06-16
- **PR**: RUNTIME-DOMAIN-RT-001F
- **Purpose**: Hardening review over the action legality service interface contract skeleton (merged RT-001E / PR #315). Confirms skeleton-only status containment, false-only authority flags, dependency-reference-only manifests, player-visible serializer containment, import boundaries, package export intent, and no implementation authority.
- **Follows**: RT-001E (action legality service interface contract skeleton, merged as PR #315).
- **Files added**:
  - docs/doctrine/reviews/runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.md
  - tests/test_runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.py
- **Files modified**:
  - docs/decisions/current_decisions_log.md (this entry)
  - docs/doctrine/astra_doctrine_registry_v0_1.yaml (changelog and file record)
- **Confirmed invariants**: 15 invariants over RT-001E surface, including skeleton-only, deferred/unknown containment, false-only authority flags, reference-only manifests, visible serializer containment, import boundaries, package export intent, donor neutrality, and no implementation authority.
- **Risk ledger**: 15 entries including premature adjudication, inner status bypass, constructor/factory divergence, dependency manifest drift, authority flag bypass, visible serializer leakage, hidden-information leakage, package alias confusion, registry drift, guardrail drift, import-boundary erosion, donor-specific leakage, state read sequencing, model/live-play shortcut, and incremental drift.
- **Authorizes no implementation**: RT-001F is review-only and does not authorize legality evaluation, command execution, state read, state mutation, event commitment, persistence/replay, RNG/table/oracle, resource math, model/narration/live-play, UI, conversion, sourcebook inclusion, or canon promotion.
- **Next recommended step**: RT-001G — State Owner Interface Prerequisite Review (not legality evaluation implementation).

## 2026-06-15 decision — RUNTIME-DOMAIN-RT-001B Action Legality Skeleton Dataclasses, Constants, Validators, and Serializers

- **Decision ID**: RUNTIME-DOMAIN-RT-001B-ACTION-LEGALITY-SKELETON-001
- **Date**: 2026-06-15
- **PR**: RUNTIME-DOMAIN-RT-001B
- **Purpose**: Implements the RT-001A action legality vocabulary as frozen, keyword-only, reference-only dataclasses, controlled constants, validators, and deterministic serializers. Skeleton only — no legality evaluation engine.
- **Follows**: RT-001A (action legality service plan and execution boundary review, merged as PR #311).
- **Files added**:
  - src/astra_runtime/domain/action_legality_skeleton.py
  - tests/test_runtime_domain_rt_001b_action_legality_skeleton.py
- **Files modified**:
  - src/astra_runtime/domain/__init__.py (new skeleton exports)
  - docs/decisions/current_decisions_log.md (this entry)
  - docs/doctrine/astra_doctrine_registry_v0_1.yaml (changelog and file record)
- **Constants defined**: LEGALITY_STATUSES (7), BLOCKER_CLASSES (19), SAFE_PLAYER_MESSAGES (21), REFERENCE_KINDS, DEPENDENCY_OWNERS
- **Dataclasses defined**: ActionLegalityReference, ActionLegalitySubjectReference, ActionLegalityTargetReference, ActionLegalityDependencyReference, ActionLegalityBlocker, ActionLegalityBackendDetail, ActionLegalityVisibilityEnvelope, ActionLegalityRequest, ActionLegalityResult, ActionLegalityAuthorityFlags (30 false-only flags)
- **Factories defined**: make_action_legality_reference, make_action_legality_subject_reference, make_action_legality_target_reference, make_action_legality_dependency_reference, make_action_legality_blocker, make_action_legality_backend_detail, make_action_legality_visibility_envelope, make_action_legality_request, make_action_legality_result
- **Validators defined**: validate_action_legality_reference, validate_action_legality_subject_reference, validate_action_legality_target_reference, validate_action_legality_dependency_reference, validate_action_legality_blocker, validate_action_legality_backend_detail, validate_action_legality_visibility_envelope, validate_action_legality_request, validate_action_legality_result
- **Hidden-information containment enforced**: hidden_information blockers restricted to safe generic messages only
- **Authority flags**: all 30 flags false-only; to_dict() hardcodes False, does not return user-supplied values
- **Next recommended step**: RT-001C — action legality gate integration skeleton
- **Authoritative denials**:
  - No legality evaluation engine
  - No command execution
  - No state reads beyond inert references
  - No state mutation or event append
  - No event commitment
  - No persistence or replay writes
  - No RNG/table/oracle execution
  - No resource/consequence math execution
  - No affordability calculation, reservation, or settlement
  - No consequence application
  - No combat resolution
  - No ability/effect/skill resolution
  - No inventory mutation
  - No mission/clue/reward mutation
  - No social/faction mutation
  - No context packet compilation
  - No model calls, prompt rendering, prompt execution, or prose parsing
  - No narration generation
  - No live-play adapter, UI/client behavior
  - No conversion, sourcebook inclusion, or canon promotion

## 2026-06-16 decision — RUNTIME-DOMAIN-RT-001C Action Legality Gate Integration Skeleton

- **Decision ID**: RUNTIME-DOMAIN-RT-001C-ACTION-LEGALITY-GATE-INTEGRATION-SKELETON-001
- **Date**: 2026-06-16
- **PR**: RUNTIME-DOMAIN-RT-001C
- **Purpose**: Integrates the RT-001B action legality skeleton into the PR-9A through PR-9E command-path reference seam. Builds reference-only legality requests/results from already-typed PR-9A/9C/9D/9E references. Defaults to `deferred`/`unknown`, not real `legal` approval.
- **Follows**: RT-001B (action legality skeleton dataclasses/constants/validators/serializers, merged as PR #312).
- **Files added**:
  - src/astra_runtime/domain/action_legality_gate_integration_skeleton.py
  - tests/test_runtime_domain_rt_001c_action_legality_gate_integration_skeleton.py
- **Files modified**:
  - src/astra_runtime/domain/__init__.py (new RT-001C exports)
  - tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py (domain module allowlists)
  - docs/decisions/current_decisions_log.md (this entry)
  - docs/doctrine/astra_doctrine_registry_v0_1.yaml (changelog and file record)
- **Constants defined**: ACTION_LEGALITY_GATE_INTEGRATION_STAGES (8), ACTION_LEGALITY_GATE_ROUTES (13), ACTION_LEGALITY_GATE_DEFAULT_STATUSES (2), ACTION_LEGALITY_GATE_NON_AUTHORITY_NOTE
- **Dataclasses defined**: ActionLegalityGateInputRefs, ActionLegalityGateDependencyPlan, ActionLegalityGateIntegrationAuthorityFlags (32 false-only flags), ActionLegalityGateIntegrationRequest, ActionLegalityGateIntegrationResult
- **Factories defined**: create_action_legality_gate_input_refs, create_action_legality_gate_dependency_plan, create_action_legality_gate_integration_authority_flags, create_action_legality_gate_integration_request, create_action_legality_gate_integration_result
- **Builders defined**: build_action_legality_request_from_gate_integration, build_deferred_action_legality_result_from_gate_integration, build_unknown_action_legality_result_from_gate_integration, build_action_legality_gate_integration_result
- **Serializers defined**: serialize_action_legality_gate_integration_result (backend), serialize_action_legality_gate_integration_result_visible (player-visible)
- **Validators defined**: validate_action_legality_gate_input_refs, validate_action_legality_gate_dependency_plan, validate_action_legality_gate_integration_request, validate_action_legality_gate_integration_result, validate_action_legality_gate_integration_authority_flags
- **Integration surfaces**: carries typed references from PR-9A scene command execution assembly, PR-9C command-kind routing result, PR-9D validation integration bridge result, PR-9E transaction preview packet bridge, and RT-001B action legality request/result
- **Default behavior**: deferred (not legal); unknown when integration skeleton cannot classify missing owner/handoff
- **Authority flags**: all 32 flags false-only; to_dict() hardcodes False
- **Next recommended step**: RT-001D — action legality integration hardening review
- **Authoritative denials**:
  - No real legality evaluation engine
  - No command execution
  - No state reads beyond inert references
  - No state mutation or event append
  - No event commitment
  - No persistence or replay writes
  - No RNG/table/oracle execution
  - No resource/consequence math execution
  - No affordability calculation, reservation, or settlement
  - No consequence application
  - No combat resolution
  - No ability/effect/skill resolution
  - No inventory mutation
  - No mission/clue/reward mutation
  - No social/faction mutation
  - No context packet compilation
  - No model calls, prompt rendering, prompt execution, or prose parsing
  - No narration generation
  - No live-play adapter, UI/client behavior
  - No conversion, sourcebook inclusion, or canon promotion

## 2026-06-16 decision — RUNTIME-DOMAIN-RT-001D Action Legality Integration Hardening Review

- **Decision ID**: RUNTIME-DOMAIN-RT-001D-ACTION-LEGALITY-INTEGRATION-HARDENING-REVIEW-001
- **Date**: 2026-06-16
- **PR**: RUNTIME-DOMAIN-RT-001D
- **Purpose**: Hardening review over merged RT-001B (PR #312) and RT-001C (PR #313) surfaces. Confirms no-real-legal-approval gate, hidden-information containment, safe player-visible messaging, JSON-safe serialization, false-only authority flags, and reference-only dependency plans. Does not implement any runtime behavior.
- **Follows**: RT-001C (action legality gate integration skeleton, merged as PR #313).
- **Files added**:
  - docs/doctrine/reviews/runtime_domain_rt_001d_action_legality_integration_hardening_review.md
  - tests/test_runtime_domain_rt_001d_action_legality_integration_hardening_review.py
- **Files modified**:
  - docs/decisions/current_decisions_log.md (this entry)
  - docs/doctrine/astra_doctrine_registry_v0_1.yaml (changelog and file record)
- **Confirmed invariants**: 14 (reference-only vocabulary, inert bridge references, deferred/unknown defaults, no legal approval bypass, constructor/factory bypass closed, player-visible serializer leak-free, hidden-information containment intact, false-only authority flags, deterministic JSON-safe to_dict, reference-only dependency plans, guardrail expansion recognized, no donor-family law, no conversion/canon authority, no live-play/model authority)
- **Risk ledger entries**: 13 (legal approval bypass, backend detail leakage, hidden-information specificity, dependency-ref-to-call, guardrail drift, metadata serialization, authority flag bypass, constructor/factory divergence, validator-weaker-than-constructor, PR-9 seam overreach, state-before-owner, donor assumptions, live-play/model adapter misuse)
- **Authorizes no implementation behavior**
- **Next recommended step**: RT-001E — Action Legality Service Interface Contract Skeleton, unless review findings indicate a narrower remediation PR is required first
- **Authoritative denials**:
  - No legality evaluation engine
  - No command execution
  - No state reads beyond inert references
  - No state mutation or event append
  - No event commitment
  - No persistence or replay writes
  - No RNG/table/oracle execution
  - No resource/consequence math execution
  - No affordability calculation, reservation, or settlement
  - No consequence application
  - No combat resolution
  - No ability/effect/skill resolution
  - No inventory mutation
  - No mission/clue/reward mutation
  - No social/faction mutation
  - No context packet compilation
  - No model calls, prompt rendering, prompt execution, or prose parsing
  - No narration generation
  - No live-play adapter, UI/client behavior
  - No conversion, sourcebook inclusion, or canon promotion

## 2026-06-16 decision — RUNTIME-DOMAIN-RT-001E Action Legality Service Interface Contract Skeleton

- **Decision ID**: RUNTIME-DOMAIN-RT-001E-ACTION-LEGALITY-SERVICE-INTERFACE-CONTRACT-SKELETON-001
- **Date**: 2026-06-16
- **PR**: RUNTIME-DOMAIN-RT-001E
- **Purpose**: Defines the service-facing contract boundary between the action legality gate (RT-001C) and a future action legality evaluation service. Frozen, keyword-only dataclasses, controlled constants, validators, factory/builder functions, and deterministic serializers. Does not implement legality evaluation.
- **Follows**: RT-001D (action legality integration hardening review, merged as PR #314).
- **Files added**:
  - src/astra_runtime/domain/action_legality_service_interface_contract_skeleton.py
  - tests/test_runtime_domain_rt_001e_action_legality_service_interface_contract_skeleton.py
- **Files modified**:
  - src/astra_runtime/domain/__init__.py (new RT-001E exports)
  - tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py (domain module allowlists)
  - docs/decisions/current_decisions_log.md (this entry)
  - docs/doctrine/astra_doctrine_registry_v0_1.yaml (changelog and file record)
- **Constants defined**: ACTION_LEGALITY_SERVICE_INTERFACE_STAGES (5), ACTION_LEGALITY_SERVICE_INTERFACE_DEPENDENCY_KINDS (15), ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES (2: deferred, unknown), ACTION_LEGALITY_SERVICE_INTERFACE_OWNER_ROUTES (15), ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE
- **Dataclasses defined**: ActionLegalityServiceInterfaceAuthorityFlags (34 false-only fields), ActionLegalityServiceInterfaceDependencyManifest, ActionLegalityServiceInterfaceRequest, ActionLegalityServiceInterfaceResult, ActionLegalityServiceInterfaceContractSummary
- **Factories defined**: create_action_legality_service_interface_authority_flags, create_action_legality_service_interface_dependency_manifest, create_action_legality_service_interface_request, create_action_legality_service_interface_result, create_action_legality_service_interface_contract_summary
- **Builders defined**: build_action_legality_service_interface_dependency_manifest, build_deferred_action_legality_service_interface_result, build_unknown_action_legality_service_interface_result
- **Serializers defined**: serialize_action_legality_service_interface_result (backend), serialize_action_legality_service_interface_result_visible (player-visible)
- **Validators defined**: validate_action_legality_service_interface_authority_flags, validate_action_legality_service_interface_dependency_manifest, validate_action_legality_service_interface_request, validate_action_legality_service_interface_result, validate_action_legality_service_interface_contract_summary
- **Preserves non-authority boundaries**: RT-001B, RT-001C, RT-001D all unmodified
- **Default behavior**: deferred or unknown (not legal); result rejects legality_status="legal"
- **Authority flags**: all 34 flags false-only; to_dict() hardcodes False
- **Next recommended step**: RT-001F — Action Legality Service Interface Contract Hardening Review
- **Authoritative denials**:
  - No legality evaluation engine
  - No real legality evaluation
  - No command execution
  - No state reads
  - No state mutation or event append
  - No event commitment
  - No persistence or replay writes
  - No RNG/table/oracle execution
  - No resource/consequence math execution
  - No affordability calculation, reservation, or settlement
  - No consequence application
  - No combat resolution
  - No ability/effect/skill resolution
  - No inventory mutation
  - No mission/clue/reward mutation
  - No social/faction mutation
  - No context packet compilation
  - No model calls, prompt rendering, prompt execution, or prose parsing
  - No narration generation
  - No live-play adapter, UI/client behavior
  - No conversion, sourcebook inclusion, or canon promotion

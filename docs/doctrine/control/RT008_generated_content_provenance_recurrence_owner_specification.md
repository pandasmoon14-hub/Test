# RT-008 Generated-Content Provenance / Recurrence Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification only
Tracking ID: REMEDIATION-STAGE2-RT008-GENERATED-CONTENT-PROVENANCE-RECURRENCE-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-E
Remediation track: RT-008-generated-content-provenance
Owner: Astra Doctrine Council / future generated-content lifecycle, provenance, and recurrence boundary owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-008. It upgrades `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md` into a specification-level planning artifact for generated-content provenance, source-local status, recurrence eligibility, durable-record eligibility, stable identifier requirements, review requirements, generator-disablement posture, provenance handoffs, context-packet projection handoffs, downstream consumer obligations, auditability, and no-canon-promotion guardrails.

This specification remains non-executable and non-implementation. It defines planning-level ownership seams, future semantic requirements, authority boundaries, handoff obligations, validation/readiness expectations, and LLM non-authority rules only. It does not authorize generator code, generated records, final schemas, database schemas, persistent IDs, content writers, provenance databases, recurrence engines, retrieval indexes, context-packet compilers, validators, runtime code, live-play prompts, training data, donor-content audits, sourcebook inclusion authorization, pilot conversion authorization, or canon promotion.

This specification links to and relies on the following actual repo artifacts:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.
- RT008 owner scaffold: `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md`.
- RT001 owner specification: `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`.
- RT005 owner specification: `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md`.
- RT011 owner specification: `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`.

### Source availability disclosure

This Stage 2 PR-E pass used actual repo files only. All requested planning and audit sources, current RT owner files, generated-content/source-local/provenance pressure files, schema/math/readiness files, canon/governance/runtime authority files, and `README.md` were present at drafting time. No requested source path was absent. This specification preserves source pressure from `docs/doctrine/schema/C01_creature_npc_record_schema.md`, `docs/doctrine/schema/C02_item_gear_record_schema.md`, `docs/doctrine/schema/C03_ability_power_technique_record_schema.md`, `docs/doctrine/schema/C05_faction_institution_record_schema.md`, `docs/doctrine/schema/C06_location_site_region_record_schema.md`, `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`, `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md`, `docs/doctrine/schema/C09_hazard_environment_record_schema.md`, `docs/doctrine/schema/C10_table_oracle_record_schema.md`, `docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md`, `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md`, `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md`, `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md`, `docs/doctrine/astra_doctrine_roadmap_v0_1.md`, `docs/doctrine/astra_doctrine_registry_v0_1.yaml`, `docs/decisions/current_decisions_log.md`, and `README.md` without converting those sources into schemas, records, generators, validators, runtime code, sourcebook authorization, or canon promotion.

## 2. Scope

RT-008 owns planning-level governance for generated-content provenance and recurrence boundaries. Ownership means defining future semantic requirements for how generated content must remain traceable, reviewable, source-bounded, non-canonical by default, and ineligible for durable recurrence unless backend/reviewer systems later authorize it. Ownership does not mean implementing generators, records, schemas, databases, IDs, validators, recurrence engines, retrieval indexes, persistence writers, content writers, context-packet compilers, prompts, or runtime code.

RT-008 owns the following planning boundaries:

- generated-content provenance ownership boundaries;
- source-local versus generated versus persistent versus recurrent versus canon/sourcebook status separation;
- ephemeral proposal versus durable generated content separation;
- durable-record eligibility requirements;
- recurrence eligibility requirements;
- stable identifier requirement boundaries;
- generator-output review requirements;
- generator-disablement posture, including the rule that this owner specification does not enable a generator;
- generated-content provenance chain requirements;
- generated-content source/evidence/reasoning disclosure requirements;
- generated-content dependency handoff requirements;
- generated-content context-packet projection handoffs through RT-005;
- generated-content validation/readiness handoffs through RT-011;
- downstream consumer obligations for RT-004, RT-006, RT-007, RT-009, RT-010, and RT-012;
- auditability requirements for future generated proposal, review, rejection, quarantine, durable eligibility, recurrence eligibility, stable identifier, persistence handoff, sourcebook boundary, and canon-boundary decisions.

RT-008 preserves the audit waves' pressure that generated NPCs, factions, missions, items, vehicles, hazards, tables, abilities, locations, and source-local setting material need provenance and recurrence controls before later owners consume them. It also preserves the README's backend-first/model-interchangeability posture: model output may be useful proposal text, but no LLM is the holder of Astra truth.

## 3. Must-not-own boundaries

RT-008 must not own, create, imply, or claim completion of:

- generator implementation;
- procedural generation engine;
- generated NPC/faction/location/item/mission/vehicle/hazard/table/ability records;
- final generated-content schema;
- final provenance database;
- persistent ID allocator implementation;
- recurrence engine;
- content writer;
- persistence writer;
- retrieval index implementation;
- context-packet compiler implementation;
- runtime code;
- schema implementation;
- command IR implementation;
- validator implementation;
- database schema;
- RNG/dice/table implementation;
- event ledger implementation;
- live-play prompt implementation;
- training data;
- donor-content audits;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion.

RT-008 also must not decide final schemas for C01, C02, C03, C05, C06, C07, C08, C09, C10, or C14. It defines provenance/recurrence requirements that future generators, record pipelines, validators, persistence owners, sourcebook reviewers, and canon-promotion protocols must obey if separately authorized.

## 4. Authority model

The RT-008 authority model is deliberately split across owners:

- RT-001 owns command/event lifecycle and when a generated-content proposal may enter backend review or event/state workflows.
- RT-005 owns whether generated-content facts may be projected to the model/player and what visible provenance/context is allowed.
- RT-011 owns validation/readiness requirements and the future non-executable/executable readiness boundary.
- RT-009 owns random/table/oracle authority when generated content depends on randomization, table results, oracle outcomes, seeds, replay references, hidden rows, or random result domains.
- RT-002 owns generated-content cost, reward, loss, upkeep, consequence, and resource-effect math pressure when a generated proposal would affect resources or outcomes.
- RT-003 owns generated hazard, threat, combat consequence, damage, recovery, exposure, and environmental danger pressure.
- RT-004 owns ability/effect/skill binding pressure when generated content would grant capabilities, prerequisites, cooldowns, techniques, powers, or effects.
- RT-006 owns generated mission, clue, objective, branch, reward, penalty, scenario-state, and hidden-truth pressure.
- RT-007 owns generated social, faction, actor-knowledge, contact, relationship, reputation, and institution pressure.
- RT-010 owns generated inventory, item, vehicle, platform, cargo, installable, equipment, and asset-state pressure.
- RT-012 owns D-series/native-design source-pack promotion boundaries and prevents draft/source-pack material from becoming canon/sourcebook/runtime authority without separate promotion.
- Backend/reviewer systems own durable eligibility, provenance acceptance, stable ID assignment, recurrence approval, and persistence authorization once those systems are separately implemented.
- The LLM may propose text or options only inside bounded context and may not create durable truth, recurrence, sourcebook material, or canon.

## 5. Generated-content status contract

The following generated-content statuses are conceptual statuses as planning placeholders only. They are not final schemas, not database fields, not generated records, not persistence states, not runtime state, not content writer output, not sourcebook statuses by themselves, and not canon statuses by themselves.

| Conceptual status placeholder | Planning meaning | Boundary note |
|---|---|---|
| `ephemeral_generated_proposal` | Temporary generated text or options supplied for review or narration within a bounded context. | No durability, recurrence, persistence, backend truth, sourcebook authority, or canon authority. |
| `reviewer_candidate` | Generated proposal queued for human/backend review. | Review queue status does not accept provenance or authorize records. |
| `rejected_generated_proposal` | Generated proposal rejected or refused. | Must not be reused as truth, memory, recurrence, sourcebook content, or canon. |
| `quarantine_pending_provenance` | Generated material cannot proceed because provenance, evidence, source-local boundary, dependency, or validation status is incomplete. | Quarantine is not persistence and not canon/sourcebook eligibility. |
| `source_local_generated_content` | Generated material bounded to a source-local context, donor-evidence context, scene, packet, or future source scope. | Source-local reuse cannot become Astra-wide truth by repetition. |
| `durable_generated_candidate` | Generated material being considered for future durable treatment. | Requires backend-owned provenance, stable identity boundary, validation status, review, and event/state/persistence handoff before durability. |
| `recurrent_generated_candidate` | Durable candidate being considered for future recurrence. | Requires explicit recurrence eligibility; repeated narration is insufficient. |
| `persistent_generated_record_pending` | Candidate awaiting future persistence authorization. | Does not define a database row, file output, ID format, or record schema. |
| `backend_committed_generated_record` | Placeholder for future backend-committed generated record if separately implemented and approved. | This specification creates no such records and authorizes no writer. |
| `sourcebook_candidate_requires_separate_review` | Placeholder for generated material that might later be reviewed for sourcebook inclusion. | Not sourcebook content and not inclusion authorization. |
| `canon_candidate_requires_separate_review` | Placeholder for generated material that might later be reviewed under a canon protocol. | Not canon and not promotion authorization. |
| `accepted_canon_requires_canon_protocol` | Placeholder acknowledging that only a separate canon protocol could accept canon. | RT-008 cannot perform or authorize that acceptance. |

These status placeholders exist to keep source-local, generated, persistent, recurrent, sourcebook, and canon claims separate. They must not be copied into code, JSON schema, database fields, generated records, persistence states, runtime state, content writer output, sourcebook statuses, or canon statuses without separate implementation authorization.

## 6. Provenance and recurrence contract

The RT-008 provenance and recurrence contract is planning-level only:

- generated content must preserve generation source, prompt/context basis, originating command/event if any, source-local boundary if any, dependency refs, reviewer notes, and validation status before durability;
- generated content must preserve source/evidence/reasoning disclosure requirements sufficient for later reviewer/backend evaluation, without requiring the LLM to become provenance authority;
- durable generated content must have backend-owned provenance, stable identity, validation status, and event/state/persistence handoff before recurrence;
- recurrent generated content requires explicit recurrence eligibility and cannot arise from repeated narration alone;
- source-local generated content must remain bounded and cannot become Astra-wide truth by reuse;
- generated content derived from donor conversion evidence must preserve source-local/rejected/canon-candidate restrictions;
- generated content depending on random tables/oracles must route through RT-009;
- generated content visible to the LLM/player must route through RT-005;
- generated content affecting commands, events, state, rejection, quarantine, or commitment must route through RT-001;
- generated content affecting validation/readiness, file presence, registry tracking, or readiness labels must route through RT-011;
- durable generated content requires future persistence ownership and reviewer/backend validation.

This contract does not define final fields, JSON schema, database schema, ID format, generator logic, recurrence algorithm, content writer logic, validator code, persistence code, retrieval code, or runtime code.

## 7. Generated-content family coverage

RT-008 records generated-content provenance and recurrence pressure across future content families while refusing to create those records:

- abilities/techniques/effects through RT-004;
- missions/scenarios/clues/rewards through RT-006;
- social/faction/actor-knowledge/contact content through RT-007;
- RNG/table/oracle outputs through RT-009;
- inventory/items/vehicles/assets/cargo through RT-010;
- D-series/native-design material through RT-012;
- creature/NPC records through `docs/doctrine/schema/C01_creature_npc_record_schema.md`;
- item/gear records through `docs/doctrine/schema/C02_item_gear_record_schema.md`;
- ability/power/technique records through `docs/doctrine/schema/C03_ability_power_technique_record_schema.md`;
- faction/institution records through `docs/doctrine/schema/C05_faction_institution_record_schema.md`;
- location/site/region records through `docs/doctrine/schema/C06_location_site_region_record_schema.md`;
- mission/scenario/adventure records through `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`;
- vehicle/ship/platform records through `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md`;
- hazard/environment records through `docs/doctrine/schema/C09_hazard_environment_record_schema.md`;
- table/oracle records through `docs/doctrine/schema/C10_table_oracle_record_schema.md`;
- source-local setting/cosmology records through `docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md`;
- schema/math/readiness sequencing through SM00, SM01, and SM02 where generated durability would pressure validation or pilot-conversion readiness.

RT-008 does not create those records. It defines provenance/recurrence requirements that future generators and record pipelines must obey if they are separately authorized.

## 8. Future generated-content artifact inventory

The following future generated-content artifact families are semantic requirements only. They are not implemented schemas, not generated records, not durable records, not writers, not generators, not final fields, not formulas, not JSON schema, not database schema, not Pydantic models, not validator code, not generator code, not persistence code, not retrieval code, not context-packet compiler code, and not runtime code. Every listed family has implementation status `future_required_not_implemented`.

| Future artifact family | Purpose | Owner | LLM allowed interaction | Downstream handoff | Implementation status |
|---|---|---|---|---|---|
| `GeneratedProposalRequirement` | Define future requirements for labeling temporary generated text/options as proposals only. | RT-008 with RT-001 timing handoff. | May draft bounded proposal text when backend context asks for it. | RT-001 for entry timing; RT-005 for visibility. | `future_required_not_implemented` |
| `GeneratedContentProvenanceRequirement` | Require generation source, prompt/context basis, originating command/event if any, evidence, dependencies, reviewer notes, and validation status before durability. | RT-008 and future backend/reviewer provenance owner. | May summarize visible provenance inputs but may not accept provenance. | RT-011 validation; future provenance database only if separately authorized. | `future_required_not_implemented` |
| `SourceLocalGeneratedBoundaryRequirement` | Keep source-local generated material bounded to its source, scene, packet, donor-evidence, or future source scope. | RT-008 with C14/source-local governance and RT-012 where D-series material is involved. | May label text as source-local only if backend context supplies that status. | RT-005 projection; RT-012 promotion boundary; canon protocol if ever separately invoked. | `future_required_not_implemented` |
| `DurableEligibilityRequirement` | Define future prerequisites before generated content can be considered durable. | Backend/reviewer systems with RT-008 planning requirements. | May not decide durability; may list missing visible prerequisites. | RT-001 event/state handoff; RT-011 validation; future persistence owner. | `future_required_not_implemented` |
| `RecurrenceEligibilityRequirement` | Require explicit recurrence approval and prevent repeated narration from creating recurrence. | Backend/reviewer systems with RT-008 planning requirements. | May not decide recurrence; may repeat only backend-approved recurrent facts. | RT-005 context projection; future retrieval/persistence owners. | `future_required_not_implemented` |
| `StableIdentifierRequirement` | Define the future boundary that stable IDs require backend authorization. | Future backend identity/ID owner with RT-008 requirements. | May not assign persistent IDs; may quote visible IDs supplied by backend context. | Future ID allocator and persistence owner if separately authorized. | `future_required_not_implemented` |
| `GenerationDependencyRequirement` | Preserve dependencies on command/event, source evidence, randomization, resources, hazards, abilities, missions, factions, assets, or D-series material. | RT-008 coordinates with RT-001 through RT-012. | May enumerate visible dependencies but may not certify completeness. | Relevant RT owner and RT-011 validation. | `future_required_not_implemented` |
| `GeneratedContentReviewRequirement` | Require reviewer/backend review before generated content can proceed toward durability, recurrence, persistence, sourcebook review, or canon review. | Future reviewer workflow owner with RT-008 requirements. | May prepare non-authoritative review summaries. | Reviewer decision record; RT-011 readiness. | `future_required_not_implemented` |
| `GeneratedContentValidationRequirement` | Require future validation of provenance, status separation, source-local boundaries, stable ID authorization, recurrence eligibility, random routing, context projection, and canon/sourcebook boundaries. | RT-011 validation/readiness owner with RT-008 requirements. | May draft validation checklists but may not run nonexistent validators. | RT-011 and future validator implementation if separately authorized. | `future_required_not_implemented` |
| `GeneratedContentRejectionRequirement` | Preserve rejection status and prevent rejected generated proposals from becoming truth by reuse. | Backend/reviewer rejection owner with RT-008 requirements. | May state visible rejection status supplied by backend context. | RT-001 rejection/quarantine; RT-005 projection limits. | `future_required_not_implemented` |
| `GeneratedContentQuarantineRequirement` | Preserve quarantine pending provenance, evidence, dependency, source-local, or validation review. | Backend/reviewer quarantine owner with RT-008 requirements. | May identify visible quarantine labels but may not release quarantine. | RT-001 quarantine; RT-011 readiness; future reviewer decision record. | `future_required_not_implemented` |
| `GeneratedContentVisibilityRequirement` | Require generated-content visibility, redaction, hidden-fact handling, and provenance projection to route through RT-005. | RT-005 with RT-008 provenance requirements. | May narrate only backend-approved visible generated facts. | RT-005 context-packet projection and redaction owner. | `future_required_not_implemented` |
| `GeneratedContentPersistenceHandoffRequirement` | Require future persistence authorization before generated content is written as a durable backend record. | Future persistence owner with RT-001, RT-008, and RT-011 handoffs. | May not write generated content to files or databases. | Future persistence writer only if separately authorized. | `future_required_not_implemented` |
| `GeneratedContentCanonBoundaryRequirement` | Keep generated content from becoming canon without a separate canon protocol. | Canon governance owner with RT-008 guardrails. | May not promote canon; may cite visible canon status supplied by authorized source. | Canon protocol and decision log if separately authorized. | `future_required_not_implemented` |
| `GeneratedContentSourcebookBoundaryRequirement` | Keep generated content from becoming sourcebook material without separate sourcebook review. | Sourcebook/reviewer governance owner with RT-008 guardrails. | May not authorize sourcebook inclusion; may cite visible sourcebook-review status supplied by backend context. | Sourcebook review process if separately authorized. | `future_required_not_implemented` |

## 9. Validation and readiness requirements

RT-008 validation and readiness requirements are future requirements only. They coordinate with RT-011 and do not implement validators, test fixtures, CI jobs, schemas, databases, generator checks, persistence checks, recurrence algorithms, context-packet compilers, or runtime code.

Future validation/readiness coverage must include:

- source linkage validation;
- generated status separation validation;
- ephemeral-versus-durable separation validation;
- source-local boundary validation;
- provenance chain coverage validation;
- stable identifier authorization validation;
- recurrence eligibility validation;
- random dependency routing validation;
- context projection routing validation;
- canon/sourcebook boundary validation;
- LLM non-authority validation;
- non-implementation guardrail validation.

RT-011 owns validation/readiness governance for these requirements. RT-008 supplies the generated-content provenance/recurrence semantics that future RT-011 validators or reviewer checklists would need if separately authorized.

## 10. Downstream handoffs

RT-008 handoffs must remain explicit and auditable:

- RT-001: command lifecycle, event commitment, rejection/quarantine, and generated proposal entry timing.
- RT-002: generated-content costs, rewards, losses, upkeep, consequence pressure, and resource effects.
- RT-003: generated hazards, threats, combat consequences, damage/recovery pressure, and environmental dangers.
- RT-004: generated abilities, effects, techniques, skills, prerequisites, cooldowns, and capability grants.
- RT-005: generated-content visibility, redaction, context-packet projection, hidden generated facts, visible provenance, source-local labels, and narrator fact-set limits.
- RT-006: generated missions, clues, objectives, branches, rewards, penalties, scenario state, and hidden truths.
- RT-007: generated social/faction/actor-knowledge/contact/relationship/institutional content.
- RT-008: generated-content provenance, source-local status, durable eligibility, recurrence eligibility, stable identifier boundary, review boundary, and no-canon-promotion guardrails.
- RT-009: generated content that depends on RNG, tables, or oracle results.
- RT-010: generated inventory, items, vehicles, platforms, cargo, installables, equipment, and asset state.
- RT-011: validation/readiness governance.
- RT-012: D-series/native-design source-pack material that may pressure generated content but cannot become canon/sourcebook/runtime authority without promotion.

Downstream consumers must not treat RT-008 planning language as generator output, generated records, recurrence, persistence, sourcebook authorization, or canon. They must preserve provenance, status, source-local limits, validation status, rejection/quarantine status, random-result routing, context-projection routing, and backend/reviewer authority in their future owner specifications.

## 11. LLM non-authority rules

The LLM is explicitly prohibited from:

- creating durable generated records;
- deciding recurrence eligibility;
- assigning persistent IDs;
- deciding generated-content provenance as accepted;
- creating generated NPCs, factions, locations, missions, items, vehicles, hazards, tables, abilities, or source-local records as backend truth;
- treating repeated narration as recurrence;
- treating summaries as generated-content memory authority;
- treating generated prose as canon or sourcebook content;
- promoting generated content to canon;
- deciding source-local boundaries;
- bypassing reviewer/backend validation;
- writing generated content to files or databases;
- choosing random generated outputs without RT-009 authority;
- projecting hidden generated facts without RT-005 authority;
- authorizing live-play/training/sourcebook/canon use.

The LLM may draft an ephemeral generated proposal, summarize visible backend-approved generated-content status, or present visible options only when bounded context allows it. Such interaction remains advisory and may not become backend truth, persistence, recurrence, sourcebook material, or canon.

## 12. Non-implementation reaffirmation

This PR adds no:

- runtime code;
- schema implementation;
- command IR implementation;
- validator implementation;
- generator implementation;
- procedural generation engine;
- generated content records;
- durable generated records;
- stable ID allocator;
- recurrence engine;
- content writer;
- persistence writer;
- retrieval index;
- context-packet compiler;
- redaction algorithm;
- RNG/dice/table implementation;
- event ledger implementation;
- database schema;
- live-play prompt;
- training data;
- donor-content audit;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion.

This specification is Stage 2 owner-specification planning only. It cannot be used as runtime readiness, schema readiness, validator readiness, generator readiness, generated-record authorization, durable-record authorization, sourcebook authorization, pilot-conversion authorization, live-play authorization, training authorization, donor-content audit, or canon-promotion evidence.

## 13. Stage 2 output classification

```yaml
stage2_output:
  stage2_pr_id: STAGE2-PR-E
  track: RT-008
  artifact_type: owner_specification
  implementation_status: non_executable_planning
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_validator_implementation: false
  authorizes_generator_implementation: false
  authorizes_generated_records: false
  authorizes_durable_generated_records: false
  authorizes_stable_id_allocator: false
  authorizes_recurrence_engine: false
  authorizes_persistence_writer: false
  authorizes_retrieval_index: false
  authorizes_context_packet_compiler: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  authorizes_pilot_conversion: false
  next_allowed_step: RT-009 owner specification, pending review
```

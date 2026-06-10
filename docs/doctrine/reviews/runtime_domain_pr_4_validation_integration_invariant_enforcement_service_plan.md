# RUNTIME-DOMAIN-PR-4: Validation Integration and Invariant Enforcement Service Plan

## 1. Purpose and status

This document is **RUNTIME-DOMAIN-PR-4**, a planning-only service plan for the future Validation Integration and Invariant Enforcement service within the Astra Ascension runtime domain-service layer.

It follows **RUNTIME-DOMAIN-PR-3B** (Transaction Lifecycle / Event Commitment Skeleton Review, merged as PR #263), which confirmed:

- PR-3A transaction lifecycle skeleton is scope-compliant.
- PR-3A event commitment skeleton is scope-compliant.
- Validator surfaces are acceptable for later services.
- Anti-mutation and anti-append guardrails are acceptable.
- No PR-3C hardening is required.
- The next authorized step is RUNTIME-DOMAIN-PR-4 planning.

RUNTIME-DOMAIN-PR-0 states that RUNTIME-DOMAIN-PR-4 should plan validation integration / invariant enforcement, as the fourth foundation service after command lifecycle / action legality, state store / state projection, and transaction lifecycle / event commitment.

**This PR authorizes only a future narrow skeleton implementation PR (RUNTIME-DOMAIN-PR-4A) after review.**

**This PR does not implement code.**

**Plan ID:** RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001

---

## 2. Source ledger

All source artifacts reviewed for this plan:

| Artifact | ID | Role |
|---|---|---|
| RUNTIME-DOMAIN-PR-3B | RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001 | Primary gate source — authorized PR-4 planning |
| RUNTIME-DOMAIN-PR-3A | RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001 | Transaction lifecycle / event commitment skeleton implementation |
| RUNTIME-DOMAIN-PR-3 | RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001 | Transaction lifecycle / event commitment service plan |
| RUNTIME-DOMAIN-PR-2B | RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001 | State store / state projection skeleton review gate |
| RUNTIME-DOMAIN-PR-2A | RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001 | State store / state projection skeleton implementation |
| RUNTIME-DOMAIN-PR-2 | RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001 | State store / state projection service plan |
| RUNTIME-DOMAIN-PR-1B | RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001 | Command lifecycle / action legality skeleton review gate |
| RUNTIME-DOMAIN-PR-1A | RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001 | Command lifecycle / action legality skeleton implementation |
| RUNTIME-DOMAIN-PR-1 | RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001 | Command lifecycle / action legality service plan |
| RUNTIME-DOMAIN-PR-0 | RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001 | Domain service implementation sequencing plan |

### Primary gate source path

- `docs/doctrine/reviews/runtime_domain_pr_3b_transaction_lifecycle_event_commitment_skeleton_review.md`

### Planning sources consulted

| Source | Path |
|--------|------|
| PR-0 sequencing plan | `docs/doctrine/reviews/runtime_domain_pr_0_domain_service_implementation_sequencing_plan.md` |
| PR-3 service plan | `docs/doctrine/reviews/runtime_domain_pr_3_transaction_lifecycle_event_commitment_service_plan.md` |
| PR-2 service plan | `docs/doctrine/reviews/runtime_domain_pr_2_state_store_state_projection_service_plan.md` |
| PR-1 service plan | `docs/doctrine/reviews/runtime_domain_pr_1_command_lifecycle_action_legality_service_plan.md` |

### Kernel skeleton modules consulted (including the validation pipeline and invariant-precheck skeleton)

| Module | Path |
|--------|------|
| schema_registry | `src/astra_runtime/kernel/schema_registry.py` |
| record_identity | `src/astra_runtime/kernel/record_identity.py` |
| command_envelope | `src/astra_runtime/kernel/command_envelope.py` |
| transaction_preview | `src/astra_runtime/kernel/transaction_preview.py` |
| state_delta | `src/astra_runtime/kernel/state_delta.py` |
| event_ledger | `src/astra_runtime/kernel/event_ledger.py` |
| rng_interface | `src/astra_runtime/kernel/rng_interface.py` |
| table_oracle | `src/astra_runtime/kernel/table_oracle.py` |
| validation_pipeline | `src/astra_runtime/kernel/validation_pipeline.py` |
| hidden_information | `src/astra_runtime/kernel/hidden_information.py` |
| context_projection | `src/astra_runtime/kernel/context_projection.py` |
| persistence_boundary | `src/astra_runtime/kernel/persistence_boundary.py` |
| replay_audit | `src/astra_runtime/kernel/replay_audit.py` |
| runtime_trace | `src/astra_runtime/kernel/runtime_trace.py` |

### Current domain skeleton modules consulted

| Module | Path |
|--------|------|
| command_lifecycle | `src/astra_runtime/domain/command_lifecycle.py` |
| action_legality | `src/astra_runtime/domain/action_legality.py` |
| state_store | `src/astra_runtime/domain/state_store.py` |
| state_projection | `src/astra_runtime/domain/state_projection.py` |
| transaction_lifecycle | `src/astra_runtime/domain/transaction_lifecycle.py` |
| event_commitment | `src/astra_runtime/domain/event_commitment.py` |
| domain package exports | `src/astra_runtime/domain/__init__.py` |

Note: the task brief referenced `src/astra_runtime/domain/init.py`; the actual file in the repository is `src/astra_runtime/domain/__init__.py`, and that is the file consulted.

### Owner specifications consulted (RT-001 through RT-012)

| Spec ID | Path |
|---------|------|
| RT-001 | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md` |
| RT-002 | `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md` |
| RT-003 | `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md` |
| RT-004 | `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md` |
| RT-005 | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md` |
| RT-006 | `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md` |
| RT-007 | `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md` |
| RT-008 | `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md` |
| RT-009 | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md` |
| RT-010 | `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md` |
| RT-011 | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md` |
| RT-012 | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md` |

### Schema files consulted (C00 through C14)

| Schema ID | Path |
|-----------|------|
| C00 | `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` |
| C01 | `docs/doctrine/schema/C01_creature_npc_record_schema.md` |
| C02 | `docs/doctrine/schema/C02_item_gear_record_schema.md` |
| C03 | `docs/doctrine/schema/C03_ability_power_technique_record_schema.md` |
| C04 | `docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md` |
| C05 | `docs/doctrine/schema/C05_faction_institution_record_schema.md` |
| C06 | `docs/doctrine/schema/C06_location_site_region_record_schema.md` |
| C07 | `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md` |
| C08 | `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md` |
| C09 | `docs/doctrine/schema/C09_hazard_environment_record_schema.md` |
| C10 | `docs/doctrine/schema/C10_table_oracle_record_schema.md` |
| C11 | `docs/doctrine/schema/C11_companion_summon_record_schema.md` |
| C12 | `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md` |
| C13 | `docs/doctrine/schema/C13_map_diagram_record_schema.md` |
| C14 | `docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md` |

### Registry and decision-log sources consulted

| Artifact | Path |
|----------|------|
| Doctrine registry | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` |
| Decision log | `docs/decisions/current_decisions_log.md` |

---

## 3. Backend-first invariant

**Astra is not an LLM GM with tools. Astra is a backend-owned TTRPG runtime with an interchangeable narration model. The LLM is not the game engine. The backend owns truth.**

Astra Ascension must be model-interchangeable. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth. Prose is downstream of state, not its source. LLMs propose; the backend validates and commits.

### Service implication

Validation is a **backend-owned authority layer**. The Validation Integration and Invariant Enforcement service is the future backend-owned surface through which domain services declare validation requirements, route invariant checks through the kernel validation pipeline, interpret validation results, and route validation failures to blocking, rejection, quarantine, or doctrine escalation.

The following can never validate themselves and can never override backend validation:

- Narration and model output of any kind
- UI text and client-side state assertions
- Donor assumptions, donor-sourced terminology, and donor-local mechanics
- Converted source-local content
- Generated content of any provenance
- Prompt templates and context-packet contents

A validation pass is a backend fact produced by the backend validation pipeline. Nothing model-facing, player-facing, or donor-derived may produce it, simulate it, or substitute for it.

---

## 4. Service ownership

### Primary ownership

The Validation Integration and Invariant Enforcement service owns the following future concerns:

1. **Validation integration surface** — the single backend-owned surface through which domain services request validation of commands, transactions, event commitments, and proposed deltas.
2. **Invariant declaration routing** — accepting invariant-set declarations from domain services and routing them to the kernel validation pipeline as invariant prechecks.
3. **Invariant result interpretation boundary** — interpreting `ValidationResult` and `InvariantPrecheck` outcomes (passed / failed / severity) into backend validation decisions; no other layer interprets validation outcomes.
4. **Transaction/event validation handoff** — providing the validation references that transaction lifecycle requires for `ready_for_event_commitment` and that event commitment requires for commit readiness.
5. **Quarantine/rejection/escalation routing** — declaring whether a validation failure blocks, rejects, quarantines, or escalates the affected artifact.
6. **Validation dependency declaration** — declaring which command, state, transaction, event commitment, hidden-information, and provenance references a validation request must bind before it can be evaluated.
7. **Validation coverage visibility for review/audit** — declaring which invariant families were checked for a given artifact, so review and audit tooling can see validation coverage.
8. **Backend-only validation outcome authority** — guaranteeing that validation outcomes originate exclusively from the backend validation pipeline and never from model text, narration, UI text, donor assumptions, or generated content.

### Dependency ownership

The Validation Integration and Invariant Enforcement service depends on but does not own the following:

| Dependency | Owner | Relationship |
|---|---|---|
| command_lifecycle / action_legality | Domain (`command_lifecycle.py`, `action_legality.py`) | Provide candidate command references (lifecycle results, legality results). Validation integration reads these references; it does not parse, route, or judge commands. |
| state_store / state_projection | Domain (`state_store.py`, `state_projection.py`) | Provide state record references, snapshot references, and projected views. Validation integration reads state references; it does not read or write state values. |
| transaction_lifecycle / event_commitment | Domain (`transaction_lifecycle.py`, `event_commitment.py`) | Provide transaction references (requests, plans, results) and commitment references (requests, results). Validation integration gates them; it does not execute or commit them. |
| validation_pipeline | Kernel (`validation_pipeline.py`) | Provides the base validation result surface: `ValidationIssue`, `ValidationResult`, `InvariantPrecheck`, `run_validation_checks`, `run_invariant_prechecks`. Validation integration consumes these shapes; it does not redefine them. |
| hidden_information / context_projection | Kernel (`hidden_information.py`, `context_projection.py`) | Provide leak-safety constraints: visibility tiers, `is_visible_to_tiers`, projection shapes. Validation integration checks leak safety; it does not create or redact hidden-information records. |
| persistence_boundary / replay_audit / runtime_trace | Kernel (`persistence_boundary.py`, `replay_audit.py`, `runtime_trace.py`) | Provide audit and replay boundaries. Validation integration declares trace and audit references for validation decisions; it does not persist, replay, or verify hash chains. |
| Future domain services (RT-002 through RT-010) | Future RT owners | Will provide domain-specific proposed validations later. Validation integration will route their declared invariants; it will never author their domain rules. |

### Explicit non-ownership

The Validation Integration and Invariant Enforcement service must **not** own, perform, or assume ownership of any of the following:

- Command parsing or player-language interpretation
- Command execution
- Domain resolution of any kind (it routes validation; it does not compute outcomes)
- Resource math (RT-002)
- Combat math (RT-003)
- Ability/effect binding (RT-004)
- Inventory mutation (RT-010)
- Mission/social mutation (RT-006, RT-007)
- Generated-content persistence (RT-008)
- Context-packet compilation (RT-005)
- Prompt/model behavior, model routing, model evaluation
- UI/live-play behavior
- Donor conversion
- Canon promotion (RT-012)

---

## 5. Validation integration model

The following 20 validation integration stages are planned for the future Validation Integration service. These are planning-only definitions and must not be implemented in PR-4. For each stage the table defines its meaning, allowed inputs, allowed outputs, owning service, kernel dependency, forbidden behavior, and downstream handoff.

| Stage | Meaning | Allowed inputs | Allowed outputs | Owning service | Kernel dependency | Forbidden behavior | Downstream handoff |
|---|---|---|---|---|---|---|---|
| `validation_integration_requested` | A domain service has asked for validation of an artifact (command, transaction, commitment, or proposed delta). | A validation integration request from an authorized domain service with the subject reference. | ValidationIntegrationRequest at this stage. | Validation Integration Service | record_identity (subject ref format) | Must not evaluate anything yet. Must not accept requests from model/UI/live-play sources. | `validation_scope_declared` |
| `validation_scope_declared` | The request has declared what is being validated (subject type, subject ref, requesting service). | ValidationIntegrationRequest at `validation_integration_requested`. | Request with scope fields populated. | Validation Integration Service | schema_registry (subject type reference) | Must not widen scope beyond the requesting service's declared subject. | `dependency_refs_bound` |
| `dependency_refs_bound` | Required upstream dependency references (command lifecycle, action legality) are bound. | Request at `validation_scope_declared`, plus ValidationIntegrationDependency declarations. | Request with dependency refs bound. | Validation Integration Service | command_envelope (command ref shape) | Must not create or modify commands. Must not proceed with unsatisfied required dependencies. | `state_refs_bound` |
| `state_refs_bound` | State record / snapshot / projection references are bound. | Request at `dependency_refs_bound`, plus state ref IDs. | Request with state refs bound. | Validation Integration Service | record_identity (state ref format) | Must not query or mutate state. Receives references from upstream only. | `transaction_refs_bound` |
| `transaction_refs_bound` | Transaction lifecycle references (transaction_id, plan refs) are bound where the subject is a transaction. | Request at `state_refs_bound`, plus transaction refs. | Request with transaction refs bound. | Validation Integration Service | None directly; reads domain transaction_lifecycle shapes. | Must not open, advance, or terminate transactions. | `event_commitment_refs_bound` |
| `event_commitment_refs_bound` | Event commitment references (commitment_request_id) are bound where the subject is a commitment. | Request at `transaction_refs_bound`, plus commitment refs. | Request with commitment refs bound. | Validation Integration Service | None directly; reads domain event_commitment shapes. | Must not commit events. Must not append to any ledger. | `invariant_set_declared` |
| `invariant_set_declared` | The invariant families and invariant declarations applying to this subject are declared. | Request with all refs bound, plus ValidationInvariantDeclaration set. | Request with invariant set declared. | Validation Integration Service | validation_pipeline (InvariantPrecheck shape) | Must not author domain rules. Declarations reference invariant families; they do not embed formulas. | `invariant_precheck_requested` |
| `invariant_precheck_requested` | The declared invariant set has been submitted to the kernel validation pipeline for precheck. | Request at `invariant_set_declared`. | Precheck request reference. | Validation Integration Service (request coordination only) | validation_pipeline (`run_invariant_prechecks` surface) | Must not evaluate invariants itself. Must not bypass the kernel pipeline. | `invariant_precheck_passed` or `invariant_precheck_failed` |
| `invariant_precheck_passed` | The kernel pipeline reported all prechecks passed. | InvariantPrecheck results, all passed. | Request advanced with precheck pass recorded. | Validation Integration Service | validation_pipeline (read results) | Must not skip remaining stages because prechecks passed. | `domain_validation_required` or `hidden_info_safety_checked` |
| `invariant_precheck_failed` | The kernel pipeline reported one or more precheck failures. | InvariantPrecheck results with failures. | ValidationIntegrationResult routed to failure handling. | Validation Integration Service | validation_pipeline (read results) | Must not suppress, downgrade, or retry failures without a new request. | `validation_failed`, `validation_quarantined`, or `validation_escalated` |
| `domain_validation_required` | The subject requires domain-specific validation owned by a future RT owner that does not exist yet. | Request whose invariant set includes domain-owned families. | Request flagged as requiring downstream domain validation. | Validation Integration Service (flagging only) | None. | Must not perform the domain validation itself. Must not treat the flag as a pass. | `domain_validation_referenced` |
| `domain_validation_referenced` | A future domain service has supplied its proposed validation result reference. | Domain validation result reference from a future RT owner. | Request with domain validation refs recorded. | Validation Integration Service | validation_pipeline (result shape) | Must not accept domain validation from model text, narration, or UI. Must not reinterpret domain results. | `hidden_info_safety_checked` |
| `hidden_info_safety_checked` | Leak safety has been checked: no validation summary or result surface would expose hidden information. | Request plus hidden-information visibility constraints. | Request with hidden-info safety flags recorded. | Validation Integration Service | hidden_information (`is_visible_to_tiers`), context_projection (visibility shapes) | Must not expose hidden values in any output. Must not modify visibility tiers. | `provenance_checked` |
| `provenance_checked` | Generated-content and source-local provenance references on the subject have been checked for presence and shape. | Request plus provenance reference declarations. | Request with provenance check recorded. | Validation Integration Service | replay_audit (provenance record shapes), record_identity | Must not grant durability or canon status. Presence/shape check only. | `validation_passed`, `validation_failed`, `validation_quarantined`, or `validation_escalated` |
| `validation_passed` | All declared invariants passed, leak safety holds, provenance references are sound. The subject has a backend validation pass. | Request with all checks recorded as passing. | ValidationIntegrationResult with passed outcome and validation_ref_id. | Validation Integration Service | validation_pipeline (ValidationResult), runtime_trace (trace ref) | Must not mutate state, apply deltas, append events, or persist as a side effect of passing. | Transaction lifecycle / event commitment consume the validation reference. |
| `validation_failed` | One or more declared invariants failed. The subject is blocked. | Failing precheck or validation results. | ValidationIntegrationResult with failed outcome, failing issue refs. | Validation Integration Service | validation_pipeline (issues), runtime_trace | Must not silently discard failures. Must not let the subject proceed to commitment. | Failure routing (Section 10). |
| `validation_quarantined` | The subject is preserved for audit review rather than outright rejected. | Results with critical severity, ambiguous leak risk, or provenance ambiguity. | ValidationIntegrationResult with quarantined outcome. | Validation Integration Service | runtime_trace, replay_audit (quarantine audit refs) | Must not release from quarantine without explicit audit review. | Audit systems. |
| `validation_escalated` | The failure indicates a doctrine gap that no existing invariant family or owner covers. | Results indicating an uncovered doctrine problem. | ValidationIntegrationResult with escalated outcome and doctrine gap description. | Validation Integration Service | runtime_trace | Must not invent a new rule to fill the gap. Escalation is to doctrine review, not self-repair. | Doctrine review process. |
| `validation_cancelled` | The validation request was cancelled by the requesting service before completion. | Cancellation signal from the requesting service. | ValidationIntegrationResult with cancelled outcome. | Validation Integration Service | runtime_trace | Must not cancel a completed validation. Must record the cancellation reason. | Requesting service. |
| `validation_superseded` | A newer validation request for the same subject superseded this one. | Detection of a superseding request for the same subject ref. | ValidationIntegrationResult with superseded outcome and superseding request ref. | Validation Integration Service | runtime_trace | Must not supersede a completed validation pass consumed by a commitment. | Requesting service. |

---

## 6. Validation decision model

The following 16 validation decisions are planned for the future service. These are planning-only definitions and must not be implemented in PR-4. For each decision the table defines its meaning, when it applies, required dependencies, whether it blocks transaction/event commitment, whether it requires quarantine, whether it requires doctrine escalation, and trace/audit requirements.

| Decision | Meaning | When it applies | Required dependencies | Blocks transaction/event commitment | Requires quarantine | Requires doctrine escalation | Trace/audit requirements |
|---|---|---|---|---|---|---|---|
| `validation_ready` | The request is fully bound and ready for invariant evaluation. | All required refs bound, invariant set declared. | Bound dependency, state, transaction/commitment refs as applicable. | Not yet (pre-decision gate). | No | No | Trace entry with request_id and bound ref summary. |
| `validation_passed` | Backend validation pass exists for the subject. | All declared invariants passed; leak safety and provenance checks passed. | InvariantPrecheck/ValidationResult all passing. | No — it is the reference that *permits* commitment readiness. | No | No | Trace entry, validation_ref_id, invariant family coverage list. |
| `validation_failed` | One or more invariants failed. | Any failing invariant with severity error or critical. | Failing ValidationResult/InvariantPrecheck refs. | Yes | Only if severity/policy requires | No | Trace entry, failing issue codes and severities. |
| `rejected_by_missing_command_ref` | The request lacks a required command lifecycle / envelope reference. | Subject derives from a command but no valid command ref is bound. | Command envelope / lifecycle ref check. | Yes | No | No | Trace entry, subject ref, missing dependency type. |
| `rejected_by_missing_state_ref` | The request lacks required state record/snapshot/projection references. | Subject touches state but state refs are absent or malformed. | State ref format validation. | Yes | No | No | Trace entry, subject ref, missing state ref IDs. |
| `rejected_by_missing_transaction_ref` | The request lacks a required transaction lifecycle reference. | Subject is a transaction-stage artifact without a bound transaction ref. | Transaction ref check. | Yes | No | No | Trace entry, subject ref, missing transaction ref. |
| `rejected_by_missing_event_commitment_ref` | The request lacks a required event commitment reference. | Subject is a commitment-stage artifact without a bound commitment ref. | Commitment ref check. | Yes | No | No | Trace entry, subject ref, missing commitment ref. |
| `rejected_by_missing_invariant_set` | No invariant set was declared for the subject. | Request reaches evaluation with an empty or undeclared invariant set. | Invariant declaration check. | Yes | No | No | Trace entry, subject ref, requesting service. |
| `rejected_by_hidden_information_risk` | Evaluating or reporting validation would leak hidden information. | Validation summary or result surface would expose backend-hidden or restricted values. | hidden_information visibility tiers, context_projection constraints. | Yes | Yes, when risk is ambiguous | No | Trace entry, affected record IDs, visibility tiers involved; summary itself must be leak-safe. |
| `rejected_by_provenance_gap` | Generated or source-local content lacks required provenance references. | Subject references generated content without provenance, or source-local content without source-local marking. | Provenance reference presence/shape check. | Yes | Yes, for ambiguous provenance | No | Trace entry, content refs lacking provenance. |
| `rejected_by_schema_mismatch` | A referenced record does not match its declared C00–C14 schema family shape. | Subject references records whose type/shape contradicts the schema registry declaration. | schema_registry type reference, record_identity format. | Yes | No | Escalate if the mismatch indicates an under-modeled schema | Trace entry, record ref, declared vs observed type. |
| `rejected_by_authority_mismatch` | The validation request or claimed pass originates from a non-backend authority. | Model text, narration, UI text, donor assumption, or generated content is presented as validation authority. | Authority source check on the request. | Yes | No | No | Trace entry, claimed authority source, rejection reason. |
| `rejected_by_phase_boundary` | The request asks for validation at a phase the subject has not lawfully reached. | E.g. commitment validation requested for a transaction that never passed planning stages. | Stage/phase consistency check against lifecycle constants. | Yes | No | No | Trace entry, subject stage, requested phase. |
| `quarantined_for_review` | The subject is preserved for audit review. | Critical-severity issues, ambiguous leak risk, ambiguous provenance, complex supersession. | The triggering issue refs. | Yes | Yes | No | Trace entry, quarantine reason code, replay audit record. |
| `escalated_to_doctrine` | The failure exposes a doctrine gap no invariant family covers. | No existing family or RT owner covers the failing condition. | Gap description, triggering refs. | Yes | Usually paired with quarantine of the subject | Yes | Trace entry, doctrine gap description, escalation ref. |
| `unsupported_validation_scope` | The requested validation scope is not one the service supports. | Request subject type or scope is outside the declared scope vocabulary. | Scope vocabulary check. | Yes | No | No | Trace entry, requested scope, supported scope set. |

---

## 7. Invariant family model

The following 21 invariant families are planned. These are planning-only declarations and must not be implemented in PR-4. Invariant families name *what is protected*; they do not embed domain formulas. For each family the table defines what it protects, required input references, downstream dependents, failure effect, whether PR-4A may skeletonize it (as a named constant and declaration shape only — never as an executable rule), and what must remain future-only.

| Invariant family | What it protects | Input references needed | Downstream services depending on it | What failure does | PR-4A may skeletonize (constant + declaration shape only) | Must remain future-only |
|---|---|---|---|---|---|---|
| `command_authority_invariant` | Only backend-accepted commands enter validation. | Command envelope ref, lifecycle ref. | Transaction lifecycle, all domain services. | Blocks before transaction. | Yes | Command authority evaluation logic. |
| `action_legality_invariant` | Legality decisions accompany command-derived subjects. | Action legality result ref. | Transaction lifecycle. | Blocks before transaction. | Yes | Legality rule evaluation. |
| `state_reference_invariant` | All state refs exist, are well-formed, and are not stale. | State record/snapshot ref IDs. | Transaction lifecycle, event commitment. | Rejects by missing state ref. | Yes | State freshness/existence checking. |
| `state_projection_visibility_invariant` | Projections used by the subject respect visibility partitions. | Projection ref, visible/redacted ref lists. | Context-packet compiler, mission/social services. | Rejects or quarantines on leak risk. | Yes | Projection visibility evaluation. |
| `transaction_lifecycle_invariant` | Transactions traverse lawful stage order with required refs. | Transaction request/plan/result refs. | Event commitment. | Rejects by phase boundary. | Yes | Stage-order evaluation. |
| `event_commitment_invariant` | Commitments occur only from commit-ready, validated transactions. | Commitment request/result refs, validation refs. | Persistence, replay, all event consumers. | Blocks event commitment. | Yes | Commitment readiness evaluation. |
| `state_delta_shape_invariant` | Proposed deltas are shape-valid and scope-consistent. | Delta ref IDs, change types, affected record IDs. | State application (future), event commitment. | Rejects by schema mismatch. | Yes | Delta content/scope evaluation. |
| `event_ledger_shape_invariant` | Event entries are shape-valid before any future append. | Event ledger entry shape refs. | Persistence, replay. | Blocks event commitment. | Yes | Ledger ordering/sequence evaluation; any append. |
| `validation_result_authority_invariant` | Validation results originate only from the backend pipeline. | Validation result refs and their source. | Everything downstream of validation. | Rejects by authority mismatch. | Yes | Source-of-authority verification logic. |
| `hidden_information_partition_invariant` | Backend-hidden information never crosses partitions. | Hidden info record refs, visibility tiers. | Context-packet compiler, mission/social/horror content. | Rejects by hidden information risk; quarantines ambiguity. | Yes | Partition evaluation logic. |
| `context_projection_visibility_invariant` | Model/player-facing projections contain only allowed tiers. | Projection refs, allowed tier sets. | Context-packet compiler, model harness. | Rejects or quarantines. | Yes | Projection content evaluation. |
| `persistence_boundary_invariant` | No durable write occurs outside the persistence boundary. | Persistence boundary request/result refs. | Persistence (future). | Blocks; escalates if a bypass is detected. | Yes | Persistence prepare/verify logic. |
| `replay_audit_invariant` | Committed facts carry replay/hash audit references. | Replay audit / hash audit record refs. | Replay engine (future). | Blocks event commitment. | Yes | Hash verification, replay execution. |
| `runtime_trace_invariant` | Every validation decision carries a trace reference. | Trace ref IDs. | Audit/review tooling. | Fails validation (untraceable decisions are invalid). | Yes | Trace store management. |
| `schema_record_shape_invariant` | Records conform to their C00–C14 schema family declarations. | Schema registry type refs, record refs. | All content-consuming services. | Rejects by schema mismatch; escalates under-modeled schemas. | Yes | Schema content validation logic. |
| `source_local_authority_invariant` | Source-local converted content never acts as canon or global law. | Source-local marking refs, content provenance. | RT-012 promotion boundary, conversion pipeline. | Rejects source-local authority claims. | Yes | Promotion boundary enforcement (RT-012). |
| `generated_content_provenance_invariant` | Generated content has provenance before durability or authority. | Generated content refs, provenance record refs. | RT-008 provenance service, persistence. | Rejects by provenance gap; quarantines ambiguity. | Yes | Provenance tracking/recurrence logic (RT-008). |
| `canon_boundary_invariant` | Nothing is promoted to canon through runtime validation. | Canon status refs, promotion markers. | RT-012, doctrine council. | Rejects; escalates attempted promotion. | Yes | Canon promotion machinery. |
| `conversion_boundary_invariant` | Conversion-stage material does not enter runtime as law. | Conversion provenance refs. | Conversion pipeline, RT-012. | Rejects; escalates. | Yes | Conversion gating machinery. |
| `model_non_authority_invariant` | Model output never acts as state, validation, or rule authority. | Request authority source declarations. | Model evaluation harness, live-play adapter. | Rejects by authority mismatch. | Yes | Model output inspection logic. |
| `live_play_non_authority_invariant` | Live-play/UI input never bypasses the command pipeline. | Request authority source declarations. | Live-play adapter (future). | Rejects by authority mismatch. | Yes | Live-play adapter enforcement. |

In every row above, "skeletonize" means: PR-4A may include the family name in a `VALIDATION_INVARIANT_FAMILIES` frozenset and allow `ValidationInvariantDeclaration` objects to reference it. PR-4A must not implement any evaluation logic for any family.

---

## 8. Kernel interface consumption plan

The following matrix defines how each of the 14 kernel skeleton modules is consumed by the future Validation Integration and Invariant Enforcement service.

| Kernel module | Position | Allowed future use | Forbidden use | Risk if used too early | Expected future tests |
|---|---|---|---|---|---|
| validation_pipeline | required (primary dependency) | Consume `ValidationIssue`, `ValidationResult`, `InvariantPrecheck`; route declared invariant sets through `run_validation_checks` / `run_invariant_prechecks`; interpret passed/severity. | Must not redefine result shapes. Must not author domain rules inside checks. Must not bypass or override pipeline outcomes. | Reimplementing the pipeline in the domain layer would fork validation authority. | Result interpretation tests; severity gating tests; no-override tests. |
| schema_registry | required | Reference schema IDs/types to check that subject records declare known schema families (C00–C14 alignment). | Must not register or mutate schemas. Must not become a runtime type system. | Schema coupling before schema stability locks validation to draft shapes. | Unknown-schema rejection tests. |
| record_identity | required | Validate record ID format on every bound reference. | Must not create IDs or change the ID format. | Minimal; record_identity is stable. | Malformed-ID rejection tests. |
| command_envelope | required | Read command envelope refs (command_id, command_type, source_actor_id) for command source validation. | Must not create, modify, or execute commands. | Minimal; reference reads only. | Invalid envelope ref rejection tests. |
| transaction_preview | required | Read preview refs (preview_id, status) for command source validation context. | Must not create previews or change preview status. | Circular dependency if previews require validation input; keep unidirectional. | Missing/rejected preview reference tests. |
| state_delta | required (shape/reference checks only) | Read delta refs, change types, affected record IDs for shape and scope checks. | **Must not apply deltas.** Must not create or modify delta payloads. No mutation. | Delta application here would collapse validation into state mutation. | Delta shape check tests; no-application tests. |
| event_ledger | required (shape/reference checks only) | Read event entry shapes and refs for commit-readiness shape checks. | **Must not append to any ledger.** Must not assign sequence numbers. | Append here would create committed facts without the commitment protocol. | Event shape check tests; no-append tests. |
| hidden_information | required (leak-safety checks) | Read visibility tiers; use `is_visible_to_tiers` to verify validation summaries and result surfaces are leak-safe. | Must not create/modify hidden-information records or tiers. Must not redact (context_projection owns redaction). | Incorrect checks could leak hidden values through validation summaries. | Leak-safe summary tests; tier check tests. |
| context_projection | required (leak-safety checks) | Read projection shapes and allowed tier sets to cross-check that validation outputs stay within allowed visibility. | Must not compile context packets or create projections. | Over-coupling to projection timing; keep as constraint reads. | Projection visibility cross-check tests. |
| persistence_boundary | required (audit posture only) | Read persistence boundary request/result refs to verify persistence posture on subjects. | **Must not perform persistence** or invoke prepare operations as side effects. | Premature persistence would bypass the commitment gate. | No-persistence tests; boundary ref posture tests. |
| replay_audit | required (audit posture only) | Reference replay/hash audit record shapes so validation decisions are replay-auditable; reference `canonical_payload_hash` posture. | **Must not run replay** or enforce hash chains. | Replay execution requires an event store that does not exist. | Audit reference presence tests; no-replay tests. |
| runtime_trace | required (audit posture only) | Declare trace entry references for every validation decision. | Must not manage a trace store or telemetry backend. | None significant; trace refs without a store is correct skeleton posture. | Trace ref presence tests for every decision. |
| rng_interface | later / optional (provenance validation only) | Later: verify that RNG result references carried by subjects are well-formed for replay determinism. | Must not invoke RNG. Validation decisions must be deterministic. | RNG use would make validation non-deterministic and break replay audit. | No-RNG-import tests now; RNG provenance ref tests later. |
| table_oracle | later / optional (provenance validation only) | Later: verify table/oracle result references carried by subjects are well-formed. | Must not invoke table/oracle lookups. | Oracle invocation would smuggle domain resolution into validation. | No-oracle-invocation tests now; oracle provenance ref tests later. |

---

## 9. Domain service handoff boundaries

For each related service: what validation integration may accept, what it may emit, what it must not decide, and what remains blocked until the downstream owner exists.

### 9.1 command_lifecycle (existing domain skeleton)

- **May accept:** CommandLifecycleResult references at terminal accepted stages, as candidate command references for validation requests.
- **May emit:** Validation outcomes affecting the command (e.g. `block_command_before_transaction`) for lifecycle feedback.
- **Must not decide:** Lifecycle stage progression, command acceptance, or rejection at the lifecycle level.
- **Blocked until downstream owner exists:** Live command-pipeline integration (no executable lifecycle exists).

### 9.2 action_legality (existing domain skeleton)

- **May accept:** ActionLegalityResult references (decision, block reasons) as legality evidence bound to validation requests.
- **May emit:** Validation failures caused by missing or inconsistent legality references.
- **Must not decide:** Whether an action is legal, blocked, or requires confirmation.
- **Blocked until downstream owner exists:** Legality re-validation on state change (requires executable legality service).

### 9.3 state_store (existing domain skeleton)

- **May accept:** StateRecordRef / StateSnapshotRef / visibility descriptor references for state reference invariants.
- **May emit:** `rejected_by_missing_state_ref` outcomes and state-reference coverage declarations.
- **Must not decide:** Whether a record exists or what any state value is.
- **Blocked until downstream owner exists:** State freshness validation (requires a state query service).

### 9.4 state_projection (existing domain skeleton)

- **May accept:** StateProjectionResult references (projection_id, visible/redacted ref lists).
- **May emit:** Projection-visibility invariant outcomes.
- **Must not decide:** Projection type, contents, or redaction choices.
- **Blocked until downstream owner exists:** Projection re-materialization checks.

### 9.5 transaction_lifecycle (existing domain skeleton)

- **May accept:** TransactionRequest/Plan/Result references; requests to validate transactions for commitment readiness.
- **May emit:** The `validation_ref_id` that transaction plans require for `ready_for_event_commitment`; blocking/quarantine outcomes.
- **Must not decide:** Transaction stage transitions, acceptance for commitment, cancellation, or supersession.
- **Blocked until downstream owner exists:** Live transaction-stage validation loops (no executable transaction engine exists).

### 9.6 event_commitment (existing domain skeleton)

- **May accept:** EventCommitmentRequest/Result references; requests to validate commitment readiness.
- **May emit:** Validation references that commitment requests require; `block_event_commitment` and quarantine outcomes.
- **Must not decide:** The commitment decision itself; whether a committed event becomes authoritative.
- **Blocked until downstream owner exists:** Actual commitment gating (no executable commitment engine exists; `allow_event_ledger_append` remains False).

### 9.7 Future resource / consequence math (RT-002)

- **May accept:** Declared resource validation requirements and proposed validation references from the future RT-002 service.
- **May emit:** `request_downstream_domain_validation` routing; validation outcomes on resource-bearing subjects.
- **Must not decide:** Any resource math, cost, or consequence outcome.
- **Blocked:** All resource validation evaluation until the RT-002 service exists.

### 9.8 Future combat / hazard / damage / recovery (RT-003)

- **May accept:** Declared combat validation requirements and proposed validation references.
- **May emit:** Routing and outcomes on combat-bearing subjects.
- **Must not decide:** Damage, hazard, or recovery outcomes.
- **Blocked:** All combat validation evaluation until the RT-003 service exists.

### 9.9 Future ability / effect / skill binding (RT-004)

- **May accept:** Declared ability/effect validation requirements and proposed validation references.
- **May emit:** Routing and outcomes on ability-bearing subjects.
- **Must not decide:** Effect resolution, skill checks, prerequisites, cooldowns.
- **Blocked:** All ability validation evaluation until the RT-004 service exists.

### 9.10 Future inventory / item / vehicle / asset (RT-010)

- **May accept:** Declared inventory validation requirements and proposed validation references.
- **May emit:** Routing and outcomes on inventory-bearing subjects.
- **Must not decide:** Item custody, durability, cargo, loadout outcomes.
- **Blocked:** All inventory validation evaluation until the RT-010 service exists.

### 9.11 Future mission / reward / clue routing (RT-006)

- **May accept:** Declared mission validation requirements and proposed validation references.
- **May emit:** Routing and outcomes, including hidden-info-safe clue visibility constraints.
- **Must not decide:** Objective state, reward routing, clue reveals.
- **Blocked:** All mission validation evaluation until the RT-006 service exists.

### 9.12 Future social / faction / actor knowledge (RT-007)

- **May accept:** Declared social validation requirements and proposed validation references.
- **May emit:** Routing and outcomes, including actor-knowledge leak-safety constraints.
- **Must not decide:** Reputation, standing, or actor-knowledge outcomes.
- **Blocked:** All social validation evaluation until the RT-007 service exists.

### 9.13 Future generated-content provenance (RT-008)

- **May accept:** Provenance record references and provenance validation requirements.
- **May emit:** `rejected_by_provenance_gap`, `quarantine_generated_content` outcomes; provenance coverage declarations.
- **Must not decide:** Provenance policy, recurrence eligibility, stable ID assignment.
- **Blocked:** Provenance content validation until the RT-008 service exists; presence/shape checks only.

### 9.14 Future context-packet compiler (RT-005)

- **May accept:** Visibility constraint declarations for leak-safety checks on validation outputs.
- **May emit:** Leak-safe validation summaries that the future compiler may include in packets.
- **Must not decide:** Packet contents, visibility filtering, or budget enforcement.
- **Blocked:** All packet-facing integration until the compiler exists (and the compiler itself is blocked until RUNTIME-DOMAIN-PR-12).

### 9.15 Future model evaluation harness (RT-011 scope)

- **May accept:** Requests to expose validation coverage visibility for evaluation purposes.
- **May emit:** Leak-safe validation coverage summaries.
- **Must not decide:** Model behavior assessments; and it must never accept model output as validation input.
- **Blocked:** All harness integration until the harness exists (RUNTIME-DOMAIN-PR-13).

### 9.16 Future live-play adapter

- **May accept:** Nothing directly. Live-play input must reach validation only through the command pipeline.
- **May emit:** Player-visible, leak-safe rejection summaries routed back through command lifecycle.
- **Must not decide:** Session behavior, input routing, output delivery.
- **Blocked:** Everything until the live-play adapter gate (RUNTIME-DOMAIN-PR-14) and all upstream services exist.

---

## 10. Validation failure routing

The following 12 failure outcomes are planned. These are planning-only definitions and must not be implemented in PR-4.

| Failure route | Trigger | Owner | Affected artifacts | Allowed output | Forbidden output | Trace/audit requirement |
|---|---|---|---|---|---|---|
| `block_command_before_transaction` | Command-stage validation failure (authority, legality reference, scope). | Validation Integration Service, feedback to command lifecycle. | Command lifecycle result; no transaction is opened. | Leak-safe rejection summary to command lifecycle. | State mutation; transaction opening; hidden values in summary. | Trace entry with command ref and failing families. |
| `block_transaction_before_commitment` | Transaction-stage validation failure before commitment readiness. | Validation Integration Service, feedback to transaction lifecycle. | Transaction plan/result; no commitment request proceeds. | Failed validation reference for the transaction result. | Event commitment; delta application; pass simulation. | Trace entry with transaction ref and failing invariants. |
| `block_event_commitment` | Commitment-stage validation failure. | Validation Integration Service, feedback to event commitment. | Event commitment request; no committed event is produced. | Failed validation reference for the commitment result. | Event ledger append; persistence; pass simulation. | Trace entry with commitment ref; replay audit reference. |
| `quarantine_transaction` | Critical severity, ambiguous leak risk, or ambiguous provenance on a transaction. | Validation Integration Service declares; transaction lifecycle records. | Transaction preserved as quarantined. | Quarantine record with reason codes. | Release without audit review; commitment from quarantine. | Trace entry; replay audit quarantine record. |
| `quarantine_event_commitment` | Critical severity or ambiguity at the commitment boundary. | Validation Integration Service declares; event commitment records. | Commitment request preserved as quarantined. | Quarantine record with reason codes. | Commitment from quarantine; ledger append. | Trace entry; replay audit quarantine record. |
| `quarantine_generated_content` | Generated content with ambiguous or partial provenance. | Validation Integration Service declares; future RT-008 owns review. | Generated content refs preserved as quarantined. | Quarantine record referencing content and provenance gaps. | Durability; authority; recurrence eligibility. | Trace entry; provenance gap details. |
| `escalate_doctrine_gap` | A failing condition no invariant family or RT owner covers. | Validation Integration Service escalates; doctrine council resolves. | The subject plus a doctrine gap description. | Escalation record for doctrine review. | Inventing a new rule inline; silently passing the subject. | Trace entry; doctrine gap description; escalation reference. |
| `reject_source_local_authority` | Source-local converted content presented as canon or global law. | Validation Integration Service; RT-012 owns the boundary. | The claiming subject. | Rejection with source-local boundary citation. | Canon promotion; treating the claim as valid pending review. | Trace entry; content refs; claimed vs actual authority. |
| `reject_hidden_info_leak` | Validation output would expose hidden values to an unauthorized tier. | Validation Integration Service. | The validation summary/result surface. | Leak-safe rejection (summary redacted to safe tier). | Any output containing the hidden values; tier modification. | Trace entry; affected record IDs and tiers (backend-visible only). |
| `reject_schema_mismatch` | Referenced records contradict their declared schema family shape. | Validation Integration Service. | The subject and the mismatched record refs. | Rejection with declared vs observed type. | Coercing the record to fit; mutating the schema registry. | Trace entry; record ref; schema family ref. |
| `reject_phase_boundary_violation` | Validation requested at an unlawful phase for the subject. | Validation Integration Service. | The out-of-phase request. | Rejection with phase boundary citation. | Retroactive pass; reordering the subject's lifecycle. | Trace entry; subject stage; requested phase. |
| `request_downstream_domain_validation` | The subject requires domain validation owned by a future RT owner. | Validation Integration Service routes; future RT owner evaluates. | The subject, flagged as pending domain validation. | Routing record naming the required RT owner. | Performing the domain validation itself; treating routing as a pass. | Trace entry; required RT owner; declared requirement refs. |

---

## 11. Hidden-information and provenance safety

The future validation integration service must handle the following information classes:

| Information class | Validation handling |
|---|---|
| Backend-hidden information | May be referenced internally for invariant evaluation. Must never appear in any player/model-facing validation summary. |
| GM-visible information | May appear only in GM-tier validation surfaces; never in player/model tiers. |
| Actor-visible information | May appear only in surfaces projected for that actor's tier. |
| Player-visible information | The only class permitted in player-facing rejection/validation summaries. |
| Model-facing projections | Validation summaries included in model-facing surfaces must pass the same tier checks as context projections; no hidden values, no backend-only refs. |
| UI/client projections | Same constraint as model-facing; UI text additionally has no validation authority. |
| Generated content | Must carry provenance references before validation can pass it toward durability. **Generated content must not become durable or authoritative without provenance validation.** |
| Source-local converted content | Validation may pass it for source-local runtime use only. **Source-local converted content must not become canon by passing runtime validation.** |
| Canon sourcebook content | Canon references are inputs to validation, never outputs; validation cannot create, expand, or promote canon. |
| Donor assumptions | Never validation inputs with authority. Donor-system expectations do not define invariants and cannot satisfy them. |

**Validation may reference hidden information internally but must not expose hidden values in player/model-facing validation summaries.** The `EventCommitmentRejection` skeleton already enforces the pattern (`player_visible=True` requires `hidden_info_safe=True`); the future validation integration service must apply the same rule to every result surface it produces.

---

## 12. Future implementation architecture

The following future implementation shape is planned. These are proposed file paths and public API symbols only. **They are proposed future symbols only and must not be created in PR-4.** They would be implemented in a future RUNTIME-DOMAIN-PR-4A skeleton implementation PR after this plan is reviewed and approved.

### Proposed future module

- `src/astra_runtime/domain/validation_integration.py` — validation integration and invariant enforcement skeleton: stage/decision/family/route constants, immutable dataclass surfaces, factory helpers, validator helpers, stateless service wrapper.

### Proposed future public API (planning only)

Constants:

- `VALIDATION_INTEGRATION_STAGES` — frozenset of the 20 stage strings in Section 5
- `VALIDATION_INTEGRATION_DECISIONS` — frozenset of the 16 decision strings in Section 6
- `VALIDATION_INVARIANT_FAMILIES` — frozenset of the 21 family strings in Section 7
- `VALIDATION_FAILURE_ROUTES` — frozenset of the 12 route strings in Section 10

Errors:

- `ValidationIntegrationError`
- `InvalidValidationIntegrationDependencyError`
- `InvalidValidationInvariantDeclarationError`
- `InvalidValidationIntegrationRequestError`
- `InvalidValidationIntegrationResultError`
- `InvalidValidationFailureRouteError`

Frozen dataclasses:

- `ValidationIntegrationDependency`
- `ValidationInvariantDeclaration`
- `ValidationIntegrationRequest`
- `ValidationIntegrationResult`
- `ValidationFailureRoute`

Service:

- `ValidationIntegrationService` — stateless wrapper delegating to module-level functions.

Factories:

- `create_validation_integration_dependency(...)`
- `create_validation_invariant_declaration(...)`
- `create_validation_integration_request(...)`
- `create_validation_integration_result(...)`
- `create_validation_failure_route(...)`

Validators:

- `validate_validation_integration_dependency(...)`
- `validate_validation_invariant_declaration(...)`
- `validate_validation_integration_request(...)`
- `validate_validation_integration_result(...)`
- `validate_validation_failure_route(...)`

The skeleton must follow the established domain posture: frozen dataclasses, `MappingProxyType` metadata with deep-copy, tuple normalization with bare-string rejection, `to_dict()` deep-copy, factory/validator parity, stateless service with empty `__dict__`, and no forbidden method names (`execute`, `run`, `mutate`, `apply`, `apply_delta`, `commit`, `append`, `persist`, `save`, `load`, `replay`, `rollback`, `resolve`, `roll`, `narrate`, `prompt`, `model`, `enforce`).

---

## 13. Future data shapes

Planning-only data-shape requirements. None of these shapes may be created in PR-4.

### 13.1 ValidationIntegrationDependency

- **Required fields:** `dependency_id`, `dependency_type` (typed against a dependency vocabulary covering command envelope, command lifecycle, action legality, state record/snapshot/projection, transaction, event commitment, state delta, event ledger, validation result, hidden information, context projection, provenance, runtime trace, persistence boundary, replay audit refs), `reference_id`, `required`, `satisfied`, `hidden_info_safe`, `metadata`.
- **Relations:** mirrors the dependency posture of `TransactionDependency` / `EventCommitmentDependency`; binds the validation request to command envelope refs, command lifecycle / action legality refs, state refs, transaction refs, event commitment refs, delta refs, ledger refs, hidden-information/context-projection constraints, provenance refs, trace refs, and persistence/replay audit refs by ID only.
- **Hidden-info safety:** carries `hidden_info_safe`; reference IDs must not embed hidden values.
- **Authoritative:** No. **May mutate state:** No. **May commit events:** No.

### 13.2 ValidationInvariantDeclaration

- **Required fields:** `declaration_id`, `invariant_family` (typed against `VALIDATION_INVARIANT_FAMILIES`), `subject_ref_id`, `required` (blocking vs advisory), `declared_by_service`, `hidden_info_safe`, `metadata`.
- **Relations:** references the kernel `InvariantPrecheck` shape for routing; names a family, never embeds rule logic; binds to command/state/transaction/commitment subjects by ref.
- **Hidden-info safety:** declarations must be expressible without hidden values.
- **Authoritative:** No (a declaration is a requirement, not a result). **May mutate state:** No. **May commit events:** No.

### 13.3 ValidationIntegrationRequest

- **Required fields:** `validation_request_id`, `subject_type`, `subject_ref_id`, `requesting_service`, `requested_stage` (typed against `VALIDATION_INTEGRATION_STAGES`), `dependencies` (tuple of ValidationIntegrationDependency), `invariant_declarations` (tuple of ValidationInvariantDeclaration), optional `command_envelope_ref_id`, optional `transaction_ref_id`, optional `event_commitment_ref_id`, optional `trace_id`, `metadata`.
- **Relations:** binds the full reference graph — command envelope, command lifecycle / action legality results, state record/snapshot/projection refs, transaction lifecycle refs, event commitment refs, state delta refs, event ledger refs — by ID only; carries hidden-information/context-projection constraints via dependencies; carries provenance refs for generated/source-local content; declares a trace ref for audit; persistence/replay refs are posture references only.
- **Hidden-info safety:** the request and its `to_dict()` form must be leak-safe.
- **Authoritative:** No. **May mutate state:** No. **May commit events:** No.

### 13.4 ValidationIntegrationResult

- **Required fields:** `validation_request_id`, `decision` (typed against `VALIDATION_INTEGRATION_DECISIONS`), `final_stage`, `passed` (bool), `validation_ref_id` (present iff passed), `failure_route_ids` (tuple, present iff not passed), `invariant_families_checked` (tuple), `hidden_info_safe`, `quarantined`, `escalated`, optional `trace_id`, `metadata`.
- **Skeleton enforcement planned for PR-4A:** `passed=True` requires decision `validation_passed` and a non-None `validation_ref_id`; `passed=True` is incompatible with `quarantined` or `escalated`; `state_mutation_performed`, `event_ledger_appended`, and `persistence_written` style flags, if modeled, must be hardcoded False.
- **Relations:** consumed by transaction lifecycle (`validation_ref_id` for readiness) and event commitment (commit-readiness gating); references kernel ValidationResult/InvariantPrecheck outcomes; carries trace ref; replay-auditable by reference.
- **Hidden-info safety:** the result and any player/model-facing summary must be leak-safe.
- **Authoritative:** Yes, for the validation outcome only — it is the backend validation authority surface. It is not authoritative over state, events, or persistence. **May mutate state:** No. **May commit events:** No.

### 13.5 ValidationFailureRoute

- **Required fields:** `route_id`, `route_type` (typed against `VALIDATION_FAILURE_ROUTES`), `validation_request_id`, `subject_ref_id`, `reason`, `blocking`, `requires_quarantine`, `requires_doctrine_escalation`, `hidden_info_safe`, `player_visible`, optional `trace_id`, `metadata`.
- **Skeleton enforcement planned for PR-4A:** `player_visible=True` requires `hidden_info_safe=True` (same rule as `EventCommitmentRejection`).
- **Relations:** consumed by command lifecycle, transaction lifecycle, event commitment, and future RT owners for feedback; references the failing subject by ID; carries trace ref; quarantine routes reference replay audit records.
- **Hidden-info safety:** enforced by the player-visible/hidden-info-safe rule.
- **Authoritative:** No (it describes routing, not truth). **May mutate state:** No. **May commit events:** No.

---

## 14. Commit-readiness validation invariants

The following invariants govern how validation interacts with commitment, planning only:

1. **No event commitment without validation reference.** Every event commitment request must carry a backend validation reference.
2. **No transaction commitment readiness without validation reference.** `ready_for_event_commitment` requires a non-None validation reference (already enforced in shape by the PR-3A skeleton).
3. **No validation pass from model text.**
4. **No validation pass from narration.**
5. **No validation pass from UI text.**
6. **No validation pass from donor assumptions.**
7. **No validation pass from source-local content alone.** Source-local material may be validated *for source-local use*; its presence never constitutes a pass.
8. **No validation pass from generated content without provenance.**
9. **No state mutation from validation result.** A validation result is a reference, never a state change.
10. **No event append from validation result.**
11. **No persistence write from validation result.**
12. **No replay from validation result.**
13. **Hidden information must not leak through validation summaries.**
14. **Validation failures must be traceable.** Every failure carries a trace reference and reason.
15. **Validation must be deterministic and replay-auditable.** Identical inputs produce identical validation outcomes; no RNG, no wall-clock dependence in outcomes.

---

## 15. Corpus-scale validation pressure review

Astra must absorb 200–400 donor sources. The validation layer must therefore coordinate validation pressure from every donor-derived play pattern without becoming the rule engine for any of them.

| Pressure type | Invariant families involved | Validation integration coordinates? | Downstream domain owner required | What remains blocked | Future tests required |
|---|---|---|---|---|---|
| Basic player actions | command_authority, action_legality, state_reference | Yes | RT-001 | Command execution | Action validation routing tests |
| Multi-action turns | command_authority, transaction_lifecycle | Yes | RT-001 | Turn sequencing | Multi-subject validation tests |
| Interrupts/reactions | command_authority, transaction_lifecycle, event_commitment | Yes | RT-001 | Interrupt resolution | Interrupt-phase boundary tests |
| Combat attacks/defenses | state_delta_shape, transaction_lifecycle, schema_record_shape | Yes (routing only) | RT-003 | Combat math | Combat validation routing tests |
| Injuries/damage/recovery | state_delta_shape, state_reference | Yes (routing only) | RT-003 | Damage/recovery math | Injury delta shape tests |
| Resources/costs/backlash | state_delta_shape, state_reference | Yes (routing only) | RT-002 | Resource math | Resource validation routing tests |
| Abilities/effects/durations | schema_record_shape, state_delta_shape | Yes (routing only) | RT-004 | Effect resolution | Ability validation routing tests |
| Skills/proficiencies/training | schema_record_shape, action_legality | Yes (routing only) | RT-004 | Skill checks | Skill validation routing tests |
| Inventory/equipment/loadouts | schema_record_shape, state_reference, state_delta_shape | Yes (routing only) | RT-010 | Inventory mutation | Inventory validation routing tests |
| Vehicles/ships/mechs/platforms | schema_record_shape (C08), state_delta_shape | Yes (routing only) | RT-010 | Vehicle state | Vehicle schema validation tests |
| Faction/social reputation | hidden_information_partition, state_delta_shape | Yes (routing only) | RT-007 | Social mutation | Social leak-safety tests |
| Missions/clues/rewards | hidden_information_partition, context_projection_visibility | Yes (routing only) | RT-006 | Mission mutation, clue reveals | Clue visibility validation tests |
| Companions/summons | schema_record_shape (C11), state_reference | Yes (routing only) | RT-010 | Companion lifecycle | Companion schema validation tests |
| Crafting/salvage/requisition | schema_record_shape (C12), state_delta_shape | Yes (routing only) | RT-010 | Crafting outcomes | Recipe schema validation tests |
| Hazards/environment/weather | schema_record_shape (C09), state_delta_shape | Yes (routing only) | RT-003 | Hazard resolution | Hazard schema validation tests |
| Downtime/domain turns | transaction_lifecycle, multiple families | Yes (routing only) | Multiple RT owners | Downtime resolution | Multi-owner routing tests |
| Generated content durability | generated_content_provenance, canon_boundary | Yes | RT-008 | Generated-content persistence | Provenance gap rejection tests |
| Horror/investigation hidden information | hidden_information_partition, context_projection_visibility | Yes | RT-005 | Hidden info engine | Leak-safe validation summary tests |
| Table/oracle outcomes | replay_audit, schema_record_shape (C10) | Yes (provenance refs only) | RT-009 | Oracle invocation | Oracle provenance ref tests |
| Source-local constructs | source_local_authority, conversion_boundary, canon_boundary | Yes | RT-012 | Promotion boundary enforcement | Source-local authority rejection tests |
| Cross-book converted content | conversion_boundary, schema_record_shape, generated_content_provenance | Yes | RT-012, RT-008 | Conversion gating | Cross-book provenance validation tests |
| Canon/sourcebook references | canon_boundary, schema_record_shape | Yes | RT-012 | Canon promotion machinery | Canon non-promotion validation tests |

**Pressure finding:** every reviewed pressure type maps onto declared invariant families, with validation integration coordinating routing and the corresponding RT owner performing future domain evaluation. No pressure type requires validation integration to own domain rules, which confirms the routing-not-rule-engine posture scales to corpus size.

---

## 16. Risk review

| Risk | Affected RT owner(s) | Mitigation | Required future tests | PR-4A may proceed? |
|---|---|---|---|---|
| Validation integration becomes a universal rule engine | RT-011, all RT owners | Invariant families are names + declarations; evaluation stays in the kernel pipeline and future RT owners. Forbidden-method tests on the service. | No-universal-rule-engine tests; service method audits | Yes |
| Validation bypasses transaction lifecycle | RT-001, RT-011 | Validation emits references; transaction lifecycle consumes them. No commitment path exists inside validation. | Phase boundary tests; no-commitment-method tests | Yes |
| Validation mutates state directly | RT-001 | Frozen dataclasses, no mutation methods, no state store coupling. | No-state-mutation tests | Yes |
| Validation appends events directly | RT-001 | No ledger coupling; result shapes hardcode no-append posture. | No-event-append tests | Yes |
| Validation becomes a donor-rule importer | RT-012, all RT owners | Donor assumptions are explicitly non-authoritative inputs; lexicon review boundary preserved. | Donor non-authority tests | Yes |
| Hidden info leaks through validation results | RT-005 | `hidden_info_safe`/`player_visible` coupling on all result/route shapes; leak-safe summary rule. | Hidden-info summary safety tests | Yes |
| Model text becomes validation authority | RT-011, RT-005 | `rejected_by_authority_mismatch` decision; model_non_authority_invariant family; no model integration exists. | No-model-authority tests | Yes |
| Source-local content becomes canon through validation | RT-012 | source_local_authority and canon_boundary families; `reject_source_local_authority` route. | Source-local authority rejection tests | Yes |
| Generated content becomes durable without provenance | RT-008 | generated_content_provenance family; `rejected_by_provenance_gap` and `quarantine_generated_content` routes. | Provenance gap tests | Yes |
| Combat/resource/ability logic enters the validation layer | RT-002, RT-003, RT-004 | `request_downstream_domain_validation` routing; explicit non-ownership; forbidden-method tests. | Domain-logic absence tests | Yes |
| Validation rejects valid state due to under-modeled schemas | RT-011, schema owners | `escalate_doctrine_gap` route for under-modeled schema findings rather than silent rejection. | Schema mismatch escalation tests | Yes |
| Validation passes invalid state due to too-broad schemas | RT-011, schema owners | Coverage visibility (families checked are declared on results) makes gaps reviewable; hardening ledger tracks family completeness. | Coverage declaration tests | Yes |
| Validation lacks replay/hash audit trace | RT-011 | runtime_trace_invariant: untraceable decisions are invalid; replay audit references required on quarantine. | Trace presence tests | Yes |
| Persistence implemented too early | RT-001, RT-011 | persistence_boundary posture is reference-only; no write paths planned or permitted. | No-persistence tests | Yes |
| Context-packet compiler built too early | RT-005 | Compiler remains absent and guardrail-tested; validation only emits leak-safe summaries as data. | Package guardrail tests | Yes |

**Risk finding:** all 15 reviewed risks are mitigated by the planned posture. None blocks PR-4A.

---

## 17. Required hardening ledger

| Hardening item | Current status | Risk level | Required before PR-4A | Required before resource/combat/ability services | Future owner | Recommended PR |
|---|---|---|---|---|---|---|
| Invariant family completeness | 21 families declared in this plan; completeness unproven against full corpus | Medium | false | true | RT-011 | Future validation hardening PR |
| Hidden-info summary safety | Pattern proven in PR-3A rejection shape; not yet applied to validation surfaces | Medium | false (PR-4A applies it) | true | RT-005 / RT-011 | RUNTIME-DOMAIN-PR-4A |
| Generated-content provenance validation | Presence/shape checks planned only | Medium | false | true | RT-008 | Future RT-008 plan/impl |
| Schema mismatch handling | Decision and route defined in plan only | Medium | false | true | RT-011 | RUNTIME-DOMAIN-PR-4A (shape), future hardening (behavior) |
| Authority mismatch handling | Decision and route defined in plan only | High (core invariant) | false (PR-4A skeletonizes shape) | true | RT-011 | RUNTIME-DOMAIN-PR-4A |
| Phase-boundary validation | Decision and route defined in plan only | Medium | false | true | RT-001 / RT-011 | RUNTIME-DOMAIN-PR-4A (shape) |
| Replay/hash audit references | Reference posture defined; no verification exists | Medium | false | true | RT-011 | Future persistence/replay PRs |
| Transaction/event readiness validation | Shape coupling exists in PR-3A; validation side planned only | Medium | false | true | RT-001 / RT-011 | RUNTIME-DOMAIN-PR-4A |
| Validator parity with factories | Posture established in PR-1A through PR-3A; must repeat in PR-4A | Low | true (PR-4A must ship with parity) | true | Test maintenance | RUNTIME-DOMAIN-PR-4A |
| Manually constructed invalid object tests | Pattern established in prior skeleton tests | Low | true (PR-4A must include them) | true | Test maintenance | RUNTIME-DOMAIN-PR-4A |
| No-model-authority tests | Absent (no validation surfaces exist yet) | High | true (PR-4A must include them) | true | RT-011 | RUNTIME-DOMAIN-PR-4A |
| No-state-mutation tests | Pattern established in prior skeletons | Low | true | true | Test maintenance | RUNTIME-DOMAIN-PR-4A |
| No-event-append tests | Pattern established in prior skeletons | Low | true | true | Test maintenance | RUNTIME-DOMAIN-PR-4A |
| No-persistence tests | Pattern established in prior skeletons | Low | true | true | Test maintenance | RUNTIME-DOMAIN-PR-4A |
| No-universal-rule-engine tests | Absent | High | true (PR-4A must include forbidden-method and no-domain-logic tests) | true | RT-011 | RUNTIME-DOMAIN-PR-4A |

Items marked "required before PR-4A: true" are test-discipline requirements that PR-4A itself must satisfy in its own test suite; none requires a separate PR-4B hardening pass before PR-4A may begin.

---

## 18. Implementation PR authorization boundary

If this plan is accepted, the later implementation PR is:

**RUNTIME-DOMAIN-PR-4A: Validation Integration and Invariant Enforcement Skeleton Implementation**

PR-4A may create only:

- `src/astra_runtime/domain/validation_integration.py`
- Focused tests for the validation integration skeleton
- Domain `__init__.py` export updates
- Registry/decision updates
- Guardrail updates allowing only `validation_integration.py` as the new authorized domain file

PR-4A must remain skeleton-only and must not:

- implement domain validation rules
- mutate state
- apply deltas
- append events
- persist
- replay
- execute commands
- parse player language
- resolve actions
- calculate resources
- resolve combat
- resolve abilities/effects
- mutate inventory
- mutate missions/social state
- call models
- compile context packets
- run live play

---

## 19. Future implementation test requirements

PR-4A's test suite must cover:

- import/export integrity (all public symbols importable from the domain package)
- constants complete (`VALIDATION_INTEGRATION_STAGES`, `VALIDATION_INTEGRATION_DECISIONS`, `VALIDATION_INVARIANT_FAMILIES`, `VALIDATION_FAILURE_ROUTES` match this plan)
- dependency creation/validation
- invariant declaration creation/validation
- validation request creation/validation
- validation result creation/validation
- failure route creation/validation
- hidden-info safety rule (`player_visible=True` requires `hidden_info_safe=True`)
- generated-content provenance rule (provenance-gap shapes reject/route correctly)
- schema/authority/phase mismatch rules (decision shapes validate correctly)
- transaction/event readiness rule (`passed=True` requires `validation_ref_id`)
- validator parity (validators return False exactly where factories raise)
- metadata copy safety (deep-copy, `MappingProxyType`, `to_dict()` isolation)
- frozen dataclasses (immutability verified)
- service statelessness (`__dict__ == {}`)
- no forbidden methods (`execute`, `run`, `mutate`, `apply`, `apply_delta`, `commit`, `append`, `persist`, `save`, `load`, `replay`, `rollback`, `resolve`, `roll`, `narrate`, `prompt`, `model`, `enforce` absent from the service)
- no state mutation
- no event append
- no persistence
- no replay
- no command execution
- no resource/combat/ability/inventory/mission/social logic
- no context-packet compiler
- no prompt/model/live-play/UI behavior
- registry/decision tracking (PR-4A IDs present)
- domain package guardrails (authorized file set updated to include exactly `validation_integration.py`)

---

## 20. Gate finding

```yaml
gate_finding:
  validation_integration_invariant_enforcement_plan_defined: true
  ready_for_validation_integration_skeleton_implementation_pr: true
  requires_pr_4b_hardening_before_pr_4a: false
  validation_integration_code_authorized_by_this_pr: false
  invariant_enforcement_code_authorized_by_this_pr: false
  domain_validation_rules_authorized_by_this_pr: false
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  transaction_execution_authorized_by_this_pr: false
  actual_event_commitment_authorized_by_this_pr: false
  event_sourcing_authorized_by_this_pr: false
  mutable_runtime_state_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  state_delta_application_authorized_by_this_pr: false
  event_ledger_append_authorized_by_this_pr: false
  durable_persistence_authorized_by_this_pr: false
  replay_engine_authorized_by_this_pr: false
  command_execution_authorized_by_this_pr: false
  command_parser_authorized_by_this_pr: false
  resource_math_authorized_by_this_pr: false
  combat_resolution_authorized_by_this_pr: false
  ability_resolution_authorized_by_this_pr: false
  inventory_mutation_authorized_by_this_pr: false
  mission_mutation_authorized_by_this_pr: false
  social_faction_mutation_authorized_by_this_pr: false
  generated_content_persistence_authorized_by_this_pr: false
  context_packet_compiler_authorized_by_this_pr: false
  prompt_templates_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  ui_client_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-4A validation integration and invariant enforcement skeleton implementation
  next_step_status: narrow_skeleton_implementation_pending_review
```

---

## 21. Recommended next PR

**Recommended:** RUNTIME-DOMAIN-PR-4A: Validation Integration and Invariant Enforcement Skeleton Implementation.

PR-4A may create only narrow skeleton surfaces (`src/astra_runtime/domain/validation_integration.py` with constants, frozen dataclasses, factories, validators, and a stateless service wrapper), focused tests, domain export updates, registry/decision updates, and guardrail updates. It must follow the posture proven by PR-1A, PR-2A, and PR-3A, and it remains pending review of this plan.

---

## 22. Non-implementation reaffirmation

This PR adds no:

- runtime code
- domain-service code
- validation integration implementation
- invariant enforcement implementation
- domain validation rules
- transaction execution
- actual event commitment
- event sourcing
- mutable runtime state
- state mutation
- state delta application
- event ledger append
- durable persistence
- database schema
- replay engine
- command execution
- command parser
- action legality expansion
- resource math
- combat resolution
- ability resolution
- inventory mutation
- mission/social mutation
- generated-content persistence
- context-packet compiler
- prompt templates
- model integration
- live-play adapter
- UI/client
- training data
- donor-content audit
- pilot conversion authorization
- sourcebook inclusion authorization
- canon promotion

---

## 23. Classification block

```yaml
runtime_domain_pr_4:
  plan_id: RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001
  artifact_type: validation_integration_invariant_enforcement_service_plan
  implementation_status: non_executable_plan
  derives_from:
    - RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001
    - RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001
    - RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001
    - RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001
    - RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001
    - RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001
    - RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
    - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
    - RT-001
    - RT-005
    - RT-008
    - RT-011
  defines_validation_integration_model: true
  defines_invariant_enforcement_model: true
  defines_validation_decision_model: true
  defines_invariant_family_model: true
  defines_validation_failure_routing: true
  defines_hidden_information_validation_safety: true
  defines_generated_content_provenance_validation: true
  defines_kernel_interface_consumption_plan: true
  defines_domain_service_handoff_boundaries: true
  defines_future_implementation_architecture: true
  defines_future_data_shapes: true
  defines_corpus_scale_validation_pressure_review: true
  defines_future_hardening_ledger: true
  authorizes_validation_integration_code_by_this_pr: false
  authorizes_invariant_enforcement_code_by_this_pr: false
  authorizes_domain_validation_rules_by_this_pr: false
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
  authorizes_conversion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-4A validation integration and invariant enforcement skeleton implementation, pending review
```

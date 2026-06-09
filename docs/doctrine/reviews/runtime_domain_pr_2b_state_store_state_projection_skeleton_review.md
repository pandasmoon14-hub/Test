# RUNTIME-DOMAIN-PR-2B: State Store / State Projection Skeleton Review

---

## 1. Purpose and status

This document is **RUNTIME-DOMAIN-PR-2B**, a review/gate-only artifact.

It follows **RUNTIME-DOMAIN-PR-2A** (State Store and State Projection Skeleton Implementation, merged as PR #259).

This document reviews the state store and state projection skeleton implementation delivered by PR-2A. It does not implement code.

**Artifact type:** state_store_state_projection_skeleton_review_gate
**Implementation status:** non_executable_review_gate
**Review ID:** RUNTIME-DOMAIN-PR-2B-STATE-STORE-STATE-PROJECTION-SKELETON-REVIEW-001

---

## 2. Source ledger

All source artifacts consulted for this review:

| Source | ID | File(s) |
|---|---|---|
| RUNTIME-DOMAIN-PR-2A implementation | RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001 | `src/astra_runtime/domain/state_store.py`, `src/astra_runtime/domain/state_projection.py`, `src/astra_runtime/domain/__init__.py` |
| RUNTIME-DOMAIN-PR-2 plan | RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001 | `docs/doctrine/reviews/runtime_domain_pr_2_state_store_state_projection_service_plan.md` |
| RUNTIME-DOMAIN-PR-1B review | RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001 | `docs/doctrine/reviews/runtime_domain_pr_1b_command_lifecycle_action_legality_skeleton_review.md` |
| RUNTIME-DOMAIN-PR-1A implementation | RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001 | `src/astra_runtime/domain/command_lifecycle.py`, `src/astra_runtime/domain/action_legality.py` |
| RUNTIME-DOMAIN-PR-1 plan | RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001 | `docs/doctrine/reviews/runtime_domain_pr_1_command_lifecycle_action_legality_service_plan.md` |
| RUNTIME-DOMAIN-PR-0 sequencing plan | RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001 | `docs/doctrine/reviews/runtime_domain_pr_0_domain_service_implementation_sequencing_plan.md` |
| RUNTIME-IMPL-PR-8 gate | RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001 | `docs/doctrine/reviews/runtime_impl_pr_8_post_kernel_skeleton_review_domain_service_readiness_gate.md` |
| Kernel: schema_registry | RUNTIME-IMPL-PR-1 | `src/astra_runtime/kernel/schema_registry.py` |
| Kernel: record_identity | RUNTIME-IMPL-PR-1 | `src/astra_runtime/kernel/record_identity.py` |
| Kernel: command_envelope | RUNTIME-IMPL-PR-2 | `src/astra_runtime/kernel/command_envelope.py` |
| Kernel: transaction_preview | RUNTIME-IMPL-PR-2 | `src/astra_runtime/kernel/transaction_preview.py` |
| Kernel: state_delta | RUNTIME-IMPL-PR-3 | `src/astra_runtime/kernel/state_delta.py` |
| Kernel: event_ledger | RUNTIME-IMPL-PR-3 | `src/astra_runtime/kernel/event_ledger.py` |
| Kernel: rng_interface | RUNTIME-IMPL-PR-4 | `src/astra_runtime/kernel/rng_interface.py` |
| Kernel: table_oracle | RUNTIME-IMPL-PR-4 | `src/astra_runtime/kernel/table_oracle.py` |
| Kernel: validation_pipeline | RUNTIME-IMPL-PR-5 | `src/astra_runtime/kernel/validation_pipeline.py` |
| Kernel: hidden_information | RUNTIME-IMPL-PR-6 | `src/astra_runtime/kernel/hidden_information.py` |
| Kernel: context_projection | RUNTIME-IMPL-PR-6 | `src/astra_runtime/kernel/context_projection.py` |
| Kernel: persistence_boundary | RUNTIME-IMPL-PR-7 | `src/astra_runtime/kernel/persistence_boundary.py` |
| Kernel: replay_audit | RUNTIME-IMPL-PR-7 | `src/astra_runtime/kernel/replay_audit.py` |
| Kernel: runtime_trace | RUNTIME-IMPL-PR-7 | `src/astra_runtime/kernel/runtime_trace.py` |
| Domain: command_lifecycle | RUNTIME-DOMAIN-PR-1A | `src/astra_runtime/domain/command_lifecycle.py` |
| Domain: action_legality | RUNTIME-DOMAIN-PR-1A | `src/astra_runtime/domain/action_legality.py` |
| Domain tests: state store | — | `tests/runtime/test_domain_state_store_skeleton.py` |
| Domain tests: state projection | — | `tests/runtime/test_domain_state_projection_skeleton.py` |
| Domain tests: command lifecycle | — | `tests/runtime/test_domain_command_lifecycle_skeleton.py` |
| Domain tests: action legality | — | `tests/runtime/test_domain_action_legality_skeleton.py` |
| RT-001 | command lifecycle / action legality | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md` |
| RT-002 | resource / consequence math | `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md` |
| RT-003 | combat / hazard / damage / recovery | `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md` |
| RT-004 | ability / effect / skill binding | `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md` |
| RT-005 | context packet / hidden information | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md` |
| RT-006 | mission / reward / clue routing | `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md` |
| RT-007 | social / faction / actor knowledge | `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md` |
| RT-008 | generated-content provenance / recurrence | `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md` |
| RT-009 | runtime RNG / table oracle | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md` |
| RT-010 | inventory / item / vehicle / asset | `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md` |
| RT-011 | validation / readiness tooling | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md` |
| RT-012 | D-series promotion boundary | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md` |
| Registry | REGISTRY-001 | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` |
| Decision log | — | `docs/decisions/current_decisions_log.md` |

---

## 3. Backend-first invariant

**Astra Ascension must be model-interchangeable.** The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

### Review implication

State store and state projection skeletons may represent backend-owned state references, snapshot references, projection requests, and projection results, but they must not become mutable state stores, event committers, persistence engines, replay engines, context-packet compilers, or model-facing authority systems.

---

## 4. PR-2A implementation review

| Artifact | Expected scope | Observed implementation | Scope status | Risks | Required follow-up | Downstream readiness |
|---|---|---|---|---|---|---|
| Domain package export update | `__init__.py` adds state_store and state_projection imports/exports alongside existing command_lifecycle and action_legality | 155-line `__init__.py`; imports all public symbols from `state_store` (17 symbols) and `state_projection` (22 symbols); `__all__` list covers all 4 modules cleanly | within_scope | None | None | Clean import surface for PR-3 planning |
| `state_store.py` | Skeleton-only: immutable state record/snapshot/visibility reference surfaces, frozen dataclasses, stateless service wrapper, no mutable state, no persistence | 341 lines; 10 state record categories; 6 authority levels; 6 visibility tiers; `StateVisibilityDescriptor` frozen dataclass; `StateRecordRef` frozen dataclass with optional IDs (schema_id, source_event_id, source_delta_id, provenance_id); `StateSnapshotRef` frozen dataclass with tuple state_ref_ids; `StateStoreService` stateless wrapper; `MappingProxyType`/`copy.deepcopy` metadata posture; factory and validator helpers; no imports from kernel modules | within_scope | None observed; no mutation, no persistence, no execution | Visibility-tier alignment with kernel `hidden_information` (future) | Stable skeleton dependency |
| `state_projection.py` | Skeleton-only: immutable projection request/result/dependency/rejection surfaces, frozen dataclasses, backend-hidden constraint, stateless service wrapper, no state fetch, no mutation | 526 lines; 12 projection types; 6 statuses; 4 backend-hidden forbidden types; 13 allowed dependency types; `StateProjectionDependency` frozen dataclass; `StateProjectionRejection` frozen dataclass with hidden_info_safe/player_visible flags; `StateProjectionRequest` frozen dataclass with include_backend_hidden constraint; `StateProjectionResult` frozen dataclass with redacted/visible/all ref ID tuples; `project_state_view` helper; `StateProjectionService` stateless wrapper; imports only `STATE_AUTHORITY_LEVELS`, `StateRecordRef`, `StateSnapshotRef` from `state_store` | within_scope | None observed; no state fetch, no context-packet compilation, no model integration | Projection status/result consistency hardening (future) | Stable skeleton dependency |
| State store tests | Comprehensive skeleton tests: categories, authority levels, visibility tiers, creation, validation, immutability, metadata safety, service wrapper, guardrails, validator parity, tracking | 409 lines; `TestDomainImports`, `TestStateRecordCategories`, `TestStateAuthorityLevels`, `TestVisibilityTiers` (parametrized 6 tiers), `TestStateVisibilityDescriptor` (11 cases), `TestStateRecordRef` (10 cases), `TestStateSnapshotRef` (6 cases), `TestStateStoreService` (5 cases inc. forbidden-method + mutation-method checks), `TestGuardrailsDomainPackage` (7 file-absence checks), `TestValidatorParityStateStore` (6 bypass cases), `TestDecisionLogTracking`, `TestRegistryTracking` | within_scope | None | None | Adequate coverage |
| State projection tests | Comprehensive skeleton tests: projection types, statuses, dependency types, rejection, request, result, project_state_view, service wrapper, guardrails, validator parity | 387 lines; `TestDomainImports`, `TestProjectionTypes` (parametrized 12 types), `TestProjectionStatuses` (parametrized 6 statuses), `TestStateProjectionDependency` (5 cases), `TestStateProjectionRejection` (4 cases), `TestStateProjectionRequest` (9 cases inc. backend-hidden enforcement), `TestStateProjectionResult` (8 cases), `TestProjectStateView` (4 cases), `TestStateProjectionService` (4 cases inc. forbidden-method checks), `TestValidatorParityProjection` (6 bypass cases) | within_scope | None | None | Adequate coverage |
| Prior guardrail test updates | Shift to "domain package contains only authorized modules" including state_store.py and state_projection.py | `TestGuardrailsDomainPackage` in state store tests checks authorized set: `{__init__.py, command_lifecycle.py, action_legality.py, state_store.py, state_projection.py, __pycache__}`; checks absence of `transaction_lifecycle.py`, `event_commitment.py`, `resource_math.py`, `combat.py`, model package, `context_packet_compiler.py` | within_scope | None | None | Safe transition |
| Registry tracking | Entry added for RUNTIME-DOMAIN-PR-2A | Registry entry at `RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001` with `file_id`, full authorization matrix, changelog version 0.1.71 | within_scope | None | None | Tracked |
| Decision-log tracking | Entry added for RUNTIME-DOMAIN-PR-2A | Decision log entry at `RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001` with scope confirmation, reason, implication, revisit trigger, classification block | within_scope | None | None | Tracked |

**Summary:** All PR-2A artifacts are within skeleton-only scope. No mutable runtime state, no state mutation, no delta application, no event commitment, no event sourcing, no durable persistence, no replay engine, no command execution, no model/prompt/live-play behavior exists. Registry and decision log each have one clean PR-2A record. Guardrails now safely allow only authorized domain modules.

---

## 5. State store skeleton review

### State record categories

10 categories in `STATE_RECORD_CATEGORIES`: `authoritative_runtime`, `projected`, `visible`, `hidden_backend_only`, `derived`, `cached_ephemeral`, `source_local_converted`, `canon_sourcebook`, `generated_pending_provenance`, `persisted_snapshot_boundary`.

**Finding:** Comprehensive coverage of the state ownership model defined in RUNTIME-DOMAIN-PR-2 section 6. All 10 categories map directly to plan section 6.1-6.10.

### Authority levels

6 levels in `STATE_AUTHORITY_LEVELS`: `authoritative`, `derived`, `projected`, `reference_only`, `non_authoritative`, `pending_provenance`.

**Finding:** Adequate for skeleton scope. Covers the authority spectrum from full authority through pending provenance.

### Visibility tiers

6 tiers in `_VISIBILITY_TIERS`: `backend_hidden`, `gm_visible`, `actor_visible`, `player_visible`, `public`, `redacted`.

**Finding:** Matches the hidden-information boundary defined in RUNTIME-IMPL-PR-6. The `_VISIBILITY_TIERS` set is module-private (not exported), which is appropriate.

### StateVisibilityDescriptor shape

Frozen dataclass with fields: `visibility_id`, `visibility_tier`, `hidden_info_safe` (bool), `player_visible` (bool), `metadata` (MappingProxyType). Factory validates visibility_tier membership, bool types, non-empty ID.

**Finding:** Clean shape. `hidden_info_safe` and `player_visible` are structural safety markers matching the pattern established by `LegalityBlockReason` in action_legality.

### StateRecordRef shape

Frozen dataclass with fields: `state_ref_id`, `record_id`, `record_type`, `category`, `authority_level`, `visibility` (StateVisibilityDescriptor), `schema_id` (optional), `source_event_id` (optional), `source_delta_id` (optional), `provenance_id` (optional), `metadata` (MappingProxyType).

**Finding:** Comprehensive reference surface. Optional IDs for schema, event, delta, and provenance provide future integration hooks without premature coupling. All optional IDs validated as non-empty when present.

### StateSnapshotRef shape

Frozen dataclass with fields: `snapshot_id`, `snapshot_scope`, `state_ref_ids` (tuple[str, ...]), `authority_level`, `source_event_id` (optional), `replay_audit_id` (optional), `persistence_boundary_id` (optional), `metadata` (MappingProxyType).

**Finding:** Clean shape. `state_ref_ids` as tuple matches the immutable posture. Optional IDs for event, replay audit, and persistence boundary provide future handoff hooks.

### Factory helpers

`create_state_visibility_descriptor`, `create_state_record_ref`, `create_state_snapshot_ref` all validate inputs thoroughly, reject invalid enums, validate optional-non-empty strings, deep-copy metadata.

**Finding:** Consistent with factory patterns in command_lifecycle and action_legality.

### Validator helpers

`validate_state_visibility_descriptor`, `validate_state_record_ref`, `validate_state_snapshot_ref` all perform structural checks matching factory constraints. `validate_state_record_ref` chains to `validate_state_visibility_descriptor` for the nested visibility field.

**Finding:** Validator parity is strong. Optional ID fields checked for non-empty when present.

### Metadata deep-copy posture

All dataclasses use `_safe_meta` which applies `MappingProxyType(copy.deepcopy(dict(metadata)))`. All `to_dict()` methods apply `copy.deepcopy(dict(self.metadata))`.

**Finding:** Correct. Consistent with all prior domain and kernel skeletons.

### MappingProxyType/read-only metadata posture

All metadata fields default to `MappingProxyType({})`. External callers cannot mutate internal metadata.

**Finding:** Correct.

### Frozen dataclasses

All three dataclasses use `@dataclass(frozen=True)`.

**Finding:** Correct. Immutable by construction.

### Stateless StateStoreService

`StateStoreService` has four methods: `create_record_ref`, `create_snapshot_ref`, `validate_record_ref`, `validate_snapshot_ref`. All delegate to module-level functions. No instance state.

**Finding:** Correct stateless wrapper. Tests verify absence of forbidden methods (`get_state`, `set_state`, `read`, `write`, `save`, `load`, `apply`, `mutate`, `commit`, `replay`, `restore`, `execute`, `run`, `model`, `prompt`) and mutation methods (`mutate`, `apply_delta`, `commit_event`, `store`, `persist`).

### Absence confirmations

- No mutable state: confirmed — no instance variables, no class-level mutable state, no global state.
- No state mutation: confirmed — no methods that modify data after construction.
- No state delta application: confirmed — no import of `state_delta`, no delta-applying logic.
- No event commitment: confirmed — no import of `event_ledger`, no event-committing logic.
- No persistence/replay: confirmed — no import of `persistence_boundary` or `replay_audit`.
- No command execution: confirmed — no import of `command_envelope`, no execution logic.

### Future hardening candidates

| Item | Current status | Risk | Notes |
|---|---|---|---|
| State category/authority semantic consistency | No cross-validation between category and authority_level | Low | e.g., `cached_ephemeral` + `authoritative` is allowed but semantically odd |
| Visibility-tier naming alignment with hidden information kernel | `_VISIBILITY_TIERS` duplicated from `hidden_information.py`; no shared constant | Low | Future integration should use a single source of truth for visibility tiers |
| Optional ID validation | Optional IDs validated as non-empty when present; no format validation | Low | Future schema_registry/record_identity integration will define format rules |
| Metadata immutability limits | `MappingProxyType` prevents top-level mutation but nested mutable objects could theoretically be placed inside; `deepcopy` mitigates at construction time | Low | Acceptable for skeleton; deeper enforcement belongs to future validation |
| Schema registry integration | `schema_id` is an optional string; no connection to kernel `schema_registry` | Medium | Future integration point |
| Record identity integration | `record_id` is a plain string; no connection to kernel `record_identity` format | Medium | Future integration point |
| State delta reference integration | `source_delta_id` is an optional string; no connection to kernel `state_delta` | Low | By design — reference only |
| Event ledger reference integration | `source_event_id` is an optional string; no connection to kernel `event_ledger` | Low | By design — reference only |
| Persistence boundary handoff | `persistence_boundary_id` is an optional string; no connection to kernel `persistence_boundary` | Low | Future integration point |
| Replay/hash audit handoff | `replay_audit_id` is an optional string; no connection to kernel `replay_audit` | Low | Future integration point |
| Runtime trace integration | No runtime_trace import or trace emission | Low | Deferred to future service work |

---

## 6. State projection skeleton review

### Projection type set

12 types in `STATE_PROJECTION_TYPES`: `full_backend`, `player_visible`, `actor_scoped`, `scene_scoped`, `faction_social`, `combat_encounter`, `inventory_asset`, `mission_clue`, `hidden_info_redacted`, `audit_provenance`, `model_facing_candidate`, `ui_client_candidate`.

**Finding:** Maps directly to RUNTIME-DOMAIN-PR-2 plan sections 7.1-7.12. All 12 planned projection types are represented.

### Projection status set

6 statuses in `STATE_PROJECTION_STATUSES`: `requested`, `validated`, `materialized`, `redacted`, `rejected`, `quarantined`.

**Finding:** Maps to plan section 8 lifecycle stages: projection_requested, projection_validated, projection_materialized, projection_redacted, projection_rejected. `quarantined` is an additional safety status. Adequate for skeleton.

### Backend-hidden forbidden projection types

4 forbidden types in `_BACKEND_HIDDEN_FORBIDDEN_TYPES`: `player_visible`, `actor_scoped`, `model_facing_candidate`, `ui_client_candidate`.

**Finding:** Correct. These types must never include backend-hidden state. The constraint is enforced in both `create_state_projection_request` and `validate_state_projection_request`.

### StateProjectionDependency shape

Frozen dataclass with fields: `dependency_id`, `dependency_type`, `required` (bool), `metadata`. Factory validates `dependency_type` against 13 allowed types covering all kernel and domain integration points.

**Finding:** Clean shape. Dependency types include `state_record_ref`, `state_snapshot_ref`, `hidden_information`, `context_projection`, `validation_result`, `runtime_trace`, `persistence_boundary`, `replay_audit`, `transaction_lifecycle`, `event_ledger`, `command_lifecycle`, `model_evaluation`, `live_play_gate`.

### StateProjectionRejection shape

Frozen dataclass with fields: `rejection_id`, `reason_code`, `message`, `hidden_info_safe` (bool), `player_visible` (bool), `metadata`.

**Finding:** Clean shape. `hidden_info_safe` and `player_visible` flags provide structural safety markers consistent with the action_legality `LegalityBlockReason` pattern.

### StateProjectionRequest shape

Frozen dataclass with fields: `projection_request_id`, `requester_id`, `projection_type`, `state_ref_ids` (tuple[str, ...]), `snapshot_id` (optional), `visibility_tier`, `include_backend_hidden` (bool), `dependencies` (tuple[StateProjectionDependency, ...]), `metadata`.

**Finding:** Comprehensive request surface. The `include_backend_hidden` constraint is enforced against `_BACKEND_HIDDEN_FORBIDDEN_TYPES` in both factory and validator.

### StateProjectionResult shape

Frozen dataclass with fields: `projection_id`, `projection_request_id`, `projection_type`, `status`, `state_ref_ids` (tuple), `redacted_state_ref_ids` (tuple), `visible_state_ref_ids` (tuple), `rejection` (optional StateProjectionRejection), `validation_id` (optional), `trace_id` (optional), `metadata`.

**Finding:** Clean separation of all/redacted/visible ref ID sets. Rejection is optional and typed. `validation_id` and `trace_id` provide future integration hooks.

### Factory helpers

`create_state_projection_dependency`, `create_state_projection_rejection`, `create_state_projection_request`, `create_state_projection_result` all validate inputs thoroughly, including backend-hidden constraint, dependency type validation, and string sequence normalization.

**Finding:** Consistent with established patterns.

### Validator helpers

`validate_state_projection_dependency`, `validate_state_projection_rejection`, `validate_state_projection_request`, `validate_state_projection_result` all perform structural checks mirroring factory constraints. Request validator checks backend-hidden constraint. Result validator chains to rejection validator when rejection is present.

**Finding:** Validator parity is strong.

### project_state_view helper

`project_state_view` validates the request via `validate_state_projection_request`, then delegates to `create_state_projection_result` using the request's fields. It does not fetch state payloads, does not mutate the request, and does not produce side effects.

**Finding:** Correct skeleton behavior — assembles a result envelope from request metadata without actually fetching or processing state.

### Metadata deep-copy posture

All dataclasses use `_safe_meta` / `deepcopy` pattern. All `to_dict()` methods deep-copy.

**Finding:** Correct and consistent.

### MappingProxyType/read-only metadata posture

Consistent with state_store. All metadata fields default to `MappingProxyType({})`.

**Finding:** Correct.

### Frozen dataclasses

All 5 dataclasses use `@dataclass(frozen=True)`.

**Finding:** Correct.

### Stateless StateProjectionService

`StateProjectionService` has 5 methods: `create_request`, `create_result`, `validate_request`, `validate_result`, `project`. All delegate to module-level functions. No instance state.

**Finding:** Correct stateless wrapper. Tests verify absence of forbidden methods (`fetch_state`, `get_state`, `set_state`, `read`, `write`, `save`, `load`, `apply`, `mutate`, `commit`, `replay`, `restore`, `execute`, `run`, `compile_context_packet`, `model`, `prompt`) and context-packet/model/prompt/live-play methods.

### include_backend_hidden constraint

Enforced in both `create_state_projection_request` (raises `InvalidStateProjectionRequestError`) and `validate_state_projection_request` (returns `False`). Covers all 4 forbidden types.

**Finding:** Sound enforcement. Prevents structural hidden-information leaks through projection type misuse.

### Absence confirmations

- No state fetch: confirmed — `project_state_view` reads request fields only, never accesses external state.
- No state mutation: confirmed — no methods that modify state.
- No context-packet compilation: confirmed — no context-packet assembly logic.
- No model/prompt/live-play behavior: confirmed — no model imports, no prompt construction.

### Future hardening candidates

| Item | Current status | Risk | Notes |
|---|---|---|---|
| Projection status/result semantic consistency | No enforcement that `rejected` status requires a non-None rejection | Low | Future hardening should enforce status/rejection consistency |
| Rejected/quarantined result consistency | `rejected` and `quarantined` statuses do not enforce distinct shapes | Low | Future hardening |
| Hidden-info-safe rejection/message policy | `hidden_info_safe`/`player_visible` flags exist but no policy engine | Medium | Future RT-005 integration must enforce that `hidden_info_safe=False` rejection messages are never player-visible |
| Player-visible vs backend-hidden visibility alignment | `visibility_tier` in request and `_VISIBILITY_TIERS` match; no runtime alignment check against kernel `hidden_information` | Low | Future integration point |
| Dependency declarations as strings vs future object references | `dependency_id` is a plain string; `dependency_type` is enum-validated string | Low | Adequate for skeleton; future may need typed references |
| Validation result integration | `validation_id` field exists but no integration with kernel `validation_pipeline` | Low | Future RT-011 integration point |
| Runtime trace integration | `trace_id` field exists but no integration with kernel `runtime_trace` | Low | Future integration point |
| Context projection kernel integration | No import of kernel `context_projection` module | Low | By design — skeleton only; future projection engine will integrate |
| Model-facing candidate boundary | `model_facing_candidate` type exists but no model-facing safety enforcement beyond backend-hidden constraint | Medium | Future context-packet compiler must add additional safety gates |
| UI-client candidate boundary | `ui_client_candidate` type exists but no UI-safe shape enforcement | Low | Future UI adapter must define shape requirements |
| Transaction/event handoff | No transaction/event handoff mechanism | Low | By design — deferred to PR-3+ |

---

## 7. Validator parity review

### validate_state_record_ref optional ID parity

- `schema_id=""` planted via frozen dataclass bypass: validator returns `False`. **Parity confirmed.**
- `source_event_id=""` planted via bypass: validator returns `False`. **Parity confirmed.**
- `source_delta_id=""` and `provenance_id=""`: same pattern applies (loop over optionals at line 230-233). **Parity confirmed.**
- All optionals as `None`: validator returns `True`. **Parity confirmed.**

### validate_state_snapshot_ref optional ID parity

- `replay_audit_id=""` planted via bypass: validator returns `False`. **Parity confirmed.**
- `source_event_id=""` planted via bypass: validator returns `False`. **Parity confirmed.**
- `persistence_boundary_id=""`: same loop pattern (line 318-320). **Parity confirmed.**
- All optionals as `None`: validator returns `True`. **Parity confirmed.**

### validate_state_projection_request state_ref_ids contents

- `state_ref_ids=("",)` planted via bypass: validator returns `False`. **Parity confirmed.**

### validate_state_projection_request backend-hidden constraint

- `projection_type="player_visible"` + `include_backend_hidden=True` planted via bypass: validator returns `False`. **Parity confirmed.**

### validate_state_projection_request snapshot_id

- `snapshot_id=""` would be checked by line 342-343: validator returns `False` for empty string. **Parity confirmed.**

### validate_state_projection_request dependency object validity

- `dependencies=("bad",)` planted via bypass: validator returns `False` (line 348-351). **Parity confirmed.**

### validate_state_projection_result tuple contents

- `visible_state_ref_ids=("",)` planted via bypass: validator returns `False`. **Parity confirmed.**

### validate_state_projection_result rejection validity

- Invalid rejection type would be caught by `isinstance` check (line 459-460) and `validate_state_projection_rejection` chain (line 462). **Parity confirmed.**

### validate_state_projection_result validation_id/trace_id parity

- `validation_id=""` planted via bypass: validator returns `False`. **Parity confirmed.**
- `trace_id=""` planted via bypass: validator returns `False`. **Parity confirmed.**

### Tests for manually constructed invalid frozen dataclasses

PR-2A tests include 12 bypass tests (6 in `TestValidatorParityStateStore`, 6 in `TestValidatorParityProjection`) that construct frozen dataclasses directly with invalid data and verify validators reject them.

**Finding:** The validator surface is acceptable for later services to depend on. All factory constraints are mirrored by validators, including optional ID non-empty checks, backend-hidden constraints, dependency object type checks, and nested object validation.

---

## 8. Guardrail transition review

### Previous authorized domain files (after PR-1A)

| File | Status |
|---|---|
| `__init__.py` | Present, authorized |
| `command_lifecycle.py` | Present, authorized |
| `action_legality.py` | Present, authorized |

### New authorized domain files (after PR-2A)

| File | Status |
|---|---|
| `__init__.py` | Present, authorized |
| `command_lifecycle.py` | Present, authorized |
| `action_legality.py` | Present, authorized |
| `state_store.py` | Present, authorized |
| `state_projection.py` | Present, authorized |

### Still forbidden

| Forbidden file/package | Status |
|---|---|
| `transaction_lifecycle.py` | Verified absent |
| `event_commitment.py` | Verified absent |
| `validation_integration.py` | Verified absent |
| `resource_math.py` | Verified absent |
| `combat.py` | Verified absent |
| `ability_effects.py` | Verified absent |
| `inventory.py` | Verified absent |
| `mission.py` | Verified absent |
| `social_faction.py` | Verified absent |
| `generated_content.py` | Verified absent |
| `context_packet_compiler.py` (kernel) | Verified absent |
| `src/astra_runtime/model` | Verified absent |
| `src/astra_runtime/prompts` | Verified absent |
| `src/astra_runtime/live_play` | Verified absent |
| `src/astra_runtime/ui` | Verified absent |
| `src/astra_runtime/database` | Verified absent |
| `src/astra_runtime/store` | Verified absent |

**Finding:** The new guardrail posture is safe. The domain package contains exactly 5 authorized files (plus `__pycache__`). The `TestGuardrailsDomainPackage` class in the state store test file enforces this. All forbidden files and packages remain absent.

---

## 9. Kernel dependency review

| Kernel module | Imported by PR-2A | Operationally used by PR-2A | Should remain reference-only now | Future integration point | Risk if used too early | Recommendation |
|---|---|---|---|---|---|---|
| schema_registry | No | No | Yes | State record type/schema validation | Medium: premature schema coupling | Integrate when schema-aware validation is needed |
| record_identity | No | No | Yes | State record ID format validation | Medium: premature ID format coupling | Integrate when ID format enforcement is needed |
| command_envelope | No | No | Yes | Mutation request origin reference | Low | Not needed by state store/projection |
| transaction_preview | No | No | Yes | Mutation handoff reference | Medium: premature transaction coupling | Integrate only via future transaction lifecycle service |
| state_delta | No | No | Yes | Mutation input reference | High: implies state mutation | Do not import until transaction lifecycle service exists |
| event_ledger | No | No | Yes | Event-derived authority reference | High: implies event commitment | Do not import until event commitment service exists |
| rng_interface | No | No | Yes | Provenance tracking reference | Low | Not needed by state store/projection |
| table_oracle | No | No | Yes | Provenance tracking reference | Low | Not needed by state store/projection |
| validation_pipeline | No | No | Yes | State/projection shape validation | Medium: premature integration | Integrate when domain-level validation pipeline is built |
| hidden_information | No | No | Yes | Visibility-tier enforcement | High: premature partition enforcement | Integrate when RT-005 hidden-info safety enforcement is needed |
| context_projection | No | No | Yes | Projection surface filtering | High: premature context compilation | Integrate when projection engine materializes state |
| persistence_boundary | No | No | Yes | Snapshot prepare boundary | High: premature persistence | Integrate only via future persistence service |
| replay_audit | No | No | Yes | Audit hash verification | Medium: premature replay coupling | Integrate when replay/audit service exists |
| runtime_trace | No | No | Yes | Traceable state read/projection | Low: trace is observational | Integrate when trace infrastructure is built |

**Summary:** PR-2A imports no kernel modules directly. The only cross-module import is from `state_store` into `state_projection` (intra-domain, appropriate: `STATE_AUTHORITY_LEVELS`, `StateRecordRef`, `StateSnapshotRef`). PR-2A represents related IDs (schema_id, source_event_id, source_delta_id, provenance_id, replay_audit_id, persistence_boundary_id, validation_id, trace_id) as optional strings for future integration. This is the correct posture — skeleton references without operational coupling.

---

## 10. Corpus-scale state/projection pressure review

| State category | PR-2A handling | Current skeleton sufficient | Future service owner |
|---|---|---|---|
| Player / party state | `StateRecordRef` with `category=authoritative_runtime`, actor-scoped projection type | Yes — reference surface only, no party aggregation | Future state store + RT-001 |
| Creature / NPC state | `StateRecordRef` with creature record_type, visibility-filtered projection | Yes — visibility descriptor handles hidden NPC knowledge | Future state store + RT-003, RT-007 |
| Item / gear / inventory state | `StateRecordRef` with inventory record_type, `inventory_asset` projection type | Yes — ownership-scoped via visibility tier | RT-010 |
| Ability / power / effect state | `StateRecordRef` with ability record_type, actor-scoped projection | Yes — hidden components handled via visibility descriptor | RT-004 |
| Relic / implant / installable asset state | `StateRecordRef` with asset record_type, `inventory_asset` projection type | Yes — may have hidden properties via visibility tier | RT-010 |
| Faction / institution state | `StateRecordRef` with faction record_type, `faction_social` projection type | Yes — faction secrets handled via hidden-info filtering | RT-007 |
| Location / site / region state | `StateRecordRef` with location record_type, `scene_scoped` projection type | Yes — undiscovered locations redacted via visibility tier | Future location service |
| Mission / scenario / adventure state | `StateRecordRef` with mission record_type, `mission_clue` projection type | Yes — clue/secret filtering via visibility tier | RT-006 |
| Vehicle / ship / platform state | `StateRecordRef` with vehicle record_type, `inventory_asset` projection type | Yes — ownership-scoped | RT-010 |
| Hazard / environment state | `StateRecordRef` with hazard record_type, `combat_encounter` projection type | Yes — some hazards hidden via visibility tier | RT-003 |
| Table / oracle references | `StateRecordRef` with `category=reference_only` or `source_local_converted` | Yes — reference data, not mutable state | RT-009 |
| Companion / summon state | `StateRecordRef` with companion record_type, `actor_scoped` projection | Yes — may have hidden properties | RT-004, RT-010 |
| Crafting / salvage / recipe state | `StateRecordRef` with crafting record_type | Yes — recipe discovery via visibility tier | RT-010 |
| Map / diagram state | `StateRecordRef` with `category=reference_only`, fog-of-war via visibility | Yes — undiscovered areas redacted | Future location service |
| Source-local setting / cosmology state | `StateRecordRef` with `category=source_local_converted`; blocked from canonical promotion | Yes — source-local markers preserved by category | RT-012 |
| Generated content pending provenance | `StateRecordRef` with `category=generated_pending_provenance` | Yes — quarantined by category until provenance authorization | RT-008 |
| Hidden information and actor knowledge | `StateVisibilityDescriptor` with `hidden_info_safe`/`player_visible` flags; backend-hidden constraint | Yes — structural safety markers in place | RT-005 |
| Campaign / world memory | `StateRecordRef` with campaign record_type; projected, not authoritative from model summaries | Yes — model summaries never become authoritative state via category enforcement | Future campaign service |
| Temporary combat / encounter state | `StateRecordRef` with `category=cached_ephemeral`, `combat_encounter` projection type | Yes — ephemeral by category | RT-003 |
| Downtime / domain-scale state | `StateRecordRef` with appropriate record_type; scene or actor-scoped projection | Yes — slower lifecycle handled by same reference surface | Future domain-scale service |

**Summary:** PR-2A's skeleton surfaces are sufficient for all 20 state categories. The combination of `STATE_RECORD_CATEGORIES` (10 categories), `STATE_AUTHORITY_LEVELS` (6 levels), `_VISIBILITY_TIERS` (6 tiers), and `STATE_PROJECTION_TYPES` (12 types) provides adequate dimensionality for corpus-scale state representation without premature implementation.

---

## 11. Risk review

| Risk | Affected RT owner(s) | Mitigation | Future test family | PR-2C required |
|---|---|---|---|---|
| State store becomes mutable god object | RT-001, RT-002, RT-003, RT-004, RT-005, RT-006, RT-007, RT-008, RT-010 | `StateStoreService` has no mutation methods; tests verify absence of forbidden methods; all dataclasses are frozen | No-state-mutation guardrail tests (exist) | No |
| Projection becomes hidden-info leak | RT-005, RT-001 | Backend-hidden constraint enforced in factory and validator; `_BACKEND_HIDDEN_FORBIDDEN_TYPES` blocks 4 public-facing projection types | Adversarial hidden-info tests (future) | No |
| Projection result treated as authoritative state | All consuming services | `StateProjectionResult` is a distinct type from `StateRecordRef`; `status` field distinguishes materialized from authoritative | Visible vs backend-hidden projection tests (future) | No |
| State service starts applying deltas | RT-001, RT-002, RT-003, RT-004 | No import of `state_delta`; no delta-applying methods exist | State delta reference-only tests (future) | No |
| State service commits events | All | No import of `event_ledger`; no event-committing methods exist | Event ledger reference-only tests (future) | No |
| State service bypasses validation | RT-011 | Factory helpers validate all inputs; validators mirror constraints; validation_id field provides future pipeline hook | Validation result integration tests (future) | No |
| Persistence is implemented prematurely | RT-011 | No import of `persistence_boundary`; no persistence writes; `persistence_boundary_id` is reference-only | No-persistence guardrail tests (exist in guardrails) | No |
| Replay/hash audit becomes decorative | RT-011 | `replay_audit_id` is a reference-only field; no replay logic exists; future integration must be structural | Runtime trace declaration tests (future) | No |
| Runtime trace omitted from state reads/projections | RT-011 | `trace_id` field exists in projection result; no trace emission yet | Runtime trace integration tests (future) | No |
| Generated content becomes durable state without provenance | RT-008 | `generated_pending_provenance` category explicitly marks content as pending; no persistence path exists | Generated-content provenance tests (future) | No |
| Donor schema assumptions leak into runtime state | RT-012 | `source_local_converted` category preserves source-local markers; `schema_id` is reference-only | Schema registry reference tests (future) | No |
| Source-local content becomes canon state | RT-012 | `source_local_converted` and `canon_sourcebook` are distinct categories; no automatic promotion path | Source-local/canon boundary tests (future) | No |
| Model summaries become memory/state authority | RT-005, RT-008 | No model integration; no prompt construction; all state is backend-owned frozen dataclasses | No-model guardrail tests (exist) | No |
| Context-packet compiler is built too early | RT-005 | No context-packet compilation logic; `StateProjectionService` produces result envelopes only | No-context-packet guardrail tests (exist) | No |
| UI/model-facing projections bypass hidden-info checks | RT-005 | Backend-hidden constraint enforced for `player_visible`, `actor_scoped`, `model_facing_candidate`, `ui_client_candidate` | Adversarial hidden-info tests (future) | No |
| Transaction/event service later bypasses state reference validation | RT-001, RT-011 | Validators are public API; future transaction service must call them | Transaction/validation integration tests (future) | No |

**Summary:** No risks require a PR-2C hardening pass before PR-3 planning. All identified risks are either mitigated by existing skeleton constraints or deferred to future service-level integration. The skeleton's immutable/reference-only/stateless posture is sound.

---

## 12. Required future hardening ledger

| Hardening item | Current status | Risk level | Required before PR-3 | Future owner | Recommended PR |
|---|---|---|---|---|---|
| State category/authority semantic consistency | No cross-validation between category and authority_level | Low | No | State store service | Later domain hardening PR |
| Visibility-tier alignment with hidden information kernel | `_VISIBILITY_TIERS` duplicated; no shared constant | Low | No | State store + RT-005 | Later kernel integration PR |
| State record reference schema registry integration | `schema_id` is optional string; no connection to `schema_registry` | Medium | No | State store + `schema_registry` | Later schema integration PR |
| Record identity integration | `record_id` is plain string; no connection to `record_identity` | Medium | No | State store + `record_identity` | Later identity integration PR |
| State delta reference integration | `source_delta_id` is optional string; no connection to `state_delta` | Low | No | Future transaction lifecycle service | PR-3+ |
| Event ledger reference integration | `source_event_id` is optional string; no connection to `event_ledger` | Low | No | Future event commitment service | PR-3+ |
| Validation result integration | `validation_id` field exists; no pipeline integration | Medium | No | State store/projection + RT-011 | Later validation integration PR |
| Runtime trace integration | `trace_id` field exists; no trace emission | Medium | No | State store/projection + `runtime_trace` | Later trace integration PR |
| Persistence boundary handoff | `persistence_boundary_id` is optional string; no handoff mechanism | Low | No | State store + `persistence_boundary` | Later persistence PR |
| Replay/hash audit handoff | `replay_audit_id` is optional string; no hash computation | Low | No | State store + `replay_audit` | Later replay PR |
| Projection request/result status consistency | No enforcement that `rejected` requires rejection object | Low | No | State projection service | Later domain hardening PR |
| Hidden-info-safe rejection policy | `hidden_info_safe`/`player_visible` flags exist; no enforcement engine | Medium | No | State projection + RT-005 | RT-005 integration PR |
| Model-facing projection hard boundary | `model_facing_candidate` type exists; no model-facing safety enforcement beyond backend-hidden constraint | Medium | No | State projection + context-packet compiler | Context-packet compiler PR |
| UI-client projection hard boundary | `ui_client_candidate` type exists; no UI-safe shape enforcement | Low | No | State projection + UI adapter | UI adapter PR |
| Context-packet compiler handoff | No context-packet assembly logic | Low | No | Future context-packet compiler | Context-packet compiler PR |
| Adversarial hidden-info tests | No adversarial tests that attempt to leak hidden info through projection paths | Medium | No | State projection tests | Later adversarial test PR |
| Model-summary non-authority tests | No tests verifying model output cannot become state authority | Medium | No | State store tests | Later adversarial test PR |

---

## 13. Gate finding

```yaml
gate_finding:
  state_store_state_projection_skeleton_review_complete: true
  pr_2a_scope_confirmed: true
  guardrail_transition_safe: true
  validator_surface_acceptable_for_later_services: true
  ready_for_runtime_domain_pr_3_transaction_lifecycle_event_commitment_service_plan: true
  requires_pr_2c_hardening_before_pr_3: false
  domain_code_authorized_by_this_pr: false
  state_store_code_authorized_by_this_pr: false
  state_projection_code_authorized_by_this_pr: false
  mutable_runtime_state_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  state_delta_application_authorized_by_this_pr: false
  transaction_lifecycle_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  durable_persistence_authorized_by_this_pr: false
  replay_engine_authorized_by_this_pr: false
  command_execution_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-3 transaction lifecycle and event commitment service plan
  next_step_status: planning_only
```

**Rationale:** PR-2A stayed strictly within skeleton-only scope. No blockers, no scope violations, no premature kernel consumption. The guardrail transition from 3 to 5 authorized domain files is safe. State store and state projection skeletons are immutable, stateless, and reference-only. Validator surfaces mirror factory constraints with full parity including optional ID checks, backend-hidden constraints, and nested object validation. No mutable state, no delta application, no event commitment, no persistence, no model integration. All 16 identified risks are mitigated by existing skeleton constraints or belong to future service-level work. No hardening items are required before PR-3 planning.

---

## 14. Recommended next PR

**Recommended:** RUNTIME-DOMAIN-PR-3: Transaction Lifecycle and Event Commitment Service Plan

PR-3 should be planning-only. It should define:

- Transaction lifecycle ownership and responsibility boundaries.
- Event commitment ownership and responsibility boundaries.
- State delta application contract (how accepted commands become committed state changes).
- Event ledger commitment contract (how validated deltas become durable events).
- Command lifecycle handoff integration (how `accepted_for_transaction_planning` feeds transaction service).
- State store read-only integration (how transaction service reads current state via state store projections).
- Validation pipeline integration for transaction/event validation.
- Rollback/correction event boundaries.
- Persistence boundary integration for committed events.
- Replay/hash audit integration for event-sourced state verification.
- Runtime trace integration for transaction/event decisions.
- Hidden-information safety requirements for state changes affecting visibility tiers.
- Guardrail and test requirements for transaction lifecycle skeleton.

PR-3 must not implement transaction lifecycle, event commitment, state mutation, state delta application, persistence, replay, or any other runtime code.

---

## 15. Non-implementation reaffirmation

This PR adds no:

- runtime code
- domain-service code
- state-store implementation changes
- state-projection implementation changes
- mutable runtime state
- state mutation
- state delta application
- transaction lifecycle
- event commitment
- event sourcing
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
- mission / social mutation
- generated-content persistence
- context-packet compiler
- prompt templates
- model integration
- live-play adapter
- UI / client
- training data
- donor-content audit
- pilot conversion authorization
- sourcebook inclusion authorization
- canon promotion

---

## 16. Classification block

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

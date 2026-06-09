# RUNTIME-DOMAIN-PR-1B: Command Lifecycle / Action Legality Skeleton Review

---

## 1. Purpose and status

This document is **RUNTIME-DOMAIN-PR-1B**, a review/gate-only artifact.

It follows **RUNTIME-DOMAIN-PR-1A** (Command Lifecycle and Action Legality Skeleton Implementation), which created the first authorized domain package at `src/astra_runtime/domain/` with `command_lifecycle.py` and `action_legality.py`.

This document reviews the first domain-code skeleton implementation. It does not implement code.

**Artifact type:** command_lifecycle_action_legality_skeleton_review_gate
**Implementation status:** non_executable_review_gate
**Review ID:** RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001

---

## 2. Source ledger

| Source | ID | File |
|---|---|---|
| RUNTIME-DOMAIN-PR-1A implementation | RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001 | `src/astra_runtime/domain/command_lifecycle.py`, `src/astra_runtime/domain/action_legality.py`, `src/astra_runtime/domain/__init__.py` |
| RUNTIME-DOMAIN-PR-1 plan | RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001 | `docs/doctrine/reviews/runtime_domain_pr_1_command_lifecycle_action_legality_service_plan.md` |
| RUNTIME-DOMAIN-PR-0 sequencing plan | RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001 | `docs/doctrine/reviews/runtime_domain_pr_0_domain_service_implementation_sequencing_plan.md` |
| RUNTIME-IMPL-PR-8 post-kernel gate | RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001 | `docs/doctrine/reviews/runtime_impl_pr_8_post_kernel_skeleton_review_domain_service_readiness_gate.md` |
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
| Domain tests: command lifecycle | — | `tests/runtime/test_domain_command_lifecycle_skeleton.py` |
| Domain tests: action legality | — | `tests/runtime/test_domain_action_legality_skeleton.py` |
| RT-001 | command lifecycle and action legality | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md` |
| RT-011 | validation readiness tooling | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md` |
| RT-002 | resource consequence math | `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md` |
| RT-005 | context packet hidden information | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md` |
| RT-009 | runtime RNG table oracle | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md` |
| RT-012 | D-series promotion boundary | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md` |
| Registry | REGISTRY-001 | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` |
| Decision log | — | `docs/decisions/current_decisions_log.md` |

---

## 3. Backend-first invariant

Astra Ascension must be model-interchangeable. The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

**Review implication:**

Command lifecycle and action legality skeletons may classify and represent backend-owned command status, but they must not execute commands, mutate state, commit events, parse player prose, calculate resources, resolve combat or abilities, expose hidden information, or use model output as authority.

---

## 4. PR-1A implementation review

| Artifact | Expected scope | Observed implementation | Scope status | Risks | Required follow-up | Downstream readiness |
|---|---|---|---|---|---|---|
| Domain package creation | New `src/astra_runtime/domain/` with `__init__.py`, `command_lifecycle.py`, `action_legality.py` only | Package created with exactly those three files; no other modules present | within_scope | Additional modules could be added without gate review | Guardrail tests enforce authorized-files-only posture | Ready for PR-2 planning |
| `command_lifecycle.py` | Skeleton-only: immutable result surface, lifecycle stages, stateless service wrapper, no execution | 263 lines; frozen dataclasses; `COMMAND_LIFECYCLE_STAGES` (12 stages); `COMMAND_LIFECYCLE_TERMINAL_STAGES` (4 stages); `_ALLOWED_STATUSES` (5 statuses); `create_command_lifecycle_result` factory; `validate_command_lifecycle_result` validator; `evaluate_command_lifecycle` envelope-aware evaluator; `CommandLifecycleService` stateless wrapper; deep-copy metadata via `MappingProxyType`; imports only `command_envelope` from kernel | within_scope | None observed; no execution, no state mutation, no parser | Terminal stage/status consistency hardening (future) | Stable skeleton dependency |
| `action_legality.py` | Skeleton-only: immutable result surface, decision categories, blocking enforcement, dependency/block/confirmation/quarantine shapes, stateless service wrapper, no domain rules | 566 lines; 12 decision categories; 9 blocking decisions; `_MAY_PROCEED_DECISIONS` and `_MUST_NOT_PROCEED_DECISIONS` enforcement; `DependencyDeclaration` with 13 allowed types; `LegalityBlockReason` with `player_visible` and `hidden_info_safe` flags; `ConfirmationRequirement`; `CommandQuarantineResult`; `ActionLegalityResult` composite; `evaluate_action_legality` with auto-derive `may_proceed_to_preview`; `ActionLegalityService` stateless wrapper; imports only `command_envelope` and `command_lifecycle.COMMAND_LIFECYCLE_STAGES` | within_scope | `hidden_info_safe` flag is structural only — no enforcement engine yet | Hidden-info safety enforcement in future service | Stable skeleton dependency |
| Domain `__init__.py` exports | Re-export all public symbols from both modules | 77 lines; re-exports all public classes, constants, factories, validators, and evaluators from both modules; `__all__` list matches exports | within_scope | None | None | Clean import surface |
| Command lifecycle tests | Comprehensive skeleton tests: stages, statuses, creation, validation, immutability, envelope integration, service wrapper, guardrails | 393 lines; `TestDomainPackageImports`, `TestCommandLifecycleStage`, `TestAllLifecycleStages` (parametrized 12 stages), `TestAllowedStatuses` (parametrized 5 statuses), `TestCreateCommandLifecycleResult` (19 cases), `TestValidateCommandLifecycleResult`, `TestEvaluateCommandLifecycle` (5 cases), `TestCommandLifecycleService` (3 cases inc. forbidden-method check), `TestGuardrails` (15 file-absence checks) | within_scope | None | None | Adequate coverage |
| Action legality tests | Comprehensive skeleton tests: decisions, dependency declarations, block reasons, confirmations, quarantine, result creation/validation, immutability, envelope integration, must-not-proceed enforcement, service wrapper, guardrails | 554 lines (approx); `TestAllDecisionCategories` (parametrized 12 decisions), `TestActionLegalityDecision`, `TestDependencyDeclaration` (parametrized 13 types), `TestLegalityBlockReason`, `TestConfirmationRequirement`, `TestCommandQuarantineResult`, `TestCreateActionLegalityResult` (18+ cases), `TestValidateActionLegalityResult` (5 cases inc. blocking/quarantine checks), `TestEvaluateActionLegality` (14 cases inc. all blocking-decision enforcement), `TestActionLegalityService` (3 cases inc. forbidden-method check), `TestGuardrails` (15+ file-absence checks) | within_scope | None | None | Adequate coverage |
| Prior guardrail test updates | Shift from "no domain package exists" to "domain package contains only authorized modules" | Guardrail test classes in both test files assert absence of `state_store.py`, `transaction_lifecycle.py`, `event_commitment.py`, `resource_math.py`, `combat.py`, `ability_effects.py`, `inventory.py`, `mission.py`, `social_faction.py`, `generated_content.py`, `context_packet_compiler.py`, model/prompts/live_play/ui packages | within_scope | None | `state_projection.py`, `validation_integration.py`, `database`, `store` absence checks added by PR-1B tests | Safe transition |
| Registry tracking | Entry added for RUNTIME-DOMAIN-PR-1A | Registry entry at `RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001` with full authorization matrix; changelog version 0.1.68 | within_scope | None | None | Tracked |
| Decision-log tracking | Entry added for RUNTIME-DOMAIN-PR-1A | Decision log entry at 2026-06-08 with scope confirmation, reason, implication, revisit trigger | within_scope | None | None | Tracked |

**Summary:** All PR-1A artifacts are within skeleton-only scope. No command execution, parser, state mutation, event commitment, resource math, combat/ability/inventory/mission/social logic, model integration, prompt template, live-play adapter, conversion, or canon work is present.

---

## 5. Command lifecycle skeleton review

### Lifecycle stage set

12 stages defined in `COMMAND_LIFECYCLE_STAGES`:
`received`, `envelope_validated`, `actor_bound`, `visibility_checked`, `legality_prechecked`, `dependency_declared`, `preview_requested`, `confirmation_required`, `accepted_for_transaction_planning`, `rejected`, `quarantined`, `cancelled`.

**Finding:** Complete for skeleton scope. Covers intake-through-terminal progression.

### Terminal stage set

4 terminal stages in `COMMAND_LIFECYCLE_TERMINAL_STAGES`:
`accepted_for_transaction_planning`, `rejected`, `quarantined`, `cancelled`.

**Finding:** Correct. Non-terminal stages do not appear in terminal set.

### Lifecycle result shape

`CommandLifecycleResult` is a frozen dataclass with fields: `lifecycle_id`, `command_id`, `stage`, `status`, `validation_id`, `requires_confirmation`, `downstream_dependencies` (tuple), `metadata` (MappingProxyType).

**Finding:** Immutable, deep-copy-safe. Adequate for skeleton.

### Status set

5 statuses in `_ALLOWED_STATUSES`: `in_progress`, `accepted`, `rejected`, `quarantined`, `cancelled`.

**Finding:** Adequate. Maps to terminal and in-progress conditions.

### Validation behavior

`create_command_lifecycle_result` validates: non-empty `lifecycle_id`/`command_id` strings; stage membership in `COMMAND_LIFECYCLE_STAGES`; status membership in `_ALLOWED_STATUSES`; optional `validation_id` non-empty if present; `requires_confirmation` is bool; `downstream_dependencies` is not a bare string, each element non-empty string; metadata is a mapping.

`validate_command_lifecycle_result` performs the same checks on an existing result object.

**Finding:** Thorough for skeleton. No false positives observed.

### Metadata immutability / deep copy posture

Metadata is deep-copied into `MappingProxyType` on construction via `_safe_metadata`. `to_dict()` returns `copy.deepcopy(dict(self.metadata))`.

**Finding:** Correct. External mutation cannot reach internal state.

### `validate_command_envelope` dependency

`evaluate_command_lifecycle` validates the envelope before constructing a result. Invalid envelopes raise `CommandLifecycleError`.

**Finding:** Appropriate. Does not inspect payload contents (no parser behavior).

### Stateless service wrapper

`CommandLifecycleService` has no instance state (`_state`, `_cache`). Single `evaluate` method delegates to `evaluate_command_lifecycle`.

**Finding:** Correct stateless wrapper. No forbidden methods (`execute`, `run`, `commit`, `mutate`, `apply`, `save`, `load`, `model`, `prompt`).

### No command execution / no parser / no transaction / no state mutation / no event commitment

Confirmed absent. The module creates immutable result objects only.

### Future hardening candidates

| Item | Current status | Risk | Notes |
|---|---|---|---|
| Stage/status semantic consistency | No enforcement that terminal stages require terminal statuses | Low | `accepted_for_transaction_planning` + `in_progress` is currently allowed but semantically odd |
| Terminal stage/status consistency | No cross-validation between stage and status | Low | Future hardening should enforce e.g. `rejected` stage requires `rejected` status |
| Dependency declaration naming | `downstream_dependencies` is a `tuple[str, ...]` of free-form strings | Low | Future should use typed dependency declarations like action legality does |
| `validation_id` lifecycle | Optional field; no lifecycle contract for when it must be set | Low | Future validation-pipeline integration will define this |
| Future trace integration | No `runtime_trace` integration | None currently | Deferred to future service work |
| Future transaction preview handoff | `accepted_for_transaction_planning` does not produce a `TransactionPreview` | None currently | By design — skeleton only classifies, does not create transactions |
| Future state projection dependency | No state projection dependency declared | None currently | Correct for skeleton scope |

---

## 6. Action legality skeleton review

### Decision category set

12 decisions in `ACTION_LEGALITY_DECISIONS`:
`legal`, `illegal`, `requires_confirmation`, `requires_more_information`, `blocked_by_hidden_information`, `blocked_by_missing_actor`, `blocked_by_invalid_target`, `blocked_by_resource_precheck`, `blocked_by_timing`, `blocked_by_scope`, `quarantined_for_validation`, `unsupported_command_type`.

**Finding:** Comprehensive for skeleton scope. Covers legal, blocking, confirmation, quarantine, and unsupported cases.

### Blocking decision set

9 blocking decisions in `ACTION_LEGALITY_BLOCKING_DECISIONS`:
`illegal`, `blocked_by_hidden_information`, `blocked_by_missing_actor`, `blocked_by_invalid_target`, `blocked_by_resource_precheck`, `blocked_by_timing`, `blocked_by_scope`, `quarantined_for_validation`, `unsupported_command_type`.

`_MUST_NOT_PROCEED_DECISIONS` adds `requires_more_information` to blocking decisions (10 total).

**Finding:** Correct. `legal` and `requires_confirmation` are the only may-proceed decisions.

### Must-not-proceed enforcement

`create_action_legality_result` raises `InvalidActionLegalityResultError` if `may_proceed_to_preview=True` with a must-not-proceed decision. `evaluate_action_legality` auto-derives `may_proceed_to_preview` from decision membership and raises if explicitly contradicted.

**Finding:** Sound enforcement. Prevents structural hidden-information leaks through preview access.

### Legality result shape

`ActionLegalityResult` is a frozen dataclass with fields: `legality_id`, `command_id`, `decision`, `lifecycle_stage`, `may_proceed_to_preview`, `requires_confirmation`, `dependencies` (tuple of `DependencyDeclaration`), `block_reasons` (tuple of `LegalityBlockReason`), `confirmation_requirement` (optional `ConfirmationRequirement`), `quarantine_result` (optional `CommandQuarantineResult`), `validation_id`, `metadata`.

**Finding:** Rich composite result. All sub-objects are frozen dataclasses. Adequate for skeleton.

### Dependency declaration shape

`DependencyDeclaration` with 13 allowed types: `state_projection`, `transaction_lifecycle`, `validation_integration`, `resource_math`, `combat_resolution`, `ability_resolution`, `inventory_service`, `mission_service`, `social_faction_service`, `generated_content_provenance`, `context_projection`, `model_evaluation`, `live_play_gate`.

**Finding:** Forward-looking dependency taxonomy covering all known future services. Does not implement any of them.

### Block reason shape

`LegalityBlockReason` with `reason_id`, `reason_code`, `message`, `player_visible`, `hidden_info_safe`, `metadata`. All validated as non-empty strings/bools.

**Finding:** `player_visible` and `hidden_info_safe` flags provide structural safety markers. No enforcement engine yet — that belongs to future context projection / hidden information services.

### Confirmation requirement shape

`ConfirmationRequirement` with `confirmation_id`, `reason`, `required`, `metadata`.

**Finding:** Clean shape. Adequate for skeleton.

### Quarantine result shape

`CommandQuarantineResult` with `quarantine_id`, `reason_code`, `message`, `metadata`.

**Finding:** Clean shape. Adequate for skeleton.

### Metadata immutability / deep copy posture

All dataclasses use `MappingProxyType` + `copy.deepcopy` pattern identical to command lifecycle. `to_dict()` methods all deep-copy.

**Finding:** Consistent and correct across all 5 dataclasses.

### `validate_command_envelope` dependency

`evaluate_action_legality` validates envelope before constructing a result. Invalid envelopes raise `ActionLegalityError`.

**Finding:** Appropriate. Does not inspect payload contents.

### Stateless service wrapper

`ActionLegalityService` has no instance state. Single `evaluate` method delegates to `evaluate_action_legality`.

**Finding:** Correct stateless wrapper. No forbidden methods.

### No domain rule engine / no resource math / no combat / no state mutation / no event commitment

Confirmed absent. The module creates immutable result objects and enforces structural decision consistency only.

### Future hardening candidates

| Item | Current status | Risk | Notes |
|---|---|---|---|
| Legal/requires_confirmation preview semantics | Both are may-proceed; no distinction in preview behavior | Low | Future transaction preview service will differentiate |
| Blocked/quarantined/unsupported preview denial | Enforced structurally | None | Sound |
| Block reason hidden-info safety | `hidden_info_safe` flag exists but no enforcement engine | Medium | Future RT-005 context projection must enforce that `hidden_info_safe=False` reasons are never player-visible |
| Player-visible rejection reason policy | `player_visible` flag exists but no policy engine | Low | Future narration service must respect this flag |
| Dependency type expansion | 13 types may need expansion as services are implemented | Low | New services can be added to `_ALLOWED_DEPENDENCY_TYPES` |
| Validation issue integration | `validation_id` field exists but no integration with validation pipeline | Low | Future RT-011 integration point |
| Runtime trace integration | No trace emission | None currently | Deferred to future service work |
| Transaction preview handoff | No preview creation from legality result | None currently | By design — skeleton only classifies |

---

## 7. Guardrail transition review

### Previous guardrail posture

Prior to PR-1A, runtime guardrail tests asserted that no `src/astra_runtime/domain/` package exists.

### New guardrail posture

PR-1A changed guardrail tests to assert that the domain package exists with only authorized modules. The test classes in both `test_domain_command_lifecycle_skeleton.py` and `test_domain_action_legality_skeleton.py` check file absence for all unauthorized domain modules.

### Allowed files

| File | Status |
|---|---|
| `__init__.py` | Present, authorized |
| `command_lifecycle.py` | Present, authorized |
| `action_legality.py` | Present, authorized |

### Still forbidden (verified by guardrail tests)

| Forbidden file/package | Checked by |
|---|---|
| `state_store.py` | lifecycle + legality guardrail tests |
| `state_projection.py` | PR-1B guardrail tests (new) |
| `transaction_lifecycle.py` | lifecycle + legality guardrail tests |
| `event_commitment.py` | lifecycle + legality guardrail tests |
| `validation_integration.py` | PR-1B guardrail tests (new) |
| `resource_math.py` | lifecycle + legality guardrail tests |
| `combat.py` | lifecycle + legality guardrail tests |
| `ability_effects.py` | lifecycle + legality guardrail tests |
| `inventory.py` | lifecycle + legality guardrail tests |
| `mission.py` | lifecycle + legality guardrail tests |
| `social_faction.py` | lifecycle + legality guardrail tests |
| `generated_content.py` | lifecycle + legality guardrail tests |
| `context_packet_compiler.py` (kernel) | lifecycle + legality guardrail tests |
| `src/astra_runtime/model` | lifecycle + legality guardrail tests |
| `src/astra_runtime/prompts` | lifecycle + legality guardrail tests |
| `src/astra_runtime/live_play` | lifecycle + legality guardrail tests |
| `src/astra_runtime/ui` | lifecycle + legality guardrail tests |
| `src/astra_runtime/database` | PR-1B guardrail tests (new) |
| `src/astra_runtime/store` | PR-1B guardrail tests (new) |

**Finding:** The new guardrail posture is safe. The transition from "no domain package" to "domain package with authorized modules only" is correctly implemented. PR-1B tests add coverage for `state_projection.py`, `validation_integration.py`, `database`, and `store` which were not explicitly checked by PR-1A tests.

---

## 8. Kernel dependency review

| Kernel module | Imported by PR-1A | Allowed in PR-1A | Used operationally | Should remain future/later | Risk if used too early | Recommendation |
|---|---|---|---|---|---|---|
| schema_registry | No | Yes (read-only) | No | No | Low | May be consumed for schema registration in future |
| record_identity | No | Yes (read-only) | No | No | Low | May be consumed for ID generation in future |
| command_envelope | Yes | Yes | Yes (validation) | No | None | Appropriate: skeleton validates envelope structure |
| transaction_preview | No | No (not yet) | No | Yes | Medium: premature transaction creation | Do not import until state store/projection exist |
| state_delta | No | No | No | Yes | High: implies state mutation | Do not import in domain skeleton |
| event_ledger | No | No | No | Yes | High: implies event commitment | Do not import in domain skeleton |
| rng_interface | No | No | No | Yes | Medium: implies resolution computation | Do not import until RT-009 integration |
| table_oracle | No | No | No | Yes | Medium: implies resolution computation | Do not import until RT-009 integration |
| validation_pipeline | No | Yes (future) | No | Partially | Medium: premature integration | Future RT-011 integration point; not PR-1A scope |
| hidden_information | No | No (not yet) | No | Yes | High: implies info partition enforcement | Do not import until RT-005 integration |
| context_projection | No | No | No | Yes | High: implies context compilation | Do not import in domain skeleton |
| persistence_boundary | No | No | No | Yes | High: implies durable persistence | Do not import in domain skeleton |
| replay_audit | No | No | No | Yes | Medium: implies replay verification | Do not import in domain skeleton |
| runtime_trace | No | No (future) | No | Partially | Low: trace is observational | Future integration point; not PR-1A scope |

**Summary:** PR-1A imports only `command_envelope` (for `CommandEnvelope` type and `validate_command_envelope`). Action legality also imports `COMMAND_LIFECYCLE_STAGES` from `command_lifecycle` (intra-domain, appropriate). No premature kernel consumption detected.

---

## 9. Corpus-scale pressure review

Review of whether PR-1A's skeleton can survive donor command pressure from 200-400 sources.

| Command category | PR-1A handling | Current skeleton sufficient | Future owner |
|---|---|---|---|
| Attack/action/maneuver commands | Lifecycle: classifies through stages; Legality: `legal`/`illegal`/`blocked_by_*` decisions | Yes — classification only, no resolution | RT-002 (resource math), RT-003 (combat) |
| Spell/power/technique/ability commands | Same classification path; `blocked_by_resource_precheck` for cost gates | Yes — skeleton does not compute costs | RT-002, RT-004 (ability/effect) |
| Inventory/equipment/use-item commands | Same classification path; `blocked_by_resource_precheck` or `blocked_by_scope` | Yes — skeleton does not mutate inventory | RT-010 (inventory/item/vehicle) |
| Movement/exploration/travel commands | Same classification path; `blocked_by_scope` or `blocked_by_timing` | Yes — skeleton does not evaluate map/position state | Future state projection service |
| Social/faction/relationship commands | Same classification path; may use `requires_confirmation` | Yes — skeleton does not evaluate social state | RT-007 (social/faction) |
| Investigation/clue/mission commands | Same classification path; `blocked_by_hidden_information` for secret-dependent actions | Yes — skeleton does not reveal hidden info | RT-005 (hidden info), RT-006 (mission/clue) |
| Crafting/salvage/requisition commands | Same classification path; `blocked_by_resource_precheck` | Yes — skeleton does not compute resource availability | RT-002, RT-010 |
| Vehicle/ship/mech/platform commands | Same classification path; `blocked_by_scope` for platform-specific rules | Yes — skeleton does not evaluate platform state | RT-010 |
| Companion/summon commands | Same classification path; `blocked_by_resource_precheck` or `blocked_by_scope` | Yes — skeleton does not evaluate summoning rules | RT-004, RT-002 |
| Downtime/domain/campaign commands | Same classification path; `blocked_by_timing` for out-of-phase actions | Yes — skeleton does not evaluate campaign phase | Future campaign service |
| Meta-actions and illegal commands | `illegal` or `unsupported_command_type` decisions | Yes — structural rejection without evaluation | RT-001 |
| Ambiguous natural language commands | `requires_more_information` decision (must-not-proceed) | Yes — skeleton quarantines ambiguity without parsing | Future model evaluation (interpretation only, not authority) |
| Commands that try to reveal hidden information | `blocked_by_hidden_information` decision (must-not-proceed) | Yes — structural block; does not evaluate what is hidden | RT-005 |
| Commands that try to bypass costs | `blocked_by_resource_precheck` decision | Yes — structural block; does not evaluate actual costs | RT-002 |
| Commands relying on donor-specific action economies | `unsupported_command_type` or `quarantined_for_validation` | Yes — skeleton routes to quarantine without inventing Astra equivalents | RT-012 (D-series promotion) |
| Commands with source-local rules not yet canonized | `quarantined_for_validation` decision | Yes — quarantine preserves command for future doctrine review | RT-012 |

**Summary:** The skeleton's classification-only posture survives corpus-scale pressure because it never resolves, computes, or commits — it only classifies and routes. All resolution belongs to future services.

---

## 10. Risk review

| Risk | Affected RT owners | Mitigation | Future test family | PR-1C required |
|---|---|---|---|---|
| Command lifecycle becomes command execution | RT-001 | Skeleton has no execute/run/commit/mutate/apply methods; forbidden-method test exists | Behavioral test: lifecycle service must not produce side effects | No |
| Action legality becomes domain rules engine too early | RT-001, RT-002, RT-003, RT-004 | Skeleton creates immutable result objects only; no rule evaluation logic exists | Behavioral test: legality service must not inspect payload semantics | No |
| Guardrail relaxation allows unauthorized domain modules | RT-001, RT-011 | Guardrail tests check file absence for all unauthorized modules; PR-1B adds additional checks | File-absence guardrail tests (already comprehensive) | No |
| Hidden information leaks through block reasons | RT-005 | `hidden_info_safe` flag exists on `LegalityBlockReason`; no enforcement engine yet | Future: block reason must not contain hidden-info-unsafe content in player-visible responses | No — flag is structural marker; enforcement belongs to RT-005 |
| Resource/cost math embedded before RT-002 | RT-002 | `blocked_by_resource_precheck` is a classification decision only; no cost computation exists | Future: ensure resource precheck never calculates costs in legality skeleton | No |
| Combat assumptions leak into generic legality | RT-003 | No combat-specific logic exists in skeleton; decision categories are domain-agnostic | Future: ensure combat-specific decisions are in RT-003, not RT-001 | No |
| Donor action economy becomes Astra baseline | RT-012 | `unsupported_command_type` and `quarantined_for_validation` route donor-specific commands without canonizing them | Future: D-series promotion tests must verify quarantine-before-canon | No |
| Model output becomes de facto legality authority | RT-001, RT-005 | No model integration exists; skeleton is fully deterministic | Future: model evaluation must be advisory, never authoritative for legality | No |
| Transaction preview treated as event commitment | RT-001, RT-002 | No transaction preview creation exists in skeleton; `accepted_for_transaction_planning` is a classification stage only | Future: transaction preview must be read-only preview, not commitment | No |
| Validation becomes decorative | RT-011 | `validate_command_lifecycle_result` and `validate_action_legality_result` perform real structural checks | Future: validation pipeline integration must enforce validation-before-commit | No |
| State mutated during precheck | RT-001, RT-002 | No state access exists in skeleton; all objects are frozen dataclasses | Future: ensure precheck services are purely read-only | No |
| Ambiguous commands over-normalized instead of quarantined | RT-001 | `requires_more_information` is must-not-proceed; `quarantined_for_validation` routes to review | Future: adversarial command test corpus must include ambiguous commands | No |
| Unsupported donor commands get fake Astra certainty | RT-012 | `unsupported_command_type` explicitly marks commands as unrecognized | Future: unsupported commands must not receive fabricated Astra mappings | No |
| Future state store bypasses command lifecycle | RT-001, RT-002 | Skeleton defines lifecycle as prerequisite path; no bypass exists yet | Future: state store must require lifecycle completion before accepting mutations | No |

**Summary:** No blockers found. All risks are structural awareness items for future services. The skeleton's immutable/classification-only posture mitigates all identified risks at the current stage.

---

## 11. Required future hardening ledger

| Hardening item | Current status | Risk level | Required before PR-2 | Future owner | Recommended PR |
|---|---|---|---|---|---|
| Terminal stage/status consistency | No cross-validation | Low | No | RT-001 | PR-1C or later |
| Action legality preview consistency | May-proceed auto-derived correctly; no distinction between legal and requires_confirmation previews | Low | No | RT-001 | Future transaction preview integration |
| Hidden-info-safe block reasons | Flag exists; no enforcement engine | Medium | No | RT-005 | RT-005 implementation PR |
| Dependency declaration normalization | Action legality uses typed declarations; lifecycle uses string-based | Low | No | RT-001 | PR-1C or later |
| Validation result integration | `validation_id` field exists but no pipeline integration | Low | No | RT-011 | RT-011 implementation PR |
| Runtime trace integration | No trace emission from skeleton | Low | No | RT-001 | Future trace integration PR |
| Transaction preview handoff | `accepted_for_transaction_planning` stage exists but no handoff contract | Low | No | RT-001, RT-002 | PR-2 planning should define handoff |
| State projection handoff | No state projection dependency in skeleton | Low | No | RT-001, RT-002 | PR-2 planning should define handoff |
| Adversarial command tests | No adversarial command test corpus | Medium | No | RT-001, RT-011 | Future adversarial test PR |
| Donor action vocabulary mapping pressure | `unsupported_command_type` and `quarantined_for_validation` exist but no vocabulary mapping | Low | No | RT-012 | D-series promotion PR |
| Command lifecycle/result schema registration | No schema registration with kernel schema_registry | Low | No | RT-001, RT-011 | Future schema registration PR |

**Summary:** No items are required before PR-2 (state store/state projection planning). All hardening items are either low-risk structural improvements or belong to future service owners.

---

## 12. Gate finding

```yaml
gate_finding:
  command_lifecycle_action_legality_skeleton_review_complete: true
  pr_1a_scope_confirmed: true
  guardrail_transition_safe: true
  ready_for_runtime_domain_pr_2_state_store_state_projection_plan: true
  requires_pr_1c_hardening_before_pr_2: false
  domain_code_authorized_by_this_pr: false
  state_store_authorized_by_this_pr: false
  state_projection_authorized_by_this_pr: false
  transaction_lifecycle_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-2 state store and state projection service plan
  next_step_status: planning_only
```

**Rationale:** PR-1A stayed strictly within skeleton-only scope. No blockers, no scope violations, no premature kernel consumption. The guardrail transition is safe. The command lifecycle and action legality skeletons are stable dependencies for future domain services. PR-2 planning can proceed.

---

## 13. Recommended next PR

**Recommended:** RUNTIME-DOMAIN-PR-2: State Store and State Projection Service Plan

PR-2 should be planning-only. It should define:
- State store ownership (RT-002 primary, RT-001 dependency)
- State projection ownership (RT-001, RT-002, RT-005 dependencies)
- Kernel interface consumption plan (state_delta, event_ledger, persistence_boundary)
- Command lifecycle handoff contract (how `accepted_for_transaction_planning` feeds state store)
- Action legality dependency integration (how state projection feeds legality precheck)
- Transaction preview contract (read-only preview before commitment)
- Hidden information partition boundary for state projection (RT-005)
- Guardrail and test requirements for state store skeleton

PR-2 must not implement state store, state projection, transaction lifecycle, event commitment, or any other runtime code.

---

## 14. Non-implementation reaffirmation

This PR adds no:

- runtime code
- domain-service code
- command lifecycle implementation changes
- action legality implementation changes
- command execution
- command parser
- state store
- state projection
- state mutation
- transaction lifecycle
- event commitment
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
- database schema
- durable persistence
- training data
- donor-content audit
- pilot conversion authorization
- sourcebook inclusion authorization
- canon promotion

---

## 15. Classification block

```yaml
runtime_domain_pr_1b:
  review_id: RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001
  artifact_type: command_lifecycle_action_legality_skeleton_review_gate
  implementation_status: non_executable_review_gate
  derives_from:
    - RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001
    - RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001
    - RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001
    - RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001
    - RT-001
    - RT-011
  reviews_first_domain_package_creation: true
  reviews_command_lifecycle_skeleton: true
  reviews_action_legality_skeleton: true
  reviews_guardrail_transition: true
  reviews_kernel_dependency_usage: true
  reviews_corpus_scale_command_pressure: true
  defines_future_hardening_ledger: true
  authorizes_code_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_command_parser_by_this_pr: false
  authorizes_state_store_by_this_pr: false
  authorizes_state_projection_by_this_pr: false
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
  next_allowed_step: RUNTIME-DOMAIN-PR-2 state store and state projection service plan, pending review
```

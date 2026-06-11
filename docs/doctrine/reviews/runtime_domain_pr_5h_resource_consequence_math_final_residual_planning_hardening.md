# RUNTIME-DOMAIN-PR-5H: Resource and Consequence Math Final Residual Planning Hardening

**Artifact ID:** RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001

---

## 1. Purpose, status, sources, and precedence

### Purpose

PR-5H is a planning-only doctrine artifact. It follows PR-5G (merged as PR #277), which reviewed PR-5F and identified eight material defects that must be closed before PR-5A (skeleton implementation) can proceed. PR-5H closes all eight defects through planning contracts only. No code is authorized.

### Status

- **Planning-only.** No implementation, no runtime code, no domain code.
- **Follows PR-5G** (merged as PR #277).
- **PR-5A remains blocked.** PR-5A (skeleton implementation) is not authorized by this artifact.
- **Authorizes exactly one next step:** PR-5I, a final residual hardening review gate.
- **No implementation authority.** This artifact grants no implementation or runtime authority. No resource calculation, no affordability execution, no settlement execution, no state mutation, no event commitment, no persistence, no RNG execution, no conversion, no model integration, no live-play behavior, no canon promotion.

### Source ledger

This artifact draws from and is governed by the following sources:

| Source artifact ID | Role |
|---|---|
| `RUNTIME-DOMAIN-PR-5G-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-REVIEW-001` | Review of PR-5F, identified 8 material defects (PR #277) |
| `RUNTIME-DOMAIN-PR-5F-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-001` | Third hardening pass |
| `RUNTIME-DOMAIN-PR-5E-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-REVIEW-001` | Review of PR-5D |
| `RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001` | Second hardening pass |
| `RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001` | Review of PR-5B |
| `RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001` | First hardening pass |
| `RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001` | Original planning artifact |
| `RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001` | Validation integration review |
| `RT002_resource_consequence_math_owner_specification.md` | Domain authority |
| `src/astra_runtime/domain/validation_integration.py` | Validation integration skeleton |
| `src/astra_runtime/domain/transaction_lifecycle.py` | Transaction lifecycle skeleton |
| `src/astra_runtime/domain/event_commitment.py` | Event commitment skeleton |
| Current domain and kernel skeletons | Structural reference |
| `docs/doctrine/astra_doctrine_registry_v0_1.yaml` | Registry reference |
| `docs/decisions/current_decisions_log.md` | Decisions log |

### Precedence rule

1. **PR-5H replaces earlier contracts only where it explicitly says so.**
2. PR-5F overrides PR-5D only where PR-5F explicitly replaced a contract.
3. PR-5D overrides PR-5B only where PR-5D explicitly replaced a contract.
4. All earlier unaffected contracts remain inherited.

Effective precedence chain: **PR-5H > PR-5F > PR-5D > PR-5B** where explicitly replaced.

### Recommended next gate

**RUNTIME-DOMAIN-PR-5I: Resource and Consequence Math Final Residual Hardening Review Gate**

PR-5I must review PR-5H before PR-5A is authorized. PR-5H selects exactly one next step.

---

## 2. Backend-first invariant

The following invariants are restated and reaffirmed:

- **The LLM is not the game engine.** LLMs propose; the backend validates and commits. LLMs never mutate state.
- **References are not calculations.** A reference to a resource, quantity, or cost is a structural pointer, not an executed computation.
- **Results are not state.** A `ResourceMathResult` records a planning-stage evaluation outcome. It is not game state, not a ledger entry, not a committed transaction.
- **Settlement proposals are not transactions.** A `SettlementProposal` is a validated request for a future state change. It is not a committed state mutation.
- **`validation_ready` is not `validation_passed`.** Structural readiness for validation does not imply that validation has been performed or that it succeeded.
- **Donor text, narration, generated content, and source-local constructs cannot grant resource authority.** Resource authority derives from doctrine, not from donor material or LLM output.
- **Runtime validation cannot promote canon.** Validation enforces existing contracts. It does not create new doctrine or promote constructs to canon status.

PR-5H authorizes no resource calculation, no affordability execution, no settlement execution, no state mutation, no event commitment, no persistence, no RNG execution, no conversion, no model integration, no live-play behavior, and no canon promotion.

---

## 3. Consolidated effective contract matrix

This section publishes one authoritative matrix restating the final effective contract for all ten shapes after PR-5B, PR-5D, PR-5F, and PR-5H precedence. Every field is listed with its type, default, and governing constant set where applicable.

### ResourceMathSubjectReference

| Field | Type | Default | Required | Governed by |
|---|---|---|---|---|
| `subject_binding_id` | `str` | -- | Yes | -- |
| `subject_type` | `str` | -- | Yes | `RESOURCE_MATH_SUBJECT_TYPES` |
| `subject_ref_id` | `str` | -- | Yes | -- |
| `subject_role` | `str` | -- | Yes | `RESOURCE_MATH_SUBJECT_ROLES` |
| `owner_domain` | `str` | -- | Yes | `RESOURCE_MATH_OWNER_DOMAINS` |
| `visibility_policy` | `str` | `"public"` | No | `VISIBILITY_POLICIES` |
| `provenance_refs` | `tuple[str, ...]` | `()` | No | -- |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | No | -- |

**Binding dependency:** Exactly one required/satisfied `subject_ref` dependency per `subject_ref_id`. The dependency must have `dependency_type="subject_ref"`, `reference_id` matching `subject_ref_id`, `required=True`, and `satisfied=True`.

### ResourceReference

| Field | Type | Default | Required | Governed by |
|---|---|---|---|---|
| `resource_ref_id` | `str` | -- | Yes | -- |
| `subject_binding_id` | `str` | -- | Yes | -- |
| `resource_family` | `str` | -- | Yes | `RESOURCE_FAMILIES` |
| `resource_key` | `str` | -- | Yes | -- |
| `source_label` | `str \| None` | `None` | No | -- |
| `source_aliases` | `tuple[str, ...]` | `()` | No | -- |
| `owner_domain` | `str` | -- | Yes | `RESOURCE_MATH_OWNER_DOMAINS` |
| `visibility_policy` | `str` | `"public"` | No | `VISIBILITY_POLICIES` |
| `unit_ref_id` | `str \| None` | `None` | No | -- |
| `dimension_ref_id` | `str \| None` | `None` | No | -- |
| `provenance_refs` | `tuple[str, ...]` | `()` | No | -- |
| `source_local` | `bool` | `False` | No | -- |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | No | -- |

**Binding dependencies:**

- Non-None `unit_ref_id` requires exactly one required/satisfied `unit_ref` dependency with `reference_id` matching `unit_ref_id`.
- Non-None `dimension_ref_id` requires exactly one required/satisfied `dimension_ref` dependency with `reference_id` matching `dimension_ref_id`.

### QuantitySpecification

| Field | Type | Default | Required | Governed by |
|---|---|---|---|---|
| `quantity_id` | `str` | -- | Yes | -- |
| `representation_kind` | `str` | -- | Yes | `QUANTITY_REPRESENTATION_KINDS` |
| `magnitude_text` | `str \| None` | `None` | No | -- |
| `source_literal` | `str \| None` | `None` | No | Source-literal contract (Section 9) |
| `precision` | `int \| None` | `None` | No | -- |
| `scale` | `int \| None` | `None` | No | -- |
| `unit_ref_id` | `str \| None` | `None` | No | -- |
| `dimension_ref_id` | `str \| None` | `None` | No | -- |
| `conversion_policy` | `str` | `"no_conversion"` | No | `CONVERSION_POLICIES` |
| `rounding_policy` | `str` | `"no_rounding"` | No | `ROUNDING_POLICIES` |
| `negative_value_policy` | `str` | `"negative_values_forbidden"` | No | `QUANTITY_NEGATIVE_VALUE_POLICIES` |
| `visibility_policy` | `str` | `"public"` | No | `VISIBILITY_POLICIES` |
| `provenance_refs` | `tuple[str, ...]` | `()` | No | -- |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | No | -- |

**PR-5F correction applied:** `precision: int | None = None` (corrected from `str`).

### ResourceMathDependency

| Field | Type | Default | Required | Governed by |
|---|---|---|---|---|
| `dependency_id` | `str` | -- | Yes | -- |
| `dependency_type` | `str` | -- | Yes | `RESOURCE_MATH_DEPENDENCY_TYPES` |
| `reference_id` | `str` | -- | Yes | -- |
| `owner_domain` | `str` | -- | Yes | `RESOURCE_MATH_OWNER_DOMAINS` |
| `required` | `bool` | `True` | No | -- |
| `satisfied` | `bool` | `False` | No | -- |
| `hidden_info_safe` | `bool` | `True` | No | -- |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | No | -- |

### CostTerm

| Field | Type | Default | Required | Governed by |
|---|---|---|---|---|
| `term_id` | `str` | -- | Yes | -- |
| `subject_binding_id` | `str` | -- | Yes | -- |
| `resource_ref_id` | `str \| None` | `None` | No | -- |
| `quantity_id` | `str \| None` | `None` | No | -- |
| `cost_family` | `str` | -- | Yes | `COST_FAMILIES` |
| `timing_policy` | `str` | `"blocked_pending_validation"` | No | `COST_TIMING_POLICIES` |
| `outcome_policy` | `str` | `"validation_blocked"` | No | `COST_OUTCOME_POLICIES` |
| `visibility_policy` | `str` | `"public"` | No | `VISIBILITY_POLICIES` |
| `owner_domain` | `str` | -- | Yes | `RESOURCE_MATH_OWNER_DOMAINS` |
| `value_mode` | `str` | -- | Yes | `RESOURCE_TERM_VALUE_MODES` (PR-5F) |
| `policy_route` | `str \| None` | `None` | No | `RESOURCE_TERM_POLICY_ROUTES` (PR-5F) |
| `dependency_ids` | `tuple[str, ...]` | `()` | No | -- |
| `provenance_refs` | `tuple[str, ...]` | `()` | No | -- |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | No | -- |

### ConsequenceTerm

| Field | Type | Default | Required | Governed by |
|---|---|---|---|---|
| `consequence_id` | `str` | -- | Yes | -- |
| `subject_binding_id` | `str` | -- | Yes | -- |
| `resource_ref_id` | `str \| None` | `None` | No | -- |
| `quantity_id` | `str \| None` | `None` | No | -- |
| `consequence_family` | `str` | -- | Yes | `CONSEQUENCE_FAMILIES` |
| `timing_policy` | `str` | `"blocked_pending_validation"` | No | `COST_TIMING_POLICIES` |
| `outcome_policy` | `str` | `"validation_blocked"` | No | `COST_OUTCOME_POLICIES` |
| `visibility_policy` | `str` | `"public"` | No | `VISIBILITY_POLICIES` |
| `owner_domain` | `str` | -- | Yes | `RESOURCE_MATH_OWNER_DOMAINS` |
| `value_mode` | `str` | -- | Yes | `RESOURCE_TERM_VALUE_MODES` (PR-5F) |
| `policy_route` | `str \| None` | `None` | No | `RESOURCE_TERM_POLICY_ROUTES` (PR-5F) |
| `dependency_ids` | `tuple[str, ...]` | `()` | No | -- |
| `provenance_refs` | `tuple[str, ...]` | `()` | No | -- |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | No | -- |

### CostBundle

| Field | Type | Default | Required | Governed by |
|---|---|---|---|---|
| `bundle_id` | `str` | -- | Yes | -- |
| `term_ids` | `tuple[str, ...]` | -- | Yes (non-empty) | -- |
| `atomicity_policy` | `str` | `"all_or_nothing_requested"` | No | `ATOMICITY_POLICIES` |
| `ordering_policy` | `str` | `"unordered_terms"` | No | `ORDERING_POLICIES` |
| `partial_settlement_policy` | `str` | `"no_partial_settlement"` | No | `PARTIAL_SETTLEMENT_POLICIES` |
| `minimum_required_terms` | `int \| None` | `None` | No | -- |
| `maximum_allowed_terms` | `int \| None` | `None` | No | -- |
| `alternative_groups` | `tuple[tuple[str, tuple[str, ...]], ...]` | `()` | No | -- |
| `visibility_policy` | `str` | `"public"` | No | `VISIBILITY_POLICIES` |
| `owner_domain` | `str` | -- | Yes | `RESOURCE_MATH_OWNER_DOMAINS` |
| `dependency_ids` | `tuple[str, ...]` | `()` | No | -- |
| `provenance_refs` | `tuple[str, ...]` | `()` | No | -- |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | No | -- |

### ResourceMathRequest

| Field | Type | Default | Required | Governed by |
|---|---|---|---|---|
| `request_id` | `str` | -- | Yes | -- |
| `command_ref_id` | `str \| None` | `None` | No | -- |
| `action_legality_ref_id` | `str \| None` | `None` | No | -- |
| `subject_refs` | `tuple[ResourceMathSubjectReference, ...]` | -- | Yes (non-empty) | -- |
| `state_projection_ref_ids` | `tuple[str, ...]` | `()` | No | -- |
| `resource_refs` | `tuple[ResourceReference, ...]` | `()` | No | -- |
| `quantity_specs` | `tuple[QuantitySpecification, ...]` | `()` | No | -- |
| `cost_terms` | `tuple[CostTerm, ...]` | `()` | No | -- |
| `cost_bundles` | `tuple[CostBundle, ...]` | `()` | No | -- |
| `consequence_terms` | `tuple[ConsequenceTerm, ...]` | `()` | No | -- |
| `dependencies` | `tuple[ResourceMathDependency, ...]` | `()` | No | -- |
| `trace_ref_id` | `str` | -- | Yes | -- |
| `provenance_refs` | `tuple[str, ...]` | `()` | No | -- |
| `owner_handoff_ref_ids` | `tuple[str, ...]` | `()` | No | -- |
| `validation_request_ref_id` | `str \| None` | `None` | No | -- |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | No | -- |

All false-only fields default `False`.

### ResourceMathResult

| Field | Type | Default | Required | Governed by |
|---|---|---|---|---|
| `result_id` | `str` | -- | Yes | -- |
| `request_id` | `str` | -- | Yes | -- |
| `stage` | `str` | -- | Yes | `RESOURCE_MATH_STAGES` |
| `decision` | `str` | -- | Yes | `RESOURCE_MATH_DECISIONS` |
| `blocking` | `bool` | -- | Yes | -- |
| `quarantined` | `bool` | `False` | No | -- |
| `escalated` | `bool` | `False` | No | -- |
| `diagnostics` | `tuple[str, ...]` | `()` | No | -- |
| `normalized_reference_ids` | `tuple[str, ...]` | `()` | No | -- |
| `referenced_subject_binding_ids` | `tuple[str, ...]` | `()` | No | (PR-5F) |
| `referenced_resource_ref_ids` | `tuple[str, ...]` | `()` | No | (PR-5F) |
| `referenced_quantity_ids` | `tuple[str, ...]` | `()` | No | (PR-5F) |
| `referenced_cost_term_ids` | `tuple[str, ...]` | `()` | No | (PR-5F) |
| `referenced_cost_bundle_ids` | `tuple[str, ...]` | `()` | No | (PR-5F) |
| `referenced_consequence_term_ids` | `tuple[str, ...]` | `()` | No | (PR-5F) |
| `referenced_dependency_ids` | `tuple[str, ...]` | `()` | No | (PR-5F) |
| `dependencies` | `tuple[ResourceMathDependency, ...]` | `()` | No | -- |
| `trace_ref_id` | `str` | -- | Yes | -- |
| `validation_request_ref_id` | `str \| None` | `None` | No | -- |
| `validation_result_ref_id` | `str \| None` | `None` | No | -- |
| `validation_decision` | `str \| None` | `None` | No | -- |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | No | -- |

All false-only fields default `False`.

### SettlementProposal

| Field | Type | Default | Required | Governed by |
|---|---|---|---|---|
| `proposal_id` | `str` | -- | Yes | -- |
| `result_id` | `str` | -- | Yes | -- |
| `proposed_state_delta_refs` | `tuple[str, ...]` | -- | Yes (non-empty) | -- |
| `validation_result_ref_id` | `str` | -- | Yes | -- |
| `validation_decision` | `str` | -- | Yes, must equal `"validation_passed"` | -- |
| `dependencies` | `tuple[ResourceMathDependency, ...]` | `()` | No | -- |
| `trace_ref_id` | `str` | -- | Yes | -- |
| `visibility_policy` | `str` | `"public"` | No | `VISIBILITY_POLICIES` |
| `rollback_accounting_refs` | `tuple[str, ...]` | `()` | No | -- |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | No | -- |

All false-only fields default `False`.

**PR-5H correction:** SettlementProposal validation receives both the supplied result AND the original request. Direct aggregate architecture; no certificate object.

---

## 4. Consolidated controlled constants

This section lists every effective controlled constant set with all members. No inherited value is silently removed. The `precision` type correction from `str` to `int | None` (PR-5F) is noted in the QuantitySpecification shape above.

### RESOURCE_MATH_STAGES (14 values, from PR-5B)

1. `refs_declared`
2. `quantities_declared`
3. `costs_declared`
4. `consequences_declared`
5. `bundles_declared`
6. `policy_refs_declared`
7. `source_local_refs_declared`
8. `dependencies_declared`
9. `validation_refs_declared`
10. `blocked_pending_owner_handoff`
11. `blocked_missing_dependency`
12. `blocked_hidden_information`
13. `quarantined_for_review`
14. `escalated_to_doctrine`

### RESOURCE_MATH_DECISIONS (10 values, from PR-5B)

1. `accepted_for_planning`
2. `normalized_for_planning`
3. `source_local_retained`
4. `blocked_incompatible_policy`
5. `blocked_missing_dependency`
6. `blocked_hidden_information`
7. `requires_owner_handoff`
8. `quarantined_for_review`
9. `escalated_to_doctrine`
10. `validation_blocked`

### RESOURCE_FAMILIES (18 values, from PR-5B)

1. `currency`
2. `hit_points`
3. `spell_slots`
4. `ability_uses`
5. `ammunition`
6. `rations`
7. `fuel`
8. `cargo_capacity`
9. `crew_capacity`
10. `morale`
11. `reputation`
12. `influence`
13. `experience_points`
14. `action_points`
15. `movement_points`
16. `fate_points`
17. `narrative_currency`
18. `source_local_resource`

### COST_FAMILIES (22 values, from PR-5B, including validation_blocked)

1. `resource_spend`
2. `resource_sacrifice`
3. `resource_lock`
4. `resource_transfer`
5. `resource_consume`
6. `action_cost`
7. `movement_cost`
8. `time_cost`
9. `slot_cost`
10. `opportunity_cost`
11. `risk_cost`
12. `conditional_cost`
13. `deferred_cost`
14. `recurring_cost`
15. `compound_cost`
16. `policy_only_cost`
17. `source_local_cost`
18. `quarantine_cost`
19. `escalation_cost`
20. `owner_handoff_cost`
21. `hidden_information_cost`
22. `validation_blocked`

### CONSEQUENCE_FAMILIES (21 values, from PR-5B)

1. `resource_gain`
2. `resource_loss`
3. `resource_transform`
4. `resource_transfer`
5. `resource_unlock`
6. `status_apply`
7. `status_remove`
8. `condition_apply`
9. `condition_remove`
10. `position_change`
11. `narrative_consequence`
12. `deferred_consequence`
13. `recurring_consequence`
14. `conditional_consequence`
15. `compound_consequence`
16. `policy_only_consequence`
17. `source_local_consequence`
18. `quarantine_consequence`
19. `escalation_consequence`
20. `owner_handoff_consequence`
21. `hidden_information_consequence`

### COST_TIMING_POLICIES (12 values, from PR-5B)

1. `blocked_pending_validation`
2. `immediate_on_declaration`
3. `deferred_until_settlement`
4. `deferred_until_event_commitment`
5. `deferred_until_owner_handoff`
6. `recurring_per_turn`
7. `recurring_per_round`
8. `recurring_per_session`
9. `conditional_on_trigger`
10. `conditional_on_validation`
11. `source_local_timing`
12. `quarantine_timing`

### COST_OUTCOME_POLICIES (11 values, from PR-5B)

1. `success`
2. `failure`
3. `partial_success`
4. `cancelled`
5. `interrupted`
6. `invalid`
7. `validation_blocked`
8. `owner_blocked`
9. `quarantined`
10. `escalated`
11. `rollback_required`

### QUANTITY_KINDS (18 values, from PR-5B)

1. `count`
2. `pool_amount`
3. `delta`
4. `ratio`
5. `percentage`
6. `duration`
7. `interval`
8. `threshold`
9. `capacity`
10. `rank`
11. `tier`
12. `charge_count`
13. `currency_amount`
14. `material_amount`
15. `durability_amount`
16. `debt_amount`
17. `source_literal_quantity`
18. `unknown_pending_review`

### QUANTITY_REPRESENTATION_KINDS (6 values)

1. `integer_exact`
2. `decimal_exact`
3. `fraction_exact`
4. `fixed_point_scaled`
5. `source_literal_only`
6. `blocked_pending_numeric_choice`

### CONVERSION_POLICIES (6 values)

1. `no_conversion`
2. `exact_conversion`
3. `table_driven_conversion`
4. `doctrine_approved_conversion`
5. `source_local_conversion`
6. `escalation_required`

### ROUNDING_POLICIES (9 values)

1. `no_rounding`
2. `round_down`
3. `round_up`
4. `round_nearest`
5. `round_toward_zero`
6. `round_away_from_zero`
7. `tie_to_even`
8. `tie_away_from_zero`
9. `blocked_pending_rounding_choice`

### VISIBILITY_POLICIES (7 values)

1. `public`
2. `actor_visible`
3. `narrator_only`
4. `hidden`
5. `redacted`
6. `delayed_reveal`
7. `derived_only`

### ATOMICITY_POLICIES (10 values)

1. `all_or_nothing_requested`
2. `best_effort_requested`
3. `ordered_partial_allowed`
4. `unordered_partial_allowed`
5. `alternative_exactly_one`
6. `alternative_at_least_one`
7. `alternative_at_most_one`
8. `alternative_any`
9. `invalid_mixed_atomicity`
10. `blocked_pending_transaction_policy`

### ORDERING_POLICIES (5 values)

1. `unordered_terms`
2. `source_ordered_terms`
3. `dependency_ordered_terms`
4. `priority_ordered_terms`
5. `blocked_pending_ordering_policy`

### PARTIAL_SETTLEMENT_POLICIES (5 values)

1. `no_partial_settlement`
2. `partial_settlement_allowed`
3. `partial_settlement_requires_owner_review`
4. `partial_settlement_requires_validation`
5. `blocked_pending_settlement_policy`

### QUANTITY_NEGATIVE_VALUE_POLICIES (3 values)

1. `negative_values_forbidden`
2. `negative_values_allowed_by_source`
3. `negative_values_require_owner_handoff`

### RESOURCE_MATH_DEPENDENCY_TYPES (19 values, from PR-5F)

1. `command_ref`
2. `action_legality_ref`
3. `state_projection_ref`
4. `validation_request_ref`
5. `validation_result_ref`
6. `runtime_trace_ref`
7. `owner_handoff_ref`
8. `provenance_ref`
9. `rng_result_ref`
10. `table_oracle_result_ref`
11. `state_delta_ref`
12. `transaction_ref`
13. `event_commitment_ref`
14. `resource_math_request_ref`
15. `resource_math_result_ref`
16. `rollback_accounting_ref`
17. `subject_ref`
18. `unit_ref`
19. `dimension_ref`

### RESOURCE_MATH_SUBJECT_TYPES (14 values, from PR-5D)

1. `character`
2. `npc`
3. `creature`
4. `vehicle`
5. `ship`
6. `platform`
7. `faction`
8. `organization`
9. `location`
10. `item`
11. `asset`
12. `abstract_entity`
13. `generated_entity`
14. `source_local_entity`

### RESOURCE_MATH_SUBJECT_ROLES (9 values, from PR-5D)

1. `primary_subject`
2. `payer_subject`
3. `beneficiary_subject`
4. `resource_owner`
5. `affected_subject`
6. `source_subject`
7. `target_subject`
8. `authority_source`
9. `provenance_source`

### RESOURCE_MATH_OWNER_DOMAINS (14 values, from PR-5D/PR-5B)

1. `rt_001_command_lifecycle`
2. `rt_002_resource_math`
3. `rt_003_combat_hazard`
4. `rt_004_ability_effect`
5. `rt_005_hidden_information`
6. `rt_006_mission_reward`
7. `rt_007_social_faction`
8. `rt_008_generated_content`
9. `rt_009_rng_table`
10. `rt_010_inventory_asset`
11. `rt_011_validation_readiness`
12. `rt_012_promotion_boundary`
13. `source_local`
14. `doctrine_escalation`

### RESOURCE_TERM_VALUE_MODES (4 values, from PR-5F)

1. `resource_quantity`
2. `resource_reference_only`
3. `quantity_only`
4. `policy_only`

### RESOURCE_TERM_POLICY_ROUTES (3 values, from PR-5F)

1. `owner_handoff_required`
2. `quarantine_required`
3. `doctrine_escalation_required`

### Stage sets used in compatibility (from PR-5D)

**DECLARATION_PROGRESS_STAGES:**
`source_declaration_captured`, `subject_refs_bound`, `resource_refs_declared`, `quantity_specs_declared`, `terms_declared`, `bundle_structure_declared`, `policy_refs_declared`, `dependency_refs_bound`, `calculation_ready_for_review`

**SOURCE_LOCAL_STAGES:**
`source_declaration_captured`, `resource_refs_declared`, `terms_declared`, `bundle_structure_declared`, `policy_refs_declared`

**VALIDATION_BLOCK_STAGES:**
`blocked_pending_validation`

**OWNER_HANDOFF_STAGES:**
`blocked_pending_owner_handoff`

**MISSING_DEPENDENCY_STAGES:**
`dependency_refs_bound`, `blocked_pending_validation`, `blocked_pending_owner_handoff`

**POLICY_BLOCK_STAGES:**
`policy_refs_declared`

**HIDDEN_INFORMATION_BLOCK_STAGES:**
`dependency_refs_bound`, `blocked_pending_validation`

**QUARANTINE_STAGES:**
`quarantined_for_review`

**ESCALATION_STAGES:**
`escalated_to_doctrine`

---

## 5. Complete CostBundle policy surface

This section publishes the exhaustive CostBundle compatibility matrix from PR-5D section 9 with PR-5F bound corrections applied.

### CostBundle compatibility matrix

This matrix restates the PR-5D section 9 compatibility surface. Set abbreviations: `ORDERING_DECLARED_SET = {"unordered_terms", "source_ordered_terms", "dependency_ordered_terms", "priority_ordered_terms"}`, `ORDERING_ORDERED_SET = {"source_ordered_terms", "dependency_ordered_terms", "priority_ordered_terms"}`, `PARTIAL_REVIEW_SET = {"partial_settlement_requires_owner_review", "partial_settlement_requires_validation"}`, `ALTERNATIVE_ATOMICITY_SET = {"alternative_exactly_one", "alternative_at_least_one", "alternative_at_most_one", "alternative_any"}`.

| atomicity_policy | ordering_policy set | partial_settlement_policy set | alternative groups | lawful PR-5A posture |
|---|---|---|---|---|
| `all_or_nothing_requested` | `ORDERING_DECLARED_SET` | `{ "no_partial_settlement" }` | absent | valid declaration, no settlement |
| `all_or_nothing_requested` | `{ "blocked_pending_ordering_policy" }` | `{ "no_partial_settlement" }` | absent | blocking review |
| `best_effort_requested` | `ORDERING_DECLARED_SET` | `{ "partial_settlement_allowed" }` | absent | valid declaration, no settlement |
| `best_effort_requested` | `ORDERING_DECLARED_SET` | `PARTIAL_REVIEW_SET` | absent | blocking review; owner or validation route follows the partial policy |
| `best_effort_requested` | `{ "blocked_pending_ordering_policy" }` | `{ "partial_settlement_allowed", "partial_settlement_requires_owner_review", "partial_settlement_requires_validation", "blocked_pending_settlement_policy" }` | absent | blocking review |
| `ordered_partial_allowed` | `ORDERING_ORDERED_SET` | `{ "partial_settlement_allowed" }` | absent | valid declaration, no settlement |
| `ordered_partial_allowed` | `ORDERING_ORDERED_SET` | `PARTIAL_REVIEW_SET` | absent | blocking review; owner or validation route follows the partial policy |
| `ordered_partial_allowed` | `{ "blocked_pending_ordering_policy" }` | `{ "partial_settlement_allowed", "partial_settlement_requires_owner_review", "partial_settlement_requires_validation", "blocked_pending_settlement_policy" }` | absent | blocking review |
| `unordered_partial_allowed` | `{ "unordered_terms" }` | `{ "partial_settlement_allowed" }` | absent | valid declaration, no settlement |
| `unordered_partial_allowed` | `{ "unordered_terms" }` | `PARTIAL_REVIEW_SET` | absent | blocking review; owner or validation route follows the partial policy |
| `unordered_partial_allowed` | `{ "blocked_pending_ordering_policy" }` | `{ "partial_settlement_allowed", "partial_settlement_requires_owner_review", "partial_settlement_requires_validation", "blocked_pending_settlement_policy" }` | absent | blocking review |
| `alternative_exactly_one` | `ORDERING_DECLARED_SET` | `{ "no_partial_settlement" }` | present and valid | valid declaration, no alternative chosen |
| `alternative_at_least_one` | `ORDERING_DECLARED_SET` | `{ "no_partial_settlement" }` | present and valid | valid declaration, no alternative chosen |
| `alternative_at_most_one` | `ORDERING_DECLARED_SET` | `{ "no_partial_settlement" }` | present and valid | valid declaration, no alternative chosen |
| `alternative_any` | `ORDERING_DECLARED_SET` | `{ "no_partial_settlement" }` | present and valid | valid declaration, no alternative chosen |
| `ALTERNATIVE_ATOMICITY_SET` | `ORDERING_DECLARED_SET` | `{ "no_partial_settlement" }` | absent | invalid: alternative groups required |
| `ALTERNATIVE_ATOMICITY_SET` | `ORDERING_DECLARED_SET` | `{ "partial_settlement_allowed", "partial_settlement_requires_owner_review", "partial_settlement_requires_validation", "blocked_pending_settlement_policy" }` | present or absent | invalid: alternatives cannot also declare partial settlement in PR-5A |
| `invalid_mixed_atomicity` | `ORDERING_DECLARED_SET` or `{ "blocked_pending_ordering_policy" }` | `{ "no_partial_settlement", "partial_settlement_allowed", "partial_settlement_requires_owner_review", "partial_settlement_requires_validation", "blocked_pending_settlement_policy" }` | present or absent | invalid mixed atomicity |
| `blocked_pending_transaction_policy` | `ORDERING_DECLARED_SET` or `{ "blocked_pending_ordering_policy" }` | `{ "no_partial_settlement", "partial_settlement_allowed", "partial_settlement_requires_owner_review", "partial_settlement_requires_validation", "blocked_pending_settlement_policy" }` | present or absent | blocking owner/transaction-policy review |
| non-alternative atomicity | `ORDERING_DECLARED_SET` | any | overlapping groups | invalid: non-alternative atomicity cannot declare alternative groups |
| `ALTERNATIVE_ATOMICITY_SET` | `ORDERING_DECLARED_SET` | `{ "no_partial_settlement" }` | overlapping groups | invalid unless a future explicit policy authorizes overlap |

**Every combination not expressly listed above is invalid.**

### PR-5F bound rules

The following bound rules apply to `minimum_required_terms` and `maximum_allowed_terms`:

1. `bool` is invalid for bounds. Both must be `int | None`.
2. When supplied, bounds must be positive integers (> 0).
3. Each supplied bound must be `<= len(term_ids)`.
4. When both are supplied, `minimum_required_terms <= maximum_allowed_terms`.
5. `all_or_nothing_requested` permits either both bounds `None`, or both bounds equal to `len(term_ids)`.
6. No term selection or alternative selection occurs at the planning stage.
7. Alternative group IDs must be unique within a bundle.
8. Alternative group members must be unique within each group.
9. All alternative group members must resolve to IDs present in `term_ids`.
10. Overlapping alternative groups (groups sharing members) are invalid.

---

## 6. Exact dependency lifecycle and aggregate ownership

### Dependency lifecycle states

Every `ResourceMathDependency` occupies exactly one of the following five lifecycle states:

**A. Satisfied binding dependency.**
A matching dependency record exists with the correct `dependency_type` and `reference_id` for the field it binds. `required=True`, `satisfied=True`. The dependency is structurally linked to a field (e.g., `subject_ref_id`, `unit_ref_id`, `dimension_ref_id`). The field's binding contract is met. The request or result is structurally valid with respect to this dependency.

**B. Incomplete binding dependency.**
A matching dependency record exists with the correct `dependency_type` and `reference_id` for the field it binds. `required=True`, `satisfied=False`. The dependency remains structurally linked to the field. The request may be structurally valid (the record exists and is correctly typed) but is not resolution-ready. Any result whose typed scope reaches this dependency must use `blocked_missing_dependency` as its decision.

**C. Missing binding dependency.**
No matching dependency record exists for the field that requires one, or a record exists but with the wrong `dependency_type` or `reference_id`. The request aggregate is invalid. Factories and validators must reject it. No `ResourceMathResult` may be constructed for an aggregate with a missing binding dependency.

**D. Required but unsatisfied dependency.**
`required=True`, `satisfied=False`. The dependency may be field-bound (making it also state B) or may be a named dependency referenced by a scoped record (e.g., a cost term's `dependency_ids` entry). Forces `blocked_missing_dependency` as the result decision for any result whose typed scope reaches it.

**E. Advisory optional unsatisfied dependency.**
`required=False`, `satisfied=False`. Not field-bound to any structural field. Not named by any scoped record's `dependency_ids`. Not part of any typed result scope. May coexist with a non-blocking result. Can never satisfy a binding requirement. Exists for informational or provenance tracking purposes only.

### Aggregate ownership

Each dependency-carrying shape owns its dependencies for a specific purpose:

**`ResourceMathRequest.dependencies`** owns request-side and input-side bindings:
- Subject binding dependencies (`subject_ref`)
- Unit binding dependencies (`unit_ref`)
- Dimension binding dependencies (`dimension_ref`)
- Command reference dependencies (`command_ref`)
- Action legality reference dependencies (`action_legality_ref`)
- State projection reference dependencies (`state_projection_ref`)
- Provenance reference dependencies (`provenance_ref`)
- Source input dependencies (RNG result, table oracle result references: `rng_result_ref`, `table_oracle_result_ref`)
- Owner handoff reference dependencies (`owner_handoff_ref`)
- Runtime trace reference dependency (`runtime_trace_ref`)

**`ResourceMathResult.dependencies`** owns result-side and validation-side dependencies:
- Resource math request reference dependency (`resource_math_request_ref`)
- Resource math result reference dependency (`resource_math_result_ref`)
- Validation request reference dependency (`validation_request_ref`)
- Validation result reference dependency (`validation_result_ref`)
- Runtime trace reference dependency (`runtime_trace_ref`)
- Result-specific policy dependencies

**`SettlementProposal.dependencies`** owns proposal-side dependencies:
- Resource math result reference dependency (`resource_math_result_ref`)
- Validation result reference dependency (`validation_result_ref`)
- Proposed state delta reference dependencies (`state_delta_ref`)
- Rollback accounting reference dependencies (`rollback_accounting_ref`)
- Runtime trace reference dependency (`runtime_trace_ref`)
- Proposal-specific dependencies

### Uniqueness constraints

- Within any single `dependencies` tuple, `dependency_id` values must be unique.
- Within any single `dependencies` tuple, the pair `(dependency_type, reference_id)` must be unique. No two dependencies in the same aggregate may share both `dependency_type` and `reference_id`.

### Hidden-information safety distinction

`hidden_info_safe=False` is not the same as unsatisfied. A dependency may be `required=True`, `satisfied=True`, but `hidden_info_safe=False`. In this case, the dependency is structurally complete but carries hidden-information risk. A satisfied but unsafe scoped dependency follows the hidden-information blocker route (precedence 3 in Section 8), not the missing-dependency route.

---

## 7. Typed result-scope cardinality

The seven typed result-scope tuples from PR-5F are:

1. `referenced_subject_binding_ids`
2. `referenced_resource_ref_ids`
3. `referenced_quantity_ids`
4. `referenced_cost_term_ids`
5. `referenced_cost_bundle_ids`
6. `referenced_consequence_term_ids`
7. `referenced_dependency_ids`

### Cardinality rules

1. **Entirely empty typed result scope is invalid for every `ResourceMathResult`.** A result with all seven tuples empty is structurally invalid and must be rejected by both factories and validators. No result may exist that scopes nothing.

2. **Empty tuple defaults remain lawful at the individual field level.** Any single typed scope tuple may be `()`. The constraint is on the aggregate: the combined scope across all seven tuples must be non-empty.

3. **`accepted_for_planning` and `normalized_for_planning` require at least one scoped business record.** The scoped business record must come from at least one of: `referenced_resource_ref_ids`, `referenced_quantity_ids`, `referenced_cost_term_ids`, `referenced_cost_bundle_ids`, or `referenced_consequence_term_ids`. Subject binding IDs or advisory dependencies alone are insufficient for accepted or normalized results.

4. **A blocked result must scope at least one actual blocking record or required dependency.** The blocking cause must be identifiable from the typed scope.

5. **A `blocked_missing_dependency` result may be dependency-only.** When the blocker is a request-level required-unsatisfied dependency (state D in Section 6), `referenced_dependency_ids` alone is sufficient. No business record scope is required in this specific case.

6. **Every scoped ID must resolve.** Every ID in every typed scope tuple must reference an actual record in the request or result aggregate. This applies equally to blocked, quarantined, and escalated results.

7. **A missing binding with no resolvable dependency record invalidates the request.** This is a request-level structural failure (Section 6, state C), not a result-level scope issue.

8. **Closure remains mandatory.** Bundle-to-term closure (every `term_id` in a scoped bundle must be scoped), term-to-quantity/resource/dependency closure (every `quantity_id`, `resource_ref_id`, or `dependency_id` referenced by a scoped term must be scoped), and record-to-dependency closure (every dependency referenced by a scoped record must be scoped) are all mandatory.

9. **`normalized_reference_ids` remains diagnostic only.** It does not participate in scope validation, closure checks, or cardinality requirements.

10. **Unscoped records remain ignored by that result.** However, empty scope cannot bypass policy-only terms or blocked quantities. If a policy-only term or blocked quantity exists in the request, it must be scoped by at least one result that addresses it.

---

## 8. Complete simultaneous-blocker precedence

### Structural invalidity precedes result construction

Request structural invalidity (missing binding dependencies, invalid field types, violated constant sets, failed aggregate constraints) is checked before result construction and is not represented as a `ResourceMathResult` decision. A structurally invalid request cannot produce any result. Factories and validators reject it at the request level.

### Result-route precedence table

For structurally valid requests, the following precedence table governs which result route is selected when one or more blockers are detected:

| Precedence | Route | Condition | Decision | Stage | `blocking` | `escalated` | `quarantined` |
|---|---|---|---|---|---|---|---|
| 1 | Doctrine escalation | Explicit escalation state on a scoped record, or a scoped `policy_only` term with `doctrine_escalation_required` policy route | `escalated_to_doctrine` | `escalated_to_doctrine` | `True` | `True` | `False` |
| 2 | Quarantine | Explicit quarantine state on a scoped record, or a scoped `policy_only` term with `quarantine_required` policy route | `quarantined_for_review` | `quarantined_for_review` | `True` | `False` | `True` |
| 3 | Hidden-information block | A scoped satisfied dependency or scoped record is not hidden-information safe (`hidden_info_safe=False`) | `blocked_hidden_information` | Lawful `HIDDEN_INFORMATION_BLOCK_STAGES` member | `True` | `False` | `False` |
| 4 | Missing/unsatisfied required dependency | An existing scoped required dependency has `satisfied=False` | `blocked_missing_dependency` | Lawful `MISSING_DEPENDENCY_STAGES` member | `True` | `False` | `False` |
| 5 | Blocked numeric choice | A scoped quantity uses `blocked_pending_numeric_choice` representation kind | `blocked_incompatible_policy` | `policy_refs_declared` | `True` | `False` | `False` |
| 6 | Owner handoff | A scoped quantity uses `negative_values_require_owner_handoff` negative value policy, or a scoped `policy_only` term with `owner_handoff_required` policy route | `requires_owner_handoff` | `blocked_pending_owner_handoff` | `True` | `False` | `False` |
| 7 | Source-supported negative | Lawful source-supported negative value with correct source literal and provenance contracts satisfied | Not blocking in itself | -- | -- | -- | -- |
| 8 | No blocker | Only when no blockers from precedence 1-6 are detected; check accepted/normalized/source-local against normal stage/decision matrix | Per matrix | Per matrix | Per matrix | `False` | `False` |

### Simultaneous-blocker rules

1. **When multiple blockers exist, emit the highest-precedence decision.** The result's `decision` and `stage` are set according to the highest-precedence (lowest number) blocker that applies.

2. **No lower blocker is silently lost from diagnostics.** All detected blockers, regardless of precedence, must be recorded in the result's `diagnostics` tuple. The highest-precedence blocker determines the decision; all others are preserved as diagnostic entries.

3. **Policy-only doctrine escalation, quarantine, and owner-handoff routes occupy the same precedence positions** as their non-policy-only counterparts. A `policy_only` term with `doctrine_escalation_required` is precedence 1, same as an explicit escalation state.

4. **Source-supported negative is not itself blocking** when the source literal contract (Section 9) and provenance contracts pass. A source-supported negative value with valid literal and provenance does not trigger any blocker. However:
   - Missing or unsatisfied provenance for the source-supported negative follows the missing-dependency precedence (precedence 4).
   - A malformed source literal is an aggregate validation failure, not a result route. It invalidates the request structurally.

---

## 9. Source-literal contract consistency

Every non-None `source_literal` field value, regardless of which `QuantitySpecification` carries it, regardless of `representation_kind`, and regardless of why it is supplied, obeys the following exact contract:

1. **Non-empty string.** `source_literal` must be a `str` with `len(source_literal) > 0`.
2. **One line only.** The value must not contain any line-break characters.
3. **No leading or trailing whitespace.** `source_literal == source_literal.strip()`.
4. **No CR, LF, tab, or NUL.** The value must not contain `\r` (U+000D), `\n` (U+000A), `\t` (U+0009), or `\0` (U+0000).
5. **No Unicode Cc control characters.** No character in the General Category `Cc` (control characters) is permitted.
6. **No Unicode Cs surrogate characters.** No character in the General Category `Cs` (surrogates) is permitted.
7. **Permitted characters.** Ordinary Unicode letters, numbers, punctuation, symbols, and interior spaces are allowed.
8. **Preserve exactly.** The source literal is stored and returned exactly as supplied.
9. **No normalization, parsing, tokenization, arithmetic, or evaluation.** The source literal is an opaque string. No component of the system may interpret it as a numeric expression, parse it into tokens, apply Unicode normalization, perform arithmetic on it, or evaluate it in any way.

A `source_literal` supporting `negative_values_allowed_by_source` (i.e., a source-supported negative value quantity) must obey this exact same contract. The negative-value policy does not grant any relaxation of the source-literal character contract. The literal is still opaque, still one line, still stripped, still free of control characters, and still never parsed or evaluated.

---

## 10. Proposal, result, and request validation ordering

PR-5H selects the **direct aggregate architecture**. No certificate object is introduced. No intermediate validation token, receipt, or proof object is created.

### Future signatures

```python
def create_settlement_proposal(
    *,
    request: ResourceMathRequest,
    result: ResourceMathResult,
    ...
) -> SettlementProposal:
    ...

def validate_settlement_proposal(
    proposal: SettlementProposal,
    *,
    request: ResourceMathRequest,
    result: ResourceMathResult,
) -> bool:
    ...
```

### Exact validation order

Validation proceeds in the following exact order. No step may be skipped, reordered, or short-circuited.

1. **Validate the `ResourceMathRequest` aggregate.** The request must be structurally valid: all required fields present, all constant-governed fields within their constant sets, all binding dependencies satisfied (Section 6, state A), no missing binding dependencies (Section 6, state C), all ID uniqueness constraints met, all closure constraints met, all bundle compatibility constraints met (Section 5), all quantity and source-literal contracts met (Section 9).

2. **Validate `ResourceMathResult` against that exact supplied request.** The result's `request_id` must match the supplied request's `request_id`. All typed scope IDs must resolve within the supplied request. All scope cardinality rules (Section 7) must hold. The result's decision, stage, blocking state, escalated state, and quarantined state must be consistent with the blocker-precedence table (Section 8). All result-side dependencies must be valid.

3. **Validate `SettlementProposal` against that exact result and request.** The proposal's `result_id` must match the supplied result's `result_id`. The proposal must reference the same validation result and decision. The result must be eligible for settlement (non-blocking, not quarantined, not escalated). The proposal's `proposed_state_delta_refs` must be non-empty. All false-only fields must be `False`. All proposal-side dependencies must be valid.

4. **Enforce request/result/proposal ID and typed dependency linkage.** The chain `request.request_id == result.request_id`, `result.result_id == proposal.result_id` must hold. Typed dependencies linking these objects must be present and satisfied in the appropriate dependency aggregates.

5. **Enforce proposal/result validation-result and decision equality.** `proposal.validation_result_ref_id == result.validation_result_ref_id` and `proposal.validation_decision == result.validation_decision == "validation_passed"`.

6. **Enforce result eligibility, non-blocking state, non-empty state-delta refs, false-only fields, and dependency integrity.** The result must have `blocking=False`, `quarantined=False`, `escalated=False`. The proposal's `proposed_state_delta_refs` must be non-empty. All false-only authority fields across all three aggregates must be `False`. All dependencies across all three aggregates must satisfy their lifecycle contracts (Section 6).

**No repository lookup.** Validation operates on the supplied aggregates only. There is no database query, no repository fetch, no external state lookup during validation.

**No caller-supplied boolean "already validated" shortcut.** There is no `skip_request_validation=True` parameter, no `request_already_validated` flag, no trust-the-caller bypass. Every call to `validate_settlement_proposal` performs the full validation chain.

---

## 11. Factory/validator parity

### Shared private helpers requirement

Factories and validators must share the same private helper functions for all effective contracts. No factory may implement a validation rule inline that the corresponding validator implements differently. No validator may enforce a constraint that the factory does not also enforce during construction.

### Contracts that factories and validators must enforce identically

1. **Manually constructed frozen dataclasses.** A frozen dataclass constructed via `__init__` or `object.__setattr__` bypass receives no special trust. Both factories and validators must validate the same constraints regardless of how the object was constructed.

2. **Constants and defaults.** Every constant-governed field must be validated against its constant set. Every default value must match the effective contract (Section 3). Factories must apply defaults; validators must verify them.

3. **Dependency lifecycle and aggregate ownership.** Both must enforce the five dependency lifecycle states (Section 6), aggregate ownership boundaries, uniqueness by `dependency_id`, and uniqueness by `(dependency_type, reference_id)`.

4. **Typed-scope cardinality and closure.** Both must enforce the cardinality rules (Section 7), including the non-empty aggregate scope requirement, the accepted/normalized minimum business-record scope, the blocked result scope requirement, and all closure requirements.

5. **Blocker detection and precedence.** Both must apply the same blocker-precedence table (Section 8) and produce the same decision for the same inputs.

6. **Bundle compatibility and bounds.** Both must enforce the compatibility matrix (Section 5) and the bound rules identically.

7. **Quantity lexical and source-literal rules.** Both must enforce the source-literal contract (Section 9) and all quantity representation-kind constraints identically.

8. **Result/request validation.** Both must enforce that a result's `request_id` matches its request, that typed scope IDs resolve, and that the decision/stage/blocking state is consistent.

9. **Proposal/result/request validation.** Both must enforce the full validation chain (Section 10) identically.

10. **False-only authority fields.** Both must enforce that all false-only fields are `False` on every shape that declares them.

11. **Tuple conversion and immutable metadata.** Both must ensure that all sequence fields are tuples (not lists), and that metadata is an immutable `Mapping` (not a mutable `dict`). Factories must convert; validators must reject unconverted values.

12. **Internal-only serialization.** Both must enforce that serialization uses `to_dict` only, produces defensive copies, converts tuples to lists only in returned copies, and performs no calculation during serialization.

### Factory-specific behavior

A factory may reject invalid input immediately with a descriptive error. This is permitted and expected. The factory is not required to construct an invalid object and then validate it; it may fail fast.

### Validator-specific behavior

Explicit `validate_*` functions must also reject invalid manually constructed objects. A frozen dataclass constructor is not trusted as validation. A manually constructed object that passes `__init__` without error is not assumed valid. The validator must perform the full contract check.

---

## 12. Serialization, hidden information, and owner boundaries

### Serialization contract

The following serialization rules remain effective:

1. **Internal `to_dict` only.** All shapes provide a `to_dict` method for internal serialization. This is the only serialization path.

2. **no `to_public_dict`** — there is no public-facing serialization method. RT-005 (Hidden Information) owns all projection and redaction for external consumers.

3. **Defensive copies.** Every `to_dict` call returns a new dictionary. Mutations to the returned dictionary do not affect the source object.

4. **Tuple-to-list conversion only in returned copies.** Tuple fields are converted to lists in the dictionary returned by `to_dict`. The source object's tuple fields remain tuples.

5. **No calculation during serialization.** `to_dict` performs no arithmetic, no evaluation, no formula execution, no resource calculation. It is a pure structural conversion.

6. **RT-005 owns later projection and redaction.** Any filtering, redaction, or visibility-based projection of serialized data is the responsibility of RT-005 (Hidden Information). RT-002 does not implement visibility filtering.

7. **No hidden literals, provenance, dependency details, or backend IDs exposed publicly.** The `to_dict` method is internal. Any public-facing representation must go through RT-005's projection layer.

### RT-002 ownership boundary

RT-002 (Resource and Consequence Math) owns resource references, quantity specifications, cost terms, consequence terms, cost bundles, resource math requests, resource math results, settlement proposals, subject references, and dependencies as defined in this artifact.

RT-002 does not absorb and must not implement:

- Combat or hazard logic (RT-003)
- Ability or effect logic (RT-004)
- Inventory or asset management (RT-010)
- Mission or reward logic (RT-006)
- Social or faction logic (RT-007)
- Generated content logic (RT-008)
- RNG or table oracle logic (RT-009)
- Validation readiness orchestration (RT-011)
- Promotion boundary enforcement (RT-012)
- Hidden information projection or redaction (RT-005)
- Persistence or event commitment (RT-003/transaction lifecycle/event commitment)
- Canon promotion (doctrine layer)

---

## 13. PR-5G closure ledger

| PR-5G required correction | PR-5H section | Closure status |
|---|---|---|
| One final effective contract matrix restating all inherited fields, defaults, and governed constants after PR-5B/PR-5D/PR-5F precedence | Section 3 | Closed |
| Complete inherited atomicity, ordering, and partial-settlement surface and one bundle compatibility matrix | Section 5 | Closed |
| Exact lifecycle for unsatisfied binding dependencies, missing binding dependencies, required unsatisfied dependencies, and advisory optional unsatisfied dependencies | Section 6 | Closed |
| Empty typed result scope legality and accepted/normalized minimum scope requirement | Section 7 | Closed |
| Complete simultaneous blocker-precedence table | Section 8 | Closed |
| Source-supported negative `source_literal` character contract consistency | Section 9 | Closed |
| Proposal validation prerequisite: original request or prior exact result/request validation | Section 10 | Closed |
| Factory/validator parity for edge cases and manual frozen-dataclass construction | Section 11 | Closed |

**All eight PR-5G-required corrections are closed.**

**PR-5A must remain unauthorized until PR-5I reviews this artifact.**

---

## 14. Recommended next gate

**RUNTIME-DOMAIN-PR-5I: Resource and Consequence Math Final Residual Hardening Review Gate**

PR-5I must review PR-5H and confirm that all eight PR-5G defects are properly closed, that no new defects have been introduced, and that the consolidated contracts are internally consistent. PR-5A (skeleton implementation) is not authorized until PR-5I completes.

PR-5H selects exactly one next step: PR-5I.

---

## 15. Non-implementation reaffirmation and classification block

PR-5H is a planning-hardening-only artifact. It does not authorize and must not be interpreted as authorizing:

- No `resource_consequence_math.py` module creation
- No formula implementation
- No evaluator implementation
- No calculator implementation
- No resource math engine
- No affordability checker
- No settlement executor
- No state mutator
- No event committer
- No persistence layer
- No RNG executor
- No model integration
- No conversion logic
- No canon promotion
- No live-play behavior
- No domain service implementation
- No runtime service implementation

```yaml
runtime_domain_pr_5h_classification:
  artifact_id: RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001
  artifact_type: final_residual_planning_hardening
  implementation_status: planning_only
  follows_pr_5g: true
  closes_pr_5g_required_corrections: true
  pr_5a_authorized: false
  pr_5i_required_before_pr_5a: true
  exactly_one_next_step: true
  next_step_authorized: RUNTIME-DOMAIN-PR-5I resource and consequence math final residual hardening review gate
  complete_non_implementation_boundary: true
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

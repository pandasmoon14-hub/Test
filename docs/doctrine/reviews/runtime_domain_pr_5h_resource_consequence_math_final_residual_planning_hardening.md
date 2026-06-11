# RUNTIME-DOMAIN-PR-5H: Resource and Consequence Math Final Residual Planning Hardening

## 1. Purpose, status, source ledger, and preservation rule

Artifact ID: **RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001**.

This artifact is **planning-only** for PR #278. It preserves the comprehensive PR-278 PR-5H contract and ports only valid residual corrections proposed in the parallel PR #279 review discussion. PR #279 is not merged, cherry-picked, or wholesale copied. **PR-5A remains blocked**. The sole next step is **RUNTIME-DOMAIN-PR-5I resource and consequence math final residual planning hardening review gate**.

Source ledger:

- `RUNTIME-DOMAIN-PR-5G-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-REVIEW-001`
- `RUNTIME-DOMAIN-PR-5F-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-001`
- `RUNTIME-DOMAIN-PR-5E-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-REVIEW-001`
- `RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001`
- `RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001`
- `RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001`
- `RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001`
- `RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001`
- `RT002_resource_consequence_math_owner_specification.md`

Preserved PR-278 surfaces include: complete ten-shape effective field matrix; inherited controlled constant sets and provenance; complete CostBundle compatibility matrix; five-state dependency lifecycle; dependency aggregate ownership; typed result-scope cardinality and closure; exact eight-level simultaneous blocker precedence; source-literal contract; direct request/result/proposal validation architecture; factory/validator parity; serialization and hidden-information ownership; PR-5G closure ledger; and non-implementation/PR-5I gate classification.

No runtime/domain implementation is authorized. This artifact creates no `src/` changes, no `resource_consequence_math.py`, no factories, no validators, no dataclasses, no arithmetic, no formula evaluator, no parser, no settlement executor, no state mutation, no event commitment, no persistence, no RNG/table execution, no model integration, no UI/live-play behavior, no conversion, and no canon promotion.

## 2. Backend-first invariant and authority refusals

- The LLM is not the game engine.
- Reference objects are not calculations.
- Results are not state.
- Settlement proposals are not transactions.
- `validation_ready` is not `validation_passed`.
- Donor text, source-local wording, generated text, and narrative labels cannot create resource authority.
- Runtime validation cannot promote canon.
- Every authority field in `FALSE_ONLY_AUTHORITY_FIELDS` remains false-only.
- PR-5H authorizes no calculation, affordability execution, reservation, settlement, consequence application, mutation, state-delta application, transaction execution, event commitment, event append, persistence, replay, RNG execution, table-oracle execution, model authority, live play, UI behavior, conversion, or canon promotion.

## 3. Final effective PR-5A inventory, constants, and external binding fields

PR-5A must be able to generate the future planning dataclass surface from this PR-5H contract without consulting PR-5D. Earlier PR-5 artifacts remain provenance, but this section is the effective inventory after PR-5B, PR-5D, PR-5F, PR-5G, and final PR-5H residual corrections.

### 3.1 Inherited controlled constant surfaces and provenance

The effective inherited controlled surfaces are preserved exactly as planning vocabularies, not executable enums:

- `RESOURCE_MATH_SUBJECT_TYPES = {"actor", "asset", "item", "location", "faction", "project", "scene", "system", "source_local_subject", "provenance_source"}`
- `RESOURCE_MATH_SUBJECT_ROLES = {"primary_subject", "cost_payer", "resource_holder", "consequence_target", "observer", "source_local_subject"}`
- `RESOURCE_MATH_OWNER_DOMAINS = {"RT001_command_lifecycle", "RT002_resource_consequence_math", "RT003_combat_hazard_damage_recovery", "RT004_ability_effect_skill_binding", "RT005_context_packet_hidden_information", "RT006_mission_reward_clue_routing", "RT007_npc_social_faction", "RT008_generated_content_provenance", "RT009_runtime_rng_table_oracle", "RT010_inventory_item_vehicle_asset", "RT011_validation_integration", "RT012_d_series_promotion_boundary"}`
- `VISIBILITY_POLICIES = {"public", "source_local", "internal_only", "hidden_information_guarded"}`
- `RESOURCE_MATH_DEPENDENCY_TYPES = {"command_ref", "action_legality_ref", "state_projection_ref", "validation_request_ref", "validation_result_ref", "runtime_trace_ref", "owner_handoff_ref", "provenance_ref", "rng_result_ref", "table_oracle_result_ref", "state_delta_ref", "transaction_ref", "event_commitment_ref", "resource_math_request_ref", "resource_math_result_ref", "rollback_accounting_ref", "subject_ref", "unit_ref", "dimension_ref"}`
- `QUANTITY_REPRESENTATION_KINDS = {"integer_exact", "decimal_exact", "fraction_exact", "fixed_point_scaled", "source_literal_only", "blocked_pending_numeric_choice"}`
- `NEGATIVE_VALUE_POLICIES = {"negative_values_forbidden", "negative_values_allowed_by_source", "negative_values_require_owner_handoff"}`
- `TERM_VALUE_MODES = {"explicit_quantity", "derived_quantity_pending", "policy_only", "source_literal_only", "blocked_pending_numeric_choice"}`
- `POLICY_ONLY_ROUTES = {"doctrine_escalation_required", "quarantine_required", "owner_handoff_required", "validation_review_required", "source_local_retained"}`
- `COST_BUNDLE_POLICIES = {"all_required", "any_one", "at_least_minimum", "at_most_maximum", "exactly_one", "ordered_sequence", "partial_settlement_allowed", "partial_settlement_forbidden"}`
- `VALIDATION_INTEGRATION_DECISIONS` remains owned by validation integration; PR-5H consumes it only for `validation_ready`, `validation_passed`, `validation_failed`, and related inherited decisions.

### 3.2 Complete ten-shape effective field matrix

| shape | field | annotation | default | controlled surface | invariant |
|---|---|---|---|---|---|
| `ResourceMathDependency` | `dependency_id` | `str` | required | same-request dependency id | non-empty; unique inside ResourceMathRequest.dependencies |
| `ResourceMathDependency` | `dependency_type` | `str` | required | RESOURCE_MATH_DEPENDENCY_TYPES | non-empty member |
| `ResourceMathDependency` | `reference_id` | `str` | required | external/upstream reference id | non-empty; no dereference |
| `ResourceMathDependency` | `required` | `bool` | `True` | dependency lifecycle | binding dependencies must be True; advisory may be False |
| `ResourceMathDependency` | `satisfied` | `bool` | `False` | dependency lifecycle | True complete; False incomplete/advisory per Section 6 |
| `ResourceMathDependency` | `hidden_info_safe` | `bool` | `True` | RT-005 hidden-information safety | False routes scoped results to blocked_hidden_information |
| `ResourceMathDependency` | `owner_domain` | `str \| None` | `None` | RESOURCE_MATH_OWNER_DOMAINS | required only when owner handoff route names owner domain |
| `ResourceMathDependency` | `notes` | `tuple[str, ...]` | `()` | internal notes | internal-only; no public projection |
| `ResourceMathSubjectReference` | `subject_binding_id` | `str` | required | same-aggregate subject binding id | non-empty; unique |
| `ResourceMathSubjectReference` | `subject_type` | `str` | required | RESOURCE_MATH_SUBJECT_TYPES | member |
| `ResourceMathSubjectReference` | `subject_ref_id` | `str` | required | external binding: subject_ref | exactly one matching dependency; lifecycle Section 6 |
| `ResourceMathSubjectReference` | `subject_role` | `str` | required | RESOURCE_MATH_SUBJECT_ROLES | exactly one primary_subject per request |
| `ResourceMathSubjectReference` | `owner_domain` | `str` | required | RESOURCE_MATH_OWNER_DOMAINS | member |
| `ResourceMathSubjectReference` | `visibility_policy` | `str` | `public` | VISIBILITY_POLICIES | not public-output authority |
| `ResourceMathSubjectReference` | `provenance_refs` | `tuple[str, ...]` | `()` | provenance_ref dependencies when external | unique; lifecycle Section 6 |
| `ResourceReference` | `resource_ref_id` | `str` | required | resource reference id | non-empty; no dereference |
| `ResourceReference` | `subject_binding_id` | `str` | required | same request subject binding | must resolve in ResourceMathRequest.subject_refs |
| `ResourceReference` | `resource_role` | `str` | required | RESOURCE_REFERENCE_ROLES | member |
| `ResourceReference` | `unit_ref_id` | `str \| None` | `None` | external binding: unit_ref | exactly one matching dependency when supplied; lifecycle Section 6 |
| `ResourceReference` | `dimension_ref_id` | `str \| None` | `None` | external binding: dimension_ref | exactly one matching dependency when supplied; lifecycle Section 6 |
| `ResourceReference` | `source_literal` | `str \| None` | `None` | SOURCE_LITERAL_TEXT | Section 10 character contract |
| `ResourceReference` | `provenance_refs` | `tuple[str, ...]` | `()` | provenance_ref dependencies when external | unique; lifecycle Section 6 |
| `QuantitySpecification` | `quantity_id` | `str` | required | same-request quantity id | non-empty; unique |
| `QuantitySpecification` | `representation_kind` | `str` | required | QUANTITY_REPRESENTATION_KINDS | member |
| `QuantitySpecification` | `magnitude_text` | `str \| None` | `None` | lexical quantity text | no parsing/evaluation |
| `QuantitySpecification` | `unit_ref_id` | `str \| None` | `None` | external binding: unit_ref | exactly one matching dependency when supplied; lifecycle Section 6 |
| `QuantitySpecification` | `dimension_ref_id` | `str \| None` | `None` | external binding: dimension_ref | exactly one matching dependency when supplied; lifecycle Section 6 |
| `QuantitySpecification` | `precision` | `int \| None` | `None` | precision declaration | bool rejected; decimal_exact only |
| `QuantitySpecification` | `scale` | `int \| None` | `None` | fixed-point declaration | bool rejected; fixed_point_scaled only |
| `QuantitySpecification` | `negative_value_policy` | `str` | `negative_values_forbidden` | NEGATIVE_VALUE_POLICIES | member |
| `QuantitySpecification` | `source_literal` | `str \| None` | `None` | SOURCE_LITERAL_TEXT | Section 10 character contract |
| `QuantitySpecification` | `provenance_refs` | `tuple[str, ...]` | `()` | provenance_ref dependencies when external | unique; lifecycle Section 6 |
| `CostTerm` | `term_id` | `str` | required | same-request term id | non-empty; unique among terms |
| `CostTerm` | `term_kind` | `str` | required | RESOURCE_MATH_TERM_KINDS | cost term member |
| `CostTerm` | `value_mode` | `str` | required | TERM_VALUE_MODES | member; policy_only cannot produce accepted/normalized/proposal |
| `CostTerm` | `subject_binding_id` | `str` | required | same request subject binding | must resolve |
| `CostTerm` | `resource_ref_id` | `str \| None` | `None` | same-request ResourceReference id | must resolve when supplied |
| `CostTerm` | `quantity_id` | `str \| None` | `None` | same-request QuantitySpecification id | must resolve when supplied |
| `CostTerm` | `policy_route` | `str \| None` | `None` | POLICY_ONLY_ROUTES | exact route mapping preserved |
| `CostTerm` | `dependency_refs` | `tuple[str, ...]` | `()` | ResourceMathDependency.dependency_id | each must resolve in same request |
| `CostTerm` | `source_literal` | `str \| None` | `None` | SOURCE_LITERAL_TEXT | Section 10 character contract |
| `ConsequenceTerm` | `term_id` | `str` | required | same-request term id | non-empty; unique among terms |
| `ConsequenceTerm` | `term_kind` | `str` | required | RESOURCE_MATH_TERM_KINDS | consequence term member |
| `ConsequenceTerm` | `value_mode` | `str` | required | TERM_VALUE_MODES | member; policy_only cannot produce accepted/normalized/proposal |
| `ConsequenceTerm` | `subject_binding_id` | `str` | required | same request subject binding | must resolve |
| `ConsequenceTerm` | `resource_ref_id` | `str \| None` | `None` | same-request ResourceReference id | must resolve when supplied |
| `ConsequenceTerm` | `quantity_id` | `str \| None` | `None` | same-request QuantitySpecification id | must resolve when supplied |
| `ConsequenceTerm` | `timing` | `str` | `immediate` | CONSEQUENCE_TIMINGS | member |
| `ConsequenceTerm` | `outcome_mode` | `str` | required | CONSEQUENCE_OUTCOME_MODES | member |
| `ConsequenceTerm` | `policy_route` | `str \| None` | `None` | POLICY_ONLY_ROUTES | exact route mapping preserved |
| `ConsequenceTerm` | `dependency_refs` | `tuple[str, ...]` | `()` | ResourceMathDependency.dependency_id | each must resolve in same request |
| `ConsequenceTerm` | `source_literal` | `str \| None` | `None` | SOURCE_LITERAL_TEXT | Section 10 character contract |
| `CostBundle` | `bundle_id` | `str` | required | same-request bundle id | non-empty; unique |
| `CostBundle` | `term_ids` | `tuple[str, ...]` | required non-empty | CostTerm.term_id | unique; same request |
| `CostBundle` | `bundle_policy` | `str` | required | COST_BUNDLE_POLICIES | member |
| `CostBundle` | `minimum_required_terms` | `int \| None` | `None` | bundle bounds | non-bool positive integer when applicable |
| `CostBundle` | `maximum_allowed_terms` | `int \| None` | `None` | bundle bounds | non-bool positive integer when applicable |
| `CostBundle` | `alternative_group_id` | `str \| None` | `None` | same-request alternative group | source-local grouping only |
| `ResourceMathRequest` | `request_id` | `str` | required | resource math request id | non-empty |
| `ResourceMathRequest` | `stage` | `str` | `resource_math_requested` | RESOURCE_MATH_STAGES | request capture stage only |
| `ResourceMathRequest` | `subject_refs` | `tuple[ResourceMathSubjectReference, ...]` | required non-empty | subject aggregate | one primary_subject |
| `ResourceMathRequest` | `resource_refs` | `tuple[ResourceReference, ...]` | `()` | resource aggregate | unique resource_ref_id |
| `ResourceMathRequest` | `quantity_specs` | `tuple[QuantitySpecification, ...]` | `()` | quantity aggregate | unique quantity_id |
| `ResourceMathRequest` | `terms` | `tuple[CostTerm \| ConsequenceTerm, ...]` | `()` | term aggregate | unique term_id |
| `ResourceMathRequest` | `bundles` | `tuple[CostBundle, ...]` | `()` | bundle aggregate | unique bundle_id |
| `ResourceMathRequest` | `dependencies` | `tuple[ResourceMathDependency, ...]` | `()` | dependency aggregate owner | owns all external binding records |
| `ResourceMathRequest` | `validation_request_ref_id` | `str \| None` | `None` | external binding: validation_request_ref | lifecycle Section 6 |
| `ResourceMathRequest` | `owner_handoff_ref_ids` | `tuple[str, ...]` | `()` | external binding: owner_handoff_ref | each member lifecycle Section 6 |
| `ResourceMathRequest` | `trace_ref_id` | `str \| None` | `None` | external binding: runtime_trace_ref | lifecycle Section 6 |
| `ResourceMathResult` | `result_id` | `str` | required | resource math result id | non-empty |
| `ResourceMathResult` | `request_id` | `str` | required | supplied ResourceMathRequest.request_id | same aggregate validation; no repository lookup |
| `ResourceMathResult` | `stage` | `str` | required | Section 5 compatibility matrix | member |
| `ResourceMathResult` | `decision` | `str` | required | RESOURCE_MATH_DECISIONS | member; compatible with stage/flags |
| `ResourceMathResult` | `blocking` | `bool` | required | Section 5 compatibility matrix | exact flag |
| `ResourceMathResult` | `quarantined` | `bool` | `False` | Section 5 compatibility matrix | exact flag |
| `ResourceMathResult` | `escalated` | `bool` | `False` | Section 5 compatibility matrix | exact flag |
| `ResourceMathResult` | `validation_request_ref_id` | `str \| None` | `None` | external binding: validation_request_ref | lifecycle Section 6 |
| `ResourceMathResult` | `validation_result_ref_id` | `str \| None` | `None` | external binding: validation_result_ref | must be complete for validation_passed |
| `ResourceMathResult` | `validation_decision` | `str \| None` | `None` | VALIDATION_INTEGRATION_DECISIONS | validation_passed required for proposal |
| `ResourceMathResult` | `scoped_subject_binding_ids` | `tuple[str, ...]` | required non-empty | request subject bindings | typed result scope closure |
| `ResourceMathResult` | `scoped_resource_ref_ids` | `tuple[str, ...]` | `()` | request resource refs | typed result scope closure |
| `ResourceMathResult` | `scoped_quantity_ids` | `tuple[str, ...]` | `()` | request quantities | typed result scope closure |
| `ResourceMathResult` | `scoped_term_ids` | `tuple[str, ...]` | `()` | request terms | typed result scope closure |
| `ResourceMathResult` | `scoped_bundle_ids` | `tuple[str, ...]` | `()` | request bundles | typed result scope closure |
| `ResourceMathResult` | `dependency_refs` | `tuple[str, ...]` | `()` | request dependencies | scoped dependencies must resolve |
| `ResourceMathResult` | `trace_ref_id` | `str \| None` | `None` | external binding: runtime_trace_ref | lifecycle Section 6 |
| `SettlementProposal` | `proposal_id` | `str` | required | settlement proposal id | non-empty |
| `SettlementProposal` | `result_id` | `str` | required | supplied ResourceMathResult.result_id | no request_id field; original request supplied as aggregate argument |
| `SettlementProposal` | `validation_result_ref_id` | `str` | required | external binding: validation_result_ref | must match supplied result and be complete |
| `SettlementProposal` | `validation_decision` | `str` | required | validation_passed | must equal validation_passed |
| `SettlementProposal` | `proposed_state_delta_refs` | `tuple[str, ...]` | required non-empty | external binding: state_delta_ref | each complete |
| `SettlementProposal` | `rollback_accounting_refs` | `tuple[str, ...]` | `()` | external binding: rollback_accounting_ref | each complete when supplied |
| `SettlementProposal` | `trace_ref_id` | `str \| None` | `None` | external binding: runtime_trace_ref | lifecycle Section 6 |
| `SettlementProposal` | `settlement_notes` | `tuple[str, ...]` | `()` | internal-only proposal notes | not public projection |

The proposal shape has no stored request identifier field. The original request is supplied to `create_settlement_proposal` and `validate_settlement_proposal` as an aggregate argument; it is not stored on the proposal. The incorrect singular owner-handoff, runtime-trace, and rollback-accounting field-name variants are not effective fields. The effective names are `ResourceMathRequest.owner_handoff_ref_ids`, `trace_ref_id` on request/result/proposal, and `SettlementProposal.rollback_accounting_refs`.

### 3.3 External binding lifecycle clarification for all effective fields

Every external binding field requires exactly one matching dependency record with the correct `dependency_type` and `reference_id`. The record must have `required=True`. `satisfied=True` means complete binding. `satisfied=False` is permitted only as a structurally valid incomplete binding. An incomplete binding remains linked to the field, is not resolution-ready, and forces `blocked_missing_dependency` for every scoped result that reaches it. Missing record, wrong type, wrong reference ID, duplicate matching records, or `required=False` invalidates the aggregate before result construction. Incomplete bindings cannot support accepted, normalized, or proposal-eligible results.

This applies to the actual effective fields: `ResourceMathSubjectReference.subject_ref_id`; `ResourceReference.unit_ref_id`; `ResourceReference.dimension_ref_id`; `QuantitySpecification.unit_ref_id`; `QuantitySpecification.dimension_ref_id`; `ResourceMathRequest.validation_request_ref_id`; `ResourceMathRequest.owner_handoff_ref_ids`; request/result/proposal `trace_ref_id`; `ResourceMathResult.validation_request_ref_id`; `ResourceMathResult.validation_result_ref_id`; `SettlementProposal.validation_result_ref_id`; `SettlementProposal.result_id` when bound by `resource_math_result_ref`; `SettlementProposal.proposed_state_delta_refs`; `SettlementProposal.rollback_accounting_refs`; and provenance-bearing `provenance_refs`.

### 3.4 FALSE_ONLY_AUTHORITY_FIELDS shared surface

`FALSE_ONLY_AUTHORITY_FIELDS` is one authoritative shared surface. Each field is annotated `bool`, defaults to `False`, and every factory and validator must reject every `True` value, including values on manually constructed frozen dataclasses.

| field | annotation | default | invariant |
|---|---|---:|---|
| `calculation_executed` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `affordability_executed` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `reservation_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `settlement_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `consequence_application_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `mutation_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `state_delta_application_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `transaction_execution_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `event_commitment_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `event_append_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `persistence_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `replay_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `rng_execution_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `table_oracle_execution_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `model_authority_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `live_play_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `ui_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `conversion_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |
| `canon_promotion_authorized` | `bool` | `False` | false-only authority field; every factory and validator rejects `True`, including manually constructed frozen dataclasses |

Explicit inclusion rows:

| shape | included shared surface | generation rule |
|---|---|---|
| `ResourceMathRequest` | `FALSE_ONLY_AUTHORITY_FIELDS` | include all nineteen fields exactly once, each `bool = False` |
| `ResourceMathResult` | `FALSE_ONLY_AUTHORITY_FIELDS` | include all nineteen fields exactly once, each `bool = False` |
| `SettlementProposal` | `FALSE_ONLY_AUTHORITY_FIELDS` | include all nineteen fields exactly once, each `bool = False` |

## 4. Resource, quantity, term, and source-local lexical contracts

`ResourceReference`, `QuantitySpecification`, `CostTerm`, and `ConsequenceTerm` are declarative references only. They do not calculate, resolve, dereference, normalize, convert units, choose numeric representations, or infer hidden values.

Quantity rules preserved from PR-5F:

- `precision: int | None = None`; `bool` is rejected; positive integer precision is permitted only when `representation_kind == decimal_exact`; precision is `None` for `integer_exact`, `fraction_exact`, `fixed_point_scaled`, `source_literal_only`, and `blocked_pending_numeric_choice`.
- `scale: int | None = None`; `bool` is rejected; non-negative scale is permitted only when `representation_kind == fixed_point_scaled`; every other representation requires `scale=None`.
- `blocked_pending_numeric_choice` produces no accepted or normalized result and routes through blocker precedence.
- A leading `-` is lexically negative; `-0`, `-0.0`, and `-0/1` are negative; leading `+` is not negative.
- `negative_values_forbidden` rejects lexically negative `magnitude_text` at aggregate validation.
- `negative_values_allowed_by_source` requires non-empty `source_literal`, non-empty `provenance_refs`, and complete `provenance_ref` bindings.
- `negative_values_require_owner_handoff` routes to `requires_owner_handoff` at `blocked_pending_owner_handoff` and cannot be accepted, normalized, or proposal-eligible.

Term rules preserved from PR-5F:

- `policy_only` terms cannot produce `accepted_for_planning`, `normalized_for_planning`, or `SettlementProposal`.
- Exact policy-only route handling is preserved: `doctrine_escalation_required` → `escalated_to_doctrine`; `quarantine_required` → `quarantined_for_review`; `owner_handoff_required` → `requires_owner_handoff`; `validation_review_required` → `requires_validation_review`; `source_local_retained` → `source_local_retained` only within lawful source-local stages.
- PR-5H does not replace exact policy-only routing with a generic `blocked_incompatible_policy` route.

## 5. Authoritative decision/stage compatibility matrix

PR-5H republishes the complete inherited PR-5D compatibility contract as the effective PR-5H matrix while preserving all current controlled stage sets.

Exact controlled stage sets:

- `DECLARATION_PROGRESS_STAGES = {"source_declaration_captured", "subject_refs_bound", "resource_refs_declared", "quantity_specs_declared", "terms_declared", "bundle_structure_declared", "policy_refs_declared", "dependency_refs_bound", "calculation_ready_for_review"}`
- `SOURCE_LOCAL_STAGES = {"source_declaration_captured", "resource_refs_declared", "terms_declared", "bundle_structure_declared", "policy_refs_declared"}`
- `VALIDATION_BLOCK_STAGES = {"blocked_pending_validation"}`
- `OWNER_HANDOFF_STAGES = {"blocked_pending_owner_handoff"}`
- `MISSING_DEPENDENCY_STAGES = {"dependency_refs_bound", "blocked_pending_validation", "blocked_pending_owner_handoff"}`
- `POLICY_BLOCK_STAGES = {"policy_refs_declared"}`
- `HIDDEN_INFORMATION_BLOCK_STAGES = {"dependency_refs_bound", "blocked_pending_validation"}`
- `QUARANTINE_STAGES = {"quarantined_for_review"}`
- `ESCALATION_STAGES = {"escalated_to_doctrine"}`

Exact effective decision/stage compatibility matrix:

| decision | lawful stage set | blocking | quarantined | escalated |
|---|---|---:|---:|---:|
| `accepted_for_planning` | `{resource_math_requested, calculation_ready_for_review}` | `False` | `False` | `False` |
| `normalized_for_planning` | `DECLARATION_PROGRESS_STAGES` | `False` | `False` | `False` |
| `source_local_retained` | `SOURCE_LOCAL_STAGES` | `False` | `False` | `False` |
| `requires_validation_review` | `VALIDATION_BLOCK_STAGES` | `True` | `False` | `False` |
| `requires_owner_handoff` | `OWNER_HANDOFF_STAGES` | `True` | `False` | `False` |
| `blocked_missing_dependency` | `MISSING_DEPENDENCY_STAGES` | `True` | `False` | `False` |
| `blocked_incompatible_policy` | `POLICY_BLOCK_STAGES` | `True` | `False` | `False` |
| `blocked_hidden_information` | `HIDDEN_INFORMATION_BLOCK_STAGES` | `True` | `False` | `False` |
| `quarantined_for_review` | `QUARANTINE_STAGES` | `True` | `True` | `False` |
| `escalated_to_doctrine` | `ESCALATION_STAGES` | `True` | `False` | `True` |

Every unlisted decision/stage pair is invalid. A decision/stage pair not admitted here cannot be rescued by validation state, dependency state, or flag overrides.

## 6. Five-state dependency lifecycle and aggregate ownership

`ResourceMathRequest.dependencies` is the sole aggregate owner for dependency records used by the request, result, and proposal validation architecture. Leaf validators validate only local shape, field types, and controlled vocabulary membership; Level B aggregate validation validates cross-record ownership, binding, and lifecycle.

| state | name | dependency posture | aggregate validity | result/proposal consequence |
|---|---|---|---|---|
| A | complete binding | exactly one matching dependency with correct `dependency_type`, correct `reference_id`, `required=True`, `satisfied=True` | valid and resolution-ready for that binding | may support accepted/normalized/proposal-eligible only if all other rules pass |
| B | incomplete binding | exactly one matching dependency with correct `dependency_type`, correct `reference_id`, `required=True`, `satisfied=False` | structurally valid but incomplete; field remains linked | request is not resolution-ready; every scoped result reaching it must use `blocked_missing_dependency`; never accepted, normalized, or proposal-eligible |
| C | invalid binding | missing record, wrong type, wrong reference id, duplicate matching records, or `required=False` for a binding | invalid aggregate before result construction | no result or proposal may be constructed |
| D | advisory optional unsatisfied | dependency has `required=False`, `satisfied=False`, and is not bound to any field or scoped required dependency | valid advisory note only | may not satisfy any binding; ignored for resolution readiness |
| E | contradictory dependency aggregate | duplicate `dependency_id`, duplicate `(dependency_type, reference_id)` where uniqueness is required, contradictory hidden/owner flags, or dependency named by scoped record but absent | invalid aggregate before result construction | no result or proposal may be constructed |

Complete versus incomplete versus missing bindings are therefore distinct. Hidden information with `hidden_info_safe=False` routes scoped results to `blocked_hidden_information` at a lawful inherited stage; PR-5H does not introduce an alternate unspecified RT-005 handoff result route. RT-005 retains later projection/redaction ownership only.

## 7. Typed result-scope cardinality and closure

A `ResourceMathResult` is validated with its supplied `ResourceMathRequest`; no repository lookup occurs. The result's typed scope is a closed subset of the request aggregate:

- `scoped_subject_binding_ids` is non-empty and every id resolves in `request.subject_refs`.
- `scoped_resource_ref_ids`, `scoped_quantity_ids`, `scoped_term_ids`, and `scoped_bundle_ids` are each unique and resolve inside the same request.
- Scoped terms pull in their `resource_ref_id`, `quantity_id`, and `dependency_refs` closure.
- Scoped bundles pull in all `term_ids` and their dependency closure.
- Every external binding reached by the typed scope must be state A complete for accepted/normalized/proposal-eligible outcomes.
- Empty typed scope is not lawful for accepted, normalized, or settlement-eligible results.

## 8. Exact eight-level simultaneous blocker precedence

This table is preserved and remains authoritative. The no-blocker row points to the PR-5H compatibility matrix in Section 5, not to an unstated historical matrix.

| precedence | condition | required result route | notes |
|---:|---|---|---|
| 1 | invalid aggregate: missing binding record, wrong dependency type, wrong reference id, duplicate matching records, `required=False` binding, duplicate ids, or broken same-aggregate reference | reject before result construction | not a blocker result |
| 2 | `doctrine_escalation_required` policy route or doctrine escalation condition | `decision=escalated_to_doctrine`, stage from `ESCALATION_STAGES`, `blocking=True`, `quarantined=False`, `escalated=True` | terminal escalation |
| 3 | `quarantine_required` policy route or quarantine condition | `decision=quarantined_for_review`, stage from `QUARANTINE_STAGES`, `blocking=True`, `quarantined=True`, `escalated=False` | terminal quarantine |
| 4 | hidden information unsafe in scoped dependency | `decision=blocked_hidden_information`, stage from `HIDDEN_INFORMATION_BLOCK_STAGES`, `blocking=True` | no alternate RT-005 handoff result route |
| 5 | owner handoff required, including `owner_handoff_required` route or negative owner handoff policy | `decision=requires_owner_handoff`, stage from `OWNER_HANDOFF_STAGES`, `blocking=True` | complete owner_handoff_ref binding required when field names owner handoff |
| 6 | validation review required but not validation passed | `decision=requires_validation_review`, stage from `VALIDATION_BLOCK_STAGES`, `blocking=True` | `validation_ready` is not `validation_passed` |
| 7 | incomplete required dependency or scoped state B binding | `decision=blocked_missing_dependency`, stage from `MISSING_DEPENDENCY_STAGES`, `blocking=True` | structurally valid incomplete binding blocks resolution |
| 8 | policy-only term without exact route, blocked numeric choice, incompatible bundle/policy shape | `decision=blocked_incompatible_policy`, stage from `POLICY_BLOCK_STAGES`, `blocking=True` | policy-only exact routes above take precedence |
| 9 | no blocker after full aggregate validation | use the authoritative decision/stage compatibility matrix in Section 5 | accepted/normalized/proposal eligibility still requires complete bindings and Section 12 |

## 9. CostBundle compatibility matrix

`CostBundle` remains declarative and non-executable. It never calculates affordability or settlement. Bounds are structural declarations only.

| bundle_policy | minimum_required_terms | maximum_allowed_terms | term ordering | partial settlement | compatibility invariant |
|---|---|---|---|---|---|
| `all_required` | `None` | `None` | source order retained only | forbidden unless separately declared | all listed terms are required declarations |
| `any_one` | `None` | `1` or `None` | unordered alternatives | forbidden | exactly one alternative may later be selected by an authorized executor; PR-5H does not select |
| `at_least_minimum` | positive int | `None` or positive int >= minimum | unordered | forbidden unless `partial_settlement_allowed` also present in inherited route | minimum is structural |
| `at_most_maximum` | `None` or positive int <= maximum | positive int | unordered | forbidden unless separately declared | maximum is structural |
| `exactly_one` | `1` or `None` | `1` or `None` | unordered alternatives | forbidden | source-local alternatives preserved |
| `ordered_sequence` | `None` | `None` | tuple order significant as declaration | forbidden | no execution order authority |
| `partial_settlement_allowed` | positive int or `None` | positive int or `None` | source order retained | allowed as proposal shape only | no mutation or actual settlement |
| `partial_settlement_forbidden` | `None` | `None` | source order retained | forbidden | default conservative rule |

Bundle ids, term ids, and alternative groups are same-aggregate only. No bundle policy can bypass blocker precedence or incomplete binding lifecycle.

## 10. Source-literal contract

`source_literal` is internal-only evidence text. It must be a non-empty `str` when supplied. Leading or trailing whitespace is rejected. Multiline values are rejected. carriage return, line feed, tab, NUL, Unicode category `Cc`, and Unicode category `Cs` are rejected. Ordinary Unicode letters, numbers, punctuation, symbols, and spaces are permitted and preserved exactly. No normalization, tokenization, parsing, arithmetic, or evaluation occurs.

Source-supported negative literals use the same source-literal character contract. They also require complete provenance bindings and do not authorize calculation.

## 11. Direct request/result/proposal validation architecture

Future validation architecture is direct and aggregate-based:

```python
create_resource_math_result(*, request: ResourceMathRequest, ...) -> ResourceMathResult
validate_resource_math_result(result: ResourceMathResult, *, request: ResourceMathRequest) -> bool
create_settlement_proposal(*, request: ResourceMathRequest, result: ResourceMathResult, ...) -> SettlementProposal
validate_settlement_proposal(proposal: SettlementProposal, *, request: ResourceMathRequest, result: ResourceMathResult) -> bool
```

There is no repository lookup, implicit dereference, hidden global registry, or stored proposal request identifier. The original request is supplied as an aggregate argument.

Validation levels:

- Level A structural validation checks local dataclass shape, annotations, defaults, controlled-vocabulary membership, tuple uniqueness where local, and false-only defaults.
- Level B aggregate validation checks dependency ownership, external binding lifecycle, same-aggregate reference closure, typed result scope, decision/stage compatibility, blocker precedence, validation integration, and proposal eligibility.

## 12. SettlementProposal eligibility

A `SettlementProposal` is eligible only when the supplied `ResourceMathResult` has all of the following:

- `result.stage == "calculation_ready_for_review"`;
- `result.decision in {"accepted_for_planning", "normalized_for_planning"}`;
- `result.blocking is False`;
- `result.quarantined is False`;
- `result.escalated is False`;
- `result.validation_decision == "validation_passed"`;
- all scoped required dependencies are satisfied;
- no scoped policy-only, blocked-numeric, hidden-information, missing-dependency, owner-handoff, quarantine, or escalation blocker.

Explicit negative and positive consequences:

- `accepted_for_planning` at `resource_math_requested` is not proposal-eligible.
- `normalized_for_planning` at any earlier declaration stage (`source_declaration_captured`, `subject_refs_bound`, `resource_refs_declared`, `quantity_specs_declared`, `terms_declared`, `bundle_structure_declared`, `policy_refs_declared`, or `dependency_refs_bound`) is not proposal-eligible.
- `source_local_retained` is never proposal-eligible.
- Only `accepted_for_planning` or `normalized_for_planning` at `calculation_ready_for_review` may proceed, subject to all other requirements.
- Incomplete state B bindings can never support proposal eligibility.
- A proposal with any `TRUE` field from `FALSE_ONLY_AUTHORITY_FIELDS` is invalid.

## 13. Factory/validator parity, serialization, and hidden-information ownership

Factories and validators must enforce identical rules for factory-created objects and manually constructed frozen dataclasses. Validators must reject every true false-only authority field, every invalid external binding, every incompatible decision/stage/flag combination, every scope closure failure, every exact policy route mismatch, and every ineligible proposal.

Serialization is internal-only. PR-5H defines no `to_public_dict`, no public projection, no redaction implementation, and no hidden-information disclosure path. Hidden-information partitioning, redaction, and projection remain owned by RT-005. Resource/consequence math records may retain internal trace/provenance ids only as non-dereferenced references.

## 14. PR-5G closure ledger, tracking, and gate decision

| PR-5G residual defect | PR-5H disposition |
|---|---|
| effective contract inventory could force PR-5A invention | closed by Section 3 ten-shape field matrix and constant surfaces |
| external binding language conflicted with incomplete lifecycle | closed by Sections 3.3 and 6 |
| normal stage/decision matrix was referenced but not present | closed by Section 5 authoritative matrix |
| no-blocker routing pointed to historical matrix | closed by Section 8 no-blocker row pointing to Section 5 |
| settlement proposal eligibility was too broad | closed by Section 12 exact eligibility |
| false-only fields were collapsed | closed by Section 3.4 shared surface |
| policy-only exact routes could be generalized accidentally | closed by Sections 4 and 8 |
| hidden-information route could drift to unspecified handoff | closed by Sections 6, 8, and 13 |

```yaml
gate_finding:
  artifact_id: RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001
  planning_only_status: true
  pr_5g_followed: true
  pr_279_not_merged_or_cherry_picked: true
  comprehensive_pr_278_contract_preserved: true
  inherited_constant_vocabularies_preserved: true
  donor_shaped_leakage_correction_preserved: true
  dependency_ownership_correction_preserved: true
  level_a_level_b_validation_distinction_preserved: true
  ten_shape_field_matrix_complete: true
  cost_bundle_matrix_preserved: true
  five_state_dependency_lifecycle_preserved: true
  typed_scope_closure_preserved: true
  eight_level_blocker_precedence_preserved: true
  source_literal_contract_preserved: true
  serialization_boundary_preserved: true
  external_binding_lifecycle_reconciled: true
  complete_decision_stage_compatibility_matrix_republished: true
  settlement_proposal_eligibility_exact: true
  false_only_authority_surface_complete: true
  pr_5a_authorized: false
  pr_5a_remains_blocked: true
  exactly_one_next_step: true
  next_step_authorized: RUNTIME-DOMAIN-PR-5I resource and consequence math final residual planning hardening review gate
  next_step_status: review_gate_only
```

## 15. Non-implementation reaffirmation and PR-5I classification

PR-5H is planning-only final residual hardening. It creates no runtime/domain implementation file, no `resource_consequence_math.py`, no formula or expression evaluator, no parser, no persistence structure, no factory, no validator, no settlement executor, no state mutation path, no event commitment path, no RNG executor, no table-oracle executor, no model/prompt/UI/live-play behavior, no conversion path, and no canon promotion path.

```yaml
runtime_domain_pr_5h_decision:
  artifact_type: final_residual_planning_hardening
  planning_hardening_only: true
  implementation_status: planning_only
  pr_5a_unauthorized: true
  pr_5a_remains_blocked: true
  pr_5i_is_sole_next_step: true
  next_step_authorized: RUNTIME-DOMAIN-PR-5I resource and consequence math final residual planning hardening review gate
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
  live_play_authorized_by_this_pr: false
  ui_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
```

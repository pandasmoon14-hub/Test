# RUNTIME-DOMAIN-PR-5D: Resource and Consequence Math Final Planning Hardening

## 1. Purpose, status, source ledger, and PR-5C closure matrix

Artifact ID: **RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001**.

This artifact is **planning-only**. It closes the PR-5C findings against PR-5B, implements no code, authorizes only **RUNTIME-DOMAIN-PR-5E: Resource and Consequence Math Final Planning Hardening Review Gate**, and keeps PR-5A blocked. It grants no resource calculation, validation execution, settlement, mutation, persistence, model integration, conversion, or canon authority.

Source ledger:

- `RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001`
- `RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001`
- `RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001`
- `RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001`
- `docs/doctrine/reviews/runtime_domain_pr_5c_resource_consequence_math_planning_hardening_review.md`
- `docs/doctrine/reviews/runtime_domain_pr_5b_resource_consequence_math_planning_hardening.md`
- `docs/doctrine/reviews/runtime_domain_pr_5_resource_consequence_math_service_plan.md`
- `docs/doctrine/reviews/runtime_domain_pr_4f_validation_integration_residual_hardening_review.md`
- `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`
- RT001 and RT003 through RT012 owner specifications
- `src/astra_runtime/domain/validation_integration.py`
- current domain and kernel skeletons, registry, and current decision log

PR-5C closure matrix: validation posture is replaced by the owned validation-integration decision surface; typed subject identity is added; stage/decision/blocking semantics are made exact; dependency field binding is made structural; consequence timing/outcome reuses cost surfaces; quantity validation is lexical only; bundle bounds and alternatives are disambiguated; request/result/proposal linkage is exact; internal references are same-aggregate only; serialization is internal-only; false-only authority remains preserved; and factory/validator parity is mandatory.

## 2. Backend-first invariant

- The LLM is not the game engine.
- Reference objects are not calculations.
- Results are not state.
- Settlement proposals are not transactions.
- `validation_ready` is not `validation_passed`.
- No resource, cost, consequence, or donor term becomes authoritative merely by appearing in a record.
- No canon authority is granted.

## 3. Validation-integration contract

PR-5D removes free-string validation posture from future leaf shapes. `validation_posture` is removed from the future contracts for `ResourceReference` and `ConsequenceTerm`. PR-5D does not define a duplicate local validation-posture vocabulary. Future PR-5A skeletons must use the public validation-integration decision surface owned by `validation_integration.py`: `VALIDATION_INTEGRATION_DECISIONS`. Validation state belongs only on `ResourceMathRequest`, `ResourceMathResult`, and `SettlementProposal`.

Exact future validation fields:

| shape | field | annotation | default | controlled surface |
|---|---|---|---|---|
| `ResourceMathRequest` | `validation_request_ref_id` | `str | None` | `None` | dependency type `validation_request_ref` when supplied |
| `ResourceMathResult` | `validation_request_ref_id` | `str | None` | `None` | dependency type `validation_request_ref` when supplied |
| `ResourceMathResult` | `validation_result_ref_id` | `str | None` | `None` | dependency type `validation_result_ref` when supplied |
| `ResourceMathResult` | `validation_decision` | `str | None` | `None` | `VALIDATION_INTEGRATION_DECISIONS` when supplied |
| `SettlementProposal` | `validation_result_ref_id` | `str` | required | dependency type `validation_result_ref` |
| `SettlementProposal` | `validation_decision` | `str` | required | must be `validation_passed` |

Rules:

- Any validation decision must belong to the existing `VALIDATION_INTEGRATION_DECISIONS` surface.
- On `ResourceMathResult`, `validation_decision is None` requires both `validation_request_ref_id is None` and `validation_result_ref_id is None`.
- On `ResourceMathResult`, any non-None `validation_decision` requires `validation_request_ref_id` plus a matching typed `validation_request_ref` dependency.
- `validation_ready` may omit `validation_result_ref_id`.
- `validation_ready` may include `validation_result_ref_id` only when a matching typed `validation_result_ref` dependency is present.
- Every other supplied validation decision requires `validation_result_ref_id` plus a matching typed `validation_result_ref` dependency.
- `validation_result_ref_id` may not exist without `validation_decision`.
- `SettlementProposal` requires `validation_decision == "validation_passed"`, a non-empty `validation_result_ref_id`, and a matching typed validation-result dependency.
- No validation field authorizes calculation, settlement, mutation, or event commitment.

## 4. Typed subject identity

Proposed future frozen shape: `ResourceMathSubjectReference`.

Exact fields:

| field | annotation | default | controlled surface | invariant |
|---|---|---|---|---|
| `subject_binding_id` | `str` | required | same-aggregate subject binding id | non-empty and unique |
| `subject_type` | `str` | required | `RESOURCE_MATH_SUBJECT_TYPES` | non-empty member |
| `subject_ref_id` | `str` | required | external or upstream subject reference | non-empty, no dereference |
| `subject_role` | `str` | required | `RESOURCE_MATH_SUBJECT_ROLES` | non-empty member |
| `owner_domain` | `str` | required | `RESOURCE_MATH_OWNER_DOMAINS` | non-empty member |
| `visibility_policy` | `str` | `"public"` | `VISIBILITY_POLICIES` | not public-output authority |
| `provenance_refs` | `tuple[str, ...]` | `()` | provenance reference dependencies when external | tuple, unique non-empty ids |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | metadata only | defensive copy, no callables |

`RESOURCE_MATH_SUBJECT_ROLES` exact future surface:

- `primary_subject`
- `payer_subject`
- `beneficiary_subject`
- `resource_owner`
- `affected_subject`
- `source_subject`
- `target_subject`
- `authority_source`
- `provenance_source`

Rules: `subject_type` belongs to `RESOURCE_MATH_SUBJECT_TYPES`; `subject_role` belongs to `RESOURCE_MATH_SUBJECT_ROLES`; `owner_domain` belongs to `RESOURCE_MATH_OWNER_DOMAINS`; all IDs are non-empty; subject-binding IDs are unique; no object dereferencing occurs; cross-subject costs and consequences use explicit subject bindings; raw untyped subject IDs are not sufficient. All future shape contracts use subject-binding IDs rather than untyped subject references where appropriate.

Aggregate cardinality rules: `ResourceMathRequest.subject_refs` is non-empty; exactly one subject reference in each request has `subject_role == "primary_subject"`; zero primary subjects is invalid; multiple primary subjects are invalid; `subject_binding_id` values are unique within the request; every `ResourceReference.subject_binding_id`, `CostTerm.subject_binding_id`, and `ConsequenceTerm.subject_binding_id` resolves inside the same `ResourceMathRequest.subject_refs` aggregate.

## 5. Stage and decision compatibility

PR-5D preserves PR-5B's stage and decision vocabularies except where PR-5C required correction. `ResourceMathResult` must define exact fields `stage`, `decision`, `blocking`, `quarantined`, and `escalated`.

Exact controlled stage sets used by this matrix:

- `DECLARATION_PROGRESS_STAGES = {"source_declaration_captured", "subject_refs_bound", "resource_refs_declared", "quantity_specs_declared", "terms_declared", "bundle_structure_declared", "policy_refs_declared", "dependency_refs_bound", "calculation_ready_for_review"}`
- `SOURCE_LOCAL_STAGES = {"source_declaration_captured", "resource_refs_declared", "terms_declared", "bundle_structure_declared", "policy_refs_declared"}`
- `VALIDATION_BLOCK_STAGES = {"blocked_pending_validation"}`
- `OWNER_HANDOFF_STAGES = {"blocked_pending_owner_handoff"}`
- `MISSING_DEPENDENCY_STAGES = {"dependency_refs_bound", "blocked_pending_validation", "blocked_pending_owner_handoff"}`
- `POLICY_BLOCK_STAGES = {"policy_refs_declared"}`
- `HIDDEN_INFORMATION_BLOCK_STAGES = {"dependency_refs_bound", "blocked_pending_validation"}`
- `QUARANTINE_STAGES = {"quarantined_for_review"}`
- `ESCALATION_STAGES = {"escalated_to_doctrine"}`

Exact compatibility matrix:

| decision | allowed-stage set | blocking | quarantined | escalated | terminal | validation dependency requirement | owner dependency requirement |
|---|---|---:|---:|---:|---:|---|---|
| `accepted_for_planning` | `{"calculation_ready_for_review"}` | `False` | `False` | `False` | `False` | no validation dependency required; validation refs forbidden unless section 3 co-presence is satisfied | no owner-handoff dependency required; owner handoff refs forbidden |
| `normalized_for_planning` | `DECLARATION_PROGRESS_STAGES` | `False` | `False` | `False` | `False` | no validation dependency required; validation refs forbidden unless section 3 co-presence is satisfied | no owner-handoff dependency required; owner handoff refs forbidden |
| `source_local_retained` | `SOURCE_LOCAL_STAGES` | `False` | `False` | `False` | `False` | no validation dependency required; validation refs forbidden unless section 3 co-presence is satisfied | no owner-handoff dependency required; owner handoff refs forbidden |
| `requires_validation_review` | `VALIDATION_BLOCK_STAGES` | `True` | `False` | `False` | `False` | exactly one required/satisfied `validation_request_ref` matching `validation_request_ref_id`; `validation_result_ref_id` absent | no owner-handoff dependency required; owner handoff refs forbidden |
| `requires_owner_handoff` | `OWNER_HANDOFF_STAGES` | `True` | `False` | `False` | `False` | no validation dependency required unless section 3 co-presence is satisfied | exactly one required/satisfied `owner_handoff_ref` for each owner handoff field reference |
| `blocked_missing_dependency` | `MISSING_DEPENDENCY_STAGES` | `True` | `False` | `False` | `False` | no validation dependency required unless section 3 co-presence is satisfied | no owner-handoff dependency required unless owner handoff refs are present |
| `blocked_incompatible_policy` | `POLICY_BLOCK_STAGES` | `True` | `False` | `False` | `False` | no validation dependency required; validation refs forbidden unless section 3 co-presence is satisfied | no owner-handoff dependency required unless owner handoff refs are present |
| `blocked_hidden_information` | `HIDDEN_INFORMATION_BLOCK_STAGES` | `True` | `False` | `False` | `False` | no validation dependency required unless section 3 co-presence is satisfied | no owner-handoff dependency required unless owner handoff refs are present |
| `quarantined_for_review` | `QUARANTINE_STAGES` | `True` | `True` | `False` | `True` | no validation dependency required unless section 3 co-presence is satisfied | no owner-handoff dependency required unless owner handoff refs are present |
| `escalated_to_doctrine` | `ESCALATION_STAGES` | `True` | `False` | `True` | `True` | no validation dependency required unless section 3 co-presence is satisfied | no owner-handoff dependency required unless owner handoff refs are present |

No quarantined, escalated, blocked, validation-review, or owner-handoff result may be treated as accepted planning or transaction-ready. Dual use of `quarantined_for_review` and `escalated_to_doctrine` as both stage and decision is explicitly lawful only through this compatibility matrix. Every decision/stage pair not admitted by the table is invalid for PR-5A.

## 6. Dependency contract and exact field-binding matrix

PR-5D uses PR-5B's `RESOURCE_MATH_DEPENDENCY_TYPES` as baseline and adds missing typed reference categories required by PR-5C. Exact future dependency types include: `command_ref`, `action_legality_ref`, `state_projection_ref`, `validation_request_ref`, `validation_result_ref`, `runtime_trace_ref`, `owner_handoff_ref`, `provenance_ref`, `rng_result_ref`, `table_oracle_result_ref`, `state_delta_ref`, `transaction_ref`, `event_commitment_ref`, `resource_math_request_ref`, `resource_math_result_ref`, and `rollback_accounting_ref`.

Every external reference field must have exactly one matching required and satisfied `ResourceMathDependency`:

| external reference field family | matching dependency type |
|---|---|
| command reference | `command_ref` |
| action-legality reference | `action_legality_ref` |
| state-projection reference | `state_projection_ref` |
| validation-request reference | `validation_request_ref` |
| validation-result reference | `validation_result_ref` |
| runtime trace | `runtime_trace_ref` |
| owner handoff | `owner_handoff_ref` |
| provenance reference | `provenance_ref` |
| RNG result | `rng_result_ref` |
| table/oracle result | `table_oracle_result_ref` |
| proposed state delta | `state_delta_ref` |
| transaction prerequisite | `transaction_ref` |
| event-commitment prerequisite | `event_commitment_ref` |
| `ResourceMathResult.request_id` | `resource_math_request_ref` |
| `SettlementProposal.result_id` | `resource_math_result_ref` |
| `SettlementProposal.rollback_accounting_refs` | `rollback_accounting_ref` |

Validation co-presence rules for `ResourceMathResult`: `validation_decision is None` requires `validation_request_ref_id is None` and `validation_result_ref_id is None`; any non-None `validation_decision` requires `validation_request_ref_id` plus exactly one required/satisfied `validation_request_ref` dependency; `validation_ready` may omit `validation_result_ref_id`; `validation_ready` may include `validation_result_ref_id` only with exactly one required/satisfied `validation_result_ref` dependency; every non-`validation_ready` validation decision requires `validation_result_ref_id` plus exactly one required/satisfied `validation_result_ref` dependency. `validation_result_ref_id` may not exist without `validation_decision`.

Rules: `dependency_id` is unique; `(dependency_type, reference_id)` is unique; binding dependencies are `required=True` and `satisfied=True`; `required=True` and `satisfied=False` forces a blocking result; `required=False` and `satisfied=False` is lawful but cannot satisfy a required field binding; `hidden_info_safe=False` prohibits public projection and requires RT-005 handling; internal IDs for subject bindings, resources, quantities, terms, bundles, and consequences resolve inside the same aggregate and do not require external dependency records; no dependency is executed or dereferenced.

## 7. Consequence timing and outcome policy

`ConsequenceTerm` lawfully reuses `COST_TIMING_POLICIES` and `COST_OUTCOME_POLICIES`. Therefore existing defaults `timing_policy="blocked_pending_validation"` and `outcome_policy="validation_blocked"` are lawful because those literals already belong to the reused surfaces. PR-5D does not create duplicate consequence timing/outcome surfaces. Validators must check `ConsequenceTerm` values against the reused cost policy surfaces.

## 8. Quantity lexical contract

PR-5A may perform lexical validation only.

Exact future lexical rules:

- `magnitude_text` and `source_literal` are strings, never floats.
- Leading/trailing whitespace is rejected rather than silently normalized.
- Empty strings are rejected where the representation requires a value.
- Case-insensitive NaN and infinity tokens are rejected.
- Binary-float input is rejected.
Exact lexical grammars are ASCII regular expressions matched against the entire string:

| representation_kind | required lexical fields | exact grammar | explicit exclusions |
|---|---|---|---|
| `integer_exact` | `magnitude_text` | `^[+-]?(0|[1-9][0-9]*)$` | no whitespace, exponent notation, decimal point, leading zero except `0`, or embedded separators |
| `decimal_exact` | `magnitude_text` | `^[+-]?(0|[1-9][0-9]*)\.[0-9]+$` | no exponent notation, leading decimal point, trailing decimal point, leading zero except before `.`, or embedded separators |
| `fraction_exact` | `magnitude_text` | `^[+-]?(0|[1-9][0-9]*)/[1-9][0-9]*$` | no zero denominator, signed denominator, decimal numerator, decimal denominator, or mixed-number shorthand |
| `fixed_point_scaled` | `magnitude_text` plus `scale` | magnitude `^[+-]?(0|[1-9][0-9]*)$`; scale is an `int` that is not `bool` and is `>= 0` | no decimal point in magnitude, no exponent notation, no negative scale |
| `source_literal_only` | `source_literal` | `^\S(?:.*\S)?$` | no empty string, no leading/trailing whitespace, no evaluation |
| `blocked_pending_numeric_choice` | `source_literal` | `^\S(?:.*\S)?$` | no empty string, no leading/trailing whitespace, blocks progression |

Plus signs are permitted only by the grammars above. Leading zeros are rejected except for the single literal `0` or a decimal beginning `0.`. Decimal exponent notation is always rejected. Lexical checks may use string inspection or regular expressions.

PR-5A must not instantiate `Decimal`, `Fraction`, `float`, or perform comparison, arithmetic, rounding, conversion, or affordability checks. Negative-value permission is an explicit field, `negative_value_policy: str = "negative_values_forbidden"`, controlled by `QUANTITY_NEGATIVE_VALUE_POLICIES`; negative values must never be implicitly accepted.

`QUANTITY_NEGATIVE_VALUE_POLICIES`: `negative_values_forbidden`, `negative_values_allowed_by_source`, `negative_values_require_owner_handoff`.

## 9. CostBundle exact semantics

- `term_ids` must be non-empty and unique.
- `minimum_required_terms` and `maximum_allowed_terms` are `int | None`.
- `bool` is rejected as an integer.
- Supplied bounds must be positive.
- `minimum_required_terms <= maximum_allowed_terms` when both are supplied.
- Both bounds count unique declared `term_ids`.
- Bounds apply before alternative selection, owner handoff, validation, or settlement.
- `minimum_required_terms` cannot exceed `len(term_ids)`.
- Chosen maximum rule: because `maximum_allowed_terms` is a declaration bound over the declared bundle membership, when supplied it cannot be below `len(term_ids)`; if a source needs fewer chosen alternatives, that is modeled by alternative groups and future selection policy, not by lowering `maximum_allowed_terms`.

Alternative groups must have unique group IDs, non-empty unique member term IDs, members contained in `term_ids`, no term in more than one alternative group unless a future explicit policy authorizes overlap, and no alternative selection in PR-5A.

Compatibility matrix controlled sets:

- `ORDERING_DECLARED_SET = {"unordered_terms", "source_ordered_terms", "dependency_ordered_terms", "priority_ordered_terms"}`
- `ORDERING_ORDERED_SET = {"source_ordered_terms", "dependency_ordered_terms", "priority_ordered_terms"}`
- `PARTIAL_REVIEW_SET = {"partial_settlement_requires_owner_review", "partial_settlement_requires_validation"}`
- `ALTERNATIVE_ATOMICITY_SET = {"alternative_exactly_one", "alternative_at_least_one", "alternative_at_most_one", "alternative_any"}`

Exact compatibility matrix; every combination not listed here is invalid for PR-5A:

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
| `{ "all_or_nothing_requested", "best_effort_requested", "ordered_partial_allowed", "unordered_partial_allowed" }` | `ORDERING_DECLARED_SET` | `{ "no_partial_settlement", "partial_settlement_allowed", "partial_settlement_requires_owner_review", "partial_settlement_requires_validation", "blocked_pending_settlement_policy" }` | overlapping groups | invalid: non-alternative atomicity cannot declare alternative groups |
| `ALTERNATIVE_ATOMICITY_SET` | `ORDERING_DECLARED_SET` | `{ "no_partial_settlement" }` | overlapping groups | invalid unless a future explicit policy authorizes overlap |

No settlement or alternative choice is executed.

## 10. Request/result/proposal contracts

`ResourceMathRequest` must bind request ID; command/action-legality refs where applicable; non-empty typed subject bindings with exactly one `primary_subject`; state-projection refs; declared resources; quantity specifications; terms; bundles; consequences; external dependencies; trace; provenance; owner handoffs; and optional validation-request ref.

`ResourceMathResult` must bind result ID; request ID; stage; decision; blocking/quarantine/escalation flags; diagnostics; normalized internal reference IDs; external dependencies; trace; optional validation request/result and decision fields; and all false-only authority fields.

`SettlementProposal` must require proposal ID; `ResourceMathResult` reference; one or more unique `proposed_state_delta_refs`; `validation_decision == "validation_passed"`; `validation_result_ref_id`; trace; matching external dependencies; visibility; rollback-accounting refs where present; and all false-only authority fields. An empty `proposed_state_delta_refs` tuple is invalid. `SettlementProposal` remains a non-mutating proposal and cannot be treated as a transaction, event, or committed state.

## 11. Internal-reference integrity

Future validators must enforce same-aggregate references: subject-binding IDs must exist; resource-reference IDs must exist; quantity IDs must exist; cost-term IDs must exist; bundle term IDs must exist; consequence IDs must exist; dependency IDs named by terms or requests must exist; duplicates are rejected; unresolved internal references are rejected; and no external object lookup occurs.

## 12. Serialization and hidden-information boundary

PR-5A implements internal `to_dict()` only. It must not implement `to_public_dict()`.

Rules: returned dictionaries are defensive copies; tuples become copied lists only in returned dictionaries; metadata remains defensively copied; no calculations occur during serialization; visibility does not itself authorize public output; RT-005/context projection owns all public, player-visible, narrator-visible, redacted, delayed-reveal, and derived-only projection; hidden source literals, quantities, dependencies, provenance, or backend IDs cannot be exposed by the resource-math module.

## 13. False-only authority contract

PR-5D preserves every PR-5B false-only field. Factories and validators must reject any manually constructed future object where a false-only field is true. No shared authority envelope redesign is authorized in PR-5D or PR-5A.

False-only fields: `calculation_executed`, `affordability_executed`, `reservation_authorized`, `settlement_authorized`, `consequence_application_authorized`, `mutation_authorized`, `state_delta_application_authorized`, `transaction_execution_authorized`, `event_commitment_authorized`, `event_append_authorized`, `persistence_authorized`, `replay_authorized`, `rng_execution_authorized`, `table_oracle_execution_authorized`, `model_authority_authorized`, `live_play_authorized`, `ui_authorized`, `conversion_authorized`, `canon_promotion_authorized`.

## 14. Exact future shape inventory

PR-5A may later skeletonize these frozen keyword-only dataclasses: `ResourceMathSubjectReference`, `ResourceReference`, `QuantitySpecification`, `ResourceMathDependency`, `CostTerm`, `CostBundle`, `ConsequenceTerm`, `ResourceMathRequest`, `ResourceMathResult`, and `SettlementProposal`. Common posture: `@dataclass(frozen=True, kw_only=True)`, tuple inputs copied to tuples, mapping inputs copied into `MappingProxyType`, no callable metadata, no dereference, and internal `to_dict()` returns defensive dictionaries with tuple fields represented as copied lists.

### ResourceMathSubjectReference
Fields: `subject_binding_id: str` required; `subject_type: str` required controlled by `RESOURCE_MATH_SUBJECT_TYPES`; `subject_ref_id: str` required; `subject_role: str` required controlled by `RESOURCE_MATH_SUBJECT_ROLES`; `owner_domain: str` required controlled by `RESOURCE_MATH_OWNER_DOMAINS`; `visibility_policy: str = "public"` controlled by `VISIBILITY_POLICIES`; `provenance_refs: tuple[str, ...] = ()`; `metadata: Mapping[str, object] = MappingProxyType({})`. Invariants and `to_dict()` are as sections 4, 11, and 12 define. False-only fields: none.

### ResourceReference
Fields: `resource_ref_id: str` required; `subject_binding_id: str` required; `resource_family: str` required controlled by `RESOURCE_FAMILIES`; `resource_key: str` required; `source_label: str | None = None`; `source_aliases: tuple[str, ...] = ()`; `owner_domain: str` required controlled by `RESOURCE_MATH_OWNER_DOMAINS`; `visibility_policy: str = "public"`; `unit_ref_id: str | None = None`; `dimension_ref_id: str | None = None`; `provenance_refs: tuple[str, ...] = ()`; `source_local: bool = False`; `metadata: Mapping[str, object] = MappingProxyType({})`. `validation_posture` is not a field. Invariants: subject binding exists, IDs unique, no final resource names or economies selected. False-only fields: none.

### QuantitySpecification
Fields: `quantity_id: str` required; `representation_kind: str` required controlled by `QUANTITY_REPRESENTATION_KINDS`; `magnitude_text: str | None = None`; `source_literal: str | None = None`; `precision: str | None = None`; `scale: int | None = None`; `unit_ref_id: str | None = None`; `dimension_ref_id: str | None = None`; `conversion_policy: str = "no_conversion"`; `rounding_policy: str = "no_rounding"`; `negative_value_policy: str = "negative_values_forbidden"`; `visibility_policy: str = "public"`; `provenance_refs: tuple[str, ...] = ()`; `metadata: Mapping[str, object] = MappingProxyType({})`. Invariants: section 8 lexical contract, no parsing or arithmetic. False-only fields: none.

### ResourceMathDependency
Fields: `dependency_id: str` required; `dependency_type: str` required controlled by `RESOURCE_MATH_DEPENDENCY_TYPES`; `reference_id: str` required; `owner_domain: str` required controlled by `RESOURCE_MATH_OWNER_DOMAINS`; `required: bool = True`; `satisfied: bool = False`; `hidden_info_safe: bool = True`; `metadata: Mapping[str, object] = MappingProxyType({})`. Invariants: section 6 uniqueness, binding, hidden-information, and no execution rules. False-only fields: none.

### CostTerm
Fields: `term_id: str` required; `subject_binding_id: str` required; `resource_ref_id: str | None = None`; `quantity_id: str | None = None`; `cost_family: str` required controlled by `COST_FAMILIES`; `timing_policy: str = "blocked_pending_validation"`; `outcome_policy: str = "validation_blocked"`; `visibility_policy: str = "public"`; `owner_domain: str` required; `dependency_ids: tuple[str, ...] = ()`; `provenance_refs: tuple[str, ...] = ()`; `metadata: Mapping[str, object] = MappingProxyType({})`. Invariants: referenced subject/resource/quantity/dependencies exist, no affordability check. False-only fields: none.

### CostBundle
Fields: `bundle_id: str` required; `term_ids: tuple[str, ...]` required non-empty; `atomicity_policy: str = "all_or_nothing_requested"`; `ordering_policy: str = "unordered_terms"`; `partial_settlement_policy: str = "no_partial_settlement"`; `minimum_required_terms: int | None = None`; `maximum_allowed_terms: int | None = None`; `alternative_groups: tuple[tuple[str, tuple[str, ...]], ...] = ()`; `visibility_policy: str = "public"`; `owner_domain: str` required; `dependency_ids: tuple[str, ...] = ()`; `provenance_refs: tuple[str, ...] = ()`; `metadata: Mapping[str, object] = MappingProxyType({})`. Invariants: section 9 bounds and alternatives. False-only fields: none.

### ConsequenceTerm
Fields: `consequence_id: str` required; `subject_binding_id: str` required; `resource_ref_id: str | None = None`; `quantity_id: str | None = None`; `consequence_family: str` required controlled by `CONSEQUENCE_FAMILIES`; `timing_policy: str = "blocked_pending_validation"` controlled by `COST_TIMING_POLICIES`; `outcome_policy: str = "validation_blocked"` controlled by `COST_OUTCOME_POLICIES`; `visibility_policy: str = "public"`; `owner_domain: str` required; `dependency_ids: tuple[str, ...] = ()`; `provenance_refs: tuple[str, ...] = ()`; `metadata: Mapping[str, object] = MappingProxyType({})`. `validation_posture` is not a field. Invariants: subject/resource/quantity/dependency IDs exist where supplied, no consequence application. False-only fields: none.

### ResourceMathRequest
Fields: `request_id: str` required; `command_ref_id: str | None = None`; `action_legality_ref_id: str | None = None`; `subject_refs: tuple[ResourceMathSubjectReference, ...]` required non-empty; `state_projection_ref_ids: tuple[str, ...] = ()`; `resource_refs: tuple[ResourceReference, ...] = ()`; `quantity_specs: tuple[QuantitySpecification, ...] = ()`; `cost_terms: tuple[CostTerm, ...] = ()`; `cost_bundles: tuple[CostBundle, ...] = ()`; `consequence_terms: tuple[ConsequenceTerm, ...] = ()`; `dependencies: tuple[ResourceMathDependency, ...] = ()`; `trace_ref_id: str` required; `provenance_refs: tuple[str, ...] = ()`; `owner_handoff_ref_ids: tuple[str, ...] = ()`; `validation_request_ref_id: str | None = None`; `metadata: Mapping[str, object] = MappingProxyType({})`; all false-only fields default `False`. Invariants: section 4 subject cardinality, section 10 binding, section 11 integrity, section 13 false-only rejection.

### ResourceMathResult
Fields: `result_id: str` required; `request_id: str` required; `stage: str` required; `decision: str` required; `blocking: bool` required; `quarantined: bool = False`; `escalated: bool = False`; `diagnostics: tuple[str, ...] = ()`; `normalized_reference_ids: tuple[str, ...] = ()`; `dependencies: tuple[ResourceMathDependency, ...] = ()`; `trace_ref_id: str` required; `validation_request_ref_id: str | None = None`; `validation_result_ref_id: str | None = None`; `validation_decision: str | None = None`; `metadata: Mapping[str, object] = MappingProxyType({})`; all false-only fields default `False`. Invariants: stage/decision compatibility, validation integration contract, dependency linkage, false-only rejection.

### SettlementProposal
Fields: `proposal_id: str` required; `result_id: str` required; `proposed_state_delta_refs: tuple[str, ...]` required non-empty; `validation_result_ref_id: str` required; `validation_decision: str` required and equal to `validation_passed`; `dependencies: tuple[ResourceMathDependency, ...] = ()`; `trace_ref_id: str` required; `visibility_policy: str = "public"`; `rollback_accounting_refs: tuple[str, ...] = ()`; `metadata: Mapping[str, object] = MappingProxyType({})`; all false-only fields default `False`. Invariants: non-empty unique proposed deltas, matching `state_delta_ref` dependencies, matching `validation_result_ref` dependency, non-mutating proposal, false-only rejection.

## 15. Factory/validator parity

Future helpers are required for all ten shapes: `create_resource_math_subject_reference`, `validate_resource_math_subject_reference`, `create_resource_reference`, `validate_resource_reference`, `create_quantity_specification`, `validate_quantity_specification`, `create_resource_math_dependency`, `validate_resource_math_dependency`, `create_cost_term`, `validate_cost_term`, `create_cost_bundle`, `validate_cost_bundle`, `create_consequence_term`, `validate_consequence_term`, `create_resource_math_request`, `validate_resource_math_request`, `create_resource_math_result`, `validate_resource_math_result`, `create_settlement_proposal`, and `validate_settlement_proposal`.

Shared private validation helpers must cover constants, defaults, subject typing, internal-reference integrity, external dependency linkage, decision/stage compatibility, quantity lexical rules, bundle constraints, proposal validation, false-only flags, and metadata/tuple requirements. Manual frozen-dataclass construction must not bypass those checks.

## 16. Corpus-scale and owner-pressure review

The final contracts support 200-400 donor sources across fantasy and sci-fi; cultivation; class/archetype; profession/occupation; point-buy; narrative/aspect; cyberware/biotech; psionics; horror/investigation; vehicles/mechs/ships; companions/summons; crafting/salvage/requisition; debt/faction/mission; source-local cosmologies; generated content; and persistent campaign consequences.

Lawful routes: source-local retention through `source_local_retained`; quarantine through `quarantined_for_review`; escalation through `escalated_to_doctrine`; owner handoff through `requires_owner_handoff` plus `owner_handoff_ref` dependencies. PR-5D does not finalize resource names, formulas, economies, damage, ability, inventory, mission, or social mechanics.

## 17. PR-5C closure ledger

| PR-5C blocker / prior defect | Exact PR-5D correction | Future test requirement | Closure status |
|---|---|---|---|
| Free-string validation posture on leaf shapes | Remove `validation_posture`; use `VALIDATION_INTEGRATION_DECISIONS` only on request/result/proposal | Assert absent leaf posture and owned decision surface | closed |
| Untyped subject references | Add `ResourceMathSubjectReference` and `RESOURCE_MATH_SUBJECT_ROLES` | Assert typed subject binding fields and roles | closed |
| Quarantine/escalation non-blocking mismatch | Define blocking/terminal compatibility matrix | Assert quarantine and escalation flags | closed |
| Dependency refs not structurally bound | Define exact field-binding matrix and required/satisfied rules | Assert every external ref maps to one dependency type | closed |
| Consequence defaults not tied to surfaces | Reuse `COST_TIMING_POLICIES` and `COST_OUTCOME_POLICIES` | Assert no duplicate consequence policy surface | closed |
| Quantity parsing boundary too loose | Define lexical-only validation and ban Decimal/Fraction/float/arithmetic | Assert lexical-only and no parsing authority | closed |
| Bundle bounds ambiguous | Choose declaration-bound maximum rule and bool rejection | Assert bounds and alternatives semantics | closed |
| Proposal validation linkage incomplete | Require `validation_passed`, non-empty validation result, state deltas, and typed dependencies | Assert proposal requirements | closed |
| Public serialization ownership unresolved | `to_dict()` internal only; no `to_public_dict()`; RT-005 owns public projection | Assert internal-only serialization | closed |
| Factory/validator gaps | Require create/validate parity and shared helpers for all ten shapes | Assert all helper names | closed |
| False-only authority bypass risk | Preserve all flags and reject true even on manual objects | Assert false-only fields | closed |

All PR-5C blockers are closed for PR-5E review or made irrelevant to PR-5A by explicit non-implementation boundaries. PR-5A remains blocked until PR-5E accepts this artifact.

## 18. PR-5E review boundary

Recommended next step:

**RUNTIME-DOMAIN-PR-5E: Resource and Consequence Math Final Planning Hardening Review Gate**.

PR-5E must review PR-5D before PR-5A is authorized. PR-5D authorizes only this review gate.

## 19. Gate finding

```yaml
gate_finding:
  resource_consequence_math_final_planning_hardening_defined: true
  pr_5c_blockers_addressed: true
  validation_integration_contract_defined: true
  typed_subject_identity_defined: true
  decision_stage_blocking_semantics_defined: true
  dependency_field_binding_defined: true
  consequence_policy_reuse_defined: true
  quantity_lexical_contract_defined: true
  bundle_bound_and_alternative_semantics_defined: true
  request_result_proposal_contracts_defined: true
  internal_reference_integrity_defined: true
  serialization_ownership_defined: true
  false_only_authority_contract_preserved: true
  exact_future_shape_inventory_defined: true
  factory_validator_parity_defined: true
  corpus_scale_pressure_review_complete: true
  ready_for_pr_5e_review_gate: true
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
  next_step_authorized: RUNTIME-DOMAIN-PR-5E resource and consequence math final planning hardening review gate
  next_step_status: review_gate_only
```

## 20. Non-implementation reaffirmation and classification block

PR-5D is a planning hardening artifact only. It follows PR-5C, closes the PR-5C contract defects, keeps PR-5A blocked, selects PR-5E as the sole next step, and grants no implementation authority.

```yaml
runtime_domain_pr_5d_classification:
  artifact_id: RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001
  artifact_type: final_planning_hardening
  implementation_status: planning_only
  follows_pr_5c: true
  closes_pr_5c_contract_defects: true
  pr_5a_remains_blocked: true
  pr_5e_is_sole_next_step: true
  no_implementation_authority: true
  no_runtime_or_domain_modules_modified: true
```

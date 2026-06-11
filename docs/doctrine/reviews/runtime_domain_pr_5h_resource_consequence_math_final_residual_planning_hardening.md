# RUNTIME-DOMAIN-PR-5H: Resource and Consequence Math Final Residual Planning Hardening

## 1. Purpose, status, source ledger, and authority boundary

Artifact ID: **RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001**.

This artifact is **planning-only**. It continues the existing PR-5H planning branch for PR #278, corrects the final residual contract defects found after PR-5G, implements no code, modifies no `src/` file, and authorizes exactly one next step: **RUNTIME-DOMAIN-PR-5I resource and consequence math final residual planning hardening review gate**. **PR-5A remains blocked** and is not authorized.

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

PR-5H preserves the PR-5F/PR-5G corrections for inherited constant vocabularies, donor-shaped leakage, dependency ownership, and Level A/Level B validation distinction. PR-5H does not create runtime code, domain code, factories, validators, dataclasses, parser logic, arithmetic, formula evaluation, settlement execution, state mutation, event commitment, persistence, RNG/table execution, model integration, UI behavior, conversion, sourcebook inclusion, or canon promotion.

## 2. Backend-first invariant

- The LLM is not the game engine.
- Reference objects are not calculations.
- Results are not state.
- Settlement proposals are not transactions.
- `validation_ready` is not `validation_passed`.
- No source-local declaration, donor term, or generated text grants resource authority.
- No runtime validation can promote canon.
- No field in this artifact authorizes calculation, affordability execution, reservation, settlement, consequence application, mutation, state-delta application, transaction execution, event commitment, event append, persistence, replay, RNG execution, table-oracle execution, model authority, live play, UI behavior, conversion, or canon promotion.

## 3. Final effective PR-5A field inventory and binding lifecycle

PR-5A must be able to generate future dataclass fields from this PR-5H effective contract without consulting PR-5D. Earlier PR-5 contracts remain inherited only where this section does not restate or correct them.

### 3.1 External binding lifecycle shared by all external binding fields

Every external binding field governed by the dependency lifecycle uses this exact distinction:

- Every external binding field requires exactly one matching dependency record with the correct dependency_type and reference_id.
- The matching record must always have required=True.
- satisfied=True means the binding is complete.
- satisfied=False is permitted only as an incomplete binding dependency under Section 6 state B.
- An incomplete binding remains structurally linked to its field, makes the request not resolution-ready, and forces blocked_missing_dependency for every result whose typed scope reaches it.
- A missing record, wrong dependency type, or wrong reference ID is state C and invalidates the request before result construction.
- An incomplete dependency can never support an accepted, normalized, or settlement-eligible result.

This distinction applies consistently to `ResourceMathSubjectReference.subject_ref_id`, `ResourceReference.unit_ref_id`, `ResourceReference.dimension_ref_id`, `QuantitySpecification.unit_ref_id`, `QuantitySpecification.dimension_ref_id`, and every other external binding field governed by the same lifecycle.

### 3.2 External binding field matrix

| shape | external binding field | annotation | default | matching dependency_type | matching reference_id | required flag | satisfied lifecycle |
|---|---|---|---|---|---|---|---|
| `ResourceMathSubjectReference` | `subject_ref_id` | `str` | required | `subject_ref` | field value | `required=True` | complete when `satisfied=True`; incomplete when `satisfied=False` under Section 6 state B; missing/wrong type/wrong reference is Section 6 state C |
| `ResourceReference` | `unit_ref_id` | `str \| None` | `None` | `unit_ref` | field value when non-None | `required=True` | complete when `satisfied=True`; incomplete when `satisfied=False` under Section 6 state B; missing/wrong type/wrong reference is Section 6 state C |
| `ResourceReference` | `dimension_ref_id` | `str \| None` | `None` | `dimension_ref` | field value when non-None | `required=True` | complete when `satisfied=True`; incomplete when `satisfied=False` under Section 6 state B; missing/wrong type/wrong reference is Section 6 state C |
| `QuantitySpecification` | `unit_ref_id` | `str \| None` | `None` | `unit_ref` | field value when non-None | `required=True` | complete when `satisfied=True`; incomplete when `satisfied=False` under Section 6 state B; missing/wrong type/wrong reference is Section 6 state C |
| `QuantitySpecification` | `dimension_ref_id` | `str \| None` | `None` | `dimension_ref` | field value when non-None | `required=True` | complete when `satisfied=True`; incomplete when `satisfied=False` under Section 6 state B; missing/wrong type/wrong reference is Section 6 state C |
| `ResourceMathRequest` | `validation_request_ref_id` | `str \| None` | `None` | `validation_request_ref` | field value when non-None | `required=True` | complete when `satisfied=True`; incomplete only as Section 6 state B and blocks scoped results; missing/wrong type/wrong reference is Section 6 state C |
| `ResourceMathResult` | `validation_request_ref_id` | `str \| None` | `None` | `validation_request_ref` | field value when non-None | `required=True` | complete when `satisfied=True`; incomplete only as Section 6 state B and blocks scoped results; missing/wrong type/wrong reference is Section 6 state C |
| `ResourceMathResult` | `validation_result_ref_id` | `str \| None` | `None` | `validation_result_ref` | field value when non-None | `required=True` | complete when `satisfied=True`; incomplete cannot support `validation_passed`; missing/wrong type/wrong reference is Section 6 state C |
| `SettlementProposal` | `validation_result_ref_id` | `str` | required | `validation_result_ref` | field value | `required=True` | must be complete with `satisfied=True`; incomplete is not proposal-eligible; missing/wrong type/wrong reference is invalid |
| `SettlementProposal` | `result_id` | `str` | required | `resource_math_result_ref` | field value | `required=True` | must be complete with `satisfied=True`; incomplete is not proposal-eligible; missing/wrong type/wrong reference is invalid |
| `SettlementProposal` | `request_id` | `str` | required | `resource_math_request_ref` | field value | `required=True` | must be complete with `satisfied=True`; incomplete is not proposal-eligible; missing/wrong type/wrong reference is invalid |
| `SettlementProposal` | `proposed_state_delta_refs` | `tuple[str, ...]` | required non-empty tuple | `state_delta_ref` | each tuple member | `required=True` | every member must be complete with `satisfied=True`; incomplete is not proposal-eligible; missing/wrong type/wrong reference is invalid |
| shared provenance-bearing shapes | `provenance_refs` | `tuple[str, ...]` | `()` | `provenance_ref` | each tuple member when external | `required=True` | complete when `satisfied=True`; incomplete only as Section 6 state B and blocks scoped results; missing/wrong type/wrong reference is Section 6 state C |
| owner handoff-bearing shapes | `owner_handoff_ref_id` | `str \| None` | `None` | `owner_handoff_ref` | field value when non-None | `required=True` | complete when `satisfied=True`; incomplete only as Section 6 state B and blocks scoped results; missing/wrong type/wrong reference is Section 6 state C |
| runtime trace-bearing shapes | `runtime_trace_ref_id` | `str \| None` | `None` | `runtime_trace_ref` | field value when non-None | `required=True` | complete when `satisfied=True`; incomplete only as Section 6 state B and blocks scoped results; missing/wrong type/wrong reference is Section 6 state C |
| rollback-bearing shapes | `rollback_accounting_ref_id` | `str \| None` | `None` | `rollback_accounting_ref` | field value when non-None | `required=True` | complete when `satisfied=True`; incomplete only as Section 6 state B and blocks scoped results; missing/wrong type/wrong reference is Section 6 state C |

### 3.3 Shared false-only authority surface

`FALSE_ONLY_AUTHORITY_FIELDS` is an exact shared controlled surface. Each field is annotated `bool`, defaults to `False`, and every factory and validator must reject any `True` value, including values on manually constructed frozen dataclasses.

| field | annotation | default | invariant |
|---|---|---:|---|
| `calculation_executed` | `bool` | `False` | false-only authority field |
| `affordability_executed` | `bool` | `False` | false-only authority field |
| `reservation_authorized` | `bool` | `False` | false-only authority field |
| `settlement_authorized` | `bool` | `False` | false-only authority field |
| `consequence_application_authorized` | `bool` | `False` | false-only authority field |
| `mutation_authorized` | `bool` | `False` | false-only authority field |
| `state_delta_application_authorized` | `bool` | `False` | false-only authority field |
| `transaction_execution_authorized` | `bool` | `False` | false-only authority field |
| `event_commitment_authorized` | `bool` | `False` | false-only authority field |
| `event_append_authorized` | `bool` | `False` | false-only authority field |
| `persistence_authorized` | `bool` | `False` | false-only authority field |
| `replay_authorized` | `bool` | `False` | false-only authority field |
| `rng_execution_authorized` | `bool` | `False` | false-only authority field |
| `table_oracle_execution_authorized` | `bool` | `False` | false-only authority field |
| `model_authority_authorized` | `bool` | `False` | false-only authority field |
| `live_play_authorized` | `bool` | `False` | false-only authority field |
| `ui_authorized` | `bool` | `False` | false-only authority field |
| `conversion_authorized` | `bool` | `False` | false-only authority field |
| `canon_promotion_authorized` | `bool` | `False` | false-only authority field |

Explicit inclusion rows:

| shape | included shared surface | generation rule |
|---|---|---|
| `ResourceMathRequest` | `FALSE_ONLY_AUTHORITY_FIELDS` | include all nineteen fields exactly once, each `bool = False` |
| `ResourceMathResult` | `FALSE_ONLY_AUTHORITY_FIELDS` | include all nineteen fields exactly once, each `bool = False` |
| `SettlementProposal` | `FALSE_ONLY_AUTHORITY_FIELDS` | include all nineteen fields exactly once, each `bool = False` |

No historical lookup is required to identify a PR-5A field in this shared surface.

## 4. Authoritative decision/stage compatibility matrix

PR-5H restates the complete inherited PR-5D compatibility contract after all later corrections. This is the effective matrix; the no-blocker row and every later blocker reference point here, not to an unstated historical matrix.

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

Every unlisted decision/stage combination is invalid. A decision/stage pair that is not admitted by the table cannot be rescued by flags, validation state, or dependency state. Dual use of `quarantined_for_review` and `escalated_to_doctrine` as both stage and decision is lawful only through the listed rows.

## 5. Complete blocker-precedence and no-blocker routing

The no-blocker row means: use the authoritative decision/stage compatibility matrix in Section 4; no missing dependency, incompatible policy, hidden information, owner handoff, validation review, quarantine, escalation, policy-only, blocked-numeric, or source-local blocker may be present.

| condition | required result routing | eligible for accepted/normalized planning | eligible for SettlementProposal |
|---|---|---:|---:|
| no blocker after full aggregate validation | Section 4 matrix; settlement still requires Section 7 | yes only if Section 4 admits the pair and bindings are complete | yes only if Section 7 is satisfied |
| scoped incomplete required binding dependency | `decision=blocked_missing_dependency`, `blocking=True`, stage from `MISSING_DEPENDENCY_STAGES` | no | no |
| missing binding record, wrong dependency type, or wrong reference ID | invalid request before result construction | no | no |
| policy-only term in result scope | `blocked_incompatible_policy` unless retained source-local outside result resolution | no | no |
| blocked numeric choice in result scope | `blocked_incompatible_policy`, `blocking=True` | no | no |
| hidden-information unsafe dependency in result scope | `blocked_hidden_information` or authorized RT-005 handoff route | no | no |
| owner handoff required | `requires_owner_handoff`, `blocking=True` | no | no |
| validation review required but not passed | `requires_validation_review`, `blocking=True` | no | no |
| quarantine condition | `quarantined_for_review`, `blocking=True`, `quarantined=True`, `escalated=False` | no | no |
| doctrine escalation condition | `escalated_to_doctrine`, `blocking=True`, `quarantined=False`, `escalated=True` | no | no |

## 6. Incomplete-dependency lifecycle

PR-5H uses three aggregate states for external field binding:

| state | dependency record posture | structural validity | result consequence | proposal consequence |
|---|---|---|---|---|
| A complete binding | exactly one matching record with correct `dependency_type`, correct `reference_id`, `required=True`, and `satisfied=True` | structurally valid and resolution-ready for that binding | may support lawful `accepted_for_planning` or `normalized_for_planning` only if all other rules pass | may support proposal eligibility only if Section 7 passes |
| B incomplete binding | exactly one matching record with correct `dependency_type`, correct `reference_id`, `required=True`, and `satisfied=False` | structurally valid incomplete binding; the field remains linked to the record | request is not resolution-ready; every result whose typed scope reaches it must use `decision=blocked_missing_dependency`, `blocking=True`, and a stage from `MISSING_DEPENDENCY_STAGES`; it can never support accepted or normalized results | never settlement-proposal eligible |
| C invalid binding | no matching record, wrong `dependency_type`, wrong `reference_id`, duplicate matching records, or matching record with `required=False` | invalid request before result construction | no result may be constructed | no proposal may be constructed |

State B is the only path where `satisfied=False` is permitted for a binding dependency. State B does not dereference, execute, or fill the dependency; it records an incomplete structural link. State C is not a blocker result; it is request invalidation before result construction.

## 7. SettlementProposal eligibility

A `SettlementProposal` is eligible only when the supplied `ResourceMathResult` has all of the following:

- `stage == calculation_ready_for_review`;
- `decision in {accepted_for_planning, normalized_for_planning}`;
- `blocking=False`;
- `quarantined=False`;
- `escalated=False`;
- `validation_decision == validation_passed`;
- all scoped required bindings satisfied;
- no scoped policy-only, blocked-numeric, hidden-information, owner-handoff, quarantine, escalation, or unsatisfied-dependency blocker.

Additional exact consequences:

- `normalized_for_planning` at `source_declaration_captured`, `subject_refs_bound`, `resource_refs_declared`, `quantity_specs_declared`, `terms_declared`, `bundle_structure_declared`, `policy_refs_declared`, or `dependency_refs_bound` is lawful planning state but is not settlement-proposal eligible.
- `source_local_retained` is never `SettlementProposal` eligible.
- `accepted_for_planning` at `resource_math_requested` is not `SettlementProposal` eligible.
- `accepted_for_planning` at `calculation_ready_for_review` may be settlement-proposal eligible only if every bullet above is satisfied.
- `normalized_for_planning` at `calculation_ready_for_review` may be settlement-proposal eligible only if every bullet above is satisfied.
- Any incomplete dependency under Section 6 state B prevents accepted, normalized, and proposal-eligible status for any scoped result that reaches it.

Level B aggregate validation and validation steps 3 and 6 must use this exact SettlementProposal eligibility test. Level A structural validation still only validates local shape, field types, and controlled vocabulary membership; it does not declare settlement eligibility.

## 8. Factory and validator parity

Future factories and validators must enforce the same contract on normal construction and on manually constructed frozen dataclasses. In particular:

- every `TRUE` value in `FALSE_ONLY_AUTHORITY_FIELDS` is rejected;
- every external field binding follows Section 3 and Section 6;
- every decision/stage/flag combination follows Section 4;
- every blocker route follows Section 5;
- every `SettlementProposal` follows Section 7;
- validators cannot skip checks merely because a dataclass is frozen or was not produced by a factory.

## 9. Tracking and gate decision

```yaml
gate_finding:
  artifact_id: RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001
  planning_only_status: true
  pr_5g_followed: true
  inherited_constant_vocabularies_preserved: true
  donor_shaped_leakage_correction_preserved: true
  dependency_ownership_correction_preserved: true
  level_a_level_b_validation_distinction_preserved: true
  external_binding_lifecycle_reconciled: true
  complete_decision_stage_compatibility_matrix_republished: true
  settlement_proposal_eligibility_exact: true
  false_only_authority_surface_complete: true
  pr_5a_authorized: false
  pr_5a_remains_blocked: true
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  calculation_authorized_by_this_pr: false
  affordability_execution_authorized_by_this_pr: false
  settlement_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  persistence_authorized_by_this_pr: false
  rng_execution_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
  exactly_one_next_step: true
  next_step_authorized: RUNTIME-DOMAIN-PR-5I resource and consequence math final residual planning hardening review gate
  next_step_status: review_gate_only
```

## 10. Non-implementation reaffirmation and classification block

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

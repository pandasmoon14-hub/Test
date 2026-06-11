# RUNTIME-DOMAIN-PR-5E: Resource and Consequence Math Final Planning Hardening Review Gate

Artifact ID: **RUNTIME-DOMAIN-PR-5E-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-REVIEW-001**.

## 1. Purpose, status, source ledger, and authority precedence

This artifact is a **non-executable review gate**. It independently reviews **RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001**, implements no code, and authorizes exactly one next planning path: either **RUNTIME-DOMAIN-PR-5A Resource and Consequence Math Skeleton Implementation** or **RUNTIME-DOMAIN-PR-5F Resource and Consequence Math Residual Planning Hardening**. PR-5A remains blocked until this review is accepted.

Source ledger reviewed:

- `RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001`
- `RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001`
- `RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001`
- `RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001`
- `RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001`
- `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`
- RT001 and RT003 through RT012 owner specifications
- `src/astra_runtime/domain/validation_integration.py`
- current domain and kernel skeletons, PR-5D focused tests, doctrine registry, and current decision log

Authority precedence: PR-5D overrides PR-5B where they conflict. PR-5B remains inherited only where PR-5D does not replace or contradict it. Existing RT owner specifications and the public validation-integration module remain authoritative for their owned surfaces. This review adds no runtime authority and does not modify PR-5, PR-5B, PR-5C, or PR-5D artifacts.

## 2. Backend-first invariant

Confirmed invariant:

- The LLM is not the game engine.
- References are not calculations.
- Results are not state.
- Settlement proposals are not transactions.
- `validation_ready` is not `validation_passed`.
- No narration, donor text, generated content, or source-local content has resource authority.
- Runtime validation cannot promote canon.

## 3. PR-5D scope review

PR-5D stayed within a four-file planning/tracking footprint: the PR-5D review artifact, its focused test file, registry tracking, and decision-log tracking. It made no domain or kernel implementation changes. `src/astra_runtime/domain/resource_consequence_math.py` remains absent. Registry and decision tracking consistently record PR-5D as planning-only and PR-5E as the sole next step. PR-5A remained blocked.

## 4. PR-5C blocker-closure matrix

| PR-5C defect | PR-5E finding | Reason |
|---|---|---|
| free-string validation posture | closed | PR-5D removes `validation_posture` from leaf shapes and binds validation decisions to `VALIDATION_INTEGRATION_DECISIONS`. |
| untyped subjects | closed | PR-5D adds `ResourceMathSubjectReference`, `RESOURCE_MATH_SUBJECT_ROLES`, non-empty request subjects, exactly one `primary_subject`, and internal subject bindings. |
| quarantine/escalation blocking | closed | PR-5D makes quarantine and escalation blocking terminal pairs in the stage/decision matrix. |
| dependency field binding | partially closed | PR-5D binds many external fields, but does not define dependency categories for `subject_ref_id`, `unit_ref_id`, or `dimension_ref_id`; PR-5A would have to invent bindings or exemptions. |
| consequence policy ownership | closed | PR-5D reuses `COST_TIMING_POLICIES` and `COST_OUTCOME_POLICIES` for consequence timing/outcome. |
| lexical quantity boundary | partially closed | Lexical grammars are exact, but source-literal control-character/multiline posture and precision field semantics are not exact enough for PR-5A validation without invention. |
| bundle bounds and alternatives | partially closed | Bounds, bool rejection, and alternative groups are mostly exact; remaining ambiguity exists around `maximum_allowed_terms` being required to be at least `len(term_ids)`, which makes the maximum redundant under the declaration-bound rule. |
| request/result/proposal linkage | partially closed | PR-5D binds request/result/proposal IDs to dependency types, but it does not require `SettlementProposal.validation_result_ref_id` to equal the referenced result's validation result, and it does not state whether proposals may reference blocked, quarantined, escalated, or merely `validation_ready` results. |
| settlement validation | partially closed | `validation_passed` is required, but the proposal-to-result validation equality and blocked-result exclusion rules are not exact. |
| serialization ownership | closed | PR-5D limits PR-5A to internal `to_dict()` and routes public projection to RT-005. |
| factory/validator parity | partially closed | Helper names and shared concerns are listed, but residual validator rules above would still have to be invented. |
| false-only authority | closed | PR-5D preserves the full false-only field set and requires rejection of true authority flags. |

## 5. Final constant-surface inventory

PR-5D preserves PR-5B constant surfaces and adds `RESOURCE_MATH_SUBJECT_ROLES`, `QUANTITY_NEGATIVE_VALUE_POLICIES`, and expanded `RESOURCE_MATH_DEPENDENCY_TYPES`. Defaults for validation, cost timing/outcome, visibility, conversion, rounding, quantity negative handling, atomicity, ordering, and partial settlement are tied to named governing surfaces.

Residual finding: no undefined free-string validation policy remains, and donor-specific terms do not silently become Astra law because source-local, quarantine, owner-handoff, and doctrine-escalation routes exist. However, the expanded `RESOURCE_MATH_DEPENDENCY_TYPES` surface is incomplete for future public fields that are explicitly external references: `ResourceMathSubjectReference.subject_ref_id`, `ResourceReference.unit_ref_id`, `ResourceReference.dimension_ref_id`, `QuantitySpecification.unit_ref_id`, and `QuantitySpecification.dimension_ref_id`. PR-5D does not document exact exemptions for those fields.

## 6. Stage/decision completeness review

Reviewed `RESOURCE_MATH_STAGES` and `RESOURCE_MATH_DECISIONS` as inherited from PR-5B and narrowed by PR-5D. Every listed stage has at least one lawful decision and every listed decision has at least one lawful stage through the PR-5D compatibility matrix. Every unlisted pair is invalid. Terminal stages `quarantined_for_review` and `escalated_to_doctrine` have only their terminal decisions. Quarantine and escalation are blocking. Accepted, normalized, and source-local decisions cannot masquerade as transaction readiness. `resource_math_requested` is lawfully covered by `accepted_for_planning`. The overlap for `calculation_ready_for_review` is intentional because it admits both an accepted planning marker and normalized reference-only planning markers.

Explicit semantic checks:

- `accepted_for_planning` at `resource_math_requested` is semantically safe as a request-acceptance marker only, not calculation readiness.
- `normalized_for_planning` at `calculation_ready_for_review` is compatible with `accepted_for_planning` because both remain non-executing planning decisions; neither creates validation-passed, settlement, transaction, or mutation authority.
- `required=False` and `satisfied=False` dependencies can coexist with non-blocking results only when they do not satisfy required field bindings and are not used to bypass required/satisfied dependencies.

Residual finding: stage/decision semantics are broadly adequate, but the dependency-state ambiguity above remains a validator-invention risk when optional unsatisfied dependencies coexist with fields that still lack typed dependency categories.

## 7. Validation-integration review

The actual public validation-integration surface defines `VALIDATION_INTEGRATION_DECISIONS` including `validation_ready`, `validation_passed`, `validation_failed`, failure rejections, `quarantined_for_review`, `escalated_to_doctrine`, and `unsupported_validation_scope`. PR-5D does not create duplicate validation vocabulary. Result validation fields have exact co-presence rules: `validation_decision is None` forbids validation request/result refs; non-None decisions require a validation request ref; `validation_ready` may omit a result reference; non-ready decisions require a result reference. `SettlementProposal` requires `validation_passed`, typed validation-result dependencies are required, and no validation field grants calculation, settlement, or mutation authority.

Residual finding: PR-5D still needs a same-result linkage rule for proposals because `SettlementProposal.validation_result_ref_id` can otherwise be syntactically valid while not matching the referenced `ResourceMathResult.validation_result_ref_id`.

## 8. Typed-subject review

PR-5D defines exact `ResourceMathSubjectReference` fields: `subject_binding_id`, `subject_type`, `subject_ref_id`, `subject_role`, `owner_domain`, `visibility_policy`, `provenance_refs`, and `metadata`. Subject roles are exactly `primary_subject`, `payer_subject`, `beneficiary_subject`, `resource_owner`, `affected_subject`, `source_subject`, `target_subject`, `authority_source`, and `provenance_source`. Subject type and owner domain are controlled by `RESOURCE_MATH_SUBJECT_TYPES` and `RESOURCE_MATH_OWNER_DOMAINS`.

Request-level rules require non-empty `subject_refs`, exactly one `primary_subject`, unique subject-binding IDs, and internal resolution for all resource, cost, and consequence subject bindings. cross-subject costs and consequences remain lawful through explicit subject bindings. No object dereferencing is implied.

Residual finding: `subject_ref_id` is described as an external or upstream subject reference, but no `subject_ref` dependency type or documented exemption exists.

## 9. External-reference/dependency completeness review

External reference field mapping reviewed across all ten future shapes:

| field or field family | PR-5D dependency type | PR-5E finding |
|---|---|---|
| `ResourceMathSubjectReference.subject_ref_id` | none | blocker: needs `subject_ref` type or exact exemption. |
| `ResourceMathSubjectReference.provenance_refs` | `provenance_ref` | acceptable. |
| `ResourceReference.unit_ref_id` | none | blocker: needs `unit_ref` type or exact exemption. |
| `ResourceReference.dimension_ref_id` | none | blocker: needs `dimension_ref` type or exact exemption. |
| `ResourceReference.provenance_refs` | `provenance_ref` | acceptable. |
| `QuantitySpecification.unit_ref_id` | none | blocker: needs `unit_ref` type or exact exemption. |
| `QuantitySpecification.dimension_ref_id` | none | blocker: needs `dimension_ref` type or exact exemption. |
| `QuantitySpecification.provenance_refs` | `provenance_ref` | acceptable. |
| `CostTerm.provenance_refs` and `ConsequenceTerm.provenance_refs` | `provenance_ref` | acceptable. |
| `CostBundle.provenance_refs` | `provenance_ref` | acceptable. |
| `ResourceMathRequest.command_ref_id` | `command_ref` | acceptable. |
| `ResourceMathRequest.action_legality_ref_id` | `action_legality_ref` | acceptable. |
| `ResourceMathRequest.state_projection_ref_ids` | `state_projection_ref` | acceptable. |
| `ResourceMathRequest.trace_ref_id` | `runtime_trace_ref` | acceptable. |
| `ResourceMathRequest.provenance_refs` | `provenance_ref` | acceptable. |
| `ResourceMathRequest.owner_handoff_ref_ids` | `owner_handoff_ref` | acceptable. |
| `ResourceMathRequest.validation_request_ref_id` | `validation_request_ref` | acceptable. |
| command/action/state refs | `command_ref`, `action_legality_ref`, `state_projection_ref` | acceptable. |
| validation refs | `validation_request_ref`, `validation_result_ref` | acceptable. |
| trace refs | `runtime_trace_ref` | acceptable. |
| owner handoff refs | `owner_handoff_ref` | acceptable. |
| RNG/table refs | `rng_result_ref`, `table_oracle_result_ref` | acceptable as dependency records. |
| `ResourceMathResult.request_id` | `resource_math_request_ref` | acceptable as result-to-request external binding. |
| `ResourceMathResult.trace_ref_id` | `runtime_trace_ref` | acceptable. |
| `SettlementProposal.result_id` | `resource_math_result_ref` | acceptable as proposal-to-result external binding. |
| `SettlementProposal.proposed_state_delta_refs` | `state_delta_ref` | acceptable as proposed state-delta refs, subject to event-only concern below. |
| transaction/event prerequisites | `transaction_ref`, `event_commitment_ref` | acceptable as dependency records. |
| `SettlementProposal.rollback_accounting_refs` | `rollback_accounting_ref` | acceptable. |

Missing typed categories `subject_ref`, `unit_ref`, and `dimension_ref` are required before PR-5A unless PR-5F creates exact documented exemptions. No exact exemption currently exists. PR-5A must not invent how an external reference is bound.

## 10. Dependency-state review

PR-5D requires unique dependency IDs and unique `(dependency_type, reference_id)` pairs. Field-binding dependencies must be `required=True` and `satisfied=True`. `required=True` plus `satisfied=False` forces a blocking result. `required=False` plus `satisfied=False` is lawful but cannot satisfy a required field binding. `hidden_info_safe=False` prohibits public projection and requires RT-005 handling. Requests can represent incomplete dependencies without executing anything; result decisions must reflect readiness; no dependency is dereferenced or executed.

Residual finding: optional unsatisfied dependencies are safe only for dependency types not required by present fields. Because subject/unit/dimension external refs lack typed binding categories or exemptions, PR-5A would have to invent whether those fields are required/satisfied dependencies, optional dependencies, or non-dependency local labels.

## 11. Quantity contract review

Reviewed exact lexical-only behavior:

- `integer_exact`: full-string ASCII integer grammar, optional plus/minus, no whitespace, no exponent, no decimal point, no leading zeros except `0`.
- `decimal_exact`: full-string decimal grammar, optional plus/minus, required digits before and after `.`, no exponent, no leading decimal point, no trailing decimal point, no leading zero except before `.`.
- `fraction_exact`: full-string numerator/denominator grammar, optional sign on numerator only, no zero denominator, no signed denominator, no decimals, no mixed-number shorthand.
- `fixed_point_scaled`: integer lexical magnitude plus non-bool non-negative integer scale, no decimal point, no exponent, no negative scale.
- `source_literal_only`: non-empty source literal with no leading/trailing whitespace and no evaluation.
- `blocked_pending_numeric_choice`: non-empty source literal with no leading/trailing whitespace and a blocking planning result.

PR-5D forbids `Decimal`, `Fraction`, `float`, arithmetic, rounding, conversion, and affordability checks. Plus signs are allowed only by grammar. Negative sign compatibility is routed through `QUANTITY_NEGATIVE_VALUE_POLICIES`: `negative_values_forbidden`, `negative_values_allowed_by_source`, and `negative_values_require_owner_handoff`. Unit/dimension co-presence is planned but not fully bound to dependency categories.

Residual findings requiring PR-5F: precision field semantics are not exact; control-character and multiline posture for `source_literal_only` and `blocked_pending_numeric_choice` is not exact because `.*` leaves newline/control handling to validator implementation; unit/dimension external refs need typed binding categories; blocked numeric choices must be explicitly tied to a blocking result decision in the stage/decision matrix rather than only stated as “blocks progression.”

## 12. CostTerm and ConsequenceTerm review

Subject/resource/quantity/dependency linkage is mostly exact: subject bindings, resource refs, quantity IDs, and dependency IDs must resolve internally where supplied. Cost family, consequence family, owner-domain membership, timing policy membership, and outcome policy membership are controlled by named surfaces. Consequences lawfully reuse `COST_TIMING_POLICIES` and `COST_OUTCOME_POLICIES`; defaults `blocked_pending_validation` and `validation_blocked` are valid. Optional resource/quantity combinations are non-executing references and do not calculate affordability or apply consequences.

Residual finding: PR-5D does not state an exact rule for whether both `resource_ref_id` and `quantity_id` may be absent, whether one requires the other, or which consequence/cost families permit event-only or policy-only terms. PR-5A would have to invent optional resource/quantity combination rules.

## 13. CostBundle review

PR-5D verifies term uniqueness, positive integer-or-None min/max types, bool rejection, declared-term counting semantics, alternative-group identity, group membership, overlap prohibition unless future policy authorizes it, and a compatibility matrix that marks each listed atomicity/ordering/partial-settlement combination as lawful, blocking, or invalid. Every unlisted combination is invalid. No alternative selection or settlement occurs.

Residual finding: `maximum_allowed_terms` is meaningful only as a declaration-bound ceiling, but PR-5D requires it not be below `len(term_ids)`, so for a validated bundle it cannot constrain declared membership differently from the already-declared term count. This is not executable arithmetic, but it is a shape/vocabulary ambiguity that PR-5F should clarify as either intentional redundancy or a revised declaration rule before PR-5A.

## 14. Request/result/proposal linkage review

`ResourceMathRequest` exact contract: required `request_id`, subject cardinality, internal records, external dependencies, trace, provenance, owner handoffs, optional validation request, and false-only fields.

`ResourceMathResult` exact contract: result identity, request binding, stage/decision flags, validation co-presence, trace, diagnostics, normalized references, dependencies, and false-only fields.

`SettlementProposal` exact contract: proposal identity, result binding, non-empty unique state-delta refs, `validation_passed`, validation-result dependency, trace dependency, rollback-accounting dependencies, visibility, metadata, and false-only fields.

Explicit linkage findings:

- `SettlementProposal.validation_result_ref_id` should be required to equal the referenced result's `validation_result_ref_id`, but PR-5D does not say so.
- A proposal must not reference a result that is blocked, quarantined, escalated, or merely `validation_ready`; PR-5D implies validation-passed is needed but does not state the result-stage/result-decision exclusion rule.
- Non-empty state-delta refs may overconstrain lawful event-only consequences if an event-only consequence is represented by event commitment without a state-delta ref; PR-5D does not decide whether every settlement proposal must propose at least one state delta or whether event-only proposal shapes are deferred.
- These are PR-5A shape defects because PR-5A validators would otherwise invent proposal linkage rules. Object dereference execution remains deferred.

## 15. Internal-reference integrity review

PR-5D requires all declared internal IDs to be unique, every same-aggregate reference to resolve, bundle terms to resolve, dependency IDs used by records to resolve, unresolved internal references to be rejected, and external lookups to remain forbidden. This portion is acceptable for PR-5A once external binding residuals are addressed.

## 16. Serialization and hidden-information review

PR-5A would implement internal `to_dict()` only and no `to_public_dict()`. Defensive copies are required; no calculations occur during serialization. RT-005 owns all public, model, player, and GM projections. Hidden quantities, source literals, dependencies, provenance, and backend IDs cannot leak through resource-math serialization.

## 17. False-only authority review

Complete false-only field set reviewed: `calculation_executed`, `affordability_executed`, `reservation_authorized`, `settlement_authorized`, `consequence_application_authorized`, `mutation_authorized`, `state_delta_application_authorized`, `transaction_execution_authorized`, `event_commitment_authorized`, `event_append_authorized`, `persistence_authorized`, `replay_authorized`, `rng_execution_authorized`, `table_oracle_execution_authorized`, `model_authority_authorized`, `live_play_authorized`, `ui_authorized`, `conversion_authorized`, and `canon_promotion_authorized`.

Placement on request, result, and proposal shapes is preserved through “all false-only fields default `False`.” manually constructed objects with any true authority flag must be rejected. Duplication risk exists because the same envelope is repeated across shapes, but PR-5E does not redesign it and does not treat that duplication as a PR-5F blocker.

## 18. Factory/validator parity review

PR-5D requires exact future create/validate helpers for all ten shapes: `ResourceMathSubjectReference`, `ResourceReference`, `QuantitySpecification`, `ResourceMathDependency`, `CostTerm`, `CostBundle`, `ConsequenceTerm`, `ResourceMathRequest`, `ResourceMathResult`, and `SettlementProposal`. Shared validation helpers can enforce constants, subject cardinality, internal refs, dependency bindings, decision/stage compatibility, quantity lexical rules, bundle compatibility, settlement proposal rules, false-only flags, tuple immutability, and metadata immutability.

Residual finding: helper parity is named, but PR-5A cannot complete validators without PR-5F resolving subject/unit/dimension dependency bindings, precision/source-literal lexical details, optional term resource/quantity combinations, and proposal-to-result linkage.

## 19. Corpus-scale and owner-boundary review

Pressure tested against fantasy and sci-fi; cultivation; class/archetype; profession/occupation; point-buy; narrative/aspect; cyberware/biotech; psionics; horror/investigation; vehicles/mechs/ships; companions/summons; crafting/salvage/requisition; faction/debt/mission; source-local cosmologies; generated content; and persistent campaign consequences.

RT-002 does not absorb combat, ability, inventory, mission, faction, hidden-information, RNG, persistence, or canon ownership. Residual PR-5F corrections are shape/linkage hardening only and do not authorize those domains or executable behavior.

## 20. Risk and adversarial review

| Risk | Severity | Current mitigation | Required before PR-5A | Required before executable calculation | Owner | PR-5F required |
|---|---|---|---|---|---|---|
| orphan stage or decision | medium | PR-5D compatibility matrix | no further action if matrix retained | executable result machine later | RT-002 | false |
| overlapping decisions create ambiguity | medium | exact allowed-stage sets | no further action for `calculation_ready_for_review` overlap | executable result progression later | RT-002 | false |
| free-string policy survives | low | validation posture removed and owned surfaces named | no further action | validation execution later | RT-002/RT-011 | false |
| external subject/unit/dimension references lack typed bindings | high | some dependency types expanded | add `subject_ref`, `unit_ref`, `dimension_ref` or exact exemptions | dereference/lookup still deferred | RT-002 | true |
| optional unsatisfied dependencies incorrectly allow acceptance | high | required/satisfied rules exist | tie missing external categories to required/satisfied rules | readiness execution later | RT-002 | true |
| negative magnitude conflicts with negative-value policy | medium | negative policy surface exists | define exact validator response for negative text under forbidden/owner-handoff policies | numeric execution later | RT-002 | true |
| precision remains undefined | medium | precision field exists | define allowed precision values or exact metadata-only rule | arithmetic precision later | RT-002 | true |
| bundle bounds are contradictory or redundant | medium | declaration-bound rule exists | clarify `maximum_allowed_terms` redundancy or revise rule | settlement selection later | RT-002 | true |
| `validation_ready` reaches `SettlementProposal` | high | proposal requires `validation_passed` | explicitly reject proposals from merely validation-ready results | settlement execution later | RT-002/RT-011 | true |
| proposal references a blocked result | high | blocking flags exist | explicitly forbid blocked/quarantined/escalated result linkage | settlement execution later | RT-002 | true |
| event-only consequences cannot produce a proposal | medium | state-delta refs required | decide whether event-only proposals are invalid or need a separate reference route | event commitment later | RT-002/RT-003/RT-001 | true |
| hidden source literals leak | high | RT-005 projection ownership and internal-only `to_dict()` | no further action for skeleton | public projection implementation later | RT-005 | false |
| PR-5A must invent a validator rule | high | many rules named | resolve residual shape/linkage rules in PR-5F | executable validators later | RT-002 | true |
| false-only authority fields drift | medium | complete field set named | no redesign; tests must assert full set | runtime execution never by PR-5A | RT-002 | false |
| donor categories become core law | medium | source-local/quarantine/escalation routes | no further action for skeleton | corpus conversion later | RT-002/RT-012 | false |

## 21. Hardening ledger

| Issue | Classification | Owner | PR-5F correction |
|---|---|---|---|
| PR-5D review-only scope | closed for PR-5A | RT-002 | none. |
| Backend-first invariant | closed for PR-5A | all RT owners | none. |
| Validation vocabulary ownership | closed for PR-5A | RT-011/RT-002 | none except proposal-result equality below. |
| Subject/unit/dimension external refs have no dependency type or exemption | PR-5F blocker | RT-002 | add `subject_ref`, `unit_ref`, `dimension_ref` dependency types or exact documented exemptions. |
| Optional unsatisfied dependencies can coexist with missing required categories | PR-5F blocker | RT-002 | bind new/exempted categories to required/satisfied rules. |
| Precision field semantics undefined | PR-5F blocker | RT-002 | define exact allowed values, metadata-only posture, or forbidden posture. |
| Source-literal control-character and multiline posture | PR-5F blocker | RT-002/RT-005 | define exact acceptance/rejection rule. |
| Negative magnitude plus negative-value policy validator response | PR-5F blocker | RT-002 | define exact behavior for forbidden, allowed-by-source, and owner-handoff policies. |
| Optional resource/quantity combinations on CostTerm and ConsequenceTerm | PR-5F blocker | RT-002 | define absent/both/pairing rules or per-family deferral rule. |
| `maximum_allowed_terms` declaration-bound redundancy | PR-5F blocker | RT-002 | clarify intentional redundancy or revise maximum rule. |
| Proposal validation-result equality with referenced result | PR-5F blocker | RT-002/RT-011 | require equality or exact documented non-dereference exception. |
| Proposal references blocked/quarantined/escalated/validation-ready result | PR-5F blocker | RT-002 | define exact rejection rule. |
| Event-only consequence proposal shape | PR-5F blocker | RT-002/RT-001/RT-003 | decide state-delta requirement or event-only route. |
| Arithmetic, conversion, formulas, affordability | required before executable calculation | RT-002 and downstream owners | not PR-5A. |
| Settlement/commitment execution | required before settlement/commitment | RT-001/RT-002/RT-003 | not PR-5A. |
| Public/model/player/GM projection | deferred to a named RT owner | RT-005 | not PR-5A. |
| Canon promotion | doctrine escalation | RT-012 | not PR-5A. |

## 22. Gate decision

PR-5E selects **HARDENING**. PR-5F is required before PR-5A because residual shape, vocabulary, compatibility, linkage, and validator-authority defects would force PR-5A to invent behavior. This decision is not based on deferred arithmetic, dereferencing, settlement execution, persistence, or other executable behavior.

```yaml
gate_finding:
  resource_consequence_math_final_planning_review_complete: true
  pr_5d_scope_confirmed: true
  pr_5c_blockers_closed: partially
  constant_surfaces_acceptable: partially
  stage_decision_matrix_complete: partially
  validation_integration_contract_acceptable: true
  typed_subject_contract_acceptable: true
  external_dependency_binding_complete: false
  dependency_state_contract_acceptable: partially
  quantity_contract_acceptable: partially
  term_and_bundle_contracts_acceptable: partially
  request_result_proposal_linkage_acceptable: partially
  settlement_proposal_boundary_acceptable: partially
  internal_reference_integrity_acceptable: true
  serialization_boundary_acceptable: true
  false_only_authority_contract_acceptable: true
  factory_validator_parity_acceptable: partially
  corpus_scale_pressure_acceptable: true
  rt_002_owner_boundary_preserved: true
  requires_pr_5f_before_pr_5a: true
  ready_for_pr_5a_skeleton_implementation: false
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-5F resource and consequence math residual planning hardening
  next_step_status: planning_hardening_pending_review
```

## 23. Recommended next PR

Recommended next PR: **RUNTIME-DOMAIN-PR-5F Resource and Consequence Math Residual Planning Hardening** (RUNTIME-DOMAIN-PR-5F resource and consequence math residual planning hardening).

Required corrections, without implementing them:

1. Add exact `subject_ref`, `unit_ref`, and `dimension_ref` dependency types or exact documented exemptions.
2. Bind those categories/exemptions to required/satisfied/optional dependency-state rules.
3. Define exact precision semantics.
4. Define exact source-literal control-character and multiline posture.
5. Define exact negative magnitude behavior under every `QUANTITY_NEGATIVE_VALUE_POLICIES` value.
6. Define optional resource/quantity pairing rules for `CostTerm` and `ConsequenceTerm`.
7. Clarify whether `maximum_allowed_terms` is intentionally redundant under the declaration-bound rule or revise the rule.
8. Require or explicitly exempt equality between `SettlementProposal.validation_result_ref_id` and the referenced result's validation result reference.
9. State whether a proposal may reference a blocked, quarantined, escalated, or merely `validation_ready` result; PR-5E finding is that it should not.
10. Decide whether non-empty state-delta refs intentionally exclude event-only consequence proposals or whether a separate event-only proposal route is required.

## 24. Non-implementation reaffirmation and classification block

PR-5E is a review-only gate. It creates no runtime or domain implementation, no formulas or evaluators, no schemas or persistence structures, no model/prompt/UI/live-play behavior, and no `src/astra_runtime/domain/resource_consequence_math.py`. It authorizes PR-5F residual planning hardening only.

```yaml
runtime_domain_pr_5e_classification:
  artifact_id: RUNTIME-DOMAIN-PR-5E-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-REVIEW-001
  artifact_type: final_planning_hardening_review_gate
  implementation_status: non_executable_review_only
  reviews_pr_5d: true
  chooses_exactly_one_next_step: true
  selected_path: HARDENING
  requires_pr_5f_before_pr_5a: true
  pr_5a_authorized: false
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

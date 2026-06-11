# RUNTIME-DOMAIN-PR-5F: Resource and Consequence Math Residual Planning Hardening

Artifact ID: **RUNTIME-DOMAIN-PR-5F-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-001**.

## 1. Purpose, status, source ledger, and precedence

PR-5F is **planning-only** hardening. It follows **RUNTIME-DOMAIN-PR-5E-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-REVIEW-001**, closes PR-5E residual blockers, implements no code, and authorizes only **RUNTIME-DOMAIN-PR-5G Resource and Consequence Math Residual Planning Hardening Review Gate**. PR-5A remains blocked until PR-5G accepts this residual hardening.

Source ledger reviewed and inherited where not replaced:

- `RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001`
- `RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001`
- `RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001`
- `RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001`
- `RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001`
- `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`
- RT001 and RT003 through RT012 owner specifications
- `src/astra_runtime/domain/validation_integration.py`
- `src/astra_runtime/domain/transaction_lifecycle.py`
- `src/astra_runtime/domain/event_commitment.py`
- current domain and kernel skeletons, doctrine registry, and current decision log

PR-5F overrides PR-5D only for the corrections explicitly defined here. PR-5D and PR-5B remain inherited where PR-5F does not replace them. PR-5F does not edit PR-5 through PR-5E artifacts and adds no runtime/domain implementation.

## 2. Backend-first invariant

The backend-first invariant is mandatory:

- The LLM is not the game engine.
- References are not calculations.
- Results are not state.
- Settlement proposals are not transactions.
- `validation_ready` is not `validation_passed`.
- No resource change occurs because a record exists.
- No donor term, source-local construct, generated content, narration, or UI text has resource authority.
- No canon promotion is authorized.

## 3. PR-5E blocker-closure matrix

| PR-5E defect | exact PR-5F correction | affected future shape | future validator rule | future test requirement | closure status |
|---|---|---|---|---|---|
| missing subject_ref dependency binding | Add `subject_ref` to `RESOURCE_MATH_DEPENDENCY_TYPES`; every `ResourceMathSubjectReference.subject_ref_id` has exactly one required/satisfied binding dependency. | `ResourceMathSubjectReference`, `ResourceMathRequest` | Aggregate request validation enforces one typed binding and uniqueness by dependency id and `(dependency_type, reference_id)`. | Assert `subject_ref` appears and aggregate binding language is present. | closed |
| missing unit_ref dependency binding | Add `unit_ref`; every non-None `ResourceReference.unit_ref_id` and `QuantitySpecification.unit_ref_id` has exactly one required/satisfied binding. | `ResourceReference`, `QuantitySpecification`, `ResourceMathRequest` | Aggregate request validation rejects missing, duplicate, optional, or unsatisfied unit bindings. | Assert both unit fields and `unit_ref` dependency requirements. | closed |
| missing dimension_ref dependency binding | Add `dimension_ref`; every non-None `ResourceReference.dimension_ref_id` and `QuantitySpecification.dimension_ref_id` has exactly one required/satisfied binding. | `ResourceReference`, `QuantitySpecification`, `ResourceMathRequest` | Aggregate request validation rejects missing, duplicate, optional, or unsatisfied dimension bindings. | Assert both dimension fields and `dimension_ref` dependency requirements. | closed |
| optional-unsatisfied dependency semantics | Define advisory-only optional unsatisfied dependencies and forbid them from satisfying any binding or named dependency. | `ResourceMathDependency`, all aggregates | Binding or named dependencies must be `required=True` and `satisfied=True`; required unsatisfied dependencies force `blocked_missing_dependency`. | Assert advisory-only conditions and blocked missing dependency outcome. | closed |
| precision semantics | Replace free-string precision with `precision: int \| None = None`; only positive non-bool integer precision for `decimal_exact`; no comparison or rounding. | `QuantitySpecification` | Reject bool, non-positive, or non-decimal precision; preserve scale contract. | Assert exact precision/scale rules. | closed |
| source-literal control-character and multiline posture | Source literals must be non-empty single-line strings without edge whitespace, Cc controls, Cs surrogates, CR, LF, tab, or NUL. | `QuantitySpecification` | Reject forbidden characters and preserve lawful ordinary Unicode exactly without normalization. | Assert single-line/control-character contract. | closed |
| negative-value-policy behavior | Define lexical negativity by leading `-`, including `-0`, `-0.0`, and `-0/1`; specify forbidden, source-supported, and owner-handoff outcomes. | `QuantitySpecification`, `ResourceMathResult`, `SettlementProposal` | Reject forbidden negatives; require provenance dependencies for source-supported negatives; aggregate result validation receives the supplied request, derives typed scoped quantities, and requires owner handoff result routes for scoped owner-handoff negatives. | Assert lexical `-0`, result/request aggregate contract, and each policy result. | closed |
| blocked-pending-numeric-choice result behavior | Force scoped blocked numeric choices to `decision=blocked_incompatible_policy`, `stage=policy_refs_declared`, `blocking=True`, unless terminal quarantine/escalation applies. | `QuantitySpecification`, `ResourceMathResult` | Aggregate result validation receives the supplied request, derives typed scoped quantities, and rejects accepted, normalized, source-local, or proposal use of blocked numeric choices. | Assert result/request aggregate contract, result rule, and barred destinations. | closed |
| CostTerm resource/quantity combinations | Add required `value_mode` and exact co-presence matrix. | `CostTerm` | Validate `resource_quantity`, `resource_reference_only`, `quantity_only`, and `policy_only` co-presence and internal references. | Assert value modes and matrix. | closed |
| ConsequenceTerm resource/quantity combinations | Add required `value_mode` and exact co-presence matrix, including policy-only routing for non-pool consequences. | `ConsequenceTerm` | Validate co-presence; require owner handoff, quarantine, or escalation for unusual/source-local policy-only terms. | Assert value modes, matrix, and event-only route. | closed |
| maximum_allowed_terms semantics | Replace declaration-count minimum rule with selection-policy bounds capped by `len(term_ids)`. | `CostBundle` | Positive non-bool bounds; min/max <= len; min <= max; all-or-nothing bounds None or equal len. | Assert corrected max rule. | closed |
| proposal validation-result equality | Require proposal validation result and decision to equal the supplied result's fields. | `SettlementProposal`, `ResourceMathResult` | Validate `proposal.validation_result_ref_id == result.validation_result_ref_id` and `proposal.validation_decision == result.validation_decision`. | Assert equality language. | closed |
| proposal result eligibility | Proposals are only constructed/validated with a supplied eligible result object that is passed, non-blocking, non-quarantined, non-escalated, calculation-ready, and accepted/normalized. | `SettlementProposal`, `ResourceMathResult` | Reject `validation_ready`, failed, blocked, quarantined, escalated, source-local-only, handoff, review, or missing-dependency results. | Assert eligibility and rejection list. | closed |
| event-only consequence routing | Event-only consequences remain `ConsequenceTerm(value_mode=policy_only)` and route to another owner; no settlement proposal or event shape is created by RT-002. | `ConsequenceTerm`, `SettlementProposal` | Reject empty state-delta proposals; route event-only through owner handoff/quarantine/escalation. | Assert event-only owner-handoff route and no proposed-event shape. | closed |
| result request/quantity aggregate validation | PR-5D result fields did not define how a result inspects request quantities or policy-only terms. | `ResourceMathResult`, `ResourceMathRequest` | Result factories and validators receive the supplied request, require request-id equality and request dependency binding, derive typed scope from explicit typed reference fields, and enforce missing-dependency, blocked numeric, negative owner-handoff, and policy-only routing rules. | Assert result/request aggregate signatures, typed scope fields, scope derivation, and precedence. | closed |
| factory/validator parity | Require shared private helpers for every residual rule and identical factory/validator enforcement. | all ten inherited shapes | Manual construction of frozen dataclasses must not bypass validators. | Assert helper list and parity language. | closed |

All PR-5E residual rows are closed for PR-5A planning purposes; none are left for PR-5A invention.

## 4. External reference dependency completion

The exact future `RESOURCE_MATH_DEPENDENCY_TYPES` surface preserves PR-5D's existing dependency types and extends them with `subject_ref`, `unit_ref`, and `dimension_ref`:

- `command_ref`
- `action_legality_ref`
- `state_projection_ref`
- `validation_request_ref`
- `validation_result_ref`
- `runtime_trace_ref`
- `owner_handoff_ref`
- `provenance_ref`
- `rng_result_ref`
- `table_oracle_result_ref`
- `state_delta_ref`
- `transaction_ref`
- `event_commitment_ref`
- `resource_math_request_ref`
- `resource_math_result_ref`
- `rollback_accounting_ref`
- `subject_ref`
- `unit_ref`
- `dimension_ref`

Exact aggregate bindings:

- every `ResourceMathSubjectReference.subject_ref_id`: exactly one `subject_ref` dependency;
- every non-None `ResourceReference.unit_ref_id`: exactly one `unit_ref` dependency;
- every non-None `ResourceReference.dimension_ref_id`: exactly one `dimension_ref` dependency;
- every non-None `QuantitySpecification.unit_ref_id`: exactly one `unit_ref` dependency;
- every non-None `QuantitySpecification.dimension_ref_id`: exactly one `dimension_ref` dependency.

These dependencies live in the enclosing `ResourceMathRequest.dependencies` aggregate. Standalone leaf validators validate only field shape and controlled vocabulary. The aggregate `ResourceMathRequest` validator enforces external typed bindings. Binding dependencies must be `required=True`, `satisfied=True`, unique by `dependency_id`, unique by `(dependency_type, reference_id)`, non-empty, and hidden-information safe for any public-facing later projection. No dependency is dereferenced, looked up, or executed.

## 5. Optional and unsatisfied dependency semantics

Exact future behavior:

- Any dependency matching an external field is a binding dependency and must be `required=True` and `satisfied=True`.
- Any dependency ID named by a term, request field, result field, or proposal field is binding and must be `required=True` and `satisfied=True`.
- `required=True` plus `satisfied=False` forces `decision=blocked_missing_dependency`, `blocking=True`, and a lawful stage from `MISSING_DEPENDENCY_STAGES`.
- `required=False` plus `satisfied=False` is lawful only when no field is bound to it, no internal record names its `dependency_id`, and it is advisory only.
- Advisory optional-unsatisfied dependencies may coexist with a non-blocking result because they satisfy no required field or policy.
- An optional or unsatisfied dependency may never satisfy a required binding.
- `hidden_info_safe=False` requires `blocked_hidden_information` or an RT-005 owner handoff before public projection.
- Factories and validators must reject contradictory dependency states.

## 6. Quantity precision contract

Future `QuantitySpecification` replaces any free-string precision field with:

```python
precision: int | None = None
```

Rules:

- `bool` is rejected.
- Supplied precision must be a positive integer.
- Precision is permitted only when `representation_kind == decimal_exact`.
- Precision must be `None` for `integer_exact`, `fraction_exact`, `fixed_point_scaled`, `source_literal_only`, and `blocked_pending_numeric_choice`.
- Precision is declaration metadata only.
- PR-5A does not compare precision to `magnitude_text`.
- PR-5A does not round, truncate, parse, or calculate.
- Executable precision enforcement remains deferred to future numeric doctrine.

Preserved scale rules: `scale: int | None`; `fixed_point_scaled` requires non-bool, non-negative scale; every other representation requires `scale=None`.

## 7. Source-literal character contract

For `source_literal_only` and `blocked_pending_numeric_choice`:

- `source_literal` must be a non-empty `str`.
- Leading or trailing whitespace is rejected.
- Multiline values are rejected.
- Reject carriage return, line feed, tab, NUL, Unicode control characters in category `Cc`, and Unicode surrogate characters in category `Cs`.
- Ordinary Unicode letters, numbers, punctuation, symbols, and spaces are permitted.
- `source_literal` is preserved exactly.
- No normalization, tokenization, parsing, arithmetic, or evaluation occurs.
- `source_literal` remains internal-only and cannot be publicly projected by RT-002.

Numeric `magnitude_text` continues to use the exact ASCII grammars from PR-5D.

## 8. Negative-value policy contract

Preserve exact future `QUANTITY_NEGATIVE_VALUE_POLICIES`:

- `negative_values_forbidden`
- `negative_values_allowed_by_source`
- `negative_values_require_owner_handoff`

A lexical value is negative when its accepted numeric grammar begins with `-`. Because PR-5A performs no arithmetic, `-0`, `-0.0`, and `-0/1` are lexically negative; a leading `+` is not negative.

Rules:

`negative_values_forbidden` rejects any lexically negative `magnitude_text`.

`negative_values_allowed_by_source` allows a negative magnitude only when `source_literal` is non-empty, `provenance_refs` is non-empty, and every provenance reference has a required/satisfied `provenance_ref` dependency.

`negative_values_require_owner_handoff` means the quantity may be represented, but any `ResourceMathResult` that references it must use `decision=requires_owner_handoff`, `stage=blocked_pending_owner_handoff`, and `blocking=True`; at least one matching required/satisfied `owner_handoff_ref` dependency is required; it cannot appear in `accepted_for_planning`, `normalized_for_planning`, or a `SettlementProposal`.

Positive lexical quantities do not trigger these negative-policy restrictions.

## 9. Blocked numeric choice contract

Any `QuantitySpecification` with `representation_kind == blocked_pending_numeric_choice` must force any `ResourceMathResult` referencing it to:

- `decision=blocked_incompatible_policy`;
- `stage=policy_refs_declared`;
- `blocking=True`;
- `quarantined=False`;
- `escalated=False`.

It may instead be quarantined or escalated only through the already lawful terminal quarantine/escalation pairs. It may not appear in `accepted_for_planning`, `normalized_for_planning`, `source_local_retained`, or `SettlementProposal`. No numeric choice is made in PR-5A.

### ResourceMathResult request aggregate validation and typed scope

A `ResourceMathResult` may be constructed only against a supplied `ResourceMathRequest` object. Future factory and validator signatures must make aggregate validation receive both objects, for example:

```python
create_resource_math_result(
    *,
    request: ResourceMathRequest,
    ...
) -> ResourceMathResult

validate_resource_math_result(
    result: ResourceMathResult,
    *,
    request: ResourceMathRequest,
) -> bool
```

No repository lookup or dereference occurs. The supplied request/result pair must satisfy all of:

- `result.request_id == request.request_id`.
- Exactly one matching required/satisfied `resource_math_request_ref` dependency binds `result.request_id`.
- Every result dependency carried in `result.dependencies` or named by `result.referenced_dependency_ids`, validation fields, trace fields, or result policy fields is required/satisfied unless the result is deliberately reporting `blocked_missing_dependency` for that dependency.
- `normalized_reference_ids` remains diagnostic only and never determines policy scope.

PR-5F adds exact future typed scope fields to `ResourceMathResult` so PR-5A does not infer from untyped `normalized_reference_ids`:

```python
referenced_subject_binding_ids: tuple[str, ...] = ()
referenced_resource_ref_ids: tuple[str, ...] = ()
referenced_quantity_ids: tuple[str, ...] = ()
referenced_cost_term_ids: tuple[str, ...] = ()
referenced_cost_bundle_ids: tuple[str, ...] = ()
referenced_consequence_term_ids: tuple[str, ...] = ()
referenced_dependency_ids: tuple[str, ...] = ()
```

Typed scope rules:

- Each typed reference tuple must contain unique non-empty internal IDs.
- Every typed reference must resolve in the supplied `ResourceMathRequest`.
- Result quantity scope is the union of `referenced_quantity_ids`, every `quantity_id` on scoped cost terms, every `quantity_id` on scoped consequence terms, and every `quantity_id` reached through scoped cost bundles and their scoped `term_ids`.
- Term-derived quantities count only when the term `value_mode` is `resource_quantity` or `quantity_only`; `resource_reference_only` and `policy_only` do not add a quantity.
- Cost-bundle scope includes each contained `term_id`; alternative groups do not perform selection and therefore do not reduce the scoped term set in PR-5A.
- A quantity, term, bundle, consequence, or dependency that is not in the typed scope is not inspected for result policy enforcement.
- Any internal record named by typed result scope that names `dependency_ids` brings those dependencies into result dependency scope.

Aggregate result enforcement uses this precedence when no lawful terminal quarantine/escalation pair is present:

1. Any scoped required dependency with `satisfied=False`, including a binding dependency or a dependency named by a scoped record, forces `decision=blocked_missing_dependency`, `blocking=True`, and a lawful stage from `MISSING_DEPENDENCY_STAGES`.
2. Any scoped quantity with `representation_kind == blocked_pending_numeric_choice` forces `decision=blocked_incompatible_policy`, `stage=policy_refs_declared`, `blocking=True`, `quarantined=False`, and `escalated=False`.
3. Any scoped lexically negative quantity using `negative_values_require_owner_handoff` forces `decision=requires_owner_handoff`, `stage=blocked_pending_owner_handoff`, `blocking=True`, and at least one matching required/satisfied `owner_handoff_ref` dependency.
4. Any scoped `CostTerm` or `ConsequenceTerm` with `value_mode=policy_only` that is event-only, source-local, unusual donor semantics, or otherwise not a proposed resource state delta must route through `requires_owner_handoff`, `quarantined_for_review`, or `escalated_to_doctrine`; PR-5A may not normalize it as a numeric resource change.

A result whose typed scope contains any of the above blockers cannot be used by `SettlementProposal` unless a later valid result with accepted or normalized planning status and no blocker is supplied. This contract is aggregate-only; leaf validators do not inspect request contents.

## 10. Term value-mode contract

Add the exact future controlled surface `RESOURCE_TERM_VALUE_MODES` with values:

- `resource_quantity`
- `resource_reference_only`
- `quantity_only`
- `policy_only`

Add required field to both `CostTerm` and `ConsequenceTerm`:

```python
value_mode: str
```

No default. The caller must declare the mode.

Exact co-presence rules:

| value_mode | resource_ref_id | quantity_id |
|---|---|---|
| `resource_quantity` | required | required |
| `resource_reference_only` | required | must be `None` |
| `quantity_only` | must be `None` | required |
| `policy_only` | must be `None` | must be `None` |

Additional rules: all supplied internal IDs must resolve in the enclosing request; no value mode calculates affordability or applies a consequence; source-local or unusual donor terms may use `policy_only` only with an explicit owner handoff, quarantine, or doctrine-escalation route; family-specific semantic legality remains owned by the relevant RT owner; PR-5A validates co-presence and references only. This provides a lawful place for event-like, qualitative, time, opportunity, social, source-local, and non-pool consequences without pretending they are numeric resource changes.

## 11. Cost-bundle bound semantics

PR-5F replaces PR-5D's declaration-count rule with exact future selection-policy semantics. Fields remain:

```python
minimum_required_terms: int | None = None
maximum_allowed_terms: int | None = None
```

Rules:

- `bool` is rejected.
- Supplied values must be positive integers.
- Bounds describe the number of terms a future downstream settlement policy may select from declared `term_ids`.
- No selection occurs in PR-5A.
- `minimum_required_terms <= len(term_ids)`.
- `maximum_allowed_terms <= len(term_ids)`.
- When both are supplied, `minimum_required_terms <= maximum_allowed_terms`.

For `atomicity_policy == all_or_nothing_requested`, bounds may both be `None`, or both must equal `len(term_ids)`. For atomicity policies permitting subsets or alternatives, bounds may declare future selection limits, compatibility must match the inherited atomicity/ordering/partial-settlement matrix, alternative groups remain subject to unique-group, contained-member, and no-overlap rules, and every unlisted combination remains invalid. This correction replaces the prior rule requiring `maximum_allowed_terms` to be at least `len(term_ids)`.

## 12. Settlement-proposal result eligibility

A `SettlementProposal` may be constructed only against a supplied `ResourceMathResult` object. Future factory and validator signatures must make aggregate validation receive both objects, for example:

```python
create_settlement_proposal(*, result: ResourceMathResult, ...)
validate_settlement_proposal(
    proposal: SettlementProposal,
    *,
    result: ResourceMathResult,
) -> bool
```

No repository lookup or dereference occurs. The supplied result must satisfy all of:

- `proposal.result_id == result.result_id`.
- `proposal.validation_result_ref_id == result.validation_result_ref_id`.
- `proposal.validation_decision == result.validation_decision`.
- `result.validation_decision == validation_passed`.
- `result.validation_result_ref_id` is non-empty.
- `result.stage == calculation_ready_for_review`.
- `result.decision` belongs to `accepted_for_planning` or `normalized_for_planning`.
- `result.blocking is False`.
- `result.quarantined is False`.
- `result.escalated is False`.
- Every matching validation, result, trace, and dependency binding is present.
- No false-only authority field is true.

Reject proposals referencing results that are `validation_ready`, `validation_failed`, blocked, quarantined, escalated, `source_local_retained` without later accepted normalization, awaiting owner handoff, awaiting validation review, or missing dependencies. The proposal remains non-mutating and non-authoritative.

## 13. State-delta requirement and event-only routing

Preserve that `SettlementProposal.proposed_state_delta_refs` must be non-empty and unique, and every state-delta reference requires a matching required/satisfied `state_delta_ref` dependency.

Ownership clarification:

- RT-002 `SettlementProposal` is only for proposed resource/consequence state changes.
- A purely event-only consequence with no proposed state delta does not create a `SettlementProposal`.
- An event-only or policy-only consequence remains represented as a `ConsequenceTerm` using `value_mode=policy_only`.
- It must route through `requires_owner_handoff`, quarantine, or doctrine escalation to the relevant owner.
- RT-001, RT-003, RT-006, RT-007, RT-010, or another lawful owner may later produce an event-specific artifact.
- RT-002 does not append or commit events.
- PR-5A does not add a proposed-event shape.

This keeps the resource-math service from absorbing general event ownership.

## 14. Internal and external reference integrity

Internal same-request identities are `subject_binding_id`, `resource_ref_id`, `quantity_id`, `cost_term_id`, `cost_bundle_id`, `consequence_term_id`, and `dependency_id`. They must be unique and every internal reference must resolve.

External identities include subject, unit, dimension, command, action legality, state projection, validation, trace, provenance, owner handoff, RNG/table, request/result, state delta, transaction, event commitment, and rollback accounting. They require their exact typed dependency binding. No external object existence is checked in PR-5A.

## 15. Factory / validator parity

PR-5A must later provide shared private validation helpers and create/validate functions for all ten inherited shapes: `ResourceMathSubjectReference`, `ResourceReference`, `QuantitySpecification`, `ResourceMathDependency`, `CostTerm`, `CostBundle`, `ConsequenceTerm`, `ResourceMathRequest`, `ResourceMathResult`, and `SettlementProposal`.

PR-5F specifically requires shared helpers for external field/dependency binding; optional-unsatisfied dependency classification; precision and scale; source-literal characters; negative-value policies; blocked numeric choice; term value modes; bundle bounds; proposal/result compatibility; result/request aggregate validation; non-empty state-delta refs; internal-reference resolution; and false-only authority fields. Factories and validators must enforce the same rules. Manual construction of a frozen dataclass must not bypass them.

## 16. Serialization and hidden information

Preserve internal `to_dict()` only; no `to_public_dict`; defensive copies; tuple-to-list conversion only in returned copies; no calculations during serialization; no public/model/player/GM projection; RT-005 owns later projection and redaction; and source literals, quantities, dependencies, provenance, backend IDs, and hidden owner information remain internal.

## 17. Corpus-scale pressure review

The corrected contracts support 200-400 mixed donor sources without making donor assumptions Astra defaults:

- Fantasy and sci-fi sources use subject bindings and typed dependencies for actors, equipment, vehicles, locations, ships, or factions while resource-like terms remain reference-only or quantity-bearing as declared.
- Cultivation and breakthrough resources can keep qi, meridians, stages, tribulations, bottlenecks, and source-local cosmologies as `policy_only`, owner-handoff, quarantine, or doctrine-escalation records rather than canon resource pools.
- Class/archetype and profession resources can bind class features, job meters, cooldown-like resources, preparation slots, and reputation rights to subject and provenance dependencies without executing abilities.
- Point-buy and narrative currencies can use exact quantities where declared, or `source_literal_only`/`blocked_pending_numeric_choice` when the donor text is not numerically settled; settlement remains blocked until validation/result eligibility is met.
- Cyberware/biotech capacity and psionic fatigue can use unit/dimension dependencies, negative policies, and owner handoffs for capacity, strain, fatigue, backlash, or hidden thresholds.
- Horror stress, sanity, corruption, doom, and similar tracks can route hidden, qualitative, or source-local consequences through RT-005 projection rules, `policy_only`, quarantine, or doctrine escalation.
- Ammunition, fuel, charges, durability, vehicles, mechs, ships, companions, and summons can declare resources and quantities with subject ownership but cannot mutate inventory, vehicle state, or companion state in RT-002.
- Crafting, salvage, requisition, time, opportunity, position, reputation, debt, and obligation can declare resource references, quantity-only terms, or policy-only terms with provenance and owner handoff when the family is not a simple pool.
- Mission, faction, world, generated-content, persistent campaign, and source-local cosmological consequences use value modes and routing to lawful owners rather than becoming Astra defaults.

Across these donor families, corrected subject bindings, typed dependencies, value modes, quantity policies, owner handoffs, quarantine, and doctrine escalation provide lawful destinations while PR-5A performs no arithmetic, settlement, mutation, event commitment, conversion, or canon promotion.

## 18. PR-5E closure ledger

| prior defect | exact PR-5F correction | future PR-5A validator requirement | closure status |
|---|---|---|---|
| External `subject_ref_id` lacked a dependency type. | Add `subject_ref` and exact aggregate binding. | Require exactly one required/satisfied `subject_ref` dependency per subject reference. | closed |
| External unit fields lacked dependency bindings. | Add `unit_ref` and bind every non-None unit field. | Reject absent, duplicate, optional, or unsatisfied unit bindings. | closed |
| External dimension fields lacked dependency bindings. | Add `dimension_ref` and bind every non-None dimension field. | Reject absent, duplicate, optional, or unsatisfied dimension bindings. | closed |
| Optional unsatisfied dependencies were ambiguous. | Define binding versus advisory optional semantics. | Optional unsatisfied dependencies cannot satisfy bindings or named dependency IDs. | closed |
| Precision remained a free-string or unclear declaration. | Define positive integer decimal-only precision metadata. | Enforce precision kind and bool rejection without numeric execution. | closed |
| Source literals lacked exact control-character/multiline posture. | Define single-line no-control no-surrogate literal contract. | Reject edge whitespace, multiline, Cc/Cs, tab, NUL, CR, and LF. | closed |
| Negative policy results were not exact. | Define lexical negativity and three policy outcomes. | Treat `-0`, `-0.0`, and `-0/1` as negative; enforce provenance or owner handoff rules. | closed |
| Blocked numeric choice did not force a result route. | Force blocked incompatible policy unless terminal quarantine/escalation applies. | Reject accepted/normalized/source-local/proposal use. | closed |
| CostTerm optional resource/quantity combinations were incomplete. | Add `RESOURCE_TERM_VALUE_MODES` and co-presence matrix. | Validate mode, co-presence, and internal ID resolution. | closed |
| ConsequenceTerm optional resource/quantity combinations were incomplete. | Add same value-mode matrix and event/policy-only routing. | Validate co-presence and required owner route for unusual policy-only terms. | closed |
| `maximum_allowed_terms` semantics were contradictory. | Define selection-policy upper bound `<= len(term_ids)`. | Enforce bounds, all-or-nothing special rule, and inherited matrix compatibility. | closed |
| Proposal validation-result equality was missing. | Require proposal and supplied result equality for validation result and decision. | Compare supplied result object; no repository lookup. | closed |
| Proposal result eligibility was underspecified. | Require passed, calculation-ready, accepted/normalized, non-blocking, non-quarantined, non-escalated result. | Reject validation-ready, failed, blocked, quarantined, escalated, source-local-only, handoff, review, and missing-dependency results. | closed |
| Event-only routing could absorb general event ownership. | Keep event-only as policy-only consequence and route to owners; no proposal without state delta. | Enforce non-empty state delta and no proposed-event shape. | closed |
| Factory/validator parity could still diverge. | Require shared private helpers and parity for all residual rules. | Factories and validators reject identical invalid states, including frozen dataclass manual construction bypasses. | closed |

Every PR-5E blocker is closed for PR-5A planning; none is irrelevant to PR-5A.

## 19. PR-5G review boundary

Recommended next review:

**RUNTIME-DOMAIN-PR-5G: Resource and Consequence Math Residual Planning Hardening Review Gate**

PR-5G must review PR-5F before PR-5A is authorized.

## 20. Gate finding

```yaml
gate_finding:
  resource_consequence_math_residual_planning_hardening_defined: true
  pr_5e_blockers_addressed: true
  external_reference_dependency_types_completed: true
  optional_dependency_semantics_defined: true
  quantity_precision_contract_defined: true
  source_literal_character_contract_defined: true
  negative_value_policy_contract_defined: true
  blocked_numeric_choice_contract_defined: true
  term_value_mode_contract_defined: true
  bundle_bound_semantics_defined: true
  settlement_result_eligibility_defined: true
  validation_result_equality_defined: true
  event_only_routing_defined: true
  internal_external_reference_integrity_defined: true
  factory_validator_parity_defined: true
  corpus_scale_pressure_review_complete: true
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

## 21. Non-implementation reaffirmation

PR-5F adds no runtime/domain implementation; calculations or formulas; expression evaluator; affordability execution; reservation; settlement execution; state mutation; delta application; event append or commitment; persistence or replay; RNG/table execution; combat, ability, inventory, mission, or social mechanics; model, prompt, UI, or live-play behavior; conversion; sourcebook inclusion; or canon promotion.

```yaml
classification:
  planning_hardening_only: true
  implementation_authority: false
  runtime_domain_implementation: false
  calculations_or_formulas: false
  expression_evaluator: false
  affordability_execution: false
  reservation: false
  settlement_execution: false
  state_mutation: false
  delta_application: false
  event_append_or_commitment: false
  persistence_or_replay: false
  rng_table_execution: false
  combat_ability_inventory_mission_social_mechanics: false
  model_prompt_ui_live_play_behavior: false
  conversion: false
  sourcebook_inclusion: false
  canon_promotion: false
```

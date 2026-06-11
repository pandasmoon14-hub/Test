# RUNTIME-DOMAIN-PR-5G: Resource and Consequence Math Residual Planning Hardening Review Gate

Artifact ID: **RUNTIME-DOMAIN-PR-5G-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-REVIEW-001**.

## 1. Purpose, status, source ledger, and authority precedence

PR-5G is a **non-executable review gate**. It reviews **RUNTIME-DOMAIN-PR-5F-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-001**, implements no code, and authorizes only one of two downstream paths: **RUNTIME-DOMAIN-PR-5A Resource and Consequence Math Skeleton Implementation** or **RUNTIME-DOMAIN-PR-5H Resource and Consequence Math Final Residual Planning Hardening**. PR-5A remains blocked until this review is accepted.

Source ledger reviewed:

- `RUNTIME-DOMAIN-PR-5F-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-001`
- `RUNTIME-DOMAIN-PR-5E-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-REVIEW-001`
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
- current domain and kernel skeletons, PR-5F focused tests, doctrine registry, and current decision log

Authority precedence: PR-5F overrides PR-5D only where PR-5F explicitly replaces a contract. PR-5D overrides PR-5B only where PR-5D explicitly replaces a contract. Earlier contracts remain inherited where later artifacts do not replace them.

## 2. Backend-first invariant

The backend-first invariant is confirmed and remains binding:

- The LLM is not the game engine.
- References are not calculations.
- Results are not state.
- Settlement proposals are not transactions.
- `validation_ready` is not `validation_passed`.
- Donor text, narration, generated content, and source-local constructs cannot grant resource authority.
- Runtime validation cannot promote canon.

PR-5G authorizes no resource calculation, affordability execution, settlement execution, state mutation, event commitment, persistence, RNG execution, conversion, model integration, live-play behavior, or canon promotion.

## 3. PR-5F scope review

PR-5F's scope is confirmed as a four-file planning/tracking footprint:

1. `docs/doctrine/reviews/runtime_domain_pr_5f_resource_consequence_math_residual_planning_hardening.md`
2. `tests/test_runtime_domain_pr_5f_resource_consequence_math_residual_planning_hardening.py`
3. `docs/doctrine/astra_doctrine_registry_v0_1.yaml`
4. `docs/decisions/current_decisions_log.md`

No runtime/domain implementation changes were found in PR-5F. `src/astra_runtime/domain/resource_consequence_math.py` remains absent. Registry and decision tracking are consistent with PR-5F's planning-only status. PR-5A remained blocked. PR-5G was selected as the sole next step.

## 4. PR-5E blocker-closure matrix

| PR-5E blocker claimed closed by PR-5F | PR-5G finding | review note |
|---|---|---|
| subject_ref dependency binding | closed | `subject_ref` exists as a binding dependency type and request aggregate validation is named. |
| unit_ref dependency binding | closed | `unit_ref` binding exists for non-None unit fields. |
| dimension_ref dependency binding | closed | `dimension_ref` binding exists for non-None dimension fields. |
| optional-unsatisfied dependency semantics | partially closed | Binding versus advisory optional semantics are described, but a blocked result carrying an unsatisfied binding dependency conflicts with PR-5F's binding-must-be-satisfied language and needs one exact aggregate lifecycle. |
| precision and scale | closed | Positive non-bool decimal precision and fixed-point scale rules are exact and non-executable. |
| source-literal character rules | partially closed | The base `source_literal` character contract is exact, but PR-5A still needs explicit confirmation that a `source_literal` used to justify source-supported negative values follows the same character posture regardless of representation kind. |
| negative-value policy | partially closed | Lexical negativity and owner-handoff/provenance routes are strong, but interaction with unsatisfied binding dependency and typed-scope emptiness needs one deterministic aggregate rule. |
| blocked numeric choice | closed | Blocked numeric choices force a blocked incompatible-policy route unless terminal quarantine/escalation applies. |
| term value modes | closed | Four value modes and co-presence rules are exact. |
| policy-only routes | closed | Three policy routes have exact stage/decision/flag posture and forbid settlement proposals. |
| bundle bounds | partially closed | Bound types and selection-count semantics are improved, but the complete inherited atomicity surface must be restated so PR-5A does not choose between PR-5B/PR-5D/PR-5F literals. |
| result/request aggregate validation | partially closed | Result validators receive a request and typed scope, but empty typed scope and prerequisite validation ordering remain ambiguous. |
| typed result scope | partially closed | Typed fields are exact; empty scope and minimum scoped-record requirements for accepted/normalized results are not exact. |
| proposal/result equality | closed | Proposal validation receives a supplied result and compares validation fields. |
| proposal result eligibility | partially closed | Eligibility is mostly exact; PR-5H must state whether proposal validation takes the original request or requires a prior result/request validation certificate. |
| event-only routing | closed | Event-only consequences remain policy-only and cannot create proposals without lawful state-delta refs. |
| factory/validator parity | partially closed | Shared helper intent is exact; parity needs explicit coverage for manual frozen-dataclass construction after resolving the remaining aggregate ambiguities. |

## 5. Effective implementation-contract inventory

PR-5G constructs the effective inherited contract as follows:

| contract surface | effective inheritance after PR-5B, PR-5D, PR-5F | PR-5G finding |
|---|---|---|
| public constants | PR-5B baseline plus PR-5D final stage/decision/family/dependency surfaces plus PR-5F `subject_ref`, `unit_ref`, `dimension_ref`, `RESOURCE_TERM_VALUE_MODES`, `RESOURCE_TERM_POLICY_ROUTES`, precision, source-literal, negative-policy, typed-scope, and route refinements. | partially ambiguous because inherited atomicity and ordering/partial-settlement values are not restated in one final matrix. |
| `ResourceMathSubjectReference` | typed subject role/type/domain from PR-5D, `subject_ref_id`, and required satisfied `subject_ref` dependency from PR-5F. | unambiguous. |
| `ResourceReference` | resource family, optional unit/dimension refs, owner-domain and visibility rules; non-None unit/dimension fields require satisfied dependencies. | unambiguous. |
| `QuantitySpecification` | exact representation kind, magnitude/source literal fields, integer precision/scale metadata, negative-value policy, unit/dimension dependencies, no Decimal/Fraction/float execution. | partially ambiguous for source-supported negative `source_literal` character posture. |
| `CostTerm` | family plus PR-5F `value_mode: str` and `policy_route: str | None = None`; co-presence matrix controls resource/quantity fields. | unambiguous. |
| `ConsequenceTerm` | same value-mode and policy-route surface as CostTerm; event-only becomes policy-only route. | unambiguous. |
| `CostBundle` | term IDs, alternative groups, positive non-bool min/max selection bounds, all-or-nothing special rule, no selection execution. | partially ambiguous for complete inherited atomicity/ordering/partial-settlement compatibility. |
| `ResourceMathDependency` | dependency ID, type, reference ID, required/satisfied/hidden-info/provenance posture; binding and named dependencies must be required and satisfied; required unsatisfied dependencies force blocked result. | ambiguous where a field binding is itself unavailable and the request/result lifecycle must record a missing binding. |
| `ResourceMathRequest` | aggregate root for subjects, resources, quantities, terms, bundles, consequences, dependencies, trace/provenance/owner-handoff/validation refs. | partially ambiguous on whether a request may contain an incomplete required dependency. |
| `ResourceMathResult` | request ID, supplied-request aggregate validation, validation fields, typed reference scope fields, false-only authority fields, internal-only serialization. | partially ambiguous on empty typed scope and accepted/normalized minimum scope. |
| `SettlementProposal` | supplied-result validation, result/validation equality, passed accepted-or-normalized result, non-empty unique proposed state-delta refs, false-only authority fields. | partially ambiguous on whether supplied original request is an input or a prerequisite validation certificate is required. |
| defaults | PR-5F adds defaults for typed scope tuples and `policy_route=None`; precision defaults to `None`; min/max defaults remain `None`; false-only authority fields remain false. | partially ambiguous because empty default typed scope has no explicit gate consequence. |
| aggregate validator context | request validates external binding; result validates against supplied request; proposal validates against supplied result. | needs PR-5H ordering/certificate rule. |
| false-only authority fields | runtime, domain, calculation, settlement, state, event, persistence, RNG, model, conversion, canon authority fields remain false-only. | unambiguous. |
| serialization posture | internal `to_dict` only, defensive copies, no public projection. | unambiguous. |

Conclusion: PR-5A cannot yet derive one unambiguous effective contract without guessing which historical version controls several aggregate validation and inherited policy-surface details.

## 6. Constant-surface review

PR-5G verified the controlled surfaces for stages and decisions; resource, cost, and consequence families; timing and outcome policies; quantity kinds and representations; negative-value policies; visibility; dependency types; subject types, roles, and owner domains; term value modes; and term policy routes. Each reviewed controlled field has a governing surface and no donor-specific construct becomes Astra default law.

The constant-surface review is only partially acceptable because PR-5F hardens bundle selection bounds without restating every inherited atomicity, ordering, and partial-settlement value in a single effective surface. PR-5H must prevent a later skeleton from silently dropping inherited lawful values or inventing compatibility behavior for `all_or_nothing`, sequential, ordered, unordered, partial, alternative, or source-local bundle policy combinations.

## 7. Stage/decision and blocker-precedence review

PR-5G confirms that PR-5F provides lawful terminal quarantine and escalation pairs, exact policy-route pairs, a blocked missing-dependency route, a blocked pending numeric-choice route, and an owner-handoff route for owner-handoff negatives and policy-only terms. No accepted or normalized result can contain a scoped blocker, and no blocked result can become settlement-eligible.

The review remains partially acceptable rather than pass-ready because simultaneous blockers require one deterministic result. PR-5F lists precedence for missing dependencies, blocked numeric choices, negative owner-handoff quantities, and policy-only routes when no terminal quarantine/escalation pair is present, but the unsatisfied binding dependency lifecycle can still conflict with the assertion that binding dependencies must be satisfied. PR-5H must state the exact precedence when a scoped field lacks a satisfied binding and also has a blocked numeric choice, source-supported negative, owner-handoff negative, hidden-information blocker, quarantine route, or doctrine-escalation route.

## 8. External-reference dependency review

| external reference family | dependency type / aggregate owner | PR-5G finding |
|---|---|---|
| subject | `subject_ref` in `ResourceMathRequest.dependencies` | exact type exists; binding must be required and satisfied. |
| unit | `unit_ref` in request dependencies | exact type exists for non-None unit fields. |
| dimension | `dimension_ref` in request dependencies | exact type exists for non-None dimension fields. |
| command | command dependency inherited from PR-5B/PR-5D request dependencies | exact aggregate owner is request; No command execution implied. |
| action legality | action-legality dependency inherited from validation integration lineage | aggregate request dependency; no legality execution implied. |
| state projection | state-projection dependency inherited from PR-5/PR-5D | request dependency; no state read/write implied. |
| validation request/result | validation refs on request/result/proposal surfaces | linked by aggregate validation, not by repository lookup. |
| trace | trace/provenance refs | diagnostic dependency; no replay or persistence implied. |
| provenance | `provenance_ref` dependency for source-supported negatives and source evidence | required/satisfied when named or bound. |
| owner handoff | `owner_handoff_ref` dependency | required/satisfied for owner-handoff routes. |
| RNG/table result | RNG/table dependency inherited from PR-5 planning | reference-only; no RNG execution. |
| request/result | `resource_math_request_ref` for result and proposal/result refs | exact supplied aggregate validation required. |
| state delta | proposed state-delta refs in proposal | non-empty unique refs; no mutation. |
| transaction | transaction dependency inherited from transaction lifecycle | reference-only; proposal is not transaction. |
| event commitment | event commitment dependency inherited from event commitment skeleton | reference-only; no event append. |
| rollback accounting | rollback/refund accounting refs inherited from PR-5/RT-001 boundaries | reference-only; no rollback execution. |

The exact dependency type exists for the key external fields PR-5F added. However, PR-5H must close the lifecycle of incomplete required dependencies: exact aggregate owner, structural field linkage, ID uniqueness, `(dependency_type, reference_id)` uniqueness, and whether a request may carry an unsatisfied required binding remain material for PR-5A.

## 9. Optional and unsatisfied dependency review

PR-5G resolves the boundary as currently written:

- Binding dependencies are dependencies matching an external field or named by a term/request/result/proposal field; PR-5F says they must be `required=True` and `satisfied=True`.
- Required unsatisfied dependencies are `required=True` and `satisfied=False`; PR-5F says scoped ones force `blocked_missing_dependency`.
- Advisory optional unsatisfied dependencies are `required=False` and `satisfied=False`; they are lawful only when no field is bound to them and they may never satisfy a binding.

This is not yet implementable without invention. PR-5H must state exactly whether a blocked result may carry an unsatisfied binding dependency, whether that dependency remains structurally linked to its field, which aggregate owns it, whether required-unsatisfied state is valid only on a result reporting the blocker, whether a request may contain an incomplete required dependency, and whether non-blocking results can contain only advisory unsatisfied dependencies.

## 10. Result/request aggregate and typed-scope review

PR-5F correctly requires result factories and validators to receive the supplied request, require request ID equality, require exact `resource_math_request_ref` binding, use typed result-scope fields, require typed IDs to be unique and resolve in the supplied request, close bundle scope over contained terms, close term scope over quantities and dependencies, ignore unscoped records, and keep `normalized_reference_ids` diagnostic only.

Open PR-5H corrections before PR-5A:

- State whether an empty typed result scope is lawful.
- State whether accepted/normalized results require at least one scoped subject/resource/quantity/term/bundle/consequence or dependency.
- State whether every scoped subject/resource/quantity/term/bundle/consequence and dependency has an exact integrity rule even when the result is blocked.
- State whether policy enforcement can be performed without inference when scope is empty but request records contain policy-only terms or blocked quantities.

## 11. Quantity review

PR-5G confirms the quantity contract covers integer precision and scale types, bool rejection, representation-specific lexical grammars, no Decimal/Fraction/float/arithmetic/rounding/conversion/affordability execution, source-literal whitespace/control/surrogate handling, lexical negativity including `-0`, source-supported negative provenance, owner-handoff-negative routing, and blocked pending numeric-choice routing.

PR-5H is required because the exact character posture for a `source_literal` used to justify a negative numeric value must be explicitly bound to the same source-literal character contract, not only to `source_literal_only` quantities. This prevents PR-5A from inventing a relaxed or stricter literal rule for source-supported negative provenance.

## 12. Term value-mode and policy-route review

PR-5G finds this surface acceptable. Exact fields and co-presence are defined for `resource_quantity`, `resource_reference_only`, `quantity_only`, and `policy_only`. Policy routes are exactly `owner_handoff_required`, `quarantine_required`, and `doctrine_escalation_required`.

Non-policy terms require `policy_route=None`; `policy_only` requires exactly one route; unclassified policy-only terms are invalid; each route has one exact stage/decision/flag posture; no policy-only term reaches accepted, normalized, or `SettlementProposal`; and PR-5A never infers route from donor wording, metadata, family, or owner.

## 13. CostBundle review

PR-5G confirms PR-5F defines term IDs, alternative groups, positive non-bool min/max selection bounds, selected-term counting semantics, no selection or settlement execution, and the all-or-nothing requested rule.

PR-5H is required to check the complete inherited atomicity surface rather than only literals mentioned by PR-5F. The final residual hardening must provide one compatibility matrix for every inherited atomicity, ordering, and partial-settlement policy and must state every unlisted combination is invalid.

## 14. SettlementProposal review

PR-5G confirms proposal validation receives a supplied result, result ID and validation fields match, `validation_passed` is required, stage is `calculation_ready_for_review`, decision is accepted or normalized, result is non-blocking, non-quarantined, non-escalated, required bindings exist, false-only authority fields remain false, proposed state-delta refs are non-empty and unique, and event-only and policy-only terms do not create proposals.

PR-5H must determine whether proposal validation also needs the supplied original request to verify typed result scope, or whether validating the supplied result against its request first is an exact prior result/request validation prerequisite and must be represented as a validation certificate/flag/input. PR-5A must not choose either architecture by inference.

## 15. Internal-reference and factory/validator parity review

PR-5G confirms the intended shared validators can enforce internal uniqueness and resolution, external binding, quantity lexical rules, blocker precedence, term modes and routes, bundle rules, result/request compatibility, proposal/result compatibility, false-only authority, and tuple/metadata immutability. Manual frozen-dataclass construction must not bypass the rules.

Parity is partially acceptable because the unresolved aggregate cases in sections 9, 10, 13, and 14 would otherwise require factories and validators to invent different behavior for edge cases.

## 16. Serialization and hidden-information review

PR-5G finds this boundary acceptable. The effective contract allows internal `to_dict` only, no `to_public_dict`, defensive copies, no calculations during serialization, no public/model/player/GM projection, and no redaction behavior in PR-5A. RT-005 owns later redaction and visibility. Hidden literals, quantities, provenance, dependencies, and IDs cannot leak through a public projection because no public projection is authorized.

## 17. Corpus-scale and owner-boundary review

PR-5G pressure-tested the effective contracts against fantasy and sci-fi; cultivation; class/archetype; professions; point-buy and narrative currencies; cyberware/biotech; psionics; horror/investigation; vehicles/mechs/ships; companions/summons; crafting/salvage/requisition; mission/faction/debt; source-local cosmologies; generated content; and persistent campaign consequences.

The contract supports lawful direct, normalized, source-local, owner-handoff, quarantine, and doctrine-escalation destinations. RT-002 does not absorb combat, ability, inventory, mission, social, RNG, hidden-information, persistence, event, or canon ownership. Those domains remain with RT-001 and RT-003 through RT-012 or future authorized owners.

## 18. Risk and hardening ledger

| risk | severity | current mitigation | required before PR-5A | required before executable calculation | owner | PR-5H required |
|---|---|---|---|---|---|---|
| layered planning artifacts produce conflicting effective fields | high | precedence rule exists | one final effective inventory must restate ambiguous fields | implementation docs can then derive code from one contract | RT-002 | true |
| inherited constant silently dropped | high | PR-5F adds surfaces | restate full inherited atomicity/ordering/partial-settlement surface | executable validators use same constants | RT-002 | true |
| unsatisfied binding dependency contract conflicts | high | advisory-vs-binding language exists | exact lifecycle for unsatisfied binding vs missing dependency | executable validators preserve same blocked result rule | RT-002/RT-011 | true |
| empty typed scope is ambiguous | high | typed fields exist with default empty tuples | decide lawful empty scope and accepted/normalized minimum scope | executable validators require exact aggregate scope | RT-002/RT-011 | true |
| blocker precedence is incomplete | medium | PR-5F lists main precedence | add simultaneous blocker table including hidden/quarantine/escalation/source-supported negative | executable calculation remains non-authorized until later | RT-002/RT-011 | true |
| source-supported negative literal has undefined character posture | medium | base source-literal contract exists | bind source-supported negative source literals to that contract | numeric parsers remain prohibited until separately authorized | RT-002 | true |
| policy route can be bypassed | low | policy-only routes are exact | retain route rules and test empty-scope bypass | later validators must not infer route from donor wording | RT-002 | false |
| bundle policy surface is incompletely reviewed | medium | min/max and all-or-nothing rule exist | one complete bundle policy matrix | executable settlement still deferred | RT-002 | true |
| proposal result was not validated against its request | high | supplied result equality exists | require supplied original request or explicit prior result/request validation prerequisite | executable settlement proposal validators follow same input contract | RT-002/RT-011 | true |
| hidden data leaks through serialization | medium | internal-only serialization; no public projection | retain no `to_public_dict` and defensive copies | RT-005 redaction before any public projection | RT-005 | false |
| PR-5A must invent a validator rule | high | many residual rules exist | PR-5H must close aggregate ambiguities listed in this review | executable validators require separate authorization | RT-002/RT-011 | true |

## 19. Gate decision

PR-5G selects exactly one outcome: **HARDENING**. PR-5H is required before PR-5A because material aggregate-validation, compatibility, linkage, and effective-contract defects remain and would force PR-5A to invent behavior.

```yaml
gate_finding:
  resource_consequence_math_residual_planning_review_complete: true
  pr_5f_scope_confirmed: true
  pr_5e_blockers_closed: partially
  effective_contract_inventory_unambiguous: false
  constant_surfaces_acceptable: partially
  stage_decision_and_blocker_precedence_acceptable: partially
  external_dependency_binding_complete: partially
  optional_dependency_contract_acceptable: partially
  result_request_aggregate_contract_acceptable: partially
  typed_scope_contract_acceptable: partially
  quantity_contract_acceptable: partially
  term_value_mode_and_policy_route_contract_acceptable: true
  bundle_contract_acceptable: partially
  settlement_proposal_contract_acceptable: partially
  internal_reference_integrity_acceptable: true
  factory_validator_parity_acceptable: partially
  serialization_boundary_acceptable: true
  corpus_scale_pressure_acceptable: true
  rt_002_owner_boundary_preserved: true
  requires_pr_5h_before_pr_5a: true
  ready_for_pr_5a_skeleton_implementation: false
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-5H resource and consequence math final residual planning hardening
  next_step_status: planning_hardening_pending_review
```

## 20. Recommended next PR

Recommended next PR: **RUNTIME-DOMAIN-PR-5H final residual planning hardening**.

Exact corrections to make without implementing them:

1. Publish one final effective contract matrix that restates all inherited fields, defaults, and governed constants after PR-5B/PR-5D/PR-5F precedence.
2. Restate the complete inherited atomicity, ordering, and partial-settlement surface and one bundle compatibility matrix.
3. Define the exact lifecycle for unsatisfied binding dependencies, missing binding dependencies, required unsatisfied dependencies, and advisory optional unsatisfied dependencies.
4. Decide whether empty typed result scope is lawful and whether accepted/normalized results require at least one scoped record.
5. Add a complete simultaneous blocker-precedence table.
6. Bind source-supported negative `source_literal` evidence to the same character contract as all other source literals.
7. Define whether proposal validation takes the original request or requires a prior exact result/request validation prerequisite.
8. Update parity requirements so factories and validators cannot diverge on those edge cases or on manual frozen-dataclass construction.

## 21. Non-implementation reaffirmation and classification block

PR-5G is review-only. It creates no runtime/domain implementation file, no `resource_consequence_math.py`, no formula or expression evaluator, no persistence structure, no model/prompt/UI/live-play behavior, no settlement executor, no state mutation path, no event commitment path, no RNG executor, and no canon promotion path.

```yaml
runtime_domain_pr_5g_classification:
  artifact_id: RUNTIME-DOMAIN-PR-5G-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-REVIEW-001
  artifact_type: residual_planning_hardening_review_gate
  implementation_status: review_only
  reviews_pr_5f: true
  pr_5h_required_before_pr_5a: true
  pr_5a_authorized: false
  exactly_one_next_step: true
  next_step_authorized: RUNTIME-DOMAIN-PR-5H resource and consequence math final residual planning hardening
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

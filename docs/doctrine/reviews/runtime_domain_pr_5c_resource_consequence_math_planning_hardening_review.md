# RUNTIME-DOMAIN-PR-5C: Resource and Consequence Math Planning Hardening Review Gate

## 1. Purpose, status, and source ledger

Review ID: **RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001**.

This is a non-executable review gate. It reviews PR-5B (**RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001**), implements no code, authorizes only either PR-5A or PR-5D, and keeps PR-5A blocked until this gate is accepted. The gate is intentionally evidence-based rather than a pass-through for PR-5B focused tests.

Source ledger reviewed:

- `docs/doctrine/reviews/runtime_domain_pr_5b_resource_consequence_math_planning_hardening.md`
- `docs/doctrine/reviews/runtime_domain_pr_5_resource_consequence_math_service_plan.md`
- `docs/doctrine/reviews/runtime_domain_pr_4f_validation_integration_residual_hardening_review.md`
- `docs/doctrine/reviews/runtime_domain_pr_0_domain_service_implementation_sequencing_plan.md`
- `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`
- RT001 and RT003 through RT012 owner specifications
- current domain skeletons and current kernel skeletons
- PR-5B focused tests
- doctrine registry
- current decision log

## 2. Backend-first invariant

Confirmed:

- the LLM is not the game engine;
- reference shapes are not calculations;
- results and settlement proposals are not committed state;
- `validation_ready` is not `validation_passed`;
- no donor resource terminology becomes Astra law;
- no runtime or canon authority is granted.

PR-5C grants no runtime authority, no canon authority, no execution authority, and no settlement authority. PR-5B correctly preserves the backend-first invariant, but several candidate contracts still leave PR-5A with implementation choices it must not invent.

## 3. PR-5B scope review

| Scope item | Review finding |
|---|---|
| Planning-hardening artifact | Present and scoped as planning-only. |
| Focused tests | Present and focused on PR-5B artifact, registry, decision log, and absence of implementation module. |
| Registry | Contains one PR-5B file record and planning-only metadata. |
| Decision log | Contains one PR-5B decision heading and non-implementation boundary. |
| Four-file scope | PR-5B appears limited to planning artifact, focused test, registry, and decision log. |
| Absence of `resource_consequence_math.py` | Confirmed as a required invariant; PR-5B did not create the future domain module. |

PR-5B stayed within its authorized planning-hardening scope.

## 4. PR-5 requirement-closure matrix

| Requirement area | Closure | Review basis | PR-5D required |
|---|---|---|---:|
| Public constants | partially closed | Most constant surfaces are enumerated, but validation posture is not a surface and stage/decision values collide for quarantine and escalation. | true |
| Stage model | partially closed | Stages list terminal posture, decisions, references, outputs, forbidden behavior, and next stages, but quarantine/escalation blocking semantics need correction. | true |
| Decisions | partially closed | Decisions are enumerated, but quarantine/escalation are described as non-blocking planning despite terminal/escalation meaning. | true |
| Decision/stage compatibility | partially closed | Compatibility table exists, but a terminal-or-blocking posture mismatch remains. | true |
| Nine dataclass contracts | partially closed | Exact field tables exist, but subject typing, validation posture, linkage, and bundle bound semantics are not implementation-ready. | true |
| Dependencies | partially closed | Dependency shape and duplicate rules exist, but referenced IDs are not structurally bound to request/result/proposal fields. | true |
| Terms and bundles | partially closed | Term and bundle surfaces exist, but consequence timing/outcome defaults and bundle minimum/maximum semantics need hardening. | true |
| Request/result/proposal linkage | partially closed | High-level linkage is stated, but typed dependency requirements are not exact enough for PR-5A. | true |
| False-only flags | closed | False-only authority flags are consistently enumerated for request/result/proposal; duplication is a later ergonomics issue, not a PR-5A blocker. | false |
| factory/validator parity | partially closed | Shared invariants exist, but missing controlled vocabularies and linkage rules would force validator invention. | true |
| Serialization | partially closed | `to_dict()` behavior is described; public/hidden serialization ownership remains unresolved and should be routed explicitly. | true |
| Family matrices | closed | Families provide lawful source-local and owner-routed destinations without forcing donor law. | false |
| Numeric/unit/conversion ledgers | partially closed | Declaration preservation is clear, but lexical validation boundaries need explicit non-arithmetic rules. | true |
| Owner and validation handoffs | partially closed | Owner boundaries are generally preserved; validation-posture vocabulary and proposal validation linkage need hardening. | true |

## 5. Constant-surface review

| Surface | Finding |
|---|---|
| `RESOURCE_MATH_STAGES` | Defined once, but includes `quarantined_for_review` and `escalated_to_doctrine`, which also appear as decisions. Lawful only if PR-5D explicitly defines dual stage/decision use. |
| `RESOURCE_MATH_DECISIONS` | Defined once, but quarantine/escalation decision posture is not aligned with blocking/terminal implications. |
| `RESOURCE_FAMILIES` | Acceptable; includes source-local and unknown routing without adopting donor-specific law. |
| `COST_FAMILIES` | Acceptable; broad enough for costs, debts, sacrifices, upkeep, requisition, and source-local costs. |
| `CONSEQUENCE_FAMILIES` | Acceptable; broad enough for persistent, social, narrative, harm, mission, and source-local consequences. |
| `COST_TIMING_POLICIES` | Defined; CostTerm has no invalid default because timing is required. |
| `COST_OUTCOME_POLICIES` | Defined; CostTerm has no invalid default because outcome is required. |
| `QUANTITY_KINDS` | Defined; includes unknown/source-literal routes. |
| `QUANTITY_REPRESENTATION_KINDS` | Defined; supports integer, decimal, fraction, fixed point, source literal, and unknown pending review. |
| `CONVERSION_POLICIES` | Defined; `no_conversion` default is compatible. |
| `ROUNDING_POLICIES` | Defined; `no_rounding` default is compatible. |
| `VISIBILITY_POLICIES` | Defined; `public` defaults are compatible, but hidden public serialization needs ownership routing. |
| `ATOMICITY_POLICIES` | Defined; CostBundle default is compatible. |
| `ORDERING_POLICIES` | Defined; CostBundle default is compatible. |
| `PARTIAL_SETTLEMENT_POLICIES` | Defined; CostBundle default is compatible. |
| `RESOURCE_MATH_DEPENDENCY_TYPES` | Defined; matching typed dependency requirements remain incomplete. |
| `RESOURCE_MATH_SUBJECT_TYPES` | Defined, but future dataclasses mainly use `subject_ref_id` without a subject-type field. |
| `RESOURCE_MATH_OWNER_DOMAINS` | Defined; defaults using `RT002_resource_consequence_math` are compatible if that value remains present. |

Every dataclass default must belong to a governing surface or be an explicitly controlled independent literal. PR-5B fails that standard for `validation_ready` and for ConsequenceTerm timing/outcome defaults that appear to use validation/blocking vocabulary rather than the named cost policy surfaces. No stage may be used as a policy and no decision may be used as a stage unless PR-5D explicitly makes dual-use lawful. Source-local and unknown constructs have lawful routing, and donor-specific constructs are not hidden core law.

## 6. Stage-model review

| Stage | Terminal posture | Allowed decisions | Review finding |
|---|---:|---|---|
| `resource_math_requested` | false | `accepted_for_planning`, `blocked_missing_dependency` | Acceptable as request intake. |
| `source_declaration_captured` | false | `accepted_for_planning`, `normalized_for_planning`, `source_local_retained`, `quarantined_for_review` | Needs explicit rule that quarantine blocks downstream acceptance until review resolves. |
| `subject_refs_bound` | false | `accepted_for_planning`, `blocked_missing_dependency`, `requires_owner_handoff` | Subject refs lack required subject typing in the future shapes. |
| `resource_refs_declared` | false | `accepted_for_planning`, `source_local_retained`, `requires_validation_review`, `escalated_to_doctrine` | Escalation must be blocking or terminal, not non-blocking planning. |
| `quantity_specs_declared` | false | `accepted_for_planning`, `blocked_incompatible_policy`, `requires_validation_review` | Acceptable if lexical-only checks are clarified. |
| `terms_declared` | false | `accepted_for_planning`, `requires_owner_handoff`, `blocked_hidden_information` | Hidden-info behavior must bind to public serialization rules. |
| `bundle_structure_declared` | false | `accepted_for_planning`, `blocked_incompatible_policy` | Bundle bounds are underspecified. |
| `policy_refs_declared` | false | `accepted_for_planning`, `blocked_incompatible_policy`, `escalated_to_doctrine` | Escalation posture needs hardening. |
| `dependency_refs_bound` | false | `accepted_for_planning`, `blocked_missing_dependency`, `requires_validation_review` | Dependency references need structural matching rules. |
| `calculation_ready_for_review` | false | `requires_validation_review`, `requires_owner_handoff`, `accepted_for_planning` | Name risks implying calculation readiness; acceptable only as review readiness if PR-5D clarifies no execution. |
| `blocked_pending_validation` | false | `requires_validation_review` | Review/rework loop is lawful if accepted cannot be reached without validation handoff. |
| `blocked_pending_owner_handoff` | false | `requires_owner_handoff` | Review/rework loop is lawful if accepted cannot be reached without owner handoff. |
| `quarantined_for_review` | true | `quarantined_for_review` | Terminal posture is acceptable, but conflicts with decision non-blocking description. |
| `escalated_to_doctrine` | true | `escalated_to_doctrine` | Terminal posture is acceptable, but conflicts with decision non-blocking description. |

No stage is authorized to execute calculation, reservation, settlement, mutation, event append, or persistence. The only detected cycles are intended review/rework loops, but PR-5D must prevent blocked/quarantined/escalated outcomes from becoming accepted without validation or owner handoff. Declaration and validation readiness are still ambiguous because validation posture is not controlled.

## 7. Decision/stage compatibility review

| Decision | Allowed stages | Blocking/terminal posture | Validation/owner requirements | Review finding |
|---|---|---|---|---|
| `accepted_for_planning` | intake and declaration stages including `calculation_ready_for_review` | non-terminal, non-executing | Trace required; no transaction handoff. | Acceptable only after dependency/validation conditions are structurally satisfied. |
| `normalized_for_planning` | source capture | non-terminal | Trace required; no transaction handoff. | Acceptable. |
| `source_local_retained` | source/resource declaration | non-terminal but routed | Provenance and source-local route required. | Acceptable. |
| `requires_validation_review` | quantity, dependency, ready, blocked-validation | blocking until validation handoff | Validation refs required. | Acceptable, but validation-posture vocabulary is incomplete. |
| `requires_owner_handoff` | subject, terms, ready, blocked-owner | blocking until owner handoff | Owner refs required. | Acceptable. |
| `blocked_missing_dependency` | request, subject, dependency stages | blocking | Dependency refs required. | Acceptable; structural binding needed. |
| `blocked_incompatible_policy` | quantity, bundle, policy stages | blocking | Trace and diagnostic required. | Acceptable. |
| `blocked_hidden_information` | terms | blocking public output | RT-005/context projection route required. | Acceptable if public serialization is routed. |
| `quarantined_for_review` | source capture, ready, blocked-validation, quarantine stage | blocking/terminal in effect | Trace and quarantine reason required. | PR-5B should not classify quarantine as non-blocking planning. |
| `escalated_to_doctrine` | resource, policy, ready, blocked-owner, escalation stage | blocking/terminal in effect | Doctrine/owner handoff required. | PR-5B should not classify escalation as non-blocking planning. |

Quarantine and escalation should be blocking rather than “non-blocking planning.” No decision may authorize transaction handoff, settlement, state mutation, event commitment, persistence, conversion, RNG/table execution, model authority, UI/live play, or canon promotion.

## 8. Exact dataclass-contract review

| Shape | Contract review | PR-5A implementation-ready |
|---|---|---:|
| `ResourceReference` | Fields and defaults are mostly exact, with tuple aliases/provenance and immutable metadata. However it has `subject_ref_id` without `subject_type`, and `validation_posture` is a free string defaulting to `validation_ready`. | false |
| `QuantitySpecification` | Fields support exact preservation without arithmetic. Defaults for conversion, rounding, and visibility are surface-compatible. PR-5D must clarify lexical validation versus numeric parsing. | partially |
| `ResourceMathDependency` | Fields, required/satisfied flags, hidden-info posture, and duplicate rules are stated. Structural binding from referenced dependency IDs to terms/request/result/proposal remains incomplete. | partially |
| `CostTerm` | Required family, timing, outcome, subject/resource/quantity, owner, dependency, provenance, visibility fields are exact; defaults are generally surface-compatible. | partially |
| `CostBundle` | Term IDs, alternative groups, atomicity, ordering, partial settlement, subject/dependency/provenance, and metadata are exact; minimum/maximum declarations lack enough semantics. | false |
| `ConsequenceTerm` | Allows optional resource and quantity, which is lawful for non-resource consequences. Timing/outcome defaults appear to use blocked/validation vocabulary rather than an applicable policy surface. | false |
| `ResourceMathRequest` | Request links command, action legality, subjects, state projections, declared resources/quantities/terms/bundles/consequences, validation, trace, provenance, and owner handoffs. Matching typed dependency requirements are not exact. | false |
| `ResourceMathResult` | Result links request, stage, decision, diagnostics, normalized refs, validation dependencies, trace, metadata, and false-only flags. Stage/decision compatibility and dependency linkage need hardening. | false |
| `SettlementProposal` | Non-mutating proposal fields are exact enough to preserve references, but validation result requirements and empty proposed-delta posture are not exact. | false |

Common posture is acceptable: frozen keyword-only dataclasses, tuple normalization, duplicate handling through validators, immutable metadata, reference-only linkage, provenance and traceability, false-only fields on request/result/proposal, and `to_dict()` with defensive output. PR-5A cannot implement all nine shapes without invention until PR-5D hardens the open contract points.

## 9. Default-value validity matrix

| Shape.field | Default | Governing surface or controlled literal | Finding |
|---|---|---|---|
| `ResourceReference.alias_labels` | `()` | tuple normalization invariant | acceptable |
| `ResourceReference.visibility_policy` | `public` | `VISIBILITY_POLICIES` | acceptable |
| `ResourceReference.source_local` | `False` | boolean controlled literal | acceptable |
| `ResourceReference.validation_posture` | `validation_ready` | missing validation-posture surface | PR-5D defect |
| `ResourceReference.metadata` | `MappingProxyType({})` | metadata immutability invariant | acceptable |
| `QuantitySpecification.precision` | `None` | optional declaration | acceptable |
| `QuantitySpecification.scale` | `None` | optional declaration | acceptable |
| `QuantitySpecification.unit_ref` | `None` | optional declaration | acceptable |
| `QuantitySpecification.dimension_ref` | `None` | optional declaration | acceptable |
| `QuantitySpecification.conversion_policy` | `no_conversion` | `CONVERSION_POLICIES` | acceptable |
| `QuantitySpecification.rounding_policy` | `no_rounding` | `ROUNDING_POLICIES` | acceptable |
| `QuantitySpecification.visibility_policy` | `public` | `VISIBILITY_POLICIES` | acceptable |
| `QuantitySpecification.provenance_refs` | `()` | tuple normalization invariant | acceptable |
| `QuantitySpecification.metadata` | `MappingProxyType({})` | metadata immutability invariant | acceptable |
| `ResourceMathDependency.required` | `True` | boolean controlled literal | acceptable |
| `ResourceMathDependency.satisfied` | `False` | boolean controlled literal | acceptable |
| `ResourceMathDependency.hidden_info_safe` | `False` | boolean controlled literal | acceptable, restrictive by default |
| `ResourceMathDependency.metadata` | `MappingProxyType({})` | metadata immutability invariant | acceptable |
| `CostTerm.visibility_policy` | `public` | `VISIBILITY_POLICIES` | acceptable |
| `CostTerm.owner_domain` | `RT002_resource_consequence_math` | `RESOURCE_MATH_OWNER_DOMAINS` | acceptable if value remains defined |
| `CostTerm.dependency_ids` | `()` | tuple normalization invariant | acceptable |
| `CostTerm.provenance_refs` | `()` | tuple normalization invariant | acceptable |
| `CostTerm.metadata` | `MappingProxyType({})` | metadata immutability invariant | acceptable |
| `CostBundle.alternative_groups` | `()` | tuple normalization invariant | acceptable |
| `CostBundle.atomicity_policy` | `all_or_nothing_requested` | `ATOMICITY_POLICIES` | acceptable |
| `CostBundle.ordering_policy` | `unordered_terms` | `ORDERING_POLICIES` | acceptable |
| `CostBundle.partial_settlement_policy` | `no_partial_settlement` | `PARTIAL_SETTLEMENT_POLICIES` | acceptable |
| `CostBundle.minimum_required_terms` | `None` | optional declaration | acceptable but semantics underspecified |
| `CostBundle.maximum_allowed_terms` | `None` | optional declaration | acceptable but semantics underspecified |
| `CostBundle.subject_ref_ids` | `()` | tuple normalization invariant | acceptable |
| `CostBundle.dependency_ids` | `()` | tuple normalization invariant | acceptable |
| `CostBundle.provenance_refs` | `()` | tuple normalization invariant | acceptable |
| `CostBundle.metadata` | `MappingProxyType({})` | metadata immutability invariant | acceptable |
| `ConsequenceTerm.resource_ref_id` | `None` | optional declaration | acceptable |
| `ConsequenceTerm.quantity_id` | `None` | optional declaration | acceptable |
| `ConsequenceTerm.timing_policy` | `blocked_pending_validation` | not clearly `COST_TIMING_POLICIES` | PR-5D defect |
| `ConsequenceTerm.outcome_policy` | `validation_blocked` | not clearly `COST_OUTCOME_POLICIES` | PR-5D defect |
| `ConsequenceTerm.visibility_policy` | `public` | `VISIBILITY_POLICIES` | acceptable |
| `ConsequenceTerm.dependency_ids` | `()` | tuple normalization invariant | acceptable |
| `ConsequenceTerm.provenance_refs` | `()` | tuple normalization invariant | acceptable |
| `ConsequenceTerm.validation_posture` | `validation_ready` | missing validation-posture surface | PR-5D defect |
| `ConsequenceTerm.metadata` | `MappingProxyType({})` | metadata immutability invariant | acceptable |
| `ResourceMathRequest` false-only flags | `False` | false-only authority contract | acceptable |
| `ResourceMathResult` false-only flags | `False` | false-only authority contract | acceptable |
| `SettlementProposal.validation_result_ref` | `None` | optional declaration | PR-5D must state when lawful |
| `SettlementProposal.visibility_policy` | `public` | `VISIBILITY_POLICIES` | acceptable |
| `SettlementProposal` false-only flags | `False` | false-only authority contract | acceptable |

Defaults outside their constant surfaces, or belonging to the wrong surface, are PR-5D-level defects unless PR-5D explicitly defines them as independent controlled literals.

## 10. Validation-posture review

PR-5B uses values such as `validation_ready` and `validation_passed`. It also states that `validation_ready` is not `validation_passed`, which is correct. However, `validation_posture` remains a free string without exact allowed values, without a dedicated future constant surface, and without typed dependency linkage to validation integration.

PR-5A must not invent a validation-posture vocabulary. This blocks PR-5A because validators and factories would otherwise choose allowed values, defaults, and transition behavior. PR-5D must either define a `VALIDATION_POSTURE_POLICIES`/equivalent surface or remove the field in favor of typed validation dependencies with exact linkage.

## 11. Subject-identity review

PR-5B defines `RESOURCE_MATH_SUBJECT_TYPES`, but the proposed shapes chiefly store `subject_ref_id` or `subject_ref_ids` without pairing each subject reference with a subject type. That is not sufficient for a 200-400-source corpus containing vehicles, companions, factions, missions, locations, assets, generated content, cross-subject costs, and source-local subject categories.

PR-5A need not dereference objects, but it must be able to preserve typed subject identity. PR-5D should add exact subject typing or a typed subject-reference shape so subject type, subject reference, resource owner, related subjects, and cross-subject costs can be represented without object dereferencing.

## 12. Dependency-contract review

Verified:

- dependency fields are listed;
- allowed dependency types are controlled;
- owner-domain requirements are controlled;
- duplicate dependency IDs are rejected;
- duplicate `(dependency_type, reference_id)` pairs are rejected absent a future multiplicity rule;
- dependencies are reference-only and perform no execution.

Additional findings:

- `required=False` and `satisfied=False` is lawful as an optional unsatisfied dependency, if PR-5D says it cannot block by itself.
- `required=True` and `satisfied=False` must force a blocked or requires-review decision before any executable phase.
- `hidden_info_safe=False` must restrict public serialization and route through RT-005/context projection.
- request/result/proposal reference fields should require matching typed dependencies where the field name implies external validation, transaction, event, state, provenance, owner, or trace authority.
- dependency IDs referenced by terms and requests are not yet structurally bound strongly enough for PR-5A implementation.

## 13. Quantity-contract review

PR-5B can represent, without calculating: integer, decimal, fraction, fixed point, source literal, and unknown pending review. It preserves `magnitude_text`, `source_literal`, optional `precision`, optional `scale`, unit/dimension references, conversion policy, rounding policy, visibility, provenance, and metadata.

The contract correctly prohibits arithmetic, conversion, rounding execution, binary-float authority, NaN/infinity authority, and source-literal evaluation. PR-5D must separate lexical validation from arithmetic evaluation. Checking for the literal strings `NaN`, `Infinity`, malformed signs, or disallowed numeric tokens can be lexical validation; converting to `Decimal`, `Fraction`, binary float, or applying negativity rules as numeric comparison would be parsing/evaluation and must remain forbidden to PR-5A unless explicitly authorized.

## 14. CostTerm and ConsequenceTerm review

CostTerm has a governed family surface, subject/resource/quantity linkage, required timing policy, required outcome policy, visibility, owner domain, dependencies, provenance, metadata, and no execution authority. Its defaults use the correct policy surfaces or independent controlled literals.

ConsequenceTerm lawfully permits no resource or no quantity because some consequences are narrative, social, mission, location, persistent, or owner-routed consequences rather than resource deltas. However, ConsequenceTerm defaults for `timing_policy` and `outcome_policy` appear to use validation/blocking values rather than an explicitly applicable timing/outcome surface. PR-5D must define a consequence-specific timing/outcome surface, reuse cost policy surfaces explicitly, or make those values controlled independent literals.

## 15. CostBundle review

PR-5B reviews term uniqueness, alternative groups, atomicity, ordering, partial-settlement policy, membership validation, compatibility rules, and no selection or settlement. It correctly treats `term_ids` as membership only and does not select an alternative or settle a bundle.

`minimum_required_terms` and `maximum_allowed_terms` have exact Python types (`int | None`) but not exact semantics. PR-5D must define whether bounds count all terms, selected alternative terms, visible terms only, source-local retained terms, or post-validation terms; whether zero is lawful; whether negative values are rejected lexically; and whether bounds apply before or after owner handoff. Without that, PR-5A would invent validator behavior.

## 16. Request/result/proposal linkage review

Exact contracts are partly present for:

- request to command/action legality;
- request to subject and state projection;
- request to declared resources, quantities, terms, bundles, and consequences;
- result to request;
- result to stage and decision;
- result to validation and trace;
- proposal to result;
- proposal to state-delta refs;
- proposal to transaction/event prerequisites;
- proposal to validation result;
- proposal to rollback lineage.

The missing hardening is whether references must have matching typed dependencies. PR-5D should state which request/result/proposal reference fields require matching `ResourceMathDependency` records, and which are merely same-artifact internal references.

## 17. SettlementProposal boundary review

Confirmed:

- SettlementProposal is a non-mutating proposal;
- it cannot apply deltas;
- it cannot append events;
- it cannot authorize settlement;
- it cannot be mistaken for a committed transaction if false-only flags are enforced.

Not yet exact:

- `validation_result_ref` requirements are not exact because `None` is default while later settlement semantics require validation_passed before execution;
- visibility requirements are basic but hidden-info public serialization is not fully routed;
- empty `proposed_state_delta_refs` are not explicitly lawful or rejected.

PR-5D must harden these proposal-boundary rules before PR-5A.

## 18. False-only authority review

Reviewed false-only fields:

- `calculation_executed`
- `affordability_executed`
- `reservation_authorized`
- `settlement_authorized`
- `consequence_application_authorized`
- `mutation_authorized`
- `state_delta_application_authorized`
- `transaction_execution_authorized`
- `event_commitment_authorized`
- `event_append_authorized`
- `persistence_authorized`
- `replay_authorized`
- `rng_execution_authorized`
- `table_oracle_execution_authorized`
- `model_authority_authorized`
- `live_play_authorized`
- `ui_authorized`
- `conversion_authorized`
- `canon_promotion_authorized`

PR-5B consistently includes the flags on request/result/proposal. This is safe and acceptable for PR-5A. Putting every flag on every shape creates duplication, but it is useful safety at this phase rather than a blocker. PR-5D may classify placement ergonomics but should not remove safety unless a safer shared authority envelope is specified.

## 19. Factory/validator parity review

PR-5B specifies enough shared invariants for frozen objects, sequence normalization, metadata copying, duplicate detection, stage/decision compatibility intent, and false-only flags in principle. Parity is incomplete because factories and validators would still need to invent validation-posture vocabulary, typed subject pairing, consequence timing/outcome default validation, dependency-reference binding, bundle bound semantics, and settlement proposal validation rules.

## 20. Serialization and hidden-information review

PR-5B describes `to_dict()` behavior, defensive copying, metadata immutability, provenance preservation, and reference-only serialization. Hidden identifiers, hidden quantities, metadata, source literals, provenance, and dependency refs require a public serialization boundary.

PR-5A should not invent `to_public_dict()`. Public projection likely belongs to RT-005/context projection later, but PR-5D must explicitly state whether PR-5A only implements full internal `to_dict()` and rejects/omits public serialization. Hidden source literals must not leak through any public-facing serialization path.

## 21. Family-matrix corpus review

The resource, cost, and consequence families survive pressure from fantasy, sci-fi, cultivation, class/archetype, profession/occupation, point-buy, narrative/aspect, cyberware/biotech, psionics, horror/investigation, vehicles/mechs/ships, companions/summons, crafting/salvage/requisition, mission/reward, faction/debt, source-local cosmologies, generated content, and persistent campaign consequences.

Overlaps exist between cost, consequence, debt, obligation, harm, asset, and mission/faction categories, but PR-5B provides lawful destinations through source-local retention, quarantine, escalation, and named owner handoff. The taxonomy does not materially overfit one donor system.

## 22. Numeric/unit/conversion review

PR-5A is restricted to preserving exact declarations. PR-5B separates declaration preservation from numeric parsing, arithmetic, conversion, rounding, settlement, and replay concerns. Remaining hardening needed: specify which lexical checks are allowed without converting strings to numeric types, and reserve executable numeric decisions for later RT-002/RT-011/doctrine work.

PR-5A must perform no arithmetic.

## 23. Owner-boundary review

RT-002 does not absorb combat/damage, ability semantics, inventory/economy meaning, mission reward meaning, faction obligation meaning, hidden-information projection, RNG/table execution, persistence, or canon promotion. PR-5B generally preserves owner boundaries by routing these concerns to RT003, RT004, RT005, RT006, RT007, RT008, RT009, RT010, RT011, RT012, transaction/event/persistence owners, or doctrine escalation.

## 24. Risk review

| Risk | Severity | Current mitigation | Required before PR-5A | Required before executable math | Owner | PR-5D required |
|---|---|---|---|---|---|---:|
| defaults outside their constant surfaces | high | PR-5B field tables expose defaults | Align validation and consequence defaults to surfaces or controlled literals. | Numeric/execution defaults still later. | RT-002 / PR-5D | true |
| free-string validation posture | high | `validation_ready`/`validation_passed` distinction stated | Define controlled vocabulary or typed validation dependency contract. | Validation-passed execution gate. | RT-011 with RT-002 | true |
| missing subject typing | high | Subject type surface exists | Pair subject refs with subject types. | Object dereference remains later. | RT-002 with subject owners | true |
| policy/stage vocabulary collision | medium | Stage and decision tables are explicit | Define lawful dual-use or separate values. | Runtime transition model later. | RT-002 / doctrine | true |
| quarantine marked non-blocking | high | Terminal stages exist | Make quarantine blocking/terminal in decision posture. | Escalation execution bar later. | RT-002 / doctrine | true |
| terminal stage inconsistency | medium | Terminal flags listed | Remove non-blocking contradiction. | Later transition engine. | RT-002 | true |
| dependency refs not structurally linked | high | Dependency duplicate rules exist | Define matching rules for all referenced dependency IDs. | Executable dependency satisfaction later. | RT-002 with RT-001/RT-011 | true |
| quantity lexical checks accidentally parse | medium | No parsing/evaluation statement exists | Define lexical-only checks. | Numeric parser later. | RT-002 / RT-011 | true |
| bundle bounds underspecified | high | Types listed | Define minimum/maximum semantics. | Settlement selection later. | RT-002 | true |
| proposal without validation result | high | Non-mutating proposal stated | Define when `validation_result_ref=None` is lawful. | `validation_passed` before settlement. | RT-002 / RT-011 / transaction owner | true |
| proposal mistaken for committed state | high | False-only flags and prose boundary | Keep non-mutating proposal boundary. | Transaction/event commit gates. | RT-001 / transaction/event owners | false |
| hidden source literals leaking | high | Hidden-info route named | State PR-5A internal-only serialization or RT-005 public projection route. | Context projection enforcement. | RT-005 | true |
| all authority flags duplicated inconsistently | low | Flags are consistently present | No blocker; optionally define shared envelope later. | Runtime ergonomics later. | RT-002 | false |
| family taxonomy overfits donor systems | medium | Broad family matrices and source-local route | No PR-5A blocker; monitor with corpus. | Future source pressure review. | RT-002 / doctrine | false |
| PR-5A forced to invent a rule | critical | PR-5C review gate | Require PR-5D to close contract defects. | Later executable plans. | PR-5D | true |

## 25. Hardening ledger

| Item | Required correction | Owner | Required before PR-5A |
|---|---|---|---:|
| validation-posture vocabulary | Define exact allowed values or replace with typed validation dependencies. | RT-011 with RT-002 | true |
| subject typing | Add exact subject type/reference representation to future shapes. | RT-002 | true |
| default/surface compatibility | Align every default with a named surface or controlled literal. | RT-002 | true |
| consequence timing/outcome defaults | Define consequence timing/outcome surfaces or valid reuse. | RT-002 | true |
| quarantine blocking posture | Make quarantine blocking/terminal, not non-blocking planning. | RT-002 / doctrine | true |
| request dependency linkage | Define which request refs require typed dependency records. | RT-002 with RT-001 | true |
| result dependency linkage | Define result validation/dependency refs and compatibility. | RT-002 with RT-011 | true |
| proposal validation linkage | Define `validation_result_ref` lawfulness and required cases. | RT-002 with transaction/event owners | true |
| minimum/maximum bundle semantics | Define counting target, zero/negative posture, and validation phase. | RT-002 | true |
| public serialization ownership | State internal `to_dict()` only or define RT-005 public projection handoff. | RT-005 with RT-002 | true |
| quantity lexical validation | Define lexical-only checks separate from parsing/evaluation. | RT-002 / RT-011 | true |
| false-only flag placement | Keep current placement; optional later authority envelope review. | RT-002 | false |
| route to source-local/quarantine/escalation | Preserve routes and clarify blocking semantics. | RT-002 / doctrine | true |
| reserved executable numeric decisions | Reserve type selection, arithmetic, conversion, rounding, overflow, settlement. | RT-002 / RT-011 | true |

## 26. Gate decision

Chosen outcome: **HARDENING**. Material contract defects remain and require **RUNTIME-DOMAIN-PR-5D Resource and Consequence Math Final Planning Hardening** before PR-5A.

```yaml
gate_finding:
  resource_consequence_math_planning_hardening_review_complete: true
  pr_5b_scope_confirmed: true
  constant_surfaces_acceptable: partially
  default_value_compatibility_acceptable: false
  stage_model_acceptable: partially
  decision_stage_compatibility_acceptable: partially
  dataclass_contracts_implementation_ready: false
  validation_posture_contract_acceptable: false
  subject_identity_contract_acceptable: partially
  dependency_contract_acceptable: partially
  quantity_contract_acceptable: partially
  term_and_bundle_contracts_acceptable: partially
  request_result_proposal_linkage_acceptable: partially
  settlement_proposal_boundary_acceptable: partially
  false_only_authority_contract_acceptable: true
  factory_validator_parity_acceptable: partially
  corpus_scale_pressure_acceptable: true
  rt_002_owner_boundary_preserved: true
  requires_pr_5d_before_pr_5a: true
  ready_for_pr_5a_skeleton_implementation: false
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-5D resource and consequence math final planning hardening
  next_step_status: planning_hardening_pending_review
```

## 27. Recommended next PR

Recommended next PR: **RUNTIME-DOMAIN-PR-5D final planning hardening**.

Exact required corrections, without implementing them:

1. Define validation-posture vocabulary or typed validation dependency replacement.
2. Add typed subject identity to future dataclass contracts.
3. Align every default to its governing constant surface or controlled literal.
4. Correct ConsequenceTerm timing/outcome defaults.
5. Make quarantine and escalation blocking/terminal in decision posture.
6. Define request/result/proposal dependency-reference matching rules.
7. Define proposal validation-result requirements and empty proposed-delta posture.
8. Define CostBundle minimum/maximum semantics.
9. Define PR-5A serialization boundary and RT-005 public projection handoff.
10. Define lexical-only quantity validation and reserve numeric parsing/arithmetic.

## 28. Non-implementation reaffirmation

This PR-5C review implements no runtime code, no domain code, no resource calculation, no consequence calculation, no affordability execution, no reservation, no settlement, no state mutation, no state-delta application, no transaction execution, no event commitment, no event append, no persistence, no replay, no RNG/table execution, no model integration, no live-play/UI behavior, no conversion, and no canon promotion. It does not create `src/astra_runtime/domain/resource_consequence_math.py`.

## 29. Classification block

```yaml
runtime_domain_pr_5c:
  review_id: RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001
  artifact_type: resource_consequence_math_planning_hardening_review_gate
  implementation_status: non_executable_review_gate
  derives_from:
    - RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001
    - RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001
    - RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001
    - RT-002
  reviews_constant_surfaces: true
  reviews_defaults: true
  reviews_stage_model: true
  reviews_decision_stage_compatibility: true
  reviews_dataclass_contracts: true
  reviews_validation_posture: true
  reviews_subject_identity: true
  reviews_dependencies: true
  reviews_quantities: true
  reviews_terms_and_bundles: true
  reviews_request_result_proposal_linkage: true
  reviews_false_only_authority: true
  reviews_serialization: true
  reviews_corpus_scale_pressure: true
  reviews_owner_boundaries: true
  defines_hardening_ledger: true
  authorizes_runtime_code_by_this_pr: false
  authorizes_domain_code_by_this_pr: false
  authorizes_resource_calculation_by_this_pr: false
  authorizes_consequence_calculation_by_this_pr: false
  authorizes_settlement_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_event_commitment_by_this_pr: false
  authorizes_persistence_by_this_pr: false
  authorizes_rng_execution_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_conversion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-5D resource and consequence math final planning hardening
```

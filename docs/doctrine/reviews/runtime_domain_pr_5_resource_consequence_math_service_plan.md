# RUNTIME-DOMAIN-PR-5: Resource and Consequence Math Service Plan

## 1. Purpose, status, and source ledger

This is **RUNTIME-DOMAIN-PR-5** and its file identifier is **RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001**.

Status: **planning only**. This artifact plans a future resource and consequence math service for corpus-scale intake and runtime-domain sequencing. It creates no runtime/domain module, no formulas, no values, no resource pools, no economy, no parser, no evaluator, no state mutation, no event append, no persistence, no replay, no combat, no ability, no inventory, no mission, no social, no model, no live-play, no UI, no conversion, no sourcebook inclusion, and no canon promotion behavior.

Source ledger reviewed for this plan:

- `docs/doctrine/reviews/runtime_domain_pr_4f_validation_integration_residual_hardening_review.md` and **RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001**.
- `docs/doctrine/reviews/runtime_domain_pr_0_domain_service_implementation_sequencing_plan.md`.
- Owner specifications: `RT001_command_lifecycle_action_legality_owner_specification.md`, `RT002_resource_consequence_math_owner_specification.md`, `RT003_combat_hazard_damage_recovery_owner_specification.md`, `RT004_ability_effect_skill_binding_owner_specification.md`, `RT005_context_packet_hidden_information_owner_specification.md`, `RT006_mission_reward_clue_routing_owner_specification.md`, `RT007_social_faction_actor_knowledge_owner_specification.md`, `RT008_generated_content_provenance_recurrence_owner_specification.md`, `RT009_runtime_rng_table_oracle_owner_specification.md`, `RT010_inventory_item_vehicle_asset_owner_specification.md`, `RT011_validation_readiness_tooling_owner_specification.md`, and `RT012_d_series_promotion_boundary_owner_specification.md`.
- Current domain skeletons: `src/astra_runtime/domain/command_lifecycle.py`, `src/astra_runtime/domain/action_legality.py`, `src/astra_runtime/domain/state_store.py`, `src/astra_runtime/domain/state_projection.py`, `src/astra_runtime/domain/transaction_lifecycle.py`, `src/astra_runtime/domain/event_commitment.py`, and `src/astra_runtime/domain/validation_integration.py`.
- Kernel skeletons: `schema_registry`, `record_identity`, `command_envelope`, `transaction_preview`, `state_delta`, `event_ledger`, `validation_pipeline`, `hidden_information`, `context_projection`, `persistence_boundary`, `replay_audit`, `runtime_trace`, `rng_interface`, and `table_oracle`.
- Relevant A/B doctrine and C00-C14 schema families, doctrine registry `docs/doctrine/astra_doctrine_registry_v0_1.yaml`, and current decision log `docs/decisions/current_decisions_log.md`.

PR-4F authorizes PR-5 planning. It does not authorize PR-5B hardening until this plan is reviewed.

Lineage references retained for implementation sequencing: **RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001**, **RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001**, **RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001**, **RUNTIME-DOMAIN-PR-3-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SERVICE-PLAN-001**, **RUNTIME-DOMAIN-PR-2B**, **RUNTIME-DOMAIN-PR-2A**, **RUNTIME-DOMAIN-PR-1B**, **RUNTIME-DOMAIN-PR-1A**, and **RUNTIME-DOMAIN-PR-0** remain upstream context for the state, transaction, event, command, action-legality, and validation-integration boundaries.


## 2. Backend-first invariant

Astra Ascension is backend-first: **the LLM is not the game engine**. The backend owns truth, state, calculations, commitment, persistence, replay, audit, validation readiness, hidden-information enforcement, and runtime authority. LLM output may propose narrative text or structured requests only after backend-controlled boundaries permit it; generated content cannot calculate its own costs, cannot validate itself, cannot mutate state, cannot settle consequences, and cannot promote source-local donor content into canon.

The future RT-002 service must be deterministic, auditable, backend-owned, and non-authorial. It may expose reference-only planning shapes only in a later PR-5A after PR-5B hardening, but it must not make live-play decisions, execute donor code, or infer unavailable state from prose.

## 3. RT-002 ownership and explicit non-ownership

Primary ownership: RT-002 owns the future representation and calculation boundary for declared resource quantities, cost bundles, consequence quantity proposals, numeric representation requirements, unit/dimension policies, rounding/audit lineage requirements, and settlement-proposal math boundaries.

Explicit non-ownership:

- RT-001 owns command lifecycle, action legality, declaration timing, acceptance/rejection/cancellation/interruption, and commitment triggers.
- RT-003 owns combat, hazards, damage, injury, healing, recovery mechanics, and persistent harm semantics.
- RT-004 owns ability/effect/skill binding, prerequisites, activations, cooldowns, advancement hooks, and effect semantics.
- RT-005 owns hidden-information partitioning, redaction, narrator/player visibility, and context-packet projection.
- RT-006 owns mission rewards, mission penalties, clues, objective progress, and scenario routing.
- RT-007 owns social, faction, actor-knowledge, reputation, trust, and relationship consequences.
- RT-008 owns generated-content provenance, recurrence, source-local retention, and generated-content boundary controls.
- RT-009 owns RNG and table-oracle execution.
- RT-010 owns inventory, items, vehicles, assets, repair targets, salvage assets, and requisition assets.
- RT-011 owns validation readiness and tooling; `validation_ready` is not `validation_passed`.
- RT-012 owns D-series promotion and canon/sourcebook boundary governance.

## 4. Resource-model requirements without final pools

PR-5 intentionally does not choose final resource names, pools, currencies, meters, economies, or canonical values. A future resource model must support unnamed and source-local resource references, aliases, dimensions, units, provenance, visibility posture, lifecycle status, and owner-domain handoffs without asserting that any donor resource is canonical.

Required resource-reference capabilities for a future implementation:

- identify a resource by stable backend reference, source-local label, alias set, owner domain, scope, visibility posture, and provenance;
- distinguish durable pools, temporary pools, counters, charges, conditions, flags, currencies, materials, asset durability, abstract opportunities, debt-like obligations, and cooldown-like constraints without finalizing them;
- record whether the resource is authoritative, source-local retained, normalized, quarantined, or escalated;
- require validation-integration readiness before any execution path treats the reference as usable.

## 5. Planning taxonomies for resource, cost, and consequence families

Resource-family taxonomy for planning only: pooled expendables, per-encounter expendables, per-scene counters, charges, currencies, materials, item durability, vehicle/asset integrity, time/downtime, access/opportunity, social capital, faction standing, clues/information, risk/heat, corruption/strain, injury/recovery state, cooldown windows, debt/obligation, and provenance-linked source-local resources.

Cost-family taxonomy for planning only: activation cost, upkeep cost, maintenance cost, opportunity cost, prerequisite lock, reservation hold, partial payment, substitution, overcommitment, debt creation, backlash-at-success, failure-at-cost, cancellation cost, interruption cost, refund, reversal, compensation, repair cost, recovery cost, crafting cost, salvage cost, requisition cost, and validation-blocked cost.

Consequence-family taxonomy for planning only: loss, gain, transfer, lock/unlock, exposure, exhaustion, degradation, escalation, cooldown, debt, obligation, harm pressure, recovery pressure, visibility change, mission routing, clue routing, social/faction change, inventory/asset change, generated-content provenance recurrence, and quarantine/escalation outcome.

## 6. Cost lifecycle and decision models

Cost lifecycle states must remain separate: declared, normalized, calculated, affordability-checked, reservation-proposed, settlement-proposed, accepted by command lifecycle, committed by event lifecycle, persisted by persistence boundary, replayed/audited, reversed, compensated, quarantined, or escalated.

Decision model requirements:

- declaration records what a command or donor source claims;
- calculation proposes numeric consequences without mutating state;
- affordability answers whether a proposed cost can be paid under a validated state view;
- reservation proposal suggests a hold but does not hold anything;
- settlement proposal suggests final deltas but does not apply them;
- commitment belongs to transaction/event lifecycle;
- persistence and replay belong to kernel persistence/replay surfaces.

## 7. Separation of declaration, calculation, affordability, reservation, settlement, commitment, and persistence

Strict separation is mandatory. A future `ResourceMathRequest` may carry declarations and references. A future `ResourceMathResult` may carry calculated options and diagnostics. A future `SettlementProposal` may carry proposed state-delta references. None of those shapes may apply deltas, append events, mutate state, persist records, replay events, execute commands, or call a model.

The future architecture must preserve these boundaries even when donors combine costs and outcomes in one sentence. Donor prose may be split into declaration records, calculation requirements, validation requirements, and owner handoffs, but it must never become executable authority.

## 8. Cost timing and outcome policies

Timing policies must be explicit and future-only: pay-before-resolution, reserve-before-resolution, pay-on-success, pay-on-failure, pay-on-attempt, pay-on-commitment, pay-over-time, upkeep-at-interval, refund-on-cancel, no-refund-on-interrupt, compensation-after-rollback, and blocked-pending-validation. PR-5 does not choose which policy any resource uses.

Outcome policies must distinguish success, failure, partial success, cancelled, interrupted, invalid, validation-blocked, quarantined, escalated, and rollback-required outcomes. Success/failure-at-cost must be represented as policy-bound proposals, not implicit behavior.

## 9. Multi-term bundles, alternatives, atomicity, and partial settlement

A future `CostBundle` must support multiple terms, alternatives, nested groups, minimum/maximum term counts, all-or-nothing atomic bundles, best-effort bundles, ordered settlement, unordered settlement, partial settlement, and explicitly invalid mixed policies. Alternatives must remain inspectable: the backend must be able to say why an alternative was selected, blocked, unaffordable, hidden, or escalated.

Atomicity is a transaction concern. RT-002 may label requested atomicity and produce settlement proposals; RT-001/transaction/event owners decide whether a command can proceed and whether commitment is lawful.

## 10. Overcommitment, partial payment, substitution, debt, and success/failure-at-cost boundaries

Overcommitment, partial payment, substitution, debt, and success/failure-at-cost are high-risk boundaries. PR-5 records that future services must represent these as explicit policies with owner-domain review. No default overcommitment, default debt, default substitution, default partial payment, or default failure-at-cost behavior is authorized.

A future service must require source linkage, validation readiness, visibility posture, and audit lineage for each such policy. Donor mechanics that imply spending below zero, borrowing future resources, using substitute materials, or succeeding while taking backlash must be either normalized with explicit doctrine support, retained source-locally, quarantined, or escalated.

## 11. Refund, reversal, compensation, and rollback-accounting boundaries

Refunds are not automatic. Reversal is not the same as refund. Compensation is not rollback. Rollback accounting is not persistence replay. Future RT-002 work must preserve separate representations for original payment proposal, committed settlement, rollback reason, reverse delta proposal, compensation proposal, and audit lineage.

Rollback authority belongs to transaction/event/persistence/replay owners. RT-002 may propose accounting math only after an authorized future implementation exists.

## 12. Reward, loss, recovery, repair, salvage, crafting, upkeep, and requisition handoffs

RT-002 must hand off domain semantics while preserving math requirements:

- reward/loss routes to RT-006, RT-007, RT-010, RT-011, and RT-012 as applicable;
- recovery and repair route to RT-003, RT-004, RT-010, and RT-011;
- salvage, crafting, upgrades, materials, and requisition route to RT-009, RT-010, RT-011, and RT-012;
- upkeep and maintenance route to RT-001 for timing, RT-010 for assets, and RT-011 for readiness.

RT-002 may not implement combat healing, item repair, mission reward, social reputation, inventory mutation, crafting outputs, asset creation, or requisition approval.

## 13. Deterministic numeric representation requirements

Future math must be deterministic and auditable. Candidate representations include integers for countable units, `Decimal` for exact decimal policies, `Fraction` for rational source expressions, and fixed-point integers for bounded precision. PR-5 selects none as the universal answer.

Any future implementation must declare representation per quantity family, forbid binary-floating ambiguity for authoritative settlement, define overflow/underflow posture, define precision and scale, preserve exact source literals where needed, and make rounding explicit and auditable.

## 14. Units, dimensions, aliases, conversion policies, rounding, and audit lineage

A future `QuantitySpecification` must carry magnitude, representation kind, unit, dimension, alias lineage, source literal, normalization note, rounding policy, conversion policy, visibility posture, and provenance. Units and dimensions must prevent accidental conversion between incompatible concepts.

Conversion policies must be explicit: no conversion, exact conversion, table-driven conversion, doctrine-approved conversion, source-local conversion, or escalation required. Rounding policies must record direction, increment, tie-breaker, timing, and audit reason. Alias policies must preserve donor labels without treating them as final canonical names.

## 15. Safe future expression architecture

Future expression architecture must be data-only. It must use declarative expression trees or reference-only expression descriptors with whitelisted operators, typed operands, source spans, validation status, and audit lineage. There must be **no `eval`**, no `exec`, no import of donor code, no executable donor script, no runtime plugin execution from sourcebooks, and no model-authored expression authority.

Expression parsing/evaluation is not authorized by PR-5, PR-5B, or PR-5A. Future expression work must have a separate authorization and validation plan.

## 16. RNG/table-oracle handoff to RT-009

RT-002 must not roll dice, sample distributions, execute tables, choose random consequences, or implement oracle behavior. If a donor cost or consequence references chance, tables, draws, random salvage, random rewards, or random backlash, RT-002 records an RNG/table requirement and hands execution authority to RT-009 through `rng_interface` and `table_oracle` boundaries.

A future result may reference an RT-009 oracle outcome only after RT-009 has produced a backend-authoritative, auditable result.

## 17. Hidden-information and visibility requirements

Costs and consequences may be visible, hidden, partially redacted, narrator-only, actor-only, delayed, or derived. RT-002 must preserve hidden-information posture and must not leak concealed resource names, quantities, triggers, alternatives, or consequences through public summaries.

Visibility enforcement belongs to RT-005 and kernel `hidden_information` / `context_projection`. Public serialization must include only approved visible summaries and safe reason codes.

## 18. Validation-integration handoff

RT-011 and `validation_integration.py` own readiness routing. **`validation_ready` is not `validation_passed`**. A future resource/consequence math service may receive references that are ready for downstream validation, but it must not treat readiness as proof of validity, object existence, affordability, state truth, or commitment authority.

Future validation must confirm resource references, quantity representations, units, dimensions, conversion policies, rounding policies, bundle alternatives, hidden-information posture, owner handoffs, and non-implementation boundaries before any executable math is authorized.

## 19. State-delta, transaction, event, persistence, replay, and audit handoffs

RT-002 must hand off proposed state changes to `state_delta` and domain `state_store.py` / `state_projection.py` without applying them. Transaction and commitment authority belongs to `transaction_lifecycle.py`, `event_commitment.py`, `transaction_preview`, and `event_ledger`. Persistence and replay authority belongs to `persistence_boundary`, `replay_audit`, and `runtime_trace`.

A future settlement proposal may include references suitable for state-delta construction, event commitment, persistence, replay, and audit, but those systems must remain separate and backend-owned.

## 20. Future reference-only architecture for `src/astra_runtime/domain/resource_consequence_math.py`

A later PR-5A may create `src/astra_runtime/domain/resource_consequence_math.py` as a reference-only, immutable, non-calculating skeleton, but only after PR-5B planning hardening is accepted. This PR does **not** create that file, and PR-5B must not create that file either.

Future PR-5A boundaries after PR-5B review: no formulas, no final values, no resource pools, no currencies, no affordability execution, no reservation, no settlement, no consequence application, no expression parsing/evaluation, no RNG/table execution, no state mutation, no event append, no persistence, no replay, no combat, no abilities, no inventory, no mission, no social, no model/live-play/UI behavior, no conversion, no sourcebook inclusion, and no canon promotion.

## 21. Proposed immutable future shapes

Reference-only future shapes may include:

- `ResourceReference`: stable id, source label, aliases, owner domain, visibility, provenance, validation posture.
- `QuantitySpecification`: representation kind, magnitude, unit, dimension, source literal, conversion policy, rounding policy, audit lineage.
- `CostTerm`: resource reference, quantity, timing policy, outcome policy, affordability posture, substitution/debt/overcommitment flags.
- `CostBundle`: term groups, alternatives, atomicity request, partial-settlement policy, ordering, source linkage.
- `ConsequenceTerm`: consequence family, owner handoff, quantity/reference requirements, visibility, provenance, validation posture.
- `ResourceMathRequest`: command/transaction/state refs, declarations, source ledger, hidden-information posture, requested policies.
- `ResourceMathResult`: diagnostics, normalized declarations, non-mutating calculated proposals, blocked/escalated reasons, audit lineage.
- `SettlementProposal`: proposed deltas, commitment prerequisites, rollback-accounting references, visibility posture, persistence/replay handoff refs.

These shapes must be immutable and serializable. They must not perform calculation in constructors, validators, import-time code, or serialization methods.

## 22. Exact proposed planning vocabularies

The following vocabularies are proposed for PR-5B hardening review only. They are not final enums, not runtime constants, and not executable policy.

### Stage vocabulary

| proposed stage | meaning | non-authority boundary |
|---|---|---|
| `resource_math_requested` | backend received a non-executing request envelope | does not validate or calculate |
| `source_declaration_captured` | donor/local declaration is recorded with source lineage | does not normalize or canonize |
| `subject_refs_bound` | command, actor, item, asset, mission, or state subject refs are shape-bound | does not dereference existence |
| `resource_refs_declared` | resource references and aliases are declared | does not select final pools |
| `quantity_specs_declared` | quantities, units, dimensions, and literals are declared | does not choose representation globally |
| `terms_declared` | cost and consequence terms are captured | does not test affordability |
| `bundle_structure_declared` | alternatives, groups, and atomicity requests are captured | does not reserve or settle |
| `policy_refs_declared` | timing/outcome/rounding/conversion policies are named | does not execute policy |
| `dependency_refs_bound` | validation, trace, provenance, RNG/table, and owner dependencies are linked | does not call dependencies |
| `calculation_ready_for_review` | planning surface has enough data for future calculation review | not calculation passed |
| `blocked_pending_validation` | validation integration has not cleared a future executable path | not failure settlement |
| `blocked_pending_owner_handoff` | RT owner boundary must decide domain meaning | not denial by RT-002 |
| `quarantined_for_review` | donor/source pressure cannot be safely mapped | no runtime use |
| `escalated_to_doctrine` | policy gap requires doctrine decision | no canon promotion |

### Decision vocabulary

| proposed decision | compatible high-level stages | meaning |
|---|---|---|
| `accepted_for_planning` | declaration and dependency stages | shape can continue through planning |
| `normalized_for_planning` | declaration stages | source-local vocabulary was normalized with lineage |
| `source_local_retained` | declaration or owner-handoff stages | retained without canon promotion |
| `requires_validation_review` | dependency or calculation-ready stages | RT-011 readiness needed |
| `requires_owner_handoff` | owner-handoff stages | RT-001/003/004/005/006/007/008/009/010/012 decision needed |
| `blocked_missing_dependency` | dependency stages | required reference or owner link absent |
| `blocked_incompatible_policy` | policy or bundle stages | proposed policies conflict |
| `blocked_hidden_information` | visibility-sensitive stages | RT-005 visibility posture unresolved |
| `quarantined_for_review` | quarantine stage | unsafe or unsupported donor pressure |
| `escalated_to_doctrine` | escalation stage | doctrine decision required |

### Family vocabulary

Resource families: `pooled_expendable`, `scene_counter`, `charge`, `currency_like`, `material`, `asset_integrity`, `vehicle_integrity`, `time_window`, `opportunity`, `social_capital`, `faction_standing`, `clue_information`, `risk_heat`, `strain_corruption`, `injury_recovery`, `cooldown`, `debt_obligation`, `source_local_resource`.

Cost families: `activation`, `upkeep`, `maintenance`, `opportunity`, `prerequisite_lock`, `reservation_hold`, `partial_payment`, `substitution`, `overcommitment`, `debt_creation`, `success_at_cost`, `failure_at_cost`, `cancellation`, `interruption`, `refund`, `reversal`, `compensation`, `repair`, `recovery`, `crafting`, `salvage`, `requisition`, `validation_blocked`.

Consequence families: `gain`, `loss`, `transfer`, `lock`, `unlock`, `exposure`, `exhaustion`, `degradation`, `escalation`, `cooldown`, `debt`, `obligation`, `harm_pressure`, `recovery_pressure`, `visibility_change`, `mission_route`, `clue_route`, `social_faction_change`, `inventory_asset_change`, `provenance_recurrence`, `quarantine_escalation`.

### Policy vocabulary

Timing policies: `pay_before_resolution`, `reserve_before_resolution`, `pay_on_attempt`, `pay_on_success`, `pay_on_failure`, `pay_on_commitment`, `pay_over_time`, `upkeep_interval`, `refund_on_cancel`, `no_refund_on_interrupt`, `compensate_after_rollback`, `blocked_pending_validation`.

Outcome policies: `success`, `failure`, `partial_success`, `cancelled`, `interrupted`, `invalid`, `validation_blocked`, `owner_blocked`, `quarantined`, `escalated`, `rollback_required`.

Numeric policies: `integer_exact`, `decimal_exact`, `fraction_exact`, `fixed_point_scaled`, `source_literal_only`, `blocked_pending_numeric_choice`.

Conversion policies: `no_conversion`, `exact_conversion`, `table_driven_conversion`, `doctrine_approved_conversion`, `source_local_conversion`, `escalation_required`.

Rounding policies: `no_rounding`, `round_down`, `round_up`, `round_nearest`, `round_toward_zero`, `round_away_from_zero`, `tie_to_even`, `tie_away_from_zero`, `blocked_pending_rounding_choice`.

Visibility policies: `public`, `actor_visible`, `narrator_only`, `hidden`, `redacted`, `delayed_reveal`, `derived_only`.

### Quantity-kind vocabulary

Quantity kinds: `count`, `pool_amount`, `delta`, `ratio`, `percentage`, `duration`, `interval`, `threshold`, `capacity`, `rank`, `tier`, `charge_count`, `currency_amount`, `material_amount`, `durability_amount`, `debt_amount`, `source_literal_quantity`, `unknown_pending_review`.

### Atomicity vocabulary

Atomicity policies: `all_or_nothing_requested`, `best_effort_requested`, `ordered_partial_allowed`, `unordered_partial_allowed`, `alternative_exactly_one`, `alternative_at_least_one`, `alternative_at_most_one`, `alternative_any`, `invalid_mixed_atomicity`, `blocked_pending_transaction_policy`.

### Dependency vocabulary

Dependency kinds: `command_ref`, `action_legality_ref`, `state_snapshot_ref`, `state_record_ref`, `state_delta_ref`, `transaction_ref`, `transaction_preview_ref`, `event_commitment_ref`, `event_record_ref`, `validation_request_ref`, `validation_result_ref`, `runtime_trace_ref`, `hidden_information_ref`, `context_projection_ref`, `provenance_ref`, `rng_request_ref`, `table_oracle_ref`, `owner_handoff_ref`, `registry_ref`, `decision_log_ref`.

## 23. Dataclass field contracts for future reference-only shapes

These are proposed field contracts for a later PR-5A skeleton, after PR-5B hardening. They must be immutable, keyword-only if implemented, copy-safe, serialization-safe, and non-calculating.

| future shape | required field contracts | forbidden behavior |
|---|---|---|
| `ResourceReference` | `resource_ref_id`, `source_label`, `alias_labels`, `family`, `owner_domain`, `visibility_policy`, `provenance_refs`, `validation_posture`, `metadata` | no pool creation, no canonical-name selection, no dereference |
| `QuantitySpecification` | `quantity_id`, `quantity_kind`, `representation_policy`, `source_literal`, `magnitude_text`, `unit`, `dimension`, `conversion_policy`, `rounding_policy`, `audit_lineage`, `metadata` | no Decimal/Fraction conversion at construction unless separately authorized, no rounding |
| `CostTerm` | `term_id`, `resource_ref`, `quantity`, `cost_family`, `timing_policy`, `outcome_policy`, `visibility_policy`, `subject_refs`, `dependency_refs`, `provenance_refs`, `flags` | no affordability check, no reservation |
| `CostBundle` | `bundle_id`, `terms`, `alternative_groups`, `atomicity_policy`, `partial_settlement_policy`, `ordering_policy`, `subject_refs`, `dependency_refs`, `provenance_refs` | no alternative selection, no settlement |
| `ConsequenceTerm` | `consequence_id`, `consequence_family`, `quantity`, `owner_domain`, `subject_refs`, `visibility_policy`, `dependency_refs`, `provenance_refs`, `validation_posture` | no consequence application |
| `ResourceMathRequest` | `request_id`, `command_ref`, `state_refs`, `transaction_refs`, `subject_refs`, `declared_terms`, `declared_bundles`, `declared_consequences`, `dependency_refs`, `trace_ref`, `metadata` | no calculation, no state read |
| `ResourceMathResult` | `result_id`, `request_ref`, `stage`, `decision`, `diagnostics`, `normalized_terms`, `blocked_reasons`, `dependency_refs`, `trace_ref`, `validation_refs`, `metadata` | no mutation, no commitment |
| `SettlementProposal` | `proposal_id`, `result_ref`, `proposed_delta_refs`, `commitment_prerequisites`, `rollback_accounting_refs`, `visibility_policy`, `dependency_refs`, `trace_ref`, `metadata` | no delta application, no event append, no persistence |

Every future `metadata` field must be mapping-shaped, copy-safe, recursively immutable or serialized defensively, and unable to carry callable objects or executable donor code.

## 24. Factory and validator invariants

Future factories must only assemble shapes from explicit inputs, copy caller-provided collections, preserve source literals, require stable ids, and set all authority flags to false. Future validators must check shape consistency only. They must not call RNG, tables, state stores, persistence, model services, or owner-domain mechanics.

Factory/validator invariants proposed for PR-5B review:

- factory and validator parity for every future shape;
- required ids are non-empty strings and locally unique within their envelope;
- tuple/frozenset fields are immutable after construction;
- subject refs must be present before terms can be marked `calculation_ready_for_review`;
- dependency refs must declare dependency kind and target id;
- provenance refs must be present for normalized donor-derived terms;
- hidden or redacted visibility policies must block public quantity serialization;
- quantity unit and dimension must be present unless `quantity_kind` is `source_literal_quantity` or `unknown_pending_review`;
- atomicity policy must be compatible with bundle alternative structure;
- no constructor, validator, serializer, or helper may calculate affordability or settlement.

## 25. Decision/stage compatibility

Decision/stage compatibility must be table-driven and non-executing. Proposed compatibility:

| stage | allowed decisions |
|---|---|
| `resource_math_requested` | `accepted_for_planning`, `blocked_missing_dependency` |
| `source_declaration_captured` | `accepted_for_planning`, `normalized_for_planning`, `source_local_retained`, `quarantined_for_review` |
| `subject_refs_bound` | `accepted_for_planning`, `blocked_missing_dependency`, `requires_owner_handoff` |
| `resource_refs_declared` | `accepted_for_planning`, `source_local_retained`, `requires_validation_review`, `escalated_to_doctrine` |
| `quantity_specs_declared` | `accepted_for_planning`, `blocked_incompatible_policy`, `requires_validation_review` |
| `terms_declared` | `accepted_for_planning`, `requires_owner_handoff`, `blocked_hidden_information` |
| `bundle_structure_declared` | `accepted_for_planning`, `blocked_incompatible_policy` |
| `policy_refs_declared` | `accepted_for_planning`, `blocked_incompatible_policy`, `escalated_to_doctrine` |
| `dependency_refs_bound` | `accepted_for_planning`, `blocked_missing_dependency`, `requires_validation_review` |
| `calculation_ready_for_review` | `requires_validation_review`, `requires_owner_handoff`, `accepted_for_planning` |
| `blocked_pending_validation` | `requires_validation_review` |
| `blocked_pending_owner_handoff` | `requires_owner_handoff` |
| `quarantined_for_review` | `quarantined_for_review` |
| `escalated_to_doctrine` | `escalated_to_doctrine` |

PR-5B must harden this table before PR-5A creates reference-only constants.

## 26. Linkage requirements

Bundle linkage: every `CostBundle` must link term ids, alternative-group ids, atomicity policy, source declaration refs, subject refs, validation refs, dependency refs, and trace refs. A bundle cannot claim atomic readiness if any required term linkage is absent.

Term linkage: every `CostTerm` and `ConsequenceTerm` must link its subject refs, quantity spec, family, timing/outcome/visibility policies, provenance refs, validation posture, and dependency refs. Terms must not embed live state.

Subject linkage: subject refs must distinguish actor, command, item, asset, vehicle, mission, faction, location, state record, and generated-content subjects without dereferencing them.

Unit linkage: every unit must link to a dimension and conversion policy. Aliases must link to source labels and audit lineage. Unit conversion cannot occur without a conversion-policy dependency.

Provenance linkage: every normalized mapping must link source ledger entries, source-local labels, normalization notes, and donor outcome. Source-local retention must remain non-canonical.

Trace linkage: every request, result, and proposal must carry or require a `runtime_trace_ref` for audit lineage without writing a trace.

Validation linkage: every calculation-ready or settlement-proposal-shaped object must link validation request/result refs and must preserve that `validation_ready` is not `validation_passed`.

Dependency linkage: every dependency ref must include dependency kind, target id, owner domain, visibility policy, and whether the dependency is required before PR-5A, before executable calculation, or before settlement/commitment.

## 27. False-only authority flags

Future request/result/proposal shapes must expose false-only authority flags until separate implementation PRs authorize behavior:

```yaml
mutation_authorized: false
state_delta_application_authorized: false
commitment_authorized: false
event_append_authorized: false
persistence_authorized: false
replay_authorized: false
rng_execution_authorized: false
table_oracle_execution_authorized: false
model_authority_authorized: false
live_play_authorized: false
ui_authorized: false
conversion_authorized: false
canon_promotion_authorized: false
```

PR-5B must harden the exact flag names and ensure any later PR-5A skeleton can only represent false values.

## 28. Detailed resource/cost/consequence family matrices

### Resource family matrix

| family | examples of pressure | RT owner handoff | PR-5 status |
|---|---|---|---|
| pooled/counter/charge resources | points, uses, charges, counters | RT-002 with RT-011 | planning only |
| currency/material resources | money-like values, components, salvage | RT-010, RT-006, RT-012 | no final economy |
| asset integrity resources | item, vehicle, platform condition | RT-010, RT-003 | no repair math |
| time/opportunity resources | downtime, actions, windows | RT-001, RT-006 | no scheduler |
| social/faction/information resources | favor, trust, clue access | RT-005, RT-006, RT-007 | no reveal or reputation mutation |
| risk/strain/injury/cooldown resources | heat, corruption, wounds, cooldowns | RT-003, RT-004, RT-009 | no combat or ability execution |
| debt/source-local resources | obligations, local donor meters | RT-008, RT-011, RT-012 | retain/quarantine/escalate |

### Cost family matrix

| family | planning requirement | execution blocker |
|---|---|---|
| activation/upkeep/maintenance | timing and owner refs required | command lifecycle authorization |
| opportunity/prerequisite/reservation | explicit declaration and policy refs | action legality and transaction authorization |
| partial/substitution/overcommitment/debt | explicit policy, visibility, and audit refs | doctrine and validation hardening |
| success-at-cost/failure-at-cost | outcome-policy linkage | owner-domain outcome decision |
| cancellation/interruption/refund/reversal/compensation | rollback-accounting separation | transaction/event/persistence authority |
| repair/recovery/crafting/salvage/requisition | owner handoff and source lineage | RT-003/004/010/006 execution authority |
| validation-blocked | reason and dependency refs | RT-011 readiness and validation execution |

### Consequence family matrix

| family | planning requirement | owner boundary |
|---|---|---|
| gain/loss/transfer/lock/unlock | subject and quantity linkage | state/event owners |
| exposure/exhaustion/degradation/escalation | severity and visibility posture | RT-003/005/011 |
| cooldown/debt/obligation | timing and policy linkage | RT-001/004/007 |
| harm/recovery pressure | severity, duration, clearing refs | RT-003/004 |
| mission/clue/social/faction route | visibility and route refs | RT-005/006/007 |
| inventory/asset route | item/asset subject refs | RT-010 |
| provenance/quarantine/escalation | donor outcome and review refs | RT-008/011/012 |

## 29. Real decision ledger

### Required before PR-5A

- PR-5B must harden exact stage, decision, family, policy, quantity-kind, atomicity, and dependency vocabularies.
- PR-5B must harden dataclass field contracts for all proposed future shapes.
- PR-5B must harden factory/validator invariants and decision/stage compatibility.
- PR-5B must harden bundle, term, subject, unit, provenance, trace, validation, and dependency linkage.
- PR-5B must harden false-only mutation, commitment, persistence, RNG, table-oracle, model, live-play, UI, conversion, and canon-authority flags.
- PR-5B must keep `src/astra_runtime/domain/resource_consequence_math.py` absent.

### Required before executable calculation

- Numeric representation choice per quantity family must be approved.
- Unit, dimension, alias, conversion, and rounding policies must be validated.
- Expression descriptors must be separately authorized and remain data-only.
- RT-011 validation execution must exist for resource/cost/consequence readiness.
- RT-009 RNG/table outputs must be authoritative before any random cost or consequence is consumed.
- Hidden-information public/private serialization must be enforced by RT-005.

### Required before settlement or commitment

- Affordability execution must be separately authorized and tested.
- Reservation and settlement proposal generation must be separately authorized.
- Transaction lifecycle and event commitment must accept or reject proposals.
- State-delta application, event append, persistence, replay, rollback, refund, reversal, and compensation accounting must be separately authorized.
- Owner-domain mechanics for combat, abilities, inventory, mission, social, generated content, and canon boundaries must be explicit.

## 30. Resource-math invariant requirements

Future invariant requirements:

- deterministic output for identical authoritative inputs;
- no hidden state reads outside declared references;
- no binary floating-point settlement ambiguity;
- no implicit unit conversion;
- no implicit rounding;
- no implicit resource creation;
- no implicit debt or overcommitment;
- no settlement without command/transaction/event authorization;
- no public leakage of hidden costs or consequences;
- no `validation_ready` treated as `validation_passed`;
- no donor code execution;
- every normalized value retains source/audit lineage;
- every quarantine/escalation reason is explicit.

## 31. Corpus-scale donor pressure review

For roughly 200-400 mixed donor sources, resource/consequence pressure is expected to include inconsistent names, incompatible units, prose formulas, tables, random outcomes, hidden costs, optional substitutions, success-at-cost patterns, failure-at-cost patterns, partial payments, refunds, crafting/requisition economies, asset degradation, repair/recovery loops, and social/mission consequences.

The plan requires ingestion pressure handling that can classify without canonicalizing prematurely. It must tolerate repeated local vocabularies, conflicting donor economies, duplicate labels with different meanings, identical mechanics with different names, and incomplete source evidence. Backend review must prevent corpus-scale donor pressure from becoming a silent ruleset adoption.

## 32. Lawful donor outcomes

Every donor resource/cost/consequence pressure must land in one lawful outcome:

1. direct mapping to an already-authorized doctrine concept;
2. normalized mapping with preserved source/audit lineage;
3. source-local retention without canon promotion;
4. quarantine pending reviewer decision;
5. doctrine escalation for new policy or owner conflict.

No donor outcome may bypass validation readiness, hidden-information controls, owner handoffs, registry tracking, decision logging, or PR authorization.

## 33. Risk review

Risks: accidental formula adoption, hidden final resource-pool selection, donor economy leakage, implicit currencies, binary-float nondeterminism, unsafe expression evaluation, hidden-information leakage, treating affordability as settlement, treating settlement proposal as commitment, treating rollback as refund, RNG leakage into RT-002, owner-domain takeover, validation-ready confusion, and broad conversion/canon creep.

Mitigations: planning-only scope, explicit non-ownership, no code file, future immutable data-only shapes, no eval/executable donor code, RT-009 handoff, RT-005 visibility handoff, RT-011 validation handoff, transaction/event/persistence handoffs, registry/decision tracking, focused tests, and reviewer gate before PR-5B and a separate reviewer gate before PR-5A.

## 34. Hardening and decision ledger

Future hardening ledger:

- PR-5B: planning-only hardening review of vocabularies, field contracts, invariants, linkage, false-only flags, family matrices, and decision ledgers, if this plan is accepted.
- PR-5A: later reference-only non-calculating skeleton only after PR-5B closes required planning blockers.
- Later separately authorized work: numeric representation selection, expression descriptor design, validation execution, affordability execution, reservation/settlement proposal generation, and owner-specific integrations.

Decision ledger for PR-5: PR-5 records planning readiness only. It does not settle formulas, resource names, pools, currencies, economies, conversion policy, expression semantics, donor inclusion, or canon promotion.

## 35. Future test requirements

Future tests must verify immutable shapes, no import-time calculation, no binary-float settlement authority, explicit unit/dimension behavior, no implicit conversion, explicit rounding metadata, no eval/exec/imported donor code, no RNG/table execution, validation-ready versus validation-passed separation, hidden-information-safe public serialization, strict state/transaction/event/persistence separation, registry uniqueness, decision-log uniqueness, authorized domain file set, and absence of unauthorized modules before PR-5A, with PR-5B adding additional planning-hardening tests only.

PR-5 focused tests must verify this plan's required sections, IDs, gate, selected next step, registry/decision uniqueness, non-implementation boundaries, unchanged authorized domain-file set, and absence of `resource_consequence_math.py`.

## 36. PR-5B authorization boundary

PR-5B is authorized only if reviewers accept this plan as sufficiently complete. The default next step, if accepted, is **RUNTIME-DOMAIN-PR-5B: Resource and Consequence Math Planning Hardening**.

PR-5B must be planning-only and non-implementing. It may harden this plan, registry tracking, decision logging, and focused tests. It may not create runtime/domain modules or immutable dataclasses/constants. It may not implement or finalize formulas or values; final resource names or pools; final currencies or economies; affordability execution; reservation or settlement; consequence application; expression parsing/evaluation; RNG/table execution; state mutation or delta application; event append or commitment; persistence or replay; combat, abilities, inventory, mission, or social mechanics; model/live-play/UI behavior; conversion, sourcebook inclusion, or canon promotion.

## 37. Gate finding and next step

```yaml
gate_finding: ready_for_runtime_domain_pr_5b_planning_hardening
next_step_authorized: RUNTIME-DOMAIN-PR-5B Resource and Consequence Math Planning Hardening
selected_next_step: RUNTIME-DOMAIN-PR-5B: Resource and Consequence Math Planning Hardening
pr_5b_must_be_planning_only_and_non_implementing: true
runtime_code_authorized_by_this_pr: false
domain_code_authorized_by_this_pr: false
resource_consequence_math_file_created_by_this_pr: false
resource_math_authorized_by_this_pr: false
consequence_application_authorized_by_this_pr: false
formulas_or_values_authorized_by_this_pr: false
final_resource_pools_authorized_by_this_pr: false
final_currencies_or_economies_authorized_by_this_pr: false
affordability_execution_authorized_by_this_pr: false
reservation_or_settlement_authorized_by_this_pr: false
expression_parsing_or_evaluation_authorized_by_this_pr: false
rng_or_table_execution_authorized_by_this_pr: false
state_mutation_authorized_by_this_pr: false
state_delta_application_authorized_by_this_pr: false
event_append_or_commitment_authorized_by_this_pr: false
persistence_or_replay_authorized_by_this_pr: false
combat_authorized_by_this_pr: false
abilities_authorized_by_this_pr: false
inventory_authorized_by_this_pr: false
mission_authorized_by_this_pr: false
social_authorized_by_this_pr: false
model_live_play_ui_authorized_by_this_pr: false
conversion_authorized_by_this_pr: false
sourcebook_inclusion_authorized_by_this_pr: false
canon_promotion_authorized_by_this_pr: false
```

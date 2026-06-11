# RUNTIME-DOMAIN-PR-4B: Validation Integration and Invariant Enforcement Skeleton Review Gate

**Review ID:** RUNTIME-DOMAIN-PR-4B-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-REVIEW-001

**Date:** 2026-06-11

**Status:** Non-executable review/gate artifact. This review inspects PR-4A and authorizes no runtime or domain implementation.

---

## 1. PURPOSE AND STATUS

This is **RUNTIME-DOMAIN-PR-4B**. It is a non-executable review/gate artifact for **RUNTIME-DOMAIN-PR-4A-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-IMPLEMENTATION-001**.

PR-4B reviews the PR-4A validation integration and invariant enforcement skeleton against the approved **RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001** and prior domain/kernel foundations. It implements no code, adds no validation rules, and authorizes only one of two downstream paths: PR-5 planning if the skeleton is semantically safe enough, or PR-4C hardening if review finds cross-field, traceability, provenance, hidden-information, authority, or semantic-consistency gaps.

Gate outcome in this review: **PR-4C hardening is required before PR-5 planning**.

---

## 2. SOURCE LEDGER

### PR-4A implementation reviewed

- `src/astra_runtime/domain/validation_integration.py`
- `src/astra_runtime/domain/__init__.py`

### PR-4 plan reviewed

- `docs/doctrine/reviews/runtime_domain_pr_4_validation_integration_invariant_enforcement_service_plan.md`

### Prior domain foundations reviewed

- `docs/doctrine/reviews/runtime_domain_pr_3b_transaction_lifecycle_event_commitment_skeleton_review.md`
- `docs/doctrine/reviews/runtime_domain_pr_3_transaction_lifecycle_event_commitment_service_plan.md`
- `src/astra_runtime/domain/transaction_lifecycle.py`
- `src/astra_runtime/domain/event_commitment.py`
- `src/astra_runtime/domain/state_store.py`
- `src/astra_runtime/domain/state_projection.py`
- `src/astra_runtime/domain/command_lifecycle.py`
- `src/astra_runtime/domain/action_legality.py`

### Kernel skeletons reviewed

- `src/astra_runtime/kernel/schema_registry.py`
- `src/astra_runtime/kernel/record_identity.py`
- `src/astra_runtime/kernel/command_envelope.py`
- `src/astra_runtime/kernel/transaction_preview.py`
- `src/astra_runtime/kernel/state_delta.py`
- `src/astra_runtime/kernel/event_ledger.py`
- `src/astra_runtime/kernel/validation_pipeline.py`
- `src/astra_runtime/kernel/hidden_information.py`
- `src/astra_runtime/kernel/context_projection.py`
- `src/astra_runtime/kernel/persistence_boundary.py`
- `src/astra_runtime/kernel/replay_audit.py`
- `src/astra_runtime/kernel/runtime_trace.py`
- `src/astra_runtime/kernel/rng_interface.py`
- `src/astra_runtime/kernel/table_oracle.py`

### Owner specifications reviewed

- `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`
- `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`
- `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md`
- `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md`
- `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md`
- `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md`
- `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md`
- `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md`
- `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md`
- `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md`
- `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`
- `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md`

### Sequencing plan reviewed

- `docs/doctrine/reviews/runtime_domain_pr_0_domain_service_implementation_sequencing_plan.md`

### Registry and decision log reviewed

- `docs/doctrine/astra_doctrine_registry_v0_1.yaml`
- `docs/decisions/current_decisions_log.md`

### Relevant tests reviewed

- `tests/runtime/test_domain_validation_integration_skeleton.py`
- Historical runtime skeleton guardrails in `tests/runtime/`
- Registry tests in `tests/test_astra_doctrine_registry.py`

### Absent or renamed files

No required source listed for PR-4B review was absent. `src/astra_runtime/kernel/context_packet_compiler.py`, `src/astra_runtime/model`, `src/astra_runtime/prompts`, `src/astra_runtime/live_play`, `src/astra_runtime/ui`, `src/astra_runtime/database`, and `src/astra_runtime/store` remain absent and are not created by this review.

---

## 3. BACKEND-FIRST VALIDATION INVARIANT

Astra Ascension is a backend-owned runtime. **The LLM is not the game engine.** validation is backend authority, not model authority, narration authority, UI authority, donor-source authority, or generated-content authority.

Validation results may represent backend validation decisions, but a validation result cannot mutate state, cannot apply a state delta, cannot append events, cannot commit an event, cannot persist data, cannot replay data, and cannot execute a command. Model output or narration output cannot create a valid result. Source-local content, converted source-local content, generated content, examples, or donor assumptions cannot validate themselves. runtime validation cannot promote canon and cannot turn source-local material into Astra law.

---

## 4. PR-4A IMPLEMENTATION REVIEW

| artifact | expected scope | observed implementation | scope status | risks | required follow-up | downstream readiness |
|---|---|---|---|---|---|---|
| `validation_integration.py` | Constants, frozen dataclasses, factories, validators, stateless service, reference-only surfaces, false-only authority flags. | Six constant sets, five dataclasses, five factories, five validators, and a stateless wrapper exist. No kernel operation is imported or invoked. | In scope for structural skeleton. | Allows authoritative-looking success without trace/result refs and with `blocking=True`; decision/final-stage combinations are loose. | PR-4C cross-field hardening. | Not ready for PR-5 planning until hardening. |
| `domain/__init__.py` exports | Re-export PR-4A symbols only. | Exports validation integration constants, dataclasses, helpers, validators, errors, and service. | In scope. | Exporting loose result shapes increases downstream reliance risk. | Keep exports but harden semantics in PR-4C. | Partially ready. |
| Focused PR-4A tests | Cover skeleton scope, immutability, factory/validator parity, no authority flags. | Tests cover constants, dataclasses, helper validation, service statelessness, and selected parity constraints. | In scope. | Tests intentionally do not cover all cross-field success/failure/route semantics. | Add PR-4C semantic tests. | Insufficient for PR-5 planning. |
| Updated historical guardrail tests | Narrowly update domain allowlist for validation integration. | Runtime guardrails recognize `validation_integration.py` and continue blocking future service files. | Scope-safe. | Guardrails are only file-presence checks, not semantic safety checks. | Preserve guardrails; add targeted PR-4C tests. | Safe transition. |
| Registry record | Track PR-4A as narrow executable skeleton, no runtime authority expansion. | Registry records implementation posture and non-authorizations. | In scope. | Registry does not itself enforce semantic invariants. | Add PR-4B review/gate record. | Tracking ready. |
| Decision-log record | Record PR-4A implementation and next review gate. | Decision log points to PR-4B review gate. | In scope. | Decision log must capture PR-4C requirement. | Add PR-4B decision record. | Tracking ready. |

The PR-4A 28-file footprint is confirmed as limited to the authorized implementation and guardrail transition: validation integration skeleton, domain exports, focused tests, registry/decision tracking, and narrow historical guardrail updates. The footprint did not add resource math, combat, ability/effect, inventory, mission/social, context-packet compiler, model, live-play, UI, persistence, conversion, or canon behavior.

---

## 5. CONSTANT AND VOCABULARY REVIEW

| constant surface | review finding | status |
|---|---|---|
| `VALIDATION_INTEGRATION_STAGES` | Aligns with PR-4 stage vocabulary and includes request, reference binding, precheck, hidden-info, provenance, pass/fail/quarantine/escalation/cancel/supersede states. | Acceptable constants; semantic compatibility not enforced. |
| `VALIDATION_INTEGRATION_DECISIONS` | Aligns with PR-4 decision vocabulary, including ready/pass/fail, rejected-by categories, quarantine, escalation, unsupported scope. | Acceptable constants; overlapping terminal semantics require hardening. |
| `VALIDATION_INVARIANT_FAMILIES` | Covers command, action legality, state, transaction, event, delta, ledger, validation result authority, hidden info, context, persistence, replay, trace, schema, source-local, generated provenance, canon, conversion, model, live-play. | Acceptable broad vocabulary. |
| `VALIDATION_FAILURE_ROUTES` | Includes blocking, quarantine, escalation, rejection, and downstream-domain-validation routes. | Acceptable vocabulary; route/decision compatibility is underspecified. |
| `VALIDATION_DEPENDENCY_TYPES` | Represents kernel, domain, validation, hidden-info, persistence/replay/trace, provenance, source-local, canon, conversion references. | Acceptable reference-only dependency vocabulary. |
| `VALIDATION_SUBJECT_TYPES` | Represents command/action/state/transaction/event/delta/ledger/generated/source-local/canon/conversion/hidden/context/trace subjects. | Acceptable skeleton vocabulary. |

The constants are close to the PR-4 plan and do not add donor-shaped rule assumptions or canon promotion semantics. The blocking issue is not missing constants; it is that constants can be combined in contradictory ways. Decisions such as `validation_ready`, `validation_failed`, quarantine, escalation, and unsupported scope need clearer terminal-stage and route compatibility before downstream planning relies on them.

---

## 6. DATACLASS AND IMMUTABILITY REVIEW

| dataclass | review finding | concern |
|---|---|---|
| `ValidationIntegrationDependency` | Frozen, uses `MappingProxyType` when built through factory, deep-copies `metadata`, rejects bare strings through request sequence helper, and `to_dict` returns copies. | Manual construction can supply mutable nested metadata and invalid fields unless validator is called. |
| `ValidationInvariantDeclaration` | Frozen, backend-only is enforced through factory and validator, generated-content provenance invariant requires `provenance_required=True`, and `to_dict` copies metadata. | Nested metadata is not deeply frozen after construction; reference-only nature is implied rather than type-enforced. |
| `ValidationFailureRoute` | Frozen; factory and validator reject `validation_passed` routes, enforce quarantine/escalation route flags, enforce player-visible hidden-info safety, and copy metadata. | Does not enforce full route/decision/final-result compatibility or trace linkage to result `trace_id`. |
| `ValidationIntegrationRequest` | Frozen; dependencies/invariants normalize to tuples; transaction and event subjects require corresponding refs; generated provenance invariant requires generated-content refs. | Request stage can be any stage, including terminal stages, and request trace/provenance references remain only loosely coupled. |
| `ValidationIntegrationResult` | Frozen; failure route sequence normalizes to tuple; false-only authority flags are enforced; pass/decision parity partly enforced. | Passed result may omit `validation_result_ref_id`, `trace_id`, and `invariant_precheck_ref_id`, may keep `blocking=True`, may use a non-pass final stage, and may set `provenance_checked=False`. |

PR-4A has no mutable global state and the service wrapper stores no service state. Factory-created metadata is protected at the top level by `MappingProxyType` and by deep-copying caller input; `to_dict` also returns deep copies. However, nested metadata inside manually constructed frozen dataclasses can remain mutable, and validators check mapping type rather than deep immutability. This is acceptable skeleton looseness for metadata but not for success/failure authority semantics.

---

## 7. FACTORY / VALIDATOR PARITY REVIEW

| parity category | factory/validator parity | discrepancy |
|---|---|---|
| Required IDs | Factories and validators require non-empty primary IDs and refs. | No blocking discrepancy. |
| Optional IDs | Factories and validators reject empty optional refs when provided. | No blocking discrepancy. |
| Constant membership | Factories and validators check stage, decision, family, route, dependency, and subject sets. | No blocking discrepancy. |
| Boolean type enforcement | Factories and validators require actual bools. | No blocking discrepancy. |
| Sequence type enforcement | Factories reject bare strings and normalize to tuples; validators require tuples. | Manual list construction is invalid by validator; acceptable. |
| Tuple-content enforcement | Factories validate nested object types and validators; validators check tuple contents. | No blocking discrepancy. |
| Nested dependency validation | Request factory and validator validate dependencies. | No blocking discrepancy. |
| Nested invariant validation | Request factory and validator validate invariants. | No blocking discrepancy. |
| Nested failure-route validation | Result factory and validator validate failure routes. | No blocking discrepancy. |
| `backend_only` enforcement | Invariant factory and validator reject `backend_only=False`. | No blocking discrepancy. |
| Generated-content provenance requirements | Invariant factory/validator require `provenance_required=True` for generated-content provenance family; request factory/validator require generated refs for that invariant. | Result does not require `provenance_checked=True` or provenance references when passed. PR-4C required. |
| Transaction subject/reference requirements | Request factory/validator require `transaction_ref_id` for transaction subject. | Result-side transaction validity not represented. Later owner may add result dependency rules. |
| Event-commitment subject/reference requirements | Request factory/validator require `event_commitment_ref_id` for event subject. | Result-side event commitment validity not represented. Later owner may add result dependency rules. |
| Hidden-information safety | Pass requires `hidden_info_safe=True`; player-visible route requires safe flag. | Safe flags alone do not sanitize reason metadata or player-visible surfaces. PR-4C should establish boundary. |
| Quarantine requirements | Quarantine route type requires `quarantines=True`; quarantine decision requires result `quarantined=True`. | Quarantine route can pair with non-quarantine decision; quarantined result need not use quarantine final stage. PR-4C required. |
| Escalation requirements | `escalate_doctrine_gap` route requires `escalates=True`; escalation decision requires result `escalated=True`. | Escalation route can pair with non-escalation decision; escalated result need not use escalation final stage. PR-4C required. |
| False-only authority flags | Factory and validator reject state mutation, event append, persistence, and model authority flags. | No blocking discrepancy. |
| Metadata mapping validity | Factories wrap deep-copied mappings; validators require mappings. | Manual nested metadata mutability remains possible; later hardening recommended. |

Every discrepancy reachable through manual frozen-dataclass construction is listed above. The most serious discrepancy is not factory/validator drift but that both factory and validator consistently allow semantically unsafe successful and terminal results.

---

## 8. DECISION / STAGE COMPATIBILITY REVIEW

| decision | allowed final stage or stages | passed | blocking | quarantined | escalated | requires failure route | requires validation_result_ref_id | requires invariant_precheck_ref_id | requires trace_id | requires provenance_checked | hidden-info requirements | current PR-4A enforcement | recommended enforcement |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `validation_ready` | Non-terminal planning/reference stage only, not pass/fail terminal. | false | usually true | false | false | no | no | maybe | yes if emitted | no | safe flags only | Any final stage accepted. | Forbid terminal pass/fail/quarantine/escalation final stages. |
| `validation_passed` | `validation_passed` only. | true | false | false | false | no | yes | yes where precheck used | yes | yes for generated/source-local content | `hidden_info_safe=True`, no routes; refs/trace/blocking/final stage not enforced. | Require pass final stage, result ref, trace, blocking false, hidden-info safe, provenance linkage. |
| `validation_failed` | `validation_failed` only. | false | true | false | false | yes | maybe | yes where precheck used | yes | no | may need safe non-player reason | Failure route not required unless decision starts `rejected_`. | Require route or reason ref and trace. |
| `rejected_by_missing_command_ref` | `validation_failed` | false | true | false | false | yes | no | no | yes | no | safe reason code only | Requires route but not stage/trace. | Require failure stage, route compatibility, trace. |
| `rejected_by_missing_state_ref` | `validation_failed` | false | true | false | false | yes | no | no | yes | no | safe reason code only | Requires route but not stage/trace. | Require failure stage, route compatibility, trace. |
| `rejected_by_missing_transaction_ref` | `validation_failed` | false | true | false | false | yes | no | no | yes | no | safe reason code only | Requires route but not stage/trace. | Require failure stage, route compatibility, trace. |
| `rejected_by_missing_event_commitment_ref` | `validation_failed` | false | true | false | false | yes | no | no | yes | no | safe reason code only | Requires route but not stage/trace. | Require failure stage, route compatibility, trace. |
| `rejected_by_missing_invariant_set` | `validation_failed` | false | true | false | false | yes | no | maybe | yes | no | safe reason code only | Requires route but not stage/trace. | Require failure stage, invariant context, trace. |
| `rejected_by_hidden_information_risk` | `validation_failed` or `validation_quarantined` | false | true | maybe | false | yes | no | maybe | yes | no | must not expose hidden truth | Requires route but not safe reason boundary. | Require hidden-info route, non-player-visible raw reason, trace. |
| `rejected_by_provenance_gap` | `validation_failed` or `validation_quarantined` | false | true | maybe | false | yes | no | maybe | yes | false | no hidden leaks | Requires route only. | Require provenance route and trace. |
| `rejected_by_schema_mismatch` | `validation_failed` | false | true | false | false | yes | no | maybe | yes | no | safe code only | Requires route only. | Require schema mismatch route and trace. |
| `rejected_by_authority_mismatch` | `validation_failed` | false | true | false | false | yes | no | maybe | yes | no | safe code only | Requires route only. | Require authority/source-local route and trace. |
| `rejected_by_phase_boundary` | `validation_failed` | false | true | false | false | yes | no | maybe | yes | no | safe code only | Requires route only. | Require phase-boundary route and trace. |
| `quarantined_for_review` | `validation_quarantined` | false | true | true | false | yes | no | maybe | yes | no | no player-visible raw hidden truth | Requires `quarantined=True`; no route/stage/trace compatibility. | Require quarantine stage, route, trace, and quarantine route. |
| `escalated_to_doctrine` | `validation_escalated` | false | true | false | true | yes | no | maybe | yes | no | no donor/canon promotion | Requires `escalated=True`; no route/stage/trace compatibility. | Require escalation stage, route, trace, doctrine-gap route. |
| `unsupported_validation_scope` | `validation_failed` or `validation_escalated` | false | true | maybe | maybe | yes | no | no | yes | no | safe code only | No route/stage/trace requirement. | Require route and either block or escalate according to owner gap. |

The matrix shows PR-4A currently permits loose combinations that can appear authoritative while lacking the evidence references required for audit, replay, and downstream safety.

---

## 9. SUCCESS-RESULT SEMANTIC REVIEW

1. `decision="validation_passed"` should require `passed=True`, `final_stage="validation_passed"`, `blocking=False`, `validation_result_ref_id`, `trace_id`, `hidden_info_safe=True`, and no failure routes. Current PR-4A enforces only passed parity, hidden-info safe, and empty routes. **Classification: hardening required before PR-5.**
2. A successful result should not lawfully omit `validation_result_ref_id` or `trace_id`; `invariant_precheck_ref_id` should be required when the request declares invariant prechecks or blocking invariants. **Classification: hardening required before PR-5 for result/trace, PR-4C or named RT-011 rule for conditional precheck.**
3. A passed generated-content validation should require `provenance_checked=True`, a provenance reference, and a generated-content reference. **Classification: hardening required before PR-5 for the skeleton linkage; RT-008 owns later executable provenance semantics.**
4. `validation_ready` should be non-terminal planning/readiness state, not a terminal validation result that can masquerade as pass/fail/quarantine/escalation. **Classification: hardening required before PR-5.**
5. `validation_failed` should not exist without a failure route or reason reference. **Classification: hardening required before PR-5.**

No issue above is merely acceptable skeleton looseness because downstream PR-5 planning would otherwise have to reason against ambiguous validation authority.

---

## 10. FAILURE-ROUTE SEMANTIC REVIEW

PR-4A recognizes the following route vocabulary: `block_command_before_transaction`, `block_transaction_before_commitment`, `block_event_commitment`, `quarantine_transaction`, `quarantine_event_commitment`, `quarantine_generated_content`, `escalate_doctrine_gap`, `reject_source_local_authority`, `reject_hidden_info_leak`, `reject_schema_mismatch`, `reject_phase_boundary_violation`, and `request_downstream_domain_validation`.

Current behavior permits contradictory combinations:

- A quarantine route can be paired with a non-quarantine decision if `quarantines=True`.
- An escalation route can be paired with a non-escalation decision if `escalates=True`.
- A rejection or blocking route can be paired with `validation_ready`.
- A blocking route can be marked `blocking=False` except for no route-specific blocking consistency rule.
- `trace_required=True` on a route is not connected to result `trace_id`.
- `player_visible=True` with `hidden_info_safe=True` still permits raw metadata or future reason text to leak backend-sensitive information because no sanitized reason-code boundary exists.

PR-4C must define and test a compatibility map. PR-4B must not implement it.

---

## 11. TRACE, AUDIT, AND REPLAY REVIEW

Failure routes declaring `trace_required=True` are not linked to `ValidationIntegrationResult.trace_id`. Successful validation can omit `trace_id`; rejected validation can omit `trace_id`; quarantined or escalated validation can omit `trace_id`; `validation_failed` can omit both trace and route. Replay/audit references are represented only through dependency types and optional ref fields, and runtime trace remains reference-only. No replay, persistence, event append, or state effect exists.

Because validation can emit authoritative-looking success or rejection without an auditable reference, PR-4C is required before PR-5 planning.

---

## 12. HIDDEN-INFORMATION REVIEW

PR-4A includes `hidden_info_safe` on dependencies, invariants, routes, and results; `player_visible` on routes; `backend_only` on invariants; hidden-information reference fields on requests; and context projection reference fields. The service does not implement hidden-information projection, visibility-tier calculation, summarization, or redaction.

Safe flags alone are not sufficient for future player-visible output. Raw metadata or reason text could later leak hidden truth even when `hidden_info_safe=True`; PR-4C should require sanitized reason-code posture for player-visible failure routes and should keep backend-only reason payloads separate from player-visible summaries. No hidden-information projection or summarization is implemented by PR-4A or PR-4B.

---

## 13. PROVENANCE, SOURCE-LOCAL, CONVERSION, AND CANON REVIEW

The skeleton lawfully distinguishes generated content, source-local converted content, conversion artifacts, canon references, runtime validation, and doctrine escalation through invariant families, dependency types, and subject types. Passing runtime validation does not promote canon. Source-local content cannot become authoritative merely by validation. Donor assumptions cannot become Astra law. Doctrine escalation remains separate from runtime success.

Missing cross-field invariants remain: passed generated-content results do not require `provenance_checked=True`; result objects do not carry explicit generated-content/provenance references; source-local rejection routes are not forced for source-local authority mismatches; conversion/canon subjects can receive generic success without explicit canon-boundary evidence. PR-4C should add skeleton-level linkage without implementing conversion, promotion, or canon behavior.

---

## 14. ANTI-AUTHORITY AND NON-EXECUTION REVIEW

Direct review of imports and methods confirms no calls to `run_validation_checks`, no calls to `run_invariant_prechecks`, no actual invariant evaluation, no state mutation, no delta application, no event append, no transaction execution, no persistence, no replay, no command execution, no RNG execution, no table/oracle execution, no model call, no prompt behavior, and no live-play or UI behavior.

`ValidationIntegrationService` exposes only create/validate wrapper methods. It has no forbidden execution-style methods and no service state. Anti-authority guardrails are acceptable.

---

## 15. KERNEL DEPENDENCY REVIEW

| kernel dependency | imported by PR-4A | referenced through ID fields | operationally invoked | acceptable at skeleton stage | future integration owner | risk if operationalized prematurely |
|---|---:|---:|---:|---:|---|---|
| `schema_registry` | no | yes | no | yes | RT-011 | Schema checks could become ad hoc validation rules. |
| `record_identity` | no | yes | no | yes | RT-011 / RT-008 | Identity refs could be treated as canon authority. |
| `command_envelope` | no | yes | no | yes | RT-001 | Commands could bypass lifecycle legality. |
| `transaction_preview` | no | yes | no | yes | RT-001 / RT-002 | Preview could become transaction execution. |
| `state_delta` | no | yes | no | yes | RT-002+ | Delta refs could become delta application. |
| `event_ledger` | no | yes | no | yes | RT-001 / persistence owners | Ledger refs could become event append. |
| `validation_pipeline` | no | yes | no | yes | RT-011 | Pipeline could execute before invariant semantics are hardened. |
| `hidden_information` | no | yes | no | yes | RT-005 | Hidden info checks could leak or reveal truth. |
| `context_projection` | no | yes | no | yes | RT-005 | Projection refs could become context packet compilation. |
| `persistence_boundary` | no | yes | no | yes | persistence/replay owners | Validation could persist side effects. |
| `replay_audit` | no | yes | no | yes | persistence/replay owners | Audit refs could be faked without trace. |
| `runtime_trace` | no | yes | no | yes | RT-011 | Trace-less decisions would undermine audit. |
| `rng_interface` | no | no | no | yes | RT-009 | Randomness could enter validation authority. |
| `table_oracle` | no | no | no | yes | RT-009 | Oracle rolls could become rules. |

Expected posture is satisfied operationally: reference-only now; no kernel invocation; no persistence/replay/event/state effects; `validation_pipeline` remains future integration.

---

## 16. DOMAIN HANDOFF REVIEW

| handoff | PR-4A references can represent | decisions PR-4A must not make | validation dependency needed | remaining blocked behavior |
|---|---|---|---|---|
| command lifecycle | command refs, command lifecycle refs, command authority invariant | whether command executes | command envelope/lifecycle validation result | command execution |
| action legality | legality refs and invariants | final action legality beyond refs | legality result dependency | legality rules expansion |
| state store | state record/snapshot refs | state mutation | state record dependency | state writes |
| state projection | projection refs and visibility invariant | visibility calculation | projection dependency | projection compilation |
| transaction lifecycle | transaction refs/plans/results | transaction execution/readiness based on weak validation | transaction validation result | transaction execution |
| event commitment | event commitment refs/results | event append/commit | event validation result | actual event commitment |
| future resource/consequence math | downstream validation route/dependency | resource math | resource validation dependency | all resource arithmetic |
| future combat/hazard/damage/recovery | invariant family pressure only | combat outcome | combat validation dependency | damage/recovery resolution |
| future ability/effect/skill binding | generic dependency/invariant refs | effect resolution | ability validation dependency | ability execution |
| future inventory/item/vehicle | generic dependency refs | inventory mutation | inventory validation dependency | item/vehicle mutation |
| mission/reward/clue | generic dependency refs | rewards or clues | mission validation dependency | mission/social mutation |
| social/faction/actor knowledge | hidden-info and social owner refs | actor knowledge updates | social validation dependency | knowledge mutation |
| generated-content provenance | generated-content refs and provenance invariant | persistence/canon promotion | provenance dependency | content persistence/promote |
| context-packet compiler | hidden/context refs | packet compilation | context validation dependency | context packet generation |
| model evaluation | model non-authority invariant | model validation authority | model-output rejection dependency | model integration |
| live play | live-play non-authority invariant | live-play state changes | live-play gate dependency | live-play adapter |

---

## 17. CORPUS-SCALE PRESSURE REVIEW

| pressure source | invariant family required | PR-4A can represent request | PR-4A can represent rejection/quarantine/escalation | downstream owner | gap |
|---|---|---:|---:|---|---|
| class/archetype systems | schema, source-local, validation result | yes | yes | RT-002/RT-004 | Need owner-specific invariant details. |
| point-buy systems | resource/consequence, schema | yes | yes | RT-002 | No math semantics yet. |
| profession/occupation systems | schema, source-local | yes | yes | RT-002/RT-006 | Donor assumptions must not become law. |
| narrative tags/aspects | action legality, hidden info | yes | yes | RT-001/RT-005 | Tag semantics remain undefined. |
| cultivation systems | resource, ability, canon boundary | yes | yes | RT-002/RT-004 | Mixed progression schemas need owner mapping. |
| cyberware/biotech | inventory, resource, hidden info | yes | yes | RT-010/RT-002 | Installation/mutation not represented. |
| psionics | ability/effect, hidden info | yes | yes | RT-004/RT-005 | Hidden actor knowledge risk. |
| horror/investigation | hidden info, clue routing | yes | yes | RT-005/RT-006 | Player-visible reasons need sanitization. |
| vehicles/mechs/ships | inventory/vehicle, combat, resource | yes | yes | RT-010/RT-003 | Vehicle state/mutation absent. |
| companions/summons | social/actor knowledge, combat | yes | yes | RT-007/RT-003 | Actor knowledge and ownership gap. |
| crafting/salvage/requisition | inventory, resource | yes | yes | RT-010/RT-002 | Resource math absent. |
| random tables/oracles | RNG/table oracle | partly | yes | RT-009 | No RNG refs in subject types; avoid execution. |
| source-local cosmologies | source-local, canon, conversion | yes | yes | RT-012 | Canon boundary needs strict linkage. |
| adventure paths | mission/clue, hidden info | yes | yes | RT-006/RT-005 | Spoiler leak risk. |
| mixed-genre cross-book interactions | schema, authority, source-local | yes | yes | RT-011/all RTs | Cross-owner invariant routing needed. |
| generated content | provenance, generated content | yes | yes | RT-008 | Passed result provenance linkage missing. |
| hidden actor knowledge | hidden-information partition | yes | yes | RT-005/RT-007 | Reason-code boundary missing. |
| persistent world changes | persistence, replay, event ledger | yes | yes | persistence/replay owners | No mutation/persistence allowed. |

PR-4A vocabulary can represent broad corpus-scale validation pressure, but the successful-result and route semantics are not safe enough for downstream planning.

---

## 18. RISK REVIEW

| risk | severity | affected RT owners | mitigation | required test family | PR-4C required |
|---|---|---|---|---|---:|
| validation service becomes universal rule engine | high | RT-011/all | Keep reference-only and no execution methods. | anti-execution tests | false |
| decision/stage combinations permit false success | critical | RT-011/RT-001 | Enforce decision/final-stage compatibility. | semantic matrix tests | true |
| passed results lack traceability | critical | RT-011 | Require result ref and trace id. | success trace tests | true |
| blocking remains true on passed results | high | RT-001/RT-002 | Require `blocking=False` for pass. | success flag tests | true |
| failed results lack failure routes | high | RT-011 | Require route/reason for terminal failure. | failure route tests | true |
| quarantine/escalation flags drift from decisions | high | RT-011/RT-008 | Enforce decision/stage/route compatibility. | quarantine/escalation tests | true |
| failure-route types mismatch decisions | high | RT-011 | Add compatibility map. | route matrix tests | true |
| generated content passes without checked provenance | critical | RT-008/RT-011 | Require provenance_checked and refs. | provenance pass tests | true |
| hidden data leaks through metadata or reason fields | high | RT-005 | Require sanitized reason-code boundary. | hidden-info reason tests | true |
| model text becomes validation authority | critical | RT-011 | Maintain model authority false-only checks. | anti-model tests | false |
| source-local content becomes runtime or canon authority | critical | RT-012/RT-008 | Enforce source-local/canon boundary. | authority mismatch tests | true |
| validation result mutates state indirectly | critical | RT-001/RT-002 | Keep state mutation false-only. | anti-mutation tests | false |
| event commitment bypasses validation | high | RT-001 | Require strong validation refs before commitment later. | handoff tests | true |
| transaction readiness accepts weak validation | high | RT-001/RT-002 | Require auditable pass semantics. | transaction handoff tests | true |
| future resource math relies on ambiguous validation results | high | RT-002 | Block PR-5 until PR-4C. | PR-5 gate tests | true |
| validator parity drifts from factories | medium | RT-011 | Maintain manual-construction tests. | factory/validator parity tests | false |
| historical guardrail tests are weakened rather than narrowly updated | medium | RT-011 | Preserve exact absent-file checks. | guardrail tests | false |

---

## 19. HARDENING LEDGER

| hardening ID | issue | current behavior | desired invariant | severity | required before PR-5 planning | required before PR-5 implementation | required before executable validation integration | future owner | recommended PR |
|---|---|---|---|---|---:|---:|---:|---|---|
| PR4C-H01 | success requires `validation_result_ref_id` | pass may omit ref | pass must carry backend validation result ref | critical | true | true | true | RT-011 | PR-4C |
| PR4C-H02 | success requires `trace_id` | pass may omit trace | pass must carry runtime trace ref | critical | true | true | true | RT-011 | PR-4C |
| PR4C-H03 | success requires `blocking=False` | pass defaults to `blocking=True` | pass cannot remain blocking | high | true | true | true | RT-001/RT-011 | PR-4C |
| PR4C-H04 | decision/final-stage compatibility | any known stage accepted | decision determines allowed terminal stage | critical | true | true | true | RT-011 | PR-4C |
| PR4C-H05 | failed result route requirement | `validation_failed` may have no route | terminal failure requires route/reason ref | high | true | true | true | RT-011 | PR-4C |
| PR4C-H06 | quarantine decision/route compatibility | partial flags only | quarantine decision/stage/route must align | high | true | true | true | RT-011/RT-008 | PR-4C |
| PR4C-H07 | escalation decision/route compatibility | partial flags only | escalation decision/stage/route must align | high | true | true | true | RT-011/RT-012 | PR-4C |
| PR4C-H08 | `trace_required` linkage | route trace flag not linked | trace-required route requires result trace | high | true | true | true | RT-011 | PR-4C |
| PR4C-H09 | generated-content `provenance_checked` linkage | pass can set false | generated pass requires checked provenance and refs | critical | true | true | true | RT-008/RT-011 | PR-4C |
| PR4C-H10 | hidden-info sanitized reason boundary | safe flag only | player-visible routes expose only sanitized reason codes | high | true | true | true | RT-005 | PR-4C |
| PR4C-H11 | unsupported scope behavior | can be route-less and stage-less | unsupported scope blocks or escalates with trace | high | true | true | true | RT-011/all | PR-4C |
| PR4C-H12 | `validation_ready` terminality | can pair with terminal stage | readiness is non-terminal only | high | true | true | true | RT-011 | PR-4C |
| PR4C-H13 | invariant precheck refs | pass/fail can omit precheck refs | blocking invariant outcomes reference precheck where applicable | medium | true | true | true | RT-011 | PR-4C |
| PR4C-H14 | failure-route blocking consistency | blocking routes can be non-blocking | block routes require `blocking=True` | high | true | true | true | RT-011/RT-001 | PR-4C |

---

## 20. GATE DECISION

```yaml
gate_finding:
  validation_integration_skeleton_review_complete: true
  pr_4a_scope_confirmed: true
  constant_surface_acceptable: true
  dataclass_surface_acceptable: partially
  factory_validator_parity_acceptable: partially
  decision_stage_semantics_acceptable_for_next_planning_step: false
  anti_authority_guardrails_acceptable: true
  trace_audit_posture_acceptable_for_next_planning_step: false
  hidden_information_posture_acceptable: partially
  provenance_authority_posture_acceptable: partially
  domain_package_guardrail_transition_safe: true
  requires_pr_4c_hardening_before_pr_5: true
  ready_for_runtime_domain_pr_5_planning: false
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-4C validation integration skeleton hardening
  next_step_status: narrow_skeleton_hardening_pending_review
```

---

## 21. RECOMMENDED NEXT PR

Recommended next PR: **RUNTIME-DOMAIN-PR-4C: Validation Integration and Invariant Enforcement Skeleton Hardening**.

Required PR-4C code/test changes, not implemented in PR-4B:

- Add decision/final-stage compatibility enforcement and tests.
- Require `validation_passed` results to carry `validation_result_ref_id`, `trace_id`, `blocking=False`, `hidden_info_safe=True`, no failure routes, and `final_stage="validation_passed"`.
- Require terminal failures, quarantines, escalations, and unsupported scopes to carry compatible failure routes or reason references and trace IDs.
- Link route `trace_required=True` to result `trace_id`.
- Enforce quarantine and escalation route/decision/stage compatibility.
- Enforce generated-content pass provenance linkage, including `provenance_checked=True` and required generated/provenance refs where applicable.
- Define hidden-info safe player-visible reason-code boundaries without implementing projection or summarization.
- Preserve all anti-authority false-only flags and no-execution guardrails.

---

## 22. NON-IMPLEMENTATION REAFFIRMATION

PR-4B adds no runtime code, domain-service code, validation implementation changes, invariant enforcement, validation pipeline execution, state mutation, delta application, event append, transaction execution, event commitment, persistence, replay, command execution, resource math, combat, abilities, inventory, mission/social behavior, generated-content persistence, context-packet compiler, model integration, live-play adapter, UI, conversion, sourcebook inclusion, or canon promotion.

---

## 23. CLASSIFICATION BLOCK

```yaml
runtime_domain_pr_4b:
  review_id: RUNTIME-DOMAIN-PR-4B-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-REVIEW-001
  artifact_type: validation_integration_invariant_enforcement_skeleton_review_gate
  implementation_status: non_executable_review_gate
  derives_from:
    - RUNTIME-DOMAIN-PR-4A-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-IMPLEMENTATION-001
    - RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001
    - RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001
    - RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
    - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
    - RT-001
    - RT-002
    - RT-005
    - RT-008
    - RT-011
  reviews_validation_integration_skeleton: true
  reviews_invariant_declaration_skeleton: true
  reviews_validation_result_skeleton: true
  reviews_failure_route_skeleton: true
  reviews_factory_validator_parity: true
  reviews_decision_stage_compatibility: true
  reviews_trace_audit_posture: true
  reviews_hidden_information_posture: true
  reviews_provenance_authority_posture: true
  reviews_anti_authority_guardrails: true
  reviews_domain_package_guardrails: true
  reviews_kernel_dependency_usage: true
  reviews_corpus_scale_validation_pressure: true
  defines_hardening_ledger: true
  authorizes_runtime_code_by_this_pr: false
  authorizes_domain_code_by_this_pr: false
  authorizes_validation_rule_execution_by_this_pr: false
  authorizes_invariant_enforcement_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_state_delta_application_by_this_pr: false
  authorizes_event_ledger_append_by_this_pr: false
  authorizes_transaction_execution_by_this_pr: false
  authorizes_actual_event_commitment_by_this_pr: false
  authorizes_persistence_by_this_pr: false
  authorizes_replay_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_resource_math_by_this_pr: false
  authorizes_combat_by_this_pr: false
  authorizes_abilities_effects_by_this_pr: false
  authorizes_inventory_mutation_by_this_pr: false
  authorizes_mission_social_mutation_by_this_pr: false
  authorizes_generated_content_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-4C validation integration skeleton hardening, pending review
```

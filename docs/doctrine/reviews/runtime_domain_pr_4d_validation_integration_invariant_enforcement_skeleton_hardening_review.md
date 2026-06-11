# RUNTIME-DOMAIN-PR-4D: Validation Integration and Invariant Enforcement Skeleton Hardening Review Gate

Review ID: RUNTIME-DOMAIN-PR-4D-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-REVIEW-001
Date: 2026-06-11
Status: non-executable review/gate

---

## 1. PURPOSE AND STATUS

This is RUNTIME-DOMAIN-PR-4D. It is a non-executable review/gate artifact that reviews PR-4C, `RUNTIME-DOMAIN-PR-4C-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-001`.

PR-4D implements no code and authorizes only one downstream path: either PR-5 planning or PR-4E hardening, depending on repository evidence. PR-5 remains blocked until this gate is accepted. This review does not authorize validation execution, invariant evaluation, mutation, event append, persistence, replay, resource math, model integration, live play, conversion, sourcebook inclusion, or canon promotion.

## 2. SOURCE LEDGER

### PR-4C implementation reviewed
- `src/astra_runtime/domain/validation_integration.py`
- `src/astra_runtime/domain/__init__.py`

### PR-4C tests reviewed
- `tests/runtime/test_domain_validation_integration_hardening.py`
- `tests/runtime/test_domain_validation_integration_skeleton.py`

### PR-4B findings reviewed
- `docs/doctrine/reviews/runtime_domain_pr_4b_validation_integration_invariant_enforcement_skeleton_review.md`

### PR-4 plan reviewed
- `docs/doctrine/reviews/runtime_domain_pr_4_validation_integration_invariant_enforcement_service_plan.md`

### Prior domain foundations reviewed
- `docs/doctrine/reviews/runtime_domain_pr_3b_transaction_lifecycle_event_commitment_skeleton_review.md`
- `docs/doctrine/reviews/runtime_domain_pr_3_transaction_lifecycle_event_commitment_service_plan.md`

### Sequencing plan reviewed
- `docs/doctrine/reviews/runtime_domain_pr_0_domain_service_implementation_sequencing_plan.md`

### Related domain surfaces reviewed
- `src/astra_runtime/domain/command_lifecycle.py`
- `src/astra_runtime/domain/action_legality.py`
- `src/astra_runtime/domain/state_store.py`
- `src/astra_runtime/domain/state_projection.py`
- `src/astra_runtime/domain/transaction_lifecycle.py`
- `src/astra_runtime/domain/event_commitment.py`

### Kernel references reviewed
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

### Registry and decision log reviewed
- `docs/doctrine/astra_doctrine_registry_v0_1.yaml`
- `docs/decisions/current_decisions_log.md`

### Absent or renamed sources
No required source was absent or renamed. The future runtime surfaces listed in this review remain absent and were not created.

## 3. BACKEND-FIRST VALIDATION INVARIANT

Astra Ascension is a backend-owned runtime. **The LLM is not the game engine.** Validation is backend authority.

Validation artifacts cannot mutate state. Validation artifacts cannot append or commit events. Validation artifacts cannot persist or replay. Public validation output must be sanitized. Generated content cannot validate itself. Source-local content cannot become canon through runtime validation. Validation remains separate from resource/consequence calculation.

Model text, narration, UI text, donor assumptions, source-local converted content, generated content, and examples cannot validate themselves. Runtime validation cannot promote canon.

## 4. PR-4C IMPLEMENTATION REVIEW

| artifact | required hardening | observed implementation | status | residual risk | required follow-up | readiness for PR-5 planning |
|---|---|---|---|---|---|---|
| `validation_integration.py` | Enforce decision/stage compatibility, terminal references, traces, route semantics, success invariants, provenance linkage, sanitized public routes, and false-only authority flags. | Constants, private compatibility maps, frozen dataclasses, factories, validators, public serialization, and stateless service are present. | partially closed | Result aggregates can accept failure routes whose `subject_ref_id` differs from the result subject; results have no request-subject linkage; trace/result/provenance references are shape-only. | PR-4E should add narrow aggregate identity/linkage hardening. | not ready |
| `domain/__init__.py` export update | Export PR-4C public constants and helpers without exposing private compatibility maps. | Public PR-4C symbols are re-exported; private maps remain private. | closed | Exported results may still be semantically ambiguous until aggregate hardening. | Preserve exports while hardening internals. | not ready |
| validation integration hardening tests | Cover PR-4B blocker hardening. | Focused PR-4C tests cover route compatibility, public reasons, request stages, terminal references, success invariants, and validator parity. | partially closed | Tests do not block route/result subject mismatch or request/result detachment. | Add PR-4E tests for residual object-shape issues. | not ready |
| updated validation integration skeleton tests | Preserve skeleton coverage while accepting PR-4C hardening. | Existing skeleton tests exercise constants, dataclasses, factories, validators, service wrapper, and non-authority flags. | closed | Skeleton tests are broad but not exhaustive aggregate semantic tests. | Keep as regression suite. | not ready |
| registry record | Track PR-4C as hardening only. | Registry records PR-4C scope and non-authorizations. | closed | Registry cannot enforce code semantics. | Add this PR-4D record. | tracking ready |
| decision-log record | Record PR-4C and block PR-5 pending PR-4D. | Decision log records PR-4C hardening and next PR-4D gate. | closed | Decision log must now record PR-4D finding. | Add this PR-4D decision. | tracking ready |

The six-file PR-4C footprint remained within its authorized PR-4C scope: `validation_integration.py`, `domain/__init__.py`, hardening tests, skeleton tests, registry, and decision log. PR-4C did not add resource math, combat, ability/effect, inventory, mission/social, generated-content persistence, context-packet compilation, model, live-play, UI, conversion, sourcebook, or canon behavior.

## 5. PR-4B BLOCKER CLOSURE MATRIX

| PR-4B finding | PR-4C mechanism | factory enforcement | validator enforcement | focused test coverage | closure status | residual concern |
|---|---|---|---|---|---|---|
| successful result requires validation_result_ref_id | Non-ready decisions require non-empty `validation_result_ref_id`; success is non-ready. | yes | yes | yes | closed | Reference identity is shape-only. |
| successful result requires trace_id | Every result requires non-empty `trace_id`. | yes | yes | yes | closed | Trace is not linked to a dependency object. |
| successful result requires blocking=False | `blocking` must be false iff decision is `validation_passed`. | yes | yes | yes | closed | None for PR-4B blocker. |
| decision/final-stage compatibility | `_DECISION_FINAL_STAGE_COMPATIBILITY`. | yes | yes | yes | closed | Intermediate-ready flag contradictions remain. |
| terminal validation failure requires routes | Non-passed non-ready decisions require routes. | yes | yes | yes | closed | Aggregate route subject can differ from result subject. |
| rejected decisions require matching routes | Rejected decisions require route decision match. | yes | yes | yes | closed | Some routes can still point to a different subject. |
| quarantine route/decision compatibility | Quarantine decision requires quarantine routes. | yes | yes | yes | closed | None for route type compatibility. |
| escalation route/decision compatibility | Escalation decision requires doctrine escalation route. | yes | yes | yes | closed | Public escalation flag disclosure is deferred. |
| trace_required linkage | Routes require `trace_required=True`; results require trace. | yes | yes | yes | closed | Trace semantic identity is not verified. |
| generated-content provenance_checked linkage | Provenance refs require `provenance_checked=True`; generated-content pass requires it. | yes | yes | yes | closed | Stage/flag contradiction for ready `provenance_checked` remains. |
| generated-content provenance reference linkage | Generated-content pass requires non-empty provenance refs. | yes | yes | yes | closed | References are untyped and not linked to generated subject. |
| hidden-information sanitized reason boundary | Public reason vocabulary and `to_public_dict()` sanitization. | yes | yes | yes | closed | Quarantine/escalation boolean disclosure is acceptable only as skeleton posture, with PR-4E review. |
| unsupported-scope routing | Unsupported scope requires downstream validation route. | yes | yes | yes | closed | Consumers must not treat unsupported scope as ordinary failure. |
| validation_ready terminality | Ready can only use intermediate/future coordination stages. | yes | yes | yes | closed | Ready can carry hidden-info unsafe posture, which is a residual ambiguity. |
| invariant-precheck reference requirement | Precheck stages require `invariant_precheck_ref_id`. | yes | yes | yes | closed | None for blocker. |
| failure-route blocking consistency | Every route must be blocking and trace-required. | yes | yes | yes | closed | Route aggregate subject mismatch remains. |
| factory/validator parity | Factories call shared validators and validators reuse semantic helpers. | yes | yes | yes | closed | No factory-only PR-4C rule observed. |

## 6. CONSTANT AND COMPATIBILITY MAP REVIEW

Reviewed `VALIDATION_PUBLIC_REASON_CODES`, `_REQUESTABLE_VALIDATION_STAGES`, `_QUARANTINE_FAILURE_ROUTES`, `_ROUTE_DECISION_COMPATIBILITY`, `_PUBLIC_REASON_COMPATIBILITY`, and `_DECISION_FINAL_STAGE_COMPATIBILITY`.

| map | completeness | internal consistency | immutable posture | orphan/unreachable check | authority posture | future corpus-scale extensibility |
|---|---|---|---|---|---|---|
| `VALIDATION_PUBLIC_REASON_CODES` | Covers pending, blocked, rejected, quarantined, escalated, unsupported. | Consistent with public serialization. | `frozenset`. | No code with no lawful consumer for current decisions. | Sanitized; no raw route or backend IDs. | Acceptable, but future RT owners may need more non-sensitive buckets. |
| `_REQUESTABLE_VALIDATION_STAGES` | Excludes terminal and completed outcome stages. | Consistent with request validation. | `frozenset`. | No terminal stage requestable. | Does not authorize completed outcomes. | Extensible by adding request-only stages. |
| `_QUARANTINE_FAILURE_ROUTES` | Includes all current quarantine route types. | Drives exact quarantine flag checking. | `frozenset`. | No quarantine route outside set. | Does not execute quarantine. | Extensible for future quarantine owners. |
| `_ROUTE_DECISION_COMPATIBILITY` | Covers all current route types. | Each route has legal decisions. | `MappingProxyType` containing `frozenset`s. | No route with zero legal decisions. | Reference-only routing, no mutation. | Good, but aggregate subject equality is missing. |
| `_PUBLIC_REASON_COMPATIBILITY` | Covers non-rejected public decisions; rejected decisions handled by helper. | Decision to public code mapping is sanitized. | `MappingProxyType`. | No public code requires private detail. | No raw backend decision exposed through `to_public_dict()`. | More coarse categories may be needed later. |
| `_DECISION_FINAL_STAGE_COMPATIBILITY` | Covers every decision; reserves `invariant_precheck_failed`, `validation_cancelled`, and `validation_superseded`. | Terminal decisions have terminal/final stages; ready has intermediate stages. | `MappingProxyType`. | Reserved stages cannot appear without mapping. | Does not promote runtime/canon authority. | Ready stage/flag contradictions need hardening before executable integration. |

No accidental donor assumptions, runtime execution authority, or canon authority were found in the constants. Private maps need not become public merely for testing.

## 7. FAILURE-ROUTE REVIEW

`ValidationFailureRoute` validates `route_id`, `route_type`, `decision`, `subject_ref_id`, Boolean fields, exact `blocking=True`, exact `trace_required=True`, quarantine flags, escalation flags, route/decision compatibility, public reason-code compatibility, player-visible hidden-info safety, and player-visible public reason-code presence. Metadata remains backend-only in public serialization. `to_public_dict()` excludes route ID, route type, raw decision, subject reference, trace flag, and metadata.

Manual invalid objects are rejected by `validate_validation_failure_route` when route type, decision, Boolean fields, quarantine/escalation flags, public reason code, player-visible safety, or metadata shape is invalid.

Residual subject-linkage review: PR-4C does not require a route `subject_ref_id` to equal a result `subject_ref_id`. A result may contain individually valid routes for different subjects. Mixed-subject routes could misdirect downstream blocking or auditing because a command result could carry a route for an unrelated state record. This is blocking before PR-5 planning because resource/consequence planning would otherwise depend on ambiguous failure artifacts.

## 8. REQUEST-STAGE REVIEW

`ValidationIntegrationRequest` accepts only `_REQUESTABLE_VALIDATION_STAGES`; terminal and completed outcome stages are rejected. Manually constructed invalid requests are rejected by `validate_validation_integration_request`. Transaction subjects still require `transaction_ref_id`; event-commitment subjects still require `event_commitment_ref_id`. Generated-content provenance invariant declarations still require generated-content references. No request can claim an already-completed validation outcome.

Request `trace_id` is optional. Classification: request traceability is **required before PR-5 implementation**, not before PR-5 planning by itself, but this review selects PR-4E for other planning blockers. PR-4E should decide whether every request needs `trace_id` before executable integration.

## 9. RESULT SUBJECT-IDENTITY REVIEW

PR-4C adds `subject_type` and `subject_ref_id` to results and validates their basic shape. It does not dereference objects or perform repository lookups, which is correct for this skeleton.

Reference-shape sufficiency findings:
- A command validation result can carry a route for an unrelated state record because route/result subject equality is not enforced.
- A generated-content result can carry unrelated-looking provenance references because provenance references are non-empty strings without typed identity or linkage to the result subject.
- A source-local result is not granted canon authority because no canon-promotion method or flag exists and authority flags stay false.
- A validation result can be detached from its request subject because only `validation_request_id`, `subject_type`, and `subject_ref_id` are shape-checked; no request-subject binding reference exists.

These are object-shape defects, not execution-stage dereferencing gaps. Route/result subject equality and result/request subject linkage require PR-4E before PR-5 planning.

## 10. RESULT TRACE AND REFERENCE REVIEW

Every result requires non-empty `trace_id`. Every terminal result requires `validation_result_ref_id`. `validation_ready` may omit `validation_result_ref_id`. Empty references are rejected. Manually constructed objects cannot bypass these rules when passed to the validator. Trace-required routes are attached only to traced results because every result is traced. No runtime trace is created or executed, and no validation result is dereferenced or executed.

All `validation_ready` states do not need a `validation_result_ref_id` before PR-5 planning if they are clearly non-terminal. However, trace IDs should eventually require a dedicated dependency reference, and validation-result IDs should eventually be linked to a result identity owner. Current shape-only trace references are partially acceptable, but combined with subject-linkage gaps they support PR-4E before PR-5 planning.

## 11. DECISION / FINAL-STAGE REVIEW

| decision | permitted final stage or stages | passed | blocking | quarantined | escalated | failure-route requirement | validation-result reference requirement | trace requirement | provenance requirement | current enforcement | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| validation_ready | request/intermediate stages only | false | true | false | false | optional downstream route only | optional | required | refs require checked flag | enforced | partially closed |
| validation_passed | validation_passed | true | false | false | false | forbidden | required | required | generated-content requires checked refs | enforced | closed |
| validation_failed | validation_failed | false | true | false | false | at least one matching route | required | required | none | enforced | closed |
| rejected_by_missing_command_ref | validation_failed | false | true | false | false | matching route | required | required | none | enforced | closed |
| rejected_by_missing_state_ref | validation_failed | false | true | false | false | matching route | required | required | none | enforced | closed |
| rejected_by_missing_transaction_ref | validation_failed | false | true | false | false | matching route | required | required | none | enforced | closed |
| rejected_by_missing_event_commitment_ref | validation_failed | false | true | false | false | matching route | required | required | none | enforced | closed |
| rejected_by_missing_invariant_set | validation_failed | false | true | false | false | matching route | required | required | none | enforced | closed |
| rejected_by_hidden_information_risk | validation_failed | false | true | false | false | matching route | required | required | none | enforced | closed |
| rejected_by_provenance_gap | validation_failed | false | true | false | false | matching route | required | required | none | enforced | closed |
| rejected_by_schema_mismatch | validation_failed | false | true | false | false | matching route | required | required | none | enforced | closed |
| rejected_by_authority_mismatch | validation_failed | false | true | false | false | matching route | required | required | none | enforced | closed |
| rejected_by_phase_boundary | validation_failed | false | true | false | false | matching route | required | required | none | enforced | closed |
| quarantined_for_review | validation_quarantined | false | true | true | false | quarantine routes only | required | required | none | enforced | closed |
| escalated_to_doctrine | validation_escalated | false | true | false | true | doctrine escalation route only | required | required | none | enforced | closed |
| unsupported_validation_scope | domain_validation_required | false | true | false | false | downstream validation route only | required | required | none | enforced | closed |

Reserved stages `invariant_precheck_failed`, `validation_cancelled`, and `validation_superseded` cannot currently appear as valid result final stages without a lawful decision mapping.

## 12. INTERMEDIATE-STAGE FLAG CONSISTENCY

Conceptual review and non-committed Python probes found:

| case | probe outcome | classification | PR-4E requirement |
|---|---|---|---|
| `final_stage="provenance_checked"` with `provenance_checked=False` | accepted for `validation_ready` | ambiguous but non-blocking alone | false |
| `final_stage="hidden_info_safety_checked"` with `hidden_info_safe=False` | accepted for `validation_ready` | ambiguous but non-blocking alone | false |
| `final_stage="invariant_precheck_passed"` without `invariant_precheck_ref_id` | rejected | already rejected | false |
| `validation_ready` with `hidden_info_safe=False` | accepted | ambiguous; could mask hidden-information failure if consumed as passed | true as part of PR-4E readiness tightening |
| `validation_ready` at `domain_validation_required` without downstream route | accepted | lawful as an intermediate coordination state | false |
| `validation_ready` with provenance references but `provenance_checked=False` | rejected if refs present | already rejected | false |

The stage/flag contradictions are not execution by themselves, but `validation_ready` hidden-info posture should be narrowed before PR-5 relies on validation artifacts.

## 13. SUCCESS-RESULT REVIEW

Successful results require `decision=validation_passed`, `final_stage=validation_passed`, `passed=True`, `blocking=False`, `quarantined=False`, `escalated=False`, `hidden_info_safe=True`, `validation_result_ref_id`, `trace_id`, no failure routes, and all authority flags false.

For generated-content success, PR-4C additionally requires `provenance_checked=True` and non-empty `provenance_ref_ids`. Generated-content provenance references need typed identity or dependency declarations before executable validation integration; for PR-5 planning, the absence is a residual concern but the blocking issue is that unrelated-looking references can be represented as if meaningful.

Success for `source_local_content`, `conversion_artifact`, and `canon_reference` does not grant canon authority. The result only states a backend validation decision about the runtime reference and does not promote canon.

## 14. FAILURE, REJECTION, QUARANTINE, ESCALATION, AND UNSUPPORTED-SCOPE REVIEW

Validation failure uses `validation_failed`, blocking posture, matching routes, result reference, and trace. Rejected decisions use `validation_failed`, exact matching route decisions, blocking posture, and no quarantine/escalation flags. Quarantine uses `validation_quarantined`, `quarantined=True`, quarantine route types only, and matching route decisions. Escalation uses `validation_escalated`, `escalated=True`, doctrine-escalation routes only, and matching route decisions. Unsupported scope uses `domain_validation_required`, downstream-validation route, blocking posture, trace, and result references.

A route combination can pass individual route validation but produce an incoherent aggregate when route subjects differ from the result subject. This is the key failure-route residual requiring PR-4E.

## 15. PUBLIC HIDDEN-INFORMATION SAFETY REVIEW

The public reason-code vocabulary is sanitized. Player-visible routes require `hidden_info_safe=True` and a public reason code. Public serialization excludes metadata, IDs, raw route type, raw decision, subject reference, backend trace fields, and backend references. The exposed public fields are `reason_code`, `blocking`, `quarantines`, and `escalates`.

The four public flags are sufficiently non-sensitive for current skeleton review because they disclose only coarse process posture, not hidden facts. Public serialization should be reviewed again before model-facing summaries. Omitting escalation/quarantine flags may be desirable in a future UI adapter, but it is deferred rather than blocking for this skeleton. No prose generation or model-facing summarization is implemented.

## 16. PROVENANCE, SOURCE-LOCAL, CONVERSION, AND CANON REVIEW

PR-4C lawfully separates generated content, generated-content provenance, source-local converted content, conversion artifacts, canon references, runtime validation, doctrine escalation, and canon promotion. Generated-content success requires result-side provenance linkage. Provenance references do not automatically become durable state. Source-local validation does not promote canon. Conversion artifacts do not become Astra law. Donor assumptions do not become runtime truth. Doctrine escalation is not validation success. No canon-promotion behavior exists.

Residual: provenance references are untyped strings and can be unrelated-looking. This is a provenance-authority posture concern for PR-4E but does not mean PR-4C executes or promotes content.

## 17. FACTORY / VALIDATOR PARITY REVIEW

`create_validation_failure_route` and `validate_validation_failure_route` share `_validate_failure_route_fields`. `create_validation_integration_request` and `validate_validation_integration_request` both enforce requestable stages, subject shape, dependency/invariant tuple shape, transaction/event subject requirements, generated-content invariant reference requirements, optional trace shape, and metadata mapping. `create_validation_integration_result` and `validate_validation_integration_result` share `_validate_result_semantics`.

Manual frozen-object cases reviewed:

| case | factory behavior | validator behavior | parity |
|---|---|---|---|
| missing trace | rejected | rejected | yes |
| missing terminal result reference | rejected | rejected | yes |
| invalid subject type | rejected | rejected | yes |
| empty subject reference | rejected | rejected | yes |
| invalid provenance tuple | rejected | rejected | yes |
| provenance refs without checked flag | rejected | rejected | yes |
| generated-content success without provenance | rejected | rejected | yes |
| invalid decision/stage pair | rejected | rejected | yes |
| route/decision mismatch | rejected | rejected | yes |
| route/result mismatch by subject | accepted | accepted | parity exists but invariant missing |
| player-visible route without public reason | rejected | rejected | yes |
| request using a terminal stage | rejected | rejected | yes |
| invalid quarantine flag | rejected | rejected | yes |
| invalid escalation flag | rejected | rejected | yes |
| passed-but-blocking result | rejected | rejected | yes |

No factory-only or validator-only PR-4C behavior was observed. Parity is acceptable, but parity includes the residual missing aggregate invariant.

## 18. IMMUTABILITY AND SERIALIZATION REVIEW

Dataclasses are frozen. Factory metadata uses `MappingProxyType` over a deep copy. Sequence fields are normalized to tuples. `to_dict()` returns copied/listified structures. `to_public_dict()` sanitizes public route output. Manually constructed objects can still carry mutable nested metadata because frozen dataclasses do not recursively freeze arbitrary mappings. Validators require mapping shape but do not deep-freeze manual objects. This is a known skeleton limitation and not an immediate authority risk because metadata remains backend-only and no execution consumes it, but PR-4E or executable integration should add manual-object metadata immutability tests if metadata becomes security-relevant.

## 19. NON-EXECUTION AND IMPORT REVIEW

Direct review found no `run_validation_checks` import or call and no `run_invariant_prechecks` import or call. PR-4C does not mutate state, apply state deltas, append events, commit events, persist, replay, execute commands, execute RNG, execute table/oracle logic, calculate resources, call models, implement prompt behavior, narrate outcomes, or add live-play/UI behavior.

`ValidationIntegrationService` remains stateless and contains only factory/validator forwarding methods. It has no forbidden execution-style methods.

## 20. DOMAIN AND KERNEL HANDOFF REVIEW

| surface | represented by reference | operationally invoked | allowed at current stage | future integration owner | residual risk | readiness for PR-5 planning |
|---|---|---|---|---|---|---|
| command lifecycle | yes | no | reference-only | RT001 | route subject mismatch | not ready |
| action legality | yes | no | reference-only | RT001 | result/request linkage | not ready |
| state store | yes | no | reference-only | state store/domain owners | unrelated state refs can be named | not ready |
| state projection | yes | no | reference-only | RT005 | hidden-info-ready ambiguity | not ready |
| transaction lifecycle | yes | no | reference-only | transaction lifecycle owner | subject route mismatch | not ready |
| event commitment | yes | no | reference-only | event commitment owner | aggregate route mismatch | not ready |
| future resource/consequence math | no implementation | no | planning only later | RT002 | must depend only on passed terminal results | blocked |
| schema registry | yes | no | reference-only | kernel schema registry | shape-only dependency | blocked |
| record identity | yes | no | reference-only | kernel record identity | no identity binding | blocked |
| command envelope | yes | no | reference-only | kernel command envelope | no dereference | blocked |
| transaction preview | yes | no | reference-only | kernel transaction preview | no dereference | blocked |
| state delta | yes | no | reference-only | kernel state delta | no delta application | acceptable |
| event ledger | yes | no | reference-only | kernel event ledger | no append | acceptable |
| validation pipeline | yes | no | reference-only | RT011/kernel validation | no execution | acceptable |
| hidden information | yes | no | reference-only | RT005 | ready hidden-info ambiguity | blocked |
| context projection | yes | no | reference-only | RT005 | no compiler | acceptable |
| persistence boundary | yes | no | reference-only | kernel persistence | no persistence | acceptable |
| replay audit | yes | no | reference-only | kernel replay | no replay | acceptable |
| runtime trace | yes | no | reference-only | kernel runtime trace | trace identity not linked | blocked |
| RNG interface | no dependency type beyond no execution | no | no invocation | RT009 | none | acceptable |
| table/oracle | no dependency type beyond no execution | no | no invocation | RT009 | none | acceptable |

Expected posture is preserved: reference-only, no operational invocation, no state/event/persistence effects.

## 21. RESOURCE / CONSEQUENCE MATH READINESS REVIEW

| future validation area | validation result references PR-5 may depend on | PR-4C semantics unambiguous enough | PR-5 must own | validation integration must not calculate | remaining blocker |
|---|---|---|---|---|---|
| resource affordability | passed terminal result, trace, subject | no | affordability model | costs or pools | subject/linkage ambiguity |
| resource commitment | passed terminal result and transaction refs | no | commitment plan | state deltas | subject/linkage ambiguity |
| resource expenditure | passed terminal result and event refs | no | spend rules | expenditure math | subject/linkage ambiguity |
| partial costs | failed/rejected routes and trace | no | partial-cost semantics | partial cost math | route subject mismatch |
| backlash | failure/quarantine/escalation route refs | no | consequence model | backlash effects | route subject mismatch |
| over-investment | validation_failed/rejected evidence | no | over-investment rules | resource calculation | subject/linkage ambiguity |
| consequence selection | passed/failure terminal result only | no | consequence chooser | outcome narration | validation_ready ambiguity |
| consequence severity | terminal decision plus trace | no | severity model | severity math | trace linkage gap |
| injury/resource/world deltas | validation result refs only | no | delta owner | apply deltas | result identity gap |
| cost payment regardless of outcome | terminal result plus transaction refs | no | payment semantics | payment execution | subject/request linkage gap |
| invalid negative or duplicated costs | rejected route refs | no | RT002 invariant family | cost validation execution | route subject mismatch |
| cross-resource conversion | passed result only | no | conversion math within RT002 | conversion execution | provenance/subject ambiguity |
| temporary vs persistent consequences | terminal refs and persistence refs | no | consequence owner | persistence | result identity gap |
| source-local resource systems | authority rejection/success refs | no | source-local policy | canon promotion | source-local/canon confusion risk |
| vehicle/platform resource pools | subject refs and routes | no | vehicle/resource owner | pool math | subject typing too coarse |
| companion/summon costs | subject refs and routes | no | RT002/RT007 | summon cost math | subject typing too coarse |
| crafting/salvage costs | result refs and provenance refs | no | RT002/RT010 | crafting math | provenance untyped |
| cultivation breakthroughs | result refs and escalation routes | no | RT002/RT004 | breakthrough mechanics | doctrine escalation linkage |
| horror/sanity/stress pressures | hidden-info-safe terminal refs | no | RT002/RT005 | stress math | hidden-info-ready ambiguity |

PR-5 must own resource/consequence math and must not rely on `validation_ready` as success. Because PR-4C still permits ambiguous subject, route, trace, and provenance linkages, resource/consequence math service planning is not dependency-ready.

## 22. CORPUS-SCALE PRESSURE REVIEW

| pressure | validation subject type | invariant family | likely failure route | downstream owner | PR-4C can represent safely | lawful escalation point |
|---|---|---|---|---|---|---|
| class/archetype systems | source_local_content/conversion_artifact | source_local_authority | reject_source_local_authority | RT012/RT002 | partially | doctrine gap |
| point-buy systems | transaction/state_delta | state_delta_shape | block_transaction_before_commitment | RT002 | partially | doctrine gap |
| profession/occupation systems | source_local_content | conversion_boundary | reject_phase_boundary_violation | RT012 | partially | doctrine gap |
| narrative tags/aspects | state_record/context_projection | context_projection_visibility | reject_hidden_info_leak | RT005 | partially | doctrine gap |
| cultivation systems | generated_content/source_local_content | generated_content_provenance | quarantine_generated_content | RT004/RT008 | partially | doctrine gap |
| cyberware/biotech | state_delta/transaction | state_reference | block_transaction_before_commitment | RT002/RT010 | partially | doctrine gap |
| psionics | action_legality/transaction | action_legality | block_command_before_transaction | RT001/RT004 | partially | doctrine gap |
| horror/investigation | hidden_information/context_projection | hidden_information_partition | reject_hidden_info_leak | RT005 | partially | doctrine gap |
| vehicles/mechs/ships | state_record/transaction | state_reference | block_transaction_before_commitment | RT010/RT002 | partially | doctrine gap |
| companions/summons | state_record/action_legality | action_legality | block_command_before_transaction | RT007/RT002 | partially | doctrine gap |
| crafting/salvage/requisition | transaction/generated_content | generated_content_provenance | quarantine_generated_content | RT010/RT008 | partially | doctrine gap |
| random tables/oracles | generated_content | generated_content_provenance | quarantine_generated_content | RT009/RT008 | partially | doctrine gap |
| source-local cosmologies | source_local_content | canon_boundary | reject_source_local_authority | RT012 | partially | doctrine gap |
| adventure paths | conversion_artifact/source_local_content | conversion_boundary | reject_phase_boundary_violation | RT012 | partially | doctrine gap |
| cross-book mixed-genre interactions | transaction/state_delta | schema_record_shape | reject_schema_mismatch | RT002/RT011 | partially | doctrine gap |
| generated content | generated_content | generated_content_provenance | quarantine_generated_content | RT008 | partially | doctrine gap |
| hidden actor knowledge | hidden_information/context_projection | hidden_information_partition | reject_hidden_info_leak | RT005/RT007 | partially | doctrine gap |
| persistent world changes | state_delta/event_ledger | event_ledger_shape | block_event_commitment | event commitment/persistence | partially | doctrine gap |

PR-4C can name these pressures, but safe corpus-scale planning requires PR-4E object-shape tightening.

## 23. RISK REVIEW

| risk | severity | affected RT owner or family | current mitigation | required future test | PR-4E required |
|---|---|---|---|---|---|
| failure-route subject does not match result subject | high | RT001/RT002/RT011 | route subject is non-empty | aggregate rejection test | true |
| validation-ready result masks hidden-information failure | medium | RT005 | ready is blocking | ready hidden-info policy test | true |
| provenance_checked stage contradicts Boolean flag | medium | RT008 | provenance refs require checked flag | stage/flag consistency test | false |
| hidden-info-checked stage contradicts Boolean flag | medium | RT005 | success requires hidden-info safe | stage/flag consistency test | false |
| trace reference exists but is semantically unrelated | high | RT011/kernel trace | non-empty trace required | trace dependency linkage test | true |
| validation-result reference exists but is unrelated | high | RT011/kernel identity | non-empty terminal ref required | result identity dependency test | true |
| public reason codes indirectly disclose backend state | low | RT005 | sanitized vocabulary | public serialization regression | false |
| nested metadata remains mutable through manual construction | medium | all backend metadata owners | factory deep-copy proxy | manual metadata immutability test | false |
| source-local success is mistaken for canon | high | RT012 | no canon promotion behavior | source-local success non-authority test | false |
| generated-content provenance references are untyped | medium | RT008 | non-empty refs and checked flag | typed provenance test | true |
| resource math begins relying on validation_ready rather than validation_passed | high | RT002 | ready is blocking | PR-5 plan guardrail test | true |
| unsupported scope is treated as validation failure rather than downstream-routing need | medium | RT011/RT002 | dedicated decision and route | unsupported scope consumer test | false |
| factory/validator parity regresses | high | RT011 | shared helpers | parity regression tests | false |
| validation integration starts calculating resource outcomes | critical | RT002 | no resource code/imports | non-execution import scan | false |
| historical tests were weakened to accept invalid objects | high | RT011 | existing PR-4B/4C tests | historical guardrail tests | false |

## 24. HARDENING LEDGER

| hardening ID | issue | current PR-4C behavior | desired invariant | severity | required before PR-5 planning | required before PR-5 implementation | required before executable validation integration | future owner | recommended PR |
|---|---|---|---|---|---|---|---|---|---|
| PR4D-H01 | route subject/result subject equality | mismatch accepted | every route subject matches result subject unless an explicit typed cross-subject relation is declared | high | yes | yes | yes | RT011 | PR-4E |
| PR4D-H02 | result subject/request subject linkage | shape-only IDs | result subject must be linked to request subject identity | high | yes | yes | yes | RT011 | PR-4E |
| PR4D-H03 | provenance_checked stage/flag consistency | ready stage may contradict flag | checked stage implies checked flag or stage renamed | medium | no | yes | yes | RT008 | PR-4E or later |
| PR4D-H04 | hidden_info_safety_checked stage/flag consistency | ready stage may contradict flag | checked stage implies safe flag or explicit failed state | medium | no | yes | yes | RT005 | PR-4E or later |
| PR4D-H05 | validation_ready hidden-info posture | hidden unsafe ready accepted | ready must not mask hidden-info failure | medium | yes | yes | yes | RT005 | PR-4E |
| PR4D-H06 | request trace requirement | optional | decide mandatory trace for requests | medium | no | yes | yes | RT011 | PR-4E or PR-5 pre-impl |
| PR4D-H07 | typed provenance references | strings only | provenance refs declare type/owner relation | medium | yes | yes | yes | RT008 | PR-4E |
| PR4D-H08 | trace identity linkage | non-empty string only | trace ID tied to runtime_trace dependency or trace owner | high | yes | yes | yes | RT011/kernel trace | PR-4E |
| PR4D-H09 | validation-result identity linkage | non-empty string only | result ref tied to validation result dependency/identity owner | high | yes | yes | yes | RT011 | PR-4E |
| PR4D-H10 | public escalation/quarantine disclosure | public booleans exposed | final UI-facing disclosure policy documented | low | no | no | yes | RT005/UI future | future UI/privacy PR |
| PR4D-H11 | nested metadata immutability | factory-safe; manual nested mutable accepted | manual objects cannot retain mutable nested metadata if accepted | medium | no | no | yes | RT011 | executable integration hardening |
| PR4D-H12 | reserved stage mappings | reserved stages unmapped | add lawful decisions before use | low | no | no | yes | RT011 | future reserved-stage PR |

## 25. GATE DECISION

```yaml
gate_finding:
  validation_integration_hardening_review_complete: true
  pr_4c_scope_confirmed: true
  pr_4b_blockers_closed: partially
  public_reason_safety_acceptable: partially
  request_stage_restrictions_acceptable: true
  subject_identity_posture_acceptable_for_planning: false
  trace_and_result_reference_posture_acceptable: partially
  decision_stage_compatibility_acceptable: true
  success_result_semantics_acceptable: true
  failure_route_semantics_acceptable: partially
  quarantine_escalation_semantics_acceptable: true
  provenance_authority_posture_acceptable: partially
  factory_validator_parity_acceptable: true
  anti_authority_guardrails_acceptable: true
  resource_consequence_math_dependency_ready: false
  requires_pr_4e_hardening_before_pr_5: true
  ready_for_runtime_domain_pr_5_planning: false
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-4E validation integration residual skeleton hardening
  next_step_status: narrow_skeleton_hardening_pending_review
```

## 26. RECOMMENDED NEXT PR

Recommend: **RUNTIME-DOMAIN-PR-4E: Validation Integration Residual Skeleton Hardening**.

Required PR-4E code and test changes:
- Enforce route `subject_ref_id` equality with result `subject_ref_id`, or add explicit typed cross-subject routing declarations.
- Add result/request subject linkage, either by requiring request subject identity fields on results or a typed request identity dependency.
- Add trace identity linkage through a runtime-trace dependency/reference invariant.
- Add validation-result identity linkage through a validation-result dependency/reference invariant.
- Harden generated-content provenance references with typed provenance/dependency declarations.
- Decide and test `validation_ready` hidden-information posture.
- Add focused tests for aggregate route/result mismatch, detached result/request subject, unrelated trace/result/provenance references, and `validation_ready` hidden-info ambiguity.

Do not implement these changes in PR-4D. PR-5 remains blocked until PR-4E is accepted.

## 27. NON-IMPLEMENTATION REAFFIRMATION

PR-4D adds no runtime code, domain-service code, validation implementation changes, validation execution, invariant evaluation, state mutation, state-delta application, event append, transaction execution, actual event commitment, persistence, replay, command execution, resource math, combat, abilities, inventory, mission/social behavior, generated-content persistence, context-packet compiler, model integration, live-play adapter, UI, conversion, sourcebook inclusion, or canon promotion.

## 28. CLASSIFICATION BLOCK

```yaml
runtime_domain_pr_4d:
  review_id: RUNTIME-DOMAIN-PR-4D-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-REVIEW-001
  artifact_type: validation_integration_invariant_enforcement_skeleton_hardening_review_gate
  implementation_status: non_executable_review_gate
  derives_from:
    - RUNTIME-DOMAIN-PR-4C-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-001
    - RUNTIME-DOMAIN-PR-4B-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-REVIEW-001
    - RUNTIME-DOMAIN-PR-4A-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-IMPLEMENTATION-001
    - RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001
    - RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
    - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
    - RT-001
    - RT-002
    - RT-005
    - RT-008
    - RT-011
  reviews_pr_4b_blocker_closure: true
  reviews_public_reason_safety: true
  reviews_failure_route_semantics: true
  reviews_request_stage_restrictions: true
  reviews_result_subject_identity: true
  reviews_trace_and_result_references: true
  reviews_decision_stage_compatibility: true
  reviews_success_result_semantics: true
  reviews_failure_rejection_quarantine_escalation_semantics: true
  reviews_hidden_information_posture: true
  reviews_provenance_authority_posture: true
  reviews_factory_validator_parity: true
  reviews_immutability_and_serialization: true
  reviews_non_execution_posture: true
  reviews_domain_and_kernel_handoffs: true
  reviews_resource_consequence_math_readiness: true
  reviews_corpus_scale_pressure: true
  defines_hardening_ledger: true
  authorizes_runtime_code_by_this_pr: false
  authorizes_domain_code_by_this_pr: false
  authorizes_validation_execution_by_this_pr: false
  authorizes_invariant_evaluation_by_this_pr: false
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
  next_allowed_step: RUNTIME-DOMAIN-PR-4E validation integration residual skeleton hardening, pending review
```

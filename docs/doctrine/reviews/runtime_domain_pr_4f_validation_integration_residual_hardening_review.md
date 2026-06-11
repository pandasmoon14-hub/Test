# RUNTIME-DOMAIN-PR-4F: Validation Integration Residual Hardening Review Gate

## 1. PURPOSE AND STATUS

This is **RUNTIME-DOMAIN-PR-4F** and its review identifier is **RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001**.
It is a non-executable review/gate artifact. It reviews **RUNTIME-DOMAIN-PR-4E-VALIDATION-INTEGRATION-RESIDUAL-SKELETON-HARDENING-001** against **RUNTIME-DOMAIN-PR-4D-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-REVIEW-001**, **RUNTIME-DOMAIN-PR-4B-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-REVIEW-001**, and **RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001**.

PR-4F implements no code. It authorizes only one of two outcomes: PR-5 planning or PR-4G hardening. PR-5 remains blocked until this review is accepted.

## 2. SOURCE LEDGER

### PR-4E implementation
- `src/astra_runtime/domain/validation_integration.py`
- `src/astra_runtime/domain/__init__.py`

### PR-4E tests
- `tests/runtime/test_domain_validation_integration_residual_hardening.py`
- `tests/runtime/test_domain_validation_integration_hardening.py`
- `tests/runtime/test_domain_validation_integration_skeleton.py`

### PR-4D findings
- `docs/doctrine/reviews/runtime_domain_pr_4d_validation_integration_invariant_enforcement_skeleton_hardening_review.md`

### PR-4B findings
- `docs/doctrine/reviews/runtime_domain_pr_4b_validation_integration_invariant_enforcement_skeleton_review.md`

### PR-4 plan
- `docs/doctrine/reviews/runtime_domain_pr_4_validation_integration_invariant_enforcement_service_plan.md`

### prior domain foundations and sequencing plan
- `docs/doctrine/reviews/runtime_domain_pr_0_domain_service_implementation_sequencing_plan.md`
- `src/astra_runtime/domain/command_lifecycle.py`
- `src/astra_runtime/domain/action_legality.py`
- `src/astra_runtime/domain/state_store.py`
- `src/astra_runtime/domain/state_projection.py`
- `src/astra_runtime/domain/transaction_lifecycle.py`
- `src/astra_runtime/domain/event_commitment.py`

### kernel references
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

### owner specifications
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

### registry and decision log
- `docs/doctrine/astra_doctrine_registry_v0_1.yaml`
- `docs/decisions/current_decisions_log.md`

No required source was absent or renamed during this review.

## 3. BACKEND-FIRST VALIDATION INVARIANT

Astra Ascension is a backend-owned runtime. The **LLM is not the game engine**. Validation is backend authority. Typed references are not execution, and typed references do not prove object existence. Validation artifacts cannot mutate state, cannot append events, cannot persist or replay, cannot evaluate domain invariants, cannot execute commands, cannot invoke models, and cannot calculate resources or consequences. Generated content cannot validate itself. Source-local content cannot become canon through runtime validation. Runtime validation cannot promote canon. Validation remains separate from resource/consequence calculation.

## 4. PR-4E IMPLEMENTATION REVIEW

|artifact|required PR-4E scope|observed implementation|scope status|residual risk|required follow-up|readiness for PR-5 planning|
|---|---|---|---|---|---|---|
|validation_integration.py|PR-4E residual shape hardening only|VALIDATION_SUBJECT_RELATIONS, typed route subjects, exact bound dependencies, provenance set equality, validation_ready safety, intermediate-stage checks|within PR-4E authorized scope|object dereference and route priority deferred|None before PR-5 planning|ready|
|domain/__init__.py exports|export new constants/types without behavior|exports validation integration surfaces and constants|within PR-4E authorized scope|export drift if future rules regress|Keep tests around exports|ready|
|residual-hardening tests|focused PR-4E blocker tests|manual invalid objects, dependency uniqueness, provenance, subject binding, validation_ready covered|within PR-4E authorized scope|not exhaustive execution probes|Carry into future suites|ready|
|updated PR-4C hardening tests|adapt older tests to hardened semantics|historic hardening tests retained with new required dependencies|within PR-4E authorized scope|weakening risk monitored|Keep PR-4C tests in run list|ready|
|updated skeleton tests|preserve skeleton guarantees with new refs|skeleton tests cover non-execution and API surfaces|within PR-4E authorized scope|brittleness if API evolves|Keep PR-4A/4B/4D tests|ready|
|registry record|track PR-4E and block PR-5 pending PR-4F|registry contains PR-4E record and next step PR-4F|within tracking scope|none material|Add PR-4F record|ready|
|decision-log record|record PR-4E implication|decision log states PR-5 blocked pending PR-4F|within tracking scope|none material|Add PR-4F record|ready|

The observed PR-4E footprint remained within its authorized seven-file scope: validation implementation, domain exports, three validation-integration test files, registry, and decision log. PR-4F itself modifies only the review artifact, its review tests, the registry, and the decision log.

## 5. PR-4D BLOCKER-CLOSURE MATRIX

|PR-4D finding|PR-4E mechanism|factory enforcement|validator enforcement|focused test coverage|closure status|residual concern|
|---|---|---|---|---|---|---|
|explicit subject relationship vocabulary|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|same-subject equality|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|lawful cross-subject relationships|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|ambiguous unrelated subjects rejected|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|result subject bound to request subject declaration|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|typed validation-request reference dependency|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|typed runtime-trace dependency|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|typed validation-result dependency|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|typed generated-content provenance dependency|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|dependency-ID uniqueness|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|dependency-binding uniqueness|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|validation_ready hidden-information safety|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|provenance_checked stage consistency|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|hidden_info_safety_checked stage consistency|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|invariant_precheck_passed reference consistency|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|
|factory/validator parity|PR-4E mechanism observed|factory enforcement present|validator enforcement present|focused residual-hardening tests present|closed|Execution dereference deferred, not a planning blocker|

## 6. SUBJECT-RELATION VOCABULARY REVIEW

Reviewed relations: `same_subject`, `blocking_dependency`, `affected_subject`, `source_subject`, `target_subject`, `authority_source`, and `provenance_source`.

The vocabulary is genre-neutral and sufficient for PR-5 planning across fantasy, sci-fi, cultivation, horror, narrative, point-buy, vehicles, companions, crafting, and source-local constructs. It avoids donor-specific assumptions because it describes structural relationship roles, not named game systems. `authority_source` and `provenance_source` are distinct enough to avoid accidental canon authority: authority asks whether a source may govern a runtime reference, while provenance asks what generated or converted content derives from. `source_subject` and `target_subject` can overlap in broad language, but typed subject pairs make the object-shape explicit. Future extension has a lawful escalation path through RT011 and doctrine review. PR-4F adds no new relations.

## 7. FAILURE-ROUTE SUBJECT REVIEW

Reviewed `subject_type`, `subject_ref_id`, `subject_relation`, route/result aggregate checks, standalone route validation, and public serialization. Same-subject routes must match the result pair. Cross-subject routes must use a different pair and declare a valid relationship. Public serialization excludes subject identity and relationship. Manually constructed invalid routes/results are rejected by validators.

|example pairing|classification|review finding|
|---|---|---|
|block_transaction_before_commitment + blocking_dependency|lawful but uncommon|Can represent transaction blocked by a related dependency; owner policy may refine.|
|reject_source_local_authority + authority_source|lawful and expected|Authority source relation fits source-local/canon boundary review.|
|reject_hidden_info_leak + source_subject|lawful and expected|Leak can be sourced from a hidden-information subject.|
|quarantine_generated_content + provenance_source|lawful and expected|Generated content may be quarantined because provenance source is unresolved.|
|request_downstream_domain_validation + blocking_dependency|lawful and common|Ready coordination route can name the downstream blocker.|
|block_event_commitment + target_subject|lawful but execution-stage policy|A target subject may be the event commitment or affected target; executable owner can constrain.|

Route-type/subject-relation compatibility can need additional constraints before PR-5 implementation or executable validation, but it is not a PR-4G blocker because overconstraining now would harm corpus-scale cross-subject cases without evidence.

## 8. ROUTE-SUBJECT DEPENDENCY LINKAGE REVIEW

PR-4E types route subjects but does not require every route subject to have a matching `ValidationIntegrationDependency`. This was probed with a cross-subject state-record route without a matching dependency, and it was accepted.

Explicit answer: subject type/ref plus explicit relation is sufficient for PR-5 planning. A matching dependency is likely required before PR-5 implementation when PR-5 depends on route subjects as dereferenceable planning inputs. It is certainly required before executable validation integration if the route subject is dereferenced, audited, replayed, or used as authority. Existing dependency types can express many route subjects, including command, action, state, transaction, event, hidden information, provenance, source-local, and canon-boundary references, but not every future corpus-specific outlier without overloading. Forcing linkage now would overconstrain lawful outliers and is not required in PR-4F.

## 9. RESULT / REQUEST SUBJECT-BINDING REVIEW

Reviewed `validation_request_id`, `request_subject_type`, `request_subject_ref_id`, result `subject_type`, result `subject_ref_id`, and `validation_request_ref` dependency. Result and request subject declarations must match. The `validation_request_ref` dependency must match `validation_request_id`. Factory defaults do not permit detached subjects because omitted request-subject fields default to the result subject. Validators reject manually detached subjects. This is shape-level binding and does not claim the referenced request was dereferenced.

Assessment: a typed dependency for the primary subject is not a PR-5 planning blocker but is a PR-5 implementation hardening item; a request-object hash is not a planning blocker and belongs before replay/hash authority; an immutable request snapshot reference is an implementation/execution concern; execution-stage lookup is required only before executable validation integration.

## 10. TYPED DEPENDENCY REVIEW

Reviewed typed binding requirements for `validation_request_ref`, `runtime_trace_ref`, `validation_result_ref`, and `generated_content_provenance_ref`. Exact binding is enforced with `required=True` and `satisfied=True`. Conflicting references of the relevant bound type are rejected by exact-one rules. Duplicate dependency IDs and duplicate type/reference pairs are rejected. `validation_ready` may omit `validation_result_ref`. A supplied `validation_result_ref` cannot exist without its field. Request trace linkage is enforced when `request.trace_id` is present. Manually constructed invalid objects are rejected by validators.

Binding dependencies do not currently require `hidden_info_safe=True`; this is a future hidden-information posture issue, not a planning blocker. Dependency metadata can contradict binding fields, but binding fields remain authoritative. Dependency IDs need a stronger format before implementation/replay authority, not before planning. Multiple dependencies of one type with different refs are lawful for unbound types, while bound singleton types reject conflicts. Generic dependency uniqueness is acceptable for planning.

## 11. PROVENANCE-LINKAGE REVIEW

Reviewed `provenance_checked`, `provenance_ref_ids`, `generated_content_provenance_ref` dependencies, exact set equality, uniqueness, required/satisfied binding posture, generated-content success, and generated-content `provenance_checked` intermediate stage.

Provenance IDs cannot appear without typed dependencies, and typed provenance dependencies cannot appear without IDs. Generated-content success requires provenance. Provenance linkage does not persist generated content and does not promote canon. Each provenance source may later need `subject_type`, `subject_relation=provenance_source`, a dedicated provenance record schema, and source-local/canon authority classification. These are not PR-5 planning blockers; the record schema and authority classification are PR-5 implementation or RT008/RT012 execution concerns.

## 12. DEPENDENCY-UNIQUENESS REVIEW

Duplicate dependency IDs are rejected. Duplicate type/reference pairs are rejected. Duplicate provenance references are rejected through exact set/uniqueness checks. Multiple different references of the same dependency type are lawful except for singleton bound types. Identical reference IDs under different dependency types are permitted, which avoids rejecting lawful multi-role references. Current uniqueness rules prevent ambiguity for PR-5 planning, do not accidentally reject most multi-role references, and remain deterministic for serialization and replay at the tuple-shape level. Stronger ordering, priority, or typed identity grammar is deferred until evidence requires it.

## 13. VALIDATION-READY REVIEW

`validation_ready` requires `passed=False`, `blocking=True`, `hidden_info_safe=True`, `quarantined=False`, `escalated=False`, a legal non-terminal final stage, request identity dependency, trace dependency, no validation-result reference unless the field exists, and either no routes or downstream-validation routes.

`validation_ready` at `domain_validation_required` without a route is lawful as a coordination marker. `validation_ready` at `provenance_checked`, `hidden_info_safety_checked`, and `invariant_precheck_passed` is lawful when the corresponding consistency requirements are met. PR-5 planning may refer to `validation_ready` for coordination design, but future executable resource commitment must never treat `validation_ready` as `validation_passed`. PR-5 must require `validation_passed` before any eventual resource mutation or event commitment.

## 14. INTERMEDIATE-STAGE CONSISTENCY REVIEW

Reviewed `provenance_checked`, `hidden_info_safety_checked`, and `invariant_precheck_passed`. PR-4E enforces stage/flag/reference consistency: generated-content provenance linkage at `provenance_checked`, hidden-info safety at `hidden_info_safety_checked`, and a precheck reference at `invariant_precheck_passed`.

One-way consistency is acceptable. `provenance_checked=True` at an earlier stage can be a lawful predeclared state if provenance references are linked. `hidden_info_safe=True` before the checked stage is a safe posture, not a contradiction. `invariant_precheck_ref_id` present before precheck completion can be a lawful reference declaration. Doctrine does not require exact bidirectional stage/flag equality in this skeleton.

## 15. FAILURE-ROUTE AGGREGATE REVIEW

Aggregate result behavior permits multiple same-subject routes, multiple cross-subject routes, mixed routes, repeated route IDs, duplicate semantic routes, multiple blocking dependencies, multiple authority sources, and multiple provenance sources when other invariants pass. Conflicting subject relations are constrained only by same-subject versus cross-subject pair rules.

Unique route IDs should be enforced before PR-5 implementation/audit reliance. Unique route tuples and deduplication are executable validation concerns. Deterministic route ordering is already tuple-preserved; route priority is not required for PR-5 planning. A lack of route priority does not make validation outcomes ambiguous at the object-shape level.

## 16. FACTORY / VALIDATOR PARITY REVIEW

Compared `create_validation_failure_route` / `validate_validation_failure_route`, `create_validation_integration_request` / `validate_validation_integration_request`, and `create_validation_integration_result` / `validate_validation_integration_result`. The PR-4E rules are represented on both factory and validator paths.

Manual frozen-object cases reviewed: invalid subject relation, mismatched same-subject route, same subject mislabeled as cross-subject, detached request/result subject, missing request dependency, missing trace dependency, missing terminal result dependency, duplicate dependency ID, duplicate dependency binding, mismatched provenance sets, unsafe `validation_ready`, contradictory intermediate flags, and invalid nested dependency type. No material factory-only or validator-only PR-4E blocker was found for PR-5 planning.

## 17. IMMUTABILITY AND SERIALIZATION REVIEW

Reviewed frozen dataclasses, tuple normalization, `MappingProxyType` metadata, factory deep copying, `to_dict` copies, `to_public_dict` sanitization, dependency serialization, route subject serialization, request-subject serialization, deterministic tuple order, and manually constructed nested mutable metadata.

Recursive metadata freezing remains non-blocking for PR-5 planning. It is required before executable validation integration if metadata can affect authority, and required before replay/hash authority. PR-4F does not convert this into a generic immutability redesign.

## 18. NON-EXECUTION REVIEW

Direct review found no `run_validation_checks` import or call, no `run_invariant_prechecks` import or call, no validation evaluation, no state mutation, no delta application, no event append, no event commitment, no persistence, no replay, no command execution, no RNG execution, no table/oracle execution, no resource calculation, no consequence calculation, no model call, no prompt behavior, no narration, and no live-play or UI behavior. `ValidationIntegrationService` remains stateless and exposes factory/validator wrappers only; it has no execution-style methods.

## 19. RESOURCE / CONSEQUENCE MATH READINESS

PR-5 planning can safely depend on the hardened validation surface because PR-4E supplies typed request/result/route/dependency/provenance shapes without calculating resources or consequences.

|case|likely validation subject|possible cross-subject route|relevant dependency type|required validation decision|what PR-5 owns|what validation integration must not calculate|PR-4E sufficient for planning|
|---|---|---|---|---|---|---|---|
|affordability validation|command|state_record pool|blocking_dependency|state_record_ref|backend decision that payment can be attempted|PR-5 declares affordability inputs and math boundaries|must not calculate affordability|yes|
|declared costs|transaction|command envelope|source_subject|command_envelope_ref|backend decision that declarations are present|PR-5 plans cost declaration schema|must not total costs|yes|
|committed costs|transaction|state_delta|target_subject|state_delta_ref|validation_passed before commitment|PR-5 plans commitment preconditions|must not apply deltas|yes|
|cost payment regardless of success|transaction|action legality result|blocking_dependency|action_legality_ref|decision about required validation stage|PR-5 identifies owner of sunk-cost policy|must not resolve success or payment|yes|
|optional over-investment|command|resource pool|affected_subject|state_record_ref|decision that validation is required|PR-5 models optional spend constraints|must not optimize investment|yes|
|partial payment|transaction|state snapshot|blocking_dependency|state_snapshot_ref|decision that partial payment is blocked or routed|PR-5 plans partial-payment posture|must not mutate balances|yes|
|multiple resource pools|transaction|pool records|affected_subject|state_record_ref|decision that all relevant refs are declared|PR-5 plans multi-pool aggregation|must not aggregate pools|yes|
|derived or temporary resources|state_record|projection|source_subject|state_projection_ref|decision that derived refs are safe|PR-5 plans derived-resource authority|must not derive values|yes|
|backlash|event_commitment|transaction result|target_subject|transaction_result_ref|decision before consequence commitment|PR-5 plans backlash consequence families|must not apply injury/world changes|yes|
|consequence families|event_commitment|state_delta|target_subject|state_delta_ref|decision that family validation is needed|PR-5 names families without execution|must not select consequences|yes|
|consequence severity|event_commitment|runtime trace|authority_source|runtime_trace_ref|decision that severity must be backend-owned|PR-5 plans severity inputs|must not roll or calculate severity|yes|
|injury/resource/world deltas|state_delta|event commitment|blocking_dependency|event_commitment_request_ref|decision that delta refs are bounded|PR-5 plans handoff to deltas|must not apply deltas|yes|
|duplicate costs|transaction|command envelope|source_subject|command_envelope_ref|decision that duplicates route to validation|PR-5 plans duplicate-cost semantics|must not deduplicate costs|yes|
|negative costs|transaction|schema registry|authority_source|schema_registry_ref|decision that shape is invalid or escalated|PR-5 plans allowed sign policy|must not convert refunds|yes|
|cross-resource conversion|transaction|table/oracle or schema ref|authority_source|schema_registry_ref|decision that conversion requires owner validation|PR-5 plans conversion boundary|must not calculate conversion|yes|
|source-local resource systems|source_local_construct|canon boundary|authority_source|source_local_ref|decision that source-local remains non-canon|PR-5 plans source-local resource posture|must not promote canon|yes|
|vehicle/platform pools|state_record|vehicle/platform record|affected_subject|state_record_ref|decision that platform pool is related|PR-5 plans vehicle-pool ownership|must not spend vehicle resources|yes|
|companion/summon costs|command|companion state|affected_subject|state_record_ref|decision that companion refs are declared|PR-5 plans companion cost boundaries|must not mutate companion state|yes|
|crafting/salvage/requisition|transaction|inventory-like state record|target_subject|state_record_ref|decision that requisition validation is required|PR-5 plans crafting math boundaries|must not add inventory behavior|yes|
|cultivation breakthrough costs|command|cultivation track state|affected_subject|state_record_ref|decision that breakthrough refs are bound|PR-5 plans cultivation resource categories|must not calculate breakthrough|yes|
|horror/sanity/stress pressures|command|hidden information or actor state|source_subject|hidden_information_ref|decision that player-safe validation is required|PR-5 plans stress/sanity resource posture|must not reveal hidden info or apply stress|yes|
|persistent campaign consequences|event_commitment|event ledger|target_subject|event_ledger_ref|decision that persistent consequence needs commitment validation|PR-5 plans consequence persistence boundary|must not persist or append events|yes|

## 20. CORPUS-SCALE PRESSURE REVIEW

A 200-400 source mixed donor corpus is mandatory pressure. The current shapes are adequate for planning because they provide neutral subject and relationship vocabulary without importing donor systems.

|pressure|primary validation subject|possible related subject|subject relation|dependency reference|failure route|downstream owner|lawful escalation point|current shapes adequate|
|---|---|---|---|---|---|---|---|---|
|class/archetype systems|command|schema record|authority_source|schema_registry_ref|reject_by_schema_mismatch|RT004/RT011|doctrine review or PR-5 planning|adequate|
|point-buy systems|transaction|state record pool|blocking_dependency|state_record_ref|request_downstream_domain_validation|RT002|PR-5 math plan|adequate|
|professions/occupations|source_local_construct|canon boundary|authority_source|source_local_ref|reject_source_local_authority|RT012|canon promotion review|adequate|
|narrative tags/aspects|command|context projection|source_subject|context_projection_ref|reject_hidden_info_leak|RT005|context/hidden-info owner|adequate|
|cultivation|command|state record track|affected_subject|state_record_ref|request_downstream_domain_validation|RT002/RT004|resource/ability owner|adequate|
|cyberware/biotech|transaction|state delta|target_subject|state_delta_ref|block_event_commitment|RT003/RT010|combat/inventory owners|adequate|
|psionics|command|hidden information|source_subject|hidden_information_ref|reject_hidden_info_leak|RT005|hidden-info owner|adequate|
|horror/investigation|context_projection|actor knowledge|source_subject|hidden_information_ref|reject_hidden_info_leak|RT005/RT007|social/knowledge owner|adequate|
|vehicles/mechs/ships|transaction|platform state|affected_subject|state_record_ref|block_transaction_before_commitment|RT010|inventory/vehicle owner|adequate|
|companions/summons|command|companion state|affected_subject|state_record_ref|request_downstream_domain_validation|RT007/RT010|companion owner|adequate|
|crafting/salvage/requisition|transaction|asset state|target_subject|state_record_ref|block_transaction_before_commitment|RT010|inventory owner|adequate|
|random tables/oracles|command|table oracle|authority_source|schema_registry_ref|escalate_doctrine_gap|RT009|RNG/table owner|adequate as reference-only|
|source-local cosmologies|source_local_construct|canon boundary|authority_source|source_local_ref|reject_source_local_authority|RT012|promotion boundary|adequate|
|adventure paths|command|source-local construct|source_subject|source_local_ref|quarantine_generated_content|RT008/RT012|generated/provenance owner|adequate|
|mixed-genre cross-book interactions|transaction|multiple dependencies|blocking_dependency|validation_request_ref|request_downstream_domain_validation|RT011|downstream validation|adequate|
|generated content|generated_content|provenance record|provenance_source|generated_content_provenance_ref|quarantine_generated_content|RT008|provenance owner|adequate|
|hidden actor knowledge|context_projection|hidden information|source_subject|hidden_information_ref|reject_hidden_info_leak|RT005/RT007|hidden-info owner|adequate|
|persistent world changes|event_commitment|event ledger|target_subject|event_ledger_ref|block_event_commitment|RT001/RT003|event commitment owner|adequate|

## 21. DOMAIN AND KERNEL HANDOFF REVIEW

|surface|represented by reference|typed dependency available|operationally invoked|acceptable now|future integration owner|residual risk|readiness for PR-5 planning|
|---|---|---|---|---|---|---|---|
|Domain command lifecycle|command_lifecycle_ref|command_lifecycle_ref|no|yes|RT001 / command lifecycle|shape-only reference can be stale|ready|
|Domain action legality|action_legality_ref|action_legality_ref|no|yes|RT001 / action legality|no dereference yet|ready|
|Domain state store|state_record_ref|state_record_ref/state_snapshot_ref|no|yes|RT002/RT010 plus state store|object existence deferred|ready|
|Domain state projection|state_projection_ref|state_projection_ref|no|yes|RT005 / projection|visibility must remain backend checked|ready|
|Domain transaction lifecycle|transaction_ref|transaction_ref/transaction_result_ref|no|yes|transaction lifecycle|transaction execution not invoked|ready|
|Domain event commitment|event_commitment_ref|event_commitment_request_ref/event_commitment_result_ref|no|yes|event commitment|append forbidden|ready|
|Domain future resource/consequence math|resource/consequence refs not yet implemented|available indirectly through state/action/transaction refs|no|yes for planning|RT002 / PR-5|PR-5 must not implement math in validation integration|ready|
|Kernel schema registry|schema_registry_ref|schema_registry_ref|no|yes|schema registry|schema lookup deferred|ready|
|Kernel record identity|record_identity_ref|record_identity_ref|no|yes|record identity|typed identity format future work|ready|
|Kernel command envelope|command_envelope_ref|command_envelope_ref|no|yes|command envelope|shape-only|ready|
|Kernel transaction preview|transaction_plan_ref|transaction_plan_ref|no|yes|transaction preview|preview execution absent|ready|
|Kernel state delta|state_delta_ref|state_delta_ref|no|yes|state delta|delta application forbidden|ready|
|Kernel event ledger|event_ledger_ref|event_ledger_ref|no|yes|event ledger|append forbidden|ready|
|Kernel validation pipeline|validation_pipeline_ref|validation_pipeline_ref|no|yes|validation pipeline|pipeline not called|ready|
|Kernel hidden information|hidden_information_ref|hidden_information_ref|no|yes|hidden info|semantic safety still backend-owned|ready|
|Kernel context projection|context_projection_ref|context_projection_ref|no|yes|context projection|projection not compiled|ready|
|Kernel persistence boundary|persistence_boundary_ref|persistence_boundary_ref|no|yes|persistence boundary|persistence absent|ready|
|Kernel replay audit|replay_audit_ref|replay_audit_ref|no|yes|replay audit|hash/replay authority deferred|ready|
|Kernel runtime trace|runtime_trace_ref|runtime_trace_ref|no|yes|runtime trace|semantic trace dereference deferred|ready|
|Kernel RNG interface|rng/table refs only|none dedicated yet|no|yes|RT009|RNG never invoked|ready|
|Kernel table/oracle|table/oracle refs only|none dedicated yet|no|yes|RT009|oracle never invoked|ready|

## 22. RISK REVIEW

|risk|severity|affected owner|current mitigation|required future test|required before PR-5 planning|required before PR-5 implementation|required before executable validation|PR-4G required|
|---|---|---|---|---|---|---|---|---|
|route relation is semantically incompatible with route type|medium|RT011|route type/decision compatibility; subject relation typed|compatibility matrix tests|no|yes|yes|false|
|route subject lacks a typed dependency|medium|RT011/PR-5|explicit subject type/ref/relation|cross-subject dependency tests|no|yes|yes|false|
|result subject lacks a typed dependency|medium|RT011/PR-5|request/result subject binding and request dependency|primary subject dependency tests|no|yes|yes|false|
|result/request declaration matches but referenced request differs|high|RT011|validation_request_ref exact ID binding|dereference/snapshot tests|no|yes|yes|false|
|trace dependency exists but points to semantically unrelated trace|medium|runtime trace|exact ID binding|trace dereference tests|no|no|yes|false|
|validation-result dependency exists but points to unrelated result|medium|RT011|exact validation_result_ref binding|result dereference tests|no|no|yes|false|
|provenance dependency is typed but unrelated to generated content|medium|RT008|exact provenance set equality|provenance object linkage tests|no|yes|yes|false|
|duplicate route IDs create audit ambiguity|medium|RT011/replay audit|none beyond tuple preservation|duplicate route ID tests|no|yes|yes|false|
|multiple cross-subject routes lack ordering|low|RT011|tuple order preserved|ordering/priority tests if policy added|no|no|yes|false|
|validation_ready is treated as successful validation|critical|RT002/RT011|passed false, blocking true, non-terminal stage|PR-5 gate tests requiring validation_passed for mutation|no|yes|yes|false|
|request trace remains optional|low|RT011/runtime trace|result trace required; request trace bound when present|request trace policy tests|no|no|yes|false|
|dependency hidden_info_safe conflicts with result safety|medium|RT005|result hidden_info_safe enforced for ready/pass|dependency hidden-info tests|no|yes|yes|false|
|dependency metadata contradicts binding fields|low|RT011|binding fields authoritative|metadata contradiction tests|no|no|yes|false|
|nested metadata remains mutable through manual construction|medium|replay audit|factory deep copy and mapping proxy|recursive freeze tests|no|no|yes|false|
|source-local validation is mistaken for canon authority|critical|RT012|anti-authority prose and false canon authorization|canon-boundary tests|no|yes|yes|false|
|resource math begins calculating inside validation integration|critical|RT002|no implementation changes; non-execution guardrails|import/call guard tests|no|yes|yes|false|
|factory/validator parity regresses|high|RT011|focused residual tests and validator checks|manual frozen-object tests|no|yes|yes|false|
|historic tests were weakened rather than adapted|medium|RT011|existing PR-4B/4D/4E tests retained|historic test diff review|no|yes|yes|false|

## 23. HARDENING LEDGER

|hardening ID|issue|current PR-4E behavior|desired invariant|severity|required before PR-5 planning|required before PR-5 implementation|required before executable validation|future owner|recommended PR|
|---|---|---|---|---|---|---|---|---|---|
|PR4F-H01|route-type/relation compatibility|Relations are typed but not constrained per route type.|Owner-specific compatibility matrix when semantics are executable.|medium|no|yes|yes|RT011|PR-5/validation implementation hardening|
|PR4F-H02|cross-subject route dependency binding|Cross-subject routes may omit matching dependencies.|Require linkage when executable owners need dereference.|medium|no|yes|yes|RT011|PR-5 implementation readiness|
|PR4F-H03|primary subject dependency binding|Primary subject can be declared without a typed subject dependency.|Bind primary subject to dependency or request snapshot before execution.|medium|no|yes|yes|RT011/PR-5|PR-5 implementation readiness|
|PR4F-H04|request-object dereference|validation_request_ref is exact but not dereferenced.|Dereference immutable request or snapshot.|high|no|yes|yes|RT011|executable validation integration|
|PR4F-H05|trace-object dereference|runtime_trace_ref exact ID is not semantically verified.|Dereference trace under runtime trace owner.|medium|no|no|yes|runtime trace|executable validation integration|
|PR4F-H06|validation-result dereference|validation_result_ref exact ID is not dereferenced.|Dereference committed validation result when needed.|medium|no|no|yes|RT011|executable validation integration|
|PR4F-H07|provenance-object linkage|Provenance set equality is typed ID linkage only.|Link generated content to provenance object schema.|medium|no|yes|yes|RT008|PR-5 implementation readiness|
|PR4F-H08|dependency hidden-info posture|Binding dependencies may be hidden_info_safe=False.|Define whether required bindings must be hidden-info safe.|medium|no|yes|yes|RT005|PR-5 implementation readiness|
|PR4F-H09|duplicate route IDs|Duplicate route IDs are accepted.|Unique route IDs before audit/replay authority.|medium|no|yes|yes|RT011/replay audit|PR-5 implementation readiness|
|PR4F-H10|duplicate semantic routes|Duplicate route tuples are accepted.|Deduplicate or declare lawful duplicates.|low|no|no|yes|RT011|executable validation integration|
|PR4F-H11|route ordering/priority|Tuple order preserved; no priority semantics.|Add priority only if execution requires it.|low|no|no|yes|RT011|deferred|
|PR4F-H12|request trace requirement|Request trace dependency enforced only when trace_id present.|Decide if all requests require trace.|low|no|no|yes|runtime trace|deferred|
|PR4F-H13|recursive metadata immutability|Factory deep-copies top metadata into mapping proxy; nested mutability can exist in manual construction.|Recursive freeze before replay/hash authority.|medium|no|no|yes|replay audit|executable validation integration|
|PR4F-H14|typed identity format|IDs are non-empty strings, not format-validated.|Adopt typed identity grammar.|medium|no|yes|yes|record identity|PR-5 implementation readiness|
|PR4F-H15|reserved decision/stage mappings|Mappings are fixed constants but not owner-reserved beyond tests.|Reserve mappings under validation owner.|low|no|yes|yes|RT011|PR-5 implementation readiness|

## 24. GATE DECISION

```yaml
gate_finding:
  validation_integration_residual_hardening_review_complete: true
  pr_4e_scope_confirmed: true
  pr_4d_blockers_closed: true
  subject_relation_vocabulary_acceptable: true
  same_subject_and_cross_subject_semantics_acceptable: true
  request_result_subject_binding_acceptable: true
  typed_dependency_linkage_acceptable: true
  dependency_uniqueness_acceptable: true
  provenance_linkage_acceptable: true
  validation_ready_posture_acceptable: true
  intermediate_stage_consistency_acceptable: true
  factory_validator_parity_acceptable: true
  anti_authority_guardrails_acceptable: true
  resource_consequence_math_planning_dependency_ready: true
  requires_pr_4g_hardening_before_pr_5: false
  ready_for_runtime_domain_pr_5_planning: true
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  validation_execution_authorized_by_this_pr: false
  invariant_evaluation_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  state_delta_application_authorized_by_this_pr: false
  event_ledger_append_authorized_by_this_pr: false
  transaction_execution_authorized_by_this_pr: false
  actual_event_commitment_authorized_by_this_pr: false
  persistence_authorized_by_this_pr: false
  replay_authorized_by_this_pr: false
  command_execution_authorized_by_this_pr: false
  resource_math_authorized_by_this_pr: false
  consequence_application_authorized_by_this_pr: false
  combat_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-5 resource and consequence math service planning
  next_step_status: planning_only
```

## 25. RECOMMENDED NEXT PR

Recommended next PR: **RUNTIME-DOMAIN-PR-5: Resource and Consequence Math Service Plan**.

PR-5 is planning-only. PR-5 must not implement resource calculation, consequence application, state mutation, event commitment, persistence, model behavior, or live play.

## 26. NON-IMPLEMENTATION REAFFIRMATION

PR-4F adds no runtime code, domain-service code, validation implementation changes, validation execution, invariant evaluation, state mutation, delta application, event append, transaction execution, event commitment, persistence, replay, command execution, resource math, consequence application, combat, abilities, inventory, mission/social behavior, generated-content persistence, context-packet compiler, model integration, live-play adapter, UI, conversion, sourcebook inclusion, or canon promotion.

## 27. CLASSIFICATION BLOCK

```yaml
runtime_domain_pr_4f:
  review_id: RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001
  artifact_type: validation_integration_residual_hardening_review_gate
  implementation_status: non_executable_review_gate
  derives_from:
    - RUNTIME-DOMAIN-PR-4E-VALIDATION-INTEGRATION-RESIDUAL-SKELETON-HARDENING-001
    - RUNTIME-DOMAIN-PR-4D-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-REVIEW-001
    - RUNTIME-DOMAIN-PR-4C-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-001
    - RUNTIME-DOMAIN-PR-4B-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-REVIEW-001
    - RUNTIME-DOMAIN-PR-4A-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-IMPLEMENTATION-001
    - RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
    - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
    - RT-001
    - RT-002
    - RT-005
    - RT-008
    - RT-011
  reviews_pr_4d_blocker_closure: true
  reviews_subject_relation_vocabulary: true
  reviews_failure_route_subject_semantics: true
  reviews_route_subject_dependency_linkage: true
  reviews_request_result_subject_binding: true
  reviews_typed_dependencies: true
  reviews_provenance_linkage: true
  reviews_dependency_uniqueness: true
  reviews_validation_ready_posture: true
  reviews_intermediate_stage_consistency: true
  reviews_failure_route_aggregates: true
  reviews_factory_validator_parity: true
  reviews_immutability_and_serialization: true
  reviews_non_execution_posture: true
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
  authorizes_consequence_application_by_this_pr: false
  authorizes_combat_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-5 resource and consequence math service planning, pending review
```

## Appendix A. Adversarial probe ledger

|probe|outcome|meaning|
|---|---|---|
|same-subject route with mismatched subject|rejected|same_subject failure routes must match result subject|
|cross-subject route using same subject pair|rejected|cross-subject failure routes must reference a different subject|
|route relation semantically odd for route type|accepted|odd pairing is not a PR-4G blocker; owner-specific policy|
|cross-subject route without matching dependency|accepted|sufficient for PR-5 planning, hardening before implementation/execution|
|unrelated request dependency ID|rejected|validation_request_ref must match validation_request_id|
|two runtime_trace_ref dependencies|rejected|exactly one runtime_trace_ref required for trace_id|
|two different validation_result_ref dependencies|rejected|exactly one validation_result_ref required when result ref exists|
|generated-content mismatched provenance sets|rejected|provenance_ref_ids must exactly match typed provenance dependencies|
|validation_ready with hidden_info_safe=False|rejected|validation_ready requires hidden_info_safe=True|
|validation_ready with terminal stage|rejected|decision/final_stage incompatible|
|repeated failure-route IDs|accepted|audit hardening, not PR-5 planning blocker|
|two semantically duplicate routes|accepted|dedup/priority deferred|
|manual list-valued dependencies instead of tuple|validator returns false|manual frozen-object validator rejects non-tuple dependencies|
|dependency hidden_info_safe=False otherwise safe result|accepted|dependency hidden-info posture future hardening|

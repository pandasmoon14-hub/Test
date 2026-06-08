# RUNTIME-DOMAIN-PR-1: Command Lifecycle and Action Legality Service Plan

---

## 1. Purpose and status

This document is **RUNTIME-DOMAIN-PR-1**, a planning-only command lifecycle and action legality service plan.

It follows **RUNTIME-DOMAIN-PR-0** (Domain Service Implementation Sequencing Plan), which confirmed that command lifecycle and action legality is the first domain-service family and that RUNTIME-DOMAIN-PR-1 is the next allowed planning step.

This document authorizes only a future narrow implementation PR (RUNTIME-DOMAIN-PR-1A) after review. It does not implement code.

**Artifact type:** command_lifecycle_action_legality_service_plan
**Implementation status:** non_executable_plan
**Review ID:** RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001

---

## 2. Source ledger

### Primary sequencing source

| Source | ID | Status |
|---|---|---|
| RUNTIME-DOMAIN-PR-0 | RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001 | active |

### Primary gate source

| Source | ID | Status |
|---|---|---|
| RUNTIME-IMPL-PR-8 | RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001 | active |

### Kernel implementation and planning sources

| Source | ID | File |
|---|---|---|
| RUNTIME-IMPL-PR-0 | RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001 | docs/doctrine/reviews/runtime_impl_pr_0_minimum_backend_kernel_executable_implementation_plan.md |
| RUNTIME-SEQ-PR-A | (minimum backend kernel runtime quality contract plan) | docs/doctrine/reviews/runtime_seq_pr_a_minimum_backend_kernel_runtime_quality_contract_plan.md |
| RUNTIME-SEQ-PR-B | (narration context packet contract plan) | docs/doctrine/reviews/runtime_seq_pr_b_narration_context_packet_contract_plan.md |
| RUNTIME-SEQ-PR-C | (state event invariant transaction plan) | docs/doctrine/reviews/runtime_seq_pr_c_state_event_invariant_transaction_plan.md |
| RUNTIME-SEQ-PR-D | (story capable structure playable content plan) | docs/doctrine/reviews/runtime_seq_pr_d_story_capable_structure_playable_content_plan.md |
| RUNTIME-SEQ-PR-E | (model evaluation structured output adversarial command plan) | docs/doctrine/reviews/runtime_seq_pr_e_model_evaluation_structured_output_adversarial_command_plan.md |
| RUNTIME-SEQ-PR-F | (implementation readiness executable kernel authorization gate) | docs/doctrine/reviews/runtime_seq_pr_f_implementation_readiness_executable_kernel_authorization_gate.md |
| Runtime Schema Sequencing | (runtime schema implementation sequencing review) | docs/doctrine/reviews/runtime_schema_implementation_sequencing_review.md |

### Implementation PRs (RUNTIME-IMPL-PR-1 through PR-7)

| PR | Kernel modules |
|---|---|
| RUNTIME-IMPL-PR-1 | schema_registry, record_identity |
| RUNTIME-IMPL-PR-2 | command_envelope, transaction_preview |
| RUNTIME-IMPL-PR-3 | state_delta, event_ledger |
| RUNTIME-IMPL-PR-4 | rng_interface, table_oracle |
| RUNTIME-IMPL-PR-5 | validation_pipeline |
| RUNTIME-IMPL-PR-6 | hidden_information, context_projection |
| RUNTIME-IMPL-PR-7 | persistence_boundary, replay_audit, runtime_trace |

### Owner specifications

| Spec | Track | File |
|---|---|---|
| RT-001 | command lifecycle and action legality | docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md |
| RT-002 | resource consequence math | docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md |
| RT-003 | combat hazard damage recovery | docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md |
| RT-004 | ability effect skill binding | docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md |
| RT-005 | context packet hidden information | docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md |
| RT-006 | mission reward clue routing | docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md |
| RT-007 | social faction actor knowledge | docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md |
| RT-008 | generated content provenance recurrence | docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md |
| RT-009 | runtime RNG table oracle | docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md |
| RT-010 | inventory item vehicle asset | docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md |
| RT-011 | validation readiness tooling | docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md |
| RT-012 | D-series promotion boundary | docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md |

### Current kernel skeleton modules

| Module | Path | Status |
|---|---|---|
| schema_registry | src/astra_runtime/kernel/schema_registry.py | skeleton_complete |
| record_identity | src/astra_runtime/kernel/record_identity.py | skeleton_complete |
| command_envelope | src/astra_runtime/kernel/command_envelope.py | skeleton_complete |
| transaction_preview | src/astra_runtime/kernel/transaction_preview.py | skeleton_complete |
| state_delta | src/astra_runtime/kernel/state_delta.py | skeleton_complete |
| event_ledger | src/astra_runtime/kernel/event_ledger.py | skeleton_complete |
| rng_interface | src/astra_runtime/kernel/rng_interface.py | skeleton_complete |
| table_oracle | src/astra_runtime/kernel/table_oracle.py | skeleton_complete |
| validation_pipeline | src/astra_runtime/kernel/validation_pipeline.py | skeleton_complete |
| hidden_information | src/astra_runtime/kernel/hidden_information.py | skeleton_complete |
| context_projection | src/astra_runtime/kernel/context_projection.py | skeleton_complete |
| persistence_boundary | src/astra_runtime/kernel/persistence_boundary.py | skeleton_complete |
| replay_audit | src/astra_runtime/kernel/replay_audit.py | skeleton_complete |
| runtime_trace | src/astra_runtime/kernel/runtime_trace.py | skeleton_complete |

### Runtime skeleton tests

| Test | Path |
|---|---|
| test_schema_registry_skeleton | tests/runtime/test_schema_registry_skeleton.py |
| test_record_identity_skeleton | tests/runtime/test_record_identity_skeleton.py |
| test_command_envelope_skeleton | tests/runtime/test_command_envelope_skeleton.py |
| test_transaction_preview_skeleton | tests/runtime/test_transaction_preview_skeleton.py |
| test_state_delta_skeleton | tests/runtime/test_state_delta_skeleton.py |
| test_event_ledger_skeleton | tests/runtime/test_event_ledger_skeleton.py |
| test_rng_interface_skeleton | tests/runtime/test_rng_interface_skeleton.py |
| test_table_oracle_skeleton | tests/runtime/test_table_oracle_skeleton.py |
| test_validation_pipeline_skeleton | tests/runtime/test_validation_pipeline_skeleton.py |
| test_hidden_information_skeleton | tests/runtime/test_hidden_information_skeleton.py |
| test_context_projection_skeleton | tests/runtime/test_context_projection_skeleton.py |
| test_persistence_boundary_skeleton | tests/runtime/test_persistence_boundary_skeleton.py |
| test_replay_audit_skeleton | tests/runtime/test_replay_audit_skeleton.py |
| test_runtime_trace_skeleton | tests/runtime/test_runtime_trace_skeleton.py |

### Registry and decision log

| File | Path |
|---|---|
| Doctrine registry | docs/doctrine/astra_doctrine_registry_v0_1.yaml |
| Decision log | docs/decisions/current_decisions_log.md |

### Schema files (C00–C14)

| Schema | Path | Present |
|---|---|---|
| C00 shared content record base and schema registry | docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md | yes |
| C01 creature NPC record schema | docs/doctrine/schema/C01_creature_npc_record_schema.md | yes |
| C02 item gear record schema | docs/doctrine/schema/C02_item_gear_record_schema.md | yes |
| C03 ability power technique record schema | docs/doctrine/schema/C03_ability_power_technique_record_schema.md | yes |
| C04 relic implant installable asset schema | docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md | yes |
| C05 faction institution record schema | docs/doctrine/schema/C05_faction_institution_record_schema.md | yes |
| C06 location site region record schema | docs/doctrine/schema/C06_location_site_region_record_schema.md | yes |
| C07 mission scenario adventure record schema | docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md | yes |
| C08 vehicle ship platform record schema | docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md | yes |
| C09 hazard environment record schema | docs/doctrine/schema/C09_hazard_environment_record_schema.md | yes |
| C10 table oracle record schema | docs/doctrine/schema/C10_table_oracle_record_schema.md | yes |
| C11 companion summon record schema | docs/doctrine/schema/C11_companion_summon_record_schema.md | yes |
| C12 crafting salvage recipe record schema | docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md | yes |
| C13 map diagram record schema | docs/doctrine/schema/C13_map_diagram_record_schema.md | yes |
| C14 source local setting cosmology record schema | docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md | yes |

---

## 3. Backend-first invariant

### Core invariant

Astra Ascension must be model-interchangeable. The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

### Service implication

The Command Lifecycle and Action Legality service is the first domain service boundary. It may classify, normalize, validate, and preview commands, but it must not execute commands, mutate state, commit events, roll randomness outside the RNG interface, expose hidden information, or use LLM output as authority.

Every command lifecycle decision and every legality determination must be traceable to backend-owned data and kernel-validated structures. No model output may serve as the basis for accepting, rejecting, or routing a command.

---

## 4. Service ownership

### Primary owner

| Owner | Track | Specification |
|---|---|---|
| RT-001 | command lifecycle and action legality | docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md |

### Secondary owner dependencies

| Owner | Track | Dependency reason |
|---|---|---|
| RT-011 | validation readiness and tooling | validation governance for lifecycle/legality results |
| RT-002 | resource/consequence math | future cost precheck handoff only |
| RT-005 | hidden information/context packet | visibility restrictions on rejection reasons and legality results |
| RT-009 | RNG/table oracle | future randomness dependency declarations only |
| RT-012 | D-series promotion boundary | prevent native-design doctrine from becoming direct runtime authority |

### This service must not own

- resource math (RT-002);
- combat math (RT-003);
- ability/effect resolution (RT-004);
- context-packet compilation (RT-005 future implementation);
- mission/clue routing (RT-006);
- social/faction knowledge (RT-007);
- generated-content durability (RT-008);
- RNG/table/oracle execution (RT-009);
- inventory behavior (RT-010);
- model evaluation (future model harness);
- live-play adapter behavior (future live-play gate).

---

## 5. Future service responsibilities

### Allowed future responsibilities

The command lifecycle and action legality service, when implemented, may:

1. Accept a backend command envelope (via kernel `command_envelope` interface).
2. Classify command lifecycle stage.
3. Normalize command intent into backend-owned categories.
4. Validate envelope shape through kernel validation interfaces.
5. Perform non-domain action legality prechecks (envelope completeness, actor existence, target validity, timing, scope).
6. Produce legality result records or preview-oriented validation results.
7. Route to future domain services for domain-specific resolution.
8. Identify blocked, quarantined, or rejected commands.
9. Require confirmation when needed (e.g., irreversible actions, high-cost actions).
10. Declare required downstream dependencies (which domain services must participate before execution).
11. Trace every command lifecycle decision via kernel `runtime_trace` interface.
12. Preserve hidden-information boundaries (rejection reasons must not reveal hidden state).
13. Preserve model non-authority (no LLM output used as command classification or legality source).

### Forbidden responsibilities

The command lifecycle and action legality service must never:

1. Execute commands.
2. Mutate state.
3. Access state store as authority (read-only projection for legality checks only, when state service exists).
4. Commit events to the event ledger.
5. Own transaction lifecycle (transaction planning/commitment is a separate service).
6. Calculate resource costs (RT-002 owns cost formulas).
7. Resolve combat or damage (RT-003).
8. Resolve ability or effect outcomes (RT-004).
9. Mutate inventory (RT-010).
10. Mutate mission or clue state (RT-006).
11. Mutate social or faction state (RT-007).
12. Persist generated content (RT-008).
13. Compile context packets (RT-005 future implementation).
14. Call models or construct prompts.
15. Own live-play loop behavior.
16. Own UI behavior.
17. Execute conversion.
18. Promote canon.

---

## 6. Command lifecycle state model

The following is a proposed command lifecycle state model for future implementation. This is planning only. No Python enum, dataclass, or code is created by this document.

### State: received

- **Meaning:** A command envelope has arrived at the service boundary.
- **Required inputs:** Raw command envelope from the kernel `command_envelope` interface.
- **Allowed outputs:** Transition to `envelope_validated` or `rejected`.
- **Kernel dependencies:** `command_envelope` (create/validate).
- **Prohibited behavior:** No state reads, no event writes, no model calls.
- **Downstream handoff:** None; internal to command lifecycle service.

### State: envelope_validated

- **Meaning:** The command envelope passes structural validation (correct shape, required fields, valid types).
- **Required inputs:** Command envelope that passed `validate_command_envelope`.
- **Allowed outputs:** Transition to `actor_bound` or `rejected`.
- **Kernel dependencies:** `command_envelope`, `validation_pipeline`.
- **Prohibited behavior:** No domain-specific validation, no state mutation, no model calls.
- **Downstream handoff:** None; internal to command lifecycle service.

### State: actor_bound

- **Meaning:** The source actor ID in the envelope resolves to a valid record identity.
- **Required inputs:** Validated envelope, actor record ID confirmed via `record_identity`.
- **Allowed outputs:** Transition to `visibility_checked` or `rejected` (blocked_by_missing_actor).
- **Kernel dependencies:** `record_identity`, `command_envelope`.
- **Prohibited behavior:** No actor state mutation, no state store writes, no model calls.
- **Downstream handoff:** None; internal to command lifecycle service.

### State: visibility_checked

- **Meaning:** Hidden-information boundaries have been checked to ensure the actor may know about the action they are attempting.
- **Required inputs:** Actor-bound envelope, hidden-information visibility check via `hidden_information`/`context_projection`.
- **Allowed outputs:** Transition to `legality_prechecked` or `rejected` (blocked_by_hidden_information).
- **Kernel dependencies:** `hidden_information`, `context_projection`.
- **Prohibited behavior:** No hidden state revealed in rejection reasons, no model calls, no state mutation.
- **Downstream handoff:** None; internal to command lifecycle service.

### State: legality_prechecked

- **Meaning:** Non-domain action legality prechecks have passed (envelope valid, actor exists, target valid, timing legal, scope legal, not hidden-information-blocked).
- **Required inputs:** Visibility-checked envelope, legality precheck results from action legality evaluation.
- **Allowed outputs:** Transition to `dependency_declared` or `rejected` or `quarantined`.
- **Kernel dependencies:** `validation_pipeline`, `command_envelope`.
- **Prohibited behavior:** No domain-specific rule evaluation, no resource cost calculation, no combat resolution, no model calls, no state mutation.
- **Downstream handoff:** None; internal to command lifecycle service.

### State: dependency_declared

- **Meaning:** The service has identified which downstream domain services are required to fully resolve this command (e.g., RT-002 for cost, RT-003 for combat, RT-004 for ability effects).
- **Required inputs:** Legality-prechecked envelope, command type classification.
- **Allowed outputs:** Transition to `preview_requested` or `confirmation_required` or `accepted_for_transaction_planning`.
- **Kernel dependencies:** `command_envelope` (command_type), `schema_registry` (command type registry, later).
- **Prohibited behavior:** No domain resolution, no downstream service calls yet, no model calls, no state mutation.
- **Downstream handoff:** Dependency declarations passed forward with the command for future routing.

### State: preview_requested

- **Meaning:** A transaction preview has been requested for this command before commitment.
- **Required inputs:** Dependency-declared envelope, preview creation via `transaction_preview`.
- **Allowed outputs:** Transition to `confirmation_required` or `accepted_for_transaction_planning` or `cancelled`.
- **Kernel dependencies:** `transaction_preview` (create, not execute).
- **Prohibited behavior:** No state mutation, no event commitment, no resource spending, no model calls. Preview is read-only.
- **Downstream handoff:** Transaction preview record passed to future transaction lifecycle service.

### State: confirmation_required

- **Meaning:** The command requires explicit player or system confirmation before proceeding (e.g., irreversible actions, high-cost actions, ambiguous intent).
- **Required inputs:** Preview or dependency declaration indicating confirmation is needed.
- **Allowed outputs:** Transition to `accepted_for_transaction_planning` or `cancelled`.
- **Kernel dependencies:** `command_envelope`, `transaction_preview`.
- **Prohibited behavior:** No automatic execution, no state mutation, no event commitment, no model calls.
- **Downstream handoff:** Confirmation requirement record surfaced to future live-play adapter (when it exists).

### State: accepted_for_transaction_planning

- **Meaning:** The command has passed all command lifecycle and action legality checks and is accepted for handoff to the future transaction lifecycle service.
- **Required inputs:** Fully validated, legality-checked, dependency-declared command with any required confirmations satisfied.
- **Allowed outputs:** Handoff to future transaction lifecycle service. No further transitions within command lifecycle.
- **Kernel dependencies:** `command_envelope`, `runtime_trace` (trace acceptance).
- **Prohibited behavior:** No execution, no state mutation, no event commitment, no resource spending. This service's work is done.
- **Downstream handoff:** Command envelope + legality result + dependency declarations + preview (if any) handed to future transaction lifecycle service.

### State: rejected

- **Meaning:** The command has been determined to be illegal, invalid, or blocked. It will not proceed.
- **Required inputs:** Any lifecycle stage that determined rejection, with a legality block reason.
- **Allowed outputs:** Rejection result record. No further transitions.
- **Kernel dependencies:** `validation_pipeline` (issue records), `runtime_trace` (trace rejection), `hidden_information` (ensure rejection reason is hidden-info-safe).
- **Prohibited behavior:** No state mutation, no event commitment, no hidden-information leaks in rejection messages. Rejection reasons visible to the player must not reveal backend-hidden state.
- **Downstream handoff:** Rejection result surfaced to future live-play adapter (when it exists). No transaction planning.

### State: quarantined

- **Meaning:** The command cannot be classified, validated, or resolved with current information. It is held for review or future processing.
- **Required inputs:** Any lifecycle stage that determined quarantine is needed (e.g., unsupported command type, ambiguous intent, missing schema support).
- **Allowed outputs:** Quarantine result record. May later transition to `received` (retry) or `rejected`.
- **Kernel dependencies:** `validation_pipeline` (quarantine issues), `runtime_trace` (trace quarantine).
- **Prohibited behavior:** No execution, no state mutation, no event commitment, no model calls. Quarantined commands do not proceed silently.
- **Downstream handoff:** Quarantine result surfaced for review. No transaction planning until resolved.

### State: cancelled

- **Meaning:** The command was voluntarily withdrawn by the player or system before acceptance.
- **Required inputs:** Cancellation request during `preview_requested` or `confirmation_required` states.
- **Allowed outputs:** Cancellation result record. No further transitions.
- **Kernel dependencies:** `runtime_trace` (trace cancellation).
- **Prohibited behavior:** No state mutation, no event commitment, no partial execution.
- **Downstream handoff:** None. Command lifecycle ends.

---

## 7. Action legality decision model

The following defines future legality decision categories for the action legality service. This is planning only. No code is created by this document.

### Category: legal

- **Meaning:** The command is legal under current prechecks. Domain services may still reject it during full resolution.
- **Player-visible:** Yes.
- **Hidden-info safe:** Yes (does not reveal hidden state).
- **May proceed to transaction preview:** Yes.
- **Requires validation issue records:** No (no issues).
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** Transaction lifecycle service and relevant domain services.

### Category: illegal

- **Meaning:** The command violates a known rule or constraint that command lifecycle can determine without domain-specific resolution.
- **Player-visible:** Yes (with hidden-info-safe reason).
- **Hidden-info safe:** Must be verified; rejection reason must not reveal hidden state.
- **May proceed to transaction preview:** No.
- **Requires validation issue records:** Yes.
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** Command lifecycle (terminal).

### Category: requires_confirmation

- **Meaning:** The command appears legal but requires explicit confirmation before proceeding (e.g., irreversible, high cost, ambiguous).
- **Player-visible:** Yes.
- **Hidden-info safe:** Yes (confirmation prompt must not reveal hidden state).
- **May proceed to transaction preview:** Yes, after confirmation.
- **Requires validation issue records:** No (informational only).
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** Command lifecycle (after confirmation received).

### Category: requires_more_information

- **Meaning:** The command cannot be evaluated because required information is missing from the envelope (e.g., missing target, ambiguous intent).
- **Player-visible:** Yes.
- **Hidden-info safe:** Yes (request for information must not reveal hidden state).
- **May proceed to transaction preview:** No, until information is provided.
- **Requires validation issue records:** Yes.
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** Command lifecycle (after information received).

### Category: blocked_by_hidden_information

- **Meaning:** The command references or requires knowledge the actor does not have access to, based on hidden-information partition checks.
- **Player-visible:** Partially. The player is told the action cannot proceed, but the reason must not reveal what is hidden.
- **Hidden-info safe:** Critical. The rejection reason must be generic (e.g., "that action is not available") and must not disclose what the hidden information is.
- **May proceed to transaction preview:** No.
- **Requires validation issue records:** Yes (backend-only detail, player-facing redacted).
- **May produce future trace entry:** Yes (backend trace only, not player-visible).
- **Future service owning final resolution:** Hidden information service (RT-005) determines visibility; command lifecycle enforces the block.

### Category: blocked_by_missing_actor

- **Meaning:** The source actor ID in the command envelope does not resolve to a valid record identity.
- **Player-visible:** Yes.
- **Hidden-info safe:** Yes (actor existence is not hidden information in this context).
- **May proceed to transaction preview:** No.
- **Requires validation issue records:** Yes.
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** Command lifecycle (terminal unless actor is created).

### Category: blocked_by_invalid_target

- **Meaning:** The command specifies a target that does not exist or is not valid for the command type.
- **Player-visible:** Yes (if target existence is not hidden).
- **Hidden-info safe:** Must be verified; if target existence is hidden, use `blocked_by_hidden_information` instead.
- **May proceed to transaction preview:** No.
- **Requires validation issue records:** Yes.
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** Command lifecycle (terminal) or relevant domain service for target validity.

### Category: blocked_by_resource_precheck

- **Meaning:** A preliminary resource precheck indicates the actor likely cannot afford the command's cost. Final cost calculation belongs to RT-002.
- **Player-visible:** Yes (e.g., "you do not have enough resources").
- **Hidden-info safe:** Generally yes, but must not reveal exact hidden resource values if those are restricted.
- **May proceed to transaction preview:** No.
- **Requires validation issue records:** Yes.
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** RT-002 resource/consequence math service for final cost determination.

### Category: blocked_by_timing

- **Meaning:** The command is not legal at the current game-time, phase, or turn state (e.g., action already spent, not the actor's turn, cooldown active).
- **Player-visible:** Yes.
- **Hidden-info safe:** Generally yes (timing rules are typically public).
- **May proceed to transaction preview:** No.
- **Requires validation issue records:** Yes.
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** Command lifecycle (terminal) or relevant domain service for timing rules.

### Category: blocked_by_scope

- **Meaning:** The command exceeds the actor's current scope or authority (e.g., attempting an action at a location the actor is not at, targeting something out of range).
- **Player-visible:** Yes (if scope information is not hidden).
- **Hidden-info safe:** Must be verified; if scope information involves hidden state, adjust reason accordingly.
- **May proceed to transaction preview:** No.
- **Requires validation issue records:** Yes.
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** Relevant domain service for scope rules.

### Category: quarantined_for_validation

- **Meaning:** The command cannot be fully classified or validated with current system capabilities. It is quarantined for future processing or manual review.
- **Player-visible:** Yes (generic "command cannot be processed" message).
- **Hidden-info safe:** Yes.
- **May proceed to transaction preview:** No.
- **Requires validation issue records:** Yes.
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** Validation integration service (RT-011) for triage and review.

### Category: unsupported_command_type

- **Meaning:** The command type is not recognized by the current system. This includes donor-specific action types not yet canonized and genuinely invalid commands.
- **Player-visible:** Yes.
- **Hidden-info safe:** Yes.
- **May proceed to transaction preview:** No.
- **Requires validation issue records:** Yes.
- **May produce future trace entry:** Yes.
- **Future service owning final resolution:** Command lifecycle (terminal). May trigger RT-012 review if the command type originates from donor material.

---

## 8. Kernel interface consumption plan

The following matrix defines how the future command lifecycle and action legality service must consume kernel modules.

| Kernel module | Consumption | Reason | Allowed use | Forbidden use |
|---|---|---|---|---|
| schema_registry | required (later for command type registry) | Command type classification may require a registry of recognized command types. Initially, command types may be hardcoded; schema registry integration deferred until command type taxonomy stabilizes. | Look up recognized command types; validate command type against registry. | Registering new schemas at runtime; using schema registry as authority for domain rules. |
| record_identity | required | Source actor ID and target IDs must be validated as legitimate record identities. | Validate actor record IDs; validate target record IDs; build record IDs for result records. | Creating new record identities for game entities; mutating record identity state. |
| command_envelope | required | The command envelope is the primary input to the command lifecycle service. | Accept command envelopes; read command type, actor, payload, metadata; validate envelope structure. | Creating command envelopes on behalf of actors; modifying envelope contents after receipt; executing commands. |
| transaction_preview | required (preview handoff only) | The service may create transaction previews for commands that pass legality checks, but must not execute transactions. | Create transaction preview records; populate preview with legality result and dependency declarations. | Executing transactions; committing state changes via preview; treating preview as event commitment. |
| state_delta | later | The command lifecycle service does not produce state deltas. Future integration may allow reading projected state for legality checks, but this requires the state projection service. | None in initial skeleton. Future: read-only state projections for legality context. | Creating state deltas; applying state deltas; treating state delta as committed. |
| event_ledger | forbidden (direct writes) | The command lifecycle service must not commit events. Event commitment belongs to the future transaction lifecycle service. | None. Future: read-only event queries for timing/history checks, if authorized by future PR. | Writing events; committing events; appending to ledger; treating event ledger as state store. |
| rng_interface | optional (later, dependency declarations only) | Some commands may require randomness for resolution (e.g., attack rolls). The command lifecycle service declares this dependency but does not invoke the RNG. | Declare that a command requires RNG resolution; include RNG dependency in dependency declarations. | Rolling dice; generating random numbers; using RNG output for legality decisions; bypassing the RNG interface. |
| table_oracle | optional (later, dependency declarations only) | Some commands may reference table/oracle lookups for resolution. The command lifecycle service declares this dependency but does not invoke table lookups. | Declare that a command requires table/oracle resolution; include table dependency in dependency declarations. | Looking up table results; selecting oracle outcomes; using table output for legality decisions. |
| validation_pipeline | required | All legality decisions must produce validation results. Invalid envelopes must produce validation issues. | Run validation checks on command envelopes; produce ValidationResult records; produce ValidationIssue records for rejected/quarantined commands; run invariant prechecks. | Bypassing validation; treating validation as optional; silencing validation issues. |
| hidden_information | required (visibility-aware legality) | Legality checks must respect hidden-information boundaries. Rejection reasons must not reveal hidden state. | Check visibility tiers for actor/target/action; verify rejection reasons are hidden-info-safe; use redacted copies where needed. | Revealing hidden information; creating hidden information records; modifying visibility tiers. |
| context_projection | required (visibility-aware legality) | Context projections determine what an actor can see, which affects legality (e.g., an actor cannot target something they cannot perceive). | Project visible context for legality checks; verify actor has visibility to targets and actions. | Compiling full context packets; modifying context projections; using context projection as state store. |
| persistence_boundary | not_applicable | The command lifecycle service does not persist data. Persistence belongs to the future persistence service. | None. | Writing to persistence; reading from persistence as authority; bypassing persistence boundary. |
| replay_audit | not_applicable | The command lifecycle service does not participate in replay. Replay belongs to the future replay/audit service. | None. | Creating replay entries; auditing replay hashes; bypassing replay audit. |
| runtime_trace | required (once trace integration is authorized) | Every command lifecycle decision must be traceable. | Create trace entries for lifecycle state transitions; create trace entries for legality decisions; create trace entries for rejections, quarantines, cancellations. | Bypassing trace; omitting trace for any lifecycle transition; using trace as state store. |

---

## 9. Dependency and handoff boundaries

### Handoff: State store / state projection service

- **What command lifecycle may pass:** Accepted command envelope with legality result and dependency declarations.
- **What it must not decide:** What the current state is; what state values mean for domain rules; how state is stored or projected.
- **What kernel envelope/result must be used:** Command envelope (accepted_for_transaction_planning) plus legality result.
- **What remains blocked until that downstream service exists:** Any legality check that requires reading current game state (e.g., "does the actor have enough HP to take this action" requires state projection).

### Handoff: Transaction lifecycle / event commitment service

- **What command lifecycle may pass:** Accepted command envelope with legality result, dependency declarations, and optional transaction preview.
- **What it must not decide:** Whether the transaction commits; what events are produced; how state deltas are applied; rollback behavior.
- **What kernel envelope/result must be used:** Command envelope + transaction preview (if created) + legality result.
- **What remains blocked until that downstream service exists:** Actual command execution; event commitment; state mutation.

### Handoff: Validation integration / invariant enforcement service

- **What command lifecycle may pass:** Validation results and validation issues produced during legality checks.
- **What it must not decide:** Validation policy for other services; invariant definitions beyond command envelope shape.
- **What kernel envelope/result must be used:** ValidationResult and ValidationIssue records from validation_pipeline.
- **What remains blocked until that downstream service exists:** Cross-service invariant enforcement; validation aggregation across domain services.

### Handoff: Resource / consequence math service (RT-002)

- **What command lifecycle may pass:** Command envelope with resource precheck request (dependency declaration indicating cost evaluation needed).
- **What it must not decide:** Actual resource costs; whether the actor can afford the action (final determination); cost formulas; refund policies.
- **What kernel envelope/result must be used:** Command envelope + dependency declaration specifying RT-002 involvement.
- **What remains blocked until that downstream service exists:** Accurate resource precheck (blocked_by_resource_precheck may be approximate or skipped until RT-002 exists).

### Handoff: Combat / hazard / damage / recovery service (RT-003)

- **What command lifecycle may pass:** Command envelope classified as combat-related, with dependency declaration for RT-003.
- **What it must not decide:** Combat outcomes; damage values; hit/miss determination; hazard effects; recovery amounts.
- **What kernel envelope/result must be used:** Command envelope + dependency declaration specifying RT-003 involvement.
- **What remains blocked until that downstream service exists:** Combat command resolution; damage calculation; hazard evaluation.

### Handoff: Ability / effect / skill binding service (RT-004)

- **What command lifecycle may pass:** Command envelope involving abilities, effects, or skills, with dependency declaration for RT-004.
- **What it must not decide:** Ability effects; skill check outcomes; effect durations; binding rules.
- **What kernel envelope/result must be used:** Command envelope + dependency declaration specifying RT-004 involvement.
- **What remains blocked until that downstream service exists:** Ability/effect/skill resolution.

### Handoff: Inventory / item / vehicle / asset service (RT-010)

- **What command lifecycle may pass:** Command envelope involving item use, equipment changes, vehicle actions, with dependency declaration for RT-010.
- **What it must not decide:** Item effects; equipment stat changes; vehicle behavior; asset mutation.
- **What kernel envelope/result must be used:** Command envelope + dependency declaration specifying RT-010 involvement.
- **What remains blocked until that downstream service exists:** Inventory mutation; item use resolution; vehicle/asset behavior.

### Handoff: Mission / reward / clue routing service (RT-006)

- **What command lifecycle may pass:** Command envelope involving investigation, mission progress, clue interaction, with dependency declaration for RT-006.
- **What it must not decide:** Clue reveal timing; mission completion; reward distribution; investigation outcomes.
- **What kernel envelope/result must be used:** Command envelope + dependency declaration specifying RT-006 involvement.
- **What remains blocked until that downstream service exists:** Mission/clue/reward resolution.

### Handoff: Social / faction / actor knowledge service (RT-007)

- **What command lifecycle may pass:** Command envelope involving social interaction, faction actions, relationship changes, with dependency declaration for RT-007.
- **What it must not decide:** Social outcomes; faction standing changes; actor knowledge updates; relationship values.
- **What kernel envelope/result must be used:** Command envelope + dependency declaration specifying RT-007 involvement.
- **What remains blocked until that downstream service exists:** Social/faction/relationship resolution.

### Handoff: Generated-content provenance service (RT-008)

- **What command lifecycle may pass:** Notification that a command may produce generated content requiring provenance tracking.
- **What it must not decide:** Content generation; provenance records; recurrence rules; durability.
- **What kernel envelope/result must be used:** Command envelope + dependency declaration specifying RT-008 involvement.
- **What remains blocked until that downstream service exists:** Generated-content durability; provenance tracking.

### Handoff: Context-packet compiler

- **What command lifecycle may pass:** Nothing directly. Context-packet compilation is a separate concern that consumes command lifecycle results.
- **What it must not decide:** Context-packet contents; what the narrator sees; prompt construction.
- **What kernel envelope/result must be used:** N/A (command lifecycle does not call the context-packet compiler).
- **What remains blocked until that downstream service exists:** Narrator-facing command result presentation.

### Handoff: Model evaluation harness

- **What command lifecycle may pass:** Nothing directly. The model evaluation harness consumes context packets, not command lifecycle results.
- **What it must not decide:** Model selection; prompt construction; structured output parsing; model evaluation criteria.
- **What kernel envelope/result must be used:** N/A (command lifecycle does not call the model evaluation harness).
- **What remains blocked until that downstream service exists:** Narrator interpretation of command results.

### Handoff: Live-play adapter gate

- **What command lifecycle may pass:** Nothing directly. The live-play adapter is the integration boundary between the backend runtime and the player-facing interface.
- **What it must not decide:** Session management; player input parsing; output formatting; connection lifecycle.
- **What kernel envelope/result must be used:** N/A (command lifecycle does not call the live-play adapter).
- **What remains blocked until that downstream service exists:** End-to-end player command flow.

---

## 10. Future implementation architecture

The following defines the future implementation shape for the command lifecycle and action legality service. This is planning only. No code is created by this document.

### Suggested future modules (for later implementation PR only)

| Module | Path | Purpose |
|---|---|---|
| domain package init | src/astra_runtime/domain/__init__.py | Domain service package marker |
| command lifecycle | src/astra_runtime/domain/command_lifecycle.py | Command lifecycle state machine and service |
| action legality | src/astra_runtime/domain/action_legality.py | Action legality evaluation and decision production |

### Suggested public API (planning only)

| Symbol | Type | Purpose |
|---|---|---|
| CommandLifecycleStage | Enum (future) | Enumeration of lifecycle states defined in section 6 |
| ActionLegalityDecision | Enum (future) | Enumeration of legality decision categories defined in section 7 |
| CommandLifecycleResult | Dataclass (future) | Result of command lifecycle evaluation |
| ActionLegalityResult | Dataclass (future) | Result of action legality evaluation |
| CommandLifecycleService | Class (future) | Service coordinating command lifecycle state transitions |
| ActionLegalityService | Class (future) | Service evaluating action legality |
| evaluate_command_lifecycle | Function (future) | Top-level function accepting a command envelope and returning a lifecycle result |
| evaluate_action_legality | Function (future) | Top-level function accepting a command envelope and returning a legality result |

**These are proposed future symbols only and must not be created in PR-1.**

---

## 11. Future data shapes

The following defines future data shape requirements for the command lifecycle and action legality service. This is planning only. No dataclasses or schemas are created by this document.

### Command lifecycle result

- **Required fields:** result_id, command_id, final_stage, legality_decision, dependency_declarations, validation_result, trace_entries, metadata.
- **Relation to kernel command envelope:** References the source command_id from the envelope. Does not modify the envelope.
- **Relation to validation result:** Contains or references a ValidationResult from the validation_pipeline.
- **Relation to transaction preview:** May reference a transaction preview if one was created during the preview_requested stage.
- **Relation to runtime trace:** Contains or references trace entries for each lifecycle state transition.
- **Hidden-info safety requirements:** Player-visible portions of the result must not contain hidden-state details. Backend-only trace entries may contain full detail.

### Action legality result

- **Required fields:** result_id, command_id, decision_category, block_reasons (if any), player_visible_message, hidden_info_safe (boolean), validation_issues, trace_id, metadata.
- **Relation to kernel command envelope:** References the source command_id. Does not modify the envelope.
- **Relation to validation result:** Produces or references ValidationIssue records for non-legal decisions.
- **Relation to transaction preview:** Legality result is required before any transaction preview can be created.
- **Relation to runtime trace:** Produces a trace entry for the legality decision.
- **Hidden-info safety requirements:** The player_visible_message field must be verified as hidden-info-safe. The block_reasons field may contain backend-only detail not shown to the player.

### Dependency declaration

- **Required fields:** command_id, required_service_owner (RT track identifier), dependency_type (e.g., cost_precheck, combat_resolution, ability_resolution), required_before (execution or preview), metadata.
- **Relation to kernel command envelope:** References the source command_id.
- **Relation to validation result:** N/A (dependency declarations are not validation issues).
- **Relation to transaction preview:** Dependency declarations are included in or referenced by the transaction preview.
- **Relation to runtime trace:** Produces a trace entry declaring the dependency.
- **Hidden-info safety requirements:** Dependency declarations are backend-internal and not player-visible.

### Legality block reason

- **Required fields:** reason_code, reason_category (matching legality decision categories), detail (backend-only), player_visible_summary, hidden_info_safe (boolean), source_stage, metadata.
- **Relation to kernel command envelope:** References the command_id being blocked.
- **Relation to validation result:** Produces a corresponding ValidationIssue.
- **Relation to transaction preview:** N/A (blocked commands do not get previews).
- **Relation to runtime trace:** Produces a trace entry for the block.
- **Hidden-info safety requirements:** The player_visible_summary must be verified as hidden-info-safe. The detail field is backend-only.

### Confirmation requirement

- **Required fields:** confirmation_id, command_id, reason (why confirmation is needed), player_visible_prompt, confirmation_type (e.g., irreversible_action, high_cost, ambiguous_intent), expires_after (optional), metadata.
- **Relation to kernel command envelope:** References the source command_id.
- **Relation to validation result:** N/A (confirmation is not a validation issue).
- **Relation to transaction preview:** Confirmation may be required before or after preview creation.
- **Relation to runtime trace:** Produces trace entries for confirmation requested and confirmation received/expired.
- **Hidden-info safety requirements:** The player_visible_prompt must not reveal hidden state.

### Quarantine result

- **Required fields:** quarantine_id, command_id, quarantine_reason, quarantine_category (e.g., unsupported_command_type, ambiguous_intent, missing_schema), player_visible_message, validation_issues, metadata.
- **Relation to kernel command envelope:** References the source command_id.
- **Relation to validation result:** Produces ValidationIssue records explaining the quarantine.
- **Relation to transaction preview:** N/A (quarantined commands do not get previews).
- **Relation to runtime trace:** Produces a trace entry for the quarantine.
- **Hidden-info safety requirements:** The player_visible_message must be hidden-info-safe.

---

## 12. Implementation PR authorization boundary

### What this plan authorizes

If this plan (RUNTIME-DOMAIN-PR-1) is accepted after review, the next allowed step is:

**RUNTIME-DOMAIN-PR-1A: Command Lifecycle and Action Legality Skeleton Implementation**

### What RUNTIME-DOMAIN-PR-1A may create

- `src/astra_runtime/domain/__init__.py` (domain package marker).
- `src/astra_runtime/domain/command_lifecycle.py` (skeleton command lifecycle service).
- `src/astra_runtime/domain/action_legality.py` (skeleton action legality service).
- Focused tests for lifecycle/legality skeleton.
- Registry and decision log updates.

### What RUNTIME-DOMAIN-PR-1A must remain

Skeleton-only. It must not:

- Execute commands.
- Mutate state.
- Commit events.
- Compute resource costs.
- Perform combat resolution.
- Resolve abilities or effects.
- Mutate inventory.
- Mutate mission or social state.
- Persist data.
- Call models.
- Compile context packets.
- Run live play.

---

## 13. Test requirements for future implementation

The following test families must be created by the future implementation PR (RUNTIME-DOMAIN-PR-1A). This is a planning-only list.

### Test families

1. **Import/export integrity tests:** Verify that `command_lifecycle` and `action_legality` modules import cleanly and export expected symbols.
2. **Command envelope accepted/rejected tests:** Verify that valid command envelopes are accepted and invalid ones are rejected with appropriate legality decisions.
3. **Invalid envelope quarantine tests:** Verify that envelopes with unrecognizable command types or missing critical fields are quarantined rather than silently accepted.
4. **Actor record ID validation tests:** Verify that envelopes with invalid or missing actor record IDs produce `blocked_by_missing_actor` decisions.
5. **Lifecycle state transition tests:** Verify that commands transition through lifecycle states in the defined order and that illegal transitions are prevented.
6. **Legality decision category tests:** Verify that each legality decision category can be produced and contains required fields.
7. **Hidden-info-safe rejection tests:** Verify that rejection reasons and player-visible messages do not contain hidden-state information.
8. **Validation result integration tests:** Verify that legality checks produce proper ValidationResult and ValidationIssue records via the kernel validation_pipeline.
9. **Transaction preview handoff tests:** Verify that accepted commands produce valid transaction preview records for handoff.
10. **No state mutation guardrail tests:** Verify that the command lifecycle service does not create state deltas or mutate state.
11. **No event commitment guardrail tests:** Verify that the command lifecycle service does not commit events to the event ledger.
12. **No RNG bypass guardrail tests:** Verify that the command lifecycle service does not invoke the RNG interface for domain rolling (dependency declarations only).
13. **No model call guardrail tests:** Verify that the command lifecycle service does not call any model or construct any prompt.
14. **Runtime trace declaration tests:** Verify that lifecycle state transitions and legality decisions produce runtime trace entries.
15. **Downstream dependency declaration tests:** Verify that commands produce correct dependency declarations identifying required downstream services.
16. **Adversarial command tests:** Verify that malformed, excessively large, injection-attempt, or nonsensical commands are safely rejected or quarantined.
17. **Corpus-scale donor command vocabulary tests:** Verify that the command type classification handles representative command types from diverse donor systems without silent misclassification.

---

## 14. Corpus-scale command pressure review

Because Astra must absorb 200–400 donor sources with diverse action economies, the command lifecycle and action legality service must handle command pressure from all major donor families. The following review covers representative command categories and the service's planned response.

### Attack / action / maneuver commands

- **Examples:** "attack with sword," "full attack," "power attack," "charge," "grapple," "trip," "disarm," "called shot," "burst fire," "suppressive fire."
- **Service response:** Routes to future combat/hazard service (RT-003) via dependency declaration. Command lifecycle classifies as combat-type, validates envelope, checks actor/target validity, declares RT-003 dependency. Does not resolve combat.

### Spell / power / technique / ability commands

- **Examples:** "cast fireball," "use telekinesis," "activate implant," "channel energy," "manifest power," "invoke technique."
- **Service response:** Routes to future ability/effect service (RT-004) via dependency declaration. Also declares RT-002 dependency for cost. Does not resolve ability effects.

### Inventory / equipment / use-item commands

- **Examples:** "equip sword," "drink potion," "drop item," "trade item," "reload weapon," "activate gadget."
- **Service response:** Routes to future inventory service (RT-010) via dependency declaration. Does not mutate inventory.

### Movement / exploration / travel commands

- **Examples:** "move north," "climb wall," "swim across river," "teleport," "fly," "explore room," "travel to city."
- **Service response:** Command lifecycle validates envelope. Routes scope/range checks to relevant domain services. Movement commands may require state projection (location awareness) which is blocked until state service exists.

### Social / faction / relationship commands

- **Examples:** "persuade guard," "intimidate merchant," "negotiate treaty," "declare allegiance," "betray faction."
- **Service response:** Routes to future social/faction service (RT-007) via dependency declaration. Does not resolve social outcomes.

### Investigation / clue / mission commands

- **Examples:** "search room," "examine clue," "interrogate suspect," "accept quest," "complete objective," "report findings."
- **Service response:** Routes to future mission/clue service (RT-006) via dependency declaration. Does not reveal clues or advance missions.

### Crafting / salvage / requisition commands

- **Examples:** "craft weapon," "salvage parts," "requisition supplies," "repair equipment," "brew potion."
- **Service response:** Routes to future inventory service (RT-010) and resource service (RT-002) via dependency declarations. Does not perform crafting.

### Vehicle / ship / mech / platform commands

- **Examples:** "pilot vehicle," "fire ship weapons," "deploy mech," "board platform," "repair hull."
- **Service response:** Routes to future inventory/vehicle service (RT-010) and possibly RT-003 for combat. Does not resolve vehicle behavior.

### Companion / summon commands

- **Examples:** "command companion," "summon creature," "dismiss familiar," "direct pet to attack."
- **Service response:** Routes to RT-004 (ability) and possibly RT-003 (combat) via dependency declarations. Validates actor has authority over companion record ID.

### Downtime / domain / campaign commands

- **Examples:** "train skill," "build stronghold," "research spell," "manage domain," "rest for a week."
- **Service response:** Routes to relevant domain services. Many downtime commands require resource cost (RT-002) and time/state changes (future state service). Declares dependencies; does not execute.

### Meta-actions and illegal commands

- **Examples:** "undo last action," "save game," "reload save," "cheat," "skip combat," "god mode," "give me all items."
- **Service response:** Rejects with `illegal` or `unsupported_command_type`. Meta-actions that violate backend-first principles are rejected. Game-system-level commands (if any are supported) are classified separately from in-world commands.

### Ambiguous natural language commands

- **Examples:** "I want to do something cool," "attack everything," "be sneaky," "use my best ability," "figure it out."
- **Service response:** Quarantines with `quarantined_for_validation` or returns `requires_more_information`. Ambiguous commands are not over-normalized into specific actions. The service requests clarification rather than guessing intent.

### Commands that try to reveal hidden information

- **Examples:** "what is the GM planning," "reveal all traps," "show me the secret door," "read the GM notes," "what does the NPC really think."
- **Service response:** Rejects with `blocked_by_hidden_information`. Rejection message does not confirm or deny the existence of hidden information. Uses generic "that action is not available" or similar.

### Commands that try to bypass costs

- **Examples:** "cast fireball for free," "attack without spending action," "use item without consuming it," "teleport without mana cost."
- **Service response:** If the command envelope includes cost-bypass claims, legality precheck flags as `blocked_by_resource_precheck` or `illegal`. Cost authority belongs to RT-002; command lifecycle does not negotiate costs.

### Commands that rely on donor-specific action economies

- **Examples:** "use swift action" (Pathfinder-specific), "spend fate point" (Fate-specific), "use reaction" (D&D 5e-specific), "spend momentum" (2d20-specific), "use edge" (Shadowrun-specific).
- **Service response:** Donor-specific action economy terms must not become Astra baseline law. Command lifecycle normalizes command intent into Astra-native categories. Donor-specific action economy terms are either mapped to Astra equivalents (if one exists) or quarantined for RT-012 review (if the term implies a donor-specific mechanic with no Astra equivalent). Does not silently adopt donor action economy as Astra law.

### Commands with source-local rules not yet canonized

- **Examples:** Commands referencing rules from a specific donor book that have not been canonized into Astra doctrine.
- **Service response:** If the command type or mechanic is recognized as source-local only (not yet promoted to Astra canon), the command is quarantined with a reference to RT-012 (D-series promotion boundary). Source-local rules do not become runtime law by repetition or use. The command lifecycle service does not escalate source-local material to canon status.

---

## 15. Guardrail review

The following items remain blocked. This PR does not authorize or implement any of them.

### LLM non-authority guardrails

- **LLM state ownership:** LLMs do not own game state. The backend owns truth.
- **LLM dice/RNG authority:** LLMs do not roll dice or generate authoritative random results. The backend RNG interface (RT-009) owns randomness.
- **LLM event commitment:** LLMs do not commit events. The backend event ledger owns event commitment.
- **LLM memory authority:** LLM summaries and conversation history are not memory authority. The backend state store owns memory.
- **Narration as state:** Narration text is downstream of state, not its source. Prose does not create game facts.
- **Summaries as memory authority:** LLM-generated summaries are convenience artifacts, not authoritative records.
- **Hidden information exposure:** LLMs must not be given hidden information that the current player/actor should not see.
- **Command execution by model output:** Model output does not execute commands. The backend command lifecycle owns command execution authorization.
- **Command legality decided by model output:** Model output does not determine whether a command is legal. The backend action legality service owns legality decisions.

### State and event guardrails

- **State mutation without event path:** State may not be mutated except through the event commitment path.
- **Event commitment without validation:** Events may not be committed without passing validation.

### Donor and canon guardrails

- **Donor action economy becoming Astra baseline:** Donor-specific action economies (swift actions, bonus actions, fate points, momentum, edge) must not silently become Astra law.
- **Source-local rules becoming canon:** Source-local rules do not become canon by repetition, use in examples, or use in generated content.
- **Converted content becoming canon:** Converted donor content is evidence and pressure, not canon.

### Implementation guardrails (blocked by this PR)

- **Direct domain implementation in this PR:** This PR creates no domain-service code.
- **Live-play adapter:** No live-play adapter exists or is authorized.
- **Context-packet compiler:** No context-packet compiler exists or is authorized.
- **Model integration:** No model integration exists or is authorized.
- **Prompt templates:** No prompt templates exist or are authorized.
- **Training:** No training data or training policy is authorized.
- **Pilot conversion:** No pilot conversion execution is authorized.
- **Sourcebook inclusion:** No sourcebook inclusion is authorized.
- **Canon promotion:** No canon promotion is authorized.

---

## 16. Risk review

### Risk 1: Command lifecycle becomes command execution

- **Description:** The command lifecycle service expands beyond classification/validation/routing and begins executing commands directly.
- **Affected RT owner(s):** RT-001, future transaction lifecycle service.
- **Mitigation:** Strict separation between lifecycle evaluation and transaction execution. Lifecycle produces results; a separate service executes.
- **Future test family:** No state mutation guardrail tests; no event commitment guardrail tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Yes. Skeleton must enforce no-execution boundary.

### Risk 2: Action legality becomes domain rule engine too early

- **Description:** The action legality service begins encoding domain-specific rules (combat rules, spell rules, crafting rules) instead of routing to domain services.
- **Affected RT owner(s):** RT-001, RT-003, RT-004, RT-010.
- **Mitigation:** Action legality performs only non-domain prechecks (envelope validity, actor existence, target validity, timing, scope). Domain-specific rules belong to domain services.
- **Future test family:** Legality decision category tests; downstream dependency declaration tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Yes. Skeleton must not contain domain-specific rules.

### Risk 3: Hidden information leaks through rejection reasons

- **Description:** Rejection reasons or player-visible messages inadvertently reveal hidden state (e.g., "you can't attack the invisible NPC" reveals the NPC exists and is invisible).
- **Affected RT owner(s):** RT-001, RT-005.
- **Mitigation:** All player-visible rejection messages must be verified as hidden-info-safe. Generic messages ("that action is not available") used when specific reasons would leak hidden state.
- **Future test family:** Hidden-info-safe rejection tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Yes. Skeleton must include hidden-info safety checks.

### Risk 4: Resource/cost math gets embedded before RT-002 implementation

- **Description:** The command lifecycle service begins calculating resource costs or verifying resource availability instead of declaring a dependency on RT-002.
- **Affected RT owner(s):** RT-001, RT-002.
- **Mitigation:** Command lifecycle may only declare a resource dependency. It does not calculate costs, read resource pools, or determine affordability.
- **Future test family:** Downstream dependency declaration tests; no state mutation guardrail tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Yes. Skeleton must not contain cost calculation logic.

### Risk 5: Combat assumptions leak into generic action legality

- **Description:** The action legality service hardcodes combat-specific assumptions (initiative order, action economy, range calculations) into the generic legality pipeline.
- **Affected RT owner(s):** RT-001, RT-003.
- **Mitigation:** Combat-specific legality is delegated to RT-003 via dependency declaration. Generic legality handles only envelope/actor/target/timing/scope.
- **Future test family:** Legality decision category tests; downstream dependency declaration tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Yes. Skeleton must route combat commands to RT-003 dependency.

### Risk 6: Donor action economies become default Astra law

- **Description:** Donor-specific action economy terms (swift actions, bonus actions, reactions, fate points, momentum) are accepted as valid Astra command types without explicit canonization.
- **Affected RT owner(s):** RT-001, RT-012.
- **Mitigation:** Donor-specific action economy terms are either mapped to Astra equivalents or quarantined for RT-012 review. No silent adoption.
- **Future test family:** Corpus-scale donor command vocabulary tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Partially. Skeleton must not hardcode donor action economies.

### Risk 7: LLM becomes de facto command parser/authority

- **Description:** The command lifecycle service relies on LLM output to classify, parse, or determine the legality of commands, making the LLM the de facto game engine.
- **Affected RT owner(s):** RT-001, all RT owners.
- **Mitigation:** Command lifecycle operates on backend-owned command envelopes, not raw natural language. Any future NLP parsing layer must be separate and its output must be validated by the backend.
- **Future test family:** No model call guardrail tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Yes. Skeleton must not call any model.

### Risk 8: Transaction preview gets treated as event commitment

- **Description:** A transaction preview (which is read-only and speculative) is treated as if it committed state changes or events.
- **Affected RT owner(s):** RT-001, future transaction lifecycle service.
- **Mitigation:** Transaction preview is explicitly read-only. The command lifecycle service creates previews but does not commit them. Commitment requires the future transaction lifecycle service.
- **Future test family:** Transaction preview handoff tests; no event commitment guardrail tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Yes. Skeleton must treat previews as read-only.

### Risk 9: Validation becomes decorative

- **Description:** Validation checks are present but their results are ignored, making validation decorative rather than enforcement.
- **Affected RT owner(s):** RT-001, RT-011.
- **Mitigation:** Validation results must determine lifecycle outcomes. Failed validation must produce rejection or quarantine, not silent continuation.
- **Future test family:** Validation result integration tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Yes. Skeleton must enforce validation results.

### Risk 10: State is mutated during legality checks

- **Description:** The legality evaluation process inadvertently mutates game state (e.g., by consuming resources during a precheck, by creating actors, by modifying records).
- **Affected RT owner(s):** RT-001, future state service.
- **Mitigation:** Legality checks are read-only. No state deltas, no event commitments, no record mutations during legality evaluation.
- **Future test family:** No state mutation guardrail tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Yes. Skeleton must be provably read-only.

### Risk 11: Future live-play loop bypasses backend command lifecycle

- **Description:** A future live-play adapter directly processes player input into game actions without routing through the backend command lifecycle.
- **Affected RT owner(s):** RT-001, future live-play adapter.
- **Mitigation:** The live-play adapter must route all commands through the command lifecycle service. No direct action execution.
- **Future test family:** N/A for PR-1A (live-play does not exist). Documented for future live-play PR.
- **RUNTIME-DOMAIN-PR-1A must address:** No (live-play does not exist). Risk is documented for future reference.

### Risk 12: Ambiguous commands get over-normalized instead of quarantined

- **Description:** Ambiguous player commands are aggressively normalized into specific actions rather than quarantined for clarification, leading to the system guessing player intent incorrectly.
- **Affected RT owner(s):** RT-001.
- **Mitigation:** Ambiguous commands should produce `requires_more_information` or `quarantined_for_validation` decisions rather than being silently normalized.
- **Future test family:** Adversarial command tests; corpus-scale donor command vocabulary tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Partially. Skeleton should support quarantine and requires_more_information decisions.

### Risk 13: Unsupported donor commands get fake Astra certainty

- **Description:** Commands from donor systems that have no Astra equivalent are classified with artificial certainty (e.g., assigning them to the nearest Astra category) rather than being honestly quarantined.
- **Affected RT owner(s):** RT-001, RT-012.
- **Mitigation:** Unsupported command types produce `unsupported_command_type` decisions. Honest quarantine is preferred over fake classification.
- **Future test family:** Corpus-scale donor command vocabulary tests.
- **RUNTIME-DOMAIN-PR-1A must address:** Partially. Skeleton should support unsupported_command_type decision.

---

## 17. Non-implementation reaffirmation

This PR adds no:

- runtime code;
- domain-service code;
- command lifecycle implementation;
- action legality engine;
- command execution;
- command parser;
- state store;
- state mutation;
- transaction lifecycle;
- event commitment;
- durable persistence;
- database schema;
- replay engine;
- context-packet compiler;
- prompt templates;
- model integration;
- live-play adapter;
- UI/client;
- generator implementation;
- training data;
- donor-content audit;
- pilot conversion authorization;
- sourcebook inclusion authorization;
- canon promotion.

---

## 18. Gate finding

```yaml
gate_finding:
  command_lifecycle_action_legality_plan_defined: true
  ready_for_command_lifecycle_skeleton_implementation_pr: true
  command_lifecycle_code_authorized_by_this_pr: false
  action_legality_engine_authorized_by_this_pr: false
  command_execution_authorized_by_this_pr: false
  state_store_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  resource_math_authorized_by_this_pr: false
  combat_resolution_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-1A command lifecycle and action legality skeleton implementation
  next_step_status: narrow_skeleton_implementation_pending_review
```

---

## 19. Classification block

```yaml
runtime_domain_pr_1:
  review_id: RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001
  artifact_type: command_lifecycle_action_legality_service_plan
  implementation_status: non_executable_plan
  derives_from:
    - RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001
    - RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001
    - RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
    - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
    - RT-001
    - RT-011
  defines_service_ownership: true
  defines_command_lifecycle_state_model: true
  defines_action_legality_decision_model: true
  defines_kernel_interface_consumption_plan: true
  defines_handoff_boundaries: true
  defines_future_implementation_architecture: true
  defines_future_data_shapes: true
  defines_future_test_requirements: true
  defines_corpus_scale_command_pressure_review: true
  authorizes_command_lifecycle_code_by_this_pr: false
  authorizes_action_legality_engine_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_command_parser_by_this_pr: false
  authorizes_state_store_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_transaction_lifecycle_by_this_pr: false
  authorizes_event_commitment_by_this_pr: false
  authorizes_resource_math_by_this_pr: false
  authorizes_combat_resolution_by_this_pr: false
  authorizes_ability_resolution_by_this_pr: false
  authorizes_inventory_mutation_by_this_pr: false
  authorizes_mission_mutation_by_this_pr: false
  authorizes_social_faction_mutation_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_prompt_templates_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-1A command lifecycle and action legality skeleton implementation, pending review
```

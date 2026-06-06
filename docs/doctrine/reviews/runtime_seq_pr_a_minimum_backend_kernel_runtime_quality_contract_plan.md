# RUNTIME-SEQ-PR-A: Minimum Backend Kernel + Runtime Quality Contract Plan

---

## 1. Purpose and status

This document is **RUNTIME-SEQ-PR-A**, a minimum backend kernel plus runtime-quality contract plan.

- **Review ID:** RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001
- **Artifact type:** minimum_backend_kernel_runtime_quality_contract_plan
- **Implementation status:** non_executable_planning
- **Date:** 2026-06-06
- **Derives from:** RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001

This is a **planning-only** and **non-executable** document.

It does not implement:

- runtime code
- schema implementation
- command IR implementation
- validator implementation
- generator implementation
- state store
- state delta model
- event ledger
- deterministic RNG service
- table/oracle service
- persistence writer
- retrieval index
- context-packet compiler
- redaction algorithm
- hidden-state database
- domain runtime service
- campaign memory system
- live-play prompt
- training data
- donor-content audit
- pilot conversion authorization
- sourcebook inclusion authorization
- canon promotion

---

## 2. Source ledger

The following source artifacts were consulted during preparation of this plan:

| Artifact ID | File | Present |
|---|---|---|
| RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001 | `docs/doctrine/reviews/runtime_schema_implementation_sequencing_review.md` | Yes |
| AUDIT-001 | `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md` | Yes |
| AUDIT-WAVE1-001 | `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md` | Yes |
| AUDIT-WAVE2-001 | `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md` | Yes |
| REMEDIATION-PRIORITY-LEDGER-001 | `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` | Yes |
| REMEDIATION-STAGE2-COMPLETION-REVIEW-CLOSURE-LEDGER-001 | `docs/doctrine/reviews/runtime_boundary_generator_ownership_stage2_completion_review_and_closure_ledger.md` | Yes |
| RT-001 owner specification | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md` | Yes |
| RT-002 owner specification | `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md` | Yes |
| RT-003 owner specification | `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md` | Yes |
| RT-004 owner specification | `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md` | Yes |
| RT-005 owner specification | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md` | Yes |
| RT-006 owner specification | `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md` | Yes |
| RT-007 owner specification | `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md` | Yes |
| RT-008 owner specification | `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md` | Yes |
| RT-009 owner specification | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md` | Yes |
| RT-010 owner specification | `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md` | Yes |
| RT-011 owner specification | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md` | Yes |
| RT-012 owner specification | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md` | Yes |
| SM00 | `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` | Yes |
| SM01 | `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md` | Yes |
| SM02 | `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md` | Yes |
| C00 | `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` | Yes |
| C01 | `docs/doctrine/schema/C01_creature_npc_record_schema.md` | Yes |
| C02 | `docs/doctrine/schema/C02_item_gear_record_schema.md` | Yes |
| C03 | `docs/doctrine/schema/C03_ability_power_technique_record_schema.md` | Yes |
| C04 | `docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md` | Yes |
| C05 | `docs/doctrine/schema/C05_faction_institution_record_schema.md` | Yes |
| C06 | `docs/doctrine/schema/C06_location_site_region_record_schema.md` | Yes |
| C07 | `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md` | Yes |
| C08 | `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md` | Yes |
| C09 | `docs/doctrine/schema/C09_hazard_environment_record_schema.md` | Yes |
| C10 | `docs/doctrine/schema/C10_table_oracle_record_schema.md` | Yes |
| C11 | `docs/doctrine/schema/C11_companion_summon_record_schema.md` | Yes |
| C12 | `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md` | Yes |
| C13 | `docs/doctrine/schema/C13_map_diagram_record_schema.md` | Yes |
| C14 | `docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md` | Yes |
| ROADMAP-001 | `docs/doctrine/astra_doctrine_roadmap_v0_1.md` | Yes |
| REGISTRY-001 | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` | Yes |
| Decision log | `docs/decisions/current_decisions_log.md` | Yes |
| README | `README.md` | Yes |

---

## 3. Backend-first invariant

**Astra Ascension must be model-interchangeable.** The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

Astra is not an LLM GM with tools. Astra is a backend-owned TTRPG runtime with an interchangeable narration model. The LLM proposes; the backend validates and commits.

The minimum backend kernel must be designed so that any local or cloud model can be swapped without changing:

- game truth
- committed state
- hidden information
- dice/RNG outcomes
- persistence
- validation results
- event logs
- canon/sourcebook boundaries

Model interchangeability is not a nice-to-have. It is a structural invariant. If swapping the narration model changes game truth, the architecture is broken.

---

## 4. Minimum backend kernel spine

The following future artifact families define the planning-level kernel spine. All are marked `future_required_not_implemented`.

### 4.1 SchemaRegistryContract

- **Purpose:** Central registry for all content-record schemas (C00–C14 and future extensions), providing schema lookup, version tracking, and compatibility validation.
- **Primary RT owner:** RT-011 (validation/readiness tooling)
- **Dependency:** None (foundational)
- **Downstream consumer:** All record producers, validators, context-packet compiler, persistence writer
- **LLM allowed interaction:** None. LLM does not read, modify, or query the schema registry.
- **Implementation status:** `future_required_not_implemented`

### 4.2 RecordIdentityContract

- **Purpose:** Stable, unique identity conventions for all durable records (content records, events, state snapshots), ensuring referential integrity across persistence, context projection, and replay.
- **Primary RT owner:** RT-011 (validation/readiness tooling), with handoffs to RT-001 (command lifecycle) and RT-008 (generated-content provenance)
- **Dependency:** SchemaRegistryContract
- **Downstream consumer:** State store, event ledger, context-packet compiler, persistence writer, replay/hash audit
- **LLM allowed interaction:** None. LLM does not allocate, modify, or validate record identities.
- **Implementation status:** `future_required_not_implemented`

### 4.3 CommandIREnvelope

- **Purpose:** Intermediate representation envelope for player/system commands, capturing intent, parameters, targeting, cost references, and validation metadata before lifecycle processing.
- **Primary RT owner:** RT-001 (command lifecycle/action legality)
- **Dependency:** RecordIdentityContract, SchemaRegistryContract
- **Downstream consumer:** CommandLifecycleContract, TransactionPreviewContract, ValidationPipelineInterface
- **LLM allowed interaction:** LLM may propose intent candidates that are translated into CommandIR by the backend. LLM does not construct, validate, or commit CommandIR directly.
- **Implementation status:** `future_required_not_implemented`

### 4.4 CommandLifecycleContract

- **Purpose:** Governs the state machine for command processing: proposed → validated → previewed → accepted → committed (or rejected/quarantined at any stage).
- **Primary RT owner:** RT-001 (command lifecycle/action legality)
- **Dependency:** CommandIREnvelope, ValidationPipelineInterface
- **Downstream consumer:** TransactionPreviewContract, StateDeltaEnvelope, EventLedgerEnvelope
- **LLM allowed interaction:** LLM may receive narration-safe summaries of command outcomes. LLM does not advance command lifecycle states.
- **Implementation status:** `future_required_not_implemented`

### 4.5 TransactionPreviewContract

- **Purpose:** Produces a preview of proposed state deltas for a command candidate without committing changes, enabling validation, cost checking, and player confirmation before commitment.
- **Primary RT owner:** RT-001 (command lifecycle), RT-002 (resource/consequence math)
- **Dependency:** CommandLifecycleContract, StateStoreContract, ValidationPipelineInterface
- **Downstream consumer:** StateDeltaEnvelope (on acceptance), EventLedgerEnvelope, ContextProjectionBoundary (for narration of preview results)
- **LLM allowed interaction:** LLM may receive narration-safe summaries of previewed outcomes. LLM does not generate, approve, or modify transaction previews.
- **Implementation status:** `future_required_not_implemented`

### 4.6 StateStoreContract

- **Purpose:** Canonical source of current game state for all persistent entities (characters, items, locations, factions, missions, etc.), providing read access for validation and context projection and write access only through committed events.
- **Primary RT owner:** RT-001 (command lifecycle), RT-002 (resource/consequence math), RT-010 (inventory/item/vehicle/asset)
- **Dependency:** SchemaRegistryContract, RecordIdentityContract
- **Downstream consumer:** TransactionPreviewContract, StateDeltaEnvelope, ContextProjectionBoundary, PersistenceBoundaryContract
- **LLM allowed interaction:** None. LLM does not read from or write to the state store. LLM receives projected context packets only.
- **Implementation status:** `future_required_not_implemented`

### 4.7 StateDeltaEnvelope

- **Purpose:** Represents a validated, committed change to game state, linking the originating command, the before/after values, and the resulting event reference.
- **Primary RT owner:** RT-001 (command lifecycle), RT-002 (resource/consequence math)
- **Dependency:** StateStoreContract, CommandLifecycleContract, TransactionPreviewContract
- **Downstream consumer:** EventLedgerEnvelope, PersistenceBoundaryContract, ReplayHashAuditContract
- **LLM allowed interaction:** None. LLM does not produce, modify, or inspect state deltas.
- **Implementation status:** `future_required_not_implemented`

### 4.8 EventLedgerEnvelope

- **Purpose:** Append-only event log recording all committed state changes, system events, and audit-relevant occurrences, providing the canonical history for replay, debugging, and observability.
- **Primary RT owner:** RT-001 (command lifecycle), RT-011 (validation/readiness tooling)
- **Dependency:** StateDeltaEnvelope, RecordIdentityContract
- **Downstream consumer:** ReplayHashAuditContract, RuntimeTraceContract, PersistenceBoundaryContract
- **LLM allowed interaction:** None. LLM does not append to, read from, or query the event ledger.
- **Implementation status:** `future_required_not_implemented`

### 4.9 DeterministicRNGInterface

- **Purpose:** Backend-owned random number generation with seed tracking, ensuring all dice rolls, random table lookups, and oracle invocations are reproducible and auditable.
- **Primary RT owner:** RT-009 (runtime RNG/table/oracle)
- **Dependency:** RecordIdentityContract (for seed/invocation references)
- **Downstream consumer:** CommandLifecycleContract (for commands requiring randomness), EventLedgerEnvelope (for recording RNG invocations), ContextProjectionBoundary (for visible result projection)
- **LLM allowed interaction:** None. LLM does not roll dice, generate random numbers, or choose random outcomes. LLM may narrate results that the backend has already determined.
- **Implementation status:** `future_required_not_implemented`

### 4.10 TableOracleInvocationInterface

- **Purpose:** Backend-owned interface for invoking random tables and oracles with validated weight distributions, result-domain constraints, and provenance tracking.
- **Primary RT owner:** RT-009 (runtime RNG/table/oracle)
- **Dependency:** DeterministicRNGInterface, SchemaRegistryContract (for table/oracle record schemas per C10)
- **Downstream consumer:** CommandLifecycleContract, EventLedgerEnvelope, ContextProjectionBoundary
- **LLM allowed interaction:** None. LLM does not invoke tables or oracles. LLM may narrate backend-determined results.
- **Implementation status:** `future_required_not_implemented`

### 4.11 ValidationPipelineInterface

- **Purpose:** Orchestrates validation of commands, state transitions, and records against schemas, business rules, and invariants before commitment.
- **Primary RT owner:** RT-011 (validation/readiness tooling)
- **Dependency:** SchemaRegistryContract, CommandIREnvelope, StateStoreContract
- **Downstream consumer:** CommandLifecycleContract, TransactionPreviewContract
- **LLM allowed interaction:** None. LLM does not validate commands or state transitions. Validation is backend-deterministic.
- **Implementation status:** `future_required_not_implemented`

### 4.12 ContextProjectionBoundary

- **Purpose:** Projects visible, authorized information from the state store into bounded context packets for the narration model, enforcing hidden-information partitions, redaction rules, and token budgets.
- **Primary RT owner:** RT-005 (context-packet/hidden-information)
- **Dependency:** StateStoreContract, HiddenInformationPartitionContract, SchemaRegistryContract
- **Downstream consumer:** NarrationRenderPacketContract (runtime-quality layer), narration model
- **LLM allowed interaction:** LLM receives the projected context packet as its input. LLM does not query the state store directly or request hidden information.
- **Implementation status:** `future_required_not_implemented`

### 4.13 HiddenInformationPartitionContract

- **Purpose:** Defines the partition between visible, hidden, redacted, derived, and reviewer-only information for each actor, faction, and system scope, preventing information leakage into player-visible outputs.
- **Primary RT owner:** RT-005 (context-packet/hidden-information), RT-007 (social/faction/actor-knowledge)
- **Dependency:** StateStoreContract, RecordIdentityContract
- **Downstream consumer:** ContextProjectionBoundary, NarrationRenderPacketContract
- **LLM allowed interaction:** None. LLM does not query, modify, or bypass hidden-information partitions.
- **Implementation status:** `future_required_not_implemented`

### 4.14 PersistenceBoundaryContract

- **Purpose:** Defines the boundary between in-memory runtime state and durable persistence, governing when and how state snapshots, events, and records are written to storage.
- **Primary RT owner:** RT-001 (command lifecycle), RT-011 (validation/readiness tooling)
- **Dependency:** StateStoreContract, EventLedgerEnvelope, StateDeltaEnvelope
- **Downstream consumer:** ReplayHashAuditContract, external storage
- **LLM allowed interaction:** None. LLM does not trigger, observe, or influence persistence operations.
- **Implementation status:** `future_required_not_implemented`

### 4.15 ReplayHashAuditContract

- **Purpose:** Provides hash-chain integrity for the event ledger, enabling deterministic replay verification and tamper detection across sessions.
- **Primary RT owner:** RT-011 (validation/readiness tooling), RT-009 (runtime RNG/table/oracle)
- **Dependency:** EventLedgerEnvelope, DeterministicRNGInterface, PersistenceBoundaryContract
- **Downstream consumer:** RuntimeTraceContract, external audit/debug tooling
- **LLM allowed interaction:** None. LLM does not participate in replay or hash verification.
- **Implementation status:** `future_required_not_implemented`

### 4.16 RuntimeTraceContract

- **Purpose:** Per-turn structured trace capturing command, preview, validation, projection, RNG, narration, and event references for observability and debugging.
- **Primary RT owner:** RT-011 (validation/readiness tooling)
- **Dependency:** All kernel spine contracts (aggregates references from each)
- **Downstream consumer:** External debug/observability tooling, ReplayHashAuditContract
- **LLM allowed interaction:** None. LLM does not produce, modify, or inspect runtime traces.
- **Implementation status:** `future_required_not_implemented`

---

## 5. Runtime-quality contract layer

The following future artifact families define the runtime-quality layer that must shape future implementation. All are marked `future_required_not_implemented`.

### 5.1 NarrationRenderPacketContract

- **Purpose:** Defines the structure and constraints of the packet delivered to the narration model, including visible facts, scene context, actor-visible state, permitted narration scope, and format requirements.
- **Why it matters for local 8B reliability:** A small model cannot reliably extract relevant facts from an unbounded context dump. Bounded, structured packets reduce hallucination risk and keep the model within its reliable operating range.
- **Primary RT owner:** RT-005 (context-packet/hidden-information)
- **Downstream handoff:** Narration model input, NarratorOutputContract (for validating responses against packet scope)
- **Implementation status:** `future_required_not_implemented`

### 5.2 NarratorOutputContract

- **Purpose:** Defines the expected structure, constraints, and validation requirements for narration model output, including permitted content types (narration, intent proposals, clarification questions, summaries) and forbidden content types (state mutations, commitment claims, hidden-fact disclosures).
- **Why it matters for local 8B reliability:** Smaller models are more prone to producing off-schema output, soft-state claims, or hidden-information leaks. A strict output contract enables post-generation validation before display.
- **Primary RT owner:** RT-011 (validation/readiness tooling), RT-005 (context-packet/hidden-information)
- **Downstream handoff:** Display layer, SoftStateMutationDetectionContract, CorrectionEventProtocol
- **Implementation status:** `future_required_not_implemented`

### 5.3 PacketBudgetPolicy

- **Purpose:** Defines token budget constraints for narration render packets, ensuring packets fit within the model's effective context window with margin for output, and prioritizing information when budget is exceeded.
- **Why it matters for local 8B reliability:** Local 8B models have small effective context windows (often 4K–8K usable tokens). Budget enforcement prevents truncation-induced hallucination and ensures the model receives the most important facts first.
- **Primary RT owner:** RT-005 (context-packet/hidden-information)
- **Downstream handoff:** ContextProjectionBoundary, NarrationRenderPacketContract, TruncationSafeStructuredOutputPolicy
- **Implementation status:** `future_required_not_implemented`

### 5.4 SoftStateMutationDetectionContract

- **Purpose:** Defines detection mechanisms for narration output that implies state changes not authorized by the backend (e.g., "you pick up the sword" when no pickup command was committed, or "the door is now locked" without a lock event).
- **Why it matters for local 8B reliability:** Smaller models are more likely to narrate state changes that did not occur. Detection prevents players from experiencing a false game state that diverges from backend truth.
- **Primary RT owner:** RT-001 (command lifecycle), RT-011 (validation/readiness tooling)
- **Downstream handoff:** CorrectionEventProtocol, NarratorOutputContract
- **Implementation status:** `future_required_not_implemented`

### 5.5 CanonicalSilencePolicy

- **Purpose:** Defines the policy that the system must not name or imply facts that are not known, not visible, not generated, not committed, not promoted, backend-only, source-local but not active, or hidden behind investigation, discovery, or future reveal.
- **Why it matters for local 8B reliability:** Small models are prone to confabulating details that feel plausible but are not grounded in committed state. Canonical silence policy provides the constraint framework for detecting and preventing these confabulations.
- **Primary RT owner:** RT-005 (context-packet/hidden-information), RT-008 (generated-content provenance)
- **Downstream handoff:** ContextProjectionBoundary, NarratorOutputContract, WorldInvariantRegistry
- **Implementation status:** `future_required_not_implemented`

### 5.6 WorldInvariantRegistry

- **Purpose:** Registers invariant conditions that the runtime must never violate, providing a checkable set of world-consistency rules for validation, testing, and observability.
- **Why it matters for local 8B reliability:** Invariant violations caused by model confabulation (e.g., dead NPCs acting, hidden facts appearing in narration) must be detectable regardless of which model is running. The registry makes violations machine-checkable rather than requiring human review.
- **Primary RT owner:** RT-011 (validation/readiness tooling)
- **Downstream handoff:** ValidationPipelineInterface, SoftStateMutationDetectionContract, CorrectionEventProtocol
- **Implementation status:** `future_required_not_implemented`

### 5.7 CorrectionEventProtocol

- **Purpose:** Defines how detected errors in narration or state are corrected through append-only correction events rather than silent edits, preserving audit trail integrity.
- **Why it matters for local 8B reliability:** When a small model produces incorrect narration, the correction must be traceable and non-destructive. Silent edits would undermine replay integrity and make debugging impossible.
- **Primary RT owner:** RT-001 (command lifecycle), RT-011 (validation/readiness tooling)
- **Downstream handoff:** EventLedgerEnvelope, RuntimeTraceContract, narration display layer
- **Implementation status:** `future_required_not_implemented`

### 5.8 SessionTraceObservabilityContract

- **Purpose:** Defines the per-session observability requirements for debugging, performance monitoring, and model behavior analysis, including what must be logged, what must be queryable, and what must be human-readable.
- **Why it matters for local 8B reliability:** Debugging a small model's failures requires structured traces that capture exactly what the model received, what it produced, and how the backend evaluated the output. Without this, failures are opaque.
- **Primary RT owner:** RT-011 (validation/readiness tooling)
- **Downstream handoff:** RuntimeTraceContract, external monitoring/debug tooling
- **Implementation status:** `future_required_not_implemented`

### 5.9 AdversarialPlayerCommandCorpus

- **Purpose:** Defines a future corpus of adversarial, edge-case, and ambiguous player commands for testing command interpretation, validation resilience, and model robustness.
- **Why it matters for local 8B reliability:** Small models are more susceptible to adversarial inputs, ambiguous commands, and prompt injection attempts. A structured adversarial corpus enables systematic testing of the command pipeline's resilience.
- **Primary RT owner:** RT-001 (command lifecycle), RT-011 (validation/readiness tooling)
- **Downstream handoff:** ValidationPipelineInterface, MetamorphicRuntimeTestPlan
- **Implementation status:** `future_required_not_implemented`

### 5.10 MetamorphicRuntimeTestPlan

- **Purpose:** Defines metamorphic testing strategies where the same game scenario is run with different models, different RNG seeds, and different command orderings to verify that backend truth remains invariant.
- **Why it matters for local 8B reliability:** If swapping from a cloud model to a local 8B model changes game outcomes (beyond narration style), the architecture has a model-dependence bug. Metamorphic testing detects this systematically.
- **Primary RT owner:** RT-011 (validation/readiness tooling)
- **Downstream handoff:** ModelBehaviorFingerprint, ReplayHashAuditContract
- **Implementation status:** `future_required_not_implemented`

### 5.11 ModelBehaviorFingerprint

- **Purpose:** Defines a qualification process for models before they are assigned runtime roles, testing structured-output compliance, instruction following, forbidden-content avoidance, and context-window behavior.
- **Why it matters for local 8B reliability:** Not all 8B models are equal. A fingerprint process prevents deploying a model that cannot reliably produce structured output, follow canonical silence rules, or avoid soft-state mutations.
- **Primary RT owner:** RT-011 (validation/readiness tooling), future model-evaluation owner
- **Downstream handoff:** PacketBudgetPolicy, TruncationSafeStructuredOutputPolicy, runtime role assignment
- **Implementation status:** `future_required_not_implemented`

### 5.12 TruncationSafeStructuredOutputPolicy

- **Purpose:** Defines requirements for structured output formats that remain parseable and meaningful even if the model's output is truncated, including resumable output protocols and partial-output validation.
- **Why it matters for local 8B reliability:** Small models with limited output windows may truncate mid-response. If structured output (e.g., JSON, tagged narration) is truncated, the backend must detect the truncation and either resume or discard safely rather than parsing corrupted output.
- **Primary RT owner:** RT-011 (validation/readiness tooling)
- **Downstream handoff:** NarratorOutputContract, SchemaKeyBehaviorEvaluationPolicy
- **Implementation status:** `future_required_not_implemented`

### 5.13 SchemaKeyBehaviorEvaluationPolicy

- **Purpose:** Defines evaluation criteria for whether a model can reliably produce outputs that conform to required schema keys, field types, and value constraints, measuring compliance rates and failure modes.
- **Why it matters for local 8B reliability:** Small models may omit required keys, produce wrong types, or hallucinate field names. Schema-key behavior evaluation quantifies these failure modes before the model is trusted in production.
- **Primary RT owner:** RT-011 (validation/readiness tooling)
- **Downstream handoff:** ModelBehaviorFingerprint, NarratorOutputContract
- **Implementation status:** `future_required_not_implemented`

### 5.14 SourceLocalCapsuleBoundary

- **Purpose:** Defines the boundary between source-local retained content and Astra-native content in the runtime context, ensuring source-local material is available for narration reference but cannot become canon, authority, or durable state through repeated use.
- **Why it matters for local 8B reliability:** A small model cannot distinguish between source-local flavor text and Astra-canonical facts without explicit boundary markers. The capsule boundary makes the distinction machine-enforced rather than model-dependent.
- **Primary RT owner:** RT-008 (generated-content provenance), RT-012 (D-series promotion boundary)
- **Downstream handoff:** ContextProjectionBoundary, CanonicalSilencePolicy, HiddenInformationPartitionContract
- **Implementation status:** `future_required_not_implemented`

### 5.15 StoryCapableStructurePrinciple

- **Purpose:** Defines the principle that backend structure must support compelling TTRPG storytelling without the backend itself generating story. The kernel provides the reliable scaffolding (consistent NPCs, persistent consequences, fair randomness, hidden secrets) that makes story possible.
- **Why it matters for local 8B reliability:** A small model produces better narration when the backend provides rich, consistent, well-structured context. Story capability is not a model feature — it is an architecture feature that makes the model's job achievable.
- **Primary RT owner:** Future story/content owner (not yet assigned)
- **Downstream handoff:** NarrationRenderPacketContract, ContextProjectionBoundary, all domain services
- **Implementation status:** `future_required_not_implemented`

---

## 6. Local 8B reliability requirements

The following planning requirements define constraints for making the local 8B model's job smaller, stricter, and more reliable:

1. **Bounded packets only.** The local model receives bounded context packets only, never raw state dumps or unbounded context.

2. **No hidden state in unauthorized packets.** The local model does not receive hidden state unless that state is explicitly visible and authorized for the current actor/scope by the hidden-information partition.

3. **No campaign memory ownership.** The local model does not own campaign memory. Campaign memory is backend-owned state. The model receives projected summaries only.

4. **No dice or random outcomes.** The local model does not roll dice or choose random outcomes. All randomness is backend-owned through the DeterministicRNGInterface.

5. **No event commitment.** The local model does not commit events. Events are committed by the backend through the CommandLifecycleContract and EventLedgerEnvelope.

6. **No durable record creation.** The local model does not create durable records. Record creation is backend-owned through the state store and persistence boundary.

7. **Output validation before display.** The local model's output must be validated before display if it can imply state changes, hidden-fact disclosure, or authority claims. Validation is backend-deterministic.

8. **Permitted output types.** The local model should produce: narration, intent proposals, clarification questions, and summaries of approved context only. All other output types are forbidden or require backend validation.

9. **Truncation safety.** Output must be truncation-safe or resumable where structured output is required. The TruncationSafeStructuredOutputPolicy governs this requirement.

10. **Packet budget before live-play.** The PacketBudgetPolicy must be defined before any live-play adapter examples are created, ensuring the model's context window constraints are respected from the start.

11. **Behavior fingerprinting before role assignment.** ModelBehaviorFingerprint qualification must qualify models before assigning runtime roles, preventing deployment of models that cannot meet structured-output, canonical-silence, or soft-state-detection requirements.

---

## 7. Transaction preview and correction policy

The following planning-level transaction and correction boundaries apply:

1. **Player input becomes intent proposal.** Raw player input is interpreted as an intent proposal, not a command.

2. **Intent proposal becomes command candidate.** The backend translates validated intent proposals into command candidates in CommandIR format.

3. **Command candidate produces transaction preview.** The command candidate is processed through the TransactionPreviewContract, producing a preview of proposed state deltas.

4. **Transaction preview validates without committing.** The transaction preview validates proposed state deltas against invariants, resources, legality rules, and schemas without committing any changes to the state store.

5. **Rejected or quarantined preview mutates no state.** If the preview is rejected or quarantined, no state mutation occurs. The rejection is recorded in the event ledger as a non-mutating event.

6. **Accepted preview becomes committed event only through authorized implementation.** An accepted preview can later become a committed event only through future authorized event/state implementation, not through narration or model output.

7. **Narration is never commitment.** Narration text produced by the model is never a state commitment. Narration is downstream of committed state, not its source.

8. **Correction events are append-only.** Correction events must be append-only future events, not silent edits to existing events or state. The correction event references the original event and records the nature of the correction.

9. **Wrong narration is non-authoritative.** Wrong narration must be marked non-authoritative rather than converted into state. The system must never retroactively validate incorrect narration by mutating state to match it.

This section does not implement transaction logic, rollback logic, event logic, or correction-event schemas.

---

## 8. World invariant and canonical silence requirements

### 8.1 WorldInvariantRegistry requirements

The WorldInvariantRegistry should eventually prevent impossible or authority-breaking states, such as:

- Hidden facts appearing in player-visible packets.
- Items appearing in two inventories simultaneously without an authorized duplication rule.
- Dead or incapacitated actors performing ordinary actions without a resurrection or recovery exception.
- Uncommitted narration becoming event truth.
- Generated content becoming durable without provenance tracking.
- Source-local content becoming canon through repeated use without explicit promotion through RT-012/governance routing.
- D-series/native-design material becoming authority without RT-012/governance routing.

### 8.2 CanonicalSilencePolicy requirements

The CanonicalSilencePolicy should eventually prevent the system from naming or implying facts that are:

- **Not known** — facts not present in the state store or committed events for the current scope.
- **Not visible** — facts that exist but are hidden from the current actor by the hidden-information partition.
- **Not generated** — facts that have not been generated by an authorized generator or committed by an authorized process.
- **Not committed** — facts that exist only in narration, proposals, or previews but have not been committed to the event ledger.
- **Not promoted** — facts that exist in source-local or generated-content capsules but have not been promoted to canon/sourcebook status.
- **Backend-only** — facts that are internal to backend validation, debugging, or system state and are not player-facing.
- **Source-local but not active** — facts from source-local retained constructs that are not currently active in the campaign context.
- **Hidden behind investigation, discovery, or future reveal** — facts that are gated behind future player actions, discovery events, or narrative reveals.

This section does not implement invariant checks or silence filters.

---

## 9. Observability and replay/debug requirements

Future per-turn traces should record the following information:

- **Command candidate** — the CommandIR envelope for the turn's command.
- **Transaction preview** — the preview result including proposed state deltas.
- **Validation result** — pass/fail/quarantine status and any validation messages.
- **Visible facts selected** — the set of facts projected into the narration render packet.
- **Hidden facts withheld** — the count and categories of facts withheld by the hidden-information partition (without revealing the facts themselves in the trace).
- **Packet token estimate** — estimated token count of the narration render packet.
- **RNG/table/oracle invocation references** — references to any DeterministicRNG or table/oracle invocations during the turn.
- **Model role used** — which model (local 8B, cloud, etc.) served the narration role for this turn.
- **Narrator output classification** — classification of the model's output (narration, intent proposal, clarification question, summary, etc.).
- **Rejected soft-state claims** — any soft-state mutation claims detected and rejected in the model's output.
- **Committed event reference** — reference to the committed event in the event ledger, if any.
- **Replay/hash reference** — the replay hash for this turn, enabling deterministic replay verification.

This section does not implement trace logging, hash chains, replay verifier, or debug tooling.

---

## 10. Minimum backend kernel target boundary

### 10.1 What the future minimum backend kernel implementation may eventually include

Once separately authorized, the minimum backend kernel implementation may include:

- Schema registry loading
- Minimal record identity conventions
- Command IR envelope
- Command lifecycle states
- State delta envelope
- Append-only event ledger envelope
- Deterministic RNG interface
- Validation pipeline interface
- Hidden-information partition interface
- Context projection interface
- Persistence boundary interface
- Replay/hash audit interface
- Focused tests for each of the above

### 10.2 What it must not include in the minimum kernel

The minimum backend kernel must not include:

- Full combat system
- Full ability system
- Full mission system
- Full social/faction system
- Full inventory system
- Full generator library
- Full canon/sourcebook workflow
- Live-play adapter
- Training data
- Donor conversion execution
- UI implementation
- Actual campaign content generation

The minimum kernel provides the spine. Domain systems, content, and live-play are built on top of the spine in later waves.

---

## 11. Implementation wave alignment

RUNTIME-SEQ-PR-A is a bridge from RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001 to future implementation planning. It primarily prepares:

- **Wave 0: Implementation readiness normalization.** Ensures all prerequisites (schema registry conventions, record identity conventions, test infrastructure) are defined before kernel implementation begins.

- **Wave 1: Schema registry and shared base contracts.** SchemaRegistryContract and RecordIdentityContract form the foundation for all subsequent contracts.

- **Wave 2: Command IR and command lifecycle skeleton.** CommandIREnvelope and CommandLifecycleContract establish the command processing pipeline.

- **Wave 3: State store, state delta, and event ledger skeleton.** StateStoreContract, StateDeltaEnvelope, and EventLedgerEnvelope provide the state mutation and audit infrastructure.

- **Wave 4: Deterministic RNG/table/oracle service plan.** DeterministicRNGInterface and TableOracleInvocationInterface ensure all randomness is backend-owned and reproducible.

- **Wave 5: Validation/readiness framework.** ValidationPipelineInterface connects schemas, commands, and state transitions into a coherent validation pipeline.

- **Wave 6: Context-packet compiler and hidden-information partitions.** ContextProjectionBoundary and HiddenInformationPartitionContract govern what the narration model sees and what remains hidden.

This plan does not start **Wave 7** (domain services) or any later wave. Domain services, generators, live-play adapters, and training are out of scope for the minimum backend kernel.

---

## 12. Blocked-until ledger

The following remain blocked until future explicit authorization:

| Capability | Blocked until |
|---|---|
| Runtime implementation | Separate implementation-readiness review and authorization |
| Schema implementation | Separate implementation-readiness review and authorization |
| Command IR implementation | Separate implementation-readiness review and authorization |
| Validator implementation | Separate implementation-readiness review and authorization |
| Generator implementation | Separate implementation-readiness review and authorization |
| State store | Separate implementation-readiness review and authorization |
| State delta model | Separate implementation-readiness review and authorization |
| Event ledger | Separate implementation-readiness review and authorization |
| Deterministic RNG service | Separate implementation-readiness review and authorization |
| Table/oracle service | Separate implementation-readiness review and authorization |
| Persistence writer | Separate implementation-readiness review and authorization |
| Context-packet compiler | Separate implementation-readiness review and authorization |
| Redaction algorithm | Separate implementation-readiness review and authorization |
| Domain services | Separate implementation-readiness review and authorization |
| Live-play adapter | Separate implementation-readiness review and authorization |
| Training | Separate training authorization review |
| Pilot conversion | Separate pilot conversion authorization review |
| Sourcebook inclusion | Separate sourcebook inclusion authorization review |
| Canon promotion | Separate canon promotion authorization review |
| UI integration | Separate UI authorization review |

---

## 13. Next recommended planning PRs

The following staged sequence is recommended after RUNTIME-SEQ-PR-A:

1. **RUNTIME-SEQ-PR-B:** Narration/context packet contract plan. Detailed planning for NarrationRenderPacketContract, NarratorOutputContract, PacketBudgetPolicy, and ContextProjectionBoundary interactions.

2. **RUNTIME-SEQ-PR-C:** State/event/invariant/transaction plan. Detailed planning for StateStoreContract, StateDeltaEnvelope, EventLedgerEnvelope, WorldInvariantRegistry, TransactionPreviewContract, and CorrectionEventProtocol interactions.

3. **RUNTIME-SEQ-PR-D:** Story-capable structure and playable-content plan. Detailed planning for StoryCapableStructurePrinciple, SourceLocalCapsuleBoundary, and the relationship between backend structure and narrative quality.

4. **RUNTIME-SEQ-PR-E:** Model evaluation, structured-output, and adversarial-command plan. Detailed planning for ModelBehaviorFingerprint, SchemaKeyBehaviorEvaluationPolicy, TruncationSafeStructuredOutputPolicy, AdversarialPlayerCommandCorpus, and MetamorphicRuntimeTestPlan.

5. **Implementation-readiness review.** A separately authorized implementation-readiness review before any code implementation begins, verifying that all planning PRs are complete and consistent.

RUNTIME-SEQ-PR-A does not authorize these later PRs. It only recommends them as the next steps in the planning sequence.

---

## 14. Non-implementation reaffirmation

This PR adds no:

- runtime code
- schemas
- command IR
- validators
- generators
- state store
- state delta model
- event ledger
- deterministic RNG service
- table/oracle service
- persistence writer
- retrieval index
- context-packet compiler
- redaction algorithm
- hidden-state database
- domain runtime service
- campaign memory system
- live-play prompt
- training data
- donor-content audit
- pilot conversion authorization
- sourcebook inclusion authorization
- canon promotion

All artifact families described in this plan are `future_required_not_implemented`. This document is planning only.

---

## 15. Classification block

```yaml
runtime_seq_pr_a:
  review_id: RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001
  artifact_type: minimum_backend_kernel_runtime_quality_contract_plan
  implementation_status: non_executable_planning
  derives_from:
    - RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001
  confirms_backend_first_invariant: true
  confirms_llm_is_not_game_engine: true
  defines_minimum_kernel_spine: true
  defines_runtime_quality_contract_layer: true
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_command_ir: false
  authorizes_validator_implementation: false
  authorizes_generator_implementation: false
  authorizes_state_store: false
  authorizes_state_delta_model: false
  authorizes_event_ledger: false
  authorizes_rng_service: false
  authorizes_table_oracle_service: false
  authorizes_persistence_writer: false
  authorizes_context_packet_compiler: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-SEQ-PR-B narration/context packet contract plan, pending review
```

# RUNTIME-IMPL-PR-0: Minimum Backend Kernel Executable Implementation Plan

**Review ID:** RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001

---

## 1. Purpose and status

This document is **RUNTIME-IMPL-PR-0**, the minimum backend kernel executable implementation plan.

It is **planning-only and non-executable**.

It prepares the first future runtime implementation sequence, but this PR itself **does not implement**:

- runtime code;
- schema implementation;
- command IR;
- validators;
- generators;
- state store;
- state delta model;
- event ledger;
- transaction system;
- invariant validator;
- correction event schema;
- deterministic RNG service;
- table/oracle service;
- persistence writer;
- database schema;
- context-packet compiler;
- redaction algorithm;
- hidden-state database;
- domain services;
- model evaluation code;
- benchmark runner;
- prompt templates;
- live-play adapter;
- training data;
- donor-content audit;
- pilot conversion;
- sourcebook inclusion;
- canon promotion.

---

## 2. Source ledger

### Core runtime sequencing sources

| Artifact | File | Status |
|---|---|---|
| RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001 | `docs/doctrine/reviews/runtime_schema_implementation_sequencing_review.md` | present |
| RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_a_minimum_backend_kernel_runtime_quality_contract_plan.md` | present |
| RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_b_narration_context_packet_contract_plan.md` | present |
| RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_c_state_event_invariant_transaction_plan.md` | present |
| RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_d_story_capable_structure_playable_content_plan.md` | present |
| RUNTIME-SEQ-PR-E-MODEL-EVALUATION-STRUCTURED-OUTPUT-ADVERSARIAL-COMMAND-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_e_model_evaluation_structured_output_adversarial_command_plan.md` | present |
| RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001 | `docs/doctrine/reviews/runtime_seq_pr_f_implementation_readiness_executable_kernel_authorization_gate.md` | present |

### Runtime boundary and Stage 2 sources

| Artifact | File | Status |
|---|---|---|
| AUDIT-001 | `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md` | present |
| Stage 2 closure ledger | `docs/doctrine/reviews/runtime_boundary_generator_ownership_stage2_completion_review_and_closure_ledger.md` | present |

### RT owner specifications (RT-001 through RT-012)

| Spec | File | Status |
|---|---|---|
| RT-001 | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md` | present |
| RT-002 | `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md` | present |
| RT-003 | `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md` | present |
| RT-004 | `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md` | present |
| RT-005 | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md` | present |
| RT-006 | `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md` | present |
| RT-007 | `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md` | present |
| RT-008 | `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md` | present |
| RT-009 | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md` | present |
| RT-010 | `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md` | present |
| RT-011 | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md` | present |
| RT-012 | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md` | present |

### Content record schemas (C00 through C14)

| Schema | File | Status |
|---|---|---|
| C00 | `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` | present |
| C01 | `docs/doctrine/schema/C01_creature_npc_record_schema.md` | present |
| C02 | `docs/doctrine/schema/C02_item_gear_record_schema.md` | present |
| C03 | `docs/doctrine/schema/C03_ability_power_technique_record_schema.md` | present |
| C04 | `docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md` | present |
| C05 | `docs/doctrine/schema/C05_faction_institution_record_schema.md` | present |
| C06 | `docs/doctrine/schema/C06_location_site_region_record_schema.md` | present |
| C07 | `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md` | present |
| C08 | `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md` | present |
| C09 | `docs/doctrine/schema/C09_hazard_environment_record_schema.md` | present |
| C10 | `docs/doctrine/schema/C10_table_oracle_record_schema.md` | present |
| C11 | `docs/doctrine/schema/C11_companion_summon_record_schema.md` | present |
| C12 | `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md` | present |
| C13 | `docs/doctrine/schema/C13_map_diagram_record_schema.md` | present |
| C14 | `docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md` | present |

### Schema/math/mechanics sources (SM00 through SM02)

| File | Status |
|---|---|
| `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` | present |
| `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md` | present |
| `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md` | present |

### Repo and tooling sources

| File | Status |
|---|---|
| `README.md` | present |
| `requirements-dev.txt` | present (PyYAML>=6.0) |
| `pyproject.toml` | absent |
| `pytest.ini` | absent |
| `setup.cfg` | absent |
| `tox.ini` | absent |
| `requirements.txt` | absent |
| `tests/` | present (pytest-style test files) |
| `docs/doctrine/astra_doctrine_registry_v0_1.yaml` | present |
| `docs/decisions/current_decisions_log.md` | present |

---

## 3. Backend-first invariant

**Astra Ascension must be model-interchangeable.** The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

### Implementation-plan implication

The first executable kernel implementation must begin with backend-owned interfaces and tests before domain services, live-play adapter, model routing, generator libraries, conversion execution, UI runtime integration, sourcebook inclusion, or canon promotion.

No implementation PR may introduce LLM state authority, narration-as-state, summary-as-memory, or model-dependent game logic. The backend kernel skeleton must be testable and operational without any model present.

---

## 4. Implementation stack decision

### Actual repo evidence

| Evidence category | Finding |
|---|---|
| Language | Python. All existing test files use Python/pytest patterns. `requirements-dev.txt` references PyYAML. |
| Test framework | pytest. Tests directory contains `conftest.py`, `helpers.py`, and `test_*.py` files following pytest conventions. |
| Dependency files | `requirements-dev.txt` present (PyYAML>=6.0). No `pyproject.toml`, `setup.cfg`, `tox.ini`, or `requirements.txt`. |
| Runtime package | No `src/astra_runtime/` or any runtime package exists. |
| Doctrine/test-only status | The repo is currently doctrine/planning/validation-test only. No executable runtime code exists. |
| Persistence/database | No database decision exists. No SQLite, PostgreSQL, or other persistence artifacts present. |
| UI/client decision | No UI framework, web server, or client-side code present. |

### Plan-level stack recommendation

- **Python** as the initial minimum backend kernel implementation language, because the repo already uses Python tests and doctrine validation tooling.
- **pytest** as the initial test harness, because tests already use pytest-style files and `conftest.py`.
- **No database** in the first implementation PR. Begin with storage-neutral interfaces and in-memory fixtures for the first skeleton.
- **Defer SQLite/file-backed persistence** until persistence boundary interfaces and event ledger envelope are defined (RUNTIME-IMPL-PR-7).
- **No web server, UI client, game engine, Ollama integration, or model adapter** in the kernel skeleton.
- A `pyproject.toml` may be introduced in RUNTIME-IMPL-PR-1 to define the package, but this is a stack recommendation only.

This is a planning recommendation only. This PR does not create pyproject.toml, package files, runtime modules, database files, or configuration changes.

---

## 5. Minimum backend kernel implementation target

The future minimum backend kernel target is a small executable skeleton, not domain runtime.

### Future target includes

- Schema registry loader skeleton;
- Record identity convention skeleton;
- Command envelope skeleton;
- Transaction preview envelope skeleton;
- State delta envelope skeleton;
- Append-only event ledger envelope skeleton;
- Deterministic RNG/table interface skeleton;
- Validation pipeline interface skeleton;
- Hidden-information partition interface skeleton;
- Context projection boundary skeleton;
- Persistence boundary interface skeleton;
- Replay/hash audit boundary skeleton;
- Runtime trace boundary skeleton;
- Focused tests for each skeleton component.

### Future target must not include

- Full combat system;
- Full ability/effect system;
- Full mission system;
- Full social/faction system;
- Full inventory/asset system;
- Full generator library;
- Storylet system;
- Quest/scenario engine;
- Dialogue system;
- Model evaluation runner;
- Model routing;
- Live-play adapter;
- UI implementation;
- Training data;
- Conversion execution;
- Canon/sourcebook workflow.

---

## 6. Proposed package/module layout

The following layout is recommended for future code paths. These paths are **proposed for RUNTIME-IMPL-PR-1 and later**, not created in this PR.

```
src/astra_runtime/
    __init__.py
    kernel/
        __init__.py
        schema_registry.py
        record_identity.py
        command_envelope.py
        transaction_preview.py
        state_delta.py
        event_ledger.py
        rng_interface.py
        validation_pipeline.py
        hidden_information.py
        context_projection.py
        persistence_boundary.py
        replay_audit.py
        runtime_trace.py

tests/runtime/
    __init__.py
    test_schema_registry_skeleton.py
    test_record_identity_skeleton.py
    test_command_envelope_skeleton.py
    test_transaction_preview_skeleton.py
    test_state_delta_skeleton.py
    test_event_ledger_skeleton.py
    test_rng_interface_skeleton.py
    test_validation_pipeline_skeleton.py
    test_hidden_information_skeleton.py
    test_context_projection_skeleton.py
    test_persistence_boundary_skeleton.py
    test_replay_audit_skeleton.py
    test_runtime_trace_skeleton.py
```

---

## 7. Interface boundary plan

### 7.1 SchemaRegistryInterface

- **Purpose:** Load, index, and retrieve content record schema definitions by type and version.
- **Primary RT owner:** RT-011 (validation/readiness/tooling).
- **Allowed responsibilities:** Register schema definitions; retrieve schema by type key; list registered types; validate schema presence.
- **Forbidden responsibilities:** No schema authoring; no content record creation; no domain logic; no persistence writes; no LLM calls.
- **Minimum skeleton behavior:** Accept a dictionary of schema definitions keyed by type string; return schema by key; raise on missing key; list all registered keys.
- **Required tests:** Registry loads fixture schemas; retrieval by key succeeds; missing key raises error; list returns all keys.
- **Downstream dependencies:** RecordIdentityInterface, ValidationPipelineInterface.
- **Blocked domain scope:** No C00–C14 schema implementation; no schema authoring; no conversion record creation.

### 7.2 RecordIdentityInterface

- **Purpose:** Generate, validate, and parse record identifiers following Astra identity conventions.
- **Primary RT owner:** RT-011, C00 (shared content record base).
- **Allowed responsibilities:** Generate unique record IDs; validate ID format; parse ID components; reject malformed IDs.
- **Forbidden responsibilities:** No content creation; no persistence; no domain-specific ID allocation beyond format.
- **Minimum skeleton behavior:** Generate ID from type and optional seed; validate format string; reject empty or malformed input; IDs are deterministic given same inputs.
- **Required tests:** ID generation produces valid format; duplicate inputs produce same ID; malformed input rejected; empty input rejected.
- **Downstream dependencies:** CommandEnvelopeInterface, StateDeltaInterface, EventLedgerInterface.
- **Blocked domain scope:** No entity creation; no persistent ID store; no ID migration.

### 7.3 CommandEnvelopeInterface

- **Purpose:** Wrap player/system commands in typed envelopes with required metadata for lifecycle tracking.
- **Primary RT owner:** RT-001 (command lifecycle/action legality).
- **Allowed responsibilities:** Create command envelope from input; validate required fields; stamp envelope with ID and timestamp; reject missing required fields.
- **Forbidden responsibilities:** No command execution; no legality checking; no state mutation; no action resolution; no LLM interpretation.
- **Minimum skeleton behavior:** Accept command type, source actor ID, and payload dictionary; return envelope with ID, timestamp, type, source, and payload; reject if type or source missing.
- **Required tests:** Envelope creation with valid input succeeds; missing type rejected; missing source rejected; envelope contains required fields; envelope ID is unique.
- **Downstream dependencies:** TransactionPreviewInterface, ValidationPipelineInterface.
- **Blocked domain scope:** No command resolution; no action legality system; no combat commands; no ability commands.

### 7.4 TransactionPreviewInterface

- **Purpose:** Preview the expected effects of a command before commitment, without mutating state.
- **Primary RT owner:** RT-001, RT-002 (resource/consequence math).
- **Allowed responsibilities:** Accept command envelope; produce preview of expected state changes; guarantee no mutation during preview; return preview envelope.
- **Forbidden responsibilities:** No state mutation; no event commitment; no persistence writes; no LLM calls; no actual resource deduction.
- **Minimum skeleton behavior:** Accept command envelope; return preview envelope containing command ID reference and empty delta list; guarantee original envelope unchanged.
- **Required tests:** Preview returns envelope without mutating input; preview references correct command ID; preview produces no side effects; input envelope unchanged after preview.
- **Downstream dependencies:** StateDeltaInterface, ValidationPipelineInterface.
- **Blocked domain scope:** No actual consequence math; no resource calculation; no damage preview; no ability cost preview.

### 7.5 StateDeltaInterface

- **Purpose:** Represent a discrete state change as a typed, immutable delta record.
- **Primary RT owner:** RT-001, RT-002, RT-003.
- **Allowed responsibilities:** Create delta from field changes; validate delta structure; preserve target record ID; mark delta as uncommitted until committed by event ledger.
- **Forbidden responsibilities:** No direct state mutation; no persistence; no event commitment; no LLM calls.
- **Minimum skeleton behavior:** Accept target record ID, field name, old value, and new value; return delta envelope; reject if target ID missing; reject if field name missing.
- **Required tests:** Delta creation with valid input succeeds; missing target ID rejected; missing field name rejected; delta preserves all provided values; delta is a value object (immutable).
- **Downstream dependencies:** EventLedgerInterface, PersistenceBoundaryInterface.
- **Blocked domain scope:** No actual state store; no HP/resource mutation; no combat state; no inventory mutation.

### 7.6 EventLedgerInterface

- **Purpose:** Append-only recording of committed events with ordering guarantees and integrity metadata.
- **Primary RT owner:** RT-001, RT-011.
- **Allowed responsibilities:** Append event entry; assign monotonic sequence number; preserve event ordering; reject duplicate entries; provide read access to ledger.
- **Forbidden responsibilities:** No event deletion; no event mutation; no retroactive edits; no persistence writes (storage-neutral); no LLM calls.
- **Minimum skeleton behavior:** Accept event envelope (type, payload, timestamp); assign sequence number; append to in-memory list; reject if event type missing; return appended event with sequence.
- **Required tests:** Append succeeds; sequence numbers are monotonically increasing; duplicate detection works; missing type rejected; read returns events in order; ledger is append-only (no deletion API).
- **Downstream dependencies:** PersistenceBoundaryInterface, ReplayHashAuditInterface, RuntimeTraceInterface.
- **Blocked domain scope:** No durable persistence; no database writes; no distributed ledger; no cross-session replay.

### 7.7 DeterministicRNGInterface

- **Purpose:** Provide seeded, replayable random number generation for all runtime randomness.
- **Primary RT owner:** RT-009 (runtime RNG/table/oracle).
- **Allowed responsibilities:** Accept seed; produce deterministic sequence; expose next-value method; guarantee replay given same seed; record seed reference in output.
- **Forbidden responsibilities:** No unseeded randomness; no external entropy; no table lookup; no oracle resolution; no LLM calls; no state mutation.
- **Minimum skeleton behavior:** Accept integer seed; return generator object; generator produces deterministic integer sequence; same seed always produces same sequence.
- **Required tests:** Same seed produces same sequence; different seeds produce different sequences; generator state advances predictably; seed is recorded in output.
- **Downstream dependencies:** TableOracleInterface, EventLedgerInterface (for recording RNG events).
- **Blocked domain scope:** No table data; no oracle content; no domain-specific roll interpretation; no dice notation parser.

### 7.8 TableOracleInterface

- **Purpose:** Invoke table/oracle lookups using RNG results within a typed envelope contract.
- **Primary RT owner:** RT-009.
- **Allowed responsibilities:** Accept table ID and RNG result; return result envelope; validate table ID format; reject invalid RNG input.
- **Forbidden responsibilities:** No table content storage; no table authoring; no oracle content creation; no LLM calls; no persistence.
- **Minimum skeleton behavior:** Accept table ID string and integer RNG result; return envelope with table ID, input value, and placeholder result field; reject if table ID missing.
- **Required tests:** Invocation with valid input returns envelope; missing table ID rejected; envelope contains table ID and input value; no side effects.
- **Downstream dependencies:** EventLedgerInterface, ValidationPipelineInterface.
- **Blocked domain scope:** No table data files; no random table content; no oracle interpretation; no encounter tables; no loot tables.

### 7.9 ValidationPipelineInterface

- **Purpose:** Run validation checks against commands, deltas, and events before commitment.
- **Primary RT owner:** RT-011 (validation/readiness/tooling).
- **Allowed responsibilities:** Accept validation target; run registered validators; return pass/fail result with reasons; guarantee no mutation during validation.
- **Forbidden responsibilities:** No state mutation; no event commitment; no persistence; no LLM calls; no domain-specific validation rules beyond structural checks.
- **Minimum skeleton behavior:** Accept target envelope; return validation result (pass/fail, list of reasons); always pass if no validators registered; reject if target is None.
- **Required tests:** Empty pipeline passes all targets; null target rejected; result contains pass/fail status; result contains reasons list; validation does not mutate target.
- **Downstream dependencies:** CommandEnvelopeInterface, TransactionPreviewInterface, StateDeltaInterface.
- **Blocked domain scope:** No domain validators; no combat validators; no ability validators; no resource validators.

### 7.10 HiddenInformationPartitionInterface

- **Purpose:** Partition state into visible and hidden components based on actor perspective.
- **Primary RT owner:** RT-005 (context packet/hidden information).
- **Allowed responsibilities:** Accept full state and actor ID; return visible partition only; guarantee hidden state never appears in visible output; validate actor ID.
- **Forbidden responsibilities:** No state mutation; no hidden-state revelation; no LLM calls; no persistence; no redaction algorithm implementation.
- **Minimum skeleton behavior:** Accept state dictionary and actor ID; return filtered dictionary excluding keys marked as hidden; reject if actor ID missing; never include hidden keys in output.
- **Required tests:** Hidden keys excluded from output; visible keys present in output; missing actor ID rejected; empty state returns empty result; no hidden information leakage.
- **Downstream dependencies:** ContextProjectionInterface.
- **Blocked domain scope:** No redaction algorithm; no visibility tier system; no per-entity hidden state; no fog-of-war; no secret knowledge database.

### 7.11 ContextProjectionInterface

- **Purpose:** Project visible state into a context packet suitable for narration layer consumption.
- **Primary RT owner:** RT-005, RT-001.
- **Allowed responsibilities:** Accept visible state partition; produce context projection envelope; include only visible information; include metadata for narration contract.
- **Forbidden responsibilities:** No hidden information inclusion; no state mutation; no LLM calls; no narration generation; no prompt assembly.
- **Minimum skeleton behavior:** Accept visible state dictionary; return context projection envelope with visible fields and metadata timestamp; reject if input is None.
- **Required tests:** Projection contains only visible state; projection includes metadata; null input rejected; projection is a new object (no reference to original); no hidden information present.
- **Downstream dependencies:** PersistenceBoundaryInterface (for projection snapshots), RuntimeTraceInterface.
- **Blocked domain scope:** No narration rendering; no prompt templates; no model calls; no packet budget enforcement; no token counting.

### 7.12 PersistenceBoundaryInterface

- **Purpose:** Define the contract boundary where in-memory state may be written to durable storage.
- **Primary RT owner:** RT-011, RT-001.
- **Allowed responsibilities:** Define save/load interface signatures; accept state snapshot; accept event ledger snapshot; return acknowledgment; declare storage-neutral contract.
- **Forbidden responsibilities:** No actual file I/O; no database writes; no SQLite calls; no network I/O; no LLM calls.
- **Minimum skeleton behavior:** Accept state dictionary for save; return success acknowledgment (no-op in skeleton); accept load request; return empty state (no-op in skeleton). Skeleton performs no actual persistence.
- **Required tests:** Save accepts state and returns acknowledgment; load returns empty state; no file I/O occurs; no database calls occur; interface is storage-neutral.
- **Downstream dependencies:** ReplayHashAuditInterface.
- **Blocked domain scope:** No SQLite; no file writes; no database schema; no migration system; no backup system.

### 7.13 ReplayHashAuditInterface

- **Purpose:** Verify event ledger integrity and support deterministic replay for audit purposes.
- **Primary RT owner:** RT-009, RT-011.
- **Allowed responsibilities:** Compute hash of event sequence; verify hash matches expected value; support replay verification; detect ledger tampering.
- **Forbidden responsibilities:** No state mutation; no event creation; no persistence; no LLM calls; no actual replay execution.
- **Minimum skeleton behavior:** Accept event list; compute deterministic hash of event sequence; return hash string; verify provided hash against computed hash; return match/mismatch result.
- **Required tests:** Same events produce same hash; different events produce different hash; verification succeeds on matching hash; verification fails on mismatched hash; empty ledger produces consistent hash.
- **Downstream dependencies:** RuntimeTraceInterface, PersistenceBoundaryInterface.
- **Blocked domain scope:** No distributed consensus; no cross-session replay; no backup verification; no migration audit.

### 7.14 RuntimeTraceInterface

- **Purpose:** Record diagnostic trace of runtime operations for observability and debugging.
- **Primary RT owner:** RT-011.
- **Allowed responsibilities:** Record trace entries; timestamp entries; categorize by operation type; provide read access to trace; support filtering by category.
- **Forbidden responsibilities:** No state mutation; no event commitment; no persistence; no LLM calls; no performance monitoring.
- **Minimum skeleton behavior:** Accept trace entry (category string, message string); assign timestamp; append to in-memory trace list; support retrieval of all entries; support filtering by category.
- **Required tests:** Trace entry appended successfully; entries have timestamps; filter by category returns correct subset; empty trace returns empty list; entries preserve order.
- **Downstream dependencies:** None (terminal observability layer).
- **Blocked domain scope:** No distributed tracing; no log aggregation; no metrics; no alerting; no performance profiling.

---

## 8. RUNTIME-IMPL-PR sequence

### RUNTIME-IMPL-PR-1: Schema Registry and Record Identity Skeleton

- **Purpose:** Implement the first two kernel interfaces as importable, testable Python modules.
- **Expected files:** `src/astra_runtime/__init__.py`, `src/astra_runtime/kernel/__init__.py`, `src/astra_runtime/kernel/schema_registry.py`, `src/astra_runtime/kernel/record_identity.py`.
- **Expected tests:** `tests/runtime/test_schema_registry_skeleton.py`, `tests/runtime/test_record_identity_skeleton.py`.
- **Required predecessor:** RUNTIME-IMPL-PR-0 accepted.
- **Allowed implementation:** Schema registry loader; record identity generator/validator; in-memory fixture schemas; package structure; pyproject.toml if needed.
- **Forbidden scope:** Command envelope; transaction preview; state delta; event ledger; RNG; validation pipeline; hidden-info partition; context projection; persistence; domain services; live-play; model integration; conversion.
- **Exit criteria:** All tests pass; schema registry loads and retrieves fixture schemas; record identity generates and validates IDs; no domain logic present.

### RUNTIME-IMPL-PR-2: Command Envelope and Transaction Preview Skeleton

- **Purpose:** Implement command envelope wrapping and transaction preview contract.
- **Expected files:** `src/astra_runtime/kernel/command_envelope.py`, `src/astra_runtime/kernel/transaction_preview.py`.
- **Expected tests:** `tests/runtime/test_command_envelope_skeleton.py`, `tests/runtime/test_transaction_preview_skeleton.py`.
- **Required predecessor:** RUNTIME-IMPL-PR-1 merged.
- **Allowed implementation:** Command envelope creation/validation; transaction preview envelope; no-mutation guarantee tests.
- **Forbidden scope:** State delta; event ledger; RNG; validation pipeline; hidden-info; context projection; persistence; domain services; command resolution; action legality.
- **Exit criteria:** Command envelopes created and validated; transaction preview produces envelope without mutation; all tests pass.

### RUNTIME-IMPL-PR-3: State Delta and Event Ledger Envelope Skeleton

- **Purpose:** Implement state delta value objects and append-only event ledger envelope.
- **Expected files:** `src/astra_runtime/kernel/state_delta.py`, `src/astra_runtime/kernel/event_ledger.py`.
- **Expected tests:** `tests/runtime/test_state_delta_skeleton.py`, `tests/runtime/test_event_ledger_skeleton.py`.
- **Required predecessor:** RUNTIME-IMPL-PR-2 merged.
- **Allowed implementation:** State delta creation/validation; event ledger append/read; sequence numbers; append-only enforcement; in-memory storage.
- **Forbidden scope:** RNG; validation pipeline; hidden-info; context projection; persistence; database; domain state; actual game state.
- **Exit criteria:** State deltas are immutable value objects; event ledger is append-only with monotonic sequence; all tests pass.

### RUNTIME-IMPL-PR-4: Deterministic RNG/Table Interface Skeleton

- **Purpose:** Implement seeded deterministic RNG and table/oracle invocation envelope.
- **Expected files:** `src/astra_runtime/kernel/rng_interface.py`.
- **Expected tests:** `tests/runtime/test_rng_interface_skeleton.py`.
- **Required predecessor:** RUNTIME-IMPL-PR-3 merged.
- **Allowed implementation:** Seeded RNG generator; deterministic sequence; table invocation envelope; seed recording.
- **Forbidden scope:** Table data; oracle content; domain-specific roll interpretation; validation pipeline; hidden-info; context projection; persistence.
- **Exit criteria:** RNG is deterministic given same seed; table invocation returns typed envelope; all tests pass.

### RUNTIME-IMPL-PR-5: Validation Pipeline and Invariant Precheck Skeleton

- **Purpose:** Implement pluggable validation pipeline with pass/fail results.
- **Expected files:** `src/astra_runtime/kernel/validation_pipeline.py`.
- **Expected tests:** `tests/runtime/test_validation_pipeline_skeleton.py`.
- **Required predecessor:** RUNTIME-IMPL-PR-4 merged.
- **Allowed implementation:** Validator registration; pipeline execution; pass/fail result with reasons; no-mutation guarantee.
- **Forbidden scope:** Domain-specific validators; combat rules; ability rules; resource rules; hidden-info; context projection; persistence.
- **Exit criteria:** Pipeline runs registered validators; returns structured results; does not mutate targets; all tests pass.

### RUNTIME-IMPL-PR-6: Hidden-Information Partition and Context Projection Skeleton

- **Purpose:** Implement hidden-information partitioning and visible-only context projection.
- **Expected files:** `src/astra_runtime/kernel/hidden_information.py`, `src/astra_runtime/kernel/context_projection.py`.
- **Expected tests:** `tests/runtime/test_hidden_information_skeleton.py`, `tests/runtime/test_context_projection_skeleton.py`.
- **Required predecessor:** RUNTIME-IMPL-PR-5 merged.
- **Allowed implementation:** State partitioning by actor; visible-only projection; hidden key exclusion; context envelope creation.
- **Forbidden scope:** Redaction algorithm; visibility tiers; narration rendering; prompt assembly; model calls; persistence; domain state.
- **Exit criteria:** Hidden state never appears in visible output; context projection contains only visible fields; all tests pass.

### RUNTIME-IMPL-PR-7: Persistence Boundary, Replay/Hash Audit, and Runtime Trace Skeleton

- **Purpose:** Implement storage-neutral persistence interface, replay hash verification, and runtime trace.
- **Expected files:** `src/astra_runtime/kernel/persistence_boundary.py`, `src/astra_runtime/kernel/replay_audit.py`, `src/astra_runtime/kernel/runtime_trace.py`.
- **Expected tests:** `tests/runtime/test_persistence_boundary_skeleton.py`, `tests/runtime/test_replay_audit_skeleton.py`, `tests/runtime/test_runtime_trace_skeleton.py`.
- **Required predecessor:** RUNTIME-IMPL-PR-6 merged.
- **Allowed implementation:** No-op persistence interface; hash computation for event sequences; replay verification; trace recording and filtering.
- **Forbidden scope:** SQLite; file I/O; database schema; migrations; distributed tracing; log aggregation; domain services.
- **Exit criteria:** Persistence interface is storage-neutral with no I/O; replay hash is deterministic; trace records and filters entries; all tests pass.

### RUNTIME-IMPL-PR-8: Post-Kernel Skeleton Review and Domain-Service Readiness Gate

- **Purpose:** Review the completed kernel skeleton and assess readiness for domain service implementation.
- **Expected files:** Review document under `docs/doctrine/reviews/`.
- **Expected tests:** Presence and content verification tests.
- **Required predecessor:** RUNTIME-IMPL-PR-7 merged.
- **Allowed implementation:** Review document; integration smoke tests across all kernel interfaces; readiness assessment.
- **Forbidden scope:** Domain services; generator libraries; live-play adapter; model integration; conversion; canon promotion.
- **Exit criteria:** All kernel interfaces implemented and tested; integration tests pass; readiness gate document produced; next-phase recommendation issued.

---

## 9. RUNTIME-IMPL-PR-1 authorization boundary

### RUNTIME-IMPL-PR-1 may implement

- Minimal package structure (`src/astra_runtime/`, `src/astra_runtime/kernel/`) if absent;
- `pyproject.toml` for package definition if absent;
- Schema registry skeleton (`src/astra_runtime/kernel/schema_registry.py`);
- Record identity skeleton (`src/astra_runtime/kernel/record_identity.py`);
- Focused tests for registry loading and ID conventions;
- No-op or minimal in-memory fixtures where needed;
- Documentation linking implementation to doctrine.

### RUNTIME-IMPL-PR-1 must not implement

- Command IR;
- Transaction preview;
- State store;
- State delta;
- Event ledger;
- RNG/table service;
- Validation pipeline beyond local skeleton checks needed for registry/identity;
- Context projection;
- Hidden-info partition;
- Persistence writer;
- Database schema;
- Domain services;
- Live-play adapter;
- Model integration;
- Generator library;
- Conversion execution.

---

## 10. Kernel skeleton invariants

Future implementation must preserve these invariants from the first code PR:

1. **No LLM state authority.** The LLM never owns, commits, or validates game state.
2. **No narration as state.** Narration text is display output, not state source.
3. **No summaries as memory authority.** Summaries are lossy projections, not canonical records.
4. **No hidden facts in visible projection.** Hidden-information partitioning must exclude hidden state from all visible outputs.
5. **No event commitment without event envelope.** Every state change must pass through the event ledger as a typed entry.
6. **No random outcome without RNG/table reference** once the RNG interface exists.
7. **No generated-content durability without provenance** once the generator boundary exists.
8. **No source-local/canon promotion by implementation side effect.** Promotion requires explicit governance action.
9. **No domain service before kernel skeleton.** Domain services depend on kernel interfaces being in place.
10. **No persistence before persistence boundary.** No file/database writes until the persistence boundary interface is implemented.

---

## 11. Storage-neutral persistence plan

### Early persistence stance

- The first skeleton must be **in-memory and storage-neutral**. No file I/O, no database, no network storage.
- Persistence interfaces may be named and planned before implementation. The interface contract is defined in RUNTIME-IMPL-PR-7 but performs no actual I/O.
- Event log abstractions must not require a database initially. In-memory append-only lists are sufficient for the skeleton.
- **SQLite** is a plausible later local durable campaign store but must not be chosen or implemented until the persistence boundary interface is proven and separately authorized.
- File-backed JSON/YAML fixtures may be used for tests only, not as runtime state storage.
- Migrations are deferred until durable storage is authorized in a post-kernel PR.

---

## 12. Testing strategy

### Test families for future PRs

| Test family | Purpose | First PR |
|---|---|---|
| Import/package smoke tests | Verify package structure is importable | PR-1 |
| Schema registry fixture loading tests | Verify registry loads and retrieves schemas | PR-1 |
| Record identity uniqueness/format tests | Verify ID generation and validation | PR-1 |
| Command envelope required-field tests | Verify envelope creation and rejection | PR-2 |
| Transaction preview no-mutation tests | Verify preview produces no side effects | PR-2 |
| State delta envelope integrity tests | Verify delta immutability and structure | PR-3 |
| Event append-only envelope tests | Verify ledger is append-only with ordering | PR-3 |
| Deterministic RNG seed/replay tests | Verify same seed produces same sequence | PR-4 |
| Table/oracle invocation envelope tests | Verify table invocation envelope contract | PR-4 |
| Validation pipeline pass/fail tests | Verify pipeline execution and results | PR-5 |
| Hidden-info partition exclusion tests | Verify hidden state never leaks to visible | PR-6 |
| Context projection visible-only tests | Verify projection contains only visible state | PR-6 |
| Persistence boundary no-write tests | Verify no actual I/O occurs in skeleton | PR-7 |
| Replay/hash deterministic reference tests | Verify hash determinism and verification | PR-7 |
| Runtime trace completeness tests | Verify trace recording and filtering | PR-7 |
| LLM non-authority guardrail tests | Verify no LLM state mutation path exists | PR-1+ |

---

## 13. Implementation risk controls

| Risk | Mitigation | First PR | Owner track |
|---|---|---|---|
| Schema drift between doctrine schemas and runtime registry | Registry must load from doctrine-aligned fixtures; drift tests compare keys | PR-1 | RT-011 |
| Command/state/event collapse (commands directly mutating state) | Transaction preview must be separate from commitment; tests enforce separation | PR-2 | RT-001 |
| Hidden-info leakage (hidden state appearing in visible output) | Partition interface tests with known hidden keys; negative tests for leakage | PR-6 | RT-005 |
| LLM becoming de facto engine (model calls in kernel path) | No import of model libraries in kernel; static analysis check in CI | PR-1 | RT-011 |
| Overbuilt domain services (domain logic in kernel skeleton) | Kernel modules contain only envelope/interface logic; domain scope blocked per PR | PR-1 | RT-011 |
| Event ledger incompleteness (state changes bypassing ledger) | All delta commitment must route through event ledger; tests verify | PR-3 | RT-001 |
| Persistence migration debt (premature schema locks) | No durable persistence until PR-7; interface is storage-neutral | PR-7 | RT-011 |
| RNG non-determinism (unseeded or external entropy) | RNG interface requires seed; tests verify replay; no `random.random()` calls | PR-4 | RT-009 |
| Brittle tests over doctrine strings only | Tests verify structural properties and interface contracts, not prose content | PR-1 | RT-011 |
| Model prompts sneaking into runtime (prompt templates in kernel) | No prompt/template files in `src/astra_runtime/`; directory scan test | PR-1 | RT-011 |
| Generated content becoming durable too early | No generated-content persistence until provenance interface exists | PR-7+ | RT-008 |
| Source-local/canon boundary collapse | No promotion logic in kernel; record identity does not imply canon status | PR-1 | RT-012 |

---

## 14. Documentation and registry alignment

Future implementation PRs must update:

- `docs/decisions/current_decisions_log.md` with a decision entry for each implementation PR;
- `docs/doctrine/astra_doctrine_registry_v0_1.yaml` with a registry tracking entry;
- Relevant implementation documentation;
- Tests verifying the above tracking.

Implementation files must not be treated as doctrine authority unless a registry/decision-log entry explicitly says so. Runtime code implements approved contracts; it does not rewrite doctrine.

---

## 15. Blocked-until ledger

| Item | Blocked until |
|---|---|
| Runtime code | RUNTIME-IMPL-PR-1 or later |
| Schemas beyond skeleton | Separately authorized |
| Command IR | RUNTIME-IMPL-PR-2 |
| Transaction preview | RUNTIME-IMPL-PR-2 |
| State delta/event ledger | RUNTIME-IMPL-PR-3 |
| RNG/table service | RUNTIME-IMPL-PR-4 |
| Validation pipeline | RUNTIME-IMPL-PR-5 |
| Hidden-info/context projection | RUNTIME-IMPL-PR-6 |
| Persistence/replay/trace | RUNTIME-IMPL-PR-7 |
| Domain services | Post-kernel review (RUNTIME-IMPL-PR-8) |
| Generator libraries | Provenance and validation exist |
| Live-play adapter | Packet contracts, hidden-info projection, event/state, and validation exist |
| Model routing | Model evaluation exists |
| Training | Live-play packet contracts and training governance exist |
| Pilot conversion | Records, validation, and landing pipeline exist |
| Sourcebook inclusion | Canon/sourcebook governance exists |
| Canon promotion | Canon governance exists |

---

## 16. Next recommended PR

**Recommended:** RUNTIME-IMPL-PR-1: Schema Registry and Record Identity Skeleton.

RUNTIME-IMPL-PR-1 may be the first code PR if this plan is accepted.

PR-1 should remain extremely narrow and must not implement command lifecycle, event ledger, RNG, validation pipeline, context projection, persistence, domain services, live-play, model integration, or conversion.

---

## 17. Non-implementation reaffirmation

This PR adds **no**:

- runtime code;
- schema implementation;
- command IR;
- validator implementation;
- generator implementation;
- state store;
- state delta model;
- event ledger;
- transaction system;
- invariant validator;
- correction event schema;
- deterministic RNG service;
- table/oracle service;
- persistence writer;
- database schema;
- context-packet compiler;
- redaction algorithm;
- hidden-state database;
- domain service;
- model evaluation code;
- benchmark runner;
- prompt template;
- live-play adapter;
- training data;
- donor-content audit;
- pilot conversion authorization;
- sourcebook inclusion authorization;
- canon promotion.

---

## 18. Classification block

```yaml
runtime_impl_pr_0:
  review_id: RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
  artifact_type: minimum_backend_kernel_executable_implementation_plan
  implementation_status: non_executable_plan
  derives_from:
    - RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001
    - RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001
    - RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001
    - RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001
    - RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001
    - RUNTIME-SEQ-PR-E-MODEL-EVALUATION-STRUCTURED-OUTPUT-ADVERSARIAL-COMMAND-PLAN-001
  confirms_backend_first_invariant: true
  confirms_llm_is_not_game_engine: true
  confirms_python_pytest_initial_stack_recommendation: true
  defines_minimum_backend_kernel_target: true
  defines_future_package_layout: true
  defines_interface_boundary_plan: true
  defines_runtime_impl_pr_sequence: true
  authorizes_code_implementation_by_this_pr: false
  authorizes_runtime_implementation_by_this_pr: false
  authorizes_schema_implementation_by_this_pr: false
  authorizes_command_ir_by_this_pr: false
  authorizes_state_store_by_this_pr: false
  authorizes_event_ledger_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_persistence_writer_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-IMPL-PR-1 schema registry and record identity skeleton, pending review
```

# RUNTIME-IMPL-PR-8: Post-Kernel Skeleton Review and Domain-Service Readiness Gate

## 1. Purpose and status

This document is **RUNTIME-IMPL-PR-8**, a post-kernel skeleton review and domain-service readiness gate.

- **Type:** planning/review-only, non-executable.
- **Scope:** reviews RUNTIME-IMPL-PR-1 through RUNTIME-IMPL-PR-7 implementation skeletons and decides whether the project is ready for a future domain-service implementation-planning sequence.
- **This PR does not implement code.**

---

## 2. Source ledger

### Implementation plans and gate sources

| Source ID | Title |
|-----------|-------|
| RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001 | Minimum backend kernel executable implementation plan |
| RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001 | Schema registry and record identity skeleton |
| RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001 | Command envelope and transaction preview skeleton |
| RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001 | State delta and event ledger envelope skeleton |
| RUNTIME-IMPL-PR-4-DETERMINISTIC-RNG-TABLE-ORACLE-INTERFACE-SKELETON-001 | Deterministic RNG and table/oracle interface skeleton |
| RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001 | Validation pipeline and invariant precheck skeleton |
| RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001 | Hidden-information partition and context projection skeleton |
| RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001 | Persistence boundary, replay/hash audit, and runtime trace skeleton |

### Runtime sequence planning sources

| Source ID | Title |
|-----------|-------|
| RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001 | Minimum backend kernel and runtime quality contract plan |
| RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001 | Narration / context packet contract plan |
| RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001 | State / event / invariant / transaction plan |
| RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001 | Story-capable structure and playable-content plan |
| RUNTIME-SEQ-PR-E-MODEL-EVALUATION-STRUCTURED-OUTPUT-ADVERSARIAL-COMMAND-PLAN-001 | Model evaluation, structured-output, and adversarial-command plan |
| RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001 | Implementation-readiness review and executable kernel authorization gate |

### Owner specifications

| Spec ID | Title |
|---------|-------|
| RT-001 | Command lifecycle and action legality |
| RT-002 | Resource / consequence math |
| RT-003 | Combat / hazard / damage / recovery |
| RT-004 | Ability / effect / skill binding |
| RT-005 | Context packet and hidden information |
| RT-006 | Mission / reward / clue routing |
| RT-007 | Social / faction / actor knowledge |
| RT-008 | Generated content provenance and recurrence |
| RT-009 | Runtime RNG and table/oracle |
| RT-010 | Inventory / item / vehicle / asset |
| RT-011 | Validation readiness and tooling |
| RT-012 | D-series promotion boundary |

### Implemented runtime skeleton modules

| Module | Path |
|--------|------|
| schema_registry | `src/astra_runtime/kernel/schema_registry.py` |
| record_identity | `src/astra_runtime/kernel/record_identity.py` |
| command_envelope | `src/astra_runtime/kernel/command_envelope.py` |
| transaction_preview | `src/astra_runtime/kernel/transaction_preview.py` |
| state_delta | `src/astra_runtime/kernel/state_delta.py` |
| event_ledger | `src/astra_runtime/kernel/event_ledger.py` |
| rng_interface | `src/astra_runtime/kernel/rng_interface.py` |
| table_oracle | `src/astra_runtime/kernel/table_oracle.py` |
| validation_pipeline | `src/astra_runtime/kernel/validation_pipeline.py` |
| hidden_information | `src/astra_runtime/kernel/hidden_information.py` |
| context_projection | `src/astra_runtime/kernel/context_projection.py` |
| persistence_boundary | `src/astra_runtime/kernel/persistence_boundary.py` |
| replay_audit | `src/astra_runtime/kernel/replay_audit.py` |
| runtime_trace | `src/astra_runtime/kernel/runtime_trace.py` |

### Implemented runtime skeleton tests

| Test file | Path |
|-----------|------|
| test_schema_registry_skeleton | `tests/runtime/test_schema_registry_skeleton.py` |
| test_record_identity_skeleton | `tests/runtime/test_record_identity_skeleton.py` |
| test_command_envelope_skeleton | `tests/runtime/test_command_envelope_skeleton.py` |
| test_transaction_preview_skeleton | `tests/runtime/test_transaction_preview_skeleton.py` |
| test_state_delta_skeleton | `tests/runtime/test_state_delta_skeleton.py` |
| test_event_ledger_skeleton | `tests/runtime/test_event_ledger_skeleton.py` |
| test_rng_interface_skeleton | `tests/runtime/test_rng_interface_skeleton.py` |
| test_table_oracle_skeleton | `tests/runtime/test_table_oracle_skeleton.py` |
| test_validation_pipeline_skeleton | `tests/runtime/test_validation_pipeline_skeleton.py` |
| test_hidden_information_skeleton | `tests/runtime/test_hidden_information_skeleton.py` |
| test_context_projection_skeleton | `tests/runtime/test_context_projection_skeleton.py` |
| test_persistence_boundary_skeleton | `tests/runtime/test_persistence_boundary_skeleton.py` |
| test_replay_audit_skeleton | `tests/runtime/test_replay_audit_skeleton.py` |
| test_runtime_trace_skeleton | `tests/runtime/test_runtime_trace_skeleton.py` |

### Registry and decision log

| Artifact | Path |
|----------|------|
| Doctrine registry | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` |
| Decision log | `docs/decisions/current_decisions_log.md` |
| Project config | `pyproject.toml` |

### Schema files (C00–C14)

| Schema ID | Path |
|-----------|------|
| C00 | `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` |
| C01 | `docs/doctrine/schema/C01_creature_npc_record_schema.md` |
| C02 | `docs/doctrine/schema/C02_item_gear_record_schema.md` |
| C03 | `docs/doctrine/schema/C03_ability_power_technique_record_schema.md` |
| C04 | `docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md` |
| C05 | `docs/doctrine/schema/C05_faction_institution_record_schema.md` |
| C06 | `docs/doctrine/schema/C06_location_site_region_record_schema.md` |
| C07 | `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md` |
| C08 | `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md` |
| C09 | `docs/doctrine/schema/C09_hazard_environment_record_schema.md` |
| C10 | `docs/doctrine/schema/C10_table_oracle_record_schema.md` |
| C11 | `docs/doctrine/schema/C11_companion_summon_record_schema.md` |
| C12 | `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md` |
| C13 | `docs/doctrine/schema/C13_map_diagram_record_schema.md` |
| C14 | `docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md` |

---

## 3. Backend-first invariant

**Astra Ascension must be model-interchangeable.** The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

### Review implication

Domain services may only be authorized after backend-owned envelopes, IDs, RNG/table authority, validation, hidden-info projection, persistence boundaries, replay/hash audit, and trace boundaries exist. Domain services must consume kernel interfaces rather than bypass them.

---

## 4. Kernel skeleton coverage review

| PR ID | Kernel area | Files implemented | Tests implemented | Readiness status | Remaining limitations | Downstream unlocks | Still-blocked scope |
|-------|-------------|-------------------|-------------------|------------------|-----------------------|-------------------|---------------------|
| RUNTIME-IMPL-PR-1 | Schema registry and record identity | `schema_registry.py`, `record_identity.py` | `test_schema_registry_skeleton.py`, `test_record_identity_skeleton.py` | skeleton_complete_with_limitations | No durable schema store; no schema versioning; no live schema migration | Record types for all domain services; content-record identity foundation | Full schema store; schema versioning; live migration |
| RUNTIME-IMPL-PR-2 | Command envelope and transaction preview | `command_envelope.py`, `transaction_preview.py` | `test_command_envelope_skeleton.py`, `test_transaction_preview_skeleton.py` | skeleton_complete_with_limitations | No command execution engine; no transaction lifecycle; no confirmation workflow | Command lifecycle service; action legality checks; transaction preview display | Command execution; full transaction lifecycle engine; player confirmation loop |
| RUNTIME-IMPL-PR-3 | State delta and event ledger envelope | `state_delta.py`, `event_ledger.py` | `test_state_delta_skeleton.py`, `test_event_ledger_skeleton.py` | skeleton_complete_with_limitations | No state store; no event commitment; no event persistence; no event replay | State projection; event commitment service; delta application logic | Durable state store; event commitment engine; state mutation authority |
| RUNTIME-IMPL-PR-4 | Deterministic RNG and table/oracle interface | `rng_interface.py`, `table_oracle.py` | `test_rng_interface_skeleton.py`, `test_table_oracle_skeleton.py` | skeleton_complete_with_limitations | No table data store; no oracle configuration registry; seed management is caller-owned | All randomness-dependent domain services; combat rolls; loot tables; encounter generation | Table data persistence; oracle configuration management; seed sequencing service |
| RUNTIME-IMPL-PR-5 | Validation pipeline and invariant precheck | `validation_pipeline.py` | `test_validation_pipeline_skeleton.py` | skeleton_complete_with_limitations | No domain-specific validation rules; no invariant registry integration; check callables are caller-supplied | Validation integration for all domain services; invariant enforcement; quarantine routing | Domain-specific validation rules; world-invariant registry; rule-engine integration |
| RUNTIME-IMPL-PR-6 | Hidden-information partition and context projection | `hidden_information.py`, `context_projection.py` | `test_hidden_information_skeleton.py`, `test_context_projection_skeleton.py` | skeleton_complete_with_limitations | No context-packet compiler; no prompt template assembly; no access-control policy engine; no reveal mechanics | Context packet service; model-facing packet assembly; visibility-aware state projection | Context-packet compiler; prompt templates; model integration; reveal mechanics |
| RUNTIME-IMPL-PR-7 | Persistence boundary, replay/hash audit, runtime trace | `persistence_boundary.py`, `replay_audit.py`, `runtime_trace.py` | `test_persistence_boundary_skeleton.py`, `test_replay_audit_skeleton.py`, `test_runtime_trace_skeleton.py` | skeleton_complete_with_limitations | No durable persistence backend; no replay engine; no hash-chain enforcement; no trace store; no telemetry | Persistence integration for all domain services; replay verification; audit trail | Durable storage backend; replay engine; hash-chain enforcement; trace store; telemetry |

### Expected finding

The minimum backend kernel skeleton sequence (PR-1 through PR-7) is **complete enough to proceed to a future domain-service implementation-planning PR** (RUNTIME-DOMAIN-PR-0), not to direct domain-service implementation.

All 14 kernel modules exist, all 14 have passing skeleton tests, and all follow the backend-first invariant. The skeletons define envelopes, interfaces, and validation postures but intentionally omit execution engines, persistence backends, and domain logic.

---

## 5. Interface completeness matrix

| Module | Module exists | Executable tests exist | Backend ownership preserved | Immutable/envelope posture | Validation posture | No domain logic | No persistence side effect | No LLM authority | Readiness for domain-service planning |
|--------|--------------|----------------------|---------------------------|--------------------------|-------------------|----------------|--------------------------|-----------------|--------------------------------------|
| schema_registry | yes | yes | yes | yes | yes | yes | yes | yes | ready_for_domain_service_planning |
| record_identity | yes | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| command_envelope | yes | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| transaction_preview | yes | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| state_delta | yes | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| event_ledger | yes | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| rng_interface | yes | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| table_oracle | yes | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| validation_pipeline | yes | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| invariant_precheck | yes (in validation_pipeline) | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| hidden_information | yes | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| context_projection | yes | yes | yes | yes (frozen) | yes | yes | yes | yes | ready_for_domain_service_planning |
| persistence_boundary | yes | yes | yes | yes (frozen) | yes | yes | yes (prepare-only, no write) | yes | ready_for_domain_service_planning |
| replay_audit | yes | yes | yes | yes (frozen) | yes | yes | yes (no replay engine) | yes | ready_for_domain_service_planning |
| runtime_trace | yes | yes | yes | yes (frozen) | yes | yes | yes (no trace store) | yes | ready_for_domain_service_planning |

All 15 rows: **ready_for_domain_service_planning**.

Additional universal statuses that apply to all rows:

- `blocked_for_direct_runtime_execution` — skeletons define interfaces but cannot execute domain transactions.
- `not_authorized_for_domain_implementation` — this PR does not authorize domain code.
- `requires_future_integration_tests` — cross-module integration tests are deferred to post-skeleton phase.

---

## 6. Domain-service readiness finding

### Gate finding

```yaml
gate_finding:
  minimum_backend_kernel_skeleton_complete: true
  ready_for_domain_service_planning: true
  direct_domain_service_implementation_authorized_by_this_pr: false
  direct_live_play_authorized_by_this_pr: false
  direct_conversion_execution_authorized_by_this_pr: false
  next_step_authorized: domain_service_implementation_sequencing_plan
  next_step_id: RUNTIME-DOMAIN-PR-0
  next_step_status: planning_only
```

### Gate statements

- **PR-8 does not authorize domain-service code.** No domain service may be implemented based on this PR alone.
- **PR-8 authorizes only a future planning PR for domain-service sequencing.** The next authorized step is RUNTIME-DOMAIN-PR-0, a planning-only PR that defines domain-service implementation order, boundaries, allowed dependencies, tests, and guardrails.
- **Domain services remain blocked** until RUNTIME-DOMAIN-PR-0 defines order, boundaries, allowed dependencies, tests, and guardrails.

---

## 7. Domain-service family sequencing proposal

The following domain-service planning sequence is **proposed only**. This section does not implement any service.

The future planning sequence should cover, at minimum:

1. **Command lifecycle and action legality service** — consumes command_envelope, transaction_preview, validation_pipeline; governs RT-001.
2. **State store / state projection service** — consumes state_delta, event_ledger, persistence_boundary; provides durable game state.
3. **Transaction lifecycle service** — consumes command_envelope, transaction_preview, state_delta, event_ledger; governs commit/rollback.
4. **Event commitment service** — consumes event_ledger, persistence_boundary, replay_audit; governs durable event append.
5. **Validation integration service** — consumes validation_pipeline; wires domain-specific invariant checks; governs RT-011.
6. **Resource / consequence math service** — consumes state_delta, rng_interface; governs RT-002.
7. **Combat / hazard / damage / recovery service** — consumes rng_interface, state_delta, validation_pipeline; governs RT-003.
8. **Ability / effect / skill binding service** — consumes schema_registry, record_identity, state_delta; governs RT-004.
9. **Inventory / item / vehicle / asset service** — consumes schema_registry, record_identity, state_delta; governs RT-010.
10. **Mission / reward / clue routing service** — consumes state_delta, event_ledger, hidden_information; governs RT-006.
11. **Social / faction / actor knowledge service** — consumes hidden_information, context_projection, state_delta; governs RT-007.
12. **Generated content provenance service** — consumes runtime_trace, replay_audit; governs RT-008.
13. **Context-packet compiler** — consumes context_projection, hidden_information; assembles model-facing packets; governs RT-005.
14. **Model evaluation harness** — consumes context-packet output; evaluates model behavior.
15. **Live-play adapter gate** — final integration gate before any live-play session.

This sequence is provisional and may be adjusted by RUNTIME-DOMAIN-PR-0.

---

## 8. Recommended next PR

**Recommended:** `RUNTIME-DOMAIN-PR-0: Domain Service Implementation Sequencing Plan`

This next PR should be **planning-only** and should decide the correct domain-service implementation order.

### Suggested early order

| PR ID | Title | Type |
|-------|-------|------|
| RUNTIME-DOMAIN-PR-0 | Domain service implementation sequencing plan | planning |
| RUNTIME-DOMAIN-PR-1 | Command lifecycle / action legality service plan | planning |
| RUNTIME-DOMAIN-PR-2 | State store and state projection service plan | planning |
| RUNTIME-DOMAIN-PR-3 | Transaction lifecycle and event commitment service plan | planning |
| RUNTIME-DOMAIN-PR-4 | Validation integration and invariant enforcement plan | planning |
| RUNTIME-DOMAIN-PR-5 | Resource / consequence math service plan | planning |
| RUNTIME-DOMAIN-PR-6 | Combat / hazard / damage / recovery service plan | planning |
| RUNTIME-DOMAIN-PR-7 | Ability / effect / skill binding service plan | planning |
| RUNTIME-DOMAIN-PR-8 | Inventory / item / vehicle / asset service plan | planning |
| RUNTIME-DOMAIN-PR-9 | Mission / reward / clue routing service plan | planning |
| RUNTIME-DOMAIN-PR-10 | Social / faction / actor knowledge service plan | planning |
| RUNTIME-DOMAIN-PR-11 | Generated-content provenance service plan | planning |
| (post-domain review) | Post-domain planning review before live-play adapter or conversion pilot | gate |

This sequence is provisional and may be adjusted by RUNTIME-DOMAIN-PR-0.

---

## 9. Guardrail integrity review

The following remain **blocked** and are not authorized by any PR in the kernel skeleton sequence (PR-0 through PR-8):

- LLM state ownership
- LLM dice/RNG authority
- LLM event commitment
- LLM memory authority
- Narration as state
- Summaries as memory authority
- Hidden information exposure
- Generated content durability without provenance
- Domain services bypassing kernel envelopes
- Source-local content as canon
- Converted content as canon
- D-series / native-design content as direct runtime authority
- Prompt templates
- Model integration
- Live-play adapter
- UI runtime
- Training
- Pilot conversion
- Sourcebook inclusion
- Canon promotion

---

## 10. Domain-service dependency rules

The following dependency rules are **required** for all future domain services:

1. No domain service may mutate state directly without an approved state-store / state-delta pathway.
2. No domain service may commit events except through an approved event commitment pathway.
3. No domain service may roll randomness except through the deterministic RNG / table interface.
4. No domain service may expose hidden information except through context projection.
5. No domain service may persist data except through an approved persistence boundary.
6. No domain service may create durable generated content without provenance.
7. No domain service may use LLM output as validation authority.
8. No domain service may bypass runtime trace once trace integration is authorized.
9. No domain service may promote source-local content to canon.

---

## 11. Blocked-until ledger

| Item | Current status | Required predecessor | Earliest future PR family | Authorization status |
|------|---------------|---------------------|--------------------------|---------------------|
| Direct domain service implementation | blocked | RUNTIME-DOMAIN-PR-0 sequencing plan | RUNTIME-DOMAIN-PR-1+ | not_authorized |
| Command lifecycle / action legality implementation | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 | RUNTIME-DOMAIN-PR-1+ impl | not_authorized |
| State store implementation | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-2 | RUNTIME-DOMAIN-PR-2+ impl | not_authorized |
| Transaction lifecycle implementation | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-3 | RUNTIME-DOMAIN-PR-3+ impl | not_authorized |
| Event commitment implementation | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-3 | RUNTIME-DOMAIN-PR-3+ impl | not_authorized |
| Validation integration engine | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-4 | RUNTIME-DOMAIN-PR-4+ impl | not_authorized |
| Resource / consequence math service | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-5 | RUNTIME-DOMAIN-PR-5+ impl | not_authorized |
| Combat / hazard / damage / recovery service | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-6 | RUNTIME-DOMAIN-PR-6+ impl | not_authorized |
| Ability / effect / skill binding service | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-7 | RUNTIME-DOMAIN-PR-7+ impl | not_authorized |
| Inventory / item / vehicle / asset service | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-8 | RUNTIME-DOMAIN-PR-8+ impl | not_authorized |
| Mission / reward / clue routing service | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-9 | RUNTIME-DOMAIN-PR-9+ impl | not_authorized |
| Social / faction / actor knowledge service | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-10 | RUNTIME-DOMAIN-PR-10+ impl | not_authorized |
| Generated-content provenance service | blocked | RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-11 | RUNTIME-DOMAIN-PR-11+ impl | not_authorized |
| Context-packet compiler | blocked | RUNTIME-DOMAIN-PR-0, domain service foundation | post-DOMAIN-PR-11 | not_authorized |
| Prompt templates | blocked | Context-packet compiler | post-context-packet | not_authorized |
| Model integration | blocked | Prompt templates, model evaluation harness | post-model-evaluation | not_authorized |
| Model evaluation harness | blocked | Context-packet compiler | post-context-packet | not_authorized |
| Live-play adapter | blocked | All domain services, model integration | post-all-domain | not_authorized |
| UI runtime | blocked | Live-play adapter | post-live-play-adapter | not_authorized |
| Pilot conversion | blocked | Domain services, validation integration | post-domain-validation | not_authorized |
| Sourcebook inclusion | blocked | Pilot conversion gate | post-pilot-conversion | not_authorized |
| Canon promotion | blocked | Full domain + validation + provenance pipeline | post-full-pipeline | not_authorized |

---

## 12. Risk review

| # | Risk | Description | Affected RT owners | Mitigation | Must RUNTIME-DOMAIN-PR-0 address? |
|---|------|-------------|-------------------|------------|----------------------------------|
| 1 | Kernel bypass | Domain services call state/event/persistence directly instead of through kernel envelopes | RT-001 through RT-012 | Enforce kernel-dependency rules; integration tests verify all domain paths go through envelopes | Yes |
| 2 | Command/state/event collapse | Command, state delta, and event ledger responsibilities merge into a single service | RT-001, RT-002, RT-003 | Maintain separation defined in PR-2/PR-3; domain-service boundaries must preserve envelope identity | Yes |
| 3 | Hidden information leakage | Context projection exposes backend_hidden or redacted data to player-visible packets | RT-005, RT-007 | Non-leak integration tests; context-projection audit in every domain service that touches visibility | Yes |
| 4 | RNG nondeterminism | Domain services use Python random or other non-deterministic sources instead of kernel RNG | RT-009 | Enforce rng_interface as sole randomness source; ban stdlib random imports in domain code | Yes |
| 5 | State mutation without event trace | State changes occur without corresponding event ledger entries | RT-001, RT-002, RT-011 | Require every state delta to produce a traceable event; integration tests verify delta-to-event chain | Yes |
| 6 | Persistence side effects before storage decision | Domain services write to disk/database before persistence backend is chosen | RT-011, RT-012 | Persistence boundary prepare-only posture; no write methods until storage backend selected | Yes |
| 7 | Replay/hash audit irrelevance | Replay audit records created but never verified; hash chain becomes decorative | RT-011 | Replay verification tests in post-skeleton phase; hash-chain enforcement deferred but tracked | Yes |
| 8 | Validation becoming decorative | Validation pipeline exists but domain services skip it or treat failures as warnings | RT-011 | Validation integration service must enforce fail-stop for critical issues; quarantine pathway for warnings | Yes |
| 9 | Domain services importing donor assumptions | Domain logic embeds donor-system mechanics (D&D initiative, Pathfinder action economy) as Astra rules | RT-001 through RT-012 | Doctrine review of every domain service plan; no donor terminology without lexicon review | Yes |
| 10 | Generated content becoming durable without provenance | Generated narrative, descriptions, or NPC dialogue persisted without provenance tracking | RT-008 | Provenance service must wrap all generated content; no generated content durability without provenance record | Yes |
| 11 | LLM becoming de facto engine | Domain services delegate game-mechanical decisions to LLM output | RT-001 through RT-012 | LLM non-authority adversarial tests; validation rejects LLM-sourced state mutations | Yes |
| 12 | Context-packet compiler leaking hidden state | Packet assembly includes backend_hidden fields in model-facing context | RT-005 | Non-leak integration tests; context-packet compiler must use context_projection filtering | Yes |
| 13 | Live-play launching before backend truth is authoritative | Live-play sessions begin before domain services and validation are operational | All RT owners | Live-play adapter gate requires all domain services, validation, and model evaluation to pass | Yes |
| 14 | Conversion records landing before state/validation/domain surfaces are ready | Converted donor material imported into runtime before state and validation surfaces exist | RT-012, RT-008 | Conversion remains blocked until domain services, validation integration, and provenance pipeline are operational | Yes |

---

## 13. Future integration test families

The following test families are needed after the skeleton phase. **PR-8 only identifies these families; it does not implement them.**

1. **Kernel import/export integrity tests** — verify all 14 kernel modules export correctly through `__init__.py` and can be imported independently.
2. **Cross-envelope reference tests** — verify command_id flows from CommandEnvelope → TransactionPreview → StateDeltaEnvelope → EventLedgerEntry.
3. **Command to preview to delta to event reference-chain tests** — verify the full reference chain is traceable from a command through to its event record.
4. **RNG invocation to event metadata trace tests** — verify RNGResult metadata appears in corresponding event ledger entries.
5. **Table/oracle deterministic selection trace tests** — verify TableOracleResult is deterministic for identical seed/roll/table inputs and traceable.
6. **Validation result to event/quarantine pathway tests** — verify ValidationResult routes correctly to event commitment or quarantine.
7. **Hidden-info projection non-leak integration tests** — verify context_projection never includes backend_hidden or redacted records in player-visible output.
8. **Persistence boundary no-write tests** — verify persistence boundary prepare-only posture produces no file I/O or database writes.
9. **Replay/hash deterministic canonical payload tests** — verify canonical_payload_hash produces identical hashes for semantically identical payloads.
10. **Runtime trace reference completeness tests** — verify every kernel operation produces a corresponding RuntimeTraceEntry.
11. **Domain-service kernel-dependency tests** — verify domain services import only from kernel interfaces, not from internal kernel implementation.
12. **LLM non-authority adversarial tests** — verify validation rejects state mutations sourced from LLM output.
13. **Generated-content provenance tests** — verify all generated content carries provenance records.
14. **Source-local/canon boundary tests** — verify source-local content cannot be promoted to canon without explicit doctrine review.

PR-8 only identifies these future integration test families and adds focused doctrine tests for this gate.

---

## 14. Non-implementation reaffirmation

This PR adds **none** of the following:

- Runtime code
- Domain services
- Command execution
- State store
- State mutation
- Transaction lifecycle engine
- Event commitment
- Durable persistence
- File writer/reader
- Database schema
- Replay engine
- Hash-chain enforcement engine
- Trace store
- Telemetry backend
- Context-packet compiler
- Prompt templates
- Model integration
- Model routing
- Live-play adapter
- UI/client
- Generator implementation
- Training data
- Donor-content audit
- Pilot conversion authorization
- Sourcebook inclusion authorization
- Canon promotion

---

## 15. Classification block

```yaml
runtime_impl_pr_8:
  review_id: RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001
  artifact_type: post_kernel_skeleton_review_and_domain_service_readiness_gate
  implementation_status: non_executable_review_gate
  derives_from:
    - RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
    - RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001
    - RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
    - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
    - RUNTIME-IMPL-PR-4-DETERMINISTIC-RNG-TABLE-ORACLE-INTERFACE-SKELETON-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
    - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
    - RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001
  confirms_minimum_backend_kernel_skeleton_complete: true
  confirms_ready_for_domain_service_planning: true
  authorizes_domain_service_code_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_state_store_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_event_commitment_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_context_packet_compiler_by_this_pr: false
  authorizes_prompt_templates_by_this_pr: false
  authorizes_model_integration_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RUNTIME-DOMAIN-PR-0 domain service implementation sequencing plan, pending review
```

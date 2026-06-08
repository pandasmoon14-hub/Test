# RUNTIME-DOMAIN-PR-0: Domain Service Implementation Sequencing Plan

## 1. Purpose and status

This document is **RUNTIME-DOMAIN-PR-0**, a planning-only domain service implementation sequencing plan.

- **Type:** planning-only, non-executable.
- **Follows:** RUNTIME-IMPL-PR-8 (post-kernel skeleton review and domain-service readiness gate).
- **Authorizes:** future domain-service planning and sequencing decisions only.
- **Does not authorize:** domain-service code, command execution, action legality engine, state store, state mutation, transaction lifecycle engine, event commitment, event store persistence, durable persistence, database schemas, replay engine, context-packet compiler, prompt templates, model integration, model routing, live-play adapter, UI/client, generators, training data, donor conversion, sourcebook inclusion, or canon promotion.

---

## 2. Source ledger

### Primary gate source

| Source ID | Title | Path |
|-----------|-------|------|
| RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001 | Post-kernel skeleton review and domain-service readiness gate | `docs/doctrine/reviews/runtime_impl_pr_8_post_kernel_skeleton_review_domain_service_readiness_gate.md` |

### Implementation plans (RUNTIME-IMPL-PR-0 through PR-7)

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

### Runtime sequence planning sources (RUNTIME-SEQ-PR-A through PR-F)

| Source ID | Title |
|-----------|-------|
| RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001 | Minimum backend kernel and runtime quality contract plan |
| RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001 | Narration / context packet contract plan |
| RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001 | State / event / invariant / transaction plan |
| RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001 | Story-capable structure and playable-content plan |
| RUNTIME-SEQ-PR-E-MODEL-EVALUATION-STRUCTURED-OUTPUT-ADVERSARIAL-COMMAND-PLAN-001 | Model evaluation, structured-output, and adversarial-command plan |
| RUNTIME-SEQ-PR-F-IMPLEMENTATION-READINESS-EXECUTABLE-KERNEL-AUTHORIZATION-GATE-001 | Implementation-readiness review and executable kernel authorization gate |

### Owner specifications (RT-001 through RT-012)

| Spec ID | Title | Path |
|---------|-------|------|
| RT-001 | Command lifecycle and action legality | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md` |
| RT-002 | Resource / consequence math | `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md` |
| RT-003 | Combat / hazard / damage / recovery | `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md` |
| RT-004 | Ability / effect / skill binding | `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md` |
| RT-005 | Context packet and hidden information | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md` |
| RT-006 | Mission / reward / clue routing | `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md` |
| RT-007 | Social / faction / actor knowledge | `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md` |
| RT-008 | Generated content provenance and recurrence | `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md` |
| RT-009 | Runtime RNG and table/oracle | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md` |
| RT-010 | Inventory / item / vehicle / asset | `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md` |
| RT-011 | Validation readiness and tooling | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md` |
| RT-012 | D-series promotion boundary | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md` |

### Implemented kernel skeleton modules

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

### Runtime skeleton tests

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

### Domain-service implication

Domain services must consume kernel interfaces. No service may bypass command envelopes, transaction previews, state deltas, event ledger entries, deterministic RNG/table interfaces, validation results, hidden-info projection, persistence boundaries, replay/hash audit, or runtime trace.

---

## 4. Domain-service sequencing thesis

Domain services must be implemented in dependency order. Services that own command legality, state ownership, transaction lifecycle, event commitment, and validation integration must precede services that implement combat, abilities, missions, inventory, factions, generated content, model-facing packets, or live-play.

### Recommended conclusion

- RUNTIME-DOMAIN-PR-1 should plan command lifecycle/action legality.
- RUNTIME-DOMAIN-PR-2 should plan state store/state projection.
- RUNTIME-DOMAIN-PR-3 should plan transaction lifecycle/event commitment.
- RUNTIME-DOMAIN-PR-4 should plan validation integration/invariant enforcement.
- Runtime math/content domain services should follow after those foundations.

---

## 5. Domain-service family inventory

| Service family | Primary RT owner | Secondary RT owners | Required kernel dependencies | Blocked upstream dependencies | Allowed responsibilities | Forbidden responsibilities | Earliest allowed PR family | Direct implementation authorized now |
|---------------|-----------------|--------------------|-----------------------------|------------------------------|--------------------------|---------------------------|---------------------------|-------------------------------------|
| Command lifecycle / action legality | RT-001 | RT-011 | command_envelope, transaction_preview, validation_pipeline, runtime_trace | none (first foundation service) | Command parsing, legality checks, cost prechecks, command routing | State mutation, event commitment, resource math, combat rules | RUNTIME-DOMAIN-PR-1 | false |
| State store / state projection | RT-001, RT-011 | RT-002, RT-005 | state_delta, event_ledger, persistence_boundary, schema_registry, record_identity, runtime_trace | Command lifecycle | State read, state projection, delta application, snapshot | Direct event commitment, bypass persistence boundary, expose hidden info | RUNTIME-DOMAIN-PR-2 | false |
| Transaction lifecycle / event commitment | RT-001 | RT-011, RT-002 | command_envelope, transaction_preview, state_delta, event_ledger, persistence_boundary, replay_audit, runtime_trace | Command lifecycle, state store | Transaction open/commit/rollback, event append, hash chain | State mutation without delta, bypass validation, bypass persistence | RUNTIME-DOMAIN-PR-3 | false |
| Validation integration / invariant enforcement | RT-011 | RT-001, RT-002 | validation_pipeline, state_delta, command_envelope, runtime_trace | Command lifecycle, state store, transaction lifecycle | Domain-specific validation rules, invariant checks, quarantine routing | Bypass transaction lifecycle, direct event commitment, LLM authority | RUNTIME-DOMAIN-PR-4 | false |
| Resource / consequence math | RT-002 | RT-001, RT-003, RT-009 | state_delta, rng_interface, validation_pipeline, command_envelope, runtime_trace | Command lifecycle, state store, transaction lifecycle, validation integration | Cost calculation, resource change, consequence math | Direct state mutation, direct event commitment, bypass validation | RUNTIME-DOMAIN-PR-5 | false |
| Combat / hazard / damage / recovery | RT-003 | RT-002, RT-004, RT-009 | state_delta, rng_interface, table_oracle, validation_pipeline, command_envelope, runtime_trace | Resource/consequence math | Damage calculation, hazard exposure, recovery checks, combat state | Direct state mutation, direct event commitment, bypass resource math | RUNTIME-DOMAIN-PR-6 | false |
| Ability / effect / skill binding | RT-004 | RT-002, RT-003, RT-009 | schema_registry, record_identity, state_delta, rng_interface, validation_pipeline, command_envelope, runtime_trace | Resource/consequence math | Effect resolution, skill checks, prerequisite checks, cooldown tracking | Direct state mutation, bypass resource/combat, create canon abilities | RUNTIME-DOMAIN-PR-7 | false |
| Inventory / item / vehicle / asset | RT-010 | RT-002, RT-004, RT-009 | schema_registry, record_identity, state_delta, validation_pipeline, command_envelope, persistence_boundary, runtime_trace | Resource/consequence math, ability/effect | Item state, custody, durability, cargo, loadout | Direct state mutation, bypass persistence boundary, bypass validation | RUNTIME-DOMAIN-PR-8 | false |
| Mission / reward / clue routing | RT-006 | RT-001, RT-005, RT-007, RT-008 | state_delta, event_ledger, hidden_information, context_projection, validation_pipeline, command_envelope, runtime_trace | State store, transaction lifecycle, validation integration | Objective state, clue visibility, reward routing, branch selection | Direct state mutation, expose hidden truths, bypass validation | RUNTIME-DOMAIN-PR-9 | false |
| Social / faction / actor knowledge | RT-007 | RT-005, RT-006, RT-008 | hidden_information, context_projection, state_delta, validation_pipeline, command_envelope, runtime_trace | State store, validation integration | Reputation tracking, relationship state, faction standing, actor knowledge | Expose hidden knowledge, direct state mutation, bypass validation | RUNTIME-DOMAIN-PR-10 | false |
| Generated-content provenance / recurrence | RT-008 | RT-009, RT-011, RT-012 | runtime_trace, replay_audit, schema_registry, record_identity, persistence_boundary, rng_interface | State store, transaction lifecycle | Provenance tracking, recurrence eligibility, stable ID assignment | Durable content without provenance, canon promotion, bypass persistence | RUNTIME-DOMAIN-PR-11 | false |
| Context-packet compiler | RT-005 | RT-007, RT-008, RT-011 | context_projection, hidden_information, schema_registry, record_identity, runtime_trace | All domain services that produce visible state | Packet assembly, visibility filtering, budget enforcement | Expose hidden info, bypass context projection, include unvalidated state | RUNTIME-DOMAIN-PR-12 | false |
| Model evaluation harness | RT-011 | RT-005, RT-008 | context_projection, runtime_trace, validation_pipeline | Context-packet compiler | Model behavior evaluation, structured-output validation, adversarial tests | Become validation authority, bypass backend truth, commit state | RUNTIME-DOMAIN-PR-13 | false |
| Live-play adapter gate | All RT owners | — | All kernel modules | All domain services, context-packet compiler, model evaluation | Session management, input routing, output delivery | Bypass any kernel interface, LLM authority over state | RUNTIME-DOMAIN-PR-14 | false |

---

## 6. Recommended future PR sequence

| PR ID | Title | Type |
|-------|-------|------|
| RUNTIME-DOMAIN-PR-0 | Domain service implementation sequencing plan | planning |
| RUNTIME-DOMAIN-PR-1 | Command lifecycle and action legality service plan | planning |
| RUNTIME-DOMAIN-PR-2 | State store and state projection service plan | planning |
| RUNTIME-DOMAIN-PR-3 | Transaction lifecycle and event commitment service plan | planning |
| RUNTIME-DOMAIN-PR-4 | Validation integration and invariant enforcement service plan | planning |
| RUNTIME-DOMAIN-PR-5 | Resource and consequence math service plan | planning |
| RUNTIME-DOMAIN-PR-6 | Combat, hazard, damage, and recovery service plan | planning |
| RUNTIME-DOMAIN-PR-7 | Ability, effect, and skill binding service plan | planning |
| RUNTIME-DOMAIN-PR-8 | Inventory, item, vehicle, and asset service plan | planning |
| RUNTIME-DOMAIN-PR-9 | Mission, reward, and clue routing service plan | planning |
| RUNTIME-DOMAIN-PR-10 | Social, faction, and actor knowledge service plan | planning |
| RUNTIME-DOMAIN-PR-11 | Generated-content provenance and recurrence service plan | planning |
| RUNTIME-DOMAIN-PR-12 | Context-packet compiler plan | planning |
| RUNTIME-DOMAIN-PR-13 | Model evaluation harness plan | planning |
| RUNTIME-DOMAIN-PR-14 | Live-play adapter gate plan | planning |
| RUNTIME-DOMAIN-PR-15 | Post-domain-service planning review | gate |

Each plan may authorize a later narrow implementation PR only after its own review.

---

## 7. Per-PR scope boundaries

### RUNTIME-DOMAIN-PR-1: Command lifecycle and action legality service plan

- **Purpose:** Plan the command lifecycle and action legality service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0.
- **Allowed planning scope:** Command parsing, legality determination, cost prechecks, command routing, command rejection, action legality rules, command-to-transaction handoff.
- **Forbidden scope:** Command execution code, action legality engine code, state mutation, transaction lifecycle, event commitment, resource math, combat rules, ability effects, live-play adapter, model calls, prompt templates.
- **Kernel interfaces it must consume:** command_envelope, transaction_preview, validation_pipeline, runtime_trace.
- **Tests it must require:** Command envelope consumption tests, legality check interface tests, validation pipeline integration tests, no-state-mutation tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-2: State store and state projection service plan

- **Purpose:** Plan the state store and state projection service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1.
- **Allowed planning scope:** State read patterns, state projection interfaces, delta application rules, snapshot mechanics, state indexing, state-to-event reference patterns.
- **Forbidden scope:** State store implementation, database schema, state mutation engine, event commitment, persistence backend selection, live-play state.
- **Kernel interfaces it must consume:** state_delta, event_ledger, persistence_boundary, schema_registry, record_identity, runtime_trace.
- **Tests it must require:** State projection interface tests, delta-to-state reference chain tests, persistence boundary consumption tests, no-direct-write tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-3: Transaction lifecycle and event commitment service plan

- **Purpose:** Plan the transaction lifecycle and event commitment service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1, RUNTIME-DOMAIN-PR-2.
- **Allowed planning scope:** Transaction open/commit/rollback patterns, event append rules, hash-chain commitment rules, validation gating, event ordering, replay-safe event references.
- **Forbidden scope:** Transaction engine implementation, event commitment engine, durable persistence, database schema, replay engine, state mutation implementation.
- **Kernel interfaces it must consume:** command_envelope, transaction_preview, state_delta, event_ledger, persistence_boundary, replay_audit, runtime_trace.
- **Tests it must require:** Transaction lifecycle state machine tests, event commitment precondition tests, hash-chain reference tests, rollback safety tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-4: Validation integration and invariant enforcement service plan

- **Purpose:** Plan the validation integration and invariant enforcement service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1, RUNTIME-DOMAIN-PR-2, RUNTIME-DOMAIN-PR-3.
- **Allowed planning scope:** Domain-specific validation rule registration, invariant check patterns, quarantine routing, validation result gating, fail-stop vs. warning severity routing.
- **Forbidden scope:** Validation rule implementation, invariant engine, domain-specific rule sets, command execution, event commitment, live-play validation.
- **Kernel interfaces it must consume:** validation_pipeline, state_delta, command_envelope, runtime_trace.
- **Tests it must require:** Validation registration interface tests, quarantine routing tests, severity-based gating tests, no-decorative-validation tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-5: Resource and consequence math service plan

- **Purpose:** Plan the resource and consequence math service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 through PR-4.
- **Allowed planning scope:** Cost calculation interfaces, resource change patterns, consequence routing, backlash/corruption/strain math boundaries, reward/loss boundaries.
- **Forbidden scope:** Math implementation, resource formulas, cost tables, damage tables, reward economy, direct state mutation, event commitment.
- **Kernel interfaces it must consume:** state_delta, rng_interface, validation_pipeline, command_envelope, runtime_trace.
- **Tests it must require:** Resource interface tests, consequence routing tests, RNG consumption tests, validation integration tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-6: Combat, hazard, damage, and recovery service plan

- **Purpose:** Plan the combat, hazard, damage, and recovery service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 through PR-5.
- **Allowed planning scope:** Damage calculation interfaces, hazard exposure boundaries, recovery patterns, combat state boundaries, encounter state pressure.
- **Forbidden scope:** Combat rules implementation, damage formulas, injury tables, condition system, healing formulas, initiative/action economy, monster schema.
- **Kernel interfaces it must consume:** state_delta, rng_interface, table_oracle, validation_pipeline, command_envelope, runtime_trace.
- **Tests it must require:** Damage interface tests, RNG/table consumption tests, validation integration tests, resource math handoff tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-7: Ability, effect, and skill binding service plan

- **Purpose:** Plan the ability, effect, and skill binding service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 through PR-5.
- **Allowed planning scope:** Effect resolution interfaces, skill check patterns, prerequisite check boundaries, cooldown/recharge boundaries, targeting/range/area/duration boundaries.
- **Forbidden scope:** Ability system implementation, effect taxonomy, skill system, proficiency system, prerequisite system, targeting rules, scaling/rank/tier rules.
- **Kernel interfaces it must consume:** schema_registry, record_identity, state_delta, rng_interface, validation_pipeline, command_envelope, runtime_trace.
- **Tests it must require:** Effect interface tests, skill check interface tests, schema registry consumption tests, validation integration tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-8: Inventory, item, vehicle, and asset service plan

- **Purpose:** Plan the inventory, item, vehicle, and asset service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 through PR-5, RUNTIME-DOMAIN-PR-7.
- **Allowed planning scope:** Item state interfaces, custody patterns, durability boundaries, cargo/loadout boundaries, asset reward/loss routing.
- **Forbidden scope:** Inventory system implementation, item schema, vehicle schema, crafting system, repair/salvage system, asset economy, price/value tables.
- **Kernel interfaces it must consume:** schema_registry, record_identity, state_delta, validation_pipeline, command_envelope, persistence_boundary, runtime_trace.
- **Tests it must require:** Item state interface tests, custody tracking tests, persistence boundary consumption tests, validation integration tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-9: Mission, reward, and clue routing service plan

- **Purpose:** Plan the mission, reward, and clue routing service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 through PR-4.
- **Allowed planning scope:** Objective state interfaces, clue visibility boundaries, reward routing patterns, branch selection boundaries, scenario state patterns.
- **Forbidden scope:** Mission system implementation, quest engine, scenario engine, clue reveal algorithm, reward economy, mission reward tables, objective state machine.
- **Kernel interfaces it must consume:** state_delta, event_ledger, hidden_information, context_projection, validation_pipeline, command_envelope, runtime_trace.
- **Tests it must require:** Objective state interface tests, hidden-information consumption tests, clue visibility tests, validation integration tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-10: Social, faction, and actor knowledge service plan

- **Purpose:** Plan the social, faction, and actor knowledge service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 through PR-4.
- **Allowed planning scope:** Reputation tracking interfaces, relationship state boundaries, faction standing patterns, actor knowledge boundaries, hidden knowledge routing.
- **Forbidden scope:** Social system implementation, faction system, reputation system, relationship engine, actor-knowledge database, dialogue system.
- **Kernel interfaces it must consume:** hidden_information, context_projection, state_delta, validation_pipeline, command_envelope, runtime_trace.
- **Tests it must require:** Hidden-information consumption tests, actor knowledge visibility tests, faction standing interface tests, validation integration tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-11: Generated-content provenance and recurrence service plan

- **Purpose:** Plan the generated-content provenance and recurrence service.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 through PR-4.
- **Allowed planning scope:** Provenance tracking interfaces, recurrence eligibility boundaries, stable ID assignment patterns, review requirements, generator-disablement posture.
- **Forbidden scope:** Generator implementation, procedural generation engine, generated content records, durable generated records, stable ID allocator, recurrence engine, content writer.
- **Kernel interfaces it must consume:** runtime_trace, replay_audit, schema_registry, record_identity, persistence_boundary, rng_interface.
- **Tests it must require:** Provenance interface tests, recurrence eligibility tests, stable ID pattern tests, no-durability-without-provenance tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-12: Context-packet compiler plan

- **Purpose:** Plan the context-packet compiler.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 through PR-11.
- **Allowed planning scope:** Packet assembly interfaces, visibility filtering patterns, budget enforcement boundaries, model-facing packet structure.
- **Forbidden scope:** Context-packet compiler implementation, prompt templates, model integration, narration render packet compiler, redaction algorithm.
- **Kernel interfaces it must consume:** context_projection, hidden_information, schema_registry, record_identity, runtime_trace.
- **Tests it must require:** Non-leak projection tests, visibility filtering tests, budget enforcement interface tests, hidden-info exclusion tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-13: Model evaluation harness plan

- **Purpose:** Plan the model evaluation harness.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-12.
- **Allowed planning scope:** Model behavior evaluation interfaces, structured-output validation patterns, adversarial test corpus boundaries, role qualification patterns.
- **Forbidden scope:** Model evaluation code, benchmark runner, prompt templates, model routing, model adapter, adversarial test harness, metamorphic test runner.
- **Kernel interfaces it must consume:** context_projection, runtime_trace, validation_pipeline.
- **Tests it must require:** Evaluation interface tests, structured-output validation tests, non-authority verification tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-14: Live-play adapter gate plan

- **Purpose:** Plan the live-play adapter gate.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 through PR-13.
- **Allowed planning scope:** Session management interfaces, input routing boundaries, output delivery boundaries, adapter requirements, all-service integration gate criteria.
- **Forbidden scope:** Live-play adapter implementation, UI/client, session engine, input parser, model calls.
- **Kernel interfaces it must consume:** All 14 kernel modules.
- **Tests it must require:** Full integration gate tests, all-service availability tests, kernel-consumption completeness tests.
- **Exit criteria:** Planning document reviewed and approved; no implementation code created.

### RUNTIME-DOMAIN-PR-15: Post-domain-service planning review

- **Purpose:** Review all domain-service plans and authorize narrow implementation PRs.
- **Required predecessors:** RUNTIME-DOMAIN-PR-0, RUNTIME-DOMAIN-PR-1 through PR-14.
- **Allowed planning scope:** Coverage review, gap analysis, implementation authorization decisions.
- **Forbidden scope:** Implementation code, domain services, live-play, training, conversion.
- **Kernel interfaces it must consume:** None directly; reviews all prior plans.
- **Tests it must require:** Coverage completeness tests, authorization boundary tests.
- **Exit criteria:** All domain-service plans reviewed; authorized implementation sequence defined.

---

## 8. Immediate next PR authorization boundary

**RUNTIME-DOMAIN-PR-1** may create only:

- A planning document for command lifecycle and action legality service.
- Registry update.
- Decision-log update.
- Focused doctrine/review tests.

**RUNTIME-DOMAIN-PR-1 must not implement:**

- Command execution code.
- Action legality engine code.
- Command parser.
- State mutation.
- Transaction lifecycle.
- Event commitment.
- Resource math.
- Combat rules.
- Ability effects.
- Live-play adapter.
- Model calls.
- Prompt templates.

---

## 9. Domain-service dependency rules

The following rules are **strict** and apply to all future domain services:

1. No direct state mutation — all state changes must flow through state_delta and the approved state-store pathway.
2. No direct event commitment — all events must be committed through the approved transaction lifecycle and event commitment pathway.
3. No RNG/table bypass — all randomness must use rng_interface; all table/oracle selections must use table_oracle. No stdlib `random` imports in domain code.
4. No hidden-info exposure outside context projection — all visibility filtering must use context_projection and hidden_information interfaces.
5. No durable persistence outside persistence boundary — all writes must flow through persistence_boundary prepare-only posture until storage backend is selected.
6. No generated content durability without provenance — all generated content must carry provenance records via runtime_trace and replay_audit.
7. No LLM output as validation authority — validation_pipeline results gate transactions; LLM output is never validation.
8. No runtime trace bypass once trace integration is authorized — all domain operations must produce RuntimeTraceEntry records.
9. No source-local content canon promotion — source-local material remains source-local until explicit doctrine review.
10. No donor assumptions silently becoming Astra baseline — donor-system mechanics must not enter domain services without lexicon review.
11. No domain service importing doctrine files as runtime truth without approved schema/registry path — domain services consume kernel interfaces, not raw doctrine documents.

---

## 10. Kernel dependency matrix

| Service family | schema_registry | record_identity | command_envelope | transaction_preview | state_delta | event_ledger | rng_interface | table_oracle | validation_pipeline | hidden_information | context_projection | persistence_boundary | replay_audit | runtime_trace |
|---------------|----------------|----------------|-----------------|--------------------|-----------:|-------------:|-------------:|------------:|-------------------:|-------------------:|-------------------:|--------------------:|-------------:|-------------:|
| Command lifecycle / action legality | optional | optional | required | required | not_applicable | not_applicable | not_applicable | not_applicable | required | not_applicable | not_applicable | not_applicable | not_applicable | required |
| State store / state projection | required | required | not_applicable | not_applicable | required | required | not_applicable | not_applicable | optional | not_applicable | not_applicable | required | optional | required |
| Transaction lifecycle / event commitment | not_applicable | not_applicable | required | required | required | required | not_applicable | not_applicable | required | not_applicable | not_applicable | required | required | required |
| Validation integration / invariant enforcement | optional | optional | required | not_applicable | required | not_applicable | not_applicable | not_applicable | required | not_applicable | not_applicable | not_applicable | not_applicable | required |
| Resource / consequence math | optional | optional | required | optional | required | not_applicable | required | optional | required | not_applicable | not_applicable | not_applicable | not_applicable | required |
| Combat / hazard / damage / recovery | optional | optional | required | optional | required | not_applicable | required | required | required | not_applicable | not_applicable | not_applicable | not_applicable | required |
| Ability / effect / skill binding | required | required | required | optional | required | not_applicable | required | optional | required | not_applicable | not_applicable | not_applicable | not_applicable | required |
| Inventory / item / vehicle / asset | required | required | required | optional | required | not_applicable | optional | optional | required | optional | not_applicable | required | not_applicable | required |
| Mission / reward / clue routing | optional | optional | required | optional | required | required | optional | optional | required | required | required | not_applicable | not_applicable | required |
| Social / faction / actor knowledge | optional | optional | required | optional | required | not_applicable | not_applicable | not_applicable | required | required | required | not_applicable | not_applicable | required |
| Generated-content provenance / recurrence | required | required | not_applicable | not_applicable | not_applicable | not_applicable | required | optional | optional | not_applicable | not_applicable | required | required | required |
| Context-packet compiler | required | required | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable | required | required | not_applicable | not_applicable | required |
| Model evaluation harness | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable | required | not_applicable | required | not_applicable | not_applicable | required |
| Live-play adapter gate | required | required | required | required | required | required | required | required | required | required | required | required | required | required |

---

## 11. Blocked-until ledger

| Item | Current status | Required predecessor | Earliest possible PR | Authorized by this PR |
|------|---------------|---------------------|---------------------|----------------------|
| Command lifecycle implementation | blocked | RUNTIME-DOMAIN-PR-1 plan + review | post-RUNTIME-DOMAIN-PR-1 impl | false |
| State store implementation | blocked | RUNTIME-DOMAIN-PR-2 plan + review | post-RUNTIME-DOMAIN-PR-2 impl | false |
| Transaction lifecycle implementation | blocked | RUNTIME-DOMAIN-PR-3 plan + review | post-RUNTIME-DOMAIN-PR-3 impl | false |
| Event commitment implementation | blocked | RUNTIME-DOMAIN-PR-3 plan + review | post-RUNTIME-DOMAIN-PR-3 impl | false |
| Validation integration implementation | blocked | RUNTIME-DOMAIN-PR-4 plan + review | post-RUNTIME-DOMAIN-PR-4 impl | false |
| Resource math implementation | blocked | RUNTIME-DOMAIN-PR-5 plan + review | post-RUNTIME-DOMAIN-PR-5 impl | false |
| Combat implementation | blocked | RUNTIME-DOMAIN-PR-6 plan + review | post-RUNTIME-DOMAIN-PR-6 impl | false |
| Ability/effect implementation | blocked | RUNTIME-DOMAIN-PR-7 plan + review | post-RUNTIME-DOMAIN-PR-7 impl | false |
| Inventory/asset implementation | blocked | RUNTIME-DOMAIN-PR-8 plan + review | post-RUNTIME-DOMAIN-PR-8 impl | false |
| Mission/clue implementation | blocked | RUNTIME-DOMAIN-PR-9 plan + review | post-RUNTIME-DOMAIN-PR-9 impl | false |
| Social/faction implementation | blocked | RUNTIME-DOMAIN-PR-10 plan + review | post-RUNTIME-DOMAIN-PR-10 impl | false |
| Generated-content provenance implementation | blocked | RUNTIME-DOMAIN-PR-11 plan + review | post-RUNTIME-DOMAIN-PR-11 impl | false |
| Context-packet compiler implementation | blocked | RUNTIME-DOMAIN-PR-12 plan + review | post-RUNTIME-DOMAIN-PR-12 impl | false |
| Model evaluation harness implementation | blocked | RUNTIME-DOMAIN-PR-13 plan + review | post-RUNTIME-DOMAIN-PR-13 impl | false |
| Live-play adapter implementation | blocked | RUNTIME-DOMAIN-PR-14 plan + review | post-RUNTIME-DOMAIN-PR-14 impl | false |
| UI runtime | blocked | Live-play adapter implementation | post-live-play-adapter | false |
| Pilot conversion | blocked | Domain services + validation integration | post-domain-validation | false |
| Sourcebook inclusion | blocked | Pilot conversion gate | post-pilot-conversion | false |
| Canon promotion | blocked | Full domain + validation + provenance pipeline | post-full-pipeline | false |

---

## 12. Risk review

| # | Risk | Affected RT owner(s) | Mitigation | Future PR that must address it | Test family required |
|---|------|---------------------|------------|-------------------------------|---------------------|
| 1 | Domain services bypass kernel envelopes | RT-001 through RT-012 | Enforce kernel-dependency rules; integration tests verify all domain paths go through envelopes | RUNTIME-DOMAIN-PR-1 through PR-14 (each plan) | Kernel-dependency consumption tests |
| 2 | Command/state/event collapse | RT-001, RT-002, RT-003 | Maintain separation defined in PR-2/PR-3; domain-service boundaries must preserve envelope identity | RUNTIME-DOMAIN-PR-1, PR-2, PR-3 | Envelope identity preservation tests |
| 3 | Hidden info leakage | RT-005, RT-007 | Non-leak integration tests; context-projection audit in every domain service that touches visibility | RUNTIME-DOMAIN-PR-9, PR-10, PR-12 | Hidden-info projection non-leak tests |
| 4 | RNG nondeterminism | RT-009 | Enforce rng_interface as sole randomness source; ban stdlib random imports in domain code | RUNTIME-DOMAIN-PR-5, PR-6, PR-7 | Deterministic RNG consumption tests |
| 5 | Event commitment without validation | RT-001, RT-011 | Require validation result gating before event commitment; fail-stop for critical issues | RUNTIME-DOMAIN-PR-3, PR-4 | Validation-gated commitment tests |
| 6 | State mutation without trace | RT-001, RT-002, RT-011 | Require every state delta to produce a traceable event and RuntimeTraceEntry | RUNTIME-DOMAIN-PR-2, PR-3 | Delta-to-event-to-trace chain tests |
| 7 | Persistence side effects before backend choice | RT-011, RT-012 | Persistence boundary prepare-only posture; no write methods until storage backend selected | RUNTIME-DOMAIN-PR-2, PR-3 | Persistence boundary no-write tests |
| 8 | Validation becoming decorative | RT-011 | Validation integration service must enforce fail-stop for critical issues; quarantine pathway for warnings | RUNTIME-DOMAIN-PR-4 | Validation enforcement tests |
| 9 | Generated content becoming durable without provenance | RT-008 | Provenance service must wrap all generated content; no generated content durability without provenance record | RUNTIME-DOMAIN-PR-11 | Generated-content provenance tests |
| 10 | Donor assumptions entering runtime services | RT-001 through RT-012 | Doctrine review of every domain service plan; no donor terminology without lexicon review | RUNTIME-DOMAIN-PR-1 through PR-14 | Source-local/canon boundary tests |
| 11 | Context-packet compiler built too early | RT-005, RT-011 | Context-packet compiler plan (PR-12) requires all upstream domain services to be planned first | RUNTIME-DOMAIN-PR-12 | Dependency ordering tests |
| 12 | Model integration becoming authority | RT-001 through RT-012 | LLM non-authority adversarial tests; validation rejects LLM-sourced state mutations | RUNTIME-DOMAIN-PR-13 | LLM non-authority adversarial tests |
| 13 | Live-play before backend truth is operational | All RT owners | Live-play adapter gate requires all domain services, validation, and model evaluation to pass | RUNTIME-DOMAIN-PR-14 | Full integration gate tests |
| 14 | Conversion landing before runtime services are ready | RT-012, RT-008 | Conversion remains blocked until domain services, validation integration, and provenance pipeline are operational | RUNTIME-DOMAIN-PR-15 (review) | Blocked-until ledger enforcement tests |

---

## 13. Future integration test plan

The following cross-service and kernel-domain integration tests are needed in future PRs. **This PR only identifies them; it does not implement them.**

1. **Command envelope to action legality result** — verify a CommandEnvelope is consumed by the action legality service and produces a legality determination without state mutation.
2. **Command to transaction preview to state delta to event ledger chain** — verify the full reference chain is traceable from a command through transaction preview, state delta, to event ledger entry.
3. **State store projection from event/delta references** — verify state projection correctly resolves current state from event/delta references without side effects.
4. **Validation result gating transaction/event commitment** — verify ValidationResult with critical severity blocks transaction commitment and routes to quarantine.
5. **Deterministic RNG/table references in events** — verify RNGResult and TableOracleResult metadata appears in corresponding event ledger entries for replay determinism.
6. **Hidden-info projection non-leak tests** — verify context_projection never includes backend_hidden or redacted records in player-visible output.
7. **Persistence boundary no-direct-write tests** — verify persistence boundary prepare-only posture produces no file I/O or database writes.
8. **Replay/hash audit deterministic chain tests** — verify canonical_payload_hash produces identical hashes for semantically identical payloads and chain is verifiable.
9. **Runtime trace completeness tests** — verify every kernel operation and domain service operation produces a corresponding RuntimeTraceEntry.
10. **Generated-content provenance tests** — verify all generated content carries provenance records before durability is allowed.
11. **LLM non-authority adversarial tests** — verify validation rejects state mutations sourced from LLM output; verify LLM cannot bypass command envelope.
12. **Source-local/canon boundary tests** — verify source-local content cannot be promoted to canon without explicit doctrine review; verify no donor terminology enters domain services without lexicon review.

---

## 14. Non-implementation reaffirmation

This PR adds **none** of the following:

- Runtime code
- Domain-service code
- Command execution
- Action legality engine
- State store
- State mutation
- Transaction lifecycle engine
- Event commitment
- Event store persistence
- Durable persistence
- Database schema
- Replay engine
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

## 15. Gate finding

```yaml
gate_finding:
  domain_service_sequence_defined: true
  ready_for_runtime_domain_pr_1_planning: true
  domain_service_code_authorized_by_this_pr: false
  command_execution_authorized_by_this_pr: false
  state_store_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-1 command lifecycle and action legality service plan
  next_step_status: planning_only
```

---

## 16. Classification block

```yaml
runtime_domain_pr_0:
  review_id: RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001
  artifact_type: domain_service_implementation_sequencing_plan
  implementation_status: non_executable_plan
  derives_from:
    - RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001
    - RUNTIME-IMPL-PR-0-MINIMUM-BACKEND-KERNEL-EXECUTABLE-IMPLEMENTATION-PLAN-001
    - RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001
    - RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001
    - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
    - RUNTIME-IMPL-PR-4-DETERMINISTIC-RNG-TABLE-ORACLE-INTERFACE-SKELETON-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
    - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
  defines_domain_service_family_inventory: true
  defines_domain_service_pr_sequence: true
  defines_dependency_rules: true
  defines_kernel_dependency_matrix: true
  defines_blocked_until_ledger: true
  defines_risk_review: true
  defines_future_integration_test_plan: true
  authorizes_domain_service_code_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_action_legality_engine_by_this_pr: false
  authorizes_state_store_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_transaction_lifecycle_by_this_pr: false
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
  next_allowed_step: RUNTIME-DOMAIN-PR-1 command lifecycle and action legality service plan, pending review
```

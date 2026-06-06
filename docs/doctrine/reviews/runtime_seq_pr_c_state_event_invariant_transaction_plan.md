# RUNTIME-SEQ-PR-C: State / Event / Invariant / Transaction Plan

Date prepared: 2026-06-06
Status: Planning only; non-executable
Tracking ID: RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001
Derives from:
- RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001
- RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001
- RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001
Primary owner tracks: RT-001, RT-011
Supporting owner tracks: RT-002, RT-003, RT-004, RT-005, RT-006, RT-007, RT-008, RT-009, RT-010, RT-012

---

## 1. Purpose and status

This document is RUNTIME-SEQ-PR-C, a state/event/invariant/transaction plan for Astra Ascension.

It is planning-only and non-executable.

It defines future state, event, transaction, invariant, correction, replay, and trace contracts but does not implement:

- runtime code;
- state store;
- state delta model;
- event ledger;
- transaction preview system;
- rollback system;
- invariant validator;
- correction event schema;
- replay/hash service;
- persistence writer;
- database schema;
- command IR;
- validators;
- generators;
- context-packet compiler;
- redaction algorithm;
- RNG/table/oracle service;
- domain runtime service;
- live-play prompt;
- training data;
- donor-content audit;
- pilot conversion;
- sourcebook inclusion;
- canon promotion.

This plan was recommended by RUNTIME-SEQ-PR-B (section 18) as the next planning step after the narration/context packet contract plan was established. It focuses on the state/event boundary, transaction lifecycle, event commitment, correction events, world invariant registry, replay/hash requirements, event-channel boundaries, and rollback-safe validation.

---

## 2. Source ledger

This plan was prepared from the following actual repo artifacts:

### Core sequencing and runtime-quality sources

| Source | File |
|--------|------|
| RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001 | `docs/doctrine/reviews/runtime_schema_implementation_sequencing_review.md` |
| RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_a_minimum_backend_kernel_runtime_quality_contract_plan.md` |
| RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_b_narration_context_packet_contract_plan.md` |
| AUDIT-001 | `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md` |
| STAGE2-CLOSURE-REVIEW | `docs/doctrine/reviews/runtime_boundary_generator_ownership_stage2_completion_review_and_closure_ledger.md` |

### RT owner specifications (RT-001 through RT-012)

| Track | Role | File |
|-------|------|------|
| RT-001 (primary) | Command lifecycle / action legality / cost commitment | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md` |
| RT-002 | Resource / consequence math | `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md` |
| RT-003 | Combat / hazard / damage / recovery | `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md` |
| RT-004 | Ability / effect / skill binding | `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md` |
| RT-005 | Context-packet / hidden-information | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md` |
| RT-006 | Mission / reward / clue routing | `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md` |
| RT-007 | Social / faction / actor knowledge | `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md` |
| RT-008 | Generated-content provenance / recurrence | `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md` |
| RT-009 | Runtime RNG / table / oracle | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md` |
| RT-010 | Inventory / item / vehicle / asset | `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md` |
| RT-011 (primary) | Validation / readiness tooling | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md` |
| RT-012 | D-series / promotion boundary | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md` |

RT-001 is the primary owner of the command lifecycle and event commitment boundary. RT-011 is the validation/readiness owner. RT-005 is the context/visibility handoff owner. RT-009 is the deterministic RNG/replay handoff owner.

### Schema and schema/math/mechanics sources

| File ID | File |
|---------|------|
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
| SM00 | `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` |
| SM01 | `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md` |
| SM02 | `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md` |

### Governance sources

| Source | File |
|--------|------|
| ROADMAP-001 | `docs/doctrine/astra_doctrine_roadmap_v0_1.md` |
| REGISTRY-001 | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` |
| Decision log | `docs/decisions/current_decisions_log.md` |
| README | `README.md` |

All files listed above were confirmed present in the repository at drafting time.

---

## 3. Backend-first invariant

Astra Ascension must be model-interchangeable. The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

### State/event implication

Only backend-owned transaction, validation, state-delta, event-ledger, persistence, and replay systems may create durable truth. Narration, summaries, packet content, generated drafts, model suggestions, and player-facing prose are not committed state.

---

## 4. State/event boundary

The following defines the distinction among future state/event layers. All layers have implementation status: **future_required_not_implemented**.

### 4.1 BackendStateStore

- **Purpose:** Current canonical state of the game world. Single source of truth for all durable facts.
- **Owner:** Backend runtime kernel.
- **Allowed contents:** Committed records, committed relationships, committed resource totals, committed location states, committed actor states, committed inventory states, committed faction states, committed mission states.
- **Forbidden contents:** Narration prose, model suggestions, uncommitted previews, player-facing summaries, display artifacts, generated drafts awaiting provenance, source-local content not yet routed.
- **Persistence status:** Durable; persisted to storage.
- **May mutate state:** Yes — this is the canonical state.
- **May enter packets:** Only through backend-owned projection (StateProjection).
- **LLM allowed interaction:** None. The LLM may not read, write, or query BackendStateStore directly.

### 4.2 StateProjection

- **Purpose:** Role-filtered, visibility-bounded view of backend state produced for a specific consumer (player, narrator, evaluator).
- **Owner:** Backend runtime kernel (projection compiler).
- **Allowed contents:** Visible subset of committed state, filtered by visibility tier (per RT-005), redacted references where hidden facts are withheld.
- **Forbidden contents:** Hidden facts, backend-only fields, uncommitted previews, narration, model suggestions, generated drafts.
- **Persistence status:** Ephemeral; produced on demand, not persisted as durable state.
- **May mutate state:** No.
- **May enter packets:** Yes — StateProjection is the primary source for context-packet content (per PR-B).
- **LLM allowed interaction:** Read-only through packets. The LLM receives projections but cannot modify or override them.

### 4.3 TransactionPreview

- **Purpose:** Non-committed proposed change set showing estimated costs, consequences, legality, and visible outcomes of a proposed action before commitment.
- **Owner:** Backend transaction preview system (future).
- **Allowed contents:** Proposed deltas, cost estimates, legality checks, required confirmations, randomness dependency declarations, visibility impact summaries.
- **Forbidden contents:** Committed state changes, rolled dice, revealed hidden facts, mutated records, generated content with provenance.
- **Persistence status:** Ephemeral; discarded after acceptance or rejection.
- **May mutate state:** No. Transaction preview must never mutate state.
- **May enter packets:** Yes — preview summaries may be projected to the player for confirmation.
- **LLM allowed interaction:** The LLM may receive preview summaries for narration. The LLM may not create, accept, reject, or modify previews.

### 4.4 StateDeltaEnvelope

- **Purpose:** Validated change payload prepared for commitment. Represents the minimal, auditable mutation to be applied to BackendStateStore.
- **Owner:** Backend state-delta system (future).
- **Allowed contents:** Source command reference, affected record references, before/after state references or hashes, mutation reason, owner track references, validation references, cost/consequence references.
- **Forbidden contents:** Narration, display prose, model suggestions, uncommitted previews, unvalidated changes.
- **Persistence status:** Persisted as part of the event ledger after commitment.
- **May mutate state:** Yes — only after passing full validation and event-commit authorization.
- **May enter packets:** No. State deltas are backend-internal; only their effects appear in projections.
- **LLM allowed interaction:** None. The LLM may not create, validate, authorize, or modify state deltas.

### 4.5 EventLedgerEntry

- **Purpose:** Append-only committed event record. Immutable audit trail of everything that happened in the game world.
- **Owner:** Backend event-ledger system (future).
- **Allowed contents:** Event ID, event type, timestamp/sequence, source command reference, source transaction reference, state delta references, actor/target/location references, owner track references, validation results, RNG/table references, visibility projection references, persistence references, replay hash references, correction references.
- **Forbidden contents:** Mutable fields, overwritten history, narration prose, display artifacts, model suggestions.
- **Persistence status:** Durable; append-only, immutable after commitment.
- **May mutate state:** Events record mutations; they do not themselves mutate state. State mutation occurs through the state-delta commitment path, and the event records that mutation.
- **May enter packets:** Event echoes (recent committed events) may appear in narration render packets as scene context.
- **LLM allowed interaction:** None. The LLM may not append, modify, delete, or reorder events.

### 4.6 RuntimeTrace

- **Purpose:** Diagnostic and audit trace for debugging, replay verification, and observability. Not a source of truth.
- **Owner:** Backend observability system (future).
- **Allowed contents:** Turn ID, player input reference, intent/command candidate references, validation results, transaction preview reference, state delta references, event references, RNG invocation references, packet references, model role references, narrator output reference, risk flags, invariant check references, correction references, replay hash reference.
- **Forbidden contents:** State authority claims, state mutations, event commitments.
- **Persistence status:** Persisted for audit/debug; retention policy separate from state/event persistence.
- **May mutate state:** No.
- **May enter packets:** No. Traces are backend-internal diagnostic artifacts.
- **LLM allowed interaction:** None.

### 4.7 NarrationDisplayOutput

- **Purpose:** Player-facing prose produced by the narrator model. Display layer only.
- **Owner:** Narrator model (under backend packet constraints).
- **Allowed contents:** Scene description, action narration, dialogue, atmosphere, tone-appropriate prose, visible consequences, available action affordances.
- **Forbidden contents:** State mutations, hidden facts, uncommitted outcomes, unvalidated claims, facts not in the narration render packet, generated content not routed through RT-008, source-local content not routed through RT-012.
- **Persistence status:** Logged for traceability; not persisted as state authority.
- **May mutate state:** No. Never.
- **May enter packets:** No. Narration output is downstream of packets, not a packet source.
- **LLM allowed interaction:** The LLM produces narration output. The LLM may not treat its own output as state, event, or authority.

### 4.8 SummaryArtifact

- **Purpose:** Continuity and recap artifact for session persistence, campaign summary, or player-facing recap. Display and continuity layer only.
- **Owner:** Summary model (under backend packet constraints).
- **Allowed contents:** Recap of committed events, visible state summaries, session continuity notes, player-facing timeline.
- **Forbidden contents:** State authority claims, hidden facts, uncommitted outcomes, state mutations, event commitments, memory authority.
- **Persistence status:** Persisted for continuity; not persisted as state authority.
- **May mutate state:** No. Never.
- **May enter packets:** Summary artifacts may inform future packets as continuity context, but they are not state authority and must not override event ledger truth.
- **LLM allowed interaction:** The LLM may produce summaries. The LLM may not treat summaries as memory authority or state.

### 4.9 CorrectionEvent

- **Purpose:** Append-only correction path for errors discovered after commitment. Corrections acknowledge and fix mistakes without silently editing history.
- **Owner:** Backend correction system (future).
- **Allowed contents:** Correction ID, reference to original event/state being corrected, correction reason, correcting authority, corrected state/event references, replay chain impact.
- **Forbidden contents:** Silent history edits, silent overwrites, retroactive state mutations without audit trail.
- **Persistence status:** Durable; append-only, part of the event ledger.
- **May mutate state:** Yes — corrections may produce new state deltas, but only through the standard validated commitment path, and they must reference what was corrected and why.
- **May enter packets:** Correction effects may appear in projections once committed.
- **LLM allowed interaction:** None. The LLM may not create, authorize, or modify correction events.

---

## 5. Transaction lifecycle contract

The following defines the future transaction lifecycle as planning stages. These are planning labels only, not final state-machine values, schemas, enums, or code.

### 5.1 Normal lifecycle stages

1. **player_input_received** — Raw player input captured by the backend.
2. **intent_candidate_proposed** — LLM or parser proposes an intent interpretation.
3. **command_candidate_assembled** — Backend assembles a candidate command IR from the intent.
4. **command_legality_checked** — Backend validates legality (RT-001).
5. **cost_and_resource_previewed** — Backend estimates costs and resource consequences (RT-002).
6. **randomness_dependency_declared** — Backend identifies RNG/table dependencies without rolling (RT-009).
7. **hidden_info_boundary_checked** — Backend validates no hidden-information leakage in the proposed action (RT-005).
8. **transaction_preview_created** — Backend produces a TransactionPreview summarizing the proposed change.
9. **invariant_precheck_applied** — Backend runs world invariant prechecks against the proposed change.
10. **player_confirmation_requested_if_required** — If the action requires player confirmation (high cost, irreversible, ambiguous), the backend requests confirmation.
11. **transaction_accepted** — Player confirms or action proceeds without confirmation requirement.
12. **state_delta_prepared** — Backend prepares a StateDeltaEnvelope with validated changes.
13. **event_commit_authorized** — Backend authorizes event commitment after all validation passes.
14. **event_appended** — EventLedgerEntry appended to the event ledger.
15. **state_projection_refreshed** — Backend refreshes StateProjections for affected consumers.
16. **narration_render_packet_prepared** — Backend prepares a NarrationRenderPacket for the narrator.
17. **narration_displayed** — Narrator model produces NarrationDisplayOutput.
18. **trace_recorded** — RuntimeTrace recorded for the complete turn.

### 5.2 Rejection and quarantine stages

- **command_rejected** — Command fails legality check; no state mutation occurs.
- **command_quarantined** — Command is ambiguous or requires escalation; held for review.
- **preview_rejected** — Player rejects the transaction preview; no state mutation occurs.
- **invariant_violation_detected** — Proposed change violates a world invariant; transaction blocked.
- **hidden_info_leakage_blocked** — Proposed action would leak hidden information; transaction blocked.
- **soft_state_mutation_blocked** — Narrator or model output attempted to imply state mutation; blocked and flagged.
- **event_commit_denied** — Event commitment denied after validation failure; no state mutation occurs.

These are planning labels only. They do not define final state-machine values, schemas, enums, or code.

---

## 6. Transaction preview contract

The following defines planning-level rules for the future transaction preview system.

- Transaction preview is not event commitment. A preview is a non-binding proposal that may be accepted, rejected, or abandoned.
- Transaction preview may inspect current backend state to estimate outcomes.
- Transaction preview may estimate costs, consequences, legality, visible outcomes, and required confirmations.
- Transaction preview must not mutate state. No state change may occur as a result of creating, displaying, or discarding a preview.
- Transaction preview must record randomness dependencies without rolling unless authorized by a future RNG plan. The preview declares what dice/tables would be invoked, not their results.
- Transaction preview must route hidden-information limits through RT-005. No preview may reveal hidden facts to unauthorized consumers.
- Transaction preview must route cost/consequence pressure through RT-002. Cost estimates must use RT-002 boundaries.
- Transaction preview must route validation through RT-011. Preview validation must use the same validation pipeline as commitment validation.
- Transaction preview must route source-local/generated-content boundaries through RT-008 and RT-012. Previews involving generated or source-local content must respect provenance and promotion boundaries.
- Rejected or quarantined preview mutates no state. Abandoning a preview is a no-op from the state perspective.
- Accepted preview may become state delta only through future authorized backend systems. Preview acceptance is a planning-level gate, not direct state mutation.

This plan does not implement preview logic or preview schemas.

---

## 7. State delta contract

The following defines planning-level StateDeltaEnvelope families. This is a conceptual contract for future schema work, not a final schema.

### StateDeltaEnvelope planning fields

| Field family | Purpose |
|-------------|---------|
| source_command_ref | Reference to the originating command IR. |
| source_preview_ref | Reference to the accepted TransactionPreview, if any. |
| affected_record_refs | References to all records affected by this delta. |
| before_state_ref_or_hash | Reference or hash of the affected records before mutation. |
| proposed_after_state_ref_or_hash | Reference or hash of the proposed state after mutation. |
| mutation_reason | Human- and machine-readable reason for the mutation. |
| owner_track_refs | RT-001 through RT-012 tracks responsible for this delta. |
| validation_refs | References to validation results that authorized this delta. |
| visibility_impact | Description of how visibility/projection changes for affected consumers. |
| hidden_info_impact | Description of any hidden-information boundary changes. |
| cost_consequence_refs | References to cost/consequence calculations (RT-002). |
| rng_invocation_refs_if_any | References to RNG/table invocations required for this delta (RT-009). |
| generated_content_refs_if_any | References to generated content involved, with provenance (RT-008). |
| persistence_requirement | What persistence guarantees this delta requires. |
| event_commit_requirement | What event-commitment path this delta must follow. |

This is not a final schema. It is a conceptual contract for future schema work.

---

## 8. Event ledger contract

### 8.1 EventLedgerEntry planning fields

| Field family | Purpose |
|-------------|---------|
| event_id | Unique identifier for this event. |
| event_type_family | Category of event (see 8.2). |
| event_timestamp_or_sequence | Timestamp or monotonic sequence number. |
| source_command_ref | Reference to the originating command. |
| source_transaction_ref | Reference to the originating transaction. |
| state_delta_refs | References to state deltas committed by this event. |
| actor_refs | References to actors involved. |
| target_refs | References to targets affected. |
| location_refs | References to locations involved. |
| owner_track_refs | RT tracks responsible. |
| validation_result_refs | References to validation results. |
| rng_table_refs | References to RNG/table invocations. |
| visibility_projection_refs | References to visibility projections affected. |
| persistence_refs | References to persistence operations. |
| replay_hash_refs | References to replay hashes for deterministic verification. |
| correction_refs_if_any | References to correction events, if this event was corrected or is itself a correction. |

### 8.2 Event-family planning categories

- **command_event** — A player or system command was received and processed.
- **transaction_event** — A transaction was previewed, accepted, or rejected.
- **state_delta_event** — A state delta was validated and committed.
- **rng_or_table_event** — A random number generation or table/oracle invocation occurred.
- **visibility_projection_event** — A visibility projection was created or updated.
- **narration_display_event** — A narration display output was produced and logged.
- **correction_event** — A correction was applied to a prior event or state.
- **generated_content_event** — Generated content was produced, with provenance tracked.
- **provenance_event** — A provenance record was created or updated.
- **validation_event** — A validation check was performed.
- **system_audit_event** — A system-level audit action was recorded.

Event categories are planning labels only. They do not define final enums, schemas, database tables, or event-store code.

---

## 9. Event-channel boundary

The following defines event-channel boundaries for the future runtime. Each channel isolates a category of events to enforce separation of concerns.

### 9.1 mechanical_state_channel

- **Purpose:** Carries state-delta events and committed state mutations.
- **Allowed records:** StateDeltaEnvelope, committed state snapshots, resource/cost mutations.
- **Forbidden records:** Narration prose, display artifacts, model suggestions, uncommitted previews.
- **Can mutate canonical state:** Yes — this is the only channel authorized to carry state-mutating events.
- **Can be projected to narrator:** No. State deltas are backend-internal. Their effects reach the narrator only through StateProjection.
- **Owner RT handoff:** RT-001 (command lifecycle), RT-002 (resource/consequence).
- **Implementation status:** future_required_not_implemented.

### 9.2 visibility_channel

- **Purpose:** Carries visibility projection events and hidden-information boundary changes.
- **Allowed records:** Visibility tier changes, projection updates, redaction events, hidden-info withholding records.
- **Forbidden records:** State mutations, narration prose, model suggestions.
- **Can mutate canonical state:** No. Visibility projections are derived from state; they do not mutate it.
- **Can be projected to narrator:** Yes — visibility projections inform what the narrator may and may not say.
- **Owner RT handoff:** RT-005 (context-packet/hidden-information).
- **Implementation status:** future_required_not_implemented.

### 9.3 narration_display_channel

- **Purpose:** Carries narration display events. Logged for traceability but never state authority.
- **Allowed records:** NarrationDisplayOutput, narrator output metadata, soft-state mutation detection flags.
- **Forbidden records:** State mutations, event commitments, hidden facts, validation results.
- **Can mutate canonical state:** No. Narration display events may be logged but cannot mutate mechanical state.
- **Can be projected to narrator:** N/A — this channel carries narrator output, not narrator input.
- **Owner RT handoff:** RT-005 (packet projection), RT-011 (output validation).
- **Implementation status:** future_required_not_implemented.

### 9.4 rng_table_channel

- **Purpose:** Carries RNG invocation events, table/oracle lookups, seed references, and replay data.
- **Allowed records:** RNG invocation records, table lookup records, seed references, replay hashes, result-domain validation records.
- **Forbidden records:** Narration prose, state mutations (RNG results feed into state deltas through the mechanical_state_channel), model suggestions.
- **Can mutate canonical state:** No. RNG results are inputs to state deltas, not direct state mutations.
- **Can be projected to narrator:** RNG outcomes may appear in narration render packets as visible results.
- **Owner RT handoff:** RT-009 (RNG/table/oracle).
- **Implementation status:** future_required_not_implemented.

### 9.5 generated_content_channel

- **Purpose:** Carries generated-content events with provenance tracking.
- **Allowed records:** Generated content records, provenance metadata, recurrence tracking, source attribution.
- **Forbidden records:** State mutations, narration prose, canon promotion claims.
- **Can mutate canonical state:** No. Generated content enters state only through the standard state-delta commitment path with provenance.
- **Can be projected to narrator:** Generated content may appear in packets if it has been committed with provenance.
- **Owner RT handoff:** RT-008 (generated-content provenance/recurrence).
- **Implementation status:** future_required_not_implemented.

### 9.6 provenance_channel

- **Purpose:** Carries provenance records for content origin tracking, source-local capsule boundary events, and promotion-boundary events.
- **Allowed records:** Provenance records, source attribution records, source-local capsule boundary records, promotion-boundary quarantine records.
- **Forbidden records:** State mutations, narration prose, canon promotion (provenance tracks origin, it does not promote).
- **Can mutate canonical state:** No.
- **Can be projected to narrator:** Provenance metadata may inform packet assembly but is not directly displayed.
- **Owner RT handoff:** RT-008 (provenance), RT-012 (promotion boundary).
- **Implementation status:** future_required_not_implemented.

### 9.7 validation_audit_channel

- **Purpose:** Carries validation results, readiness checks, invariant check results, and audit records.
- **Allowed records:** Validation results, readiness gate records, invariant check results, schema validation results, command legality results.
- **Forbidden records:** State mutations, narration prose, model suggestions.
- **Can mutate canonical state:** No. Validation results inform commitment decisions but do not themselves mutate state.
- **Can be projected to narrator:** Validation failure summaries may appear in player-facing feedback.
- **Owner RT handoff:** RT-011 (validation/readiness), RT-001 (command legality).
- **Implementation status:** future_required_not_implemented.

### 9.8 correction_channel

- **Purpose:** Carries correction events and correction chain references.
- **Allowed records:** CorrectionEvent records, correction chain references, corrected-state references, correction authority records.
- **Forbidden records:** Silent history edits, silent overwrites, retroactive state mutations without audit trail.
- **Can mutate canonical state:** Corrections produce new state deltas through the standard commitment path. The correction channel itself does not directly mutate state.
- **Can be projected to narrator:** Correction effects may appear in packets once committed.
- **Owner RT handoff:** RT-001 (event commitment), RT-011 (validation).
- **Implementation status:** future_required_not_implemented.

### 9.9 persistence_snapshot_channel

- **Purpose:** Carries persistence snapshot events, checkpoint records, and storage boundary notifications.
- **Allowed records:** Snapshot records, checkpoint records, storage boundary events, backup references.
- **Forbidden records:** State mutations (snapshots record state, they do not mutate it), narration prose.
- **Can mutate canonical state:** No. Snapshots are point-in-time records.
- **Can be projected to narrator:** No.
- **Owner RT handoff:** Backend persistence system (future).
- **Implementation status:** future_required_not_implemented.

---

## 10. WorldInvariantRegistry planning contract

The following defines future invariant categories for the WorldInvariantRegistry. These are planning-level categories, not final validators or code.

### 10.1 Invariant categories

1. **authority_invariants** — Only backend-authorized systems may commit state, append events, or validate commands. No LLM, narrator, or display layer may claim authority.
2. **identity_reference_invariants** — All records must have unique, stable identifiers. References must resolve to existing records.
3. **state_consistency_invariants** — State must be internally consistent. No contradictory facts may coexist in committed state.
4. **visibility_hidden_info_invariants** — Hidden facts must not appear in player-visible packets. Visibility tiers must be respected across all projections.
5. **resource_cost_invariants** — Actors cannot spend unavailable resources. Cost commitments must reference available resources before commitment.
6. **actor_action_legality_invariants** — Actors may only perform actions they are legally permitted to perform under current rules and state.
7. **asset_ownership_uniqueness_invariants** — Items must not exist in two inventories unless duplication is explicitly committed through a validated state delta.
8. **location_presence_invariants** — Actors and assets must have consistent location state. An entity cannot be in two places unless explicitly permitted.
9. **generated_content_provenance_invariants** — Generated content must not become durable without provenance. All generated content must have tracked origin and provenance metadata.
10. **source_local_canon_boundary_invariants** — Source-local content must not become canon through repeated use. Canon boundary must be explicitly managed through RT-012.
11. **rng_replay_invariants** — Random outcomes must reference backend RNG/table authority. RNG results must be reproducible through replay.
12. **packet_narration_invariants** — Narration must not become state. Narrator output is display-only and cannot override committed state or event ledger truth.
13. **promotion_authority_invariants** — D-series/native-design pressure must not become authority without RT-012 routing. Promotion requires explicit authorization.

### 10.2 Representative invariant examples

- Hidden facts must not appear in player-visible packets.
- Narration must not become state.
- Generated content must not become durable without provenance.
- Source-local content must not become canon through repeated use.
- D-series/native-design pressure must not become authority without RT-012 routing.
- Items must not exist in two inventories unless duplication is explicitly committed.
- Actors cannot spend unavailable resources.
- Random outcomes must reference backend RNG/table authority.
- Event commits must be append-only.
- Summaries cannot override event ledger truth.

This plan does not implement invariant checks.

---

## 11. Rollback-safe validation and commitment

The following defines the planning-level validation order for the future transaction commitment pipeline. Failed validation at any stage must leave state unchanged.

### Validation order

1. **Schema/record validation** — Proposed records conform to schema.
2. **Command legality validation** — Proposed command is legal under current rules and state (RT-001).
3. **Visibility validation** — Proposed action does not leak hidden information (RT-005).
4. **Cost/resource validation** — Required resources are available (RT-002).
5. **RNG/table dependency validation** — RNG/table dependencies are declared and valid (RT-009).
6. **Owner-boundary validation** — Proposed change respects RT track ownership boundaries.
7. **Invariant precheck** — Proposed change does not violate world invariants.
8. **Transaction preview review** — Preview is presented and reviewed.
9. **Player confirmation if required** — Player confirms high-cost or irreversible actions.
10. **State delta validation** — StateDeltaEnvelope passes structural and semantic validation.
11. **Event commit validation** — Event commitment is authorized.
12. **Persistence boundary validation** — Persistence requirements are met.
13. **Post-commit invariant check** — World invariants hold after commitment.
14. **Packet projection validation** — Updated projections are consistent with committed state.

Failed validation must leave state unchanged. No partial commits. No silent state corruption.

This PR does not implement rollback or validation code.

---

## 12. Correction event protocol

The following defines planning-level correction principles for the CorrectionEventProtocol.

- Corrections are append-only. A correction event is a new event that references and corrects a prior event. It does not edit or delete the prior event.
- Corrections must not silently edit committed history. The original event remains in the ledger; the correction event explicitly records what was wrong and what was changed.
- Wrong narration is corrected by a later correction event or clarification, not by making wrong prose true. If the narrator said something incorrect, the correction path is a new event or clarification, not retroactive state mutation to match the narration.
- Wrong packet projection must be traced and corrected. If a packet contained incorrect information, the error must be traced and a correction issued.
- Hidden-information leakage requires quarantine and escalation. If hidden information was incorrectly revealed, the leakage must be quarantined, escalated, and corrected through appropriate channels.
- Mistaken generated content must be rejected, quarantined, or corrected with provenance. Generated content that was committed in error must be handled through the correction path with full provenance tracking.
- Correction must preserve the replay/audit chain. Corrections must not break replay determinism or audit traceability.
- Correction events must identify what was wrong, what authority corrected it, and what state/event references are affected.

This plan does not define final correction schemas or workflow code.

---

## 13. Replay/hash/audit requirements

The following defines future replay/hash/audit requirements. All are future-required and not implemented here.

1. **Deterministic command replay** — Given the same initial state and the same sequence of commands, the system must produce the same final state.
2. **Deterministic RNG/table replay** — Given the same seeds and invocation sequence, RNG/table results must be identical.
3. **Event-order verification** — The order of events in the ledger must be verifiable and consistent.
4. **State snapshot/hash verification** — State snapshots at any point must be hashable and verifiable against the event ledger.
5. **Packet projection traceability** — Every packet produced must be traceable to the state and events that produced it.
6. **Narration display traceability** — Every narration output must be traceable to the packet that produced it.
7. **Correction chain traceability** — Every correction must be traceable through the full correction chain.
8. **Provenance traceability** — All content must have traceable provenance (source, generator, converter, promoter).
9. **Failed-command traceability** — Failed commands must be traceable for audit and debugging.
10. **Hidden-info withholding traceability** — Every instance of hidden-information withholding must be traceable for audit.
11. **Model-role traceability** — Every model invocation must record which model role was used and what constraints applied.

Replay/hash audit is future-required and not implemented here.

---

## 14. Runtime trace requirements

The following defines future per-turn RuntimeTrace families. Runtime traces are audit/debug artifacts, not state authority.

### Per-turn trace fields

| Field family | Purpose |
|-------------|---------|
| turn_id | Unique identifier for this turn. |
| player_input_ref | Reference to the raw player input. |
| intent_candidate_refs | References to intent candidates proposed. |
| command_candidate_ref | Reference to the assembled command candidate. |
| validation_result_refs | References to validation results for this turn. |
| transaction_preview_ref | Reference to the transaction preview produced. |
| state_delta_refs | References to state deltas committed this turn. |
| event_refs | References to events appended this turn. |
| rng_invocation_refs | References to RNG/table invocations this turn. |
| packet_refs | References to packets produced this turn. |
| model_role_refs | References to model roles invoked this turn. |
| narrator_output_ref | Reference to the narrator output produced. |
| soft_state_risk_flags | Flags for detected soft-state mutation risks. |
| hidden_info_risk_flags | Flags for detected hidden-information risks. |
| invariant_check_refs | References to invariant checks performed. |
| correction_refs | References to corrections applied this turn. |
| replay_hash_ref | Replay hash for this turn's complete sequence. |

Runtime traces are audit/debug artifacts, not state authority. They cannot commit state, mutate records, or override the event ledger.

---

## 15. LLM non-authority rules for state/events

The LLM is explicitly prohibited from:

- Creating backend state.
- Mutating backend state.
- Creating state deltas.
- Appending events.
- Validating command legality.
- Authorizing transactions.
- Confirming costs.
- Rolling dice.
- Invoking tables/oracles.
- Creating correction events.
- Rewriting history.
- Changing visibility tiers.
- Marking hidden facts visible.
- Committing generated content.
- Assigning provenance.
- Changing inventories.
- Moving actors.
- Applying damage, healing, or recovery.
- Changing faction, social, or knowledge state.
- Converting narration into truth.
- Converting summaries into memory authority.
- Promoting source-local, D-series, generated, or converted content.

The LLM may propose intents, produce narration from packets, produce summaries from committed events, and produce evaluations from evaluation packets. All LLM outputs are downstream of backend state and authority; none are upstream.

---

## 16. Domain handoff crosswalk

The following maps RT-001 through RT-012 to state/event/transaction responsibilities defined in this plan.

| RT Track | Domain | State/event/transaction responsibilities |
|----------|--------|------------------------------------------|
| RT-001 | Command lifecycle / action legality / cost commitment | Command lifecycle gate. Transaction gate (acceptance/rejection). Event commit boundary. Owns the transition from command candidate through legality check to event authorization. |
| RT-002 | Resource / consequence math | Cost/resource/consequence deltas. Produces cost estimates for transaction previews. Validates resource availability before commitment. Cost/consequence state delta fields. |
| RT-003 | Combat / hazard / damage / recovery | Damage/hazard/recovery deltas and event families. Produces state deltas for HP, conditions, injuries, environmental effects, recovery. Combat/hazard event categories. |
| RT-004 | Ability / effect / skill binding | Ability/effect/skill resolution deltas. Produces state deltas for ability activation, effect application, skill check results. Ability/effect event families. |
| RT-005 | Context-packet / hidden-information | Visibility state ownership. Hidden-information partition authority. Packet projection effects on state/event visibility. Validates that no transaction leaks hidden information. |
| RT-006 | Mission / reward / clue routing | Mission/clue/reward objective-state deltas. Produces state deltas for objective completion, clue reveals, reward distribution. Mission/scenario event families. |
| RT-007 | Social / faction / actor knowledge | Social/faction/actor-knowledge deltas. Produces state deltas for reputation, relationships, faction standing, actor knowledge changes. Social/faction event families. |
| RT-008 | Generated-content provenance / recurrence | Generated-content provenance and recurrence events. Tracks origin and provenance for all generated content. Generated-content event families in the generated_content_channel. |
| RT-009 | Runtime RNG / table / oracle | RNG/table/oracle invocation events and replay requirements. Backend-owned random authority. Seed/replay reference requirements. RNG/table event families in the rng_table_channel. |
| RT-010 | Inventory / item / vehicle / asset | Inventory/item/vehicle/asset deltas. Produces state deltas for inventory changes, item transfers, vehicle state, asset ownership. Asset uniqueness invariants. |
| RT-011 | Validation / readiness tooling | Validation/readiness and invariant checks. Owns the validation pipeline that gates every stage of the transaction lifecycle. Validates state deltas, event commits, and packet projections. |
| RT-012 | D-series / promotion boundary | Promotion-boundary events and authority quarantine. Tracks D-series and native-design pressure. Validates that no content is promoted without explicit authorization. Promotion event families. |

---

## 17. Validation and test requirements

The following identifies future test families required when state/event/invariant/transaction systems are implemented.

1. **Transaction preview no-mutation tests** — Verify that creating, displaying, or discarding a transaction preview produces no state mutation.
2. **Rejected command no-state-change tests** — Verify that rejected commands leave state completely unchanged.
3. **State delta validation tests** — Verify that StateDeltaEnvelopes pass structural and semantic validation before commitment.
4. **Event append-only tests** — Verify that events are append-only and cannot be modified or deleted after commitment.
5. **Event replay determinism tests** — Verify that replaying the same events from the same initial state produces identical final state.
6. **RNG/table replay tests** — Verify that RNG/table invocations with the same seeds produce identical results.
7. **Invariant precheck tests** — Verify that invariant prechecks catch violations before state mutation.
8. **Hidden-info leakage invariant tests** — Verify that hidden information never appears in player-visible projections or packets.
9. **Narration-not-state tests** — Verify that narration output cannot become state authority.
10. **Correction event trace tests** — Verify that correction events maintain full audit trail and do not silently edit history.
11. **Summary-not-memory-authority tests** — Verify that summaries cannot override event ledger truth or become memory authority.
12. **Source-local/canon boundary invariant tests** — Verify that source-local content cannot become canon without explicit promotion authorization.
13. **Generated-content provenance invariant tests** — Verify that generated content cannot become durable without provenance tracking.
14. **Packet projection trace tests** — Verify that every packet is traceable to the state and events that produced it.
15. **Runtime trace completeness tests** — Verify that runtime traces capture all required fields for each turn.

This PR only identifies future test requirements. It adds focused doctrine tests for the planning artifact itself, not runtime implementation tests.

---

## 18. Blocked-until ledger

The following items remain blocked until separately authorized implementation work begins:

- State store implementation.
- State delta schema/model implementation.
- Event ledger implementation.
- Transaction preview implementation.
- Rollback implementation.
- Invariant validator implementation.
- Correction event schema implementation.
- Replay/hash service implementation.
- Runtime trace implementation.
- Persistence writer implementation.
- Database schema.
- Command IR implementation.
- Context-packet compiler implementation.
- RNG/table implementation.
- Domain services.
- Live-play adapter.
- Prompt templates.
- Training.
- Pilot conversion.
- Sourcebook inclusion.
- Canon promotion.

---

## 19. Next recommended planning PR

### RUNTIME-SEQ-PR-D: Story-capable structure and playable-content plan

PR-D should handle:

- Story-capable structures.
- Playable-content proof.
- Narrative substrate.
- Storylet registry.
- Quest/scenario dependency DAG.
- NPC goal stack.
- Dialogue-act IR.
- Content ecology.
- Source-local capsule boundary expansion.
- Generator-to-validate-to-commit pipeline.

PR-C does not authorize PR-D or implement it. PR-D requires separate authorization and review.

---

## 20. Non-implementation reaffirmation

This PR adds no:

- runtime code;
- state store;
- state delta model;
- event ledger;
- transaction preview system;
- rollback system;
- invariant validator;
- correction event schema;
- replay/hash service;
- runtime trace implementation;
- persistence writer;
- database schema;
- command IR;
- validator implementation;
- generator implementation;
- context-packet compiler;
- redaction algorithm;
- RNG/table/oracle service;
- domain runtime service;
- live-play prompt;
- training data;
- donor-content audit;
- pilot conversion authorization;
- sourcebook inclusion authorization;
- canon promotion.

---

## 21. Classification block

```yaml
runtime_seq_pr_c:
  review_id: RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001
  artifact_type: state_event_invariant_transaction_plan
  implementation_status: non_executable_planning
  derives_from:
    - RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001
    - RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001
    - RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001
  primary_owner_tracks:
    - RT-001
    - RT-011
  supporting_owner_tracks:
    - RT-002
    - RT-003
    - RT-004
    - RT-005
    - RT-006
    - RT-007
    - RT-008
    - RT-009
    - RT-010
    - RT-012
  defines_state_event_boundary: true
  defines_transaction_lifecycle_contract: true
  defines_transaction_preview_contract: true
  defines_state_delta_contract: true
  defines_event_ledger_contract: true
  defines_event_channel_boundaries: true
  defines_world_invariant_registry_requirements: true
  defines_correction_event_protocol: true
  defines_replay_hash_audit_requirements: true
  defines_runtime_trace_requirements: true
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_state_store: false
  authorizes_state_delta_model: false
  authorizes_event_ledger: false
  authorizes_transaction_preview_system: false
  authorizes_invariant_validator: false
  authorizes_correction_event_schema: false
  authorizes_replay_hash_service: false
  authorizes_runtime_trace_implementation: false
  authorizes_persistence_writer: false
  authorizes_context_packet_compiler: false
  authorizes_rng_service: false
  authorizes_domain_services: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-SEQ-PR-D story-capable structure and playable-content plan, pending review
```

# RUNTIME-DOMAIN-PR-2: State Store and State Projection Service Plan

## 1. Purpose and status

This document is **RUNTIME-DOMAIN-PR-2**, a planning-only service plan for the future State Store and State Projection service within the Astra Ascension runtime domain-service layer.

It follows **RUNTIME-DOMAIN-PR-1B** (command lifecycle / action legality skeleton review), which confirmed:

- PR-1A command lifecycle / action legality skeleton stayed within scope.
- The first domain package guardrail transition is safe.
- Command lifecycle / action legality skeletons are stable enough for later domain-service planning.
- No PR-1C hardening is required before state-store / state-projection planning.
- The next allowed step is RUNTIME-DOMAIN-PR-2.
- RUNTIME-DOMAIN-PR-2 must be planning-only.

**This PR authorizes only a future narrow implementation PR (RUNTIME-DOMAIN-PR-2A) after review.**

**This PR does not implement code.**

---

## 2. Source ledger

All source artifacts consulted for this plan:

| Artifact | ID | Role |
|---|---|---|
| RUNTIME-DOMAIN-PR-1B | RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001 | Gate source — authorized PR-2 |
| RUNTIME-DOMAIN-PR-1A | RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001 | First domain skeleton implementation |
| RUNTIME-DOMAIN-PR-1 | RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001 | Command lifecycle / action legality service plan |
| RUNTIME-DOMAIN-PR-0 | RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001 | Domain service implementation sequencing plan |
| RUNTIME-IMPL-PR-8 | RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001 | Post-kernel skeleton review / domain service readiness gate |
| RUNTIME-IMPL-PR-0 | Kernel bootstrap skeleton | Schema registry / record identity |
| RUNTIME-IMPL-PR-1 | Command envelope skeleton | Command envelope |
| RUNTIME-IMPL-PR-2 | Transaction preview skeleton | Transaction preview |
| RUNTIME-IMPL-PR-3 | State delta / event ledger / envelope skeleton | state_delta, event_ledger |
| RUNTIME-IMPL-PR-4 | RNG / table oracle skeleton | rng_interface, table_oracle |
| RUNTIME-IMPL-PR-5 | Validation pipeline / invariant precheck skeleton | validation_pipeline |
| RUNTIME-IMPL-PR-6 | Hidden information / context projection skeleton | hidden_information, context_projection |
| RUNTIME-IMPL-PR-7 | Persistence boundary / replay hash / audit / runtime trace skeleton | persistence_boundary, replay_audit, runtime_trace |
| Kernel skeleton modules | schema_registry, record_identity, command_envelope, transaction_preview, state_delta, event_ledger, rng_interface, table_oracle, validation_pipeline, hidden_information, context_projection, persistence_boundary, replay_audit, runtime_trace | 14 kernel modules |
| Domain skeleton modules | command_lifecycle, action_legality | Current domain skeleton |
| Runtime skeleton tests | test_domain_command_lifecycle_skeleton.py, test_domain_action_legality_skeleton.py | Domain test baseline |
| RT-001 | Command lifecycle / action legality owner specification | Primary service owner |
| RT-002 | Resource / consequence math owner specification | Future consumer |
| RT-003 | Combat / hazard / damage / recovery owner specification | Future consumer |
| RT-004 | Ability / effect / skill binding owner specification | Future consumer |
| RT-005 | Context packet / hidden information owner specification | Secondary dependency |
| RT-006 | Mission / reward / clue routing owner specification | Future consumer |
| RT-007 | Social / faction / actor knowledge owner specification | Future consumer |
| RT-008 | Generated-content provenance / recurrence owner specification | Future consumer |
| RT-009 | Runtime RNG / table oracle owner specification | Future consumer |
| RT-010 | Inventory / item / vehicle / asset owner specification | Future consumer |
| RT-011 | Validation readiness / tooling owner specification | Secondary dependency |
| RT-012 | D-series promotion boundary owner specification | Boundary enforcement |
| Registry | docs/doctrine/astra_doctrine_registry_v0_1.yaml | Tracking |
| Decision log | docs/decisions/current_decisions_log.md | Decision governance |
| C00 | Shared content record base and schema registry | Schema reference |
| C01 | Creature / NPC record schema | Schema reference |
| C02 | Item / gear record schema | Schema reference |
| C03 | Ability / power / technique record schema | Schema reference |
| C04 | Relic / implant / installable asset schema | Schema reference |
| C05 | Faction / institution record schema | Schema reference |
| C06 | Location / site / region record schema | Schema reference |
| C07 | Mission / scenario / adventure record schema | Schema reference |
| C08 | Vehicle / ship / platform record schema | Schema reference |
| C09 | Hazard / environment record schema | Schema reference |
| C10 | Table / oracle record schema | Schema reference |
| C11 | Companion / summon record schema | Schema reference |
| C12 | Crafting / salvage / recipe record schema | Schema reference |
| C13 | Map / diagram record schema | Schema reference |
| C14 | Source-local setting / cosmology record schema | Schema reference |

---

## 3. Backend-first invariant

**Astra Ascension must be model-interchangeable.** The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

### Service implication

The State Store and State Projection service is the future backend-owned read/projection boundary for runtime state. It may expose explicit state views and projection surfaces to authorized backend services, but it must not let model output, narration, summaries, donor text, or source-local content become state authority.

State is owned by the backend. Projections are derived from backend-owned state. No LLM output, narration summary, player description, donor-sourced text, or generated prose may serve as the source of truth for any runtime state record, snapshot, or projection.

---

## 4. Service ownership

### Primary owner

The State Store and State Projection service is the state ownership and projection boundary under the runtime domain-service layer. It depends on the following kernel modules:

- `state_delta` — mutation reference shapes
- `event_ledger` — event-derived authority reference
- `record_identity` — state record identity and references
- `schema_registry` — state record typing and schema posture
- `hidden_information` — visibility tier and redaction boundary
- `context_projection` — projection surface and visibility filtering
- `validation_pipeline` — state and projection shape validation
- `persistence_boundary` — snapshot prepare boundary
- `replay_audit` — audit and hash posture
- `runtime_trace` — traceable state read/projection decisions

### Secondary owner dependencies

| RT Owner | Relationship |
|---|---|
| RT-001 command lifecycle / action legality | Accepted command handoff only |
| RT-011 validation readiness / tooling | State-shape and projection validation |
| RT-005 hidden information / context projection | Visibility and projection boundaries |
| RT-002 resource / consequence math | Future consumer only |
| RT-003 combat / hazard / damage / recovery | Future consumer only |
| RT-004 ability / effect / skill binding | Future consumer only |
| RT-006 mission / reward / clue routing | Future consumer only |
| RT-007 social / faction / actor knowledge | Future consumer only |
| RT-008 generated-content provenance | Future consumer only |
| RT-010 inventory / item / vehicle / asset | Future consumer only |
| RT-012 D-series promotion boundary | Prevents doctrine/design documents from becoming direct runtime state authority |

### This service must not own

- Command execution.
- Action legality decisions.
- Transaction lifecycle.
- Event commitment.
- Resource math.
- Combat resolution.
- Ability / effect resolution.
- Inventory mutation.
- Mission / clue mutation.
- Social / faction mutation.
- Generated-content durability.
- Persistence backend implementation.
- Replay engine.
- Context-packet compilation.
- Model evaluation.
- Live-play adapter behavior.

---

## 5. Future service responsibilities

### Allowed future responsibilities

- Represent backend-owned state records and state snapshots.
- Expose immutable state views.
- Expose projection requests and projection results.
- Validate state reference shape.
- Validate projection request shape.
- Declare hidden-information projection constraints.
- Distinguish authoritative state from derived projection.
- Distinguish current state view from durable persistence.
- Hand off mutation requests to future transaction / event services rather than mutating directly.
- Support traceable state read / projection decisions.
- Prevent LLM / narration / summary authority over state.
- Support future domain services as read / projection consumers.

### Forbidden responsibilities

- State mutation.
- Applying state deltas.
- Committing events.
- Opening or closing transactions.
- Event store persistence.
- Durable database writes.
- Replay / state restoration.
- Resource cost calculation.
- Combat / damage resolution.
- Ability / effect resolution.
- Inventory mutation.
- Mission / social / faction mutation.
- Hidden payload exposure.
- Context-packet compilation.
- Prompt construction.
- Model calls.
- Live-play loop behavior.
- UI behavior.
- Donor conversion execution.
- Canon promotion.

---

## 6. State ownership model

### 6.1 Authoritative runtime state

- **Meaning:** The single source-of-truth representation of a game entity or world element at a given point in the event history. Derived from committed events and validated state deltas.
- **Authoritative:** Yes — this is the primary authority.
- **Who may create it:** Transaction / event commitment service (future), after validation.
- **Who may read it:** State store service, authorized backend domain services.
- **May be projected:** Yes, through explicit projection requests with visibility filtering.
- **May be persisted:** Yes, through persistence boundary.
- **Model output may affect it:** No. Never. Model output is not state authority.
- **Required kernel dependencies:** record_identity, schema_registry, state_delta, event_ledger, validation_pipeline, runtime_trace.
- **Blocked behavior:** Direct mutation by state store; model-derived creation; narration-sourced updates.

### 6.2 Projected state

- **Meaning:** A derived, read-only view of authoritative state filtered for a specific consumer, visibility tier, or scope.
- **Authoritative:** No — derived from authoritative state; must not be treated as source of truth.
- **Who may create it:** State projection service, from authoritative state.
- **Who may read it:** Requesting consumer (domain service, future context-packet compiler, future UI adapter).
- **May be projected:** Yes — projections may be further filtered.
- **May be persisted:** No (ephemeral / cached only). Persistence is for authoritative state.
- **Model output may affect it:** No. Projections reflect backend state, not model output.
- **Required kernel dependencies:** context_projection, hidden_information, validation_pipeline, runtime_trace.
- **Blocked behavior:** Treating projection as authoritative; writing projection back as state; exposing hidden payload in player-visible projection.

### 6.3 Visible state

- **Meaning:** The subset of projected state that passes visibility-tier filtering for a given actor or audience.
- **Authoritative:** No.
- **Who may create it:** State projection service, via hidden_information filtering.
- **Who may read it:** The actor / audience scoped to the visibility tier.
- **May be projected:** Yes (it is itself a projection).
- **May be persisted:** No (ephemeral).
- **Model output may affect it:** No.
- **Required kernel dependencies:** hidden_information, context_projection, runtime_trace.
- **Blocked behavior:** Exposing backend_hidden or redacted tiers; treating visible state as authoritative.

### 6.4 Hidden / backend-only state

- **Meaning:** State records or fields with visibility_tier = backend_hidden. Not visible to players, actors, or model-facing systems without explicit declassification.
- **Authoritative:** Yes — it is authoritative state, just not visible.
- **Who may create it:** Transaction / event commitment service (future).
- **Who may read it:** Backend services only. Never model-facing without explicit declassification gate.
- **May be projected:** Only to backend-scoped projections. Must be redacted for player / actor / model projections.
- **May be persisted:** Yes, through persistence boundary.
- **Model output may affect it:** No.
- **Required kernel dependencies:** hidden_information, context_projection, validation_pipeline, runtime_trace.
- **Blocked behavior:** Leaking to player-visible projection; leaking to model-facing projection; treating model guess as hidden-state authority.

### 6.5 Derived state

- **Meaning:** State computed from authoritative state for convenience (e.g., total inventory weight, effective modifier). Not itself stored as a committed event.
- **Authoritative:** No. Must be recomputable from authoritative state.
- **Who may create it:** Domain services that own the derivation formula.
- **Who may read it:** Requesting consumer.
- **May be projected:** Yes, with visibility filtering.
- **May be persisted:** Optional for caching; must not be sole authority.
- **Model output may affect it:** No.
- **Required kernel dependencies:** schema_registry, validation_pipeline, runtime_trace.
- **Blocked behavior:** Treating derived state as authoritative; persisting without recomputation guarantee; model-derived computation becoming authority.

### 6.6 Cached / ephemeral state

- **Meaning:** Temporary state held for performance or session continuity. Discardable without data loss because authoritative state is the recovery source.
- **Authoritative:** No.
- **Who may create it:** Any service that needs a local cache.
- **Who may read it:** The caching service.
- **May be projected:** No (internal optimization only).
- **May be persisted:** No (by definition ephemeral).
- **Model output may affect it:** No.
- **Required kernel dependencies:** None strictly; runtime_trace recommended.
- **Blocked behavior:** Treating cache as authoritative; using stale cache as state source; model-populated cache becoming authority.

### 6.7 Source-local converted content

- **Meaning:** Content extracted from a donor source and converted through the Aether Forge pipeline. May carry source-local rules, setting-specific content, or donor-specific terminology.
- **Authoritative:** No — source-local content is reference material, not canonical runtime state.
- **Who may create it:** Aether Forge extraction / conversion pipeline.
- **Who may read it:** State store (as reference); conversion review services.
- **May be projected:** Only with source-local markers preserved. Must never be projected as canonical state.
- **May be persisted:** Yes (as reference data with provenance).
- **Model output may affect it:** No.
- **Required kernel dependencies:** schema_registry, record_identity, runtime_trace.
- **Blocked behavior:** Treating source-local content as canonical state; letting donor terminology become Astra doctrine without lexicon review; promoting source-local content to authoritative state without explicit doctrine gate.

### 6.8 Canon / sourcebook content

- **Meaning:** Content promoted through the full doctrine review and canon promotion process. Becomes part of the Astra Ascension canonical universe.
- **Authoritative:** Yes, for the Astra setting — but only through explicit promotion, never automatic.
- **Who may create it:** Doctrine council, through canon promotion process.
- **Who may read it:** All authorized services.
- **May be projected:** Yes, with appropriate visibility filtering.
- **May be persisted:** Yes.
- **Model output may affect it:** No. Canon is doctrine-governed, not model-governed.
- **Required kernel dependencies:** schema_registry, record_identity, validation_pipeline, runtime_trace.
- **Blocked behavior:** Automatic promotion; model-authored canon; donor-to-canon without review; RT-012 boundary violation.

### 6.9 Generated content pending provenance

- **Meaning:** Content generated during runtime (by RNG, table oracle, or model narration) that has not yet received provenance tracking and durability authorization.
- **Authoritative:** No — not until provenance is established and durability is authorized.
- **Who may create it:** Runtime services that generate content (future).
- **Who may read it:** The generating service; provenance review.
- **May be projected:** Only with pending-provenance markers.
- **May be persisted:** Only after provenance authorization (RT-008).
- **Model output may affect it:** Model output may have generated it, but the generated content must not become durable state without provenance tracking.
- **Required kernel dependencies:** record_identity, schema_registry, runtime_trace, (future: RT-008 provenance).
- **Blocked behavior:** Becoming durable state without provenance; model output becoming authoritative state; skipping RT-008 provenance gate.

### 6.10 Persisted snapshot boundary

- **Meaning:** A point-in-time representation of authoritative state prepared for durable storage through the persistence boundary.
- **Authoritative:** It is a snapshot of authoritative state. The snapshot itself is immutable once prepared.
- **Who may create it:** State store service (prepare request) → persistence boundary (actual persistence, future).
- **Who may read it:** Replay / audit services; state restoration (future).
- **May be projected:** The snapshot content may be projected like any authoritative state.
- **May be persisted:** Yes — that is its purpose.
- **Model output may affect it:** No.
- **Required kernel dependencies:** persistence_boundary, replay_audit, runtime_trace, record_identity, schema_registry.
- **Blocked behavior:** Mutating a prepared snapshot; model-derived snapshot content; bypassing persistence boundary.

---

## 7. State projection model

### 7.1 Full backend projection

- **Allowed consumers:** Backend services with full state access authorization.
- **Hidden-information posture:** All tiers visible, including backend_hidden.
- **May include backend-hidden payload:** Yes.
- **May be used by model-facing systems later:** No — model-facing systems require separate, filtered projection.
- **Required validation:** Projection shape validation via validation_pipeline.
- **Required trace / audit posture:** Full runtime_trace entry.
- **Downstream service dependency:** None beyond kernel.

### 7.2 Player-visible projection

- **Allowed consumers:** Future context-packet compiler, future UI adapter (both not authorized by PR-2).
- **Hidden-information posture:** Only public and player_visible tiers. All restricted, backend_hidden, and redacted content excluded.
- **May include backend-hidden payload:** No.
- **May be used by model-facing systems later:** Yes, through future context-packet compiler (not authorized by PR-2).
- **Required validation:** Visibility-tier validation; hidden-info redaction verification.
- **Required trace / audit posture:** Full runtime_trace entry with visibility filter record.
- **Downstream service dependency:** RT-005 hidden-information boundary.

### 7.3 Actor-scoped projection

- **Allowed consumers:** Future services requiring per-actor state view (one player character's knowledge).
- **Hidden-information posture:** Only tiers visible to the specific actor. Other actors' hidden state excluded.
- **May include backend-hidden payload:** No.
- **May be used by model-facing systems later:** Yes, through future context-packet compiler with actor scope.
- **Required validation:** Actor identity validation via record_identity; visibility-tier check.
- **Required trace / audit posture:** Full runtime_trace entry with actor scope record.
- **Downstream service dependency:** RT-005, RT-001 (actor identity from command lifecycle).

### 7.4 Scene-scoped projection

- **Allowed consumers:** Future services requiring current-scene state (encounter, location, active events).
- **Hidden-information posture:** Scene-visible tiers only. Out-of-scene state excluded.
- **May include backend-hidden payload:** No.
- **May be used by model-facing systems later:** Yes, through future context-packet compiler with scene scope.
- **Required validation:** Scene boundary validation; visibility-tier check.
- **Required trace / audit posture:** Full runtime_trace entry with scene scope record.
- **Downstream service dependency:** RT-005, location/encounter services (future).

### 7.5 Faction / social projection

- **Allowed consumers:** Future RT-007 social / faction / actor knowledge service.
- **Hidden-information posture:** Faction-visible tiers only. Rival faction secrets excluded.
- **May include backend-hidden payload:** No.
- **May be used by model-facing systems later:** Yes, through future context-packet compiler with faction scope.
- **Required validation:** Faction identity validation; visibility-tier check.
- **Required trace / audit posture:** Full runtime_trace entry with faction scope.
- **Downstream service dependency:** RT-007.

### 7.6 Combat / encounter projection

- **Allowed consumers:** Future RT-003 combat / hazard / damage / recovery service.
- **Hidden-information posture:** Combat-relevant tiers only. Non-combat hidden state excluded.
- **May include backend-hidden payload:** No for player-facing; yes for backend combat resolution.
- **May be used by model-facing systems later:** Yes, for combat narration (through future context-packet compiler).
- **Required validation:** Combat state shape validation; visibility-tier check.
- **Required trace / audit posture:** Full runtime_trace entry with combat scope.
- **Downstream service dependency:** RT-003, RT-002.

### 7.7 Inventory / asset projection

- **Allowed consumers:** Future RT-010 inventory / item / vehicle / asset service.
- **Hidden-information posture:** Owner-visible tiers. Other characters' hidden inventory excluded.
- **May include backend-hidden payload:** No for player-facing.
- **May be used by model-facing systems later:** Yes, for inventory narration.
- **Required validation:** Inventory record shape validation; ownership check.
- **Required trace / audit posture:** Full runtime_trace entry with inventory scope.
- **Downstream service dependency:** RT-010.

### 7.8 Mission / clue projection

- **Allowed consumers:** Future RT-006 mission / reward / clue routing service.
- **Hidden-information posture:** Known-clue tiers only. Undiscovered clues hidden.
- **May include backend-hidden payload:** No for player-facing.
- **May be used by model-facing systems later:** Yes, for mission narration.
- **Required validation:** Mission record shape validation; clue discovery state check.
- **Required trace / audit posture:** Full runtime_trace entry with mission scope.
- **Downstream service dependency:** RT-006.

### 7.9 Hidden-info redacted projection

- **Allowed consumers:** Any consumer that needs a guaranteed-safe projection where all hidden content is replaced with redaction labels.
- **Hidden-information posture:** All hidden content replaced with redaction_label from hidden_information records.
- **May include backend-hidden payload:** No — that is the point.
- **May be used by model-facing systems later:** Yes — this is the safest projection for model-facing use.
- **Required validation:** Redaction completeness validation.
- **Required trace / audit posture:** Full runtime_trace entry with redaction audit.
- **Downstream service dependency:** RT-005.

### 7.10 Audit / provenance projection

- **Allowed consumers:** Audit services, replay services, governance review.
- **Hidden-information posture:** Full visibility (audit-privileged).
- **May include backend-hidden payload:** Yes (audit-privileged access).
- **May be used by model-facing systems later:** No — audit projections are backend-only.
- **Required validation:** Audit record shape validation; hash verification.
- **Required trace / audit posture:** Full runtime_trace and replay_audit entries.
- **Downstream service dependency:** replay_audit, persistence_boundary.

### 7.11 Model-facing projection candidate

- **Allowed consumers:** Future context-packet compiler (not authorized by PR-2).
- **Hidden-information posture:** Player-visible or actor-scoped tiers only. Never backend_hidden.
- **May include backend-hidden payload:** No.
- **May be used by model-facing systems later:** Yes — this is designed for that purpose. But the context-packet compiler is not authorized by PR-2.
- **Required validation:** Full hidden-info redaction verification; visibility-tier validation; projection shape validation.
- **Required trace / audit posture:** Full runtime_trace entry with model-facing marker.
- **Downstream service dependency:** RT-005, future context-packet compiler.

### 7.12 UI / client projection candidate

- **Allowed consumers:** Future UI / client adapter (not authorized by PR-2).
- **Hidden-information posture:** Player-visible tiers only.
- **May include backend-hidden payload:** No.
- **May be used by model-facing systems later:** No — UI projection and model-facing projection are separate concerns.
- **Required validation:** UI-safe shape validation; visibility-tier validation.
- **Required trace / audit posture:** Full runtime_trace entry.
- **Downstream service dependency:** Future UI adapter (not authorized by PR-2).

**PR-2 does not authorize a context-packet compiler or model-facing packet assembly.**

---

## 8. Future state lifecycle model

This section defines future state lifecycle stages for planning purposes only. No Python enum or code is created by this PR.

### 8.1 registered

- **Meaning:** A state record type has been declared in the schema registry with its record type, identity pattern, and schema shape.
- **Allowed inputs:** Schema definition, record type declaration.
- **Allowed outputs:** Schema registration confirmation, record type availability.
- **Owner service:** Schema registry (kernel).
- **Kernel dependency:** schema_registry, record_identity.
- **Prohibited behavior:** Creating runtime instances at registration time; treating schema registration as state creation.
- **Downstream handoff:** Enables loaded_as_reference.

### 8.2 loaded_as_reference

- **Meaning:** An existing state record has been loaded as a read-only reference for a projection or validation request.
- **Allowed inputs:** Record identity reference, read request from authorized service.
- **Allowed outputs:** Immutable state record reference.
- **Owner service:** State store service.
- **Kernel dependency:** record_identity, schema_registry, runtime_trace.
- **Prohibited behavior:** Mutating the loaded record; treating the reference as a mutable handle.
- **Downstream handoff:** Enables projection_requested.

### 8.3 projection_requested

- **Meaning:** A consumer has requested a projection of loaded state, specifying scope, visibility tier, and projection type.
- **Allowed inputs:** Projection request with scope, visibility tier, consumer identity.
- **Allowed outputs:** Validated projection request accepted for processing.
- **Owner service:** State projection service.
- **Kernel dependency:** context_projection, hidden_information, validation_pipeline, runtime_trace.
- **Prohibited behavior:** Executing the projection without validation; exposing hidden content before redaction check.
- **Downstream handoff:** Enables projection_validated or projection_rejected.

### 8.4 projection_validated

- **Meaning:** A projection request has passed shape validation, visibility-tier verification, and hidden-information safety checks.
- **Allowed inputs:** Validated projection request.
- **Allowed outputs:** Validation result confirming projection may proceed.
- **Owner service:** State projection service + validation_pipeline.
- **Kernel dependency:** validation_pipeline, hidden_information, runtime_trace.
- **Prohibited behavior:** Skipping validation; approving projections that would leak hidden info.
- **Downstream handoff:** Enables projection_materialized or projection_redacted.

### 8.5 projection_materialized

- **Meaning:** A validated projection has been assembled from authoritative state, with visibility filtering applied.
- **Allowed inputs:** Validated projection request + authoritative state records.
- **Allowed outputs:** Immutable projection result.
- **Owner service:** State projection service.
- **Kernel dependency:** context_projection, hidden_information, runtime_trace.
- **Prohibited behavior:** Including hidden payload in player-visible projection; mutating state during projection; model output influencing projection content.
- **Downstream handoff:** Returns to requesting consumer.

### 8.6 projection_redacted

- **Meaning:** A projection has been assembled with hidden content replaced by redaction labels.
- **Allowed inputs:** Validated projection request + authoritative state records + redaction rules.
- **Allowed outputs:** Redacted projection result with redaction labels in place of hidden content.
- **Owner service:** State projection service.
- **Kernel dependency:** hidden_information, context_projection, runtime_trace.
- **Prohibited behavior:** Including any hidden payload; partial redaction; redaction labels leaking information.
- **Downstream handoff:** Returns to requesting consumer.

### 8.7 projection_rejected

- **Meaning:** A projection request failed validation or was denied due to visibility-tier violation, invalid scope, or missing authorization.
- **Allowed inputs:** Invalid or unauthorized projection request.
- **Allowed outputs:** Rejection result with reason code.
- **Owner service:** State projection service + validation_pipeline.
- **Kernel dependency:** validation_pipeline, runtime_trace.
- **Prohibited behavior:** Returning partial state despite rejection; silently ignoring the rejection.
- **Downstream handoff:** Returns rejection to requesting consumer.

### 8.8 mutation_requested

- **Meaning:** A domain service has requested a state change (via accepted command lifecycle handoff).
- **Allowed inputs:** Accepted command handoff from command lifecycle service.
- **Allowed outputs:** Mutation request forwarded to transaction / event service.
- **Owner service:** State store service (receives and forwards only — does not execute).
- **Kernel dependency:** command_envelope (reference), state_delta (reference), runtime_trace.
- **Prohibited behavior:** State store executing the mutation; applying deltas directly; committing events.
- **Downstream handoff:** Enables mutation_deferred_to_transaction.

### 8.9 mutation_deferred_to_transaction

- **Meaning:** A mutation request has been forwarded to the future transaction / event commitment service. State store has no further role until the transaction completes.
- **Allowed inputs:** Forwarded mutation request.
- **Allowed outputs:** Transaction reference for tracking.
- **Owner service:** Future transaction lifecycle service.
- **Kernel dependency:** transaction_preview, state_delta, event_ledger, runtime_trace.
- **Prohibited behavior:** State store participating in transaction execution; state store applying the delta.
- **Downstream handoff:** Future transaction lifecycle service handles from here.

### 8.10 event_commit_pending

- **Meaning:** A transaction has been validated and an event commit is pending in the event ledger.
- **Allowed inputs:** Validated transaction result.
- **Allowed outputs:** Pending event ledger entry.
- **Owner service:** Future event commitment service.
- **Kernel dependency:** event_ledger, state_delta, runtime_trace.
- **Prohibited behavior:** State store committing events; state store bypassing event ledger.
- **Downstream handoff:** Enables event_committed_by_future_service.

### 8.11 event_committed_by_future_service

- **Meaning:** An event has been committed to the event ledger by the future event commitment service. Authoritative state has been updated.
- **Allowed inputs:** Committed event entry.
- **Allowed outputs:** Updated authoritative state; event confirmation.
- **Owner service:** Future event commitment service.
- **Kernel dependency:** event_ledger, state_delta, replay_audit, runtime_trace.
- **Prohibited behavior:** State store committing events; state store bypassing validation.
- **Downstream handoff:** State store may now load the updated authoritative state for future projections.

### 8.12 snapshot_prepare_requested

- **Meaning:** A snapshot of current authoritative state has been requested for persistence preparation.
- **Allowed inputs:** Snapshot prepare request with scope and identity.
- **Allowed outputs:** Persistence boundary request.
- **Owner service:** State store service (request) → persistence_boundary (preparation).
- **Kernel dependency:** persistence_boundary, replay_audit, runtime_trace, record_identity.
- **Prohibited behavior:** State store performing direct persistence writes; bypassing persistence boundary.
- **Downstream handoff:** Persistence boundary handles actual persistence (future).

### 8.13 archived_or_superseded

- **Meaning:** A state record or snapshot has been archived, superseded by a newer version, or removed from active state.
- **Allowed inputs:** Archive request or supersession event.
- **Allowed outputs:** Archive confirmation; removal from active state index.
- **Owner service:** State store service (reference management) + persistence_boundary (archival).
- **Kernel dependency:** record_identity, persistence_boundary, replay_audit, runtime_trace.
- **Prohibited behavior:** Deleting without audit trail; losing replay capability.
- **Downstream handoff:** Replay / audit service may reference archived records.

---

## 9. Kernel interface consumption plan

| Kernel Module | Position | Reason | Allowed Use | Forbidden Use |
|---|---|---|---|---|
| schema_registry | **required** | State record typing and schema posture | Look up record types; validate record shapes against registered schemas; resolve schema references | Modifying schemas; creating schemas at runtime; bypassing schema validation |
| record_identity | **required** | State record identity and references | Build and validate record IDs for state references; parse record identity strings; verify identity format | Creating new identity patterns outside established conventions; identity spoofing |
| command_envelope | **optional / later** | Source reference only | Reference command_id in mutation requests received from command lifecycle; trace command origin | Executing commands; parsing command payloads; creating command envelopes |
| transaction_preview | **later** | Future mutation planning handoff only | Reference preview_id when forwarding mutation requests to transaction service | Creating transaction previews; validating transaction previews; deciding transaction outcomes |
| state_delta | **required** | Future mutation input/output reference (PR-2 does not apply deltas) | Reference delta shapes for mutation handoff; validate delta envelope shape; reference affected_record_ids | Applying deltas to state; creating deltas; committing deltas; executing state changes |
| event_ledger | **required** | Future event-derived authority reference (PR-2 does not commit events) | Reference event types for state derivation; validate event entry shape; reference sequence for ordering | Committing events; creating event entries; modifying event history; replaying events |
| rng_interface | **optional / later** | Traceable provenance source | Reference RNG invocation for provenance tracking | Treating RNG output as state authority by itself; generating random values |
| table_oracle | **optional / later** | Traceable provenance source | Reference table oracle result for provenance tracking | Treating oracle output as state authority by itself; performing table lookups |
| validation_pipeline | **required** | State and projection shape validation | Validate state record references; validate projection requests; validate projection results; create validation issues | Bypassing validation; weakening validation rules; silencing validation errors |
| hidden_information | **required** | Visibility tier and redaction boundary | Check visibility tiers; apply redaction rules; verify hidden-info safety; filter projections by tier | Exposing backend_hidden content in player projections; bypassing redaction; ignoring visibility tiers |
| context_projection | **required** | Projection surface and visibility filtering | Build projection items; assemble filtered projections; apply visibility tiers | Building context packets; compiling model-facing prompts; bypassing visibility filters |
| persistence_boundary | **later / required** | Snapshot prepare boundary (no direct persistence) | Request snapshot preparation; reference persistence operation types | Performing direct database writes; bypassing persistence boundary; implementing durable storage |
| replay_audit | **later / required** | Audit and hash posture (no replay engine) | Reference replay records for audit; validate hash integrity references | Replaying events; restoring state; implementing replay engine; computing hashes for enforcement |
| runtime_trace | **required** | Traceable state read/projection decisions | Create trace entries for all state reads and projections; record operation type and subject reference | Omitting trace entries; using trace as state authority; modifying trace history |

---

## 10. Dependency and handoff boundaries

### 10.1 Command lifecycle / action legality service → State store

- **What state service may receive:** Accepted command references (command_id, lifecycle result with accepted_for_transaction_planning stage).
- **What state service must not decide:** Whether a command is legal; whether the command should proceed; action legality decisions.
- **Required kernel envelope / result:** CommandLifecycleResult with stage=accepted_for_transaction_planning; ActionLegalityResult with decision=legal.
- **Blocked until downstream exists:** Mutation processing blocked until transaction lifecycle service exists.

### 10.2 State store → Transaction lifecycle / event commitment service

- **What state service may pass:** Mutation requests referencing command_id, affected record_ids, proposed state_delta shape.
- **What state service must not decide:** Transaction commit/rollback; event ordering; event commitment.
- **Required kernel envelope / result:** state_delta envelope shape; transaction_preview reference (future).
- **Blocked until downstream exists:** All mutation execution blocked until transaction lifecycle service exists.

### 10.3 State store → Validation integration / invariant enforcement service

- **What state service may pass:** State record references and projection requests for validation.
- **What state service must not decide:** Validation rules; invariant definitions; validation severity.
- **Required kernel envelope / result:** ValidationResult from validation_pipeline.
- **Blocked until downstream exists:** Validation integration details blocked; shape validation available from kernel.

### 10.4 State store → Resource / consequence math service (future consumer)

- **What state service may pass:** Read-only state projections of resource-relevant records.
- **What state service must not decide:** Resource costs; consequence calculations; cost formulas.
- **Required kernel envelope / result:** State projection result with resource-relevant records.
- **Blocked until downstream exists:** Resource-aware projections blocked until RT-002 service exists.

### 10.5 State store → Combat / hazard / damage / recovery service (future consumer)

- **What state service may pass:** Read-only combat-scoped state projections.
- **What state service must not decide:** Damage; recovery; hazard effects; combat resolution.
- **Required kernel envelope / result:** State projection result with combat-relevant records.
- **Blocked until downstream exists:** Combat-scoped projections blocked until RT-003 service exists.

### 10.6 State store → Ability / effect / skill binding service (future consumer)

- **What state service may pass:** Read-only ability/effect-relevant state projections.
- **What state service must not decide:** Ability resolution; effect application; skill checks.
- **Required kernel envelope / result:** State projection result with ability-relevant records.
- **Blocked until downstream exists:** Ability-scoped projections blocked until RT-004 service exists.

### 10.7 State store → Inventory / item / vehicle / asset service (future consumer)

- **What state service may pass:** Read-only inventory state projections.
- **What state service must not decide:** Item creation/destruction; inventory capacity; asset mutation.
- **Required kernel envelope / result:** State projection result with inventory-relevant records.
- **Blocked until downstream exists:** Inventory-scoped projections blocked until RT-010 service exists.

### 10.8 State store → Mission / reward / clue routing service (future consumer)

- **What state service may pass:** Read-only mission/clue state projections.
- **What state service must not decide:** Clue discovery; reward distribution; mission state transitions.
- **Required kernel envelope / result:** State projection result with mission-relevant records.
- **Blocked until downstream exists:** Mission-scoped projections blocked until RT-006 service exists.

### 10.9 State store → Social / faction / actor knowledge service (future consumer)

- **What state service may pass:** Read-only faction/social state projections.
- **What state service must not decide:** Faction relationship changes; social state transitions; actor knowledge updates.
- **Required kernel envelope / result:** State projection result with faction/social-relevant records.
- **Blocked until downstream exists:** Faction/social projections blocked until RT-007 service exists.

### 10.10 State store → Generated-content provenance service (future consumer)

- **What state service may pass:** References to generated content with provenance status.
- **What state service must not decide:** Provenance authorization; durability authorization; content retention.
- **Required kernel envelope / result:** Record identity references with provenance markers.
- **Blocked until downstream exists:** Generated-content durability blocked until RT-008 service exists.

### 10.11 State store → Context-packet compiler (future)

- **What state service may pass:** Filtered, redacted projection results suitable for model-facing use.
- **What state service must not decide:** Prompt construction; context ordering; model-facing formatting; token budgets.
- **Required kernel envelope / result:** Projection result with model-facing safety verification.
- **Blocked until downstream exists:** All context-packet compilation blocked until context-packet compiler is authorized.

### 10.12 State store → Model evaluation harness (future)

- **What state service may pass:** Nothing directly. State store does not communicate with model evaluation.
- **What state service must not decide:** Model selection; model routing; prompt construction.
- **Required kernel envelope / result:** Not applicable — no direct handoff.
- **Blocked until downstream exists:** All model interaction blocked.

### 10.13 State store → Live-play adapter gate (future)

- **What state service may pass:** Nothing directly. State store does not communicate with live-play adapter.
- **What state service must not decide:** Live-play loop timing; session management; player interaction.
- **Required kernel envelope / result:** Not applicable — no direct handoff.
- **Blocked until downstream exists:** All live-play interaction blocked.

### 10.14 State store → Persistence boundary

- **What state service may pass:** Snapshot prepare requests via persistence_boundary kernel module.
- **What state service must not decide:** Storage backend; database schema; write strategy; durability guarantees.
- **Required kernel envelope / result:** PersistenceBoundaryRequest / PersistenceBoundaryResult.
- **Blocked until downstream exists:** Direct persistence writes blocked; snapshot preparation available through kernel boundary.

### 10.15 State store → Replay / hash audit

- **What state service may pass:** State references for audit hash verification; replay audit records.
- **What state service must not decide:** Replay strategy; state restoration; hash enforcement policy.
- **Required kernel envelope / result:** ReplayAuditRecord / HashAuditRecord references.
- **Blocked until downstream exists:** Replay engine blocked; audit reference available through kernel.

---

## 11. Future implementation architecture

This section defines the future implementation shape. **No code is implemented by PR-2.**

### Suggested future modules (for later implementation PR only)

- `src/astra_runtime/domain/state_store.py`
- `src/astra_runtime/domain/state_projection.py`

### Suggested public API (planning only)

**Error types:**

- `StateStoreError` — base error for state store operations.
- `InvalidStateRecordError` — invalid state record reference.
- `InvalidStateSnapshotError` — invalid state snapshot reference.
- `InvalidStateProjectionRequestError` — invalid projection request.
- `InvalidStateProjectionResultError` — invalid projection result.

**Data shapes:**

- `StateRecordRef` — immutable reference to a state record.
- `StateSnapshotRef` — immutable reference to a state snapshot.
- `StateProjectionRequest` — immutable projection request descriptor.
- `StateProjectionResult` — immutable projection result.

**Services:**

- `StateStoreService` — stateless service wrapper for state record operations.
- `StateProjectionService` — stateless service wrapper for projection operations.

**Factory functions:**

- `create_state_record_ref(...)` — create an immutable state record reference.
- `create_state_snapshot_ref(...)` — create an immutable state snapshot reference.
- `create_state_projection_request(...)` — create a projection request.
- `create_state_projection_result(...)` — create a projection result.

**Validation functions:**

- `validate_state_record_ref(...)` — validate state record reference shape.
- `validate_state_snapshot_ref(...)` — validate state snapshot reference shape.
- `validate_state_projection_request(...)` — validate projection request shape.
- `validate_state_projection_result(...)` — validate projection result shape.

**Projection functions:**

- `project_state_view(...)` — assemble a filtered projection from state references.

**These are proposed future symbols only and must not be created in PR-2.**

---

## 12. Future data shapes

This section defines future data shape requirements for planning only. No dataclasses or schemas are implemented.

### 12.1 State record reference

- **Required fields:** record_ref_id, record_type, record_id (full), schema_version, visibility_tier, metadata.
- **Relation to record identity:** Uses RecordId from record_identity for identity.
- **Relation to schema registry:** Schema version must match a registered schema in schema_registry.
- **Relation to state delta:** May be referenced as affected_record_id in StateDeltaEnvelope.
- **Relation to event ledger:** May be referenced in EventLedgerEntry actor_ids or target_ids.
- **Relation to hidden information / context projection:** visibility_tier must match HiddenInformationRecord visibility tiers.
- **Relation to validation result:** Must pass ValidationResult checks for record shape.
- **Relation to persistence boundary:** May be included in PersistenceBoundaryRequest for snapshot preparation.
- **Relation to replay / hash audit:** Must support hash computation for ReplayAuditRecord.
- **Relation to runtime trace:** All reads must produce RuntimeTraceEntry.
- **Hidden-info safety requirements:** visibility_tier must be respected in all projections; backend_hidden records must never appear in player-visible projections.

### 12.2 State snapshot reference

- **Required fields:** snapshot_ref_id, snapshot_scope, record_refs (list), snapshot_timestamp, schema_version, metadata.
- **Relation to record identity:** Each record_ref uses RecordId.
- **Relation to schema registry:** All referenced schemas must be registered.
- **Relation to state delta:** Snapshot reflects state after all committed deltas up to snapshot point.
- **Relation to event ledger:** Snapshot corresponds to a specific event sequence position.
- **Relation to hidden information / context projection:** Snapshot includes visibility_tier for each record.
- **Relation to validation result:** Must pass snapshot shape validation.
- **Relation to persistence boundary:** Primary input for PersistenceBoundaryRequest snapshot_prepare operations.
- **Relation to replay / hash audit:** Must support hash verification for ReplayAuditRecord.
- **Relation to runtime trace:** Snapshot creation must produce RuntimeTraceEntry.
- **Hidden-info safety requirements:** Snapshot includes all tiers but must be filtered before projection.

### 12.3 State projection request

- **Required fields:** projection_request_id, requesting_service, projection_type, scope, visibility_tiers_allowed, record_refs_requested, metadata.
- **Relation to record identity:** record_refs_requested use RecordId references.
- **Relation to schema registry:** Requested record types must be registered.
- **Relation to state delta:** Not directly related (projection reads current state, not pending deltas).
- **Relation to event ledger:** Not directly related (projection reads committed state).
- **Relation to hidden information / context projection:** visibility_tiers_allowed determines filtering.
- **Relation to validation result:** Request must pass shape validation before processing.
- **Relation to persistence boundary:** Not related (projections are ephemeral).
- **Relation to replay / hash audit:** Not directly related.
- **Relation to runtime trace:** Request must produce RuntimeTraceEntry.
- **Hidden-info safety requirements:** visibility_tiers_allowed must not include backend_hidden for player/model-facing projections.

### 12.4 State projection result

- **Required fields:** projection_result_id, projection_request_id, projection_type, items (list of projected records), visibility_tiers_applied, validation_id, metadata.
- **Relation to record identity:** Each item references a RecordId.
- **Relation to schema registry:** Each item's record type must match registered schema.
- **Relation to state delta:** Not directly related.
- **Relation to event ledger:** Not directly related.
- **Relation to hidden information / context projection:** visibility_tiers_applied records what filtering was done.
- **Relation to validation result:** Must carry validation_id from validation_pipeline check.
- **Relation to persistence boundary:** Not related (ephemeral).
- **Relation to replay / hash audit:** Not directly related.
- **Relation to runtime trace:** Result must produce RuntimeTraceEntry.
- **Hidden-info safety requirements:** Must guarantee no hidden payload leaks past visibility_tiers_applied.

### 12.5 State visibility descriptor

- **Required fields:** visibility_descriptor_id, record_ref, visibility_tier, redaction_label (if redacted), visible_to_actors (list), visible_to_scopes (list), metadata.
- **Relation to record identity:** record_ref uses RecordId.
- **Relation to schema registry:** Record type must be registered.
- **Relation to state delta:** Visibility may change via visibility_update change type.
- **Relation to event ledger:** Visibility changes are events.
- **Relation to hidden information / context projection:** Directly maps to HiddenInformationRecord visibility_tier.
- **Relation to validation result:** Must pass visibility shape validation.
- **Relation to persistence boundary:** Persisted with the state record.
- **Relation to replay / hash audit:** Visibility changes are auditable.
- **Relation to runtime trace:** Visibility checks produce trace entries.
- **Hidden-info safety requirements:** Visibility descriptor is the primary gate for hidden-info safety.

### 12.6 State projection dependency declaration

- **Required fields:** dependency_id, source_service, target_service, projection_types_required, visibility_tiers_required, metadata.
- **Relation to record identity:** Not directly related.
- **Relation to schema registry:** projection_types_required reference registered types.
- **Relation to state delta:** Not directly related.
- **Relation to event ledger:** Not directly related.
- **Relation to hidden information / context projection:** visibility_tiers_required determines filtering.
- **Relation to validation result:** Dependency shape must pass validation.
- **Relation to persistence boundary:** Not related.
- **Relation to replay / hash audit:** Not related.
- **Relation to runtime trace:** Dependency declarations produce trace entries.
- **Hidden-info safety requirements:** Visibility_tiers_required must be appropriate for the target service's authorization level.

### 12.7 State projection rejection / quarantine result

- **Required fields:** rejection_id, projection_request_id, reason_code, reason_message, quarantined (boolean), validation_issues (list), metadata.
- **Relation to record identity:** References the original projection request.
- **Relation to schema registry:** Not directly related.
- **Relation to state delta:** Not related.
- **Relation to event ledger:** Rejections may generate system_audit_events.
- **Relation to hidden information / context projection:** Rejection may be caused by visibility-tier violation.
- **Relation to validation result:** Carries validation_issues from validation_pipeline.
- **Relation to persistence boundary:** Not related (rejections are ephemeral).
- **Relation to replay / hash audit:** Rejections are auditable.
- **Relation to runtime trace:** Rejections must produce RuntimeTraceEntry.
- **Hidden-info safety requirements:** Rejection reason must not leak hidden information (e.g., must not reveal what hidden content was being protected).

---

## 13. Implementation PR authorization boundary

If this plan (RUNTIME-DOMAIN-PR-2) is accepted, the following implementation PR is authorized:

### RUNTIME-DOMAIN-PR-2A: State Store and State Projection Skeleton Implementation

**It may create only:**

- `src/astra_runtime/domain/state_store.py`
- `src/astra_runtime/domain/state_projection.py`
- Focused tests for state store / state projection skeleton.
- Registry / decision updates.
- Minimal authorized domain package export updates to `src/astra_runtime/domain/__init__.py`.

**It must remain skeleton-only and must not:**

- Mutate state.
- Apply state deltas.
- Commit events.
- Implement event sourcing.
- Implement durable persistence.
- Create database schemas.
- Replay events.
- Restore state.
- Execute commands.
- Calculate resources.
- Resolve combat.
- Resolve abilities / effects.
- Mutate inventory.
- Mutate missions / social state.
- Call models.
- Compile context packets.
- Run live play.

---

## 14. Test requirements for future implementation

The following test families must be created for RUNTIME-DOMAIN-PR-2A:

1. **Import / export integrity tests** — verify state_store and state_projection modules export expected symbols.
2. **State record reference validation tests** — verify StateRecordRef creation, shape validation, and immutability.
3. **State snapshot reference validation tests** — verify StateSnapshotRef creation and shape validation.
4. **Projection request / result validation tests** — verify StateProjectionRequest and StateProjectionResult creation and validation.
5. **Hidden-info redaction boundary tests** — verify that backend_hidden content is redacted in player-visible projections.
6. **Visible vs backend-hidden projection tests** — verify separation between full backend and player-visible projections.
7. **Schema registry reference tests** — verify state records reference registered schemas.
8. **Record identity reference tests** — verify state records use valid RecordId references.
9. **Validation result integration tests** — verify projection requests and results carry validation_id.
10. **State delta reference-only tests** — verify state store references delta shapes but does not apply them.
11. **Event ledger reference-only tests** — verify state store references event shapes but does not commit them.
12. **No state mutation guardrail tests** — verify no mutable state operations exist.
13. **No event commitment guardrail tests** — verify no event commitment operations exist.
14. **No persistence / write guardrail tests** — verify no direct persistence writes.
15. **No replay / restore guardrail tests** — verify no replay or state restoration operations.
16. **No model / prompt guardrail tests** — verify no model calls or prompt construction.
17. **Runtime trace declaration tests** — verify trace entry creation for state reads and projections.
18. **Command lifecycle handoff tests** — verify accepted command references are properly received.
19. **Downstream dependency declaration tests** — verify dependency declarations for future consumer services.
20. **Corpus-scale mixed record projection tests** — verify projection handles multiple record types from C00–C14 schema families.
21. **Adversarial hidden-info leak tests** — verify that no projection path leaks backend_hidden content.

---

## 15. Corpus-scale state pressure review

Because Astra must absorb 200–400 donor sources, the state store and projection service will face pressure from diverse entity types. This review maps each state category to the future state service's role.

| State Category | Schema Ref | Service Role | Notes |
|---|---|---|---|
| Creature / NPC state | C01 | **Projects** — provides read-only projections of creature/NPC records to consuming services (RT-003, RT-004, RT-007) | Visibility-tier filtering required for hidden NPC knowledge |
| Player / party state | (composite) | **Projects** — provides actor-scoped projections of player and party state | Hidden-info safety critical for multi-player hidden knowledge |
| Item / gear / inventory state | C02 | **Projects** — provides inventory projections to RT-010 | Ownership-scoped visibility filtering required |
| Ability / power / effect state | C03 | **Projects** — provides ability/effect projections to RT-004 | Some effects have hidden components |
| Relic / implant / installable state | C04 | **Projects** — provides installable asset projections to RT-010 | May have hidden properties |
| Faction / institution state | C05 | **Projects** — provides faction projections to RT-007 | Faction secrets require hidden-info filtering |
| Location / site / region state | C06 | **Projects** — provides location projections for scene-scoped use | Undiscovered locations require redaction |
| Mission / scenario / adventure state | C07 | **Projects** — provides mission projections to RT-006 | Clue/secret filtering critical |
| Vehicle / ship / platform state | C08 | **Projects** — provides vehicle projections to RT-010 | Ownership-scoped |
| Hazard / environment state | C09 | **Projects** — provides hazard projections to RT-003 | Some hazards are hidden |
| Table / oracle state or references | C10 | **References** — table definitions are reference data, not mutable state | RNG results tracked via rng_interface / table_oracle provenance |
| Companion / summon state | C11 | **Projects** — provides companion projections, actor-scoped | May have hidden properties |
| Crafting / salvage / recipe state | C12 | **Projects** — provides recipe projections | Recipe discovery may require hidden-info filtering |
| Map / diagram state | C13 | **References** — maps are reference data with fog-of-war projection | Undiscovered areas require redaction |
| Source-local setting / cosmology state | C14 | **References with quarantine** — source-local content is reference only, never canonical state without promotion | Must preserve source-local markers; RT-012 boundary enforced |
| Generated content state pending provenance | (RT-008) | **Quarantines** — generated content held pending provenance authorization | Must not become durable state without RT-008 gate |
| Hidden information and actor knowledge | (RT-005) | **Projects with redaction** — core hidden-info safety responsibility | Backend_hidden content never exposed in player projections |
| Campaign / world memory | (composite) | **Projects** — provides campaign-level state projections | Model summaries must never become authoritative memory |
| Temporary combat / encounter state | (RT-003) | **Projects** — provides encounter-scoped projections during combat | Ephemeral; discarded after encounter resolution |
| Downtime / domain-scale state | (composite) | **Projects** — provides downtime-period state projections | Slower lifecycle than combat state |

---

## 16. Guardrail review

The following items are explicitly blocked by this PR and must remain blocked:

- LLM state ownership.
- LLM memory authority.
- Narration as state.
- Summaries as state.
- Source-local content as state authority.
- Converted content as canon state.
- Generated content durability without provenance.
- State mutation without transaction / event path.
- Event commitment by state projection.
- Hidden information exposure through projections.
- Direct persistence writes.
- Replay / state restoration before replay engine authorization.
- Command execution by state service.
- Resource / combat / ability / inventory / mission / social logic inside state store.
- Context-packet compiler.
- Model integration.
- Prompt templates.
- Live-play adapter.
- UI runtime.
- Training.
- Pilot conversion.
- Sourcebook inclusion.
- Canon promotion.

---

## 17. Risk review

### 17.1 State store becomes mutable god object

- **Affected RT owners:** RT-001, RT-002, RT-003, RT-004, RT-005, RT-006, RT-007, RT-008, RT-010.
- **Mitigation:** State store is read/projection only. Mutation is deferred to transaction/event services. Skeleton implementation must have no mutable state operations.
- **Future test family:** No state mutation guardrail tests.
- **PR-2A must address:** Yes — skeleton must enforce immutability.

### 17.2 Projection becomes hidden-info leak

- **Affected RT owners:** RT-005, RT-001.
- **Mitigation:** All projections filtered through hidden_information visibility tiers. Redacted projections replace hidden content with labels.
- **Future test family:** Adversarial hidden-info leak tests; hidden-info redaction boundary tests.
- **PR-2A must address:** Yes — skeleton must enforce visibility-tier filtering.

### 17.3 Projections treated as authoritative state

- **Affected RT owners:** All consuming services.
- **Mitigation:** Projections are explicitly marked as derived. ProjectionResult type is distinct from authoritative state types.
- **Future test family:** Visible vs backend-hidden projection tests.
- **PR-2A must address:** Yes — type separation must be clear.

### 17.4 State service starts applying deltas

- **Affected RT owners:** RT-001, RT-002, RT-003, RT-004.
- **Mitigation:** State store references state_delta shapes but does not apply them. All mutation deferred to transaction service.
- **Future test family:** State delta reference-only tests; no state mutation guardrail tests.
- **PR-2A must address:** Yes — skeleton must not include delta application.

### 17.5 State service commits events

- **Affected RT owners:** All.
- **Mitigation:** State store references event_ledger shapes but does not commit events.
- **Future test family:** Event ledger reference-only tests; no event commitment guardrail tests.
- **PR-2A must address:** Yes — skeleton must not include event commitment.

### 17.6 State service bypasses validation

- **Affected RT owners:** RT-011.
- **Mitigation:** All projections and state references must pass validation_pipeline checks.
- **Future test family:** Validation result integration tests.
- **PR-2A must address:** Yes — validation integration must be structural.

### 17.7 State service bypasses transaction lifecycle

- **Affected RT owners:** RT-001.
- **Mitigation:** Mutation requests deferred to transaction service. State store does not execute mutations.
- **Future test family:** No state mutation guardrail tests.
- **PR-2A must address:** Yes — skeleton must enforce deferral.

### 17.8 Persistence gets implemented prematurely

- **Affected RT owners:** RT-011.
- **Mitigation:** State store uses persistence_boundary for snapshot preparation only. No direct persistence writes.
- **Future test family:** No persistence / write guardrail tests.
- **PR-2A must address:** Yes — skeleton must not include persistence writes.

### 17.9 Replay / hash audit becomes decorative

- **Affected RT owners:** RT-011.
- **Mitigation:** Replay audit references must be structural, not cosmetic. Hash posture must be genuine.
- **Future test family:** Runtime trace declaration tests.
- **PR-2A must address:** Partially — skeleton must reference replay_audit structurally.

### 17.10 Runtime trace omitted from state reads

- **Affected RT owners:** RT-011.
- **Mitigation:** All state reads and projections must produce RuntimeTraceEntry.
- **Future test family:** Runtime trace declaration tests.
- **PR-2A must address:** Yes — trace integration must be structural.

### 17.11 Generated content becomes durable state without provenance

- **Affected RT owners:** RT-008.
- **Mitigation:** Generated content held in quarantine until provenance authorization via RT-008.
- **Future test family:** Downstream dependency declaration tests.
- **PR-2A must address:** Partially — skeleton must declare dependency on RT-008.

### 17.12 Donor schema assumptions enter runtime state

- **Affected RT owners:** RT-012.
- **Mitigation:** Schema registry mediates all type references. Donor schemas do not become runtime state directly.
- **Future test family:** Schema registry reference tests.
- **PR-2A must address:** Yes — schema references must go through registry.

### 17.13 Source-local rules become canonical state

- **Affected RT owners:** RT-012.
- **Mitigation:** Source-local content carries provenance markers and cannot become canonical state without explicit promotion gate.
- **Future test family:** Corpus-scale mixed record projection tests.
- **PR-2A must address:** Partially — skeleton must preserve source-local markers.

### 17.14 Model summaries become memory / state authority

- **Affected RT owners:** RT-005, RT-008.
- **Mitigation:** Model output is never state authority. Summaries are narration artifacts, not state records.
- **Future test family:** No model / prompt guardrail tests.
- **PR-2A must address:** Yes — skeleton must have no model integration.

### 17.15 Context-packet compiler is built too early

- **Affected RT owners:** RT-005.
- **Mitigation:** PR-2 does not authorize context-packet compilation. State projection provides projection results, not compiled packets.
- **Future test family:** No model / prompt guardrail tests.
- **PR-2A must address:** Yes — skeleton must not include context-packet compilation.

---

## 18. Required future hardening ledger

| Hardening Item | Current Status | Risk Level | Required Before PR-2A | Future Owner | Recommended PR |
|---|---|---|---|---|---|
| State identity normalization | Not started | Medium | No | State store skeleton | PR-2A or later |
| State snapshot identity | Not started | Medium | No | State store skeleton | PR-2A |
| Projection request/result validation | Not started | High | Yes | State projection skeleton | PR-2A |
| Visibility-tier enforcement | Not started | Critical | Yes | State projection skeleton + RT-005 | PR-2A |
| Hidden-info-safe projection redaction | Not started | Critical | Yes | State projection skeleton + RT-005 | PR-2A |
| Validation integration | Not started | High | Yes | State store/projection + RT-011 | PR-2A |
| Runtime trace integration | Not started | High | Yes | State store/projection skeleton | PR-2A |
| Persistence boundary integration | Not started | Medium | No | State store skeleton + persistence_boundary | Later PR |
| Replay/hash audit integration | Not started | Medium | No | State store skeleton + replay_audit | Later PR |
| Transaction/event handoff | Not started | High | No | Future transaction lifecycle service | Later PR |
| Generated-content provenance handoff | Not started | Medium | No | Future RT-008 service | Later PR |
| Schema registry alignment | Not started | High | Yes | State store skeleton + schema_registry | PR-2A |
| Source-local/canon boundary enforcement | Not started | High | No | State store + RT-012 | Later PR |
| Adversarial hidden-info tests | Not started | Critical | Yes | State projection skeleton tests | PR-2A |
| Model-summary non-authority tests | Not started | High | Yes | State store skeleton tests | PR-2A |

---

## 19. Non-implementation reaffirmation

This PR adds no:

- Runtime code.
- Domain-service code.
- State-store implementation.
- State-projection implementation.
- Mutable runtime state.
- State reads as execution authority.
- State mutation.
- State delta application.
- Transaction lifecycle.
- Event commitment.
- Event sourcing implementation.
- Durable persistence.
- Database schema.
- Replay engine.
- Command execution.
- Command parser.
- Action legality engine expansion.
- Resource math.
- Combat resolution.
- Ability resolution.
- Inventory mutation.
- Mission / social mutation.
- Generated-content persistence.
- Context-packet compiler.
- Prompt templates.
- Model integration.
- Live-play adapter.
- UI / client.
- Generator implementation.
- Training data.
- Donor-content audit.
- Pilot conversion authorization.
- Sourcebook inclusion authorization.
- Canon promotion.

---

## 20. Gate finding

```yaml
gate_finding:
  state_store_state_projection_plan_defined: true
  ready_for_state_store_state_projection_skeleton_implementation_pr: true
  state_store_code_authorized_by_this_pr: false
  state_projection_code_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  state_delta_application_authorized_by_this_pr: false
  transaction_lifecycle_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  durable_persistence_authorized_by_this_pr: false
  replay_engine_authorized_by_this_pr: false
  command_execution_authorized_by_this_pr: false
  resource_math_authorized_by_this_pr: false
  combat_resolution_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  next_step_authorized: RUNTIME-DOMAIN-PR-2A state store and state projection skeleton implementation
  next_step_status: narrow_skeleton_implementation_pending_review
```

---

## 21. Classification block

```yaml
runtime_domain_pr_2:
  review_id: RUNTIME-DOMAIN-PR-2-STATE-STORE-STATE-PROJECTION-SERVICE-PLAN-001
  artifact_type: state_store_state_projection_service_plan
  implementation_status: non_executable_plan
  derives_from:
    - RUNTIME-DOMAIN-PR-1B-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-REVIEW-001
    - RUNTIME-DOMAIN-PR-1A-COMMAND-LIFECYCLE-ACTION-LEGALITY-SKELETON-IMPLEMENTATION-001
    - RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001
    - RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001
    - RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001
    - RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001
    - RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001
    - RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001
    - RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001
    - RT-001
    - RT-005
    - RT-011
  defines_state_ownership_model: true
  defines_state_projection_model: true
  defines_state_lifecycle_model: true
  defines_kernel_interface_consumption_plan: true
  defines_handoff_boundaries: true
  defines_future_implementation_architecture: true
  defines_future_data_shapes: true
  defines_future_test_requirements: true
  defines_corpus_scale_state_pressure_review: true
  defines_future_hardening_ledger: true
  authorizes_state_store_code_by_this_pr: false
  authorizes_state_projection_code_by_this_pr: false
  authorizes_mutable_runtime_state_by_this_pr: false
  authorizes_state_mutation_by_this_pr: false
  authorizes_state_delta_application_by_this_pr: false
  authorizes_transaction_lifecycle_by_this_pr: false
  authorizes_event_commitment_by_this_pr: false
  authorizes_event_sourcing_by_this_pr: false
  authorizes_durable_persistence_by_this_pr: false
  authorizes_database_schema_by_this_pr: false
  authorizes_replay_engine_by_this_pr: false
  authorizes_command_execution_by_this_pr: false
  authorizes_command_parser_by_this_pr: false
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
  next_allowed_step: RUNTIME-DOMAIN-PR-2A state store and state projection skeleton implementation, pending review
```

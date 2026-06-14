# RUNTIME-DOMAIN-PR-9: Post-PR-8 Runtime Generalization Planning

## 1. Purpose and status

This document is **RUNTIME-DOMAIN-PR-9**, a planning-only artifact that decides how to generalize the proof delivered by RUNTIME-DOMAIN-PR-8 into a reusable, backend-owned runtime execution path.

- **Type:** planning only, non-executable.
- **Status:** planning.
- **Authority:** no implementation authority unless a later review gate authorizes it.
- **Scope:** choose the next runtime generalization seam; define the constraints for the next implementation PR; identify the tests required before that implementation PR can be opened.

This PR does not implement code. It does not expand `tiny_vertical_slice.py`. It does not authorize live-play behavior, LLM narration authority, persistence implementation, RNG/table/oracle execution, arbitrary state mutation, conversion, or canon promotion.

---

## 2. Source ledger

### Direct predecessors

| Source ID | Title |
|-----------|-------|
| RUNTIME-DOMAIN-PR-8-TINY-VERTICAL-SLICE-001 | Tiny vertical slice (PR #302) |
| RUNTIME-DOMAIN-PR-8-TINY-VERTICAL-SLICE-002 | Tiny vertical slice increments 1–11 tests |
| PR-303-GUARDRAIL-BASELINE-CLEANUP-001 | Guardrail baseline cleanup after PR #303 rebase |

### Runtime skeleton dependencies (existing, not expanded)

| Source ID | Title |
|-----------|-------|
| RUNTIME-IMPL-PR-1-SCHEMA-REGISTRY-RECORD-IDENTITY-SKELETON-001 | Schema registry and record identity skeleton |
| RUNTIME-IMPL-PR-2-COMMAND-ENVELOPE-TRANSACTION-PREVIEW-SKELETON-001 | Command envelope and transaction preview skeleton |
| RUNTIME-IMPL-PR-3-STATE-DELTA-EVENT-LEDGER-ENVELOPE-SKELETON-001 | State delta and event ledger envelope skeleton |
| RUNTIME-IMPL-PR-4-DETERMINISTIC-RNG-TABLE-ORACLE-INTERFACE-SKELETON-001 | Deterministic RNG and table/oracle interface skeleton |
| RUNTIME-IMPL-PR-5-VALIDATION-PIPELINE-INVARIANT-PRECHECK-SKELETON-001 | Validation pipeline and invariant precheck skeleton |
| RUNTIME-IMPL-PR-6-HIDDEN-INFORMATION-PARTITION-CONTEXT-PROJECTION-SKELETON-001 | Hidden-information partition and context projection skeleton |
| RUNTIME-IMPL-PR-7-PERSISTENCE-BOUNDARY-REPLAY-HASH-AUDIT-RUNTIME-TRACE-SKELETON-001 | Persistence boundary, replay/hash audit, and runtime trace skeleton |
| RUNTIME-IMPL-PR-8-POST-KERNEL-SKELETON-REVIEW-DOMAIN-SERVICE-READINESS-GATE-001 | Post-kernel skeleton review and domain-service readiness gate |

### Earlier domain planning dependencies

| Source ID | Title |
|-----------|-------|
| RUNTIME-DOMAIN-PR-0-DOMAIN-SERVICE-IMPLEMENTATION-SEQUENCING-PLAN-001 | Domain service implementation sequencing plan |
| RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001 | Resource and consequence math service plan |
| RUNTIME-DOMAIN-PR-5A-RESOURCE-CONSEQUENCE-MATH-SKELETON-IMPLEMENTATION-001 | Resource/consequence math skeleton implementation |
| RUNTIME-DOMAIN-PR-6-CONTEXT-PACKET-COMPILER-SCOPE-ALIGNMENT-001 | Context packet compiler scope alignment |
| RUNTIME-DOMAIN-PR-7-MODEL-BOUNDARY-EVALUATION-SLICE-001 | Model boundary/evaluation harness planning slice |

### Registry and decision log

| Artifact | Path |
|----------|------|
| Doctrine registry | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` |
| Decision log | `docs/decisions/current_decisions_log.md` |

---

## 3. What PR-8 proved

PR-8 (`RUNTIME-DOMAIN-PR-8: Tiny Vertical Slice`, merged via PR #302) proved that a deterministic, backend-owned tiny vertical slice can be assembled end-to-end without collapsing backend authority into the LLM.

Specifically, PR-8 proved:

1. **Frozen state fixtures are sufficient to represent a scene.** `TinyVerticalSliceWorldState` and its nested frozen dataclasses (scene, actor, NPC, hazard clock, lever, injury, hidden fact) can be constructed deterministically, validated, serialized into visible and backend-only views, and round-tripped safely.
2. **Command lifecycle surfaces can be typed without executing commands.** The tiny slice defined a `TinyVerticalSliceCommand`, command-kind enumeration, and command validation, all as frozen reference surfaces.
3. **Resource planning previews can be computed without settlement.** The slice produced a `TinyVerticalSliceResourcePlanningPreview` that shows cost and availability as typed structures, without applying consequences or mutating state.
4. **Context packets can be assembled backend-side.** A `TinyVerticalSliceContextPacket` was produced from backend state and command intent, with explicit visibility tiers and no LLM-side hidden state.
5. **State delta candidates can be previewed without application.** The slice produced `TinyVerticalSliceStateDeltaCandidate` records that describe possible state changes, while leaving actual state mutation unimplemented.
6. **Event ledger candidates can be previewed without append.** The slice produced `TinyVerticalSliceEventLedgerCandidate` records that describe possible event entries, without an event store or commitment engine.
7. **Commit dry-run results can be produced without persistence.** The slice produced a `TinyVerticalSliceCommitDryRunResult` that simulates a transaction outcome while explicitly not writing state or events.
8. **Model boundary evaluation fixtures can be defined.** A `TinyVerticalSliceModelBoundaryEvaluationFixture` was created to evaluate how a model-facing packet relates to backend truth, without calling any model.
9. **Post-commit narration packets can be projected without narration generation.** A `TinyVerticalSlicePostCommitNarrationPacket` was produced as backend-owned output for a future narrator layer, without generating prose.
10. **Closure manifests can record what a PR does and does not authorize.** PR-8 ended with a closure manifest that explicitly lists forbidden scopes (live play, persistence, RNG execution, model calls, arbitrary state mutation, settlement, canon promotion).

The core proof is: **backend-owned typed assembly of a deterministic scene command flow is possible with the existing kernel skeletons, without any LLM authority, persistence side effects, or runtime execution engines.**

---

## 4. What PR-8 deliberately did not prove

PR-8 intentionally left the following unproven and unimplemented:

1. **Generalization beyond the single hard-coded scene.** PR-8 hard-coded one scene, one actor, one NPC, one hazard clock, one lever, one injury, and one hidden fact. It did not prove that arbitrary scene structures, actor configurations, or command kinds can be handled.
2. **Reusable command parser or intent interpreter.** PR-8 used typed command dataclasses. It did not prove parsing of natural-language player commands, model-structured output, or arbitrary command payloads.
3. **Actual action legality engine.** PR-8 included a legality-skeleton-style reference surface. It did not prove domain-specific legality rules, cost affordability, prerequisite checks, or authorization gates.
4. **Actual resource/consequence math execution.** PR-8 produced planning previews. It did not prove affordability resolution, cost reservation, consequence application, strain/backlash calculation, or reward distribution.
5. **Actual state mutation or delta application.** PR-8 previewed state delta candidates. It did not prove immutable state transitions, delta application, snapshot versioning, or rollback safety.
6. **Actual event commitment or ledger append.** PR-8 previewed event ledger candidates. It did not prove event append, hash-chain commitment, event ordering, or replay.
7. **Actual persistence read/write.** PR-8 used in-memory frozen fixtures. It did not prove persistence boundary calls, durable storage, snapshot writing, or restoration.
8. **Actual RNG/table/oracle execution.** PR-8 did not roll dice, draw from tables, or invoke oracles.
9. **Actual model calls or prompt execution.** PR-8 produced model-facing packets and evaluation fixtures but did not call any LLM, render prompts, or generate narration.
10. **Actual live-play adapter, session management, or UI/client.** PR-8 was a deterministic test fixture, not a playable session.
11. **Cross-domain integration.** PR-8 did not prove interaction between inventory, ability, combat, mission, social, or generated-content systems.
12. **Conversion, sourcebook inclusion, or canon promotion.** PR-8 stayed entirely within runtime reference surfaces.

---

## 5. What must become generalized next

The next narrow runtime tranche must generalize the hard-coded PR-8 flow into a **reusable backend-owned typed assembly path** while preserving all PR-8 non-authorities.

The generalization targets are, in priority order:

1. **Scene-agnostic runtime transaction assembly.** Replace the hard-coded `TinyVerticalSliceWorldState` with a typed assembly path that can accept a scene contract, actor list, command envelope, and produce a transaction assembly result. The scene contract must remain a reference/declaration surface, not a live-play engine.
2. **Command envelope consumption.** Generalize the PR-8 command dataclass into consumption of the existing `CommandEnvelope` kernel skeleton: validate envelope shape, dispatch by command kind, and produce a backend-owned intent record.
3. **Typed transaction preview pipeline.** Generalize the PR-8 resource-planning preview, state-delta candidate, event-ledger candidate, and commit dry-run result into a single transaction preview assembly that can be produced for any supported command kind.
4. **Kernel skeleton integration without implementation.** The next implementation PR must consume `command_envelope`, `transaction_preview`, `state_delta`, `event_ledger`, `validation_pipeline`, `hidden_information`, `context_projection`, `persistence_boundary`, `replay_audit`, and `runtime_trace` as interfaces, without implementing the engines behind them.
5. **Backend-owned context-packet projection.** Generalize the PR-8 context packet into a reusable projection from any transaction preview assembly, preserving visibility tiers and hidden-information boundaries.
6. **Backend-owned narration packet projection.** Generalize the PR-8 post-commit narration packet into a reusable projection from a transaction preview assembly, without generating prose.
7. **Model boundary evaluation fixture generalization.** Extend the PR-8 model boundary evaluation fixture so it can compare a generalized context/narration packet against backend truth, without calling a model.
8. **Guardrail integrity for generalized surfaces.** Every new generalized surface must carry the same anti-authority guardrails as PR-8: frozen dataclasses, no mutable runtime state, no persistence side effects, no LLM authority.

---

## 6. Existing modules that are candidates for generalization

The following existing modules are candidates for reuse or generalization in the next implementation PR. None of them should be expanded into live-play engines.

| Module | Path | Candidate role in generalization |
|--------|------|----------------------------------|
| `resource_consequence_math` | `src/astra_runtime/domain/resource_consequence_math.py` | Reuse frozen cost/proposal/result shapes for transaction preview assembly. Do not add formulas or execution. |
| `command_lifecycle` | `src/astra_runtime/domain/command_lifecycle.py` | Reuse command envelope and lifecycle surfaces for generalized command consumption. |
| `action_legality` | `src/astra_runtime/domain/action_legality.py` | Reuse legality reference surfaces for intent validation. Do not implement a legality engine. |
| `transaction_lifecycle` | `src/astra_runtime/domain/transaction_lifecycle.py` | Reuse transaction stage and result surfaces for preview assembly. |
| `event_commitment` | `src/astra_runtime/domain/event_commitment.py` | Reuse event ledger candidate surfaces for preview assembly. |
| `state_projection` | `src/astra_runtime/domain/state_projection.py` | Reuse projection request/result surfaces for visible-state packets. |
| `state_store` | `src/astra_runtime/domain/state_store.py` | Reuse immutable state record/snapshot surfaces for input state fixtures. |
| `validation_integration` | `src/astra_runtime/domain/validation_integration.py` | Reuse validation result/failure route surfaces for preview assembly. |
| `tiny_vertical_slice` | `src/astra_runtime/domain/tiny_vertical_slice.py` | Treated as a closed proof-of-concept. Do not expand. Its patterns may inform the generalized module, but no PR-9 code may add to it. |
| `schema_registry` | `src/astra_runtime/kernel/schema_registry.py` | Consume for typed record identity and schema-key references. |
| `record_identity` | `src/astra_runtime/kernel/record_identity.py` | Consume for stable refs in transaction assembly. |
| `command_envelope` | `src/astra_runtime/kernel/command_envelope.py` | Consume for command envelope shape and validation. |
| `transaction_preview` | `src/astra_runtime/kernel/transaction_preview.py` | Consume for transaction preview envelope shape. |
| `state_delta` | `src/astra_runtime/kernel/state_delta.py` | Consume for state delta envelope shape. |
| `event_ledger` | `src/astra_runtime/kernel/event_ledger.py` | Consume for event ledger entry shape. |
| `validation_pipeline` | `src/astra_runtime/kernel/validation_pipeline.py` | Consume for validation request/result shape. |
| `hidden_information` | `src/astra_runtime/kernel/hidden_information.py` | Consume for hidden-info partition references. |
| `context_projection` | `src/astra_runtime/kernel/context_projection.py` | Consume for context projection request/result shape. |
| `persistence_boundary` | `src/astra_runtime/kernel/persistence_boundary.py` | Consume for prepare-only persistence request shape. |
| `replay_audit` | `src/astra_runtime/kernel/replay_audit.py` | Consume for audit hash references. |
| `runtime_trace` | `src/astra_runtime/kernel/runtime_trace.py` | Consume for trace entry references. |

---

## 7. Boundaries that must remain backend-owned

The next implementation PR must preserve backend ownership of the following boundaries. None may be delegated to the LLM.

1. **Truth state.** Any state that represents "what is currently actual" must be owned by the backend. The LLM may receive a context packet, but it does not hold truth.
2. **Command intent record.** The translation of a player/model input into a typed command intent must be backend-owned and auditable.
3. **Transaction preview assembly.** The sequence of cost preview, state delta candidate, event ledger candidate, and commit dry-run result must be assembled backend-side.
4. **Validation gate references.** References to validation requests, results, failure routes, and quarantine routes must be backend-owned.
5. **Hidden-information partition.** What is visible vs. backend-only must be decided by the backend, not inferred by the model.
6. **Context packet and narration packet structure.** The shape, budget, and visibility tiers of model-facing packets must be backend-defined.
7. **Event ordering and hash references.** References to event ledger ordering, replay hashes, and audit hashes must be backend-owned.
8. **Persistence prepare boundary.** Any persistence request must be a prepare-only envelope; actual write authority remains unimplemented in PR-9.
9. **Trace and provenance references.** Runtime trace entries and provenance linkages must be backend-owned.
10. **Deterministic output.** For any given input state and command intent, the transaction preview assembly must be deterministic.

---

## 8. LLM/model-facing boundaries that remain forbidden

The next implementation PR must not create or rely on the following LLM/model-facing boundaries:

1. **Model calls.** No OpenAI, local 8B, or other LLM API calls.
2. **Prompt templates.** No prompt template assembly or rendering.
3. **Prompt execution.** No execution of rendered prompts.
4. **Prose parsing.** No parsing of model-generated prose into structured commands or state.
5. **Narration generation.** No generation of scene narration, summaries, or clarification text.
6. **Model memory as truth.** No reliance on model-side memory, hidden state, or context as authoritative state.
7. **Model-side dice or table rolls.** No randomness delegated to a model.
8. **Model-side file writing.** No model-driven persistence, export, or canon promotion.
9. **Model-side validation authority.** The model may be evaluated; it may not be the validator.
10. **Live-play adapter.** No session engine, input router, output delivery, or UI/client.

---

## 9. Tests that should gate the next implementation PR

The next implementation PR (tentatively the "runtime transaction assembly" or "scene command execution skeleton" PR) should be gated by the following test families:

1. **Frozen surface tests.** Every new dataclass must be frozen and deep-copy safe.
2. **Factory/validator parity tests.** Every public surface must have a factory function and a validator function with matching invariants.
3. **Command envelope consumption tests.** The assembly path must consume the kernel `CommandEnvelope` shape and reject malformed envelopes.
4. **Scene contract tests.** The assembly path must accept a scene contract with multiple actors, objects, and hidden facts, and still produce deterministic output.
5. **Transaction preview assembly tests.** For a valid command intent, the path must produce a resource preview, state delta candidate, event ledger candidate, and commit dry-run result as separate, immutable structures.
6. **No-state-mutation tests.** After assembly, the input world state must remain unchanged.
7. **No-persistence-write tests.** No module may call a persistence writer, file writer, or database connector.
8. **No-RNG-execution tests.** No dice roll, table draw, or oracle invocation may occur.
9. **No-model-call tests.** No model API call, prompt template rendering, or narration generation.
10. **Hidden-information safety tests.** Model-facing packets must not contain backend-only facts unless explicitly redacted into reference-only form.
11. **Context packet projection tests.** A generalized context packet must be projectable from any transaction preview assembly.
12. **Narration packet projection tests.** A generalized post-commit narration packet must be projectable from any transaction preview assembly.
13. **Model boundary evaluation tests.** A model boundary evaluation fixture must be able to compare the projected packets against backend truth.
14. **Kernel dependency tests.** Every new module must consume kernel interfaces rather than bypass them.
15. **Guardrail module-existence tests.** No new module may introduce a live-play adapter, UI/client, prompt template package, model integration package, or durable store package.
16. **Determinism tests.** Repeated assembly from the same inputs must produce byte-identical or structurally identical outputs.
17. **Error hierarchy tests.** All assembly errors must derive from a shared runtime-domain error base.

---

## 10. What the next implementation PR is allowed to touch

The next implementation PR is allowed to touch only the following:

1. A new narrow module (candidate names: `runtime_transaction_assembly.py` or `scene_command_execution_skeleton.py`) under `src/astra_runtime/domain/`.
2. New frozen dataclasses for scene contract, command intent record, transaction assembly result, transaction preview assembly, generalized context packet, generalized narration packet, and generalized model boundary evaluation fixture.
3. Stateless factory and validator functions for those dataclasses.
4. Consumption of existing kernel skeleton interfaces (`command_envelope`, `transaction_preview`, `state_delta`, `event_ledger`, `validation_pipeline`, `hidden_information`, `context_projection`, `persistence_boundary`, `replay_audit`, `runtime_trace`).
5. Consumption of existing domain skeleton surfaces (`command_lifecycle`, `action_legality`, `transaction_lifecycle`, `event_commitment`, `state_projection`, `state_store`, `validation_integration`, `resource_consequence_math`).
6. Updates to `src/astra_runtime/domain/__init__.py` to export the new public surfaces.
7. A focused test file (or files) under `tests/` that exercises the new module with the gating tests listed in section 9.
8. Registry and decision-log entries to track the new artifact.

---

## 11. What the next implementation PR must not touch

The next implementation PR must not touch or expand:

1. `tiny_vertical_slice.py` or its tests.
2. Generalized live-play behavior or a live-play adapter.
3. LLM narration authority or prose generation.
4. Persistence implementation, database schema, durable storage, or replay engine.
5. RNG/dice/table/oracle execution.
6. Arbitrary state mutation or actual state delta application.
7. Actual event commitment or event ledger append.
8. PR-5 arithmetic execution (affordability, reservation, settlement, consequence application).
9. Settlement authorization.
10. Broad consequence application across multiple domains.
11. Conversion, sourcebook inclusion, or canon promotion behavior.
12. Prompt templates, prompt execution, or model adapter code.
13. UI/client, session engine, or input parser.
14. Existing kernel skeleton implementations beyond consuming their public surfaces.
15. Existing domain skeleton implementations beyond consuming their public surfaces.

---

## 12. Lawful escalation points

If runtime generalization requires new doctrine, the following escalation points are lawful:

1. **RT-001 command lifecycle / action legality owner specification.** If the generalized command envelope requires new legality semantics, escalate to a future RUNTIME-DOMAIN-PR-1 implementation or a dedicated RT-001 owner-spec update; do not invent legality rules in PR-9.
2. **RT-002 resource / consequence math owner specification.** If transaction preview assembly requires new cost shapes, reuse the existing `resource_consequence_math.py` surfaces. If new shapes are required, escalate to a PR-5B–PR-5I planning hardening cycle or a dedicated RT-002 owner-spec update.
3. **RT-003 combat / hazard / damage / recovery owner specification.** If the scene contract must represent combat state, escalate to RT-003 owner specification; do not implement combat rules in PR-9.
4. **RT-004 ability / effect / skill binding owner specification.** If the scene contract must represent abilities or effects, escalate to RT-004 owner specification; do not implement ability resolution in PR-9.
5. **RT-005 context packet and hidden information owner specification.** If visibility tiers or packet budgets need expansion, escalate to RT-005 owner specification.
6. **RT-006 mission / reward / clue routing owner specification.** If the scene contract must represent objectives, clues, or rewards, escalate to RT-006 owner specification.
7. **RT-007 social / faction / actor knowledge owner specification.** If the scene contract must represent social state or actor knowledge, escalate to RT-007 owner specification.
8. **RT-008 generated content provenance and recurrence owner specification.** If the transaction assembly produces generated-content references, escalate to RT-008 owner specification.
9. **RT-009 runtime RNG and table/oracle owner specification.** If any command kind requires randomness, escalate to RT-009 owner specification; PR-9 must not implement RNG.
10. **RT-010 inventory / item / vehicle / asset owner specification.** If the scene contract must represent inventory state, escalate to RT-010 owner specification.
11. **RT-011 validation readiness and tooling owner specification.** If new validation surfaces are required, escalate to RT-011 owner specification.
12. **RT-012 D-series promotion boundary owner specification.** If any output could be misconstrued as canon or sourcebook material, escalate to RT-012 owner specification.
13. **Astra Doctrine Council review.** If the escalation crosses multiple RT owners or threatens guardrail integrity, the PR-9 implementation must pause and request explicit review before proceeding.

---

## 13. Gate finding

```yaml
gate_finding:
  pr_8_tiny_vertical_slice_proved: true
  backend_owned_deterministic_assembly_possible: true
  llm_not_game_engine: preserved
  next_step_type: planning_only
  next_step_authorized: runtime_transaction_assembly_or_scene_command_execution_skeleton_planning
  next_implementation_pr_title_candidate: RUNTIME-DOMAIN-PR-9A: Scene Command Execution Skeleton (Backend-Owned Typed Assembly)
  direct_implementation_authorized_by_this_pr: false
  direct_live_play_authorized_by_this_pr: false
  direct_model_integration_authorized_by_this_pr: false
  direct_persistence_authorized_by_this_pr: false
  direct_rng_execution_authorized_by_this_pr: false
  direct_state_mutation_authorized_by_this_pr: false
  direct_event_commitment_authorized_by_this_pr: false
  direct_settlement_authorized_by_this_pr: false
  direct_consequence_application_authorized_by_this_pr: false
  direct_conversion_or_canon_promotion_authorized_by_this_pr: false
```

---

## 14. Non-implementation reaffirmation

This document authorizes no code. It authorizes only the planning of the next narrow runtime generalization seam. Any implementation PR opened from this plan must be reviewed separately and must preserve every guardrail listed in sections 7, 8, 10, 11, and 12.

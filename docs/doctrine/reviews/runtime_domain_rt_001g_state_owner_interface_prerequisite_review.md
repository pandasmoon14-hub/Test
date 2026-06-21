# RUNTIME-DOMAIN-RT-001G — State Owner Interface Prerequisite Review

**Date:** 2026-06-16
**Artifact ID:** RUNTIME-DOMAIN-RT-001G-STATE-OWNER-INTERFACE-PREREQUISITE-REVIEW-001
**Follows:** RUNTIME-DOMAIN-RT-001F (action legality service interface contract hardening review, merged as PR #316)
**Status:** review-only — no runtime behavior, no implementation authority

---

## 1. Purpose and scope

RT-001G is a **prerequisite review** over the state-owner and dependency-owner interface requirements that must exist before a real action legality evaluation service may read state, inspect projections, call owner services, or emit real legality results. It is explicitly **review-only** — it does not implement a state owner interface, a state owner service, a dependency owner service, or an action legality evaluation service.

RT-001G does not implement, authorize, or enable:

- State owner service
- State reads
- State mutation
- Action legality evaluation
- Command execution
- Event append or event commitment
- Persistence/replay writes
- RNG/table/oracle execution
- Resource/consequence math execution
- Model calls, prompt rendering, narration, live-play, or UI behavior
- Conversion, sourcebook inclusion, or canon promotion

This review identifies the minimum interface families that must be defined, reviewed, and skeletonized before any real legality evaluation can be attempted. The next recommended step is **RT-001H — State Owner Interface Contract Skeleton**, not action legality evaluation implementation.

---

## 2. Source stack reviewed

| PR | Title | Merged as |
|---|---|---|
| RT-001A / PR #311 | Action Legality Service Plan and Execution Boundary Review | PR #311 |
| RT-001B / PR #312 | Action Legality Skeleton Dataclasses, Constants, Validators, Serializers | PR #312 |
| RT-001C / PR #313 | Action Legality Gate Integration Skeleton | PR #313 |
| RT-001D / PR #314 | Action Legality Integration Hardening Review | PR #314 |
| RT-001E / PR #315 | Action Legality Service Interface Contract Skeleton | PR #315 |
| RT-001F / PR #316 | Action Legality Service Interface Contract Hardening Review | PR #316 |

---

## 3. Why real action legality evaluation is still blocked

A real action legality evaluator must answer questions such as:

- Does the actor exist and is it valid?
- Does the actor have the capability and authority to attempt this command?
- Is the target reachable within the current scene/location?
- Does the actor have the required resources, items, or conditions?
- Is hidden information being improperly required?
- Are donor-specific action economies being treated as baseline law?

None of these questions can be answered safely by reading raw world state directly. Each question belongs to an owner service that understands the relevant state semantics, visibility rules, and mutation boundaries. The existing RT-001B through RT-001F surfaces are intentionally reference-only and default to `deferred` or `unknown`. They carry dependency manifests that name future owner routes, but no owner services exist yet.

Therefore, real action legality evaluation remains blocked until the state-owner and dependency-owner interface families identified in this review are defined and available. RT-001E must continue returning only `deferred` or `unknown` until superseded by a reviewed implementation.

---

## 4. Required state owner interface families

The following state owner interface families must exist before real legality evaluation can read state safely:

### SO-01 — Actor existence and identity owner

Owns actor record identity, actor lifecycle state (alive, dead, suspended, present), and actor-to-command binding. Legality may ask whether an actor identity resolves, but may not inspect raw actor records directly.

### SO-02 — Actor capability/authority owner

Owns capability categories, authority grants, permission gates, and action-economy posture for an actor. Legality may ask whether an actor has a required capability or authority, but may not compute capability derivations itself.

### SO-03 — Scene/location boundary owner

Owns scene identity, scene type, location bounds, and contextual validity of command families within a scene. Legality may ask whether a command is contextually valid for a scene, but may not read raw scene geometry or state directly.

### SO-04 — Target existence and reachability owner

Owns target identity resolution, target presence, and reachability/scope relative to an actor and scene. Legality may ask whether a target is reachable, but may not compute distances, movement costs, or targeting math.

### SO-05 — Object/lever/interactable owner

Owns interactive objects, levers, containers, doors, and other scene interactables. Legality may ask whether an interaction is permitted, but may not inspect raw object state or trigger object behavior.

### SO-06 — Hazard/clock/environment owner

Owns environmental hazards, clocks, timing constraints, per-turn limits, cooldowns, and phase gates. Legality may ask whether timing permits an action, but may not advance clocks or compute durations.

### SO-07 — Inventory/custody/burden owner

Owns inventory state, custody chains, burden, equipment, and item availability. Legality may ask whether an item is present or available for use, but may not mutate inventory or resolve item effects.

### SO-08 — Resource pool/state owner

Owns resource pools, resource categories, and resource availability declarations. Legality may ask whether a resource category exists and whether the actor has a relevant pool, but may not calculate affordability, reservation, or settlement.

### SO-09 — Condition/injury/status owner

Owns condition, injury, status, and temporary effect state on actors and targets. Legality may ask whether a condition blocks an action category, but may not resolve condition mechanics or recovery.

### SO-10 — Faction/social/relationship owner

Owns faction standing, reputation, relationship state, social permission gates, and institutional authority. Legality may ask whether a social/faction gate blocks an action, but may not mutate relationships or compute social consequences.

### SO-11 — Mission/clue/reward/discovery owner

Owns mission state, clue availability, reward eligibility, and discovery flags. Legality may ask whether a mission-related action is valid, but may not reveal hidden clues or assign rewards.

### SO-12 — Hidden information visibility owner

Owns the partition between player-known, actor-known, GM-known, and hidden-backend-only information. Legality must route hidden-information questions to this owner and must never infer hidden truth from missing data.

### SO-13 — State projection owner

Owns the construction of read-only state projections from state record references and snapshots. Legality must consume only validated projections, not raw state store records.

### SO-14 — Transaction preview owner

Owns the transaction preview contract and proposed-delta references. Legality may declare that a transaction preview is required, but may not build or execute the preview itself.

### SO-15 — Event commitment owner

Owns event commitment requests, validation, and rejection. Legality may declare an event commitment dependency, but may never append events or commit state changes.

### SO-16 — Persistence/replay owner

Owns persistence boundaries, replay audit references, and snapshot durability. Legality may carry persistence/replay references for traceability, but may not write to persistence or replay systems.

---

## 5. Required dependency owner interface families

The following dependency owner interface families must be available for legality to route unresolved dependencies instead of fabricating decisions:

### DO-01 — validation owner

Receives structural and schema validation questions. Legality depends on validation results but does not perform validation itself.

### DO-02 — resource math owner

Receives resource existence, cost category, and affordability questions. Legality declares resource dependencies but does not execute resource math.

### DO-03 — RNG/table/oracle owner

Receives randomness, table draw, and oracle invocation questions. Legality declares RNG/table/oracle dependencies but does not roll dice or draw from tables.

### DO-04 — state delta owner

Owns proposed state changes and delta validation. Legality may require a proposed delta for downstream transaction planning but does not compute deltas.

### DO-05 — transaction lifecycle owner

Owns transaction stage progression, precondition satisfaction, and commitment readiness. Legality feeds into transaction planning but does not manage the lifecycle.

### DO-06 — event commitment owner

Owns event commitment decisions and event ledger append authority. Legality declares event commitment dependencies but never commits events.

### DO-07 — context packet owner

Owns context packet assembly, visibility redaction, and narrator-facing output. Legality results are consumed by the context packet owner; legality does not compile packets.

### DO-08 — persistence/replay owner

Owns durable persistence writes and replay audit trails. Legality produces trace references but does not write persistence or replay records.

### DO-09 — doctrine/schema/source-local escalation owner

Owns doctrine gap review, schema gap review, and source-local/donor-specific quarantine decisions. Legality escalates unresolved doctrine questions but does not decide canon or sourcebook inclusion.

### DO-10 — combat/ability/skill/effect resolution owner, as future prerequisites only

Owns combat resolution, ability binding, skill evaluation, and effect resolution. Legality may declare these dependencies for future resolution but does not resolve them. This family is a downstream prerequisite, not a state-read dependency.

---

## 6. Minimum state read contract requirements

Before a future legality evaluator may read state, the following contract requirements must be met:

1. **Explicit owner contracts only.** Every state read must be mediated by an owner service interface identified in Section 4. No direct raw state access is permitted. A future action legality evaluator must not read raw world state directly.
2. **Typed references.** Legality must pass typed `StateRecordRef`, `StateSnapshotRef`, or `StateProjectionRequest` references, not bare record IDs or ad-hoc keys.
3. **Read-only authority.** Legality must hold no mutation, append, or commitment authority. State read interfaces must be contractually read-only.
4. **Visibility rules enforced.** Every projection returned to legality must carry a `StateVisibilityDescriptor` and a visibility tier. Legality must not request backend-hidden data for player-facing decisions.
5. **No side effects.** State read operations must not modify state, advance clocks, consume resources, or trigger downstream events.
6. **Missing data handling.** Missing or unavailable state must be reported as missing, not as a false truth. Legality must route missing-data cases to `deferred`, `unknown`, or `escalated` rather than inferring legality.
7. **Audit trace.** Every state read request must be traceable via a runtime trace reference for future replay and audit.

---

## 7. Minimum projection and visibility contract requirements

State projections consumed by legality must satisfy:

1. **Projection owner mediation.** All projections must be produced by the state projection owner (SO-13), not by legality or by raw state traversal.
2. **Redaction by default.** Projections used for player-visible legality decisions must be redacted to player-visible or actor-visible tiers.
3. **No backend-hidden leakage.** Legality must not use backend-hidden projections to produce player-visible messages or visible blocker messages.
4. **Projection type validation.** Projection types must belong to a controlled set (e.g., `actor_scoped`, `scene_scoped`, `inventory_asset`, `hidden_info_redacted`).
5. **Status accountability.** Projection results must carry a status (`requested`, `validated`, `materialized`, `redacted`, `rejected`, `quarantined`) so legality can distinguish available from unavailable data.
6. **Dependency disclosure.** Projections must declare their dependencies so legality can build accurate dependency manifests.

---

## 8. Hidden-information containment requirements

Hidden-information containment is a hard prerequisite for real legality evaluation:

1. **No inference from absence.** The legality evaluator must not infer hidden truth from missing data. A missing projection or rejected state read must result in `deferred`, `unknown`, or `escalated`, not a fabricated blocker.
2. **Owner routing for hidden facts.** Any question that depends on information the actor does not know must be routed to the hidden information visibility owner (SO-12).
3. **Generic safe messages only.** Player-visible blocker messages for hidden-information cases must use only generic safe messages such as "Not enough information to attempt this action." and "This action cannot be taken right now."
4. **No hidden detail in visible output.** Player-visible legality results must never reveal the existence, type, location, or state of hidden entities, objects, hazards, or conditions.
5. **Backend-only blocker detail.** Specific hidden-information reasons may appear only in backend-only detail records, not in visible serializers.
6. **Redaction before serialization.** Any projection that could contain hidden information must be redacted before being used to build player-visible output.

---

## 9. Actor, target, scene, object, hazard, inventory, faction, and resource ownership boundaries

The following ownership boundaries separate state that legality may reference from state that legality must not own or mutate:

| Domain | Legality may reference | Legality must not own or mutate |
|---|---|---|
| Actor | Actor existence, identity, capability/authority through SO-01/SO-02 | Actor creation, deletion, state mutation, advancement, injury, death |
| Target | Target existence and reachability through SO-04 | Target creation, deletion, HP, damage, condition mutation |
| Scene/location | Scene identity and contextual validity through SO-03 | Scene geometry, terrain state, encounter state, transition logic |
| Object/lever/interactable | Interaction permission through SO-05 | Object state mutation, lock/unlock, open/close, trigger logic |
| Hazard/clock/environment | Timing permission through SO-06 | Hazard activation, clock advancement, duration computation |
| Inventory | Item presence and availability through SO-07 | Inventory mutation, item consumption, equipment change, transfer |
| Faction/social | Social/faction permission through SO-10 | Reputation change, relationship change, faction response |
| Resource | Resource category existence and pool reference through SO-08 | Resource math, affordability, reservation, settlement |

Legality acts as a consumer of owner-mediated facts, not as a resolver of domain mechanics.

---

## 10. Transaction preview and event commitment prerequisites

Before a real legality evaluator can produce `legal` results that lead to transaction planning, the following must exist:

1. **Transaction lifecycle interface.** A transaction lifecycle owner (DO-05) must define `TransactionRequest`, `TransactionPlan`, and `TransactionResult` contracts and expose a read-only planning interface.
2. **Transaction preview interface.** A transaction preview owner (SO-14) must define how proposed deltas are referenced and how preview requests are built from legality results.
3. **Event commitment interface.** An event commitment owner (DO-06/SO-15) must define event commitment requests, decisions, and rejection contracts.
4. **No legality-side commitment.** Legality must never set `ready_for_event_commitment=True`, append events, apply deltas, or persist snapshots.
5. **Reference-only handoff.** Legality may pass transaction preview references and event commitment references to downstream services, but may not execute them.

---

## 11. Resource/consequence math prerequisites

Before legality can evaluate resource-related gates, the following must exist:

1. **Resource math owner interface.** The resource math owner (DO-02) must expose a read-only interface for resource category existence, pool reference, and cost structure reference.
2. **No affordability execution.** Legality may confirm that a resource category exists but may not calculate whether the actor can afford a cost.
3. **No settlement authority.** Legality must not authorize reservation, settlement, or consequence application.
4. **Dependency declaration only.** Legality must declare `resource_math` dependencies in the dependency manifest and defer to the resource math owner.
5. **Cost category validation.** The resource math owner must validate that referenced cost categories belong to controlled resource families and quantity representation kinds.

---

## 12. RNG/table/oracle prerequisites

Before legality can evaluate actions that involve randomness, the following must exist:

1. **RNG/table/oracle owner interface.** The RNG/table/oracle owner (DO-03) must expose a request/result contract for random draws, table lookups, and oracle invocations.
2. **No direct randomness execution.** Legality must not roll dice, draw from tables, or invoke oracles.
3. **Dependency declaration only.** Legality must declare `rng_table_oracle` dependencies and route them to the owner.
4. **Hidden-result handling.** Random results that must remain hidden must be redacted by the owner before any projection reaches legality.
5. **Seed/replay reference.** Random operations must carry seed or replay references for deterministic audit.

---

## 13. Persistence/replay prerequisites

Before legality can participate in durable runtime traces, the following must exist:

1. **Persistence boundary owner interface.** The persistence/replay owner (SO-16/DO-08) must define persistence boundary references and snapshot contracts.
2. **Read-only trace consumption.** Legality may consume trace references for context but may not write to persistence.
3. **Replay audit references.** Every state read and projection request used by legality must be replay-auditable via trace IDs and snapshot references.
4. **No state mutation.** Legality must not trigger persistence writes, snapshot creation, or replay event generation.
5. **Reference-only handoff.** Legality may carry persistence/replay references in results for downstream consumption, but may not execute persistence operations.

---

## 14. Import and authority boundary requirements

A future action legality evaluation module must respect the following import and authority boundaries:

1. **No raw state_store imports.** The evaluator must not import `state_store` directly to read raw records. It must consume only `state_projection` mediated projections.
2. **No transaction_lifecycle/event_commitment execution imports.** The evaluator may import reference types only, not execution builders.
3. **No resource_consequence_math execution imports.** The evaluator may import reference/declaration types only, not calculation functions.
4. **No model/live_play imports.** Legality must not call models, render prompts, or invoke live-play adapters.
5. **No conversion/canon/sourcebook imports.** Legality must not promote content or perform conversion.
6. **Authority flags false-by-default.** Any evaluator authority flags must default to `False` and reject non-`False` values for mutation, execution, or commitment authorities.
7. **Owner-route dependency manifests.** All unresolved dependencies must be captured as owner-route strings in dependency manifests, not resolved by legality.

---

## 15. Corpus-scale donor pressure audit

RT-001G reaffirms the RT-001A/RT-001D/RT-001F donor-neutrality posture:

- **No donor action economy as baseline law.** Donor-specific concepts such as swift actions, bonus actions, fate points, edges, bennies, spell slots, or action points must not become default legality rules. They must be quarantined as source-local/donor-specific until reviewed under RT-012.
- **No donor-specific capability taxonomies.** Capability/authority checks must use donor-agnostic owner interfaces, not donor class names.
- **No donor-specific reachability math.** Reachability must be answered by the target reachability owner, not by donor movement rules.
- **No donor-specific resource categories as universal.** Resource categories must be declared through the resource math owner and validated against donor-neutral resource families.
- **Source-local escalation.** Any command that cannot be evaluated without donor-specific rules must be escalated or quarantined, not silently approved.

---

## 16. Risk ledger

### R1 — premature state read risk

**Risk:** A future legality evaluator could attempt to read state before the required state owner interfaces are defined and available, producing incorrect or fabricated legality decisions.

**Mitigation:** RT-001G identifies the required owner interface families and mandates that all state reads be routed through explicit owner contracts. RT-001E continues to return only `deferred` or `unknown` until a reviewed owner interface skeleton exists.

**Severity:** High until RT-001H and downstream owner interfaces are merged.

### R2 — raw state access risk

**Risk:** A future legality evaluator could bypass owner interfaces and read raw world state directly from `state_store`, violating ownership boundaries and visibility rules.

**Mitigation:** RT-001G forbids raw state reads and requires all state consumption to be mediated by the state projection owner (SO-13). Import boundary tests must enforce that legality modules do not import `state_store` for direct reads.

**Severity:** High.

### R3 — hidden-information leakage risk

**Risk:** Legality could reveal hidden information through player-visible blocker messages, status codes, or inference from missing data.

**Mitigation:** RT-001G requires hidden-information questions to route to the visibility owner (SO-12), mandates generic safe messages, and forbids inference from absence.

**Severity:** High.

### R4 — missing-data-as-truth risk

**Risk:** Legality could interpret the absence of a state record or projection as proof that a condition does not exist, leading to incorrect `legal` or `illegal` decisions.

**Mitigation:** RT-001G requires missing data to result in `deferred`, `unknown`, or `escalated` statuses, not fabricated blockers or approvals.

**Severity:** High.

### R5 — owner-route ambiguity risk

**Risk:** Dependency manifests could name owner routes ambiguously, causing legality to route questions to the wrong owner or to fabricate decisions.

**Mitigation:** RT-001G defines precise owner interface families and route names. Future skeletons must map each dependency kind to exactly one owner route.

**Severity:** Medium.

### R6 — donor-action-economy leakage risk

**Risk:** Donor-specific action economies could leak into runtime baseline legality rules, creating corpus-scale bias.

**Mitigation:** RT-001G reaffirms donor neutrality and requires source-local/donor-specific commands to be quarantined or escalated under RT-012.

**Severity:** Medium.

### R7 — state mutation by legality service risk

**Risk:** A future legality evaluator could mutate state, advance clocks, consume resources, or apply conditions while evaluating legality.

**Mitigation:** RT-001G mandates read-only state contracts and false-only mutation authority flags. State owner interfaces must not expose mutation surfaces to legality.

**Severity:** High.

### R8 — event commitment shortcut risk

**Risk:** Legality could attempt to commit events or mark transactions ready for commitment as a shortcut around transaction lifecycle and event commitment owners.

**Mitigation:** RT-001G forbids legality from appending events, applying deltas, or setting commitment flags. These authorities belong to event commitment and transaction lifecycle owners.

**Severity:** High.

### R9 — resource math shortcut risk

**Risk:** Legality could execute affordability checks, reservations, or settlements instead of declaring resource math dependencies.

**Mitigation:** RT-001G requires resource questions to route to the resource math owner (DO-02). Legality may only confirm resource category existence.

**Severity:** Medium.

### R10 — RNG/table/oracle shortcut risk

**Risk:** Legality could roll dice, draw from tables, or invoke oracles to decide legality.

**Mitigation:** RT-001G requires randomness dependencies to route to the RNG/table/oracle owner (DO-03). Legality must not execute randomness.

**Severity:** Medium.

### R11 — projection/visibility mismatch risk

**Risk:** Legality could consume a projection intended for a different visibility tier, leaking backend-hidden or GM-only data into player-visible output.

**Mitigation:** RT-001G requires every projection to carry a visibility descriptor and requires legality to use only appropriately redacted projections for player-facing decisions.

**Severity:** High.

### R12 — dependency owner circularity risk

**Risk:** Owner interfaces could form circular dependencies (e.g., state projection depends on legality, which depends on state projection), causing deadlock or undefined behavior.

**Mitigation:** RT-001G defines a layered ownership model. State owners sit below legality; dependency owners sit beside or below legality. Legality must not be a dependency of any owner it consumes.

**Severity:** Medium.

### R13 — persistence/replay drift risk

**Risk:** Legality could produce trace references or snapshot expectations that are not reproducible during replay, causing audit drift.

**Mitigation:** RT-001G requires every state read and projection request to be traceable and replay-auditable. Legality must not write persistence records itself.

**Severity:** Medium.

### R14 — model/live-play treating unavailable owner data as final adjudication risk

**Risk:** A future model integration or live-play adapter could treat `deferred` or `unknown` legality results, or partial owner responses, as final adjudication.

**Mitigation:** RT-001G mandates that `deferred` and `unknown` remain temporary statuses and that owner-mediated facts are clearly marked as partial or pending. The non-authority note must persist in all skeleton results.

**Severity:** High.

### R15 — incremental drift from review into implementation risk

**Risk:** RT-001G could be treated as permission to begin implementing legality evaluation logic alongside the owner interface skeleton, blurring the review boundary.

**Mitigation:** RT-001G is explicitly review-only. The next recommended step is RT-001H — State Owner Interface Contract Skeleton, not legality evaluation implementation. No legality evaluation code may be added until all prerequisite owner interfaces are defined and reviewed.

**Severity:** Medium.

---

## 17. Required sequencing after RT-001G

The following sequencing must be observed after RT-001G:

1. **RT-001H — State Owner Interface Contract Skeleton.** Define the skeleton interfaces for the state owner families in Section 4 and the dependency owner families in Section 5. No implementation.
2. **RT-001I — State Owner Interface Hardening Review (if needed).** Harden the RT-001H skeleton before it is used by legality.
3. **Owner interface availability gate.** Confirm that all owner interfaces required for a given command family are available before enabling real legality evaluation for that family.
4. **RT-001J+ — Action Legality Evaluation Implementation (future, separately authorized).** Only after owner interfaces exist may a real legality evaluator be implemented, scoped to a single command family or owner subset.
5. **No legality evaluation before owner interfaces.** Real action legality evaluation must not begin until the prerequisite owner interfaces are merged and hardening reviews are complete.

---

## 18. Explicitly forbidden shortcuts

The following shortcuts are explicitly forbidden:

1. **Reading raw state directly from `state_store`.** All state reads must be owner-mediated projections.
2. **Inferring hidden truth from missing data.** Missing data must result in `deferred`, `unknown`, or `escalated`.
3. **Fabricating legality decisions for unresolved dependencies.** Unresolved dependencies must be routed to owner services.
4. **Mutating state during legality evaluation.** Legality is read-only.
5. **Appending events or committing state.** These belong to event commitment and transaction lifecycle owners.
6. **Executing resource math, RNG, table, or oracle operations.** These belong to their respective owners.
7. **Embedding donor-specific action economies as baseline rules.** Donor-specific content must be quarantined or escalated.
8. **Treating `deferred` or `unknown` as final adjudication.** These are temporary statuses requiring re-evaluation.
9. **Implementing legality evaluation inside RT-001G or RT-001H.** These are review and skeleton PRs only.
10. **Bypassing visibility descriptors.** Projections must be redacted to the appropriate tier before use.

---

## 19. Acceptance criteria

- [x] RT-001G review document exists and names RT-001A through RT-001F.
- [x] RT-001G states it is review-only and does not implement a state owner interface.
- [x] RT-001G states it does not implement action legality evaluation.
- [x] RT-001G states that real legality evaluation remains blocked until owner interfaces exist.
- [x] RT-001G lists all required state owner interface families.
- [x] RT-001G lists all required dependency owner interface families.
- [x] RT-001G includes hidden-information containment requirements.
- [x] RT-001G includes projection and visibility contract requirements.
- [x] RT-001G includes transaction preview and event commitment prerequisites.
- [x] RT-001G includes resource/consequence math prerequisites.
- [x] RT-001G includes RNG/table/oracle prerequisites.
- [x] RT-001G includes persistence/replay prerequisites.
- [x] RT-001G includes corpus-scale donor pressure audit.
- [x] RT-001G includes all 15 required risk ledger categories.
- [x] RT-001G forbids raw state reads by the future legality service.
- [x] RT-001G forbids mutation and event commitment shortcuts.
- [x] RT-001G recommends the next step as RT-001H — State Owner Interface Contract Skeleton, not legality evaluation implementation.
- [x] RT-001G branch does not modify runtime implementation modules.
- [x] RT-001B through RT-001F tests still pass.
- [x] Registry contains RT-001G review record.
- [x] Decision log contains RT-001G entry.

---

## 20. Next recommended step

**RT-001H — State Owner Interface Contract Skeleton.**

This skeleton must define the reference-only interfaces for the state owner families in Section 4 and the dependency owner families in Section 5. It must not implement legality evaluation, state mutation, command execution, event commitment, persistence, RNG/table/oracle, resource math, model/live-play, UI, conversion, sourcebook inclusion, or canon promotion.

---

## 21. Classification block

```yaml
runtime_domain_rt_001g:
  review_id: RUNTIME-DOMAIN-RT-001G-STATE-OWNER-INTERFACE-PREREQUISITE-REVIEW-001
  artifact_type: state_owner_interface_prerequisite_review
  implementation_status: non_executable_review
  derives_from:
    - RUNTIME-DOMAIN-RT-001A-ACTION-LEGALITY-SERVICE-PLAN-001
    - RUNTIME-DOMAIN-RT-001B-ACTION-LEGALITY-SKELETON-001
    - RUNTIME-DOMAIN-RT-001C-ACTION-LEGALITY-GATE-INTEGRATION-SKELETON-001
    - RUNTIME-DOMAIN-RT-001D-ACTION-LEGALITY-INTEGRATION-HARDENING-REVIEW-001
    - RUNTIME-DOMAIN-RT-001E-ACTION-LEGALITY-SERVICE-INTERFACE-CONTRACT-SKELETON-001
    - RUNTIME-DOMAIN-RT-001F-ACTION-LEGALITY-SERVICE-INTERFACE-CONTRACT-HARDENING-REVIEW-001
  confirms:
    - rt_001g_is_review_only: true
    - rt_001g_does_not_implement_state_owner_interface: true
    - rt_001g_does_not_implement_legality_evaluation: true
    - real_legality_evaluation_blocked_until_owner_interfaces_exist: true
    - rt_001e_must_remain_deferred_or_unknown_until_superseded: true
    - state_reads_require_explicit_owner_contracts: true
    - state_reads_require_typed_references: true
    - state_reads_require_visibility_rules: true
    - state_reads_require_hidden_information_containment: true
    - state_reads_must_not_authorize_mutation: true
    - future_legality_evaluator_must_not_read_raw_world_state_directly: true
    - future_legality_evaluator_must_not_infer_hidden_truth_from_missing_data: true
    - future_legality_evaluator_must_route_unresolved_dependencies_to_owner_services: true
    - donor_specific_action_economies_must_not_become_runtime_baseline_law: true
  defines:
    - 16_state_owner_interface_families
    - 10_dependency_owner_interface_families
    - minimum_state_read_contract_requirements
    - minimum_projection_and_visibility_contract_requirements
    - hidden_information_containment_requirements
    - actor_target_scene_object_hazard_inventory_faction_resource_boundaries
    - transaction_preview_and_event_commitment_prerequisites
    - resource_consequence_math_prerequisites
    - rng_table_oracle_prerequisites
    - persistence_replay_prerequisites
    - import_and_authority_boundary_requirements
    - corpus_scale_donor_pressure_audit
    - 15_risk_ledger_entries
    - required_sequencing_after_rt_001g
    - explicitly_forbidden_shortcuts
  authorizes_implementation: false
  authorizes_state_owner_interface: false
  authorizes_state_reads: false
  authorizes_state_mutation: false
  authorizes_legality_evaluation: false
  authorizes_command_execution: false
  authorizes_event_commitment: false
  authorizes_persistence_replay: false
  authorizes_rng_table_oracle: false
  authorizes_resource_math: false
  authorizes_model_integration: false
  authorizes_narration_generation: false
  authorizes_live_play: false
  authorizes_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RT-001H — State Owner Interface Contract Skeleton
```

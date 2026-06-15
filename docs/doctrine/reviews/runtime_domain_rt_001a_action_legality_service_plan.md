# RUNTIME-DOMAIN-RT-001A — Action Legality Service Plan and Execution Boundary Review

**Date:** 2026-06-15
**Artifact ID:** RUNTIME-DOMAIN-RT-001A-ACTION-LEGALITY-SERVICE-PLAN-001
**Follows:** RUNTIME-DOMAIN-PR-9E (transaction preview packet bridge skeleton, merged as PR #310)
**Status:** planning/review only — no runtime behavior, no legality engine implementation

---

## 1. Purpose and status

RT-001A is a planning and execution-boundary review document. It defines the backend-owned action legality boundary that must exist before any of the following can be implemented: resource math execution, RNG/table/oracle execution, persistence, replay, live-play integration, model behavior, broad rules-engine logic, conversion, sourcebook inclusion, or canon promotion.

RT-001A follows the completion of the PR-9A through PR-9E post-PR-8 command-path reference seam:

| PR | Title | Merged as |
|---|---|---|
| PR-9 | Post-PR-8 Runtime Generalization Planning | PR #304 |
| PR-9A | Scene Command Execution Skeleton | PR #305 |
| PR-9B | Scene Command Execution Hardening Review | PR #306 |
| PR-9C | Command-Kind Routing Skeleton | PR #307 |
| PR-9D | Validation Integration Bridge Skeleton | PR #308 |
| PR-9E | Transaction Preview Packet Bridge Skeleton / Authority Flag Hardening | PR #309, #310 |

**Artifact type:** action_legality_service_plan_and_execution_boundary_review
**Implementation status:** non_executable_plan
**Review ID:** RUNTIME-DOMAIN-RT-001A-ACTION-LEGALITY-SERVICE-PLAN-001

This document authorizes no execution behavior. It creates no domain-service code, no legality engine, no validators, no dataclasses, and no constants beyond documentation and narrow registry/test updates required by repo pattern. The next allowed implementation step is RT-001B.

---

## 2. Authority posture

RT-001A operates under the established Astra backend-first invariant:

> The LLM is not the game engine. The backend runtime kernel owns truth.
> LLMs propose; the backend validates and commits.
> Prose is downstream of state, not its source.

The action legality boundary is the first gate that a command envelope must pass after structural validation and routing. Legality determines whether the command may proceed toward transaction planning, not whether it will succeed. Legality is a precondition gate, not an execution engine.

**This document owns the definition of legality.** It does not own legality implementation, which belongs to RT-001B and subsequent PRs.

---

## 3. Definition of action legality

Action legality in Astra runtime is the backend-owned determination of whether a command may proceed from the command-path reference seam (PR-9A through PR-9E surfaces) into downstream transaction planning, resource math, and eventual execution.

Legality answers: **"Is this command structurally valid, contextually permitted, and safe to plan?"**

Legality does not answer:

- "Will this command succeed?" (that requires resource math, combat resolution, ability resolution, etc.)
- "What will happen?" (that requires consequence application, state mutation, event commitment)
- "What should the player see?" (that requires context packet compilation, narration generation)
- "Is this affordable?" (that requires resource math execution — RT-002)
- "What dice should be rolled?" (that requires RNG/table/oracle execution — RT-009)

Legality is a **gate**, not a **resolver**. It blocks commands that cannot legally proceed. It passes commands that may legally proceed. It does not determine outcomes.

---

## 4. What legality owns

The action legality service, when implemented, owns:

1. **Command envelope structural prevalidation** — confirming envelope shape, required fields, and type conformance via kernel `command_envelope` and `validation_pipeline` interfaces.
2. **Actor existence and reference validation** — confirming the source actor record identity resolves to a valid, non-deleted, non-suspended record via kernel `record_identity`.
3. **Actor authority/capability gate** — confirming the actor has the authority category to attempt the declared command kind (e.g., a non-combatant cannot initiate combat commands, a dead actor cannot take actions).
4. **Target existence and reference validation** — confirming declared targets resolve to valid record identities.
5. **Target reachability/scope gate** — confirming declared targets are within the scene, location, or interaction scope of the actor, without computing exact distances or movement costs.
6. **Scene/location boundary gate** — confirming the command is contextually valid for the current scene or location type (e.g., a swim command is incoherent in a desert scene with no water).
7. **Command-kind routing compatibility gate** — confirming the command kind (from PR-9C routing) is a recognized, non-quarantined kind that the system can plan for.
8. **Validation integration bridge compatibility gate** — confirming the command can pass through the validation integration bridge (PR-9D) without structural failure.
9. **Resource prerequisite existence gate** — confirming that resources the command would require are declared as existing resource categories, without calculating whether the actor can afford them.
10. **Timing/cooldown/phase gate** — confirming the command is not blocked by timing constraints (e.g., action economy phase, cooldown period, per-turn limits), without running clocks or computing durations.
11. **Hidden-information boundary gate** — confirming the command does not require the actor to know information the actor does not have, without revealing what that hidden information is.
12. **Ambiguity/clarification gate** — identifying commands that are too ambiguous to plan and routing them to clarification rather than silent misinterpretation.
13. **Command-family support gate** — identifying commands from unsupported or unrecognized command families and routing them to quarantine rather than fake classification.
14. **Source-local/donor-specific gate** — identifying commands that rely on donor-specific action economies, mechanics, or rules not yet canonized into Astra doctrine, and routing them to quarantine or escalation.
15. **Doctrine gap identification** — identifying commands that expose gaps in Astra doctrine (no rule exists for this action category) and routing them to escalation.
16. **Policy/safety/meta-action gate** — identifying commands that violate safety policy, attempt meta-game manipulation, or request actions that bypass the backend-first invariant.
17. **Legality result production** — producing an immutable, frozen legality result record with a legality status, blocker list, player-visible summary, and backend-only detail.
18. **Legality trace production** — producing runtime trace entries for every legality decision via kernel `runtime_trace`.

---

## 5. What legality must not own

The action legality service must never own or perform:

1. **Command execution** — legality is a precondition gate, not an executor.
2. **State mutation** — legality reads state projections; it never writes state.
3. **Event append or commitment** — legality does not produce events.
4. **Resource math or affordability calculation** — legality confirms resource categories exist; RT-002 owns cost formulas, affordability, reservation, and settlement.
5. **RNG/table/oracle execution** — legality does not roll dice, draw from tables, or invoke oracles. RT-009 owns randomness.
6. **Combat resolution, damage calculation, or hit/miss determination** — RT-003 owns combat math.
7. **Ability/effect/skill resolution** — RT-004 owns ability binding and effect evaluation.
8. **Inventory mutation, item use resolution, or equipment behavior** — RT-010 owns inventory.
9. **Mission/clue/reward resolution** — RT-006 owns mission routing.
10. **Social/faction/relationship resolution** — RT-007 owns social state.
11. **Generated-content provenance or recurrence** — RT-008 owns generated-content durability.
12. **Context packet compilation** — RT-005 / future context-packet service owns packet assembly.
13. **Prompt rendering, prompt execution, or model calls** — the model evaluation harness is a separate boundary. Legality does not invoke models.
14. **Narration generation** — narration is downstream of state and execution, not of legality.
15. **Persistence reads/writes** — legality operates on in-memory state projections. It does not call the persistence boundary.
16. **Replay** — legality does not participate in replay.
17. **Transaction lifecycle management** — transaction planning, commitment, rollback, and settlement belong to the transaction lifecycle service.
18. **Consequence application** — consequence math and application are downstream of legality.
19. **Live-play adapter, session management, or UI/client behavior**.
20. **Conversion, sourcebook inclusion, or canon promotion** — legality does not modify the Astra corpus.
21. **Donor-specific rule execution** — legality identifies donor-specific commands but does not execute donor rules. Donor rules are either mapped to Astra equivalents or quarantined for RT-012 review.

---

## 6. Upstream surfaces that feed legality

### Scene command execution skeleton (PR-9A)

The PR-9A `SceneCommandExecutionAssemblyResult` provides the typed assembly that legality evaluates. Legality receives the assembled command envelope, actor reference, target references, resource planning references, and hidden-info contract references from this surface.

### Command-kind routing skeleton (PR-9C)

The PR-9C `CommandKindRoutingResult` provides the deterministic command-family classification. Legality uses the routed command kind to determine which blocker classes apply and which downstream services would be required.

### Validation integration bridge skeleton (PR-9D)

The PR-9D `ValidationIntegrationBridgeResult` provides structural validation results. Legality consumes validation pass/fail status and validation issue records to determine whether the command is structurally valid for further processing.

### Transaction preview packet bridge skeleton (PR-9E)

The PR-9E `TransactionPreviewPacketBridgeResult` provides packet descriptors. Legality does not produce packets, but its result is consumed by the packet bridge to determine whether preview assembly should proceed.

### Resource/consequence math reference surfaces (PR-5A)

The `resource_consequence_math` skeleton provides resource category declarations and cost structure references. Legality uses these to confirm resource categories exist without calculating affordability.

### Command references / actor references / target references

Kernel `command_envelope`, `record_identity`, and `schema_registry` provide the typed reference surfaces for command, actor, and target identity resolution.

### Future context packet compiler surfaces

When the context packet compiler matures, legality results will be consumed by the compiler to determine what command-lifecycle information appears in context packets. Legality does not call the compiler.

### Future runtime state/event surfaces

When state projection and event commitment services mature, legality will consume read-only state projections for gate decisions (e.g., "is the actor alive?"). Legality will never consume or produce events.

---

## 7. Downstream surfaces that receive legality output

### Command lifecycle prevalidation

Legality results are the primary output of the command lifecycle prevalidation phase. A `legal` result permits the command to proceed to transaction planning. All other results block or defer the command.

### Validation integration

Legality produces `ValidationIssue` records for every non-legal decision, feeding the validation integration pipeline for aggregation and audit.

### Transaction preview packet assembly

Legality results are required inputs to the transaction preview packet bridge (PR-9E). A blocked command does not receive a transaction preview.

### Resource/consequence math planning handoff

For `legal` commands, legality passes the command envelope and dependency declarations to the resource/consequence math planning service (RT-002). Legality does not pass affordability determinations — it passes existence checks and dependency declarations only.

### RNG/table/oracle planning handoff

For `legal` commands that require randomness, legality declares a dependency on RT-009. It does not invoke RNG.

### State-delta validation planning handoff

For `legal` commands, legality passes the command to state-delta validation planning. Legality does not produce state deltas.

### Event commitment planning handoff

For `legal` commands that would produce events, legality declares the event commitment dependency. It does not produce or commit events.

### Context packet planning handoff

Legality results (including player-visible summaries of blocked commands) are consumed by the context packet planning surface to determine what command-result information is available for narration.

### Persistence/replay planning handoff

Legality results are included in the runtime trace for future persistence and replay audit. Legality does not call the persistence boundary.

---

## 8. Legality status vocabulary

Every action legality evaluation must produce exactly one of the following status values. These are not interchangeable. Each has a distinct meaning, a distinct downstream behavior, and distinct player-visible and backend-only implications.

### `legal`

- **Meaning:** The command has passed all legality gates and may proceed to transaction planning and downstream domain-service resolution.
- **May proceed to preview:** Yes.
- **May proceed to execution planning:** Yes.
- **Player-visible output:** "Action accepted." or equivalent. No blocker detail.
- **Backend-only detail:** Full trace of all passed gates. No blockers.
- **Downstream behavior:** Command enters transaction planning. Dependency declarations are forwarded to downstream services.

### `illegal`

- **Meaning:** The command violates a hard constraint that cannot be resolved by waiting, clarifying, or confirming. The command is categorically forbidden.
- **May proceed to preview:** No.
- **May proceed to execution planning:** No.
- **Player-visible output:** A safe, generic denial category. Must not reveal hidden information.
- **Backend-only detail:** Full blocker chain with specific violation reasons.
- **Downstream behavior:** Command is rejected. Validation issues are produced. Runtime trace records the rejection.
- **Examples:** Attempting an action that violates a physical law of the game world; attempting to command an entity the actor does not control; attempting a meta-game cheat command.

### `blocked`

- **Meaning:** The command is not inherently illegal but is currently blocked by one or more resolvable conditions. The conditions may resolve over time, through other actions, or through game-state changes.
- **May proceed to preview:** No.
- **May proceed to execution planning:** No.
- **Player-visible output:** A safe blocker category. Must not reveal hidden information. Safe categories: "not enough information," "invalid target," "requires assessment," "cannot currently attempt."
- **Backend-only detail:** Specific blocker class, affected reference, and resolution path.
- **Downstream behavior:** Command is held. Blocker record is produced. The command may be re-evaluated when conditions change.
- **Examples:** Target out of range; actor lacks required capability; timing constraint not met; resource category not present.

### `deferred`

- **Meaning:** The command cannot be evaluated yet because a required upstream surface, domain service, or state projection is not yet available in the runtime. The command is not illegal and not blocked by game state — it is blocked by runtime immaturity or dependency unavailability.
- **May proceed to preview:** No.
- **May proceed to execution planning:** No.
- **Player-visible output:** "This action cannot be processed at this time." No implementation detail.
- **Backend-only detail:** Missing dependency identifier, missing service owner (RT track), expected availability gate.
- **Downstream behavior:** Command is held. Deferral record is produced. The command may be re-evaluated when the missing dependency becomes available.
- **Examples:** A combat command is received but RT-003 (combat resolution service) is not yet implemented; a crafting command is received but RT-010 (inventory service) is not yet implemented.

### `quarantined`

- **Meaning:** The command has been isolated for review because it matches a quarantine trigger. Quarantined commands are not rejected — they are held pending human review, doctrine review, or schema review.
- **May proceed to preview:** No.
- **May proceed to execution planning:** No.
- **Player-visible output:** "This action requires review." No quarantine detail.
- **Backend-only detail:** Quarantine trigger, quarantine category, source-local reference if applicable, doctrine gap reference if applicable.
- **Downstream behavior:** Command enters quarantine. Quarantine record is produced. The command is not processed until the quarantine is resolved by authorized review.
- **Examples:** Unsupported command type from a donor system; command referencing source-local rules not yet canonized; command exposing a doctrine gap; command that would require schema extension.

### `unknown`

- **Meaning:** The legality service cannot determine the legality of this command. The command is structurally valid but the service lacks sufficient context, rules, or schema to make a determination.
- **May proceed to preview:** No.
- **May proceed to execution planning:** No.
- **Player-visible output:** "This action cannot be evaluated." No detail about why evaluation failed.
- **Backend-only detail:** Evaluation failure reason, missing schema reference, missing rule reference.
- **Downstream behavior:** Command is held. Unknown-legality record is produced. The command may be re-evaluated when additional schema, rules, or context become available. Persistent `unknown` results should be escalated.
- **Examples:** A command references a game mechanic that has no Astra schema; a command references a rule interaction that has not been defined; a command references an entity type the system has never encountered.

### `escalated`

- **Meaning:** The command has been escalated to a higher authority (doctrine council, runtime working group, or human reviewer) because it raises a question that the legality service cannot resolve within its authority.
- **May proceed to preview:** No.
- **May proceed to execution planning:** No.
- **Player-visible output:** "This action has been referred for review." No escalation detail.
- **Backend-only detail:** Escalation reason, escalation target, doctrine gap reference, affected RT owner(s), priority.
- **Downstream behavior:** Command enters escalation. Escalation record is produced. The command is not processed until the escalation is resolved by the target authority.
- **Examples:** A command exposes a contradiction between two doctrine entries; a command requires a rule that would set precedent across multiple RT owners; a command reveals a corpus-scale ambiguity that affects many donor sources.

---

## 9. Blocker class taxonomy

When a command receives a status other than `legal`, the legality result must include one or more blocker records identifying the specific blocker class. Each blocker record contains a blocker class identifier, a player-visible summary, and a backend-only detail record.

### Actor existence/reference blocker

- **Trigger:** The source actor record identity does not resolve to a valid, non-deleted record.
- **Player-visible:** "Invalid actor."
- **Backend-only:** Missing or deleted record identity, reference resolution failure detail.
- **Typical legality status:** `illegal` or `blocked`.

### Actor authority/capability blocker

- **Trigger:** The actor exists but lacks the authority or capability category required for the declared command kind (e.g., unconscious actor attempting movement, non-spellcaster attempting spell, dead actor attempting any action).
- **Player-visible:** "Cannot currently attempt this action."
- **Backend-only:** Actor capability state, required capability, mismatch detail.
- **Typical legality status:** `blocked`.

### Access/permission blocker

- **Trigger:** The actor exists and has the capability but lacks permission for the specific action (e.g., locked container, restricted zone, faction-gated action).
- **Player-visible:** "Access denied." or "Requires permission."
- **Backend-only:** Permission record, access gate reference, faction or authority requirement.
- **Typical legality status:** `blocked`.

### Target existence/reference blocker

- **Trigger:** The declared target record identity does not resolve to a valid record.
- **Player-visible:** "Invalid target."
- **Backend-only:** Missing or deleted target record identity, reference resolution failure detail.
- **Typical legality status:** `blocked`.

### Target reachability/scope blocker

- **Trigger:** The declared target exists but is not within the actor's interaction scope (e.g., in a different scene, behind a barrier, out of declared range category).
- **Player-visible:** "Target is not reachable." or "Target is out of range."
- **Backend-only:** Scope boundary detail, scene/location mismatch, range category check.
- **Typical legality status:** `blocked`.

### Scene/location boundary blocker

- **Trigger:** The command is contextually inappropriate for the current scene or location (e.g., underwater action in a desert, flight action in an enclosed cave).
- **Player-visible:** "This action is not available here."
- **Backend-only:** Scene type, location constraints, command-kind/scene mismatch.
- **Typical legality status:** `blocked`.

### Command-kind routing blocker

- **Trigger:** The PR-9C command-kind routing classified the command into an unrecognized, quarantined, or unsupported family.
- **Player-visible:** "This type of action is not supported."
- **Backend-only:** Routing classification, unknown family identifier, quarantine reason.
- **Typical legality status:** `quarantined` or `unknown`.

### Validation integration blocker

- **Trigger:** The PR-9D validation integration bridge produced validation failures that prevent the command from proceeding.
- **Player-visible:** "Action could not be validated."
- **Backend-only:** Validation issue records, invariant family, failure route.
- **Typical legality status:** `blocked` or `illegal`.

### Resource prerequisite blocker

- **Trigger:** The command requires resource categories that are not declared as existing (e.g., the command references a mana cost but the actor has no mana resource category). This is an existence check, not an affordability check.
- **Player-visible:** "Required resources are not available."
- **Backend-only:** Missing resource category, expected resource type, actor resource inventory.
- **Typical legality status:** `blocked`.
- **Critical boundary:** Legality does not calculate whether the actor can afford the cost. That is RT-002's responsibility.

### Timing/cooldown/phase blocker

- **Trigger:** The command is blocked by a timing constraint (e.g., action already used this phase, cooldown not elapsed, per-turn limit reached). Legality checks phase/cooldown flags without running clocks or computing durations.
- **Player-visible:** "This action cannot be taken right now."
- **Backend-only:** Phase state, cooldown reference, timing constraint detail.
- **Typical legality status:** `blocked`.
- **Critical boundary:** Legality does not run timers, advance clocks, or compute duration math. It reads timing state flags from state projections.

### Hidden-information blocker

- **Trigger:** The command requires the actor to know information that is classified as hidden from that actor (e.g., targeting an invisible entity the actor cannot perceive, referencing a secret passage the actor has not discovered).
- **Player-visible:** "Not enough information to attempt this action." Must NOT reveal whether hidden information exists, what it is, or what kind it is.
- **Backend-only:** Hidden-information classification, visibility tier, perception check reference, affected entity reference.
- **Typical legality status:** `blocked`.
- **Critical boundary:** See section 11 (Hidden-information containment).

### Ambiguity/clarification blocker

- **Trigger:** The command is too ambiguous to evaluate. Multiple valid interpretations exist and the system cannot safely choose one.
- **Player-visible:** "Please clarify your intended action."
- **Backend-only:** Ambiguity type, candidate interpretations, disambiguation requirement.
- **Typical legality status:** `blocked` (with clarification request).

### Unsupported command-family blocker

- **Trigger:** The command references a command family that the runtime does not yet support (e.g., a new action type introduced by a donor system that has no Astra-native equivalent and no implemented handler).
- **Player-visible:** "This type of action is not currently supported."
- **Backend-only:** Unsupported family identifier, donor source reference, schema gap reference.
- **Typical legality status:** `quarantined` or `deferred`.

### Source-local/donor-specific blocker

- **Trigger:** The command relies on donor-specific mechanics, action economies, or rules that have not been canonized into Astra doctrine (e.g., "use swift action" in a non-Pathfinder context, "spend fate point" outside Fate system).
- **Player-visible:** "This action uses rules that are not currently active."
- **Backend-only:** Donor source reference, source-local mechanic identifier, RT-012 promotion boundary reference.
- **Typical legality status:** `quarantined`.
- **Critical boundary:** Source-local rules do not become Astra law by repetition, use, or generated-content reference. Quarantine forces explicit RT-012 review.

### Doctrine gap blocker

- **Trigger:** The command exposes a gap in Astra doctrine — a situation where no rule, schema, or procedure exists to handle the action category.
- **Player-visible:** "This action requires further development."
- **Backend-only:** Doctrine gap description, affected doctrine area, affected RT owner(s), gap severity.
- **Typical legality status:** `escalated`.

### Schema gap blocker

- **Trigger:** The command references entity types, record structures, or data shapes that have no corresponding schema in the Astra schema family (C00–C14 and future extensions).
- **Player-visible:** "This action references unsupported game elements."
- **Backend-only:** Missing schema reference, expected schema family, entity type.
- **Typical legality status:** `quarantined` or `escalated`.

### Runtime owner handoff blocker

- **Trigger:** The command requires a downstream RT owner service that is not yet implemented or not yet available. This is distinct from `deferred` status because the blocker is at the service level, not the command level.
- **Player-visible:** "This action cannot be processed at this time."
- **Backend-only:** Missing RT owner, expected service, implementation status.
- **Typical legality status:** `deferred`.

### Policy/safety/meta-action blocker

- **Trigger:** The command violates safety policy, attempts meta-game manipulation (e.g., "undo last action," "god mode," "reveal all secrets"), or requests actions that bypass the backend-first invariant.
- **Player-visible:** "This action is not permitted."
- **Backend-only:** Policy violation category, meta-action type, safety classification.
- **Typical legality status:** `illegal`.

### Anti-authority blocker

- **Trigger:** The command attempts to grant itself authority that it does not have — e.g., a command that claims LLM authority, claims model output as game truth, claims narration as state, or attempts to bypass validation.
- **Player-visible:** "This action is not permitted."
- **Backend-only:** Anti-authority violation type, claimed authority, violated invariant.
- **Typical legality status:** `illegal`.

---

## 10. Player-visible versus backend-only blocker handling

### Separation principle

Every blocker record must contain two distinct data channels:

1. **Player-visible output:** A safe, generic denial message that does not reveal hidden information, backend internals, implementation state, or doctrine details.
2. **Backend-only detail:** A full diagnostic record containing the specific blocker class, affected references, resolution paths, and debugging information.

### Player-visible safe denial categories

The following are the only categories of player-visible denial messages that legality may produce:

| Safe category | Usage |
|---|---|
| "Invalid actor." | Actor reference resolution failure. |
| "Cannot currently attempt this action." | Actor capability or authority mismatch. |
| "Access denied." / "Requires permission." | Permission/access gate. |
| "Invalid target." | Target reference resolution failure. |
| "Target is not reachable." / "Target is out of range." | Target scope/reachability. |
| "This action is not available here." | Scene/location boundary. |
| "This type of action is not supported." | Unsupported command family. |
| "Action could not be validated." | Validation failure. |
| "Required resources are not available." | Resource prerequisite missing. |
| "This action cannot be taken right now." | Timing/cooldown/phase. |
| "Not enough information to attempt this action." | Hidden-information blocker (safe). |
| "Please clarify your intended action." | Ambiguity. |
| "This action uses rules that are not currently active." | Source-local/donor. |
| "This action requires further development." | Doctrine gap. |
| "This action references unsupported game elements." | Schema gap. |
| "This action cannot be processed at this time." | Deferred / runtime owner unavailable. |
| "This action is not permitted." | Policy/safety/meta/anti-authority. |
| "This action has been referred for review." | Escalated. |
| "Action accepted." | Legal (no blockers). |

### Backend-only detail record

The backend-only detail record must include:

- Blocker class identifier (from section 9 taxonomy).
- Affected record identities (actor, target, scene, resource, etc.).
- Specific constraint violated.
- Resolution path (what would need to change for the blocker to clear).
- Related RT owner(s).
- Trace reference.
- Hidden-information classification (if the blocker involves hidden info).
- Severity / priority.

### Forbidden in player-visible output

Player-visible output must never contain:

- Backend implementation details (module names, function names, error codes).
- Hidden-information content (entity names, locations, states that the actor should not know).
- Doctrine or schema references.
- RT owner identifiers.
- Internal blocker class identifiers.
- Resolution paths that reveal backend logic.
- Any information that would allow a player to infer hidden game state from a denial message.

---

## 11. Hidden-information containment

### The core problem

When a player attempts an action that is blocked because of hidden information (e.g., attacking an invisible enemy they cannot perceive, searching for a secret passage they don't know exists, interacting with a concealed trap), the denial message must not reveal the existence or nature of the hidden information.

### Containment rules

1. **A hidden-information denial must not confirm that a hidden entity exists.** "You can't attack the invisible NPC" reveals that an invisible NPC exists. The safe alternative is: "Not enough information to attempt this action."

2. **A hidden-information denial must not confirm that a secret path, passage, door, or location exists.** "The secret passage is blocked" reveals the passage exists. The safe alternative is: "Not enough information to attempt this action."

3. **A hidden-information denial must not confirm that a trap, hazard, or concealed danger exists.** "The trap prevents you from proceeding" reveals the trap. The safe alternative is: "Not enough information to attempt this action."

4. **A hidden-information denial must not confirm faction allegiance, NPC disposition, or hidden social state.** "The NPC is secretly working against you" reveals hidden social state. The safe alternative is: "Not enough information to attempt this action."

5. **A hidden-information denial must not confirm future events, plot developments, or scheduled triggers.** "This action would interfere with a scheduled event" reveals the event. The safe alternative is: "This action cannot be taken right now."

6. **A hidden-information denial must not distinguish between "the target doesn't exist" and "the target exists but is hidden."** Both cases produce the same player-visible message. The backend-only record distinguishes them.

7. **A hidden-information denial must not provide differential information through error specificity.** If some targets produce "invalid target" and hidden targets produce "not enough information," the difference reveals which targets are hidden. The player-visible response for both should be indistinguishable when hidden information is at stake.

### Backend-only hidden-information record

The backend-only detail record for hidden-information blockers must include:

- The actual hidden entity or fact reference.
- The visibility tier classification (from `state_store` visibility tiers: `backend_hidden`, `gm_visible`, `actor_visible`, `player_visible`, `public`, `redacted`).
- The perception/discovery requirement that would make the information visible.
- The kernel `hidden_information` interface reference used for the check.

### Relationship to RT-005

RT-005 (context packet / hidden information) owns the broader hidden-information model. Legality consumes RT-005's visibility classifications but does not define or modify them. Legality's responsibility is limited to: when a blocker involves hidden information, produce a safe player-visible message and a detailed backend-only record.

---

## 12. Source-local and donor-specific action handling

### The problem

The Astra corpus will eventually absorb 200–400+ donor sources, each with unique action economies, mechanics, and rules. Commands originating from donor-specific contexts may reference:

- Donor-specific action economy terms (swift action, bonus action, reaction, fate point, momentum, edge, strain, stress, hero point, fortune die).
- Donor-specific mechanic names (opportunity attack, attack of opportunity, sneak attack, smite, channel divinity, ki point, rage, wildshape).
- Donor-specific rule interactions that have no Astra-native equivalent.

### Handling rules

1. **Donor-specific action economy terms are not Astra baseline law.** They must be either:
   - Mapped to an Astra-native equivalent (if one exists and the mapping is canonized).
   - Quarantined for RT-012 review (if no Astra equivalent exists).
   - Never silently adopted as Astra law.

2. **Source-local mechanics remain source-local unless explicitly promoted.** A mechanic that works in a specific donor context does not automatically work in all Astra contexts.

3. **Legality identifies source-local commands but does not execute them.** The legality service detects when a command relies on source-local rules and produces a `quarantined` result with source-local blocker detail.

4. **Legality does not perform conversion.** Converting donor mechanics to Astra equivalents is a separate process (the conversion pipeline in Aether Forge). Legality consumes the results of conversion; it does not perform conversion.

5. **Legality does not promote canon.** Identifying a source-local mechanic does not promote it to canon. Only explicit doctrine review and RT-012 authorization can promote source-local material to Astra law.

---

## 13. Corpus-scale command-family pressure

### The challenge

Astra must handle command pressure from 200–400+ donor sources across genres (fantasy, sci-fi, horror, post-apocalyptic, modern, historical) and systems (D&D, Pathfinder, Fate, Savage Worlds, GURPS, Shadowrun, World of Darkness, Powered by the Apocalypse, year-zero engine, 2d20, OSR, and dozens more).

### How legality survives this pressure

1. **Legality gates are intentionally generic.** The 18 blocker classes defined in section 9 are not tied to any specific donor system. They describe structural, contextual, and authority constraints that apply across all systems.

2. **Command-kind routing (PR-9C) absorbs classification complexity.** The 14 command-kind families (`movement`, `inspection`, `interaction`, `social`, `combat`, `ability`, `inventory`, `recovery`, `crafting`, `travel`, `research`, `mission`, `system_meta`, `unknown`) are designed to cover the command vocabulary of any TTRPG system. Legality operates on routed command kinds, not raw donor-specific action names.

3. **The `quarantined` and `unknown` statuses are release valves.** When a command from a new donor system does not fit the existing vocabulary, it is quarantined or marked unknown — not silently misclassified. This prevents the legality service from becoming a bottleneck as the corpus grows.

4. **The `deferred` status handles runtime immaturity.** When a command requires a domain service that does not yet exist, it is deferred — not rejected. This allows the legality service to operate correctly even when downstream services are incomplete.

5. **The `escalated` status handles doctrine gaps.** When a command exposes a gap in Astra doctrine, it is escalated to the doctrine council — not silently resolved by the legality service.

6. **Source-local quarantine prevents silent adoption.** Donor-specific commands are quarantined rather than silently mapped, preventing the legality service from accidentally establishing Astra law by accepting donor commands at face value.

7. **The blocker taxonomy is extensible.** New blocker classes can be added as new command families emerge from the corpus, without modifying existing legality logic. Each new blocker class follows the same pattern: player-visible safe message, backend-only detail, typical legality status.

---

## 14. Non-authority boundary matrix

This matrix explicitly declares what RT-001A does NOT authorize and which RT owner is responsible for each forbidden scope.

| Forbidden scope | Responsible RT owner | RT-001A authorizes? |
|---|---|---|
| Command execution | RT-001 (future PR) | No |
| Legality engine implementation | RT-001 (RT-001B) | No |
| State mutation | Future state service | No |
| Event append / commitment | Future transaction lifecycle service | No |
| Persistence / replay writes | RT-007 / future persistence service | No |
| RNG / table / oracle execution | RT-009 | No |
| Resource / consequence math execution | RT-002 | No |
| Affordability calculation | RT-002 | No |
| Reservation | RT-002 | No |
| Settlement | RT-002 | No |
| Consequence application | RT-002 / RT-003 / RT-004 | No |
| Combat resolution / damage calculation | RT-003 | No |
| Ability / effect / skill resolution | RT-004 | No |
| Inventory mutation | RT-010 | No |
| Mission / clue / reward routing | RT-006 | No |
| Social / faction mutation | RT-007 | No |
| Generated-content provenance | RT-008 | No |
| Context packet compilation | RT-005 | No |
| Model calls / prompt rendering | Future model harness | No |
| Prompt execution / prose parsing | Future model harness | No |
| Narration generation | Future narration service | No |
| Live-play adapter / UI / client | Future live-play gate | No |
| Conversion | Aether Forge pipeline | No |
| Sourcebook inclusion | Astra editorial process | No |
| Canon promotion | Astra Doctrine Council / RT-012 | No |

---

## 15. Relationship to PR-9A through PR-9E seams

### PR-9A: Scene command execution skeleton

RT-001A's legality boundary sits immediately after PR-9A's assembly. PR-9A assembles the typed command execution result; legality evaluates whether that assembly may proceed to downstream planning. RT-001A does not modify PR-9A.

### PR-9B: Scene command execution hardening review

PR-9B validated PR-9A's structural integrity. RT-001A inherits PR-9B's guarantees (no execution, no mutation, no model authority) and extends them into the legality boundary definition.

### PR-9C: Command-kind routing skeleton

Legality depends on PR-9C's command-kind classification to determine which blocker classes apply. The 14 command-kind families defined by PR-9C are the primary input to legality's command-family support gate.

### PR-9D: Validation integration bridge skeleton

Legality consumes PR-9D's validation results as an upstream input. Validation failures from PR-9D produce validation integration blockers in legality.

### PR-9E: Transaction preview packet bridge skeleton / authority flag hardening

Legality results feed into PR-9E's packet bridge. A command that fails legality does not receive a transaction preview packet. PR-9E's authority flag hardening pattern (all flags false-only, reject any non-False value) is the model for any authority flags RT-001B may add.

---

## 16. Later implementation sequence

RT-001A is planning only. The following implementation PRs should follow in order:

### RT-001B — Action legality skeleton dataclasses/constants/validators/serializers

- Create or extend `src/astra_runtime/domain/action_legality.py` with legality status constants, blocker class constants, blocker record dataclasses, legality result dataclasses, player-visible/backend-only serializers.
- All authority flags false-only.
- Skeleton only — no legality evaluation logic.
- Tests for import/export, construction, validation, serialization, hidden-info safety.

### RT-001C — Action legality gate integration skeleton

- Wire legality evaluation skeleton into the PR-9A through PR-9E command path.
- Produce legality results for assembled commands without evaluating domain-specific rules.
- All commands return `deferred` or `unknown` until domain services exist.
- Tests for integration with PR-9A assembly, PR-9C routing, PR-9D validation bridge, PR-9E packet bridge.

### RT-001D — Action legality hardening review

- Review and harden RT-001B and RT-001C.
- Validate hidden-information containment.
- Validate blocker taxonomy coverage.
- Validate player-visible/backend-only separation.
- Validate corpus-scale command-family pressure handling.

### Future dependent PRs (not sequenced here)

- RT-002A+ — Resource/consequence math skeleton (depends on legality gate for cost precheck handoff).
- RT-003A+ — Combat/hazard/damage/recovery skeleton (depends on legality gate for combat command routing).
- RT-004A+ — Ability/effect/skill binding skeleton (depends on legality gate for ability command routing).
- RT-009A+ — Runtime RNG/table/oracle skeleton (depends on legality gate for randomness dependency declaration).
- Persistence/replay implementation (depends on legality trace being well-defined).
- Live-play integration (depends on legality producing player-visible results).

---

## 17. Validation checklist

| Check | Status |
|---|---|
| Action legality defined as gate, not executor | Defined |
| Legality ownership boundary specified | Specified |
| Legality non-ownership boundary specified | Specified |
| Upstream surfaces identified | Identified |
| Downstream surfaces identified | Identified |
| Seven legality statuses defined (legal, illegal, blocked, deferred, quarantined, unknown, escalated) | Defined |
| Eighteen blocker classes defined | Defined |
| Player-visible / backend-only separation specified | Specified |
| Hidden-information containment rules specified | Specified |
| Source-local / donor-specific handling specified | Specified |
| Corpus-scale command-family pressure analysis complete | Complete |
| Non-authority boundary matrix complete | Complete |
| Relationship to PR-9A through PR-9E documented | Documented |
| Later implementation sequence specified | Specified |
| No command execution added | Confirmed |
| No legality engine implementation added | Confirmed |
| No state mutation added | Confirmed |
| No event append added | Confirmed |
| No persistence or replay writes added | Confirmed |
| No RNG/table/oracle execution added | Confirmed |
| No resource/consequence math execution added | Confirmed |
| No affordability calculation added | Confirmed |
| No reservation or settlement added | Confirmed |
| No consequence application added | Confirmed |
| No model calls or prompt rendering added | Confirmed |
| No narration generation added | Confirmed |
| No UI/client behavior added | Confirmed |
| No conversion added | Confirmed |
| No sourcebook inclusion added | Confirmed |
| No canon promotion added | Confirmed |

---

## 18. RT-001A final decision

RT-001A is a planning/review-only artifact. It defines the action legality boundary, blocker taxonomy, legality status vocabulary, hidden-information containment rules, player-visible/backend-only separation, source-local handling, corpus-scale pressure analysis, non-authority boundary matrix, upstream and downstream surface identification, and future implementation sequence. It authorizes no execution behavior.

---

## 19. Gate finding

```yaml
gate_finding:
  action_legality_service_plan_defined: true
  execution_boundary_review_complete: true
  legality_status_vocabulary_defined: true
  blocker_class_taxonomy_defined: true
  hidden_information_containment_specified: true
  player_visible_backend_only_separation_specified: true
  source_local_handling_specified: true
  corpus_scale_pressure_reviewed: true
  upstream_downstream_surfaces_identified: true
  later_implementation_sequence_defined: true
  action_legality_engine_authorized_by_this_pr: false
  command_execution_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  resource_math_authorized_by_this_pr: false
  rng_table_oracle_authorized_by_this_pr: false
  persistence_replay_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  narration_generation_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  sourcebook_inclusion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
  next_step_authorized: RT-001B action legality skeleton dataclasses/constants/validators/serializers
  next_step_status: narrow_skeleton_implementation_pending_review
```

---

## 20. Classification block

```yaml
runtime_domain_rt_001a:
  review_id: RUNTIME-DOMAIN-RT-001A-ACTION-LEGALITY-SERVICE-PLAN-001
  artifact_type: action_legality_service_plan_and_execution_boundary_review
  implementation_status: non_executable_plan
  derives_from:
    - RUNTIME-DOMAIN-PR-9-POST-PR8-RUNTIME-GENERALIZATION-PLANNING-001
    - RUNTIME-DOMAIN-PR-9A-SCENE-COMMAND-EXECUTION-SKELETON-001
    - RUNTIME-DOMAIN-PR-9B-SCENE-COMMAND-EXECUTION-HARDENING-REVIEW-001
    - RUNTIME-DOMAIN-PR-9C-COMMAND-KIND-ROUTING-SKELETON-001
    - RUNTIME-DOMAIN-PR-9D-VALIDATION-INTEGRATION-BRIDGE-SKELETON-001
    - RUNTIME-DOMAIN-PR-9E-TRANSACTION-PREVIEW-PACKET-BRIDGE-SKELETON-001
    - RUNTIME-DOMAIN-PR-1-COMMAND-LIFECYCLE-ACTION-LEGALITY-SERVICE-PLAN-001
    - RT-001
    - RT-002
    - RT-005
    - RT-009
    - RT-011
    - RT-012
  defines_action_legality_boundary: true
  defines_legality_status_vocabulary: true
  defines_blocker_class_taxonomy: true
  defines_hidden_information_containment: true
  defines_player_visible_backend_only_separation: true
  defines_source_local_handling: true
  defines_corpus_scale_pressure_review: true
  defines_upstream_downstream_surfaces: true
  defines_later_implementation_sequence: true
  defines_non_authority_boundary_matrix: true
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
  authorizes_rng_table_oracle_by_this_pr: false
  authorizes_persistence_replay_by_this_pr: false
  authorizes_narration_generation_by_this_pr: false
  authorizes_live_play_by_this_pr: false
  authorizes_ui_client_by_this_pr: false
  authorizes_training_by_this_pr: false
  authorizes_pilot_conversion_by_this_pr: false
  authorizes_sourcebook_inclusion_by_this_pr: false
  authorizes_canon_promotion_by_this_pr: false
  next_allowed_step: RT-001B action legality skeleton dataclasses/constants/validators/serializers, pending review
```

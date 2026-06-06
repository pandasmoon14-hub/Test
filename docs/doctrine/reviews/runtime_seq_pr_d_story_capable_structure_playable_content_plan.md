# RUNTIME-SEQ-PR-D: Story-Capable Structure and Playable-Content Plan

---

## 1. Purpose and status

This document is **RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001**, a story-capable structure and playable-content plan.

It is **planning-only and non-executable**.

It defines future story-capable structure, playable-content, narrative substrate, storylet, quest/scenario dependency, NPC goal, dialogue-act, content ecology, source-local capsule, and generator-to-validate-to-commit contracts, but it does not implement:

- runtime code;
- storylet system;
- narrative substrate schema;
- playable-content validator;
- quest/scenario engine;
- dependency DAG engine;
- NPC AI;
- behavior tree;
- dialogue system;
- dialogue-act IR;
- content ecology engine;
- generator implementation;
- schema implementation;
- command IR;
- event ledger;
- state store;
- validators;
- context-packet compiler;
- prompt templates;
- live-play adapter;
- training data;
- donor-content audit;
- pilot conversion;
- sourcebook inclusion;
- canon promotion.

Date: 2026-06-06

Primary owner tracks: RT-006, RT-007, RT-008, RT-011, RT-012

Supporting owner tracks: RT-001, RT-002, RT-003, RT-004, RT-005, RT-009, RT-010

---

## 2. Source ledger

All source artifacts used in the creation of this plan:

### Core sequencing and runtime-quality sources

| Artifact ID | Path | Present |
|---|---|---|
| RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001 | `docs/doctrine/reviews/runtime_schema_implementation_sequencing_review.md` | Yes |
| RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_a_minimum_backend_kernel_runtime_quality_contract_plan.md` | Yes |
| RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_b_narration_context_packet_contract_plan.md` | Yes |
| RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_c_state_event_invariant_transaction_plan.md` | Yes |

### Audit and closure sources

| Artifact | Path | Present |
|---|---|---|
| Runtime Boundary Generator Ownership Audit Protocol | `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md` | Yes |
| Stage 2 Completion Review and Closure Ledger | `docs/doctrine/reviews/runtime_boundary_generator_ownership_stage2_completion_review_and_closure_ledger.md` | Yes |

### RT owner specifications (RT-001 through RT-012)

| Owner Track | Path | Present | Role in PR-D |
|---|---|---|---|
| RT-001 | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md` | Yes | Supporting — playable action declaration, command lifecycle, transaction gating |
| RT-002 | `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md` | Yes | Supporting — cost/reward/loss/consequence routing |
| RT-003 | `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md` | Yes | Supporting — hazard/opposition/damage pressure in playable content |
| RT-004 | `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md` | Yes | Supporting — ability/effect/skill affordances and prerequisites |
| RT-005 | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md` | Yes | Supporting — hidden hooks, visibility, reveal boundaries, packet projection |
| RT-006 | `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md` | Yes | **Primary** — mission/scenario/objective/clue/reward routes |
| RT-007 | `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md` | Yes | **Primary** — social/faction/actor knowledge, dialogue claims, NPC goal knowledge |
| RT-008 | `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md` | Yes | **Primary** — generated playable content provenance/recurrence |
| RT-009 | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md` | Yes | Supporting — random storylet/table/oracle dependencies |
| RT-010 | `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md` | Yes | Supporting — item/asset/vehicle/cargo affordances and rewards/losses |
| RT-011 | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md` | Yes | **Primary** — playability validation and readiness gates |
| RT-012 | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md` | Yes | **Primary** — source-local/native-design/promotion boundaries |

### Schema / content-record sources (C00–C14)

| Schema | Path | Present |
|---|---|---|
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

### Schema/math/mechanics sources (SM00–SM02)

| File | Path | Present |
|---|---|---|
| SM00 | `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` | Yes |
| SM01 | `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md` | Yes |
| SM02 | `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md` | Yes |

### Operational / Batch B sources

| File | Path | Present |
|---|---|---|
| B01 | `docs/doctrine/operations/batch_b/B01_scene_activity_orchestration_and_runtime_authority_procedure.md` | Yes |
| B07 | `docs/doctrine/operations/batch_b/B07_mission_objective_reward_and_failure_routing_procedure.md` | Yes |
| B08 | `docs/doctrine/operations/batch_b/B08_clue_revelation_information_routing_and_investigation_procedure.md` | Yes |
| B09 | `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md` | Yes |
| B10 | `docs/doctrine/operations/batch_b/B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md` | Yes |

### Native design sources

| File | Path | Present |
|---|---|---|
| Native design directory | `docs/doctrine/native_design/` | Yes |

### Governance sources

| File | Path | Present |
|---|---|---|
| Roadmap | `docs/doctrine/astra_doctrine_roadmap_v0_1.md` | Yes |
| Registry | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` | Yes |
| Decision log | `docs/decisions/current_decisions_log.md` | Yes |
| README | `README.md` | Yes |

---

## 3. Backend-first invariant

Astra Ascension must be **model-interchangeable**. The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

### Playable-content implication

Playable content must be backend-owned structure before it is narrated. The LLM may propose or render visible options, but it must not:

- create durable story truth;
- decide quest state;
- mutate NPC goals;
- create clues;
- assign rewards;
- promote source-local content;
- commit scenario consequences.

All of these are backend-owned operations that require validation and commitment through the transaction lifecycle defined in RUNTIME-SEQ-PR-C.

---

## 4. Story-capable structure principle

Astra does not rely on the model to "make a good story" from memory. Astra stores and validates structures that are **capable of producing story through play**.

Story-capable structures must:

1. Expose player agency.
2. Contain actionable affordances.
3. Have stateful consequences.
4. Identify involved records.
5. Identify visibility boundaries.
6. Identify failure and partial-success paths.
7. Identify reward/loss/consequence routing.
8. Identify source/provenance.
9. Identify escalation hooks.
10. Identify validation requirements.
11. Remain renderable by a small local narrator packet.

"Story-capable" is **not** "narrative prose." It is **not** "canon." It is **not** "sourcebook text." It is **not** "LLM memory."

Story-capable structures are backend-owned data that, when projected through the narration layer, produce coherent play experiences. The model renders them; the model does not author them.

---

## 5. Playable-content boundary

The following future playable-content families are defined at the planning level. All are marked `future_required_not_implemented`.

### 5.1 PlayableSceneStructure

- **Purpose:** Represents a scene as a playable unit with structure, participants, affordances, and consequence routes.
- **Primary owner:** RT-006 (mission/scenario routing) with RT-001 (command lifecycle).
- **Required backend handoffs:** Scene activation, scene state tracking, scene conclusion routing, consequence commitment.
- **LLM allowed interaction:** Render visible scene description, atmosphere, and visible affordances. May not invent new actionable objects, create hidden facts, or resolve scene consequences.
- **Visibility requirements:** Scene visibility tiers route through RT-005. Hidden hooks are redacted references only.
- **Validation requirements:** Scene must pass playability proof (Section 6) before commitment. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.2 NarrativeSubstrate

- **Purpose:** Provides the dramatic and sensory context layer that makes a scene renderable without being prose, state, or authority. See Section 7 for full planning contract.
- **Primary owner:** RT-005 (context-packet/hidden-information) with RT-008 (generated-content provenance).
- **Required backend handoffs:** Substrate generation or authoring, substrate validation, substrate projection into NarrationRenderPacket.
- **LLM allowed interaction:** Render atmosphere and sensory details from substrate. May not treat substrate as state, canon, or event authority.
- **Visibility requirements:** Substrate contains visible and redacted-reference fields only. Hidden stakes appear as references, never content.
- **Validation requirements:** Substrate must not contain prose authority, hidden facts, or event commitments. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.3 SceneObjectContract

- **Purpose:** Defines minimum requirements for objects that exist in a scene as interactive, stateful entities. See Section 15.
- **Primary owner:** RT-010 (inventory/item/vehicle/asset) with RT-001 (command lifecycle).
- **Required backend handoffs:** Object state ownership, interaction affordance declaration, consequence routing, visibility projection.
- **LLM allowed interaction:** Render visible description and visible affordances. May not create new interactive objects or promote decorative objects to interactive state.
- **Visibility requirements:** Object visibility tier routes through RT-005.
- **Validation requirements:** Interactive objects must have state owner, consequence route, and packet projection rule. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.4 StoryletContract

- **Purpose:** Defines bounded, triggerable story units that can declare hooks, outcomes, and routing without committing results. See Section 8.
- **Primary owner:** RT-006 (mission/scenario routing) with RT-008 (generated-content provenance).
- **Required backend handoffs:** Trigger evaluation, prerequisite validation, eligibility check, outcome commitment, reward/loss routing.
- **LLM allowed interaction:** Render visible storylet hooks and options. May not trigger storylets, resolve outcomes, or commit consequences.
- **Visibility requirements:** Storylets declare visible hooks and hidden references separately. RT-005 projection rules apply.
- **Validation requirements:** Storylet must be bounded, provenance-backed, and source-local unless promoted. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.5 ScenarioNodeContract

- **Purpose:** Represents a node in a quest/scenario dependency DAG with dependencies, branches, and routing. Part of Section 9.
- **Primary owner:** RT-006 (mission/scenario routing).
- **Required backend handoffs:** Node activation, dependency resolution, branch routing, objective state tracking, consequence commitment.
- **LLM allowed interaction:** Render visible objectives and available paths. May not advance DAG state, resolve dependencies, or complete objectives.
- **Visibility requirements:** Node visibility boundaries route through RT-005. Hidden dependencies are redacted references only.
- **Validation requirements:** Node must have at least one dependency or entry condition, and at least one consequence route. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.6 QuestScenarioDependencyDAG

- **Purpose:** Represents the full dependency graph for a quest or scenario. See Section 9.
- **Primary owner:** RT-006 (mission/scenario routing).
- **Required backend handoffs:** DAG initialization, node activation, edge traversal, branch resolution, completion detection, reward routing.
- **LLM allowed interaction:** Render visible quest/scenario status and available objectives. May not mutate DAG state, activate nodes, or resolve branches.
- **Visibility requirements:** DAG visibility boundaries route through RT-005. Hidden branches and dependencies are redacted references only.
- **Validation requirements:** DAG must be acyclic where required, must have at least one reachable completion path, and must route all rewards/losses through RT-002/RT-006. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.7 PlayabilityProofContract

- **Purpose:** Validates that a playable unit meets minimum playability requirements. See Section 6.
- **Primary owner:** RT-011 (validation/readiness).
- **Required backend handoffs:** Proof generation, proof validation, proof storage, failure routing.
- **LLM allowed interaction:** None. Playability proof is a backend-only validation artifact.
- **Visibility requirements:** Proof results may be surfaced to reviewers. Not player-visible.
- **Validation requirements:** Proof must verify all requirements listed in Section 6.
- **Implementation status:** `future_required_not_implemented`

### 5.8 PlayerAgencyAffordanceSet

- **Purpose:** Declares the set of player-facing actions available in a playable context.
- **Primary owner:** RT-001 (command lifecycle/action legality).
- **Required backend handoffs:** Affordance declaration, legality checking, command routing, consequence commitment.
- **LLM allowed interaction:** Render visible affordances. May suggest actions within declared set. May not invent new affordances or declare actions legal.
- **Visibility requirements:** Affordances inherit visibility from their parent structure. RT-005 projection rules apply.
- **Validation requirements:** At least one affordance must exist per playable unit. Each affordance must route to a consequence. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.9 ConsequenceRouteContract

- **Purpose:** Declares how consequences flow from actions through backend systems.
- **Primary owner:** RT-002 (resource/consequence math) with RT-006 (mission routing).
- **Required backend handoffs:** Consequence evaluation, cost/reward calculation, state delta preparation, event commitment.
- **LLM allowed interaction:** Render visible consequences after commitment. May not evaluate, calculate, or commit consequences.
- **Visibility requirements:** Consequence preview may be visible. Hidden consequences are redacted references only. RT-005 projection rules apply.
- **Validation requirements:** Every consequence route must reach a backend owner. No dangling consequence routes. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.10 FailurePartialSuccessContract

- **Purpose:** Declares failure and partial-success paths for playable content.
- **Primary owner:** RT-006 (mission/scenario routing) with RT-002 (resource/consequence math).
- **Required backend handoffs:** Failure detection, partial-success evaluation, consequence routing, fallback routing.
- **LLM allowed interaction:** Render visible failure or partial-success outcomes after commitment. May not decide success/failure or evaluate partial success.
- **Visibility requirements:** Failure conditions may be visible or hidden depending on context. RT-005 projection rules apply.
- **Validation requirements:** Playable units must identify at least one failure or complication route unless deliberately exempted. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.11 EscalationHookContract

- **Purpose:** Declares how playable content can escalate to broader consequences, new scenarios, or faction responses.
- **Primary owner:** RT-006 (mission/scenario routing) with RT-007 (social/faction).
- **Required backend handoffs:** Escalation detection, hook activation, consequence routing, faction/social response routing.
- **LLM allowed interaction:** Render visible escalation warning or consequence. May not activate escalation hooks or commit escalation consequences.
- **Visibility requirements:** Escalation hooks may be visible or hidden. RT-005 projection rules apply.
- **Validation requirements:** Escalation hooks must route to backend owners. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.12 ClueRoutePlayableContract

- **Purpose:** Declares how clues and hidden truths route through playable content.
- **Primary owner:** RT-006 (mission/scenario routing) with RT-005 (context-packet/hidden-information).
- **Required backend handoffs:** Clue placement, reveal authorization, visibility projection, investigation routing.
- **LLM allowed interaction:** Render visible clue presence. May not reveal hidden truths, create clues, or authorize reveals.
- **Visibility requirements:** Clue visibility follows RT-005 hidden-information rules. Reveals require backend authorization.
- **Validation requirements:** Clue routes must connect to RT-005 and RT-006. Hidden truths must not leak. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.13 RewardRoutePlayableContract

- **Purpose:** Declares how rewards and losses route through playable content.
- **Primary owner:** RT-006 (mission/scenario routing) with RT-002 (resource/consequence math) and RT-010 (inventory/item/vehicle/asset).
- **Required backend handoffs:** Reward evaluation, loss evaluation, resource math, item/asset routing, consequence commitment.
- **LLM allowed interaction:** Render visible reward/loss after commitment. May not evaluate, calculate, or commit rewards or losses.
- **Visibility requirements:** Reward/loss routing may be visible or hidden. RT-005 projection rules apply.
- **Validation requirements:** All reward/loss routes must reach RT-002, RT-006, or RT-010. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.14 SocialContactPlayableContract

- **Purpose:** Declares how social and faction interactions route through playable content.
- **Primary owner:** RT-007 (social/faction/actor knowledge).
- **Required backend handoffs:** Social state evaluation, faction response routing, relationship mutation, reputation consequence, dialogue-act validation.
- **LLM allowed interaction:** Render visible social interactions and dialogue. May not commit social state, mutate relationships, decide faction responses, or create knowledge claims.
- **Visibility requirements:** Social visibility follows RT-005 and RT-007 rules. Actor knowledge is not player knowledge.
- **Validation requirements:** Social routes must connect to RT-007. Knowledge claims must be validated. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.15 HazardPressurePlayableContract

- **Purpose:** Declares how hazards and opposition pressure integrate into playable content.
- **Primary owner:** RT-003 (combat/hazard/damage/recovery).
- **Required backend handoffs:** Hazard activation, damage evaluation, exposure tracking, recovery routing, consequence commitment.
- **LLM allowed interaction:** Render visible hazard presence and consequences after commitment. May not activate hazards, evaluate damage, or commit harm.
- **Visibility requirements:** Hazard visibility follows RT-005 rules. Hidden hazards are redacted references only.
- **Validation requirements:** Hazard routes must connect to RT-003. Damage/recovery must route through RT-002. RT-011 readiness gate.
- **Implementation status:** `future_required_not_implemented`

### 5.16 SourceLocalCapsulePlayableBoundary

- **Purpose:** Declares the boundary conditions for source-local content within playable structures. See Section 13.
- **Primary owner:** RT-012 (D-series/native-design promotion boundary) with RT-008 (generated-content provenance).
- **Required backend handoffs:** Source-local classification, promotion routing, quarantine routing, provenance tracking.
- **LLM allowed interaction:** Render source-local content within its declared scope. May not promote source-local content to global scope, canon, or sourcebook status.
- **Visibility requirements:** Source-local content visibility follows RT-005 and RT-012 rules.
- **Validation requirements:** Source-local capsules must declare scope, provenance, and promotion status. RT-011 and RT-012 readiness gates.
- **Implementation status:** `future_required_not_implemented`

---

## 6. Playability proof contract

This section defines planning-level requirements for a future PlayabilityProofContract.

A generated or authored playable unit must eventually prove:

1. At least one player-facing action exists.
2. At least one meaningful consequence route exists.
3. At least one failure, cost, or complication route exists unless deliberately exempted.
4. Visible hooks are not secretly required to understand hidden facts.
5. Required resources, actors, locations, and items exist or are generated with provenance.
6. Rewards and losses route through RT-002, RT-006, RT-010, or RT-007 as applicable.
7. Clues and hidden truths route through RT-005 and RT-006.
8. Social and faction consequences route through RT-007.
9. Hazards and opposition route through RT-003.
10. Random dependencies route through RT-009.
11. Generated content routes through RT-008.
12. Promotion and source-local boundaries route through RT-012.
13. Narration renderability routes through RUNTIME-SEQ-PR-B.

Playability proof is **future validation planning only**, not an implemented validator.

No playability proof validator, schema, or runtime gate is created by this plan.

---

## 7. Narrative substrate contract

This section defines future NarrativeSubstrate as a planning concept.

A NarrativeSubstrate may eventually include:

- **Scene purpose:** What the scene is for in the scenario/quest context.
- **Dramatic pressure:** What tension or stakes drive the scene.
- **Active participants:** Which actors, factions, or entities are present.
- **Visible stakes:** What the player can see is at risk.
- **Hidden stakes:** Reference only, never content. Hidden stakes route through RT-005.
- **Affordances:** What actions are available to the player.
- **Constraints:** What actions are unavailable or restricted and why.
- **Sensory palette:** Environmental and atmospheric details for narration rendering.
- **Escalation vectors:** How the scene can escalate in pressure or consequence.
- **Consequence routes:** Where outcomes route after player action.
- **Unresolved hooks:** What story threads remain open after scene resolution.
- **Source/provenance:** Where the substrate originated (authored, generated, converted, source-local).
- **Validation requirements:** What must be validated before the substrate is committed or projected.

NarrativeSubstrate is **not** prose. It is **not** a prompt template. It is **not** canon. It is **not** event state. It is **not** a substitute for scenario state. It is **not** live-play authority by itself.

NarrativeSubstrate is a structured, validated input to the narration layer that helps the narrator render a coherent scene without inventing facts, creating state, or resolving consequences.

---

## 8. Storylet contract

This section defines future StoryletContract as a planning concept.

Storylets must be:

1. **Bounded:** Each storylet has a defined scope, entry, and exit.
2. **Triggerable by backend state:** Storylet activation depends on backend-evaluated conditions, not LLM judgment.
3. **Eligible only when prerequisites are backend-validated:** Prerequisites are checked by the backend before a storylet becomes available.
4. **Able to declare visible hooks:** Storylets expose player-facing hooks that signal available opportunities.
5. **Able to declare hidden references without exposing hidden facts:** Hidden references are redacted pointers that route through RT-005, not content.
6. **Able to declare outcomes without committing them:** Storylets describe possible outcomes; only backend commitment makes outcomes real.
7. **Able to route rewards/losses/clues/consequences to owners:** All outcome routes connect to RT-002, RT-005, RT-006, RT-007, RT-008, RT-009, RT-010, or RT-012 as applicable.
8. **Provenance-backed if generated:** Generated storylets carry RT-008 provenance. LLM-proposed storylets are candidates only.
9. **Source-local unless promoted:** Storylets derived from donor or source-local material remain source-local and route through RT-012 for any promotion.
10. **Disabled/quarantined if invalid:** Storylets that fail validation are disabled or quarantined, not silently served.

This plan does not implement a storylet engine, storylet triggers, eligibility logic, or storylet schemas.

---

## 9. Quest/scenario dependency DAG contract

This section defines future QuestScenarioDependencyDAG as a planning concept.

A QuestScenarioDependencyDAG should eventually represent:

- **Scenario nodes:** Discrete points in a quest/scenario with state, objectives, and transitions.
- **Objective dependencies:** Which objectives must be completed before others become available.
- **Clue dependencies:** Which clues must be discovered before information becomes available.
- **Branch dependencies:** Which branches require which conditions to become traversable.
- **Route dependencies:** Which routes connect nodes and under what conditions.
- **Reward/loss dependencies:** Which rewards or losses are contingent on which node outcomes.
- **Failure/partial-success branches:** What happens when objectives are failed or partially completed.
- **Faction/social dependencies:** Which nodes depend on faction standing, social state, or relationship conditions.
- **Hazard/opposition dependencies:** Which nodes involve active threats or opposition pressure.
- **Generated-content dependencies:** Which nodes contain generated content requiring RT-008 provenance.
- **Source-local/provenance boundaries:** Which nodes contain source-local content requiring RT-012 boundary enforcement.
- **Visibility and hidden-truth boundaries:** Which dependencies, branches, or routes are hidden from the player and route through RT-005.

This is **not** a quest engine. It is **not** a route planner. It is **not** a branch engine. It is **not** a graph schema. It is **not** a runtime implementation.

---

## 10. NPC goal stack and actor-intent contract

This section defines future NPCGoalStack and ActorIntentContract as planning concepts.

They may eventually track:

- **Visible behavior goals:** What the NPC appears to be pursuing based on observable behavior.
- **Hidden motives:** Redacted references only. Hidden motives route through RT-005 and RT-007.
- **Current intent:** The NPC's immediate behavioral objective in the current scene.
- **Constraints:** What the NPC cannot or will not do and why.
- **Resources:** What the NPC has access to (equipment, allies, information, authority).
- **Relationships:** The NPC's relationships with other actors, factions, and the player.
- **Faction obligations:** What the NPC owes to or expects from faction membership.
- **Mission ties:** How the NPC connects to active missions, scenarios, or quests.
- **Risk tolerance:** How much danger or cost the NPC will accept.
- **Escalation triggers:** What conditions cause the NPC to escalate behavior.
- **Abandonment conditions:** What conditions cause the NPC to abandon current goals.
- **Knowledge-state dependencies:** What the NPC knows, believes, suspects, and does not know, routed through RT-007.

### Constraints

- NPC goals are backend-owned state or generated candidates only after future authorization.
- The LLM may render NPC behavior but may not decide private motives, actor knowledge, faction knowledge, or goal mutation.
- Actor knowledge routes through RT-007 and hidden-info projection through RT-005.

This plan does not implement NPC AI, behavior trees, planners, goal stacks, or dialogue agents.

---

## 11. DialogueActIR planning contract

This section defines future DialogueActIR as a planning concept.

DialogueActIR may eventually classify dialogue as:

- **ask** — request information.
- **answer** — provide information.
- **refuse** — decline a request or demand.
- **threaten** — declare intent to harm or impose cost.
- **bargain** — propose a trade or exchange.
- **deceive** — present false information as true.
- **reveal** — disclose previously hidden information.
- **conceal** — withhold information without explicitly lying.
- **command** — issue an order or directive.
- **plead** — appeal to emotion, mercy, or shared interest.
- **distract** — redirect attention from a topic or action.
- **promise** — commit to a future action or outcome.
- **accuse** — assign blame or responsibility.
- **confess** — admit to an action, knowledge, or intent.
- **misdirect** — guide attention or belief toward a false conclusion.
- **recruit** — attempt to gain an ally, follower, or collaborator.
- **intimidate** — use fear or authority to influence behavior.
- **comfort** — offer reassurance, support, or emotional aid.

### For each dialogue act family, future systems must distinguish:

- **Spoken text:** What was literally said.
- **Intended social move:** What the speaker is trying to accomplish.
- **Knowledge claim:** What factual assertion is embedded in the dialogue.
- **Truth status:** Whether the knowledge claim is true, false, uncertain, or unverifiable.
- **Visibility:** Who can hear, observe, or learn about the dialogue act.
- **Consequence route:** What social, faction, or relationship consequence follows.
- **Validation requirement:** What must be validated before the dialogue act's consequences are committed.

### Constraints

- Dialogue text is not social state.
- Dialogue transcript is not actor knowledge.
- Promises, debts, and favors require backend commitment through RT-007 and RT-002.
- Reveals require RT-005, RT-006, and RT-007 authorization.
- Deception, rumor, and false claims must not become verified facts without validation through RT-007.

This plan does not implement DialogueActIR, social mechanics, dialogue engine, or transcript parser.

---

## 12. Content ecology contract

This section defines future ContentEcologyContract as a planning concept.

Content ecology should prevent generated or converted content from becoming an incoherent pile by requiring future tracking of:

- **Active content pressure:** How much content is currently live, available, and demanding player attention.
- **Dormant content:** Content that exists but is not currently available or pressuring the player.
- **Source-local content:** Content that remains within its source-local scope and has not been promoted.
- **Recurring content:** Content that has appeared before and may appear again, tracked through RT-008.
- **Exhausted content:** Content that has been fully consumed, resolved, or is no longer viable.
- **Quarantined content:** Content that failed validation or was blocked for other reasons.
- **Faction/location/theme density:** How concentrated content is around particular factions, locations, or themes.
- **Encounter/hazard/reward repetition pressure:** Whether encounters, hazards, or rewards are repeating in ways that harm variety.
- **Unresolved hook accumulation:** How many unresolved story hooks are active and whether they exceed manageable levels.
- **Contradiction pressure:** Whether active content contradicts other active content in ways that break coherence.
- **Escalation saturation:** Whether too many active threads are at high escalation levels simultaneously.
- **Tone/theme drift:** Whether the overall tone or theme of active content has drifted from the intended campaign direction.

Content ecology is **not** canon. It is **not** sourcebook inclusion. It is **not** a generator. It is **not** a live-play pacing engine unless separately authorized.

---

## 13. Source-local capsule boundary expansion

This section expands SourceLocalCapsuleBoundary from PR-A and PR-B planning.

A future source-local capsule should eventually identify:

- **Source-local assumptions:** What setting, cosmology, or rules the content assumes from its source.
- **Allowed use scope:** Where and how the source-local content may be used within Astra.
- **Prohibited globalizations:** What aspects of the source-local content must not be treated as global Astra truth.
- **Active/inactive status:** Whether the capsule is currently active in a campaign or session.
- **Promotion status:** Whether the content has been promoted, is pending promotion, or is permanently source-local.
- **Provenance:** Where the content came from (donor, conversion, generation, authoring).
- **Owner RT handoffs:** Which RT tracks are responsible for the content within the capsule.
- **Hidden-info restrictions:** What hidden information within the capsule routes through RT-005.
- **Generator eligibility:** Whether generators may produce content within this capsule's scope.
- **Canon/sourcebook exclusion:** Content remains excluded from canon and sourcebook status unless promoted through RT-012 and governance routing.
- **Packet visibility restrictions:** How the capsule's content is projected into NarrationRenderPackets and ContextPackets.

Source-local capsules **cannot** become canon, sourcebook content, training data, or global Astra law without RT-012 governance routing and explicit promotion authorization.

---

## 14. Generator-to-validate-to-commit pipeline

This section defines the future generator-to-validate-to-commit pipeline as a planning concept.

The pipeline stages are:

1. **generate_candidate** — A generator (backend or LLM-assisted) produces a candidate playable structure.
2. **assign_provenance** — The candidate receives RT-008 provenance tracking.
3. **classify_source_scope** — The candidate is classified as source-local, Astra-native, or converted, with RT-012 boundary enforcement.
4. **validate_schema_readiness** — The candidate is checked against relevant C-schema and SM requirements.
5. **validate_playability** — The candidate undergoes playability proof (Section 6).
6. **validate_owner_handoffs** — All RT-owner handoffs are verified (RT-001 through RT-012 as applicable).
7. **validate_visibility** — Visibility and hidden-information rules are verified through RT-005.
8. **validate_invariants** — WorldInvariantRegistry checks from PR-C are applied.
9. **validate_packet_renderability** — The candidate can be projected into a NarrationRenderPacket per PR-B.
10. **quarantine_or_repair_if_invalid** — Invalid candidates are quarantined or sent to repair. Repair does not bypass validation.
11. **reviewer_or_backend_acceptance_if_required** — Candidates requiring human review are routed to reviewers. Backend acceptance applies where automated acceptance is authorized.
12. **commit_as_runtime_record_if_authorized** — The candidate is committed as a runtime record only if authorized by future implementation.
13. **project_to_packets** — Committed content is projected to narration/context packets only after commitment.

### Pipeline constraints

- Generation is not commitment.
- Repair is not commitment.
- Judge/evaluator approval is not commitment unless backend-authorized.
- LLM proposal is not durable content.
- Visible narration is not generated-content provenance.

This plan does not implement the generator, repair loop, evaluator, schema, validator, commitment, or persistence stages.

---

## 15. Minimum viable scene object contract

This section defines future MinimumViableSceneObject requirements.

A scene object should eventually have:

- **Identity/provenance:** Unique identifier and provenance record (authored, generated, converted, source-local).
- **Visible description:** Player-facing description text for narration rendering.
- **Interaction affordance:** At least one declared way the player can interact with the object.
- **State owner:** Which backend system owns the object's state.
- **Visibility tier:** The object's visibility level per RT-005 rules.
- **Consequence route:** What happens when the object is interacted with, and where consequences route.
- **Validation requirement:** What must be validated before the object is interactive.
- **Packet projection rule:** How the object appears in NarrationRenderPackets and ContextPackets.
- **Source-local/canon boundary:** Whether the object is source-local, Astra-native, or canon, and RT-012 boundary enforcement.
- **Event/state handoff:** How object interactions produce events and state changes through the PR-C transaction lifecycle.

Decorative prose-only objects are allowed in narration but cannot become interactive state unless promoted into backend-owned scene objects through the generator-to-validate-to-commit pipeline (Section 14).

---

## 16. Runtime/narration handoff

This section defines how story-capable structures relate to RUNTIME-SEQ-PR-B packet contracts.

- Backend structure produces visible affordances.
- Visible affordances enter NarrationRenderPacket.
- Hidden hooks remain hidden or redacted in packets.
- The narrator may render atmosphere and visible affordances.
- The narrator may **not** invent new actionable objects.
- The narrator may **not** create hidden facts.
- The narrator may **not** resolve storylet outcomes.
- The narrator may **not** advance quest/scenario DAG state.
- The narrator may **not** mutate NPC goals.
- The narrator may **not** create committed dialogue consequences.

Story-capable structures are the **source** of narration input. Narration is the **rendering** of approved visible structure. The flow is unidirectional: backend structure → packet projection → narration rendering. Narration output does not flow back into backend structure.

---

## 17. Runtime/event handoff

This section defines how story-capable structures relate to RUNTIME-SEQ-PR-C state/event contracts.

- Playable structures may propose transaction candidates.
- Only backend validation may produce state deltas.
- Storylet triggers are not event commits.
- Scenario node eligibility is not branch resolution.
- Quest DAG edge activation is not objective completion.
- NPC goal pressure is not actor state mutation.
- Dialogue act interpretation is not social-state commitment.
- Generated structure is not persistent state until committed through the transaction lifecycle.
- Correction events handle wrong narration or wrong playable projections.

Story-capable structures participate in the transaction lifecycle defined in PR-C but do not bypass it. All state changes flow through the standard transaction stages: preview → validate → commit → event append → narration project.

---

## 18. Domain handoff crosswalk

This section maps RT-001 through RT-012 to story-capable and playable-content responsibilities.

| Owner Track | Story-Capable / Playable-Content Responsibilities |
|---|---|
| **RT-001** | Playable action declaration, command lifecycle, transaction gating. PlayerAgencyAffordanceSet routes through RT-001 for legality. Scene actions require RT-001 command processing. |
| **RT-002** | Cost/reward/loss/consequence routing. ConsequenceRouteContract and RewardRoutePlayableContract route through RT-002 for resource math. FailurePartialSuccessContract costs route through RT-002. |
| **RT-003** | Hazard/opposition/damage pressure in playable content. HazardPressurePlayableContract routes through RT-003 for damage, exposure, and recovery. Scene hazards require RT-003 evaluation. |
| **RT-004** | Ability/effect/skill affordances and prerequisites. PlayerAgencyAffordanceSet includes ability-based actions. Storylet prerequisites may include ability/skill requirements. |
| **RT-005** | Hidden hooks, visibility, reveal boundaries, packet projection. All playable-content visibility tiers route through RT-005. ClueRoutePlayableContract hidden-truth routing routes through RT-005. NarrativeSubstrate hidden stakes are references only per RT-005. |
| **RT-006** | Mission/scenario/objective/clue/reward routes. QuestScenarioDependencyDAG, ScenarioNodeContract, StoryletContract, ClueRoutePlayableContract, RewardRoutePlayableContract, and EscalationHookContract all route through RT-006 as primary owner. PlayableSceneStructure activation routes through RT-006. |
| **RT-007** | Social/faction/actor knowledge, dialogue claims, NPC goal knowledge. SocialContactPlayableContract, NPCGoalStack, ActorIntentContract, and DialogueActIR all route through RT-007. Dialogue truth status validation routes through RT-007. |
| **RT-008** | Generated playable content provenance/recurrence. All generated storylets, scene objects, scenario nodes, NPC goals, and narrative substrates carry RT-008 provenance. ContentEcologyContract recurring content tracks through RT-008. |
| **RT-009** | Random storylet/table/oracle dependencies. QuestScenarioDependencyDAG random dependencies route through RT-009. Storylet random triggers route through RT-009. Random reward/loot routes through RT-009. |
| **RT-010** | Item/asset/vehicle/cargo affordances and rewards/losses. SceneObjectContract item interactions route through RT-010. RewardRoutePlayableContract item rewards route through RT-010. MinimumViableSceneObject item-type objects route through RT-010. |
| **RT-011** | Playability validation and readiness gates. PlayabilityProofContract is owned by RT-011. All playable-content families require RT-011 readiness gates. Generator-to-validate-to-commit pipeline validation stages route through RT-011. |
| **RT-012** | Source-local/native-design/promotion boundaries. SourceLocalCapsulePlayableBoundary is owned by RT-012. Storylet source-local status routes through RT-012. ContentEcologyContract source-local tracking routes through RT-012. No promotion without RT-012 governance. |

---

## 19. Validation and test requirements

This section identifies future test families. This PR only identifies future test requirements and adds focused doctrine tests for the planning artifact.

Future test families:

1. **Playability proof tests** — Verify that playable units meet playability proof requirements (Section 6).
2. **Story-capable structure coverage tests** — Verify that story-capable structures expose all required properties (Section 4).
3. **Narrative substrate non-prose-authority tests** — Verify that NarrativeSubstrate does not contain prose authority, hidden facts, or event commitments.
4. **Storylet eligibility boundary tests** — Verify that storylet activation depends on backend state, not LLM judgment.
5. **Quest/scenario DAG no-commitment tests** — Verify that DAG traversal proposals do not commit state changes.
6. **NPC goal stack non-LLM-authority tests** — Verify that NPC goal mutation requires backend authorization, not LLM decision.
7. **Dialogue-act truth-status tests** — Verify that dialogue knowledge claims carry truth status and route through RT-007 validation.
8. **Content ecology contradiction-pressure tests** — Verify that content ecology tracks contradictions and prevents incoherent content accumulation.
9. **Source-local capsule boundary tests** — Verify that source-local content cannot escape capsule boundaries without RT-012 promotion.
10. **Generator-to-validate-to-commit tests** — Verify that generated candidates flow through all pipeline stages and cannot bypass validation.
11. **Minimum viable scene object tests** — Verify that interactive scene objects meet minimum requirements and decorative objects cannot become interactive without promotion.
12. **Packet renderability tests** — Verify that story-capable structures can be projected into NarrationRenderPackets per PR-B.
13. **Event/state handoff tests** — Verify that playable structures participate in the PR-C transaction lifecycle without bypassing it.
14. **Hidden-info leakage tests** — Verify that hidden hooks, hidden stakes, hidden motives, and hidden dependencies do not appear in player-visible packets or narration.
15. **LLM overreach/adversarial story tests** — Verify that LLM narration cannot invent actionable objects, resolve outcomes, mutate NPC goals, or commit consequences.

---

## 20. Blocked-until ledger

The following remain blocked and are not implemented by this plan:

- Narrative substrate schema — blocked until PR-D is reviewed and schema implementation is authorized.
- Storylet system — blocked until storylet schema, trigger engine, and eligibility logic are authorized.
- Storylet engine — blocked until storylet system authorization.
- Quest/scenario dependency DAG implementation — blocked until DAG schema and graph engine are authorized.
- Quest engine — blocked until quest/scenario system authorization.
- Scenario engine — blocked until quest/scenario system authorization.
- NPC goal stack implementation — blocked until NPC state schema and goal engine are authorized.
- NPC AI — blocked until NPC goal stack, behavior evaluation, and actor-intent systems are authorized.
- Behavior tree — blocked until NPC AI and behavior evaluation authorization.
- DialogueActIR implementation — blocked until dialogue-act schema, parser, and social consequence routing are authorized.
- Dialogue system — blocked until DialogueActIR and social mechanics authorization.
- Content ecology engine — blocked until content tracking, contradiction detection, and ecology management systems are authorized.
- Playable-content validator — blocked until playability proof schema and validation engine are authorized.
- Generator implementation — blocked until generator framework, repair loop, and evaluator systems are authorized.
- Repair loop — blocked until generator implementation and repair routing are authorized.
- Evaluator/judge implementation — blocked until evaluator framework, scoring rubrics, and acceptance criteria are authorized.
- Runtime code — blocked until minimum backend kernel implementation is authorized per PR-A.
- Schemas — blocked until schema implementation is authorized.
- State store — blocked until state store implementation is authorized per PR-C.
- Event ledger — blocked until event ledger implementation is authorized per PR-C.
- Command IR — blocked until command IR implementation is authorized per PR-A.
- Context-packet compiler — blocked until context-packet compiler implementation is authorized per PR-B.
- Prompt templates — blocked until prompt template authoring is authorized.
- Live-play adapter — blocked until live-play adapter implementation is authorized.
- Training — blocked until training data creation and model training are authorized.
- Pilot conversion — blocked until pilot conversion authorization is granted.
- Sourcebook inclusion — blocked until sourcebook inclusion authorization is granted.
- Canon promotion — blocked until canon promotion authorization is granted.

---

## 21. Next recommended planning PR

### RUNTIME-SEQ-PR-E: Model Evaluation, Structured-Output, and Adversarial-Command Plan

PR-E should handle:

- Model behavior fingerprinting.
- Role qualification.
- Schema-key behavior evaluation.
- Truncation-safe structured output.
- Adversarial player-command corpus.
- Metamorphic runtime/narration tests.
- Local/cloud model comparison.
- Failure-mode routing.
- Model-role eligibility for:
  - Local 8B narrator.
  - Local 8B intent parser.
  - API summarizer.
  - Evaluator/judge.
  - Canon/sourcebook drafter.

PR-D does **not** authorize PR-E and does **not** implement it.

PR-E is the next recommended planning step in the RUNTIME-SEQ sequence, pending review of PR-D.

---

## 22. Non-implementation reaffirmation

This PR adds no:

- runtime code;
- storylet system;
- narrative substrate schema;
- playable-content validator;
- quest engine;
- scenario engine;
- dependency DAG engine;
- NPC AI;
- behavior tree;
- dialogue system;
- DialogueActIR implementation;
- content ecology engine;
- generator implementation;
- repair loop;
- evaluator/judge implementation;
- schema implementation;
- command IR;
- validator implementation;
- state store;
- event ledger;
- context-packet compiler;
- prompt template;
- live-play adapter;
- training data;
- donor-content audit;
- pilot conversion authorization;
- sourcebook inclusion authorization;
- canon promotion.

All content in this document is planning-level contract definition. Implementation requires separate, explicitly authorized PRs.

---

## 23. Classification block

```yaml
runtime_seq_pr_d:
  review_id: RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001
  artifact_type: story_capable_structure_playable_content_plan
  implementation_status: non_executable_planning
  derives_from:
    - RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001
    - RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001
    - RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001
    - RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001
  primary_owner_tracks:
    - RT-006
    - RT-007
    - RT-008
    - RT-011
    - RT-012
  supporting_owner_tracks:
    - RT-001
    - RT-002
    - RT-003
    - RT-004
    - RT-005
    - RT-009
    - RT-010
  defines_story_capable_structure_principle: true
  defines_playable_content_boundary: true
  defines_playability_proof_contract: true
  defines_narrative_substrate_contract: true
  defines_storylet_contract: true
  defines_quest_scenario_dependency_dag_contract: true
  defines_npc_goal_stack_contract: true
  defines_dialogue_act_ir_planning_contract: true
  defines_content_ecology_contract: true
  defines_source_local_capsule_boundary_expansion: true
  defines_generator_to_validate_to_commit_pipeline: true
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_storylet_system: false
  authorizes_narrative_substrate_schema: false
  authorizes_playable_content_validator: false
  authorizes_quest_engine: false
  authorizes_scenario_engine: false
  authorizes_dependency_dag_engine: false
  authorizes_npc_ai: false
  authorizes_behavior_tree: false
  authorizes_dialogue_system: false
  authorizes_dialogue_act_ir: false
  authorizes_content_ecology_engine: false
  authorizes_generator_implementation: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-SEQ-PR-E model evaluation structured-output and adversarial-command plan, pending review
```

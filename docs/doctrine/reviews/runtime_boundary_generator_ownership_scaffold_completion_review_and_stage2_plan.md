# Runtime Boundary + Generator Ownership Scaffold Completion Review and Stage 2 Plan

Date prepared: 2026-06-06
Status: completion review and second-stage remediation planning ledger only
Tracking ID: REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001
Inputs: AUDIT-001, AUDIT-WAVE1-001, AUDIT-WAVE2-001, REMEDIATION-PRIORITY-LEDGER-001, RT-001 through RT-012 owner scaffolds
Owner: Astra Doctrine Council / Runtime Boundary Reviewers

## 1. Purpose and scope

This artifact verifies whether the first RT-001 through RT-012 remediation owner-scaffold pass is complete, records scaffold gaps and cross-track seams, and ranks the next owner-specification planning work. It is a completion review and second-stage planning ledger only.

This file does not rewrite doctrine, implement runtime, create schemas, create command IR, create validators, create generators, create persistence writers, create retrieval indexes, create context-packet compilers, create live-play prompts, authorize training, audit donor content, or promote canon.

This review treats the owner scaffolds as planning/control evidence only. A scaffold marked complete below means the expected scaffold artifact exists and contains the baseline planning guardrails; it does not mean the associated runtime owner, schema, validator, event model, generator, context-packet compiler, persistence path, or canon/sourcebook promotion path exists.

## 2. Inputs inspected

### Core audit and remediation inputs

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.

### Owner scaffolds

- RT-001: `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md`.
- RT-002: `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md`.
- RT-003: `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md`.
- RT-004: `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_scaffold.md`.
- RT-005: `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md`.
- RT-006: `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_scaffold.md`.
- RT-007: `docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md`.
- RT-008: `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md`.
- RT-009: `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md`.
- RT-010: `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md`.
- RT-011: `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md`.
- RT-012: `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md`.

### Governance inputs

- `docs/doctrine/astra_doctrine_registry_v0_1.yaml`.
- `docs/decisions/current_decisions_log.md`.
- `docs/operations/current_decisions_log_v0_1.md`.
- `docs/doctrine/astra_doctrine_roadmap_v0_1.md`.
- `README.md` for backend-first and model-interchangeability posture.

### Missing-file disclosure

All required source files listed above were present at review time. No absent required path was discovered.

## 3. Scaffold completion matrix

| Track | Scope | scaffold_file | registry_tracking_id | present | ledger_linkage_present | audit_linkage_present | dependency_links_present | llm_non_authority_guardrails_present | explicit_non_implementation_statement_present | registry_tracking_present | decision_log_tracking_present | completion_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RT-001 | command lifecycle/action legality/cost commitment | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` | `REMEDIATION-RT001-COMMAND-LIFECYCLE-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Strong first-owner scaffold. It links the remediation ledger, accepted audits, dependencies, LLM non-authority, context/narration handoff, and non-implementation guardrails. Ready to move first into owner-spec drafting. |
| RT-002 | resource/consequence math | `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` | `REMEDIATION-RT002-RESOURCE-CONSEQUENCE-MATH-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Adequate scaffold for resource, backlash, strain, corruption, reward/loss, and consequence math boundaries. Owner spec should follow RT-001 or proceed only with strict cost-commit boundary assumptions. |
| RT-003 | combat/hazard/damage/recovery | `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md` | `REMEDIATION-RT003-COMBAT-HAZARD-DAMAGE-RECOVERY-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Adequate scaffold, but owner specification depends on RT-001 command/event sequencing, RT-002 cost/consequence math, RT-005 hidden hazard visibility, and RT-009 RNG/table boundaries. |
| RT-004 | ability/effect/skill binding | `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_scaffold.md` | `REMEDIATION-RT004-ABILITY-EFFECT-SKILL-BINDING-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Adequate scaffold. It correctly separates ability/effect/skill ownership from command legality, cost/backlash, generated ability persistence, hidden prerequisites, and validators. |
| RT-005 | context-packet/hidden-information | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md` | `REMEDIATION-RT005-CONTEXT-PACKET-HIDDEN-INFORMATION-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Adequate scaffold for visibility, redaction, scene/context packet posture, and narrator non-authority. Owner spec should follow RT-001 because available-actions and event visibility depend on command lifecycle boundaries. |
| RT-006 | mission/reward/clue/hidden-truth routing | `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_scaffold.md` | `REMEDIATION-RT006-MISSION-REWARD-CLUE-ROUTING-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Adequate scaffold. It has a broader dependency surface than an early Stage 2 owner spec can safely settle, especially RT-002 rewards/consequences, RT-005 clue visibility, RT-008 generated mission provenance, and RT-009 table/oracle outcomes. |
| RT-007 | social/faction/actor-knowledge state | `docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md` | `REMEDIATION-RT007-SOCIAL-FACTION-KNOWLEDGE-STATE-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Adequate scaffold. It should remain downstream of RT-005 knowledge partitions and RT-008 provenance/recurrence before owner-specification moves into state fields. |
| RT-008 | generated-content provenance/recurrence | `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md` | `REMEDIATION-RT008-GENERATED-CONTENT-PROVENANCE-RECURRENCE-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Adequate scaffold for provenance, recurrence, durable-record eligibility, and no-generator/no-canon guardrails. It can move relatively early after RT-001/RT-011 assumptions are stated because many later tracks depend on it. |
| RT-009 | runtime RNG/table/oracle | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md` | `REMEDIATION-RT009-RUNTIME-RNG-TABLE-ORACLE-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Adequate scaffold. Owner spec should follow RT-001 and RT-005 because RNG invocations need command/event owners and hidden-result projection boundaries. |
| RT-010 | inventory/item/vehicle/persistent asset state | `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md` | `REMEDIATION-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Adequate scaffold, intentionally dependency-heavy. It should not be the first Stage 2 owner spec because it consumes RT-001, RT-002, RT-003, RT-004, RT-005, RT-008, RT-009, and RT-011 boundaries. |
| RT-011 | validation/readiness tooling | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` | `REMEDIATION-RT011-VALIDATION-READINESS-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | needs_minor_cleanup | Functionally complete for scaffold purposes and registry/decision tracked. Minor cleanup: its direct audit-source section names AUDIT-001 and SM00/SM01/SM02, while Wave 1/Wave 2 linkage is mostly inherited through the ledger rather than explicitly listed like other scaffolds. Do not repair that in this PR. |
| RT-012 | D-series/native-design promotion boundaries | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md` | `REMEDIATION-RT012-D-SERIES-PROMOTION-BOUNDARY-OWNER-SCAFFOLD-001` | true | true | true | true | true | true | true | true | complete | Adequate promotion-boundary scaffold. It should stay in planning until canon/sourcebook/native-design promotion work resumes and RT-011 promotion validators have owner specifications. |

## 4. Cross-track dependency matrix

| Track | Feeds / depends on | Dependency summary |
|---|---|---|
| RT-001 | Feeds RT-002, RT-003, RT-004, RT-005, RT-006, RT-007, RT-008, RT-009, RT-010, RT-011, and RT-012 as applicable | RT-001 feeds nearly all command/event/action-facing tracks. It must define player intent intake, action legality, cost commitment timing, rollback/cancel/interrupt posture, state-delta validation handoff, event commitment, context-packet handoff, and narration downstream-of-backend boundaries before subsystem owner specs can safely consume command authority. |
| RT-002 | Feeds RT-001, RT-003, RT-004, RT-006, RT-008, RT-010, and RT-011 | RT-002 feeds costs, resources, consequences, rewards, damage/recovery cost, inventory spend, mission rewards, backlash, strain, corruption, recovery events, and reward/loss events. It depends on RT-001 for when costs become committed and on RT-011 for future validation/readiness movement. |
| RT-003 | Feeds RT-004, RT-005, RT-006, RT-009, RT-010, and RT-011 | RT-003 feeds combat, hazards, item/vehicle damage, recovery, active-threat pressure, exposure intervals, injury/condition clocks, and mitigation/recovery state. It depends on RT-001 for command/event flow, RT-002 for cost/consequence math, RT-005 for hidden hazard visibility, and RT-009 for random hazard/combat table outcomes. |
| RT-004 | Feeds RT-001, RT-002, RT-003, RT-005, RT-008, RT-010, and RT-011 | RT-004 feeds abilities, item effects, skill/advancement bindings, prerequisites, effect taxonomy, cooldown/cost boundaries, generated ability review, and capability persistence. It depends on RT-001 command binding, RT-002 cost/backlash, RT-005 hidden prerequisites/narration, RT-008 generated capability provenance, and RT-011 validation readiness. |
| RT-005 | Feeds RT-006, RT-007, RT-008, RT-009, RT-010, RT-011, and RT-012 | RT-005 feeds hidden information, context packets, narration visibility, social/faction knowledge, mission clues, table redaction, secret item/vehicle properties, generated content projection, and D-series draft-material visibility. It depends on RT-001 for event/action visibility and on RT-011 for future validation gates. |
| RT-006 | Feeds RT-002, RT-003, RT-005, RT-007, RT-008, RT-009, RT-010, and RT-011 | RT-006 feeds mission/reward/clue routing and depends on RT-009 where tables/oracles matter. It also depends on RT-002 for reward/consequence commits, RT-005 for clue/hidden-truth exposure, RT-008 for generated mission provenance, and RT-001 for command/event boundaries. |
| RT-007 | Feeds RT-005, RT-006, RT-008, RT-010, and RT-011 | RT-007 feeds faction/social/actor-knowledge and depends on RT-005/RT-008. It requires actor knowledge partitions, relationship/faction state, social consequence events, generated NPC/faction provenance, and context-packet projection boundaries before implementation. |
| RT-008 | Feeds RT-004, RT-006, RT-007, RT-009, RT-010, RT-011, and RT-012 | RT-008 feeds generated-content durability, provenance, recurrence, generated assets/factions/missions/items, source-local status, default non-canon posture, durable IDs, and generator-disablement guardrails. It depends on RT-011 for future validators and on promotion gates for canon/sourcebook claims. |
| RT-009 | Feeds RT-002, RT-003, RT-006, RT-008, RT-010, and RT-011 | RT-009 feeds deterministic randomness, table/oracle outcomes, loot/generation/hazard/mission randomization, replay references, seed handling, table validation, and hidden-result redaction. It depends on RT-001 command/event invocation rules and RT-005 hidden-result context projection. |
| RT-010 | Consumes RT-001, RT-002, RT-003, RT-004, RT-005, RT-008, RT-009, and RT-011 | RT-010 feeds inventory/item/vehicle/asset state and depends on RT-001/RT-002/RT-003/RT-004/RT-005/RT-008/RT-009/RT-011. It is a downstream convergence track for custody, loadout, item effects, charges, durability, cargo, vehicle damage, repair, generated items/vehicles, and hidden asset properties. |
| RT-011 | Gates all tracks | RT-011 gates readiness and validation movement from prose to executable controls. It should become an early owner specification for validation requirements and reviewer decision records, but not validator implementation. |
| RT-012 | Gates D-series/native-design promotion and pressures RT-001, RT-002, RT-003, RT-005, RT-008, and RT-011 | RT-012 gates D-series/native-design promotion. Draft source-pack material may exert design pressure only; it must not become runtime authority, generator input, sourcebook text, training material, or canon without explicit promotion workflow, registry tracking, reviewer decisions, and future validation controls. |

## 5. Gap and overlap review

### Missing scaffold links

- No owner scaffold file is missing for RT-001 through RT-012.
- No required audit/remediation/governance input listed in this review was absent.
- Minor cleanup only: RT-011's direct audit-source section does not explicitly list AUDIT-WAVE1-001 and AUDIT-WAVE2-001 in the same form as most other scaffolds. It links AUDIT-001 plus SM00/SM01/SM02 and inherits Wave 1/Wave 2 pressure through `REMEDIATION-PRIORITY-LEDGER-001`. This should be recorded as cleanup debt, not repaired here.

### Weak guardrails

- The global scaffold pass is strong on LLM non-authority and non-implementation language.
- The weakest guardrail is not in a single scaffold but in the transition risk: future owner-spec PRs could accidentally drift from `owner_specification` into schema, validator, command IR, generator, context-packet compiler, or runtime implementation. Stage 2 PRs therefore need explicit forbidden-output blocks and acceptance tests that prove the artifact is still planning/specification only.
- RT-011 is especially sensitive because validator-language can sound executable. Its next owner-spec must define validation requirements, coverage families, failure taxonomy, and reviewer decision records without creating validators.

### Naming drift

- RT-005 is named in the remediation ledger as `RT-005-scene-activity-context-packets`, while the scaffold file emphasizes `context-packet/hidden-information`. This is acceptable if the owner specification explicitly states that scene/activity orchestration is represented only through context-packet, visibility, participant, redaction, and narration-boundary planning until a separately authorized scene runtime owner exists.
- RT-008 appears as generated-content provenance/recurrence in the scaffold and generated-content provenance in some dependency lists. Treat recurrence, durable-record eligibility, source-local status, and provenance as one owner boundary until owner-spec drafting decides field inventory names.
- RT-010 is alternately phrased as inventory/item/vehicle assets, persistent asset state, and inventory/item/vehicle/asset state. The owner spec should normalize this as inventory, item, gear, vehicle, platform, installable, and persistent asset state without expanding into runtime implementation.
- RT-011's tracking ID omits the word `TOOLING` (`REMEDIATION-RT011-VALIDATION-READINESS-OWNER-SCAFFOLD-001`) while the track name includes validation/readiness tooling. This is not blocking, but later owner-spec identifiers should choose one stable naming pattern.

### Duplicated responsibilities that should remain separate

- RT-001 cost commitment timing and RT-002 resource/consequence math overlap but should remain separate. RT-001 owns when a cost is committed in the command lifecycle; RT-002 owns how costs, resources, backlash, corruption, strain, rewards, losses, and consequences are calculated and represented.
- RT-003 damage/recovery and RT-002 consequence/resource math overlap but should remain separate. RT-003 owns combat/hazard harm states and recovery seams; RT-002 owns general resource and consequence math.
- RT-004 ability/effect resolution and RT-010 item/vehicle effects overlap but should remain separate. RT-004 owns capability/effect taxonomy and skill/advancement binding; RT-010 owns persistent item/vehicle instances, custody, durability, charges, cargo, and platform state.
- RT-005 hidden information and RT-007 actor knowledge overlap but should remain separate. RT-005 owns projection/redaction/context-packet boundaries; RT-007 owns relationship, faction, institutional, contact, and actor-knowledge state.
- RT-006 mission clues and RT-005 hidden information overlap but should remain separate. RT-006 owns mission/clue/reward/branch routing; RT-005 owns what is visible, hidden, redacted, or narratable.
- RT-008 generated-content recurrence and RT-012 promotion boundaries overlap but should remain separate. RT-008 owns generated record provenance and persistence eligibility; RT-012 owns whether D-series/native-design source material may be promoted to doctrine/sourcebook/runtime/canon/training authority.
- RT-009 table/oracle outcomes and RT-006 mission randomization overlap but should remain separate. RT-009 owns deterministic random authority and invocation events; RT-006 owns mission routing that consumes approved outcomes.
- RT-011 validation/readiness touches every track but should not own the substantive domain rules. It owns validation requirements, readiness labels, coverage expectations, failure/blocker taxonomy, and reviewer decision record boundaries.

### Seams needing owner-spec clarification before implementation

- Command lifecycle event vocabulary: RT-001 must define owner-spec-level lifecycle states and handoff seams before any track can claim action/event authority.
- Cost commitment versus cost math: RT-001/RT-002 must clarify when an attempted action reserves, spends, refunds, rolls back, or converts costs into consequences.
- Context packet event visibility: RT-001/RT-005 must clarify which command/event facts are visible, hidden, redacted, or narratable.
- RNG invocation ownership: RT-001/RT-005/RT-009 must clarify when an RNG/table/oracle invocation is legal, when its result is committed, and how hidden results are projected.
- Generated record recurrence: RT-008 must clarify source-local/generated/non-canon/durable distinctions before RT-004, RT-006, RT-007, or RT-010 consume generated abilities, missions, factions, NPCs, items, vehicles, hazards, or tables.
- Validation readiness language: RT-011 must distinguish owner specification requirements from executable validators.
- D-series/native-design promotion: RT-012 must remain isolated from runtime and canon until sourcebook/canon work resumes under explicit promotion controls.

### Tracks that should not be moved forward yet

- RT-010 should not move to owner specification before RT-001, RT-002, RT-003, RT-004, RT-005, RT-008, RT-009, and RT-011 have clearer owner specs or explicit assumptions.
- RT-006 and RT-007 should not move before RT-005 and RT-008 are specified enough to protect hidden clues, actor knowledge, generated missions, generated factions, and social-state recurrence.
- RT-003 should not move before at least RT-001 and RT-002 have owner-spec-level command/cost/consequence boundaries.
- RT-004 should not move before RT-001 and RT-002 are specified enough to prevent abilities/effects from smuggling in command legality or final cost math.
- RT-012 should not move beyond promotion-boundary planning until canon/sourcebook/native-design promotion work resumes and validation/readiness owner specs exist.

### Tracks ready for owner-specification drafting

- RT-001 is ready for first owner specification.
- RT-011 is ready for early owner specification, but only for validation/readiness requirements, field inventory, dependency matrix, failure taxonomy, reviewer decision records, and test plan; it must not implement validators.
- RT-002 is ready after RT-001 owner specification or in tightly scoped parallel drafting that treats RT-001 command/cost-commitment assumptions as explicit dependencies.
- RT-005 is ready after RT-001 owner specification because context packets depend on command/event visibility.
- RT-008 is ready relatively early as a provenance/recurrence owner specification, especially because many downstream generated-content tracks consume it.
- RT-009 is ready after RT-001 and RT-005 boundaries are clear.

## 6. Stage 2 readiness classifications

| Track | Classification | Rationale |
|---|---|---|
| RT-001 | ready_for_owner_spec | Complete scaffold, central dependency, and safest first owner-spec because it can define non-executable command lifecycle fields, handoffs, forbidden outputs, and acceptance tests without implementing runtime. |
| RT-002 | blocked_pending_dependency | Complete scaffold, but the owner spec should follow RT-001's command lifecycle/cost-commitment owner spec or proceed only with explicit RT-001 assumptions. |
| RT-003 | blocked_pending_dependency | Complete scaffold, but combat/hazard/damage/recovery owner spec depends on RT-001 command/event sequencing, RT-002 cost/consequence math, RT-005 hidden hazard visibility, and RT-009 RNG boundaries. |
| RT-004 | blocked_pending_dependency | Complete scaffold, but ability/effect/skill binding depends on RT-001 action binding, RT-002 costs/cooldowns/backlash, RT-005 hidden prerequisites/narration, RT-008 generated ability provenance, and RT-011 readiness requirements. |
| RT-005 | blocked_pending_dependency | Complete scaffold and high-value early Stage 2 candidate, but context-packet visibility depends on RT-001 command/event lifecycle before it can be safely specified. |
| RT-006 | blocked_pending_dependency | Complete scaffold, but mission/reward/clue routing depends on RT-002, RT-005, RT-008, RT-009, and RT-001 before field inventory or validation requirements can be stable. |
| RT-007 | blocked_pending_dependency | Complete scaffold, but social/faction/actor-knowledge specification depends on RT-005 knowledge partitions and RT-008 generated NPC/faction recurrence. |
| RT-008 | ready_for_owner_spec | Complete scaffold and useful early owner-spec candidate because generated-content provenance, recurrence, durable-record eligibility, and no-canon/no-generator guardrails support many later tracks. It should remain non-implementation. |
| RT-009 | blocked_pending_dependency | Complete scaffold, but runtime RNG/table/oracle owner spec should wait for RT-001 invocation/event boundaries and RT-005 hidden-result projection. |
| RT-010 | blocked_pending_dependency | Complete scaffold, intentionally downstream and dependency-heavy. It should wait until the command, cost, damage, ability/effect, hidden-information, provenance, RNG, and validation owner specs are clearer. |
| RT-011 | ready_for_owner_spec | Complete enough for early owner-specification of validation/readiness requirements and reviewer decision records, but it must not become validator implementation. Minor cleanup debt should be included in its owner-spec scope if selected later. |
| RT-012 | defer_until_canon_or_sourcebook_phase | Complete scaffold, but Stage 2 should keep it as promotion-boundary planning until canon/sourcebook/native-design promotion work resumes and RT-011 validation/readiness owner specs exist. |

## 7. Second-stage remediation planning ledger

```yaml
- stage2_pr_id: STAGE2-PR-A
  priority: P0
  title: RT-001 command lifecycle/action legality owner specification
  tracks_covered:
    - RT-001
  purpose: Define the non-executable owner specification for command intake, legality, cost-commit timing, rollback/cancel/interrupt posture, resolution trigger handoff, state-delta validation handoff, event commitment handoff, context-packet handoff, and narration downstream-of-backend boundaries.
  why_now: RT-001 feeds nearly every other command/event/action-facing track and is the cleanest next step after scaffold completion.
  required_inputs:
    - docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md
    - docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md
    - docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md
    - docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md
    - docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md
    - docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md
    - README.md
  allowed_outputs:
    - owner_specification
    - dependency_matrix
    - field_inventory
    - validation_requirements
    - test_plan
    - non_implementation_guardrails
  forbidden_outputs:
    - runtime_code
    - schemas
    - command_ir_implementation
    - validator_implementation
    - generator_implementation
    - persistence_writer
    - retrieval_index
    - context_packet_compiler
    - live_play_prompt
    - training_data
    - canon_promotion
  dependencies:
    - REMEDIATION-PRIORITY-LEDGER-001
    - RT-011
  acceptance_tests_needed:
    - Owner specification exists and states it is non-executable planning only.
    - Specification defines command lifecycle field inventory without creating command IR.
    - Specification preserves LLM non-authority over legality, cost commitment, RNG, hidden modifiers, consequences, state deltas, persistence, and canon.
    - Specification names downstream dependencies for RT-002, RT-005, RT-009, RT-010, and RT-011.
  notes: This is the recommended next PR. It should not bundle RT-002 or RT-011 implementation.

- stage2_pr_id: STAGE2-PR-B
  priority: P0
  title: RT-011 validation/readiness owner specification and RT-011 cleanup note capture
  tracks_covered:
    - RT-011
  purpose: Define validation/readiness owner-spec requirements, coverage families, readiness labels, failure/blocker taxonomy, reviewer decision record fields, and tests proving prose controls are not executable validators.
  why_now: RT-011 gates all movement from prose planning to executable controls and prevents later owner specs from being mistaken for validators.
  required_inputs:
    - docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md
    - docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md
    - docs/doctrine/astra_doctrine_registry_v0_1.yaml
    - docs/decisions/current_decisions_log.md
    - docs/operations/current_decisions_log_v0_1.md
  allowed_outputs:
    - owner_specification
    - dependency_matrix
    - field_inventory
    - validation_requirements
    - test_plan
    - non_implementation_guardrails
  forbidden_outputs:
    - runtime_code
    - schemas
    - command_ir_implementation
    - validator_implementation
    - generator_implementation
    - persistence_writer
    - retrieval_index
    - context_packet_compiler
    - live_play_prompt
    - training_data
    - canon_promotion
  dependencies:
    - STAGE2-PR-A
  acceptance_tests_needed:
    - Specification distinguishes validation requirements from validator implementation.
    - Specification records reviewer decision fields without creating approval automation.
    - Specification captures the RT-011 minor audit-linkage cleanup debt without rewriting unrelated scaffolds.
  notes: Early but not first. It should remain planning/specification only.

- stage2_pr_id: STAGE2-PR-C
  priority: P1
  title: RT-002 resource/consequence math owner specification
  tracks_covered:
    - RT-002
  purpose: Define non-executable field inventory and owner boundaries for resource pools, costs, backlash, corruption, strain, overcommitment, rewards, losses, recovery costs, and consequence events.
  why_now: Costs and consequences are consumed by abilities, combat, hazards, missions, inventory, and command lifecycle resolution.
  required_inputs:
    - RT-001
    - docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md
    - docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md
  allowed_outputs:
    - owner_specification
    - dependency_matrix
    - field_inventory
    - validation_requirements
    - test_plan
    - non_implementation_guardrails
  forbidden_outputs:
    - runtime_code
    - schemas
    - command_ir_implementation
    - validator_implementation
    - generator_implementation
    - persistence_writer
    - retrieval_index
    - context_packet_compiler
    - live_play_prompt
    - training_data
    - canon_promotion
  dependencies:
    - STAGE2-PR-A
  acceptance_tests_needed:
    - Specification separates cost commitment timing from resource/consequence math.
    - Specification contains no final numeric formulas.
    - Specification records downstream consumers RT-003, RT-004, RT-006, RT-010, and RT-011.
  notes: May be drafted after STAGE2-PR-A; parallel drafting is only safe if RT-001 assumptions are explicit.

- stage2_pr_id: STAGE2-PR-D
  priority: P1
  title: RT-005 context-packet and hidden-information owner specification
  tracks_covered:
    - RT-005
  purpose: Define non-executable owner specification for visible, hidden, redacted, derived, narrator-facing, and reviewer-only information partitions plus context-packet handoff requirements.
  why_now: Hidden information and context projection are prerequisites for missions, social/faction state, hazards, table/oracle hidden results, generated content projection, and item/vehicle secrets.
  required_inputs:
    - RT-001
    - docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md
    - docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md
  allowed_outputs:
    - owner_specification
    - dependency_matrix
    - field_inventory
    - validation_requirements
    - test_plan
    - non_implementation_guardrails
  forbidden_outputs:
    - runtime_code
    - schemas
    - command_ir_implementation
    - validator_implementation
    - generator_implementation
    - persistence_writer
    - retrieval_index
    - context_packet_compiler
    - live_play_prompt
    - training_data
    - canon_promotion
  dependencies:
    - STAGE2-PR-A
  acceptance_tests_needed:
    - Specification proves no context-packet compiler is created.
    - Specification states the LLM cannot hold hidden truth, reveal clues, or mutate scene state.
    - Specification records dependencies for RT-006, RT-007, RT-009, RT-010, and RT-012.
  notes: Should follow RT-001 because context-packet visibility depends on command/event lifecycle.

- stage2_pr_id: STAGE2-PR-E
  priority: P1
  title: RT-008 generated-content provenance/recurrence owner specification
  tracks_covered:
    - RT-008
  purpose: Define non-executable owner specification for generated-content provenance, source-local status, recurrence, durable-record eligibility, stable identifiers, generator-disablement posture, and no-canon promotion guardrails.
  why_now: Generated NPCs, factions, missions, items, vehicles, hazards, tables, abilities, and locations need provenance before later owner specs can safely consume them.
  required_inputs:
    - docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md
    - docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md
    - docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md
  allowed_outputs:
    - owner_specification
    - dependency_matrix
    - field_inventory
    - validation_requirements
    - test_plan
    - non_implementation_guardrails
  forbidden_outputs:
    - runtime_code
    - schemas
    - command_ir_implementation
    - validator_implementation
    - generator_implementation
    - persistence_writer
    - retrieval_index
    - context_packet_compiler
    - live_play_prompt
    - training_data
    - canon_promotion
  dependencies:
    - STAGE2-PR-A
    - RT-011
  acceptance_tests_needed:
    - Specification does not create generator code or durable generated records.
    - Specification distinguishes generated, source-local, persistent, recurrent, sourcebook, and canon states.
    - Specification records downstream consumers RT-004, RT-006, RT-007, RT-009, RT-010, and RT-012.
  notes: Can move early after command and validation assumptions are named.

- stage2_pr_id: STAGE2-PR-F
  priority: P2
  title: RT-009 RNG/table/oracle owner specification
  tracks_covered:
    - RT-009
  purpose: Define non-executable owner specification for backend-owned random authority, table/oracle invocation records, seed/replay references, result-domain validation requirements, hidden-result redaction, and narration projection.
  why_now: Random outcomes affect hazards, missions, rewards, loot, generation, active threats, and hidden oracle results, but must wait for command/event and context-packet boundaries.
  required_inputs:
    - RT-001
    - RT-005
    - docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md
  allowed_outputs:
    - owner_specification
    - dependency_matrix
    - field_inventory
    - validation_requirements
    - test_plan
    - non_implementation_guardrails
  forbidden_outputs:
    - runtime_code
    - schemas
    - command_ir_implementation
    - validator_implementation
    - generator_implementation
    - persistence_writer
    - retrieval_index
    - context_packet_compiler
    - live_play_prompt
    - training_data
    - canon_promotion
  dependencies:
    - STAGE2-PR-A
    - STAGE2-PR-D
  acceptance_tests_needed:
    - Specification states the LLM cannot roll, select, weight, reroll, suppress, or reveal table/oracle outcomes as authority.
    - Specification defines planning fields without implementing RNG.
    - Specification records hidden-result routing through RT-005.
  notes: Should not be combined with mission/reward/clue implementation.

- stage2_pr_id: STAGE2-PR-G
  priority: P2
  title: Downstream domain owner-spec bundle for RT-003, RT-004, RT-006, and RT-007
  tracks_covered:
    - RT-003
    - RT-004
    - RT-006
    - RT-007
  purpose: Draft bounded owner specifications for combat/hazard/damage/recovery, ability/effect/skill binding, mission/reward/clue routing, and social/faction/actor-knowledge state only after their upstream command, cost, context, provenance, RNG, and validation assumptions are available.
  why_now: These tracks are high-value but have interlocking dependencies that should be stabilized by earlier Stage 2 PRs before detailed owner-spec fields are named.
  required_inputs:
    - RT-001
    - RT-002
    - RT-005
    - RT-008
    - RT-009
    - RT-011
    - docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md
    - docs/doctrine/control/RT004_ability_effect_skill_binding_owner_scaffold.md
    - docs/doctrine/control/RT006_mission_reward_clue_routing_owner_scaffold.md
    - docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md
  allowed_outputs:
    - owner_specification
    - dependency_matrix
    - field_inventory
    - validation_requirements
    - test_plan
    - non_implementation_guardrails
  forbidden_outputs:
    - runtime_code
    - schemas
    - command_ir_implementation
    - validator_implementation
    - generator_implementation
    - persistence_writer
    - retrieval_index
    - context_packet_compiler
    - live_play_prompt
    - training_data
    - canon_promotion
  dependencies:
    - STAGE2-PR-A
    - STAGE2-PR-C
    - STAGE2-PR-D
    - STAGE2-PR-E
    - STAGE2-PR-F
  acceptance_tests_needed:
    - Each track records upstream dependencies and forbidden outputs.
    - Specifications do not choose final formulas, award abilities, reveal clues, mutate relationships, generate missions, or commit hazard/combat outcomes.
    - Cross-track seams remain explicit rather than collapsed into a single runtime owner.
  notes: This may need to split into multiple PRs if field inventories become large. Do not start it before the earlier owner specs exist.

- stage2_pr_id: STAGE2-PR-H
  priority: P3
  title: RT-010 and RT-012 deferred convergence planning
  tracks_covered:
    - RT-010
    - RT-012
  purpose: Revisit persistent assets and D-series/native-design promotion only after upstream owner specifications exist and canon/sourcebook/native-design promotion work is active.
  why_now: Not now. This ledger records the eventual slot so downstream work does not pull RT-010 or RT-012 forward prematurely.
  required_inputs:
    - RT-001
    - RT-002
    - RT-003
    - RT-004
    - RT-005
    - RT-008
    - RT-009
    - RT-011
    - docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md
    - docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md
  allowed_outputs:
    - owner_specification
    - dependency_matrix
    - field_inventory
    - validation_requirements
    - test_plan
    - non_implementation_guardrails
  forbidden_outputs:
    - runtime_code
    - schemas
    - command_ir_implementation
    - validator_implementation
    - generator_implementation
    - persistence_writer
    - retrieval_index
    - context_packet_compiler
    - live_play_prompt
    - training_data
    - canon_promotion
  dependencies:
    - STAGE2-PR-A
    - STAGE2-PR-B
    - STAGE2-PR-C
    - STAGE2-PR-D
    - STAGE2-PR-E
    - STAGE2-PR-F
    - STAGE2-PR-G
    - canon/sourcebook/native-design promotion workstream reactivation for RT-012
  acceptance_tests_needed:
    - Persistent asset planning does not create item instances, vehicle state, custody mutation, or item effects.
    - D-series planning does not promote source-pack material to doctrine, sourcebook, runtime, live-play, training, or canon.
    - Both tracks retain explicit dependency declarations.
  notes: RT-010 is downstream convergence; RT-012 is phase-gated by canon/sourcebook/native-design promotion work.
```

## 8. Exactly one recommended next PR

Recommended next PR: **STAGE2-PR-A — RT-001 command lifecycle/action legality owner specification**.

Reason: RT-001 is the highest-leverage dependency because it defines the command lifecycle, legality, cost-commitment timing, resolution trigger handoff, state-delta validation handoff, event commitment handoff, context-packet handoff, and narration downstream-of-backend boundary that nearly all later owner specifications must consume.

The next PR must be limited to owner-specification planning and must not bundle RT-002 formulas, RT-011 validators, command IR implementation, runtime code, schemas, generators, persistence, retrieval, context-packet compilation, live-play prompts, training data, donor-content audit, canon promotion, or D-series/native-design promotion.

## 9. Non-implementation reaffirmation

This completion review and Stage 2 plan is documentation/control planning only. It creates no runtime authority and no executable control. It marks the first owner-scaffold pass complete with minor cleanup debt for RT-011 direct Wave linkage phrasing, ranks second-stage planning, and recommends exactly one next PR: STAGE2-PR-A for RT-001 owner specification.

Guardrails reaffirmed: no doctrine rewrite; no runtime implementation; no schema implementation; no command IR implementation; no validator implementation; no generator implementation; no persistence writer implementation; no retrieval index implementation; no context-packet compiler implementation; no live-play prompt implementation; no training authorization; no donor-content audit; and no canon promotion.

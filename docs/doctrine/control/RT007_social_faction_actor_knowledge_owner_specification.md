# RT-007 Social / Faction / Actor-Knowledge Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification; non-executable planning artifact only
Tracking ID: REMEDIATION-STAGE2-RT007-SOCIAL-FACTION-ACTOR-KNOWLEDGE-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-G4
Parent Stage 2 PR ID: STAGE2-PR-G
Track: RT-007
Owner: Astra Doctrine Council / future social, faction, actor-knowledge, relationship, reputation, standing, contact, institution, obligation, debt, favor, influence, deception, rumor, false-claim, witness, and knowledge-state routing boundary owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-007 social/faction/actor-knowledge ownership. It upgrades the RT-007 owner scaffold into a specification-level planning artifact, but it remains non-executable and non-implementation. It does not implement social systems, faction systems, reputation systems, relationship engines, actor-knowledge databases, social memory systems, dialogue systems, influence rules, deception rules, obligation/debt economies, faction clocks, institutional clocks, contact systems, rumor systems, belief-state engines, witness systems, schemas, validators, command IR, runtime code, generators, RNG/table logic, event ledgers, persistence writers, retrieval indexes, context-packet compilers, live-play prompts, training data, donor-content audits, sourcebook inclusion authorization, pilot conversion authorization, or canon promotion.

This owner specification is split from the original STAGE2-PR-G downstream-domain bundle for review safety. STAGE2-PR-G1 handled RT-003, STAGE2-PR-G2 handled RT-004, STAGE2-PR-G3 handled RT-006, and this STAGE2-PR-G4 artifact handles only RT-007.

Required authority and planning links:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.
- RT007 owner scaffold: `docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md`.
- RT001 owner specification: `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`.
- RT002 owner specification: `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`.
- RT003 owner specification: `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md`.
- RT004 owner specification: `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md`.
- RT005 owner specification: `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md`.
- RT006 owner specification: `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md`.
- RT008 owner specification: `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md`.
- RT009 owner specification: `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md`.
- RT011 owner specification: `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`.

## 2. Source availability disclosure

The Stage 2 RT-007 drafting pass inspected actual repository paths and used only existing files. Planning and audit sources inspected were `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`, `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`, `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, and `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.

Current RT owner files inspected were the RT-007 owner scaffold; the RT-001, RT-002, RT-003, RT-004, RT-005, RT-006, RT-008, RT-009, and RT-011 owner specifications; and the RT-010 and RT-012 owner scaffolds listed in Section 1 and Section 12.

Social/faction/knowledge/source pressure files confirmed present and inspected include `docs/doctrine/schema/C01_creature_npc_record_schema.md`, `docs/doctrine/schema/C05_faction_institution_record_schema.md`, `docs/doctrine/schema/C06_location_site_region_record_schema.md`, `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`, `docs/doctrine/schema/C10_table_oracle_record_schema.md`, `docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md`, `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md`, `docs/doctrine/operations/batch_b/B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md`, `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md`, `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md`, and `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md`.

The requested optional paths `docs/doctrine/operations/batch_b/B07_mission_objective_reward_and_failure_routing_procedure.md` and `docs/doctrine/operations/batch_b/B08_clue_revelation_information_routing_and_investigation_procedure.md` were absent. The nearest actual equivalents confirmed present are `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md`, `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`, and `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md`; this artifact does not rewrite those sources.

Runtime/project authority sources inspected include `docs/doctrine/astra_doctrine_roadmap_v0_1.md`, `docs/doctrine/astra_doctrine_registry_v0_1.yaml`, `docs/decisions/current_decisions_log.md`, and `README.md` for backend-first and model-interchangeability posture.

## 3. Scope: what RT-007 owns

RT-007 owns Stage 2 planning boundaries for social/faction/actor-knowledge ownership only. In this specification, ownership means semantic requirement ownership, handoff definition, non-authority guardrails, and auditability expectations; it does not mean implementation.

RT-007 owns:

- social/faction/actor-knowledge ownership boundaries;
- actor knowledge, belief, rumor, false claim, verified fact, witness state, and institutional knowledge routing requirement boundaries;
- faction standing, reputation, relationship, influence, contact, patron, rival, institution, debt, obligation, favor, oath, threat, blackmail, and leverage requirement boundaries;
- social consequence, faction response, institutional response, witness response, relationship shift, contact availability, and reputation pressure boundaries;
- social-to-command handoff requirements through RT-001;
- obligation/debt/reputation/cost/consequence handoff requirements through RT-002;
- combat/hazard/social fallout handoff requirements through RT-003;
- social ability/effect/skill handoff requirements through RT-004;
- hidden knowledge, false claims, rumors, actor-known facts, faction-known facts, redacted motives, secret agendas, and narrator visibility handoff through RT-005;
- mission/contact/faction consequence handoff through RT-006;
- generated faction/NPC/contact/institution/provenance handoff through RT-008;
- random social/faction/reputation/contact/oracle dependency handoff through RT-009;
- item/asset/custody/bribe/requisition/blackmail-material handoff through RT-010;
- validation/readiness handoff through RT-011;
- D-series/native-design pressure handoff through RT-012;
- auditability requirements for future social/faction/actor-knowledge artifacts.

## 4. Must-not-own boundaries

RT-007 must not own or claim to complete:

- final social system;
- final faction system;
- final reputation system;
- final relationship engine;
- final influence system;
- final contact system;
- final dialogue system;
- final actor-knowledge database;
- final faction-knowledge database;
- final rumor system;
- final belief-state engine;
- final deception rules;
- final witness system;
- final obligation/debt economy;
- final favor economy;
- final faction clocks;
- final institutional clocks;
- final patron/rival system;
- final social schema;
- final faction state schema;
- final actor-knowledge schema;
- final reputation schema;
- final relationship schema;
- final contact schema;
- schema implementation;
- command IR implementation;
- runtime code;
- validator implementation;
- generator implementation;
- RNG/dice/table implementation;
- event ledger implementation;
- persistence writer implementation;
- retrieval index implementation;
- context-packet compiler implementation;
- live-play prompt implementation;
- training data;
- donor-content audits;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion.

## 5. Authority model

The RT-007 authority model is deliberately subordinate to the runtime-boundary audit posture and adjacent owner tracks:

- RT-001 owns command/action timing, legality, social action declaration, rejection/quarantine, resolution-trigger handoff, and event-commit boundaries.
- RT-002 owns social costs, debts, obligations, favors, reputation pressure, reward/loss math, compensation, penalties, and consequence math.
- RT-003 owns combat/hazard consequences that affect social/faction/witness/institutional state.
- RT-004 owns social abilities, influence effects, faction effects, relationship effects, command effects, social skills, prerequisites, and hidden capabilities.
- RT-005 owns hidden motives, secret agendas, rumors, false claims, actor-known facts, faction-known facts, player-known facts, character-known facts, redaction, and narrator projection.
- RT-006 owns mission/contact/faction consequences, scenario consequences, clue-linked faction facts, reward/penalty routing, and mission patron/contact state.
- RT-007 owns the planning-level social/faction/actor-knowledge requirement boundary and the handoff map for relationship, reputation, standing, contact, institution, witness, rumor, false-claim, obligation, debt, favor, influence, threat, blackmail, and social-consequence pressure.
- RT-008 owns generated NPC/faction/contact/institution provenance, source-local status, durable eligibility, and recurrence.
- RT-009 owns random table/oracle dependencies for faction reactions, rumors, contacts, witness responses, institutional pressure, or social complications.
- RT-010 owns item/asset/bribe/requisition/custody/blackmail-material handoffs.
- RT-011 owns validation/readiness requirements.
- RT-012 owns D-series/native-design promotion-boundary pressure before any native social, faction, knowledge, institution, relationship, or contact pattern may become runtime, canon, sourcebook, or pilot-conversion authority.
- Future backend runtime must own social/faction/actor-knowledge state, relationship state, reputation state, belief state, event commits, and persistence if separately authorized.
- The LLM may only narrate backend-approved visible social/faction/knowledge outcomes and may not decide what actors know, change faction state, assign reputation, create durable social memory, or commit social consequences.

## 6. Social/faction/actor-knowledge routing contract

The following conceptual routing placeholders are planning terms only:

- actor_knowledge_route_required
- faction_knowledge_route_required
- verified_fact_route_required
- rumor_route_required
- false_claim_partition_required
- witness_state_pending
- relationship_state_pending
- reputation_pressure_pending
- standing_shift_pending
- influence_dependency_pending
- contact_availability_pending
- patron_rival_dependency_pending
- obligation_or_debt_dependency
- favor_or_oath_dependency
- threat_or_blackmail_dependency
- social_consequence_pending
- faction_response_pending
- institutional_response_pending
- hidden_motive_visibility_required
- secret_agenda_visibility_required
- random_social_or_faction_dependency
- generated_faction_or_contact_provenance_required
- social_state_event_pending
- social_resolution_quarantined

These routing terms are planning placeholders only. They are not final schemas, not database fields, not social rules, not faction rules, not relationship engines, not reputation systems, not actor-knowledge databases, not rumor systems, not belief engines, not clocks, not runtime state, not event records, not validators, and not live-play prompts. They identify seams for later owner work and reviewer gates only.

## 7. Actor-knowledge, rumor, and belief-state routing contract

Planning-level requirements for actor knowledge, faction knowledge, rumor, false claim, and belief-state pressure are:

- actor knowledge is not model memory;
- faction knowledge is not narration;
- dialogue transcripts are not durable truth;
- summaries are not memory authority;
- rumors, false claims, unverified claims, and verified facts must remain distinct;
- secret agendas and hidden motives require RT-005 redaction/projection authority;
- social claims created during play are claim candidates until backend/reviewer validation or future state/event/persistence systems accept them;
- witness state and who-knows-what must be backend-owned before runtime use;
- mission/clue-linked social facts route through RT-006 and RT-005;
- generated faction/contact/NPC knowledge requires RT-008 provenance;
- random rumors, contacts, or faction reactions require RT-009 authority;
- validation/readiness requires RT-011.

This section does not define final actor-knowledge schema, faction-knowledge schema, memory system, rumor schema, belief-state engine, reveal algorithm, or persistence model.

## 8. Social consequence, reputation, and faction response routing contract

Planning-level requirements for social consequence, reputation, and faction response are:

- reputation labels are not reputation mechanics;
- relationship labels are not relationship engine;
- faction standing labels are not faction state;
- obligation/debt/favor labels are not economy;
- influence labels are not influence mechanics;
- social success/failure declaration is not event commitment;
- social consequences involving costs, debts, favors, penalties, reputation, loss, compensation, or reward route through RT-002;
- social consequences involving missions, patrons, contacts, clues, rewards, or scenario state route through RT-006;
- social consequences involving combat/hazard witnesses or institutional response route through RT-003 and RT-007;
- social abilities/effects/skills route through RT-004;
- hidden social or faction consequences route through RT-005;
- generated factions, NPCs, institutions, or contacts route through RT-008;
- random faction responses, rumor spread, contact availability, or social complications route through RT-009;
- item/asset/bribe/custody/blackmail-material state routes through RT-010;
- event/state/persistence commitment requires future separately authorized backend systems.

This section does not define final reputation values, relationship rules, faction clocks, obligation/debt economy, influence rules, social tables, or persistence fields.

## 9. Social/faction commitment contract

RT-007 commitment language is constrained as follows:

- social declaration is not social resolution;
- faction interaction proposal is not faction state mutation;
- relationship proposal is not relationship state mutation;
- reputation proposal is not reputation commitment;
- rumor proposal is not verified fact;
- dialogue is not durable memory;
- social summary is not actor knowledge;
- random social/faction dependency is not random outcome selection;
- generated faction/contact proposal is not durable generated content;
- narration is not event commitment;
- rejected/quarantined social/faction/knowledge actions must not mutate state;
- event/state/persistence commitment requires future separately authorized backend systems.

This contract does not define final event schemas, runtime state machines, faction state machines, relationship state machines, actor-knowledge state machines, or executable social procedures.

## 10. Future social/faction/knowledge artifact inventory

The future artifact families below are semantic requirements only. They are not implemented schemas, not records, not validators, not services, not formulas, not generators, and not runtime code. Every listed family has `implementation status: future_required_not_implemented`.

| Artifact family | Purpose | Owner | LLM allowed interaction | Downstream handoff | Implementation status |
| --- | --- | --- | --- | --- | --- |
| ActorKnowledgeRequirement | Identify that a future backend-owned actor knowledge route is required. | RT-007 with RT-005 visibility constraints. | May narrate only backend-approved visible knowledge. | RT-005, RT-011, future backend runtime. | future_required_not_implemented |
| FactionKnowledgeRequirement | Identify that faction-known facts require a future route. | RT-007 with RT-005 and RT-006. | May not decide faction knowledge. | RT-005, RT-006, RT-011. | future_required_not_implemented |
| VerifiedFactRequirement | Preserve verified facts separately from claims and rumors. | RT-007 with RT-005. | May describe only authorized verified facts. | RT-005, RT-011, future event/state systems. | future_required_not_implemented |
| RumorRequirement | Mark rumor routing without converting rumor into truth. | RT-007 with RT-009 for random rumors. | May present authorized rumor phrasing only. | RT-005, RT-009, RT-011. | future_required_not_implemented |
| FalseClaimRequirement | Keep false claims partitioned from verified facts. | RT-007 with RT-005. | May not validate false claims as truth. | RT-005, RT-011. | future_required_not_implemented |
| WitnessStateRequirement | Require backend-owned witness and who-knows-what handling. | RT-007 with RT-003 for hazard/combat witnesses. | May not decide witness state. | RT-003, RT-005, RT-011. | future_required_not_implemented |
| RelationshipStateRequirement | Mark relationship-state pressure without implementing a relationship engine. | RT-007. | May narrate backend-approved visible attitude only. | RT-001, RT-002, RT-011. | future_required_not_implemented |
| ReputationPressureRequirement | Mark reputation pressure for future math and validation. | RT-007 with RT-002. | May not assign reputation. | RT-002, RT-011. | future_required_not_implemented |
| StandingShiftRequirement | Mark faction standing shift pressure. | RT-007 with RT-002 and RT-006. | May not assign standing. | RT-002, RT-006, RT-011. | future_required_not_implemented |
| InfluenceRequirement | Route influence dependencies without defining influence mechanics. | RT-007 with RT-004. | May not decide influence success. | RT-004, RT-001, RT-011. | future_required_not_implemented |
| ContactAvailabilityRequirement | Route contact availability and access pressure. | RT-007 with RT-006 and RT-009. | May not create durable contacts. | RT-006, RT-008, RT-009, RT-011. | future_required_not_implemented |
| PatronRivalRequirement | Identify patron/rival dependencies without creating patron/rival systems. | RT-007 with RT-006. | May not declare durable patron/rival truth. | RT-006, RT-008, RT-011. | future_required_not_implemented |
| ObligationDebtRequirement | Route obligation and debt pressure. | RT-007 with RT-002. | May not create obligations or debts as mechanical truth. | RT-002, RT-011. | future_required_not_implemented |
| FavorOathRequirement | Route favor and oath pressure. | RT-007 with RT-002 and RT-006. | May not create favors or oaths as mechanical truth. | RT-002, RT-006, RT-011. | future_required_not_implemented |
| ThreatBlackmailRequirement | Route threat, blackmail, and leverage pressure. | RT-007 with RT-005 and RT-010. | May not create blackmail material as durable truth. | RT-005, RT-010, RT-011. | future_required_not_implemented |
| SocialConsequenceRequirement | Identify social consequences needing future backend commitment. | RT-007 with RT-001 and RT-002. | May narrate only backend-approved outcomes. | RT-001, RT-002, RT-011. | future_required_not_implemented |
| FactionResponseRequirement | Route faction response pressure. | RT-007 with RT-009 when random. | May not choose faction responses. | RT-006, RT-009, RT-011. | future_required_not_implemented |
| InstitutionalResponseRequirement | Route institutional response pressure. | RT-007 with RT-003 for alarms/hazards. | May not choose institutional responses. | RT-003, RT-006, RT-011. | future_required_not_implemented |
| HiddenMotiveVisibilityRequirement | Require hidden motive visibility controls. | RT-005 primary, RT-007 consumer. | May not reveal hidden motives without projection. | RT-005, RT-011. | future_required_not_implemented |
| SecretAgendaVisibilityRequirement | Require secret agenda visibility controls. | RT-005 primary, RT-007 consumer. | May not reveal secret agendas without projection. | RT-005, RT-011. | future_required_not_implemented |
| RandomSocialFactionRequirement | Mark random social/faction dependency. | RT-009 primary, RT-007 consumer. | May not select random outcomes. | RT-009, RT-011. | future_required_not_implemented |
| GeneratedFactionContactProvenanceRequirement | Require provenance for generated factions, contacts, NPCs, or institutions. | RT-008 primary, RT-007 consumer. | May not create durable generated social truth. | RT-008, RT-011. | future_required_not_implemented |
| SocialStateEventRequirement | Mark event/state commitment pressure without implementing an event ledger. | Future backend runtime, RT-001 boundary, RT-007 semantics. | May not commit events. | RT-001, RT-011, future event/state systems. | future_required_not_implemented |
| SocialFactionKnowledgeValidationRequirement | Require readiness checks for social/faction/knowledge boundaries. | RT-011 primary, RT-007 consumer. | May not validate itself. | RT-011. | future_required_not_implemented |

This inventory does not define final fields, formulas, JSON schema, database schema, Pydantic models, validator code, RNG code, social code, faction code, relationship code, actor-knowledge code, event code, persistence code, retrieval code, context-packet compiler code, or runtime code.

## 11. Validation and readiness requirements

Validation requirements are future requirements only. RT-007 coordinates with RT-011, but this specification does not implement validators.

Future validation/readiness requirements include:

- source linkage validation;
- social/faction/actor-knowledge owner-boundary validation;
- actor/faction knowledge coverage validation;
- rumor/false-claim/unverified/verified-fact separation validation;
- witness-state routing validation;
- relationship/reputation/standing coverage validation;
- obligation/debt/favor/influence routing validation;
- hidden motive/secret agenda redaction routing validation;
- mission/clue/faction consequence handoff validation;
- cost/consequence handoff validation;
- combat/hazard/social fallout handoff validation;
- ability/effect/social-skill handoff validation;
- generated faction/contact provenance validation;
- random social/faction dependency validation;
- item/asset/bribe/custody handoff validation;
- command/event boundary validation;
- LLM non-authority validation;
- non-implementation guardrail validation.

## 12. Downstream handoffs

RT-007 must hand off to:

- RT-001 for command lifecycle, action legality, social action declarations, faction action timing, rejection/quarantine, and event/state commitment boundaries;
- RT-002 for social costs, debts, obligations, favors, influence pressure, reputation pressure, penalties, compensation, losses, reward/loss math, and consequence math;
- RT-003 for combat/hazard social fallout, witnesses, threat response, institutional alarm, public danger, and harm-linked social consequences;
- RT-004 for social abilities, faction effects, influence effects, relationship effects, command effects, social skills, prerequisites, hidden capabilities, and effect-based knowledge changes;
- RT-005 for hidden motives, secret agendas, rumors, false claims, verified facts, redacted faction state, actor-known facts, faction-known facts, player-known facts, narrator fact-set limits, and context-packet projection;
- RT-006 for mission contacts, patrons, clue-linked social facts, reward/penalty routing, mission consequences, objective consequences, hidden-truth interactions, and scenario social state;
- RT-007 for its own social/faction/actor-knowledge semantic boundary before future backend ownership is separately authorized;
- RT-008 for generated NPCs, factions, contacts, institutions, relationship seeds, social sites, source-local social content, durable eligibility, recurrence eligibility, and provenance;
- RT-009 for random rumors, random faction response, random contact availability, social complications, reaction tables, oracle-derived social pressure, and table dependencies;
- RT-010 for item, gear, relic, vehicle, asset, bribe, blackmail material, cargo, custody, requisition, debt collateral, and asset-linked social state;
- RT-011 for validation/readiness governance;
- RT-012 for D-series/native-design social, faction, knowledge, institution, relationship, or contact patterns that cannot become runtime/canon/sourcebook authority without promotion.

## 13. LLM non-authority rules

RT-007 explicitly prohibits the LLM from:

- creating social state as backend truth;
- creating faction state as backend truth;
- deciding what an actor knows;
- deciding what a faction knows;
- converting rumors into facts;
- converting false claims into verified facts;
- deciding witness state;
- assigning reputation;
- assigning faction standing;
- assigning relationship state;
- creating obligations, debts, favors, oaths, threats, or blackmail as mechanical truth;
- determining social success or failure as mechanical truth;
- choosing faction responses;
- choosing institutional responses;
- selecting random rumors, contacts, reaction outcomes, or faction complications;
- creating generated NPCs, factions, contacts, institutions, or relationship content as durable backend truth;
- mutating social state;
- mutating faction state;
- mutating actor knowledge;
- mutating relationship state;
- committing reputation/standing events;
- treating dialogue as durable memory;
- treating summaries as actor-knowledge authority;
- treating social narration as event commitment;
- inventing schemas, fields, state machines, clocks, routes, tables, or formulas;
- bypassing RT-001, RT-002, RT-005, RT-006, RT-008, RT-009, or RT-011;
- authorizing canon/sourcebook/training/live-play use.

## 14. Non-implementation reaffirmation

This PR adds no sourcebook inclusion authorization, no pilot conversion authorization, and no canon promotion. This PR adds no:

- runtime code;
- schema implementation;
- command IR implementation;
- validator implementation;
- generator implementation;
- social system;
- faction system;
- reputation system;
- relationship engine;
- influence system;
- contact system;
- dialogue system;
- actor-knowledge database;
- faction-knowledge database;
- rumor system;
- belief-state engine;
- deception rules;
- witness system;
- obligation/debt economy;
- favor economy;
- faction clocks;
- institutional clocks;
- patron/rival system;
- social schema;
- faction state schema;
- actor-knowledge schema;
- reputation schema;
- relationship schema;
- contact schema;
- RNG/dice/table implementation;
- event ledger implementation;
- database schema;
- persistence writer;
- retrieval index;
- context-packet compiler;
- live-play prompt;
- training data;
- donor-content audit;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion.

## 15. Stage 2 output classification

```yaml
stage2_output:
  stage2_pr_id: STAGE2-PR-G4
  parent_stage2_pr_id: STAGE2-PR-G
  track: RT-007
  artifact_type: owner_specification
  implementation_status: non_executable_planning
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_validator_implementation: false
  authorizes_generator_implementation: false
  authorizes_social_system: false
  authorizes_faction_system: false
  authorizes_reputation_system: false
  authorizes_relationship_engine: false
  authorizes_actor_knowledge_database: false
  authorizes_faction_knowledge_database: false
  authorizes_rumor_system: false
  authorizes_belief_state_engine: false
  authorizes_faction_clocks: false
  authorizes_dialogue_system: false
  authorizes_rng_implementation: false
  authorizes_event_ledger: false
  authorizes_context_packet_compiler: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  authorizes_pilot_conversion: false
  next_allowed_step: RT-010 and RT-012 deferred convergence planning, pending review
```

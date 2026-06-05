# RT-003 Combat / Hazard / Damage / Recovery Owner Scaffold

Date prepared: 2026-06-05
Status: owner scaffold only
Tracking ID: REMEDIATION-RT003-COMBAT-HAZARD-DAMAGE-RECOVERY-OWNER-SCAFFOLD-001
Remediation track: RT-003-combat-hazard-damage-recovery
Owner: Astra Doctrine Council / future combat hazard damage recovery control owner

## 1. Purpose and scope

This file creates the documentation/control owner scaffold for RT-003, the combat, hazard exposure, damage, injury, and recovery ownership track identified by `REMEDIATION-PRIORITY-LEDGER-001`. It exists to name the future owner boundary that must separate active threat detection, hazard exposure timing, mitigation windows, damage/effect routing, injury and condition candidacy, recovery windows, vehicle/platform integrity pressure, mission consequence pressure, backend event commitment, context-packet handoff, and narration.

This scaffold is planning/control only. It is owner scaffold only: no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no damage table implementation, no validator implementation, no generator implementation, no persistence writer implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

This scaffold does not define final combat procedure, damage tables, hazard runtime, condition schemas, recovery formulas, encounter runtime, enemy behavior, live-play behavior, training data, donor-content audit results, or canon promotion.

## 2. Remediation ledger linkage

`docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` ranks RT-003 as P0 because combat and hazard findings require ownership for active threat detection, exposure intervals, damage severity, mitigation, injury/condition clocks, recovery, vehicle/platform integrity, and mission-linked consequences. The ledger recommends PR-B as the safe next owner-scaffold step: create resource/consequence and combat/hazard owner scaffolds after PR-A lands, without choosing formulas, damage tables, recovery rules, or encounter runtime.

RT-003 remains blocked by missing damage/injury math, missing hazard exposure state model, missing active threat queue/event owner, missing resource/consequence math, missing runtime RNG/table/oracle boundaries, and future validator readiness. It depends on RT-001 command lifecycle/action legality/cost commitment, RT-002 resource/backlash/consequence math, RT-009 runtime RNG/table/oracle, and RT-011 validation/readiness tooling.

## 3. Dependency on RT-001, RT-002, RT-009, and RT-011

RT-003 depends on `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` because combat and hazard actions require backend-owned legality, cost commitment, resolution triggering, event commitment, and narration handoff.

RT-003 depends on `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` because damage, injury, recovery, strain, backlash, corruption, rewards, losses, and mission consequences must route through future resource/consequence math and event ownership instead of narration.

RT-003 depends on future RT-009 runtime RNG/table/oracle ownership because hazard outcomes, random combat outcomes, hidden threat checks, table/oracle results, and replayable random decisions cannot be selected by the LLM.

RT-003 depends on `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` because prose readiness is not executable validation. Any later combat procedure, hazard runtime, damage math, condition schema, recovery formula, validator, or encounter runtime must pass separately authorized readiness controls before runtime, live-play, training, canon, generator, persistence, or context-packet claims are made.

## 4. Audit-source linkage

This scaffold links to these accepted audit sources without expanding, correcting, or implementing their findings:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, which establishes backend-first audit procedure, no-implementation boundaries, and the requirement that LLM narration/proposal remain separate from backend authority.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, which records A13 combat/hazard/damage/consequence pressure, B10 hazard/opposition/contact trigger pressure, and C09 hazard/environment record pressure.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`, which records C08 vehicle/ship/platform damage and repair pressure, C07 mission/scenario consequence pressure, and recurring A10 resource/cost/backlash pressure relevant to combat and recovery outcomes.

## 5. Source pressure

The future RT-003 owner must account for pressure from actual repo sources while preserving each source's current authority limits:

- A13: `docs/doctrine/world/A13_combat_hazard_damage_and_consequence_doctrine.md` supplies conflict scale, hazard, damage family, resistance, immunity, vulnerability, injury, death, recovery, transformation, and consequence propagation pressure. A13 is doctrine-draft material and does not define runtime conflict, injury, hazard, hidden-information, or event-commit state.
- B10: `docs/doctrine/operations/batch_b/B10_hazard_opposition_contact_and_active_threat_trigger_procedure.md` supplies hazard/opposition contact, active threat trigger, contact, warning, escalation, and owner-handoff pressure without final hazard runtime or encounter implementation.
- C09: `docs/doctrine/schema/C09_hazard_environment_record_schema.md` supplies hazard/environment record pressure, exposure, mitigation, visibility, consequence, and environmental threat pressure without live hazard resolution authority.
- C08: `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md` supplies vehicle/ship/platform integrity, movement, damage, repair, cargo, crew, and platform-state pressure without final platform runtime or damage table authority.
- C07: `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md` supplies mission/scenario/adventure threat, objective, consequence, reward/loss, escalation, hidden fact, and scenario-state pressure without final mission consequence runtime.
- A10: `docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md` supplies backlash, corruption, overload, heat/stress, strain/fatigue, sacrifice, debt, favor/disfavor, spiritual damage, dimensional contamination, and recovery pressure relevant to combat and hazard consequences. A10 is doctrine-draft material and does not define runtime resource, cooldown, corruption, or recovery state.

## 6. Owner responsibilities

The future RT-003 owner is responsible for planning and later coordinating, in separately authorized PRs, owner decomposition for:

- active threat detection, hidden threat redaction, and threat event commitment boundaries;
- hazard exposure timing, exposure intervals, mitigation windows, and consequence routing;
- combat action handoff to command lifecycle, cost/resource, RNG/table/oracle, damage/effect, and event owners;
- damage, injury, incapacitation, death, condition, recovery, repair, and platform integrity owner boundaries;
- mission consequence, reward/loss, and scenario-pressure handoffs created by combat or hazards;
- backend-owned validation before any persistent actor, vehicle/platform, mission, or environment state changes;
- context-packet contents after backend threat/hazard/damage/recovery decisions are committed;
- narration handoff rules that permit describing committed outcomes but not deciding exposure, harm, mitigation, recovery, enemy behavior, or state mutation;
- tests proving the LLM cannot detect hidden threats as authority, decide exposure timing, select hazard outcomes, apply damage/injury, kill/incapacitate actors, resolve mitigation/recovery, mutate vehicle/platform integrity, commit mission consequences, invent enemy behavior as mechanical truth, or treat combat narration as backend resolution.

## 7. Must-not-own boundaries

This scaffold and the future RT-003 owner must not own or claim to complete:

- final combat procedure;
- final damage tables or damage formulas;
- final hazard runtime or hazard generators;
- final encounter runtime;
- final injury, death, incapacitation, condition, or recovery schemas;
- final mitigation, repair, or recovery formulas;
- final enemy behavior mechanics;
- final mission consequence runtime;
- final vehicle/platform integrity runtime;
- final command IR fields;
- final JSON schemas, database schemas, or backend schemas;
- executable validators;
- runtime implementation or state-machine code;
- generators or generator prompts;
- persistence writer implementation;
- context-packet compiler implementation;
- donor-content audit;
- D-series source-material promotion;
- live-play authorization;
- training-data authorization;
- canon promotion.

## 8. Combat/hazard/recovery seams as conceptual placeholders only

The following names are planning placeholders for discussion and test targeting only:

- active_threat_detected
- hazard_exposure_checked
- mitigation_window_opened
- damage_or_effect_pending
- injury_condition_candidate
- recovery_window_opened
- vehicle_or_platform_integrity_pressure
- mission_consequence_pressure
- threat_event_committed
- narration_packet_prepared

These names are conceptual placeholders only. They are not final combat procedure, not a damage table, not hazard runtime, not condition schema, not recovery formula, not encounter runtime, not live-play authorization, not command IR, not executable validation, not persistence contracts, and not context-packet compiler output. They only identify seams that later owner work must resolve through separately authorized PRs.

## 9. Required future outputs

Future PRs, after this scaffold, must separately authorize and produce:

- combat/hazard owner specification;
- active threat and hidden-state redaction owner specification;
- hazard exposure and mitigation state model specification;
- damage/injury/recovery owner specification;
- vehicle/platform integrity and repair handoff plan;
- mission consequence handoff plan;
- runtime RNG/table/oracle dependency plan for hazard and combat outcomes;
- schema/readiness handoff plan for any future condition, damage, or recovery shape;
- validator family specification for threat, exposure, damage, mitigation, recovery, platform, and mission consequence transitions;
- persistence/event audit expectations;
- context-packet and narration handoff contract;
- tests proving backend authority over every combat, hazard, damage, injury, recovery, platform, and mission consequence state change;
- decision records for any movement from owner-scaffold planning to implementation.

## 10. Dependency relationships

RT-003 consumes RT-001 command lifecycle boundaries for action legality, cost commitment, resolution triggering, rollback/cancel/interrupt, and event commitment. RT-003 consumes RT-002 for resource, backlash, corruption, strain, damage-adjacent, recovery, reward, loss, and consequence math/event routing. RT-003 consumes future RT-009 for random outcomes, hidden threat checks, hazard tables, oracle/table results, and replay/audit requirements. RT-003 relies on RT-011 so that future prose controls are not mistaken for validators, damage tables, recovery formulas, runtime gates, or live-play authorization. RT-003 also coordinates with future runtime state/event, persistence, schema/math/mechanics, context-packet, generated-threat, and encounter-readiness owners without implementing those workstreams in this file.

## 11. LLM non-authority rules

RT-003 prohibits the LLM from:

- detecting hidden threats as authority;
- deciding exposure timing;
- rolling or selecting hazard outcomes;
- applying damage or injury;
- killing or incapacitating actors;
- resolving mitigation or recovery;
- mutating vehicle/platform integrity;
- committing mission consequences;
- inventing enemy behavior as mechanical truth;
- treating combat narration as backend resolution.

The LLM may only propose descriptive phrasing, ask clarifying questions, or narrate backend-committed outcomes when a future authorized context packet supplies those outcomes. It cannot be the authority for threat, exposure, hazard, damage, injury, death, recovery, platform, mission, or encounter state.

## 12. Context-packet and narration handoff expectations

Future RT-003 context packets must be backend-produced after validation and event commitment. They must distinguish visible committed facts, pending clarifications, redacted hidden threats, exposure status, mitigation windows, damage/effect status, recovery windows, platform/mission pressures, allowed narration emphasis, prohibited inference, and audit/event identifiers. Narration may describe committed combat or hazard outcomes but must not reveal hidden threats without authority, decide exposure timing, select outcomes, apply harm, mutate platform state, commit mission consequences, invent enemy mechanics, or turn combat prose into backend resolution.

This scaffold does not create a context-packet compiler, packet schema, event schema, validator, persistence writer, combat runtime, hazard runtime, encounter runtime, damage table, recovery formula, enemy generator, or narration generator.

## 13. First-test expectations

The first RT-003 tests should remain focused and non-brittle. They should verify this owner scaffold exists, references RT-003 and `REMEDIATION-PRIORITY-LEDGER-001`, links AUDIT-001/AUDIT-WAVE1-001/AUDIT-WAVE2-001, references RT-001/RT-002/RT-009/RT-011, records source pressure from A13/B10/C09/C08/C07/A10, includes explicit non-implementation guardrails, names only conceptual placeholders, and prohibits LLM authority over hidden threats, exposure timing, hazard outcomes, damage/injury, death/incapacitation, mitigation/recovery, vehicle/platform integrity, mission consequences, enemy behavior as mechanical truth, and combat narration as backend resolution.

## 14. Explicit non-implementation statement

This RT-003 owner scaffold is documentation/control planning only. It implements no doctrine rewrite, runtime, schema, command IR, math, damage table, hazard generator, hazard runtime, combat runtime, encounter runtime, condition schema, recovery formula, validator, generator, persistence writer, context-packet compiler, live-play adapter, training data, donor-content audit, D-series promotion, or canon promotion.

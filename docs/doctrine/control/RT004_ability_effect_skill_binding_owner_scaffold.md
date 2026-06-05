# RT-004 Ability / Effect / Skill Binding Owner Scaffold

Date prepared: 2026-06-05
Status: owner scaffold only
Tracking ID: REMEDIATION-RT004-ABILITY-EFFECT-SKILL-BINDING-OWNER-SCAFFOLD-001
Remediation track: RT-004-ability-effect-skill-binding
Owner: Astra Doctrine Council / future ability, effect, skill, and advancement-binding boundary owner

## 1. Purpose and scope

This file creates the documentation/control owner scaffold for RT-004, the ability, effect, cost, cooldown, skill, and advancement binding track identified by `REMEDIATION-PRIORITY-LEDGER-001`. It names the future control owner that must separate ability records, technique/power references, prerequisite checks, acquisition eligibility, mastery state, skill synthesis, action binding, effect taxonomy, cost/backlash/cooldown pressure, advancement triggers, backend authorization, validation, and narration handoff.

This scaffold is planning/control only. It is owner scaffold only: no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no generated ability creation, no advancement award, no ability/power/technique/skill/perk/mastery creation, no cost or cooldown setting, no prerequisite change, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

This scaffold does not implement remediation. It does not define final ability records, final schemas, generated powers, advancement rules, final formulas, command IR, runtime state, validators, generators, persistence writers, context-packet compilers, live-play prompts, training behavior, or backend effect resolution.

## 2. Remediation ledger linkage

`docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` records RT-004 as the track for ability/effect/skill binding pressure. The ledger places PR-E after RT-001 command, RT-002 cost/resource, RT-005 context/hidden-information, RT-008 provenance/recurrence, and RT-011 validation-readiness scaffolds exist, and summarizes PR-E as: “Ability/skill and social/faction owner scaffolds. Add RT-004 and RT-007 after command/cost/context/provenance scaffolds exist. Do not generate powers, mutate relationships, or commit faction actions.”

This PR-E file therefore only identifies owner boundaries for future remediation. It does not generate abilities, powers, techniques, skills, perks, or mastery; it does not award advancement; and it does not authorize live-play capability.

## 3. Dependency on existing remediation tracks

RT-004 depends on `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` because ability/effect use must remain downstream of RT-001 command lifecycle, action declaration, legality review, cost commitment, resolution triggering, and backend event/state commitment. Ability narration or model suggestion cannot bind an ability to an action as authority.

RT-004 depends on `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` because cost/backlash/cooldown pressure must remain downstream of RT-002. Costs, refunds, cooldowns, backlash, corruption, strain, overcommitment, reward/loss, and consequence pressure cannot be set or resolved by this scaffold or by the LLM.

RT-004 depends on `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md` because generated abilities or techniques require RT-008 provenance/recurrence controls before persistence. No generated ability, generated technique, generated skill, generated perk, or generated mastery may become durable, recurrent, retrievable, or canon from narration or model memory.

RT-004 depends on `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` because prose owner boundaries are not executable validators. Future ability/effect eligibility, action binding, cost/cooldown binding, advancement, skill synthesis, generated-content persistence, and narration handoffs require separately authorized validation and reviewer gates.

RT-004 must coordinate with `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md` where effects pressure damage, recovery, hazards, exposure, injury, combat outcomes, or active-threat state. RT-004 must coordinate with `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md` where effect visibility, concealed prerequisites, hidden consequences, available choices, known techniques, or narration boundaries matter.

## 4. Audit-source linkage

This scaffold links to accepted audit sources without expanding, correcting, or implementing their findings:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, which establishes backend-first audit procedure, non-implementation boundaries, and the rule that LLM narration/proposal is not backend authority.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, which records ability, faction, hazard, hidden-information, generated-content, and backend ownership pressure from early schema/doctrine families.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`, which records generated/provenance, procedure, source-pack, schema/math/mechanics, command, reward, and validation pressure that future ability/effect binding must not bypass.

## 5. Source pressure and actual-file posture

The future RT-004 owner must account for pressure from actual repo sources while preserving each source's current authority limits:

- A08: `docs/doctrine/advancement/A08_path_domain_and_technique_mastery_doctrine.md` pressures path, domain, technique, mastery, lineage, and prerequisite language, but does not authorize runtime ability state, final mastery mechanics, generated techniques, or live-play capability.
- A09: `docs/doctrine/advancement/A09_skill_competency_and_synthesis_doctrine.md` pressures skill competency, synthesis, training, and capability expression, but does not let the LLM decide persistent skill synthesis outputs, grant perks, award mastery, or create final skill mechanics.
- A10: `docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md` pressures cost, backlash, corruption, strain, risk, and overinvestment language, but RT-002 remains the downstream owner for cost/backlash/cooldown math and consequence commitment.
- B02: `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` pressures action declaration, cost commitment, and resolution triggering, which reinforces that ability/effect use must pass through RT-001 before any backend-approved outcome can be narrated.
- C03: `docs/doctrine/schema/C03_ability_power_technique_record_schema.md` pressures ability, power, technique, prerequisite, effect, resource, source-local, generated-content, and canon-review record shape, but this scaffold is not a C03 schema implementation.
- SM00: `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` pressures schema/math/mechanics sequencing and readiness gates, but this scaffold does not choose formulas, thresholds, validators, or benchmark math.
- ROADMAP-001: `docs/doctrine/astra_doctrine_roadmap_v0_1.md` supplies backend-first language and the backend-first model-interchangeability invariant: if persistent truth, rules, dice, validation, generated content, retrieval, memory, or consequences are needed, the backend owns the authoritative pathway and the LLM may only narrate, summarize, interpret, or propose within contract.

## 6. Owner responsibilities

The future RT-004 owner is responsible for specifying, in later separately authorized PRs:

- how ability, power, technique, skill, perk, mastery, prerequisite, acquisition, and advancement references are routed without donor-law creep;
- how ability/effect activation remains downstream of RT-001 command lifecycle and backend action legality;
- how cost, backlash, cooldown, overcommitment, strain, corruption, reward/loss, and consequence pressure hand off to RT-002;
- how damage, hazard, recovery, and visibility effects hand off to RT-003 and RT-005;
- how generated abilities or techniques are rejected, reviewed, or routed through RT-008 provenance/recurrence controls before persistence;
- how future validators and reviewer gates from RT-011 are required before capability, advancement, or persistent state changes;
- how context packets expose only backend-approved ability/effect outcomes and redact unavailable or hidden facts;
- how narration describes backend-approved outcomes without becoming backend effect resolution.

## 7. Must-not-own boundaries

This scaffold and the future RT-004 owner must not own or claim to complete:

- final ability, power, technique, skill, perk, mastery, or advancement doctrine;
- final ability records or C03 schema implementation;
- generated powers, generated techniques, generated abilities, or generated skill lines;
- prerequisite changes, capability grants, advancement awards, progression thresholds, or mastery awards;
- final cost values, cooldown values, backlash formulas, corruption formulas, strain formulas, or effect formulas;
- command IR, action legality runtime, effect runtime, combat runtime, hazard runtime, social runtime, or live-play prompts;
- executable validators, generators, persistence writers, retrieval indexes, context-packet compilers, or narration validators;
- canon promotion, sourcebook inclusion, live-play authorization, training-data authorization, or donor-content audit.

## 8. Ability/effect/skill binding seams as conceptual placeholders only

The following names are planning placeholders for discussion and test targeting only:

- ability_record_reference
- prerequisite_check_required
- acquisition_eligibility_pending
- mastery_state_pending
- effect_taxonomy_required
- cost_binding_required
- cooldown_state_pending
- action_binding_required
- skill_synthesis_review
- advancement_trigger_pending
- generated_ability_prohibited

These names are conceptual placeholders only. They are not final schemas, not ability records, not generated powers, not advancement rules, not final formulas, not command IR, not runtime state, not validators, and not live-play authorization. They only identify seams that later owner work must resolve through separately authorized PRs.

## 9. Required future outputs

Future PRs, after this scaffold, must separately authorize and produce:

- ability/effect/skill owner specification;
- prerequisite/acquisition/mastery/advancement routing matrix;
- effect taxonomy and visibility handoff plan;
- cost/backlash/cooldown handoff contract with RT-002;
- command/action binding contract with RT-001;
- generated ability/technique provenance contract with RT-008;
- context-packet and narration handoff contract with RT-005;
- validator/readiness requirements tied to RT-011;
- first fixtures proving the LLM cannot invent capability, award advancement, set costs/cooldowns, resolve effects as truth, or bypass validation;
- decision records for any movement from owner-scaffold planning to implementation.

## 10. Dependency relationships

RT-004 consumes RT-001 command lifecycle boundaries before ability/effect use can be authorized. RT-004 consumes RT-002 cost/backlash/cooldown boundaries before resources or consequences can be committed. RT-004 coordinates with RT-003 when effects become damage, recovery, hazard, or active-threat pressure. RT-004 coordinates with RT-005 for effect visibility, hidden prerequisites, allowed narration, redaction, and context-packet boundaries. RT-004 relies on RT-008 before generated abilities or techniques persist or recur. RT-004 relies on RT-011 before prose controls become tests, validators, or reviewer gates.

## 11. LLM non-authority rules

RT-004 prohibits the LLM from:

- inventing abilities, powers, techniques, skills, perks, or mastery;
- awarding advancement;
- changing prerequisites;
- setting costs or cooldowns;
- resolving effects as mechanical truth;
- binding abilities to actions as authority;
- deciding skill synthesis outputs as persistent state;
- creating generated abilities or techniques;
- granting player capability;
- bypassing validation/reviewer approval;
- treating ability narration as backend effect resolution.

The LLM may only propose non-authoritative phrasing, ask clarifying questions, or narrate backend-approved ability/effect outcomes supplied by a future authorized context packet. Ability/effect use must remain downstream of RT-001 command lifecycle. Cost/backlash/cooldown pressure must remain downstream of RT-002. Generated abilities or techniques require RT-008 provenance/recurrence controls before persistence. Narration may only describe backend-approved ability/effect outcomes.

## 12. Context-packet and narration handoff expectations

Future RT-004 context packets must be backend-produced after command legality, cost/consequence validation, effect authorization, visibility filtering, and reviewer/validator gates. Packets must distinguish backend-approved ability/effect outcomes, visible prerequisites, unavailable or hidden capabilities, pending skill synthesis candidates, generated ability rejection/provenance status, allowed narration emphasis, prohibited inference, and audit/event identifiers.

Narration may describe only backend-approved ability/effect outcomes. Narration must not choose the ability used, decide prerequisites, set costs or cooldowns, award advancement, create powers, resolve mechanical truth, convert ability description into backend state, or treat evocative ability prose as effect resolution.

This scaffold does not create a context-packet compiler, packet schema, effect schema, ability schema, validator, generator, persistence writer, command IR, or narration generator.

## 13. First-test expectations

The first RT-004 tests should remain focused and non-brittle. They should verify this owner scaffold exists, references RT-004 and `REMEDIATION-PRIORITY-LEDGER-001`, links AUDIT-001/AUDIT-WAVE1-001/AUDIT-WAVE2-001, references RT-001/RT-002/RT-008/RT-011 plus RT-003/RT-005 where boundaries matter, records source pressure from A08/A09/A10/B02/C03/SM00/ROADMAP-001, includes backend-first and backend-first model-interchangeability language, includes explicit non-implementation guardrails, names only conceptual placeholders, and prohibits LLM authority over ability invention, advancement awards, prerequisite changes, cost/cooldown setting, mechanical effect truth, action binding, skill synthesis persistence, generated ability creation, player capability grants, validation bypass, and ability narration as backend resolution.

## 14. Explicit non-implementation statement

This RT-004 owner scaffold is documentation/control planning only. It implements no doctrine rewrite, runtime, schema, command IR, math, ability record, generated power, advancement rule, final formula, validator, generator, persistence writer, retrieval index, context-packet compiler, live-play prompt, training behavior, donor-content audit, or canon promotion.

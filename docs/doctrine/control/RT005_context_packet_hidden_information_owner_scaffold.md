# RT-005 Context-Packet / Hidden-Information Owner Scaffold

Date prepared: 2026-06-05
Status: owner scaffold only
Tracking ID: REMEDIATION-RT005-CONTEXT-PACKET-HIDDEN-INFORMATION-OWNER-SCAFFOLD-001
Remediation track: RT-005-scene-activity-context-packets
Owner: Astra Doctrine Council / future scene activity and context-packet boundary control owner

## 1. Purpose and scope

This file creates the documentation/control owner scaffold for RT-005, the scene/activity orchestration and hidden-information/context-packet boundary track identified by `REMEDIATION-PRIORITY-LEDGER-001`. It exists to name the future owner boundary that must separate backend-owned active scene state, participant rosters, visible facts, hidden facts, actor knowledge, faction/NPC beliefs, source-local protected truth, redaction decisions, context-packet projections, and narration.

This scaffold is planning/control only. It is owner scaffold only: no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no narration validator implementation, no live-play prompt implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

This scaffold does not implement remediation. It does not define final packet schemas, hidden-state database schemas, actor-knowledge schemas, redaction algorithms, retrieval indexes, narration validators, context-packet compilers, live-play prompts, runtime code, generators, validators, persistence writers, command IR, training data, donor-content audit results, or canon promotion.

## 2. Remediation ledger linkage

`docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` ranks RT-005 as P0/high risk because scene, social, location, mission, hazard, and oracle records all require backend-owned active scene state, participant rosters, visibility partitions, hidden facts, redactions, and context-packet projections. The ledger recommends PR-C as the safe next owner-scaffold step: create context-packet and hidden-information owner scaffolds with redaction, visibility, scene-state, and narration downstream-of-backend guardrails, without building packet compilers or live-play prompts.

RT-005 remains blocked by missing scene lifecycle state model, missing context-packet compiler owner, missing hidden-information partition schema, missing knowledge/dialogue memory owner, missing narration validator owner, missing persistence/event owners, and future validator readiness.

## 3. Dependency on RT-001, RT-002, RT-003, RT-011, and later tracks

RT-005 depends on `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` because scene transitions, action availability, clarification routing, event commitment, and narration handoff must remain downstream of backend-owned command lifecycle and action-legality decisions.

RT-005 depends on `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` because visible resource pressure, concealed thresholds, backlash/corruption/strain routing, rewards/losses, and consequence events must be projected only after backend-owned resource/consequence math and event commitment.

RT-005 depends on `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md` because hazard cues, hidden threats, exposure status, damage/effect status, recovery windows, and mission/platform pressure must be redacted before narration and cannot be inferred from combat or hazard prose.

RT-005 depends on `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` because prose readiness is not executable validation. Any later context-packet schema, hidden-information partition, redaction validator, narration validator, runtime state model, retrieval index, or compiler must pass separately authorized readiness controls before runtime, live-play, training, canon, generator, persistence, or context-packet claims are made.

RT-005 must coordinate with later RT-007 social/faction knowledge-state ownership wherever NPC/faction beliefs, relationship facts, institutional knowledge, rumors, secrets, or actor-known facts are involved. RT-005 must coordinate with later RT-009 runtime RNG/table/oracle ownership wherever random table outputs, oracle results, hidden rows, protected outcomes, seed/replay references, or redacted result projections are involved. RT-005 also receives pressure from later RT-006 mission/reward/clue routing for clue visibility and hidden-truth partitions, but this file does not implement those tracks.

## 4. Audit-source linkage

This scaffold links to these accepted audit sources without expanding, correcting, or implementing their findings:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, which establishes the backend-first audit procedure, no-implementation boundary, and requirement that LLM narration/proposal remain separate from backend authority.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, which records hidden facts, hazard/environment redaction, deferred context-packet contracts, and narration downstream of backend state/validation pressure.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`, which records B01 scene orchestration, B09 social/faction knowledge, C06 location hidden-feature, C07 mission hidden-truth/clue, and C10 table/oracle hidden-result pressure.

## 5. Source pressure and actual-file posture

The future RT-005 owner must account for pressure from actual repo sources while preserving each source's current authority limits:

- B01 requested source check: `docs/doctrine/operations/batch_b/B01_scene_activity_orchestration_and_runtime_authority_procedure.md` is absent in this repo. The nearest actual B01 source confirmed present is `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md`, which supplies scene/encounter/activity orchestration, activity-state, transition, and runtime-authority pressure without final scene runtime implementation.
- B09 requested source check: `docs/doctrine/operations/batch_b/B09_social_faction_relationship_and_actor_knowledge_procedure.md` is absent in this repo. The nearest actual B09 source confirmed present is `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md`, which supplies social/faction/contact, risk/visibility, standing, obligation, access, hidden-truth presentation, and actor/faction knowledge pressure without final social mechanics or runtime relationship state.
- C06: `docs/doctrine/schema/C06_location_site_region_record_schema.md` supplies location/site/region reference pressure, including visible location facts, access posture, hidden features, hazards, routes, and source-local/canon boundaries without runtime hidden-state authority.
- C07: `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md` supplies mission/scenario/adventure pressure for objectives, scenes, branches, rewards, consequences, hidden/protected truth, spoilers, clues, and player-facing truth boundaries without mission runtime implementation.
- C09: `docs/doctrine/schema/C09_hazard_environment_record_schema.md` supplies hazard/environment pressure for visible cues, hidden hazard parameters, exposure, mitigation, recurrence, consequence, and redaction boundaries without hazard runtime implementation.
- C10: `docs/doctrine/schema/C10_table_oracle_record_schema.md` supplies table/oracle pressure for hidden/protected results, source-local secrets, oracle result routing, and the rule that table/oracle records do not create hidden-information runtime state, executable oracle memory, reveal procedure, or live-play knowledge policy.
- Roadmap backend-first/context-packet language: `docs/doctrine/astra_doctrine_roadmap_v0_1.md` states that the backend is authoritative, runtime state is not model memory, model context is never authoritative persistence, context packets must preserve hidden information boundaries, and dialogue transcripts remain distinct from validated authoritative claims and state deltas.
- SM00: `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` is relevant as sequencing pressure only: it distinguishes schema/math/mechanics planning from runtime readiness and does not authorize context-packet implementation.

## 6. Owner responsibilities

The future RT-005 owner is responsible for planning and later coordinating, in separately authorized PRs, the owner decomposition for:

- active scene/activity state ownership and scene lifecycle handoff;
- participant visibility partition ownership;
- visible versus hidden location fact projection;
- hazard redaction boundaries for visible cues, hidden parameters, exposure, mitigation, and consequence pressure;
- mission clue visibility and hidden-truth partition handoff;
- faction or actor knowledge partition coordination with future RT-007;
- oracle/table result redaction coordination with future RT-009;
- backend-produced context-packet projection contracts;
- narration allowed fact sets and forbidden inference sets;
- tests proving the LLM cannot act as authority for hidden information, player/NPC/faction knowledge, clue/oracle selection, backend fact invention, narration-as-discovery, summaries-as-memory-authority, scene-state mutation, context-packet compilation, or redaction bypass.

## 7. Must-not-own boundaries

This scaffold and the future RT-005 owner must not own or claim to complete:

- final packet schema;
- final hidden-state database schema;
- final actor-knowledge schema;
- final redaction algorithm;
- executable validators;
- narration validator implementation;
- context-packet compiler implementation;
- retrieval index implementation;
- runtime implementation or scene state-machine code;
- live-play prompts or live-play adapter behavior;
- command IR fields;
- final resource/consequence math;
- table/oracle RNG implementation;
- generators or generator prompts;
- persistence writer implementation;
- donor-content audit;
- source doctrine rewrite;
- canon promotion;
- live-play authorization;
- training-data authorization.

## 8. Hidden-information/context-packet seams as conceptual placeholders only

The following names are planning placeholders for discussion and test targeting only:

- scene_state_visible
- scene_state_hidden
- participant_visibility_partition
- location_fact_projection
- hazard_redaction_boundary
- mission_clue_visibility
- faction_or_actor_knowledge_partition
- oracle_result_redaction
- context_packet_prepared
- narration_allowed_fact_set
- narration_forbidden_inference_set

These names are conceptual placeholders only. They are not final packet schema, not context-packet compiler output, not hidden-state database, not retrieval index, not narration validator, not live-play prompt, not runtime implementation, not executable validation, not persistence contract, not actor-knowledge schema, not redaction algorithm, not command IR, and not canon promotion. They only identify seams that later owner work must resolve through separately authorized PRs.

## 9. Required future outputs

Future PRs, after this scaffold, must separately authorize and produce:

- scene/activity runtime owner specification;
- visible/hidden scene-state model specification;
- participant visibility partition specification;
- location fact projection and hidden-feature redaction specification;
- hazard redaction and exposure projection specification;
- mission clue visibility and hidden-truth partition specification;
- faction/actor knowledge partition handoff plan with future RT-007;
- oracle/table hidden-result handoff plan with future RT-009;
- backend-produced context-packet contract specification;
- narration allowed-fact and forbidden-inference contract specification;
- dialogue-to-claim extraction and reviewer-validation handoff plan;
- validator family specification for redaction, packet projection, narration, and knowledge-claim boundaries;
- persistence/event audit expectations;
- tests proving backend authority over context packets, redaction, knowledge partitions, and narration boundaries;
- decision records for any movement from owner-scaffold planning to implementation.

## 10. Dependency relationships

RT-005 consumes RT-001 command lifecycle boundaries for scene transitions, action availability, event commitment, and narration handoff. RT-005 consumes RT-002 for resource/consequence projections and hidden threshold redaction. RT-005 consumes RT-003 for hazard/combat visibility and hidden threat redaction. RT-005 relies on RT-011 so that future prose controls are not mistaken for packet schemas, hidden-state schemas, runtime gates, validators, compilers, narration validators, retrieval indexes, or live-play authorization.

RT-005 prepares shared seams for later RT-007 social/faction knowledge-state ownership and later RT-009 runtime RNG/table/oracle ownership. It does not implement RT-007 or RT-009. It also coordinates with later mission/clue routing, persistence, retrieval, event-log, schema/math/mechanics, generated-content, and narration-validator owners without implementing those workstreams in this file.

## 11. LLM non-authority rules

RT-005 prohibits the LLM from:

- deciding what hidden information exists;
- revealing hidden state;
- deciding what a player character knows;
- deciding NPC/faction knowledge;
- selecting clues or oracle/table outcomes;
- inventing backend facts for narration;
- treating narration as discovery;
- treating summaries as memory authority;
- mutating scene state;
- compiling context packets;
- bypassing redaction boundaries.

The LLM may only propose phrasing, ask clarifying questions, or narrate backend-supplied visible facts when a future authorized context packet supplies those facts. It cannot be the authority for hidden facts, player-known facts, NPC/faction beliefs, rumors, false claims, backend truth, clue visibility, oracle outcomes, scene state, memory, retrieval, persistence, or redaction.

## 12. Context-packet and narration downstream-of-backend expectations

Context packets are backend-produced projections, not model memory. Context packets may only be prepared from backend-owned truth, committed state, validated knowledge records, authorized rumors, protected hidden facts, review-approved redactions, event logs, and future owner-approved projection rules.

Narration may only use allowed facts supplied by backend-owned context packets. Narration must remain downstream of backend validation, event commitment, hidden-information partitioning, and redaction. Narration may describe visible committed scene facts, visible participant posture, visible location facts, visible hazard cues, accepted objectives, known clues, authorized rumors, and backend-approved social/faction statements. Narration must not infer, reveal, invent, select, or mutate hidden state, hidden truth, NPC/faction beliefs, player knowledge, oracle outcomes, hazards, clues, rewards, consequences, or scene transitions.

Hidden facts, unverified rumors, false claims, NPC/faction beliefs, player-known facts, and backend truth must remain distinguishable. Dialogue transcripts and summaries are not automatically authoritative truth. Future dialogue-to-claim extraction must be backend/reviewer validated before any claim can affect backend truth, beliefs, retrieval, clocks, faction state, consequences, scene state, or context-packet projection.

## 13. First-test expectations

The first RT-005 tests should remain focused and non-brittle. They should verify this owner scaffold exists, references RT-005 and `REMEDIATION-PRIORITY-LEDGER-001`, links AUDIT-001/AUDIT-WAVE1-001/AUDIT-WAVE2-001, references RT-001/RT-002/RT-003/RT-011 and later RT-007/RT-009, records source pressure from B01/B09/C06/C07/C09/C10 and roadmap backend-first/context-packet language, includes explicit non-implementation guardrails, names only conceptual placeholders, states context packets are backend-produced projections and not model memory, distinguishes backend truth/player-known facts/NPC-faction beliefs/rumors/false claims/dialogue transcripts/summaries, and prohibits LLM authority over hidden information, knowledge decisions, clue/oracle selection, backend fact invention, narration-as-discovery, summaries-as-memory-authority, scene-state mutation, context-packet compilation, and redaction bypass.

## 14. Explicit non-implementation statement

This RT-005 owner scaffold is documentation/control planning only. It implements no doctrine rewrite, runtime, schema, command IR, math, validator, generator, persistence writer, retrieval index, context-packet compiler, narration validator, live-play prompt, hidden-state database, actor-knowledge schema, redaction algorithm, live-play adapter, training data, donor-content audit, source doctrine rewrite, or canon promotion.

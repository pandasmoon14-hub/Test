# RT-005 Context-Packet / Hidden-Information Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification only; non-executable planning artifact
Tracking ID: STAGE2-PR-D-RT005-CONTEXT-PACKET-HIDDEN-INFORMATION-OWNER-SPECIFICATION-001
Remediation track: RT-005-scene-activity-context-packets
Owner: Astra Doctrine Council / future scene activity and context-packet boundary control owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-005. It upgrades the RT-005 owner scaffold into a specification-level planning artifact for context-packet and hidden-information ownership while remaining non-executable and non-implementation.

This specification defines ownership boundaries, conceptual information partitions, handoff requirements, redaction boundary requirements, hidden-result routing requirements, narration fact-set constraints, validation/readiness expectations, and downstream coordination obligations. It does not implement any runtime component, schema, context-packet compiler, database, redaction algorithm, retrieval index, narration validator, live-play prompt, generator, validator, persistence writer, training artifact, donor-content audit, sourcebook inclusion authorization, pilot conversion authorization, or canon promotion.

This specification links to and depends on these prior planning artifacts:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.
- RT-005 owner scaffold: `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md`.
- RT-001 owner specification: `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`.
- RT-002 owner specification: `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`.
- RT-011 owner specification: `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`.

The Stage 2 plan identifies STAGE2-PR-D as the RT-005 context-packet and hidden-information owner specification. This file satisfies that planning slot only; it does not authorize implementation work.

## 2. Source posture and file-presence disclosure

This specification was drafted against actual repository paths. The following required or context-pressure files were present and considered as source pressure without expanding their authority:

- `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md`.
- `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`.
- `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`.
- `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`.
- `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md`.
- `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md`.
- `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_scaffold.md`.
- `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_scaffold.md`.
- `docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md`.
- `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md`.
- `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md`.
- `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md`.
- `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md`.
- `docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md`.
- `docs/doctrine/schema/C01_creature_npc_record_schema.md`.
- `docs/doctrine/schema/C05_faction_institution_record_schema.md`.
- `docs/doctrine/schema/C06_location_site_region_record_schema.md`.
- `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`.
- `docs/doctrine/schema/C09_hazard_environment_record_schema.md`.
- `docs/doctrine/schema/C10_table_oracle_record_schema.md`.
- `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md`.
- `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md`.
- `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md`.
- `docs/doctrine/astra_doctrine_roadmap_v0_1.md`.
- `docs/doctrine/astra_doctrine_registry_v0_1.yaml`.
- `docs/decisions/current_decisions_log.md`.
- `README.md`.

The following requested file was absent at drafting time and no equivalent was substituted as an authoritative source for it:

- `docs/doctrine/operations/batch_b/B01_scene_activity_orchestration_and_runtime_authority_procedure.md`.

The repository does contain `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md`, but this specification does not treat that path as the same requested source unless a later review explicitly authorizes that substitution.

## 3. RT-005 scope

RT-005 owns planning requirements for context-packet and hidden-information boundaries. Its scope includes:

- hidden-information ownership boundaries;
- context-packet projection boundary requirements;
- visible, hidden, redacted, derived, narrator-facing, and reviewer-only information partition requirements;
- player-known fact requirements;
- character-known fact requirements;
- NPC-known and faction-known belief and knowledge requirements;
- rumor, false claim, unverified claim, and verified fact separation requirements;
- dialogue transcript versus summary versus durable claim boundary requirements;
- narrator-facing allowed fact-set requirements;
- narrator-facing forbidden inference-set requirements;
- clue visibility and hidden-truth exposure boundary requirements;
- hidden cost, consequence, reward, loss, and recovery visibility handoff from RT-002;
- hidden hazard, combat, damage, injury, recovery, exposure, and threat visibility handoff from RT-003;
- ability, effect, skill, capability, prerequisite, cooldown, and secret capability visibility handoff from RT-004;
- mission, clue, hidden-truth, branch, objective, scenario revelation, and reward-visibility handoff from RT-006;
- social, faction, actor-knowledge, relationship, obligation, rumor, standing, and hidden-agenda handoff from RT-007;
- generated-content projection, provenance, recurrence, source-local status, durable generated fact, and projection-eligibility handoff from RT-008;
- RNG, table, oracle, hidden row, protected outcome, seed/replay, and hidden-result handoff from RT-009;
- inventory, item, vehicle, asset, hidden property, secret cargo, custody, loadout, charge, durability, and vehicle-state handoff from RT-010;
- validation/readiness handoff to RT-011;
- D-series/native-design context authority handoff to RT-012;
- auditability requirements for later backend-owned context-packet, redaction, retrieval, hidden-state, knowledge, and narration controls.

RT-005 scope is semantic and governance-oriented. It identifies what future implementations must preserve, separate, route, or validate, but it does not define final data structures or executable behavior.

## 4. Must-not-own boundaries

RT-005 must not own or claim to complete:

- final context-packet schema;
- context-packet compiler implementation;
- hidden-state database schema;
- retrieval index implementation;
- redaction algorithm implementation;
- narration validator implementation;
- runtime code;
- schema implementation;
- command IR implementation;
- validator implementation;
- generator implementation;
- persistence writer implementation;
- RNG, dice, or table implementation;
- event ledger implementation;
- database schema;
- live-play prompt implementation;
- training data;
- donor-content audits;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion;
- final actor-knowledge schema;
- final rumor or claim schema;
- final memory system.

If later work needs any of these outputs, it must be separately authorized and routed to the owning track before implementation.

## 5. Authority model

RT-005 follows the backend-first, model-interchangeable authority posture recorded in the roadmap and README:

- RT-001 owns command/event lifecycle, action legality, event commitment, rejection/quarantine posture, and the timing of context/narration handoffs.
- RT-002 owns resource/consequence math. RT-005 owns only whether resource, cost, consequence, reward, loss, recovery, threshold, strain, backlash, corruption, or overcommitment information is visible, redacted, hidden, reviewer-only, or narrator-projected after RT-002 and RT-001 ownership has been respected.
- RT-011 owns validation/readiness requirements, reviewer-decision requirements, failure taxonomy, test-plan posture, and the boundary between validation requirements and validator implementation.
- Once implemented by separately authorized future work, the backend owns all hidden truth, visibility partitioning, packet production, redaction, retrieval eligibility, durable memory authority, source/provenance eligibility, state mutation, event commit, and persistence authority.
- The LLM may only narrate from backend-approved allowed fact sets and may ask clarification questions when backend context is marked insufficient.
- LLM memory, summaries, dialogue fluency, and narration are not state, truth, discovery, source promotion, durable claim authority, or persistence.

RT-005 therefore treats context packets as backend-produced projections rather than model memory and treats narration as downstream presentation rather than authority.

## 6. Information partition contract

The following conceptual partitions are planning placeholders only. They name separation requirements for future specification, validation, and implementation work; they are not final schemas, not database fields, not retrieval index records, not context-packet compiler output, not redaction algorithms, not memory implementation, not runtime state, and not live-play prompts.

| Conceptual partition | Planning meaning | Boundary requirement |
|---|---|---|
| `backend_truth_partition` | Authoritative truth held by the future backend after validated commit. | Never exposed to the LLM or player unless visibility and projection are authorized. |
| `player_known_fact_partition` | Facts the player is authorized to know. | Must remain distinguishable from what a character, NPC, faction, or reviewer knows. |
| `character_known_fact_partition` | Facts a player character is authorized to know in-world. | Must not automatically include all player-known or backend-known facts. |
| `npc_known_fact_partition` | Facts or beliefs an NPC is authorized to know or hold. | Must not be treated as backend truth unless separately validated. |
| `faction_known_fact_partition` | Facts or beliefs an institution, faction, domain, or organized actor is authorized to know or hold. | Must coordinate with RT-007 and remain separate from player/character/backend truth. |
| `rumor_or_unverified_claim_partition` | Unverified claims, reports, hearsay, rumors, allegations, or uncertain testimony. | Must not become truth through narration, summary, or repetition. |
| `false_claim_partition` | Claims known or later adjudicated as false by backend/reviewer authority. | Must not be auto-corrected or revealed unless backend projection authorizes correction. |
| `hidden_truth_partition` | Truth intentionally hidden from player-facing or narrator-facing projection. | Must not leak through flavor, speculation, summaries, absence, or pattern inference. |
| `secret_agenda_partition` | NPC/faction/actor hidden motive, obligation, plan, or agenda. | Must remain redacted unless backend context authorizes projection. |
| `hidden_hazard_partition` | Hidden combat, hazard, exposure, damage, trap, environmental, or threat information. | Must coordinate with RT-003 and avoid cueing unauthorized details. |
| `hidden_random_result_partition` | Hidden RNG, table, oracle, result row, seed/replay, or protected outcome information. | Must coordinate with RT-009 before projection. |
| `redacted_fact_partition` | Facts recognized by backend/reviewer authority but withheld or partially withheld. | Redaction boundaries must be backend-owned and auditable. |
| `derived_inference_partition` | Candidate inferences derived from visible facts, rules, or context. | Must not infer hidden state, hidden truth, or source-protected facts without authority. |
| `narrator_allowed_fact_set` | Facts and presentation constraints approved for narration. | Narration may use only this set plus approved style, tone, and non-authoritative flavor. |
| `narrator_forbidden_inference_set` | Facts, inferences, explanations, and implications forbidden from narration. | The LLM must not reason around or reveal these through implication. |
| `reviewer_only_partition` | Information visible to reviewers/auditors but not player/narrator projection. | Must support future auditability without live-play or canon promotion. |
| `dialogue_transcript_candidate` | Dialogue text that may be reviewed as a possible source of claims. | Dialogue is not truth, memory authority, or durable claim by itself. |
| `summary_not_memory_authority` | Summaries used for readability or review compression. | Summaries cannot mutate state or establish memory authority. |
| `durable_claim_pending_review` | Candidate claim awaiting backend/reviewer validation and routing. | Cannot affect truth, context packets, social state, missions, or memory until validated. |

The partition names above are not field names, class names, database table names, Pydantic models, JSON keys, retrieval index record names, prompt blocks, compiler outputs, or live-play packet sections.

## 7. Context-packet handoff contract

Future context-packet work must satisfy these planning-level requirements:

- Context packets are backend-produced projections, not model memory, chat history, transcript state, or LLM-owned continuity.
- Allowed fact sets must be distinguishable from hidden backend truth, redacted facts, reviewer-only notes, derived inferences, rumors, false claims, and pending claims.
- Narrator-facing packet contents must be bounded by scene, actor, visibility, authority, source/provenance status, redaction status, command/event timing, and downstream owner handoffs.
- Hidden facts must not be exposed through summaries, flavor text, apparently likely inference, unstated assumptions, tone, foreshadowing, “the obvious answer,” model speculation, or absence/pattern inference.
- Missing context must trigger clarification, rejection/quarantine routing, or backend lookup; it must not trigger invention.
- Packet outputs must preserve source/provenance references where RT-008 requires projection provenance, source-local status, recurrence eligibility, generated-content status, or durable generated-fact review.
- Packet outputs involving RNG, table, oracle, hidden rows, protected outcomes, seed/replay visibility, or redacted random results must route through RT-009.
- Packet outputs involving command lifecycle, event commitment, rejection/quarantine, scene transition timing, or narration timing must route through RT-001.
- Durable context, memory, claim, dialogue-derived, or summary-derived writes require future persistence ownership and backend/reviewer validation.

This contract does not define final packet fields, packet JSON, packet schemas, retrieval query syntax, compiler code, redaction algorithms, narration validators, prompts, or runtime code.

## 8. Hidden-information and claim contract

RT-005 requires future work to preserve these distinctions:

- Backend truth, player-known facts, character-known facts, NPC/faction beliefs, rumors, false claims, unverified claims, dialogue transcripts, summaries, generated prose, reviewer notes, and source-local draft pressure must remain distinguishable.
- Dialogue may produce a claim candidate only. Dialogue does not create authoritative truth, durable memory, faction state, mission state, clue discovery, or context-packet eligibility by itself.
- Summaries are not memory authority and cannot establish hidden truth, actor knowledge, claim truth, durable recurrence, or source promotion.
- Clues and hidden truths require backend-owned reveal/visibility authorization and must coordinate with RT-006.
- False or unverified information must not be auto-corrected by the model unless the backend provides correction authority to the narrator allowed fact set.
- Hidden NPC, faction, institutional, organized-actor, or creature agendas must remain redacted unless backend context authorizes projection and RT-007 requirements are satisfied.
- Hidden random results require RT-009 ownership and cannot be selected, exposed, or inferred by RT-005 or the LLM.
- Generated recurring facts require RT-008 provenance, recurrence, and durability handoff before they can appear as persistent context.
- Social/faction belief state requires RT-007 before belief, relationship, standing, rumor, obligation, or agenda state can become durable.
- Validation/readiness routes through RT-011.

This contract does not define final claim schema, memory schema, actor-knowledge schema, reveal algorithm, transcript format, summary algorithm, or durable-claim workflow implementation.

## 9. Future context/visibility artifact inventory

The artifact families below are future semantic requirements only. They are not implemented schemas, compilers, fields, formulas, JSON schemas, database schemas, Pydantic models, validators, packet compiler code, retrieval code, runtime code, prompts, persistence writers, or generated records.

| Future artifact family | Purpose | Owner | LLM allowed interaction | Downstream handoff | Implementation status |
|---|---|---|---|---|---|
| `ContextPacketRequirement` | Define future requirements for backend-produced context projections. | RT-005 with RT-001 timing and RT-011 readiness. | Narrate only from approved packet content; ask clarification if insufficient. | RT-001, RT-008, RT-009, RT-011. | `future_required_not_implemented` |
| `VisibleFactRequirement` | Identify future requirements for facts authorized for player/narrator visibility. | RT-005. | Present as approved narration only. | RT-001, RT-006, RT-007, RT-008, RT-011. | `future_required_not_implemented` |
| `HiddenFactRequirement` | Identify future requirements for facts withheld from player/narrator projection. | RT-005 plus source domain owner. | No direct interaction. | RT-003, RT-006, RT-007, RT-009, RT-010, RT-011. | `future_required_not_implemented` |
| `RedactedFactRequirement` | Identify future requirements for partially withheld facts. | RT-005. | Use only approved redacted wording. | RT-008, RT-009, RT-011. | `future_required_not_implemented` |
| `PlayerKnownFactRequirement` | Separate player-known facts from character, NPC, faction, and backend truth. | RT-005. | Summarize visible player-known facts only. | RT-001, RT-007, RT-011. | `future_required_not_implemented` |
| `CharacterKnownFactRequirement` | Separate character-known facts from player-known and backend-known facts. | RT-005 with future actor knowledge ownership. | Narrate only if character perspective is authorized. | RT-007, RT-011. | `future_required_not_implemented` |
| `ActorKnowledgeRequirement` | Plan actor-specific knowledge/belief separation. | RT-007 with RT-005 projection boundary. | No authority; may present authorized visible beliefs. | RT-007, RT-011. | `future_required_not_implemented` |
| `FactionKnowledgeRequirement` | Plan faction/institution knowledge and belief separation. | RT-007 with RT-005 projection boundary. | No authority; may present authorized visible institutional facts. | RT-007, RT-011. | `future_required_not_implemented` |
| `RumorClaimRequirement` | Preserve rumor and unverified-claim status. | RT-005 with RT-007 and RT-008 where applicable. | May repeat only as labeled rumor if approved. | RT-007, RT-008, RT-011. | `future_required_not_implemented` |
| `FalseClaimRequirement` | Preserve false-claim status without auto-correction leakage. | RT-005 with backend/reviewer authority. | May present only if backend authorizes correction or falsehood display. | RT-007, RT-011. | `future_required_not_implemented` |
| `DialogueTranscriptRequirement` | Treat dialogue as candidate evidence, not truth. | Future dialogue/memory owner with RT-005 boundary. | May summarize visible dialogue without converting it to truth. | RT-001, RT-007, RT-011. | `future_required_not_implemented` |
| `SummaryBoundaryRequirement` | Prevent summaries from becoming memory or truth authority. | RT-005 with future persistence/memory owner. | May summarize visible facts as non-authoritative presentation. | RT-011 and future persistence owner. | `future_required_not_implemented` |
| `DurableClaimReviewRequirement` | Route candidate claims to backend/reviewer validation before durability. | Future claim/persistence owner with RT-005 boundary. | No authority; may request review or clarification if backend allows. | RT-007, RT-008, RT-011 and future persistence owner. | `future_required_not_implemented` |
| `NarrationAllowedFactSetRequirement` | Define future requirements for facts allowed in narration. | RT-005. | Narrate within the allowed set only. | RT-001, RT-011. | `future_required_not_implemented` |
| `NarrationForbiddenInferenceRequirement` | Define future requirements for facts/inferences barred from narration. | RT-005. | Must not use or imply forbidden facts. | RT-003, RT-006, RT-007, RT-009, RT-011. | `future_required_not_implemented` |
| `HiddenTruthRevealRequirement` | Plan reveal authorization for hidden truths. | RT-006 with RT-005 visibility boundary. | May narrate reveal only after backend authorization. | RT-006, RT-001, RT-011. | `future_required_not_implemented` |
| `ClueVisibilityRequirement` | Plan clue visibility and non-leakage requirements. | RT-006 with RT-005 projection boundary. | May present clues only when backend approves. | RT-006, RT-009, RT-011. | `future_required_not_implemented` |
| `HiddenRandomResultRedactionRequirement` | Plan redaction/projection of hidden random results. | RT-009 with RT-005 projection boundary. | May present only authorized result projection. | RT-009, RT-001, RT-011. | `future_required_not_implemented` |
| `SourceProvenanceProjectionRequirement` | Preserve source/provenance in context projections where required. | RT-008 with RT-005 packet boundary. | May cite or present source status only as approved. | RT-008, RT-011, RT-012. | `future_required_not_implemented` |
| `ContextPacketValidationRequirement` | Plan future validation of packet boundaries and readiness. | RT-011 with RT-005 requirements. | No validator authority. | RT-011. | `future_required_not_implemented` |

## 10. Validation and readiness requirements

The validation requirements below are future requirements only. They coordinate with RT-011 and do not implement validators, tests, automation, schemas, or runtime checks in this PR:

- Source linkage validation: future packets and partitions must preserve required source/provenance references without promoting source-local material.
- Context/source availability validation: future context production must detect missing context and route to backend lookup, clarification, or quarantine rather than invention.
- Visibility partition coverage validation: future packets must prove visible, hidden, redacted, derived, narrator-facing, player-known, actor-known, faction-known, rumor, false-claim, and reviewer-only seams are covered where relevant.
- Hidden/visible/redacted partition validation: future validators must check that hidden, visible, and redacted facts cannot cross projection boundaries without authorization.
- Narrator allowed/forbidden fact-set validation: future readiness checks must ensure narrator-facing content contains only allowed facts and excludes forbidden inferences.
- Claim/rumor/false-claim separation validation: future checks must distinguish verified facts, rumors, unverified claims, false claims, dialogue candidates, and summaries.
- Dialogue-summary non-authority validation: future checks must prevent transcripts and summaries from becoming truth, memory, discovery, or durable state.
- Clue/hidden-truth reveal boundary validation: future checks must confirm reveal authorization before clues or hidden truths enter allowed narration.
- Hidden random result routing validation: future checks must confirm hidden random outputs route through RT-009 before projection.
- Generated-content provenance handoff validation: future checks must confirm generated recurring facts, source-local facts, and projection eligibility route through RT-008.
- LLM non-authority validation: future checks must prove the model cannot decide hidden truth, visibility, knowledge, clues, oracle outcomes, state mutation, memory, redaction, or canon/training/sourcebook authorization.
- Non-implementation guardrail validation: future review must confirm this owner specification remains planning-only until an implementation PR is separately authorized.

## 11. Downstream handoffs

RT-005 hands off or coordinates as follows:

- RT-001: command lifecycle, event commitment, rejection/quarantine, state-delta timing, scene transition timing, context-packet handoff timing, and narration handoff timing.
- RT-002: hidden or visible resource, cost, consequence, reward, loss, recovery, strain, threshold, corruption, backlash, and overcommitment information.
- RT-003: hidden or visible combat, hazard, damage, injury, recovery, exposure, threat, mitigation, recurrence, and environmental pressure information.
- RT-004: visible or hidden ability, effect, skill, capability, prerequisite, cooldown, resource-binding, secret technique, and hidden capability information.
- RT-006: mission clues, hidden truths, objectives, branches, scenario revelations, protected spoilers, consequence routing, and reward visibility.
- RT-007: actor knowledge, relationship state, NPC/faction beliefs, social standing, obligations, institutional knowledge, rumors, false claims, access, legal/social pressure, and hidden agendas.
- RT-008: generated-content provenance, recurrence, durable generated facts, source-local status, source/provenance retention, projection eligibility, and no-canon/no-training separation.
- RT-009: hidden random results, table/oracle outcomes, hidden rows, protected outcomes, seed/replay visibility, randomness authority, and result redaction.
- RT-010: inventory, item, vehicle, asset visibility, hidden properties, secret cargo, custody, loadout, charges, durability, use state, and vehicle state projection.
- RT-011: validation/readiness governance, reviewer decision records, test-plan posture, failure taxonomy, and non-implementation guardrail review.
- RT-012: D-series/native-design material that may appear as draft design pressure but is not authoritative context, sourcebook material, runtime truth, live-play input, or canon unless explicitly promoted through separate gates.

## 12. LLM non-authority rules

The LLM is explicitly prohibited from:

- deciding what hidden information exists;
- revealing hidden state;
- deciding what a player, character, NPC, or faction knows;
- deciding NPC/faction beliefs as truth;
- selecting or revealing clues;
- selecting or revealing hidden truths;
- selecting oracle/table outcomes;
- inventing backend facts for narration;
- treating narration as discovery;
- treating summaries as memory authority;
- treating dialogue as durable truth;
- mutating scene state;
- compiling context packets;
- choosing redaction boundaries;
- bypassing redaction;
- inferring hidden information from absence or pattern;
- overriding backend validators;
- authorizing canon use, sourcebook use, training use, live-play use, pilot conversion, or source promotion.

The LLM may only narrate committed or approved backend-projected content, summarize visible and validated dialogue history as non-authoritative presentation, interpret player intent into constrained proposals where RT-001 allows it, and ask clarification questions when backend context is insufficient.

## 13. Non-implementation reaffirmation

This PR adds no:

- runtime code;
- schema implementation;
- command IR implementation;
- validator implementation;
- generator implementation;
- persistence writer;
- retrieval index;
- context-packet compiler;
- redaction algorithm;
- narration validator;
- hidden-state database;
- actor-knowledge database;
- memory system;
- RNG, dice, or table implementation;
- event ledger implementation;
- database schema;
- live-play prompt;
- training data;
- donor-content audit;
- canon promotion;
- sourcebook inclusion authorization;
- pilot conversion authorization.

This file is documentation/control planning only. Any later movement from owner specification to implementation requires separate approval, separate ownership, separate readiness checks, and separate review.

## 14. Auditability requirements

Future RT-005-aligned implementation work must be auditable, but this specification does not implement auditing. Future auditability requirements include:

- traceable source/provenance linkage for context facts where RT-008 requires it;
- traceable owner handoff for any context fact sourced from RT-001 through RT-012 dependencies;
- traceable distinction between hidden truth, visible fact, redacted fact, derived inference, rumor, false claim, dialogue transcript, summary, reviewer-only information, and durable claim candidate;
- traceable reason for any reveal, redaction, omission, or narration allowance;
- traceable evidence that hidden facts were not exposed through summaries, flavor, inference, or model speculation;
- traceable reviewer/backend decision record before durable memory, claim, or recurrence authority is granted.

These auditability requirements are future review targets only and do not create audit tooling, event ledgers, databases, validators, schemas, or persistence writers.

## 15. Stage 2 output classification

```yaml
stage2_output:
  stage2_pr_id: STAGE2-PR-D
  track: RT-005
  artifact_type: owner_specification
  implementation_status: non_executable_planning
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_validator_implementation: false
  authorizes_context_packet_compiler: false
  authorizes_redaction_algorithm: false
  authorizes_retrieval_index: false
  authorizes_memory_system: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_canon_promotion: false
  authorizes_pilot_conversion: false
  next_allowed_step: RT-008 owner specification or RT-009 owner specification, pending review
```

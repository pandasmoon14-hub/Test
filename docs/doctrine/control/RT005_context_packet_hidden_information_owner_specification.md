# RT-005 Context-Packet / Hidden-Information Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification only
Tracking ID: REMEDIATION-STAGE2-RT005-CONTEXT-PACKET-HIDDEN-INFORMATION-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-D
Remediation track: RT-005-scene-activity-context-packets
Owner: Astra Doctrine Council / future context-packet and hidden-information control owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-005. It upgrades `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md` into a specification-level planning artifact for context-packet projection, hidden-information ownership, redaction boundaries, visibility partitions, narrator-facing fact-set constraints, and hidden-result routing.

This specification remains non-executable and non-implementation. It defines planning-level ownership seams, handoff obligations, future requirement families, validation/readiness expectations, auditability requirements, and LLM non-authority rules only. It does not authorize runtime implementation, schema implementation, command IR implementation, validator implementation, generator implementation, persistence writer implementation, retrieval index implementation, context-packet compiler implementation, redaction algorithm implementation, narration validator implementation, hidden-state database implementation, live-play prompt implementation, training authorization, donor-content audit, sourcebook inclusion authorization, pilot conversion authorization, or canon promotion.

This specification links to and relies on the following actual repo artifacts:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.
- RT005 owner scaffold: `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md`.
- RT001 owner specification: `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`.
- RT002 owner specification: `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`.
- RT011 owner specification: `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`.

### Source availability disclosure

This Stage 2 PR-D pass used actual repo files only. The requested path `docs/doctrine/operations/batch_b/B01_scene_activity_orchestration_and_runtime_authority_procedure.md` was absent at drafting time; the nearest actual B01 equivalent confirmed present in the repo is `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md`. All other requested planning, audit, current RT owner, context/hidden-info/source-pressure, schema/math/readiness, registry, decision-log, roadmap, and README source files were present at drafting time. This specification does not rewrite B01, B09, C01, C05, C06, C07, C09, C10, SM00, SM01, SM02, the RT scaffolds, RT001 owner specification, RT002 owner specification, RT011 owner specification, or source doctrine.

## 2. Scope

RT-005 owns planning-level governance for context-packet and hidden-information boundaries. Ownership means defining future semantic requirements, authority seams, handoff obligations, validation/readiness needs, redaction boundaries, narrator-facing fact-set constraints, and LLM non-authority rules. Ownership does not mean implementing packet schemas, compilers, redaction algorithms, retrieval indexes, validators, databases, memory systems, runtime code, persistence, prompts, or generators.

RT-005 owns the following planning boundaries:

- hidden-information ownership boundaries;
- context-packet projection boundary requirements;
- visible/hidden/redacted/derived/reviewer-only information partition requirements;
- player-known fact requirements;
- character-known fact requirements;
- NPC/faction-known belief and knowledge requirements;
- rumor, false claim, unverified claim, and verified fact separation requirements;
- dialogue transcript versus summary versus durable claim boundary requirements;
- narrator-facing allowed fact-set requirements;
- narrator-facing forbidden inference-set requirements;
- clue visibility and hidden-truth exposure boundary requirements;
- hidden cost/consequence visibility handoff from RT-002;
- hidden hazard/combat/exposure visibility handoff from RT-003;
- ability/effect visibility and secret capability handoff from RT-004;
- mission/clue/hidden-truth handoff from RT-006;
- social/faction/actor-knowledge handoff from RT-007;
- generated-content projection/provenance handoff from RT-008;
- RNG/table/oracle hidden-result handoff from RT-009;
- inventory/item/vehicle secret-state handoff from RT-010;
- validation/readiness handoff to RT-011;
- D-series/native-design context authority handoff to RT-012;
- auditability requirements for future context-packet, hidden-information, redaction, reveal, claim, rumor, and narration-boundary decisions.

RT-005 preserves pressure from the audit waves, remediation ledger, Stage 2 plan, B01, B09, C01, C05, C06, C07, C09, C10, SM00, SM01, SM02, roadmap, registry, decision log, and README backend-first/model-interchangeability posture without converting those sources into final runtime behavior, schemas, packet fields, or live-play authority.

## 3. Must-not-own boundaries

RT-005 must not own, create, imply, or claim completion of:

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
- RNG/dice/table implementation;
- event ledger implementation;
- database schema;
- live-play prompt implementation;
- training data;
- donor-content audits;
- sourcebook inclusion authorization;
- pilot conversion authorization;
- canon promotion;
- final actor-knowledge schema;
- final rumor/claim schema;
- final memory system.

Any future PR that attempts those outputs must receive separate authorization and must not cite this owner specification as implementation authority.

## 4. Authority model

RT-005 follows a backend-first authority model:

- RT-001 owns command/event lifecycle and when context/narration handoffs occur, including event commitment, rejection, quarantine, clarification routing, and the timing at which a context packet may be prepared for narration.
- RT-002 owns resource/consequence math, while RT-005 owns whether cost/consequence information is visible, redacted, hidden, or narrator-projected after RT-002 and RT-001 have established the relevant committed or withheld outcome boundary.
- RT-011 owns validation/readiness requirements, including future checks that prove this owner specification remains prose planning and is not executable validation, runtime readiness, schema readiness, or live-play authorization.
- Future backend owners own all hidden truth, visibility partitioning, packet production, redaction, retrieval eligibility, reveal authorization, durable memory authority, and persistence authority once separately authorized and implemented.
- The LLM may only narrate from backend-approved allowed fact sets and may ask clarification questions when backend marks the context insufficient.
- LLM memory, summaries, and fluent narration are not state, truth, discovery, or persistence.
- The LLM cannot be the authority for hidden truth, player-known facts, character-known facts, NPC/faction beliefs, rumors, false claims, source provenance, random results, clue visibility, redaction status, durable claims, scene mutation, or future retrieval eligibility.

## 5. Information partition contract

The following conceptual information partitions are planning placeholders only. They are semantic requirement labels for future owner work; they are not final schemas, not database fields, not retrieval index records, not context-packet compiler output, not redaction algorithms, not memory implementation, not runtime state, and not live-play prompts.

| Partition placeholder | Planning meaning | Primary owner/handoff | Non-implementation status |
| --- | --- | --- | --- |
| `backend_truth_partition` | Future protected truth known to backend authority, not to the model by default. | Future backend state/persistence owners with RT-005 projection governance. | `future_required_not_implemented` |
| `player_known_fact_partition` | Future facts authorized as known to the player or table-facing record. | RT-005 with RT-001 event timing and future persistence. | `future_required_not_implemented` |
| `character_known_fact_partition` | Future facts known by a player character or controlled actor. | RT-005 with RT-007 actor-knowledge handoff. | `future_required_not_implemented` |
| `npc_known_fact_partition` | Future facts or beliefs available to an NPC. | RT-007, projected through RT-005. | `future_required_not_implemented` |
| `faction_known_fact_partition` | Future institutional knowledge, beliefs, standing, and obligations. | RT-007, projected through RT-005. | `future_required_not_implemented` |
| `rumor_or_unverified_claim_partition` | Future statements not validated as truth and not automatically corrected. | RT-005 with RT-006/RT-007/RT-008 as applicable. | `future_required_not_implemented` |
| `false_claim_partition` | Future claims known or later reviewed as false without making the model correction authority. | RT-005 with reviewer/backend validation. | `future_required_not_implemented` |
| `hidden_truth_partition` | Future concealed scenario, site, actor, item, or event truth. | Domain owner plus RT-005 reveal/projection governance. | `future_required_not_implemented` |
| `secret_agenda_partition` | Future hidden NPC/faction motives or plans. | RT-007 projected/redacted through RT-005. | `future_required_not_implemented` |
| `hidden_hazard_partition` | Future concealed threat, exposure, damage, injury, recovery, or environmental danger. | RT-003 projected/redacted through RT-005. | `future_required_not_implemented` |
| `hidden_random_result_partition` | Future concealed table/oracle/RNG result or protected replay detail. | RT-009 projected/redacted through RT-005. | `future_required_not_implemented` |
| `redacted_fact_partition` | Future facts withheld or transformed for narrator/player visibility. | RT-005 with domain owner source authority. | `future_required_not_implemented` |
| `derived_inference_partition` | Future derived facts whose derivation and visibility must be backend-approved. | RT-005 with source domain and validation handoff. | `future_required_not_implemented` |
| `narrator_allowed_fact_set` | Future bounded visible facts the LLM may narrate. | RT-005 after backend preparation and RT-001 handoff. | `future_required_not_implemented` |
| `narrator_forbidden_inference_set` | Future facts, patterns, absences, or implications the LLM must not infer or reveal. | RT-005 with RT-011 validation requirements. | `future_required_not_implemented` |
| `reviewer_only_partition` | Future reviewer-facing notes, escalations, or audit materials not player/narrator-facing. | Reviewer/backend governance with RT-011. | `future_required_not_implemented` |
| `dialogue_transcript_candidate` | Future raw or normalized speech record that may yield claim candidates but is not truth. | RT-005 with RT-007 and future persistence review. | `future_required_not_implemented` |
| `summary_not_memory_authority` | Future summary material that can aid review but cannot itself become memory authority. | RT-005 with RT-011 non-authority validation. | `future_required_not_implemented` |
| `durable_claim_pending_review` | Future claim awaiting backend/reviewer validation before durability or projection. | RT-005 with future persistence and RT-011. | `future_required_not_implemented` |

These labels intentionally do not define final fields, formulas, JSON schema, database schema, Pydantic models, validator code, packet compiler code, retrieval code, runtime code, or prompt text.

## 6. Context-packet handoff contract

At planning level, RT-005 requires future context-packet work to obey these constraints:

- Context packets are backend-produced projections, not model memory.
- Allowed fact sets must be distinguishable from hidden backend truth.
- Narrator-facing packet contents must be bounded by scene, actor, visibility, authority, and redaction status.
- Hidden facts must not be exposed through summaries, flavor text, "likely" inference, pattern inference, omission inference, or model speculation.
- Missing context should trigger clarification or backend lookup, not invention.
- Packet outputs must preserve source/provenance references where required by RT-008.
- Packet outputs involving RNG/table/oracle results must route through RT-009.
- Packet outputs involving command lifecycle or event commitment must route through RT-001.
- Packet outputs involving visible or hidden resource/cost/consequence/reward/loss/recovery information must route through RT-002.
- Packet outputs involving combat, hazard, damage, injury, exposure, or threat information must route through RT-003.
- Packet outputs involving abilities, effects, skills, capabilities, prerequisites, cooldowns, or secret techniques must route through RT-004.
- Packet outputs involving mission clues, objectives, branches, hidden truths, scenario revelations, or reward visibility must route through RT-006.
- Packet outputs involving social standing, relationship state, NPC/faction beliefs, actor knowledge, obligations, rumors, or agendas must route through RT-007.
- Packet outputs involving inventory, items, vehicles, assets, hidden properties, secret cargo, custody, loadout, charges, durability, or vehicle state must route through RT-010.
- Durable context/memory writes require future persistence ownership and reviewer/backend validation.

This contract does not define final packet fields, JSON schema, retrieval query syntax, compiler code, redaction algorithm, or live-play prompt.

## 7. Hidden-information and claim contract

RT-005 requires future hidden-information and claim work to preserve the following distinctions:

- Backend truth, player-known facts, character-known facts, NPC/faction beliefs, rumors, false claims, dialogue transcripts, summaries, and generated prose must remain distinguishable.
- Dialogue may produce a claim candidate only, not authoritative truth.
- Summaries are not memory authority.
- Generated prose is not discovery, state mutation, player knowledge, NPC knowledge, faction knowledge, memory, or persistence.
- Clues and hidden truths require backend-owned reveal/visibility authorization.
- False or unverified information must not be auto-corrected by the model unless the backend provides correction authority.
- Hidden NPC/faction agendas must remain redacted unless backend context authorizes projection.
- Hidden random results require RT-009.
- Generated recurring facts require RT-008.
- Social/faction belief state requires RT-007.
- Validation/readiness routes through RT-011.

This contract does not define a final claim schema, memory schema, actor-knowledge schema, reveal algorithm, redaction algorithm, hidden-state database, actor-knowledge database, retrieval index, or context-packet compiler.

## 8. Future context/visibility artifact inventory

The following future artifact families are semantic requirements only, not implemented schemas or compilers. Every row has implementation status `future_required_not_implemented` and cannot be cited as final fields, formulas, JSON schema, database schema, Pydantic models, validator code, packet compiler code, retrieval code, runtime code, memory implementation, redaction algorithm, or live-play prompt. These rows are not final fields, not implemented schemas or compilers, and not runtime code.

| Future artifact family | Purpose | Owner | LLM allowed interaction | Downstream handoff | Implementation status |
| --- | --- | --- | --- | --- | --- |
| `ContextPacketRequirement` | Require future backend-produced packet projection rules and packet authority boundaries. | RT-005. | May narrate only approved allowed facts or ask clarification when marked insufficient. | RT-001, RT-008, RT-011. | `future_required_not_implemented` |
| `VisibleFactRequirement` | Require future distinction for facts authorized for player/narrator visibility. | RT-005 with source domain owner. | May describe approved visible facts. | RT-001, RT-011. | `future_required_not_implemented` |
| `HiddenFactRequirement` | Require future treatment for protected backend truth and non-projection. | RT-005 with source domain owner. | No hidden-fact access or inference authority. | RT-003, RT-006, RT-007, RT-009, RT-010, RT-011. | `future_required_not_implemented` |
| `RedactedFactRequirement` | Require future redaction status and redacted projection obligations. | RT-005. | May narrate only backend-approved redacted presentation. | RT-011 and source domain owners. | `future_required_not_implemented` |
| `PlayerKnownFactRequirement` | Require future player-known fact visibility boundary. | RT-005. | May restate approved player-known facts. | RT-001, future persistence, RT-011. | `future_required_not_implemented` |
| `CharacterKnownFactRequirement` | Require future character-known fact boundary separate from player-known and backend truth. | RT-005 with RT-007. | May narrate approved character-perspective facts. | RT-007, RT-011. | `future_required_not_implemented` |
| `ActorKnowledgeRequirement` | Require future actor knowledge and belief separation. | RT-007 with RT-005 projection. | May portray only approved visible actor knowledge. | RT-007, RT-011. | `future_required_not_implemented` |
| `FactionKnowledgeRequirement` | Require future faction/institution knowledge and belief boundary. | RT-007 with RT-005 projection. | May narrate only approved visible faction statements. | RT-007, RT-011. | `future_required_not_implemented` |
| `RumorClaimRequirement` | Require future handling for rumors and unverified claims without truth promotion. | RT-005 with RT-006/RT-007. | May present only as authorized rumor/unverified claim. | RT-006, RT-007, RT-011. | `future_required_not_implemented` |
| `FalseClaimRequirement` | Require future false-claim preservation without model correction authority. | RT-005 with reviewer/backend validation. | May present only if backend authorizes the claim status. | RT-007, RT-011. | `future_required_not_implemented` |
| `DialogueTranscriptRequirement` | Require future transcript-to-claim boundary. | RT-005 with RT-007/future persistence. | May summarize transcript only when approved and not as truth. | RT-007, RT-011. | `future_required_not_implemented` |
| `SummaryBoundaryRequirement` | Require future proof that summaries are not memory authority. | RT-005 with RT-011. | May summarize visible facts only; summary is not durable authority. | RT-011 and future persistence. | `future_required_not_implemented` |
| `DurableClaimReviewRequirement` | Require future backend/reviewer review before a claim becomes durable. | RT-005 with future persistence and RT-011. | No durability authority. | RT-011, future persistence. | `future_required_not_implemented` |
| `NarrationAllowedFactSetRequirement` | Require future bounded narrator allowed fact sets. | RT-005. | May narrate exactly within approved set. | RT-001, RT-011. | `future_required_not_implemented` |
| `NarrationForbiddenInferenceRequirement` | Require future forbidden inference boundaries, including absence/pattern speculation. | RT-005. | Must not infer, reveal, or speculate. | RT-011. | `future_required_not_implemented` |
| `HiddenTruthRevealRequirement` | Require future backend reveal authorization for concealed truths. | RT-005 with RT-006/domain owner. | May reveal only after backend authorization. | RT-006, RT-011. | `future_required_not_implemented` |
| `ClueVisibilityRequirement` | Require future clue visibility and clue-routing boundary. | RT-006 with RT-005 projection. | May mention only authorized visible clues. | RT-006, RT-011. | `future_required_not_implemented` |
| `HiddenRandomResultRedactionRequirement` | Require future routing/redaction for hidden table/oracle outcomes. | RT-009 with RT-005 projection. | No outcome selection or hidden-result reveal authority. | RT-009, RT-011. | `future_required_not_implemented` |
| `SourceProvenanceProjectionRequirement` | Require future source/provenance references on projected generated or source-local facts. | RT-008 with RT-005 projection. | May cite/summarize only approved provenance-bearing facts. | RT-008, RT-011. | `future_required_not_implemented` |
| `ContextPacketValidationRequirement` | Require future validation/readiness coverage for packet projection, partitioning, and guardrails. | RT-011 with RT-005 requirements. | May not validate itself. | RT-011. | `future_required_not_implemented` |

## 9. Validation and readiness requirements

These validation/readiness requirements are future requirements only. RT-005 coordinates with RT-011, but this specification does not implement validators, tests-as-runtime-gates, schemas, compilers, redaction algorithms, narration validators, retrieval indexes, databases, or runtime code.

Future RT-005 validation planning must cover:

- source linkage validation;
- context/source availability validation;
- visibility partition coverage validation;
- hidden/visible/redacted partition validation;
- narrator allowed/forbidden fact-set validation;
- claim/rumor/false-claim separation validation;
- dialogue-summary non-authority validation;
- clue/hidden-truth reveal boundary validation;
- hidden random result routing validation;
- generated-content provenance handoff validation;
- LLM non-authority validation;
- non-implementation guardrail validation.

RT-011 remains the owner for readiness classifications, validator authorization gates, dependency-skip reporting, registry/file tracking checks, and proof that prose owner specifications are not executable validation.

## 10. Downstream handoffs

RT-005 must coordinate with every runtime track that can generate visible, hidden, redacted, derived, narrator-facing, player-known, actor-known, rumor, false-claim, reviewer-only, or source-local information:

- RT-001: command lifecycle, event commitment, rejection/quarantine, clarification, and context/narration handoff timing.
- RT-002: hidden or visible resource, cost, consequence, reward, loss, recovery, repair, and economy-pressure information.
- RT-003: hidden/visible combat, hazard, damage, injury, recovery, exposure, threat, environmental pressure, and danger-cue information.
- RT-004: visible/hidden ability, effect, skill, capability, prerequisite, cooldown, secret technique, and concealed capability information.
- RT-006: mission clues, hidden truths, objectives, branches, scenario revelations, rewards, losses, and reward visibility.
- RT-007: actor knowledge, relationship state, NPC/faction beliefs, social standing, obligations, rumors, hidden agendas, and faction/institution knowledge.
- RT-008: generated-content provenance, recurrence, durable generated facts, source-local status, donor/source pressure, and projection eligibility.
- RT-009: hidden random results, table/oracle outcomes, seed/replay visibility, protected rows, result redaction, and generated random-output projection.
- RT-010: inventory/item/vehicle/asset visibility, hidden properties, secret cargo, custody, loadout, charges, durability, attachments, platforms, and vehicle state projection.
- RT-011: validation/readiness governance, future validator requirement ownership, dependency skip reporting, registry/file tracking, and non-implementation guardrail checks.
- RT-012: D-series/native-design material that may appear as draft pressure but not authoritative context unless explicitly promoted by separate sourcebook/canon authorization.

## 11. LLM non-authority rules

RT-005 explicitly prohibits the LLM from:

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
- authorizing canon/sourcebook/training/live-play use.

The LLM may propose phrasing, summarize backend-approved visible material, and ask clarification questions when backend context is insufficient. Those allowed interactions never become state, truth, discovery, validation, persistence, memory authority, redaction authority, sourcebook authorization, training authorization, live-play authorization, or canon promotion.

## 12. Non-implementation reaffirmation

This Stage 2 PR-D owner specification adds no:

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
- RNG/dice/table implementation;
- event ledger implementation;
- database schema;
- live-play prompt;
- training data;
- donor-content audit;
- canon promotion;
- sourcebook inclusion authorization;
- pilot conversion authorization.

It also adds no final context-packet schema, hidden-state database schema, actor-knowledge schema, final rumor/claim schema, final memory system, final packet fields, retrieval query syntax, live-play adapter prompt, donor PDF audit, donor book audit, source doctrine rewrite, pilot conversion authorization, or canon/sourcebook promotion.

## 13. Stage 2 output classification

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

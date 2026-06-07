# RUNTIME-SEQ-PR-E: Model Evaluation, Structured-Output, and Adversarial-Command Plan

**Review ID:** RUNTIME-SEQ-PR-E-MODEL-EVALUATION-STRUCTURED-OUTPUT-ADVERSARIAL-COMMAND-PLAN-001
**Date:** 2026-06-06
**Status:** Planning-only, non-executable
**Artifact type:** Model evaluation, structured-output, and adversarial-command plan
**Primary owner tracks:** RT-005, RT-011, RT-012
**Supporting owner tracks:** RT-001, RT-002, RT-003, RT-004, RT-006, RT-007, RT-008, RT-009, RT-010

---

## 1. Purpose and status

This is RUNTIME-SEQ-PR-E, a model evaluation, structured-output, and adversarial-command plan.

It is **planning-only** and **non-executable**.

It defines future model evaluation, structured-output, adversarial-command, metamorphic-test, role-qualification, failure-routing, and model-behavior fingerprint contracts, but it does **not** implement:

- model evaluation code;
- benchmark runner;
- prompt templates;
- model routing;
- model adapter;
- structured-output schema;
- schema-key validator;
- adversarial test harness;
- metamorphic test runner;
- training data;
- runtime code;
- command IR;
- state store;
- event ledger;
- context-packet compiler;
- redaction algorithm;
- live-play adapter;
- donor-content audit;
- pilot conversion;
- sourcebook inclusion;
- canon promotion.

All content in this document is planning-level contract definition. Implementation requires separate, explicitly authorized PRs.

---

## 2. Source ledger

This plan draws on the following source artifacts:

| Artifact ID | Path | Status |
|---|---|---|
| RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001 | `docs/doctrine/reviews/runtime_schema_implementation_sequencing_review.md` | Present |
| RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_a_minimum_backend_kernel_runtime_quality_contract_plan.md` | Present |
| RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_b_narration_context_packet_contract_plan.md` | Present |
| RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_c_state_event_invariant_transaction_plan.md` | Present |
| RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_d_story_capable_structure_playable_content_plan.md` | Present |
| RT-001 Command Lifecycle / Action Legality Owner Specification | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md` | Present |
| RT-002 Resource / Consequence Math Owner Specification | `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md` | Present |
| RT-003 Combat / Hazard / Damage / Recovery Owner Specification | `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md` | Present |
| RT-004 Ability / Effect / Skill Binding Owner Specification | `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md` | Present |
| RT-005 Context Packet / Hidden Information Owner Specification | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md` | Present |
| RT-006 Mission / Reward / Clue Routing Owner Specification | `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md` | Present |
| RT-007 Social / Faction / Actor Knowledge Owner Specification | `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md` | Present |
| RT-008 Generated Content / Provenance / Recurrence Owner Specification | `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md` | Present |
| RT-009 Runtime RNG / Table / Oracle Owner Specification | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md` | Present |
| RT-010 Inventory / Item / Vehicle / Asset Owner Specification | `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md` | Present |
| RT-011 Validation / Readiness / Tooling Owner Specification | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md` | Present |
| RT-012 D-Series / Promotion Boundary Owner Specification | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md` | Present |
| Runtime Boundary Generator Ownership Audit Protocol | `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md` | Present |
| Stage 2 Completion Review and Closure Ledger | `docs/doctrine/reviews/runtime_boundary_generator_ownership_stage2_completion_review_and_closure_ledger.md` | Present |
| SM00 Schema Math Mechanics Master Scope and Sequencing Plan | `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` | Present |
| SM01 Validation Schema Inventory and Readiness Controls | `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md` | Present |
| SM02 Minimum Pilot Conversion Readiness and Packet Validation Controls | `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md` | Present |
| C00 Shared Content Record Base and Schema Registry | `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` | Present |
| C01–C14 Content Record Schemas | `docs/doctrine/schema/C01_creature_npc_record_schema.md` through `docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md` | Present |
| Astra Doctrine Roadmap v0.1 | `docs/doctrine/astra_doctrine_roadmap_v0_1.md` | Present |
| Astra Doctrine Registry v0.1 | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` | Present |
| Current Decisions Log | `docs/decisions/current_decisions_log.md` | Present |
| README | `README.md` | Present |
| Astra Evaluation and Benchmark Pack | `docs/doctrine/astra_evaluation_and_benchmark_pack.md` | **Not present** |
| Evaluation directory | `docs/doctrine/evaluation/` | **Not present** |

Primary owner tracks for this plan:

- **RT-005** — context-packet / hidden-information owner. Model evaluation must test hidden-info discipline.
- **RT-011** — validation / readiness / tooling owner. Model role qualification is a readiness gate.
- **RT-012** — D-series / promotion boundary owner. Model outputs must respect source-local / canon / sourcebook / training boundaries.

---

## 3. Backend-first invariant

Astra Ascension must be **model-interchangeable**. The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

**Model-evaluation implication:**

No model is trusted because it is powerful, fluent, local, cloud-hosted, fine-tuned, uncensored, cheap, fast, or aesthetically good. A model is eligible for a role only if future evaluation proves it can obey the role's packet contract, output contract, hidden-information limits, structured-output constraints, and non-authority boundaries.

A model that generates beautiful prose but leaks hidden information is ineligible. A model that follows every instruction but invents mechanics is ineligible. A model that produces perfect structured output but promotes source-local content to canon is ineligible. Eligibility is earned through evaluation, not assumed from capability.

---

## 4. Model role taxonomy

The following model roles are defined as future planning concepts. None are implemented.

### 4.1. local_8b_narrator

- **Purpose:** Render narration prose from NarrationRenderPacket facts for player-facing output.
- **Allowed packet inputs:** NarrationRenderPacket only.
- **Allowed outputs:** Narration prose with structured metadata (output_type, model_role, source_packet_ref, visible_facts_used, uncertainty_flags, hidden_info_risk_flags, soft_state_risk_flags, invented_fact_risk_flags, schema_completion_status, continuation_required).
- **Forbidden authority:** May not invent mechanics, reveal hidden information, create state, roll dice, assign rewards, mutate NPC goals, promote content, bypass costs, or act as GM.
- **Required evaluation gates:** Narration faithfulness, hidden-info discipline, soft-state mutation, packet-budget obedience, truncation-safe output, style-under-constraint.
- **Failure modes to test:** Hidden-info leakage, invented mechanics, invented rewards, soft-state mutation, overbroad narration, truncation data loss, GM behavior.
- **Implementation status:** future_required_not_implemented.

### 4.2. local_8b_intent_parser

- **Purpose:** Extract structured intent proposals from player commands.
- **Allowed packet inputs:** IntentParsingPacket only.
- **Allowed outputs:** Structured intent proposals with intent_proposals, clarification_questions, uncertainty_flags, boundary_refusal.
- **Forbidden authority:** May not invent mechanics, resolve actions, commit state, assign costs, grant rewards, or bypass legality checks.
- **Required evaluation gates:** Command intent extraction accuracy, ambiguity detection, no-mechanics-invention, structured intent proposal format compliance.
- **Failure modes to test:** Command IR confusion, invented mechanics, false certainty, action resolution, cost/reward invention.
- **Implementation status:** future_required_not_implemented.

### 4.3. local_8b_clarification_assistant

- **Purpose:** Generate procedural clarification questions when player commands are ambiguous or incomplete.
- **Allowed packet inputs:** ClarificationPacket only.
- **Allowed outputs:** Clarification questions with uncertainty_flags, needs_backend_context.
- **Forbidden authority:** May not invent state, resolve ambiguity by assumption, grant information the player has not earned, or commit any state change.
- **Required evaluation gates:** Procedural question quality, no-state-invention, missing-information handling.
- **Failure modes to test:** State invention, hidden-info leakage, false certainty, assumption-based resolution.
- **Implementation status:** future_required_not_implemented.

### 4.4. local_8b_visible_summary_assistant

- **Purpose:** Produce visible-only summaries of game state for player reference.
- **Allowed packet inputs:** SummaryPacket only.
- **Allowed outputs:** Summary text with visible_facts_used, hidden_info_risk_flags.
- **Forbidden authority:** May not serve as memory authority, reveal hidden information, promote summaries to event status, or create new state.
- **Required evaluation gates:** Summary-not-memory-authority, visible-only recap, hidden-info discipline, no-state-creation.
- **Failure modes to test:** Hidden-info leakage, memory-authority claims, state invention, fact invention, summary-as-canon.
- **Implementation status:** future_required_not_implemented.

### 4.5. api_reflective_summarizer

- **Purpose:** Produce longer-context summarization for review, audit, and reflective analysis.
- **Allowed packet inputs:** SummaryPacket or EvaluationPacket (scoped per task).
- **Allowed outputs:** Summary text with source separation markers, uncertainty_flags, no-promotion markers.
- **Forbidden authority:** May not promote summaries to canon, create doctrine, assign authority to analyzed content, or merge source boundaries.
- **Required evaluation gates:** Longer-context summarization accuracy, source separation, no-promotion discipline.
- **Failure modes to test:** Source-boundary merging, canon promotion, doctrine invention, authority escalation.
- **Implementation status:** future_required_not_implemented.

### 4.6. api_evaluator_or_judge

- **Purpose:** Evaluate content against rubrics, grade submissions, and provide structured judgments.
- **Allowed packet inputs:** EvaluationPacket only.
- **Allowed outputs:** Evaluation judgments with rubric_scores, evidence_refs, uncertainty_flags, boundary_refusal.
- **Forbidden authority:** May not commit evaluation results as backend truth, escalate own authority, create backdoor commitments, or bypass reviewer oversight.
- **Required evaluation gates:** Rubric adherence, evidence grounding, no-authority-escalation, no-backdoor-commitment.
- **Failure modes to test:** Authority escalation, backdoor commitment, rubric drift, evidence fabrication, self-referential scoring.
- **Implementation status:** future_required_not_implemented.

### 4.7. api_canon_or_sourcebook_drafter

- **Purpose:** Draft canon or sourcebook content for human review and explicit promotion.
- **Allowed packet inputs:** EvaluationPacket with drafting scope.
- **Allowed outputs:** Draft content with authority_hierarchy markers, source_boundary markers, promotion_status (always: draft_pending_review).
- **Forbidden authority:** May not promote content to canon without review, merge source-local into canon, bypass promotion gates, or create self-authorizing content.
- **Required evaluation gates:** Authority hierarchy obedience, canon/sourcebook boundary discipline, no-promotion-without-review, source-local separation.
- **Failure modes to test:** Self-promotion, source-local/canon merger, promotion-gate bypass, authority hierarchy violation.
- **Implementation status:** future_required_not_implemented.

### 4.8. conversion_assistant

- **Purpose:** Assist with donor-content conversion under lawful outcome taxonomy constraints.
- **Allowed packet inputs:** Conversion-scoped packet (future definition).
- **Allowed outputs:** Conversion proposals with lawful_outcome_tags, donor_assumption_flags, source_local_retention_markers, quarantine_markers.
- **Forbidden authority:** May not promote donor content to canon, bypass quarantine, assume donor authority, or skip lawful outcome taxonomy.
- **Required evaluation gates:** Lawful outcome taxonomy adherence, donor-assumption quarantine, source-local retention, no-canon-promotion.
- **Failure modes to test:** Canon promotion, quarantine bypass, donor-assumption leakage, lawful-outcome skip, source-local/canon merger.
- **Implementation status:** future_required_not_implemented.

### 4.9. backend_validator

- **Purpose:** Validate backend state, schemas, and invariants.
- **Allowed packet inputs:** N/A — this is a backend-owned role.
- **Allowed outputs:** N/A — backend-owned.
- **Forbidden authority:** N/A — backend-owned.
- **Required evaluation gates:** N/A — not an LLM role.
- **Failure modes to test:** N/A.
- **Implementation status:** future_required_not_implemented.

### 4.10. backend_packet_compiler

- **Purpose:** Compile context packets from backend state for model consumption.
- **Allowed packet inputs:** N/A — this is a backend-owned role.
- **Allowed outputs:** N/A — backend-owned.
- **Forbidden authority:** N/A — backend-owned.
- **Required evaluation gates:** N/A — not an LLM role.
- **Failure modes to test:** N/A.
- **Implementation status:** future_required_not_implemented.

**Note:** backend_validator and backend_packet_compiler are **not** LLM roles unless a future architecture explicitly authorizes a constrained assistant role. Backend validation and packet compilation remain backend-owned. If a future architecture introduces LLM assistance for these roles, that authorization must be explicit and separately evaluated.

---

## 5. ModelBehaviorFingerprint contract

The following defines the future ModelBehaviorFingerprint as a planning concept. It is not implemented.

A ModelBehaviorFingerprint evaluates a model across the following dimensions:

### 5.1. Instruction adherence

- **What it measures:** Whether the model follows explicit packet-level and role-level instructions.
- **Why it matters for Astra:** Every model role operates under constraints. A model that ignores instructions cannot be trusted in any role.
- **Affected model roles:** All LLM roles.
- **Status:** future_required_not_implemented.

### 5.2. Packet-boundary obedience

- **What it measures:** Whether the model confines its output to facts present in its input packet and does not reference information from other packets, prior turns, or its training data.
- **Why it matters for Astra:** Packet boundaries enforce visibility tiers (RT-005) and prevent hidden-info leakage.
- **Affected model roles:** All LLM roles.
- **Status:** future_required_not_implemented.

### 5.3. Hidden-information discipline

- **What it measures:** Whether the model avoids revealing hidden state, private NPC motives, unrevealed clues, locked rewards, or information not present in the visible portion of the packet.
- **Why it matters for Astra:** RT-005 defines hidden-information ownership. A model that leaks hidden info breaks game integrity.
- **Affected model roles:** local_8b_narrator, local_8b_intent_parser, local_8b_clarification_assistant, local_8b_visible_summary_assistant.
- **Status:** future_required_not_implemented.

### 5.4. Schema-key obedience

- **What it measures:** Whether the model produces outputs with correct, stable, fully-spelled schema keys and does not invent, omit, or misspell required fields.
- **Why it matters for Astra:** Downstream parsers depend on schema-key stability. Invented keys create phantom state.
- **Affected model roles:** All LLM roles producing structured output.
- **Status:** future_required_not_implemented.

### 5.5. Structured-output completeness

- **What it measures:** Whether the model produces all required structured fields before optional prose content.
- **Why it matters for Astra:** Incomplete structured output cannot be validated. Missing metadata fields make output unparseable.
- **Affected model roles:** All LLM roles producing structured output.
- **Status:** future_required_not_implemented.

### 5.6. Structured-output stability

- **What it measures:** Whether the model produces consistent structured output format across repeated runs with the same input.
- **Why it matters for Astra:** Unstable output format creates validation flakiness and parser failures.
- **Affected model roles:** All LLM roles producing structured output.
- **Status:** future_required_not_implemented.

### 5.7. Truncation behavior

- **What it measures:** Whether the model preserves critical metadata fields when output is truncated by token limits.
- **Why it matters for Astra:** Local 8B models under packet pressure may truncate. Critical fields (output_type, model_role, source_packet_ref, risk flags) must survive truncation.
- **Affected model roles:** local_8b_narrator, local_8b_intent_parser, local_8b_clarification_assistant, local_8b_visible_summary_assistant.
- **Status:** future_required_not_implemented.

### 5.8. Refusal/boundary behavior

- **What it measures:** Whether the model correctly refuses requests that exceed its role authority and reports the refusal in structured output.
- **Why it matters for Astra:** Models must refuse to act as GM, reveal hidden info, or commit state. Silent compliance with overreach is a critical failure.
- **Affected model roles:** All LLM roles.
- **Status:** future_required_not_implemented.

### 5.9. Hallucinated mechanics rate

- **What it measures:** How often the model invents game mechanics, rules, abilities, costs, or resolution procedures not present in the input packet or committed state.
- **Why it matters for Astra:** Invented mechanics create false player expectations and corrupt game logic. RT-001 through RT-004 own mechanics.
- **Affected model roles:** local_8b_narrator, local_8b_intent_parser, api_evaluator_or_judge.
- **Status:** future_required_not_implemented.

### 5.10. Soft-state mutation rate

- **What it measures:** How often the model's output implies or asserts state changes that were not committed by the backend (e.g., "you now have 5 gold" when no transaction occurred).
- **Why it matters for Astra:** Soft-state mutation undermines backend truth. Players may believe narrated state is real state.
- **Affected model roles:** local_8b_narrator, local_8b_visible_summary_assistant.
- **Status:** future_required_not_implemented.

### 5.11. Invented reward/clue/item/faction/action rate

- **What it measures:** How often the model invents rewards, clues, items, factions, or actions not present in the input packet.
- **Why it matters for Astra:** RT-006 (mission/reward/clue), RT-007 (social/faction), RT-010 (inventory/item) own these domains. Invention bypasses backend authority.
- **Affected model roles:** local_8b_narrator, local_8b_intent_parser, api_evaluator_or_judge.
- **Status:** future_required_not_implemented.

### 5.12. Actor-knowledge leakage rate

- **What it measures:** How often the model gives an NPC knowledge that the NPC should not have according to actor-knowledge state (RT-007).
- **Why it matters for Astra:** Actor-knowledge leakage breaks information asymmetry, a core TTRPG principle.
- **Affected model roles:** local_8b_narrator.
- **Status:** future_required_not_implemented.

### 5.13. Source-local/canon boundary obedience

- **What it measures:** Whether the model treats source-local content as source-local and does not promote it to canon or global authority (RT-012).
- **Why it matters for Astra:** Source-local content is donor-specific. Promotion to canon requires explicit review and authorization.
- **Affected model roles:** All LLM roles, especially api_canon_or_sourcebook_drafter and conversion_assistant.
- **Status:** future_required_not_implemented.

### 5.14. Command-intent parsing accuracy

- **What it measures:** Whether the model correctly extracts player intent from natural-language commands and maps them to structured intent proposals.
- **Why it matters for Astra:** Incorrect intent parsing leads to wrong actions. RT-001 owns command lifecycle.
- **Affected model roles:** local_8b_intent_parser.
- **Status:** future_required_not_implemented.

### 5.15. Narration faithfulness to packet facts

- **What it measures:** Whether narration prose accurately reflects the facts in the NarrationRenderPacket without addition, omission, or distortion.
- **Why it matters for Astra:** Unfaithful narration misleads players and creates divergence between state and perception.
- **Affected model roles:** local_8b_narrator.
- **Status:** future_required_not_implemented.

### 5.16. Narration quality under small packet constraints

- **What it measures:** Whether the model can produce acceptable narration when the input packet is small or sparse.
- **Why it matters for Astra:** Local 8B models may receive trimmed packets. Quality must not collapse to filler, repetition, or invention.
- **Affected model roles:** local_8b_narrator.
- **Status:** future_required_not_implemented.

### 5.17. Consistency under repeated runs

- **What it measures:** Whether the model produces consistent outputs (same facts, same structure, compatible tone) when given the same input packet multiple times.
- **Why it matters for Astra:** Replay and audit depend on consistency. Wild variation across runs undermines trust.
- **Affected model roles:** All LLM roles.
- **Status:** future_required_not_implemented.

### 5.18. Degradation under longer packets

- **What it measures:** Whether the model's guardrail compliance degrades as input packet size increases.
- **Why it matters for Astra:** Longer packets may push models past their reliable attention range. Guardrail degradation is a disqualifying failure.
- **Affected model roles:** All LLM roles, especially local_8b_narrator.
- **Status:** future_required_not_implemented.

### 5.19. Recovery from missing information

- **What it measures:** Whether the model asks for clarification or flags uncertainty when information is absent from the packet, rather than inventing facts.
- **Why it matters for Astra:** Invention under uncertainty is the most common model failure mode in constrained environments.
- **Affected model roles:** All LLM roles.
- **Status:** future_required_not_implemented.

### 5.20. Ability to ask procedural clarification

- **What it measures:** Whether the model can generate well-formed procedural clarification questions when player intent is ambiguous.
- **Why it matters for Astra:** Clarification prevents wrong-action commits.
- **Affected model roles:** local_8b_intent_parser, local_8b_clarification_assistant.
- **Status:** future_required_not_implemented.

### 5.21. Tendency to over-author or become GM

- **What it measures:** Whether the model drifts from its assigned role into game-mastering behavior — deciding outcomes, revealing plot, making NPC decisions, or narrating consequences that require backend commitment.
- **Why it matters for Astra:** The LLM is not the game engine. GM behavior is a role-disqualifying failure.
- **Affected model roles:** All LLM roles, especially local_8b_narrator.
- **Status:** future_required_not_implemented.

**Threshold policy:** This plan does not define final numeric thresholds for any fingerprint dimension. The repo does not currently define thresholds. Future calibration is required before any model can be qualified for a runtime role.

---

## 6. Role qualification contract

A model must **not** be assigned a runtime role until it passes future role-specific gates.

### 6.1. local_8b_narrator gates

- Narration faithfulness test.
- Hidden-info discipline test.
- Soft-state mutation test.
- Packet-budget obedience test.
- Truncation-safe output test.
- Style-under-constraint test.

### 6.2. local_8b_intent_parser gates

- Command intent extraction accuracy test.
- Ambiguity detection test.
- No-mechanics-invention test.
- Structured intent proposal format compliance test.

### 6.3. local_8b_clarification_assistant gates

- Procedural question quality test.
- No-state-invention test.
- Missing-information handling test.

### 6.4. local_8b_visible_summary_assistant gates

- Summary-not-memory-authority test.
- Visible-only recap test.

### 6.5. api_reflective_summarizer gates

- Longer-context summarization accuracy test.
- Source separation test.
- No-promotion test.

### 6.6. api_evaluator_or_judge gates

- Rubric adherence test.
- Evidence grounding test.
- No-authority-escalation test.
- No-backdoor-commitment test.

### 6.7. api_canon_or_sourcebook_drafter gates

- Authority hierarchy obedience test.
- Canon/sourcebook boundary discipline test.
- No-promotion-without-review test.
- Source-local separation test.

### 6.8. conversion_assistant gates

- Lawful outcome taxonomy adherence test.
- Donor-assumption quarantine test.
- Source-local retention test.
- No-canon-promotion test.

Role qualification is **future governance planning only**, not implemented here.

---

## 7. Structured-output contract

Future model outputs may need structured sections such as:

- **output_type** — type of output produced (narration, intent_proposals, summary, evaluation, clarification, refusal).
- **model_role** — which model role produced this output.
- **source_packet_ref** — reference to the input packet that produced this output.
- **visible_facts_used** — list of visible facts from the packet that the output references.
- **intent_proposals** — structured intent proposals extracted from player commands.
- **clarification_questions** — procedural clarification questions for ambiguous input.
- **narration_text** — narration prose for player-facing display.
- **summary_text** — summary text for recap or review.
- **uncertainty_flags** — flags indicating where the model was uncertain.
- **needs_backend_context** — flags indicating the model needs additional backend context.
- **soft_state_risk_flags** — flags indicating potential soft-state mutation in the output.
- **hidden_info_risk_flags** — flags indicating potential hidden-information leakage.
- **invented_fact_risk_flags** — flags indicating potential invented facts.
- **boundary_refusal** — structured refusal when a request exceeds role authority.
- **schema_completion_status** — whether all required schema fields are present.
- **continuation_required** — whether the output was truncated and continuation is needed.

**Structured-output invariants:**

- Structured output is **not** backend truth.
- Structured output is **not** event commitment.
- Structured output is **not** memory authority.
- Structured output is **not** canon/sourcebook promotion.
- Structured output must be validated before use in any backend-adjacent flow.
- Unparseable structured output must be rejected, retried, or quarantined.
- Truncation-safe output must preserve critical fields before optional prose.

This section does not implement structured-output schema, parser, or validator.

---

## 8. Schema-key behavior evaluation

The following defines the future SchemaKeyBehaviorEvaluationPolicy as a planning concept. It is not implemented.

Schema-key behavior evaluation should test:

- **Required key presence** — all required keys are present in the output.
- **Forbidden key absence** — no forbidden or unauthorized keys appear.
- **Stable key spelling** — key names are spelled consistently across runs.
- **Null/unknown handling** — null and unknown values are handled explicitly, not silently dropped.
- **No hidden keys** — no keys are present that the output contract does not define.
- **No extra state mutation keys** — no keys that imply state changes the model is not authorized to make.
- **No invented schema fields** — no fields appear that are not part of the defined output schema.
- **Valid enum discipline** — once enums are defined, values must be drawn from the defined set.
- **Continuation/resume marker behavior** — continuation markers are well-formed and do not invent facts.
- **Refusal field behavior** — refusal fields are present when the model refuses, and absent when it complies.
- **Uncertainty field behavior** — uncertainty flags are present when the model is uncertain, and not used as false humility.
- **Packet reference preservation** — source_packet_ref is preserved accurately from input to output.

Schema-key behavior testing is required before model outputs can feed command candidates, summaries, evaluator judgments, or live-play narration.

This section does not implement schema tests or parsers.

---

## 9. Truncation-safe structured output policy

The following defines the future TruncationSafeStructuredOutputPolicy as a planning concept.

- Critical metadata must appear before optional prose. The output format must place structured metadata fields at the top, not the bottom.
- The following fields must be prioritized in output ordering: output_type, model_role, source_packet_ref, uncertainty_flags, hidden_info_risk_flags, soft_state_risk_flags, invented_fact_risk_flags, schema_completion_status, continuation_required.
- Local 8B narrator output must be safe under packet pressure. If the model's output token budget is constrained, metadata must survive.
- Partially completed output must not be treated as complete. A truncated output missing continuation_required must be flagged, not silently accepted.
- Continuation requests must not invent new facts. A continuation must resume from the same packet facts, not generate novel content.
- Long narration should be resumable from backend-visible packet facts, not model memory.
- Failed truncation safety should disqualify a model from roles requiring structured output until re-evaluation.

This section does not implement truncation handling or continuation protocol.

---

## 10. Adversarial player-command corpus

The following defines the future AdversarialPlayerCommandCorpus as a planning concept. It is not implemented, and no corpus data is created in this PR.

### 10.1. Hidden-information reveal attempts

- **Target failure mode:** Model reveals hidden state, unrevealed clues, locked rewards, or private NPC motives.
- **Relevant RT owners:** RT-005, RT-006, RT-007.
- **Expected safe behavior:** Model refuses to reveal hidden information; flags uncertainty; reports hidden_info_risk_flags.
- **Implementation status:** future_required_not_implemented.

### 10.2. Cost-bypass attempts

- **Target failure mode:** Model narrates or implies that costs were not incurred when the backend has not waived them.
- **Relevant RT owners:** RT-002, RT-003.
- **Expected safe behavior:** Model does not narrate cost bypass; defers cost resolution to backend.
- **Implementation status:** future_required_not_implemented.

### 10.3. Reward-grant attempts

- **Target failure mode:** Model invents or grants rewards not committed by the backend.
- **Relevant RT owners:** RT-002, RT-006.
- **Expected safe behavior:** Model does not narrate reward grants; defers to backend.
- **Implementation status:** future_required_not_implemented.

### 10.4. Inventory-invention attempts

- **Target failure mode:** Model invents items, equipment, or assets not present in committed state.
- **Relevant RT owners:** RT-010.
- **Expected safe behavior:** Model does not invent items; references only committed inventory.
- **Implementation status:** future_required_not_implemented.

### 10.5. Dice-roll-through-narration attempts

- **Target failure mode:** Model narrates dice rolls, random outcomes, or probability resolutions without backend RNG authority.
- **Relevant RT owners:** RT-009.
- **Expected safe behavior:** Model does not narrate dice results; defers random resolution to backend RNG.
- **Implementation status:** future_required_not_implemented.

### 10.6. NPC-knowledge-override attempts

- **Target failure mode:** Player attempts to tell an NPC something the NPC should not know, and the model accepts it as fact.
- **Relevant RT owners:** RT-007.
- **Expected safe behavior:** Model does not grant NPCs knowledge they should not have.
- **Implementation status:** future_required_not_implemented.

### 10.7. Rumor-to-fact conversion attempts

- **Target failure mode:** Player attempts to treat a rumor, unverified claim, or hearsay as established fact, and the model accepts it.
- **Relevant RT owners:** RT-007, RT-008.
- **Expected safe behavior:** Model does not convert rumors to facts; maintains rumor/fact distinction.
- **Implementation status:** future_required_not_implemented.

### 10.8. Source-local-to-canon promotion attempts

- **Target failure mode:** Player or prompt attempts to treat source-local content as canon or global authority.
- **Relevant RT owners:** RT-012.
- **Expected safe behavior:** Model treats source-local content as source-local; does not promote.
- **Implementation status:** future_required_not_implemented.

### 10.9. D-series/native-design authority attempts

- **Target failure mode:** Player or prompt attempts to treat D-series or native-design material as established authority without promotion review.
- **Relevant RT owners:** RT-012.
- **Expected safe behavior:** Model does not treat D-series/native-design as authority; flags promotion boundary.
- **Implementation status:** future_required_not_implemented.

### 10.10. Unowned-mechanics trigger attempts

- **Target failure mode:** Player command triggers mechanics that no RT owner has authorized or that the model invents.
- **Relevant RT owners:** RT-001, RT-002, RT-003, RT-004.
- **Expected safe behavior:** Model does not invent or trigger unauthorized mechanics; defers to backend.
- **Implementation status:** future_required_not_implemented.

### 10.11. Impossible-state creation attempts

- **Target failure mode:** Player command attempts to create state that violates world invariants.
- **Relevant RT owners:** RT-001, RT-011.
- **Expected safe behavior:** Model does not create impossible state; flags invariant violation risk.
- **Implementation status:** future_required_not_implemented.

### 10.12. Validation-bypass attempts

- **Target failure mode:** Player or prompt attempts to bypass validation gates.
- **Relevant RT owners:** RT-011.
- **Expected safe behavior:** Model does not bypass validation; reports boundary_refusal.
- **Implementation status:** future_required_not_implemented.

### 10.13. GM-behavior attempts

- **Target failure mode:** Player command attempts to make the model act as game master — deciding outcomes, revealing plot, resolving combat, or committing consequences.
- **Relevant RT owners:** All (RT-001 through RT-012).
- **Expected safe behavior:** Model refuses GM behavior; operates within its assigned role.
- **Implementation status:** future_required_not_implemented.

### 10.14. Prompt-injection inside player speech

- **Target failure mode:** Player embeds system-level instructions inside in-character speech to manipulate model behavior.
- **Relevant RT owners:** RT-005, RT-011.
- **Expected safe behavior:** Model does not follow embedded instructions that exceed role authority.
- **Implementation status:** future_required_not_implemented.

### 10.15. Missing-packet-context exploitation

- **Target failure mode:** Player exploits gaps in the input packet to extract information the packet intentionally omits.
- **Relevant RT owners:** RT-005.
- **Expected safe behavior:** Model asks for clarification or flags uncertainty rather than filling gaps with invention.
- **Implementation status:** future_required_not_implemented.

### 10.16. Ambiguity exploitation

- **Target failure mode:** Player exploits ambiguous game state or rules to force the model into committing unauthorized interpretations.
- **Relevant RT owners:** RT-001, RT-004.
- **Expected safe behavior:** Model flags ambiguity and requests backend resolution rather than deciding unilaterally.
- **Implementation status:** future_required_not_implemented.

---

## 11. Metamorphic runtime/narration test plan

The following defines the future MetamorphicRuntimeNarrationTestPlan as a planning concept. It is not implemented.

### 11.1. Packet-fact reorder invariance

Equivalent visible state with reordered packet facts should preserve outcome meaning. The model should not change its behavior based on fact ordering.

### 11.2. Hidden-fact removal invariance

Hidden facts removed from the packet should not appear in narration. If the packet compiler redacts a fact, the model must not reconstruct it from training data or context.

### 11.3. Committed-event summary consistency

The same committed event should produce a consistent visible summary across repeated runs. Summary content may vary in wording but must preserve factual accuracy.

### 11.4. Cosmetic-wording intent invariance

Cosmetic wording changes in player commands should not alter intent parsing. "I attack the goblin" and "I strike at the goblin" should produce equivalent intent proposals.

### 11.5. Source-local label scope invariance

Source-local labels should not become global claims. A source-local setting name referenced in one packet should not bleed into unrelated narration.

### 11.6. Model-provider backend-truth invariance

Changing model provider should not change backend truth. Switching from a local 8B to a cloud API model must produce different prose style but identical backend-relevant structured output.

### 11.7. Repeated-run state invariance

Repeated runs should not create new state. Running the same input packet through the same model role multiple times must not accumulate phantom state.

### 11.8. Packet-size guardrail stability

Increased packet size should not erase guardrails. A model that obeys hidden-info discipline on small packets must still obey it on large packets.

### 11.9. Missing-information clarification invariance

Missing information should produce clarification, not invention. If a fact is absent from the packet, the model should ask or flag, not fabricate.

### 11.10. RNG-backend-reference invariance

Random outcomes should remain tied to backend RNG references. The model must not narrate random results without a backend RNG reference in the packet.

This section does not implement metamorphic tests.

---

## 12. Local/cloud model comparison contract

Future model comparison must evaluate:

- **local_8b_narrator suitability** — can a local 8B model narrate faithfully within packet constraints?
- **local_8b_intent_parser suitability** — can a local 8B model parse intent accurately?
- **API summarizer suitability** — does an API model provide better summarization without source-boundary violations?
- **API evaluator/judge suitability** — does an API model evaluate more reliably with rubric adherence?
- **API drafting suitability** — does an API model draft content with better authority-hierarchy discipline?
- **Latency/quality tradeoffs** — what latency cost does each provider impose, and what quality gain justifies it?
- **Packet-size tolerance** — how much packet content can each model handle before degradation?
- **Structured-output reliability** — how reliably does each model produce parseable structured output?
- **Hidden-info discipline** — does the model provider affect hidden-info leakage rates?
- **Boundary obedience** — does the model provider affect role-boundary obedience?
- **Replay consistency** — does the model provider affect output consistency across replays?
- **Cost/offline constraints** — what is the cost of each provider, and can local models operate offline?
- **Privacy/locality constraints** — does the deployment scenario require local-only inference?

**Model comparison cannot change backend authority.** A stronger model may improve narration or evaluation, but it cannot become the engine. Backend truth is invariant across model providers.

---

## 13. Failure-mode routing

The following defines the future FailureModeRoutingContract as a planning concept. It is not implemented.

### 13.1. malformed_output

- **Future routing options:** retry; reduce packet; switch model; quarantine output.

### 13.2. incomplete_output

- **Future routing options:** retry with continuation marker; reduce packet; switch model; quarantine output.

### 13.3. packet_overflow_failure

- **Future routing options:** reduce packet; retry with trimmed packet; switch model; escalate to backend validation.

### 13.4. hidden_info_leakage

- **Future routing options:** quarantine output; mark model role-ineligible pending further evaluation; escalate to backend validation; require reviewer review.

### 13.5. soft_state_mutation_attempt

- **Future routing options:** quarantine output; retry; mark model role-ineligible pending further evaluation; escalate to backend validation.

### 13.6. invented_mechanic

- **Future routing options:** quarantine output; retry; mark model role-ineligible pending further evaluation.

### 13.7. invented_fact

- **Future routing options:** quarantine output; retry; ask clarification; escalate to backend validation.

### 13.8. invented_reward

- **Future routing options:** quarantine output; mark model role-ineligible pending further evaluation; escalate to backend validation.

### 13.9. invented_clue

- **Future routing options:** quarantine output; mark model role-ineligible pending further evaluation; escalate to backend validation.

### 13.10. invented_item

- **Future routing options:** quarantine output; mark model role-ineligible pending further evaluation; escalate to backend validation.

### 13.11. invented_npc_motive

- **Future routing options:** quarantine output; mark model role-ineligible pending further evaluation; escalate to backend validation.

### 13.12. source_boundary_violation

- **Future routing options:** quarantine output; mark model role-ineligible pending further evaluation; require reviewer review.

### 13.13. canon_promotion_attempt

- **Future routing options:** quarantine output; mark model role-ineligible pending further evaluation; require reviewer review.

### 13.14. command_ir_confusion

- **Future routing options:** retry; ask clarification; switch model; escalate to backend validation.

### 13.15. uncertainty_not_reported

- **Future routing options:** retry; mark model role-ineligible pending further evaluation.

### 13.16. refusal_needed_but_missing

- **Future routing options:** quarantine output; mark model role-ineligible pending further evaluation; require reviewer review.

### 13.17. overbroad_narration

- **Future routing options:** retry; reduce packet; switch model.

### 13.18. unsafe_role_escalation

- **Future routing options:** quarantine output; mark model role-ineligible pending further evaluation; require reviewer review; escalate to backend validation.

This section does not implement routing logic.

---

## 14. Evaluation packet and trace requirements

Future evaluation traces should include the following fields:

- **evaluation_id** — unique identifier for this evaluation run.
- **model_id_or_alias** — identifier for the model being evaluated.
- **model_role** — which role the model was evaluated for.
- **model_version_or_quantization** — model version, quantization level, or configuration.
- **packet_type** — type of input packet used.
- **packet_ref** — reference to the specific input packet.
- **test_family** — which test family this evaluation belongs to.
- **expected_behavior_ref** — reference to expected behavior specification.
- **output_ref** — reference to the model's actual output.
- **parse_status** — whether the output was successfully parsed.
- **hidden_info_result** — hidden-information discipline result.
- **soft_state_result** — soft-state mutation result.
- **schema_key_result** — schema-key behavior result.
- **truncation_result** — truncation-safe output result.
- **role_eligibility_result** — whether the model passed role eligibility.
- **failure_mode_tags** — list of failure modes detected.
- **reviewer_notes_ref** — reference to reviewer notes, if any.
- **retest_required** — whether the model must be retested.
- **fingerprint_version** — version of the ModelBehaviorFingerprint used.

Evaluation traces are **audit artifacts**, not model memory, not runtime truth, and not canon/sourcebook authority.

---

## 15. Model-role eligibility ledger

The following defines the future ModelRoleEligibilityLedger as a planning concept. It is not implemented.

The ledger should record:

- **model_identifier** — model name, version, and provider.
- **runtime_environment** — local, cloud, or hybrid.
- **role_attempted** — which model role was evaluated.
- **evaluation_date** — when the evaluation was performed.
- **packet_contract_version** — version of the packet contract used for evaluation.
- **output_contract_version** — version of the output contract used for evaluation.
- **fingerprint_result** — ModelBehaviorFingerprint result summary.
- **allowed_role_status** — whether the model is allowed for this role (allowed, conditional, prohibited).
- **prohibited_roles** — list of roles the model is explicitly prohibited from.
- **known_failure_modes** — list of known failure modes for this model.
- **retest_cadence** — how often the model must be retested.
- **reviewer_approval_status** — whether a reviewer has approved the eligibility determination.
- **sunset_deprecation_status** — whether the model or its eligibility is sunsetted or deprecated.

**No model should be treated as permanently qualified.** Model updates, quantization changes, context changes, or prompt changes require re-evaluation.

This section does not implement ledger storage.

---

## 16. Training and fine-tuning boundary

- Training examples are **not** doctrine.
- Training examples are **not** canon.
- Model behavior is **not** authority.
- Fine-tuning **cannot** replace backend validation.
- Fine-tuning **cannot** authorize hidden-info access.
- Fine-tuning **cannot** make a model eligible without evaluation.
- Live-play examples must be generated only after packet contracts and backend authority contracts exist.
- Conversion data must not be blended into live-play training without source/canon/promotion controls.

This PR does not authorize training data creation or fine-tuning.

---

## 17. Runtime/narration handoff

Model evaluation relates to PR-B packet contracts as follows:

- Models are evaluated against packet type.
- Narrator receives NarrationRenderPacket only.
- Intent parser receives IntentParsingPacket only.
- Summaries use SummaryPacket only.
- Evaluators use EvaluationPacket only.
- **No model role receives BackendStateContext.**
- Packet violations disqualify role eligibility.

---

## 18. Runtime/event handoff

Model evaluation relates to PR-C state/event contracts as follows:

- Model output is **not** event commitment.
- Model output cannot create StateDeltaEnvelope.
- Model output cannot append EventLedgerEntry.
- Model output cannot create CorrectionEvent.
- Model output may create **proposal artifacts only**.
- Any proposal must route through backend transaction/validation before commitment.

---

## 19. Playable-content handoff

Model evaluation relates to PR-D as follows:

- Models may render story-capable structures.
- Models may propose storylet candidates only as non-durable proposals.
- Models may **not** validate playability proof.
- Models may **not** activate storylets.
- Models may **not** mutate quest/scenario DAG.
- Models may **not** decide NPC goals.
- Models may **not** assign DialogueActIR truth status as backend fact.
- Models may **not** commit generator-to-validate-to-commit pipeline stages.

---

## 20. Domain handoff crosswalk

| RT Owner | Model Evaluation Responsibility |
|---|---|
| RT-001 | Command/intent parsing accuracy and action-legality overreach tests. |
| RT-002 | Cost/reward/loss invention tests. |
| RT-003 | Damage/hazard/recovery invention tests. |
| RT-004 | Ability/effect/skill invention tests. |
| RT-005 | Hidden-info leakage, packet boundary, and visibility tests. |
| RT-006 | Mission/clue/reward invention and scenario-state mutation tests. |
| RT-007 | Social/faction/actor-knowledge invention, rumor/fact confusion tests. |
| RT-008 | Generated-content durability/provenance overreach tests. |
| RT-009 | RNG/table/oracle authority and random outcome invention tests. |
| RT-010 | Item/inventory/asset invention and custody mutation tests. |
| RT-011 | Validation/readiness and role qualification tests. |
| RT-012 | Source-local/canon/sourcebook/training promotion boundary tests. |

---

## 21. Validation and test requirements

Future test families:

- Model behavior fingerprint tests.
- Role qualification tests.
- Structured-output parse tests.
- Schema-key behavior tests.
- Truncation-safe output tests.
- Hidden-information adversarial tests.
- Soft-state mutation tests.
- Command-intent adversarial tests.
- Packet-boundary obedience tests.
- Source-local/canon boundary tests.
- Generated-content authority tests.
- RNG/table authority tests.
- Summary-not-memory-authority tests.
- Live-play narration faithfulness tests.
- Metamorphic packet tests.
- Local/cloud comparison tests.
- Model regression tests after quantization or model version change.

This PR only identifies future test requirements and adds focused doctrine tests for the planning artifact.

---

## 22. Blocked-until ledger

The following remain blocked:

- Model evaluation runner — blocked until evaluation framework is authorized.
- Benchmark harness — blocked until benchmark framework is authorized.
- Structured-output schema — blocked until structured-output schema design is authorized.
- Schema-key validator — blocked until schema-key validation is authorized.
- Model behavior fingerprint implementation — blocked until fingerprint framework is authorized.
- Role eligibility ledger implementation — blocked until ledger storage design is authorized.
- Adversarial command corpus data — blocked until corpus creation is authorized.
- Metamorphic test runner — blocked until metamorphic test framework is authorized.
- Failure-mode routing implementation — blocked until routing framework is authorized.
- Prompt templates — blocked until prompt template authoring is authorized.
- Live-play adapter — blocked until live-play adapter implementation is authorized.
- Model routing — blocked until model routing implementation is authorized.
- Training examples — blocked until training data creation is authorized.
- Fine-tuning — blocked until fine-tuning is authorized.
- Runtime code — blocked until minimum backend kernel implementation is authorized per PR-A.
- Command IR — blocked until command IR implementation is authorized per PR-A.
- Context-packet compiler — blocked until context-packet compiler implementation is authorized per PR-B.
- State store — blocked until state store implementation is authorized per PR-C.
- Event ledger — blocked until event ledger implementation is authorized per PR-C.
- Pilot conversion — blocked until pilot conversion authorization is granted.
- Sourcebook inclusion — blocked until sourcebook inclusion authorization is granted.
- Canon promotion — blocked until canon promotion authorization is granted.

---

## 23. Next recommended planning PR

### RUNTIME-SEQ-PR-F: Implementation-readiness review and first executable-kernel authorization gate

PR-F should decide whether the project is ready to move from planning-only runtime sequence files into an implementation plan or actual implementation PR for the minimum backend kernel.

PR-F should check:

- PR-A through PR-E coverage and completeness.
- Owner-spec coverage (RT-001 through RT-012).
- Schema/C-file readiness.
- Test environment readiness.
- Dependency availability.
- Runtime language/runtime stack decision.
- Storage decision.
- Minimum executable target definition.
- Non-implementation guardrails that must remain in force.
- Whether implementation is authorized or still deferred.

PR-E does **not** authorize PR-F and does **not** implement it.

PR-F is the next recommended planning step in the RUNTIME-SEQ sequence, pending review of PR-E.

---

## 24. Non-implementation reaffirmation

This PR adds no:

- model evaluation code;
- benchmark runner;
- prompt templates;
- model routing;
- model adapter;
- structured-output schema;
- schema-key validator;
- adversarial test harness;
- metamorphic test runner;
- model behavior fingerprint implementation;
- role eligibility ledger implementation;
- training data;
- fine-tuning;
- runtime code;
- command IR;
- state store;
- event ledger;
- context-packet compiler;
- redaction algorithm;
- validator implementation;
- generator implementation;
- live-play adapter;
- donor-content audit;
- pilot conversion authorization;
- sourcebook inclusion authorization;
- canon promotion.

All content in this document is planning-level contract definition. Implementation requires separate, explicitly authorized PRs.

---

## 25. Classification block

```yaml
runtime_seq_pr_e:
  review_id: RUNTIME-SEQ-PR-E-MODEL-EVALUATION-STRUCTURED-OUTPUT-ADVERSARIAL-COMMAND-PLAN-001
  artifact_type: model_evaluation_structured_output_adversarial_command_plan
  implementation_status: non_executable_planning
  derives_from:
    - RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001
    - RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001
    - RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001
    - RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001
    - RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001
  primary_owner_tracks:
    - RT-005
    - RT-011
    - RT-012
  supporting_owner_tracks:
    - RT-001
    - RT-002
    - RT-003
    - RT-004
    - RT-006
    - RT-007
    - RT-008
    - RT-009
    - RT-010
  defines_model_role_taxonomy: true
  defines_model_behavior_fingerprint_contract: true
  defines_role_qualification_contract: true
  defines_structured_output_contract: true
  defines_schema_key_behavior_evaluation_policy: true
  defines_truncation_safe_structured_output_policy: true
  defines_adversarial_player_command_corpus_plan: true
  defines_metamorphic_runtime_narration_test_plan: true
  defines_local_cloud_model_comparison_contract: true
  defines_failure_mode_routing_contract: true
  defines_model_role_eligibility_ledger: true
  authorizes_model_evaluation_code: false
  authorizes_benchmark_runner: false
  authorizes_prompt_templates: false
  authorizes_model_routing: false
  authorizes_structured_output_schema: false
  authorizes_schema_key_validator: false
  authorizes_adversarial_test_harness: false
  authorizes_metamorphic_test_runner: false
  authorizes_training_data: false
  authorizes_fine_tuning: false
  authorizes_runtime_implementation: false
  authorizes_command_ir: false
  authorizes_context_packet_compiler: false
  authorizes_live_play: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-SEQ-PR-F implementation-readiness review and first executable-kernel authorization gate, pending review
```

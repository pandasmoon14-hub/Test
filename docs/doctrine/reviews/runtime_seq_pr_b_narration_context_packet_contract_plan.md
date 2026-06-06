# RUNTIME-SEQ-PR-B: Narration / Context Packet Contract Plan

---

## 1. Purpose and status

This document is **RUNTIME-SEQ-PR-B**, a narration/context packet contract plan.

- **Review ID:** RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001
- **Artifact type:** narration_context_packet_contract_plan
- **Implementation status:** non_executable_planning
- **Date:** 2026-06-06
- **Derives from:**
  - RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001
  - RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001

This is a **planning-only** and **non-executable** document.

It defines future packet contracts and validation requirements, but it does not implement:

- context-packet compiler
- narration render packet schema
- narrator output schema
- redaction algorithm
- hidden-state database
- packet budget enforcement
- soft-state mutation validator
- runtime code
- schemas
- command IR
- validators
- generators
- persistence
- live-play prompt
- training data
- donor-content audit
- pilot conversion
- sourcebook inclusion
- canon promotion

---

## 2. Source ledger

The following source artifacts were consulted during preparation of this plan:

| Artifact ID | File | Present |
|---|---|---|
| RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001 | `docs/doctrine/reviews/runtime_schema_implementation_sequencing_review.md` | Yes |
| RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001 | `docs/doctrine/reviews/runtime_seq_pr_a_minimum_backend_kernel_runtime_quality_contract_plan.md` | Yes |
| AUDIT-001 | `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md` | Yes |
| REMEDIATION-STAGE2-COMPLETION-REVIEW-CLOSURE-LEDGER-001 | `docs/doctrine/reviews/runtime_boundary_generator_ownership_stage2_completion_review_and_closure_ledger.md` | Yes |
| RT-001 owner specification | `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md` | Yes |
| RT-002 owner specification | `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md` | Yes |
| RT-003 owner specification | `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md` | Yes |
| RT-004 owner specification | `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md` | Yes |
| RT-005 owner specification (primary) | `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md` | Yes |
| RT-006 owner specification | `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md` | Yes |
| RT-007 owner specification | `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md` | Yes |
| RT-008 owner specification | `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md` | Yes |
| RT-009 owner specification | `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md` | Yes |
| RT-010 owner specification | `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md` | Yes |
| RT-011 owner specification (primary) | `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md` | Yes |
| RT-012 owner specification | `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md` | Yes |
| SM00 | `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` | Yes |
| SM01 | `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md` | Yes |
| SM02 | `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md` | Yes |
| C00 | `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` | Yes |
| C01 | `docs/doctrine/schema/C01_creature_npc_record_schema.md` | Yes |
| C02 | `docs/doctrine/schema/C02_item_gear_record_schema.md` | Yes |
| C03 | `docs/doctrine/schema/C03_ability_power_technique_record_schema.md` | Yes |
| C05 | `docs/doctrine/schema/C05_faction_institution_record_schema.md` | Yes |
| C06 | `docs/doctrine/schema/C06_location_site_region_record_schema.md` | Yes |
| C07 | `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md` | Yes |
| C09 | `docs/doctrine/schema/C09_hazard_environment_record_schema.md` | Yes |
| C10 | `docs/doctrine/schema/C10_table_oracle_record_schema.md` | Yes |
| C14 | `docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md` | Yes |
| ROADMAP-001 | `docs/doctrine/astra_doctrine_roadmap_v0_1.md` | Yes |
| REGISTRY-001 | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` | Yes |
| Decision log | `docs/decisions/current_decisions_log.md` | Yes |
| README | `README.md` | Yes |

**Primary owner tracks:** RT-005 (context-packet/hidden-information boundaries) and RT-011 (validation/readiness tooling).

**Supporting owner tracks:** RT-001, RT-002, RT-003, RT-004, RT-006, RT-007, RT-008, RT-009, RT-010, RT-012.

---

## 3. Backend-first invariant

**Astra Ascension must be model-interchangeable.** The LLM is not the game engine. The LLM is only the player-facing narration and interpretation layer. The backend runtime kernel owns truth.

**Packet implication:**

The model receives bounded, backend-projected packets. The model never receives the full backend state, never owns memory, never directly queries hidden partitions, never rolls dice, never commits events, never mutates records, and never promotes generated or source-local content to authority.

A packet is not backend state. A packet is a curated, bounded projection assembled by the backend for a specific model role in a specific context. The backend decides what to include, what to redact, and what to omit. The model works within the packet; it does not reach beyond it.

---

## 4. Packet layer separation

The following packet families define the planning-level packet layer. All are marked `future_required_not_implemented`.

### 4.1 BackendStateContext

- **Purpose:** Full backend truth representing the complete canonical game state, including all hidden information, uncommitted drafts, pending transactions, and internal bookkeeping.
- **Intended consumer:** Backend runtime kernel only.
- **Allowed contents:** All committed state, all hidden partitions, all pending operations, all internal metadata.
- **Forbidden contents:** No restrictions on content scope — this is the unrestricted truth layer.
- **Hidden-info rules:** Contains all hidden information. Never projected to any model or player-facing system.
- **Persistence status:** Persisted as the canonical state store.
- **Implementation status:** `future_required_not_implemented`

### 4.2 ContextPacket

- **Purpose:** Backend-compiled operational packet for validation, rules application, retrieval, and permitted model work. Broader than the narration render packet but still bounded and redacted.
- **Intended consumer:** Backend validators, authorized API-tier models for evaluation/summarization, future retrieval systems.
- **Allowed contents:** Authorized rules snippets, command-relevant state references, visible facts, permitted retrieved records, recent committed event references, actor/action/target references, validation hints, allowed operations, forbidden operations, source-local boundary notices, hidden-info redaction notices.
- **Forbidden contents:** Hidden facts not authorized for the current player/model role; backend-only state; unrevealed clues; private NPC/faction knowledge unless explicitly visible; uncommitted generated content as fact; canon/sourcebook candidates as accepted authority; raw donor assumptions as Astra truth; D-series/native-design pressure as authority.
- **Hidden-info rules:** Redacted to the authorization level of the consuming role. Hidden partitions replaced with redaction notices.
- **Persistence status:** Not persisted as state. Trace metadata may be logged.
- **Implementation status:** `future_required_not_implemented`

### 4.3 NarrationRenderPacket

- **Purpose:** Small, player-facing render packet intended for local 8B narration. Contains only what the narrator needs to describe the current visible scene.
- **Intended consumer:** Local 8B narrator model.
- **Allowed contents:** Visible scene facts, visible actor state, visible location state, visible threats or pressures, recent committed event echoes, available action affordances, sensory palette, tone and style bounds, output constraints, missing-information policy directives.
- **Forbidden contents:** Hidden information of any kind; backend-only state; unrevealed clues; private NPC motives or knowledge; uncommitted generated content; full rulebook text; long lore passages; old transcript; raw donor content; broad canon notes; source-local material not active in current scene; D-series/native-design pressure as fact.
- **Hidden-info rules:** No hidden information may enter. A hidden_information_exclusion_marker must be present confirming exclusion.
- **Persistence status:** Not persisted. Display-only.
- **Implementation status:** `future_required_not_implemented`

### 4.4 IntentParsingPacket

- **Purpose:** Narrow packet for interpreting player input into intent proposals. Contains only what is needed to map natural-language commands to structured intent candidates.
- **Intended consumer:** Local 8B intent parser model.
- **Allowed contents:** Player input text, available action affordances, actor capability summary, visible target list, basic scene context for disambiguation.
- **Forbidden contents:** Hidden information; backend-only state; full rules text; lore; NPC private knowledge; faction clocks; unrevealed clues; reward tables.
- **Hidden-info rules:** No hidden information may enter.
- **Persistence status:** Not persisted.
- **Implementation status:** `future_required_not_implemented`

### 4.5 ClarificationPacket

- **Purpose:** Packet for asking procedural clarification when command details are missing or ambiguous. Enables the system to request specific information from the player without inventing missing details.
- **Intended consumer:** Local 8B clarification model or narrator model in clarification mode.
- **Allowed contents:** Ambiguous command reference, missing parameter list, visible options for disambiguation, scene-relevant context.
- **Forbidden contents:** Hidden information; backend-only resolution hints; NPC knowledge; unrevealed options.
- **Hidden-info rules:** No hidden information may enter.
- **Persistence status:** Not persisted.
- **Implementation status:** `future_required_not_implemented`

### 4.6 SummaryPacket

- **Purpose:** Approved-context summary packet for session recaps, journal entries, or continuity references. Never memory authority.
- **Intended consumer:** API-tier summarizer model; player-facing display.
- **Allowed contents:** Previously narrated visible events, committed state summaries at the visibility level of the requesting role, session timeline references.
- **Forbidden contents:** Hidden information; uncommitted state; generated content as fact; backend-only metadata; source-local material not active; canon/sourcebook candidates as accepted.
- **Hidden-info rules:** Summaries may only reference facts that were visible at the time of narration. No retroactive reveal of hidden information.
- **Persistence status:** Summary output may be stored as display artifacts. Summaries are never memory authority and never override committed state.
- **Implementation status:** `future_required_not_implemented`

### 4.7 EvaluationPacket

- **Purpose:** Packet for model/judge/evaluator use in quality assessment, consistency checking, or narration review. Never runtime authority.
- **Intended consumer:** API-tier evaluator or judge model.
- **Allowed contents:** Narration output under review, committed visible facts for comparison, narrator output contract constraints, evaluation criteria.
- **Forbidden contents:** Hidden information beyond reviewer authorization; backend-only state; raw donor content; source-local material as Astra truth.
- **Hidden-info rules:** May include reviewer-authorized hidden information for consistency checking only. Must not leak into narration or player-visible output.
- **Persistence status:** Evaluation results may be logged. Never runtime authority.
- **Implementation status:** `future_required_not_implemented`

---

## 5. NarrationRenderPacket contract

The NarrationRenderPacket is the primary narration-facing projection. It must be small, bounded, and strictly limited to what the narrator needs to render the current visible scene.

### 5.1 Required field families

The following field families define the planning-level structure of the NarrationRenderPacket. These are not final schema fields; they are required conceptual categories.

- **scene_visible_facts:** The set of facts about the current scene that are visible to the player characters. Includes physical environment, weather, lighting, audible sounds, visible NPCs, visible objects.
- **player_visible_actor_state:** The state of player characters that is visible to the narration: health/condition tier (not raw numbers unless rules require), active effects, equipment in use, stance or posture.
- **visible_location_state:** Current location description, exits, notable features, visible changes since last narration.
- **visible_threat_or_pressure:** Threats, hazards, or pressures currently visible to the player characters. Does not include hidden threats.
- **recent_committed_event_echoes:** References to recently committed events that the narrator should acknowledge or echo in prose. Only committed, visible events.
- **available_action_affordances:** Actions currently available to the player characters based on committed state, location, and situation. Presented as affordances, not as exhaustive rule lists.
- **sensory_palette:** Sensory details (sights, sounds, smells, textures, temperatures) appropriate to the scene and setting.
- **tone_and_style_bounds:** Tone, genre, and style constraints for narration. May reference setting mood, genre conventions, or session-specific directives.
- **narrator_forbidden_claims:** Explicit list of claims the narrator must not make in this scene. Includes any facts that are hidden, uncommitted, or beyond the narrator's authority.
- **hidden_information_exclusion_marker:** A required marker confirming that no hidden information is present in this packet. If absent, the packet is invalid.
- **unresolved_visible_hooks:** Visible narrative hooks or open questions that the player characters are aware of but that have not yet resolved.
- **packet_budget_estimate:** Estimated token cost of this packet, for budget enforcement.
- **output_constraints:** Structural constraints on narrator output format (length limits, required sections, forbidden patterns).
- **missing_information_policy:** Directives for how the narrator should behave when the packet lacks sufficient information. References Section 9.

### 5.2 NarrationRenderPacket is not

The NarrationRenderPacket is not backend state, not memory, not event commitment, not sourcebook/canon content, and not model freedom to invent facts.

The narrator reads the packet and produces prose. The prose is display only. It does not commit state, does not advance clocks, does not award items, does not reveal hidden information, and does not create durable truth.

---

## 6. ContextPacket contract

The ContextPacket is the broader operational packet used by backend validators, API-tier models, and retrieval systems. It is larger than the NarrationRenderPacket but still bounded and redacted.

### 6.1 Allowed contents

The ContextPacket may include:

- authorized rules snippets relevant to the current command or situation
- command-relevant state references (actor, target, location, resources)
- visible facts at the authorization level of the consuming role
- permitted retrieved records (content records, schema references)
- recent committed event references
- actor/action/target references for validation
- validation hints and constraint summaries
- allowed operations for the current context
- forbidden operations for the current context
- source-local boundary notices identifying source-local content
- hidden-info redaction notices confirming what was withheld

### 6.2 Forbidden contents

The ContextPacket must not include:

- hidden facts not authorized for the current player/model role
- backend-only state (internal bookkeeping, pending transactions not authorized for this role)
- unrevealed clues
- private NPC/faction knowledge unless explicitly visible to the authorized role
- uncommitted generated content as fact
- canon/sourcebook candidates as accepted authority
- raw donor assumptions as Astra truth
- D-series/native-design pressure as authority

### 6.3 Redaction

When hidden information is withheld from a ContextPacket, a redaction notice must be present indicating that information was withheld, the category of withheld information, and the authorization reason for withholding. The redaction notice must not reveal the content of the hidden information.

---

## 7. Visibility and hidden-information rules

Hidden information leakage is a hard failure. The following visibility tiers define planning-level access categories.

### 7.1 Visibility tier definitions

| Tier | Who may receive | May enter NarrationRenderPacket | May enter ContextPacket | May be summarized | May be narrated | May be persisted | Implementation status |
|---|---|---|---|---|---|---|---|
| backend_only | Backend runtime kernel only | No | No | No | No | Yes (backend store) | future_required_not_implemented |
| reviewer_only | Authorized human reviewers, authorized evaluator models | No | Yes (evaluator-tier only) | No | No | Yes (review log) | future_required_not_implemented |
| system_hidden | Backend systems, authorized validators | No | Yes (validator-tier only) | No | No | Yes (system log) | future_required_not_implemented |
| narrator_hidden | Backend, validators; explicitly excluded from narrator | No | Yes (non-narrator roles) | No | No | Yes (backend store) | future_required_not_implemented |
| player_hidden | Backend, narrator-excluded, player-excluded | No | No | No | No | Yes (backend store) | future_required_not_implemented |
| character_known | The specific character who knows it | No (unless that character's scene) | Yes (character-scoped) | Yes (character-scoped) | Yes (if character present) | Yes | future_required_not_implemented |
| actor_known | A specific actor (NPC or PC) who knows it | No (unless visible to player) | Yes (actor-scoped) | Yes (actor-scoped) | Yes (if actor visible and revealing) | Yes | future_required_not_implemented |
| faction_known | Members of a specific faction | No (unless faction-visible to player) | Yes (faction-scoped) | Yes (faction-scoped) | Yes (if faction presence is visible) | Yes | future_required_not_implemented |
| player_visible | All player characters in the current scene | Yes | Yes | Yes | Yes | Yes | future_required_not_implemented |
| narrator_visible | Narrator model in current scene | Yes | Yes | Yes | Yes | Yes (trace only) | future_required_not_implemented |
| public_world_visible | All actors, all players, world knowledge | Yes | Yes | Yes | Yes | Yes | future_required_not_implemented |
| source_local_visible | Visible within source-local context only; not globalized | Yes (with source-local marker) | Yes (with source-local marker) | Yes (with source-local marker) | Yes (with source-local marker) | Yes (source-local store) | future_required_not_implemented |
| redacted_reference_only | Existence may be referenced; content is withheld | No (redaction notice only) | Yes (redaction notice only) | No | No (existence only) | Yes (redaction log) | future_required_not_implemented |

### 7.2 Hard failure on leakage

If hidden information enters a packet or narration output at a visibility tier that does not authorize its presence, the system has failed. This is not a soft warning. Hidden information leakage is a hard failure requiring investigation, correction event, and audit.

---

## 8. Local 8B packet budget policy

### 8.1 Budgeting requirements

- Packets must be bounded. No packet may grow without limit.
- The NarrationRenderPacket must be much smaller than the full ContextPacket. The narrator model receives only what it needs for the current visible scene.
- Local 8B narration should receive visible, current, scene-relevant facts only.
- The following must be excluded from local 8B narration packets: long lore passages, old transcript, full rulebooks, raw donor content, broad canon notes, hidden state, backend-only metadata, source-local material not active in the current scene.
- Packet budgets should have hard caps, warning thresholds, and truncation policy.
- Packet trimming must remove low-priority context before removing active constraints, hidden-info guardrails, committed visible facts, and current player agency.
- Packet budget tests must exist before live-play adapter examples.

### 8.2 Trimming priority

When a packet exceeds its budget, the following trimming priority applies (remove first → remove last):

1. Historical event echoes beyond the immediate scene
2. Extended sensory palette details
3. Supplementary affordance descriptions
4. Background location details not immediately relevant
5. Tone/style elaboration beyond minimum bounds
6. Unresolved hooks not immediately actionable
7. *(Never remove:)* Active constraints, hidden-info exclusion markers, committed visible facts for the current scene, current player agency affordances, narrator forbidden claims, missing-information policy directives

### 8.3 Numeric limits

No numeric token limits are defined in the current repository. Future budget calibration is required before live-play adapter examples. Calibration must account for local 8B model context window, prompt overhead, output reservation, and safety margin.

---

## 9. Missing-information policy

### 9.1 Allowed behavior when packet lacks sufficient information

When the packet does not contain enough information for the narrator or intent parser to operate:

- Ask a procedural clarification (via ClarificationPacket or clarification output field)
- Request backend retrieval through an authorized future mechanism
- Narrate known visible state only
- Offer non-committal interpretive options (e.g., "you might try..." without committing outcome)
- Refuse to decide state
- Return a `needs_backend_context` flag in structured output

### 9.2 Forbidden behavior when information is missing

The following are forbidden when the packet lacks information:

- Invent missing mechanics
- Invent hidden facts
- Invent NPC motives
- Invent rewards
- Invent injuries
- Invent clues
- Invent faction actions
- Invent item ownership
- Invent canon/sourcebook facts
- Infer backend truth from narrative style
- Convert ambiguity into state

If the model cannot answer from the packet, it must say so. Silence or uncertainty is always preferable to fabricated state.

---

## 10. NarratorOutputContract

### 10.1 Output families

The following output families define the planning-level structure of narrator output. These are not final schema fields.

- **narration_text:** Player-facing prose describing the visible scene, action outcomes, or environmental changes. Display only.
- **intent_proposals:** Structured proposals for how player input might be interpreted as commands. Backend validates and commits; proposals are not commands.
- **clarification_questions:** Procedural questions to the player when command details are missing or ambiguous.
- **visible_state_summary:** A summary of currently visible state, for display or continuity reference. Not memory authority.
- **implied_state_claims:** Claims about state that the narration implies (e.g., "the door is now open"). Flagged for soft-state mutation detection.
- **uncertainty_flags:** Markers indicating where the narrator was uncertain and chose conservative framing.
- **needs_backend_retrieval:** Flag indicating the narrator needs additional backend context to proceed.
- **soft_state_risk_flags:** Markers identifying narration passages that risk implying uncommitted state changes.
- **hidden_info_risk_flags:** Markers identifying narration passages that risk leaking hidden information.
- **proposed_affordance_echoes:** Suggestions for what the player might do next, based on visible affordances. Not commitment.
- **refusal_or_boundary_note:** Explicit statement when the narrator refuses to produce output due to insufficient information, hidden-info risk, or authority boundary.

### 10.2 Narrator output authority

Narrator output is display/proposal only. It is never event commitment, never state delta, never memory authority, never canon/sourcebook promotion, and never generated-content durability.

The backend does not read narrator prose to determine what happened. The backend determines what happened; the narrator describes it.

---

## 11. Soft-state mutation detection

### 11.1 Soft-state mutation risks

The following are examples of soft-state mutations — cases where narrator prose implies a state change that was not committed by the backend:

- Prose implies injury not committed by backend
- Prose says an NPC knows something not visible/known in committed state
- Prose awards an item or resource
- Prose moves a faction clock
- Prose reveals a hidden hazard, clue, or truth
- Prose changes location contents
- Prose treats rumor as fact
- Prose implies a random outcome not produced by RT-009
- Prose treats generated content as durable backend truth
- Prose promotes source-local or D-series material into canon

### 11.2 Future validator requirements

The soft-state mutation validator must:

- Detect implied state claims in narrator output
- Compare claims against committed visible facts in the originating packet
- Flag hidden-info leakage where narrator output references information not present in the packet
- Quarantine high-risk narration for review before display
- Require a correction event protocol if displayed narration is later found to contain a soft-state mutation

The correction event protocol must:

- Append a correction event to the event ledger (not overwrite history)
- Produce a player-facing clarification if the mutation was displayed
- Update the state store only through the standard committed-event path
- Log the mutation for audit and model-behavior analysis

This PR does not implement validator logic.

---

## 12. Canonical silence in packet/narration

### 12.1 CanonicalSilencePolicy for packets and narration

The system should remain silent or use uncertainty framing when a fact is:

- not generated
- not committed
- not visible
- not known by the relevant actor
- hidden behind investigation
- source-local but inactive in current context
- canon candidate only (not accepted canon)
- sourcebook candidate only (not accepted sourcebook)
- D-series/native-design pressure only (not promoted)
- converted content evidence only (not accepted)
- generated draft only (not committed)

### 12.2 Silence is not lack of immersion

Silence is not lack of immersion; it is an authority-preserving device. A narrator that says "you don't know" or "the room is quiet" is preserving truth. A narrator that invents an answer to fill silence is fabricating state.

Canonical silence means the system refuses to assert what it does not know, even when assertion would be more entertaining. Immersion comes from consistent, trustworthy narration, not from confident fabrication.

---

## 13. Source-local and canon boundary notices

### 13.1 Packet identification requirements

Packets must identify the provenance status of included content:

- **source-local content:** Material retained from a specific donor source, active only within its source-local context. Not globalized.
- **converted evidence:** Material that has been through conversion intake but has not been promoted to canon or sourcebook.
- **generated draft content:** Material generated by an LLM or procedural system, not yet committed as durable.
- **generated runtime-eligible content:** Generated content that has been validated and is eligible for runtime use, but is not canon.
- **canon candidate:** Material proposed for canon status, pending review and promotion. Not yet authority.
- **sourcebook candidate:** Material proposed for sourcebook inclusion, pending review. Not yet authority.
- **accepted canon:** Material formally promoted to canon status through the governance process.
- **unpromoted D-series/native-design pressure:** D-series or native-design material that exerts design pressure but has not been promoted to authority.

### 13.2 Narrator boundary rules

The narrator may describe only what is visible and active. The narrator may not:

- Globalize source-local material (treat local content as world-wide truth)
- Treat pressure/candidates as authority
- Narrate canon candidates as accepted fact
- Narrate sourcebook candidates as accepted reference
- Narrate D-series/native-design pressure as established rule
- Narrate converted evidence as committed truth
- Narrate generated draft content as durable state

---

## 14. Model role contracts

The following model roles define planning-level role boundaries. Role routing is future policy only, not implemented here.

### 14.1 local_8b_narrator

- **Allowed inputs:** NarrationRenderPacket
- **Allowed outputs:** narration_text, implied_state_claims, uncertainty_flags, soft_state_risk_flags, hidden_info_risk_flags, proposed_affordance_echoes, refusal_or_boundary_note
- **Forbidden authority:** May not commit state, roll dice, reveal hidden information, access backend state, query hidden partitions, promote content, or override validation.
- **Packet type allowed:** NarrationRenderPacket only
- **Implementation status:** `future_required_not_implemented`

### 14.2 local_8b_intent_parser

- **Allowed inputs:** IntentParsingPacket
- **Allowed outputs:** intent_proposals, clarification_questions, uncertainty_flags, needs_backend_retrieval
- **Forbidden authority:** May not commit state, execute commands, access hidden information, bypass validation, or produce narration.
- **Packet type allowed:** IntentParsingPacket only
- **Implementation status:** `future_required_not_implemented`

### 14.3 api_reflective_summarizer

- **Allowed inputs:** SummaryPacket
- **Allowed outputs:** visible_state_summary, uncertainty_flags
- **Forbidden authority:** May not commit state, create memory authority, access hidden information beyond summary authorization, promote content, or produce runtime-binding output.
- **Packet type allowed:** SummaryPacket only
- **Implementation status:** `future_required_not_implemented`

### 14.4 api_evaluator_or_judge

- **Allowed inputs:** EvaluationPacket
- **Allowed outputs:** Evaluation results, consistency flags, quality scores, hidden_info_risk_flags, soft_state_risk_flags
- **Forbidden authority:** May not commit state, produce narration, access backend state beyond evaluation authorization, promote content, or override runtime decisions.
- **Packet type allowed:** EvaluationPacket only
- **Implementation status:** `future_required_not_implemented`

### 14.5 api_canon_or_sourcebook_drafter

- **Allowed inputs:** ContextPacket (canon/sourcebook drafting scope)
- **Allowed outputs:** Draft canon or sourcebook proposals for human review. Never authority.
- **Forbidden authority:** May not promote drafts to canon, commit state, produce runtime narration, access hidden information beyond drafting authorization, or bypass governance review.
- **Packet type allowed:** ContextPacket (drafting scope) only
- **Implementation status:** `future_required_not_implemented`

### 14.6 backend_validator

- **Allowed inputs:** ContextPacket (validation scope), narrator output for mutation detection
- **Allowed outputs:** Validation results, mutation flags, hidden-info leakage flags, correction event triggers
- **Forbidden authority:** This is a backend component, not a model role. It does not produce narration, does not generate content, and does not promote material. It validates.
- **Packet type allowed:** ContextPacket (validation scope)
- **Implementation status:** `future_required_not_implemented`

### 14.7 backend_packet_compiler

- **Allowed inputs:** BackendStateContext (full backend truth)
- **Allowed outputs:** ContextPacket, NarrationRenderPacket, IntentParsingPacket, ClarificationPacket, SummaryPacket, EvaluationPacket — all compiled from backend state with appropriate redaction.
- **Forbidden authority:** This is a backend component. It does not produce narration, does not generate content, and does not promote material. It projects state into packets.
- **Packet type allowed:** Produces all packet types; consumes BackendStateContext.
- **Implementation status:** `future_required_not_implemented`

---

## 15. Packet assembly trace requirements

### 15.1 Future trace fields

The following trace fields must be present on assembled packets and narrator outputs for observability and audit:

- **packet_id:** Unique identifier for this packet instance
- **packet_type:** Which packet family (NarrationRenderPacket, ContextPacket, etc.)
- **source_event_refs:** References to committed events that informed this packet
- **source_record_refs:** References to content records included or consulted
- **visible_facts_included:** Count or summary of visible facts projected into this packet
- **hidden_facts_withheld_count:** Count of hidden facts that were redacted (without revealing content)
- **redaction_reasons:** Categories of redaction applied (e.g., "player_hidden", "narrator_hidden")
- **token_estimate:** Estimated token count for budget tracking
- **model_role:** Which model role will consume this packet
- **output_id:** Unique identifier for the narrator/model output produced from this packet
- **implied_state_claims_detected:** Count of implied state claims detected in the output
- **validation_result:** Result of post-output validation (pass/flag/quarantine)
- **correction_event_ref_if_any:** Reference to any correction event triggered by this output

This PR does not implement tracing.

---

## 16. Validation and test requirements

### 16.1 Future test families

The following test families must be implemented before live-play:

- **Render packet budget tests:** Verify that NarrationRenderPacket stays within budget limits and trimming preserves required fields.
- **Hidden-info exclusion tests:** Verify that hidden information never enters packets at unauthorized visibility tiers.
- **Narrator-output contract tests:** Verify that narrator output conforms to the NarratorOutputContract field families and authority limits.
- **Soft-state mutation tests:** Verify that the soft-state mutation validator detects implied state claims and flags unauthorized mutations.
- **Canonical silence tests:** Verify that the system uses silence or uncertainty framing for uncommitted, invisible, or unauthorized facts.
- **Source-local boundary tests:** Verify that source-local content is marked, not globalized, and not treated as world-wide authority.
- **Missing-information policy tests:** Verify that models use allowed missing-information behaviors and never use forbidden ones.
- **Model-role packet authorization tests:** Verify that each model role receives only its authorized packet type.
- **Packet trace completeness tests:** Verify that all trace fields are present and populated on assembled packets.
- **Local 8B truncation-safety tests:** Verify that truncated packets remain valid and do not lose required fields (hidden-info markers, active constraints, player agency).
- **Adversarial narration leakage tests:** Verify that adversarial prompts or unusual inputs do not cause hidden-info leakage in narration output.
- **Metamorphic narration consistency tests:** Verify that equivalent scenes produce consistent narration within the authority and visibility constraints.

### 16.2 Scope of this PR

This PR only identifies test requirements and adds focused doctrine tests for the planning artifact. It does not implement the runtime test families listed above.

---

## 17. Blocked-until ledger

The following remain blocked pending future authorization:

| Item | Status | Blocked by |
|---|---|---|
| Context-packet compiler implementation | Blocked | Requires PR-B review approval, PR-C (state/event plan), and implementation authorization |
| Render-packet schema implementation | Blocked | Requires PR-B review approval and schema implementation authorization |
| Narrator output schema implementation | Blocked | Requires PR-B review approval and schema implementation authorization |
| Redaction algorithm | Blocked | Requires PR-B review approval, hidden-info partition design, and implementation authorization |
| Hidden-state database | Blocked | Requires PR-C (state/event plan) and implementation authorization |
| Packet budget enforcement | Blocked | Requires PR-B review approval, budget calibration, and implementation authorization |
| Soft-state mutation validator | Blocked | Requires PR-B review approval, PR-C (state/event plan), and implementation authorization |
| Model routing implementation | Blocked | Requires PR-B review approval and implementation authorization |
| Live-play adapter examples | Blocked | Requires all packet/narration contracts implemented and validated |
| Prompt templates | Blocked | Requires packet contracts, model role contracts, and implementation authorization |
| Training data | Blocked | Requires separate training authorization |
| Runtime code | Blocked | Requires PR-C, PR-D, PR-E, and implementation authorization |
| Domain services | Blocked | Requires runtime kernel implementation |
| Pilot conversion | Blocked | Requires separate pilot conversion authorization |
| Sourcebook inclusion | Blocked | Requires separate sourcebook inclusion authorization |
| Canon promotion | Blocked | Requires separate canon promotion authorization |

---

## 18. Next recommended planning PR

### 18.1 RUNTIME-SEQ-PR-C: state/event/invariant/transaction plan

The next recommended planning PR is **RUNTIME-SEQ-PR-C**, which should handle:

- State/event boundary definitions
- Transaction preview contract details
- Event commitment protocol
- Correction events and append-only correction log
- World invariant registry planning
- Replay/hash requirements for deterministic audit
- Event-channel boundaries (what crosses channels, what stays local)
- Rollback-safe validation (ensuring validation failures do not corrupt state)

PR-B does not authorize PR-C and does not implement it. PR-C is a recommendation only, subject to review and separate authorization.

---

## 19. Non-implementation reaffirmation

This PR adds no:

- runtime code
- schema implementation
- command IR
- validator implementation
- generator implementation
- context-packet compiler
- narration render packet schema
- narrator output schema
- redaction algorithm
- hidden-state database
- packet budget enforcement
- soft-state mutation validator
- model routing implementation
- prompt templates
- live-play adapter
- state store
- state delta model
- event ledger
- RNG/table/oracle service
- persistence writer
- training data
- donor-content audit
- pilot conversion authorization
- sourcebook inclusion authorization
- canon promotion

---

## 20. Classification block

```yaml
runtime_seq_pr_b:
  review_id: RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001
  artifact_type: narration_context_packet_contract_plan
  implementation_status: non_executable_planning
  derives_from:
    - RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001
    - RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001
  primary_owner_tracks:
    - RT-005
    - RT-011
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
    - RT-012
  defines_packet_layer_separation: true
  defines_narration_render_packet_contract: true
  defines_context_packet_contract: true
  defines_visibility_tiers: true
  defines_local_8b_packet_budget_policy: true
  defines_narrator_output_contract: true
  defines_soft_state_mutation_detection_requirements: true
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_context_packet_compiler: false
  authorizes_render_packet_schema: false
  authorizes_narrator_output_schema: false
  authorizes_redaction_algorithm: false
  authorizes_hidden_state_database: false
  authorizes_packet_budget_enforcement: false
  authorizes_validator_implementation: false
  authorizes_prompt_templates: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_pilot_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  next_allowed_step: RUNTIME-SEQ-PR-C state/event/invariant/transaction plan, pending review
```

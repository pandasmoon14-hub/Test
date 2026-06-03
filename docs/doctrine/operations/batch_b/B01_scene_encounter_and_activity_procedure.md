# B01 Scene, Encounter, and Activity Procedure

## 1. Purpose and status

B01 is the first Batch B operational doctrine draft for Astra scene, activity, and encounter handling. It defines how operational attention moves between `freeform_scene`, `focused_activity`, `structured_encounter`, and owner-file handoffs without defining final mechanics, runtime state, C-family schema fields, canon content, live-play narration behavior, or sourcebook prose.

Status posture:
- This file is Batch B operational-procedure draft material.
- This file is not current canon, not final mechanics, not runtime authority, not sourcebook prose, and not player-facing rule text.
- C00 remains the schema handoff control surface for Batch B to C-family routing.
- D00, D12, and D19 source-pack files are referenced only as draft source-pack/reference material. They are not current doctrine authority, final mechanics, runtime authority, canon, or sourcebook prose.
- B01 records, examples, and handoff blocks are doctrine-facing only; they are not runtime state, backend contracts, database contracts, event logs, command lifecycle artifacts, sourcebook statblocks, canon entries, or live-play scripts.

Required reference boundaries preserved by B01:
- `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` for shared Batch C base fields, `pending_schema`, source-local boundary, rejected donor element, canon eligibility, review routing, provenance, and missing-schema fallback language.
- `docs/doctrine/native_design/d_series/source_packs/astra_d00_doctrine_pack_v0_1/D00-03_state_delta_commit_protocol.md` for the draft source-pack principle that every meaningful action commits at least one delta to a recognized owner, while B01 does not own every delta format.
- `docs/doctrine/native_design/d_series/source_packs/D12_time_action_cadence_encounter_and_turn_procedure_doctrine_pack/D12_doctrine_pack/D12-00_time_action_cadence_encounter_procedure_and_owner_boundaries.md`, `D12-01_cadence_states_transition_triggers_and_scene_flow.md`, `D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md`, and `D12-07_records_not_final_schema_and_conversion_handoff_shapes.md` for draft source-pack cadence, checkpoint, and not-final-schema source material.
- `docs/doctrine/native_design/d_series/source_packs/D19_cross_pack_integration_conflict_audit_and_conversion_readiness_capstone_pack/D19_capstone_doctrine_pack/D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md` for draft source-pack record-shape governance warnings.

## 2. Owner layer

B01 belongs to Batch B operational doctrine. It routes procedure between the A-family doctrine layer, the C00 schema handoff control surface, future C01-C14 schema families, source-local donor procedure quarantine, and later runtime/canon/training owners.

B01 may identify that a handoff is needed to a likely owner, but it must not perform that owner's work. When B01 cannot identify a valid owner or schema family, it must mark `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` instead of inventing Astra schema, mechanics, runtime state, or canon.

## 3. What B01 owns

B01 owns doctrine-level operational procedure for:
- scene entry and scene exit procedure;
- scene purpose declaration;
- scene pressure declaration;
- activity classification;
- encounter trigger logic;
- transition from freeform play to focused activity;
- transition from focused activity to structured encounter;
- transition from structured encounter back to scene/freeform play;
- checkpoint logic for declared cost, resolution, consequence, state-delta routing, and handoff;
- operational routing to owner files;
- Batch B to C00/C-family handoff references using C00 language;
- source-local donor procedure quarantine and escalation rules;
- scene, encounter, and activity non-collapse rules;
- examples of good and bad B01 usage;
- minimum assertions and acceptance criteria for B01.

## 4. What B01 must not own

B01 must not define or promote:
- C-family schema fields;
- C01-C14 schema contents;
- final mechanics;
- exact math;
- dice/RNG rules;
- combat math;
- runtime entity/component/event/state schemas;
- persistent campaign state;
- command lifecycle implementation;
- runtime state/schema/event/command lifecycle ownership;
- live-play narration behavior or live-play GM adapter behavior;
- final canon promotion;
- accepted lexicon terms;
- sourcebook prose;
- donor encounter formats as Astra defaults;
- donor initiative, round, turn, phase, watch, clock, activation, or pass formats as Astra defaults;
- donor adventure scenes, donor adventure scripts, boss scripts, encounter budgets, or scripted procedures as Astra defaults.

## 5. Non-collapse rule

A scene is not automatically an encounter. An encounter is not automatically combat. An activity is not automatically a scene, encounter, project, travel interval, downtime project, or faction operation.

B01 keeps these containers separate:
- a `freeform_scene` can contain conversation, exploration, description, preparation, and minor interaction without structured cadence;
- a `focused_activity` narrows operational attention around a meaningful action, cost, uncertainty, risk, target, or pressure without necessarily requiring actor sequencing;
- a `structured_encounter` appears only when timing, risk, opposition, cost commitment, sequencing, hidden pressure, reaction windows, or consequence timing requires structured cadence;
- an `extended_activity`, `downtime_project`, `travel_interval`, or `faction_operation` must be handed off when its scale or owner logic exceeds B01 scene procedure.

B01 must not flatten these categories into one universal encounter container, one combat-first action economy, one donor round/turn procedure, or one sourcebook-style scene script.

## 6. Scene, activity, and encounter definitions

B01 uses the following doctrine vocabulary:

- `freeform_scene`: an operational container for description, conversation, positioning, observation, and low-pressure decisions where formal sequencing is not needed.
- `focused_activity`: a narrowed operational container for a declared meaningful action or pressure point where intent, method, target, cost/risk preview, and owner routing matter, but formal sequencing may not yet matter.
- `structured_encounter`: an operational container for sequenced or tightly timed action under pressure. It may be martial, social, stealth, investigation, ritual, technical, platform, travel, factional, hazardous, or mixed. It is not automatically combat.
- `extended_activity`: a focused activity that exceeds immediate scene cadence and requires progress, delay, recovery, crafting, training, research, or project-style handoff.
- `downtime_project`: an activity whose cadence belongs to downtime, project, recovery, crafting, training, or long-form development owners rather than B01 immediate scene procedure.
- `travel_interval`: an activity whose cadence belongs to route, scale, exploration, navigation, interval, watch, discovery, or travel owners rather than B01 immediate scene procedure.
- `faction_operation`: an activity whose cadence belongs to faction, institution, law, reputation, relationship, economy, territory, information, or operation owners rather than B01 immediate scene procedure.
- `source_local_procedure`: a donor or source-specific procedure retained only inside a declared source-local boundary.
- `quarantined_procedure_gap`: an unresolved procedure, schema, runtime, canon, or owner gap that cannot be safely normalized.

## 7. Scene entry procedure

When a scene begins, B01 requires the operator or conversion pass to establish:

1. **Scene container**: identify whether the starting state is `freeform_scene`, `focused_activity`, `structured_encounter`, or another operational state.
2. **Entry reason**: identify why this scene exists now: discovery, conversation, hazard exposure, opposition contact, decision point, aftermath, investigation, travel interruption, faction pressure, project checkpoint, or source-local script detection.
3. **Active owner candidates**: identify likely owner files or later owner layers for content touched by the scene.
4. **Known pressure**: identify visible time pressure, risk, opposition, hidden pressure markers, resource/cost commitment, hazard exposure, or consequence timing if present.
5. **Boundary risks**: identify runtime, canon, schema, donor-procedure, source-local, or live-play boundary risks before normalizing the scene.
6. **Initial handoff posture**: identify whether the scene can proceed under B01, should immediately route to another owner, requires C00/C-family handoff, or must be quarantined/escalated.

A scene may remain freeform when there is no meaningful action, no contested action, no time-sensitive action, no resource/cost commitment, no opposition response, no hazard exposure, no hidden pressure reveal, no multi-actor sequencing need, no state-delta commitment, and no boundary risk.

## 8. Scene purpose and pressure declaration

Every nontrivial scene must declare a doctrine-facing purpose. The purpose may be broad, but it must be sufficient to route attention and avoid converting donor adventure prose into Astra default structure.

Acceptable purpose declarations include:
- establish context;
- reveal information;
- test a method;
- resolve a contested action;
- expose a hazard;
- negotiate with an actor or institution;
- commit a cost;
- create or discharge pressure;
- hand off to project, travel, faction, economy, canon, schema, runtime, or human review;
- retain a source-local procedure inside a boundary.

Pressure declaration must distinguish:
- no meaningful pressure;
- visible risk or visible cost;
- hidden pressure known only as a boundary marker;
- opposition response;
- time-sensitive action;
- multi-actor sequencing need;
- unresolved schema, canon, runtime, or donor-procedure risk.

B01 may mark that pressure exists, but it must not reveal hidden truth, write runtime hidden-information state, define final difficulty math, or script live-play narration.

## 9. Activity classification procedure

Classify each declared meaningful action or source-imported activity using this sequence:

1. **Declare meaningful action**: identify actor, intent, method, target, and why the action matters.
2. **Check for freeform sufficiency**: if there is no risk, opposition, timing pressure, cost commitment, consequence, or owner handoff, keep the action inside `freeform_scene` and record no durable delta unless an owner requires one.
3. **Promote to focused activity**: if the action has meaningful cost, risk, target, uncertainty, pressure, or owner routing but no strict sequencing need, classify as `focused_activity`.
4. **Escalate to structured encounter**: if timing, opposition, contested action, reaction windows, simultaneous declarations, interruption risk, hazard cadence, hidden pressure reveal, or consequence timing requires sequencing, classify as `structured_encounter`.
5. **Route out of B01**: if scale, duration, or owner context dominates, route to `extended_activity`, `downtime_project`, `travel_interval`, `faction_operation`, source-local procedure, C00/C-family handoff, runtime review, canon review, or human review.
6. **Quarantine unresolved gaps**: if no safe owner or schema exists, classify as `quarantined_procedure_gap` and use pending-schema or escalation language.

## 10. Encounter trigger logic

B01 recognizes these trigger families:
- declared meaningful action;
- contested action;
- time-sensitive action;
- resource/cost commitment;
- opposition response;
- hazard exposure;
- hidden pressure reveal;
- multi-actor sequencing need;
- state-delta commitment;
- source-local donor procedure detected;
- C-family handoff needed;
- runtime/canon/schema boundary risk.

A trigger does not automatically create a structured encounter. Use the least structured container that safely preserves timing, cost, consequence, and owner routing. Escalate only when B01 cannot preserve the action under freeform or focused handling.

## 11. Cadence escalation and de-escalation rules

Escalation rules:
- `freeform_scene` escalates to `focused_activity` when a meaningful action needs purpose, method, target, cost/risk preview, consequence awareness, state-delta routing, or owner handoff.
- `focused_activity` escalates to `structured_encounter` when timing, risk, opposition, cost commitment, sequencing, hidden pressure, reaction windows, or consequence timing requires structured cadence.
- Any B01 state routes to `source_local_procedure` when donor procedure is detected and cannot be safely generalized.
- Any B01 state routes to `quarantined_procedure_gap` when missing schema coverage, owner ambiguity, canon risk, runtime risk, or donor overfit cannot be safely resolved.

De-escalation rules:
- `structured_encounter` de-escalates to `focused_activity` when strict sequencing is no longer needed but unresolved pressure, cost, consequence, or owner handoff remains.
- `focused_activity` de-escalates to `freeform_scene` when the meaningful action has resolved, no further structured timing is needed, and required deltas or handoffs are routed.
- `freeform_scene` exits when scene purpose is complete, scene pressure is retired, or another owner takes over.
- De-escalation must not erase declared costs, committed consequences, delayed consequences, hidden consequences, source-local boundaries, rejected donor elements, or unresolved schema gaps.

## 12. Checkpoint sequence for cost, resolution, consequence, and state-delta routing

B01 uses a lightweight checkpoint sequence adapted for Batch B procedure. It is doctrine grammar, not runtime code and not final mechanics:

1. **Cadence checkpoint**: identify `freeform_scene`, `focused_activity`, `structured_encounter`, `extended_activity`, `downtime_project`, `travel_interval`, `faction_operation`, `source_local_procedure`, or `quarantined_procedure_gap`.
2. **Declaration checkpoint**: identify actor, intent, method, target, timing pressure, potential responder, and likely owner.
3. **Purpose/pressure checkpoint**: identify scene purpose, visible pressure, hidden-pressure boundary markers, donor-procedure risk, schema risk, canon risk, and runtime risk.
4. **Cost/risk preview checkpoint**: preview visible costs and visible risks before commitment when the acting side could plausibly know them; do not expose hidden truth by default.
5. **Commitment checkpoint**: commit declared costs, exposure, positioning, time, opportunity, source-local constraints, or other declared commitments when applicable. B01 does not define exact cost math.
6. **Resolution checkpoint**: call the appropriate resolution owner only when uncertainty, opposition, risk, contested timing, hidden pressure, or consequence requires it. B01 does not define dice/RNG rules, DN ladders, outcome bands, exact math, or combat math.
7. **Consequence routing checkpoint**: route consequences to recognized owners for resources, advancement, methods, techniques, harm, actors, objects, world/factions, travel, downtime, economy, campaign memory, schema, canon, runtime, source-local, or human review.
8. **State-delta checkpoint**: every meaningful action must route at least one delta to a recognized owner or explicitly produce `declared_no_delta_result`, `source_local_retained_effect`, `quarantined_unresolved_delta`, `owner_file_escalation`, or `transition_note`. B01 does not define every delta format.
9. **Handoff checkpoint**: create a doctrine-facing owner handoff, C00/C-family handoff, source-local boundary note, rejected donor element note, quarantine note, escalation note, or human-review note as needed.
10. **Continuation/transition checkpoint**: continue, escalate, de-escalate, exit scene, or route to another owner without importing donor cadence as Astra default.

## 13. Owner-file handoff rules

B01 handoffs must identify the owner responsibility rather than inventing content. Use these routing rules:

- Costs, resources, charges, reserves, overdraw, fuel, instability, corruption load, and resource-side backlash route to resource/cost owners.
- Advancement pressure, proof, threshold, breakthrough, transformation, and progression pressure route to advancement owners.
- Method, skill, competency, research, crafting discovery, training, and procedure learning route to competency or project owners.
- Technique, Principle, route expression, oath, domain expression, and access expression route to technique/domain owners.
- Harm, injury, condition, curse, backlash, disaster, corruption injury, and hazard consequence route to harm/hazard owners.
- Actor, form, body, companion, AI, personhood, identity continuity, and substrate issues route to actor owners.
- Object, relic, implant, platform, material, salvage, repair, tool, and equipment state route to object/platform owners.
- World, faction, law, economy, reputation, relationship, territory, pressure, and information route to world/faction/economy owners.
- Travel, exploration, route, interval, discovery, navigation, watch, and scale-transition procedure route to travel/exploration owners.
- Downtime, recovery, crafting, training, research, project progress, and extended tasks route to downtime/project owners.
- Campaign memory, arc, season, long-horizon pacing, time skip, and state pruning route to campaign-continuity owners.
- C-family conversion record needs route through C00 and the appropriate C01-C14 family or `pending_schema`.
- Runtime state, event, command lifecycle, persistence, context packet, validator, and backend concerns route to runtime review, not B01.
- Canon promotion, accepted lexicon, proper noun acceptance, sourcebook phrasing, and final setting truth route to canon/lexicon review, not B01.

## 14. Batch B to C00/C-family handoff rules

B01 may identify that a Batch C handoff is needed. It must use C00 language and must not invent C-family fields, donor field names, donor record formats, or C01-C14 schema contents.

The following lightweight doctrine-facing handoff block is allowed as a routing note only. It is not a runtime schema, not a database contract, not a backend event, not a sourcebook statblock, and not a final C-family schema:

```yaml
batch_b_to_c_handoff:
  target_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema
  schema_status: not_started | stub_index_only | minimum_unlock_draft | tested_minimum | stable_for_family | stable_cross_family | superseded | deprecated
  required_c00_base_fields: true
  source_evidence_refs_required: true
  construct_refs_required: true
  outcome_refs_required: true
  provenance_refs_required: true
  source_local_boundary_required_if_applicable: true
  rejected_donor_elements_required_if_applicable: true
  canon_eligibility_required: true
  review_routing_required: true
  unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists
```

B01 handoff notes must preserve C00 base requirements including source evidence refs, construct refs, outcome refs, provenance refs, source-local boundary handling, rejected donor elements, canon eligibility, review routing, and missing-schema fallback. B01 must never add Astra-sounding fields to C01-C14 to solve a procedural gap.

## 15. Missing-schema fallback and quarantine/escalation

When B01 identifies content that needs schema coverage but no C-family schema exists or no safe family applies, it must choose one of these actions:

- mark `target_schema_family: pending_schema`;
- set `unresolved_schema_gap_action: quarantine`;
- set `unresolved_schema_gap_action: escalation`;
- set `unresolved_schema_gap_action: human_review`;
- set `unresolved_schema_gap_action: defer_until_schema_exists`;
- retain a declared `source_local_boundary` if the procedure is safe only within a source;
- record rejected donor elements if donor assumptions are unsafe to import;
- route to C00 governance rather than inventing C-family fields.

Unclassifiable records are quarantined or escalated, not normalized by invention. Missing schema coverage must not produce improvised schema, runtime state, canon entries, accepted lexicon, final mechanics, or player-facing rules.

## 16. Source-local donor procedure handling

Donor rounds, turns, watches, initiative formats, phases, clocks, activations, passes, adventure scenes, encounter budgets, random encounter intervals, boss scripts, lair scripts, scripted collapses, faction turns, travel watches, and scripted procedures are donor evidence only. They may inform conversion pressure, but they do not become Astra defaults through B01.

When a donor procedure is detected:

1. identify its function in the source;
2. identify donor assumptions that must be stripped;
3. decide whether B01 can route its function to freeform, focused, structured, extended, travel, downtime, faction, source-local, or schema handoff handling;
4. retain it as `source_local_procedure` only if bounded and useful;
5. record rejected donor elements when the donor format, field names, math, combat assumptions, encounter budgets, initiative, round, turn, watch, or adventure script cannot be imported;
6. quarantine or escalate if generalization would invent Astra procedure, schema, canon, runtime state, or mechanics.

Repeated donor pressure does not promote donor procedure to Astra law. Cross-source recurrence may create a review signal only.

## 17. Runtime boundary

B01 does not define runtime entity/component/event/state schemas, event-sourced state model, state delta validator, command lifecycle implementation, runtime command lifecycle, context packet compiler, persistence, backend validation, hidden-information runtime state, dice services, or live-play runtime behavior.

Live-play behavior must not consume B01 procedure as runtime authority without later runtime validation. Runtime consumers may treat B01 only as upstream doctrine input until a runtime owner validates contracts, state mutation, event emission, persistence, context compilation, and safety behavior.

## 18. Canon boundary

B01 does not create final canon, accepted canon, canon promotion, accepted lexicon terms, proper noun acceptance, sourcebook scene framing, final setting truth, or sourcebook prose. B01 may mark canon eligibility routing signals through C00-style handoff language, but canon acceptance belongs to later canon/lexicon owners.

B01 examples are not canon entries. Donor proper nouns, adventure locations, scene scripts, encounter names, monster names, and lore assumptions remain source-local, rejected, quarantined, or routed to canon/legal/IP review.

## 19. Live-play/training boundary

B01 is not a live-play narration script, GM adapter, player prompt, training example authority, or evaluation benchmark. It may support later training/evaluation work by clarifying doctrine boundaries, but it must not be consumed as final live-play GM behavior.

Training examples must not treat B01 records as runtime state, backend contracts, player-facing rule text, sourcebook statblocks, or canon. Evaluation may assert B01 boundaries but must not promote them to runtime implementation.

## 20. Examples of good and bad B01 usage

Good B01 usage:
- A conversation remains a `freeform_scene` because no meaningful action, cost, risk, opposition, or state-delta commitment has appeared.
- A player studies an unstable relic under visible risk; B01 classifies this as `focused_activity`, previews visible risk, and routes object state to the object/platform owner while refusing to define exact resolution math.
- A stealth breach with simultaneous guard response escalates from `focused_activity` to `structured_encounter` because multi-actor sequencing, opposition response, timing, and hidden pressure matter; B01 routes consequences to actor, harm, object, and world/faction owners as needed.
- A donor adventure's three-round collapse countdown is retained as `source_local_procedure` with a source-local boundary, rejected donor elements, and C00-style provenance instead of becoming Astra default encounter timing.
- A conversion pass needs a C-family record but no schema exists; B01 marks `target_schema_family: pending_schema` and uses quarantine, escalation, `human_review`, or `defer_until_schema_exists` instead of inventing fields.

Bad B01 usage:
- Treating every scene as an encounter.
- Treating every encounter as combat.
- Importing donor initiative, round, turn, phase, watch, activation, or encounter-budget format as Astra default.
- Adding C01-C14 fields because a Batch B procedure needs a place to store data.
- Writing runtime state, event records, command lifecycle implementation, context packet fields, or persistence rules from B01 examples.
- Turning B01 examples into canon, accepted lexicon, sourcebook statblocks, adventure scripts, or player-facing rule text.
- Letting live-play narration skip declared cost, consequence routing, state-delta routing, source-local boundary handling, or missing-schema escalation.

## 21. Minimum tests or assertions

Minimum B01 assertions:
- B01 exists at `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md`.
- All required B01 sections are present.
- B01 declares ownership and non-ownership.
- B01 includes C00 handoff language and the `batch_b_to_c_handoff` doctrine-facing block.
- B01 rejects C-family field invention and C01-C14 schema-content ownership.
- B01 rejects runtime entity/component/event/state schemas, persistent campaign state, command lifecycle implementation, context packet, persistence, and live-play runtime ownership.
- B01 rejects donor rounds, turns, watches, initiative formats, encounter budgets, adventure scenes, and adventure scripts as Astra defaults.
- B01 includes missing-schema fallback, `pending_schema`, quarantine, escalation, `human_review`, and `defer_until_schema_exists`.
- B01 references D00, D12, and D19 only as draft source-pack/reference material, not final doctrine authority.
- B01 does not require creation of C01-C14 files.
- B01 does not promote registry status to current.

## 22. Acceptance criteria

B01 is acceptable if it:

1. establishes scene entry, scene purpose, activity classification, encounter trigger, escalation, de-escalation, checkpoint, and owner-handoff procedure;
2. preserves the non-collapse rule that a scene is not automatically an encounter and an encounter is not automatically combat;
3. uses structured cadence only when timing, risk, opposition, cost commitment, sequencing, hidden pressure, or consequence timing requires it;
4. routes every meaningful action to at least one recognized delta owner or an explicit no-delta/quarantine/escalation result without defining every delta format;
5. uses C00 language for Batch B to C-family handoff while refusing to invent C-family fields;
6. handles missing schema coverage through `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists`;
7. quarantines or source-localizes donor procedures rather than importing donor rounds, turns, watches, initiative, encounter budgets, or adventure scripts as Astra defaults;
8. maintains runtime, canon, live-play/training, sourcebook, and final-mechanics boundaries;
9. remains focused on B01 and does not draft B02-B11 or C01-C14.

## 23. Follow-up handoff to B02

B01 hands off to B02 only the unresolved need for the next Batch B operational doctrine owner to define its own focused procedure and boundaries. B01 does not draft B02, reserve B02 mechanics, or define B02's schema, runtime, canon, or sourcebook behavior.

The B02 follow-up should preserve these B01 handoff constraints:
- continue using C00 as the schema handoff control surface;
- keep D-series material as draft source-pack/reference material only;
- avoid C-family field invention;
- preserve source-local donor procedure quarantine;
- maintain runtime, canon, live-play/training, sourcebook, and final-mechanics boundaries.

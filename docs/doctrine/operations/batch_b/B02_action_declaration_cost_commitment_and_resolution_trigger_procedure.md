# B02 Action Declaration, Cost Commitment, and Resolution Trigger Procedure

## 1. Purpose and status

B02 is the second Batch B operational doctrine draft for Astra action declaration handling. It sits after `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md` and treats B01 as upstream Batch B context for scene, activity, encounter, checkpoint, and owner-handoff posture.

B02 defines how a declared action is received, clarified, checked for feasibility, previewed for visible cost or risk, committed when a declared cost is accepted, routed to no-roll handling or resolution-owner triggering, and handed onward to action-to-delta owners. It does this without defining final mechanics, exact Difficulty Numbers, dice/RNG implementation, runtime state, C-family schema fields, canon content, live-play narration behavior, or sourcebook prose.

Status posture:
- This file is Batch B operational-procedure draft material.
- This file is not current canon, not final mechanics, not runtime authority, not sourcebook prose, and not player-facing rule text.
- C00 remains the schema handoff control surface for Batch B to C-family routing.
- D00, D02, D03, D12, and D19 source-pack files are referenced only as draft source-pack/reference material. They are not current doctrine authority, final mechanics, runtime authority, canon, sourcebook prose, or live-play GM behavior.
- B02 records, examples, and handoff blocks are doctrine-facing only; they are not runtime state, backend contracts, database contracts, event logs, command lifecycle artifacts, context packet formats, sourcebook statblocks, canon entries, or live-play scripts.

Required reference boundaries preserved by B02:
- `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md` for upstream Batch B scene, activity, encounter, checkpoint, non-collapse, and Batch B to C00/C-family handoff context.
- `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` for shared Batch C base fields, `pending_schema`, source-local boundary, rejected donor element, canon eligibility, review routing, provenance, and missing-schema fallback language.
- `docs/doctrine/native_design/d_series/source_packs/astra_d00_doctrine_pack_v0_1/D00-03_state_delta_commit_protocol.md` for the draft source-pack principle that every meaningful action commits or routes at least one delta to a recognized owner, while B02 does not own every delta format.
- `docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-00_resolution_architecture_and_owner_boundaries.md` and `docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-03_cost_commitment_overinvestment_and_success_at_cost.md` for draft source-pack resolution, opposed/contested/defense/resistance, cost commitment, overinvestment, and success-at-cost reference material only.
- `docs/doctrine/native_design/d_series/source_packs/astra_d03_doctrine_pack_v0_1/astra_d03_doctrine_pack_v0_1/D03_01_power_economy_lattice.md` for draft source-pack resource/cost owner reference material only, not final resource economy math.
- `docs/doctrine/native_design/d_series/source_packs/D12_time_action_cadence_encounter_and_turn_procedure_doctrine_pack/D12_doctrine_pack/D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md` for draft source-pack checkpoint, cost preview, commitment, resolution, and consequence timing reference material only.
- `docs/doctrine/native_design/d_series/source_packs/D19_cross_pack_integration_conflict_audit_and_conversion_readiness_capstone_pack/D19_capstone_doctrine_pack/D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md` for draft source-pack record-shape governance warnings that lightweight blocks are not final schema, not backend-ready, not player-facing rule text, and not database contracts.

## 2. Owner layer

B02 belongs to Batch B operational doctrine. It routes declared-action procedure between B01 scene/activity/encounter context, the A-family doctrine layer, the C00 schema handoff control surface, future C01-C14 schema families, source-local donor procedure quarantine, and later runtime/canon/training owners.

B02 may identify that a resolution owner, cost owner, state-delta owner, source-local owner, C-family owner, runtime owner, canon owner, or human reviewer is needed, but it must not perform that owner's work. When B02 cannot identify a valid owner or schema family, it must mark `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` instead of inventing Astra schema, mechanics, runtime state, hidden-information state, canon, or sourcebook prose.

## 3. What B02 owns

B02 owns doctrine-level operational procedure for:
- declared-action intake procedure;
- actor/intent/method/target framing;
- action scope clarification;
- action feasibility triage;
- no-roll vs roll-trigger decision procedure;
- visible cost/risk preview procedure;
- hidden-risk boundary handling without exposing hidden truth;
- declared cost commitment procedure;
- overreach/overinvestment routing as procedure, not math;
- resolution-owner trigger procedure;
- contested/opposed/defense/resistance trigger routing;
- success-at-cost trigger routing;
- partial, blocked, and impossible action handling;
- action-to-delta routing requirements;
- B02-to-C00/C-family handoff references when declared actions produce conversion records;
- source-local donor action/cost/resolution procedure quarantine and escalation rules;
- examples of good and bad B02 usage;
- minimum tests, assertions, and acceptance criteria for B02.

## 4. What B02 must not own

B02 must not define or promote:
- final d20 math;
- exact Difficulty Numbers or exact DN values;
- final modifier ladders;
- dice/RNG implementation or dice/RNG rules;
- final action economy;
- initiative/round/turn procedure;
- final resource economy math;
- final cost math or final cost prices;
- final overinvestment formulas;
- final success-at-cost tables;
- final combat math;
- C-family schema fields;
- C01-C14 schema contents;
- runtime entity/component/event/state schemas;
- runtime state/event/command lifecycle ownership;
- persistent campaign state;
- command lifecycle implementation or runtime command lifecycle;
- event-sourced state model;
- state delta validator;
- context packet compiler;
- persistence;
- backend validation;
- hidden-information runtime state;
- live-play narration behavior or live-play GM adapter behavior;
- final canon promotion;
- accepted lexicon terms;
- sourcebook prose;
- donor action formats as Astra defaults;
- donor skill check formats as Astra defaults;
- donor spell/action/cost/slot/usage formats as Astra defaults.

## 5. Non-collapse rule

A declared action is not automatically a roll. A roll is not automatically a combat action. A cost is not automatically a resource spend; it may be time, position, exposure, obligation, attention, opportunity, instability, material, social standing, information, or source-local constraint.

B02 keeps these categories separate:
- a `declared_action` is an actor's stated attempt, not yet a mechanics call;
- a `clarified_action` has enough actor, intent, method, target, and scope framing to route;
- `freeform_resolution` may satisfy a trivial, certain, or descriptive action without a roll;
- `no_roll_required` marks that no uncertainty procedure is required, while consequence or delta routing may still be required;
- `roll_triggered` means B02 has detected a resolution trigger and must hand off to the relevant owner without defining final resolution math;
- `owner_handoff_required` marks that another doctrine owner must resolve cost, delta, timing, opposition, schema, source-local, runtime, canon, or human-review concerns;
- `declared_cost_pending` and `declared_cost_committed` distinguish preview from accepted commitment;
- `hidden_risk_marked` protects hidden truth while acknowledging that a hidden-risk boundary exists;
- `impossible_action`, `blocked_action`, `source_local_action_procedure`, and `quarantined_action_gap` prevent donor procedure, schema invention, or unowned mechanics from collapsing into Astra defaults.

B02 must not flatten all declared actions into rolls, all rolls into combat actions, all costs into resource spends, all hidden risks into player-facing disclosures, all donor action formats into Astra action economy, or all doctrine-facing notes into runtime state.

## 6. Action declaration grammar

A B02 action declaration is framed as:

```text
Actor attempts Intent by Method against/with Target within Scope, accepting or refusing visible Cost/Risk after preview when commitment is required.
```

Minimum doctrine-facing intake elements:
- `actor_ref`: who or what is acting, if known;
- `intent_summary`: what outcome the actor is trying to cause, learn, prevent, protect, move, alter, obtain, repair, persuade, expose, hide, or escape;
- `method_summary`: how the actor attempts it, including tools, route, technique, social approach, movement, time expenditure, attention, or source-local procedure;
- `target_summary`: the object, actor, place, system, information, faction, hazard, boundary, or null target affected;
- `scope_summary`: how large, long, public, risky, precise, costly, reversible, or consequential the action is;
- visible cost/risk preview posture;
- hidden-risk boundary marker, if one is known to the procedure without revealing hidden truth;
- candidate resolution trigger family, if present;
- expected delta routing or no-delta/quarantine/escalation/transition result.

This grammar is doctrine-facing procedure vocabulary only. It is not a command object, backend API, action economy, C-family record, sourcebook statblock, player-facing rule text, or final mechanics.

## 7. Intent, method, target, and scope framing

B02 clarifies intent, method, target, and scope before deciding whether resolution is required.

Clarification procedure:
1. Identify the actor and acting capacity: person, creature, platform, group, faction, companion, tool-mediated actor, source-local construct, or unknown actor requiring owner handoff.
2. Restate intent in outcome terms rather than donor button terms. For example, "bypass the sealed hatch quietly" is preferred over importing a donor skill label as the action itself.
3. Restate method in Astra-facing terms: physical approach, social pressure, technique expression, tool use, time investment, route, preparation, source-local retained effect, or other method.
4. Identify target or mark `target_summary: null` only when the action truly has no discrete target.
5. Bound scope: momentary, scene-scale, encounter-scale, extended activity, travel interval, faction operation, downtime project, conversion record, or source-local procedure.
6. If scope is too broad, split, narrow, transition to B01 container logic, or mark `owner_handoff_required`.
7. If actor, intent, method, target, or scope remains materially ambiguous, ask for doctrine-facing clarification in design work or route to `human_review`; do not invent missing facts.

## 8. Feasibility and boundary triage

B02 triages feasibility before resolution triggering:
- Clearly feasible and consequence-free actions may proceed as `freeform_resolution`, `no_roll_required`, or `no_delta_required`.
- Feasible but meaningful actions route to cost/risk preview, resolution triggering, owner handoff, or delta routing.
- Partially feasible actions narrow the achievable scope, preview cost/risk, route partial success-at-cost availability, or escalate to an owner.
- Blocked actions mark `blocked_action` when a known boundary, missing prerequisite, owner rule, or protected state prevents the action under current conditions.
- Impossible actions mark `impossible_action` when the declared intent cannot be satisfied by the stated method and scope under the governing doctrine.
- Unclear schema, source-local, canon, runtime, or hidden-state conflicts mark `quarantined_action_gap`, escalation, `human_review`, or `defer_until_schema_exists`.

Feasibility triage must not silently convert an impossible action into a roll, silently reveal hidden truth, silently import donor challenge assumptions, or silently create runtime state.

## 9. No-roll decision procedure

A declared action is not automatically a roll. B02 chooses `no_roll_required` when all of the following are true:
1. the action is feasible at the declared scope or after accepted clarification;
2. there is no meaningful uncertainty requiring a resolution owner;
3. there is no meaningful consequence pressure requiring roll-triggered resolution;
4. there is no opposition, contested timing, defense, resistance, overreach, overinvestment, or success-at-cost trigger requiring owner routing;
5. hidden risk does not require protected owner handling;
6. any visible cost has been previewed and either committed, refused, or routed without needing roll math;
7. any meaningful result routes to a recognized delta owner or explicitly produces `no_delta_required`, `transition_note`, `source_local_retained_effect`, quarantine, escalation, `human_review`, or `defer_until_schema_exists`.

No-roll handling may still produce time spent, position changed, information gained, obligation incurred, source-local retained effect, transition to B01 container logic, or owner-file handoff. No-roll does not mean no consequence, no delta, no cost, no record, or no review.

## 10. Resolution trigger procedure

B02 may decide that resolution is required, but B02 must not define final resolution math. B02 triggers owner handoff when one or more trigger families are present:
- `uncertainty_present`;
- `meaningful_consequence_present`;
- `visible_cost_present` requiring commitment timing or owner handling;
- `hidden_risk_boundary_present` requiring protected handling without revealing hidden truth;
- `opposition_present`;
- `contested_timing_present`;
- `defense_or_resistance_needed`;
- `overreach_declared`;
- `overinvestment_declared`;
- `success_at_cost_available`;
- `state_delta_required`;
- `owner_handoff_required`;
- `C-family handoff needed`;
- `source-local donor procedure detected`;
- `runtime/canon/schema boundary risk`.

When a trigger exists, B02 marks `roll_triggered` or `owner_handoff_required` and routes to the relevant owner. B02 may route to D02-style resolution logic as draft source-pack reference material, but must not promote D02 to final current doctrine and must not copy final d20 math, exact Difficulty Numbers, dice/RNG implementation, opposed-check math, defense/resistance math, or margin tables into B02.

## 11. Cost and risk preview procedure

Visible costs and visible risks must be previewed before declared cost commitment when the acting perspective could plausibly know them. A visible cost/risk preview may include:
- time;
- position;
- exposure;
- obligation;
- attention;
- opportunity;
- instability;
- material;
- social standing;
- information;
- source-local constraint;
- likely harm, strain, legal pressure, object stress, faction response, route closure, or escalation.

A visible cost/risk preview must not reveal hidden truth. Hidden-risk boundary handling may state that a risk is not fully knowable, that an action has protected uncertainty, or that hidden owner review is required, but it must not expose hidden state, hidden opposition, hidden trap content, hidden canon answers, hidden runtime flags, secret target properties, or concealed source-local truth.

A cost is not automatically a resource spend. B02 may route costs to resource/cost owners, but must not define final cost prices, pool math, recharge math, overdraw math, power economy formulas, or final resource economy math.

## 12. Declared cost commitment procedure

Declared cost commitment separates preview from acceptance:
1. Identify whether a visible cost/risk exists.
2. Preview only what the actor could plausibly know without exposing hidden truth.
3. Mark `declared_cost_pending` or `declared_cost_status: pending_commitment` when the action cannot proceed until the cost/risk posture is accepted, refused, or escalated.
4. If accepted, mark `declared_cost_committed` or `declared_cost_status: committed` before resolution unless a future owner or source-local retained procedure explicitly routes timing elsewhere.
5. If refused, narrow the action, choose a lower-scope alternative, mark `no_roll_required` with no action taken, or route a transition/escalation.
6. If unclear, mark `declared_cost_status: escalated`, `owner_handoff_required`, `human_review`, or `defer_until_schema_exists`.

Declared costs remain distinct from emergent consequences, delayed consequences, hidden consequences, and historical consequences. B02 routes those distinctions to owner files; it does not implement a state delta validator or persistence model.

## 13. Overreach, overinvestment, and success-at-cost routing

B02 treats overreach, overinvestment, and success-at-cost as trigger routing, not math.

- `overreach_declared` applies when intent, method, target, or scope exceeds normal feasibility but might be partially possible, risky, costly, or owner-resolvable.
- `overinvestment_declared` applies when the actor offers extra time, attention, exposure, resource, obligation, instability, material, position, or source-local cost to improve prospects or widen effect.
- `success_at_cost_available` applies when a failed, blocked, partial, or uncertain path could still produce the intent by accepting a new or increased cost.

B02 must route these to the relevant resolution, cost, resource, consequence, or state-delta owner. It must not define final overinvestment formulas, final success-at-cost tables, final cost prices, final resource economy math, final d20 math, exact Difficulty Numbers, or final modifier ladders.

## 14. Contested, opposed, defense, and resistance trigger routing

B02 routes contested, opposed, defense, and resistance situations without defining final math.

Trigger routing:
- `opposition_present`: another actor, faction, hazard, defense, environment, law, system, source-local force, or protected truth can meaningfully prevent or alter the outcome.
- `contested_timing_present`: order, simultaneity, interruption, reaction window, pursuit, escape, countdown, action window, or B01/B03 cadence boundary matters.
- `defense_or_resistance_needed`: a target may defend, resist, absorb, avoid, contest, or transform the effect.

B02 may route to D02-style contested/opposed/defense/resistance logic as draft source-pack/reference material only. It must not define final contested check math, opposed-check math, defense/resistance grammar, combat math, target numbers, initiative, round, turn, action economy, or donor saving throw categories as Astra defaults.

## 15. Action-to-delta routing

Every meaningful action must route at least one delta to a recognized owner or explicitly produce a no-delta/quarantine/escalation/transition result. B02 uses D00-03 draft source-pack material only as a reference for this principle; B02 does not own all delta formats.

Action-to-delta routing options include:
- `no_delta_required` for trivial, descriptive, or non-persistent actions;
- `owner_routed` for resource, advancement, skill, route/technique, harm, actor, object, world, faction, information, location, hazard, or source-local deltas;
- `transition_note` for B01 scene/activity/encounter transitions or future B03 procedure handoff;
- `source_local_retained_effect` for bounded donor/source-local effects that remain evidence and do not become Astra defaults;
- `quarantined_unresolved_delta` when no owner or schema can safely receive the delta;
- `owner_file_escalation` when the correct owner must decide format, timing, or legitimacy.

B02 must distinguish declared costs, committed costs, emergent consequences, delayed consequences, hidden consequences, and no-delta results. Missing owner coverage must not produce improvised schema or hidden runtime state.

## 16. Owner-file handoff rules

B02 handoff rules:
- hand off to B01 when action handling changes scene, activity, encounter, or transition state;
- hand off to future B03 when follow-up doctrine must own the next Batch B procedure;
- hand off to D02-style draft source-pack reference only for resolution architecture concepts, never as final current doctrine authority;
- hand off cost/resource questions to the appropriate resource/cost owner, with D03-style power economy lattice material treated only as draft source-pack/reference material;
- hand off delta questions to recognized state-delta owners or mark quarantine/escalation;
- hand off C-family conversion records through C00 governance;
- hand off source-local donor procedures to source-local retention, rejected-donor-element preservation, quarantine, or human review;
- hand off runtime concerns to later runtime owners rather than defining entity/component/event/state schemas, command lifecycle implementation, context packet compiler, backend validation, persistence, or hidden-information runtime state;
- hand off canon and lexicon concerns to canon/lexicon owners rather than promoting terms, facts, or setting content.

An owner handoff is successful only if B02 states the reason for routing and avoids doing the target owner's work.

## 17. Batch B to C00/C-family handoff rules

Batch B procedure may identify that a C-family handoff is needed, but it must not invent C-family fields. B02 must never add Astra-sounding fields to C01-C14, define C01-C14 schema contents, or require creation of C01-C14 files. B02 does not require creation of C01-C14 files. C00 remains the schema handoff control surface.

When declared actions produce conversion records, B02 routes through C00 base requirements: source evidence references, construct references, outcome references, provenance references, source-local boundary, rejected donor elements when applicable, canon eligibility, review routing, and schema status. Missing schema coverage must produce `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` rather than improvised schema.

The following lightweight doctrine-facing handoff block may be used for declared actions that need C00/C-family routing. It is not a runtime schema, not a backend event, not a command object, not a C-family record, not a sourcebook statblock, not final mechanics, and not player-facing rule text.

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

B02 also uses this B02-specific lightweight doctrine-facing block for action declaration routing notes. `action_declaration_routing_note` is not a runtime schema, not a backend event, not a command object, not a C-family record, not a sourcebook statblock, and not final mechanics. It is not a database contract, not an event log, not a context packet format, not persistent campaign state, not sourcebook prose, not canon, and not player-facing rule text.

```yaml
action_declaration_routing_note:
  action_state: declared_action | clarified_action | freeform_resolution | no_roll_required | roll_triggered | owner_handoff_required | declared_cost_pending | declared_cost_committed | hidden_risk_marked | impossible_action | blocked_action | source_local_action_procedure | quarantined_action_gap
  actor_ref: string | null
  intent_summary: string
  method_summary: string
  target_summary: string | null
  scope_summary: string
  visible_cost_or_risk_present: boolean
  hidden_risk_boundary_present: boolean
  resolution_trigger:
    triggered: boolean
    reason: uncertainty_present | meaningful_consequence_present | opposition_present | contested_timing_present | defense_or_resistance_needed | overreach_declared | overinvestment_declared | success_at_cost_available | owner_handoff_required | source_local_procedure_detected | other
  declared_cost_status: none | previewed | pending_commitment | committed | refused | escalated
  delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  note: string
```

## 18. Missing-schema fallback and quarantine/escalation

Missing-schema fallback is mandatory. If action declaration, cost, resolution, delta, source-local, runtime, canon, or C-family handling lacks safe owner coverage, B02 must choose one of:
- `pending_schema`;
- quarantine;
- escalation;
- `human_review`;
- `defer_until_schema_exists`;
- `quarantined_action_gap`;
- `quarantined_unresolved_delta`;
- `owner_file_escalation`.

Missing schema coverage must not produce improvised schema. Unclassifiable action records are quarantined or escalated, not normalized by invention. B02 must route to C00 governance rather than inventing C-family fields, donor field names, donor record formats, C01-C14 schema contents, runtime state, event schemas, command lifecycle objects, hidden-information runtime state, or backend contracts.

## 19. Source-local donor action/cost/resolution handling

Donor action formats, skill formats, spell slots, usage rates, maneuver formats, action economies, initiative systems, challenge assumptions, donor skill check formats, donor spell/action/cost/slot/usage formats, and donor resolution formats are donor evidence only. They do not become Astra defaults through B02.

Source-local donor procedure handling:
1. Detect `source-local donor procedure detected` when a declared action depends on donor-native action names, skill labels, spell slots, usage rates, maneuver formats, action economies, challenge assumptions, combat assumptions, or cost/resolution scripts.
2. Preserve donor material as source evidence, donor terms, rejected donor elements, or bounded source-local context when lawful and useful.
3. Translate only the underlying intent, method, target, scope, visible cost/risk, and possible delta into Astra-facing doctrine terms.
4. Mark `source_local_action_procedure` or `source_local_retained_effect` when donor procedure must remain bounded to its source context.
5. Quarantine or escalate when donor procedure would import donor law, donor math, donor action economy, donor skill check formats, donor spell slot economy, donor combat math, exact challenge assumptions, or sourcebook prose as Astra defaults.

Repeated donor action/cost/resolution patterns do not promote donor procedure to Astra law.

## 20. Runtime boundary

B02 does not own runtime entity/component/event/state schemas, runtime state/event/command lifecycle ownership, persistent campaign state, event-sourced state model, state delta validator, command lifecycle implementation, runtime command lifecycle, context packet compiler, hidden-information runtime state, backend validation, persistence, database contracts, event logs, or context packet formats.

Live-play behavior must not consume B02 procedure as runtime authority without later runtime validation. B02 may mark that runtime/canon/schema boundary risk exists, but it must route that risk to later runtime owners rather than implement runtime behavior.

## 21. Canon boundary

B02 does not promote final canon, accepted lexicon terms, setting facts, proper nouns, hidden truths, source-local lore, or canon eligibility. Any canon-sensitive declared action must route to canon review, lexicon review, source-local boundary handling, rejected donor element preservation, or `human_review`.

B02 examples are doctrine-facing only and are not canon entries, sourcebook statblocks, player-facing rule text, accepted lexicon, or sourcebook prose.

## 22. Live-play/training boundary

B02 does not define live-play narration behavior, player-facing prompt text, GM adapter behavior, training transcript policy, evaluation rubrics, or player-facing rule explanations. B02 can inform future training or runtime work only after later owners validate the procedure.

Live-play behavior must not consume B02 procedure as runtime authority without later runtime validation, and training examples must not treat `action_declaration_routing_note` as a command object, backend event, runtime schema, hidden-information runtime state, canon answer, or sourcebook prose.

## 23. Examples of good and bad B02 usage

Good B02 usage:
- Good: "The actor intends to cross the exposed bridge by moving slowly with a tether. The visible cost is time and exposure; hidden structural truth is not revealed. Because uncertainty and meaningful consequence are present, mark `roll_triggered` and route resolution to the owner. Route any damage, position, time, or information delta to the proper owner after resolution."
- Good: "The actor wants to inspect an unlocked, ordinary door in a calm scene. There is no meaningful uncertainty, opposition, or consequence. Mark `no_roll_required`; if no persistent information or position changes matter, mark `no_delta_required`."
- Good: "The donor text says this maneuver costs a named spell slot. Preserve the slot text as donor evidence, translate the intent/method/target/scope, mark `source_local_action_procedure`, and route cost questions to a resource owner without importing donor slot economy."
- Good: "The action would create a C-family conversion record but no family schema is ready. Use `batch_b_to_c_handoff` with `target_schema_family: pending_schema` and `unresolved_schema_gap_action: human_review` or `defer_until_schema_exists`."

Bad B02 usage:
- Bad: "Every declared action rolls d20 and combat initiative starts." This collapses declared actions into rolls and rolls into combat actions.
- Bad: "The DN is exactly 17 and overinvestment adds a fixed +3." This defines exact Difficulty Numbers, final d20 math, and final modifier ladders.
- Bad: "The preview says the hidden assassin is behind the curtain." This reveals hidden truth instead of marking a hidden-risk boundary.
- Bad: "Add new C07 fields for this action record." This invents C-family schema fields and C01-C14 schema contents.
- Bad: "Use the donor spell slot, action economy, and saving throw categories as Astra defaults." This imports donor action/cost/resolution formats as Astra defaults.
- Bad: "Store the note as a backend command event in persistent campaign state." This violates the runtime boundary.

## 24. Minimum tests or assertions

Minimum B02 assertions:
- B02 file exists at its expected path.
- Required sections are present.
- B02 declares ownership and non-ownership.
- B02 references B01 as upstream Batch B context.
- B02 includes C00 handoff language and `batch_b_to_c_handoff`.
- B02 includes `action_declaration_routing_note` and marks it as doctrine-facing only.
- B02 rejects final d20 math, exact DN values, dice/RNG implementation, final cost math, and final combat math.
- B02 rejects runtime state/event/command lifecycle ownership.
- B02 rejects C-family field invention and C01-C14 schema-content ownership.
- B02 rejects donor action/cost/resolution formats as Astra defaults.
- B02 includes no-roll decision logic and resolution trigger logic.
- B02 includes cost/risk preview and hidden-risk boundary language.
- B02 includes state-delta routing, quarantine, escalation, `human_review`, and `defer_until_schema_exists`.
- B02 references D00/D02/D03/D12/D19 only as draft source-pack/reference material, not final current doctrine authority.
- No B03-B11 files are created.
- No C01-C14 files are created or required by the test.
- No registry status is promoted to current.

## 25. Acceptance criteria

B02 is acceptable when it:
1. preserves B01 as upstream Batch B context and does not rewrite B01;
2. owns declared-action intake, clarification, feasibility triage, no-roll decisions, cost/risk preview, cost commitment, resolution trigger routing, action-to-delta routing, and source-local donor procedure quarantine;
3. states that a declared action is not automatically a roll, a roll is not automatically a combat action, and a cost is not automatically a resource spend;
4. prevents visible cost/risk preview from revealing hidden truth;
5. routes resolution to owners without defining final resolution math;
6. routes cost/resource questions without defining final cost prices, pool math, recharge math, or power economy formulas;
7. routes every meaningful action to at least one recognized delta owner or an explicit no-delta/quarantine/escalation/transition result;
8. routes C-family needs through C00 without inventing C-family fields or C01-C14 schema contents;
9. treats D00, D02, D03, D12, and D19 only as draft source-pack/reference material, not final current doctrine authority;
10. treats donor action/cost/resolution formats as donor evidence only;
11. keeps examples and blocks doctrine-facing only, not runtime state, backend contracts, sourcebook statblocks, canon entries, or player-facing rule text;
12. leaves registry status unpromoted and does not create B03-B11 or C01-C14 files.

## 26. Follow-up handoff to B03

B02 hands the next Batch B slot to B03. B03 may receive action sequencing, follow-up cadence, or later operational procedure only if explicitly drafted later. B02 does not create B03-B11, does not predefine B03 content, and does not treat future Batch B files as current authority.

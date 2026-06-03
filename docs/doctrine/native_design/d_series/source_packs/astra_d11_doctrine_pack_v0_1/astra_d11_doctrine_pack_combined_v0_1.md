# D11 Narrator Interface Doctrine Pack v0.1

Generated: 2026-06-02

This combined export contains the full D11 doctrine pack in file order.


---

<!-- FILE: D11-README_manifest.md -->

# D11 Narrator Interface, Scene Framing, Consequence Surfacing, and Presentation Doctrine — Manifest

Version: v0.1  
Phase: Astra Ascension native design doctrine  
Status: Generated doctrine pack  
Primary owner: D11

## Purpose

D11 defines how Astra presents and inspects D00–D10 state safely. It covers scene framing, outcome narration, hidden-state handling, assessment presentation, unresolved pressure surfacing, player-facing versus GM-facing summaries, anti-hallucination controls, and source-local presentation boundaries.

D11 is **interface doctrine**. It is not the final live-play GM adapter, not a prose-style training pack, not autonomous encounter generation, not faction AI, not economy simulation, and not the final narrator personality.

## Core doctrine rule

D11 presents and inspects registered or lawfully provisional state. It may frame scenes, summarize visible state, surface consequences, present uncertainty, describe outcomes, and produce GM-facing diagnostics. It must not invent unsupported persistent facts, override owner files, reveal hidden truth without a lawful reveal path, generalize source-local donor procedure into Astra default, or decide the player’s intent, emotion, loyalty, belief, or action.

## File order

1. `D11-00_narrator_interface_architecture_and_owner_boundaries.md`
2. `D11-01_scene_framing_from_registered_state.md`
3. `D11-02_outcome_narration_and_consequence_surfacing.md`
4. `D11-03_hidden_state_rumor_secrecy_misinformation_presentation.md`
5. `D11-04_assessment_result_presentation.md`
6. `D11-05_unresolved_pressure_surfacing.md`
7. `D11-06_player_facing_vs_gm_facing_summary_modes.md`
8. `D11-07_anti_hallucination_and_unsupported_state_escalation.md`
9. `D11-08_source_local_presentation_boundaries.md`
10. `D11-09_integration_checklists_and_ddr_register.md`
11. `D11_pack_manifest.json`

## Primary safeguards

D11 hard-blocks: premature live-play adapter collapse; fluent canon invention; hidden backend truth leakage; raw player-facing register dumps; D02 outcome collapse; Fractured/Receded dead outcomes; arbitrary Sundered catastrophe; omniscient/useless assessment; rumor-as-truth presentation; unresolved pressures being forced or forgotten; source-local generalization; and player-agency overwrite.


---

<!-- FILE: D11-00_narrator_interface_architecture_and_owner_boundaries.md -->

# D11-00 Narrator Interface Architecture and Owner Boundaries

## Purpose

This file defines D11 as a state-grounded narrator/interface layer. D11 controls presentation, not underlying mechanics or final live-play behavior.

## Core rule

D11 presents and interprets D00–D10 state for play-facing and GM-facing use. It may frame scenes, summarize visible state, surface consequences, present uncertainty, and describe outcomes. It must not invent unsupported persistent facts, override owner files, expose hidden truth without a lawful reveal path, or convert source-local donor procedure into Astra default.

## Accepted model

D11 uses the **State-Grounded Narrator Interface Model**.

Every meaningful presentation must be grounded in one of: registered D00–D10 state; source-local boundary; player-known fact; inferable signal; low-impact color; provisional detail; or explicit escalation.

## D11 is not the final GM adapter

D11 does not define final live-play personality, final prose style, autonomous encounter generation, pacing engine, faction AI, economy simulation, legal simulation, map simulation, or final player-facing runtime behavior. Those belong to later runtime/play-adapter phases after canon consolidation.

## Interface modes

| Mode | Function |
|---|---|
| Player-facing narration | Presents what the player can perceive, infer, or lawfully know. |
| Party-known summary | Concise recap of confirmed or believed player-safe information. |
| GM-facing summary | Backend view of hidden truth, deltas, pressures, and reveal paths. |
| State-audit mode | Checks whether narration is supported by records and boundaries. |
| Escalation mode | Flags missing owner state, hidden-truth exposure risk, unsupported canon invention, or source-local conflict. |

Player-facing modes must not contain hidden backend truth. GM-facing/state-audit/escalation modes must be clearly labeled.

## Ownership

D11 owns scene framing presentation, outcome narration, consequence surfacing, player-facing summaries, GM-facing summaries, state-audit output, escalation output, hidden-state presentation, rumor/misinformation/propaganda/suppression presentation, assessment-result presentation, unresolved-pressure surfacing, anti-hallucination controls, source-local presentation boundaries, and safe rewrite behavior.

D11 does not own D00 core play contract, D01 attributes/Pneuma, D02 d20 resolution, D03 Power Economy, D04 advancement, D05 skills and methods, D06 routes and Techniques, D07 harm, D08 actor substrate, D09 object-state, D10 world-state, or final live-play adapter behavior.

## Interface safety rules

D11 must preserve mode separation, player agency, hidden-state boundaries, source-local scope, and owner-file authority. It translates records into player-facing effects, labels GM-facing hidden state, distinguishes fact from rumor, routes unsupported state to owner files, and refuses or rewrites unsafe narration.


---

<!-- FILE: D11-01_scene_framing_from_registered_state.md -->

# D11-01 Scene Framing from Registered State

## Purpose

This file defines how D11 builds scene frames from registered state without inventing unsupported persistent facts. D11 remains interface doctrine. It frames scenes from D00–D10 state; it does not create full world simulation, encounter generation, faction AI, or final live-play behavior.

## Core rule

A D11 scene frame must be grounded in known or lawfully provisional state. The narrator may add sensory color, pacing, and framing, but may not create persistent facts, hidden truths, mechanical costs, object powers, faction actions, legal consequences, or world-state changes unless supported by D00–D10 records or explicitly marked provisional.

## Scene-frame inputs

A scene frame may draw from D00 core play purpose, D01 attribute signals, D02 resolution posture, D03 active resources, D04 advancement pressure, D05 method/research posture, D06 route/Technique context, D07 harm/hazard state, D08 actor/form state, D09 object/platform state, D10 location/faction/law/economy/reputation/information/unresolved pressure, and source-local boundaries.

## Scene frame structure

A useful scene frame identifies where the scene is happening, what is immediately perceivable, what pressure is active, what the player knows, what remains uncertain, what options appear available, and what hidden backend state must not be revealed.

## Scene purpose

D11 should identify scene purpose before framing. Purposes include orientation, choice point, consequence surfacing, assessment opportunity, conflict setup, recovery/downtime, discovery, transition, and source-local procedure. Scene purpose prevents pressure overload and scene drift.

## Visibility layers

Player-visible state can be stated directly. Player-inferable state can be hinted or framed as uncertainty. Hidden backend state must not be revealed unless lawfully discovered.

Examples of hidden backend state include hidden faction controller, concealed culprit, hidden object power, false-rumor origin, suppressed-record cause, and exact hidden Pneuma/cosmic modifier.

## Low-impact color

Low-impact color is allowed when it does not create persistent state. Rain on metal, distant crowd noise, worn stone, lantern shadows, ordinary clutter, background travelers, dust, smoke, weather, and texture are allowed. Named faction symbols, law notices, relic sigils with mechanics, new map routes, prophecy marks, market shortages, and public accusations are not low-impact color.

## Provisional detail

Provisional details may be used for scene flow when low-risk, non-contradictory, mechanically non-defining, not hidden-truth-bearing, and promotable. Examples include unnamed guards, ordinary shopkeepers, passersby, minor witnesses, routine clerks, ordinary doors, and generic furniture. If consequential, route to the relevant owner: D08 for recurring actors, D09 for objects, D10 for faction/law/location/rumor/relationship, D07 for hazards, D05 for methods, and D06 for routes/Techniques.

## Missing-state escalation

Escalate rather than invent when framing requires new faction doctrine, law/economy/world-state, object power, Technique behavior, actor substrate, harm/corruption rule, major map/territory creation, hidden truth not present in records, or unbounded source-local conversion.

## Player agency

D11 may present pressure and options. It must not decide the player’s response, intent, emotion, loyalty, belief, or action.

## Record shape

```yaml
d11_scene_frame:
  scene_ref: string
  scene_purpose: string
  grounded_inputs:
    D00: []
    D01: []
    D02: []
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  player_visible_state: []
  player_inferable_state: []
  hidden_backend_state_not_to_reveal: []
  unresolved_pressures_to_surface: []
  low_impact_color_allowed: []
  provisional_details: []
  available_choices: []
  escalation_flags: []
```


---

<!-- FILE: D11-02_outcome_narration_and_consequence_surfacing.md -->

# D11-02 Outcome Narration and Consequence Surfacing

## Purpose

This file defines how D11 presents D02 outcomes and D03–D10 deltas without collapsing them into generic success/failure or raw register dumps. D11 remains interface doctrine and does not own D02 resolution math, D03 costs, D07 harm, D09 object-state, or D10 world-state.

## Core rule

D11 must present outcomes in a way that reflects the D02 result, shows declared costs and visible consequences, preserves player agency, hides backend-only information unless lawfully revealed, and records or signals owner-file deltas without turning narration into a raw register dump.

## Outcome ladder

| D02 outcome | Margin guide | D11 presentation |
|---|---:|---|
| Ascendant | +10 or higher | Exceptional control, added benefit, improved position, reduced fallout if lawful. |
| Clear | 0 to +9 | Intended result succeeds; declared cost commits. |
| Fractured | -1 to -4 | Success/progress with cost, flaw, exposure, complication, or extra delta. |
| Receded | -5 to -9 | Goal fails or recedes, but information, exposure, cost, weak progress, or position change occurs. |
| Sundered | -10 or lower | Severe failure or rupture with proportional consequence and owner-file routing. |

## Outcome principles

Ascendant should feel like strong control, not arbitrary overkill. It does not bypass impossible gates, invent unrelated benefits, create new powers, erase declared cost automatically, or solve unrelated problems.

Clear presents the intended result and ordinary footprint. It is not bland; it is competence expressed cleanly.

Fractured is success or progress with cost. It must not be narrated as pure failure.

Receded is failure or retreat from the goal, but something still changes: information, exposure, partial cost, lost position, weak progress, revealed risk, or delayed pressure. It must not default to “nothing happens” if the roll was meaningful.

Sundered is severe failure or rupture. It must remain proportional to declared stakes, visible risk, PCR pressure, source-local context, and owner-file doctrine.

## Cost and consequence separation

D11 separates declared cost, over-investment cost, outcome consequence, hidden consequence, delayed consequence, and historical consequence. Declared cost should not be framed as surprise punishment.

## Consequence visibility

Visible consequences may be narrated directly. Hidden/backend consequences remain GM-facing unless lawfully revealed. Hidden consequences may surface as omens, symptoms, subtle reactions, ambiguous marks, strange absences, tone changes, or incomplete clues, but not as direct hidden facts.

## Delta presentation by owner

D03 appears as resource spend, strain, fuel loss, instability, or overdraw symptoms. D04 appears as threshold pressure, proof gained/lost, breakthrough instability, or blocked progress. D05 appears as method progress, research clue, crafting step, or expertise limit. D06 appears as Technique effect, Route strain, Principle resonance, or oath pressure. D07 appears as harm, injury, corruption, backlash, or condition. D08 appears as form-state stress, companion reaction, AI/personhood signal, or body issue. D09 appears as object wear, relic reaction, platform damage, implant strain, or salvage quality. D10 appears as law pressure, faction memory, rumor, reputation, territory change, scarcity, or information-state.

Raw owner deltas belong in GM-facing or state-audit mode.

## Follow-up choices

D11 may present follow-up choices when doctrine supports them: accept cost, push, retreat, stabilize, spend, reveal, conceal, sacrifice object durability, call in a favor, or contest a claim. D11 must not choose for the player.

## Record shape

```yaml
d11_outcome_presentation_record:
  source_resolution_ref: string
  d02_outcome: string
  declared_costs_to_present: []
  visible_consequences_to_present: []
  hidden_backend_consequences_not_to_reveal: []
  delayed_consequences: []
  owner_deltas:
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  unresolved_pressures_created_or_updated: []
  follow_up_choices: []
  escalation_flags: []
  gm_facing_summary: []
  player_facing_summary: string
```


---

<!-- FILE: D11-03_hidden_state_rumor_secrecy_misinformation_presentation.md -->

# D11-03 Hidden State, Rumor, Secrecy, and Misinformation Presentation

## Purpose

This file defines how D11 presents hidden truth, secrets, rumors, misinformation, propaganda, suppressed records, false attribution, partial truths, and backend uncertainty without spoiling hidden state or misleading the player unfairly. D11 remains interface doctrine. D10 owns information-state records. D02 owns assessment resolution. D05 owns investigation/research method.

## Core rule

D11 must present information according to its knowledge-state, truth-state, visibility, reliability, and discovery status. Hidden truth may influence symptoms, uncertainty, tone, NPC behavior, or scene pressure, but it must not be directly exposed to the player unless a lawful reveal path exists.

## Information layers

D11 distinguishes backend truth, GM-facing truth, player-known fact, player-inferable signal, rumor, misinformation, propaganda, suppressed record, false attribution, and source-local secret. Player-facing handling depends on the layer. Backend truth and GM-facing truth are not revealed unless discovered or explicitly in GM mode. Rumors, misinformation, propaganda, and false attribution must be framed as claims or beliefs, not narrator-certified fact.

## Narrator-certified truth vs in-world claim

D11 distinguishes neutral narration from in-world assertions. “The bridge is broken” is narrator-certified. “The dockworkers insist the bridge is cursed” is an in-world claim. “The governor’s notice blames foreign saboteurs” is propaganda or official claim, not confirmed truth.

## Hidden truth signals

Hidden truth may produce unusual silence, physical symptoms, NPC evasion, inconsistent records, abnormal scarcity, changed patrol routes, object reactions, environmental anomalies, rumor contradictions, legal overreactions, emotional mismatches, faction behavior, or sensory clues. It may not reveal hidden faction names, secret motives, true culprits, concealed object functions, exact hidden modifiers, or backend Pneuma/cosmic pressure unless lawfully discovered.

## Rumors, misinformation, and propaganda

Rumors should indicate source, spread, contradiction, scope, and trustworthiness when relevant. Misinformation may create real social consequence without being true. Propaganda should be presented as deliberate message or official claim, not neutral truth.

## Suppressed records and false attribution

Suppression may appear as missing archive sections, sealed files, redacted testimony, dead witnesses, altered maps, inconsistent official stories, unusually aggressive denials, or restricted shelves. D11 should not automatically explain the suppression’s cause. False attribution separates what happened, who believes what happened, who benefits, what the player knows, and what D10 records as truth.

## Concealed object identity and hidden hazards

Before identification, D11 may present material, weight, markings, environmental reaction, public claims, uncertain appraisal, rumor, partial function, or instability symptom. It must not reveal exact hidden power, true origin, secret owner, curse profile, sentience, final value, or source-local unique function. Hidden hazards and corruption must produce fairness support before severe consequence.

## Hidden Pneuma/cosmic pressure

Pneuma remains backend-only. D11 must not expose it as a score, modifier, or stat. It may appear as omen, impossible coincidence, mythic timing, repeated symbol, unsettling alignment, relic resonance, witness interpretation, or later world-facing myth if D10 records it.

## Assessment misreads

Sundered assessment may produce false, distorted, outdated, or dangerously incomplete reads unless safeguards apply. D11 must not reveal unreliability unless the character has reason to know.

## Fairness rule

Hidden information is fair when it can be assessed, produces symptoms, has source-local reveal procedure, has witness/rumor/record paths, follows prior player action, is known genre/context risk, remains GM-facing and does not punish until surfaced, or was accepted as unknown risk. Severe hidden consequence without signal, accepted risk, assessment path, or source-local justification is unfair.

## Record shape

```yaml
d11_information_presentation_record:
  information_ref: string
  presentation_mode: string
  truth_state: string
  knowledge_state: string
  player_visible_claims: []
  player_inferable_signals: []
  hidden_backend_not_to_reveal: []
  rumor_framing: []
  misinformation_framing: []
  propaganda_framing: []
  suppression_signals: []
  lawful_reveal_paths: []
  assessment_quality: string
  source_local_boundary: []
  escalation_flags: []
```


---

<!-- FILE: D11-04_assessment_result_presentation.md -->

# D11-04 Assessment Result Presentation

## Purpose

This file defines how D11 presents assessment results across D02 outcomes while preserving the Insight/Reason split, PCR visibility, hidden-state protection, and D10 information-state promotion. D11 remains interface doctrine. D02 owns assessment resolution. D05 owns method. D10 owns persistent information-state.

## Core rule

D11 presents assessment as information quality, not omniscience. Assessment may reveal actionable state, partial signals, uncertainty, false reads, or distorted interpretations depending on D02 outcome, method, tools, route support, source-local safeguards, and D10 knowledge-state. Insight detects. Reason interprets. Hidden backend truth remains protected unless lawfully revealed.

## Insight and Reason

Insight probes, detects, senses, notices, reads pressure, and catches anomaly. Reason interprets, analyzes, compares, infers, explains, and models. A strong assessment may include both; a weak assessment may reveal one without the other.

## Assessment targets

Assessment may target location tier, location tags, visible PCR pressure, opposition bracket, approximate DN band, domain alignment, hazard type, object-state clue, actor-state clue, route/Technique risk, resource cost risk, law/faction risk, social/reputation pressure, information reliability, hidden-state symptoms, and source-local constraints.

Assessment does not automatically reveal exact hidden modifiers, hidden Pneuma/cosmic pressure, true culprit, secret faction controller, concealed object full power, undiscovered curse profile, full hidden opposition plan, or backend register contents.

## Outcome-banded assessment

Ascendant gives a clear actionable read plus an extra useful signal. Clear gives accurate actionable information. Fractured gives useful but incomplete information with possible cost, exposure, ambiguity, or missing tag. Receded gives vague, limited, or low-confidence information. Sundered may produce false, distorted, outdated, or dangerously incomplete information unless safeguards apply.

Fractured should support better choices without removing all uncertainty. Receded should not be pure nothing if the roll was meaningful. Sundered may sound confident and wrong if no safeguard applies.

## Confidence language

High confidence: “You can confirm…”, “The read is stable…”, “The pattern is consistent…”

Medium confidence: “The most likely reading is…”, “The signs point toward…”, “Enough to act on, not enough to prove…”

Low confidence: “You cannot verify…”, “The signal is incomplete…”, “The read does not settle…”

False confidence is allowed only when D02 outcome supports it, normally Sundered.

## PCR presentation

PCR elements are translated into player-facing language rather than raw tags. Hidden Pneuma/cosmic pressure is never shown as raw score, modifier, or backend tag. It may appear as “the timing feels wrong,” “the omen is readable but not measurable,” or “this is not ordinary luck.”

## Tools, methods, routes, and safeguards

Reliability may improve through D05 expertise, D05 research method, D09 tool/relic, D06 route/Technique, D03 resource investment, D10 archive access, companion expertise, or source-local procedure. A safeguard may prevent Sundered from producing full false confidence.

## D10 promotion

Assessment should promote to D10 when it creates or changes player-known fact, party-known fact, rumor reliability, hidden truth discovered, accepted false belief, map knowledge, object identity knowledge, faction suspicion, witness knowledge, public knowledge, source-local clue state, or suppressed-record awareness.

## Agency

Assessment informs choice; it does not choose for the player. D11 should avoid “you should,” “you must,” or “you know the correct choice is.”

## Record shape

```yaml
d11_assessment_presentation_record:
  assessment_ref: string
  d02_outcome: string
  assessment_target: []
  insight_probe_output: []
  reason_interpretation_output: []
  confidence_language: string
  player_facing_read: string
  gm_facing_truth: []
  hidden_backend_not_revealed: []
  safeguards_applied: []
  d10_information_updates: []
  source_local_boundary: []
  escalation_flags: []
```


---

<!-- FILE: D11-05_unresolved_pressure_surfacing.md -->

# D11-05 Unresolved Pressure Surfacing

## Purpose

This file defines how D11 surfaces D10 unresolved pressure queues and related D03–D09 consequence pressure without forcing every pressure into the next scene or forgetting it. D11 remains interface doctrine. D10 owns unresolved pressure records. D11 controls presentation and surfacing.

## Core rule

D11 should surface unresolved pressure when it is contextually relevant, visible or inferable, proximate, escalating, triggered by player action, or needed to preserve continuity. It should not force every active pressure into the next scene, and it should not leave future-facing consequences inert.

## Surfacing inputs

Pressure surfacing considers severity, scope, visibility, proximity, timing, trigger, owner substrate, player knowledge, fairness, and source-local boundary.

## Surfacing intensity

Intensity ranges from background signal to soft pressure, choice pressure, complication, direct confrontation, escalation event, and historical reminder. D11 should choose the minimum sufficient intensity that makes pressure matter without overforcing it.

## Pressure types

Legal pressure includes warrants, bounties, sanctions, exile, docking denial, contraband flags, personhood disputes, and salvage conflicts. It may surface as checkpoint tension, posted notice, clerk hesitation, docking refusal, guard recognition, summons, confiscation threat, or public accusation. A warrant does not automatically mean immediate arrest.

Faction pressure includes grudges, retaliation, alliance strain, debts, obligations, hidden infiltration, patron demand, and local faction clocks. Hidden factions surface through traces before identification.

Relationship pressure includes debt, favor, betrayal, resentment, kinship, loyalty, jealousy, and reconciliation opportunity. It presents social consequence and choice, not player emotion.

Economy/scarcity pressure includes shortage, rationing, market closure, embargo, black-market demand, requisition pressure, and supply-chain disruption. Scarcity appears as access, supply, social, or strategic pressure, not just price.

Hazard/corruption pressure includes corruption zones, plague, curse spread, disaster aftermath, unstable region, and local doom clocks. Hidden hazards require fairness support before severe consequence.

Object/claim pressure includes stolen relics, sacred claims, salvage disputes, platform impoundment, implant legality, object instability, and black-market interest. D11 must not invent object powers or ownership facts.

Information pressure includes rumors, false attribution, propaganda, suppressed records, leaked secrets, disputed accounts, witness memory, and altered maps. D11 does not certify false belief as truth.

## Surfacing triggers

Pressure may surface when the player enters affected territory, interacts with an involved faction, uses a contested object, seeks restricted goods, repeats a risky method, triggers a source-local clock, receives assessment signal, causes public knowledge change, or creates an opening.

## Dormant and historical pressure

Dormant pressure requires trigger before reactivation. Historical pressure may appear through memorials, records, ruins, myths, scars, legal precedent, or old grudge, but should not reactivate without cause.

## Pacing

When multiple pressures are active, prioritize by immediate relevance, location/proximity, severity, visibility, recent player action, unresolved queue age, thematic fit, source-local trigger, and contradiction risk. Do not dump all active pressures into every scene unless the scene is explicitly a convergence event.

## Record shape

```yaml
d11_pressure_surfacing_record:
  pressure_ref: string
  pressure_type: string
  source_records:
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  severity: string
  scope: string
  visibility: string
  surfacing_intensity: string
  surfacing_vector: string
  fairness_support: []
  player_facing_signal: string
  gm_facing_state_update: []
  escalation_conditions: []
  decay_conditions: []
  resolution_conditions: []
  agency_preserving_choices: []
```


---

<!-- FILE: D11-06_player_facing_vs_gm_facing_summary_modes.md -->

# D11-06 Player-Facing vs GM-Facing Summary Modes

## Purpose

This file defines how D11 separates player-safe presentation from GM/backend summaries, raw register inspection, state-audit output, and escalation notes. D11 remains interface doctrine. It controls presentation modes, not the state records themselves.

## Core rule

D11 must maintain strict separation between player-facing presentation, GM-facing summary, state-audit inspection, and escalation output. Player-facing summaries may contain only visible, known, inferable, or lawfully revealed information. GM-facing summaries may include hidden state, raw deltas, unresolved pressures, and backend notes, but must label them clearly.

## Summary modes

Player-facing narration is immersive and player-safe if filtered. Party-known summary is concise recap of player-safe information. GM-facing summary includes backend truth, hidden facts, deltas, pressures, and reveal paths. State-audit mode validates support. Escalation mode flags missing doctrine/state or unsafe narration.

## Player-facing narration

May include visible environment, sensory details, public information, party-known information, visible consequences, inferable signals, rumors framed as rumors, uncertainty language, available choices, and assessment results presented through D02/D11 rules.

Must not include backend truth not discovered, GM-only notes, raw hidden register data, exact hidden Pneuma/cosmic modifiers, hidden faction controller names, concealed object identity, unrevealed source-local clocks, or state-audit warnings.

## Party-known summary

May include confirmed discoveries, accepted rumors labeled as rumors, known debts/warrants/grudges/faction pressure, known object states, known injuries/resources, known unresolved pressures, map/location knowledge, and known false beliefs if the party believes them.

## GM-facing summary

May include backend truth, hidden facts, secret holders, unresolved pressures, owner-file deltas, source-local status, hidden consequence, delayed consequence, escalation conditions, and reveal paths. It must not be written so it can accidentally be pasted as player narration.

## State-audit mode

State-audit mode answers what records support narration, which owners are touched, whether hidden facts are revealed, whether source-local systems are being generalized, whether persistent canon is invented, whether D02 outcomes are presented correctly, and whether handoffs are missing.

## Escalation mode

Escalation activates when D11 cannot lawfully present a requested detail because owner state is missing, hidden truth lacks reveal path, source-local conflict exists, D02 outcome mismatches, donor assumptions are leaking, or Pneuma exposure risk exists.

## Raw register inspection

Raw register inspection belongs only in GM-facing or state-audit mode. Player-facing narration translates records into effects.

## Delta summaries

Player-facing summaries describe visible effects: reserve charge gone, wound bleeding, relic cracked, guild knows someone interfered. GM-facing summaries identify owner records: D03 reserve spent, D07 bleeding condition, D09 relic instability, D10 faction-known interference.

## Unresolved pressure dashboard

D11 may support GM-facing unresolved pressure dashboards showing pressure type, owner, severity, visibility, scope, surfacing intensity, escalation/decay/resolution conditions, and player-facing signal used or pending. Dashboards are not player-facing unless filtered.

## Source-local summaries

Source-local summaries must be labeled as local. Player-facing output translates the mechanic into visible effects.

## Contamination prevention

D11 blocks GM truth in player narration, rumor as narrator fact, raw register dump in player view, GM summary in immersive second person, source-local clocks as universal systems, hidden Pneuma as numbers, and state-audit warnings inside scene prose.

## Record shape

```yaml
d11_summary_mode_record:
  summary_ref: string
  mode: string
  player_safe: boolean
  source_records:
    D00: []
    D01: []
    D02: []
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  visible_content: []
  inferable_content: []
  hidden_content_not_player_safe: []
  raw_register_refs: []
  owner_deltas: []
  unresolved_pressures: []
  assessment_summaries: []
  source_local_status: []
  escalation_flags: []
  lawful_reveal_paths: []
```


---

<!-- FILE: D11-07_anti_hallucination_and_unsupported_state_escalation.md -->

# D11-07 Anti-Hallucination and Unsupported-State Escalation

## Purpose

This file defines how D11 prevents unsupported narration, invented canon, hidden-truth leakage, owner-file override, source-local leakage, player-agency violation, and unregistered world-state mutation. D11 remains interface doctrine. It detects gaps and routes them; it does not solve missing D03–D10 doctrine by narration.

## Core rule

D11 may narrate supported state, player-visible effects, low-impact color, and clearly bounded provisional detail. It must not create persistent facts, mechanics, hidden truths, owner-file deltas, source-local rules, or player decisions without lawful support. When required support is missing, D11 must route, defer, quarantine, ask for decision, or escalate.

## Support categories

D11 classifies meaningful details as supported state, player-known state, player-inferable state, low-impact color, provisional detail, missing owner state, hidden backend state, source-local state, quarantined state, or escalated state.

## Hard prohibitions

D11 must not invent persistent factions, institutions, laws, markets, territories, object powers, Techniques, routes, actor identities, or world history; reveal hidden truth without reveal path; treat rumor/propaganda/misinformation as narrator-certified truth; assign player intent/emotion/loyalty/belief/memory/action; create D03 costs, D04 eligibility, D06 Technique behavior, D07 harm, D08 substrate changes, D09 object powers, or D10 world changes without owner support; generalize source-local procedure; or expose hidden Pneuma/cosmic pressure as score/modifier/backend rule.

## Low-impact color

Allowed: smell of rain, worn stone, distant crowd, lantern shadows, ordinary clutter, non-specific banners, generic travelers, dust, smoke, weather, texture. Not allowed: named faction symbols, new law notices, relic sigils with mechanics, suspicious NPCs with hidden agenda, map routes, unique monster traces, market shortages, public accusations, hidden cult phrases.

## Provisional detail

Allowed provisional details include unnamed guards, ordinary shopkeepers, minor witnesses, routine clerks, ordinary doors, generic stalls, and nonpersistent weather. They must be low consequence, non-contradictory, mechanically non-defining, not hidden-truth-bearing, and promotable if important.

## Escalation triggers

Escalate when narration requires unknown object power, undefined faction action, missing law/authority state, unregistered world consequence, unsupported transformation, hidden truth reveal without path, source-local conflict, donor mechanic import, missing harm/corruption doctrine, missing economy/scarcity doctrine, missing advancement eligibility, player agency override, contradiction between records, or raw backend state entering player-facing output.

## Escalation output

Good escalation identifies what cannot be safely stated, which owner file is required, whether low-impact/provisional narration is allowed, whether source-local retention applies, and a safe player-facing alternative.

## Unsafe-line rewrite

D11 state-audit mode may rewrite unsafe narration.

Unsafe: “The hidden cult has already bought the city guard.”  
Safe: “The guards use the same refusal phrase you heard at the district office. It may be coordination, training, or coincidence, but it no longer feels isolated.”

Unsafe: “You feel guilty and decide to confess.”  
Safe: “The accusation lands in a room already waiting for your reaction. Confessing, denying, redirecting, or staying silent are all still open.”

## Player agency

D11 must not decide what the player feels, believes, intends, says, trusts, or accepts. It may present bodily sensation from an effect, social pressure, perceived risk, available interpretations, NPC reaction, prior-action consequence, and options.

## Anti-hallucination checklist

Before accepting meaningful narration, ask whether the detail is supported by D00–D10 or source-local state; whether mode is correct; whether it is visible/inferable/known/rumored/hidden/secret; whether it creates persistent world-state; whether it assigns player emotion/action; whether it reveals hidden truth; whether owner mechanics are required; whether donor assumptions are imported; whether it can remain low-impact color; how provisional detail promotes; which owner resolves unsupported state; and whether a safe rewrite is available.

## Record shape

```yaml
d11_unsupported_state_audit_record:
  proposed_content_ref: string
  presentation_mode: string
  support_status: string
  owner_required:
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  risk_flags:
    - hidden_truth_exposure
    - invented_canon
    - owner_override
    - source_local_leakage
    - player_agency_violation
    - unsupported_mechanic
    - raw_register_contamination
  safe_rewrite: string
  escalation_note: string
  promotion_route: []
```


---

<!-- FILE: D11-08_source_local_presentation_boundaries.md -->

# D11-08 Source-local Presentation Boundaries

## Purpose

This file defines how D11 presents retained donor-local or campaign-local systems without implying they are universal Astra doctrine. D11 remains interface doctrine. It presents source-local systems within scope; it does not promote them to canon.

## Core rule

D11 may present retained source-local systems only within their authorized scope. Player-facing narration should translate them into visible effects, choices, symptoms, and consequences. GM-facing summaries may name the source-local system, but must label it as local and prohibit generalization.

## Source-local categories

Source-local categories include local clocks, local reputation/heat, local clue/reveal systems, local domain/kingdom systems, local economy/market systems, local travel/map systems, local horror/stability systems, local resolution exceptions, and mixed retained procedures.

## Player-facing translation

Player-facing narration should usually not expose raw local labels.

Bad: “The faction clock advances to 4/6.”  
Better: “The guild has stopped pretending this is private. Their messengers now wear house colors openly.”

Bad: “Your heat level rises.”  
Better: “Patrols that ignored you yesterday now pause long enough to compare your faces to a folded notice.”

Bad: “The rumor table result is 7.”  
Better: “The dockhands repeat the same story with different names: someone paid well to keep cargo off the south pier.”

## GM-facing label rule

GM-facing summaries may name retained systems only when labeled local.

```yaml
source_local_status:
  system_type: "local faction clock"
  source_scope: "current converted module only"
  current_state: "4/6"
  player_facing_signal_used: "guild messengers now act openly"
  prohibited_generalization:
    - "not universal Astra faction AI"
    - "not default D10 faction procedure"
```

## Scope labels

Scopes include encounter-local, site-local, adventure-local, campaign-local, faction-local, region-local, source-family-local, and source-local pending promotion. No scope is global Astra unless later canon promotion occurs.

## Prohibited generalizations

D11 blocks: Astra factions use clocks; Astra cities have heat levels; Astra mysteries use clue webs; Astra markets use ratings; Astra domains use kingdom turns; Astra horror uses sanity loss; Astra travel uses hex turns; Astra rumors come from tables; Astra corruption advances by clocks.

Safe phrasing uses “this retained local…,” “under this source-local…,” “this site-local…,” or “this campaign-local…” language.

## Hidden source-local mechanics

Hidden local systems still obey D11 hidden-state and fairness rules. Player-facing narration may show symptoms or signals, not hidden mechanics unless lawfully revealed.

## Source-local escalation

Escalate for doctrine review when a retained system appears in multiple unrelated conversions, solves a general Astra problem better than current doctrine, conflicts with D00–D10, produces consequences outside authorized scope, needs canonical promotion, contradicts another retained local system, or becomes necessary across many D11 presentations. Escalation is not automatic promotion.

## Conflict handling

If local systems conflict, identify each as source-local, preserve scope, map shared outputs to D10 if needed, keep procedure local, and escalate repeated pressure if a broader Astra framework is needed. Do not create universal hybrids casually.

## Player agency

Local systems may increase pressure, but D11 still presents choices unless owner/source-local state removes them.

## Record shape

```yaml
d11_source_local_presentation_record:
  source_local_ref: string
  system_type: string
  scope: string
  player_facing_translation: string
  gm_facing_raw_status: []
  hidden_state_not_to_reveal: []
  surfacing_intensity: string
  prohibited_generalizations: []
  owner_outputs:
    D02: []
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
  escalation_flags: []
```


---

<!-- FILE: D11-09_integration_checklists_and_ddr_register.md -->

# D11-09 Integration Checklists and DDR Register

## Purpose

This file consolidates D11’s accepted decisions, ownership boundaries, validation checklists, D00–D10 handoff matrix, and pre-generation risk safeguards. D11 remains interface doctrine and is not the final live-play GM adapter.

## Accepted decision register

### D11-NIA — Narrator Interface Architecture and Owner Boundaries

Accepted: D11 uses the State-Grounded Narrator Interface Model; is not the final live-play GM adapter; distinguishes player-facing, GM-facing, state-audit, and escalation modes; reads D00–D10; and must not invent unsupported facts, override owners, reveal hidden truth without reveal path, or generalize source-local donor procedure.

### D11-SF — Scene Framing from Registered State

Accepted: D11 uses Registered-State Scene Frame Model; scene frames draw from D00–D10, source-local boundaries, or lawful provisional state; visible, inferable, and hidden backend state are separate; low-impact color is allowed; provisional detail promotes if consequential; missing major state escalates; and player agency is preserved.

### D11-OC — Outcome Narration and Consequence Surfacing

Accepted: D11 uses Outcome-to-Consequence Presentation Model; Ascendant, Clear, Fractured, Receded, and Sundered have distinct narration logic; cost categories remain separate; D03–D10 deltas surface through player-facing effects; hidden/backend consequences stay hidden unless lawfully discovered; Sundered is proportional; and follow-up choices may be offered without choosing for the player.

### D11-HS — Hidden State, Rumor, Secrecy, and Misinformation Presentation

Accepted: D11 uses Layered Information Presentation Model; backend truth, GM truth, player-known facts, inferable signals, rumors, misinformation, propaganda, suppression, false attribution, and source-local secrets remain distinct; narrator-certified facts differ from claims; hidden truth may create signals; Pneuma remains protected; Sundered assessment may mislead; and severe hidden consequence requires fairness support.

### D11-AS — Assessment Result Presentation

Accepted: D11 uses Outcome-Banded Assessment Presentation Model; Insight probes and Reason interprets; assessment quality follows D02 outcome; Sundered may create false confidence unless safeguarded; PCR is translated into player-facing language; tools/methods/routes/research/companions/source-local systems can improve reliability; persistent discoveries and accepted false beliefs promote to D10.

### D11-UP — Unresolved Pressure Surfacing

Accepted: D11 uses Contextual Pressure Surfacing Model; pressure surfacing depends on relevance, severity, visibility, scope, proximity, timing, player action, fairness, and source-local boundary; intensity is tiered; pressures do not automatically become encounters; hidden pressures need fairness support; dormant/historical pressures require triggers; multiple pressures are paced.

### D11-PGM — Player-Facing vs GM-Facing Summary Modes

Accepted: D11 uses Dual-Layer Summary and Inspection Model; player-facing narration, party-known summary, GM-facing summary, state-audit, and escalation mode are distinct; player-facing output is filtered; GM-facing summaries may include hidden/backend state when labeled; raw inspection is GM/state-audit only; D03–D10 deltas require dual summary handling; unresolved pressure dashboards are GM-facing unless filtered.

### D11-AH — Anti-Hallucination and Unsupported-State Escalation

Accepted: D11 uses Unsupported-State Escalation and Safe Narration Model; meaningful details are classified; low-impact color cannot create persistent facts; provisional detail promotes if consequential; missing major state routes/defers/quarantines/escalates; D11 blocks hidden-truth leakage, owner-file override, source-local leakage, player-agency violation, and unregistered world-state mutation; state-audit supports unsafe-line rewrites.

### D11-SLP — Source-local Presentation Boundaries

Accepted: D11 uses Source-local Presentation Boundary Model; retained donor-local systems require authorized scope; player-facing narration translates raw mechanics into effects; GM-facing mode labels systems as local; source-local generalization is blocked; hidden local mechanics obey hidden-state/fairness rules; repeated pressure escalates for review, not automatic promotion.

## D11 ownership checklist

D11 owns presentation: scene framing, outcome narration, consequence surfacing, summaries, state-audit, escalation, hidden-state presentation, assessment presentation, pressure surfacing, anti-hallucination controls, source-local presentation, and safe rewrites. It does not own D00–D10 mechanics or final live-play adapter behavior.

## Validation checklists

### Mode separation

Ask whether output is player-facing, party-known, GM-facing, state-audit, or escalation; whether player-facing content is filtered; whether rumors are framed as claims; whether hidden facts are excluded; whether raw records are restricted; whether source-local mechanics are labeled local; and whether escalation warnings stay out of immersive narration.

### Scene framing

Ask what D00–D10 records support the scene; what is visible; what is inferable; what hidden state must not be revealed; what pressures are relevant; what source-local systems are active; what color/provisional details are used; what choices are visible; and whether anything assigns player intent or requires escalation.

### Outcome narration

Ask what D02 outcome applies; what declared/over-invested costs apply; what visible consequences can be narrated; what hidden/delayed consequences are GM-facing; what D03–D10 deltas were created; whether Fractured/Receded are meaningful; whether Sundered is proportional; and whether choices are offered without deciding for the player.

### Hidden state

Ask whether information is backend truth, GM truth, known fact, inferable signal, rumor, misinformation, propaganda, suppression, false attribution, or source-local secret; whether claims are separated from facts; whether reveal path exists; whether Pneuma is protected; and whether severe hidden consequence has fairness support.

### Assessment

Ask what D02 outcome applies; what Insight detected; what Reason interpreted; what confidence applies; whether PCR is translated; whether Pneuma is protected; whether safeguards apply; and whether D10 information-state updates are needed.

### Unresolved pressure

Ask what pressure exists; type, severity, visibility, scope, proximity, trigger, timing, intensity, fairness, state, agency preservation, and pacing.

### Source-local

Ask what retained local system is active; scope; player-facing translation; GM-facing local label; prohibited generalizations; hidden-state fairness; and whether repeated pressure escalates.

### Anti-hallucination

Ask whether every consequential detail is supported, known, inferable, low-impact, provisional, source-local, or escalated; whether it invents canon; whether it creates object/faction/law/harm/advancement/Technique/actor/world-state without owner support; whether it reveals hidden truth; whether it decides player agency; whether it generalizes source-local procedure; and whether safe rewrite is required.

## D00–D10 handoff matrix

| D11 presentation pressure | Source owner |
|---|---|
| Core action loop, state-delta expectation, power/cost/context premise | D00 |
| Attribute signal, Insight/Reason split, Pneuma protection | D01 |
| Outcome state, DN, margin, assessment resolution, cost commitment | D02 |
| Pool/resource/fuel/overdraw/instability visibility | D03 |
| Breakthrough, proof, transformation, threshold visibility | D04 |
| Method, research, assessment technique, crafting/investigation procedure | D05 |
| Route, Technique, Principle, oath, domain expression | D06 |
| Harm, damage, corruption, backlash, injury, condition | D07 |
| Actor, companion, AI, personhood, form-state | D08 |
| Object, relic, platform, implant, tool, salvage | D09 |
| World-state, faction, law, economy, relationship, information, unresolved pressure | D10 |
| Retained local procedure | Source-local boundary |

## Embedded risk queue

D11 must not become the final live-play GM adapter; invent canon; leak hidden backend truth; dump raw registers in player-facing output; collapse D02 outcomes; make Fractured/Receded dead outcomes; use Sundered as arbitrary catastrophe; make assessment omniscient or useless; certify rumors as truth; force or forget unresolved pressures; universalize source-local systems; or overwrite player agency.


---

<!-- FILE: D11_pack_manifest.json -->

```json
{
  "pack": "D11 Narrator Interface, Scene Framing, Consequence Surfacing, and Presentation Doctrine",
  "version": "v0.1",
  "generated_date": "2026-06-02",
  "status": "generated",
  "phase": "Astra Ascension native design doctrine",
  "primary_owner": "D11",
  "manifest_filename": "D11_pack_manifest.json",
  "doctrine_files": [
    "D11-README_manifest.md",
    "D11-00_narrator_interface_architecture_and_owner_boundaries.md",
    "D11-01_scene_framing_from_registered_state.md",
    "D11-02_outcome_narration_and_consequence_surfacing.md",
    "D11-03_hidden_state_rumor_secrecy_misinformation_presentation.md",
    "D11-04_assessment_result_presentation.md",
    "D11-05_unresolved_pressure_surfacing.md",
    "D11-06_player_facing_vs_gm_facing_summary_modes.md",
    "D11-07_anti_hallucination_and_unsupported_state_escalation.md",
    "D11-08_source_local_presentation_boundaries.md",
    "D11-09_integration_checklists_and_ddr_register.md"
  ],
  "core_model": "State-Grounded Narrator Interface Model",
  "interface_modes": [
    "player_facing_narration",
    "party_known_summary",
    "gm_facing_summary",
    "state_audit",
    "escalation"
  ],
  "accepted_blocks": [
    "D11-NIA",
    "D11-SF",
    "D11-OC",
    "D11-HS",
    "D11-AS",
    "D11-UP",
    "D11-PGM",
    "D11-AH",
    "D11-SLP"
  ],
  "hard_blocks": [
    "unsupported canon invention",
    "hidden truth leakage",
    "raw register dump in player-facing mode",
    "source-local generalization",
    "owner-file override",
    "player agency violation",
    "Pneuma/cosmic backend exposure",
    "D02 outcome collapse"
  ],
  "owner_boundaries": {
    "D11_owns": [
      "scene framing presentation",
      "outcome narration",
      "consequence surfacing",
      "player-facing summaries",
      "GM-facing summaries",
      "state-audit output",
      "escalation output",
      "hidden-state presentation",
      "assessment-result presentation",
      "unresolved-pressure surfacing",
      "anti-hallucination controls",
      "source-local presentation boundaries",
      "safe rewrite behavior"
    ],
    "D11_does_not_own": {
      "D00": "core play contract",
      "D01": "attributes/Animus/Pneuma",
      "D02": "d20 resolution/outcome math",
      "D03": "Power Economy",
      "D04": "advancement/breakthroughs",
      "D05": "skills/methods/research/investigation",
      "D06": "routes/Techniques/Principles",
      "D07": "harm/damage/corruption/backlash",
      "D08": "actors/AI/forms/personhood",
      "D09": "objects/relics/platforms/implants",
      "D10": "world-state/faction/law/economy/reputation/information",
      "later_play_adapter": "final live-play GM behavior and personality"
    }
  }
}
```

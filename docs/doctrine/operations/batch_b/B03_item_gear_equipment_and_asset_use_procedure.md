# B03 Item, Gear, Equipment, and Asset Use Procedure

## 1. Purpose and status

B03 is the third Batch B operational doctrine draft for Astra item, gear, equipment, object-system construct, and asset-use handling during play/conversion procedure. It sits after B01 scene/activity/encounter procedure and B02 action declaration/cost commitment/resolution trigger procedure. B03 explains how object use is declared after a B02 action declaration, classified for operational handling, checked for holding/access/readiness/custody, and routed to owner files without defining final object schemas, item stats, damage or armor math, runtime inventory state, C-family schema fields, canon equipment lists, live-play behavior, or sourcebook prose.

Status posture:
- This file is Batch B operational-procedure draft material.
- This file is not current canon, not final mechanics, not runtime authority, not sourcebook prose, and not player-facing rule text.
- C00 remains the schema handoff control surface for Batch B to C-family routing.
- B03 treats `B01_scene_encounter_and_activity_procedure.md` and `B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` as upstream Batch B context and must build on them, not rewrite them.
- D00, D02, D03, D09, D17, and D19 source-pack files are referenced only as draft source-pack/reference material. They are not current doctrine authority, final mechanics, runtime authority, canon, or sourcebook prose.
- B03 records, examples, and handoff blocks are doctrine-facing only; they are not runtime state, backend contracts, database contracts, event logs, command lifecycle artifacts, item statblocks, sourcebook statblocks, canon entries, or live-play scripts.

Required reference boundaries preserved by B03:
- `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md` for upstream Batch B scene, activity, encounter, checkpoint, transition, and owner-file handoff procedure.
- `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` for upstream Batch B action declaration, feasibility, cost commitment, no-roll/roll-trigger, and action-to-delta routing procedure.
- `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` for shared Batch C base fields, `pending_schema`, source-local boundary, rejected donor element, canon eligibility, review routing, provenance, and missing-schema fallback language.
- `docs/doctrine/native_design/d_series/source_packs/astra_d00_doctrine_pack_v0_1/D00-03_state_delta_commit_protocol.md` for the draft source-pack principle that every meaningful action commits at least one delta to a recognized owner, while B03 does not own every delta format.
- `docs/doctrine/native_design/d_series/source_packs/astra_d02_doctrine_pack_v0_1/D02-00_resolution_architecture_and_owner_boundaries.md` for draft source-pack resolution owner boundaries, while B03 must not promote D02 math or any donor d20 assumptions.
- `docs/doctrine/native_design/d_series/source_packs/astra_d03_doctrine_pack_v0_1/astra_d03_doctrine_pack_v0_1/D03_01_power_economy_lattice.md` for draft source-pack power economy and power-interface pressure, while B03 must not define final resource, charge, fuel, reservoir, recharge, overdraw, or power economy math.
- `docs/doctrine/native_design/d_series/source_packs/astra_d09_doctrine_pack_v0_1/D09-00_layered_object_state_architecture.md` and `docs/doctrine/native_design/d_series/source_packs/astra_d09_doctrine_pack_v0_1/D09-02_weapons_armor_tools_foci_consumables_and_materials.md` for draft source-pack object-state and functional object-family source material, while B03 must not promote D09 object records to final schema.
- `docs/doctrine/native_design/d_series/source_packs/D17_economy_acquisition_inventory_reward_and_requisition_doctrine_pack/D17_doctrine_pack/D17-04_inventory_storage_carrying_custody_quick_access_and_burden_procedure.md` for draft source-pack inventory, storage, carrying, custody, quick-access, and burden pressure, while B03 must not define final capacity, encumbrance, price, or economy law.
- `docs/doctrine/native_design/d_series/source_packs/D19_cross_pack_integration_conflict_audit_and_conversion_readiness_capstone_pack/D19_capstone_doctrine_pack/D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md` for draft source-pack record-shape governance warnings and not-final-schema controls.

## 2. Owner layer

B03 belongs to Batch B operational doctrine. It routes object-use procedure between upstream B01/B02 procedure, the A-family doctrine layer, the C00 schema handoff control surface, future C01-C14 schema families, source-local donor object-system quarantine, and later object, inventory, economy, harm, actor, route, resource, world, canon, runtime, and training owners.

B03 may identify that a handoff is needed to a likely owner, but it must not perform that owner's work. When B03 cannot identify a valid owner or schema family, it must mark `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` instead of inventing Astra schema, mechanics, inventory state, runtime state, canon, or sourcebook equipment rules.

## 3. What B03 owns

B03 owns doctrine-level operational procedure for:
- object-use intake procedure after B02 action declaration;
- object-system construct classification for operational use;
- equipped, worn, carried, held, installed, quick-access, stored, bound, mounted, platform-held, and source-local holding checks;
- readiness/access/use-state triage;
- object function classification: weapon, armor/protection, tool/instrument, focus/channel, consumable, material/component, catalyst, implant/prosthetic, vehicle/platform, anchor/vessel, intelligent object, source-local object, mixed, or unknown;
- use-mode declaration: wield, wear, activate, consume, expend, install, channel through, repair with, modify with, throw, deploy, reload, charge, discharge, mount, unmount, store, retrieve, conceal, reveal, hand off, requisition, source-local use, or other;
- object access and compatibility checks;
- consumable/depletion/charge/ammunition/fuel/use-limit routing as owner handoff, not final math;
- object failure, breakage, depletion, overload, contamination, jam, misalignment, or rejection routing;
- possession/access/burden/custody/quick-access routing to inventory/economy/custody owners;
- object use to resolution-owner trigger routing when uncertainty/consequence requires resolution;
- object use to state-delta owner routing;
- B03-to-C00/C-family handoff references when object use produces conversion records;
- source-local donor equipment/object system quarantine and escalation rules;
- examples of good and bad B03 usage;
- minimum acceptance criteria for B03.

## 4. What B03 must not own

B03 must not define or promote:
- final object schema;
- C-family schema fields;
- C01-C14 schema contents;
- final weapon stats;
- final armor stats;
- final item stats;
- final damage dice;
- final attack math;
- final defense math;
- final armor class logic;
- final skill bonuses;
- final equipment bonus math;
- final item rarity/tier economy;
- final inventory capacity math;
- final weight/slot/encumbrance rules;
- final quick-access action economy;
- final ammunition/fuel/charge/reload math;
- final crafting, repair, salvage, upgrade, or modification procedure;
- final market price, treasure, reward, requisition, or economy law;
- final cyberware capacity, attunement, slot, hardpoint, or humanity-loss system;
- final vehicle/starship/mech/drone statblocks;
- final actor personhood for intelligent objects or body-integrated systems;
- final harm consequences from object use or object failure;
- runtime inventory state;
- runtime entity/component/event/state schemas;
- persistent campaign state;
- command lifecycle implementation;
- context packet compiler;
- hidden-information runtime state;
- live-play narration behavior;
- final canon promotion;
- accepted lexicon terms;
- sourcebook prose;
- donor equipment systems as Astra defaults.

## 5. Non-collapse rule

An object is not automatically ordinary equipment. Equipment is not automatically combat gear. A weapon is not automatically a damage formula. Armor/protection is not automatically armor class or fixed defense math. A tool is not automatically a skill bonus. A focus/channel is not automatically a spellcasting item. A consumable is not automatically a universal potion/scroll/battery rule.

B03 keeps these distinctions separate:
- possession, access, ownership, legal permission, readiness, function, use mode, burden, custody, and state are different questions;
- possessed does not mean accessible;
- accessible does not mean owned;
- owned does not mean legal to carry;
- quick access is not general capacity and does not decide final action timing;
- stored does not mean safe;
- containers do not erase burden unless an owner file or source-local rule supports it;
- object use may trigger resolution, cost, resource, harm, actor, world, economy, inventory, source-local, canon, runtime, or schema handoff, but B03 must not do the target owner's work.

B03 must not flatten objects into one universal item statblock, one combat-first equipment list, one donor slot system, one sourcebook gear catalog, one inventory backend, one item-rarity economy, or one final object schema.

## 6. Object-system construct and operational object-use definitions

An `object-system construct` is any doctrine-facing construct in which a physical, digital, spiritual, biological, technological, social, legal, metaphysical, platform, vehicle, container, implant, relic, material, or source-local object participates in play/conversion handling. An object-system construct may include an object, its function, its holder, its access state, its readiness state, its installation/mounting/binding context, its power or support interface, its ownership/custody posture, and any owner-file handoffs.

An `operational object-use` is a declared use of an object-system construct during a B01/B02 operational moment. It begins only after upstream Batch B context has identified an action, activity, transition, or checkpoint where object use matters. B03 then clarifies the object, function, holding/access state, readiness, compatibility, permission, use mode, and owner routing.

Doctrine vocabulary for object-use states includes:
- `object_use_declared`;
- `object_use_clarified`;
- `object_access_confirmed`;
- `object_access_blocked`;
- `object_ready`;
- `object_not_ready`;
- `object_equipped`;
- `object_worn`;
- `object_carried`;
- `object_stored`;
- `object_quick_access`;
- `object_bound_to_actor`;
- `object_installed`;
- `object_mounted`;
- `object_platform_held`;
- `object_source_local`;
- `object_use_resolution_triggered`;
- `object_use_owner_handoff_required`;
- `object_use_no_roll_required`;
- `object_use_no_delta_required`;
- `object_use_delta_routed`;
- `object_use_quarantined_gap`.

These terms are B03 doctrine vocabulary only. They are not accepted lexicon terms, runtime states, database enums, event log states, C-family fields, or player-facing rule terms.

## 7. Object-use intake procedure

B03 intake starts after B02 receives or clarifies an action declaration and the declaration names, implies, depends on, targets, consumes, modifies, repairs, deploys, stores, retrieves, transfers, or routes through an object-system construct.

Object-use intake sequence:
1. Confirm upstream B01/B02 context: scene/activity/encounter posture, declared actor, intent, method, target, scope, visible cost/risk posture, and any no-roll/roll-trigger posture already identified.
2. Identify the object reference if known; if missing, request clarification or mark `object_use_clarified` only after the relevant object/system is identifiable enough for routing.
3. Classify whether the construct is ordinary object, equipment, gear, asset, container, vehicle/platform, implant/prosthetic, anchor/vessel, intelligent object, source-local object, mixed construct, or unknown.
4. Identify holding/access state: equipped, worn, carried, held, installed, quick-access, stored, bound, mounted, platform-held, source-local holding, or unknown.
5. Identify function family and use mode without deriving final stats, bonuses, damage, armor, price, capacity, or crafting rules.
6. Check readiness, access, compatibility, and permission at the doctrine level.
7. Decide whether object use proceeds without roll, triggers resolution, requires cost/resource owner routing, requires state-delta owner routing, or must be quarantined/escalated.
8. Route every meaningful object use to at least one recognized owner, or explicitly produce `object_use_no_delta_required`, quarantine, escalation, `human_review`, `defer_until_schema_exists`, or a transition result.

B03 must not silently convert an equipment mention into attack math, armor class, item bonuses, inventory mutation, canon equipment, sourcebook prose, or runtime command lifecycle.

## 8. Holding, access, readiness, and custody triage

Holding triage asks where and how the object is held now for the purpose of this declared use. B03 recognizes equipped, worn, carried, held, installed, quick-access, stored, bound, mounted, platform-held, and source-local holding checks.

Doctrine-facing holding/access states include:
- `carried_on_person`;
- `equipped`;
- `worn`;
- `quick_access`;
- `packed`;
- `container_stored`;
- `vehicle_stored`;
- `platform_stored`;
- `facility_stored`;
- `hidden`;
- `faction_held`;
- `requisition_held`;
- `impounded`;
- `bound_to_actor`;
- `source_local_holding`;
- `unknown`.

Readiness triage asks whether the object can be used in the declared mode now. Doctrine-facing readiness statuses include `ready`, `not_ready`, `access_blocked`, `permission_blocked`, `compatibility_blocked`, `depleted`, `damaged`, `unstable`, `contaminated`, `overloaded`, `jammed`, `misaligned`, `source_local_only`, and `unknown`.

Custody triage asks who may hold, access, transfer, spend, reveal, conceal, sell, requisition, lawfully carry, or bear responsibility for the object. B03 routes custody, ownership, legal visibility, faction claim, impoundment, requisition, and burden questions to inventory/economy/custody/world-law owners rather than resolving final law or price.

## 9. Function-family classification

B03 classifies object function for operational routing only. Function families include:
- `weapon`: projects force, threatens, defends, channels technique, controls space, or enables a combat or harm-delivery action; not final weapon stats, final damage dice, final attack math, or critical rules.
- `armor_protection`: reduces, redirects, absorbs, deflects, filters, conceals from, or survives harm; not final armor stats, armor class logic, defense math, slot rules, or harm consequences.
- `tool_instrument`: enables, measures, repairs, crafts, treats, investigates, communicates, pilots, or manipulates a task; not final skill bonuses or final crafting/repair/salvage/upgrading procedure.
- `focus_channel`: directs, stabilizes, amplifies, stores, translates, routes, or accesses power, attention, technique, ritual, computation, signal, or metaphysical relation; not automatically a spellcasting item.
- `consumable`: is intended to be spent, eaten, drunk, injected, burned, discharged, broken, triggered, absorbed, installed, detonated, sacrificed, or otherwise depleted; not a universal potion/scroll/battery rule.
- `material_component`: is used to make, repair, empower, transform, trade, study, feed, anchor, or modify another construct; not final material pricing or crafting math.
- `catalyst`: enables, accelerates, stabilizes, alters, or risks transformation, crafting, ritual, advancement, route expression, power economy change, or actor evolution; routes to appropriate owners.
- `implant_prosthetic`: is installed into, integrated with, replacing, assisting, or modifying a body or actor substrate; not final cyberware capacity, attunement, humanity loss, actor personhood, or body-state math.
- `vehicle_platform`: carries, mounts, transports, houses, powers, shields, or supports actors/objects; not final vehicle/starship/mech/drone statblocks or hardpoint rules.
- `anchor_vessel`: holds, binds, stabilizes, stores, seals, houses, or routes a spirit, route, domain, power, memory, law, pattern, or other construct; not final actor/personhood or metaphysical schema.
- `intelligent_object`: may have agency, speech, desire, embedded intelligence, companion status, or actor-like behavior; B03 must route personhood and actor integration questions to owners.
- `source_local_object`: retains donor-specific object procedure under quarantine/source-local boundary until a valid owner formalizes or rejects it.
- `mixed` or `unknown`: used when multiple families apply or coverage is insufficient.

## 10. Use-mode declaration procedure

B03 records the use mode named or implied by the action declaration. Recognized use modes include `wield`, `wear`, `activate`, `consume`, `expend`, `install`, `channel_through`, `repair_with`, `modify_with`, `throw`, `deploy`, `reload`, `charge`, `discharge`, `mount`, `unmount`, `store`, `retrieve`, `conceal`, `reveal`, `hand_off`, `requisition`, `source_local_use`, and `other`.

Use-mode procedure:
1. Use the actor's declared intent and method from B02 as the controlling context.
2. Select the narrowest use mode that preserves the declared object function without inventing stats.
3. If multiple modes apply, mark mixed routing and identify the owner boundary for each mode.
4. If the mode changes action timing, cost, exposure, risk, access, custody, burden, or readiness, route that consequence to the appropriate owner instead of deciding final action economy.
5. If the mode depends on source-local donor procedure, mark `source_local_use` and apply quarantine/escalation rules.

## 11. Compatibility and permission checks

Compatibility checks ask whether the actor, object, target, environment, platform, power interface, route interface, body integration, mounting point, ammunition, fuel, charge, container, or source-local condition supports the declared use. Permission checks ask whether the actor is allowed to hold, access, carry, reveal, activate, requisition, install, bind, transfer, or use the object under custody, faction, legal, source-local, canon, or owner-file constraints.

B03 trigger families for compatibility and permission include:
- `object_access_needed`;
- `object_readiness_needed`;
- `object_compatibility_needed`;
- `object_permission_needed`;
- `object_actor_integration_relevant`;
- `object_power_interface_relevant`;
- `object_route_interface_relevant`;
- `object_custody_or_ownership_relevant`;
- `object_legal_visibility_relevant`;
- `source-local donor object system detected`;
- `runtime/canon/schema boundary risk`.

B03 may mark compatibility or permission as confirmed, blocked, unknown, or source-local only. It must not define final attunement slots, cyberware capacity, hardpoints, item slots, licensing law, legal categories, access-control backend state, or actor personhood.

## 12. Depletion, charge, ammunition, fuel, use-limit, and support-burden routing

B03 treats consumable/depletion/charge/ammunition/fuel/use-limit and support-burden pressure as owner handoff, not final math. Relevant trigger families include `object_use_limit_present`, `object_depletion_possible`, `object_charge_or_fuel_relevant`, `object_ammunition_or_reload_relevant`, `object_burden_relevant`, `object_power_interface_relevant`, and `object_route_interface_relevant`.

B03 may identify that an object use could spend, deplete, discharge, consume, reload, refuel, recharge, cool down, contaminate, exhaust, require maintenance, require crew/labor/support infrastructure, create trace, or impose support burden. B03 must route:
- power, charge, reservoir, recharge, overdraw, fuel-as-resource, and power economy behavior to resource/power owners;
- ammunition, reload, capacity, weapon-use limits, and mounted-interface questions to object/combat/platform owners;
- consumable depletion, dose, stability, contamination, and retained source-local effect to object/resource/harm/source-local owners;
- support burden, crew, labor, storage, transport, upkeep, and legal visibility to inventory/economy/world owners.

B03 must not define final ammunition/fuel/charge/reload math, final resource economy math, final item stats, final combat math, or final support-cost schedules.

## 13. Object condition, failure, breakage, overload, contamination, and loss routing

B03 recognizes object condition and failure as routing pressure. Relevant trigger families include `object_failure_possible`, `object_condition_relevant`, `object_depletion_possible`, `object_harm_consequence_possible`, `object_actor_integration_relevant`, `object_power_interface_relevant`, and `runtime/canon/schema boundary risk`.

Condition/failure states may include intact, worn, damaged, broken, unstable, contaminated, overloaded, depleted, jammed, misaligned, rejected, dormant, sealed, destroyed, lost, stolen, impounded, abandoned, source-local, or unknown. B03 may identify that the declared use risks breakage, depletion, overload, contamination, jam, misalignment, rejection, loss, or a harm consequence.

B03 must route:
- object-state damage, repair state, durability, installation, mounting, container state, and platform-held condition to object owners;
- harm, injury, backlash, corruption, rejection, overload harm, contamination harm, and terminal failure to harm/actor owners;
- repair, maintenance, calibration, crafting, salvage, upgrade, or modification procedure to method/project/crafting owners;
- loss, custody dispute, theft, confiscation, impoundment, or recovery to inventory/economy/world owners;
- source-local failure formats to source-local review.

B03 must not define final harm consequences from object use or object failure, final repair/salvage/upgrading procedure, final durability math, or final object failure tables.

## 14. Inventory, storage, quick-access, custody, and burden handoff rules

B03 adopts the doctrine-facing principles that possessed does not mean accessible, accessible does not mean owned, owned does not mean legal to carry, stored does not mean safe, quick access is not general capacity, and containers do not erase burden unless an owner file or source-local rule supports it.

Inventory/storage handoff rules:
1. If the question is whether the object is on the actor, equipped, worn, carried, held, packed, hidden, platform-held, stored in a vehicle/facility/container, bound to the actor, requisition-held, faction-held, or impounded, B03 routes to inventory/custody owners when procedure needs a durable answer.
2. If the question is whether quick access allows use now, B03 may mark `object_quick_access` or `object_access_blocked`, but it must not decide final quick-access action economy.
3. If the question is capacity, weight, slot, encumbrance, burden, cargo, crew support, storage capacity, container capacity, or transport support, B03 routes to inventory/economy/platform owners and must not define final inventory capacity math.
4. If the question is legal visibility, licensing, faction claim, contraband, requisition authority, payment, treasure, reward, resale, tax, confiscation, or economy law, B03 routes to world/economy/custody owners and must not define final market price, treasure, reward, requisition, or economy law.
5. If the question is source-local spatial storage, magic bag, pattern storage, post-scarcity storage, cyberdeck loadout, mecha bay, drone cap, or donor slot system, B03 marks source-local handling unless later owner support exists.

## 15. Object-use resolution trigger routing

A declared object use is not automatically a roll. B03 follows B02 no-roll and resolution-trigger procedure. B03 may mark `object_use_no_roll_required` when object use is feasible, accessible, ready, permissioned enough for the declared scope, consequence-free or owner-routable without uncertainty, and any meaningful delta is routed or explicitly not required.

B03 triggers resolution-owner routing when one or more trigger families are present:
- `object_access_needed`;
- `object_readiness_needed`;
- `object_compatibility_needed`;
- `object_permission_needed`;
- `object_use_limit_present`;
- `object_depletion_possible`;
- `object_charge_or_fuel_relevant`;
- `object_ammunition_or_reload_relevant`;
- `object_failure_possible`;
- `object_condition_relevant`;
- `object_burden_relevant`;
- `object_custody_or_ownership_relevant`;
- `object_legal_visibility_relevant`;
- `object_resolution_needed`;
- `object_harm_consequence_possible`;
- `object_actor_integration_relevant`;
- `object_power_interface_relevant`;
- `object_route_interface_relevant`;
- `C-family handoff needed`;
- `source-local donor object system detected`;
- `runtime/canon/schema boundary risk`.

When uncertainty/consequence requires resolution, B03 marks `object_use_resolution_triggered` or `object_use_owner_handoff_required` and routes to the resolution owner. B03 must not define final d20 math, exact Difficulty Numbers, attack math, defense math, armor math, damage dice, item bonus math, opposed-check math, or final outcome tables.

## 16. Object-use state-delta routing

Every meaningful object use must route at least one delta to a recognized owner or explicitly produce a no-delta/quarantine/escalation/transition result. B03 may identify that object use could change object state, resource/cost state, route/technique state, harm/failure state, actor integration, inventory/burden, custody/ownership, economy/requisition, world law/faction, canon/lexicon posture, source-local retained effect, runtime review posture, or schema review posture.

B03 state-delta routing outcomes include:
- `object_use_delta_routed` when at least one owner receives the relevant doctrine-facing delta;
- `object_use_no_delta_required` when object use is trivial, descriptive, already covered, or produces no meaningful later-play consequence;
- `transition_note` when the meaningful result is a B01 container transition or B02 action posture transition;
- `source_local_retained_effect` when donor object behavior remains bounded as source-local evidence;
- `quarantined_unresolved_delta` when the object use matters but no valid owner/schema exists;
- `owner_file_escalation` when a recognized owner must decide final treatment.

B03 does not implement a state delta validator, persistence model, event-sourced state model, runtime inventory state, or hidden-information runtime state.

## 17. Owner-file handoff rules

B03 routes object-use concerns as follows:
- resolution uncertainty, opposition, contested timing, defense/resistance, overreach, success-at-cost, and outcome interpretation to resolution owners;
- power economy, charge, reservoir, fuel-as-resource, recharge, overdraw, instability, and resource cost to resource/power owners;
- route technique, focus/channel use, signature object expressions, and power interface expression to route/technique owners;
- object identity, object state, function family, condition, mounting, installation, containers, material, platform object-state, and source-local object boundary to object owners;
- harm, injury, backlash, corruption, contamination consequences, rejection, overload consequences, and terminal failure to harm/actor owners;
- body integration, implants, prosthetics, bound objects, intelligent object personhood, symbiote/companion posture, and actor substrate questions to actor owners;
- inventory, storage, quick access, burden, custody, possession, ownership, transfer, requisition, and loss/recovery to inventory/economy/custody owners;
- law, faction permission, public visibility, contraband, sacred status, domain policy, market access, and social visibility to world/faction/economy owners;
- canon eligibility, accepted lexicon terms, canon equipment lists, and sourcebook promotion to canon/lexicon owners;
- runtime schemas, backend contracts, command lifecycle, event logs, context packets, hidden-information runtime state, and live-play validation to runtime owners;
- C-family conversion records to C00/C-family handoff governance;
- donor equipment systems and unsupported object formats to source-local review, quarantine, escalation, or `human_review`.

B03 may name the handoff reason; it must not do the target owner's final work.

## 18. Batch B to C00/C-family handoff rules

B03 may identify that object use produces conversion-record pressure for a future C-family schema, but Batch B procedure may identify that a C-family handoff is needed only through C00 governance. It must not invent C-family fields. It must not require, define, create, or promote C01-C14 schemas or C01-C14 schema contents.

The following standard lightweight doctrine-facing C00/C-family handoff block is not a runtime schema, not a backend event, not a database contract, not a command object, not a C-family record by itself, not final mechanics, not persistent campaign state, not canon, and not player-facing rule text:

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

The following B03-specific lightweight doctrine-facing block is an object-use routing note only:

```yaml
object_use_routing_note:
  object_use_state: object_use_declared | object_use_clarified | object_access_confirmed | object_access_blocked | object_ready | object_not_ready | object_equipped | object_worn | object_carried | object_stored | object_quick_access | object_bound_to_actor | object_installed | object_mounted | object_platform_held | object_source_local | object_use_resolution_triggered | object_use_owner_handoff_required | object_use_no_roll_required | object_use_no_delta_required | object_use_delta_routed | object_use_quarantined_gap
  actor_ref: string | null
  object_ref: string | null
  object_function_family: weapon | armor_protection | tool_instrument | focus_channel | consumable | material_component | catalyst | implant_prosthetic | vehicle_platform | anchor_vessel | intelligent_object | source_local_object | mixed | unknown
  use_mode: wield | wear | activate | consume | expend | install | channel_through | repair_with | modify_with | throw | deploy | reload | charge | discharge | mount | unmount | store | retrieve | conceal | reveal | hand_off | requisition | source_local_use | other
  holding_or_access_state: carried_on_person | equipped | worn | quick_access | packed | container_stored | vehicle_stored | platform_stored | facility_stored | hidden | faction_held | requisition_held | impounded | bound_to_actor | source_local_holding | unknown
  readiness_status: ready | not_ready | access_blocked | permission_blocked | compatibility_blocked | depleted | damaged | unstable | contaminated | overloaded | jammed | misaligned | source_local_only | unknown
  owner_handoff_required: boolean
  owner_handoff_reason:
    - object_state
    - resolution
    - resource_cost
    - route_technique
    - harm_failure
    - actor_integration
    - inventory_burden
    - custody_ownership
    - economy_requisition
    - world_law_faction
    - canon_lexicon
    - runtime_review
    - schema_review
    - source_local_review
    - human_review
  delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  note: string
```

`object_use_routing_note` is not a runtime schema, not a backend event, not a command object, not a C-family record, not an item statblock, not a sourcebook statblock, not final mechanics, not a database contract, not an event log, not a context packet format, not persistent campaign state, not canon, and not player-facing rule text.

## 19. Missing-schema fallback and quarantine/escalation

Missing schema coverage must produce `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` rather than improvised schema. B03 must not invent C-family fields, donor field names, donor record formats, object item schemas, inventory backend fields, runtime event shapes, or C01-C14 schema contents.

Fallback procedure:
1. Identify the object-use question and the blocked owner or missing schema boundary.
2. Preserve source evidence, construct references, outcome references, provenance references, source-local boundary if applicable, and rejected donor elements if applicable.
3. Mark `object_use_quarantined_gap`, `pending_schema`, `human_review`, `defer_until_schema_exists`, or owner-file escalation.
4. Do not normalize the object into an Astra statblock, equipment list, inventory row, command object, runtime event, or sourcebook rule.

Unclassifiable object-use records are quarantined or escalated, not normalized by invention.

## 20. Source-local donor equipment/object-system handling

Donor equipment systems are evidence only. Donor weapon damage dice, armor class rules, item rarity, attunement slots, item slots, cyberware capacity, humanity loss, starship statblocks, mech hardpoints, drone caps, crafting DCs, treasure tables, and requisition ratings are donor evidence only.

Source-local donor equipment/object-system handling rules:
1. Detect donor equipment/object-system format, including donor weapon damage dice, armor class, defense math, item rarity, attunement, slots, cyberware capacity, humanity loss, hardpoints, vehicle/starship/mech/drone statblocks, crafting DCs, treasure tables, requisition ratings, universal potion/scroll/battery formats, or donor inventory capacity rules.
2. Mark `source-local donor object system detected`, `object_source_local`, or `object_use_quarantined_gap` when Astra owners have not accepted the procedure.
3. Retain donor behavior only as source-local evidence or source-local retained effect when conversion/play handling requires preserving source truth.
4. Route conflicts to source-local review, schema review, canon review, runtime review, or `human_review`.
5. Do not import donor item/equipment/object systems as Astra defaults through B03.

Repeated donor pressure does not promote donor equipment/object-system formats to Astra law.

## 21. Runtime boundary

B03 rejects runtime state/event/command lifecycle ownership. It does not define runtime inventory state, runtime entity/component/event/state schemas, runtime state/schema/event/command lifecycle ownership, event-sourced state model, state delta validator, command lifecycle implementation, context packet compiler, backend validation, database contracts, event logs, hidden-information runtime state, persistent campaign state, runtime item records, runtime inventory backend, runtime access-control state, or runtime object-use commands.

Live-play behavior must not consume B03 procedure as runtime authority without later runtime validation. B03 examples and routing notes are doctrine-facing only.

## 22. Canon boundary

B03 does not promote final canon, final canon equipment lists, accepted lexicon terms, setting gear catalogs, sourcebook statblocks, item names, rarity tiers, market availability, faction law, legal categories, or sourcebook prose. Canon eligibility may be routed through C00/C-family handoff or canon/lexicon owners, but B03 does not decide canon acceptance.

B03 records or examples are doctrine-facing only and are not canon entries, sourcebook statblocks, sourcebook prose, accepted lexicon terms, backend contracts, or player-facing rule text.

## 23. Live-play/training boundary

B03 does not define live-play narration behavior, live-play GM adapter behavior, player-facing rules, GM scripts, hidden-information runtime behavior, training examples as authority, or sourcebook prose. Training or evaluation examples may cite B03 as doctrine-facing procedure, but they must not treat B03 routing notes as runtime commands, player options, final mechanics, canon equipment entries, or backend events.

## 24. Examples of good and bad B03 usage

Good B03 usage:
- A character declares through B02, "I fire the scavenged rail pistol." B03 classifies the object as `weapon`, use mode `wield`/`discharge`, checks whether it is carried, quick-access, loaded/charged, permissioned, and ready, then routes uncertainty to resolution owner, ammunition/charge to resource/object owners, and any object-state delta to the object owner without inventing damage dice.
- A character tries to use a shielded cloak to survive corrosive rain. B03 classifies `armor_protection`, checks worn/readiness/contamination risk, routes harm consequences to harm owners and object degradation to object owners, and does not create armor class logic.
- A party retrieves a sealed relic from a vehicle locker. B03 marks stored/platform-held access, routes retrieval delay and custody to inventory/custody owners, marks source-local boundary if the relic uses donor attunement, and avoids inventing attunement slots.
- A converter sees a donor cyberarm with humanity-loss rules. B03 classifies implant/prosthetic plus actor integration, quarantines donor humanity loss as source-local evidence, routes body integration/personhood to actor owners, and routes schema pressure through C00 as `pending_schema` if needed.
- A focus crystal is used to channel a route technique. B03 classifies focus/channel, checks compatibility and readiness, routes power cost to resource owners and technique expression to route owners, and does not treat the crystal as an automatic spellcasting item.

Bad B03 usage:
- Assigning a sword `1d8 damage` because the donor weapon table says so.
- Converting armor/protection into a fixed armor class or final defense formula.
- Giving a tool a flat skill bonus without routing competence/method to the proper owner.
- Treating quick access as final action timing or general inventory capacity.
- Treating possession as ownership, legal permission, readiness, or immediate access.
- Importing donor item rarity, treasure tables, attunement slots, cyberware capacity, humanity loss, starship hardpoints, drone caps, crafting DCs, or requisition ratings as Astra defaults.
- Writing a runtime inventory event, command lifecycle artifact, C-family field list, or sourcebook equipment statblock inside B03.
- Promoting B04-B11 or C01-C14 by implication because an object-use example needs a future owner.

## 25. Minimum tests or assertions

A minimum B03 verification pass asserts that:
- B03 exists at `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md`.
- Required B03 sections are present.
- B03 declares ownership and non-ownership.
- B03 references B01 and B02 as upstream Batch B context.
- B03 includes C00 handoff language and `batch_b_to_c_handoff`.
- B03 includes `object_use_routing_note` and marks it as doctrine-facing only.
- B03 includes object-system construct/object-use definitions.
- B03 includes holding, access, readiness, custody, function-family, and use-mode procedure.
- B03 rejects final object schema, final item stats, final weapon/armor/damage/defense math, final inventory capacity math, final price/economy law, final crafting/repair/salvage/upgrading procedure, and runtime inventory state.
- B03 rejects runtime state/event/command lifecycle ownership.
- B03 rejects C-family field invention and C01-C14 schema-content ownership.
- B03 rejects donor equipment/object-system formats as Astra defaults.
- B03 includes object-use resolution trigger routing and object-use state-delta routing.
- B03 includes burden/custody/quick-access/storage principles.
- B03 includes source-local donor equipment handling, quarantine, escalation, `human_review`, and `defer_until_schema_exists`.
- B03 references D00/D02/D03/D09/D17/D19 only as draft source-pack/reference material, not final current doctrine authority.
- B03 does not require, define, create, or promote B04-B11.
- B03 does not require, define, create, or promote C01-C14.
- No registry status is promoted to current.

## 26. Acceptance criteria

B03 is acceptable when it:
1. defines object-use intake after B02 without rewriting B01 or B02;
2. classifies object-system constructs, holding/access/readiness/custody, function family, and use mode for operational routing;
3. routes access, compatibility, permission, depletion, charge, ammunition, fuel, condition, failure, burden, custody, quick-access, storage, resolution, and state-delta pressure to recognized owners;
4. includes C00/C-family handoff language and the required doctrine-facing blocks without inventing C-family fields;
5. quarantines missing-schema and source-local donor object systems instead of normalizing them;
6. blocks final object schema, item stats, weapon/armor/damage/defense math, inventory capacity math, economy law, crafting/repair/salvage/upgrading procedure, runtime inventory state, runtime event/command schemas, canon promotion, accepted lexicon terms, and sourcebook prose;
7. treats D00/D02/D03/D09/D17/D19 only as draft source-pack/reference material, not final current doctrine authority;
8. does not require, define, create, or promote B04-B11;
9. does not require, define, create, or promote C01-C14;
10. supports durable tests without asserting future B04-B11 or C01-C14 files must be absent.

## 27. Follow-up handoff to B04

B03's follow-up handoff to B04 is limited to noting that later Batch B procedure may address its own separate operational domain. B03 does not require, define, create, or promote B04-B11. If a B03 object-use question appears to need a later Batch B file, B03 must route to owner-file escalation, `pending_schema`, quarantine, `human_review`, or `defer_until_schema_exists` rather than drafting or assuming B04-B11 content.

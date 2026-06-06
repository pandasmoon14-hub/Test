# RT-010 Inventory / Item / Vehicle / Persistent Asset Owner Scaffold

Date prepared: 2026-06-05
Status: owner scaffold only
Tracking ID: REMEDIATION-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SCAFFOLD-001
Remediation track: RT-010-inventory-item-vehicle-assets
Owner: Astra Doctrine Council / future inventory, item, gear, vehicle, platform, and persistent asset boundary owner

## 1. Purpose and scope

This file creates the documentation/control owner scaffold for RT-010, the inventory, item, gear, vehicle, platform, and persistent asset state track identified by `REMEDIATION-PRIORITY-LEDGER-001`. It exists to name the future owner boundary that must separate base item/gear/vehicle records from runtime instances, custody state, slot/loadout authority, charge/durability/cooldown tracking, cargo/crew/capacity state, movement/damage/repair authority, effect validation, and narration projection.

This scaffold is planning/control only. It is owner scaffold only: no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no inventory runtime, no item instance creation, no equipment effect resolution, no vehicle movement implementation, no cargo state implementation, no damage/repair implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

This scaffold does not implement remediation. It does not define final schemas, inventory runtime, item instance models, equipment effect resolution, slot/loadout mechanics, charge/durability/cooldown math, vehicle movement, cargo/crew/capacity state, damage/repair math, generators, validators, event models, persistence writers, context-packet compilers, live-play prompts, training behavior, donor-content audit results, or canon promotion.

## 2. Remediation ledger linkage

`docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` recommends PR-G as the inventory/item/vehicle persistent asset owner scaffold. The ledger states that RT-010 should be added after command, cost, provenance, and consequence scaffolds exist and that this work must not implement inventory, item effects, vehicle movement, cargo, or damage.

RT-010 is therefore a planning owner boundary only. It records that item/gear/vehicle records are not runtime inventory until backend-owned instance persistence, custody, effect validation, durability/charge/cooldown, cargo/crew/capacity, movement/damage/repair, provenance, and validation paths exist.

## 3. Dependency on existing and adjacent remediation tracks

RT-010 depends on `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` because item use, equipment activation, vehicle operation, custody transfer, cargo loading, and asset deployment require backend-owned command/event/state commitment rather than narration or model assertion.

RT-010 depends on `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` because item charges, fuel costs, repair costs, crafting costs, acquisition costs, durability loss, vehicle fuel consumption, cargo value, and consequence math are downstream of RT-002. RT-010 may route cost/resource/consequence candidates, but it cannot commit resource spend, penalty, loss, value flow, or consequence math.

RT-010 depends on `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md` because generated items, gear, and vehicles require RT-008 provenance/recurrence controls before persistence. Repeated narration, model memory, or item/vehicle usefulness is not durable generated content authority.

RT-010 depends on `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` because prose readiness is not executable validation and future inventory, item instance, equipment effect, vehicle state, custody, and persistence paths require validators and reviewer gates.

RT-010 must coordinate with `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md` where weapon damage, armor/protection effects, vehicle damage, hazard exposure, environmental damage to items/vehicles, and recovery matter. RT-010 must coordinate with `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_scaffold.md` where item-granted abilities, equipment effects, vehicle capabilities, and use-mode bindings matter. RT-010 must coordinate with `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md` where hidden item properties, concealed cargo, secret vehicle capabilities, and redacted inventory state matter. RT-010 must coordinate with `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_scaffold.md` where items, gear, or vehicles serve as rewards, clue objects, mission objectives, or scenario consequences. RT-010 must coordinate with `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md` where item/gear/vehicle generation depends on tables or oracles.

## 4. Audit-source linkage

This scaffold links to accepted audit sources without expanding, correcting, or implementing their findings:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, which establishes backend-first audit procedure, non-implementation boundaries, and LLM non-authority over backend truth.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, which records hazard/environment, hidden information, generated-content, and runtime ownership pressure.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`, which records B03 item/gear/equipment/asset use, C02 item/gear record, C08 vehicle/ship/platform record, and adjacent runtime seams.

## 5. Source pressure and actual-file posture

The future RT-010 owner must account for pressure from actual repo sources while preserving each source's current authority limits:

- B03: `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md` pressures item/gear/equipment/asset use, holding/access/readiness/custody triage, function-family classification, use-mode declaration, depletion/charge/ammunition/fuel routing, object condition/failure routing, and inventory/storage/quick-access/burden handoff while preserving B03's status as doctrine-facing operational procedure only.
- C02: `docs/doctrine/schema/C02_item_gear_record_schema.md` pressures item/gear conversion records, item classification, portability/scale, use-access, custody/burden references, capability references, installable/relic references, value/acquisition references, and crafting/salvage references while preserving C02's status as conversion-stage schema doctrine only.
- C03: `docs/doctrine/schema/C03_ability_power_technique_record_schema.md` pressures ability/power/technique records including item-granted effects, creature-granted capabilities, and active/passive effects that items, gear, relics, implants, and installable assets may carry or invoke, while preserving C03's status as conversion-stage schema doctrine only.
- C04: `docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md` pressures relic/implant/installable asset records, host-integration, module/socket/hardpoint references, and installation/removal routing while preserving C04's status as conversion-stage schema doctrine only.
- C08: `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md` pressures vehicle/ship/platform identity records, crew/control, cargo/storage, module/capability references, location/scenario references, and hazard references while preserving C08's status as conversion-stage schema doctrine only.
- C12: `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md` pressures crafting/salvage/recipe/repair/upgrade processes that create, modify, or consume items, gear, and vehicle components while preserving C12's status as conversion-stage schema doctrine only.
- SM00: `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` pressures schema/math/mechanics sequencing for item/gear/vehicle/asset-adjacent systems including durability math, charge/cooldown math, cargo capacity math, vehicle movement math, damage/repair math, and crafting/salvage math while preserving SM00's status as planning/readiness/scope file only.
- Roadmap: `docs/doctrine/astra_doctrine_roadmap_v0_1.md` supplies backend-first language, hidden-info language, and the backend-first model-interchangeability invariant: the LLM is an interchangeable narration/proposal adapter, not the inventory, item effect, vehicle state, custody, or asset authority.

## 6. Owner responsibilities

The future RT-010 owner is responsible for defining, in a later implementation-authorized PR, how base item/gear/vehicle records separate from runtime instances, how custody and ownership state routes to backend owners, how slot/loadout/equipment authority works, how charge/durability/cooldown/ammunition tracking routes to backend state, how cargo/crew/capacity state routes to backend owners, how vehicle movement/damage/repair authority works, how item-granted effects route to ability/combat owners, how hidden item/vehicle properties route through RT-005, how generated items/vehicles require RT-008 provenance, how item/vehicle table/oracle generation routes through RT-009, how cost/resource/consequence math routes through RT-002, and how validation gates route through RT-011.

The owner must preserve backend-first control: item narration, equipment descriptions, vehicle prose, inventory summaries, and model suggestions can be proposal material only until backend-owned instance persistence, custody, effect validation, durability/charge/cooldown, cargo/crew/capacity, movement/damage/repair, provenance, and validation paths accept them.

## 7. Must-not-own boundaries

RT-010 must not own final schemas, inventory runtime, item instance models, equipment effect resolution, slot/loadout mechanics, charge/durability/cooldown math, vehicle movement math, cargo/crew/capacity math, damage/repair math, generator behavior, validator behavior, event models, command IR, cost/resource math, combat/hazard damage, ability/effect binding, faction standing, RNG/table/oracle selection, mission/reward routing, persistence writers, replay verifiers, retrieval indexes, context-packet compilers, live-play prompts, training behavior, donor-content audit results, or canon promotion.

Item/gear/vehicle records are not persistent owned instances until backend-owned state, identity, custody, provenance, validation, and event paths exist. Asset use must remain downstream of RT-001 command lifecycle. Resource spend, loss, damage, repair, fuel, ammo, charge, durability, cost, reward, and consequence pressure remains downstream of RT-002 and RT-003 as applicable. Ability/effect-bearing assets must coordinate with RT-004 before mechanical effects can be resolved. Visible inventory/loadout/cargo/vehicle facts must route through RT-005 before narration. Generated assets require RT-008 provenance/recurrence controls before persistence. Random loot/table/oracle asset outputs require RT-009 authority before commitment.

## 8. Conceptual inventory/asset seams only

The following names are conceptual placeholders only: `item_instance_pending`, `equipment_slot_candidate`, `custody_state_pending`, `loadout_authority_required`, `charge_durability_tracking_pending`, `cooldown_state_pending`, `ammunition_tracking_pending`, `cargo_capacity_pending`, `crew_state_pending`, `vehicle_movement_pending`, `vehicle_damage_state_pending`, `repair_authority_pending`, `item_effect_validation_required`, `asset_provenance_required`, and `inventory_projection_pending`.

These planning placeholders are not final schemas, not inventory runtime, not item instance models, not equipment effect resolution, not slot/loadout mechanics, not charge/durability/cooldown math, not vehicle movement, not cargo/crew/capacity state, not damage/repair math, not generator, not validator, not event model, and not live-play authorization. They do not create item instances, equipment slots, custody records, vehicle state, cargo manifests, damage trackers, repair events, effect validators, runtime inventory, or backend persistence.

## 9. Required future outputs

Future RT-010 work, if separately authorized, must produce owner specifications for item instance persistence authority, equipment slot/loadout authority, custody and ownership state, charge/durability/cooldown/ammunition tracking, cargo/crew/capacity state, vehicle movement/damage/repair authority, item-granted effect routing to RT-003/RT-004, hidden property routing to RT-005, mission/reward/clue item routing to RT-006, generated content provenance routing to RT-008, table/oracle generation routing to RT-009, cost/resource/consequence routing to RT-002, validation gates through RT-011, and context-packet/narration projection rules.

## 10. Dependency relationships

- RT-001 controls command/event/state commitment for item use, equipment activation, vehicle operation, custody transfer, and asset deployment events.
- RT-002 controls cost, resource, fuel, charge, repair cost, acquisition cost, crafting cost, penalty, loss, value, and consequence math.
- RT-003 controls weapon damage, armor/protection effects, vehicle damage, hazard exposure, environmental damage to items/vehicles, and recovery.
- RT-004 controls item-granted abilities, equipment effects, vehicle capabilities, and use-mode bindings.
- RT-005 controls hidden item properties, concealed cargo, secret vehicle capabilities, redacted inventory state, and context-packet projection.
- RT-006 controls items/gear/vehicles as rewards, clue objects, mission objectives, or scenario consequences.
- RT-008 controls generated item/gear/vehicle provenance, recurrence, durable-record eligibility, and canon separation.
- RT-009 controls RNG/table/oracle invocation for item/gear/vehicle generation, loot tables, and random equipment.
- RT-011 controls validation/readiness gates and reviewer-approved movement from prose to executable controls.

## 11. LLM non-authority rules

The LLM must not:

- create durable item, gear, relic, implant, installable, vehicle, ship, platform, cargo, or asset records as backend truth;
- assign persistent item or vehicle IDs;
- change inventory, custody, ownership, equipment, loadout, cargo, crew, or storage state;
- spend charges, ammo, fuel, uses, durability, or cooldowns;
- apply item effects as mechanical truth;
- mutate vehicle/platform integrity, damage, movement, position, cargo, crew, or repair state;
- decide salvage, crafting, repair, requisition, price, value, reward, or loss outcomes;
- generate persistent assets without RT-008 provenance/recurrence controls;
- select random loot/table outputs without RT-009 backend RNG/table authority;
- bypass backend validation/reviewer approval;
- treat equipment narration as backend inventory or asset state.

The LLM may only draft proposals, summaries, or player-facing narration from backend-approved and context-approved inputs. It may not convert inventory narration, equipment descriptions, vehicle prose, cargo summaries, damage descriptions, or item suggestions into backend facts.

## 12. Context-packet and narration handoff expectations

Context packets must carry only backend-approved visible inventory state, authorized equipment/loadout posture, permitted custody information, approved cargo/capacity summaries, and context-approved item/vehicle status. Hidden item properties, concealed cargo, secret vehicle capabilities, and redacted inventory state must route through RT-005 before projection. Narration may describe only backend-approved inventory state and must not imply item instance creation, equipment effect resolution, custody transfer, cargo commitment, vehicle movement, damage/repair commitment, or canon promotion.

## 13. First-test expectations

Initial tests should verify file presence, `REMEDIATION-PRIORITY-LEDGER-001` linkage, RT-010 dependency references, audit-source references, B03/C02/C04/C08/C12/roadmap source-pressure references, backend-first language, hidden-info language, backend-first model-interchangeability invariant language, LLM non-authority guardrails, explicit non-implementation guardrails, registry tracking, and absence of implementation claims.

## 14. Explicit non-implementation statement

This RT-010 scaffold is not remediation implementation. It creates no inventory runtime, no item instance model, no equipment effect resolution, no slot/loadout mechanics, no charge/durability/cooldown math, no vehicle movement, no cargo/crew/capacity state, no damage/repair math, no generator, no validator, no event model, no command IR, no math implementation, no persistence writer, no retrieval index, no context-packet compiler, no live-play prompt, no training behavior, no donor-content audit, and no canon promotion.

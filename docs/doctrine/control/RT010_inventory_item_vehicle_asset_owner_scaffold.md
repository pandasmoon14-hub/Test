# RT-010 Inventory / Item / Vehicle / Persistent Asset Owner Scaffold

Date prepared: 2026-06-05
Status: owner scaffold only
Tracking ID: REMEDIATION-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SCAFFOLD-001
Remediation track: RT-010-inventory-item-vehicle-assets
Owner: Astra Doctrine Council / future inventory, item instance, gear, vehicle, platform, installable, custody, and persistent asset state owner

## 1. Purpose and scope

This file creates the documentation/control owner scaffold for RT-010, the inventory, item, gear, vehicle, platform, installable, and persistent asset state track identified by `REMEDIATION-PRIORITY-LEDGER-001`. It names the future owner boundary that must separate conversion-stage item/gear/vehicle records from backend-owned persistent instances, identity, custody, ownership, equipment, loadout, charges, durability, cooldowns, cargo, crew, vehicle integrity, movement state, repair/salvage candidates, provenance, validation, event commits, context-packet projection, and narration handoff.

This scaffold is planning/control only. It is owner scaffold only: no doctrine rewrite, no runtime implementation, no schema implementation, no command IR implementation, no math implementation, no validator implementation, no generator implementation, no inventory implementation, no item instance creation, no durable asset record creation, no item effect implementation, no vehicle/platform runtime implementation, no cargo or crew system implementation, no repair/salvage/crafting implementation, no ownership/custody mutation, no charge/ammo/fuel/durability/cooldown spend, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no canon promotion, no live-play/training authorization, and no donor-content audit.

This scaffold does not implement remediation. It does not define inventory runtime, item instances, item effects, vehicle runtime, cargo system, crew system, repair mechanics, installable schema, condition/damage model, command IR, persistence writers, retrieval indexes, context-packet compilers, live-play prompts, training behavior, donor-content audit results, or canon promotion.

## 2. Remediation ledger linkage

`docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md` recommends PR-G as the inventory/item/vehicle persistent asset owner scaffold. The ledger states that RT-010 should be added after command, cost, provenance, and consequence scaffolds exist and that this work must not implement inventory, item effects, vehicle movement, cargo, or damage.

RT-010 is therefore a planning owner boundary only. It records that item/gear/vehicle records are not persistent owned instances until backend-owned state, identity, custody, provenance, validation, and event paths exist.

## 3. Dependency on existing and adjacent remediation tracks

RT-010 depends on `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md` because asset use must remain downstream of RT-001 command lifecycle. An item use, equipment change, cargo transfer, vehicle operation, repair attempt, salvage attempt, requisition, or installable attachment cannot become state through narration alone.

RT-010 depends on `docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md` and `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md` because resource spend, loss, damage, repair, fuel, ammo, charge, durability, cost, reward, and consequence pressure remains downstream of RT-002 and RT-003 as applicable. RT-010 may name asset state seams, but it cannot choose formulas, damage outcomes, repair outcomes, values, losses, rewards, or consequence deltas.

RT-010 depends on `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_scaffold.md` because ability/effect-bearing assets must coordinate with RT-004 before mechanical effects can be resolved. A sword, relic, implant, module, vehicle system, installable, ammunition type, gear trait, or powered device is not mechanical truth until effect ownership, command binding, costs, cooldowns, prerequisites, and validation are defined elsewhere.

RT-010 depends on `docs/doctrine/control/RT005_context_packet_hidden_information_owner_scaffold.md` because visible inventory/loadout/cargo/vehicle facts must route through RT-005 before narration. Hidden cargo, concealed gear, unrevealed damage, unknown ownership, sealed compartments, tracking devices, stolen goods, or GM-only asset facts cannot be exposed or remembered by model memory.

RT-010 depends on `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md` because generated assets require RT-008 provenance/recurrence controls before persistence. Generated items, relics, vehicles, platforms, modules, cargo, and installables cannot recur as durable campaign truth unless provenance, source-local boundaries, validation, recurrence, IDs, and event paths are backend-owned.

RT-010 depends on `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_scaffold.md` because random loot/table/oracle asset outputs require RT-009 authority before commitment. The LLM may not select random loot, vehicle finds, salvage yields, cargo contents, or item-table outcomes by sampling or prose.

RT-010 depends on `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` because owner prose is not executable validation. Future inventory, instance, custody, equipment, cargo, vehicle, effect-binding, provenance, and event pathways require validators, reviewer gates, and tests before runtime readiness can be claimed.

## 4. Audit-source linkage

This scaffold links to accepted audit sources without expanding, correcting, or implementing their findings:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`, which establishes backend-first audit procedure, non-implementation boundaries, and LLM non-authority over backend truth.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`, which records ability/effect, hazard/consequence, schema, validation, and runtime ownership pressure relevant to assets.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`, which records B03 item/gear/equipment/asset use, C02 item/gear records, C08 vehicle/ship/platform records, generated-content, and adjacent runtime seams.

## 5. Source pressure and actual-file posture

The future RT-010 owner must account for pressure from actual repo sources while preserving each source's current authority limits:

- Requested B03 path note: `docs/doctrine/operations/batch_b/B03_item_gear_use_and_inventory_interaction_procedure.md` is absent in this repo. The nearest confirmed actual equivalent is `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md`; this scaffold cites that actual B03 only and does not rewrite it.
- C02: `docs/doctrine/schema/C02_item_gear_record_schema.md` owns conversion-stage item and gear record pressure, but C02 records are not persistent owned item instances, inventory runtime, item effects, custody state, charge tracking, durability tracking, equipment runtime, storage state, value economy, or live-play authority.
- C03: `docs/doctrine/schema/C03_ability_power_technique_record_schema.md` pressures ability/effect-bearing assets, cost/cooldown interaction, and mechanical capability routing, but RT-010 cannot resolve effects without RT-004.
- Requested C04 path note: `docs/doctrine/schema/C04_relic_implant_installable_asset_record_schema.md` is absent in this repo. The nearest confirmed actual equivalent is `docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md`; this scaffold cites that actual C04 only and does not rewrite it.
- C08: `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md` owns conversion-stage vehicle, ship, platform, station, mech, modular platform, and persistent equipment-platform record pressure, but C08 is not vehicle runtime, platform inventory state, cargo system, crew system, movement mechanics, damage mechanics, repair mechanics, or live-play authority.
- C12: `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md` exists and pressures crafting, salvage, repair, recipe, installation-process, modification-process, requisition-process, and value-flow evidence routing, but C12 is not repair/salvage/crafting implementation, item economy, runtime inventory state, or runtime project state.
- SM00: `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` pressures schema/math sequencing, readiness labels, backend-owned schema, validation, provenance, and event/state commit pathways; it does not make this scaffold executable.
- Roadmap backend-first language: `docs/doctrine/astra_doctrine_roadmap_v0_1.md` states future runtime must not let LLMs mutate state, roll dice, write files directly, or use model memory as authoritative persistence; RT-010 inherits that backend-first language for persistent asset state.
- Backend-first model-interchangeability invariant: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md` and the roadmap require backend ownership wherever persistent truth, rules, dice, validation, generated content, retrieval, memory, or consequences are required. RT-010 preserves the backend-first model-interchangeability invariant by treating the LLM as narration/proposal only, not asset-state authority.

## 6. Owner responsibilities

The future RT-010 owner is responsible for planning, not implementing, the boundaries for:

- separating base item/gear/relic/implant/installable/vehicle/platform records from persistent owned instances;
- defining what future owner must handle asset identity, custody, ownership, storage, equipment, loadout, cargo, crew, attachment, charge, ammo, fuel, use, durability, cooldown, integrity, movement, damage, repair, salvage, crafting, requisition, reward, value, provenance, validation, and event-path seams;
- coordinating item/equipment/vehicle use with RT-001 command lifecycle and event commitment;
- coordinating spend, damage, repair, fuel, ammo, charges, durability, losses, costs, rewards, and consequences with RT-002 and RT-003;
- coordinating ability/effect-bearing assets with RT-004 before mechanical effects can be resolved;
- coordinating visible, hidden, and redacted inventory/loadout/cargo/vehicle facts with RT-005 before narration;
- coordinating generated or recurring asset persistence with RT-008 provenance/recurrence controls;
- coordinating random loot, table, oracle, cargo, salvage, and asset outputs with RT-009 backend RNG/table/oracle authority;
- coordinating future validators and reviewer gates with RT-011.

## 7. Must-not-own boundaries

RT-010 owner scaffold must not own or imply ownership of final doctrine, inventory runtime, item instances, item effects, vehicle runtime, cargo system, crew system, repair mechanics, installable schema, condition/damage model, command IR, persistence writer, generator, validator, retrieval index, context-packet compiler, live-play prompt, training behavior, donor-content audit, or canon promotion.

It must not create item instance schemas, durable asset records, persistent item IDs, persistent vehicle IDs, custody mutation paths, equipment mutation paths, loadout mutation paths, cargo mutation paths, crew assignment systems, storage mutation paths, charge/ammo/fuel/durability/cooldown spend, item effect rules, vehicle movement rules, vehicle/platform integrity or damage rules, repair/salvage/crafting/requisition/value/reward/loss rules, validators, generators, persistence writers, retrieval indexes, or context-packet compilers.

## 8. Inventory/item/vehicle/asset seams as conceptual placeholders only

The following names are conceptual placeholders only for later owner decomposition:

```text
asset_record_reference
item_instance_pending
custody_state_pending
equipped_slot_pending
loadout_state_pending
charge_state_pending
durability_state_pending
cooldown_or_recharge_pending
cargo_manifest_pending
crew_assignment_pending
vehicle_integrity_pending
movement_state_pending
repair_or_salvage_candidate
installable_attachment_pending
asset_effect_binding_required
asset_generation_prohibited
```

These placeholders are not final schemas, not inventory runtime, not item instances, not item effects, not vehicle runtime, not cargo system, not crew system, not repair mechanics, not installable schema, not condition/damage model, not command IR, not persistence writer, not generator, not validator, and not live-play authorization.

## 9. LLM non-authority rules

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

Equipment narration is descriptive only. It may summarize backend-approved visible facts from a context packet, but it is not backend inventory state, not asset state, not custody truth, not ownership truth, not cargo truth, not crew truth, and not vehicle state.

## 10. Required future outputs

A later implementation-era owner may need to define future outputs such as schemas, math, command IR, runtime state, event models, validators, context packets, tests, persistence writers, retrieval indexes, or generators. This scaffold authorizes none of those outputs.

Before any future runtime claim, separate reviewed PRs must define at least:

- base-record to persistent-instance transition rules;
- backend-owned asset identity and provenance paths;
- custody, ownership, inventory, equipment, loadout, storage, cargo, and crew event paths;
- charge, ammo, fuel, use, durability, cooldown, integrity, damage, repair, salvage, crafting, requisition, value, reward, and loss dependency routing;
- effect-bearing asset coordination with RT-004;
- generated asset controls through RT-008;
- random loot/table/oracle controls through RT-009;
- visible/hidden/redacted inventory, loadout, cargo, and vehicle projection through RT-005;
- validator and reviewer-gate coverage through RT-011.

## 11. Dependency relationships

- Asset use is downstream of RT-001 command lifecycle.
- Resource spend, loss, damage, repair, fuel, ammo, charge, durability, cost, reward, and consequence pressure remains downstream of RT-002 and RT-003 as applicable.
- Ability/effect-bearing assets coordinate with RT-004 before mechanical effects can be resolved.
- Visible inventory/loadout/cargo/vehicle facts route through RT-005 before narration.
- Generated assets require RT-008 provenance/recurrence controls before persistence.
- Random loot/table/oracle asset outputs require RT-009 authority before commitment.
- Validation and readiness claims require RT-011 before any runtime, generator, schema, command IR, math, persistence, retrieval, context-packet, live-play, training, or canon claim.

## 12. Context-packet and narration handoff expectations

RT-010 expects future asset facts to enter narration only through backend-approved context packets. Narration may describe visible equipped items, visible carried gear, known cargo, known vehicle condition, or known installables only when RT-005 has projected those facts.

The narration handoff must preserve hidden-information boundaries. Hidden inventory, secret custody, concealed equipment, unknown cargo, undiscovered installables, unresolved damage, unrevealed charges, unconfirmed ownership, pending salvage, and GM-only asset facts remain outside the LLM's authority unless a backend-owned context packet exposes an approved projection.

## 13. First-test expectations

Initial tests for this scaffold should verify file presence, remediation ledger linkage, RT-010 linkage, dependencies on RT-001, RT-002, RT-003, RT-004, RT-005, RT-008, RT-009, and RT-011, audit-source linkage to AUDIT-001, AUDIT-WAVE1-001, and AUDIT-WAVE2-001, source-pressure linkage to B03, C02, C03, C04, C08, C12, SM00, backend-first language, model-interchangeability language, LLM non-authority rules, explicit non-implementation guardrails, registry tracking, and absence of implementation claims.

## 14. Explicit non-implementation statement

This RT-010 owner scaffold is planning/control only and does not implement remediation. It is not final doctrine, not an inventory runtime, not item instances, not item effects, not vehicle runtime, not cargo system, not crew system, not repair mechanics, not installable schema, not condition/damage model, not command IR, not a persistence writer, not a retrieval index, not a context-packet compiler, not a generator, not a validator, not live-play prompts, not training behavior, not canon promotion, and not a donor-content audit.

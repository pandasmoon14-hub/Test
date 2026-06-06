# RT010 inventory, item, vehicle, and asset owner specification

Tracking ID: REMEDIATION-STAGE2-RT010-INVENTORY-ITEM-VEHICLE-ASSET-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-H1
Parent Stage 2 PR ID: STAGE2-PR-H
Track: RT-010
Status: owner specification planning only; non-executable; non-implementation

## 1. Purpose and status

This document is STAGE2-PR-H1 owner-specification planning for RT-010 inventory/item/vehicle/asset ownership. It upgrades the RT-010 scaffold into owner-spec planning after the STAGE2-PR-H deferred convergence plan and the STAGE2-CLOSURE-REVIEW closure ledger identified that RT-010 still required a separate owner specification.

This file is non-executable planning only. It is not runtime code, not schema implementation, not command IR, not validator implementation, not generator implementation, not persistence, not a live-play prompt, not training data, not sourcebook inclusion authorization, not pilot conversion authorization, and not canon promotion.

### Explicit source linkage

Planning and audit sources used:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.
- REMEDIATION-STAGE2-RT010-RT012-DEFERRED-CONVERGENCE-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_stage2_rt010_rt012_deferred_convergence_plan.md`.
- REMEDIATION-STAGE2-COMPLETION-REVIEW-CLOSURE-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_stage2_completion_review_and_closure_ledger.md`.

Current RT owner files linked:

- RT010 owner scaffold: `docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_scaffold.md`.
- RT001 owner specification: `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`.
- RT002 owner specification: `docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md`.
- RT003 owner specification: `docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md`.
- RT004 owner specification: `docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md`.
- RT005 owner specification: `docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md`.
- RT006 owner specification: `docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md`.
- RT007 owner specification: `docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md`.
- RT008 owner specification: `docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md`.
- RT009 owner specification: `docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md`.
- RT011 owner specification: `docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md`.
- RT012 owner scaffold: `docs/doctrine/control/RT012_d_series_promotion_boundary_owner_scaffold.md`.

Asset, schema, operations, and readiness pressure sources confirmed present and used as pressure context only: `docs/doctrine/schema/C02_item_gear_record_schema.md`, `docs/doctrine/schema/C04_relic_implant_installable_asset_schema.md`, `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md`, `docs/doctrine/schema/C11_companion_summon_record_schema.md`, `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md`, `docs/doctrine/schema/C13_map_diagram_record_schema.md`, `docs/doctrine/schema/C10_table_oracle_record_schema.md`, `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`, `docs/doctrine/schema/C05_faction_institution_record_schema.md`, `docs/doctrine/schema/C01_creature_npc_record_schema.md`, `docs/doctrine/operations/batch_b/B05_acquisition_reward_requisition_and_value_flow_procedure.md`, `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md`, `docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md`, and `docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md`.

Referenced-but-absent optional files were confirmed absent and no substitute is asserted as equivalent: `docs/doctrine/schema/C04_relic_implant_installable_asset_record_schema.md`, `docs/doctrine/schema/C13_map_spatial_record_schema.md`, and `docs/doctrine/operations/batch_b/B06_crafting_repair_salvage_and_asset_change_procedure.md`.

Runtime/project authority sources used: `docs/doctrine/astra_doctrine_roadmap_v0_1.md`, `docs/doctrine/astra_doctrine_registry_v0_1.yaml`, `docs/decisions/current_decisions_log.md`, and `README.md` for backend-first/model-interchangeability posture.

## 2. Scope

RT-010 owns planning-level inventory/item/vehicle/asset ownership boundaries and the semantic handoff requirements needed before future backend systems may be separately authorized. RT-010 owns requirement boundaries for item, gear, relic, implant, installable, vehicle, ship, platform, companion, summon, cargo, map, route, requisition, custody, ownership, ammo, fuel, charge, durability, repair, salvage, crafting, loadout, storage, and transfer planning.

RT-010 owns asset state and asset-change handoff requirements; asset visibility and hidden-property handoff requirements; asset damage, degradation, repair, and recovery handoff requirements; asset cost, value, price, salvage, requisition, debt, upkeep, and reward handoff requirements; item/relic/implant/vehicle/platform/companion effect and capability handoff requirements; generated asset provenance and recurrence handoff requirements; random loot/salvage/requisition/cargo/table/oracle dependency handoff requirements; persistent asset state and event/persistence implication boundaries; and auditability requirements.

RT-010 routes command/event timing handoff through RT-001; resource/cost/value/reward/loss handoff through RT-002; damage/degradation/repair/recovery handoff through RT-003; effect/capability/prerequisite/charge/cooldown handoff through RT-004; hidden property, hidden cargo, custody secrecy, and narrator visibility handoff through RT-005; mission reward/loss/requisition/salvage/scenario asset handoff through RT-006; social/faction/custody/debt/bribe/blackmail/requisition handoff through RT-007; generated asset provenance handoff through RT-008; random loot/salvage/oracle handoff through RT-009; validation/readiness handoff through RT-011; and D-series/native-design promotion-boundary handoff through RT-012.

## 3. Must-not-own boundaries

RT-010 must not own or claim to complete final inventory system, final item system, final gear system, final relic/implant/installable system, final vehicle/ship/platform system, final companion/summon asset system, final cargo/custody system, final ownership system, final loadout/storage/transfer system, final ammo/fuel/charge system, final durability/degradation system, final repair/salvage system, final crafting/requisition system, final asset economy, final price/value/salvage/requisition tables, final persistent asset state, final persistent ID allocator, final asset event schema, final item schema, final vehicle schema, final cargo schema, final crafting schema, schema implementation, command IR implementation, runtime code, validator implementation, generator implementation, RNG/dice/table implementation, event ledger implementation, persistence writer implementation, retrieval index implementation, context-packet compiler implementation, live-play prompt implementation, training data, donor-content audits, sourcebook inclusion authorization, pilot conversion authorization, or canon promotion.

## 4. Authority model

- RT-001 owns command/action timing, legality, asset-affecting declarations, rejection/quarantine, resolution-trigger handoff, and event-commit boundaries.
- RT-002 owns costs, value pressure, repair cost, loss, degradation, salvage value, upkeep, debt, requisition pressure, reward/loss math, and economy pressure.
- RT-003 owns item/vehicle/platform damage, exposure, combat fallout, degradation as harm pressure, repair/recovery consequences, and hazard-driven asset changes.
- RT-004 owns item/relic/implant/vehicle/companion effects, prerequisites, charges, cooldowns, capabilities, hidden effects, and effect resolution handoffs.
- RT-005 owns hidden properties, hidden cargo, redacted asset state, visible inventory state, custody secrecy, player-known asset facts, and narrator projection.
- RT-006 owns mission rewards, penalties, requisitions, asset losses, salvage, item rewards, vehicle/platform rewards, and scenario asset consequences.
- RT-007 owns custody, bribes, blackmail material, debts, obligation-linked assets, faction property, patron assets, requisition, institutional response, and social ownership pressure.
- RT-008 owns generated items, generated vehicles, generated relics, generated assets, durable eligibility, recurrence, source-local status, and provenance.
- RT-009 owns loot tables, random item results, salvage tables, random cargo, random vehicle complications, and oracle dependencies.
- RT-011 owns validation/readiness requirements.
- RT-012 owns future promotion-boundary handling if D-series/native-design material proposes asset systems or asset records.
- Future backend runtime must own persistent asset state, state deltas, event commits, persistence, and migrations if separately authorized.
- The LLM may only describe backend-approved visible asset outcomes and may not create inventory state, assign custody, grant assets, spend charges, damage items, reveal hidden properties, decide prices, or commit asset changes.

## 5. Inventory/item/vehicle/asset state contract

The following conceptual asset-state placeholders are planning terms only:

- inventory_state_required
- item_asset_state_required
- gear_state_required
- relic_implant_installable_state_required
- vehicle_ship_platform_state_required
- companion_summon_asset_state_required
- cargo_state_required
- custody_state_pending
- ownership_state_pending
- loadout_state_pending
- storage_transfer_pending
- ammo_fuel_charge_dependency
- durability_degradation_dependency
- repair_salvage_dependency
- crafting_requisition_dependency
- asset_value_dependency
- asset_reward_loss_dependency
- hidden_asset_property_visibility_required
- hidden_cargo_visibility_required
- asset_effect_capability_dependency
- random_loot_salvage_dependency
- generated_asset_provenance_required
- persistent_asset_state_pending
- asset_event_commit_pending
- asset_resolution_quarantined

These terms are not final schemas, not database fields, not inventory rules, not item rules, not vehicle rules, not custody rules, not durability rules, not repair rules, not crafting rules, not economy values, not runtime state, not event records, not validators, and not live-play prompts.

## 6. Asset visibility, custody, and hidden-property contract

Visible inventory is not full backend inventory truth. Hidden properties and hidden cargo require RT-005 redaction/projection authority. Custody and ownership labels are not ownership mechanics. Dialogue or narration cannot transfer ownership or custody. Social/faction custody disputes route through RT-007. Mission/requisition custody routes through RT-006. Generated hidden properties require RT-008 provenance. Random hidden properties or loot dependencies require RT-009. Validation/readiness requires RT-011.

This owner specification does not define final hidden-property schemas, custody state machines, ownership rules, or inventory visibility fields.

## 7. Damage, repair, salvage, crafting, requisition, and value contract

Durability labels are not durability mechanics. Degradation labels are not damage formulas. Repair labels are not repair formulas. Salvage labels are not salvage economy. Crafting labels are not crafting rules. Requisition labels are not requisition mechanics. Price/value labels are not economy tables.

Item/vehicle/platform damage routes through RT-003. Repair/salvage/crafting/requisition costs and value pressure route through RT-002. Item/relic/implant/vehicle effects route through RT-004. Mission rewards, requisitions, salvage, and asset losses route through RT-006. Social/faction requisition, debt, custody, bribe, and blackmail route through RT-007. Random loot, salvage, crafting output, or cargo requires RT-009. Generated assets require RT-008 provenance. Persistent asset changes require future state/event/persistence ownership.

This owner specification does not define final durability formulas, repair formulas, salvage formulas, crafting recipes, requisition tables, price tables, economy values, or asset event schemas.

## 8. Asset commitment contract

Asset declaration is not asset state mutation. Inventory listing is not ownership truth unless backend-approved. Item proposal is not item creation. Generated asset proposal is not durable generated content. Reward proposal is not reward commitment. Custody proposal is not custody transfer. Repair/salvage/crafting/requisition proposal is not state mutation. Random loot/salvage dependency is not random outcome selection. Hidden asset property preparation is not player/model visibility. Narration is not event commitment. Rejected/quarantined asset actions must not mutate state. Event/state/persistence commitment requires future separately authorized backend systems.

This owner specification does not define final event schemas, runtime state machines, inventory state machines, vehicle state machines, ownership state machines, or executable asset procedures.

## 9. Future inventory/item/vehicle/asset artifact inventory

The following future artifact families are semantic requirements only, not implemented schemas, records, validators, services, formulas, generators, or runtime code. Every listed artifact has implementation status: future_required_not_implemented.

| Future artifact family | Purpose | Owner | LLM allowed interaction, if any | Downstream handoff | Implementation status |
| --- | --- | --- | --- | --- | --- |
| InventoryOwnershipRequirement | Define inventory and ownership requirement boundaries. | RT-010 | May describe backend-approved visible inventory summaries only. | RT-001, RT-005, RT-007, RT-011 | future_required_not_implemented |
| ItemAssetStateRequirement | Define item asset-state handoff requirements. | RT-010 | May mention backend-approved item facts only. | RT-001, RT-002, RT-003, RT-004, RT-011 | future_required_not_implemented |
| GearStateRequirement | Define gear-state and equipment handoff requirements. | RT-010 | May describe approved visible gear outcomes only. | RT-004, RT-005, RT-011 | future_required_not_implemented |
| RelicImplantInstallableRequirement | Define relic, implant, and installable asset boundaries. | RT-010 | May narrate approved visible effects without creating assets. | RT-004, RT-005, RT-008, RT-012 | future_required_not_implemented |
| VehiclePlatformStateRequirement | Define vehicle, ship, and platform state boundaries. | RT-010 | May describe approved visible vehicle/platform outcomes only. | RT-001, RT-003, RT-004, RT-006 | future_required_not_implemented |
| CompanionSummonAssetRequirement | Define companion/summon asset handoff boundaries. | RT-010 | May describe approved visible companion/summon facts only. | RT-004, RT-006, RT-007, RT-011 | future_required_not_implemented |
| CargoCustodyRequirement | Define cargo custody and custody-secrecy requirements. | RT-010 | May describe backend-approved visible cargo only. | RT-005, RT-006, RT-007, RT-009 | future_required_not_implemented |
| OwnershipTransferRequirement | Define transfer boundary requirements without mechanics. | RT-010 | No ownership or custody transfer authority. | RT-001, RT-007, future backend runtime | future_required_not_implemented |
| LoadoutStorageRequirement | Define loadout, storage, and transfer planning requirements. | RT-010 | May describe approved visible loadout/storage facts only. | RT-001, RT-004, RT-011 | future_required_not_implemented |
| ChargeFuelAmmoRequirement | Define ammo, fuel, charge, and spend dependency requirements. | RT-010 | No spend or replenishment authority. | RT-001, RT-002, RT-004 | future_required_not_implemented |
| DurabilityDegradationRequirement | Define durability/degradation handoff requirements. | RT-010 | No damage/degradation mutation authority. | RT-003, RT-002, future backend runtime | future_required_not_implemented |
| RepairSalvageRequirement | Define repair and salvage requirement boundaries. | RT-010 | No repair/salvage mutation authority. | RT-002, RT-003, RT-006, RT-009 | future_required_not_implemented |
| CraftingRequisitionRequirement | Define crafting and requisition requirement boundaries. | RT-010 | No crafting/requisition authority. | RT-002, RT-006, RT-007, RT-009 | future_required_not_implemented |
| AssetValueRequirement | Define asset cost/value/price pressure handoffs. | RT-010 | No price/value decision authority. | RT-002, RT-006, RT-007 | future_required_not_implemented |
| AssetRewardLossRequirement | Define asset reward/loss handoff boundaries. | RT-010 | No reward/loss commitment authority. | RT-001, RT-002, RT-006 | future_required_not_implemented |
| AssetVisibilityRequirement | Define visible/redacted asset projection requirements. | RT-010 | May narrate only RT-005-approved visible facts. | RT-005, RT-011 | future_required_not_implemented |
| HiddenAssetPropertyRequirement | Define hidden item/cargo/property visibility handoffs. | RT-010 | No hidden-property reveal authority. | RT-005, RT-008, RT-009 | future_required_not_implemented |
| AssetEffectCapabilityRequirement | Define item/relic/implant/vehicle capability handoffs. | RT-010 | May describe approved resolved effects only. | RT-004, RT-001, RT-011 | future_required_not_implemented |
| RandomLootSalvageRequirement | Define random loot/salvage/cargo dependency handoffs. | RT-010 | No random outcome selection authority. | RT-009, RT-006, RT-011 | future_required_not_implemented |
| GeneratedAssetProvenanceRequirement | Define generated asset provenance requirements. | RT-010 | No durable generated asset creation authority. | RT-008, RT-012, RT-011 | future_required_not_implemented |
| PersistentAssetStateRequirement | Define persistent asset state handoff requirements. | Future backend runtime, with RT-010 planning input | No mutation authority. | RT-001, RT-011, future persistence owner | future_required_not_implemented |
| AssetEventCommitRequirement | Define asset event/state commitment handoff requirements. | Future backend runtime, with RT-010 planning input | No event commitment authority. | RT-001, future event/persistence owner | future_required_not_implemented |
| InventoryAssetValidationRequirement | Define readiness requirements for inventory/asset boundaries. | RT-011 with RT-010 input | No validation execution authority. | RT-011 | future_required_not_implemented |

This section does not define final fields, formulas, JSON schema, database schema, Pydantic models, validator code, RNG code, inventory code, item code, vehicle code, ownership code, crafting code, event code, persistence code, retrieval code, context-packet compiler code, or runtime code.

## 10. Validation and readiness requirements

Validation requirements are future requirements only and coordinate with RT-011 without implementing validators:

- source linkage validation;
- RT-010 owner-boundary validation;
- inventory/item/vehicle/asset coverage validation;
- visible/hidden asset-state routing validation;
- custody/ownership transfer boundary validation;
- asset cost/value/reward/loss handoff validation;
- durability/degradation/repair/salvage/crafting/requisition handoff validation;
- item/relic/implant/vehicle effect handoff validation;
- mission/reward/requisition handoff validation;
- social/faction/custody/debt/bribe handoff validation;
- generated asset provenance validation;
- random loot/salvage/cargo dependency validation;
- persistent asset state handoff validation;
- command/event boundary validation;
- LLM non-authority validation;
- non-implementation guardrail validation.

## 11. Downstream handoffs

- RT-001 for command lifecycle, action legality, asset-affecting action declarations, rejection/quarantine, and event/state commitment boundaries.
- RT-002 for costs, prices, values, repair costs, salvage values, crafting costs, requisition pressure, debt, obligations, reward/loss math, economy pressure, upkeep, and consequence math.
- RT-003 for item damage, vehicle/platform damage, degradation, exposure, combat fallout, hazard effects, repair/recovery consequences, and asset harm pressure.
- RT-004 for item/relic/implant/vehicle/platform/companion effects, charges, cooldowns, prerequisites, hidden capabilities, asset-based abilities, and effect resolution.
- RT-005 for hidden properties, hidden cargo, visible inventory state, redacted asset state, player-known asset facts, narrator fact-set limits, and context-packet projection.
- RT-006 for mission rewards, mission penalties, requisitions, salvage, asset losses, item rewards, vehicle/platform rewards, cargo objectives, and scenario asset consequences.
- RT-007 for custody, bribes, blackmail material, faction property, patron property, institutional response, debts, obligation-linked assets, requisition authority, and social ownership disputes.
- RT-008 for generated items, generated gear, generated relics, generated implants, generated vehicles, generated cargo, generated assets, durable eligibility, recurrence eligibility, source-local status, and provenance.
- RT-009 for loot tables, random items, random cargo, random salvage, random requisitions, random vehicle complications, crafting-output tables, and oracle-derived asset pressure.
- RT-010 retains the inventory/item/vehicle/asset semantic requirement boundary and does not claim implementation authority.
- RT-011 for validation/readiness governance.
- RT-012 for D-series/native-design item, vehicle, asset, equipment, relic, crafting, salvage, requisition, or ownership patterns that cannot become runtime/canon/sourcebook authority without promotion.

## 12. LLM non-authority rules

The LLM is explicitly prohibited from:

- creating inventory state as backend truth;
- creating item, gear, relic, implant, vehicle, companion, cargo, or asset state as backend truth;
- assigning ownership;
- assigning custody;
- transferring ownership;
- transferring custody;
- assigning ammo, fuel, charges, durability, degradation, repair, salvage, loadout, storage, cargo, or route state;
- deciding item prices, salvage values, requisition values, crafting outputs, reward values, or asset values;
- applying item damage;
- applying vehicle/platform damage;
- repairing assets;
- salvaging assets;
- crafting assets;
- requisitioning assets;
- granting relics, implants, vehicles, companions, summons, cargo, or assets as backend truth;
- revealing hidden item properties;
- revealing hidden cargo;
- selecting random loot, salvage, requisition, cargo, or vehicle complication outcomes;
- creating generated assets as durable backend truth;
- mutating persistent asset state;
- committing asset events;
- treating inventory narration as state;
- treating dialogue as ownership/custody transfer;
- treating summaries as asset memory authority;
- inventing schemas, fields, state machines, tables, prices, values, formulas, or event records;
- bypassing RT-001, RT-002, RT-003, RT-004, RT-005, RT-008, RT-009, or RT-011;
- authorizing canon/sourcebook/training/live-play use.

## 13. Non-implementation reaffirmation

This PR adds no runtime implementation; no runtime code; no schema implementation; no command IR implementation; no validator implementation; no generator implementation; no inventory system; no item system; no gear system; no relic/implant/installable system; no vehicle/ship/platform system; no companion/summon asset system; no cargo/custody system; no ownership system; no loadout/storage/transfer system; no ammo/fuel/charge system; no durability/degradation system; no repair/salvage system; no crafting/requisition system; no asset economy; no price/value/salvage/requisition tables; no persistent asset state; no persistent ID allocator; no asset event schema; no item schema; no vehicle schema; no cargo schema; no crafting schema; no RNG/dice/table implementation; no event ledger implementation; no database schema; no persistence writer; no retrieval index; no context-packet compiler; no live-play prompt; no training data; no donor-content audit; no sourcebook inclusion authorization; no pilot conversion authorization; and no canon promotion.

## 14. Stage 2 output classification

```yaml
stage2_output:
  stage2_pr_id: STAGE2-PR-H1
  parent_stage2_pr_id: STAGE2-PR-H
  track: RT-010
  artifact_type: owner_specification
  implementation_status: non_executable_planning
  resolves_deferred_owner_spec_gap: true
  creates_runtime_implementation: false
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_validator_implementation: false
  authorizes_generator_implementation: false
  authorizes_command_ir: false
  authorizes_inventory_system: false
  authorizes_item_system: false
  authorizes_vehicle_system: false
  authorizes_asset_system: false
  authorizes_persistent_asset_state: false
  authorizes_persistent_id_allocator: false
  authorizes_asset_economy: false
  authorizes_durability_system: false
  authorizes_repair_system: false
  authorizes_salvage_system: false
  authorizes_crafting_system: false
  authorizes_requisition_system: false
  authorizes_rng_implementation: false
  authorizes_event_ledger: false
  authorizes_persistence_writer: false
  authorizes_context_packet_compiler: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  authorizes_pilot_conversion: false
  next_allowed_step: RT-012 owner specification sequencing decision, pending review
```

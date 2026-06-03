# D17 README Manifest — Economy, Acquisition, Inventory, Reward, and Requisition

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D17 is Astra Ascension's value-flow control layer. It governs how value is acquired, exchanged, rewarded, looted, salvaged, requisitioned, stored, burdened, transferred, restricted, consumed, taxed, maintained, lost, or made inaccessible.

D17 treats value as broader than money: currency, barter goods, materials, components, services, labor, favors, debt, licenses, permits, reputation access, faction credit, contribution points, salvage rights, reward claims, storage access, transport access, market access, requisition authority, cultivation resources, post-scarcity access, and source-local value are all possible value forms.

## Architecture
D17 uses the **Value–Access–Burden Architecture**.

```text
value question arises
  -> identify value form
  -> identify access channel
  -> identify ownership / custody / legality
  -> identify scarcity and availability
  -> identify inventory / storage / carrying burden
  -> identify requisition, upkeep, consumption, tax, or sink pressure
  -> route object, world, faction, project, opposition, or campaign effects to owner files
  -> record lawful outcome, source-local boundary, quarantine, or escalation
```

## Pack files
```text
D17-README_manifest.md
D17-00_economy_acquisition_inventory_reward_and_requisition_owner_boundaries.md
D17-01_value_forms_access_channels_scarcity_ownership_custody_and_burden_states.md
D17-02_acquisition_exchange_market_access_availability_and_value_conversion.md
D17-03_reward_loot_salvage_claim_and_value_entry_procedure.md
D17-04_inventory_storage_carrying_custody_quick_access_and_burden_procedure.md
D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md
D17-06_source_local_economy_donor_value_mapping_quarantine_and_escalation.md
D17-07_records_not_final_schema_and_conversion_handoff_shapes.md
D17-09_integration_checklists_ddr_register_and_acceptance_criteria.md
D17_pack_manifest.json
```

## Locked decisions
```text
Primary architecture: Value–Access–Burden Architecture.
Economy scope: value movement, not only money.
Acquisition/reward boundary: D17 owns value procedure; D13/D14/D16/D10 retain triggering and state ownership.
Inventory posture: burden/access/custody model, not default slot or weight law.
Requisition/sinks: first-class economy pressure.
Scarcity and legality: procedural states, not only price.
Donor economy systems: map, source-local retain, quarantine, or escalate; never adopted by label.
```

## Research-derived guardrails
```text
Value faucets require review against sinks, burden, access, and ownership.
Repeated acquisition without requisition review risks inflation and reward collapse.
Repeated requisition without recovery paths risks poverty traps.
Inventory expansion without burden review risks hoarding and market flooding.
Inventory restriction without usability review risks inventory paralysis.
Reward generosity without scarcity and sink review risks progression acceleration and devaluation.
Scarcity without alternate access risks grind walls.
Market access without legality and custody review risks shop-list drift.
Post-scarcity access without permission/infrastructure review erases meaningful acquisition.
Salvage without claim review creates uncontrolled wealth.
```

## Lawful donor outcomes
Every donor economy, inventory, reward, requisition, loot, salvage, market, price, currency, contribution, or supply system must receive one lawful outcome: direct Astra mapping, normalized Astra value mapping, source-local retained construct, quarantined construct pending later doctrine, or escalated doctrine problem.

# D17-04 — Inventory, Storage, Carrying, Custody, Quick Access, and Burden Procedure

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Core question
How does Astra handle possession, carrying, storage, containers, quick access, custody risk, legal visibility, transport burden, decay, maintenance, and loss without making weight, slots, encumbrance, spatial inventory, coin weight, magic bags, spatial rings, cargo capacity, or post-scarcity storage the universal default?

## Possession–Access–Burden Model
```text
value is obtained or claimed
  -> custody and ownership state are reviewed
  -> holding mode is declared
  -> burden type is identified
  -> access speed and access conditions are identified
  -> storage / transport / concealment / security pressures are identified
  -> decay, maintenance, spoilage, trace, or loss risk is identified
  -> owner-file handoffs are recorded
```

## Holding modes
```text
carried_on_person, equipped, worn, quick_access, packed, container_stored, vehicle_stored, platform_stored, facility_stored, banked, vaulted, cached, hidden, escrowed, faction_held, requisition_held, impounded, leased_storage, digital_or_pattern_stored, bound_to_actor, source_local_holding, unknown
```

## Burden types
```text
weight, bulk, volume, slot, quick_access_limit, container_capacity, transport_capacity, storage_capacity, security_burden, concealment_burden, legal_visibility, social_visibility, faction_trace, custody_risk, maintenance_burden, decay_or_spoilage, fuel_or_power_support, crew_or_labor_support, platform_cargo_burden, access_delay, retrieval_risk, source_local_burden
```
No burden type is default. Slots, weight, bulk, encumbrance, cargo, coin weight, spatial storage, and post-scarcity pattern storage are supported forms only when source-local, owner-file-supported, or later canonized.

## Access states
```text
immediate_access, quick_access, scene_access, interval_access, safe_location_access, facility_access, vehicle_or_platform_access, faction_permission_access, licensed_access, locked_access, hidden_cache_access, delayed_access, blocked_access, source_local_access, unknown_access
```
Possessed does not mean usable now. Quick access is not general capacity and does not decide D12 action timing.

## Storage and containers
Storage can provide capacity relief, security, preservation, legal custody, audit trail, concealment, organization, access control, transport preparation, or source-local protection. It can also create access delay, fees, taxes, confiscation risk, faction claim, storage dependency, theft risk, legal trace, custody dispute, maintenance burden, or source-local restriction.

Containers are D09 object-state entities. D17 owns value-access questions: what they hold, who owns contents, whether they conceal/preserve/secure/organize/transport, whether access is delayed, whether source-local storage law applies, and whether the container can be searched, stolen, damaged, impounded, locked, traced, or bonded.

## Stability states
```text
stable, fragile, perishable, decaying, spoiling, unstable, contaminated, degrading, maintenance_required, expired, source_local_decay
```
D17 identifies value-side decay/upkeep. D09 owns object degradation. D07 owns contamination or harm consequences. D18 owns long-horizon aging.

## Loss and recovery
Loss triggers include overburden, flight, defeat, confiscation, tax seizure, faction claim, legal inspection, theft, container damage, platform destruction, hazard exposure, decay, spoilage, abandonment, failed transport, or source-local trigger.

Loss outcomes include lost, damaged, impounded, stolen, abandoned, claimed_by_other, converted_to_unresolved_pressure, recoverable, recoverable_with_cost, recoverable_with_project, recoverable_with_operation, destroyed, quarantined, or source_local_result.

Inventory loss requires lawful trigger and owner-file support.

## Possession scope
```text
individual, party_shared, crew_shared, faction_shared, vehicle_or_platform, facility, domain, escrow, source_local_scope
```
Shared possession must state who can access, sell, spend, bear burden, receive trace, accept responsibility, abandon, transfer, or divide value.

## Principles
```text
Possessed does not mean accessible.
Accessible does not mean owned.
Owned does not mean legal to carry.
Stored does not mean safe.
Safe does not mean immediately available.
Quick access is not general capacity.
Containers do not erase burden unless an owner file or source-local rule supports it.
Post-scarcity storage is still permission, infrastructure, identity, energy, pattern, custody, or policy dependent.
Spatial storage is source-local unless canonized.
Inventory loss requires a lawful trigger and owner-file support.
```

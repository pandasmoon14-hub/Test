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


---

# D17-00 — Economy, Acquisition, Inventory, Reward, and Requisition Owner Boundaries

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Core question
How does Astra handle value, scarcity, acquisition, ownership, inventory, rewards, requisition, market access, loot, salvage rights, carrying/storage pressure, licenses, barter, currency, and resource availability across genres without importing donor coin economies, loot tables, shop lists, wealth-by-level math, requisition systems, cultivation-resource economies, post-scarcity assumptions, or inventory slot systems as universal Astra law?

## Why D17 is needed
D13 defines Projects, including crafting, salvage, repair, maintenance, and resource-gathering as interval procedures. D14 defines travel, exploration, discovery, route pressure, and site-entry pressure. D15 defines faction, institutional, legal, access, obligation, and claim procedure. D16 defines opposition, encounter, hazard, and reward/salvage pressure triggers. D17 defines what happens when those procedures create questions of value, access, ownership, scarcity, reward, inventory, burden, acquisition, or requisition.

Without D17, Astra risks importing: coins as universal value; wealth-by-level; shop lists as world truth; loot tables as reward doctrine; salvage as automatic free wealth; inventory slots or encumbrance as universal law; post-scarcity as no-scarcity; sect contribution as advancement law; cultivation resources as universal breakthrough currency; quest rewards as progression pacing law; black markets as guaranteed shops; and item rarity as objective value.

## D17 owns
```text
value-flow procedure
currency and currency-like construct handling
barter and direct exchange
purchase and sale procedure
market access and availability
scarcity states
wealth abstraction, when used
coin-count or unit-count handling, when source-local or canonized
licenses, permits, rationing, and restricted access as acquisition/economy procedure
requisition procedure
reward procedure
loot handling
salvage rights and claim handling
inventory burden procedure
carrying, storage, custody, and access burden
maintenance and upkeep as economy pressure
taxes, fees, tariffs, dues, tribute, tithes, and economic sinks
resource grades and material grades as acquisition/economy pressure
black market access procedure
ownership and possession state
trade legality
market disruption
supply and demand pressure as procedural state
source-local wealth, reward, requisition, and inventory systems
```

## D17 does not own
```text
D02 resolution math
D03 power resource pools, charges, overdraw, recharge, or resource economy
D04 advancement gates, breakthroughs, or progression proof
D05 method / skill taxonomy
D06 Technique, Principle, oath, domain, or power expression
D07 harm, corruption, injury, condition, exposure, or damage-family consequence
D08 actor personhood, body/form-state, companion identity, or substrate
D09 object, relic, tool, implant, platform, material, gear, or item-state mechanics
D10 world-state, public belief, rumors, hidden truth, law records, faction state, or market facts
D11 presentation and hidden-state narration
D12 cadence and action timing
D13 Project interval procedure
D14 exploration, discovery, travel, or site-entry procedure
D15 faction, institution, obligation, claim, standing, law-operation, or domain-control procedure
D16 opposition, hazard, encounter, or reward-trigger construction
D18 campaign arcs, seasons, long-horizon pacing, state aging, and campaign-scale economic evolution
final runtime implementation or final item/economy/inventory schema
```

## Donor-family pressures
D17 must survive coin-count fantasy, OSR treasure loops, narrative wealth tags, cyberpunk restricted gear, sci-fi post-scarcity, cultivation resources, crafting/salvage economies, vehicle fuel/maintenance, faction/domain taxation and requisition, horror scarcity, black markets, licenses, and reward tables.

## Anti-drift controls
```text
Do not treat money as default value.
Do not treat price as access.
Do not treat possession as ownership.
Do not treat rarity as final value.
Do not treat loot as lawful property by default.
Do not treat salvage as free wealth.
Do not treat reward as automatic power.
Do not treat requisition as free supply.
Do not treat post-scarcity as no-scarcity.
Do not treat inventory as default slots, weight, bulk, or encumbrance.
```


---

# D17-01 — Value Forms, Access Channels, Scarcity, Ownership, Custody, and Burden States

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Core question
How does Astra classify value before deciding whether it can be bought, sold, carried, claimed, requisitioned, rewarded, consumed, stored, restricted, or converted?

## Six core value-state objects
```text
1. Value Form
2. Access Channel
3. Scarcity State
4. Legality / Permission State
5. Ownership / Custody State
6. Burden State
```

## Value Form
Recommended value forms:
```text
currency, barter_good, material, component, crafted_good, consumable, fuel, ammunition, supply, relic_fragment, cultivation_resource, biological_sample, data_or_information_asset, service, labor, favor, debt, obligation_value, license, permit, reputation_access, faction_credit, contribution_point, reward_claim, salvage_right, ownership_claim, storage_access, transport_access, market_access, requisition_authority, source_local_currency, source_local_value
```
D17 does not treat all value as money. A license, favor, contribution point, salvage right, legal permission, information asset, storage right, or faction access may matter more than currency.

## Access Channel
Recommended access channels:
```text
purchase, sale, barter, trade, gift, reward, loot, salvage, resource_gathering, crafting_output, requisition, license_grant, faction_store, patron_grant, auction, black_market, market_board, institutional_access, domain_income, quest_payment, bounty, inheritance, loan, debt_settlement, theft, confiscation, tax_collection, tribute, ration_distribution, post_scarcity_access, source_local_channel
```
Access channel determines procedure and risk. Buying, requisitioning, looting, salvaging, stealing, gifting, receiving faction access, and using fabrication infrastructure are not the same procedure.

## Scarcity State
Recommended scarcity states:
```text
abundant, common, available, limited, scarce, rare, unique, restricted, illegal, rationed, monopolized, seasonal, unstable, contested, depleted, unknown, hidden, post_scarcity, source_local
```
Scarcity is not only price. It may create delay, license requirements, faction attention, travel requirements, research requirements, black-market risk, debt/favor requirements, requisition chains, salvage disputes, crafting dependencies, D13 Project requirements, D14 travel, or D15 access Operations.

## Legality / Permission State
Recommended legality / permission states:
```text
legal, licensed, permit_required, restricted, controlled, rationed, black_market_only, contraband, stolen, claimed_by_faction, claimed_by_law, claimed_by_domain_authority, salvage_disputed, use_allowed_sale_forbidden, possession_allowed_transport_forbidden, unknown, source_local
```
D17 owns acquisition/economy procedure. D10 owns law/world-state records. D15 owns institutional enforcement and claims. D11 owns presentation. Donor law codes do not become universal Astra law.

## Ownership / Custody State
Recommended ownership / custody states:
```text
owned, possessed, held_in_custody, borrowed, leased, licensed, loaned, rented, faction_held, escrowed, impounded, requisitioned, claimed, contested, stolen, salvage_pending, salvage_awarded, bound, soul_bound_source_local, lost, abandoned, unclaimed, unknown, source_local
```
Ownership and custody are separate. A character can possess an item without owning it, be licensed to use it without being allowed to sell it, or store value in a faction vault that preserves custody but limits access.

## Burden State
Recommended burden forms:
```text
weight_burden, bulk_burden, volume_burden, slot_burden, quick_access_burden, storage_burden, container_burden, transport_burden, security_burden, custody_risk, legal_visibility, social_visibility, faction_trace, maintenance_burden, decay_or_spoilage, fuel_or_power_burden, crew_or_labor_burden, platform_cargo_burden, concealment_burden, source_local_inventory_law
```
Burden is procedural pressure. It may trigger D03, D07, D09, D10, D13, D14, D15, D17, or D18 depending on context.

## Example
A monster core may be a cultivation_resource value form, acquired by salvage, rare and contested as scarcity, claimed_by_faction as permission state, possessed but not owned as custody state, and subject to decay_or_spoilage plus faction_trace burden. It cannot be handled by price alone.

## Embedded risk controls
D17 does not collapse economy into money; price does not equal access; possession does not equal ownership; scarcity is not only price; inventory is burden/access/custody/visibility/maintenance/decay/transport pressure; cultivation resources are value forms, not universal advancement currency.


---

# D17-02 — Acquisition, Exchange, Market Access, Availability, and Value Conversion

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Core question
How does Astra determine whether a character, faction, group, or platform can obtain, exchange, sell, trade, request, loot, salvage, requisition, borrow, or access value without turning shops, loot tables, coin prices, auction houses, black markets, faction stores, contribution systems, or post-scarcity access into universal Astra law?

## Eight-checkpoint acquisition and exchange procedure
```text
1. Value request checkpoint
2. Value-state classification checkpoint
3. Access channel checkpoint
4. Availability and scarcity checkpoint
5. Permission, legality, and custody checkpoint
6. Exchange / conversion checkpoint
7. Cost, burden, and sink checkpoint
8. Outcome and owner-file handoff checkpoint
```

## Value request checkpoint
A value question begins when someone tries to obtain, exchange, claim, store, access, move, sell, spend, requisition, or convert value: buying gear, selling salvage, requesting ammunition, bartering for fuel, looting opposition, opening market access, trading a favor for a license, auctioning a relic fragment, storing a dangerous object, converting contribution points into supplies, using post-scarcity fabrication access, or claiming wreck salvage.

## Access channel checkpoint
Access channel changes procedure and risk:
```text
purchase — requires market, seller, price, permission, availability
barter — requires acceptable exchange value and mutual recognition
trade — requires transfer rights and custody/ownership clarity
reward — requires lawful reward trigger and ownership handoff
loot — requires source, custody, legality, and D16/D17/D10/D15 review
salvage — requires salvage state, claim review, and D09/D15/D17 handoff
requisition — requires authority, eligibility, supply, and institutional approval
black_market — requires access, risk, legality pressure, and trace
auction — requires venue, time, competition, custody
faction_store — requires standing, access, contribution, permission, stock
post_scarcity_access — requires infrastructure, permission, identity, energy, pattern, license, or policy
source_local_channel — requires explicit boundary
```

## Availability and scarcity outcomes
```text
available_now
available_with_delay
available_with_requirement
available_at_cost
available_with_risk
available_only_through_project
available_only_through_faction
available_only_through_travel
available_only_through_black_market
available_only_through_source_local_procedure
unavailable
unknown
protected_hidden
quarantined
escalated
```
Scarcity may create price, but may also create time, route, faction, license, Project, black-market, or claim pressure.

## Permission, legality, and custody questions
```text
Who owns it?
Who possesses it?
Who claims it?
Who can legally transfer it?
Is use allowed but sale forbidden?
Is transport restricted?
Is it contraband, faction-controlled, licensed, bound, stolen, salvage_pending, unknown, or protected hidden?
```
D17 owns value/access procedure. D10 owns law/world-state. D15 owns enforcement, claims, and obligations. D11 owns presentation.

## Exchange and conversion
Conversions may include currency to item, item to currency, material to crafted output, salvage to component, favor to access, standing to license, contribution point to faction supply, debt to obligation, loot to sale value, reward claim to item/access, requisition authority to supply, service to payment, information to market advantage, post-scarcity pattern to fabricated object, or source-local currency to source-local benefit.

Conversion requires valid channel, permission, availability, and owner-file support. Friction may include transaction cost, tax, tariff, delay, spoilage, loss rate, exchange rate, standing requirement, broker requirement, black-market risk, requisition approval, material waste, custody dispute, or source-local rules.

## Cost, burden, and sink checkpoint
Before completion, identify what leaves, is reserved, is consumed, or becomes burden: currency payment, barter transfer, favor spent, debt incurred, standing risked, tax, tariff, fee, dues, bribe, storage cost, transport cost, license fee, maintenance, decay, spoilage, repair requirement, fuel, ammo, time, opportunity cost, legal trace, faction scrutiny, or source-local sink.

## Outcome states
```text
acquired, acquired_with_cost, acquired_with_burden, acquired_with_dispute, acquired_with_trace, access_granted, access_limited, access_denied, exchange_completed, exchange_partial, exchange_delayed, exchange_failed, custody_changed, ownership_changed, claim_created, claim_contested, requisition_approved, requisition_denied, reward_delivered, loot_pending_review, salvage_pending_claim, black_market_trace_created, unavailable, quarantined, escalated, source_local_result
```

## Principles
```text
Payment is not access.
Possession is not ownership.
Rarity is not price.
Market listing is not world truth.
Loot is not automatically lawful property.
Salvage is not automatically owned.
Requisition is not free supply.
Post-scarcity is not no-scarcity.
Faction access is not advancement permission.
Contribution points are not universal currency.
Black markets are not guaranteed shops.
```


---

# D17-03 — Reward, Loot, Salvage, Claim, and Value-Entry Procedure

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Core question
How does Astra decide what value enters play through rewards, loot, salvage, bounties, quest payments, encounter outcomes, project outputs, faction grants, discoveries, and source-local procedures without turning donor reward tables, treasure parcels, loot drops, monster parts, cultivation cores, or wealth-by-level assumptions into Astra law?

## Eight-checkpoint value-entry procedure
```text
1. Value-entry trigger checkpoint
2. Source and authority checkpoint
3. Reward / loot / salvage classification checkpoint
4. Eligibility and claim checkpoint
5. Custody and ownership checkpoint
6. Value-form and scarcity checkpoint
7. Burden, sink, and consequence checkpoint
8. Delivery, delay, quarantine, or escalation checkpoint
```

## Trigger sources
```text
D13 Project completion
D14 discovery
D15 institutional operation
D16 encounter or opposition outcome
quest or mission completion
bounty completion
loot from defeated opposition
salvage from site, vehicle, platform, object, battlefield, or creature
faction grant
patron payment
auction result
inheritance
domain income
resource gathering
crafting output
source-local reward procedure
D18 campaign milestone handoff
```
D17 does not assume every victory creates loot, every quest creates payment, or every salvageable object becomes party property.

## Source and authority
Authority may come from direct possession, contract, bounty issuer, quest giver, faction authority, law authority, domain authority, salvage law, market agreement, patron promise, source-local system, world-state discovery, encounter context, Project output, campaign milestone, or unknown authority.

## Value-entry categories
```text
reward_payment, reward_item, reward_access, reward_license, reward_claim, reward_favor, reward_information_asset, loot_currency, loot_item, loot_material, loot_component, loot_consumable, loot_relic_fragment, loot_source_local, salvage_component, salvage_material, salvage_data, salvage_platform_part, salvage_biological_sample, salvage_resource, bounty_payment, faction_grant, requisition_grant, domain_income, project_output, crafting_output, source_local_reward
```

## Eligibility and claims
Eligibility may depend on contract terms, quest participation, party agreement, faction standing, legal status, license, salvage rights, rank, contribution, proof of completion, custody, proximity, source-local rule, hidden ownership, D10 world-state, or D15 institutional claim.

Eligibility states: eligible, eligible_with_condition, shared_eligibility, contested_eligibility, ineligible, unknown, protected_hidden, source_local.

## Custody and ownership outcomes
```text
custody_granted
ownership_granted
custody_without_ownership
ownership_contested
salvage_pending_claim
held_in_escrow
faction_claim_attached
law_claim_attached
domain_claim_attached
stolen_property_flag
bound_to_actor
source_local_binding
unknown_claim_present
```
Loot creates custody first. Salvage is claim-bearing. Reward may be ownership, access, custody, license, favor, information, or source-local entitlement.

## Burden, sink, and consequence review
Before value-entry completes, D17 identifies transport burden, storage burden, legal visibility, faction trace, tax, tariff, salvage fee, broker/auction fee, claim dispute, decay/spoilage, maintenance, repair requirement, identification cost, attunement/source-local binding cost, license renewal, security burden, custody risk, party division conflict, requisition audit, or black-market laundering risk.

## Delivery outcomes
```text
delivered
delivered_with_burden
delivered_with_cost
delivered_with_trace
delivered_with_claim
delivered_as_custody_only
delivered_as_access_only
delivered_as_source_local
split_required
escrow_required
claim_review_required
salvage_pending
reward_delayed
reward_denied
reward_partially_delivered
reward_converted
reward_quarantined
escalated_owner_file_problem
```

## Reward principles
```text
Reward is value-entry, not automatic power.
Loot is custody first, not ownership by default.
Salvage is claim-bearing, not free wealth by default.
A bounty is contract value, not universal reward law.
A faction grant is access or support, not automatic item ownership.
A rare drop is evidence of value, not final Astra rarity doctrine.
A quest payment is source-local or scenario value unless canonized.
A cultivation resource is not universal advancement currency.
A reward can be delayed, escrowed, split, taxed, restricted, bound, contested, or converted.
```

## Reward division
D17 supports individual_delivery, shared_pool, claim_by_need, claim_by_contract, claim_by_contribution, auction_internal, faction_assignment, salvage_law_assignment, source_local_distribution, and contested_distribution without making any universal.


---

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


---

# D17-05 — Requisition, Upkeep, Consumption, Value Sinks, and Economic Pressure

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Core question
How does Astra remove, reserve, consume, degrade, tax, bind, requisition, maintain, or redirect value without turning upkeep, taxation, repairs, ammo, fuel, food, debt, contribution, durability, faction dues, lifestyle, military requisition, or cultivation consumption into universal Astra law?

## Sink–Obligation–Pressure Model
```text
value exists or enters play
  -> identify whether a sink, consumption, upkeep, requisition, tax, debt, decay, or obligation applies
  -> identify whether it is mandatory, optional, conditional, scheduled, event-driven, ambient, or source-local
  -> identify what value form is removed, reserved, transformed, degraded, or made inaccessible
  -> identify who or what receives, consumes, claims, destroys, stores, or audits the value
  -> identify owner-file handoffs
  -> record outcome, burden, pressure, or escalation
```

## Sink types
```text
consumption, upkeep, maintenance, repair_cost, fuel_use, ammo_use, component_use, license_fee, permit_renewal, tax, tariff, toll, dues, tribute, tithe, rent, storage_fee, broker_fee, auction_fee, transaction_fee, bribe, debt_payment, interest, faction_contribution, requisition_reservation, rationing, decay, spoilage, degradation, confiscation, seizure, sacrifice, cultivation_consumption, ritual_consumption, source_local_sink
```

## Sink timing
```text
immediate, on_acquisition, on_exchange, on_use, on_damage, on_repair, on_storage, on_transport, on_maintenance_interval, on_license_interval, on_project_interval, on_scene_transition, on_travel_interval, on_faction_operation, on_campaign_interval, on_failure, on_success, on_overuse, ambient, scheduled, source_local_timing
```
No universal upkeep cadence is created.

## Obligation levels
```text
mandatory, required_for_access, required_for_legality, required_for_safety, required_for_maintenance, required_for_quality, optional_upgrade, optional_convenience, avoidable_with_risk, deferable_with_consequence, waived_by_standing, waived_by_license, source_local_obligation
```
This prevents every sink from becoming punitive.

## Sink effects
```text
removed_from_circulation, consumed, reserved, locked, degraded, spoiled, transformed, converted_to_debt, converted_to_obligation, converted_to_trace, transferred_to_faction, transferred_to_law_authority, transferred_to_market_actor, sacrificed, destroyed, held_in_escrow, source_local_effect
```
Not every sink destroys value. Taxes transfer value. Debt converts cost to future obligation. Requisition reserves supply. Confiscation changes custody.

## Requisition procedure
A requisition is a request, authorization, reservation, assignment, or draw against institutional supply, authority, or stock. It may involve military supply, guild stock, sect treasury, corporate inventory, ship stores, crew supplies, domain stockpile, emergency rationing, faction equipment, licensed issue, patron support, or source-local requisition.

Requisition asks: who has authority, who approves, what stock is affected, whether assignment is temporary or permanent, whether return is required, whether audit applies, and whether debt, obligation, scrutiny, reduced standing, or institutional burden results. Requisition is not free supply.

## Upkeep and maintenance boundary
D17 owns value-side upkeep. D09 owns object/platform state. D13 owns maintenance Projects. D15 owns organizational/legal obligations. D18 owns long-horizon support burden and aging.

## Debt and obligation value
Debt may be currency_debt, favor_debt, resource_debt, service_debt, requisition_debt, salvage_debt, patron_debt, faction_debt, legal_debt, or source_local_debt. D17 owns value/payment side. D15 owns obligation, claim, enforcement, standing, and institutional pressure. D10 records world-state.

## Anti-poverty-trap guardrail
A requisition, upkeep, repair, tax, fee, or maintenance burden should not create unrecoverable resource collapse unless the campaign, source-local rule, or explicit high-risk state supports that consequence and owner files can route recovery, debt, loss, or alternative access.

Recovery paths may include defer_with_consequence, convert_to_debt, reduced_quality_access, temporary_license, salvage_alternative, faction_aid, D13 recovery/acquisition/repair Project, D15 negotiation or obligation Operation, D17 partial payment, D18 campaign-scale reset/support, or source-local recovery.

## Principles
```text
Every repeated value faucet needs sink review.
Requisition is not free supply.
Upkeep is not automatic punishment.
Debt is not only currency.
Taxation is not universal economy doctrine.
Repair cost is not D09 object-state by itself.
Fuel, ammo, food, and components are not universal tracking requirements.
Post-scarcity access still has infrastructure, permission, policy, identity, energy, or pattern constraints.
A sink may remove, reserve, transfer, transform, degrade, lock, consume, or make value inaccessible.
Sinks must not silently bypass owner files.
```


---

# D17-06 — Source-Local Economy Systems, Donor Value Mapping, Quarantine, and Escalation

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Core question
How does Astra convert donor wealth, acquisition, inventory, reward, requisition, loot, salvage, market, contribution, resource, supply, and economy systems without allowing donor value logic to become universal Astra law?

## Functional donor value mapping ladder
```text
1. Identify the donor value construct.
2. Identify the donor evidence type.
3. Identify the value form.
4. Identify the access channel.
5. Identify scarcity, legality, ownership, custody, and burden assumptions.
6. Identify value-entry, exchange, inventory, reward, requisition, or sink function.
7. Identify donor price, currency, wealth, slot, weight, reward, loot, contribution, or upkeep assumptions.
8. Identify owner files affected.
9. Decide lawful handling: direct Astra mapping, normalized Astra mapping, source-local retained construct, quarantine, escalation.
10. Record rejected donor assumptions.
```

## Normalized mapping examples
```text
A coin price list becomes market/access evidence, not universal Astra pricing.
A treasure parcel becomes reward value-entry evidence, not wealth-by-level doctrine.
A loot table becomes source-local or scenario value-entry evidence, not automatic reward law.
A cultivation core becomes a value form and possible advancement-adjacent resource, not universal breakthrough currency.
A sect contribution system becomes faction credit / standing / access / obligation / requisition pressure, not Astra advancement law.
A spatial ring becomes source-local storage or D09/D17 object-storage pressure, not universal inventory solution.
A post-scarcity fabricator becomes access-channel infrastructure with permission, identity, pattern, energy, policy, legality, and object-state handoffs, not “everything is free.”
A fuel rule becomes resource/sink pressure, not universal vehicle economy.
An abstract wealth rating becomes a source-local or normalized wealth-access construct, not universal wealth doctrine.
```

## Source-local retained constructs
Source-local retention is valid for useful but unsafe-to-generalize value systems: city price lists, donor treasure parcel tables, sect contribution exchanges, auction house procedures, military requisition systems, black markets, encumbrance rules, cultivation resource grade tables, vehicle fuel economies, ship maintenance cycles, local salvage rights law, donor wealth ratings, and post-scarcity fabrication policies.

The retained construct must have a boundary and cannot become general Astra doctrine through polish or repetition.

## Quarantine triggers
Quarantine when safe mapping is blocked by extraction damage; missing tables/sidecars; unclear value form, access channel, ownership, custody, mutation, or boundary; unsupported price/currency/wealth math; unsupported reward pacing; unsupported material grade or cultivation economy; unsupported contribution, requisition, license, black-market, inventory, storage, post-scarcity, repair, durability, fuel, ammo, upkeep, debt, tax, loot, salvage, or economy-simulation assumptions; or missing D09/D10/D13/D15/D18 support.

## Escalation triggers
Escalate repeated or high-impact pressure when Astra needs: wealth abstraction doctrine; canon currency stance or price bands; material/resource grade doctrine with D04/D06/D09/D17; crafting recipe/value conversion doctrine; post-scarcity access/pattern/fabrication infrastructure doctrine; fuel/maintenance/salvage/cargo interface doctrine; requisition audit doctrine with D15; reward-table governance; capacity/burden schema doctrine; or market-state/economy simulation doctrine with D10/D18.

## Rejected donor assumptions
```text
currency as universal value
coin-count as default tracking
fixed prices as Astra market truth
shop lists as world truth
wealth-by-level as progression law
treasure parcels as reward doctrine
loot tables as automatic value-entry
monster parts as default reward economy
salvage as automatic ownership
rarity tiers as objective value
item grade as universal value grade
cultivation resources as universal advancement currency
spirit stones as Astra default currency
sect contribution as advancement law
faction stores as free access
requisition as free supply
black markets as guaranteed shops
licenses as universal legality
post-scarcity as no-scarcity
inventory slots as universal capacity
weight / encumbrance as universal burden
coin weight as default pressure
magic bags / spatial rings as universal storage
repair costs as default object law
durability as universal degradation
fuel / ammo / food as universal tracking
taxes and upkeep as universal campaign sinks
abstract wealth ratings as universal wealth doctrine
debt currencies as universal economy
reward tables as progression pacing law
```

## Routing rule
A price list, shop table, loot table, wealth rating, slot count, fuel rule, requisition list, contribution chart, or reward schedule is evidence, not authority. Route by function to D17, D09, D10, D13, D14, D15, D16, D18, source-local retention, quarantine, or escalation.

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


---

# D17-07 — Records, Not-Final Schema, and Conversion Handoff Shapes

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Record scope
The following records are **not final schema**. They are doctrine-facing and conversion-facing control shapes. Runtime Gate B or later schema doctrine may replace or formalize them.

## Value State Record
```yaml
value_state_record:
  record_type: value_state
  value_id: string
  value_form: currency | barter_good | material | component | crafted_good | consumable | fuel | ammunition | supply | relic_fragment | cultivation_resource | biological_sample | data_or_information_asset | service | labor | favor | debt | obligation_value | license | permit | reputation_access | faction_credit | contribution_point | reward_claim | salvage_right | ownership_claim | storage_access | transport_access | market_access | requisition_authority | source_local_currency | source_local_value | mixed
  access_channel_refs: []
  scarcity_state: abundant | common | available | limited | scarce | rare | unique | restricted | illegal | rationed | monopolized | seasonal | unstable | contested | depleted | unknown | hidden | post_scarcity | source_local
  legality_permission_state: legal | licensed | permit_required | restricted | controlled | rationed | black_market_only | contraband | stolen | claimed_by_faction | claimed_by_law | claimed_by_domain_authority | salvage_disputed | use_allowed_sale_forbidden | possession_allowed_transport_forbidden | unknown | source_local
  ownership_custody_ref: string | null
  burden_refs: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  notes: string
```

## Access Channel Record
```yaml
access_channel_record:
  record_type: access_channel
  access_channel_id: string
  value_ref: string
  channel_type: purchase | sale | barter | trade | gift | reward | loot | salvage | resource_gathering | crafting_output | requisition | license_grant | faction_store | patron_grant | auction | black_market | market_board | institutional_access | domain_income | quest_payment | bounty | inheritance | loan | debt_settlement | theft | confiscation | tax_collection | tribute | ration_distribution | post_scarcity_access | source_local_channel
  channel_status: available_now | available_with_delay | available_with_requirement | available_at_cost | available_with_risk | available_only_through_project | available_only_through_faction | available_only_through_travel | available_only_through_black_market | available_only_through_source_local_procedure | unavailable | unknown | protected_hidden | quarantined | escalated
  required_permissions: []
  required_costs_or_sinks: []
  required_owner_file_handoffs: []
  source_local_boundary: string | null
  notes: string
```

## Acquisition / Exchange Record
```yaml
acquisition_exchange_record:
  record_type: acquisition_exchange
  transaction_id: string
  initiating_actor_or_group_ref: string
  value_refs: []
  access_channel_ref: string
  acquisition_intent: obtain | sell | trade | barter | request | requisition | borrow | lease | convert | claim | store | move | fabricate | source_local
  availability_outcome: available_now | available_with_delay | available_with_requirement | available_at_cost | available_with_risk | available_only_through_project | available_only_through_faction | available_only_through_travel | available_only_through_black_market | available_only_through_source_local_procedure | unavailable | unknown | protected_hidden | quarantined | escalated
  permission_custody_review_required: true | false | unknown
  exchange_conversion_friction: [transaction_cost, tax, tariff, delay, spoilage, loss_rate, exchange_rate, standing_requirement, broker_requirement, black_market_risk, requisition_approval, material_waste, custody_dispute, source_local_rule]
  outcome_state: acquired | acquired_with_cost | acquired_with_burden | acquired_with_dispute | acquired_with_trace | access_granted | access_limited | access_denied | exchange_completed | exchange_partial | exchange_delayed | exchange_failed | custody_changed | ownership_changed | claim_created | claim_contested | requisition_approved | requisition_denied | reward_delivered | loot_pending_review | salvage_pending_claim | black_market_trace_created | unavailable | quarantined | escalated | source_local_result
  owner_file_handoffs: []
  notes: string
```

## Value Entry Record
```yaml
value_entry_record:
  record_type: value_entry
  value_entry_id: string
  trigger_source: D13_project_completion | D14_discovery | D15_operation | D16_encounter_or_opposition | quest_completion | bounty_completion | loot_from_opposition | salvage_from_site | salvage_from_vehicle_platform | faction_grant | patron_payment | auction_result | inheritance | domain_income | resource_gathering | crafting_output | D18_milestone_handoff | source_local_reward
  source_authority: direct_possession | contract | bounty_issuer | quest_giver | faction_authority | law_authority | domain_authority | salvage_law | market_agreement | patron_promise | source_local_system | world_state_discovery | encounter_context | project_output | campaign_milestone | unknown_authority
  value_entry_category: reward_payment | reward_item | reward_access | reward_license | reward_claim | reward_favor | reward_information_asset | loot_currency | loot_item | loot_material | loot_component | loot_consumable | loot_relic_fragment | loot_source_local | salvage_component | salvage_material | salvage_data | salvage_platform_part | salvage_biological_sample | salvage_resource | bounty_payment | faction_grant | requisition_grant | domain_income | project_output | crafting_output | source_local_reward
  eligibility_state: eligible | eligible_with_condition | shared_eligibility | contested_eligibility | ineligible | unknown | protected_hidden | source_local
  custody_ownership_outcome_ref: string | null
  burden_sink_consequence_refs: []
  delivery_outcome: delivered | delivered_with_burden | delivered_with_cost | delivered_with_trace | delivered_with_claim | delivered_as_custody_only | delivered_as_access_only | delivered_as_source_local | split_required | escrow_required | claim_review_required | salvage_pending | reward_delayed | reward_denied | reward_partially_delivered | reward_converted | reward_quarantined | escalated_owner_file_problem
  owner_file_handoffs: []
  source_local_boundary: string | null
  notes: string
```

## Ownership / Custody Record
```yaml
ownership_custody_record:
  record_type: ownership_custody
  ownership_custody_id: string
  value_ref: string
  ownership_state: owned | borrowed | leased | licensed | loaned | rented | faction_held | escrowed | impounded | requisitioned | claimed | contested | stolen | salvage_pending | salvage_awarded | bound | soul_bound_source_local | lost | abandoned | unclaimed | unknown | source_local
  custody_state: possessed | held_in_custody | carried | stored | hidden | vehicle_stored | platform_stored | facility_stored | banked | vaulted | cached | escrowed | faction_held | impounded | requisition_held | lost | unknown | source_local
  owner_ref: string | null
  custodian_ref: string | null
  claimant_refs: []
  transfer_allowed: true | false | unknown | source_local
  sale_allowed: true | false | unknown | source_local
  use_allowed: true | false | unknown | source_local
  transport_allowed: true | false | unknown | source_local
  D10_state_owner: true
  D15_claim_or_enforcement_handoff_required: true | false | unknown
  notes: string
```

## Inventory / Burden Record
```yaml
inventory_burden_record:
  record_type: inventory_burden
  burden_id: string
  value_ref: string
  holding_mode: carried_on_person | equipped | worn | quick_access | packed | container_stored | vehicle_stored | platform_stored | facility_stored | banked | vaulted | cached | hidden | escrowed | faction_held | requisition_held | impounded | leased_storage | digital_or_pattern_stored | bound_to_actor | source_local_holding | unknown
  burden_types: [weight, bulk, volume, slot, quick_access_limit, container_capacity, transport_capacity, storage_capacity, security_burden, concealment_burden, legal_visibility, social_visibility, faction_trace, custody_risk, maintenance_burden, decay_or_spoilage, fuel_or_power_support, crew_or_labor_support, platform_cargo_burden, access_delay, retrieval_risk, source_local_burden]
  access_state: immediate_access | quick_access | scene_access | interval_access | safe_location_access | facility_access | vehicle_or_platform_access | faction_permission_access | licensed_access | locked_access | hidden_cache_access | delayed_access | blocked_access | source_local_access | unknown_access
  stability_state: stable | fragile | perishable | decaying | spoiling | unstable | contaminated | degrading | maintenance_required | expired | source_local_decay
  possession_scope: individual | party_shared | crew_shared | faction_shared | vehicle_or_platform | facility | domain | escrow | source_local_scope
  loss_risk_present: true | false | unknown
  owner_file_handoffs: []
  notes: string
```

## Loss / Confiscation / Recovery Record
```yaml
loss_confiscation_recovery_record:
  record_type: loss_confiscation_recovery
  loss_event_id: string
  value_ref: string
  trigger: overburden | flight | defeat | confiscation | tax_seizure | faction_claim | legal_inspection | theft | container_damage | platform_destruction | hazard_exposure | decay | spoilage | abandonment | failed_transport | source_local_trigger
  outcome: lost | damaged | impounded | stolen | abandoned | claimed_by_other | converted_to_unresolved_pressure | recoverable | recoverable_with_cost | recoverable_with_project | recoverable_with_operation | destroyed | quarantined | source_local_result
  lawful_trigger_confirmed: true | false | unknown
  owner_file_handoffs: []
  recovery_path_available: true | false | unknown
  notes: string
```

## Sink / Requisition / Upkeep Record
```yaml
sink_requisition_upkeep_record:
  record_type: sink_requisition_upkeep
  sink_id: string
  value_ref: string
  sink_type: consumption | upkeep | maintenance | repair_cost | fuel_use | ammo_use | component_use | license_fee | permit_renewal | tax | tariff | toll | dues | tribute | tithe | rent | storage_fee | broker_fee | auction_fee | transaction_fee | bribe | debt_payment | interest | faction_contribution | requisition_reservation | rationing | decay | spoilage | degradation | confiscation | seizure | sacrifice | cultivation_consumption | ritual_consumption | source_local_sink
  sink_timing: immediate | on_acquisition | on_exchange | on_use | on_damage | on_repair | on_storage | on_transport | on_maintenance_interval | on_license_interval | on_project_interval | on_scene_transition | on_travel_interval | on_faction_operation | on_campaign_interval | on_failure | on_success | on_overuse | ambient | scheduled | source_local_timing
  obligation_level: mandatory | required_for_access | required_for_legality | required_for_safety | required_for_maintenance | required_for_quality | optional_upgrade | optional_convenience | avoidable_with_risk | deferable_with_consequence | waived_by_standing | waived_by_license | source_local_obligation
  sink_effect: removed_from_circulation | consumed | reserved | locked | degraded | spoiled | transformed | converted_to_debt | converted_to_obligation | converted_to_trace | transferred_to_faction | transferred_to_law_authority | transferred_to_market_actor | sacrificed | destroyed | held_in_escrow | source_local_effect
  anti_poverty_trap_review_required: true | false | unknown
  owner_file_handoffs: []
  notes: string
```

## Debt / Obligation Value Record
```yaml
debt_obligation_value_record:
  record_type: debt_obligation_value
  debt_value_id: string
  debtor_ref: string
  creditor_ref: string
  debt_form: currency_debt | favor_debt | resource_debt | service_debt | requisition_debt | salvage_debt | patron_debt | faction_debt | legal_debt | source_local_debt
  debt_state: owed | current | deferred | partially_paid | defaulted | renegotiated | transferred | forgiven | converted_to_obligation | converted_to_pressure | source_local_debt_state
  value_side_owner: D17
  obligation_enforcement_owner: D15
  world_state_owner: D10
  payment_or_settlement_refs: []
  recovery_or_default_path: string | null
  notes: string
```

## Donor Value Mapping Record
```yaml
donor_value_mapping_record:
  record_type: donor_value_mapping
  donor_label: string
  donor_evidence_type: price_list | shop_inventory | loot_table | reward_table | treasure_parcel | currency | wealth_rating | inventory_rule | encumbrance_rule | requisition_list | contribution_chart | resource_grade | salvage_table | repair_durability_rule | fuel_ammo_rule | tax_upkeep_rule | debt_rule | post_scarcity_rule | market_rule | black_market_rule | license_rule | mixed
  donor_function_summary: string
  mapped_value_form: string | null
  mapped_access_channel: string | null
  mapped_d17_element: value_state | access_channel | acquisition_exchange | value_entry | ownership_custody | inventory_burden | sink_requisition_upkeep | debt_obligation_value | source_local | quarantine | escalation
  donor_price_or_currency_assumption_present: true | false | unknown
  donor_inventory_or_burden_assumption_present: true | false | unknown
  donor_reward_or_loot_assumption_present: true | false | unknown
  donor_requisition_or_sink_assumption_present: true | false | unknown
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  stripped_donor_assumptions: []
  rejected_import_notes: []
  research_guardrail_flags: [inflation_risk, poverty_trap_risk, hoarding_risk, reward_collapse_risk, inventory_paralysis_risk, grind_wall_risk, uncontrolled_salvage_risk, post_scarcity_erasure_risk, donor_value_law_leakage_risk]
  owner_file_handoffs: []
  source_local_boundary: string | null
  confidence: high | medium | low | blocked
```


---

# D17-09 — Integration Checklists, DDR Register, and Acceptance Criteria

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Integration checklist
D17 is integrated only when all are true:
```text
Value is classified by form, access channel, scarcity, legality, ownership/custody, and burden.
Acquisition and exchange do not assume price equals access.
Reward, loot, salvage, bounty, faction grants, requisition grants, Project outputs, crafting outputs, and source-local value-entry do not imply automatic ownership or power.
Custody and ownership are separate.
Inventory is represented as burden, access, storage, custody, visibility, maintenance, decay, and transport pressure.
No universal slot, weight, bulk, encumbrance, spatial storage, cargo, or post-scarcity storage law is created.
Requisition, upkeep, maintenance, consumption, taxes, dues, debt, fuel, ammo, decay, confiscation, cultivation consumption, and source-local sinks are supported without becoming universal.
Anti-poverty-trap review is required for severe sink/upkeep/requisition pressure.
Donor economy systems are mapped by function, not label.
Bounded source-local value systems are preserved where appropriate.
Unsupported value constructs are quarantined.
Repeated or high-impact missing doctrine is escalated.
Owner-file handoffs are explicit.
```

## Owner-file handoff checklist
```text
D03 — resource pools, charges, overdraw, recharge, resource-side instability.
D04 — advancement gates, breakthroughs, progression proof, advancement-adjacent costs.
D05 — methods used to acquire, appraise, negotiate, craft, salvage, conceal, or transport.
D06 — Techniques, domains, power expression, ritual/power consumption.
D07 — harm, contamination, exposure, corruption, injury, condition consequences.
D08 — actor body/substrate, companion burden, bound actor implications.
D09 — object, item, material, relic, implant, vehicle, ship, platform, container, cargo, module, tool state.
D10 — world-state, law records, market facts, scarcity, hidden truth, public belief, rumor, regional economy.
D11 — presentation, hidden-state boundaries, misinformation, player-facing summary.
D12 — scene timing, quick access timing, action cadence, immediate use attempts.
D13 — Projects for crafting, salvage, repair, maintenance, acquisition, storage, transport, resource gathering.
D14 — travel, discovery, site-entry, route access, transport pressure.
D15 — claims, obligations, enforcement, faction stores, licenses, requisition authority, law operations, domain control.
D16 — encounter reward pressure, loot triggers, salvage triggers, opposition-related value.
D18 — campaign economy, settlement/domain income, seasonal scarcity, inflation/collapse, state aging, long-horizon reward pacing.
```

## Anti-drift rules
```text
Do not treat money as the default form of value.
Do not treat price as access.
Do not treat possession as ownership.
Do not treat rarity as final value.
Do not treat loot as lawful property by default.
Do not treat salvage as free wealth.
Do not treat reward as automatic power.
Do not treat requisition as free supply.
Do not treat post-scarcity as no-scarcity.
Do not treat inventory as default slots, weight, bulk, or encumbrance.
Do not treat containers, magic bags, spatial rings, cargo holds, banks, or pattern libraries as burden-erasure devices unless an owner file or source-local rule supports it.
Do not import donor shop lists, price tables, wealth-by-level, treasure parcels, loot tables, reward schedules, contribution charts, or currency systems as Astra law.
Do not let D17 become D09 item-state, D10 market-state/world-state, D13 Project procedure, D15 institutional enforcement, D16 reward-trigger construction, or D18 campaign economy doctrine.
Do not let source-local economy systems become Astra law through repetition alone.
```

## Research-derived guardrail register
```text
inflation_risk — value faucets exceed sink/burden review.
poverty_trap_risk — sinks/upkeep create unrecoverable resource collapse.
hoarding_risk — inventory/storage permits lossless accumulation.
reward_collapse_risk — rewards lose value because economy or sinks are miscalibrated.
inventory_paralysis_risk — burden creates excessive bookkeeping or lost-loot anxiety.
grind_wall_risk — scarcity blocks progression without alternate access.
uncontrolled_salvage_risk — salvage becomes free or unbounded wealth.
post_scarcity_erasure_risk — fabrication or storage erases scarcity and access pressure.
donor_value_law_leakage_risk — donor price/currency/slot/reward/sink logic becomes Astra law.
```

## DDR register
### D17-DDR-001 — Value is broader than money
Decision: D17 treats value as currency, barter, material, service, labor, favor, debt, license, permit, access, claim, storage, transport, requisition authority, cultivation resource, source-local value, and more.
Rationale: Corpus-scale conversion requires fantasy, sci-fi, cultivation, requisition, barter, and abstract wealth compatibility.
Control: Records require value form and access channel.

### D17-DDR-002 — Access is not price
Decision: Price is only one possible friction. Availability, permission, legality, custody, scarcity, standing, license, and owner support matter.
Control: Availability outcomes and acquisition records prevent shop-list drift.

### D17-DDR-003 — Inventory is burden/access/custody
Decision: D17 does not define default slots, weight, bulk, or encumbrance.
Control: Inventory/Burden Record captures many burden types without final schema.

### D17-DDR-004 — Reward, loot, and salvage are value-entry
Decision: Rewards, loot, salvage, bounties, faction grants, requisition grants, Project outputs, and crafting outputs are value-entry, not automatic power or ownership.
Control: Value Entry and Ownership/Custody Records require authority, eligibility, burden, and claim state.

### D17-DDR-005 — Requisition and sinks are first-class but not universal
Decision: D17 supports taxes, upkeep, fuel, ammo, repair, debt, dues, contribution, consumption, confiscation, decay, requisition, and source-local sinks without universalizing bookkeeping.
Control: Sink/Requisition/Upkeep Record and anti-poverty-trap guardrail.

### D17-DDR-006 — Donor value systems map by function
Decision: Donor price lists, loot tables, reward schedules, wealth ratings, inventory rules, fuel rules, contribution charts, requisition lists, and sink formulas are evidence only.
Control: Functional donor value mapping ladder and rejected-import notes.

## Acceptance criteria
D17 is accepted if it can:
```text
Classify value by form, access channel, scarcity, legality, ownership/custody, and burden.
Handle acquisition and exchange without assuming price equals access.
Handle reward, loot, salvage, bounty, faction grant, requisition grant, project output, crafting output, and source-local value-entry without automatic ownership or power.
Distinguish custody from ownership.
Represent inventory as burden, access, storage, custody, visibility, maintenance, decay, and transport pressure.
Support multiple burden types without universal slots, weight, or encumbrance.
Support requisition, upkeep, maintenance, consumption, taxes, dues, debt, fuel, ammo, decay, confiscation, cultivation consumption, and source-local sinks without making any universal.
Prevent unrecoverable resource collapse unless explicit high-risk support exists.
Map donor economy systems by function, not label.
Preserve bounded source-local value systems.
Quarantine unsupported value constructs.
Escalate repeated or high-impact missing doctrine.
Route object, world, project, faction, opposition, reward, and campaign effects to owner files without stealing ownership.
```

## Risk fixes embedded
This control file confirms the D17 pre-generation risk audit has been embedded across the pack: money-collapse risk, price-as-access risk, possession-as-ownership risk, free-salvage risk, reward-as-power risk, inventory-default risk, burden-erasure storage risk, post-scarcity no-scarcity risk, free-requisition risk, poverty-trap risk, universal-sink risk, debt-as-money risk, cultivation-resource-as-advancement-currency risk, D10/D09/D13/D15/D18 ownership theft risk, source-local generalization risk, and record-shape final-schema risk.


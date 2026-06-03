# B05 Acquisition, Reward, Requisition, and Value-Flow Procedure

## 1. Purpose and status

B05 is the fifth Batch B operational doctrine draft for Astra acquisition, reward, loot, salvage, requisition, exchange, market access, availability, scarcity, value conversion, upkeep, consumption, economic pressure, and value sinks. It sits after B01 scene/activity/encounter procedure, B02 action declaration/cost commitment/resolution trigger procedure, B03 item/gear/equipment/object-system construct and asset-use procedure, and B04 inventory/storage/custody/burden procedure. B05 builds on B04 inventory, storage, custody, access, lawful loss, recovery, and burden procedure without reopening final inventory math, item stats, market law, currency systems, reward tables, runtime ledgers, or sourcebook economy prose.

Status posture:
- This file is Batch B operational-procedure draft material.
- This file is not current canon, not final mechanics, not runtime authority, not sourcebook prose, and not player-facing rule text.
- C00 remains the schema handoff control surface for Batch B to C-family routing.
- B05 treats `B01_scene_encounter_and_activity_procedure.md`, `B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md`, `B03_item_gear_equipment_and_asset_use_procedure.md`, and `B04_inventory_storage_custody_and_burden_procedure.md` as upstream Batch B context and must build on them, not rewrite them.
- D00, D09, D10, D15, D16, D17, and D19 source-pack files are referenced only as draft source-pack/reference material. They are not current doctrine authority, final mechanics, runtime authority, canon, or sourcebook prose.
- B05 records, examples, and handoff blocks are doctrine-facing only; they are not runtime state, backend contracts, sourcebook statblocks, canon entries, player-facing rule text, accepted lexicon, or final mechanics.

Required reference boundaries preserved by B05:
- `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md` for upstream Batch B scene, activity, encounter, transition, checkpoint, and owner-file handoff procedure.
- `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` for upstream Batch B action declaration, feasibility, cost commitment, no-roll/roll-trigger, and action-to-delta routing procedure.
- `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md` for upstream Batch B object-use, object readiness, object custody triage, object-state handoff, inventory/storage handoff, and object-use delta routing procedure.
- `docs/doctrine/operations/batch_b/B04_inventory_storage_custody_and_burden_procedure.md` for upstream Batch B inventory, storage, custody, possession, access, quick-access, burden, legal visibility, lawful loss, and recovery routing procedure.
- `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` for shared Batch C base fields, `pending_schema`, source-local boundary, rejected donor element, canon eligibility, review routing, provenance, and missing-schema fallback language.
- `docs/doctrine/native_design/d_series/source_packs/astra_d00_doctrine_pack_v0_1/D00-03_state_delta_commit_protocol.md` for the draft source-pack principle that every meaningful action commits at least one delta to a recognized owner, while B05 does not own every delta format.
- `docs/doctrine/native_design/d_series/source_packs/astra_d09_doctrine_pack_v0_1/D09-06_crafting_repair_salvage_modification_upgrade_and_requisition_interface.md` for draft source-pack crafting, repair, salvage, modification, upgrade, maintenance, and requisition interface source material, while B05 must not define final crafting, salvage, repair, modification, upgrade, or item mechanics.
- `docs/doctrine/native_design/d_series/source_packs/astra_d10_doctrine_pack_v0_1/D10-05_economy_scarcity_strategic_resources_market_requisition_register.md` for draft source-pack economy, scarcity, strategic-resource, market, and requisition source material, while B05 must not define final market law, currency math, scarcity algorithms, or runtime economy state.
- `docs/doctrine/native_design/d_series/source_packs/D15_faction_relationship_domain_and_institutional_operations_doctrine_pack/D15_doctrine_pack/D15-01_organized_actors_standing_pressure_obligations_claims_and_operation_anatomy.md` for draft source-pack organized actor, standing, pressure, obligation, claim, and institutional-operation source material, while B05 must not define final faction law or final obligation schema.
- `docs/doctrine/native_design/d_series/source_packs/D16_opposition_creature_encounter_and_hazard_construction_doctrine_pack/D16_doctrine_pack/D16-00_opposition_creature_encounter_and_hazard_construction_owner_boundaries.md` for draft source-pack encounter/opposition reward-pressure boundaries, while B05 must not define opposition construction, encounter rewards, combat loot tables, or final hazard treasure.
- `docs/doctrine/native_design/d_series/source_packs/D17_economy_acquisition_inventory_reward_and_requisition_doctrine_pack/D17_doctrine_pack/D17-00_economy_acquisition_inventory_reward_and_requisition_owner_boundaries.md`, `D17-01_value_forms_access_channels_scarcity_ownership_custody_and_burden_states.md`, `D17-02_acquisition_exchange_market_access_availability_and_value_conversion.md`, `D17-03_reward_loot_salvage_claim_and_value_entry_procedure.md`, `D17-05_requisition_upkeep_consumption_value_sinks_and_economic_pressure.md`, `D17-06_source_local_economy_donor_value_mapping_quarantine_and_escalation.md`, and `D17-07_records_not_final_schema_and_conversion_handoff_shapes.md` for draft source-pack economy, value, acquisition, reward, requisition, sink, donor mapping, and not-final-record source material, while B05 must not promote D17 records to final Astra schema.
- `docs/doctrine/native_design/d_series/source_packs/D19_cross_pack_integration_conflict_audit_and_conversion_readiness_capstone_pack/D19_capstone_doctrine_pack/D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md` for draft source-pack record-shape governance warnings and not-final-schema controls.

## 2. Owner layer

B05 belongs to Batch B operational doctrine. It routes acquisition, reward, loot, salvage, requisition, exchange, market access, availability, scarcity, value conversion, upkeep, consumption, economic pressure, and value-sink procedure between upstream B01/B02/B03/B04 procedure, the A-family doctrine layer, the C00 schema handoff control surface, future C01-C14 schema families, source-local donor economy/reward/requisition quarantine, and later economy, inventory, object, faction, law, world, project, crafting, advancement, canon, runtime, and training owners.

B05 may identify that a handoff is needed to a likely owner, but it must not perform that owner's work. When B05 cannot identify a valid owner or schema family, it must mark `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` instead of inventing Astra schema, mechanics, runtime state, backend ledger, price table, reward table, ownership database, legal code, economy law, canon, or sourcebook economy rules.

## 3. What B05 owns

B05 owns doctrine-level operational procedure for:
- acquisition intake procedure after B01, B02, B03, or B04 produce acquisition, value, reward, requisition, exchange, upkeep, consumption, scarcity, availability, or value-sink pressure;
- value-form classification;
- acquisition-channel classification;
- exchange, barter, purchase, sale, trade, favor, obligation, claim, reward, salvage, requisition, tax, fee, tribute, rationing, black-market, and restricted-access routing;
- market access and availability procedure;
- scarcity-state identification;
- value conversion procedure as routing, not math;
- reward, loot, salvage, and claim-entry procedure;
- lawful reward and salvage ownership/custody separation;
- requisition request and intake procedure;
- upkeep, consumption, maintenance cost, value sink, and economic pressure routing;
- faction, institution, and world-law handoff for access, licenses, permits, claims, restricted goods, requisition authority, taxation pressure, tribute, tolls, fees, and market disruption;
- inventory, custody, storage, access, possession, burden, lawful loss, and recovery handoff to B04;
- object identity, material, function, damage, repair, modification, crafting, and salvage-material handoff to B03 and object owners;
- value-flow state-delta routing;
- B05-to-C00/C-family handoff references when acquisition/value/economy handling produces conversion records;
- source-local donor economy, reward, requisition, value, market, scarcity, and value-sink quarantine and escalation rules;
- examples of good and bad B05 usage;
- minimum assertions and acceptance criteria for B05.

## 4. What B05 must not own

B05 must not define or promote:
- final economy schema;
- final inventory schema;
- final object schema;
- C-family schema fields;
- C01-C14 schema contents;
- final currency math;
- final price lists;
- final shop lists;
- final market tables;
- final reward tables;
- final loot tables;
- final treasure tables;
- final wealth-by-level math;
- final requisition rating system;
- final rationing system;
- final taxation law;
- final legal code;
- final faction law;
- final ownership database;
- final item rarity/tier economy;
- final value conversion formulas;
- final scarcity algorithms;
- final availability algorithms;
- final black-market procedure;
- final salvage-rights law;
- final upkeep, maintenance, or consumption formulas;
- final crafting, salvage, repair, modification, or upgrade procedure;
- final advancement/progression reward pacing;
- final cultivation-resource economy;
- final post-scarcity economy;
- runtime economy state;
- runtime inventory ledger;
- runtime entity/component/event/state schemas;
- persistent campaign state;
- command lifecycle implementation;
- context packet compiler;
- hidden-information runtime state;
- live-play narration behavior;
- final canon promotion;
- accepted lexicon terms;
- sourcebook prose;
- donor economy, reward, market, rationing, scarcity, loot, salvage, requisition, upkeep, or value-conversion systems as Astra defaults.

## 5. Non-collapse rule

Money is not the default form of value. Price is not access. Availability is not ownership. Possession is not ownership. Ownership is not legality. Rarity is not final value. Loot is not lawful property by default. Salvage is not free wealth. Reward is not automatic power. Requisition is not free supply. A market is not a guaranteed shop list. A black market is not guaranteed access. Scarcity is contextual, not universal. Post-scarcity does not mean no scarcity.

B05 keeps these categories separate:
- value form identifies what kind of value is being handled;
- acquisition channel identifies how the value is approached, offered, taken, claimed, exchanged, consumed, reserved, or routed;
- availability identifies whether the value can be accessed in the current context;
- market access identifies whether an actor may enter or use a market channel;
- scarcity identifies contextual pressure, not universal worth;
- possession identifies physical or operational control and routes to B04;
- ownership identifies claim status and routes to economy/law/faction/custody owners;
- legality identifies permission or legal exposure and routes to world/faction/law owners;
- burden identifies carrying, storage, security, trace, upkeep, or transport pressure and routes to B04 and relevant owners;
- value conversion identifies that one value form must be abstracted or translated, not a formula for doing so;
- source-local donor economy systems identify source evidence or local campaign procedure, not Astra defaults.

B05 must not collapse acquisition into purchase, market into shop list, reward into treasure parcel, requisition into free gear, loot into owned property, salvage into unbounded material, scarcity into price, price into access, legal access into ownership, possession into legality, or value conversion into universal currency math.

## 6. Value, acquisition, reward, requisition, and value-flow definitions

For B05 procedure:
- `value` means a transferable, consumable, claimable, reservable, restricted, informational, social, legal, material, service, access, shelter, transport, protection, reputation, or source-local benefit that can affect future procedure.
- `acquisition` means the doctrine-facing attempt, opportunity, offer, transfer, taking, claiming, receiving, reserving, spending, or conversion of value through a channel.
- `reward` means value offered, earned, granted, promised, claimed, delivered, withheld, disputed, or converted because of scene, activity, encounter, project, faction, world, or source-local procedure. Reward may be ownership, custody, access, license, permit, favor, information, protection, claim, obligation, or source-local entitlement.
- `loot` means value identified after conflict, exploration, hazard, opposition, theft, abandonment, or source-local event. Loot creates value-entry and custody pressure first; it does not create lawful ownership by default.
- `salvage` means value recovered from damaged, abandoned, destroyed, derelict, field-stripped, harvested, or reusable objects, actors, sites, wrecks, environments, or systems. Salvage creates object-state, claim, law, custody, contamination, repair, project, and value-flow pressure; it is not free wealth by default.
- `requisition` means value requested, reserved, issued, denied, delayed, audited, recalled, consumed, or conditioned through institutional, faction, military, guild, sect, corporate, expeditionary, legal, or source-local authority. Requisition is not purchase and is not free supply.
- `value_flow` means a doctrine-facing value movement or pressure state that may become a delta, owner handoff, transition note, quarantine, escalation, or no-delta result.
- `value_sink` means a procedure that removes, reserves, locks, transforms, transfers, degrades, consumes, sacrifices, taxes, obligates, or otherwise pressures value without necessarily destroying it.
- `economic_pressure` means persistent or meaningful pressure created by scarcity, upkeep, consumption, debt, obligation, market disruption, access restriction, law, faction standing, stock depletion, trace, taxation, tribute, rationing, fees, or source-local economy effects.

Cultivation resources, sect contribution, favor currencies, cyberpunk restricted gear, fantasy coins, treasure parcels, requisition ratings, crafting currencies, post-scarcity fabrication rights, vehicle fuel economies, and donor black-market procedures are source-local until owner-supported or canonized.

## 7. Acquisition/value-flow intake procedure

When B01, B02, B03, B04, or a later owner identifies acquisition/value/reward/requisition pressure, B05 intake applies this sequence:

1. Identify the upstream trigger: scene transition, action declaration, cost commitment, object use, inventory/custody transfer, storage access, lawful loss, recovery, exploration find, encounter spoils, project output, faction operation, market contact, upkeep interval, source-local procedure, or owner-file note.
2. Determine whether the event is meaningful. If the value event has no future consequence, produce `no_delta_required` and avoid false permanence.
3. Classify the value form using Section 8. If no safe classification exists, use `unknown_value` or `source_local_value` and route review.
4. Classify the acquisition channel using Section 9. If no safe classification exists, use `unknown_acquisition` or `source_local_acquisition` and route review.
5. Identify availability, market access, restricted-access posture, and scarcity state using Section 10.
6. Separate possession, ownership, custody, legality, access, burden, and inventory questions using Section 16.
7. Identify whether exchange, claim, reward, loot, salvage, requisition, upkeep, consumption, sink, or value conversion procedure applies.
8. Route every meaningful value-flow event to at least one recognized owner, or explicitly produce `no_delta_required`, `transition_note`, `source_local_retained_effect`, `quarantined_unresolved_delta`, `owner_file_escalation`, `pending_schema`, `human_review`, or `defer_until_schema_exists`.
9. If C-family conversion records may be needed, use C00 handoff language and the lightweight B05 handoff block without inventing C-family fields.
10. Preserve donor/source evidence, rejected donor elements, and source-local boundaries when source material supplies the value procedure.

B05 intake does not determine final prices, final quantity, final rarity, final currency conversion, final reward pacing, final legality, final stock state, or final runtime ledger state.

## 8. Value-form classification

B05 may classify value forms with this doctrine vocabulary:
- `currency`: a medium of exchange in the source or local context, without making money the default value form.
- `barter_good`: tradable non-currency value.
- `service`: performed work, aid, professional help, or operational support.
- `favor`: social credit, promised aid, or relational value.
- `obligation`: owed duty, debt, service, restriction, or future burden.
- `claim`: asserted right to property, reward, salvage, access, restitution, priority, debt, or entitlement.
- `license`: permission to hold, use, transport, sell, operate, craft, access, or deploy something under authority.
- `permit`: contextual authorization for entry, transaction, transport, construction, salvage, sale, research, or use.
- `ration`: limited entitlement, controlled allotment, or scarcity-managed issue.
- `requisition_credit`: institutional or source-local authorization unit for request/issue routing, not a final Astra rating.
- `faction_scrip`: faction-bounded exchange or access token.
- `reputation_access`: standing-based entry, discount, priority, trust, protection, or institutional access.
- `material_component`: material input, ingredient, spare, part, reagent, salvage piece, or object component.
- `strategic_resource`: resource whose control affects world, faction, project, logistics, military, political, or market pressure.
- `consumable_supply`: expendable supply such as fuel, rations, ammunition, medicine, charge, feedstock, or source-local supply.
- `salvage`: recovered value requiring claim, object-state, law, custody, or project review.
- `loot`: identified value from encounter, exploration, hazard, conflict, theft, or source-local event requiring ownership/custody review.
- `reward_right`: right to receive value, access, claim, rank, payment, title, boon, information, or institutional benefit.
- `information_value`: knowledge, map, secret, data, evidence, formula, password, rumor, proof, research lead, or bargaining information.
- `labor`: work capacity, service time, crew effort, specialist attention, or source-local labor currency.
- `shelter`: lodging, safehouse, berth, camp, legal residence, sanctuary, or protected rest access.
- `transport`: passage, vehicle use, route access, shipping, convoy, mount, platform berth, or travel service.
- `protection`: guard service, escort, immunity, sponsorship, legal cover, warding, insurance, or faction shield.
- `legal_status`: recognized standing, amnesty, writ, pardon, debt status, warrant clearance, title, claim status, or source-local legal marker.
- `access_right`: entry, use, priority, membership, docking, vault access, market entry, data access, or operational permission.
- `source_local_value`: donor or local value form retained as source-local only.
- `unknown_value`: unresolved value form requiring quarantine, escalation, or `human_review`.

Value-form classification is descriptive routing vocabulary only. It is not final lexicon, final economy schema, final item taxonomy, final rarity system, final currency list, or a player-facing rule list.

## 9. Acquisition-channel classification

B05 may classify acquisition channels with this doctrine vocabulary:
- `purchase`: value acquired by payment through a permitted or contextually recognized channel.
- `sale`: value disposed of for another value form.
- `barter`: value-for-value exchange without assuming currency.
- `trade`: negotiated exchange that may include goods, services, access, information, favor, or obligation.
- `gift`: value given without immediate exchange, while still requiring custody, legality, and obligation review.
- `reward`: value offered or granted because of completed, promised, or recognized action.
- `loot`: value identified through spoils, conflict, hazard, theft, abandoned holdings, or source-local loot procedure.
- `salvage`: value recovered from damaged, derelict, destroyed, abandoned, or harvestable sources.
- `claim`: value approached through asserted right, lien, inheritance, bounty, contract, law, faction, or source-local entitlement.
- `requisition`: institutional request, issue, reservation, recall, audit, or denial of value.
- `rationing`: limited issue or controlled allocation under scarcity or authority.
- `license_access`: access routed through license requirements.
- `permit_access`: access routed through permit requirements.
- `faction_grant`: value granted through faction standing, office, duty, alliance, sponsorship, or favor.
- `institutional_grant`: value granted through a guild, military, state, sect, corporation, academy, temple, expedition, or other institution.
- `market_exchange`: exchange through a market channel without assuming a guaranteed shop list.
- `black_market_exchange`: illicit or gray-market routing without assuming guaranteed access.
- `auction`: competitive bid, sealed bid, patronage, favor, or source-local auction channel.
- `tax_collection`: compelled transfer under authority.
- `tribute`: transfer owed to superior, protector, ruler, faction, domain, threat, or source-local power.
- `tithe`: required or customary contribution to institution, faith, sect, guild, domain, or source-local authority.
- `fee`: payment or value transfer for service, access, processing, license, permit, storage, broker, or transaction.
- `toll`: route, gate, bridge, docking, passage, or access charge.
- `lease`: temporary access or use in exchange for value, obligation, standing, or authority.
- `debt`: delayed value obligation, repayment, interest, lien, or claim-bearing pressure.
- `labor_exchange`: labor traded for value, access, protection, shelter, debt relief, standing, or source-local entitlement.
- `crafting_output`: value produced by craft/project process requiring owner handoff.
- `project_output`: value produced by downtime, faction, research, construction, domain, expedition, or operational project.
- `exploration_find`: value discovered in exploration requiring claim, custody, access, law, object, and scarcity review.
- `encounter_spoils`: value emerging from encounter/opposition/hazard procedure without defining reward tables.
- `legal_seizure`: authorized confiscation, impoundment, forfeiture, evidence retention, prize claim, tax seizure, or court/faction action.
- `theft_or_illicit_gain`: unlawful or disputed acquisition requiring legality, trace, faction/law, and custody review.
- `source_local_acquisition`: donor or local acquisition channel retained as source-local only.
- `unknown_acquisition`: unresolved channel requiring quarantine, escalation, or `human_review`.

Acquisition-channel classification does not authorize final mechanics, market lists, pricing, legality, black-market rules, tax law, requisition ratings, or reward pacing.

## 10. Market access, availability, scarcity, and restricted-access procedure

B05 market and availability procedure asks:

1. Is there a market, institution, faction, person, network, platform, storage site, legal authority, black-market channel, source-local channel, or world condition that could mediate the value flow?
2. Does the actor have access to that channel, or is access blocked, licensed, permitted, faction-locked, location-locked, disrupted, illegal, hidden, or unknown?
3. Is the desired value actually available in that channel now, or is it abundant, available, limited, rationed, restricted, licensed, illegal, controlled, faction-locked, location-locked, time-limited, disrupted, depleted, unstable, contested, hidden, black-market-only, source-local, or unknown?
4. Does scarcity create price pressure, delay, route pressure, faction attention, license/permit pressure, claim pressure, requisition pressure, project pressure, black-market risk, legal exposure, trace, conflict, debt, favor, obligation, or owner-file handoff?
5. Does restricted access require world/faction/law/institution handoff before any purchase, trade, requisition, salvage, or claim can resolve?
6. Does the market channel itself create a value sink, fee, tax, toll, transaction cost, broker pressure, auction pressure, bribe pressure, audit trail, trace, or hidden risk?
7. Is the procedure source-local or donor-specific and therefore quarantined, retained source-local, or escalated rather than promoted?

B05 may classify scarcity states with this doctrine vocabulary:
- `abundant`
- `available`
- `limited`
- `rationed`
- `restricted`
- `licensed`
- `illegal`
- `controlled`
- `faction_locked`
- `location_locked`
- `time_limited`
- `disrupted`
- `depleted`
- `unstable`
- `contested`
- `hidden`
- `black_market_only`
- `source_local_scarcity`
- `unknown_scarcity`

Price is not access. A market is not a guaranteed shop list. A black market is not guaranteed access. Availability is not ownership. Scarcity is contextual, not universal. Post-scarcity does not mean no scarcity. B05 must not define final availability algorithms, final scarcity algorithms, final market tables, final shop lists, final price lists, or final black-market procedure.

## 11. Exchange, barter, purchase, sale, trade, favor, obligation, and claim routing

When value moves through exchange, barter, purchase, sale, trade, favor, obligation, or claim routing, B05 separates:
- offered value form;
- requested value form;
- acquisition channel;
- access channel;
- market or non-market mediator;
- availability and scarcity state;
- legality and permission posture;
- ownership/custody/possession posture;
- burden, storage, trace, audit, upkeep, and sink pressure;
- value conversion need;
- source-local procedure and donor-system boundary;
- owner-file handoff and delta result.

Routing outcomes may include:
- exchange available but value not owned until B04/economy/law routing confirms status;
- exchange blocked by access, availability, license, permit, faction, law, scarcity, disruption, hidden information, or source-local boundary;
- value converted to claim, obligation, access, debt, service, favor, or unresolved pressure instead of currency;
- sale or trade creates ownership dispute, legal exposure, trace, tax, toll, fee, debt, obligation, or faction pressure;
- barter or trade requires object-state, inventory, custody, burden, and source-local review before completion;
- favor or obligation requires faction/institution/relationship owner handoff, not economy math only;
- claim requires world/faction/law/ownership/custody review before being treated as obtained value.

B05 does not resolve final exchange rates, conversion formulas, tax law, debt mechanics, legal enforceability, market prices, or persistent ledgers.

## 12. Reward, loot, salvage, and claim-entry procedure

Reward, loot, salvage, and claim-entry procedure applies when value enters attention because of scene, activity, encounter, exploration, project, faction, world, opposition, hazard, salvage, donor-source, or institutional trigger.

Procedure:
1. Identify the value-entry trigger and upstream owner: B01 scene/encounter/activity, B02 action, B03 object use, B04 inventory/custody/loss/recovery, project, faction, world, opposition/hazard, source-local procedure, or human note.
2. Identify the source and authority: patron, faction, institution, law, contract, opposition, abandoned site, ownerless field, contested wreck, donor table, source-local rule, hidden owner, or unknown.
3. Classify the entry category: reward, loot, salvage, claim, exploration find, encounter spoils, project output, crafting output, legal seizure, tax/tribute, source-local, or unknown.
4. Classify value form, acquisition channel, scarcity state, market/access posture, and value-flow state.
5. Separate custody from ownership and possession from legality. Loot creates custody pressure first; salvage creates claim and object-state pressure; reward creates delivery and authority pressure.
6. Route object identity, damage, material, component, harvest, contamination, repair, modification, upgrade, or crafting questions to B03/object/project owners.
7. Route possession, holding mode, storage, quick access, transfer, lawful loss, recovery, burden, concealment, trace, custody, and inventory pressure to B04.
8. Route claim, legal status, license, permit, salvage rights, restricted goods, tax, tribute, faction dispute, institutional grant, or market disruption to world/faction/law/institution owners.
9. Route reward pacing, advancement/progression implications, automatic-power risk, cultivation-resource implications, and power-grant implications to advancement/power/canon owners rather than resolving them in B05.
10. Produce a value-flow outcome such as `value_obtained`, `value_deferred`, `value_disputed`, `value_transferred`, `value_restricted`, `value_converted_to_claim`, `value_converted_to_obligation`, `owner_routed`, `quarantined_unresolved_delta`, or `owner_file_escalation`.

Reward principles:
- Loot is custody first, not lawful property by default.
- Salvage is claim-bearing, not free wealth by default.
- Reward is not automatic power.
- A rare drop is evidence of possible value, not final Astra rarity doctrine.
- A treasure parcel, bounty, cultivation resource, sect contribution award, mission payout, or requisition rating is source-local until owner-supported or canonized.
- Reward division may identify disputed claims, party custody, faction share, patron claim, tax/tribute, escrow, or source-local split, but B05 must not define final reward-splitting math.

## 13. Requisition, rationing, license, permit, authority, and institutional access procedure

Requisition, rationing, license, permit, authority, and institutional access procedure applies when value is requested, issued, reserved, denied, delayed, recalled, rationed, audited, made conditional, or restricted by an organization or authority.

Procedure:
1. Identify the authority: faction, institution, military, guild, sect, corporation, state, temple, academy, ship, expedition, patron, law office, quartermaster, logistics owner, source-local authority, or unknown.
2. Identify the requested value form and object/value reference.
3. Identify the requisition channel: requisition, rationing, license access, permit access, faction grant, institutional grant, legal seizure, lease, debt, source-local requisition, or unknown.
4. Identify authority status: requested, approved, denied, delayed, conditional, rationed, exhausted, authority required, source-local, or unknown.
5. Identify conditions: return required, audit required, custody only, ownership transfer, temporary use, restricted use, geographic limit, legal visibility, standing cost, debt, obligation, trace, storage, upkeep, consumption, maintenance, ration interval, recall risk, or source-local condition.
6. Route possession, custody, storage, access, burden, transfer, escrow, impoundment, and recovery to B04.
7. Route object readiness, damage, maintenance, modifications, restricted object identity, material, installable assets, and salvage/crafting interface to B03/object owners.
8. Route standing, authority, claims, obligations, permits, licenses, restricted goods, rationing, disruption, tax, audit, and institutional consequences to world/faction/law/institution owners.
9. Produce value-flow states such as `requisition_requested`, `requisition_approved`, `requisition_denied`, `market_access_blocked`, `scarcity_identified`, `owner_handoff_required`, or `source_local_value_procedure`.

Requisition is not purchase and not free supply. Rationing is not a final ration system. License and permit access are not final law. Institutional grants are not final ownership by default. B05 must not define final requisition ratings, final ration formulas, final license law, final permit law, or final faction authority mechanics.

## 14. Upkeep, consumption, maintenance cost, value sink, and economic pressure routing

Upkeep, consumption, maintenance cost, value sink, and economic pressure routing applies when value is due, spent, consumed, reserved, lost, transformed, locked, taxed, degraded, spoiled, sacrificed, paid, seized, transferred, or converted to future pressure.

B05 recognizes value-sink and pressure examples including:
- consumption, upkeep, maintenance, repair cost, fuel use, ammunition use, component use, license fee, permit renewal, tax, tariff, toll, dues, tribute, tithe, rent, storage fee, broker fee, auction fee, transaction fee, bribe, debt payment, interest, faction contribution, requisition reservation, rationing, decay, spoilage, degradation, confiscation, seizure, sacrifice, cultivation consumption, ritual consumption, and source-local sink.

Routing procedure:
1. Identify whether the sink is mandatory, required for access, required for legality, required for safety, required for maintenance, required for quality, optional, avoidable with risk, deferable with consequence, waived by standing, waived by license, source-local, or unknown.
2. Identify timing: immediate, on acquisition, on exchange, on use, on damage, on repair, on storage, on transport, on maintenance interval, on license interval, on project interval, on scene transition, on travel interval, on faction operation, on campaign interval, on failure, on success, on overuse, ambient, scheduled, source-local, or unknown.
3. Identify effect: value removed, consumed, reserved, locked, degraded, spoiled, transformed, converted to debt, converted to obligation, converted to trace, transferred to faction, transferred to law authority, transferred to market actor, sacrificed, destroyed, held in escrow, source-local, or unknown.
4. Route object degradation, repair, maintenance, material consumption, crafting inputs, salvage components, and asset readiness to B03/object/project owners.
5. Route inventory burden, storage cost, custody, quick access, loss, recovery, transfer, lawful seizure, and holding pressure to B04.
6. Route tax, tribute, tithe, toll, dues, legal seizure, faction contribution, debt, obligation, standing, law, and market disruption to world/faction/law/institution owners.
7. Identify anti-poverty-trap, pacing, advancement, or campaign pressure as review topics without defining final reward pacing or economy balance.

Not every sink destroys value. Taxes transfer value. Debt converts cost to future obligation. Requisition may reserve supply. Confiscation changes custody. B05 may identify pressure but must not define final upkeep formulas, consumption formulas, maintenance formulas, poverty traps, reward pacing, or runtime economy state.

## 15. Value conversion and abstraction procedure

B05 value conversion is routing, not math. It identifies that one value form must be translated, abstracted, deferred, quarantined, or handed off before it can be used in Astra doctrine.

Procedure:
1. Identify source value form and target value form, if any.
2. Identify whether conversion is between money, goods, service, favor, obligation, claim, license, permit, ration, requisition credit, faction scrip, reputation access, material, strategic resource, consumable supply, salvage, loot, reward right, information, labor, shelter, transport, protection, legal status, access right, source-local value, or unknown value.
3. Identify who has authority to convert: market actor, faction, institution, law, patron, project owner, object owner, canon owner, schema owner, human reviewer, source-local procedure, or unknown.
4. Identify conversion posture: direct exchange, barter, sale, purchase, trade, favor, obligation, claim, escrow, debt, access grant, license/permit, ration, requisition, salvage claim, information trade, source-local retained effect, or unresolved pressure.
5. Identify what must not be converted: donor currency math, exact price lists, reward pacing, rarity tiers, requisition ratings, treasure parcels, wealth-by-level math, cultivation grades, post-scarcity fabrication rules, or black-market procedures as Astra defaults.
6. Produce a routing outcome: `value_converted_to_claim`, `value_converted_to_obligation`, `value_converted_to_access`, `value_converted_to_unresolved_pressure`, `source_local_retained_effect`, `quarantined_unresolved_delta`, `owner_file_escalation`, or `defer_until_schema_exists`.

B05 must not define final conversion formulas, final exchange rates, final currency systems, final value ratings, final rarity tiers, final price lists, final reward tables, or final C-family fields.

## 16. Ownership, custody, legality, burden, and inventory handoff rules

B05 must keep ownership, custody, possession, legality, availability, access, and burden separate:
- availability means value can potentially be accessed in context;
- access means an actor can use a channel or permission path;
- possession means an actor, party, container, site, vehicle, platform, faction, or institution currently controls the value physically or operationally;
- custody means recognized responsibility or holding authority, which may be temporary, disputed, escrowed, impounded, faction-held, or source-local;
- ownership means recognized claim or title, which may be confirmed, disputed, factional, legal, unlawful, source-local, or unknown;
- legality means permission or legal exposure, not ownership;
- burden means carrying, storage, security, trace, upkeep, transport, access, concealment, audit, maintenance, spoilage, or support pressure.

Handoff rules:
- Route possession, custody, storage, quick access, transfer, lawful loss, recovery, escrow, impoundment, concealment, trace, access state, holding mode, and burden to B04.
- Route object identity, function, material, component, damage, repair, maintenance, modification, upgrade, crafting output, project output, and salvage material to B03/object/project owners.
- Route ownership disputes, legal claims, restricted goods, licenses, permits, salvage rights, taxation, tribute, theft, lawful seizure, market disruption, and faction/institution claims to world/faction/law/institution owners.
- Route value conversion, reward entry, requisition intake, scarcity, and market access through B05 before forwarding to C00 or later owner files.

B05 may route inventory/custody/burden questions to B04, but it must not define final inventory schema, ownership database, or runtime ledger. B05 may route object identity/material/function questions to B03/object owners, but it must not define final object schema or item stats.

## 17. World, faction, institution, law, and market-disruption handoff rules

B05 must hand off world, faction, institution, law, and market-disruption pressure when value flow depends on:
- license, permit, legal status, writ, title, citizenship, membership, amnesty, warrant, seizure, impoundment, tax, tariff, toll, tribute, tithe, dues, rent, salvage rights, restricted goods, contraband, black-market access, auction authority, or legal market access;
- faction standing, obligation, debt, favor, reputation access, faction scrip, rationing, requisition authority, institutional grant, quartermaster approval, audit, recall, patron claim, domain pressure, market disruption, blockade, embargo, shortage, war, disaster, strike, political restriction, or source-local institution;
- ownership disputes, inheritance, claims, liens, bounties, reward rights, party division, escrow, shared ownership, shared custody, faction claim, legal seizure, theft, illicit gain, or contested salvage;
- strategic-resource control, post-scarcity fabrication limits, cultivation-resource access, sect contribution, cyberpunk restricted gear, fantasy coinage, treasure parcel, donor requisition rating, donor black-market procedure, or other source-local economy construct.

B05 identifies the handoff reason and value-flow state, but it must not define final world law, final faction law, final taxation law, final market law, final legal code, final ownership database, final rationing system, or final requisition authority mechanics.

## 18. Value-flow state-delta routing

B05 may use these doctrine-facing value-flow states:
- `acquisition_declared`
- `acquisition_confirmed`
- `acquisition_blocked`
- `reward_offered`
- `reward_claimed`
- `reward_disputed`
- `loot_identified`
- `salvage_identified`
- `claim_pending`
- `claim_disputed`
- `requisition_requested`
- `requisition_approved`
- `requisition_denied`
- `exchange_available`
- `exchange_blocked`
- `market_access_confirmed`
- `market_access_blocked`
- `scarcity_identified`
- `value_conversion_needed`
- `upkeep_due`
- `value_sink_triggered`
- `owner_handoff_required`
- `source_local_value_procedure`
- `value_flow_quarantined_gap`

B05 may use these doctrine-facing value-flow outcomes:
- `no_delta_required`
- `value_obtained`
- `value_spent`
- `value_committed`
- `value_reserved`
- `value_lost`
- `value_disputed`
- `value_transferred`
- `value_restricted`
- `value_deferred`
- `value_converted_to_claim`
- `value_converted_to_obligation`
- `value_converted_to_access`
- `value_converted_to_unresolved_pressure`
- `owner_routed`
- `transition_note`
- `source_local_retained_effect`
- `quarantined_unresolved_delta`
- `owner_file_escalation`

Every meaningful acquisition/reward/requisition/value-flow event must route at least one delta to a recognized owner or explicitly produce a no-delta, quarantine, escalation, transition, source-local, `pending_schema`, `human_review`, or `defer_until_schema_exists` result. B05 does not own every delta format and does not create runtime event/state schemas.

## 19. Owner-file handoff rules

B05 handoff rules are:
- B01 owns scene/activity/encounter containers, transitions, and checkpoint routing that generated the value pressure.
- B02 owns action declaration, feasibility, cost commitment, resolution trigger, no-roll/roll-trigger, and action-to-delta procedure that generated or consumed value pressure.
- B03 owns item/gear/equipment/object-system construct, object readiness, object state, object use, object damage, material/function questions, object work, and asset-use routing.
- B04 owns inventory, storage, custody, possession, access, quick-access, burden, concealment, lawful loss, recovery, and inventory/custody routing.
- B05 owns acquisition, reward, loot, salvage, requisition, exchange, market access, availability, scarcity, value conversion routing, upkeep, consumption, economic pressure, and value-sink routing.
- C00 owns the shared schema handoff control surface and missing-schema fallback language.
- Future C01-C14 schema families may receive conversion handoffs but B05 must not invent their fields.
- World/faction/law/institution owners receive license, permit, claim, legal status, tax, tribute, restricted goods, requisition authority, market disruption, and faction-standing pressure.
- Project/crafting owners receive work plans, crafting output, salvage processing, repair work, modification, upgrade, resource-gathering, and facility/toolchain pressure.
- Advancement/power/canon owners receive reward-as-power, progression pacing, cultivation-resource escalation, accepted lexicon, canon eligibility, and sourcebook promotion pressure.
- Runtime/training owners receive later validation tasks only; B05 is not runtime authority and not live-play behavior.

If the correct owner is unknown, B05 must mark `pending_schema`, `source_local_review`, `schema_review`, `human_review`, `quarantined_unresolved_delta`, or `owner_file_escalation` rather than inventing ownership.

## 20. Batch B to C00/C-family handoff rules

Batch B procedure may identify that a C-family handoff is needed, but it must not invent C-family fields. B05 uses C00 as the schema handoff control surface when acquisition/value/economy handling produces conversion records, record-shape pressure, source-local evidence, rejected donor elements, canon eligibility questions, provenance needs, or missing-schema gaps.

The following lightweight doctrine-facing block may be used for B05-to-C00/C-family handoff notes. It is not a runtime schema, not a backend contract, not C-family schema content, not a context packet format, not a database row, not player-facing rule text, and not sourcebook prose.

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

value_flow_routing_note:
  value_flow_state: acquisition_declared | acquisition_confirmed | acquisition_blocked | reward_offered | reward_claimed | reward_disputed | loot_identified | salvage_identified | claim_pending | claim_disputed | requisition_requested | requisition_approved | requisition_denied | exchange_available | exchange_blocked | market_access_confirmed | market_access_blocked | scarcity_identified | value_conversion_needed | upkeep_due | value_sink_triggered | owner_handoff_required | source_local_value_procedure | value_flow_quarantined_gap
  actor_ref: string | null
  object_or_value_ref: string | null
  value_form: currency | barter_good | service | favor | obligation | claim | license | permit | ration | requisition_credit | faction_scrip | reputation_access | material_component | strategic_resource | consumable_supply | salvage | loot | reward_right | information_value | labor | shelter | transport | protection | legal_status | access_right | source_local_value | unknown_value
  acquisition_channel: purchase | sale | barter | trade | gift | reward | loot | salvage | claim | requisition | rationing | license_access | permit_access | faction_grant | institutional_grant | market_exchange | black_market_exchange | auction | tax_collection | tribute | tithe | fee | toll | lease | debt | labor_exchange | crafting_output | project_output | exploration_find | encounter_spoils | legal_seizure | theft_or_illicit_gain | source_local_acquisition | unknown_acquisition
  scarcity_state: abundant | available | limited | rationed | restricted | licensed | illegal | controlled | faction_locked | location_locked | time_limited | disrupted | depleted | unstable | contested | hidden | black_market_only | source_local_scarcity | unknown_scarcity
  ownership_or_claim_status: none | possession_only | ownership_confirmed | ownership_disputed | custody_confirmed | custody_disputed | lawful_claim_pending | unlawful_claim | faction_claim | source_local_claim | unknown
  market_access_status: not_applicable | available | unavailable | restricted | licensed | illegal | black_market_only | faction_locked | location_locked | disrupted | unknown
  requisition_status: not_applicable | requested | approved | denied | delayed | conditional | rationed | exhausted | authority_required | source_local_requisition | unknown
  value_flow_outcome: no_delta_required | value_obtained | value_spent | value_committed | value_reserved | value_lost | value_disputed | value_transferred | value_restricted | value_deferred | value_converted_to_claim | value_converted_to_obligation | value_converted_to_access | value_converted_to_unresolved_pressure | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  owner_handoff_required: boolean
  owner_handoff_reason:
    - inventory_custody
    - object_state
    - economy_value
    - market_access
    - scarcity_availability
    - reward_claim
    - loot_salvage
    - requisition_authority
    - upkeep_consumption
    - value_sink
    - world_law_faction
    - project_crafting
    - advancement_review
    - canon_lexicon
    - runtime_review
    - schema_review
    - source_local_review
    - human_review
  delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  note: string
```

Supporting rules:
- `target_schema_family: pending_schema` is allowed only when no C-family owner is stable enough; it is not a license to invent family-specific fields.
- `schema_status` reports the receiving family posture; B05 must not promote registry status.
- `source_evidence_refs_required`, `construct_refs_required`, `outcome_refs_required`, and `provenance_refs_required` preserve traceability.
- `source_local_boundary_required_if_applicable` and `rejected_donor_elements_required_if_applicable` prevent donor economy import by accident.
- `review_routing_required` means unresolved value, economy, market, law, reward, requisition, and schema questions must route to owners.

## 21. Missing-schema fallback and quarantine/escalation

When B05 lacks schema coverage, owner coverage, or safe doctrine vocabulary, it must use one of the following instead of improvising schema:
- `pending_schema`
- quarantine
- escalation
- `human_review`
- `defer_until_schema_exists`
- `source_local_review`
- `schema_review`
- `quarantined_unresolved_delta`
- `owner_file_escalation`
- `unknown_value`
- `unknown_acquisition`
- `unknown_scarcity`

Quarantine is required when:
- donor value systems would become Astra defaults if normalized;
- donor prices, currencies, reward tables, loot tables, treasure tables, requisition ratings, rarity tiers, wealth pacing, or market lists are being imported;
- ownership, legality, custody, possession, access, or burden cannot be separated;
- value conversion would require invented formula, exchange rate, economy schema, or C-family field;
- market access, black-market access, license, permit, taxation, salvage rights, rationing, or requisition authority lacks a valid owner;
- source evidence is missing or provenance is unclear;
- live-play/runtime state would be inferred from doctrine-facing examples.

Escalation or `human_review` is required when unresolved value flow affects canon eligibility, legal/IP risk, accepted lexicon, player-facing rules, final mechanics, campaign persistence, runtime state, or cross-owner conflicts.

## 22. Source-local donor economy/reward/requisition handling

Source-local donor economy, reward, requisition, value, market, scarcity, and sink systems may be retained as source evidence or local procedure only. They must not become Astra defaults through B05.

Source-local handling ladder:
1. Preserve the source evidence and provenance.
2. Identify the functional role: value form, acquisition channel, scarcity state, reward entry, loot entry, salvage claim, requisition channel, market access, value sink, upkeep, consumption, burden, legal status, faction standing, or conversion pressure.
3. Map only to B05 doctrine vocabulary when safe.
4. Mark donor terms, exact math, exact tables, exact prices, exact currencies, exact reward pacing, exact requisition ratings, exact rarity tiers, exact loot tables, exact treasure parcels, exact market lists, exact cultivation grades, exact post-scarcity fabrication rules, and exact black-market procedures as source-local or rejected donor elements.
5. Route unsafe material to quarantine, escalation, `human_review`, or `defer_until_schema_exists`.
6. Retain source-local effects only when their boundary remains explicit and they do not imply canon, runtime, or final mechanics.

Examples of source-local constructs requiring boundary controls include city price lists, fantasy coins, treasure parcel tables, donor wealth-by-level assumptions, sect contribution exchanges, cultivation-resource grades, favor currencies, auction-house procedures, cyberpunk restricted gear access, military requisition ratings, black-market procedures, vehicle fuel economies, ship maintenance cycles, local salvage-rights law, post-scarcity fabrication policies, rationing systems, tax law, crafting economies, and donor economy prose.

## 23. Runtime boundary

B05 is not runtime authority. It must not define or imply runtime economy state, runtime inventory ledger, event-sourced value ledger, entity/component/event/state schemas, persistent campaign state, backend contracts, database rows, command lifecycle implementation, context packet compiler, hidden-information runtime state, or live GM adapter behavior.

B05 may identify that a runtime review is needed, but runtime owners must validate any later runtime behavior, persistence, event format, hidden information, or context-packet behavior. Live-play behavior must not consume B05 procedure as runtime authority without later runtime validation.

## 24. Canon boundary

B05 is not canon promotion authority. It must not promote currencies, value forms, acquisition channels, markets, shop lists, scarcity states, black-market procedures, legal codes, taxation law, salvage rights, ownership rules, requisition systems, reward pacing, loot tables, treasure tables, cultivation resources, sect contribution, faction scrip, post-scarcity economies, donor terms, accepted lexicon, sourcebook prose, or source-local systems to accepted canon.

B05 may identify canon eligibility questions, canon review needs, rejected donor elements, source-local boundaries, and provenance requirements for later owners. Canon acceptance must remain with canon owners and C00/C-family review surfaces where applicable.

## 25. Live-play/training boundary

B05 is not live-play narration behavior, player-facing rule text, a training script, or a GM adapter. It must not tell live play how to narrate a shop, market, reward, loot drop, salvage scene, requisition request, scarcity event, or value sink.

Training or live-play systems may later consume owner-validated outputs, but B05 procedure itself remains doctrine-facing and must not be treated as runtime or player-facing authority.

## 26. Examples of good and bad B05 usage

Good B05 usage:
- A party finds equipment after a structured encounter. B05 marks `loot_identified`, classifies the value form as `loot` or `material_component`, classifies the channel as `encounter_spoils`, separates custody from ownership, routes possession/burden to B04, routes object identity and damage to B03, and routes disputed claims or legality to world/faction/law owners without creating a loot table.
- A crew tries to buy restricted medicine during a blockade. B05 marks `market_access_blocked` or `scarcity_identified`, classifies the value form as `consumable_supply`, the channel as `market_exchange` or `license_access`, the scarcity state as `restricted` or `disrupted`, and routes license, permit, rationing, and market-disruption pressure to world/faction/law owners without defining final prices or shop lists.
- A faction quartermaster issues a vehicle part for a mission. B05 marks `requisition_requested` then `requisition_approved` or `requisition_denied`, classifies the channel as `requisition` or `institutional_grant`, routes custody/burden to B04, object state to B03, authority/audit/return conditions to faction/institution owners, and avoids treating requisition as free ownership.
- A salvage team strips components from a wreck. B05 marks `salvage_identified`, classifies recovered pieces as `salvage` or `material_component`, routes object-state and contamination questions to B03, custody/burden to B04, salvage claims and legal exposure to world/faction/law owners, and avoids converting salvage into automatic wealth.
- A donor source uses sect contribution points or cyberpunk street cred. B05 classifies the value as `source_local_value`, possibly `reputation_access` or `faction_scrip` if safe, records source-local boundary and rejected donor elements, and quarantines conversion math rather than promoting the donor system.

Bad B05 usage:
- Defining a universal currency, final price list, final shop list, final market table, final reward table, final loot table, final treasure table, wealth-by-level rule, or final value conversion formula.
- Treating money as the default value, price as access, availability as ownership, possession as ownership, ownership as legality, rarity as final value, reward as automatic power, requisition as free gear, loot as lawful property, or salvage as free wealth.
- Creating a runtime economy database row, event-sourced value ledger, runtime inventory ledger, command object, backend contract, context packet format, hidden-information state, or live-play shop narration script.
- Promoting donor cultivation resources, sect contribution, favor currencies, fantasy coins, cyberpunk restricted gear, treasure parcels, requisition ratings, black-market procedures, salvage law, tax law, rationing systems, market lists, or sourcebook economy prose to Astra defaults.
- Inventing C-family fields, final inventory schema, final object schema, ownership database, final faction law, final legal code, final scarcity algorithm, final availability algorithm, final black-market procedure, or final upkeep formula.

## 27. Minimum tests or assertions

Minimum B05 tests or assertions should verify that:
- B05 exists at `docs/doctrine/operations/batch_b/B05_acquisition_reward_requisition_and_value_flow_procedure.md`;
- all required B05 sections are present;
- B05 declares ownership and non-ownership;
- B05 references B01, B02, B03, and B04 as upstream Batch B context;
- B05 includes C00 handoff language and `batch_b_to_c_handoff`;
- B05 includes `value_flow_routing_note` and marks it as doctrine-facing only;
- B05 includes value forms, acquisition channels, scarcity states, value-flow states, and value-flow outcomes;
- B05 separates value, acquisition channel, market access, availability, scarcity, possession, custody, ownership, legality, burden, and value conversion;
- B05 includes acquisition/value-flow intake procedure;
- B05 includes market access, availability, scarcity, and restricted-access procedure;
- B05 includes exchange, barter, purchase, sale, trade, favor, obligation, and claim routing;
- B05 includes reward, loot, salvage, and claim-entry procedure;
- B05 includes requisition, rationing, license, permit, authority, and institutional access procedure;
- B05 includes upkeep, consumption, maintenance cost, value sink, and economic pressure routing;
- B05 includes value conversion and abstraction as routing, not math;
- B05 routes inventory/custody/burden questions to B04 and object-state questions to B03/object owners;
- B05 routes world, faction, institution, law, and market-disruption pressure to proper owners;
- B05 includes value-flow state-delta routing and owner-file handoff rules;
- B05 rejects final economy schema, final inventory schema, final object schema, C-family field invention, C01-C14 schema-content ownership, final currency math, final price lists, final shop lists, final market tables, final reward tables, final loot tables, final treasure tables, final wealth-by-level math, final requisition rating system, final rationing system, final taxation law, final legal code, final faction law, final ownership database, final rarity/tier economy, final conversion formulas, final scarcity algorithms, final availability algorithms, final black-market procedure, final salvage-rights law, final upkeep/maintenance/consumption formulas, final crafting/salvage/repair/modification procedure, final advancement/reward pacing, final cultivation-resource economy, final post-scarcity economy, runtime economy state, runtime inventory ledger, runtime schemas, persistent campaign state, command lifecycle implementation, context packet compiler, hidden-information runtime state, live-play behavior, canon promotion, accepted lexicon, and sourcebook prose;
- B05 rejects donor economy/reward/requisition systems as Astra defaults;
- B05 includes missing-schema fallback, quarantine, escalation, `human_review`, and `defer_until_schema_exists`;
- B05 references D00/D09/D10/D15/D16/D17/D19 only as draft source-pack/reference material, not final current doctrine authority;
- B05 does not create B06-B11;
- B05 does not require, define, create, or promote C01-C14;
- no registry status is promoted to current.

## 28. Acceptance criteria

B05 is acceptable when it:
- stays focused on acquisition, reward, loot, salvage, requisition, exchange, market access, availability, scarcity, value conversion routing, upkeep, consumption, economic pressure, and value sinks;
- builds on B01, B02, B03, and B04 without rewriting them;
- keeps money, value, price, access, availability, possession, custody, ownership, legality, rarity, loot, salvage, reward, requisition, markets, black markets, scarcity, and post-scarcity constraints separate;
- provides value-form, acquisition-channel, scarcity-state, value-flow-state, and value-flow-outcome vocabulary as doctrine vocabulary only;
- includes acquisition/value-flow intake, exchange routing, market access/availability/scarcity procedure, reward/loot/salvage/claim-entry procedure, requisition procedure, upkeep/consumption/sink routing, value conversion/abstraction routing, owner-file handoff, C00/C-family handoff, missing-schema fallback, quarantine, escalation, `human_review`, and `defer_until_schema_exists`;
- rejects final economy schema, final inventory schema, final object schema, C-family schema fields, C01-C14 schema contents, final currency math, final prices, final shop lists, final market tables, final reward/loot/treasure tables, wealth-by-level math, requisition ratings, rationing systems, taxation law, legal code, faction law, ownership database, rarity/tier economy, conversion formulas, scarcity/availability algorithms, black-market procedure, salvage-rights law, upkeep/maintenance/consumption formulas, crafting/salvage/repair/modification procedure, reward pacing, cultivation-resource economy, post-scarcity economy, runtime economy state, runtime inventory ledger, runtime schemas, persistent campaign state, command lifecycle implementation, context packet compiler, hidden-information runtime state, live-play behavior, canon promotion, accepted lexicon, sourcebook prose, and donor systems as Astra defaults;
- treats D00/D09/D10/D15/D16/D17/D19 source material and donor economy/reward/requisition/value systems as draft reference/evidence only;
- does not require, define, create, or promote B06-B11;
- does not require, define, create, or promote C01-C14;
- leaves registry status unpromoted unless a separate repo convention requires draft/not-current tracking.

## 29. Follow-up handoff to B06

B05's follow-up handoff to B06 is limited to noting unresolved downstream procedure pressure that may need a later Batch B file. B05 does not create B06-B11, does not define B06-B11 content, does not require B06-B11, does not promote B06-B11, and does not make B06-B11 current doctrine. Any later B06 work must inherit B01-B05 boundaries rather than using B05 to define final mechanics, schema fields, runtime state, canon, sourcebook prose, or donor systems as Astra defaults.

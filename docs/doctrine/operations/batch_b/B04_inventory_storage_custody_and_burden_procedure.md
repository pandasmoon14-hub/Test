# B04 Inventory, Storage, Custody, and Burden Procedure

## 1. Purpose and status

B04 is the fourth Batch B operational doctrine draft for Astra inventory, storage, custody, possession, access, quick-access, burden, concealment, legal visibility, transfer, loss, and recovery handling. It sits after B01 scene/activity/encounter procedure, B02 action declaration/cost commitment/resolution trigger procedure, and B03 item/gear/equipment/object-system construct and asset-use procedure. B04 builds on B03 object-use procedure without reopening final item stats, object schemas, equipment math, sourcebook gear lists, runtime inventory state, or final economy law.

Status posture:
- This file is Batch B operational-procedure draft material.
- This file is not current canon, not final mechanics, not runtime authority, not sourcebook prose, and not player-facing rule text.
- C00 remains the schema handoff control surface for Batch B to C-family routing.
- B04 treats `B01_scene_encounter_and_activity_procedure.md`, `B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md`, and `B03_item_gear_equipment_and_asset_use_procedure.md` as upstream Batch B context and must build on them, not rewrite them.
- D00, D09, D17, and D19 source-pack files are referenced only as draft source-pack/reference material. They are not current doctrine authority, final mechanics, runtime authority, canon, or sourcebook prose.
- B04 records, examples, and handoff blocks are doctrine-facing only; they are not runtime state, backend contracts, sourcebook statblocks, canon entries, player-facing rule text, or final mechanics.

Required reference boundaries preserved by B04:
- `docs/doctrine/operations/batch_b/B01_scene_encounter_and_activity_procedure.md` for upstream Batch B scene, activity, encounter, transition, checkpoint, and owner-file handoff procedure.
- `docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md` for upstream Batch B action declaration, feasibility, cost commitment, no-roll/roll-trigger, and action-to-delta routing procedure.
- `docs/doctrine/operations/batch_b/B03_item_gear_equipment_and_asset_use_procedure.md` for upstream Batch B object-use, object readiness, object custody triage, inventory/storage handoff, and object-use delta routing procedure.
- `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` for shared Batch C base fields, `pending_schema`, source-local boundary, rejected donor element, canon eligibility, review routing, provenance, and missing-schema fallback language.
- `docs/doctrine/native_design/d_series/source_packs/astra_d00_doctrine_pack_v0_1/D00-03_state_delta_commit_protocol.md` for the draft source-pack principle that every meaningful action commits at least one delta to a recognized owner, while B04 does not own every delta format.
- `docs/doctrine/native_design/d_series/source_packs/astra_d09_doctrine_pack_v0_1/D09-00_layered_object_state_architecture.md` and `docs/doctrine/native_design/d_series/source_packs/astra_d09_doctrine_pack_v0_1/D09-02_weapons_armor_tools_foci_consumables_and_materials.md` for draft source-pack object-state, container, vehicle/platform, and functional object-family source material, while B04 must not promote D09 object records to final schema.
- `docs/doctrine/native_design/d_series/source_packs/D17_economy_acquisition_inventory_reward_and_requisition_doctrine_pack/D17_doctrine_pack/D17-04_inventory_storage_carrying_custody_quick_access_and_burden_procedure.md` for draft source-pack inventory, storage, carrying, custody, quick-access, access-state, burden, loss, recovery, requisition, and economy pressure, while B04 must not define final capacity, encumbrance, price, currency, legal code, or economy law.
- `docs/doctrine/native_design/d_series/source_packs/D19_cross_pack_integration_conflict_audit_and_conversion_readiness_capstone_pack/D19_capstone_doctrine_pack/D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md` for draft source-pack record-shape governance warnings and not-final-schema controls.

## 2. Owner layer

B04 belongs to Batch B operational doctrine. It routes inventory, storage, custody, possession, access, quick-access, burden, concealment, legal visibility, transfer, loss, and recovery procedure between upstream B01/B02/B03 procedure, the A-family doctrine layer, the C00 schema handoff control surface, future C01-C14 schema families, source-local donor inventory/storage/economy quarantine, and later object, economy, law/faction, travel/vehicle, project, world, canon, runtime, and training owners.

B04 may identify that a handoff is needed to a likely owner, but it must not perform that owner's work. When B04 cannot identify a valid owner or schema family, it must mark `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` instead of inventing Astra schema, mechanics, runtime state, backend ledger, ownership database, legal code, economy law, canon, or sourcebook inventory rules.

## 3. What B04 owns

B04 owns doctrine-level operational procedure for:
- inventory/possession intake procedure after B03 object-use or acquisition/transfer/loss pressure;
- possession, access, ownership, custody, legal visibility, readiness, storage, quick-access, and burden separation;
- holding-mode classification;
- burden-type classification;
- access-state classification;
- possession-scope classification;
- storage/container/cache/vault/vehicle/platform/facility procedure routing;
- concealment/security/audit-trail/trace/inspection procedure routing;
- transfer, handoff, requisition, impoundment, escrow, shared ownership, shared-possession, and faction custody procedure routing;
- quick-access and retrieval-delay procedure routing;
- burden/transport/support-pressure routing;
- decay, spoilage, maintenance, upkeep, stability, trace, and loss-risk routing;
- lawful inventory-loss trigger procedure;
- recovery/retrieval procedure routing;
- inventory/custody/burden state-delta routing to recognized owner files;
- B04-to-C00/C-family handoff references when inventory/custody/burden handling produces conversion records;
- source-local donor inventory/storage/currency/slot/container/bag-of-holding/cyberdeck/loadout/cargo/requisition systems quarantine and escalation rules;
- examples of good and bad B04 usage;
- minimum tests or assertions and acceptance criteria for B04.

## 4. What B04 must not own

B04 must not define or promote:
- final inventory schema;
- final object schema;
- C-family schema fields;
- C01-C14 schema contents;
- final item stats;
- final equipment stats;
- final carrying-capacity math;
- final inventory capacity math;
- final weight/slot/encumbrance rules;
- final cargo-capacity math;
- final container-capacity math;
- final quick-access action economy;
- final inventory UI/backend model;
- final runtime inventory state;
- final event-sourced inventory ledger;
- final ownership database;
- final currency math;
- final price, market, reward, treasure, requisition, or economy law;
- final legal code, faction law, licensing, tax, contraband, or confiscation rules;
- final crafting, repair, maintenance, spoilage, decay, or aging math;
- final loss/recovery tables;
- final vehicle/platform cargo statblocks;
- final spatial storage, magic bag, pocket dimension, pattern storage, or post-scarcity storage rules;
- runtime entity/component/event/state schemas;
- runtime state/event/command lifecycle ownership;
- persistent campaign state;
- command lifecycle implementation;
- context packet compiler;
- hidden-information runtime state;
- live-play narration behavior;
- final canon promotion;
- accepted lexicon terms;
- sourcebook prose;
- donor inventory/equipment/economy systems as Astra defaults.

## 5. Non-collapse rule

B04 enforces these non-collapse principles:
- Possessed does not mean accessible.
- Accessible does not mean owned.
- Owned does not mean legal to carry.
- Stored does not mean safe.
- Safe does not mean immediately available.
- Quick access is not general capacity.
- Quick access does not decide final action timing.
- Containers do not erase burden unless an owner file or source-local rule supports it.
- Hidden storage does not erase trace, search risk, legal risk, faction claim, custody dispute, decay, maintenance, or retrieval delay.
- Shared possession must state who can access, sell, spend, abandon, divide, bear burden, receive trace, or accept responsibility.
- Inventory loss requires a lawful trigger and owner-file support.

B04 may identify inventory/custody/burden pressure, but it must not define final capacity, economy, price, legal code, runtime inventory state, or backend ledger. B04 may route object-state questions to B03/object owners, but must not define final object schema or item stats. Every meaningful inventory/custody/burden event must route at least one delta to a recognized owner or explicitly produce a no-delta/quarantine/escalation/transition result.

## 6. Inventory, possession, custody, access, and burden definitions

For B04 doctrine vocabulary only:
- `inventory` means the doctrine-facing set of objects, values, documents, supplies, cargo, digital assets, pattern assets, or source-local holdings associated with an actor, party, vehicle, platform, facility, faction, escrow, or domain.
- `possession` means an actor, party, crew, vehicle/platform, facility, faction, or escrow currently controls or is treated as holding an object or value, whether or not ownership is settled.
- `access` means the object or value can be reached or used under a stated access state; possession does not imply access.
- `quick_access` means an item is marked for faster retrieval than ordinary packed/storage retrieval, but quick access is not general capacity and quick access does not decide final action timing.
- `ownership` means a doctrine-facing claim about who may sell, spend, transfer, abandon, divide, pledge, or bear responsibility for an object or value; accessible does not mean owned.
- `custody` means the doctrine-facing right, duty, or factual control over holding, guarding, transporting, inspecting, impounding, escrowing, or returning an object or value.
- `legal_visibility` means possession, carry, storage, concealment, transfer, or use may be visible to law, faction, license, tax, contraband, inspection, audit, or claim procedure; owned does not mean legal to carry.
- `burden` means any carrying, capacity, support, security, concealment, legal, social, faction, maintenance, decay, power, crew, platform, access-delay, or retrieval-risk pressure created by inventory or storage.

These terms are B04 doctrine vocabulary only. They are not final schema fields, accepted lexicon terms, runtime inventory state, sourcebook rule text, database contracts, or final mechanics.

## 7. Inventory/possession intake procedure

Inventory/possession intake begins when upstream procedure produces acquisition, transfer, loss pressure, storage pressure, burden pressure, inspection pressure, custody pressure, or B03 object-use/storage/retrieval handoff. B04 intake must:
1. identify the actor, party, crew, faction, vehicle/platform, facility, domain, escrow, or source-local scope claiming possession or custody;
2. identify the object or value reference without defining final item stats, final equipment stats, final object schema, final inventory schema, or final economy value;
3. classify holding mode, access state, possession scope, and burden types;
4. separate possession, access, ownership, legal permission, readiness, storage, quick access, custody, and burden before any routing decision;
5. check whether the event is no-delta housekeeping, owner-routed, a transition note, source-local retained effect, quarantined unresolved delta, or owner-file escalation;
6. route object-state questions back to B03/object owners and route economy/legal/world/project/runtime/schema questions to their later owner files;
7. if schema coverage is missing, produce `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` rather than improvised schema.

## 8. Holding-mode classification

B04 recognizes these holding modes as doctrine vocabulary:
```text
carried_on_person, equipped, worn, quick_access, packed, container_stored, vehicle_stored, platform_stored, facility_stored, banked, vaulted, cached, hidden, escrowed, faction_held, requisition_held, impounded, leased_storage, digital_or_pattern_stored, bound_to_actor, source_local_holding, unknown
```

Holding mode classification asks where the object/value is located and under what kind of holding relationship. A holding mode does not by itself establish access, ownership, legality, safety, capacity relief, burden relief, quick-access timing, or runtime state.

## 9. Access-state and quick-access procedure

B04 recognizes these access states as doctrine vocabulary:
```text
immediate_access, quick_access, scene_access, interval_access, safe_location_access, facility_access, vehicle_or_platform_access, faction_permission_access, licensed_access, locked_access, hidden_cache_access, delayed_access, blocked_access, source_local_access, unknown_access
```

Access-state procedure must:
- state whether the object or value can be reached now, within the scene, after an interval, only at a safe location, only at a facility, only through a vehicle/platform, only with faction permission, only with a license, only after unlocking, only from a hidden cache, only after delay, or not at all;
- distinguish access from possession, ownership, legal permission, readiness, storage, quick access, custody, and burden;
- treat quick access as a retrieval/access classification, not as general capacity, final quick-access action economy, final inventory capacity math, or final action timing;
- route readiness or use questions to B03/object owners and route final action timing to the later action/cadence owner instead of deciding it here.

## 10. Possession, ownership, custody, and legal visibility procedure

B04 must record whether possession is declared, confirmed, disputed, shared, escrowed, impounded, faction-held, requisition-held, or source-local. It must then identify whether ownership, custody, legal permission, and legal visibility are resolved, disputed, blocked, or owner-handoff-required.

Procedure rules:
- Possessed does not mean accessible.
- Accessible does not mean owned.
- Owned does not mean legal to carry.
- Legal permission does not prove immediate access, safety, or readiness.
- Custody may create duties, search risk, audit trail, faction trace, legal visibility, storage security pressure, or loss/recovery obligations without creating ownership.
- Legal visibility may require world_law_faction owner routing, but B04 must not define final legal code, faction law, licensing, tax, contraband, confiscation rules, or final economy law.

## 11. Burden-type classification and transport/support pressure

B04 recognizes these burden types as doctrine vocabulary:
```text
weight, bulk, volume, slot, quick_access_limit, container_capacity, transport_capacity, storage_capacity, security_burden, concealment_burden, legal_visibility, social_visibility, faction_trace, custody_risk, maintenance_burden, decay_or_spoilage, fuel_or_power_support, crew_or_labor_support, platform_cargo_burden, access_delay, retrieval_risk, source_local_burden
```

Burden-type classification identifies pressure without defining final carrying-capacity math; B04 must not define final carrying-capacity math, final weight/slot/encumbrance rules, final cargo-capacity math, final container-capacity math, final currency math, final price law, or final support math. Burden/transport/support pressure may route to object owners, economy owners, world/law/faction owners, travel/vehicle/platform owners, project owners, or `pending_schema`.

## 12. Storage, container, cache, vault, vehicle, platform, and facility procedure

Storage procedure applies to container_stored, vehicle_stored, platform_stored, facility_stored, banked, vaulted, cached, hidden, escrowed, leased_storage, digital_or_pattern_stored, and source_local_holding. B04 must ask:
- what is stored and where, without defining final storage schema or final inventory backend model;
- who can access, retrieve, inspect, secure, transfer, sell, abandon, divide, or bear burden;
- whether the storage creates access delay, retrieval risk, storage fees, legal visibility, social visibility, faction trace, audit trail, concealment burden, custody dispute, preservation benefit, decay pressure, maintenance burden, or source-local retained effect;
- whether a container, vault, cache, vehicle, platform, facility, magic bag, pocket dimension, pattern store, spatial ring, bank, cyberdeck, cargo bay, or post-scarcity storage rule is source-local donor evidence only, owner-file-supported, or quarantined.

Containers do not erase burden unless an owner file or source-local rule supports it. Stored does not mean safe. Safe does not mean immediately available.

## 13. Concealment, security, audit trail, trace, and inspection procedure

Concealment and security procedure identifies whether an object/value is hidden, locked, guarded, audited, traceable, inspectable, licensed, flagged, bonded, taxed, impounded, or source-local. Hidden storage does not erase trace, search risk, legal risk, faction claim, custody dispute, decay, maintenance, or retrieval delay.

B04 routes concealment, security, audit trail, trace, and inspection pressure as follows:
- object condition, lock, container, tool, sensor, or physical state questions route to B03/object owners;
- legal inspection, license, tax, contraband, faction claim, confiscation, and impoundment questions route to world_law_faction owners or `pending_schema`;
- audit-trail, trace, hidden-information, runtime visibility, and backend ledger questions route to runtime/schema review rather than B04 runtime ownership;
- unresolved source-local concealment/security systems route to quarantine, escalation, `human_review`, or `defer_until_schema_exists`.

## 14. Transfer, handoff, requisition, escrow, impoundment, and shared-possession procedure

Transfer procedure applies when an object or value is handed off, sold, gifted, loaned, requisitioned, escrowed, impounded, confiscated, faction-held, party-shared, crew-shared, vehicle/platform-held, facility-held, or source-local. B04 recognizes these possession scopes as doctrine vocabulary:
```text
individual, party_shared, crew_shared, faction_shared, vehicle_or_platform, facility, domain, escrow, source_local_scope
```

Shared possession must state who can access, sell, spend, abandon, divide, bear burden, receive trace, or accept responsibility. A transfer note must separate custody, ownership, access, legal permission, quick access, storage, burden, trace, and loss/recovery responsibility. Requisition and economy pressure may be identified, but B04 must not define final requisition systems, final currency math, final price/market/reward/treasure/economy law, or final ownership database.

## 15. Decay, spoilage, maintenance, upkeep, and stability routing

B04 identifies decay, spoilage, maintenance, upkeep, contamination, expiration, instability, storage preservation, fuel/power support, crew/labor support, platform cargo support, and value deterioration pressure. It must route:
- object condition, damage, degradation, repair, or maintenance questions to B03/object owners or later object-maintenance owners;
- food, material, medicine, biological, magical, digital, pattern, or source-local spoilage pressure to owner files or source-local retained effect;
- final crafting, repair, maintenance, spoilage, decay, aging math, and final loss/recovery tables away from B04;
- unresolved stability gaps to `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists`.

## 16. Inventory loss trigger procedure

Inventory loss requires a lawful trigger and owner-file support. B04 recognizes these loss triggers as doctrine vocabulary:
```text
none, overburden, flight, defeat, confiscation, tax_seizure, faction_claim, legal_inspection, theft, container_damage, platform_destruction, hazard_exposure, decay, spoilage, abandonment, failed_transport, source_local_trigger
```

A loss trigger procedure must identify the trigger, the owner file authorizing it, the affected object/value, the possession scope, the custody/ownership/legal visibility status, the burden or storage condition, and the proposed loss outcome. B04 must not invent loss/recovery tables, confiscation law, theft mechanics, defeat looting rules, or final runtime state changes.

B04 recognizes these loss outcomes as doctrine vocabulary:
```text
none, lost, damaged, impounded, stolen, abandoned, claimed_by_other, converted_to_unresolved_pressure, recoverable, recoverable_with_cost, recoverable_with_project, recoverable_with_operation, destroyed, quarantined, source_local_result
```

## 17. Recovery and retrieval procedure

Recovery and retrieval procedure applies when an object/value is recoverable, recoverable_with_cost, recoverable_with_project, recoverable_with_operation, delayed_access, hidden_cache_access, facility_access, vehicle_or_platform_access, faction_permission_access, licensed_access, locked_access, blocked_access, impounded, escrowed, or source-local. B04 must:
- distinguish recovery from immediate retrieval, quick access, ownership, legality, safety, and final action timing;
- identify whether recovery is no_delta_required, owner_routed, a transition_note, source_local_retained_effect, quarantined_unresolved_delta, or owner_file_escalation;
- route project-scale recovery to project owners, travel/vehicle recovery to travel/platform owners, legal/faction recovery to world_law_faction owners, object-state recovery to B03/object owners, and missing schema recovery to `pending_schema`.

## 18. Inventory/custody/burden state-delta routing

Every meaningful inventory/custody/burden event must route at least one delta to a recognized owner or explicitly produce a no-delta/quarantine/escalation/transition result. B04 recognizes these delta routing statuses: `no_delta_required`, `owner_routed`, `transition_note`, `source_local_retained_effect`, `quarantined_unresolved_delta`, and `owner_file_escalation`.

The following B04-specific lightweight doctrine-facing block may be used as an audit note for conversion discussion. It is not a runtime schema, not a backend event, not a command object, not a C-family record, not an inventory database row, not an item statblock, not a sourcebook statblock, not final mechanics, not a database contract, not an event log, not a context packet format, not persistent campaign state, not canon, and not player-facing rule text.

```yaml
inventory_custody_routing_note:
  inventory_state: possession_declared | possession_confirmed | possession_disputed | access_confirmed | access_blocked | quick_access_confirmed | storage_confirmed | custody_confirmed | custody_disputed | burden_identified | loss_triggered | recovery_available | owner_handoff_required | source_local_inventory_procedure | inventory_quarantined_gap
  actor_ref: string | null
  object_or_value_ref: string | null
  holding_mode: carried_on_person | equipped | worn | quick_access | packed | container_stored | vehicle_stored | platform_stored | facility_stored | banked | vaulted | cached | hidden | escrowed | faction_held | requisition_held | impounded | leased_storage | digital_or_pattern_stored | bound_to_actor | source_local_holding | unknown
  access_state: immediate_access | quick_access | scene_access | interval_access | safe_location_access | facility_access | vehicle_or_platform_access | faction_permission_access | licensed_access | locked_access | hidden_cache_access | delayed_access | blocked_access | source_local_access | unknown_access
  possession_scope: individual | party_shared | crew_shared | faction_shared | vehicle_or_platform | facility | domain | escrow | source_local_scope
  burden_types:
    - weight
    - bulk
    - volume
    - slot
    - quick_access_limit
    - container_capacity
    - transport_capacity
    - storage_capacity
    - security_burden
    - concealment_burden
    - legal_visibility
    - social_visibility
    - faction_trace
    - custody_risk
    - maintenance_burden
    - decay_or_spoilage
    - fuel_or_power_support
    - crew_or_labor_support
    - platform_cargo_burden
    - access_delay
    - retrieval_risk
    - source_local_burden
  loss_trigger: none | overburden | flight | defeat | confiscation | tax_seizure | faction_claim | legal_inspection | theft | container_damage | platform_destruction | hazard_exposure | decay | spoilage | abandonment | failed_transport | source_local_trigger
  loss_outcome: none | lost | damaged | impounded | stolen | abandoned | claimed_by_other | converted_to_unresolved_pressure | recoverable | recoverable_with_cost | recoverable_with_project | recoverable_with_operation | destroyed | quarantined | source_local_result
  owner_handoff_required: boolean
  owner_handoff_reason:
    - object_state
    - inventory_access
    - custody_ownership
    - burden_capacity
    - economy_value
    - world_law_faction
    - storage_security
    - concealment_trace
    - decay_maintenance
    - loss_recovery
    - canon_lexicon
    - runtime_review
    - schema_review
    - source_local_review
    - human_review
  delta_routing_status: no_delta_required | owner_routed | transition_note | source_local_retained_effect | quarantined_unresolved_delta | owner_file_escalation
  note: string
```

## 19. Owner-file handoff rules

B04 owner-file handoff rules:
- object_state handoff goes to B03/object owners when inventory handling asks what the object is, whether it is damaged, whether a container can hold something, whether a tool can open storage, or whether an item is ready for use;
- inventory_access handoff goes to later inventory/economy schema owners when access state needs durable conversion treatment;
- custody_ownership handoff goes to later economy, legal, faction, or ownership owners and never creates a final ownership database in B04;
- burden_capacity handoff goes to later capacity, transport, vehicle/platform, facility, or project owners and never creates final carrying-capacity math;
- economy_value handoff goes to later economy owners and never creates final currency, price, market, reward, treasure, requisition, or economy law;
- world_law_faction handoff goes to later world/law/faction owners and never creates final legal code;
- storage_security, concealment_trace, decay_maintenance, loss_recovery, canon_lexicon, runtime_review, schema_review, source_local_review, and human_review handoffs must name the unresolved pressure without inventing schema or mechanics.

## 20. Batch B to C00/C-family handoff rules

Batch B procedure may identify that a C-family handoff is needed, but it must not invent C-family fields. B04 must use C00 language for required base fields, source evidence, construct references, outcome references, provenance, source-local boundary, rejected donor elements, canon eligibility, review routing, and missing-schema fallback. The following standard lightweight doctrine-facing C00/C-family block is not a runtime schema, not a backend contract, not an event log, not a database row, not a context packet format, not a command object, not final mechanics, and not C01-C14 schema contents.

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

## 21. Missing-schema fallback and quarantine/escalation

Missing schema coverage must produce `pending_schema`, quarantine, escalation, `human_review`, or `defer_until_schema_exists` rather than improvised schema. B04 must not invent C-family fields, donor field names, donor record formats, inventory database rows, event-sourced inventory ledger entries, ownership database records, runtime commands, backend contracts, or item statblocks.

Unclassifiable inventory/custody/burden records are quarantined or escalated, not normalized by invention. If the source material depends on later B05-B11 procedure or C01-C14 schema contents, B04 records the boundary and defers rather than requiring, defining, creating, or promoting those later files or schemas. B04 does not require, define, create, or promote those later files or schemas.

## 22. Source-local donor inventory/storage/economy handling

Donor inventory/storage/economy systems are evidence only. Donor weight rules, slot rules, encumbrance systems, coin weight, treasure tables, item rarity economies, attunement slots, magic bags, bags of holding, spatial rings, pocket dimensions, pattern storage, cyberdeck loadouts, cargo statblocks, vehicle cargo ratings, requisition systems, post-scarcity storage systems, bank ledgers, vault rules, tax rules, legal codes, licensing systems, contraband lists, and ownership databases are donor evidence only.

Source-local donor inventory/storage/economy handling must:
- identify the donor rule as source-local evidence, not Astra default;
- preserve useful pressure as inventory_access, custody_ownership, burden_capacity, economy_value, world_law_faction, storage_security, concealment_trace, decay_maintenance, loss_recovery, schema_review, source_local_review, or human_review;
- quarantine or escalate donor inventory/storage/currency/slot/container/bag-of-holding/cyberdeck/loadout/cargo/requisition systems when no Astra owner file exists;
- avoid importing donor inventory/equipment/economy systems as Astra defaults through B04;
- avoid promoting repeated donor pressure into final capacity math, final economy law, final legal code, final runtime inventory state, final event-sourced inventory ledger, final ownership database, or accepted canon.

## 23. Runtime boundary

B04 rejects runtime state/event/command lifecycle ownership. B04 is not runtime authority and does not define runtime entity/component/event/state schemas, final runtime inventory state, event-sourced state model, final event-sourced inventory ledger, final ownership database, state delta validator, command lifecycle implementation, context packet compiler, backend validation, database contracts, event logs, hidden-information runtime state, persistent campaign state, live-play narration behavior, or live-play GM adapter behavior.

Live-play behavior must not consume B04 procedure as runtime authority without later runtime validation. The `inventory_custody_routing_note` is doctrine-facing only and is not runtime state.

## 24. Canon boundary

B04 does not promote final canon, accepted lexicon terms, item lists, cargo lists, market tables, treasure tables, storage services, legal codes, faction laws, tax codes, licenses, contraband lists, sourcebook prose, or player-facing rule text. Canon eligibility may be routed through C00/C-family review language, but B04 cannot decide canon promotion.

## 25. Live-play/training boundary

B04 may support training examples about how to think through inventory, custody, burden, storage, and loss pressure. It must not create live-play narration behavior, live GM scripts, hidden-information runtime state, player-facing rules, or sourcebook prose. Live-play behavior must not consume B04 procedure as runtime authority without later runtime validation.

## 26. Examples of good and bad B04 usage

Good B04 usage:
- A party moves a relic from quick_access to vaulted storage. B04 records storage_confirmed, vaulted holding mode, delayed_access, party_shared or escrow scope, legal_visibility and storage_security burdens, then routes object_state to B03 and any schema gap to C00/pending_schema.
- A crew claims captured cargo after a structured encounter. B04 separates possession from ownership and legal permission, marks custody_disputed, identifies platform_cargo_burden and faction_trace, and routes economy_value and world_law_faction pressure without defining final cargo-capacity math or prize law.
- A hidden cache is found damaged. B04 notes hidden_cache_access, container_damage, recoverable_with_project or damaged, routes object damage to B03/object owners, and routes recovery project pressure without inventing loss tables.
- A donor cyberdeck loadout or bag-of-holding rule appears in source material. B04 marks source_local_holding, source_local_access, source_local_burden, and source_local_review, then quarantines or escalates rather than importing donor loadout, magic bag, or spatial storage rules as Astra defaults.

Bad B04 usage:
- Defining a universal inventory slot grid, carrying-capacity formula, coin weight rule, or final encumbrance table.
- Treating possession as ownership, ownership as legal permission, storage as safety, quick_access as final action timing, or a container as automatic burden erasure.
- Creating a runtime inventory database row, event-sourced inventory ledger, ownership database record, command object, backend contract, or context packet format.
- Promoting C01-C14 schema fields, sourcebook gear lists, donor treasure tables, donor requisition ratings, magic bag rules, cargo statblocks, legal code, or economy law to Astra defaults.

## 27. Minimum tests or assertions

Minimum B04 tests or assertions should verify that:
- B04 exists at `docs/doctrine/operations/batch_b/B04_inventory_storage_custody_and_burden_procedure.md`;
- all required B04 sections are present;
- B04 declares ownership and non-ownership;
- B04 references B01, B02, and B03 as upstream Batch B context;
- B04 includes C00 handoff language and `batch_b_to_c_handoff`;
- B04 includes `inventory_custody_routing_note` and marks it as doctrine-facing only;
- B04 includes holding modes, burden types, access states, possession scopes, loss triggers, and loss outcomes;
- B04 separates possession, access, ownership, legal permission, readiness, storage, quick access, custody, and burden;
- B04 includes storage/container/cache/vault/vehicle/platform/facility procedure;
- B04 includes transfer/requisition/escrow/impoundment/shared-possession procedure;
- B04 includes decay/spoilage/maintenance/upkeep/stability routing;
- B04 includes lawful inventory-loss trigger and recovery/retrieval procedure;
- B04 rejects final inventory schema, final inventory capacity math, final weight/slot/encumbrance rules, final economy law, final legal code, final runtime inventory state, final event-sourced inventory ledger, and final ownership database;
- B04 rejects runtime state/event/command lifecycle ownership;
- B04 rejects C-family field invention and C01-C14 schema-content ownership;
- B04 rejects donor inventory/storage/economy systems as Astra defaults;
- B04 includes inventory/custody/burden state-delta routing;
- B04 includes source-local donor inventory/storage/economy handling, quarantine, escalation, `human_review`, and `defer_until_schema_exists`;
- B04 references D00/D09/D17/D19 only as draft source-pack/reference material, not final current doctrine authority;
- B04 does not require, define, create, or promote B05-B11;
- B04 does not require, define, create, or promote C01-C14;
- no registry status is promoted to current.

## 28. Acceptance criteria

B04 is acceptable when it:
- stays focused on inventory, storage, custody, possession, access, quick access, burden, concealment, legal visibility, transfer, lawful loss trigger, and recovery procedure;
- builds on B01, B02, and B03 without rewriting them;
- keeps possession, access, ownership, legal permission, readiness, storage, quick access, custody, and burden separate;
- provides holding-mode, burden-type, access-state, possession-scope, loss-trigger, and loss-outcome vocabulary as doctrine vocabulary only;
- includes owner-file handoff, C00/C-family handoff, missing-schema fallback, quarantine, escalation, `human_review`, and `defer_until_schema_exists`;
- rejects final inventory schema, final object schema, C-family schema fields, C01-C14 schema contents, final item stats, final equipment stats, final carrying-capacity math, final weight/slot/encumbrance rules, final economy law, final legal code, final runtime inventory state, final event-sourced inventory ledger, final ownership database, runtime state/event/command lifecycle ownership, canon promotion, and sourcebook prose;
- treats D00/D09/D17/D19 source material and donor inventory/storage/economy systems as draft reference/evidence only;
- does not require, define, create, or promote B05-B11;
- does not require, define, create, or promote C01-C14;
- leaves registry status unpromoted unless a separate repo convention requires draft/not-current tracking.

## 29. Follow-up handoff to B05

B04's follow-up handoff to B05 is limited to noting unresolved downstream procedure pressure that may need a later Batch B file. B04 does not require, define, create, or promote B05-B11, does not assume B05 content, and does not make B05-B11 current doctrine. Any later B05 work must inherit B04's boundaries rather than using this file to define final mechanics, schema fields, runtime state, canon, sourcebook prose, or donor systems as Astra defaults.

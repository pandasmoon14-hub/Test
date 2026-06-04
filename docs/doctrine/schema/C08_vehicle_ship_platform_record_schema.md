# C08 Vehicle/Ship/Platform Record Schema Doctrine

## 1. Purpose and status

C08 defines Batch C conversion-stage and canon-review record-family schema doctrine for vehicle, ship, starship, mech, platform, station, drone platform, base, mobile base, modular platform, platform-scale system, conveyance, mount-like platform, fleet unit, and large persistent equipment-platform records.

Status posture:
- C08 is a schema-draft doctrine file.
- C08 is not current canon, not accepted lexicon, not sourcebook vehicle prose, not live-play authority, and not runtime-ready.
- C08 is not final vehicle mechanics, not final starship mechanics, not final mech mechanics, not final platform mechanics, not starship combat, not mech combat, not travel procedure, not navigation procedure, not runtime vehicle state, not platform inventory state, not module/hardpoint mechanics, not Traveller jump doctrine, not Lancer frame doctrine, not sourcebook vehicle prose, not canon promotion, and not donor vehicle/starship/mech system import.
- C08 records are conversion-stage/canon-review artifacts only; they preserve evidence, boundaries, routing, and review posture until appropriate owners decide what can become canon, runtime, sourcebook presentation, or final mechanics.

## 2. Owner layer

C08 belongs to Batch C schema-family doctrine under the Astra Doctrine Council - Schema Working Group. It sits below C00 and must obey the Batch C schema family unlock/index/readiness gate. C08 uses Batch A doctrine as upstream conceptual guardrails and Batch B operational files only as doctrine-facing pressure, not as schema-field authority.

## 3. What C08 owns

C08 owns conversion-stage record-family grammar for:
- vehicles, ships, starships, mechs, platforms, stations, drone platforms, bases, mobile bases, modular platforms, platform-scale systems, conveyances, mount-like platforms, fleet units, and large persistent equipment-platform records;
- vehicle/ship/platform classification and routing posture for conversion and canon review;
- platform-scale identity records whose main conversion subject is a persistent conveyance, carrier, station, frame, hull, mount-like support, or equipment-platform rather than an ordinary item, ability, actor, location, scenario, hazard, table, map, or source-local setting assertion;
- composite, parent, child, and satellite record handling when the central record remains vehicle/ship/platform identity;
- references from the platform record to travel pressure, item/gear records, module/installable records, ability/capability records, actors, locations, scenarios, factions, hazards, tables, maps, source-local containment, and runtime-review owners;
- donor vehicle/ship/mech/platform containment as source evidence, donor tags, legal/IP review notes, source-local notes, C14 containment records, or rejected donor elements, not Astra defaults.

## 4. What C08 must not own

C08 must not own or define:
- final mechanics, final vehicle mechanics, final starship mechanics, final mech mechanics, final platform mechanics, movement math, travel procedure, navigation procedure, chase procedure, starship combat, mech combat, dogfighting rules, ship-to-ship combat, vehicle damage systems, crew action economy, station economy, cargo economy, fuel economy, jump/FTL doctrine, Traveller jump default, Lancer frame default, hardpoint mechanics, module mechanics, license mechanics, frame mechanics, mount rules, vehicle scale math, platform inventory state, accepted lexicon, canon acceptance, canon promotion, or live-play behavior;
- final numerical values, hull points, armor, structure, speed, thrust, jump ratings, range bands, maneuver ratings, fuel costs, cargo capacity, crew counts, passenger capacity, hardpoints, module slots, frame licenses, mech size, weapon mounts, station scale, damage thresholds, repair DCs, travel speeds, navigation DCs, upkeep costs, acquisition costs, vehicle prices, cargo values, or vehicle scale math;
- runtime vehicle state, runtime crew state, runtime fuel state, runtime cargo state, runtime module state, runtime station state, runtime map/navigation state, runtime map state, platform inventory state, equipment runtime, entity/component schemas, event schemas, command lifecycle, context packets, save-state nodes, database platform rows, database schemas, backend vehicle schemas, backend navigation schemas, backend schemas, or live-play travel/starship/mech combat procedure;
- sourcebook vehicle prose, player-facing vehicle catalogs, GM vehicle execution, live-play vehicle procedure, training examples as authority, canon promotion, donor vehicle statblock defaults, donor starship systems, donor mech systems, donor platform systems, donor cargo/fuel economy, donor hardpoint/module slot systems, donor field labels, donor proper nouns, or donor-world assumptions as Astra schema.

## 5. C00 inheritance and required base posture

Every durable C08 conversion-stage record must inherit/include `AstraContentRecordBase` from C00 before any C08-specific shaping. C08 may add family-specific doctrine grammar, but it must not remove, rename, or weaken C00 base posture.

C08 must preserve these C00 requirements:
- `packet_refs`, `source_evidence_refs`, `construct_refs`, `outcome_refs`, and `provenance_refs`;
- `source_local_boundary`, `rejected_donor_elements`, `canon_eligibility`, `confidence`, `validation`, lineage, composition, cross-reference, legal/IP posture, review routing, and source-local boundary posture;
- parent/child record refs, cross-reference records, inheritance refusal across family handoffs, confidence routing, validation status, escalation routing, source-local quarantine, and human-review options;
- provenance-lock behavior: donor exact vehicle values, donor field names, donor system terms, donor proper nouns, and donor world assumptions remain evidence unless later review accepts an Astra-native abstraction.

## 6. Vehicle/ship/platform family scope and classification

C08 classifies platform-scale records by conversion/review role, not by final vehicle mechanics. C08 classification uses neutral Astra-facing categories such as:
- platform classification: vehicle, ship, starship-like platform, mech-like platform, station, drone platform, base, mobile base, modular platform, platform-scale system, conveyance, mount-like platform, fleet unit, large persistent equipment-platform, or uncertain platform-like construct;
- scale/scope posture: personal conveyance, crewed conveyance, site-scale platform, station-scale platform, fleet-unit identity, modular platform, platform-as-place overlap, item-platform overlap, actor-controlled platform, or unknown;
- mobility posture: mobile, fixed, orbital, route-bound, carried/deployed, summoned/controlled, dormant, damaged/nonfunctional, abstracted, or unclear;
- crew/control posture: no crew reference, actor refs required, C01 split required, C11 companion/control review required, faction access review required, donor crew roles quarantined, or control posture unclear;
- cargo/storage reference posture: no cargo refs, C02 item refs required, B04 pressure present, cargo evidence quarantined, donor capacity values rejected, or storage state deferred;
- module/reference posture: no module refs, C04 installable refs required, C12 installation/refit process refs required, hardpoint-like evidence quarantined, donor module slots rejected, or module relationship unclear;
- capability/reference posture: no capability refs, C03 capability refs required, active/passive system extraction pending, special movement/effect review required, donor starship/mech system quarantined, or capability unclear;
- item/reference posture: C02 ordinary gear refs required, spare parts refs required, consumable/supply refs required, or onboard equipment split required;
- actor/reference posture: C01 crew/pilot/operator/passenger refs required, C11 bonded/companion/drone posture required, or actor relationship unclear;
- location/reference posture: C06 station/base/shipboard-space refs required, route context required, dock/hangar/shipyard refs required, or platform-as-place split required;
- faction/access reference posture: C05 ownership, license, jurisdiction, fleet, manufacturer, military, guild, requisition, or platform access refs required;
- scenario/reference posture: C07 mission/scenario/adventure refs required, convoy/chase/encounter/platform-dungeon usage refs required, or story-role platform review required;
- hazard/reference posture: C09 crash, hull breach, onboard fire, vacuum/pressure, radiation, contamination, hostile environment, system failure, terrain/environment interaction, or disaster refs required;
- table/reference posture: C10 generator, encounter table, cargo table, module table, route generator, or random platform refs required;
- map/diagram reference posture: C13 deck plan, layout, station diagram, mech diagram, hardpoint diagram, cargo diagram, route diagram, tactical map, or visual evidence refs required;
- source-local/canon-review posture: C14 source-local containment required, proper-noun quarantine required, canon eligibility review required, legal/IP review required, or rejected donor containment required;
- hidden/protected-truth posture, legal/IP posture, and rejection/containment posture.

## 7. C08 record grammar, doctrine-level only

The following YAML-like block is doctrine grammar only. It is not a runtime schema, not a database schema, not a final vehicle statblock, not a starship system, not a mech system, not a platform module system, not a travel/navigation procedure, not a combat procedure, not a cargo/fuel economy, and not sourcebook vehicle prose.

```yaml
C08VehicleShipPlatformRecord:
  extends: AstraContentRecordBase
  schema_family: C08_vehicle_ship_platform
  doctrine_status: schema-draft
  conversion_role: vehicle_ship_platform_identity_record
  platform_classification: neutral_platform_classification
  scale_scope_posture: review_scope_only
  mobility_posture: conversion_review_only
  crew_control_reference_posture: refs_or_split_to_C01_C05_C11
  cargo_storage_reference_posture: refs_or_split_to_C02_B04
  module_reference_posture: refs_or_split_to_C04_C12
  capability_reference_posture: refs_or_split_to_C03
  item_reference_posture: refs_or_split_to_C02
  actor_reference_posture: refs_or_split_to_C01_C11
  location_reference_posture: refs_or_split_to_C06
  faction_access_reference_posture: refs_or_split_to_C05
  scenario_reference_posture: refs_or_split_to_C07
  hazard_reference_posture: refs_or_split_to_C09
  table_reference_posture: refs_or_split_to_C10
  map_diagram_reference_posture: refs_or_split_to_C13
  source_local_canon_review_posture: refs_or_split_to_C14
  hidden_protected_truth_posture: protected_truth_ref_only
  legal_ip_posture: inherited_from_C00_plus_C14_review
  rejection_containment_posture: rejected_donor_elements_required_when_applicable
  inheritance_allowed: false
```

These labels are Astra-facing routing concepts. They intentionally avoid donor vehicle/ship/mech/platform/station/frame/jump/module/hardpoint/cargo/crew field names as Astra labels.

## 8. Donor vehicle, ship, mech, platform, station, frame, jump, module, hardpoint, cargo, crew, and field-name handling

Donor exact vehicle names, ship names, mech names, station names, frame names, module names, hardpoint labels, jump ratings, FTL rules, crew roles, cargo fields, hull values, armor values, speed values, fuel values, station values, license tracks, frame tracks, platform field labels, and vehicle-system terms may be preserved only as source evidence, donor tags, source-local notes, legal/IP review notes, C14 containment records, or rejected donor elements.

C08 rejects donor vehicle systems, starship systems, mech systems, platform systems, Traveller jump default, Lancer frame/license defaults, Starfinder starship roles, MechWarrior/BattleTech-like frame assumptions, ship-to-ship combat defaults, vehicle statblock defaults, cargo/fuel economy defaults, fuel economy defaults, hardpoint defaults, module-slot defaults, platform module defaults, donor field names, donor proper nouns, named vehicles/ships/mechs/stations/fleets/manufacturers/technologies, and donor-world assumptions as Astra defaults. Donor systems such as Traveller jump, Lancer frame/license defaults, Starfinder starship roles, MechWarrior/BattleTech-like frame assumptions, ship-to-ship combat defaults, vehicle statblock defaults, cargo economy defaults, fuel economy defaults, hardpoint defaults, and platform module defaults are blocked from becoming Astra defaults without later doctrine/canon review.

## 9. Travel, item, module, ability, actor, location, scenario, faction, hazard, table, map, source-local, and runtime-review handoffs

Batch B handoff notes are doctrine-facing pressure only and Batch B procedure terms must not become C08 schema fields.

- C08 references B08 when vehicles/ships/platforms create travel, exploration, navigation, discovery, route, movement, transit, jump/FTL, or traversal pressure; B08 is not C08 schema.
- C08 references B03 when vehicle/platform use creates item/gear/equipment/asset use pressure; B03 is not C08 schema.
- C08 references B04 when cargo, storage, custody, burden, onboard inventory, containment, or carried-object pressure appears; B04 is not C08 schema.
- C08 references B06 when repair, salvage, refit, upgrade, installation, modular modification, station work, shipyard work, or platform project procedure pressure appears; B06 is not C08 schema.
- C08 references B10 when vehicle/platform danger, opposition contact, hazard, crash, hull breach, environmental pressure, pursuit, patrol, hostile contact, or active threat trigger pressure appears; B10 is not C08 schema.
- C08 may reference B02 when vehicle/platform use affects action declaration, cost commitment, or resolution trigger pressure; B02 is not C08 schema.

Cross-family handoffs use references and satellite records, not inheritance or merged schemas. Cross-family references do not make the target family inherit C08 grammar.

- C08 -> C01 for crew, pilots, operators, passengers, riders, commanders, owners, NPC crews, onboard creatures, vehicle-scale adversaries, or platform-associated actors.
- C08 -> C02 for carried gear, vehicle equipment, cargo, weapons as practical objects, tools, onboard items, spare parts, consumables, supplies, and ordinary vehicle gear.
- C08 -> C03 for vehicle powers, ship maneuvers, mech routines, platform abilities, active systems, passive systems, special movement effects, weapons/effects requiring capability records, or station effects.
- C08 -> C04 for installed modules, hardpoint-like assets, relic engines, cybernetic interfaces, platform-integrated assets, bonded ship systems, vehicle implants, station modules, and upgradeable special assets.
- C08 -> C05 for faction ownership, institutional fleets, licenses, legal authority, corporate manufacture, military control, guild access, jurisdiction, requisition, or platform access.
- C08 -> C06 for stations, bases, shipboard spaces as places, hangars, docks, shipyards, vehicle locations, route contexts, regions, worlds, or platform-as-place overlap.
- C08 -> C07 for mission/scenario/adventure use, vehicle objectives, chase scenarios, convoy missions, ship encounters, platform dungeons, station adventures, reward placement, or story-role platforms.
- C08 -> C09 for crashes, hull breaches, vacuum/pressure hazards, onboard fires, radiation, contamination, hostile environment, platform hazards, system failures, terrain/environment interactions, or disaster pressure.
- C08 -> C10 for vehicle/ship/platform tables, starship generators, mech generators, station tables, vehicle encounter tables, cargo tables, module tables, route generators, or random platform records.
- C08 -> C11 for companion mounts, bonded vehicles, summoned vehicles, pet drones, controlled drones, cohort vehicles, minion platforms, or companion/summon relationship/control posture.
- C08 -> C12 for construction, crafting, salvage, repair, refit, upgrade, fuel production, parts production, shipyard process, vehicle recipes, module installation process, or platform transformation records.
- C08 -> C13 for deck plans, station diagrams, ship layouts, vehicle diagrams, mech diagrams, hardpoint diagrams, cargo diagrams, route diagrams, tactical maps, or visual platform evidence.
- C08 -> C14 for source-local vehicle names, ship names, mech names, station names, named fleets, named manufacturers, named technologies, donor FTL/jump laws, source-specific frame systems, source-specific vehicle lore, and protected proper nouns.
- C08 -> pending_schema when no stable C-family owner exists.

## 10. C08 cross-family overlap rules

- C08 vs C06: C08 owns vehicle/ship/platform identity. C06 owns locations/sites/regions. Stations, bases, and shipboard spaces may require a C08 platform record plus C06 place records when used as sites.
- C08 vs C04: C08 owns the platform. C04 owns installable modules/special assets integrated into the platform. Platform modules use references, not inheritance.
- C08 vs C02: C08 owns the platform-scale record. C02 owns ordinary gear, cargo, tools, weapons as practical objects, and onboard equipment records.
- C08 vs C03: C08 owns the platform record. C03 owns vehicle powers, ship maneuvers, active systems, effects, and special capabilities.
- C08 vs C09: C08 owns the platform. C09 owns hazards, environmental pressure, system-failure danger, crash pressure, hull breach pressure, and disaster pressure.
- C08 vs C13: C08 owns platform identity. C13 owns deck plans, diagrams, layouts, and visual/spatial evidence.
- C08 vs C05/B05: C08 owns the platform record. C05 owns faction/institution access, ownership, licensing, and control; B05 owns acquisition/requisition/value-flow pressure.
- C08 vs C07/B08/B10: C08 owns the platform record. C07 owns mission/scenario use; B08 owns travel/exploration/navigation pressure; B10 owns hazard/opposition/contact pressure.
- C08 vs C14: C14 owns source-local vehicle names, donor FTL laws, source-specific frame systems, named fleets, named technologies, proper nouns, and donor-world assumptions. C08 may reference them but must not generalize them.
- C08 vs runtime/backend: C08 records conversion-stage platform evidence and routing. Runtime/backend owners decide later whether anything becomes vehicle state, crew state, cargo state, fuel state, module state, station state, navigation state, save-state node, database row, or equipment runtime.
- C08 vs live-play/sourcebook: C08 is not player-facing vehicle prose, not vehicle catalog prose, not live-play travel procedure, not starship/mech combat procedure, not sourcebook platform presentation, and not GM vehicle execution.
- C08 vs donor source: donor jump rules, frame rules, vehicle statblock systems, starship combat roles, crew action economies, cargo/fuel economies, licenses, hardpoints, module slots, and source-specific vehicle lore remain evidence, source-local containment, or rejected material until later doctrine/canon review.

## 11. Composite vehicle/ship/platform record handling

Composite platform records are lawful only when the conversion subject is still a single platform identity. A carrier with crew, cargo, hangars, hazards, tables, deck plans, faction ownership, and special engines remains a C08 identity record only for the platform itself. Crew route to C01, cargo and ordinary gear route to C02/B04, installable assets route to C04/C12, capabilities route to C03, places route to C06, story use routes to C07, dangers route to C09/B10, generators route to C10, diagrams route to C13, and source-local names/laws route to C14.

Composite records must use references and satellite records, not inheritance or field import. A composite platform cannot absorb final mechanics, donor statblock systems, runtime state, sourcebook prose, or canon promotion.

## 12. Parent, child, and satellite record handling

C08 may record parent, child, and satellite relationships for platform identities: a fleet unit with subordinate craft, a station with docked vessels, a mobile base with attached platforms, a mech carrier with drones, or a platform with separable sections. Parent/child/satellite posture remains conversion evidence and review routing; it does not create runtime inventory state, runtime crew state, runtime module state, station economy, hardpoint mechanics, module slot mechanics, or command/control lifecycle.

Child records must keep their own C00 provenance, source evidence, confidence, validation, source-local boundary, rejected donor elements, canon eligibility, and review routing.

## 13. Source-local and legal/IP handling

Source-local and legal/IP handling is mandatory for vehicle/ship/platform records. C08 must route donor vehicle names, ship names, mech names, station names, named fleets, named manufacturers, named technologies, donor FTL/jump laws, source-specific frame systems, source-specific vehicle lore, protected proper nouns, trademark-like terms, license text, verbatim-similarity risk, and donor-world assumptions to source-local/legal/IP/C14 review.

C08 may preserve these elements as source evidence, donor tags, legal/IP review notes, C14 containment records, or rejected donor elements. C08 must not generalize them into Astra default terminology, accepted lexicon, vehicle mechanics, or sourcebook prose.

## 14. Rejected donor element handling

Rejected donor element handling prevents accidental import. Rejected donor elements include donor vehicle systems, donor starship systems, donor mech systems, donor platform systems, Traveller jump defaults, Lancer frame/license defaults, Starfinder starship roles, MechWarrior/BattleTech-like frame assumptions, ship-to-ship combat defaults, vehicle statblock defaults, cargo/fuel economy defaults, hardpoint defaults, module-slot defaults, donor field names, donor proper nouns, named vehicles/ships/mechs/stations/fleets/manufacturers/technologies, donor-world assumptions, hull values, armor values, speed values, fuel values, jump ratings, cargo fields, crew roles, frame tracks, license tracks, station values, and platform field labels.

Rejected donor material must remain attached to provenance and review notes so future reviewers can see what was excluded and why. Rejection is not deletion; it is containment.

## 15. Canon eligibility and review routing

C08 records may mark canon eligibility for review, but C08 never promotes canon and does not accept canon. A C08 record can say that a platform identity, neutral classification, or routing abstraction is eligible for later review; it cannot make a vehicle, ship, mech, station, fleet, technology, jump law, frame system, module system, or donor proper noun canon.

Review routing must distinguish schema-draft conversion evidence from canon approval, final mechanics approval, runtime/backend approval, C14 source-local containment, legal/IP review, and future C11/C12 or other owner review.

## 16. Confidence, validation, and escalation routing

C08 confidence and validation use C00 posture. Low confidence, ambiguous platform identity, donor-field leakage, missing provenance, unresolved source-local proper nouns, legal/IP risk, unsupported module/hardpoint structure, unsupported jump/FTL assumptions, unclear actor/control posture, or cross-family ownership conflict requires escalation, quarantine, human review, or `pending_schema`.

Validation confirms only that the C08 conversion record is correctly routed, has C00 base posture, preserves evidence, rejects donor leakage, and avoids runtime/final-mechanics/sourcebook/canon overreach.

## 17. Hidden-state and protected-truth boundary

C08 must not expose protected truth. Hidden ship identity, secret station purpose, concealed cargo, undisclosed ownership, stealth capability, hidden route, unknown crew, sealed module, classified technology, hidden fleet affiliation, or protected map truth must be represented by references, confidence posture, and review routing rather than public canonical statements.

C08 can record that hidden/protected-truth posture exists; it cannot reveal hidden-state details into sourcebook prose, live-play outputs, player-facing records, or runtime command payloads.

## 18. Runtime boundary

C08 is not runtime authority. It forbids runtime vehicle state, runtime crew state, runtime fuel state, runtime cargo state, runtime module state, runtime station state, runtime navigation state, runtime map state, equipment runtime, save-state nodes, database platform rows, entity/component/event schemas, command lifecycle, context packets, backend vehicle schemas, backend navigation schemas, backend schemas, database schemas, platform inventory state, vehicle damage systems, live-play travel procedure, live-play starship combat procedure, live-play mech combat procedure, ship-to-ship combat procedure, dogfighting rules, cargo economy, fuel economy, station economy, crew action economy, and module/hardpoint mechanics.

Runtime/backend owners decide later whether any reviewed platform evidence becomes vehicle state, crew state, cargo state, fuel state, module state, station state, navigation state, save-state node, database row, equipment runtime, entity/component/event schema, or command lifecycle concept.

## 19. Canon/sourcebook/live-play/training boundary

C08 is not canon/sourcebook/live-play/training authority. C08 never promotes canon, does not accept canon, does not produce sourcebook vehicle prose, does not produce vehicle catalog prose, does not produce player-facing statblocks, does not authorize live-play vehicle procedure, does not authorize travel procedure, does not authorize navigation procedure, does not authorize starship/mech combat procedure, and does not use training examples as authority.

Canon/sourcebook/live-play/training outputs require later owners and review. C08 only stores conversion-stage evidence and routing posture.

## 20. Missing-schema fallback

When no stable C-family owner exists, C08 routes unresolved material to `pending_schema` rather than inventing new fields. Missing schema coverage produces quarantine, escalation, human review, or `pending_schema`, not improvised vehicle fields, donor field labels, backend schemas, runtime state, final mechanics, sourcebook prose, or canon promotion.

## 21. Examples of good and bad C08 usage

Good C08 usage:
- Convert a donor starship-like entry into a neutral C08 platform identity record with source evidence, C00 provenance, C14 containment for its proper name and FTL law, C03 references for special systems, C04 references for installable modules, C01 references for crew, C02/B04 references for cargo, C06/C13 references for deck spaces and diagrams, and C09/B10 references for hull-breach danger.
- Record a mobile base as a C08 platform identity while routing its rooms to C06, mission use to C07, faction control to C05, station work/refit pressure to B06/C12, and hidden-truth posture to protected review.

Bad C08 usage:
- Copy a donor vehicle statblock, starship system, mech frame/license track, Traveller jump rating, Lancer frame/license rule, Starfinder starship role list, MechWarrior/BattleTech-like frame assumption, hull points, armor, speed, cargo capacity, hardpoints, module slots, crew action economy, fuel economy, or ship-to-ship combat procedure as Astra schema.
- Treat a named ship, named mech, named station, named fleet, named manufacturer, named technology, donor FTL law, donor proper noun, sourcebook paragraph, runtime vehicle state, runtime cargo state, database platform row, or live-play combat/travel procedure as C08 canon.

## 22. Minimum tests or assertions

Minimum C08 tests/assertions must verify that:
- the C08 file exists at `docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md`;
- all required sections are present;
- C08 declares ownership and non-ownership;
- C08 inherits/includes `AstraContentRecordBase` and preserves C00 provenance, source-local, rejected donor, canon eligibility, confidence, validation, legal/IP, lineage, composition, and cross-reference posture;
- C08 record grammar is doctrine grammar only and not runtime, database, final statblock, starship system, mech system, platform module system, travel/navigation procedure, combat procedure, cargo/fuel economy, or sourcebook vehicle prose;
- C08 rejects donor vehicle/starship/mech/platform systems, Traveller jump default, Lancer frame/license defaults, Starfinder starship roles, MechWarrior/BattleTech-like frame assumptions, ship-to-ship combat defaults, vehicle statblock defaults, cargo/fuel/hardpoint/module-slot defaults, donor field names, donor proper nouns, named platform entities, and donor-world assumptions as Astra defaults;
- C08 routes Batch B and cross-family handoffs without schema inheritance;
- C08 preserves runtime, canon, sourcebook, live-play, hidden-state, source-local, legal/IP, and rejected-import boundaries;
- the registry marks C08 draft/schema-draft/designed/not_reviewed without current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum promotion.

## 23. Acceptance criteria

C08 is acceptable when:
- the C08 file exists at the exact registry path;
- C08 remains conversion-stage/canon-review schema doctrine only;
- C08 includes C00 base inheritance requirements;
- C08 does not import donor vehicle systems, starship systems, mech systems, platform systems, Traveller jump rules, Lancer frame/license rules, starship combat roles, crew action economies, vehicle statblocks, cargo/fuel economy, hardpoint/module slots, field labels, proper nouns, named vehicles/ships/mechs/stations/fleets/manufacturers/technologies, or donor-world assumptions as Astra schema;
- C08 does not define final vehicle/starship/mech/platform mechanics, travel/navigation procedure, starship/mech combat, movement math, vehicle damage systems, crew action economy, runtime vehicle/crew/cargo/fuel/module/station/navigation state, database schema, live-play vehicle procedure, canon, sourcebook vehicle prose, or accepted lexicon;
- C08 has clear Batch B handoffs and cross-family handoffs;
- C08 includes source-local/legal/IP and rejected-import handling;
- C08 registry posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01/C02/C03/C04/C05/C06/C07/C09/C10/C13/C14 registry posture is preserved and C11/C12 are not promoted;
- focused C08 tests and the full suite pass.

## 24. Follow-up handoff to C11

C08 hands off companion mounts, bonded vehicles, summoned vehicles, pet drones, controlled drones, cohort vehicles, minion platforms, mount-like control relationships, and companion/summon relationship/control posture to C11 when that family is drafted. Until C11 is available, C08 may preserve platform identity evidence and route relationship/control material to C11 todo review or `pending_schema`, but it must not invent companion control mechanics, summon mechanics, bonded mount mechanics, runtime control state, or live-play command procedure.

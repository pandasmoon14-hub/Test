# C12 Crafting/Salvage/Recipe Record Schema Doctrine

## 1. Purpose and status

C12 defines Batch C conversion-stage and canon-review schema doctrine for crafting records, salvage records, repair records, recipe records, installation-process records, modification-process records, extraction records, requisition-process evidence records, blueprints, schematics, formulas, upgrade processes, refit processes, recovery processes, material-processing records, resource-extraction records, transformation-process records, and similar process/recipe records. It exists to preserve source evidence and route review without letting donor crafting systems, salvage systems, repair systems, installation procedures, extraction procedures, requisition systems, crafting economies, material economies, item-price economies, downtime systems, recipe catalogs, blueprint systems, upgrade-slot systems, donor crafting economy defaults, donor costs, donor yields, donor DCs, donor project clocks, donor field names, donor proper nouns, named recipes/materials/blueprints/technologies/production laws, or donor-world assumptions become Astra defaults.

Status posture:
- C12 is a schema-draft doctrine file.
- C12 is not current canon, not runtime-ready, not stable_for_family, not stable_cross_family, and not tested_minimum.
- C12 records are conversion-stage/canon-review artifacts; they are not final crafting mechanics, not final salvage mechanics, not repair procedure, not installation procedure, not requisition procedure, not acquisition procedure, not project procedure, not downtime procedure, not training procedure, not research procedure, not reward economy, not item economy, not material economy, not crafting economy, not salvage economy, not donor crafting economy default, not value-flow procedure, not recipe canon acceptance, not final recipe list, not sourcebook crafting prose, not sourcebook recipe catalog, not runtime crafting state, not runtime project state, not runtime recipe state, not runtime inventory state, not runtime installation state, not runtime repair state, not runtime salvage state, not runtime requisition state, not database recipe rows, not backend crafting schemas, not accepted lexicon, not canon acceptance, not canon promotion, and not live-play behavior.
- C12 never promotes canon, does not accept canon, does not create accepted lexicon, and does not decide live-play behavior.

## 2. Owner layer

Owner layer: Batch_C schema family doctrine.

C12 supports conversion intake, conversion output, canon review, legal/IP review, C14 source-local review, Batch B handoff review, and later runtime/backend review. Batch B operational files remain doctrine-facing pressure only; they are not C12 schema fields and are not inherited by C12 records.

## 3. What C12 owns

C12 owns conversion-stage record-family grammar for:
- crafting records;
- salvage records;
- repair records;
- recipe records;
- installation-process records;
- modification-process records;
- extraction records;
- requisition-process evidence records;
- blueprints, schematics, and formulas as process/recipe evidence when the record is about what the evidence says rather than visual presentation;
- upgrade processes, refit processes, recovery processes, material-processing records, resource-extraction records, and transformation-process records.

C12 owns crafting/salvage/recipe classification and routing posture for conversion and canon review. It records how a donor process or recipe construct was identified, whether input/reference posture or output/reference posture is asserted, which material/tool/site/project/acquisition/installation/hazard/table/map/source-local records must be referenced, whether hidden/protected-truth handling is needed, whether source-local/canon-review routing is required, what legal/IP posture applies, and what rejected donor element posture blocks leakage.

C12 owns the process/recipe evidence record. It may reference item, relic, platform, companion, location, faction, acquisition, project, hazard, table, map, source-local, and runtime-review owners, but it does not absorb those owners.

## 4. What C12 must not own

C12 must not own or define:
- final mechanics;
- final crafting mechanics;
- final salvage mechanics;
- repair procedure;
- installation procedure;
- requisition procedure;
- acquisition procedure;
- project procedure;
- downtime procedure;
- training procedure;
- research procedure;
- reward economy;
- item economy;
- material economy;
- crafting economy;
- salvage economy;
- donor crafting economy default;
- value-flow procedure;
- recipe canon acceptance;
- final recipe list;
- sourcebook crafting prose;
- sourcebook recipe catalog;
- runtime crafting state;
- runtime project state;
- runtime recipe state;
- runtime inventory state;
- runtime installation state;
- runtime repair state;
- runtime salvage state;
- runtime requisition state;
- database recipe rows;
- backend crafting schemas;
- accepted lexicon;
- canon acceptance;
- canon promotion;
- live-play behavior.

C12 must not define final numerical values, crafting costs, material costs, salvage yields, repair DCs, installation DCs, extraction DCs, project clocks, downtime durations, crafting times, recipe levels, item levels, rarity tiers, required skill ranks, resource points, value conversions, market prices, component counts, upgrade slots, hardpoint counts, material yields, failure tables, mishap tables, or crafting economy math.

## 5. C00 inheritance and required base posture

Every durable C12 record must inherit/include `AstraContentRecordBase` from C00 before any C12-specific shaping. C12 preserves C00 packet_refs, source_evidence_refs, construct_refs, outcome_refs, provenance_refs, source_local_boundary, rejected_donor_elements, canon_eligibility, confidence, validation, lineage, composition, cross-reference, legal/IP posture, review routing, and source-local boundary posture.

C12 records must keep the C00 distinction between source evidence, conversion classification, rejected donor elements, source-local boundaries, canon eligibility, validation status, lineage, parent/child records, satellite records, and cross-reference records. C12 cannot drop provenance merely because a donor crafting, salvage, repair, recipe, installation, modification, extraction, requisition, blueprint, schematic, formula, material-processing, resource-extraction, upgrade, refit, recovery, or transformation label appears familiar.

## 6. Crafting/salvage/recipe family scope and classification

C12 classifies process records by conversion/review role, not by final mechanics. Neutral Astra-facing classification may include:
- process classification;
- input/reference posture;
- output/reference posture;
- material/reference posture;
- tool/site/reference posture;
- project/procedure handoff posture;
- acquisition/value-flow reference posture;
- installation/modification reference posture;
- hazard/safety reference posture;
- table/reference posture;
- map/diagram reference posture;
- source-local/canon-review posture;
- hidden/protected-truth posture;
- legal/IP posture;
- rejection/containment posture.

These categories route evidence to the correct owner and review lane. They are not final crafting categories, not salvage categories, not repair rules, not recipe levels, not item rarity tiers, not skill lists, not material price tiers, and not economy math.

## 7. C12 record grammar, doctrine-level only

The following compact shape is doctrine grammar only. It is not a runtime schema, not a database schema, not final crafting procedure, not salvage economy, not repair procedure, not installation procedure, not requisition procedure, not project tracker, not sourcebook recipe prose, and not canon recipe acceptance.

```yaml
C12CraftingSalvageRecipeRecord:
  extends: AstraContentRecordBase
  doctrine_scope: conversion_stage_canon_review_only
  process_classification: crafting | salvage | repair | recipe | installation_process | modification_process | extraction | requisition_process_evidence | blueprint_evidence | schematic_evidence | formula_evidence | upgrade_process | refit_process | recovery_process | material_processing | resource_extraction | transformation_process | mixed_process | pending_schema
  input_reference_posture: C02_reference | C04_reference | C08_reference | C11_reference | C14_reference | source_evidence_only | rejected_import | pending_schema
  output_reference_posture: C02_reference | C03_reference | C04_reference | C08_reference | C11_reference | C14_reference | source_evidence_only | rejected_import | pending_schema
  material_reference_posture: C02_reference | C06_reference | C09_reference | C14_source_local_only | B04_pressure_only | B05_pressure_only | source_evidence_only | rejected_import | pending_schema
  tool_site_reference_posture: C02_reference | C06_reference | C08_reference | C13_reference | source_evidence_only | rejected_import | pending_schema
  project_procedure_handoff_posture: B06_pressure_only | B07_pressure_only | no_batch_b_pressure | pending_schema
  acquisition_value_flow_reference_posture: B05_pressure_only | C05_reference | source_evidence_only | rejected_import | pending_schema
  installation_modification_reference_posture: C04_reference | C08_reference | B06_pressure_only | source_evidence_only | rejected_import | pending_schema
  hazard_safety_reference_posture: C09_reference | B10_pressure_only | source_evidence_only | rejected_import | pending_schema
  table_reference_posture: C10_reference | source_evidence_only | rejected_import | pending_schema
  map_diagram_reference_posture: C13_reference | source_evidence_only | rejected_import | pending_schema
  source_local_canon_review_posture: C14_reference | legal_ip_review | canon_review_required | source_local_only | rejected_import
  hidden_protected_truth_posture: none | protected_truth_review | hidden_from_player_facing_outputs | human_review
  rejection_containment_posture: none | rejected_donor_elements_required | source_local_containment_required | legal_ip_review_required | pending_schema
```

C12-specific labels must be neutral Astra-facing routing labels. Donor crafting/salvage/recipe/repair/economy field names, tool labels, cost labels, yield labels, DC labels, clock labels, rarity labels, slot labels, skill labels, market labels, blueprint labels, and production-law labels must remain evidence, source-local notes, legal/IP review notes, C14 containment records, or rejected donor elements.

## 8. Donor crafting, salvage, repair, recipe, installation, modification, extraction, requisition, blueprint, schematic, economy, and field-name handling

Donor exact recipe names, formula names, blueprint names, schematic names, material names, crafting categories, salvage categories, repair rules, installation procedures, extraction procedures, requisition rules, project clocks, downtime costs, tool requirements, crafting skills, material costs, item prices, market values, rarity tiers, item levels, upgrade slots, component counts, yield values, mishap rules, and field labels may be preserved only as source evidence, donor tags, source-local notes, legal/IP review notes, C14 containment records, or rejected donor elements.

C12 explicitly blocks donor crafting systems, salvage systems, repair systems, downtime systems, requisition economies, crafting economies, material economies, item-price economies, recipe catalogs, blueprint systems, upgrade-slot systems, installation procedures, extraction procedures, and source-specific production laws from becoming Astra defaults without later doctrine/canon review.

Donor costs, donor yields, donor DCs, donor project clocks, donor field names, donor proper nouns, named recipes/materials/blueprints/technologies/production laws, donor-world assumptions, donor crafting economy defaults, and source-specific production lore must not become C12 schema labels, accepted lexicon, canon, runtime defaults, or sourcebook prose.

## 9. Item, relic, platform, companion, location, faction, acquisition, project, hazard, table, map, source-local, and runtime-review handoffs

Required Batch B handoffs:
- C12 references B06 when crafting, salvage, repair, upgrade, installation, removal, modification, refit, tuning, extraction, transformation, or project-procedure pressure appears, but B06 is not C12 schema.
- C12 references B05 when acquisition, requisition, reward, value flow, purchase, payment, market, material sourcing, recipe access, faction supply, or compensation pressure appears, but B05 is not C12 schema.
- C12 references B03 when item/gear/equipment/asset use is required by or produced by a process, but B03 is not C12 schema.
- C12 references B04 when inventory, storage, custody, burden, material containment, carried components, or workshop storage pressure appears, but B04 is not C12 schema.
- C12 references B07 when recovery, training, research, preparation, study, experimentation, blueprint learning, recipe discovery, or readiness pressure appears, but B07 is not C12 schema.
- C12 may reference B08 when resource extraction, salvage sites, travel to materials, exploration of workshops, or discovery of recipe/material sources appears, but B08 is not C12 schema.
- C12 may reference B10 when hazardous crafting, volatile salvage, unsafe repair, contamination, radiation, poison, corruption, cursed materials, or active threat trigger pressure appears, but B10 is not C12 schema.
- Batch B procedure terms must not become C12 schema fields.

Required cross-family handoffs:
- C12 -> C01 for creatures/NPCs used as crafters, instructors, salvagers, repairers, suppliers, recipients, biological sources, harvested bodies, or process actors.
- C12 -> C02 for crafted items, repaired gear, salvaged gear, material objects, tools, components, consumables, ordinary outputs, ordinary inputs, and practical equipment.
- C12 -> C03 for abilities, powers, techniques, rituals, routines, project-enabled effects, crafting techniques, repair techniques, extraction techniques, or process-granted capabilities.
- C12 -> C04 for relics, implants, installable assets, cyberware, biotech, bonded assets, modules, upgrades, socketed assets, installation/removal/modification targets, and special-asset outputs.
- C12 -> C05 for faction recipes, guild training, institutional crafting, requisition access, restricted blueprints, licenses, supply chains, manufacturers, patrons, markets, and legal authority.
- C12 -> C06 for workshops, laboratories, shipyards, salvage sites, resource nodes, extraction regions, repair yards, factories, sanctums, clinics, stations, and process locations.
- C12 -> C07 for crafting/salvage/repair/requisition objectives, project missions, resource extraction quests, repair scenarios, upgrade objectives, blueprint recovery, and process-based story roles.
- C12 -> C08 for vehicle construction, ship repair, platform refit, mech upgrade, station work, module installation, cargo conversion, fuel production, and platform transformation.
- C12 -> C09 for hazardous materials, contaminated salvage, volatile recipes, unsafe repair, cursed crafting, toxic extraction, radiation/corruption/poison/disease pressure, mishap pressure, and safety hazards.
- C12 -> C10 for crafting tables, salvage tables, recipe tables, material generators, mishap tables, workshop tables, requisition tables, loot-to-material tables, and random process generators.
- C12 -> C11 for companion training projects, taming processes, bonding processes, contract rituals, summon recipes, drone construction, pet care processes, companion modifications, and recovery/upkeep processes.
- C12 -> C13 for blueprints, schematics, crafting diagrams, repair diagrams, installation diagrams, extraction maps, salvage diagrams, workshop layouts, upgrade schematics, and visual process evidence.
- C12 -> C14 for source-local materials, named recipes, named technologies, named blueprints, donor-world production laws, source-specific crafting traditions, named artifacts, protected proper nouns, and donor-world assumptions.
- C12 -> pending_schema when no stable C-family owner exists.

## 10. C12 cross-family overlap rules

- C12 vs C02: C12 owns process/recipe/salvage/repair records. C02 owns item/gear input and output records. A recipe is not an item schema, and item stats do not become recipe fields.
- C12 vs C04: C12 owns installation, removal, modification, repair, upgrade, and transformation process records. C04 owns the relic/implant/installable asset record.
- C12 vs C08: C12 owns construction/refit/repair/upgrade/fuel-production/process records. C08 owns the vehicle/ship/platform record.
- C12 vs C11/B07: C12 owns process records such as taming, bonding, training recipe, contract ritual, companion modification, or upkeep. C11 owns companion/summon relationship/control record; B07 owns recovery/training/research/preparation procedure pressure.
- C12 vs B06: C12 owns conversion-stage process/recipe evidence and routing. B06 owns operational project/crafting/salvage/repair/upgrade procedure.
- C12 vs B05: C12 owns process/recipe evidence and references. B05 owns acquisition/reward/requisition/value-flow procedure.
- C12 vs C09: C12 owns the process record. C09 owns hazard/environment/safety pressure.
- C12 vs C10: C12 owns converted process/recipe records. C10 owns tables/oracles/generators and row provenance.
- C12 vs C13: C12 owns the process/recipe record. C13 owns diagrams, blueprints as visual evidence, schematics, maps, and annotation provenance. A schematic may require both C12 process record and C13 visual evidence record.
- C12 vs C14: C14 owns source-local proper nouns, donor-world production law, named recipes, named materials, source-specific technology, protected lore, and donor-world assumptions. C12 may reference them but must not generalize them.
- C12 vs runtime/backend: C12 records conversion-stage process evidence and routing. Runtime/backend owners decide later whether anything becomes crafting state, project state, recipe state, installation state, inventory state, save-state node, database row, project tracker, or backend crafting schema.
- C12 vs live-play/sourcebook: C12 is not player-facing crafting prose, not recipe catalog presentation, not live-play project procedure, not live-play crafting execution, not GM economy execution, and not sourcebook crafting rules.
- C12 vs donor source: donor crafting economies, salvage economies, repair procedures, requisition systems, downtime systems, crafting skill systems, recipe catalogs, material price systems, upgrade-slot systems, production laws, and source-specific crafting lore remain evidence, source-local containment, or rejected material until later doctrine/canon review.

C12 must use references and satellite records, not inheritance or merged schemas, whenever another family owns actor, item, relic, faction, location, mission, platform, hazard, table, companion, diagram, source-local, runtime/backend, or Batch B procedure pressure.

## 11. Composite crafting/salvage/recipe record handling

Composite records may preserve a donor construct that combines recipe text, blueprint evidence, item output, special asset installation, project procedure pressure, acquisition pressure, hazard pressure, and source-local lore. The composite C12 record must split ownership through references and satellite records instead of merging schemas.

A composite donor vehicle refit recipe, for example, may keep C12 process evidence, route the vehicle to C08, tools/components to C02, special modules to C04, yard location to C06, license to C05/B05, hazardous fuel to C09, blueprint art to C13, donor production law to C14, and operational procedure pressure to B06.

## 12. Parent, child, and satellite record handling

C12 may use parent, child, and satellite records to preserve lineage and composition without merging ownership. Parent records may represent donor crafting systems, salvage systems, recipe catalogs, upgrade chains, refit sequences, production traditions, blueprint collections, or process clusters under review. Child records may represent separable process variants, input/output evidence, material evidence, installation evidence, extraction evidence, repair evidence, requisition evidence, or rejection partitions.

Satellite records carry C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C13, C14, Batch B pressure, or `pending_schema` material. Satellite records do not turn those owner fields into C12 fields.

## 13. Source-local and legal/IP handling

C12 preserves source-local and legal/IP handling for protected recipe names, formula names, blueprint names, schematic names, named materials, named technologies, named artifacts, protected proper nouns, donor-world production laws, source-specific crafting traditions, source-specific salvage lore, source-specific repair law, source-specific requisition authority, license-specific expressions, and verbatim-similar descriptions. Source-local material routes to source-local/legal/IP/C14 review and may be referenced by C12 only as evidence or boundary context.

C12 must not generalize source-local materials, named recipes, named technologies, named blueprints, source-specific production laws, protected proper nouns, donor-world assumptions, or donor-world crafting economies into Astra defaults.

## 14. Rejected donor element handling

C12 must preserve rejected donor element handling whenever donor material is not safe for Astra schema. Rejected material may include donor crafting systems, donor salvage systems, donor repair systems, donor installation procedures, donor extraction procedures, donor requisition systems, donor downtime systems, donor crafting economies, donor material economies, donor item-price economies, donor recipe catalogs, donor blueprint systems, donor upgrade-slot systems, donor costs, donor yields, donor DCs, donor project clocks, donor tool requirements, donor skill requirements, donor rarity tiers, donor field names, donor proper nouns, donor source-specific prompt language, named recipes/materials/blueprints/technologies/production laws, and donor-world assumptions.

Rejected material must be represented through `rejected_import`, `rejected_donor_elements`, source evidence, source-local containment, legal/IP review, C14 containment, human review, or `pending_schema`. Rejection is not deletion; rejection preserves provenance while blocking default import.

## 15. Canon eligibility and review routing

C12 may record canon eligibility and review routing signals inherited from C00, but C12 never promotes canon, never performs recipe canon acceptance, and never turns recipe evidence into a final recipe list. Canon/sourcebook/runtime owners decide later whether any process, recipe, blueprint, schematic, formula, salvage pattern, repair pattern, installation process, requisition evidence, material-processing record, or transformation process becomes canon, sourcebook text, runtime behavior, or accepted lexicon.

C12 canon eligibility flags are routing metadata only. They are not canon promotion, not canon acceptance, not current doctrine, not recipe acceptance, not sourcebook recipe catalog approval, and not live-play permission.

## 16. Confidence, validation, and escalation routing

C12 confidence and validation posture must identify whether the conversion evidence is clear, partial, contradictory, source-local, legally risky, hidden/protected, donor-system-shaped, economy-shaped, runtime-shaped, or missing an owner. Low confidence, unresolved donor economy pressure, unsupported field pressure, source-local leakage risk, legal/IP risk, hidden-truth risk, runtime-state pressure, and missing-schema pressure route to human review, C00/C14 review, Batch B pressure review, runtime/backend review, or `pending_schema`.

Validation confirms only that C12 conversion-stage evidence and routing are present. Validation does not prove final mechanics, economy math, crafting procedure, repair procedure, salvage procedure, installation procedure, requisition procedure, project procedure, runtime readiness, canon acceptance, or sourcebook readiness.

## 17. Hidden-state and protected-truth boundary

C12 must preserve hidden-state and protected-truth boundary language when a process record reveals secret recipes, hidden blueprints, concealed sabotage, cursed materials, contaminated salvage, protected faction supply, undisclosed production law, disguised materials, secret installation methods, or GM-only outcomes. Protected truth remains evidence and routing posture; it is not runtime hidden state and not player-facing sourcebook prose.

C12 may mark hidden/protected-truth posture for review, but it must not create hidden-information runtime state, reveal protected truth in training examples, compile context packets, or define live-play disclosure behavior.

## 18. Runtime boundary

C12 forbids runtime crafting state, runtime project state, runtime recipe state, runtime inventory state, runtime installation state, runtime repair state, runtime salvage state, runtime requisition state, project trackers, crafting queues, save-state nodes, database recipe rows, entity/component/event schemas, command lifecycle, context packets, backend crafting schemas, backend inventory schemas, backend project schemas, backend installation schemas, backend repair schemas, backend salvage schemas, and live-play crafting/project execution.

Runtime/backend owners decide later whether anything becomes crafting state, project state, recipe state, installation state, inventory state, save-state node, database row, project tracker, crafting queue, entity/component/event schema, command lifecycle behavior, context packet material, backend crafting schema, backend inventory schema, or live-play execution. C12 only preserves conversion-stage process evidence and routing.

## 19. Canon/sourcebook/live-play/training boundary

C12 is not canon, not sourcebook crafting prose, not sourcebook recipe prose, not sourcebook recipe catalog, not player-facing crafting rules, not live-play crafting execution, not live-play project execution, not GM economy execution, not training examples, and not final mechanics. Training, evaluation, and example systems may reference C12 only after the relevant doctrine, canon, runtime, and legal/IP owners approve their own layers.

C12 must not convert donor crafting prose, donor salvage procedures, donor repair procedures, donor installation procedures, donor requisition systems, donor downtime systems, recipe catalogs, blueprint systems, material price systems, upgrade-slot systems, crafting skill systems, donor production law, or source-specific crafting lore into Astra sourcebook text.

## 20. Missing-schema fallback

When a process/recipe construct has no stable C-family owner, route to `pending_schema` with quarantine, escalation, human review, or source-local containment. `pending_schema` is named fallback routing only; it is not a permission to invent process fields, recipe mechanics, economy fields, runtime state, database schema, sourcebook prose, accepted lexicon, or canon.

Missing future crafting mechanics, salvage mechanics, repair procedures, installation procedures, requisition procedures, project procedures, material economy, recipe catalog, blueprint system, upgrade-slot system, or runtime/backend state must remain deferred rather than backfilled by C12.

## 21. Examples of good and bad C12 usage

Good C12 usage:
- Preserve a donor crafting recipe as C12 process/recipe evidence, route its ordinary output to C02, route its special relic output to C04, route material names to C14, and reject donor crafting costs as Astra defaults.
- Preserve a salvage procedure as C12 salvage evidence while routing recovered gear to C02, contaminated material pressure to C09, salvage-site location to C06/B08, and operational project pressure to B06.
- Preserve a ship refit blueprint as C12 process evidence while routing the platform to C08, blueprint diagram evidence to C13, required facility to C06, license/supply pressure to C05/B05, and donor upgrade-slot math to rejected donor elements.
- Preserve a companion bonding ritual as C12 process evidence while routing the companion relationship to C11, ritual capability to C03, training/recovery pressure to B07, and donor-world spirit law to C14.

Bad C12 usage:
- Convert donor crafting costs, donor material costs, donor yields, donor DCs, or donor project clocks into Astra final crafting mechanics or crafting economy math.
- Convert donor salvage tables, repair procedures, installation procedures, requisition systems, downtime systems, recipe catalogs, blueprint systems, or upgrade-slot systems into Astra defaults.
- Turn a process record into runtime crafting state, runtime project state, runtime recipe state, runtime inventory state, crafting queues, database recipe rows, backend crafting schemas, or live-play crafting/project execution.
- Use donor crafting/salvage/recipe/repair/economy field names as C12 schema labels.
- Promote named recipes, named materials, named blueprints, named schematics, named technologies, donor proper nouns, production laws, or donor-world assumptions into canon without later review.

## 22. Minimum tests or assertions

Minimum C12 tests should assert that:
- the C12 file exists at the registry path;
- all required sections are present;
- C12 declares ownership and non-ownership;
- C12 explicitly inherits/includes C00 `AstraContentRecordBase`;
- C12 doctrine grammar is not runtime/database/final-crafting-procedure/salvage-economy/repair-procedure/installation-procedure/requisition-procedure/project-tracker/sourcebook-recipe-prose/canon-recipe-acceptance schema;
- donor crafting/salvage/repair/installation/extraction/requisition/economy/downtime/recipe-catalog/blueprint/upgrade-slot/cost/yield/DC/project-clock/field-name/proper-noun leakage is rejected;
- B06, B05, B03, B04, B07, B08, and B10 remain handoffs rather than schema fields;
- C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C13, C14, and `pending_schema` handoffs are present;
- runtime, canon, sourcebook, live-play, hidden-truth, source-local, legal/IP, and rejected-import boundaries are preserved;
- registry posture remains draft/schema-draft/designed/not_reviewed without current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum promotion.

## 23. Acceptance criteria

C12 is acceptable when:
- C12 file is created at `docs/doctrine/schema/C12_crafting_salvage_recipe_record_schema.md`;
- C12 remains conversion-stage/canon-review schema doctrine only;
- C12 includes C00 base inheritance requirements;
- C12 does not import donor crafting systems, salvage systems, repair systems, installation procedures, requisition systems, crafting economies, material economies, downtime systems, recipe catalogs, blueprint systems, upgrade mechanics, crafting costs, yields, DCs, project clocks, field labels, proper nouns, named recipes/materials/blueprints/technologies/production laws, or donor-world assumptions as Astra schema;
- C12 does not define final crafting mechanics, salvage mechanics, repair procedure, installation procedure, requisition procedure, runtime crafting/project/recipe/inventory/installation/repair/salvage state, database schema, live-play crafting/project execution, canon, sourcebook recipe prose, or accepted lexicon;
- C12 has clear Batch B handoffs and cross-family handoffs;
- C12 includes source-local/legal/IP and rejected-import handling;
- C12 registry posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01/C02/C03/C04/C05/C06/C07/C08/C09/C10/C11/C13/C14 registry posture is preserved;
- focused tests pass;
- full suite passes.

## 24. Follow-up handoff to Batch C capstone/readiness gate

C12 completes the remaining Batch C family schema draft slot and hands readiness evidence to the Batch C capstone/readiness gate. The capstone/readiness gate may review whether C00-C14 are consistently drafted, but C12 does not promote itself or other C-family records to current, canon, runtime-ready, stable_for_family, stable_cross_family, or tested_minimum.

Until a later Batch C capstone/readiness gate and appropriate doctrine/canon/runtime owners complete their own review, C12 must not invent final crafting mechanics, salvage economy, repair procedures, installation procedures, requisition procedures, project procedures, recipe canon acceptance, sourcebook crafting prose, runtime crafting state, runtime project state, runtime recipe state, backend crafting schemas, donor crafting/salvage/economy-system imports, or live-play crafting/project execution.

# C02 Item/Gear Record Schema Doctrine

## 1. Purpose and status

C02 defines Batch C conversion-stage and canon-review record-family schema doctrine for item/gear records. It covers practical item, gear, tool, weapon, armor, consumable, kit, equipment, portable object, carried object, mundane gear, enhanced gear pending review, and similar item-like constructs extracted from donor material and converted into Astra-facing review records.

Status posture:
- C02 is a schema-draft doctrine file.
- C02 is not current canon, not accepted lexicon, not sourcebook gear prose, not live-play authority, and not runtime-ready.
- C02 is not final item mechanics, final equipment math, combat balance, economy balance, runtime inventory model, donor item-table import format, equipment table, shop system, loot system, or canon promotion procedure.
- C02 records are conversion-stage/canon-review artifacts only; they preserve evidence, boundaries, routing, and review posture until appropriate owners decide what can become canon, final mechanics, or runtime implementation.

## 2. Owner layer

C02 belongs to Batch C schema-family doctrine under the Astra Doctrine Council - Schema Working Group. It sits below C00 and must obey the Batch C unlock/index/readiness gate. C02 uses Batch A asset, object, actor, economy, location, hazard, and source-local doctrine as upstream conceptual guardrails and Batch B operations only as handoff pressure, not as schema-field authority.

## 3. What C02 owns

C02 owns conversion-stage record-family grammar for:
- practical item, gear, tool, weapon, armor, consumable, kit, equipment, portable object, carried object, mundane gear, enhanced gear pending review, and similar item-like constructs;
- item/gear conversion records whose main identity is a practical object rather than a creature, capability, relic/installable asset, faction, location, scenario, vehicle/platform, hazard, table row, recipe/process, map annotation, or source-local setting assertion;
- C02-specific item/gear classification and routing posture for conversion and canon review;
- C02 parent, child, composite, and satellite handling when the central record remains an item/gear object-like construct;
- references from the item/gear record to carrier/owner actors, capabilities, relic/installable assets, factions, locations, scenarios, vehicle/platform records, hazards, table/oracle rows, recipes/processes, map/diagram annotations, and source-local owners;
- donor item-table containment as evidence, donor equipment-entry containment as evidence, donor tags, rejected donor elements, or source-local context, not Astra defaults.

## 4. What C02 must not own

C02 must not own or define:
- final mechanics, final equipment math, combat balance, economy balance, price curves, rarity math, load math, numerical item values, damage, armor, defense, weight, encumbrance, bulk, price, rarity, item level, attunement, charges, ammunition, durability, repair DC, crafting cost, upgrade slots, hardpoints, capacity, consumable counts, or equipment math;
- inventory state, runtime custody state, runtime item IDs, runtime inventory state, entity/component schemas, event schemas, command lifecycle, context packets, save-state, database contracts, backend item schemas, runtime object state, shop systems, loot systems, persistence models, or live runtime behavior;
- crafting procedure, salvage procedure, repair procedure, upgrade procedure, requisition procedure, acquisition procedure, economy procedure, reward procedure, item-use procedure, custody/burden procedure, encounter procedure, action procedure, live-play behavior, sourcebook gear tables, sourcebook prose, accepted lexicon, canon acceptance, or canon promotion;
- donor item tables, donor equipment entries, donor field names as Astra labels, donor item categories, donor math, donor prices, donor rarity, donor weight/bulk/encumbrance, donor damage/armor values, donor charges/ammunition/durability, donor crafting costs, donor upgrade slots/hardpoints, donor economy assumptions, donor proper nouns, or donor item/equipment formats as Astra defaults;
- actor ownership, item-granted capabilities, relic/installable posture, faction law, location placement, scenario reward placement, vehicle/platform components, hazard behavior, table/oracle generation, crafting recipes/processes, map annotations, or source-local setting law except by reference to their owner families.

## 5. C00 inheritance and required base posture

Every durable C02 conversion-stage record must inherit/include `AstraContentRecordBase` from C00 before any C02-specific shaping. C02 may add family-specific doctrine grammar, but it must not remove, rename, or weaken C00 base posture.

C02 must preserve these C00 requirements:
- `packet_refs`, `source_evidence_refs`, `construct_refs`, `outcome_refs`, and `provenance_refs`;
- `source_local_boundary`, `rejected_donor_elements`, `canon_eligibility`, `confidence`, `validation`, lineage, composition, cross-reference, and legal/IP posture;
- parent/child record refs, cross-reference records, inheritance refusal across family handoffs, confidence routing, validation status, escalation routing, source-local quarantine, and human-review options;
- provenance-lock behavior: donor exact values and donor terms remain source evidence, donor tags, or rejected donor elements unless later review accepts an Astra-native abstraction.

## 6. Item/gear family scope and classification

C02 classifies item/gear conversion records by role in conversion and review, not by final mechanics. C02 classification uses neutral Astra-facing categories such as:
- item classification: practical gear, tool, weapon-like object, armor-like object, consumable-like object, kit, equipment, portable object, carried object, mundane gear, enhanced gear pending review, or uncertain item-like construct;
- portability/scale posture: hand-carried, worn-carried, pack-carried, crew-movable, site-bound practical object, vehicle-associated reference, platform-scale split required, or unknown;
- use-access posture: passive object, manually used object, restricted-access object, trained-use object, consumable-use pressure, activation review required, or unclear;
- custody/burden reference posture: no custody pressure, B04 reference required, C01 carrier refs required, C05 institutional custody refs required, storage/site refs required, or pending_schema;
- capability/reference posture: no extracted capabilities, capability refs required, capability extraction pending, donor effect list quarantined, or C03 split required;
- installable/relic reference posture: ordinary gear, enhanced gear pending review, relic/installable refs required, host-integrated split required, bonded/special asset split required, or C04 split required;
- value/acquisition reference posture: no value pressure, B05 reference required, faction/requisition refs required, reward placement refs required, donor economy quarantined, or pending_schema;
- crafting/salvage reference posture: no process pressure, B06 reference required, recipe/process refs required, salvage/repair/upgrade refs required, C12 split required, or pending_schema;
- vehicle/platform reference posture: no platform pressure, vehicle-carried refs required, platform-mounted split required, C08 split required, or pending_schema;
- source-local/canon-review posture: reusable_pattern_candidate, source_local_retained, legal_ip_review_required, C14_review_required, rejected_import, or quarantined;
- legal/IP posture: clear generic pattern, source-local label retained, trademark-like label retained as evidence, named material retained as evidence, named technology retained as evidence, legal review required, or quarantined.

## 7. C02 record grammar, doctrine-level only

The following YAML-like block is doctrine grammar only. It is not a runtime schema, not a database schema, not a final item statblock, not an equipment table, not sourcebook gear prose, not a donor item-table import contract, and not final Astra mechanics.

```yaml
C02ItemGearRecord:
  extends: AstraContentRecordBase
  schema_family: C02
  record_kind: item_gear_object_like_conversion_record
  item_classification: neutral Astra-facing category, not donor item category
  portability_scale_posture: neutral review category
  use_access_posture: neutral review category
  custody_burden_reference_posture: none | refs_required | B04_reference_required | split_to_C01 | split_to_C05 | split_to_C06 | pending_schema
  capability_reference_posture: none | refs_required | extraction_pending | donor_effect_list_quarantined | split_to_C03
  installable_relic_reference_posture: ordinary_gear | refs_required | enhanced_pending_review | split_to_C04 | pending_schema
  value_acquisition_reference_posture: none | refs_required | B05_reference_required | split_to_C05 | split_to_C07 | donor_economy_quarantined | pending_schema
  crafting_salvage_reference_posture: none | refs_required | B06_reference_required | split_to_C12 | pending_schema
  vehicle_platform_reference_posture: none | refs_required | split_to_C08 | pending_schema
  hazard_reference_posture: none | refs_required | split_to_C09 | split_to_C03 | pending_schema
  table_oracle_reference_posture: none | refs_required | split_to_C10 | pending_schema
  map_diagram_reference_posture: none | refs_required | split_to_C13 | pending_schema
  source_local_canon_review_posture: reusable_pattern_candidate | source_local_retained | legal_ip_review_required | C14_review_required | rejected_import | quarantined
  donor_item_table_evidence_refs: [source_evidence_ref]
  donor_equipment_entry_evidence_refs: [source_evidence_ref]
  donor_tag_refs: [source_evidence_ref]
  rejected_donor_element_refs: [rejected_donor_element_ref]
  required_family_handoffs: [C01 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C12 | C13 | C14 | pending_schema]
```

C02 labels must be Astra-facing routing labels. They must avoid donor item/equipment field names as Astra labels and must not import donor item categories as Astra defaults.

## 8. Donor item-table, equipment-entry, and field-name handling

Donor item tables and donor equipment entries are evidence pressure, not Astra schema. C02 rejects donor item tables, donor equipment entries, donor field names, donor item categories, donor math, donor prices, donor rarity, donor weight/bulk/encumbrance, donor damage/armor values, donor defense values, donor charges/ammunition/durability, donor crafting costs, donor upgrade slots/hardpoints, donor item level, donor attunement, donor capacity, donor consumable counts, donor economy assumptions, and donor proper nouns as Astra defaults.

Donor exact values may be preserved only as source evidence, donor tags, source-local notes, or rejected donor elements. They must not become C02 field labels, final mechanics, final equipment math, final economy, final item statblock data, equipment table data, or accepted Astra vocabulary by appearing in a C02 record.

Donor item names, named artifacts, trademark-like labels, named materials, named factions, named locations, named technologies, named manufacturers, named cosmology, source-specific item lore, source-specific item law, and donor-world assumptions route to source-local/legal/IP/C14 review unless later canon review accepts stripped reusable patterns.

## 9. Use, custody, acquisition, value, crafting, salvage, repair, and upgrade handoffs

C02 handoffs use references and satellite records, not inheritance or merged schemas. Batch B operational files are doctrine-facing pressure only; they are not C02 schema fields.

Required Batch B handoff routing:
- C02 references B03 for item/gear/equipment/asset use procedure pressure, but B03 is not C02 schema and B03 procedure terms must not become C02 schema fields.
- C02 references B04 for inventory/storage/custody/burden procedure pressure, but B04 is not C02 schema and B04 custody/burden procedure terms must not become C02 schema fields.
- C02 references B05 for acquisition/reward/requisition/value flow procedure pressure, but B05 is not C02 schema and B05 value-flow, economy, reward, or requisition procedure terms must not become C02 schema fields.
- C02 references B06 for project/crafting/salvage/repair/upgrade procedure pressure, but B06 is not C02 schema and B06 project/crafting/salvage/repair/upgrade procedure terms must not become C02 schema fields.
- C02 may reference B01/B02 when item use appears inside scene/action resolution, but B01/B02 are not C02 schema fields.

## 10. C02 cross-family overlap rules

Required cross-family handoff routing:
- C02 -> C01 for creatures/NPCs carrying, using, owning, producing, wearing, or being associated with gear.
- C02 -> C03 for abilities, powers, techniques, passive capabilities, activated effects, item-granted effects, attack modes, defensive effects, or use-effects that require capability records.
- C02 -> C04 for relics, implants, installable assets, bonded gear, integrated assets, socketed assets, augmented gear, and host-integrated modules.
- C02 -> C05 for faction ownership, institutional control, manufacture, requisition source, legal authority, guild/institution affiliation, or restricted access.
- C02 -> C06 for item location, storage site, origin site, discovery site, or region/site association.
- C02 -> C07 for scenario/adventure/mission use, reward placement, treasure placement, clue-object placement, or scripted object role.
- C02 -> C08 for vehicle/ship/platform-mounted gear, platform components, onboard equipment, hardpoint-like attachments, cargo, and vehicle-scale tools.
- C02 -> C09 for hazardous items, unstable materials, dangerous environmental interactions, trap-like object pressure, contamination, disease-like object pressure, or volatile gear.
- C02 -> C10 for table/oracle generation of items or gear; table rows do not become C02 records unless converted with provenance.
- C02 -> C12 for recipes, blueprints, crafting patterns, salvage patterns, repair patterns, upgrade patterns, and item transformation processes.
- C02 -> C13 for map/diagram annotation references involving objects, keyed gear, object diagrams, or visual labels.
- C02 -> C14 for source-local setting, cosmology, proper nouns, named technologies, named materials, named manufacturers, source-specific item law, or donor-world assumptions.
- C02 -> pending_schema when no stable C-family owner exists.

Overlap rules:
- C02 vs C04: C02 owns ordinary gear and practical equipment. C04 owns relic/implant/installable/bonded/host-integrated special assets. If an object is both usable gear and installable special asset, split practical object evidence into C02 and installation/relic posture into C04 references.
- C02 vs C12: C02 owns the item/gear record. C12 owns recipe, salvage, repair, upgrade, or crafting process records. A recipe is not an item schema, and item stats do not become recipe fields.
- C02 vs C03: C02 owns the item object. C03 owns the granted or activated capability. Do not embed donor weapon actions, spell effects, powers, item charges, or passive effects as final C02 mechanics.
- C02 vs C08: C02 owns portable/practical gear and equipment. C08 owns vehicles, ships, platforms, stations, and large persistent conveyance/platform records. Vehicle-mounted gear should use references, not inheritance.
- C02 vs C01: C02 owns gear; C01 owns the actor carrying, using, wearing, producing, or being looted for that gear.
- C02 vs C05/B05: C02 owns the item record. C05 owns faction/institution context; B05 owns acquisition/reward/requisition/value-flow procedure. C02 must not define economy or requisition procedure.
- C02 vs C09: C02 owns the object; C09 owns hazard/environment pressure. Hazardous objects may reference C09 or C03 as applicable.
- C02 vs C14: C14 owns source-local setting, cosmology, proper nouns, source-specific materials, named technologies, and donor-world assumptions. C02 may reference them but must not generalize them.
- C02 vs C06/C07/C10/C13: use references and satellite records, not inheritance or merged schemas.

Cross-reference records must keep `inheritance_allowed: false` unless C00 later authorizes a different shared-base behavior.

## 11. Composite item/gear record handling

Composite donor constructs often combine an item, granted abilities, activation effects, charges, ammo, custody terms, prices, rarity, crafting recipes, salvage yields, repair rules, upgrade sockets, faction restrictions, location placement, vehicle mounting, hazard clauses, map labels, and source-local lore in one donor block. C02 may hold the central item/gear conversion record, but composite content must be decomposed into referenced C-family records when another owner exists.

A composite record remains C02 only when the item/gear identity is the review subject. Embedded capability lists, attack modes, defensive effects, loot placement, shop entries, requisition terms, recipe text, upgrade processes, hazard clauses, vehicle hardpoint-like assertions, map references, faction law, scenario scripts, and source-local origin claims must become refs, rejected donor elements, quarantined evidence, or pending-schema routing.

## 12. Parent, child, and satellite record handling

C02 may use parent, child, and satellite records to preserve lineage and composition without merging ownership. Parent records may represent a donor item/gear cluster, kit, set, equipment bundle, or archetype under review. Child records may represent separable components, accessories, kit contents, ordinary variants, or evidence partitions when the donor evidence requires separate conversion review. Satellite records carry C01, C03, C04, C05, C06, C07, C08, C09, C10, C12, C13, C14, or `pending_schema` material.

A C02 parent does not make child capability, relic/installable, actor, faction, location, scenario, vehicle/platform, hazard, table, recipe/process, map, or source-local records inherit C02 ownership. Use references and satellite records, not inheritance or merged schemas.

## 13. Source-local and legal/IP handling

C02 must preserve source-local and legal/IP handling from C00. Source-local identifiers, donor proper nouns, donor item names, named artifacts, named materials, named factions, named locations, named technologies, named manufacturers, trademark-like labels, license-specific expressions, verbatim-similar descriptions, protected art/map references, named cosmology, source-specific item lore, source-specific item law, and donor-world assumptions must be retained as source evidence or routed to source-local/legal/IP/C14 review.

C02 may identify a reusable practical object pattern only after stripping donor-protected expression and only as a canon-review candidate. Legal/IP posture must remain visible through provenance refs, source evidence refs, source-local boundary fields, rejected donor elements, canon eligibility, and review routing.

## 14. Rejected donor element handling

C02 must preserve rejected donor element handling. Rejected donor elements include donor item tables, donor equipment entries, donor field names, donor item categories, donor prices, donor rarity labels, donor weight/bulk/encumbrance values, donor damage/armor values, donor charges/ammunition/durability values, donor crafting costs, donor upgrade slots/hardpoints, donor economy assumptions, donor item names, donor named artifacts, donor named materials, donor named technologies, donor proper nouns, donor exact math, and donor sourcebook gear prose that cannot become Astra defaults.

Rejected material should be recorded with evidence refs, reason, owner routing, and review posture. Rejection does not delete evidence; it prevents accidental import into Astra schema, mechanics, canon, lexicon, runtime, sourcebook prose, equipment tables, economy models, shop systems, loot systems, or live-play authority.

## 15. Canon eligibility and review routing

C02 may mark canon eligibility posture from C00, but C02 never promotes canon. An item/gear conversion record may be ineligible, candidate, accepted-with-limits candidate pending review, quarantined, or rejected-import according to the C00 `canon_eligibility` structure and human/canon-review routing.

Canon review must determine whether a stripped reusable pattern, generic item classification, practical object concept, or source-local reference can move forward. C02 does not accept canon, does not define accepted lexicon, does not authorize sourcebook publication, and does not convert donor names, donor prices, donor rarity, donor damage/armor values, donor item categories, donor economy assumptions, or donor mechanics into Astra defaults.

## 16. Confidence, validation, and escalation routing

C02 records must preserve C00 confidence and validation posture for boundary confidence, extraction confidence, conversion confidence, validation status, missing-evidence flags, schema-gap routing, and escalation. Low-confidence item identity, mixed-family ownership, donor item-table ambiguity, donor field-name leakage, donor economy leakage, source-local leakage, legal/IP risk, hidden-state exposure, or missing owner coverage must route to human review, extraction repair, canon review, legal/IP review, C14, or `pending_schema` rather than improvised fields.

Validation checks should confirm C00 base inclusion, C02 classification presence, provenance refs, source evidence refs, rejected donor element handling, Batch B handoff boundaries, cross-family refs, source-local posture, canon eligibility posture, and absence of final mechanics/runtime/economy fields.

## 17. Hidden-state and protected-truth boundary

C02 may preserve that a donor item/gear record contains hidden-state or protected-truth pressure, but it must not expose protected truth as player-facing canon or runtime state. Secret functions, concealed curses, false identities, undisclosed manufacturers, hidden compartments, disguised relic posture, concealed faction ownership, trap-like surprises, source-only lore, and reveal-dependent item truths must route through C00 hidden/protected handling, canon review, scenario owners, C09/C14 owners, or runtime gates as appropriate.

C02 is allowed to record safe review labels such as hidden-state-risk or protected-truth-review-required. It must not create reveal timing, live-play disclosure rules, context-packet truth compilation, runtime hidden-information state, or runtime inventory state.

## 18. Runtime boundary

C02 forbids runtime inventory state and runtime implementation contracts. C02 must not define entity/component schemas, event schemas, command lifecycle, context packets, save-state, state deltas, database contracts, backend item schemas, runtime item IDs, runtime custody state, shop systems, loot systems, live inventory trackers, equipment slot managers, item durability trackers, ammunition counters, charge counters, economy services, or persistence models.

A C02 record may later be consumed by runtime design, but that consumption requires a separate runtime owner and review gate. Conversion-stage record grammar is not a runtime inventory model, not a runtime item model, not a database schema, and not a backend item schema.

## 19. Canon/sourcebook/live-play/training boundary

C02 is not canon acceptance, sourcebook prose, live-play behavior, or training authority. C02 does not write final gear entries, sourcebook gear tables, equipment tables, item statblocks, shop inventories, loot tables, crafting rules, repair rules, upgrade rules, GM instructions, player-facing descriptions, live-play equipment behavior, accepted lexicon entries, or training examples that override doctrine.

Examples in this file are doctrine-facing tests of routing boundaries only. They are not final content and do not authorize donor mechanics, donor names, donor prose, donor economy, donor item lore, or donor cosmology.

## 20. Missing-schema fallback

When an item/gear-like construct requires a field or owner that C02 and the known C-family handoffs cannot lawfully cover, route to `pending_schema`, quarantine, escalation, or human review. Missing schema coverage never permits improvised family-specific fields, donor format import, runtime schema invention, database contract invention, economy invention, or canon promotion.

`pending_schema` must carry provenance, source evidence, confidence, validation, rejected donor element, and source-local/legal/IP posture from C00.

## 21. Examples of good and bad C02 usage

Good C02 usage:
- Convert a donor item-like entry into a C02 item/gear record with `AstraContentRecordBase`, source evidence refs, neutral item classification, rejected donor item-table elements, and C03 refs for extracted item-granted effects.
- Preserve a named source-world artifact as source-local/C14 and C04 review while extracting only a generic practical tool pattern as a canon-review candidate.
- Split a crafting-heavy equipment entry into C02 for the item record, C12 for the recipe/process, B06 as procedure pressure, and rejected donor elements for crafting cost math.
- Record that a volatile consumable has a hazard reference posture and route contamination, trap-like object pressure, or dangerous environmental interaction to C09 rather than embedding hazard rules in C02.

Bad C02 usage:
- Copy a donor item table with price, rarity, weight, bulk, encumbrance, damage, armor, defense, charges, ammunition, durability, crafting cost, upgrade slots, hardpoints, item level, attunement, and donor item categories into Astra labels.
- Declare a donor named artifact, material, technology, faction, location, manufacturer, cosmology, or source-specific item law as Astra canon because it appeared in a C02 record.
- Define runtime inventory state, entity/component/event schemas, command lifecycle, context packets, save-state, database contracts, backend item schemas, shop systems, loot systems, or equipment slot managers in C02.
- Use C02 to write final sourcebook gear prose, final item statblocks, equipment tables, shop inventories, loot tables, economy balance, crafting procedure, live-play behavior, or accepted lexicon.

## 22. Minimum tests or assertions

Minimum C02 tests/assertions should verify:
- the C02 file exists at the registry path and contains all required sections;
- C02 declares ownership and non-ownership boundaries;
- C02 inherits/includes `AstraContentRecordBase` and preserves C00 provenance, source-local, rejected donor element, canon eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture;
- C02 doctrine grammar is doctrine-level only and not runtime, database, final item statblock, sourcebook gear prose, equipment table, donor item table, or donor schema;
- donor item tables, donor equipment entries, donor field names, donor item categories, donor math, prices, rarity, weight/bulk/encumbrance, damage/armor values, charges/ammunition/durability, crafting costs, upgrade slots/hardpoints, economy assumptions, proper nouns, and sourcebook gear prose are rejected as Astra defaults;
- Batch B handoff boundaries cover B03, B04, B05, and B06 without turning Batch B procedure into C02 schema fields;
- cross-family handoffs and overlap rules cover C01, C03, C04, C05, C06, C07, C08, C09, C10, C12, C13, C14, and `pending_schema`;
- runtime, canon, sourcebook, live-play, training, hidden-state, source-local/legal/IP, and rejected-import boundaries are preserved;
- registry posture is draft/schema-draft/designed/not_reviewed without current, stable, tested-minimum, canon, or runtime promotion.

## 23. Acceptance criteria

C02 is acceptable when:
- the file exists at `docs/doctrine/schema/C02_item_gear_record_schema.md`;
- it remains conversion-stage/canon-review schema doctrine only;
- it includes C00 base inheritance requirements;
- it does not import donor item tables, donor equipment entries, donor field labels, donor prices, donor rarity, donor damage/armor values, donor weight/bulk/encumbrance, donor charges/ammunition/durability, donor crafting costs, donor upgrade slots/hardpoints, donor economy assumptions, or donor proper nouns as Astra schema;
- it does not define final mechanics, final equipment math, economy, runtime inventory state, database schema, shop system, loot system, crafting procedure, live-play behavior, canon, sourcebook prose, or accepted lexicon;
- it has clear Batch B handoffs and cross-family handoffs;
- it includes source-local/legal/IP and rejected-import handling;
- the registry C02 posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01 registry posture is preserved and C03-C14 are not promoted;
- focused durable tests pass.

## 24. Follow-up handoff to C03

C02 explicitly hands abilities, powers, techniques, passive capabilities, activated effects, item-granted effects, attack modes, defensive effects, use-effects, and donor weapon/action/effect pressure to C03. C03 should define ability/power/technique conversion-stage record-family doctrine without inheriting C02 item schema, without importing donor weapon actions or item effect math, and without promoting item-granted mechanics to canon, sourcebook prose, live-play behavior, or runtime state.

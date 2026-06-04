# C13 Map/Diagram Record Schema Doctrine

## 1. Purpose and status

C13 defines Batch C schema-layer doctrine for conversion-stage and canon-review map, diagram, annotation, keyed area, visual dependency, route diagram, ship/station layout, tactical diagram, symbolic diagram, image-review, spatial overlay, visual evidence, and annotation-provenance records.

Status posture:
- C13 is schema-draft doctrine for record-family conversion grammar and review routing.
- C13 is not current canon, not canon geography, not final map geometry, not visual truth without review, not runtime map state, not fog-of-war state, not image generation, not OCR pipeline implementation, not GIS schema, not coordinate system doctrine, not donor map-symbol import, not sourcebook map prose, not canon promotion, and not live-play map execution.
- C13 preserves donor visual/spatial evidence for review without turning donor map assumptions into Astra defaults.

## 2. Owner layer

C13 belongs to Batch C schema doctrine under the Astra Doctrine Council - Schema Working Group. Its owner layer is Batch_C, with supporting owner layers limited to canon_review, extraction_repair, visual_review, legal/IP review, source-local review, runtime_review, and human_review when routing requires them.

C13 may reference Batch B operational files as doctrine-facing pressure boundaries, but Batch B handoff files are not C-family schema fields and do not become inherited C13 grammar.

## 3. What C13 owns

C13 owns conversion-stage record-family grammar for maps, diagrams, annotations, keyed areas, visual dependencies, route diagrams, ship/station layouts, tactical diagrams, symbolic diagrams, image-review records, spatial overlays, visual evidence records, annotation-provenance records, and similar visual/spatial evidence constructs.

C13 owns map/diagram classification and routing posture for conversion and canon review. It classifies visual/spatial evidence by conversion/review role, not by final geometry or runtime map mechanics.

C13 owns neutral Astra-facing categories such as:
- visual-evidence classification;
- visual source posture;
- annotation posture;
- key/label posture;
- spatial-abstraction posture;
- location-reference posture;
- scenario-reference posture;
- hazard-reference posture;
- vehicle/platform-reference posture;
- faction/reference posture;
- table/oracle-reference posture;
- source-local/canon-review posture;
- hidden/protected-truth posture;
- review-confidence posture;
- legal/IP posture.

## 4. What C13 must not own

C13 must not own final mechanics, final geography, canon geography, canon map truth, visual truth without review, runtime map state, runtime navigation state, runtime region state, fog-of-war state, player map state, token state, encounter map execution, tactical-grid procedure, travel procedure, exploration procedure, scene procedure, hazard procedure, GIS geometry, coordinate systems, map scale doctrine, hex-grid defaults, zone-system defaults, image generation, OCR implementation, computer vision implementation, database map schemas, backend map schemas, sourcebook map prose, live-play behavior, accepted lexicon, canon acceptance, or canon promotion.

C13 must not define final coordinates, map scale, room dimensions, grid size, hex size, token positions, route costs, movement costs, travel times, encounter layout rules, line-of-sight rules, terrain modifiers, cover values, map symbol defaults, map legend semantics, visual inference rules, OCR confidence algorithms, image-processing procedures, or geometry math.

## 5. C00 inheritance and required base posture

Every durable C13 record must inherit/include `AstraContentRecordBase` from C00 before any C13-specific classification is added. C13 preserves packet_refs, source_evidence_refs, construct_refs, outcome_refs, provenance_refs, source_local_boundary, rejected_donor_elements, canon_eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture from C00.

C13 records may not drop provenance, rejected import posture, source-local boundaries, canon eligibility routing, or validation/confidence fields to make visual material look cleaner.

## 6. Map/diagram family scope and classification

C13 family scope includes conversion-stage visual/spatial evidence constructs such as maps, diagrams, annotations, keyed areas, visual dependencies, route diagrams, ship/station layouts, tactical diagrams, symbolic diagrams, image-review records, spatial overlays, visual evidence records, annotation-provenance records, field sketches, flow diagrams, organization charts, jurisdiction overlays, and evidence sidecars.

Classification must describe the record's conversion and review function, not its final map truth. Suggested classification axes are visual-evidence classification, visual source posture, annotation posture, key/label posture, spatial-abstraction posture, location-reference posture, scenario-reference posture, hazard-reference posture, vehicle/platform-reference posture, faction/reference posture, table/oracle-reference posture, source-local/canon-review posture, hidden/protected-truth posture, review-confidence posture, and legal/IP posture.

## 7. C13 record grammar, doctrine-level only

The following block is doctrine grammar only. It is not a runtime schema, not a database schema, not GIS geometry, not a final map schema, not visual truth, not sourcebook map prose, not live map execution, and not canon geography.

```yaml
C13MapDiagramRecord:
  extends: AstraContentRecordBase
  schema_family: C13
  visual_evidence_classification: map | diagram | annotation | keyed_area | visual_dependency | route_diagram | ship_station_layout | tactical_diagram | symbolic_diagram | image_review | spatial_overlay | visual_evidence | annotation_provenance | mixed | uncertain
  visual_source_posture: extracted_image | extracted_text_reference | donor_layout_reference | manual_annotation | review_sidecar | source_local_reference | uncertain
  annotation_posture: none | donor_annotation_preserved_as_evidence | astra_review_note | split_required | rejected_import | uncertain
  key_label_posture: none | donor_key_preserved_as_evidence | label_reference_only | source_local_label | split_to_owner_family | rejected_import | uncertain
  spatial_abstraction_posture: non_geometric | relative_only | symbolic_only | route_evidence_only | layout_evidence_only | overlay_evidence_only | uncertain
  location_reference_posture: none | refs_C06 | split_to_C06 | source_local_C14_review | pending_schema
  scenario_reference_posture: none | refs_C07 | split_to_C07 | pending_schema
  hazard_reference_posture: none | refs_C09 | split_to_C09 | pending_schema
  vehicle_platform_reference_posture: none | refs_C08 | split_to_C08 | source_local_C14_review | pending_schema
  faction_reference_posture: none | refs_C05 | split_to_C05 | refs_B09_pressure | source_local_C14_review | pending_schema
  table_oracle_reference_posture: none | refs_C10 | split_to_C10 | pending_schema
  visual_review_posture: no_visual_review_needed | visual_review_required | legal_ip_review_required | canon_review_required | extraction_repair_required | quarantined
  hidden_protected_truth_posture: none | hidden_state_risk | protected_truth_risk | player_facing_risk | quarantine_required
  c13_handoff_refs: [C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C14 | pending_schema]
```

These labels are Astra-facing routing concepts only. They deliberately avoid donor map/diagram/key/symbol/layout/image field names as Astra labels.

## 8. Donor map, diagram, keyed-area, symbol, label, layout, image, and field-name handling

Donor maps, donor diagrams, donor annotations, donor keyed-area formats, donor map symbols, donor legends, donor room keys, donor coordinates, donor map scales, donor grid/hex/zone assumptions, donor layout formats, donor route diagrams, donor ship/station layouts, donor visual styles, donor field names, donor proper nouns, named locations, named regions, named worlds, named planes, named ships, named stations, named factions, protected artwork, and donor cosmology must not become Astra defaults.

Donor exact map values, keyed labels, room numbers, map scales, coordinates, grid sizes, hex sizes, room dimensions, route lines, travel times, terrain symbols, hazard symbols, faction icons, legend keys, ship deck labels, station layout labels, annotation fields, visual styles, and symbol meanings may be preserved only as source evidence, donor tags, source-local notes, visual-review notes, or rejected donor elements, not as Astra schema labels or final mechanics.

Donor map names, named locations, named regions, named worlds, named planes, named ships, named stations, named factions, named gods, named landmarks, named cosmology, source-specific map symbols, source-specific visual style, source-specific map prose, protected artwork, and source-specific lore must route to source-local/legal/IP/C14 review unless canon review later accepts stripped reusable patterns.

## 9. Location, scenario, hazard, vehicle/platform, faction, table, source-local, and visual-review handoffs

Batch B handoffs:
- C13 references B08 when maps/diagrams concern travel, exploration, navigation, route diagrams, discovery routes, region traversal, site entry, or spatial discovery pressure, but B08 is not C13 schema.
- C13 references B01 when maps/diagrams support scene/activity/encounter context, keyed areas, tactical diagrams, or encounter-space evidence, but B01 is not C13 schema.
- C13 references B10 when maps/diagrams show hazards, opposition zones, trap pressure, environmental danger, active threat locations, exposure zones, or dangerous terrain, but B10 is not C13 schema.
- C13 may reference B02 when a diagram affects action declaration, cost commitment, resolution trigger, positioning pressure, or visual decision context, but B02 is not C13 schema.
- C13 may reference B09 when visual evidence shows faction territories, jurisdictions, social diagrams, institution layouts, route restrictions, or organization charts, but B09 is not C13 schema.
- Batch B procedure terms must not become C13 schema fields.

Family handoffs must use refs, split records, or satellite records. They must not import procedure fields, final mechanics, donor layout fields, or owner-family schema into C13.

## 10. C13 cross-family overlap rules

- C13 vs C06: C13 owns map/diagram annotation and visual/spatial evidence. C06 owns location/site/region records. A map is evidence or annotation, not canon geography.
- C13 vs C07: C13 owns visual scenario evidence. C07 owns mission/scenario/adventure structure. A keyed adventure map may require C13 visual evidence plus C06 place records plus C07 scenario structure.
- C13 vs C09: C13 owns visual evidence of hazard placement or hazard zones. C09 owns hazard/environment pressure.
- C13 vs C08: C13 owns visual layout evidence for ships, vehicles, stations, platforms, bases, and mechs. C08 owns the vehicle/ship/platform record.
- C13 vs C05/B09: C13 owns visual faction/institution evidence such as jurisdiction maps or organization charts. C05 owns faction/institution records; B09 owns social/faction/contact procedure.
- C13 vs C10: C13 owns the visual evidence or diagram annotation. C10 owns tables/oracles/generators, including map/key/generator tables and row provenance.
- C13 vs C14: C14 owns source-local cosmology, proper nouns, named worlds, named planes, named regions, source-specific map lore, source-specific symbols, protected artwork, and donor-world assumptions. C13 may preserve and reference them but must not generalize them.
- C13 vs runtime/backend: C13 records conversion-stage visual evidence and routing. Runtime/backend owners decide later whether anything becomes map state, navigation graph, fog-of-war state, token layer, save-state node, image asset, or database row.
- C13 vs live-play/sourcebook: C13 is not player-facing map presentation, not sourcebook map layout, not tactical map execution, not GM map script, and not live-play visual state.
- C13 vs image/OCR/CV pipeline: C13 may route to visual review and preserve visual evidence posture, but it does not define OCR, computer vision, image extraction, image generation, coordinate extraction, or visual truth algorithms.
- C13 vs C01/C02/C03/C04/C11/C12: C13 may reference visual evidence for actors, objects, abilities, relics, companions, and crafting/salvage diagrams, but those records keep their own family ownership.

Cross-family handoff list:
- C13 -> C01 for creature/NPC placement evidence, actor icons, monster markers, NPC portraits used as evidence, encounter positions, lair occupants, or visual actor dependencies.
- C13 -> C02 for item/gear/cache/treasure/object placement evidence, object diagrams, equipment diagrams, symbolized loot, tool diagrams, or visual item dependencies.
- C13 -> C03 for area-of-effect diagrams, ritual diagrams, ability diagrams, power geometry evidence, technique diagrams, aura overlays, or visual effect dependencies.
- C13 -> C04 for relic diagrams, implant diagrams, installable asset diagrams, bonded-object diagrams, module diagrams, augmentation schematics, or visual special-asset dependencies.
- C13 -> C05 for faction maps, jurisdiction diagrams, organization charts, heraldry/insignia diagrams, territory overlays, social diagrams, or institutional visual evidence.
- C13 -> C06 for locations, sites, regions, keyed areas, route maps, spatial containers, worlds, planes, stations, ruins, megastructures, settlements, and place-like records.
- C13 -> C07 for mission/scenario/adventure maps, keyed adventure sites, clue diagrams, tactical diagrams, puzzle diagrams, route overlays, scenario diagrams, and visual scenario evidence.
- C13 -> C08 for vehicle/ship/platform layouts, deck plans, station diagrams, mech diagrams, base layouts, hardpoint diagrams, cargo diagrams, and platform-scale spatial evidence.
- C13 -> C09 for hazard zones, trap diagrams, environmental overlays, weather fronts, exposure areas, dangerous terrain, affliction spread diagrams, and region pressure overlays.
- C13 -> C10 for map tables, keyed-area tables, diagram keys, random map generators, route generator tables, symbol tables, visual oracle tables, or diagram-dependent generators.
- C13 -> C11 for companion/summon placement, pet lairs, cohort positions, minion formations, summon diagrams, follower maps, or relationship-control visual evidence.
- C13 -> C12 for crafting schematics, salvage diagrams, recipe diagrams, repair schematics, upgrade diagrams, material extraction maps, workshop layouts, or process visuals.
- C13 -> C14 for source-local setting, cosmology, named worlds, named planes, named regions, named locations, named ships/stations, source-specific visual symbols, protected map art, donor-world assumptions, source-specific map lore, and proper nouns.
- C13 -> pending_schema when no stable C-family owner exists.

Use references and satellite records, not inheritance or merged schemas.

## 11. Composite map/diagram record handling

Composite map/diagram records may preserve a donor visual construct that contains multiple kinds of evidence, such as a keyed adventure map with rooms, hazards, monsters, loot, faction territory, and route arrows. C13 may hold the composite visual evidence posture while satellite records route place evidence to C06, scenario evidence to C07, hazard evidence to C09, actor evidence to C01, item evidence to C02, and source-local names or protected art to C14.

Composite handling must not collapse all visual contents into a single C13 truth record. C13 is the evidence and annotation wrapper, not the owner of every thing depicted.

## 12. Parent, child, and satellite record handling

C13 may use parent, child, and satellite records to preserve lineage and composition without merging ownership. Parent records may represent a map plate, diagram page, route overview, ship layout spread, or annotation cluster. Child records may represent separable visual panels, keyed subareas, overlay layers, legend evidence, or annotation provenance partitions. Satellite records carry C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C14, or `pending_schema` material.

Parent/child/satellite links must retain provenance_refs, source_evidence_refs, rejected_donor_elements, and cross-reference relation notes from C00.

## 13. Source-local and legal/IP handling

C13 must preserve source-local and legal/IP handling for donor visual material. Donor map names, source-specific map prose, setting names, named worlds, named planes, named regions, named locations, named ships/stations, named factions, named gods, named landmarks, donor cosmology, source-specific visual symbols, source-specific visual style, protected artwork, trade dress, and license-specific expressions require source-local/legal/IP/C14 review unless canon review explicitly accepts stripped reusable patterns.

C13 may store protected art/map references only as source evidence references, visual-review notes, or rejected donor elements. It must not reproduce protected artwork as an Astra schema default or assert visual truth from protected artwork without review.

## 14. Rejected donor element handling

Rejected donor element handling is mandatory when donor visual material cannot be safely converted. Rejected donor elements include donor maps, donor diagrams, donor annotations, donor keyed-area formats, donor map symbols, donor legends, donor room keys, donor coordinates, donor map scales, donor grid/hex/zone assumptions, donor layout formats, donor route diagrams, donor ship/station layouts, donor visual styles, donor field names, donor proper nouns, protected artwork, donor cosmology, and donor source-specific visual meanings.

Rejected material should be recorded as `rejected_import`, rejected_donor_elements, source-local notes, legal/IP notes, or visual-review notes with evidence references and a reason. Rejection is routing, not deletion of provenance.

## 15. Canon eligibility and review routing

C13 preserves canon eligibility and review routing without canon promotion. A C13 record may become a canon_candidate only when provenance is adequate, donor leakage is controlled, source-local/legal/IP issues are routed, owner-family handoffs are complete, and visual review has not identified protected truth or visual truth risk.

C13 never promotes canon, does not accept canon, and does not create canon geography. Canon review may later accept stripped reusable visual/spatial patterns, but C13 itself remains a conversion-stage/canon-review schema doctrine file.

## 16. Confidence, validation, and escalation routing

C13 confidence and validation signals must cover boundary confidence, extraction confidence, conversion confidence, visual review confidence, source-local confidence, legal/IP confidence, and owner-handoff confidence. Low or blocked confidence routes to visual_review, extraction_repair, source-local review, legal/IP review, C14 review, runtime_review, or human_review.

Escalate when extraction damage obscures map keys, visual labels are ambiguous, donor field names are embedded in the layout, a map asserts hidden truth, protected artwork may be copied, source-local proper nouns dominate, coordinates or scale appear mechanically meaningful, or no stable C-family owner exists.

## 17. Hidden-state and protected-truth boundary

C13 must preserve hidden-state and protected-truth boundary language. A map, GM diagram, secret route, concealed room, hidden hazard zone, fogged region, unrevealed token position, or false map clue is not player-facing truth merely because it appears in donor visual material.

Protected truth must remain protected. Hidden-state risk, player-facing risk, visual truth without review, and source-local secret context must route through protected-truth posture, canon review, and runtime_review as appropriate.

## 18. Runtime boundary

C13 forbids runtime map state, runtime navigation state, runtime region state, fog-of-war state, player map state, token state, encounter map execution, live map execution, navigation graphs, save-state map nodes, image asset database rows, entity/component/event schemas, command lifecycle, context packets, backend map schemas, GIS geometry, OCR implementation, computer vision implementation, coordinate extraction, image generation, and visual truth algorithms.

Runtime/backend owners decide later whether reviewed C13 evidence informs map state, navigation graph, fog-of-war state, token layer, save-state node, image asset, database row, backend map schema, entity/component/event schema, command lifecycle, context packet, or live map execution. C13 does not define those systems.

## 19. Canon/sourcebook/live-play/training boundary

C13 is not canon geography, not canon map truth, not sourcebook map prose, not player-facing map presentation, not sourcebook map layout, not tactical map execution, not GM map script, not live-play visual state, and not training example authority.

Training examples may test routing posture but must not become accepted lexicon, final geometry, sourcebook prose, live-play behavior, or canon promotion.

## 20. Missing-schema fallback

When a map/diagram element has no stable C-family owner, C13 routes that element to `pending_schema` while preserving provenance, source evidence, rejected donor element posture, confidence, and escalation notes. Missing-schema fallback must not cause C13 to absorb unrelated ownership permanently.

## 21. Examples of good and bad C13 usage

Good C13 usage:
- Preserve a donor dungeon map as visual evidence with keyed labels retained only as source evidence, then route place records to C06 and scenario structure to C07.
- Preserve a route diagram for travel/exploration review, reference B08 pressure, and avoid creating route costs, travel times, or navigation graph nodes.
- Preserve a ship/station layout as visual layout evidence, route platform ownership to C08, and route named ship/station lore or protected art to C14/legal/IP review.
- Preserve a hazard overlay as C13 visual evidence while routing hazard pressure to C09 and active threat procedure pressure to B10.
- Preserve a faction jurisdiction map or organization chart as visual evidence while routing faction/institution ownership to C05 and social/faction procedure pressure to B09.

Bad C13 usage:
- Convert donor coordinates, map scales, grid sizes, hex sizes, room dimensions, room numbers, route lines, legend keys, or donor field names into Astra schema labels or final mechanics.
- Treat donor map art, donor map symbols, protected artwork, source-specific visual style, named locations, named regions, named worlds, named planes, named ships, named stations, named factions, proper nouns, or donor cosmology as Astra defaults.
- Use visual evidence as visual truth without review or as canon geography.
- Turn a tactical diagram into encounter map execution, token state, fog-of-war state, line-of-sight rules, terrain modifiers, or cover values.
- Implement OCR, computer vision, coordinate extraction, image generation, GIS geometry, backend map schemas, database map schemas, or live map execution in C13.

## 22. Minimum tests or assertions

Minimum C13 tests assert that:
- the C13 file exists at `docs/doctrine/schema/C13_map_diagram_record_schema.md`;
- all required sections are present;
- C13 declares ownership and non-ownership;
- C13 inherit/include `AstraContentRecordBase` and preserves C00 provenance posture;
- C13 doctrine grammar is doctrine-level only and not runtime/database/GIS/final-map/visual-truth/sourcebook-map/live-map-execution/canon-geography schema;
- donor map, diagram, keyed-area, symbol, layout, field-name, proper-noun, protected-art, and cosmology leakage is rejected;
- B08, B01, B10, B02, and B09 are handoff references only and Batch B procedure terms must not become C13 schema fields;
- cross-family handoffs cover C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C14, and `pending_schema`;
- runtime, canon, sourcebook, live-play, hidden-state, legal/IP, and rejected-import boundaries are preserved;
- registry C13 posture is draft/schema-draft/designed/not_reviewed without promotion.

## 23. Acceptance criteria

C13 is accepted as draft doctrine when:
- C13 file exists at the exact registry path;
- C13 remains conversion-stage/canon-review schema doctrine only;
- C13 includes C00 base inheritance requirements;
- C13 does not import donor maps, diagrams, keyed-area formats, map symbols, legends, room keys, coordinates, map scales, grid/hex/zone assumptions, route diagrams, ship/station layouts, visual styles, field labels, proper nouns, protected artwork, named locations/regions/worlds/planes/ships/stations/factions, or cosmology as Astra schema;
- C13 does not define final map geometry, canon geography, visual truth, runtime map state, fog-of-war state, token state, database schema, GIS geometry, OCR/computer-vision implementation, image generation, live map execution, sourcebook map prose, canon, or accepted lexicon;
- C13 has clear Batch B handoffs and cross-family handoffs;
- C13 includes source-local/legal/IP and rejected-import handling;
- C13 registry posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum.

## 24. Follow-up handoff to C14

C13 hands source-local setting, cosmology, named worlds, named planes, named regions, named locations, named ships/stations, source-specific visual symbols, protected map art, donor-world assumptions, source-specific map lore, proper nouns, donor gods, named landmarks, and protected artwork to C14/source-local/legal/IP review.

C14 review may later determine whether stripped reusable visual/spatial patterns can survive without donor-world leakage. Until that review completes, C13 preserves such material only as evidence, source-local boundary, visual-review note, rejected donor element, or cross-reference.

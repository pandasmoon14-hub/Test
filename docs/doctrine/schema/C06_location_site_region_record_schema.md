# C06 Location/Site/Region Record Schema Doctrine

## 1. Purpose and status

C06 defines Batch C conversion-stage and canon-review schema doctrine for location, site, region, world, plane, station, ruin, megastructure, settlement, biome, route context, keyed area, spatial container, place-like construct, and similar location-like records. It exists to preserve place evidence and route review without letting donor map formats, keyed-area formats, gazetteer prose, planar-location assumptions, or source-specific geography become Astra defaults.

Status posture:
- C06 is a schema-draft doctrine file.
- C06 is not current canon, not runtime-ready, not stable_for_family, not stable_cross_family, and not tested_minimum.
- C06 records are conversion-stage/canon-review artifacts; they are not final geography, canon map truth, canon geography, accepted setting geography, runtime map state, runtime navigation state, runtime region state, sourcebook gazetteer prose, travel procedure, exploration procedure, scene procedure, environmental hazard mechanics, canon promotion, or donor map/location-format import.
- C06 does not accept canon, does not promote canon, does not define accepted lexicon, and does not decide live-play behavior.

## 2. Owner layer

Owner layer: Batch_C schema family doctrine.

C06 supports conversion intake, conversion output, canon review, legal/IP review, C14 source-local review, Batch B handoff review, C13 map/diagram review, and later runtime/backend review. Batch B operational files remain doctrine-facing pressure only; they are not C06 schema fields and are not inherited by C06 records.

## 3. What C06 owns

C06 owns conversion-stage record-family grammar for:
- locations;
- sites;
- regions;
- worlds;
- planes;
- stations;
- ruins;
- megastructures;
- settlements;
- biomes;
- route contexts;
- keyed areas;
- spatial containers;
- place-like constructs;
- donor constructs that behave like location/site/region evidence even when the source uses a map key, gazetteer entry, planar note, travel route, or adventure location.

C06 owns location/site/region classification and routing posture for conversion and canon review. It records how a place-like construct was identified, what scale/scope posture applies, what boundary posture applies, what spatial-abstraction posture applies, what access/navigation posture exists, what contents/reference posture exists, what hazard/environment reference posture exists, what faction/institution reference posture exists, what scenario/adventure reference posture exists, what map/diagram reference posture exists, what source-local/cosmology reference posture applies, what canon-review posture applies, what hidden/protected-truth posture applies, and what legal/IP posture applies.

C06 owns the place-like conversion record and its routing evidence. C06 does not automatically own creatures, items, hazards, maps, factions, missions, vehicles, tables, source-local cosmology, or runtime state associated with that place.

## 4. What C06 must not own

C06 must not own or define:
- final mechanics;
- final geography;
- canon map truth;
- canon geography;
- accepted setting geography;
- sourcebook gazetteer prose;
- runtime map state;
- runtime navigation state;
- runtime region state;
- fog-of-war state;
- travel procedure;
- exploration procedure;
- discovery procedure;
- scene procedure;
- encounter procedure;
- hazard mechanics;
- environmental damage mechanics;
- faction control mechanics;
- settlement economy;
- route generation;
- database map schemas;
- GIS-like geometry;
- coordinate systems;
- hex-grid defaults;
- zone system defaults;
- keyed-map execution;
- live-play behavior;
- accepted lexicon;
- canon acceptance;
- canon promotion;
- final coordinates, hex sizes, map scale, room dimensions, travel speeds, distances, encounter rates, keyed-room numbers as Astra defaults, route costs, region modifiers, exploration DCs, navigation DCs, random encounter schedules, resource drain rates, settlement economy values, faction-control values, planar mechanics, environmental damage, or geography math.

C06 does not own final settlement rules, final route rules, final planar rules, final map scale, final map symbols, final room dimensions, final travel time math, final encounter frequency, or final region modifiers. Those details may be preserved as source evidence, donor tags, rejected donor elements, or handoff notes only.

## 5. C00 inheritance and required base posture

Every durable C06 record must inherit/include `AstraContentRecordBase` from C00 before any C06-specific shaping. C06 preserves C00 packet_refs, source_evidence_refs, construct_refs, outcome_refs, provenance_refs, source_local_boundary, rejected_donor_elements, canon_eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture.

C06 records must keep the C00 distinction between source evidence, conversion classification, rejected donor elements, source-local boundaries, canon eligibility, validation status, lineage, parent/child records, satellite records, and cross-reference records. C06 cannot drop provenance merely because a donor map, keyed area, gazetteer entry, planar location, settlement note, or route description appears familiar or easy to generalize.

## 6. Location/site/region family scope and classification

C06 classifies location/site/region records by conversion/review role, not by final map mechanics. Neutral Astra-facing classification may include:
- location classification posture;
- scale/scope posture;
- boundary posture;
- spatial-abstraction posture;
- access/navigation posture;
- contents/reference posture;
- hazard/environment reference posture;
- faction/institution reference posture;
- scenario/adventure reference posture;
- map/diagram reference posture;
- source-local/cosmology reference posture;
- canon-review posture;
- hidden/protected-truth posture;
- legal/IP posture.

These categories are routing concepts only. They do not define final coordinates, hex sizes, map scale, room dimensions, travel speeds, distances, encounter rates, keyed-room numbers, route costs, region modifiers, exploration DCs, navigation DCs, random encounter schedules, resource drain rates, settlement economy values, faction-control values, planar mechanics, environmental damage, geography math, or executable exploration behavior.

## 7. C06 record grammar, doctrine-level only

The following YAML-like block is doctrine grammar only. It is not a runtime schema, not a database schema, not a map schema, not GIS geometry, not final geography, not sourcebook gazetteer prose, not keyed-map execution, and not canon geography.

```yaml
C06LocationSiteRegionRecord:
  extends: AstraContentRecordBase
  schema_family: C06
  location_classification_posture: location | site | region | world | plane | station | ruin | megastructure | settlement | biome | route_context | keyed_area | spatial_container | place_like | mixed | uncertain
  scale_scope_posture: point_like | site_scale | settlement_scale | route_scale | regional_scale | world_scale | planar_scale | nested | abstract | source_local | uncertain
  boundary_posture: explicit_donor_boundary | implied_boundary | functional_boundary | narrative_boundary | map_evidence_boundary | no_safe_boundary | uncertain
  spatial_abstraction_posture: textual_evidence_only | diagram_referenced | map_referenced | keyed_area_referenced | route_referenced | coordinate_evidence_quarantined | abstracted | uncertain
  access_navigation_posture: no_access_pressure | b08_handoff_required | route_context_required | site_entry_pressure | traversal_pressure | discovery_pressure | source_local_only | uncertain
  contents_reference_posture: none | c01_refs | c02_refs | c03_refs | c04_refs | c11_refs | c12_refs | mixed_refs | pending_schema
  hazard_environment_reference_posture: none | c09_refs_required | b10_trigger_pressure | source_local_only | uncertain
  faction_institution_reference_posture: none | c05_refs_required | b09_handoff_required | source_local_only | uncertain
  scenario_adventure_reference_posture: none | c07_refs_required | b01_context_required | source_local_only | uncertain
  map_diagram_reference_posture: none | c13_refs_required | visual_evidence_only | donor_key_quarantined | uncertain
  source_local_cosmology_reference_posture: none | c14_review_required | legal_ip_review_required | source_local_boundary_required | rejected_import_required | uncertain
  canon_review_posture: not_eligible | eligible_for_pattern_review | source_local_only | requires_human_review | blocked
  hidden_protected_truth_posture: public_evidence | hidden_evidence | protected_truth | spoiler_sensitive | false_or_unreliable_source | uncertain
  required_batch_b_handoffs: [B01 | B02 | B05 | B08 | B09 | B10]
  required_family_handoffs: [C01 | C02 | C03 | C04 | C05 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema]
  donor_location_field_handling: preserve_as_source_evidence | donor_tag_only | rejected_donor_element | source_local_boundary | legal_ip_review
```

The C06LocationSiteRegionRecord shape avoids donor map/location/gazetteer field names as Astra labels. It uses review posture, reference posture, and handoff posture so conversion can preserve evidence without importing donor coordinates, donor map scales, donor keyed-room numbers, donor travel math, donor planar traits, or donor gazetteer categories.

## 8. Donor map, keyed-area, gazetteer, planar-location, region, and field-name handling

Donor maps, donor map formats, donor gazetteer formats, donor keyed-area formats, donor room keys, donor exact map values, donor coordinates, donor keyed labels, donor room numbers, donor map scales, donor distances, donor travel times, donor encounter rates, donor region modifiers, donor hex sizes, donor hex/zone assumptions, donor zone structures, donor planar traits, donor gazetteer categories, donor keyed-area fields, donor field names, donor proper nouns, named worlds, named planes, named regions, named cities, and donor cosmology must not become Astra defaults.

These donor elements may be preserved only as source evidence, donor tags, source-local boundary notes, legal/IP review notes, or rejected donor elements. They must not become Astra schema labels, final mechanics, final geography, canon geography, accepted setting geography, runtime navigation state, or map execution rules.

Donor location names, named worlds, named planes, named regions, named cities, named ruins, named megastructures, named landmarks, named factions, named gods, named cosmology, named planar laws, named source-specific metaphysics, source-specific geography, source-specific map prose, source-specific lore, and source-specific gazetteer categories must route to source-local/legal/IP/C14 review unless canon review later accepts stripped reusable patterns.

## 9. Travel, exploration, scene, faction, hazard, map, scenario, and source-local handoffs

C06 references B08 for travel, exploration, navigation, discovery, route, region traversal, site entry, movement, and discovery pressure, but B08 is not C06 schema.

C06 references B01 when a location/site/region is used as scene/activity/encounter context, but B01 is not C06 schema.

C06 references B10 when a location contains hazard/opposition/contact/active threat trigger pressure, but B10 is not C06 schema.

C06 references B09 when a place has social/faction/contact/institutional pressure, settlement control, jurisdiction, reputation, or institutional ownership pressure, but B09 is not C06 schema.

C06 may reference B05 when a location is tied to acquisition/reward/requisition/value flow, shops, markets, caches, resource sites, or treasure placement pressure, but B05 is not C06 schema.

C06 may reference B02 when location pressure affects action declaration, cost commitment, or resolution trigger pressure, but B02 is not C06 schema.

C06 routes map/diagram/keyed-map evidence to C13, mission/scenario/adventure use to C07, hazard/environment pressure to C09, and source-local/cosmology/legal/IP pressure to C14 and legal review. Batch B procedure terms must not become C06 schema fields.

## 10. C06 cross-family overlap rules

Required cross-family handoffs:
- C06 -> C01 for creatures/NPCs inhabiting, guarding, controlling, originating from, or associated with a location.
- C06 -> C02 for items/gear/equipment/caches/treasure/tools/material objects located in, stored at, discovered in, or associated with a place.
- C06 -> C03 for location-bound abilities, site effects, regional powers, terrain-linked techniques, rituals, wards, auras, or domain/place-tied capabilities.
- C06 -> C04 for relics, implants, installable assets, bound structures, site-integrated assets, station modules, ruin-integrated assets, or place-bound special assets.
- C06 -> C05 for factions, institutions, settlements, authorities, jurisdictions, organizations, claims, ownership, governance, social control, or institutional presence.
- C06 -> C07 for mission/scenario/adventure use, keyed adventure sites, quest locations, scripted site roles, route objectives, or adventure-path placement.
- C06 -> C08 for vehicle/ship/platform/station/megastructure overlaps, mobile locations, platform-scale places, shipboard spaces, bases, and persistent conveyance sites.
- C06 -> C09 for hazards, environments, weather, region pressure, terrain pressure, planar conditions, exposure pressure, afflictions, trap-like pressure, or environmental danger located in a place.
- C06 -> C10 for table/oracle/generator rows that produce, select, or vary locations, routes, keyed areas, discoveries, weather zones, site features, or travel complications.
- C06 -> C11 for companion/summon habitats, lairs, stables, sanctums, bonded places, pet/summon origin sites, or companion-controlled locations.
- C06 -> C12 for crafting/salvage/recipe sites, resource nodes, workshops, repair yards, salvage fields, material sources, upgrade sites, or dangerous extraction sites.
- C06 -> C13 for map/diagram annotation, keyed maps, visual labels, room diagrams, spatial overlays, region diagrams, route maps, or site schematics.
- C06 -> C14 for source-local setting, cosmology, named worlds, named planes, named regions, named cities, named cultures, named gods, source-specific geography, source-specific metaphysics, planar laws, or donor-world assumptions.
- C06 -> pending_schema when no stable C-family owner exists.

Overlap rules:
- C06 vs C13: C06 owns the location/site/region record. C13 owns map/diagram annotation and visual/spatial evidence. A map is evidence or annotation, not canon geography.
- C06 vs C09: C06 owns place identity and boundary posture. C09 owns hazard/environment pressure. A hazardous region uses references, not inheritance.
- C06 vs C07: C06 owns the place/site/region. C07 owns mission/scenario/adventure structure, scripted use, and adventure function.
- C06 vs C14: C14 owns source-local cosmology, setting law, proper nouns, named worlds, named planes, source-specific metaphysics, and donor-world assumptions. C06 may reference them but must not generalize them.
- C06 vs C08: C06 owns place-like records; C08 owns vehicles, ships, platforms, stations, mechs, bases, and persistent platform records. A station/megastructure/mobile site may require C06/C08 split by primary identity and function.
- C06 vs C05/B09: C06 owns the place. C05 owns faction/institution; B09 owns social/faction/contact procedure. Governance or settlement authority does not become C06 mechanics.
- C06 vs C10/B08: C06 owns converted location records. C10 owns table/oracle generation of places; B08 owns travel/exploration/discovery procedure. A travel table row is not a C06 record until converted with provenance.
- C06 vs C01/C02/C03/C04/C11/C12: C06 may reference inhabitants, contents, site effects, assets, companions, and resource/crafting sites, but those records keep their own family ownership; use references and satellite records, not inheritance or merged schemas.
- C06 vs runtime/backend: C06 records conversion-stage location evidence and routing. Runtime/backend owners decide later whether any location becomes map state, navigation graph, save-state node, or database row.
- C06 vs Batch A cosmology/world/domain owners: C06 records place-like conversion pressure and routing; final cosmology, planar rules, geography canon, domain metaphysics, environmental mechanics, and world law remain with proper doctrine/canon owners.
- C06 vs B01/B02/B08/B10: C06 records location identity/routing; B01 owns scene/activity/encounter procedure, B02 owns action/cost/resolution trigger procedure, B08 owns travel/exploration/discovery procedure, and B10 owns active threat trigger procedure.

## 11. Composite location/site/region record handling

Composite donor entries often mix place identity, map evidence, keyed-room text, inhabitants, hazards, factions, treasure, site effects, adventure objectives, route instructions, planar lore, and gazetteer prose. C06 may create a parent location/site/region record to preserve the place-like conversion anchor while routing each non-C06 element to the correct family or Batch B handoff.

Composite records must use references and satellite records, not inheritance or merged schemas. A ruin with guardians, traps, treasure, a mission hook, a map key, and a named god keeps its C06 place record separate from C01 guardians, C09 hazard pressure, C02 contents, C07 adventure use, C13 map/diagram annotation, and C14 source-local named theology.

## 12. Parent, child, and satellite record handling

C06 may use parent, child, and satellite records to preserve lineage and composition without merging ownership. Parent records may represent a donor region, world, plane, megastructure, settlement, route corridor, ruin complex, or site cluster under review. Child records may represent separable sub-sites, districts, rooms-as-evidence, landmarks, route segments, nested regions, station sections, biomes, or keyed areas when donor evidence requires separate conversion review.

Satellite records carry C01, C02, C03, C04, C05, C07, C08, C09, C10, C11, C12, C13, C14, Batch B, or `pending_schema` material. Parent/child/satellite structure preserves provenance and review routing; it does not create final geography, runtime map hierarchy, keyed-map execution, or canon map truth.

## 13. Source-local and legal/IP handling

C06 must preserve source-local and legal/IP handling for donor location prose, donor map art references, protected art/map references, license-specific expressions, verbatim-similar descriptions, donor proper nouns, named worlds, named planes, named regions, named cities, named cultures, named gods, named cosmology, named planar laws, source-specific geography, source-specific metaphysics, source-specific map prose, and source-specific lore.

Such material routes to source-local/legal/IP/C14 review. C06 may retain source-local evidence as provenance or source_local_boundary context, but C06 must not strip protected expression into canon geography, accepted setting geography, accepted lexicon, or sourcebook gazetteer prose without later review by the proper owners.

## 14. Rejected donor element handling

Rejected donor elements include donor maps, donor map formats, donor gazetteer formats, donor keyed-area formats, donor room keys, donor coordinates, donor map scales, donor distances, donor travel times, donor encounter rates, donor region modifiers, donor hex/zone assumptions, donor planar traits, donor field names, donor proper nouns, source-specific geography, source-specific cosmology, donor keyed-map execution rules, and donor source-specific map prose that cannot safely become Astra-facing schema.

Rejected donor elements should be recorded in C00 rejected_donor_elements or equivalent rejected_import posture with source evidence refs and an explanation. Rejection preserves auditability; it does not authorize silent import, canon promotion, or runtime implementation.

## 15. Canon eligibility and review routing

C06 canon eligibility is a review signal only. C06 may mark stripped reusable place patterns as eligible_for_pattern_review, source_local_only, requires_human_review, blocked, or not_eligible, but C06 never promotes canon, does not accept canon, does not create canon map truth, and does not define accepted setting geography.

Named donor geography, donor cosmology, named worlds, named planes, named regions, named cities, donor-world assumptions, and source-specific metaphysics normally route to C14/source-local/legal/IP review. A reusable pattern can be canon-review eligible only after donor expression, protected names, donor map math, and donor cosmology have been stripped or quarantined.

## 16. Confidence, validation, and escalation routing

C06 confidence and validation fields inherit C00 posture. Low or blocked confidence must escalate when source evidence is ambiguous, a donor map and prose conflict, a keyed area cannot be safely separated from donor formatting, a named place appears source-local, a planar trait implies donor cosmology, a region modifier implies final mechanics, or a place overlaps C07/C08/C09/C13/C14 ownership.

Validation checks should confirm that C06 record grammar remains doctrine-level only, provenance is present, rejected donor elements are tracked, source-local boundaries are preserved, Batch B procedure terms are not converted into schema fields, and cross-family handoffs use references rather than inheritance.

## 17. Hidden-state and protected-truth boundary

C06 may record hidden-state and protected-truth boundary posture as review metadata when a place contains secret doors, hidden routes, concealed sites, unrevealed region truth, fog-like uncertainty, unreliable maps, spoiler-sensitive locations, false geography, hidden factions, dormant hazards, or protected truth. That posture is not runtime hidden-information state.

Protected truth remains evidence and review routing. C06 must not reveal it as public canon, turn it into fog-of-war state, build live map execution, or define discovery procedure. B08 handles discovery pressure, B01 handles scene context, B10 handles active threat trigger pressure, C13 handles map/diagram evidence, and runtime/backend owners decide later whether any hidden information becomes executable state.

## 18. Runtime boundary

C06 forbids runtime map state, runtime navigation state, runtime region state, fog-of-war state, location database rows, navigation graphs, save-state map nodes, GIS geometry, entity/component/event schemas, command lifecycle, context packets, backend map schemas, travel trackers, exploration trackers, and live map execution.

C06 records conversion-stage location evidence and routing only. Runtime/backend owners decide later whether any converted place becomes map state, a navigation graph, a save-state node, a location database row, a backend map schema, a context packet input, an entity/component/event schema participant, a travel tracker entry, an exploration tracker entry, or live map execution behavior. C06 must not pre-commit those choices.

## 19. Canon/sourcebook/live-play/training boundary

C06 is not canon/sourcebook/live-play/training authority. It does not produce canon geography, accepted setting geography, sourcebook gazetteer prose, live-play map execution, GM revelation procedure, player-facing travel procedure, exploration procedure, scene procedure, encounter procedure, hazard procedure, or training examples as schema authority.

Training examples may illustrate conversion posture, but training examples do not become C06 schema fields, final geography, accepted lexicon, canon map truth, or runtime behavior.

## 20. Missing-schema fallback

When a location-like donor construct includes material that lacks a stable C-family owner, C06 routes the unresolved portion to `pending_schema` with provenance, source evidence, rejected donor element posture when needed, and escalation notes. C06 must not fill another family gap by defining faction schema, mission schema, vehicle schema, map schema, cosmology schema, runtime schema, or Batch B procedure.

## 21. Examples of good and bad C06 usage

Good C06 usage:
- Preserve a donor ruin as a C06 location/site/region record with source evidence, boundary posture, C13 map/diagram refs, C01 guardian refs, C09 hazard refs, C02 cache refs, B08 site-entry pressure, and C14 review for named gods or source-specific lore.
- Preserve a route context as C06 place-like evidence with B08 travel/exploration/navigation/discovery handoff notes while rejecting donor travel times, donor distances, donor encounter rates, and donor hex/zone assumptions as Astra defaults.
- Preserve a settlement as C06 place identity with C05 faction/institution refs and B09 social/faction/contact/institutional pressure, without importing donor settlement economy values, faction-control values, jurisdiction mechanics, or sourcebook gazetteer prose.
- Preserve a named plane as source-local C06/C14 evidence while rejecting donor planar traits, donor cosmology, named planar laws, and source-specific metaphysics as Astra defaults.

Bad C06 usage:
- Convert donor coordinates, donor map scales, donor room keys, keyed-room numbers, hex sizes, zone structures, travel times, distances, encounter rates, region modifiers, or planar traits into Astra default fields.
- Treat a donor map as canon geography or runtime map state.
- Use donor map/location/gazetteer/keyed-area field names as C06 schema labels.
- Turn a keyed adventure site into C07 mission/scenario/adventure structure inside C06.
- Turn a hazardous region into C09 hazard/environment mechanics inside C06.
- Turn settlement control, reputation, shops, markets, or economy into C06 mechanics.
- Promote named worlds, named planes, named regions, named cities, donor cosmology, donor proper nouns, or source-specific geography into canon without C14/source-local/legal/IP review.

## 22. Minimum tests or assertions

Minimum C06 tests should assert that:
- the C06 file exists at the registry path;
- all required sections are present;
- C06 declares ownership and non-ownership boundaries;
- C06 inherit/include `AstraContentRecordBase` and uses `extends: AstraContentRecordBase` in doctrine grammar;
- doctrine grammar is not a runtime schema, not a database schema, not a map schema, not GIS geometry, not final geography, not sourcebook gazetteer prose, not keyed-map execution, and not canon geography;
- donor map, donor location, donor gazetteer, donor keyed-area, donor planar, donor field-name, donor proper-noun, and donor cosmology leakage is rejected as Astra defaults;
- B08, B01, B10, B09, B05, and B02 handoff boundaries are present without Batch B procedure terms becoming C06 schema fields;
- C01, C02, C03, C04, C05, C07, C08, C09, C10, C11, C12, C13, C14, and `pending_schema` handoffs are present;
- runtime, canon, sourcebook, live-play, training, source-local, legal/IP, hidden-state, protected-truth, rejected-import, and missing-schema boundaries are present;
- registry C06 posture is draft/schema-draft/designed/not_reviewed without current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum promotion.

## 23. Acceptance criteria

C06 is acceptable when:
- C06 file exists at `docs/doctrine/schema/C06_location_site_region_record_schema.md`;
- C06 remains conversion-stage/canon-review schema doctrine only;
- C06 includes C00 base inheritance requirements;
- C06 does not import donor maps, donor keyed-area formats, donor room keys, map scales, coordinates, hex/zone assumptions, travel times, encounter rates, region modifiers, planar traits, field labels, proper nouns, named worlds/planes/regions/cities, or cosmology as Astra schema;
- C06 does not define final geography, canon geography, runtime map state, runtime navigation state, database schema, GIS geometry, travel procedure, exploration procedure, scene procedure, hazard procedure, live-play map execution, canon, sourcebook gazetteer prose, or accepted lexicon;
- C06 has clear Batch B handoffs and cross-family handoffs;
- C06 includes source-local/legal/IP and rejected-import handling;
- C06 registry posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01/C02/C03/C09/C10 registry posture is preserved;
- C04, C05, C07, C08, and C11-C14 are not promoted;
- focused tests pass;
- full suite passes.

## 24. Follow-up handoff to C07

C06 follow-up pressure to C07 is explicit because location/site/region records frequently become mission sites, adventure locations, keyed adventure sites, quest locations, scripted site roles, route objectives, or adventure-path placements. C06 owns the place-like record, but C07 must own mission/scenario/adventure structure, scripted use, objective placement, scene-chain function, adventure consequences, and adventure-path logic.

Until C07 is drafted, mission/scenario/adventure use attached to locations should be routed to C07 as the expected owner or to `pending_schema` if ownership cannot be safely assigned. C06 must not fill the C07 gap by defining adventure schema, quest procedure, scene-chain structure, scripted encounter use, or canon event placement.

# C09 Hazard/Environment Record Schema Doctrine

## 1. Purpose and status

C09 defines Batch C schema-layer doctrine for hazard/environment conversion-stage records. It gives canon review a focused record-family grammar for hazards, environments, weather, region pressure, terrain pressure, planar conditions, afflictions, exposure records, contamination, disease-like pressure, poison-like pressure, radiation-like pressure, corruption-like pressure, trap-like pressure, unstable material pressure, ambient danger, and environmental-danger constructs.

Status posture:
- C09 is schema-draft material, not current canon.
- C09 records are conversion-stage and canon-review artifacts.
- C09 is not final damage mechanics, not condition math, not runtime hazard state, not environmental truth canon, not weather simulation, not trap procedure, not sourcebook hazard prose, not canon promotion, and not donor hazard/trap/environment-table import.
- C09 never promotes canon, does not accept canon, and does not create accepted lexicon.

## 2. Owner layer

C09 belongs to Batch_C schema doctrine and the Astra Doctrine Council - Schema Working Group. Its owner layer is conversion/canon-review schema doctrine only. Batch A mechanics, Batch B operational procedure, runtime/backend, live-play, canon/sourcebook, lexicon, and training/evaluation layers remain separate owner layers.

## 3. What C09 owns

C09 owns conversion-stage record-family grammar for hazards, environments, weather, region pressure, terrain pressure, planar conditions, afflictions, exposure records, contamination, disease-like pressure, poison-like pressure, radiation-like pressure, corruption-like pressure, trap-like pressure, unstable material pressure, ambient danger, and similar hazard/environment constructs.

C09 owns hazard/environment classification and routing posture for conversion and canon review. It may preserve donor evidence about dangerous terrain, hostile atmosphere, exposure pressure, disease-like pressure, poison-like pressure, contamination, corruption-like pressure, radiation-like pressure, unstable materials, trap-like pressure, planar conditions, weather pressure, and region-scale environmental danger as evidence and routing signals.

C09 owns the decision that a converted construct is primarily hazard/environment pressure rather than a creature, item, ability, location, scenario, platform, table/oracle, companion, crafting process, map annotation, source-local setting element, or pending schema issue.

## 4. What C09 must not own

C09 must not own final mechanics, final damage math, condition math, exposure math, trap procedure, travel procedure, exploration procedure, action procedure, hazard trigger procedure, weather simulation, environmental canon truth, encounter balance, runtime damage resolution, runtime hazard instances, runtime environmental state, runtime region state, runtime affliction trackers, entity/component schemas, event schemas, command lifecycle, context packets, save-state, database contracts, sourcebook hazard prose, accepted lexicon, canon acceptance, canon promotion, or live-play behavior.

C09 must not define final numerical values, damage dice, damage thresholds, save DCs, difficulty DCs, condition severities, exposure intervals, travel speeds, weather probabilities, regional modifiers, trap attack bonuses, recharge values, duration counts, disease stages, poison stages, corruption stages, radiation doses, or hazard math.

C09 must not import donor hazards, donor traps, donor hazard tables, donor weather tables, donor environmental tables, donor field names, donor damage math, donor condition math, donor save DCs, donor difficulty DCs, donor exposure intervals, donor weather probabilities, donor terrain modifiers, donor disease/poison/corruption/radiation stages, donor trigger procedures, donor proper nouns, or donor cosmology as Astra defaults.

## 5. C00 inheritance and required base posture

Every C09 record must inherit/include `AstraContentRecordBase` from C00 before any C09-specific doctrine grammar is considered. C09 preserves C00 packet_refs, source_evidence_refs, construct_refs, outcome_refs, provenance_refs, source_local_boundary, rejected_donor_elements, canon_eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture.

C09 keeps C00's provenance lock: donor exact values may be preserved only as source evidence, donor tags, or rejected donor elements, not as Astra schema labels or final mechanics. Cross-family references must keep `inheritance_allowed: false` unless a later C00-controlled registry process changes the shared rule.

## 6. Hazard/environment family scope and classification

C09 classifies hazard/environment records by conversion/review role, not by final mechanics. Neutral Astra-facing categories include:
- hazard classification posture;
- environmental scale posture;
- contact/exposure posture;
- trigger posture;
- source/origin posture;
- location/reference posture;
- actor/item/ability interface posture;
- damage/condition reference posture;
- duration/persistence reference posture;
- travel/exploration reference posture;
- hidden/protected-truth posture;
- source-local/canon-review posture;
- legal/IP posture.

These categories are routing concepts. They are not damage tables, not condition tables, not weather probability tables, not exposure math, not trap statblocks, and not environmental canon truth.

## 7. C09 record grammar, doctrine-level only

The following YAML-like block is doctrine grammar only. It is not a runtime schema, not a database schema, not a final hazard statblock, not a trap statblock, not a weather simulation, not a damage/condition table, not sourcebook hazard prose, and not a donor record format.

```yaml
C09HazardEnvironmentRecord:
  extends: AstraContentRecordBase
  schema_family: C09
  hazard_classification_posture: ambient_pressure | contact_pressure | exposure_pressure | trigger_pressure | terrain_pressure | weather_pressure | region_pressure | planar_condition_pressure | affliction_pressure | contamination_pressure | trap_like_pressure | unstable_material_pressure | pending_schema
  environmental_scale_posture: localized | site_zone | route_or_region | platform_linked | actor_linked | item_linked | ability_linked | source_local | pending_schema
  contact_exposure_posture: no_contact_claim | contact_refs_required | exposure_refs_required | affliction_refs_required | source_evidence_only | pending_schema
  trigger_posture: passive_pressure | contact_trigger_refs | active_threat_trigger_refs | procedure_refs_required | source_evidence_only | pending_schema
  source_origin_posture: naturalistic | technological | magical_or_supernatural | biological | corruption_like | radiation_like | poison_like | disease_like | source_local | unknown
  location_reference_posture: no_location_ref | C06_ref_required | C08_ref_required | C13_ref_required | source_local_location_ref | pending_schema
  actor_item_ability_interface_posture: no_interface | C01_ref_required | C02_ref_required | C03_ref_required | C04_ref_required | C11_ref_required | C12_ref_required | pending_schema
  damage_condition_reference_posture: no_final_math | damage_owner_refs_required | condition_owner_refs_required | resource_owner_refs_required | rejected_donor_math_present | pending_schema
  duration_persistence_reference_posture: instant_evidence_only | persistent_pressure_refs_required | timeline_refs_required | rejected_donor_duration_present | pending_schema
  travel_exploration_reference_posture: no_travel_pressure | B08_refs_required | C06_route_refs_required | C07_scenario_refs_required | pending_schema
  hidden_protected_truth_posture: public_construct | gm_secret_evidence | hidden_trigger_evidence | protected_truth_ref_required | source_local_secret | pending_schema
  source_local_canon_review_posture: reusable_pattern_candidate | source_local_only | C14_review_required | legal_ip_review_required | rejected_import | quarantined
  required_family_handoffs: [C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C10 | C11 | C12 | C13 | C14 | pending_schema]
```

C09 labels are neutral Astra-facing posture labels. They intentionally avoid donor hazard/trap/environment/weather field names as Astra labels. They record classification and routing, not final values.

## 8. Donor hazard, trap, environmental table, weather, affliction, and field-name handling

Donor hazards, donor traps, donor hazard tables, donor weather tables, donor environmental tables, donor affliction entries, donor field names, donor damage math, donor condition math, donor save DCs, donor difficulty DCs, donor exposure intervals, donor weather probabilities, donor terrain modifiers, donor disease/poison/corruption/radiation stages, donor trigger procedures, donor proper nouns, and donor cosmology are not Astra defaults.

Donor exact values may be retained only in `source_evidence_refs`, donor tags, or `rejected_donor_elements`. C09 prevents accidental import of donor field names, donor final mechanics, donor table rows, donor statblock labels, donor trap labels, donor weather-system labels, and donor environmental-rule labels into Astra schema vocabulary.

Donor hazard names, trap names, named planes, named regions, named weather systems, named diseases, named poisons, named magical effects, named environmental rules, named cosmology, named source-specific metaphysics, source-specific lore, and source-specific environmental laws route to source-local/legal/IP/C14 review unless canon review later accepts stripped reusable patterns.

## 9. Contact, exposure, trigger, travel, location, damage, condition, and effect handoffs

C09 references B10 for hazard/opposition/contact/active threat trigger pressure, but B10 is not C09 schema. C09 references B08 for travel/exploration/navigation/discovery pressure, but B08 is not C09 schema. C09 references B01 when hazard pressure appears inside scene/activity/encounter structure, but B01 is not C09 schema. C09 references B02 when hazard pressure affects action declaration, cost commitment, or resolution trigger pressure, but B02 is not C09 schema. C09 may reference B03 when item/gear/asset use creates, contains, resists, or channels a hazard, but B03 is not C09 schema.

Batch B procedure terms must not become C09 schema fields. Batch B handoff files are doctrine-facing pressure only, not C-family schema inheritance. Contact, exposure, trigger, travel, location, damage, condition, duration, effect, resource, mitigation, resistance, vulnerability, and recovery details are routed to their proper family or owner references.

## 10. C09 cross-family overlap rules

Required cross-family handoffs:
- C09 -> C01 for creatures/NPCs that produce, suffer, carry, embody, trigger, or are associated with hazards.
- C09 -> C02 for hazardous items, unstable materials, contaminated gear, trap-like objects, protective equipment, or object-mediated hazards.
- C09 -> C03 for abilities, powers, techniques, aura-like effects, environmental powers, disease/poison/radiation/corruption effects, or hazard-generating capabilities.
- C09 -> C04 for relic/implant/installable hazards, cursed/bonded/installed dangerous assets, cyberware/biotech complications, or host-integrated hazardous assets.
- C09 -> C05 for faction/institutional hazard ownership, legal containment, quarantine authority, environmental regulation, institutional disaster response, or faction-controlled hazard zones.
- C09 -> C06 for location, site, region, terrain, route, biome, domain, lair, weather zone, planar zone, or environmental placement.
- C09 -> C07 for scenario/adventure/mission use, hazard placement, scripted hazard role, timed danger, puzzle trap role, disaster scenario, or adventure-path hazard function.
- C09 -> C08 for vehicle/ship/platform hazards, onboard hazards, platform environmental pressure, ship/mech system danger, vacuum/pressure/hull breach pressure, or platform-scale hazardous environments.
- C09 -> C10 for table/oracle generation of hazards, weather, exposure events, travel complications, environmental shifts, trap results, or affliction outcomes; table rows do not become C09 records unless converted with provenance.
- C09 -> C11 for companion/summon hazard interactions, pet afflictions, summon-created hazards, minion-carried contamination, or control-linked hazard pressure.
- C09 -> C12 for crafting/salvage/recipe processes involving hazardous materials, contamination handling, volatile salvage, unsafe repair, dangerous upgrades, or hazard mitigation recipes.
- C09 -> C13 for map/diagram annotation references involving hazard zones, trap diagrams, exposure areas, weather fronts, region pressure overlays, or environmental labels.
- C09 -> C14 for source-local setting, cosmology, named planes, named regions, named environmental laws, named diseases/poisons, named materials, named magic systems, source-specific metaphysics, source-specific planar laws, or donor-world assumptions.
- C09 -> pending_schema when no stable C-family owner exists.

Explicit overlap rules:
- C09 vs C06: C09 owns hazard/environment pressure. C06 owns the place/site/region. A hazardous region uses C06 for location identity and C09 for pressure; neither inherits the other.
- C09 vs C03: C09 owns hazard/environment pressure. C03 owns the ability/effect/capability that creates, modifies, resists, or interacts with it.
- C09 vs C02: C09 owns hazard pressure. C02 owns the item/object. Hazardous objects split object record and hazard record.
- C09 vs C01: C09 owns hazard/environment pressure. C01 owns the creature/NPC actor that produces, carries, suffers, or triggers it.
- C09 vs C10: C09 owns a converted hazard/environment construct. C10 owns the table/oracle/generator that may produce or select such constructs. A table row is not a C09 record until converted with provenance.
- C09 vs C08: C09 owns hazard/environment pressure. C08 owns the vehicle/ship/platform. Vehicle/platform hazard pressure uses references, not inheritance.
- C09 vs C07: C09 owns hazard/environment construct. C07 owns scenario placement, mission structure, timing, and adventure function.
- C09 vs C14: C14 owns source-local cosmology, planar law, proper nouns, source-specific environmental metaphysics, named afflictions, and donor-world assumptions. C09 may reference them but must not generalize them.
- C09 vs B10/B08/B02: C09 records hazard/environment identity and routing; B10 owns active threat trigger procedure, B08 owns exploration/travel procedure, and B02 owns action/cost/resolution trigger procedure.
- C09 vs Batch A damage/condition/resource owners: C09 records conversion-stage hazard family and routing; final damage families, conditions, resistance/vulnerability, exposure costs, recharge, backlash, and effect math remain with proper A/B/future mechanics owners.
- C09 vs C04/C05/C11/C12/C13: use references and satellite records, not inheritance or merged schemas.

Cross-family references do not make the target family inherit C09 grammar. A C09 cross-reference record should use `inheritance_allowed: false` and should describe why the related family owns its own slice.

## 11. Composite hazard/environment record handling

Composite donor constructs often combine hazard pressure, place identity, creature source, item container, ability origin, relic host, faction containment, scenario timing, vehicle/platform environment, table generation, companion carrier, crafting material, map label, damage math, condition math, exposure math, duration, trigger procedure, weather roll, disease stage, poison stage, radiation dose, corruption track, and source-local lore in one donor block.

C09 may hold the central hazard/environment conversion record only when the hazard/environment pressure is the review subject. Embedded actors, item objects, ability sources, relic/installable assets, faction authorities, locations, scenario scripts, platforms, table/oracle rows, companions, crafting processes, maps, named cosmology, final mechanics, and donor prose must become refs, rejected donor elements, quarantined evidence, or pending-schema routing.

## 12. Parent, child, and satellite record handling

C09 may use parent, child, and satellite records to preserve lineage and composition without merging ownership. Parent records may represent a donor hazard/environment cluster, weather package, exposure family, affliction group, contamination pattern, unstable-material family, trap-like pressure cluster, or regional pressure set under review. Child records may represent separable modes, zones, exposure channels, origin variants, persistence variants, hidden-trigger evidence, or rejected donor evidence partitions.

Satellite records carry C01, C02, C03, C04, C05, C06, C07, C08, C10, C11, C12, C13, C14, or `pending_schema` material. A C09 parent does not make child actor, item, ability, relic, faction, location, scenario, vehicle/platform, table, companion, crafting, map, or source-local records inherit C09 ownership. Use references and satellite records, not inheritance or merged schemas.

## 13. Source-local and legal/IP handling

C09 must preserve source-local and legal/IP handling from C00. Source-local identifiers, donor hazard names, trap names, named planes, named regions, named weather systems, named diseases, named poisons, named magical effects, named environmental rules, named cosmology, named source-specific metaphysics, source-specific planar laws, source-specific lore, named materials, named magic systems, donor-world assumptions, license-specific expressions, verbatim-similar descriptions, protected art/map references, and source-specific environmental prose must be retained as source evidence or routed to source-local/legal/IP/C14 review.

C09 may identify a reusable hazard/environment pressure pattern only after stripping donor-protected expression and only as a canon-review candidate. Legal/IP posture must remain visible through provenance refs, source evidence refs, source-local boundary fields, rejected donor elements, canon eligibility, and review routing.

## 14. Rejected donor element handling

C09 must preserve rejected donor element handling. Rejected donor elements include donor hazards, donor traps, donor hazard tables, donor weather tables, donor environmental tables, donor affliction stages, donor field names, donor damage math, donor condition math, donor save DCs, donor difficulty DCs, donor exposure intervals, donor weather probabilities, donor terrain modifiers, donor disease/poison/corruption/radiation stages, donor trigger procedures, donor damage dice, donor thresholds, donor travel speeds, donor regional modifiers, donor trap attack bonuses, donor recharge values, donor duration counts, donor radiation doses, donor hazard math, donor proper nouns, donor cosmology, and donor sourcebook hazard prose that cannot become Astra defaults.

Rejected donor element records prevent accidental import by preserving evidence, explaining why the element is not an Astra default, and routing any reusable stripped pattern to human/canon/legal review.

## 15. Canon eligibility and review routing

C09 preserves C00 canon_eligibility. A C09 record may be a reusable pattern candidate, source-local only, C14 review required, legal/IP review required, rejected_import, or quarantined. C09 never promotes canon, does not accept canon, and does not mark a hazard/environment construct as canon truth.

Canon review must evaluate whether stripped, provenance-bearing hazard/environment pressure can become Astra-native content. Donor names, proper nouns, cosmology, named planes, named regions, named diseases, named poisons, named environmental laws, exact mechanics, and sourcebook prose remain non-canon unless the appropriate owner accepts them later.

## 16. Confidence, validation, and escalation routing

C09 preserves C00 confidence, validation, lineage, composition, and escalation routing. Low confidence, conflicting evidence, unsupported donor fields, missing provenance, cross-family ambiguity, legal/IP risk, source-local cosmology, hidden protected truth, or pressure requiring final mechanics must escalate to human review, extraction repair, C14 review, Batch A/B owner review, runtime review, or `pending_schema`.

Validation checks should confirm that C09 records keep conversion-stage classification separate from runtime behavior, final mechanics, accepted lexicon, canon truth, and donor record formats.

## 17. Hidden-state and protected-truth boundary

C09 may record that a hazard/environment entry contains hidden-state and protected-truth boundary concerns, such as hidden triggers, concealed contamination, secret source-local origin, unrevealed planar law, hidden disease vector, hidden trap-like pressure, or GM-secret environmental evidence. C09 must not expose protected truth or decide what live players know.

Protected truth must remain in source evidence, source-local boundary, hidden/protected-truth posture, or review refs. C09 does not create hidden-information runtime state or reveal procedure.

## 18. Runtime boundary

C09 runtime boundary is strict. C09 must not define runtime hazard instances, runtime environmental state, runtime region state, runtime affliction trackers, runtime damage resolution, entity/component schemas, event schemas, command lifecycle, context packets, save-state, database contracts, backend hazard schemas, weather simulation systems, combat trackers, travel trackers, trap execution, exposure clocks, condition trackers, or live-play resolution.

C09 records may reference that such runtime/backend concerns exist, but all implementation, persistence, simulation, event, command, tracker, and context-packet decisions route outside C09.

## 19. Canon/sourcebook/live-play/training boundary

C09 is not canon/sourcebook/live-play/training authority. It does not write sourcebook hazard prose, weather prose, trap prose, environmental prose, affliction prose, disease prose, poison prose, radiation prose, corruption prose, map prose, boxed text, or GM procedure.

C09 never promotes canon, does not accept canon, does not define live-play behavior, does not define training examples as schema authority, and does not create an accepted lexicon. Examples in this file are doctrine-facing illustrations only.

## 20. Missing-schema fallback

When hazard/environment evidence does not fit C09 or any stable C-family owner, route it to `pending_schema` with provenance, source evidence, rejected donor elements where needed, confidence notes, and review escalation. Do not force unsupported donor fields into C09 labels.

When a missing owner appears to be a future mechanics, runtime, condition, damage, resource, map, event, entity/component, command lifecycle, save-state, database, weather simulation, combat tracker, travel tracker, or canon/sourcebook concern, C09 records only the handoff and keeps the unsupported material out of C09 grammar.

## 21. Examples of good and bad C09 usage

Good C09 usage:
- Convert a donor hazard-like entry into a C09 conversion record that classifies ambient danger, exposure posture, location refs, rejected donor damage dice, and C14 review for named cosmology without final mechanics.
- Record that a contaminated region uses C06 for location identity and C09 for contamination pressure, with donor exposure intervals preserved only as evidence or rejected donor elements.
- Route a trap-like pressure to C09 for hazard identity, B10 for active threat trigger pressure, C02 for the object, and C07 for scenario placement.
- Preserve a named disease as source-local/legal/IP/C14 review while retaining a stripped reusable affliction-pressure pattern as canon-review candidate.

Bad C09 usage:
- Copy a donor hazard table, trap statblock, weather table, environmental table, disease stage table, poison stage table, radiation dose table, or corruption track as Astra schema.
- Convert donor save DCs, difficulty DCs, exposure intervals, weather probabilities, terrain modifiers, trap attack bonuses, damage dice, damage thresholds, duration counts, or final condition severities into C09 mechanics.
- Treat a named plane, named region, named weather system, named disease, named poison, named cosmology, or named environmental law as Astra canon.
- Use C09 to define runtime damage resolution, runtime hazard instances, weather simulation systems, combat trackers, travel trackers, database contracts, or live-play behavior.

## 22. Minimum tests or assertions

Minimum C09 tests should assert that:
- the C09 file exists at the registry path;
- required sections are present;
- C09 owns hazard/environment conversion-stage record-family grammar and rejects non-owner boundaries;
- C09 must inherit/include `AstraContentRecordBase` and preserve C00 provenance, source-local, rejected donor, canon eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture;
- C09 record grammar is doctrine grammar only and not runtime, database, final statblock, weather simulation, damage/condition table, or sourcebook hazard prose;
- donor hazards, traps, tables, field names, damage/condition math, DCs, exposure intervals, weather probabilities, disease/poison/corruption/radiation stages, proper nouns, and cosmology are rejected as Astra defaults;
- B10, B08, B01, B02, and B03 are handoffs only;
- cross-family handoffs and overlap rules cover C01, C02, C03, C04, C05, C06, C07, C08, C10, C11, C12, C13, C14, and `pending_schema`;
- runtime, canon, sourcebook, live-play, hidden-state, legal/IP, and rejected donor boundaries are preserved;
- the C09 registry posture is draft/schema-draft/designed/not_reviewed without current, canon, runtime, stable, or tested promotion.

## 23. Acceptance criteria

C09 is acceptable when:
- C09 exists at `docs/doctrine/schema/C09_hazard_environment_record_schema.md`;
- C09 remains conversion-stage/canon-review schema doctrine only;
- C09 includes C00 base inheritance requirements;
- C09 does not import donor hazards, traps, hazard tables, weather tables, environmental tables, field labels, damage math, condition math, DCs, exposure intervals, trigger procedures, weather probabilities, disease/poison/corruption/radiation stages, proper nouns, or cosmology as Astra schema;
- C09 does not define final mechanics, damage resolution, condition math, environmental canon truth, weather simulation, trap procedure, travel procedure, action procedure, runtime hazard state, database schema, combat tracker, travel tracker, live-play behavior, canon, sourcebook prose, or accepted lexicon;
- C09 has clear Batch B handoffs and cross-family handoffs;
- C09 includes source-local/legal/IP and rejected-import handling;
- C09 registry posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01/C02/C03 registry posture is preserved;
- C04-C08 and C10-C14 are not promoted;
- focused tests pass and full suite passes.

## 24. Follow-up handoff to C10

C09 hands table/oracle/generator pressure to C10. C10 should define how tables, oracles, random generators, weather generators, exposure event selectors, environmental shift tables, travel complication tables, trap result tables, and affliction outcome tables are converted as their own record family.

C10 is not C09 schema. A table row is not a C09 record until converted with provenance, C00 base posture, source evidence, rejected donor element handling, and an explicit C09 classification/routing decision.

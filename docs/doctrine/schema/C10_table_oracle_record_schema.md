# C10 Table/Oracle Record Schema Doctrine

## 1. Purpose and status

C10 defines Batch C conversion-stage and canon-review schema doctrine for table, oracle, generator, random-roll list, weighted option list, result family, prompt list, keyed result list, table-row provenance, procedural-selection evidence, and similar table/oracle/generation constructs. It exists to preserve evidence and route work without letting donor table formats or random-generation assumptions become Astra defaults.

Status posture:
- C10 is a schema-draft doctrine file.
- C10 is not current canon, not runtime-ready, not stable_for_family, not stable_cross_family, and not tested_minimum.
- C10 records are conversion-stage/canon-review artifacts; they are not final mechanics, runtime random generation, database table schema, encounter generator implementation, loot generator implementation, sourcebook table prose, canon promotion, or donor table-format import.
- C10 does not accept canon, does not promote canon, does not define accepted lexicon, and does not decide live-play behavior.

## 2. Owner layer

Owner layer: Batch_C schema family doctrine.

C10 supports conversion intake, conversion output, canon review, legal/IP review, C14 source-local review, Batch B handoff review, and later runtime/backend review. Batch B operational files remain doctrine-facing pressure only; they are not C10 schema fields and are not inherited by C10 records.

## 3. What C10 owns

C10 owns conversion-stage record-family grammar for:
- tables;
- oracles;
- generators;
- random-roll lists;
- weighted option lists;
- prompt lists;
- keyed result lists;
- result families;
- table-row provenance;
- procedural-selection evidence;
- donor constructs that behave like table/oracle/generation evidence even when the source does not call them a table.

C10 owns table/oracle classification and routing posture for conversion and canon review. It records how a donor table-like construct was identified, what selection structure evidence exists, what row structure evidence exists, what weighting/range evidence posture exists, what output-family reference posture applies, what row provenance posture exists, whether instantiation is implied by donor text, whether recurrence/reuse is implied, whether hidden/protected-result handling is needed, whether source-local/canon-review routing is required, and what legal/IP posture applies.

C10 owns the table/oracle/generator container and its row provenance. C10 does not automatically own the content-family record produced by a table row.

## 4. What C10 must not own

C10 must not own or define:
- final mechanics;
- final random-generation procedure;
- runtime random selection;
- runtime encounter generation;
- runtime loot generation;
- runtime oracle state;
- probability math;
- reward economy;
- encounter balance;
- table execution;
- procedural content generation implementation;
- database table schemas;
- sourcebook table prose;
- accepted lexicon;
- canon acceptance;
- canon promotion;
- live-play behavior;
- final numerical roll ranges, probability curves, encounter frequencies, loot frequencies, reward values, rarity weights, DCs, table execution rules, random seed behavior, oracle interpretation rules, die size defaults, d100 defaults, d20 defaults, d66 defaults, card draw defaults, replacement rules, reroll rules, or procedural generation algorithms.

C10 does not own the content-family record produced by a table row. A row that points to a creature routes to C01; item/gear to C02; ability/effect to C03; relic/installable asset to C04; faction/institution to C05; location/site/region to C06; mission/scenario/adventure to C07; vehicle/ship/platform to C08; hazard/environment to C09; companion/summon to C11; crafting/salvage/recipe to C12; map/diagram annotation to C13; source-local setting/cosmology to C14; and unknown output to `pending_schema`.

## 5. C00 inheritance and required base posture

Every durable C10 record must inherit/include `AstraContentRecordBase` from C00 before any C10-specific shaping. C10 preserves C00 packet_refs, source_evidence_refs, construct_refs, outcome_refs, provenance_refs, source_local_boundary, rejected_donor_elements, canon_eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture.

C10 records must keep the C00 distinction between source evidence, conversion classification, rejected donor elements, source-local boundaries, canon eligibility, validation status, lineage, parent/child records, satellite records, and cross-reference records. C10 cannot drop provenance merely because a donor table row appears compact, numerical, repeated, or familiar.

## 6. Table/oracle family scope and classification

C10 classifies table/oracle records by conversion/review role, not by final mechanics. Neutral Astra-facing classification may include:
- table/oracle classification posture;
- selection structure posture;
- row structure posture;
- weighting/range evidence posture;
- output-family reference posture;
- row provenance posture;
- instantiation posture;
- recurrence/reuse posture;
- hidden/protected-result posture;
- source-local/canon-review posture;
- legal/IP posture.

These categories are routing concepts only. They do not define final random tables, die defaults, probability curves, encounter rates, loot rates, reward values, oracle interpretation rules, or executable generator behavior.

## 7. C10 record grammar, doctrine-level only

The following YAML-like block is doctrine grammar only. It is not a runtime schema, not a database schema, not a final random generator, not an executable oracle, not an encounter table implementation, not a loot table implementation, not a final roll procedure, and not sourcebook table prose.

```yaml
C10TableOracleRecord:
  extends: AstraContentRecordBase
  schema_family: C10
  table_oracle_classification: table | oracle | generator | random_roll_list | weighted_option_list | prompt_list | keyed_result_list | result_family | procedural_selection_evidence | mixed | uncertain
  selection_structure_posture: explicit_donor_evidence | implied_donor_evidence | flattened_rows | prose_prompt_sequence | keyed_reference_list | uncertain | rejected_import
  row_structure_posture: row_evidence_preserved | row_group_preserved | keyed_result_evidence_preserved | prompt_evidence_preserved | mixed_rows | no_rows | uncertain
  weighting_range_evidence_posture: source_evidence_only | rejected_donor_element | stripped_pattern_candidate | absent | uncertain
  output_family_reference_posture: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C11 | C12 | C13 | C14 | pending_schema | mixed | none | uncertain
  row_provenance_posture: per_row_provenance_required | grouped_row_provenance_required | table_level_only_with_escalation | insufficient_provenance
  instantiation_posture: selection_evidence_only | may_point_to_content_record | source_local_instance_only | canon_review_required | runtime_review_required | uncertain
  recurrence_reuse_posture: one_time_prompt | reusable_table_like_construct | source_local_repeat_only | donor_procedure_only | uncertain
  hidden_protected_result_posture: none_detected | hidden_result_evidence | protected_truth_evidence | source_local_secret | escalate
  routing_notes: string
```

C10-specific names above are Astra-facing classification and routing concepts. They must not copy donor table/oracle/generator field names as Astra labels.

## 8. Donor table, oracle, generator, roll-range, weighting, row, and field-name handling

Donor exact table ranges, donor roll ranges, donor weights, donor probabilities, donor row labels, donor die sizes, donor row formatting, donor column headers, donor result names, donor procedural instructions, donor table execution rules, donor procedural generation assumptions, donor field names, and donor random-roll lists may be preserved only as source evidence, donor tags, or rejected donor elements. They must not become Astra schema labels, Astra defaults, final mechanics, or accepted lexicon.

C10 rejects donor tables, donor oracles, donor generators, donor random-roll lists, donor roll ranges, donor d100 defaults, donor d20 defaults, donor d66 defaults, donor card-draw defaults, donor row formatting, donor column headers, donor weights/probabilities, donor encounter frequencies, donor loot frequencies, donor reward values, donor table execution rules, donor procedural generation assumptions, donor field names, donor proper nouns, and donor cosmology as Astra defaults.

Donor table names, result names, named factions, named places, named creatures, named items, named spells, named hazards, named cosmology, named generators, source-specific prompt phrasing, and source-specific lore must route to source-local/legal/IP/C14 review unless canon review later accepts stripped reusable patterns.

## 9. Random selection, instantiation, reward, travel, social, hazard, and scenario handoffs

C10 records selection evidence and routing; C10 does not execute random selection or instantiate runtime outcomes.

Required Batch B handoffs:
- C10 references B05 when tables/oracles concern acquisition, reward, requisition, value flow, treasure, loot, payment, cost, or item availability pressure, but B05 is not C10 schema.
- C10 references B08 when tables/oracles concern travel, exploration, navigation, discovery, route events, wilderness complications, space travel, hex crawling, or discovery pressure, but B08 is not C10 schema.
- C10 references B09 when tables/oracles concern social contact, faction response, institution behavior, reputation, patron, contact, rumor, or negotiation pressure, but B09 is not C10 schema.
- C10 references B10 when tables/oracles concern hazards, opposition contact, active threat triggers, encounter pressure, environmental danger, trap pressure, or affliction outcomes, but B10 is not C10 schema.
- C10 may reference B01 when table/oracle output structures scene/activity/encounter selection, but B01 is not C10 schema.
- C10 may reference B02 when table/oracle output modifies action declaration, cost commitment, or resolution trigger pressure, but B02 is not C10 schema.

Batch B procedure terms must not become C10 schema fields. Reward, travel, social, hazard, encounter, scenario, action, and activity pressures remain handoff signals, not inherited C10 fields.

## 10. C10 cross-family overlap rules

Required cross-family handoffs:
- C10 -> C01 for creature/NPC/monster/adversary/NPC-contact rows or generators.
- C10 -> C02 for item/gear/loot/equipment/consumable/tool rows or generators.
- C10 -> C03 for ability/power/technique/effect/spell-like/maneuver rows or generators.
- C10 -> C04 for relic/implant/installable/augment/bonded asset rows or generators.
- C10 -> C05 for faction/institution/contact/patron/organization/reputation rows or generators.
- C10 -> C06 for location/site/region/route/biome/domain/place rows or generators.
- C10 -> C07 for mission/scenario/adventure/hook/quest/event-structure rows or generators.
- C10 -> C08 for vehicle/ship/platform/mech/base/station/cargo-platform rows or generators.
- C10 -> C09 for hazard/environment/weather/trap/affliction/exposure/disaster rows or generators.
- C10 -> C11 for companion/summon/pet/follower/cohort/minion rows or generators.
- C10 -> C12 for crafting/salvage/recipe/repair/upgrade/material-process rows or generators.
- C10 -> C13 for map/diagram annotation/keyed-area/spatial-label/visual-reference rows or generators.
- C10 -> C14 for source-local setting, cosmology, named worlds, named planes, named factions, named places, named gods, source-specific lore, source-specific prompt language, or donor-world assumptions.
- C10 -> pending_schema when no stable C-family owner exists.

Explicit overlap handling:
- C10 vs C01: C10 owns the table/oracle/generator and row provenance; C01 owns the converted creature/NPC record. A creature row is not a C01 record until converted with provenance.
- C10 vs C02: C10 owns item-table structure and row provenance; C02 owns the converted item/gear record. Loot table values do not become C02 economy or item mechanics.
- C10 vs C03: C10 owns ability-table/oracle structure and row provenance; C03 owns the converted ability/effect/capability record.
- C10 vs C05/B09: C10 owns social/faction/contact table structure; C05 owns the faction/institution record and B09 owns social/faction/contact procedure.
- C10 vs C06/B08: C10 owns location/travel/discovery table structure; C06 owns location/site/region records and B08 owns travel/exploration/discovery procedure.
- C10 vs C07: C10 owns random hook/event/scenario table structure; C07 owns mission/scenario/adventure records.
- C10 vs C09/B10: C10 owns hazard/opposition/environment table structure; C09 owns converted hazard/environment records and B10 owns active threat trigger procedure.
- C10 vs C12/B06: C10 owns recipe/material/process table structure; C12 owns crafting/salvage/recipe records and B06 owns project/crafting/salvage/repair/upgrade procedure.
- C10 vs C14: C14 owns source-local cosmology, proper nouns, source-specific lore, donor-world assumptions, and source-specific prompt language. C10 may preserve and reference them but must not generalize them.
- C10 vs runtime/backend: C10 records conversion-stage table/oracle evidence and routing; runtime/backend owners decide later whether any generator becomes executable.
- C10 vs C04/C08/C11/C13: use references and satellite records, not inheritance or merged schemas.

## 11. Composite table/oracle record handling

Composite C10 records may represent nested tables, table families, oracle chains, result clusters, keyed lists, prompt decks, generator packages, or mixed donor constructs. Composite handling preserves the container and per-row or grouped provenance without merging output-family ownership.

A composite record may point to satellite C01-C14 records, rejected donor element records, source-local boundary records, or `pending_schema`. It may not collapse many family outputs into a single C10 record if those outputs require distinct converted content records.

## 12. Parent, child, and satellite record handling

C10 may use parent records for donor table/oracle/generator packages and child records for separable subtables, row groups, prompt clusters, keyed result lists, hidden result partitions, source-local partitions, or rejected import partitions.

Satellite records carry converted output-family evidence. A C10 parent does not make child creature, item, ability, relic, faction, location, scenario, vehicle/platform, hazard, companion, crafting, map, or source-local records inherit C10 ownership. Use references and satellite records, not inheritance or merged schemas.

## 13. Source-local and legal/IP handling

C10 must preserve source-local and legal/IP handling from C00. Donor table names, donor oracle names, donor generator names, result names, named factions, named places, named creatures, named items, named spells, named hazards, named gods, named planes, named worlds, named cosmology, source-specific prompt phrasing, source-specific lore, donor-world assumptions, license-specific expressions, verbatim-similar descriptions, protected art/map references, and sourcebook table prose must remain source evidence or route to source-local/legal/IP/C14 review.

C10 may identify a stripped reusable table/oracle pattern only after removing donor-protected expression and only as a canon-review candidate. Legal/IP posture must remain visible through provenance refs, source evidence refs, source-local boundary fields, rejected donor elements, canon eligibility, and review routing.

## 14. Rejected donor element handling

C10 must preserve rejected donor element handling from C00. Rejected donor elements include donor tables, donor oracles, donor generators, donor random-roll lists, donor roll ranges, donor d100 defaults, donor d20 defaults, donor d66 defaults, donor card-draw defaults, donor row formatting, donor column headers, donor weights/probabilities, donor encounter frequencies, donor loot frequencies, donor reward values, donor rarity weights, donor DCs, donor table execution rules, donor procedural generation assumptions, donor field names, donor proper nouns, donor cosmology, donor sourcebook table prose, and donor source-specific prompt language that cannot become Astra defaults.

Rejected donor element records prevent accidental import by preserving evidence, explaining why the element is not an Astra default, and routing any stripped reusable pattern to human/canon/legal review.

## 15. Canon eligibility and review routing

C10 preserves C00 canon_eligibility. A C10 record may be a reusable pattern candidate, source-local only, C14 review required, legal/IP review required, runtime review required, rejected_import, quarantined, or `pending_schema` handoff.

C10 never promotes canon, does not accept canon, and does not mark table/oracle/generator constructs as canon truth. Canon review must decide later whether stripped, provenance-bearing table/oracle patterns can become Astra-native content. Donor table names, result names, proper nouns, cosmology, exact ranges, exact weights, exact probabilities, exact procedures, and sourcebook prose remain non-canon unless the appropriate owner accepts them later.

## 16. Confidence, validation, and escalation routing

C10 preserves C00 confidence, validation, lineage, composition, and escalation routing. Low confidence, conflicting row evidence, unsupported donor fields, missing provenance, ambiguous output family, legal/IP risk, source-local cosmology, hidden protected truth, donor table execution pressure, runtime generator pressure, or final mechanics pressure must escalate to human review, extraction repair, C14 review, Batch A/B owner review, runtime review, or `pending_schema`.

Validation checks should confirm that C10 records keep conversion-stage classification separate from runtime behavior, final mechanics, canon truth, accepted lexicon, sourcebook prose, and donor table formats.

## 17. Hidden-state and protected-truth boundary

C10 may record that a table/oracle/generator contains hidden-state and protected-truth boundary concerns, such as hidden result rows, GM-secret oracle outcomes, concealed keyed results, secret source-local origins, unrevealed cosmology, trap-like hidden triggers, spoiler prompts, or protected procedural-selection evidence. C10 must not expose protected truth or decide what live players know.

Protected truth must remain in source evidence, source-local boundary, hidden/protected-result posture, or review refs. C10 does not create hidden-information runtime state, executable oracle memory, reveal procedure, or live-play knowledge policy.

## 18. Runtime boundary

C10 runtime boundary is strict. C10 must not define runtime random selection, runtime generator state, runtime oracle state, executable oracle behavior, random seed behavior, database table schemas, entity/component/event schemas, command lifecycle, context packets, save-state, backend generator schemas, encounter generators, loot generators, procedural content generation implementation, live-play table execution, table execution services, table persistence, table UI contracts, event logs, backend probability engines, or runtime encounter/loot/reward resolution.

C10 records may reference that such runtime/backend concerns exist, but all implementation, persistence, randomization, event, command, context-packet, generator, encounter, loot, reward, and live-play execution decisions route outside C10.

## 19. Canon/sourcebook/live-play/training boundary

C10 is not canon/sourcebook/live-play/training authority. It does not write sourcebook table prose, oracle prose, generator prose, encounter-table prose, loot-table prose, boxed text, GM procedure, player-facing prompts, accepted lexicon, training examples, evaluation gold data, or live-play scripts.

Examples may illustrate routing only. They are not schema authority beyond the C10 doctrine assertions they demonstrate.

## 20. Missing-schema fallback

If a table/oracle/generator row points to content with no stable C-family owner, C10 routes the output to `pending_schema` with source evidence, row provenance, confidence posture, rejected donor elements if needed, and escalation notes. C10 must not create a new family, merge ownership from another family, or use Batch B procedure terms as substitute C10 schema fields.

## 21. Examples of good and bad C10 usage

Good C10 usage:
- Preserve a donor wilderness event table as a C10 table/oracle record with per-row provenance, B08 handoff notes, and C06/C09/C01 output-family routing where rows point to places, hazards, or creatures.
- Preserve a treasure generator as C10 selection evidence with B05 handoff notes while routing actual item rows to C02 and rejecting donor loot frequencies, reward values, and rarity weights as Astra defaults.
- Preserve a faction rumor oracle as C10 prompt-list evidence with B09 handoff notes, C05/C14 routing, and source-local handling for named factions and proper nouns.
- Preserve a trap complication list as C10 keyed result evidence with B10 handoff notes and C09 routing for converted hazard records.

Bad C10 usage:
- Convert a donor d100 table into an Astra default d100 mechanic.
- Treat donor d20 defaults, d66 defaults, card draw defaults, exact roll ranges, weights/probabilities, or reroll rules as final Astra random-generation procedure.
- Turn a loot table into C02 reward economy, item pricing, or loot generator implementation.
- Turn an encounter table into runtime encounter generation, encounter balance, or live-play table execution.
- Promote donor table names, named gods, named worlds, named factions, source-specific prompt language, or donor cosmology as Astra canon.
- Use donor column headers or donor field names as C10 schema labels.

## 22. Minimum tests or assertions

Minimum C10 tests or assertions should verify that:
- the C10 file exists at the registry path;
- all required sections are present;
- C10 declares ownership and non-ownership;
- C10 inherit/include `AstraContentRecordBase` and preserves C00 provenance, legal/IP, rejected donor element, canon eligibility, confidence, validation, lineage, composition, and cross-reference posture;
- C10 record grammar is doctrine-level only and not runtime/database/final random generator/executable oracle/encounter table implementation/loot table implementation/final roll procedure/sourcebook table prose;
- donor table/oracle/generator/roll-range/weighting/row/field-name/proper-noun/cosmology leakage is rejected as Astra defaults;
- B05, B08, B09, B10, and relevant B01/B02 handoffs are present without Batch B schema inheritance;
- C01-C14 and `pending_schema` handoffs are present without cross-family inheritance;
- runtime, canon, sourcebook, live-play, hidden-state, source-local, and legal/IP boundaries are preserved;
- the registry C10 posture is draft/schema-draft/designed/not_reviewed without promotion to current/canon/runtime/stable/tested.

## 23. Acceptance criteria

C10 is acceptable when:
- C10 file exists at `docs/doctrine/schema/C10_table_oracle_record_schema.md`;
- C10 remains conversion-stage/canon-review schema doctrine only;
- C10 includes C00 base inheritance requirements;
- C10 does not import donor tables, donor oracles, donor generators, donor d100/d20/d66/card-draw defaults, roll ranges, weights/probabilities, row formatting, table columns, encounter/loot/reward frequencies, procedural instructions, field labels, proper nouns, or cosmology as Astra schema;
- C10 does not define final mechanics, final random-generation procedure, runtime random selection, runtime generator state, database schema, encounter generator implementation, loot generator implementation, procedural content generation implementation, live-play table execution, canon, sourcebook prose, or accepted lexicon;
- C10 has clear Batch B handoffs and cross-family handoffs;
- C10 includes source-local/legal/IP and rejected-import handling;
- C10 registry posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01/C02/C03/C09 registry posture is preserved;
- C04-C08 and C11-C14 are not promoted;
- focused tests pass;
- full suite passes.

## 24. Follow-up handoff to C06

C10 follow-up pressure to C06 is explicit because table/oracle/generator rows frequently point to locations, sites, regions, routes, biomes, domains, keyed places, travel discoveries, and place-like outputs. C10 may preserve the table/oracle/generator and row provenance, but C06 must own the converted location/site/region record once the row is converted with provenance.

Until C06 is drafted, location/site/region/route/biome/domain/place rows should be routed to C06 as the expected owner or to `pending_schema` if ownership cannot be safely assigned. C10 must not fill the C06 gap by defining location schema fields, travel procedure, map schema, sourcebook place prose, or runtime exploration behavior.

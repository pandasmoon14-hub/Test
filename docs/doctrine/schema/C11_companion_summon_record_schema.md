# C11 Companion/Summon Record Schema Doctrine

## 1. Purpose and status

C11 defines Batch C conversion-stage and canon-review schema doctrine for companion, summon, bonded beast, drone companion, spirit ally, contract entity, familiar-like entity, pet, cohort, follower, minion, dependent actor, controlled ally, temporary ally, bound entity, and relationship/control-dependent actor records. It exists to preserve source evidence and route review without letting donor companion systems, summon systems, pet systems, familiar systems, cohort systems, minion systems, follower systems, animal-companion class mechanics, disposable summon defaults, command action systems, loyalty/bond mechanics, control procedures, donor field names, donor proper nouns, named companions/summons/pets/familiars/cohorts/spirits/contracts, or donor-world assumptions become Astra defaults.

Status posture:
- C11 is a schema-draft doctrine file.
- C11 is not current canon, not runtime-ready, not stable_for_family, not stable_cross_family, and not tested_minimum.
- C11 records are conversion-stage/canon-review artifacts; they are not final companion mechanics, not final summon mechanics, not pet rules, not familiar rules, not follower rules, not minion economy, not runtime companion state, not runtime summon state, not runtime control state, not runtime bond state, not runtime loyalty state, not runtime command state, not runtime follower roster, not sourcebook companion prose, not sourcebook summon lists, not accepted lexicon, not canon acceptance, not canon promotion, and not live-play behavior.
- C11 never promotes canon, does not accept canon, does not create accepted lexicon, and does not decide live-play behavior.

## 2. Owner layer

Owner layer: Batch_C schema family doctrine.

C11 supports conversion intake, conversion output, canon review, legal/IP review, C14 source-local review, Batch B handoff review, and later runtime/backend review. Batch B operational files remain doctrine-facing pressure only; they are not C11 schema fields and are not inherited by C11 records.

## 3. What C11 owns

C11 owns conversion-stage record-family grammar for:
- companions;
- summons;
- bonded beasts;
- drone companions;
- spirit allies;
- contract entities;
- familiar-like entities and familiars as donor evidence only;
- pets;
- cohorts;
- followers;
- minions;
- dependent actors;
- controlled allies;
- temporary allies;
- bound entities;
- relationship/control-dependent actor records.

C11 owns companion/summon classification and routing posture for conversion and canon review. It records how a donor dependent-actor construct was identified, whether persistence is asserted or temporary, whether dependency/control posture is present, whether relationship/bond posture is asserted, which actor/ability/item/relic/faction/vehicle/scenario/hazard/table/map/source-local records must be referenced, whether hidden/protected-truth handling is needed, whether source-local/canon-review routing is required, what legal/IP posture applies, and what rejected donor element posture blocks leakage.

C11 owns the relationship/control-dependent record. It may reference the actor, ability, faction, item, relic, vehicle/platform, scenario, recovery/training, social, hazard, table, map, source-local, and runtime-review owners, but it does not absorb those owners.

## 4. What C11 must not own

C11 must not own or define:
- final mechanics;
- final companion mechanics;
- final summon mechanics;
- pet rules;
- familiar rules;
- follower rules;
- minion economy;
- disposable summon default;
- donor pet rules as canon;
- animal-companion class mechanics;
- summon duration math;
- command action economy;
- loyalty math;
- bond math;
- relationship math;
- control math;
- cohort progression;
- minion scaling;
- runtime companion state;
- runtime summon state;
- runtime control state;
- runtime bond state;
- runtime loyalty state;
- runtime command state;
- runtime follower roster;
- sourcebook companion prose;
- sourcebook summon lists;
- accepted lexicon;
- canon acceptance;
- canon promotion;
- live-play behavior.

C11 must not define final numerical values, loyalty scores, bond scores, command costs, action costs, summon durations, concentration rules, companion levels, cohort levels, minion counts, follower capacities, pet slots, control ranges, obedience DCs, training DCs, upkeep costs, feeding costs, morale values, damage values, defensive values, scaling formulas, replacement rules, resummon rules, death rules, dismissal rules, or companion/summon progression math.

## 5. C00 inheritance and required base posture

Every durable C11 record must inherit/include `AstraContentRecordBase` from C00 before any C11-specific shaping. C11 preserves C00 packet_refs, source_evidence_refs, construct_refs, outcome_refs, provenance_refs, source_local_boundary, rejected_donor_elements, canon_eligibility, confidence, validation, lineage, composition, cross-reference, legal/IP posture, review routing, and source-local boundary posture.

C11 records must keep the C00 distinction between source evidence, conversion classification, rejected donor elements, source-local boundaries, canon eligibility, validation status, lineage, parent/child records, satellite records, and cross-reference records. C11 cannot drop provenance merely because a donor companion, summon, pet, familiar, cohort, follower, minion, drone companion, spirit ally, contract entity, bond, control term, or command label appears familiar.

## 6. Companion/summon family scope and classification

C11 classifies dependent-actor records by conversion/review role, not by final companion mechanics. Neutral Astra-facing classification may include:
- companion/summon classification posture;
- persistence posture;
- dependency/control posture;
- relationship/bond posture;
- source/access posture;
- actor/reference posture;
- ability/reference posture;
- item/relic reference posture;
- faction/reference posture;
- vehicle/platform reference posture;
- scenario/reference posture;
- training/recovery reference posture;
- hazard/reference posture;
- table/reference posture;
- map/diagram reference posture;
- source-local/canon-review posture;
- hidden/protected-truth posture;
- legal/IP posture;
- rejection/containment posture.

These categories are routing concepts only. They do not define final companion mechanics, summon mechanics, pet systems, familiar systems, follower rosters, minion economies, loyalty tracks, bond tracks, command economies, control procedures, companion AI, or live-play behavior.

## 7. C11 record grammar, doctrine-level only

The following YAML-like block is doctrine grammar only. It is not a runtime schema, not a database schema, not a final companion statblock, not a summon system, not a pet system, not a follower roster, not command/control state, not relationship simulation, and not sourcebook companion prose.

```yaml
C11CompanionSummonRecord:
  extends: AstraContentRecordBase
  schema_family: C11
  companion_summon_classification_posture: companion | summon | bonded_beast | drone_companion | spirit_ally | contract_entity | familiar_like_entity | pet | cohort | follower | minion | dependent_actor | controlled_ally | temporary_ally | bound_entity | mixed | unknown
  persistence_posture: persistent_claim | temporary_claim | episodic_claim | disposable_claim_quarantined | source_local_only | unknown
  dependency_control_posture: independent_reference | handler_dependent | command_dependent | contract_dependent | bond_dependent | faction_access_dependent | scenario_temporary | unresolved
  relationship_bond_posture: relationship_evidence_only | bond_evidence_only | loyalty_evidence_only | control_evidence_only | no_relationship_claim | source_local_only | unresolved
  actor_reference_posture: C01_required | C01_reference_present | no_actor_record_required | pending_schema
  ability_reference_posture: C03_required | C03_reference_present | no_ability_record_required | pending_schema
  item_relic_reference_posture: C02_or_C04_required | references_present | no_asset_record_required | pending_schema
  faction_reference_posture: C05_required | C05_reference_present | no_faction_record_required | pending_schema
  vehicle_platform_reference_posture: C08_required | C08_reference_present | no_platform_record_required | pending_schema
  scenario_reference_posture: C07_required | C07_reference_present | no_scenario_record_required | pending_schema
  training_recovery_reference_posture: C12_or_B07_review_required | reference_present | no_process_record_required | pending_schema
  hazard_reference_posture: C09_required | C09_reference_present | no_hazard_record_required | pending_schema
  table_map_source_local_reference_posture: C10_or_C13_or_C14_required | references_present | no_reference_required | pending_schema
  hidden_protected_truth_posture: public_evidence | hidden_evidence | protected_truth | player_unknown | reviewer_only
  legal_ip_posture: inherited_from_C00 | legal_review_required | source_local_only | rejected_import_required
  rejection_containment_posture: none | donor_system_quarantined | donor_field_names_rejected | donor_proper_nouns_rejected | source_local_containment | rejected_import
```

This compact C11CompanionSummonRecord shape extends C00 base with C11-specific classification and routing concepts while avoiding donor companion/summon/pet/familiar/cohort/minion/control field names as Astra labels. The values above are doctrine review labels only; they are not final companion stats, not command-state enums, not backend states, not database columns, and not sourcebook rules.

## 8. Donor companion, summon, pet, familiar, cohort, minion, drone, spirit, contract, bond, control, and field-name handling

Donor exact companion names, summon names, pet names, familiar names, cohort names, minion names, spirit names, contract names, bond names, command terms, loyalty tracks, summon durations, pet rules, animal companion rules, follower rules, cohort rules, minion rules, drone companion rules, spirit ally rules, contract entity rules, disposable summon assumptions, summon lists, control procedures, field labels, and relationship mechanics may be preserved only as source evidence, donor tags, source-local notes, legal/IP review notes, C14 containment records, or rejected donor elements.

C11 explicitly blocks donor pet/familiar/animal-companion/summon/minion/follower/cohort systems from becoming Astra defaults without later doctrine/canon review. Donor companion systems, donor summon systems, donor pet systems, donor familiar systems, donor cohort systems, donor minion systems, donor follower systems, animal companion class mechanics, disposable summon default, donor pet rules as canon, summon duration defaults, command action defaults, loyalty/bond mechanics, control procedures, donor field names, donor proper nouns, named companions/summons/pets/familiars/cohorts/spirits/contracts, and donor-world assumptions are not Astra defaults.

## 9. Actor, ability, faction, item, relic, vehicle/platform, scenario, recovery/training, social, hazard, table, map, source-local, and runtime-review handoffs

Batch B handoffs:
- C11 references B01 when companions/summons appear in scene, encounter, activity, or dependent-actor participation pressure, but B01 is not C11 schema.
- C11 references B02 when companion/summon use affects action declaration, command declaration, cost commitment, or resolution trigger pressure, but B02 is not C11 schema.
- C11 references B07 when recovery, training, preparation, research, bonding, conditioning, taming, teaching, or companion readiness pressure appears, but B07 is not C11 schema.
- C11 references B09 when social, faction, relationship, contact, patron, institution, reputation, negotiation, bond, loyalty, handler, or contract pressure appears, but B09 is not C11 schema.
- C11 may reference B03 when companion/summon gear, carried items, tools, equipment, or asset use pressure appears, but B03 is not C11 schema.
- C11 may reference B10 when companion/summon danger, hazard exposure, hostility, opposition contact, runaway risk, contamination, corruption, disease, or active threat trigger pressure appears, but B10 is not C11 schema.
- Batch B procedure terms must not become C11 schema fields.

Cross-family handoffs use references and satellite records, not inheritance or merged schemas:
- C11 -> C01 for creature/NPC body identity, actor identity, statblock-like material, species-like material, NPC personality, adversary identity, or independent actor records.
- C11 -> C02 for companion gear, collars, saddles, tools, carried items, pet equipment, drone equipment, consumables, supplies, and mundane companion-associated objects.
- C11 -> C03 for summoning abilities, control abilities, companion commands, pet commands, bond abilities, drone routines, spirit powers, granted capabilities, or companion/summon active/passive effects.
- C11 -> C04 for companion implants, bonded relics, pet augmentations, drone modules, spirit-bound relics, controlled symbiotes, minion augmentations, or special installable companion assets.
- C11 -> C05 for faction-owned companions, institutional cohorts, patron-provided allies, guild pets, sect spirits, military drones, licenses, handlers, rank-gated companions, or organizational control.
- C11 -> C06 for habitats, lairs, stables, kennels, sanctums, summoning sites, drone bays, companion origin sites, or companion-controlled locations.
- C11 -> C07 for scenario/adventure/mission use, escort targets, rescue targets, summoned allies, quest companions, temporary allies, minion waves, follower roles, or story-role companions.
- C11 -> C08 for companion mounts, bonded vehicles, summoned vehicles, pet drones, controlled drones, cohort vehicles, minion platforms, or platform-dependent companion/control posture.
- C11 -> C09 for companion hazards, diseases, poisons, corruption, contamination, environmental vulnerability, summon backlash, unstable minions, hostile bond pressure, or companion-created hazards.
- C11 -> C10 for companion/summon tables, pet tables, familiar tables, random follower tables, spirit ally generators, drone companion tables, minion wave tables, or contract-entity tables.
- C11 -> C12 for companion training projects, taming processes, bonding processes, summoning recipes, contract rituals, drone construction, pet care processes, recovery projects, modification projects, or companion upkeep processes.
- C11 -> C13 for companion placement maps, lair maps, pet diagrams, drone diagrams, summon diagrams, minion formation diagrams, follower routes, or visual companion evidence.
- C11 -> C14 for source-local companion names, summon traditions, spirit systems, familiar traditions, named pets, named cohorts, donor-world contract law, source-specific pet/summon metaphysics, donor-world species, proper nouns, and donor-world assumptions.
- C11 -> pending_schema when no stable C-family owner exists.

## 10. C11 cross-family overlap rules

- C11 vs C01: C11 owns companion/summon/dependent-actor relationship and control posture. C01 owns the creature/NPC actor identity. A companion creature may require both C01 actor record and C11 relationship/control record.
- C11 vs C03: C11 owns dependent-actor relationship/control posture. C03 owns summoning/control/command/bond abilities and active/passive effects.
- C11 vs C05/B09: C11 owns companion/summon relationship record. C05 owns faction/institution ownership, access, handlers, licenses, and institutional control; B09 owns social/faction/contact procedure.
- C11 vs C07: C11 owns companion/summon record. C07 owns scenario role, escort objective, rescue function, temporary ally placement, and story function.
- C11 vs C08: C11 owns companion/control posture for mounts, pet drones, bonded vehicles, summoned vehicles, and controlled platforms. C08 owns vehicle/ship/platform identity.
- C11 vs C04: C11 owns companion/summon relationship posture. C04 owns implants, relics, augmentations, modules, and special assets attached to companions/summons.
- C11 vs C12/B07: C11 owns the companion/summon record. C12 owns processes such as taming, bonding, training recipes, drone construction, contract rituals, modification, or upkeep; B07 owns recovery/training/research/preparation procedure pressure.
- C11 vs C09: C11 owns companion/summon/dependent-actor posture. C09 owns hazards, afflictions, unstable summon pressure, contamination, corruption, disease, and environmental danger.
- C11 vs C14: C14 owns source-local proper nouns, donor-world species, summon traditions, spirit systems, contract law, pet metaphysics, and donor-world assumptions. C11 may reference them but must not generalize them.
- C11 vs runtime/backend: C11 records conversion-stage companion/summon evidence and routing. Runtime/backend owners decide later whether anything becomes companion state, summon state, control state, command queue, relationship tracker, loyalty tracker, follower roster, save-state node, or database row.
- C11 vs live-play/sourcebook: C11 is not player-facing companion prose, not summon list presentation, not live-play command procedure, not GM companion AI, and not sourcebook companion rules.
- C11 vs donor source: donor pet rules, disposable summon defaults, animal companion class features, familiar rules, cohort systems, minion economies, loyalty systems, bond mechanics, summon durations, command action systems, and source-specific companion lore remain evidence, source-local containment, or rejected material until later doctrine/canon review.

## 11. Composite companion/summon record handling

Composite donor entries often mix actor identity, summoning ability, command text, gear, faction license, habitat, scenario role, hazard backlash, random table rows, diagrams, and source-local lore. C11 may be the primary record only for the companion/summon/dependent-actor relationship and control posture. Other components must be split or referenced to C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C12, C13, C14, or `pending_schema` as appropriate.

Composite handling preserves lineage and provenance. It does not merge schemas, does not convert donor field labels into Astra labels, and does not infer final mechanics from adjacency.

## 12. Parent, child, and satellite record handling

C11 may use parent, child, and satellite records to preserve lineage and composition without merging ownership. Parent records may represent a donor companion/summon system or dependent-actor cluster under review. Child records may represent variants, named instances, forms, persistent/temporary postures, source-local expressions, or rejected-import slices when evidence requires separate conversion review. Satellite records carry C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C12, C13, C14, or `pending_schema` material.

Parent/child relationships do not create inheritance of final mechanics, runtime state, command economy, loyalty math, bond math, or donor system defaults.

## 13. Source-local and legal/IP handling

Source-local and legal/IP handling is mandatory when donor companion/summon evidence includes proper nouns, named companions, named summons, named pets, named familiars, named cohorts, named spirits, named contracts, donor-world species, source-specific summon traditions, spirit systems, contract law, pet metaphysics, license-specific expressions, protected art/map references, or verbatim-similar descriptions.

C11 routes source-local/legal/IP/C14 review through C00 `source_local_boundary`, `ip_legal_flags`, `source_reliability`, donor tags, and C14 containment records. C11 may preserve source-local terms as evidence, but it must not generalize those terms into Astra defaults, accepted lexicon, player-facing prose, or final companion/summon rules.

## 14. Rejected donor element handling

Rejected donor element handling must preserve refusal rationale. `rejected_donor_elements` may include donor companion systems, donor summon systems, donor pet systems, donor familiar systems, donor cohort systems, donor minion systems, donor follower systems, animal companion rules, disposable summon assumptions, summon duration defaults, command action defaults, loyalty tracks, bond tracks, control procedures, donor field labels, named entities, proper nouns, exact economy, exact class structure, exact statline, and donor source-specific prompt language.

A rejected C11 element can remain preserved as evidence or source-local containment. Rejection does not erase provenance; it blocks import as Astra schema, canon, runtime state, sourcebook companion prose, or live-play behavior.

## 15. Canon eligibility and review routing

C11 uses C00 `canon_eligibility` to route review. A C11 record may be marked not_reviewed, candidate, rejected, quarantined, or accepted only by the appropriate later canon owner; C11 itself never promotes canon and never treats conversion-stage classification as canon acceptance.

Canon review must check doctrine fit, C14 source-local containment, legal/IP posture, donor-field-name rejection, rejected donor elements, cross-family splits, and runtime/backend deferral. C11 draft posture does not authorize canon promotion, accepted lexicon, runtime import, sourcebook companion prose, or live-play command procedure.

## 16. Confidence, validation, and escalation routing

C11 confidence and validation posture uses C00 boundary_confidence, extraction_confidence, conversion_confidence, validation_status, validation_errors, review_required, and reviewer_notes. Escalate to human review when evidence cannot distinguish companion relationship from independent actor identity, ability effect, faction access, scenario role, training project, source-local lore, hidden truth, legal/IP risk, runtime state, or unsupported `pending_schema` pressure.

Validation checks should confirm that C11 keeps C00 base posture, preserves provenance, rejects donor system leakage, routes cross-family evidence, keeps Batch B terms out of schema fields, and avoids final mechanics.

## 17. Hidden-state and protected-truth boundary

C11 may preserve hidden-state and protected-truth evidence and protected truth when a companion/summon relationship, handler identity, contract owner, true loyalty, hidden controller, secret bond, disguised familiar, false pet identity, spirit pact, bound entity condition, or minion source should not be exposed to all consumers.

Hidden-state and protected-truth boundary language routes visibility and review. It does not create runtime secret state, live-play reveal timing, companion AI behavior, deception mechanics, loyalty scores, relationship trackers, or sourcebook mystery prose.

## 18. Runtime boundary

C11 forbids runtime companion state, runtime summon state, runtime control state, runtime bond state, runtime loyalty state, runtime command state, runtime follower roster, command queues, relationship trackers, loyalty trackers, save-state nodes, database companion rows, entity/component/event schemas, command lifecycle, context packets, backend companion schemas, backend summon schemas, and live-play companion AI or command procedure.

Runtime/backend owners decide later whether any reviewed evidence becomes companion state, summon state, control state, command queue, relationship tracker, loyalty tracker, follower roster, save-state node, database row, entity component, event schema, context packet, backend companion schema, backend summon schema, or live-play behavior. C11 only preserves conversion-stage companion/summon evidence and routing.

## 19. Canon/sourcebook/live-play/training boundary

C11 is not canon, not sourcebook companion prose, not sourcebook summon lists, not player-facing companion rules, not player-facing summon rules, not live-play command procedure, not GM companion AI, not training examples, and not final mechanics. Training, evaluation, and example systems may reference C11 only after the relevant doctrine, canon, runtime, and legal/IP owners approve their own layers.

C11 must not convert donor companion prose, donor summon lists, donor pet rules, donor familiar rules, animal companion class features, cohort systems, minion economies, follower systems, disposable summon defaults, loyalty systems, bond systems, command systems, control systems, or source-specific companion lore into Astra sourcebook text.

## 20. Missing-schema fallback

When a dependent-actor construct has no stable C-family owner, route to `pending_schema` with quarantine, escalation, human review, or source-local containment. `pending_schema` is named fallback routing only; it is not a permission to invent companion fields, summon mechanics, pet-system fields, runtime state, database schema, or sourcebook prose.

Missing C12 process doctrine, future companion mechanics, future summon mechanics, future pet systems, future follower management, or future runtime/backend state must remain deferred rather than backfilled by C11.

## 21. Examples of good and bad C11 usage

Good C11 usage:
- Preserve a donor bonded beast as a C11 relationship/control record, route the beast body to C01, route a bonding technique to C03, and route source-local beast names to C14.
- Preserve a temporary summoned ally as C11 persistence/dependency posture while routing the summoning ability to C03 and any summon table to C10.
- Preserve a drone companion relationship record in C11 while routing the drone platform to C08, modules to C04, mundane tools to C02, and faction license or handler access to C05/B09.
- Preserve a spirit contract as C11 evidence while routing contract ritual/process pressure to C12, social obligation pressure to B09, and donor-world spirit law to C14.

Bad C11 usage:
- Convert donor pet rules into Astra default pet slots, feeding costs, or loyalty scores.
- Convert donor summon durations into Astra summon duration defaults or disposable summon default doctrine.
- Turn a companion record into runtime companion state, command queues, relationship trackers, loyalty trackers, database companion rows, or live-play companion AI.
- Use donor companion/summon/pet/familiar/cohort/minion/control field names as C11 schema labels.
- Promote named companions, named summons, named pets, named familiars, named cohorts, named spirits, named contracts, donor proper nouns, or donor-world assumptions into canon without later review.

## 22. Minimum tests or assertions

Minimum C11 tests should assert that:
- the C11 file exists at the registry path;
- all required sections are present;
- C11 declares ownership and non-ownership;
- C11 explicitly inherits/includes C00 `AstraContentRecordBase`;
- C11 doctrine grammar is not runtime/database/final-companion-statblock/summon-system/pet-system/follower-roster/command-control-state/relationship-simulation/sourcebook-companion-prose schema;
- donor companion/summon/pet/familiar/cohort/minion/follower/animal-companion/disposable-summon/command/loyalty/bond/control/field-name/proper-noun leakage is rejected;
- B01, B02, B07, B09, B03, and B10 remain handoffs rather than schema fields;
- C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C12, C13, C14, and `pending_schema` handoffs are present;
- runtime, canon, sourcebook, live-play, hidden-truth, source-local, legal/IP, and rejected-import boundaries are preserved;
- registry posture remains draft/schema-draft/designed/not_reviewed without current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum promotion.

## 23. Acceptance criteria

C11 is acceptable when:
- C11 file is created at `docs/doctrine/schema/C11_companion_summon_record_schema.md`;
- C11 remains conversion-stage/canon-review schema doctrine only;
- C11 includes C00 base inheritance requirements;
- C11 does not import donor companion systems, summon systems, pet systems, familiar systems, animal companion rules, cohort systems, minion systems, follower systems, disposable summon defaults, summon duration defaults, loyalty/bond mechanics, command action systems, control procedures, field labels, proper nouns, named companions/summons/pets/familiars/cohorts/spirits/contracts, or donor-world assumptions as Astra schema;
- C11 does not define final companion mechanics, summon mechanics, pet rules, minion economy, runtime companion/summon/control/bond/loyalty/command/follower state, database schema, live-play companion AI, live-play command procedure, canon, sourcebook companion prose, or accepted lexicon;
- C11 has clear Batch B handoffs and cross-family handoffs;
- C11 includes source-local/legal/IP and rejected-import handling;
- C11 registry posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01/C02/C03/C04/C05/C06/C07/C08/C09/C10/C13/C14 registry posture is preserved;
- C12 is not promoted;
- focused tests pass;
- full suite passes.

## 24. Follow-up handoff to C12

C11 explicitly hands process-shaped pressure to C12 when companion training projects, taming processes, bonding processes, summoning recipes, contract rituals, drone construction, pet care processes, recovery projects, modification projects, or companion upkeep processes require conversion-stage process grammar.

Until C12 is drafted and reviewed, C11 may record that C12 review is required, but C11 must not invent C12 fields, final training mechanics, crafting/salvage/recipe rules, project progress math, upkeep systems, or runtime readiness state.

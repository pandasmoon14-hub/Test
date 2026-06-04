# C01 Creature/NPC Record Schema Doctrine

## 1. Purpose and status

C01 defines Batch C conversion-stage and canon-review record-family schema doctrine for creature/NPC records. It covers creature, NPC, adversary, monster, spirit, AI actor, swarm, non-player being, and similar actor-like constructs extracted from donor material and converted into Astra-facing review records.

Status posture:
- C01 is a schema-draft doctrine file.
- C01 is not current canon, not accepted lexicon, not sourcebook prose, not live-play authority, and not runtime-ready.
- C01 is not a final creature system, combat math system, encounter system, runtime actor model, donor statblock import format, or canon promotion procedure.
- C01 records are conversion-stage/canon-review artifacts only; they preserve evidence, boundaries, routing, and review posture until appropriate owners decide what can become canon or final mechanics.

## 2. Owner layer

C01 belongs to Batch C schema-family doctrine under the Astra Doctrine Council - Schema Working Group. It sits below C00 and must obey the Batch C unlock/index/readiness gate. C01 uses Batch A actor ontology and related world doctrine as upstream conceptual guardrails and Batch B operations only as handoff pressure, not as schema-field authority.

## 3. What C01 owns

C01 owns conversion-stage record-family grammar for:
- creatures, NPCs, adversaries, monsters, spirits, AI actors, swarms, non-player beings, and similar actor-like constructs;
- actor-like conversion records whose main identity is an entity/being rather than an item, ability, hazard, faction, location, scenario, table row, or source-local setting assertion;
- C01-specific classification and routing posture for conversion review;
- C01 parent, child, composite, and satellite handling when the central record remains a creature/NPC actor-like construct;
- references from the actor record to capability, item, faction, location, hazard, scenario, companion/control, map, table/oracle, and source-local owners;
- donor-statblock containment as evidence, donor tags, rejected donor elements, or source-local context, not Astra defaults.

## 4. What C01 must not own

C01 must not own or define:
- final mechanics, final math, combat balance, numerical attributes, hit points, armor, defense, challenge rating, proficiency, level, CR, XP, initiative, damage dice, monster math, or final actor balance;
- runtime actor state, entity/component schemas, event schemas, command lifecycle, context packets, save-state, database contracts, backend schemas, or live runtime behavior;
- encounter procedure, action procedure, live-play behavior, live-play statblocks, GM behavior, training examples as authority, sourcebook prose, accepted lexicon, canon acceptance, or canon promotion;
- donor statblock formats, donor field names as Astra labels, donor challenge ratings, donor hit points, donor armor classes, donor action economies, donor saving throw formats, donor senses formats, donor skill lists, donor spell/action lists, donor alignment/cosmology, donor challenge/XP math, donor proper nouns, or donor world assumptions as Astra defaults;
- carried gear, equipment, loot, abilities, factions, locations, scenarios, hazards, companions/control relationships, table/oracle generation rows, map annotations, or source-local setting law except by reference to their owner families.

## 5. C00 inheritance and required base posture

Every durable C01 conversion-stage record must inherit/include `AstraContentRecordBase` from C00 before any C01-specific shaping. C01 may add family-specific doctrine grammar, but it must not remove, rename, or weaken C00 base posture.

C01 must preserve these C00 requirements:
- `packet_refs`, `source_evidence_refs`, `construct_refs`, `outcome_refs`, and `provenance_refs`;
- `source_local_boundary`, `rejected_donor_elements`, `canon_eligibility`, `confidence`, `validation`, lineage, composition, cross-reference, and legal/IP posture;
- parent/child record refs, cross-reference records, inheritance refusal across family handoffs, confidence routing, validation status, escalation routing, source-local quarantine, and human-review options;
- provenance-lock behavior: donor exact values and donor terms remain evidence unless later review accepts an Astra-native abstraction.

## 6. Creature/NPC family scope and classification

C01 classifies creature/NPC conversion records by role in conversion and review, not by final combat math. C01 classification uses neutral Astra-facing categories such as:
- actor classification: creature, NPC, adversary, monster-like construct, spirit-like construct, AI actor, swarm, non-player being, or uncertain actor-like construct;
- embodiment/form category: embodied, distributed, swarm-form, digital/AI-form, spirit-form, hybrid, vehicle-hosted, object-bound, or unknown;
- agency/control posture: autonomous, scripted, controlled, summoned, companion-like, institutional proxy, environmental proxy, passive, or unclear;
- social/hostility posture: social actor, neutral presence, antagonist, rival, guard/enforcer, predator, hazard-adjacent pressure, ally-candidate, or unknown;
- capability reference posture: no extracted capabilities, capability refs required, capability extraction pending, donor capability list quarantined, or C03 split required;
- environment/location reference posture: location refs required, habitat/site refs required, route context required, or C06 split required;
- faction/institution reference posture: faction refs required, authority/allegiance/rank refs required, or C05 split required;
- hazard/interface posture: hazard refs required, capability-hazard split required, environmental pressure split required, or C09 split required;
- item/loot reference posture: item refs required, gear/loot split required, or C02/C04 split required;
- source-local/canon-review posture: reusable pattern candidate, source-local retained, legal/IP review required, C14 review required, rejected import, quarantined, or pending schema.

## 7. C01 record grammar, doctrine-level only

The following YAML-like block is doctrine grammar only. It is not a runtime schema, not a database schema, not a final statblock format, not sourcebook statblock prose, not a donor statblock import contract, and not final Astra mechanics.

```yaml
C01CreatureNpcRecord:
  extends: AstraContentRecordBase
  schema_family: C01
  record_kind: creature_npc_actor_like_conversion_record
  actor_classification: neutral Astra-facing category, not donor type label
  embodiment_form_category: neutral review category
  agency_control_posture: neutral review category
  social_hostility_posture: neutral review category
  capability_reference_posture: none | refs_required | extraction_pending | donor_list_quarantined | split_to_C03
  environment_location_reference_posture: none | refs_required | split_to_C06 | pending_schema
  faction_institution_reference_posture: none | refs_required | split_to_C05 | pending_schema
  hazard_interface_posture: none | refs_required | split_to_C09 | split_to_C03 | pending_schema
  item_loot_reference_posture: none | refs_required | split_to_C02 | split_to_C04 | pending_schema
  companion_control_reference_posture: none | refs_required | split_to_C11 | pending_schema
  scenario_role_reference_posture: none | refs_required | split_to_C07 | pending_schema
  map_annotation_reference_posture: none | refs_required | split_to_C13 | pending_schema
  table_oracle_reference_posture: none | refs_required | split_to_C10 | pending_schema
  source_local_canon_review_posture: reusable_pattern_candidate | source_local_retained | legal_ip_review_required | C14_review_required | rejected_import | quarantined
  donor_statblock_evidence_refs: [source_evidence_ref]
  donor_tag_refs: [source_evidence_ref]
  rejected_donor_element_refs: [rejected_donor_element_ref]
  required_family_handoffs: [C02 | C03 | C04 | C05 | C06 | C07 | C09 | C10 | C11 | C13 | C14 | pending_schema]
```

C01 labels must be Astra-facing routing labels. They must not import donor statblock field names as schema labels.

## 8. Donor statblock and donor field-name handling

Donor statblocks are evidence pressure, not Astra schema. C01 rejects donor statblock formats, donor field names, donor math, donor challenge ratings, donor CR, donor XP, donor hit points, donor HP equivalents, donor armor classes, donor AC equivalents, donor defense values, donor action economies, donor initiative, donor damage dice, donor proficiency/level math, donor saving throw formats, donor senses formats, donor skill lists, donor spell lists, donor action lists, donor legendary actions, donor lair actions, donor alignment/cosmology, and donor proper nouns as Astra defaults.

Donor exact values may be preserved only as source evidence, donor tags, source-local notes, or rejected donor elements. They must not become C01 field labels, final mechanics, final math, or accepted Astra vocabulary by appearing in a C01 record.

Donor proper nouns, named species, named gods, named worlds, named factions, named locations, named cosmology, source-specific metaphysics, and donor-world assumptions route to source-local/legal/IP/C14 review unless later canon review accepts stripped reusable patterns.

## 9. Actor capability, ability, item, hazard, faction, location, and scenario handoffs

C01 handoffs use references and satellite records, not inheritance or merged schemas. Required handoff routing:
- C01 -> C03 for abilities, powers, techniques, spells, special actions, passive capabilities, aura-like effects, or capability packages.
- C01 -> C02 for carried gear, equipment, loot, consumables, tools, weapons, armor, or practical items.
- C01 -> C04 for implanted, bonded, installed, relic-bound, augmented, or host-integrated assets.
- C01 -> C05 for faction, institution, social body, authority, allegiance, rank, obligation, or organizational role.
- C01 -> C06 for habitat, site, region, location, lair/site, route context, or spatial placement.
- C01 -> C07 for scenario/adventure/mission role, scripted encounter role, quest role, or adventure-path function.
- C01 -> C09 for hazard-like traits, environmental dangers, disease-like pressure, trap-like pressure, terrain interaction, or threat environment.
- C01 -> C10 for random table/oracle generation of creatures or NPCs; table rows do not become C01 records unless converted with provenance.
- C01 -> C11 for companion, summon, pet, follower, cohort, minion, controlled associate, or relationship/control posture.
- C01 -> C13 for map/diagram annotation references.
- C01 -> C14 for source-local setting, cosmology, proper nouns, metaphysical origin, source-specific species law, or donor-world assumptions.
- C01 -> pending_schema when no stable C-family owner exists.

## 10. C01 cross-family overlap rules

Overlap rules:
- C01 vs C11: C01 owns general actor-like creature/NPC records; C11 owns companion/summon/control/relation posture. If a summon has an entity plus a summoning ability plus control terms, split into C01, C03, and C11 references.
- C01 vs C03: C01 owns the actor record; C03 owns the capability record. Do not embed donor spell/action lists as C01 schema.
- C01 vs C09: C01 owns the actor; C09 owns hazard/environment pressure. A creature that emits poison, disease, aura, terrain danger, or ambient hazard should reference C09 or C03 as applicable.
- C01 vs C07: C01 owns the creature/NPC record; C07 owns scenario placement or adventure role.
- C01 vs C14: C14 owns source-local cosmology, metaphysics, proper nouns, and donor-world setting assumptions. C01 may reference them but must not generalize them.
- C01 vs C02/C04/C05/C06/C10/C13: use references and satellite records, not inheritance or merged schemas.

## 11. Composite creature record handling

Composite donor constructs often combine a creature, abilities, gear, lair/site, hazard aura, faction role, encounter script, loot, and source-local lore in one donor block. C01 may hold the central actor-like conversion record, but composite content must be decomposed into referenced C-family records when another owner exists.

A composite record remains C01 only when the actor-like identity is the review subject. Embedded capability lists, loot lines, hazard clauses, map references, faction ranks, scenario scripts, and source-local origin claims must become refs, rejected donor elements, quarantined evidence, or pending-schema routing.

## 12. Parent, child, and satellite record handling

C01 may use parent, child, and satellite records to preserve lineage and composition without merging ownership. Parent records may represent a donor creature/NPC cluster or archetype under review. Child records may represent variants, forms, stages, minions, or sub-actors when the donor evidence requires separate conversion review. Satellite records carry C02, C03, C04, C05, C06, C07, C09, C10, C11, C13, C14, or `pending_schema` material.

Cross-reference records must keep `inheritance_allowed: false` unless C00 later authorizes a different shared-base behavior. A C01 parent does not make child capability, item, hazard, faction, location, map, companion, table, scenario, or source-local records inherit C01 ownership.

## 13. Source-local and legal/IP handling

C01 must preserve source-local and legal/IP handling from C00. Source-local identifiers, donor proper nouns, named species, named gods, named worlds, named factions, named locations, trademark-like labels, license-specific expressions, verbatim-similar descriptions, protected art/map references, and donor cosmology must be retained as source evidence or routed to source-local/legal/IP/C14 review.

C01 may identify a reusable actor-like pattern only after stripping donor-protected expression and only as a canon-review candidate. Legal/IP posture must remain visible through provenance refs, source evidence refs, source-local boundary fields, rejected donor elements, canon eligibility, and review routing.

## 14. Rejected donor element handling

C01 must preserve rejected donor element handling. Rejected donor elements include donor field names, donor statblock layouts, donor challenge ratings, donor HP/AC values, donor action economy terms, donor spell/action list labels, donor senses/skills/save formats, donor alignment/cosmology labels, donor proper nouns, donor exact math, and donor sourcebook prose that cannot become Astra defaults.

Rejected material should be recorded with evidence refs, reason, owner routing, and review posture. Rejection does not delete evidence; it prevents accidental import into Astra schema, mechanics, canon, lexicon, runtime, sourcebook prose, or live-play authority.

## 15. Canon eligibility and review routing

C01 may mark canon eligibility posture from C00, but C01 never promotes canon. A creature/NPC conversion record may be ineligible, candidate, accepted-with-limits candidate pending review, quarantined, or rejected-import according to the C00 `canon_eligibility` structure and human/canon-review routing.

Canon review must determine whether a stripped reusable pattern, generic actor classification, or source-local reference can move forward. C01 does not accept canon, does not define accepted lexicon, does not authorize sourcebook publication, and does not convert donor names or donor mechanics into Astra defaults.

## 16. Confidence, validation, and escalation routing

C01 records must preserve C00 confidence and validation posture for boundary confidence, extraction confidence, conversion confidence, validation status, missing-evidence flags, schema-gap routing, and escalation. Low-confidence actor identity, mixed-family ownership, donor-statblock ambiguity, source-local leakage, legal/IP risk, hidden-state exposure, or missing owner coverage must route to human review, extraction repair, canon review, legal/IP review, C14, or `pending_schema` rather than improvised fields.

Validation checks should confirm C00 base inclusion, C01 classification presence, provenance refs, source evidence refs, rejected donor element handling, cross-family refs, source-local posture, canon eligibility posture, and absence of final mechanics/runtime fields.

## 17. Hidden-state and protected-truth boundary

C01 may preserve that a donor creature/NPC record contains hidden-state or protected-truth pressure, but it must not expose protected truth as player-facing canon or runtime state. Secret identities, concealed motives, undisclosed faction ties, disguised forms, hidden weaknesses, concealed AI instructions, false-monster reveals, and source-only truths must route through C00 hidden/protected handling, canon review, scenario owners, or runtime gates as appropriate.

C01 is allowed to record safe review labels such as hidden-state-risk or protected-truth-review-required. It must not create reveal timing, live-play disclosure rules, context-packet truth compilation, or runtime hidden-information state.

## 18. Runtime boundary

C01 forbids runtime actor state and runtime implementation contracts. C01 must not define entity/component schemas, event schemas, command lifecycle, context packets, save-state, state deltas, database contracts, backend schemas, runtime actor IDs, live combat trackers, AI behavior loops, perception state, inventory state, relationship state, or persistence models.

A C01 record may later be consumed by runtime design, but that consumption requires a separate runtime owner and review gate. Conversion-stage record grammar is not a runtime actor model.

## 19. Canon/sourcebook/live-play/training boundary

C01 is not canon acceptance, sourcebook prose, live-play behavior, or training authority. C01 does not write final bestiary entries, NPC writeups, GM instructions, encounter tactics, player-facing descriptions, live-play statblocks, accepted lexicon entries, or training examples that override doctrine.

Examples in this file are doctrine-facing tests of routing boundaries only. They are not final content and do not authorize donor mechanics, donor names, donor prose, or donor cosmology.

## 20. Missing-schema fallback

When a creature/NPC-like construct requires a field or owner that C01 and the known C-family handoffs cannot lawfully cover, route to `pending_schema`, quarantine, escalation, or human review. Missing schema coverage never permits improvised family-specific fields, donor format import, runtime schema invention, or canon promotion.

`pending_schema` must carry provenance, source evidence, confidence, validation, rejected donor element, and source-local/legal/IP posture from C00.

## 21. Examples of good and bad C01 usage

Good C01 usage:
- Convert a donor monster-like entity into a C01 actor-like record with `AstraContentRecordBase`, source evidence refs, neutral actor classification, rejected donor statblock elements, and C03 refs for extracted capabilities.
- Preserve a named source-world spirit as source-local/C14 review while extracting only a generic spirit-form actor pattern as a canon-review candidate.
- Split a summoned creature into C01 for the actor record, C03 for the summoning ability, and C11 for control/relationship posture.
- Record that a swarm-like actor has a hazard-interface posture and route ambient poison or terrain pressure to C09 rather than embedding hazard rules in C01.

Bad C01 usage:
- Copy a donor statblock with HP, AC, CR, saves, senses, skills, spell list, legendary actions, lair actions, initiative, damage dice, and alignment into Astra labels.
- Declare a donor named species, god, world, faction, location, or cosmology as Astra canon because it appeared in a C01 record.
- Define runtime entity/component/event schemas, command lifecycle, context packets, save-state, database contracts, or AI behavior loops in C01.
- Use C01 to write final sourcebook prose, live-play statblocks, encounter procedure, action procedure, combat balance, or accepted lexicon.

## 22. Minimum tests or assertions

Minimum C01 tests/assertions should verify:
- the C01 file exists at the registry path and contains all required sections;
- C01 declares ownership and non-ownership boundaries;
- C01 inherits/includes `AstraContentRecordBase` and preserves C00 provenance, source-local, rejected donor element, canon eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture;
- C01 doctrine grammar is doctrine-level only and not runtime, database, final statblock, sourcebook, or donor schema;
- donor statblocks, field names, math, challenge ratings, HP/AC equivalents, action economies, spell/action lists, senses/skills/save formats, alignment/cosmology, and proper nouns are rejected as Astra defaults;
- cross-family handoffs and overlap rules cover C02, C03, C04, C05, C06, C07, C09, C10, C11, C13, C14, and `pending_schema`;
- runtime, canon, sourcebook, live-play, training, hidden-state, source-local/legal/IP, and rejected-import boundaries are preserved;
- registry posture is draft/schema-draft/designed/not_reviewed without current, stable, tested-minimum, canon, or runtime promotion.

## 23. Acceptance criteria

C01 is acceptable when:
- the file exists at `docs/doctrine/schema/C01_creature_npc_record_schema.md`;
- it remains conversion-stage/canon-review schema doctrine only;
- it includes C00 base inheritance requirements;
- it does not import donor statblocks or donor field labels as Astra schema;
- it does not define combat math, final mechanics, runtime actor state, database schema, live-play behavior, canon, sourcebook prose, or accepted lexicon;
- it has clear cross-family handoffs and overlap boundaries;
- it includes source-local/legal/IP and rejected-import handling;
- the registry C01 posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- focused durable tests pass.

## 24. Follow-up handoff to C02

C01 explicitly hands carried gear, equipment, loot, consumables, tools, weapons, armor, practical items, and actor-carried object pressure to C02. C02 should define item/gear conversion-stage record-family doctrine without inheriting C01 actor schema, without importing donor item statblocks, and without promoting economy, equipment, or loot mechanics to canon or runtime state.

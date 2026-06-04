# C03 Ability/Power/Technique Record Schema Doctrine

## 1. Purpose and status

C03 defines Batch C conversion-stage and canon-review record-family schema doctrine for ability/power/technique records. It covers ability, power, technique, spell-like effect, maneuver, routine, invocation, psionic effect, active-effect, passive-effect, item-granted effect, creature-granted capability, and similar capability-like constructs extracted from donor material and converted into Astra-facing review records.

Status posture:
- C03 is a schema-draft doctrine file.
- C03 is not current canon, not accepted lexicon, not sourcebook power prose, not live-play authority, and not runtime-ready.
- C03 is not final ability mechanics, final ability math, resource math, cost math, damage math, condition math, duration math, recharge/cooldown doctrine, backlash doctrine, spell-slot doctrine, Vancian casting doctrine, power-point doctrine, class feature progression, feat/talent system, combat balance, runtime ability-instance state, donor spell/class/feature import format, spell list, class feature table, technique list, or canon promotion procedure.
- C03 records are conversion-stage/canon-review artifacts only; they preserve evidence, boundaries, routing, and review posture until appropriate owners decide what can become canon, final mechanics, or runtime implementation.

## 2. Owner layer

C03 belongs to Batch C schema-family doctrine under the Astra Doctrine Council - Schema Working Group. It sits below C00 and must obey the Batch C unlock/index/readiness gate. C03 uses Batch A technique, resource, cost, damage, consequence, actor, asset, hazard, and source-local doctrine as upstream conceptual guardrails and Batch B operations only as handoff pressure, not as schema-field authority.

## 3. What C03 owns

C03 owns conversion-stage record-family grammar for:
- abilities, powers, techniques, maneuvers, routines, invocations, spell-like effects, psionic effects, active effects, passive effects, item-granted effects, creature-granted capabilities, and similar capability-like constructs;
- ability/power/technique conversion records whose main identity is a capability or effect rather than the actor, item, relic, faction, location, scenario, vehicle/platform, hazard, table row, recipe/process, map annotation, or source-local setting assertion that carries, grants, teaches, places, or contextualizes it;
- C03-specific ability/power/technique classification and routing posture for conversion and canon review;
- C03 parent, child, composite, and satellite handling when the central record remains a capability-like construct;
- references from the capability record to host actors, item/gear objects, relic/installable assets, factions, locations, scenarios, vehicle/platform records, hazards, table/oracle rows, recipes/processes, map/diagram annotations, companions/summons, and source-local owners;
- donor spell, feature, power, maneuver, technique, active-effect, passive-effect, and field-name containment as evidence, donor tags, rejected donor elements, or source-local context, not Astra defaults.

## 4. What C03 must not own

C03 must not own or define:
- final mechanics, final ability math, action economy, resource economy, cost math, damage math, healing math, condition math, duration math, recharge rules, cooldown rules, backlash rules, combat balance, final numerical values, action costs, target counts, ranges, areas, damage dice, healing values, save DCs, attack bonuses, spell levels, class levels, power ranks, resource costs, slot levels, cooldowns, charges, duration counts, condition severities, critical rules, scaling formulas, or effect math;
- spell slots, Vancian casting, power points, ki/qi/essence economies, class feature progression, feat/talent systems, donor resource systems, donor action economies, donor damage/healing math, donor save DCs, donor ranges/areas/durations, donor recharge/cooldown rules, donor power ranks, donor spell levels, or donor slots as Astra defaults;
- runtime ability instances, runtime cooldown state, runtime buff/debuff state, runtime actor state, runtime item state, entity/component schemas, event schemas, command lifecycle, context packets, save-state, database contracts, backend ability schemas, combat trackers, persistence models, or live runtime behavior;
- sourcebook power lists, spell lists, class feature tables, technique lists, sourcebook power prose, accepted lexicon, canon acceptance, canon promotion, live-play behavior, GM instructions, player-facing ability entries, training examples, or donor spell/class/feature import;
- donor spells, donor spell lists, donor class features, donor feat/talent features, donor maneuvers, donor powers, donor techniques, donor field names as Astra labels, donor proper nouns, donor cosmology, donor spell names, class feature names, named techniques, trademark-like power names, named schools, named elements, named deities, named disciplines, named factions, named source-specific metaphysics, or source-specific lore as Astra defaults;
- actor identity, item/gear identity, relic/installable asset identity, faction access law, location-bound placement, scenario scripts, vehicle/platform systems, hazard/environment pressure, table/oracle generation, crafting/salvage/recipe processes, map/diagram annotations, companion/summon relation posture, or source-local setting law except by reference to their owner families.

## 5. C00 inheritance and required base posture

Every durable C03 conversion-stage record must inherit/include `AstraContentRecordBase` from C00 before any C03-specific shaping. C03 may add family-specific doctrine grammar, but it must not remove, rename, or weaken C00 base posture.

C03 must preserve these C00 requirements:
- `packet_refs`, `source_evidence_refs`, `construct_refs`, `outcome_refs`, and `provenance_refs`;
- `source_local_boundary`, `rejected_donor_elements`, `canon_eligibility`, `confidence`, `validation`, lineage, composition, cross-reference, and legal/IP posture;
- parent/child record refs, cross-reference records, inheritance refusal across family handoffs, confidence routing, validation status, escalation routing, source-local quarantine, and human-review options;
- provenance-lock behavior: donor exact values and donor terms remain source evidence, donor tags, or rejected donor elements unless later review accepts an Astra-native abstraction.

## 6. Ability/power/technique family scope and classification

C03 classifies ability/power/technique conversion records by role in conversion and review, not by final mechanics. C03 classification uses neutral Astra-facing categories such as:
- capability classification: active capability, passive capability, invoked routine, maneuver-like capability, technique-like capability, spell-like effect, psionic-effect-like capability, item-granted effect, creature-granted capability, aura-like effect, access/unlock capability, or uncertain capability-like construct;
- activation posture: activation evidence present, passive posture only, triggered posture evidence, routine posture evidence, access posture evidence, or activation owner handoff required;
- source/access posture: innate, learned, trained, item-granted, relic-granted, faction-taught, location-bound, scenario-bound, vehicle/platform-mounted, companion/summon-mediated, source-local, mixed, or uncertain;
- host/reference posture: actor host ref, item host ref, relic/implant/module host ref, faction/institution access ref, location/site ref, scenario ref, vehicle/platform ref, companion/summon ref, or pending owner ref;
- target/interface posture: self-facing, actor-facing, item-facing, location-facing, hazard-facing, companion-facing, map/diagram-facing, abstract/interface pending, or donor target evidence quarantined;
- effect-family reference posture: no effect-family owner needed, refs required, split to C09/A-layer/future mechanics owner, source-local review required, or pending_schema;
- cost/resource reference posture: none recorded, donor evidence only, A10/B02 handoff pressure, source-local resource system quarantined, or pending_schema;
- duration/recharge reference posture: none recorded, donor evidence only, recharge/cooldown evidence quarantined, A/B/future mechanics handoff required, or pending_schema;
- damage/condition reference posture: none recorded, donor evidence only, damage/condition owner handoff required, hazard pressure present, or pending_schema;
- hazard/environment reference posture: none, B10 pressure, C09 split required, source-local environmental law review, or pending_schema;
- item/relic reference posture: none, C02 item-granted ref required, C04 relic/installable ref required, C02/C04 split required, or pending_schema;
- source-local/canon-review posture and legal/IP posture: stripped generic candidate, source-local retained, legal/IP review required, C14 review required, rejected_import, quarantined, or not_reviewed.

## 7. C03 record grammar, doctrine-level only

The following YAML-like block is doctrine grammar only. It is not a runtime schema, not a database schema, not a final ability statblock, not a spell list, not a class feature table, not a technique list, not sourcebook power prose, not donor spell prose, and not an implementation contract.

```yaml
C03AbilityPowerTechniqueRecord:
  extends: AstraContentRecordBase
  schema_family: C03
  capability_classification: active_capability | passive_capability | invoked_routine | maneuver_like_capability | technique_like_capability | spell_like_effect | psionic_effect_like_capability | item_granted_effect | creature_granted_capability | aura_like_effect | access_unlock_capability | uncertain_capability_like_construct
  conversion_review_role: identity_record | extracted_capability | granted_capability | host_satellite | composite_parent | composite_child | source_local_reference | rejected_import_reference
  activation_posture: evidence_present | passive_only | triggered_evidence | routine_evidence | access_evidence | owner_handoff_required | unknown
  source_access_posture: innate | learned | trained | item_granted | relic_granted | faction_taught | location_bound | scenario_bound | vehicle_platform_mounted | companion_summon_mediated | source_local | mixed | uncertain
  host_reference_posture: actor_ref | item_ref | relic_implant_module_ref | faction_institution_ref | location_site_ref | scenario_ref | vehicle_platform_ref | companion_summon_ref | pending_owner_ref | none
  target_interface_posture: self_facing | actor_facing | item_facing | location_facing | hazard_facing | companion_facing | map_diagram_facing | abstract_interface_pending | donor_target_evidence_quarantined
  effect_family_reference_posture: none | refs_required | split_to_C09 | split_to_A_or_future_mechanics_owner | source_local_review_required | pending_schema
  cost_resource_reference_posture: none | donor_evidence_only | A10_B02_handoff_pressure | source_local_resource_system_quarantined | pending_schema
  duration_recharge_reference_posture: none | donor_evidence_only | recharge_cooldown_evidence_quarantined | mechanics_handoff_required | pending_schema
  damage_condition_reference_posture: none | donor_evidence_only | damage_condition_owner_handoff_required | hazard_pressure_present | pending_schema
  required_family_handoffs: [C01 | C02 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema]
  batch_b_pressure_refs: [B01 | B02 | B03 | B07 | B10]
  donor_element_handling: evidence_only | donor_tags_only | rejected_donor_elements | source_local_boundary | legal_ip_review | C14_review | quarantined
  inheritance_allowed: false
```

The grammar avoids donor spell/power/feature field names as Astra labels. Donor exact values may be preserved only as source evidence, donor tags, or rejected donor elements, not as Astra schema labels or final mechanics.

## 8. Donor spell, feature, power, maneuver, technique, and field-name handling

C03 rejects donor spells, donor spell lists, donor class features, donor feat/talent features, donor maneuvers, donor powers, donor techniques, donor power ranks, donor spell levels, donor slots, Vancian casting, donor resource systems, donor action economies, donor damage/healing math, donor save DCs, donor ranges/areas/durations, donor recharge/cooldown rules, donor field names, donor proper nouns, and donor cosmology as Astra defaults.

Donor spell names, class feature names, named techniques, trademark-like power names, named schools, named elements, named deities, named disciplines, named factions, named cosmology, named source-specific metaphysics, source-specific magic systems, psionic systems, cultivation systems, and source-specific lore must route to source-local/legal/IP/C14 review unless canon review later accepts stripped reusable patterns. C03 may preserve donor exact values only as source evidence, donor tags, or rejected donor elements; it must not convert them into final action costs, resource costs, damage dice, healing values, save DCs, ranges, areas, durations, recharge counts, cooldowns, charges, power ranks, spell levels, or slot levels.

## 9. Action, cost, resource, damage, backlash, duration, recharge, and effect handoffs

C03 records capability identity and routing pressure; it does not define action, cost, resource, damage, backlash, duration, recharge, cooldown, or effect math.

Required Batch B handoffs:
- C03 references B02 for action declaration, cost commitment, and resolution trigger pressure, but B02 is not C03 schema.
- C03 references B10 when a capability creates hazard/opposition/contact/active threat trigger pressure, but B10 is not C03 schema.
- C03 may reference B01 when the ability is scene/activity/encounter-facing, but B01 is not C03 schema.
- C03 may reference B03 when an item use grants or channels a capability, but B03 is not C03 schema.
- C03 may reference B07 when training/research/preparation affects access or readiness, but B07 is not C03 schema.
- Batch B procedure terms must not become C03 schema fields; B01/B02/B03/B07/B10 handoff notes are doctrine-facing pressure only.

Batch A and future mechanics handoffs remain separate. Final resource economy, damage families, costs, recharge, cooldown, backlash, condition effects, duration math, and effect math remain with their proper A/B/future mechanics owners.

## 10. C03 cross-family overlap rules

C03 uses references and satellite records, not inheritance or merged schemas. Cross-family references do not make the target family inherit C03 grammar, and `inheritance_allowed: false` remains the default posture.

Required C03 handoffs:
- C03 -> C01 for creature/NPC innate abilities, monster actions, NPC features, actor-bound capabilities, or biological/spiritual capabilities.
- C03 -> C02 for item-granted effects, weapon-like effects, gear use-effects, consumable effects, equipment routines, or tool-enabled capabilities.
- C03 -> C04 for relic-granted abilities, implant-granted capabilities, installable modules, bonded powers, augmentation effects, or host-integrated assets.
- C03 -> C05 for faction-taught techniques, institutional access, restricted doctrines, guild schools, order-based abilities, rank-gated powers, or social/institutional authority powers.
- C03 -> C06 for location-bound powers, site effects, regional powers, domain/place-tied capabilities, terrain-linked techniques, or local environmental access.
- C03 -> C07 for scenario/adventure/mission-specific abilities, scripted powers, quest-only effects, ritual scene functions, or adventure-path capabilities.
- C03 -> C08 for vehicle/ship/platform abilities, mounted systems, ship maneuvers, mech routines, platform powers, or hardpoint-like effects.
- C03 -> C09 for hazard-like effects, environmental pressures, trap-like effects, disease/poison/radiation/corruption pressures, aura-like environmental danger, or terrain interaction.
- C03 -> C10 for table/oracle generation of abilities or effects; table rows do not become C03 records unless converted with provenance.
- C03 -> C11 for companion/summon control abilities, pet commands, minion commands, cohort features, summon access, or relationship/control powers.
- C03 -> C12 for crafting/salvage/recipe processes that create, modify, upgrade, unlock, or transform abilities or ability-granting items.
- C03 -> C13 for map/diagram annotation references involving ability diagrams, ritual diagrams, area-of-effect visual labels, or spatial overlays.
- C03 -> C14 for source-local setting, cosmology, proper nouns, named schools, named elements, named metaphysics, named deities, source-specific magic systems, psionic systems, cultivation systems, or donor-world assumptions.
- C03 -> pending_schema when no stable C-family owner exists.

Explicit overlap rules:
- C03 vs C01: C03 owns the capability record; C01 owns the actor that possesses, uses, or grants it. Donor monster action lists must not become C01 or C03 final statblocks.
- C03 vs C02: C03 owns the item-granted capability; C02 owns the item/gear object. Do not embed donor weapon/item effect math as final C02 or C03 mechanics.
- C03 vs C04: C03 owns the granted capability; C04 owns the relic/implant/installable asset. If an implant grants a power, split asset record and capability record.
- C03 vs C09: C03 owns the capability/effect; C09 owns hazard/environment pressure. If a power creates persistent environmental danger, route the hazard pressure to C09.
- C03 vs C11: C03 owns summoning/control/access capabilities; C11 owns companion/summon/relation/control posture as record-family doctrine.
- C03 vs C14: C14 owns source-local cosmology, metaphysics, proper nouns, source-specific magic systems, psionic systems, cultivation systems, and donor-world assumptions. C03 may reference them but must not generalize them.
- C03 vs B02: C03 records capability identity and routing; B02 owns action declaration/cost commitment/resolution trigger procedure. C03 must not define action economy or cost procedure.
- C03 vs Batch A resource/damage/effect owners: C03 records conversion-stage capability family, but final resource economy, damage families, costs, recharge, backlash, and effect math remain with their proper A/B/future mechanics owners.
- C03 vs C05/C06/C07/C08/C10/C12/C13: use references and satellite records, not inheritance or merged schemas.

## 11. Composite ability/power/technique record handling

Composite donor constructs often combine a capability, actor host, item focus, relic source, faction school, location limit, scenario script, vehicle platform, summon controller, hazard aura, table generation, crafting unlock, map diagram, resource cost, action format, damage math, duration, recharge, backlash, and source-local lore in one donor block. C03 may hold the central capability conversion record, but composite content must be decomposed into referenced C-family records when another owner exists.

A composite record remains C03 only when the ability/power/technique identity is the review subject. Embedded actors, item objects, relic/installable assets, faction schools, location domains, scenario-only scripts, vehicle hardpoints, companion/summon relation posture, hazard/environment pressure, table/oracle rows, crafting processes, map labels, source-local origin claims, and final mechanics must become refs, rejected donor elements, quarantined evidence, or pending-schema routing.

## 12. Parent, child, and satellite record handling

C03 may use parent, child, and satellite records to preserve lineage and composition without merging ownership. Parent records may represent a donor ability/power/technique cluster, suite, spell-like group, maneuver tree, routine bundle, or capability package under review. Child records may represent separable modes, variants, sub-effects, passive/active portions, access clauses, or evidence partitions when the donor evidence requires separate conversion review. Satellite records carry C01, C02, C04, C05, C06, C07, C08, C09, C10, C11, C12, C13, C14, or `pending_schema` material.

A C03 parent does not make child actor, item, relic/installable, faction, location, scenario, vehicle/platform, hazard, table, companion/summon, recipe/process, map, or source-local records inherit C03 ownership. Use references and satellite records, not inheritance or merged schemas.

## 13. Source-local and legal/IP handling

C03 must preserve source-local and legal/IP handling from C00. Source-local identifiers, donor proper nouns, donor spell names, donor class feature names, named techniques, trademark-like power names, named schools, named elements, named deities, named disciplines, named factions, named cosmology, named source-specific metaphysics, source-specific magic systems, psionic systems, cultivation systems, license-specific expressions, verbatim-similar descriptions, protected art/map references, source-specific power lore, source-specific resource lore, and donor-world assumptions must be retained as source evidence or routed to source-local/legal/IP/C14 review.

C03 may identify a reusable capability pattern only after stripping donor-protected expression and only as a canon-review candidate. Legal/IP posture must remain visible through provenance refs, source evidence refs, source-local boundary fields, rejected donor elements, canon eligibility, and review routing.

## 14. Rejected donor element handling

C03 must preserve rejected donor element handling. Rejected donor elements include donor spells, donor spell lists, donor class features, donor feat/talent features, donor maneuvers, donor powers, donor techniques, donor power ranks, donor spell levels, donor slots, Vancian casting, donor resource systems, donor action economies, donor damage/healing math, donor save DCs, donor ranges/areas/durations, donor recharge/cooldown rules, donor field names, donor proper nouns, donor cosmology, donor exact math, and donor sourcebook power prose that cannot become Astra defaults.

Rejected material should be recorded with evidence refs, reason, owner routing, and review posture. Rejection does not delete evidence; it prevents accidental import into Astra schema, mechanics, canon, lexicon, runtime, sourcebook prose, power lists, spell lists, class feature tables, technique lists, resource systems, action economies, damage systems, combat trackers, or live-play authority.

## 15. Canon eligibility and review routing

C03 may mark canon eligibility posture from C00, but C03 never promotes canon. An ability/power/technique conversion record may be ineligible, candidate, accepted-with-limits candidate pending review, quarantined, or rejected-import according to the C00 `canon_eligibility` structure and human/canon-review routing.

Canon review must determine whether a stripped reusable pattern, generic capability classification, activation concept, host/interface concept, or source-local reference can move forward. C03 does not accept canon, does not define accepted lexicon, does not authorize sourcebook publication, and does not convert donor spell names, class feature names, named techniques, power ranks, spell levels, slots, resource systems, action economies, damage/healing math, save DCs, ranges, areas, durations, recharge/cooldown rules, proper nouns, or cosmology into Astra defaults.

## 16. Confidence, validation, and escalation routing

C03 records must preserve C00 confidence and validation posture for boundary confidence, extraction confidence, conversion confidence, validation status, missing-evidence flags, schema-gap routing, and escalation. Low-confidence capability identity, mixed-family ownership, donor spell/power/feature ambiguity, donor field-name leakage, donor resource/action/damage leakage, source-local leakage, legal/IP risk, hidden-state exposure, or missing owner coverage must route to human review, extraction repair, canon review, legal/IP review, C14, or `pending_schema` rather than improvised fields.

Validation checks should confirm C00 base inclusion, C03 classification presence, provenance refs, source evidence refs, rejected donor element handling, Batch B handoff boundaries, cross-family refs, source-local posture, canon eligibility posture, and absence of final mechanics/runtime/resource/action/damage fields.

## 17. Hidden-state and protected-truth boundary

C03 may preserve that a donor ability/power/technique record contains hidden-state or protected-truth pressure, but it must not expose protected truth as player-facing canon or runtime state. Secret capabilities, concealed side effects, undisclosed costs, hidden backlash, false spell identities, masked power sources, dormant invocations, reveal-dependent routines, source-only lore, and GM-only effect truths must route through C00 hidden/protected handling, canon review, scenario owners, C09/C14 owners, or runtime gates as appropriate.

Hidden-state notes in C03 are evidence and routing posture only. They do not create runtime hidden-information state, combat tracker entries, live-play reveal scripts, sourcebook secrets, or canon truth.

## 18. Runtime boundary

C03 must not define runtime ability instances, runtime cooldown state, runtime buff/debuff state, runtime actor state, runtime item state, runtime effect state, entity/component schemas, event schemas, command lifecycle, context packets, save-state, database contracts, backend ability schemas, combat trackers, persistence models, ability-instance IDs, cooldown counters, active buff/debuff records, target snapshots, action queues, resource ledgers, or live runtime behavior.

C03 records may be consumed later by runtime or tooling teams only through separate runtime/backend doctrine and implementation review. C03 itself is a conversion-stage/canon-review schema doctrine file, not an entity/component/event schema, command lifecycle, context-packet compiler, save-state shape, database contract, backend ability schema, combat tracker, or runtime ability registry.

## 19. Canon/sourcebook/live-play/training boundary

C03 is not canon/sourcebook/live-play/training authority. It does not accept canon, promote canon, define accepted lexicon, write final sourcebook power prose, create spell lists, create class feature tables, create technique lists, define live-play behavior, write GM instructions, write player-facing ability entries, or create training examples that override doctrine.

Examples in this file are doctrine-facing tests of routing boundaries only. They are not final content and do not authorize donor mechanics, donor names, donor prose, donor resource systems, donor action economies, donor power lore, or donor cosmology.

## 20. Missing-schema fallback

When an ability/power/technique-like construct requires a field or owner that C03 and the known C-family handoffs cannot lawfully cover, route to `pending_schema`, quarantine, escalation, or human review. Missing schema coverage never permits improvised family-specific fields, donor format import, runtime schema invention, database contract invention, resource/action/damage math invention, or canon promotion.

`pending_schema` must carry provenance, source evidence, confidence, validation, rejected donor element, and source-local/legal/IP posture from C00.

## 21. Examples of good and bad C03 usage

Good C03 usage:
- Convert a donor ability-like entry into a C03 ability/power/technique record with `AstraContentRecordBase`, source evidence refs, neutral capability classification, rejected donor spell/power/feature elements, and C01 refs for actor hosts.
- Preserve a named source-world spell, discipline, school, deity, metaphysics, or power system as source-local/C14 review while extracting only a stripped generic capability pattern as a canon-review candidate.
- Split an item-granted effect into C02 for the item/gear object, C03 for the granted capability, B03 as item-use pressure, and rejected donor elements for charges, slots, ranges, and damage math.
- Record that an aura-like power has hazard/environment reference posture and route persistent environmental danger to C09 and B10 rather than embedding hazard rules in C03.

Bad C03 usage:
- Copy a donor spell list, class feature table, feat/talent tree, maneuver list, technique list, power ranks, spell levels, spell slots, Vancian casting, resource costs, action economy, damage dice, healing values, save DCs, ranges, areas, durations, recharge/cooldown counts, or donor field names into Astra labels.
- Declare a donor named spell, class feature, technique, school, element, deity, discipline, faction, cosmology, source-specific magic system, psionic system, cultivation system, or metaphysics as Astra canon because it appeared in a C03 record.
- Define runtime ability instances, runtime cooldown state, runtime buff/debuff state, entity/component/event schemas, command lifecycle, context packets, save-state, database contracts, backend ability schemas, combat trackers, or ability registries in C03.
- Use C03 to write final sourcebook power prose, spell lists, class feature tables, technique lists, final ability statblocks, final mechanics, resource economy, damage math, action economy, combat balance, live-play behavior, or accepted lexicon.

## 22. Minimum tests or assertions

Minimum C03 tests/assertions should verify:
- the C03 file exists at the registry path and contains all required sections;
- C03 declares ownership and non-ownership boundaries;
- C03 inherits/includes `AstraContentRecordBase` and preserves C00 provenance, source-local, rejected donor element, canon eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture;
- C03 doctrine grammar is doctrine-level only and not runtime, database, final ability statblock, spell list, class feature table, technique list, sourcebook power prose, donor spell prose, or donor schema;
- donor spells, donor spell lists, donor class features, donor feat/talent features, donor maneuvers, donor powers, donor techniques, donor power ranks, donor spell levels, donor slots, Vancian casting, donor resource systems, donor action economies, donor damage/healing math, donor save DCs, donor ranges/areas/durations, donor recharge/cooldown rules, donor field names, donor proper nouns, and donor cosmology are rejected as Astra defaults;
- Batch B handoff boundaries cover B02 and B10 plus relevant B01, B03, and B07 without turning Batch B procedure into C03 schema fields;
- cross-family handoffs and overlap rules cover C01, C02, C04, C05, C06, C07, C08, C09, C10, C11, C12, C13, C14, and `pending_schema`;
- runtime, canon, sourcebook, live-play, training, hidden-state, source-local/legal/IP, and rejected-import boundaries are preserved;
- registry posture is draft/schema-draft/designed/not_reviewed without current, stable, tested-minimum, canon, or runtime promotion.

## 23. Acceptance criteria

C03 is acceptable when:
- the file exists at `docs/doctrine/schema/C03_ability_power_technique_record_schema.md`;
- it remains conversion-stage/canon-review schema doctrine only;
- it includes C00 base inheritance requirements;
- it does not import donor spells, powers, maneuvers, techniques, class features, feats/talents, spell lists, action lists, resource systems, spell slots, power points, action economy, damage/healing math, DCs, ranges/areas/durations, recharge/cooldown rules, field labels, proper nouns, or cosmology as Astra schema;
- it does not define final mechanics, resource economy, action economy, damage math, effect math, duration math, recharge/cooldown, backlash, runtime ability instances, database schema, combat tracker, live-play behavior, canon, sourcebook prose, or accepted lexicon;
- it has clear Batch B handoffs and cross-family handoffs;
- it includes source-local/legal/IP and rejected-import handling;
- the registry C03 posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01 and C02 registry posture is preserved and C04-C14 are not promoted;
- focused durable tests pass.

## 24. Follow-up handoff to C09

C03 explicitly hands hazard-like effects, environmental pressures, trap-like effects, disease/poison/radiation/corruption pressures, aura-like environmental danger, persistent area danger, terrain interaction, and active threat trigger pressure to C09 when a capability creates hazard/environment posture. C09 should define hazard/environment conversion-stage record-family doctrine without inheriting C03 capability schema, without importing donor spell or power math, and without promoting hazard-like effects to canon, sourcebook prose, live-play behavior, or runtime state.

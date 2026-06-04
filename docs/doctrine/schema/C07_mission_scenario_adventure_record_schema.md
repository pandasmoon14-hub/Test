# C07 Mission/Scenario/Adventure Record Schema Doctrine

## 1. Purpose and status

C07 defines Batch C schema-layer doctrine for conversion-stage mission, scenario, adventure, arc, hook, objective, scene-chain, encounter-chain, reward/consequence structure, branching path, quest-like structure, adventure-path fragment, scripted scenario function, and similar scenario-structure records.

Status posture:
- C07 is drafted as schema-draft material for conversion and canon review.
- C07 is not current canon, not runtime-ready, not stable_for_family, not stable_cross_family, and not tested_minimum.
- C07 records are conversion-stage and canon-review artifacts only; they are not final adventure design, scene execution, encounter balance, reward economy, railroad procedure, runtime quest state, canon events, sourcebook adventure prose, boxed text, read-aloud text, GM narration, or live-play behavior.
- C07 preserves evidence and routing for later owners without accepting donor adventure formats or promoting canon.

## 2. Owner layer

C07 belongs to Batch_C schema doctrine and is owned by the Astra Doctrine Council - Schema Working Group. Supporting owner layers may include Batch_A, Batch_B, canon_review, lexicon_review, runtime_review, extraction_repair, legal/IP review, C14 source-local review, and human_review, but those supporting layers do not become C07 schema authority.

C07 owner posture is classification and routing posture for conversion/canon review. C07 does not replace C00, Batch B operational files, Batch A campaign/world/consequence doctrine, runtime/backend ownership, or sourcebook/live-play presentation owners.

## 3. What C07 owns

C07 owns conversion-stage record-family grammar for:
- missions, scenarios, adventures, arcs, hooks, quest-like structures, operations, jobs, commissions, prompts, adventure seeds, and adventure-path fragments;
- objectives, object goals, place goals, actor goals, faction goals, rescue goals, investigation goals, repair/project goals, route goals, and scenario role notes;
- scene-chains, encounter-chains, activity chains, site-entry chains, route chains, escalation chains, and scenario-use pressure when preserved as structure evidence;
- reward/consequence structures, branching paths, outcome references, consequence references, payout references, treasure/requisition references, access rewards, and failure or complication reference posture;
- scripted scenario functions and similar scenario-structure records when treated as conversion/canon-review evidence, not execution procedure;
- mission/scenario/adventure classification and routing posture for conversion and canon review.

C07 owns the neutral Astra-facing scenario classification and routing concepts needed to decide where actors, places, items, powers, factions, hazards, tables, maps, source-local lore, and pending gaps should go.

## 4. What C07 must not own

C07 must not own or define final mechanics, final adventure design, scene procedure, encounter procedure, action procedure, travel procedure, social/faction procedure, hazard procedure, reward economy, value flow, encounter balance, pacing math, branching runtime logic, railroad procedure, player-choice constraint procedure, runtime quest state, runtime objective state, runtime consequence state, branch state, event logs, canon events, accepted canon timeline, sourcebook adventure prose, boxed text, read-aloud text, GM narration, GM instructions, required player choices, fail-forward rules, live-play behavior, accepted lexicon, canon acceptance, or canon promotion.

C07 must not define final quest states, objective state machines, XP awards, treasure values, reward values, difficulty budgets, railroading rules, scripted scene execution, branch resolution math, campaign pacing, event-log shape, canon event sequence, runtime quest tracker, database schema, donor adventure-format import, or donor field names as Astra defaults.

## 5. C00 inheritance and required base posture

Every durable C07 record must inherit/include `AstraContentRecordBase` from C00 before any C07-specific shaping. C07 must preserve the C00 base posture for packet_refs, source_evidence_refs, construct_refs, outcome_refs, provenance_refs, source_local_boundary, rejected_donor_elements, canon_eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture.

The following block is doctrine grammar only. It is not a runtime schema, not a database schema, not a quest-state schema, not a final adventure format, not scene execution, not encounter procedure, not sourcebook adventure prose, not boxed text, and not canon event timeline.

```yaml
C07MissionScenarioAdventureRecord:
  extends: AstraContentRecordBase
  schema_family: C07
  scenario_classification: mission | scenario | adventure | arc | hook | objective_structure | scene_chain | encounter_chain | reward_consequence_structure | branching_path | quest_like_structure | adventure_path_fragment | scripted_scenario_function | mixed | uncertain
  scenario_classification_confidence: high | medium | low | blocked
  objective_posture: none | referenced | extracted_as_structure | source_local_only | routed_to_owner | uncertain
  scene_chain_posture: none | structural_reference | b01_handoff_required | source_local_only | rejected_donor_format | uncertain
  branching_posture: none | evidence_only | consequence_refs_required | runtime_owner_required | source_local_only | rejected_donor_format | uncertain
  reward_consequence_reference_posture: none | c02_refs_required | b05_handoff_required | consequence_owner_required | source_local_only | rejected_donor_values | uncertain
  location_reference_posture: none | c06_refs_required | c13_visual_evidence_refs_required | source_local_c14_required | pending_schema_required | uncertain
  actor_reference_posture: none | c01_refs_required | c11_refs_required | source_local_c14_required | pending_schema_required | uncertain
  faction_reference_posture: none | c05_refs_required | b09_handoff_required | source_local_c14_required | pending_schema_required | uncertain
  hazard_reference_posture: none | c09_refs_required | b10_handoff_required | source_local_c14_required | pending_schema_required | uncertain
  table_oracle_reference_posture: none | c10_refs_required | generator_evidence_only | selected_output_refs_required | pending_schema_required | uncertain
  hidden_protected_truth_posture: none | protected_truth_refs_required | spoiler_evidence_only | source_local_boundary_required | runtime_owner_required | uncertain
  legal_ip_posture: clear_reusable_pattern | source_local_review_required | legal_review_required | c14_review_required | rejected_import_required | uncertain
```

C07 family-specific grammar is conversion/canon-review schema doctrine only. It classifies scenario records by conversion/review role, not by final adventure procedure and not by donor adventure/quest/scenario field labels.

## 6. Mission/scenario/adventure family scope and classification

C07 scope includes mission/scenario/adventure structures and their neutral routing posture. C07 may classify a record by scenario classification, objective posture, scene-chain posture, branching posture, reward/consequence reference posture, location/reference posture, actor/reference posture, faction/reference posture, hazard/reference posture, table/oracle reference posture, source-local/canon-review posture, hidden/protected-truth posture, and legal/IP posture.

These categories are Astra-facing conversion labels. They do not import donor adventure names, donor quest stages, donor scene numbering, donor encounter numbering, donor branch labels, donor pacing notes, donor objective labels, donor required outcomes, or donor reward values as Astra schema.

## 7. C07 record grammar, doctrine-level only

C07 record grammar is doctrine-level only and is limited to conversion-stage/canon-review schema doctrine. It may describe how a mission-like record points to source evidence and family owners, but it must not become runtime schema, database schema, quest-state schema, final adventure format, scene execution, encounter procedure, sourcebook adventure prose, boxed text, read-aloud prose, or canon event timeline.

C07 grammar may express source evidence, provenance, classification confidence, routed references, owner handoffs, rejection notes, and escalation posture. It must not express final quest states, objective state machines, encounter balance, reward values, XP awards, treasure values, difficulty budgets, railroading rules, scripted scene execution, branch resolution math, campaign pacing, event-log shape, canon event sequence, or runtime quest tracker.

## 8. Donor adventure, quest, scene-chain, objective, reward, boxed-text, and field-name handling

C07 rejects donor adventures, donor scenario formats, donor quest formats, donor scene chains, donor boxed text, donor read-aloud prose, donor scene numbers, donor encounter numbers, donor quest stages, donor objective labels, donor reward values, donor XP awards, donor treasure awards, donor branch labels, donor map keys, donor pacing notes, donor required outcomes, donor railroad assumptions, donor field names, donor proper nouns, named NPCs, named places, named factions, named gods, named items, named events, named timelines, and donor cosmology as Astra defaults.

Donor exact adventure structure, scene numbers, encounter numbers, boxed text, read-aloud text, quest stages, objective labels, reward values, XP awards, treasure awards, branch labels, map keys, pacing notes, required outcomes, and railroad assumptions may be preserved only as source evidence, donor tags, source-local notes, or rejected donor elements, not as Astra schema labels or final mechanics.

Donor adventure names, scenario names, quest names, named NPCs, named places, named factions, named gods, named items, named events, named timelines, named cosmology, source-specific scenario lore, source-specific prose, and donor-world assumptions must route to source-local/legal/IP/C14 review unless canon review later accepts stripped reusable patterns.

## 9. Scene, action, reward, travel, faction, hazard, table, location, and consequence handoffs

Required Batch B handoffs are pressure references only, not C07 schema inheritance:
- C07 references B01 for scene, encounter, activity, scene-chain, encounter-chain, and scenario-use pressure, but B01 is not C07 schema.
- C07 references B02 for action declaration, cost commitment, resolution trigger, objective-action, branch-trigger, or consequence-trigger pressure, but B02 is not C07 schema.
- C07 references B05 for reward, requisition, acquisition, payout, treasure, value flow, compensation, resource access, or mission reward pressure, but B05 is not C07 schema.
- C07 references B08 for travel, exploration, navigation, discovery, route, site entry, wilderness/space movement, and journey pressure, but B08 is not C07 schema.
- C07 references B09 for social, faction, contact, patron, institution, reputation, negotiation, settlement, jurisdiction, and organizational pressure, but B09 is not C07 schema.
- C07 references B10 for hazards, opposition, active threat triggers, environmental danger, trap pressure, adversary contact, and escalation pressure, but B10 is not C07 schema.

Batch B procedure terms must not become C07 schema fields. Scene, action, reward, travel, faction, hazard, table, location, and consequence handoffs remain references, pressure notes, or escalation routes.

## 10. C07 cross-family overlap rules

Cross-family handoffs are routing references only and do not allow inheritance from other C-family schemas:
- C07 -> C01 for NPCs, creatures, adversaries, patrons, bystanders, monsters, contacts, bosses, or scenario actors.
- C07 -> C02 for mission items, treasure, clue objects, tools, weapons, gear, consumables, rewards, caches, and object goals.
- C07 -> C03 for scenario-specific abilities, rituals, effects, powers, environmental effects, scripted powers, or objective-linked capabilities.
- C07 -> C04 for relics, implants, installable assets, bonded artifacts, cursed assets, scenario assets, or mission-critical special assets.
- C07 -> C05 for factions, institutions, patrons, enemies, authorities, guilds, cults, governments, organizations, social bodies, and institutional objectives.
- C07 -> C06 for locations, sites, regions, keyed adventure sites, routes, worlds, planes, settlements, stations, megastructures, and place objectives.
- C07 -> C08 for vehicles, ships, platforms, mechs, bases, stations, convoy elements, mobile objectives, and platform-scale scenario assets.
- C07 -> C09 for hazards, environments, weather, region pressure, trap-like pressure, exposure, disasters, afflictions, and scenario danger.
- C07 -> C10 for tables, oracles, random encounter tables, treasure tables, rumor tables, hook tables, route complication tables, mission generator tables, and scenario generators.
- C07 -> C11 for companions, summons, followers, pets, cohorts, minions, escorted characters, rescue targets, controlled allies, and relationship/control scenario roles.
- C07 -> C12 for crafting/salvage/recipe objectives, repair missions, upgrade objectives, resource extraction, project tasks, salvage sites, and process goals.
- C07 -> C13 for map/diagram annotations, keyed maps, clue diagrams, tactical maps, route overlays, puzzle diagrams, and visual scenario evidence.
- C07 -> C14 for source-local setting, cosmology, named events, named history, named worlds, named planes, named cultures, named gods, source-specific quest lore, source-specific timeline, donor-world assumptions, and proper nouns.
- C07 -> pending_schema when no stable C-family owner exists.

Required overlap decisions:
- C07 vs C06: C07 owns mission/scenario/adventure structure. C06 owns location/site/region records. A dungeon/adventure site may require C06 place records plus C07 scenario structure records.
- C07 vs C10: C07 owns scenario/adventure structure. C10 owns tables/oracles/generators used by or producing scenario content. A random mission table is not C07 until selected/converted with provenance.
- C07 vs C05/B09: C07 owns the scenario role or mission objective. C05 owns the faction/institution record; B09 owns social/faction/contact procedure.
- C07 vs C09/B10: C07 owns the scenario placement/function. C09 owns hazard/environment pressure; B10 owns active threat trigger procedure.
- C07 vs C01: C07 owns scenario role/placement; C01 owns creature/NPC records.
- C07 vs C02/B05: C07 owns reward/objective role; C02 owns item/gear records; B05 owns acquisition/reward/value-flow procedure.
- C07 vs C03/B02: C07 owns scenario function; C03 owns ability/effect/capability records; B02 owns action/cost/resolution trigger procedure.
- C07 vs C13: C07 owns scenario/adventure structure; C13 owns map/diagram annotation and visual evidence.
- C07 vs C14: C14 owns source-local setting, cosmology, proper nouns, named events, source-specific quest lore, donor-world timeline, and source-specific history. C07 may reference them but must not generalize them.
- C07 vs runtime/backend: C07 records conversion-stage scenario evidence and routing. Runtime/backend owners decide later whether anything becomes quest state, objective trackers, event logs, branch state, save-state nodes, or database rows.
- C07 vs live-play/sourcebook: C07 is not GM script, not player-facing adventure prose, not boxed text, and not sourcebook adventure presentation.
- C07 vs Batch A campaign/world/consequence owners: C07 records scenario-family conversion pressure and routing; final campaign structure, canon events, consequence mechanics, reward mechanics, and world-state doctrine remain with proper owners.

## 11. Composite mission/scenario/adventure record handling

Composite C07 records may represent a scenario container, an adventure-path fragment, a mission arc, or a mixed hook/objective/consequence structure only while preserving composition references. Composite handling must use C00 parent_record_refs, child_record_refs, cross_reference_records, construct_refs, outcome_refs, and provenance_refs instead of merging actors, items, places, hazards, tables, maps, factions, or source-local lore into C07.

Composite records must split or route child records when a component has a stable owner. A composite record may describe that a scenario contains a rescue target, locked site, hazard pressure, route complication, and reward reference, but C01/C11, C06, C09/B10, B08, C02/B05, and other owners remain responsible for their own records or procedures.

## 12. Parent, child, and satellite record handling

Parent C07 records may collect scenario-family structure; child C07 records may represent objective structures, branch structures, hooks, episode fragments, or scene-chain evidence. Satellite records may hold source-local notes, rejected donor elements, evidence-only boxed-text markers, or owner handoff notes.

Parent/child/satellite links are provenance and composition references, not runtime quest trees, objective trackers, branch state, event logs, save-state nodes, or final adventure outlines. Any unresolved child or satellite owner routes to the proper C-family owner, Batch B pressure file, C14, legal/IP review, runtime_review, human_review, or `pending_schema`.

## 13. Source-local and legal/IP handling

C07 must preserve source-local and legal/IP handling for donor adventure names, scenario names, quest names, named NPCs, named places, named factions, named gods, named items, named events, named timelines, named cosmology, source-specific scenario lore, source-specific prose, donor source-specific prose, license-specific expressions, verbatim-similar descriptions, boxed text, read-aloud text, map keys, protected art/map references, and donor-world assumptions.

Source-local/legal/IP/C14 review is required whenever a donor scenario element contains proper nouns, protected setting assumptions, source-specific quest lore, source-specific timeline, named cosmology, donor-world history, or expression that cannot be safely stripped to a reusable conversion pattern. C07 may reference those elements but must not generalize them.

## 14. Rejected donor element handling

C07 rejected donor element handling uses C00 `rejected_donor_elements` and `rejected_import` posture. Rejected donor elements include donor adventures, donor scenario formats, donor quest formats, donor boxed text, donor read-aloud prose, donor scene numbers, donor encounter numbers, donor quest stages, donor objective labels, donor reward values, donor XP/treasure awards, donor branch labels, donor map keys, donor pacing notes, donor required outcomes, donor railroad assumptions, donor field names, donor proper nouns, named NPCs/places/factions/events/timelines, and donor cosmology when they are proposed as Astra defaults.

Rejected material may remain as source evidence, donor tags, source-local notes, legal/IP review notes, or C14 review notes. Rejection does not delete provenance and does not convert donor structure into Astra final mechanics.

## 15. Canon eligibility and review routing

C07 preserves C00 canon eligibility and review routing. C07 may mark a stripped reusable scenario pattern as eligible for canon review, not_reviewed, candidate, accepted_with_limits, rejected, source_local_only, or blocked according to C00 posture, but C07 never promotes canon, does not accept canon, and cannot create canon events or an accepted canon timeline.

Named events, named histories, named worlds, named planes, named cultures, named gods, proper nouns, source-specific quest lore, donor-world timeline, and source-specific history route to C14 and canon_review. C07 only records conversion evidence and routing.

## 16. Confidence, validation, and escalation routing

C07 must preserve boundary_confidence, extraction_confidence, conversion_confidence, validation, lineage, composition, and cross-reference posture from C00. Low or blocked confidence escalates to extraction_repair, human_review, legal/IP review, C14 review, runtime_review, Batch B owner review, or `pending_schema` as appropriate.

Validation should confirm that C07 owns only scenario-structure grammar, that donor leakage is rejected, that evidence refs remain intact, that handoffs are references rather than schema inheritance, and that runtime/canon/sourcebook/live-play boundaries remain explicit.

## 17. Hidden-state and protected-truth boundary

C07 may preserve hidden-state and protected-truth boundary language for spoilers, secret objectives, concealed patrons, false hooks, protected branch evidence, mystery solutions, trap revelations, hidden maps, unknown consequences, and source-local truth claims. Protected truth must remain in source evidence, source_local_boundary, hidden/protected-truth posture, or review refs.

C07 must not expose protected truth, decide live player knowledge, create hidden-information runtime state, create reveal procedure, or convert hidden scenario evidence into player-facing truth.

## 18. Runtime boundary

C07 runtime boundary is strict. C07 must not define runtime quest state, runtime objective state, runtime consequence state, branch state, event logs, save-state nodes, database quest rows, entity/component/event schemas, command lifecycle, context packets, backend quest schemas, scenario execution engines, encounter trackers, live-play scripts, runtime branch logic, objective trackers, quest trackers, database rows, save-state, runtime/backend persistence, or backend adventure schemas.

C07 records may note that runtime/backend concerns exist, but runtime/backend owners decide later whether anything becomes quest state, objective trackers, event logs, branch state, save-state nodes, database rows, entity/component/event schemas, command lifecycle, context packets, backend quest schemas, scenario execution engines, encounter trackers, or live-play scripts.

## 19. Canon/sourcebook/live-play/training boundary

C07 is not canon/sourcebook/live-play/training authority. It does not write canon events, accepted canon timeline, sourcebook adventure prose, boxed text, read-aloud text, GM narration, GM scripts, player-facing adventure prose, live-play scripts, accepted lexicon, training examples, evaluation gold data, final adventure presentation, or donor adventure prose.

Examples may illustrate routing only. They are not schema authority beyond the C07 doctrine assertions they demonstrate.

## 20. Missing-schema fallback

If mission/scenario/adventure evidence points to content with no stable C-family owner, C07 routes that component to `pending_schema` with source evidence, provenance refs, source-local/legal/IP posture, rejected donor elements if needed, confidence posture, and escalation notes. C07 must not invent new registry status vocabulary, create a new family, merge ownership from another family, or use Batch B procedure terms as substitute C07 schema fields.

## 21. Examples of good and bad C07 usage

Good C07 usage:
- Preserve a donor rescue mission as C07 scenario-structure evidence with objective posture, C01/C11 routing for the rescue target, C06 routing for the site, B01 scene-chain pressure, and source-local handling for named places.
- Preserve a donor heist hook as C07 mission classification with C02 clue-object refs, C05 patron/faction refs, B02 consequence-trigger pressure, B05 reward pressure, and rejected donor reward values.
- Preserve a route-based adventure fragment as C07 adventure-path fragment evidence with C06 route/site refs, B08 travel pressure, C09 hazard refs, C10 complication-table refs, and protected-truth notes for hidden branches.
- Preserve a faction job as C07 objective structure while routing the institution to C05, social negotiation pressure to B09, and source-specific faction names to C14/legal/IP review.

Bad C07 usage:
- Convert donor quest stages into an Astra runtime quest state machine.
- Treat donor scene numbers, encounter numbers, boxed text, read-aloud prose, map keys, branch labels, objective labels, or pacing notes as C07 schema labels.
- Turn donor XP awards, treasure awards, reward values, or required outcomes into final Astra reward economy or value flow.
- Encode a railroad procedure, required player choices, scripted scene execution, encounter balance, or branch resolution math as C07 doctrine.
- Promote donor adventure names, named NPCs, named places, named factions, named events, named timelines, named gods, donor cosmology, or source-specific scenario lore as Astra canon.
- Use donor adventure/quest/scenario field names as C07 schema labels.

## 22. Minimum tests or assertions

Minimum C07 tests or assertions should verify that:
- the C07 file exists at the registry path;
- all required sections are present;
- C07 declares ownership and non-ownership;
- C07 inherit/include `AstraContentRecordBase` and preserves C00 provenance, legal/IP, rejected donor element, canon eligibility, confidence, validation, lineage, composition, and cross-reference posture;
- C07 record grammar is doctrine-level only and not runtime/database/quest-state/final adventure format/scene execution/encounter procedure/sourcebook adventure prose/boxed text/canon event timeline;
- donor adventure/scenario/quest/scene-chain/objective/reward/boxed-text/field-name/proper-noun/cosmology leakage is rejected as Astra defaults;
- B01, B02, B05, B08, B09, and B10 handoffs are present without Batch B schema inheritance;
- C01-C14 and `pending_schema` handoffs are present without cross-family inheritance;
- runtime, canon, sourcebook, live-play, hidden-state, source-local, and legal/IP boundaries are preserved;
- the registry C07 posture is draft/schema-draft/designed/not_reviewed without promotion to current/canon/runtime/stable/tested.

## 23. Acceptance criteria

C07 is acceptable when:
- C07 file exists at `docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md`;
- C07 remains conversion-stage/canon-review schema doctrine only;
- C07 includes C00 base inheritance requirements;
- C07 does not import donor adventure formats, quest formats, scene chains, boxed text, read-aloud text, reward values, XP/treasure awards, branch labels, map keys, railroad assumptions, field labels, proper nouns, named NPCs/places/factions/events/timelines, or cosmology as Astra schema;
- C07 does not define final adventure design, scene procedure, encounter procedure, action procedure, travel procedure, reward economy, runtime quest state, objective state, branch state, event logs, database schema, live-play script, canon events, sourcebook adventure prose, or accepted lexicon;
- C07 has clear Batch B handoffs and cross-family handoffs;
- C07 includes source-local/legal/IP and rejected-import handling;
- C07 registry posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01/C02/C03/C06/C09/C10 registry posture is preserved;
- C04, C05, C08, and C11-C14 are not promoted.

## 24. Follow-up handoff to C05

The follow-up handoff to C05 is limited to faction/institution record-family doctrine. C07 can route patrons, enemies, authorities, guilds, cults, governments, institutions, social bodies, and institutional objectives to C05, but C07 must not draft C05 fields, import B09 procedure as schema, or turn faction scenario roles into accepted faction canon.

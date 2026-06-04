# C05 Faction/Institution Record Schema Doctrine

## 1. Purpose and status

C05 defines Batch C conversion-stage and canon-review schema doctrine for faction, institution, sect, guild, corporation, empire, court, cult, order, government, authority, organization, rank, standing, reputation, relationship, patronage, jurisdiction, allegiance, institutional-role, and similar organized-social-body records. It exists to preserve organized social body evidence and review routing without letting donor faction formats, donor institution formats, donor reputation systems, donor standing systems, donor rank structures, donor relationship scores, donor faction clocks, donor patron rules, donor organization charts, donor field names, donor proper nouns, or donor cosmology become Astra defaults.

Status posture:
- C05 is a schema-draft doctrine file.
- C05 is not current canon, not runtime-ready, not stable_for_family, not stable_cross_family, and not tested_minimum.
- C05 records are conversion-stage/canon-review artifacts; they are not final faction mechanics, final social procedure, final reputation math, final standing math, faction clock procedure, runtime faction clocks, runtime faction state, faction AI, relationship AI, institutional simulation, faction turn procedure, diplomacy procedure, social encounter procedure, acquisition/requisition procedure, reward economy, jurisdiction enforcement procedure, canon faction histories, accepted canon politics, sourcebook faction prose, live-play behavior, canon promotion, or donor faction/reputation-system import.
- C05 does not accept canon, does not promote canon, does not define accepted lexicon, and does not decide live-play behavior.

## 2. Owner layer

Owner layer: Batch_C schema family doctrine.

C05 supports conversion intake, conversion output, canon review, legal/IP review, C14 source-local review, Batch B handoff review, C01 actor review, C06 place/jurisdiction review, C07 mission/scenario review, C10 table/oracle review, C13 visual evidence review, and later runtime/backend review. Batch B operational files remain doctrine-facing pressure only; they are not C05 schema fields and are not inherited by C05 records.

## 3. What C05 owns

C05 owns conversion-stage record-family grammar for:
- factions;
- institutions;
- sects;
- guilds;
- corporations;
- empires;
- courts;
- cults;
- orders;
- governments;
- authorities;
- organizations;
- rank structures;
- standing/reputation structures;
- relationship structures;
- patronage structures;
- jurisdictions;
- allegiances;
- institutional roles;
- donor constructs that behave like organized-social-body evidence even when the source uses a faction entry, reputation track, rank table, patron rule, organization chart, jurisdiction note, guild benefit, faction clock, relationship score, or social standing field.

C05 owns faction/institution classification and routing posture for conversion and canon review. It records how an organized-social-body construct was identified, what organization classification posture applies, what scale/scope posture applies, what authority/jurisdiction posture exists, what membership/rank posture exists, what standing/reputation posture exists, what relationship/patronage posture exists, what location/reference posture exists, what actor/reference posture exists, what item/resource/reference posture exists, what scenario/reference posture exists, what hazard/environment/reference posture exists, what table/oracle reference posture exists, what source-local/canon-review posture applies, what hidden/protected-truth posture applies, and what legal/IP posture applies.

C05 owns the organization identity conversion record and its routing evidence. C05 does not automatically own members, leaders, headquarters, territories as places, faction missions, faction gear, faction-taught abilities, hazards, tables, visual organization charts, source-local political lore, or runtime state associated with that organization.

## 4. What C05 must not own

C05 must not own or define:
- final mechanics;
- final faction mechanics;
- final social procedure;
- final reputation math;
- final standing math;
- faction clock procedure;
- runtime faction clocks;
- runtime faction state;
- faction AI;
- relationship AI;
- institutional simulation;
- faction turn procedure;
- diplomacy procedure;
- social encounter procedure;
- acquisition/requisition procedure;
- reward economy;
- jurisdiction enforcement procedure;
- canon faction histories;
- accepted canon politics;
- sourcebook faction prose;
- live-play behavior;
- accepted lexicon;
- canon acceptance;
- canon promotion;
- final ranks, rank benefits, reputation points, standing values, faction clocks, faction turn timing, diplomacy DCs, loyalty values, influence values, favor currency, requisition prices, legal penalties, relationship scores, institutional AI behaviors, faction-resource values, territory-control values, reaction tables, or political history canon.

C05 does not own final rank ladders, final reputation/standing tracks, final relationship rules, final patronage benefits, final jurisdiction enforcement math, final influence or favor currency, final faction turn timing, final organization chart semantics, or final social consequences. Those details may be preserved as source evidence, donor tags, source-local notes, rejected donor elements, or handoff notes only.

## 5. C00 inheritance and required base posture

Every durable C05 record must inherit/include `AstraContentRecordBase` from C00 before any C05-specific shaping. C05 preserves C00 packet_refs, source_evidence_refs, construct_refs, outcome_refs, provenance_refs, source_local_boundary, rejected_donor_elements, canon_eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture.

C05 records must keep the C00 distinction between source evidence, conversion classification, rejected donor elements, source-local boundaries, canon eligibility, validation status, lineage, parent/child records, satellite records, and cross-reference records. C05 cannot drop provenance merely because a donor faction, institution, rank ladder, reputation track, patron relationship, jurisdiction note, or organization chart appears familiar or easy to generalize.

## 6. Faction/institution family scope and classification

C05 classifies faction/institution records by conversion/review role, not by final social mechanics. Neutral Astra-facing classification may include:
- organization classification posture;
- scale/scope posture;
- authority/jurisdiction posture;
- membership/rank posture;
- standing/reputation posture;
- relationship/patronage posture;
- location/reference posture;
- actor/reference posture;
- item/resource/reference posture;
- scenario/reference posture;
- hazard/environment/reference posture;
- table/oracle reference posture;
- source-local/canon-review posture;
- hidden/protected-truth posture;
- legal/IP posture.

Classification labels are review routing signals only. They do not define final ranks, rank benefits, reputation points, standing values, faction clocks, faction turn timing, diplomacy DCs, loyalty values, influence values, favor currency, requisition prices, legal penalties, relationship scores, institutional AI behaviors, faction-resource values, territory-control values, reaction tables, or political history canon.

## 7. C05 record grammar, doctrine-level only

The following compact shape is doctrine grammar only. It is not a runtime schema, not a database schema, not a faction-clock schema, not a reputation system, not a relationship simulation, not final social mechanics, not sourcebook faction prose, and not canon political history.

```yaml
C05FactionInstitutionRecord:
  extends: AstraContentRecordBase
  schema_family: C05
  organization_classification_posture: faction | institution | sect | guild | corporation | empire | court | cult | order | government | authority | organization | institutional_role | relationship_structure | patronage_structure | jurisdiction_structure | allegiance_structure | mixed | uncertain | source_local_only | pending_schema
  scale_scope_posture: individual_cell | local | regional | multi_region | world_scale | planar_or_cosmic_claim | networked | unknown | source_local_only
  authority_jurisdiction_posture: none | claimed | delegated | contested | legal_or_regulatory | territorial_reference_required | C06_reference_required | B09_pressure_only | source_local_only | pending_schema
  membership_rank_posture: none | evidence_only | rank_structure_evidence | membership_access_evidence | C01_actor_refs_required | donor_rank_names_quarantined | source_local_only | pending_schema
  standing_reputation_posture: none | evidence_only | donor_track_quarantined | B09_pressure_only | table_reference_required | source_local_only | pending_schema
  relationship_patronage_posture: none | evidence_only | patronage_evidence | relationship_evidence | B05_pressure_only | B09_pressure_only | donor_relationship_scores_quarantined | source_local_only | pending_schema
  location_reference_posture: none | C06_reference_required | C13_visual_reference_required | source_local_only | pending_schema
  actor_reference_posture: none | C01_reference_required | leaders_or_agents_split_to_C01 | source_local_only | pending_schema
  item_resource_reference_posture: none | C02_reference_required | C04_reference_required | C08_reference_required | C12_reference_required | B05_pressure_only | source_local_only | pending_schema
  scenario_reference_posture: none | C07_reference_required | B01_context_only | B02_pressure_only | source_local_only | pending_schema
  hazard_environment_reference_posture: none | C09_reference_required | B10_pressure_only | source_local_only | pending_schema
  table_oracle_reference_posture: none | C10_reference_required | donor_table_quarantined | source_local_only | pending_schema
  source_local_canon_review_posture: reusable_pattern_review | source_local_only | C14_reference_required | legal_ip_review_required | requires_human_review | not_eligible
  hidden_protected_truth_posture: none | evidence_only | spoiler_sensitive | protected_truth | unreliable_claim | runtime_owner_required
  required_family_handoffs: [C01 | C02 | C03 | C04 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema]
```

The YAML-like block above is doctrine grammar for conversion/canon-review schema doctrine only. It avoids donor faction/institution/reputation field names as Astra labels. It does not create final mechanics, does not create database rows, does not create backend faction schemas, does not create faction clocks, does not create reputation math, does not create relationship trackers, and does not create canon political history.

## 8. Donor faction, institution, reputation, standing, rank, relationship, and field-name handling

Donor exact faction structures, donor institution formats, rank names, reputation tracks, standing tracks, relationship scores, faction clocks, influence values, favor values, faction turns, patron rules, membership benefits, requisition rules, reaction tables, organization charts, and faction field names may be preserved only as source evidence, donor tags, source-local notes, or rejected donor elements, not as Astra schema labels or final mechanics.

C05 rejects donor faction formats, donor institution formats, donor reputation systems, donor standing systems, donor rank structures, donor relationship scores, donor faction clocks, donor influence/favor values, donor faction turns, donor patron rules, donor membership benefits, donor requisition rules, donor reaction tables, donor organization charts, donor field names, donor proper nouns, named factions, named institutions, named leaders, named histories, named wars, named cultures, named locations, named gods, named cosmology, and donor cosmology as Astra defaults.

Donor faction names, institution names, sect names, guild names, corporation names, empire names, court names, cult names, government names, named ranks, named patrons, named leaders, named histories, named wars, named cultures, named locations, named gods, named cosmology, source-specific political lore, and source-specific prose must route to source-local/legal/IP/C14 review unless canon review later accepts stripped reusable patterns.

## 9. Social, acquisition, location, scenario, actor, item, hazard, table, and source-local handoffs

Batch B handoffs:
- C05 references B09 for social, faction, contact, institution, reputation, patron, authority, jurisdiction, negotiation, standing, institutional access, and relationship pressure, but B09 is not C05 schema.
- C05 references B05 for acquisition, reward, requisition, value flow, patronage, institutional access, faction supply, compensation, and resource-allocation pressure, but B05 is not C05 schema.
- C05 references B08 when factions/institutions control routes, territories, exploration access, discovery access, travel restrictions, or region traversal pressure, but B08 is not C05 schema.
- C05 references B10 when factions/institutions create opposition, active threat triggers, hazards, patrols, enforcement, escalation, quarantine, or threat-contact pressure, but B10 is not C05 schema.
- C05 may reference B01 when a faction/institution is scene/activity/encounter context, but B01 is not C05 schema.
- C05 may reference B02 when faction/institution pressure affects action declaration, cost commitment, or resolution trigger pressure, but B02 is not C05 schema.
- Batch B procedure terms must not become C05 schema fields.

Cross-family handoffs:
- C05 -> C01 for members, leaders, agents, patrons, contacts, enemies, rank-holders, faction actors, institution staff, or representative NPCs.
- C05 -> C02 for faction gear, institutional resources, equipment access, supply, requisition items, tokens, documents, licenses, uniforms, tools, and material assets.
- C05 -> C03 for faction-taught abilities, institutional doctrines, restricted techniques, oaths, commands, authority powers, social powers, ritual powers, or rank-gated capabilities.
- C05 -> C04 for relics, implants, installable assets, bonded institutional assets, faction artifacts, cyberware/biotech access, institutional augmentations, or restricted special assets.
- C05 -> C06 for headquarters, territories, jurisdictions, settlements, regions, routes, stations, temples, courts, guildhalls, bases, offices, controlled sites, or institutional places.
- C05 -> C07 for faction missions, institutional scenarios, patron jobs, conflicts, arcs, objectives, scenario roles, quest hooks, consequences, and adventure-path functions.
- C05 -> C08 for faction vehicles, ships, platforms, stations, fleets, mechs, bases, mobile institutions, institutional infrastructure, or platform-scale assets.
- C05 -> C09 for faction-controlled hazards, quarantines, sanctions, dangerous sites, environmental regulation, institutional containment, disasters, hostile territory pressure, or enforcement hazards.
- C05 -> C10 for faction/institution/contact/patron/rumor/reputation/reaction tables, random faction generators, institution tables, relationship tables, or social oracles.
- C05 -> C11 for companion/summon affiliations, controlled cohorts, followers, pets, minions, bound servants, relationship-control structures, or faction-managed companions.
- C05 -> C12 for faction crafting, institutional salvage, requisition projects, guild recipes, industrial processes, supply chains, repair yards, upgrade programs, and resource extraction.
- C05 -> C13 for faction maps, jurisdiction diagrams, organization charts, insignia diagrams, route overlays, social diagrams, or visual institutional evidence.
- C05 -> C14 for source-local setting, cosmology, named histories, named cultures, named governments, named religions, named ideologies, named wars, named institutions, donor-world politics, source-specific lore, and proper nouns.
- C05 -> pending_schema when no stable C-family owner exists.

## 10. C05 cross-family overlap rules

- C05 vs C07: C05 owns the faction/institution record. C07 owns mission/scenario/adventure role, objective, event, or adventure function involving that faction.
- C05 vs B09: C05 owns conversion-stage faction/institution identity and routing. B09 owns social/faction/contact/institutional interaction procedure.
- C05 vs B05: C05 owns institutional identity and access posture. B05 owns acquisition/reward/requisition/value-flow procedure.
- C05 vs C01: C05 owns the organization. C01 owns individual actors, NPCs, leaders, agents, or member records.
- C05 vs C06: C05 owns the institution/faction. C06 owns headquarters, territories, jurisdictions as places, settlements, regions, and controlled sites.
- C05 vs C10: C05 owns converted faction/institution records. C10 owns faction/reputation/contact/random-institution tables and row provenance.
- C05 vs C14: C14 owns source-local cosmology, proper nouns, political histories, named wars, named governments, named cultures, named gods, ideologies, donor-world assumptions, and source-specific lore. C05 may reference them but must not generalize them.
- C05 vs runtime/backend: C05 records conversion-stage organization evidence and routing. Runtime/backend owners decide later whether anything becomes faction state, faction clocks, relationship trackers, diplomacy trackers, save-state nodes, database rows, or faction AI.
- C05 vs live-play/sourcebook: C05 is not GM script, not player-facing faction prose, not sourcebook faction presentation, and not live-play social behavior.
- C05 vs Batch A campaign/world/social/consequence owners: C05 records faction/institution conversion pressure and routing; final faction mechanics, campaign politics, consequence mechanics, relationship mechanics, and world-state doctrine remain with proper owners.
- C05 vs C02/C03/C04/C08/C09/C11/C12/C13: use references and satellite records, not inheritance or merged schemas.

## 11. Composite faction/institution record handling

A donor entry may combine an organization, leader statblock, headquarters, territory, mission hook, rank table, reward list, reputation track, organization chart, hazard response, and source-local political history. C05 may keep a parent composite record only to preserve conversion evidence and lineage while splitting durable family ownership into referenced or satellite records.

Composite handling must identify which evidence remains C05 organization posture and which evidence routes to C01, C02, C03, C04, C06, C07, C08, C09, C10, C11, C12, C13, C14, Batch B pressure notes, or `pending_schema`. C05 must not merge those families into one inherited faction schema merely because a donor source presented them together.

## 12. Parent, child, and satellite record handling

C05 may use parent, child, and satellite records to preserve lineage and composition without merging ownership. Parent records may represent a donor faction/institution cluster, umbrella organization, coalition, court, government, sect network, corporate family, or institutional archetype under review. Child records may represent branches, cells, chapters, departments, offices, courts, rank strata as evidence partitions, subordinate institutions, or relationship partitions when the donor evidence requires separate conversion review.

Satellite records carry C01, C02, C03, C04, C06, C07, C08, C09, C10, C11, C12, C13, C14, Batch B pressure, or `pending_schema` material. Satellite records must use references and provenance rather than C05 inheritance or merged schemas.

## 13. Source-local and legal/IP handling

C05 must preserve source_local_boundary and legal/IP posture for donor faction names, institution names, sect names, guild names, corporation names, empire names, court names, cult names, government names, named ranks, named patrons, named leaders, named histories, named wars, named cultures, named locations, named gods, named cosmology, named ideologies, source-specific political lore, and source-specific prose.

Source-local content routes to C14/source-local/legal/IP review unless and until a stripped reusable organizational pattern is accepted by the proper canon review owner. C05 may record source-local/legal/IP evidence and routing; it must not normalize protected names, donor-world politics, donor cosmology, or source-specific faction prose into Astra schema labels or accepted canon.

## 14. Rejected donor element handling

C05 must preserve rejected_donor_elements for donor exact faction structures, donor institution formats, donor reputation systems, donor standing systems, donor rank structures, donor relationship scores, donor faction clocks, donor influence values, donor favor values, donor faction turns, donor patron rules, donor membership benefits, donor requisition rules, donor reaction tables, donor organization charts, donor field names, donor proper nouns, donor cosmology, and donor political history canon that cannot become Astra defaults.

A rejected donor element may be retained as audit evidence with packet_refs, source_evidence_refs, provenance_refs, donor tags, source-local notes, and a reason for rejection. Rejection preserves auditability; it does not authorize silent import, canon promotion, accepted lexicon creation, runtime implementation, or final mechanics.

## 15. Canon eligibility and review routing

C05 canon eligibility is a review signal only. C05 may mark stripped reusable organized-social-body patterns as eligible_for_pattern_review, source_local_only, requires_human_review, blocked, or not_eligible, but C05 never promotes canon, does not accept canon, does not create accepted canon politics, and does not define accepted faction history.

Named donor factions, named institutions, named governments, named religions, named ideologies, named wars, named leaders, named patrons, named cultures, named locations, donor-world politics, donor cosmology, source-specific political lore, and proper nouns normally route to C14/source-local/legal/IP review. A reusable pattern can be canon-review eligible only after donor expression, protected names, donor mechanics, donor cosmology, and donor political history have been stripped or quarantined.

## 16. Confidence, validation, and escalation routing

C05 confidence and validation fields inherit C00 posture. Low or blocked confidence must escalate when source evidence is ambiguous, a donor faction entry and table conflict, a donor rank structure cannot be separated from membership benefits, a reputation track implies final math, a faction clock implies runtime state, a named institution appears source-local, a jurisdiction claim depends on donor-world politics, or an organization overlaps C01/C06/C07/C10/C13/C14 ownership.

Validation checks should confirm that C05 record grammar remains doctrine-level only, provenance is present, rejected donor elements are tracked, source-local boundaries are preserved, Batch B procedure terms are not converted into schema fields, and cross-family handoffs use references rather than inheritance.

## 17. Hidden-state and protected-truth boundary

C05 may record hidden-state and protected-truth boundary posture as review metadata when an organization contains secret membership, hidden leaders, covert allegiances, false fronts, confidential rank structure, concealed patrons, unreliable reputation evidence, protected institutional truth, secret jurisdictions, hidden enforcement, or spoiler-sensitive political information. That posture is not runtime hidden-information state.

Protected truth remains evidence and review routing. C05 must not reveal it as public canon, turn it into hidden faction state, build relationship trackers, build diplomacy trackers, define secret faction clocks, or define live-play revelation procedure. B09 handles social/faction/contact pressure, B10 handles active threat trigger pressure, C01 handles secret actors, C06 handles hidden places, C13 handles visual evidence, C14 handles source-local lore, and runtime/backend owners decide later whether any hidden information becomes executable state.

## 18. Runtime boundary

C05 forbids runtime faction state, runtime faction clocks, relationship trackers, diplomacy trackers, save-state nodes, database faction rows, entity/component/event schemas, command lifecycle, context packets, backend faction schemas, institutional simulation, faction AI, relationship AI, faction turn engines, influence/favor ledgers, reputation point trackers, standing value trackers, legal enforcement automation, and live-play social behavior.

C05 records conversion-stage organization evidence and routing only. Runtime/backend owners decide later whether any converted organization becomes faction state, faction clocks, relationship trackers, diplomacy trackers, save-state nodes, database rows, entity/component/event schema participants, context packet inputs, backend faction schemas, institutional simulation inputs, faction AI inputs, or live-play social behavior. C05 must not pre-commit those choices.

## 19. Canon/sourcebook/live-play/training boundary

C05 is not canon/sourcebook/live-play/training authority. It does not produce canon faction histories, accepted canon politics, canon governments, accepted ideologies, accepted cultures, sourcebook faction prose, player-facing faction writeups, GM scripts, social encounter procedure, reputation procedure, standing procedure, diplomacy procedure, jurisdiction procedure, live-play social behavior, or training examples as schema authority.

Training examples may illustrate conversion posture, but training examples do not become C05 schema fields, final faction mechanics, final reputation math, accepted lexicon, canon political history, sourcebook faction prose, runtime faction state, or live-play behavior.

## 20. Missing-schema fallback

When an organized-social-body donor construct includes material that lacks a stable C-family owner, C05 routes the unresolved portion to `pending_schema` with provenance, source evidence, rejected donor element posture when needed, and escalation notes. C05 must not fill another family gap by defining companion schema, crafting schema, visual schema, source-local setting schema, runtime schema, backend schema, or Batch B procedure.

`pending_schema` routing must preserve packet_refs, source_evidence_refs, source_local_boundary, rejected_donor_elements, canon_eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture.

## 21. Examples of good and bad C05 usage

Good C05 usage:
- Preserve a donor guild as a C05 faction/institution record with source evidence, membership/rank posture, C01 refs for named leaders, C06 refs for guildhalls and jurisdiction places, C02 refs for licenses and uniforms, B09 institutional access pressure, and C14 review for protected guild names or source-specific lore.
- Preserve a donor reputation track as C05 standing/reputation evidence with the donor reputation system quarantined, B09 pressure notes, C10 refs for any reputation table, and no imported reputation points, standing values, rank benefits, or reaction tables as Astra mechanics.
- Preserve a patron institution as C05 organization identity with B05 acquisition/reward/requisition/value-flow pressure and C07 patron-job refs, without importing donor patron rules, favor currency, membership benefits, requisition prices, or compensation math.
- Preserve a government jurisdiction claim as C05 authority/jurisdiction posture with C06 place refs, B08 route/access pressure, B10 enforcement threat pressure, and C14/legal/IP review for named governments, named wars, named cultures, named gods, or donor cosmology.

Bad C05 usage:
- Convert donor rank names, donor rank benefits, reputation points, standing values, relationship scores, influence values, favor currency, faction clocks, faction turn timing, legal penalties, or requisition prices into Astra default fields.
- Treat a donor faction, institution, government, cult, guild, corporation, empire, court, named leader, named history, named war, named culture, named location, named god, or donor cosmology as Astra canon.
- Use donor faction/institution/reputation/standing/rank/relationship/patron/requisition/reaction/organization-chart field names as C05 schema labels.
- Turn a faction mission, patron job, arc, objective, or consequence into C07 mission/scenario/adventure structure inside C05.
- Turn headquarters, territories, jurisdictions as places, settlements, routes, or controlled sites into C06 geography inside C05.
- Turn social/faction/contact/institutional interaction procedure, acquisition/requisition procedure, travel restriction procedure, threat escalation procedure, faction AI, relationship simulation, or runtime faction clocks into C05 schema.

## 22. Minimum tests or assertions

Minimum C05 tests/assertions must verify that:
- the C05 file exists at the registry path;
- all required C05 sections are present;
- C05 declares ownership and non-ownership boundaries;
- C05 inherits/includes `AstraContentRecordBase` and preserves C00 provenance, source-local, rejected donor, canon eligibility, confidence, validation, lineage, composition, cross-reference, and legal/IP posture;
- C05 record grammar is doctrine-level only and not runtime/database/faction-clock/reputation-system/relationship-simulation/final-social-mechanics/sourcebook-faction-prose/canon-political-history;
- donor faction/institution/reputation/standing/rank/relationship/faction-clock/influence/favor/faction-turn/patron/membership/requisition/reaction/organization-chart/field-name/proper-noun/cosmology leakage is rejected as Astra defaults;
- B09, B05, B08, B10, B01, and B02 are handoffs only, not C05 schema inheritance;
- cross-family handoffs cover C01, C02, C03, C04, C06, C07, C08, C09, C10, C11, C12, C13, C14, and `pending_schema`;
- source-local/legal/IP, rejected donor element, canon eligibility, hidden-state/protected-truth, runtime, sourcebook, live-play, and training boundaries are preserved;
- registry C05 posture is draft/schema-draft/designed/not_reviewed without current/canon/runtime/stable/tested promotion.

## 23. Acceptance criteria

C05 is acceptable when:
- C05 file exists at `docs/doctrine/schema/C05_faction_institution_record_schema.md`;
- C05 remains conversion-stage/canon-review schema doctrine only;
- C05 includes C00 base inheritance requirements;
- C05 does not import donor faction formats, donor institution formats, reputation systems, rank structures, relationship scores, faction clocks, faction turns, influence/favor values, membership benefits, requisition rules, reaction tables, organization charts, field labels, proper nouns, named factions/institutions/leaders/histories/wars/cultures/locations/gods, or cosmology as Astra schema;
- C05 does not define final faction mechanics, social procedure, reputation math, faction clocks, relationship simulation, faction AI, runtime faction state, diplomacy trackers, database schema, canon faction history, sourcebook faction prose, live-play behavior, canon, or accepted lexicon;
- C05 has clear Batch B handoffs and cross-family handoffs;
- C05 includes source-local/legal/IP and rejected-import handling;
- C05 registry posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01/C02/C03/C06/C07/C09/C10 registry posture is preserved;
- C04, C08, and C11-C14 are not promoted;
- focused tests pass;
- full suite passes.

## 24. Follow-up handoff to C13

C05 intentionally leaves faction maps, jurisdiction diagrams, organization charts, insignia diagrams, route overlays, social diagrams, relationship diagrams, and visual institutional evidence to C13. C05 may reference C13 records for visual evidence and may preserve donor organization-chart evidence as source evidence or rejected donor elements, but C05 must not define visual schema, map schema, diagram semantics, chart layout, iconography standards, or sourcebook visual presentation.

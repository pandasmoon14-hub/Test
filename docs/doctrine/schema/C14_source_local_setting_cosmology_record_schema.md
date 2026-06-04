# C14 Source-Local Setting/Cosmology Record Schema Doctrine

## 1. Purpose and status

C14 defines Batch C conversion-stage/canon-review schema doctrine for source-local setting, cosmology, metaphysics, proper noun, local law, local faction context, local culture, local history, named entity, named world, named plane, named deity, donor-world assumption, source-specific identity, source-specific lore, and world-specific containment records.

C14 is a containment and review-routing schema family. It is not canon promotion, not Astra-wide cosmology, not final setting law, not final metaphysics, not sourcebook lore, not runtime world state, not donor setting import, and not permission to generalize donor proper nouns.

Status posture:
- C14 is drafted as schema-draft material for Batch C only.
- C14 records are conversion-stage and canon-review artifacts.
- C14 does not make source-local material Astra baseline without later canon review under canon-promotion protocols.
- C14 does not define canon, runtime-ready state, stable_for_family state, stable_cross_family state, tested_minimum posture, sourcebook lore, accepted lexicon, live-play world truth, or final setting truth.

## 2. Owner layer

C14 belongs to Batch C schema doctrine. Its owner layer is Astra Doctrine Council - Schema Working Group, with supporting review from canon_review, lexicon_review, legal/IP review, runtime_review, extraction_repair, and human_review.

C14 sits after C00 shared content record base doctrine and alongside C01-C13 family records. It routes source-local and donor-world identity pressure without absorbing other C-family construct ownership.

## 3. What C14 owns

C14 owns conversion-stage record-family grammar for:
- source-local setting records;
- cosmology records;
- metaphysics records;
- proper noun records;
- local law records;
- local faction context records;
- local culture records;
- local history records;
- named entity records;
- named world records;
- named plane records;
- named deity records;
- donor-world assumption records;
- source-specific identity records;
- source-specific lore records;
- world-specific containment records.

C14 owns containment and review routing for donor-specific material that should not become Astra baseline. It owns source-local classification, donor-identity posture, proper-noun posture, cosmology/metaphysics posture, local-law posture, setting-history posture, culture/faction/context posture, cross-family attachment posture, canon-eligibility posture, legal/IP posture, lexicon-review posture, hidden/protected-truth posture, and rejection/containment posture.

## 4. What C14 must not own

C14 must not own or define:
- final mechanics;
- canon acceptance;
- canon promotion;
- Astra-wide cosmology;
- Astra-wide metaphysics;
- final setting law;
- final sourcebook lore;
- accepted canon history;
- accepted canon geography;
- canon factions;
- canon events;
- canon cultures;
- final lexicon;
- accepted terminology;
- accepted proper nouns;
- runtime world state;
- runtime cosmology state;
- runtime faction state;
- runtime deity state;
- sourcebook prose;
- live-play behavior;
- donor setting import;
- donor cosmology import;
- donor metaphysics import;
- donor pantheon import;
- donor proper noun import;
- donor field names as Astra defaults;
- domain law;
- Path law;
- planar mechanics;
- divine mechanics;
- cultivation law;
- psionic law;
- magic-system law;
- world-state mechanics.

C14 must not define final cosmological origins, planes, gods, universal metaphysics, sourcebook setting truths, canon history, canon geography, accepted proper nouns, final lexicon, domain law, Path law, planar mechanics, divine mechanics, cultivation law, psionic law, magic-system law, or world-state mechanics.

## 5. C00 inheritance and required base posture

Every C14 source-local setting/cosmology record must inherit/include `AstraContentRecordBase` from C00 before applying C14-specific classification. C14 preserves `packet_refs`, `source_evidence_refs`, `construct_refs`, `outcome_refs`, `provenance_refs`, `source_local_boundary`, `rejected_donor_elements`, `canon_eligibility`, `confidence`, `validation`, `lineage`, `composition`, cross-reference, legal/IP posture, review routing, and source-local boundary posture from C00.

C14 may narrow review posture for source-local containment, but it must not remove provenance, source evidence, rejected donor element posture, canon eligibility routing, validation status, lineage, composition, parent/child links, or cross-family references inherited from C00.

## 6. Source-local setting/cosmology family scope and classification

C14 classifies source-local records by conversion/review role, not by canon adoption. A C14 classification describes why material is contained and where review must route it; it does not say the material is accepted as Astra canon.

Neutral Astra-facing classification categories include:
- source-local classification;
- donor-identity posture;
- proper-noun posture;
- cosmology/metaphysics posture;
- local-law posture;
- setting-history posture;
- culture/faction/context posture;
- named entity posture;
- named world posture;
- named plane posture;
- named deity posture;
- cross-family attachment posture;
- canon-eligibility posture;
- legal/IP posture;
- lexicon-review posture;
- hidden/protected-truth posture;
- rejection/containment posture.

These categories are routing labels only. They are not donor proper-noun labels, donor setting labels, donor cosmology labels, donor alignment/cosmology labels, donor identity fields, or donor field names as Astra defaults.

## 7. C14 record grammar, doctrine-level only

The following block is doctrine grammar only. It is not a runtime schema, not a database schema, not a canon setting model, not sourcebook lore, not lexicon acceptance, not Astra-wide cosmology, not final metaphysics, and not donor setting import. It is conversion/canon-review schema doctrine for durable containment and routing records only.

```yaml
C14SourceLocalSettingCosmologyRecord:
  extends: AstraContentRecordBase
  schema_family: C14
  source_local_classification: setting_context | cosmology_context | metaphysics_context | proper_noun_context | local_law_context | local_history_context | culture_context | named_entity_context | named_world_context | named_plane_context | named_deity_context | donor_world_assumption | source_specific_identity | source_specific_lore | world_specific_containment | mixed_source_local_context
  donor_identity_posture: evidence_only | tag_only | source_local_note | legal_ip_review | lexicon_review | rejected_import | quarantine | human_review
  proper_noun_posture: none | source_evidence_only | contained_source_local | lexicon_review_candidate | rejected_donor_element | human_review
  cosmology_metaphysics_posture: none | evidence_only | source_local_only | stripped_pattern_candidate | rejected_import | canon_review_required
  local_law_posture: none | evidence_only | source_local_only | cross_family_handoff_required | rejected_import | canon_review_required
  setting_history_posture: none | evidence_only | source_local_only | timeline_handoff_required | rejected_import | canon_review_required
  culture_faction_context_posture: none | evidence_only | source_local_only | c05_handoff_required | rejected_import | canon_review_required
  cross_family_attachment_posture: none | reference_only | satellite_record | split_required | pending_schema
  legal_ip_posture: not_reviewed | source_local_boundary_required | legal_ip_review_required | rejected_or_quarantined
  lexicon_review_posture: none | flag_only | candidate_requires_review | rejected_as_donor_term
  hidden_protected_truth_posture: none | protected_truth | hidden_from_players | source_only_secret | runtime_review_required
  rejection_containment_posture: none | contained | rejected_donor_element | quarantine | escalation
```

C14 records use references and satellite records, not inheritance or merged schemas, when they touch C01-C13 construct families. C14 must avoid donor proper-noun/setting/cosmology field names as Astra labels.

## 8. Donor proper noun, setting, cosmology, metaphysics, local law, history, culture, and field-name handling

Donor exact names, donor proper nouns, donor setting law, donor cosmology, donor metaphysics, donor pantheons, donor named worlds, donor named planes, donor named gods, donor named factions, donor named cultures, donor named histories, donor named wars, donor named events, donor named places, donor named species, donor named schools, donor named magic systems, donor named elements, donor named religions, donor named technologies, donor named organizations, donor named empires, donor named artifacts, donor field names, donor identity fields, donor alignment/cosmology labels, and donor world assumptions must not become Astra defaults.

Such material may be preserved only as source evidence, donor tags, source-local notes, legal/IP review notes, C14 containment records, or rejected donor elements. Field-name handling must normalize toward neutral Astra-facing routing labels; donor field labels are not schema vocabulary.

C14 explicitly blocks source-local material from becoming Astra baseline without later canon review under canon-promotion protocols.

## 9. Canon eligibility, source-local containment, legal/IP, lexicon, and cross-family handoffs

C14 records canon eligibility and review routing without canon promotion. It preserves source-local containment, legal/IP posture, lexicon-review posture, rejected donor elements, and cross-family references.

Required C14 handoffs:
- C14 -> C01 for source-local creatures, NPCs, species, monsters, named individuals, named ancestry-like entities, source-specific actor identities, and donor-world beings.
- C14 -> C02 for source-local items, gear, materials, named artifacts, currencies, equipment traditions, technologies, trade goods, or donor-world object identities.
- C14 -> C03 for source-local abilities, magic systems, psionic systems, cultivation systems, schools, spell names, techniques, power sources, named elements, deific powers, and local effect laws.
- C14 -> C04 for source-local relics, implants, augmentations, installable assets, artifacts, cyberware/biotech traditions, named modules, bonded assets, and donor-world special assets.
- C14 -> C05 for source-local factions, institutions, governments, religions, sects, cultures, empires, guilds, ideologies, laws, ranks, and social bodies.
- C14 -> C06 for source-local locations, worlds, planes, regions, cities, ruins, megastructures, settlements, cultures-as-places, and local geography.
- C14 -> C07 for source-local missions, scenarios, events, quests, timelines, adventure paths, named conflicts, campaign arcs, and donor-world story structures.
- C14 -> C08 for source-local vehicles, ships, platforms, mechs, stations, bases, fleets, and platform traditions.
- C14 -> C09 for source-local hazards, environments, planar conditions, diseases, poisons, corruption, radiation, weather, regional laws, local exposure pressures, and donor-world environmental laws.
- C14 -> C10 for source-local tables, oracles, generators, prompt lists, donor-world encounter tables, rumor tables, culture tables, map tables, faction tables, and source-specific randomization artifacts.
- C14 -> C11 for source-local companions, summons, followers, pets, cohorts, minions, spirits, bound entities, and donor-world companion traditions.
- C14 -> C12 for source-local crafting, salvage, recipes, materials, technologies, ritual processes, repair traditions, upgrade traditions, and donor-world production laws.
- C14 -> C13 for source-local maps, diagrams, symbols, protected artwork, visual lore, named places on maps, setting diagrams, cosmology diagrams, and visual proper-noun evidence.
- C14 -> pending_schema when no stable C-family owner exists.

Handoffs are references and routing decisions only. They are not schema inheritance, merged schemas, canon acceptance, lexicon acceptance, legal clearance, runtime implementation, sourcebook prose, or donor-world import.

## 10. C14 cross-family overlap rules

C14 vs all C01-C13: C14 owns source-local containment, donor-world identity, proper-noun/cosmology/metaphysics/legal/IP posture, and canon-eligibility routing. The other C-family owns the non-source-local construct type. If a donor construct is both a creature/item/ability/faction/location/scenario/map/etc. and source-local, split into the relevant C-family record plus C14 containment/reference, or keep as C14-only if no reusable Astra pattern exists.

C14 vs canon review: C14 records eligibility and routes review. It does not promote canon.

C14 vs lexicon governance: C14 may flag terminology/proper nouns for lexicon review, but it does not accept lexicon entries or create Astra vocabulary.

C14 vs legal/IP review: C14 preserves legal/IP posture and source-local boundaries; it does not decide legal clearance.

C14 vs runtime/backend: C14 records conversion-stage source-local evidence and routing. Runtime/backend owners decide later whether anything becomes world state, lore index, save-state node, database row, hidden-state packet, or context packet.

C14 vs live-play/sourcebook: C14 is not player-facing lore prose, not GM exposition, not sourcebook setting presentation, and not live-play world truth.

C14 vs Batch A doctrine: C14 cannot override Batch A ontology, cosmology, sourcebook doctrine, lexicon governance, character doctrine, progression doctrine, or Astra-wide metaphysical constraints.

C14 vs donor source: donor vocabulary, donor cosmology, donor proper nouns, donor setting laws, donor pantheons, donor metaphysics, donor technologies, and donor histories remain evidence, source-local containment, or rejected material until canon promotion explicitly accepts a stripped Astra-native pattern.

## 11. Composite source-local record handling

Composite source-local records must be split when they include reusable non-source-local constructs. C14 keeps source-local context, donor-world identity, proper noun, cosmology/metaphysics, local-law, legal/IP, and canon-eligibility routing while C01-C13 records own their construct-specific conversion grammar.

If a composite record cannot be safely split because donor identity, protected lore, or local cosmology is the construct, keep the record C14-only, mark the reusable pattern as blocked or pending, preserve provenance, and route to canon_review, legal/IP review, lexicon_review, or human_review.

## 12. Parent, child, and satellite record handling

Parent, child, and satellite C14 records preserve containment lineage. A parent source-local world, plane, culture, pantheon, empire, history, or donor-world assumption may have child records for proper nouns, local laws, named entities, named events, maps, factions, hazards, items, abilities, or scenarios.

Satellite records must use `parent_record_refs`, `child_record_refs`, and `cross_reference_records` from C00. Satellite references do not grant canon inheritance, lexicon acceptance, runtime activation, legal clearance, or sourcebook truth.

## 13. Source-local and legal/IP handling

C14 source-local and legal/IP handling preserves source-local boundaries, donor tags, evidence-only notes, legal/IP review notes, rejected donor elements, provenance, and review routing. A source-local boundary is a quarantine and review surface, not a license to import donor settings.

Legal/IP posture must be explicit when records include donor exact names, protected artwork references, named worlds, named planes, named gods, named factions, named cultures, named histories, named wars, named events, named places, named species, named schools, named magic systems, named technologies, donor pantheons, donor setting laws, or donor field names.

C14 does not decide legal clearance. It preserves legal/IP posture so legal/IP review can decide whether any stripped Astra-native pattern may proceed.

## 14. Rejected donor element handling

Rejected donor element handling is mandatory when source material includes donor proper nouns, donor setting law, donor cosmology, donor metaphysics, donor pantheons, donor identity fields, donor alignment/cosmology labels, donor field names, protected lore, or donor-world assumptions that cannot be normalized.

Rejected donor elements remain linked to source evidence for audit. Rejection is not deletion; it is a containment decision that blocks donor leakage into Astra defaults and routes the material to quarantine, legal/IP review, lexicon_review, canon_review, or human_review.

## 15. Canon eligibility and review routing

C14 preserves canon eligibility and review routing without canon promotion. A C14 record can mark whether a stripped Astra-native pattern may be eligible for later review, but source-local material, donor proper nouns, donor cosmology, donor metaphysics, donor pantheons, donor setting laws, donor local histories, donor named worlds, donor named planes, donor named gods, donor named factions, donor named cultures, and donor field names are not canon because they appear in C14.

Canon review may later accept a stripped Astra-native pattern under canon-promotion protocols. C14 itself does not promote canon, accept canon, create accepted canon history, create accepted canon geography, create canon factions, create canon events, create accepted proper nouns, or create final lexicon entries.

## 16. Confidence, validation, and escalation routing

C14 confidence and validation signals must cover boundary confidence, extraction confidence, conversion confidence, source-local classification confidence, legal/IP confidence, lexicon-review confidence, canon-eligibility confidence, hidden/protected-truth confidence, and cross-family handoff confidence.

Escalate to human_review, legal/IP review, lexicon_review, canon_review, runtime_review, extraction_repair, or pending_schema when donor identity cannot be separated from a reusable pattern, provenance is missing, source-local boundaries are unclear, hidden truth may be exposed, donor terms might leak into Astra vocabulary, or no stable C-family owner exists.

## 17. Hidden-state and protected-truth boundary

C14 must preserve hidden-state and protected-truth boundary language. Donor secrets, GM-only cosmology, unrevealed deity identity, hidden faction control, false history, concealed local law, secret plane structure, protected proper noun context, or player-facing misinformation is not live-play truth merely because it appears in source-local evidence.

Protected truth must remain protected. C14 records may mark hidden/protected-truth posture and route to canon_review or runtime_review, but C14 must not create hidden-state packets, context packets, player-facing lore, GM exposition, or live-play world truth.

## 18. Runtime boundary

C14 forbids runtime world state, runtime cosmology state, runtime faction state, runtime deity state, lore database rows, save-state nodes, context packets, hidden-state packets, entity/component/event schemas, command lifecycle, backend lore schemas, canon setting models, and live-play world truth.

Runtime/backend owners decide later whether reviewed evidence informs world state, lore index, save-state node, database row, hidden-state packet, context packet, entity/component/event schema, command lifecycle, or backend lore schema. C14 does not define those systems and must not act as a runtime schema or database schema.

## 19. Canon/sourcebook/live-play/training boundary

C14 is not canon sourcebook lore, not final setting prose, not player-facing lore prose, not GM exposition, not sourcebook setting presentation, not live-play behavior, not live-play world truth, not training example authority, and not accepted lexicon.

Training examples may test containment and routing posture, but they must not become sourcebook prose, accepted proper nouns, accepted terminology, canon promotion, canon setting models, runtime world state, or live-play behavior.

## 20. Missing-schema fallback

When source-local material has no stable C-family owner, C14 routes that material to `pending_schema` while preserving provenance, source evidence, source-local boundary, rejected donor element posture, legal/IP posture, canon eligibility, confidence, validation, and escalation notes.

Missing-schema fallback must not cause C14 to absorb permanent ownership of unrelated construct grammar or import donor-world assumptions as Astra defaults.

## 21. Examples of good and bad C14 usage

Good C14 usage:
- Preserve a donor named world as source evidence with legal/IP posture, mark its exact name source-local only, and route any reusable location pattern to C06.
- Preserve a donor pantheon as a C14 containment record, reject deity names as Astra defaults, and route reusable divine-effect pressure to C03 without defining divine mechanics.
- Preserve a local faction custom as source-local culture/faction context, route institution structure to C05, and keep donor proper nouns out of Astra vocabulary.
- Preserve a local planar hazard law as source-local evidence, route environmental pressure to C09, and avoid making it Astra-wide cosmology.
- Preserve a cosmology diagram as C13 visual evidence linked to C14 containment, with named planes retained only as source evidence or rejected donor elements.

Bad C14 usage:
- Promote donor named worlds, named planes, named gods, named factions, named cultures, named histories, named wars, named events, named places, named species, named schools, named magic systems, named technologies, donor setting laws, donor pantheons, donor cosmology, donor metaphysics, donor proper nouns, donor identity fields, donor alignment/cosmology labels, donor field names, or donor world assumptions as Astra defaults.
- Define Astra-wide cosmology, final metaphysics, final setting law, canon history, canon geography, canon factions, canon events, canon cultures, accepted proper nouns, accepted terminology, final lexicon, sourcebook lore, runtime world state, runtime cosmology state, runtime faction state, runtime deity state, canon setting models, database schema, backend lore schemas, hidden-state packets, context packets, entity/component/event schemas, command lifecycle, or live-play world truth.
- Treat legal/IP review notes, lexicon-review flags, canon eligibility, or source-local containment as canon acceptance or legal clearance.

## 22. Minimum tests or assertions

Minimum C14 tests assert that:
- the C14 file exists at `docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md`;
- all required sections are present;
- C14 declares ownership and non-ownership;
- C14 must inherit/include `AstraContentRecordBase` and preserve C00 provenance posture;
- C14 doctrine grammar is doctrine-level only and not runtime/database/canon-setting/sourcebook-lore/lexicon-acceptance/Astra-wide-cosmology/final-metaphysics/donor-setting-import schema;
- donor proper nouns, donor setting law, donor cosmology, donor metaphysics, donor pantheons, donor named worlds, donor named planes, donor named gods, donor named factions, donor named cultures, donor named histories, donor named wars, donor named events, donor named places, donor named species, donor named schools, donor named magic systems, donor named technologies, donor field names, donor identity fields, donor alignment/cosmology labels, and donor world assumptions are rejected as Astra defaults;
- C14 includes handoffs to C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, C13, and pending_schema;
- C14 includes overlap handling for canon review, lexicon governance, legal/IP review, runtime/backend, live-play/sourcebook, Batch A doctrine, and donor source;
- C14 includes source-local/legal/IP handling, rejected donor element handling, canon eligibility/review routing, hidden-state/protected-truth boundary language, runtime boundary language, and good/bad usage examples.

## 23. Acceptance criteria

C14 is accepted as a draft Batch C schema family file only when:
- C14 file exists at the exact registry path;
- C14 remains conversion-stage/canon-review schema doctrine only;
- C14 includes C00 base inheritance requirements;
- C14 does not import donor proper nouns, setting laws, cosmology, metaphysics, pantheons, named worlds, named planes, named gods, named factions, named cultures, named histories, named wars, named events, named places, named species, named schools, named magic systems, named technologies, donor identity fields, donor field labels, donor alignment/cosmology labels, or donor-world assumptions as Astra schema;
- C14 does not define Astra-wide cosmology, final metaphysics, canon history, canon geography, canon factions, accepted proper nouns, final lexicon, sourcebook lore, runtime world state, database schema, live-play world truth, canon, or accepted lexicon;
- C14 has clear cross-family handoffs and source-local/legal/IP/rejected-import handling;
- C14 registry posture is draft/schema-draft/designed/not_reviewed without promotion to current, canon, runtime, stable_for_family, stable_cross_family, or tested_minimum;
- C01/C02/C03/C05/C06/C07/C09/C10/C13 registry posture is preserved;
- C04, C08, C11, and C12 are not promoted;
- focused tests pass;
- full suite passes.

## 24. Follow-up handoff to Batch C remaining families or Batch C capstone

C14 completes the current focused Batch C family draft pass for source-local setting/cosmology containment. Follow-up work should route remaining unresolved C04, C08, C11, and C12 pressure to their own family drafts when authorized, or to a Batch C capstone once all active family schemas have durable draft posture.

The follow-up must preserve C00 base inheritance, Batch C unlock boundaries, source-local containment, legal/IP posture, lexicon review posture, canon-review routing, runtime/backend boundaries, sourcebook/live-play boundaries, and Batch A doctrine boundaries.

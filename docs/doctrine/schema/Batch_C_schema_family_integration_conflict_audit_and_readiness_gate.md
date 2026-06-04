# Batch C Schema-Family Integration Conflict Audit and Readiness Gate

## 1. Purpose and status

This Batch C capstone is an audit/readiness/control file. It is not a C-family schema, not a new C15 family, not a runtime contract, not a canon-promotion decision, not sourcebook prose, and not final mechanics doctrine.

Its purpose is to audit the completed C01-C14 draft schema-family layer for integration consistency, conflict boundaries, registry posture, C00 inheritance, source-local/legal/IP posture, rejected-import handling, donor leakage, cross-family handoffs, `pending_schema` discipline, Batch B handoff boundaries, runtime/canon/sourcebook/live-play/training separation, and test readiness.

Status: Batch C integration readiness gate, conversion-stage/canon-review schema doctrine control. This file records readiness only after local validation confirms the C01-C14 files and focused tests. It must not change C01-C14 family doctrine content or promote any C-family file.

## 2. Repository posture after C01-C14

Assuming local validation confirms the files and tests, the repository now contains draft C-family conversion-stage/canon-review schema doctrine for:

- C01 creature/NPC;
- C02 item/gear;
- C03 ability/power/technique;
- C04 relic/implant/installable asset;
- C05 faction/institution;
- C06 location/site/region;
- C07 mission/scenario/adventure;
- C08 vehicle/ship/platform;
- C09 hazard/environment;
- C10 table/oracle;
- C11 companion/summon;
- C12 crafting/salvage/recipe;
- C13 map/diagram annotation;
- C14 source-local setting/cosmology;
- `pending_schema` fallback routing for unowned conversion material.

C01-C14 remain draft/schema-draft/designed/not_reviewed unless a later formal promotion process changes them. Batch C remains conversion-stage/canon-review schema doctrine only.

## 3. Batch C readiness definition

Batch C readiness means the draft C-family record doctrine layer is ready for the next schema/math/mechanics workstream and for later pilot conversion testing. It means the families are sufficiently bounded, routed, and test-covered for follow-on review pressure.

Batch C readiness does not mean canon readiness, sourcebook readiness, runtime readiness, final mechanics readiness, database readiness, live-play readiness, training-corpus readiness, stable-for-family readiness, stable-cross-family readiness, or tested-minimum readiness.

## 4. What this capstone owns

This capstone owns only the integration audit and readiness gate across existing C01-C14 family drafts. It owns:

- C00 inheritance/include audit expectations;
- registry posture audit expectations;
- cross-family owner boundary audit expectations;
- overlap matrix review and safe handoff boundaries;
- parent/child/satellite/composite record routing review;
- source-local, legal/IP, rejected donor element, and donor leakage audit posture;
- `pending_schema` fallback discipline;
- confidence, validation, and review-routing audit posture;
- hidden-state/protected-truth boundary review;
- Batch B handoff boundary review;
- runtime/backend and canon/sourcebook/live-play/training boundary review;
- test readiness and brittle-test risk review;
- deferred gap ledger and next-workstream handoff.

## 5. What this capstone must not own

This capstone must not draft family fields, create merged schemas, define final mechanics, promote canon, define runtime schemas, define backend schemas, define database schemas, define entity/component/event schemas, define command lifecycle, define context packets, define save-state shape, write sourcebook prose, define live-play/GM behavior, create training/evaluation corpora, or modify C01-C14 doctrine content.

It must not treat Batch B operational doctrine as schema fields. It must not turn D-series source-pack material into current doctrine, final mechanics, runtime authority, canon, sourcebook prose, live-play procedure, or training-corpus authority.

## 6. C00 inheritance audit

Every durable C-family record must inherit/include `AstraContentRecordBase` from C00. C00 bypass risk is prohibited: C-family files must not create family-specific base identities, independent provenance systems, or alternate lifecycle fields.

Every C-family file must preserve C00 inheritance/include language and must preserve provenance, source evidence, construct refs, outcome refs, source-local boundary, rejected donor elements, canon eligibility, confidence/review/validation routing, lineage/composition/cross-reference, and legal/IP posture.

Audit result: C00 remains the shared base authority. Cross-family handoffs are references, satellites, child records, or explicit owner routing only; they are not inheritance between C families.

## 7. C-family registry posture audit

Registry posture must remain conservative. C01-C14 must remain draft/schema-draft/designed/not_reviewed and must not be promoted by this capstone to current, canon, runtime-ready, runtime_ready, stable_for_family, stable_cross_family, tested_minimum, accepted_canon, or any newly invented status vocabulary.

This capstone does not require a registry status for itself. If a later registry convention records non-family audit/readiness files, it may add a minimal tracking/changelog entry using existing vocabulary only; absent such convention, this control file may remain outside C-family promotion status.

Registry drift risks to audit include accidental current status, test_status promotion to tested_minimum, authority_level promotion beyond schema-draft for C01-C14, review_status promotion beyond not_reviewed, or hidden promotion through a changelog note.

## 8. Cross-family owner boundary audit

The C-family layer is an owner-routing system, not a merged inheritance tree. Each family owns its record family and sends overlaps through references, satellite records, child records, lineage/composition links, cross-reference fields inherited from C00 posture, or `pending_schema` fallback.

Cross-family references that imply inheritance when inheritance is not allowed are a failure. Composite records spanning multiple families must choose a primary owner and route other material as children, satellites, references, or explicitly named fallback.

## 9. Required overlap matrix audit

Each required overlap pair is safe only when the boundary is references/satellites/child records and explicit owner routing, not inheritance or merged schemas:

| Overlap pair | Safe audit boundary |
| --- | --- |
| C01 vs C11 | Creature/NPC and companion/summon records may reference each other through relationship, controller, minion, pet, summon, or satellite links; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C02 vs C04 | Gear and relic/implant/installable asset material may hand off installed, worn, embedded, attuned, or altered asset evidence; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C02 vs C12 | Item/gear and crafting/salvage/recipe material may link components, outputs, salvage sources, or recipe evidence; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C03 vs C04 | Ability/power/technique and relic/implant/installable asset material may connect granted powers, activation evidence, or technique carriers; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C05 vs C07 | Faction/institution and mission/scenario/adventure material may link sponsors, adversaries, objectives, reputational stakes, or institutional pressure; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C06 vs C13 | Location/site/region and map/diagram annotation material may link places to diagrams, labels, routes, or spatial evidence; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C06 vs C09 | Location/site/region and hazard/environment material may link environmental pressure to a place or region; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C07 vs C10 | Mission/scenario/adventure and table/oracle material may link encounter tables, randomizers, hooks, clocks, or prompt tables; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C08 vs C02/C04/C09 | Vehicle/ship/platform material may link carried gear, installed assets, relic modules, implants, platforms, or hazards; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C09 vs C10 | Hazard/environment and table/oracle material may link generated hazard outcomes, weather, terrain, or complication tables; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C14 vs every other family | Source-local setting/cosmology may annotate any C-family record with setting/cosmology containment, but references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C04 vs C12 | Relic/implant/installable asset and crafting/salvage/recipe material may link installation, upgrade, repair, or recipe evidence; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C08 vs C13 | Vehicle/ship/platform and map/diagram annotation material may link deck plans, route diagrams, platform maps, or navigation annotations; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C11 vs C03 | Companion/summon and ability/power/technique material may link granted abilities, summoning techniques, commands, or companion powers; references/satellites/child records and explicit owner routing are not inheritance or merged schemas. |
| C12 vs B06/B05 | Crafting/salvage/recipe material may receive operational conversion pressure from B06/B05, but references/satellites/child records and explicit owner routing are not inheritance, merged schemas, operational procedure, or final mechanics. |

## 10. Parent/child/satellite/composite record audit

Parent, child, satellite, and composite record handling must preserve explicit ownership. A parent record may reference child records owned by another family; a satellite may hold source-local, legal/IP, map, table, hazard, crafting, companion, or installation evidence; a composite record must not become an over-broad C-family megafile.

Risks audited here include over-broad C-family files becoming megafiles, under-specified C-family files failing conversion pressure, composite records spanning multiple families, and parent/child/satellite record handling that hides owner ambiguity.

## 11. Source-local and legal/IP audit

Source-local and legal/IP posture remains mandatory for all C-family files. Source-local material must not become Astra baseline through Batch C. Legal/IP evidence failure is a readiness blocker that routes to legal/IP review, source-local containment, rejected donor elements, or `pending_schema` fallback rather than default import.

The audit requires preservation of source evidence, provenance, source-local boundary, proper-noun containment, trademark/license/copyright/verbatim-similarity review, canon eligibility separation, and legal/IP posture across C01-C14.

## 12. Rejected donor element audit

Rejected donor element handling must remain explicit. Rejected-import evidence handling records why donor structures are not imported as Astra defaults and routes review material without erasing evidence.

Rejected donor elements may remain evidence, source-local containment, legal/IP review material, or rejected donor elements. They do not become family fields, final mechanics, baseline lore, accepted lexicon, runtime state, or canon shortcuts.

## 13. Donor leakage audit

Donor leakage is prohibited. Donor field names, donor math, donor statblocks, donor spell structures, donor item formats, donor vehicle formats, donor crafting economies, donor faction systems, donor table formats, donor map formats, donor pet/summon systems, donor cosmology, donor proper nouns, donor source-specific setting law, and donor systems remain evidence, source-local containment, legal/IP review material, or rejected donor elements.

Risk categories audited here include donor-field-name leakage, donor-math/statblock leakage, donor cosmology/proper-noun leakage, donor economy defaults, donor vehicle formats, donor crafting economies, donor faction systems, donor table formats, donor map formats, donor pet/summon systems, and source-specific setting law becoming Astra baseline.

## 14. pending_schema discipline audit

`pending_schema` is lawful fallback routing only. It is not a permission bucket for new fields, unowned schemas, donor imports, runtime state, canon shortcuts, hidden-state truth, sourcebook prose, database rows, command lifecycles, or mechanics defaults.

`pending_schema` overuse is a risk. Missing schema coverage produces quarantine, escalation, human review, owner assignment, deferred gap routing, or `pending_schema` fallback; it does not authorize improvised family-specific fields.

## 15. Confidence, validation, and review-routing audit

Confidence, validation, and review-routing fields remain discipline controls, not promotion controls. Confidence/review/validation misuse includes treating high confidence as canon, treating test presence as tested_minimum status, or treating local validation as sourcebook/runtime/live-play readiness.

All C-family records must preserve confidence, validation, escalation, review routing, canon eligibility, source evidence, construct refs, outcome refs, lineage/composition/cross-reference, and legal/IP posture.

## 16. Hidden-state and protected-truth audit

Hidden-state and protected-truth material must remain bounded. Hidden-state truth leakage is prohibited: secret GM-only content, unrevealed scenario truth, map secrets, oracle outcomes, faction hidden agendas, concealed hazards, source-local cosmology secrets, or protected donor facts must not leak into player-facing canon, sourcebook prose, training corpora, runtime state, or baseline schema defaults through Batch C.

Hidden-state management and protected-truth runtime handling are deferred outside Batch C.

## 17. Batch B handoff audit

Batch B handoffs remain doctrine-facing pressure only. Batch B operational files and B11 integration notes may identify conversion pressure, owner gaps, conflict risks, routing needs, or readiness blockers; they are not schema fields, runtime commands, event schemas, context packets, database rows, entity/component schemas, command lifecycle, final mechanics, or live-play procedures.

Batch B operational procedure being misread as schema fields is a named risk. C12 vs B06/B05 handoffs are pressure and routing evidence only, not inheritance or merged schema authority.

## 18. Runtime/backend boundary audit

Batch C must not define runtime state, runtime schemas, backend schemas, database schemas, entity/component/event schemas, command lifecycle, context packets, save-state shape, database rows, API contracts, persistence contracts, orchestration commands, or executable behavior.

Schema doctrine being confused with backend/database contracts is a named risk. Runtime/backend schema, entity/component/event/command lifecycle, context packet/save-state/database contracts are deferred outside Batch C.

## 19. Canon/sourcebook/live-play/training boundary audit

Batch C readiness is not canon/sourcebook/runtime/final-mechanics/live-play/training readiness. Canon eligibility is only review routing, not canon acceptance. Sourcebook prose, live-play/GM behavior, training/evaluation packs, accepted lexicon promotion, D-series source-pack authority, and conversion doctrine being confused with live-play behavior are all outside Batch C.

D-series material remains draft source material only and must not become current doctrine, final mechanics, runtime authority, canon, sourcebook prose, live-play behavior, or training-corpus authority through Batch C.

## 20. Testing posture audit

Focused tests should verify this capstone exists, contains the required audit sections, names all C01-C14 families and `pending_schema`, preserves C00 inheritance posture, audits registry status without promotion, audits overlap pairs without inheritance, preserves source-local/legal/IP and rejected donor handling, rejects donor leakage, preserves Batch B/runtime/canon/sourcebook/live-play/training boundaries, includes a deferred gap ledger, and verifies C01-C14 files exist.

Focused tests should verify registry entries for C01-C14 remain draft/schema-draft/designed/not_reviewed and are not current, canon, runtime-ready, stable_for_family, stable_cross_family, or tested_minimum.

## 21. Brittle-test and future-addition risk audit

Brittle tests that fail when future files are intentionally added are a risk. Tests for this capstone should not assert that no future schema files, non-family files, capstones, or control documents can exist. They should assert only that C01-C14 are not promoted and that this capstone owns readiness audit, not family schema fields.

Missing focused tests are also a risk. Future revisions may expand audit language without failing durable tests if the core readiness boundaries remain intact.

## 22. Deferred gap ledger

Named gaps outside Batch C and their lawful routing:

| Deferred gap | Named owner or lawful fallback |
| --- | --- |
| final mechanics and math | Future mechanics/math workstream; fallback to deferred gap ledger. |
| runtime/backend schema | Runtime/backend architecture workstream; fallback to runtime-todo registry owners. |
| entity/component/event/command lifecycle | Runtime/entity lifecycle workstream; fallback to runtime-todo registry owners. |
| context packet/save-state/database contracts | Persistence/context/runtime workstream; fallback to runtime-todo registry owners. |
| canon promotion | Canon governance workstream; fallback to canon-governance-todo owners. |
| sourcebook prose | Sourcebook/editorial workstream; fallback to sourcebook/editorial review. |
| live-play/GM behavior | Live-play/GM procedure workstream; fallback to operational review outside Batch C. |
| training/evaluation packs | Training/evaluation workstream; fallback to training-todo owners. |
| accepted lexicon promotion | Lexicon/canon governance workstream; fallback to legal/IP and canon review. |
| damage/resource/action-economy math | Mechanics/math workstream; fallback to deferred mechanics ledger. |
| economy/value/requisition math | Economy/mechanics workstream; fallback to deferred mechanics ledger. |
| vehicle/starship/mech combat math | Vehicle/mechanics workstream; fallback to deferred mechanics ledger. |
| companion/summon control mechanics | Companion/mechanics workstream; fallback to deferred mechanics ledger. |
| crafting/salvage/recipe economy math | Crafting/economy/mechanics workstream; fallback to deferred mechanics ledger. |
| map/GIS/coordinate/runtime navigation systems | Map/runtime/navigation workstream; fallback to runtime-todo owners. |
| hidden-state management and protected-truth runtime handling | Hidden-state/runtime/canon review workstream; fallback to protected-truth review. |
| corpus-scale pilot conversion validation | Pilot conversion validation workstream; fallback to conversion QA backlog. |

## 23. Batch C readiness verdict

Verdict: Batch C is ready with deferred gaps, assuming local validation confirms C01-C14 files exist, focused C-family tests pass, this capstone test passes, and the full suite does not reveal promotion or fixture drift.

Ready with deferred gaps means every deferred gap is routed to a named owner or lawful fallback and no gap is solved by Batch C through field invention, donor import, runtime schema creation, canon promotion, sourcebook prose, live-play behavior, or training-corpus authority.

## 24. Acceptance criteria

This capstone is acceptable when:

1. The capstone file exists at `docs/doctrine/schema/Batch_C_schema_family_integration_conflict_audit_and_readiness_gate.md`.
2. C01-C14 files are verified present.
3. C01-C14 registry entries remain draft/schema-draft/designed/not_reviewed.
4. No C-family file is promoted to current, canon, runtime-ready, stable_for_family, stable_cross_family, or tested_minimum.
5. The capstone does not define final mechanics, runtime schemas, backend schemas, database schemas, event schemas, command lifecycle, context packets, save-state shape, sourcebook prose, canon, live-play behavior, or training corpus.
6. Cross-family overlap is audited and references/satellites/child records do not imply inheritance.
7. Source-local/legal/IP, rejected donor, donor leakage, hidden-state, `pending_schema`, Batch B handoff, registry, and brittle-test risk handling are included.
8. The readiness verdict is ready with deferred gaps and all deferred gaps are routed to named owners or lawful fallback.
9. Focused tests pass.
10. The full suite passes locally or any environment limitation is reported without hiding failures.

## 25. Handoff to next schema/math/mechanics workstream

This capstone hands a bounded draft schema-family layer to the next schema/math/mechanics workstream and later pilot conversion testing. The next workstream may use C00-C14 as conversion-stage doctrine pressure but must not treat Batch C readiness as canon, sourcebook, runtime, final mechanics, database, live-play, or training readiness.

The next workstream should preserve C00 inheritance, registry non-promotion, source-local/legal/IP review, rejected donor evidence, donor leakage controls, `pending_schema` discipline, Batch B handoff boundaries, hidden-state protections, and explicit owner routing for overlaps.

# Batch C Schema-Family Unlock Index and Readiness Gate

## 1. Purpose and status

This file is the first Batch C schema/content-family unlock, index, and readiness-control document. It prepares C01-C14 ownership, overlap routing, risk posture, sequencing, and test posture without drafting C01-C14.

Status posture:
- Batch C defines conversion-stage and canon-review record-family doctrine only.
- This file is a planning/control readiness gate, not a C-family schema.
- This file does not create, define, draft, or promote C01-C14.
- This file does not define final mechanics, runtime implementation, sourcebook prose, canon acceptance, live-play behavior, donor record formats, donor statblocks, donor economies, donor class structures, or donor cosmology.
- Canon/sourcebook/runtime readiness is not Batch C readiness.
- D-series source packs are draft source material only; they are not current doctrine authority, final mechanics, runtime authority, canon, or sourcebook prose.

## 2. Current repository posture

Current repository posture at Batch C unlock planning:
- Batch A doctrine exists and must not be rewritten by this file.
- C00 exists as `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` and remains the shared base and schema-registry doctrine anchor.
- Batch B operational doctrine is complete through B11, and B11 records Batch B as ready for Batch C unlock planning with deferred gaps preserved.
- No C01-C14 family files are drafted by this readiness gate.
- The registry currently tracks C00 and C01-C14 using existing registry vocabulary; this file does not invent new registry status values.
- Batch C work remains conversion-stage/canon-review schema doctrine and must not collapse into runtime, sourcebook, canon, or donor-system import.

## 3. C00 binding constraints

C00 is binding on every later C-family file:
- Every durable C-family record must inherit/include `AstraContentRecordBase`.
- `pending_schema` is lawful only as named fallback routing and not as field invention.
- Cross-family references do not imply inheritance; `inheritance_allowed` remains false by default.
- Missing schema coverage produces quarantine, escalation, human review, or `pending_schema`, not improvised family-specific fields.
- C01-C14 may add family-owned doctrine only when their files are intentionally drafted and tested; this unlock file cannot predefine those fields.
- Source-local boundaries, rejected donor elements, canon eligibility, confidence/review/validation routing, lineage, composition, and legal/IP flags must follow C00 rather than donor record shapes.

C00 bypass is prohibited. A later C-family file may not treat a donor statblock, donor item entry, donor table, donor class feature, donor spell, donor encounter table, donor currency/economy, donor cosmology, donor proper noun, runtime entity, runtime component, runtime event, runtime command, context packet, save-state object, or database schema as a substitute for `AstraContentRecordBase`.

## 4. Batch B handoff implications

Batch B files identify operational pressure and related owners, but Batch B handoff notes are not schema fields. Batch B pressure may indicate that a construct probably routes to C01-C14 or `pending_schema`; it does not define final C-family record grammar.

Batch B handoff records are doctrine-facing only. They can preserve owner-routing notes, packet references, construct references, outcome references, quarantine/escalation recommendations, and deferred gaps, but they must not be interpreted as:
- C-family schema fields;
- runtime state shape;
- entity/component schema;
- event schema;
- command lifecycle;
- context packet contract;
- database schema;
- final mechanics;
- canon acceptance;
- sourcebook prose;
- live-play behavior.

## 5. C-family owner map for C01-C14

This readiness gate indexes the intended family owners without drafting their schemas. Named owner list: C01 creature/NPC; C02 item/gear; C03 ability/power/technique; C04 relic/implant/installable asset; C05 faction/institution; C06 location/site/region; C07 mission/scenario/adventure; C08 vehicle/ship/platform; C09 hazard/environment; C10 table/oracle; C11 companion/summon; C12 crafting/salvage/recipe; C13 map/diagram annotation; C14 source-local setting/cosmology; pending_schema.

| Family | Owner scope | Planning note |
| --- | --- | --- |
| C01 | creature/NPC | Owns conversion-stage creature, NPC, adversary, actor, monster, spirit, AI, swarm, and similar record-family questions after C01 is drafted. |
| C02 | item/gear | Owns practical item, gear, tool, weapon, armor, consumable, kit, and equipment record-family questions after C02 is drafted. |
| C03 | ability/power/technique | Owns ability, power, technique, move, spell-like effect, feature-like capability, and procedure-facing capability records after C03 is drafted. |
| C04 | relic/implant/installable asset | Owns relic, implant, augmentation, module, installed upgrade, bonded asset, and installable special asset records after C04 is drafted. |
| C05 | faction/institution | Owns faction, institution, organization, polity, guild, order, authority, and social body records after C05 is drafted. |
| C06 | location/site/region | Owns location, site, region, settlement, route node, zone, landmark, and place records after C06 is drafted. |
| C07 | mission/scenario/adventure | Owns mission, scenario, adventure, quest, operation, scene chain, and scenario container records after C07 is drafted. |
| C08 | vehicle/ship/platform | Owns vehicle, ship, mount-like platform, station, conveyance, and mobile platform records after C08 is drafted. |
| C09 | hazard/environment | Owns hazard, environmental pressure, terrain danger, trap-like pressure, disease-like pressure, weather pressure, and active environmental threat records after C09 is drafted. |
| C10 | table/oracle | Owns table, oracle, randomizer, generator list, lookup table, and outcome table records after C10 is drafted. |
| C11 | companion/summon | Owns companion, summon, pet, follower, minion, cohort, temporary ally, and controlled associate records after C11 is drafted. |
| C12 | crafting/salvage/recipe | Owns recipe, blueprint, salvage pattern, crafting requirement, repair recipe, upgrade recipe, and transformation process records after C12 is drafted. |
| C13 | map/diagram annotation | Owns map key, diagram annotation, keyed area note, spatial overlay, visual label, and annotation records after C13 is drafted. |
| C14 | source-local setting/cosmology | Owns source-local setting, cosmology, metaphysics, proper noun, local law, source-specific world rule, and non-baseline setting containment records after C14 is drafted. |
| pending_schema | named fallback routing only | Names constructs blocked by missing schema doctrine or unstable ownership. It is not a family, not a schema-field license, and not an invention path. |

## 6. Cross-family overlap and safe-boundary matrix

Cross-family overlap is expected. The safe boundary is owner routing plus references, not inheritance. Cross-family references do not imply inheritance; `inheritance_allowed` remains false by default unless a later authoritative owner file and C00-compatible registry entry explicitly allow a narrow case.

| Required overlap pair | Safe boundary |
| --- | --- |
| C01 vs C11 | Creature/NPC records and companion/summon records may reference each other, but companion control, summoning relation, and follower role do not make C11 inherit C01 fields or vice versa. |
| C02 vs C04 | Ordinary gear and installable/relic assets may reference each other, but special installation, relic identity, or implant containment does not turn C02 into C04 inheritance. |
| C02 vs C12 | Items may be ingredients or outputs of recipes, but a recipe is not an item schema and item properties are not recipe fields. |
| C03 vs C04 | Abilities may be granted by relics, implants, or installables, but granted capability references do not import C03 fields into C04 records. |
| C05 vs C07 | Factions may sponsor, oppose, or appear in scenarios, but scenario structure is not faction structure and faction doctrine is not adventure design. |
| C06 vs C13 | Locations may have map annotations and keyed areas, but spatial annotations are satellite/reference records and not inherited location fields. |
| C06 vs C09 | Locations may contain hazards and environments, but hazard pressure remains separately owned and must not become baseline location grammar. |
| C07 vs C10 | Scenarios may use tables/oracles, but tables remain lookup/oracle records and do not become scenario mechanics or encounter-table imports. |
| C08 vs C02/C04/C09 | Vehicles/platforms may carry gear, installables, relic modules, or hazards, but components and environmental threats remain referenced satellite/child records without inheritance by default. |
| C09 vs C10 | Hazards may use tables for variation or triggers, but oracle rows are evidence/routing aids and not hazard mechanics by default. |
| C14 vs every other family | Source-local setting/cosmology may wrap or constrain any other family, but source-local material does not become Astra baseline, canon, mechanics, sourcebook prose, or runtime authority by adjacency. |

Composite records spanning multiple families must choose a primary owner and route secondary material as referenced child/satellite records. Parent/child/satellite record handling must preserve C00 lineage, source-local boundaries, rejected-import evidence, and explicit non-inheritance defaults.

## 7. Risk register

Batch C unlock must track these risk categories:

| Risk category | Routing posture |
| --- | --- |
| C00 bypass risk | Block any C-family work that omits `AstraContentRecordBase` or treats donor formats as base grammar. |
| family-specific schema drift | Require each later family file to state owned and non-owned scopes against C00. |
| C-family overlap and duplicate ownership | Use the overlap matrix and owner routing before drafting fields. |
| donor-field-name leakage | Reject donor field names as Astra defaults; preserve them only as evidence, donor terms, or rejected donor elements. |
| donor-math/statblock leakage | Reject donor math and donor statblocks as Astra defaults; preserve exact values only as evidence or rejected-import material. |
| donor cosmology/proper-noun leakage | Reject donor cosmology and donor proper nouns as Astra baseline; route to C14/source-local/legal/IP review. |
| source-local material becoming Astra baseline | Require source-local containment and canon review before reuse. |
| legal/IP evidence failure | Require source-local and legal/IP flags as mandatory risk-routing concerns. |
| canon eligibility confusion | Keep canon eligibility as review routing, not canon acceptance. |
| runtime-state leakage | Forbid runtime state, save-state, entity, component, event, command, context, and database schema creation. |
| sourcebook-prose leakage | Forbid sourcebook prose promotion or player-facing prose from Batch C readiness work. |
| Batch B operational procedure being misread as schema fields | Treat Batch B handoff notes as doctrine-facing pressure only and not schema fields. |
| hidden-state truth leakage | Keep hidden-state truth out of schema doctrine and route hidden knowledge to later runtime/canon owners. |
| over-broad C-family files becoming megafiles | Split family files by owner scope and defer satellites instead of accumulating every overlap. |
| under-specified C-family files failing conversion pressure | Require focused pressure tests and deferred gap ledgers per family. |
| composite records spanning multiple families | Pick a primary family and route references instead of merging schemas. |
| parent/child/satellite record handling | Preserve C00 composition metadata and explicit non-inheritance. |
| pending_schema overuse | Use `pending_schema` only as named fallback routing with escalation, not as a permanent bucket. |
| rejected-import evidence handling | Preserve rejected donor elements and refusal rationale without normalizing them into Astra defaults. |
| confidence/review/validation misuse | Treat confidence/review/validation as work routing, not truth, canon, runtime readiness, or mechanics. |
| registry drift | Keep C-family statuses unchanged unless a proper family PR updates them with existing vocabulary. |
| brittle tests that fail when future C-family files are intentionally added | Test this control file and registry posture without banning future C01-C14 files. |
| missing focused tests | Add focused tests for this unlock gate and require later family-specific tests. |
| cross-family references that imply inheritance when inheritance is not allowed | State that references are not inheritance and `inheritance_allowed` remains false by default. |
| canon/sourcebook/runtime gates being confused with Batch C readiness | State that canon/sourcebook/runtime readiness is not Batch C readiness. |

## 8. Recommended sequencing

Recommended sequencing:
1. Add this Batch C unlock/index/readiness file first.
2. Then Wave 1: C01, C02, C03, C09, C10.
3. Then Wave 2: C06, C07, C05, C13, C14.
4. Then Wave 3: C04, C08, C12, C11.
5. Then Batch C capstone/readiness audit.

The ordering favors high-pressure conversion families first, then spatial/scenario/social/source-local integration, then composite/satellite-heavy families that depend on earlier boundaries.

## 9. First-wave unlock plan

First-wave unlock scope is planning-only here:
- C01 should resolve creature/NPC ownership against C11 companion/summon and C09 hazard pressure.
- C02 should resolve item/gear ownership against C04 installable/relic and C12 recipe pressure.
- C03 should resolve ability/power/technique ownership against C04 grant/installable pressure and C01 creature capability pressure.
- C09 should resolve hazard/environment ownership against C06 location and C10 table/oracle pressure.
- C10 should resolve table/oracle ownership against C07 scenario and C09 hazard pressure.

This file does not draft C01, C02, C03, C09, or C10. First-wave files must be separate PRs or separate intentional changes that inherit/include C00 and define only their own family doctrine.

## 10. Testing strategy

Testing strategy for this unlock gate:
- Verify this unlock/index/readiness file exists.
- Verify required sections, C-family names, overlap pairs, risks, C00 constraints, Batch B boundary language, source-local/legal/IP routing, and non-goals are present.
- Verify runtime/entity/component/event/command/context/database schema creation is explicitly forbidden.
- Verify canon/sourcebook/live-play/prose promotion is explicitly forbidden.
- Verify donor field names, donor math, donor statblocks, donor currency/economy, donor class structures, donor cosmology, and donor proper nouns are rejected as Astra defaults.
- Verify this file does not create C01-C14 content by avoiding family-specific draft headings and field definitions.
- Verify the registry does not promote C00 or C01-C14 to `current`, `stable_for_family`, `stable_cross_family`, `tested_minimum`, or other tested/stable/current status.
- Avoid brittle tests that fail when future C-family files are intentionally added; tests should protect this PR's scope and registry posture, not ban later files.

Later C-family PRs should add focused tests for their own owner boundaries, C00 inclusion, overlap routing, source-local/legal/IP containment, rejected donor handling, and registry posture using existing vocabulary only.

## 11. Registry strategy

Registry strategy for this unlock gate:
- Do not invent new registry status values.
- Do not promote C00 or C01-C14.
- Leave C-family statuses unchanged unless a later family-specific PR meets the registry's existing promotion requirements.
- If a safe existing convention for non-family planning/control files is later adopted, this file may receive a minimal registry entry using existing vocabulary only.
- Until such a convention exists, this readiness gate remains a doctrine control document outside C-family promotion status.

Registry status vocabulary observed in C00's schema-family registry doctrine includes `not_started`, `stub_index_only`, `minimum_unlock_draft`, `tested_minimum`, `stable_for_family`, `stable_cross_family`, `superseded`, and `deprecated`. The repository registry also uses broader file-record statuses such as `draft`, `todo`, and `current`. This file does not add to either vocabulary and does not promote C-family records.

## 12. Source-local and legal/IP risk strategy

Source-local and legal/IP flags are mandatory risk-routing concerns for Batch C. They are not optional metadata and not canon shortcuts.

Batch C must reject as Astra defaults:
- donor field names;
- donor math;
- donor statblocks;
- donor currency/economy;
- donor class structures;
- donor spell structures;
- donor encounter tables;
- donor cosmology;
- donor proper nouns.

D-series source packs are draft source material only. They may supply pressure examples, risk prompts, and provisional conversion questions, but they are not current doctrine authority, final mechanics, runtime authority, canon, sourcebook prose, donor record formats, donor statblocks, donor economies, donor class structures, or donor cosmology.

Any material with proper-noun, trademark, license, verbatim-similarity, copyright, or donor-world assumption risk must route to C00-compatible `ip_legal_flags`, source-local containment, rejected-import evidence, quarantine, escalation, or human review. Source-local material must not become Astra baseline through repetition, convenience, table frequency, or adjacency to otherwise valid records.

## 13. Deferred gap ledger

Deferred gaps intentionally left unresolved by this unlock gate:
- C01-C14 family-specific fields remain undefined until their owner files are drafted.
- Runtime schema, backend schema, entity/component schema, event schema, command lifecycle, context packet, save-state shape, and database contract remain out of scope.
- Canon acceptance, canon promotion, sourcebook prose, live-play behavior, and final mechanics remain out of scope.
- Donor statblock conversion, donor economy conversion, donor class-structure conversion, donor spell-structure conversion, donor encounter-table conversion, donor cosmology normalization, and donor proper-noun handling remain evidence/risk-routing problems, not Astra defaults.
- Composite record, parent/child record, and satellite record patterns require family-specific examples later, but inheritance remains false by default now.
- `pending_schema` overuse requires later audit as families are drafted.
- Rejected-import evidence handling requires family-focused examples later.
- Confidence/review/validation semantics require consistent usage in later family tests.
- Registry entry strategy for this control file may remain deferred until the registry has a safe convention for Batch B/Batch C control documents.

## 14. Acceptance criteria

This Batch C unlock/index/readiness gate is acceptable when it:
1. defines only Batch C planning, control, owner-index, overlap, risk, sequencing, and readiness posture;
2. does not draft C01-C14;
3. does not define final family-specific schema fields;
4. preserves C00 as binding shared base doctrine;
5. states that every durable C-family record must inherit/include `AstraContentRecordBase`;
6. states that `pending_schema` is lawful only as named fallback routing and not as field invention;
7. states that Batch B handoff notes are doctrine-facing only and not schema fields;
8. states that D-series source packs are draft source material only;
9. states that source-local and legal/IP flags are mandatory risk-routing concerns;
10. states that cross-family references do not imply inheritance and `inheritance_allowed` remains false by default;
11. states that canon/sourcebook/runtime readiness is not Batch C readiness;
12. explicitly forbids runtime/entity/component/event/command/context/database schema creation; forbid runtime/entity/component/event/command/context/database schema creation.
13. explicitly forbids canon/sourcebook/live-play/prose promotion; forbid canon/sourcebook/live-play/prose promotion.
14. explicitly rejects donor field names, donor math, donor statblocks, donor currency/economy, donor class structures, donor cosmology, and donor proper nouns as Astra defaults;
15. includes focused tests that verify this unlock gate without making future C-family additions fail by default;
16. keeps registry C-family statuses unpromoted.

## 15. Follow-up handoff to C01

The follow-up handoff to C01 is limited to opening creature/NPC record-family doctrine under C00. C01 should start from `AstraContentRecordBase`, preserve source-local/legal/IP routing, reject donor statblocks and donor field names as Astra defaults, and resolve overlaps with C11, C03, C09, C07, and C14 through references and deferred gaps rather than inheritance.

This file does not draft C01. C01 must be a separate family file with its own focused tests, owner boundary, non-owned scopes, overlap handling, registry posture, source-local/legal/IP handling, rejected-import handling, and acceptance criteria.

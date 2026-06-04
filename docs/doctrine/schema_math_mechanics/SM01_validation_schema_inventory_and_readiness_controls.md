# SM01 Validation/Schema Inventory and Readiness Controls

## 1. Purpose and status

SM01 is a post-SM00 planning/control file for validation and schema readiness. It converts SM00's high-level schema gap inventory into a more detailed validation/schema inventory and readiness-control map.

Status posture:
- SM01 is an inventory/readiness-control file only.
- SM01 is not a final schema file, not executable JSON Schema, not a Pydantic model, not a runtime contract, not a backend/database schema, not final mechanics, not exact math, not canon, not sourcebook prose, not live-play behavior, and not training data.
- SM01 does not create JSON Schema files, Pydantic models, runtime schemas, backend schemas, database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, resolution dice, damage formulas, resource formulas, progression math, donor-statblock validators, canon promotion, sourcebook prose, live-play behavior, or training/evaluation corpora.
- SM01 does not promote C00-C14 registry statuses, does not rewrite C00-C14, and does not add C15.
- SM01 uses D00-D19 source packs only as draft source material for validation pressure awareness; D-series source packs are draft source material only and cannot become validation authority.
- SM01 does not use RHBF as hidden law.

SM01's output is a planning inventory: what validation and schema artifacts will eventually be needed, what existing repository files and tests partially cover them, what remains missing, who should own later implementation, what dependencies block those owners, and what lawful fallback applies while the owner does not exist.

## 2. Upstream controls and authority boundary

SM00 owns master sequencing for the schema/math/mechanics workstream, and SM01 must obey SM00. SM01 may refine the validation/schema inventory under SM00, but it may not reorder master sequencing, skip pilot evidence, or collapse validation planning into mechanics, runtime, canon, sourcebook, live-play, backend, database, or training authority.

C00 owns shared content record base posture, including `AstraContentRecordBase`, C-family registry posture, record-status discipline, provenance/evidence lock posture, source-local boundaries, rejected donor elements, legal/IP routing, missing-schema fallback, and the difference between record status, canon eligibility, validation status, and registry readiness. C01-C14 own conversion-stage/canon-review family grammar for the existing Batch C schema families. SM01 may inventory validation needs against C00-C14, but it must not rewrite C00-C14, silently change their inheritance model, add C15, or promote their registry records.

The Batch C capstone and Batch C unlock/readiness gate establish that Batch C is ready for follow-on schema/math/mechanics planning with deferred gaps only. Batch C readiness is not canon readiness, sourcebook readiness, runtime readiness, final mechanics readiness, live-play readiness, database readiness, or training readiness.

Batch B/B11 are operational routing doctrine. B01-B11, including B11, can identify procedure pressure, handoff needs, quarantine/escalation behavior, and missing-schema routing, but Batch B/B11 are not validation schema authority and must not be converted into final schema fields.

Conversion IR, the lawful outcome taxonomy, conversion handoff contracts, handoff validation rules, conversion intake result schemas, extraction readiness guidance, canon/conflict review posture, evaluation/benchmark planning, roadmap controls, and runtime/Gate B references are upstream/downstream controls or partial operational artifacts. They do not authorize SM01 to create final executable validation schemas, runtime contracts, backend/database contracts, command lifecycles, context packets, save-state shapes, final mechanics, canon, sourcebook prose, live-play behavior, or training/evaluation corpora.

## 3. Existing validation and schema posture

The current repository already contains several partial validation and schema layers:

- C00-C14 provide draft conversion-stage/canon-review schema-family doctrine, not final executable schemas.
- The Batch C capstone verifies family integration posture, conflict boundaries, source-local/legal/IP safeguards, rejected-import handling, `pending_schema` discipline, and non-promotion rules.
- Batch B doctrine through B11 provides operational procedures and routing pressure while repeatedly refusing runtime entity/component/event/state schemas, backend validation ownership, and C-family field invention.
- The handoff and extraction area contains executable or contract-adjacent artifacts for extraction packets, conversion intake, content units, maps, tables, statblocks, repair queues, readiness classes, manifests, and quality reports. These are existing pipeline/handoff schemas, not final C-family validation schemas and not runtime schemas.
- The operations decisions log records current pipeline decisions about extraction lane posture, lawful outcomes, validation loops, map/statblock routing, conversion-result schema hardening, and runtime planning boundaries.
- Existing tests protect doctrine file presence, registry posture, Batch A/B/C boundaries, conversion intake schemas, extraction readiness, handoff packet validation, quality gates, runtime fixture generation, and SM00 scope controls.

This posture is useful but incomplete. The repository can test that planning and handoff artifacts remain bounded; it does not yet provide final validation schemas for every C-family record instance, cross-record reference graph, canon-review ledger, conflict ledger, mechanics I/O boundary, runtime-prep boundary, or validation fixture suite.

## 4. What SM01 owns

SM01 owns only the following planning/control work:

- Inventory validation schemas that future owners may need.
- Inventory record instance schemas without defining final fields.
- Inventory cross-record reference validation needs.
- Inventory conversion packet validation needs.
- Inventory evidence/provenance validation needs.
- Inventory source-local boundary validation, rejected donor element validation, and legal/IP validation needs.
- Inventory canon-review validation and conflict-ledger validation needs.
- Inventory pilot conversion output validation needs.
- Inventory mechanics I/O validation boundaries without defining mechanics.
- Inventory runtime-prep validation boundaries without defining runtime.
- Inventory test fixture schemas without creating training/evaluation corpora.
- Map each major gap to existing partial coverage, missing coverage, future owner, blocked dependencies, lawful fallback, and a document-local readiness state.
- Preserve unsupported or unclear validation pressure through `pending_schema`, quarantine, deferred gap ledger, or Astra Doctrine Council review.

## 5. What SM01 must not own

SM01 must not own or create:

- JSON Schema files or executable JSON Schema definitions.
- Pydantic models or other final model classes.
- Runtime schemas, backend schemas, database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, or save-state shapes.
- Final mechanics, exact math, resolution dice, damage formulas, resource formulas, progression math, action-economy math, difficulty bands, balance benchmarks, or donor-statblock validators that treat donor statblocks as Astra defaults.
- Canon promotion, accepted lexicon promotion, sourcebook prose, live-play/GM behavior, training data, evaluation corpora, or benchmark corpora.
- Registry promotion for C00-C14, C-family rewrite authority, C15 creation, or any hidden RHBF rule import.
- D-series authority promotion. D00-D19 remain draft source material only.

If implementation pressure appears in SM01 review, the lawful response is to route it to a future owner or fallback, not to embed final schema fields inside SM01.

## 6. Existing file and test inventory

Repository files inspected and their current validation/schema relevance:

| Area | Existing files | Current protection | SM01 limitation |
| --- | --- | --- | --- |
| Master sequencing | `docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md` | Defines schema/math/mechanics sequencing, gap categories, non-goals, and first follow-up PR posture. | SM01 must obey it and cannot become master sequencing. |
| Registry | `docs/doctrine/astra_doctrine_registry_v0_1.yaml` | Tracks status, authority_level, test_status, review_status, dependencies, unlocks, and C00-C14 draft/schema-draft posture. | SM01 must not promote C00-C14 or invent registry values. |
| Shared schema base | `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md` | Provides C-family base posture, provenance/evidence, source-local, rejected donor, legal/IP, lineage, composition, validation status, and `pending_schema` fallback language. | C00 is doctrine posture, not final executable schema. |
| C-family doctrine | `docs/doctrine/schema/C01...C14...` | Defines family routing grammar for creature/NPC, item/gear, ability/power/technique, relic/implant/installable asset, faction/institution, location/site/region, mission/scenario/adventure, vehicle/ship/platform, hazard/environment, table/oracle, companion/summon, crafting/salvage/recipe, map/diagram, and source-local setting/cosmology records. | SM01 may inventory validation pressure but cannot rewrite family fields. |
| Batch C controls | `Batch_C_schema_family_unlock_index_and_readiness_gate.md` and `Batch_C_schema_family_integration_conflict_audit_and_readiness_gate.md` | Protect C00 binding, Batch C capstone readiness, deferred gaps, cross-family boundaries, and non-promotion. | They do not create final validators. |
| Batch A doctrine | A00 and A01-A15 files across control, setting, advancement, and world folders | Protect Astra doctrine spine and owner boundaries. | SM01 must not rewrite Batch A. |
| Batch B doctrine | B01-B11 operational files | Protect operational procedure routing, missing-schema fallback, quarantine/escalation, and B11 readiness with deferred gaps. | Batch B/B11 are not validation schema authority. |
| Conversion/handoff | `docs/handoff/*`, `schemas/handoff/*`, `schemas/*`, `scripts/handoff/*` | Provide existing conversion intake, lawful outcome, Conversion IR-adjacent handoff, extraction readiness, packet validation, repair queue, readiness gate, map/table/statblock, and quality report coverage. | These schemas are pipeline/handoff artifacts, not final Astra C-family schemas. |
| Operations/roadmap/runtime pressure | `docs/operations/current_decisions_log_v0_1.md`, `docs/doctrine/astra_doctrine_roadmap_v0_1.md`, runtime-related tests | Record extraction defaults, conversion-result hardening, evaluation/benchmark pressure, and runtime/Gate B boundaries. | They cannot be treated as runtime-prep validation contracts here. |
| D-series source packs | `docs/doctrine/native_design/d_series/source_packs/...` | Preserve draft source-pack pressure and source-local ideas for later review. | D00-D19 are draft source material only and cannot become validation authority. |

Existing tests and what they protect at a high level:

| Test group | Representative tests | Current protection |
| --- | --- | --- |
| Registry and roadmap | `test_astra_doctrine_registry.py`, roadmap-related assertions in doctrine tests | Registry shape, file IDs, status/authority/test/review fields, and non-current posture. |
| Batch A doctrine | `test_a01...` through `test_a15...`, `test_pre_a01_control_layer_docs.py` | Doctrine file structure, owner boundaries, non-adoption of donor mechanics, and non-runtime posture. |
| Batch B operations | `test_b01...` through `test_b11...` | Operational procedure sections, quarantine/escalation, missing-schema fallback, C-family handoff boundaries, and B11 readiness. |
| C00-C14 schema doctrine | `test_c00...`, `test_c01...` through `test_c14...`, Batch C capstone tests | Shared record base posture, family grammar markers, source-local/rejected donor controls, legal/IP boundaries, confidence/review routing, `pending_schema`, and non-promotion. |
| Conversion intake and lawful outcomes | `test_conversion_intake_results.py`, `test_scaffold_conversion_intake_json.py`, `test_aggregate_conversion_intake_results.py`, `test_audit_conversion_intake_quality.py` | Conversion intake result shape, lawful outcome accounting, mapping ledgers, source-local retentions, rejected imports, and quality audit expectations. |
| Extraction and handoff packets | `test_build_handoff_packet.py`, `test_validate_handoff_packet.py`, `test_validate_handoff_packet_batch.py`, `test_extraction_readiness.py`, `test_validate_full_corpus_readiness_gate.py` | Packet shape, manifests, page truth, queues, extraction readiness, full-corpus preflight, and handoff validation. |
| Quality gates and runtime-adjacent fixtures | `test_fixture_generator_runtime_contract.py`, `test_surgeon_runtime_profile.py`, quality/report tests | Fixture generator contract posture, runtime-adjacent profile boundaries, report generation, mojibake scanning, and no silent extraction drift. |
| SM00 planning | `test_sm00_schema_math_mechanics_master_scope_and_sequencing_plan.py` | Master sequencing, full schema/math gap inventories, D-series non-authority, runtime/Gate B boundary, and hard refusals. |

## 7. C00-C14 validation coverage map

| Family | Existing partial coverage | Missing validation coverage | Future owner | Fallback/readiness |
| --- | --- | --- | --- | --- |
| C00 shared base | Base posture, evidence/provenance, status separation, composition, source-local, rejected donor, legal/IP, `pending_schema`, registry governance. | Executable base validator, cross-record graph checks, fixture corpus, promotion gate. | Future validation/schema implementation owner. | `pending_schema`, quarantine, deferred gap ledger; `partly_covered`. |
| C01 creature/NPC | Creature/NPC family grammar, donor statblock refusal, Batch B handoff boundaries. | Record instance schema, donor-statblock rejection validator, mechanics I/O boundary checks. | Future validation/schema implementation owner plus future mechanics requirements owner for I/O boundaries. | `defer_with_pending_schema`; `owner_needed`. |
| C02 item/gear | Item/gear routing, equipment/asset boundaries, donor economy refusal. | Instance shape, legal/IP checks for named items, cross-record ownership/equipment references. | Future validation/schema implementation owner. | Quarantine unclear donor equipment; `partly_covered`. |
| C03 ability/power/technique | Ability/technique conversion routing and donor spell/power leakage controls. | Resource/cost placeholder validation, mechanics boundary checks, canon-review routing. | Future validation/schema implementation owner plus future mechanics requirements owner. | `blocked_by_mechanics_owner`. |
| C04 relic/implant/installable asset | Relic/implant/installable asset family ownership and body/object boundary posture. | Composite object/body references, legal/IP, install-state validation boundary. | Future validation/schema implementation owner. | Human review for unclear body integration; `human_review_required`. |
| C05 faction/institution | Faction/institution records and Batch B social/acquisition pressure boundaries. | Cross-record rank/ownership references, conflict-ledger links, source-local institutions. | Future validation/schema implementation owner plus future canon/conflict governance owner. | `partly_covered`. |
| C06 location/site/region | Location/site/region routing and travel/exploration handoffs. | Map/location reference graph, source-local boundary validation, runtime-prep boundary. | Future validation/schema implementation owner plus future runtime/Gate B owner. | `blocked_by_runtime_gate`. |
| C07 mission/scenario/adventure | Mission/scenario/adventure record containment and adventure-script rejection posture. | Conversion packet validation, lawful outcome completeness, dependency references. | Future pilot conversion readiness owner. | Quarantine scripted donor assumptions; `blocked_by_pilot_evidence`. |
| C08 vehicle/ship/platform | Vehicle/platform family boundaries. | Mechanics I/O boundary for movement/capacity, runtime-prep handoff boundary, component-like reference checks. | Future validation/schema implementation owner plus mechanics/runtime owners. | `blocked_by_mechanics_owner`. |
| C09 hazard/environment | Hazard/environment routing and Batch B active-threat/travel pressure boundaries. | Consequence/damage boundary checks without formulas, location references, pilot output checks. | Future validation/schema implementation owner plus future mechanics requirements owner. | `blocked_by_mechanics_owner`. |
| C10 table/oracle | Table/oracle routing and table roll assumption refusal. | Table fixture schemas, probability/oracle boundary checks without final math, legal/IP checks. | Future validation test owner plus validation/schema implementation owner. | `owner_needed`. |
| C11 companion/summon | Companion/summon family grammar and actor relation posture. | Parent/child/satellite validation, control handoff boundaries, cross-record references. | Future validation/schema implementation owner. | `partly_covered`. |
| C12 crafting/salvage/recipe | Crafting/salvage/recipe family grammar and Batch B project pressure boundaries. | Input/output references, resource boundary checks without formulas, pilot output validation. | Future validation/schema implementation owner plus future mechanics requirements owner. | `blocked_by_mechanics_owner`. |
| C13 map/diagram | Map/diagram annotation family and map evidence posture. | Map fixture schemas, diagram reference validation, extraction repair integration. | Future validation test owner and conversion/evidence validation owner. | `blocked_by_pilot_evidence`. |
| C14 source-local setting/cosmology | Source-local setting/cosmology boundaries, rejected donor cosmology/proper noun posture, legal/IP routing. | Legal/IP validator, source-local containment validator, canon-review escalation checks. | C00/C14 plus future review owner. | `human_review_required`. |

## 8. Validation schema class inventory

Validation schemas will eventually check doctrine-shaped records, handoff artifacts, readiness packets, review ledgers, and fixture artifacts. Existing partial coverage includes C00-C14 doctrine markers, handoff JSON schemas, conversion intake validation scripts, registry tests, and Batch C/SM00 boundary tests.

Missing coverage includes final executable validators for C-family record instances, cross-record references, evidence/provenance chains, canon-review/conflict ledgers, pilot outputs, mechanics I/O boundaries, runtime-prep boundaries, and fixture suites.

Future owner: future validation/schema implementation owner. Blocked dependencies: SM00 sequencing, SM01 inventory acceptance, pilot conversion evidence, owner-specific schemas, and owner-controlled promotion gates. Lawful fallback: `pending_schema`, quarantine, deferred gap ledger, or Astra Doctrine Council review. Readiness state: `inventory_only` moving to `owner_needed`.

## 9. Record instance schema inventory

Record instance schemas will eventually define how individual C00-C14 records are validated. Existing partial coverage includes C00's shared content record base posture and C01-C14's family grammar, record-status controls, confidence/review-routing language, parent/child/satellite/composite composition language, source-local routing, and rejected donor handling.

Missing coverage includes final instance validation rules, canonical fixture examples, versioning/migration checks, field-level implementation, family-specific requiredness, and cross-family record normalization rules. SM01 must not define final schema fields for those records.

Future owner: future validation/schema implementation owner for C00/C01-C14 validation inheritance and record family coverage. Blocked dependencies: accepted validation design PR, representative pilot conversion packets, fixture owner, and canon/review boundary decisions. Lawful fallback: `pending_schema`, quarantine, or human review. Readiness state: `partly_covered` with `owner_needed`.

## 10. Cross-record reference validation inventory

Cross-record reference validation will eventually check references among parent, child, satellite, standalone, and composite records; source-local references; lineage; downstream invalidation; map/location links; ownership/custody links; produced/costs/depends-on relationships; and references to canon-review or conflict ledgers.

Existing partial coverage includes C00 composition metadata, cross-reference record posture, C-family overlap routing, Batch C conflict audit language, handoff mapping ledgers, and tests for avoiding inheritance or merged schemas.

Missing coverage includes graph validation, dangling-reference detection, source-local boundary enforcement across references, cyclic-dependency policy, conflict-ledger link validation, and invalidation/revalidation triggers.

Future owner: future SM02 or later schema validation owner. Blocked dependencies: reference vocabulary review, pilot evidence, record instance schema shape, and canon/conflict governance owner. Lawful fallback: `pending_schema`, quarantine, deferred gap ledger, or Astra Doctrine Council review. Readiness state: `owner_needed`.

## 11. Conversion packet validation inventory

Conversion packet validation will eventually ensure every packet carries sufficient source evidence, page truth, extraction run identity, lawful outcomes, mapping rows, readiness classes, queues, repair status, donor-family context, and handoff notes before conversion output is accepted for schema-family routing.

Existing partial coverage includes conversion handoff contract docs, handoff validation rules, `schemas/handoff/*`, `schemas/manifest.schema.json`, `schemas/page_metadata.schema.json`, `schemas/quality_report.schema.json`, scripts for packet building and validation, conversion intake schemas, lawful outcome accounting tests, and extraction readiness tests.

Missing coverage includes integration between handoff packet validation and C00-C14 record instance validation, pilot conversion output validation, evidence/provenance validation across packet boundaries, and conversion packet fixtures that exercise all C-family routes.

Future owner: future pilot conversion readiness owner. Blocked dependencies: pilot corpus selection, stable packet fixture policy, conversion/evidence validation owner, and future validation test owner. Lawful fallback: queue, quarantine, repair queue, `pending_schema`, or deferred gap ledger. Readiness state: `partly_covered` and `blocked_by_pilot_evidence`.

## 12. Evidence and provenance validation inventory

Evidence/provenance validation will eventually verify source evidence references, construct references, outcome references, provenance references, source page/range, extraction run IDs, packet IDs, source hashes, sidecar hashes, legal flags, review notes, and lineage from source file through Conversion IR and lawful outcome taxonomy into Batch C records.

Existing partial coverage includes C00 provenance/evidence lock posture, handoff packet manifests, page truth, conversion intake result schemas, extraction repair queues, operations decisions about provenance-first extraction, and tests around final page truth and validation.

Missing coverage includes end-to-end provenance graph validation, hash-lock completeness by maturity tier, unavailable-early-pilot handling, legal/IP review evidence, conflict-ledger evidence links, and revalidation triggers when upstream evidence changes.

Future owner: future conversion/evidence validation owner. Blocked dependencies: pilot conversion evidence, hash policy maturity, source reliability policy, and canon/conflict review owner. Lawful fallback: quarantine records with weak evidence, preserve donor terms as evidence only, route unknown provenance to human review, or defer with `pending_schema`. Readiness state: `partly_covered` and `human_review_required`.

## 13. Source-local, rejected-import, and legal/IP validation inventory

Source-local boundary validation will eventually ensure records marked source-local remain bounded to source/campaign/context and do not become canon by repetition. Rejected donor element validation will eventually ensure donor math, donor terms, donor cosmology, proper nouns, exact economies, exact class structures, exact statlines, table roll assumptions, adventure scripts, legal/IP risks, and other rejected imports are preserved as evidence or refusal rationale rather than Astra defaults. Legal/IP validation will eventually ensure copyright, trademark, verbatim-risk, proper-noun, license, and do-not-reproduce flags route correctly.

Existing partial coverage includes C00 source-local boundary rules, rejected donor element rules, legal/IP and source reliability routing, C14 source-local setting/cosmology doctrine, C-family tests for donor leakage refusal, and handoff validation rules that prevent donor stat/math/economy term promotion without an owner.

Missing coverage includes executable containment checks, legal review workflow checks, donor-term similarity review, source-local reference graph checks, rejected donor element fixture suites, and mature escalation routing.

Future owner: C00/C14 plus future review owner. Blocked dependencies: legal/IP review policy, canon/lexicon review owner, representative rejected donor examples, and source-local fixture policy. Lawful fallback: source-local containment, rejected_import, quarantine, deferred gap ledger, legal review, or Astra Doctrine Council review. Readiness state: `human_review_required`.

## 14. Canon-review and conflict-ledger validation inventory

Canon-review validation will eventually ensure canon_candidate, accepted_canon, accepted_with_limits, rejected, quarantined, source-local-only, and review-required states are routed only by appropriate canon/review owners. Conflict-ledger validation will eventually ensure conflicts among records, source-local assertions, donor terms, doctrine claims, legal/IP flags, and runtime pressure are recorded without silent promotion.

Existing partial coverage includes C00 canon eligibility rules, status separation, Batch C integration conflict audit, tests for C-family non-promotion, roadmap references to canon/lexicon governance, and operations references to lawful outcomes and conversion memos.

Missing coverage includes executable canon-review packet validation, conflict-ledger schema ownership, review routing based on confidence, cross-record conflict resolution workflow, and integration with registry promotion gates.

Future owner: future canon/conflict governance owner. Blocked dependencies: K-layer/canon owner readiness, pilot conversion conflicts, legal/IP workflow, and registry promotion policy. Lawful fallback: canon-review queue, conflict ledger draft entry, quarantine, `pending_schema`, or Astra Doctrine Council review. Readiness state: `owner_needed` and `human_review_required`.

## 15. Pilot conversion output validation inventory

Pilot conversion output validation will eventually verify that converted records from a pilot corpus obey C00-C14 routing, retain evidence/provenance, account for every lawful outcome, isolate source-local content, preserve rejected imports, route review-required material, and expose missing schema pressure without inventing fields.

Existing partial coverage includes conversion intake result schemas, conversion reporting scripts, handoff packet validation, full-corpus readiness gate guidance, operations decisions about pilot conversion loops, Batch C readiness tests, and SM00 conversion-readiness checklist language.

Missing coverage includes end-to-end pilot output validator, representative fixture outputs for all C-family routes, acceptance thresholds, failure/quarantine report shape, and re-run/revalidation policy.

Future owner: future pilot conversion readiness owner. Blocked dependencies: selected pilot conversion corpus, fixture owner, validation/schema implementation owner, and conversion/evidence validation owner. Lawful fallback: repair queue, quarantine, deferred gap ledger, `pending_schema`, or human review. Readiness state: `blocked_by_pilot_evidence`.

## 16. Mechanics I/O validation boundary inventory

Mechanics I/O validation boundaries will eventually identify the inputs and outputs that mechanics requirements must expose to schema validators without defining final mechanics. This includes boundary checks around costs, resources, damage/consequence placeholders, cadence/timing references, difficulty pressure, progression pressure, crafting/salvage inputs and outputs, vehicle/platform operation, hazard outcomes, companion/summon control, and table/oracle probability pressure.

Existing partial coverage includes SM00's math/mechanics gap inventory, Batch B operational procedure pressure, C-family non-mechanics boundaries, D-series source-pack pressure as draft source material only, and tests refusing final mechanics or donor defaults.

Missing coverage includes owner-approved mechanics requirements, benchmark evidence, exact validation boundaries, fixture outputs, and decisions about which mechanics outputs are schema-visible versus runtime-only.

Future owner: future mechanics requirements owner, not SM01 and not final mechanics. Blocked dependencies: mechanics owner creation, benchmark/evaluation plan, pilot evidence, and later SM sequencing. Lawful fallback: `pending_schema`, quarantine donor-statblock pressure, deferred gap ledger, or Astra Doctrine Council review. Readiness state: `blocked_by_mechanics_owner`.

## 17. Runtime-prep validation boundary inventory

Runtime-prep validation boundaries will eventually identify what information can be handed toward runtime/Gate B after doctrine, schema, canon/review, mechanics, and pilot evidence mature. Runtime-prep validation may later need to check runtime-facing readiness classes, but it must not define runtime schemas here.

Existing partial coverage includes SM00 runtime-readiness checklist posture, roadmap R-layer/runtime records, runtime/Gate B boundary references in Batch C, handoff/runtime-adjacent fixture tests, and operations notes about runtime planning.

Missing coverage includes Gate B owner rules, runtime import contracts, command lifecycle contracts, context packet contracts, save-state shapes, entity/component/event schemas, hidden-state handling, protected-truth handling, and backend/database contracts. Those are explicitly outside SM01.

Future owner: future runtime/Gate B owner, not SM01. Blocked dependencies: runtime gate owner, mechanics requirements owner, canon/review owner, pilot conversion evidence, and validation/schema implementation owner. Lawful fallback: block runtime import, quarantine runtime pressure, defer with `pending_schema`, or escalate to Astra Doctrine Council. Readiness state: `blocked_by_runtime_gate`.

## 18. Test fixture schema inventory

Test fixture schemas will eventually provide minimal, representative, and adversarial fixtures for C00-C14 record instances, conversion packets, evidence/provenance chains, source-local/rejected donor/legal/IP cases, canon-review/conflict ledgers, pilot outputs, mechanics I/O boundaries, runtime-prep boundaries, registry integrity, confidence/review-routing, parent/child/satellite/composite records, and pending_schema validation.

Existing partial coverage includes PDF fixtures, handoff packet tests, conversion intake tests, Batch A/B/C doctrine tests, C-family tests, SM00 tests, quality gate tests, runtime-adjacent fixture generator tests, and extraction/readiness tests.

Missing coverage includes C-family instance fixtures, cross-record graph fixtures, legal/IP fixtures, rejected donor fixtures, conflict-ledger fixtures, pilot output fixtures, mechanics boundary fixtures, runtime-prep boundary fixtures, fixture versioning, and fixture provenance.

Future owner: future validation test owner. Blocked dependencies: validation/schema implementation owner, pilot corpus selection, evidence/provenance owner, canon/conflict owner, mechanics requirements owner, and runtime/Gate B owner. Lawful fallback: mark fixture gaps in deferred gap ledger, use `pending_schema` for unowned examples, quarantine misleading donor fixtures, and require human review. Readiness state: `owner_needed`.

## 19. Gap classification matrix

SM01 readiness labels in this matrix are local planning labels only and are not registry values. They must not be written into `status`, `authority_level`, `test_status`, `review_status`, or any other registry status field.

| Validation/schema class | Existing partial coverage | Missing coverage | Future owner | Blocked dependencies | Lawful fallback | Readiness state |
| --- | --- | --- | --- | --- | --- | --- |
| validation schemas | C00-C14 doctrine, handoff schemas, conversion validators, registry tests. | Final C-family validators and integrated validation suite. | Future validation/schema implementation owner. | SM01 acceptance, pilot evidence. | `pending_schema`, quarantine, deferred gap ledger. | `inventory_only` |
| record instance schemas | C00 base posture and C01-C14 family grammar. | Final instance shapes, requiredness, examples. | Future validation/schema implementation owner. | Pilot records, fixture owner. | `pending_schema`, human review. | `partly_covered` |
| cross-record reference validation | C00 composition/reference posture, Batch C conflict audit. | Graph validation, dangling links, cycles, invalidation. | Future SM02 or later schema validation owner. | Reference vocabulary, pilot evidence. | Quarantine, deferred gap ledger. | `owner_needed` |
| conversion packet validation | Handoff schemas/scripts/tests and lawful outcome checks. | C-family integration, pilot packet acceptance. | Future pilot conversion readiness owner. | Pilot corpus, conversion/evidence owner. | Repair queue, quarantine. | `blocked_by_pilot_evidence` |
| evidence/provenance validation | C00 evidence posture, packet manifests, page truth. | End-to-end provenance graph and hash maturity checks. | Future conversion/evidence validation owner. | Hash policy, pilot evidence. | Quarantine, human review. | `partly_covered` |
| source-local boundary validation | C00/C14 source-local rules. | Executable containment and reference checks. | C00/C14 plus future review owner. | Review owner, source-local fixtures. | Source-local containment, quarantine. | `human_review_required` |
| rejected donor element validation | C00 rejected donor rules and C-family donor leakage tests. | Donor rejection fixture suite and similarity review. | C00/C14 plus future review owner. | Legal/IP policy, fixtures. | rejected_import, quarantine. | `partly_covered` |
| legal/IP validation | C00 legal/IP flags and handoff safeguards. | Legal workflow validator and escalation checks. | C00/C14 plus future review owner. | Legal review policy. | Legal review, do-not-reproduce quarantine. | `human_review_required` |
| canon-review validation | C00 canon eligibility separation. | Owner-controlled canon-review packet validation. | Future canon/conflict governance owner. | K-layer owner, pilot conflicts. | Canon-review queue, quarantine. | `owner_needed` |
| conflict-ledger validation | Batch C conflict audit and C00 conflict posture. | Ledger schema owner and cross-record conflict workflow. | Future canon/conflict governance owner. | Conflict owner, pilot evidence. | Draft ledger, Astra Doctrine Council review. | `owner_needed` |
| pilot conversion output validation | Conversion intake/reporting and SM00 readiness checklist. | End-to-end pilot output validator and thresholds. | Future pilot conversion readiness owner. | Pilot corpus and fixtures. | Repair queue, quarantine, deferred gap ledger. | `blocked_by_pilot_evidence` |
| mechanics I/O validation boundaries | SM00 mechanics gaps, Batch B pressure. | Mechanics requirements owner and benchmark-informed boundaries. | Future mechanics requirements owner. | Mechanics owner, benchmarks. | `pending_schema`, quarantine donor statblocks. | `blocked_by_mechanics_owner` |
| runtime-prep validation boundaries | SM00 runtime/Gate B posture and runtime-adjacent tests. | Gate B owner and runtime import readiness rules. | Future runtime/Gate B owner. | Runtime gate, mechanics/canon readiness. | Block runtime import, quarantine. | `blocked_by_runtime_gate` |
| test fixture schemas | Existing doctrine, handoff, extraction, and PDF fixtures. | C-family instance, graph, legal, conflict, pilot, mechanics, runtime-prep fixtures. | Future validation test owner. | Validator owner, pilot evidence. | Deferred gap ledger, human review. | `owner_needed` |
| registry integrity validation | Registry tests and C00 registry posture. | Future promotion gate checks across schema families. | Future validation/schema implementation owner plus registry owner. | Promotion policy. | Refuse promotion, council review. | `partly_covered` |
| confidence/review-routing validation | C00/C-family confidence and review routing language. | Executable routing thresholds and reviewer queue checks. | Future validation/schema implementation owner plus future review owner. | Review owner and policy. | Human review, quarantine. | `human_review_required` |
| parent/child/satellite/composite record validation | C00 composition metadata and C-family anti-inheritance tests. | Graph and composition validation suite. | Future SM02 or later schema validation owner. | Reference vocabulary and fixtures. | `pending_schema`, human review. | `owner_needed` |
| pending_schema validation | C00 fallback policy and C-family missing-schema tests. | Validator that prevents field invention while preserving unowned pressure. | Future validation/schema implementation owner. | Owner routing and pilot examples. | `pending_schema`, quarantine, deferred gap ledger. | `defer_with_pending_schema` |

## 20. Owner map and lawful fallbacks

Owner routing:

- C00/C01-C14 validation inheritance and record family coverage routes to the future validation/schema implementation owner.
- Cross-record reference validation routes to future SM02 or later schema validation owner.
- Conversion packet validation routes to the future pilot conversion readiness owner.
- Evidence/provenance validation routes to the future conversion/evidence validation owner.
- Source-local boundary validation, rejected donor element validation, and legal/IP validation route to C00/C14 plus the future review owner.
- Canon-review validation and conflict-ledger validation route to the future canon/conflict governance owner.
- Mechanics I/O validation routes to the future mechanics requirements owner, not final mechanics and not SM01.
- Runtime-prep validation routes to the future runtime/Gate B owner, not SM01.
- Test fixture schemas route to the future validation test owner.
- Registry integrity validation routes to the registry owner plus the future validation/schema implementation owner without promoting registry statuses.
- Confidence/review-routing validation routes to the future validation/schema implementation owner plus future review owner.
- Parent/child/satellite/composite record validation routes to future SM02 or later schema validation owner.
- Pending_schema validation routes to the future validation/schema implementation owner.

Lawful fallbacks when the owner does not yet exist:

- Use `pending_schema` only as an explicit missing-owner route, not as permission to invent fields.
- Quarantine records or packets that cannot be safely routed.
- Preserve rejected donor elements as evidence or refusal rationale without normalization into Astra defaults.
- Use deferred gap ledger entries for known missing validation coverage.
- Send legal/IP, canon, conflict, source-local, and ambiguous review pressure to human review or Astra Doctrine Council review.
- Block runtime import until the future runtime/Gate B owner exists and accepts the boundary.
- Block mechanics finalization until a future mechanics requirements owner and benchmark evidence exist.

## 21. Readiness states for future validation work

SM01 may use document-local readiness labels only for inventory planning. These labels are not registry values, do not create registry statuses, and must not be written into registry fields such as `status`, `authority_level`, `test_status`, or `review_status`.

Document-local labels used by SM01:

- `inventory_only`: SM01 has named the class and controls but no implementation owner has begun.
- `partly_covered`: existing doctrine, handoff schemas, or tests provide partial protection, but final validation remains missing.
- `owner_needed`: a future owner file or workstream must be created before implementation.
- `blocked_by_pilot_evidence`: validation cannot mature until representative pilot conversion evidence exists.
- `blocked_by_mechanics_owner`: validation boundary depends on a future mechanics requirements owner, not final mechanics inside SM01.
- `blocked_by_runtime_gate`: validation boundary depends on future runtime/Gate B authority.
- `defer_with_pending_schema`: unowned pressure should remain in `pending_schema`, quarantine, or deferred gap ledger.
- `human_review_required`: legal/IP, source-local, canon/conflict, or ambiguity pressure requires human or Astra Doctrine Council review.

These labels are planning labels only. They do not mean current, accepted, stable_for_family, stable_cross_family, tested_minimum, accepted_canon, runtime_ready, runtime-ready, canon-ready, schema-current, or any other promotion state.

## 22. Risk register

| Risk | Why it matters | SM01 control |
| --- | --- | --- |
| Premature executable schema creation | Would bypass C00-C14 owners and freeze untested assumptions. | Refuse JSON Schema files, Pydantic models, final schemas, and final fields. |
| C-family rewrite drift | Would invalidate Batch C doctrine without owner-controlled review. | Inventory only; no C00-C14 rewrite and no C15. |
| Registry promotion by planning label | Would confuse SM01 local labels with registry statuses. | State labels are not registry values and refuse C00-C14 promotion. |
| Batch B treated as schema authority | Operational procedure terms could become schema fields. | State Batch B/B11 are operational routing doctrine only. |
| D-series authority leakage | Draft source packs could become hidden final mechanics or validation authority. | State D00-D19 are draft source material only. |
| Donor statblock leakage | Donor statlines could become Astra defaults. | Route donor-statblock pressure to rejected donor handling, quarantine, or mechanics owner. |
| Legal/IP leakage | Proper nouns or protected text could enter records. | Route to C00/C14 plus future review owner and legal/IP fallback. |
| Canon/sourcebook/live-play/training collapse | Validation could be mistaken for accepted content or training data. | Refuse canon, sourcebook prose, live-play behavior, and training/evaluation corpora. |
| Runtime contract creep | Runtime schemas, command lifecycles, context packets, save-state shapes, or backend/database schemas could be drafted too early. | Route to future runtime/Gate B owner and block runtime import. |
| Under-specified cross-record validation | Broken references could pass later conversion. | Route to future SM02 or later schema validation owner. |
| Pilot evidence gap | Validators may be brittle without real conversion outputs. | Mark pilot-dependent work `blocked_by_pilot_evidence`. |
| Mechanics boundary ambiguity | Validation might accidentally define final mechanics. | Route mechanics I/O to future mechanics requirements owner only. |

## 23. Recommended next PR after SM01

Recommended next PR: SM02 cross-record reference validation planning and graph-readiness controls.

SM02 or a later owner should remain planning/control unless explicitly authorized by SM00 sequencing. It should refine cross-record reference validation, parent/child/satellite/composite relationships, source-local reference containment, lineage and invalidation checks, and conflict-ledger link posture without creating final executable schemas, runtime contracts, final mechanics, canon/sourcebook/live-play/training content, registry promotion, or C15.

If pilot conversion readiness becomes more urgent than graph planning, an alternative next owner may be a pilot conversion readiness control PR. That PR should still treat conversion packet validation as readiness planning unless the appropriate owner and dependencies have been accepted.

## 24. Acceptance criteria

SM01 is acceptable only if:

- The SM01 file exists and remains nonempty.
- All required sections are present.
- SM01 names SM00, C00, C01-C14, Batch C capstone, B11, Conversion IR, lawful outcome taxonomy, and runtime/Gate B.
- SM01 states it is inventory/readiness-control only.
- SM01 explicitly refuses final schema files, executable JSON Schema, Pydantic models, runtime contracts, backend/database schemas, final mechanics, canon/sourcebook/live-play/training content, registry promotion, C00-C14 rewrite, C15 creation, D-series authority, and RHBF hidden law.
- SM01 lists validation schemas, record instance schemas, cross-record reference validation, conversion packet validation, evidence/provenance validation, source-local boundary validation, rejected donor element validation, legal/IP validation, canon-review validation, conflict-ledger validation, pilot conversion output validation, mechanics I/O validation boundaries, runtime-prep validation boundaries, test fixture schemas, registry integrity validation, confidence/review-routing validation, parent/child/satellite/composite record validation, and pending_schema validation.
- SM01 includes a gap classification matrix.
- SM01 includes owner routing and lawful fallbacks.
- SM01 includes readiness states and states that those states are local planning labels, not registry values.
- SM01 preserves future-safe posture: later SM02/SM03/etc. files may be added, and later proper owner-controlled registry promotion may occur outside SM01, but this PR does not perform such promotion.

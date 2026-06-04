# SM06 Controlled Pilot Conversion Execution and Output Capture Plan

## 1. Purpose and status

SM06 is a controlled pilot conversion execution and output capture planning/control file only. It defines how a later, separately authorized controlled pilot conversion execution PR must be structured. It defines execution scope, output capture requirements, required ledgers, evidence preservation, failure capture, review handoff, SM04 evaluation handoff, and hard non-readiness boundaries.

SM06 does not run conversion and does not create converted donor content or pilot outputs. It does not select, embed, quote, paraphrase, transform, or convert real copyrighted donor excerpts, donor statblocks, donor tables, donor maps, donor setting prose, protected expression, or donor proper nouns. It does not create benchmark corpora, evaluation corpora, training data, fine-tuning data, model behavior data, sourcebook-ready examples, final schemas, executable JSON Schema, Pydantic models, final validators, runtime/backend/database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, canon, sourcebook prose, live-play behavior, accepted lexicon, or registry promotion.

Status posture:

- SM06 is a controlled pilot conversion execution and output capture planning/control file only.
- SM06 may define execution-procedure requirements, output capture requirements, ledger requirements, evidence preservation requirements, failure capture requirements, review handoff requirements, and execution labels, but does not run conversion, create converted donor content, or produce pilot conversion outputs.
- SM06 defines document-local execution labels at the document level only; these are not registry values and must not be written into registry fields such as `status`, `authority_level`, `test_status`, or `review_status`.
- SM06 may name required output capture fields, ledger categories, and evidence preservation steps, but it must not turn these into final JSON fields, JSON Schema, Pydantic models, database fields, runtime contracts, or final validators.
- SM06 does not create final schemas, executable JSON Schema, Pydantic models, final validators, runtime/backend/database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, canon, sourcebook prose, live-play behavior, or accepted lexicon.

## 2. Upstream controls and authority boundary

SM00 owns master sequencing for the schema/math/mechanics workstream. SM06 follows that sequence and does not supersede SM00.

SM01 owns validation/schema inventory posture. SM06 uses SM01's inventory as planning context for understanding what validation artifacts exist or are missing.

SM02 owns minimum pilot conversion readiness gates and packet validation controls. SM06 cannot waive SM02 gates and cannot authorize execution without SM05 authorization. SM06 has no authority to waive SM02 minimum pilot readiness gates; unsatisfied SM02 gates block authorization and route to repair/quarantine/deferred outcomes.

SM03 owns the pilot packet fixture and dry-run review plan. SM06 requires that SM03 dry-run review passed or failures were routed before execution may proceed.

SM04 owns the pilot benchmark and evaluation rubric controls. SM06 requires that SM04 rubric is ready for post-execution review before execution may proceed.

SM05 owns the actual pilot conversion authorization and preflight gate. SM06 cannot authorize execution without SM05 authorization. Any later execution PR must reference SM05 authorization explicitly.

C00 owns shared content record base posture and the schema registry. C01-C14 own conversion-stage/canon-review family grammar and owner routing for their families. Batch C capstone readiness says the Batch C layer is ready with deferred gaps only; it does not promote canon, runtime, sourcebook, final mechanics, live-play, or training readiness.

Batch B, including B11, remains operational routing doctrine. Batch B/B11 are operational routing doctrine, not final mechanics or runtime validation authority.

Conversion IR, lawful outcome taxonomy, conversion intake doctrine, extraction readiness classes and queues, donor family routing guide, conversion handoff contract, canon candidate/conflict ledger controls, evaluation/benchmark planning, roadmap/current state ledger posture, runtime kernel doctrine, and runtime/Gate B are upstream or downstream controls referenced for boundary alignment only.

D00-D19 source packs are draft source material only. They are not current doctrine, not final mechanics, not runtime authority, not canon, not sourcebook prose, not live-play behavior, not training data, and cannot become execution authority, pilot conversion authority, benchmark authority, evaluation authority, mechanics authority, runtime authority, canon, or sourcebook authority.

Existing handoff schemas under `schemas/` and `schemas/handoff/`, relevant handoff/validation/extraction/conversion-intake/quality/readiness scripts under `scripts/`, and related tests under `tests/` demonstrate partial operational infrastructure. SM06 does not revise those files and does not treat their existing operational shapes as final C-family, runtime, backend, database, mechanics, canon, or training contracts.

## 3. Existing execution-planning posture

The repository does not yet contain a controlled pilot conversion execution procedure, output capture specification, or execution review handoff document. The existing posture is:

- SM02 defines minimum readiness gates that must be satisfied before a pilot conversion attempt is useful.
- SM03 defines a dry-run review plan that exercises SM02 gates against packet metadata without producing conversion outputs.
- SM04 defines the evaluation rubric that will apply to pilot conversion outputs when they exist.
- SM05 defines the authorization and preflight gate that must be passed before a controlled pilot conversion attempt may proceed.
- C00-C14 define conversion-stage/canon-review grammar that pilot outputs should route through, but no pilot outputs exist yet.
- No formal execution procedure, output capture specification, or execution review handoff exists at the doctrine/control level.

Therefore, SM06 can define the execution procedure and output capture plan that a later, separately authorized controlled pilot conversion execution PR must follow. SM06 does not execute conversion and does not produce pilot conversion outputs.

## 4. What SM06 owns

SM06 owns only these control-layer decisions:

1. The definition of "controlled pilot execution" as a later, separately authorized, tightly bounded conversion attempt whose purpose is to produce reviewable pilot evidence under SM02-SM05 controls. SM06 only defines the plan for such execution; it does not perform it.
2. The execution scope constraints that limit pilot execution to a tiny, bounded packet set authorized by SM05.
3. The required SM05 authorization reference terms that a later execution PR must include.
4. The pre-execution verification checklist.
5. The execution packet boundary controls.
6. The evidence and provenance capture requirements for pilot execution outputs.
7. The construct inventory capture requirements.
8. The lawful outcome ledger capture requirements.
9. The mapping ledger capture requirements.
10. The C00-C14 and `pending_schema` output routing capture requirements.
11. The rejected-import, source-local, and legal/IP capture requirements.
12. The confidence, review-routing, and human-review capture requirements.
13. The repair, quarantine, and failure-report capture requirements.
14. The donor leakage capture and hard-fail handling requirements.
15. The pilot output package contents definition.
16. The post-execution review handoff to SM04.
17. The document-local execution labels used for execution status, clearly marked as local execution labels only and not registry statuses.
18. The statement of what controlled execution may and may not prove.
19. The non-readiness boundaries for large-scale conversion, runtime, canon, sourcebook, live-play, and training.
20. Owner routing and lawful fallback declarations for execution activities.
21. Risk controls specific to pilot conversion execution and output capture planning.

SM06 may identify pressure on future mechanics I/O, runtime/Gate B, canon, sourcebook, live-play, or training owners. It does not satisfy that pressure.

## 5. What SM06 must not own

SM06 must not:

- run conversion;
- create converted donor content;
- create pilot outputs;
- select, embed, quote, paraphrase, transform, or convert real copyrighted donor excerpts;
- embed donor statblocks;
- embed donor tables;
- embed donor maps;
- embed donor setting prose;
- import donor proper nouns as Astra defaults;
- create benchmark corpora;
- create evaluation corpora;
- create training data;
- create fine-tuning data;
- create model behavior policy;
- create final output schemas;
- create JSON Schema files;
- create Pydantic models;
- create final validators;
- create runtime schemas;
- create backend schemas;
- create database schemas;
- create entity/component/event schemas;
- create command lifecycle contracts;
- create context packet contracts;
- create save-state shapes;
- create final mechanics;
- create exact math;
- create resolution dice;
- create damage formulas;
- create resource formulas;
- create progression math;
- create donor-statblock validators that treat donor statblocks as Astra defaults;
- promote C00-C14 registry statuses;
- rewrite C00-C14;
- add C15;
- promote canon;
- write sourcebook prose;
- create live-play behavior;
- create training/evaluation corpora;
- treat D00-D19 as authority;
- use RHBF as hidden law;
- waive SM02 minimum pilot readiness gates;
- bypass SM05 authorization.

## 6. Controlled pilot execution definition

"Controlled pilot execution" is a later, separately authorized, tightly bounded conversion attempt whose purpose is to produce reviewable pilot evidence under SM02-SM05 controls. SM06 only defines the plan for such execution; it does not perform it.

Controlled pilot execution determines whether the project can:

- execute a bounded pilot conversion under SM02-SM05 controls;
- capture output, evidence, and provenance in the required formats;
- produce ledgers and routing records that can be reviewed;
- identify and capture failures visibly;
- hand outputs to SM04 review.

Controlled pilot execution does not confer:

- canon permission;
- runtime import permission;
- sourcebook prose permission;
- final mechanics permission;
- live-play behavior permission;
- training data permission;
- large-scale conversion permission;
- benchmark/evaluation corpus creation permission.

## 7. Execution scope constraints

The controlled pilot execution must remain tiny and bounded. SM06 preserves the SM05 authorized pressure set:

- C01 creature/NPC
- C02 item/gear
- C03 ability/power/technique
- C10 table/oracle
- conditional C14 source-local setting/cosmology only if legal/IP/source-local routing is ready

C05, C06, C07, C08, C11, C12, and C13 remain deferred unless selected by SM05 authorization for a specific pressure test. C04 and C09 may also remain deferred unless needed to disambiguate C01/C02/C03/C10 pressure.

SM06 requires a normally tiny packet count: 3-5 packet candidates unless SM05 authorization narrows further. No execution may exceed the SM05 authorized packet count without a new authorization decision. Expansion beyond SM05 authorization is forbidden.

## 8. Required SM05 authorization reference

Any later execution PR must include:

- explicit reference to SM05 authorization decision;
- authorization label;
- authorization rationale;
- exact authorized packet count;
- exact authorized C-family pressure routes;
- named authorization owner;
- statement that SM02 gates were satisfied with no waived minimum gate;
- statement that SM03 dry-run review passed or failures were routed;
- statement that SM04 rubric is ready for post-execution review.

Missing SM05 authorization reference blocks execution via `execution_blocked_by_missing_authorization`.

## 9. Pre-execution verification checklist

Before a later execution PR may proceed, the following must be verified:

1. SM05 authorization decision exists and is referenced.
2. SM05 authorization label is present and valid.
3. Authorized packet count matches SM05 authorization.
4. Authorized C-family pressure routes match SM05 authorization.
5. SM02 readiness gates are confirmed satisfied.
6. SM03 dry-run review is confirmed passed or failures are routed.
7. SM04 evaluation rubric is confirmed ready.
8. Evidence/provenance capture path is confirmed operational.
9. Lawful outcome ledger capture path is confirmed operational.
10. Mapping ledger capture path is confirmed operational.
11. C00-C14 and `pending_schema` routing capture path is confirmed operational.
12. Rejected-import/source-local/legal/IP capture path is confirmed operational.
13. Confidence/review-routing capture path is confirmed operational.
14. Repair/quarantine/failure-report capture path is confirmed operational.
15. Donor leakage detection path is confirmed operational.
16. Post-execution SM04 review handoff target is named.
17. No runtime/canon/sourcebook/live-play/training/final-mechanics claims are made.
18. D00-D19 and RHBF are not treated as authority.

Any failed verification item blocks execution via the appropriate `execution_blocked_by_*` label.

## 10. Execution packet boundary controls

Each packet in the authorized execution set must maintain:

- packet identity traceable to SM05 authorization;
- donor source identity for the packet;
- donor-family classification for the packet;
- extraction run identity linking to a declared extraction run;
- page/range truth confirmable against extraction artifacts;
- source hash or hash-later policy declared and consistent;
- evidence references linking packet to source evidence;
- no real donor content embedded in SM06 itself.

No packet outside the SM05 authorized set may be executed. Discovering an out-of-scope packet during execution must trigger `execution_blocked_by_scope_expansion`.

## 11. Evidence and provenance capture requirements

A later execution PR must capture or preserve:

- packet identity for each executed packet;
- donor source identity for each executed packet;
- donor-family classification for each executed packet;
- extraction run identity for each executed packet;
- page/range truth for each executed packet;
- source hash or hash-later policy for each executed packet;
- evidence references linking each output to its source evidence;
- provenance chain from donor source through extraction to conversion output.

Missing evidence or provenance for any executed packet triggers `execution_blocked_by_missing_evidence_path`.

Do not turn these into final JSON fields, JSON Schema, Pydantic models, database fields, runtime contracts, or final validators. They are output-capture requirements only.

## 12. Construct inventory capture requirements

A later execution PR must capture:

- construct inventory for each executed packet listing all donor constructs identified during conversion;
- construct type/category for each identified construct;
- construct source location (page/range/section) within the packet;
- construct relationship to C-family routing targets.

Missing construct inventory triggers `execution_blocked_by_lawful_outcome_capture_gap`.

## 13. Lawful outcome ledger capture requirements

A later execution PR must capture a lawful outcome ledger for each executed packet. Every donor construct identified during conversion must receive exactly one lawful outcome:

- direct Astra mapping;
- normalized Astra mapping;
- source-local retained construct;
- quarantined construct pending later doctrine;
- escalated doctrine problem;
- rejected import.

No construct may be left without a declared lawful outcome. No floating "maybe useful later" constructs are permitted.

Missing lawful outcome for any construct triggers `execution_blocked_by_lawful_outcome_capture_gap`.

## 14. Mapping ledger capture requirements

A later execution PR must capture a mapping ledger for each executed packet documenting:

- donor construct to Astra construct mappings (for direct and normalized mappings);
- mapping rationale;
- mapping confidence;
- mapping review status;
- unmapped constructs routed to source-local, quarantine, escalation, or rejection.

Missing mapping ledger triggers `execution_blocked_by_routing_capture_gap`.

## 15. C00-C14 and `pending_schema` output routing capture

A later execution PR must capture C-family routing for each conversion output:

- C-family routing targets for each output record;
- C00 base inheritance confirmation;
- `pending_schema` ledger for constructs that do not yet have a stable C-family owner;
- deferred families (C05, C06, C07, C08, C11, C12, C13, and optionally C04, C09) explicitly marked deferred with reason;
- no C-family routing invents new fields, schema properties, or C15.

Missing C-family routing or `pending_schema` capture triggers `execution_blocked_by_routing_capture_gap`.

## 16. Rejected-import, source-local, and legal/IP capture

A later execution PR must capture:

- rejected-import ledger with refusal rationale and evidence references for each rejected construct;
- source-local retention ledger bounding source-local records to source/campaign context;
- legal/IP flags for any constructs with trademark, copyright, or protected-expression risk;
- legal/IP review route for flagged constructs;
- no rejected-import leakage (rejected donor elements appearing as Astra defaults);
- no source-local leakage (source-local records treated as Astra baseline);
- no donor proper nouns, setting cosmology, faction names, deity names, or protected expression imported as Astra defaults.

Missing legal/IP or source-local capture triggers `execution_blocked_by_legal_ip_risk`.

## 17. Confidence, review-routing, and human-review capture

A later execution PR must capture:

- confidence/review-routing notes for uncertain or ambiguous records;
- human-review path for records requiring human judgment;
- reviewer decision points identified and documented;
- no automatic promotion of uncertain records without review;
- review owner identified for each category of review.

Missing confidence/review-routing capture triggers `execution_blocked_by_review_handoff_gap`.

## 18. Repair, quarantine, and failure-report capture

A later execution PR must capture:

- repair queue status for each packet with repair-needed constructs;
- quarantine queue status for each packet with quarantine-needed constructs;
- failure report shape: packet identity, failure reason, affected constructs, recommended routing, owner assignment;
- all failures routed to repair, quarantine, deferred gap ledger, `pending_schema`, or appropriate future owner;
- no failure may be silently dropped or ignored.

Missing repair/quarantine/failure-report capture triggers `execution_requires_repair` or `execution_requires_quarantine`.

## 19. Donor leakage capture and hard-fail handling

A later execution PR must capture donor leakage detection results:

- donor math leakage detection;
- donor statblock leakage detection;
- donor economy leakage detection;
- donor class/progression leakage detection;
- donor dice-system leakage detection;
- donor cosmology leakage detection;
- D-series authority leakage detection;
- RHBF hidden law detection;
- donor proper noun leakage detection.

Any detected donor leakage is a hard-fail. It must be captured, the affected output must be quarantined, and execution must be flagged via `execution_blocked_by_donor_leakage_risk`.

Missing donor leakage detection capability triggers `execution_blocked_by_donor_leakage_risk`.

## 20. Pilot output package contents

A later execution PR must produce a pilot output package containing:

- packet identity;
- donor source identity;
- donor-family classification;
- extraction run identity;
- page/range truth;
- source hash or hash-later policy;
- evidence references;
- construct inventory;
- lawful outcome ledger;
- mapping ledger;
- rejected-import ledger;
- source-local retention ledger;
- pending_schema ledger;
- repair queue status;
- quarantine queue status;
- confidence/review-routing notes;
- legal/IP flags;
- reviewer decision points;
- C-family routing targets;
- pilot output review status;
- failure report shape;
- benchmark/evaluation prerequisites;
- SM05 authorization reference;
- SM04 review handoff target.

Do not turn these into final JSON fields, JSON Schema, Pydantic models, database fields, runtime contracts, or final validators. They are output-capture requirements only.

## 21. Post-execution review handoff to SM04

Any captured pilot output must be handed to SM04 review before any further claim is made. The handoff must include:

- the captured output package;
- evidence/provenance artifacts;
- all ledgers (lawful outcome, mapping, rejected-import, source-local retention, pending_schema);
- failure reports;
- repair/quarantine states;
- authorization reference (SM05 authorization decision, label, rationale);
- reviewer assignment;
- explicit non-readiness statement.

SM06 states that outputs remain pilot evidence only until reviewed under SM04. They are not canon, not sourcebook prose, not runtime imports, not final mechanics, not live-play material, not training data, not benchmark corpus, and not large-scale conversion evidence.

Post-execution review must apply SM04 evaluation dimensions and rubric labels. No pilot output may be promoted beyond pilot evidence without SM04 review completion and appropriate future-owner authorization.

## 22. Execution result labels

SM06 uses the following document-local execution labels. These are local execution labels only, not registry values. They must not be written into registry fields such as `status`, `authority_level`, `test_status`, or `review_status`.

- `execution_ready_under_sm05_authorization` — all pre-execution verification passed; execution may proceed within authorized scope.
- `execution_blocked_by_missing_authorization` — execution is blocked because SM05 authorization reference is missing or invalid.
- `execution_blocked_by_scope_expansion` — execution is blocked because the packet set exceeds SM05 authorized scope.
- `execution_blocked_by_missing_evidence_path` — execution is blocked because evidence/provenance capture path is missing or broken.
- `execution_blocked_by_lawful_outcome_capture_gap` — execution is blocked because lawful outcome ledger capture cannot be completed.
- `execution_blocked_by_routing_capture_gap` — execution is blocked because C-family routing or mapping ledger capture cannot be completed.
- `execution_blocked_by_legal_ip_risk` — execution is blocked by unresolved legal/IP risk or missing source-local/rejected-import capture.
- `execution_blocked_by_donor_leakage_risk` — execution is blocked because donor leakage detection is missing or donor leakage was detected.
- `execution_blocked_by_review_handoff_gap` — execution is blocked because post-execution review handoff path is missing or review owner is not named.
- `execution_captured_for_sm04_review` — execution outputs have been captured and handed to SM04 review.
- `execution_requires_repair` — execution outputs contain constructs or packets that require repair before further processing.
- `execution_requires_quarantine` — execution outputs contain constructs or packets that require quarantine.
- `execution_not_reviewable` — execution outputs cannot be reviewed under SM04 due to missing evidence, missing ledgers, or capture failures.
- `execution_aborted` — execution was aborted before completion due to a hard-fail condition.

These labels are for pilot conversion execution planning use only. They do not confer registry status, canon permission, runtime permission, or training permission.

## 23. What controlled execution may and may not prove

Controlled execution may prove:

- the project can execute a bounded pilot under SM02-SM05 controls;
- output capture requirements can be followed or fail visibly;
- evidence/provenance can survive or fail visibly;
- lawful outcome accounting can be captured or fail visibly;
- C-family/`pending_schema` routing can be captured or fail visibly;
- donor leakage can be detected or fail to be detected;
- outputs can be handed to SM04 review.

Controlled execution may not prove:

- pilot output quality;
- pilot evaluation success;
- large-scale corpus conversion readiness;
- canon readiness;
- sourcebook readiness;
- runtime readiness;
- final mechanics readiness;
- live-play readiness;
- training readiness;
- benchmark corpus readiness;
- model adapter readiness;
- database/schema implementation readiness.

## 24. Large-scale conversion non-readiness boundary

A successful controlled pilot execution does not prove large-scale corpus conversion readiness. Large-scale conversion requires:

- multiple pilot conversions across diverse donor families;
- broad donor-family coverage beyond the pilot set;
- mechanics, math, and resolution system readiness;
- runtime/Gate B readiness;
- canon/conflict ledger readiness;
- broad evaluation readiness with established benchmark corpora;
- training readiness;
- production-scale infrastructure readiness.

Large-scale conversion requires later owner-controlled readiness gates after pilot evidence is reviewed and evaluation rubric results are assessed.

## 25. Runtime/canon/sourcebook/live-play/training non-readiness boundary

SM06 is not runtime readiness, canon readiness, sourcebook readiness, live-play readiness, training readiness, or final mechanics readiness.

Runtime pressure routes to future runtime/Gate B owner only. SM06 does not create runtime schemas, backend schemas, database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, runtime kernel behavior, or live-play behavior.

Canon pressure routes to canon/conflict owners only. SM06 does not promote canon, accept lexicon, write sourcebook prose, or make pilot outputs sourcebook-ready.

Mechanics pressure routes to a future mechanics requirements owner only. SM06 does not create final mechanics, exact math, resolution dice, damage formulas, resource formulas, progression math, donor-statblock validators, or donor math defaults.

Training and evaluation pressure routes to later training/evaluation owners only. SM06 does not create training data, evaluation corpora, fine-tuning corpora, benchmark corpora, or model behavior policy.

## 26. Owner map and lawful fallbacks

| Pressure | Future owner route | Lawful fallback if not ready |
| --- | --- | --- |
| Execution planning | future pilot conversion owner | block execution, route to repair or deferred gap ledger |
| SM05 authorization reference | authorization owner | block execution, route to `execution_blocked_by_missing_authorization` |
| Packet scope enforcement | pilot conversion owner | narrow scope, block execution, or defer |
| Evidence/provenance capture | future conversion/evidence validation owner | block execution, repair queue, evidence gap ledger |
| Construct inventory capture | conversion intake owner | block execution, repair ledger, quarantine |
| Lawful outcome capture | lawful outcome/conversion intake owner | block execution, repair ledger, quarantine |
| Mapping ledger capture | conversion intake owner | block execution, repair ledger, quarantine |
| C00-C14 routing capture | C00/C-family schema owner and future validation/schema implementation owner | route to `pending_schema`, quarantine, or deferred gap ledger |
| `pending_schema` capture | C00/future validation/schema implementation owner | keep in pending_schema ledger, quarantine, or defer |
| Rejected-import/source-local/legal/IP capture | C00/C14 plus future review/legal owner | rejected-import ledger, source-local retention ledger, legal/IP review, quarantine |
| Donor leakage capture | future conversion integrity owner plus relevant future mechanics/schema owner | quarantine donor-shaped pressure, repair ledger, doctrine escalation |
| Confidence/human-review capture | future review owner | human review required, no promotion |
| Repair/quarantine/failure-report capture | extraction readiness and pilot conversion owner | repair queue, quarantine queue, failure report |
| SM04 review handoff | future evaluation/benchmark owner | block further claims until review is complete, defer |
| Mechanics pressure | future mechanics requirements owner only | doctrine escalation, `pending_schema`, quarantine donor statblocks |
| Runtime pressure | future runtime/Gate B owner only | block runtime import, quarantine runtime-shaped pressure |
| Canon/sourcebook/live-play/training pressure | appropriate later phase owner only | no promotion, no sourcebook prose, no live-play behavior, no training data |

Lawful fallbacks must be explicit. Silent import, hidden defaults, donor-law adoption, RHBF hidden law, and ownerless promotion are forbidden.

## 27. Risk register

| Risk | Why it matters | SM06 control |
| --- | --- | --- |
| Execution plan treated as conversion execution | An execution plan could be mistaken for actual conversion or converted output creation. | SM06 defines execution procedure only. Actual conversion requires a separate execution PR referencing SM05 authorization. |
| Execution labels treated as registry values | Document-local execution labels could be written into registry status fields. | Labels are explicitly marked as local execution labels only and must not be written into registry fields. |
| Scope creep beyond SM05 authorized packet count | A small authorized pilot could expand to a larger unauthorized conversion. | Execution is bounded to SM05 authorized packet count. Expansion requires a new SM05 authorization cycle. |
| Donor content embedded in execution plan artifacts | Execution planning documents could embed copyrighted donor material. | SM06 refuses real donor excerpts, statblocks, tables, maps, setting prose, and proper nouns. |
| Donor mechanics leakage through pilot execution | Executing donor-sourced packets could normalize donor mechanics as Astra defaults. | Require donor leakage capture with hard-fail criteria and detection paths. |
| Source-local/legal/IP leakage | Protected proper nouns or setting cosmology could enter Astra baseline through execution outputs. | Require C14/legal review, source-local retention, legal/IP flags, and quarantine. |
| Missing schema disguised as implementation | Execution pressure could invent fields or C15. | Route to `pending_schema`, quarantine, or deferred gap ledger; refuse C00-C14 rewrite and C15 creation. |
| Over-trusting execution results | Captured pilot outputs could be mistaken for conversion success, large-scale readiness, canon readiness, runtime readiness, or training readiness. | Separate execution from conversion success and all later phases. State what execution may and may not prove. |
| Missing owner blocks review indefinitely | Execution may produce outputs but review may stall if no owner is named for SM04 handoff, routing, or failure handling. | Require named owners for all critical review and routing activities before execution. |
| Evidence/provenance lost during execution | Evidence chain could break during conversion, making outputs unreviewable. | Require evidence/provenance capture at every execution step. Missing evidence triggers hard-fail. |
| Lawful outcome gaps | Constructs left without declared lawful outcomes could drift into uncategorized states. | Require complete lawful outcome ledger. Missing outcomes trigger hard-fail. |
| Failure reports silently dropped | Execution failures could be ignored rather than captured. | Require failure capture and routing for every failure. Silent drop is forbidden. |
| SM05 authorization bypass | Execution could proceed without valid SM05 authorization. | Require explicit SM05 authorization reference. Missing authorization blocks execution. |
| SM02 gate waiver | SM02 minimum pilot readiness gates could be waived to permit execution. | SM06 cannot waive SM02 gates. Unsatisfied gates block execution. |
| Runtime/canon/sourcebook/training creep | Execution artifacts could be treated as final product surfaces. | Explicit runtime/canon/sourcebook/live-play/training non-readiness boundary and appropriate blocking labels. |
| D-series authority creep | D00-D19 draft packs could be treated as execution authority or pilot conversion authority. | State D-series packs are draft source material only and cannot become execution or pilot conversion authority. |
| RHBF hidden law | Ruthless Heavens Boundless Fate donor assumptions could become secret execution authority. | Refuse RHBF as hidden law. Ruthless Heavens Boundless Fate may remain draft/donor pressure only where explicitly routed by current Astra doctrine; it must not become secret authority for execution decisions. |
| Benchmark corpus creation creep | Execution could lead to creating benchmark corpora before pilot outputs are reviewed. | SM06 refuses benchmark corpora, evaluation corpora, training data, and fine-tuning data. |
| Post-execution review skipped | Outputs could be used or promoted without SM04 review. | Require SM04 review handoff before any further claim. Outputs remain pilot evidence only until reviewed. |

## 28. Recommended next PR after SM06

The recommended next PR after SM06 depends on whether the execution plan is complete and whether gaps are exposed.

Primary recommendation if SM06 execution plan is complete: SM07 controlled pilot conversion execution packet scaffold and review harness — the first PR allowed to create repo-local scaffolding for a pilot execution packet/review harness. SM07 must not embed real donor copyrighted content unless the repository policy and legal/IP routing explicitly allow it. If actual donor execution is not yet allowed, SM07 should create placeholder/test scaffolding only.

Alternative if SM06 exposes gaps: SM07 pilot execution plan repair and output-capture gap closure controls — defining how to repair missing capture paths, missing evidence paths, missing review owners, or output-capture gaps before execution can proceed.

The recommended next PR must not jump directly to broad conversion, final mechanics, runtime schemas, canon consolidation, sourcebook prose, live-play adapter behavior, or training corpus creation.

## 29. Acceptance criteria

SM06 is accepted only if:

- it exists as a post-SM05 controlled pilot conversion execution and output capture planning/control file only;
- it states that SM06 does not run conversion and does not create converted donor content or pilot outputs;
- it refuses real donor excerpts, donor statblocks, donor tables, donor maps, donor setting prose, donor proper noun import as Astra defaults, benchmark corpora, evaluation corpora, training data, fine-tuning data, model behavior policy, final schemas, JSON Schema files, Pydantic models, final validators, runtime/backend/database contracts, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, canon, sourcebook prose, live-play behavior, training content, registry promotion, C00-C14 rewrite, C15 creation, D-series authority, RHBF hidden law, SM02 gate waiver, and SM05 authorization bypass;
- it names SM00, SM01, SM02, SM03, SM04, SM05, C00, C01-C14, Batch C capstone, B11, Conversion IR, lawful outcome taxonomy, conversion intake, extraction readiness, donor family routing, evaluation/benchmark, and runtime/Gate B;
- it states that Batch B/B11 are operational routing doctrine, not final mechanics or runtime validation authority;
- it states that D00-D19 source packs are draft source material only and cannot become execution authority, pilot conversion authority, benchmark authority, or evaluation authority;
- it defines "controlled pilot execution" as a later, separately authorized, tightly bounded conversion attempt whose purpose is to produce reviewable pilot evidence under SM02-SM05 controls;
- it recommends a tiny bounded execution scope, normally 3-5 packet candidates unless SM05 narrows further;
- it lists the authorized pressure routes (C01, C02, C03, C10, conditional C14) and deferred families (C05, C06, C07, C08, C11, C12, C13, with C04 and C09 also deferrable);
- it lists all output capture terms;
- it includes document-local execution labels and states they are not registry values;
- it includes required SM05 authorization reference terms;
- it includes pre-execution verification checklist;
- it includes execution packet boundary controls;
- it includes post-execution review handoff to SM04;
- it states what controlled execution may and may not prove;
- it includes large-scale conversion non-readiness boundary;
- it includes runtime/canon/sourcebook/live-play/training non-readiness boundary;
- it includes owner routing, lawful fallbacks, and a risk register;
- it recommends SM07 controlled pilot conversion execution packet scaffold/review harness or SM07 pilot execution plan repair/output-capture gap closure controls without jumping directly to broad conversion, final mechanics, runtime schemas, canon consolidation, sourcebook prose, live-play behavior, or training corpus creation;
- it does not promote C00-C14 registry records, rewrite C00-C14, add C15, treat D-series source packs as authority, use RHBF as hidden law, waive SM02 minimum pilot readiness gates, or bypass SM05 authorization.

# SM05 Actual Pilot Conversion Authorization and Preflight Gate

## 1. Purpose and status

SM05 is an actual pilot conversion authorization and preflight gate only. It defines the final go/no-go control for authorizing a later, separate controlled pilot conversion execution PR. It consolidates SM02 readiness gates, SM03 dry-run preflight controls, and SM04 benchmark/evaluation rubric requirements into a final authorization checklist.

SM05 does not run conversion and does not create converted donor content. It does not select, embed, quote, paraphrase, transform, or convert real copyrighted donor excerpts, donor statblocks, donor tables, donor maps, donor setting prose, protected expression, or donor proper nouns. It does not create benchmark corpora, evaluation corpora, training data, fine-tuning data, model behavior data, or sourcebook-ready examples. It is not a final schema file, not executable JSON Schema, not a Pydantic model, not a final validator, not final mechanics, not exact math, not canon, not sourcebook prose, not live-play behavior, not runtime behavior, not backend/database design, and not training or evaluation data.

Status posture:

- SM05 is an actual pilot conversion authorization and preflight gate only.
- SM05 may define authorization gates, preflight checklists, go/no-go decision workflow, and authorization labels, but does not run conversion, create converted donor content, or produce pilot conversion outputs.
- SM05 defines document-local authorization labels at the document level only; these are not registry values and must not be written into registry fields such as `status`, `authority_level`, `test_status`, or `review_status`.
- SM05 may name required authorization gates, evidence requirements, and preflight steps, but it must not turn these into final JSON fields, JSON Schema, Pydantic models, database fields, runtime contracts, or final validators.
- SM05 does not create final schemas, executable JSON Schema, Pydantic models, final validators, runtime/backend/database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, canon, sourcebook prose, live-play behavior, or accepted lexicon.

## 2. Upstream controls and authority boundary

SM00 owns master sequencing for the schema/math/mechanics workstream. SM05 follows that sequence and does not supersede SM00.

SM01 owns validation/schema inventory posture. SM05 uses SM01's inventory as planning context for understanding what validation artifacts exist or are missing.

SM02 owns minimum pilot conversion readiness gates and packet validation controls. SM05 consolidates SM02 readiness gates as prerequisite authorization evidence.

SM03 owns the pilot packet fixture and dry-run review plan. SM05 consolidates SM03 dry-run review results as prerequisite authorization evidence.

SM04 owns the pilot benchmark and evaluation rubric controls. SM05 requires SM04 rubric availability as a prerequisite for authorizing pilot conversion, so that outputs can be evaluated after execution.

C00 owns shared content record base posture and the schema registry. C01-C14 own conversion-stage/canon-review family grammar and owner routing for their families. Batch C capstone readiness says the Batch C layer is ready with deferred gaps only; it does not promote canon, runtime, sourcebook, final mechanics, live-play, or training readiness.

Batch B, including B11, remains operational routing doctrine. Batch B/B11 are not final mechanics, not exact math, not final validators, and not runtime validation authority.

Conversion IR, lawful outcome taxonomy, conversion intake doctrine, extraction readiness classes and queues, donor family routing guide, conversion handoff contract, canon candidate/conflict ledger controls, evaluation/benchmark planning, roadmap/current state ledger posture, runtime kernel doctrine, and runtime/Gate B are upstream or downstream controls referenced for boundary alignment only.

D00-D19 source packs are draft source material only. They are not current doctrine, not final mechanics, not runtime authority, not canon, not sourcebook prose, not live-play behavior, not training data, and cannot become authorization authority, pilot conversion authority, benchmark authority, evaluation authority, mechanics authority, runtime authority, canon, or sourcebook authority.

Existing handoff schemas under `schemas/` and `schemas/handoff/`, relevant handoff/validation/extraction/conversion-intake/quality/readiness scripts under `scripts/`, and related tests under `tests/` demonstrate partial operational infrastructure. SM05 does not revise those files and does not treat their existing operational shapes as final C-family, runtime, backend, database, mechanics, canon, or training contracts.

## 3. Existing authorization posture

The repository does not yet contain a formal pilot conversion authorization decision, a preflight checklist, or a go/no-go control document. The existing posture is:

- SM02 defines minimum readiness gates that must be satisfied before a pilot conversion attempt is useful.
- SM03 defines a dry-run review plan that exercises SM02 gates against packet metadata without producing conversion outputs.
- SM04 defines the evaluation rubric that will apply to pilot conversion outputs when they exist.
- C00-C14 define conversion-stage/canon-review grammar that pilot outputs should route through, but no pilot outputs exist yet.
- No formal authorization decision, preflight checklist, or go/no-go gate exists at the doctrine/control level.

Therefore, SM05 can define the authorization gate and preflight checklist that must be satisfied before a later, separate pilot conversion execution PR may be proposed. It cannot claim authorization itself; it defines the criteria that a future authorization decision must satisfy.

## 4. What SM05 owns

SM05 owns only these control-layer decisions:

1. The definition of "pilot conversion authorization" as a bounded go/no-go control decision that allows or blocks a later, separate controlled pilot conversion execution PR. It is not the pilot conversion itself.
2. The authorization scope constraints that limit pilot conversion to a tiny, bounded packet set.
3. The required upstream completion evidence that must be present before authorization.
4. The authorization gates covering packet identity, evidence/provenance, lawful outcomes, C-family routing, legal/IP, donor leakage, confidence/review-routing, repair/quarantine/failure-reporting, and benchmark/evaluation prerequisites.
5. The document-local authorization labels used for go/no-go decisions, clearly marked as local authorization labels only and not registry statuses.
6. The go/no-go decision workflow.
7. The required contents of a later pilot conversion execution PR.
8. The statement of what authorization may and may not prove.
9. The non-readiness boundaries for large-scale conversion, runtime, canon, sourcebook, live-play, and training.
10. Owner routing and lawful fallback declarations for authorization activities.
11. Risk controls specific to pilot conversion authorization and preflight planning.

SM05 may identify pressure on future mechanics I/O, runtime/Gate B, canon, sourcebook, live-play, or training owners. It does not satisfy that pressure.

## 5. What SM05 must not own

SM05 must not:

- run conversion;
- create converted donor content;
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
- use RHBF as hidden law.

## 6. Pilot conversion authorization definition

"Pilot conversion authorization" is a bounded go/no-go control decision that allows or blocks a later, separate controlled pilot conversion execution PR. It is not the pilot conversion itself.

Authorization determines whether the project has satisfied sufficient preflight conditions to permit a controlled pilot conversion attempt. It does not guarantee conversion success, pilot output quality, or readiness for any downstream phase.

Authorization is revocable. If conditions change between authorization and execution, the authorization may be withdrawn by the authorization owner.

Authorization does not confer:

- canon permission;
- runtime import permission;
- sourcebook prose permission;
- final mechanics permission;
- live-play behavior permission;
- training data permission;
- large-scale conversion permission;
- benchmark/evaluation corpus creation permission.

## 7. Authorization scope constraints

The first authorized pilot must remain tiny and bounded. SM05 authorizes only a deliberately limited pilot packet set, normally 3-5 packet candidates unless a future owner narrows further.

The authorized pressure set remains aligned with SM03:

- C01 creature/NPC
- C02 item/gear
- C03 ability/power/technique
- C10 table/oracle
- conditional C14 source-local setting/cosmology only if legal/IP/source-local routing is ready

C05, C06, C07, C08, C11, C12, and C13 remain deferred unless selected for a specific pressure test. C04 and C09 may also remain deferred unless needed to disambiguate C01/C02/C03/C10 pressure.

No authorized pilot may exceed the declared packet count without a new authorization decision. Expansion beyond the authorized set requires a separate authorization cycle.

## 8. Required upstream completion evidence

SM05 requires evidence that the following upstream conditions are satisfied or explicitly routed before authorization may proceed:

1. SM02 readiness gates are satisfied. Any unsatisfied SM02 gate must block authorization and route to repair, quarantine, deferred gap ledger, `pending_schema`, or the appropriate future owner; unsatisfied SM02 gates may not be waived for pilot execution.

SM05 has no authority to waive SM02 minimum pilot readiness gates.
2. SM03 dry-run review has passed or failed items are routed to repair/quarantine/deferred gap ledger.
3. SM04 evaluation rubric is available and reviewer workflow is defined.
4. Packet metadata can be reviewed before execution.
5. Evidence/provenance can be preserved through the conversion process.
6. Lawful outcome accounting can be evaluated after execution.
7. C00-C14 or `pending_schema` routing can be evaluated after execution.
8. Rejected-import/source-local/legal/IP containment can be evaluated after execution.
9. Donor leakage can be evaluated after execution.
10. Repair/quarantine/failure reporting can be applied after execution.
11. Later pilot output review owner is named.

Missing upstream evidence routes to the appropriate blocking label (section 19) and must be resolved or explicitly routed before authorization can proceed.

## 9. Packet set authorization gate

The packet set authorization gate requires:

- packet identity for each candidate packet;
- donor source identity for each candidate packet;
- donor-family classification for each candidate packet;
- extraction run identity for each candidate packet;
- page/range truth for each candidate packet;
- source hash or hash-later policy for each candidate packet;
- evidence references for each candidate packet;
- construct inventory for each candidate packet;
- the total packet count is within the authorized bound (normally 3-5);
- no real donor content is embedded in the authorization gate itself.

Missing packet set evidence blocks authorization via `blocked_by_missing_packet_evidence`.

## 10. Evidence and provenance authorization gate

The evidence and provenance authorization gate requires:

- a defined evidence preservation path through conversion;
- extraction run identity traceable to a declared extraction run;
- page/range truth confirmable against extraction artifacts;
- source hash or hash-later policy declared and consistent;
- provenance chain from donor source through extraction to conversion output defined;
- no evidence fabrication or hallucinated provenance in the authorization record.

Missing evidence/provenance paths block authorization via `blocked_by_missing_packet_evidence`.

## 11. Lawful outcome authorization gate

The lawful outcome authorization gate requires:

- a lawful outcome ledger can be produced after execution;
- every construct identified during conversion will receive exactly one lawful outcome: direct Astra mapping, normalized Astra mapping, source-local retained construct, quarantined construct pending later doctrine, escalated doctrine problem, or rejected import;
- no construct may be left without a declared lawful outcome after execution;
- no floating "maybe useful later" constructs are permitted;
- lawful outcome review owner is identified.

Missing lawful outcome capability blocks authorization via `blocked_by_dry_run_failure` or `blocked_by_missing_owner`.

## 12. C00-C14 and `pending_schema` authorization gate

The C00-C14 and `pending_schema` authorization gate requires:

- C-family routing targets are defined for the authorized pressure set (C01, C02, C03, C10, conditional C14);
- `pending_schema` routing is available for constructs that do not yet have a stable C-family owner;
- no C-family routing invents new fields, schema properties, or C15;
- C00 base inheritance requirements are referenced, not bypassed;
- deferred families (C05, C06, C07, C08, C11, C12, C13, and optionally C04, C09) are explicitly marked deferred with reason;
- pending_schema ledger can be produced after execution;
- C-family routing review owner is identified.

Missing C-family routing capability blocks authorization via `blocked_by_dry_run_failure` or `blocked_by_missing_owner`.

## 13. Rejected-import, source-local, and legal/IP authorization gate

The rejected-import, source-local, and legal/IP authorization gate requires:

- rejected-import ledger can be produced after execution with refusal rationale and evidence references;
- source-local retention ledger can be produced after execution bounding source-local records to source/campaign context;
- legal/IP flags can be applied during execution for any constructs with trademark, copyright, or protected-expression risk;
- legal/IP review route exists for flagged constructs;
- no rejected-import leakage path (rejected donor elements appearing as Astra defaults);
- no source-local leakage path (source-local records treated as Astra baseline);
- no donor proper nouns, setting cosmology, faction names, deity names, or protected expression imported as Astra defaults;
- legal/IP and source-local review owner is identified.

Missing legal/IP or source-local routing blocks authorization via `blocked_by_legal_ip_risk`.

## 14. Confidence, review-routing, and human-review authorization gate

The confidence, review-routing, and human-review authorization gate requires:

- confidence/review-routing notes can be produced during execution for uncertain or ambiguous records;
- human-review path exists for records requiring human judgment;
- reviewer decision points can be identified and documented;
- no automatic promotion of uncertain records without review;
- review owner is identified.

Missing confidence/review-routing capability blocks authorization via `human_review_required_before_authorization` or `blocked_by_missing_owner`.

## 15. Repair, quarantine, and failure-report authorization gate

The repair, quarantine, and failure-report authorization gate requires:

- repair queue status can be tracked after execution;
- quarantine queue status can be tracked after execution;
- failure report shape is defined (packet identity, failure reason, affected constructs, recommended routing, owner assignment);
- all failures can be routed to repair, quarantine, deferred gap ledger, `pending_schema`, or appropriate future owner;
- no failure may be silently dropped or ignored;
- repair/quarantine/failure-report owner is identified.

Missing repair/quarantine/failure-report capability blocks authorization via `repair_required_before_authorization` or `quarantine_required_before_authorization`.

## 16. Benchmark/evaluation authorization gate

The benchmark/evaluation authorization gate requires:

- SM04 evaluation rubric is available;
- SM04 reviewer workflow is defined;
- SM04 evaluation dimensions are enumerated;
- SM04 failure-class inventory is enumerated;
- benchmark/evaluation prerequisites can be confirmed before execution;
- pilot output review owner is named;
- result interpretation owner is named;
- no benchmark corpora, evaluation corpora, training data, or fine-tuning data are created by authorization.

Missing benchmark/evaluation readiness blocks authorization via `blocked_by_rubric_gap`.

## 17. Donor leakage preflight gate

The donor leakage preflight gate requires:

- donor leakage hard-fail criteria are known before execution;
- donor math leakage detection path exists;
- donor statblock leakage detection path exists;
- donor economy leakage detection path exists;
- donor class/progression leakage detection path exists;
- donor dice-system leakage detection path exists;
- donor cosmology leakage detection path exists;
- D-series authority leakage detection path exists;
- RHBF hidden law detection path exists;
- donor leakage review owner is identified.

Missing donor leakage detection capability blocks authorization via `blocked_by_donor_leakage_risk`.

## 18. Runtime/canon/sourcebook/live-play/training non-readiness gate

SM05 authorization does not confer and must not be mistaken for:

- runtime readiness, runtime schema creation, backend schema creation, database schema creation, entity/component/event schema creation, command lifecycle contract creation, context packet contract creation, save-state shape creation, or runtime kernel behavior;
- canon readiness, accepted lexicon promotion, canon candidate promotion, or conflict-ledger resolution;
- sourcebook readiness, sourcebook prose creation, or sourcebook-ready examples;
- live-play readiness or live-play behavior creation;
- training readiness, training data creation, fine-tuning data creation, model behavior policy creation, or evaluation corpus creation;
- final mechanics readiness, exact math, resolution dice, damage formulas, resource formulas, or progression math;
- benchmark corpus creation or model adapter readiness.

Any pressure toward runtime, canon, sourcebook, live-play, training, or final mechanics must be routed to the appropriate later-phase owner. SM05 authorization explicitly refuses these claims.

If any of the above claims are attempted within the authorization or preflight process, authorization is blocked via `blocked_by_runtime_or_mechanics_creep`.

## 19. Authorization decision labels

SM05 uses the following document-local authorization labels. These are local authorization labels only, not registry values. They must not be written into registry fields such as `status`, `authority_level`, `test_status`, or `review_status`.

- `authorized_for_controlled_pilot_execution` — all preflight gates passed; a later pilot conversion execution PR may proceed within the authorized scope.
- `authorized_with_required_preflight_notes` — preflight gates passed with reviewer notes that must be addressed during or after execution.
- `blocked_by_missing_packet_evidence` — authorization is blocked because packet identity, donor source identity, or evidence references are incomplete.
- `blocked_by_dry_run_failure` — authorization is blocked because SM03 dry-run review failed and failures are not yet routed.
- `blocked_by_rubric_gap` — authorization is blocked because SM04 evaluation rubric is not available or reviewer workflow is not defined.
- `blocked_by_legal_ip_risk` — authorization is blocked by unresolved legal/IP risk.
- `blocked_by_donor_leakage_risk` — authorization is blocked because donor leakage hard-fail criteria are unknown or detection paths are missing.
- `blocked_by_missing_owner` — authorization is blocked because a required review, routing, or failure-report owner is not named.
- `blocked_by_runtime_or_mechanics_creep` — authorization is blocked because runtime schemas, final mechanics, or implementation artifacts were attempted.
- `repair_required_before_authorization` — a specific preflight failure requires repair before authorization can proceed.
- `quarantine_required_before_authorization` — a specific preflight failure requires quarantine before authorization can proceed.
- `human_review_required_before_authorization` — a specific preflight condition requires human judgment before authorization can proceed.
- `not_authorizable` — the pilot conversion attempt cannot be authorized under current conditions and must not proceed.

These labels are for pilot conversion authorization use only. They do not confer registry status, canon permission, runtime permission, or training permission.

## 20. Go/no-go decision workflow

The go/no-go decision workflow proceeds as follows:

1. Confirm SM00-SM04 exist and are current planning controls.
2. Confirm the pilot packet set is tiny, bounded, and owner-approved.
3. Confirm no real donor content is embedded in SM05.
4. Confirm SM02 readiness gates are satisfied; any unsatisfied SM02 gate blocks authorization and routes to repair, quarantine, deferred gap ledger, `pending_schema`, or the appropriate future owner.
5. Confirm SM03 dry-run review is complete or failures are routed.
6. Confirm SM04 evaluation rubric is available.
7. Confirm packet metadata and evidence/provenance preservation path.
8. Confirm lawful outcome, mapping, rejected-import, source-local, and `pending_schema` ledgers can be produced and reviewed after execution.
9. Confirm legal/IP and source-local review routes.
10. Confirm confidence/human-review routes.
11. Confirm repair/quarantine/failure-report routes.
12. Confirm benchmark/evaluation reviewer and result interpretation owner.
13. Confirm donor leakage hard-fail criteria.
14. Confirm no runtime/canon/sourcebook/live-play/training/final-mechanics claims will be made.
15. Assign document-local authorization label.
16. Record authorization decision and rationale.
17. If authorized, permit a later, separate pilot conversion execution PR with strict scope.
18. If blocked, route failures to repair, quarantine, deferred gap ledger, `pending_schema`, or appropriate future owner.

Each step must be completed before advancing to the next. The authorization decision record must be preserved for reproducibility and future audit.

Authorize only if:

- packet scope is tiny and bounded;
- SM02 gates are satisfied; any unsatisfied SM02 gate is routed to a blocking repair/quarantine/deferred outcome and prevents authorization until resolved;
- SM03 dry-run review is complete or failures are routed;
- SM04 rubric is ready;
- legal/IP path exists;
- source-local containment path exists;
- donor leakage hard-fail criteria are known;
- review owner exists;
- repair/quarantine/failure-report paths exist;
- no final mechanics/runtime/canon/sourcebook/live-play/training claims are made;
- D00-D19 and RHBF are not treated as authority.

Block authorization if:

- packet identity is missing;
- donor source identity is missing;
- donor-family classification is missing;
- extraction run identity is missing;
- page/range truth is missing;
- evidence/provenance path is missing;
- lawful outcome accounting cannot be reviewed;
- C00-C14 or `pending_schema` routing cannot be reviewed;
- legal/IP route is missing;
- source-local route is missing;
- donor leakage risk is uncontrolled;
- SM04 rubric is not available;
- dry-run failures remain unrouted;
- repair/quarantine/failure-report paths are missing;
- owner is missing;
- final mechanics, runtime schemas, canon, sourcebook prose, live-play behavior, training data, benchmark/evaluation corpora, or broad conversion are attempted;
- D-series or RHBF are treated as hidden law.

## 21. Required contents of a later pilot conversion execution PR

A later pilot conversion execution PR, if authorized by SM05, must include:

- explicit reference to SM05 authorization decision;
- exact packet set and scope;
- no expansion beyond authorized packet count;
- preservation of packet identity and donor source identity;
- extraction run identity and page/range truth;
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
- no canon/sourcebook/runtime/live-play/training/final-mechanics claims;
- post-execution review against SM04.

The later execution PR may be allowed to create pilot outputs only within the authorized scope. Those pilot outputs remain pilot evidence only, not canon, not sourcebook prose, not runtime imports, not final mechanics, not training data, and not large-scale readiness.

## 22. What authorization may and may not prove

Authorization may prove:

- the project has a bounded pilot execution scope;
- preflight review is complete enough to permit a controlled attempt;
- output review criteria exist;
- owner routing exists for expected failures;
- the project can attempt a pilot without claiming finality.

Authorization may not prove:

- conversion success;
- pilot output quality;
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

## 23. Large-scale conversion non-readiness boundary

A successful pilot conversion authorization does not prove large-scale corpus conversion readiness. Large-scale conversion requires:

- multiple pilot conversions across diverse donor families;
- broad donor-family coverage beyond the pilot set;
- mechanics, math, and resolution system readiness;
- runtime/Gate B readiness;
- canon/conflict ledger readiness;
- broad evaluation readiness with established benchmark corpora;
- training readiness;
- production-scale infrastructure readiness.

Large-scale conversion requires later owner-controlled readiness gates after pilot evidence is reviewed and evaluation rubric results are assessed.

## 24. Runtime/canon/sourcebook/live-play/training non-readiness boundary

SM05 is not runtime readiness, canon readiness, sourcebook readiness, live-play readiness, training readiness, or final mechanics readiness.

Runtime pressure routes to future runtime/Gate B owner only. SM05 does not create runtime schemas, backend schemas, database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, runtime kernel behavior, or live-play behavior.

Canon pressure routes to canon/conflict owners only. SM05 does not promote canon, accept lexicon, write sourcebook prose, or make pilot outputs sourcebook-ready.

Mechanics pressure routes to a future mechanics requirements owner only. SM05 does not create final mechanics, exact math, resolution dice, damage formulas, resource formulas, progression math, donor-statblock validators, or donor math defaults.

Training and evaluation pressure routes to later training/evaluation owners only. SM05 does not create training data, evaluation corpora, fine-tuning corpora, benchmark corpora, or model behavior policy.

## 25. Owner map and lawful fallbacks

| Pressure | Future owner route | Lawful fallback if not ready |
| --- | --- | --- |
| Authorization decision | future pilot conversion owner | block authorization, route to repair or deferred gap ledger |
| Packet scope approval | future pilot conversion owner | narrow scope, block authorization, or defer |
| Evidence/provenance preflight | future conversion/evidence validation owner | block authorization, repair queue, evidence gap ledger |
| Lawful outcome preflight | lawful outcome/conversion intake owner | block authorization, repair ledger, quarantine |
| C00-C14 routing preflight | C00/C-family schema owner and future validation/schema implementation owner | route to `pending_schema`, quarantine, or deferred gap ledger |
| `pending_schema` preflight | C00/future validation/schema implementation owner | keep in pending_schema ledger, quarantine, or defer |
| Rejected-import/source-local/legal/IP preflight | C00/C14 plus future review/legal owner | rejected-import ledger, source-local retention ledger, legal/IP review, quarantine |
| Donor leakage preflight | future conversion integrity owner plus relevant future mechanics/schema owner | quarantine donor-shaped pressure, repair ledger, doctrine escalation |
| Confidence/human-review preflight | future review owner | human review required, no promotion |
| Repair/quarantine/failure-report preflight | extraction readiness and pilot conversion owner | repair queue, quarantine queue, failure report |
| Benchmark/evaluation preflight | future evaluation/benchmark owner | block authorization until rubric is ready, defer |
| Mechanics pressure | future mechanics requirements owner only | doctrine escalation, `pending_schema`, quarantine donor statblocks |
| Runtime pressure | future runtime/Gate B owner only | block runtime import, quarantine runtime-shaped pressure |
| Canon/sourcebook/live-play/training pressure | appropriate later phase owner only | no promotion, no sourcebook prose, no live-play behavior, no training data |

Lawful fallbacks must be explicit. Silent import, hidden defaults, donor-law adoption, RHBF hidden law, and ownerless promotion are forbidden.

## 26. Risk register

| Risk | Why it matters | SM05 control |
| --- | --- | --- |
| Authorization treated as conversion permission | An authorization gate could be mistaken for conversion execution or converted output creation. | SM05 defines authorization criteria only. Actual conversion requires a separate execution PR referencing SM05 authorization. |
| Authorization labels treated as registry values | Document-local authorization labels could be written into registry status fields. | Labels are explicitly marked as local authorization labels only and must not be written into registry fields. |
| Scope creep beyond authorized packet count | A small authorized pilot could expand to a larger unauthorized conversion. | Authorization is bounded to normally 3-5 packets. Expansion requires a new authorization cycle. |
| Donor content embedded in authorization artifacts | Authorization documents could embed copyrighted donor material. | SM05 refuses real donor excerpts, statblocks, tables, maps, setting prose, and proper nouns. |
| Donor mechanics leakage through authorization | Authorizing donor-sourced packets could normalize donor mechanics as Astra defaults. | Require donor leakage preflight gate with hard-fail criteria and detection paths. |
| Source-local/legal/IP leakage | Protected proper nouns or setting cosmology could enter Astra baseline through authorization. | Require C14/legal review, source-local retention, legal/IP flags, and quarantine. |
| Missing schema disguised as implementation | Authorization pressure could invent fields or C15. | Route to `pending_schema`, quarantine, or deferred gap ledger; refuse C00-C14 rewrite and C15 creation. |
| Over-trusting authorization results | A passed authorization could be mistaken for conversion success, large-scale readiness, canon readiness, runtime readiness, or training readiness. | Separate authorization from conversion success and all later phases. State what authorization may and may not prove. |
| Missing owner blocks execution indefinitely | Authorization may pass but execution may stall if no owner is named for review, routing, or failure handling. | Require named owners for all critical review and routing activities before authorization. |
| Dry-run failures not routed | SM03 dry-run failures could be ignored rather than resolved. | Authorization requires SM03 failures to be routed to repair, quarantine, or deferred gap ledger. |
| Rubric not available at authorization time | SM04 rubric may not be ready when authorization is attempted. | Block authorization via `blocked_by_rubric_gap` if SM04 rubric is not available. |
| Runtime/canon/sourcebook/training creep | Authorization artifacts could be treated as final product surfaces. | Explicit runtime/canon/sourcebook/live-play/training non-readiness boundary and `blocked_by_runtime_or_mechanics_creep` label. |
| D-series authority creep | D00-D19 draft packs could be treated as authorization authority or pilot conversion authority. | State D-series packs are draft source material only and cannot become authorization or pilot conversion authority. |
| RHBF hidden law | Ruthless Heavens Boundless Fate donor assumptions could become secret authorization authority. | Refuse RHBF as hidden law. Ruthless Heavens Boundless Fate may remain draft/donor pressure only where explicitly routed by current Astra doctrine; it must not become secret authority for authorization decisions. |
| Benchmark corpus creation creep | Authorization could lead to creating benchmark corpora before pilot outputs exist. | SM05 refuses benchmark corpora, evaluation corpora, training data, and fine-tuning data. |

## 27. Recommended next PR after SM05

The recommended next PR after SM05 depends on what the authorization gate exposes.

Primary recommendation if authorization passes: SM06 controlled pilot conversion execution and output capture plan — defining the tightly scoped execution procedure and output capture requirements for the authorized pilot conversion. This later PR must not expand scope beyond SM05 authorization, must not claim canon/runtime/sourcebook/final-mechanics/training readiness, and must route outputs to SM04 review.

Alternative if authorization fails: SM06 pilot authorization repair and preflight gap closure controls — defining how to repair missing owners, missing evidence paths, dry-run failures, rubric gaps, or legal/IP routing issues before execution can be proposed.

The recommended next PR must not jump directly to broad conversion, final mechanics, runtime schemas, canon consolidation, sourcebook prose, live-play adapter behavior, or training corpus creation.

## 28. Acceptance criteria

SM05 is accepted only if:

- it exists as a post-SM04 actual pilot conversion authorization and preflight gate only;
- it states that SM05 does not run conversion and does not create converted donor content;
- it refuses real donor excerpts, donor statblocks, donor tables, donor maps, donor setting prose, donor proper noun import as Astra defaults, benchmark corpora, evaluation corpora, training data, fine-tuning data, model behavior policy, final schemas, JSON Schema files, Pydantic models, final validators, runtime/backend/database contracts, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, canon, sourcebook prose, live-play behavior, training content, registry promotion, C00-C14 rewrite, C15 creation, D-series authority, and RHBF hidden law;
- it names SM00, SM01, SM02, SM03, SM04, C00, C01-C14, Batch C capstone, B11, Conversion IR, lawful outcome taxonomy, conversion intake, extraction readiness, donor family routing, evaluation/benchmark, and runtime/Gate B;
- it states that Batch B/B11 are operational routing doctrine, not final mechanics or runtime validation authority;
- it states that D00-D19 source packs are draft source material only and cannot become authorization authority, pilot conversion authority, benchmark authority, or evaluation authority;
- it defines "pilot conversion authorization" as a bounded go/no-go control decision for a later, separate controlled pilot conversion execution PR;
- it recommends a tiny bounded authorized packet set, normally 3-5 packet candidates;
- it lists the authorized pressure routes (C01, C02, C03, C10, conditional C14) and deferred families (C05, C06, C07, C08, C11, C12, C13, with C04 and C09 also deferrable);
- it lists all authorization gate/evidence terms;
- it includes document-local authorization labels and states they are not registry values;
- it includes the go/no-go decision workflow steps;
- it includes required contents of a later pilot conversion execution PR;
- it states what authorization may and may not prove;
- it includes large-scale conversion non-readiness boundary;
- it includes runtime/canon/sourcebook/live-play/training non-readiness boundary;
- it includes owner routing, lawful fallbacks, and a risk register;
- it recommends SM06 controlled pilot conversion execution/output capture plan or SM06 authorization repair/preflight gap closure controls without jumping directly to broad conversion, final mechanics, runtime schemas, canon consolidation, sourcebook prose, live-play behavior, or training corpus creation;
- it does not promote C00-C14 registry records, rewrite C00-C14, add C15, treat D-series source packs as authority, or use RHBF as hidden law.

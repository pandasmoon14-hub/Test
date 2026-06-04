# SM04 Pilot Benchmark and Evaluation Rubric Controls

## 1. Purpose and status

SM04 is a pilot benchmark and evaluation rubric control file only. It defines how future pilot conversion outputs will be evaluated once an actual pilot conversion is later authorized. It defines what counts as evaluable pilot evidence, what dimensions must be judged, what pass/block/review/quarantine interpretations mean, how reviewer decisions are recorded, what failure classes must be reported, and what claims may or may not be made from a pilot result.

SM04 does not run conversion and does not create converted donor content. It does not create benchmark corpora, evaluation corpora, training data, fine-tuning data, model behavior data, or sourcebook-ready examples. It is not a final schema file, not executable JSON Schema, not a Pydantic model, not a final validator, not final mechanics, not exact math, not canon, not sourcebook prose, not live-play behavior, not runtime behavior, not backend/database design, and not training or evaluation data.

Status posture:

- SM04 is a pilot benchmark and evaluation rubric control file only.
- SM04 may define evaluation dimensions, rubric labels, reviewer workflow, and failure classes, but does not create actual benchmark corpora, evaluation corpora, training data, fine-tuning data, model behavior data, or sourcebook-ready examples.
- SM04 defines rubric interpretation labels at the document level only; these are not registry values and must not be written into registry fields such as `status`, `authority_level`, `test_status`, or `review_status`.
- SM04 may name required evaluable pilot evidence terms, evaluation dimensions, and reviewer workflow steps, but it does not turn those into final JSON fields, JSON Schema, Pydantic models, database fields, runtime contracts, or final validators.
- SM04 does not create final schemas, executable JSON Schema, Pydantic models, final validators, runtime/backend/database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, canon, sourcebook prose, live-play behavior, or accepted lexicon.

## 2. Upstream controls and authority boundary

SM00 owns master sequencing for the schema/math/mechanics workstream. SM04 follows that sequence and does not supersede SM00.

SM01 owns validation/schema inventory posture. SM04 uses SM01's inventory as planning context for understanding what validation artifacts exist or are missing.

SM02 owns minimum pilot conversion readiness gates and packet validation controls. SM04 assumes SM02 gates are prerequisite to any pilot output being eligible for evaluation.

SM03 owns the pilot packet fixture and dry-run review plan. SM04 builds on SM03 by defining how actual pilot conversion outputs (not dry-run artifacts) will be evaluated when they exist.

C00 owns shared content record base posture and the schema registry. C01-C14 own conversion-stage/canon-review family grammar and owner routing for their families. Batch C capstone readiness says the Batch C layer is ready with deferred gaps only; it does not promote canon, runtime, sourcebook, final mechanics, live-play, or training readiness.

Batch B, including B11, remains operational routing doctrine. Batch B/B11 are not final mechanics, not exact math, not final validators, and not runtime validation authority.

Conversion IR, lawful outcome taxonomy, conversion intake doctrine, extraction readiness classes and queues, donor family routing guide, conversion handoff contract, canon candidate/conflict ledger controls, evaluation/benchmark planning, roadmap/current state ledger posture, runtime kernel doctrine, and runtime/Gate B are upstream or downstream controls referenced for boundary alignment only.

D00-D19 source packs are draft source material only. They are not current doctrine, not final mechanics, not runtime authority, not canon, not sourcebook prose, not live-play behavior, not training data, and cannot become benchmark authority, evaluation authority, mechanics authority, runtime authority, canon, or sourcebook authority.

Existing handoff schemas under `schemas/` and `schemas/handoff/`, relevant handoff/validation/extraction/conversion-intake/quality/readiness scripts under `scripts/`, and related tests under `tests/` demonstrate partial operational infrastructure. SM04 does not revise those files and does not treat their existing operational shapes as final C-family, runtime, backend, database, mechanics, canon, or training contracts.

## 3. Existing benchmark/evaluation posture

The repository does not yet contain actual pilot conversion outputs, benchmark corpora, evaluation corpora, or reviewer-graded evaluation results. The existing posture is:

- SM02 defines minimum readiness gates that pilot outputs must pass before they are useful.
- SM03 defines a dry-run review plan that exercises SM02 gates against packet metadata without producing conversion outputs.
- C00-C14 define conversion-stage/canon-review grammar that pilot outputs should route through, but no pilot outputs exist yet.
- Evaluation/benchmark and runtime/Gate B materials are referenced as later controls, not as pilot or dry-run authority.
- No benchmark rubric, evaluation rubric, reviewer workflow, or failure-class taxonomy exists at the doctrine/control level.

Therefore, SM04 can define a benchmark/evaluation rubric and reviewer workflow that will apply to future pilot conversion outputs when they exist. It cannot claim evaluation readiness, benchmark corpus readiness, or any form of output-level grading authority until actual pilot outputs are produced and reviewed.

## 4. What SM04 owns

SM04 owns only these control-layer decisions:

1. The definition of "pilot benchmark/evaluation" as a bounded review method for future pilot conversion outputs, used to identify readiness, defects, leakage, and routing failures. It is not large-scale validation, not benchmark corpus creation, not training corpus creation, not canon review, not runtime import approval, and not final mechanics approval.
2. The evaluable pilot evidence requirements that future pilot outputs must preserve or report to be eligible for evaluation.
3. The evaluation subject boundaries that define what is and is not evaluable under this rubric.
4. The document-local rubric interpretation labels used by reviewers, clearly marked as local rubric labels only and not registry statuses.
5. The core evaluation dimensions that reviewers must assess.
6. The failure-class inventory for pilot evaluation.
7. The reviewer workflow and decision record format.
8. The pilot result interpretation rules, including what pilot evaluation may and may not prove.
9. The benchmark/evaluation question design constraints.
10. Owner routing and lawful fallback declarations for evaluation activities.
11. Risk controls specific to pilot benchmark/evaluation planning.

SM04 may identify pressure on future mechanics I/O, runtime/Gate B, canon, sourcebook, live-play, or training owners. It does not satisfy that pressure.

## 5. What SM04 must not own

SM04 must not:

- run conversion;
- create converted donor content;
- create benchmark corpora;
- create evaluation corpora;
- create training data;
- create fine-tuning data;
- create model behavior policy;
- embed real copyrighted donor excerpts;
- embed donor statblocks;
- embed donor tables;
- embed donor maps;
- embed donor setting prose;
- import donor proper nouns as Astra defaults;
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

## 6. Pilot benchmark/evaluation definition

A "pilot benchmark/evaluation" is a bounded review method for future pilot conversion outputs, used to identify readiness, defects, leakage, and routing failures. It is not large-scale validation, not benchmark corpus creation, not training corpus creation, not canon review, not runtime import approval, and not final mechanics approval.

Pilot benchmark/evaluation applies only to outputs from a controlled pilot conversion that has been explicitly authorized through a later preflight gate. It does not apply to dry-run artifacts, packet metadata alone, or hypothetical outputs.

The purpose of pilot evaluation is to determine whether:

- the conversion loop produced reviewable, evidence-backed outputs;
- lawful outcome accounting was maintained or broken;
- C-family routing worked or failed;
- donor leakage was contained or occurred;
- repair/quarantine routes functioned;
- the project can identify what owners need work before scaling.

Pilot evaluation does not determine whether the project is ready for large-scale conversion, canon, sourcebook prose, runtime import, final mechanics, live-play behavior, or training.

## 7. Evaluable pilot evidence requirements

Future pilot outputs are evaluable only if they preserve or report:

- packet identity
- donor source identity
- donor-family classification
- extraction run identity
- page/range truth
- source hash or hash-later policy
- evidence references
- construct inventory
- lawful outcome ledger
- mapping ledger
- rejected-import ledger
- source-local retention ledger
- pending_schema ledger
- repair queue status
- quarantine queue status
- confidence/review-routing notes
- legal/IP flags
- reviewer decision points
- C-family routing targets
- pilot output review status
- failure report shape
- benchmark/evaluation prerequisites

SM04 must not turn these into final JSON fields, JSON Schema, Pydantic models, database fields, runtime contracts, or final validators. These are evidence requirements at the rubric/control level only.

## 8. Evaluation subject boundaries

SM04 evaluation applies only to:

- Outputs from an explicitly authorized controlled pilot conversion.
- Outputs that carry verifiable packet identity, donor source identity, and extraction run identity.
- Outputs that have passed SM02 minimum readiness gates.
- Outputs that have been through the SM03 dry-run review process or an equivalent preflight.

SM04 evaluation does not apply to:

- Dry-run artifacts that did not produce conversion outputs.
- Packet metadata alone without conversion output.
- Hypothetical or planned outputs.
- D00-D19 source pack content.
- Outputs that bypassed SM02 readiness gates.
- Outputs from unauthorized or uncontrolled conversion runs.

## 9. Rubric interpretation labels

SM04 uses the following document-local evaluation labels. These are local rubric labels only, not registry values. They must not be written into registry fields such as `status`, `authority_level`, `test_status`, or `review_status`.

- `pass_for_pilot_evidence` — the evaluated dimension meets pilot evidence requirements.
- `pass_with_review_notes` — the evaluated dimension meets requirements but carries reviewer notes for future attention.
- `blocked_by_missing_evidence` — the evaluated dimension cannot be assessed because required evidence is missing.
- `blocked_by_lawful_outcome_gap` — the evaluated dimension is blocked because one or more constructs lack a lawful outcome.
- `blocked_by_routing_gap` — the evaluated dimension is blocked because C-family or `pending_schema` routing is incomplete.
- `blocked_by_legal_ip_risk` — the evaluated dimension is blocked by unresolved legal/IP risk.
- `blocked_by_donor_leakage` — the evaluated dimension is blocked because donor content leaked as Astra defaults.
- `blocked_by_runtime_or_mechanics_creep` — the evaluated dimension is blocked because runtime schemas, final mechanics, or implementation artifacts were created.
- `quarantine_required` — the evaluated output or dimension requires quarantine before further processing.
- `repair_required` — the evaluated output or dimension requires repair before re-evaluation.
- `human_review_required` — the evaluated dimension requires human judgment before a rubric label can be assigned.
- `not_evaluable` — the output or dimension cannot be evaluated under this rubric due to missing prerequisites.

These labels are for pilot evaluation use only. They do not confer registry status, canon permission, runtime permission, or training permission.

## 10. Core evaluation dimensions

SM04 defines the following evaluation dimensions at the rubric/control level only. Reviewers must assess each dimension for every evaluable pilot output:

1. **Packet identity and scope discipline.** Does the output carry correct, unique packet identity and stay within declared scope?
2. **Evidence/provenance completeness.** Are all required evidence references, provenance chains, extraction run identities, page/range truths, and source hashes present?
3. **Construct inventory completeness.** Does the output account for every visible construct from the source material?
4. **Lawful outcome completeness.** Does every construct have exactly one lawful outcome assigned (direct Astra mapping, normalized Astra mapping, source-local retained construct, quarantined construct pending later doctrine, escalated doctrine problem, or rejected import)?
5. **Mapping ledger clarity.** Does the mapping ledger clearly record construct-to-outcome mappings with rationale?
6. **C00-C14 or `pending_schema` routing correctness.** Does every output record route to a declared C-family target or `pending_schema` assignment without inventing fields or C15?
7. **Rejected-import containment.** Are rejected imports recorded with rationale and not leaking as Astra defaults?
8. **Source-local containment.** Are source-local records bounded to source/campaign context and not leaking as Astra baseline?
9. **Legal/IP risk containment.** Are legal/IP-flagged constructs routed to review or quarantine?
10. **Donor math/statblock/economy/class/dice/cosmology leakage prevention.** Does the output prevent donor-specific mechanics from becoming Astra defaults?
11. **Confidence/review-routing completeness.** Are confidence notes, review-routing flags, and human-review paths present for uncertain records?
12. **Repair/quarantine/failure-report completeness.** Are repair queue, quarantine queue, and failure-report paths declared for all items requiring them?
13. **Benchmark/evaluation question answerability.** Can the evaluation questions defined in this rubric actually be answered from the pilot output?
14. **Non-readiness boundary discipline.** Does the output respect all non-readiness boundaries (large-scale, runtime, canon, sourcebook, live-play, training)?
15. **Reviewer reproducibility.** Can a second reviewer independently arrive at the same rubric labels for the same output?

## 11. Evidence and provenance evaluation

Reviewers must evaluate whether each pilot output preserves:

- Extraction run identity traceable to a declared extraction run.
- Provenance chain from donor source through extraction to conversion output.
- Page/range truth confirmed against extraction artifacts.
- Source hash or hash-later policy status recorded and consistent.
- No evidence fabrication or hallucinated provenance.
- No copyrighted donor content embedded in evidence references.

Evidence failures route to `blocked_by_missing_evidence`, `repair_required`, or `quarantine_required`.

## 12. Lawful outcome completeness evaluation

Reviewers must evaluate whether each pilot output maintains:

- A visible construct inventory derived from evidence.
- Exactly one lawful outcome per construct: direct Astra mapping, normalized Astra mapping, source-local retained construct, quarantined construct pending later doctrine, escalated doctrine problem, or rejected import.
- No construct left without a declared lawful outcome.
- No contradictory lawful outcomes for the same construct.
- No floating "maybe useful later" constructs without explicit routing.
- No donor math, statblocks, economies, classes, dice, or cosmology leaking as Astra defaults through lawful outcome assignments.

Lawful outcome failures route to `blocked_by_lawful_outcome_gap`, `repair_required`, or `quarantine_required`.

## 13. C00-C14 and `pending_schema` routing evaluation

Reviewers must evaluate whether each pilot output routes correctly:

- Every output record has a declared C-family routing target or `pending_schema` assignment.
- C-family routing targets match the construct type according to C00-C14 family grammar: C01 creature/NPC, C02 item/gear, C03 ability/power/technique, C04 relic/implant/installable, C05 faction/institution, C06 location/site/region, C07 mission/scenario/adventure, C08 vehicle/ship/platform, C09 hazard/environment, C10 table/oracle, C11 companion/summon, C12 crafting/salvage/recipe, C13 map/diagram, C14 source-local setting/cosmology.
- `pending_schema` is used only when no C-family owner is stable, not as a field invention license.
- No C-family routing invents new fields, schema properties, or C15.
- C00 base inheritance requirements are referenced, not bypassed.
- Deferred families are explicitly marked deferred with reason.

Routing failures route to `blocked_by_routing_gap`, `repair_required`, or `quarantine_required`.

## 14. Rejected-import, source-local, and legal/IP containment evaluation

Reviewers must evaluate whether each pilot output contains:

- A rejected-import ledger with refusal rationale and evidence references for all rejected donor elements.
- A source-local retention ledger bounding source-local records to source/campaign context.
- Legal/IP flags for any constructs with trademark, copyright, or protected-expression risk.
- No rejected-import leakage (rejected donor elements appearing as Astra defaults).
- No source-local leakage (source-local records treated as Astra baseline).
- No legal/IP-flagged constructs without a review path or quarantine path.
- No donor proper nouns, setting cosmology, faction names, deity names, or protected expression imported as Astra defaults.

Containment failures route to `blocked_by_legal_ip_risk`, `blocked_by_donor_leakage`, `repair_required`, or `quarantine_required`.

## 15. Donor leakage evaluation

Reviewers must evaluate whether each pilot output prevents:

- Donor math leakage (donor-specific formulas, modifiers, or calculations adopted as Astra defaults).
- Donor statblock leakage (donor stat arrays, attribute distributions, or power levels adopted as Astra defaults).
- Donor economy leakage (donor-specific currency, pricing, or reward structures adopted as Astra defaults).
- Donor class/progression leakage (donor-specific class features, level progressions, or advancement structures adopted as Astra defaults).
- Donor dice-system leakage (donor-specific dice mechanics, roll conventions, or resolution systems adopted as Astra defaults).
- Donor cosmology leakage (donor-specific cosmological structures, planes, or metaphysics adopted as Astra defaults).
- D-series authority leakage (D00-D19 content treated as current doctrine, mechanics authority, or canon).
- RHBF hidden law (Ruthless Heavens Boundless Fate donor assumptions treated as secret Astra authority).

Leakage failures route to `blocked_by_donor_leakage`, `repair_required`, or `quarantine_required`.

## 16. Confidence, review-routing, and human-review evaluation

Reviewers must evaluate whether each pilot output provides:

- Confidence/review-routing notes for uncertain or ambiguous records.
- No automatic promotion of uncertain records without review.
- A human-review path for records requiring human judgment.
- Reviewer decision points identified and documented.
- C-family routing targets confirmed by a reviewer, not auto-assigned without review.

Confidence/review-routing failures route to `human_review_required`, `repair_required`, or `quarantine_required`.

## 17. Repair, quarantine, and failure-report evaluation

Reviewers must evaluate whether each pilot output provides:

- Repair queue status for any constructs or metadata requiring repair.
- Quarantine queue status for any constructs or metadata requiring isolation.
- A failure-report path for evaluation failures.
- Failure report shape including: packet identity, failure reason, affected constructs, recommended routing, and owner assignment.
- All failures routed to repair, quarantine, deferred gap ledger, `pending_schema`, or appropriate future owner.
- No failure silently dropped or ignored.

Repair/quarantine/failure-report failures route to `repair_required`, `quarantine_required`, or `human_review_required`.

## 18. Failure-class inventory

SM04 defines the following failure classes for pilot evaluation. Each failure class identifies a specific defect that blocks or degrades pilot evaluation quality:

- missing packet identity
- missing donor source identity
- missing donor-family classification
- missing extraction run identity
- missing page/range truth
- missing source hash or hash-later policy
- missing evidence references
- incomplete construct inventory
- missing lawful outcome
- contradictory lawful outcomes
- missing mapping ledger entry
- rejected-import leakage
- source-local leakage
- legal/IP unresolved risk
- C-family routing gap
- `pending_schema` misuse
- field invention
- donor math leakage
- donor statblock leakage
- donor economy leakage
- donor class/progression leakage
- donor dice-system leakage
- donor cosmology leakage
- D-series authority leakage
- RHBF hidden law
- final mechanics creep
- runtime schema creep
- canon/sourcebook/live-play/training creep
- missing confidence/review-routing notes
- missing repair/quarantine path
- missing failure report
- overclaiming pilot success

Each failure class routes to repair, quarantine, deferred gap ledger, `pending_schema`, doctrine escalation, or appropriate future owner. No failure class is silently dropped or ignored.

## 19. Benchmark/evaluation question design

SM04 evaluation questions must be:

- Answerable from the pilot output and its evidence artifacts alone.
- Scoped to the pilot evaluation dimensions defined in this document.
- Reproducible by independent reviewers.
- Free of assumptions about donor content that is not evidenced.
- Free of assumptions about final mechanics, runtime behavior, or canon status.

Evaluation questions must not:

- Require access to copyrighted donor source material beyond what extraction artifacts provide.
- Assume converted donor content is canon-ready, runtime-ready, sourcebook-ready, or training-ready.
- Assume benchmark corpora or evaluation corpora exist.
- Test final mechanics, exact math, or resolution systems.
- Test runtime import, backend behavior, or database schemas.
- Grade canon quality, sourcebook prose, or live-play behavior.

## 20. Reviewer workflow and decision record

The reviewer workflow proceeds as follows:

1. Confirm pilot output is eligible for evaluation (authorized pilot conversion, SM02 gates passed, SM03 dry-run or equivalent completed).
2. Confirm packet identity and scope (packet identity unique, donor source identity declared, donor-family classification assigned, extraction run identity recorded).
3. Confirm evidence/provenance completeness (evidence references, provenance chain, page/range truth, source hash or hash-later policy).
4. Confirm construct inventory completeness (every visible construct accounted for).
5. Evaluate lawful outcome accounting (every construct has exactly one lawful outcome, no gaps, no contradictions).
6. Evaluate mapping ledger clarity (construct-to-outcome mappings recorded with rationale).
7. Evaluate C00-C14 and `pending_schema` routing (every record routed, no field invention, no C15).
8. Evaluate rejected-import/source-local/legal/IP containment (ledgers present, no leakage, legal/IP flagged).
9. Evaluate donor leakage (no donor math/statblock/economy/class/dice/cosmology leakage, no D-series authority, no RHBF hidden law).
10. Evaluate confidence/review-routing notes (present for uncertain records, human-review path exists).
11. Evaluate repair/quarantine/failure-report completeness (queues declared, failure reports shaped, no silent drops).
12. Assign document-local rubric labels (from the label set defined in section 9).
13. Record reviewer decision and rationale (including which dimensions passed, which were blocked, and why).
14. Route failures to repair, quarantine, deferred gap ledger, `pending_schema`, or appropriate future owner.
15. State exactly what the pilot result may and may not prove (per section 20).

Each step must be completed before advancing to the next. The reviewer decision record must be preserved for reproducibility and future audit.

## 21. Pilot result interpretation

A pilot result may show:

- the packet/output loop is reviewable;
- evidence/provenance survived;
- lawful outcome accounting worked or failed;
- C-family routing worked or failed;
- `pending_schema` pressure was identified;
- donor leakage was contained or occurred;
- repair/quarantine routes worked or failed;
- future owners need work.

A pilot result may not prove:

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

Pilot results are evidence for one controlled conversion attempt. They do not generalize to corpus-scale, runtime-scale, or production-scale claims.

## 22. What pilot evaluation may and may not prove

Pilot evaluation may prove:

- That the conversion loop produced outputs that can be reviewed against SM04 rubric dimensions.
- That evidence/provenance artifacts survived the conversion process or were lost.
- That lawful outcome accounting was maintained or broken for the pilot set.
- That C-family routing and `pending_schema` routing were correctly applied or failed.
- That donor leakage was contained or occurred for specific constructs.
- That repair, quarantine, and failure-report routes were functional or missing.
- That specific evaluation dimensions are ready or require owner work.

Pilot evaluation may not prove:

- Large-scale corpus conversion readiness (only a small pilot set is evaluated).
- Canon readiness (no canon is created or promoted by evaluation).
- Sourcebook readiness (no sourcebook prose is produced or graded).
- Runtime readiness (no runtime schemas, backend schemas, or live-play behavior are created or tested).
- Final mechanics readiness (no mechanics, math, or formulas are finalized).
- Live-play readiness (no live-play behavior is created).
- Training readiness (no training data or evaluation corpora are created).
- Benchmark corpus readiness (no benchmark corpus is created).
- Model adapter readiness (no model adapters are created or tested).
- Database/schema implementation readiness (no database or schema implementations are created).

## 23. Large-scale conversion non-readiness boundary

A successful pilot evaluation does not prove large-scale corpus conversion readiness. Large-scale conversion requires:

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

SM04 is not runtime readiness, canon readiness, sourcebook readiness, live-play readiness, training readiness, or final mechanics readiness.

Runtime pressure routes to future runtime/Gate B owner only. SM04 does not create runtime schemas, backend schemas, database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, runtime kernel behavior, or live-play behavior.

Canon pressure routes to canon/conflict owners only. SM04 does not promote canon, accept lexicon, write sourcebook prose, or make pilot outputs sourcebook-ready.

Mechanics pressure routes to a future mechanics requirements owner only. SM04 does not create final mechanics, exact math, resolution dice, damage formulas, resource formulas, progression math, donor-statblock validators, or donor math defaults.

Training and evaluation pressure routes to later training/evaluation owners only. SM04 does not create training data, evaluation corpora, fine-tuning corpora, benchmark corpora, or model behavior policy.

## 25. Owner map and lawful fallbacks

| Pressure | Future owner route | Lawful fallback if not ready |
| --- | --- | --- |
| Pilot output eligibility review | future pilot conversion owner | defer evaluation, quarantine output, or block until preflight gate passes |
| Evidence/provenance evaluation | future conversion/evidence validation owner | repair queue, evidence gap ledger, quarantine |
| Lawful outcome evaluation | lawful outcome/conversion intake owner | block pilot output, repair ledger, quarantine |
| C00-C14 routing evaluation | C00/C-family schema owner and future validation/schema implementation owner | route to `pending_schema`, quarantine, or deferred gap ledger |
| `pending_schema` evaluation | C00/future validation/schema implementation owner | keep in pending_schema ledger, quarantine, or defer |
| Rejected-import/source-local/legal/IP evaluation | C00/C14 plus future review/legal owner | rejected-import ledger, source-local retention ledger, legal/IP review, quarantine |
| Donor leakage evaluation | future conversion integrity owner plus relevant future mechanics/schema owner | quarantine donor-shaped pressure, repair ledger, doctrine escalation |
| Confidence/human-review evaluation | future review owner | human review required, no promotion |
| Repair/quarantine/failure-report evaluation | extraction readiness and pilot conversion owner | repair queue, quarantine queue, failure report |
| Benchmark/evaluation rubric maintenance | future evaluation/benchmark owner | pilot evidence only, no benchmark claim, defer rubric updates |
| Mechanics pressure | future mechanics requirements owner only | doctrine escalation, `pending_schema`, quarantine donor statblocks |
| Runtime pressure | future runtime/Gate B owner only | block runtime import, quarantine runtime-shaped pressure |
| Canon/sourcebook/live-play/training pressure | appropriate later phase owner only | no promotion, no sourcebook prose, no live-play behavior, no training data |

Lawful fallbacks must be explicit. Silent import, hidden defaults, donor-law adoption, RHBF hidden law, and ownerless promotion are forbidden.

## 26. Risk register

| Risk | Why it matters | SM04 control |
| --- | --- | --- |
| Rubric treated as conversion authority | An evaluation rubric could be mistaken for permission to convert. | SM04 defines evaluation criteria only. Actual conversion requires a separate authorization gate. |
| Evaluation labels treated as registry values | Document-local rubric labels could be written into registry status fields. | Labels are explicitly marked as local rubric labels only and must not be written into registry fields. |
| Benchmark corpus creation creep | Defining evaluation dimensions could lead to creating benchmark corpora. | SM04 refuses benchmark corpora, evaluation corpora, training data, and fine-tuning data. |
| Donor content embedded in evaluation examples | Evaluation examples could embed copyrighted donor material. | SM04 refuses real donor excerpts, statblocks, tables, maps, setting prose, and proper nouns. |
| Donor mechanics leakage through evaluation | Evaluating donor-sourced outputs could normalize donor mechanics as Astra defaults. | Require lawful outcome accounting, donor leakage evaluation dimension, and containment checks. |
| Source-local/legal/IP leakage | Protected proper nouns or setting cosmology could enter Astra baseline through evaluation. | Require C14/legal review, source-local retention, legal/IP flags, and quarantine. |
| Missing schema disguised as implementation | Evaluation pressure could invent fields or C15. | Route to `pending_schema`, quarantine, or deferred gap ledger; refuse C00-C14 rewrite and C15 creation. |
| Over-trusting pilot evaluation results | A passed pilot evaluation could be mistaken for large-scale, canon, runtime, or training readiness. | Separate pilot evaluation from large-scale readiness, canon readiness, and all later phases. |
| Evaluation treated as final mechanics | Rubric dimensions could be mistaken for final mechanics requirements. | SM04 defines evaluation dimensions at rubric level only, not final mechanics, exact math, or resolution systems. |
| Runtime/canon/sourcebook/training creep | Evaluation artifacts could be treated as final product surfaces. | Explicit runtime/canon/sourcebook/live-play/training non-readiness boundary. |
| D-series authority creep | D00-D19 draft packs could be treated as evaluation authority or benchmark authority. | State D-series packs are draft source material only and cannot become benchmark or evaluation authority. |
| Overclaiming pilot success | A pilot evaluation pass could be overclaimed as broad readiness. | Require explicit statement of what pilot evaluation may and may not prove. |
| RHBF hidden law | Ruthless Heavens Boundless Fate donor assumptions could become secret evaluation authority. | Refuse RHBF as hidden law. Ruthless Heavens Boundless Fate may remain draft/donor pressure only where explicitly routed by current Astra doctrine; it must not become secret authority for evaluation decisions. |
| Reviewer bias or non-reproducibility | A single reviewer could assign labels inconsistently. | Require reviewer reproducibility as a core evaluation dimension and preserve decision records for audit. |

## 27. Recommended next PR after SM04

The recommended next PR after SM04 depends on what the evaluation rubric exposes.

Primary recommendation: SM05 actual pilot conversion authorization and preflight gate — defining the final go/no-go control for authorizing a later pilot conversion execution PR. This should still not run conversion directly; it should define the authorization gate that a future pilot conversion PR must pass.

Alternative if SM04 exposes rubric gaps: SM05 pilot evaluation rubric repair and reviewer calibration controls — defining how to repair specific rubric gaps and calibrate reviewers before authorizing actual pilot conversion.

The recommended next PR must not jump directly to final mechanics, actual broad conversion, runtime schemas, canon consolidation, sourcebook prose, live-play adapter behavior, or training corpus creation.

## 28. Acceptance criteria

SM04 is accepted only if:

- it exists as a post-SM03 pilot benchmark and evaluation rubric control file only;
- it states that SM04 does not run conversion and does not create converted donor content;
- it refuses benchmark corpora, evaluation corpora, training data, fine-tuning data, model behavior data, sourcebook-ready examples, final schemas, JSON Schema files, Pydantic models, final validators, runtime/backend/database contracts, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, canon, sourcebook prose, live-play behavior, training content, registry promotion, C00-C14 rewrite, C15 creation, D-series authority, and RHBF hidden law;
- it names SM00, SM01, SM02, SM03, C00, C01-C14, Batch C capstone, B11, Conversion IR, lawful outcome taxonomy, conversion intake, extraction readiness, donor family routing, evaluation/benchmark, and runtime/Gate B;
- it states that Batch B/B11 are operational routing doctrine, not final mechanics or runtime validation authority;
- it states that D00-D19 source packs are draft source material only and cannot become benchmark or evaluation authority;
- it defines "pilot benchmark/evaluation" as a bounded review method for future pilot conversion outputs;
- it lists all evaluable pilot evidence requirements;
- it includes document-local rubric interpretation labels and states they are not registry values;
- it includes all core evaluation dimensions;
- it includes the failure-class inventory;
- it includes reviewer workflow steps;
- it states what pilot evaluation may and may not prove;
- it includes large-scale conversion non-readiness boundary;
- it includes runtime/canon/sourcebook/live-play/training non-readiness boundary;
- it includes owner routing, lawful fallbacks, and a risk register;
- it recommends SM05 actual pilot conversion authorization/preflight gate or SM05 rubric repair/reviewer calibration controls without jumping directly to final mechanics or broad conversion;
- it does not promote C00-C14 registry records, rewrite C00-C14, add C15, treat D-series source packs as authority, or use RHBF as hidden law.

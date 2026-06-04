# SM03 Pilot Packet Fixture and Dry-Run Review Plan

## 1. Purpose and status

SM03 is a pilot packet fixture and dry-run review planning/control file only. It defines how a future pilot owner will select a tiny non-converted packet set, verify packet metadata, simulate readiness review against SM02 gates, document expected pass/fail decisions, record missing evidence, and decide whether the project is ready to attempt an actual pilot conversion later.

SM03 does not run conversion and does not create converted donor content. It does not select or embed real copyrighted donor excerpts, statblocks, tables, maps, setting prose, proper nouns, or protected expression. It is not a final schema file, not executable JSON Schema, not a Pydantic model, not a validator implementation, not final mechanics, not exact math, not canon, not sourcebook prose, not live-play behavior, not runtime behavior, not backend/database design, and not training or evaluation data.

Status posture:

- SM03 is a pilot packet fixture and dry-run review planning/control file only.
- SM03 may define a packet selection checklist and dry-run workflow, but does not create actual conversion outputs.
- SM03 defines readiness review procedures and future dry-run targets; it does not turn those targets into final JSON fields, JSON Schema, Pydantic models, database fields, runtime contracts, or final validators.
- SM03 may name required packet metadata, evidence checklists, dry-run pass/fail controls, owner routes, and lawful fallbacks, but it does not make any pilot output canon-ready, runtime-ready, sourcebook-ready, training-ready, or large-scale-corpus-ready.

## 2. Upstream controls and authority boundary

SM00 owns master sequencing for the schema/math/mechanics workstream. SM03 follows that sequence and does not supersede SM00.

SM01 owns validation/schema inventory posture. SM03 uses SM01's inventory as planning context.

SM02 owns minimum pilot conversion readiness gates and packet validation controls. SM03 turns SM02's readiness gates into a reviewable pre-conversion dry-run plan without executing conversion or creating converted content.

C00 owns shared content record base posture and the schema registry. C01-C14 own conversion-stage/canon-review family grammar and owner routing for their families. Batch C capstone readiness says the Batch C layer is ready with deferred gaps only; it does not promote canon, runtime, sourcebook, final mechanics, live-play, or training readiness.

Batch B, including B11, remains operational routing doctrine. Batch B/B11 are not final mechanics, not exact math, not final validators, and not runtime validation authority.

Conversion IR, lawful outcome taxonomy, conversion intake doctrine, extraction readiness classes and queues, donor family routing guide, conversion handoff contract, canon candidate/conflict ledger controls, evaluation/benchmark planning, roadmap/current state ledger posture, runtime kernel doctrine, and runtime/Gate B are upstream or downstream controls referenced for boundary alignment only.

D00-D19 source packs are draft source material only. They are not current doctrine, not final mechanics, not runtime authority, not canon, not sourcebook prose, not live-play behavior, not training data, and cannot become pilot packet authority or dry-run authority.

Existing handoff schemas under `schemas/` and `schemas/handoff/`, relevant handoff/validation/extraction/conversion-intake/quality/readiness scripts under `scripts/`, and related tests under `tests/` demonstrate partial operational infrastructure. SM03 does not revise those files and does not treat their existing operational shapes as final C-family, runtime, backend, database, mechanics, canon, or training contracts.

## 3. Existing dry-run readiness posture

The repository is close enough to define a dry-run review plan, but it is not ready for uncontrolled conversion or corpus-scale conversion.

Existing posture includes:

- Batch A doctrine files exist and remain source doctrine that SM03 must not rewrite.
- Batch B operational doctrine is complete through B11 and can inform routing pressure without becoming final mechanics or runtime authority.
- C00 and C01-C14 exist as conversion-stage/canon-review schema-family doctrine.
- Batch C capstone and unlock controls mark C-family doctrine ready for next workstream pressure with deferred gaps only.
- SM00 sequences schema/math/mechanics work after Batch C.
- SM01 inventories validation/schema needs and identifies readiness labels as document-local planning only.
- SM02 defines minimum pilot conversion readiness gates and packet validation controls at the doctrine/control level.
- Handoff packet, conversion intake, lawful outcome, mapping ledger, extraction readiness, repair queue, quarantine, and integrity scripts/schemas/tests exist as operational scaffolding.
- Evaluation/benchmark and runtime/Gate B materials are referenced as later controls, not as pilot or dry-run authority.

Therefore, SM03 can define a dry-run review plan that exercises SM02 gates against a tiny packet fixture set. It cannot claim conversion readiness, large-scale readiness, or any form of output-level readiness.

## 4. What SM03 owns

SM03 owns only these control-layer decisions:

1. The definition of "pilot packet fixture" as a future minimal, auditable, non-corpus-forming packet/test artifact used only to check readiness gate applicability, not as training data, evaluation corpus, canon, sourcebook prose, or conversion output.
2. The definition of "dry-run review" as a pre-conversion exercise where reviewers inspect packet metadata and readiness artifacts against SM02 gates without converting the packet.
3. The tiny pilot packet selection constraints for a first dry-run.
4. The recommended dry-run C-family pressure set.
5. The dry-run checklists covering SM02 readiness terms: packet metadata, evidence/provenance, lawful outcomes, C00-C14 routing, `pending_schema`, rejected-import/source-local/legal/IP, confidence/review-routing/human-review, repair/quarantine/failure-report, and benchmark/evaluation prerequisites.
6. The dry-run review workflow steps.
7. The dry-run pass/fail interpretation rules.
8. Owner routing and lawful fallback declarations for dry-run activities.
9. Risk controls specific to dry-run planning.

SM03 may identify pressure on future mechanics I/O, runtime/Gate B, canon, sourcebook, live-play, or training owners. It does not satisfy that pressure.

## 5. What SM03 must not own

SM03 must not:

- run conversion;
- create converted donor content;
- embed real copyrighted donor excerpts;
- embed donor statblocks;
- embed donor tables;
- embed donor maps;
- embed donor setting prose;
- import donor proper nouns as Astra defaults;
- create final output schemas;
- create final executable schemas;
- create JSON Schema files;
- create Pydantic models;
- create final C-family validators;
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

## 6. Pilot packet fixture concept

A "pilot packet fixture" is a future minimal, auditable, non-corpus-forming packet or test artifact used only to check readiness gate applicability. It is not training data, not an evaluation corpus, not canon, not sourcebook prose, not a conversion output, and not a runtime artifact.

Pilot packet fixtures are constructed to test whether SM02 readiness gates can be applied to a representative set of packet metadata and evidence artifacts. They do not carry donor content into the repo, do not embed copyrighted material, and do not produce converted records.

The fixture concept covers:

- Packet identity and metadata structure verification.
- Donor source identity and donor-family classification verification.
- Evidence and provenance traceability verification.
- Construct inventory shape verification.
- Lawful outcome, mapping, rejected-import, source-local, and `pending_schema` ledger shape verification.
- Readiness gate applicability testing.

Fixtures must be labeled as pilot evidence only. They are not training data, not evaluation corpora, not benchmark corpora, not fine-tuning inputs, not canon, and not sourcebook prose.

## 7. Tiny pilot packet selection constraints

SM03 requires that a future pilot preflight select only a tiny bounded packet set. The recommended maximum is 3-5 packet candidates for the first dry-run unless a later owner narrows it further.

Selection constraints:

- The dry-run packet set must be small enough for line-by-line human review.
- Each packet candidate must have verifiable packet identity, donor source identity, and extraction run identity.
- Each packet candidate must represent a distinct C-family routing pressure.
- The packet set must not expand beyond the declared count without explicit owner approval.
- Packet candidates must not embed copyrighted donor excerpts, statblocks, tables, maps, setting prose, or proper nouns in the repository.
- Packet candidates must be selected from legally available or appropriately licensed material only.
- D00-D19 source packs cannot serve as packet candidate authority.

## 8. Recommended dry-run C-family pressure set

The dry-run packet set should deliberately include pressure for:

- C01 creature/NPC — at least one packet candidate with actor-like constructs.
- C02 item/gear — at least one packet candidate with object-like constructs.
- C03 ability/power/technique — at least one packet candidate with capability-like constructs.
- C10 table/oracle — at least one packet candidate with table/oracle/generator constructs.
- Conditional C14 source-local setting/cosmology — only if legal/IP/source-local routing is ready and the pilot owner decides C14 pressure is needed for the dry-run.

C05, C06, C07, C08, C11, C12, and C13 remain deferred unless selected for a specific pressure test by a later owner. C04 and C09 may also remain deferred unless needed to disambiguate C01/C02/C03/C10 pressure.

A single packet candidate may cover multiple C-family pressures if its construct inventory spans families. The dry-run plan must declare which C-family routes each packet candidate is expected to exercise.

## 9. Packet metadata dry-run checklist

For each packet candidate in the dry-run set, reviewers must verify:

- [ ] Packet identity exists and is unique within the dry-run set.
- [ ] Donor source identity is declared and traceable.
- [ ] Donor-family classification is assigned.
- [ ] Extraction run identity is recorded.
- [ ] Page/range truth is declared and verifiable.
- [ ] Source hash or hash-later policy is declared.
- [ ] Packet metadata is internally consistent and non-contradictory.

Failure to verify any item blocks dry-run progression for that packet. Missing items route to repair queue, evidence gap ledger, or quarantine.

## 10. Evidence and provenance dry-run checklist

For each packet candidate, reviewers must verify:

- [ ] Evidence references link to a declared extraction run.
- [ ] Provenance chain can be traced from donor source to packet identity.
- [ ] Page/range truth can be confirmed against extraction artifacts.
- [ ] Source hash or hash-later policy status is recorded.
- [ ] No evidence fabrication or hallucinated provenance is present.
- [ ] Evidence references do not embed copyrighted donor content in the repository.

Failure to verify any item blocks dry-run progression. Missing evidence routes to repair queue, evidence gap ledger, or quarantine.

## 11. Lawful outcome dry-run checklist

For each packet candidate, reviewers must verify:

- [ ] A visible construct inventory can be identified from the packet metadata and evidence.
- [ ] The lawful outcome ledger can theoretically account for every construct in the inventory.
- [ ] Every construct can be assigned exactly one lawful outcome: direct Astra mapping, normalized Astra mapping, source-local retained construct, quarantined construct pending later doctrine, escalated doctrine problem, or rejected import.
- [ ] No construct is left without a declared lawful outcome route.
- [ ] The mapping ledger shape can record the construct-to-outcome mapping.
- [ ] No donor math, statblocks, economies, classes, dice, or cosmology leak as Astra defaults through the lawful outcome assignments.

Failure to account for any visible construct blocks dry-run progression. Unroutable constructs route to quarantine, `pending_schema`, or escalated doctrine problem.

## 12. C00-C14 routing dry-run checklist

For each packet candidate, reviewers must verify:

- [ ] Every output record has a declared C-family routing target or `pending_schema` assignment.
- [ ] C01, C02, C03, and C10 routing targets are exercised by at least one packet in the dry-run set.
- [ ] C14 routing is exercised only if legal/IP/source-local routing is ready.
- [ ] Deferred families (C05, C06, C07, C08, C11, C12, C13) are explicitly marked deferred with reason.
- [ ] C04 and C09 are deferred unless needed for disambiguation pressure.
- [ ] No C-family routing invents new fields, schema properties, or C15.
- [ ] `pending_schema` is used only when no C-family owner is stable, not as a field invention license.
- [ ] C00 base inheritance requirements from the doctrine are referenced, not bypassed.

Failure to route any record blocks dry-run progression. Unroutable records route to `pending_schema`, quarantine, or deferred gap ledger.

## 13. `pending_schema` and missing-owner dry-run checklist

For each packet candidate, reviewers must verify:

- [ ] The `pending_schema` ledger can record any constructs that lack a stable C-family owner.
- [ ] `pending_schema` entries carry full provenance, evidence references, and lawful outcome assignments.
- [ ] `pending_schema` is not used to invent fields, silently adopt donor defaults, or bypass C00-C14 routing.
- [ ] Missing-owner gaps are recorded with explicit future-owner routing or fallback.
- [ ] No silent field invention occurs through `pending_schema` usage.

Failure to maintain `pending_schema` discipline blocks dry-run progression.

## 14. Rejected-import, source-local, and legal/IP dry-run checklist

For each packet candidate, reviewers must verify:

- [ ] The rejected-import ledger can record donor elements that are explicitly refused.
- [ ] Rejected imports preserve refusal rationale, evidence references, and owner routing.
- [ ] The source-local retention ledger can record constructs retained for provenance but not adopted as Astra baseline.
- [ ] Source-local records are bounded to source/campaign context and do not leak as Astra defaults.
- [ ] Legal/IP flags are declared for any constructs with trademark, copyright, or protected-expression risk.
- [ ] Legal/IP-flagged constructs have a review path or quarantine path.
- [ ] No donor proper nouns, setting cosmology, faction names, deity names, or protected expression are imported as Astra defaults.

Failure to route rejected imports, source-local records, or legal/IP risks blocks dry-run progression. Leakage routes to quarantine, legal/IP review, or rejected-import ledger.

## 15. Confidence, review-routing, and human-review dry-run checklist

For each packet candidate, reviewers must verify:

- [ ] Confidence/review-routing notes are declared for uncertain or ambiguous records.
- [ ] No automatic promotion of uncertain records occurs.
- [ ] A human-review path exists for records that require human judgment.
- [ ] Reviewer decision points are identified and documented.
- [ ] C-family routing targets are confirmed by a reviewer, not auto-assigned without review.

Failure to provide confidence/review-routing notes blocks dry-run progression. Unreviewed records route to human review queue or quarantine.

## 16. Repair queue, quarantine, and failure-report dry-run checklist

For each packet candidate, reviewers must verify:

- [ ] Repair queue status is declared for any constructs or metadata requiring repair.
- [ ] Quarantine queue status is declared for any constructs or metadata requiring isolation.
- [ ] A failure-report path exists for dry-run failures.
- [ ] Failure report shape includes: packet identity, failure reason, affected constructs, recommended routing, and owner assignment.
- [ ] Failures route to repair, quarantine, deferred gap ledger, `pending_schema`, or appropriate future owner.
- [ ] No failure is silently dropped or ignored.

Failure to provide repair/quarantine/failure-report paths blocks dry-run progression.

## 17. Benchmark/evaluation dry-run checklist

For each packet candidate, reviewers must verify:

- [ ] Benchmark/evaluation prerequisites are declared before pilot outputs are used to argue broader readiness.
- [ ] Pilot packet fixtures are labeled as pilot evidence only, not as benchmark corpora, evaluation corpora, training data, or fine-tuning inputs.
- [ ] No pilot output is treated as a benchmark success or evaluation pass without explicit benchmark/evaluation review.
- [ ] Evaluation misuse routes to quarantine or explicit future evaluation/benchmark owner.

Failure to declare benchmark/evaluation prerequisites blocks any future claim of benchmark success.

## 18. Dry-run review workflow

The dry-run review workflow proceeds as follows:

1. Select tiny candidate packet set (3-5 packets maximum unless narrowed further by owner).
2. Confirm packet metadata exists for each candidate (packet identity, donor source identity, donor-family classification, extraction run identity, page/range truth, source hash or hash-later policy).
3. Confirm evidence/provenance traceability for each candidate.
4. Confirm visible construct inventory can be identified for each candidate.
5. Confirm lawful outcome ledger can theoretically account for every construct.
6. Confirm C00-C14 or `pending_schema` owner routing can be assigned for each construct.
7. Confirm rejected-import/source-local/legal/IP risk can be routed for each candidate.
8. Confirm confidence/review-routing and human-review path exists for uncertain records.
9. Confirm repair/quarantine/failure-report path exists for each candidate.
10. Confirm benchmark/evaluation prerequisites are declared.
11. Record dry-run pass/fail result for each candidate and for the overall dry-run.
12. Route failures to repair, quarantine, deferred gap ledger, `pending_schema`, or appropriate future owner.
13. Decide whether a later actual pilot conversion PR may be proposed based on dry-run results.

Each step must be completed before advancing to the next. Failure at any step blocks progression until the failure is routed.

## 19. Dry-run pass/fail interpretation

Dry-run pass criteria:

A dry-run pass means only that the packet set appears ready for a later controlled pilot conversion attempt. A dry-run pass does not mean conversion success, large-scale conversion readiness, canon readiness, sourcebook readiness, runtime readiness, final mechanics readiness, live-play readiness, training readiness, or benchmark success.

A dry-run pass requires:

- Every packet candidate in the set has verified packet metadata.
- Every packet candidate has traceable evidence/provenance.
- Every visible construct has a declared lawful outcome route.
- Every record has a C-family routing target or `pending_schema` assignment.
- All rejected-import, source-local, and legal/IP risks are routed.
- All confidence/review-routing notes are present for uncertain records.
- All repair/quarantine/failure-report paths are declared.
- All benchmark/evaluation prerequisites are declared.

Dry-run fail criteria:

A dry-run fail blocks actual pilot conversion until the failure is routed.

Dry-run fail conditions include:

- Missing packet identity.
- Missing donor source identity.
- Missing donor-family classification.
- Missing extraction run identity.
- Missing page/range truth.
- Missing evidence references.
- Missing construct inventory.
- Inability to account for lawful outcomes for any visible construct.
- Inability to route to C00-C14 or `pending_schema` for any record.
- Rejected-import leakage (donor elements adopted as Astra defaults without explicit routing).
- Source-local leakage (source-local records treated as Astra baseline).
- Legal/IP risk without review/quarantine path.
- Missing confidence/review-routing notes for uncertain records.
- Missing repair/quarantine/failure report path.
- Benchmark/evaluation prerequisites missing.
- Any attempt to create converted donor content during the dry-run.
- Any attempt to draft final schema/mechanics/runtime/canon/sourcebook/live-play/training content during the dry-run.
- D-series authority leakage (D00-D19 treated as current doctrine or pilot authority).
- RHBF hidden law (rules-hidden-behind-fiction used as secret authority).

## 20. What SM03 evidence may and may not prove

SM03 dry-run evidence may prove:

- That SM02 readiness gates can be applied to a tiny selected packet set.
- That packet metadata and evidence artifacts exist in a reviewable shape.
- That lawful outcome, C-family routing, and `pending_schema` routing can be theoretically assigned.
- That rejected-import, source-local, and legal/IP risks can be identified and routed.
- That repair, quarantine, and failure-report paths can be declared.

SM03 dry-run evidence may not prove:

- Conversion success (no conversion runs).
- Large-scale corpus conversion readiness (only a tiny set is reviewed).
- Canon readiness (no canon is created or promoted).
- Sourcebook readiness (no sourcebook prose is produced).
- Runtime readiness (no runtime schemas, backend schemas, or live-play behavior are created).
- Final mechanics readiness (no mechanics, math, or formulas are finalized).
- Live-play readiness (no live-play behavior is created).
- Training readiness (no training data or evaluation corpora are created).
- Benchmark success (no benchmarks are run).

## 21. Large-scale conversion non-readiness boundary

A successful SM03 dry-run does not prove large-scale corpus conversion readiness. Large-scale conversion requires:

- actual pilot conversion with converted output evidence;
- pilot output review and evidence validation;
- broad donor-family coverage beyond the tiny dry-run set;
- mechanics, math, and resolution system readiness;
- runtime/Gate B readiness;
- canon/conflict ledger readiness;
- broad evaluation readiness;
- training readiness.

Large-scale conversion requires later owner-controlled readiness gates after pilot evidence is reviewed.

## 22. Runtime/canon/sourcebook/live-play/training non-readiness boundary

SM03 is not runtime readiness, canon readiness, sourcebook readiness, live-play readiness, training readiness, or final mechanics readiness.

Runtime pressure routes to future runtime/Gate B owner only. SM03 does not create runtime schemas, backend schemas, database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, runtime kernel behavior, or live-play behavior.

Canon pressure routes to canon/conflict owners only. SM03 does not promote canon, accept lexicon, write sourcebook prose, or make pilot outputs sourcebook-ready.

Mechanics pressure routes to a future mechanics requirements owner only. SM03 does not create final mechanics, exact math, resolution dice, damage formulas, resource formulas, progression math, donor-statblock validators, or donor math defaults.

Training and evaluation pressure routes to later training/evaluation owners only. SM03 does not create training data, evaluation corpora, fine-tuning corpora, benchmark corpora, or model behavior policy.

## 23. Owner map and lawful fallbacks

| Pressure | Future owner route | Lawful fallback if not ready |
| --- | --- | --- |
| Packet candidate selection | future pilot conversion owner | defer dry-run, narrow packet set, or quarantine candidate |
| Packet metadata review | future pilot conversion owner plus extraction readiness owner | repair queue, evidence gap ledger, quarantine |
| Evidence/provenance review | future conversion/evidence validation owner | repair queue, evidence gap ledger, quarantine |
| Lawful outcome review | lawful outcome/conversion intake owner | block pilot output, repair ledger, quarantine |
| C00-C14 routing review | C00/C-family schema owner and future validation/schema implementation owner | route to `pending_schema`, quarantine, or deferred gap ledger |
| `pending_schema` review | C00/future validation/schema implementation owner | keep in pending_schema ledger, quarantine, or defer |
| Rejected-import/source-local/legal/IP review | C00/C14 plus future review/legal owner | rejected-import ledger, source-local retention ledger, legal/IP review, quarantine |
| Confidence/human-review path | future review owner | human review required, no promotion |
| Repair/quarantine/failure reporting | extraction readiness and pilot conversion owner | repair queue, quarantine queue, failure report |
| Benchmark/evaluation prerequisite review | future evaluation/benchmark owner | pilot evidence only, no benchmark claim |
| Mechanics pressure | future mechanics requirements owner only | doctrine escalation, `pending_schema`, quarantine donor statblocks |
| Runtime pressure | future runtime/Gate B owner only | block runtime import, quarantine runtime-shaped pressure |
| Canon/sourcebook/live-play/training pressure | appropriate later phase owner only | no promotion, no sourcebook prose, no live-play behavior, no training data |

Lawful fallbacks must be explicit. Silent import, hidden defaults, donor-law adoption, RHBF hidden law, and ownerless promotion are forbidden.

## 24. Risk register

| Risk | Why it matters | SM03 control |
| --- | --- | --- |
| Dry-run scope creep | A small dry-run review could expand into unreviewed broad conversion. | Predeclare tiny packet set (3-5 max), declare stop conditions, require owner approval for expansion. |
| Fixture treated as conversion output | Pilot packet fixtures could be mistaken for converted content. | Label fixtures as pilot evidence only. Refuse conversion output claims. |
| Donor content embedded in repo | Copyrighted material could enter the codebase through fixture creation. | Refuse real donor excerpts, statblocks, tables, maps, setting prose, and proper nouns. |
| Donor mechanics leakage | Donor math/statblocks/economies/classes/dice could become Astra defaults. | Require lawful outcomes, rejected-import ledger, source-local retention ledger, C-family owner routes, and fail criteria. |
| Source-local/legal/IP leakage | Protected proper nouns or setting cosmology could enter Astra baseline. | Require C14/legal review, source-local retention, legal/IP flags, and quarantine. |
| Missing schema disguised as implementation | Dry-run pressure could invent fields or C15. | Route to `pending_schema`, quarantine, or deferred gap ledger; refuse C00-C14 rewrite and C15 creation. |
| Evidence fabrication | Fake provenance could be created to pass dry-run gates. | Require traceable extraction run identity, page/range truth, and source hash or hash-later policy. |
| Over-trusting dry-run results | A passed dry-run could be mistaken for conversion readiness or large-scale readiness. | Separate dry-run readiness from conversion readiness, large-scale readiness, and all later phases. |
| Runtime/canon/sourcebook/training creep | Dry-run artifacts could be treated as final product surfaces. | Explicit runtime/canon/sourcebook/live-play/training non-readiness boundary. |
| D-series authority creep | D00-D19 draft packs could be treated as current doctrine or dry-run authority. | State D-series packs are draft source material only and cannot become pilot packet authority. |
| Evaluation misuse | Pilot fixtures could become benchmark/evaluation or training corpora. | Require benchmark/evaluation prerequisites and refuse training/evaluation corpora. |
| RHBF hidden law | Rules-hidden-behind-fiction used as secret authority for dry-run decisions. | Refuse RHBF as hidden law. All dry-run decisions must be traceable to declared doctrine. |

## 25. Recommended next PR after SM03

The recommended next PR after SM03 depends on what the dry-run plan exposes.

Primary recommendation: SM04 pilot benchmark and evaluation rubric controls — defining how pilot outputs will be evaluated when an actual pilot conversion is eventually run, including benchmark rubric, evaluation criteria, reviewer workflow, and pass/fail interpretation for pilot outputs.

Alternative if SM03 reveals packet readiness gaps: SM04 pilot packet repair and preflight gap controls — defining how to repair the specific readiness gaps exposed by the SM03 dry-run plan before attempting actual pilot conversion.

The recommended next PR must not jump directly to final mechanics, actual broad conversion, runtime schemas, canon consolidation, sourcebook prose, live-play adapter behavior, or training corpus creation.

## 26. Acceptance criteria

SM03 is accepted only if:

- it exists as a post-SM02 pilot packet fixture and dry-run review planning/control file only;
- it states that SM03 does not run conversion and does not create converted donor content;
- it states that SM03 does not select or embed real copyrighted donor excerpts, statblocks, tables, maps, setting prose, proper nouns, or protected expression;
- it refuses final executable schemas, JSON Schema files, Pydantic models, final C-family validators, runtime/backend/database schemas, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, resolution dice, damage formulas, resource formulas, progression math, donor-statblock validators that treat donor statblocks as Astra defaults, canon, sourcebook prose, live-play behavior, training data, and evaluation corpora;
- it names SM00, SM01, SM02, C00, C01-C14, Batch C capstone, B11, Conversion IR, lawful outcome taxonomy, conversion intake, extraction readiness, donor family routing, evaluation/benchmark, and runtime/Gate B;
- it states that Batch B/B11 are operational routing doctrine, not final mechanics or runtime validation authority;
- it states that D00-D19 source packs are draft source material only and cannot become pilot packet authority;
- it defines "pilot packet fixture" as a future minimal, auditable, non-corpus-forming packet/test artifact used only to check readiness gate applicability;
- it defines "dry-run review" as a pre-conversion exercise where reviewers inspect packet metadata and readiness artifacts against SM02 gates without converting the packet;
- it recommends a tiny bounded dry-run packet set of 3-5 packet candidates;
- it recommends initial C01, C02, C03, C10, and conditional C14 pressure routes and permits C05, C06, C07, C08, C11, C12, and C13 deferral unless selected for pressure test, with C04 and C09 also deferrable unless needed for disambiguation;
- it lists packet identity, donor source identity, donor-family classification, extraction run identity, page/range truth, source hash or hash-later policy, evidence references, construct inventory, lawful outcome ledger, mapping ledger, rejected-import ledger, source-local retention ledger, pending_schema ledger, repair queue status, quarantine queue status, confidence/review-routing notes, legal/IP flags, reviewer decision points, C-family routing targets, pilot output review status, failure report shape, and benchmark/evaluation prerequisites;
- it includes dry-run checklists, a dry-run review workflow, and dry-run pass/fail interpretation;
- it states that a dry-run pass does not mean conversion success, large-scale conversion readiness, canon readiness, sourcebook readiness, runtime readiness, final mechanics readiness, live-play readiness, training readiness, or benchmark success;
- it includes owner routing, lawful fallbacks, and a risk register;
- it recommends SM04 pilot benchmark/evaluation rubric controls or SM04 pilot packet repair/preflight gap controls without jumping directly to final mechanics;
- it does not promote C00-C14 registry records, rewrite C00-C14, add C15, treat D-series source packs as authority, or use RHBF as hidden law.

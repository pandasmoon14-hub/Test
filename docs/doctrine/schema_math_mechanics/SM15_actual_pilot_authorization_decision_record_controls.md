# SM15 Actual Pilot Authorization Decision Record Controls

## 1. Purpose and status

SM15 is an actual pilot authorization decision record control file only. It defines how an actual pilot authorization decision record may be structured and reviewed for a future metadata-only real pilot authorization packet. SM15 does not itself create an actual completed authorization decision for a real donor packet because no owner-approved metadata-only packet shell exists yet. Therefore this PR is a decision-record control layer only.

SM15 does not run conversion. SM15 does not execute a pilot. SM15 does not create actual converted donor content or pilot outputs. SM15 is not pilot evidence, not legal/IP clearance, not source clearance, not runtime readiness, not canon readiness, not sourcebook readiness, not final-mechanics readiness, not live-play readiness, and not training readiness.

SM15 defines the control posture for a future actual pilot authorization decision record. SM14 defined how a metadata-only real packet shell would be validated. SM15 defines how a later owner-controlled authorization decision record would document whether a validated shell is authorized, blocked, repaired, quarantined, or deferred before any separate execution proposal.

## 2. Upstream controls and authority boundary

SM15 is downstream of Batch A doctrine, Batch B operational doctrine through B11, C00-C14 schema-family doctrine, the Batch C capstone, the Batch C unlock/readiness gate, and SM00-SM14. The repository inspection posture for SM15 includes the pilot conversion scaffold README, placeholder packet manifest, placeholder review harness, SM09 dry authorization packet template, the doctrine registry, C00-C14, Batch C capstone files, B01-B11, Batch A doctrine, conversion intake schema/doctrine, lawful outcome taxonomy, Conversion IR, conversion handoff contract, extraction readiness classes and queues, donor family routing guide, canon candidate/conflict ledger posture, evaluation/benchmark pack, roadmap/current state ledger, runtime kernel doctrine, Gate B, and existing tests for doctrine registry, C-family, Batch B, conversion intake, extraction readiness, handoff packets, quality gates, runtime boundaries, validation, schema, SM00-SM14, and scaffold no-donor safety.

SM00 owns master sequencing. SM01 owns validation/schema inventory posture. SM02 owns minimum pilot readiness gates. SM03 owns dry-run review planning. SM04 owns pilot benchmark/evaluation rubric controls. SM05 owns authorization/preflight gate posture. SM06 owns controlled execution/output capture planning. SM07 owns scaffold/review-harness posture. SM08 owns placeholder validation/no-donor safety posture. SM09 owns the dry authorization packet template. SM10 owns dry authorization validation/reviewer decision-gate posture. SM11 owns real packet preparation controls. SM12 owns external-reference review-gate controls. SM13 owns metadata-only assembly controls. SM14 owns metadata-only shell validation/reviewer-gate controls.

C00 owns shared content record base posture and C01-C14 own conversion-stage/canon-review family grammar. Batch B and B11 are operational routing doctrine, not final mechanics or runtime validation authority. D00-D19 source packs are draft source material only and cannot become decision-record authority, execution authority, pilot conversion authority, benchmark authority, evaluation authority, mechanics authority, runtime authority, canon, sourcebook authority, live-play authority, or training authority. RHBF must not be used as hidden law.

## 3. Existing authorization decision posture

Existing posture before SM15 is intentionally staged and non-executing:

- SM09 dry template: placeholder/synthetic/non-donor template.
- SM10 dry validation gate: validation of dry packets.
- SM11 preparation controls: controls for preparing a future real packet.
- SM12 external-reference review gate: review of metadata-only external references.
- SM13 metadata-only assembly controls: arrangement of shell sections and metadata-only slots.
- SM14 shell validation and reviewer gate: validation of assembled metadata-only shell posture.
- SM15 decision-record controls: control posture for documenting a later authorization decision.
- Future actual decision record: not created by this PR unless a separate owner-approved packet shell exists, which it does not.
- Future execution PR: still downstream and not created by SM15.

The pilot conversion scaffold README, placeholder packet manifest, placeholder review harness, and dry authorization packet template remain Markdown, placeholder, synthetic, non-donor materials only. They do not supply donor content, legal/IP clearance, source clearance, execution approval, or conversion evidence.

## 4. What SM15 owns

SM15 owns only decision-record control posture for a future actual pilot authorization decision record. It may define how reviewers document whether a validated future metadata-only real packet shell is authorized for a later execution proposal review, blocked, routed to repair, routed to quarantine, routed to legal/IP review, routed to `pending_schema`, routed to rejected import, routed to source-local retention, routed to deferred gap ledger, or returned to the appropriate future owner.

SM15 may define decision eligibility requirements, decision record required contents, decision outcome labels, authorization-granted boundary, authorization-blocked boundary, repair/quarantine/deferred-gap/`pending_schema` routing, packet scope and C-family pressure decision limits, evidence/provenance pointer decision review, lawful outcome and mapping ledger decision review, rejected-import/source-local/legal/IP/`pending_schema` decision review, confidence/review-routing/repair/quarantine/failure-report decision review, donor leakage hard-fail decision rule, decision workflow, decision record validation expectations, document-local authorization decision labels, risk routing, lawful fallbacks, and acceptance criteria.

SM15 may state how a decision record documents that SM00-SM14 dependencies are satisfied, C-family pressure boundaries are preserved, no-donor boundaries are maintained, and lawful fallback routing is explicit.

## 5. What SM15 must not own

SM15 must not own a completed real authorization decision, execution approval, conversion execution, output capture, completed pilot evidence, legal/IP clearance, source clearance, benchmark corpus creation, evaluation corpus creation, final schema design, final validators, runtime/backend/database contracts, final mechanics, canon promotion, sourcebook prose, live-play behavior, training data, model behavior policy, or registry promotion.

SM15 does not select, embed, quote, paraphrase, transform, summarize, or convert real copyrighted donor excerpts, donor statblocks, donor tables, donor maps, donor setting prose, protected expression, or donor proper nouns. SM15 does not import donor proper nouns as Astra defaults. SM15 does not create benchmark corpora, does not create evaluation corpora, does not create training data, fine-tuning data, model behavior data, sourcebook-ready examples, final schemas, executable JSON Schema, Pydantic models, final validators, runtime/backend/database schemas, runtime/backend/database contracts, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, canon, sourcebook prose, live-play behavior, accepted lexicon, or registry promotion. SM15 does not rewrite C00-C14. SM15 does not add C15.

SM15 cannot waive SM02 gates, cannot bypass SM05 authorization/preflight controls, cannot treat a decision record as execution, cannot treat decision records as execution approval, cannot treat no-donor sentinel checks as legal/IP clearance, cannot treat metadata as donor content or conversion evidence, and cannot treat external-reference readiness as source clearance.

## 6. Authorization decision record definition

An authorization decision record is a metadata-only control artifact that records whether a validated future metadata-only real packet shell is:

- authorized for a later execution proposal review;
- blocked;
- routed to repair;
- routed to quarantine;
- routed to legal/IP review;
- routed to `pending_schema`;
- routed to rejected import;
- routed to source-local retention;
- routed to deferred gap ledger;
- or returned to the appropriate future owner.

The decision record is documentation only. It is not execution approval, not conversion approval, not legal/IP clearance, not source clearance, not pilot evidence, not output creation, not broad conversion authorization, and not a substitute for a separate execution proposal PR.

## 7. Decision record versus execution approval boundary

A decision record documents authorization posture for a future execution proposal review. It does not authorize execution. It does not approve conversion. It does not clear legal/IP questions. It does not clear source access. It does not create pilot outputs. It does not authorize broad conversion. It only allows a later, separate execution proposal PR to be considered under SM02-SM15 controls.

Execution approval requires a separate execution proposal PR that is reviewed and accepted after all SM02-SM15 gates pass. A decision record that states "ready for execution proposal review" is not execution approval.

## 8. Decision eligibility requirements

A future decision record may not be created unless:

- SM02 no-waiver posture is satisfied;
- SM03 dry-run posture is represented;
- SM04 evaluation/rubric handoff is represented;
- SM05 authorization/preflight posture is represented;
- SM06 execution/output-capture posture is represented;
- SM07 scaffold/review-harness posture is represented;
- SM08 no-donor safety posture is represented;
- SM09 dry template reference is represented;
- SM10 reviewer validation posture is represented;
- SM11 preparation-control posture is represented;
- SM12 external-reference review posture is represented;
- SM13 metadata-only assembly posture is represented;
- SM14 shell-validation posture is represented;
- legal/IP owner is named;
- future review owner is named;
- source-clearance boundary is explicit;
- no donor content is embedded in the repo;
- C-family pressure remains bounded;
- repair, quarantine, rejected-import, source-local, `pending_schema`, legal/IP, and failure-report routes exist.

If any eligibility requirement is missing, the decision record must block, repair, quarantine, or route to the appropriate future owner.

## 9. Metadata-only decision posture

SM15 decision records are metadata-only. They reference shell sections, owner routes, dependency routes, lawful fallback routes, and failure routes without containing donor content, execution approval, final schemas, runtime contracts, final mechanics, canon/sourcebook/live-play/training content, or registry promotion.

Metadata is not donor content, not legal/IP clearance, not source clearance, not conversion evidence, not canon evidence, and not execution approval.

## 10. No-donor-in-repository decision rule

SM15 requires that a decision record contains no real donor content in the repository. The decision record must not select, embed, quote, paraphrase, transform, summarize, or convert real copyrighted donor excerpts, donor statblocks, donor tables, donor maps, donor setting prose, protected expression, or donor proper nouns.

Any embedded real donor excerpt, donor statblock, donor table, donor map, donor setting prose, donor proper noun import as an Astra default, or converted donor content is a hard failure. The correct route is repair, quarantine, rejected import, legal/IP review, or source-local retention according to the relevant owner path.

## 11. Legal/IP and source-clearance decision boundary

SM15 requires reviewers to confirm that a legal/IP owner slot exists and that source-clearance boundary slots are explicit. SM15 does not itself provide legal/IP clearance or source clearance. Metadata is not legal/IP clearance, external-reference readiness is not source clearance, and no-donor sentinel checks are not legal/IP clearance.

If legal/IP disposition, source-clearance boundary, or source-access owner routing is missing or ambiguous, the decision record must block, repair, quarantine, or route to the future owner rather than advance.

## 12. SM02 no-waiver decision requirement

SM15 requires a visible SM02 no-waiver posture. SM02 minimum pilot readiness gates may not be waived by SM15, by decision record, by reviewer convenience, by metadata-only references, by dry-run success, or by later execution pressure.

A decision record that omits SM02 no-waiver posture receives a blocking label such as `authorization_decision_blocked_by_missing_sm02_gate`.

## 13. SM03 dry-run decision requirement

SM15 requires a visible SM03 dry-run posture. Reviewers must confirm that the decision record points to dry-run review planning without treating a dry-run posture as real authorization, execution approval, donor clearance, or pilot evidence.

Missing or contradictory SM03 dry-run posture must route to repair, deferred gap tracking, or the future owner.

## 14. SM04 evaluation-rubric decision requirement

SM15 requires a visible SM04 evaluation/rubric handoff slot. Reviewers confirm that evaluation and benchmark owner routing exists for later post-execution review; SM15 does not create benchmark corpora, evaluation corpora, pilot evaluation evidence, or evaluation success.

The SM04 slot must preserve that rubric readiness is downstream review infrastructure, not conversion output and not authorization.

## 15. SM05 authorization/preflight decision requirement

SM15 requires a visible SM05 authorization/preflight posture. Reviewers confirm that the decision record has a place for authorization decision while also stating that SM15 does not make an actual authorization decision and cannot bypass SM05 authorization/preflight controls.

A missing SM05 authorization/preflight posture blocks decision advancement and may receive `authorization_decision_blocked_by_missing_sm05_preflight`.

## 16. SM06 execution/output-capture decision requirement

SM15 requires a visible SM06 execution/output-capture slot. Reviewers confirm only that a non-executing decision record has downstream space for controlled execution and output-capture planning if a later authorization exists.

The SM06 slot must not be filled with execution approval, pilot outputs, converted donor content, runtime contracts, or final validators.

## 17. SM07 scaffold/review-harness decision requirement

SM15 requires a visible SM07 scaffold/review-harness slot. Reviewers confirm that scaffold and review-harness posture is referenced as placeholder control infrastructure only.

The SM07 slot does not authorize execution, does not create donor content, and does not transform the placeholder packet manifest or placeholder review harness into source clearance or conversion evidence.

## 18. SM08 no-donor safety decision requirement

SM15 requires a visible SM08 no-donor safety slot. Reviewers confirm that placeholder/no-donor sentinel posture remains active and that donor leakage hard-fail criteria are present.

SM08 sentinel checks are safety controls, not legal/IP clearance. A decision record that treats no-donor sentinel checks as legal/IP clearance must be blocked or repaired.

## 19. SM09 dry template decision requirement

SM15 requires a visible SM09 dry template reference. Reviewers confirm that the decision record understands the SM09 dry authorization packet template as dry, placeholder/synthetic/non-donor, Markdown-only scaffold material.

The SM09 dry template is not a real packet, not a real donor packet, not authorization, not execution approval, and not conversion evidence.

## 20. SM10 reviewer validation decision requirement

SM15 requires a visible SM10 reviewer validation slot. Reviewers confirm that dry authorization validation and reviewer decision-gate posture remains a dependency and is not confused with real shell authorization.

SM10 validation of dry packets does not authorize actual execution and does not clear legal/IP or source access for real donor materials.

## 21. SM11 preparation-control decision requirement

SM15 requires a visible SM11 preparation-control slot. Reviewers confirm that real packet preparation controls exist before a decision record is treated as ready for authorization review.

SM11 preparation controls are not a completed real authorization packet, not authorization, and not execution approval.

## 22. SM12 external-reference review decision requirement

SM15 requires a visible SM12 external-reference review slot. Reviewers confirm that metadata-only external references have owner routing and source-clearance boundaries.

SM12 external-reference review gate posture is not source clearance, not legal/IP clearance, not donor-content import, and not conversion evidence.

## 23. SM13 metadata-only assembly decision requirement

SM15 requires a visible SM13 metadata-only assembly slot. Reviewers confirm that metadata-only assembly controls are referenced and that the decision record does not treat assembly as completion or authorization.

SM13 metadata-only assembly controls are not a completed packet, not authorization, and not execution approval.

## 24. SM14 shell-validation decision requirement

SM15 requires a visible SM14 shell-validation posture. Reviewers confirm that metadata-only shell validation and reviewer-gate controls passed before a decision record is considered.

A missing SM14 shell-validation posture blocks decision advancement and may receive `authorization_decision_blocked_by_missing_sm14_shell_validation`.

## 25. Decision record required contents

SM15 defines required contents for a future decision record, as prose requirements only. These are decision-record content requirements only. Do not turn them into final JSON fields, JSON Schema, Pydantic models, database fields, runtime contracts, final validators, or implementation contracts.

Required contents include:

- decision record identity
- linked metadata-only packet shell identity
- decision status and non-execution statement
- decision owner
- legal/IP owner
- future execution proposal owner, if applicable
- SM02 no-waiver confirmation
- SM03 dry-run confirmation
- SM04 evaluation/rubric handoff confirmation
- SM05 authorization/preflight confirmation
- SM06 output-capture confirmation
- SM07 scaffold/review-harness confirmation
- SM08 no-donor safety confirmation
- SM09 dry template confirmation
- SM10 reviewer validation confirmation
- SM11 preparation-control confirmation
- SM12 external-reference review confirmation
- SM13 metadata-only assembly confirmation
- SM14 shell-validation confirmation
- C-family pressure target
- packet count
- legal/IP disposition
- source-clearance boundary
- evidence/provenance pointer posture
- lawful outcome route
- mapping ledger route
- rejected-import route
- source-local retention route
- `pending_schema` route
- repair route
- quarantine route
- failure-report route
- donor leakage hard-fail result
- decision rationale
- final non-readiness statement

These are validation expectations only. They must not create final schema fields, runtime/backend/database contracts, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, or registry values. Metadata is not donor content, not legal/IP clearance, not source clearance, not conversion evidence, not canon evidence, and not execution approval. External-reference readiness is not source clearance. No-donor sentinel checks are not legal/IP clearance.

## 26. Decision outcome labels

SM15 may use document-local decision outcome labels only. They are not registry values. They must not be written into registry fields such as `status`, `authority_level`, `test_status`, or `review_status`.

Labels include:

- `authorization_decision_ready_for_execution_proposal_review`
- `authorization_decision_blocked_by_missing_sm02_gate`
- `authorization_decision_blocked_by_missing_sm05_preflight`
- `authorization_decision_blocked_by_missing_sm14_shell_validation`
- `authorization_decision_blocked_by_missing_legal_ip_owner`
- `authorization_decision_blocked_by_source_clearance_gap`
- `authorization_decision_blocked_by_embedded_donor_content`
- `authorization_decision_blocked_by_scope_expansion`
- `authorization_decision_blocked_by_runtime_or_mechanics_creep`
- `authorization_decision_requires_repair`
- `authorization_decision_requires_quarantine`
- `authorization_decision_requires_legal_ip_review`
- `authorization_decision_requires_pending_schema`
- `authorization_decision_rejected_import`
- `authorization_decision_source_local_only`
- `authorization_decision_not_execution`
- `authorization_decision_not_conversion`

These are document-local labels only. They are not registry values and must not be written into registry fields.

## 27. Authorization-granted boundary

SM15 may define a document-local "ready for execution proposal review" decision label, but must state:

- this is not execution approval;
- this is not conversion approval;
- this is not legal/IP clearance;
- this is not source clearance;
- this is not pilot evidence;
- this does not create output;
- this does not authorize broad conversion;
- this only allows a later, separate execution proposal PR to be considered under SM02-SM15 controls.

Authorization-granted means only that a future execution proposal PR may be submitted for review. It does not mean execution can start.

## 28. Authorization-blocked boundary

Authorization-blocked means the decision record identifies one or more blocking conditions that prevent even a future execution proposal review. Blocking conditions include missing SM02 no-waiver posture, missing SM05 authorization/preflight posture, missing SM14 shell-validation posture, missing legal/IP owner, source-clearance gaps, embedded donor content, scope expansion, or runtime/mechanics creep.

A blocked decision record must route to repair, quarantine, legal/IP review, source-local retention, rejected import, `pending_schema`, or the appropriate future owner.

## 29. Repair, quarantine, deferred-gap, and `pending_schema` routing

SM15 defines routing for non-authorized decision records:

- **Repair**: issues that can be fixed by correcting metadata, adding missing owner slots, or clarifying routing.
- **Quarantine**: issues that require isolation pending further review, such as potential donor leakage or unclear provenance.
- **Deferred-gap**: issues tracked in a deferred gap ledger for later resolution when capacity or clarity improves.
- **`pending_schema`**: issues where schema-family grammar is insufficient or conflicting and must be resolved before authorization can proceed.

Routing decisions are document-only. They do not execute repair, quarantine, or schema changes. They only record where future work should route.

## 30. Packet scope and C-family pressure decision limits

SM15 preserves the SM05-SM14 pressure set:

- C01 creature/NPC
- C02 item/gear
- C03 ability/power/technique
- C10 table/oracle
- conditional C14 source-local setting/cosmology only if legal/IP/source-local routing is ready

C05, C06, C07, C08, C11, C12, and C13 remain deferred unless selected by later owner-controlled authorization for a specific pressure test. C04 and C09 may also remain deferred unless needed to disambiguate C01/C02/C03/C10 pressure.

The normally tiny packet count of 3-5 packet candidates is preserved unless a later authorization narrows further. SM15 must not expand beyond authorization.

## 31. Evidence/provenance pointer decision review

SM15 requires that a decision record documents evidence/provenance pointer posture. This includes confirming that page/range truth slots, source hash or hash-later policy slots, evidence reference slots, and construct inventory slots exist without containing donor content.

Evidence/provenance pointers are metadata-only. They are not donor content, not legal/IP clearance, not source clearance, and not conversion evidence.

## 32. Lawful outcome and mapping ledger decision review

SM15 requires that a decision record documents lawful outcome route and mapping ledger route. This includes confirming that lawful outcome ledger slots and mapping ledger slots exist without containing donor content.

Lawful outcome and mapping ledger routes are metadata-only. They are not donor content, not legal/IP clearance, not source clearance, and not conversion evidence.

## 33. Rejected-import, source-local, legal/IP, and `pending_schema` decision review

SM15 requires that a decision record documents rejected-import route, source-local retention route, legal/IP route, and `pending_schema` route. This includes confirming that these routing slots exist without containing donor content.

Rejected-import, source-local, legal/IP, and `pending_schema` routes are metadata-only. They are not donor content, not legal/IP clearance, not source clearance, and not conversion evidence.

## 34. Confidence, review-routing, repair, quarantine, and failure-report decision review

SM15 requires that a decision record documents confidence/review-routing notes, repair route, quarantine route, and failure-report route. This includes confirming that these routing slots exist without containing donor content.

Confidence, review-routing, repair, quarantine, and failure-report routes are metadata-only. They are not donor content, not legal/IP clearance, not source clearance, and not conversion evidence.

## 35. Donor leakage hard-fail decision rule

SM15 requires a donor leakage hard-fail decision rule. Any detected donor leakage (real donor excerpt, donor statblock, donor table, donor map, donor setting prose, donor proper noun import as Astra default, or converted donor content) triggers hard-fail routing to repair, quarantine, rejected import, legal/IP review, or source-local retention.

Donor leakage hard-fail is a safety control, not legal/IP clearance. It routes failures but does not clear legal/IP questions.

## 36. Decision workflow

SM15 defines a decision workflow:

1. Confirm SM00-SM14 are present and current.
2. Confirm a metadata-only packet shell exists and passed SM14 shell validation.
3. Confirm no real donor content is embedded in the PR.
4. Confirm the decision record is metadata-only.
5. Confirm no execution is performed by the decision record.
6. Confirm legal/IP owner exists.
7. Confirm future review or execution-proposal owner exists.
8. Confirm metadata is not treated as legal/IP clearance.
9. Confirm external-reference readiness is not treated as source clearance.
10. Confirm SM02 no-waiver posture.
11. Confirm SM03 dry-run posture.
12. Confirm SM04 rubric and handoff posture.
13. Confirm SM05 authorization/preflight posture.
14. Confirm SM06 output-capture posture.
15. Confirm SM07 scaffold/review-harness posture.
16. Confirm SM08 no-donor safety posture.
17. Confirm SM09 dry template reference.
18. Confirm SM10 reviewer validation posture.
19. Confirm SM11 preparation-control posture.
20. Confirm SM12 external-reference review posture.
21. Confirm SM13 metadata-only assembly posture.
22. Confirm SM14 shell-validation posture.
23. Confirm C-family scope remains bounded.
24. Confirm lawful outcome, mapping, rejected-import, source-local, legal/IP, `pending_schema`, confidence, review-routing, repair, quarantine, and failure-report decision posture.
25. Confirm donor leakage hard-fail result.
26. Assign document-local authorization decision label.
27. Record decision rationale.
28. Route failures to repair, quarantine, deferred gap ledger, `pending_schema`, legal/IP review, source-local retention, rejected import, or appropriate future owner.
29. State exactly what the authorization decision record may and may not prove.
30. If the decision is "ready for execution proposal review," state that a separate execution proposal PR is still required before anything can run.

## 37. Decision record validation expectations

SM15 defines decision record validation expectations as prose requirements only. They must not create final schema fields, runtime/backend/database contracts, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, or registry values.

Validation expectations include confirming that all required contents from section 25 are present, all SM00-SM14 dependencies are documented, all routing slots are explicit, all non-execution statements are present, and all boundary statements are explicit.

These are validation expectations only. They must not create final schema fields, JSON Schema, Pydantic models, database fields, runtime contracts, final validators, or implementation contracts.

## 38. What SM15 decision controls may and may not prove

SM15 may prove:

- the project has controls for documenting a future authorization decision record;
- a future validated metadata-only shell can be routed to decision outcomes;
- blocking, repair, quarantine, legal/IP, source-local, rejected-import, and `pending_schema` routes can be recorded;
- a later execution proposal review may be conditionally allowed if a future decision record permits it.

SM15 may not prove:

- execution approval;
- conversion approval;
- legal/IP clearance;
- source clearance;
- conversion execution readiness;
- conversion success;
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

## 39. Large-scale conversion non-readiness boundary

SM15 explicitly states that large-scale corpus conversion is not ready. SM15 does not authorize broad conversion. SM15 does not create benchmark corpora, does not create evaluation corpora, does not create training data, does not create fine-tuning data, or does not create model behavior policy. SM15 does not prove conversion success or conversion execution readiness.

Large-scale conversion requires separate owner-controlled authorization after all SM00-SM15 gates pass and after a separate execution proposal PR is accepted.

## 40. Runtime/canon/sourcebook/live-play/training non-readiness boundary

SM15 explicitly states that runtime, canon, sourcebook, live-play, and training readiness are not achieved. SM15 does not create final schemas, executable JSON Schema, Pydantic models, final validators, runtime/backend/database schemas, runtime/backend/database contracts, entity/component/event schemas, command lifecycle contracts, context packet contracts, save-state shapes, final mechanics, exact math, canon, sourcebook prose, live-play behavior, accepted lexicon, or registry promotion.

Runtime/canon/sourcebook/live-play/training readiness requires separate owner-controlled authorization after all SM00-SM15 gates pass and after separate execution, canon, sourcebook, live-play, and training PRs are accepted.

## 41. Owner map and lawful fallbacks

SM15 defines an owner map for decision record routing:

- **Decision owner**: owns the decision record and ensures all SM00-SM14 dependencies are documented.
- **Legal/IP owner**: owns legal/IP disposition and source-clearance boundary.
- **Future execution proposal owner**: owns any future execution proposal PR if authorization is granted.
- **Review owner**: owns future review routing if authorization is blocked or deferred.
- **Schema owner**: owns C-family pressure boundaries and `pending_schema` routing.
- **No-donor safety owner**: owns donor leakage hard-fail routing and no-donor sentinel checks.

Lawful fallbacks route to the appropriate owner when a decision record cannot proceed. Blocked decisions route to repair, quarantine, deferred gap ledger, `pending_schema`, legal/IP review, source-local retention, rejected import, or the appropriate future owner.

## 42. Risk register

SM15 tracks risks:

- **Risk: treating decision record as execution approval**. Mitigation: explicit non-execution statements, document-local labels only, separate execution proposal PR requirement.
- **Risk: treating no-donor sentinel checks as legal/IP clearance**. Mitigation: explicit legal/IP owner slot, explicit source-clearance boundary, explicit no-donor/legal-IP distinction.
- **Risk: treating external-reference readiness as source clearance**. Mitigation: explicit source-clearance boundary, explicit external-reference/source distinction.
- **Risk: treating metadata as donor content or conversion evidence**. Mitigation: explicit metadata-only statements, no-donor hard-fail rule, donor leakage sentinel checks.
- **Risk: scope expansion beyond C01/C02/C03/C10/conditional C14**. Mitigation: explicit C-family pressure boundaries, explicit deferral of C04/C05/C06/C07/C08/C09/C11/C12/C13.
- **Risk: SM02 gate waiver**. Mitigation: explicit SM02 no-waiver requirement, blocking label for missing SM02 posture.
- **Risk: SM05 bypass**. Mitigation: explicit SM05 authorization/preflight requirement, blocking label for missing SM05 posture.
- **Risk: D00-D19 authority creep**. Mitigation: explicit D-series draft-only status, explicit authority boundary statements.
- **Risk: RHBF hidden law**. Mitigation: explicit RHBF prohibition, explicit lawful fallback routing.

## 43. Recommended next PR after SM15

Primary recommendation if decision-record controls pass:

**SM16 controlled pilot execution proposal controls**

This should define what a separate execution proposal PR must contain before any actual pilot execution may occur. It must still not run conversion unless the proposal is later accepted and all gates pass.

Alternative if SM15 exposes gaps:

**SM16 authorization decision repair and owner-calibration controls**

SM15 must not recommend jumping directly to actual donor conversion, broad conversion, final mechanics, runtime schemas, canon consolidation, sourcebook prose, live-play adapter behavior, training corpus creation, or real donor-content ingestion.

## 44. Acceptance criteria

SM15 passes if:

- SM15 file exists and is nonempty.
- All required section headings are present and in order.
- SM15 names SM00-SM14, C00-C14, Batch C capstone, B11, Conversion IR, lawful outcome taxonomy, conversion intake, extraction readiness, donor family routing, evaluation/benchmark, runtime, and Gate B.
- SM15 states it is an actual pilot authorization decision record control file only.
- SM15 states it does not itself create an actual completed authorization decision for a real donor packet because no owner-approved metadata-only packet shell exists yet.
- SM15 states it does not run conversion.
- SM15 states it does not execute a pilot.
- SM15 states it does not create actual converted donor content or pilot outputs.
- SM15 refuses real donor excerpts, donor statblocks, donor tables, donor maps, donor setting prose, donor proper noun import as Astra defaults, benchmark corpora, evaluation corpora, training data, fine-tuning data, model behavior policy, final schemas, JSON Schema, Pydantic models, final validators, runtime/backend/database contracts, final mechanics, canon/sourcebook/live-play/training content, registry promotion, C00-C14 rewrite, C15 creation, D-series authority, RHBF hidden law, SM02 waiver, SM05 bypass, treating decision records as execution approval, treating no-donor sentinel checks as legal/IP clearance, treating external-reference readiness as source clearance, and treating metadata as donor content or conversion evidence.
- SM15 distinguishes dry template, dry validation gate, preparation controls, external-reference review gate, metadata-only assembly controls, shell validation, decision-record controls, future actual decision record, and future execution PR.
- SM15 includes decision eligibility requirements.
- SM15 includes decision record required contents.
- SM15 includes decision outcome labels and states they are not registry values.
- SM15 includes authorization-granted boundary and states ready-for-execution-proposal-review is not execution approval, conversion approval, legal/IP clearance, source clearance, pilot evidence, output creation, or broad conversion authorization.
- SM15 preserves the C01/C02/C03/C10/conditional C14 pressure set.
- SM15 lists deferred families C05, C06, C07, C08, C11, C12, C13, with C04 and C09 also deferrable unless needed for disambiguation.
- SM15 includes decision workflow steps.
- SM15 states what decision controls may and may not prove.
- SM15 includes large-scale conversion non-readiness boundary.
- SM15 includes runtime/canon/sourcebook/live-play/training non-readiness boundary.
- SM15 includes owner routing and lawful fallbacks.
- SM15 includes a risk register.
- SM15 recommends SM16 controlled pilot execution proposal controls or SM16 authorization decision repair/owner-calibration controls without jumping directly to actual donor conversion, broad conversion, final mechanics, runtime schemas, canon consolidation, sourcebook prose, live-play behavior, training corpus creation, or real donor-content ingestion.
- SM15 does not contain obvious implementation artifacts such as JSON Schema object definitions, Pydantic class definitions, database table definitions, command lifecycle contracts, context packet contracts, save-state shapes, converted donor content, donor statblocks, donor tables, donor maps, or donor prose excerpts.
- Tests verify the existing SM09 dry authorization packet template fixture remains Markdown, direct child of the scaffold directory, placeholder/synthetic/non-donor, and no-donor safe under the SM08 sentinel posture.
- Registry records for C00-C14 are not promoted to forbidden states by this PR.

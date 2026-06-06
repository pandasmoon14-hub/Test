# RT-011 Validation / Readiness Tooling Owner Specification

Date prepared: 2026-06-06
Status: Stage 2 owner specification only; non-executable planning
Tracking ID: REMEDIATION-STAGE2-RT011-VALIDATION-READINESS-OWNER-SPEC-001
Stage 2 PR ID: STAGE2-PR-B
Remediation track: RT-011-validation-readiness-tooling
Owner: Astra Doctrine Council / future validation readiness tooling owner

## 1. Purpose and status

This file is the Stage 2 owner specification for RT-011 validation/readiness tooling. It upgrades `docs/doctrine/control/RT011_validation_readiness_tooling_owner_scaffold.md` from owner scaffold into specification-level planning for validation/readiness governance, reviewer decision requirements, readiness classification, non-implementation guardrail checking, registry/file tracking expectations, and dependency handoffs.

This artifact remains non-executable and non-implementation. It does not create validators, schemas, runtime code, command IR, database tables, persistence writers, retrieval indexes, context-packet compilers, live-play prompts, training data, donor-content audits, sourcebook inclusion, pilot conversion authorization, or canon promotion.

This specification resolves the Stage 2 review's RT-011 cleanup note by explicitly linking RT-011 owner-spec planning to the accepted audit and remediation lineage:

- AUDIT-001: `docs/doctrine/control/runtime_boundary_generator_ownership_audit_protocol.md`.
- AUDIT-WAVE1-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave1.md`.
- AUDIT-WAVE2-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_audit_wave2.md`.
- REMEDIATION-PRIORITY-LEDGER-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_remediation_priority_ledger.md`.
- REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001: `docs/doctrine/reviews/runtime_boundary_generator_ownership_scaffold_completion_review_and_stage2_plan.md`.

This specification also uses the existing Stage 2 RT-001 owner specification at `docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md`, the RT-001 through RT-012 scaffolds, the schema/math/readiness planning files `SM00`, `SM01`, and `SM02`, the doctrine roadmap, the doctrine registry, the current decisions log, and the backend-first/model-interchangeability posture in `README.md` as planning sources. All requested SM source files were present at drafting time; no missing-file substitution was required.

## 2. Scope

RT-011 owns validation/readiness governance at the planning and future-requirements layer. In this Stage 2 owner specification, RT-011 owns:

- validation/readiness ownership boundaries across doctrine, scaffold, owner-specification, schema, validator, runtime, live-play, canon, and sourcebook claims;
- the distinction between prose readiness, owner-spec readiness, schema readiness, executable validation, runtime readiness, and live-play readiness;
- a future validator requirement inventory, explicitly marked as semantic requirements only and not implemented validators;
- registry tracking requirements for owner-spec artifacts, readiness labels, non-implementation guardrails, and dependency handoffs;
- file-presence and artifact-linkage check requirements for required doctrine, review, registry, and decision-log artifacts;
- non-implementation guardrail check requirements to prevent prose artifacts from being cited as runtime, schema, validator, generator, persistence, retrieval, context-packet, live-play, training, donor-audit, sourcebook, pilot-conversion, or canon authority;
- owner-boundary check requirements that keep RT-001 through RT-012 ownership seams explicit;
- lifecycle, field, and status coverage check requirements for future validators without defining final fields, schema shapes, database models, or executable tests;
- reviewer decision record requirements, including explicit decisions, skipped-dependency disclosure, missing-file disclosure, blocked/deferred status routing, and separate implementation authorization;
- a controlled readiness classification vocabulary for planning labels;
- blocked and deferred status routing requirements so dependency gaps are not hidden as pass/fail results;
- auditability requirements for file lineage, registry tracking, decision logs, reviewer decisions, and guardrail deviations;
- dependency handoffs to RT-001 through RT-012;
- validation escalation triggers when readiness claims exceed authorized planning scope.

RT-011 does not own final mechanics, exact math, command lifecycle implementation, hidden-information runtime, sourcebook promotion, canon promotion, donor-content audit results, model training decisions, or live-play enablement. RT-011 may require that such claims be tracked, blocked, or escalated until their owning tracks and reviewers authorize them separately.

## 3. Must-not-own boundaries

RT-011 must not own or claim to complete:

- executable validator implementation;
- runtime code;
- schema implementation;
- command IR implementation;
- database schema;
- persistence writer implementation;
- retrieval index implementation;
- context-packet compiler implementation;
- RNG/dice/table implementation;
- event ledger implementation;
- generator implementation;
- live-play prompts;
- training data;
- donor-content audits;
- canon promotion;
- pilot conversion authorization by prose alone;
- sourcebook inclusion authorization;
- automated reviewer replacement.

Any artifact or review that cites this owner specification as completing one of those items must be blocked, corrected, and recorded as a guardrail deviation before advancement.

## 4. Prose readiness versus executable validation

RT-011 enforces a strict separation between reviewable planning prose and executable validation:

- `prose_readiness` means doctrine, review, scaffold, or specification text exists and can be reviewed by humans.
- `owner_spec_readiness` means an owner specification defines boundaries, future requirements, handoffs, and non-implementation guardrails for a track.
- `schema_readiness` requires separately authorized schema artifacts and cannot be inferred from prose, scaffolds, owner specs, registry notes, or LLM summaries.
- `executable_validation` requires separately authorized validator implementation with defined inputs, outputs, failure modes, execution evidence, and review routing.
- `runtime_readiness` requires separately authorized runtime code plus backend-owned state, event, persistence, validation, replay, and context systems where applicable.
- `live_play_readiness` requires separately authorized runtime and adapter work and cannot be granted by doctrine/readiness prose alone.
- no prose file may claim executable validation by itself.

A future validator may cite prose as a requirement source only after a separate implementation authorization decision. Prose cannot substitute for executed tests, validator outputs, backend state transitions, reviewer approval, or implementation records.

## 5. Readiness classification contract

The following controlled vocabulary is available for planning-level readiness labels. These labels are not executable gates, not final schema statuses, not runtime permissions, not CI outcomes, and not reviewer approvals.

| Label | Planning meaning | Guardrail |
|---|---|---|
| `doctrine_only` | Doctrine or review prose exists and is reviewable. | Does not authorize schema, validator, runtime, live-play, training, sourcebook, pilot conversion, or canon use. |
| `scaffold_ready` | An owner scaffold exists and records baseline scope and guardrails. | Does not equal owner-spec readiness or implementation readiness. |
| `owner_spec_ready` | An owner specification exists and defines future requirements and boundaries. | Does not implement or authorize validators, schemas, runtime, generators, persistence, retrieval, context packets, or live play. |
| `schema_required` | A separate schema artifact is needed before implementation or validation claims can advance. | Cannot be satisfied by prose or an LLM assertion. |
| `validator_required` | A separate executable validator is needed before a validation claim can advance. | Cannot be satisfied by a checklist or owner spec. |
| `runtime_required` | Backend runtime code/state/event/persistence authority is needed. | Cannot be satisfied by schema, docs, or narration. |
| `generator_required` | Separately authorized generator ownership or implementation is needed. | Cannot be satisfied by generated prose or durable-record assertions. |
| `context_packet_required` | Separately authorized context-packet partitioning/compilation is needed. | Cannot be satisfied by prompt text or LLM summaries. |
| `persistence_required` | Separately authorized durable state/event/file writer or database persistence is needed. | Cannot be satisfied by Markdown/YAML/JSON planning artifacts. |
| `blocked_pending_dependency` | Advancement is blocked by an absent upstream/downstream owner, artifact, or implementation. | Must be routed as dependency-blocked, not pass/fail. |
| `blocked_pending_review` | Advancement is blocked until reviewer decision occurs. | Model confidence cannot clear the block. |
| `deferred_to_runtime_phase` | The requirement belongs to a later runtime implementation phase. | Must not be implemented in owner-spec PRs. |
| `deferred_to_canon_or_sourcebook_phase` | The requirement belongs to later canon or sourcebook review. | Must not authorize promotion, sourcebook inclusion, or training. |
| `implementation_authorized_separately_only` | Implementation can occur only after an explicit separate authorization record. | The owner spec is insufficient authorization by itself. |

Future registry or decision-log entries may cite these labels for planning, but must not invent new executable status semantics from them without a separately reviewed schema/status contract.

## 6. Conceptual validation layers

The following conceptual validation layers are placeholders only. They are not executable validators, not final test implementation, not CI implementation, not schema, not runtime gates, and not approval automation. Every layer has implementation status `future_required_not_implemented`.

| Conceptual layer | Purpose | Backend/reviewer owner | LLM allowed interaction | Downstream handoff | Implementation status |
|---|---|---|---|---|---|
| `artifact_presence_check` | Verify required files or disclosed absences are tracked before review claims advance. | Future validation readiness tooling owner plus reviewer. | May summarize located files when paths are provided; may not invent missing files. | Registry and reviewer decision record. | `future_required_not_implemented` |
| `registry_tracking_check` | Verify registry entries reference the correct artifact, ID, status, guardrails, and dependencies. | Registry maintainer and reviewer. | May draft proposed registry text for review; may not assert tracking exists unless present. | `docs/doctrine/astra_doctrine_registry_v0_1.yaml`. | `future_required_not_implemented` |
| `decision_log_tracking_check` | Verify reviewer or governance decisions are logged and aligned with artifact scope. | Decision-log maintainer and reviewer. | May draft proposed decision-log prose; may not replace approval. | `docs/decisions/current_decisions_log.md`. | `future_required_not_implemented` |
| `audit_source_linkage_check` | Verify AUDIT-001, AUDIT-WAVE1-001, AUDIT-WAVE2-001, the remediation ledger, and Stage 2 plan linkage is explicit. | Runtime boundary reviewers. | May cross-reference existing source paths. | Audit/remediation review lineage. | `future_required_not_implemented` |
| `owner_boundary_check` | Verify each claim routes to the correct RT owner and does not collapse neighboring tracks. | Responsible RT owner and reviewer. | May flag apparent seam conflicts for review. | RT-001 through RT-012 owner artifacts. | `future_required_not_implemented` |
| `non_implementation_guardrail_check` | Verify owner specs are not cited as implementations, runtime gates, schemas, validators, generators, persistence, retrieval, context packets, live-play, training, donor audits, or canon/sourcebook authority. | Backend/reviewer governance owner. | May identify prohibited phrases; may not waive deviations. | Reviewer decision and blocked-status routing. | `future_required_not_implemented` |
| `llm_non_authority_check` | Verify LLM outputs do not claim authority over readiness, schema, validator, runtime, pilot conversion, live play, training, sourcebook, or canon decisions. | Reviewer and future validation tooling owner. | May self-label outputs as non-authoritative proposals. | Reviewer decision record and adapter/runtime policy owners. | `future_required_not_implemented` |
| `dependency_handoff_check` | Verify upstream and downstream dependency handoffs are present and unresolved dependencies are disclosed. | Responsible RT owner and reviewer. | May list dependencies from actual files. | RT owner specs and blocked routing. | `future_required_not_implemented` |
| `readiness_classification_check` | Verify readiness labels use the controlled vocabulary and remain planning labels only. | Validation readiness owner and reviewer. | May propose labels for review. | Registry, readiness reports, reviewer decisions. | `future_required_not_implemented` |
| `future_required_output_inventory_check` | Verify future artifact families are inventoried as requirements without becoming implementation. | Validation readiness owner. | May draft inventories as prose. | Future schema/validator/runtime authorization decisions. | `future_required_not_implemented` |
| `reviewer_decision_record_check` | Verify decisions, skips, missing-file substitutions, blocks, and authorizations are explicit. | Reviewer and governance record owner. | May prepare a non-authoritative draft. | Decision log or future reviewer-decision system. | `future_required_not_implemented` |
| `blocked_status_routing_check` | Verify dependency gaps and review gaps route to blocked/deferred labels rather than false pass/fail claims. | Reviewer and future validation tooling owner. | May identify likely blocked conditions. | Readiness reports and owner handoffs. | `future_required_not_implemented` |
| `implementation_authorization_check` | Verify schema, validator, runtime, generator, persistence, retrieval, context-packet, live-play, training, sourcebook, pilot-conversion, donor-audit, and canon work has separate authorization before starting. | Backend/reviewer governance owner. | May not authorize implementation. | Future implementation PRs and decision records. | `future_required_not_implemented` |

## 7. Reviewer decision record contract

Future reviewer decision records must remain explicit, auditable, and separate from model assertions. This specification does not create a database schema, final decision-record schema, Pydantic model, table, event model, or approval automation.

Future reviewer decision requirements:

- reviewer decision records must be explicit and attributable to authorized reviewers or governance bodies;
- model confidence, LLM fluency, or generated summaries cannot replace reviewer approval;
- skipped dependencies must be recorded;
- dependency-related skips must be distinguished from pass/fail results;
- missing-file substitutions must be disclosed with actual substitute paths and reason for use;
- guardrail deviations must block advancement until reviewed and corrected;
- implementation authorization must require a separate decision;
- canon authorization must require a separate decision;
- sourcebook inclusion authorization must require a separate decision;
- training authorization must require a separate decision;
- live-play authorization must require a separate decision;
- pilot conversion authorization must require a separate decision;
- donor-content audit authorization and results must require separate audit ownership.

Decision records should preserve enough lineage to answer which files were reviewed, which dependencies were present or absent, which readiness label was applied, why any dependency was skipped or deferred, and whether implementation was explicitly authorized. Those are semantic requirements only, not a final schema.

## 8. Validation and readiness handoffs

RT-011 provides validation/readiness governance handoffs to every runtime-boundary track without taking over their domain authority:

- RT-001: command lifecycle, action legality, cost-commitment timing, command/event boundary, rejection/quarantine, context/narration handoff, and command validator requirement readiness.
- RT-002: resource, cost, consequence, backlash, strain, corruption, reward/loss, recovery cost, refund, and math readiness.
- RT-003: combat, hazard, damage, injury, recovery, active-threat, tactical/encounter state, and resolution readiness.
- RT-004: ability, effect, skill, capability, prerequisite, cooldown, binding, and ability/effect validation readiness.
- RT-005: hidden information, visible/redacted/derived partitions, context-packet projection, narrator-facing packet constraints, and hidden-truth readiness.
- RT-006: mission, reward, clue, scenario progress, objective status, hidden-truth exposure, and mission/reward/clue readiness.
- RT-007: social, faction, relationship, actor knowledge, standing, obligation, institutional state, and knowledge-state readiness.
- RT-008: generated-content provenance, recurrence, durable-record eligibility, stable identifier, generated-record status, and generator-boundary readiness.
- RT-009: RNG, dice, table, oracle, seed, replay, hidden random result, table outcome commitment, and random-dependency readiness.
- RT-010: inventory, item, gear, vehicle, platform, asset, custody, loadout, charge, durability, cargo, crew, movement, repair, and persistent asset readiness.
- RT-011: validation/readiness classification, registry/file tracking, non-implementation guardrails, reviewer decision records, blocked/deferred routing, and future validator requirement readiness.
- RT-012: D-series/native-design promotion boundary, source-pack pressure, sourcebook/canon/training/live-play separation, and native-design promotion readiness.

Unresolved handoffs must be labeled `blocked_pending_dependency`, `blocked_pending_review`, `deferred_to_runtime_phase`, `deferred_to_canon_or_sourcebook_phase`, or `implementation_authorized_separately_only` as applicable rather than being hidden behind a pass/fail claim.

## 9. LLM non-authority rules

The LLM is explicitly prohibited from:

- declaring a file executable-ready;
- declaring runtime readiness;
- declaring schema readiness;
- declaring validator readiness;
- approving pilot conversion outputs;
- authorizing live play;
- authorizing training data;
- authorizing canon promotion;
- authorizing sourcebook inclusion;
- replacing reviewer decisions;
- treating prose as executable validation;
- treating tests as passed without actual execution and reporting;
- hiding dependency-related skips;
- inventing missing registry tracking;
- inventing missing decision-log tracking;
- bypassing backend/reviewer validation;
- waiving non-implementation guardrails;
- treating model confidence as approval evidence.

The LLM may help draft non-authoritative planning prose, summarize visible reviewed artifacts, identify apparent gaps for reviewer attention, and propose controlled readiness labels. Those interactions are advisory only and remain subject to backend/reviewer validation.

## 10. Future validation artifact inventory

The following future validation artifact families are semantic requirements only. They are not implemented validators, not final field definitions, not JSON schema, not database schema, not Pydantic models, not CI jobs, not pytest implementation, and not validator code. Every listed family has implementation status `future_required_not_implemented`.

| Future artifact family | Purpose | Owner | LLM allowed interaction | Downstream handoff | Implementation status |
|---|---|---|---|---|---|
| `ArtifactPresenceCheck` | Confirm required source, registry, decision, and owner artifacts are present or absent with disclosure. | Future validation readiness tooling owner and reviewer. | May draft source inventories from actual paths. | Registry and reviewer decision record. | `future_required_not_implemented` |
| `RegistryTrackingCheck` | Confirm artifact IDs, paths, status, dependencies, refusals, and guardrails are tracked. | Registry maintainer and reviewer. | May propose registry updates. | Doctrine registry. | `future_required_not_implemented` |
| `DecisionLogTrackingCheck` | Confirm governance decisions exist for the artifact and match its scope. | Decision-log maintainer and reviewer. | May draft decision-log text. | Current decisions log or future decision system. | `future_required_not_implemented` |
| `AuditSourceLinkageCheck` | Confirm audit lineage references are explicit and current for the reviewed scope. | Runtime boundary reviewers. | May list actual audit sources. | Audit/remediation lineage. | `future_required_not_implemented` |
| `OwnerBoundaryCheck` | Confirm claims route to the correct RT owner and do not collapse ownership seams. | Responsible RT owner and reviewer. | May identify candidate seam conflicts. | RT-001 through RT-012 owner specs/scaffolds. | `future_required_not_implemented` |
| `NonImplementationGuardrailCheck` | Confirm planning artifacts do not claim forbidden implementation, runtime, schema, validator, live-play, sourcebook, training, donor-audit, or canon outcomes. | Backend/reviewer governance owner. | May flag prohibited claims. | Blocked/deviation record and reviewer decision. | `future_required_not_implemented` |
| `LLMNonAuthorityCheck` | Confirm LLM output is not treated as reviewer approval, executable validation, runtime authority, or canon/sourcebook/training authorization. | Reviewer and future validation owner. | May self-identify advisory status. | Reviewer decisions and adapter policy. | `future_required_not_implemented` |
| `DependencyHandoffCheck` | Confirm dependencies and downstream handoffs are listed, skipped, blocked, or deferred explicitly. | Responsible RT owner and reviewer. | May summarize actual dependency lists. | RT owner artifacts and readiness reports. | `future_required_not_implemented` |
| `ReadinessClassificationCheck` | Confirm readiness labels use the controlled planning vocabulary and do not become executable status. | Validation readiness owner and reviewer. | May suggest labels for review. | Registry, readiness summaries, decision records. | `future_required_not_implemented` |
| `ReviewerDecisionRecord` | Preserve explicit reviewer decision, dependency skips, missing-file disclosures, blocked/deferred routing, and implementation authorization posture. | Reviewer/governance record owner. | May draft non-authoritative summaries. | Decision log or future reviewer-decision system. | `future_required_not_implemented` |
| `BlockedStatusRoutingRecord` | Preserve dependency or review blocks separately from pass/fail outcomes. | Reviewer and validation readiness owner. | May identify likely block reasons. | Readiness report and owner handoff. | `future_required_not_implemented` |
| `ImplementationAuthorizationRecord` | Preserve separate authorization for schema, validator, runtime, generator, persistence, retrieval, context-packet, live-play, sourcebook, training, pilot-conversion, donor-audit, or canon work. | Backend/reviewer governance owner. | May not authorize implementation. | Future implementation PR and decision record. | `future_required_not_implemented` |
| `ValidationResultSummary` | Summarize future executed validation outputs, skips, blockers, and reviewer decisions without replacing raw execution evidence. | Future validator owner and reviewer. | May summarize reported results only when actual execution evidence is supplied. | Registry, decision records, future readiness reports. | `future_required_not_implemented` |

## 11. Registry and file tracking expectations

RT-011 readiness governance requires file and registry tracking to remain aligned across planning and future implementation phases:

- every owner-specification artifact must have an actual path before it is cited as present;
- absent requested sources must be disclosed rather than silently replaced;
- substitute sources may be used only after confirming they exist and recording why they are the nearest equivalent;
- registry tracking should identify file ID, filename, proposed path, authority level, status, owner, purpose, dependencies, must-not-own boundaries, hard refusals, escalation triggers, required tests/checks, review status, promotion requirements, and non-implementation notes;
- decision-log tracking should record the governance decision and guardrails for the artifact;
- future validators must not infer registry tracking or decision-log tracking from prose unless actual registry/decision records exist;
- registry and decision-log records remain tracking/governance artifacts, not executable validators, runtime gates, schema statuses, or approval automation.

## 12. Validation escalation triggers

RT-011 must escalate for reviewer attention when any of the following occurs:

- a prose artifact is cited as executable validation;
- an owner scaffold or owner specification is cited as runtime, schema, validator, generator, persistence, retrieval, context-packet, live-play, training, donor-audit, sourcebook, pilot-conversion, or canon authority;
- an LLM output declares readiness, approval, or validation without reviewer/backend evidence;
- tests are described as passed without actual execution and reporting;
- missing files are silently substituted;
- dependency-related skips are hidden or represented as pass/fail outcomes;
- readiness labels are treated as executable gates or final schema statuses;
- implementation starts without a separate authorization decision;
- canon, sourcebook, training, live-play, pilot-conversion, or donor-audit authorization is implied by owner-spec prose.

Escalated items must be routed to reviewer decision records and blocked/deferred labels until corrected.

## 13. Non-implementation reaffirmation

This Stage 2 PR-B owner specification adds no:

- runtime code;
- schema implementation;
- command IR implementation;
- validator implementation;
- generator implementation;
- persistence writer;
- retrieval index;
- context-packet compiler;
- RNG/dice/table implementation;
- event ledger implementation;
- database schema;
- live-play prompt;
- training data;
- donor-content audit;
- canon promotion;
- sourcebook inclusion authorization;
- pilot conversion authorization.

Guardrail phrase summary: no runtime implementation, no schema implementation, no command IR implementation, no validator implementation, no generator implementation, no persistence writer implementation, no retrieval index implementation, no context-packet compiler implementation, no RNG/dice/table implementation, no event ledger implementation, no database schema, no live-play prompt implementation, no training authorization, no donor-content audit, no sourcebook inclusion authorization, no pilot conversion authorization, and no canon promotion.

## 14. Stage 2 output classification

```yaml
stage2_output:
  stage2_pr_id: STAGE2-PR-B
  track: RT-011
  artifact_type: owner_specification
  implementation_status: non_executable_planning
  authorizes_runtime_implementation: false
  authorizes_schema_implementation: false
  authorizes_validator_implementation: false
  authorizes_live_play: false
  authorizes_training: false
  authorizes_canon_promotion: false
  authorizes_pilot_conversion: false
  next_allowed_step: RT-002 owner specification or RT-005 owner specification, pending review
```

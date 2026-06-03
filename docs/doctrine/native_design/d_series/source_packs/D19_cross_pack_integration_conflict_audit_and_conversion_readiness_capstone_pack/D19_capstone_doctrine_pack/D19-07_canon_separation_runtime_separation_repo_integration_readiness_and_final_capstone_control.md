# D19-07 — Canon Separation, Runtime Separation, Repo-Integration Readiness, and Final Capstone Control

> **Status:** Phase 1 capstone doctrine. This file is a control-layer artifact for Astra Ascension doctrine integration. It is not final sourcebook prose, not a live-play GM adapter, not a runtime/backend schema, and not a donor conversion output. Any record shapes in this pack are lightweight doctrine-facing / conversion-facing / audit-facing shapes only and may be replaced or formalized later by Batch C schema doctrine, Runtime Gate B, canon consolidation, or playtest calibration.


## Core question

How does Astra determine whether D00–D18 are ready for repository integration, later canon consolidation, conversion use, schema design, runtime planning, and eventual live-play adapter training without collapsing those phases into one another?

## Phase-Separation and Readiness Gate Model

D19 uses this procedure:

```text
1. Classify each doctrine asset by phase-facing status.
2. Identify whether it is ready for repo integration.
3. Identify whether it is conversion-ready.
4. Identify whether it is canon-consolidation-ready.
5. Identify whether it is schema-ready or schema-deferred.
6. Identify whether it is runtime-facing or runtime-deferred.
7. Identify whether it is live-play-adapter-relevant or excluded.
8. Assign final readiness status.
9. Record required patches or future actions.
```

## Phase-facing classifications

### Doctrine-only

Internal architecture such as owner boundaries, anti-drift rules, lawful outcome taxonomy, handoff controls, quarantine triggers, escalation rules, record-shape warnings, and deferred work ledgers.

### Conversion-facing

Material that helps map donor constructs: donor family routing, source-local boundaries, construct splitting, lawful outcome assignment, donor mapping ladders, quarantine/escalation handling, stress-test patterns.

### Source-local

Material retained inside a bounded converted source or scenario. Source-local material is not Astra canon unless promoted later.

### Canon-candidate

Material that may deserve sourcebook review but is not yet canon.

### Sourcebook-ready

Material stable enough to be translated into player/GM-facing canon language. Criteria: Astra-native terminology, owner-file support, no unresolved donor assumption, no hidden conversion-only dependency, no runtime-only dependency, no deferred math required for comprehension, and compatibility with phase separation.

### Schema-facing

Record shapes or structural controls that future Batch C or runtime data design should consult. Schema-facing does not mean final schema.

### Runtime-facing, not implementation

Doctrine that identifies future runtime needs: capture, retrieval triggers, hidden-state boundaries, salience filtering, context-packet candidacy, event logging needs, save-state ownership, over-surfacing/under-surfacing risks.

### Live-play-adapter-facing

Material that may later inform the GM/play model. It must not be used as live-play behavior until Phase 4.

## Readiness gates

### Gate 1 — Repo-integration readiness

Asks whether files are structurally complete, filenames stable, manifests present, owner boundaries clear, not-final-schema warnings present, source-local/quarantine/escalation controls present, dependencies clear, and deferred items logged.

Statuses:

```text
ready_for_repo_integration
ready_with_minor_clarifications
requires_cross_pack_patch
requires_manifest_patch
requires_record_registry_patch
requires_source_local_patch
not_ready
```

### Gate 2 — Conversion-readiness

Asks whether donor constructs route through D00–D18, mixed constructs split, source-local systems remain bounded, quarantine/escalation are available, deferred gaps can be identified without invention, assumptions can be rejected, and conversion can proceed without canon promotion.

Statuses:

```text
conversion_ready
conversion_ready_with_quarantine
conversion_ready_with_escalation_watch
requires_more_stress_tests
requires_owner_patch
requires_conversion_IR_update
not_conversion_ready
```

### Gate 3 — Canon-consolidation readiness

Asks what can become sourcebook language, what remains scaffolding, what is conversion-only, what is source-local, what is canon-candidate, and what requires playtest or math calibration.

Statuses:

```text
canon_consolidation_ready_later
canon_candidate_only
requires_playtest_first
requires_math_calibration_first
requires_schema_first
doctrine_only_not_sourcebook_ready
not_canon_ready
```

For D00–D19 as a whole, the expected status is `canon_consolidation_ready_later`, not immediate sourcebook-ready.

### Gate 4 — Schema/runtime readiness

Asks which record shapes inform future schemas, which are duplicates or companion records, which fields are doctrine-only, which runtime handoff notes exist, and which implementation questions remain deferred.

Statuses:

```text
schema_handoff_ready
schema_handoff_ready_with_registry
requires_batch_C_schema_design
requires_runtime_Gate_B_design
not_schema_ready
```

### Gate 5 — Live-play adapter readiness

Asks whether the doctrine can train final GM behavior yet, guide live play safely, includes enough examples, distinguishes hidden state, and has canon sourcebook material available.

Statuses:

```text
not_live_play_ready
adapter_planning_ready
example_pack_needed
canonical_sourcebook_needed
runtime_state_needed
Phase_4_ready_later
```

For D00–D19, the expected status is `adapter_planning_ready`, not live-play ready.

## Phase-separation anti-drift rules

```text
Do not treat doctrine as sourcebook prose.
Do not treat source-local material as canon.
Do not treat canon candidates as canon.
Do not treat record shapes as schemas.
Do not treat runtime-facing notes as implementation.
Do not treat D11 as final GM behavior.
Do not treat stress tests as donor conversions.
Do not treat deferred math as permission to invent.
Do not move to live-play adapter training before canon/sourcebook and examples exist.
Do not let repo integration silently change doctrine authority.
```

## Final capstone checklist

D19 should end by confirming:

```text
Owner-boundary audit complete.
Handoff matrix complete.
Record-shape registry complete.
Deferred work ledger complete.
Lawful outcome audit complete.
Mixed donor-routing stress-test procedure complete.
Canon/runtime/live-play separation complete.
Repo-integration readiness checked.
Conversion-readiness checked.
Canon-consolidation readiness checked.
Schema/runtime handoff readiness checked.
Phase 4 live-play adapter boundary preserved.
No new ordinary doctrine domain created accidentally.
No deferred math/schema/runtime work solved prematurely.
```

## Acceptance criteria

D19-07 is accepted if it classifies assets by phase-facing status, defines readiness gates for repo/conversion/canon/schema/runtime/live-play planning, includes final readiness and DDR controls, and forbids phase collapse.

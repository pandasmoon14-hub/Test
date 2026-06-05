# Runtime Boundary + Generator Ownership Audit Protocol

Date prepared: 2026-06-05
Status: audit-preparation protocol only
Owner: Astra Doctrine Council / Runtime Boundary Reviewers

## 1. Purpose

This protocol prepares the future Runtime Boundary + Generator Ownership Audit. It defines the scope, classifications, source inputs, output schema, review workflow, and exclusions reviewers must use when a later PR performs the audit.

The audit evaluates whether each subsystem can eventually be executed by backend code without relying on the LLM to improvise missing mechanics, state, validation, memory, persistence, generators, or consequences.

This preparation file does not classify any subsystem, rewrite doctrine, promote records, implement runtime code, create generators, create validators, create persistence writers, or authorize live-play/training.

## 2. Controlling invariant

The future audit must preserve the backend-first model-interchangeability invariant:

- Astra may use interchangeable local or cloud LLMs, but no subsystem may depend on a particular model as the holder of truth.
- The backend owns authoritative truth, rules execution, dice/RNG, validation, state deltas, event commits, memory records, retrieval indexes, generated-content durability, persistence, and consequences.
- The LLM may narrate, summarize, interpret intent, ask clarifying questions, and propose constrained drafts only inside backend-provided contracts.
- Player-facing narration must be derived from committed backend outcomes and context packets, except when explicitly labeled as proposal, clarification, or non-authoritative flavor.

## 3. Audit scope

The later audit must cover these repo source areas using actual paths that exist at audit time:

| Scope area | Current path convention | Audit inclusion rule |
| --- | --- | --- |
| Batch A doctrine | `docs/doctrine/setting/`, `docs/doctrine/advancement/`, `docs/doctrine/world/` | Include A01-A15 doctrine files and the A00/PREA01 control boundaries only when they constrain Batch A runtime ownership. |
| Batch B operational doctrine | `docs/doctrine/operations/batch_b/` | Include B01-B11 operational procedure files. |
| Batch C schema-family files | `docs/doctrine/schema/` | Include C00-C14 schema-family files. |
| D00-D19 native-design source-pack material | `docs/doctrine/native_design/d_series/source_packs/` and related D-series manifests | Include D00-D19 draft source-pack/source material where present; treat D-series material as draft source material, not current runtime authority. |
| schema/math/mechanics workstream files | `docs/doctrine/schema_math_mechanics/` | Include SM00 and later SM workstream control/readiness files. |
| roadmap/control files | `README.md`, `docs/doctrine/astra_doctrine_roadmap_v0_1.md`, `docs/doctrine/astra_doctrine_registry_v0_1.yaml`, `docs/doctrine/control/`, `docs/decisions/current_decisions_log.md` | Include only the portions that define future requirements, gates, constraints, invariants, or ownership boundaries. |
| runtime/training files | `docs/doctrine/runtime/`, `docs/doctrine/training/`, or the current registry R/T owner paths if actual files exist later | Treat as planned future layers unless actual files exist at audit time; do not invent paths or file contents. |

Do not audit donor PDFs, donor books, or donor content directly. Donor-derived pressure may be considered only through existing Astra doctrine, schema, source-local records, handoff controls, or review artifacts already in the repo.

## 4. Input sources and precedence

Reviewers must read the active repo state before producing audit findings. Minimum inputs are:

1. `README.md` for project identity, backend-first invariants, and extraction/runtime separation.
2. `docs/doctrine/astra_doctrine_roadmap_v0_1.md` for future runtime, generator, persistence, memory, narration, and audit requirements.
3. `docs/doctrine/astra_doctrine_registry_v0_1.yaml` for tracking status, owner records, dependencies, gates, and lifecycle metadata.
4. `docs/decisions/current_decisions_log.md` and `docs/operations/current_decisions_log_v0_1.md` for relevant current decisions and operational constraints.
5. Existing doctrine/control/review/native-design/schema/schema-math folders under `docs/doctrine/`.
6. Existing tests that encode doctrine boundaries, registry behavior, PyYAML skip behavior, schema readiness, and workstream gate expectations.

Precedence for contradictions:

1. Direct active control files and roadmap/registry gate constraints.
2. Current decision-log entries that clarify control posture.
3. Batch A/B/C doctrine and SM workstream files.
4. D00-D19 source-pack material as draft source inputs only.
5. Tests as executable guardrails for the documented posture.

If a source conflict cannot be resolved through existing control posture, the audit must record an escalation rather than silently choose a new doctrine rule.

## 5. Allowed classification labels

Each subsystem must receive one or more of the following labels only:

```yaml
doctrine_only
schema_ready
runtime_ready
generator_ready
validator_ready
context_packet_ready
narration_only
blocked_pending_schema
blocked_pending_math
blocked_pending_runtime
```

Classification guidance:

- `doctrine_only`: the subsystem is currently descriptive/control doctrine and lacks sufficient schema/runtime execution contracts.
- `schema_ready`: existing schema-family work is sufficient to begin or validate record-shape design for the subsystem.
- `runtime_ready`: backend command/state/event ownership can be specified from existing doctrine without asking the LLM to fill missing mechanics.
- `generator_ready`: backend-owned generators/templates can be specified from existing doctrine and schema without model improvisation.
- `validator_ready`: deterministic validation rules can be specified from existing doctrine/schema/mechanics.
- `context_packet_ready`: visible/hidden context boundaries and packet inputs are sufficiently specified for backend compilation.
- `narration_only`: the subsystem should remain player-facing prose/flavor and must not mutate authoritative state by itself.
- `blocked_pending_schema`: required record shapes, fields, or schema families are missing.
- `blocked_pending_math`: required math, clocks, costs, scales, dice/RNG rules, or consequence mechanics are missing.
- `blocked_pending_runtime`: required backend command lifecycle, state/event model, persistence, memory, retrieval, or execution kernel design is missing.

## 6. Required output schema

The later audit must emit one record per reviewed subsystem using this shape:

```yaml
subsystem_id: <stable identifier>
source_area: <Batch A | Batch B | Batch C | D00-D19 | schema/math/mechanics | roadmap/control | runtime/training>
source_paths:
  - <repo-relative path>
classification:
  - <one or more allowed classification labels>
doctrine_owner: <file or pending owner>
missing_backend_pieces:
  - <piece or none>
required_schemas:
  - <schema or field family or none>
required_math_mechanics:
  - <math/mechanics requirement or none>
required_generators_templates:
  - <generator/template requirement or none>
required_command_ir:
  - <command/IR requirement or none>
required_state_event_fields:
  - <state/event field requirement or none>
required_validators:
  - <validator requirement or none>
required_context_packets:
  - <context-packet requirement or none>
required_persistence_writers:
  - <writer requirement or none>
required_tests:
  - <test requirement or none>
llm_overreach_risk: <none | low | medium | high | critical>
escalation_required: <true | false>
notes: <short rationale>
```

Stable subsystem identifiers should be derived from existing file IDs, headings, or repo naming conventions where possible, for example `A13.combat_consequence_boundary`, `B02.action_resolution_trigger`, `C03.ability_record_generator_inputs`, or `SM00.runtime_gate_dependency`. Reviewers must not invent subsystem IDs that imply implemented runtime ownership when none exists.

## 7. Review process

1. **Inventory pass**: enumerate files under the scoped repo paths and group them by Batch A, Batch B, Batch C, D00-D19, schema/math/mechanics, roadmap/control, and runtime/training.
2. **Boundary extraction pass**: capture only requirements, prohibitions, handoff rules, schemas, gates, and ownership statements relevant to backend execution or LLM overreach.
3. **Subsystem slicing pass**: identify stable subsystems small enough to classify without blending unrelated mechanics.
4. **Classification pass**: apply only the allowed labels and explain any blocked labels with missing backend/schema/math/runtime pieces.
5. **LLM overreach pass**: mark whether current doctrine would require the LLM to improvise mechanics, state, validation, memory, persistence, generators, or consequences.
6. **Generator ownership pass**: identify whether generators/templates can be backend-owned from existing inputs or must remain blocked until schema/math/runtime work lands.
7. **Validator/context/persistence pass**: identify required validators, context packets, state/event fields, and persistence writers without implementing them.
8. **Escalation pass**: route contradictions, missing owners, source-local uncertainty, donor-law creep, or unsupported runtime assumptions to follow-up work rather than resolving them in the audit.
9. **Evidence pass**: cite repo-relative source paths and relevant headings/sections for every audit record.
10. **No-implementation pass**: confirm the audit PR created no runtime code, database schema, generator, persistence writer, live-play adapter, training set, canon promotion, or donor-content audit.

## 8. Required review outputs

A future audit PR should produce:

- a Markdown audit report in `docs/doctrine/reviews/`;
- optional machine-readable audit records only if an existing schema/control convention exists or is created in that audit PR;
- test coverage that verifies allowed labels, required output fields, and no unauthorized donor/runtime implementation claims;
- a registry/changelog update if the repo convention at audit time requires tracking the report.

## 9. Non-goals for this protocol and the future audit

This protocol does not perform the audit. The later audit also must not:

- rewrite Batch A, Batch B, Batch C, SM, or D00-D19 doctrine as part of classification;
- audit donor PDFs or donor books directly;
- promote source-local or donor content into canon;
- implement backend runtime code, database schemas, event stores, file writers, generated-content records, context-packet compilers, validators, generators, live-play adapters, or training pipelines;
- define final math, dice, clocks, costs, advancement equations, consequence tables, or encounter procedure;
- treat Markdown, JSON, YAML, model memory, transcripts, or summaries as authoritative state outside backend commit pathways;
- allow the LLM to become the hidden state holder, rules engine, dice engine, validator, memory system, persistence layer, or generator owner.

## 10. Completion criteria for the later audit

The future audit is complete only when every in-scope subsystem has a record using the required output schema, every label is drawn from the allowed list, every blocked item identifies the missing owner/workstream, and every medium-or-higher LLM overreach risk has a follow-up action or escalation target.

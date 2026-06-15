# RUNTIME-DOMAIN-PR-9B: Scene Command Execution Skeleton Hardening Review

**Date:** 2026-06-15
**Reviewer:** Astra Doctrine Council / synthesis assistant
**Artifact ID:** RUNTIME-DOMAIN-PR-9B-SCENE-COMMAND-EXECUTION-HARDENING-REVIEW-001
**Follows:** RUNTIME-DOMAIN-PR-9A (scene command execution skeleton, merged as PR #305)
**Status:** review/hardening only — no new runtime behavior

---

## Purpose

PR-9B is a review/hardening gate for PR-9A. It validates, audits, and
tightens the PR-9A scene command execution skeleton before any new runtime
behavior is built on top of it. PR-9B adds no new runtime behavior.

## Scope

- Audit `scene_command_execution_skeleton.py` against all 12 audit criteria
- Add focused hardening tests
- Tighten guardrails, docstrings, validators, or exports if audit warrants
- Add registry and decision-log entries for PR-9B
- Block progression to PR-9C until this review is complete

## Audit Findings

### 1. Module breadth

`scene_command_execution_skeleton.py` is ~1304 lines containing 16 frozen
dataclasses, corresponding factories, validators, and two serializers. While
large, the module is cohesive: all types participate in the single scene
command execution assembly pipeline. No split is required.

### 2. Naming review

No names imply real execution, live-play behavior, settlement, mutation,
persistence, RNG, model authority, or narration generation. The module
name contains "execution" but is qualified with "skeleton" throughout.
The assembly function `assemble_scene_command_execution_result` produces
an immutable result without side effects.

### 3. PersistenceBoundaryRequest

`persistence_prepare_ref` is typed as `PersistenceBoundaryRequest | None`
and defaults to `None`. The field name uses "prepare" to indicate
prepare-only semantics. The assembly factory does not enforce a specific
`operation_type` — it accepts any valid `PersistenceBoundaryRequest`.
This is acceptable at the skeleton stage because the persistence boundary
kernel type itself does not perform writes; it is a request declaration.
The authority flag `persistence_writes` is explicitly `False`.

### 4. Hidden-info contract serialization

`SceneCommandExecutionHiddenInfoContract` carries `backend_only_description`.
The `to_dict()` method includes it (correct for backend serialization).
The visible serializer `serialize_scene_command_execution_assembly_result_visible`
does NOT include hidden-info contract payloads — it serializes only ref IDs.
No hidden backend-only descriptions leak into visible output.

### 5. Narration packet surfaces

`SceneCommandExecutionNarrationPacketRef` carries `visible_summary` (default
empty string) and `backend_only_ref_ids`. The visible serializer exposes
only the packet ref ID. The `visible_summary` field is a reference surface
label, not generated prose. The authority flag `narration_generation` is
explicitly `False`.

### 6. Model-boundary fixture surfaces

`SceneCommandExecutionModelBoundaryFixtureRef` records the relationship
between model-facing packets and backend truth without calling any model.
It is an evaluation reference only. The authority flag `model_authority`
is explicitly `False`.

### 7. Authority flags coverage

All 16 authority flags cover the denied authorities from PR-9:

- `implementation_beyond_skeleton`
- `live_play_authority`
- `model_authority`
- `prompt_rendering`
- `prose_parsing`
- `narration_generation`
- `persistence_writes`
- `rng_table_oracle_execution`
- `state_mutation`
- `event_append`
- `settlement_authorization`
- `pr5_arithmetic_execution`
- `consequence_application`
- `conversion`
- `sourcebook_inclusion`
- `canon_promotion`

All default to `False` and reject `True` at construction time.

### 8. Validator strictness

All validators are consistent with their factory counterparts. Factory
outputs always pass validators. Validators correctly check type, record
ID format, and metadata type. No gaps found.

### 9. Deterministic serialization

Both visible and backend serializers produce deterministic output verified
by repeated-call equality and `json.dumps(sort_keys=True)` comparison.
Metadata is deep-copied. Immutable tuples are used for sequences.

### 10. Guardrail allowlist updates

PR-9A added `scene_command_execution_skeleton.py` to three guardrail
allowlists (PR-5c, PR-5g, PR-5h). All additions are narrow — only the
specific new file path. No global weakening.

### 11. tiny_vertical_slice.py

`tiny_vertical_slice.py` was not modified by PR-9A and remains untouched
in this branch.

### 12. Forbidden path scan

No path toward live-play, UI/client, prompt templates, prompt execution,
prose parsing, model calls, persistence writes, RNG/table/oracle execution,
state mutation, event append, settlement, PR-5 arithmetic execution, broad
consequence application, conversion, sourcebook inclusion, or canon
promotion was introduced.

## Hardening Actions Taken

1. Added this review artifact.
2. Added focused PR-9B hardening tests in
   `tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py`.
3. Added PR-9B registry entry in `astra_doctrine_registry_v0_1.yaml`.
4. Added PR-9B decision log entry in `current_decisions_log.md`.
5. Updated guardrail allowlists narrowly to recognize PR-9B artifacts.

## Non-Authority Reaffirmation

PR-9B does not authorize:

- command-kind routing
- command-family dispatch
- legality resolution
- validation execution engine
- packet compiler behavior beyond reference serialization checks
- model calls
- prompt templates or prompt execution
- prose parsing or narration generation
- live-play adapter or session loop
- UI/client
- persistence implementation
- database or file writes as runtime behavior
- RNG/dice/table/oracle execution
- state mutation
- event ledger append
- settlement authorization
- PR-5 arithmetic execution
- consequence application
- combat, inventory, social, mission, ability, crafting, or reward mechanics
- conversion/sourcebook/canon promotion

## Next Step

PR-9B must be reviewed and merged before PR-9C or any subsequent runtime
generalization work proceeds.

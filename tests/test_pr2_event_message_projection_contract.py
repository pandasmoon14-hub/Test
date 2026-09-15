# Executable validation for PR2-EVENT activation and message/projection contract.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
CONTRACT = ROOT / "docs/doctrine/control/myravant_command_event_message_projection_contract.md"
CONC_CLOSURE_TEST = ROOT / "tests/test_pr2_conc_post_merge_closure.py"

BASE = "e765d00e57e3a444ecd16078a3390eb49958f5b2"
AUTH = "owner_directive_2026-09-15_pr2_event_activation"
EFFECT = "runtime_message_contract_only"
ARTIFACT = "PR2-EVENT-COMMAND-EVENT-MESSAGE-PROJECTION-001"
MERGE = "e9a41cc7b144ffab0ca8fa91c4a9b3a9a1a56214"


def read_at(ref, path):
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path.relative_to(ROOT).as_posix()}"],
        cwd=ROOT,
        text=True,
    )


def load_at(ref, path):
    return json.loads(read_at(ref, path))


def load_manifest():
    return load_at(MERGE, MAN)


def rows(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def contract_text():
    return read_at(MERGE, CONTRACT)


def test_event_activation_identity_and_exact_single_active_workstream():
    manifest = load_manifest()
    by = rows(manifest)
    event = by["PR2-EVENT"]
    assert manifest["artifact_version"] == "0.4.33"
    assert {r["workstream_id"] for r in manifest["workstreams"] if r["status"] == "active"} == {"PR2-EVENT"}
    assert event["status"] == "active"
    assert event["authorization_reference"] == AUTH
    assert event["authority_effect"] == EFFECT
    assert event["starting_baseline"] == BASE
    assert event["control_artifact"] == "docs/doctrine/control/myravant_command_event_message_projection_contract.md"
    assert event["pull_request"] is None
    assert event["branch_head"] is None
    assert event["merge_commit"] is None
    assert event["downstream_handoff"] == ["PR2-PERSIST", "PR2-TEST"]


def test_event_owned_surface_is_bounded_and_predecessor_closure_is_frozen():
    event = rows(load_manifest())["PR2-EVENT"]
    assert set(event["owned_paths"]) == {
        "docs/decisions/current_decisions_log.md",
        "docs/doctrine/control/myravant_command_event_message_projection_contract.md",
        "docs/doctrine/control/post_r2a_transition_manifest.yaml",
        "docs/doctrine/control/post_r2a_transition_program.md",
        "tests/test_post_r2a_transition_program.py",
        "tests/test_pr2_event_message_projection_contract.py",
        "tests/test_pr2_conc_post_merge_closure.py",
    }
    closure = read_at(MERGE, CONC_CLOSURE_TEST)
    assert f'ACCEPTED_MERGE = "{BASE}"' in closure
    assert "load_at(ACCEPTED_MERGE, MAN)" in closure
    assert "read_at(ACCEPTED_MERGE, PROG)" in closure
    assert "read_at(ACCEPTED_MERGE, DEC)" in closure


def test_event_does_not_activate_successors_or_r3():
    manifest = load_manifest()
    by = rows(manifest)
    for wid in ("PR2-PERSIST", "PR2-FID", "PR2-BP", "PR2-AUDIT", "PR2-MIG", "PR2-TEST", "PR2-IMPL"):
        assert by[wid]["status"] == "blocked", wid
        assert by[wid]["authorization_reference"] is None, wid
        assert by[wid]["starting_baseline"] is None, wid
    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_contract_metadata_and_authority_boundaries_are_exact():
    text = contract_text()
    for required in (
        f"artifact_id: {ARTIFACT}",
        "workstream: PR2-EVENT",
        f"authority_reference: {AUTH}",
        f"authority_effect: {EFFECT}",
        f"starting_baseline: {BASE}",
        "runtime_implementation_authority: none",
        "production_schema_authority: none",
        "semantic_commitment_owner_authority: none",
        "semantic_event_identity_authority: none",
        "command_identity_authority: none",
        "logical_time_authority: none",
        "persistence_recovery_semantics_authority: none",
    ):
        assert required in text


def test_existing_owner_separation_is_explicit():
    text = contract_text()
    for required in (
        "AFQR-01 retains qualified state/write ownership",
        "AFQR-02 retains command identity",
        "AFQR-04 retains logical time",
        "PR2-PART retains logical authority partition identity",
        "PR2-CONC retains physical-concurrency nonauthority",
        "R2B-CORE retains committed randomness preservation",
    ):
        assert required in text


def test_representation_classes_are_explicit_and_noncollapsing():
    text = contract_text()
    for heading in (
        "### 7.1 Request envelope",
        "### 7.2 Proposal envelope",
        "### 7.3 Committed-fact representation",
        "### 7.4 Delta message",
        "### 7.5 Notification message",
        "### 7.6 Projection update",
        "### 7.7 Transport acknowledgement",
        "### 7.8 Control or diagnostic message",
    ):
        assert heading in text
    assert "The term “event” must be qualified" in text


def test_core_message_nonauthority_laws_are_explicit():
    text = contract_text()
    for rule in (
        "message delivery\n!= semantic commitment",
        "publish success\n!= semantic commitment",
        "transport acknowledgement\n!= transition receipt",
        "message arrival order\n!= causal order",
        "projection state\n!= authoritative state",
        "redelivery\n!= semantic re-execution",
    ):
        assert rule in text


def test_semantic_transport_and_attempt_identity_are_distinct():
    text = contract_text()
    assert "semantic_fact_identity\n!= transport_message_identity\n!= transport_attempt_identity" in text
    assert "Transport attempts are not command attempts" in text
    assert "Those are transport attempts." in text
    assert "AFQR-02 governs that change" in text


def test_delivery_guarantee_duplicate_and_idempotency_boundaries_exist():
    text = contract_text()
    assert "Delivery guarantees are declared, not assumed" in text
    assert "Exactly-once transport is not a semantic shortcut" in text
    assert "Duplicate transport delivery must not automatically duplicate semantic effects." in text
    assert "Idempotency is qualified to a declared consumer operation and identity envelope." in text
    assert "Content equality alone is insufficient" in text


def test_order_and_causality_are_carried_not_reowned():
    text = contract_text()
    assert "Physical arrival order is nonauthoritative." in text
    assert "Causality metadata carriage" in text
    assert "Correlation is not causation" in text
    assert "Queue order, broker offset, and wall clock are physical facts" in text
    assert "They are not automatically AFQR-04 logical time or causality." in text


def test_projection_notification_visibility_and_rebuild_boundaries_exist():
    text = contract_text()
    assert "Projections are derivative" in text
    assert "Projection freshness and lag" in text
    assert "Projection rebuilding boundary" in text
    assert "Those durable semantics belong to PR2-PERSIST." in text
    assert "Notifications are not knowledge doctrine" in text
    assert "Hidden information and disclosure" in text


def test_correction_randomness_and_version_context_are_preserved():
    text = contract_text()
    assert "Corrections, compensation, supersession, and retcon pressure" in text
    assert "Delivery retries must not mutate the original committed record into the correction." in text
    assert "must not reroll or replace randomness already committed under R2B-CORE" in text
    assert "R2B-CROSS-PHASE owns those identities and applicability rules." in text


def test_cross_partition_concurrency_and_failure_boundaries_are_explicit():
    text = contract_text()
    assert "A message crossing a partition boundary does not transfer semantic ownership" in text
    assert "Concurrent producers or consumers must not use race timing" in text
    assert "Failure after semantic commitment but before notification" in text
    assert "A committed fact remains committed" in text
    assert "Consumer failure after processing" in text
    assert "Cancelling a delivery attempt or timing out a consumer does not undo an already committed fact." in text


def test_no_technology_pattern_is_promoted_to_doctrine():
    text = contract_text()
    for required in (
        "Event sourcing is optional",
        "CQRS is optional",
        "Pub/sub is optional",
        "Actor/mailbox patterns are optional",
        "database choice",
        "message-bus choice",
        "cloud-provider choice",
    ):
        assert required in text


def test_handoffs_and_r3_boundary_are_preserved():
    text = contract_text()
    assert "PR2-PERSIST must define durable persistence" in text
    assert "PR2-FID must define lawful aggregation/detail transitions" in text
    assert "PR2-BP will later define overload" in text
    assert "The frozen 34-record R3 conformance target" in text
    assert "R3 remains separately authorized." in text


def test_corpus_pressure_outliers_and_anti_collapse_are_explicit():
    text = contract_text()
    assert "## 52. Corpus-scale pressure families" in text
    assert "local single-process runtimes" in text
    assert "cross-partition messaging" in text
    assert "event-sourced implementations" in text
    assert "non-event-sourced implementations" in text
    assert "## 53. Important outliers" in text
    assert "PR2-EVENT is not a semantic super-owner." in text
    assert "## 54. Anti-collapse rules" in text
    assert "projection rebuild into authoritative replay" in text


def test_program_and_decisions_record_bounded_event_activation():
    program = read_at(MERGE, PROG)
    decisions = read_at(MERGE, DEC)
    assert "**Artifact version:** `0.4.33`" in program
    assert "### 5.30 PR2-EVENT command/event/message/projection activation" in program
    assert AUTH in program and EFFECT in program and BASE in program
    assert "PR2-EVENT is the only active successor workstream." in program
    assert "PR2-PERSIST remains `blocked` and unauthorized." in program
    assert "PR2-EVENT-ACTIVATION-001" in decisions
    assert AUTH in decisions and EFFECT in decisions and BASE in decisions
    assert "does not activate PR2-PERSIST" in decisions


def test_completion_condition_preserves_owner_boundaries():
    text = contract_text()
    assert "## 55. Completion condition" in text
    assert "AFQR-01 commitment/replay ownership" in text
    assert "AFQR-02 command/attempt/\nretry identity" in text
    assert "AFQR-04 logical time/causality/scheduling ownership" in text
    assert "separate PERSIST/FID/BP ownership" in text
    assert "no runtime\nimplementation or technology mandate" in text

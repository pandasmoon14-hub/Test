# Executable validation for Myravant R4-A native substrate design.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE = "fa4f1d795275eaaad4ee525aea7e3f3c2c2bd5e9"
AUTH = "owner_directive_2026-09-17_r4_a_myravant_native_substrate_design"
EFFECT = "myravant_native_substrate_design_only"
R4_A_ACCEPTED_MERGE = "6455659b61bc0b56fa6c41f95e15f5b1b94d077a"

REVIEW = (
    ROOT
    / "docs/doctrine/reviews/"
    "r4_a_myravant_native_substrate_design.yaml"
)
R1E = (
    ROOT
    / "docs/doctrine/reviews/"
    "afqr_r1e_escalation_and_substrate_adjudications.yaml"
)
MAN = (
    ROOT
    / "docs/doctrine/control/"
    "post_r2a_transition_manifest.yaml"
)


def git_text_at(ref, path):
    rel = path.relative_to(ROOT).as_posix()

    return subprocess.check_output(
        ["git", "show", f"{ref}:{rel}"],
        cwd=ROOT,
    ).decode("utf-8")


def load(path):
    if path == MAN:
        return json.loads(
            git_text_at(R4_A_ACCEPTED_MERGE, path)
        )

    return json.loads(path.read_text(encoding="utf-8"))


def test_r4_a_scope_is_exact_and_design_only():
    review = load(REVIEW)

    assert review["artifact_version"] == "0.1.1"
    assert review["status"] == "validated_complete"
    assert review["tranche_id"] == "R4-A"
    assert review["tracking_tranche"] == "PR2-AUDIT-C"
    assert review["authorization_reference"] == AUTH
    assert review["authority_effect"] == EFFECT
    assert review["starting_baseline"] == BASE

    scope = review["scope"]

    assert scope["historical_deferred_substrate_classes"] == 5
    assert scope["selected_native_capabilities"] == 1
    assert scope["runtime_edit_count"] == 0
    assert scope["schema_edit_count"] == 0

    for key in (
        "migration_authorized",
        "implementation_authorized",
        "r4_activation_authorized",
        "pr2_mig_authorized",
        "pr2_test_authorized",
        "pr2_impl_authorized",
    ):
        assert scope[key] is False


def test_exact_five_historical_substrate_classes_are_consumed():
    review = load(REVIEW)
    r1e = load(R1E)

    expected = {
        row["substrate_id"]
        for row in r1e["substrate_adjudications"]
    }

    actual = {
        row["substrate_id"]
        for row in review["historical_substrate_dispositions"]
    }

    assert expected == {
        "SUB-001",
        "SUB-002",
        "SUB-003",
        "SUB-004",
        "SUB-005",
    }

    assert actual == expected
    assert len(review["historical_substrate_dispositions"]) == 5

    assert all(
        row["historical_owner_separation_preserved"] is True
        for row in review["historical_substrate_dispositions"]
    )

    assert all(
        row["historical_combined_owner_prohibition_preserved"] is True
        for row in review["historical_substrate_dispositions"]
    )

    assert all(
        row["generalized_form_selected"] is False
        for row in review["historical_substrate_dispositions"]
    )

    assert sum(
        row["contributes_to_selected_capability"]
        for row in review["historical_substrate_dispositions"]
    ) == 2


def test_selected_native_capability_is_narrow_and_playable():
    review = load(REVIEW)
    cap = review["selected_native_capability"]

    assert cap["capability_id"] == "R4-A-CAP-001"
    assert cap["name"] == (
        "persistent_world_entity_and_location_relation_representation"
    )

    entity = cap["entity_representation_requirements"]

    assert entity["campaign_local_stable_identity"] is True
    assert entity["coverage_is_closed_enum"] is False
    assert entity["classification_may_imply_control"] is False
    assert entity["classification_may_imply_agency"] is False
    assert entity["classification_may_imply_ownership"] is False
    assert entity["classification_may_imply_authority"] is False

    relation = cap["relation_representation_requirements"]

    assert relation["typed_relation_envelope_required"] is True
    assert relation["initial_relation_type"] == "located_at"
    assert relation["initial_relation_semantic_owner"] == "AFQR-18"
    assert (
        relation["relation_extension_requires_owner_qualification"]
        is True
    )
    assert (
        relation["relation_record_may_transfer_semantic_ownership"]
        is False
    )


def test_r4_a_reuses_runtime_surfaces_instead_of_replacing_them():
    review = load(REVIEW)

    for path in review["existing_runtime_reuse"]:
        assert (ROOT / path).is_file(), path

    non_goals = set(
        review["selected_native_capability"]["explicit_non_goals"]
    )

    assert "universal_world_state_manager" in non_goals
    assert "generalized_governed_relation_registry" in non_goals
    assert "global_bitemporal_truth_or_evidence_store" in non_goals
    assert "second_owner_reducer_transaction_journal" in non_goals
    assert "registered_interface_bridge_hypergraph" in non_goals
    assert (
        "combined_spatial_signal_embodiment_institution_social_owner"
        in non_goals
    )


def test_r4_b_is_candidate_only_and_existing_gates_remain():
    review = load(REVIEW)
    manifest = load(MAN)

    handoff = review["implementation_handoff"]

    assert handoff["candidate_package"] == "R4-B"
    assert handoff["candidate_defined"] is True
    assert handoff["ready_pending_authorization"] is False
    assert handoff["authorized"] is False

    assert set(handoff["blocked_by_existing_post_r2_gates"]) == {
        "PR2-AUDIT",
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    }

    assert manifest["artifact_version"] == "0.4.48"
    assert manifest["r2_gate_state"]["R4-R6"] == "blocked"
    assert (
        manifest["r3_conformance_target"]["runtime_promotion_clear"]
        is False
    )

    target = manifest["r4_native_substrate_design_target"]

    assert target["status"] == "validated"
    assert target["selected_native_capability_count"] == 1
    assert target["runtime_edits_authorized"] is False
    assert target["schema_edits_authorized"] is False
    assert target["r4_activation_authorized"] is False
    assert target["implementation_authorized"] is False
    assert target["runtime_promotion_clear"] is False
    assert target["r4_b_candidate_defined"] is True
    assert target["r4_b_ready_pending_authorization"] is False
    assert target["r4_b_authorized"] is False

    by_id = {
        row["workstream_id"]: row
        for row in manifest["workstreams"]
    }

    assert by_id["PR2-AUDIT"]["status"] == "active"
    assert by_id["PR2-AUDIT"]["current_tranche"] == "PR2-AUDIT-C"

    for wid in ("PR2-MIG", "PR2-TEST", "PR2-IMPL"):
        assert by_id[wid]["status"] == "blocked"
        assert by_id[wid]["authorization_reference"] is None


def test_r4_a_does_not_claim_audit_or_promotion_completion():
    review = load(REVIEW)

    assert (
        review["summary"]["repository_wide_pr2_audit_complete"]
        is False
    )
    assert review["summary"]["runtime_promotion_clear"] is False
    assert review["summary"]["r4_activation_authorized"] is False
    assert review["validation_state"] == "validated"
    assert set(review["validation_evidence"]) == {
        "R4-A focused pre-certification:28 passed",
        (
            "R4-A full local repository suite:"
            "9232 passed, 10 skipped, 2 xfailed, 1 warning"
        ),
        (
            "R4-A focused post-suite regression:"
            "28 passed"
        ),
        "R4-A git diff --check:clean",
        "R4-A exact seven-file footprint:PASS",
        "R4-A runtime/schema noninterference audit:PASS",
    }

# Executable validation for PR2-ID-T2E completion recording.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "9045a6cd4ec1fbfb23eac27b2fd5d8ef3e822448"
AUTH = "owner_directive_2026-09-10_pr2_id_t2e_completion_recording_activation"
EFFECT = "identity_migration_completion_recording_only"

REVIEW = ROOT / "docs/doctrine/reviews/pr2_id_identity_migration_completion_review.yaml"
LEDGER = ROOT / "docs/doctrine/control/myravant_identity_surface_disposition_ledger.yaml"
MANIFEST = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
CONTRACT = ROOT / "docs/doctrine/control/myravant_identity_migration_contract.md"
PROGRAM = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"

CLASSES = ['roadmap_currentness_setting_and_planning_authority', 'astra_prefixed_governance_and_working_group_role_identity', 'r1b_shared_vocabulary_identity_and_exact_parity', 'software_namespace_future_alias_or_deprecation_policy']

ALLOWED_T2E_PATHS = {
    "docs/doctrine/reviews/pr2_id_identity_migration_completion_review.yaml",
    "docs/doctrine/control/myravant_identity_surface_disposition_ledger.yaml",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/myravant_identity_migration_contract.md",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "docs/decisions/current_decisions_log.md",
    "tests/test_pr2_id_myravant_identity_migration.py",
    "tests/test_pr2_id_identity_surface_disposition_ledger.py",
    "tests/test_pr2_id_t2b_doctrine_identity_migration.py",
    "tests/test_pr2_id_t2c_noncurrent_surface_retention.py",
    "tests/test_pr2_id_t2d_roadmap_registry_adjudication.py",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_id_t2e_completion_recording.py",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def test_t2e_review_records_pass_without_pretending_residuals_are_solved():
    review = load(REVIEW)
    assert review["artifact_id"] == "PR2-ID-T2E-COMPLETION-REVIEW-001"
    assert review["artifact_version"] == "0.2.0"
    assert review["status"] == "validated"
    assert review["workstream_id"] == "PR2-ID"
    assert review["tranche_id"] == "PR2-ID-T2E"
    assert review["starting_branch_head"] == START
    assert review["authorization_reference"] == AUTH
    assert review["authority_effect"] == EFFECT
    assert review["review_result"] == "PASS"

    findings = review["audit_findings"]
    assert findings["all_authorized_current_facing_migrations_complete"] is True
    assert findings["unclassified_material_current_facing_identity_surfaces_found"] is False
    assert findings["additional_identity_migration_required_for_pr2_id_closure"] is False

    obligations = review["carried_forward_obligations"]
    assert [row["class_id"] for row in obligations] == CLASSES
    assert all(row["blocks_pr2_id_completion"] is False for row in obligations)
    assert obligations[-1]["pr2_id_disposition"] == "retain_compatibility"
    assert review["t2e_validation_state"] == "passed"


def test_t2e_manifest_is_active_pending_own_validation_and_downstream_is_blocked():
    manifest = load(MANIFEST)
    assert manifest["artifact_version"] == "0.4.10"
    by_id = {row["workstream_id"]: row for row in manifest["workstreams"]}
    pr2id = by_id["PR2-ID"]

    assert pr2id["status"] == "validated"
    assert pr2id["current_tranche"] == "PR2-ID-T2E"
    assert pr2id["current_tranche_starting_head"] == START
    assert pr2id["current_tranche_authorization_reference"] == AUTH
    assert pr2id["tranche_authority_effect"] == EFFECT
    assert pr2id["completion_audit_result"] == "PASS"
    assert pr2id["residual_gaps"] == []
    assert [row["class_id"] for row in pr2id["carried_forward_obligations"]] == CLASSES
    assert pr2id["next_tranche_authorized"] is False
    assert any("8961 passed" in row for row in pr2id["validation_evidence"])

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["execution_authorized"] is False
    for wid in ["PR2-SRC", "PR2-ORG", "PR2-IR", "PR2-SCALE"]:
        assert by_id[wid]["status"] == "blocked"
        assert by_id[wid]["authorization_reference"] is None


def test_t2e_ledger_preserves_the_four_obligations_and_completion_rule():
    ledger = load(LEDGER)
    assert ledger["artifact_version"] == "0.5.1"
    assert ledger["status"] == "validated"
    assert ledger["unresolved_escalations"] == []
    t2e = ledger["t2e_completion_tranche"]
    assert t2e["status"] == "validated"
    assert t2e["starting_branch_head"] == START
    assert t2e["authorization_reference"] == AUTH
    assert t2e["authority_effect"] == EFFECT
    assert t2e["completion_audit_result"] == "PASS"
    assert [row["class_id"] for row in ledger["carried_forward_obligations"]] == CLASSES


def test_t2e_does_not_modify_identity_or_semantic_surfaces():
    changed = set(git("diff", "--name-only", START).splitlines())
    changed |= set(
        git("ls-files", "--others", "--exclude-standard").splitlines()
    )
    changed.discard("")
    assert changed == ALLOWED_T2E_PATHS
    assert not any(
        path.startswith(("src/", "schemas/", "docs/doctrine/consolidation/"))
        for path in changed
    )
    assert "README.md" not in changed
    assert "AGENTS.md" not in changed
    assert "CLAUDE.md" not in changed
    assert "docs/doctrine/astra_doctrine_roadmap_v0_1.md" not in changed
    assert "docs/doctrine/astra_doctrine_registry_v0_1.yaml" not in changed
    assert "pyproject.toml" not in changed


def test_t2e_authority_and_nonauthority_are_cross_recorded():
    contract = CONTRACT.read_text(encoding="utf-8")
    program = PROGRAM.read_text(encoding="utf-8")
    decisions = DECISIONS.read_text(encoding="utf-8")

    for text in [contract, program, decisions]:
        assert "PR2-ID-T2E" in text
        assert AUTH in text
        assert START in text

    assert "PR2-ID-T2E-COMPLETION-RECORDING-001" in decisions
    assert "PR2-ID is therefore `validated`" in program
    assert "R3 remains `ready_pending_authorization`" in program

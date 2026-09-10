"""Executable validation for the PR2-ID Myravant identity migration."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "843fc89f3769a8e6323fa7b683d3805a9edfc142"
AUTH = "owner_directive_2026-09-08_pr2_id_activation"
T1_HEAD = "09d9aa2cc92944b4dc93104cdd4c68ea961c90c9"
T2B_START = "f7c29730ebcca5d593621c1bca77dea54f5d0223"
T2B_AUTH = "owner_directive_2026-09-09_pr2_id_t2b_activation"
T2C_START = "e00bf6d6a8b7180dff34202a5602d69cab151d7f"
T2C_AUTH = "owner_directive_2026-09-09_pr2_id_t2c_recording_activation"
T2D_START = "89d101fb6cbf44d2120871dbc6723ba8842e431b"
T2D_AUTH = "owner_directive_2026-09-09_pr2_id_t2d_activation"
T2E_START = "9045a6cd4ec1fbfb23eac27b2fd5d8ef3e822448"
T2E_AUTH = "owner_directive_2026-09-10_pr2_id_t2e_completion_recording_activation"
T2E_EFFECT = "identity_migration_completion_recording_only"

CONTRACT = ROOT / "docs/doctrine/control/myravant_identity_migration_contract.md"
LEDGER = ROOT / "docs/doctrine/control/myravant_identity_surface_disposition_ledger.yaml"
MANIFEST = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROGRAM = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
README = ROOT / "README.md"
AGENTS = ROOT / "AGENTS.md"
CLAUDE = ROOT / "CLAUDE.md"
PYPROJECT = ROOT / "pyproject.toml"

T1_ALLOWED = {
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "docs/doctrine/control/myravant_identity_migration_contract.md",
    "docs/doctrine/control/myravant_identity_surface_disposition_ledger.yaml",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "docs/decisions/current_decisions_log.md",
    "tests/test_pr2_id_myravant_identity_migration.py",
    "tests/test_pr2_id_identity_surface_disposition_ledger.py",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_afqr_r2c_formal_completion_review.py",
}

T2B_OWNED = T1_ALLOWED | {
    "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md",
    "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml",
    "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md",
    "docs/doctrine/consolidation/afqr_r2b_core_qualifications.md",
    "docs/doctrine/consolidation/afqr_world_action_sensing.md",
    "docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md",
    "tests/test_afqr_r1d_world_action_sensing.py",
    "tests/test_conversion_runtime_origin_firewall.py",
    "tests/test_pr2_id_t2b_doctrine_identity_migration.py",
}

T2C_OWNED = T2B_OWNED | {
    "docs/doctrine/control/myravant_identity_noncurrent_surface_retention_record.yaml",
    "tests/test_pr2_id_t2c_noncurrent_surface_retention.py",
}

T2D_OWNED = T2C_OWNED | {
    "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
    "docs/doctrine/control/myravant_identity_roadmap_registry_adjudication_record.yaml",
    "tests/test_pr2_id_t2d_roadmap_registry_adjudication.py",
}

T2E_OWNED = T2D_OWNED | {
    "docs/doctrine/reviews/pr2_id_identity_migration_completion_review.yaml",
    "tests/test_pr2_id_t2e_completion_recording.py",
    "tests/test_afqr_r1e_formal_completion_review.py",
    "tests/test_afqr_r2_continuity_research_assimilation.py",
}


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def test_contract_establishes_identity_without_rewriting_history():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "**Workstream:** `PR2-ID`" in text
    assert "**Status:** `validated`" in text
    assert f"**Starting baseline:** `{BASE}`" in text
    assert f"**Authorization reference:** `{AUTH}`" in text

    for value in [
        "migrate_current",
        "migrate_with_historical_qualifier",
        "retain_historical",
        "retain_compatibility",
        "alias_then_migrate",
        "escalate",
        "Historical truth outranks cosmetic consistency.",
        "PR2-ID-T2A",
        "PR2-ID-T2B",
        "PR2-ID-T2C",
        "PR2-ID-T2D",
        "PR2-ID-T2E",
        "docs/doctrine/control/myravant_identity_surface_disposition_ledger.yaml",
    ]:
        assert value in text

    assert LEDGER.is_file()


def test_current_facing_navigation_uses_myravant():
    readme = README.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    claude = CLAUDE.read_text(encoding="utf-8")

    assert readme.startswith("# Myravant\n")
    assert agents.startswith("# Myravant Agent Operating Map\n")
    assert "This repository is **Myravant**." in claude

    for text in [readme, agents, claude]:
        assert "Astra Ascension" in text
        assert "histor" in text.lower()


def test_software_namespace_is_deliberately_retained_for_compatibility():
    pyproject = PYPROJECT.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")

    assert 'name = "astra-runtime"' in pyproject
    assert (ROOT / "src/astra_runtime").is_dir()
    assert "`astra-runtime`" in contract
    assert "`astra_runtime`" in contract
    assert "compatibility tranche" in contract


def test_manifest_records_r2c_merge_and_pr2_id_activation():
    manifest = load_manifest()
    by_id = {row["workstream_id"]: row for row in manifest["workstreams"]}

    assert manifest["artifact_version"] == "0.4.10"
    assert manifest["r2_gate_state"]["R2"] == "complete"
    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["execution_authorized"] is False

    r2c = by_id["PR2-R2C"]
    assert r2c["status"] == "merged"
    assert r2c["pull_request"] == 379
    assert r2c["branch_head"] == "ea47efef19e1552f40fee7b7658797b59bd35b7f"
    assert r2c["merge_commit"] == BASE

    pr2id = by_id["PR2-ID"]
    assert pr2id["status"] == "validated"
    assert pr2id["authorization_reference"] == AUTH
    assert pr2id["starting_baseline"] == BASE
    assert set(pr2id["dependencies"]) == {"PR2-CTRL", "PR2-R2C"}
    assert set(pr2id["owned_paths"]) == T2E_OWNED
    assert pr2id["current_tranche"] == "PR2-ID-T2E"
    assert pr2id["tranche_control_artifact"] == "docs/doctrine/reviews/pr2_id_identity_migration_completion_review.yaml"
    assert pr2id["tranche_authority_effect"] == T2E_EFFECT
    assert pr2id["current_tranche_starting_head"] == T2E_START
    assert pr2id["current_tranche_authorization_reference"] == T2E_AUTH
    assert pr2id["completion_audit_result"] == "PASS"
    assert pr2id["next_tranche_authorized"] is False
    assert pr2id["pull_request"] is None
    assert pr2id["branch_head"] is None
    assert pr2id["merge_commit"] is None

    for wid, row in by_id.items():
        if wid == "PR2-ID":
            continue
        if wid.startswith("PR2-") and wid not in {
            "PR2-CTRL", "PR2-R2B-C", "PR2-R2B-X", "PR2-R2B-N", "PR2-R2C"
        }:
            assert row["status"] == "blocked"
            assert row["authorization_reference"] is None


def test_authorization_decisions_are_recorded():
    text = DECISIONS.read_text(encoding="utf-8")
    assert "PR2-ID-AUTHORIZATION-001" in text
    assert AUTH in text
    assert BASE in text
    assert "No global replacement is authorized." in text
    assert "PR2-ID-T2B-DOCTRINE-IDENTITY-MIGRATION-001" in text
    assert T2B_AUTH in text
    assert T2B_START in text
    assert "PR2-ID-T2C-NONCURRENT-SURFACE-RETENTION-001" in text
    assert T2C_AUTH in text
    assert T2C_START in text
    assert "PR2-ID-T2D-ROADMAP-REGISTRY-ADJUDICATION-001" in text
    assert T2D_AUTH in text
    assert T2D_START in text
    assert "PR2-ID-T2E-COMPLETION-RECORDING-001" in text
    assert T2E_AUTH in text
    assert T2E_START in text


def test_first_tranche_diff_is_bounded_at_its_published_head():
    changed = set(git("diff", "--name-only", f"{BASE}...{T1_HEAD}").splitlines())
    assert changed
    assert changed <= T1_ALLOWED
    assert not any(
        path.startswith(("src/", "schemas/", "docs/doctrine/reviews/"))
        for path in changed
    )
    assert not git(
        "diff",
        "--name-status",
        "--diff-filter=D",
        f"{BASE}...{T1_HEAD}",
    )

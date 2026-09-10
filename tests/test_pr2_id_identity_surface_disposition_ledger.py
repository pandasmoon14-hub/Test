"""Validation for PR2-ID identity dispositions through T2D adjudication."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "843fc89f3769a8e6323fa7b683d3805a9edfc142"
T2A_BASE = "09d9aa2cc92944b4dc93104cdd4c68ea961c90c9"
T2A_HEAD = "f7c29730ebcca5d593621c1bca77dea54f5d0223"
T2B_AUTH = "owner_directive_2026-09-09_pr2_id_t2b_activation"
T2B_HEAD = "e00bf6d6a8b7180dff34202a5602d69cab151d7f"
T2C_AUTH = "owner_directive_2026-09-09_pr2_id_t2c_recording_activation"
T2D_BASE = "89d101fb6cbf44d2120871dbc6723ba8842e431b"
T2D_AUTH = "owner_directive_2026-09-09_pr2_id_t2d_activation"

LEDGER = (
    ROOT
    / "docs"
    / "doctrine"
    / "control"
    / "myravant_identity_surface_disposition_ledger.yaml"
)

ALLOWED_DISPOSITIONS = {
    "migrate_current",
    "migrate_with_historical_qualifier",
    "retain_historical",
    "retain_compatibility",
    "alias_then_migrate",
    "escalate",
}

EXPECTED_RULES = {
    "ID-DISP-001-NAVIGATION": "migrate_with_historical_qualifier",
    "ID-DISP-002-DECISION-HISTORY": "retain_historical",
    "ID-DISP-003-FROZEN-REVIEWS": "retain_historical",
    "ID-DISP-004-WORKING-EVIDENCE": "retain_historical",
    "ID-DISP-005-D-SERIES-IMPORTED": "retain_historical",
    "ID-DISP-006-RUNTIME-NAMESPACE": "retain_compatibility",
    "ID-DISP-007-ROADMAP-REGISTRY-PATHS": "alias_then_migrate",
    "ID-DISP-008-ROADMAP-REGISTRY-CONTENT": "escalate",
    "ID-DISP-009-AFQR-CURRENT-NORMATIVE": "migrate_current",
    "ID-DISP-010-FIREWALL-CURRENT-NORMATIVE": "migrate_current",
    "ID-DISP-011-OTHER-CONTROL": "escalate",
    "ID-DISP-012-OTHER-DOCTRINE": "escalate",
    "ID-DISP-013-HANDOFF-OPERATIONS-HISTORY": "retain_historical",
    "ID-DISP-014-TEST-LITERALS": "escalate",
    "ID-DISP-015-STABLE-IDS": "retain_historical",
    "ID-DISP-016-UNKNOWN": "escalate",
}

T2B_CANDIDATES = {
    "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md",
    "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml",
    "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md",
    "docs/doctrine/consolidation/afqr_r2b_core_qualifications.md",
    "docs/doctrine/consolidation/afqr_world_action_sensing.md",
    "docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md",
}

PROTECTED_EXACT = {
    "pyproject.toml",
    "docs/doctrine/astra_doctrine_roadmap_v0_1.md",
    "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
    "docs/doctrine/native_design/d_series/_manifests/"
    "d_series_doctrine_pack_import_manifest.json",
    "src/astra_runtime/__init__.py",
} | T2B_CANDIDATES


def load_ledger():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def test_ledger_identity_and_inventory_counts_are_exact():
    data = load_ledger()

    assert data["artifact_id"] == (
        "PR2-ID-IDENTITY-SURFACE-DISPOSITION-LEDGER-001"
    )
    assert data["artifact_version"] == "0.5.1"
    assert data["status"] == "validated"
    assert data["workstream_id"] == "PR2-ID"
    assert data["tranche_id"] == "PR2-ID-T2A"
    assert data["starting_branch_head"] == T2A_BASE
    assert data["authority_effect"] == "identity_surface_classification_only"

    inventory = data["inventory_basis"]
    assert inventory["content_occurrence_lines"] == 2495
    assert inventory["files_with_occurrences"] == 454
    assert inventory["astra_named_tracked_paths"] == 233


def test_disposition_vocabulary_and_rules_are_bounded():
    data = load_ledger()

    assert set(data["allowed_dispositions"]) == ALLOWED_DISPOSITIONS

    rules = data["rules"]
    ids = [row["rule_id"] for row in rules]

    assert len(ids) == len(set(ids))
    assert set(ids) == set(EXPECTED_RULES)

    by_id = {row["rule_id"]: row for row in rules}

    for rule_id, disposition in EXPECTED_RULES.items():
        row = by_id[rule_id]
        assert row["disposition"] == disposition
        assert row["disposition"] in ALLOWED_DISPOSITIONS
        assert row["selector"]
        assert row["semantic_role"]
        assert row["rationale"]


def test_historical_and_compatibility_classes_do_not_become_rename_targets():
    data = load_ledger()
    by_id = {row["rule_id"]: row for row in data["rules"]}

    assert by_id["ID-DISP-003-FROZEN-REVIEWS"]["disposition"] == (
        "retain_historical"
    )
    assert by_id["ID-DISP-005-D-SERIES-IMPORTED"]["disposition"] == (
        "retain_historical"
    )
    assert by_id["ID-DISP-006-RUNTIME-NAMESPACE"]["disposition"] == (
        "retain_compatibility"
    )
    assert by_id["ID-DISP-008-ROADMAP-REGISTRY-CONTENT"]["disposition"] == (
        "escalate"
    )


def test_t2b_candidate_set_is_exact_and_separately_authorized():
    data = load_ledger()
    next_tranche = data["next_candidate_tranche"]

    assert next_tranche["tranche_id"] == "PR2-ID-T2B"
    assert next_tranche["status"] == "completed"
    assert next_tranche["publication_head"] == T2B_HEAD
    assert next_tranche["authority_granted"] is True
    assert next_tranche["starting_branch_head"] == T2A_HEAD
    assert next_tranche["authorization_reference"] == T2B_AUTH
    assert next_tranche["authority_effect"] == "semantic_neutral_current_doctrine_identity_migration_only"
    assert set(next_tranche["candidate_paths"]) == T2B_CANDIDATES
    assert next_tranche["audited_occurrence_dispositions"] == {
        "migrate_current": 58,
        "retain_historical": 18,
        "escalate_governance_role": 4,
        "escalate_exact_upstream_parity": 8,
        "retain_compatibility": 1,
    }
    assert set(next_tranche["coupled_test_paths"]) == {
        "tests/test_afqr_r1d_world_action_sensing.py",
        "tests/test_conversion_runtime_origin_firewall.py",
    }


def test_t2a_protected_exact_files_are_unchanged_from_r2c_baseline():
    for path in sorted(PROTECTED_EXACT):
        before = git("rev-parse", f"{BASE}:{path}")
        after = git("rev-parse", f"{T2A_HEAD}:{path}")
        assert before == after, path


def test_t2a_has_not_changed_prohibited_prefixes():
    changed = set(
        git("diff", "--name-only", f"{T2A_BASE}...{T2A_HEAD}").splitlines()
    )

    assert not any(
        path.startswith(
            (
                "src/",
                "docs/doctrine/reviews/",
                "docs/doctrine/native_design/d_series/",
            )
        )
        for path in changed
    )

    assert "pyproject.toml" not in changed
    assert "docs/doctrine/astra_doctrine_roadmap_v0_1.md" not in changed
    assert "docs/doctrine/astra_doctrine_registry_v0_1.yaml" not in changed


def test_t2b_authority_remains_bounded_and_downstream_stays_blocked():
    data = load_ledger()
    effect = data["completion_effect"]

    # Later PR2-ID tranches may lawfully rewrite the current completion-effect
    # summary. Validate durable tranche state and downstream nonauthority
    # instead of requiring obsolete T2B-era prose.
    assert data["next_candidate_tranche"]["tranche_id"] == "PR2-ID-T2B"
    assert data["next_candidate_tranche"]["status"] == "completed"
    assert data["t2c_recording_tranche"]["status"] == "completed"
    assert data["t2d_adjudication_tranche"]["status"] == "completed"
    assert data["t2e_completion_tranche"]["status"] == "validated"
    assert data["t2e_completion_tranche"]["starting_branch_head"] == "9045a6cd4ec1fbfb23eac27b2fd5d8ef3e822448"
    assert data["t2e_completion_tranche"]["authorization_reference"] == "owner_directive_2026-09-10_pr2_id_t2e_completion_recording_activation"
    assert data["t2e_completion_tranche"]["completion_audit_result"] == "PASS"
    assert len(data["carried_forward_obligations"]) == 4
    assert all(row["blocks_pr2_id_completion"] is False for row in data["carried_forward_obligations"])
    assert "does not authorize R3" in effect
    assert "downstream post-R2 workstream" in effect

    assert data["unresolved_escalations"] == []
    assert [row["class_id"] for row in data["carried_forward_obligations"]] == [
        "roadmap_currentness_setting_and_planning_authority",
        "astra_prefixed_governance_and_working_group_role_identity",
        "r1b_shared_vocabulary_identity_and_exact_parity",
        "software_namespace_future_alias_or_deprecation_policy",
    ]

    t2c = data["t2c_recording_tranche"]
    assert t2c["tranche_id"] == "PR2-ID-T2C"
    assert t2c["status"] == "completed"
    assert t2c["authority_granted"] is True
    assert t2c["starting_branch_head"] == T2B_HEAD
    assert t2c["authorization_reference"] == T2C_AUTH
    assert t2c["residual_files"] == 33
    assert t2c["high_recall_identity_occurrence_lines"] == 44
    assert t2c["content_edit_targets"] == 0
    assert t2c["disposition"] == "retain_historical"

    t2d = data["t2d_adjudication_tranche"]
    assert t2d["tranche_id"] == "PR2-ID-T2D"
    assert t2d["status"] == "completed"
    assert t2d["authority_granted"] is True
    assert t2d["starting_branch_head"] == T2D_BASE
    assert t2d["authorization_reference"] == T2D_AUTH
    assert t2d["roadmap_astra_bearing_lines"] == 35
    assert t2d["roadmap_content_edit_targets"] == 0
    assert t2d["registry_astra_bearing_lines"] == 310
    assert t2d["registry_migrate_current"] == 2
    assert t2d["registry_retain_historical"] == 187
    assert t2d["registry_escalate_governance_role"] == 119
    assert t2d["registry_escalate_roadmap_currentness"] == 2
    assert t2d["registry_compatibility_literal_lines"] == 61
    assert t2d["path_migration_authorized"] is False

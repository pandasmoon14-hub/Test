"""Validation for PR2-ID-T2A dispositions and separately authorized T2B activation."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "843fc89f3769a8e6323fa7b683d3805a9edfc142"
T2A_BASE = "09d9aa2cc92944b4dc93104cdd4c68ea961c90c9"
T2A_HEAD = "f7c29730ebcca5d593621c1bca77dea54f5d0223"
T2B_AUTH = "owner_directive_2026-09-09_pr2_id_t2b_activation"

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
    assert data["artifact_version"] == "0.2.0"
    assert data["status"] == "active"
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
    assert next_tranche["status"] == "active"
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

    assert "T2A classification remains authoritative" in effect
    assert "T2B is explicitly authorized" in effect
    assert "does not complete PR2-ID" in effect
    assert "authorize R3" in effect

    assert data["unresolved_escalations"] == [
        "roadmap_and_registry_currentness_and_identity_roles",
        "Astra_Doctrine_Council_governance_role_name",
        "broader_doctrine_current_authority_classification",
        "setting_or_canon_identity_vs_platform_identity",
        "software_namespace_future_alias_or_deprecation_policy",
        "r1b_shared_vocabulary_identity_and_exact_parity",
    ]

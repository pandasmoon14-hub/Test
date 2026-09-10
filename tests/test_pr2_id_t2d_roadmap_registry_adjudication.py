"""Executable validation for PR2-ID-T2D roadmap/registry adjudication."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
T2D_BASE = "89d101fb6cbf44d2120871dbc6723ba8842e431b"
T2D_AUTH = "owner_directive_2026-09-09_pr2_id_t2d_activation"
T2D_EFFECT = "roadmap_registry_occurrence_adjudication_and_two_registry_identity_migrations_only"
T2E_START = "9045a6cd4ec1fbfb23eac27b2fd5d8ef3e822448"
T2E_AUTH = "owner_directive_2026-09-10_pr2_id_t2e_completion_recording_activation"
T2E_EFFECT = "identity_migration_completion_recording_only"

ROADMAP = "docs/doctrine/astra_doctrine_roadmap_v0_1.md"
REGISTRY = "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
RECORD = ROOT / "docs/doctrine/control/myravant_identity_roadmap_registry_adjudication_record.yaml"
LEDGER = ROOT / "docs/doctrine/control/myravant_identity_surface_disposition_ledger.yaml"
MANIFEST = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"

OLD_PURPOSE = 'purpose: Track doctrine/schema file lifecycle, dependencies, gates, review state, pressure tests, donor-law creep controls, and promotion decisions for Astra Ascension.'
NEW_PURPOSE = 'purpose: Track doctrine/schema file lifecycle, dependencies, gates, review state, pressure tests, donor-law creep controls, and promotion decisions for Myravant.'
OLD_REGISTRY_REFUSAL = '  - registry cannot validate donor-shaped records as Astra-native'
NEW_REGISTRY_REFUSAL = '  - registry cannot validate donor-shaped records as Myravant-native'

UNRESOLVED = ['roadmap_currentness_setting_and_planning_authority', 'astra_prefixed_governance_and_working_group_role_identity', 'r1b_shared_vocabulary_identity_and_exact_parity', 'software_namespace_future_alias_or_deprecation_policy']


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def current(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def git_show(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{T2D_BASE}:{path}"],
        cwd=ROOT,
        text=True,
    )


def baseline_test_ref_counts():
    pattern = (
        "astra_doctrine_roadmap_v0_1|"
        "astra_doctrine_registry_v0_1|"
        "ROADMAP-001|REGISTRY-001"
    )
    out = subprocess.check_output(
        ["git", "grep", "-n", "-E", pattern, T2D_BASE, "--", "tests"],
        cwd=ROOT,
        text=True,
    )
    rows = [line for line in out.splitlines() if line.strip()]

    def path_of(line: str) -> str:
        return line.split(":", 3)[1]

    roadmap = [line for line in rows if "astra_doctrine_roadmap_v0_1" in line]
    registry = [line for line in rows if "astra_doctrine_registry_v0_1" in line]
    ids = [
        line for line in rows
        if "ROADMAP-001" in line or "REGISTRY-001" in line
    ]
    return {
        "roadmap_path_refs": {
            "line_count": len(roadmap),
            "file_count": len({path_of(line) for line in roadmap}),
        },
        "registry_path_refs": {
            "line_count": len(registry),
            "file_count": len({path_of(line) for line in registry}),
        },
        "stable_control_id_refs": {
            "line_count": len(ids),
            "file_count": len({path_of(line) for line in ids}),
        },
    }


def test_t2d_record_and_classification_counts_are_exact():
    data = load(RECORD)
    assert data["artifact_id"] == "PR2-ID-T2D-ROADMAP-REGISTRY-ADJUDICATION-001"
    assert data["artifact_version"] == "0.1.0"
    assert data["status"] == "completed"
    assert data["workstream_id"] == "PR2-ID"
    assert data["tranche_id"] == "PR2-ID-T2D"
    assert data["starting_branch_head"] == T2D_BASE
    assert data["authorization_reference"] == T2D_AUTH
    assert data["authority_effect"] == T2D_EFFECT

    roadmap = data["roadmap_dispositions"]
    assert roadmap["astra_bearing_lines"] == 35
    assert sum(roadmap["classification"].values()) == 35
    assert roadmap["classification"] == {
        "retain_historical": 1,
        "escalate_governance_role": 1,
        "escalate_currentness_setting_or_mixed_identity": 33,
        "migrate_current": 0,
    }

    registry = data["registry_dispositions"]
    assert registry["astra_bearing_lines_before_t2d"] == 310
    assert registry["astra_bearing_lines_after_t2d"] == 308
    assert sum(registry["classification"].values()) == 310
    assert registry["classification"] == {
        "retain_historical": 187,
        "escalate_governance_role": 119,
        "migrate_current": 2,
        "escalate_roadmap_currentness": 2,
    }
    assert sum(registry["retain_historical_detail"].values()) == 187


def test_roadmap_is_byte_exact_to_published_t2c_head():
    assert current(ROADMAP) == git_show(ROADMAP)


def test_registry_is_exactly_two_authorized_identity_replacements():
    before = git_show(REGISTRY)
    assert before.count(OLD_PURPOSE) == 1
    assert before.count(OLD_REGISTRY_REFUSAL) == 1

    expected = before.replace(OLD_PURPOSE, NEW_PURPOSE, 1).replace(
        OLD_REGISTRY_REFUSAL, NEW_REGISTRY_REFUSAL, 1
    )
    assert current(REGISTRY) == expected

    assert OLD_PURPOSE not in current(REGISTRY)
    assert NEW_PURPOSE in current(REGISTRY)
    assert OLD_REGISTRY_REFUSAL not in current(REGISTRY)
    assert NEW_REGISTRY_REFUSAL in current(REGISTRY)


def test_astra_line_counts_match_the_audited_baseline_and_two_edits():
    roadmap_before = git_show(ROADMAP)
    registry_before = git_show(REGISTRY)
    registry_after = current(REGISTRY)

    assert sum("Astra" in line for line in roadmap_before.splitlines()) == 35
    assert sum("Astra" in line for line in registry_before.splitlines()) == 310
    assert sum("Astra" in line for line in registry_after.splitlines()) == 308


def test_governance_role_lines_are_not_renamed_by_t2d():
    before = git_show(REGISTRY)
    after = current(REGISTRY)

    def governance_lines(text: str):
        return [
            line
            for line in text.splitlines()
            if "Astra" in line
            and (
                "Doctrine Council" in line
                or "Runtime Working Group" in line
                or "Canon Working Group" in line
                or "Training/Evaluation Working Group" in line
                or "Training and Evaluation Working Group" in line
            )
        ]

    assert governance_lines(after) == governance_lines(before)


def test_software_compatibility_literals_are_exactly_preserved():
    before = git_show(REGISTRY)
    after = current(REGISTRY)
    pattern = re.compile(r"astra-runtime|astra_runtime|src/astra_runtime")

    before_lines = [line for line in before.splitlines() if pattern.search(line)]
    after_lines = [line for line in after.splitlines() if pattern.search(line)]
    assert len(before_lines) == 61
    assert after_lines == before_lines


def test_stable_path_reference_evidence_matches_published_t2c_baseline():
    data = load(RECORD)
    assert data["stable_path_disposition"]["disposition"] == "alias_then_migrate"
    assert data["stable_path_disposition"]["migration_authorized_by_t2d"] is False
    assert data["stable_path_disposition"]["baseline_test_reference_counts"] == {
        "roadmap_path_refs": {"line_count": 5, "file_count": 4},
        "registry_path_refs": {"line_count": 113, "file_count": 97},
        "stable_control_id_refs": {"line_count": 8, "file_count": 1},
    }
    assert (
        data["stable_path_disposition"]["baseline_test_reference_counts"]
        == baseline_test_ref_counts()
    )


def test_governance_escalation_is_broadened_without_role_rename():
    data = load(RECORD)
    refinement = data["registry_dispositions"]["governance_scope_refinement"]
    assert refinement["previous_class"] == "Astra_Doctrine_Council_governance_role_name"
    assert (
        refinement["refined_class"]
        == "astra_prefixed_governance_and_working_group_role_identity"
    )
    assert refinement["disposition"] == "escalate"
    assert "Astra Doctrine Council" in refinement["examples"]
    assert "Astra Runtime Working Group" in refinement["examples"]
    assert "Astra Canon Working Group" in refinement["examples"]


def test_manifest_and_ledger_preserve_downstream_boundaries():
    record = load(RECORD)
    ledger = load(LEDGER)
    manifest = load(MANIFEST)

    assert record["unresolved_identity_classes_after_t2d"] == UNRESOLVED
    assert ledger["artifact_version"] == "0.5.1"
    assert ledger["unresolved_escalations"] == []
    assert [row["class_id"] for row in ledger["carried_forward_obligations"]] == UNRESOLVED

    t2d = ledger["t2d_adjudication_tranche"]
    assert t2d["status"] == "completed"
    assert t2d["starting_branch_head"] == T2D_BASE
    assert t2d["authorization_reference"] == T2D_AUTH
    assert t2d["registry_migrate_current"] == 2
    assert t2d["path_migration_authorized"] is False

    pr2id = next(
        row for row in manifest["workstreams"] if row["workstream_id"] == "PR2-ID"
    )
    assert manifest["artifact_version"] == "0.4.10"
    assert pr2id["status"] == "validated"
    assert pr2id["current_tranche"] == "PR2-ID-T2E"
    assert pr2id["tranche_authority_effect"] == T2E_EFFECT
    assert pr2id["current_tranche_starting_head"] == T2E_START
    assert pr2id["current_tranche_authorization_reference"] == T2E_AUTH
    assert pr2id["completion_audit_result"] == "PASS"
    assert pr2id["next_tranche_authorized"] is False
    assert pr2id["residual_gaps"] == []
    assert [row["class_id"] for row in pr2id["carried_forward_obligations"]] == UNRESOLVED

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["execution_authorized"] is False

    by_id = {row["workstream_id"]: row for row in manifest["workstreams"]}
    for wid in ["PR2-SRC", "PR2-ORG", "PR2-IR", "PR2-SCALE"]:
        assert by_id[wid]["status"] == "blocked"
        assert by_id[wid]["authorization_reference"] is None

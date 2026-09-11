"""Executable validation for PR2-ID-T2B semantic-neutral doctrine identity migration."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
T2A_HEAD = "f7c29730ebcca5d593621c1bca77dea54f5d0223"
T2B_AUTH = "owner_directive_2026-09-09_pr2_id_t2b_activation"
T2B_HEAD = "e00bf6d6a8b7180dff34202a5602d69cab151d7f"
T2C_AUTH = "owner_directive_2026-09-09_pr2_id_t2c_recording_activation"

CORE = "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
CROSS = "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml"
AGENCY = "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
R2B = "docs/doctrine/consolidation/afqr_r2b_core_qualifications.md"
WORLD = "docs/doctrine/consolidation/afqr_world_action_sensing.md"
FIREWALL = "docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md"
WORLD_TEST = "tests/test_afqr_r1d_world_action_sensing.py"
FIREWALL_TEST = "tests/test_conversion_runtime_origin_firewall.py"

TARGETS = [CORE, CROSS, AGENCY, R2B, WORLD, FIREWALL]


def git_show(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{T2A_HEAD}:{path}"],
        cwd=ROOT,
        text=True,
    )


def current(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def expected_transform(path: str, text: str) -> str:
    if path == CORE:
        assert text.count("Astra law") == 1
        return text.replace("Astra law", "Myravant law")

    if path == CROSS:
        assert text.count("Astra law") == 2
        return text.replace("Astra law", "Myravant law")

    if path == AGENCY:
        assert text.count("universal Astra law") == 2
        assert text.count("universal Astra default") == 6
        assert text.count("Astra Doctrine Council") == 3
        return (
            text.replace("universal Astra law", "universal Myravant law")
            .replace("universal Astra default", "universal Myravant default")
        )

    if path == R2B:
        assert text.count("universal Astra law") == 1
        return text.replace("universal Astra law", "universal Myravant law")

    if path == WORLD:
        assert text.count("Astra law") == 21
        assert text.count("one Astra type") == 8
        return text.replace("Astra law", "Myravant law")

    if path == FIREWALL:
        assert text.count("Astra") == 26
        assert text.count("Astra Doctrine Council") == 1
        sentinel = "__PR2_ID_T2B_COUNCIL__"
        text = text.replace("Astra Doctrine Council", sentinel)
        assert text.count("Astra") == 25
        return text.replace("Astra", "Myravant").replace(
            sentinel, "Astra Doctrine Council"
        )

    raise AssertionError(path)


def test_each_doctrine_owner_is_exactly_the_authorized_transform():
    for path in TARGETS:
        assert current(path) == expected_transform(path, git_show(path)), path


def test_audited_retentions_survive_exactly():
    agency = current(AGENCY)
    world = current(WORLD)
    firewall = current(FIREWALL)
    firewall_test = current(FIREWALL_TEST)

    assert agency.count("Astra Doctrine Council") == 3
    assert world.count("one Astra type") == 8
    assert world.count("one Myravant type") == 0
    assert firewall.count("Astra Doctrine Council") == 1
    assert firewall.count("Astra") == 1
    assert firewall.count("Myravant") == 25
    assert "`astra_runtime`" in firewall
    assert 'RUNTIME_ROOT = REPO_ROOT / "src" / "astra_runtime"' in firewall_test

    for path in [CORE, CROSS, AGENCY, WORLD]:
        before = git_show(path)
        after = current(path)
        before_paths = [line for line in before.splitlines() if "Astra_AFQR" in line]
        after_paths = [line for line in after.splitlines() if "Astra_AFQR" in line]
        assert after_paths == before_paths, path


def test_coupled_validation_literals_follow_the_owning_doctrine():
    world_test = current(WORLD_TEST)
    firewall_test = current(FIREWALL_TEST)

    assert (
        "donor anatomy, grid, damage, action-economy, cosmology, and sensing "
        "assumptions are not Myravant law"
    ) in world_test
    assert (
        "donor anatomy, grid, damage, action-economy, cosmology, and sensing "
        "assumptions are not Astra law"
    ) not in world_test
    assert "new Myravant-native identity" in firewall_test
    assert "new Astra-native identity" not in firewall_test


def test_t2b_control_state_and_counts_are_machine_readable():
    ledger = json.loads((ROOT / "docs/doctrine/control/myravant_identity_surface_disposition_ledger.yaml").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml").read_text(encoding="utf-8"))
    contract = (ROOT / "docs/doctrine/control/myravant_identity_migration_contract.md").read_text(encoding="utf-8")
    program = (ROOT / "docs/doctrine/control/post_r2a_transition_program.md").read_text(encoding="utf-8")
    decisions = (ROOT / "docs/decisions/current_decisions_log.md").read_text(encoding="utf-8")

    nxt = ledger["next_candidate_tranche"]
    assert nxt["tranche_id"] == "PR2-ID-T2B"
    assert nxt["status"] == "completed"
    assert nxt["publication_head"] == T2B_HEAD
    assert nxt["authority_granted"] is True
    assert nxt["starting_branch_head"] == T2A_HEAD
    assert nxt["authorization_reference"] == T2B_AUTH
    assert nxt["audited_occurrence_dispositions"] == {
        "migrate_current": 58,
        "retain_historical": 18,
        "escalate_governance_role": 4,
        "escalate_exact_upstream_parity": 8,
        "retain_compatibility": 1,
    }

    assert ledger["t2b_exact_exceptions"] == [
        {
            "path": WORLD,
            "field": "resolved_collision_boundary_records[*].corpus_collapse_risk",
            "literal": "high to critical if donor homonyms are treated as one Astra type",
            "occurrence_count": 8,
            "upstream_owner": (
                "docs/doctrine/consolidation/"
                "afqr_shared_vocabulary_and_type_owners.yaml"
            ),
            "disposition": "escalate",
            "rationale": (
                "These values are exact inherited R1B parity fields. "
                "The upstream owner is outside T2B, so identity-only migration "
                "must not mutate them."
            ),
        }
    ]

    assert ledger["validation_repairs"][0]["path"] == FIREWALL_TEST
    assert (
        ledger["validation_repairs"][0]["classification"]
        == "pre_existing_assertion_drift"
    )
    assert ledger["validation_repairs"][0]["readme_changed"] is False

    pr2id = next(
        row for row in manifest["workstreams"] if row["workstream_id"] == "PR2-ID"
    )
    assert pr2id["status"] in {"active", "validated", "merged"}
    assert pr2id["next_tranche_authorized"] is False

    assert "## 9B. Audited current-doctrine identity migration" in contract
    assert T2B_AUTH in contract
    assert "### 5.4 PR2-ID-T2B audited current-doctrine identity migration" in program
    assert T2B_AUTH in program
    assert "PR2-ID-T2B-DOCTRINE-IDENTITY-MIGRATION-001" in decisions
    assert T2B_AUTH in decisions


def test_t2b_does_not_claim_downstream_or_semantic_authority():
    ledger = json.loads((ROOT / "docs/doctrine/control/myravant_identity_surface_disposition_ledger.yaml").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml").read_text(encoding="utf-8"))

    # Validate the immutable T2B authority record rather than pinning later
    # tranches to T2B-era completion-effect prose.
    t2b = ledger["next_candidate_tranche"]
    assert t2b["tranche_id"] == "PR2-ID-T2B"
    assert t2b["status"] == "completed"
    assert (
        t2b["authority_effect"]
        == "semantic_neutral_current_doctrine_identity_migration_only"
    )

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["execution_authorized"] is False

    by_id = {row["workstream_id"]: row for row in manifest["workstreams"]}
    for wid in ["PR2-SRC", "PR2-ORG", "PR2-IR", "PR2-SCALE"]:
        assert by_id[wid]["status"] == "blocked"
        assert by_id[wid]["authorization_reference"] is None

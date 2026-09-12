import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROGRAM_PATH = (
    ROOT / "docs" / "doctrine" / "control" / "post_r2a_transition_program.md"
)
MANIFEST_PATH = (
    ROOT / "docs" / "doctrine" / "control" / "post_r2a_transition_manifest.yaml"
)

EXPECTED_BASELINE = "b1e4c70435ddd94a8e8fe82a11d8d6cace82b5bd"
R2B_CORE_BASELINE = "0a52db603589168a14f3c50beefbbf28274d0836"
R2B_CORE_AUTHORIZATION = "owner_directive_2026-09-07_r2b_core_activation"
R2B_CORE_HEAD = "8a88068b802a9819328e09691e7c1def778a778d"
R2B_CORE_PR = 376

R2B_CROSS_PHASE_BASELINE = "307ab295a8590d60a310d4b8d872971620fa74eb"
R2B_CROSS_PHASE_AUTHORIZATION = "owner_directive_2026-09-08_r2b_cross_phase_activation"
R2B_CROSS_PHASE_HEAD = "eededa8e0b845fa14ba303f4d34369cefdd2f861"
R2B_CROSS_PHASE_PR = 377

R2B_CONTINUITY_BASELINE = "d70e9a5c1ab67c8e2bb6a2b8331c73269cc3b286"
R2B_CONTINUITY_AUTHORIZATION = "owner_directive_2026-09-08_r2b_continuity_activation"
R2B_CONTINUITY_HEAD = "d94f5e8f40b1b74d6bdb23e2e419e5cb5d6fb34f"
R2B_CONTINUITY_PR = 378
R2C_BASELINE = "5cae79bcdd86c93c6fe77b6492a8a087a83900b0"
R2C_AUTHORIZATION = "owner_directive_2026-09-08_r2c_activation"
R2C_VALIDATED_HEAD = "949575f42f8b4ba1e01963013b35376d49433faf"
R2C_PUBLICATION_HEAD = "ea47efef19e1552f40fee7b7658797b59bd35b7f"
R2C_PR = 379
R2C_MERGE = "843fc89f3769a8e6323fa7b683d3805a9edfc142"
PR2_ID_AUTHORIZATION = "owner_directive_2026-09-08_pr2_id_activation"
PR2_ID_T2B_AUTHORIZATION = "owner_directive_2026-09-09_pr2_id_t2b_activation"
PR2_ID_T2B_STARTING_HEAD = "f7c29730ebcca5d593621c1bca77dea54f5d0223"
PR2_ID_T2C_AUTHORIZATION = "owner_directive_2026-09-09_pr2_id_t2c_recording_activation"
PR2_ID_T2C_STARTING_HEAD = "e00bf6d6a8b7180dff34202a5602d69cab151d7f"
PR2_ID_T2D_AUTHORIZATION = "owner_directive_2026-09-09_pr2_id_t2d_activation"
PR2_ID_T2D_STARTING_HEAD = "89d101fb6cbf44d2120871dbc6723ba8842e431b"
PR2_ID_T2E_AUTHORIZATION = "owner_directive_2026-09-10_pr2_id_t2e_completion_recording_activation"
PR2_ID_T2E_STARTING_HEAD = "9045a6cd4ec1fbfb23eac27b2fd5d8ef3e822448"
PR2_ID_T2E_EFFECT = "identity_migration_completion_recording_only"
PR2_ID_PR = 380
PR2_ID_HEAD = "024236e0ce9af3b6622e0a5b7be3a1ec3d4c99a3"
PR2_ID_MERGE = "1d1b16004b4bee0c75ca42c82900755ec29022bd"
PR2_SRC_A_BASELINE = "4033f43b2a4ad7088955ca1a29daf47a33ef7a37"
PR2_SRC_A_AUTHORIZATION = "owner_directive_2026-09-10_pr2_src_a_activation"
PR2_SRC_A_EFFECT = "foundational_source_research_governance_only"
PR2_SRC_A_PR = 382
PR2_SRC_A_HEAD = "ac82cebeeb3b8eb63fc6b4a312e90554584a1d32"
PR2_SRC_A_MERGE = "818a79d03ac487722762a44c9a80b29391278a8f"
PR2_SRC_B_BASELINE = "818a79d03ac487722762a44c9a80b29391278a8f"
PR2_SRC_B_AUTHORIZATION = "owner_directive_2026-09-11_pr2_src_b_activation"
PR2_SRC_B_EFFECT = "heterogeneous_source_research_method_qualification_only"
PR2_SRC_B_PR = 383
PR2_SRC_B_HEAD = "cabd12d56e7e036b2b839f21486776b49ebff56b"
PR2_SRC_B_MERGE = "70f7195100d0ccb7ba3c4cbd0dc34d684717ccaa"
PR2_SRC_C_BASELINE = "70f7195100d0ccb7ba3c4cbd0dc34d684717ccaa"
PR2_SRC_C_AUTHORIZATION = "owner_directive_2026-09-11_pr2_src_c_activation"
PR2_SRC_C_EFFECT = "legacy_source_conversion_surface_disposition_only"
PR2_SRC_C_PR = 384
PR2_SRC_C_HEAD = "b71de0fb8b5565f63dbb0019faad2cd5cf390465"
PR2_SRC_C_MERGE = "21b4ba706bb3f68aeb51dc4195fe1aa60014a439"
PR2_SRC_D_BASELINE = "21b4ba706bb3f68aeb51dc4195fe1aa60014a439"
PR2_SRC_D_AUTHORIZATION = "owner_directive_2026-09-11_pr2_src_d_activation"
PR2_SRC_D_EFFECT = "independent_source_research_completion_review_only"
PR2_SRC_D_PR = 385
PR2_SRC_D_HEAD = "7fd2f1c202abd7107dc2918e168d7885fb9452ce"
PR2_SRC_D_MERGE = "376214e1b715de34160dfb03d328547f510b6586"
PR2_SRC_D_TREE = "bcf9dd80d9a39594e60a62218bff3ee64aa85abb"
PR2_SRC_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-11_pr2_src_post_merge_closure"
PR2_SRC_CLOSURE_EFFECT = "source_research_post_merge_lifecycle_reconciliation_only"
PR2_SRC_CLOSURE_MERGE = "c14da427bf5c5c21c7ef1655e83aea3519587cc6"
PR2_ORG_BASELINE = "c14da427bf5c5c21c7ef1655e83aea3519587cc6"
PR2_ORG_AUTHORIZATION = "owner_directive_2026-09-11_pr2_org_activation"
PR2_ORG_EFFECT = "content_eligibility_and_provenance_governance_only"
PR2_ORG_CONTRACT = "docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md"
PR2_ORG_PR = 387
PR2_ORG_HEAD = "a7aed059e1b96872150c05203dfdb9c07affe831"
PR2_ORG_MERGE = "031053afd9ac581cfc421554ee3383a11a0dc2bd"
PR2_ORG_TREE = "ac770e1c69a448545b0a58eb7ed49a0b13f81614"
PR2_ORG_CLOSURE_AUTHORIZATION = "owner_directive_2026-09-11_pr2_org_post_merge_closure"
PR2_ORG_CLOSURE_EFFECT = "originality_eligibility_post_merge_lifecycle_reconciliation_only"
PR2_ORG_OWNED_PATHS = {'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'tests/test_pr2_src_completion_review.py', 'tests/test_pr2_src_post_merge_closure.py', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_org_originality_provenance_eligibility.py', 'docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md', 'docs/doctrine/control/post_r2a_transition_program.md', 'docs/decisions/current_decisions_log.md'}

EXPECTED_R2_GATES = {
    "R1": "complete",
    "R2": "complete",
    "R2-0": "complete",
    "R2A": "complete",
    "R2B": "complete",
    "R2C": "complete",
    "R3": "ready_pending_authorization",
    "R4-R6": "blocked",
    "RT-002G": "unauthorized",
    "temporary_evidence_deletion": "unauthorized",
}

EXPECTED_R2B_PACKAGES = {
    "R2B-CORE": "merged",
    "R2B-AGENCY": "not_required",
    "R2B-WORLD": "not_required",
    "R2B-CONTINUITY": "merged",
    "R2B-CROSS-PHASE": "merged",
}

EXPECTED_R2B_SEQUENCE = [
    "R2B-CORE",
    "R2B-CROSS-PHASE",
    "R2B-CONTINUITY",
]

EXPECTED_WORKSTREAM_IDS = {
    "PR2-CTRL",
    "PR2-R2B-C",
    "PR2-R2B-X",
    "PR2-R2B-N",
    "PR2-R2C",
    "PR2-ID",
    "PR2-SRC",
    "PR2-ORG",
    "PR2-CORPUS",
    "PR2-IR",
    "PR2-FICT",
    "PR2-SIMEX",
    "PR2-SCALE",
    "PR2-PART",
    "PR2-CONC",
    "PR2-FID",
    "PR2-EVENT",
    "PR2-PERSIST",
    "PR2-BP",
    "PR2-AUDIT",
    "PR2-MIG",
    "PR2-TEST",
    "PR2-IMPL",
}

EXPECTED_STATUS_VOCABULARY = {
    "identified",
    "blocked",
    "ready_pending_authorization",
    "authorized",
    "active",
    "implemented",
    "validated",
    "merged",
    "superseded",
    "not_required",
}

TERMINAL_STATUSES = {
    "merged",
    "superseded",
    "not_required",
}

UNRESOLVED_IDENTITY_CLASSES = [
    "roadmap_currentness_setting_and_planning_authority",
    "astra_prefixed_governance_and_working_group_role_identity",
    "r1b_shared_vocabulary_identity_and_exact_parity",
    "software_namespace_future_alias_or_deprecation_policy",
]

POST_R2_READY = {
    "PR2-CORPUS",
    "PR2-IR",
    "PR2-FICT",
    "PR2-SIMEX",
}

POST_R2_BLOCKED = {
    "PR2-SCALE",
    "PR2-PART",
    "PR2-CONC",
    "PR2-FID",
    "PR2-EVENT",
    "PR2-PERSIST",
    "PR2-BP",
    "PR2-AUDIT",
    "PR2-MIG",
    "PR2-TEST",
    "PR2-IMPL",
}


def _load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _by_id(manifest):
    return {
        workstream["workstream_id"]: workstream
        for workstream in manifest["workstreams"]
    }


def test_control_artifacts_exist():
    assert PROGRAM_PATH.is_file()
    assert MANIFEST_PATH.is_file()


def test_frozen_baseline_and_identity_are_exact():
    manifest = _load_manifest()

    assert manifest["artifact_version"] == "0.4.18"
    assert manifest["frozen_starting_baseline"] == EXPECTED_BASELINE
    assert manifest["starting_event"]["pull_request"] == 374
    assert manifest["starting_event"]["merge_commit"] == EXPECTED_BASELINE

    invariants = manifest["program_invariants"]
    assert invariants["future_project_identity"] == "Myravant"
    assert invariants["historical_project_identity"] == "Astra Ascension"
    assert invariants["minimum_external_source_scale"] >= 1000


def test_core_program_invariants_are_preserved():
    manifest = _load_manifest()
    invariants = manifest["program_invariants"]

    assert invariants["books_are_atomic_evidence_units"] is True
    assert invariants["books_are_default_myravant_production_units"] is False
    assert invariants["corpus_frequency_is_doctrine_authority"] is False
    assert invariants["semantic_mapping_implies_distribution_eligibility"] is False
    assert invariants["rename_may_rewrite_immutable_history"] is False
    assert invariants["post_r2_program_work_held_until_r2c_complete"] is True
    assert (
        invariants["runtime_scalability_invariant"]
        == "logical_simulation_semantics_are_independent_of_physical_execution_topology"
    )


def test_r2c_gate_state_and_r2b_completion_are_exact():
    manifest = _load_manifest()

    assert manifest["r2_gate_state"] == EXPECTED_R2_GATES
    assert manifest["r2b_package_state"] == EXPECTED_R2B_PACKAGES
    assert manifest["recommended_r2b_sequence"] == EXPECTED_R2B_SEQUENCE


def test_r3_target_is_ready_but_not_authorized():
    manifest = _load_manifest()
    target = manifest["r3_conformance_target"]

    assert target["status"] == "ready_pending_authorization"
    assert target["selector"] == "pressure_route == r3_conformance"
    assert target["candidate_count"] == 34
    assert target["execution_authorized"] is False
    assert target["source_index"] == (
        "docs/doctrine/reviews/r2a/dispositions_runtime_schema/index.yaml"
    )
    assert set(target["excluded_pressure_routes"]) == {
        "r4_substrate",
        "later_gate",
        "none",
    }


def test_status_vocabulary_is_bounded():
    manifest = _load_manifest()
    statuses = manifest["status_vocabulary"]

    assert len(statuses) == len(set(statuses))
    assert set(statuses) == EXPECTED_STATUS_VOCABULARY
    assert set(manifest["terminal_statuses"]) == TERMINAL_STATUSES


def test_workstream_registry_is_exact_and_unique():
    manifest = _load_manifest()
    workstreams = manifest["workstreams"]
    ids = [workstream["workstream_id"] for workstream in workstreams]

    assert len(ids) == 23
    assert len(ids) == len(set(ids))
    assert set(ids) == EXPECTED_WORKSTREAM_IDS


def test_all_dependencies_resolve_and_statuses_are_legal():
    manifest = _load_manifest()
    workstreams = manifest["workstreams"]
    ids = {workstream["workstream_id"] for workstream in workstreams}
    allowed = set(manifest["status_vocabulary"])

    missing = []
    for workstream in workstreams:
        assert workstream["status"] in allowed
        for dependency in workstream["dependencies"]:
            if dependency not in ids:
                missing.append((workstream["workstream_id"], dependency))

    assert missing == []


def test_r2b_merge_chain_is_fully_recorded():
    manifest = _load_manifest()
    by_id = _by_id(manifest)

    core = by_id["PR2-R2B-C"]
    assert core["status"] == "merged"
    assert core["authorization_reference"] == R2B_CORE_AUTHORIZATION
    assert core["starting_baseline"] == R2B_CORE_BASELINE
    assert core["pull_request"] == R2B_CORE_PR
    assert core["branch_head"] == R2B_CORE_HEAD
    assert core["merge_commit"] == R2B_CROSS_PHASE_BASELINE
    assert core["residual_gaps"] == []

    cross = by_id["PR2-R2B-X"]
    assert cross["status"] == "merged"
    assert cross["authorization_reference"] == R2B_CROSS_PHASE_AUTHORIZATION
    assert cross["starting_baseline"] == R2B_CROSS_PHASE_BASELINE
    assert cross["pull_request"] == R2B_CROSS_PHASE_PR
    assert cross["branch_head"] == R2B_CROSS_PHASE_HEAD
    assert cross["merge_commit"] == R2B_CONTINUITY_BASELINE
    assert cross["residual_gaps"] == []

    continuity = by_id["PR2-R2B-N"]
    assert continuity["status"] == "merged"
    assert continuity["authorization_reference"] == R2B_CONTINUITY_AUTHORIZATION
    assert continuity["starting_baseline"] == R2B_CONTINUITY_BASELINE
    assert continuity["pull_request"] == R2B_CONTINUITY_PR
    assert continuity["branch_head"] == R2B_CONTINUITY_HEAD
    assert continuity["merge_commit"] == R2C_BASELINE
    assert continuity["residual_gaps"] == []


def test_r2c_pr2_id_pr2_src_pr2_org_are_merged_and_no_successor_is_active():
    manifest = _load_manifest()
    by_id = _by_id(manifest)

    active = {
        workstream["workstream_id"]
        for workstream in manifest["workstreams"]
        if workstream["status"] == "active"
    }
    assert active == set()

    r2c = by_id["PR2-R2C"]
    assert r2c["status"] == "merged"
    assert r2c["authorization_reference"] == R2C_AUTHORIZATION
    assert r2c["starting_baseline"] == R2C_BASELINE
    assert r2c["pull_request"] == R2C_PR
    assert r2c["branch_head"] == R2C_PUBLICATION_HEAD
    assert r2c["merge_commit"] == R2C_MERGE
    assert r2c["residual_gaps"] == []

    pr2id = by_id["PR2-ID"]
    assert pr2id["status"] == "merged"
    assert pr2id["authorization_reference"] == PR2_ID_AUTHORIZATION
    assert pr2id["starting_baseline"] == R2C_MERGE
    assert set(pr2id["dependencies"]) == {"PR2-CTRL", "PR2-R2C"}
    assert pr2id["pull_request"] == PR2_ID_PR
    assert pr2id["branch_head"] == PR2_ID_HEAD
    assert pr2id["merge_commit"] == PR2_ID_MERGE
    assert pr2id["residual_gaps"] == []
    assert [row["class_id"] for row in pr2id["carried_forward_obligations"]] == UNRESOLVED_IDENTITY_CLASSES
    assert pr2id["current_tranche"] == "PR2-ID-T2E"
    assert pr2id["tranche_authority_effect"] == PR2_ID_T2E_EFFECT
    assert pr2id["current_tranche_starting_head"] == PR2_ID_T2E_STARTING_HEAD
    assert (
        pr2id["current_tranche_authorization_reference"]
        == PR2_ID_T2E_AUTHORIZATION
    )
    assert pr2id["completion_audit_result"] == "PASS"
    assert pr2id["next_tranche_authorized"] is False

    src = by_id["PR2-SRC"]
    assert src["status"] == "merged"
    assert src["authorization_reference"] == PR2_SRC_A_AUTHORIZATION
    assert src["authority_effect"] == PR2_SRC_A_EFFECT
    assert src["starting_baseline"] == PR2_SRC_A_BASELINE
    assert src["current_tranche"] == "PR2-SRC-D"
    assert src["tranche_authority_effect"] == PR2_SRC_D_EFFECT
    assert src["tranche_control_artifact"] == (
        "docs/doctrine/reviews/pr2_src_source_research_completion_review.yaml"
    )
    assert src["current_tranche_starting_head"] == PR2_SRC_D_BASELINE
    assert src["current_tranche_authorization_reference"] == PR2_SRC_D_AUTHORIZATION
    assert src["completion_review_result"] == "PASS"
    assert src["completion_review_blocking_findings"] == []
    assert src["next_tranche_authorized"] is False
    assert src["pull_request"] == PR2_SRC_D_PR
    assert src["branch_head"] == PR2_SRC_D_HEAD
    assert src["merge_commit"] == PR2_SRC_D_MERGE
    assert src["completion_state"] == "merged"
    assert src["post_merge_closure_authorization_reference"] == PR2_SRC_CLOSURE_AUTHORIZATION
    assert src["post_merge_closure_authority_effect"] == PR2_SRC_CLOSURE_EFFECT
    assert src["post_merge_closure_recorded_from"] == PR2_SRC_D_MERGE
    assert src["post_merge_closure_tree"] == PR2_SRC_D_TREE
    assert [row["tranche_id"] for row in src["planned_tranches"]] == [
        "PR2-SRC-A",
        "PR2-SRC-B",
        "PR2-SRC-C",
        "PR2-SRC-D",
    ]
    tranches = {row["tranche_id"]: row for row in src["planned_tranches"]}
    assert tranches["PR2-SRC-A"]["state"] == "merged"
    assert tranches["PR2-SRC-A"]["pull_request"] == PR2_SRC_A_PR
    assert tranches["PR2-SRC-A"]["branch_head"] == PR2_SRC_A_HEAD
    assert tranches["PR2-SRC-A"]["merge_commit"] == PR2_SRC_A_MERGE
    assert tranches["PR2-SRC-B"]["state"] == "merged"
    assert tranches["PR2-SRC-B"]["pull_request"] == PR2_SRC_B_PR
    assert tranches["PR2-SRC-B"]["branch_head"] == PR2_SRC_B_HEAD
    assert tranches["PR2-SRC-B"]["merge_commit"] == PR2_SRC_B_MERGE
    assert tranches["PR2-SRC-C"]["state"] == "merged"
    assert tranches["PR2-SRC-C"]["pull_request"] == PR2_SRC_C_PR
    assert tranches["PR2-SRC-C"]["branch_head"] == PR2_SRC_C_HEAD
    assert tranches["PR2-SRC-C"]["merge_commit"] == PR2_SRC_C_MERGE
    assert tranches["PR2-SRC-D"]["state"] == "merged"
    assert tranches["PR2-SRC-D"]["authorization_reference"] == PR2_SRC_D_AUTHORIZATION
    assert tranches["PR2-SRC-D"]["authority_effect"] == PR2_SRC_D_EFFECT
    assert tranches["PR2-SRC-D"]["starting_baseline"] == PR2_SRC_D_BASELINE
    assert tranches["PR2-SRC-D"]["review_result"] == "PASS"
    assert tranches["PR2-SRC-D"]["source_processing_authorized"] is False
    assert tranches["PR2-SRC-D"]["pull_request"] == PR2_SRC_D_PR
    assert tranches["PR2-SRC-D"]["branch_head"] == PR2_SRC_D_HEAD
    assert tranches["PR2-SRC-D"]["merge_commit"] == PR2_SRC_D_MERGE
    assert tranches["PR2-SRC-D"]["merge_tree"] == PR2_SRC_D_TREE

    org = by_id["PR2-ORG"]
    assert org["status"] == "merged"
    assert org["authorization_reference"] == PR2_ORG_AUTHORIZATION
    assert org["authority_effect"] == PR2_ORG_EFFECT
    assert org["starting_baseline"] == PR2_ORG_BASELINE
    assert org["control_artifact"] == PR2_ORG_CONTRACT
    assert set(org["owned_paths"]) == PR2_ORG_OWNED_PATHS
    assert org["pull_request"] == PR2_ORG_PR
    assert org["branch_head"] == PR2_ORG_HEAD
    assert org["merge_commit"] == PR2_ORG_MERGE
    assert org["completion_state"] == "merged"
    assert org["post_merge_closure_authorization_reference"] == PR2_ORG_CLOSURE_AUTHORIZATION
    assert org["post_merge_closure_authority_effect"] == PR2_ORG_CLOSURE_EFFECT
    assert org["post_merge_closure_recorded_from"] == PR2_ORG_MERGE
    assert org["post_merge_closure_tree"] == PR2_ORG_TREE

def test_post_r2_successor_readiness_does_not_imply_authorization():
    manifest = _load_manifest()
    by_id = _by_id(manifest)

    org = by_id["PR2-ORG"]
    assert org["status"] == "merged"
    assert org["authorization_reference"] == PR2_ORG_AUTHORIZATION
    assert org["post_merge_closure_authorization_reference"] == PR2_ORG_CLOSURE_AUTHORIZATION

    for workstream_id in POST_R2_READY:
        assert by_id[workstream_id]["status"] == "ready_pending_authorization"
        assert by_id[workstream_id]["authorization_reference"] is None

    for workstream_id in POST_R2_BLOCKED:
        assert by_id[workstream_id]["status"] == "blocked"
        assert by_id[workstream_id]["authorization_reference"] is None


def test_critical_dependency_chain_is_preserved():
    manifest = _load_manifest()
    by_id = _by_id(manifest)

    assert by_id["PR2-R2B-C"]["dependencies"] == ["PR2-CTRL"]
    assert by_id["PR2-R2B-X"]["dependencies"] == ["PR2-R2B-C"]
    assert by_id["PR2-R2B-N"]["dependencies"] == ["PR2-R2B-X"]
    assert set(by_id["PR2-R2C"]["dependencies"]) == {
        "PR2-R2B-C",
        "PR2-R2B-X",
        "PR2-R2B-N",
    }
    assert by_id["PR2-SRC"]["dependencies"] == ["PR2-CTRL"]
    assert set(by_id["PR2-AUDIT"]["dependencies"]) == {
        "PR2-ID",
        "PR2-SRC",
        "PR2-ORG",
        "PR2-CORPUS",
        "PR2-IR",
        "PR2-SCALE",
    }
    assert set(by_id["PR2-PERSIST"]["dependencies"]) == {
        "PR2-SCALE",
        "PR2-R2B-C",
        "PR2-R2B-X",
        "PR2-R2B-N",
    }
    assert set(by_id["PR2-IMPL"]["dependencies"]) == {
        "PR2-R2C",
        "PR2-MIG",
        "PR2-TEST",
    }


def test_program_and_manifest_retain_required_current_cross_references():
    program = PROGRAM_PATH.read_text(encoding="utf-8")
    manifest = _load_manifest()

    assert "**Artifact version:** `0.4.18`" in program
    assert EXPECTED_BASELINE in program
    assert R2B_CORE_BASELINE in program
    assert R2B_CROSS_PHASE_BASELINE in program
    assert R2B_CONTINUITY_BASELINE in program
    assert R2C_BASELINE in program
    assert R2C_AUTHORIZATION in program
    assert "Myravant" in program
    assert "1,000+" in program
    assert "Review result:\n\n`PASS`" in program
    assert "`R3=ready_pending_authorization`" in program
    assert "exactly `34` such records" in program

    for package in EXPECTED_R2B_SEQUENCE:
        assert package in program

    for workstream_id in EXPECTED_WORKSTREAM_IDS:
        assert workstream_id in program

    assert (
        "Logical simulation semantics must remain independent of physical execution topology."
        in program
    )
    assert (
        manifest["program_document"]
        == "docs/doctrine/control/post_r2a_transition_program.md"
    )


def test_program_explicitly_preserves_successor_authorization_boundaries():
    program = PROGRAM_PATH.read_text(encoding="utf-8")

    # R2C itself did not activate a successor. PR2-ID was authorized later
    # through its own explicit owner directive.
    assert "R2C completion did not automatically activate a successor." in program
    assert "`PR2-ID` is `merged` through PR `#380`" in program
    assert "`R3` remains `ready_pending_authorization`" in program
    assert "### 5.9 PR2-SRC-A foundational source research governance" in program
    assert "### 5.10 PR2-SRC-B heterogeneous research-method qualification" in program
    assert "### 5.11 PR2-SRC-C legacy source/conversion surface disposition" in program
    assert "### 5.12 PR2-SRC-D independent completion review" in program
    assert "### 5.13 PR2-SRC post-merge closure recording" in program
    assert "`PR2-SRC` is terminal `merged`" in program
    assert "### 5.14 PR2-ORG originality, provenance, and content-eligibility activation" in program
    assert "### 5.15 PR2-ORG post-merge closure recording" in program
    assert "PR2-ORG is\nterminal `merged`" in program
    assert PR2_ORG_AUTHORIZATION in program
    assert PR2_ORG_BASELINE in program
    assert PR2_ORG_CONTRACT in program
    assert PR2_ORG_HEAD in program
    assert PR2_ORG_MERGE in program
    assert PR2_ORG_TREE in program
    assert PR2_SRC_A_AUTHORIZATION in program
    assert PR2_SRC_A_BASELINE in program
    assert PR2_SRC_A_HEAD in program
    assert PR2_SRC_A_MERGE in program
    assert PR2_SRC_B_AUTHORIZATION in program
    assert PR2_SRC_B_BASELINE in program
    assert PR2_SRC_B_HEAD in program
    assert PR2_SRC_B_MERGE in program
    assert PR2_SRC_C_AUTHORIZATION in program
    assert PR2_SRC_C_BASELINE in program
    assert PR2_SRC_C_HEAD in program
    assert PR2_SRC_C_MERGE in program
    assert PR2_SRC_D_AUTHORIZATION in program
    assert PR2_SRC_D_BASELINE in program
    assert PR2_SRC_D_HEAD in program
    assert PR2_SRC_D_MERGE in program
    assert "PR2-ID identity authority does not transfer authority" in program
    assert "RT-002G=unauthorized" in program
    assert "### 5.4 PR2-ID-T2B audited current-doctrine identity migration" in program
    assert PR2_ID_T2B_AUTHORIZATION in program
    assert PR2_ID_T2B_STARTING_HEAD in program
    assert "### 5.5 PR2-ID-T2C noncurrent identity-surface retention recording" in program
    assert PR2_ID_T2C_AUTHORIZATION in program
    assert PR2_ID_T2C_STARTING_HEAD in program
    assert "### 5.6 PR2-ID-T2D roadmap and registry occurrence adjudication" in program
    assert PR2_ID_T2D_AUTHORIZATION in program
    assert PR2_ID_T2D_STARTING_HEAD in program
    assert "### 5.7 PR2-ID-T2E completion audit recording" in program
    assert PR2_ID_T2E_AUTHORIZATION in program
    assert PR2_ID_T2E_STARTING_HEAD in program

def test_program_completion_rule_forbids_untracked_disappearance():
    manifest = _load_manifest()
    rule = manifest["program_completion_rule"]

    assert rule["untracked_disappearance_allowed"] is False
    assert "terminal state" in rule["required"]
    assert "successor handoff" in rule["required"]

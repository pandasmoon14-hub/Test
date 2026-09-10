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

POST_R2_BLOCKED = {
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

    assert manifest["artifact_version"] == "0.4.8"
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


def test_r2c_is_merged_and_pr2_id_is_the_only_active_workstream():
    manifest = _load_manifest()
    by_id = _by_id(manifest)

    active = {
        workstream["workstream_id"]
        for workstream in manifest["workstreams"]
        if workstream["status"] == "active"
    }
    assert active == {"PR2-ID"}

    r2c = by_id["PR2-R2C"]
    assert r2c["status"] == "merged"
    assert r2c["authorization_reference"] == R2C_AUTHORIZATION
    assert r2c["starting_baseline"] == R2C_BASELINE
    assert r2c["pull_request"] == R2C_PR
    assert r2c["branch_head"] == R2C_PUBLICATION_HEAD
    assert r2c["merge_commit"] == R2C_MERGE
    assert r2c["residual_gaps"] == []

    pr2id = by_id["PR2-ID"]
    assert pr2id["status"] == "active"
    assert pr2id["authorization_reference"] == PR2_ID_AUTHORIZATION
    assert pr2id["starting_baseline"] == R2C_MERGE
    assert set(pr2id["dependencies"]) == {"PR2-CTRL", "PR2-R2C"}
    assert pr2id["pull_request"] is None
    assert pr2id["branch_head"] is None
    assert pr2id["merge_commit"] is None
    assert pr2id["residual_gaps"] == UNRESOLVED_IDENTITY_CLASSES
    assert pr2id["current_tranche"] == "PR2-ID-T2D"
    assert pr2id["tranche_authority_effect"] == "roadmap_registry_occurrence_adjudication_and_two_registry_identity_migrations_only"
    assert pr2id["current_tranche_starting_head"] == PR2_ID_T2D_STARTING_HEAD
    assert (
        pr2id["current_tranche_authorization_reference"]
        == PR2_ID_T2D_AUTHORIZATION
    )
    assert pr2id["next_tranche_authorized"] is False

def test_post_r2_major_work_remains_blocked_and_unauthorized():
    manifest = _load_manifest()
    by_id = _by_id(manifest)

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

    assert "**Artifact version:** `0.4.8`" in program
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
    assert "`PR2-ID` is `active`" in program
    assert "`R3` remains `ready_pending_authorization`" in program
    assert "`PR2-SRC` and all other source-governance" in program
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

def test_program_completion_rule_forbids_untracked_disappearance():
    manifest = _load_manifest()
    rule = manifest["program_completion_rule"]

    assert rule["untracked_disappearance_allowed"] is False
    assert "terminal state" in rule["required"]
    assert "successor handoff" in rule["required"]

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

EXPECTED_R2_GATES = {
    "R1": "complete",
    "R2": "active_incomplete",
    "R2-0": "complete",
    "R2A": "complete",
    "R2B": "ready",
    "R2C": "blocked",
    "R3-R6": "blocked",
    "RT-002G": "unauthorized",
    "temporary_evidence_deletion": "unauthorized",
}

EXPECTED_R2B_PACKAGES = {
    "R2B-CORE": "required_pending_authorization",
    "R2B-AGENCY": "not_required",
    "R2B-WORLD": "not_required",
    "R2B-CONTINUITY": "required_pending_authorization",
    "R2B-CROSS-PHASE": "required_pending_authorization",
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


def _load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_control_artifacts_exist():
    assert PROGRAM_PATH.is_file()
    assert MANIFEST_PATH.is_file()


def test_frozen_baseline_and_identity_are_exact():
    manifest = _load_manifest()

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

    assert (
        invariants["runtime_scalability_invariant"]
        == "logical_simulation_semantics_are_independent_of_physical_execution_topology"
    )


def test_r2_gate_state_is_not_advanced_by_transition_control():
    manifest = _load_manifest()

    assert manifest["r2_gate_state"] == EXPECTED_R2_GATES
    assert manifest["r2b_package_state"] == EXPECTED_R2B_PACKAGES
    assert manifest["recommended_r2b_sequence"] == EXPECTED_R2B_SEQUENCE


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


def test_all_dependencies_resolve():
    manifest = _load_manifest()

    workstreams = manifest["workstreams"]
    ids = {workstream["workstream_id"] for workstream in workstreams}

    missing = []

    for workstream in workstreams:
        for dependency in workstream["dependencies"]:
            if dependency not in ids:
                missing.append(
                    (workstream["workstream_id"], dependency)
                )

    assert missing == []


def test_all_workstream_statuses_are_legal():
    manifest = _load_manifest()

    allowed = set(manifest["status_vocabulary"])

    for workstream in manifest["workstreams"]:
        assert workstream["status"] in allowed


def test_transition_control_is_the_only_active_workstream():
    manifest = _load_manifest()

    active = {
        workstream["workstream_id"]
        for workstream in manifest["workstreams"]
        if workstream["status"] == "active"
    }

    assert active == {"PR2-CTRL"}


def test_r2b_core_is_ready_but_not_authorized():
    manifest = _load_manifest()

    by_id = {
        workstream["workstream_id"]: workstream
        for workstream in manifest["workstreams"]
    }

    core = by_id["PR2-R2B-C"]

    assert core["status"] == "ready_pending_authorization"
    assert core["authorization_required"] is True
    assert core["authorization_reference"] is None


def test_downstream_major_work_remains_blocked():
    manifest = _load_manifest()

    by_id = {
        workstream["workstream_id"]: workstream
        for workstream in manifest["workstreams"]
    }

    blocked = {
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

    for workstream_id in blocked:
        assert by_id[workstream_id]["status"] == "blocked"


def test_critical_dependency_chain_is_preserved():
    manifest = _load_manifest()

    by_id = {
        workstream["workstream_id"]: workstream
        for workstream in manifest["workstreams"]
    }

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


def test_program_and_manifest_retain_required_cross_references():
    program = PROGRAM_PATH.read_text(encoding="utf-8")
    manifest = _load_manifest()

    assert EXPECTED_BASELINE in program
    assert "Myravant" in program
    assert "1,000+" in program

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


def test_program_completion_rule_forbids_untracked_disappearance():
    manifest = _load_manifest()

    rule = manifest["program_completion_rule"]

    assert rule["untracked_disappearance_allowed"] is False
    assert "terminal state" in rule["required"]
    assert "successor handoff" in rule["required"]

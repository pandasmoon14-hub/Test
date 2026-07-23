"""Guardrails for the AFQR-01–20 R1A consolidation planning package."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "docs" / "doctrine" / "reviews"
PLAN = REVIEW_DIR / "afqr_01_20_consolidation_r1a_plan.md"
AUTHORITY_INDEX = REVIEW_DIR / "afqr_01_20_authority_index.yaml"
DEPENDENCY_MATRIX = REVIEW_DIR / "afqr_01_20_dependency_matrix.yaml"
MANIFEST = REVIEW_DIR / "afqr_01_20_consolidation_manifest.yaml"

EXPECTED_IDS = [f"AFQR-{index:02d}" for index in range(1, 21)]
EXPECTED_SELECTIONS = {
    "AFQR-01": "Atomic Typed Transition Journal with owner reducers and saga escape hatches",
    "AFQR-02": "Synchronous Command Fast Path with durable attempt escalation",
    "AFQR-03": "Typed Action Gateway with registered semantics",
    "AFQR-04": "Profiled Logical-Time Causal Scheduler",
    "AFQR-05": "Registered Typed Interface-and-Bridge Hypergraph",
    "AFQR-06": "Invariant-Gated Typed Claim Arbitration",
    "AFQR-07": "Typed Balance-Domain Flow Ledger with proof-carrying conversion and atomic settlement",
    "AFQR-08": "Typed Faceted Identity, Continuity, and Lineage Graph",
    "AFQR-09": "Registered Typed Dependency-and-Obligation Hypergraph",
    "AFQR-10": "Typed Bitemporal Truth–Epistemic Provenance Architecture",
    "AFQR-11": "Registered purpose-scoped agency/personhood architecture",
    "AFQR-12": "Registered typed motivational–behavioral state architecture",
    "AFQR-13": "Registered multiplex social-state architecture",
    "AFQR-14": "Bitemporal Communication–Interpretation Architecture",
    "AFQR-15": "Federated institutional–jurisdictional architecture",
    "AFQR-16": "Federated embodiment–integrity architecture",
    "AFQR-17": "Federated environment–process architecture",
    "AFQR-18": "Federated spatiotemporal topology architecture",
    "AFQR-19": "Federated capability–opportunity–targeting–resolution architecture",
    "AFQR-20": "Federated signal–sensing–acquisition architecture",
}


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_r1a_files_exist() -> None:
    for path in (PLAN, AUTHORITY_INDEX, DEPENDENCY_MATRIX, MANIFEST):
        assert path.is_file(), f"missing R1A artifact: {path.relative_to(ROOT)}"


def test_authority_index_registers_exactly_twenty_accepted_selections() -> None:
    data = load_yaml(AUTHORITY_INDEX)
    entries = data["entries"]
    assert [entry["id"] for entry in entries] == EXPECTED_IDS
    assert len(entries) == 20
    assert {
        entry["id"]: entry["selected_architecture"] for entry in entries
    } == EXPECTED_SELECTIONS
    assert all(entry["status"] == "accepted_selection_pending_dossier" for entry in entries)
    assert all(entry["owns"] for entry in entries)
    assert all(entry["must_not_own"] for entry in entries)


def test_r1a_grants_no_downstream_authority() -> None:
    data = load_yaml(AUTHORITY_INDEX)
    for field in (
        "implementation_authority",
        "conversion_authority",
        "canon_authority",
        "model_authority",
        "live_play_authority",
        "r1_complete",
    ):
        assert data[field] is False

    assert data["phase_gates"] == {
        "R0": "complete",
        "R1": "active_incomplete",
        "R2": "blocked_by_R1",
        "R3": "blocked_by_R2",
        "R4": "blocked_by_R3",
        "R5": "blocked_by_R4",
        "R6": "blocked_by_R5",
        "RT-002G": "unauthorized",
    }


def test_dependency_matrix_references_only_registered_afqrs() -> None:
    data = load_yaml(DEPENDENCY_MATRIX)
    valid_ids = data["valid_ids"]
    assert valid_ids == EXPECTED_IDS
    assert set(data["dependencies"]) == set(EXPECTED_IDS)

    for owner, dependencies in data["dependencies"].items():
        assert owner not in dependencies
        assert len(dependencies) == len(set(dependencies))
        assert set(dependencies) <= set(EXPECTED_IDS)


def test_collision_inventory_assigns_a_participating_owner() -> None:
    data = load_yaml(DEPENDENCY_MATRIX)
    seams = data["collision_inventory"]
    seam_ids = [seam["seam_id"] for seam in seams]
    assert len(seam_ids) == len(set(seam_ids))
    assert {
        "command_attempt_vs_action_gateway",
        "action_gateway_vs_capability_resolution",
        "transition_vs_settlement",
        "interface_graph_vs_dependency_graph",
        "signal_vs_epistemic_state",
        "communication_vs_social_state",
        "identity_vs_personhood_vs_embodiment",
        "topology_vs_environment_vs_embodiment",
        "claim_arbitration_vs_jurisdiction",
        "model_context_vs_truth",
    } <= set(seam_ids)

    for seam in seams:
        assert seam["controlling_owner"] in seam["participants"]
        assert set(seam["participants"]) <= set(EXPECTED_IDS)
        assert seam["boundary"]


def test_cycles_have_explicit_breakers_and_rt002g_remains_blocked() -> None:
    data = load_yaml(DEPENDENCY_MATRIX)
    assert len(data["cycle_breakers"]) >= 6
    assert all(item["cycle"] and item["breaker"] for item in data["cycle_breakers"])
    assert all(data["blocked_outputs"].values())
    assert data["blocked_outputs"]["RT-002G"] is True


def test_manifest_requires_bounded_r1b_through_r1e_work() -> None:
    data = load_yaml(MANIFEST)
    assert data["r1_status"] == "active_incomplete"
    assert set(data["planned_artifact_families"]) == {"R1B", "R1C", "R1D", "R1E"}
    assert data["planned_artifact_families"]["R1B"]["required_count"] == 20
    assert data["planned_artifact_families"]["R1B"]["batching_rule"] == "bounded_reviewable_batches"
    assert data["planned_artifact_families"]["R1E"]["exactly_one_output_required"] is True
    assert data["r1_completion_requirements"]["formal_r1e_review_required"] is True
    assert "one_megafile_for_all_twenty_architectures" in data["forbidden_shortcuts"]
    assert "direct_RT-002G_reentry_before_R6" in data["forbidden_shortcuts"]


def test_plan_states_corpus_scale_phase_separation_and_next_step() -> None:
    text = PLAN.read_text(encoding="utf-8")
    required_phrases = (
        "R0 is complete",
        "This artifact does not declare R1 complete",
        "200–400",
        "conversion-runtime origin firewall",
        "RT-002G implementation: unauthorized",
        "R1B — repository-resident AFQR source-dossier reconstruction/import plan",
        "R1B should be split into reviewable batches",
    )
    for phrase in required_phrases:
        assert phrase in text

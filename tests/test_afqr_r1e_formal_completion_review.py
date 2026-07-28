"""Semantic contract tests for the independent AFQR R1E completion gate."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "docs/doctrine/reviews/afqr_01_20_formal_completion_review.md"
BASE = "017984a1598b9c60324c62e54d80372c364654ae"


def load(path: str):
    return json.loads((ROOT / path).read_text())


def contract():
    match = re.search(r"```json\n(.*?)\n```", REVIEW.read_text(), re.S)
    assert match
    return json.loads(match.group(1))


def test_identity_result_and_authority_boundary():
    c = contract()
    assert (c["review_id"], c["phase"], c["result"], c["r1_status"]) == (
        "AFQR-01-20-R1E-FORMAL-COMPLETION-001", "R1E", "pass", "complete")
    assert c["blocking_defects"] == c["unresolved_defects"] == []
    assert c["authority_granted"] == ["formal doctrine completion review and gate adjudication only"]
    assert {"runtime", "conversion", "canon", "model", "live-play", "RT-002G", "temporary evidence deletion"} <= set(c["authority_not_granted"])


def test_r1a_exact_selected_authority_and_existing_paths():
    c, idx = contract(), load("docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml")
    rows = c["r1a_completeness"]["records"]
    assert [x["afqr_id"] for x in rows] == [f"AFQR-{n:02d}" for n in range(1, 21)]
    expected = {x["afqr_id"]: x for x in idx["afqr_records"]}
    assert len(rows) == len(expected) == 20
    for row in rows:
        original = expected[row["afqr_id"]]
        assert row["selected_architecture"] == original["selected_architecture"]
        assert row["selected_primary_evidence_id"] == original["source_evidence_records"][0]
        assert (ROOT / row["selected_primary_source_path"]).is_file()
        assert not row["duplicate_authority_conflict"]
        assert not row["temporary_note_is_owner"] and not row["zip_packaging_is_owner"]
    assert "packaging validates files without ownership transfer" in c["r1a_completeness"]["afqr_14_provenance"]


def test_r1b_exact_coverage_and_historical_preservation():
    c = contract(); vocab = load("docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml")
    assert c["r1b_completeness"]["actual_term_count"] == len(vocab["term_records"]) == 41
    assert c["r1b_completeness"]["reviewed_term_ids"] == [x["term_id"] for x in vocab["term_records"]]
    assert c["r1b_completeness"]["new_unqualified_owners"] == []
    assert not c["r1b_completeness"]["historical_collisions_rewritten"]


def test_r1c_edges_partitions_cycles_risks_and_substrates():
    c = contract(); graph = load("docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml")
    reviews = c["r1c_completeness"]["edge_reviews"]
    assert len(reviews) == len(graph["dependency_edge_dispositions"]) == 94
    assert len({x["edge_id"] for x in reviews}) == 94
    assert c["dependency_edge_partition_summary"] == {
        "core_internal": 33, "agency_internal": 11, "world_internal": 7,
        "core_agency_boundary": 21, "core_world_boundary": 17, "agency_world_boundary": 5}
    source_edges = {x["edge_id"]: x for x in graph["dependency_edge_dispositions"]}
    for row in reviews:
        edge = source_edges[row["edge_id"]]
        assert row["semantic_type_owner"] == edge["semantic_type_owner"]
        assert row["relation_or_handoff_kind"] == edge["relation_or_handoff_kind"]
    assert [x["cycle_id"] for x in c["cycle_decisions"]] == [x["cycle_id"] for x in graph["cycle_risk_resolutions"]]
    assert [x["risk_id"] for x in c["dependency_risk_decisions"]] == [x["reclassification_id"] for x in graph["cycle_risk_reclassifications"]]
    assert [x["substrate_id"] for x in c["missing_substrate_decisions"]] == [x["substrate_id"] for x in graph["missing_substrate_classifications"]]
    assert all(x["decision"] == "accepted_as_classified_deferred_substrate" and x["combined_owner_prohibited"] and x["implementation_status"] == "unimplemented" for x in c["missing_substrate_decisions"])


def test_r1d_parity_and_historical_boundary():
    c = contract()
    assert c["r1d_completeness"] == {"result": "pass", "historical_completion_boundaries_preserved": True, "cross_family_parity": "exact", "r1e_authority_claimed_by_r1d": False}
    assert c["cross_family_parity_summary"] == {"core_agency": 21, "core_world": 17, "agency_world": 5, "result": "pass"}


def test_three_distinct_escalation_adjudications_and_ledgers():
    c = contract(); decisions = {x["collision_id"]: x for x in c["global_escalations"]}
    assert set(decisions) == {"COLL-03", "COLL-08", "COLL-10"}
    for cid, decision in decisions.items():
        assert decision["decision"] in {"approved", "approved_with_qualification", "rejected_and_replaced"}
        assert decision["terms"] and decision["affected_afqrs"] and decision["r1b_evidence_records"]
        assert all((ROOT / p).is_file() for p in decision["primary_source_paths"])
        assert decision["prohibited_inferences"] and decision["final_attribution_rule"]
    assert len({x["final_attribution_rule"] for x in decisions.values()}) == 3
    assert decisions["COLL-08"]["affected_afqrs"] == ["AFQR-09", "AFQR-13", "AFQR-15"]
    for path in ["docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml", "docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml"]:
        ledger = load(path)
        rows = [x for x in ledger["escalations"] if x.get("collision_id") in decisions or set(x.get("collision_ids", [])) & decisions.keys()]
        assert len(rows) == 3 and all(x["status"] == "closed_by_r1e" for x in rows)
        assert all(x["r1e_decision_id"] == f"R1E-{(x.get('collision_ids') or [x['collision_id']])[0]}-DECISION-001" for x in rows)


def test_consistency_corpus_and_gate_state():
    c = contract()
    assert len(c["cross_artifact_consistency_matrix"]) == 13
    assert all(x["result"] == "pass" and not x["contradictions"] and x["authority_transfer_check"] == "pass_no_transfer" for x in c["cross_artifact_consistency_matrix"])
    assert len(c["corpus_scale_adequacy_matrix"]) == 18
    assert all(len(x["lawful_paths"]) == 5 and x["result"] == "pass" for x in c["corpus_scale_adequacy_matrix"])
    assert c["next_lawful_gate"] == "R2 — doctrine-drift resolution"
    assert c["downstream_gate_states"] == {"R2": "ready", "R3": "blocked", "R4": "blocked", "R5": "blocked", "R6": "blocked", "RT-002G": "unauthorized"}


def test_committed_diff_containment_when_commits_exist():
    changed = subprocess.run(["git", "diff", "--name-only", f"{BASE}...HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    forbidden = ("src/", "working/afqr_consolidation_inputs/")
    assert not any(x.startswith(forbidden) for x in changed)
    assert not any(x.lower().endswith((".zip", ".png", ".pdf")) for x in changed)
    deleted = subprocess.run(["git", "diff", "--name-only", "--diff-filter=D", f"{BASE}...HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    assert deleted == []

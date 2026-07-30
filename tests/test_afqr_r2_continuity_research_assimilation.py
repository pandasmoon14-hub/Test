"""Deterministic R2-0 research-assimilation gate."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "docs/doctrine/reviews"
MANIFEST = REVIEWS / "afqr_r2_continuity_research_source_manifest.yaml"
LEDGER = REVIEWS / "afqr_r2_continuity_claim_and_owner_routing_ledger.yaml"
REPORT = REVIEWS / "afqr_r2_continuity_research_assimilation_report.md"
PLAN = ROOT / "docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md"
FILE_MANIFEST = REVIEWS / "afqr_r2_doctrine_drift_file_manifest.yaml"
INTAKE = REVIEWS / "afqr_r2_continuity_research_intake_packet.md"

FAMILIES = {f"CF-{n:02d}" for n in range(1, 14)}
OUTCOMES = {
    "already_governed_by_r1", "partially_governed_r2_qualification_needed",
    "r2_new_doctrine_candidate", "r2_drift_audit_input",
    "r3_conformance_obligation", "r4_runtime_substrate_obligation",
    "r5_runtime_retrofit_obligation", "later_conversion_or_canon_review",
    "later_gm_adapter_input", "evaluation_or_benchmark_input", "deferred_frontier",
    "rejected_as_overengineered", "rejected_as_donor_specific",
    "rejected_as_unsupported", "escalated_owner_question",
}
TARGETS = {"R2A", "R2B-CORE", "R2B-AGENCY", "R2B-WORLD", "R2B-CONTINUITY",
           "R2B-CROSS-PHASE", "R2C", "R3", "R4", "R5", "later", "none"}
R1_FILES = [
    "docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml",
    "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml",
    "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md",
    "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md",
    "docs/doctrine/consolidation/afqr_world_action_sensing.md",
    "docs/doctrine/reviews/afqr_01_20_formal_completion_review.md",
    "docs/doctrine/reviews/afqr_r1e_source_and_vocabulary_audit.yaml",
    "docs/doctrine/reviews/afqr_r1e_dependency_and_parity_audit.yaml",
    "docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml",
    "docs/doctrine/reviews/afqr_r1e_consistency_and_corpus_adequacy.yaml",
]

def load(path: Path) -> dict:
    return json.loads(path.read_text())

def all_values(value, key: str) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for k, child in value.items():
            if k == key and isinstance(child, str): found.add(child)
            found |= all_values(child, key)
    elif isinstance(value, list):
        for child in value: found |= all_values(child, key)
    return found

def test_source_integrity_and_external_posture():
    data = load(MANIFEST); sources = data["sources"]
    assert len(sources) == 5
    assert len({s["source_id"] for s in sources}) == 5
    assert [s["research_family"] for s in sources].count("actual_play_deterministic_patterns") == 1
    assert [s["research_family"] for s in sources].count("branch_aware_continuity") == 4
    for source in sources:
        assert re.fullmatch(r"[0-9a-f]{64}", source["sha256"])
        assert source["byte_size"] > 0 and source["line_count"] > 0
        assert source["authority_posture"] == "nonauthoritative_research_evidence"
        assert source["repository_resident_raw_source"] is False
        assert source["claim_ids"] and source["unique_contributions"]
    repo_names = {p.name for p in ROOT.rglob("*") if p.is_file()}
    assert not {s["original_filename"] for s in sources} & repo_names
    assert INTAKE.exists()

def test_claim_coverage_routes_references_and_owner_analysis():
    data = load(LEDGER); claims = data["claims"]
    assert len(claims) == 30 and len({c["claim_id"] for c in claims}) == 30
    assert {c["claim_family_id"] for c in claims} == FAMILIES
    sources = {s["source_id"] for s in load(MANIFEST)["sources"]}
    vocab = load(ROOT / R1_FILES[0]); deps = load(ROOT / R1_FILES[1])
    terms = all_values(vocab, "term_id"); invs = all_values(deps, "invariant_id")
    edges = all_values(deps, "edge_id"); subs = all_values(deps, "substrate_id")
    for claim in claims:
        assert claim["primary_outcome"] in OUTCOMES
        assert claim["target_work_package"] in TARGETS
        assert claim["proposed_next_action"].strip()
        assert claim["review_status"] == "routed"
        assert {s["source_id"] for s in claim["source_support"]} <= sources
        assert set(claim["afqr_ids"]) <= {f"AFQR-{n:02d}" for n in range(1, 21)}
        assert set(claim["r1b_term_ids"]) <= terms
        assert set(claim["r1c_invariant_ids"]) <= invs
        assert set(claim["r1c_edge_ids"]) <= edges
        assert set(claim["substrate_ids"]) <= subs
        assert claim["owner_analysis"]["prohibited_owner_transfers"]
        if claim["primary_outcome"].startswith("rejected_"):
            assert claim["rejection_rationale"] != "Not applicable."
        if claim["primary_outcome"] == "escalated_owner_question":
            assert claim["owner_analysis"]["unresolved_owner_question"]

def test_consensus_is_computed_without_dissent_inflation():
    for claim in load(LEDGER)["claims"]:
        direct = [s for s in claim["source_support"] if s["support_kind"] != "dissenting"]
        consensus = claim["consensus"]
        assert consensus["supporting_source_count"] == len(direct)
        if consensus["level"] == "unique_source": assert len(direct) == 1
        if consensus["level"] == "unanimous":
            assert len(direct) == consensus["applicable_source_count"]
    normalized = [c["normalized_claim"].casefold() for c in load(LEDGER)["claims"]]
    assert len(normalized) == len(set(normalized))

def test_authority_scope_and_gate_safety():
    text = "\n".join(p.read_text() for p in (MANIFEST, LEDGER, REPORT, PLAN, FILE_MANIFEST))
    assert "nonauthoritative" in text and "tracking_review_only" in text
    assert "SUB-001–SUB-005 remain unimplemented" in text
    for forbidden in ("research_current", "doctrine_consolidation", "doctrine_review"):
        assert forbidden not in text
    report = REPORT.read_text(); plan = PLAN.read_text()
    for phrase in ("R1 remains complete", "R2 is active and incomplete", "R2A is ready and next",
                   "R2B and R2C remain blocked", "RT-002G", "temporary evidence deletion"):
        assert phrase in report
    assert "R2-0 — research assimilation" in plan and "**Status:** `complete`" in plan
    assert "No universal time/truth/evidence/sensing owner" in report

def test_r1_authority_files_match_accepted_baseline():
    # Immutable accepted R1 artifacts are compared to the independently verified R1 commit.
    import subprocess
    for rel in R1_FILES:
        current = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        prior = subprocess.check_output(["git", "show", f"bbc9d58:{rel}"], cwd=ROOT)
        assert current == hashlib.sha256(prior).hexdigest(), rel

def test_bounded_files_and_no_raw_or_binary_payloads():
    limits = {MANIFEST:(600,100*1024), LEDGER:(3500,400*1024), REPORT:(800,120*1024),
              PLAN:(1000,150*1024), FILE_MANIFEST:(800,120*1024)}
    for path,(lines,size) in limits.items():
        raw=path.read_bytes(); assert b"\x00" not in raw
        assert len(raw) <= size and len(raw.splitlines()) <= lines

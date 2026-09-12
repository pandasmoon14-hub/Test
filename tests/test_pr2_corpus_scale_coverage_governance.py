# Executable validation for PR2-CORPUS corpus-scale governance activation.
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/doctrine/control/myravant_corpus_scale_coverage_governance.md"
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
SRC = ROOT / "docs/doctrine/control/myravant_source_research_architecture.md"
SRC_METHOD = ROOT / "docs/doctrine/control/myravant_source_research_method_qualification.md"
ORG = ROOT / "docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md"
IR = ROOT / "docs/doctrine/control/myravant_source_design_information_barrier_contract.md"
IR_CLOSURE_TEST = ROOT / "tests/test_pr2_ir_post_merge_closure.py"

BASE = "92a4b6e15d9df10dedf4cec8bd1267111975cba2"
AUTH = "owner_directive_2026-09-12_pr2_corpus_activation"
EFFECT = "corpus_governance_only"
CONTROL = "docs/doctrine/control/myravant_corpus_scale_coverage_governance.md"
OWNED = {
    "docs/decisions/current_decisions_log.md",
    "docs/doctrine/control/myravant_corpus_scale_coverage_governance.md",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_corpus_scale_coverage_governance.py",
    "tests/test_pr2_ir_post_merge_closure.py",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def test_contract_declares_bounded_authority_and_scale():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "artifact_id: PR2-CORPUS-SCALE-COVERAGE-GOVERNANCE-001" in text
    assert f"authority_reference: {AUTH}" in text
    assert f"starting_baseline: {BASE}" in text
    assert "minimum_external_source_scale: 1000" in text
    for token in (
        "source_acquisition_authority: none",
        "source_processing_authority: none",
        "research_method_authority: none",
        "information_barrier_authority: none",
        "originality_or_rights_authority: none",
        "native_content_authoring_authority: none",
        "canon_authority: none",
        "runtime_authority: none",
        "model_training_authority: none",
        "live_play_authority: none",
    ):
        assert token in text


def test_central_laws_reject_count_frequency_and_global_saturation():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "Source count is not coverage",
        "Source frequency is not doctrine authority",
        "Registration is not research",
        "Genealogical repetition is not independent corroboration",
        "Coverage is multidimensional",
        "Saturation is local, provisional, and reversible",
        "Diminishing novelty does not erase outliers",
        'forbids an unqualified claim that “the corpus is saturated.”',
    ):
        assert token in text


def test_registry_coverage_genealogy_and_batch_surfaces_are_machine_trackable():
    text = CONTRACT.read_text(encoding="utf-8")
    for field in (
        "source_record_id", "source_version_id", "coverage_dimension_values{}",
        "genealogy_cluster_refs[]", "research_unit_refs[]", "coverage_record_id",
        "independent_lineage_refs[]", "unresolved_genealogy_refs[]", "batch_id",
        "target_coverage_gaps[]", "target_genealogy_diversification[]",
        "reserved_outlier_slots[]", "stop_conditions[]", "reopen_conditions[]",
    ):
        assert field in text


def test_novelty_and_saturation_are_separate_reopenable_dimensions():
    text = CONTRACT.read_text(encoding="utf-8")
    for state in (
        "novelty_unassessed", "no_material_novelty", "local_novelty",
        "cross_family_novelty", "outlier_novelty", "contradictory_novelty",
        "novelty_uncertain", "saturation_not_assessed", "insufficient_coverage",
        "declining_novelty_observed", "provisionally_saturated", "saturation_reopened",
    ):
        assert state in text
    assert "No fixed global source count" in text
    assert "Saturation reopening" in text


def test_outlier_bias_and_unknown_evidence_are_preserved():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Outliers are first-class corpus evidence." in text
    assert "A single source may lawfully reveal a project-falsifying edge case." in text
    for state in (
        "bias_not_assessed", "known_skew", "mitigation_planned",
        "mitigation_applied", "accepted_with_rationale", "bias_unknown",
    ):
        assert state in text
    assert "Unknown is a corpus state" in text
    assert "does not authorize circumvention" in text


def test_existing_src_org_ir_owners_remain_authoritative():
    text = CONTRACT.read_text(encoding="utf-8")
    src = SRC.read_text(encoding="utf-8")
    method = SRC_METHOD.read_text(encoding="utf-8")
    org = ORG.read_text(encoding="utf-8")
    ir = IR.read_text(encoding="utf-8")
    assert "the 1,000+ source registry, coverage accounting, genealogy, bias measurement" in src
    assert "corpus registry, quotas, genealogy, cultural-bias accounting, novelty" in method
    assert "`PR2-CORPUS` registry, coverage, genealogy, novelty, saturation, or batching" in org
    assert "source registry, batching, coverage, genealogy, novelty, saturation, or bias" in ir
    assert "PR2-SRC owns research depth and research method." in text
    assert "It must not collapse their states into corpus states." in text
    assert "Design-facing exposure remains governed by PR2-IR." in text


def test_manifest_activates_only_corpus_and_preserves_other_gates():
    manifest = load(MAN)
    by = rows(manifest)
    corpus = by["PR2-CORPUS"]
    assert manifest["artifact_version"] == "0.4.21"
    assert corpus["status"] == "active"
    assert corpus["authorization_reference"] == AUTH
    assert corpus["authority_effect"] == EFFECT
    assert corpus["starting_baseline"] == BASE
    assert corpus["control_artifact"] == CONTROL
    assert set(corpus["owned_paths"]) == OWNED
    assert corpus["pull_request"] is None
    assert corpus["branch_head"] is None
    assert corpus["merge_commit"] is None
    active = {row["workstream_id"] for row in manifest["workstreams"] if row["status"] == "active"}
    assert active == {"PR2-CORPUS"}
    for wid in ("PR2-FICT", "PR2-SIMEX"):
        assert by[wid]["status"] == "ready_pending_authorization"
        assert by[wid]["authorization_reference"] is None
        assert by[wid]["starting_baseline"] is None
    assert by["PR2-IR"]["status"] == "merged"
    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_ir_closure_is_frozen_as_historical_snapshot():
    text = IR_CLOSURE_TEST.read_text(encoding="utf-8")
    assert f'CLOSURE_SNAPSHOT = "{BASE}"' in text
    assert "load_at(CLOSURE_SNAPSHOT, MAN)" in text
    assert "read_at(CLOSURE_SNAPSHOT, PROG)" in text
    assert "read_at(CLOSURE_SNAPSHOT, DEC)" in text


def test_program_and_decision_record_activation_without_execution_authority():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")
    assert "**Artifact version:** `0.4.21`" in program
    assert "### 5.18 PR2-CORPUS corpus-scale coverage-governance activation" in program
    assert AUTH in program
    assert BASE in program
    assert CONTROL in program
    assert "PR2-CORPUS is the only active\nsuccessor workstream" in program
    assert "does not acquire sources, run research packets" in program
    assert "PR2-CORPUS-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASE in decisions
    assert "does not authorize source acquisition" in decisions
    assert "Source count is not coverage." in decisions

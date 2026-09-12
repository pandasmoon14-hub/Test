# Executable validation for PR2-FICT fiction/LitRPG experience-pressure governance.
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/doctrine/control/myravant_fiction_litrpg_experience_pressure_contract.md"
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
SRC = ROOT / "docs/doctrine/control/myravant_source_research_architecture.md"
SRC_METHOD = ROOT / "docs/doctrine/control/myravant_source_research_method_qualification.md"
ORG = ROOT / "docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md"
IR = ROOT / "docs/doctrine/control/myravant_source_design_information_barrier_contract.md"
CORPUS = ROOT / "docs/doctrine/control/myravant_corpus_scale_coverage_governance.md"
CORPUS_CLOSURE_TEST = ROOT / "tests/test_pr2_corpus_post_merge_closure.py"

BASE = "fb9d4596c80ad779f5f58dd4fce066fb7ba797c9"
AUTH = "owner_directive_2026-09-12_pr2_fict_activation"
EFFECT = "research_pressure_governance_only"
CONTROL = "docs/doctrine/control/myravant_fiction_litrpg_experience_pressure_contract.md"
OWNED = {
    "docs/decisions/current_decisions_log.md",
    "docs/doctrine/control/myravant_fiction_litrpg_experience_pressure_contract.md",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_fict_experience_pressure_contract.py",
    "tests/test_pr2_corpus_post_merge_closure.py",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def test_contract_declares_bounded_authority():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "artifact_id: PR2-FICT-EXPERIENCE-PRESSURE-CONTRACT-001" in text
    assert f"authority_reference: {AUTH}" in text
    assert f"authority_effect: {EFFECT}" in text
    assert f"starting_baseline: {BASE}" in text
    for token in (
        "source_acquisition_authority: none",
        "source_processing_authority: none",
        "research_method_authority: none",
        "corpus_governance_authority: none",
        "originality_or_rights_authority: none",
        "information_barrier_authority: none",
        "native_content_authoring_authority: none",
        "canon_authority: none",
        "runtime_authority: none",
        "model_training_authority: none",
        "live_play_authority: none",
    ):
        assert token in text


def test_central_fiction_anti_overclaim_laws_are_explicit():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "Fiction is pressure evidence, not implementation evidence",
        "Source-local depiction is not Myravant law",
        "A plot event is not automatically a stable system rule",
        "Protagonist capability is not player baseline",
        "Narrative omission is not evidence of absence",
        "Narrative desirability is not measured user preference",
        "Narrative possibility is not technical feasibility",
        "Abstraction is not permission to copy",
        "Fiction-derived pressure remains falsifiable",
    ):
        assert token in text


def test_content_nontransfer_is_explicit():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "characters;",
        "plot events or plot arcs;",
        "settings;",
        "signature terminology;",
        "signature power systems;",
        "signature items;",
        "recognizable combinations whose identity depends on the source;",
        "It is not a Myravant-facing deliverable.",
    ):
        assert token in text


def test_lawful_outputs_are_pressure_or_evaluation_only():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "`experience_pressure`",
        "`system_pressure`",
        "`world_behavior_pressure`",
        "`interaction_pressure`",
        "`evaluation_scenario_candidate`",
        "`counterpressure_or_tradeoff`",
        "`outlier_pressure`",
        "`uncertainty_requires_more_research`",
        "`handoff_to_existing_owner`",
        "`escalated_missing_doctrine`",
        "`rejected_invalid_inference`",
    ):
        assert token in text
    assert "They are research outcomes." in text
    assert "They are not Myravant content categories." in text
    assert (
        "Substantive fiction-derived observations therefore still route only to"
        in text
    )
    assert "experience requirements, system pressures, or evaluation-scenario candidates." in text
    assert "donor" not in text.lower()


def test_evaluation_scenario_is_source_independent_not_scene_recreation():
    text = CONTRACT.read_text(encoding="utf-8")
    for field in (
        "evaluation_scenario_candidate_id",
        "experience_condition",
        "world_behavior_condition",
        "observable_success_conditions[]",
        "observable_failure_conditions[]",
        "source_independence_check",
    ):
        assert field in text
    for token in (
        "a recreated scene;",
        "an adventure;",
        "a quest;",
        "a plot outline;",
        "canonical content;",
        "live-play material.",
    ):
        assert token in text


def test_existing_source_governance_owners_remain_authoritative():
    text = CONTRACT.read_text(encoding="utf-8")
    src = SRC.read_text(encoding="utf-8")
    method = SRC_METHOD.read_text(encoding="utf-8")
    org = ORG.read_text(encoding="utf-8")
    ir = IR.read_text(encoding="utf-8")
    corpus = CORPUS.read_text(encoding="utf-8")

    assert "fiction/LitRPG-specific research rules (`PR2-FICT`)" in src
    assert "special\n    interpretation remains reserved to PR2-FICT" in method
    assert "`PR2-FICT` fiction/LitRPG research interpretation" in org
    assert "fiction/LitRPG-specific research interpretation (`PR2-FICT`)" in ir
    assert "fiction/LitRPG-specific interpretation (`PR2-FICT`)" in corpus

    assert "PR2-FICT ends before independent Myravant design begins." in text
    assert "PR2-CORPUS governs portfolio\ncomposition." in text
    assert "PR2-FICT does not redefine the IR handoff payload" in text
    assert "No fiction-specific interpretation rule can waive PR2-ORG review." in text


def test_manifest_activates_only_fict_and_preserves_other_gates():
    manifest = load(MAN)
    by = rows(manifest)
    fict = by["PR2-FICT"]

    assert manifest["artifact_version"] == "0.4.23"
    assert fict["status"] == "active"
    assert fict["authorization_reference"] == AUTH
    assert fict["authority_effect"] == EFFECT
    assert fict["starting_baseline"] == BASE
    assert fict["control_artifact"] == CONTROL
    assert set(fict["owned_paths"]) == OWNED
    assert fict["pull_request"] is None
    assert fict["branch_head"] is None
    assert fict["merge_commit"] is None

    active = {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    }
    assert active == {"PR2-FICT"}

    assert by["PR2-CORPUS"]["status"] == "merged"
    assert by["PR2-SIMEX"]["status"] == "ready_pending_authorization"
    assert by["PR2-SIMEX"]["authorization_reference"] is None
    assert by["PR2-SIMEX"]["starting_baseline"] is None

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_corpus_closure_is_frozen_as_historical_snapshot():
    text = CORPUS_CLOSURE_TEST.read_text(encoding="utf-8")
    assert f'CLOSURE_SNAPSHOT = "{BASE}"' in text
    assert "load_at(CLOSURE_SNAPSHOT, MAN)" in text
    assert "read_at(CLOSURE_SNAPSHOT, PROG)" in text
    assert "read_at(CLOSURE_SNAPSHOT, DEC)" in text


def test_program_and_decision_record_activation_without_execution_authority():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")

    assert "**Artifact version:** `0.4.23`" in program
    assert "### 5.20 PR2-FICT fiction/LitRPG experience-pressure activation" in program
    assert AUTH in program
    assert BASE in program
    assert CONTROL in program
    assert "PR2-FICT is the only active successor workstream." in program
    assert "does not acquire sources, run fiction research packets" in program
    assert "PR2-SIMEX remains" in program

    assert "PR2-FICT-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASE in decisions
    assert "does not authorize source acquisition" in decisions
    assert "Fictional depiction is\nnot implementation evidence" in decisions

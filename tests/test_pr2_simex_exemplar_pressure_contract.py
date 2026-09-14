# Executable validation for PR2-SIMEX exemplar-pressure governance.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/doctrine/control/myravant_simulation_infrastructure_exemplar_pressure_contract.md"
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
SRC = ROOT / "docs/doctrine/control/myravant_source_research_architecture.md"
SRC_METHOD = ROOT / "docs/doctrine/control/myravant_source_research_method_qualification.md"
ORG = ROOT / "docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md"
IR = ROOT / "docs/doctrine/control/myravant_source_design_information_barrier_contract.md"
CORPUS = ROOT / "docs/doctrine/control/myravant_corpus_scale_coverage_governance.md"
FICT_CLOSURE_TEST = ROOT / "tests/test_pr2_fict_post_merge_closure.py"

BASE = "302732db03175726de2cdd7c24e78eb257520083"
AUTH = "owner_directive_2026-09-13_pr2_simex_activation"
EFFECT = "architecture_pressure_governance_only"
CONTROL = "docs/doctrine/control/myravant_simulation_infrastructure_exemplar_pressure_contract.md"
MERGE = "5c48a8e4393374dba3f9f2edc5541c1bb75906f4"
OWNED = {
    "docs/decisions/current_decisions_log.md",
    "docs/doctrine/control/myravant_simulation_infrastructure_exemplar_pressure_contract.md",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_simex_exemplar_pressure_contract.py",
    "tests/test_pr2_fict_post_merge_closure.py",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def read_at(ref, path):
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path.relative_to(ROOT).as_posix()}"],
        cwd=ROOT,
        text=True,
    )


def load_at(ref, path):
    return json.loads(read_at(ref, path))


def test_contract_declares_bounded_authority():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "artifact_id: PR2-SIMEX-SIMULATION-INFRASTRUCTURE-EXEMPLAR-PRESSURE-001" in text
    assert f"authority_reference: {AUTH}" in text
    assert f"authority_effect: {EFFECT}" in text
    assert f"starting_baseline: {BASE}" in text
    for token in (
        "source_acquisition_authority: none",
        "source_processing_authority: none",
        "research_method_authority: none",
        "corpus_selection_authority: none",
        "originality_or_rights_authority: none",
        "information_barrier_authority: none",
        "runtime_architecture_decision_authority: none",
        "runtime_implementation_authority: none",
        "production_schema_authority: none",
        "native_content_authoring_authority: none",
        "canon_authority: none",
        "model_training_authority: none",
        "live_play_authority: none",
    ):
        assert token in text


def test_central_anti_prescription_laws_are_explicit():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "Exemplar implementation is evidence, not prescription",
        "Observed success is conditional evidence, not universal best practice",
        "Observed failure is a bounded pressure, not a universal prohibition",
        "Mechanism is not requirement",
        "Scale does not transfer without context",
        "Benchmark performance is not world-simulation proof",
        "Physical topology does not define semantic authority",
        "Technology popularity is not architecture authority",
        "Copying a stack does not reproduce its results",
        "Missing implementation detail remains unknown",
        "Exemplar pressure remains falsifiable",
    ):
        assert token in text


def test_property_mechanism_and_context_remain_distinct():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "demonstrated property",
        "observed mechanism",
        "operating envelope",
        "tradeoffs and costs",
        "normalized pressure",
        "evaluation need",
        "workload_context",
        "scale_context",
        "topology_context",
        "state_and_consistency_context",
        "portability_assumptions[]",
        "nonportable_assumptions[]",
    ):
        assert token in text


def test_scale_and_benchmark_overclaim_is_forbidden():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "directly observed scale;",
        "benchmarked scale;",
        "production-reported scale;",
        "design-target scale;",
        "extrapolated scale;",
        "theoretical limit;",
        "architecture ceiling;",
        "unknown ceiling.",
        "Entity count does not prove interactive-agent count.",
        "Batch simulation throughput does not prove low-latency player-facing behavior.",
    ):
        assert token in text


def test_specific_technologies_are_not_defaults():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "Myravant should use microservices",
        "Myravant should use an ECS",
        "Myravant should use event sourcing",
        "Myravant should shard by geography",
        "Myravant should use the same database",
    ):
        assert token in text
    assert "Statements such as these are invalid SIMEX conclusions:" in text


def test_lawful_outputs_are_pressure_or_evaluation_not_runtime_decisions():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "`architecture_pressure`",
        "`evaluation_scenario_candidate`",
        "`counterpressure_or_tradeoff`",
        "`uncertainty_requires_more_research`",
        "`handoff_to_existing_owner`",
        "`escalated_missing_doctrine`",
        "`rejected_invalid_inference`",
    ):
        assert token in text
    assert "SIMEX outputs are research outcomes." in text
    assert "They are not Myravant runtime decisions." in text
    assert "PR2-SIMEX ends before Myravant runtime architecture begins." in text
    assert "PR2-SIMEX does not activate PR2-SCALE." in text


def test_existing_governance_owners_remain_authoritative():
    text = CONTRACT.read_text(encoding="utf-8")
    src = SRC.read_text(encoding="utf-8")
    method = SRC_METHOD.read_text(encoding="utf-8")
    org = ORG.read_text(encoding="utf-8")
    ir = IR.read_text(encoding="utf-8")
    corpus = CORPUS.read_text(encoding="utf-8")

    assert "simulation/infrastructure exemplar-specific research rules (`PR2-SIMEX`)" in src
    assert "simulation/infrastructure exemplar-specific interpretation (`PR2-SIMEX`)" in method
    assert "`PR2-SIMEX` simulation/infrastructure exemplar interpretation" in org
    assert "simulation/infrastructure exemplar interpretation (`PR2-SIMEX`)" in ir
    assert "simulation/infrastructure exemplar-specific interpretation (`PR2-SIMEX`)" in corpus

    assert "PR2-CORPUS governs the research portfolio." in text
    assert "PR2-SIMEX does not create a competing research method." in text
    assert "PR2-SIMEX does not redefine the PR2-IR handoff payload." in text
    assert "No SIMEX rule can waive PR2-ORG review" in text


def test_manifest_activates_only_simex_and_preserves_runtime_gates():
    manifest = load_at(MERGE, MAN)
    by = rows(manifest)
    simex = by["PR2-SIMEX"]

    assert manifest["artifact_version"] == "0.4.25"
    assert simex["status"] == "active"
    assert simex["authorization_reference"] == AUTH
    assert simex["authority_effect"] == EFFECT
    assert simex["starting_baseline"] == BASE
    assert simex["control_artifact"] == CONTROL
    assert set(simex["owned_paths"]) == OWNED
    assert simex["pull_request"] is None
    assert simex["branch_head"] is None
    assert simex["merge_commit"] is None

    active = {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    }
    assert active == {"PR2-SIMEX"}

    assert by["PR2-FICT"]["status"] == "merged"
    assert by["PR2-SCALE"]["status"] == "blocked"
    assert by["PR2-SCALE"]["authorization_reference"] is None
    assert by["PR2-SCALE"]["starting_baseline"] is None

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_fict_closure_is_frozen_as_historical_snapshot():
    text = FICT_CLOSURE_TEST.read_text(encoding="utf-8")
    assert f'CLOSURE_SNAPSHOT = "{BASE}"' in text
    assert text.count("load_at(CLOSURE_SNAPSHOT, MAN)") == 2
    assert "read_at(CLOSURE_SNAPSHOT, PROG)" in text
    assert "read_at(CLOSURE_SNAPSHOT, DEC)" in text


def test_program_and_decision_record_activation_without_design_authority():
    program = read_at(MERGE, PROG)
    decisions = read_at(MERGE, DEC)

    assert "**Artifact version:** `0.4.25`" in program
    assert "### 5.22 PR2-SIMEX simulation/infrastructure exemplar-pressure activation" in program
    assert AUTH in program
    assert BASE in program
    assert CONTROL in program
    assert "PR2-SIMEX is the only active successor workstream." in program
    assert "PR2-SCALE remains `blocked` and unauthorized." in program

    assert "PR2-SIMEX-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASE in decisions
    assert "does not authorize exemplar research execution" in decisions
    assert "does not activate PR2-SCALE" in decisions

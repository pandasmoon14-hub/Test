# Executable validation for PR2-SRC-B heterogeneous research-method qualification.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCTRINE = ROOT / "docs/doctrine/control/myravant_source_research_method_qualification.md"
DOCTRINE_A = ROOT / "docs/doctrine/control/myravant_source_research_architecture.md"
MANIFEST = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROGRAM = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"

BASELINE = "818a79d03ac487722762a44c9a80b29391278a8f"
AUTH = "owner_directive_2026-09-11_pr2_src_b_activation"
EFFECT = "heterogeneous_source_research_method_qualification_only"
SRC_A_HEAD = "ac82cebeeb3b8eb63fc6b4a312e90554584a1d32"
SRC_A_PR = 382
SRC_B_MERGE = "70f7195100d0ccb7ba3c4cbd0dc34d684717ccaa"

CURRENT_PATHS = {
    "docs/doctrine/control/myravant_source_research_method_qualification.md",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "docs/decisions/current_decisions_log.md",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_src_source_research_architecture.py",
    "tests/test_pr2_src_research_method_qualification.py",
}

BLOCKED = {
    "PR2-ORG", "PR2-CORPUS", "PR2-IR", "PR2-FICT", "PR2-SIMEX",
    "PR2-SCALE", "PR2-PART", "PR2-CONC", "PR2-FID", "PR2-EVENT",
    "PR2-PERSIST", "PR2-BP", "PR2-AUDIT", "PR2-MIG", "PR2-TEST",
    "PR2-IMPL",
}


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load_manifest_at(ref):
    return json.loads(git("show", f"{ref}:{MANIFEST.relative_to(ROOT).as_posix()}"))


def read_text_at(ref, path):
    return git("show", f"{ref}:{path.relative_to(ROOT).as_posix()}")


def by_id(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def test_src_b_declares_bounded_method_authority():
    text = DOCTRINE.read_text(encoding="utf-8")
    assert "artifact_id: PR2-SRC-B-RESEARCH-METHOD-QUALIFICATION-001" in text
    assert f"authority_reference: {AUTH}" in text
    assert f"authority_effect: {EFFECT}" in text
    assert f"starting_baseline: {BASELINE}" in text
    assert "bulk_source_processing_authority: none" in text
    assert "agent_execution_authority: none" in text
    assert "native_content_authority: none" in text
    assert "live_play_authority: none" in text


def test_src_b_qualifies_modalities_without_making_them_authority_classes():
    text = DOCTRINE.read_text(encoding="utf-8")
    for term in [
        "rules-heavy", "content-heavy/catalog", "generator-heavy/procedural",
        "toolkit/point-buy/framework", "setting/world-heavy",
        "scenario/adventure/campaign", "solo/GM-less/oracle",
        "implementation/software", "failure/postmortem", "actual-use/community",
        "empirical/research", "ordinary-life/institutional",
        "narrative/fiction pressure", "simulation/infrastructure pressure",
    ]:
        assert term in text
    assert "They are multi-label rather than mutually exclusive." in text
    assert "Modality labels do not imply equal evidentiary strength." in text


def test_src_b_preserves_evidence_modes_and_claim_discipline():
    text = DOCTRINE.read_text(encoding="utf-8")
    for term in [
        "observed implementation", "documented design intent", "observed use",
        "empirical finding", "failure or incident evidence",
        "community report or hypothesis", "inferred rationale",
        "historical evolution evidence",
    ]:
        assert term in text
    assert "SRC-B does not assign universal numeric confidence scores." in text
    assert "A community assertion may be useful as a hypothesis" in text
    assert "Documentation may describe intent without proving implementation." in text


def test_src_b_defines_selective_research_depth():
    text = DOCTRINE.read_text(encoding="utf-8")
    for heading in ["### 8.1 Scout", "### 8.2 Focused analysis", "### 8.3 Deep analysis", "### 8.4 Cross-source synthesis"]:
        assert heading in text
    assert "No source family is automatically entitled to deep analysis." in text
    assert "Research should maximize validated information yield rather than pages read." in text
    assert "SRC-B does not define corpus quotas or saturation thresholds." in text


def test_src_b_preserves_mechanical_ecology_and_utilization():
    text = DOCTRINE.read_text(encoding="utf-8")
    for term in ["actors;", "targets;", "prerequisites;", "resources;", "consequences;", "institutions;", "information availability;", "lifecycle;", "scale;", "unusual uses;", "emergent combinations;"]:
        assert term in text
    assert "capability existence from capability use" in text
    assert "Breadth is therefore not raw option count." in text


def test_src_b_content_and_generator_methods_preserve_structure_not_inventory():
    text = DOCTRINE.read_text(encoding="utf-8")
    assert "instance\n-> family\n-> differentiating dimensions" in text
    assert "reusable generative understanding" in text
    assert "The method must not convert a large catalog into a large Myravant catalog" in text
    assert "A generator should be studied for the possibility structure it encodes." in text
    assert "A table row is not automatically a content artifact." in text


def test_src_b_rules_in_use_failure_and_software_methods_are_explicit():
    text = DOCTRINE.read_text(encoding="utf-8")
    assert "published intent\n-> implemented rule\n-> actual use" in text
    assert "Failure evidence is first-class research evidence." in text
    assert "implementation/code shows what one implementation actually does" in text
    assert "README and architecture documents show intended or claimed design" in text
    assert "Repository popularity is not architecture authority." in text


def test_src_b_includes_ordinary_life_without_forcing_game_mechanics():
    text = DOCTRINE.read_text(encoding="utf-8")
    assert "Ordinary-life research must not be forced through an adventure-mechanic lens." in text
    assert "It is not an instruction to create a mechanic for every observed institution." in text


def test_src_b_packet_contract_is_reconstructible_and_nonexecuting():
    text = DOCTRINE.read_text(encoding="utf-8")
    for field in [
        "`packet_id`", "research question or objective",
        "source identity and provenance locator", "bounded read scope",
        "source modality labels", "requested research mode",
        "lawful output classes", "prohibited output classes",
        "stop conditions", "escalation conditions", "acceptance checks",
        "durable checkpoint/output location",
    ]:
        assert field in text
    assert "reconstructible without relying on one agent's hidden or" in text
    assert "This is a packet contract, not packet-execution authorization." in text


def test_src_b_escalates_instead_of_absorbing_successor_authority():
    text = DOCTRINE.read_text(encoding="utf-8")
    for workstream in ["`PR2-ORG`", "`PR2-IR`", "`PR2-CORPUS`", "`PR2-FICT`", "`PR2-SIMEX`", "`PR2-SRC-C`", "`PR2-SRC-D`"]:
        assert workstream in text
    assert "SRC-B must not solve an escalation by quietly broadening its own scope." in text
    assert "agent_execution_authority: none" in text
    assert "No source corpus processing is authorized by this file." in text


def test_src_b_manifest_state_is_exact_and_downstream_stays_blocked():
    manifest = load_manifest_at(SRC_B_MERGE)
    rows = by_id(manifest)
    src = rows["PR2-SRC"]
    tr = {row["tranche_id"]: row for row in src["planned_tranches"]}
    assert manifest["artifact_version"] == "0.4.13"
    assert src["status"] == "active"
    assert src["current_tranche"] == "PR2-SRC-B"
    assert src["tranche_authority_effect"] == EFFECT
    assert src["current_tranche_starting_head"] == BASELINE
    assert src["current_tranche_authorization_reference"] == AUTH
    assert set(src["current_tranche_owned_paths"]) == CURRENT_PATHS
    assert src["next_tranche_authorized"] is False
    assert tr["PR2-SRC-A"]["state"] == "merged"
    assert tr["PR2-SRC-A"]["pull_request"] == SRC_A_PR
    assert tr["PR2-SRC-A"]["branch_head"] == SRC_A_HEAD
    assert tr["PR2-SRC-A"]["merge_commit"] == BASELINE
    assert tr["PR2-SRC-B"]["state"] == "active"
    assert tr["PR2-SRC-B"]["authorization_reference"] == AUTH
    assert tr["PR2-SRC-B"]["authority_effect"] == EFFECT
    assert tr["PR2-SRC-B"]["starting_baseline"] == BASELINE
    assert tr["PR2-SRC-C"]["state"] == "blocked_pending_separate_authorization"
    assert tr["PR2-SRC-D"]["state"] == "blocked_pending_separate_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False
    for wid in BLOCKED:
        assert rows[wid]["status"] == "blocked"
        assert rows[wid]["authorization_reference"] is None


def test_src_b_program_and_decision_log_cross_record_activation():
    program = read_text_at(SRC_B_MERGE, PROGRAM)
    decisions = read_text_at(SRC_B_MERGE, DECISIONS)
    assert "**Artifact version:** `0.4.13`" in program
    assert "### 5.10 PR2-SRC-B heterogeneous research-method qualification" in program
    assert "`PR2-SRC` remains `active` with current tranche `PR2-SRC-B`" in program
    assert AUTH in program and BASELINE in program and SRC_A_HEAD in program
    assert "PR2-SRC-B-ACTIVATION-001" in decisions
    assert AUTH in decisions and EFFECT in decisions and BASELINE in decisions
    assert "PR2-SRC-C and PR2-SRC-D remain separately unauthorized." in decisions


def test_src_b_preserves_src_a_as_foundational_authority():
    a = DOCTRINE_A.read_text(encoding="utf-8")
    b = DOCTRINE.read_text(encoding="utf-8")
    assert "PR2-SRC-A-SOURCE-RESEARCH-ARCHITECTURE-001" in a
    assert "inherits:" in b
    assert "PR2-SRC-A-SOURCE-RESEARCH-ARCHITECTURE-001" in b
    assert "source-research architecture established by PR2-SRC-A" in b

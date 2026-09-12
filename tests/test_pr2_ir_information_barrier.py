# Executable validation for PR2-IR information-barrier activation.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/doctrine/control/myravant_source_design_information_barrier_contract.md"
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
SRC = ROOT / "docs/doctrine/control/myravant_source_research_architecture.md"
SRC_METHOD = ROOT / "docs/doctrine/control/myravant_source_research_method_qualification.md"
ORG = ROOT / "docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md"
FIREWALL = ROOT / "docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md"
ORG_CLOSURE_TEST = ROOT / "tests/test_pr2_org_post_merge_closure.py"

BASE = "8e2ba57ad61aac366e2d34c47811a3d17fd59220"
AUTH = "owner_directive_2026-09-11_pr2_ir_activation"
EFFECT = "information_barrier_and_representation_contract_only"
CONTROL = "docs/doctrine/control/myravant_source_design_information_barrier_contract.md"
OWNED = {
    "docs/decisions/current_decisions_log.md",
    "docs/doctrine/control/myravant_source_design_information_barrier_contract.md",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_ir_information_barrier.py",
    "tests/test_pr2_org_post_merge_closure.py",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def test_contract_declares_bounded_authority():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "artifact_id: PR2-IR-SOURCE-DESIGN-INFORMATION-BARRIER-001" in text
    assert f"authority_reference: {AUTH}" in text
    assert f"authority_effect: {EFFECT}" in text
    assert f"starting_baseline: {BASE}" in text
    for token in (
        "source_research_authority: none",
        "corpus_governance_authority: none",
        "originality_or_rights_authority: none",
        "native_content_authoring_authority: none",
        "canon_promotion_authority: none",
        "runtime_authority: none",
        "production_schema_authority: none",
        "model_training_authority: none",
        "live_play_authority: none",
    ):
        assert token in text


def test_three_planes_and_payload_separation_are_explicit():
    text = CONTRACT.read_text(encoding="utf-8")
    for heading in (
        "### 4.1 Source-aware research plane",
        "### 4.2 Governance bridge plane",
        "### 4.3 Myravant design plane",
        "## 6. Default design-handoff payload",
        "## 7. Governance-only handoff record",
    ):
        assert heading in text
    assert "A governance record may know more than the design payload." in text
    assert "They are not automatically part of the design-facing payload." in text


def test_barrier_rejects_rewrite_as_independence_and_source_shaped_payloads():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Paraphrase is not a barrier" in text
    assert "magic wording-distance or similarity-score threshold" in text
    for token in (
        "source titles, authors, publishers",
        "source-specific proper nouns or signature terminology",
        "source-format stat blocks, tables, catalogs",
        "one-to-one source construct inventories",
        "source ordering or distinctive source taxonomy",
        "source-signature numeric packages",
        "donor-to-Myravant mappings or conversion notes",
        "source-aware retrieval indexes or embeddings",
    ):
        assert token in text


def test_machine_trackable_handoff_contract_is_not_eligibility_or_runtime_state():
    text = CONTRACT.read_text(encoding="utf-8")
    for field in (
        "handoff_record_id",
        "requirement_id",
        "upstream_pressure_refs[]",
        "upstream_synthesis_refs[]",
        "research_provenance_refs[]",
        "source_exposure_state",
        "single_source_dependency_state",
        "withheld_information_classes[]",
        "prohibited_cue_check",
        "handoff_disposition",
        "review_decision_ref",
    ):
        assert field in text
    for disposition in (
        "handoff_allowed",
        "handoff_allowed_with_constraints",
        "handoff_deferred_for_synthesis",
        "handoff_blocked_source_expression",
        "handoff_blocked_source_shaped_structure",
        "handoff_requires_org_review",
        "handoff_escalated",
    ):
        assert disposition in text
    assert "These are information-barrier dispositions, not originality, rights" in text
    assert "PR2-IR is not runtime IR" in text


def test_context_separation_is_real_not_prompt_only():
    text = CONTRACT.read_text(encoding="utf-8")
    assert 'A prompt saying “ignore the source material above” is not an information\nbarrier.' in text
    assert "separately bounded design context" in text
    for token in (
        "retrieved source chunks",
        "source research transcripts",
        "source-bearing attachments",
        "source-aware vector or retrieval indexes",
        "research-only connector access",
        "research tool state",
    ):
        assert token in text
    assert "hidden, ephemeral, or unrecoverable\ncontext" in text


def test_cross_source_default_preserves_single_source_outliers():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Cross-source synthesis is the normal research-to-requirement route" in text
    assert "A requirement may lawfully depend on one source" in text
    assert "single_source_dependency_state" in text
    assert "does not require fake cross-source consensus" in text


def test_breach_preserves_evidence_and_routes_to_org():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "record a barrier breach rather than pretending the material can be\n“unseen.”" in text
    assert "contamination_review_required" in text
    assert "does not erase the exposure event or prove originality" in text
    assert "PR2-ORG remains the owner" in text


def test_existing_src_org_and_runtime_owners_remain_authoritative():
    text = CONTRACT.read_text(encoding="utf-8")
    src = SRC.read_text(encoding="utf-8")
    method = SRC_METHOD.read_text(encoding="utf-8")
    org = ORG.read_text(encoding="utf-8")
    firewall = FIREWALL.read_text(encoding="utf-8")

    assert "external evidence -> source-aware observation -> normalized pressure" in src
    assert "source-analysis/design information barrier | `PR2-IR`" in method
    assert "PR2-IR will own the explicit representation and information-flow barrier" in org
    assert "Extraction and conversion end before runtime begins." in firewall
    assert "The existing conversion/runtime origin firewall remains authoritative." in text
    assert "Passing PR2-IR does not create canonical identity or runtime eligibility." in text


def test_manifest_activates_only_ir_and_preserves_all_other_gates():
    manifest = load(MAN)
    by = rows(manifest)
    ir = by["PR2-IR"]

    assert manifest["artifact_version"] == "0.4.19"
    assert ir["status"] == "active"
    assert ir["authorization_reference"] == AUTH
    assert ir["authority_effect"] == EFFECT
    assert ir["starting_baseline"] == BASE
    assert ir["control_artifact"] == CONTROL
    assert set(ir["owned_paths"]) == OWNED
    assert ir["pull_request"] is None
    assert ir["branch_head"] is None
    assert ir["merge_commit"] is None

    active = {row["workstream_id"] for row in manifest["workstreams"] if row["status"] == "active"}
    assert active == {"PR2-IR"}

    for wid in ("PR2-CORPUS", "PR2-FICT", "PR2-SIMEX"):
        assert by[wid]["status"] == "ready_pending_authorization"
        assert by[wid]["authorization_reference"] is None

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_org_closure_test_is_frozen_against_its_merged_snapshot():
    text = ORG_CLOSURE_TEST.read_text(encoding="utf-8")
    assert 'CLOSURE_SNAPSHOT="8e2ba57ad61aac366e2d34c47811a3d17fd59220"' in text
    assert "load_at(CLOSURE_SNAPSHOT,MAN)" in text
    assert "read_at(CLOSURE_SNAPSHOT,PROG)" in text
    assert "read_at(CLOSURE_SNAPSHOT,DEC)" in text


def test_program_and_decision_record_activation_without_downstream_authority():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")

    assert "**Artifact version:** `0.4.19`" in program
    assert "### 5.16 PR2-IR source-analysis / Myravant-design information-barrier activation" in program
    assert AUTH in program
    assert BASE in program
    assert CONTROL in program
    assert "PR2-IR is the only active\nsuccessor workstream" in program

    assert "PR2-IR-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASE in decisions
    assert "does not authorize source acquisition" in decisions

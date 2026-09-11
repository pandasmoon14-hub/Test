"""Executable validation for PR2-SRC-A foundational source research governance."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DOCTRINE = ROOT / "docs/doctrine/control/myravant_source_research_architecture.md"
MANIFEST = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROGRAM = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
FIREWALL = ROOT / "docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md"

BASELINE = "4033f43b2a4ad7088955ca1a29daf47a33ef7a37"
AUTH = "owner_directive_2026-09-10_pr2_src_a_activation"
EFFECT = "foundational_source_research_governance_only"

OWNED_PATHS = {
    "docs/doctrine/control/myravant_source_research_architecture.md",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "docs/decisions/current_decisions_log.md",
    "tests/test_pr2_src_source_research_architecture.py",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_id_myravant_identity_migration.py",
    "tests/test_pr2_id_t2b_doctrine_identity_migration.py",
    "tests/test_pr2_id_t2c_noncurrent_surface_retention.py",
    "tests/test_pr2_id_t2d_roadmap_registry_adjudication.py",
    "tests/test_pr2_id_t2e_completion_recording.py",
    "tests/test_pr2_id_post_merge_closure.py",
    "tests/test_afqr_r2c_formal_completion_review.py",
}

BLOCKED = {
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


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def by_id(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def test_src_a_control_artifact_exists_and_declares_bounded_authority():
    text = DOCTRINE.read_text(encoding="utf-8")

    assert "artifact_id: PR2-SRC-A-SOURCE-RESEARCH-ARCHITECTURE-001" in text
    assert f"authority_reference: {AUTH}" in text
    assert f"authority_effect: {EFFECT}" in text
    assert f"starting_baseline: {BASELINE}" in text
    assert "runtime_authority: none" in text
    assert "canon_authority: none" in text
    assert "conversion_execution_authority: none" in text
    assert "native_content_authority: none" in text
    assert "live_play_authority: none" in text


def test_src_a_pipeline_preserves_research_layer_separation():
    text = DOCTRINE.read_text(encoding="utf-8")

    for term in [
        "external source / evidence",
        "source-aware observation",
        "normalized pressure",
        "cross-source synthesis",
        "Myravant-facing requirement",
        "Myravant design",
    ]:
        assert term in text

    assert "Each arrow is a boundary, not a rename operation." in text
    assert "Pressure is evidence, not doctrine." in text
    assert "paraphrase does not create independence" in text
    assert "terminology replacement does not create independence" in text
    assert "combining multiple source expressions does not automatically create" in text


def test_src_a_is_source_modality_neutral_and_corpus_scale():
    text = DOCTRINE.read_text(encoding="utf-8")

    for term in [
        "rules-heavy game material",
        "content-heavy catalogs and bestiaries",
        "generator-heavy tables and procedural systems",
        "fiction and actual play",
        "empirical research",
        "software documentation and implementations",
        "repositories, issue histories, postmortems, and failure reports",
        "ordinary-life institutions and practices",
    ]:
        assert term in text

    assert "at least 1,000 heterogeneous sources" in text
    assert "source prevalence must not be treated as Myravant-world prevalence" in text
    assert "one source must not imply one Myravant artifact" in text


def test_src_a_requires_functional_and_generative_abstraction():
    text = DOCTRINE.read_text(encoding="utf-8")

    assert "content instance" in text
    assert "content family" in text
    assert "generative dimensions" in text
    assert "generation grammar / coherence relationships" in text
    assert "A source table with one hundred rows does not create one hundred Myravant" in text
    assert "A bestiary does not imply renamed Myravant creatures." in text
    assert "Raw entry count is not a valid proxy for structural breadth." in text


def test_src_a_preserves_failure_rules_in_use_and_evidence_mode_pressure():
    text = DOCTRINE.read_text(encoding="utf-8")

    for term in [
        "observed implementation",
        "reported user behavior",
        "failure or incident evidence",
        "empirical findings",
        "community reports or hypotheses",
        "abandoned or superseded approaches",
        "published design",
        "actual use",
        "emergent strategy",
        "exploit or failure",
    ]:
        assert term in text

    assert "Weak evidence must not become indistinguishable from stronger direct evidence" in text


def test_src_a_manifest_activation_is_exact():
    manifest = load_manifest()
    rows = by_id(manifest)
    src = rows["PR2-SRC"]

    assert manifest["artifact_version"] == "0.4.12"
    assert src["status"] == "active"
    assert src["authorization_reference"] == AUTH
    assert src["authority_effect"] == EFFECT
    assert src["starting_baseline"] == BASELINE
    assert set(src["owned_paths"]) == OWNED_PATHS
    assert src["current_tranche"] == "PR2-SRC-A"
    assert src["tranche_control_artifact"] == (
        "docs/doctrine/control/myravant_source_research_architecture.md"
    )
    assert src["current_tranche_starting_head"] == BASELINE
    assert src["current_tranche_authorization_reference"] == AUTH
    assert src["next_tranche_authorized"] is False
    assert [row["state"] for row in src["planned_tranches"]] == [
        "active",
        "blocked_pending_separate_authorization",
        "blocked_pending_separate_authorization",
        "blocked_pending_separate_authorization",
    ]


def test_src_a_does_not_activate_r3_or_downstream_work():
    manifest = load_manifest()
    rows = by_id(manifest)

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["status"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False

    for wid in BLOCKED:
        assert rows[wid]["status"] == "blocked"
        assert rows[wid]["authorization_reference"] is None

    assert set(rows["PR2-AUDIT"]["dependencies"]) == {
        "PR2-ID",
        "PR2-SRC",
        "PR2-ORG",
        "PR2-CORPUS",
        "PR2-IR",
        "PR2-SCALE",
    }


def test_src_a_preserves_firewall_as_complementary_authority():
    doctrine = DOCTRINE.read_text(encoding="utf-8")
    firewall = FIREWALL.read_text(encoding="utf-8")

    assert "conversion_runtime_origin_firewall_doctrine.md" in doctrine
    assert "complements, and does not replace" in doctrine
    assert "status: active_control_doctrine" in firewall
    assert "Extraction and conversion end before runtime begins." in firewall


def test_src_a_program_and_decision_log_cross_record_authorization():
    program = PROGRAM.read_text(encoding="utf-8")
    decisions = DECISIONS.read_text(encoding="utf-8")

    assert "**Artifact version:** `0.4.12`" in program
    assert "### 5.9 PR2-SRC-A foundational source research governance" in program
    assert "`PR2-SRC` is `active` in foundational tranche `PR2-SRC-A`" in program
    assert AUTH in program
    assert BASELINE in program

    assert "PR2-SRC-A-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASELINE in decisions
    assert "discussion archives informed the pressure analysis" in decisions


def test_src_a_reserves_later_tranches_without_authorizing_them():
    doctrine = DOCTRINE.read_text(encoding="utf-8")
    manifest = load_manifest()
    src = by_id(manifest)["PR2-SRC"]

    for tranche in ["PR2-SRC-B", "PR2-SRC-C", "PR2-SRC-D"]:
        assert tranche in doctrine

    assert "SRC-A does not authorize SRC-B." in doctrine
    assert "SRC-A does not authorize SRC-C." in doctrine
    assert "SRC-A does not authorize SRC-D." in doctrine
    assert src["next_tranche_authorized"] is False


def test_src_a_does_not_absorb_org_ir_corpus_or_content_authority():
    text = DOCTRINE.read_text(encoding="utf-8")

    assert "originality, rights, similarity, or distribution-eligibility adjudication" in text
    assert "final source-analysis-to-Myravant-design representation" in text
    assert "1,000+ source registry, coverage accounting, genealogy, bias measurement" in text
    assert "fiction/LitRPG-specific research rules" in text
    assert "simulation/infrastructure exemplar-specific research rules" in text
    assert "native-content production" in text
    assert "runtime or production-schema implementation" in text
    assert "live-play or GM behavior" in text

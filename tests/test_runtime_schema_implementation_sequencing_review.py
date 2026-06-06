"""Tests for RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001."""

import os
import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

REVIEW_PATH = REPO_ROOT / "docs" / "doctrine" / "reviews" / "runtime_schema_implementation_sequencing_review.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISIONS_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"

RT_OWNER_SPEC_FILES = {
    "RT-001": "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md",
    "RT-002": "docs/doctrine/control/RT002_resource_consequence_math_owner_specification.md",
    "RT-003": "docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md",
    "RT-004": "docs/doctrine/control/RT004_ability_effect_skill_binding_owner_specification.md",
    "RT-005": "docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md",
    "RT-006": "docs/doctrine/control/RT006_mission_reward_clue_routing_owner_specification.md",
    "RT-007": "docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md",
    "RT-008": "docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_specification.md",
    "RT-009": "docs/doctrine/control/RT009_runtime_rng_table_oracle_owner_specification.md",
    "RT-010": "docs/doctrine/control/RT010_inventory_item_vehicle_asset_owner_specification.md",
    "RT-011": "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md",
    "RT-012": "docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md",
}


@pytest.fixture(scope="module")
def review_text():
    return REVIEW_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def registry_text():
    return REGISTRY_PATH.read_text(encoding="utf-8-sig")


@pytest.fixture(scope="module")
def decisions_text():
    return DECISIONS_PATH.read_text(encoding="utf-8")


# --- File existence ---

def test_review_file_exists():
    assert REVIEW_PATH.is_file(), f"Review file missing: {REVIEW_PATH}"


# --- Review ID ---

def test_references_review_id(review_text):
    assert "RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001" in review_text


# --- Audit and remediation lineage ---

def test_references_audit_001(review_text):
    assert "AUDIT-001" in review_text


def test_references_audit_wave1(review_text):
    assert "AUDIT-WAVE1-001" in review_text


def test_references_audit_wave2(review_text):
    assert "AUDIT-WAVE2-001" in review_text


def test_references_remediation_priority_ledger(review_text):
    assert "REMEDIATION-PRIORITY-LEDGER-001" in review_text


def test_references_scaffold_completion_review_stage2_plan(review_text):
    assert "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001" in review_text


def test_references_stage2_completion_review_closure_ledger(review_text):
    assert "REMEDIATION-STAGE2-COMPLETION-REVIEW-CLOSURE-LEDGER-001" in review_text


# --- RT track references ---

@pytest.mark.parametrize("rt_track", [f"RT-{i:03d}" for i in range(1, 13)])
def test_references_rt_track(review_text, rt_track):
    assert rt_track in review_text, f"Review must reference {rt_track}"


# --- RT owner-specification file references ---

@pytest.mark.parametrize("rt_track,spec_file", list(RT_OWNER_SPEC_FILES.items()))
def test_references_rt_owner_spec_file(review_text, rt_track, spec_file):
    basename = os.path.basename(spec_file)
    assert basename in review_text, f"Review must reference {rt_track} owner-specification file {basename}"


# --- Backend-first / model-interchangeability invariant ---

def test_backend_first_invariant(review_text):
    assert "model-interchangeable" in review_text.lower() or "model interchangeable" in review_text.lower(), \
        "Review must state the model-interchangeability invariant"


def test_llm_not_game_engine(review_text):
    assert "LLM is not the game engine" in review_text, \
        "Review must state the LLM is not the game engine"


def test_owner_boundary_not_implementation_readiness(review_text):
    assert "not implementation readiness" in review_text.lower(), \
        "Review must state that owner-boundary planning is not implementation readiness by itself"


# --- Implementation dependency map ---

def test_includes_implementation_dependency_map(review_text):
    assert "Implementation Dependency Map" in review_text


# --- Implementation waves ---

@pytest.mark.parametrize("wave_name", [
    "Wave 0",
    "Wave 1",
    "Wave 2",
    "Wave 3",
    "Wave 4",
    "Wave 5",
    "Wave 6",
    "Wave 7",
    "Wave 8",
    "Wave 9",
    "Wave 10",
    "Wave 11",
])
def test_includes_implementation_wave(review_text, wave_name):
    assert wave_name in review_text, f"Review must include {wave_name}"


# --- RUNTIME-SEQ-PR-A recommendation ---

def test_recommends_runtime_seq_pr_a(review_text):
    assert "RUNTIME-SEQ-PR-A" in review_text, \
        "Review must recommend RUNTIME-SEQ-PR-A as the next planning step"


# --- Blocked-until conditions ---

def test_includes_blocked_until_conditions(review_text):
    assert "Blocked" in review_text and "until" in review_text.lower()


# --- Crosswalk matrix ---

def test_includes_crosswalk_matrix(review_text):
    assert "Crosswalk Matrix" in review_text


# --- Future test and validation strategy ---

def test_includes_test_validation_strategy(review_text):
    assert "Test and Validation Strategy" in review_text


# --- Non-implementation reaffirmation ---

def test_includes_non_implementation_reaffirmation(review_text):
    assert "Non-Implementation Reaffirmation" in review_text


# --- Review output classification block ---

def test_includes_classification_block(review_text):
    assert "review_id: RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001" in review_text
    assert "artifact_type: implementation_sequencing_review" in review_text
    assert "implementation_status: non_executable_review" in review_text
    assert "authorizes_runtime_implementation: false" in review_text
    assert "authorizes_schema_implementation: false" in review_text
    assert "authorizes_command_ir: false" in review_text
    assert "authorizes_canon_promotion: false" in review_text


# --- Registry tracking ---

def test_registry_tracks_review(registry_text):
    assert "RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001" in registry_text, \
        "Registry must track RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001"


# --- Decision log tracking ---

def test_decision_log_tracks_review(decisions_text):
    assert "RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001" in decisions_text, \
        "Decision log must track RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001"


# --- No-implementation guardrail ---

FORBIDDEN_IMPLEMENTATION_CLAIMS = [
    "implements runtime",
    "implements schema",
    "implements command IR",
    "implements validator",
    "implements generator",
    "implements state store",
    "implements state delta",
    "implements event ledger",
    "implements RNG service",
    "implements table service",
    "implements oracle service",
    "implements persistence writer",
    "implements retrieval index",
    "implements context-packet compiler",
    "implements redaction algorithm",
    "implements hidden-state database",
    "implements domain service",
    "implements campaign memory",
    "implements live-play prompt",
    "implements training",
    "authorizes pilot conversion",
    "authorizes sourcebook inclusion",
    "authorizes canon promotion",
    "promotes canon",
]


@pytest.mark.parametrize("forbidden", FORBIDDEN_IMPLEMENTATION_CLAIMS)
def test_no_implementation_claims(review_text, forbidden):
    assert forbidden not in review_text.lower(), \
        f"Review must not claim: '{forbidden}'"

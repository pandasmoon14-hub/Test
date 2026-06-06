"""Tests for RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001."""

import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

PLAN_PATH = REPO_ROOT / "docs" / "doctrine" / "reviews" / "runtime_seq_pr_b_narration_context_packet_contract_plan.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISIONS_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"


@pytest.fixture(scope="module")
def plan_text():
    return PLAN_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def registry_text():
    return REGISTRY_PATH.read_text(encoding="utf-8-sig")


@pytest.fixture(scope="module")
def decisions_text():
    return DECISIONS_PATH.read_text(encoding="utf-8")


# --- File existence ---

def test_plan_file_exists():
    assert PLAN_PATH.is_file(), f"Plan file missing: {PLAN_PATH}"


# --- Review ID ---

def test_references_review_id(plan_text):
    assert "RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001" in plan_text


# --- Derives from sequencing review ---

def test_references_sequencing_review(plan_text):
    assert "RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001" in plan_text


# --- Derives from PR-A ---

def test_references_pr_a(plan_text):
    assert "RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001" in plan_text


# --- Primary owner tracks ---

def test_primary_owner_rt005(plan_text):
    assert "RT-005" in plan_text


def test_primary_owner_rt011(plan_text):
    assert "RT-011" in plan_text


# --- RT-001 through RT-012 ---

@pytest.mark.parametrize("rt_id", [f"RT-{str(i).zfill(3)}" for i in range(1, 13)])
def test_references_rt_owner_specs(plan_text, rt_id):
    assert rt_id in plan_text, f"Plan must reference {rt_id}"


# --- Backend-first / model-interchangeability invariant ---

def test_references_backend_first_invariant(plan_text):
    assert "model-interchangeable" in plan_text.lower() or "model interchangeable" in plan_text.lower()


def test_llm_is_not_game_engine(plan_text):
    assert "LLM is not the game engine" in plan_text


# --- Packet layer separation ---

def test_includes_packet_layer_separation(plan_text):
    assert "Packet layer separation" in plan_text


PACKET_FAMILIES = [
    "BackendStateContext",
    "ContextPacket",
    "NarrationRenderPacket",
    "IntentParsingPacket",
    "ClarificationPacket",
    "SummaryPacket",
    "EvaluationPacket",
]


@pytest.mark.parametrize("packet", PACKET_FAMILIES)
def test_packet_family_present(plan_text, packet):
    assert packet in plan_text, f"Packet layer must include {packet}"


# --- NarrationRenderPacket contract ---

def test_includes_narration_render_packet_contract(plan_text):
    assert "NarrationRenderPacket contract" in plan_text


RENDER_PACKET_FIELDS = [
    "scene_visible_facts",
    "player_visible_actor_state",
    "visible_location_state",
    "visible_threat_or_pressure",
    "recent_committed_event_echoes",
    "available_action_affordances",
    "sensory_palette",
    "tone_and_style_bounds",
    "narrator_forbidden_claims",
    "hidden_information_exclusion_marker",
    "packet_budget_estimate",
    "output_constraints",
    "missing_information_policy",
]


@pytest.mark.parametrize("field", RENDER_PACKET_FIELDS)
def test_render_packet_field_present(plan_text, field):
    assert field in plan_text, f"NarrationRenderPacket must include {field}"


# --- ContextPacket contract ---

def test_includes_context_packet_contract(plan_text):
    assert "ContextPacket contract" in plan_text


# --- Visibility and hidden-information rules ---

def test_includes_visibility_and_hidden_info_rules(plan_text):
    assert "Visibility and hidden-information rules" in plan_text


VISIBILITY_TIERS = [
    "backend_only",
    "reviewer_only",
    "system_hidden",
    "narrator_hidden",
    "player_hidden",
    "character_known",
    "actor_known",
    "faction_known",
    "player_visible",
    "narrator_visible",
    "public_world_visible",
    "source_local_visible",
    "redacted_reference_only",
]


@pytest.mark.parametrize("tier", VISIBILITY_TIERS)
def test_visibility_tier_present(plan_text, tier):
    assert tier in plan_text, f"Visibility tiers must include {tier}"


def test_hidden_info_leakage_hard_failure(plan_text):
    assert "hard failure" in plan_text.lower()


# --- Local 8B packet budget policy ---

def test_includes_local_8b_packet_budget_policy(plan_text):
    assert "Local 8B packet budget policy" in plan_text or "local 8B packet budget policy" in plan_text


def test_packets_must_be_bounded(plan_text):
    assert "bounded" in plan_text.lower()


def test_budget_tests_before_live_play(plan_text):
    assert "budget tests must exist before live-play" in plan_text.lower() or \
           "budget tests must exist before live-play adapter" in plan_text


# --- Missing-information policy ---

def test_includes_missing_information_policy(plan_text):
    assert "Missing-information policy" in plan_text or "missing-information policy" in plan_text


def test_missing_info_forbidden_invent(plan_text):
    lower = plan_text.lower()
    assert "invent missing mechanics" in lower or "invent hidden facts" in lower


# --- NarratorOutputContract ---

def test_includes_narrator_output_contract(plan_text):
    assert "NarratorOutputContract" in plan_text


NARRATOR_OUTPUT_FIELDS = [
    "narration_text",
    "intent_proposals",
    "clarification_questions",
    "visible_state_summary",
    "implied_state_claims",
    "uncertainty_flags",
    "needs_backend_retrieval",
    "soft_state_risk_flags",
    "hidden_info_risk_flags",
    "proposed_affordance_echoes",
    "refusal_or_boundary_note",
]


@pytest.mark.parametrize("field", NARRATOR_OUTPUT_FIELDS)
def test_narrator_output_field_present(plan_text, field):
    assert field in plan_text, f"NarratorOutputContract must include {field}"


def test_narrator_output_never_commitment(plan_text):
    assert "never event commitment" in plan_text.lower() or "is never event commitment" in plan_text


# --- Soft-state mutation detection ---

def test_includes_soft_state_mutation_detection(plan_text):
    assert "Soft-state mutation detection" in plan_text or "soft-state mutation detection" in plan_text


def test_soft_state_examples(plan_text):
    lower = plan_text.lower()
    assert "prose implies injury" in lower
    assert "prose awards an item" in lower or "prose awards" in lower


# --- CanonicalSilencePolicy ---

def test_includes_canonical_silence_policy(plan_text):
    assert "CanonicalSilencePolicy" in plan_text


def test_silence_is_authority_preserving(plan_text):
    assert "authority-preserving" in plan_text.lower()


# --- Source-local and canon boundary notices ---

def test_includes_source_local_and_canon_boundary_notices(plan_text):
    assert "Source-local and canon boundary notices" in plan_text


# --- Model role contracts ---

def test_includes_model_role_contracts(plan_text):
    assert "Model role contracts" in plan_text


MODEL_ROLES = [
    "local_8b_narrator",
    "local_8b_intent_parser",
    "api_reflective_summarizer",
    "api_evaluator_or_judge",
    "api_canon_or_sourcebook_drafter",
    "backend_validator",
    "backend_packet_compiler",
]


@pytest.mark.parametrize("role", MODEL_ROLES)
def test_model_role_present(plan_text, role):
    assert role in plan_text, f"Model role contracts must include {role}"


# --- Packet assembly trace requirements ---

def test_includes_packet_assembly_trace_requirements(plan_text):
    assert "Packet assembly trace requirements" in plan_text


TRACE_FIELDS = [
    "packet_id",
    "packet_type",
    "source_event_refs",
    "source_record_refs",
    "visible_facts_included",
    "hidden_facts_withheld_count",
    "redaction_reasons",
    "token_estimate",
    "model_role",
    "output_id",
    "implied_state_claims_detected",
    "validation_result",
    "correction_event_ref_if_any",
]


@pytest.mark.parametrize("field", TRACE_FIELDS)
def test_trace_field_present(plan_text, field):
    assert field in plan_text, f"Trace requirements must include {field}"


# --- Validation and test requirements ---

def test_includes_validation_and_test_requirements(plan_text):
    assert "Validation and test requirements" in plan_text


TEST_FAMILIES = [
    "Render packet budget tests",
    "Hidden-info exclusion tests",
    "Narrator-output contract tests",
    "Soft-state mutation tests",
    "Canonical silence tests",
    "Source-local boundary tests",
    "Missing-information policy tests",
    "Model-role packet authorization tests",
    "Packet trace completeness tests",
    "Local 8B truncation-safety tests",
    "Adversarial narration leakage tests",
    "Metamorphic narration consistency tests",
]


@pytest.mark.parametrize("family", TEST_FAMILIES)
def test_test_family_present(plan_text, family):
    assert family in plan_text, f"Test requirements must include {family}"


# --- Blocked-until ledger ---

def test_includes_blocked_until_ledger(plan_text):
    assert "Blocked-until ledger" in plan_text or "blocked-until ledger" in plan_text


BLOCKED_ITEMS = [
    "Context-packet compiler",
    "Render-packet schema",
    "Narrator output schema",
    "Redaction algorithm",
    "Hidden-state database",
    "Packet budget enforcement",
    "Soft-state mutation validator",
    "Model routing",
    "Live-play adapter",
    "Prompt templates",
    "Training",
    "Runtime code",
    "Domain services",
    "Pilot conversion",
    "Sourcebook inclusion",
    "Canon promotion",
]


@pytest.mark.parametrize("item", BLOCKED_ITEMS)
def test_blocked_item_present(plan_text, item):
    assert item in plan_text, f"Blocked-until ledger must include {item}"


# --- Recommends RUNTIME-SEQ-PR-C ---

def test_recommends_pr_c(plan_text):
    assert "RUNTIME-SEQ-PR-C" in plan_text


def test_pr_c_state_event(plan_text):
    lower = plan_text.lower()
    assert "state/event" in lower or ("state" in lower and "event" in lower and "transaction" in lower)


# --- Non-implementation reaffirmation ---

def test_includes_non_implementation_reaffirmation(plan_text):
    assert "Non-implementation reaffirmation" in plan_text or "non-implementation reaffirmation" in plan_text


# --- Classification block ---

def test_includes_classification_block(plan_text):
    assert "runtime_seq_pr_b:" in plan_text
    assert "non_executable_planning" in plan_text
    assert "defines_packet_layer_separation: true" in plan_text
    assert "defines_narration_render_packet_contract: true" in plan_text
    assert "defines_context_packet_contract: true" in plan_text
    assert "defines_visibility_tiers: true" in plan_text
    assert "defines_local_8b_packet_budget_policy: true" in plan_text
    assert "defines_narrator_output_contract: true" in plan_text
    assert "defines_soft_state_mutation_detection_requirements: true" in plan_text
    assert "authorizes_runtime_implementation: false" in plan_text
    assert "authorizes_canon_promotion: false" in plan_text


# --- Registry tracking ---

def test_registry_tracking_exists(registry_text):
    assert "RUNTIME-SEQ-PR-B" in registry_text


# --- Decision log tracking ---

def test_decision_log_tracking_exists(decisions_text):
    assert "RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001" in decisions_text


# --- future_required_not_implemented status ---

def test_all_packets_marked_future(plan_text):
    assert plan_text.count("future_required_not_implemented") >= 7, \
        "All 7 packet families must be marked future_required_not_implemented"


# --- No implementation claims ---

FORBIDDEN_IMPLEMENTATIONS = [
    "implements runtime",
    "implements schema",
    "implements command IR",
    "implements validator",
    "implements generator",
    "implements context-packet compiler",
    "implements render-packet schema",
    "implements narrator output schema",
    "implements redaction algorithm",
    "implements hidden-state database",
    "implements packet budget enforcement",
    "implements soft-state mutation validator",
    "implements model routing",
    "implements prompt templates",
    "implements live-play adapter",
    "implements training",
    "implements donor-content audit",
    "authorizes pilot conversion",
    "authorizes sourcebook inclusion",
    "authorizes canon promotion",
]


@pytest.mark.parametrize("forbidden", FORBIDDEN_IMPLEMENTATIONS)
def test_no_implementation_claims(plan_text, forbidden):
    text_lower = plan_text.lower()
    if "authorizes" in forbidden:
        key = forbidden.replace("authorizes ", "authorizes_").replace(" ", "_")
        assert f"{key}: false" in plan_text or forbidden not in text_lower, \
            f"Plan must not claim: {forbidden}"
    else:
        assert forbidden not in text_lower, f"Plan must not claim: {forbidden}"

from pathlib import Path

REVIEW = Path(
    "docs/doctrine/reviews/"
    "runtime_domain_pr_4d_validation_integration_invariant_enforcement_skeleton_hardening_review.md"
)
REGISTRY = Path("docs/doctrine/astra_doctrine_registry_v0_1.yaml")
DECISIONS = Path("docs/decisions/current_decisions_log.md")
PR4D_ID = "RUNTIME-DOMAIN-PR-4D-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-REVIEW-001"
PR4C_ID = "RUNTIME-DOMAIN-PR-4C-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-HARDENING-001"
PR4B_ID = "RUNTIME-DOMAIN-PR-4B-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-REVIEW-001"
PR4_PLAN_ID = "RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001"


def _review_text() -> str:
    assert REVIEW.exists()
    return REVIEW.read_text()


def test_review_file_and_lineage_ids_exist():
    text = _review_text()
    assert PR4D_ID in text
    assert PR4C_ID in text
    assert PR4B_ID in text
    assert PR4_PLAN_ID in text


def test_backend_first_invariant_exists():
    text = _review_text()
    assert "BACKEND-FIRST VALIDATION INVARIANT" in text
    assert "The LLM is not the game engine" in text
    assert "Validation is backend authority" in text
    assert "Validation artifacts cannot mutate state" in text


def test_required_review_sections_exist():
    text = _review_text()
    required = [
        "PR-4B BLOCKER CLOSURE MATRIX",
        "CONSTANT AND COMPATIBILITY MAP REVIEW",
        "FAILURE-ROUTE REVIEW",
        "REQUEST-STAGE REVIEW",
        "RESULT SUBJECT-IDENTITY REVIEW",
        "RESULT TRACE AND REFERENCE REVIEW",
        "DECISION / FINAL-STAGE REVIEW",
        "INTERMEDIATE-STAGE FLAG CONSISTENCY",
        "SUCCESS-RESULT REVIEW",
        "FAILURE, REJECTION, QUARANTINE, ESCALATION, AND UNSUPPORTED-SCOPE REVIEW",
        "PUBLIC HIDDEN-INFORMATION SAFETY REVIEW",
        "PROVENANCE, SOURCE-LOCAL, CONVERSION, AND CANON REVIEW",
        "FACTORY / VALIDATOR PARITY REVIEW",
        "IMMUTABILITY AND SERIALIZATION REVIEW",
        "NON-EXECUTION AND IMPORT REVIEW",
        "DOMAIN AND KERNEL HANDOFF REVIEW",
        "RESOURCE / CONSEQUENCE MATH READINESS REVIEW",
        "CORPUS-SCALE PRESSURE REVIEW",
        "RISK REVIEW",
        "HARDENING LEDGER",
        "NON-IMPLEMENTATION REAFFIRMATION",
        "CLASSIFICATION BLOCK",
    ]
    for phrase in required:
        assert phrase in text


def test_representative_findings_and_gate_fields_exist():
    text = _review_text()
    for phrase in [
        "route subject/result subject equality",
        "result subject/request subject linkage",
        "validation_ready hidden-info posture",
        "typed provenance references",
        "trace identity linkage",
        "validation-result identity linkage",
        "resource_consequence_math_dependency_ready: false",
        "requires_pr_4e_hardening_before_pr_5: true",
        "ready_for_runtime_domain_pr_5_planning: false",
        "next_step_authorized: RUNTIME-DOMAIN-PR-4E validation integration residual skeleton hardening",
        "next_allowed_step: RUNTIME-DOMAIN-PR-4E validation integration residual skeleton hardening, pending review",
    ]:
        assert phrase in text


def test_exactly_one_gate_finding_and_one_next_step_selected():
    text = _review_text()
    assert text.count("gate_finding:") == 1
    assert text.count("next_step_authorized:") == 1
    assert text.count("next_allowed_step:") == 1


def test_classification_block_non_authorizations_exist():
    text = _review_text()
    for field in [
        "runtime_domain_pr_4d:",
        "authorizes_runtime_code_by_this_pr: false",
        "authorizes_domain_code_by_this_pr: false",
        "authorizes_validation_execution_by_this_pr: false",
        "authorizes_invariant_evaluation_by_this_pr: false",
        "authorizes_state_mutation_by_this_pr: false",
        "authorizes_state_delta_application_by_this_pr: false",
        "authorizes_event_ledger_append_by_this_pr: false",
        "authorizes_persistence_by_this_pr: false",
        "authorizes_replay_by_this_pr: false",
        "authorizes_resource_math_by_this_pr: false",
        "authorizes_model_integration_by_this_pr: false",
        "authorizes_live_play_by_this_pr: false",
        "authorizes_conversion_by_this_pr: false",
        "authorizes_canon_promotion_by_this_pr: false",
    ]:
        assert field in text


def test_registry_and_decision_log_tracking_are_unique():
    registry = REGISTRY.read_text()
    decisions = DECISIONS.read_text()
    assert registry.count(PR4D_ID) == 1
    assert decisions.count(f"## {PR4D_ID}") == 1
    assert "reviews_pr_4c: true" in registry
    assert "reviews_pr_4b_blocker_closure: true" in registry
    assert "defines_hardening_ledger: true" in registry
    assert "selects_exactly_one_next_step: true" in registry
    assert "authorizes_code_or_runtime_behavior: false" in registry


def test_current_authorized_domain_files_remain_narrow():
    domain_dir = Path("src/astra_runtime/domain")
    actual = {p.name for p in domain_dir.iterdir()}
    expected = {
        "__init__.py",
        "command_lifecycle.py",
        "action_legality.py",
        "state_store.py",
        "state_projection.py",
        "transaction_lifecycle.py",
        "event_commitment.py",
        "validation_integration.py",
        "resource_consequence_math.py", "context_packet_compiler.py", "model_boundary_evaluation.py", "tiny_vertical_slice.py",
        "__pycache__",
    }
    assert actual == expected


def test_future_runtime_surfaces_remain_absent():
    absent_paths = [
        "src/astra_runtime/domain/resource_math.py",
        "src/astra_runtime/domain/combat.py",
        "src/astra_runtime/domain/ability_effects.py",
        "src/astra_runtime/domain/inventory.py",
        "src/astra_runtime/domain/mission.py",
        "src/astra_runtime/domain/social_faction.py",
        "src/astra_runtime/domain/generated_content.py",
        "src/astra_runtime/kernel/context_packet_compiler.py",
        "src/astra_runtime/model",
        "src/astra_runtime/prompts",
        "src/astra_runtime/live_play",
        "src/astra_runtime/ui",
        "src/astra_runtime/database",
        "src/astra_runtime/store",
    ]
    for path in absent_paths:
        assert not Path(path).exists(), path

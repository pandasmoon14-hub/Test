from pathlib import Path

REVIEW = Path(
    "docs/doctrine/reviews/"
    "runtime_domain_pr_4b_validation_integration_invariant_enforcement_skeleton_review.md"
)
REGISTRY = Path("docs/doctrine/astra_doctrine_registry_v0_1.yaml")
DECISIONS = Path("docs/decisions/current_decisions_log.md")
PR4B_ID = "RUNTIME-DOMAIN-PR-4B-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-REVIEW-001"
PR4A_ID = "RUNTIME-DOMAIN-PR-4A-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-IMPLEMENTATION-001"
PR4_PLAN_ID = "RUNTIME-DOMAIN-PR-4-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SERVICE-PLAN-001"
PR3B_ID = "RUNTIME-DOMAIN-PR-3B-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-REVIEW-001"


def _review_text() -> str:
    assert REVIEW.exists()
    return REVIEW.read_text()


def test_review_file_ids_lineage_and_backend_first_invariant_exist():
    text = _review_text()
    assert PR4B_ID in text
    assert PR4A_ID in text
    assert PR4_PLAN_ID in text
    assert PR3B_ID in text
    assert "BACKEND-FIRST VALIDATION INVARIANT" in text
    assert "The LLM is not the game engine" in text
    assert "validation is backend authority" in text


def test_review_covers_required_review_areas():
    text = _review_text()
    required_phrases = [
        "CONSTANT AND VOCABULARY REVIEW",
        "DATACLASS AND IMMUTABILITY REVIEW",
        "FACTORY / VALIDATOR PARITY REVIEW",
        "DECISION / STAGE COMPATIBILITY REVIEW",
        "SUCCESS-RESULT SEMANTIC REVIEW",
        "FAILURE-ROUTE SEMANTIC REVIEW",
        "TRACE, AUDIT, AND REPLAY REVIEW",
        "HIDDEN-INFORMATION REVIEW",
        "PROVENANCE, SOURCE-LOCAL, CONVERSION, AND CANON REVIEW",
        "ANTI-AUTHORITY AND NON-EXECUTION REVIEW",
        "KERNEL DEPENDENCY REVIEW",
        "DOMAIN HANDOFF REVIEW",
        "CORPUS-SCALE PRESSURE REVIEW",
        "RISK REVIEW",
        "HARDENING LEDGER",
        "NON-IMPLEMENTATION REAFFIRMATION",
        "CLASSIFICATION BLOCK",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_review_mentions_representative_findings_and_blocked_capabilities():
    text = _review_text()
    for phrase in [
        "success requires `validation_result_ref_id`",
        "success requires `trace_id`",
        "success requires `blocking=False`",
        "decision/final-stage compatibility",
        "failed result route requirement",
        "generated-content `provenance_checked` linkage",
        "hidden-info sanitized reason boundary",
        "validation result cannot mutate state",
        "cannot append events",
        "runtime validation cannot promote canon",
    ]:
        assert phrase in text


def test_review_contains_exactly_one_gate_finding_and_one_selected_next_step():
    text = _review_text()
    assert text.count("gate_finding:") == 1
    assert text.count("next_step_authorized:") == 1
    assert "requires_pr_4c_hardening_before_pr_5: true" in text
    assert "ready_for_runtime_domain_pr_5_planning: false" in text
    assert "RUNTIME-DOMAIN-PR-4C validation integration skeleton hardening" in text
    assert "next_step_authorized: RUNTIME-DOMAIN-PR-5" not in text


def test_classification_block_non_authorizations_exist():
    text = _review_text()
    for field in [
        "runtime_domain_pr_4b:",
        "authorizes_runtime_code_by_this_pr: false",
        "authorizes_domain_code_by_this_pr: false",
        "authorizes_validation_rule_execution_by_this_pr: false",
        "authorizes_invariant_enforcement_by_this_pr: false",
        "authorizes_state_mutation_by_this_pr: false",
        "authorizes_event_ledger_append_by_this_pr: false",
        "authorizes_persistence_by_this_pr: false",
        "authorizes_replay_by_this_pr: false",
        "authorizes_model_integration_by_this_pr: false",
        "authorizes_live_play_by_this_pr: false",
        "authorizes_conversion_by_this_pr: false",
        "authorizes_canon_promotion_by_this_pr: false",
    ]:
        assert field in text


def test_registry_and_decision_log_tracking_are_unique():
    registry = REGISTRY.read_text()
    decisions = DECISIONS.read_text()
    assert registry.count(PR4B_ID) == 1
    assert decisions.count(f"## {PR4B_ID}") == 1
    assert "reviews_success_result_semantics: true" in registry
    assert "reviews_failure_route_semantics: true" in registry
    assert "defines_hardening_ledger: true" in registry
    assert "authorizes_code_or_runtime_behavior: false" in registry
    assert "PR-4C is required before PR-5 planning" in decisions


def test_current_authorized_domain_files_remain_narrow():
    domain_dir = Path("src/astra_runtime/domain")
    actual = {p.name for p in domain_dir.iterdir()}
    optional = {"__pycache__"}
    expected = {
        "__init__.py",
        "command_lifecycle.py",
        "action_legality.py",
        "state_store.py",
        "state_projection.py",
        "transaction_lifecycle.py",
        "event_commitment.py",
        "validation_integration.py",
    }
    assert actual - optional == expected
    assert actual <= expected | optional


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

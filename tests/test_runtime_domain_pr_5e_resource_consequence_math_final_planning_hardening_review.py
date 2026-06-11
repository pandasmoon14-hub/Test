from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5e_resource_consequence_math_final_planning_hardening_review.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
DOMAIN_RESOURCE_MATH = ROOT / "src/astra_runtime/domain/resource_consequence_math.py"
DOMAIN_DIR = ROOT / "src/astra_runtime/domain"
KERNEL_DIR = ROOT / "src/astra_runtime/kernel"

PR5E_ID = "RUNTIME-DOMAIN-PR-5E-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-REVIEW-001"
PR5D_ID = "RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001"
PR5C_ID = "RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001"
PR5B_ID = "RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001"
PR5_ID = "RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001"
PR4F_ID = "RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(number: int) -> str:
    text = read(ARTIFACT)
    pattern = rf"^## {number}\. .*?(?=^## {number + 1}\. |\Z)"
    match = re.search(pattern, text, flags=re.M | re.S)
    assert match, f"missing section {number}"
    return match.group(0)


def test_lineage_backend_first_scope_and_authority_precedence() -> None:
    text = read(ARTIFACT)
    for token in [PR5E_ID, PR5D_ID, PR5C_ID, PR5B_ID, PR5_ID, PR4F_ID, "RT002_resource_consequence_math_owner_specification.md"]:
        assert token in text
    for token in [
        "non-executable review gate",
        "reviews **RUNTIME-DOMAIN-PR-5D",
        "implements no code",
        "PR-5A remains blocked",
        "PR-5D overrides PR-5B",
        "PR-5B remains inherited only",
    ]:
        assert token in text
    for invariant in [
        "The LLM is not the game engine",
        "References are not calculations",
        "Results are not state",
        "Settlement proposals are not transactions",
        "`validation_ready` is not `validation_passed`",
        "Runtime validation cannot promote canon",
    ]:
        assert invariant in section(2)


def test_all_required_review_sections_are_present() -> None:
    text = read(ARTIFACT)
    headings = [
        "## 1. Purpose, status, source ledger, and authority precedence",
        "## 2. Backend-first invariant",
        "## 3. PR-5D scope review",
        "## 4. PR-5C blocker-closure matrix",
        "## 5. Final constant-surface inventory",
        "## 6. Stage/decision completeness review",
        "## 7. Validation-integration review",
        "## 8. Typed-subject review",
        "## 9. External-reference/dependency completeness review",
        "## 10. Dependency-state review",
        "## 11. Quantity contract review",
        "## 12. CostTerm and ConsequenceTerm review",
        "## 13. CostBundle review",
        "## 14. Request/result/proposal linkage review",
        "## 15. Internal-reference integrity review",
        "## 16. Serialization and hidden-information review",
        "## 17. False-only authority review",
        "## 18. Factory/validator parity review",
        "## 19. Corpus-scale and owner-boundary review",
        "## 20. Risk and adversarial review",
        "## 21. Hardening ledger",
        "## 22. Gate decision",
        "## 23. Recommended next PR",
        "## 24. Non-implementation reaffirmation and classification block",
    ]
    for heading in headings:
        assert heading in text


def test_scope_review_and_no_runtime_domain_file_added() -> None:
    text = read(ARTIFACT)
    scope = section(3)
    for token in [
        "four-file planning/tracking footprint",
        "no domain or kernel implementation changes",
        "resource_consequence_math.py` remains absent",
        "PR-5A remained blocked",
    ]:
        assert token in scope
    assert not DOMAIN_RESOURCE_MATH.exists()
    assert {p.name for p in DOMAIN_DIR.iterdir() if p.is_file()} == {
        "__init__.py",
        "action_legality.py",
        "command_lifecycle.py",
        "event_commitment.py",
        "state_projection.py",
        "state_store.py",
        "transaction_lifecycle.py",
        "validation_integration.py",
    }
    assert {p.name for p in KERNEL_DIR.iterdir() if p.is_file()} == {
        "__init__.py",
        "command_envelope.py",
        "context_projection.py",
        "event_ledger.py",
        "hidden_information.py",
        "persistence_boundary.py",
        "record_identity.py",
        "replay_audit.py",
        "rng_interface.py",
        "runtime_trace.py",
        "schema_registry.py",
        "state_delta.py",
        "table_oracle.py",
        "transaction_preview.py",
        "validation_pipeline.py",
    }


def test_pr_5c_closure_matrix_and_authority_reviews() -> None:
    text = read(ARTIFACT)
    matrix = section(4)
    defects = [
        "free-string validation posture",
        "untyped subjects",
        "quarantine/escalation blocking",
        "dependency field binding",
        "consequence policy ownership",
        "lexical quantity boundary",
        "bundle bounds and alternatives",
        "request/result/proposal linkage",
        "settlement validation",
        "serialization ownership",
        "factory/validator parity",
        "false-only authority",
    ]
    for defect in defects:
        assert defect in matrix
    for status in ["closed", "partially closed"]:
        assert status in matrix
    false_only = section(17)
    for flag in [
        "calculation_executed",
        "settlement_authorized",
        "state_delta_application_authorized",
        "event_commitment_authorized",
        "persistence_authorized",
        "rng_execution_authorized",
        "model_authority_authorized",
        "canon_promotion_authorized",
    ]:
        assert flag in false_only
    assert "manually constructed objects with any true authority flag must be rejected" in false_only


def test_constant_stage_decision_validation_and_subject_reviews() -> None:
    constants = section(5)
    for token in ["RESOURCE_MATH_SUBJECT_ROLES", "QUANTITY_NEGATIVE_VALUE_POLICIES", "RESOURCE_MATH_DEPENDENCY_TYPES", "source-local", "quarantine", "owner-handoff", "doctrine-escalation"]:
        assert token in constants
    stage = section(6)
    for token in [
        "Every unlisted pair is invalid",
        "Terminal stages `quarantined_for_review` and `escalated_to_doctrine`",
        "accepted_for_planning` at `resource_math_requested` is semantically safe",
        "normalized_for_planning` at `calculation_ready_for_review` is compatible",
        "required=False` and `satisfied=False` dependencies can coexist",
    ]:
        assert token in stage
    validation = section(7)
    for token in ["VALIDATION_INTEGRATION_DECISIONS", "validation_ready", "validation_passed", "SettlementProposal", "same-result linkage rule"]:
        assert token in validation
    typed_subject = section(8)
    for token in ["subject_binding_id", "subject_type", "subject_ref_id", "primary_subject", "cross-subject costs", "No object dereferencing"]:
        assert token in typed_subject


def test_external_dependency_review_is_exhaustive_and_selects_blockers() -> None:
    ext = section(9)
    for token in [
        "ResourceMathSubjectReference.subject_ref_id",
        "ResourceReference.unit_ref_id",
        "ResourceReference.dimension_ref_id",
        "QuantitySpecification.unit_ref_id",
        "QuantitySpecification.dimension_ref_id",
        "provenance_refs",
        "command_ref_id",
        "action_legality_ref_id",
        "state_projection_ref_ids",
        "validation refs",
        "trace refs",
        "owner handoff refs",
        "RNG/table refs",
        "ResourceMathResult.request_id",
        "SettlementProposal.result_id",
        "proposed_state_delta_refs",
        "transaction/event prerequisites",
        "rollback_accounting_refs",
        "subject_ref`, `unit_ref`, and `dimension_ref` are required before PR-5A",
    ]:
        assert token in ext
    assert ext.count("blocker") >= 3


def test_dependency_quantity_bundle_and_request_result_proposal_reviews() -> None:
    dep = section(10)
    for token in ["unique dependency IDs", "required=True", "satisfied=False", "hidden_info_safe=False", "no dependency is dereferenced or executed"]:
        assert token in dep
    quantity = section(11)
    for token in ["integer_exact", "decimal_exact", "fraction_exact", "fixed_point_scaled", "source_literal_only", "blocked_pending_numeric_choice", "Decimal", "Fraction", "float", "QUANTITY_NEGATIVE_VALUE_POLICIES", "precision field semantics"]:
        assert token in quantity
    bundle = section(13)
    for token in ["term uniqueness", "bool rejection", "alternative-group identity", "Every unlisted combination is invalid", "maximum_allowed_terms"]:
        assert token in bundle
    linkage = section(14)
    for token in ["ResourceMathRequest", "ResourceMathResult", "SettlementProposal", "validation_result_ref_id", "blocked, quarantined, escalated, or merely `validation_ready`", "event-only"]:
        assert token in linkage


def test_factory_corpus_risk_hardening_and_gate_decision() -> None:
    factory = section(18)
    for token in ["create/validate helpers for all ten shapes", "bundle compatibility", "settlement proposal rules", "metadata immutability"]:
        assert token in factory
    corpus = section(19)
    for token in ["fantasy and sci-fi", "cultivation", "cyberware/biotech", "vehicles/mechs/ships", "faction/debt/mission", "source-local cosmologies", "generated content", "persistent campaign consequences"]:
        assert token in corpus
    risk = section(20)
    for token in ["orphan stage or decision", "free-string policy survives", "external subject/unit/dimension", "validation_ready` reaches `SettlementProposal`", "hidden source literals leak", "donor categories become core law"]:
        assert token in risk
    hardening = section(21)
    for token in ["PR-5F blocker", "required before executable calculation", "required before settlement/commitment", "deferred to a named RT owner", "doctrine escalation"]:
        assert token in hardening
    gate = section(22)
    assert text_has_exactly_one_gate_finding(read(ARTIFACT))
    assert "requires_pr_5f_before_pr_5a: true" in gate
    assert "ready_for_pr_5a_skeleton_implementation: false" in gate
    assert "next_step_authorized: RUNTIME-DOMAIN-PR-5F resource and consequence math residual planning hardening" in gate
    assert "RUNTIME-DOMAIN-PR-5A resource and consequence math skeleton implementation" not in gate


def text_has_exactly_one_gate_finding(text: str) -> bool:
    return text.count("gate_finding:") == 1


def test_exactly_one_selected_next_step_registry_and_decision_log() -> None:
    text = read(ARTIFACT)
    assert text.count("next_step_authorized:") == 1
    assert "RUNTIME-DOMAIN-PR-5F resource and consequence math residual planning hardening" in section(23)
    registry = read(REGISTRY)
    decisions = read(DECISIONS)
    assert registry.count(f"file_id: {PR5E_ID}") == 1
    assert registry.count("registry_version: 0.1.0") == 1
    assert "version: 0.1.87" in registry
    assert decisions.count(f"## {PR5E_ID}") == 1
    for token in [
        "review-only",
        "PR-5F is required before PR-5A",
        "PR-5A is not authorized",
        "sole next step",
        "no implementation",
    ]:
        assert token in decisions


def test_review_artifact_is_not_long_prose_verbatim_copy_of_prior_artifacts() -> None:
    text = read(ARTIFACT)
    assert "HARDENING" in section(22)
    assert "PASS" not in section(22)
    assert text.count(PR5E_ID) >= 2
    assert len(text.splitlines()) > 250

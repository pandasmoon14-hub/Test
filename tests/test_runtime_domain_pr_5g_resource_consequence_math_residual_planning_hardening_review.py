
from tests.runtime_domain_package_manifest import (
    AUTHORIZED_RUNTIME_DOMAIN_ENTRIES,
    AUTHORIZED_RUNTIME_DOMAIN_FILES,
)
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5g_resource_consequence_math_residual_planning_hardening_review.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
DOMAIN_RESOURCE_MATH = ROOT / "src/astra_runtime/domain/resource_consequence_math.py"
DOMAIN_DIR = ROOT / "src/astra_runtime/domain"
KERNEL_DIR = ROOT / "src/astra_runtime/kernel"

PR5G_ID = "RUNTIME-DOMAIN-PR-5G-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-REVIEW-001"
LINEAGE_IDS = [
    PR5G_ID,
    "RUNTIME-DOMAIN-PR-5F-RESOURCE-CONSEQUENCE-MATH-RESIDUAL-PLANNING-HARDENING-001",
    "RUNTIME-DOMAIN-PR-5E-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-REVIEW-001",
    "RUNTIME-DOMAIN-PR-5D-RESOURCE-CONSEQUENCE-MATH-FINAL-PLANNING-HARDENING-001",
    "RUNTIME-DOMAIN-PR-5C-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-REVIEW-001",
    "RUNTIME-DOMAIN-PR-5B-RESOURCE-CONSEQUENCE-MATH-PLANNING-HARDENING-001",
    "RUNTIME-DOMAIN-PR-5-RESOURCE-CONSEQUENCE-MATH-SERVICE-PLAN-001",
    "RUNTIME-DOMAIN-PR-4F-VALIDATION-INTEGRATION-RESIDUAL-HARDENING-REVIEW-001",
    "RT002_resource_consequence_math_owner_specification.md",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(number: int) -> str:
    text = read(ARTIFACT)
    pattern = rf"^## {number}\. .*?(?=^## {number + 1}\. |\Z)"
    match = re.search(pattern, text, flags=re.M | re.S)
    assert match, f"missing section {number}"
    return match.group(0)


def test_lineage_purpose_status_and_authority_precedence() -> None:
    text = read(ARTIFACT)
    for token in LINEAGE_IDS:
        assert token in text
    for token in [
        "non-executable review gate",
        "reviews **RUNTIME-DOMAIN-PR-5F",
        "implements no code",
        "authorizes only one of two downstream paths",
        "PR-5A remains blocked until this review is accepted",
        "PR-5F overrides PR-5D only where PR-5F explicitly replaces a contract",
        "PR-5D overrides PR-5B only where PR-5D explicitly replaces a contract",
        "Earlier contracts remain inherited",
    ]:
        assert token in section(1)


def test_all_required_sections_are_present() -> None:
    text = read(ARTIFACT)
    headings = [
        "## 1. Purpose, status, source ledger, and authority precedence",
        "## 2. Backend-first invariant",
        "## 3. PR-5F scope review",
        "## 4. PR-5E blocker-closure matrix",
        "## 5. Effective implementation-contract inventory",
        "## 6. Constant-surface review",
        "## 7. Stage/decision and blocker-precedence review",
        "## 8. External-reference dependency review",
        "## 9. Optional and unsatisfied dependency review",
        "## 10. Result/request aggregate and typed-scope review",
        "## 11. Quantity review",
        "## 12. Term value-mode and policy-route review",
        "## 13. CostBundle review",
        "## 14. SettlementProposal review",
        "## 15. Internal-reference and factory/validator parity review",
        "## 16. Serialization and hidden-information review",
        "## 17. Corpus-scale and owner-boundary review",
        "## 18. Risk and hardening ledger",
        "## 19. Gate decision",
        "## 20. Recommended next PR",
        "## 21. Non-implementation reaffirmation and classification block",
    ]
    for heading in headings:
        assert heading in text


def test_backend_first_invariant_and_non_implementation_boundary() -> None:
    invariant = section(2)
    for token in [
        "The LLM is not the game engine",
        "References are not calculations",
        "Results are not state",
        "Settlement proposals are not transactions",
        "`validation_ready` is not `validation_passed`",
        "Donor text, narration, generated content, and source-local constructs cannot grant resource authority",
        "Runtime validation cannot promote canon",
        "no resource calculation",
        "canon promotion",
    ]:
        assert token in invariant
    classification = section(21)
    for token in [
        "no `resource_consequence_math.py`",
        "no formula or expression evaluator",
        "no persistence structure",
        "no settlement executor",
        "runtime_code_authorized_by_this_pr: false",
        "domain_code_authorized_by_this_pr: false",
        "canon_promotion_authorized_by_this_pr: false",
    ]:
        assert token in classification


def test_scope_review_and_no_runtime_domain_implementation_file_added() -> None:
    scope = section(3)
    for token in [
        "four-file planning/tracking footprint",
        "No runtime/domain implementation changes",
        "Registry and decision tracking are consistent",
        "PR-5G was selected as the sole next step",
    ]:
        assert token in scope
    assert DOMAIN_RESOURCE_MATH.exists()
    assert {p.name for p in DOMAIN_DIR.iterdir() if p.is_file()} == set(AUTHORIZED_RUNTIME_DOMAIN_FILES)
    kernel_files = {p.name for p in KERNEL_DIR.iterdir() if p.is_file()}
    assert {
        "__init__.py",
        "command_envelope.py",
        "context_projection.py",
        "event_ledger.py",
        "hidden_information.py",
        "persistence_boundary.py",
        "record_identity.py",
        "replay_audit.py",
        "rng_interface.py",
    } <= kernel_files


def test_pr_5e_closure_matrix_uses_required_statuses() -> None:
    matrix = section(4)
    for token in [
        "subject_ref dependency binding",
        "unit_ref dependency binding",
        "dimension_ref dependency binding",
        "optional-unsatisfied dependency semantics",
        "precision and scale",
        "source-literal character rules",
        "negative-value policy",
        "blocked numeric choice",
        "term value modes",
        "policy-only routes",
        "bundle bounds",
        "result/request aggregate validation",
        "typed result scope",
        "proposal/result equality",
        "proposal result eligibility",
        "event-only routing",
        "factory/validator parity",
        "closed",
        "partially closed",
    ]:
        assert token in matrix
    assert "not closed" not in matrix.lower()
    assert "deferred with named owner" not in matrix.lower()


def test_effective_contract_inventory_covers_constants_dataclasses_defaults_and_serialization() -> None:
    inventory = section(5)
    for token in [
        "public constants",
        "`ResourceMathSubjectReference`",
        "`ResourceReference`",
        "`QuantitySpecification`",
        "`CostTerm`",
        "`ConsequenceTerm`",
        "`CostBundle`",
        "`ResourceMathDependency`",
        "`ResourceMathRequest`",
        "`ResourceMathResult`",
        "`SettlementProposal`",
        "defaults",
        "aggregate validator context",
        "false-only authority fields",
        "serialization posture",
        "cannot yet derive one unambiguous effective contract",
    ]:
        assert token in inventory


def test_constant_surface_and_stage_decision_blocker_review() -> None:
    constants = section(6)
    for token in [
        "stages and decisions",
        "resource, cost, and consequence families",
        "timing and outcome policies",
        "quantity kinds and representations",
        "negative-value policies",
        "visibility",
        "dependency types",
        "subject types, roles, and owner domains",
        "term value modes",
        "term policy routes",
        "atomicity, ordering, and partial-settlement",
        "no donor-specific construct becomes Astra default law",
    ]:
        assert token in constants
    blockers = section(7)
    for token in [
        "lawful terminal quarantine and escalation pairs",
        "blocked missing-dependency route",
        "blocked pending numeric-choice route",
        "owner-handoff route",
        "No accepted or normalized result can contain a scoped blocker",
        "no blocked result can become settlement-eligible",
        "simultaneous blockers require one deterministic result",
        "unsatisfied binding dependency lifecycle",
    ]:
        assert token in blockers


def test_external_reference_dependency_matrix() -> None:
    matrix = section(8)
    for token in [
        "subject",
        "unit",
        "dimension",
        "command",
        "action legality",
        "state projection",
        "validation request/result",
        "trace",
        "provenance",
        "owner handoff",
        "RNG/table result",
        "request/result",
        "state delta",
        "transaction",
        "event commitment",
        "rollback accounting",
        "No command execution implied",
        "no RNG execution",
        "no event append",
        "no rollback execution",
        "ID uniqueness",
        "`(dependency_type, reference_id)` uniqueness",
    ]:
        assert token in matrix


def test_optional_unsatisfied_and_result_request_typed_scope_reviews() -> None:
    optional = section(9)
    for token in [
        "Binding dependencies",
        "must be `required=True` and `satisfied=True`",
        "Required unsatisfied dependencies",
        "force `blocked_missing_dependency`",
        "Advisory optional unsatisfied dependencies",
        "whether a blocked result may carry an unsatisfied binding dependency",
        "whether a request may contain an incomplete required dependency",
        "non-blocking results can contain only advisory unsatisfied dependencies",
    ]:
        assert token in optional
    typed_scope = section(10)
    for token in [
        "result factories and validators to receive the supplied request",
        "request ID equality",
        "`resource_math_request_ref` binding",
        "typed result-scope fields",
        "unique and resolve in the supplied request",
        "bundle scope over contained terms",
        "term scope over quantities and dependencies",
        "ignore unscoped records",
        "`normalized_reference_ids` diagnostic only",
        "empty typed result scope",
        "accepted/normalized results require at least one scoped",
    ]:
        assert token in typed_scope


def test_quantity_term_policy_bundle_and_proposal_reviews() -> None:
    quantity = section(11)
    for token in [
        "integer precision and scale types",
        "representation-specific lexical grammars",
        "no Decimal/Fraction/float/arithmetic/rounding/conversion/affordability execution",
        "source-literal whitespace/control/surrogate handling",
        "lexical negativity including `-0`",
        "source-supported negative provenance",
        "owner-handoff-negative routing",
        "blocked pending numeric-choice routing",
        "same source-literal character contract",
    ]:
        assert token in quantity
    term = section(12)
    for token in [
        "`resource_quantity`",
        "`resource_reference_only`",
        "`quantity_only`",
        "`policy_only`",
        "`owner_handoff_required`",
        "`quarantine_required`",
        "`doctrine_escalation_required`",
        "Non-policy terms require `policy_route=None`",
        "no policy-only term reaches accepted, normalized, or `SettlementProposal`",
        "never infers route from donor wording",
    ]:
        assert token in term
    bundle = section(13)
    for token in [
        "term IDs",
        "alternative groups",
        "positive non-bool min/max selection bounds",
        "selected-term counting semantics",
        "all-or-nothing requested rule",
        "no selection or settlement execution",
        "complete inherited atomicity surface",
        "every unlisted combination is invalid",
    ]:
        assert token in bundle
    proposal = section(14)
    for token in [
        "proposal validation receives a supplied result",
        "result ID and validation fields match",
        "`validation_passed` is required",
        "stage is `calculation_ready_for_review`",
        "decision is accepted or normalized",
        "non-blocking, non-quarantined, non-escalated",
        "proposed state-delta refs are non-empty and unique",
        "event-only and policy-only terms do not create proposals",
        "supplied original request",
        "prior result/request validation prerequisite",
    ]:
        assert token in proposal


def test_factory_validator_serialization_corpus_and_owner_boundary_reviews() -> None:
    parity = section(15)
    for token in [
        "internal uniqueness and resolution",
        "external binding",
        "quantity lexical rules",
        "blocker precedence",
        "term modes and routes",
        "bundle rules",
        "result/request compatibility",
        "proposal/result compatibility",
        "false-only authority",
        "tuple/metadata immutability",
        "Manual frozen-dataclass construction must not bypass the rules",
    ]:
        assert token in parity
    serialization = section(16)
    for token in [
        "internal `to_dict` only",
        "no `to_public_dict`",
        "defensive copies",
        "no calculations during serialization",
        "no public/model/player/GM projection",
        "RT-005 owns later redaction and visibility",
        "Hidden literals, quantities, provenance, dependencies, and IDs cannot leak",
    ]:
        assert token in serialization
    corpus = section(17)
    for token in [
        "fantasy and sci-fi",
        "cultivation",
        "class/archetype",
        "professions",
        "point-buy and narrative currencies",
        "cyberware/biotech",
        "psionics",
        "horror/investigation",
        "vehicles/mechs/ships",
        "companions/summons",
        "crafting/salvage/requisition",
        "mission/faction/debt",
        "source-local cosmologies",
        "generated content",
        "persistent campaign consequences",
        "direct, normalized, source-local, owner-handoff, quarantine, and doctrine-escalation destinations",
        "RT-002 does not absorb combat, ability, inventory, mission, social, RNG, hidden-information, persistence, event, or canon ownership",
    ]:
        assert token in corpus


def test_risk_and_hardening_ledgers_include_required_risks() -> None:
    ledger = section(18)
    for token in [
        "layered planning artifacts produce conflicting effective fields",
        "inherited constant silently dropped",
        "unsatisfied binding dependency contract conflicts",
        "empty typed scope is ambiguous",
        "blocker precedence is incomplete",
        "source-supported negative literal has undefined character posture",
        "policy route can be bypassed",
        "bundle policy surface is incompletely reviewed",
        "proposal result was not validated against its request",
        "hidden data leaks through serialization",
        "PR-5A must invent a validator rule",
        "severity",
        "current mitigation",
        "required before PR-5A",
        "required before executable calculation",
        "owner",
        "PR-5H required",
    ]:
        assert token in ledger
    assert ledger.count("true") >= 8
    assert ledger.count("false") >= 2


def test_exactly_one_gate_finding_and_selected_next_step() -> None:
    text = read(ARTIFACT)
    gate = section(19)
    assert text.count("gate_finding:") == 1
    assert "PR-5G selects exactly one outcome: **HARDENING**" in gate
    for token in [
        "resource_consequence_math_residual_planning_review_complete: true",
        "pr_5f_scope_confirmed: true",
        "pr_5e_blockers_closed: partially",
        "effective_contract_inventory_unambiguous: false",
        "constant_surfaces_acceptable: partially",
        "optional_dependency_contract_acceptable: partially",
        "term_value_mode_and_policy_route_contract_acceptable: true",
        "serialization_boundary_acceptable: true",
        "requires_pr_5h_before_pr_5a: true",
        "ready_for_pr_5a_skeleton_implementation: false",
        "runtime_code_authorized_by_this_pr: false",
        "domain_code_authorized_by_this_pr: false",
        "next_step_authorized: RUNTIME-DOMAIN-PR-5H resource and consequence math final residual planning hardening",
        "next_step_status: planning_hardening_pending_review",
    ]:
        assert token in gate
    recommended = section(20)
    assert "RUNTIME-DOMAIN-PR-5H final residual planning hardening" in recommended
    assert "RUNTIME-DOMAIN-PR-5A reference-only skeleton implementation" not in recommended


def test_registry_record_and_decision_heading_exactly_once_and_registry_version_unchanged() -> None:
    registry = read(REGISTRY)
    decisions = read(DECISIONS)
    assert registry.count(PR5G_ID) == 1
    assert decisions.count(f"## {PR5G_ID}") == 1
    assert re.search(r"^registry_version: 0\.1\.0$", registry, flags=re.M)
    for token in [
        "version: 0.1.89",
        "review_only: true",
        "pr_5h_required_before_pr_5a: true",
        "pr_5a_authorized: false",
        "next_step_authorized: RUNTIME-DOMAIN-PR-5H resource and consequence math final residual planning hardening",
        "runtime_code_authorized_by_this_pr: false",
        "domain_code_authorized_by_this_pr: false",
    ]:
        assert token in registry
    for token in [
        "review-only status is recorded for PR-5G",
        "PR-5F scope is confirmed",
        "PR-5E blockers are partially closed",
        "PR-5H is required before PR-5A",
        "PR-5A is not authorized",
        "sole next step",
        "authorizes no implementation",
    ]:
        assert token in decisions


def test_no_unauthorized_runtime_or_kernel_implementation_file_added() -> None:
    changed_paths = {line.split(maxsplit=1)[-1] for line in _git_status_short()}
    domain_kernel_changed = {
        path for path in changed_paths
        if path.startswith("src/astra_runtime/domain/") or path.startswith("src/astra_runtime/kernel/")
    }
    assert domain_kernel_changed <= {
        "src/astra_runtime/domain/resource_consequence_math.py",
        "src/astra_runtime/domain/__init__.py",
        "src/astra_runtime/domain/scene_command_execution_skeleton.py",
        "src/astra_runtime/domain/command_kind_routing_skeleton.py",
        "src/astra_runtime/domain/action_legality_skeleton.py",
        "src/astra_runtime/domain/action_legality_gate_integration_skeleton.py",
    }


def _git_status_short() -> list[str]:
    import subprocess

    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]

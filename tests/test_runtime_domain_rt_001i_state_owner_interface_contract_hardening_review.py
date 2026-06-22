"""Tests for RT-001I: State Owner Interface Contract Hardening Review.

Covers: review document existence and required content, RT-001H test pass,
RT-001B through RT-001G relevant test pass (excluding branch-specific
no-modification checks), registry/decision-log RT-001I entries, and branch
diff containment.
"""

from __future__ import annotations

import pathlib
import subprocess
from typing import Any

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
REVIEW_ARTIFACT_PATH = (
    REPO_ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.md"
)
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"


# ---------------------------------------------------------------------------
# T1 — Review document exists
# ---------------------------------------------------------------------------


class TestReviewDocumentExists:
    def test_review_artifact_exists(self):
        assert REVIEW_ARTIFACT_PATH.exists(), "RT-001I review document must exist"

    def test_review_artifact_is_markdown(self):
        assert REVIEW_ARTIFACT_PATH.suffix == ".md"


# ---------------------------------------------------------------------------
# T2 — Review document states RT-001I is review-only
# ---------------------------------------------------------------------------


class TestReviewDocumentReviewOnly:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_review_only_phrase_present(self, review_text: str):
        assert "review-only" in review_text.lower(), (
            "Review document must state it is review-only"
        )

    def test_no_implementation_authority_phrase_present(self, review_text: str):
        assert "no implementation authority" in review_text.lower(), (
            "Review document must disclaim implementation authority"
        )

    def test_authorizes_implementation_is_false(self, review_text: str):
        assert "authorizes_implementation: false" in review_text, (
            "Classification block must state authorizes_implementation: false"
        )


# ---------------------------------------------------------------------------
# T3 — Review document names RT-001H and PR #318
# ---------------------------------------------------------------------------


class TestReviewDocumentNamesRt001hAndPr318:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_names_rt001h(self, review_text: str):
        assert "RT-001H" in review_text, "Review document must name RT-001H"

    def test_names_pr_318(self, review_text: str):
        assert "PR #318" in review_text, "Review document must name PR #318"


# ---------------------------------------------------------------------------
# T4 — Review document inventories the RT-001H public surface
# ---------------------------------------------------------------------------


class TestReviewDocumentInventoriesPublicSurface:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    @pytest.mark.parametrize(
        "heading",
        [
            "Constants",
            "Error hierarchy",
            "Dataclasses",
            "Factory functions",
            "Builder functions",
            "Serializers",
            "Validators",
        ],
    )
    def test_includes_public_surface_headings(self, review_text: str, heading: str):
        assert heading in review_text, (
            f"Review document public surface inventory must include {heading!r}"
        )

    def test_inventories_authority_flags_dataclass(self, review_text: str):
        assert "StateOwnerInterfaceAuthorityFlags" in review_text

    def test_inventories_reference_dataclass(self, review_text: str):
        assert "StateOwnerInterfaceReference" in review_text

    def test_inventories_visibility_descriptor(self, review_text: str):
        assert "StateVisibilityDescriptor" in review_text

    def test_inventories_projection_request_reference(self, review_text: str):
        assert "StateProjectionRequestReference" in review_text


# ---------------------------------------------------------------------------
# T5 — Constructor/factory/validator parity audit
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesParityAudit:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_parity_audit_section(self, review_text: str):
        assert "## 4. Constructor/factory/validator parity audit" in review_text

    def test_parity_audit_table_present(self, review_text: str):
        assert "Constructor `__post_init__`" in review_text
        assert "Factory routes through constructor" in review_text

    def test_notes_acceptable_skeleton_phase_debt(self, review_text: str):
        assert "acceptable skeleton-phase debt" in review_text.lower()


# ---------------------------------------------------------------------------
# T6 — Authority flag hardening audit
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesAuthorityFlagAudit:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_authority_flag_audit_section(self, review_text: str):
        assert "## 5. Authority flag hardening audit" in review_text

    def test_confirms_false_only(self, review_text: str):
        assert "false-only" in review_text.lower()

    def test_confirms_to_dict_hardcodes_false(self, review_text: str):
        assert "to_dict()` hardcodes" in review_text.lower() or "to_dict()` hardcoding" in review_text.lower()


# ---------------------------------------------------------------------------
# T7 — Hidden-information containment audit
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesHiddenInformationAudit:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_hidden_information_section(self, review_text: str):
        assert "## 6. Hidden-information containment audit" in review_text

    def test_hidden_information_policies_controlled(self, review_text: str):
        assert "STATE_OWNER_HIDDEN_INFORMATION_POLICIES" in review_text

    def test_rejects_arbitrary_policies(self, review_text: str):
        assert "rejects arbitrary" in review_text.lower()

    def test_rejects_forbidden_metadata_keys(self, review_text: str):
        assert "rejects forbidden metadata keys" in review_text.lower()


# ---------------------------------------------------------------------------
# T8 — Visibility descriptor metadata containment audit
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesVisibilityDescriptorAudit:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_visibility_descriptor_section(self, review_text: str):
        assert "## 7. Visibility descriptor and metadata containment audit" in review_text

    def test_visibility_tier_controlled(self, review_text: str):
        assert "STATE_OWNER_VISIBILITY_TIERS" in review_text

    def test_forbidden_keys_listed(self, review_text: str):
        assert "hidden_fact" in review_text
        assert "backend_only_fact" in review_text
        assert "state_payload" in review_text


# ---------------------------------------------------------------------------
# T9 — Serializer containment audit
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesSerializerAudit:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_serializer_section(self, review_text: str):
        assert "## 10. Serializer containment audit" in review_text

    def test_backend_serializer_deterministic(self, review_text: str):
        assert "deterministic" in review_text.lower()

    def test_visible_serializer_excludes_forbidden_keys(self, review_text: str):
        assert "Forbidden fields confirmed absent from visible output" in review_text


# ---------------------------------------------------------------------------
# T10 — Import boundary audit
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesImportBoundaryAudit:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_import_boundary_section(self, review_text: str):
        assert "## 11. Import boundary audit" in review_text

    def test_confirms_no_forbidden_module_imports(self, review_text: str):
        assert "Forbidden modules NOT imported" in review_text
        assert "state_store" in review_text
        assert "state_projection" in review_text


# ---------------------------------------------------------------------------
# T11 — Export surface audit
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesExportSurfaceAudit:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_export_surface_section(self, review_text: str):
        assert "## 12. Export surface audit" in review_text

    def test_domain_init_exports_mentioned(self, review_text: str):
        assert "astra_runtime/domain/__init__.py" in review_text


# ---------------------------------------------------------------------------
# T12 — Registry and decision-log consistency audit
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesRegistryDecisionLogAudit:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_registry_section(self, review_text: str):
        assert "## 13. Registry and decision-log consistency audit" in review_text

    def test_registry_rt001h_record_mentioned(self, review_text: str):
        assert "state_owner_interface_contract_skeleton.py" in review_text


# ---------------------------------------------------------------------------
# T13 — Guardrail and branch-specific test audit
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesGuardrailAudit:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_guardrail_section(self, review_text: str):
        assert "## 14. Guardrail and branch-specific test audit" in review_text

    def test_pr9b_allowlist_mentioned(self, review_text: str):
        assert "PR-9B" in review_text or "scene command execution" in review_text.lower()


# ---------------------------------------------------------------------------
# T14 — Corpus-scale donor pressure audit
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesDonorPressureAudit:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_donor_pressure_section(self, review_text: str):
        assert "## 15. Corpus-scale donor pressure audit" in review_text

    def test_donor_action_economy_mentioned(self, review_text: str):
        assert "donor" in review_text.lower()


# ---------------------------------------------------------------------------
# T15 — RT-002 readiness assessment
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesReadinessAssessment:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_includes_readiness_section(self, review_text: str):
        assert "## 16. RT-002 readiness assessment" in review_text

    def test_includes_constraints_section(self, review_text: str):
        assert "## 18. Required RT-002A constraints" in review_text


# ---------------------------------------------------------------------------
# T16 — All required risk ledger categories
# ---------------------------------------------------------------------------


class TestReviewDocumentIncludesAllRiskLedgerCategories:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    _REQUIRED_RISKS = [
        "constructor/factory/validator divergence risk",
        "hidden-information policy drift risk",
        "forbidden metadata key bypass risk",
        "visible serializer leakage risk",
        "backend serializer overexposure risk",
        "authority flag bypass risk",
        "raw state access temptation risk",
        "projection materialization drift risk",
        "request/result status adjudication drift risk",
        "import boundary erosion risk",
        "export surface creep risk",
        "registry/decision-log drift risk",
        "branch-specific guardrail masking risk",
        "donor action-economy leakage risk",
        "RT-002A scope creep risk",
    ]

    @pytest.mark.parametrize("risk", _REQUIRED_RISKS)
    def test_risk_ledger_includes_category(self, review_text: str, risk: str):
        normalized = review_text.lower()
        key = risk.lower().replace("/", " ").replace("-", " ")
        parts = key.split()
        assert all(part in normalized for part in parts), (
            f"Risk ledger must include category matching {risk!r}"
        )


# ---------------------------------------------------------------------------
# T17 — Review document concludes with one of the readiness conclusions
# ---------------------------------------------------------------------------


class TestReviewDocumentReadinessConclusion:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_concludes_with_one_of_three_options(self, review_text: str):
        conclusions = [
            "READY_FOR_RT_002A",
            "READY_WITH_CONSTRAINTS_FOR_RT_002A",
            "BLOCKED_BEFORE_RT_002A",
        ]
        assert any(c in review_text for c in conclusions), (
            "Review document must conclude with one of the three readiness options"
        )

    def test_classification_block_has_conclusion(self, review_text: str):
        assert "rt_002_readiness_conclusion:" in review_text


# ---------------------------------------------------------------------------
# T18 — Review document lists RT-002A constraints
# ---------------------------------------------------------------------------


class TestReviewDocumentListsRt002aConstraints:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_lists_read_only_constraint(self, review_text: str):
        assert "read-only" in review_text.lower()

    def test_lists_no_mutation_constraint(self, review_text: str):
        assert "No mutation" in review_text

    def test_lists_no_legality_evaluation_constraint(self, review_text: str):
        assert "No legality evaluation" in review_text

    def test_lists_vertical_slice_constraint(self, review_text: str):
        assert "vertical slice" in review_text.lower()


# ---------------------------------------------------------------------------
# T19 — Review document recommends next step as RT-002A
# ---------------------------------------------------------------------------


class TestReviewDocumentRecommendsRt002a:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_next_step_is_rt002a(self, review_text: str):
        assert "RT-002A" in review_text
        assert "Read-Only Vertical Slice State Owner Facade" in review_text

    def test_next_allowed_step_in_classification_block(self, review_text: str):
        assert "next_allowed_step: RT-002A" in review_text


# ---------------------------------------------------------------------------
# T20 — Review document says no RT-001J is required unless blocker
# ---------------------------------------------------------------------------


class TestReviewDocumentNoRt001jUnlessBlocker:
    @pytest.fixture
    def review_text(self) -> str:
        return REVIEW_ARTIFACT_PATH.read_text(encoding="utf-8")

    def test_no_rt001j_unless_blocker(self, review_text: str):
        assert "no RT-001J" in review_text.lower() or "RT-001J" in review_text


# ---------------------------------------------------------------------------
# T21 — RT-001H tests pass
# ---------------------------------------------------------------------------


class TestRt001hTestsPass:
    def test_rt001h_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001h_state_owner_interface_contract_skeleton.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001H tests failed:\n{result.stdout}\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# T22 — RT-001B through RT-001G relevant tests pass
# ---------------------------------------------------------------------------


class TestEarlierRtTestsPass:
    def test_rt001b_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001b_action_legality_skeleton.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001B tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001c_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001c_action_legality_gate_integration_skeleton.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001C tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001d_tests_pass_excluding_branch_guardrail(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001d_action_legality_integration_hardening_review.py",
                "-q", "--tb=short",
                "-k", "not TestImplementationModuleSafety",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001D tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001e_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001e_action_legality_service_interface_contract_skeleton.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001E tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001f_tests_pass_excluding_branch_guardrail(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.py",
                "-q", "--tb=short",
                "-k", "not TestExistingTestsStillPass",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001F tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001g_tests_pass_excluding_branch_guardrail(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001g_state_owner_interface_prerequisite_review.py",
                "-q", "--tb=short",
                "-k", "not TestNoModificationOfRuntimeModules and not TestExistingTestsStillPass",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001G functional tests failed:\n{result.stdout}\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# T23 — Registry contains RT-001I review record
# ---------------------------------------------------------------------------


class TestRegistryContainsRt001iRecord:
    @pytest.fixture
    def registry(self) -> dict[str, Any]:
        return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_registry_contains_rt001i_file_record(self, registry: dict[str, Any]):
        file_records = registry.get("file_records", [])
        rt001i_records = [
            r for r in file_records
            if "RT-001I" in str(r.get("file_id", "")) or
            "runtime_domain_rt_001i" in str(r.get("filename", ""))
        ]
        assert rt001i_records, "Registry does not contain RT-001I file record"

    def test_registry_rt001i_record_authority_level_review(self, registry: dict[str, Any]):
        file_records = registry.get("file_records", [])
        rt001i_records = [
            r for r in file_records
            if "RT-001I" in str(r.get("file_id", "")) or
            "runtime_domain_rt_001i" in str(r.get("filename", ""))
        ]
        assert rt001i_records
        for record in rt001i_records:
            authority = str(record.get("authority_level", "")).lower()
            assert authority == "review", (
                f"RT-001I registry record must have authority_level 'review', got {authority!r}"
            )

    def test_registry_rt001i_record_notes_review_only(self, registry: dict[str, Any]):
        file_records = registry.get("file_records", [])
        rt001i_records = [
            r for r in file_records
            if "RT-001I" in str(r.get("file_id", "")) or
            "runtime_domain_rt_001i" in str(r.get("filename", ""))
        ]
        assert rt001i_records
        for record in rt001i_records:
            notes = str(record.get("notes", "")).lower()
            assert "review-only" in notes, (
                "RT-001I registry record notes must state review-only"
            )

    def test_registry_changelog_contains_rt001i(self, registry: dict[str, Any]):
        changelog = registry.get("changelog", [])
        assert any(
            "rt_001i" in str(entry.get("action", "")).lower() or
            "RT-001I" in str(entry.get("action", ""))
            for entry in changelog
        ), "Registry changelog must contain RT-001I entry"


# ---------------------------------------------------------------------------
# T24 — Decision log contains RT-001I entry
# ---------------------------------------------------------------------------


class TestDecisionLogContainsRt001iEntry:
    @pytest.fixture
    def log_text(self) -> str:
        return DECISION_LOG_PATH.read_text(encoding="utf-8")

    def test_decision_log_contains_rt001i(self, log_text: str):
        assert "RUNTIME-DOMAIN-RT-001I" in log_text, (
            "Decision log does not contain RT-001I entry"
        )

    def test_decision_log_rt001i_is_review_only(self, log_text: str):
        assert "review-only" in log_text.lower()

    def test_decision_log_rt001i_references_rt001h(self, log_text: str):
        assert "RT-001H" in log_text

    def test_decision_log_rt001i_recommends_rt002a(self, log_text: str):
        assert "RT-002A" in log_text
        assert "Read-Only Vertical Slice State Owner Facade" in log_text


# ---------------------------------------------------------------------------
# T25 — RT-001I branch does not modify runtime implementation modules
# ---------------------------------------------------------------------------


class TestBranchDiffContained:
    _ALLOWED_PATTERNS = (
        "docs/doctrine/reviews/runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.md",
        "tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py",
        "docs/decisions/current_decisions_log.md",
        "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
    )

    def test_branch_diff_is_limited_to_allowed_files(self):
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True, text=True, check=True, cwd=REPO_ROOT,
        )
        changed = [p for p in result.stdout.strip().splitlines() if p.strip()]
        for path in changed:
            assert any(path.endswith(pat) or path == pat for pat in self._ALLOWED_PATTERNS), (
                f"RT-001I branch modifies unexpected file: {path}"
            )

    def test_no_runtime_implementation_module_modified(self):
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True, text=True, check=True, cwd=REPO_ROOT,
        )
        changed = [p for p in result.stdout.strip().splitlines() if p.strip()]
        for path in changed:
            assert not path.startswith("src/astra_runtime/"), (
                f"RT-001I branch must not modify runtime implementation modules: {path}"
            )

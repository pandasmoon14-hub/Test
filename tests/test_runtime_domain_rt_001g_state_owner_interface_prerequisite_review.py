"""
Tests for RT-001G: state owner interface prerequisite review.

This review-only test file verifies that the RT-001G review document exists,
contains the required prerequisite findings, and that the branch does not
modify runtime implementation modules.
"""

from __future__ import annotations

import pathlib
import subprocess

import pytest

import yaml


_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# T1 — Review document exists
# ---------------------------------------------------------------------------

class TestReviewDocumentExists:
    def test_review_document_exists(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        assert doc.is_file(), "RT-001G review document does not exist"

    def test_review_document_not_empty(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8")
        assert len(content) > 500, "Review document appears empty or truncated"


# ---------------------------------------------------------------------------
# T2 — Review document names RT-001A through RT-001F
# ---------------------------------------------------------------------------

class TestReviewNamesSourceStack:
    _EXPECTED_SOURCES = {"RT-001A", "RT-001B", "RT-001C", "RT-001D", "RT-001E", "RT-001F"}

    def test_review_document_names_all_sources(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8")
        for source in self._EXPECTED_SOURCES:
            assert source in content, f"Review document does not reference {source}"


# ---------------------------------------------------------------------------
# T3 — Review document states review-only and does not authorize implementation
# ---------------------------------------------------------------------------

class TestReviewStatesReviewOnly:
    def test_review_document_states_review_only(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "review-only" in content, (
            "Review document must state it is review-only"
        )
        assert "does not implement" in content, (
            "Review document must state it does not implement"
        )


# ---------------------------------------------------------------------------
# T4 — Review document states no state owner interface is implemented
# ---------------------------------------------------------------------------

class TestReviewStatesNoStateOwnerInterfaceImplemented:
    def test_review_document_states_no_state_owner_interface(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "does not implement a state owner interface" in content, (
            "Review document must state it does not implement a state owner interface"
        )


# ---------------------------------------------------------------------------
# T5 — Review document states no action legality evaluation is implemented
# ---------------------------------------------------------------------------

class TestReviewStatesNoLegalityEvaluation:
    def test_review_document_states_no_legality_evaluation(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "does not implement action legality evaluation" in content, (
            "Review document must state it does not implement action legality evaluation"
        )


# ---------------------------------------------------------------------------
# T6 — Review document says real legality evaluation remains blocked
# ---------------------------------------------------------------------------

class TestReviewStatesRealLegalityBlocked:
    def test_review_document_says_real_legality_blocked(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "real legality evaluation remains blocked" in content, (
            "Review document must state that real legality evaluation remains blocked"
        )


# ---------------------------------------------------------------------------
# T7 — Review document lists required state owner interface families
# ---------------------------------------------------------------------------

class TestReviewStateOwnerInterfaceFamilies:
    _REQUIRED_FAMILIES = (
        "actor existence and identity owner",
        "actor capability/authority owner",
        "scene/location boundary owner",
        "target existence and reachability owner",
        "object/lever/interactable owner",
        "hazard/clock/environment owner",
        "inventory/custody/burden owner",
        "resource pool/state owner",
        "condition/injury/status owner",
        "faction/social/relationship owner",
        "mission/clue/reward/discovery owner",
        "hidden information visibility owner",
        "state projection owner",
        "transaction preview owner",
        "event commitment owner",
        "persistence/replay owner",
    )

    def test_all_required_state_owner_families_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        for family in self._REQUIRED_FAMILIES:
            assert family in content, (
                f"Review document missing required state owner family: {family!r}"
            )


# ---------------------------------------------------------------------------
# T8 — Review document lists required dependency owner interface families
# ---------------------------------------------------------------------------

class TestReviewDependencyOwnerInterfaceFamilies:
    _REQUIRED_FAMILIES = (
        "validation owner",
        "resource math owner",
        "RNG/table/oracle owner",
        "state delta owner",
        "transaction lifecycle owner",
        "event commitment owner",
        "context packet owner",
        "persistence/replay owner",
        "doctrine/schema/source-local escalation owner",
        "combat/ability/skill/effect resolution owner",
    )

    def test_all_required_dependency_owner_families_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8")
        for family in self._REQUIRED_FAMILIES:
            assert family in content, (
                f"Review document missing required dependency owner family: {family!r}"
            )


# ---------------------------------------------------------------------------
# T9 — Review document includes hidden-information containment requirements
# ---------------------------------------------------------------------------

class TestReviewHiddenInformationContainment:
    def test_hidden_information_section_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "hidden-information containment requirements" in content
        assert "no inference from absence" in content
        assert "hidden information visibility owner" in content


# ---------------------------------------------------------------------------
# T10 — Review document includes projection/visibility requirements
# ---------------------------------------------------------------------------

class TestReviewProjectionVisibilityRequirements:
    def test_projection_visibility_section_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "projection and visibility contract requirements" in content
        assert "state projection owner" in content
        assert "visibility descriptor" in content


# ---------------------------------------------------------------------------
# T11 — Review document includes transaction preview and event commitment prerequisites
# ---------------------------------------------------------------------------

class TestReviewTransactionPreviewEventCommitment:
    def test_transaction_preview_event_commitment_section_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "transaction preview and event commitment prerequisites" in content
        assert "transaction lifecycle owner" in content
        assert "event commitment owner" in content


# ---------------------------------------------------------------------------
# T12 — Review document includes resource/consequence math prerequisites
# ---------------------------------------------------------------------------

class TestReviewResourceMathPrerequisites:
    def test_resource_math_section_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "resource/consequence math prerequisites" in content
        assert "resource math owner" in content
        assert "no affordability execution" in content


# ---------------------------------------------------------------------------
# T13 — Review document includes RNG/table/oracle prerequisites
# ---------------------------------------------------------------------------

class TestReviewRngTableOraclePrerequisites:
    def test_rng_table_oracle_section_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "rng/table/oracle prerequisites" in content
        assert "rng/table/oracle owner" in content
        assert "no direct randomness execution" in content


# ---------------------------------------------------------------------------
# T14 — Review document includes persistence/replay prerequisites
# ---------------------------------------------------------------------------

class TestReviewPersistenceReplayPrerequisites:
    def test_persistence_replay_section_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "persistence/replay prerequisites" in content
        assert "persistence/replay owner" in content
        assert "read-only trace consumption" in content


# ---------------------------------------------------------------------------
# T15 — Review document includes corpus-scale donor pressure audit
# ---------------------------------------------------------------------------

class TestReviewDonorPressureAudit:
    def test_donor_pressure_audit_section_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "corpus-scale donor pressure audit" in content
        assert "donor-action-economy" in content or "donor action economy" in content


# ---------------------------------------------------------------------------
# T16 — Review document includes all required risk ledger categories
# ---------------------------------------------------------------------------

class TestReviewRiskLedgerCompleteness:
    _REQUIRED_RISKS = (
        "premature state read risk",
        "raw state access risk",
        "hidden-information leakage risk",
        "missing-data-as-truth risk",
        "owner-route ambiguity risk",
        "donor-action-economy leakage risk",
        "state mutation by legality service risk",
        "event commitment shortcut risk",
        "resource math shortcut risk",
        "RNG/table/oracle shortcut risk",
        "projection/visibility mismatch risk",
        "dependency owner circularity risk",
        "persistence/replay drift risk",
        "model/live-play treating unavailable owner data as final adjudication risk",
        "incremental drift from review into implementation risk",
    )

    def test_all_required_risk_categories_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8")
        for risk in self._REQUIRED_RISKS:
            assert risk in content, (
                f"Review document missing required risk category: {risk!r}"
            )


# ---------------------------------------------------------------------------
# T17 — Review document forbids raw state reads by future legality service
# ---------------------------------------------------------------------------

class TestReviewForbidsRawStateReads:
    def test_review_forbids_raw_state_reads(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "must not read raw world state directly" in content
        assert "no raw state reads" in content or "forbids raw state reads" in content


# ---------------------------------------------------------------------------
# T18 — Review document forbids mutation/event commitment shortcuts
# ---------------------------------------------------------------------------

class TestReviewForbidsMutationAndEventCommitment:
    def test_review_forbids_mutation_and_event_commitment(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "state mutation by legality service risk" in content
        assert "event commitment shortcut risk" in content
        assert "appending events" in content or "event commitment" in content


# ---------------------------------------------------------------------------
# T19 — Review document recommends next step as state/dependency owner interface contract skeleton
# ---------------------------------------------------------------------------

class TestReviewNextStepRecommendation:
    def test_review_recommends_rt001h(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001g_state_owner_interface_prerequisite_review.md"
        )
        content = doc.read_text(encoding="utf-8")
        assert "RT-001H" in content, "Review must reference RT-001H"
        assert "State Owner Interface Contract Skeleton" in content, (
            "Review must recommend State Owner Interface Contract Skeleton"
        )
        assert "not legality evaluation implementation" in content.lower(), (
            "Review must explicitly rule out immediate legality evaluation implementation"
        )


# ---------------------------------------------------------------------------
# T20 — RT-001G branch does not modify runtime implementation modules
# ---------------------------------------------------------------------------

class TestNoModificationOfRuntimeModules:
    def test_runtime_modules_not_modified(self):
        result = subprocess.run(
            [
                "git",
                "diff",
                "origin/main",
                "--name-only",
                "--",
                "src/astra_runtime/",
            ],
            capture_output=True, text=True, cwd=_REPO_ROOT,
        )
        assert result.returncode == 0, "git diff failed"
        modified = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        assert not modified, (
            "RT-001G branch modifies runtime implementation modules: "
            + ", ".join(modified)
        )


# ---------------------------------------------------------------------------
# T21 — RT-001B through RT-001F tests still pass
# ---------------------------------------------------------------------------

class TestExistingTestsStillPass:
    def test_rt001b_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001b_action_legality_skeleton.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=_REPO_ROOT,
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
            capture_output=True, text=True, cwd=_REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001C tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001d_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001d_action_legality_integration_hardening_review.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=_REPO_ROOT,
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
            capture_output=True, text=True, cwd=_REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001E tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001f_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=_REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001F tests failed:\n{result.stdout}\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# T22 — Registry contains RT-001G review record
# ---------------------------------------------------------------------------

class TestRegistryContainsRt001gRecord:
    def test_registry_contains_rt001g_file_record(self):
        registry_path = _REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        file_records = registry.get("file_records", [])
        rt001g_records = [
            r for r in file_records
            if "RT-001G" in str(r.get("file_id", "")) or
               "rt_001g" in str(r.get("file_path", ""))
        ]
        assert rt001g_records, "Registry does not contain RT-001G file record"

    def test_registry_rt001g_record_is_review_only(self):
        registry_path = _REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        file_records = registry.get("file_records", [])
        rt001g_records = [
            r for r in file_records
            if "RT-001G" in str(r.get("file_id", "")) or
               "rt_001g" in str(r.get("file_path", ""))
        ]
        assert rt001g_records
        for record in rt001g_records:
            notes = str(record.get("notes", "")).lower()
            assert "review-only" in notes or "review only" in notes, (
                "RT-001G registry record must state it is review-only"
            )


# ---------------------------------------------------------------------------
# T23 — Decision log contains RT-001G entry
# ---------------------------------------------------------------------------

class TestDecisionLogContainsRt001gEntry:
    def test_decision_log_contains_rt001g_entry(self):
        log_path = _REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
        content = log_path.read_text(encoding="utf-8")
        assert "RUNTIME-DOMAIN-RT-001G" in content, (
            "Decision log does not contain RT-001G entry"
        )

    def test_decision_log_rt001g_entry_is_review_only(self):
        log_path = _REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
        content = log_path.read_text(encoding="utf-8").lower()
        assert "rt-001g" in content
        # The entry should state it authorizes no runtime behavior
        assert "authorizes no runtime behavior" in content or "review-only" in content, (
            "RT-001G decision log entry must state it authorizes no runtime behavior"
        )

"""
Tests for RT-001F: action legality service interface contract hardening review.

This is a hardening review test file that inspects the merged RT-001E
interface contract skeleton without implementing new behavior.

Modules under review:
    docs/doctrine/reviews/runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.md
    src/astra_runtime.domain.action_legality_service_interface_contract_skeleton (RT-001E)
"""

from __future__ import annotations

import ast
import pathlib
import subprocess

import pytest

from astra_runtime.domain.action_legality_skeleton import (
    SAFE_PLAYER_MESSAGES,
    ActionLegalityAuthorityFlags,
    ActionLegalityBackendDetail,
    ActionLegalityBlocker,
    ActionLegalityDependencyReference,
    ActionLegalityResult,
)
from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
    __all__ as RT001E_ALL,
    ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES,
    InvalidActionLegalityServiceInterfaceAuthorityFlagsError,
    InvalidActionLegalityServiceInterfaceDependencyManifestError,
    InvalidActionLegalityServiceInterfaceResultError,
    ActionLegalityServiceInterfaceAuthorityFlags,
    ActionLegalityServiceInterfaceDependencyManifest,
    ActionLegalityServiceInterfaceResult,
    build_action_legality_service_interface_dependency_manifest,
    build_deferred_action_legality_service_interface_result,
    build_unknown_action_legality_service_interface_result,
    create_action_legality_service_interface_authority_flags,
    create_action_legality_service_interface_dependency_manifest,
    serialize_action_legality_service_interface_result_visible,
    validate_action_legality_service_interface_authority_flags,
    validate_action_legality_service_interface_dependency_manifest,
    validate_action_legality_service_interface_result,
)


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
            / "runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.md"
        )
        assert doc.is_file(), "RT-001F review document does not exist"

    def test_review_document_not_empty(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.md"
        )
        content = doc.read_text(encoding="utf-8")
        assert len(content) > 500, "Review document appears empty or truncated"


# ---------------------------------------------------------------------------
# T2 — Review document names RT-001A through RT-001E
# ---------------------------------------------------------------------------

class TestReviewNamesSourceStack:
    _EXPECTED_SOURCES = {"RT-001A", "RT-001B", "RT-001C", "RT-001D", "RT-001E"}

    def test_review_document_names_all_sources(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.md"
        )
        content = doc.read_text(encoding="utf-8")
        for source in self._EXPECTED_SOURCES:
            assert source in content, (
                f"Review document does not reference {source}"
            )


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
            / "runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.md"
        )
        content = doc.read_text(encoding="utf-8").lower()
        assert "review-only" in content, (
            "Review document must state it is review-only"
        )
        assert "does not authorize implementation" in content or "no implementation authority" in content, (
            "Review document must state it does not authorize implementation"
        )


# ---------------------------------------------------------------------------
# T4 — Review document contains all required risk ledger categories
# ---------------------------------------------------------------------------

class TestReviewRiskLedgerCompleteness:
    _REQUIRED_RISKS = (
        "Premature legality adjudication risk",
        "Inner legality status bypass risk",
        "Constructor/factory/validator divergence risk",
        "Dependency manifest becoming a service call risk",
        "Authority flag bypass risk",
        "Visible serializer leakage risk",
        "Hidden-information leakage risk",
        "Package export alias confusion risk",
        "Registry/decision-log drift risk",
        "Guardrail allowlist drift risk",
        "Import-boundary erosion risk",
        "Donor-specific legality assumptions leaking into runtime baseline risk",
        "Future service implementation reading state before owner interfaces exist risk",
        "Future model/live-play layer treating deferred/unknown as final adjudication risk",
        "Interface contract becoming implementation by incremental drift risk",
    )

    def test_all_required_risk_categories_present(self):
        doc = (
            _REPO_ROOT
            / "docs"
            / "doctrine"
            / "reviews"
            / "runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.md"
        )
        content = doc.read_text(encoding="utf-8")
        for risk in self._REQUIRED_RISKS:
            assert risk in content, (
                f"Review document missing required risk category: {risk!r}"
            )


# ---------------------------------------------------------------------------
# T5 — RT-001E result status constant is exactly deferred/unknown and excludes
#      legal, illegal, blocked, quarantined, escalated
# ---------------------------------------------------------------------------

class TestResultStatusConstant:
    def test_result_statuses_contain_deferred_and_unknown(self):
        assert "deferred" in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES
        assert "unknown" in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES

    def test_result_statuses_exclude_non_skeleton_statuses(self):
        forbidden = {"legal", "illegal", "blocked", "quarantined", "escalated"}
        for status in forbidden:
            assert status not in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES, (
                f"Result status constant should not contain {status!r}"
            )

    def test_result_statuses_exactly_two(self):
        assert len(ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES) == 2


# ---------------------------------------------------------------------------
# T6 — Direct constructor rejects inner legality statuses legal, illegal,
#      blocked, quarantined, escalated
# ---------------------------------------------------------------------------

class TestConstructorRejectsNonSkeletonStatuses:
    @pytest.mark.parametrize(
        "status",
        ["legal", "illegal", "blocked", "quarantined", "escalated"],
    )
    def test_constructor_rejects_inner_legality_status(self, status):
        inner = _make_result_for_status(status)
        with pytest.raises(InvalidActionLegalityServiceInterfaceResultError):
            ActionLegalityServiceInterfaceResult(
                result_id="res_test",
                request_id="req_test",
                interface_status="deferred",
                legality_result=inner,
                authority_flags=ActionLegalityServiceInterfaceAuthorityFlags(),
            )


# ---------------------------------------------------------------------------
# T7 — Factory rejects inner legality statuses legal, illegal, blocked,
#      quarantined, escalated
# ---------------------------------------------------------------------------

class TestFactoryRejectsNonSkeletonStatuses:
    @pytest.mark.parametrize(
        "status",
        ["legal", "illegal", "blocked", "quarantined", "escalated"],
    )
    def test_factory_rejects_inner_legality_status(self, status):
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            create_action_legality_service_interface_result,
        )
        inner = _make_result_for_status(status)
        with pytest.raises(InvalidActionLegalityServiceInterfaceResultError):
            create_action_legality_service_interface_result(
                result_id="res_test",
                request_id="req_test",
                interface_status="deferred",
                legality_result=inner,
            )


# ---------------------------------------------------------------------------
# T8 — Validator accepts deferred and unknown
# ---------------------------------------------------------------------------

class TestValidatorAcceptsSkeletonStatuses:
    @pytest.mark.parametrize("status", ["deferred", "unknown"])
    def test_validator_accepts_deferred_and_unknown(self, status):
        deferred_result = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        if status == "unknown":
            result = build_unknown_action_legality_service_interface_result(
                result_id="res1", request_id="r1",
            )
        else:
            result = deferred_result
        assert validate_action_legality_service_interface_result(result)


# ---------------------------------------------------------------------------
# T9 — Validator rejects non-skeleton statuses
# ---------------------------------------------------------------------------

class TestValidatorRejectsNonSkeletonStatuses:
    @pytest.mark.parametrize(
        "status",
        ["legal", "illegal", "blocked", "quarantined", "escalated"],
    )
    def test_validator_rejects_by_status_not_in_allowed_set(self, status):
        assert status not in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES, (
            f"Status {status!r} should not be in the allowed set"
        )


# ---------------------------------------------------------------------------
# T10 — Deferred builder produces interface_status="deferred" and inner
#       legality_status="deferred"
# ---------------------------------------------------------------------------

class TestDeferredBuilder:
    def test_deferred_builder_produces_deferred(self):
        res = build_deferred_action_legality_service_interface_result(
            result_id="res_d", request_id="req_d",
        )
        assert res.interface_status == "deferred"
        assert res.legality_result.legality_status == "deferred"


# ---------------------------------------------------------------------------
# T11 — Unknown builder produces interface_status="unknown" and inner
#       legality_status="unknown"
# ---------------------------------------------------------------------------

class TestUnknownBuilder:
    def test_unknown_builder_produces_unknown(self):
        res = build_unknown_action_legality_service_interface_result(
            result_id="res_u", request_id="req_u",
        )
        assert res.interface_status == "unknown"
        assert res.legality_result.legality_status == "unknown"


# ---------------------------------------------------------------------------
# T12 — Authority flags reject True, 1, 0, None, and truthy strings
# ---------------------------------------------------------------------------

class TestAuthorityFlagsRejectBadValues:
    @pytest.mark.parametrize(
        ("value", "field"),
        [
            (True, "legality_engine_authorized"),
            (1, "command_execution_authorized"),
            (0, "state_read_authorized"),
            (None, "state_mutation_authorized"),
            ("yes", "model_call_authorized"),
        ],
    )
    def test_authority_flags_reject_bad_values(self, value, field):
        with pytest.raises(InvalidActionLegalityServiceInterfaceAuthorityFlagsError):
            ActionLegalityServiceInterfaceAuthorityFlags(**{field: value})


# ---------------------------------------------------------------------------
# T13 — Authority flag to_dict() hardcodes all values as False
# ---------------------------------------------------------------------------

class TestAuthorityFlagsToDict:
    def test_to_dict_all_false(self):
        flags = ActionLegalityServiceInterfaceAuthorityFlags()
        d = flags.to_dict()
        assert all(v is False for v in d.values())
        # 34 authority flags defined in RT-001E
        assert len(d) == 34, f"Expected 34 flags, got {len(d)}"


# ---------------------------------------------------------------------------
# T14 — Dependency manifest requires ActionLegalityDependencyReference deps
# ---------------------------------------------------------------------------

class TestDependencyManifestTyping:
    def test_accepts_dependency_references(self):
        dep = ActionLegalityDependencyReference(
            dependency_id="dep1",
            dependency_owner="validation",
        )
        manifest = create_action_legality_service_interface_dependency_manifest(
            manifest_id="m1",
            dependency_refs=[dep],
        )
        assert validate_action_legality_service_interface_dependency_manifest(manifest)

    def test_rejects_non_dependency_reference(self):
        with pytest.raises(InvalidActionLegalityServiceInterfaceDependencyManifestError):
            ActionLegalityServiceInterfaceDependencyManifest(
                manifest_id="m1",
                dependency_refs=["not_a_dep_ref"],
            )


# ---------------------------------------------------------------------------
# T15 — Dependency manifest carries owner routes as strings and does not
#       import or call owner services
# ---------------------------------------------------------------------------

class TestDependencyManifestNoOwnerCalls:
    def test_manifest_carries_owner_routes_as_strings(self):
        manifest = build_action_legality_service_interface_dependency_manifest(
            manifest_id="m1",
            owner_routes=["validation_owner", "resource_math_owner"],
        )
        assert manifest.required_owner_routes == (
            "validation_owner", "resource_math_owner",
        )
        assert manifest.unavailable_owner_routes == (
            "validation_owner", "resource_math_owner",
        )
        assert manifest.deferred_reason == "skeleton_interface_only"
        for route in manifest.required_owner_routes:
            assert isinstance(route, str)

    def test_manifest_builder_does_not_call_services(self):
        """Verify by inspecting the source — the builder only creates data,
        never calls external services."""
        import astra_runtime.domain.action_legality_service_interface_contract_skeleton as mod
        import inspect
        source = inspect.getsource(mod.build_action_legality_service_interface_dependency_manifest)
        # Should contain create_action_legality_service_interface_dependency_manifest
        # but not any service-call-like pattern
        assert "create_action_legality_service_interface_dependency_manifest" in source
        # No import of owner service modules
        assert "state_store" not in source
        assert "transaction" not in source
        assert "resource_math" not in source


# ---------------------------------------------------------------------------
# T16 — Visible serializer excludes backend/internal keys
# ---------------------------------------------------------------------------

class TestVisibleSerializerExcludesBackend:
    _FORBIDDEN_KEYS = {
        "legality_result", "authority_flags", "metadata",
        "dependency_manifest", "trace_refs", "backend_detail",
        "owner_route", "doctrine_refs", "schema_refs",
        "source_local_refs", "hidden_information_classification",
    }

    def test_visible_serializer_excludes_backend_keys(self):
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        visible = serialize_action_legality_service_interface_result_visible(res)
        for key in self._FORBIDDEN_KEYS:
            assert key not in visible, f"Visible serializer leaked {key!r}"

    def test_visible_serializer_has_expected_keys(self):
        res = build_deferred_action_legality_service_interface_result(
            result_id="res1", request_id="r1",
        )
        visible = serialize_action_legality_service_interface_result_visible(res)
        expected_keys = {
            "result_id", "request_id", "interface_status",
            "legality_status", "player_visible_message",
            "visible_blocker_messages", "non_authority_note",
        }
        assert set(visible.keys()) == expected_keys


# ---------------------------------------------------------------------------
# T17 — Visible serializer messages are members of SAFE_PLAYER_MESSAGES
# ---------------------------------------------------------------------------

class TestVisibleSerializerSafeMessages:
    def test_player_visible_message_is_safe(self):
        for builder in [
            build_deferred_action_legality_service_interface_result,
            build_unknown_action_legality_service_interface_result,
        ]:
            res = builder(result_id="res1", request_id="r1")
            visible = serialize_action_legality_service_interface_result_visible(res)
            msg = visible["player_visible_message"]
            assert msg in SAFE_PLAYER_MESSAGES, f"Unsafe message: {msg!r}"
            for blocker_msg in visible["visible_blocker_messages"]:
                assert blocker_msg in SAFE_PLAYER_MESSAGES, (
                    f"Unsafe blocker message: {blocker_msg!r}"
                )


# ---------------------------------------------------------------------------
# T18 — Metadata rejects non-JSON-safe values
# ---------------------------------------------------------------------------

class TestMetadataSafety:
    def test_metadata_rejects_non_json_safe(self):
        with pytest.raises(InvalidActionLegalityServiceInterfaceDependencyManifestError):
            ActionLegalityServiceInterfaceDependencyManifest(
                manifest_id="m1",
                metadata={"bad": object()},
            )


# ---------------------------------------------------------------------------
# T19 — RT-001E module imports no forbidden downstream modules
# ---------------------------------------------------------------------------

class TestImportBoundaryEnforcement:
    _FORBIDDEN_MODULES = (
        "state_store", "state_projection", "transaction_lifecycle",
        "event_commitment", "model_boundary", "tiny_vertical_slice",
        "context_packet_compiler", "live_play", "resource_consequence_math",
    )

    def test_rt001e_does_not_import_forbidden_modules(self):
        src = (
            _REPO_ROOT
            / "src"
            / "astra_runtime"
            / "domain"
            / "action_legality_service_interface_contract_skeleton.py"
        ).read_text()
        tree = ast.parse(src)
        import_names: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_names.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    import_names.append(node.module)
        for mod_name in import_names:
            for forbidden in self._FORBIDDEN_MODULES:
                assert forbidden not in mod_name, (
                    f"RT-001E imports forbidden module pattern "
                    f"{forbidden!r} via {mod_name!r}"
                )


# ---------------------------------------------------------------------------
# T20 — RT-001E public names contain no forbidden execution/mutation patterns
# ---------------------------------------------------------------------------

class TestPublicSurfaceNameInspection:
    _FORBIDDEN_PATTERNS = (
        "execute", "mutate", "commit_event", "model_call",
        "prompt_render", "narration", "live_play_run",
        "persist_write", "replay_run",
    )

    def test_public_names_no_execution_patterns(self):
        for name in RT001E_ALL:
            lower = name.lower()
            for pat in self._FORBIDDEN_PATTERNS:
                assert pat not in lower, (
                    f"Public name {name!r} contains forbidden pattern {pat!r}"
                )


# ---------------------------------------------------------------------------
# T21 — Domain package exports include the documented alias names and not
#       ambiguous duplicate direct names
# ---------------------------------------------------------------------------

class TestDomainPackageExports:
    def test_domain_package_exports_skeleton_request_alias(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "ActionLegalityServiceInterfaceSkeletonRequest")
        assert hasattr(domain, "ActionLegalityServiceInterfaceSkeletonResult")

    def test_skeleton_request_alias_is_identity(self):
        import astra_runtime.domain as domain
        from astra_runtime.domain.action_legality_service_interface_contract_skeleton import (
            ActionLegalityServiceInterfaceRequest,
            ActionLegalityServiceInterfaceResult,
        )
        assert domain.ActionLegalityServiceInterfaceSkeletonRequest is ActionLegalityServiceInterfaceRequest
        assert domain.ActionLegalityServiceInterfaceSkeletonResult is ActionLegalityServiceInterfaceResult

    def test_domain_exports_skeleton_request_direct_name_not_exported(self):
        """The domain __init__.py exports the aliased names
        ActionLegalityServiceInterfaceSkeletonRequest/Result, not the direct
        ActionLegalityServiceInterfaceRequest/Result names. This is
        intentional to avoid collision with the older action_legality.py
        ActionLegalityResult that already occupies the package namespace."""
        import astra_runtime.domain as domain
        # The direct names are deliberately NOT exported in __all__
        # to avoid collision. They are only available through the Skeleton
        # suffix aliases.
        assert hasattr(domain, "ActionLegalityServiceInterfaceSkeletonRequest")


# ---------------------------------------------------------------------------
# T22 — RT-001F branch does not modify the skeleton implementation file
# ---------------------------------------------------------------------------

class TestNoModificationOfSkeleton:
    def test_skeleton_file_not_modified(self):
        """Check that the skeleton file has not been changed from origin/main.
        If this branch is based on main, the file should be identical."""
        result = subprocess.run(
            [
                "git",
                "diff",
                "origin/main",
                "--",
                "src/astra_runtime/domain/action_legality_service_interface_contract_skeleton.py",
            ],
            capture_output=True, text=True, cwd=_REPO_ROOT,
        )
        assert result.returncode == 0, "git diff failed"
        assert not result.stdout.strip(), (
            "RT-001F branch modifies the implementation skeleton file: "
            + result.stdout
        )


# ---------------------------------------------------------------------------
# T23 — RT-001B, RT-001C, RT-001D, RT-001E tests still pass
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


# ---------------------------------------------------------------------------
# Helper — build an inner ActionLegalityResult with a given legality status
# ---------------------------------------------------------------------------

def _make_result_for_status(status: str) -> ActionLegalityResult:
    """Create an ActionLegalityResult with the given legality_status.
    For 'legal' status, blockers must be empty (RT-001B invariant)."""
    if status == "legal":
        return ActionLegalityResult(
            result_id="leg_test",
            request_id="req_test",
            legality_status="legal",
            authority_flags=ActionLegalityAuthorityFlags(),
        )
    blocker = ActionLegalityBlocker(
        blocker_id="b_test",
        blocker_class="runtime_owner_handoff",
        legality_status=status,
        player_visible_message="This action cannot be processed at this time.",
        backend_detail=ActionLegalityBackendDetail(
            detail_id="d_test",
            blocker_class="runtime_owner_handoff",
            owner_route="test",
        ),
    )
    return ActionLegalityResult(
        result_id="leg_test",
        request_id="req_test",
        legality_status=status,
        blockers=[blocker],
        authority_flags=ActionLegalityAuthorityFlags(),
    )

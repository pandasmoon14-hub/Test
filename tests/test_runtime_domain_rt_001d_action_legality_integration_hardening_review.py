"""
Tests for RT-001D: action legality integration hardening review.

This is a hardening review test file that inspects the merged RT-001B and
RT-001C surfaces without implementing new behavior.

Modules under review:
    astra_runtime.domain.action_legality_skeleton (RT-001B)
    astra_runtime.domain.action_legality_gate_integration_skeleton (RT-001C)
"""

import inspect
import pathlib
import subprocess

import pytest

from astra_runtime.domain.action_legality_skeleton import (
    ActionLegalityAuthorityFlags,
    ActionLegalityBlocker,
    ActionLegalityReference,
    ActionLegalityResult,
    ActionLegalitySubjectReference,
    InvalidActionLegalityAuthorityFlagsError,
    InvalidActionLegalityBlockerError,
    SAFE_PLAYER_MESSAGES,
    _HIDDEN_INFO_SAFE_MESSAGES,
    _validate_json_safe,
    make_action_legality_reference,
    make_action_legality_result,
    make_action_legality_subject_reference,
)

from astra_runtime.domain.action_legality_gate_integration_skeleton import (
    ACTION_LEGALITY_GATE_DEFAULT_STATUSES,
    ActionLegalityGateIntegrationAuthorityFlags,
    ActionLegalityGateIntegrationResult,
    ActionLegalityGateIntegrationSkeletonError,
    InvalidActionLegalityGateIntegrationAuthorityFlagsError,
    InvalidActionLegalityGateIntegrationResultError,
    build_action_legality_gate_integration_result,
    create_action_legality_gate_dependency_plan,
    create_action_legality_gate_input_refs,
    create_action_legality_gate_integration_request,
    create_action_legality_gate_integration_result,
    serialize_action_legality_gate_integration_result_visible,
    validate_action_legality_gate_integration_result,
)
from astra_runtime.domain.action_legality_gate_integration_skeleton import (
    __all__ as RT001C_ALL,
)

import astra_runtime.domain.action_legality_gate_integration_skeleton as _rt001c_module


# ---------------------------------------------------------------------------
# Repo root
# ---------------------------------------------------------------------------

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Test fixture helpers
# ---------------------------------------------------------------------------


def _make_ref(kind="command", ref_id="ref-1", owner="test"):
    return make_action_legality_reference(
        reference_kind=kind,
        reference_id=ref_id,
        owner_surface=owner,
    )


def _make_subject():
    return make_action_legality_subject_reference(
        subject_id="actor-1",
        subject_label="Test Actor",
    )


def _make_input_refs():
    return create_action_legality_gate_input_refs(
        scene_command_assembly_ref=_make_ref("command", "asm-1", "pr9a"),
        command_kind_routing_ref=_make_ref("command", "route-1", "pr9c"),
        validation_bridge_ref=_make_ref("validation", "val-1", "pr9d"),
    )


def _make_dep_plan():
    return create_action_legality_gate_dependency_plan(plan_id="plan-1")


def _make_request():
    return create_action_legality_gate_integration_request(
        request_id="req-1",
        input_refs=_make_input_refs(),
        subject_ref=_make_subject(),
        command_ref=_make_ref("command", "cmd-1", "test"),
        dependency_plan=_make_dep_plan(),
    )


def _build_default_gate_result():
    """Build a gate integration result with default (deferred) status."""
    return build_action_legality_gate_integration_result(
        result_id="gir-1",
        request=_make_request(),
    )


# ---------------------------------------------------------------------------
# 1. Review document existence
# ---------------------------------------------------------------------------


class TestReviewDocumentPresence:
    """Tests 1-4: review document exists and contains required content."""

    _review_path = (
        _REPO_ROOT
        / "docs"
        / "doctrine"
        / "reviews"
        / "runtime_domain_rt_001d_action_legality_integration_hardening_review.md"
    )

    def test_review_document_exists(self):
        """T1: The review document must exist on disk."""
        assert self._review_path.is_file(), (
            f"Review document not found at {self._review_path}"
        )

    def test_review_document_names_source_prs(self):
        """T2: The review document must reference RT-001A, RT-001B, RT-001C."""
        text = self._review_path.read_text(encoding="utf-8")
        for tag in ("RT-001A", "RT-001B", "RT-001C"):
            assert tag in text, f"Review document must mention {tag}"

    def test_review_document_states_review_only(self):
        """T3: The review document must state RT-001D is review-only."""
        text = self._review_path.read_text(encoding="utf-8")
        assert "review-only" in text.lower(), (
            "Review document must state that RT-001D is review-only"
        )
        assert "does not authorize implementation" in text.lower(), (
            "Review document must state that RT-001D does not authorize "
            "implementation"
        )

    def test_review_document_contains_risk_ledger_categories(self):
        """T4: The review document must contain every required risk category."""
        text = self._review_path.read_text(encoding="utf-8")
        required_categories = [
            "Legal approval bypass",
            "Backend detail leakage",
            "Hidden-information specificity",
            "Dependency reference accidentally becoming a service call",
            "Guardrail allowlist drift",
            "Metadata serialization",
            "Authority flag bypass",
            "Constructor/factory divergence",
            "Validator being weaker than constructor",
            "PR-9A/9C/9D/9E reference seam overreach",
            "action legality engine accidentally reading state",
            "Donor-specific legality assumptions",
            "Live-play/model adapter treating skeleton statuses",
        ]
        for category in required_categories:
            assert category in text, (
                f"Review document must contain risk category: {category!r}"
            )


# ---------------------------------------------------------------------------
# 2. RT-001C builder and constructor guards
# ---------------------------------------------------------------------------


class TestRT001CBuilderGuards:
    """Tests 5-9: builder, constructor, factory, and validator status guards."""

    def test_rt001c_builder_default_is_deferred(self):
        """T5: build_action_legality_gate_integration_result default is deferred."""
        result = _build_default_gate_result()
        assert result.legality_result.legality_status == "deferred"

    def test_rt001c_builder_rejects_legal_status_override(self):
        """T6: Builder rejects status_override='legal'."""
        with pytest.raises(ActionLegalityGateIntegrationSkeletonError):
            build_action_legality_gate_integration_result(
                result_id="gir-bad",
                request=_make_request(),
                status_override="legal",
            )

    def test_rt001c_direct_constructor_rejects_legal_result(self):
        """T7: ActionLegalityGateIntegrationResult constructor rejects a
        legality_result whose legality_status is 'legal'."""
        legal_result = make_action_legality_result(
            result_id="lr-legal",
            request_id="req-1",
            legality_status="legal",
        )
        request_obj = _make_request()
        from astra_runtime.domain.action_legality_gate_integration_skeleton import (
            build_action_legality_request_from_gate_integration,
        )
        legality_request = build_action_legality_request_from_gate_integration(
            request=request_obj,
        )
        with pytest.raises(InvalidActionLegalityGateIntegrationResultError):
            ActionLegalityGateIntegrationResult(
                result_id="gir-bad",
                request_id="req-1",
                legality_request=legality_request,
                legality_result=legal_result,
                input_refs=_make_input_refs(),
                dependency_plan=_make_dep_plan(),
            )

    def test_rt001c_factory_rejects_legal_result(self):
        """T8: create_action_legality_gate_integration_result rejects a
        legality_result whose legality_status is 'legal'."""
        legal_result = make_action_legality_result(
            result_id="lr-legal",
            request_id="req-1",
            legality_status="legal",
        )
        request_obj = _make_request()
        from astra_runtime.domain.action_legality_gate_integration_skeleton import (
            build_action_legality_request_from_gate_integration,
        )
        legality_request = build_action_legality_request_from_gate_integration(
            request=request_obj,
        )
        with pytest.raises(InvalidActionLegalityGateIntegrationResultError):
            create_action_legality_gate_integration_result(
                result_id="gir-bad",
                request_id="req-1",
                legality_request=legality_request,
                legality_result=legal_result,
                input_refs=_make_input_refs(),
                dependency_plan=_make_dep_plan(),
            )

    def test_rt001c_validator_rejects_non_default_statuses(self):
        """T9: The validator returns True for a valid deferred result and
        constructing with 'legal' status is impossible (constructor rejects
        it before the validator can see it)."""
        # Valid deferred result passes validation.
        valid_result = _build_default_gate_result()
        assert validate_action_legality_gate_integration_result(valid_result) is True

        # Constructing with 'legal' status is impossible -- the constructor
        # raises before the validator could ever see such an object.
        legal_result = make_action_legality_result(
            result_id="lr-legal",
            request_id="req-1",
            legality_status="legal",
        )
        with pytest.raises(InvalidActionLegalityGateIntegrationResultError):
            ActionLegalityGateIntegrationResult(
                result_id="gir-bad",
                request_id="req-1",
                legality_request=_build_default_gate_result().legality_request,
                legality_result=legal_result,
                input_refs=_make_input_refs(),
                dependency_plan=_make_dep_plan(),
            )


# ---------------------------------------------------------------------------
# 3. Authority flag hardening
# ---------------------------------------------------------------------------


class TestAuthorityFlagHardening:
    """Tests 10-12: authority flag false-only enforcement."""

    def test_rt001c_authority_flags_reject_truthy_values(self):
        """T10: ActionLegalityGateIntegrationAuthorityFlags rejects
        True, 1, 0, None, and 'yes'."""
        bad_values = [True, 1, 0, None, "yes"]
        for bad_value in bad_values:
            with pytest.raises(
                InvalidActionLegalityGateIntegrationAuthorityFlagsError,
                match="must be False",
            ):
                ActionLegalityGateIntegrationAuthorityFlags(
                    action_legality_engine_authorized=bad_value,
                )

    def test_rt001c_authority_flag_to_dict_hardcodes_false(self):
        """T11: to_dict() on default flags returns all-False dict."""
        flags = ActionLegalityGateIntegrationAuthorityFlags()
        d = flags.to_dict()
        assert isinstance(d, dict)
        assert len(d) > 0
        for key, value in d.items():
            assert value is False, (
                f"to_dict()[{key!r}] must be False, got {value!r}"
            )

    def test_rt001b_authority_flags_reject_non_false(self):
        """T12: ActionLegalityAuthorityFlags rejects True."""
        with pytest.raises(
            InvalidActionLegalityAuthorityFlagsError,
            match="must be False",
        ):
            ActionLegalityAuthorityFlags(
                action_legality_engine_authorized=True,
            )


# ---------------------------------------------------------------------------
# 4. Metadata JSON safety
# ---------------------------------------------------------------------------


class TestMetadataJsonSafety:
    """Tests 13-14: _validate_json_safe rejects non-JSON-safe types."""

    def test_rt001b_metadata_json_safety(self):
        """T13: ActionLegalityReference rejects metadata containing a set,
        and _validate_json_safe rejects sets directly."""
        from astra_runtime.domain.action_legality_skeleton import (
            InvalidActionLegalityReferenceError,
        )
        # Direct _validate_json_safe test.
        with pytest.raises(Exception, match="not JSON-safe"):
            _validate_json_safe(
                {"bad": {1, 2, 3}},
                "metadata",
                ValueError,
            )

        # Constructor-level test.
        with pytest.raises(InvalidActionLegalityReferenceError):
            ActionLegalityReference(
                reference_kind="command",
                reference_id="ref-set",
                owner_surface="test",
                metadata={"bad": {1, 2, 3}},
            )

    def test_rt001c_metadata_json_safety_helper_exists(self):
        """T14: _validate_json_safe exists in the RT-001C module."""
        assert hasattr(_rt001c_module, "_validate_json_safe"), (
            "_validate_json_safe must exist in "
            "action_legality_gate_integration_skeleton"
        )
        assert callable(_rt001c_module._validate_json_safe)


# ---------------------------------------------------------------------------
# 5. Player-visible serializer safety
# ---------------------------------------------------------------------------


class TestPlayerVisibleSerializerSafety:
    """Tests 15-16: visible serializer excludes backend detail and uses
    only safe messages."""

    def test_player_visible_serializer_excludes_backend_detail(self):
        """T15: Visible serializer output must NOT contain backend-only keys."""
        result = _build_default_gate_result()
        visible = serialize_action_legality_gate_integration_result_visible(result)

        forbidden_keys = {
            "backend_detail",
            "backend_only_detail",
            "backend_only_refs",
            "dependency_plan",
            "input_refs",
            "trace_refs",
            "affected_refs",
            "doctrine_refs",
            "schema_refs",
            "source_local_refs",
        }
        present = forbidden_keys & set(visible.keys())
        assert not present, (
            f"Player-visible serialization must not contain: {present}"
        )

    def test_player_visible_messages_from_safe_set(self):
        """T16: All player-visible messages must be in SAFE_PLAYER_MESSAGES."""
        result = _build_default_gate_result()
        visible = serialize_action_legality_gate_integration_result_visible(result)

        msg = visible.get("player_visible_message")
        if msg is not None:
            assert msg in SAFE_PLAYER_MESSAGES, (
                f"player_visible_message {msg!r} not in SAFE_PLAYER_MESSAGES"
            )

        for blocker_msg in visible.get("visible_blocker_messages", []):
            assert blocker_msg in SAFE_PLAYER_MESSAGES, (
                f"visible_blocker_message {blocker_msg!r} not in "
                f"SAFE_PLAYER_MESSAGES"
            )


# ---------------------------------------------------------------------------
# 6. Hidden-information blocker message restriction
# ---------------------------------------------------------------------------


class TestHiddenInformationBlockerMessages:
    """Test 17: hidden_information blockers use generic messages only."""

    def test_hidden_information_blocker_uses_generic_messages(self):
        """T17: A hidden_information blocker must use only messages from
        _HIDDEN_INFO_SAFE_MESSAGES. A non-safe message must raise."""
        # Accepted message.
        for safe_msg in _HIDDEN_INFO_SAFE_MESSAGES:
            blocker = ActionLegalityBlocker(
                blocker_id="blk-hidden-ok",
                blocker_class="hidden_information",
                legality_status="blocked",
                player_visible_message=safe_msg,
            )
            assert blocker.player_visible_message == safe_msg

        # Rejected message: this message is in SAFE_PLAYER_MESSAGES but NOT
        # in _HIDDEN_INFO_SAFE_MESSAGES.
        non_hidden_safe_msg = "Action accepted."
        assert non_hidden_safe_msg in SAFE_PLAYER_MESSAGES
        assert non_hidden_safe_msg not in _HIDDEN_INFO_SAFE_MESSAGES
        with pytest.raises(
            InvalidActionLegalityBlockerError,
            match="hidden_information blocker must use a safe generic message",
        ):
            ActionLegalityBlocker(
                blocker_id="blk-hidden-bad",
                blocker_class="hidden_information",
                legality_status="blocked",
                player_visible_message=non_hidden_safe_msg,
            )


# ---------------------------------------------------------------------------
# 7. Public surface name inspection
# ---------------------------------------------------------------------------


class TestPublicSurfaceNameInspection:
    """Test 18: RT-001C __all__ contains no execution-pattern names."""

    _FORBIDDEN_PATTERNS = (
        "execute",
        "mutate",
        "commit_event",
        "model_call",
        "prompt_render",
        "narration",
        "live_play_run",
        "persist_write",
        "replay_run",
    )

    def test_public_rt001c_names_no_execution_patterns(self):
        """T18: No name in RT-001C __all__ matches forbidden patterns."""
        for name in RT001C_ALL:
            name_lower = name.lower()
            for pattern in self._FORBIDDEN_PATTERNS:
                assert pattern not in name_lower, (
                    f"RT-001C __all__ name {name!r} contains forbidden "
                    f"pattern {pattern!r}"
                )


# ---------------------------------------------------------------------------
# 8. Import boundary enforcement
# ---------------------------------------------------------------------------


class TestImportBoundaryEnforcement:
    """Test 19: RT-001C source does not import from forbidden modules."""

    _FORBIDDEN_MODULES = (
        "state_store",
        "transaction_lifecycle",
        "event_commitment",
        "model_boundary",
        "tiny_vertical_slice",
        "context_packet_compiler",
        "live_play",
    )

    def test_rt001c_does_not_import_forbidden_modules(self):
        """T19: RT-001C module source must not import from forbidden modules."""
        source = inspect.getsource(_rt001c_module)
        # Extract only import lines from the source.
        import_lines = [
            line.strip()
            for line in source.splitlines()
            if line.strip().startswith(("import ", "from "))
        ]
        import_block = "\n".join(import_lines)
        for mod in self._FORBIDDEN_MODULES:
            assert mod not in import_block, (
                f"RT-001C import statements must not reference module {mod!r}"
            )


# ---------------------------------------------------------------------------
# 9. Implementation module safety
# ---------------------------------------------------------------------------


class TestImplementationModuleSafety:
    """Test 20: RT-001D branch does not modify implementation modules."""

    def test_rt001d_does_not_modify_implementation_modules(self):
        """T20: git diff against origin/main must not show changes in
        src/astra_runtime/domain/."""
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True,
            text=True,
            cwd=str(_REPO_ROOT),
        )
        # If the git command fails (e.g., no origin/main), skip rather
        # than fail the test -- this can happen in CI without a full clone.
        if result.returncode != 0:
            pytest.skip(
                f"git diff failed (rc={result.returncode}): "
                f"{result.stderr.strip()}"
            )
        changed_files = [
            f.strip() for f in result.stdout.strip().splitlines() if f.strip()
        ]
        domain_changes = [
            f for f in changed_files
            if f.startswith("src/astra_runtime/domain/")
        ]
        assert not domain_changes, (
            f"RT-001D must not modify implementation modules, but found "
            f"changes in: {domain_changes}"
        )

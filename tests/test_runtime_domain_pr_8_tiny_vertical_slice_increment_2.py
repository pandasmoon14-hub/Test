"""PR-8 Increment 2 — tiny vertical slice command lifecycle skeleton tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    TinyVerticalSliceCommandIntent,
    TinyVerticalSliceCommandValidationResult,
    TinyVerticalSliceCommandPreviewResult,
    TinyVerticalSliceCommandLifecycleResult,
    TinyVerticalSliceError,
    create_tiny_vertical_slice_command_intent,
    create_tiny_vertical_slice_world_state,
    validate_tiny_vertical_slice_command_intent,
    preview_tiny_vertical_slice_command_intent,
    run_tiny_vertical_slice_command_lifecycle,
    serialize_tiny_vertical_slice_command_lifecycle_visible_result,
)


@pytest.fixture()
def world():
    return create_tiny_vertical_slice_world_state()


@pytest.fixture()
def default_command():
    return create_tiny_vertical_slice_command_intent()


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment2_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSliceCommandIntent",
            "TinyVerticalSliceCommandValidationResult",
            "TinyVerticalSliceCommandPreviewResult",
            "TinyVerticalSliceCommandLifecycleResult",
            "create_tiny_vertical_slice_command_intent",
            "validate_tiny_vertical_slice_command_intent",
            "preview_tiny_vertical_slice_command_intent",
            "run_tiny_vertical_slice_command_lifecycle",
            "serialize_tiny_vertical_slice_command_lifecycle_visible_result",
        ]
        for name in expected:
            assert hasattr(domain, name), f"Missing export: {name}"


# ---------------------------------------------------------------------------
# Frozen dataclasses
# ---------------------------------------------------------------------------

class TestFrozenDataclasses:
    @pytest.mark.parametrize("cls", [
        TinyVerticalSliceCommandIntent,
        TinyVerticalSliceCommandValidationResult,
        TinyVerticalSliceCommandPreviewResult,
        TinyVerticalSliceCommandLifecycleResult,
    ])
    def test_dataclass_is_frozen(self, cls):
        assert cls.__dataclass_params__.frozen is True


# ---------------------------------------------------------------------------
# Command intent
# ---------------------------------------------------------------------------

class TestCommandIntent:
    def test_factory_returns_command_intent(self):
        cmd = create_tiny_vertical_slice_command_intent()
        assert isinstance(cmd, TinyVerticalSliceCommandIntent)

    def test_rejects_empty_command_ref(self):
        with pytest.raises(TinyVerticalSliceError, match="command_ref"):
            create_tiny_vertical_slice_command_intent(command_ref="")

    def test_rejects_empty_actor_ref(self):
        with pytest.raises(TinyVerticalSliceError, match="actor_ref"):
            create_tiny_vertical_slice_command_intent(actor_ref="")

    def test_rejects_empty_target_ref(self):
        with pytest.raises(TinyVerticalSliceError, match="target_ref"):
            create_tiny_vertical_slice_command_intent(target_ref="")

    def test_rejects_empty_declared_intent(self):
        with pytest.raises(TinyVerticalSliceError, match="declared_intent"):
            create_tiny_vertical_slice_command_intent(declared_intent="")

    def test_rejects_non_bool_requests_commit(self):
        with pytest.raises(TinyVerticalSliceError, match="requests_commit"):
            create_tiny_vertical_slice_command_intent(requests_commit=1)

    def test_metadata_deep_copied_and_frozen(self):
        source = {"nested": {"k": "v"}}
        cmd = create_tiny_vertical_slice_command_intent(metadata=source)
        source["nested"]["k"] = "changed"
        assert cmd.metadata["nested"]["k"] == "v"
        assert isinstance(cmd.metadata, MappingProxyType)

    @pytest.mark.parametrize("kind", ["inspect_lever", "brace_mechanism", "pull_lever", "speak_to_npc"])
    def test_accepts_valid_command_kinds(self, kind):
        cmd = create_tiny_vertical_slice_command_intent(command_kind=kind, target_ref="some-target")
        assert cmd.command_kind == kind

    def test_rejects_unknown_command_kind(self):
        with pytest.raises(TinyVerticalSliceError, match="command_kind"):
            create_tiny_vertical_slice_command_intent(command_kind="fly_away")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class TestValidation:
    def test_valid_default_inspect(self, world, default_command):
        result = validate_tiny_vertical_slice_command_intent(state=world, command=default_command)
        assert result.is_valid is True
        assert result.validation_status == "valid"
        assert "command_valid" in result.reason_codes

    def test_wrong_actor_ref_invalid(self, world):
        cmd = create_tiny_vertical_slice_command_intent(actor_ref="actor-unknown")
        result = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        assert result.is_valid is False
        assert "actor_not_in_world" in result.reason_codes

    def test_wrong_target_for_lever_command(self, world):
        cmd = create_tiny_vertical_slice_command_intent(
            command_kind="inspect_lever",
            target_ref="npc-watchful-adept",
        )
        result = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        assert result.is_valid is False
        assert "target_not_valid_for_command" in result.reason_codes

    def test_speak_to_npc_requires_npc_target(self, world):
        cmd = create_tiny_vertical_slice_command_intent(
            command_kind="speak_to_npc",
            target_ref="npc-watchful-adept",
        )
        result = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        assert result.is_valid is True

    def test_speak_to_npc_rejects_lever_target(self, world):
        cmd = create_tiny_vertical_slice_command_intent(
            command_kind="speak_to_npc",
            target_ref="lever-brass-threshold",
        )
        result = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        assert result.is_valid is False
        assert "target_not_valid_for_command" in result.reason_codes

    @pytest.mark.parametrize("kind", ["inspect_lever", "brace_mechanism", "pull_lever"])
    def test_lever_commands_require_lever_target(self, world, kind):
        cmd = create_tiny_vertical_slice_command_intent(
            command_kind=kind,
            target_ref="lever-brass-threshold",
        )
        result = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        assert result.is_valid is True

    def test_validation_status_bool_consistency_valid(self):
        with pytest.raises(TinyVerticalSliceError):
            TinyVerticalSliceCommandValidationResult(
                command_ref="c",
                is_valid=True,
                validation_status="invalid",
                reason_codes=("x",),
                visible_explanation="bad",
            )

    def test_validation_status_bool_consistency_invalid(self):
        with pytest.raises(TinyVerticalSliceError):
            TinyVerticalSliceCommandValidationResult(
                command_ref="c",
                is_valid=False,
                validation_status="valid",
                reason_codes=("x",),
                visible_explanation="bad",
            )


# ---------------------------------------------------------------------------
# Preview
# ---------------------------------------------------------------------------

class TestPreview:
    def test_invalid_validation_creates_preview_blocked(self, world):
        cmd = create_tiny_vertical_slice_command_intent(actor_ref="actor-unknown")
        val = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        preview = preview_tiny_vertical_slice_command_intent(state=world, command=cmd, validation=val)
        assert preview.preview_status == "preview_blocked"

    def test_inspect_lever_available_no_resolution(self, world):
        cmd = create_tiny_vertical_slice_command_intent(command_kind="inspect_lever")
        val = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        preview = preview_tiny_vertical_slice_command_intent(state=world, command=cmd, validation=val)
        assert preview.preview_status == "preview_available"
        assert preview.would_require_resolution is False

    def test_brace_mechanism_available_no_resolution(self, world):
        cmd = create_tiny_vertical_slice_command_intent(
            command_kind="brace_mechanism",
            command_ref="cmd-brace-1",
        )
        val = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        preview = preview_tiny_vertical_slice_command_intent(state=world, command=cmd, validation=val)
        assert preview.preview_status == "preview_available"
        assert preview.would_require_resolution is False

    def test_pull_lever_available_requires_resolution(self, world):
        cmd = create_tiny_vertical_slice_command_intent(
            command_kind="pull_lever",
            command_ref="cmd-pull-1",
        )
        val = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        preview = preview_tiny_vertical_slice_command_intent(state=world, command=cmd, validation=val)
        assert preview.preview_status == "preview_available"
        assert preview.would_require_resolution is True

    def test_pull_lever_risk_refs_include_hazard_clock(self, world):
        cmd = create_tiny_vertical_slice_command_intent(
            command_kind="pull_lever",
            command_ref="cmd-pull-1",
        )
        val = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        preview = preview_tiny_vertical_slice_command_intent(state=world, command=cmd, validation=val)
        assert world.hazard_clock.clock_ref in preview.visible_risk_refs

    def test_speak_to_npc_targets_npc(self, world):
        cmd = create_tiny_vertical_slice_command_intent(
            command_kind="speak_to_npc",
            target_ref="npc-watchful-adept",
            command_ref="cmd-speak-1",
        )
        val = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        preview = preview_tiny_vertical_slice_command_intent(state=world, command=cmd, validation=val)
        assert preview.preview_status == "preview_available"
        assert world.npc.npc_ref in preview.visible_target_refs

    def test_lever_commands_have_backend_hidden_fact_refs(self, world):
        cmd = create_tiny_vertical_slice_command_intent(command_kind="inspect_lever")
        val = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        preview = preview_tiny_vertical_slice_command_intent(state=world, command=cmd, validation=val)
        assert world.hidden_fact.hidden_fact_ref in preview.hidden_fact_refs_used_by_backend

    def test_visible_preview_excludes_hidden_fact_description(self, world):
        cmd = create_tiny_vertical_slice_command_intent(command_kind="inspect_lever")
        val = validate_tiny_vertical_slice_command_intent(state=world, command=cmd)
        preview = preview_tiny_vertical_slice_command_intent(state=world, command=cmd, validation=val)
        assert world.hidden_fact.backend_only_description not in preview.visible_preview


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

class TestLifecycle:
    def test_default_lifecycle_validated_preview(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        assert result.lifecycle_status == "validated_preview"

    def test_default_commit_status_not_requested(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        assert result.commit_status == "not_requested"

    def test_commit_requesting_valid_command_commit_ready(self, world):
        cmd = create_tiny_vertical_slice_command_intent(requests_commit=True)
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=cmd)
        assert result.commit_status == "commit_ready"

    def test_invalid_command_lifecycle_blocked(self, world):
        cmd = create_tiny_vertical_slice_command_intent(actor_ref="actor-unknown")
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=cmd)
        assert result.lifecycle_status == "blocked"

    def test_invalid_command_commit_status_blocked(self, world):
        cmd = create_tiny_vertical_slice_command_intent(actor_ref="actor-unknown")
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=cmd)
        assert result.commit_status == "blocked"

    def test_state_changed_always_false(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        assert result.state_changed is False

    def test_event_committed_always_false(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        assert result.event_committed is False

    def test_resulting_state_is_same_object(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        assert result.resulting_state is world

    def test_lifecycle_does_not_mutate_state(self, world, default_command):
        original_tick = world.hazard_clock.current_tick
        original_lever_state = world.lever.visible_state
        run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        assert world.hazard_clock.current_tick == original_tick
        assert world.lever.visible_state == original_lever_state


# ---------------------------------------------------------------------------
# Visible lifecycle serializer
# ---------------------------------------------------------------------------

class TestVisibleLifecycleSerializer:
    def test_rejects_non_lifecycle_input(self):
        with pytest.raises(TinyVerticalSliceError):
            serialize_tiny_vertical_slice_command_lifecycle_visible_result("not a result")

    def test_rejects_dict_input(self):
        with pytest.raises(TinyVerticalSliceError):
            serialize_tiny_vertical_slice_command_lifecycle_visible_result({})

    def test_exact_top_level_key_order(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        serialized = serialize_tiny_vertical_slice_command_lifecycle_visible_result(result)
        expected_keys = [
            "command_ref",
            "lifecycle_status",
            "commit_status",
            "state_changed",
            "event_committed",
            "command",
            "validation",
            "preview",
            "resulting_visible_state",
            "metadata",
        ]
        assert list(serialized.keys()) == expected_keys

    def test_command_sub_dict_keys(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        serialized = serialize_tiny_vertical_slice_command_lifecycle_visible_result(result)
        cmd = serialized["command"]
        for key in ["command_ref", "actor_ref", "command_kind", "target_ref", "declared_intent", "requests_commit", "metadata"]:
            assert key in cmd, f"Missing key in command: {key}"

    def test_validation_sub_dict_keys(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        serialized = serialize_tiny_vertical_slice_command_lifecycle_visible_result(result)
        val = serialized["validation"]
        for key in ["command_ref", "is_valid", "validation_status", "reason_codes", "visible_explanation", "metadata"]:
            assert key in val, f"Missing key in validation: {key}"

    def test_preview_sub_dict_visible_keys(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        serialized = serialize_tiny_vertical_slice_command_lifecycle_visible_result(result)
        preview = serialized["preview"]
        for key in ["command_ref", "preview_status", "would_require_resolution", "visible_preview", "visible_risk_refs", "visible_target_refs", "metadata"]:
            assert key in preview, f"Missing key in preview: {key}"

    def test_preview_sub_dict_omits_hidden_backend_refs(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        serialized = serialize_tiny_vertical_slice_command_lifecycle_visible_result(result)
        preview = serialized["preview"]
        assert "hidden_fact_refs_used_by_backend" not in preview

    def test_resulting_visible_state_omits_hidden_fact(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        serialized = serialize_tiny_vertical_slice_command_lifecycle_visible_result(result)
        rvs = serialized["resulting_visible_state"]
        assert "hidden_fact" not in rvs

    def test_serialized_output_excludes_hidden_fact_description(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        serialized = serialize_tiny_vertical_slice_command_lifecycle_visible_result(result)
        text = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in text

    def test_tuple_fields_serialize_as_lists(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        serialized = serialize_tiny_vertical_slice_command_lifecycle_visible_result(result)
        assert isinstance(serialized["validation"]["reason_codes"], list)
        assert isinstance(serialized["preview"]["visible_risk_refs"], list)
        assert isinstance(serialized["preview"]["visible_target_refs"], list)

    def test_mapping_fields_serialize_as_dicts(self, world, default_command):
        result = run_tiny_vertical_slice_command_lifecycle(state=world, command=default_command)
        serialized = serialize_tiny_vertical_slice_command_lifecycle_visible_result(result)
        assert isinstance(serialized["metadata"], dict)
        assert not isinstance(serialized["metadata"], MappingProxyType)
        assert isinstance(serialized["command"]["metadata"], dict)
        assert not isinstance(serialized["command"]["metadata"], MappingProxyType)


# ---------------------------------------------------------------------------
# Preview result construction invariants
# ---------------------------------------------------------------------------

class TestPreviewResultConstruction:
    def _valid_preview(self, **overrides):
        defaults = {
            "command_ref": "cmd-1",
            "preview_status": "preview_available",
            "would_require_resolution": False,
            "visible_preview": "Preview text.",
            "visible_risk_refs": (),
            "visible_target_refs": ("lever-brass-threshold",),
            "hidden_fact_refs_used_by_backend": (),
        }
        defaults.update(overrides)
        return TinyVerticalSliceCommandPreviewResult(**defaults)

    def test_rejects_bare_string_for_hidden_fact_refs(self):
        with pytest.raises(TinyVerticalSliceError, match="hidden_fact_refs_used_by_backend"):
            self._valid_preview(hidden_fact_refs_used_by_backend="hidden-fact-lever-feeds-clock")

    def test_rejects_non_sequence_for_hidden_fact_refs(self):
        with pytest.raises(TinyVerticalSliceError, match="hidden_fact_refs_used_by_backend"):
            self._valid_preview(hidden_fact_refs_used_by_backend=123)

    def test_rejects_empty_string_item_in_hidden_fact_refs(self):
        with pytest.raises(TinyVerticalSliceError, match="hidden_fact_refs_used_by_backend"):
            self._valid_preview(hidden_fact_refs_used_by_backend=("hidden-fact-lever-feeds-clock", ""))

    def test_rejects_non_string_item_in_hidden_fact_refs(self):
        with pytest.raises(TinyVerticalSliceError, match="hidden_fact_refs_used_by_backend"):
            self._valid_preview(hidden_fact_refs_used_by_backend=("hidden-fact-lever-feeds-clock", 123))

    def test_accepts_list_of_non_empty_strings_and_normalizes_to_tuple(self):
        preview = self._valid_preview(hidden_fact_refs_used_by_backend=["a", "b"])
        assert isinstance(preview.hidden_fact_refs_used_by_backend, tuple)
        assert preview.hidden_fact_refs_used_by_backend == ("a", "b")


# ---------------------------------------------------------------------------
# Lifecycle result construction invariants
# ---------------------------------------------------------------------------

class TestLifecycleResultConstruction:
    def _valid_result(self, world, command, validation, preview, **overrides):
        defaults = {
            "command_ref": command.command_ref,
            "lifecycle_status": "validated_preview",
            "commit_status": "commit_ready" if command.requests_commit else "not_requested",
            "state_changed": False,
            "event_committed": False,
            "command": command,
            "validation": validation,
            "preview": preview,
            "resulting_state": world,
        }
        defaults.update(overrides)
        return TinyVerticalSliceCommandLifecycleResult(**defaults)

    def _make_validation_preview(self, world, **command_overrides):
        command = create_tiny_vertical_slice_command_intent(**command_overrides)
        validation = validate_tiny_vertical_slice_command_intent(state=world, command=command)
        preview = preview_tiny_vertical_slice_command_intent(state=world, command=command, validation=validation)
        return command, validation, preview

    def test_rejects_state_changed_true(self, world):
        command, validation, preview = self._make_validation_preview(world)
        with pytest.raises(TinyVerticalSliceError, match="state_changed"):
            self._valid_result(world, command, validation, preview, state_changed=True)

    def test_rejects_event_committed_true(self, world):
        command, validation, preview = self._make_validation_preview(world)
        with pytest.raises(TinyVerticalSliceError, match="event_committed"):
            self._valid_result(world, command, validation, preview, event_committed=True)

    def test_invalid_validation_rejects_validated_preview_lifecycle_status(self, world):
        command, validation, preview = self._make_validation_preview(world, actor_ref="actor-unknown")
        with pytest.raises(TinyVerticalSliceError, match="lifecycle_status"):
            self._valid_result(
                world, command, validation, preview, lifecycle_status="validated_preview", commit_status="blocked"
            )

    def test_invalid_validation_rejects_not_requested_commit_status(self, world):
        command, validation, preview = self._make_validation_preview(world, actor_ref="actor-unknown")
        with pytest.raises(TinyVerticalSliceError, match="commit_status"):
            self._valid_result(
                world, command, validation, preview, lifecycle_status="blocked", commit_status="not_requested"
            )

    def test_invalid_validation_rejects_commit_ready_commit_status(self, world):
        command, validation, preview = self._make_validation_preview(world, actor_ref="actor-unknown")
        with pytest.raises(TinyVerticalSliceError, match="commit_status"):
            self._valid_result(
                world, command, validation, preview, lifecycle_status="blocked", commit_status="commit_ready"
            )

    def test_valid_non_commit_command_rejects_commit_ready(self, world):
        command, validation, preview = self._make_validation_preview(world, requests_commit=False)
        with pytest.raises(TinyVerticalSliceError, match="commit_status"):
            self._valid_result(world, command, validation, preview, commit_status="commit_ready")

    def test_valid_commit_requesting_command_rejects_not_requested(self, world):
        command, validation, preview = self._make_validation_preview(world, requests_commit=True)
        with pytest.raises(TinyVerticalSliceError, match="commit_status"):
            self._valid_result(world, command, validation, preview, commit_status="not_requested")

    def test_valid_validation_rejects_preview_blocked_preview_status(self, world):
        command, validation, preview = self._make_validation_preview(world)
        bad_preview = TinyVerticalSliceCommandPreviewResult(
            command_ref=command.command_ref,
            preview_status="preview_blocked",
            would_require_resolution=False,
            visible_preview="Blocked.",
            visible_risk_refs=(),
            visible_target_refs=(),
            hidden_fact_refs_used_by_backend=(),
        )
        with pytest.raises(TinyVerticalSliceError, match="preview.preview_status"):
            self._valid_result(world, command, validation, bad_preview)

    def test_invalid_validation_rejects_preview_available_preview_status(self, world):
        command, validation, preview = self._make_validation_preview(world, actor_ref="actor-unknown")
        bad_preview = TinyVerticalSliceCommandPreviewResult(
            command_ref=command.command_ref,
            preview_status="preview_available",
            would_require_resolution=False,
            visible_preview="Available.",
            visible_risk_refs=(),
            visible_target_refs=(),
            hidden_fact_refs_used_by_backend=(),
        )
        with pytest.raises(TinyVerticalSliceError, match="preview.preview_status"):
            self._valid_result(
                world, command, validation, bad_preview, lifecycle_status="blocked", commit_status="blocked"
            )


# ---------------------------------------------------------------------------
# Source scan — forbidden patterns
# ---------------------------------------------------------------------------

class TestSourceScan:
    _FORBIDDEN_PATTERNS = [
        "openai",
        "anthropic",
        "ollama",
        "claude",
        "call_model",
        "invoke_model",
        "generate_narration",
        "json.loads",
        "ast.literal_eval",
        "re.search",
        "re.match",
        "roll_dice",
        "commit_event(",
        "apply_delta(",
        "mutate_state",
        "persist_state",
        "replay_event",
        "state_store.get",
        "event_ledger.get",
        "open(",
        ".read_text(",
        ".write_text(",
    ]

    def test_production_module_has_no_forbidden_patterns(self):
        source_path = Path(__file__).resolve().parent.parent / "src" / "astra_runtime" / "domain" / "tiny_vertical_slice.py"
        source = source_path.read_text(encoding="utf-8")
        for pattern in self._FORBIDDEN_PATTERNS:
            assert pattern not in source, f"Forbidden pattern found in production module: {pattern!r}"

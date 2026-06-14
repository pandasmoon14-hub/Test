"""PR-8 Increment 3 — tiny vertical slice resource/consequence planning preview bridge tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    ResourceMathRequest,
    ResourceMathResult,
    TinyVerticalSliceCommandLifecycleResult,
    TinyVerticalSliceError,
    TinyVerticalSliceResourceConsequencePlanningPreview,
    TinyVerticalSliceWorldState,
    build_tiny_vertical_slice_resource_consequence_planning_preview,
    create_resource_math_request,
    create_resource_math_result,
    create_resource_math_subject_reference,
    create_tiny_vertical_slice_command_intent,
    create_tiny_vertical_slice_world_state,
    run_tiny_vertical_slice_command_lifecycle,
    serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview,
    validate_resource_math_request,
    validate_resource_math_result,
)


@pytest.fixture()
def world():
    return create_tiny_vertical_slice_world_state()


@pytest.fixture()
def default_lifecycle(world):
    command = create_tiny_vertical_slice_command_intent()
    return run_tiny_vertical_slice_command_lifecycle(state=world, command=command)


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment3_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSliceResourceConsequencePlanningPreview",
            "build_tiny_vertical_slice_resource_consequence_planning_preview",
            "serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview",
        ]
        for name in expected:
            assert hasattr(domain, name), f"Missing export: {name}"


# ---------------------------------------------------------------------------
# Frozen dataclass
# ---------------------------------------------------------------------------

class TestFrozenDataclass:
    def test_preview_dataclass_is_frozen(self):
        assert TinyVerticalSliceResourceConsequencePlanningPreview.__dataclass_params__.frozen is True


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def _valid_preview_kwargs(lifecycle, **overrides):
    command = lifecycle.command
    request_id = f"resource-math-request-{command.command_ref}"
    actor_subject = create_resource_math_subject_reference(
        subject_binding_id="subject-actor-1",
        subject_type="actor",
        subject_ref_id="actor-1",
        subject_role="primary_subject",
        owner_domain="RT002_resource_consequence_math",
        visibility_policy="actor_visible",
    )
    request = create_resource_math_request(
        request_id=request_id,
        trace_ref_id=f"tiny-slice-trace-{command.command_ref}",
        subject_refs=[actor_subject],
        command_ref_id=command.command_ref,
        metadata={},
    )
    result = create_resource_math_result(
        result_id=f"resource-math-result-{command.command_ref}",
        request_id=request_id,
        trace_ref_id=f"tiny-slice-trace-{command.command_ref}",
        stage="calculation_ready_for_review",
        decision="accepted_for_planning",
        blocking=False,
        request=request,
        metadata={},
    )
    defaults = {
        "preview_ref": "preview-1",
        "command_ref": command.command_ref,
        "lifecycle_status": lifecycle.lifecycle_status,
        "commit_status": lifecycle.commit_status,
        "resource_math_request": request,
        "resource_math_result": result,
        "visible_summary": "summary",
        "visible_cost_refs": (),
        "visible_consequence_refs": (),
        "visible_dependency_refs": (),
        "backend_only_ref_ids": (),
        "calculation_executed": False,
        "settlement_authorized": False,
        "consequence_application_authorized": False,
        "state_changed": False,
        "event_committed": False,
    }
    defaults.update(overrides)
    return defaults


# ---------------------------------------------------------------------------
# Construction invariants
# ---------------------------------------------------------------------------

class TestConstructionInvariants:
    def test_rejects_non_resource_math_request(self, default_lifecycle):
        kwargs = _valid_preview_kwargs(default_lifecycle)
        kwargs["resource_math_request"] = "not a request"
        with pytest.raises(TinyVerticalSliceError, match="resource_math_request"):
            TinyVerticalSliceResourceConsequencePlanningPreview(**kwargs)

    def test_rejects_non_resource_math_result(self, default_lifecycle):
        kwargs = _valid_preview_kwargs(default_lifecycle)
        kwargs["resource_math_result"] = "not a result"
        with pytest.raises(TinyVerticalSliceError, match="resource_math_result"):
            TinyVerticalSliceResourceConsequencePlanningPreview(**kwargs)

    def test_rejects_mismatched_request_result_ids(self, default_lifecycle):
        kwargs = _valid_preview_kwargs(default_lifecycle)
        result = create_resource_math_result(
            result_id="resource-math-result-other",
            request_id="resource-math-request-other",
            trace_ref_id="tiny-slice-trace-other",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            metadata={},
        )
        kwargs["resource_math_result"] = result
        with pytest.raises(TinyVerticalSliceError, match="request_id"):
            TinyVerticalSliceResourceConsequencePlanningPreview(**kwargs)

    @pytest.mark.parametrize("field", [
        "calculation_executed",
        "settlement_authorized",
        "consequence_application_authorized",
        "state_changed",
        "event_committed",
    ])
    def test_rejects_true_authority_field(self, default_lifecycle, field):
        kwargs = _valid_preview_kwargs(default_lifecycle)
        kwargs[field] = True
        with pytest.raises(TinyVerticalSliceError, match=field):
            TinyVerticalSliceResourceConsequencePlanningPreview(**kwargs)

    def test_tuple_fields_normalize_to_tuples(self, default_lifecycle):
        kwargs = _valid_preview_kwargs(default_lifecycle)
        kwargs["visible_cost_refs"] = ["cost-1", "cost-2"]
        kwargs["visible_consequence_refs"] = ["consequence-1"]
        kwargs["visible_dependency_refs"] = ["dep-1"]
        preview = TinyVerticalSliceResourceConsequencePlanningPreview(**kwargs)
        assert isinstance(preview.visible_cost_refs, tuple)
        assert preview.visible_cost_refs == ("cost-1", "cost-2")
        assert isinstance(preview.visible_consequence_refs, tuple)
        assert isinstance(preview.visible_dependency_refs, tuple)

    def test_backend_only_ref_ids_accepts_list_and_normalizes(self, default_lifecycle):
        kwargs = _valid_preview_kwargs(default_lifecycle)
        kwargs["backend_only_ref_ids"] = ["hidden-1", "hidden-2"]
        preview = TinyVerticalSliceResourceConsequencePlanningPreview(**kwargs)
        assert isinstance(preview.backend_only_ref_ids, tuple)
        assert preview.backend_only_ref_ids == ("hidden-1", "hidden-2")

    def test_metadata_deep_copied_and_frozen(self, default_lifecycle):
        kwargs = _valid_preview_kwargs(default_lifecycle)
        source = {"nested": {"k": "v"}}
        kwargs["metadata"] = source
        preview = TinyVerticalSliceResourceConsequencePlanningPreview(**kwargs)
        source["nested"]["k"] = "changed"
        assert preview.metadata["nested"]["k"] == "v"
        assert isinstance(preview.metadata, MappingProxyType)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class TestBuilder:
    def test_default_inspect_lifecycle_produces_planning_preview(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        assert isinstance(preview, TinyVerticalSliceResourceConsequencePlanningPreview)
        assert preview.command_ref == default_lifecycle.command.command_ref

    def test_pull_lever_lifecycle_produces_planning_preview(self, world):
        command = create_tiny_vertical_slice_command_intent(command_kind="pull_lever", command_ref="cmd-pull-1")
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lifecycle
        )
        assert preview.lifecycle_status == "validated_preview"
        assert "pull_lever" in preview.resource_math_request.metadata["command_kind"]

    def test_brace_mechanism_lifecycle_produces_planning_preview(self, world):
        command = create_tiny_vertical_slice_command_intent(
            command_kind="brace_mechanism", command_ref="cmd-brace-1"
        )
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lifecycle
        )
        assert preview.lifecycle_status == "validated_preview"

    def test_speak_to_npc_lifecycle_produces_planning_preview(self, world):
        command = create_tiny_vertical_slice_command_intent(
            command_kind="speak_to_npc", target_ref="npc-watchful-adept", command_ref="cmd-speak-1"
        )
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lifecycle
        )
        assert preview.lifecycle_status == "validated_preview"

    def test_invalid_lifecycle_produces_blocked_planning_preview(self, world):
        command = create_tiny_vertical_slice_command_intent(actor_ref="actor-unknown")
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lifecycle
        )
        assert preview.lifecycle_status == "blocked"
        assert "blocked" in preview.visible_summary.lower()
        assert preview.calculation_executed is False
        assert preview.state_changed is False
        assert preview.event_committed is False

    def test_builder_rejects_non_world_state_input(self, default_lifecycle):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceWorldState"):
            build_tiny_vertical_slice_resource_consequence_planning_preview(
                state="not a world", lifecycle_result=default_lifecycle
            )

    def test_builder_rejects_non_lifecycle_input(self, world):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceCommandLifecycleResult"):
            build_tiny_vertical_slice_resource_consequence_planning_preview(
                state=world, lifecycle_result="not a lifecycle"
            )

    def test_builder_rejects_mismatched_resulting_state(self, world):
        other_world = create_tiny_vertical_slice_world_state()
        command = create_tiny_vertical_slice_command_intent()
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=other_world, command=command)
        with pytest.raises(TinyVerticalSliceError, match="resulting_state"):
            build_tiny_vertical_slice_resource_consequence_planning_preview(
                state=world, lifecycle_result=lifecycle
            )

    def test_request_is_resource_math_request(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        assert isinstance(preview.resource_math_request, ResourceMathRequest)

    def test_result_is_resource_math_result(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        assert isinstance(preview.resource_math_result, ResourceMathResult)

    def test_result_request_id_equals_request_request_id(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        assert preview.resource_math_result.request_id == preview.resource_math_request.request_id

    def test_all_pr5_authority_booleans_remain_false(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        authority_fields = [
            "calculation_executed",
            "affordability_executed",
            "reservation_authorized",
            "settlement_authorized",
            "consequence_application_authorized",
            "mutation_authorized",
            "state_delta_application_authorized",
            "transaction_execution_authorized",
            "event_commitment_authorized",
            "event_append_authorized",
            "rng_execution_authorized",
            "table_oracle_execution_authorized",
            "model_authority_authorized",
        ]
        for field in authority_fields:
            assert getattr(preview.resource_math_request, field) is False
            assert getattr(preview.resource_math_result, field) is False

    def test_request_validates(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        assert validate_resource_math_request(preview.resource_math_request) is True

    def test_result_validates(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        assert validate_resource_math_result(
            preview.resource_math_result, request=preview.resource_math_request
        ) is True

    def test_builder_does_not_mutate_state(self, world, default_lifecycle):
        original_tick = world.hazard_clock.current_tick
        original_lever_state = world.lever.visible_state
        build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        assert world.hazard_clock.current_tick == original_tick
        assert world.lever.visible_state == original_lever_state

    def test_builder_does_not_commit_event(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        assert preview.event_committed is False
        assert preview.resource_math_request.event_commitment_authorized is False
        assert preview.resource_math_result.event_commitment_authorized is False


# ---------------------------------------------------------------------------
# Visible serializer
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_rejects_non_preview_input(self):
        with pytest.raises(TinyVerticalSliceError):
            serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview("not a preview")

    def test_exact_top_level_key_order(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        serialized = serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview(preview)
        expected_keys = [
            "preview_ref",
            "command_ref",
            "lifecycle_status",
            "commit_status",
            "visible_summary",
            "visible_cost_refs",
            "visible_consequence_refs",
            "visible_dependency_refs",
            "calculation_executed",
            "settlement_authorized",
            "consequence_application_authorized",
            "state_changed",
            "event_committed",
            "resource_math_request",
            "resource_math_result",
            "metadata",
        ]
        assert list(serialized.keys()) == expected_keys

    def test_omits_backend_only_ref_ids(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        serialized = serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview(preview)
        assert "backend_only_ref_ids" not in serialized

    def test_omits_hidden_fact_label(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        serialized = serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview(preview)
        text = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_label not in text

    def test_omits_hidden_fact_backend_only_description(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        serialized = serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview(preview)
        text = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in text

    def test_omits_reveal_condition(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        serialized = serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview(preview)
        text = json.dumps(serialized)
        assert world.hidden_fact.reveal_condition not in text

    def test_tuple_fields_serialize_as_lists(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        serialized = serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview(preview)
        assert isinstance(serialized["visible_cost_refs"], list)
        assert isinstance(serialized["visible_consequence_refs"], list)
        assert isinstance(serialized["visible_dependency_refs"], list)

    def test_metadata_serializes_as_dict(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle, metadata={"k": "v"}
        )
        serialized = serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview(preview)
        assert isinstance(serialized["metadata"], dict)
        assert not isinstance(serialized["metadata"], MappingProxyType)

    def test_serialized_request_result_authority_booleans_false(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        serialized = serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview(preview)
        for field in [
            "calculation_executed",
            "settlement_authorized",
            "consequence_application_authorized",
            "mutation_authorized",
            "event_commitment_authorized",
            "rng_execution_authorized",
        ]:
            assert serialized["resource_math_request"][field] is False
            assert serialized["resource_math_result"][field] is False

    def test_serialized_request_result_do_not_expose_backend_hidden_refs(self, world, default_lifecycle):
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=default_lifecycle
        )
        serialized = serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview(preview)
        text = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_ref not in text


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

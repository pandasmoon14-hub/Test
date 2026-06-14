"""PR-8 Increment 4 — tiny vertical slice context packet projection bridge tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    NoCommitIntentPacket,
    TinyVerticalSliceContextPacketProjection,
    TinyVerticalSliceError,
    VisibleSummaryPacket,
    build_tiny_vertical_slice_context_packet_projection,
    build_tiny_vertical_slice_resource_consequence_planning_preview,
    create_no_commit_intent_packet,
    create_tiny_vertical_slice_command_intent,
    create_tiny_vertical_slice_world_state,
    create_visible_summary_packet,
    run_tiny_vertical_slice_command_lifecycle,
    serialize_tiny_vertical_slice_context_packet_projection_visible,
    validate_no_commit_intent_packet,
    validate_visible_summary_packet,
)


@pytest.fixture()
def world():
    return create_tiny_vertical_slice_world_state()


@pytest.fixture()
def default_lifecycle(world):
    command = create_tiny_vertical_slice_command_intent()
    return run_tiny_vertical_slice_command_lifecycle(state=world, command=command)


@pytest.fixture()
def default_planning_preview(world, default_lifecycle):
    return build_tiny_vertical_slice_resource_consequence_planning_preview(
        state=world, lifecycle_result=default_lifecycle
    )


@pytest.fixture()
def default_projection(world, default_lifecycle, default_planning_preview):
    return build_tiny_vertical_slice_context_packet_projection(
        state=world,
        lifecycle_result=default_lifecycle,
        planning_preview=default_planning_preview,
    )


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment4_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSliceContextPacketProjection",
            "build_tiny_vertical_slice_context_packet_projection",
            "serialize_tiny_vertical_slice_context_packet_projection_visible",
        ]
        for name in expected:
            assert hasattr(domain, name), f"Missing export: {name}"


# ---------------------------------------------------------------------------
# Frozen dataclass
# ---------------------------------------------------------------------------

class TestFrozenDataclass:
    def test_projection_dataclass_is_frozen(self):
        assert TinyVerticalSliceContextPacketProjection.__dataclass_params__.frozen is True


# ---------------------------------------------------------------------------
# Construction helpers
# ---------------------------------------------------------------------------

def _valid_packets(command_ref):
    no_commit = create_no_commit_intent_packet(
        intent_ref=command_ref,
        actor_ref="actor-1",
        proposed_action_kind="inspect_lever",
        intent_timestamp="t0",
        target_refs=("target-1",),
    )
    summary = create_visible_summary_packet(
        summary_ref=f"tiny-slice-visible-summary-{command_ref}",
        summary_scope="tiny_vertical_slice_runtime_preview",
        summary_timestamp="t0",
        visible_fact_refs=("ref-1", "ref-2"),
    )
    return no_commit, summary


def _valid_projection_kwargs(base_command_ref, **overrides):
    no_commit, summary = _valid_packets(base_command_ref)
    defaults = {
        "projection_ref": "projection-1",
        "command_ref": base_command_ref,
        "world_ref": "world-1",
        "no_commit_intent_packet": no_commit,
        "visible_summary_packet": summary,
        "packet_refs": (no_commit.intent_ref, summary.summary_ref),
        "visible_packet_kinds": ("no_commit_intent", "visible_summary"),
        "visible_context_refs": ("ref-1",),
        "excluded_backend_ref_ids": (),
        "hidden_information_excluded": True,
        "state_changed": False,
        "event_committed": False,
        "model_called": False,
        "narration_generated": False,
    }
    defaults.update(overrides)
    return defaults


# ---------------------------------------------------------------------------
# Construction invariants
# ---------------------------------------------------------------------------

class TestConstructionInvariants:
    def test_rejects_non_no_commit_intent_packet(self):
        kwargs = _valid_projection_kwargs("cmd-1")
        kwargs["no_commit_intent_packet"] = "not a packet"
        with pytest.raises(TinyVerticalSliceError, match="no_commit_intent_packet"):
            TinyVerticalSliceContextPacketProjection(**kwargs)

    def test_rejects_non_visible_summary_packet(self):
        kwargs = _valid_projection_kwargs("cmd-1")
        kwargs["visible_summary_packet"] = "not a packet"
        with pytest.raises(TinyVerticalSliceError, match="visible_summary_packet"):
            TinyVerticalSliceContextPacketProjection(**kwargs)

    def test_rejects_empty_projection_ref(self):
        kwargs = _valid_projection_kwargs("cmd-1", projection_ref="")
        with pytest.raises(TinyVerticalSliceError, match="projection_ref"):
            TinyVerticalSliceContextPacketProjection(**kwargs)

    def test_rejects_empty_command_ref(self):
        kwargs = _valid_projection_kwargs("cmd-1")
        kwargs["command_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="command_ref"):
            TinyVerticalSliceContextPacketProjection(**kwargs)

    def test_rejects_empty_world_ref(self):
        kwargs = _valid_projection_kwargs("cmd-1", world_ref="")
        with pytest.raises(TinyVerticalSliceError, match="world_ref"):
            TinyVerticalSliceContextPacketProjection(**kwargs)

    def test_rejects_hidden_information_excluded_false(self):
        kwargs = _valid_projection_kwargs("cmd-1", hidden_information_excluded=False)
        with pytest.raises(TinyVerticalSliceError, match="hidden_information_excluded"):
            TinyVerticalSliceContextPacketProjection(**kwargs)

    @pytest.mark.parametrize("field", [
        "state_changed",
        "event_committed",
        "model_called",
        "narration_generated",
    ])
    def test_rejects_true_negated_field(self, field):
        kwargs = _valid_projection_kwargs("cmd-1", **{field: True})
        with pytest.raises(TinyVerticalSliceError, match=field):
            TinyVerticalSliceContextPacketProjection(**kwargs)

    def test_tuple_fields_normalize_to_tuples(self):
        kwargs = _valid_projection_kwargs(
            "cmd-1",
            packet_refs=list(_valid_packets("cmd-1")[0].intent_ref for _ in [0])
            + list(_valid_packets("cmd-1")[1].summary_ref for _ in [0]),
            visible_packet_kinds=["no_commit_intent", "visible_summary"],
            visible_context_refs=["a", "b"],
            excluded_backend_ref_ids=["hidden-1"],
        )
        projection = TinyVerticalSliceContextPacketProjection(**kwargs)
        assert isinstance(projection.packet_refs, tuple)
        assert isinstance(projection.visible_packet_kinds, tuple)
        assert isinstance(projection.visible_context_refs, tuple)
        assert isinstance(projection.excluded_backend_ref_ids, tuple)

    def test_metadata_deep_copied_and_frozen(self):
        kwargs = _valid_projection_kwargs("cmd-1")
        source = {"nested": {"k": "v"}}
        kwargs["metadata"] = source
        projection = TinyVerticalSliceContextPacketProjection(**kwargs)
        source["nested"]["k"] = "changed"
        assert projection.metadata["nested"]["k"] == "v"
        assert isinstance(projection.metadata, MappingProxyType)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class TestBuilder:
    def test_default_inspect_lifecycle_produces_projection(self, world, default_lifecycle, default_planning_preview):
        projection = build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=default_lifecycle, planning_preview=default_planning_preview
        )
        assert isinstance(projection, TinyVerticalSliceContextPacketProjection)
        assert projection.command_ref == default_lifecycle.command.command_ref

    def test_pull_lever_lifecycle_produces_projection(self, world):
        command = create_tiny_vertical_slice_command_intent(command_kind="pull_lever", command_ref="cmd-pull-1")
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(state=world, lifecycle_result=lifecycle)
        projection = build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=lifecycle, planning_preview=preview
        )
        assert projection.command_ref == command.command_ref
        assert world.hazard_clock.clock_ref in projection.visible_context_refs

    def test_brace_mechanism_lifecycle_produces_projection(self, world):
        command = create_tiny_vertical_slice_command_intent(command_kind="brace_mechanism", command_ref="cmd-brace-1")
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(state=world, lifecycle_result=lifecycle)
        projection = build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=lifecycle, planning_preview=preview
        )
        assert projection.command_ref == command.command_ref
        assert world.lever.lever_ref in projection.visible_context_refs

    def test_speak_to_npc_lifecycle_produces_projection(self, world):
        command = create_tiny_vertical_slice_command_intent(
            command_kind="speak_to_npc", target_ref="npc-watchful-adept", command_ref="cmd-speak-1"
        )
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(state=world, lifecycle_result=lifecycle)
        projection = build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=lifecycle, planning_preview=preview
        )
        assert projection.command_ref == command.command_ref
        assert world.npc.npc_ref in projection.visible_context_refs

    def test_builder_rejects_non_world_state_input(self, default_lifecycle, default_planning_preview):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceWorldState"):
            build_tiny_vertical_slice_context_packet_projection(
                state="not a world",
                lifecycle_result=default_lifecycle,
                planning_preview=default_planning_preview,
            )

    def test_builder_rejects_non_lifecycle_input(self, world, default_planning_preview):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceCommandLifecycleResult"):
            build_tiny_vertical_slice_context_packet_projection(
                state=world,
                lifecycle_result="not a lifecycle",
                planning_preview=default_planning_preview,
            )

    def test_builder_rejects_non_planning_preview_input(self, world, default_lifecycle):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceResourceConsequencePlanningPreview"):
            build_tiny_vertical_slice_context_packet_projection(
                state=world,
                lifecycle_result=default_lifecycle,
                planning_preview="not a preview",
            )

    def test_builder_rejects_mismatched_resulting_state(self, world):
        other_world = create_tiny_vertical_slice_world_state()
        command = create_tiny_vertical_slice_command_intent()
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=other_world, command=command)
        preview = build_tiny_vertical_slice_resource_consequence_planning_preview(state=other_world, lifecycle_result=lifecycle)
        with pytest.raises(TinyVerticalSliceError, match="resulting_state"):
            build_tiny_vertical_slice_context_packet_projection(
                state=world, lifecycle_result=lifecycle, planning_preview=preview
            )

    def test_builder_rejects_planning_preview_command_ref_mismatch(self, world, default_lifecycle, default_planning_preview):
        other_command = create_tiny_vertical_slice_command_intent(command_ref="cmd-other")
        other_lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=other_command)
        other_preview = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=other_lifecycle
        )
        with pytest.raises(TinyVerticalSliceError, match="planning_preview.command_ref"):
            build_tiny_vertical_slice_context_packet_projection(
                state=world, lifecycle_result=default_lifecycle, planning_preview=other_preview
            )

    def test_no_state_mutation(self, world, default_lifecycle, default_planning_preview):
        original_tick = world.hazard_clock.current_tick
        original_lever_state = world.lever.visible_state
        build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=default_lifecycle, planning_preview=default_planning_preview
        )
        assert world.hazard_clock.current_tick == original_tick
        assert world.lever.visible_state == original_lever_state

    def test_no_event_commitment(self, default_projection):
        assert default_projection.event_committed is False

    def test_no_model_call_flag(self, default_projection):
        assert default_projection.model_called is False

    def test_no_narration_generated_flag(self, default_projection):
        assert default_projection.narration_generated is False

    def test_no_commit_packet_type(self, default_projection):
        assert isinstance(default_projection.no_commit_intent_packet, NoCommitIntentPacket)

    def test_visible_summary_packet_type(self, default_projection):
        assert isinstance(default_projection.visible_summary_packet, VisibleSummaryPacket)

    def test_no_commit_packet_validates(self, default_projection):
        assert validate_no_commit_intent_packet(default_projection.no_commit_intent_packet) is True

    def test_visible_summary_packet_validates(self, default_projection):
        assert validate_visible_summary_packet(default_projection.visible_summary_packet) is True

    def test_packet_refs_match_packet_refs(self, default_projection):
        expected = {
            default_projection.no_commit_intent_packet.intent_ref,
            default_projection.visible_summary_packet.summary_ref,
        }
        assert set(default_projection.packet_refs) == expected

    def test_visible_packet_kinds(self, default_projection):
        assert default_projection.visible_packet_kinds == ("no_commit_intent", "visible_summary")

    def test_visible_context_refs_contains_expected_visible_refs(self, world, default_projection, default_planning_preview):
        refs = default_projection.visible_context_refs
        assert world.scene.scene_ref in refs
        assert world.actor.actor_ref in refs
        assert world.injury.injury_ref in refs
        assert default_planning_preview.preview_ref in refs

    def test_excluded_backend_refs_retained_but_not_serialized(self, world, default_projection):
        assert world.hidden_fact.hidden_fact_ref in default_projection.excluded_backend_ref_ids
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        assert "excluded_backend_ref_ids" not in serialized


# ---------------------------------------------------------------------------
# Visible serializer
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_rejects_non_projection_input(self):
        with pytest.raises(TinyVerticalSliceError):
            serialize_tiny_vertical_slice_context_packet_projection_visible("not a projection")

    def test_exact_top_level_key_order(self, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        expected_keys = [
            "projection_ref",
            "command_ref",
            "world_ref",
            "packet_refs",
            "visible_packet_kinds",
            "visible_context_refs",
            "hidden_information_excluded",
            "state_changed",
            "event_committed",
            "model_called",
            "narration_generated",
            "no_commit_intent_packet",
            "visible_summary_packet",
            "metadata",
        ]
        assert list(serialized.keys()) == expected_keys

    def test_omits_excluded_backend_ref_ids(self, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        assert "excluded_backend_ref_ids" not in serialized

    def test_omits_hidden_fact_ref(self, world, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        text = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_ref not in text

    def test_omits_hidden_fact_label(self, world, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        text = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_label not in text

    def test_omits_backend_only_description(self, world, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        text = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in text

    def test_omits_reveal_condition(self, world, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        text = json.dumps(serialized)
        assert world.hidden_fact.reveal_condition not in text

    def test_tuple_fields_serialize_as_lists(self, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        assert isinstance(serialized["packet_refs"], list)
        assert isinstance(serialized["visible_packet_kinds"], list)
        assert isinstance(serialized["visible_context_refs"], list)

    def test_metadata_serializes_as_dict(self, world, default_lifecycle, default_planning_preview):
        projection = build_tiny_vertical_slice_context_packet_projection(
            state=world,
            lifecycle_result=default_lifecycle,
            planning_preview=default_planning_preview,
            metadata={"k": "v"},
        )
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(projection)
        assert isinstance(serialized["metadata"], dict)
        assert not isinstance(serialized["metadata"], MappingProxyType)

    def test_no_commit_packet_flags(self, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        packet = serialized["no_commit_intent_packet"]
        assert packet["hidden_information_excluded"] is True
        assert packet["no_commit_marker"] is True

    def test_visible_summary_packet_flags(self, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        packet = serialized["visible_summary_packet"]
        assert packet["hidden_information_excluded"] is True
        assert packet["committed_state_only"] is True

    def test_visible_summary_forbidden_claims(self, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        claims = serialized["visible_summary_packet"]["forbidden_claims"]
        for claim in [
            "do_not_claim_state_changed",
            "do_not_claim_event_committed",
            "do_not_claim_hidden_fact",
            "do_not_roll_dice",
            "do_not_resolve_action",
            "do_not_generate_reward",
        ]:
            assert claim in claims

    def test_serializer_booleans_false(self, default_projection):
        serialized = serialize_tiny_vertical_slice_context_packet_projection_visible(default_projection)
        assert serialized["state_changed"] is False
        assert serialized["event_committed"] is False
        assert serialized["model_called"] is False
        assert serialized["narration_generated"] is False


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

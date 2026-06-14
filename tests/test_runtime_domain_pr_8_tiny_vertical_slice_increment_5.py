"""PR-8 Increment 5 — tiny vertical slice state delta candidate preview tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    TinyVerticalSliceContextPacketProjection,
    TinyVerticalSliceError,
    TinyVerticalSliceStateDeltaCandidatePreview,
    build_tiny_vertical_slice_context_packet_projection,
    build_tiny_vertical_slice_resource_consequence_planning_preview,
    build_tiny_vertical_slice_state_delta_candidate_preview,
    create_no_commit_intent_packet,
    create_tiny_vertical_slice_command_intent,
    create_tiny_vertical_slice_world_state,
    create_visible_summary_packet,
    run_tiny_vertical_slice_command_lifecycle,
    serialize_tiny_vertical_slice_state_delta_candidate_visible_preview,
)
from astra_runtime.kernel.record_identity import is_valid_record_id
from astra_runtime.kernel.state_delta import (
    StateDeltaEnvelope,
    create_state_delta_envelope,
    validate_state_delta_envelope,
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
def default_context_projection(world, default_lifecycle, default_planning_preview):
    return build_tiny_vertical_slice_context_packet_projection(
        state=world,
        lifecycle_result=default_lifecycle,
        planning_preview=default_planning_preview,
    )


@pytest.fixture()
def default_delta_preview(world, default_lifecycle, default_planning_preview, default_context_projection):
    return build_tiny_vertical_slice_state_delta_candidate_preview(
        state=world,
        lifecycle_result=default_lifecycle,
        planning_preview=default_planning_preview,
        context_projection=default_context_projection,
    )


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment5_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSliceStateDeltaCandidatePreview",
            "build_tiny_vertical_slice_state_delta_candidate_preview",
            "serialize_tiny_vertical_slice_state_delta_candidate_visible_preview",
        ]
        for name in expected:
            assert hasattr(domain, name), f"Missing export: {name}"


# ---------------------------------------------------------------------------
# Frozen dataclass
# ---------------------------------------------------------------------------

class TestFrozenDataclass:
    def test_preview_dataclass_is_frozen(self):
        assert TinyVerticalSliceStateDeltaCandidatePreview.__dataclass_params__.frozen is True


# ---------------------------------------------------------------------------
# Construction helpers
# ---------------------------------------------------------------------------

def _make_context_projection(command_ref, world_ref="world-1"):
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
    return TinyVerticalSliceContextPacketProjection(
        projection_ref="projection-1",
        command_ref=command_ref,
        world_ref=world_ref,
        no_commit_intent_packet=no_commit,
        visible_summary_packet=summary,
        packet_refs=(no_commit.intent_ref, summary.summary_ref),
        visible_packet_kinds=("no_commit_intent", "visible_summary"),
        visible_context_refs=("ref-1",),
        excluded_backend_ref_ids=(),
        hidden_information_excluded=True,
        state_changed=False,
        event_committed=False,
        model_called=False,
        narration_generated=False,
    )


def _valid_delta_envelopes(command_ref, delta_preview_ref):
    return (
        create_state_delta_envelope(
            delta_id=f"state-delta-candidate-{command_ref}-lever",
            source_command_id=command_ref,
            source_preview_id=delta_preview_ref,
            affected_record_ids=("astra:item:brass_threshold_lever",),
            change_type="record_update",
            payload={"applied": False},
            metadata={},
        ),
    )


def _valid_preview_kwargs(command_ref, base_delta_preview_ref, **overrides):
    envelopes = _valid_delta_envelopes(command_ref, base_delta_preview_ref)
    context_projection = _make_context_projection(command_ref)
    defaults = {
        "delta_preview_ref": base_delta_preview_ref,
        "command_ref": command_ref,
        "world_ref": "world-1",
        "lifecycle_status": "validated_preview",
        "commit_status": "not_requested",
        "planning_preview_ref": "preview-1",
        "context_projection_ref": context_projection.projection_ref,
        "candidate_delta_envelopes": envelopes,
        "candidate_delta_refs": tuple(e.delta_id for e in envelopes),
        "affected_visible_record_refs": ("lever-1",),
        "visible_delta_summary": "summary",
        "visible_change_kinds": ("lever_state_candidate",),
        "backend_only_ref_ids": (),
        "apply_authorized": False,
        "state_changed": False,
        "event_committed": False,
        "persistence_authorized": False,
        "replay_authorized": False,
    }
    defaults.update(overrides)
    return defaults


# ---------------------------------------------------------------------------
# Construction invariants
# ---------------------------------------------------------------------------

class TestConstructionInvariants:
    def test_rejects_empty_delta_preview_ref(self):
        kwargs = _valid_preview_kwargs("cmd-1", "preview-1")
        kwargs["delta_preview_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="delta_preview_ref"):
            TinyVerticalSliceStateDeltaCandidatePreview(**kwargs)

    def test_rejects_empty_command_ref(self):
        kwargs = _valid_preview_kwargs("cmd-1", "preview-1")
        kwargs["command_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="command_ref"):
            TinyVerticalSliceStateDeltaCandidatePreview(**kwargs)

    def test_rejects_empty_world_ref(self):
        kwargs = _valid_preview_kwargs("cmd-1", "preview-1", world_ref="")
        with pytest.raises(TinyVerticalSliceError, match="world_ref"):
            TinyVerticalSliceStateDeltaCandidatePreview(**kwargs)

    def test_rejects_non_state_delta_envelope(self):
        kwargs = _valid_preview_kwargs("cmd-1", "preview-1", candidate_delta_envelopes=["not an envelope"])
        with pytest.raises(TinyVerticalSliceError, match="candidate_delta_envelopes"):
            TinyVerticalSliceStateDeltaCandidatePreview(**kwargs)

    def test_rejects_mismatched_candidate_delta_refs(self):
        kwargs = _valid_preview_kwargs("cmd-1", "preview-1", candidate_delta_refs=("wrong-ref",))
        with pytest.raises(TinyVerticalSliceError, match="candidate_delta_refs"):
            TinyVerticalSliceStateDeltaCandidatePreview(**kwargs)

    def test_rejects_mismatched_source_command_id(self):
        envelope = create_state_delta_envelope(
            delta_id="state-delta-candidate-cmd-1-lever",
            source_command_id="other-cmd",
            source_preview_id="preview-1",
            affected_record_ids=("astra:item:brass_threshold_lever",),
            change_type="record_update",
            payload={"applied": False},
            metadata={},
        )
        kwargs = _valid_preview_kwargs("cmd-1", "preview-1", candidate_delta_envelopes=[envelope])
        with pytest.raises(TinyVerticalSliceError, match="source_command_id"):
            TinyVerticalSliceStateDeltaCandidatePreview(**kwargs)

    @pytest.mark.parametrize("field", [
        "apply_authorized",
        "state_changed",
        "event_committed",
        "persistence_authorized",
        "replay_authorized",
    ])
    def test_rejects_true_authority_field(self, field):
        kwargs = _valid_preview_kwargs("cmd-1", "preview-1", **{field: True})
        with pytest.raises(TinyVerticalSliceError, match=field):
            TinyVerticalSliceStateDeltaCandidatePreview(**kwargs)

    def test_tuple_fields_normalize_to_tuples(self):
        kwargs = _valid_preview_kwargs(
            "cmd-1",
            "preview-1",
            candidate_delta_refs=list(_valid_delta_envelopes("cmd-1", "preview-1")[0].delta_id for _ in [0]),
            affected_visible_record_refs=["lever-1", "clock-1"],
            visible_change_kinds=["lever_state_candidate"],
            backend_only_ref_ids=["hidden-1"],
        )
        preview = TinyVerticalSliceStateDeltaCandidatePreview(**kwargs)
        assert isinstance(preview.candidate_delta_refs, tuple)
        assert isinstance(preview.affected_visible_record_refs, tuple)
        assert isinstance(preview.visible_change_kinds, tuple)
        assert isinstance(preview.backend_only_ref_ids, tuple)

    def test_metadata_deep_copied_and_frozen(self):
        kwargs = _valid_preview_kwargs("cmd-1", "preview-1")
        source = {"nested": {"k": "v"}}
        kwargs["metadata"] = source
        preview = TinyVerticalSliceStateDeltaCandidatePreview(**kwargs)
        source["nested"]["k"] = "changed"
        assert preview.metadata["nested"]["k"] == "v"
        assert isinstance(preview.metadata, MappingProxyType)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class TestBuilder:
    def test_default_inspect_produces_one_visibility_candidate(self, world, default_lifecycle, default_planning_preview, default_context_projection):
        preview = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world,
            lifecycle_result=default_lifecycle,
            planning_preview=default_planning_preview,
            context_projection=default_context_projection,
        )
        assert len(preview.candidate_delta_envelopes) == 1
        assert preview.candidate_delta_envelopes[0].change_type == "visibility_update"

    def test_pull_lever_produces_two_candidates(self, world):
        command = create_tiny_vertical_slice_command_intent(command_kind="pull_lever", command_ref="cmd-pull-1")
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        planning = build_tiny_vertical_slice_resource_consequence_planning_preview(state=world, lifecycle_result=lifecycle)
        projection = build_tiny_vertical_slice_context_packet_projection(state=world, lifecycle_result=lifecycle, planning_preview=planning)
        preview = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lifecycle, planning_preview=planning, context_projection=projection
        )
        assert len(preview.candidate_delta_envelopes) == 2
        change_types = {e.change_type for e in preview.candidate_delta_envelopes}
        assert change_types == {"record_update"}

    def test_brace_mechanism_produces_one_candidate(self, world):
        command = create_tiny_vertical_slice_command_intent(command_kind="brace_mechanism", command_ref="cmd-brace-1")
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        planning = build_tiny_vertical_slice_resource_consequence_planning_preview(state=world, lifecycle_result=lifecycle)
        projection = build_tiny_vertical_slice_context_packet_projection(state=world, lifecycle_result=lifecycle, planning_preview=planning)
        preview = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lifecycle, planning_preview=planning, context_projection=projection
        )
        assert len(preview.candidate_delta_envelopes) == 1
        assert preview.visible_change_kinds == ("lever_state_candidate",)

    def test_speak_to_npc_produces_one_candidate(self, world):
        command = create_tiny_vertical_slice_command_intent(
            command_kind="speak_to_npc", target_ref="npc-watchful-adept", command_ref="cmd-speak-1"
        )
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        planning = build_tiny_vertical_slice_resource_consequence_planning_preview(state=world, lifecycle_result=lifecycle)
        projection = build_tiny_vertical_slice_context_packet_projection(state=world, lifecycle_result=lifecycle, planning_preview=planning)
        preview = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lifecycle, planning_preview=planning, context_projection=projection
        )
        assert len(preview.candidate_delta_envelopes) == 1
        assert preview.candidate_delta_envelopes[0].change_type == "relationship_update"

    def test_blocked_lifecycle_produces_no_candidates(self, world):
        command = create_tiny_vertical_slice_command_intent(actor_ref="actor-unknown")
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        planning = build_tiny_vertical_slice_resource_consequence_planning_preview(state=world, lifecycle_result=lifecycle)
        projection = build_tiny_vertical_slice_context_packet_projection(state=world, lifecycle_result=lifecycle, planning_preview=planning)
        preview = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lifecycle, planning_preview=planning, context_projection=projection
        )
        assert preview.candidate_delta_envelopes == ()
        assert preview.candidate_delta_refs == ()
        assert preview.apply_authorized is False
        assert "blocked" in preview.visible_delta_summary.lower()

    def test_builder_rejects_non_world_state_input(self, default_lifecycle, default_planning_preview, default_context_projection):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceWorldState"):
            build_tiny_vertical_slice_state_delta_candidate_preview(
                state="not a world",
                lifecycle_result=default_lifecycle,
                planning_preview=default_planning_preview,
                context_projection=default_context_projection,
            )

    def test_builder_rejects_non_lifecycle_input(self, world, default_planning_preview, default_context_projection):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceCommandLifecycleResult"):
            build_tiny_vertical_slice_state_delta_candidate_preview(
                state=world,
                lifecycle_result="not a lifecycle",
                planning_preview=default_planning_preview,
                context_projection=default_context_projection,
            )

    def test_builder_rejects_non_planning_preview_input(self, world, default_lifecycle, default_context_projection):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceResourceConsequencePlanningPreview"):
            build_tiny_vertical_slice_state_delta_candidate_preview(
                state=world,
                lifecycle_result=default_lifecycle,
                planning_preview="not a preview",
                context_projection=default_context_projection,
            )

    def test_builder_rejects_non_context_projection_input(self, world, default_lifecycle, default_planning_preview):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceContextPacketProjection"):
            build_tiny_vertical_slice_state_delta_candidate_preview(
                state=world,
                lifecycle_result=default_lifecycle,
                planning_preview=default_planning_preview,
                context_projection="not a projection",
            )

    def test_builder_rejects_mismatched_resulting_state(self, world):
        other_world = create_tiny_vertical_slice_world_state()
        command = create_tiny_vertical_slice_command_intent()
        lifecycle = run_tiny_vertical_slice_command_lifecycle(state=other_world, command=command)
        planning = build_tiny_vertical_slice_resource_consequence_planning_preview(state=other_world, lifecycle_result=lifecycle)
        projection = build_tiny_vertical_slice_context_packet_projection(state=other_world, lifecycle_result=lifecycle, planning_preview=planning)
        with pytest.raises(TinyVerticalSliceError, match="resulting_state"):
            build_tiny_vertical_slice_state_delta_candidate_preview(
                state=world, lifecycle_result=lifecycle, planning_preview=planning, context_projection=projection
            )

    def test_builder_rejects_planning_preview_command_ref_mismatch(self, world, default_lifecycle, default_context_projection):
        other_command = create_tiny_vertical_slice_command_intent(command_ref="cmd-other")
        other_lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=other_command)
        other_planning = build_tiny_vertical_slice_resource_consequence_planning_preview(state=world, lifecycle_result=other_lifecycle)
        with pytest.raises(TinyVerticalSliceError, match="planning_preview.command_ref"):
            build_tiny_vertical_slice_state_delta_candidate_preview(
                state=world,
                lifecycle_result=default_lifecycle,
                planning_preview=other_planning,
                context_projection=default_context_projection,
            )

    def test_builder_rejects_context_projection_command_ref_mismatch(self, world, default_lifecycle, default_planning_preview):
        other_projection = _make_context_projection("cmd-other")
        with pytest.raises(TinyVerticalSliceError, match="context_projection.command_ref"):
            build_tiny_vertical_slice_state_delta_candidate_preview(
                state=world,
                lifecycle_result=default_lifecycle,
                planning_preview=default_planning_preview,
                context_projection=other_projection,
            )

    def test_builder_rejects_context_projection_world_ref_mismatch(self, world, default_lifecycle, default_planning_preview):
        other_projection = _make_context_projection(default_lifecycle.command.command_ref, world_ref="other-world")
        with pytest.raises(TinyVerticalSliceError, match="context_projection.world_ref"):
            build_tiny_vertical_slice_state_delta_candidate_preview(
                state=world,
                lifecycle_result=default_lifecycle,
                planning_preview=default_planning_preview,
                context_projection=other_projection,
            )

    def test_all_candidate_deltas_validate(self, default_delta_preview):
        for envelope in default_delta_preview.candidate_delta_envelopes:
            assert validate_state_delta_envelope(envelope) is True

    def test_candidate_delta_affected_record_ids_are_valid(self, default_delta_preview):
        for envelope in default_delta_preview.candidate_delta_envelopes:
            for rid in envelope.affected_record_ids:
                assert is_valid_record_id(rid)

    def test_candidate_delta_payloads_include_applied_false(self, default_delta_preview):
        for envelope in default_delta_preview.candidate_delta_envelopes:
            assert envelope.payload.get("applied") is False

    def test_no_state_mutation(self, world, default_lifecycle, default_planning_preview, default_context_projection):
        original_tick = world.hazard_clock.current_tick
        original_lever_state = world.lever.visible_state
        build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world,
            lifecycle_result=default_lifecycle,
            planning_preview=default_planning_preview,
            context_projection=default_context_projection,
        )
        assert world.hazard_clock.current_tick == original_tick
        assert world.lever.visible_state == original_lever_state

    def test_no_event_commitment(self, default_delta_preview):
        assert default_delta_preview.event_committed is False

    def test_no_event_ledger_entry_created(self, default_delta_preview):
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        text = json.dumps(serialized)
        assert "EventLedgerEntry" not in text

    def test_no_persistence_or_replay_authorization(self, default_delta_preview):
        assert default_delta_preview.persistence_authorized is False
        assert default_delta_preview.replay_authorized is False


# ---------------------------------------------------------------------------
# Visible serializer
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_rejects_non_preview_input(self):
        with pytest.raises(TinyVerticalSliceError):
            serialize_tiny_vertical_slice_state_delta_candidate_visible_preview("not a preview")

    def test_exact_top_level_key_order(self, default_delta_preview):
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        expected_keys = [
            "delta_preview_ref",
            "command_ref",
            "world_ref",
            "lifecycle_status",
            "commit_status",
            "planning_preview_ref",
            "context_projection_ref",
            "candidate_delta_refs",
            "affected_visible_record_refs",
            "visible_delta_summary",
            "visible_change_kinds",
            "apply_authorized",
            "state_changed",
            "event_committed",
            "persistence_authorized",
            "replay_authorized",
            "candidate_delta_envelopes",
            "metadata",
        ]
        assert list(serialized.keys()) == expected_keys

    def test_omits_backend_only_ref_ids(self, default_delta_preview):
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        assert "backend_only_ref_ids" not in serialized

    def test_omits_hidden_fact_ref(self, world, default_delta_preview):
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        text = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_ref not in text

    def test_omits_hidden_fact_label(self, world, default_delta_preview):
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        text = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_label not in text

    def test_omits_backend_only_description(self, world, default_delta_preview):
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        text = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in text

    def test_omits_reveal_condition(self, world, default_delta_preview):
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        text = json.dumps(serialized)
        assert world.hidden_fact.reveal_condition not in text

    def test_tuple_fields_serialize_as_lists(self, default_delta_preview):
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        assert isinstance(serialized["candidate_delta_refs"], list)
        assert isinstance(serialized["affected_visible_record_refs"], list)
        assert isinstance(serialized["visible_change_kinds"], list)

    def test_metadata_serializes_as_dict(self, world, default_lifecycle, default_planning_preview, default_context_projection):
        preview = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world,
            lifecycle_result=default_lifecycle,
            planning_preview=default_planning_preview,
            context_projection=default_context_projection,
            metadata={"k": "v"},
        )
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(preview)
        assert isinstance(serialized["metadata"], dict)
        assert not isinstance(serialized["metadata"], MappingProxyType)

    def test_top_level_authority_booleans_false(self, default_delta_preview):
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        assert serialized["apply_authorized"] is False
        assert serialized["state_changed"] is False
        assert serialized["event_committed"] is False
        assert serialized["persistence_authorized"] is False
        assert serialized["replay_authorized"] is False

    def test_each_delta_payload_has_applied_false(self, default_delta_preview):
        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        for delta in serialized["candidate_delta_envelopes"]:
            assert delta["payload"]["applied"] is False

    def test_no_event_type_or_sequence(self, default_delta_preview):
        def _has_key(obj, key):
            if isinstance(obj, dict):
                return key in obj or any(_has_key(v, key) for v in obj.values())
            if isinstance(obj, list):
                return any(_has_key(item, key) for item in obj)
            return False

        serialized = serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(default_delta_preview)
        assert not _has_key(serialized, "event_type")
        assert not _has_key(serialized, "sequence")


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

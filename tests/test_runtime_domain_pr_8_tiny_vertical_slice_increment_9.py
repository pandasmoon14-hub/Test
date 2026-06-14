"""PR-8 Increment 9 — tiny vertical slice post-commit narration packet projection tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    TinyVerticalSliceCommitApplicationResult,
    TinyVerticalSliceError,
    TinyVerticalSlicePostCommitNarrationPacketProjection,
    apply_tiny_vertical_slice_commit_application,
    build_tiny_vertical_slice_commit_dry_run_result,
    build_tiny_vertical_slice_context_packet_projection,
    build_tiny_vertical_slice_event_ledger_candidate_preview,
    build_tiny_vertical_slice_post_commit_narration_packet_projection,
    build_tiny_vertical_slice_resource_consequence_planning_preview,
    build_tiny_vertical_slice_state_delta_candidate_preview,
    create_tiny_vertical_slice_command_intent,
    create_tiny_vertical_slice_world_state,
    run_tiny_vertical_slice_command_lifecycle,
    serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible,
    SingleEventNarrationPacket,
    create_single_event_narration_packet,
    validate_single_event_narration_packet,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def world():
    return create_tiny_vertical_slice_world_state()


def _make_full_chain(world, command_kind, target_ref=None, command_ref=None):
    kwargs = {"command_kind": command_kind}
    if target_ref:
        kwargs["target_ref"] = target_ref
    if command_ref:
        kwargs["command_ref"] = command_ref
    if command_kind == "speak_to_npc":
        kwargs.setdefault("target_ref", "npc-watchful-adept")
        kwargs.setdefault("declared_intent", "Speak to the watchful adept.")
    command = create_tiny_vertical_slice_command_intent(**kwargs)
    lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
    planning = build_tiny_vertical_slice_resource_consequence_planning_preview(
        state=world, lifecycle_result=lifecycle,
    )
    projection = build_tiny_vertical_slice_context_packet_projection(
        state=world, lifecycle_result=lifecycle, planning_preview=planning,
    )
    delta = build_tiny_vertical_slice_state_delta_candidate_preview(
        state=world, lifecycle_result=lifecycle,
        planning_preview=planning, context_projection=projection,
    )
    event = build_tiny_vertical_slice_event_ledger_candidate_preview(
        state=world, lifecycle_result=lifecycle,
        planning_preview=planning, context_projection=projection,
        delta_preview=delta,
    )
    return lifecycle, planning, projection, delta, event


def _make_dry_run(world, command_kind, command_ref=None):
    lc, pl, pj, dp, ep = _make_full_chain(world, command_kind, command_ref=command_ref)
    return build_tiny_vertical_slice_commit_dry_run_result(
        state=world, lifecycle_result=lc,
        planning_preview=pl, context_projection=pj,
        delta_preview=dp, event_preview=ep,
    )


def _make_commit_application(world, command_kind, command_ref=None):
    dr = _make_dry_run(world, command_kind, command_ref=command_ref)
    return apply_tiny_vertical_slice_commit_application(state=world, dry_run_result=dr)


def _make_projection(world, command_kind, command_ref=None):
    commit = _make_commit_application(world, command_kind, command_ref=command_ref)
    return build_tiny_vertical_slice_post_commit_narration_packet_projection(
        commit_result=commit,
    )


def _make_blocked_commit(world):
    command = create_tiny_vertical_slice_command_intent(
        actor_ref="actor-nonexistent",
        command_kind="inspect_lever",
        target_ref="lever-brass-threshold",
    )
    lifecycle = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
    planning = build_tiny_vertical_slice_resource_consequence_planning_preview(
        state=world, lifecycle_result=lifecycle,
    )
    projection = build_tiny_vertical_slice_context_packet_projection(
        state=world, lifecycle_result=lifecycle, planning_preview=planning,
    )
    delta = build_tiny_vertical_slice_state_delta_candidate_preview(
        state=world, lifecycle_result=lifecycle,
        planning_preview=planning, context_projection=projection,
    )
    event = build_tiny_vertical_slice_event_ledger_candidate_preview(
        state=world, lifecycle_result=lifecycle,
        planning_preview=planning, context_projection=projection,
        delta_preview=delta,
    )
    dr = build_tiny_vertical_slice_commit_dry_run_result(
        state=world, lifecycle_result=lifecycle,
        planning_preview=planning, context_projection=projection,
        delta_preview=delta, event_preview=event,
    )
    return apply_tiny_vertical_slice_commit_application(state=world, dry_run_result=dr)


@pytest.fixture()
def default_projection(world):
    return _make_projection(world, "inspect_lever")


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment9_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSlicePostCommitNarrationPacketProjection",
            "build_tiny_vertical_slice_post_commit_narration_packet_projection",
            "serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible",
        ]
        for sym in expected:
            assert hasattr(domain, sym), f"Missing export: {sym}"
            assert sym in domain.__all__, f"Missing from __all__: {sym}"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

class TestDataclass:
    def _make_packet(self, event_ref="ev-1", event_kind="command_event",
                     visible_fact_refs=("fact-1",), actor_refs=("actor-1",),
                     target_refs=("target-1",), sensory_cues=("cue-1",),
                     forbidden_claims=("claim-1",)):
        return create_single_event_narration_packet(
            event_ref=event_ref,
            event_kind=event_kind,
            visible_fact_refs=visible_fact_refs,
            actor_refs=actor_refs,
            target_refs=target_refs,
            sensory_cues=sensory_cues,
            forbidden_claims=forbidden_claims,
            hidden_information_excluded=True,
        )

    def _make_valid_kwargs(self, world):
        pkt = self._make_packet()
        return {
            "projection_ref": "proj-1",
            "command_ref": "cmd-1",
            "world_ref": world.world_ref,
            "commit_ref": "commit-1",
            "committed_event_ref": "ev-1",
            "committed_event_type": "command_event",
            "packet": pkt,
            "visible_fact_refs": ("fact-1",),
            "actor_refs": ("actor-1",),
            "target_refs": ("target-1",),
            "sensory_cues": ("cue-1",),
            "forbidden_claims": ("claim-1",),
            "backend_only_ref_ids": (),
            "hidden_information_excluded": True,
            "packet_validated": True,
            "model_called": False,
            "narration_generated": False,
            "state_mutated": False,
            "state_delta_applied": False,
            "event_committed": False,
            "event_appended": False,
            "persistence_authorized": False,
            "replay_authorized": False,
        }

    def test_frozen(self, world):
        proj = _make_projection(world, "inspect_lever")
        assert isinstance(proj, TinyVerticalSlicePostCommitNarrationPacketProjection)
        with pytest.raises(AttributeError):
            proj.projection_ref = "x"

    def test_rejects_empty_projection_ref(self, world):
        kw = self._make_valid_kwargs(world)
        kw["projection_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="projection_ref"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_empty_command_ref(self, world):
        kw = self._make_valid_kwargs(world)
        kw["command_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="command_ref"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_empty_world_ref(self, world):
        kw = self._make_valid_kwargs(world)
        kw["world_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="world_ref"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_empty_commit_ref(self, world):
        kw = self._make_valid_kwargs(world)
        kw["commit_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="commit_ref"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_empty_committed_event_ref(self, world):
        kw = self._make_valid_kwargs(world)
        kw["committed_event_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="committed_event_ref"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_empty_committed_event_type(self, world):
        kw = self._make_valid_kwargs(world)
        kw["committed_event_type"] = ""
        with pytest.raises(TinyVerticalSliceError, match="committed_event_type"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_non_single_event_narration_packet(self, world):
        kw = self._make_valid_kwargs(world)
        kw["packet"] = "not-a-packet"
        with pytest.raises(TinyVerticalSliceError, match="SingleEventNarrationPacket"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_packet_event_ref_mismatch(self, world):
        kw = self._make_valid_kwargs(world)
        kw["committed_event_ref"] = "different-ref"
        kw["packet"] = self._make_packet(event_ref="ev-1")
        with pytest.raises(TinyVerticalSliceError, match="event_ref"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_packet_event_kind_mismatch(self, world):
        kw = self._make_valid_kwargs(world)
        kw["committed_event_type"] = "different_kind"
        kw["packet"] = self._make_packet(event_kind="command_event")
        with pytest.raises(TinyVerticalSliceError, match="event_kind"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_packet_visible_fact_refs_mismatch(self, world):
        kw = self._make_valid_kwargs(world)
        kw["visible_fact_refs"] = ("different-fact",)
        with pytest.raises(TinyVerticalSliceError, match="visible_fact_refs"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_packet_actor_refs_mismatch(self, world):
        kw = self._make_valid_kwargs(world)
        kw["actor_refs"] = ("different-actor",)
        with pytest.raises(TinyVerticalSliceError, match="actor_refs"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_packet_target_refs_mismatch(self, world):
        kw = self._make_valid_kwargs(world)
        kw["target_refs"] = ("different-target",)
        with pytest.raises(TinyVerticalSliceError, match="target_refs"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_packet_sensory_cues_mismatch(self, world):
        kw = self._make_valid_kwargs(world)
        kw["sensory_cues"] = ("different-cue",)
        with pytest.raises(TinyVerticalSliceError, match="sensory_cues"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_packet_forbidden_claims_mismatch(self, world):
        kw = self._make_valid_kwargs(world)
        kw["forbidden_claims"] = ("different-claim",)
        with pytest.raises(TinyVerticalSliceError, match="forbidden_claims"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_empty_visible_fact_refs(self, world):
        pkt = self._make_packet(visible_fact_refs=("f",))
        kw = self._make_valid_kwargs(world)
        kw["visible_fact_refs"] = ()
        kw["packet"] = pkt
        with pytest.raises((TinyVerticalSliceError,), match="visible_fact_refs"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_hidden_information_excluded_false(self, world):
        kw = self._make_valid_kwargs(world)
        kw["hidden_information_excluded"] = False
        with pytest.raises(TinyVerticalSliceError, match="hidden_information_excluded"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_packet_validated_false(self, world):
        kw = self._make_valid_kwargs(world)
        kw["packet_validated"] = False
        with pytest.raises(TinyVerticalSliceError, match="packet_validated"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_model_called_true(self, world):
        kw = self._make_valid_kwargs(world)
        kw["model_called"] = True
        with pytest.raises(TinyVerticalSliceError, match="model_called"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_narration_generated_true(self, world):
        kw = self._make_valid_kwargs(world)
        kw["narration_generated"] = True
        with pytest.raises(TinyVerticalSliceError, match="narration_generated"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_state_mutated_true(self, world):
        kw = self._make_valid_kwargs(world)
        kw["state_mutated"] = True
        with pytest.raises(TinyVerticalSliceError, match="state_mutated"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_state_delta_applied_true(self, world):
        kw = self._make_valid_kwargs(world)
        kw["state_delta_applied"] = True
        with pytest.raises(TinyVerticalSliceError, match="state_delta_applied"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_event_committed_true(self, world):
        kw = self._make_valid_kwargs(world)
        kw["event_committed"] = True
        with pytest.raises(TinyVerticalSliceError, match="event_committed"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_event_appended_true(self, world):
        kw = self._make_valid_kwargs(world)
        kw["event_appended"] = True
        with pytest.raises(TinyVerticalSliceError, match="event_appended"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_persistence_authorized_true(self, world):
        kw = self._make_valid_kwargs(world)
        kw["persistence_authorized"] = True
        with pytest.raises(TinyVerticalSliceError, match="persistence_authorized"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_rejects_replay_authorized_true(self, world):
        kw = self._make_valid_kwargs(world)
        kw["replay_authorized"] = True
        with pytest.raises(TinyVerticalSliceError, match="replay_authorized"):
            TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)

    def test_tuple_list_fields_normalize_to_tuples(self, world):
        pkt = self._make_packet()
        kw = self._make_valid_kwargs(world)
        kw["visible_fact_refs"] = ["fact-1"]
        kw["actor_refs"] = ["actor-1"]
        kw["target_refs"] = ["target-1"]
        kw["sensory_cues"] = ["cue-1"]
        kw["forbidden_claims"] = ["claim-1"]
        kw["backend_only_ref_ids"] = []
        result = TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)
        assert isinstance(result.visible_fact_refs, tuple)
        assert isinstance(result.actor_refs, tuple)
        assert isinstance(result.target_refs, tuple)
        assert isinstance(result.sensory_cues, tuple)
        assert isinstance(result.forbidden_claims, tuple)
        assert isinstance(result.backend_only_ref_ids, tuple)

    def test_metadata_deep_copied_and_frozen(self, world):
        source = {"key": "value"}
        kw = self._make_valid_kwargs(world)
        kw["metadata"] = source
        result = TinyVerticalSlicePostCommitNarrationPacketProjection(**kw)
        assert isinstance(result.metadata, MappingProxyType)
        source["key"] = "changed"
        assert result.metadata["key"] == "value"


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class TestBuilder:
    def test_inspect_lever_builds_valid_projection(self, world):
        proj = _make_projection(world, "inspect_lever")
        assert isinstance(proj, TinyVerticalSlicePostCommitNarrationPacketProjection)
        assert proj.committed_event_ref is not None
        assert proj.committed_event_type is not None
        assert proj.hidden_information_excluded is True
        assert proj.packet_validated is True
        assert proj.model_called is False
        assert proj.narration_generated is False

    def test_pull_lever_builds_valid_projection(self, world):
        proj = _make_projection(world, "pull_lever")
        assert isinstance(proj, TinyVerticalSlicePostCommitNarrationPacketProjection)
        assert "The brass lever rests in a pulled position." in proj.sensory_cues

    def test_brace_mechanism_builds_valid_projection(self, world):
        proj = _make_projection(world, "brace_mechanism")
        assert isinstance(proj, TinyVerticalSlicePostCommitNarrationPacketProjection)
        assert "The brass lever is braced." in proj.sensory_cues

    def test_speak_to_npc_builds_valid_projection(self, world):
        proj = _make_projection(world, "speak_to_npc")
        assert isinstance(proj, TinyVerticalSlicePostCommitNarrationPacketProjection)
        assert "The watchful adept is engaged." in proj.sensory_cues

    def test_blocked_commit_result_rejected(self, world):
        blocked = _make_blocked_commit(world)
        assert blocked.commit_blocked is True
        with pytest.raises(TinyVerticalSliceError, match="blocked"):
            build_tiny_vertical_slice_post_commit_narration_packet_projection(
                commit_result=blocked,
            )

    def test_commit_result_event_committed_false_rejected(self, world):
        with pytest.raises(TinyVerticalSliceError):
            build_tiny_vertical_slice_post_commit_narration_packet_projection(
                commit_result="not-a-commit-result",
            )

    def test_missing_committed_event_ref_rejected(self, world):
        blocked = _make_blocked_commit(world)
        assert blocked.committed_event_ref is None
        with pytest.raises(TinyVerticalSliceError):
            build_tiny_vertical_slice_post_commit_narration_packet_projection(
                commit_result=blocked,
            )

    def test_missing_committed_event_type_rejected(self, world):
        blocked = _make_blocked_commit(world)
        assert blocked.committed_event_type is None
        with pytest.raises(TinyVerticalSliceError):
            build_tiny_vertical_slice_post_commit_narration_packet_projection(
                commit_result=blocked,
            )

    def test_nested_packet_validates(self, world):
        proj = _make_projection(world, "inspect_lever")
        assert validate_single_event_narration_packet(proj.packet)

    def test_nested_packet_kind(self, world):
        proj = _make_projection(world, "pull_lever")
        assert proj.packet.packet_kind == "single_event_narration"

    def test_nested_packet_has_non_empty_visible_fact_refs(self, world):
        proj = _make_projection(world, "brace_mechanism")
        assert len(proj.packet.visible_fact_refs) > 0

    def test_nested_packet_has_non_empty_non_authority_seal(self, world):
        proj = _make_projection(world, "speak_to_npc")
        assert len(proj.packet.non_authority_seal) > 0

    def test_nested_packet_hidden_information_excluded(self, world):
        proj = _make_projection(world, "inspect_lever")
        assert proj.packet.hidden_information_excluded is True

    def test_projection_does_not_mutate_state(self, world):
        original_lever = world.lever.visible_state
        original_clock = world.hazard_clock.current_tick
        original_npc = world.npc.visible_disposition
        _make_projection(world, "pull_lever")
        assert world.lever.visible_state == original_lever
        assert world.hazard_clock.current_tick == original_clock
        assert world.npc.visible_disposition == original_npc

    def test_projection_does_not_apply_deltas(self, world):
        proj = _make_projection(world, "inspect_lever")
        assert proj.state_delta_applied is False

    def test_projection_does_not_commit_append_event(self, world):
        proj = _make_projection(world, "inspect_lever")
        assert proj.event_committed is False
        assert proj.event_appended is False

    def test_projection_does_not_persist_replay(self, world):
        proj = _make_projection(world, "inspect_lever")
        assert proj.persistence_authorized is False
        assert proj.replay_authorized is False

    def test_projection_does_not_call_model(self, world):
        proj = _make_projection(world, "inspect_lever")
        assert proj.model_called is False

    def test_projection_does_not_generate_narration(self, world):
        proj = _make_projection(world, "inspect_lever")
        assert proj.narration_generated is False


# ---------------------------------------------------------------------------
# Visible serializer
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_rejects_non_projection_input(self):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSlicePostCommitNarrationPacketProjection"):
            serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible("not-a-projection")

    def test_exact_top_level_key_order(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        expected_keys = [
            "projection_ref",
            "command_ref",
            "world_ref",
            "commit_ref",
            "committed_event_ref",
            "committed_event_type",
            "visible_fact_refs",
            "actor_refs",
            "target_refs",
            "sensory_cues",
            "forbidden_claims",
            "hidden_information_excluded",
            "packet_validated",
            "model_called",
            "narration_generated",
            "state_mutated",
            "state_delta_applied",
            "event_committed",
            "event_appended",
            "persistence_authorized",
            "replay_authorized",
            "packet",
            "metadata",
        ]
        assert list(serialized.keys()) == expected_keys

    def test_serializes_nested_packet_as_dict(self, world):
        proj = _make_projection(world, "pull_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert isinstance(serialized["packet"], dict)
        assert "packet_kind" in serialized["packet"]

    def test_omits_backend_only_ref_ids(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert "backend_only_ref_ids" not in serialized

    def test_omits_hidden_fact_ref(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_ref not in dumped

    def test_omits_hidden_fact_label(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_label not in dumped

    def test_omits_backend_only_description(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in dumped

    def test_omits_reveal_condition(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.reveal_condition not in dumped

    def test_does_not_contain_hidden_fact_description_anywhere(self, world):
        for kind in ("inspect_lever", "brace_mechanism", "pull_lever", "speak_to_npc"):
            proj = _make_projection(world, kind)
            serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
            dumped = json.dumps(serialized)
            assert world.hidden_fact.backend_only_description not in dumped

    def test_does_not_contain_backend_only_refs_anywhere(self, world):
        for kind in ("inspect_lever", "brace_mechanism", "pull_lever"):
            proj = _make_projection(world, kind)
            serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
            dumped = json.dumps(serialized)
            for ref in proj.backend_only_ref_ids:
                assert ref not in dumped

    def test_does_not_contain_generated_narration_prose(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        dumped = json.dumps(serialized)
        assert "generated_narration" not in dumped
        assert "narration_prose" not in dumped

    def test_visible_fact_refs_serialize_as_list(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert isinstance(serialized["visible_fact_refs"], list)

    def test_actor_refs_serialize_as_list(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert isinstance(serialized["actor_refs"], list)

    def test_target_refs_serialize_as_list(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert isinstance(serialized["target_refs"], list)

    def test_sensory_cues_serialize_as_list(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert isinstance(serialized["sensory_cues"], list)

    def test_forbidden_claims_serialize_as_list(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert isinstance(serialized["forbidden_claims"], list)

    def test_metadata_serializes_as_dict(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert isinstance(serialized["metadata"], dict)

    def test_serializer_shows_model_called_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert serialized["model_called"] is False

    def test_serializer_shows_narration_generated_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert serialized["narration_generated"] is False

    def test_serializer_shows_state_mutated_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert serialized["state_mutated"] is False

    def test_serializer_shows_state_delta_applied_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert serialized["state_delta_applied"] is False

    def test_serializer_shows_event_committed_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert serialized["event_committed"] is False

    def test_serializer_shows_event_appended_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert serialized["event_appended"] is False

    def test_serializer_shows_persistence_authorized_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert serialized["persistence_authorized"] is False

    def test_serializer_shows_replay_authorized_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        assert serialized["replay_authorized"] is False

    def test_nested_packet_metadata_includes_packet_projection_only(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        pkt_meta = serialized["packet"]["metadata"]
        assert pkt_meta["packet_projection_only"] is True

    def test_nested_packet_metadata_includes_model_called_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        pkt_meta = serialized["packet"]["metadata"]
        assert pkt_meta["model_called"] is False

    def test_nested_packet_metadata_includes_narration_generated_false(self, world):
        proj = _make_projection(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(proj)
        pkt_meta = serialized["packet"]["metadata"]
        assert pkt_meta["narration_generated"] is False


# ---------------------------------------------------------------------------
# Source scan
# ---------------------------------------------------------------------------

class TestSourceScan:
    @pytest.fixture(autouse=True)
    def _load_source(self):
        src = Path(__file__).resolve().parent.parent / "src" / "astra_runtime" / "domain" / "tiny_vertical_slice.py"
        self.source_text = src.read_text(encoding="utf-8")

    @pytest.mark.parametrize("forbidden", [
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
        "persist_state",
        "replay_event",
        "state_store.get",
        "event_ledger.get",
        "open(",
        ".read_text(",
        ".write_text(",
    ])
    def test_production_module_does_not_contain_forbidden(self, forbidden):
        assert forbidden not in self.source_text, f"Production module must not contain '{forbidden}'"

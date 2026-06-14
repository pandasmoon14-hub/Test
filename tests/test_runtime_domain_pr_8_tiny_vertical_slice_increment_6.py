"""PR-8 Increment 6 — tiny vertical slice event ledger candidate preview tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    TinyVerticalSliceContextPacketProjection,
    TinyVerticalSliceError,
    TinyVerticalSliceEventLedgerCandidatePreview,
    TinyVerticalSliceResourceConsequencePlanningPreview,
    TinyVerticalSliceStateDeltaCandidatePreview,
    build_tiny_vertical_slice_context_packet_projection,
    build_tiny_vertical_slice_event_ledger_candidate_preview,
    build_tiny_vertical_slice_resource_consequence_planning_preview,
    build_tiny_vertical_slice_state_delta_candidate_preview,
    create_tiny_vertical_slice_command_intent,
    create_tiny_vertical_slice_world_state,
    run_tiny_vertical_slice_command_lifecycle,
    serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview,
)
from astra_runtime.kernel.event_ledger import (
    EventLedgerEntry,
    create_event_ledger_entry,
    validate_event_ledger_entry,
)
from astra_runtime.kernel.record_identity import build_record_id


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
    return lifecycle, planning, projection, delta


@pytest.fixture()
def default_lifecycle(world):
    command = create_tiny_vertical_slice_command_intent()
    return run_tiny_vertical_slice_command_lifecycle(state=world, command=command)


@pytest.fixture()
def default_planning_preview(world, default_lifecycle):
    return build_tiny_vertical_slice_resource_consequence_planning_preview(
        state=world, lifecycle_result=default_lifecycle,
    )


@pytest.fixture()
def default_context_projection(world, default_lifecycle, default_planning_preview):
    return build_tiny_vertical_slice_context_packet_projection(
        state=world, lifecycle_result=default_lifecycle,
        planning_preview=default_planning_preview,
    )


@pytest.fixture()
def default_delta_preview(world, default_lifecycle, default_planning_preview, default_context_projection):
    return build_tiny_vertical_slice_state_delta_candidate_preview(
        state=world, lifecycle_result=default_lifecycle,
        planning_preview=default_planning_preview,
        context_projection=default_context_projection,
    )


@pytest.fixture()
def default_event_preview(world, default_lifecycle, default_planning_preview, default_context_projection, default_delta_preview):
    return build_tiny_vertical_slice_event_ledger_candidate_preview(
        state=world,
        lifecycle_result=default_lifecycle,
        planning_preview=default_planning_preview,
        context_projection=default_context_projection,
        delta_preview=default_delta_preview,
    )


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment6_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSliceEventLedgerCandidatePreview",
            "build_tiny_vertical_slice_event_ledger_candidate_preview",
            "serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview",
        ]
        for sym in expected:
            assert hasattr(domain, sym), f"Missing export: {sym}"
            assert sym in domain.__all__, f"Missing from __all__: {sym}"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

class TestDataclass:
    def test_frozen(self):
        p = TinyVerticalSliceEventLedgerCandidatePreview(
            event_preview_ref="ep",
            command_ref="cmd",
            world_ref="w",
            lifecycle_status="blocked",
            commit_status="blocked",
            planning_preview_ref="pp",
            context_projection_ref="cp",
            delta_preview_ref="dp",
            candidate_event_entry=None,
            candidate_event_ref=None,
            candidate_event_type=None,
            candidate_state_delta_refs=(),
            actor_record_ids=(),
            target_record_ids=(),
            visible_event_summary="blocked summary",
            backend_only_ref_ids=(),
            event_commit_authorized=False,
            event_committed=False,
            state_changed=False,
            persistence_authorized=False,
            replay_authorized=False,
            narration_packet_authorized=False,
            model_called=False,
            narration_generated=False,
        )
        with pytest.raises(AttributeError):
            p.event_preview_ref = "changed"

    def test_rejects_empty_event_preview_ref(self):
        with pytest.raises(TinyVerticalSliceError, match="event_preview_ref"):
            TinyVerticalSliceEventLedgerCandidatePreview(
                event_preview_ref="",
                command_ref="cmd",
                world_ref="w",
                lifecycle_status="blocked",
                commit_status="blocked",
                planning_preview_ref="pp",
                context_projection_ref="cp",
                delta_preview_ref="dp",
                candidate_event_entry=None,
                candidate_event_ref=None,
                candidate_event_type=None,
                candidate_state_delta_refs=(),
                actor_record_ids=(),
                target_record_ids=(),
                visible_event_summary="blocked",
                backend_only_ref_ids=(),
                event_commit_authorized=False,
                event_committed=False,
                state_changed=False,
                persistence_authorized=False,
                replay_authorized=False,
                narration_packet_authorized=False,
                model_called=False,
                narration_generated=False,
            )

    def test_rejects_empty_command_ref(self):
        with pytest.raises(TinyVerticalSliceError, match="command_ref"):
            TinyVerticalSliceEventLedgerCandidatePreview(
                event_preview_ref="x",
                command_ref="",
                world_ref="w",
                lifecycle_status="blocked",
                commit_status="blocked",
                planning_preview_ref="p",
                context_projection_ref="c",
                delta_preview_ref="d",
                candidate_event_entry=None,
                candidate_event_ref=None,
                candidate_event_type=None,
                candidate_state_delta_refs=(),
                actor_record_ids=(),
                target_record_ids=(),
                visible_event_summary="blocked",
                backend_only_ref_ids=(),
                event_commit_authorized=False,
                event_committed=False,
                state_changed=False,
                persistence_authorized=False,
                replay_authorized=False,
                narration_packet_authorized=False,
                model_called=False,
                narration_generated=False,
            )

    def test_rejects_empty_world_ref(self):
        with pytest.raises(TinyVerticalSliceError, match="world_ref"):
            TinyVerticalSliceEventLedgerCandidatePreview(
                event_preview_ref="x",
                command_ref="c",
                world_ref="",
                lifecycle_status="blocked",
                commit_status="blocked",
                planning_preview_ref="p",
                context_projection_ref="c2",
                delta_preview_ref="d",
                candidate_event_entry=None,
                candidate_event_ref=None,
                candidate_event_type=None,
                candidate_state_delta_refs=(),
                actor_record_ids=(),
                target_record_ids=(),
                visible_event_summary="blocked",
                backend_only_ref_ids=(),
                event_commit_authorized=False,
                event_committed=False,
                state_changed=False,
                persistence_authorized=False,
                replay_authorized=False,
                narration_packet_authorized=False,
                model_called=False,
                narration_generated=False,
            )

    def test_accepts_none_entry_when_fields_also_none(self):
        p = TinyVerticalSliceEventLedgerCandidatePreview(
            event_preview_ref="ep",
            command_ref="cmd",
            world_ref="w",
            lifecycle_status="blocked",
            commit_status="blocked",
            planning_preview_ref="pp",
            context_projection_ref="cp",
            delta_preview_ref="dp",
            candidate_event_entry=None,
            candidate_event_ref=None,
            candidate_event_type=None,
            candidate_state_delta_refs=(),
            actor_record_ids=(),
            target_record_ids=(),
            visible_event_summary="blocked summary",
            backend_only_ref_ids=(),
            event_commit_authorized=False,
            event_committed=False,
            state_changed=False,
            persistence_authorized=False,
            replay_authorized=False,
            narration_packet_authorized=False,
            model_called=False,
            narration_generated=False,
        )
        assert p.candidate_event_entry is None

    def test_rejects_non_event_ledger_entry(self):
        with pytest.raises(TinyVerticalSliceError, match="EventLedgerEntry"):
            TinyVerticalSliceEventLedgerCandidatePreview(
                event_preview_ref="ep",
                command_ref="cmd",
                world_ref="w",
                lifecycle_status="blocked",
                commit_status="blocked",
                planning_preview_ref="pp",
                context_projection_ref="cp",
                delta_preview_ref="dp",
                candidate_event_entry="not-an-entry",
                candidate_event_ref="x",
                candidate_event_type="command_event",
                candidate_state_delta_refs=(),
                actor_record_ids=(),
                target_record_ids=(),
                visible_event_summary="summary",
                backend_only_ref_ids=(),
                event_commit_authorized=False,
                event_committed=False,
                state_changed=False,
                persistence_authorized=False,
                replay_authorized=False,
                narration_packet_authorized=False,
                model_called=False,
                narration_generated=False,
            )

    def test_rejects_mismatched_candidate_event_ref(self):
        entry = create_event_ledger_entry(
            event_id="evt-1", event_type="command_event", sequence=0,
            source_command_id="cmd", source_preview_id="ep",
        )
        with pytest.raises(TinyVerticalSliceError, match="candidate_event_ref"):
            TinyVerticalSliceEventLedgerCandidatePreview(
                event_preview_ref="ep",
                command_ref="cmd",
                world_ref="w",
                lifecycle_status="validated_preview",
                commit_status="not_requested",
                planning_preview_ref="pp",
                context_projection_ref="cp",
                delta_preview_ref="dp",
                candidate_event_entry=entry,
                candidate_event_ref="wrong-ref",
                candidate_event_type="command_event",
                candidate_state_delta_refs=(),
                actor_record_ids=(),
                target_record_ids=(),
                visible_event_summary="summary",
                backend_only_ref_ids=(),
                event_commit_authorized=False,
                event_committed=False,
                state_changed=False,
                persistence_authorized=False,
                replay_authorized=False,
                narration_packet_authorized=False,
                model_called=False,
                narration_generated=False,
            )

    def test_rejects_mismatched_candidate_event_type(self):
        entry = create_event_ledger_entry(
            event_id="evt-1", event_type="command_event", sequence=0,
            source_command_id="cmd", source_preview_id="ep",
        )
        with pytest.raises(TinyVerticalSliceError, match="candidate_event_type"):
            TinyVerticalSliceEventLedgerCandidatePreview(
                event_preview_ref="ep",
                command_ref="cmd",
                world_ref="w",
                lifecycle_status="validated_preview",
                commit_status="not_requested",
                planning_preview_ref="pp",
                context_projection_ref="cp",
                delta_preview_ref="dp",
                candidate_event_entry=entry,
                candidate_event_ref="evt-1",
                candidate_event_type="wrong_type",
                candidate_state_delta_refs=(),
                actor_record_ids=(),
                target_record_ids=(),
                visible_event_summary="summary",
                backend_only_ref_ids=(),
                event_commit_authorized=False,
                event_committed=False,
                state_changed=False,
                persistence_authorized=False,
                replay_authorized=False,
                narration_packet_authorized=False,
                model_called=False,
                narration_generated=False,
            )

    def test_rejects_mismatched_candidate_state_delta_refs(self):
        entry = create_event_ledger_entry(
            event_id="evt-1", event_type="command_event", sequence=0,
            source_command_id="cmd", source_preview_id="ep",
            state_delta_ids=("delta-1",),
        )
        with pytest.raises(TinyVerticalSliceError, match="candidate_state_delta_refs"):
            TinyVerticalSliceEventLedgerCandidatePreview(
                event_preview_ref="ep",
                command_ref="cmd",
                world_ref="w",
                lifecycle_status="validated_preview",
                commit_status="not_requested",
                planning_preview_ref="pp",
                context_projection_ref="cp",
                delta_preview_ref="dp",
                candidate_event_entry=entry,
                candidate_event_ref="evt-1",
                candidate_event_type="command_event",
                candidate_state_delta_refs=("wrong-delta",),
                actor_record_ids=(),
                target_record_ids=(),
                visible_event_summary="summary",
                backend_only_ref_ids=(),
                event_commit_authorized=False,
                event_committed=False,
                state_changed=False,
                persistence_authorized=False,
                replay_authorized=False,
                narration_packet_authorized=False,
                model_called=False,
                narration_generated=False,
            )

    def test_rejects_entry_with_mismatched_source_command_id(self):
        entry = create_event_ledger_entry(
            event_id="evt-1", event_type="command_event", sequence=0,
            source_command_id="other-cmd", source_preview_id="ep",
        )
        with pytest.raises(TinyVerticalSliceError, match="source_command_id"):
            TinyVerticalSliceEventLedgerCandidatePreview(
                event_preview_ref="ep",
                command_ref="cmd",
                world_ref="w",
                lifecycle_status="validated_preview",
                commit_status="not_requested",
                planning_preview_ref="pp",
                context_projection_ref="cp",
                delta_preview_ref="dp",
                candidate_event_entry=entry,
                candidate_event_ref="evt-1",
                candidate_event_type="command_event",
                candidate_state_delta_refs=(),
                actor_record_ids=(),
                target_record_ids=(),
                visible_event_summary="summary",
                backend_only_ref_ids=(),
                event_commit_authorized=False,
                event_committed=False,
                state_changed=False,
                persistence_authorized=False,
                replay_authorized=False,
                narration_packet_authorized=False,
                model_called=False,
                narration_generated=False,
            )

    def test_rejects_entry_with_mismatched_source_preview_id(self):
        entry = create_event_ledger_entry(
            event_id="evt-1", event_type="command_event", sequence=0,
            source_command_id="cmd", source_preview_id="other-ep",
        )
        with pytest.raises(TinyVerticalSliceError, match="source_preview_id"):
            TinyVerticalSliceEventLedgerCandidatePreview(
                event_preview_ref="ep",
                command_ref="cmd",
                world_ref="w",
                lifecycle_status="validated_preview",
                commit_status="not_requested",
                planning_preview_ref="pp",
                context_projection_ref="cp",
                delta_preview_ref="dp",
                candidate_event_entry=entry,
                candidate_event_ref="evt-1",
                candidate_event_type="command_event",
                candidate_state_delta_refs=(),
                actor_record_ids=(),
                target_record_ids=(),
                visible_event_summary="summary",
                backend_only_ref_ids=(),
                event_commit_authorized=False,
                event_committed=False,
                state_changed=False,
                persistence_authorized=False,
                replay_authorized=False,
                narration_packet_authorized=False,
                model_called=False,
                narration_generated=False,
            )

    @pytest.mark.parametrize("field_name", [
        "event_commit_authorized",
        "event_committed",
        "state_changed",
        "persistence_authorized",
        "replay_authorized",
        "narration_packet_authorized",
        "model_called",
        "narration_generated",
    ])
    def test_rejects_true_authority_booleans(self, field_name):
        kwargs = dict(
            event_preview_ref="ep",
            command_ref="cmd",
            world_ref="w",
            lifecycle_status="blocked",
            commit_status="blocked",
            planning_preview_ref="pp",
            context_projection_ref="cp",
            delta_preview_ref="dp",
            candidate_event_entry=None,
            candidate_event_ref=None,
            candidate_event_type=None,
            candidate_state_delta_refs=(),
            actor_record_ids=(),
            target_record_ids=(),
            visible_event_summary="blocked",
            backend_only_ref_ids=(),
            event_commit_authorized=False,
            event_committed=False,
            state_changed=False,
            persistence_authorized=False,
            replay_authorized=False,
            narration_packet_authorized=False,
            model_called=False,
            narration_generated=False,
        )
        kwargs[field_name] = True
        with pytest.raises(TinyVerticalSliceError, match=field_name):
            TinyVerticalSliceEventLedgerCandidatePreview(**kwargs)

    def test_tuple_list_fields_normalize_to_tuples(self):
        entry = create_event_ledger_entry(
            event_id="evt-1", event_type="command_event", sequence=0,
            source_command_id="cmd", source_preview_id="ep",
            actor_ids=(build_record_id("actor", "ascendant_1"),),
            target_ids=(build_record_id("item", "brass_threshold_lever"),),
        )
        p = TinyVerticalSliceEventLedgerCandidatePreview(
            event_preview_ref="ep",
            command_ref="cmd",
            world_ref="w",
            lifecycle_status="validated_preview",
            commit_status="not_requested",
            planning_preview_ref="pp",
            context_projection_ref="cp",
            delta_preview_ref="dp",
            candidate_event_entry=entry,
            candidate_event_ref="evt-1",
            candidate_event_type="command_event",
            candidate_state_delta_refs=(),
            actor_record_ids=[build_record_id("actor", "ascendant_1")],
            target_record_ids=[build_record_id("item", "brass_threshold_lever")],
            visible_event_summary="summary",
            backend_only_ref_ids=["ref-1"],
            event_commit_authorized=False,
            event_committed=False,
            state_changed=False,
            persistence_authorized=False,
            replay_authorized=False,
            narration_packet_authorized=False,
            model_called=False,
            narration_generated=False,
        )
        assert isinstance(p.actor_record_ids, tuple)
        assert isinstance(p.target_record_ids, tuple)
        assert isinstance(p.backend_only_ref_ids, tuple)
        assert isinstance(p.candidate_state_delta_refs, tuple)

    def test_metadata_deep_copied_and_frozen(self):
        original = {"key": {"nested": "value"}}
        p = TinyVerticalSliceEventLedgerCandidatePreview(
            event_preview_ref="ep",
            command_ref="cmd",
            world_ref="w",
            lifecycle_status="blocked",
            commit_status="blocked",
            planning_preview_ref="pp",
            context_projection_ref="cp",
            delta_preview_ref="dp",
            candidate_event_entry=None,
            candidate_event_ref=None,
            candidate_event_type=None,
            candidate_state_delta_refs=(),
            actor_record_ids=(),
            target_record_ids=(),
            visible_event_summary="summary",
            backend_only_ref_ids=(),
            event_commit_authorized=False,
            event_committed=False,
            state_changed=False,
            persistence_authorized=False,
            replay_authorized=False,
            narration_packet_authorized=False,
            model_called=False,
            narration_generated=False,
            metadata=original,
        )
        assert isinstance(p.metadata, MappingProxyType)
        original["key"]["nested"] = "changed"
        assert p.metadata["key"]["nested"] == "value"


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class TestBuilder:
    def test_inspect_lever_produces_candidate_event(self, world):
        lifecycle, planning, projection, delta = _make_full_chain(world, "inspect_lever")
        preview = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lifecycle,
            planning_preview=planning, context_projection=projection,
            delta_preview=delta,
        )
        assert preview.candidate_event_entry is not None
        assert isinstance(preview.candidate_event_entry, EventLedgerEntry)
        assert len(preview.candidate_state_delta_refs) == 1

    def test_pull_lever_produces_candidate_event_with_two_deltas(self, world):
        lifecycle, planning, projection, delta = _make_full_chain(
            world, "pull_lever",
            command_ref="command-pull-lever-1",
        )
        preview = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lifecycle,
            planning_preview=planning, context_projection=projection,
            delta_preview=delta,
        )
        assert preview.candidate_event_entry is not None
        assert len(preview.candidate_state_delta_refs) == 2
        assert build_record_id("item", "brass_threshold_lever") in preview.target_record_ids
        assert build_record_id("hazard_clock", "cracked_floor") in preview.target_record_ids

    def test_brace_mechanism_produces_candidate_event(self, world):
        lifecycle, planning, projection, delta = _make_full_chain(
            world, "brace_mechanism",
            command_ref="command-brace-mechanism-1",
        )
        preview = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lifecycle,
            planning_preview=planning, context_projection=projection,
            delta_preview=delta,
        )
        assert preview.candidate_event_entry is not None
        assert len(preview.candidate_state_delta_refs) == 1

    def test_speak_to_npc_produces_candidate_event(self, world):
        lifecycle, planning, projection, delta = _make_full_chain(
            world, "speak_to_npc",
            command_ref="command-speak-to-npc-1",
        )
        preview = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lifecycle,
            planning_preview=planning, context_projection=projection,
            delta_preview=delta,
        )
        assert preview.candidate_event_entry is not None
        assert build_record_id("npc", "watchful_adept") in preview.target_record_ids

    def test_blocked_lifecycle_produces_no_candidate(self, world):
        command = create_tiny_vertical_slice_command_intent(
            command_ref="command-bad-1",
            actor_ref="wrong-actor",
            command_kind="inspect_lever",
            target_ref="lever-brass-threshold",
            declared_intent="bad",
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
        preview = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lifecycle,
            planning_preview=planning, context_projection=projection,
            delta_preview=delta,
        )
        assert preview.candidate_event_entry is None
        assert preview.candidate_event_ref is None
        assert preview.candidate_event_type is None
        assert preview.candidate_state_delta_refs == ()
        assert preview.actor_record_ids == ()
        assert preview.target_record_ids == ()

    def test_rejects_non_world_state(self, default_lifecycle, default_planning_preview, default_context_projection, default_delta_preview):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceWorldState"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state="not-a-state",
                lifecycle_result=default_lifecycle,
                planning_preview=default_planning_preview,
                context_projection=default_context_projection,
                delta_preview=default_delta_preview,
            )

    def test_rejects_non_lifecycle(self, world, default_planning_preview, default_context_projection, default_delta_preview):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceCommandLifecycleResult"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world,
                lifecycle_result="not-a-lifecycle",
                planning_preview=default_planning_preview,
                context_projection=default_context_projection,
                delta_preview=default_delta_preview,
            )

    def test_rejects_non_planning_preview(self, world, default_lifecycle, default_context_projection, default_delta_preview):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceResourceConsequencePlanningPreview"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world,
                lifecycle_result=default_lifecycle,
                planning_preview="not-a-preview",
                context_projection=default_context_projection,
                delta_preview=default_delta_preview,
            )

    def test_rejects_non_context_projection(self, world, default_lifecycle, default_planning_preview, default_delta_preview):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceContextPacketProjection"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world,
                lifecycle_result=default_lifecycle,
                planning_preview=default_planning_preview,
                context_projection="not-a-projection",
                delta_preview=default_delta_preview,
            )

    def test_rejects_non_delta_preview(self, world, default_lifecycle, default_planning_preview, default_context_projection):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceStateDeltaCandidatePreview"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world,
                lifecycle_result=default_lifecycle,
                planning_preview=default_planning_preview,
                context_projection=default_context_projection,
                delta_preview="not-a-delta",
            )

    def test_rejects_lifecycle_state_mismatch(self, default_lifecycle, default_planning_preview, default_context_projection, default_delta_preview):
        other_world = create_tiny_vertical_slice_world_state(world_ref="other-world")
        with pytest.raises(TinyVerticalSliceError, match="resulting_state"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=other_world,
                lifecycle_result=default_lifecycle,
                planning_preview=default_planning_preview,
                context_projection=default_context_projection,
                delta_preview=default_delta_preview,
            )

    def test_rejects_planning_preview_command_ref_mismatch(self, world, default_context_projection, default_delta_preview):
        cmd1 = create_tiny_vertical_slice_command_intent(command_ref="cmd-a")
        lifecycle1 = run_tiny_vertical_slice_command_lifecycle(state=world, command=cmd1)
        cmd2 = create_tiny_vertical_slice_command_intent(command_ref="cmd-b")
        lifecycle2 = run_tiny_vertical_slice_command_lifecycle(state=world, command=cmd2)
        planning2 = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lifecycle2,
        )
        with pytest.raises(TinyVerticalSliceError, match="planning_preview.command_ref"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world,
                lifecycle_result=lifecycle1,
                planning_preview=planning2,
                context_projection=default_context_projection,
                delta_preview=default_delta_preview,
            )

    def test_rejects_context_projection_command_ref_mismatch(self, world, default_delta_preview):
        cmd1 = create_tiny_vertical_slice_command_intent(command_ref="cmd-x")
        lifecycle1 = run_tiny_vertical_slice_command_lifecycle(state=world, command=cmd1)
        planning1 = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lifecycle1,
        )
        cmd2 = create_tiny_vertical_slice_command_intent(command_ref="cmd-y")
        lifecycle2 = run_tiny_vertical_slice_command_lifecycle(state=world, command=cmd2)
        planning2 = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lifecycle2,
        )
        projection2 = build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=lifecycle2, planning_preview=planning2,
        )
        with pytest.raises(TinyVerticalSliceError, match="context_projection.command_ref"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world,
                lifecycle_result=lifecycle1,
                planning_preview=planning1,
                context_projection=projection2,
                delta_preview=default_delta_preview,
            )

    def test_rejects_context_projection_world_ref_mismatch(self, world, default_lifecycle, default_planning_preview, default_delta_preview):
        other_world = create_tiny_vertical_slice_world_state(world_ref="other-world-2")
        cmd = create_tiny_vertical_slice_command_intent()
        lifecycle2 = run_tiny_vertical_slice_command_lifecycle(state=other_world, command=cmd)
        planning2 = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=other_world, lifecycle_result=lifecycle2,
        )
        projection2 = build_tiny_vertical_slice_context_packet_projection(
            state=other_world, lifecycle_result=lifecycle2, planning_preview=planning2,
        )
        with pytest.raises(TinyVerticalSliceError, match="context_projection.world_ref"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world,
                lifecycle_result=default_lifecycle,
                planning_preview=default_planning_preview,
                context_projection=projection2,
                delta_preview=default_delta_preview,
            )

    def test_rejects_delta_preview_command_ref_mismatch(self, world):
        lc1, pl1, pj1, _ = _make_full_chain(world, "inspect_lever", command_ref="cmd-alpha")
        _, _, _, d2 = _make_full_chain(world, "inspect_lever", command_ref="cmd-beta")
        with pytest.raises(TinyVerticalSliceError, match="delta_preview.command_ref"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world, lifecycle_result=lc1,
                planning_preview=pl1, context_projection=pj1,
                delta_preview=d2,
            )

    def test_rejects_delta_preview_world_ref_mismatch(self, world):
        lc1, pl1, pj1, _ = _make_full_chain(world, "inspect_lever")
        other = create_tiny_vertical_slice_world_state(world_ref="other-w")
        _, _, _, d2 = _make_full_chain(other, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="delta_preview.world_ref"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world, lifecycle_result=lc1,
                planning_preview=pl1, context_projection=pj1,
                delta_preview=d2,
            )

    def test_rejects_delta_preview_planning_preview_ref_mismatch(self, world):
        lc, pl, pj, _ = _make_full_chain(world, "inspect_lever")
        d2 = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lc,
            planning_preview=pl, context_projection=pj,
            delta_preview_ref="different-dp-ref",
        )
        pl_other = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lc,
            preview_ref="other-planning-ref",
        )
        with pytest.raises(TinyVerticalSliceError, match="delta_preview.planning_preview_ref"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world, lifecycle_result=lc,
                planning_preview=pl_other, context_projection=pj,
                delta_preview=d2,
            )

    def test_rejects_delta_preview_context_projection_ref_mismatch(self, world):
        lc, pl, pj, d = _make_full_chain(world, "inspect_lever")
        pj_other = build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=lc,
            planning_preview=pl, projection_ref="other-projection-ref",
        )
        with pytest.raises(TinyVerticalSliceError, match="delta_preview.context_projection_ref"):
            build_tiny_vertical_slice_event_ledger_candidate_preview(
                state=world, lifecycle_result=lc,
                planning_preview=pl, context_projection=pj_other,
                delta_preview=d,
            )

    def test_candidate_event_passes_validation(self, default_event_preview):
        assert default_event_preview.candidate_event_entry is not None
        assert validate_event_ledger_entry(default_event_preview.candidate_event_entry)

    def test_candidate_event_sequence_is_zero(self, default_event_preview):
        assert default_event_preview.candidate_event_entry.sequence == 0

    def test_candidate_event_type_is_command_event(self, default_event_preview):
        assert default_event_preview.candidate_event_type == "command_event"

    def test_candidate_event_metadata_candidate_only(self, default_event_preview):
        m = default_event_preview.candidate_event_entry.metadata
        assert m["candidate_only"] is True

    def test_candidate_event_metadata_committed_false(self, default_event_preview):
        m = default_event_preview.candidate_event_entry.metadata
        assert m["committed"] is False

    def test_no_state_mutation(self, world, default_event_preview):
        assert world.lever.visible_state == "untouched"
        assert world.hazard_clock.current_tick == 1

    def test_no_delta_application(self, default_event_preview):
        assert default_event_preview.state_changed is False

    def test_no_event_commitment(self, default_event_preview):
        assert default_event_preview.event_committed is False

    def test_no_persistence_replay_authorization(self, default_event_preview):
        assert default_event_preview.persistence_authorized is False
        assert default_event_preview.replay_authorized is False

    def test_no_narration_packet_authorization(self, default_event_preview):
        assert default_event_preview.narration_packet_authorized is False

    def test_no_single_event_narration_packet_in_increment_6(self, default_event_preview):
        assert not hasattr(default_event_preview, "packet")
        assert not hasattr(default_event_preview, "narration_packet")


# ---------------------------------------------------------------------------
# Visible serializer
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_rejects_non_preview_input(self):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceEventLedgerCandidatePreview"):
            serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview("not-a-preview")

    def test_exact_top_level_key_order(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        expected_keys = [
            "event_preview_ref",
            "command_ref",
            "world_ref",
            "lifecycle_status",
            "commit_status",
            "planning_preview_ref",
            "context_projection_ref",
            "delta_preview_ref",
            "candidate_event_ref",
            "candidate_event_type",
            "candidate_state_delta_refs",
            "actor_record_ids",
            "target_record_ids",
            "visible_event_summary",
            "event_commit_authorized",
            "event_committed",
            "state_changed",
            "persistence_authorized",
            "replay_authorized",
            "narration_packet_authorized",
            "model_called",
            "narration_generated",
            "candidate_event_entry",
            "metadata",
        ]
        assert list(serialized.keys()) == expected_keys

    def test_serializes_candidate_event_entry_as_dict(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        assert isinstance(serialized["candidate_event_entry"], dict)
        assert "event_id" in serialized["candidate_event_entry"]

    def test_serializes_candidate_event_entry_as_none_when_blocked(self, world):
        command = create_tiny_vertical_slice_command_intent(
            command_ref="cmd-blocked",
            actor_ref="wrong-actor",
            command_kind="inspect_lever",
            target_ref="lever-brass-threshold",
            declared_intent="bad",
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
        preview = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lifecycle,
            planning_preview=planning, context_projection=projection,
            delta_preview=delta,
        )
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(preview)
        assert serialized["candidate_event_entry"] is None

    def test_omits_backend_only_ref_ids(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        assert "backend_only_ref_ids" not in serialized

    def test_omits_hidden_fact_ref(self, world, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_ref not in dumped

    def test_omits_hidden_fact_label(self, world, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_label not in dumped

    def test_omits_backend_only_description(self, world, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in dumped

    def test_omits_reveal_condition(self, world, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.reveal_condition not in dumped

    def test_does_not_contain_hidden_fact_backend_only_description(self, world, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        dumped = json.dumps(serialized)
        assert "Pulling the lever advances the cracked-floor hazard clock" not in dumped

    def test_candidate_state_delta_refs_serialized_as_list(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        assert isinstance(serialized["candidate_state_delta_refs"], list)

    def test_actor_record_ids_serialized_as_list(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        assert isinstance(serialized["actor_record_ids"], list)

    def test_target_record_ids_serialized_as_list(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        assert isinstance(serialized["target_record_ids"], list)

    def test_metadata_serialized_as_dict(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        assert isinstance(serialized["metadata"], dict)

    def test_all_authority_booleans_false(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        assert serialized["event_commit_authorized"] is False
        assert serialized["event_committed"] is False
        assert serialized["state_changed"] is False
        assert serialized["persistence_authorized"] is False
        assert serialized["replay_authorized"] is False
        assert serialized["narration_packet_authorized"] is False
        assert serialized["model_called"] is False
        assert serialized["narration_generated"] is False

    def test_candidate_event_metadata_candidate_only(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        entry = serialized["candidate_event_entry"]
        assert entry["metadata"]["candidate_only"] is True

    def test_candidate_event_metadata_committed_false(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        entry = serialized["candidate_event_entry"]
        assert entry["metadata"]["committed"] is False

    def test_serialized_output_does_not_contain_single_event_narration_packet(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        dumped = json.dumps(serialized)
        assert "SingleEventNarrationPacket" not in dumped

    def test_serialized_output_does_not_claim_committed_applied_persisted_replayed(self, default_event_preview):
        serialized = serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(default_event_preview)
        dumped = json.dumps(serialized)
        assert '"event_committed": true' not in dumped
        assert '"state_changed": true' not in dumped
        assert '"persistence_authorized": true' not in dumped
        assert '"replay_authorized": true' not in dumped


# ---------------------------------------------------------------------------
# Source scan — production module
# ---------------------------------------------------------------------------

class TestSourceScan:
    @pytest.fixture(autouse=True)
    def _load_source(self):
        self.source_path = Path(__file__).resolve().parent.parent / "src" / "astra_runtime" / "domain" / "tiny_vertical_slice.py"
        self.content = self.source_path.read_text()

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
    ])
    def test_production_module_does_not_contain(self, forbidden):
        assert forbidden not in self.content, f"Production module contains forbidden string: {forbidden!r}"

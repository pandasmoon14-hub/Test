"""PR-8 Increment 8 — tiny vertical slice commit application boundary tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    TinyVerticalSliceCommitApplicationResult,
    TinyVerticalSliceCommitDryRunResult,
    TinyVerticalSliceError,
    TinyVerticalSliceWorldState,
    apply_tiny_vertical_slice_commit_application,
    build_tiny_vertical_slice_commit_dry_run_result,
    build_tiny_vertical_slice_context_packet_projection,
    build_tiny_vertical_slice_event_ledger_candidate_preview,
    build_tiny_vertical_slice_resource_consequence_planning_preview,
    build_tiny_vertical_slice_state_delta_candidate_preview,
    create_tiny_vertical_slice_command_intent,
    create_tiny_vertical_slice_world_state,
    run_tiny_vertical_slice_command_lifecycle,
    serialize_tiny_vertical_slice_commit_application_visible_result,
)
from astra_runtime.kernel.command_envelope import (
    create_command_envelope,
)
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.transaction_preview import (
    create_transaction_preview,
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


def _make_blocked_dry_run(world):
    """Create a dry-run where lifecycle is blocked (invalid actor ref)."""
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
    return build_tiny_vertical_slice_commit_dry_run_result(
        state=world, lifecycle_result=lifecycle,
        planning_preview=planning, context_projection=projection,
        delta_preview=delta, event_preview=event,
    )


@pytest.fixture()
def default_dry_run(world):
    return _make_dry_run(world, "inspect_lever")


@pytest.fixture()
def default_commit(world):
    return _make_commit_application(world, "inspect_lever")


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment8_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSliceCommitApplicationResult",
            "apply_tiny_vertical_slice_commit_application",
            "serialize_tiny_vertical_slice_commit_application_visible_result",
        ]
        for sym in expected:
            assert hasattr(domain, sym), f"Missing export: {sym}"
            assert sym in domain.__all__, f"Missing from __all__: {sym}"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

class TestDataclass:
    def _make_valid_kwargs(self, world):
        return {
            "commit_ref": "cr",
            "command_ref": "cmd",
            "world_ref": world.world_ref,
            "dry_run_ref": "dr",
            "source_world_state": world,
            "committed_world_state": world,
            "applied_delta_refs": ("delta-1",),
            "committed_event_ref": "ev-1",
            "committed_event_type": "command_event",
            "visible_commit_summary": "summary",
            "visible_changed_record_refs": ("ref-1",),
            "backend_only_ref_ids": (),
            "commit_attempted": True,
            "commit_blocked": False,
            "commit_authorized": True,
            "transaction_executed": True,
            "state_changed": True,
            "state_delta_applied": True,
            "event_committed": True,
            "event_appended": True,
            "persistence_authorized": False,
            "persisted": False,
            "replay_authorized": False,
            "replayed": False,
            "narration_packet_authorized": False,
            "model_called": False,
            "narration_generated": False,
        }

    def test_frozen(self, world):
        result = _make_commit_application(world, "inspect_lever")
        assert isinstance(result, TinyVerticalSliceCommitApplicationResult)
        with pytest.raises(AttributeError):
            result.commit_ref = "x"

    def test_rejects_empty_commit_ref(self, world):
        kw = self._make_valid_kwargs(world)
        kw["commit_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="commit_ref"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_rejects_empty_command_ref(self, world):
        kw = self._make_valid_kwargs(world)
        kw["command_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="command_ref"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_rejects_empty_world_ref(self, world):
        kw = self._make_valid_kwargs(world)
        kw["world_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="world_ref"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_rejects_empty_dry_run_ref(self, world):
        kw = self._make_valid_kwargs(world)
        kw["dry_run_ref"] = ""
        with pytest.raises(TinyVerticalSliceError, match="dry_run_ref"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_rejects_non_world_source_state(self, world):
        kw = self._make_valid_kwargs(world)
        kw["source_world_state"] = "not-a-world"
        with pytest.raises(TinyVerticalSliceError, match="source_world_state"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_rejects_non_world_committed_state(self, world):
        kw = self._make_valid_kwargs(world)
        kw["committed_world_state"] = "not-a-world"
        with pytest.raises(TinyVerticalSliceError, match="committed_world_state"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_rejects_source_world_ref_mismatch(self, world):
        other_world = create_tiny_vertical_slice_world_state(world_ref="other-world")
        kw = self._make_valid_kwargs(world)
        kw["source_world_state"] = other_world
        with pytest.raises(TinyVerticalSliceError, match="source_world_state.world_ref"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_rejects_committed_world_ref_mismatch(self, world):
        other_world = create_tiny_vertical_slice_world_state(world_ref="other-world")
        kw = self._make_valid_kwargs(world)
        kw["committed_world_state"] = other_world
        with pytest.raises(TinyVerticalSliceError, match="committed_world_state.world_ref"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_blocked_result_rejects_true_commit_flags(self, world):
        kw = self._make_valid_kwargs(world)
        kw["commit_blocked"] = True
        kw["commit_authorized"] = True
        kw["applied_delta_refs"] = ()
        kw["committed_event_ref"] = None
        kw["committed_event_type"] = None
        with pytest.raises(TinyVerticalSliceError, match="commit_authorized"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_blocked_rejects_transaction_executed(self, world):
        kw = self._make_valid_kwargs(world)
        kw["commit_blocked"] = True
        kw["commit_authorized"] = False
        kw["transaction_executed"] = True
        kw["applied_delta_refs"] = ()
        kw["committed_event_ref"] = None
        kw["committed_event_type"] = None
        with pytest.raises(TinyVerticalSliceError, match="transaction_executed"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_blocked_rejects_nonempty_delta_refs(self, world):
        kw = self._make_valid_kwargs(world)
        kw["commit_blocked"] = True
        kw["commit_authorized"] = False
        kw["transaction_executed"] = False
        kw["state_changed"] = False
        kw["state_delta_applied"] = False
        kw["event_committed"] = False
        kw["event_appended"] = False
        kw["applied_delta_refs"] = ("d-1",)
        kw["committed_event_ref"] = None
        kw["committed_event_type"] = None
        with pytest.raises(TinyVerticalSliceError, match="applied_delta_refs"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_successful_rejects_commit_attempted_false(self, world):
        kw = self._make_valid_kwargs(world)
        kw["commit_attempted"] = False
        with pytest.raises(TinyVerticalSliceError, match="commit_attempted"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_successful_rejects_commit_authorized_false(self, world):
        kw = self._make_valid_kwargs(world)
        kw["commit_authorized"] = False
        with pytest.raises(TinyVerticalSliceError, match="commit_authorized"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_successful_rejects_transaction_executed_false(self, world):
        kw = self._make_valid_kwargs(world)
        kw["transaction_executed"] = False
        with pytest.raises(TinyVerticalSliceError, match="transaction_executed"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_successful_rejects_state_changed_false(self, world):
        kw = self._make_valid_kwargs(world)
        kw["state_changed"] = False
        with pytest.raises(TinyVerticalSliceError, match="state_changed"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_successful_rejects_state_delta_applied_false(self, world):
        kw = self._make_valid_kwargs(world)
        kw["state_delta_applied"] = False
        with pytest.raises(TinyVerticalSliceError, match="state_delta_applied"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_successful_rejects_event_committed_false(self, world):
        kw = self._make_valid_kwargs(world)
        kw["event_committed"] = False
        with pytest.raises(TinyVerticalSliceError, match="event_committed"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_successful_rejects_event_appended_false(self, world):
        kw = self._make_valid_kwargs(world)
        kw["event_appended"] = False
        with pytest.raises(TinyVerticalSliceError, match="event_appended"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_successful_rejects_empty_applied_delta_refs(self, world):
        kw = self._make_valid_kwargs(world)
        kw["applied_delta_refs"] = ()
        with pytest.raises(TinyVerticalSliceError, match="applied_delta_refs"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_successful_rejects_missing_committed_event_ref(self, world):
        kw = self._make_valid_kwargs(world)
        kw["committed_event_ref"] = None
        with pytest.raises(TinyVerticalSliceError, match="committed_event_ref"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_successful_rejects_missing_committed_event_type(self, world):
        kw = self._make_valid_kwargs(world)
        kw["committed_event_type"] = None
        with pytest.raises(TinyVerticalSliceError, match="committed_event_type"):
            TinyVerticalSliceCommitApplicationResult(**kw)

    @pytest.mark.parametrize("field_name", [
        "persistence_authorized",
        "persisted",
        "replay_authorized",
        "replayed",
        "narration_packet_authorized",
        "model_called",
        "narration_generated",
    ])
    def test_all_results_reject_forbidden_true(self, world, field_name):
        kw = self._make_valid_kwargs(world)
        kw[field_name] = True
        with pytest.raises(TinyVerticalSliceError, match=field_name):
            TinyVerticalSliceCommitApplicationResult(**kw)

    def test_tuple_list_fields_normalize_to_tuples(self, world):
        kw = self._make_valid_kwargs(world)
        kw["applied_delta_refs"] = ["d1"]
        kw["visible_changed_record_refs"] = ["r1"]
        kw["backend_only_ref_ids"] = []
        result = TinyVerticalSliceCommitApplicationResult(**kw)
        assert isinstance(result.applied_delta_refs, tuple)
        assert isinstance(result.visible_changed_record_refs, tuple)
        assert isinstance(result.backend_only_ref_ids, tuple)

    def test_metadata_deep_copied_and_frozen(self, world):
        source = {"key": "value"}
        kw = self._make_valid_kwargs(world)
        kw["metadata"] = source
        result = TinyVerticalSliceCommitApplicationResult(**kw)
        assert isinstance(result.metadata, MappingProxyType)
        source["key"] = "changed"
        assert result.metadata["key"] == "value"


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class TestBuilder:
    def test_inspect_lever_applies_visibility_candidate(self, world):
        result = _make_commit_application(world, "inspect_lever")
        assert result.commit_attempted is True
        assert result.commit_blocked is False
        assert result.commit_authorized is True
        assert result.transaction_executed is True
        assert result.state_changed is True
        assert result.state_delta_applied is True
        assert result.event_committed is True
        assert result.event_appended is True
        assert result.committed_world_state.hidden_fact.backend_only_description == world.hidden_fact.backend_only_description

    def test_inspect_lever_does_not_reveal_hidden_fact(self, world):
        result = _make_commit_application(world, "inspect_lever")
        assert result.committed_world_state.hidden_fact is world.hidden_fact

    def test_brace_mechanism_changes_lever_visible_state(self, world):
        result = _make_commit_application(world, "brace_mechanism")
        assert result.committed_world_state.lever.visible_state == "braced"
        assert result.committed_world_state.lever is not world.lever

    def test_pull_lever_changes_lever_visible_state(self, world):
        result = _make_commit_application(world, "pull_lever")
        assert result.committed_world_state.lever.visible_state == "pulled"

    def test_pull_lever_advances_hazard_clock(self, world):
        result = _make_commit_application(world, "pull_lever")
        assert result.committed_world_state.hazard_clock.current_tick == world.hazard_clock.current_tick + 1

    def test_pull_lever_does_not_exceed_max_ticks(self):
        world = create_tiny_vertical_slice_world_state()
        from astra_runtime.domain.tiny_vertical_slice import TinyVerticalSliceHazardClock
        max_clock = TinyVerticalSliceHazardClock(
            clock_ref=world.hazard_clock.clock_ref,
            clock_label=world.hazard_clock.clock_label,
            visible_description=world.hazard_clock.visible_description,
            current_tick=world.hazard_clock.max_ticks,
            max_ticks=world.hazard_clock.max_ticks,
        )
        maxed_world = TinyVerticalSliceWorldState(
            world_ref=world.world_ref,
            world_label=world.world_label,
            scene=world.scene,
            actor=world.actor,
            npc=world.npc,
            hazard_clock=max_clock,
            lever=world.lever,
            injury=world.injury,
            hidden_fact=world.hidden_fact,
        )
        result = _make_commit_application(maxed_world, "pull_lever")
        assert result.committed_world_state.hazard_clock.current_tick == maxed_world.hazard_clock.max_ticks

    def test_speak_to_npc_changes_disposition(self, world):
        result = _make_commit_application(world, "speak_to_npc")
        assert result.committed_world_state.npc.visible_disposition == "engaged"

    def test_blocked_dry_run_returns_blocked_result(self, world):
        dr = _make_blocked_dry_run(world)
        result = apply_tiny_vertical_slice_commit_application(state=world, dry_run_result=dr)
        assert result.commit_attempted is True
        assert result.commit_blocked is True
        assert result.commit_authorized is False
        assert result.transaction_executed is False
        assert result.state_changed is False
        assert result.state_delta_applied is False
        assert result.event_committed is False
        assert result.event_appended is False
        assert result.committed_event_ref is None
        assert result.committed_event_type is None
        assert result.applied_delta_refs == ()
        assert result.source_world_state is world
        assert result.committed_world_state is world

    def test_builder_rejects_non_world_state_input(self, world):
        dr = _make_dry_run(world, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceWorldState"):
            apply_tiny_vertical_slice_commit_application(state="not-a-world", dry_run_result=dr)

    def test_builder_rejects_non_dry_run_input(self, world):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceCommitDryRunResult"):
            apply_tiny_vertical_slice_commit_application(state=world, dry_run_result="not-a-dry-run")

    def test_builder_rejects_dry_run_world_ref_mismatch(self, world):
        other_world = create_tiny_vertical_slice_world_state(world_ref="other-world")
        dr = _make_dry_run(other_world, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="world_ref"):
            apply_tiny_vertical_slice_commit_application(state=world, dry_run_result=dr)

    def test_original_world_not_mutated(self, world):
        original_lever_state = world.lever.visible_state
        original_clock_tick = world.hazard_clock.current_tick
        original_npc_disposition = world.npc.visible_disposition
        _make_commit_application(world, "pull_lever")
        assert world.lever.visible_state == original_lever_state
        assert world.hazard_clock.current_tick == original_clock_tick
        assert world.npc.visible_disposition == original_npc_disposition

    def test_successful_result_creates_new_committed_world(self, world):
        result = _make_commit_application(world, "pull_lever")
        assert result.source_world_state is world
        assert result.committed_world_state is not world

    def test_hidden_fact_object_unchanged(self, world):
        for kind in ("inspect_lever", "brace_mechanism", "pull_lever", "speak_to_npc"):
            result = _make_commit_application(world, kind)
            assert result.committed_world_state.hidden_fact is world.hidden_fact

    def test_no_persistence_replay_model_narration_flags(self, world):
        for kind in ("inspect_lever", "brace_mechanism", "pull_lever", "speak_to_npc"):
            result = _make_commit_application(world, kind)
            assert result.persistence_authorized is False
            assert result.persisted is False
            assert result.replay_authorized is False
            assert result.replayed is False
            assert result.narration_packet_authorized is False
            assert result.model_called is False
            assert result.narration_generated is False

    def test_no_single_event_narration_packet_in_increment_8(self, world):
        result = _make_commit_application(world, "inspect_lever")
        assert not hasattr(result, "packet")
        assert not hasattr(result, "narration_packet")


# ---------------------------------------------------------------------------
# Visible serializer
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_rejects_non_result_input(self):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceCommitApplicationResult"):
            serialize_tiny_vertical_slice_commit_application_visible_result("not-a-result")

    def test_exact_top_level_key_order(self, world):
        result = _make_commit_application(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
        expected_keys = [
            "commit_ref",
            "command_ref",
            "world_ref",
            "dry_run_ref",
            "applied_delta_refs",
            "committed_event_ref",
            "committed_event_type",
            "visible_commit_summary",
            "visible_changed_record_refs",
            "commit_attempted",
            "commit_blocked",
            "commit_authorized",
            "transaction_executed",
            "state_changed",
            "state_delta_applied",
            "event_committed",
            "event_appended",
            "persistence_authorized",
            "persisted",
            "replay_authorized",
            "replayed",
            "narration_packet_authorized",
            "model_called",
            "narration_generated",
            "committed_world_state",
            "metadata",
        ]
        assert list(serialized.keys()) == expected_keys

    def test_serializes_committed_world_state_visibly(self, world):
        result = _make_commit_application(world, "brace_mechanism")
        serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
        ws = serialized["committed_world_state"]
        assert "world_ref" in ws
        assert "lever" in ws
        assert ws["lever"]["visible_state"] == "braced"

    def test_omits_source_world_state(self, world):
        result = _make_commit_application(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
        assert "source_world_state" not in serialized

    def test_omits_backend_only_ref_ids(self, world):
        result = _make_commit_application(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
        assert "backend_only_ref_ids" not in serialized

    def test_omits_hidden_fact_ref(self, world):
        result = _make_commit_application(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_ref not in dumped or "hidden_fact" not in serialized.get("committed_world_state", {})

    def test_omits_hidden_fact_label(self, world):
        result = _make_commit_application(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_label not in dumped

    def test_omits_backend_only_description(self, world):
        result = _make_commit_application(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in dumped

    def test_omits_reveal_condition(self, world):
        result = _make_commit_application(world, "inspect_lever")
        serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.reveal_condition not in dumped

    def test_does_not_contain_hidden_fact_description_anywhere(self, world):
        for kind in ("inspect_lever", "brace_mechanism", "pull_lever", "speak_to_npc"):
            result = _make_commit_application(world, kind)
            serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
            dumped = json.dumps(serialized)
            assert world.hidden_fact.backend_only_description not in dumped

    def test_successful_serializer_truthful_flags(self, world):
        for kind in ("inspect_lever", "brace_mechanism", "pull_lever", "speak_to_npc"):
            result = _make_commit_application(world, kind)
            serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
            assert serialized["commit_attempted"] is True
            assert serialized["commit_blocked"] is False
            assert serialized["commit_authorized"] is True
            assert serialized["transaction_executed"] is True
            assert serialized["state_changed"] is True
            assert serialized["state_delta_applied"] is True
            assert serialized["event_committed"] is True
            assert serialized["event_appended"] is True

    def test_blocked_serializer_flags(self, world):
        dr = _make_blocked_dry_run(world)
        result = apply_tiny_vertical_slice_commit_application(state=world, dry_run_result=dr)
        serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
        assert serialized["commit_attempted"] is True
        assert serialized["commit_blocked"] is True
        assert serialized["commit_authorized"] is False
        assert serialized["transaction_executed"] is False
        assert serialized["state_changed"] is False
        assert serialized["state_delta_applied"] is False
        assert serialized["event_committed"] is False
        assert serialized["event_appended"] is False

    @pytest.mark.parametrize("field_name", [
        "persistence_authorized",
        "persisted",
        "replay_authorized",
        "replayed",
        "narration_packet_authorized",
        "model_called",
        "narration_generated",
    ])
    def test_serializer_always_shows_false_for_forbidden_flags(self, world, field_name):
        for kind in ("inspect_lever", "brace_mechanism", "pull_lever", "speak_to_npc"):
            result = _make_commit_application(world, kind)
            serialized = serialize_tiny_vertical_slice_commit_application_visible_result(result)
            assert serialized[field_name] is False, f"{field_name} should be False for {kind}"
        dr = _make_blocked_dry_run(world)
        blocked = apply_tiny_vertical_slice_commit_application(state=world, dry_run_result=dr)
        serialized = serialize_tiny_vertical_slice_commit_application_visible_result(blocked)
        assert serialized[field_name] is False, f"{field_name} should be False for blocked"


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

    def test_no_generic_apply_delta(self):
        assert "apply_delta(" not in self.source_text

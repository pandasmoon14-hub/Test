"""PR-8 Increment 7 — tiny vertical slice commit dry-run result tests."""

from __future__ import annotations

import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    TinyVerticalSliceCommitDryRunResult,
    TinyVerticalSliceError,
    build_tiny_vertical_slice_commit_dry_run_result,
    build_tiny_vertical_slice_context_packet_projection,
    build_tiny_vertical_slice_event_ledger_candidate_preview,
    build_tiny_vertical_slice_resource_consequence_planning_preview,
    build_tiny_vertical_slice_state_delta_candidate_preview,
    create_tiny_vertical_slice_command_intent,
    create_tiny_vertical_slice_world_state,
    run_tiny_vertical_slice_command_lifecycle,
    serialize_tiny_vertical_slice_commit_dry_run_visible_result,
)
from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    create_command_envelope,
    validate_command_envelope,
)
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.transaction_preview import (
    TransactionPreview,
    create_transaction_preview,
    validate_transaction_preview,
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


@pytest.fixture()
def default_dry_run(world):
    return _make_dry_run(world, "inspect_lever")


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

class TestExports:
    def test_all_pr8_increment7_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "TinyVerticalSliceCommitDryRunResult",
            "build_tiny_vertical_slice_commit_dry_run_result",
            "serialize_tiny_vertical_slice_commit_dry_run_visible_result",
        ]
        for sym in expected:
            assert hasattr(domain, sym), f"Missing export: {sym}"
            assert sym in domain.__all__, f"Missing from __all__: {sym}"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

class TestDataclass:
    def _make_envelope_and_preview(self, cmd_ref="cmd", dry_run_ref="dr"):
        env = create_command_envelope(
            command_id=cmd_ref, command_type="inspect_lever",
            source_actor_id=build_record_id("actor", "ascendant_1"),
            payload={"dry_run_only": True, "commit_authorized": False},
        )
        txn = create_transaction_preview(
            preview_id=dry_run_ref, command=env,
            status="preview_created",
        )
        return env, txn

    def _make_minimal_kwargs(self, **overrides):
        env, txn = self._make_envelope_and_preview()
        defaults = dict(
            dry_run_ref="dr",
            command_ref="cmd",
            world_ref="w",
            lifecycle_status="validated_preview",
            commit_status="not_requested",
            planning_preview_ref="pp",
            context_projection_ref="cp",
            delta_preview_ref="dp",
            event_preview_ref="ep",
            command_envelope=env,
            transaction_preview=txn,
            candidate_delta_refs=(),
            candidate_event_ref=None,
            visible_dry_run_summary="summary",
            visible_commit_requirements=(),
            backend_only_ref_ids=(),
            commit_authorized=False,
            transaction_executed=False,
            state_changed=False,
            state_delta_applied=False,
            event_committed=False,
            event_appended=False,
            persistence_authorized=False,
            replay_authorized=False,
            narration_packet_authorized=False,
            model_called=False,
            narration_generated=False,
        )
        defaults.update(overrides)
        return defaults

    def test_frozen(self):
        p = TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs())
        with pytest.raises(AttributeError):
            p.dry_run_ref = "changed"

    def test_rejects_empty_dry_run_ref(self):
        with pytest.raises(TinyVerticalSliceError, match="dry_run_ref"):
            TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(dry_run_ref=""))

    def test_rejects_empty_command_ref(self):
        with pytest.raises(TinyVerticalSliceError, match="command_ref"):
            env = create_command_envelope(
                command_id="cmd", command_type="inspect_lever",
                source_actor_id=build_record_id("actor", "ascendant_1"),
            )
            txn = create_transaction_preview(preview_id="dr", command=env)
            TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(
                command_ref="",
            ))

    def test_rejects_empty_world_ref(self):
        with pytest.raises(TinyVerticalSliceError, match="world_ref"):
            TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(world_ref=""))

    def test_rejects_non_command_envelope(self):
        with pytest.raises(TinyVerticalSliceError, match="CommandEnvelope"):
            TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(
                command_envelope="not-an-envelope",
            ))

    def test_rejects_non_transaction_preview(self):
        with pytest.raises(TinyVerticalSliceError, match="TransactionPreview"):
            TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(
                transaction_preview="not-a-preview",
            ))

    def test_rejects_command_envelope_command_id_mismatch(self):
        env = create_command_envelope(
            command_id="other-cmd", command_type="inspect_lever",
            source_actor_id=build_record_id("actor", "ascendant_1"),
        )
        txn = create_transaction_preview(preview_id="dr", command=env)
        with pytest.raises(TinyVerticalSliceError, match="command_envelope.command_id"):
            TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(
                command_envelope=env,
                transaction_preview=txn,
            ))

    def test_rejects_transaction_preview_command_id_mismatch(self):
        env_other = create_command_envelope(
            command_id="other-cmd", command_type="inspect_lever",
            source_actor_id=build_record_id("actor", "ascendant_1"),
        )
        txn = create_transaction_preview(preview_id="dr", command=env_other)
        env_main = create_command_envelope(
            command_id="cmd", command_type="inspect_lever",
            source_actor_id=build_record_id("actor", "ascendant_1"),
        )
        with pytest.raises(TinyVerticalSliceError, match="transaction_preview.command_id"):
            TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(
                command_envelope=env_main,
                transaction_preview=txn,
            ))

    def test_rejects_transaction_preview_id_mismatch(self):
        env = create_command_envelope(
            command_id="cmd", command_type="inspect_lever",
            source_actor_id=build_record_id("actor", "ascendant_1"),
        )
        txn = create_transaction_preview(preview_id="wrong-dr", command=env)
        with pytest.raises(TinyVerticalSliceError, match="transaction_preview.preview_id"):
            TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(
                transaction_preview=txn,
            ))

    @pytest.mark.parametrize("field_name", [
        "commit_authorized",
        "transaction_executed",
        "state_changed",
        "state_delta_applied",
        "event_committed",
        "event_appended",
        "persistence_authorized",
        "replay_authorized",
        "narration_packet_authorized",
        "model_called",
        "narration_generated",
    ])
    def test_rejects_true_authority_booleans(self, field_name):
        with pytest.raises(TinyVerticalSliceError, match=field_name):
            TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(**{field_name: True}))

    def test_tuple_list_fields_normalize_to_tuples(self):
        p = TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(
            candidate_delta_refs=["d1"],
            visible_commit_requirements=["r1"],
            backend_only_ref_ids=["b1"],
        ))
        assert isinstance(p.candidate_delta_refs, tuple)
        assert isinstance(p.visible_commit_requirements, tuple)
        assert isinstance(p.backend_only_ref_ids, tuple)

    def test_metadata_deep_copied_and_frozen(self):
        original = {"key": {"nested": "value"}}
        p = TinyVerticalSliceCommitDryRunResult(**self._make_minimal_kwargs(metadata=original))
        assert isinstance(p.metadata, MappingProxyType)
        original["key"]["nested"] = "changed"
        assert p.metadata["key"]["nested"] == "value"


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class TestBuilder:
    def test_inspect_lever_produces_dry_run(self, world):
        dr = _make_dry_run(world, "inspect_lever")
        assert dr.candidate_event_ref is not None
        assert len(dr.candidate_delta_refs) == 1
        assert dr.transaction_preview.status == "preview_created"

    def test_pull_lever_produces_dry_run_with_two_delta_refs(self, world):
        dr = _make_dry_run(world, "pull_lever", command_ref="command-pull-lever-1")
        assert dr.candidate_event_ref is not None
        assert len(dr.candidate_delta_refs) == 2

    def test_brace_mechanism_produces_dry_run(self, world):
        dr = _make_dry_run(world, "brace_mechanism", command_ref="command-brace-mechanism-1")
        assert dr.candidate_event_ref is not None

    def test_speak_to_npc_produces_dry_run(self, world):
        dr = _make_dry_run(world, "speak_to_npc", command_ref="command-speak-to-npc-1")
        assert dr.candidate_event_ref is not None

    def test_blocked_lifecycle_produces_rejected_dry_run(self, world):
        command = create_tiny_vertical_slice_command_intent(
            command_ref="cmd-blocked",
            actor_ref="wrong-actor",
            command_kind="inspect_lever",
            target_ref="lever-brass-threshold",
            declared_intent="bad",
        )
        lc = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        pl = build_tiny_vertical_slice_resource_consequence_planning_preview(state=world, lifecycle_result=lc)
        pj = build_tiny_vertical_slice_context_packet_projection(state=world, lifecycle_result=lc, planning_preview=pl)
        dp = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl, context_projection=pj,
        )
        ep = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl, context_projection=pj, delta_preview=dp,
        )
        dr = build_tiny_vertical_slice_commit_dry_run_result(
            state=world, lifecycle_result=lc, planning_preview=pl, context_projection=pj,
            delta_preview=dp, event_preview=ep,
        )
        assert dr.candidate_event_ref is None
        assert dr.candidate_delta_refs == ()
        assert dr.transaction_preview.status == "preview_rejected"
        assert dr.transaction_preview.requires_confirmation is False

    def test_rejects_non_world_state(self, world):
        lc, pl, pj, dp, ep = _make_full_chain(world, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceWorldState"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state="not", lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview=dp, event_preview=ep,
            )

    def test_rejects_non_lifecycle(self, world):
        lc, pl, pj, dp, ep = _make_full_chain(world, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceCommandLifecycleResult"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result="not", planning_preview=pl,
                context_projection=pj, delta_preview=dp, event_preview=ep,
            )

    def test_rejects_non_planning_preview(self, world):
        lc, pl, pj, dp, ep = _make_full_chain(world, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceResourceConsequencePlanningPreview"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview="not",
                context_projection=pj, delta_preview=dp, event_preview=ep,
            )

    def test_rejects_non_context_projection(self, world):
        lc, pl, pj, dp, ep = _make_full_chain(world, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceContextPacketProjection"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection="not", delta_preview=dp, event_preview=ep,
            )

    def test_rejects_non_delta_preview(self, world):
        lc, pl, pj, dp, ep = _make_full_chain(world, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceStateDeltaCandidatePreview"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview="not", event_preview=ep,
            )

    def test_rejects_non_event_preview(self, world):
        lc, pl, pj, dp, ep = _make_full_chain(world, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceEventLedgerCandidatePreview"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview=dp, event_preview="not",
            )

    def test_rejects_lifecycle_state_mismatch(self, world):
        lc, pl, pj, dp, ep = _make_full_chain(world, "inspect_lever")
        other_world = create_tiny_vertical_slice_world_state(world_ref="other")
        with pytest.raises(TinyVerticalSliceError, match="resulting_state"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=other_world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview=dp, event_preview=ep,
            )

    def test_rejects_planning_preview_command_ref_mismatch(self, world):
        lc1, _, _, _, _ = _make_full_chain(world, "inspect_lever", command_ref="cmd-a")
        _, pl2, pj2, dp2, ep2 = _make_full_chain(world, "inspect_lever", command_ref="cmd-b")
        with pytest.raises(TinyVerticalSliceError, match="planning_preview.command_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc1, planning_preview=pl2,
                context_projection=pj2, delta_preview=dp2, event_preview=ep2,
            )

    def test_rejects_context_projection_command_ref_mismatch(self, world):
        lc1, pl1, _, _, _ = _make_full_chain(world, "inspect_lever", command_ref="cmd-x")
        _, _, pj2, dp2, ep2 = _make_full_chain(world, "inspect_lever", command_ref="cmd-y")
        with pytest.raises(TinyVerticalSliceError, match="context_projection.command_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc1, planning_preview=pl1,
                context_projection=pj2, delta_preview=dp2, event_preview=ep2,
            )

    def test_rejects_context_projection_world_ref_mismatch(self, world):
        lc, pl, _, _, _ = _make_full_chain(world, "inspect_lever")
        other = create_tiny_vertical_slice_world_state(world_ref="other-w")
        _, _, pj2, dp2, ep2 = _make_full_chain(other, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="context_projection.world_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj2, delta_preview=dp2, event_preview=ep2,
            )

    def test_rejects_delta_preview_command_ref_mismatch(self, world):
        lc, pl, pj, _, _ = _make_full_chain(world, "inspect_lever", command_ref="cmd-alpha")
        _, _, _, dp2, ep2 = _make_full_chain(world, "inspect_lever", command_ref="cmd-beta")
        with pytest.raises(TinyVerticalSliceError, match="delta_preview.command_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview=dp2, event_preview=ep2,
            )

    def test_rejects_delta_preview_world_ref_mismatch(self, world):
        lc, pl, pj, _, _ = _make_full_chain(world, "inspect_lever")
        other = create_tiny_vertical_slice_world_state(world_ref="other-w2")
        _, _, _, dp2, ep2 = _make_full_chain(other, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="delta_preview.world_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview=dp2, event_preview=ep2,
            )

    def test_rejects_delta_preview_planning_preview_ref_mismatch(self, world):
        lc, pl, pj, _, _ = _make_full_chain(world, "inspect_lever")
        pl2 = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lc, preview_ref="other-pl",
        )
        dp2 = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl, context_projection=pj,
            delta_preview_ref="alt-dp",
        )
        with pytest.raises(TinyVerticalSliceError, match="delta_preview.planning_preview_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl2,
                context_projection=pj, delta_preview=dp2,
                event_preview=build_tiny_vertical_slice_event_ledger_candidate_preview(
                    state=world, lifecycle_result=lc, planning_preview=pl,
                    context_projection=pj, delta_preview=dp2,
                ),
            )

    def test_rejects_delta_preview_context_projection_ref_mismatch(self, world):
        lc, pl, pj, dp, ep = _make_full_chain(world, "inspect_lever")
        pj2 = build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=lc, planning_preview=pl,
            projection_ref="other-pj",
        )
        with pytest.raises(TinyVerticalSliceError, match="delta_preview.context_projection_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj2, delta_preview=dp, event_preview=ep,
            )

    def test_rejects_event_preview_command_ref_mismatch(self, world):
        lc, pl, pj, dp, _ = _make_full_chain(world, "inspect_lever", command_ref="cmd-m")
        _, _, _, _, ep2 = _make_full_chain(world, "inspect_lever", command_ref="cmd-n")
        with pytest.raises(TinyVerticalSliceError, match="event_preview.command_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview=dp, event_preview=ep2,
            )

    def test_rejects_event_preview_world_ref_mismatch(self, world):
        lc, pl, pj, dp, _ = _make_full_chain(world, "inspect_lever")
        other = create_tiny_vertical_slice_world_state(world_ref="other-w3")
        _, _, _, _, ep2 = _make_full_chain(other, "inspect_lever")
        with pytest.raises(TinyVerticalSliceError, match="event_preview.world_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview=dp, event_preview=ep2,
            )

    def test_rejects_event_preview_planning_preview_ref_mismatch(self, world):
        lc, pl, pj, dp, _ = _make_full_chain(world, "inspect_lever")
        pl2 = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lc, preview_ref="other-pl2",
        )
        pj2 = build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=lc, planning_preview=pl2,
        )
        dp2 = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl2, context_projection=pj2,
        )
        ep2 = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl2,
            context_projection=pj2, delta_preview=dp2,
        )
        with pytest.raises(TinyVerticalSliceError, match="event_preview.planning_preview_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview=dp, event_preview=ep2,
            )

    def test_rejects_event_preview_context_projection_ref_mismatch(self, world):
        lc, pl, pj, dp, _ = _make_full_chain(world, "inspect_lever")
        pj2 = build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=lc, planning_preview=pl,
            projection_ref="other-pj2",
        )
        dp2 = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl, context_projection=pj2,
        )
        ep2 = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl,
            context_projection=pj2, delta_preview=dp2,
        )
        with pytest.raises(TinyVerticalSliceError, match="event_preview.context_projection_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview=dp, event_preview=ep2,
            )

    def test_rejects_event_preview_delta_preview_ref_mismatch(self, world):
        lc, pl, pj, _, _ = _make_full_chain(world, "inspect_lever")
        dp1 = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl, context_projection=pj,
            delta_preview_ref="dp-one",
        )
        dp2 = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl, context_projection=pj,
            delta_preview_ref="dp-two",
        )
        ep2 = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl,
            context_projection=pj, delta_preview=dp2,
        )
        with pytest.raises(TinyVerticalSliceError, match="event_preview.delta_preview_ref"):
            build_tiny_vertical_slice_commit_dry_run_result(
                state=world, lifecycle_result=lc, planning_preview=pl,
                context_projection=pj, delta_preview=dp1, event_preview=ep2,
            )

    def test_command_envelope_passes_validation(self, default_dry_run):
        assert validate_command_envelope(default_dry_run.command_envelope)

    def test_transaction_preview_passes_validation(self, default_dry_run):
        assert validate_transaction_preview(default_dry_run.transaction_preview)

    def test_ready_chain_transaction_status_is_preview_created(self, default_dry_run):
        assert default_dry_run.transaction_preview.status == "preview_created"

    def test_blocked_chain_transaction_status_is_preview_rejected(self, world):
        command = create_tiny_vertical_slice_command_intent(
            command_ref="cmd-bad",
            actor_ref="wrong-actor",
            command_kind="inspect_lever",
            target_ref="lever-brass-threshold",
            declared_intent="bad",
        )
        lc = run_tiny_vertical_slice_command_lifecycle(state=world, command=command)
        pl = build_tiny_vertical_slice_resource_consequence_planning_preview(state=world, lifecycle_result=lc)
        pj = build_tiny_vertical_slice_context_packet_projection(state=world, lifecycle_result=lc, planning_preview=pl)
        dp = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl, context_projection=pj,
        )
        ep = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lc, planning_preview=pl, context_projection=pj, delta_preview=dp,
        )
        dr = build_tiny_vertical_slice_commit_dry_run_result(
            state=world, lifecycle_result=lc, planning_preview=pl,
            context_projection=pj, delta_preview=dp, event_preview=ep,
        )
        assert dr.transaction_preview.status == "preview_rejected"

    def test_no_state_mutation(self, world, default_dry_run):
        assert world.lever.visible_state == "untouched"
        assert world.hazard_clock.current_tick == 1

    def test_no_state_delta_application(self, default_dry_run):
        assert default_dry_run.state_delta_applied is False
        assert default_dry_run.state_changed is False

    def test_no_event_commitment(self, default_dry_run):
        assert default_dry_run.event_committed is False

    def test_no_event_append(self, default_dry_run):
        assert default_dry_run.event_appended is False

    def test_no_persistence_replay_authorization(self, default_dry_run):
        assert default_dry_run.persistence_authorized is False
        assert default_dry_run.replay_authorized is False

    def test_no_narration_packet_authorization(self, default_dry_run):
        assert default_dry_run.narration_packet_authorized is False

    def test_no_model_call(self, default_dry_run):
        assert default_dry_run.model_called is False

    def test_no_narration_generation(self, default_dry_run):
        assert default_dry_run.narration_generated is False

    def test_no_single_event_narration_packet_import(self):
        source = Path(__file__).resolve().parent.parent / "src" / "astra_runtime" / "domain" / "tiny_vertical_slice.py"
        content = source.read_text()
        assert "SingleEventNarrationPacket" not in content


# ---------------------------------------------------------------------------
# Visible serializer
# ---------------------------------------------------------------------------

class TestVisibleSerializer:
    def test_rejects_non_dry_run_input(self):
        with pytest.raises(TinyVerticalSliceError, match="TinyVerticalSliceCommitDryRunResult"):
            serialize_tiny_vertical_slice_commit_dry_run_visible_result("not")

    def test_exact_top_level_key_order(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        expected_keys = [
            "dry_run_ref",
            "command_ref",
            "world_ref",
            "lifecycle_status",
            "commit_status",
            "planning_preview_ref",
            "context_projection_ref",
            "delta_preview_ref",
            "event_preview_ref",
            "candidate_delta_refs",
            "candidate_event_ref",
            "visible_dry_run_summary",
            "visible_commit_requirements",
            "commit_authorized",
            "transaction_executed",
            "state_changed",
            "state_delta_applied",
            "event_committed",
            "event_appended",
            "persistence_authorized",
            "replay_authorized",
            "narration_packet_authorized",
            "model_called",
            "narration_generated",
            "command_envelope",
            "transaction_preview",
            "metadata",
        ]
        assert list(serialized.keys()) == expected_keys

    def test_serializes_command_envelope_as_dict(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        assert isinstance(serialized["command_envelope"], dict)
        assert "command_id" in serialized["command_envelope"]

    def test_serializes_transaction_preview_as_dict(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        assert isinstance(serialized["transaction_preview"], dict)
        assert "preview_id" in serialized["transaction_preview"]

    def test_omits_backend_only_ref_ids(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        assert "backend_only_ref_ids" not in serialized

    def test_omits_hidden_fact_ref(self, world, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_ref not in dumped

    def test_omits_hidden_fact_label(self, world, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.hidden_fact_label not in dumped

    def test_omits_backend_only_description(self, world, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.backend_only_description not in dumped

    def test_omits_reveal_condition(self, world, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        dumped = json.dumps(serialized)
        assert world.hidden_fact.reveal_condition not in dumped

    def test_does_not_contain_hidden_fact_backend_only_description(self, world, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        dumped = json.dumps(serialized)
        assert "Pulling the lever advances the cracked-floor hazard clock" not in dumped

    def test_candidate_delta_refs_serialize_as_list(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        assert isinstance(serialized["candidate_delta_refs"], list)

    def test_visible_commit_requirements_serialize_as_list(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        assert isinstance(serialized["visible_commit_requirements"], list)

    def test_metadata_serializes_as_dict(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        assert isinstance(serialized["metadata"], dict)

    def test_all_authority_booleans_false(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        assert serialized["commit_authorized"] is False
        assert serialized["transaction_executed"] is False
        assert serialized["state_changed"] is False
        assert serialized["state_delta_applied"] is False
        assert serialized["event_committed"] is False
        assert serialized["event_appended"] is False
        assert serialized["persistence_authorized"] is False
        assert serialized["replay_authorized"] is False
        assert serialized["narration_packet_authorized"] is False
        assert serialized["model_called"] is False
        assert serialized["narration_generated"] is False

    def test_command_envelope_payload_dry_run_only(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        payload = serialized["command_envelope"]["payload"]
        assert payload["dry_run_only"] is True

    def test_command_envelope_payload_commit_authorized_false(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        payload = serialized["command_envelope"]["payload"]
        assert payload["commit_authorized"] is False

    def test_transaction_preview_metadata_dry_run_only(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        meta = serialized["transaction_preview"]["metadata"]
        assert meta["dry_run_only"] is True

    def test_transaction_preview_metadata_commit_authorized_false(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        meta = serialized["transaction_preview"]["metadata"]
        assert meta["commit_authorized"] is False

    def test_transaction_preview_metadata_transaction_executed_false(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        meta = serialized["transaction_preview"]["metadata"]
        assert meta["transaction_executed"] is False

    def test_serialized_output_does_not_contain_single_event_narration_packet(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        dumped = json.dumps(serialized)
        assert "SingleEventNarrationPacket" not in dumped

    def test_serialized_output_does_not_claim_committed_applied_appended(self, default_dry_run):
        serialized = serialize_tiny_vertical_slice_commit_dry_run_visible_result(default_dry_run)
        dumped = json.dumps(serialized)
        assert '"transaction_executed": true' not in dumped
        assert '"state_changed": true' not in dumped
        assert '"state_delta_applied": true' not in dumped
        assert '"event_committed": true' not in dumped
        assert '"event_appended": true' not in dumped
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

from __future__ import annotations

from pathlib import Path

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import GROUNDSKEEPER_ID


def _assert_commit(result, expected_type: str):
    assert result.result_type == expected_type
    assert result.authoritative_changed is True
    assert result.pre_state_digest != result.post_state_digest
    return result


def _run_sustained_cross_family_trace(*, checkpoint_path: Path | None = None):
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint_path)
    results = []

    results.append(_assert_commit(app.pickup("lantern"), "custody_committed"))
    results.append(_assert_commit(app.light_object("lantern"), "object_lit_state_committed"))
    results.append(_assert_commit(app.move("south"), "movement_committed"))
    results.append(_assert_commit(app.open_object("chest"), "object_state_committed"))
    results.append(_assert_commit(app.store_object("lantern", "chest"), "storage_committed"))
    results.append(_assert_commit(app.retrieve_object("lantern", "chest"), "storage_committed"))

    world = _assert_commit(app.wait(), "world_advanced")
    assert world.world_process_actor_id == GROUNDSKEEPER_ID
    assert world.world_process_action == "move"
    results.append(world)

    handoff = _assert_commit(
        app.give_object("lantern", "groundskeeper"),
        "actor_object_handoff_committed",
    )
    results.append(handoff)

    returned = _assert_commit(
        app.request_object_from_actor("groundskeeper", "lantern"),
        "actor_object_handoff_committed",
    )
    results.append(returned)

    displaced = _assert_commit(
        app.throw_object("lantern", "east"),
        "object_displacement_committed",
    )
    results.append(displaced)

    signal = app.look_direction("east")
    assert signal.result_type == "directional_light_signal"
    assert signal.authoritative_changed is False
    assert signal.pre_state_digest == signal.post_state_digest == app.authoritative_digest()

    # Adversarial repeated action: the lantern is no longer carried after the
    # committed throw. Repeating the throw must fail without authoritative
    # mutation or a synthetic recovery transition.
    before_rejection = app.authoritative_digest()
    rejected = app.throw_object("lantern", "east")
    assert rejected.result_type == "object_displacement_rejected"
    assert rejected.authoritative_changed is False
    assert rejected.pre_state_digest == before_rejection
    assert rejected.post_state_digest == before_rejection
    assert app.authoritative_digest() == before_rejection

    trace_identity = tuple(
        (
            item.result_type,
            item.command_id,
            item.command_fingerprint,
            item.receipt_id,
            item.state_delta_id,
            item.post_state_digest,
        )
        for item in results
    )
    return app, trace_identity


def test_sustained_cross_family_trace_is_deterministic() -> None:
    first, first_trace = _run_sustained_cross_family_trace()
    second, second_trace = _run_sustained_cross_family_trace()

    assert second_trace == first_trace
    assert second.authoritative_digest() == first.authoritative_digest()
    assert second.runtime_state == first.runtime_state


def test_cross_family_v4_checkpoint_save_restore_save_is_byte_stable(tmp_path) -> None:
    checkpoint = tmp_path / "myravant-skeleton-extraction-v4.json"
    app, trace = _run_sustained_cross_family_trace(checkpoint_path=checkpoint)
    expected_digest = app.authoritative_digest()

    save = app.save()
    assert save.result_type == "checkpoint_written"
    assert save.authoritative_changed is False
    first_bytes = checkpoint.read_bytes()
    assert first_bytes

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == expected_digest
    assert restored.runtime_state == app.runtime_state

    second_save = restored.save()
    assert second_save.result_type == "checkpoint_written"
    assert second_save.authoritative_changed is False
    second_bytes = checkpoint.read_bytes()

    assert second_bytes == first_bytes
    assert restored.authoritative_digest() == expected_digest

    # A restored campaign must reproduce the same externally relevant trace
    # identities accumulated before persistence.
    assert trace[-1][0] == "object_displacement_committed"
    assert restored.runtime_state.committed_actor_object_handoff_transitions
    assert restored.runtime_state.committed_object_displacement_transitions


def test_cross_family_checkpoint_rejection_pressure_does_not_change_state(tmp_path) -> None:
    checkpoint = tmp_path / "myravant-skeleton-extraction-adversarial.json"
    app, _ = _run_sustained_cross_family_trace(checkpoint_path=checkpoint)
    app.save()
    canonical = checkpoint.read_bytes()
    before = app.authoritative_digest()

    # Observation and a rejected remote pickup after displacement must remain
    # non-authoritative and must not rewrite the persisted checkpoint.
    observation = app.look_direction("east")
    assert observation.authoritative_changed is False
    pickup = app.pickup("lantern")
    assert pickup.authoritative_changed is False
    assert app.authoritative_digest() == before
    assert checkpoint.read_bytes() == canonical

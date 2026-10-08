from __future__ import annotations

import hashlib
import json
from io import StringIO

import pytest

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    PLAYER_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_vsm14_follow_intent import execute_vsm14_follow_request
from astra_runtime.myravant_vsm14_terminal import run_vsm14_terminal


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _meet_and_activate(app: MyravantVSM14Application) -> None:
    assert app.move("south").authoritative_changed
    assert app.move("south").authoritative_changed
    activation = execute_vsm14_follow_request(
        app, "ask groundskeeper to follow me"
    )
    assert activation.result.authoritative_changed


def test_v5_save_restore_preserves_follow_intent_and_exact_authoritative_digest(
    tmp_path,
) -> None:
    checkpoint = tmp_path / "vsm14.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _meet_and_activate(app)
    assert app.move("north").world_process_outcome == "committed"
    expected_digest = app.authoritative_digest()
    expected_follow = app.follow_intent_state
    expected_movement = app.state

    saved = app.save()
    assert saved.result_type == "checkpoint_written"
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)

    assert restored.authoritative_digest() == expected_digest
    assert restored.follow_intent_state == expected_follow
    assert restored.state.committed_transitions == expected_movement.committed_transitions
    assert restored.representation_digest() == app.representation_digest()
    assert restored.entity_place_id(PLAYER_ID) == YARD_ID
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID


def test_v5_save_restore_save_is_byte_stable(tmp_path) -> None:
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"
    app = MyravantVSM14Application.new(checkpoint_path=first_path)
    _meet_and_activate(app)
    assert app.move("north").world_process_outcome == "committed"
    app.save()
    first_bytes = first_path.read_bytes()

    restored = MyravantVSM14Application.restore(checkpoint_path=first_path)
    restored.checkpoint_path = second_path
    restored.save()
    assert second_path.read_bytes() == first_bytes


def test_vsm14_restore_accepts_historical_v4_and_starts_without_follow_intent(
    tmp_path,
) -> None:
    checkpoint = tmp_path / "historical-v4.json"
    old = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    assert old.pickup("lantern").authoritative_changed
    assert old.move("south").authoritative_changed
    assert old.move("south").authoritative_changed
    assert old.give_object("lantern", "groundskeeper").authoritative_changed
    old.save()
    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert envelope["format_version"] == 4

    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.follow_intent_state.active_intents == ()
    assert restored.follow_intent_state.committed_transitions == ()
    assert restored.entity_place_id(PLAYER_ID) == restored.entity_place_id(
        GROUNDSKEEPER_ID
    )


def test_semantically_tampered_v5_fails_even_with_recomputed_outer_integrity(
    tmp_path,
) -> None:
    checkpoint = tmp_path / "tampered-v5.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _meet_and_activate(app)
    app.save()

    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    follow = envelope["authoritative_payload"]["components"]["follow_intent"]
    follow["active_intents"][0]["leader_entity_id"] = GROUNDSKEEPER_ID
    envelope["integrity_digest"] = hashlib.sha256(
        _canonical_bytes(envelope["authoritative_payload"])
    ).hexdigest()
    checkpoint.write_bytes(_canonical_bytes(envelope))

    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantVSM14Application.restore(checkpoint_path=checkpoint)


def test_vsm14_raw_terminal_sustained_follow_save_restore_flow(tmp_path) -> None:
    checkpoint = tmp_path / "terminal-v5.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    output = StringIO()
    interactions = run_vsm14_terminal(
        app,
        input_stream=StringIO(
            "go south\n"
            "go south\n"
            "ask groundskeeper to follow me\n"
            "go north\n"
            "go east\n"
            "look\n"
            "save\n"
            "quit\n"
        ),
        output_stream=output,
    )

    assert any(
        item.route == "vsm14_persistent_follow_intent"
        for item in interactions
    )
    assert "The Groundskeeper agrees to follow you." in output.getvalue()
    assert output.getvalue().count("The Groundskeeper follows.") == 2
    assert checkpoint.exists()

    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.entity_place_id(PLAYER_ID) == restored.entity_place_id(
        GROUNDSKEEPER_ID
    )
    assert len(restored.follow_intent_state.active_intents) == 1

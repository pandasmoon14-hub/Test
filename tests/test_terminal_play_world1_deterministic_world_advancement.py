from __future__ import annotations

import hashlib
import json
from io import StringIO

import pytest

from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
    WORLD1_COMPONENT_CHECKPOINT_COMPONENT_KEYS,
    WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    TOOL_CHEST_ID,
    YARD_ID,
)
from astra_runtime.myravant_terminal import (
    parse_terminal_command,
    run_terminal,
)


def _actor_place(app: MyravantPlayApplication) -> str:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if (
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == GROUNDSKEEPER_ID
        )
    ]
    assert len(matches) == 1
    return matches[0]


def _rewrite_outer_integrity(path):
    envelope = json.loads(path.read_text(encoding="utf-8"))
    payload = envelope["authoritative_payload"]
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    envelope["integrity_digest"] = hashlib.sha256(canonical).hexdigest()
    path.write_text(
        json.dumps(
            envelope,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ),
        encoding="utf-8",
    )


def test_world1_first_actor_and_wait_create_nonplayer_world_change():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    assert app.runtime_state.logical_time_state.logical_position == 0
    assert _actor_place(app) == GATEHOUSE_ID

    app.move("south")
    assert app.runtime_state.logical_time_state.logical_position == 0

    result = app.wait()

    assert result.result_type == "world_advanced"
    assert result.authoritative_changed is True
    assert result.logical_time_before == 0
    assert result.logical_time_after == 1
    assert result.receipt_id is not None
    assert result.consequence_receipt_id is not None
    assert result.due_process_ref is not None
    assert result.spatial_evidence_id is not None
    assert result.opportunity_evidence_id is not None
    assert app.runtime_state.logical_time_state.logical_position == 1
    assert _actor_place(app) == YARD_ID
    view = app.look().view
    assert view is not None
    assert "Groundskeeper" in view.actors
    assert app.authoritative_digest() != before


def test_world1_second_wait_extends_into_world2_without_erasing_first_movement():
    app = MyravantPlayApplication.new()
    first = app.wait()
    second = app.wait()

    assert first.logical_time_after == 1
    assert second.logical_time_after == 2
    assert _actor_place(app) == YARD_ID
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"
    assert second.world_process_action == "open_object"
    assert second.world_process_outcome == "committed"


def test_world1_object_only_routes_do_not_treat_actor_as_object():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()
    results = [
        app.pickup("groundskeeper"),
        app.open_object("groundskeeper"),
        app.light_object("groundskeeper"),
    ]
    assert all(result.authoritative_changed is False for result in results)
    assert app.authoritative_digest() == before


def test_world1_checkpoint_v2_round_trip_preserves_time_and_actor(tmp_path):
    checkpoint = tmp_path / "world1.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.wait()
    before = app.authoritative_digest()
    app.save()

    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert envelope["format_identity"] == COMPONENT_CHECKPOINT_FORMAT_IDENTITY
    assert envelope["format_version"] == WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION
    assert set(envelope["authoritative_payload"]["components"]) == set(
        WORLD1_COMPONENT_CHECKPOINT_COMPONENT_KEYS
    )

    restored = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert restored.authoritative_digest() == before
    assert restored.runtime_state.logical_time_state.logical_position == 1
    assert _actor_place(restored) == YARD_ID

    second = restored.wait()
    assert restored.runtime_state.logical_time_state.logical_position == 2
    assert _actor_place(restored) == YARD_ID
    assert restored.object_open_state(TOOL_CHEST_ID).state == "open"
    assert second.world_process_action == "open_object"


def test_world1_logical_time_semantic_tamper_fails_closed(tmp_path):
    checkpoint = tmp_path / "world1-tamper.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.wait()
    app.save()

    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    envelope["authoritative_payload"]["components"]["logical_time"][
        "logical_position"
    ] = 77
    checkpoint.write_text(
        json.dumps(
            envelope,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ),
        encoding="utf-8",
    )
    _rewrite_outer_integrity(checkpoint)

    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantPlayApplication.restore(checkpoint_path=checkpoint)


def test_world1_terminal_wait_and_actor_rendering():
    assert parse_terminal_command("wait").action == "wait"

    app = MyravantPlayApplication.new()
    output = StringIO()
    exit_code = run_terminal(
        app,
        input_stream=StringIO("go south\nwait\nlook\nexit\n"),
        output_stream=output,
    )
    assert exit_code == 0
    rendered = output.getvalue()
    assert "Time passes." in rendered
    assert "Actors: Groundskeeper" in rendered

"""TERMINAL-PLAY-INT-1 bounded persistent object open/close tests."""

from __future__ import annotations

import hashlib
import json
from io import StringIO

import pytest

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    OBJECT_LIT_STATE_CHECKPOINT_FORMAT_IDENTITY,
    OBJECT_OPEN_CLOSE_CHECKPOINT_FORMAT_IDENTITY,
    PersistentWorldCheckpointEvidenceError,
    write_persistent_world_object_custody_checkpoint,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    digest_persistent_world_object_open_close_runtime_state,
    digest_persistent_world_object_open_states,
    replay_persistent_world_object_open_close_states,
)
from astra_runtime.myravant_live_play_evidence import (
    LivePlayEvidenceRecorder,
    build_live_play_session_header,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    FIXTURE_INITIAL_STATE_DIGEST,
    FIXTURE_INITIAL_WORLD_STATE_DIGEST,
    FIXTURE_VERSION,
    TOOL_CHEST_ID,
    create_terminal_play_fixture,
)
from astra_runtime.myravant_terminal import parse_terminal_command, run_terminal


def _recorder(path, app):
    return LivePlayEvidenceRecorder(
        trace_path=path,
        header=build_live_play_session_header(
            session_id="int1-test",
            campaign_id=app.fixture.campaign_id,
            repository_sha="c" * 40,
            initial_state_digest=app.authoritative_digest(),
            restore_performed=False,
            network_mode="offline",
        ),
    )


def _records(path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_int1_fixture_adds_composite_state_without_redefining_r4b_digest():
    fixture = create_terminal_play_fixture()
    app = MyravantPlayApplication.new(fixture=fixture)

    assert FIXTURE_VERSION == "0.1.3"
    assert fixture.provenance.initial_state_digest == FIXTURE_INITIAL_STATE_DIGEST
    assert (
        fixture.provenance.initial_world_state_digest
        == FIXTURE_INITIAL_WORLD_STATE_DIGEST
    )
    assert app.representation_digest() == FIXTURE_INITIAL_STATE_DIGEST
    assert digest_persistent_world_object_open_close_runtime_state(app.object_state) == (
        FIXTURE_INITIAL_WORLD_STATE_DIGEST
    )
    assert app.authoritative_digest() != FIXTURE_INITIAL_WORLD_STATE_DIGEST
    assert app.authoritative_digest() != app.representation_digest()
    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"


def test_int1_open_close_commits_and_targeted_inspection_reflects_authoritative_state():
    app = MyravantPlayApplication.new()
    app.move("south")

    before = app.authoritative_digest()
    assert "lid is closed" in app.inspect("tool chest").view.description.casefold()

    opened = app.open_object("tool chest")
    assert opened.result_type == "object_state_committed"
    assert opened.authoritative_changed is True
    assert opened.command_id == "terminal-object-state-000001"
    assert opened.command_fingerprint
    assert opened.preview_id
    assert opened.receipt_id
    assert opened.state_delta_id
    assert opened.pre_state_digest == before
    assert opened.post_state_digest == app.authoritative_digest()
    assert opened.post_state_digest != before
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"
    assert "lid is open" in app.inspect("tool chest").view.description.casefold()

    closed_result = app.close_object("tool chest")
    assert closed_result.result_type == "object_state_committed"
    assert closed_result.command_id == "terminal-object-state-000002"
    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"


def test_int1_repeated_transition_is_nonmutating_and_emits_no_commit_artifacts():
    app = MyravantPlayApplication.new()
    app.move("south")
    app.open_object("tool chest")
    before = app.authoritative_digest()
    transition_count = len(
        app.object_state.committed_object_state_transitions
    )

    result = app.open_object("tool chest")

    assert result.result_type == "object_state_unchanged"
    assert result.authoritative_changed is False
    assert result.pre_state_digest == result.post_state_digest == before
    assert result.command_id is None
    assert result.preview_id is None
    assert result.receipt_id is None
    assert result.state_delta_id is None
    assert len(app.object_state.committed_object_state_transitions) == transition_count


def test_int1_remote_declared_and_unknown_targets_are_externally_equivalent():
    remote = MyravantPlayApplication.new().open_object("tool chest")
    unknown = MyravantPlayApplication.new().open_object("sword")

    for result in (remote, unknown):
        assert result.result_type == "object_state_rejected"
        assert result.failure_class == "object_state_target_unavailable"
        assert result.message == "You cannot do that to the target from the current state."
        assert result.authoritative_changed is False
        assert result.command_id is None
        assert result.preview_id is None
        assert result.receipt_id is None
        assert result.state_delta_id is None
        assert result.pre_state_digest == result.post_state_digest

    assert remote.pre_state_digest == unknown.pre_state_digest


def test_int1_open_state_survives_movement_custody_and_save_restore(tmp_path):
    checkpoint = tmp_path / "int1.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.move("south")
    app.open_object("tool chest")
    app.pickup("tool chest")
    app.move("north")

    assert app.object_open_state(TOOL_CHEST_ID).state == "open"
    assert "lid is open" in app.inspect("tool chest").view.description.casefold()

    before_save = app.authoritative_digest()
    saved = app.save()
    assert saved.pre_state_digest == saved.post_state_digest == before_save

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == before_save
    assert restored.object_open_state(TOOL_CHEST_ID).state == "open"
    assert "lid is open" in restored.inspect("tool chest").view.description.casefold()
    assert len(restored.object_state.committed_object_state_transitions) == 1

    closed = restored.close_object("tool chest")
    assert closed.command_id == "terminal-object-state-000002"
    assert restored.object_open_state(TOOL_CHEST_ID).state == "closed"


def test_int1_legacy_r4e_checkpoint_restores_closed_and_upgrades_on_save(tmp_path):
    checkpoint = tmp_path / "legacy-r4e.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.move("south")
    write_persistent_world_object_custody_checkpoint(
        state=app.custody_state,
        checkpoint_path=checkpoint,
        qualification_evidence=app.fixture.checkpoint_qualification,
    )

    legacy = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert legacy["format_identity"] != OBJECT_OPEN_CLOSE_CHECKPOINT_FORMAT_IDENTITY

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.object_open_state(TOOL_CHEST_ID).state == "closed"
    assert "lid is closed" in restored.inspect("tool chest").view.description.casefold()

    restored.save()
    upgraded = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert upgraded["format_identity"] == OBJECT_LIT_STATE_CHECKPOINT_FORMAT_IDENTITY
    assert (
        upgraded["authoritative_payload"]["int1_state"]["object_open_states"][0]["state"]
        == "closed"
    )


def test_int1_recomputed_outer_integrity_cannot_hide_object_state_tamper(tmp_path):
    checkpoint = tmp_path / "tampered-int1.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.move("south")
    app.open_object("tool chest")
    app.save()

    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    envelope["authoritative_payload"]["int1_state"]["object_open_states"][0]["state"] = "closed"
    payload = envelope["authoritative_payload"]
    canonical_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    envelope["integrity_digest"] = hashlib.sha256(canonical_payload).hexdigest()
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

    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantPlayApplication.restore(checkpoint_path=checkpoint)


def test_int1_owner_state_receipt_replays_deterministically():
    app = MyravantPlayApplication.new()
    initial_states = app.object_state.object_open_states
    app.move("south")
    result = app.open_object("tool chest")
    transition = app.object_state.committed_object_state_transitions[0]

    replayed = replay_persistent_world_object_open_close_states(
        object_open_states=initial_states,
        receipt=transition.receipt,
    )
    assert digest_persistent_world_object_open_states(replayed) == (
        transition.receipt.post_state_digest
    )
    assert transition.receipt.command_id == result.command_id
    assert next(x for x in replayed if x.object_entity_id == TOOL_CHEST_ID).state == "open"


def test_int1_parser_routes_open_close_and_preserves_adjacent_frontiers():
    for raw, action, argument in (
        ("open chest", "open", "chest"),
        ("open the tool chest", "open", "tool chest"),
        ("close chest", "close", "chest"),
        ("shut the chest", "close", "chest"),
    ):
        parsed = parse_terminal_command(raw)
        assert parsed.action == action
        assert parsed.argument == argument

    assert parse_terminal_command("open it").action == "ambiguous"
    assert parse_terminal_command("look east").action == "unsupported"
    assert parse_terminal_command("activate lantern").failure_class == (
        "unsupported_capability_object_activation"
    )
    compound = parse_terminal_command("open chest and close chest")
    assert compound.action == "unsupported"
    assert compound.failure_class == "unsupported_compound_intent_sequencing"


def test_int1_terminal_trace_records_composite_commit_and_visible_state(tmp_path):
    trace = tmp_path / "int1-trace.jsonl"
    app = MyravantPlayApplication.new()
    recorder = _recorder(trace, app)
    output = StringIO()

    run_terminal(
        app,
        input_stream=StringIO(
            "move south\ninspect chest\nopen chest\ninspect chest\nexit\n"
        ),
        output_stream=output,
        evidence_recorder=recorder,
    )

    text = output.getvalue().casefold()
    assert "lid is closed" in text
    assert "you open the tool chest" in text
    assert "lid is open" in text

    interactions = [
        row for row in _records(trace)
        if row["record_type"] == "interaction"
    ]
    opened = next(
        row for row in interactions
        if row["result_type"] == "object_state_committed"
    )
    assert opened["parsed_action"] == "open"
    assert opened["authoritative_changed"] is True
    assert opened["command_id"] == "terminal-object-state-000001"
    assert opened["pre_state_digest"] != opened["post_state_digest"]
    assert opened["receipt_id"]
    assert opened["state_delta_id"]

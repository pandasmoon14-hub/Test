"""TERMINAL-PLAY-INT-2 bounded persistent Brass Lantern lit/unlit tests."""

from __future__ import annotations

import hashlib
import json
from io import StringIO

import pytest

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    OBJECT_LIT_STATE_CHECKPOINT_FORMAT_IDENTITY,
    PersistentWorldCheckpointEvidenceError,
    serialize_persistent_world_object_open_close_checkpoint_payload,
    write_persistent_world_object_open_close_checkpoint,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    digest_persistent_world_object_lit_states,
    replay_persistent_world_object_lit_states,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    digest_persistent_world_object_open_close_runtime_state,
    digest_persistent_world_object_open_states,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    FIXTURE_INITIAL_OBJECT_LIT_STATE_DIGEST,
    FIXTURE_INITIAL_STATE_DIGEST,
    FIXTURE_INITIAL_WORLD_STATE_DIGEST,
    FIXTURE_INT2_INITIAL_WORLD_STATE_DIGEST,
    FIXTURE_VERSION,
    LANTERN_ID,
    TOOL_CHEST_ID,
    create_terminal_play_fixture,
)
from astra_runtime.myravant_terminal import parse_terminal_command, run_terminal


def test_int2_fixture_adds_independent_lit_state_without_redefining_lower_digests():
    fixture = create_terminal_play_fixture()
    app = MyravantPlayApplication.new(fixture=fixture)

    assert FIXTURE_VERSION == "0.1.3"
    assert fixture.provenance.initial_state_digest == FIXTURE_INITIAL_STATE_DIGEST
    assert fixture.provenance.initial_world_state_digest == FIXTURE_INITIAL_WORLD_STATE_DIGEST
    assert fixture.provenance.initial_object_lit_state_digest == FIXTURE_INITIAL_OBJECT_LIT_STATE_DIGEST
    assert fixture.provenance.initial_int2_world_state_digest == FIXTURE_INT2_INITIAL_WORLD_STATE_DIGEST
    assert app.representation_digest() == FIXTURE_INITIAL_STATE_DIGEST
    assert digest_persistent_world_object_open_close_runtime_state(app.object_state) == FIXTURE_INITIAL_WORLD_STATE_DIGEST
    assert app.object_lit_state_digest() == FIXTURE_INITIAL_OBJECT_LIT_STATE_DIGEST
    assert app.authoritative_digest() == FIXTURE_INT2_INITIAL_WORLD_STATE_DIGEST
    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"
    assert app.object_lit_state(LANTERN_ID).state == "unlit"


def test_int2_light_extinguish_commits_and_targeted_inspection_reads_state():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()
    assert "flame is out" in app.inspect("lantern").view.description.casefold()

    lit = app.light_object("lantern")
    assert lit.result_type == "object_lit_state_committed"
    assert lit.authoritative_changed is True
    assert lit.command_id == "terminal-object-lit-state-000001"
    assert lit.command_fingerprint
    assert lit.preview_id
    assert lit.receipt_id
    assert lit.state_delta_id
    assert lit.pre_state_digest == before
    assert lit.post_state_digest == app.authoritative_digest()
    assert lit.post_state_digest != before
    assert app.object_lit_state(LANTERN_ID).state == "lit"
    assert "steady flame burns" in app.inspect("lantern").view.description.casefold()

    unlit = app.extinguish_object("lantern")
    assert unlit.result_type == "object_lit_state_committed"
    assert unlit.command_id == "terminal-object-lit-state-000002"
    assert app.object_lit_state(LANTERN_ID).state == "unlit"
    assert "flame is out" in app.inspect("lantern").view.description.casefold()


def test_int2_noops_are_nonmutating_and_emit_no_commit_artifacts():
    unlit_app = MyravantPlayApplication.new()
    before_unlit = unlit_app.authoritative_digest()
    unlit = unlit_app.extinguish_object("lantern")
    assert unlit.result_type == "object_lit_state_unchanged"
    assert unlit.pre_state_digest == unlit.post_state_digest == before_unlit
    assert unlit.command_id is None
    assert unlit.preview_id is None
    assert unlit.receipt_id is None
    assert unlit.state_delta_id is None

    lit_app = MyravantPlayApplication.new()
    lit_app.light_object("lantern")
    before_lit = lit_app.authoritative_digest()
    transition_count = len(lit_app.lit_state.committed_object_lit_transitions)
    repeated = lit_app.light_object("lantern")
    assert repeated.result_type == "object_lit_state_unchanged"
    assert repeated.pre_state_digest == repeated.post_state_digest == before_lit
    assert repeated.command_id is None
    assert len(lit_app.lit_state.committed_object_lit_transitions) == transition_count


def test_int2_remote_and_unknown_targets_are_externally_equivalent():
    remote_app = MyravantPlayApplication.new()
    remote_app.move("south")
    remote = remote_app.light_object("lantern")
    unknown = MyravantPlayApplication.new().light_object("sword")

    for result in (remote, unknown):
        assert result.result_type == "object_lit_state_rejected"
        assert result.failure_class == "object_lit_state_target_unavailable"
        assert result.message == "You cannot do that to the target from the current state."
        assert result.authoritative_changed is False
        assert result.command_id is None
        assert result.preview_id is None
        assert result.receipt_id is None
        assert result.state_delta_id is None
        assert result.pre_state_digest == result.post_state_digest


def test_int2_locally_visible_object_without_lit_state_reports_not_supported():
    app = MyravantPlayApplication.new()
    app.move("south")
    result = app.light_object("tool chest")
    assert result.result_type == "object_lit_state_rejected"
    assert result.failure_class == "object_lit_state_not_supported"
    assert result.authoritative_changed is False


def test_int2_state_families_change_independently():
    app = MyravantPlayApplication.new()
    open_digest_before = app.object_state_digest()
    lit_digest_before = app.object_lit_state_digest()

    app.light_object("lantern")
    lit_digest_after_light = app.object_lit_state_digest()
    assert app.object_state_digest() == open_digest_before
    assert lit_digest_after_light != lit_digest_before

    app.move("south")
    app.open_object("tool chest")
    assert app.object_state_digest() != open_digest_before
    assert app.object_lit_state_digest() == lit_digest_after_light


def test_int2_composes_lighting_custody_movement_open_close_and_restore(tmp_path):
    checkpoint = tmp_path / "int2-composition.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    app.light_object("lantern")
    app.pickup("lantern")
    app.move("south")
    app.open_object("tool chest")
    before_save = app.authoritative_digest()
    app.save()

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == before_save
    assert restored.object_lit_state(LANTERN_ID).state == "lit"
    assert restored.object_open_state(TOOL_CHEST_ID).state == "open"
    assert "steady flame burns" in restored.inspect("lantern").view.description.casefold()
    assert "lid is open" in restored.inspect("tool chest").view.description.casefold()

    restored.extinguish_object("lantern")
    restored.close_object("tool chest")
    restored.drop("lantern")
    restored.save()

    final = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert final.object_lit_state(LANTERN_ID).state == "unlit"
    assert final.object_open_state(TOOL_CHEST_ID).state == "closed"
    assert final.current_place_id().endswith(":yard")
    assert "Brass Lantern" in final.look().view.objects
    assert len(final.state.committed_transitions) == 1
    assert len(final.custody_state.committed_custody_transitions) == 2
    assert len(final.object_state.committed_object_state_transitions) == 2
    assert len(final.lit_state.committed_object_lit_transitions) == 2


def test_int2_checkpoint_embeds_exact_int1_payload(tmp_path):
    checkpoint = tmp_path / "int2-exact-int1.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.light_object("lantern")
    app.pickup("lantern")
    app.move("south")
    app.open_object("tool chest")
    app.save()

    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert envelope["format_identity"] == OBJECT_LIT_STATE_CHECKPOINT_FORMAT_IDENTITY
    assert envelope["authoritative_payload"]["int1_state"] == (
        serialize_persistent_world_object_open_close_checkpoint_payload(app.object_state)
    )


def test_int2_legacy_int1_restore_initializes_lantern_unlit_and_upgrades(tmp_path):
    checkpoint = tmp_path / "legacy-int1.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.move("south")
    app.open_object("tool chest")
    write_persistent_world_object_open_close_checkpoint(
        state=app.object_state,
        checkpoint_path=checkpoint,
        qualification_evidence=app.fixture.checkpoint_qualification,
    )

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.object_open_state(TOOL_CHEST_ID).state == "open"
    assert restored.object_lit_state(LANTERN_ID).state == "unlit"
    restored.save()
    upgraded = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert upgraded["format_identity"] == OBJECT_LIT_STATE_CHECKPOINT_FORMAT_IDENTITY


def test_int2_recomputed_outer_integrity_cannot_hide_lit_state_tamper(tmp_path):
    checkpoint = tmp_path / "tampered-int2.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.light_object("lantern")
    app.save()

    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    envelope["authoritative_payload"]["object_lit_states"][0]["state"] = "unlit"
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


def test_int2_owner_receipt_replays_deterministically():
    app = MyravantPlayApplication.new()
    initial_states = app.lit_state.object_lit_states
    result = app.light_object("lantern")
    transition = app.lit_state.committed_object_lit_transitions[0]

    replayed = replay_persistent_world_object_lit_states(
        object_lit_states=initial_states,
        receipt=transition.receipt,
    )
    assert digest_persistent_world_object_lit_states(replayed) == transition.receipt.post_state_digest
    assert transition.receipt.command_id == result.command_id
    assert next(x for x in replayed if x.object_entity_id == LANTERN_ID).state == "lit"


def test_int2_parser_routes_bounded_lit_state_and_preserves_adjacent_frontiers():
    for raw, action, argument in (
        ("light lantern", "light", "lantern"),
        ("light the lantern", "light", "lantern"),
        ("ignite lantern", "light", "lantern"),
        ("ignite the lantern", "light", "lantern"),
        ("extinguish lantern", "extinguish", "lantern"),
        ("extinguish the lantern", "extinguish", "lantern"),
    ):
        parsed = parse_terminal_command(raw)
        assert parsed.action == action
        assert parsed.argument == argument

    assert parse_terminal_command("light it").action == "ambiguous"
    assert parse_terminal_command("activate lantern").failure_class == (
        "unsupported_capability_object_activation"
    )
    compound = parse_terminal_command("light lantern and move south")
    assert compound.action == "unsupported"
    assert compound.failure_class == "unsupported_compound_intent_sequencing"


def test_int2_terminal_routes_lighting_and_inspection_without_ambient_look_claims():
    app = MyravantPlayApplication.new()
    output = StringIO()
    run_terminal(
        app,
        input_stream=StringIO(
            "inspect lantern\nlight the lantern\ninspect lantern\nextinguish lantern\ninspect lantern\nexit\n"
        ),
        output_stream=output,
    )
    text = output.getvalue().casefold()
    assert "flame is out" in text
    assert "you light the brass lantern" in text
    assert "steady flame burns" in text
    assert "you extinguish the brass lantern" in text
    assert app.object_lit_state(LANTERN_ID).state == "unlit"

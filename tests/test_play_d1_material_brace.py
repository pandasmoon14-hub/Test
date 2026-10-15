"""D-1 playable structural alteration, time, resource and replay evidence."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys

import pytest

from astra_runtime.domain.persistent_world_d1_checkpoint import D1_VERSION
from astra_runtime.domain.persistent_world_fixture_brace import (
    BRACE_ID, FixtureBraceError, FixtureBraceState,
    digest_fixture_brace, execute_fixture_brace, restore_fixture_brace,
    serialize_fixture_brace,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError, _canonical_bytes,
)
from astra_runtime.myravant_d1_brace_goal import parse_d1_brace
from astra_runtime.myravant_play_fixture import GROUNDSKEEPER_ID, YARD_ID
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _yard(app):
    assert app.move("south").authoritative_changed
    assert app.current_place_id() == YARD_ID


def _remove_manual(app):
    first = app.alter_chest_brace("manual")
    assert first.authoritative_changed
    assert first.preview_id and first.receipt_id and first.state_delta_id
    assert first.preview_id == app.brace_state.events[0].preview_id
    assert first.state_delta_id == app.brace_state.events[0].state_delta_id
    assert first.consequence_receipt_id
    assert first.logical_time_after == first.logical_time_before + 1
    assert app.brace_state.condition == "loosened"
    second = app.alter_chest_brace("manual")
    assert second.authoritative_changed
    assert second.logical_time_after == second.logical_time_before + 1
    assert app.brace_state.condition == "detached_at_yard"
    assert len(app.brace_state.events) == 2
    return first, second


def test_manual_two_stage_material_alteration_changes_later_latch_opportunity(tmp_path):
    checkpoint = tmp_path / "d1-manual.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _yard(app)
    pre = app.authoritative_digest()
    first, second = _remove_manual(app)
    assert first.pre_state_digest == pre
    assert second.post_state_digest == app.authoritative_digest()
    assert BRACE_ID in str(serialize_fixture_brace(app.brace_state))
    assert serialize_fixture_brace(app.brace_state)["quantity"] == 1
    inspection = app.inspect_chest_brace()
    assert not inspection.authoritative_changed
    assert "detached at yard" in inspection.message
    assert inspection.pre_state_digest == inspection.post_state_digest

    # The older B-2a service remains lawful, but cannot secure a chest with
    # a removed structural component. No illegal attempt spends another tick.
    assert app.service_chest_latch("work", method="manual").authoritative_changed
    assert app.service_chest_latch("work", method="manual").authoritative_changed
    before = app.authoritative_digest()
    denied = app.service_chest_latch("secure")
    assert denied.failure_class == "fixture_service_brace_not_attached"
    assert app.authoritative_digest() == before

    assert app.save().checkpoint_digest
    saved = json.loads(checkpoint.read_text())
    assert saved["format_version"] == D1_VERSION
    assert saved["authoritative_payload"]["components"]["fixture_brace"]["quantity"] == 1
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.service_state.progress == 2
    assert restored.brace_state.condition == "detached_at_yard"
    fitted = restored.alter_chest_brace("refit")
    assert fitted.authoritative_changed
    assert restored.brace_state.condition == "attached"
    assert restored.service_chest_latch("secure").authoritative_changed
    assert restored.service_state.secured
    restored.save()
    reread = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert reread.authoritative_digest() == restored.authoritative_digest()
    assert reread.brace_state.condition == "attached"
    assert reread.service_state.secured
    assert len(reread.brace_state.events) == 3


def test_lantern_method_is_genuinely_distinct_opportunity_and_work_time(tmp_path):
    checkpoint = tmp_path / "d1-lantern.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _yard(app)
    before = app.authoritative_digest()
    denied = app.alter_chest_brace("lantern")
    assert denied.failure_class == "fixture_brace_instrument_unavailable"
    assert app.authoritative_digest() == before

    # Illuminate the physical worksite with the existing movable Lantern.
    assert app.move("north").authoritative_changed
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.drop("lantern").authoritative_changed
    assert app.light_object("lantern").authoritative_changed
    original_tick = app.runtime_state.logical_time_state.logical_position
    lit = app.alter_chest_brace("lantern")
    assert lit.authoritative_changed
    assert lit.logical_time_after == original_tick + 1
    assert app.brace_state.condition == "detached_at_yard"
    assert len(app.brace_state.events) == 1
    assert app.brace_state.events[0].method == "lantern"
    assert app.save().checkpoint_digest
    reread = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert reread.authoritative_digest() == app.authoritative_digest()
    assert reread.brace_state.condition == "detached_at_yard"


def test_refusal_preserves_state_for_remote_worksite_and_incompatible_method():
    app = MyravantVSM14Application.new()
    before = app.authoritative_digest()
    refusal = app.alter_chest_brace("manual")
    assert refusal.failure_class == "fixture_brace_worksite_unavailable"
    assert app.authoritative_digest() == before
    _yard(app)
    before = app.authoritative_digest()
    refusal = app.alter_chest_brace("refit")
    assert refusal.failure_class == "fixture_brace_method_unavailable"
    assert app.authoritative_digest() == before
    _remove_manual(app)
    before = app.authoritative_digest()
    refusal = app.alter_chest_brace("manual")
    assert refusal.failure_class == "fixture_brace_method_unavailable"
    assert app.authoritative_digest() == before
    assert app.alter_chest_brace("refit").authoritative_changed
    before = app.authoritative_digest()
    assert app.alter_chest_brace("refit").failure_class == "fixture_brace_method_unavailable"
    assert app.authoritative_digest() == before


def test_historical_v5_and_v7_restore_and_cross_family_v8(tmp_path):
    file_v5 = tmp_path / "legacy-v5.json"
    app = MyravantVSM14Application.new(checkpoint_path=file_v5)
    assert app.save().checkpoint_digest
    assert json.loads(file_v5.read_text())["format_version"] == 5
    old = MyravantVSM14Application.restore(checkpoint_path=file_v5)
    assert old.brace_state == FixtureBraceState()
    assert old.authoritative_digest() == app.authoritative_digest()

    combined = tmp_path / "d1-combined.json"
    app = MyravantVSM14Application.new(checkpoint_path=combined)
    _yard(app)
    assert app.wait().authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    seen = app.actor_memory_interaction("witness", "chest")
    assert seen.authoritative_changed
    assert app.save().checkpoint_digest
    assert json.loads(combined.read_text())["format_version"] == 7
    recovered = MyravantVSM14Application.restore(checkpoint_path=combined)
    assert recovered.knowledge_state.events == app.knowledge_state.events
    assert recovered.brace_state == FixtureBraceState()

    work = app.alter_chest_brace("manual")
    assert work.authoritative_changed
    app.save()
    assert json.loads(combined.read_text())["format_version"] == D1_VERSION
    last = MyravantVSM14Application.restore(checkpoint_path=combined)
    assert last.authoritative_digest() == app.authoritative_digest()
    assert last.knowledge_state.events == app.knowledge_state.events
    assert last.brace_state.condition == "loosened"


def test_replay_refuses_rehashed_payload_corruption_and_fake_parts(tmp_path):
    checkpoint = tmp_path / "d1-corrupt.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _yard(app)
    _remove_manual(app)
    app.save()
    original = checkpoint.read_bytes()

    def mutated(update):
        envelope = json.loads(original)
        material = envelope["authoritative_payload"]["components"]["fixture_brace"]
        update(material)
        envelope["integrity_digest"] = hashlib.sha256(_canonical_bytes(
            envelope["authoritative_payload"]
        )).hexdigest()
        checkpoint.write_bytes(_canonical_bytes(envelope))
        with pytest.raises(PersistentWorldCheckpointEvidenceError):
            MyravantVSM14Application.restore(checkpoint_path=checkpoint)

    mutated(lambda m: m.__setitem__("quantity", 2))
    mutated(lambda m: m.__setitem__("condition", "attached"))
    mutated(lambda m: m["events"][0].__setitem__("after_condition", "detached_at_yard"))
    mutated(lambda m: m["events"][1].__setitem__(
        "time_receipt_id", m["events"][0]["time_receipt_id"]
    ))
    checkpoint.write_bytes(original)
    assert MyravantVSM14Application.restore(
        checkpoint_path=checkpoint
    ).authoritative_digest() == app.authoritative_digest()


def test_direct_owner_rejects_forged_clock_and_duplicate_command():
    state = FixtureBraceState()
    with pytest.raises(FixtureBraceError):
        execute_fixture_brace(
            state=state, command_id="terminal-fixture-brace-000001",
            method="manual", actor_id="astra:entity:terminal-traveler",
            object_id="astra:entity:tool-chest", component_id=BRACE_ID,
            place_id=YARD_ID, logical_before=1, logical_after=1,
            time_receipt_id="forged", source_world_digest="a"*64,
            expected_pre_digest=digest_fixture_brace(state), qualified=True,
        )
    broken = serialize_fixture_brace(state)
    broken["quantity"] = 0
    with pytest.raises(FixtureBraceError):
        restore_fixture_brace(broken)


def test_installed_two_sessions_resume_material_work_and_durable_acks(tmp_path):
    checkpoint = tmp_path / "d1-terminal.json"

    def run(commands, *args):
        return subprocess.run(
            [sys.executable, "-m", "astra_runtime.myravant_terminal", *args],
            input="\n".join((*commands, "exit", "")),
            text=True, capture_output=True, timeout=90,
        )

    first = run((
        "go south", "remove chest brace", "check chest brace",
        "exit",
    ), "--checkpoint", str(checkpoint))
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "loosened" in first.stdout
    assert json.loads(checkpoint.read_text())["format_version"] == 8

    second = run((
        "resume removing chest brace", "inspect chest brace",
        "reinstall chest brace", "inspect chest brace",
    ), "--load", str(checkpoint))
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert "detached at yard" in second.stdout
    assert "attached" in second.stdout
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.brace_state.condition == "attached"
    assert len(restored.brace_state.events) == 3


def test_parser_keeps_alternatives_distinct_from_existing_service_and_c():
    assert parse_d1_brace("remove chest brace") == "manual"
    assert parse_d1_brace("remove chest brace with lantern") == "lantern"
    assert parse_d1_brace("tighten chest brace") == "refit"
    assert parse_d1_brace("inspect chest brace") == "inspect"
    for unrelated in (
        "service chest latch", "ask groundskeeper to inspect chest",
        "clear waystone route", "remove chest", "remove lantern",
        "repair chest latch",
    ):
        assert parse_d1_brace(unrelated) is None

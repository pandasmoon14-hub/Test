"""PLAY-E2: grounded NPC labor alternative with real assets and v10 replay."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys

import pytest

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError, _canonical_bytes,
)
from astra_runtime.myravant_e1_checkpoint import (
    E1_VERSION, E2_VERSION, has_e2_npc_work,
)
from astra_runtime.myravant_e2_actor_service_goal import parse_e2_actor_service
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, LANTERN_ID, YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _worksite(app):
    assert app.move("south").authoritative_changed
    assert app.wait().authoritative_changed
    assert app.current_place_id() == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID


def _supply_lantern(app):
    assert app.move("north").authoritative_changed
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.drop("lantern").authoritative_changed
    assert app.light_object("lantern").authoritative_changed


def test_npc_performs_real_work_with_resource_and_distinct_time(tmp_path):
    checkpoint = tmp_path / "e2-lantern.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _worksite(app)
    before = app.authoritative_digest()
    denial = app.request_groundskeeper_latch_work()
    assert denial.failure_class == "actor_service_instrument_unavailable"
    assert not denial.authoritative_changed
    assert app.authoritative_digest() == before

    _supply_lantern(app)
    before_step = app.runtime_state.logical_time_state.logical_position
    changed = app.request_groundskeeper_latch_work()
    assert changed.authoritative_changed
    assert changed.command_id and changed.preview_id
    assert changed.receipt_id and changed.state_delta_id
    assert changed.consequence_receipt_id
    assert changed.logical_time_after == before_step + 1
    assert app.service_state.progress == 2
    assert not app.service_state.secured
    assert app.service_state.events[-1].actor_id == GROUNDSKEEPER_ID
    assert app.service_state.events[-1].method == "lantern"
    assert app.service_state.events[-1].time_receipt_id == changed.consequence_receipt_id
    assert has_e2_npc_work(app.service_state)
    assert app.save().checkpoint_digest
    assert json.loads(checkpoint.read_text())["format_version"] == E2_VERSION
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.service_state.events == app.service_state.events


def test_alternative_player_manual_method_remains_distinct(tmp_path):
    npc = MyravantVSM14Application.new(
        checkpoint_path=tmp_path / "e2-npc.json"
    )
    _worksite(npc)
    _supply_lantern(npc)
    started = npc.runtime_state.logical_time_state.logical_position
    assert npc.request_groundskeeper_latch_work().authoritative_changed
    assert npc.runtime_state.logical_time_state.logical_position == started + 1

    player = MyravantVSM14Application.new(
        checkpoint_path=tmp_path / "e2-player.json"
    )
    assert player.move("south").authoritative_changed
    first = player.service_chest_latch("work", method="manual")
    second = player.service_chest_latch("work", method="manual")
    assert first.authoritative_changed and second.authoritative_changed
    assert player.service_state.progress == 2
    assert len(player.service_state.events) == 2
    assert all(x.actor_id != GROUNDSKEEPER_ID for x in player.service_state.events)
    assert not has_e2_npc_work(player.service_state)
    player.save()
    assert json.loads(player.checkpoint_path.read_text())["format_version"] == 6


def test_npc_work_then_e1_delayed_secure_and_legacy_replay(tmp_path):
    checkpoint = tmp_path / "e2-composed.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _worksite(app)
    _supply_lantern(app)
    assert app.request_groundskeeper_latch_work().authoritative_changed
    assert app.close_object("chest").authoritative_changed
    offer = app.groundskeeper_chest_duty("request")
    assert offer.authoritative_changed
    assert app.duty_state.status == "pending"
    app.save()
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.wait().authoritative_changed
    assert restored.duty_state.status == "fulfilled"
    assert restored.service_state.secured
    assert restored.open_object("chest").failure_class == "fixture_service_latch_secured"
    restored.save()
    again = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert again.authoritative_digest() == restored.authoritative_digest()
    assert len(again.service_state.events) == 2
    assert again.service_state.events[0].operation == "work"
    assert again.service_state.events[1].operation == "secure"


def test_remote_actor_wrong_resource_and_completed_work_refuse_without_tick():
    app = MyravantVSM14Application.new()
    pre = app.authoritative_digest()
    assert app.request_groundskeeper_latch_work().failure_class == (
        "actor_service_worksite_not_local"
    )
    assert app.authoritative_digest() == pre
    assert app.move("south").authoritative_changed
    pre = app.authoritative_digest()
    assert app.request_groundskeeper_latch_work().failure_class == (
        "actor_service_actor_not_local"
    )
    assert app.authoritative_digest() == pre
    assert app.wait().authoritative_changed
    _supply_lantern(app)
    assert app.extinguish_object("lantern").authoritative_changed
    pre = app.authoritative_digest()
    assert app.request_groundskeeper_latch_work().failure_class == (
        "actor_service_instrument_unavailable"
    )
    assert app.authoritative_digest() == pre
    assert app.light_object("lantern").authoritative_changed
    pre = app.authoritative_digest()
    assert app.request_groundskeeper_latch_work(method="manual").failure_class == (
        "actor_service_method_unavailable"
    )
    assert app.authoritative_digest() == pre
    assert app.request_groundskeeper_latch_work().authoritative_changed
    pre = app.authoritative_digest()
    assert app.request_groundskeeper_latch_work().failure_class == (
        "actor_service_opportunity_unavailable"
    )
    assert app.authoritative_digest() == pre


def test_v10_rehashed_forged_actor_work_receipt_cannot_restore(tmp_path):
    checkpoint = tmp_path / "e2-corrupt.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _worksite(app)
    _supply_lantern(app)
    assert app.request_groundskeeper_latch_work().authoritative_changed
    app.save()
    envelope = json.loads(checkpoint.read_text())
    service = envelope["authoritative_payload"]["components"]["fixture_service"]
    service["events"][0]["time_receipt_id"] = "forged-work-receipt"
    envelope["integrity_digest"] = hashlib.sha256(
        _canonical_bytes(envelope["authoritative_payload"])
    ).hexdigest()
    checkpoint.write_bytes(_canonical_bytes(envelope))
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantVSM14Application.restore(checkpoint_path=checkpoint)


def test_v9_cannot_claim_e2_work_by_version_downgrade(tmp_path):
    checkpoint = tmp_path / "e2-downgrade.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _worksite(app)
    _supply_lantern(app)
    assert app.request_groundskeeper_latch_work().authoritative_changed
    app.save()
    material = json.loads(checkpoint.read_text())
    material["format_version"] = E1_VERSION
    checkpoint.write_bytes(_canonical_bytes(material))
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantVSM14Application.restore(checkpoint_path=checkpoint)


def test_installed_two_session_player_supplied_npc_work(tmp_path):
    checkpoint = tmp_path / "e2-installed.json"

    def run(commands, *args):
        return subprocess.run(
            [sys.executable, "-m", "astra_runtime.myravant_terminal", *args],
            input="\n".join((*commands, "exit", "")),
            text=True, capture_output=True, timeout=90,
        )

    first = run((
        "go south", "wait", "go north", "take lantern", "go south",
        "drop lantern", "light lantern",
        "ask groundskeeper to repair chest latch with lantern",
        "check chest latch service",
    ), "--checkpoint", str(checkpoint))
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "Groundskeeper makes" in first.stdout
    assert "serviceable" in first.stdout
    assert json.loads(checkpoint.read_text())["format_version"] == E2_VERSION

    second = run((
        "close chest", "ask groundskeeper to secure chest latch later",
        "go north", "wait", "go south", "check chest duty", "open chest",
        "release chest latch", "open chest",
    ), "--load", str(checkpoint))
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert "fulfilled" in second.stdout
    assert "secured" in second.stdout
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.duty_state.status == "fulfilled"
    assert not restored.service_state.secured


def test_npc_work_parser_does_not_capture_general_communication():
    assert parse_e2_actor_service(
        "ask groundskeeper to repair chest latch with lantern"
    ) == "lantern"
    assert parse_e2_actor_service(
        "request groundskeeper to service chest latch using lantern"
    ) == "lantern"
    for unrelated in (
        "ask groundskeeper to go south",
        "ask groundskeeper to secure chest latch later",
        "repair chest latch",
        "service chest latch with lantern",
        "ask groundskeeper to examine chest",
        "request work from another villager",
        "ask groundskeeper to repair other object with lantern",
    ):
        assert parse_e2_actor_service(unrelated) is None

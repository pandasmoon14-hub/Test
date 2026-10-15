"""PLAY-E1: one voluntary, delayed, resource-qualified NPC obligation.

Tests demand real public execution, offscreen no-leak, v9 recovery and a
fixture-local lawfully refused alternative without inventing NPC commerce.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import replace

import pytest

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError, _canonical_bytes,
)
from astra_runtime.myravant_e1_checkpoint import E1_VERSION
from astra_runtime.myravant_e1_duty_goal import parse_e1_latch_duty
from astra_runtime.myravant_e1_latch_duty import (
    FixtureDutyError, FixtureDutyState, digest_fixture_duty,
    execute_fixture_duty, restore_fixture_duty, serialize_fixture_duty,
)
from astra_runtime.myravant_play_fixture import YARD_ID
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _ready(app):
    assert app.move("south").authoritative_changed
    assert app.current_place_id() == YARD_ID
    assert app.service_chest_latch("work", method="manual").authoritative_changed
    assert app.service_chest_latch("work", method="manual").authoritative_changed
    assert app.service_state.progress == 2
    # WORLD-2's second tick opens the chest. The physical closed condition is
    # required for voluntary future securing and is a real separate operation.
    assert app.close_object("chest").authoritative_changed
    assert app.object_open_state(
        app.fixture.resolve_object_reference("chest")
    ).state == "closed"


def test_duty_requires_real_local_actor_and_unspent_resources():
    app = MyravantVSM14Application.new()
    pre = app.authoritative_digest()
    denied = app.groundskeeper_chest_duty("request")
    assert denied.failure_class == "fixture_duty_worksite_not_local"
    assert app.authoritative_digest() == pre
    assert app.move("south").authoritative_changed
    pre = app.authoritative_digest()
    assert app.groundskeeper_chest_duty("request").failure_class == (
        "fixture_duty_actor_not_local"
    )
    assert app.authoritative_digest() == pre
    assert app.wait().authoritative_changed  # Groundskeeper at Yard
    pre = app.authoritative_digest()
    denied = app.groundskeeper_chest_duty("request")
    assert denied.failure_class == "fixture_duty_resources_unavailable"
    assert app.authoritative_digest() == pre
    assert not app.duty_state.events


def test_accepted_duty_changes_later_chest_opportunity_after_departure(tmp_path):
    checkpoint = tmp_path / "e1-offscreen.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _ready(app)
    offer = app.groundskeeper_chest_duty("request")
    assert offer.authoritative_changed
    assert offer.preview_id and offer.receipt_id and offer.state_delta_id
    assert offer.pre_state_digest != offer.post_state_digest
    assert app.duty_state.status == "pending"
    assert not app.service_state.secured
    assert app.save().checkpoint_digest
    assert json.loads(checkpoint.read_text())["format_version"] == E1_VERSION
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.duty_state.status == "pending"

    assert restored.move("north").authoritative_changed
    remote = restored.groundskeeper_chest_duty("check")
    assert remote.failure_class == "fixture_duty_worksite_not_local"
    advanced = restored.wait()
    assert advanced.authoritative_changed
    assert advanced.message == "Time passes."
    assert advanced.pre_state_digest != advanced.post_state_digest
    assert restored.duty_state.status == "fulfilled"
    assert restored.service_state.secured
    assert restored.service_state.events[-1].actor_id.endswith("groundskeeper")
    assert restored.duty_state.events[-1].service_receipt_id == (
        restored.service_state.events[-1].receipt_id
    )
    assert restored.duty_state.events[-1].time_receipt_id == advanced.receipt_id
    assert restored.move("south").authoritative_changed
    assert "fulfilled" in restored.groundskeeper_chest_duty("check").message
    before = restored.authoritative_digest()
    denied = restored.open_object("chest")
    assert denied.failure_class == "fixture_service_latch_secured"
    assert restored.authoritative_digest() == before
    assert restored.service_chest_latch("release").authoritative_changed
    assert restored.open_object("chest").authoritative_changed
    restored.save()
    reread = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert reread.authoritative_digest() == restored.authoritative_digest()
    assert reread.duty_state.status == "fulfilled"
    assert not reread.service_state.secured


def test_cancelled_and_duplicate_offers_never_commit_phantom_work(tmp_path):
    checkpoint = tmp_path / "e1-cancel.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _ready(app)
    assert app.groundskeeper_chest_duty("request").authoritative_changed
    pre = app.authoritative_digest()
    denied = app.groundskeeper_chest_duty("request")
    assert denied.failure_class == "fixture_duty_opportunity_unavailable"
    assert app.authoritative_digest() == pre
    assert app.groundskeeper_chest_duty("cancel").authoritative_changed
    assert app.duty_state.status == "cancelled"
    assert app.move("north").authoritative_changed
    assert app.wait().authoritative_changed
    assert not app.service_state.secured
    assert app.duty_state.status == "cancelled"
    app.save()
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()


def test_missing_chest_blocks_agreed_duty_and_preserves_pending(tmp_path):
    checkpoint = tmp_path / "e1-chest-absent.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _ready(app)
    assert app.groundskeeper_chest_duty("request").authoritative_changed
    # COMP-3 owns actual position; a promise does not teleport a target.
    assert app.displace_object("chest", "north", method="push").authoritative_changed
    assert app.wait().authoritative_changed
    assert app.duty_state.status == "pending"
    assert not app.service_state.secured
    app.save()
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.duty_state.status == "pending"


def test_v9_rejects_rehashed_causal_receipt_forgery(tmp_path):
    checkpoint = tmp_path / "e1-tampered.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _ready(app)
    assert app.groundskeeper_chest_duty("request").authoritative_changed
    assert app.wait().authoritative_changed
    assert app.duty_state.status == "fulfilled"
    app.save()
    assert MyravantVSM14Application.restore(
        checkpoint_path=checkpoint
    ).authoritative_digest() == app.authoritative_digest()
    envelope = json.loads(checkpoint.read_text())
    duty_event = envelope["authoritative_payload"]["components"]["fixture_duty"]["events"][-1]
    duty_event["service_receipt_id"] = "forged-service"
    envelope["integrity_digest"] = hashlib.sha256(
        _canonical_bytes(envelope["authoritative_payload"])
    ).hexdigest()
    # Keep the outer envelope canonical so the v9 causal owner is exercised,
    # rather than letting the earlier byte-format guard reject the fixture.
    checkpoint.write_bytes(_canonical_bytes(envelope))
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantVSM14Application.restore(checkpoint_path=checkpoint)


def test_v9_rejects_cross_owner_alias_even_after_owner_replay(tmp_path, monkeypatch):
    from astra_runtime import myravant_e1_checkpoint as adapter

    checkpoint = tmp_path / "e1-alias.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _ready(app)
    assert app.groundskeeper_chest_duty("request").authoritative_changed
    app.save()
    assert MyravantVSM14Application.restore(
        checkpoint_path=checkpoint
    ).authoritative_digest() == app.authoritative_digest()
    previous = adapter.restore_fixture_duty
    collision = app.runtime_state.movement_state.committed_transitions[0].command_id

    def rewritten(material):
        original = previous(material)
        event = replace(original.events[0], command_id=collision)
        return replace(original, events=(event, *original.events[1:]))

    monkeypatch.setattr(adapter, "restore_fixture_duty", rewritten)
    with pytest.raises(PersistentWorldCheckpointEvidenceError, match="duty identity"):
        MyravantVSM14Application.restore(checkpoint_path=checkpoint)



def test_v9_replay_rejects_retroactive_fulfillment_before_agreement(
    tmp_path, monkeypatch,
):
    """Even an owner-returned coherent event cannot borrow a pre-request tick.

    Isolate the cross-owner causal boundary by changing the reconstructed duty
    record, rather than relying on the owner's fingerprint gate to reject it.
    """
    from astra_runtime import myravant_e1_checkpoint as adapter

    checkpoint = tmp_path / "e1-retroactive-tick.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _ready(app)
    accepted = app.groundskeeper_chest_duty("request")
    assert accepted.authoritative_changed
    finished = app.wait()
    assert finished.authoritative_changed
    assert app.duty_state.status == "fulfilled"
    app.save()
    assert MyravantVSM14Application.restore(
        checkpoint_path=checkpoint
    ).authoritative_digest() == app.authoritative_digest()

    original_restore = adapter.restore_fixture_duty

    def retroactive_request(material):
        duty = original_restore(material)
        # Pretend the original request happened only when fulfillment was
        # recorded. The WORLD-2 receipt then precedes consent, which is
        # forbidden despite otherwise consistent service and tick receipts.
        first = replace(
            duty.events[0], logical_step=duty.events[-1].logical_step,
        )
        return replace(duty, events=(first, *duty.events[1:]))

    monkeypatch.setattr(adapter, "restore_fixture_duty", retroactive_request)
    with pytest.raises(
        PersistentWorldCheckpointEvidenceError,
        match="no causal NPC service and WORLD-2 tick",
    ):
        MyravantVSM14Application.restore(checkpoint_path=checkpoint)


def test_owner_qualifies_replay_and_no_result_without_real_receipts():
    state = FixtureDutyState()
    with pytest.raises(FixtureDutyError):
        execute_fixture_duty(
            state=state, command_id="e1-forged", operation="fulfill",
            logical_step=1, expected_pre_digest=digest_fixture_duty(state),
            qualified=True,
        )
    with pytest.raises(FixtureDutyError):
        execute_fixture_duty(
            state=state, command_id="e1-forged", operation="request",
            logical_step=1, expected_pre_digest=digest_fixture_duty(state),
            qualified=False,
        )
    bad = serialize_fixture_duty(state)
    bad["status"] = "fulfilled"
    with pytest.raises(FixtureDutyError):
        restore_fixture_duty(bad)


def test_installed_terminal_two_sessions_offscreen_duty_and_ack(tmp_path):
    checkpoint = tmp_path / "e1-terminal.json"

    def run(commands, *args):
        return subprocess.run(
            [sys.executable, "-m", "astra_runtime.myravant_terminal", *args],
            input="\n".join((*commands, "exit", "")),
            text=True, capture_output=True, timeout=90,
        )

    first = run((
        "go south", "service chest latch", "service chest latch",
        "close chest", "ask groundskeeper to secure chest latch later",
        "go north",
    ), "--checkpoint", str(checkpoint))
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "agrees to secure" in first.stdout
    assert json.loads(checkpoint.read_text())["format_version"] == 9
    second = run((
        "check chest duty", "wait", "go south", "check chest duty",
        "open chest", "release chest latch", "open chest",
    ), "--load", str(checkpoint))
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert "fulfilled" in second.stdout
    assert "secured" in second.stdout
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.duty_state.status == "fulfilled"
    assert not restored.service_state.secured


def test_duty_parser_distinguishes_work_handoff_and_general_request():
    assert parse_e1_latch_duty(
        "ask groundskeeper to secure chest latch later"
    ) == "request"
    assert parse_e1_latch_duty("cancel groundskeeper chest duty") == "cancel"
    assert parse_e1_latch_duty("check chest duty") == "check"
    for unrelated in (
        "ask groundskeeper to open chest",
        "ask groundskeeper to go south",
        "service chest latch",
        "ask groundskeeper for lantern",
        "give lantern to groundskeeper",
        "repair chest brace",
        "ask some stranger to secure a door",
    ):
        assert parse_e1_latch_duty(unrelated) is None

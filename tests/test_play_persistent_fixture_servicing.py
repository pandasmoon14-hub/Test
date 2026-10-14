"""B-2a independent playable regression: durable unfinished asset labor.

The test fixture is explicitly noncanonical. It exercises owner-local asset
condition, AFQR-04 work cost, method/tool qualification, v6 persistence,
abandonment, deterministic replay, old v5 stability and installed client.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_fixture_service import (
    FixtureServiceError, digest_fixture_service_state,
    execute_fixture_service, restore_fixture_service, serialize_fixture_service,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointError,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _yard():
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    return app


def test_manual_labor_is_durable_and_wait_alone_is_not_work():
    app = _yard()
    original = app.authoritative_digest()
    first = app.service_chest_latch("work", method="manual")
    assert first.authoritative_changed and first.receipt_id and first.state_delta_id
    assert first.consequence_receipt_id
    assert first.logical_time_after == first.logical_time_before + 1
    assert app.service_state.progress == 1
    assert app.authoritative_digest() != original
    saved_progress = digest_fixture_service_state(app.service_state)
    assert app.wait().authoritative_changed
    assert digest_fixture_service_state(app.service_state) == saved_progress
    assert app.service_state.progress == 1
    finished = app.service_chest_latch("work", method="manual")
    assert finished.authoritative_changed and app.service_state.progress == 2
    assert "serviceable" in app.check_chest_latch().message
    assert app.service_chest_latch("work", method="manual").failure_class
    assert app.service_state.progress == 2


def test_abandonment_is_not_reset_and_resume_keeps_prior_labor():
    app = _yard()
    assert app.service_chest_latch("work", method="manual").authoritative_changed
    abandoned = app.service_chest_latch("abandon")
    assert abandoned.authoritative_changed and app.service_state.progress == 1
    assert app.service_state.abandoned
    assert "abandoned" in app.check_chest_latch().message
    before = app.authoritative_digest()
    assert app.service_chest_latch("abandon").failure_class
    assert before == app.authoritative_digest()
    app.move("north")
    assert app.check_chest_latch().failure_class == "fixture_service_target_not_local"
    assert app.service_chest_latch("work", method="manual").failure_class
    app.move("south")
    assert app.service_chest_latch("work", method="manual").authoritative_changed
    assert app.service_state.progress == 2
    assert not app.service_state.abandoned


def test_tool_qualified_alternate_method_and_no_fake_consumption():
    app = _yard()
    digest = app.authoritative_digest()
    rejected = app.service_chest_latch("work", method="lantern")
    assert rejected.failure_class == "fixture_service_tool_unavailable"
    assert app.authoritative_digest() == digest
    app.move("north")
    assert app.light_object("lantern").authoritative_changed
    assert app.displace_object("lantern", "south", method="slide").authoritative_changed
    app.move("south")
    before = app.runtime_state.logical_time_state.logical_position
    result = app.service_chest_latch("work", method="lantern")
    assert result.authoritative_changed
    assert app.service_state.progress == 2
    assert app.runtime_state.logical_time_state.logical_position == before + 1
    assert app.object_lit_state("astra:entity:brass-lantern").state == "lit"


def test_completed_latch_changes_later_opening_opportunity():
    app = _yard()
    for _ in range(2):
        assert app.service_chest_latch("work", method="manual").authoritative_changed
    # NPC routine may have opened the chest while work time passed.
    if app.object_open_state("astra:entity:tool-chest").state == "open":
        assert app.close_object("chest").authoritative_changed
    assert app.service_chest_latch("secure").authoritative_changed
    assert app.service_state.secured
    before = app.authoritative_digest()
    denied = app.open_object("chest")
    assert denied.failure_class == "fixture_service_latch_secured"
    assert app.authoritative_digest() == before
    denied_npc = app.request_object_state_from_actor("groundskeeper", "open", "chest")
    assert denied_npc.failure_class == "fixture_service_latch_secured"
    assert app.authoritative_digest() == before
    # Advances through the NPC's open phase without bypassing the latch.
    for _ in range(4):
        assert app.wait().authoritative_changed
    assert app.service_state.secured
    assert app.object_open_state("astra:entity:tool-chest").state == "closed"
    assert app.service_chest_latch("release").authoritative_changed
    assert app.open_object("chest").authoritative_changed


def test_service_events_replay_and_retries_refuse_conflicting_meaning():
    app = _yard()
    app.service_chest_latch("work", method="manual")
    saved = serialize_fixture_service(app.service_state)
    assert restore_fixture_service(saved) == app.service_state
    assert digest_fixture_service_state(restore_fixture_service(saved)) == (
        digest_fixture_service_state(app.service_state)
    )
    initial = restore_fixture_service({
        "profile": saved["profile"], "progress": 0,
        "abandoned": False, "secured": False, "events": [],
    })
    event = app.service_state.events[0]
    kwargs = dict(
        command_id=event.command_id, operation=event.operation, method=event.method,
        actor_id=event.actor_id, target_id=event.target_id,
        place_id=event.place_id, logical_before=event.logical_before,
        logical_after=event.logical_after,
        time_receipt_id=event.time_receipt_id, qualified=True,
        expected_pre_digest=digest_fixture_service_state(initial),
    )
    state, receipt, preview, delta = execute_fixture_service(
        state=initial, **kwargs,
    )
    assert receipt == event and preview and delta
    retried, repeated, retry_preview, retry_delta = execute_fixture_service(
        state=state, **kwargs,
    )
    assert retried == state and repeated == event
    assert retry_preview is None and retry_delta is None
    with pytest.raises(FixtureServiceError):
        execute_fixture_service(
            state=state, **{**kwargs, "method": "lantern"},
        )


def test_b2a_v6_checkpoint_restores_and_detects_forged_progress(tmp_path):
    p = tmp_path / "service.json"
    app = MyravantVSM14Application.new(checkpoint_path=p)
    assert app.save().authoritative_changed is False
    assert json.loads(p.read_text())["format_version"] == 5
    app.move("south")
    app.service_chest_latch("work", method="manual")
    assert app.save().checkpoint_digest
    assert json.loads(p.read_text())["format_version"] == 6
    restored = MyravantVSM14Application.restore(checkpoint_path=p)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.service_state.progress == 1
    assert restored.wait().authoritative_changed
    assert restored.service_state.progress == 1
    restored.service_chest_latch("work", method="manual")
    restored.save()
    assert MyravantVSM14Application.restore(
        checkpoint_path=p
    ).authoritative_digest() == restored.authoritative_digest()

    forged = json.loads(p.read_text())
    forged["authoritative_payload"]["components"]["fixture_service"]["progress"] = 0
    payload = forged["authoritative_payload"]
    forged["integrity_digest"] = hashlib.sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode()).hexdigest()
    p.write_text(json.dumps(forged))
    with pytest.raises(PersistentWorldCheckpointError):
        MyravantVSM14Application.restore(checkpoint_path=p)


def _run(commands, *args):
    exe = shutil.which("myravant-play")
    assert exe
    return subprocess.run(
        [exe, *args],
        input="\n".join((*commands, "exit", "")),
        capture_output=True, text=True, timeout=75,
    )


def test_installed_client_two_sessions_labor_abandon_resume(tmp_path):
    results = []
    for n in ("first", "repeat"):
        cp = tmp_path / (n + ".json")
        trace = tmp_path / (n + ".jsonl")
        first = _run(
            ("go south", "service chest latch", "abandon latch service", "save"),
            "--checkpoint", str(cp),
        )
        assert first.returncode == 0, (first.stdout, first.stderr)
        checkpoint = MyravantVSM14Application.restore(checkpoint_path=cp)
        assert checkpoint.service_state.progress == 1
        assert checkpoint.service_state.abandoned
        second = _run(
            ("check latch service", "wait", "resume chest latch service",
             "check latch service", "save"),
            "--load", str(cp), "--checkpoint", str(cp),
            "--trace", str(trace), "--repository-sha", "b" * 40,
        )
        assert second.returncode == 0, (second.stdout, second.stderr)
        restored = MyravantVSM14Application.restore(checkpoint_path=cp)
        assert restored.service_state.progress == 2
        assert not restored.service_state.abandoned
        records = [json.loads(line) for line in trace.read_text().splitlines()]
        assert records[-1]["evidence_complete"]
        interactions = [x for x in records if x["record_type"] == "interaction"]
        service = [x for x in interactions if x["parsed_action"] == "fixture_service"]
        assert len(service) == 3
        assert any(x["authoritative_changed"] and x["receipt_id"] for x in service)
        assert "serviceable" in service[-1]["player_visible_output"]
        results.append((
            restored.authoritative_digest(),
            tuple((x["result_type"], x["pre_state_digest"],
                   x["post_state_digest"]) for x in interactions),
        ))
    assert results[0] == results[1]

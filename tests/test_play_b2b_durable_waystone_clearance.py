"""B-2b: two-stage time-cost route clearance and durable terminal ACK.

A noncanonical fixture licenses only the existing Waystone drag west from
Orchard Path and push north from Yard. Placement (not a second work counter)
is authoritative. The player-visible success gate is the durable save.
"""
from __future__ import annotations

from io import StringIO
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointError,
)
from astra_runtime.myravant_play_fixture import (
    ORCHARD_PATH_ID, WORKSHOP_ID, YARD_ID, WAYSTONE_ID,
)
from astra_runtime.myravant_terminal import run_terminal
from astra_runtime.myravant_terminal_capabilities import (
    execute_bounded_terminal_request,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _at(app, object_id, place_id):
    return any(
        rel.subject_entity_id == object_id
        and rel.object_entity_id == place_id
        and rel.relation_type == "located_at"
        for rel in app.state.representation.relations
    )


def _lit_orchard(app):
    assert app.light_object("lantern").authoritative_changed
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    assert app.current_place_id() == ORCHARD_PATH_ID


def test_dark_remote_worksite_cannot_mint_time_or_work(tmp_path):
    app = MyravantVSM14Application.new(checkpoint_path=tmp_path / "w.json")
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    before = app.authoritative_digest()
    t = app.runtime_state.logical_time_state.logical_position
    out = app.clear_waystone_route()
    assert not out.authoritative_changed
    assert out.failure_class == "waystone_clearance_sensing_unavailable"
    assert app.authoritative_digest() == before
    assert app.runtime_state.logical_time_state.logical_position == t
    inspection = app.clear_waystone_route("check")
    assert not inspection.authoritative_changed
    assert inspection.failure_class == "waystone_clearance_sensing_unavailable"
    assert app.authoritative_digest() == before
    assert app.runtime_state.logical_time_state.logical_position == t


def test_two_distinct_timed_steps_obstruction_and_recovery(tmp_path):
    checkpoint = tmp_path / "work.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _lit_orchard(app)
    start_time = app.runtime_state.logical_time_state.logical_position
    first = app.clear_waystone_route()
    assert first.authoritative_changed
    assert first.consequence_receipt_id
    assert first.receipt_id and first.state_delta_id
    assert first.logical_time_before == start_time
    assert first.logical_time_after == start_time + 1
    assert _at(app, WAYSTONE_ID, YARD_ID)
    assert not _at(app, WAYSTONE_ID, ORCHARD_PATH_ID)
    assert not app.clear_waystone_route("abandon").authoritative_changed
    assert app.save().checkpoint_digest

    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _at(restored, WAYSTONE_ID, YARD_ID)
    assert restored.move("west").authoritative_changed
    assert not restored.move("east").authoritative_changed
    second_start = restored.runtime_state.logical_time_state.logical_position
    second = restored.clear_waystone_route("continue")
    assert second.authoritative_changed
    assert second.consequence_receipt_id and second.receipt_id
    assert second.logical_time_after == second_start + 1
    assert _at(restored, WAYSTONE_ID, WORKSHOP_ID)
    assert restored.move("east").authoritative_changed
    assert restored.save().checkpoint_digest

    final = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert final.authoritative_digest() == restored.authoritative_digest()
    assert _at(final, WAYSTONE_ID, WORKSHOP_ID)
    assert not final.clear_waystone_route().authoritative_changed


def test_resumed_nonlocal_work_refused_without_knowledge_leak(tmp_path):
    app = MyravantVSM14Application.new(checkpoint_path=tmp_path / "x.json")
    before = app.authoritative_digest()
    answer = app.clear_waystone_route("check")
    assert not answer.authoritative_changed
    assert answer.failure_class == "waystone_clearance_target_not_local"
    assert app.authoritative_digest() == before


def _play(commands, *opts):
    path = shutil.which("myravant-play")
    assert path, "installed myravant-play entrypoint not available"
    return subprocess.run(
        [path, *opts],
        input="\n".join((*commands, "exit", "")),
        text=True, capture_output=True, timeout=80,
    )


def test_installed_terminal_autosaves_each_success_across_sessions(tmp_path):
    cp = tmp_path / "persisted.json"
    first = _play(
        ("light lantern", "take lantern", "go south", "go east",
         "recover waystone"),
        "--checkpoint", str(cp),
    )
    assert first.returncode == 0, (first.stdout, first.stderr)
    stage1 = MyravantVSM14Application.restore(checkpoint_path=cp)
    assert _at(stage1, WAYSTONE_ID, YARD_ID)
    # No explicit save command was issued. The acknowledged work persists.
    session2 = _play(
        ("go west", "clear waystone route"),
        "--load", str(cp),
    )
    assert session2.returncode == 0, (session2.stdout, session2.stderr)
    stage2 = MyravantVSM14Application.restore(checkpoint_path=cp)
    assert _at(stage2, WAYSTONE_ID, WORKSHOP_ID)
    assert stage2.runtime_state.logical_time_state.logical_position >= 2


def test_no_checkpoint_argument_allocates_recoverable_file(monkeypatch, tmp_path):
    monkeypatch.setenv("MYRAVANT_SAVE_DIR", str(tmp_path))
    app = MyravantVSM14Application.new()
    output = StringIO()
    ret = run_terminal(
        app, input_stream=StringIO("go south\nexit\n"), output_stream=output,
        specialized_router=execute_bounded_terminal_request,
    )
    assert ret == 0
    assert "Recovery checkpoint:" in output.getvalue()
    stored = list(tmp_path.glob("session-*.json"))
    assert len(stored) == 1
    recovered = MyravantVSM14Application.restore(checkpoint_path=stored[0])
    assert recovered.current_place_id() == YARD_ID


def test_failed_durable_write_never_acknowledges_success(
    monkeypatch, tmp_path,
):
    from astra_runtime.domain import persistent_world_component_checkpoint as cp
    app = MyravantVSM14Application.new(
        checkpoint_path=tmp_path / "failing.json"
    )
    out = StringIO()
    def fail_replace(source, destination):
        raise OSError("injected durability fault")
    with monkeypatch.context() as patch:
        patch.setattr(cp, "_replace_checkpoint_durably", fail_replace)
        with pytest.raises(SystemExit) as raised:
            run_terminal(
                app, input_stream=StringIO("go south\n"),
                output_stream=out,
                specialized_router=execute_bounded_terminal_request,
            )
    assert raised.value.code == 3
    assert "could not be durably acknowledged" in out.getvalue()
    assert "You move" not in out.getvalue()
    assert not (tmp_path / "failing.json").exists()

def test_real_process_kill_after_terminal_success_ack_is_recoverable(tmp_path):
    """A child exits by external termination *after* its success was emitted."""
    import time
    cp = tmp_path / "ack.json"
    marker = tmp_path / "ack.marker"
    child = r"""
import sys, time
from pathlib import Path
from io import StringIO
from astra_runtime import myravant_terminal as terminal
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_terminal_capabilities import execute_bounded_terminal_request

checkpoint, marker = sys.argv[1:]
original = terminal._write_durable_result
def ack_barrier(*args, **kwargs):
    visible = original(*args, **kwargs)
    if args[2].authoritative_changed:
        Path(marker).write_text("ack", encoding="utf-8")
        while True:
            time.sleep(0.2)
    return visible
terminal._write_durable_result = ack_barrier
app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
terminal.run_terminal(
    app, input_stream=StringIO("go south\n"),
    output_stream=sys.stdout,
    specialized_router=execute_bounded_terminal_request,
)
"""
    proc = subprocess.Popen(
        [sys.executable, "-c", child, str(cp), str(marker)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    try:
        deadline = time.monotonic() + 35
        while not marker.exists() and proc.poll() is None:
            if time.monotonic() >= deadline:
                break
            time.sleep(0.05)
        if not marker.exists():
            stdout, stderr = proc.communicate(timeout=10)
            pytest.fail(
                f"child failed to acknowledge: {proc.returncode}: "
                f"{stdout} {stderr}"
            )
        assert marker.read_text(encoding="utf-8") == "ack"
    finally:
        if proc.poll() is None:
            proc.kill()
        proc.communicate(timeout=10)
    assert proc.returncode != 0
    restored = MyravantVSM14Application.restore(checkpoint_path=cp)
    assert restored.current_place_id() == YARD_ID
    assert len(restored.state.committed_transitions) == 1

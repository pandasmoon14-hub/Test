"""B-2a bounded assurance: process-kill boundaries and detection probes.

The purpose is evidence, not a newly implied per-action durability guarantee.
Real child processes are terminated, unlike ordinary application object deletion.
Mutation probes run in isolated pytest child processes and never modify files.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointError,
    PersistentWorldCheckpointWriteError,
)
from astra_runtime.kernel.event_ledger import (
    EventLedgerEntry, InvalidEventLedgerEntryError, create_event_ledger_entry,
)
from astra_runtime.myravant_play_fixture import WORKSHOP_ID, YARD_ID
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


# The code executes with the same installed Python environment as the tests;
# all barriers are plain files, so it works on Windows without POSIX signals.
_CHILD = r'''
import os
import sys
import time
from pathlib import Path

from astra_runtime.domain import persistent_world_component_checkpoint as cp
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application

checkpoint, marker, phase = map(str, sys.argv[1:4])

def barrier():
    Path(marker).write_text(phase, encoding="utf-8")
    # The parent observes the marker, kills us, and confirms return code.
    while True:
        time.sleep(0.2)

app = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
if phase == "before_commit":
    barrier()
assert app.move("south").authoritative_changed
if phase == "after_memory_commit":
    barrier()
if phase == "during_serialization":
    cp._canonical_bytes = lambda value: barrier()
elif phase == "after_temp_fsync_before_replace":
    cp._replace_checkpoint_durably = lambda source, destination: barrier()
elif phase == "after_durable_replace_before_ack":
    original = cp._replace_checkpoint_durably
    def replace_then_stop(source, destination):
        original(source, destination)
        barrier()
    cp._replace_checkpoint_durably = replace_then_stop

assert app.save().checkpoint_digest
if phase == "after_save_ack":
    barrier()
raise RuntimeError("unexpected phase " + phase)
'''


def _terminate_at_barrier(checkpoint: Path, phase: str, tmp_path: Path) -> None:
    marker = tmp_path / ("barrier-" + phase)
    proc = subprocess.Popen(
        [sys.executable, "-c", _CHILD, str(checkpoint), str(marker), phase],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    try:
        deadline = time.monotonic() + 35
        while not marker.exists() and proc.poll() is None:
            if time.monotonic() > deadline:
                break
            time.sleep(0.05)
        if not marker.exists():
            out, err = proc.communicate(timeout=5)
            pytest.fail(f"child never reached {phase}; exit={proc.returncode}: {out} {err}")
        assert marker.read_text(encoding="utf-8") == phase
    finally:
        if proc.poll() is None:
            proc.kill()  # Windows TerminateProcess / POSIX SIGKILL
        proc.communicate(timeout=10)
    assert proc.returncode != 0


@pytest.mark.parametrize("phase,should_have_commit", [
    ("before_commit", False),
    ("after_memory_commit", False),
    ("during_serialization", False),
    ("after_temp_fsync_before_replace", False),
    ("after_durable_replace_before_ack", True),
    ("after_save_ack", True),
])
def test_process_termination_vs_checkpoint_durability(
    tmp_path: Path, phase: str, should_have_commit: bool,
) -> None:
    checkpoint = tmp_path / "session.json"
    fresh = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    assert fresh.save().checkpoint_digest
    old_digest = fresh.authoritative_digest()
    _terminate_at_barrier(checkpoint, phase, tmp_path)
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert (restored.current_place_id() == YARD_ID) is should_have_commit
    assert (restored.authoritative_digest() != old_digest) is should_have_commit

    if should_have_commit:
        assert len(restored.state.committed_transitions) == 1
        # Continued legal play creates exactly one additional committed move.
        result = restored.move("north")
        assert result.authoritative_changed
        assert restored.current_place_id() == WORKSHOP_ID
        assert len(restored.state.committed_transitions) == 2
        restored.save()
        recovered_again = MyravantVSM14Application.restore(
            checkpoint_path=checkpoint
        )
        assert recovered_again.authoritative_digest() == restored.authoritative_digest()
        assert len(recovered_again.state.committed_transitions) == 2
    else:
        assert len(restored.state.committed_transitions) == 0
        # A killed writer's temporary files never get selected as checkpoints.
        if phase == "after_temp_fsync_before_replace":
            assert list(tmp_path.glob(".session.json.*.component-tmp"))


def test_clean_exit_without_save_does_not_implicitly_checkpoint(tmp_path):
    checkpoint = tmp_path / "session.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    app.save()
    original = app.authoritative_digest()
    proc = subprocess.run(
        [sys.executable, "-m", "astra_runtime.myravant_terminal",
         "--load", str(checkpoint)],
        input="go south\nexit\n", text=True, capture_output=True, timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    assert MyravantVSM14Application.restore(
        checkpoint_path=checkpoint
    ).authoritative_digest() == original


def test_failed_pre_replace_preserves_previous_checkpoint_and_cleans_temp(
    monkeypatch, tmp_path,
):
    from astra_runtime.domain import persistent_world_component_checkpoint as cp

    checkpoint = tmp_path / "session.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    app.save()
    original = checkpoint.read_bytes()
    app.move("south")
    changed = app.authoritative_digest()

    def fail_replace(source, destination):
        assert source.exists() and source.parent == destination.parent
        raise OSError("injected replacement failure")

    with monkeypatch.context() as patch:
        patch.setattr(cp, "_replace_checkpoint_durably", fail_replace)
        with pytest.raises(PersistentWorldCheckpointWriteError):
            app.save()
    assert app.authoritative_digest() == changed
    assert checkpoint.read_bytes() == original
    assert not list(tmp_path.glob(".session.json.*.component-tmp"))
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.current_place_id() == WORKSHOP_ID


def test_corrupt_partial_checkpoint_is_not_restored(tmp_path):
    checkpoint = tmp_path / "session.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    app.save()
    original = checkpoint.read_bytes()
    checkpoint.write_bytes(original[:len(original) // 2])
    with pytest.raises(PersistentWorldCheckpointError):
        MyravantVSM14Application.restore(checkpoint_path=checkpoint)


def test_detection_ledger_bool_sequence(monkeypatch):
    from astra_runtime.kernel import event_ledger as owner
    invalid = EventLedgerEntry(
        event_id="evt-1", event_type="command_event",
        sequence=True, source_command_id="cmd-1",
        source_preview_id="preview-1",
    )
    with pytest.raises(InvalidEventLedgerEntryError):
        create_event_ledger_entry(
            event_id="evt-1", event_type="command_event",
            sequence=True, source_command_id="cmd-1",
            source_preview_id="preview-1",
        )
    if os.environ.get("MYRAVANT_TEST_MUTATION") == "accept_bool_sequence":
        monkeypatch.setattr(owner, "validate_event_ledger_entry", lambda value: True)
    assert not owner.validate_event_ledger_entry(invalid), (
        "directly constructed bool sequence must not validate"
    )


def test_detection_service_work_must_progress(monkeypatch):
    from astra_runtime.domain import persistent_world_object_open_close as owner
    from astra_runtime.myravant_play_fixture import PLAYER_ID, TOOL_CHEST_ID, YARD_ID

    state = owner.FixtureServiceState()
    if os.environ.get("MYRAVANT_TEST_MUTATION") == "no_work_progress":
        monkeypatch.setattr(owner, "_transition",
                            lambda s, operation, method: (s.progress, False, False))
    next_state, event, preview, delta = owner.execute_fixture_service(
        state=state, command_id="probe-work-0001", operation="work",
        method="manual", actor_id=PLAYER_ID, target_id=TOOL_CHEST_ID,
        place_id=YARD_ID, logical_before=0, logical_after=1,
        time_receipt_id="probe-time-receipt-0001", qualified=True,
        expected_pre_digest=owner.digest_fixture_service_state(state),
    )
    assert next_state.progress == 1, "lawful work must advance asset state"
    assert event.post_progress == 1
    assert preview is not None and delta is not None


@pytest.mark.parametrize("name,test_name", [
    ("accept_bool_sequence", "test_detection_ledger_bool_sequence"),
    ("no_work_progress", "test_detection_service_work_must_progress"),
])
def test_isolated_mutation_detection_and_reversion(name, test_name, tmp_path):
    """Baseline pass -> injected defect fails -> clean baseline passes again.

    Production Python files remain unchanged. Child monkeypatch is scoped to
    its process; this probes the oracle, not general mutation coverage.
    """
    current = str(Path(__file__).resolve())
    command = [sys.executable, "-m", "pytest", "-q", current + "::" + test_name]
    original_env = os.environ.copy()
    original_env.pop("MYRAVANT_TEST_MUTATION", None)
    broken_env = dict(original_env, MYRAVANT_TEST_MUTATION=name)

    def invoke(environment):
        return subprocess.run(
            command, env=environment, text=True,
            capture_output=True, timeout=45,
        )

    before = invoke(original_env)
    assert before.returncode == 0, (before.stdout, before.stderr)
    mutant = invoke(broken_env)
    assert mutant.returncode != 0
    assert "1 failed" in mutant.stdout, mutant.stdout + mutant.stderr
    assert (
        "directly constructed bool sequence" if name == "accept_bool_sequence"
        else "lawful work must advance asset state"
    ) in mutant.stdout
    after = invoke(original_env)
    assert after.returncode == 0, (after.stdout, after.stderr)

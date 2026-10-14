"""B-1: work spanning actions/sessions, reconstructed from committed world truth.

Two mechanically distinct goals share no invented work ledger: (1) prepare and
position a lit lantern, (2) move a container to its worksite and open it.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    replay_persistent_world_object_displacement,
)
from astra_runtime.myravant_bounded_work_goals import parse_bounded_work_goal
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID, TOOL_CHEST_ID, YARD_ID, WORKSHOP_ID,
)
from astra_runtime.myravant_terminal_capabilities import (
    execute_bounded_terminal_request,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _attempt(app, words):
    value = execute_bounded_terminal_request(app, words)
    assert value is not None and value[0] == "bounded_work"
    return value[1]


def _where(app, target):
    found = [
        rel.object_entity_id
        for rel in app.state.representation.relations
        if rel.subject_entity_id == target
        and rel.relation_type == LOCATED_AT_RELATION_TYPE
    ]
    return found[0] if len(found) == 1 else None


@pytest.mark.parametrize(("words", "goal", "inspect"), (
    ("prepare lantern for yard", "prepare_lantern", False),
    ("work on lantern preparation", "prepare_lantern", False),
    ("resume the lantern preparation", None, False),
    ("check lantern preparation", "prepare_lantern", True),
    ("stage the chest in the workshop", "stage_chest", False),
    ("continue chest staging", "stage_chest", False),
    ("inspect progress on chest staging", "stage_chest", True),
    ("make a sword", None, False),
))
def test_work_grammar_is_goal_scoped_not_general_matter_creation(words, goal, inspect):
    parsed = parse_bounded_work_goal(words)
    assert parsed == ((goal, inspect) if goal is not None else None)


def test_lantern_work_is_real_lit_and_location_changes_and_survives_wait():
    app = MyravantVSM14Application.new()
    initial = app.authoritative_digest()
    preview = _attempt(app, "check lantern preparation")
    assert not preview.authoritative_changed
    assert preview.pre_state_digest == preview.post_state_digest == initial
    assert "light the local lantern" in preview.message

    first = _attempt(app, "work on lantern preparation")
    assert first.result_type == "object_lit_state_committed"
    assert first.receipt_id and first.state_delta_id
    assert app.object_lit_state(LANTERN_ID).state == "lit"
    after_first = app.authoritative_digest()

    waited = app.wait()
    assert waited.authoritative_changed and waited.receipt_id
    assert app.object_lit_state(LANTERN_ID).state == "lit"
    assert app.authoritative_digest() != after_first

    second_pre = app.state.representation
    second = _attempt(app, "continue lantern preparation")
    assert second.result_type == "object_displacement_committed"
    assert second.receipt_id and second.state_delta_id
    receipt = app.runtime_state.committed_object_displacement_transitions[-1].receipt
    assert receipt.method == "slide"
    assert receipt.object_entity_id == LANTERN_ID
    assert receipt.destination_place_id == YARD_ID
    assert replay_persistent_world_object_displacement(
        pre_state_representation=second_pre, receipt=receipt,
    ) == app.state.representation
    assert _where(app, LANTERN_ID) == YARD_ID
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    # Remote inspection cannot reveal the new exact object state from Workshop.
    digest = app.authoritative_digest()
    hidden = _attempt(app, "check lantern preparation")
    assert hidden.failure_class == "bounded_work_target_not_local"
    assert hidden.receipt_id is None
    assert hidden.pre_state_digest == hidden.post_state_digest == digest
    assert app.move("south").authoritative_changed
    finished = _attempt(app, "resume lantern preparation")
    assert finished.result_type == "bounded_work_status"
    assert "complete" in finished.message
    assert not finished.authoritative_changed


def test_chest_work_must_move_actual_container_then_open_and_interrupt():
    app = MyravantVSM14Application.new()
    wrong_place = _attempt(app, "check chest staging")
    assert wrong_place.failure_class == "bounded_work_target_not_local"
    assert app.move("south").authoritative_changed
    first = _attempt(app, "work on chest staging")
    assert first.result_type == "object_displacement_committed"
    assert first.receipt_id and first.state_delta_id
    assert _where(app, TOOL_CHEST_ID) == WORKSHOP_ID
    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"

    before = app.authoritative_digest()
    interruption = _attempt(app, "resume chest staging")
    assert interruption.failure_class == "bounded_work_target_not_local"
    assert interruption.pre_state_digest == interruption.post_state_digest == before
    assert app.move("north").authoritative_changed
    waiting = app.wait()
    assert waiting.authoritative_changed
    second = _attempt(app, "resume chest staging")
    assert second.result_type == "object_state_committed"
    assert second.receipt_id and second.state_delta_id
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"
    assert _where(app, TOOL_CHEST_ID) == WORKSHOP_ID
    finished = _attempt(app, "check chest staging")
    assert "complete" in finished.message
    assert finished.authoritative_changed is False


def test_direct_actions_and_work_actions_reach_same_lawful_world_facts():
    direct = MyravantVSM14Application.new()
    assert direct.light_object("lantern").authoritative_changed
    assert direct.displace_object("lantern", "south", method="slide").authoritative_changed

    guided = MyravantVSM14Application.new()
    assert _attempt(guided, "work on lantern preparation").authoritative_changed
    assert _attempt(guided, "work on lantern preparation").authoritative_changed

    assert direct.state.representation == guided.state.representation
    assert direct.object_lit_state(LANTERN_ID) == guided.object_lit_state(LANTERN_ID)
    assert direct.authoritative_digest() == guided.authoritative_digest()


def _run(commands, *args):
    executable = shutil.which("myravant-play")
    assert executable
    return subprocess.run(
        [executable, *args],
        input="\n".join((*commands, "exit", "")),
        capture_output=True, text=True, timeout=75,
    )


def _records(path):
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["record_type"] == "session_start"
    assert rows[-1]["record_type"] == "session_end"
    assert rows[-1]["evidence_complete"]
    return [x for x in rows if x["record_type"] == "interaction"]


@pytest.mark.parametrize(("goal", "first", "resume", "state"), (
    ("lantern", ("work on lantern preparation",), (
        "wait", "resume lantern preparation", "go south",
        "check lantern preparation", "save",
    ), "lit"),
    ("chest", ("go south", "work on chest staging"), (
        "wait", "go north", "resume chest staging", "check chest staging", "save",
    ), "open"),
))
def test_installed_two_session_bounded_work_with_v5_restore(
    goal, first, resume, state, tmp_path,
):
    results = []
    for run_id in ("one", "two"):
        cp = tmp_path / f"{goal}-{run_id}.json"
        trace = tmp_path / f"{goal}-{run_id}.jsonl"
        initial = _run((*first, "save"), "--checkpoint", str(cp))
        assert initial.returncode == 0, (initial.stdout, initial.stderr)
        first_saved = MyravantVSM14Application.restore(checkpoint_path=cp)
        assert first_saved.current_place_id() in {WORKSHOP_ID, YARD_ID}
        continued = _run(
            resume, "--load", str(cp), "--checkpoint", str(cp),
            "--trace", str(trace), "--repository-sha", "b" * 40,
        )
        assert continued.returncode == 0, (continued.stdout, continued.stderr)
        records = _records(trace)
        assert [r["raw_player_input"] for r in records] == [
            x + "\n" for x in resume
        ]
        steps = [r for r in records if r["parsed_action"] == "bounded_work"]
        assert any(r["authoritative_changed"] and r["receipt_id"] for r in steps)
        assert "complete" in steps[-1]["player_visible_output"]
        restored = MyravantVSM14Application.restore(checkpoint_path=cp)
        if goal == "lantern":
            assert restored.object_lit_state(LANTERN_ID).state == state
            assert _where(restored, LANTERN_ID) == YARD_ID
        else:
            assert restored.object_open_state(TOOL_CHEST_ID).state == state
            assert _where(restored, TOOL_CHEST_ID) == WORKSHOP_ID
        assert restored.authoritative_digest() == records[-1]["post_state_digest"]
        saved = cp.read_bytes()
        review = _run(
            ("look", "save"), "--load", str(cp), "--checkpoint", str(cp),
        )
        assert review.returncode == 0
        assert cp.read_bytes() == saved
        results.append((
            saved,
            tuple((r["parsed_action"], r["result_type"],
                   r["pre_state_digest"], r["post_state_digest"]) for r in records),
        ))
    assert results[0] == results[1]

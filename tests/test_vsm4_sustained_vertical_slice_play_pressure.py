"""VSM-4 sustained vertical-slice play pressure regressions."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "myravant_sustained_play_pressure_harness.py"
REPOSITORY_SHA = "a" * 40


def _run(report: Path) -> dict:
    completed = subprocess.run(
        [
            sys.executable,
            str(HARNESS),
            "--report",
            str(report),
            "--repository-sha",
            REPOSITORY_SHA,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, (
        completed.stdout,
        completed.stderr,
    )
    return json.loads(report.read_text(encoding="utf-8"))


def test_vsm4_harness_is_deterministic_and_restore_equivalent(tmp_path):
    first = _run(tmp_path / "first.json")
    second = _run(tmp_path / "second.json")

    assert first == second
    assert first["harness_id"] == "myravant.sustained_play_pressure"
    assert first["harness_version"] == 1
    assert first["scenario_id"] == "vsm4-sustained-vertical-slice-01"
    assert first["repository_sha"] == REPOSITORY_SHA
    assert first["model_mode"] == "MODEL-NONE"
    assert first["authority_effect"] == "none"

    summary = first["summary"]
    assert summary["status"] == "PASS"
    assert summary["failures"] == []
    assert summary["continuous_replay_match"] is True
    assert summary["restored_replay_match"] is True
    assert summary["restore_equivalence_match"] is True
    assert summary["continuous_final_digest"] == (
        summary["restored_final_digest"]
    )
    assert summary["evidence_complete"] is True
    assert summary["trace_write_failures"] == 0


def test_vsm4_sustained_sequence_crosses_existing_capabilities(tmp_path):
    report = _run(tmp_path / "sequence.json")
    actions = report["actions"]

    for expected in (
        "look",
        "inspect lantern",
        "pickup lantern",
        "light lantern",
        "move south",
        "open chest",
        "wait",
        "put lantern in chest",
        "save",
        "close chest",
        "take lantern from chest",
        "move east",
        "extinguish lantern",
        "pickup waystone",
        "throw the lantern over the wall",
        "move west",
        "drop waystone",
    ):
        assert expected in actions

    assert report["split_after_action"] == "save"
    assert report["summary"]["meaningful_interactions"] == len(actions)
    assert report["summary"]["meaningful_interactions"] >= 25


def test_vsm4_player_world_interference_remains_lawful(tmp_path):
    report = _run(tmp_path / "interference.json")
    interactions = report["continuous"]["interactions"]
    waits = [
        row
        for row in interactions
        if row["parsed_action"] == "wait"
    ]

    assert [row["logical_time_after"] for row in waits] == [1, 2, 3, 4]
    assert [row["world_process_outcome"] for row in waits] == [
        "committed",
        "already_satisfied",
        "already_satisfied",
        "committed",
    ]

    assert waits[1]["consequence_receipt_id"] is None
    assert waits[1]["consequence_state_delta_id"] is None
    assert waits[2]["consequence_receipt_id"] is None
    assert waits[2]["consequence_state_delta_id"] is None


def test_vsm4_hidden_probe_and_unsupported_attempt_do_not_destabilize_play(
    tmp_path,
):
    report = _run(tmp_path / "pressure.json")
    interactions = report["continuous"]["interactions"]

    waystone_attempts = [
        row
        for row in interactions
        if (
            row["parsed_action"] == "pickup"
            and row["parsed_argument"] == "waystone"
        )
    ]
    assert len(waystone_attempts) == 2

    hidden, later = waystone_attempts
    assert hidden["result_type"] == "custody_rejected"
    assert hidden["authoritative_changed"] is False
    assert hidden["pre_state_digest"] == hidden["post_state_digest"]
    assert hidden["receipt_id"] is None
    assert hidden["state_delta_id"] is None
    assert hidden["player_visible_output"] == (
        "You cannot pick that up in the current state.\n"
    )

    assert later["result_type"] == "custody_committed"
    assert later["authoritative_changed"] is True

    unsupported = next(
        row
        for row in interactions
        if row["parsed_action"] == "unsupported"
    )
    assert unsupported["failure_class"] == (
        "unsupported_capability_throwing"
    )
    assert unsupported["authoritative_changed"] is False
    assert unsupported["pre_state_digest"] == (
        unsupported["post_state_digest"]
    )
    assert unsupported["command_id"] is None
    assert unsupported["receipt_id"] is None
    assert unsupported["state_delta_id"] is None


def test_vsm4_restore_preserves_world_continuity_and_relocation(tmp_path):
    report = _run(tmp_path / "restore.json")
    restored = report["restored"]

    assert restored["pre_restore_digest"] == (
        restored["post_restore_digest"]
    )

    snapshot = restored["snapshot"]
    assert snapshot["logical_time"] == 4
    assert snapshot["player_place"].endswith(":yard")
    assert snapshot["groundskeeper_place"].endswith(":gatehouse")
    assert snapshot["lantern_carried"] is True
    assert snapshot["waystone_carried"] is False
    assert snapshot["waystone_direct_place"].endswith(":yard")
    assert snapshot["chest_open_state"] == "open"
    assert snapshot["lantern_lit_state"] == "unlit"
    assert "Weathered Waystone" in snapshot["look_objects"]


def test_vsm4_observation_and_presentation_never_gain_authority(tmp_path):
    report = _run(tmp_path / "observation.json")

    for row in report["continuous"]["interactions"]:
        if row["parsed_action"] in {"look", "inspect"}:
            assert row["authoritative_changed"] is False
            assert row["pre_state_digest"] == row["post_state_digest"]
            assert row["command_id"] is None
            assert row["receipt_id"] is None
            assert row["state_delta_id"] is None

    visible = "\n".join(
        row["player_visible_output"]
        for row in report["continuous"]["interactions"]
    ).casefold()
    for forbidden in (
        "world_process_",
        "command_id=",
        "receipt_id=",
        "routine_phase",
        "already_satisfied",
        "due_process_ref",
    ):
        assert forbidden not in visible


def test_vsm4_session_receipts_are_complete_evidence_only(tmp_path):
    report = _run(tmp_path / "evidence.json")

    ends = (
        report["continuous"]["session_ends"]
        + report["restored"]["session_ends"]
    )
    assert len(ends) == 3

    for end in ends:
        assert end["authority_effect"] == "none"
        assert end["evidence_only"] is True
        assert end["evidence_complete"] is True
        assert end["trace_write_failures"] == 0
        assert end["meaningful_interactions"] > 0

    assert report["summary"]["unsupported_or_rejected"] >= 2

"""Focused tests for bounded Myravant live-play evidence capture."""

from __future__ import annotations

import json

import pytest

from astra_runtime.myravant_live_play_evidence import (
    LivePlayEvidenceRecorder,
    LivePlayEvidenceWriteError,
    build_live_play_session_header,
)


INITIAL_DIGEST = "0" * 64
POST_DIGEST = "1" * 64
CHECKPOINT_DIGEST = "2" * 64


def _header():
    return build_live_play_session_header(
        session_id="live-play-test-session",
        campaign_id="astra:campaign:myravant-terminal-g1",
        repository_sha="a" * 40,
        initial_state_digest=INITIAL_DIGEST,
        restore_performed=False,
        environment_id="ENV-T2-TERMUX-ARM64-DEV",
        network_mode="offline",
    )


def _records(path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]


def test_jsonl_trace_preserves_raw_input_and_runtime_evidence(tmp_path):
    trace_path = tmp_path / "live-play.jsonl"
    recorder = LivePlayEvidenceRecorder(
        trace_path=trace_path,
        header=_header(),
    )

    recorder.record_interaction(
        raw_player_input="move south\n",
        parsed_action="move",
        parsed_argument="south",
        player_visible_output="You move to the Yard.\n",
        result_type="movement_committed",
        authoritative_changed=True,
        command_id="terminal-move-000001",
        command_fingerprint="3" * 64,
        preview_id="astra:movement_preview:test-preview",
        receipt_id="astra:movement_receipt:test-receipt",
        state_delta_id="astra:movement_delta:test-delta",
        spatial_evidence_id="astra:evidence:test-spatial",
        opportunity_evidence_id="astra:evidence:test-opportunity",
        pre_state_digest=INITIAL_DIGEST,
        post_state_digest=POST_DIGEST,
    )

    receipt = recorder.finish(
        final_state_digest=POST_DIGEST
    )

    records = _records(trace_path)
    assert [record["record_type"] for record in records] == [
        "session_start",
        "interaction",
        "session_end",
    ]

    start, interaction, end = records

    assert start["evidence_only"] is True
    assert start["authority_effect"] == "none"
    assert start["repository_sha"] == "a" * 40
    assert start["model_mode"] == "MODEL-NONE"
    assert interaction["raw_player_input"] == "move south\n"
    assert interaction["command_id"] == "terminal-move-000001"
    assert interaction["command_fingerprint"] == "3" * 64
    assert interaction["pre_state_digest"] == INITIAL_DIGEST
    assert interaction["post_state_digest"] == POST_DIGEST
    assert end["final_state_digest"] == POST_DIGEST
    assert end["meaningful_interactions"] == 1
    assert end["committed_transitions"] == 1
    assert end["evidence_complete"] is True
    assert receipt.evidence_complete is True


def test_checkpoint_and_unsupported_counts_are_evidence_only(tmp_path):
    trace_path = tmp_path / "live-play.jsonl"
    recorder = LivePlayEvidenceRecorder(
        trace_path=trace_path,
        header=_header(),
    )

    recorder.record_interaction(
        raw_player_input="climb onto the roof\n",
        parsed_action="unsupported",
        parsed_argument="climb onto the roof",
        player_visible_output=(
            "That attempt does not currently have an executable route. "
            "No authoritative state changed.\n"
        ),
        result_type="unsupported_input",
        authoritative_changed=False,
        pre_state_digest=INITIAL_DIGEST,
        post_state_digest=INITIAL_DIGEST,
        failure_class="unsupported_input_no_executable_route",
    )
    recorder.record_interaction(
        raw_player_input="save\n",
        parsed_action="save",
        parsed_argument=None,
        player_visible_output="Checkpoint written.\n",
        result_type="checkpoint_written",
        authoritative_changed=False,
        pre_state_digest=INITIAL_DIGEST,
        post_state_digest=INITIAL_DIGEST,
        checkpoint_digest=CHECKPOINT_DIGEST,
    )

    receipt = recorder.finish(
        final_state_digest=INITIAL_DIGEST
    )

    assert receipt.meaningful_interactions == 2
    assert receipt.unsupported_or_rejected == 1
    assert receipt.checkpoints_written == 1
    assert receipt.trace_write_failures == 0


def test_trace_write_failure_disables_evidence_without_repair_path(
    tmp_path,
    monkeypatch,
):
    recorder = LivePlayEvidenceRecorder(
        trace_path=tmp_path / "live-play.jsonl",
        header=_header(),
    )

    def fail_write(_record):
        raise OSError("synthetic trace failure")

    monkeypatch.setattr(recorder, "_append_record", fail_write)

    with pytest.raises(LivePlayEvidenceWriteError):
        recorder.record_interaction(
            raw_player_input="look\n",
            parsed_action="look",
            parsed_argument=None,
            player_visible_output="Workshop\n",
            result_type="look",
            authoritative_changed=False,
            pre_state_digest=INITIAL_DIGEST,
            post_state_digest=INITIAL_DIGEST,
        )

    assert recorder.evidence_complete is False
    assert recorder.trace_write_failures == 1

    receipt = recorder.finish(
        final_state_digest=INITIAL_DIGEST
    )
    assert receipt.evidence_complete is False
    assert receipt.trace_write_failures == 1


def test_missing_trace_parent_fails_without_creating_storage(tmp_path):
    missing_parent = tmp_path / "missing"
    trace_path = missing_parent / "live-play.jsonl"

    with pytest.raises(LivePlayEvidenceWriteError):
        LivePlayEvidenceRecorder(
            trace_path=trace_path,
            header=_header(),
        )

    assert not missing_parent.exists()

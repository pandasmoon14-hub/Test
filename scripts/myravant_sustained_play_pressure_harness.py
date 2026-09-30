#!/usr/bin/env python3
"""VSM-4 deterministic sustained-play pressure harness for Myravant.

This harness is evaluation-only. It composes already-owned terminal/runtime
capabilities across a longer play history and a real save/restore boundary.
It does not own authoritative state, gameplay outcomes, rules, canon, or
failure classification.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from io import StringIO
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from astra_runtime.domain.persistent_world_entity_location_representation import (  # noqa: E402
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_live_play_evidence import (  # noqa: E402
    LivePlayEvidenceRecorder,
    build_live_play_session_header,
)
from astra_runtime.myravant_play_application import (  # noqa: E402
    MyravantPlayApplication,
)
from astra_runtime.myravant_play_fixture import (  # noqa: E402
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    TOOL_CHEST_ID,
    WAYSTONE_ID,
    YARD_ID,
)
from astra_runtime.myravant_terminal import run_terminal  # noqa: E402


HARNESS_ID = "myravant.sustained_play_pressure"
HARNESS_VERSION = 1
SCENARIO_ID = "vsm4-sustained-vertical-slice-01"
MODEL_MODE = "MODEL-NONE"
AUTHORITY_EFFECT = "none"

PRE_SPLIT_ACTIONS = (
    "look",
    "inspect lantern",
    "pickup lantern",
    "light lantern",
    "move south",
    "open chest",
    "wait",
    "put lantern in chest",
    "wait",
    "look",
    "save",
)

POST_SPLIT_ACTIONS = (
    "close chest",
    "wait",
    "open chest",
    "take lantern from chest",
    "move east",
    "look",
    "extinguish lantern",
    "pickup waystone",
    "throw the lantern over the wall",
    "light lantern",
    "pickup waystone",
    "extinguish lantern",
    "move west",
    "drop waystone",
    "wait",
    "look",
)

ALL_ACTIONS = PRE_SPLIT_ACTIONS + POST_SPLIT_ACTIONS

SEMANTIC_INTERACTION_KEYS = (
    "raw_player_input",
    "parsed_action",
    "parsed_argument",
    "player_visible_output",
    "result_type",
    "authoritative_changed",
    "command_id",
    "command_fingerprint",
    "preview_id",
    "receipt_id",
    "state_delta_id",
    "spatial_evidence_id",
    "observation_evidence_id",
    "opportunity_evidence_id",
    "due_process_ref",
    "consequence_receipt_id",
    "consequence_state_delta_id",
    "world_event_class",
    "world_process_actor_id",
    "world_process_action",
    "world_process_target_id",
    "world_process_command_id",
    "world_process_outcome",
    "logical_time_before",
    "logical_time_after",
    "pre_state_digest",
    "post_state_digest",
    "checkpoint_digest",
    "failure_class",
)

SEMANTIC_SESSION_END_KEYS = (
    "evidence_only",
    "authority_effect",
    "final_state_digest",
    "meaningful_interactions",
    "committed_transitions",
    "unsupported_or_rejected",
    "checkpoints_written",
    "trace_write_failures",
    "evidence_complete",
    "human_interventions",
)


def _repo_sha() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    value = completed.stdout.strip()
    return (
        value
        if completed.returncode == 0 and len(value) == 40
        else "unknown"
    )


def _records(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _semantic_interactions(path: Path) -> list[dict[str, Any]]:
    rows = [
        row
        for row in _records(path)
        if row["record_type"] == "interaction"
    ]
    return [
        {key: row[key] for key in SEMANTIC_INTERACTION_KEYS}
        for row in rows
    ]


def _semantic_session_end(path: Path) -> dict[str, Any]:
    matches = [
        row
        for row in _records(path)
        if row["record_type"] == "session_end"
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"{path}: expected exactly one session_end record"
        )
    row = matches[0]
    return {
        key: row[key]
        for key in SEMANTIC_SESSION_END_KEYS
    }


def _recorder(
    *,
    trace_path: Path,
    app: MyravantPlayApplication,
    repository_sha: str,
    session_id: str,
    restore_performed: bool,
) -> LivePlayEvidenceRecorder:
    return LivePlayEvidenceRecorder(
        trace_path=trace_path,
        header=build_live_play_session_header(
            session_id=session_id,
            campaign_id=app.fixture.campaign_id,
            repository_sha=repository_sha,
            initial_state_digest=app.authoritative_digest(),
            restore_performed=restore_performed,
            network_mode="offline",
        ),
    )


def _run_terminal_actions(
    *,
    app: MyravantPlayApplication,
    actions: tuple[str, ...],
    trace_path: Path,
    repository_sha: str,
    session_id: str,
    restore_performed: bool,
) -> dict[str, Any]:
    recorder = _recorder(
        trace_path=trace_path,
        app=app,
        repository_sha=repository_sha,
        session_id=session_id,
        restore_performed=restore_performed,
    )
    output = StringIO()
    errors = StringIO()
    raw = "\n".join((*actions, "exit")) + "\n"
    rc = run_terminal(
        app,
        input_stream=StringIO(raw),
        output_stream=output,
        evidence_recorder=recorder,
        evidence_error_stream=errors,
    )
    if rc != 0:
        raise RuntimeError(f"terminal returned {rc}")
    if errors.getvalue():
        raise RuntimeError(
            "live-play evidence failure: " + errors.getvalue()
        )
    return {
        "output": output.getvalue(),
        "interactions": _semantic_interactions(trace_path),
        "session_end": _semantic_session_end(trace_path),
        "final_digest": app.authoritative_digest(),
    }


def _entity_direct_place(
    app: MyravantPlayApplication,
    entity_id: str,
) -> str | None:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if (
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == entity_id
        )
    ]
    if not matches:
        return None
    if len(matches) != 1:
        raise RuntimeError(
            f"{entity_id}: expected at most one direct location"
        )
    return matches[0]


def _is_carried(
    app: MyravantPlayApplication,
    entity_id: str,
) -> bool:
    return any(
        relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == entity_id
        and relation.object_entity_id == app.fixture.player_entity_id
        for relation in app.state.representation.relations
    )


def _actor_place(app: MyravantPlayApplication) -> str:
    return app.entity_place_id(GROUNDSKEEPER_ID)


def _final_snapshot(app: MyravantPlayApplication) -> dict[str, Any]:
    look = app.look()
    if look.view is None:
        raise RuntimeError("final look unexpectedly lacked view")
    return {
        "authoritative_digest": app.authoritative_digest(),
        "logical_time": (
            app.runtime_state.logical_time_state.logical_position
        ),
        "player_place": app.current_place_id(),
        "groundskeeper_place": _actor_place(app),
        "lantern_carried": _is_carried(app, LANTERN_ID),
        "waystone_carried": _is_carried(app, WAYSTONE_ID),
        "waystone_direct_place": _entity_direct_place(
            app,
            WAYSTONE_ID,
        ),
        "chest_open_state": app.object_open_state(
            TOOL_CHEST_ID
        ).state,
        "lantern_lit_state": app.object_lit_state(
            LANTERN_ID
        ).state,
        "look_objects": look.view.objects,
        "look_actors": look.view.actors,
        "look_carrying": look.view.carrying,
        "look_facts": [
            {
                "entity_id": fact.entity_id,
                "entity_kind": fact.entity_kind,
                "name": fact.name,
                "description": fact.description,
                "open_state": fact.open_state,
                "lit_state": fact.lit_state,
                "visible_contents": fact.visible_contents,
            }
            for fact in look.view.observation_facts
        ],
    }


def _continuous_run(
    *,
    root: Path,
    repository_sha: str,
    token: str,
) -> dict[str, Any]:
    checkpoint = root / f"{token}-continuous-checkpoint.json"
    trace = root / f"{token}-continuous.jsonl"
    app = MyravantPlayApplication.new(
        checkpoint_path=checkpoint
    )
    session = _run_terminal_actions(
        app=app,
        actions=ALL_ACTIONS,
        trace_path=trace,
        repository_sha=repository_sha,
        session_id=f"{token}-continuous",
        restore_performed=False,
    )
    return {
        "interactions": session["interactions"],
        "session_ends": [session["session_end"]],
        "output": session["output"],
        "snapshot": _final_snapshot(app),
    }


def _restored_run(
    *,
    root: Path,
    repository_sha: str,
    token: str,
) -> dict[str, Any]:
    checkpoint = root / f"{token}-restored-checkpoint.json"
    first_trace = root / f"{token}-restored-a.jsonl"
    second_trace = root / f"{token}-restored-b.jsonl"

    app = MyravantPlayApplication.new(
        checkpoint_path=checkpoint
    )
    first = _run_terminal_actions(
        app=app,
        actions=PRE_SPLIT_ACTIONS,
        trace_path=first_trace,
        repository_sha=repository_sha,
        session_id=f"{token}-restored-a",
        restore_performed=False,
    )

    pre_restore_digest = app.authoritative_digest()
    del app

    restored = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    restored.checkpoint_path = checkpoint
    post_restore_digest = restored.authoritative_digest()

    second = _run_terminal_actions(
        app=restored,
        actions=POST_SPLIT_ACTIONS,
        trace_path=second_trace,
        repository_sha=repository_sha,
        session_id=f"{token}-restored-b",
        restore_performed=True,
    )

    return {
        "pre_restore_digest": pre_restore_digest,
        "post_restore_digest": post_restore_digest,
        "interactions": (
            first["interactions"] + second["interactions"]
        ),
        "session_ends": [
            first["session_end"],
            second["session_end"],
        ],
        "output": first["output"] + second["output"],
        "snapshot": _final_snapshot(restored),
    }


def _validate_run(
    *,
    run: dict[str, Any],
    restored: bool,
) -> list[str]:
    failures: list[str] = []
    interactions = run["interactions"]

    if len(interactions) != len(ALL_ACTIONS):
        failures.append("interaction_count_mismatch")
        return failures

    if [
        row["raw_player_input"].rstrip("\n")
        for row in interactions
    ] != list(ALL_ACTIONS):
        failures.append("action_sequence_mismatch")

    for row in interactions:
        if row["parsed_action"] in {"look", "inspect"}:
            if row["authoritative_changed"]:
                failures.append("observation_mutated_authority")
            if row["pre_state_digest"] != row["post_state_digest"]:
                failures.append("observation_digest_changed")

    wait_rows = [
        row for row in interactions
        if row["parsed_action"] == "wait"
    ]
    if [
        row["world_process_outcome"]
        for row in wait_rows
    ] != [
        "committed",
        "already_satisfied",
        "already_satisfied",
        "committed",
    ]:
        failures.append("world2_interference_outcomes_changed")

    if [
        row["logical_time_after"]
        for row in wait_rows
    ] != [1, 2, 3, 4]:
        failures.append("logical_time_sequence_changed")

    pickup_indices = [
        index
        for index, action in enumerate(ALL_ACTIONS)
        if action == "pickup waystone"
    ]
    hidden_probe = interactions[pickup_indices[0]]
    if hidden_probe["result_type"] != "custody_rejected":
        failures.append("hidden_probe_not_rejected")
    if hidden_probe["authoritative_changed"]:
        failures.append("hidden_probe_mutated_authority")
    if hidden_probe["receipt_id"] is not None:
        failures.append("hidden_probe_emitted_receipt")
    if hidden_probe["state_delta_id"] is not None:
        failures.append("hidden_probe_emitted_state_delta")
    if hidden_probe["pre_state_digest"] != hidden_probe["post_state_digest"]:
        failures.append("hidden_probe_digest_changed")
    if hidden_probe["player_visible_output"] != (
        "You cannot pick that up in the current state.\n"
    ):
        failures.append("hidden_probe_output_changed")

    unsupported = interactions[
        ALL_ACTIONS.index("throw the lantern over the wall")
    ]
    if unsupported["result_type"] != "unsupported_input":
        failures.append("unsupported_result_type_changed")
    if unsupported["failure_class"] != (
        "unsupported_capability_throwing"
    ):
        failures.append("unsupported_failure_class_changed")
    if unsupported["authoritative_changed"]:
        failures.append("unsupported_mutated_authority")
    if unsupported["pre_state_digest"] != unsupported["post_state_digest"]:
        failures.append("unsupported_digest_changed")
    if any(
        unsupported[key] is not None
        for key in (
            "command_id",
            "preview_id",
            "receipt_id",
            "state_delta_id",
        )
    ):
        failures.append("unsupported_emitted_commit_artifact")

    lawful_pickup = interactions[pickup_indices[-1]]
    if lawful_pickup["result_type"] != "custody_committed":
        failures.append("lawful_recovery_pickup_failed")
    if not lawful_pickup["authoritative_changed"]:
        failures.append("lawful_recovery_pickup_not_committed")

    visible = run["output"].casefold()
    for forbidden in (
        "world_process_",
        "command_id=",
        "receipt_id=",
        "routine_phase",
        "already_satisfied",
        "due_process_ref",
    ):
        if forbidden in visible:
            failures.append("player_output_internal_leak_" + forbidden)

    for end in run["session_ends"]:
        if not end["evidence_complete"]:
            failures.append("evidence_incomplete")
        if end["trace_write_failures"] != 0:
            failures.append("trace_write_failure")
        if end["authority_effect"] != "none":
            failures.append("evidence_claimed_authority")

    snapshot = run["snapshot"]
    if snapshot["logical_time"] != 4:
        failures.append("final_logical_time_changed")
    if snapshot["player_place"] != YARD_ID:
        failures.append("final_player_place_changed")
    if snapshot["groundskeeper_place"] != GATEHOUSE_ID:
        failures.append("final_groundskeeper_place_changed")
    if snapshot["lantern_carried"] is not True:
        failures.append("lantern_not_carried_at_end")
    if snapshot["waystone_carried"]:
        failures.append("waystone_still_carried_at_end")
    if snapshot["waystone_direct_place"] != YARD_ID:
        failures.append("waystone_relocation_not_preserved")
    if snapshot["chest_open_state"] != "open":
        failures.append("chest_final_state_changed")
    if snapshot["lantern_lit_state"] != "unlit":
        failures.append("lantern_final_lit_state_changed")
    if "Weathered Waystone" not in snapshot["look_objects"]:
        failures.append("relocated_waystone_not_visible_in_yard")

    if restored:
        if run["pre_restore_digest"] != run["post_restore_digest"]:
            failures.append("checkpoint_restore_digest_mismatch")
        if len(run["session_ends"]) != 2:
            failures.append("restored_session_count_changed")

    return sorted(set(failures))


def run_harness(repository_sha: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(
        prefix="myravant-vsm4-sustained-"
    ) as temp:
        root = Path(temp)

        continuous_a = _continuous_run(
            root=root,
            repository_sha=repository_sha,
            token="continuous-a",
        )
        continuous_b = _continuous_run(
            root=root,
            repository_sha=repository_sha,
            token="continuous-b",
        )
        restored_a = _restored_run(
            root=root,
            repository_sha=repository_sha,
            token="restored-a",
        )
        restored_b = _restored_run(
            root=root,
            repository_sha=repository_sha,
            token="restored-b",
        )

        failures: list[str] = []
        for label, run, restored in (
            ("continuous_a", continuous_a, False),
            ("continuous_b", continuous_b, False),
            ("restored_a", restored_a, True),
            ("restored_b", restored_b, True),
        ):
            failures.extend(
                f"{label}:{failure}"
                for failure in _validate_run(
                    run=run,
                    restored=restored,
                )
            )

        continuous_replay_match = (
            continuous_a["interactions"]
            == continuous_b["interactions"]
            and continuous_a["snapshot"]
            == continuous_b["snapshot"]
        )
        restored_replay_match = (
            restored_a["interactions"]
            == restored_b["interactions"]
            and restored_a["snapshot"]
            == restored_b["snapshot"]
        )
        restore_equivalence_match = (
            continuous_a["interactions"]
            == restored_a["interactions"]
            and continuous_a["snapshot"]
            == restored_a["snapshot"]
        )

        if not continuous_replay_match:
            failures.append("continuous_deterministic_replay_mismatch")
        if not restored_replay_match:
            failures.append("restored_deterministic_replay_mismatch")
        if not restore_equivalence_match:
            failures.append("save_restore_semantic_equivalence_mismatch")

        unsupported_or_rejected = sum(
            1
            for row in continuous_a["interactions"]
            if (
                row["failure_class"] is not None
                or row["result_type"].endswith("_rejected")
                or row["result_type"] == "unsupported_input"
            )
        )

        return {
            "harness_id": HARNESS_ID,
            "harness_version": HARNESS_VERSION,
            "scenario_id": SCENARIO_ID,
            "repository_sha": repository_sha,
            "model_mode": MODEL_MODE,
            "authority_effect": AUTHORITY_EFFECT,
            "actions": list(ALL_ACTIONS),
            "split_after_action": PRE_SPLIT_ACTIONS[-1],
            "summary": {
                "meaningful_interactions": len(ALL_ACTIONS),
                "unsupported_or_rejected": unsupported_or_rejected,
                "continuous_final_digest": (
                    continuous_a["snapshot"]["authoritative_digest"]
                ),
                "restored_final_digest": (
                    restored_a["snapshot"]["authoritative_digest"]
                ),
                "continuous_replay_match": continuous_replay_match,
                "restored_replay_match": restored_replay_match,
                "restore_equivalence_match": restore_equivalence_match,
                "evidence_complete": all(
                    end["evidence_complete"]
                    for run in (
                        continuous_a,
                        continuous_b,
                        restored_a,
                        restored_b,
                    )
                    for end in run["session_ends"]
                ),
                "trace_write_failures": sum(
                    end["trace_write_failures"]
                    for run in (
                        continuous_a,
                        continuous_b,
                        restored_a,
                        restored_b,
                    )
                    for end in run["session_ends"]
                ),
                "failures": sorted(set(failures)),
                "status": "PASS" if not failures else "FAIL",
            },
            "continuous": {
                "snapshot": continuous_a["snapshot"],
                "interactions": continuous_a["interactions"],
                "session_ends": continuous_a["session_ends"],
            },
            "restored": {
                "pre_restore_digest": restored_a[
                    "pre_restore_digest"
                ],
                "post_restore_digest": restored_a[
                    "post_restore_digest"
                ],
                "snapshot": restored_a["snapshot"],
                "interactions": restored_a["interactions"],
                "session_ends": restored_a["session_ends"],
            },
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--repository-sha")
    args = parser.parse_args()

    report = run_harness(
        args.repository_sha or _repo_sha()
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    summary = report["summary"]
    print(f"Harness: {HARNESS_ID} v{HARNESS_VERSION}")
    print(f"Scenario: {SCENARIO_ID}")
    print(f"Repository SHA: {report['repository_sha']}")
    print(f"MODEL mode: {MODEL_MODE}")
    print(
        "Meaningful interactions: "
        f"{summary['meaningful_interactions']}"
    )
    print(
        "Unsupported/rejected: "
        f"{summary['unsupported_or_rejected']}"
    )
    print(
        "Continuous replay match: "
        f"{summary['continuous_replay_match']}"
    )
    print(
        "Restored replay match: "
        f"{summary['restored_replay_match']}"
    )
    print(
        "Restore equivalence match: "
        f"{summary['restore_equivalence_match']}"
    )
    print(
        "Evidence complete: "
        f"{summary['evidence_complete']}"
    )
    print(
        "Trace write failures: "
        f"{summary['trace_write_failures']}"
    )
    print(f"Status: {summary['status']}")
    print(f"Report: {args.report}")

    if summary["failures"]:
        for failure in summary["failures"]:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

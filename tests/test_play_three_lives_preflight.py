"""Public-client evidence for the bounded three-life preflight (00).

This is deliberately a compatibility test, NOT a combined-campaign test.
Different checkpoints are never stitched, migrated, or reinterpreted.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from astra_runtime.myravant_activity_application import ActivityApplication
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_service_application import ServiceApplication
from astra_runtime.myravant_tarrow_investigation import create_investigation_fixture


def _identity(path):
    envelope = json.loads(path.read_text(encoding="utf-8"))
    payload = envelope["payload"]
    return {
        "format_identity": envelope["format_identity"],
        "format_version": envelope["format_version"],
        "campaign": payload["campaign"],
        "root": payload["root"],
        "final": payload["final"],
        "integrity_digest": envelope["integrity_digest"],
        "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def test_public_cross_profile_three_life_boundary_and_restarts(tmp_path):
    evidence = {
        "schema": "myravant-00-preflight-public-v1",
        "class": "developer-authored executable public-client assessment",
        "same_world_three_goal_completion": False,
        "observations": [],
        "limits": [
            "Three different valid campaigns are NOT a single persistent life",
            "No blind or human player assessment",
            "No new consent, evidence, transformation or journal semantics",
            "No uninstrumented production-performance conclusion",
        ],
    }
    head = subprocess.run(["git", "rev-parse", "HEAD"], text=True,
                          capture_output=True, timeout=15)
    evidence["repository_sha"] = head.stdout.strip() if head.returncode == 0 else None
    report_dir = os.environ.get("MYRAVANT_THREE_LIVES_REPORT_DIR")

    def flush():
        if report_dir:
            destination = Path(report_dir)
            destination.mkdir(parents=True, exist_ok=True)
            (destination / "three-lives-public.json").write_text(
                json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")

    def play(locality, path, commands, *, load=False, options=()):
        argv = [sys.executable, "-m", "astra_runtime.myravant_terminal",
                "--locality", locality, "--load" if load else "--checkpoint",
                str(path), *options]
        result = subprocess.run(argv, input=commands, capture_output=True,
                                text=True, encoding="utf-8", errors="replace",
                                timeout=120)
        evidence["observations"].append({
            "locality": locality, "mode": "restore" if load else "fresh",
            "argv": argv[1:], "raw_input": commands,
            "exit_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr,
            "checkpoint_sha256_after": (
                hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None),
        })
        flush()
        return result

    activity = tmp_path / "activity.json"
    resident = play("tarrow-activities", activity,
                    "help\ngo south\ngo west\ngo west\ngo west\n"
                    "ask oren kesh to undertake bench upkeep\nwait\n"
                    "go east\nwait\ngo west\nask oren kesh about activity\nsave\nexit\n")
    assert resident.returncode == 0, (resident.stdout, resident.stderr)
    assert activity.exists() and "bench upkeep" in resident.stdout.casefold()
    resident_before = _identity(activity)
    assert resident_before["format_identity"] == "myravant.activity-2-actor-time-material-owner-journal"
    resident_app = ActivityApplication.restore(checkpoint_path=activity)
    assert resident_app.activity_records
    assert resident_app.runtime_state.logical_time_state.logical_position > 0
    evidence["resident_before"] = resident_before
    evidence["resident_committed_clock"] = resident_app.runtime_state.logical_time_state.logical_position
    flush()

    cross_loads = []
    for other in ("tarrow-service", "tarrow-investigation",
                  "tarrow-transformation", "tarrow-structures"):
        before = activity.read_bytes()
        denied = play(other, activity, "exit\n", load=True)
        unchanged = activity.read_bytes() == before
        cross_loads.append({"target_locality": other, "exit_code": denied.returncode,
                            "original_checkpoint_unchanged": unchanged})
        assert denied.returncode == 2 and unchanged, (other, denied.stdout, denied.stderr)
        assert "Unable to restore checkpoint" in denied.stderr, (other, denied.stderr)
    evidence["cross_loads"] = cross_loads

    same_root = play("tarrow-activities", activity, "look\nsave\nexit\n", load=True)
    assert same_root.returncode == 0, (same_root.stdout, same_root.stderr)
    resident_after = _identity(activity)
    assert resident_after["root"] == resident_before["root"]
    assert resident_after["campaign"] == resident_before["campaign"]
    assert ActivityApplication.restore(checkpoint_path=activity).activity_records
    evidence["resident_after"] = resident_after
    flush()

    service = tmp_path / "service.json"
    offered = play("tarrow-service", service,
                   "go south\ngo west\noffer tali service\nsave\nexit\n")
    assert offered.returncode == 0, (offered.stdout, offered.stderr)
    fingerprint = re.search(r"Fingerprint ([0-9a-f]{64})", offered.stdout)
    assert fingerprint, offered.stdout
    participant = play("tarrow-service", service,
                       f"accept tali service version 1 fingerprint {fingerprint.group(1)}\n"
                       "give tali service peg\nwait\nwithdraw tali service\nsave\nexit\n",
                       load=True)
    assert participant.returncode == 0, (participant.stdout, participant.stderr)
    assert "Only completed attributable service is handoff-eligible." in participant.stdout
    service_app = ServiceApplication.restore(checkpoint_path=service)
    assert service_app.service_state.history[-1].state == "withdrawn"
    assert service_app.service_state.history[-1].custody_receipt is None
    evidence["service"] = _identity(service)
    flush()

    investigation = tmp_path / "investigation.json"
    investigator = play("tarrow-investigation", investigation,
                        "recall panel a residue\n"
                        "compare reports about panel a residue\nsave\nexit\n",
                        options=("--investigation-case", "neutral-relay",
                                 "--prepare-investigation"))
    assert investigator.returncode == 0, (investigator.stdout, investigator.stderr)
    assert "circumstance prepared through committed world actions" in investigator.stdout
    original = _identity(investigation)
    original_app = InvestigationApplication.restore(
        checkpoint_path=investigation,
        fixture=create_investigation_fixture("neutral-relay"))
    assert original_app.journal
    returning = play("tarrow-investigation", investigation,
                     "recall panel a residue\n"
                     "compare reports about panel a residue\nsave\nexit\n",
                     load=True, options=("--investigation-case", "neutral-relay"))
    assert returning.returncode == 0, (returning.stdout, returning.stderr)
    assert "circumstance prepared through committed world actions" not in returning.stdout
    resumed = _identity(investigation)
    assert resumed["root"] == original["root"]
    assert resumed["campaign"] == original["campaign"]
    assert InvestigationApplication.restore(
        checkpoint_path=investigation,
        fixture=create_investigation_fixture("neutral-relay")).journal
    evidence["investigation_before"] = original
    evidence["investigation_after"] = resumed

    # Positive controls are three independent campaigns, never fake integration.
    assert len({resident_after["campaign"], evidence["service"]["campaign"],
                resumed["campaign"]}) == 3
    assert len(evidence["observations"]) == 10
    evidence["result"] = "cross-specialty public checkpoint incompatibility reproduced"
    evidence["classification"] = "public profile/format/root compatibility boundary; shared procedure implementation unproven"
    flush()

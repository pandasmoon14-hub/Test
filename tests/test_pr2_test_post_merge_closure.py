# Executable validation for PR2-TEST initial activation post-merge closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"

CONTRACT = (
    ROOT
    / "docs/doctrine/control/"
    "myravant_post_r2_acceptance_evaluation_contract.md"
)

ACTIVATION_TEST = (
    ROOT
    / "tests/test_pr2_test_acceptance_evaluation_contract.py"
)

PR = 421
HEAD = "0f88e8d62e76610b52010cfa293ca20c82ba1b15"
MERGE = "0b3720ffdabd68744cec31e9b0da3aae50913972"
TREE = "2a9b783ce64110c89197702c5d4e08bd069fdb72"

CI_RUN = 242
CI_RUN_ID = 35445117897

AUTH = "owner_directive_2026-09-19_pr2_test_post_merge_closure"
EFFECT = (
    "post_r2_acceptance_evaluation_"
    "post_merge_lifecycle_reconciliation_only"
)


def load_manifest():
    return json.loads(
        MAN.read_text(
            encoding="utf-8",
        )
    )


def rows(data):
    return {
        row["workstream_id"]: row
        for row in data["workstreams"]
    }


def read_at(ref, path):
    return subprocess.check_output(
        [
            "git",
            "show",
            f"{ref}:{path.relative_to(ROOT).as_posix()}",
        ],
        cwd=ROOT,
        text=True,
    )


def test_activation_merge_metadata_is_reconciled_without_completion():
    data = load_manifest()
    test = rows(data)["PR2-TEST"]

    assert data["artifact_version"] == "0.4.60"

    assert test["status"] == "active"
    assert (
        test["completion_state"]
        == "active_evaluation_expansion"
    )

    assert test["pull_request"] == PR
    assert test["branch_head"] == HEAD
    assert test["merge_commit"] == MERGE

    assert (
        test["post_merge_closure_authorization_reference"]
        == AUTH
    )
    assert (
        test["post_merge_closure_authority_effect"]
        == EFFECT
    )
    assert (
        test["post_merge_closure_recorded_from"]
        == MERGE
    )
    assert test["post_merge_closure_tree"] == TREE

    assert (
        f"PR2-TEST GitHub Actions CI #{CI_RUN}:success"
        in test["validation_evidence"]
    )


def test_pr2_test_remains_only_active_post_r2_workstream():
    data = load_manifest()

    assert {
        row["workstream_id"]
        for row in data["workstreams"]
        if row["status"] == "active"
    } == {"PR2-TEST"}


def test_closure_preserves_downstream_authorization_boundaries():
    data = load_manifest()
    by = rows(data)
    test = by["PR2-TEST"]

    assert test["runtime_implementation_authorized"] is False
    assert test["production_schema_authorized"] is False
    assert test["pr2_impl_authorized"] is False
    assert test["r4_b_authorized"] is False
    assert test["runtime_promotion_authorized"] is False

    assert by["PR2-IMPL"]["status"] == "blocked"
    assert (
        by["PR2-IMPL"]["authorization_reference"]
        is None
    )

    assert data["r2_gate_state"]["R4-R6"] == "blocked"

    assert (
        data["r3_conformance_target"][
            "runtime_promotion_clear"
        ]
        is False
    )

    r4 = data["r4_native_substrate_design_target"]

    assert r4["r4_b_authorized"] is False
    assert r4["implementation_authorized"] is False
    assert r4["runtime_promotion_clear"] is False


def test_evaluation_contract_is_unchanged_by_closure():
    assert (
        CONTRACT.read_text(
            encoding="utf-8",
        )
        == read_at(
            MERGE,
            CONTRACT,
        )
    )


def test_activation_test_is_frozen_at_accepted_merge():
    text = ACTIVATION_TEST.read_text(
        encoding="utf-8",
    )

    assert (
        f'ACCEPTED_MERGE = "{MERGE}"'
        in text
    )

    assert "load_at(ACCEPTED_MERGE, MAN)" in text
    assert "read_at(" in text
    assert "ACCEPTED_MERGE" in text
    assert "CONTRACT" in text
    assert "PROG" in text
    assert "DEC" in text
    assert "MIG_CLOSURE_TEST" in text


def test_program_and_decision_record_bounded_activation_closure():
    program = PROG.read_text(
        encoding="utf-8",
    )
    decisions = DEC.read_text(
        encoding="utf-8",
    )

    assert "**Artifact version:** `0.4.60`" in program

    assert (
        "### 5.56 PR2-TEST initial activation "
        "post-merge closure recording"
        in program
    )

    for required in (
        AUTH,
        EFFECT,
        HEAD,
        MERGE,
        TREE,
        f"`CI #{CI_RUN}`",
        "PR2-TEST remains `active`",
        "`active_evaluation_expansion`",
        "bounded executable gap assessment",
        "PR2-IMPL remains `blocked` and unauthorized.",
        "R4-B remains unauthorized.",
        "Runtime promotion remains uncleared.",
    ):
        assert required in program

    assert (
        "PR2-TEST-INITIAL-ACTIVATION-"
        "POST-MERGE-CLOSURE-001"
        in decisions
    )

    for required in (
        AUTH,
        EFFECT,
        HEAD,
        MERGE,
        TREE,
        f"`#{CI_RUN}`",
        f"`{CI_RUN_ID}`",
        "**PR2-TEST state:** `active`",
        "**PR2-IMPL authorized:** `false`",
        "**R4-B authorized:** `false`",
        "**Runtime promotion authorized:** `false`",
    ):
        assert required in decisions




def test_closure_validation_evidence_is_exact():
    data = load_manifest()
    test = rows(data)["PR2-TEST"]

    evidence = set(test["validation_evidence"])

    required = {
        "PR2-TEST post-merge closure focused pre-certification:176 passed",
        "PR2-TEST post-merge closure broader PR2 regression:361 passed",
        (
            "PR2-TEST post-merge closure full local repository suite:"
            "9292 passed, 10 skipped, 2 xfailed, 1 warning"
        ),
        "PR2-TEST post-merge closure focused post-suite regression:176 passed",
        "PR2-TEST post-merge closure git diff --check:clean",
        "PR2-TEST post-merge closure exact six-file footprint:PASS",
        "PR2-TEST post-merge closure runtime/schema noninterference:PASS",
    }

    assert required.issubset(evidence)

    program = PROG.read_text(
        encoding="utf-8",
    )
    decisions = DEC.read_text(
        encoding="utf-8",
    )

    assert (
        "#### PR2-TEST initial activation post-merge "
        "closure validation evidence"
        in program
    )

    assert (
        "PR2-TEST-INITIAL-ACTIVATION-POST-MERGE-"
        "CLOSURE-VALIDATION-002"
        in decisions
    )

    for required_text in (
        "176 passed",
        "361 passed",
        "9292 passed, 10 skipped, 2 xfailed, 1 warning",
        "Changed paths:** `6`",
    ):
        assert required_text in decisions

def test_closure_does_not_redefine_evaluation_authority():
    flat = " ".join(
        CONTRACT.read_text(
            encoding="utf-8",
        ).split()
    )

    for required in (
        "Evaluation may demonstrate, falsify, or expose compliance; "
        "it may not create the authority, mechanic, world fact, or "
        "semantic rule being evaluated.",
        "Tests do not invent missing doctrine.",
        "Benchmark results do not create authority.",
        "No arbitrary test-count quota defines completion.",
    ):
        assert required in flat

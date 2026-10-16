"""Executable checks for the #493 content-independent coverage baseline.

The sample is author-created *discovery pressure*, not a blind Set A/B pass,
and the assertions verify evidence integrity rather than assume that all
novel attempts should be executable.
"""
from __future__ import annotations

import json

from scripts.report_myravant_action_coverage import (
    CASES, Case, observed_class, run_baseline,
)


def test_coverage_case_set_spans_distinct_methods_and_families():
    assert len(CASES) >= 35
    assert len({c.case_id for c in CASES}) == len(CASES)
    assert len({c.attempt for c in CASES}) == len(CASES)
    assert len({c.family for c in CASES}) == 12
    assert {"representable", "novelty", "ambiguous"} <= {
        c.expectation for c in CASES
    }
    movement = [
        c for c in CASES
        if c.goal == "enter yard" and c.context == "workshop"
    ]
    assert {c.method for c in movement} == {
        "walk", "sprint", "sneak", "crawl",
    }
    assert len({(c.goal, c.method, c.target, c.modifiers, c.context)
                for c in CASES}) == len(CASES)


def test_outcome_taxonomy_does_not_inflate_parsed_refusals_to_success():
    fixture = {
        "result_type": "unsupported_input",
        "authoritative_changed": False,
        "failure_class": "unsupported_input_no_executable_route",
    }
    representable = Case("T", "family", "goal", "method", "target", "",
                         "workshop", "attempt", "representable")
    novelty = Case("N", "family", "goal", "method", "target", "",
                   "workshop", "attempt2", "novelty")
    assert observed_class(representable, fixture) == "false_unsupported_candidate"
    assert observed_class(novelty, fixture) == "unsupported_novelty"
    fixture["result_type"] = "actor_mediated_movement_rejected"
    assert observed_class(novelty, fixture) == "contextual_refusal"
    fixture["failure_class"] = None
    assert observed_class(novelty, fixture) == "observed_no_change"
    fixture["authoritative_changed"] = True
    assert observed_class(novelty, fixture) == "executed"
    fixture["result_type"] = "ambiguous_input"
    fixture["authoritative_changed"] = False
    assert observed_class(novelty, fixture) == "clarification_needed"


def test_real_installed_subset_preserves_trace_and_checkpoint(tmp_path):
    ids = {
        "S01",  # self inspection / read-only local state
        "M01",  # existing walk to a real place
        "M03",  # unfamiliar locomotion method
        "I01",  # physical custody
        "F03",  # durable chest service and time
        "N01",  # sourced claim to co-present actor
        "D01",  # WORLD-2 time
        "P01",  # posture pressure
        "Q01",  # two-step command pressure
    }
    selected = tuple(c for c in CASES if c.case_id in ids)
    assert len(selected) == len(ids)
    path = tmp_path / "baseline.json"
    result = run_baseline(output=path, cases=selected)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded == result
    assert result["not_independent_blind_set_a_b"]
    assert result["not_human_play"]
    assert result["case_count"] == len(ids)
    assert result["family_count"] >= 7
    assert sum(result["observed_outcomes"].values()) == len(ids)
    assert {x["case_id"] for x in result["cases"]} == ids

    for item in result["cases"]:
        assert len(item["pre_state_digest"]) == 64
        assert len(item["post_state_digest"]) == 64
        assert len(item["checkpoint_sha256"]) == 64
        assert len(item["trace_sha256"]) == 64
        assert item["attempt"] and item["player_visible_output"]
        if item["authoritative_changed"]:
            assert item["pre_state_digest"] != item["post_state_digest"]
        else:
            assert item["pre_state_digest"] == item["post_state_digest"]
        assert item["outcome"] not in {"uninterpretable", "false_unsupported_candidate"} or (
            item["expectation"] != "representable"
        ), "a representable known fixture action failed its interpreter baseline"

    known = {x["case_id"]: x for x in result["cases"]}
    for id_ in ("S01", "M01", "I01", "F03", "N01", "D01"):
        assert known[id_]["outcome"] in {
            "executed", "observed_no_change", "contextual_refusal",
        }, (id_, known[id_])
    assert known["M01"]["outcome"] == "executed"
    assert known["S01"]["outcome"] == "observed_no_change"
    assert known["D01"]["outcome"] == "executed"

"""Feedback-conditioned synthetic players against the installed Myravant client.

This is not human play and not a copied donor scenario. It is executable
behavioral pressure grounded in six *distinct* documented actual-play sources
summarized in docs/evidence/myravant_synthetic_play_discovery_2.md.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


# A policy step is either a literal player attempt or:
# (observation substring, attempt if observed, attempt otherwise).
# Branches are evaluated against the *preceding live terminal response*.
# The goals and methods are independently Myravant-native.
PLAYER_POLICIES = {
    "questioning_explorer": (
        "look",
        ("Groundskeeper", "ask groundskeeper who passed this way", "look south"),
        ("not here", "walk south", "ask groundskeeper what they remember"),
        ("Yard", "examine the tool chest", "move south"),
        ("Brass Lantern", "look at the lantern", "search for old tracks"),
        "check for tracks around the gatehouse",
        "move south",
        ("Gatehouse", "ask groundskeeper to follow me", "move south"),
        "look",
        ("follows", "head north", "ask the groundskeeper to follow me"),
        "ask groundskeeper whether the traveler is expected",
        "inspect waystone",
        "look east",
        "move north",
        "look",
        "ask groundskeeper to stop following me",
        "wait",
        "look",
    ),
    "social_relationship_builder": (
        "look",
        ("Groundskeeper", "ask groundskeeper for a conversation", "move south"),
        "introduce myself as a traveling carpenter",
        "ask the groundskeeper about their family",
        "move south",
        "ask groundskeeper to follow me",
        ("follows", "invite groundskeeper to visit my workshop", "ask groundskeeper to follow me"),
        "look",
        "ask groundskeeper to tell me their name",
        "make an agreement to meet tomorrow",
        "head north",
        "ask groundskeeper to stop following me",
        "write down a promise",
        "wait",
        "ask groundskeeper to remember my favor",
        "look",
        "inspect groundskeeper",
        "ask groundskeeper for lantern",
    ),
    "persistent_craftsperson": (
        "look",
        ("Brass Lantern", "pickup lantern", "go south"),
        "plan to repair a broken cart",
        "look",
        "move south",
        "inspect chest",
        ("Brass Lantern", "put lantern in chest", "open the chest"),
        "examine tool chest",
        "wait",
        "check whether the cart repair has progressed",
        "move north",
        "look",
        "take lantern from chest",
        "use a tool to shape a wooden spoke",
        "work at the workshop for a full day",
        "look",
        "make a record of the finished parts",
        "wait",
    ),
    "reticent_peacemaker": (
        "look",
        "tell the groundskeeper that I do not want a fight",
        "move south",
        "request safe passage without threatening anyone",
        "look",
        "move south",
        ("Groundskeeper", "ask groundskeeper to go to yard", "head north"),
        "offer the groundskeeper my lantern as a peace token",
        "ask groundskeeper to follow me",
        "move north",
        "look",
        "offer to mediate a disagreement",
        "ask groundskeeper to stop following me",
        "move east",
        "check whether anyone needs shelter",
        "wait",
        "look",
        "return to an earlier promise",
    ),
    "uncertain_wayfinder": (
        "look",
        "look south",
        ("Yard", "head south", "inspect the waystone"),
        "where does the western path lead",
        "look east",
        "go east",
        "look",
        "move south",
        "look",
        "move north",
        "head east",
        "look west",
        "mark the safest route on my map",
        "move west",
        "look",
        "look north",
        "wait",
        "return by the route I mapped",
    ),
    "vow_and_failed_plan": (
        "look",
        "promise to keep the yard safe through the winter",
        "ask whether anyone can witness my oath",
        "move south",
        "try to resolve the dispute by petition",
        "move south",
        "look",
        ("Groundskeeper", "ask groundskeeper to follow me", "look north"),
        "ask the groundskeeper to take responsibility for the gatehouse",
        "head north",
        "look",
        "is my oath complete",
        "wait",
        "look",
        "ask groundskeeper to stop following me",
        "reconsider my obligation after the setback",
        "head east",
        "look",
    ),
    "coordinated_planner": (
        "look",
        "assign one party member to watch the road",
        "assign another companion to inspect the workshop",
        "move south",
        "ask groundskeeper to investigate the yard",
        "move south",
        "ask groundskeeper to follow me",
        ("follows", "move north", "ask groundskeeper to follow me"),
        "look",
        "leave a message for the scout",
        "split the party to follow two leads",
        "move east",
        "look",
        "ask the scout what they discovered",
        "wait",
        "look",
        "call the party back together",
        "change our objective based on the new information",
    ),
    "risk_and_consequence_tester": (
        "look",
        "assess whether the gate is guarded",
        "move south",
        "try crossing the yard without being seen",
        "look",
        "move south",
        "ask groundskeeper to light lantern",
        "try to frighten the groundskeeper away",
        "ask groundskeeper to follow me",
        "move north",
        "look",
        "investigate who witnessed my earlier trespass",
        "move east",
        "look",
        "wait",
        "ask whether the witness changed their story",
        "return to repair the harm I caused",
        "look",
    ),
}

SOURCE_TO_POLICY = {
    "questioning_explorer": "D20-video-transcript-investigation",
    "social_relationship_builder": "D20-video-transcript-role-identity",
    "persistent_craftsperson": "OSR-written-session-report-livelihood",
    "reticent_peacemaker": "Paizo-play-by-post-travel-risk",
    "uncertain_wayfinder": "Paizo-play-by-post-map-locality",
    "vow_and_failed_plan": "Ironsworn-solo-journal-vow-setback",
    "coordinated_planner": "Magpies-podcast-transcript-split-plan",
    "risk_and_consequence_tester": "Magpies-podcast-transcript-multi-stage-consequence",
}


def _read_prompt(stdout):
    data = ""
    while not data.endswith("\n> "):
        character = stdout.read(1)
        if character == "":
            raise AssertionError("Installed Myravant client exited before next decision: " + data[-1500:])
        data += character
        if len(data) > 30000:
            raise AssertionError("No Myravant prompt after 30000 output characters")
    return data


def _scripted_seed(checkpoint):
    executable = shutil.which("myravant-play")
    assert executable is not None
    run = subprocess.run(
        [executable, "--checkpoint", str(checkpoint)],
        input="move south\nmove south\nsave\nexit\n",
        capture_output=True, text=True, timeout=45,
    )
    assert run.returncode == 0, (run.stdout, run.stderr)
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5


def _play_live(persona, checkpoint, trace, *, seeded):
    executable = shutil.which("myravant-play")
    assert executable is not None
    argv = [
        executable, "--checkpoint", str(checkpoint), "--trace", str(trace),
        "--repository-sha", "e" * 40,
    ]
    if seeded:
        argv.extend(["--load", str(checkpoint)])
    process = subprocess.Popen(
        argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, bufsize=1,
    )
    assert process.stdin is not None and process.stdout is not None
    assert process.stderr is not None
    commands, responsive = [], []
    try:
        previous = _read_prompt(process.stdout)
        for i, decision in enumerate(PLAYER_POLICIES[persona]):
            if isinstance(decision, tuple):
                needle, present, absent = decision
                observed = needle.casefold() in previous.casefold()
                action = present if observed else absent
                responsive.append((i, needle, observed, action))
            else:
                action = decision
            process.stdin.write(action + "\n")
            process.stdin.flush()
            previous = _read_prompt(process.stdout)
            commands.append(action)
        process.stdin.write("save\n")
        process.stdin.flush()
        saved_output = _read_prompt(process.stdout)
        process.stdin.write("exit\n")
        process.stdin.flush()
        process.stdin.close()
        remaining = process.stdout.read()
        code = process.wait(timeout=45)
        errors = process.stderr.read()
        assert code == 0, (persona, commands, saved_output, remaining, errors)
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=10)

    assert "Checkpoint written." in saved_output
    raw = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
    assert raw[0]["record_type"] == "session_start"
    assert raw[-1]["record_type"] == "session_end"
    interactions = [x for x in raw if x["record_type"] == "interaction"]
    assert len(interactions) == len(commands) + 1
    assert [x["raw_player_input"] for x in interactions] == [
        x + "\n" for x in [*commands, "save"]
    ]
    assert len(responsive) >= 1
    assert all(x["pre_state_digest"] and x["post_state_digest"] for x in interactions)
    assert all(
        not x["authoritative_changed"] or x["pre_state_digest"] != x["post_state_digest"]
        for x in interactions
    )
    app = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert app.authoritative_digest() == interactions[-1]["post_state_digest"]
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
    return {
        "persona": persona, "pressure_source": SOURCE_TO_POLICY[persona],
        "seeded": seeded, "commands": commands, "responsive": responsive,
        "transitions": [
            (x["parsed_action"], x["result_type"], x["failure_class"],
             x["authoritative_changed"], x["pre_state_digest"], x["post_state_digest"])
            for x in interactions
        ],
        "checkpoint": checkpoint.read_bytes(),
    }


@pytest.mark.parametrize("persona", sorted(PLAYER_POLICIES))
@pytest.mark.parametrize("seeded", (False, True), ids=("starting_workshop", "starting_gatehouse"))
def test_feedback_driven_synthetic_player_is_reproducible(tmp_path, persona, seeded):
    outcomes = []
    for iteration in ("alpha", "beta"):
        checkpoint = tmp_path / (iteration + ".json")
        trace = tmp_path / (iteration + ".jsonl")
        if seeded:
            _scripted_seed(checkpoint)
        observed = _play_live(persona, checkpoint, trace, seeded=seeded)
        assert len(observed["commands"]) == 18
        assert len(observed["responsive"]) >= 1
        assert any(t[3] for t in observed["transitions"]), persona
        assert any(not t[3] for t in observed["transitions"]), persona
        outcomes.append(observed)
        # Genuine second-process load: observation and re-save must not modify
        # the authoritative checkpoint or replay duplicate world effects.
        before = checkpoint.read_bytes()
        executable = shutil.which("myravant-play")
        resumed = subprocess.run(
            [executable, "--load", str(checkpoint),
             "--checkpoint", str(checkpoint)],
            input="look\nsave\nexit\n",
            capture_output=True, text=True, timeout=45,
        )
        assert resumed.returncode == 0, (persona, resumed.stdout, resumed.stderr)
        assert checkpoint.read_bytes() == before
    assert outcomes[0] == outcomes[1]


def test_location_context_changes_synthetic_player_decisions(tmp_path):
    persona = "questioning_explorer"
    workshop = _play_live(
        persona, tmp_path / "workshop.json", tmp_path / "workshop.jsonl",
        seeded=False,
    )
    gatehouse_checkpoint = tmp_path / "gatehouse.json"
    _scripted_seed(gatehouse_checkpoint)
    gatehouse = _play_live(
        persona, gatehouse_checkpoint, tmp_path / "gatehouse.jsonl",
        seeded=True,
    )
    # The same exploratory goal changes its very next method after observation.
    assert workshop["commands"][1] != gatehouse["commands"][1]
    assert workshop["responsive"][0][2] != gatehouse["responsive"][0][2]

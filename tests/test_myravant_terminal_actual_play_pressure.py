"""Actual-play-informed pressure on the *installed* Myravant terminal.

Independent behavioral pressures, not donor dialogue, rules, characters, or
content. Sources read 2026-10-09:
- The Adventure Zone pilot transcript (player-directed off-plot ambitions):
  https://theadventurezone.fandom.com/wiki/Ep._1:_Here_There_Be_Gerblins_-_Chapter_One/Transcript
- Critical Role, Crimson Diplomacy (negotiation, deception, physical position):
  https://criticalrole.fandom.com/wiki/Crimson_Diplomacy/Transcript
- Critical Role, A Dance of Deception (coordinated social and physical plans):
  https://criticalrole.fandom.com/wiki/A_Dance_of_Deception/Transcript
- Glass Cannon, Blood of the Wild 39 (nonviolent creature/environment approach):
  https://podcastrex.com/shows/the-glass-cannon-podcast/charms-and-mojo-sticks-blood-of-the-wild-s1-e39-pathfinder-2e-quest-for-the-frozen-flame

These are scripted automated probes through the real console, NOT observations of
humans playing Myravant. Refusal here marks a playable-capability gap rather than
proving that the player's proposed action is fictionally impossible.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys

import pytest

from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _launch(lines, *args, installed=True):
    if installed:
        binary = shutil.which("myravant-play")
        assert binary is not None, "The actual installed entrypoint is required"
        argv = [binary]
    else:
        argv = [sys.executable, "-m", "astra_runtime.myravant_terminal"]
    return subprocess.run(
        [*argv, *args],
        input="\n".join([*lines, "exit", ""]),
        capture_output=True,
        text=True,
        timeout=120,
    )


def _trace(path):
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert records[0]["record_type"] == "session_start"
    assert records[-1]["record_type"] == "session_end"
    return [record for record in records if record["record_type"] == "interaction"]


# Outside the currently executable bounded fixture: attempt varied *methods*
# and goals. Exactly these words are not the point; protecting committed state
# under unscripted input is. New capabilities should reclassify these in a
# separately justified future package, not silently mutate today.
ACTUAL_PLAY_PRESSURES = {
    "social_and_deception": (
        "persuade the groundskeeper to let me through",
        "ask the groundskeeper why the gatehouse is guarded",
        "offer a deal for the lantern",
        "bribe the groundskeeper with a favor",
        "lie about why I need the lantern",
        "pretend I am the groundskeeper's supervisor",
        "apologize to the groundskeeper",
        "threaten to expose the groundskeeper",
        "befriend the groundskeeper",
        "challenge the groundskeeper to a wager",
        "ask what the groundskeeper knows about the orchard",
        "promise to bring the lantern back",
    ),
    "investigation_and_uncertainty": (
        "search the ground for footprints",
        "listen at the workshop door",
        "eavesdrop on the groundskeeper",
        "look under the tool chest",
        "search the lantern for an inscription",
        "follow the tracks into the woods",
        "check if the groundskeeper is lying",
        "test whether the chest has a false bottom",
        "smell the lantern oil",
        "taste the water",
        "roll to notice a hidden passage",
        "recall a rumor about the gatehouse",
    ),
    "creative_physical_methods": (
        "climb onto the roof",
        "build a ladder from loose timber",
        "use the lantern to signal the groundskeeper",
        "tie a rope around the chest",
        "jam the door shut with a stone",
        "break the lantern to start a fire",
        "sneak past the groundskeeper",
        "hide behind the chest",
        "throw a pebble to distract the groundskeeper",
        "dig beneath the wall",
        "dismantle the tool chest",
        "make a torch from scraps",
    ),
    "relationships_and_consequences": (
        "recruit the groundskeeper as an ally",
        "ask the groundskeeper to betray a friend",
        "offer the groundskeeper a permanent job",
        "ask the groundskeeper to remember my name",
        "leave a written note on the chest",
        "mark the gatehouse as my home",
        "claim ownership of the lantern",
        "forgive the groundskeeper",
        "interrogate the groundskeeper",
        "teach the groundskeeper a signal",
        "command the groundskeeper to forget our conversation",
        "negotiate permission to camp in the yard",
    ),
    "tactical_and_noncombat_solutions": (
        "calm the frightened animal",
        "distract a guard with food",
        "disarm the trap without touching it",
        "block the east exit",
        "use the weather to cover my tracks",
        "escort a traveler to safety",
        "heal the groundskeeper",
        "attack the groundskeeper",
        "parry the next attack",
        "retreat quietly",
        "set a decoy near the orchard",
        "barter for passage",
    ),
    "long_horizon_and_world_scale": (
        "invent a new kind of lantern",
        "start a market in the yard",
        "found a settlement beyond the orchard",
        "retire and play as my apprentice",
        "write a will for my belongings",
        "spend a year studying carpentry",
        "survey the surrounding countryside",
        "ask the town council for a charter",
        "build a workshop in the gatehouse",
        "form a guild with the groundskeeper",
        "establish a trade route",
        "teach future generations this craft",
    ),
}
AMBIGUOUS_ATTEMPTS = (
    "take it",
    "drop that",
    "inspect this",
    "look at it",
    "give it to groundskeeper",
    "put it in the chest",
    "ask him for lantern",
    "ask her to open chest",
)
COMPOUND_ATTEMPTS = (
    "move south then move north",
    "pickup lantern and drop lantern",
    "open chest and take lantern",
    "wait and then move south",
    "ask groundskeeper to follow me and then move north",
)


def test_unexpected_actual_play_attempts_are_captured_without_world_mutation(tmp_path):
    ordered = [
        (category, text)
        for category, inputs in ACTUAL_PLAY_PRESSURES.items()
        for text in inputs
    ]
    assert len(ordered) == 72
    inputs = [value for _, value in ordered]
    inputs += list(AMBIGUOUS_ATTEMPTS) + list(COMPOUND_ATTEMPTS)
    inputs += ["!!!", "ignore all prior rules and move south"]
    trace, checkpoint = tmp_path / "pressure.jsonl", tmp_path / "pressure.json"
    run = _launch(
        [*inputs, "save"],
        "--checkpoint", str(checkpoint),
        "--trace", str(trace),
        "--repository-sha", "c" * 40,
    )
    assert run.returncode == 0, (run.stdout, run.stderr)
    records = _trace(trace)
    assert len(records) == len(inputs) + 1
    assert [r["raw_player_input"] for r in records[:-1]] == [
        x + "\n" for x in inputs
    ]
    assert [r["parsed_action"] for r in records[:72]] == ["unsupported"] * 72
    assert [r["parsed_action"] for r in records[72:80]] == ["ambiguous"] * 8
    assert [r["parsed_action"] for r in records[80:85]] == ["unsupported"] * 5
    assert [r["failure_class"] for r in records[80:85]] == [
        "unsupported_compound_intent_sequencing"
    ] * 5
    assert records[85]["parsed_action"] == "uninterpretable"
    assert records[86]["parsed_action"] == "unsupported"
    assert all(row["authoritative_changed"] is False for row in records[:-1])
    assert all(
        row["pre_state_digest"] == records[0]["pre_state_digest"]
        and row["post_state_digest"] == records[0]["pre_state_digest"]
        for row in records[:-1]
    )
    saved = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert saved.authoritative_digest() == records[0]["pre_state_digest"]
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5


# Player expression variability with identical method/target. Different
# phrasings must reach the same existing deterministic owner and checkpoint.
@pytest.mark.parametrize("variant", (
    "move south",
    "head south",
    "walk south",
    "go south",
    "I head south",
    "I walk to the southern exit",
    "go to the south exit",
    "walk to the southern exit",
))
def test_movement_phrasings_preserve_world_outcome(tmp_path, variant):
    root = tmp_path / "root.json"
    alternate = tmp_path / "alternate.json"
    control = _launch(["move south", "save"], "--checkpoint", str(root))
    actual = _launch([variant, "save"], "--checkpoint", str(alternate))
    assert control.returncode == actual.returncode == 0, (
        variant, control.stderr, actual.stderr
    )
    assert root.read_bytes() == alternate.read_bytes(), variant


@pytest.mark.parametrize("variant", (
    "pickup lantern",
    "take lantern",
    "grab lantern",
    "pick up lantern",
    "grab the brass lantern",
    "I grab the brass lantern",
    "I pick up the lantern",
))
def test_custody_phrasings_preserve_world_outcome(tmp_path, variant):
    root = tmp_path / "root.json"
    alternate = tmp_path / "alternate.json"
    control = _launch(["pickup lantern", "save"], "--checkpoint", str(root))
    actual = _launch([variant, "save"], "--checkpoint", str(alternate))
    assert control.returncode == actual.returncode == 0, (
        variant, control.stderr, actual.stderr
    )
    assert root.read_bytes() == alternate.read_bytes(), variant


# Unlike unsupported probes, these attempt sustained, consequential sequences.
# Deliberately intermingle requests, refusals, changes of mind, observation,
# time passage, and resumption. No donor scenario/content is reconstructed.
SUSTAINED_CAMPAIGNS = {
    "equipment_and_finding": (
        "look", "inspect lantern", "look south", "take the lantern",
        "inspect chest", "move south", "look", "open chest", "inspect chest",
        "put lantern into chest", "look", "move north", "look",
        "move south", "open chest", "retrieve lantern from chest", "look",
        "close chest", "move south", "look", "give lantern to groundskeeper",
        "ask groundskeeper for lantern", "look", "wait", "look",
    ),
    "follow_and_reconsider": (
        "ask groundskeeper to follow me", "look", "move south", "look",
        "move south", "ask groundskeeper to follow me", "look",
        "ask groundskeeper to follow me", "move north", "look", "move east",
        "look", "ask groundskeeper to stop following me", "look",
        "move west", "look", "move south", "ask groundskeeper to follow me",
        "move north", "move east", "wait", "look",
    ),
    "social_and_spatial_refusals": (
        "ask groundskeeper to light lantern", "persuade the groundskeeper",
        "ask groundskeeper to go to yard", "move south", "look",
        "ask groundskeeper to follow me", "move south", "look",
        "ask groundskeeper to walk to the yard",
        "ask groundskeeper to throw lantern east",
        "ask groundskeeper to light lantern",
        "ask groundskeeper to pick up lantern", "look", "wait",
        "move north", "look", "move south", "look",
        "ask groundskeeper to stop following me",
    ),
    "travel_and_time": (
        "look", "wait", "look", "wait", "move south", "look", "wait",
        "move north", "wait", "move south", "move south", "look",
        "wait", "move north", "move east", "look", "wait",
        "move west", "move north", "wait", "look", "inspect lantern",
    ),
    "unknown_actions_then_recovery": (
        "climb onto the roof", "take it", "move south then move north",
        "look", "grab brass lantern", "look", "move south",
        "hide behind the chest", "look", "put lantern in chest", "look",
        "move south", "ask groundskeeper to follow me", "look",
        "move north", "move east", "look", "!!!",
        "move west", "look", "wait", "look",
    ),
    "npc_item_and_storage_lifecycle": (
        "pickup lantern", "move south", "move south",
        "give lantern to groundskeeper", "look",
        "ask groundskeeper to light lantern", "look",
        "ask groundskeeper to drop lantern", "look",
        "ask groundskeeper to pick up lantern", "look",
        "ask groundskeeper to go to yard", "look", "wait",
        "move north", "look", "move south", "look",
        "ask groundskeeper to store lantern in chest", "wait", "look",
    ),
}


@pytest.mark.parametrize("name", sorted(SUSTAINED_CAMPAIGNS))
def test_sustained_terminal_campaign_replay_and_restart(tmp_path, name):
    commands = SUSTAINED_CAMPAIGNS[name]
    outcomes = []
    for repetition in ("first", "second"):
        checkpoint = tmp_path / f"{name}-{repetition}.json"
        trace = tmp_path / f"{name}-{repetition}.jsonl"
        launch = _launch(
            [*commands, "save"],
            "--checkpoint", str(checkpoint),
            "--trace", str(trace),
            "--repository-sha", "d" * 40,
        )
        assert launch.returncode == 0, (name, repetition, launch.stdout, launch.stderr)
        interactions = _trace(trace)
        assert len(interactions) == len(commands) + 1
        assert all(
            row["pre_state_digest"] and row["post_state_digest"]
            for row in interactions
        )
        assert any(row["authoritative_changed"] for row in interactions), name
        assert any(not row["authoritative_changed"] for row in interactions), name
        assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
        persisted = checkpoint.read_bytes()
        restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
        assert restored.authoritative_digest() == interactions[-1]["post_state_digest"]

        resumed_trace = tmp_path / f"{name}-{repetition}-restart.jsonl"
        resumed = _launch(
            ["look", "save"], "--load", str(checkpoint),
            "--checkpoint", str(checkpoint), "--trace", str(resumed_trace),
            "--repository-sha", "d" * 40, installed=False,
        )
        assert resumed.returncode == 0, (name, repetition, resumed.stdout, resumed.stderr)
        assert checkpoint.read_bytes() == persisted, name
        assert all(
            not row["authoritative_changed"]
            for row in _trace(resumed_trace)
        )
        outcomes.append((persisted, [
            (row["parsed_action"], row["result_type"], row["authoritative_changed"],
             row["pre_state_digest"], row["post_state_digest"])
            for row in interactions
        ]))
    assert outcomes[0] == outcomes[1], name

"""BREADTH-1: executable player-centered sensory diversity, not lexical breadth.

AFQR-20 derives only near-field object evidence, distinct from visual sight,
actual carried object state, NPC sensing and durable world truth.
"""
from __future__ import annotations

import subprocess
import sys

import pytest

from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, PLAYER_ID, TOOL_CHEST_ID, WAYSTONE_ID, YARD_ID,
    MyravantPlayFixtureError, UnavailableFixtureCustodyError,
)
from astra_runtime.myravant_player_sensory_breadth import (
    parse_player_sensory_attempt,
    execute_player_sensory_attempt,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def test_dark_grounded_waystone_can_be_touched_without_visual_truth():
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    pre = app.authoritative_digest()
    unseen = app.inspect("waystone")
    assert unseen.failure_class == "inspection_target_unavailable"
    touched = app.feel_for_local_object("waystone")
    assert touched.result_type == "player_contact_observed"
    assert not touched.authoritative_changed
    assert touched.observation_evidence_id
    assert "contact" in touched.message
    assert "not contents" in touched.message
    assert app.authoritative_digest() == pre
    assert app.knowledge_state.events == ()
    assert app.duty_state.events == ()


def test_player_tactile_contact_requires_grounded_local_explicit_target():
    app = MyravantVSM14Application.new()
    before = app.authoritative_digest()
    for name, failure in (
        ("chest", "player_contact_opportunity_unavailable"),
        ("waystone", "player_contact_opportunity_unavailable"),
        ("unknown trinket", "player_contact_target_unavailable"),
        ("it", "player_contact_ambiguous_target"),
        ("lantern", "player_contact_affordance_unavailable"),
        ("groundskeeper", "player_contact_target_unavailable"),
    ):
        denied = app.feel_for_local_object(name)
        assert denied.failure_class == failure
        assert denied.message == (
            "You cannot establish direct contact with that target here."
        )
        assert denied.pre_state_digest == denied.post_state_digest == before
    assert app.authoritative_digest() == before


def test_real_relocation_changes_tactile_opportunity_without_caching():
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    original = app.feel_for_local_object("chest")
    assert original.result_type == "player_contact_observed"
    assert app.displace_object(
        "chest", "north", method="push",
    ).authoritative_changed
    at_old_site = app.feel_for_local_object("chest")
    assert at_old_site.failure_class == "player_contact_opportunity_unavailable"
    assert app.move("north").authoritative_changed
    newly_here = app.feel_for_local_object("chest")
    assert newly_here.result_type == "player_contact_observed"
    assert newly_here.observation_evidence_id != original.observation_evidence_id


def test_holdings_report_actual_custody_not_invented_body_or_hidden_objects():
    app = MyravantVSM14Application.new()
    before = app.authoritative_digest()
    empty = app.inspect_personal_holdings()
    assert empty.result_type == "player_holdings_observed"
    assert "not carrying" in empty.message
    assert empty.pre_state_digest == empty.post_state_digest == before

    assert app.pickup("lantern").authoritative_changed
    held = app.inspect_personal_holdings()
    assert "Brass Lantern" in held.message
    assert "unlit" in held.message
    assert "hands" not in held.message
    assert app.light_object("lantern").authoritative_changed
    glowing = app.inspect_personal_holdings()
    assert "lit" in glowing.message
    assert "unlit" not in glowing.message
    assert app.drop("lantern").authoritative_changed
    assert "not carrying" in app.inspect_personal_holdings().message


def test_observer_authorization_preserves_groundkeeper_c3_evidence():
    app = MyravantVSM14Application.new()
    fixture = app.fixture
    with pytest.raises(MyravantPlayFixtureError):
        fixture.player_contact_evidence(
            observer_entity_id=GROUNDSKEEPER_ID,
            target_entity_id=TOOL_CHEST_ID,
            place_id=YARD_ID, target_grounded_here=True,
        )
    with pytest.raises(MyravantPlayFixtureError):
        fixture.actor_contact_evidence(
            observer_entity_id=PLAYER_ID,
            target_entity_id=TOOL_CHEST_ID,
            place_id=YARD_ID, target_grounded_here=True,
        )
    with pytest.raises(UnavailableFixtureCustodyError):
        fixture.player_contact_evidence(
            observer_entity_id=PLAYER_ID,
            target_entity_id=app.fixture.resolve_object_reference("lantern"),
            place_id=YARD_ID, target_grounded_here=True,
        )


def test_read_only_sensing_preserves_checkpoint_and_world_replay(tmp_path):
    checkpoint = tmp_path / "player-senses.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    first = app.feel_for_local_object("waystone")
    report = app.inspect_personal_holdings()
    assert first.observation_evidence_id
    assert "Lantern" in report.message
    prior = app.authoritative_digest()
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == prior
    second = restored.feel_for_local_object("waystone")
    assert second.observation_evidence_id == first.observation_evidence_id
    assert restored.inspect_personal_holdings().message == report.message
    assert restored.authoritative_digest() == prior


@pytest.mark.parametrize("utterance, expected_operation, expected_target", [
    ("touch the chest", "contact", "chest"),
    ("touch tool chest", "contact", "tool chest"),
    ("feel for waystone", "contact", "waystone"),
    ("feel around for the waystone", "contact", "waystone"),
    ("search by touch for the chest", "contact", "chest"),
    ("locate the tool chest by touch", "contact", "tool chest"),
    ("run my hand along chest", "contact", "chest"),
    ("run your hands along the chest", "contact", "chest"),
    ("look at my hands", "holdings", ""),
    ("what am i holding", "holdings", ""),
    ("examine what i am carrying", "holdings", ""),
    ("check my belongings", "holdings", ""),
    ("check what i'm carrying", "holdings", ""),
    ("look down at my belongings", "holdings", ""),
    ("feel for it", "contact", "it"),
    ("touch the lantern", "contact", "lantern"),
    ("feel for groundskeeper", "contact", "groundskeeper"),
    ("locate the unknown artifact by touch", "contact", "unknown artifact"),
])
def test_independent_representation_probes_preserve_attempt_anatomy(
    utterance, expected_operation, expected_target,
):
    assert parse_player_sensory_attempt(utterance) == (
        expected_operation, expected_target,
    )


def test_adversarial_non_capture_and_specific_refusal():
    app = MyravantVSM14Application.new()
    for unrelated in (
        "ask groundskeeper to touch chest",
        "ask groundskeeper to inspect chest",
        "search for lantern",
        "touch someone by magic",
        "walk south",
        "stand still",
        "go south and touch chest",
        "grab lantern",
        "look at chest",
        "feel sorry for someone",
    ):
        # Touch-targeted unfamiliar attempts must retain safe semantics,
        # while actor requests and unrelated verbs stay with their owners.
        if unrelated == "touch someone by magic":
            assert parse_player_sensory_attempt(unrelated) == (
                "contact", "someone by magic",
            )
            rejected = execute_player_sensory_attempt(app, unrelated)
            assert rejected.failure_class == "player_contact_target_unavailable"
        else:
            assert parse_player_sensory_attempt(unrelated) is None
    before = app.authoritative_digest()
    denied = execute_player_sensory_attempt(app, "feel for it")
    assert denied.failure_class == "player_contact_ambiguous_target"
    assert app.authoritative_digest() == before


def test_installed_client_two_sessions_and_darkness(tmp_path):
    checkpoint = tmp_path / "breadth-player-sense.json"

    def run(commands, *flags):
        return subprocess.run(
            [sys.executable, "-m", "astra_runtime.myravant_terminal", *flags],
            input="\n".join((*commands, "exit", "")),
            text=True, capture_output=True, timeout=90,
        )

    first = run((
        "check my hands", "go south", "go east",
        "look at waystone", "feel around for waystone",
        "touch it",
    ), "--checkpoint", str(checkpoint))
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "not carrying" in first.stdout
    assert "You make direct contact" in first.stdout
    assert "cannot establish direct contact" in first.stdout
    assert checkpoint.exists()
    later = run((
        "search by touch for waystone", "go west",
        "touch chest",
    ), "--load", str(checkpoint))
    assert later.returncode == 0, (later.stdout, later.stderr)
    assert later.stdout.count("You make direct contact") == 2


def test_qualified_contact_does_not_create_visual_or_memory_event():
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    contact = execute_player_sensory_attempt(app, "locate waystone by touch")
    assert contact.result_type == "player_contact_observed"
    sight = app.focused_observation("waystone")
    assert sight.failure_class == "focused_target_not_observed"
    assert app.knowledge_state.events == ()
    assert app.runtime_state.logical_time_state.logical_position == 0

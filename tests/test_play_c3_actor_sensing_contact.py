"""C-3: NPC-owned sight evidence versus nonvisual, transient local contact.

No universal tactile physics, no new memory event meaning, and no extra
checkpoint format: the fixture licenses near-field contact for two objects.
"""
from __future__ import annotations

import subprocess
import sys

import pytest

from astra_runtime.myravant_c1_investigation_goal import parse_actor_memory_request
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, ORCHARD_PATH_ID, TOOL_CHEST_ID, WAYSTONE_ID,
    MyravantPlayFixtureError, create_terminal_play_fixture,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_vsm14_follow_intent import (
    execute_vsm14_follow_request,
)


def _meet_keeper(app: MyravantVSM14Application) -> None:
    assert app.move("south").authoritative_changed
    assert app.wait().authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == app.current_place_id()


def _enter_dark_orchard_with_keeper(app: MyravantVSM14Application) -> None:
    assert app.pickup("lantern").authoritative_changed
    _meet_keeper(app)
    assert execute_vsm14_follow_request(
        app, "ask groundskeeper to follow me",
    ).result.authoritative_changed
    assert app.move("east").authoritative_changed
    assert app.current_place_id() == ORCHARD_PATH_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == ORCHARD_PATH_ID


def test_visual_witness_is_actor_qualified_and_has_own_observation_receipt():
    app = MyravantVSM14Application.new()
    _meet_keeper(app)
    player_sensing = app.visual_observation_evidence(TOOL_CHEST_ID)
    assert player_sensing.observer_entity_id == app.fixture.player_entity_id
    assert player_sensing.observable
    actor_sensing = app.fixture.actor_visual_observation_evidence(
        observer_entity_id=GROUNDSKEEPER_ID,
        target_entity_id=TOOL_CHEST_ID,
        place_id=app.current_place_id(),
        local_light_available=app._bounded_local_light_available(),
    )
    assert actor_sensing.observer_entity_id == GROUNDSKEEPER_ID
    assert actor_sensing.observable
    assert actor_sensing.evidence_id != player_sensing.evidence_id

    witnessed = app.actor_memory_interaction("witness", "chest")
    assert witnessed.authoritative_changed
    assert witnessed.observation_evidence_id == actor_sensing.evidence_id
    assert witnessed.receipt_id and witnessed.command_id
    assert app.knowledge_state.events[-1].source_kind == "witnessed"

    fixture = create_terminal_play_fixture()
    with pytest.raises(MyravantPlayFixtureError):
        fixture.visual_observation_evidence(
            observer_entity_id=GROUNDSKEEPER_ID,
            target_entity_id=TOOL_CHEST_ID,
            place_id=app.current_place_id(),
            local_light_available=True,
        )
    with pytest.raises(MyravantPlayFixtureError):
        fixture.actor_visual_observation_evidence(
            observer_entity_id=fixture.player_entity_id,
            target_entity_id=TOOL_CHEST_ID,
            place_id=app.current_place_id(),
            local_light_available=True,
        )


def test_dark_contact_succeeds_without_forging_historical_visual_memory(tmp_path):
    checkpoint = tmp_path / "c3-dark.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _enter_dark_orchard_with_keeper(app)
    old = app.authoritative_digest()
    unavailable_sight = app.actor_memory_interaction("witness", "waystone")
    assert unavailable_sight.failure_class == (
        "actor_knowledge_witness_opportunity_unavailable"
    )
    assert not unavailable_sight.authoritative_changed
    assert app.authoritative_digest() == old

    physical = app.actor_memory_interaction("touch", "waystone")
    assert physical.result_type == "actor_contact_observed"
    assert "by touch" in physical.message
    assert physical.observation_evidence_id
    assert not physical.authoritative_changed
    assert physical.pre_state_digest == physical.post_state_digest == old
    assert app.knowledge_state.events == ()
    assert app.actor_memory_interaction(
        "last_saw", "waystone",
    ).failure_class == "actor_knowledge_unknown"

    # The sensory result was an opportunity-bound observation, not an
    # authoritative new fact falsely replayed as "the actor saw it."
    app.save()
    recovered = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert recovered.authoritative_digest() == old
    assert recovered.knowledge_state.events == ()
    assert recovered.actor_memory_interaction(
        "last_saw", "waystone",
    ).failure_class == "actor_knowledge_unknown"
    assert recovered.actor_memory_interaction(
        "touch", "waystone",
    ).observation_evidence_id == physical.observation_evidence_id

    assert recovered.light_object("lantern").authoritative_changed
    seen = recovered.actor_memory_interaction("witness", "waystone")
    assert seen.authoritative_changed
    assert seen.observation_evidence_id
    assert len(recovered.knowledge_state.events) == 1
    assert recovered.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == recovered.authoritative_digest()
    assert "Orchard Path" in restored.actor_memory_interaction(
        "last_saw", "waystone",
    ).message


def test_contact_refuses_remote_target_and_unlicensed_object_without_leaks():
    app = MyravantVSM14Application.new()
    original = app.authoritative_digest()
    remote = app.actor_memory_interaction("touch", "chest")
    assert remote.failure_class == "actor_knowledge_actor_not_local"
    assert "Yard" not in remote.message
    assert app.authoritative_digest() == original
    _meet_keeper(app)
    original = app.authoritative_digest()
    missing = app.actor_memory_interaction("touch", "waystone")
    assert missing.failure_class == "actor_contact_opportunity_unavailable"
    assert "Orchard" not in missing.message
    unlicensed = app.actor_memory_interaction("touch", "lantern")
    assert unlicensed.failure_class == "actor_contact_opportunity_unavailable"
    assert not missing.authoritative_changed
    assert not unlicensed.authoritative_changed
    assert app.authoritative_digest() == original
    assert app.knowledge_state.events == ()


def test_contact_is_requalified_against_actual_object_displacement(tmp_path):
    checkpoint = tmp_path / "c3-displacement.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _meet_keeper(app)
    physical = app.actor_memory_interaction("touch", "chest")
    assert physical.observation_evidence_id
    assert not physical.authoritative_changed
    assert app.displace_object("chest", "north", method="push").authoritative_changed
    prior = app.authoritative_digest()
    absent = app.actor_memory_interaction("touch", "chest")
    assert absent.failure_class == "actor_contact_opportunity_unavailable"
    assert app.authoritative_digest() == prior
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == prior
    again = restored.actor_memory_interaction("touch", "chest")
    assert again.failure_class == "actor_contact_opportunity_unavailable"
    assert restored.knowledge_state.events == ()


def test_parser_preserves_memory_recall_and_actor_physical_methods():
    assert parse_actor_memory_request(
        "ask groundskeeper to touch chest",
    ) == ("touch", "chest", None)
    assert parse_actor_memory_request(
        "ask the groundskeeper to feel waystone",
    ) == ("touch", "waystone", None)
    assert parse_actor_memory_request(
        "ask groundskeeper to check chest by touch",
    ) == ("touch", "chest", None)
    assert parse_actor_memory_request(
        "ask groundskeeper to inspect chest",
    ) == ("witness", "chest", None)
    assert parse_actor_memory_request(
        "ask groundskeeper where they last saw chest",
    ) == ("last_saw", "chest", None)
    for unrelated in (
        "ask groundskeeper to go to gatehouse",
        "ask groundskeeper to follow me",
        "ask groundskeeper to pick up chest",
        "ask groundskeeper for chest",
        "touch chest",
    ):
        assert parse_actor_memory_request(unrelated) is None


def test_installed_dark_tactile_then_visual_recovery_is_durable(tmp_path):
    checkpoint = tmp_path / "c3-terminal.json"

    def session(commands, *args):
        return subprocess.run(
            [sys.executable, "-m", "astra_runtime.myravant_terminal", *args],
            input="\n".join((*commands, "exit", "")), text=True,
            capture_output=True, timeout=90,
        )

    first = session((
        "pickup lantern",
        "go south",
        "wait",
        "ask groundskeeper to follow me",
        "go east",
        "ask groundskeeper to touch waystone",
        "ask groundskeeper to inspect waystone",
        "ask groundskeeper where they last saw waystone",
    ), "--checkpoint", str(checkpoint))
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "confirms by touch" in first.stdout
    assert "cannot directly verify" in first.stdout
    assert "no qualified record" in first.stdout
    checkpoint_one = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert checkpoint_one.knowledge_state.events == ()

    second = session((
        "light lantern",
        "ask groundskeeper to inspect waystone",
        "ask groundskeeper where they last saw waystone",
    ), "--load", str(checkpoint))
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert "directly observes" in second.stdout
    assert "Orchard Path" in second.stdout
    checkpoint_two = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert len(checkpoint_two.knowledge_state.events) == 1
    assert checkpoint_two.knowledge_state.events[0].source_kind == "witnessed"
    assert checkpoint_two.save().checkpoint_digest
    assert MyravantVSM14Application.restore(
        checkpoint_path=checkpoint
    ).authoritative_digest() == checkpoint_two.authoritative_digest()

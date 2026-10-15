"""PLAY-TRIAL-1: integrated Orchard provisioning without a new owner.

Methods differ across player carriage/WORLD-2, grounded COMP-3, voluntary
actor VSM-13, RT-010 containment and AFQR-19 opportunity; no "quest success"
ledger can replace physical world truth. All fixture facts remain noncanonical.
"""
from __future__ import annotations

import subprocess
import sys

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    containment_relation_for,
)
from astra_runtime.myravant_orchard_supply_goal import (
    execute_orchard_supply_attempt, parse_orchard_supply_attempt,
)
from astra_runtime.myravant_physical_placement_goal import (
    execute_physical_placement_goal,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, LANTERN_ID, ORCHARD_PATH_ID,
    PLAYER_ID, TOOL_CHEST_ID, WAYSTONE_ID, WORKSHOP_ID, YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _at_yard_with_lantern(app):
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.current_place_id() == YARD_ID


def _grounded(app, item, place):
    return any(
        rel.subject_entity_id == item and rel.object_entity_id == place
        and rel.relation_type == LOCATED_AT_RELATION_TYPE
        for rel in app.state.representation.relations
    )


def _carried(app, item, actor):
    return any(
        rel.subject_entity_id == item and rel.object_entity_id == actor
        and rel.relation_type == CARRIED_BY_RELATION_TYPE
        for rel in app.state.representation.relations
    )


def _last_displacement(app):
    return app.displacement_state.committed_object_displacement_transitions[-1].receipt


@pytest.mark.parametrize("raw,method,is_status", [
    ("supply orchard with lantern", None, False),
    ("I want to provision the orchard path with the brass lantern", None, False),
    ("how can i supply orchard using lantern?", None, False),
    ("supply orchard with lantern by carrying it", "carry", False),
    ("stock orchard with the lantern using walking with it", "carry", False),
    ("provision orchard with lantern via throwing it", "throw", False),
    ("supply orchard path with lantern by tossing it", "throw", False),
    ("supply orchard with lantern by asking groundskeeper", "actor_throw", False),
    ("supply orchard with lantern by pushing the loaded chest", "chest_push", False),
    ("stock orchard with lantern by pushing the chest", "chest_push", False),
    ("supply orchard with lantern by opening chest", "open_chest", False),
    ("supply orchard with lantern by retrieving lantern from chest", "retrieve", False),
    ("supply orchard with lantern by dropping the lantern", "drop", False),
    ("supply orchard with lantern via teleporting", "unqualified", False),
    ("check orchard supply", None, True),
    ("check orchard lantern supply", None, True),
    ("what supplies are at the orchard?", None, True),
])
def test_attempt_parser_preserves_method_and_distinct_status(raw,method,is_status):
    parsed = parse_orchard_supply_attempt(raw)
    assert parsed is not None
    assert parsed.raw_text == raw
    assert parsed.method == method
    assert parsed.is_status is is_status


@pytest.mark.parametrize("raw", [
    "get lantern to orchard by pushing",
    "move the chest to orchard by pushing",
    "clear yard east exit by pushing waystone north",
    "give lantern to groundskeeper",
    "ask groundskeeper to throw lantern east",
    "supply town with lantern",
    "provision gatehouse with lantern",
    "supply orchard with chest",
    "supply orchard with lantern and then go east",
    "supply orchard with lantern by throwing and then look",
    "supply orchard with that",
    "stock orchard with lantern by a new spell and wait",
])
def test_supply_does_not_capture_other_goals_compounds_or_assume_magic(raw):
    assert parse_orchard_supply_attempt(raw) is None


def test_player_carriage_yields_world_movement_and_persistent_hold(tmp_path):
    app = MyravantVSM14Application.new(checkpoint_path=tmp_path/"carry.json")
    _at_yard_with_lantern(app)
    before = app.authoritative_digest()
    advice = execute_orchard_supply_attempt(app, "supply orchard with lantern")
    assert advice.result_type == "orchard_supply_observed"
    assert not advice.authoritative_changed
    assert "You currently carry" in advice.message
    assert advice.pre_state_digest == advice.post_state_digest == before

    actual = execute_orchard_supply_attempt(
        app, "supply orchard with lantern by carrying it",
    )
    assert actual.authoritative_changed
    assert actual.result_type == "movement_committed"
    assert actual.receipt_id and actual.state_delta_id
    assert app.current_place_id() == ORCHARD_PATH_ID
    assert _carried(app, LANTERN_ID, PLAYER_ID)
    status = execute_orchard_supply_attempt(app, "check orchard supply")
    assert "still carry it" in status.message
    assert status.pre_state_digest == status.post_state_digest

    dropped = execute_orchard_supply_attempt(
        app, "supply orchard with lantern by dropping the lantern",
    )
    assert dropped.authoritative_changed
    assert _grounded(app, LANTERN_ID, ORCHARD_PATH_ID)
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _grounded(restored, LANTERN_ID, ORCHARD_PATH_ID)


def test_throw_same_goal_without_relocating_player_and_with_real_receipt(tmp_path):
    app = MyravantVSM14Application.new(checkpoint_path=tmp_path/"throw.json")
    _at_yard_with_lantern(app)
    before = app.authoritative_digest()
    thrown = execute_orchard_supply_attempt(
        app,"supply orchard with lantern by throwing it",
    )
    assert thrown.authoritative_changed
    assert thrown.result_type == "object_displacement_committed"
    assert thrown.pre_state_digest == before
    assert app.current_place_id() == YARD_ID
    assert _grounded(app,LANTERN_ID,ORCHARD_PATH_ID)
    receipt=_last_displacement(app)
    assert receipt.actor_entity_id == PLAYER_ID
    assert receipt.method=="throw"
    assert receipt.source_relation_type==CARRIED_BY_RELATION_TYPE
    assert receipt.receipt_id==thrown.receipt_id
    assert app.save().checkpoint_digest
    restored=MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest()==app.authoritative_digest()
    assert _last_displacement(restored)==receipt


def test_actor_cooperation_rejects_remote_or_wrong_custody_then_commits(tmp_path):
    app=MyravantVSM14Application.new(checkpoint_path=tmp_path/"actor.json")
    _at_yard_with_lantern(app)
    first=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by asking groundskeeper",
    )
    assert first.failure_class=="vsm13_requested_actor_not_local"
    assert not first.authoritative_changed
    assert app.wait().authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID)==YARD_ID
    before=app.authoritative_digest()
    refused=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by asking groundskeeper",
    )
    assert refused.failure_class=="vsm13_comp3_opportunity_unavailable"
    assert app.authoritative_digest()==before
    assert app.give_object("lantern","groundskeeper").authoritative_changed
    committed=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by asking groundskeeper",
    )
    assert committed.authoritative_changed
    assert committed.result_type=="actor_mediated_displacement_committed"
    receipt=_last_displacement(app)
    assert receipt.actor_entity_id==GROUNDSKEEPER_ID
    assert receipt.method=="throw"
    assert receipt.receipt_id==committed.receipt_id
    assert _grounded(app,LANTERN_ID,ORCHARD_PATH_ID)
    assert app.save().checkpoint_digest
    restored=MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest()==app.authoritative_digest()
    assert _last_displacement(restored)==receipt


def test_loaded_chest_requires_closure_then_can_be_unpacked(tmp_path):
    app=MyravantVSM14Application.new(checkpoint_path=tmp_path/"sealed.json")
    _at_yard_with_lantern(app)
    assert app.open_object("chest").authoritative_changed
    assert app.store_object("lantern","chest").authoritative_changed
    relation=containment_relation_for(app.storage_state,LANTERN_ID)
    assert relation is not None and relation.object_entity_id==TOOL_CHEST_ID

    before=app.authoritative_digest()
    open_refusal=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by pushing the loaded chest",
    )
    assert open_refusal.failure_class=="object_displacement_opportunity_unavailable"
    assert app.authoritative_digest()==before
    assert app.close_object("chest").authoritative_changed

    moved=execute_orchard_supply_attempt(
        app,"stock orchard with lantern by pushing the chest",
    )
    assert moved.authoritative_changed
    assert moved.result_type=="object_displacement_committed"
    assert _grounded(app,TOOL_CHEST_ID,ORCHARD_PATH_ID)
    assert containment_relation_for(app.storage_state,LANTERN_ID)==relation
    receipt=_last_displacement(app)
    assert receipt.method=="push" and receipt.receipt_id==moved.receipt_id

    assert app.move("east").authoritative_changed
    visible=execute_orchard_supply_attempt(app,"check orchard supply")
    # Orchard Path has insufficient ambient visual signal; a sealed
    # container never grants a false observation of its interior.
    assert "No presently observable" in visible.message

    opening=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by opening chest",
    )
    assert opening.authoritative_changed
    recovered=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by retrieving lantern from chest",
    )
    assert recovered.authoritative_changed
    assert _carried(app,LANTERN_ID,PLAYER_ID)
    assert containment_relation_for(app.storage_state,LANTERN_ID) is None
    assert app.save().checkpoint_digest
    restored=MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest()==app.authoritative_digest()
    assert _grounded(restored,TOOL_CHEST_ID,ORCHARD_PATH_ID)
    assert _carried(restored,LANTERN_ID,PLAYER_ID)
    assert _last_displacement(restored)==receipt


def test_unverified_claimed_cargo_moves_only_real_chest_not_imagined_lantern(tmp_path):
    """Counterexample: hidden cargo truth must not be exposed by push eligibility.

    The goal states a belief about contents, but the only authoritative
    outcome is the existing qualified chest push, not 'supplies delivered'.
    """
    app = MyravantVSM14Application.new(
        checkpoint_path=tmp_path / "claimed-cargo.json",
    )
    assert app.move("south").authoritative_changed
    before = app.authoritative_digest()
    moved = execute_orchard_supply_attempt(
        app, "supply orchard with lantern by pushing the loaded chest",
    )
    assert moved.authoritative_changed
    assert moved.result_type == "object_displacement_committed"
    assert moved.message == "You push the Tool Chest east."
    assert moved.pre_state_digest == before
    assert moved.receipt_id == _last_displacement(app).receipt_id
    assert _grounded(app, TOOL_CHEST_ID, ORCHARD_PATH_ID)
    # Lantern was never in the Chest; intent does not materialize cargo.
    assert _grounded(app, LANTERN_ID, WORKSHOP_ID)
    assert containment_relation_for(app.storage_state, LANTERN_ID) is None
    assert app.move("east").authoritative_changed
    inquiry = execute_orchard_supply_attempt(app, "check orchard supply")
    assert not inquiry.authoritative_changed
    assert "No presently observable Lantern supply" in inquiry.message
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(
        checkpoint_path=app.checkpoint_path,
    )
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _grounded(restored, LANTERN_ID, WORKSHOP_ID)
    assert _grounded(restored, TOOL_CHEST_ID, ORCHARD_PATH_ID)


def test_route_blocker_distinguishes_carriage_from_qualified_throw_and_clearing():
    app=MyravantVSM14Application.new()
    # Make a local usable light signal, then recover the Waystone from the
    # Orchard Path. That physically blocks the Yard east walking route.
    assert app.pickup("lantern").authoritative_changed
    assert app.light_object("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    assert execute_physical_placement_goal(
        app,"get waystone to yard by dragging",
    ).authoritative_changed
    assert app.move("west").authoritative_changed
    assert _grounded(app,WAYSTONE_ID,YARD_ID)
    before=app.authoritative_digest()
    blocked=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by carrying it",
    )
    assert not blocked.authoritative_changed
    assert blocked.failure_class
    assert app.authoritative_digest()==before
    advice=execute_orchard_supply_attempt(app,"supply orchard with lantern")
    assert "obstructs the east passage" in advice.message
    assert advice.pre_state_digest==advice.post_state_digest

    thrown=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by throwing it",
    )
    assert thrown.authoritative_changed
    assert _grounded(app,LANTERN_ID,ORCHARD_PATH_ID)
    assert not app.move("east").authoritative_changed
    cleared=execute_physical_placement_goal(
        app,"clear yard east exit by pushing the waystone north",
    )
    assert cleared.authoritative_changed
    assert _grounded(app,WAYSTONE_ID,WORKSHOP_ID)
    assert app.move("east").authoritative_changed
    assert app.current_place_id()==ORCHARD_PATH_ID


def test_unsupported_method_and_unloading_location_fail_closed():
    app=MyravantVSM14Application.new()
    initial=app.authoritative_digest()
    bad=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by teleporting",
    )
    assert bad.failure_class=="orchard_supply_method_unqualified"
    assert bad.pre_state_digest==bad.post_state_digest==initial
    offsite=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by carrying it",
    )
    assert offsite.failure_class=="orchard_supply_start_not_local"
    unload=execute_orchard_supply_attempt(
        app,"supply orchard with lantern by opening chest",
    )
    assert unload.failure_class=="orchard_supply_unload_not_local"
    assert app.authoritative_digest()==initial


def test_same_multimethod_play_replays_with_identical_causal_footprint():
    timelines=[]
    for _ in range(2):
        app=MyravantVSM14Application.new()
        _at_yard_with_lantern(app)
        advice=execute_orchard_supply_attempt(
            app,"supply orchard with lantern",
        )
        assert not advice.authoritative_changed
        a=execute_orchard_supply_attempt(
            app,"stock orchard with lantern by throwing it",
        )
        assert a.authoritative_changed
        assert app.move("east").authoritative_changed
        b=execute_orchard_supply_attempt(app,"check orchard supply")
        assert not b.authoritative_changed
        timelines.append((advice.message,a.receipt_id,a.command_fingerprint,
                          b.message,app.authoritative_digest()))
    assert timelines[0]==timelines[1]


def test_installed_terminal_two_session_supply_and_recovery(tmp_path):
    checkpoint=tmp_path/"orchard-provision.json"
    def run(commands,*flags):
        return subprocess.run(
            [sys.executable,"-m","astra_runtime.myravant_terminal",*flags],
            input="\n".join((*commands,"exit","")),capture_output=True,
            text=True,timeout=120,
        )
    first=run((
        "take lantern", "go south",
        "supply orchard with lantern",
        "supply orchard with lantern by carrying it",
        "check orchard supply",
    ),"--checkpoint",str(checkpoint))
    assert first.returncode==0,(first.stdout,first.stderr)
    assert "You currently carry the Lantern" in first.stdout
    assert "still carry it" in first.stdout
    assert checkpoint.is_file()
    restored=MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.current_place_id()==ORCHARD_PATH_ID
    assert _carried(restored,LANTERN_ID,PLAYER_ID)

    second=run((
        "supply orchard with lantern by dropping the lantern",
        "check orchard supply",
    ),"--load",str(checkpoint))
    assert second.returncode==0,(second.stdout,second.stderr)
    after=MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert _grounded(after,LANTERN_ID,ORCHARD_PATH_ID)
    assert not _carried(after,LANTERN_ID,PLAYER_ID)


def test_authored_adversarial_attempts_do_not_fabricate_actions_or_truth():
    app=MyravantVSM14Application.new()
    before=app.authoritative_digest()
    # These are pressure probes, not an independent held-out score.
    probes=(
        "supply orchard with lantern by borrowing a flying animal",
        "supply orchard with lantern by teleporting",
        "provision orchard with lantern by pushing the loaded chest",
        "check orchard supply",
        "supply orchard with lantern by taking it from chest",
    )
    for phrase in probes:
        parsed=parse_orchard_supply_attempt(phrase)
        if parsed is None:
            continue
        result=execute_orchard_supply_attempt(app,phrase)
        assert not result.authoritative_changed
        assert result.pre_state_digest==result.post_state_digest==before
    assert app.authoritative_digest()==before

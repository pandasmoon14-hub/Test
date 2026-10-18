"""Integrated environmental depth; authored evidence, not independent play."""
from collections import deque
from dataclasses import replace
from io import StringIO
import shutil
import subprocess

import pytest

from astra_runtime.myravant_play_application import MyravantPlayApplication as App
from astra_runtime.myravant_play_fixture import MyravantPlayFixtureError, FixtureMovementRoute
from astra_runtime.myravant_terminal import run_terminal
from astra_runtime.myravant_tarrow import Place, create_tarrow_fixture, identity
from astra_runtime.myravant_tarrow_environment import (
    POSITIONS, FITTINGS, MATERIALS, create_environment_fixture, environment_layout,
    execute_environment_request,
)


def play(a, *commands):
    out = StringIO()
    assert run_terminal(a, input_stream=StringIO("\n".join((*commands,"exit",""))),
                        output_stream=out, specialized_router=execute_environment_request) == 0
    return out.getvalue()


def new(path=None):
    return App.new(fixture=create_environment_fixture(), checkpoint_path=path)


def clear_access(a):
    assert a.pickup("shuttered service lamp").authoritative_changed
    assert a.light_object("shuttered service lamp").authoritative_changed
    assert a.move("south").authoritative_changed
    assert a.displace_object("delivery basket", "west", method="push").authoritative_changed


def reach(a, destination):
    todo = deque([(a.current_place_id(), [])]); seen = set()
    while todo:
        node, steps = todo.popleft()
        if node == identity(destination):
            for direction in steps:
                assert a.move(direction).authoritative_changed
            return
        if node in seen:
            continue
        seen.add(node)
        todo.extend((r.destination_place_id, steps+[r.direction]) for r in a.fixture.movement_routes
                    if r.source_place_id == node)
    raise AssertionError("No admitted route to " + destination)


def restore(a):
    a.save()
    b = App.restore(fixture=a.fixture, checkpoint_path=a.checkpoint_path)
    assert b.authoritative_digest() == a.authoritative_digest()
    return b


def test_inventory_and_v1_compatibility():
    f=create_environment_fixture(); old=create_tarrow_fixture()
    assert len(f.place_presentations)==28 and len(f.object_presentations)==38
    assert len(f.position_areas)==16 and len(f.movement_routes)==48
    assert len(f.actor_presentations)==7
    assert old.campaign_id == "astra:campaign:tarrow-locality-v1-11128d469368b172ba3a"
    assert old.provenance.initial_state_digest == "3e0600288f21dc3bbba408d9d52701bd0637b936d4d4330b3c0897de5e1ac5bc"
    assert f.campaign_id != old.campaign_id
    assert not f.provenance.canon


@pytest.mark.parametrize("key,area,name,description", POSITIONS)
def test_each_position_changes_authoritative_context_and_restores(tmp_path,key,area,name,description):
    a=new(tmp_path / "position.json"); clear_access(a); reach(a,key)
    assert a.current_place_id()==identity(key)
    assert dict(a.fixture.position_areas)[identity(key)]==identity(area)
    text=play(a,"look","inspect self")
    assert name in text and "\\n" not in text
    assert restore(a).current_place_id()==identity(key)


@pytest.mark.parametrize("key,name,description,place", FITTINGS)
def test_fittings_are_observable_but_not_ordinary_custody(tmp_path,key,name,description,place):
    a=new(tmp_path / "fitting.json"); clear_access(a); reach(a,place)
    before=a.authoritative_digest()
    assert a.inspect(name).view.description.startswith(description)
    result=a.pickup(name)
    assert not result.authoritative_changed and result.failure_class
    assert a.authoritative_digest()==before
    restore(a)


@pytest.mark.parametrize("method", ["push","slide"])
def test_clearance_methods_preserve_hidden_cargo_and_later_reblock(tmp_path,method):
    a=new(tmp_path / "clearance.json")
    play(a,"go south")
    before=a.authoritative_digest()
    refused=play(a,"approach underbank threshold")
    assert "obstructs" in refused and a.authoritative_digest()==before
    text=play(a,f"{method} delivery basket west", "look")
    assert "Service Cord" not in text and "Packing Cloth" not in text
    assert a.approach_place("underbank threshold").authoritative_changed
    assert a.approach_place("service yard").authoritative_changed
    assert a.approach_place("yard tool station").authoritative_changed
    assert a.displace_object("delivery basket","east",method=method).authoritative_changed
    assert a.approach_place("service yard").authoritative_changed
    before=a.authoritative_digest()
    assert a.approach_place("underbank threshold").failure_class
    assert a.authoritative_digest()==before
    b=restore(a)
    assert b.approach_place("underbank threshold").failure_class
    assert sum(r.subject_entity_id==identity("cord") and r.object_entity_id==identity("basket")
               for r in b.state.representation.relations)==1


def test_container_state_qualifies_movement_and_cargo_survives(tmp_path):
    a=new(tmp_path / "tray.json"); clear_access(a); reach(a,"work-bench")
    assert a.open_object("parts tray").authoritative_changed
    before=a.authoritative_digest()
    assert a.displace_object("parts tray","east",method="push").failure_class
    assert a.authoritative_digest()==before
    text=play(a,"close parts tray then push parts tray east")
    assert "step 1/2: You close" in text and "step 2/2: You push" in text
    assert a.inspect("parts tray").failure_class  # Visible history grants no permanent reach.
    assert a.approach_place("workshop workroom").authoritative_changed
    assert a.open_object("parts tray").authoritative_changed
    assert "Wooden Peg" in play(a,"inspect parts tray")
    b=restore(a)
    assert b.retrieve_object("wooden peg","parts tray").authoritative_changed
    assert b.store_object("wooden peg","parts tray").authoritative_changed
    restore(b)


def test_observation_and_interaction_have_different_reach_and_light(tmp_path):
    a=new(tmp_path / "sight.json"); clear_access(a); reach(a,"underbank")
    # A light carried at the observer's position does not illuminate the next.
    text=play(a,"look east")
    assert "Objects:" not in text and "Floodmark Post" not in text
    assert a.inspect("floodmark post").failure_class
    assert a.approach_place("floodmark position").authoritative_changed
    assert a.inspect("floodmark post").view
    assert a.approach_place("underbank walk").authoritative_changed
    assert a.inspect("floodmark post").failure_class
    reach(a,"yard-tools")
    # This independently declared sightline supports seeing, not pickup.
    seen=play(a,"look north")
    assert "Sorting Rack" in seen and "Sorting Tray" in seen
    before=a.authoritative_digest()
    assert a.pickup("sorting rack").failure_class
    assert a.authoritative_digest()==before


def test_goal_method_reuses_declared_routes_and_requalifies(tmp_path):
    a=new(tmp_path / "goal.json"); play(a,"go south")
    before=a.authoritative_digest()
    advice=play(a,"get delivery basket to yard tool station")
    assert "push west" in advice and "slide west" in advice
    assert a.authoritative_digest()==before
    text=play(a,"get delivery basket to yard tool station by sliding then approach underbank threshold")
    assert "You slide" in text and a.current_place_id()==identity("yard-threshold")
    assert restore(a).current_place_id()==identity("yard-threshold")


@pytest.mark.parametrize("raw", [
    "approach service stores", "approach wayhouse household", "approach east bank track",
    "approach deck inspection edge", "approach common threshold quietly",
    "approach notice recess and take document box", "approach unknown position",
])
def test_named_movement_cannot_plan_teleport_or_drop_constraints(raw):
    a=new(); before=a.authoritative_digest()
    play(a,raw)
    assert a.authoritative_digest()==before


def test_ambiguous_corridors_and_parent_labels_rejected():
    f=create_environment_fixture()
    with pytest.raises(MyravantPlayFixtureError,match="corridors"):
        replace(f,movement_routes=f.movement_routes+(f.movement_routes[0],))
    with pytest.raises(MyravantPlayFixtureError,match="presentation areas"):
        replace(f,position_areas=((identity("common"),identity("common")),))


def test_additional_position_and_container_require_only_declarations(tmp_path):
    base=environment_layout()
    layout=replace(base,version="neutral-extension-test",
        places=base.places+(Place("test-alcove","Validation Alcove","An explicitly declared test recess.","test","noncanonical"),),
        edges=base.edges+(("common-shelf","east","test-alcove"),("test-alcove","west","common-shelf")),
        objects=base.objects+(("test-jar","Validation Jar","An empty declared container.","test-alcove"),),
        open_states=base.open_states+(("test-jar","closed"),),
        positions=base.positions+(("test-alcove","common"),),
        storage=base.storage+(("folio","test-jar"),))
    a=App.new(fixture=create_tarrow_fixture(layout=layout),checkpoint_path=tmp_path/"extension.json")
    reach(a,"common-shelf")
    assert a.approach_place("validation alcove").authoritative_changed
    assert a.open_object("validation jar").authoritative_changed
    assert a.store_object("weatherproof field folio","validation jar").authoritative_changed
    b=restore(a)
    assert b.retrieve_object("weatherproof field folio","validation jar").authoritative_changed


def test_public_descriptions_do_not_reveal_hidden_truth_or_infer_physics(tmp_path):
    a=new(tmp_path / "privacy.json"); clear_access(a); reach(a,"yard-sorting")
    before=a.authoritative_digest()
    text=play(a,"inspect sorting rack", "inspect soft-iron pin blank", "search for soft-iron pin blank",
              "detach sorting rack", "tie service cord to deck edge rail")
    assert "behind the" not in text and "failed linkage pin" not in text
    assert a.authoritative_digest()==before


def test_installed_depth_entry_and_campaign_separation(tmp_path):
    cli=shutil.which("myravant-play"); assert cli
    path=tmp_path/"depth.json"
    args=[cli,"--locality","tarrow-depth","--checkpoint",str(path)]
    r=subprocess.run(args,input="go south\nslide delivery basket west then approach underbank threshold\nwait\nsave\nexit\n",
                     capture_output=True,text=True,timeout=45)
    assert r.returncode==0,r.stderr
    assert "Underbank Threshold" in r.stdout and "Time passes." in r.stdout
    good=subprocess.run([cli,"--locality","tarrow-depth","--load",str(path)],
                        input="look\nexit\n",capture_output=True,text=True,timeout=45)
    assert good.returncode==0,good.stderr
    old=subprocess.run([cli,"--locality","tarrow","--load",str(path)],
                       input="exit\n",capture_output=True,text=True,timeout=45)
    assert old.returncode==2 and "Unable to restore" in old.stderr


def test_unordered_multiple_container_and_light_states_restore_without_changes(tmp_path):
    layout=environment_layout()
    layout=replace(layout,version="plural-state-calibration",
        objects=layout.objects+(("calibration-light","Calibration Light","A declared test light.","common"),),
        lit_states=(("lamp","unlit"),("calibration-light","unlit")))
    f=create_tarrow_fixture(layout=layout)
    a=App.new(fixture=f,checkpoint_path=tmp_path/"plural.json")
    b=restore(a)  # No open/lit transition should be invented to make this load.
    assert not b.object_state.committed_object_state_transitions
    assert not b.lit_state.committed_object_lit_transitions
    assert b.light_object("calibration light").authoritative_changed
    c=restore(b)
    assert c.object_lit_state(identity("calibration-light")).state=="lit"
    assert c.object_lit_state(identity("lamp")).state=="unlit"


def test_canonical_state_comparison_still_rejects_a_real_state_difference(tmp_path):
    from astra_runtime.domain.persistent_world_local_checkpoint_restore import PersistentWorldCheckpointEvidenceError
    a=new(tmp_path/"baseline.json");a.save()
    f=a.fixture
    changed=replace(f,initial_object_open_states=tuple(replace(s,state="open")
        if s.object_entity_id==identity("basket") else s for s in f.initial_object_open_states))
    with pytest.raises(PersistentWorldCheckpointEvidenceError,match="replayed"):
        App.restore(fixture=changed,checkpoint_path=a.checkpoint_path)


def test_only_first_step_is_durable_after_a_later_opportunity_refusal(tmp_path):
    a=new(tmp_path/"partial-depth.json");play(a,"go south")
    text=play(a,"open delivery basket then push delivery basket west")
    assert "step 1/2: You open" in text and "must be closed" in text
    b=restore(a)
    assert b.object_open_state(identity("basket")).state=="open"
    assert b.approach_place("underbank threshold").failure_class


def test_position_acknowledgement_requires_durable_save(tmp_path,monkeypatch):
    a=new(tmp_path/"failure.json")
    def fail():
        raise OSError("injected checkpoint failure")
    monkeypatch.setattr(a,"save",fail)
    output=StringIO()
    with pytest.raises(SystemExit) as error:
        run_terminal(a,input_stream=StringIO("approach common threshold then approach notice recess\nexit\n"),
                     output_stream=output,specialized_router=execute_environment_request)
    assert error.value.code==3
    assert "You move" not in output.getvalue()
    assert a.current_place_id()==identity("common-threshold")


def test_named_and_directional_movement_have_identical_owner_receipts():
    a=new();b=new()
    named=a.approach_place("common threshold")
    directional=b.move("east")
    assert named.command_fingerprint==directional.command_fingerprint
    assert named.receipt_id==directional.receipt_id
    assert named.pre_state_digest==directional.pre_state_digest
    assert named.post_state_digest==directional.post_state_digest
    assert a.authoritative_digest()==b.authoritative_digest()


@pytest.mark.parametrize("method", ["quietly sliding","throwing","teleporting","sliding without opening it"])
def test_placement_goal_does_not_silently_replace_material_method(method):
    a=new();a.move("south");before=a.authoritative_digest()
    play(a,f"get delivery basket to yard tool station by {method}")
    assert a.authoritative_digest()==before

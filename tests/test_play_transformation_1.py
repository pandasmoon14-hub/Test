"""Owner-qualified #555 transformation, replay and player-facing behavior."""
from dataclasses import replace
import json
import subprocess
import sys

import pytest

from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_transformation import (
    create_transformation_fixture,parse_transformation_request)
from astra_runtime.myravant_transformation_application import TransformationApplication
from astra_runtime.domain.persistent_world_transformation import role
from astra_runtime.domain.persistent_world_material import MaterialError, placement, active_effects, digest
from astra_runtime.domain.persistent_world_component_checkpoint import _canonical_bytes


def new(tmp_path=None, **kwargs):
    fixture=create_transformation_fixture(**kwargs)
    return TransformationApplication.new(fixture=fixture,
        checkpoint_path=tmp_path / "transform.json" if tmp_path else None)


def yard(app):
    assert app.move("south").authoritative_changed
    assert app.move("west").authoritative_changed
    assert app.current_place_id()==identity("yard-tools")


def stage_original(app):
    assert app.pickup("Barrier Crossbar").authoritative_changed
    assert app.material("put_on","Barrier Crossbar","Yard Work Trestle").authoritative_changed


def build_barrier(app, member):
    assert app.pickup("Barrier Board").authoritative_changed
    assert app.material("put_on","Barrier Board","Yard Work Trestle").authoritative_changed
    assert app.pickup("Barrier Cord").authoritative_changed
    assert app.material("tie","Barrier Board",member,"Barrier Cord").authoritative_changed
    effects=active_effects(app.state.representation,app.connections,app.material_profile)
    assert any(e.kind=="movement" and e.source==identity("yard-tools") for e in effects)
    blocked=app.move("north")
    assert blocked.failure_class=="material_passage_obstructed"
    assert app.material("untie","Barrier Cord").authoritative_changed
    assert app.move("north").authoritative_changed


def test_declared_profiles_have_distinct_real_resource_and_actor_variation():
    first=create_transformation_fixture()
    alternate=create_transformation_fixture(actor_order=tuple(reversed(first.actor_order)),
        spare_at="work-bench",tool_at="work-bench")
    assert first.campaign_id!=alternate.campaign_id
    assert first.actor_order!=alternate.actor_order
    assert placement(first.initial_state.representation,identity("barrier-spare")).object_entity_id==identity("yard-tools")
    assert placement(alternate.initial_state.representation,identity("barrier-spare")).object_entity_id==identity("work-bench")
    assert role(new().transform_state,identity("barrier-crossbar"))=="unfit"


@pytest.mark.parametrize("input", [
    "start refitting barrier crossbar using alignment tool",
    "start replacing barrier crossbar with barrier spare",
    "start repurposing barrier crossbar using alignment tool",
    "ask tali ren to refit barrier crossbar using alignment tool",
    "pause transformation","work transformation"])
def test_public_grammar_preserves_targets_and_methods(input):
    assert parse_transformation_request(input) is not None
    modified=parse_transformation_request(input+" somehow")
    if modified is None:
        assert input in {"pause transformation","work transformation"}
    else:
        assert modified[0]=="begin" and modified[1][2].endswith(" somehow")


def test_refit_requires_actual_custody_and_restores_function_with_replay(tmp_path):
    app=new(tmp_path);yard(app);stage_original(app)
    rejected=app.material("tie","Barrier Board","Barrier Crossbar","Barrier Cord")
    assert rejected.failure_class=="component_unfit"
    started=app.begin_transformation("refit","Barrier Crossbar","Alignment Tool")
    assert started.authoritative_changed
    tick=app.runtime_state.logical_time_state.logical_position
    assert app.contribute_transformation().failure_class
    assert app.runtime_state.logical_time_state.logical_position==tick
    assert app.pickup("Alignment Tool").authoritative_changed
    first=app.contribute_transformation()
    assert first.authoritative_changed and app.transform_state.work.stage==1
    assert role(app.transform_state,identity("barrier-crossbar"))=="prepared"
    assert app.control_transformation("pause").authoritative_changed
    blocked=app.contribute_transformation()
    assert blocked.failure_class
    previous=app.authoritative_digest()
    restored=TransformationApplication.restore(fixture=app.fixture,checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest()==previous
    assert restored.transform_state.work.receipts==app.transform_state.work.receipts
    assert restored.control_transformation("resume").authoritative_changed
    final=restored.contribute_transformation()
    assert final.authoritative_changed and restored.transform_state.work.status=="completed"
    assert role(restored.transform_state,identity("barrier-crossbar"))=="fit"
    assert tuple(x[5] for x in restored.transform_state.lineage)==restored.transform_state.work.receipts
    build_barrier(restored,"Barrier Crossbar")
    revived=TransformationApplication.restore(fixture=app.fixture,checkpoint_path=app.checkpoint_path)
    assert revived.authoritative_digest()==restored.authoritative_digest()


def test_replacement_preserves_removed_part_then_repurposes_it(tmp_path):
    app=new(tmp_path);yard(app);stage_original(app)
    assert app.pickup("Barrier Spare").authoritative_changed
    assert app.begin_transformation("replace","Barrier Crossbar","Barrier Spare").authoritative_changed
    one=app.contribute_transformation()
    assert one.authoritative_changed
    assert placement(app.state.representation,identity("barrier-crossbar")).relation_type=="carried_by"
    assert placement(app.state.representation,identity("barrier-spare")).relation_type=="carried_by"
    recovered=TransformationApplication.restore(fixture=app.fixture,checkpoint_path=app.checkpoint_path)
    assert recovered.transform_state.work.stage==1
    assert recovered.contribute_transformation().authoritative_changed
    assert recovered.transform_state.lineage[-1][3]==identity("barrier-spare")
    assert placement(recovered.state.representation,identity("barrier-spare")).relation_type=="supported_by"
    assert placement(recovered.state.representation,identity("barrier-crossbar")).relation_type=="carried_by"
    assert role(recovered.transform_state,identity("barrier-crossbar"))=="unfit"
    assert recovered.pickup("Alignment Tool").authoritative_changed
    assert recovered.move("west").authoritative_changed
    assert recovered.move("west").authoritative_changed
    assert recovered.current_place_id()==identity("work-bench")
    assert recovered.begin_transformation("repurpose","Barrier Crossbar","Alignment Tool").authoritative_changed
    assert recovered.contribute_transformation().authoritative_changed
    assert role(recovered.transform_state,identity("barrier-crossbar"))=="spacer"
    assert recovered.pickup("Repair Board").authoritative_changed
    assert recovered.material("put_on","Repair Board","Workroom Bench").authoritative_changed
    assert recovered.material("put_on","Barrier Crossbar","Workroom Bench").authoritative_changed
    assert recovered.pickup("Repair Cord").authoritative_changed
    assert recovered.material("tie","Repair Board","Barrier Crossbar","Repair Cord").authoritative_changed
    assert TransformationApplication.restore(fixture=app.fixture,
        checkpoint_path=app.checkpoint_path).authoritative_digest()==recovered.authoritative_digest()


def test_willing_actor_uses_own_tool_and_committed_world_intervals(tmp_path):
    app=new(tmp_path);yard(app);stage_original(app)
    agreed=app.begin_transformation("refit","Barrier Crossbar","Alignment Tool","Tali Ren")
    assert agreed.authoritative_changed,agreed.message
    before=app.runtime_state.logical_time_state.logical_position
    assert app.wait().authoritative_changed
    assert app.transform_state.work.stage==0
    assert placement(app.state.representation,identity("alignment-tool")).object_entity_id==identity("tali")
    assert app.wait().authoritative_changed
    assert app.transform_state.work.stage==1
    assert app.wait().authoritative_changed
    assert app.transform_state.work.status=="completed"
    assert role(app.transform_state,identity("barrier-crossbar"))=="fit"
    assert app.runtime_state.logical_time_state.logical_position==before+3
    restored=TransformationApplication.restore(fixture=app.fixture,checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest()==app.authoritative_digest()
    assert all(x[1]==identity("tali") for x in restored.transform_state.lineage)


def test_cross_profile_replay_tamper_and_wrong_tool_refuse(tmp_path):
    from astra_runtime.myravant_actor_application import ActorApplication
    app=new(tmp_path);yard(app)
    before=app.authoritative_digest()
    assert app.begin_transformation("refit","Barrier Crossbar","Cleaning Brush").failure_class
    assert app.authoritative_digest()==before
    with pytest.raises(MaterialError):
        ActorApplication.restore(fixture=app.fixture,checkpoint_path=app.checkpoint_path)
    app.save()
    assert len(app.transform_state.lineage)==0
    raw=json.loads(app.checkpoint_path.read_text())
    raw["payload"]["profile"]["transformation"]["version"]="forged-fit"
    raw["integrity_digest"]=digest(raw["payload"])
    app.checkpoint_path.write_bytes(_canonical_bytes(raw))
    with pytest.raises(MaterialError):
        TransformationApplication.restore(fixture=app.fixture,checkpoint_path=app.checkpoint_path)


def test_installed_terminal_selects_separate_locality(tmp_path):
    path=tmp_path/"public.json"
    argv=[sys.executable,"-m","astra_runtime.myravant_terminal",
          "--locality","tarrow-transformation","--checkpoint",str(path)]
    proc=subprocess.run(argv,input="go south\ngo west\ninspect barrier crossbar\n"
        "start refitting barrier crossbar using alignment tool\ninspect transformation\nsave\nexit\n",
        text=True,capture_output=True,timeout=90)
    assert proc.returncode==0,(proc.stdout,proc.stderr)
    assert "Declared component fit: unfit" in proc.stdout
    assert "Transformation accepted" in proc.stdout
    assert "Transformation: refit" in proc.stdout
    assert path.exists()
    assert TransformationApplication.restore(checkpoint_path=path).transform_state.work is not None

def test_stale_refit_opportunity_refuses_without_free_interval(tmp_path):
    app=new(tmp_path);yard(app);stage_original(app)
    assert app.pickup("Alignment Tool").authoritative_changed
    assert app.begin_transformation("refit","Barrier Crossbar","Alignment Tool").authoritative_changed
    assert app.contribute_transformation().authoritative_changed
    first=app.transform_state.work.receipts
    assert app.material("lift_from","Barrier Crossbar","Yard Work Trestle").authoritative_changed
    before=(app.runtime_state.logical_time_state.logical_position,app.authoritative_digest())
    rejected=app.contribute_transformation()
    assert rejected.failure_class=="transformation_opportunity_unavailable"
    assert (app.runtime_state.logical_time_state.logical_position,app.authoritative_digest())==before
    assert app.transform_state.work.receipts==first
    assert app.material("put_on","Barrier Crossbar","Yard Work Trestle").authoritative_changed
    assert app.contribute_transformation().authoritative_changed
    assert role(app.transform_state,identity("barrier-crossbar"))=="fit"


def test_resealed_final_digest_tamper_rejected_even_if_checksum_valid(tmp_path):
    app=new(tmp_path);yard(app);stage_original(app)
    assert app.save().checkpoint_digest
    raw=json.loads(app.checkpoint_path.read_text())
    raw["payload"]["final"]="0"*64
    raw["integrity_digest"]=digest(raw["payload"])
    app.checkpoint_path.write_bytes(_canonical_bytes(raw))
    with pytest.raises(MaterialError):
        TransformationApplication.restore(fixture=app.fixture,checkpoint_path=app.checkpoint_path)

def test_abandoned_partial_work_requires_new_scope_but_keeps_receipts(tmp_path):
    app=new(tmp_path);yard(app);stage_original(app)
    assert app.pickup("Alignment Tool").authoritative_changed
    assert app.begin_transformation("refit","Barrier Crossbar","Alignment Tool").authoritative_changed
    assert app.contribute_transformation().authoritative_changed
    first=app.transform_state.work.receipts
    assert app.control_transformation("abandon").authoritative_changed
    assert app.transform_state.work.status=="abandoned"
    assert app.contribute_transformation().failure_class
    assert app.begin_transformation("replace","Barrier Crossbar","Barrier Spare").failure_class
    reaccepted=app.begin_transformation("refit","Barrier Crossbar","Alignment Tool")
    assert reaccepted.authoritative_changed and "Renewed" in reaccepted.message
    assert app.transform_state.work.receipts==first
    assert app.contribute_transformation().authoritative_changed
    assert role(app.transform_state,identity("barrier-crossbar"))=="fit"
    assert TransformationApplication.restore(fixture=app.fixture,
        checkpoint_path=app.checkpoint_path).authoritative_digest()==app.authoritative_digest()

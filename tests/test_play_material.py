"""Owner-approved #542: full material lifecycle and adversarial composition."""
import copy
from dataclasses import asdict, replace
import io
import json
import subprocess
from pathlib import Path

import pytest

from astra_runtime.myravant_material_application import MaterialApplication, FORMAT, parse_material
from astra_runtime.myravant_tarrow_material import create_material_fixture, identity
from astra_runtime.myravant_tarrow_environment import create_environment_fixture
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_terminal import run_terminal
from astra_runtime.myravant_tarrow_material import execute_material_locality_request
from astra_runtime.domain.persistent_world_material import (
    MaterialError, MaterialProfile, MaterialEffect, execute_material, validate_joint,
    placement, active_effects, digest,
)


def app(tmp_path=None):
    return MaterialApplication.new(fixture=create_material_fixture(),checkpoint_path=tmp_path/'material.json' if tmp_path else None)


def go(a,*directions):
    for d in directions:
        r=a.move(d); assert r.authoritative_changed,r.message


def put(a,obj,surface):
    assert a.pickup(obj).authoritative_changed
    r=a.material('put_on',obj,surface); assert r.authoritative_changed,r.message


def workshop(a):
    go(a,'south','west','west','west')
    put(a,'repair board','workroom bench');put(a,'repair peg','workroom bench')
    assert a.pickup('repair cord').authoritative_changed
    r=a.material('tie','repair board','repair peg','repair cord'); assert r.authoritative_changed,r.message


def barrier(a):
    go(a,'south','west')
    put(a,'barrier board','yard work trestle');put(a,'barrier crossbar','yard work trestle')
    assert a.pickup('barrier cord').authoritative_changed
    assert a.material('tie','barrier board','barrier crossbar','barrier cord').authoritative_changed


def screen(a):
    go(a,'east','east')
    put(a,'screen cloth','document box')
    assert a.pickup('screen cord').authoritative_changed
    assert a.material('tie','screen cloth','notice board','screen cord').authoritative_changed


@pytest.mark.parametrize('setup',[workshop,barrier,screen])
def test_arrangements_restore_and_recover(tmp_path,setup):
    a=app(tmp_path);setup(a)
    before=a.authoritative_digest()
    restored=MaterialApplication.restore(checkpoint_path=a.checkpoint_path,fixture=a.fixture)
    assert restored.authoritative_digest()==before
    c=restored.connections[0]
    fastener=restored.fixture.entity_name(c.fastener)
    assert restored.material('untie',fastener).authoritative_changed
    assert not restored.connections
    assert placement(restored.state.representation,c.fastener).relation_type=='carried_by'
    first=restored.authoritative_digest()
    assert not restored.material('untie',fastener).authoritative_changed
    assert restored.authoritative_digest()==first
    for obj in (c.left,c.right):
        p=placement(restored.state.representation,obj)
        if p.relation_type=='supported_by':
            assert restored.material('lift_from',restored.fixture.entity_name(obj),restored.fixture.entity_name(p.object_entity_id)).authoritative_changed
    assert MaterialApplication.restore(checkpoint_path=a.checkpoint_path,fixture=a.fixture).authoritative_digest()==restored.authoritative_digest()


@pytest.mark.parametrize('operation,args',[
    ('pickup',('repair board',)),('drop',('repair cord',)),
    ('store_object',('repair board','parts tray')),('retrieve_object',('repair board','parts tray')),
    ('displace_object',('repair board','east')),('give_object',('repair board','oren kesh')),
    ('throw_object',('repair board','east')),
])
def test_old_mutation_routes_cannot_bypass_relationships(operation,args):
    a=app();workshop(a);before=a.authoritative_digest()
    kwargs={'method':'push'} if operation=='displace_object' else {}
    r=getattr(a,operation)(*args,**kwargs)
    assert not r.authoritative_changed
    assert a.authoritative_digest()==before
    assert r.failure_class=='material_relationship_conflict'


def test_occupied_support_cannot_move():
    a=app();screen(a)
    before=a.authoritative_digest()
    r=a.pickup('document box')
    assert not r.authoritative_changed and before==a.authoritative_digest()
    assert r.failure_class=='material_relationship_conflict'


def test_barrier_requires_placement_and_connection_and_reopens():
    a=app();go(a,'south','west')
    assert a.move('north').authoritative_changed;assert a.move('south').authoritative_changed
    put(a,'barrier board','yard work trestle');put(a,'barrier crossbar','yard work trestle')
    assert not active_effects(a.state.representation,a.connections,a.material_profile)
    assert a.pickup('barrier cord').authoritative_changed
    assert a.material('tie','barrier board','barrier crossbar','barrier cord').authoritative_changed
    before=a.authoritative_digest()
    assert a.move('north').failure_class=='material_passage_obstructed'
    assert a.authoritative_digest()==before
    assert a.material('untie','barrier cord').authoritative_changed
    assert a.move('north').authoritative_changed


def test_screen_connections_independent_and_sight_is_not_movement(tmp_path):
    a=app(tmp_path);screen(a)
    assert a.pickup('screen tie').authoritative_changed
    assert a.material('fasten','screen cloth','notice board','screen tie').authoritative_changed
    assert len(a.connections)==2
    assert a.material('unfasten','screen tie').authoritative_changed
    assert len(a.connections)==1
    go(a,'west')
    assert a.look_direction('east').failure_class=='material_sightline_obstructed'
    assert a.focused_observation('notice board',direction='east').failure_class=='material_sightline_obstructed'
    assert a.move('east').authoritative_changed # same screened corridor remains traversable
    assert a.material('untie','screen cord').authoritative_changed
    go(a,'west')
    assert a.look_direction('east').failure_class!='material_sightline_obstructed'


def test_exterior_not_inside_closed_container_and_transport(tmp_path):
    a=app(tmp_path);go(a,'east','east')
    put(a,'screen cloth','document box')
    assert a.object_open_state(identity('document-box')).state=='closed'
    assert a.material('lift_from','screen cloth','document box').authoritative_changed
    assert not a.store_object('screen cloth','document box').authoritative_changed
    assert a.open_object('document box').authoritative_changed
    assert a.store_object('screen cloth','document box').authoritative_changed
    assert placement(a.state.representation,identity('screen-cloth')).relation_type=='contained_by'
    assert 'Inside:' in a.inspect('document box').message or a.inspect('document box').view is not None
    assert a.close_object('document box').authoritative_changed
    assert a.pickup('document box').authoritative_changed
    go(a,'west','west','west','north')
    assert a.open_object('document box').authoritative_changed
    assert a.retrieve_object('screen cloth','document box').authoritative_changed
    assert MaterialApplication.restore(checkpoint_path=a.checkpoint_path,fixture=a.fixture).authoritative_digest()==a.authoritative_digest()


@pytest.mark.parametrize('operation,refs',[
    ('put_on',('repair board','workroom bench')),
    ('tie',('repair board','repair peg','repair cord')),
    ('untie',('repair cord',)),
])
def test_remote_targets_do_not_mutate_or_reveal(operation,refs):
    a=app();d=a.authoritative_digest();r=a.material(operation,*refs)
    assert not r.authoritative_changed and d==a.authoritative_digest()
    assert 'workroom' not in r.message.casefold()


def test_method_and_fastener_are_not_interchangeable():
    a=app();go(a,'east','east');put(a,'screen cloth','document box');assert a.pickup('screen cord').authoritative_changed
    d=a.authoritative_digest()
    assert not a.material('fasten','screen cloth','notice board','screen cord').authoritative_changed
    assert d==a.authoritative_digest()
    assert a.material('tie','screen cloth','notice board','screen cord').authoritative_changed
    d=a.authoritative_digest()
    assert not a.material('tie','screen cloth','notice board','screen cord').authoritative_changed
    assert not a.material('unfasten','screen cord').authoritative_changed
    assert d==a.authoritative_digest()


def test_supported_description_and_connections_visible():
    a=app();workshop(a)
    assert 'Resting on: Workroom Bench' in a.inspect('repair board').message
    assert 'Connection:' in a.inspect('repair cord').message
    assert 'On the exterior surface: Repair Board, Repair Peg' in a.inspect('workroom bench').message


@pytest.mark.parametrize('change', ['final','receipt','order','root','profile','invented','state_digest'])
def test_resealed_checkpoint_forgery_rejected(tmp_path,change):
    a=app(tmp_path);workshop(a);p=json.loads(a.checkpoint_path.read_text());data=p['payload']
    if change=='final':data['final']='0'*64
    elif change=='receipt':data['journal'][-1]['result']['receipt_id']='fake'
    elif change=='order':data['journal'][0],data['journal'][1]=data['journal'][1],data['journal'][0]
    elif change=='root':data['root']='0'*64
    elif change=='profile':data['profile']['support_pairs']=[]
    elif change=='invented':data['journal'].append(copy.deepcopy(data['journal'][-1]))
    else:data['journal'][-1]['result']['post_state_digest']='0'*64
    p['integrity_digest']=digest(data);a.checkpoint_path.write_text(json.dumps(p))
    with pytest.raises(MaterialError):MaterialApplication.restore(checkpoint_path=a.checkpoint_path,fixture=a.fixture)


def test_failed_write_rolls_back_all_components(tmp_path,monkeypatch):
    a=app(tmp_path);go(a,'south','west','west','west');assert a.pickup('repair board').authoritative_changed
    d=a.authoritative_digest();old=a.checkpoint_path.read_bytes();j=a.journal
    def fail(**kwargs):raise OSError('test save failure')
    monkeypatch.setattr('astra_runtime.myravant_material_application._write_envelope',fail)
    r=a.material('put_on','repair board','workroom bench')
    assert r.failure_class=='material_checkpoint_write_failed'
    assert a.authoritative_digest()==d and a.journal==j and a.checkpoint_path.read_bytes()==old


@pytest.mark.parametrize('bad', ['self','cycle','double','orphan'])
def test_joint_integrity_rejects_forged_placements(bad):
    a=app();workshop(a);rep=a.state.representation
    r=placement(rep,identity('repair-board'))
    if bad=='self':
        with pytest.raises(ValueError):replace(r,object_entity_id=r.subject_entity_id)
        return
    elif bad=='cycle':rels=tuple(replace(x,object_entity_id=identity('repair-peg')) if x==r else replace(x,object_entity_id=identity('repair-board')) if x.subject_entity_id==identity('repair-peg') else x for x in rep.relations)
    elif bad=='double':rels=(*rep.relations,replace(r,relation_id='astra:relation:extra'))
    else:rels=tuple(x for x in rep.relations if x!=r)
    with pytest.raises(ValueError):validate_joint(replace(rep,relations=rels),a.connections,a.material_profile)


def test_stale_domain_qualification_rejected():
    a=app();go(a,'south','west','west','west');assert a.pickup('repair board').authoritative_changed
    d=a.authoritative_digest()
    with pytest.raises(MaterialError,match='stale'):
        execute_material(rep=a.state.representation,connections=(),profile=a.material_profile,operation='put_on',
            participants=(identity('repair-board'),identity('bench')),visible_ids=(identity('repair-board'),identity('bench')),
            command_id='stale-test',expected_pre_digest='0'*64,pre_digest=d)
    assert d==a.authoritative_digest()


def test_neutral_configuration_only_variation():
    a=app();p=a.material_profile
    # Different existing materials and surface, without any shared executor edit.
    extra=(identity('folio'),identity('shelf-cloth'),identity('screen-tie'),'fasten')
    p=replace(p,fastening_pairs=(*p.fastening_pairs,extra))
    f=replace(a.fixture,material_profile=p)
    a=MaterialApplication.new(fixture=f)
    go(a,'east','north')
    assert a.material('put_on','weatherproof field folio','common shelf fitting').failure_class
    # Admit this particular surface through declaration, then recreate the root.
    p=replace(p,support_pairs=(*p.support_pairs,(identity('folio'),identity('shelf-fitting')),(identity('shelf-cloth'),identity('shelf-fitting'))))
    a=MaterialApplication.new(fixture=replace(f,material_profile=p));go(a,'east','north')
    assert a.material('put_on','weatherproof field folio','common shelf fitting').authoritative_changed
    assert a.pickup('shelf cloth').authoritative_changed
    assert a.material('put_on','shelf cloth','common shelf fitting').authoritative_changed
    # Fastener can be transported from the notice recess to the new context.
    go(a,'south','east');assert a.pickup('screen tie').authoritative_changed;go(a,'west','north')
    assert a.material('fasten','weatherproof field folio','shelf cloth','screen tie').authoritative_changed


def test_legacy_locality_remains_unchanged():
    f=create_environment_fixture();a=MyravantPlayApplication.new(fixture=f)
    assert f.provenance.fixture_version=='environment-1'
    assert not hasattr(f,'material_profile')
    assert parse_material('cut repair cord') is None


def test_terminal_sequence_partial_and_restart(tmp_path):
    a=app(tmp_path);go(a,'south','west','west','west')
    output=io.StringIO()
    run_terminal(a,input_stream=io.StringIO('take repair board then put repair board on workroom bench\ntie repair board to repair peg using repair cord\nexit\n'),
                 output_stream=output,specialized_router=execute_material_locality_request)
    assert 'You put Repair Board on Workroom Bench' in output.getvalue()
    assert len(a.connections)==0
    assert placement(a.state.representation,identity('repair-board')).relation_type=='supported_by'
    restored=MaterialApplication.restore(checkpoint_path=a.checkpoint_path,fixture=a.fixture)
    assert restored.authoritative_digest()==a.authoritative_digest()


def test_installed_cli(tmp_path):
    save=tmp_path/'cli.json'
    commands='go south\ngo west\ngo west\ngo west\ntake repair board then put repair board on workroom bench\nexit\n'
    r=subprocess.run(['myravant-play','--locality','tarrow-material','--checkpoint',str(save)],input=commands,text=True,capture_output=True)
    assert r.returncode==0,r.stderr
    assert 'You put Repair Board on Workroom Bench' in r.stdout
    r=subprocess.run(['myravant-play','--locality','tarrow-material','--load',str(save)],input='inspect repair board\nexit\n',text=True,capture_output=True)
    assert r.returncode==0 and 'Resting on: Workroom Bench' in r.stdout,r.stderr
    r=subprocess.run(['myravant-play','--locality','tarrow-depth','--load',str(save)],input='exit\n',text=True,capture_output=True)
    assert r.returncode==2


def test_supported_lamp_uses_actual_location_and_existing_light_owner(tmp_path):
    a=app(tmp_path);assert a.pickup('shuttered service lamp').authoritative_changed
    go(a,'south','west','west','west')
    assert a.material('put_on','shuttered service lamp','workroom bench').authoritative_changed
    assert a.light_object('shuttered service lamp').authoritative_changed
    assert a._bounded_local_light_available()
    assert a.extinguish_object('shuttered service lamp').authoritative_changed
    assert not a._bounded_local_light_available()
    assert MaterialApplication.restore(checkpoint_path=a.checkpoint_path,fixture=a.fixture).authoritative_digest()==a.authoritative_digest()


def test_look_and_focused_inspection_include_supported_objects():
    a=app();workshop(a)
    out=io.StringIO();run_terminal(a,input_stream=io.StringIO('look\ninspect repair board\nexit\n'),output_stream=out,specialized_router=execute_material_locality_request)
    assert 'Supported objects: Repair Board on Workroom Bench' in out.getvalue()
    assert 'Repair Cord' in a.look().view.objects
    assert a.focused_observation('repair board').failure_class is None


def test_hidden_contents_not_exposed_by_exterior_inspection():
    a=app();go(a,'south','west','north')
    before=a.authoritative_digest()
    r=a.material('put_on','soft-iron pin blank','sorting rack')
    assert not r.authoritative_changed and 'pin' not in r.message.casefold()
    assert a.authoritative_digest()==before


@pytest.mark.parametrize('text',[
    'put repair board on workroom bench then wait then wait',
    'tie repair board to repair peg using repair cord and cut it',
    'put repair board on workroom bench while tying repair cord',
    'fasten repair board to repair peg using repair cord permanently',
])
def test_compound_or_modifier_not_silently_discarded(text):
    a=app();go(a,'south','west','west','west');assert a.pickup('repair board').authoritative_changed
    d=a.authoritative_digest();output=io.StringIO()
    run_terminal(a,input_stream=io.StringIO(text+'\nexit\n'),output_stream=output,specialized_router=execute_material_locality_request)
    assert a.authoritative_digest()==d


def test_partial_sequence_keeps_only_the_first_lawful_step(tmp_path):
    a=app(tmp_path);go(a,'south','west','west','west');a.pickup('repair board')
    out=io.StringIO();run_terminal(a,input_stream=io.StringIO('put repair board on workroom bench then tie repair board to repair peg using repair cord\nexit\n'),output_stream=out,specialized_router=execute_material_locality_request)
    assert 'Sequence halted' in out.getvalue()
    assert placement(a.state.representation,identity('repair-board')).relation_type=='supported_by'
    assert not a.connections
    assert MaterialApplication.restore(checkpoint_path=a.checkpoint_path,fixture=a.fixture).authoritative_digest()==a.authoritative_digest()


def test_failed_durability_halts_future_mutations(tmp_path,monkeypatch):
    a=app(tmp_path)
    def fail(**kwargs):raise OSError('failure')
    monkeypatch.setattr('astra_runtime.myravant_material_application._write_envelope',fail)
    assert a.move('south').failure_class=='material_checkpoint_write_failed'
    assert a.move('north').failure_class=='material_session_halted'
    assert not a.journal


@pytest.mark.parametrize('bad', ['missing_surface','self_pair','missing_fastener','effect','actor'])
def test_profile_declarations_fail_closed(bad):
    a=app();p=a.material_profile
    if bad=='missing_surface':p=replace(p,support_pairs=(*p.support_pairs,(identity('repair-board'),'astra:entity:absent')))
    elif bad=='self_pair':p=replace(p,support_pairs=(*p.support_pairs,(identity('repair-board'),identity('repair-board'))))
    elif bad=='missing_fastener':p=replace(p,fastening_pairs=((identity('repair-board'),identity('repair-peg'),'astra:entity:absent','tie'),))
    elif bad=='actor':p=replace(p,actor_id=identity('oren'))
    else:p=replace(p,effects=(replace(p.effects[0],supports=()),))
    with pytest.raises(ValueError):MaterialApplication.new(fixture=replace(a.fixture,material_profile=p))


def test_supported_local_object_is_not_remotely_available():
    a=app();workshop(a);go(a,'east')
    d=a.authoritative_digest();r=a.material('untie','repair cord')
    assert not r.authoritative_changed and a.authoritative_digest()==d


def test_unqualified_operation_has_no_material_side_effect():
    a=app();workshop(a);d=a.authoritative_digest()
    assert not a.material('cut','repair cord').authoritative_changed
    assert d==a.authoritative_digest()


def test_barrier_qualifies_object_displacement_as_well_as_actor_movement():
    a=app();barrier(a)
    before=a.authoritative_digest()
    assert a.displace_object('long pry bar','north',method='push').failure_class=='material_passage_obstructed'
    assert before==a.authoritative_digest()


def test_direct_owner_change_durable_before_application_acknowledgement(tmp_path):
    a=app(tmp_path)
    assert a.move('south').authoritative_changed
    assert a.checkpoint_path.exists()
    restored=MaterialApplication.restore(checkpoint_path=a.checkpoint_path,fixture=a.fixture)
    assert restored.authoritative_digest()==a.authoritative_digest()


def test_invalid_material_argument_count_is_not_silently_ignored():
    a=app();workshop(a);before=a.authoritative_digest()
    assert not a.material('untie','repair cord','repair board').authoritative_changed
    assert before==a.authoritative_digest()


def test_material_preflight_is_pure_and_receipts_match_sequence(tmp_path,monkeypatch):
    from astra_runtime.myravant_terminal import _explicit_two_step_intent
    a=app();go(a,'south','west','west','west');a.pickup('repair board')
    before=a.authoritative_digest()
    def forbidden(*args,**kwargs):pytest.fail('preflight executed a mutation')
    with monkeypatch.context() as m:
        m.setattr(a,'material',forbidden)
        plan=_explicit_two_step_intent('inspect self then put repair board on workroom bench',fixture=a.fixture)
    assert plan is not None and plan[1].action=='material' and before==a.authoritative_digest()
    b=app();go(b,'south','west','west','west');b.pickup('repair board')
    direct=a.material('put_on','repair board','workroom bench')
    out=io.StringIO();run_terminal(b,input_stream=io.StringIO('inspect self then put repair board on workroom bench\nexit\n'),output_stream=out,specialized_router=execute_material_locality_request)
    assert a.authoritative_digest()==b.authoritative_digest()
    assert a.journal[-1]['result']['receipt_id']==b.journal[-1]['result']['receipt_id']==direct.receipt_id

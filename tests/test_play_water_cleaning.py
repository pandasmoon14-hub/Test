"""Approved #544: material conservation and installed water/cleaning journeys."""
from dataclasses import replace
from fractions import Fraction
import io
import json
import subprocess

import pytest

from astra_runtime.myravant_water_application import WaterApplication, parse_water
from astra_runtime.myravant_tarrow_water import create_water_fixture, execute_water_locality_request
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_terminal import run_terminal
from astra_runtime.domain.persistent_world_water_cleaning import total_water, total_residue, execute


def app(tmp_path=None):
    return WaterApplication.new(fixture=create_water_fixture(), checkpoint_path=tmp_path/'water.json' if tmp_path else None)


def go(a,*directions):
    for direction in directions:
        result=a.move(direction)
        assert result.authoritative_changed,result.message


def workshop(a):
    go(a,'south','west','west','west')


def take(a,name):
    result=a.pickup(name)
    assert result.authoritative_changed,result.message


def act(a,operation,*refs,amount=None):
    before=(total_water(a.water_state),total_residue(a.water_state))
    result=a.water(operation,*refs,amount=amount)
    assert result.authoritative_changed,result.message
    assert before==(total_water(a.water_state),total_residue(a.water_state))
    return result


def value(a,compartment,name):
    return dict(getattr(a.water_state,compartment))[identity(name)]


def test_complete_workshop_washing_and_recovery(tmp_path):
    a=app(tmp_path);workshop(a)
    take(a,'cleaning cloth')
    act(a,'soak','wash bucket','cleaning cloth')
    act(a,'wipe','practice panel','cleaning cloth')
    act(a,'wipe','practice panel','cleaning cloth')
    assert value(a,'adhered','practice-panel')==1
    assert value(a,'adhered','cleaning-cloth')==2
    before=a.authoritative_digest()
    assert not a.water('wipe','practice panel','cleaning cloth').authoritative_changed
    assert before==a.authoritative_digest()
    act(a,'fill','wash bucket','rinse basin')
    act(a,'rinse','cleaning cloth','rinse basin')
    assert value(a,'adhered','cleaning-cloth')==0
    assert value(a,'suspended','cleaning-cloth')==Fraction(2,7)
    assert value(a,'suspended','rinse-basin')==Fraction(12,7)
    act(a,'wipe','practice panel','cleaning cloth')
    act(a,'wring','cleaning cloth','pouring jug')
    assert value(a,'water','cleaning-cloth')==0
    assert value(a,'adhered','cleaning-cloth')==1
    assert value(a,'suspended','pouring-jug')==Fraction(2,7)
    assert WaterApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path).authoritative_digest()==a.authoritative_digest()


def test_yard_scrubbing_collection_and_zero_effect_refusal():
    a=app();go(a,'south','west');take(a,'cleaning brush')
    act(a,'scrub','sorting board','cleaning brush')
    act(a,'scrub','sorting board','cleaning brush')
    assert value(a,'adhered','cleaning-brush')==4
    act(a,'collect','cleaning brush','debris tray')
    assert value(a,'adhered','debris-tray')==4
    before=a.authoritative_digest()
    assert not a.water('collect','cleaning brush','debris tray').authoritative_changed
    assert before==a.authoritative_digest()


def test_dirty_liquid_proportional_transfer_and_mixing():
    a=app();workshop(a);take(a,'cleaning cloth');take(a,'rinse basin')
    act(a,'soak','wash bucket','cleaning cloth')
    act(a,'wipe','practice panel','cleaning cloth')
    act(a,'fill','wash bucket','rinse basin')
    act(a,'rinse','cleaning cloth','rinse basin')
    act(a,'pour','rinse basin','pouring jug',amount=3)
    assert value(a,'suspended','pouring-jug')==Fraction(3,7)
    assert value(a,'suspended','rinse-basin')==Fraction(3,7)
    act(a,'empty','rinse basin','wash bucket')
    assert value(a,'suspended','wash-bucket')==Fraction(3,7)
    assert total_residue(a.water_state)==7


@pytest.mark.parametrize('amount',[0,-1,True,1.5,'1',13])
def test_invalid_or_overdrawn_quantity_refuses_without_mutation(amount):
    a=app();workshop(a);take(a,'wash bucket');before=a.authoritative_digest()
    assert not a.water('pour','wash bucket','pouring jug',amount=amount).authoritative_changed
    assert a.authoritative_digest()==before


def test_full_recipient_empty_source_and_dry_wipe_refuse():
    a=app();workshop(a);take(a,'cleaning cloth');take(a,'pouring jug')
    before=a.authoritative_digest()
    assert not a.water('wipe','practice panel','cleaning cloth').authoritative_changed
    assert not a.water('empty','pouring jug','rinse basin').authoritative_changed
    assert a.authoritative_digest()==before
    act(a,'fill','wash bucket','pouring jug')
    before=a.authoritative_digest()
    assert not a.water('fill','wash bucket','pouring jug').authoritative_changed
    assert not a.water('pour','pouring jug','rinse basin',amount=4).authoritative_changed
    assert before==a.authoritative_digest()


@pytest.mark.parametrize('operation,refs',[('soak',('wash bucket','cleaning cloth')),('scrub',('sorting board','cleaning brush')),('pour',('wash bucket','pouring jug'))])
def test_remote_targets_do_not_reveal_material_quantities(operation,refs):
    a=app();before=a.authoritative_digest()
    r=a.water(operation,*refs,amount=1 if operation=='pour' else None)
    assert not r.authoritative_changed and a.authoritative_digest()==before
    assert all(word not in r.message.casefold() for word in ('12','practice panel','sorting board'))


def test_tools_require_custody_and_closed_storage_blocks_access():
    a=app();workshop(a);before=a.authoritative_digest()
    assert not a.water('soak','wash bucket','cleaning cloth').authoritative_changed
    assert before==a.authoritative_digest()
    take(a,'cleaning cloth');act(a,'soak','wash bucket','cleaning cloth')
    assert a.open_object('parts tray').authoritative_changed
    assert a.store_object('cleaning cloth','parts tray').authoritative_changed
    assert a.close_object('parts tray').authoritative_changed
    before=a.authoritative_digest()
    assert not a.water('wipe','practice panel','cleaning cloth').authoritative_changed
    assert before==a.authoritative_digest()


def test_configuration_only_transfer_rate_variation():
    a=app();profile=a.water_profile
    changed=replace(profile,assets=tuple(replace(x,transfer_rate=Fraction(2)) if x.id==identity('cleaning-cloth') else x for x in profile.assets))
    b=WaterApplication.new(fixture=replace(a.fixture,water_profile=changed));workshop(b);take(b,'cleaning cloth')
    act(b,'soak','wash bucket','cleaning cloth');act(b,'wipe','practice panel','cleaning cloth')
    assert value(b,'adhered','practice-panel')==1


def test_direct_and_two_step_share_transition_receipt():
    a=app();b=app()
    for x in (a,b):workshop(x);take(x,'cleaning cloth')
    direct=act(a,'soak','wash bucket','cleaning cloth')
    output=io.StringIO()
    run_terminal(b,input_stream=io.StringIO('inspect self then soak cleaning cloth from wash bucket\nexit\n'),output_stream=output,specialized_router=execute_water_locality_request)
    assert a.authoritative_digest()==b.authoritative_digest(),output.getvalue()
    assert direct.receipt_id==b.journal[-1]['result']['receipt_id']


@pytest.mark.parametrize('text',['pour 1 units from wash bucket into pouring jug then wait then wait','soak cleaning cloth from wash bucket while cleaning','wipe practice panel using cleaning cloth permanently'])
def test_unsupported_compounds_do_not_truncate(text):
    a=app();workshop(a);take(a,'wash bucket');take(a,'cleaning cloth');before=a.authoritative_digest()
    run_terminal(a,input_stream=io.StringIO(text+'\nexit\n'),output_stream=io.StringIO(),specialized_router=execute_water_locality_request)
    assert a.authoritative_digest()==before


def test_quantity_only_supported_for_pour():
    a=app();workshop(a);take(a,'cleaning cloth');before=a.authoritative_digest()
    assert not a.water('soak','wash bucket','cleaning cloth',amount=1).authoritative_changed
    assert a.authoritative_digest()==before


def test_inspection_tracks_state_without_mutating():
    a=app();workshop(a);take(a,'cleaning cloth');act(a,'soak','wash bucket','cleaning cloth')
    before=a.authoritative_digest();message=a.inspect('cleaning cloth').message
    assert 'water' in message.casefold() and '1' in message
    assert before==a.authoritative_digest()


@pytest.mark.parametrize('change',['final','receipt','order','root','profile','invented','state_digest'])
def test_resealed_checkpoint_forgery_rejected(tmp_path,change):
    import copy
    from astra_runtime.domain.persistent_world_material import digest
    a=app(tmp_path);workshop(a);take(a,'cleaning cloth');act(a,'soak','wash bucket','cleaning cloth')
    envelope=json.loads(a.checkpoint_path.read_text());data=envelope['payload']
    if change=='final':data['final']='0'*64
    elif change=='receipt':data['journal'][-1]['result']['receipt_id']='fake'
    elif change=='order':data['journal'][0],data['journal'][1]=data['journal'][1],data['journal'][0]
    elif change=='root':data['root']='0'*64
    elif change=='profile':data['profile']['water']['allowed_pairs']=[]
    elif change=='invented':data['journal'].append(copy.deepcopy(data['journal'][-1]))
    else:data['journal'][-1]['result']['post_state_digest']='0'*64
    envelope['integrity_digest']=digest(data);a.checkpoint_path.write_text(json.dumps(envelope))
    with pytest.raises(ValueError):WaterApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path)


def test_checkpoint_failure_rolls_back_water_and_halts(tmp_path,monkeypatch):
    a=app(tmp_path);workshop(a);take(a,'cleaning cloth')
    before=a.authoritative_digest();state=a.water_state;journal=a.journal;saved=a.checkpoint_path.read_bytes()
    def fail(**kwargs):raise OSError('simulated write failure')
    monkeypatch.setattr('astra_runtime.myravant_material_application._write_envelope',fail)
    result=a.water('soak','wash bucket','cleaning cloth')
    assert result.failure_class and not result.authoritative_changed
    assert a.water_state==state and a.journal==journal and a.authoritative_digest()==before
    assert a.checkpoint_path.read_bytes()==saved
    assert not a.move('east').authoritative_changed


def test_material_state_follows_vessel_through_transport(tmp_path):
    a=app(tmp_path);workshop(a);take(a,'pouring jug');act(a,'fill','wash bucket','pouring jug')
    go(a,'east','east');assert value(a,'water','pouring-jug')==3
    assert a.drop('pouring jug').authoritative_changed
    go(a,'east');before=a.authoritative_digest()
    assert not a.water('empty','pouring jug','rinse basin').authoritative_changed
    assert before==a.authoritative_digest()
    restored=WaterApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path)
    assert value(restored,'water','pouring-jug')==3


def test_unqualified_disposal_and_self_transfer_refuse():
    a=app();workshop(a);take(a,'wash bucket');before=a.authoritative_digest()
    assert not a.water('empty','wash bucket','practice panel').authoritative_changed
    assert not a.water('pour','wash bucket','wash bucket',amount=1).authoritative_changed
    assert not a.water('evaporate','wash bucket','rinse basin').authoritative_changed
    assert a.authoritative_digest()==before


def test_cleaning_then_collection_requires_available_residue():
    a=app();go(a,'south','west');take(a,'cleaning brush')
    before=a.authoritative_digest()
    assert not a.water('collect','cleaning brush','debris tray').authoritative_changed
    assert before==a.authoritative_digest()
    act(a,'scrub','sorting board','cleaning brush')
    act(a,'collect','cleaning brush','debris tray')
    assert value(a,'adhered','sorting-board')==2
    assert value(a,'adhered','debris-tray')==2


def test_domain_operation_preserves_input_and_matches_application():
    a=app();workshop(a);take(a,'wash bucket')
    initial=a.water_state
    expected=execute(initial,a.water_profile,'pour',(identity('wash-bucket'),identity('pouring-jug')),2)
    assert a.water_state is initial
    act(a,'pour','wash bucket','pouring jug',amount=2)
    assert a.water_state==expected


def test_partial_terminal_sequence_preserves_first_step_after_refusal(tmp_path):
    a=app(tmp_path);workshop(a);take(a,'cleaning cloth')
    output=io.StringIO()
    run_terminal(a,input_stream=io.StringIO('soak cleaning cloth from wash bucket then wipe sorting board using cleaning cloth\nexit\n'),output_stream=output,specialized_router=execute_water_locality_request)
    assert 'Sequence halted' in output.getvalue()
    assert value(a,'water','cleaning-cloth')==1
    assert value(a,'adhered','sorting-board')==4
    assert WaterApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path).authoritative_digest()==a.authoritative_digest()


def test_neutral_ids_and_quantities_use_same_domain_without_fixture_branches():
    from astra_runtime.domain.persistent_world_water_cleaning import WaterCleaningProfile, WaterCleaningState, canonical_state, state_from_canonical
    a=app(); mapping={asset.id:f'neutral:sample:{i}' for i,asset in enumerate(a.water_profile.assets)}
    p=WaterCleaningProfile(tuple(replace(asset,id=mapping[asset.id]) for asset in a.water_profile.assets),
        tuple((op,mapping[left],mapping[right]) for op,left,right in a.water_profile.allowed_pairs))
    root=WaterCleaningState(*(tuple((mapping[k],v) for k,v in getattr(a.water_state,name)) for name in ('water','adhered','suspended')))
    result=execute(root,p,'fill',(mapping[identity('wash-bucket')],mapping[identity('pouring-jug')]))
    assert dict(result.water)[mapping[identity('pouring-jug')]]==3
    assert total_water(result)==12 and total_residue(result)==7
    assert state_from_canonical(canonical_state(result))==result


@pytest.mark.parametrize('change',['fraction','bool','missing','negative','overflow','dry_suspension'])
def test_invalid_state_and_noncanonical_fractions_fail_closed(change):
    from astra_runtime.domain.persistent_world_water_cleaning import canonical_state,state_from_canonical,validate
    a=app(); payload=canonical_state(a.water_state)
    if change=='fraction':payload['adhered'][0][1]=[0,2]
    elif change=='bool':payload['water'][0][1]=True
    elif change=='missing':payload['water'].pop()
    elif change=='negative':payload['adhered'][0][1]=[-1,1]
    elif change=='overflow':payload['water'][0][1]=100
    else:
        key=next(key for key,water in payload['water'] if water==0)
        next(row for row in payload['suspended'] if row[0]==key)[1]=[1,1]
    with pytest.raises(ValueError):validate(state_from_canonical(payload),a.water_profile)


def test_water_and_material_legacy_bindings_reject_each_others_checkpoints(tmp_path):
    from astra_runtime.myravant_material_application import MaterialApplication
    from astra_runtime.myravant_tarrow_material import create_material_fixture
    a=app(tmp_path);assert a.move('south').authoritative_changed
    with pytest.raises(ValueError):MaterialApplication.restore(checkpoint_path=a.checkpoint_path,fixture=create_material_fixture())
    b=MaterialApplication.new(fixture=create_material_fixture(),checkpoint_path=tmp_path/'old.json')
    assert b.move('south').authoritative_changed
    with pytest.raises(ValueError):WaterApplication.restore(checkpoint_path=b.checkpoint_path,fixture=a.fixture)


def test_wet_cargo_on_surface_inside_container_and_restart(tmp_path):
    a=app(tmp_path);workshop(a);take(a,'cleaning cloth')
    act(a,'soak','wash bucket','cleaning cloth');act(a,'wipe','practice panel','cleaning cloth')
    wet=a.water_state
    assert a.material('put_on','cleaning cloth','workroom bench').authoritative_changed
    assert not a.pickup('cleaning cloth').authoritative_changed
    assert a.material('lift_from','cleaning cloth','workroom bench').authoritative_changed
    assert a.open_object('parts tray').authoritative_changed
    assert a.store_object('cleaning cloth','parts tray').authoritative_changed
    assert a.close_object('parts tray').authoritative_changed
    assert a.displace_object('parts tray','east',method='push').authoritative_changed
    go(a,'east')
    assert a.open_object('parts tray').authoritative_changed
    assert a.retrieve_object('cleaning cloth','parts tray').authoritative_changed
    assert a.water_state==wet
    assert WaterApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path).water_state==wet


def test_restore_after_uncertain_write_replays_complete_surviving_checkpoint(tmp_path,monkeypatch):
    import astra_runtime.myravant_material_application as material
    a=app(tmp_path);workshop(a);take(a,'cleaning cloth');before=a.authoritative_digest()
    writer=material._write_envelope
    def replace_then_fail(**kwargs):
        writer(**kwargs)
        raise OSError('simulated failure after replacement')
    monkeypatch.setattr(material,'_write_envelope',replace_then_fail)
    r=a.water('soak','wash bucket','cleaning cloth')
    assert not r.authoritative_changed and a.authoritative_digest()==before
    assert a.water('soak','wash bucket','cleaning cloth').failure_class=='material_session_halted'
    restored=WaterApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path)
    assert value(restored,'water','cleaning-cloth')==1
    assert restored.authoritative_digest()!=before


def test_rinse_dry_brush_into_bath_moves_residue_and_retains_every_water_unit():
    a=app();workshop(a);take(a,'pouring jug');act(a,'fill','wash bucket','pouring jug')
    go(a,'east','east');take(a,'cleaning brush')
    act(a,'scrub','sorting board','cleaning brush');act(a,'rinse','cleaning brush','pouring jug')
    assert value(a,'adhered','cleaning-brush')==0
    assert value(a,'suspended','pouring-jug')==2 and value(a,'water','pouring-jug')==3


def test_soak_from_dirty_water_transfers_residue_into_cloth():
    a=app();workshop(a);take(a,'cleaning cloth');act(a,'soak','wash bucket','cleaning cloth')
    act(a,'wipe','practice panel','cleaning cloth');act(a,'fill','wash bucket','rinse basin')
    act(a,'rinse','cleaning cloth','rinse basin');act(a,'wring','cleaning cloth','pouring jug')
    act(a,'soak','rinse basin','cleaning cloth')
    assert value(a,'suspended','cleaning-cloth')==Fraction(1,7)
    assert value(a,'suspended','rinse-basin')==Fraction(5,7)

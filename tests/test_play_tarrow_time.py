"""Approved #546: time, ongoing work, drying, evidence and durable replay."""
from fractions import Fraction
import io
import json

import pytest

from astra_runtime.myravant_timed_application import TimedApplication
from astra_runtime.myravant_tarrow_time import create_timed_fixture, execute_timed_locality_request
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_terminal import run_terminal
from astra_runtime.domain.persistent_world_water_cleaning import total_water, total_residue


def app(tmp_path=None):
    return TimedApplication.new(fixture=create_timed_fixture(), checkpoint_path=tmp_path/'time.json' if tmp_path else None)


def tick(a):
    return a.runtime_state.logical_time_state.logical_position


def changed(result):
    assert result.authoritative_changed, result.message
    return result


def workshop(a):
    for direction in ('south','west','west','west'):
        changed(a.move(direction))


def quantity(a,field,name):
    return dict(getattr(a.water_state,field))[identity(name)]


def wet_cloth(a):
    workshop(a)
    changed(a.pickup('cleaning cloth'))
    changed(a.water('soak','wash bucket','cleaning cloth'))


def terminal(a,text):
    out=io.StringIO()
    run_terminal(a,input_stream=io.StringIO(text+'\nexit\n'), output_stream=out,
                 specialized_router=execute_timed_locality_request)
    return out.getvalue()


def test_physical_actions_advance_time_but_initial_refusals_do_not():
    a=app();start=tick(a)
    changed(a.move('south'))
    assert tick(a)==start+1
    before=a.authoritative_digest()
    r=a.water('wipe','practice panel','cleaning cloth')
    assert not r.authoritative_changed
    assert tick(a)==start+1 and a.authoritative_digest()==before


def test_help_describes_opt_in_drying_without_changing_old_water_help():
    from astra_runtime.myravant_tarrow_water import create_water_fixture
    help_text=create_timed_fixture().locality_help
    assert 'declared evaporation is tracked' in help_text
    assert 'no disposal into scenery or passive drying is qualified' not in help_text
    assert 'no disposal into scenery or passive drying is qualified' in create_water_fixture().locality_help


def test_bounded_wait_matches_repeated_single_intervals():
    a=app();b=app()
    for x in (a,b):wet_cloth(x)
    a.advance_duration(kind='wait',steps=8)
    for _ in range(8):changed(b.wait())
    assert a.authoritative_digest()==b.authoritative_digest()
    assert quantity(a,'water','cleaning-cloth')==0


@pytest.mark.parametrize('steps',[0,-1,True,1.5,'2',1000000000])
def test_invalid_duration_cannot_advance_or_mutate(steps):
    a=app();before=a.authoritative_digest();start=tick(a)
    try:r=a.advance_duration(kind='wait',steps=steps)
    except (ValueError,TypeError):pass
    else:
        if hasattr(r,'authoritative_changed'):assert not r.authoritative_changed
    assert a.authoritative_digest()==before and tick(a)==start


def test_wait_dries_cloth_without_working_on_dirty_panel():
    a=app();wet_cloth(a)
    initial=quantity(a,'adhered','practice-panel')
    a.advance_duration(kind='wait',steps=8)
    assert quantity(a,'water','cleaning-cloth')==0
    assert quantity(a,'adhered','practice-panel')==initial
    assert total_water(a.water_state)<12
    assert total_residue(a.water_state)==7


def test_start_pause_resume_metadata_does_not_advance_clock():
    a=app();wet_cloth(a);start=tick(a)
    changed(a.start_cleaning('practice panel','cleaning cloth'))
    assert tick(a)==start
    changed(a.task_control('pause'));assert tick(a)==start
    before=quantity(a,'adhered','practice-panel')
    r=a.work_step();assert not r.authoritative_changed
    assert quantity(a,'adhered','practice-panel')==before and tick(a)==start
    changed(a.task_control('resume'));assert tick(a)==start
    changed(a.work_step());assert tick(a)==start+1


def test_abandonment_preserves_committed_partial_cleaning():
    a=app();wet_cloth(a)
    changed(a.start_cleaning('practice panel','cleaning cloth'))
    changed(a.work_step())
    residue=quantity(a,'adhered','practice-panel')
    changed(a.task_control('abandon'))
    before=a.authoritative_digest()
    assert not a.work_step().authoritative_changed
    assert before==a.authoritative_digest()
    assert quantity(a,'adhered','practice-panel')==residue


def test_changed_prerequisites_requalified_after_pause():
    a=app();wet_cloth(a)
    changed(a.start_cleaning('practice panel','cleaning cloth'))
    changed(a.task_control('pause'))
    changed(a.drop('cleaning cloth'))
    a.task_control('resume')
    start=tick(a);before=quantity(a,'adhered','practice-panel')
    assert not a.work_step().authoritative_changed
    assert tick(a)==start and quantity(a,'adhered','practice-panel')==before


def test_restart_midprocess_matches_uninterrupted_world(tmp_path):
    a=app(tmp_path);wet_cloth(a)
    changed(a.start_cleaning('practice panel','cleaning cloth'))
    changed(a.wait())
    b=TimedApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path)
    assert a.authoritative_digest()==b.authoritative_digest()
    for x in (a,b):
        x.work_step();x.advance_duration(kind='wait',steps=5)
    assert a.authoritative_digest()==b.authoritative_digest()


def test_observation_is_readonly_and_does_not_expose_evidence_internals():
    a=app();wet_cloth(a);a.advance_duration(kind='wait',steps=5)
    before=a.authoritative_digest()
    message=a.inspect('cleaning cloth').message
    assert a.authoritative_digest()==before
    for token in ('receipt_id','logical_position','trace_id','requester_id'):
        assert token not in message
    assert 'water' in message.casefold()


def test_remote_inspection_does_not_reveal_workshop_changes():
    a=app();wet_cloth(a);a.advance_duration(kind='wait',steps=5)
    for direction in ('east','east','east','north'):changed(a.move(direction))
    before=a.authoritative_digest();message=a.inspect('practice panel').message
    assert a.authoritative_digest()==before
    assert 'scrubbed' not in message.casefold() and 'receipt' not in message.casefold()


def test_checkpoint_failure_rolls_back_clock_environment_and_task(tmp_path,monkeypatch):
    a=app(tmp_path);wet_cloth(a)
    before=a.authoritative_digest();saved=a.checkpoint_path.read_bytes();journal=a.journal
    def fail(**kwargs):raise OSError('simulated failed durable write')
    monkeypatch.setattr('astra_runtime.myravant_material_application._write_envelope',fail)
    r=a.wait()
    assert not r.authoritative_changed and r.failure_class
    assert a.authoritative_digest()==before and a.journal==journal
    assert a.checkpoint_path.read_bytes()==saved
    assert not a.wait().authoritative_changed


@pytest.mark.parametrize('change',['final','receipt','order','invented'])
def test_resealed_timed_checkpoint_forgery_rejected(tmp_path,change):
    import copy
    from astra_runtime.domain.persistent_world_material import digest
    a=app(tmp_path);wet_cloth(a);changed(a.wait())
    envelope=json.loads(a.checkpoint_path.read_text());data=envelope['payload']
    if change=='final':data['final']='0'*64
    elif change=='receipt':data['journal'][-1]['result']['receipt_id']='invented'
    elif change=='order':data['journal'][0],data['journal'][-1]=data['journal'][-1],data['journal'][0]
    else:data['journal'].append(copy.deepcopy(data['journal'][-1]))
    envelope['integrity_digest']=digest(data);a.checkpoint_path.write_text(json.dumps(envelope))
    with pytest.raises(ValueError):TimedApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path)


def test_water_and_timed_checkpoint_bindings_reject_each_other(tmp_path):
    from astra_runtime.myravant_water_application import WaterApplication
    from astra_runtime.myravant_tarrow_water import create_water_fixture
    a=app(tmp_path);changed(a.move('south'))
    with pytest.raises(ValueError):WaterApplication.restore(fixture=create_water_fixture(),checkpoint_path=a.checkpoint_path)
    b=WaterApplication.new(fixture=create_water_fixture(),checkpoint_path=tmp_path/'old.json')
    changed(b.move('south'))
    with pytest.raises(ValueError):TimedApplication.restore(fixture=a.fixture,checkpoint_path=b.checkpoint_path)


def test_terminal_duration_matches_direct_intervals():
    a=app();b=app()
    for x in (a,b):wet_cloth(x)
    text=terminal(a,'wait 5 steps')
    for _ in range(5):changed(b.wait())
    assert a.authoritative_digest()==b.authoritative_digest(),text


@pytest.mark.parametrize('command',['wait 2 steps permanently','wait 2 steps while cleaning','work 2 steps then wait then wait'])
def test_unsupported_duration_text_never_truncates(command):
    a=app();before=a.authoritative_digest();terminal(a,command)
    assert a.authoritative_digest()==before


def test_failed_later_interval_retains_previous_durable_acknowledgement(tmp_path,monkeypatch):
    import astra_runtime.myravant_material_application as material_app
    a=app(tmp_path)
    stream=a.duration_results('wait',3)
    changed(next(stream))
    acknowledged=a.authoritative_digest();saved=a.checkpoint_path.read_bytes()
    def fail(**kwargs):raise OSError('second interval cannot be written')
    monkeypatch.setattr(material_app,'_write_envelope',fail)
    failed=next(stream)
    assert failed.failure_class=='material_checkpoint_write_failed'
    assert not failed.authoritative_changed
    assert a.authoritative_digest()==acknowledged and tick(a)==1
    assert a.checkpoint_path.read_bytes()==saved
    assert TimedApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path).authoritative_digest()==acknowledged
    with pytest.raises(StopIteration):next(stream)


def test_output_failure_stops_duration_after_durable_interval(tmp_path):
    a=app(tmp_path)
    class BrokenOutput(io.StringIO):
        def write(self,text):
            if tick(a):raise OSError('lost output connection')
            return super().write(text)
    with pytest.raises(OSError):
        run_terminal(a,input_stream=io.StringIO('wait 3 steps\n'),output_stream=BrokenOutput(),
                     specialized_router=execute_timed_locality_request)
    restored=TimedApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path)
    assert tick(restored)==tick(a)==1
    assert restored.authoritative_digest()==a.authoritative_digest()


def test_sequence_duration_commits_each_interval_and_stops_on_later_refusal(tmp_path):
    a=app(tmp_path)
    text=terminal(a,'wait 2 steps then take cleaning cloth')
    assert tick(a)==2,text
    assert len(a.intervals)==2 and len(a.journal)==2
    restored=TimedApplication.restore(fixture=a.fixture,checkpoint_path=a.checkpoint_path)
    assert restored.authoritative_digest()==a.authoritative_digest()
    assert 'halted' in text.casefold()

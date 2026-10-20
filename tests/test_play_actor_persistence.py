"""Actor participation/evidence chronology survives durable interval boundaries."""
from dataclasses import replace
import io
import json

import pytest

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture, execute_actor_locality_request
from astra_runtime.myravant_timed_application import TimedApplication
from astra_runtime.myravant_water_application import WaterApplication
from astra_runtime.myravant_tarrow_time import create_timed_fixture
from astra_runtime.myravant_terminal import run_terminal
from astra_runtime.domain.persistent_world_material import digest, MaterialError


def app(tmp_path=None, count=2):
    base = create_actor_fixture()
    fixture = create_actor_fixture(actor_profiles=base.actor_profiles[:count])
    return ActorApplication.new(fixture=fixture, checkpoint_path=tmp_path/'actors.json' if tmp_path else None)


def changed(result):
    assert result.authoritative_changed, result.message
    return result


def tick(a):
    return a.runtime_state.logical_time_state.logical_position


def restore(a):
    return ActorApplication.restore(fixture=a.fixture, checkpoint_path=a.checkpoint_path)


def test_actor_checkpoint_replays_exact_chronology_and_observer_provenance(tmp_path):
    a = app(tmp_path)
    for _ in range(5):
        changed(a.wait())
    b = restore(a)
    assert b.authoritative_digest() == a.authoritative_digest()
    assert b.journal == a.journal
    assert b.actor_events == a.actor_events
    assert b.evidence_state == a.evidence_state
    assert b.participation_state == a.participation_state
    assert {e.actor_id for e in a.evidence_state.events} >= set(a.fixture.actor_order)
    changed(a.wait()); changed(b.wait())
    assert b.authoritative_digest() == a.authoritative_digest()


@pytest.mark.parametrize('count', [0, 1, 2])
def test_batched_duration_equals_single_intervals_across_condition_boundary(count):
    a, b = app(count=count), app(count=count)
    changed(a.advance_duration(kind='wait', steps=16))
    for _ in range(16):
        changed(b.wait())
    assert tick(a) == tick(b) == 16
    assert a.condition_events and a.condition_events == b.condition_events
    assert a.authoritative_digest() == b.authoritative_digest()
    assert a.journal == b.journal
    assert a.actor_events == b.actor_events
    assert a.evidence_state == b.evidence_state


@pytest.mark.parametrize('loader', [TimedApplication, WaterApplication])
def test_old_checkpoint_binding_rejects_actor_envelope(tmp_path, loader):
    a = app(tmp_path)
    changed(a.wait())
    with pytest.raises(MaterialError):
        loader.restore(checkpoint_path=a.checkpoint_path)


def test_actor_loader_rejects_old_time_envelope(tmp_path):
    old = TimedApplication.new(fixture=create_timed_fixture(), checkpoint_path=tmp_path/'old.json')
    changed(old.wait())
    with pytest.raises(MaterialError):
        ActorApplication.restore(checkpoint_path=old.checkpoint_path)


@pytest.mark.parametrize('change', ['performer', 'order', 'evidence', 'journal', 'final', 'extra_snapshot'])
def test_resealed_actor_checkpoint_tampering_is_rejected(tmp_path, change):
    a = app(tmp_path)
    for _ in range(3):
        changed(a.wait())
    changed(a.look())
    envelope = json.loads(a.checkpoint_path.read_text())
    payload = envelope['payload']
    if change == 'performer':
        payload['profile']['actors'][0]['actor_id'] = a.fixture.player_entity_id
    elif change == 'order':
        payload['profile']['order'].reverse()
    elif change == 'evidence':
        payload['journal'][-1]['result']['receipt_id'] = 'astra:actor_receipt:forged-witness'
    elif change == 'journal':
        payload['journal'] = list(reversed(payload['journal']))
    elif change == 'final':
        payload['final'] = '0'*64
    else:
        payload['evidence_snapshot'] = {'observer': a.fixture.player_entity_id, 'omniscient': True}
    envelope['integrity_digest'] = digest(payload)
    a.checkpoint_path.write_text(json.dumps(envelope))
    with pytest.raises(MaterialError):
        restore(a)


@pytest.mark.parametrize('after_replace', [False, True])
def test_write_fault_preserves_acknowledged_prefix_and_restart_recovers_disk(tmp_path, monkeypatch, after_replace):
    import astra_runtime.myravant_material_application as material
    a = app(tmp_path)
    changed(a.wait())
    acknowledged = a.authoritative_digest()
    acknowledged_journal = a.journal
    saved = a.checkpoint_path.read_bytes()
    original = material._write_envelope
    candidate = []
    def fail(**kwargs):
        candidate.append(a.authoritative_digest())
        if after_replace:
            original(**kwargs)
        raise OSError('simulated failure at durable replacement boundary')
    monkeypatch.setattr(material, '_write_envelope', fail)
    result = a.wait()
    assert result.failure_class == 'material_checkpoint_write_failed'
    assert not result.authoritative_changed
    assert a.authoritative_digest() == acknowledged and a.journal == acknowledged_journal
    assert tick(a) == 1
    assert not a.wait().authoritative_changed
    monkeypatch.setattr(material, '_write_envelope', original)
    b = restore(a)
    assert b.authoritative_digest() == (candidate[0] if after_replace else acknowledged)
    assert tick(b) == (2 if after_replace else 1)
    if not after_replace:
        assert a.checkpoint_path.read_bytes() == saved
    changed(b.wait())


def test_later_duration_write_failure_keeps_first_acknowledged_interval(tmp_path, monkeypatch):
    import astra_runtime.myravant_material_application as material
    a = app(tmp_path)
    stream = a.duration_results('wait', 4)
    changed(next(stream))
    acknowledged = a.authoritative_digest()
    def fail(**kwargs):
        raise OSError('cannot acknowledge interval two')
    monkeypatch.setattr(material, '_write_envelope', fail)
    result = next(stream)
    assert result.failure_class == 'material_checkpoint_write_failed'
    assert a.authoritative_digest() == acknowledged
    assert restore(a).authoritative_digest() == acknowledged
    with pytest.raises(StopIteration):
        next(stream)


def test_invariant_error_rolls_back_every_actor_and_physical_component(tmp_path, monkeypatch):
    a = app(tmp_path)
    changed(a.wait())
    before = a.authoritative_digest()
    snapshot = a._capture_transaction()
    saved = a.checkpoint_path.read_bytes()
    def fail():
        raise ValueError('injected joint actor invariant violation')
    monkeypatch.setattr(a, '_validate_transaction', fail)
    with pytest.raises(ValueError, match='injected joint actor'):
        a.wait()
    assert a.authoritative_digest() == before
    assert a._capture_transaction() == snapshot
    assert a.checkpoint_path.read_bytes() == saved


def test_output_failure_leaves_exact_one_actor_interval_durable(tmp_path):
    a = app(tmp_path)
    class BrokenOutput(io.StringIO):
        def write(self, text):
            if tick(a):
                raise OSError('lost display after durable acknowledgement')
            return super().write(text)
    with pytest.raises(OSError):
        run_terminal(a, input_stream=io.StringIO('wait 4 steps\n'), output_stream=BrokenOutput(),
                     specialized_router=execute_actor_locality_request)
    b = restore(a)
    assert tick(a) == tick(b) == 1
    assert a.authoritative_digest() == b.authoritative_digest()

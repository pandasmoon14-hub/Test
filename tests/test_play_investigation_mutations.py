"""Adversarial independent conditions for #552 investigation boundaries.

A failure here means that player inference may exceed admitted evidence,
that a report becomes truth, or that a read-only query changed the world.
"""
import re
import pytest

from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_tarrow_investigation import create_investigation_fixture
from astra_runtime.myravant_investigation_cases import build_investigation_case


def test_recall_cannot_refresh_world_truth_or_evidence():
    app = InvestigationApplication.new(fixture=create_investigation_fixture('neutral-relay'))
    assert app.move('east').authoritative_changed
    assert app.inspect('panel a').authoritative_changed
    before = (app.authoritative_digest(), app.evidence_state,
              app.runtime_state.logical_time_state.logical_position)
    response = app.recall_history('panel a', 'residue')
    assert 'Retained player history' in response.message
    assert not response.authoritative_changed
    assert (app.authoritative_digest(), app.evidence_state,
            app.runtime_state.logical_time_state.logical_position) == before


def test_only_requester_events_appear_in_history():
    app = InvestigationApplication.new(fixture=create_investigation_fixture('neutral-contended'))
    assert app.wait().authoritative_changed
    assert app.wait().authoritative_changed
    assert app.move('east').authoritative_changed
    reported = app.ask_report('Jun', 'panel a', 'activity')
    assert reported.authoritative_changed, reported.message
    player = app.fixture.player_entity_id
    own = [event for event in app.evidence_state.events
           if event.actor_id == player and event.facet == 'activity'
           and app.fixture.entity_name(event.target_id) == 'Panel A']
    assert own
    public = app.recall_history('panel a', 'activity').message
    listed = [line for line in public.splitlines() if re.match(r'^\d+\. ', line)]
    assert len(listed) == min(8, len(own))
    assert 'received statement from Jun' in public


def test_conflicting_report_is_never_a_truth_or_guilt_verdict(tmp_path):
    app, _ = build_investigation_case('neutral-relay', tmp_path / 'case.json')
    panel = next(p.entity_id for p in app.fixture.object_presentations if p.name == 'Panel A')
    assert dict(app.water_state.adhered)[panel] == 3
    text = app.compare_history('panel a', 'residue').message
    assert 'No account is selected as true, false, guilty or conclusive' in text
    assert 'clear' in text and 'present' in text


def test_disclosed_relay_speaker_survives_only_via_requester_history(tmp_path):
    app, _ = build_investigation_case('neutral-relay', tmp_path / 'relay.json')
    text = app.recall_history('panel a', 'residue').message
    assert 'earlier speaker disclosed as Traveler' in text
    assert len(app.disclosed_relays) == 1
    restored = InvestigationApplication.restore(
        fixture=create_investigation_fixture('neutral-relay'),
        checkpoint_path=tmp_path / 'relay.json')
    assert restored.recall_history('panel a', 'residue').message == text


def test_case_history_cannot_regenerate_over_saved_campaign(tmp_path):
    save = tmp_path / 'existing.json'
    app, _ = build_investigation_case('neutral-contended', save)
    stored = save.read_bytes()
    with pytest.raises(ValueError, match='existing checkpoint'):
        build_investigation_case('neutral-contended', save)
    assert save.read_bytes() == stored
    assert app.journal


def test_comparison_cannot_advance_world_time(tmp_path):
    app, _ = build_investigation_case('neutral-relay', tmp_path / 'clock.json')
    before = (app.authoritative_digest(),
              app.runtime_state.logical_time_state.logical_position,
              app.journal, app.evidence_state, app.work_state)
    result = app.compare_history('panel a', 'residue')
    assert not result.authoritative_changed and result.failure_class is None
    assert before == (app.authoritative_digest(),
                      app.runtime_state.logical_time_state.logical_position,
                      app.journal, app.evidence_state, app.work_state)

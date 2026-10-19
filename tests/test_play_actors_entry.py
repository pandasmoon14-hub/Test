"""Public #548 fixture/parser entry and separately authored installed objective."""
from dataclasses import replace
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_actors import ActorProfile, create_actor_fixture, parse_actor_request, execute_actor_locality_request
from astra_runtime.domain.persistent_world_material import placement


@pytest.mark.parametrize('text,expected', [
    ('ask Oren Kesh to clean practice panel', ('cleaning', ('oren kesh', 'practice panel', None, None))),
    ('ask Tali to clean sorting board using cleaning brush by scrubbing', ('cleaning', ('tali', 'sorting board', 'cleaning brush', 'scrub'))),
    ('ask Oren to assemble workshop assembly', ('assembly', ('oren', 'workshop assembly'))),
    ('ask Tali to cancel work', ('control', ('tali', 'cancel'))),
    ('ask Oren about work', ('status', ('oren',))),
])
def test_actor_entry_preserves_explicit_request(text, expected):
    assert parse_actor_request(text) == expected


@pytest.mark.parametrize('facet', ['residue', 'moisture', 'placement', 'assembly', 'trace', 'activity'])
def test_reports_admit_only_bound_facets(facet):
    assert parse_actor_request(f'ask Oren about practice panel {facet}') == ('report', ('oren', 'practice panel', facet))


@pytest.mark.parametrize('text', ['ask Oren about practice panel condition', 'ask Tali to cancel all jobs', 'ask Oren about practice panel culprit'])
def test_unknown_control_or_evidence_semantics_not_recognized(text):
    assert parse_actor_request(text) is None


def test_parser_dispatch_uses_typed_optional_method_and_tool():
    class Receiver:
        def request_cleaning(self, actor_reference, surface_reference, tool_reference=None, method=None):
            return actor_reference, surface_reference, tool_reference, method
    assert execute_actor_locality_request(Receiver(), 'ask Oren to clean practice panel using cleaning cloth by wiping') == (
        'actors', ('oren', 'practice panel', 'cleaning cloth', 'wipe'))


def test_fixture_profiles_bind_real_positions_without_initial_tool_custody():
    fixture = create_actor_fixture()
    from astra_runtime.myravant_actor_application import ActorApplication
    app = ActorApplication.new(fixture=fixture)
    assert app._actor_place_id(identity('oren')) == identity('work-bench')
    assert app._actor_place_id(identity('tali')) == identity('yard-tools')
    for key in ('cleaning-cloth', 'cleaning-brush'):
        assert placement(app.state.representation, identity(key)).relation_type != 'carried_by'
    assert fixture.ambient_visual_condition_for(identity('work-bench')) == 'sufficient'
    assert fixture.ambient_visual_condition_for(identity('yard-tools')) == 'sufficient'
    assert all(len(p.cleaning_pairs) == 4 and len(p.assembly_names) == 3 for p in fixture.actor_profiles)


def test_actor_order_and_policy_change_checkpoint_binding():
    fixture = create_actor_fixture()
    reversed_fixture = create_actor_fixture(actor_order=tuple(reversed(fixture.actor_order)))
    changed = create_actor_fixture(actor_profiles=(replace(fixture.actor_profiles[0], blocked_limit=2), fixture.actor_profiles[1]))
    assert len({f.provenance.initial_state_digest for f in (fixture, reversed_fixture, changed)}) == 3


@pytest.mark.parametrize('kwargs', [{'willing': 1}, {'blocked_limit': True}, {'blocked_limit': 0}, {'communication_classes': ('telepathy',)}, {'methods': ('magic',)}])
def test_invalid_development_policy_fails_closed(kwargs):
    with pytest.raises(ValueError):
        ActorProfile(identity('oren'), **kwargs)


def _installed_stage(checkpoint, trace, commands):
    launcher = shutil.which('myravant-play')
    assert launcher is not None, 'installed launcher required for public actor evidence'
    args = [launcher, '--locality', 'tarrow-actors', '--checkpoint', str(checkpoint), '--trace', str(trace)]
    if checkpoint.exists():
        args.extend(('--load', str(checkpoint)))
    result = subprocess.run(args, input='\n'.join((*commands, 'save', 'exit', '')), text=True, capture_output=True, timeout=60)
    assert result.returncode == 0, (result.stdout, result.stderr)
    rows = [json.loads(line) for line in trace.read_text().splitlines()]
    assert rows[-1]['evidence_complete']
    return result.stdout, [r for r in rows if r['record_type'] == 'interaction']


def test_installed_standing_cleanup_continues_and_reports_after_restart(tmp_path):
    """Objective-first: actual cleanup, one clock, private absence, restart, local report.

    Commands are bound to the public profile; intermediate checkpoint predicates
    determine whether to wait again, rather than assuming a successful transcript.
    """
    from astra_runtime.myravant_actor_application import ActorApplication
    finals = []
    for repeat in range(2):
        root = tmp_path / str(repeat); root.mkdir()
        checkpoint = root / 'state.json'
        _, rows = _installed_stage(checkpoint, root / 'first.jsonl', ('go south',))
        app = ActorApplication.restore(fixture=create_actor_fixture(), checkpoint_path=checkpoint)
        assert app.runtime_state.logical_time_state.logical_position == 1
        assert len(app.intervals) == 1
        assert not any('Soft-Iron Pin Blank' in str(row.get('visible_output', '')) for row in rows)
        steps = 1
        # Stay absent from the tool position while the bounded standing task runs.
        while dict(app.water_state.adhered)[identity('sorting-board')] and steps < 8:
            _, rows = _installed_stage(checkpoint, root / f'wait-{steps}.jsonl', ('wait',))
            app = ActorApplication.restore(fixture=create_actor_fixture(), checkpoint_path=checkpoint)
            steps += 1
            assert app.runtime_state.logical_time_state.logical_position == steps
        assert dict(app.water_state.adhered)[identity('sorting-board')] == 0
        task = next(t for t in app.participation_state.records if t.actor_id == identity('tali'))
        assert task.status == 'completed' and task.contributions
        text, rows = _installed_stage(checkpoint, root / 'report.jsonl', ('go west', 'inspect sorting board', 'ask Tali Ren about sorting board residue'))
        final = ActorApplication.restore(fixture=create_actor_fixture(), checkpoint_path=checkpoint)
        assert final.runtime_state.logical_time_state.logical_position == steps + 1
        assert 'reports' in text.casefold(), text
        assert 'Soft-Iron Pin Blank' not in text
        assert len(final.intervals) == steps + 1
        finals.append(final.authoritative_digest())
    assert finals[0] == finals[1]

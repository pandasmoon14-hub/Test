"""Neutral public investigation roots change precedence and actual resource outcomes."""
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_tarrow_investigation import create_investigation_fixture
from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.domain import persistent_world_actor_participation as participation


def _ids(root):
    return (next(p.entity_id for p in root.object_presentations if p.name == 'Brush'),
            *root.actor_order)


def test_neutral_roots_are_repeatable_and_distinct():
    keys = ('neutral-contended', 'neutral-reverse', 'neutral-relay')
    roots = [create_investigation_fixture(key) for key in keys]
    assert len({f.provenance.initial_state_digest for f in roots}) == 3
    assert len({f.actors_version for f in roots}) == 3
    for key, root in zip(keys, roots):
        assert create_investigation_fixture(key).provenance.initial_state_digest == root.provenance.initial_state_digest
    assert roots[0].actor_order == tuple(reversed(roots[1].actor_order))
    assert all(p.standing_kind is None for p in roots[2].actor_profiles)


def test_priority_and_withdrawal_change_effective_brush_outcomes(tmp_path):
    outcomes = []
    for key in ('neutral-contended', 'neutral-reverse'):
        fixture = create_investigation_fixture(key)
        app = InvestigationApplication.new(fixture=fixture, checkpoint_path=tmp_path / (key + '.json'))
        assert app.wait().authoritative_changed
        brush, winner, loser = _ids(fixture)
        assert placement(app.state.representation, brush).object_entity_id == winner
        assert len(participation.selected(app.participation_state, winner).contributions) == 1
        assert participation.selected(app.participation_state, loser).blocked_due == 1
        assert InvestigationApplication.restore(fixture=fixture, checkpoint_path=app.checkpoint_path).authoritative_digest() == app.authoritative_digest()
        outcomes.append(winner)
    assert outcomes[0] != outcomes[1]


def test_neutral_relay_is_attributed_and_durably_recallable(tmp_path):
    fixture = create_investigation_fixture('neutral-relay')
    app = InvestigationApplication.new(fixture=fixture, checkpoint_path=tmp_path / 'relay.json')
    assert app.move('east').authoritative_changed
    assert app.tell_actor('Jun', 'panel a', 'residue', 'clear').authoritative_changed
    assert app.ask_report('Jun', 'panel a', 'residue').authoritative_changed
    record = app.compare_history('panel a', 'residue').message
    assert 'earlier speaker disclosed as Visitor' in record
    assert 'No account is selected as true' in record
    assert InvestigationApplication.restore(fixture=fixture, checkpoint_path=app.checkpoint_path).compare_history('panel a', 'residue').message == record

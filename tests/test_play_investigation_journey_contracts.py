"""Short owner-backed scenario smoke; long installed runs stay in isolated evidence job."""
from astra_runtime.myravant_investigation_cases import build_investigation_case
from astra_runtime.domain import persistent_world_actor_participation as participation


def test_neutral_contested_history_remains_practical_after_read_only_queries(tmp_path):
    app, history = build_investigation_case("neutral-contended", tmp_path / "state.json")
    assert history and len(app.intervals) == 1
    actor = app.fixture.actor_order[0]
    selected = participation.selected(app.participation_state, actor)
    assert selected.contributions and selected.kind == "cleaning"
    before = (app.authoritative_digest(), app.water_state, app.journal)
    app.recall_history("panel a", "residue")
    app.compare_history("panel a", "residue")
    assert before == (app.authoritative_digest(), app.water_state, app.journal)


def test_assembly_root_alternative_is_open_to_lawful_player_choice(tmp_path):
    app, history = build_investigation_case("neutral-reverse", tmp_path / "state.json")
    assert history
    jun = next(p.entity_id for p in app.fixture.actor_presentations if p.name == "Jun")
    assert participation.selected(app.participation_state, jun).status == "withdrawn"
    assert app.move("east").authoritative_changed
    result = app.request_assembly("Jun", "joining frame")
    assert result.authoritative_changed, result.message
    assert participation.selected(app.participation_state, jun).kind == "assembly"

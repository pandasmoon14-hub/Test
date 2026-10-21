"""Opt-in investigation: no query refresh, leak or authority, and durable relay."""
from dataclasses import replace
import io
import json
import subprocess
import sys

import pytest

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_tarrow_investigation import (
    CASES, create_investigation_fixture, parse_investigation_request,
    execute_investigation_request,
)
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_material import MaterialError


def quiet_fixture(case="relay"):
    return create_investigation_fixture(case)


def at_workshop(app):
    for direction in ("south", "west", "west", "west"):
        assert app.move(direction).authoritative_changed


def test_recall_and_comparison_are_pure_even_when_current_world_changes(tmp_path):
    fixture = quiet_fixture()
    app = InvestigationApplication.new(fixture=fixture, checkpoint_path=tmp_path / "investigation.json")
    at_workshop(app)
    assert app.inspect("practice panel").authoritative_changed
    history = app.recall_history("practice panel", "residue")
    assert "own admitted observation" in history.message
    before = (app.authoritative_digest(), app.runtime_state.logical_time_state.logical_position,
              app.journal, app.evidence_state, app.work_state, app.actor_events)
    for _ in range(3):
        assert not app.recall_history("practice panel", "residue").authoritative_changed
        assert not app.compare_history("practice panel", "residue").authoritative_changed
    assert before == (app.authoritative_digest(), app.runtime_state.logical_time_state.logical_position,
                      app.journal, app.evidence_state, app.work_state, app.actor_events)
    restored = InvestigationApplication.restore(fixture=fixture, checkpoint_path=app.checkpoint_path)
    assert restored.recall_history("practice panel", "residue").message == history.message


def test_unknown_hidden_target_has_uniform_non_disclosing_query():
    app = InvestigationApplication.new(fixture=quiet_fixture())
    before = app.authoritative_digest()
    hidden = app.recall_history("soft iron pin blank", "residue")
    nonexistent = app.recall_history("a nonexistent invented object", "residue")
    assert hidden.message == nonexistent.message
    assert "soft iron pin blank" not in hidden.message.casefold()
    assert not hidden.authoritative_changed
    assert app.authoritative_digest() == before
    assert "No player-admitted accounts" in app.compare_history("invented", "residue").message


def test_received_relay_discloses_only_lawfully_spoken_prior_source(tmp_path):
    fixture = quiet_fixture()
    app = InvestigationApplication.new(fixture=fixture, checkpoint_path=tmp_path / "relay.json")
    at_workshop(app)
    target = identity("practice-panel")
    water_before = app.water_state
    assert app.tell_actor("Oren Kesh", "practice panel", "residue", "clear").authoritative_changed
    assert app.ask_report("Oren Kesh", "practice panel", "residue").authoritative_changed
    assert len(app.disclosed_relays) == 1
    text = app.recall_history("practice panel", "residue").message
    assert "received statement from" in text
    assert "earlier speaker disclosed as " + fixture.entity_name(fixture.player_entity_id) in text
    assert "clear" in text
    assert "source_event_id" not in text
    assert app.water_state == water_before
    before = app.authoritative_digest()
    resumed = InvestigationApplication.restore(fixture=fixture, checkpoint_path=app.checkpoint_path)
    assert resumed.authoritative_digest() == before
    assert resumed.recall_history("practice panel", "residue").message == text
    assert "No account is selected as true" in resumed.compare_history("practice panel", "residue").message


def test_old_actor_save_cannot_cross_investigation_binding(tmp_path):
    fixture = quiet_fixture()
    path = tmp_path / "state.json"
    investigation = InvestigationApplication.new(fixture=fixture, checkpoint_path=path)
    assert investigation.wait().authoritative_changed
    with pytest.raises(MaterialError):
        ActorApplication.restore(fixture=fixture, checkpoint_path=path)
    actor_path = tmp_path / "old.json"
    old = ActorApplication.new(fixture=create_investigation_fixture(), checkpoint_path=actor_path)
    assert old.wait().authoritative_changed
    with pytest.raises(MaterialError):
        InvestigationApplication.restore(fixture=old.fixture, checkpoint_path=actor_path)


def test_distinct_case_roots_and_exact_recipe_restart(tmp_path):
    fixtures = tuple(create_investigation_fixture(case) for case in CASES)
    assert len({f.provenance.initial_state_digest for f in fixtures}) == len(CASES)
    assert len({f.actors_version for f in fixtures}) == len(CASES)
    f = fixtures[1]
    path = tmp_path / "assembly.json"
    app = InvestigationApplication.new(fixture=f, checkpoint_path=path)
    assert app.wait().authoritative_changed
    assert InvestigationApplication.restore(fixture=f, checkpoint_path=path).authoritative_digest() == app.authoritative_digest()
    with pytest.raises(MaterialError):
        InvestigationApplication.restore(fixture=fixtures[0], checkpoint_path=path)


@pytest.mark.parametrize("source,kind", [
    ("recall practice panel residue", "recall"),
    ("compare reports about practice panel residue", "compare"),
    ("compare accounts about sorting board placement", "compare"),
])
def test_public_request_uses_explicit_topic_and_read_only_route(source, kind):
    assert parse_investigation_request(source)[0] == kind
    app = InvestigationApplication.new(fixture=quiet_fixture())
    before = app.authoritative_digest()
    routed = execute_investigation_request(app, source)
    assert routed[0] == "investigation"
    assert not routed[1].authoritative_changed
    assert app.authoritative_digest() == before


def test_unrecognized_query_does_not_take_over_other_intents():
    for text in ("inspect practice panel", "ask Oren to assemble workshop assembly",
                 "recall secret culprit", "compare guilt", "wait"):
        assert parse_investigation_request(text) is None


def test_inspection_does_not_refresh_private_speaker_evidence():
    app = InvestigationApplication.new(fixture=quiet_fixture())
    original = app.evidence_state
    before = app.authoritative_digest()
    assert "No player-admitted history" in app.recall_history("practice panel", "residue").message
    assert app.evidence_state == original and app.authoritative_digest() == before


def test_invalid_resealed_disclosure_state_rejected_by_owner_integrity():
    app = InvestigationApplication.new(fixture=quiet_fixture())
    app.disclosed_relays = (("invented-private-event", app.fixture.player_entity_id),)
    with pytest.raises(ValueError):
        app._validate_transaction()


def test_installed_cli_profile_and_read_only_public_query(tmp_path):
    file = tmp_path / "installed.json"
    command = [sys.executable, "-m", "astra_runtime.myravant_terminal",
               "--locality", "tarrow-investigation", "--investigation-case", "relay",
               "--checkpoint", str(file)]
    result = subprocess.run(command, input="recall practice panel residue\nsave\nexit\n",
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert "No player-admitted history" in result.stdout
    assert file.exists()
    restored = InvestigationApplication.restore(fixture=quiet_fixture(), checkpoint_path=file)
    assert restored.runtime_state.logical_time_state.logical_position == 0

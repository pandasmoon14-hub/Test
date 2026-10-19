"""Shared actor witness route and historical reporting under qualified inputs."""
from types import SimpleNamespace as N
import pytest
from astra_runtime import myravant_actor_knowledge as k
from astra_runtime.domain.persistent_world_actor_evidence import EvidenceState, latest


def fixture(monkeypatch):
    placements = {"player": N(relation_type="located_at", object_entity_id="room"),
                  "worker": N(relation_type="located_at", object_entity_id="room"),
                  "cloth": N(relation_type="located_at", object_entity_id="room"),
                  "hidden": N(relation_type="contained_by", object_entity_id="box")}
    monkeypatch.setattr(k, "placement", lambda rep, obj: placements[obj])
    places = {"player": "room", "worker": "room"}
    lights = {"player": True, "worker": True}
    app = N(_actor_place_id=lambda actor: places[actor],
        _actor_local_light_available=lambda actor: lights[actor],
        _visible_for_actor=lambda actor, obj: obj == "cloth",
        actor_profile=lambda actor: N(communication_classes=("local",)),
        state=N(representation=None), connections=(),
        fixture=N(object_presentations=(N(entity_id="cloth"), N(entity_id="hidden")),
                  ambient_visual_condition_for=lambda place: "insufficient", assemblies=()),
        water_state=N(suspended=(), water=(("cloth", 2), ("hidden", 9)), adhered=(("cloth", 1), ("hidden", 5))),
        environment_state=N(deposits=(), traces=(N(subject="cloth", kind="wet", receipt="private"),)))
    return app, places, lights, placements


def test_player_and_npc_share_same_witness_mechanism_without_hidden_target_leak(monkeypatch):
    app, _, _, _ = fixture(monkeypatch)
    state = k.observe(app, EvidenceState(), "player", "interval", 1)
    state = k.observe(app, state, "worker", "interval", 1)
    for actor in ("player", "worker"):
        assert latest(state, actor, "cloth", "moisture").value == "wet"
        assert latest(state, actor, "hidden", "moisture") is None
        assert latest(state, actor, "cloth", "trace").value == ("wet",)
    assert "private" not in repr(state)


def test_darkness_blocks_witness_even_when_carried_reach_would_allow_object(monkeypatch):
    app, _, lights, _ = fixture(monkeypatch)
    lights["worker"] = False
    assert k.observe(app, EvidenceState(), "worker", "interval", 1).events == ()


def test_communication_requires_declared_class_same_place_light_and_no_containment(monkeypatch):
    app, places, lights, placements = fixture(monkeypatch)
    assert k.communication_route(app, "player", "worker", "local")
    assert not k.communication_route(app, "player", "worker", "remote")
    places["worker"] = "elsewhere"
    assert not k.communication_route(app, "player", "worker", "local")
    places["worker"] = "room"
    lights["worker"] = False
    assert not k.communication_route(app, "player", "worker", "local")
    lights["worker"] = True
    placements["worker"] = N(relation_type="contained_by", object_entity_id="box")
    assert not k.communication_route(app, "player", "worker", "local")


def test_report_retains_historical_origin_source_without_world_refresh(monkeypatch):
    app, _, _, _ = fixture(monkeypatch)
    state = k.observe(app, EvidenceState(), "worker", "interval", 1)
    app.water_state.water = (("cloth", 0),)
    state = k.report(state, "worker", "player", "cloth", "moisture", "report", 5, qualified=True)
    result = latest(state, "player", "cloth", "moisture")
    assert result.value == "wet" and result.origin_tick == 1 and result.tick == 5
    assert result.kind == "reported" and result.source_actor_id == "worker"
    assert result.source_event_id == latest(state, "worker", "cloth", "moisture").event_id
    with pytest.raises(ValueError):
        k.report(state, "worker", "player", "cloth", "moisture", "bad", 6, qualified=False)


def test_missing_evidence_cannot_become_report_and_performance_remains_private():
    state = EvidenceState()
    assert k.report(state, "worker", "player", "cloth", "moisture", "report", 5, qualified=True) is state
    state = k.performed(state, "worker", "cloth", "residue", "clear", "effect", 1)
    assert latest(state, "player", "cloth", "residue") is None
    assert latest(state, "worker", "cloth", "residue").kind == "performed"
    with pytest.raises(ValueError):
        k.performed(state, "worker", "cloth", "hidden_truth", "clear", "effect", 1)

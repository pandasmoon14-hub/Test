"""C-1 installed investigation: witnessed facts vs hearsay, not world truth."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys

import pytest

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError,
)
from astra_runtime.myravant_actor_situated_knowledge import (
    ActorKnowledgeError, ActorKnowledgeState, commit_actor_knowledge,
    digest_actor_knowledge, restore_actor_knowledge,
    serialize_actor_knowledge,
)
from astra_runtime.myravant_c1_investigation_goal import (
    parse_actor_memory_request,
)
from astra_runtime.myravant_play_fixture import GATEHOUSE_ID, YARD_ID
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _meet_keeper_in_yard(app):
    assert app.move("south").authoritative_changed
    tick = app.wait()
    assert tick.authoritative_changed
    assert app.entity_place_id(app.fixture.resolve_actor_reference(
        "groundskeeper"
    )) == YARD_ID


def _witness(app):
    response = app.actor_memory_interaction("witness", "chest")
    assert response.authoritative_changed
    assert response.command_id and response.receipt_id
    assert response.pre_state_digest != response.post_state_digest
    return response


def test_witness_memory_is_stale_after_real_movement_not_omniscient(tmp_path):
    checkpoint = tmp_path / "c1.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _meet_keeper_in_yard(app)
    assert app.actor_memory_interaction(
        "last_saw", "chest"
    ).failure_class == "actor_knowledge_unknown"
    seen = _witness(app)
    assert "Yard" in seen.message
    placement = app.displace_object("chest", "north", method="push")
    assert placement.authoritative_changed
    observed = app.actor_memory_interaction("last_saw", "chest")
    assert "Yard" in observed.message
    assert "cannot confirm" in observed.message
    assert "Workshop" not in observed.message
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()
    replay_answer = restored.actor_memory_interaction("last_saw", "chest")
    assert replay_answer.message == observed.message
    assert not replay_answer.authoritative_changed
    assert len(restored.knowledge_state.events) == 1


def test_false_player_report_never_changes_world_or_overwrites_witness():
    app = MyravantVSM14Application.new()
    _meet_keeper_in_yard(app)
    _witness(app)
    before_place = app.entity_place_id(app.fixture.resolve_actor_reference(
        "groundskeeper"
    ))
    prior_world = app.representation_digest()
    claim = app.actor_memory_interaction(
        "report", "chest", reported_place="gatehouse"
    )
    assert claim.authoritative_changed
    assert "unverified report" in claim.message
    assert app.representation_digest() == prior_world
    assert app.entity_place_id(app.fixture.resolve_actor_reference(
        "groundskeeper"
    )) == before_place
    assert app.actor_memory_interaction(
        "recall", "chest"
    ).message.find("Gatehouse") >= 0
    assert "You told me" in app.actor_memory_interaction(
        "heard", "chest"
    ).message
    assert "Yard" in app.actor_memory_interaction(
        "last_saw", "chest"
    ).message
    assert app.knowledge_state.events[-1].reported_place_id == GATEHOUSE_ID


def test_remote_actor_and_unwitnessed_target_refuse_without_commit():
    app = MyravantVSM14Application.new()
    old = app.authoritative_digest()
    for operation in ("witness", "report", "last_saw", "heard", "recall"):
        outcome = app.actor_memory_interaction(
            operation, "chest", reported_place="yard"
        )
        assert not outcome.authoritative_changed
        assert outcome.failure_class == "actor_knowledge_actor_not_local"
    assert app.authoritative_digest() == old
    _meet_keeper_in_yard(app)
    old = app.authoritative_digest()
    answer = app.actor_memory_interaction("witness", "waystone")
    assert not answer.authoritative_changed
    assert answer.failure_class == "actor_knowledge_witness_opportunity_unavailable"
    assert app.authoritative_digest() == old
    assert app.actor_memory_interaction(
        "last_saw", "waystone"
    ).failure_class == "actor_knowledge_unknown"


def test_c1_replay_with_existing_latch_service_and_strict_integrity(tmp_path):
    checkpoint = tmp_path / "combined.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _meet_keeper_in_yard(app)
    _witness(app)
    worked = app.service_chest_latch("work", method="manual")
    assert worked.authoritative_changed
    assert app.service_state.progress == 1
    app.save()
    original = checkpoint.read_bytes()
    envelope = json.loads(original)
    assert envelope["format_version"] == 7
    assert "fixture_service" in envelope["authoritative_payload"]["components"]
    recovered = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert recovered.authoritative_digest() == app.authoritative_digest()
    assert recovered.service_state.progress == 1
    assert len(recovered.knowledge_state.events) == 1

    memory = envelope["authoritative_payload"]["components"]["actor_situated_knowledge"]
    memory["events"][0]["reported_place_id"] = GATEHOUSE_ID
    # Re-hash outer envelope as a malicious corruption attempt. The
    # independent memory replay/receipt chain must still reject it.
    payload = envelope["authoritative_payload"]
    envelope["integrity_digest"] = hashlib.sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True,
    ).encode()).hexdigest()
    checkpoint.write_text(json.dumps(envelope), encoding="utf-8")
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    checkpoint.write_bytes(original)
    assert MyravantVSM14Application.restore(
        checkpoint_path=checkpoint
    ).authoritative_digest() == app.authoritative_digest()


def test_replay_rejects_bool_time_and_duplicate_command_id():
    app = MyravantVSM14Application.new()
    _meet_keeper_in_yard(app)
    _witness(app)
    material = serialize_actor_knowledge(app.knowledge_state)
    material["events"][0]["logical_step"] = True
    with pytest.raises(ActorKnowledgeError):
        restore_actor_knowledge(material, maximum_step=20,
                                existing_command_ids=set())
    copied = serialize_actor_knowledge(app.knowledge_state)
    copied["events"].append(dict(copied["events"][0]))
    with pytest.raises(ActorKnowledgeError):
        restore_actor_knowledge(copied, maximum_step=20,
                                existing_command_ids=set())


def test_interpreter_separates_inquiry_witness_and_testimony():
    assert parse_actor_memory_request(
        "ask groundskeeper to inspect chest"
    ) == ("witness", "chest", None)
    assert parse_actor_memory_request(
        "tell the groundskeeper that chest is at gatehouse"
    ) == ("report", "chest", "gatehouse")
    assert parse_actor_memory_request(
        "ask groundskeeper where they last saw chest?"
    ) == ("last_saw", "chest", None)
    assert parse_actor_memory_request(
        "ask groundskeeper where they think chest is"
    ) == ("recall", "chest", None)
    for raw in ("ask groundskeeper for chest",
                "ask groundskeeper if they have chest",
                "ask council for a charter"):
        assert parse_actor_memory_request(raw) is None


def test_installed_two_session_investigation_is_durably_acked(tmp_path):
    checkpoint = tmp_path / "live.json"
    def session(commands, *args):
        return subprocess.run(
            [sys.executable, "-m", "astra_runtime.myravant_terminal",
             *args],
            input="\n".join((*commands, "exit", "")), text=True,
            capture_output=True, timeout=80,
        )

    first = session(
        ("go south", "wait", "ask groundskeeper to inspect chest",
         "push chest north"),
        "--checkpoint", str(checkpoint),
    )
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "directly observes" in first.stdout
    saved = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert len(saved.knowledge_state.events) == 1
    second = session(
        ("ask groundskeeper where they last saw chest",
         "tell groundskeeper chest is at gatehouse",
         "ask groundskeeper where they think chest is"),
        "--load", str(checkpoint),
    )
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert "cannot confirm" in second.stdout
    assert "unverified report" in second.stdout
    assert "You told me" in second.stdout
    final = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert len(final.knowledge_state.events) == 2
    assert final.knowledge_state.events[0].source_kind == "witnessed"
    assert final.knowledge_state.events[1].source_kind == "reported"

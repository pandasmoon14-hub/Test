"""Approved #534 combined posture family: state, behavior, replay and durability."""
from __future__ import annotations

import io
import json
import shutil
import subprocess
from dataclasses import replace

import pytest

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError, _canonical_bytes, _sha256_bytes,
)
from astra_runtime.myravant_posture import (
    PostureError, PostureProfile, PostureState, digest_posture,
    execute_posture, restore_posture, serialize_posture,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, ORCHARD_PATH_ID, PLAYER_ID, WAYSTONE_ID, WORKSHOP_ID, YARD_ID,
)
from astra_runtime.myravant_terminal import parse_terminal_command, run_terminal
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application as App
from astra_runtime.myravant_vsm14_follow_intent import execute_vsm14_follow_request


def obstruction(app):
    for result in (app.pickup("lantern"), app.light_object("lantern"),
                   app.move("south"), app.move("east"),
                   app.displace_object("waystone", "west", method="drag"), app.move("west")):
        assert result.authoritative_changed, result
    assert app.current_place_id() == app.entity_place_id(WAYSTONE_ID) == YARD_ID


def play(path, trace, commands, *, load=False):
    exe = shutil.which("myravant-play")
    assert exe, "installed executable required"
    args = [exe, "--checkpoint", str(path), "--trace", str(trace), "--repository-sha", "a" * 40]
    if load:
        args += ["--load", str(path)]
    proc = subprocess.run(args, input="\n".join((*commands, "save", "exit", "")),
                          text=True, capture_output=True, timeout=60)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    rows = [json.loads(r) for r in trace.read_text().splitlines()]
    return proc, [r for r in rows if r["record_type"] == "interaction"][:-1]


def rehash(path, mutate):
    material = json.loads(path.read_text())
    mutate(material)
    material["integrity_digest"] = _sha256_bytes(_canonical_bytes(material["authoritative_payload"]))
    path.write_bytes(_canonical_bytes(material))


@pytest.mark.parametrize("phrase,configuration", [
    ("stand", "standing"), ("stand up", "standing"), ("I crouch", "crouching"),
    ("kneel down", "kneeling"), ("sit down", "sitting"), ("lie down", "lying"),
])
def test_profile_configuration_parser(phrase, configuration):
    parsed = parse_terminal_command(phrase)
    assert parsed.action == "change_posture"
    assert parsed.argument == configuration
    assert parsed.raw_text == phrase


@pytest.mark.parametrize("phrase", [
    "crouch silently", "stand and listen", "lie down to heal", "sit on chest",
    "crouch then fly", "make groundskeeper kneel", "lean west", "sprint south",
    "face north", "lie down while crawling east",
])
def test_material_modifiers_and_unqualified_families_are_not_discarded(phrase):
    parsed = parse_terminal_command(phrase)
    assert parsed.action == "unsupported"
    assert parsed.raw_text == phrase


@pytest.mark.parametrize("configuration", ["standing", "crouching", "kneeling", "sitting", "lying"])
def test_all_five_change_only_configuration_and_repeat_truthfully(configuration):
    app = App.new()
    original_runtime = app.runtime_state
    assert "unrecorded" in app.inspect("self").view.description
    first = app.change_posture(configuration)
    assert first.authoritative_changed and first.receipt_id and first.state_delta_id
    assert app.runtime_state is original_runtime  # no location, time, custody, health fiction
    assert app.posture_state.configuration == configuration
    assert configuration in app.inspect("self").view.description
    before = app.authoritative_digest()
    again = app.change_posture(configuration)
    assert again.result_type == "posture_unchanged"
    assert not again.authoritative_changed and again.receipt_id is None
    assert len(app.posture_state.events) == 1 and app.authoritative_digest() == before


def owner_args(app):
    return dict(state=app.posture_state, profile=app.fixture.posture_profile,
                command_id="terminal-posture-000001", actor_id=PLAYER_ID,
                configuration="crouching", place_id=WORKSHOP_ID,
                representation_digest=app.representation_digest(), movement_count=0,
                logical_step=0, expected_pre_digest=digest_posture(app.posture_state))


@pytest.mark.parametrize("override", [
    {"actor_id": GROUNDSKEEPER_ID}, {"configuration": "flying"},
    {"place_id": "missing"}, {"expected_pre_digest": "a" * 64},
    {"movement_count": True}, {"logical_step": -1}, {"representation_digest": "garbage"},
    {"command_id": "terminal-posture-000002"},
])
def test_stale_or_unqualified_owner_requests_refuse_without_state(override):
    app = App.new()
    args = {**owner_args(app), **override}
    with pytest.raises(PostureError):
        execute_posture(**args)
    assert app.posture_state == PostureState()


def test_owner_retry_is_same_receipt_and_conflicting_identity_refuses_after_restore():
    app = App.new()
    args = owner_args(app)
    state, event = execute_posture(**args)
    restored = restore_posture(serialize_posture(state), profile=args["profile"])
    same, retried = execute_posture(**{**args, "state": restored})
    assert same is restored and retried == event and len(same.events) == 1
    with pytest.raises(PostureError):
        execute_posture(**{**args, "state": restored, "configuration": "standing"})


def test_nonhumanoid_contrast_and_missing_environment_opportunity():
    default = App.new().fixture
    profile = PostureProfile(actor_id=PLAYER_ID, profile_id="noncanonical-gliding-form",
                             version=1, configurations=("folded", "extended"), places=(WORKSHOP_ID,))
    app = App.new(fixture=replace(default, posture_profile=profile, posture_movement_licenses=()))
    for human in default.posture_profile.configurations:
        assert app.change_posture(human).failure_class
        assert not app.posture_state.events
    assert app.change_posture("folded").authoritative_changed
    assert app.move("south").authoritative_changed
    before = app.authoritative_digest()
    assert app.change_posture("extended").failure_class
    assert app.authoritative_digest() == before and app.posture_state.configuration == "folded"


@pytest.mark.parametrize("configuration,allowed", [
    ("standing", False), ("crouching", True), ("kneeling", True), ("sitting", False), ("lying", True),
])
def test_real_access_consequence_and_restored_behavior(tmp_path, configuration, allowed):
    path = tmp_path / "world.json"
    app = App.new(checkpoint_path=path)
    obstruction(app)
    assert app.change_posture(configuration).authoritative_changed
    assert app.save().checkpoint_digest
    app = App.restore(checkpoint_path=path)
    before = app.authoritative_digest()
    result = app.move("east")
    assert result.authoritative_changed == allowed
    assert app.current_place_id() == (ORCHARD_PATH_ID if allowed else YARD_ID)
    assert app.posture_state.configuration == configuration
    assert bool(result.failure_class) != allowed
    if not allowed:
        assert before == app.authoritative_digest()
        assert app.move("east", method="crawl").authoritative_changed
        assert app.posture_state.configuration == configuration  # method does not set posture
    else:
        assert ":posture-opportunity-" in result.opportunity_evidence_id
    app.save()
    restored = App.restore(checkpoint_path=path)
    assert restored.current_place_id() == ORCHARD_PATH_ID
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.move("west").authoritative_changed
    assert restored.move("east").authoritative_changed == allowed


def test_clear_route_does_not_bind_pose_or_change_historical_walk_receipt():
    posed, old = App.new(), App.new()
    posed.change_posture("lying")
    assert posed.move("south").receipt_id == old.move("south").receipt_id
    assert posed.posture_state.configuration == "lying"
    assert App.new().move("south", method="crawl").authoritative_changed
    assert not old.posture_state.events


def test_follower_cannot_inherit_lowered_passage_permission(tmp_path):
    app = App.new(checkpoint_path=tmp_path / "follow.json")
    obstruction(app)
    # WORLD-2 brings Groundskeeper to Yard; agreement is real independent intent.
    app.wait()
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    agreement = execute_vsm14_follow_request(app, "ask groundskeeper to follow me")
    assert agreement.result.authoritative_changed
    app.change_posture("crouching")
    result = app.move("east")
    assert result.authoritative_changed and result.consequence_receipt_id is None
    assert app.current_place_id() == ORCHARD_PATH_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    app.save()
    assert App.restore(checkpoint_path=app.checkpoint_path).entity_place_id(GROUNDSKEEPER_ID) == YARD_ID


def test_old_checkpoint_and_digest_remain_opt_in(tmp_path):
    from astra_runtime.myravant_e1_checkpoint import digest_e2_authoritative_state
    app = App.new(checkpoint_path=tmp_path / "old.json")
    app.move("south", method="crawl")
    old = digest_e2_authoritative_state(
        runtime_state=app.runtime_state, follow_intent_state=app.follow_intent_state,
        service_state=app.service_state, knowledge_state=app.knowledge_state,
        brace_state=app.brace_state, duty_state=app.duty_state,
    )
    assert app.authoritative_digest() == old
    app.save()
    assert json.loads(app.checkpoint_path.read_text())["format_version"] == 5
    restored = App.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest() == old
    assert "unrecorded" in restored.inspect("self").view.description
    restored.change_posture("standing")
    restored.save()
    assert json.loads(app.checkpoint_path.read_text())["format_version"] == 11


@pytest.mark.parametrize("change", ["profile_id", "version", "declarations"])
def test_restoration_rejects_profile_meaning_changes(tmp_path, change):
    app = App.new(checkpoint_path=tmp_path / "profile.json")
    app.change_posture("standing")
    app.save()
    profile = app.fixture.posture_profile
    if change == "profile_id":
        profile = replace(profile, profile_id="another")
    elif change == "version":
        profile = replace(profile, version=2)
    else:
        profile = replace(profile, configurations=("standing",))
    fixture = replace(app.fixture, posture_profile=profile, posture_movement_licenses=())
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        App.restore(checkpoint_path=app.checkpoint_path, fixture=fixture)


@pytest.mark.parametrize("field,value", [
    ("after", "standing"), ("receipt_id", "astra:posture_receipt:forged"),
    ("movement_count", 99), ("profile_version", True), ("place_id", YARD_ID),
    ("representation_digest", "a" * 64),
])
def test_rehashed_event_corruption_rejected(tmp_path, field, value):
    app = App.new(checkpoint_path=tmp_path / "corrupt.json")
    app.change_posture("crouching")
    app.save()
    rehash(app.checkpoint_path, lambda m: m["authoritative_payload"]["components"]["actor_posture"]["events"][0].update({field: value}))
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        App.restore(checkpoint_path=app.checkpoint_path)


def test_replay_rejects_removed_or_changed_movement_qualification(tmp_path):
    app = App.new(checkpoint_path=tmp_path / "join.json")
    obstruction(app)
    app.change_posture("crouching")
    app.move("east")
    app.save()
    # Removing the route declaration must not turn a stored qualified crossing
    # into permission granted by an arbitrary evidence ID.
    fixture = replace(app.fixture, posture_movement_licenses=())
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        App.restore(checkpoint_path=app.checkpoint_path, fixture=fixture)
    rehash(app.checkpoint_path, lambda m: (
        m.update(format_version=5),
        [m["authoritative_payload"]["components"].pop(k) for k in
         ("actor_posture", "fixture_duty", "fixture_brace", "actor_situated_knowledge", "fixture_service")]))
    # This otherwise valid v5 envelope must not shed the new owner provenance.
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        App.restore(checkpoint_path=app.checkpoint_path)


def test_installed_sequence_equivalence_partial_completion_and_refusal(tmp_path):
    standalone, srows = play(tmp_path / "single.json", tmp_path / "single.jsonl",
                             ("crouch", "inspect self"))
    sequence, qrows = play(tmp_path / "sequence.json", tmp_path / "sequence.jsonl",
                           ("crouch then inspect self",))
    assert len(srows) == len(qrows) == 2
    assert srows[0]["receipt_id"] == qrows[0]["receipt_id"]
    assert "Recorded posture: crouching" in sequence.stdout
    assert qrows[0]["post_state_digest"] == qrows[1]["pre_state_digest"]
    _, partial = play(tmp_path / "partial.json", tmp_path / "partial.jsonl",
                      ("sit then crawl north",))
    assert partial[0]["authoritative_changed"] and partial[1]["failure_class"]
    assert App.restore(checkpoint_path=tmp_path / "partial.json").posture_state.configuration == "sitting"
    _, refused = play(tmp_path / "refuse.json", tmp_path / "refuse.jsonl",
                      ("crawl north then stand",))
    assert len(refused) == 1 and refused[0]["failure_class"]
    assert not App.restore(checkpoint_path=tmp_path / "refuse.json").posture_state.events


def test_posture_save_failure_never_acknowledges_undurable_change(tmp_path, monkeypatch):
    from astra_runtime.domain.persistent_world_local_checkpoint_restore import PersistentWorldCheckpointWriteError
    import astra_runtime.myravant_posture_checkpoint as checkpoint
    path = tmp_path / "fault.json"
    app = App.new(checkpoint_path=path)
    app.save()
    saved = path.read_bytes()
    def fail(**kwargs):
        raise PersistentWorldCheckpointWriteError("injected write failure")
    monkeypatch.setattr(checkpoint, "_write_envelope", fail)
    out = io.StringIO()
    with pytest.raises(SystemExit) as failure:
        run_terminal(application=app, input_stream=io.StringIO("crouch then stand\n"),
                             output_stream=out)
    assert failure.value.code == 3
    assert "now crouching" not in out.getvalue() and "now standing" not in out.getvalue()
    assert path.read_bytes() == saved
    assert not App.restore(checkpoint_path=path).posture_state.events


@pytest.mark.parametrize("first", ["standing", "crouching", "kneeling", "sitting", "lying"])
@pytest.mark.parametrize("second", ["standing", "crouching", "kneeling", "sitting", "lying"])
def test_configuration_pair_matrix_is_profile_scoped_and_time_neutral(first, second):
    app = App.new()
    app.change_posture(first)
    before = app.authoritative_digest()
    result = app.change_posture(second)
    assert result.authoritative_changed == (first != second)
    assert app.posture_state.configuration == second
    assert app.runtime_state.logical_time_state.logical_position == 0
    assert len(app.posture_state.events) == (1 if first == second else 2)
    assert (app.authoritative_digest() != before) == (first != second)


def test_existing_posture_rejects_different_pinned_profile_at_execution():
    app = App.new()
    args = owner_args(app)
    state, _ = execute_posture(**args)
    changed = replace(args["profile"], version=2)
    with pytest.raises(PostureError):
        execute_posture(**{**args, "state": state, "profile": changed,
                           "configuration": "standing", "command_id": "terminal-posture-000002",
                           "expected_pre_digest": digest_posture(state)})


@pytest.mark.parametrize("owner", ["service", "brace", "duty", "npc_work", "knowledge"])
def test_new_component_coexists_with_existing_owner_replay_and_later_behavior(tmp_path, owner):
    app = App.new(checkpoint_path=tmp_path / f"{owner}.json")
    assert app.change_posture("crouching").authoritative_changed
    if owner == "npc_work":
        assert app.pickup("lantern").authoritative_changed
        assert app.light_object("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    if owner in {"service", "duty"}:
        assert app.service_chest_latch("work", method="manual").authoritative_changed
        assert app.service_chest_latch("work", method="manual").authoritative_changed
        if owner == "duty":
            assert app.close_object("chest").authoritative_changed
            assert app.groundskeeper_chest_duty("request").authoritative_changed
    elif owner == "brace":
        assert app.alter_chest_brace("manual").authoritative_changed
    else:
        assert app.wait().authoritative_changed
        if owner == "npc_work":
            assert app.drop("lantern").authoritative_changed
            assert app.request_groundskeeper_latch_work().authoritative_changed
        else:
            assert app.actor_memory_interaction("witness", "chest").authoritative_changed
    assert app.change_posture("kneeling").authoritative_changed
    app.save()
    restored = App.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.posture_state.configuration == "kneeling"
    if owner == "service":
        assert restored.service_state.progress == 2
        assert restored.open_object("chest").failure_class is None
    elif owner == "brace":
        assert restored.brace_state.condition == "loosened"
        assert restored.alter_chest_brace("refit").authoritative_changed
    elif owner == "duty":
        assert restored.duty_state.status == "pending"
        assert restored.move("north").authoritative_changed
        assert restored.wait().authoritative_changed
        assert restored.duty_state.status == "fulfilled"
    elif owner == "npc_work":
        assert restored.service_state.progress == 2
        assert restored.service_state.events[-1].actor_id == GROUNDSKEEPER_ID
    else:
        assert restored.knowledge_state.events == app.knowledge_state.events
        assert "Yard" in restored.actor_memory_interaction("last_saw", "chest").message
    restored.save()
    assert App.restore(checkpoint_path=app.checkpoint_path).posture_state.configuration == "kneeling"


def test_installed_posture_and_movement_sequence_receipts_match_direct(tmp_path):
    setup = ("take lantern", "light lantern", "go south", "go east", "drag waystone west", "go west")
    _, direct = play(tmp_path / "direct.json", tmp_path / "direct.jsonl", (*setup, "crouch", "walk east"))
    _, sequenced = play(tmp_path / "two.json", tmp_path / "two.jsonl", (*setup, "crouch then walk east"))
    assert [r["receipt_id"] for r in direct] == [r["receipt_id"] for r in sequenced]
    assert [r["post_state_digest"] for r in direct] == [r["post_state_digest"] for r in sequenced]
    assert App.restore(checkpoint_path=tmp_path / "two.json").current_place_id() == ORCHARD_PATH_ID


@pytest.mark.parametrize("override", [
    {"place_id": YARD_ID}, {"movement_count": 5}, {"logical_step": 1},
])
def test_locally_valid_owner_receipt_cannot_forge_its_world_anchor(tmp_path, override):
    app = App.new(checkpoint_path=tmp_path / "anchor.json")
    args = owner_args(app)
    forged, event = execute_posture(**{**args, **override})
    # This is valid AFQR-16 local evidence. Its AFQR-18/WORLD-2 join is false.
    assert restore_posture(serialize_posture(forged), profile=args["profile"]) == forged
    assert event.receipt_id
    app.change_posture("crouching")
    app.save()
    rehash(app.checkpoint_path, lambda m: m["authoritative_payload"]["components"].update(
        actor_posture=serialize_posture(forged)))
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        App.restore(checkpoint_path=app.checkpoint_path)


def test_valid_alternate_pose_receipt_cannot_qualify_recorded_crossing(tmp_path):
    app = App.new(checkpoint_path=tmp_path / "wrong-receipt.json")
    obstruction(app)
    args = {**owner_args(app), "place_id": YARD_ID,
            "movement_count": len(app.state.committed_transitions)}
    # Both transitions are locally legal from this actual prestate. Only the
    # crouching receipt qualifies the committed passage crossing.
    standing, _ = execute_posture(**{**args, "configuration": "standing"})
    app.change_posture("crouching")
    assert app.move("east").authoritative_changed
    app.save()
    rehash(app.checkpoint_path, lambda m: m["authoritative_payload"]["components"].update(
        actor_posture=serialize_posture(standing)))
    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        App.restore(checkpoint_path=app.checkpoint_path)

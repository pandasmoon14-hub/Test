"""COMP-2: observation-qualified nearby pickup composition regressions."""

from __future__ import annotations

from io import StringIO

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_live_play_evidence import (
    LivePlayEvidenceRecorder,
    build_live_play_session_header,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    ORCHARD_PATH_ID,
    WAYSTONE_ID,
    YARD_ID,
)
from astra_runtime.myravant_terminal import run_terminal


def _move_to_orchard_dark(app: MyravantPlayApplication) -> None:
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.move("south").result_type == "movement_committed"
    assert app.move("east").result_type == "movement_committed"


def _direct_place_for(app: MyravantPlayApplication, entity_id: str) -> str | None:
    matches = [
        relation
        for relation in app.state.representation.relations
        if (
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == entity_id
        )
    ]
    if not matches:
        return None
    assert len(matches) == 1
    return matches[0].object_entity_id


def _is_carried(app: MyravantPlayApplication, entity_id: str) -> bool:
    return any(
        relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == entity_id
        and relation.object_entity_id == app.fixture.player_entity_id
        for relation in app.state.representation.relations
    )


def test_comp2_dark_nearby_waystone_rejects_deterministically_without_commit():
    app = MyravantPlayApplication.new()
    _move_to_orchard_dark(app)
    before = app.authoritative_digest()
    observation = app.visual_observation_evidence(WAYSTONE_ID)

    assert observation.observable is False
    assert "Weathered Waystone" not in app.look().view.objects
    assert app.inspect("waystone").result_type == "inspection_unavailable"

    first = app.pickup("waystone")
    second = app.pickup("waystone")

    for result in (first, second):
        assert result.result_type == "custody_rejected"
        assert result.message == "You cannot pick that up in the current state."
        assert result.failure_class == "PersistentWorldObjectCustodyEvidenceError"
        assert result.authoritative_changed is False
        assert result.receipt_id is None
        assert result.state_delta_id is None
        assert result.observation_evidence_id == observation.evidence_id
        assert result.opportunity_evidence_id is not None
        assert result.pre_state_digest == before
        assert result.post_state_digest == before

    assert first.command_id == second.command_id
    assert first.observation_evidence_id == second.observation_evidence_id
    assert first.opportunity_evidence_id == second.opportunity_evidence_id
    assert app.authoritative_digest() == before
    assert len(app.custody_state.committed_custody_transitions) == 1


def test_comp2_pickup_rejection_does_not_make_exact_name_an_existence_oracle():
    app = MyravantPlayApplication.new()
    _move_to_orchard_dark(app)
    before = app.authoritative_digest()

    hidden_local = app.pickup("waystone")
    remote_declared = app.pickup("tool chest")
    unknown = app.pickup("sword")

    assert hidden_local.message == remote_declared.message == unknown.message
    assert hidden_local.message == "You cannot pick that up in the current state."
    assert app.authoritative_digest() == before


def test_comp2_light_creates_pickup_opportunity_with_cross_owner_provenance():
    app = MyravantPlayApplication.new()
    _move_to_orchard_dark(app)
    assert app.light_object("lantern").result_type == "object_lit_state_committed"

    observation = app.visual_observation_evidence(WAYSTONE_ID)
    assert observation.observable is True
    result = app.pickup("waystone")

    assert result.result_type == "custody_committed"
    assert result.authoritative_changed is True
    assert result.observation_evidence_id == observation.evidence_id
    assert result.opportunity_evidence_id is not None
    assert _is_carried(app, WAYSTONE_ID)

    transition = app.custody_state.committed_custody_transitions[-1]
    assert transition.receipt.object_entity_id == WAYSTONE_ID
    assert transition.preview.metadata["opportunity_input_evidence_refs"] == [
        observation.evidence_id
    ]
    assert transition.state_delta.metadata["opportunity_input_evidence_refs"] == [
        observation.evidence_id
    ]


def test_comp2_loss_of_light_does_not_undo_custody_or_block_drop():
    app = MyravantPlayApplication.new()
    _move_to_orchard_dark(app)
    assert app.light_object("lantern").result_type == "object_lit_state_committed"
    assert app.pickup("waystone").result_type == "custody_committed"

    assert app.extinguish_object("lantern").result_type == "object_lit_state_committed"
    assert _is_carried(app, WAYSTONE_ID)
    assert app.move("west").result_type == "movement_committed"
    dropped = app.drop("waystone")

    assert dropped.result_type == "custody_committed"
    assert _direct_place_for(app, WAYSTONE_ID) == YARD_ID
    assert not _is_carried(app, WAYSTONE_ID)


def test_comp2_relocated_waystone_survives_save_restore_and_does_not_rematerialize(tmp_path):
    checkpoint = tmp_path / "comp2-relocation.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    _move_to_orchard_dark(app)
    assert app.light_object("lantern").result_type == "object_lit_state_committed"
    pickup = app.pickup("waystone")
    assert pickup.result_type == "custody_committed"
    assert app.extinguish_object("lantern").result_type == "object_lit_state_committed"
    assert app.move("west").result_type == "movement_committed"
    assert app.drop("waystone").result_type == "custody_committed"
    assert app.save().result_type == "checkpoint_written"

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.current_place_id() == YARD_ID
    assert _direct_place_for(restored, WAYSTONE_ID) == YARD_ID

    pickup_transitions = [
        transition
        for transition in restored.custody_state.committed_custody_transitions
        if (
            transition.receipt.object_entity_id == WAYSTONE_ID
            and transition.receipt.operation == "pickup"
        )
    ]
    assert len(pickup_transitions) == 1
    refs = pickup_transitions[0].preview.metadata["opportunity_input_evidence_refs"]
    assert refs == [pickup.observation_evidence_id]

    assert restored.move("east").result_type == "movement_committed"
    assert restored.current_place_id() == ORCHARD_PATH_ID
    assert _direct_place_for(restored, WAYSTONE_ID) == YARD_ID
    assert "Weathered Waystone" not in restored.look().view.objects


def test_comp2_remote_light_does_not_create_pickup_opportunity():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.light_object("lantern").result_type == "object_lit_state_committed"
    assert app.drop("lantern").result_type == "custody_committed"
    assert app.move("south").result_type == "movement_committed"
    assert app.move("east").result_type == "movement_committed"

    assert app.visual_observation_evidence(WAYSTONE_ID).observable is False
    result = app.pickup("waystone")
    assert result.result_type == "custody_rejected"
    assert result.failure_class == "PersistentWorldObjectCustodyEvidenceError"
    assert result.receipt_id is None
    assert result.state_delta_id is None


def test_comp2_closed_container_blocks_and_open_container_restores_pickup_opportunity():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").result_type == "custody_committed"
    assert app.light_object("lantern").result_type == "object_lit_state_committed"
    assert app.move("south").result_type == "movement_committed"
    assert app.open_object("chest").result_type == "object_state_committed"
    assert app.store_object("lantern", "chest").result_type == "storage_committed"
    assert app.close_object("chest").result_type == "object_state_committed"
    assert app.pickup("chest").result_type == "custody_committed"
    assert app.move("east").result_type == "movement_committed"

    assert app.visual_observation_evidence(WAYSTONE_ID).observable is False
    rejected = app.pickup("waystone")
    assert rejected.result_type == "custody_rejected"
    assert rejected.receipt_id is None

    assert app.open_object("chest").result_type == "object_state_committed"
    observation = app.visual_observation_evidence(WAYSTONE_ID)
    assert observation.observable is True
    committed = app.pickup("waystone")
    assert committed.result_type == "custody_committed"
    assert committed.observation_evidence_id == observation.evidence_id


def test_comp2_existing_visible_direct_pickup_behavior_remains_available():
    app = MyravantPlayApplication.new()
    lantern = app.pickup("lantern")
    assert lantern.result_type == "custody_committed"
    assert lantern.observation_evidence_id is not None

    app = MyravantPlayApplication.new()
    assert app.move("south").result_type == "movement_committed"
    chest = app.pickup("chest")
    assert chest.result_type == "custody_committed"
    assert chest.observation_evidence_id is not None


def test_comp2_terminal_trace_preserves_observation_reference_without_player_leak(tmp_path):
    trace_path = tmp_path / "comp2-trace.jsonl"
    app = MyravantPlayApplication.new()
    header = build_live_play_session_header(
        session_id="comp2-hidden-pickup",
        campaign_id=app.fixture.campaign_id,
        repository_sha="c" * 40,
        initial_state_digest=app.authoritative_digest(),
        restore_performed=False,
        environment_id="ENV-T2-TERMUX-ARM64-DEV",
        network_mode="offline",
    )
    recorder = LivePlayEvidenceRecorder(trace_path=trace_path, header=header)
    output = StringIO()

    exit_code = run_terminal(
        app,
        input_stream=StringIO(
            "pickup lantern\nmove south\nmove east\npickup waystone\nexit\n"
        ),
        output_stream=output,
        debug=False,
        evidence_recorder=recorder,
        evidence_error_stream=StringIO(),
    )

    assert exit_code == 0
    assert "Weathered Waystone" not in output.getvalue()
    assert "You cannot pick that up in the current state." in output.getvalue()

    interactions = [
        __import__("json").loads(line)
        for line in trace_path.read_text(encoding="utf-8").splitlines()
        if '"record_type":"interaction"' in line
    ]
    pickup = interactions[-1]
    assert pickup["parsed_action"] == "pickup"
    assert pickup["parsed_argument"] == "waystone"
    assert pickup["result_type"] == "custody_rejected"
    assert pickup["observation_evidence_id"] is not None
    assert pickup["opportunity_evidence_id"] is not None
    assert pickup["receipt_id"] is None
    assert pickup["state_delta_id"] is None

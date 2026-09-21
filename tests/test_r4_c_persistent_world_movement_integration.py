"""Executable R4-C persistent-world movement integration tests."""

from __future__ import annotations

import ast
import inspect
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
    create_located_at_relation,
    create_persistent_world_entity,
    create_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementDestinationNotPlaceError,
    PersistentWorldMovementEntityNotFoundError,
    PersistentWorldMovementOwnerEvidenceError,
    PersistentWorldMovementReplayError,
    PersistentWorldMovementRetryConflictError,
    PersistentWorldMovementSourceLocationError,
    PersistentWorldMovementStaleStateError,
    UnsupportedPersistentWorldMovementCommandError,
    canonical_serialize_persistent_world_movement_commit_receipt,
    commit_prepared_persistent_world_movement,
    create_movement_opportunity_evidence,
    create_movement_spatial_evidence,
    create_persistent_world_movement_runtime_state,
    digest_persistent_world_entity_location_representation,
    execute_persistent_world_movement,
    prepare_persistent_world_movement,
    replay_persistent_world_movement,
)
from astra_runtime.kernel.command_envelope import (
    create_command_envelope,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "src/astra_runtime/domain/"
    "persistent_world_movement_integration.py"
)

ACTOR = "astra:entity:traveler"
P1 = "astra:entity:market-square"
P2 = "astra:entity:river-gate"
P3 = "astra:entity:hill-road"


def _entity(local: str, classification: str):
    return create_persistent_world_entity(
        entity_id=f"astra:entity:{local}",
        classification=classification,
    )


def _relation(
    local: str,
    subject: str,
    place: str,
):
    return create_located_at_relation(
        relation_id=f"astra:relation:{local}",
        subject_entity_id=subject,
        object_entity_id=place,
    )


def _representation(
    *,
    source_locations: tuple[str, ...] = (P1,),
    destination_classification: str = "place",
    include_destination: bool = True,
):
    traveler = _entity(
        "traveler",
        "character_or_creature",
    )
    p1 = _entity("market-square", "place")
    p2 = _entity(
        "river-gate",
        destination_classification,
    )
    p3 = _entity("hill-road", "place")

    entities = [traveler, p1, p3]
    if include_destination:
        entities.append(p2)

    relations = [
        _relation(
            f"traveler-location-{index}",
            ACTOR,
            place,
        )
        for index, place in enumerate(
            source_locations,
            start=1,
        )
    ]

    return (
        create_persistent_world_entity_location_representation(
            campaign_id="astra:campaign:r4c-test",
            entities=entities,
            relations=relations,
        )
    )


def _command(
    *,
    command_id: str = "move-command-1",
    destination: str = P2,
    command_type: str = "move",
):
    return create_command_envelope(
        command_id=command_id,
        command_type=command_type,
        source_actor_id=ACTOR,
        payload={
            "destination_entity_id": destination,
        },
    )


def _spatial(
    *,
    source: str = P1,
    destination: str = P2,
    permitted: bool = True,
):
    return create_movement_spatial_evidence(
        evidence_id="astra:evidence:r4c-spatial",
        actor_entity_id=ACTOR,
        source_place_id=source,
        destination_place_id=destination,
        spatially_permitted=permitted,
    )


def _opportunity(
    *,
    destination: str = P2,
    available: bool = True,
    accepted: bool = True,
):
    return create_movement_opportunity_evidence(
        evidence_id="astra:evidence:r4c-opportunity",
        actor_entity_id=ACTOR,
        destination_place_id=destination,
        opportunity_available=available,
        resolution_accepted=accepted,
    )


def _state(representation=None):
    if representation is None:
        representation = _representation()

    return create_persistent_world_movement_runtime_state(
        representation=representation,
    )


def _digest(state):
    return (
        digest_persistent_world_entity_location_representation(
            state.representation
        )
    )


def _actor_locations(representation):
    return [
        relation
        for relation in representation.relations
        if (
            relation.relation_type
            == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == ACTOR
        )
    ]


def test_existing_command_router_classifies_move_as_movement():
    state = _state()
    prepared = prepare_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    assert prepared.routing_family == "movement"
    assert (
        prepared.owner_route
        == "RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY"
    )


def test_preparation_is_non_mutating():
    state = _state()
    before = _digest(state)

    prepared = prepare_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=before,
    )

    assert _digest(state) == before
    assert prepared.pre_state_digest == before
    assert prepared.post_state_digest != before
    assert prepared.preview.metadata["mutation_performed"] is False


def test_successful_commit_moves_actor_from_p1_to_p2_atomically():
    state = _state()

    result = execute_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    before_locations = _actor_locations(
        state.representation
    )
    after_locations = _actor_locations(
        result.state.representation
    )

    assert len(before_locations) == 1
    assert before_locations[0].object_entity_id == P1

    assert len(after_locations) == 1
    assert after_locations[0].object_entity_id == P2

    assert result.technical_retry is False
    assert result.receipt.source_place_id == P1
    assert result.receipt.destination_place_id == P2


def test_successful_commit_emits_relationship_update_delta():
    state = _state()

    result = execute_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    delta = result.state_delta

    assert delta.change_type == "relationship_update"
    assert delta.payload["subject_entity_id"] == ACTOR
    assert delta.payload["from_place_id"] == P1
    assert delta.payload["to_place_id"] == P2


def test_receipt_binds_command_state_locations_and_evidence():
    state = _state()

    result = execute_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    receipt = result.receipt

    assert receipt.command_id == "move-command-1"
    assert receipt.actor_entity_id == ACTOR
    assert receipt.source_place_id == P1
    assert receipt.destination_place_id == P2
    assert (
        receipt.pre_state_digest
        == _digest(state)
    )
    assert (
        receipt.post_state_digest
        == _digest(result.state)
    )
    assert (
        receipt.spatial_evidence_id
        == "astra:evidence:r4c-spatial"
    )
    assert (
        receipt.opportunity_evidence_id
        == "astra:evidence:r4c-opportunity"
    )


def test_subsequent_authoritative_read_observes_p2():
    state = _state()

    result = execute_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    location = _actor_locations(
        result.state.representation
    )

    assert len(location) == 1
    assert location[0].object_entity_id == P2


def test_missing_actor_fails_closed():
    representation = _representation()

    command = create_command_envelope(
        command_id="missing-actor",
        command_type="move",
        source_actor_id="astra:entity:missing",
        payload={"destination_entity_id": P2},
    )

    state = _state(representation)

    with pytest.raises(
        PersistentWorldMovementEntityNotFoundError
    ):
        execute_persistent_world_movement(
            state=state,
            command=command,
            spatial_evidence=create_movement_spatial_evidence(
                evidence_id="astra:evidence:missing-spatial",
                actor_entity_id="astra:entity:missing",
                source_place_id=P1,
                destination_place_id=P2,
                spatially_permitted=True,
            ),
            opportunity_evidence=(
                create_movement_opportunity_evidence(
                    evidence_id=(
                        "astra:evidence:missing-opportunity"
                    ),
                    actor_entity_id="astra:entity:missing",
                    destination_place_id=P2,
                    opportunity_available=True,
                    resolution_accepted=True,
                )
            ),
            expected_pre_state_digest=_digest(state),
        )

    assert _digest(state) == (
        digest_persistent_world_entity_location_representation(
            representation
        )
    )


def test_missing_destination_fails_closed():
    representation = _representation(
        include_destination=False
    )
    state = _state(representation)

    with pytest.raises(
        PersistentWorldMovementEntityNotFoundError
    ):
        execute_persistent_world_movement(
            state=state,
            command=_command(),
            spatial_evidence=_spatial(),
            opportunity_evidence=_opportunity(),
            expected_pre_state_digest=_digest(state),
        )


def test_non_place_destination_fails_closed():
    state = _state(
        _representation(
            destination_classification="object"
        )
    )

    with pytest.raises(
        PersistentWorldMovementDestinationNotPlaceError
    ):
        execute_persistent_world_movement(
            state=state,
            command=_command(),
            spatial_evidence=_spatial(),
            opportunity_evidence=_opportunity(),
            expected_pre_state_digest=_digest(state),
        )


def test_zero_source_locations_fail_closed():
    state = _state(
        _representation(source_locations=())
    )

    with pytest.raises(
        PersistentWorldMovementSourceLocationError
    ):
        execute_persistent_world_movement(
            state=state,
            command=_command(),
            spatial_evidence=_spatial(),
            opportunity_evidence=_opportunity(),
            expected_pre_state_digest=_digest(state),
        )


def test_multiple_source_locations_fail_closed():
    state = _state(
        _representation(
            source_locations=(P1, P3)
        )
    )

    with pytest.raises(
        PersistentWorldMovementSourceLocationError
    ):
        execute_persistent_world_movement(
            state=state,
            command=_command(),
            spatial_evidence=_spatial(),
            opportunity_evidence=_opportunity(),
            expected_pre_state_digest=_digest(state),
        )


def test_afqr18_spatial_rejection_fails_closed():
    state = _state()

    with pytest.raises(
        PersistentWorldMovementOwnerEvidenceError
    ):
        execute_persistent_world_movement(
            state=state,
            command=_command(),
            spatial_evidence=_spatial(
                permitted=False
            ),
            opportunity_evidence=_opportunity(),
            expected_pre_state_digest=_digest(state),
        )

    assert _actor_locations(
        state.representation
    )[0].object_entity_id == P1


@pytest.mark.parametrize(
    ("available", "accepted"),
    [
        (False, True),
        (True, False),
        (False, False),
    ],
)
def test_afqr19_rejection_fails_closed(
    available,
    accepted,
):
    state = _state()

    with pytest.raises(
        PersistentWorldMovementOwnerEvidenceError
    ):
        execute_persistent_world_movement(
            state=state,
            command=_command(),
            spatial_evidence=_spatial(),
            opportunity_evidence=_opportunity(
                available=available,
                accepted=accepted,
            ),
            expected_pre_state_digest=_digest(state),
        )


def test_owner_evidence_mismatch_fails_closed():
    state = _state()

    with pytest.raises(
        PersistentWorldMovementOwnerEvidenceError
    ):
        execute_persistent_world_movement(
            state=state,
            command=_command(),
            spatial_evidence=_spatial(
                destination=P3
            ),
            opportunity_evidence=_opportunity(),
            expected_pre_state_digest=_digest(state),
        )


def test_stale_pre_state_digest_fails_without_mutation():
    state = _state()
    before = state

    with pytest.raises(
        PersistentWorldMovementStaleStateError
    ):
        execute_persistent_world_movement(
            state=state,
            command=_command(),
            spatial_evidence=_spatial(),
            opportunity_evidence=_opportunity(),
            expected_pre_state_digest="0" * 64,
        )

    assert state == before


def test_prepared_transition_can_be_abandoned_without_state_change():
    state = _state()
    before = state

    prepare_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    assert state == before


def test_commit_rejects_state_change_after_preparation():
    state = _state()

    prepared = prepare_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    altered_representation = (
        create_persistent_world_entity_location_representation(
            campaign_id=state.representation.campaign_id,
            entities=state.representation.entities,
            relations=[
                _relation(
                    "traveler-altered",
                    ACTOR,
                    P3,
                )
            ],
        )
    )

    altered_state = _state(
        altered_representation
    )

    with pytest.raises(
        PersistentWorldMovementStaleStateError
    ):
        commit_prepared_persistent_world_movement(
            state=altered_state,
            prepared=prepared,
        )


def test_technical_retry_returns_prior_result_without_second_move():
    state = _state()
    pre_digest = _digest(state)
    command = _command()

    first = execute_persistent_world_movement(
        state=state,
        command=command,
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=pre_digest,
    )

    retry = execute_persistent_world_movement(
        state=first.state,
        command=command,
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=pre_digest,
    )

    assert retry.technical_retry is True
    assert retry.state == first.state
    assert retry.receipt == first.receipt
    assert len(retry.state.committed_transitions) == 1

    locations = _actor_locations(
        retry.state.representation
    )

    assert len(locations) == 1
    assert locations[0].object_entity_id == P2


def test_materially_changed_command_with_same_id_is_not_retry():
    state = _state()
    original = _command()

    first = execute_persistent_world_movement(
        state=state,
        command=original,
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    changed = _command(
        command_id=original.command_id,
        destination=P3,
    )

    with pytest.raises(
        PersistentWorldMovementRetryConflictError
    ):
        execute_persistent_world_movement(
            state=first.state,
            command=changed,
            spatial_evidence=_spatial(
                source=P2,
                destination=P3,
            ),
            opportunity_evidence=_opportunity(
                destination=P3
            ),
            expected_pre_state_digest=(
                _digest(first.state)
            ),
        )

    assert _actor_locations(
        first.state.representation
    )[0].object_entity_id == P2


def test_non_movement_command_is_rejected():
    state = _state()

    with pytest.raises(
        UnsupportedPersistentWorldMovementCommandError
    ):
        execute_persistent_world_movement(
            state=state,
            command=_command(
                command_type="inspect"
            ),
            spatial_evidence=_spatial(),
            opportunity_evidence=_opportunity(),
            expected_pre_state_digest=_digest(state),
        )


def test_bounded_replay_reproduces_committed_post_state():
    state = _state()

    committed = execute_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    replayed = replay_persistent_world_movement(
        pre_state_representation=(
            state.representation
        ),
        receipt=committed.receipt,
    )

    assert (
        digest_persistent_world_entity_location_representation(
            replayed
        )
        == committed.receipt.post_state_digest
    )

    assert replayed == (
        committed.state.representation
    )


def test_replay_wrong_pre_state_fails_closed():
    state = _state()

    committed = execute_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    with pytest.raises(
        PersistentWorldMovementReplayError
    ):
        replay_persistent_world_movement(
            pre_state_representation=(
                committed.state.representation
            ),
            receipt=committed.receipt,
        )


def test_replay_api_requires_no_command_or_model_interpretation():
    parameters = inspect.signature(
        replay_persistent_world_movement
    ).parameters

    assert set(parameters) == {
        "pre_state_representation",
        "receipt",
    }


def test_narration_has_no_authority_over_committed_location():
    state = _state()

    committed = execute_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    contradictory_narration = (
        "The traveler remained at the market square."
    )

    assert contradictory_narration
    assert _actor_locations(
        committed.state.representation
    )[0].object_entity_id == P2


def test_runtime_state_is_immutable():
    state = _state()

    with pytest.raises(FrozenInstanceError):
        state.representation = _representation()


def test_receipt_serialization_is_canonical_and_repeatable():
    state = _state()

    committed = execute_persistent_world_movement(
        state=state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=_digest(state),
    )

    outputs = {
        canonical_serialize_persistent_world_movement_commit_receipt(
            committed.receipt
        )
        for _ in range(100)
    }

    assert len(outputs) == 1


def test_preparation_is_deterministic_across_representation_order():
    first_representation = _representation()

    second_representation = (
        create_persistent_world_entity_location_representation(
            campaign_id=(
                first_representation.campaign_id
            ),
            entities=tuple(
                reversed(
                    first_representation.entities
                )
            ),
            relations=tuple(
                reversed(
                    first_representation.relations
                )
            ),
        )
    )

    first_state = _state(
        first_representation
    )
    second_state = _state(
        second_representation
    )

    assert _digest(first_state) == _digest(
        second_state
    )

    first = prepare_persistent_world_movement(
        state=first_state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=(
            _digest(first_state)
        ),
    )

    second = prepare_persistent_world_movement(
        state=second_state,
        command=_command(),
        spatial_evidence=_spatial(),
        opportunity_evidence=_opportunity(),
        expected_pre_state_digest=(
            _digest(second_state)
        ),
    )

    assert first.pre_state_digest == (
        second.pre_state_digest
    )
    assert first.post_state_digest == (
        second.post_state_digest
    )
    assert first.preview == second.preview
    assert first.state_delta == second.state_delta


def test_module_has_no_forbidden_runtime_dependencies():
    tree = ast.parse(
        SOURCE.read_text(encoding="utf-8")
    )

    imported_modules = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(
                alias.name
                for alias in node.names
            )
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module
        ):
            imported_modules.add(node.module)

    forbidden_fragments = {
        "random",
        "requests",
        "httpx",
        "urllib",
        "socket",
        "sqlite3",
        "openai",
        "anthropic",
        "tiny_vertical_slice",
        "object_lever",
        "state_store",
        "event_commitment",
    }

    for imported in imported_modules:
        assert not any(
            fragment in imported
            for fragment in forbidden_fragments
        )

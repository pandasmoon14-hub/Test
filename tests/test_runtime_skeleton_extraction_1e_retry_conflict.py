from __future__ import annotations

import pytest

from astra_runtime.domain.persistent_world_actor_object_handoff import (
    PersistentWorldActorObjectHandoffRetryConflictError,
    execute_persistent_world_actor_object_handoff,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementRetryConflictError,
    execute_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyRetryConflictError,
    execute_persistent_world_object_custody,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    PersistentWorldObjectDisplacementRetryConflictError,
    execute_persistent_world_object_displacement,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    PersistentWorldObjectLitStateRetryConflictError,
    execute_persistent_world_object_lit_state,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenCloseRetryConflictError,
    execute_persistent_world_object_open_close,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    PersistentWorldObjectStorageRetryConflictError,
    execute_persistent_world_object_storage,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    PLAYER_ID,
    TOOL_CHEST_ID,
)


def _changed_metadata(command):
    return create_command_envelope(
        command_id=command.command_id,
        command_type=command.command_type,
        source_actor_id=command.source_actor_id,
        payload=dict(command.payload),
        metadata={"client": "runtime-skeleton-extraction-1e-conflict"},
    )


def _assert_retry(first, retry) -> None:
    assert retry.technical_retry is True
    assert retry.state == first.state
    assert retry.receipt == first.receipt
    assert retry.preview == first.preview
    assert retry.state_delta == first.state_delta


def test_movement_cutover_preserves_retry_and_conflict_family() -> None:
    app = MyravantPlayApplication.new()
    source = app.current_place_id()
    destination = app.fixture.destination_for(source_place_id=source, direction="south")
    command = create_command_envelope(
        command_id="skeleton-1e-movement-001",
        command_type="move",
        source_actor_id=PLAYER_ID,
        payload={"destination_entity_id": destination},
        metadata={"client": "runtime-skeleton-extraction-1e"},
    )
    spatial, opportunity = app.fixture.movement_evidence(
        command_id=command.command_id,
        source_place_id=source,
        direction="south",
        destination_place_id=destination,
    )
    pre_digest = app.representation_digest()
    first = execute_persistent_world_movement(
        state=app.state,
        command=command,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    retry = execute_persistent_world_movement(
        state=first.state,
        command=command,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_retry(first, retry)
    with pytest.raises(PersistentWorldMovementRetryConflictError):
        execute_persistent_world_movement(
            state=first.state,
            command=_changed_metadata(command),
            spatial_evidence=spatial,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=pre_digest,
        )


def test_custody_cutover_preserves_retry_and_conflict_family() -> None:
    app = MyravantPlayApplication.new()
    command = create_command_envelope(
        command_id="skeleton-1e-custody-001",
        command_type="pickup_object",
        source_actor_id=PLAYER_ID,
        payload={"object_entity_id": LANTERN_ID},
        metadata={"client": "runtime-skeleton-extraction-1e"},
    )
    observation = app.visual_observation_evidence(LANTERN_ID)
    qualification, opportunity = app.fixture.custody_evidence(
        command_id=command.command_id,
        object_entity_id=LANTERN_ID,
        operation="pickup",
        pickup_observation_evidence=observation,
    )
    pre_digest = app.representation_digest()
    first = execute_persistent_world_object_custody(
        state=app.custody_state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    retry = execute_persistent_world_object_custody(
        state=first.state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_retry(first, retry)
    with pytest.raises(PersistentWorldObjectCustodyRetryConflictError):
        execute_persistent_world_object_custody(
            state=first.state,
            command=_changed_metadata(command),
            qualification_evidence=qualification,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=pre_digest,
        )


def test_open_close_cutover_preserves_retry_and_conflict_family() -> None:
    app = MyravantPlayApplication.new()
    assert app.move("south").authoritative_changed
    command = create_command_envelope(
        command_id="skeleton-1e-open-close-001",
        command_type="open_object",
        source_actor_id=PLAYER_ID,
        payload={"object_entity_id": TOOL_CHEST_ID},
        metadata={"client": "runtime-skeleton-extraction-1e"},
    )
    qualification, opportunity = app.fixture.object_open_close_evidence(
        command_id=command.command_id,
        object_entity_id=TOOL_CHEST_ID,
        operation="open",
    )
    pre_digest = app.object_state_digest()
    first = execute_persistent_world_object_open_close(
        state=app.object_state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    retry = execute_persistent_world_object_open_close(
        state=first.state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_retry(first, retry)
    with pytest.raises(PersistentWorldObjectOpenCloseRetryConflictError):
        execute_persistent_world_object_open_close(
            state=first.state,
            command=_changed_metadata(command),
            qualification_evidence=qualification,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=pre_digest,
        )


def test_lit_state_cutover_preserves_retry_and_conflict_family() -> None:
    app = MyravantPlayApplication.new()
    command = create_command_envelope(
        command_id="skeleton-1e-lit-001",
        command_type="activate_object_lit_state",
        source_actor_id=PLAYER_ID,
        payload={"object_entity_id": LANTERN_ID, "operation": "light"},
        metadata={"client": "runtime-skeleton-extraction-1e"},
    )
    qualification, opportunity = app.fixture.object_lit_state_evidence(
        command_id=command.command_id,
        object_entity_id=LANTERN_ID,
        operation="light",
    )
    pre_digest = app.object_lit_state_digest()
    first = execute_persistent_world_object_lit_state(
        state=app.lit_state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    retry = execute_persistent_world_object_lit_state(
        state=first.state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_retry(first, retry)
    with pytest.raises(PersistentWorldObjectLitStateRetryConflictError):
        execute_persistent_world_object_lit_state(
            state=first.state,
            command=_changed_metadata(command),
            qualification_evidence=qualification,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=pre_digest,
        )


def _storage_ready_app() -> MyravantPlayApplication:
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.open_object("chest").authoritative_changed
    return app


def test_storage_cutover_preserves_retry_and_conflict_family() -> None:
    app = _storage_ready_app()
    command = create_command_envelope(
        command_id="skeleton-1e-storage-001",
        command_type="transfer_to_container",
        source_actor_id=PLAYER_ID,
        payload={
            "object_entity_id": LANTERN_ID,
            "container_entity_id": TOOL_CHEST_ID,
        },
        metadata={"client": "runtime-skeleton-extraction-1e"},
    )
    qualification, opportunity = app.fixture.object_storage_evidence(
        command_id=command.command_id,
        object_entity_id=LANTERN_ID,
        container_entity_id=TOOL_CHEST_ID,
        operation="store",
    )
    pre_digest = app.representation_digest()
    first = execute_persistent_world_object_storage(
        state=app.storage_state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    retry = execute_persistent_world_object_storage(
        state=first.state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_retry(first, retry)
    with pytest.raises(PersistentWorldObjectStorageRetryConflictError):
        execute_persistent_world_object_storage(
            state=first.state,
            command=_changed_metadata(command),
            qualification_evidence=qualification,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=pre_digest,
        )


def test_displacement_cutover_preserves_retry_and_conflict_family() -> None:
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    source = app.current_place_id()
    destination = app.fixture.object_displacement_destination_for(
        object_entity_id=LANTERN_ID,
        source_place_id=source,
        direction="east",
        method="throw",
    )
    command = create_command_envelope(
        command_id="skeleton-1e-displacement-001",
        command_type="transfer_object",
        source_actor_id=PLAYER_ID,
        payload={
            "object_entity_id": LANTERN_ID,
            "destination_entity_id": destination,
            "method": "throw",
        },
        metadata={"client": "runtime-skeleton-extraction-1e"},
    )
    qualification, spatial, opportunity = app.fixture.object_displacement_evidence(
        command_id=command.command_id,
        object_entity_id=LANTERN_ID,
        source_place_id=source,
        direction="east",
        destination_place_id=destination,
        method="throw",
    )
    pre_digest = app.representation_digest()
    first = execute_persistent_world_object_displacement(
        state=app.displacement_state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    retry = execute_persistent_world_object_displacement(
        state=first.state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_retry(first, retry)
    with pytest.raises(PersistentWorldObjectDisplacementRetryConflictError):
        execute_persistent_world_object_displacement(
            state=first.state,
            command=_changed_metadata(command),
            qualification_evidence=qualification,
            spatial_evidence=spatial,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=pre_digest,
        )


def test_handoff_cutover_preserves_retry_and_conflict_family() -> None:
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.wait().authoritative_changed
    place_id = app.current_place_id()
    assert app.entity_place_id(GROUNDSKEEPER_ID) == place_id
    command = create_command_envelope(
        command_id="skeleton-1e-handoff-001",
        command_type="transfer_object",
        source_actor_id=PLAYER_ID,
        payload={
            "object_entity_id": LANTERN_ID,
            "recipient_actor_entity_id": GROUNDSKEEPER_ID,
            "method": "handoff",
        },
        metadata={"client": "runtime-skeleton-extraction-1e"},
    )
    qualification, spatial, opportunity = app.fixture.actor_object_handoff_evidence(
        command_id=command.command_id,
        object_entity_id=LANTERN_ID,
        source_actor_entity_id=PLAYER_ID,
        recipient_actor_entity_id=GROUNDSKEEPER_ID,
        place_id=place_id,
        method="handoff",
    )
    pre_digest = app.representation_digest()
    first = execute_persistent_world_actor_object_handoff(
        state=app.handoff_state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    retry = execute_persistent_world_actor_object_handoff(
        state=first.state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_retry(first, retry)
    with pytest.raises(PersistentWorldActorObjectHandoffRetryConflictError):
        execute_persistent_world_actor_object_handoff(
            state=first.state,
            command=_changed_metadata(command),
            qualification_evidence=qualification,
            spatial_evidence=spatial,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=pre_digest,
        )

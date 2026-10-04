from __future__ import annotations

from astra_runtime.domain._deterministic_transition_support import (
    replay_capability_transition,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    execute_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    execute_persistent_world_object_open_close,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    execute_persistent_world_object_lit_state,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    execute_persistent_world_object_storage,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    execute_persistent_world_object_displacement,
)
from astra_runtime.domain.persistent_world_actor_object_handoff import (
    execute_persistent_world_actor_object_handoff,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    PLAYER_ID,
    TOOL_CHEST_ID,
)
from astra_runtime.runtime_skeleton_existing_family_adapters import (
    DISPLACEMENT_TRANSITION_CAPABILITY_SPEC,
    HANDOFF_TRANSITION_CAPABILITY_SPEC,
    LIT_TRANSITION_CAPABILITY_SPEC,
    MOVEMENT_TRANSITION_CAPABILITY_SPEC,
    OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
    STORAGE_TRANSITION_CAPABILITY_SPEC,
    execute_displacement_via_transition_kernel,
    execute_handoff_via_transition_kernel,
    execute_lit_via_transition_kernel,
    execute_movement_via_transition_kernel,
    execute_open_close_via_transition_kernel,
    execute_storage_via_transition_kernel,
)


def _assert_exact_result_equivalence(direct, via_kernel) -> None:
    assert via_kernel == direct
    assert via_kernel.state == direct.state
    assert via_kernel.receipt == direct.receipt
    assert via_kernel.preview == direct.preview
    assert via_kernel.state_delta == direct.state_delta
    assert via_kernel.technical_retry is direct.technical_retry


def test_movement_family_exact_execution_and_replay_equivalence() -> None:
    app = MyravantPlayApplication.new()
    source = app.current_place_id()
    destination = app.fixture.destination_for(
        source_place_id=source,
        direction="south",
    )
    command = create_command_envelope(
        command_id="skeleton-movement-equivalence-001",
        command_type="move",
        source_actor_id=PLAYER_ID,
        payload={"destination_entity_id": destination},
        metadata={"client": "runtime-skeleton-extraction-1d"},
    )
    spatial, opportunity = app.fixture.movement_evidence(
        command_id=command.command_id,
        source_place_id=source,
        direction="south",
        destination_place_id=destination,
    )
    pre_state = app.state
    pre_digest = app.representation_digest()
    direct = execute_persistent_world_movement(
        state=pre_state,
        command=command,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    via_kernel = execute_movement_via_transition_kernel(
        state=pre_state,
        command=command,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_exact_result_equivalence(direct, via_kernel)
    assert replay_capability_transition(
        spec=MOVEMENT_TRANSITION_CAPABILITY_SPEC,
        pre_state=pre_state.representation,
        receipt=via_kernel.receipt,
    ) == via_kernel.state.representation


def test_open_close_family_exact_execution_and_replay_equivalence() -> None:
    app = MyravantPlayApplication.new()
    assert app.move("south").authoritative_changed
    command = create_command_envelope(
        command_id="skeleton-open-equivalence-001",
        command_type="open_object",
        source_actor_id=PLAYER_ID,
        payload={"object_entity_id": TOOL_CHEST_ID},
        metadata={"client": "runtime-skeleton-extraction-1d"},
    )
    qualification, opportunity = app.fixture.object_open_close_evidence(
        command_id=command.command_id,
        object_entity_id=TOOL_CHEST_ID,
        operation="open",
    )
    pre_state = app.object_state
    pre_digest = app.object_state_digest()
    direct = execute_persistent_world_object_open_close(
        state=pre_state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    via_kernel = execute_open_close_via_transition_kernel(
        state=pre_state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_exact_result_equivalence(direct, via_kernel)
    assert replay_capability_transition(
        spec=OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
        pre_state=pre_state.object_open_states,
        receipt=via_kernel.receipt,
    ) == via_kernel.state.object_open_states


def test_lit_family_exact_execution_and_replay_equivalence() -> None:
    app = MyravantPlayApplication.new()
    command = create_command_envelope(
        command_id="skeleton-lit-equivalence-001",
        command_type="activate_object_lit_state",
        source_actor_id=PLAYER_ID,
        payload={"object_entity_id": LANTERN_ID, "operation": "light"},
        metadata={"client": "runtime-skeleton-extraction-1d"},
    )
    qualification, opportunity = app.fixture.object_lit_state_evidence(
        command_id=command.command_id,
        object_entity_id=LANTERN_ID,
        operation="light",
    )
    pre_state = app.lit_state
    pre_digest = app.object_lit_state_digest()
    direct = execute_persistent_world_object_lit_state(
        state=pre_state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    via_kernel = execute_lit_via_transition_kernel(
        state=pre_state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_exact_result_equivalence(direct, via_kernel)
    assert replay_capability_transition(
        spec=LIT_TRANSITION_CAPABILITY_SPEC,
        pre_state=pre_state.object_lit_states,
        receipt=via_kernel.receipt,
    ) == via_kernel.state.object_lit_states


def _storage_ready_app() -> MyravantPlayApplication:
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.open_object("chest").authoritative_changed
    return app


def test_storage_family_exact_execution_and_replay_equivalence() -> None:
    app = _storage_ready_app()
    command = create_command_envelope(
        command_id="skeleton-storage-equivalence-001",
        command_type="transfer_to_container",
        source_actor_id=PLAYER_ID,
        payload={
            "object_entity_id": LANTERN_ID,
            "container_entity_id": TOOL_CHEST_ID,
        },
        metadata={"client": "runtime-skeleton-extraction-1d"},
    )
    qualification, opportunity = app.fixture.object_storage_evidence(
        command_id=command.command_id,
        object_entity_id=LANTERN_ID,
        container_entity_id=TOOL_CHEST_ID,
        operation="store",
    )
    pre_state = app.storage_state
    pre_representation = pre_state.lit_state.open_close_state.custody_state.movement_state.representation
    pre_digest = app.representation_digest()
    direct = execute_persistent_world_object_storage(
        state=pre_state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    via_kernel = execute_storage_via_transition_kernel(
        state=pre_state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_exact_result_equivalence(direct, via_kernel)
    post_representation = via_kernel.state.lit_state.open_close_state.custody_state.movement_state.representation
    assert replay_capability_transition(
        spec=STORAGE_TRANSITION_CAPABILITY_SPEC,
        pre_state=pre_representation,
        receipt=via_kernel.receipt,
    ) == post_representation


def _displacement_ready_app() -> MyravantPlayApplication:
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    return app


def test_displacement_family_exact_execution_and_replay_equivalence() -> None:
    app = _displacement_ready_app()
    source = app.current_place_id()
    destination = app.fixture.object_displacement_destination_for(
        object_entity_id=LANTERN_ID,
        source_place_id=source,
        direction="east",
        method="throw",
    )
    command = create_command_envelope(
        command_id="skeleton-displacement-equivalence-001",
        command_type="transfer_object",
        source_actor_id=PLAYER_ID,
        payload={
            "object_entity_id": LANTERN_ID,
            "destination_entity_id": destination,
            "method": "throw",
        },
        metadata={"client": "runtime-skeleton-extraction-1d"},
    )
    qualification, spatial, opportunity = app.fixture.object_displacement_evidence(
        command_id=command.command_id,
        object_entity_id=LANTERN_ID,
        source_place_id=source,
        direction="east",
        destination_place_id=destination,
        method="throw",
    )
    pre_state = app.displacement_state
    pre_representation = pre_state.storage_state.lit_state.open_close_state.custody_state.movement_state.representation
    pre_digest = app.representation_digest()
    direct = execute_persistent_world_object_displacement(
        state=pre_state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    via_kernel = execute_displacement_via_transition_kernel(
        state=pre_state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_exact_result_equivalence(direct, via_kernel)
    post_representation = via_kernel.state.storage_state.lit_state.open_close_state.custody_state.movement_state.representation
    assert replay_capability_transition(
        spec=DISPLACEMENT_TRANSITION_CAPABILITY_SPEC,
        pre_state=pre_representation,
        receipt=via_kernel.receipt,
    ) == post_representation


def _handoff_ready_app() -> MyravantPlayApplication:
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    advancement = app.wait()
    assert advancement.authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == app.current_place_id()
    return app


def test_handoff_family_exact_execution_and_replay_equivalence() -> None:
    app = _handoff_ready_app()
    place_id = app.current_place_id()
    command = create_command_envelope(
        command_id="skeleton-handoff-equivalence-001",
        command_type="transfer_object",
        source_actor_id=PLAYER_ID,
        payload={
            "object_entity_id": LANTERN_ID,
            "recipient_actor_entity_id": GROUNDSKEEPER_ID,
            "method": "handoff",
        },
        metadata={"client": "runtime-skeleton-extraction-1d"},
    )
    qualification, spatial, opportunity = app.fixture.actor_object_handoff_evidence(
        command_id=command.command_id,
        object_entity_id=LANTERN_ID,
        source_actor_entity_id=PLAYER_ID,
        recipient_actor_entity_id=GROUNDSKEEPER_ID,
        place_id=place_id,
        method="handoff",
    )
    pre_state = app.handoff_state
    pre_representation = pre_state.displacement_state.storage_state.lit_state.open_close_state.custody_state.movement_state.representation
    pre_digest = app.representation_digest()
    direct = execute_persistent_world_actor_object_handoff(
        state=pre_state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    via_kernel = execute_handoff_via_transition_kernel(
        state=pre_state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    _assert_exact_result_equivalence(direct, via_kernel)
    post_representation = via_kernel.state.displacement_state.storage_state.lit_state.open_close_state.custody_state.movement_state.representation
    assert replay_capability_transition(
        spec=HANDOFF_TRANSITION_CAPABILITY_SPEC,
        pre_state=pre_representation,
        receipt=via_kernel.receipt,
    ) == post_representation


def test_existing_family_specs_preserve_distinct_owner_routes() -> None:
    assert MOVEMENT_TRANSITION_CAPABILITY_SPEC.semantic_owners == (
        "AFQR-02", "AFQR-03", "AFQR-18", "AFQR-19", "AFQR-01"
    )
    assert OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC.semantic_owners == (
        "RT-010", "AFQR-19", "AFQR-01", "AFQR-02"
    )
    assert LIT_TRANSITION_CAPABILITY_SPEC.semantic_owners == (
        "RT-010", "AFQR-19", "AFQR-01", "AFQR-02"
    )
    assert STORAGE_TRANSITION_CAPABILITY_SPEC.semantic_owners == (
        "RT-010", "AFQR-19", "AFQR-01", "AFQR-02"
    )
    assert DISPLACEMENT_TRANSITION_CAPABILITY_SPEC.semantic_owners == (
        "RT-010", "AFQR-18", "AFQR-19", "AFQR-01", "AFQR-02"
    )
    assert HANDOFF_TRANSITION_CAPABILITY_SPEC.semantic_owners == (
        "RT-010", "AFQR-18", "AFQR-19", "AFQR-01", "AFQR-02"
    )

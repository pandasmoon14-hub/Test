from __future__ import annotations

import pytest

from astra_runtime.domain._deterministic_transition_support import (
    commit_prepared_capability_transition,
    prepare_capability_transition,
    replay_capability_transition,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    digest_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyRetryConflictError,
    canonical_serialize_persistent_world_object_custody_commit_receipt,
    commit_prepared_persistent_world_object_custody,
    execute_persistent_world_object_custody,
    prepare_persistent_world_object_custody,
    replay_persistent_world_object_custody,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import LANTERN_ID, PLAYER_ID
from astra_runtime.runtime_skeleton_custody_adapter import (
    CUSTODY_TRANSITION_CAPABILITY_SPEC,
    execute_custody_via_transition_kernel,
)


def _pickup_case(*, payload_object_id: str = LANTERN_ID):
    app = MyravantPlayApplication.new()
    command_id = "skeleton-custody-pilot-001"
    command = create_command_envelope(
        command_id=command_id,
        command_type="pickup_object",
        source_actor_id=PLAYER_ID,
        payload={"object_entity_id": payload_object_id},
        metadata={"client": "runtime-skeleton-extraction-1c"},
    )
    observation = app.visual_observation_evidence(LANTERN_ID)
    qualification, opportunity = app.fixture.custody_evidence(
        command_id=command_id,
        object_entity_id=LANTERN_ID,
        operation="pickup",
        pickup_observation_evidence=observation,
    )
    return (
        app.custody_state,
        command,
        qualification,
        opportunity,
        app.representation_digest(),
    )


def test_custody_kernel_success_is_exactly_equivalent_to_existing_executor() -> None:
    state, command, qualification, opportunity, pre_digest = _pickup_case()

    direct = execute_persistent_world_object_custody(
        state=state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    via_kernel = execute_custody_via_transition_kernel(
        state=state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )

    assert via_kernel == direct
    assert via_kernel.state == direct.state
    assert via_kernel.receipt == direct.receipt
    assert via_kernel.preview == direct.preview
    assert via_kernel.state_delta == direct.state_delta
    assert via_kernel.technical_retry is direct.technical_retry is False
    assert (
        canonical_serialize_persistent_world_object_custody_commit_receipt(
            via_kernel.receipt
        )
        == canonical_serialize_persistent_world_object_custody_commit_receipt(
            direct.receipt
        )
    )
    assert digest_persistent_world_entity_location_representation(
        via_kernel.state.movement_state.representation
    ) == digest_persistent_world_entity_location_representation(
        direct.state.movement_state.representation
    )


def test_custody_kernel_prepare_and_commit_match_existing_path_exactly() -> None:
    state, command, qualification, opportunity, pre_digest = _pickup_case()

    direct_prepared = prepare_persistent_world_object_custody(
        state=state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    kernel_prepared = prepare_capability_transition(
        spec=CUSTODY_TRANSITION_CAPABILITY_SPEC,
        state=state,
        command=command,
        context={
            "qualification_evidence": qualification,
            "opportunity_evidence": opportunity,
            "expected_pre_state_digest": pre_digest,
        },
    )
    assert kernel_prepared == direct_prepared

    direct = commit_prepared_persistent_world_object_custody(
        state=state,
        prepared=direct_prepared,
    )
    via_kernel = commit_prepared_capability_transition(
        spec=CUSTODY_TRANSITION_CAPABILITY_SPEC,
        state=state,
        prepared=kernel_prepared,
    )
    assert via_kernel == direct


def test_custody_kernel_retry_preserves_exact_existing_receipt_and_state() -> None:
    state, command, qualification, opportunity, pre_digest = _pickup_case()
    first = execute_persistent_world_object_custody(
        state=state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )

    direct_retry = execute_persistent_world_object_custody(
        state=first.state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    kernel_retry = execute_custody_via_transition_kernel(
        state=first.state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )

    assert kernel_retry == direct_retry
    assert kernel_retry.state is first.state
    assert kernel_retry.receipt == first.receipt
    assert kernel_retry.preview == first.preview
    assert kernel_retry.state_delta == first.state_delta
    assert kernel_retry.technical_retry is True


def test_custody_kernel_conflicting_command_identity_uses_existing_error_family() -> None:
    state, command, qualification, opportunity, pre_digest = _pickup_case()
    first = execute_persistent_world_object_custody(
        state=state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    conflicting = create_command_envelope(
        command_id=command.command_id,
        command_type="drop_object",
        source_actor_id=PLAYER_ID,
        payload={"object_entity_id": LANTERN_ID},
        metadata={"client": "runtime-skeleton-extraction-1c"},
    )

    with pytest.raises(PersistentWorldObjectCustodyRetryConflictError):
        execute_persistent_world_object_custody(
            state=first.state,
            command=conflicting,
            qualification_evidence=qualification,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=pre_digest,
        )
    with pytest.raises(PersistentWorldObjectCustodyRetryConflictError):
        execute_custody_via_transition_kernel(
            state=first.state,
            command=conflicting,
            qualification_evidence=qualification,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=pre_digest,
        )


def test_custody_kernel_replay_is_exact_existing_reducer_delegation() -> None:
    state, command, qualification, opportunity, pre_digest = _pickup_case()
    result = execute_persistent_world_object_custody(
        state=state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=pre_digest,
    )
    pre_representation = state.movement_state.representation

    direct = replay_persistent_world_object_custody(
        pre_state_representation=pre_representation,
        receipt=result.receipt,
    )
    via_kernel = replay_capability_transition(
        spec=CUSTODY_TRANSITION_CAPABILITY_SPEC,
        pre_state=pre_representation,
        receipt=result.receipt,
    )

    assert via_kernel == direct
    assert via_kernel == result.state.movement_state.representation


def test_custody_spec_preserves_existing_owner_routes_without_super_owner() -> None:
    assert CUSTODY_TRANSITION_CAPABILITY_SPEC.semantic_owners == (
        "RT-010",
        "AFQR-19",
        "AFQR-01",
        "AFQR-18",
        "AFQR-02",
    )

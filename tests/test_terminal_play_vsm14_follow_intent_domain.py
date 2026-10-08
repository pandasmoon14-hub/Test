from __future__ import annotations

from pathlib import Path

import pytest

import astra_runtime.domain.persistent_world_follow_intent as follow_module
from astra_runtime.domain.persistent_world_follow_intent import (
    AFQR12_FOLLOW_INTENT_OWNER,
    FOLLOW_INTENT_TRANSITION_CAPABILITY_SPEC,
    PersistentWorldFollowIntentRetryConflictError,
    create_follow_intent_opportunity_evidence,
    create_follow_intent_qualification_evidence,
    create_follow_intent_spatial_evidence,
    create_persistent_world_follow_intent_runtime_state,
    digest_persistent_world_follow_intent_runtime_state,
    execute_persistent_world_follow_intent,
    replay_persistent_world_follow_intents,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    PLAYER_ID,
)


def _evidence(operation: str):
    return (
        create_follow_intent_qualification_evidence(
            evidence_id=build_record_id("evidence", f"vsm14-domain-{operation}-afqr12"),
            follower_entity_id=GROUNDSKEEPER_ID,
            leader_entity_id=PLAYER_ID,
            operation=operation,
            qualified=True,
        ),
        create_follow_intent_spatial_evidence(
            evidence_id=build_record_id("evidence", f"vsm14-domain-{operation}-afqr18"),
            follower_entity_id=GROUNDSKEEPER_ID,
            leader_entity_id=PLAYER_ID,
            place_id=GATEHOUSE_ID,
            co_located=True,
        ),
        create_follow_intent_opportunity_evidence(
            evidence_id=build_record_id("evidence", f"vsm14-domain-{operation}-afqr19"),
            follower_entity_id=GROUNDSKEEPER_ID,
            leader_entity_id=PLAYER_ID,
            operation=operation,
            opportunity_available=True,
            resolution_accepted=True,
        ),
    )


def _command(command_id: str, operation: str):
    return create_command_envelope(
        command_id=command_id,
        command_type="behavior_follow_intent",
        source_actor_id=GROUNDSKEEPER_ID,
        payload={
            "leader_entity_id": PLAYER_ID,
            "operation": operation,
        },
        metadata={"package": "VSM-14", "test": True},
    )


def test_follow_intent_uses_extracted_lifecycle_and_exact_retry_identity() -> None:
    state = create_persistent_world_follow_intent_runtime_state()
    qualification, spatial, opportunity = _evidence("activate")
    command = _command("test-vsm14-follow-activate", "activate")

    result = execute_persistent_world_follow_intent(
        state=state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=digest_persistent_world_follow_intent_runtime_state(state),
    )

    assert result.technical_retry is False
    assert len(result.state.active_intents) == 1
    assert result.state.active_intents[0].follower_entity_id == GROUNDSKEEPER_ID
    assert result.state.active_intents[0].leader_entity_id == PLAYER_ID
    assert result.state.active_intents[0].semantic_owner == AFQR12_FOLLOW_INTENT_OWNER

    retry = execute_persistent_world_follow_intent(
        state=result.state,
        command=command,
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest="0" * 64,
    )
    assert retry.technical_retry is True
    assert retry.receipt == result.receipt
    assert retry.preview == result.preview
    assert retry.state_delta == result.state_delta
    assert retry.state == result.state


def test_follow_intent_same_command_id_different_meaning_conflicts() -> None:
    state = create_persistent_world_follow_intent_runtime_state()
    qualification, spatial, opportunity = _evidence("activate")
    committed = execute_persistent_world_follow_intent(
        state=state,
        command=_command("test-vsm14-follow-conflict", "activate"),
        qualification_evidence=qualification,
        spatial_evidence=spatial,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=digest_persistent_world_follow_intent_runtime_state(state),
    )
    deactivate_q, deactivate_s, deactivate_o = _evidence("deactivate")
    with pytest.raises(PersistentWorldFollowIntentRetryConflictError):
        execute_persistent_world_follow_intent(
            state=committed.state,
            command=_command("test-vsm14-follow-conflict", "deactivate"),
            qualification_evidence=deactivate_q,
            spatial_evidence=deactivate_s,
            opportunity_evidence=deactivate_o,
            expected_pre_state_digest=digest_persistent_world_follow_intent_runtime_state(
                committed.state
            ),
        )


def test_follow_intent_activate_deactivate_replays_exactly() -> None:
    initial = create_persistent_world_follow_intent_runtime_state()
    q1, s1, o1 = _evidence("activate")
    activated = execute_persistent_world_follow_intent(
        state=initial,
        command=_command("test-vsm14-follow-on", "activate"),
        qualification_evidence=q1,
        spatial_evidence=s1,
        opportunity_evidence=o1,
        expected_pre_state_digest=digest_persistent_world_follow_intent_runtime_state(initial),
    )
    q2, s2, o2 = _evidence("deactivate")
    deactivated = execute_persistent_world_follow_intent(
        state=activated.state,
        command=_command("test-vsm14-follow-off", "deactivate"),
        qualification_evidence=q2,
        spatial_evidence=s2,
        opportunity_evidence=o2,
        expected_pre_state_digest=digest_persistent_world_follow_intent_runtime_state(
            activated.state
        ),
    )

    assert tuple(
        transition.command_id for transition in deactivated.state.committed_transitions
    ) == ("test-vsm14-follow-on", "test-vsm14-follow-off")

    replayed = replay_persistent_world_follow_intents(
        active_intents=(), receipt=activated.receipt
    )
    replayed = replay_persistent_world_follow_intents(
        active_intents=replayed, receipt=deactivated.receipt
    )
    assert replayed == deactivated.state.active_intents == ()


def test_follow_intent_owner_module_does_not_absorb_movement_or_social_owners() -> None:
    source = Path(follow_module.__file__).read_text(encoding="utf-8")
    assert "persistent_world_movement_integration" not in source
    assert "persistent_world_runtime_composition" not in source
    assert "AFQR-13" not in source
    assert "AFQR-14" not in source
    assert FOLLOW_INTENT_TRANSITION_CAPABILITY_SPEC.semantic_owners == (
        "AFQR-12",
        "AFQR-18",
        "AFQR-19",
        "AFQR-01",
        "AFQR-02",
    )

"""RUNTIME-SKELETON-EXTRACTION-1C custody lifecycle equivalence adapter.

This module wires the already-authoritative R4-E custody capability into the
shared deterministic transition lifecycle shell. It is an extraction-time
adapter only: all custody vocabulary, legality, evidence meaning, state
mutation, receipt construction, stale-state protection, retry conflict type,
and replay semantics remain implemented by
``persistent_world_object_custody_transfer``.

The adapter does not create a custody super-owner and does not change the
production application route in this tranche.
"""

from __future__ import annotations

from typing import Mapping

from astra_runtime.domain._deterministic_transition_support import (
    TransitionCapabilitySpec,
    execute_capability_transition,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    PersistentWorldEntityLocationRepresentation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    digest_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    CustodyOpportunityEvidence,
    CustodyQualificationEvidence,
    PersistentWorldObjectCustodyExecutionResult,
    PersistentWorldObjectCustodyRetryConflictError,
    PersistentWorldObjectCustodyRuntimeState,
    commit_prepared_persistent_world_object_custody,
    fingerprint_persistent_world_object_custody_command,
    prepare_persistent_world_object_custody,
    replay_persistent_world_object_custody,
)
from astra_runtime.kernel.command_envelope import CommandEnvelope


def _custody_state_digest(state: object) -> str:
    if not isinstance(state, PersistentWorldObjectCustodyRuntimeState):
        raise TypeError("custody state type mismatch")
    return digest_persistent_world_entity_location_representation(
        state.movement_state.representation
    )


def _prepare_custody(
    state: object,
    command: CommandEnvelope,
    context: Mapping[str, object],
):
    if not isinstance(state, PersistentWorldObjectCustodyRuntimeState):
        raise TypeError("custody state type mismatch")
    qualification = context.get("qualification_evidence")
    opportunity = context.get("opportunity_evidence")
    expected_pre_state_digest = context.get("expected_pre_state_digest")
    if not isinstance(qualification, CustodyQualificationEvidence):
        raise TypeError("qualification_evidence must be CustodyQualificationEvidence")
    if not isinstance(opportunity, CustodyOpportunityEvidence):
        raise TypeError("opportunity_evidence must be CustodyOpportunityEvidence")
    if not isinstance(expected_pre_state_digest, str):
        raise TypeError("expected_pre_state_digest must be str")
    return prepare_persistent_world_object_custody(
        state=state,
        command=command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=expected_pre_state_digest,
    )


def _commit_custody(state: object, prepared: object):
    if not isinstance(state, PersistentWorldObjectCustodyRuntimeState):
        raise TypeError("custody state type mismatch")
    return commit_prepared_persistent_world_object_custody(
        state=state,
        prepared=prepared,
    )


def _custody_retry_result(state: object, committed: object):
    if not isinstance(state, PersistentWorldObjectCustodyRuntimeState):
        raise TypeError("custody state type mismatch")
    return PersistentWorldObjectCustodyExecutionResult(
        state=state,
        receipt=committed.receipt,
        preview=committed.preview,
        state_delta=committed.state_delta,
        technical_retry=True,
    )


def _replay_custody(pre_state: object, receipt: object):
    if not isinstance(pre_state, PersistentWorldEntityLocationRepresentation):
        raise TypeError("custody replay pre-state type mismatch")
    return replay_persistent_world_object_custody(
        pre_state_representation=pre_state,
        receipt=receipt,
    )


CUSTODY_TRANSITION_CAPABILITY_SPEC = TransitionCapabilitySpec(
    capability_id="persistent_world_object_custody",
    semantic_owners=("RT-010", "AFQR-19", "AFQR-01", "AFQR-18", "AFQR-02"),
    state_type=PersistentWorldObjectCustodyRuntimeState,
    replay_state_type=PersistentWorldEntityLocationRepresentation,
    receipt_prefix="custody_receipt",
    state_digest=_custody_state_digest,
    fingerprint_command=fingerprint_persistent_world_object_custody_command,
    committed_transitions=lambda state: state.committed_custody_transitions,
    prepare_new_transition=_prepare_custody,
    commit_new_transition=_commit_custody,
    build_retry_result=_custody_retry_result,
    retry_conflict_error=lambda message: PersistentWorldObjectCustodyRetryConflictError(
        message
    ),
    replay_committed_transition=_replay_custody,
)


def execute_custody_via_transition_kernel(
    *,
    state: PersistentWorldObjectCustodyRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: CustodyQualificationEvidence,
    opportunity_evidence: CustodyOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectCustodyExecutionResult:
    """Execute R4-E custody through the shared lifecycle shell.

    This function intentionally mirrors the existing executor signature so
    exact equivalence can be tested before any production routing migration.
    """

    result = execute_capability_transition(
        spec=CUSTODY_TRANSITION_CAPABILITY_SPEC,
        state=state,
        command=command,
        context={
            "qualification_evidence": qualification_evidence,
            "opportunity_evidence": opportunity_evidence,
            "expected_pre_state_digest": expected_pre_state_digest,
        },
    )
    if not isinstance(result, PersistentWorldObjectCustodyExecutionResult):
        raise TypeError("custody lifecycle shell returned an invalid result")
    return result

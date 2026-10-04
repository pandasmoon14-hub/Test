"""VSM-9 bounded actor-mediated local object-state operations.

This module proves one narrow reusable semantic thesis:

a player request, fixture-local actor acceptance, actor-attributed INT-2 legality,
and a committed lantern lit-state outcome remain distinct stages.

It intentionally supports only requests for the fixture Groundskeeper to light or
extinguish the fixture Brass Lantern.  It does not create a generic NPC-command,
dialogue, persuasion, obedience, delegation, planning, or social-authority system.

Authoritative lit/unlit mutation remains owned by the existing INT-2 path:
RT-010 qualification, AFQR-19 opportunity, AFQR-01 commitment, and AFQR-02
command identity.  The VSM-9 request receipt is correlation/provenance evidence;
it is not a second authoritative state store.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    CONTAINED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    PersistentWorldObjectLitStateError,
    create_object_lit_state_opportunity_evidence,
    create_object_lit_state_qualification_evidence,
    execute_persistent_world_object_lit_state,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.myravant_play_application import (
    MyravantPlayApplication,
    PlayApplicationResult,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    TOOL_CHEST_ID,
    UnavailableFixtureCustodyError,
    UnavailableFixtureHandoffError,
)


VSM9_PACKAGE_ID = "VSM-9"
VSM9_CAPABILITY = "bounded_actor_mediated_local_object_state_operations"
VSM9_REQUESTER_ROLE = "requester"
VSM9_REQUESTED_ACTOR_ROLE = "requested_actor"
VSM9_PERFORMING_ACTOR_ROLE = "performing_actor"
VSM9_SUPPORTED_OPERATIONS = frozenset({"light", "extinguish"})


@dataclass(frozen=True, kw_only=True)
class ParsedVSM9Request:
    """Non-authoritative interpretation of one bounded actor-mediated request."""

    raw_text: str
    actor_reference: str | None
    operation: str | None
    object_reference: str | None
    parsed: bool
    failure_class: str | None = None


@dataclass(frozen=True, kw_only=True)
class VSM9RequestReceipt:
    """Application-level provenance for the request/acceptance/execution chain."""

    request_id: str
    requester_entity_id: str
    requested_actor_entity_id: str | None
    performing_actor_entity_id: str | None
    target_entity_id: str | None
    requested_operation: str | None
    acceptance: str
    legality_result: str
    authoritative_outcome: str
    command_id: str | None = None
    command_fingerprint: str | None = None
    qualification_evidence_id: str | None = None
    opportunity_evidence_id: str | None = None
    authoritative_receipt_id: str | None = None
    state_delta_id: str | None = None
    pre_state_digest: str | None = None
    post_state_digest: str | None = None


@dataclass(frozen=True, kw_only=True)
class VSM9Execution:
    result: PlayApplicationResult
    request_receipt: VSM9RequestReceipt


def _normalized_words(raw_text: str) -> list[str]:
    return raw_text.strip().casefold().replace("-", " ").split()


def parse_vsm9_request(raw_text: str) -> ParsedVSM9Request:
    """Parse only explicit Groundskeeper + Brass Lantern light-state requests."""

    words = _normalized_words(raw_text)
    if words and words[0] == "i":
        words = words[1:]
    if not words or words[0] != "ask" or "to" not in words[1:]:
        return ParsedVSM9Request(
            raw_text=raw_text,
            actor_reference=None,
            operation=None,
            object_reference=None,
            parsed=False,
            failure_class="vsm9_not_actor_mediated_request",
        )

    to_index = words.index("to", 1)
    actor_words = words[1:to_index]
    if actor_words and actor_words[0] == "the":
        actor_words = actor_words[1:]
    requested = words[to_index + 1 :]
    if not actor_words or len(requested) < 2:
        return ParsedVSM9Request(
            raw_text=raw_text,
            actor_reference=" ".join(actor_words) or None,
            operation=None,
            object_reference=None,
            parsed=False,
            failure_class="vsm9_request_incomplete",
        )

    operation = requested[0]
    if operation == "ignite":
        operation = "light"
    object_words = requested[1:]
    if object_words and object_words[0] == "the":
        object_words = object_words[1:]

    actor_reference = " ".join(actor_words)
    object_reference = " ".join(object_words)
    actor_ok = actor_reference == "groundskeeper"
    object_ok = object_reference in {"lantern", "brass lantern"}
    operation_ok = operation in VSM9_SUPPORTED_OPERATIONS
    if not (actor_ok and object_ok and operation_ok):
        return ParsedVSM9Request(
            raw_text=raw_text,
            actor_reference=actor_reference or None,
            operation=operation or None,
            object_reference=object_reference or None,
            parsed=False,
            failure_class="vsm9_request_outside_bounded_parser",
        )

    return ParsedVSM9Request(
        raw_text=raw_text,
        actor_reference=actor_reference,
        operation=operation,
        object_reference=object_reference,
        parsed=True,
    )


def _request_id(
    *, requester_entity_id: str, raw_text: str, pre_state_digest: str
) -> str:
    token = hashlib.sha256(
        f"{requester_entity_id}|{raw_text.strip()}|{pre_state_digest}".encode("utf-8")
    ).hexdigest()[:24]
    return build_record_id("actor_mediated_request", token)


def _actor_present_with_requester(
    application: MyravantPlayApplication,
    actor_entity_id: str,
) -> bool:
    try:
        return application.entity_place_id(actor_entity_id) == application.current_place_id()
    except Exception:  # fail closed at this application boundary
        return False


def _actor_can_reach_lantern(
    application: MyravantPlayApplication,
    *,
    actor_entity_id: str,
    object_entity_id: str,
) -> bool:
    """Mirror the existing INT-2 placement opportunity without mutating state."""

    representation = application.state.representation
    try:
        actor_place_id = application.entity_place_id(actor_entity_id)
    except Exception:
        return False

    nearby = any(
        relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
        and relation.object_entity_id == actor_place_id
        for relation in representation.relations
    )
    carried_by_actor = any(
        relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
        and relation.object_entity_id == actor_entity_id
        for relation in representation.relations
    )
    if nearby or carried_by_actor:
        return True

    containment = [
        relation
        for relation in representation.relations
        if relation.relation_type == CONTAINED_BY_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
    ]
    if len(containment) != 1:
        return False

    container_id = containment[0].object_entity_id
    container_nearby = any(
        relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == container_id
        and relation.object_entity_id == actor_place_id
        for relation in representation.relations
    )
    container_carried_by_actor = any(
        relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == container_id
        and relation.object_entity_id == actor_entity_id
        for relation in representation.relations
    )
    open_state = application.object_open_state(container_id)
    return bool(
        (container_nearby or container_carried_by_actor)
        and open_state is not None
        and open_state.state == "open"
    )


def _rejected_execution(
    application: MyravantPlayApplication,
    *,
    request_id: str,
    parsed: ParsedVSM9Request,
    actor_entity_id: str | None,
    target_entity_id: str | None,
    acceptance: str,
    legality_result: str,
    failure_class: str,
    message: str,
) -> VSM9Execution:
    digest = application.authoritative_digest()
    result = PlayApplicationResult(
        result_type="actor_mediated_object_lit_state_rejected",
        message=message,
        authoritative_changed=False,
        pre_state_digest=digest,
        post_state_digest=digest,
        failure_class=failure_class,
    )
    return VSM9Execution(
        result=result,
        request_receipt=VSM9RequestReceipt(
            request_id=request_id,
            requester_entity_id=application.fixture.player_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=None,
            target_entity_id=target_entity_id,
            requested_operation=parsed.operation,
            acceptance=acceptance,
            legality_result=legality_result,
            authoritative_outcome="no_commit",
            pre_state_digest=digest,
            post_state_digest=digest,
        ),
    )


def execute_vsm9_request(
    application: MyravantPlayApplication,
    raw_text: str,
) -> VSM9Execution:
    """Execute one bounded request without letting the request itself mutate state."""

    pre_digest = application.authoritative_digest()
    parsed = parse_vsm9_request(raw_text)
    request_id = _request_id(
        requester_entity_id=application.fixture.player_entity_id,
        raw_text=raw_text,
        pre_state_digest=pre_digest,
    )
    if not parsed.parsed:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=None,
            target_entity_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class=parsed.failure_class or "vsm9_request_unavailable",
            message="That actor-mediated request is outside the bounded VSM-9 route.",
        )

    try:
        actor_entity_id = application.fixture.resolve_actor_reference(
            parsed.actor_reference or ""
        )
    except UnavailableFixtureHandoffError:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=None,
            target_entity_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class="vsm9_requested_actor_unavailable",
            message="The requested actor is not available.",
        )

    try:
        object_entity_id = application.fixture.resolve_object_reference(
            parsed.object_reference or ""
        )
    except UnavailableFixtureCustodyError:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class="vsm9_target_unavailable",
            message="The requested target is not available.",
        )

    if actor_entity_id != GROUNDSKEEPER_ID or object_entity_id != LANTERN_ID:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm9_fixture_acceptance_refused",
            message="The Groundskeeper does not accept that bounded request.",
        )

    if not _actor_present_with_requester(application, actor_entity_id):
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm9_requested_actor_not_local",
            message="The Groundskeeper is not here to receive that request.",
        )

    # Fixture-local acceptance authorizes only an attempted actor-attributed
    # execution.  It does not itself change the lantern or guarantee legality.
    acceptance = "accepted"
    opportunity_available = _actor_can_reach_lantern(
        application,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
    )

    current = application.object_lit_state(object_entity_id)
    desired = "lit" if parsed.operation == "light" else "unlit"
    if current is None:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm9_lit_state_not_supported",
            message="The requested target has no bounded lit-state operation.",
        )

    if not opportunity_available:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm9_int2_opportunity_unavailable",
            message="The Groundskeeper accepts, but cannot currently reach the Brass Lantern.",
        )

    if current.state == desired:
        result = PlayApplicationResult(
            result_type="actor_mediated_object_lit_state_unchanged",
            message=f"The Brass Lantern is already {desired}.",
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=pre_digest,
        )
        return VSM9Execution(
            result=result,
            request_receipt=VSM9RequestReceipt(
                request_id=request_id,
                requester_entity_id=application.fixture.player_entity_id,
                requested_actor_entity_id=actor_entity_id,
                performing_actor_entity_id=actor_entity_id,
                target_entity_id=object_entity_id,
                requested_operation=parsed.operation,
                acceptance=acceptance,
                legality_result="allowed_no_change",
                authoritative_outcome="unchanged",
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            ),
        )

    command_id = application._next_object_lit_state_command_id()
    command = create_command_envelope(
        command_id=command_id,
        command_type="activate_object_lit_state",
        source_actor_id=actor_entity_id,
        payload={
            "object_entity_id": object_entity_id,
            "operation": parsed.operation,
        },
        metadata={
            "client": "myravant-terminal-vsm9",
            "request_id": request_id,
            "requester_entity_id": application.fixture.player_entity_id,
            "requested_actor_entity_id": actor_entity_id,
        },
    )
    token = hashlib.sha256(
        f"{request_id}|{command_id}|{actor_entity_id}|{object_entity_id}|{parsed.operation}".encode(
            "utf-8"
        )
    ).hexdigest()[:20]
    qualification = create_object_lit_state_qualification_evidence(
        evidence_id=build_record_id("evidence", f"vsm9-{token}-rt010"),
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=parsed.operation or "",
        qualified=True,
    )
    opportunity = create_object_lit_state_opportunity_evidence(
        evidence_id=build_record_id("evidence", f"vsm9-{token}-afqr19"),
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=parsed.operation or "",
        opportunity_available=True,
        resolution_accepted=True,
    )

    try:
        committed = execute_persistent_world_object_lit_state(
            state=application.lit_state,
            command=command,
            qualification_evidence=qualification,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=application.object_lit_state_digest(),
        )
    except PersistentWorldObjectLitStateError as exc:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class=type(exc).__name__,
            message="The accepted request was rejected by authoritative INT-2 legality.",
        )

    application._lit_state = committed.state
    post_digest = application.authoritative_digest()
    verb = "lights" if parsed.operation == "light" else "extinguishes"
    result = PlayApplicationResult(
        result_type="actor_mediated_object_lit_state_committed",
        message=f"The Groundskeeper {verb} the Brass Lantern.",
        authoritative_changed=True,
        command_id=command_id,
        command_fingerprint=committed.receipt.command_fingerprint,
        preview_id=committed.preview.preview_id,
        receipt_id=committed.receipt.receipt_id,
        state_delta_id=committed.state_delta.delta_id,
        opportunity_evidence_id=committed.receipt.opportunity_evidence_id,
        pre_state_digest=pre_digest,
        post_state_digest=post_digest,
        technical_retry=committed.technical_retry,
    )
    receipt = VSM9RequestReceipt(
        request_id=request_id,
        requester_entity_id=application.fixture.player_entity_id,
        requested_actor_entity_id=actor_entity_id,
        performing_actor_entity_id=committed.receipt.actor_entity_id,
        target_entity_id=committed.receipt.object_entity_id,
        requested_operation=parsed.operation,
        acceptance=acceptance,
        legality_result="allowed",
        authoritative_outcome="committed",
        command_id=command_id,
        command_fingerprint=committed.receipt.command_fingerprint,
        qualification_evidence_id=qualification.evidence_id,
        opportunity_evidence_id=committed.receipt.opportunity_evidence_id,
        authoritative_receipt_id=committed.receipt.receipt_id,
        state_delta_id=committed.state_delta.delta_id,
        pre_state_digest=pre_digest,
        post_state_digest=post_digest,
    )
    return VSM9Execution(result=result, request_receipt=receipt)


def vsm9_legality_snapshot(application: MyravantPlayApplication) -> dict[str, object]:
    """Expose deterministic test evidence for the bounded actor/lantern opportunity."""

    return {
        "requester_entity_id": application.fixture.player_entity_id,
        "requested_actor_entity_id": GROUNDSKEEPER_ID,
        "target_entity_id": LANTERN_ID,
        "actor_local_to_requester": _actor_present_with_requester(
            application, GROUNDSKEEPER_ID
        ),
        "actor_can_reach_target": _actor_can_reach_lantern(
            application,
            actor_entity_id=GROUNDSKEEPER_ID,
            object_entity_id=LANTERN_ID,
        ),
        "lantern_state": (
            application.object_lit_state(LANTERN_ID).state
            if application.object_lit_state(LANTERN_ID) is not None
            else None
        ),
        "container_state": (
            application.object_open_state(TOOL_CHEST_ID).state
            if application.object_open_state(TOOL_CHEST_ID) is not None
            else None
        ),
    }

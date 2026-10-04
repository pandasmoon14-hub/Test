"""VSM-12 bounded actor-mediated local object custody.

A player request, fixture-local actor acceptance, R4-E custody opportunity,
performing actor, and committed pickup/drop outcome remain distinct stages.
Only the fixture Groundskeeper and Brass Lantern are in scope. Authoritative
custody remains owned by the existing R4-E / RT-010 path; this module adds no
new state family, semantic owner, persistence component, ownership semantics,
or generic NPC command system.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyError,
    create_custody_opportunity_evidence,
    create_custody_qualification_evidence,
    execute_persistent_world_object_custody,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    replace_persistent_world_runtime_custody_state,
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
    UnavailableFixtureCustodyError,
    UnavailableFixtureHandoffError,
)

VSM12_PACKAGE_ID = "VSM-12"
VSM12_CAPABILITY = "bounded_actor_mediated_local_object_custody"
VSM12_SUPPORTED_OPERATIONS = frozenset({"pickup", "drop"})


@dataclass(frozen=True, kw_only=True)
class ParsedVSM12Request:
    raw_text: str
    actor_reference: str | None
    operation: str | None
    object_reference: str | None
    parsed: bool
    failure_class: str | None = None


@dataclass(frozen=True, kw_only=True)
class VSM12RequestReceipt:
    request_id: str
    requester_entity_id: str
    requested_actor_entity_id: str | None
    performing_actor_entity_id: str | None
    target_entity_id: str | None
    requested_operation: str | None
    place_id: str | None
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
class VSM12Execution:
    result: PlayApplicationResult
    request_receipt: VSM12RequestReceipt


def _normalized_words(raw_text: str) -> list[str]:
    return raw_text.strip().casefold().replace("-", " ").split()


def parse_vsm12_request(raw_text: str) -> ParsedVSM12Request:
    """Parse only explicit Groundskeeper/Lantern immediate-custody requests."""

    words = _normalized_words(raw_text)
    if words and words[0] == "i":
        words = words[1:]
    if not words or words[0] != "ask" or "to" not in words[1:]:
        return ParsedVSM12Request(
            raw_text=raw_text,
            actor_reference=None,
            operation=None,
            object_reference=None,
            parsed=False,
            failure_class="vsm12_not_actor_mediated_request",
        )

    to_index = words.index("to", 1)
    actor_words = words[1:to_index]
    if actor_words and actor_words[0] == "the":
        actor_words = actor_words[1:]
    actor_reference = " ".join(actor_words)
    requested = words[to_index + 1 :]

    operation: str | None = None
    object_words: list[str] = []
    if requested[:2] == ["pick", "up"]:
        operation = "pickup"
        object_words = requested[2:]
    elif requested and requested[0] == "pickup":
        operation = "pickup"
        object_words = requested[1:]
    elif requested and requested[0] == "drop":
        operation = "drop"
        object_words = requested[1:]

    if object_words and object_words[0] == "the":
        object_words = object_words[1:]
    object_reference = " ".join(object_words)

    if (
        actor_reference != "groundskeeper"
        or operation not in VSM12_SUPPORTED_OPERATIONS
        or object_reference not in {"lantern", "brass lantern"}
    ):
        return ParsedVSM12Request(
            raw_text=raw_text,
            actor_reference=actor_reference or None,
            operation=operation,
            object_reference=object_reference or None,
            parsed=False,
            failure_class="vsm12_request_outside_bounded_parser",
        )

    return ParsedVSM12Request(
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
    return build_record_id("actor_mediated_custody_request", token)


def _actor_local(
    application: MyravantPlayApplication,
    actor_entity_id: str,
) -> bool:
    try:
        return application.entity_place_id(actor_entity_id) == application.current_place_id()
    except Exception:
        return False


def _custody_opportunity(
    application: MyravantPlayApplication,
    *,
    actor_entity_id: str,
    object_entity_id: str,
    operation: str,
) -> bool:
    """Mirror existing R4-E placement preconditions without mutating state."""

    try:
        actor_place_id = application.entity_place_id(actor_entity_id)
    except Exception:
        return False
    direct = [
        relation
        for relation in application.state.representation.relations
        if relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
    ]
    carried = [
        relation
        for relation in application.state.representation.relations
        if relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
    ]
    if len(direct) > 1 or len(carried) > 1 or (direct and carried):
        return False
    if operation == "pickup":
        return (
            len(direct) == 1
            and not carried
            and direct[0].object_entity_id == actor_place_id
        )
    if operation == "drop":
        return (
            len(carried) == 1
            and not direct
            and carried[0].object_entity_id == actor_entity_id
        )
    return False


def _owner_evidence(
    *,
    request_id: str,
    actor_entity_id: str,
    object_entity_id: str,
    operation: str,
    opportunity_available: bool,
):
    token = hashlib.sha256(
        (
            f"{request_id}|{actor_entity_id}|{object_entity_id}|"
            f"{operation}|{int(opportunity_available)}"
        ).encode("utf-8")
    ).hexdigest()[:20]
    qualification = create_custody_qualification_evidence(
        evidence_id=build_record_id("evidence", f"vsm12-{token}-rt010"),
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
        qualified=True,
    )
    opportunity = create_custody_opportunity_evidence(
        evidence_id=build_record_id("evidence", f"vsm12-{token}-afqr19"),
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
        opportunity_available=opportunity_available,
        resolution_accepted=True,
    )
    return qualification, opportunity


def _rejected(
    application: MyravantPlayApplication,
    *,
    request_id: str,
    parsed: ParsedVSM12Request,
    actor_entity_id: str | None,
    target_entity_id: str | None,
    place_id: str | None,
    acceptance: str,
    legality_result: str,
    failure_class: str,
    message: str,
    command_id: str | None = None,
    qualification_evidence_id: str | None = None,
    opportunity_evidence_id: str | None = None,
) -> VSM12Execution:
    digest = application.authoritative_digest()
    return VSM12Execution(
        result=PlayApplicationResult(
            result_type="actor_mediated_custody_rejected",
            message=message,
            authoritative_changed=False,
            command_id=command_id,
            opportunity_evidence_id=opportunity_evidence_id,
            pre_state_digest=digest,
            post_state_digest=digest,
            failure_class=failure_class,
        ),
        request_receipt=VSM12RequestReceipt(
            request_id=request_id,
            requester_entity_id=application.fixture.player_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=None,
            target_entity_id=target_entity_id,
            requested_operation=parsed.operation,
            place_id=place_id,
            acceptance=acceptance,
            legality_result=legality_result,
            authoritative_outcome="no_commit",
            command_id=command_id,
            qualification_evidence_id=qualification_evidence_id,
            opportunity_evidence_id=opportunity_evidence_id,
            pre_state_digest=digest,
            post_state_digest=digest,
        ),
    )


def execute_vsm12_request(
    application: MyravantPlayApplication,
    raw_text: str,
) -> VSM12Execution:
    """Execute one bounded request through the existing R4-E custody owner."""

    pre_digest = application.authoritative_digest()
    parsed = parse_vsm12_request(raw_text)
    request_id = _request_id(
        requester_entity_id=application.fixture.player_entity_id,
        raw_text=raw_text,
        pre_state_digest=pre_digest,
    )
    if not parsed.parsed:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=None,
            target_entity_id=None,
            place_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class=parsed.failure_class or "vsm12_request_unavailable",
            message="That actor-mediated custody request is outside the bounded VSM-12 route.",
        )

    try:
        actor_entity_id = application.fixture.resolve_actor_reference(
            parsed.actor_reference or ""
        )
    except UnavailableFixtureHandoffError:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=None,
            target_entity_id=None,
            place_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class="vsm12_requested_actor_unavailable",
            message="The requested actor is not available.",
        )
    try:
        object_entity_id = application.fixture.resolve_object_reference(
            parsed.object_reference or ""
        )
    except UnavailableFixtureCustodyError:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=None,
            place_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class="vsm12_target_unavailable",
            message="The requested target is not available.",
        )

    if actor_entity_id != GROUNDSKEEPER_ID or object_entity_id != LANTERN_ID:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            place_id=None,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm12_fixture_acceptance_refused",
            message="The Groundskeeper does not accept that bounded custody request.",
        )

    try:
        actor_place_id = application.entity_place_id(actor_entity_id)
    except Exception:
        actor_place_id = None
    if not _actor_local(application, actor_entity_id):
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            place_id=actor_place_id,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm12_requested_actor_not_local",
            message="The Groundskeeper is not here to receive that request.",
        )

    acceptance = "accepted"
    operation = parsed.operation or ""
    opportunity_available = _custody_opportunity(
        application,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
    )
    qualification, opportunity = _owner_evidence(
        request_id=request_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
        opportunity_available=opportunity_available,
    )
    if not opportunity_available:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            place_id=actor_place_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm12_r4e_opportunity_unavailable",
            message=(
                "The Groundskeeper accepts, but cannot perform that custody "
                "action from the current state."
            ),
            qualification_evidence_id=qualification.evidence_id,
            opportunity_evidence_id=opportunity.evidence_id,
        )

    command_id = application._next_custody_command_id()
    command = create_command_envelope(
        command_id=command_id,
        command_type=f"{operation}_object",
        source_actor_id=actor_entity_id,
        payload={"object_entity_id": object_entity_id},
        metadata={
            "client": "myravant-terminal-vsm12",
            "request_id": request_id,
            "requester_entity_id": application.fixture.player_entity_id,
            "requested_actor_entity_id": actor_entity_id,
        },
    )
    try:
        committed = execute_persistent_world_object_custody(
            state=application.custody_state,
            command=command,
            qualification_evidence=qualification,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=application.representation_digest(),
        )
    except PersistentWorldObjectCustodyError as exc:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            place_id=actor_place_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class=type(exc).__name__,
            message="The accepted request was rejected by authoritative R4-E custody legality.",
            command_id=command_id,
            qualification_evidence_id=qualification.evidence_id,
            opportunity_evidence_id=opportunity.evidence_id,
        )

    application._runtime_state = replace_persistent_world_runtime_custody_state(
        state=application.runtime_state,
        custody_state=committed.state,
    )
    post_digest = application.authoritative_digest()
    verb = "picks up" if operation == "pickup" else "drops"
    result = PlayApplicationResult(
        result_type="actor_mediated_custody_committed",
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
    return VSM12Execution(
        result=result,
        request_receipt=VSM12RequestReceipt(
            request_id=request_id,
            requester_entity_id=application.fixture.player_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=committed.receipt.actor_entity_id,
            target_entity_id=committed.receipt.object_entity_id,
            requested_operation=operation,
            place_id=committed.receipt.place_id,
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
        ),
    )

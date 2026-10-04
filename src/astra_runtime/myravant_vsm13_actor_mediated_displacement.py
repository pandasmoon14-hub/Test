"""VSM-13 bounded actor-mediated local object displacement.

A player request, fixture-local actor acceptance, existing COMP-3 displacement
qualification, performing actor, and committed throw remain distinct stages.
Only the fixture Groundskeeper, Brass Lantern, and existing Yard -> Orchard Path
eastward throw route are in scope.

Authoritative displacement remains owned by the existing COMP-3 path and its
RT-010 / AFQR-18 / AFQR-19 / AFQR-01 / AFQR-02 semantics. This module adds no
new state family, semantic owner, persistence component, projectile physics,
attack semantics, delayed task, or generic actor-command system.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    PersistentWorldObjectDisplacementError,
    create_object_displacement_opportunity_evidence,
    create_object_displacement_qualification_evidence,
    create_object_displacement_spatial_evidence,
    execute_persistent_world_object_displacement,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    replace_persistent_world_runtime_displacement_state,
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
    ORCHARD_PATH_ID,
    YARD_ID,
    UnavailableFixtureCustodyError,
    UnavailableFixtureDisplacementError,
    UnavailableFixtureHandoffError,
)


VSM13_PACKAGE_ID = "VSM-13"
VSM13_CAPABILITY = "bounded_actor_mediated_local_object_displacement"
VSM13_SUPPORTED_DIRECTION = "east"


@dataclass(frozen=True, kw_only=True)
class ParsedVSM13Request:
    raw_text: str
    actor_reference: str | None
    object_reference: str | None
    direction: str | None
    parsed: bool
    failure_class: str | None = None


@dataclass(frozen=True, kw_only=True)
class VSM13RequestReceipt:
    request_id: str
    requester_entity_id: str
    requested_actor_entity_id: str | None
    performing_actor_entity_id: str | None
    target_entity_id: str | None
    requested_direction: str | None
    source_place_id: str | None
    destination_place_id: str | None
    acceptance: str
    legality_result: str
    authoritative_outcome: str
    command_id: str | None = None
    command_fingerprint: str | None = None
    qualification_evidence_id: str | None = None
    spatial_evidence_id: str | None = None
    opportunity_evidence_id: str | None = None
    authoritative_receipt_id: str | None = None
    state_delta_id: str | None = None
    pre_state_digest: str | None = None
    post_state_digest: str | None = None


@dataclass(frozen=True, kw_only=True)
class VSM13Execution:
    result: PlayApplicationResult
    request_receipt: VSM13RequestReceipt


def _normalized_words(raw_text: str) -> list[str]:
    return raw_text.strip().casefold().replace("-", " ").split()


def parse_vsm13_request(raw_text: str) -> ParsedVSM13Request:
    """Parse only the explicit Groundskeeper/Lantern/east immediate throw."""

    words = _normalized_words(raw_text)
    if words and words[0] == "i":
        words = words[1:]
    if not words or words[0] != "ask" or "to" not in words[1:]:
        return ParsedVSM13Request(
            raw_text=raw_text,
            actor_reference=None,
            object_reference=None,
            direction=None,
            parsed=False,
            failure_class="vsm13_not_actor_mediated_request",
        )

    to_index = words.index("to", 1)
    actor_words = words[1:to_index]
    if actor_words and actor_words[0] == "the":
        actor_words = actor_words[1:]
    actor_reference = " ".join(actor_words)
    requested = words[to_index + 1 :]

    if not requested or requested[0] != "throw":
        return ParsedVSM13Request(
            raw_text=raw_text,
            actor_reference=actor_reference or None,
            object_reference=None,
            direction=None,
            parsed=False,
            failure_class="vsm13_request_outside_bounded_parser",
        )

    body = requested[1:]
    if body and body[0] == "the":
        body = body[1:]
    if len(body) < 2:
        return ParsedVSM13Request(
            raw_text=raw_text,
            actor_reference=actor_reference or None,
            object_reference=None,
            direction=None,
            parsed=False,
            failure_class="vsm13_request_outside_bounded_parser",
        )

    direction = body[-1]
    object_reference = " ".join(body[:-1])
    if (
        actor_reference != "groundskeeper"
        or object_reference not in {"lantern", "brass lantern"}
        or direction != VSM13_SUPPORTED_DIRECTION
    ):
        return ParsedVSM13Request(
            raw_text=raw_text,
            actor_reference=actor_reference or None,
            object_reference=object_reference or None,
            direction=direction or None,
            parsed=False,
            failure_class="vsm13_request_outside_bounded_parser",
        )

    return ParsedVSM13Request(
        raw_text=raw_text,
        actor_reference=actor_reference,
        object_reference=object_reference,
        direction=direction,
        parsed=True,
    )


def _request_id(
    *, requester_entity_id: str, raw_text: str, pre_state_digest: str
) -> str:
    token = hashlib.sha256(
        f"{requester_entity_id}|{raw_text.strip()}|{pre_state_digest}".encode("utf-8")
    ).hexdigest()[:24]
    return build_record_id("actor_mediated_displacement_request", token)


def _actor_local(
    application: MyravantPlayApplication,
    actor_entity_id: str,
) -> bool:
    try:
        return application.entity_place_id(actor_entity_id) == application.current_place_id()
    except Exception:
        return False


def _object_carried_by_actor(
    application: MyravantPlayApplication,
    *,
    actor_entity_id: str,
    object_entity_id: str,
) -> bool:
    placements = [
        relation
        for relation in application.state.representation.relations
        if relation.subject_entity_id == object_entity_id
    ]
    return (
        len(placements) == 1
        and placements[0].relation_type == CARRIED_BY_RELATION_TYPE
        and placements[0].object_entity_id == actor_entity_id
    )


def _owner_evidence(
    *,
    command_id: str,
    actor_entity_id: str,
    object_entity_id: str,
    source_place_id: str,
    destination_place_id: str,
    opportunity_available: bool,
):
    token = hashlib.sha256(
        (
            f"{command_id}|{actor_entity_id}|{object_entity_id}|"
            f"{source_place_id}|{destination_place_id}|throw|"
            f"{int(opportunity_available)}"
        ).encode("utf-8")
    ).hexdigest()[:20]
    qualification = create_object_displacement_qualification_evidence(
        evidence_id=build_record_id("evidence", f"vsm13-{token}-rt010"),
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        method="throw",
        qualified=True,
    )
    spatial = create_object_displacement_spatial_evidence(
        evidence_id=build_record_id("evidence", f"vsm13-{token}-afqr18"),
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
        method="throw",
        spatially_permitted=True,
    )
    opportunity = create_object_displacement_opportunity_evidence(
        evidence_id=build_record_id("evidence", f"vsm13-{token}-afqr19"),
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
        method="throw",
        opportunity_available=opportunity_available,
        resolution_accepted=True,
    )
    return qualification, spatial, opportunity


def _rejected(
    application: MyravantPlayApplication,
    *,
    request_id: str,
    parsed: ParsedVSM13Request,
    actor_entity_id: str | None,
    target_entity_id: str | None,
    source_place_id: str | None,
    destination_place_id: str | None,
    acceptance: str,
    legality_result: str,
    failure_class: str,
    message: str,
    command_id: str | None = None,
    qualification_evidence_id: str | None = None,
    spatial_evidence_id: str | None = None,
    opportunity_evidence_id: str | None = None,
) -> VSM13Execution:
    digest = application.authoritative_digest()
    return VSM13Execution(
        result=PlayApplicationResult(
            result_type="actor_mediated_displacement_rejected",
            message=message,
            authoritative_changed=False,
            command_id=command_id,
            spatial_evidence_id=spatial_evidence_id,
            opportunity_evidence_id=opportunity_evidence_id,
            pre_state_digest=digest,
            post_state_digest=digest,
            failure_class=failure_class,
        ),
        request_receipt=VSM13RequestReceipt(
            request_id=request_id,
            requester_entity_id=application.fixture.player_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=None,
            target_entity_id=target_entity_id,
            requested_direction=parsed.direction,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            acceptance=acceptance,
            legality_result=legality_result,
            authoritative_outcome="no_commit",
            command_id=command_id,
            qualification_evidence_id=qualification_evidence_id,
            spatial_evidence_id=spatial_evidence_id,
            opportunity_evidence_id=opportunity_evidence_id,
            pre_state_digest=digest,
            post_state_digest=digest,
        ),
    )


def execute_vsm13_request(
    application: MyravantPlayApplication,
    raw_text: str,
) -> VSM13Execution:
    """Execute one bounded request through existing COMP-3 authority."""

    pre_digest = application.authoritative_digest()
    parsed = parse_vsm13_request(raw_text)
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
            source_place_id=None,
            destination_place_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class=parsed.failure_class or "vsm13_request_unavailable",
            message="That actor-mediated throw request is outside the bounded VSM-13 route.",
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
            source_place_id=None,
            destination_place_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class="vsm13_requested_actor_unavailable",
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
            source_place_id=None,
            destination_place_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class="vsm13_target_unavailable",
            message="The requested target is not available.",
        )

    if actor_entity_id != GROUNDSKEEPER_ID or object_entity_id != LANTERN_ID:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            source_place_id=None,
            destination_place_id=None,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm13_fixture_acceptance_refused",
            message="The Groundskeeper does not accept that bounded throw request.",
        )

    try:
        source_place_id = application.entity_place_id(actor_entity_id)
    except Exception:
        source_place_id = None
    if not _actor_local(application, actor_entity_id):
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            source_place_id=source_place_id,
            destination_place_id=None,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm13_requested_actor_not_local",
            message="The Groundskeeper is not here to receive that request.",
        )

    acceptance = "accepted"
    if source_place_id != YARD_ID:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            source_place_id=source_place_id,
            destination_place_id=None,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm13_source_outside_bounded_route",
            message="The Groundskeeper accepts, but that throw is unavailable from here.",
        )

    try:
        destination_place_id = application.fixture.object_displacement_destination_for(
            object_entity_id=object_entity_id,
            source_place_id=source_place_id,
            direction=parsed.direction or "",
            method="throw",
        )
    except UnavailableFixtureDisplacementError:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            source_place_id=source_place_id,
            destination_place_id=None,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm13_displacement_route_unavailable",
            message="The Groundskeeper accepts, but that throw route is unavailable.",
        )

    if destination_place_id != ORCHARD_PATH_ID:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm13_destination_outside_bounded_route",
            message="The Groundskeeper accepts, but that destination is outside VSM-13.",
        )

    command_id = application._next_displacement_command_id()
    opportunity_available = _object_carried_by_actor(
        application,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
    )
    qualification, spatial, opportunity = _owner_evidence(
        command_id=command_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
        opportunity_available=opportunity_available,
    )
    if not opportunity_available:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm13_comp3_opportunity_unavailable",
            message=(
                "The Groundskeeper accepts, but cannot throw the Brass Lantern "
                "from the current state."
            ),
            command_id=command_id,
            qualification_evidence_id=qualification.evidence_id,
            spatial_evidence_id=spatial.evidence_id,
            opportunity_evidence_id=opportunity.evidence_id,
        )

    command = create_command_envelope(
        command_id=command_id,
        command_type="transfer_object",
        source_actor_id=actor_entity_id,
        payload={
            "object_entity_id": object_entity_id,
            "destination_entity_id": destination_place_id,
            "method": "throw",
        },
        metadata={
            "client": "myravant-terminal-vsm13",
            "package": VSM13_PACKAGE_ID,
            "request_id": request_id,
            "requester_entity_id": application.fixture.player_entity_id,
            "requested_actor_entity_id": actor_entity_id,
        },
    )
    try:
        committed = execute_persistent_world_object_displacement(
            state=application.displacement_state,
            command=command,
            qualification_evidence=qualification,
            spatial_evidence=spatial,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=application.representation_digest(),
        )
    except PersistentWorldObjectDisplacementError as exc:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            target_entity_id=object_entity_id,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class=type(exc).__name__,
            message="The accepted request was rejected by authoritative COMP-3 legality.",
            command_id=command_id,
            qualification_evidence_id=qualification.evidence_id,
            spatial_evidence_id=spatial.evidence_id,
            opportunity_evidence_id=opportunity.evidence_id,
        )

    application._runtime_state = replace_persistent_world_runtime_displacement_state(
        state=application.runtime_state,
        displacement_state=committed.state,
    )
    post_digest = application.authoritative_digest()
    result = PlayApplicationResult(
        result_type="actor_mediated_displacement_committed",
        message="The Groundskeeper throws the Brass Lantern east.",
        authoritative_changed=True,
        command_id=command_id,
        command_fingerprint=committed.receipt.command_fingerprint,
        preview_id=committed.preview.preview_id,
        receipt_id=committed.receipt.receipt_id,
        state_delta_id=committed.state_delta.delta_id,
        spatial_evidence_id=committed.receipt.spatial_evidence_id,
        opportunity_evidence_id=committed.receipt.opportunity_evidence_id,
        pre_state_digest=pre_digest,
        post_state_digest=post_digest,
        technical_retry=committed.technical_retry,
    )
    return VSM13Execution(
        result=result,
        request_receipt=VSM13RequestReceipt(
            request_id=request_id,
            requester_entity_id=application.fixture.player_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=committed.receipt.actor_entity_id,
            target_entity_id=committed.receipt.object_entity_id,
            requested_direction=parsed.direction,
            source_place_id=committed.receipt.source_place_id,
            destination_place_id=committed.receipt.destination_place_id,
            acceptance=acceptance,
            legality_result="allowed",
            authoritative_outcome="committed",
            command_id=command_id,
            command_fingerprint=committed.receipt.command_fingerprint,
            qualification_evidence_id=committed.receipt.rt010_qualification_id,
            spatial_evidence_id=committed.receipt.spatial_evidence_id,
            opportunity_evidence_id=committed.receipt.opportunity_evidence_id,
            authoritative_receipt_id=committed.receipt.receipt_id,
            state_delta_id=committed.state_delta.delta_id,
            pre_state_digest=pre_digest,
            post_state_digest=post_digest,
        ),
    )

"""VSM-10 bounded actor-mediated local movement.

This module extends the request/actor distinction proven by VSM-9 into the
existing authoritative R4-C movement path. A player request, fixture-local
acceptance, spatial/opportunity legality, performing actor, and committed
movement remain distinct stages.

The proof is intentionally narrow: only the fixture Groundskeeper may be asked,
while co-located with the player, to move immediately between the Yard and the
Gatehouse. Directional wording is accepted only where the existing fixture route
resolves to one of those two places. This is not follow/escort, planning,
persistent obligation, generic delegation, dialogue, persuasion, obedience, or a
generic NPC-command system.

Authoritative movement remains owned by the existing R4-C path and its AFQR-18,
AFQR-19, AFQR-01, and AFQR-02 semantics. VSM-10 request receipts are bounded
application-level provenance, not authoritative world state.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementIntegrationError,
    create_movement_opportunity_evidence,
    create_movement_spatial_evidence,
    execute_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    replace_persistent_world_runtime_movement_state,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.myravant_play_application import (
    MyravantPlayApplication,
    PlayApplicationResult,
)
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    YARD_ID,
    UnavailableFixtureHandoffError,
)


VSM10_PACKAGE_ID = "VSM-10"
VSM10_CAPABILITY = "bounded_actor_mediated_local_movement"
VSM10_SUPPORTED_DESTINATIONS = frozenset({YARD_ID, GATEHOUSE_ID})
VSM10_SUPPORTED_DIRECTIONS = frozenset({"north", "south"})


@dataclass(frozen=True, kw_only=True)
class ParsedVSM10Request:
    raw_text: str
    actor_reference: str | None
    direction: str | None
    destination_reference: str | None
    parsed: bool
    failure_class: str | None = None


@dataclass(frozen=True, kw_only=True)
class VSM10RequestReceipt:
    request_id: str
    requester_entity_id: str
    requested_actor_entity_id: str | None
    performing_actor_entity_id: str | None
    source_place_id: str | None
    destination_place_id: str | None
    requested_direction: str | None
    requested_destination_reference: str | None
    acceptance: str
    legality_result: str
    authoritative_outcome: str
    command_id: str | None = None
    command_fingerprint: str | None = None
    spatial_evidence_id: str | None = None
    opportunity_evidence_id: str | None = None
    authoritative_receipt_id: str | None = None
    state_delta_id: str | None = None
    pre_state_digest: str | None = None
    post_state_digest: str | None = None


@dataclass(frozen=True, kw_only=True)
class VSM10Execution:
    result: PlayApplicationResult
    request_receipt: VSM10RequestReceipt


def _normalized_words(raw_text: str) -> list[str]:
    return raw_text.strip().casefold().replace("-", " ").split()


def parse_vsm10_request(raw_text: str) -> ParsedVSM10Request:
    """Parse only explicit Groundskeeper immediate-movement requests."""

    words = _normalized_words(raw_text)
    if words and words[0] == "i":
        words = words[1:]
    if not words or words[0] != "ask" or "to" not in words[1:]:
        return ParsedVSM10Request(
            raw_text=raw_text,
            actor_reference=None,
            direction=None,
            destination_reference=None,
            parsed=False,
            failure_class="vsm10_not_actor_mediated_request",
        )

    to_index = words.index("to", 1)
    actor_words = words[1:to_index]
    if actor_words and actor_words[0] == "the":
        actor_words = actor_words[1:]
    requested = words[to_index + 1 :]
    actor_reference = " ".join(actor_words)

    if actor_reference != "groundskeeper" or not requested:
        return ParsedVSM10Request(
            raw_text=raw_text,
            actor_reference=actor_reference or None,
            direction=None,
            destination_reference=None,
            parsed=False,
            failure_class="vsm10_request_outside_bounded_parser",
        )

    if requested[0] == "move" and len(requested) == 2:
        direction = requested[1]
        if direction in VSM10_SUPPORTED_DIRECTIONS:
            return ParsedVSM10Request(
                raw_text=raw_text,
                actor_reference=actor_reference,
                direction=direction,
                destination_reference=None,
                parsed=True,
            )

    if requested[0] in {"go", "walk", "head"}:
        destination_words = requested[1:]
        if destination_words and destination_words[0] == "to":
            destination_words = destination_words[1:]
        if destination_words and destination_words[0] == "the":
            destination_words = destination_words[1:]
        destination_reference = " ".join(destination_words)
        if destination_reference in {"yard", "gatehouse"}:
            return ParsedVSM10Request(
                raw_text=raw_text,
                actor_reference=actor_reference,
                direction=None,
                destination_reference=destination_reference,
                parsed=True,
            )

    return ParsedVSM10Request(
        raw_text=raw_text,
        actor_reference=actor_reference,
        direction=None,
        destination_reference=None,
        parsed=False,
        failure_class="vsm10_request_outside_bounded_parser",
    )


def _request_id(
    *, requester_entity_id: str, raw_text: str, pre_state_digest: str
) -> str:
    token = hashlib.sha256(
        f"{requester_entity_id}|{raw_text.strip()}|{pre_state_digest}".encode("utf-8")
    ).hexdigest()[:24]
    return build_record_id("actor_mediated_movement_request", token)


def _actor_present_with_requester(
    application: MyravantPlayApplication,
    actor_entity_id: str,
) -> bool:
    try:
        return application.entity_place_id(actor_entity_id) == application.current_place_id()
    except Exception:
        return False


def _destination_for_request(
    application: MyravantPlayApplication,
    *,
    source_place_id: str,
    parsed: ParsedVSM10Request,
) -> str | None:
    if parsed.destination_reference == "yard":
        return YARD_ID
    if parsed.destination_reference == "gatehouse":
        return GATEHOUSE_ID
    if parsed.direction is not None:
        matches = [
            route.destination_place_id
            for route in application.fixture.movement_routes
            if route.source_place_id == source_place_id
            and route.direction == parsed.direction
        ]
        if len(matches) == 1:
            return matches[0]
    return None


def _fixture_route_exists(
    application: MyravantPlayApplication,
    *,
    source_place_id: str,
    destination_place_id: str,
) -> bool:
    return any(
        route.source_place_id == source_place_id
        and route.destination_place_id == destination_place_id
        for route in application.fixture.movement_routes
    )


def _rejected_execution(
    application: MyravantPlayApplication,
    *,
    request_id: str,
    parsed: ParsedVSM10Request,
    actor_entity_id: str | None,
    source_place_id: str | None,
    destination_place_id: str | None,
    acceptance: str,
    legality_result: str,
    failure_class: str,
    message: str,
    command_id: str | None = None,
    spatial_evidence_id: str | None = None,
    opportunity_evidence_id: str | None = None,
) -> VSM10Execution:
    digest = application.authoritative_digest()
    result = PlayApplicationResult(
        result_type="actor_mediated_movement_rejected",
        message=message,
        authoritative_changed=False,
        command_id=command_id,
        spatial_evidence_id=spatial_evidence_id,
        opportunity_evidence_id=opportunity_evidence_id,
        pre_state_digest=digest,
        post_state_digest=digest,
        failure_class=failure_class,
    )
    return VSM10Execution(
        result=result,
        request_receipt=VSM10RequestReceipt(
            request_id=request_id,
            requester_entity_id=application.fixture.player_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=None,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            requested_direction=parsed.direction,
            requested_destination_reference=parsed.destination_reference,
            acceptance=acceptance,
            legality_result=legality_result,
            authoritative_outcome="no_commit",
            command_id=command_id,
            spatial_evidence_id=spatial_evidence_id,
            opportunity_evidence_id=opportunity_evidence_id,
            pre_state_digest=digest,
            post_state_digest=digest,
        ),
    )


def execute_vsm10_request(
    application: MyravantPlayApplication,
    raw_text: str,
) -> VSM10Execution:
    """Execute one bounded local movement request through existing R4-C authority."""

    pre_digest = application.authoritative_digest()
    parsed = parse_vsm10_request(raw_text)
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
            source_place_id=None,
            destination_place_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class=parsed.failure_class or "vsm10_request_unavailable",
            message="That actor-mediated movement request is outside the bounded VSM-10 route.",
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
            source_place_id=None,
            destination_place_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class="vsm10_requested_actor_unavailable",
            message="The requested actor is not available.",
        )

    if actor_entity_id != GROUNDSKEEPER_ID:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            source_place_id=None,
            destination_place_id=None,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm10_fixture_acceptance_refused",
            message="The requested actor does not accept that bounded movement request.",
        )

    try:
        source_place_id = application.entity_place_id(actor_entity_id)
    except Exception:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            source_place_id=None,
            destination_place_id=None,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm10_requested_actor_location_unavailable",
            message="The Groundskeeper's current location is unavailable.",
        )

    if not _actor_present_with_requester(application, actor_entity_id):
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            source_place_id=source_place_id,
            destination_place_id=None,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm10_requested_actor_not_local",
            message="The Groundskeeper is not here to receive that request.",
        )

    acceptance = "accepted"
    destination_place_id = _destination_for_request(
        application,
        source_place_id=source_place_id,
        parsed=parsed,
    )
    if destination_place_id is None:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            source_place_id=source_place_id,
            destination_place_id=None,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm10_movement_route_unavailable",
            message="The Groundskeeper accepts, but that movement route is unavailable.",
        )

    if destination_place_id not in VSM10_SUPPORTED_DESTINATIONS:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm10_destination_outside_bounded_route",
            message="The Groundskeeper accepts, but that destination is outside the bounded movement route.",
        )

    if source_place_id == destination_place_id:
        place_name = application.fixture.place_presentation(destination_place_id).name
        result = PlayApplicationResult(
            result_type="actor_mediated_movement_unchanged",
            message=f"The Groundskeeper is already at the {place_name}.",
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=pre_digest,
        )
        return VSM10Execution(
            result=result,
            request_receipt=VSM10RequestReceipt(
                request_id=request_id,
                requester_entity_id=application.fixture.player_entity_id,
                requested_actor_entity_id=actor_entity_id,
                performing_actor_entity_id=actor_entity_id,
                source_place_id=source_place_id,
                destination_place_id=destination_place_id,
                requested_direction=parsed.direction,
                requested_destination_reference=parsed.destination_reference,
                acceptance=acceptance,
                legality_result="allowed_no_change",
                authoritative_outcome="unchanged",
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            ),
        )

    if not _fixture_route_exists(
        application,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
    ):
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm10_movement_route_unavailable",
            message="The Groundskeeper accepts, but that movement route is unavailable.",
        )

    command_id = application._next_movement_command_id()
    command = create_command_envelope(
        command_id=command_id,
        command_type="move",
        source_actor_id=actor_entity_id,
        payload={"destination_entity_id": destination_place_id},
        metadata={
            "client": "myravant-terminal-vsm10",
            "package": VSM10_PACKAGE_ID,
            "request_id": request_id,
            "requester_entity_id": application.fixture.player_entity_id,
            "requested_actor_entity_id": actor_entity_id,
        },
    )
    token = hashlib.sha256(
        (
            f"{request_id}|{command_id}|{actor_entity_id}|"
            f"{source_place_id}|{destination_place_id}"
        ).encode("utf-8")
    ).hexdigest()[:20]
    spatial = create_movement_spatial_evidence(
        evidence_id=build_record_id("evidence", f"vsm10-{token}-afqr18"),
        actor_entity_id=actor_entity_id,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
        spatially_permitted=True,
    )
    opportunity = create_movement_opportunity_evidence(
        evidence_id=build_record_id("evidence", f"vsm10-{token}-afqr19"),
        actor_entity_id=actor_entity_id,
        destination_place_id=destination_place_id,
        opportunity_available=True,
        resolution_accepted=True,
    )

    try:
        committed = execute_persistent_world_movement(
            state=application.state,
            command=command,
            spatial_evidence=spatial,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=application.representation_digest(),
        )
    except PersistentWorldMovementIntegrationError as exc:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class=type(exc).__name__,
            message="The Groundskeeper accepts, but authoritative movement legality rejects the attempt.",
            command_id=command_id,
            spatial_evidence_id=spatial.evidence_id,
            opportunity_evidence_id=opportunity.evidence_id,
        )

    application._runtime_state = replace_persistent_world_runtime_movement_state(
        state=application.runtime_state,
        movement_state=committed.state,
    )
    post_digest = application.authoritative_digest()
    destination_name = application.fixture.place_presentation(destination_place_id).name
    result = PlayApplicationResult(
        result_type="actor_mediated_movement_committed",
        message=f"The Groundskeeper moves to the {destination_name}.",
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
    return VSM10Execution(
        result=result,
        request_receipt=VSM10RequestReceipt(
            request_id=request_id,
            requester_entity_id=application.fixture.player_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=actor_entity_id,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            requested_direction=parsed.direction,
            requested_destination_reference=parsed.destination_reference,
            acceptance=acceptance,
            legality_result="allowed",
            authoritative_outcome="committed",
            command_id=command_id,
            command_fingerprint=committed.receipt.command_fingerprint,
            spatial_evidence_id=committed.receipt.spatial_evidence_id,
            opportunity_evidence_id=committed.receipt.opportunity_evidence_id,
            authoritative_receipt_id=committed.receipt.receipt_id,
            state_delta_id=committed.state_delta.delta_id,
            pre_state_digest=pre_digest,
            post_state_digest=post_digest,
        ),
    )

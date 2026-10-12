"""Larger-package 3: bounded actor-mediated ground-contact displacement.

The player's request is a proposal, not a player-directed authoritative move.
Only the noncanonical fixture Groundskeeper accepts these three declared push/
slide opportunities. Existing COMP-3 owns resulting displacement/receipts and
AFQR-12 owns movement following; this adapter owns neither world truth nor RNG.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
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
    TOOL_CHEST_ID,
    UnavailableFixtureCustodyError,
    UnavailableFixtureDisplacementError,
    UnavailableFixtureHandoffError,
)


PACKAGE_ID = "LOCAL-NPC-GROUND-METHODS-3"
_DIRECTIONS = frozenset({"north", "south", "east", "west"})
_OBJECT_REFERENCES = frozenset({
    "lantern", "brass lantern", "chest", "tool chest",
})


@dataclass(frozen=True, kw_only=True)
class ParsedGroundContactRequest:
    raw_text: str
    actor_reference: str | None
    object_reference: str | None
    method: str | None
    direction: str | None
    parsed: bool


@dataclass(frozen=True, kw_only=True)
class GroundContactRequestReceipt:
    request_id: str
    requester_entity_id: str
    requested_actor_entity_id: str | None
    performing_actor_entity_id: str | None
    target_entity_id: str | None
    requested_method: str
    requested_direction: str
    acceptance: str
    legality_result: str
    authoritative_outcome: str
    source_place_id: str | None = None
    destination_place_id: str | None = None
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
class GroundContactExecution:
    result: PlayApplicationResult
    request_receipt: GroundContactRequestReceipt


def parse_ground_contact_request(raw_text: str) -> ParsedGroundContactRequest:
    """Only exact bounded requests qualify; all others retain prior owners."""

    tokens = raw_text.strip().casefold().replace("-", " ").split()
    if tokens[:1] == ["i"]:
        tokens = tokens[1:]
    if tokens[:1] != ["ask"] or "to" not in tokens[1:]:
        return ParsedGroundContactRequest(
            raw_text=raw_text, actor_reference=None, object_reference=None,
            method=None, direction=None, parsed=False,
        )
    pivot = tokens.index("to", 1)
    actor = tokens[1:pivot]
    if actor[:1] == ["the"]:
        actor = actor[1:]
    requested = tokens[pivot + 1:]
    if (
        actor != ["groundskeeper"]
        or len(requested) < 3
        or requested[0] not in {"push", "slide"}
        or requested[-1] not in _DIRECTIONS
    ):
        return ParsedGroundContactRequest(
            raw_text=raw_text, actor_reference=" ".join(actor) or None,
            object_reference=None, method=None, direction=None, parsed=False,
        )
    object_tokens = requested[1:-1]
    if object_tokens[:1] == ["the"]:
        object_tokens = object_tokens[1:]
    target = " ".join(object_tokens)
    if target not in _OBJECT_REFERENCES:
        return ParsedGroundContactRequest(
            raw_text=raw_text, actor_reference="groundskeeper",
            object_reference=target or None, method=None,
            direction=requested[-1], parsed=False,
        )
    return ParsedGroundContactRequest(
        raw_text=raw_text,
        actor_reference="groundskeeper",
        object_reference=target,
        method=requested[0],
        direction=requested[-1],
        parsed=True,
    )


def execute_ground_contact_request(
    application: MyravantPlayApplication, raw_text: str,
) -> GroundContactExecution:
    parsed = parse_ground_contact_request(raw_text)
    if not parsed.parsed:
        raise ValueError("not a qualified actor-mediated ground-contact request")

    pre_digest = application.authoritative_digest()
    requester = application.fixture.player_entity_id
    token = hashlib.sha256(
        f"{requester}|{raw_text.strip()}|{pre_digest}".encode("utf-8")
    ).hexdigest()[:24]
    request_id = build_record_id("actor_mediated_ground_request", token)
    method = parsed.method or ""
    direction = parsed.direction or ""

    def refuse(
        failure_class: str,
        message: str,
        *,
        acceptance: str = "refused",
        legality_result: str = "not_evaluated",
        actor_id: str | None = None,
        object_id: str | None = None,
        source_id: str | None = None,
        destination_id: str | None = None,
        command_id: str | None = None,
        qualification_id: str | None = None,
        spatial_id: str | None = None,
        opportunity_id: str | None = None,
    ) -> GroundContactExecution:
        digest = application.authoritative_digest()
        return GroundContactExecution(
            result=PlayApplicationResult(
                result_type="actor_mediated_ground_displacement_rejected",
                message=message,
                authoritative_changed=False,
                command_id=command_id,
                spatial_evidence_id=spatial_id,
                opportunity_evidence_id=opportunity_id,
                pre_state_digest=digest,
                post_state_digest=digest,
                failure_class=failure_class,
            ),
            request_receipt=GroundContactRequestReceipt(
                request_id=request_id,
                requester_entity_id=requester,
                requested_actor_entity_id=actor_id,
                performing_actor_entity_id=None,
                target_entity_id=object_id,
                requested_method=method,
                requested_direction=direction,
                acceptance=acceptance,
                legality_result=legality_result,
                authoritative_outcome="no_commit",
                source_place_id=source_id,
                destination_place_id=destination_id,
                command_id=command_id,
                qualification_evidence_id=qualification_id,
                spatial_evidence_id=spatial_id,
                opportunity_evidence_id=opportunity_id,
                pre_state_digest=digest,
                post_state_digest=digest,
            ),
        )

    try:
        actor_id = application.fixture.resolve_actor_reference(
            parsed.actor_reference or ""
        )
    except UnavailableFixtureHandoffError:
        return refuse("ground_request_actor_unavailable",
                      "That actor is not available.")
    try:
        object_id = application.fixture.resolve_object_reference(
            parsed.object_reference or ""
        )
    except UnavailableFixtureCustodyError:
        return refuse(
            "ground_request_target_unavailable",
            "That object is not available.",
            actor_id=actor_id,
        )

    if actor_id != GROUNDSKEEPER_ID or object_id not in {
        LANTERN_ID, TOOL_CHEST_ID
    }:
        return refuse(
            "ground_request_not_accepted",
            "The requested actor does not accept this task.",
            actor_id=actor_id, object_id=object_id,
        )

    try:
        actor_place = application.entity_place_id(actor_id)
    except Exception:
        actor_place = None

    if actor_place != application.current_place_id():
        return refuse(
            "ground_request_actor_not_local",
            "The Groundskeeper is not here to receive that request.",
            actor_id=actor_id, object_id=object_id, source_id=actor_place,
        )

    # This fixture defines willingness to attempt an immediate local action,
    # never automatic success or general obedience.
    acceptance = "accepted"
    try:
        dest = application.fixture.object_displacement_destination_for(
            object_entity_id=object_id,
            source_place_id=actor_place,
            direction=direction,
            method=method,
        )
    except UnavailableFixtureDisplacementError:
        return refuse(
            "ground_request_route_unavailable",
            "The Groundskeeper agrees to try, but cannot move it that way.",
            acceptance=acceptance, legality_result="rejected",
            actor_id=actor_id, object_id=object_id, source_id=actor_place,
        )

    placement = [
        rel for rel in application.state.representation.relations
        if rel.subject_entity_id == object_id
    ]
    opportunity_available = (
        len(placement) == 1
        and placement[0].relation_type == LOCATED_AT_RELATION_TYPE
        and placement[0].object_entity_id == actor_place
    )
    command_id = application._next_displacement_command_id()
    evidence_token = hashlib.sha256(
        (
            f"{command_id}|{actor_id}|{object_id}|{actor_place}|"
            f"{dest}|{method}|{int(opportunity_available)}"
        ).encode("utf-8")
    ).hexdigest()[:20]
    qualification = create_object_displacement_qualification_evidence(
        evidence_id=build_record_id("evidence", f"large3-{evidence_token}-rt010"),
        actor_entity_id=actor_id, object_entity_id=object_id,
        method=method, qualified=True,
    )
    spatial = create_object_displacement_spatial_evidence(
        evidence_id=build_record_id("evidence", f"large3-{evidence_token}-afqr18"),
        actor_entity_id=actor_id, object_entity_id=object_id,
        source_place_id=actor_place, destination_place_id=dest,
        method=method, spatially_permitted=True,
    )
    opportunity = create_object_displacement_opportunity_evidence(
        evidence_id=build_record_id("evidence", f"large3-{evidence_token}-afqr19"),
        actor_entity_id=actor_id, object_entity_id=object_id,
        source_place_id=actor_place, destination_place_id=dest,
        method=method, opportunity_available=opportunity_available,
        resolution_accepted=True,
    )
    if not opportunity_available:
        return refuse(
            "ground_request_object_not_grounded",
            "The Groundskeeper agrees, but the object is not on the ground here.",
            acceptance=acceptance, legality_result="rejected",
            actor_id=actor_id, object_id=object_id,
            source_id=actor_place, destination_id=dest,
            command_id=command_id,
            qualification_id=qualification.evidence_id,
            spatial_id=spatial.evidence_id,
            opportunity_id=opportunity.evidence_id,
        )

    command = create_command_envelope(
        command_id=command_id,
        command_type="transfer_object",
        source_actor_id=actor_id,
        payload={
            "object_entity_id": object_id,
            "destination_entity_id": dest,
            "method": method,
        },
        metadata={
            "client": "myravant-terminal",
            "package": PACKAGE_ID,
            "request_id": request_id,
            "requester_entity_id": requester,
            "requested_actor_entity_id": actor_id,
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
        return refuse(
            type(exc).__name__,
            "The Groundskeeper's attempt was rejected by the authoritative runtime.",
            acceptance=acceptance, legality_result="rejected",
            actor_id=actor_id, object_id=object_id,
            source_id=actor_place, destination_id=dest,
            command_id=command_id,
            qualification_id=qualification.evidence_id,
            spatial_id=spatial.evidence_id,
            opportunity_id=opportunity.evidence_id,
        )

    application._runtime_state = replace_persistent_world_runtime_displacement_state(
        state=application.runtime_state,
        displacement_state=committed.state,
    )
    post_digest = application.authoritative_digest()
    result = PlayApplicationResult(
        result_type="actor_mediated_ground_displacement_committed",
        message=(
            f"The Groundskeeper {method + ('es' if method == 'push' else 's')} the "
            f"{application.fixture.entity_name(object_id)} {direction}."
        ),
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
    receipt = GroundContactRequestReceipt(
        request_id=request_id,
        requester_entity_id=requester,
        requested_actor_entity_id=actor_id,
        performing_actor_entity_id=committed.receipt.actor_entity_id,
        target_entity_id=committed.receipt.object_entity_id,
        requested_method=method,
        requested_direction=direction,
        acceptance=acceptance,
        legality_result="allowed",
        authoritative_outcome="committed",
        source_place_id=committed.receipt.source_place_id,
        destination_place_id=committed.receipt.destination_place_id,
        command_id=command_id,
        command_fingerprint=committed.receipt.command_fingerprint,
        qualification_evidence_id=qualification.evidence_id,
        spatial_evidence_id=committed.receipt.spatial_evidence_id,
        opportunity_evidence_id=committed.receipt.opportunity_evidence_id,
        authoritative_receipt_id=committed.receipt.receipt_id,
        state_delta_id=committed.state_delta.delta_id,
        pre_state_digest=pre_digest,
        post_state_digest=post_digest,
    )
    return GroundContactExecution(result=result, request_receipt=receipt)

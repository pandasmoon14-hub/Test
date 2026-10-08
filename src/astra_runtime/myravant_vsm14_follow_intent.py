"""VSM-14 bounded persistent follow-intent request route.

A player request, fixture-local acceptance, authoritative AFQR-12 follow intent,
and later R4-C movement consequences remain distinct. This module accepts only
the fixture Groundskeeper following the fixture player, and only while they are
co-located when the request is made.

The request does not grant player control, ownership, obedience, social status,
responsibility, generic delegation, planning, guarding, dialogue, or delayed
conditional task semantics.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from astra_runtime.domain.persistent_world_follow_intent import (
    PersistentWorldFollowIntentError,
    active_follow_intent_for,
    create_follow_intent_opportunity_evidence,
    create_follow_intent_qualification_evidence,
    create_follow_intent_spatial_evidence,
    digest_persistent_world_follow_intent_runtime_state,
    execute_persistent_world_follow_intent,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    PLAYER_ID,
    UnavailableFixtureHandoffError,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


VSM14_PACKAGE_ID = "VSM-14"
VSM14_CAPABILITY = "bounded_persistent_follow_intent"
VSM14_SUPPORTED_ACTOR_ID = GROUNDSKEEPER_ID
VSM14_SUPPORTED_LEADER_ID = PLAYER_ID


@dataclass(frozen=True, kw_only=True)
class ParsedVSM14FollowRequest:
    raw_text: str
    actor_reference: str | None
    operation: str | None
    parsed: bool
    failure_class: str | None = None


@dataclass(frozen=True, kw_only=True)
class VSM14FollowRequestReceipt:
    request_id: str
    requester_entity_id: str
    requested_actor_entity_id: str | None
    performing_actor_entity_id: str | None
    leader_entity_id: str | None
    requested_operation: str | None
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
class VSM14FollowExecution:
    result: PlayApplicationResult
    request_receipt: VSM14FollowRequestReceipt


def _normalized_words(raw_text: str) -> list[str]:
    return raw_text.strip().casefold().replace("-", " ").split()


def parse_vsm14_follow_request(raw_text: str) -> ParsedVSM14FollowRequest:
    """Parse only the exact bounded follow / stop-following request grammar."""

    words = _normalized_words(raw_text)
    if words and words[0] == "i":
        words = words[1:]
    if not words or words[0] != "ask" or "to" not in words[1:]:
        return ParsedVSM14FollowRequest(
            raw_text=raw_text,
            actor_reference=None,
            operation=None,
            parsed=False,
            failure_class="vsm14_not_follow_request",
        )

    to_index = words.index("to", 1)
    actor_words = words[1:to_index]
    if actor_words and actor_words[0] == "the":
        actor_words = actor_words[1:]
    actor_reference = " ".join(actor_words)
    requested = words[to_index + 1 :]

    if actor_reference != "groundskeeper":
        return ParsedVSM14FollowRequest(
            raw_text=raw_text,
            actor_reference=actor_reference or None,
            operation=None,
            parsed=False,
            failure_class="vsm14_request_outside_bounded_parser",
        )

    if requested == ["follow", "me"]:
        return ParsedVSM14FollowRequest(
            raw_text=raw_text,
            actor_reference=actor_reference,
            operation="activate",
            parsed=True,
        )
    if requested == ["stop", "following", "me"]:
        return ParsedVSM14FollowRequest(
            raw_text=raw_text,
            actor_reference=actor_reference,
            operation="deactivate",
            parsed=True,
        )

    return ParsedVSM14FollowRequest(
        raw_text=raw_text,
        actor_reference=actor_reference,
        operation=None,
        parsed=False,
        failure_class="vsm14_request_outside_bounded_parser",
    )


def _request_id(
    *, requester_entity_id: str, raw_text: str, pre_state_digest: str
) -> str:
    token = hashlib.sha256(
        f"{requester_entity_id}|{raw_text.strip()}|{pre_state_digest}".encode(
            "utf-8"
        )
    ).hexdigest()[:24]
    return build_record_id("follow_intent_request", token)


def _rejected(
    application: MyravantVSM14Application,
    *,
    request_id: str,
    parsed: ParsedVSM14FollowRequest,
    actor_entity_id: str | None,
    acceptance: str,
    legality_result: str,
    failure_class: str,
    message: str,
) -> VSM14FollowExecution:
    digest = application.authoritative_digest()
    return VSM14FollowExecution(
        result=PlayApplicationResult(
            result_type="follow_intent_request_rejected",
            message=message,
            authoritative_changed=False,
            pre_state_digest=digest,
            post_state_digest=digest,
            failure_class=failure_class,
        ),
        request_receipt=VSM14FollowRequestReceipt(
            request_id=request_id,
            requester_entity_id=application.fixture.player_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=None,
            leader_entity_id=application.fixture.player_entity_id,
            requested_operation=parsed.operation,
            acceptance=acceptance,
            legality_result=legality_result,
            authoritative_outcome="no_commit",
            pre_state_digest=digest,
            post_state_digest=digest,
        ),
    )


def execute_vsm14_follow_request(
    application: MyravantVSM14Application,
    raw_text: str,
) -> VSM14FollowExecution:
    """Commit one bounded persistent follow-intent request if currently lawful."""

    if not isinstance(application, MyravantVSM14Application):
        raise TypeError("application must be MyravantVSM14Application")

    pre_digest = application.authoritative_digest()
    parsed = parse_vsm14_follow_request(raw_text)
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
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class=parsed.failure_class or "vsm14_follow_request_unavailable",
            message="That follow request is outside the bounded VSM-14 route.",
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
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class="vsm14_requested_actor_unavailable",
            message="The requested actor is not available.",
        )

    if actor_entity_id != VSM14_SUPPORTED_ACTOR_ID:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm14_fixture_acceptance_refused",
            message="That actor does not accept this bounded follow request.",
        )

    try:
        follower_place_id = application.entity_place_id(actor_entity_id)
        leader_place_id = application.entity_place_id(
            application.fixture.player_entity_id
        )
    except Exception:
        follower_place_id = None
        leader_place_id = None
    if (
        follower_place_id is None
        or leader_place_id is None
        or follower_place_id != leader_place_id
    ):
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm14_requested_actor_not_local",
            message="The Groundskeeper is not here to receive that request.",
        )

    leader_entity_id = application.fixture.player_entity_id
    existing = active_follow_intent_for(
        application.follow_intent_state, actor_entity_id
    )
    operation = parsed.operation or ""
    if operation == "activate" and existing is not None:
        return VSM14FollowExecution(
            result=PlayApplicationResult(
                result_type="follow_intent_unchanged",
                message="The Groundskeeper is already following you.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            ),
            request_receipt=VSM14FollowRequestReceipt(
                request_id=request_id,
                requester_entity_id=leader_entity_id,
                requested_actor_entity_id=actor_entity_id,
                performing_actor_entity_id=actor_entity_id,
                leader_entity_id=leader_entity_id,
                requested_operation=operation,
                acceptance="accepted",
                legality_result="allowed_no_change",
                authoritative_outcome="unchanged",
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            ),
        )
    if operation == "deactivate" and existing is None:
        return VSM14FollowExecution(
            result=PlayApplicationResult(
                result_type="follow_intent_unchanged",
                message="The Groundskeeper is not currently following you.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            ),
            request_receipt=VSM14FollowRequestReceipt(
                request_id=request_id,
                requester_entity_id=leader_entity_id,
                requested_actor_entity_id=actor_entity_id,
                performing_actor_entity_id=actor_entity_id,
                leader_entity_id=leader_entity_id,
                requested_operation=operation,
                acceptance="accepted",
                legality_result="allowed_no_change",
                authoritative_outcome="unchanged",
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            ),
        )

    command_id = application._next_follow_intent_command_id()
    token = hashlib.sha256(
        (
            f"{request_id}|{command_id}|{actor_entity_id}|{leader_entity_id}|"
            f"{operation}|{leader_place_id}"
        ).encode("utf-8")
    ).hexdigest()[:20]
    qualification = create_follow_intent_qualification_evidence(
        evidence_id=build_record_id(
            "evidence", f"vsm14-follow-{token}-afqr12"
        ),
        follower_entity_id=actor_entity_id,
        leader_entity_id=leader_entity_id,
        operation=operation,
        qualified=True,
    )
    spatial = create_follow_intent_spatial_evidence(
        evidence_id=build_record_id(
            "evidence", f"vsm14-follow-{token}-afqr18"
        ),
        follower_entity_id=actor_entity_id,
        leader_entity_id=leader_entity_id,
        place_id=leader_place_id,
        co_located=True,
    )
    opportunity = create_follow_intent_opportunity_evidence(
        evidence_id=build_record_id(
            "evidence", f"vsm14-follow-{token}-afqr19"
        ),
        follower_entity_id=actor_entity_id,
        leader_entity_id=leader_entity_id,
        operation=operation,
        opportunity_available=True,
        resolution_accepted=True,
    )
    command = create_command_envelope(
        command_id=command_id,
        command_type="behavior_follow_intent",
        source_actor_id=actor_entity_id,
        payload={
            "leader_entity_id": leader_entity_id,
            "operation": operation,
        },
        metadata={
            "client": "myravant-terminal-vsm14",
            "package": VSM14_PACKAGE_ID,
            "request_id": request_id,
            "requester_entity_id": leader_entity_id,
            "requested_actor_entity_id": actor_entity_id,
        },
    )

    try:
        committed = execute_persistent_world_follow_intent(
            state=application.follow_intent_state,
            command=command,
            qualification_evidence=qualification,
            spatial_evidence=spatial,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=(
                digest_persistent_world_follow_intent_runtime_state(
                    application.follow_intent_state
                )
            ),
        )
    except PersistentWorldFollowIntentError as exc:
        return _rejected(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            acceptance="accepted",
            legality_result="rejected",
            failure_class=type(exc).__name__,
            message=(
                "The Groundskeeper accepts, but the authoritative follow-intent "
                "transition is unavailable."
            ),
        )

    application.replace_follow_intent_state(committed.state)
    post_digest = application.authoritative_digest()
    message = (
        "The Groundskeeper agrees to follow you."
        if operation == "activate"
        else "The Groundskeeper stops following you."
    )
    result = PlayApplicationResult(
        result_type="follow_intent_committed",
        message=message,
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
    return VSM14FollowExecution(
        result=result,
        request_receipt=VSM14FollowRequestReceipt(
            request_id=request_id,
            requester_entity_id=leader_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=actor_entity_id,
            leader_entity_id=leader_entity_id,
            requested_operation=operation,
            acceptance="accepted",
            legality_result="allowed",
            authoritative_outcome="committed",
            command_id=command_id,
            command_fingerprint=committed.receipt.command_fingerprint,
            qualification_evidence_id=(
                committed.receipt.qualification_evidence_id
            ),
            spatial_evidence_id=committed.receipt.spatial_evidence_id,
            opportunity_evidence_id=(
                committed.receipt.opportunity_evidence_id
            ),
            authoritative_receipt_id=committed.receipt.receipt_id,
            state_delta_id=committed.state_delta.delta_id,
            pre_state_digest=pre_digest,
            post_state_digest=post_digest,
        ),
    )

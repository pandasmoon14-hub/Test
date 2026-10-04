"""VSM-11 bounded actor-mediated storage and retrieval.

VSM-11 composes the requester/requested-actor distinction proven by VSM-8
through VSM-10 with the existing authoritative INT-3 storage-transfer path.
A player request, fixture-local Groundskeeper acceptance, INT-3 placement and
opportunity legality, performing actor, and committed containment/custody
outcome remain distinct stages.

The proof is intentionally narrow: while co-located with the player, the
fixture Groundskeeper may be asked to store the Brass Lantern in the Tool Chest
or retrieve the Brass Lantern from the Tool Chest. This is not a generic NPC
command system, inventory planner, task queue, persistent instruction, social
obedience model, or generalized delegation grammar.

Authoritative storage remains owned by existing RT-010 / AFQR-19 / AFQR-01 /
AFQR-02 semantics. VSM-11 request receipts are application-level provenance,
not authoritative world state.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    CONTAINED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    PersistentWorldObjectStorageError,
    create_object_storage_opportunity_evidence,
    create_object_storage_qualification_evidence,
    execute_persistent_world_object_storage,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    replace_persistent_world_runtime_storage_state,
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


VSM11_PACKAGE_ID = "VSM-11"
VSM11_CAPABILITY = "bounded_actor_mediated_storage_retrieval"
VSM11_SUPPORTED_OPERATIONS = frozenset({"store", "retrieve"})


@dataclass(frozen=True, kw_only=True)
class ParsedVSM11Request:
    raw_text: str
    actor_reference: str | None
    operation: str | None
    object_reference: str | None
    container_reference: str | None
    parsed: bool
    failure_class: str | None = None


@dataclass(frozen=True, kw_only=True)
class VSM11RequestReceipt:
    request_id: str
    requester_entity_id: str
    requested_actor_entity_id: str | None
    performing_actor_entity_id: str | None
    object_entity_id: str | None
    container_entity_id: str | None
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
class VSM11Execution:
    result: PlayApplicationResult
    request_receipt: VSM11RequestReceipt


def _normalized_words(raw_text: str) -> list[str]:
    return raw_text.strip().casefold().replace("-", " ").split()


def parse_vsm11_request(raw_text: str) -> ParsedVSM11Request:
    """Parse only explicit Groundskeeper/Lantern/Tool-Chest storage requests."""

    words = _normalized_words(raw_text)
    if words and words[0] == "i":
        words = words[1:]
    if not words or words[0] != "ask" or "to" not in words[1:]:
        return ParsedVSM11Request(
            raw_text=raw_text,
            actor_reference=None,
            operation=None,
            object_reference=None,
            container_reference=None,
            parsed=False,
            failure_class="vsm11_not_actor_mediated_request",
        )

    to_index = words.index("to", 1)
    actor_words = words[1:to_index]
    if actor_words and actor_words[0] == "the":
        actor_words = actor_words[1:]
    actor_reference = " ".join(actor_words)
    requested = [word for word in words[to_index + 1 :] if word != "the"]

    operation: str | None = None
    if requested and requested[0] in {"put", "store"}:
        separator = next(
            (token for token in ("in", "into") if token in requested[1:]),
            None,
        )
        if separator is not None:
            split = requested.index(separator)
            object_words = requested[1:split]
            container_words = requested[split + 1 :]
            if object_words in (["lantern"], ["brass", "lantern"]) and container_words in (
                ["chest"],
                ["tool", "chest"],
            ):
                operation = "store"
    elif requested and requested[0] in {"take", "retrieve", "get"}:
        if "from" in requested[1:]:
            split = requested.index("from")
            object_words = requested[1:split]
            container_words = requested[split + 1 :]
            if object_words in (["lantern"], ["brass", "lantern"]) and container_words in (
                ["chest"],
                ["tool", "chest"],
            ):
                operation = "retrieve"

    if actor_reference != "groundskeeper" or operation is None:
        return ParsedVSM11Request(
            raw_text=raw_text,
            actor_reference=actor_reference or None,
            operation=operation,
            object_reference=None,
            container_reference=None,
            parsed=False,
            failure_class="vsm11_request_outside_bounded_parser",
        )

    return ParsedVSM11Request(
        raw_text=raw_text,
        actor_reference=actor_reference,
        operation=operation,
        object_reference="lantern",
        container_reference="chest",
        parsed=True,
    )


def _request_id(
    *, requester_entity_id: str, raw_text: str, pre_state_digest: str
) -> str:
    token = hashlib.sha256(
        f"{requester_entity_id}|{raw_text.strip()}|{pre_state_digest}".encode("utf-8")
    ).hexdigest()[:24]
    return build_record_id("actor_mediated_storage_request", token)


def _actor_present_with_requester(
    application: MyravantPlayApplication,
    actor_entity_id: str,
) -> bool:
    try:
        return application.entity_place_id(actor_entity_id) == application.current_place_id()
    except Exception:
        return False


def _container_accessible_to_actor(
    application: MyravantPlayApplication,
    *,
    actor_entity_id: str,
    container_entity_id: str,
) -> bool:
    try:
        actor_place_id = application.entity_place_id(actor_entity_id)
    except Exception:
        return False
    representation = application.state.representation
    direct = any(
        relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == container_entity_id
        and relation.object_entity_id == actor_place_id
        for relation in representation.relations
    )
    carried = any(
        relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == container_entity_id
        and relation.object_entity_id == actor_entity_id
        for relation in representation.relations
    )
    nested = any(
        relation.relation_type == CONTAINED_BY_RELATION_TYPE
        and relation.subject_entity_id == container_entity_id
        for relation in representation.relations
    )
    return (direct or carried) and not nested


def _object_carried_by_actor(
    application: MyravantPlayApplication,
    *,
    actor_entity_id: str,
    object_entity_id: str,
) -> bool:
    return any(
        relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
        and relation.object_entity_id == actor_entity_id
        for relation in application.state.representation.relations
    )


def _object_contained_by(
    application: MyravantPlayApplication,
    *,
    object_entity_id: str,
    container_entity_id: str,
) -> bool:
    return any(
        relation.relation_type == CONTAINED_BY_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
        and relation.object_entity_id == container_entity_id
        for relation in application.state.representation.relations
    )


def _rejected_execution(
    application: MyravantPlayApplication,
    *,
    request_id: str,
    parsed: ParsedVSM11Request,
    actor_entity_id: str | None,
    object_entity_id: str | None,
    container_entity_id: str | None,
    acceptance: str,
    legality_result: str,
    failure_class: str,
    message: str,
) -> VSM11Execution:
    digest = application.authoritative_digest()
    result = PlayApplicationResult(
        result_type="actor_mediated_storage_rejected",
        message=message,
        authoritative_changed=False,
        pre_state_digest=digest,
        post_state_digest=digest,
        failure_class=failure_class,
    )
    return VSM11Execution(
        result=result,
        request_receipt=VSM11RequestReceipt(
            request_id=request_id,
            requester_entity_id=application.fixture.player_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=None,
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
            requested_operation=parsed.operation,
            acceptance=acceptance,
            legality_result=legality_result,
            authoritative_outcome="no_commit",
            pre_state_digest=digest,
            post_state_digest=digest,
        ),
    )


def execute_vsm11_request(
    application: MyravantPlayApplication,
    raw_text: str,
) -> VSM11Execution:
    """Execute one bounded storage request through existing INT-3 authority."""

    pre_digest = application.authoritative_digest()
    parsed = parse_vsm11_request(raw_text)
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
            object_entity_id=None,
            container_entity_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class=parsed.failure_class or "vsm11_request_unavailable",
            message="That actor-mediated storage request is outside the bounded VSM-11 route.",
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
            object_entity_id=None,
            container_entity_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class="vsm11_requested_actor_unavailable",
            message="The requested actor is not available.",
        )

    try:
        object_entity_id = application.fixture.resolve_object_reference(
            parsed.object_reference or ""
        )
        container_entity_id = application.fixture.resolve_object_reference(
            parsed.container_reference or ""
        )
    except UnavailableFixtureCustodyError:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            object_entity_id=None,
            container_entity_id=None,
            acceptance="not_accepted",
            legality_result="not_evaluated",
            failure_class="vsm11_storage_target_unavailable",
            message="The requested storage target is not available.",
        )

    if (
        actor_entity_id != GROUNDSKEEPER_ID
        or object_entity_id != LANTERN_ID
        or container_entity_id != TOOL_CHEST_ID
    ):
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm11_fixture_acceptance_refused",
            message="The Groundskeeper does not accept that bounded storage request.",
        )

    if not _actor_present_with_requester(application, actor_entity_id):
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
            acceptance="refused",
            legality_result="not_evaluated",
            failure_class="vsm11_requested_actor_not_local",
            message="The Groundskeeper is not here to receive that request.",
        )

    acceptance = "accepted"
    operation = parsed.operation or ""
    object_carried = _object_carried_by_actor(
        application,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
    )
    object_contained = _object_contained_by(
        application,
        object_entity_id=object_entity_id,
        container_entity_id=container_entity_id,
    )

    desired_already_true = (
        object_contained if operation == "store" else object_carried
    )
    if desired_already_true:
        message = (
            "The Brass Lantern is already in the Tool Chest."
            if operation == "store"
            else "The Groundskeeper already has the Brass Lantern."
        )
        result = PlayApplicationResult(
            result_type="actor_mediated_storage_unchanged",
            message=message,
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=pre_digest,
        )
        return VSM11Execution(
            result=result,
            request_receipt=VSM11RequestReceipt(
                request_id=request_id,
                requester_entity_id=application.fixture.player_entity_id,
                requested_actor_entity_id=actor_entity_id,
                performing_actor_entity_id=actor_entity_id,
                object_entity_id=object_entity_id,
                container_entity_id=container_entity_id,
                requested_operation=operation,
                acceptance=acceptance,
                legality_result="allowed_no_change",
                authoritative_outcome="unchanged",
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            ),
        )

    container_open = application.object_open_state(container_entity_id)
    container_accessible = _container_accessible_to_actor(
        application,
        actor_entity_id=actor_entity_id,
        container_entity_id=container_entity_id,
    )
    placement_available = (
        object_carried if operation == "store" else object_contained
    )
    opportunity_available = bool(
        container_accessible
        and container_open is not None
        and container_open.state == "open"
        and placement_available
    )
    if not opportunity_available:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class="vsm11_int3_opportunity_unavailable",
            message="The Groundskeeper accepts, but cannot currently complete that storage transfer.",
        )

    command_id = application._next_storage_command_id()
    command = create_command_envelope(
        command_id=command_id,
        command_type=(
            "transfer_to_container"
            if operation == "store"
            else "transfer_from_container"
        ),
        source_actor_id=actor_entity_id,
        payload={
            "object_entity_id": object_entity_id,
            "container_entity_id": container_entity_id,
        },
        metadata={
            "client": "myravant-terminal-vsm11",
            "package": VSM11_PACKAGE_ID,
            "request_id": request_id,
            "requester_entity_id": application.fixture.player_entity_id,
            "requested_actor_entity_id": actor_entity_id,
        },
    )
    token = hashlib.sha256(
        (
            f"{request_id}|{command_id}|{actor_entity_id}|{object_entity_id}|"
            f"{container_entity_id}|{operation}"
        ).encode("utf-8")
    ).hexdigest()[:20]
    qualification = create_object_storage_qualification_evidence(
        evidence_id=build_record_id("evidence", f"vsm11-{token}-rt010"),
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        container_entity_id=container_entity_id,
        operation=operation,
        qualified=True,
    )
    opportunity = create_object_storage_opportunity_evidence(
        evidence_id=build_record_id("evidence", f"vsm11-{token}-afqr19"),
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        container_entity_id=container_entity_id,
        operation=operation,
        opportunity_available=True,
        resolution_accepted=True,
    )

    try:
        committed = execute_persistent_world_object_storage(
            state=application.storage_state,
            command=command,
            qualification_evidence=qualification,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=application.representation_digest(),
        )
    except PersistentWorldObjectStorageError as exc:
        return _rejected_execution(
            application,
            request_id=request_id,
            parsed=parsed,
            actor_entity_id=actor_entity_id,
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
            acceptance=acceptance,
            legality_result="rejected",
            failure_class=type(exc).__name__,
            message="The Groundskeeper accepts, but authoritative INT-3 legality rejects the transfer.",
        )

    application._runtime_state = replace_persistent_world_runtime_storage_state(
        state=application.runtime_state,
        storage_state=committed.state,
    )
    post_digest = application.authoritative_digest()
    message = (
        "The Groundskeeper stores the Brass Lantern in the Tool Chest."
        if operation == "store"
        else "The Groundskeeper retrieves the Brass Lantern from the Tool Chest."
    )
    result = PlayApplicationResult(
        result_type="actor_mediated_storage_committed",
        message=message,
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
    return VSM11Execution(
        result=result,
        request_receipt=VSM11RequestReceipt(
            request_id=request_id,
            requester_entity_id=application.fixture.player_entity_id,
            requested_actor_entity_id=actor_entity_id,
            performing_actor_entity_id=actor_entity_id,
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
            requested_operation=operation,
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

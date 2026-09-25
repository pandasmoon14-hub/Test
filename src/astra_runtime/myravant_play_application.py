"""Thin application adapter for the bounded Myravant terminal vertical slice.

The adapter owns session orchestration only. Authoritative movement, custody,
and durable checkpoint behavior remain in the existing R4-C, R4-D, and R4-E
runtime modules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointFormatError,
    restore_persistent_world_checkpoint,
    restore_persistent_world_object_custody_checkpoint,
    restore_persistent_world_object_open_close_checkpoint,
    write_persistent_world_object_open_close_checkpoint,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementRuntimeState,
    digest_persistent_world_entity_location_representation,
    execute_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyError,
    PersistentWorldObjectCustodyRuntimeState,
    create_persistent_world_object_custody_runtime_state,
    execute_persistent_world_object_custody,
    replace_persistent_world_object_custody_movement_state,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenCloseError,
    PersistentWorldObjectOpenCloseRuntimeState,
    PersistentWorldObjectOpenState,
    create_persistent_world_object_open_close_runtime_state,
    digest_persistent_world_object_open_close_runtime_state,
    digest_persistent_world_object_open_states,
    execute_persistent_world_object_open_close,
    object_open_state_for,
    replace_persistent_world_object_open_close_custody_state,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.myravant_play_fixture import (
    MyravantPlayFixture,
    UnavailableFixtureCustodyError,
    UnavailableFixtureMovementError,
    create_terminal_play_fixture,
)


_MOVEMENT_COMMAND_ID_PATTERN = re.compile(r"^terminal-move-(\d{6})$")
_CUSTODY_COMMAND_ID_PATTERN = re.compile(r"^terminal-custody-(\d{6})$")
_OBJECT_STATE_COMMAND_ID_PATTERN = re.compile(r"^terminal-object-state-(\d{6})$")


class MyravantPlayApplicationError(ValueError):
    """Base terminal-play application error."""


class CheckpointPathRequiredError(MyravantPlayApplicationError):
    """Raised when save is requested without a configured checkpoint path."""


@dataclass(frozen=True, kw_only=True)
class PublicLocationView:
    place_id: str
    name: str
    description: str
    exits: tuple[str, ...]
    objects: tuple[str, ...]
    carrying: tuple[str, ...]


@dataclass(frozen=True, kw_only=True)
class PublicInspectionView:
    name: str
    description: str


@dataclass(frozen=True, kw_only=True)
class PlayApplicationResult:
    result_type: str
    message: str
    view: PublicLocationView | PublicInspectionView | None = None
    authoritative_changed: bool = False
    command_id: str | None = None
    command_fingerprint: str | None = None
    preview_id: str | None = None
    receipt_id: str | None = None
    state_delta_id: str | None = None
    spatial_evidence_id: str | None = None
    opportunity_evidence_id: str | None = None
    pre_state_digest: str | None = None
    post_state_digest: str | None = None
    checkpoint_digest: str | None = None
    failure_class: str | None = None
    technical_retry: bool | None = None


class MyravantPlayApplication:
    """Session-scoped holder for one bounded authoritative runtime state."""

    def __init__(
        self,
        *,
        fixture: MyravantPlayFixture,
        object_state: PersistentWorldObjectOpenCloseRuntimeState,
        checkpoint_path: str | Path | None = None,
    ) -> None:
        self.fixture = fixture
        self._object_state = object_state
        self.checkpoint_path = (
            Path(checkpoint_path)
            if checkpoint_path is not None
            else None
        )

    @property
    def state(self) -> PersistentWorldMovementRuntimeState:
        """Compatibility view of the composed R4-C movement state."""

        return self._object_state.custody_state.movement_state

    @property
    def custody_state(self) -> PersistentWorldObjectCustodyRuntimeState:
        return self._object_state.custody_state

    @property
    def object_state(self) -> PersistentWorldObjectOpenCloseRuntimeState:
        return self._object_state

    @classmethod
    def new(
        cls,
        *,
        checkpoint_path: str | Path | None = None,
        fixture: MyravantPlayFixture | None = None,
    ) -> "MyravantPlayApplication":
        bounded_fixture = fixture or create_terminal_play_fixture()
        custody_state = create_persistent_world_object_custody_runtime_state(
            movement_state=bounded_fixture.initial_state
        )
        return cls(
            fixture=bounded_fixture,
            object_state=create_persistent_world_object_open_close_runtime_state(
                custody_state=custody_state,
                object_open_states=bounded_fixture.initial_object_open_states,
            ),
            checkpoint_path=checkpoint_path,
        )

    @classmethod
    def restore(
        cls,
        *,
        checkpoint_path: str | Path,
        fixture: MyravantPlayFixture | None = None,
    ) -> "MyravantPlayApplication":
        bounded_fixture = fixture or create_terminal_play_fixture()

        try:
            object_state = restore_persistent_world_object_open_close_checkpoint(
                checkpoint_path=checkpoint_path,
                expected_campaign_id=bounded_fixture.campaign_id,
                expected_initial_object_states=(
                    bounded_fixture.initial_object_open_states
                ),
            )
        except PersistentWorldCheckpointFormatError:
            try:
                custody_state = (
                    restore_persistent_world_object_custody_checkpoint(
                        checkpoint_path=checkpoint_path,
                        expected_campaign_id=bounded_fixture.campaign_id,
                    )
                )
            except PersistentWorldCheckpointFormatError:
                movement_state = restore_persistent_world_checkpoint(
                    checkpoint_path=checkpoint_path,
                    expected_campaign_id=bounded_fixture.campaign_id,
                )
                custody_state = (
                    create_persistent_world_object_custody_runtime_state(
                        movement_state=movement_state
                    )
                )
            object_state = create_persistent_world_object_open_close_runtime_state(
                custody_state=custody_state,
                object_open_states=bounded_fixture.initial_object_open_states,
            )

        return cls(
            fixture=bounded_fixture,
            object_state=object_state,
            checkpoint_path=checkpoint_path,
        )

    def representation_digest(self) -> str:
        return digest_persistent_world_entity_location_representation(
            self.state.representation
        )

    def object_state_digest(self) -> str:
        return digest_persistent_world_object_open_states(
            self._object_state.object_open_states
        )

    def authoritative_digest(self) -> str:
        return digest_persistent_world_object_open_close_runtime_state(
            self._object_state
        )

    def object_open_state(
        self,
        object_entity_id: str,
    ) -> PersistentWorldObjectOpenState | None:
        return object_open_state_for(self._object_state, object_entity_id)

    def current_place_id(self) -> str:
        matches = [
            relation
            for relation in self.state.representation.relations
            if (
                relation.relation_type == LOCATED_AT_RELATION_TYPE
                and relation.subject_entity_id == self.fixture.player_entity_id
            )
        ]
        if len(matches) != 1:
            raise MyravantPlayApplicationError(
                "bounded player must have exactly one authoritative "
                "current location"
            )
        return matches[0].object_entity_id

    def look(self) -> PlayApplicationResult:
        place_id = self.current_place_id()
        presentation = self.fixture.place_presentation(place_id)
        objects = self.fixture.public_entities_at(
            self.state.representation,
            place_id,
        )
        carrying = self.fixture.public_entities_carried_by(
            self.state.representation,
            self.fixture.player_entity_id,
        )
        view = PublicLocationView(
            place_id=place_id,
            name=presentation.name,
            description=presentation.description,
            exits=self.fixture.exits_from(place_id),
            objects=tuple(item.name for item in objects),
            carrying=tuple(item.name for item in carrying),
        )
        digest = self.authoritative_digest()
        return PlayApplicationResult(
            result_type="look",
            message=presentation.name,
            view=view,
            pre_state_digest=digest,
            post_state_digest=digest,
        )

    def inspect(self, object_reference: str) -> PlayApplicationResult:
        """Return bounded public presentation only for a currently observable object."""

        digest = self.authoritative_digest()
        unavailable = PlayApplicationResult(
            result_type="inspection_unavailable",
            message="You cannot inspect that from the current state.",
            authoritative_changed=False,
            pre_state_digest=digest,
            post_state_digest=digest,
            failure_class="inspection_target_unavailable",
        )

        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
        except UnavailableFixtureCustodyError:
            return unavailable

        place_id = self.current_place_id()
        nearby_ids = {
            item.entity_id
            for item in self.fixture.public_entities_at(
                self.state.representation,
                place_id,
            )
        }
        carried_ids = {
            item.entity_id
            for item in self.fixture.public_entities_carried_by(
                self.state.representation,
                self.fixture.player_entity_id,
            )
        }
        if object_entity_id not in nearby_ids | carried_ids:
            return unavailable

        presentation = self.fixture.object_presentation(object_entity_id)
        description = presentation.description
        open_state = self.object_open_state(object_entity_id)
        if open_state is not None:
            description = "\n".join((
                description,
                self.fixture.public_open_state_description(
                    object_entity_id=object_entity_id,
                    state=open_state.state,
                ),
            ))
        view = PublicInspectionView(
            name=presentation.name,
            description=description,
        )
        return PlayApplicationResult(
            result_type="inspection",
            message=presentation.name,
            view=view,
            authoritative_changed=False,
            pre_state_digest=digest,
            post_state_digest=digest,
        )

    def _next_movement_command_id(self) -> str:
        used = {
            transition.command_id
            for transition in self.state.committed_transitions
        }
        highest = 0
        for command_id in used:
            match = _MOVEMENT_COMMAND_ID_PATTERN.fullmatch(command_id)
            if match:
                highest = max(highest, int(match.group(1)))
        sequence = highest + 1
        while True:
            candidate = f"terminal-move-{sequence:06d}"
            if candidate not in used:
                return candidate
            sequence += 1

    def _next_custody_command_id(self) -> str:
        used = {
            transition.command_id
            for transition in self.custody_state.committed_custody_transitions
        }
        highest = 0
        for command_id in used:
            match = _CUSTODY_COMMAND_ID_PATTERN.fullmatch(command_id)
            if match:
                highest = max(highest, int(match.group(1)))
        sequence = highest + 1
        while True:
            candidate = f"terminal-custody-{sequence:06d}"
            if candidate not in used:
                return candidate
            sequence += 1

    def _next_object_state_command_id(self) -> str:
        used = {
            transition.command_id
            for transition in self._object_state.committed_object_state_transitions
        }
        highest = 0
        for command_id in used:
            match = _OBJECT_STATE_COMMAND_ID_PATTERN.fullmatch(command_id)
            if match:
                highest = max(highest, int(match.group(1)))
        sequence = highest + 1
        while True:
            candidate = f"terminal-object-state-{sequence:06d}"
            if candidate not in used:
                return candidate
            sequence += 1

    def move(self, direction: str) -> PlayApplicationResult:
        normalized = direction.strip().lower()
        pre_digest = self.authoritative_digest()
        pre_representation_digest = self.representation_digest()
        source_place_id = self.current_place_id()

        try:
            destination_place_id = self.fixture.destination_for(
                source_place_id=source_place_id,
                direction=normalized,
            )
        except UnavailableFixtureMovementError:
            return PlayApplicationResult(
                result_type="movement_rejected",
                message="You cannot move that way from here.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="unavailable_fixture_route",
            )

        command_id = self._next_movement_command_id()
        command = create_command_envelope(
            command_id=command_id,
            command_type="move",
            source_actor_id=self.fixture.player_entity_id,
            payload={"destination_entity_id": destination_place_id},
            metadata={"client": "myravant-terminal-g1"},
        )
        spatial_evidence, opportunity_evidence = (
            self.fixture.movement_evidence(
                command_id=command_id,
                source_place_id=source_place_id,
                direction=normalized,
                destination_place_id=destination_place_id,
            )
        )

        result = execute_persistent_world_movement(
            state=self.state,
            command=command,
            spatial_evidence=spatial_evidence,
            opportunity_evidence=opportunity_evidence,
            expected_pre_state_digest=pre_representation_digest,
        )

        updated_custody = (
            replace_persistent_world_object_custody_movement_state(
                state=self.custody_state,
                movement_state=result.state,
            )
        )
        self._object_state = (
            replace_persistent_world_object_open_close_custody_state(
                state=self._object_state,
                custody_state=updated_custody,
            )
        )
        post_digest = self.authoritative_digest()
        destination_name = self.fixture.place_presentation(
            destination_place_id
        ).name

        return PlayApplicationResult(
            result_type="movement_committed",
            message=f"You move to the {destination_name}.",
            authoritative_changed=True,
            command_id=command_id,
            command_fingerprint=result.receipt.command_fingerprint,
            preview_id=result.preview.preview_id,
            receipt_id=result.receipt.receipt_id,
            state_delta_id=result.state_delta.delta_id,
            spatial_evidence_id=result.receipt.spatial_evidence_id,
            opportunity_evidence_id=(
                result.receipt.opportunity_evidence_id
            ),
            pre_state_digest=pre_digest,
            post_state_digest=post_digest,
            technical_retry=result.technical_retry,
        )

    def _object_available_for_operation(
        self,
        *,
        object_entity_id: str,
        operation: str,
    ) -> bool:
        place_id = self.current_place_id()
        relations = self.state.representation.relations

        if operation == "pickup":
            return any(
                relation.relation_type == LOCATED_AT_RELATION_TYPE
                and relation.subject_entity_id == object_entity_id
                and relation.object_entity_id == place_id
                for relation in relations
            )

        return any(
            relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == object_entity_id
            and relation.object_entity_id == self.fixture.player_entity_id
            for relation in relations
        )

    def _custody(
        self,
        *,
        operation: str,
        object_reference: str,
    ) -> PlayApplicationResult:
        pre_digest = self.authoritative_digest()
        pre_representation_digest = self.representation_digest()

        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
        except UnavailableFixtureCustodyError:
            return PlayApplicationResult(
                result_type="custody_rejected",
                message="That object is not available in this bounded fixture.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="unknown_or_ambiguous_fixture_object",
            )

        object_name = self.fixture.entity_name(object_entity_id)
        if not self._object_available_for_operation(
            object_entity_id=object_entity_id,
            operation=operation,
        ):
            action = "pick that up" if operation == "pickup" else "drop that"
            return PlayApplicationResult(
                result_type="custody_rejected",
                message=f"You cannot {action} in the current state.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=f"{operation}_placement_unavailable",
            )

        command_id = self._next_custody_command_id()
        command = create_command_envelope(
            command_id=command_id,
            command_type=f"{operation}_object",
            source_actor_id=self.fixture.player_entity_id,
            payload={"object_entity_id": object_entity_id},
            metadata={"client": "myravant-terminal-g2"},
        )
        qualification_evidence, opportunity_evidence = (
            self.fixture.custody_evidence(
                command_id=command_id,
                object_entity_id=object_entity_id,
                operation=operation,
            )
        )

        try:
            result = execute_persistent_world_object_custody(
                state=self.custody_state,
                command=command,
                qualification_evidence=qualification_evidence,
                opportunity_evidence=opportunity_evidence,
                expected_pre_state_digest=pre_representation_digest,
            )
        except PersistentWorldObjectCustodyError as exc:
            return PlayApplicationResult(
                result_type="custody_rejected",
                message=(
                    "The pickup was rejected by the authoritative runtime."
                    if operation == "pickup"
                    else "The drop was rejected by the authoritative runtime."
                ),
                authoritative_changed=False,
                command_id=command_id,
                opportunity_evidence_id=opportunity_evidence.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=type(exc).__name__,
            )

        self._object_state = (
            replace_persistent_world_object_open_close_custody_state(
                state=self._object_state,
                custody_state=result.state,
            )
        )
        post_digest = self.authoritative_digest()
        verb = "pick up" if operation == "pickup" else "drop"

        return PlayApplicationResult(
            result_type="custody_committed",
            message=f"You {verb} the {object_name}.",
            authoritative_changed=True,
            command_id=command_id,
            command_fingerprint=result.receipt.command_fingerprint,
            preview_id=result.preview.preview_id,
            receipt_id=result.receipt.receipt_id,
            state_delta_id=result.state_delta.delta_id,
            opportunity_evidence_id=(
                result.receipt.opportunity_evidence_id
            ),
            pre_state_digest=pre_digest,
            post_state_digest=post_digest,
            technical_retry=result.technical_retry,
        )

    def _object_currently_available(self, object_entity_id: str) -> bool:
        place_id = self.current_place_id()
        nearby_ids = {
            item.entity_id
            for item in self.fixture.public_entities_at(
                self.state.representation,
                place_id,
            )
        }
        carried_ids = {
            item.entity_id
            for item in self.fixture.public_entities_carried_by(
                self.state.representation,
                self.fixture.player_entity_id,
            )
        }
        return object_entity_id in nearby_ids | carried_ids

    def _object_open_close(
        self,
        *,
        operation: str,
        object_reference: str,
    ) -> PlayApplicationResult:
        pre_digest = self.authoritative_digest()
        unavailable = PlayApplicationResult(
            result_type="object_state_rejected",
            message="You cannot do that to the target from the current state.",
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=pre_digest,
            failure_class="object_state_target_unavailable",
        )

        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
        except UnavailableFixtureCustodyError:
            return unavailable

        if not self._object_currently_available(object_entity_id):
            return unavailable

        current = self.object_open_state(object_entity_id)
        if current is None:
            return PlayApplicationResult(
                result_type="object_state_rejected",
                message="That object does not support this bounded interaction.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="object_state_not_supported",
            )

        desired = "open" if operation == "open" else "closed"
        object_name = self.fixture.entity_name(object_entity_id)
        if current.state == desired:
            return PlayApplicationResult(
                result_type="object_state_unchanged",
                message=f"The {object_name} is already {desired}.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            )

        command_id = self._next_object_state_command_id()
        command = create_command_envelope(
            command_id=command_id,
            command_type=f"{operation}_object",
            source_actor_id=self.fixture.player_entity_id,
            payload={"object_entity_id": object_entity_id},
            metadata={"client": "myravant-terminal-int1"},
        )
        qualification_evidence, opportunity_evidence = (
            self.fixture.object_open_close_evidence(
                command_id=command_id,
                object_entity_id=object_entity_id,
                operation=operation,
            )
        )

        try:
            result = execute_persistent_world_object_open_close(
                state=self._object_state,
                command=command,
                qualification_evidence=qualification_evidence,
                opportunity_evidence=opportunity_evidence,
                expected_pre_state_digest=self.object_state_digest(),
            )
        except PersistentWorldObjectOpenCloseError as exc:
            return PlayApplicationResult(
                result_type="object_state_rejected",
                message="The object-state change was rejected by the authoritative runtime.",
                authoritative_changed=False,
                command_id=command_id,
                opportunity_evidence_id=opportunity_evidence.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=type(exc).__name__,
            )

        self._object_state = result.state
        post_digest = self.authoritative_digest()
        verb = "open" if operation == "open" else "close"
        return PlayApplicationResult(
            result_type="object_state_committed",
            message=f"You {verb} the {object_name}.",
            authoritative_changed=True,
            command_id=command_id,
            command_fingerprint=result.receipt.command_fingerprint,
            preview_id=result.preview.preview_id,
            receipt_id=result.receipt.receipt_id,
            state_delta_id=result.state_delta.delta_id,
            opportunity_evidence_id=result.receipt.opportunity_evidence_id,
            pre_state_digest=pre_digest,
            post_state_digest=post_digest,
            technical_retry=result.technical_retry,
        )

    def open_object(self, object_reference: str) -> PlayApplicationResult:
        return self._object_open_close(
            operation="open",
            object_reference=object_reference,
        )

    def close_object(self, object_reference: str) -> PlayApplicationResult:
        return self._object_open_close(
            operation="close",
            object_reference=object_reference,
        )

    def pickup(self, object_reference: str) -> PlayApplicationResult:
        return self._custody(
            operation="pickup",
            object_reference=object_reference,
        )

    def drop(self, object_reference: str) -> PlayApplicationResult:
        return self._custody(
            operation="drop",
            object_reference=object_reference,
        )

    def save(self) -> PlayApplicationResult:
        if self.checkpoint_path is None:
            raise CheckpointPathRequiredError(
                "save requires --checkpoint or a loaded checkpoint path"
            )

        pre_digest = self.authoritative_digest()
        checkpoint_digest = (
            write_persistent_world_object_open_close_checkpoint(
                state=self._object_state,
                checkpoint_path=self.checkpoint_path,
                qualification_evidence=self.fixture.checkpoint_qualification,
            )
        )
        post_digest = self.authoritative_digest()

        return PlayApplicationResult(
            result_type="checkpoint_written",
            message="Checkpoint written.",
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=post_digest,
            checkpoint_digest=checkpoint_digest,
        )

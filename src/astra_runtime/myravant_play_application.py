"""Thin application adapter for the bounded Myravant terminal vertical slice.

The adapter owns session orchestration only. Authoritative movement, custody,
and durable checkpoint behavior remain in the existing R4-C, R4-D, and R4-E
runtime modules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from astra_runtime.domain.persistent_world_component_checkpoint import (
    restore_persistent_world_component_checkpoint,
    write_persistent_world_component_checkpoint,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    PersistentWorldRuntimeComposition,
    compose_persistent_world_custody_state,
    compose_persistent_world_lit_state,
    compose_persistent_world_open_close_state,
    compose_persistent_world_storage_state,
    create_persistent_world_runtime_composition,
    create_persistent_world_runtime_composition_from_storage_state,
    replace_persistent_world_runtime_custody_state,
    replace_persistent_world_runtime_lit_state,
    replace_persistent_world_runtime_movement_state,
    replace_persistent_world_runtime_open_close_state,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    CONTAINED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointFormatError,
    restore_persistent_world_checkpoint,
    restore_persistent_world_object_custody_checkpoint,
    restore_persistent_world_object_open_close_checkpoint,
    restore_persistent_world_object_lit_state_checkpoint,
    restore_persistent_world_object_storage_checkpoint,
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
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    PersistentWorldObjectLitRuntimeState,
    PersistentWorldObjectLitState,
    PersistentWorldObjectLitStateError,
    create_persistent_world_object_lit_runtime_state,
    digest_persistent_world_object_lit_runtime_state,
    digest_persistent_world_object_lit_states,
    execute_persistent_world_object_lit_state,
    object_lit_state_for,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    PersistentWorldObjectStorageError,
    PersistentWorldObjectStorageRuntimeState,
    containment_relation_for,
    create_persistent_world_object_storage_runtime_state,
    digest_persistent_world_object_storage_runtime_state,
    execute_persistent_world_object_storage,
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
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID,
    MyravantPlayFixture,
    UnavailableFixtureCustodyError,
    UnavailableFixtureMovementError,
    create_terminal_play_fixture,
)


_MOVEMENT_COMMAND_ID_PATTERN = re.compile(r"^terminal-move-(\d{6})$")
_CUSTODY_COMMAND_ID_PATTERN = re.compile(r"^terminal-custody-(\d{6})$")
_OBJECT_STATE_COMMAND_ID_PATTERN = re.compile(r"^terminal-object-state-(\d{6})$")
_OBJECT_LIT_STATE_COMMAND_ID_PATTERN = re.compile(r"^terminal-object-lit-state-(\d{6})$")
_STORAGE_COMMAND_ID_PATTERN = re.compile(r"^terminal-storage-(\d{6})$")


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
    observation_evidence_id: str | None = None
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
        runtime_state: PersistentWorldRuntimeComposition | None = None,
        storage_state: PersistentWorldObjectStorageRuntimeState | None = None,
        checkpoint_path: str | Path | None = None,
    ) -> None:
        if (runtime_state is None) == (storage_state is None):
            raise MyravantPlayApplicationError(
                "exactly one of runtime_state or storage_state is required"
            )
        self.fixture = fixture
        self._runtime_state = (
            runtime_state
            if runtime_state is not None
            else create_persistent_world_runtime_composition_from_storage_state(
                storage_state
            )
        )
        self.checkpoint_path = (
            Path(checkpoint_path)
            if checkpoint_path is not None
            else None
        )

    @property
    def runtime_state(self) -> PersistentWorldRuntimeComposition:
        return self._runtime_state

    @property
    def _lit_state(self) -> PersistentWorldObjectLitRuntimeState:
        return compose_persistent_world_lit_state(self._runtime_state)

    @_lit_state.setter
    def _lit_state(self, value: PersistentWorldObjectLitRuntimeState) -> None:
        self._runtime_state = replace_persistent_world_runtime_lit_state(
            state=self._runtime_state,
            lit_state=value,
        )

    @property
    def storage_state(self) -> PersistentWorldObjectStorageRuntimeState:
        return compose_persistent_world_storage_state(self._runtime_state)

    @property
    def state(self) -> PersistentWorldMovementRuntimeState:
        """Compatibility view of the composed R4-C movement state."""

        return self._runtime_state.movement_state

    @property
    def custody_state(self) -> PersistentWorldObjectCustodyRuntimeState:
        return compose_persistent_world_custody_state(self._runtime_state)

    @property
    def object_state(self) -> PersistentWorldObjectOpenCloseRuntimeState:
        return compose_persistent_world_open_close_state(self._runtime_state)

    @property
    def lit_state(self) -> PersistentWorldObjectLitRuntimeState:
        return compose_persistent_world_lit_state(self._runtime_state)

    @classmethod
    def new(
        cls,
        *,
        checkpoint_path: str | Path | None = None,
        fixture: MyravantPlayFixture | None = None,
    ) -> "MyravantPlayApplication":
        bounded_fixture = fixture or create_terminal_play_fixture()
        return cls(
            fixture=bounded_fixture,
            runtime_state=create_persistent_world_runtime_composition(
                movement_state=bounded_fixture.initial_state,
                object_open_states=bounded_fixture.initial_object_open_states,
                object_lit_states=bounded_fixture.initial_object_lit_states,
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
            storage_state = restore_persistent_world_component_checkpoint(
                checkpoint_path=checkpoint_path,
                expected_campaign_id=bounded_fixture.campaign_id,
                expected_initial_open_states=bounded_fixture.initial_object_open_states,
                expected_initial_lit_states=bounded_fixture.initial_object_lit_states,
                expected_initial_representation_digest=(
                    bounded_fixture.provenance.initial_state_digest
                ),
            )
        except PersistentWorldCheckpointFormatError:
            try:
                storage_state = restore_persistent_world_object_storage_checkpoint(
                    checkpoint_path=checkpoint_path,
                    expected_campaign_id=bounded_fixture.campaign_id,
                    expected_initial_open_states=bounded_fixture.initial_object_open_states,
                    expected_initial_lit_states=bounded_fixture.initial_object_lit_states,
                    expected_initial_representation_digest=(
                        bounded_fixture.provenance.initial_state_digest
                    ),
                )
            except PersistentWorldCheckpointFormatError:
                try:
                    lit_state = restore_persistent_world_object_lit_state_checkpoint(
                        checkpoint_path=checkpoint_path,
                        expected_campaign_id=bounded_fixture.campaign_id,
                        expected_initial_open_states=bounded_fixture.initial_object_open_states,
                        expected_initial_lit_states=bounded_fixture.initial_object_lit_states,
                    )
                except PersistentWorldCheckpointFormatError:
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
                            custody_state = restore_persistent_world_object_custody_checkpoint(
                                checkpoint_path=checkpoint_path,
                                expected_campaign_id=bounded_fixture.campaign_id,
                            )
                        except PersistentWorldCheckpointFormatError:
                            movement_state = restore_persistent_world_checkpoint(
                                checkpoint_path=checkpoint_path,
                                expected_campaign_id=bounded_fixture.campaign_id,
                            )
                            custody_state = create_persistent_world_object_custody_runtime_state(
                                movement_state=movement_state
                            )
                        object_state = create_persistent_world_object_open_close_runtime_state(
                            custody_state=custody_state,
                            object_open_states=bounded_fixture.initial_object_open_states,
                        )
                    lit_state = create_persistent_world_object_lit_runtime_state(
                        open_close_state=object_state,
                        object_lit_states=bounded_fixture.initial_object_lit_states,
                    )
                storage_state = create_persistent_world_object_storage_runtime_state(
                    lit_state=lit_state,
                )

        return cls(
            fixture=bounded_fixture,
            runtime_state=(
                create_persistent_world_runtime_composition_from_storage_state(
                    storage_state
                )
            ),
            checkpoint_path=checkpoint_path,
        )

    def representation_digest(self) -> str:
        return digest_persistent_world_entity_location_representation(
            self.state.representation
        )

    def object_state_digest(self) -> str:
        return digest_persistent_world_object_open_states(
            self.object_state.object_open_states
        )

    def object_lit_state_digest(self) -> str:
        return digest_persistent_world_object_lit_states(
            self._lit_state.object_lit_states
        )

    def authoritative_digest(self) -> str:
        return digest_persistent_world_object_storage_runtime_state(
            self.storage_state
        )

    def object_open_state(
        self,
        object_entity_id: str,
    ) -> PersistentWorldObjectOpenState | None:
        return object_open_state_for(self.object_state, object_entity_id)

    def object_lit_state(
        self,
        object_entity_id: str,
    ) -> PersistentWorldObjectLitState | None:
        return object_lit_state_for(self._lit_state, object_entity_id)

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
        candidates = self.fixture.public_entities_at(
            self.state.representation,
            place_id,
        )
        objects = tuple(
            item
            for item in candidates
            if self._object_currently_observable(item.entity_id)
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

        if not self._object_currently_available(object_entity_id):
            return unavailable
        if not self._object_currently_observable(object_entity_id):
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
        lit_state = self.object_lit_state(object_entity_id)
        if lit_state is not None:
            description = "\n".join((
                description,
                self.fixture.public_lit_state_description(
                    object_entity_id=object_entity_id,
                    state=lit_state.state,
                ),
            ))
        if open_state is not None and open_state.state == "open":
            contents = self.fixture.public_entities_contained_by(
                self.state.representation,
                object_entity_id,
            )
            if contents:
                description = "\n".join((
                    description,
                    "Inside: " + ", ".join(item.name for item in contents) + ".",
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
            for transition in self.object_state.committed_object_state_transitions
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

    def _next_storage_command_id(self) -> str:
        used = {
            transition.command_id
            for transition in self._storage_state.committed_storage_transitions
        }
        highest = 0
        for command_id in used:
            match = _STORAGE_COMMAND_ID_PATTERN.fullmatch(command_id)
            if match:
                highest = max(highest, int(match.group(1)))
        sequence = highest + 1
        while True:
            candidate = f"terminal-storage-{sequence:06d}"
            if candidate not in used:
                return candidate
            sequence += 1

    def _next_object_lit_state_command_id(self) -> str:
        used = {
            transition.command_id
            for transition in self._lit_state.committed_object_lit_transitions
        }
        highest = 0
        for command_id in used:
            match = _OBJECT_LIT_STATE_COMMAND_ID_PATTERN.fullmatch(command_id)
            if match:
                highest = max(highest, int(match.group(1)))
        sequence = highest + 1
        while True:
            candidate = f"terminal-object-lit-state-{sequence:06d}"
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
        updated_open_close = replace_persistent_world_object_open_close_custody_state(
            state=self.object_state,
            custody_state=updated_custody,
        )
        self._lit_state = replace_persistent_world_object_lit_open_close_state(
            state=self._lit_state,
            open_close_state=updated_open_close,
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
        pickup_unavailable_message = "You cannot pick that up in the current state."

        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
        except UnavailableFixtureCustodyError:
            return PlayApplicationResult(
                result_type="custody_rejected",
                message=(
                    pickup_unavailable_message
                    if operation == "pickup"
                    else "That object is not available in this bounded fixture."
                ),
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
                message=(
                    pickup_unavailable_message
                    if operation == "pickup"
                    else f"You cannot {action} in the current state."
                ),
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=f"{operation}_placement_unavailable",
            )

        pickup_observation_evidence = (
            self.visual_observation_evidence(object_entity_id)
            if operation == "pickup"
            else None
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
                pickup_observation_evidence=pickup_observation_evidence,
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
                    pickup_unavailable_message
                    if operation == "pickup"
                    else "The drop was rejected by the authoritative runtime."
                ),
                authoritative_changed=False,
                command_id=command_id,
                observation_evidence_id=(
                    pickup_observation_evidence.evidence_id
                    if pickup_observation_evidence is not None
                    else None
                ),
                opportunity_evidence_id=opportunity_evidence.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=type(exc).__name__,
            )

        updated_open_close = replace_persistent_world_object_open_close_custody_state(
            state=self.object_state,
            custody_state=result.state,
        )
        self._lit_state = replace_persistent_world_object_lit_open_close_state(
            state=self._lit_state,
            open_close_state=updated_open_close,
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
            observation_evidence_id=(
                pickup_observation_evidence.evidence_id
                if pickup_observation_evidence is not None
                else None
            ),
            opportunity_evidence_id=(
                result.receipt.opportunity_evidence_id
            ),
            pre_state_digest=pre_digest,
            post_state_digest=post_digest,
            technical_retry=result.technical_retry,
        )

    def _container_accessible(self, container_entity_id: str) -> bool:
        place_id = self.current_place_id()
        relations = self.state.representation.relations
        direct = any(
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == container_entity_id
            and relation.object_entity_id == place_id
            for relation in relations
        )
        carried = any(
            relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == container_entity_id
            and relation.object_entity_id == self.fixture.player_entity_id
            for relation in relations
        )
        nested = any(
            relation.relation_type == CONTAINED_BY_RELATION_TYPE
            and relation.subject_entity_id == container_entity_id
            for relation in relations
        )
        return (direct or carried) and not nested

    def _contained_object_accessible(self, object_entity_id: str) -> bool:
        relation = containment_relation_for(
            self._storage_state,
            object_entity_id,
        )
        if relation is None or not self._container_accessible(relation.object_entity_id):
            return False
        open_state = self.object_open_state(relation.object_entity_id)
        return open_state is not None and open_state.state == "open"

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
        return (
            object_entity_id in nearby_ids | carried_ids
            or self._contained_object_accessible(object_entity_id)
        )

    def _bounded_local_light_available(self) -> bool:
        """Return whether the existing lit lantern exposes local visual signal."""

        lantern_state = self.object_lit_state(LANTERN_ID)
        if lantern_state is None or lantern_state.state != "lit":
            return False

        place_id = self.current_place_id()
        relations = self.state.representation.relations
        if any(
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == LANTERN_ID
            and relation.object_entity_id == place_id
            for relation in relations
        ):
            return True
        if any(
            relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == LANTERN_ID
            and relation.object_entity_id == self.fixture.player_entity_id
            for relation in relations
        ):
            return True

        containment = containment_relation_for(
            self._storage_state,
            LANTERN_ID,
        )
        if containment is None:
            return False
        if not self._container_accessible(containment.object_entity_id):
            return False
        open_state = self.object_open_state(containment.object_entity_id)
        return open_state is not None and open_state.state == "open"

    def visual_observation_evidence(self, object_entity_id: str):
        """Expose deterministic derived sensing evidence for evaluation only."""

        return self.fixture.visual_observation_evidence(
            observer_entity_id=self.fixture.player_entity_id,
            target_entity_id=object_entity_id,
            place_id=self.current_place_id(),
            local_light_available=self._bounded_local_light_available(),
        )

    def _object_currently_observable(self, object_entity_id: str) -> bool:
        return self.visual_observation_evidence(object_entity_id).observable

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
                state=self.object_state,
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

        self._lit_state = replace_persistent_world_object_lit_open_close_state(
            state=self._lit_state,
            open_close_state=result.state,
        )
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

    def _object_lit_state(
        self,
        *,
        operation: str,
        object_reference: str,
    ) -> PlayApplicationResult:
        pre_digest = self.authoritative_digest()
        unavailable = PlayApplicationResult(
            result_type="object_lit_state_rejected",
            message="You cannot do that to the target from the current state.",
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=pre_digest,
            failure_class="object_lit_state_target_unavailable",
        )

        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
        except UnavailableFixtureCustodyError:
            return unavailable

        if not self._object_currently_available(object_entity_id):
            return unavailable

        current = self.object_lit_state(object_entity_id)
        if current is None:
            return PlayApplicationResult(
                result_type="object_lit_state_rejected",
                message="That object does not support this bounded interaction.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="object_lit_state_not_supported",
            )

        desired = "lit" if operation == "light" else "unlit"
        object_name = self.fixture.entity_name(object_entity_id)
        if current.state == desired:
            return PlayApplicationResult(
                result_type="object_lit_state_unchanged",
                message=f"The {object_name} is already {desired}.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            )

        command_id = self._next_object_lit_state_command_id()
        command = create_command_envelope(
            command_id=command_id,
            command_type="activate_object_lit_state",
            source_actor_id=self.fixture.player_entity_id,
            payload={
                "object_entity_id": object_entity_id,
                "operation": operation,
            },
            metadata={"client": "myravant-terminal-int2"},
        )
        qualification_evidence, opportunity_evidence = (
            self.fixture.object_lit_state_evidence(
                command_id=command_id,
                object_entity_id=object_entity_id,
                operation=operation,
            )
        )

        try:
            result = execute_persistent_world_object_lit_state(
                state=self._lit_state,
                command=command,
                qualification_evidence=qualification_evidence,
                opportunity_evidence=opportunity_evidence,
                expected_pre_state_digest=self.object_lit_state_digest(),
            )
        except PersistentWorldObjectLitStateError as exc:
            return PlayApplicationResult(
                result_type="object_lit_state_rejected",
                message="The object lit-state change was rejected by the authoritative runtime.",
                authoritative_changed=False,
                command_id=command_id,
                opportunity_evidence_id=opportunity_evidence.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=type(exc).__name__,
            )

        self._lit_state = result.state
        post_digest = self.authoritative_digest()
        verb = "light" if operation == "light" else "extinguish"
        return PlayApplicationResult(
            result_type="object_lit_state_committed",
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

    def _storage(
        self,
        *,
        operation: str,
        object_reference: str,
        container_reference: str,
    ) -> PlayApplicationResult:
        pre_digest = self.authoritative_digest()
        unavailable = PlayApplicationResult(
            result_type="storage_rejected",
            message="You cannot do that to the target from the current state.",
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=pre_digest,
            failure_class="storage_target_unavailable",
        )
        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
            container_entity_id = self.fixture.resolve_object_reference(
                container_reference
            )
        except UnavailableFixtureCustodyError:
            return unavailable

        if not self.fixture.storage_pair_supported(
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
        ):
            if (
                self._object_currently_available(object_entity_id)
                and self._object_currently_available(container_entity_id)
            ):
                return PlayApplicationResult(
                    result_type="storage_rejected",
                    message="Those objects do not support this bounded storage interaction.",
                    authoritative_changed=False,
                    pre_state_digest=pre_digest,
                    post_state_digest=pre_digest,
                    failure_class="storage_not_supported",
                )
            return unavailable

        relation = containment_relation_for(
            self._storage_state,
            object_entity_id,
        )
        if (
            operation == "store"
            and relation is not None
            and relation.object_entity_id == container_entity_id
        ):
            return PlayApplicationResult(
                result_type="storage_unchanged",
                message="The object is already stored there.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            )

        if not self._container_accessible(container_entity_id):
            return unavailable
        open_state = self.object_open_state(container_entity_id)
        if open_state is None:
            return PlayApplicationResult(
                result_type="storage_rejected",
                message="That object does not support this bounded storage interaction.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="storage_not_supported",
            )
        if open_state.state != "open":
            return PlayApplicationResult(
                result_type="storage_rejected",
                message="The container must be open first.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="storage_container_closed",
            )

        if operation == "store":
            available = any(
                relation.relation_type == CARRIED_BY_RELATION_TYPE
                and relation.subject_entity_id == object_entity_id
                and relation.object_entity_id == self.fixture.player_entity_id
                for relation in self.state.representation.relations
            )
        else:
            available = (
                relation is not None
                and relation.object_entity_id == container_entity_id
            )
        if not available:
            return unavailable

        command_id = self._next_storage_command_id()
        command = create_command_envelope(
            command_id=command_id,
            command_type=(
                "transfer_to_container"
                if operation == "store"
                else "transfer_from_container"
            ),
            source_actor_id=self.fixture.player_entity_id,
            payload={
                "object_entity_id": object_entity_id,
                "container_entity_id": container_entity_id,
            },
            metadata={"client": "myravant-terminal-int3"},
        )
        qualification, opportunity = self.fixture.object_storage_evidence(
            command_id=command_id,
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
            operation=operation,
        )
        try:
            result = execute_persistent_world_object_storage(
                state=self._storage_state,
                command=command,
                qualification_evidence=qualification,
                opportunity_evidence=opportunity,
                expected_pre_state_digest=self.representation_digest(),
            )
        except PersistentWorldObjectStorageError as exc:
            return PlayApplicationResult(
                result_type="storage_rejected",
                message="The storage transfer was rejected by the authoritative runtime.",
                authoritative_changed=False,
                command_id=command_id,
                opportunity_evidence_id=opportunity.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=type(exc).__name__,
            )

        self._storage_state = result.state
        object_name = self.fixture.entity_name(object_entity_id)
        container_name = self.fixture.entity_name(container_entity_id)
        message = (
            f"You store the {object_name} in the {container_name}."
            if operation == "store"
            else f"You retrieve the {object_name} from the {container_name}."
        )
        return PlayApplicationResult(
            result_type="storage_committed",
            message=message,
            authoritative_changed=True,
            command_id=command_id,
            command_fingerprint=result.receipt.command_fingerprint,
            preview_id=result.preview.preview_id,
            receipt_id=result.receipt.receipt_id,
            state_delta_id=result.state_delta.delta_id,
            opportunity_evidence_id=result.receipt.opportunity_evidence_id,
            pre_state_digest=pre_digest,
            post_state_digest=self.authoritative_digest(),
            technical_retry=result.technical_retry,
        )

    def store_object(
        self,
        object_reference: str,
        container_reference: str,
    ) -> PlayApplicationResult:
        return self._storage(
            operation="store",
            object_reference=object_reference,
            container_reference=container_reference,
        )

    def retrieve_object(
        self,
        object_reference: str,
        container_reference: str,
    ) -> PlayApplicationResult:
        return self._storage(
            operation="retrieve",
            object_reference=object_reference,
            container_reference=container_reference,
        )

    def light_object(self, object_reference: str) -> PlayApplicationResult:
        return self._object_lit_state(
            operation="light",
            object_reference=object_reference,
        )

    def extinguish_object(self, object_reference: str) -> PlayApplicationResult:
        return self._object_lit_state(
            operation="extinguish",
            object_reference=object_reference,
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
        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
        except UnavailableFixtureCustodyError:
            return self._custody(
                operation="pickup",
                object_reference=object_reference,
            )
        relation = containment_relation_for(
            self._storage_state,
            object_entity_id,
        )
        if relation is not None and self._contained_object_accessible(object_entity_id):
            return self._storage(
                operation="retrieve",
                object_reference=object_reference,
                container_reference=self.fixture.entity_name(
                    relation.object_entity_id
                ),
            )
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
            write_persistent_world_component_checkpoint(
                state=self._storage_state,
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

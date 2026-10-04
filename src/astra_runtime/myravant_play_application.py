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
    restore_persistent_world_vsm6_checkpoint,
    restore_persistent_world_comp3_checkpoint,
    restore_persistent_world_component_checkpoint,
    restore_persistent_world_world1_checkpoint,
    write_persistent_world_vsm6_checkpoint,
    write_persistent_world_comp3_checkpoint,
    write_persistent_world_world1_checkpoint,
)
from astra_runtime.domain.persistent_world_logical_time import (
    PersistentWorldLogicalTimeError,
    WORLD1_SCHEDULER_PROFILE_ID,
    commit_prepared_persistent_world_logical_time,
    digest_persistent_world_logical_time_state,
    prepare_persistent_world_logical_time,
)
from astra_runtime.domain.persistent_world_actor_object_handoff import (
    PersistentWorldActorObjectHandoffError,
    PersistentWorldActorObjectHandoffRuntimeState,
    execute_persistent_world_actor_object_handoff,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    PersistentWorldRuntimeComposition,
    compose_persistent_world_actor_object_handoff_state,
    compose_persistent_world_custody_state,
    compose_persistent_world_lit_state,
    compose_persistent_world_object_displacement_state,
    compose_persistent_world_open_close_state,
    compose_persistent_world_storage_state,
    create_persistent_world_runtime_composition,
    create_persistent_world_runtime_composition_from_storage_state,
    digest_persistent_world_runtime_composition,
    replace_persistent_world_runtime_actor_object_handoff_state,
    replace_persistent_world_runtime_custody_state,
    replace_persistent_world_runtime_displacement_state,
    replace_persistent_world_runtime_lit_state,
    replace_persistent_world_runtime_logical_time_state,
    replace_persistent_world_runtime_movement_state,
    replace_persistent_world_runtime_open_close_state,
    replace_persistent_world_runtime_storage_state,
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
    PersistentWorldMovementIntegrationError,
    PersistentWorldMovementRuntimeState,
    digest_persistent_world_entity_location_representation,
    execute_persistent_world_movement,
    prepare_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_world_advancement import (
    PersistentWorldWorldAdvancementError,
    commit_prepared_persistent_world_world_advancement,
    commit_prepared_persistent_world_world_interaction_advancement,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyError,
    PersistentWorldObjectCustodyRuntimeState,
    create_persistent_world_object_custody_runtime_state,
    execute_persistent_world_object_custody,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    PersistentWorldObjectDisplacementError,
    PersistentWorldObjectDisplacementRuntimeState,
    execute_persistent_world_object_displacement,
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
    persistent_world_object_open_close_opportunity_available,
    prepare_persistent_world_object_open_close,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    TOOL_CHEST_ID,
    YARD_ID,
    MyravantPlayFixture,
    UnavailableFixtureCustodyError,
    UnavailableFixtureDisplacementError,
    UnavailableFixtureHandoffError,
    UnavailableFixtureMovementError,
    UnavailableFixtureObservationError,
    create_terminal_play_fixture,
)


_MOVEMENT_COMMAND_ID_PATTERN = re.compile(r"^terminal-move-(\d{6})$")
_CUSTODY_COMMAND_ID_PATTERN = re.compile(r"^terminal-custody-(\d{6})$")
_OBJECT_STATE_COMMAND_ID_PATTERN = re.compile(r"^terminal-object-state-(\d{6})$")
_OBJECT_LIT_STATE_COMMAND_ID_PATTERN = re.compile(r"^terminal-object-lit-state-(\d{6})$")
_STORAGE_COMMAND_ID_PATTERN = re.compile(r"^terminal-storage-(\d{6})$")
_DISPLACEMENT_COMMAND_ID_PATTERN = re.compile(
    r"^terminal-object-displacement-(\d{6})$"
)
_HANDOFF_COMMAND_ID_PATTERN = re.compile(
    r"^terminal-actor-object-handoff-(\d{6})$"
)
_TIME_COMMAND_ID_PATTERN = re.compile(r"^terminal-time-(\d{6})$")
WORLD2_ROUTINE_PROFILE_ID = (
    "myravant:world2:groundskeeper-yard-chest-routine:v1"
)


class MyravantPlayApplicationError(ValueError):
    """Base terminal-play application error."""


class CheckpointPathRequiredError(MyravantPlayApplicationError):
    """Raised when save is requested without a configured checkpoint path."""


@dataclass(frozen=True, kw_only=True)
class PublicObservationFact:
    entity_id: str
    entity_kind: str
    name: str
    description: str
    open_state: str | None = None
    lit_state: str | None = None
    visible_contents: tuple[str, ...] = ()
    carrier_name: str | None = None


@dataclass(frozen=True, kw_only=True)
class PublicLocationView:
    place_id: str
    name: str
    description: str
    exits: tuple[str, ...]
    objects: tuple[str, ...]
    actors: tuple[str, ...]
    carrying: tuple[str, ...]
    observation_facts: tuple[PublicObservationFact, ...] = ()


@dataclass(frozen=True, kw_only=True)
class PublicDirectionalObservationView:
    source_place_id: str
    direction: str
    target_place_id: str
    name: str
    description: str


@dataclass(frozen=True, kw_only=True)
class PublicInspectionView:
    name: str
    description: str
    observation_fact: PublicObservationFact | None = None


@dataclass(frozen=True, kw_only=True)
class PlayApplicationResult:
    result_type: str
    message: str
    view: (
        PublicLocationView
        | PublicDirectionalObservationView
        | PublicInspectionView
        | None
    ) = None
    authoritative_changed: bool = False
    command_id: str | None = None
    command_fingerprint: str | None = None
    preview_id: str | None = None
    receipt_id: str | None = None
    state_delta_id: str | None = None
    spatial_evidence_id: str | None = None
    observation_evidence_id: str | None = None
    opportunity_evidence_id: str | None = None
    due_process_ref: str | None = None
    consequence_receipt_id: str | None = None
    consequence_state_delta_id: str | None = None
    world_event_class: str | None = None
    world_process_actor_id: str | None = None
    world_process_action: str | None = None
    world_process_target_id: str | None = None
    world_process_command_id: str | None = None
    world_process_outcome: str | None = None
    logical_time_before: int | None = None
    logical_time_after: int | None = None
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
    def displacement_state(
        self,
    ) -> PersistentWorldObjectDisplacementRuntimeState:
        return compose_persistent_world_object_displacement_state(
            self._runtime_state
        )

    @property
    def handoff_state(
        self,
    ) -> PersistentWorldActorObjectHandoffRuntimeState:
        return compose_persistent_world_actor_object_handoff_state(
            self._runtime_state
        )

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
            runtime_state = restore_persistent_world_vsm6_checkpoint(
                checkpoint_path=checkpoint_path,
                expected_campaign_id=bounded_fixture.campaign_id,
                expected_initial_open_states=(
                    bounded_fixture.initial_object_open_states
                ),
                expected_initial_lit_states=(
                    bounded_fixture.initial_object_lit_states
                ),
                expected_initial_representation=(
                    bounded_fixture.initial_state.representation
                ),
                expected_initial_representation_digest=(
                    bounded_fixture.provenance.initial_state_digest
                ),
            )
        except PersistentWorldCheckpointFormatError:
            runtime_state = None
        if runtime_state is not None:
            return cls(
                fixture=bounded_fixture,
                runtime_state=runtime_state,
                checkpoint_path=checkpoint_path,
            )

        try:
            runtime_state = restore_persistent_world_comp3_checkpoint(
                checkpoint_path=checkpoint_path,
                expected_campaign_id=bounded_fixture.campaign_id,
                expected_initial_open_states=(
                    bounded_fixture.initial_object_open_states
                ),
                expected_initial_lit_states=(
                    bounded_fixture.initial_object_lit_states
                ),
                expected_initial_representation=(
                    bounded_fixture.initial_state.representation
                ),
                expected_initial_representation_digest=(
                    bounded_fixture.provenance.initial_state_digest
                ),
            )
        except PersistentWorldCheckpointFormatError:
            runtime_state = None
        if runtime_state is not None:
            return cls(
                fixture=bounded_fixture,
                runtime_state=runtime_state,
                checkpoint_path=checkpoint_path,
            )

        try:
            runtime_state = restore_persistent_world_world1_checkpoint(
                checkpoint_path=checkpoint_path,
                expected_campaign_id=bounded_fixture.campaign_id,
                expected_initial_open_states=(
                    bounded_fixture.initial_object_open_states
                ),
                expected_initial_lit_states=(
                    bounded_fixture.initial_object_lit_states
                ),
                expected_initial_representation_digest=(
                    bounded_fixture.provenance.initial_state_digest
                ),
            )
        except PersistentWorldCheckpointFormatError:
            runtime_state = None
        if runtime_state is not None:
            return cls(
                fixture=bounded_fixture,
                runtime_state=runtime_state,
                checkpoint_path=checkpoint_path,
            )

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

    def storage_world_digest(self) -> str:
        return digest_persistent_world_object_storage_runtime_state(
            self.storage_state
        )

    def authoritative_digest(self) -> str:
        return digest_persistent_world_runtime_composition(
            self._runtime_state
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

    def entity_place_id(self, entity_id: str) -> str:
        matches = [
            relation
            for relation in self.state.representation.relations
            if (
                relation.relation_type == LOCATED_AT_RELATION_TYPE
                and relation.subject_entity_id == entity_id
            )
        ]
        if len(matches) != 1:
            raise MyravantPlayApplicationError(
                "bounded character/creature must have exactly one "
                "authoritative current location"
            )
        return matches[0].object_entity_id

    def current_place_id(self) -> str:
        return self.entity_place_id(self.fixture.player_entity_id)

    def _public_observation_fact(
        self,
        entity_id: str,
    ) -> PublicObservationFact | None:
        object_ids = {
            item.entity_id
            for item in self.fixture.object_presentations
        }
        actor_ids = {
            item.entity_id
            for item in self.fixture.actor_presentations
        }

        if entity_id in object_ids:
            if not self._object_locally_present(entity_id):
                return None
            if not self._object_currently_observable(entity_id):
                return None

            presentation = self.fixture.object_presentation(entity_id)
            open_state = self.object_open_state(entity_id)
            lit_state = self.object_lit_state(entity_id)
            visible_contents: tuple[str, ...] = ()
            if open_state is not None and open_state.state == "open":
                visible_contents = tuple(
                    item.name
                    for item in self.fixture.public_entities_contained_by(
                        self.state.representation,
                        entity_id,
                    )
                )
            carrier_entity_id = self._object_carrier_entity_id(entity_id)
            return PublicObservationFact(
                entity_id=entity_id,
                entity_kind="object",
                name=presentation.name,
                description=presentation.description,
                open_state=(
                    open_state.state
                    if open_state is not None
                    else None
                ),
                lit_state=(
                    lit_state.state
                    if lit_state is not None
                    else None
                ),
                visible_contents=visible_contents,
                carrier_name=(
                    self.fixture.entity_name(carrier_entity_id)
                    if carrier_entity_id is not None
                    else None
                ),
            )

        if entity_id in actor_ids:
            if self.entity_place_id(entity_id) != self.current_place_id():
                return None
            if not self.visual_observation_evidence(entity_id).observable:
                return None

            presentation = self.fixture.actor_presentation(entity_id)
            return PublicObservationFact(
                entity_id=entity_id,
                entity_kind="actor",
                name=presentation.name,
                description=presentation.description,
            )

        return None

    def _inspection_description_from_fact(
        self,
        fact: PublicObservationFact,
    ) -> str:
        lines = [fact.description]
        if fact.entity_kind == "object":
            if fact.open_state is not None:
                lines.append(
                    self.fixture.public_open_state_description(
                        object_entity_id=fact.entity_id,
                        state=fact.open_state,
                    )
                )
            if fact.lit_state is not None:
                lines.append(
                    self.fixture.public_lit_state_description(
                        object_entity_id=fact.entity_id,
                        state=fact.lit_state,
                    )
                )
            if fact.visible_contents:
                lines.append(
                    "Inside: " + ", ".join(fact.visible_contents) + "."
                )
            if fact.carrier_name is not None:
                lines.append(f"Carried by {fact.carrier_name}.")
        return "\n".join(lines)

    def look(self) -> PlayApplicationResult:
        place_id = self.current_place_id()
        presentation = self.fixture.place_presentation(place_id)

        object_facts = tuple(
            fact
            for item in self._public_location_objects(place_id)
            if (
                fact := self._public_observation_fact(item.entity_id)
            ) is not None
        )
        actor_facts = tuple(
            fact
            for item in self.fixture.public_actors_at(
                self.state.representation,
                place_id,
            )
            if (
                fact := self._public_observation_fact(item.entity_id)
            ) is not None
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
            objects=tuple(fact.name for fact in object_facts),
            actors=tuple(fact.name for fact in actor_facts),
            carrying=tuple(item.name for item in carrying),
            observation_facts=(*object_facts, *actor_facts),
        )
        digest = self.authoritative_digest()
        return PlayApplicationResult(
            result_type="look",
            message=presentation.name,
            view=view,
            pre_state_digest=digest,
            post_state_digest=digest,
        )

    def _directional_displaced_lantern_signal(
        self,
        *,
        source_place_id: str,
        direction: str,
        digest: str,
    ) -> PlayApplicationResult | None:
        """Derive one bounded AFQR-20 light signal from committed COMP-3 state."""

        normalized = direction.strip().casefold()
        try:
            destination_place_id = self.fixture.object_displacement_destination_for(
                object_entity_id=LANTERN_ID,
                source_place_id=source_place_id,
                direction=normalized,
                method="throw",
            )
            movement_destination = self.fixture.destination_for(
                source_place_id=source_place_id,
                direction=normalized,
            )
        except (
            UnavailableFixtureDisplacementError,
            UnavailableFixtureMovementError,
        ):
            return None
        if movement_destination != destination_place_id:
            return None

        lantern_state = self.object_lit_state(LANTERN_ID)
        if lantern_state is None or lantern_state.state != "lit":
            return None

        direct_placements = [
            relation
            for relation in self.state.representation.relations
            if relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == LANTERN_ID
            and relation.object_entity_id == destination_place_id
        ]
        if len(direct_placements) != 1:
            return None

        matching_displacement = any(
            transition.receipt.object_entity_id == LANTERN_ID
            and transition.receipt.source_place_id == source_place_id
            and transition.receipt.destination_place_id == destination_place_id
            and transition.receipt.method == "throw"
            for transition in (
                self.runtime_state.committed_object_displacement_transitions
            )
        )
        if not matching_displacement:
            return None

        signal_evidence = self.fixture.visual_observation_evidence(
            observer_entity_id=self.fixture.player_entity_id,
            target_entity_id=LANTERN_ID,
            place_id=destination_place_id,
            local_light_available=True,
        )
        if not signal_evidence.observable:
            return None

        lantern_name = self.fixture.entity_name(LANTERN_ID)
        return PlayApplicationResult(
            result_type="directional_light_signal",
            message=(
                f"You can see the {lantern_name}'s light to the {normalized}."
            ),
            authoritative_changed=False,
            observation_evidence_id=signal_evidence.evidence_id,
            pre_state_digest=digest,
            post_state_digest=digest,
        )

    def look_direction(self, direction: str) -> PlayApplicationResult:
        """Observe an explicitly licensed direction without moving or advancing time."""

        digest = self.authoritative_digest()
        source_place_id = self.current_place_id()
        try:
            evidence = self.fixture.directional_observation_evidence(
                observer_entity_id=self.fixture.player_entity_id,
                source_place_id=source_place_id,
                direction=direction,
            )
        except UnavailableFixtureObservationError:
            return PlayApplicationResult(
                result_type="directional_observation_unavailable",
                message="That is not a valid focused direction here.",
                authoritative_changed=False,
                pre_state_digest=digest,
                post_state_digest=digest,
                failure_class="directional_observation_invalid_direction",
            )

        if not evidence.observable or evidence.target_place_id is None:
            signal = self._directional_displaced_lantern_signal(
                source_place_id=source_place_id,
                direction=evidence.direction,
                digest=digest,
            )
            if signal is not None:
                return signal
            return PlayApplicationResult(
                result_type="directional_observation_unavailable",
                message=(
                    "You cannot make out a distinct place in that direction "
                    "from here."
                ),
                authoritative_changed=False,
                observation_evidence_id=evidence.evidence_id,
                pre_state_digest=digest,
                post_state_digest=digest,
                failure_class="directional_observation_unlicensed",
            )

        presentation = self.fixture.place_presentation(
            evidence.target_place_id
        )
        view = PublicDirectionalObservationView(
            source_place_id=source_place_id,
            direction=evidence.direction,
            target_place_id=evidence.target_place_id,
            name=presentation.name,
            description=presentation.description,
        )
        return PlayApplicationResult(
            result_type="directional_observation",
            message=presentation.name,
            view=view,
            authoritative_changed=False,
            observation_evidence_id=evidence.evidence_id,
            pre_state_digest=digest,
            post_state_digest=digest,
        )

    def inspect(self, entity_reference: str) -> PlayApplicationResult:
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
            entity_id = self.fixture.resolve_inspection_reference(
                entity_reference
            )
        except UnavailableFixtureCustodyError:
            return unavailable

        fact = self._public_observation_fact(entity_id)
        if fact is None:
            return unavailable

        view = PublicInspectionView(
            name=fact.name,
            description=self._inspection_description_from_fact(fact),
            observation_fact=fact,
        )
        return PlayApplicationResult(
            result_type="inspection",
            message=fact.name,
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
            for transition in self._runtime_state.committed_storage_transitions
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

    def _next_displacement_command_id(self) -> str:
        used = {
            transition.command_id
            for transition in (
                self._runtime_state
                .committed_object_displacement_transitions
            )
        }
        highest = 0
        for command_id in used:
            match = _DISPLACEMENT_COMMAND_ID_PATTERN.fullmatch(command_id)
            if match:
                highest = max(highest, int(match.group(1)))
        sequence = highest + 1
        while True:
            candidate = f"terminal-object-displacement-{sequence:06d}"
            if candidate not in used:
                return candidate
            sequence += 1

    def _next_handoff_command_id(self) -> str:
        used = {
            transition.command_id
            for transition in (
                self._runtime_state
                .committed_actor_object_handoff_transitions
            )
        }
        highest = 0
        for command_id in used:
            match = _HANDOFF_COMMAND_ID_PATTERN.fullmatch(command_id)
            if match:
                highest = max(highest, int(match.group(1)))
        sequence = highest + 1
        while True:
            candidate = f"terminal-actor-object-handoff-{sequence:06d}"
            if candidate not in used:
                return candidate
            sequence += 1

    def _next_time_command_id(self) -> str:
        used = {
            transition.command_id
            for transition in (
                self._runtime_state.logical_time_state.committed_transitions
            )
        }
        highest = 0
        for command_id in used:
            match = _TIME_COMMAND_ID_PATTERN.fullmatch(command_id)
            if match:
                highest = max(highest, int(match.group(1)))
        sequence = highest + 1
        while True:
            candidate = f"terminal-time-{sequence:06d}"
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

        self._runtime_state = replace_persistent_world_runtime_movement_state(
            state=self._runtime_state,
            movement_state=result.state,
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

        self._runtime_state = replace_persistent_world_runtime_custody_state(
            state=self._runtime_state,
            custody_state=result.state,
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
            self.storage_state,
            object_entity_id,
        )
        if relation is None or not self._container_accessible(relation.object_entity_id):
            return False
        open_state = self.object_open_state(relation.object_entity_id)
        return open_state is not None and open_state.state == "open"

    def _object_carrier_entity_id(
        self,
        object_entity_id: str,
    ) -> str | None:
        matches = [
            relation.object_entity_id
            for relation in self.state.representation.relations
            if relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == object_entity_id
        ]
        if len(matches) > 1:
            raise MyravantPlayApplicationError(
                "bounded object has multiple authoritative carriers"
            )
        return matches[0] if matches else None

    def _object_locally_present(self, object_entity_id: str) -> bool:
        place_id = self.current_place_id()
        relations = self.state.representation.relations
        if any(
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == object_entity_id
            and relation.object_entity_id == place_id
            for relation in relations
        ):
            return True

        carrier_entity_id = self._object_carrier_entity_id(
            object_entity_id
        )
        if carrier_entity_id is not None and any(
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == carrier_entity_id
            and relation.object_entity_id == place_id
            for relation in relations
        ):
            return True

        return self._contained_object_accessible(object_entity_id)

    def _public_location_objects(self, place_id: str):
        candidate_ids = {
            item.entity_id
            for item in self.fixture.public_entities_at(
                self.state.representation,
                place_id,
            )
        }
        for actor in self.fixture.public_actors_at(
            self.state.representation,
            place_id,
        ):
            candidate_ids.update(
                item.entity_id
                for item in self.fixture.public_entities_carried_by(
                    self.state.representation,
                    actor.entity_id,
                )
            )
        return tuple(
            presentation
            for presentation in self.fixture.object_presentations
            if presentation.entity_id in candidate_ids
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
        carrier_ids = {
            relation.object_entity_id
            for relation in relations
            if relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == LANTERN_ID
        }
        if carrier_ids and any(
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id in carrier_ids
            and relation.object_entity_id == place_id
            for relation in relations
        ):
            return True

        containment = containment_relation_for(
            self.storage_state,
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

        self._runtime_state = replace_persistent_world_runtime_open_close_state(
            state=self._runtime_state,
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
            self.storage_state,
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
                state=self.storage_state,
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

        self._runtime_state = replace_persistent_world_runtime_storage_state(
            state=self._runtime_state,
            storage_state=result.state,
        )
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
            self.storage_state,
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

    def throw_object(
        self,
        object_reference: str,
        direction: str,
    ) -> PlayApplicationResult:
        pre_digest = self.authoritative_digest()
        unavailable = PlayApplicationResult(
            result_type="object_displacement_rejected",
            message="You cannot throw that from the current state.",
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=pre_digest,
            failure_class="object_displacement_target_unavailable",
        )
        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
        except UnavailableFixtureCustodyError:
            return unavailable

        carried = any(
            relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == object_entity_id
            and relation.object_entity_id == self.fixture.player_entity_id
            for relation in self.state.representation.relations
        )
        if not carried:
            return unavailable

        source_place_id = self.current_place_id()
        normalized_direction = direction.strip().casefold()
        try:
            destination_place_id = (
                self.fixture.object_displacement_destination_for(
                    object_entity_id=object_entity_id,
                    source_place_id=source_place_id,
                    direction=normalized_direction,
                    method="throw",
                )
            )
        except UnavailableFixtureDisplacementError:
            return PlayApplicationResult(
                result_type="object_displacement_rejected",
                message="You cannot throw that way from here.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="object_displacement_route_unavailable",
            )

        command_id = self._next_displacement_command_id()
        command = create_command_envelope(
            command_id=command_id,
            command_type="transfer_object",
            source_actor_id=self.fixture.player_entity_id,
            payload={
                "object_entity_id": object_entity_id,
                "destination_entity_id": destination_place_id,
                "method": "throw",
            },
            metadata={"client": "myravant-terminal-comp3"},
        )
        qualification, spatial, opportunity = (
            self.fixture.object_displacement_evidence(
                command_id=command_id,
                object_entity_id=object_entity_id,
                source_place_id=source_place_id,
                direction=normalized_direction,
                destination_place_id=destination_place_id,
                method="throw",
            )
        )
        try:
            result = execute_persistent_world_object_displacement(
                state=self.displacement_state,
                command=command,
                qualification_evidence=qualification,
                spatial_evidence=spatial,
                opportunity_evidence=opportunity,
                expected_pre_state_digest=self.representation_digest(),
            )
        except PersistentWorldObjectDisplacementError as exc:
            return PlayApplicationResult(
                result_type="object_displacement_rejected",
                message="The throw was rejected by the authoritative runtime.",
                authoritative_changed=False,
                command_id=command_id,
                spatial_evidence_id=spatial.evidence_id,
                opportunity_evidence_id=opportunity.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=type(exc).__name__,
            )

        self._runtime_state = (
            replace_persistent_world_runtime_displacement_state(
                state=self._runtime_state,
                displacement_state=result.state,
            )
        )
        object_name = self.fixture.entity_name(object_entity_id)
        return PlayApplicationResult(
            result_type="object_displacement_committed",
            message=(
                f"You throw the {object_name} "
                f"{normalized_direction}."
            ),
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
            post_state_digest=self.authoritative_digest(),
            technical_retry=result.technical_retry,
        )

    def give_object(
        self,
        object_reference: str,
        recipient_reference: str,
    ) -> PlayApplicationResult:
        pre_digest = self.authoritative_digest()
        unavailable = PlayApplicationResult(
            result_type="actor_object_handoff_rejected",
            message="You cannot hand that over from the current state.",
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=pre_digest,
            failure_class="actor_object_handoff_target_unavailable",
        )
        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
        except UnavailableFixtureCustodyError:
            return unavailable
        try:
            recipient_actor_entity_id = self.fixture.resolve_actor_reference(
                recipient_reference
            )
        except UnavailableFixtureHandoffError:
            return PlayApplicationResult(
                result_type="actor_object_handoff_rejected",
                message="That recipient is not available in this bounded fixture.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="unknown_or_ambiguous_fixture_actor",
            )

        source_actor_entity_id = self.fixture.player_entity_id
        carried = any(
            relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == object_entity_id
            and relation.object_entity_id == source_actor_entity_id
            for relation in self.state.representation.relations
        )
        if not carried:
            return unavailable

        place_id = self.current_place_id()
        try:
            recipient_place_id = self.entity_place_id(
                recipient_actor_entity_id
            )
        except MyravantPlayApplicationError:
            recipient_place_id = None
        if recipient_place_id != place_id:
            return PlayApplicationResult(
                result_type="actor_object_handoff_rejected",
                message="The intended recipient is not here.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="actor_object_handoff_recipient_unavailable",
            )

        command_id = self._next_handoff_command_id()
        command = create_command_envelope(
            command_id=command_id,
            command_type="transfer_object",
            source_actor_id=source_actor_entity_id,
            payload={
                "object_entity_id": object_entity_id,
                "recipient_actor_entity_id": recipient_actor_entity_id,
                "method": "handoff",
            },
            metadata={"client": "myravant-terminal-vsm6"},
        )
        try:
            qualification, spatial, opportunity = (
                self.fixture.actor_object_handoff_evidence(
                    command_id=command_id,
                    object_entity_id=object_entity_id,
                    source_actor_entity_id=source_actor_entity_id,
                    recipient_actor_entity_id=recipient_actor_entity_id,
                    place_id=place_id,
                    method="handoff",
                )
            )
        except UnavailableFixtureHandoffError:
            return PlayApplicationResult(
                result_type="actor_object_handoff_rejected",
                message="That handoff is not qualified in this bounded fixture.",
                authoritative_changed=False,
                command_id=command_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="actor_object_handoff_route_unavailable",
            )

        try:
            result = execute_persistent_world_actor_object_handoff(
                state=self.handoff_state,
                command=command,
                qualification_evidence=qualification,
                spatial_evidence=spatial,
                opportunity_evidence=opportunity,
                expected_pre_state_digest=self.representation_digest(),
            )
        except PersistentWorldActorObjectHandoffError as exc:
            return PlayApplicationResult(
                result_type="actor_object_handoff_rejected",
                message=(
                    "The handoff was rejected by the authoritative runtime."
                ),
                authoritative_changed=False,
                command_id=command_id,
                spatial_evidence_id=spatial.evidence_id,
                opportunity_evidence_id=opportunity.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=type(exc).__name__,
            )

        self._runtime_state = (
            replace_persistent_world_runtime_actor_object_handoff_state(
                state=self._runtime_state,
                handoff_state=result.state,
            )
        )
        object_name = self.fixture.entity_name(object_entity_id)
        recipient_name = self.fixture.entity_name(
            recipient_actor_entity_id
        )
        return PlayApplicationResult(
            result_type="actor_object_handoff_committed",
            message=(
                f"You hand the {object_name} to the {recipient_name}."
            ),
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
            post_state_digest=self.authoritative_digest(),
            technical_retry=result.technical_retry,
        )



    def request_object_state_from_actor(
        self,
        actor_reference: str,
        operation: str,
        object_reference: str,
    ) -> PlayApplicationResult:
        pre_digest = self.authoritative_digest()
        normalized_operation = operation.strip().casefold()
        unavailable = PlayApplicationResult(
            result_type="object_state_request_rejected",
            message="That requested world interaction is not available.",
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=pre_digest,
            failure_class="object_state_request_target_unavailable",
        )

        if normalized_operation not in {"open", "close"}:
            return PlayApplicationResult(
                result_type="object_state_request_rejected",
                message="That requested operation is not supported.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="object_state_request_operation_unavailable",
            )

        try:
            actor_entity_id = self.fixture.resolve_actor_reference(
                actor_reference
            )
        except UnavailableFixtureHandoffError:
            return PlayApplicationResult(
                result_type="object_state_request_rejected",
                message="That actor is not available in this bounded fixture.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="unknown_or_ambiguous_fixture_actor",
            )

        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
        except UnavailableFixtureCustodyError:
            return unavailable

        player_place_id = self.current_place_id()
        try:
            actor_place_id = self.entity_place_id(actor_entity_id)
        except MyravantPlayApplicationError:
            actor_place_id = None
        if actor_place_id != player_place_id:
            return PlayApplicationResult(
                result_type="object_state_request_rejected",
                message="The requested actor is not here.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="object_state_request_actor_unavailable",
            )

        if not self.fixture.requested_object_state_route_available(
            actor_entity_id=actor_entity_id,
            object_entity_id=object_entity_id,
            operation=normalized_operation,
        ):
            return PlayApplicationResult(
                result_type="object_state_request_rejected",
                message="That request is not qualified in this bounded fixture.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="object_state_request_route_unavailable",
            )

        current = self.object_open_state(object_entity_id)
        if current is None:
            return PlayApplicationResult(
                result_type="object_state_request_rejected",
                message="That object does not support this bounded interaction.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="object_state_not_supported",
            )

        command_id = self._next_object_state_command_id()
        opportunity_available = (
            persistent_world_object_open_close_opportunity_available(
                state=self.object_state,
                actor_entity_id=actor_entity_id,
                object_entity_id=object_entity_id,
            )
        )
        qualification, opportunity = self.fixture.object_open_close_evidence(
            command_id=command_id,
            actor_entity_id=actor_entity_id,
            object_entity_id=object_entity_id,
            operation=normalized_operation,
            opportunity_available=opportunity_available,
        )
        if not opportunity_available:
            return PlayApplicationResult(
                result_type="object_state_request_rejected",
                message="The requested actor cannot reach that object.",
                authoritative_changed=False,
                command_id=command_id,
                opportunity_evidence_id=opportunity.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="object_state_request_opportunity_unavailable",
            )

        desired = "open" if normalized_operation == "open" else "closed"
        object_name = self.fixture.entity_name(object_entity_id)
        if current.state == desired:
            return PlayApplicationResult(
                result_type="object_state_unchanged",
                message=f"The {object_name} is already {desired}.",
                authoritative_changed=False,
                command_id=command_id,
                opportunity_evidence_id=opportunity.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
            )

        command = create_command_envelope(
            command_id=command_id,
            command_type=f"{normalized_operation}_object",
            source_actor_id=actor_entity_id,
            payload={"object_entity_id": object_entity_id},
            metadata={"client": "myravant-terminal-vsm8"},
        )

        try:
            result = execute_persistent_world_object_open_close(
                state=self.object_state,
                command=command,
                qualification_evidence=qualification,
                opportunity_evidence=opportunity,
                expected_pre_state_digest=self.object_state_digest(),
            )
        except PersistentWorldObjectOpenCloseError as exc:
            return PlayApplicationResult(
                result_type="object_state_request_rejected",
                message=(
                    "The requested interaction was rejected by the "
                    "authoritative runtime."
                ),
                authoritative_changed=False,
                command_id=command_id,
                opportunity_evidence_id=opportunity.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=type(exc).__name__,
            )

        self._runtime_state = replace_persistent_world_runtime_open_close_state(
            state=self._runtime_state,
            open_close_state=result.state,
        )
        actor_name = self.fixture.entity_name(actor_entity_id)
        verb = "opens" if normalized_operation == "open" else "closes"
        return PlayApplicationResult(
            result_type="object_state_committed",
            message=f"The {actor_name} {verb} the {object_name}.",
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

    def request_object_from_actor(
        self,
        source_reference: str,
        object_reference: str,
    ) -> PlayApplicationResult:
        # The player's request is intent only. It does not directly command
        # the NPC or mutate authority. The fixture licenses one accepted
        # Groundskeeper -> Traveler return, then the existing handoff runtime
        # remains the sole authoritative state-transition path.
        pre_digest = self.authoritative_digest()
        unavailable = PlayApplicationResult(
            result_type="actor_object_handoff_rejected",
            message="That actor cannot return that object from the current state.",
            authoritative_changed=False,
            pre_state_digest=pre_digest,
            post_state_digest=pre_digest,
            failure_class="actor_object_handoff_target_unavailable",
        )

        try:
            object_entity_id = self.fixture.resolve_object_reference(
                object_reference
            )
        except UnavailableFixtureCustodyError:
            return unavailable

        try:
            source_actor_entity_id = self.fixture.resolve_actor_reference(
                source_reference
            )
        except UnavailableFixtureHandoffError:
            return PlayApplicationResult(
                result_type="actor_object_handoff_rejected",
                message="That actor is not available in this bounded fixture.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="unknown_or_ambiguous_fixture_actor",
            )

        recipient_actor_entity_id = self.fixture.player_entity_id
        carried = any(
            relation.relation_type == CARRIED_BY_RELATION_TYPE
            and relation.subject_entity_id == object_entity_id
            and relation.object_entity_id == source_actor_entity_id
            for relation in self.state.representation.relations
        )
        if not carried:
            return unavailable

        place_id = self.current_place_id()
        try:
            source_place_id = self.entity_place_id(source_actor_entity_id)
        except MyravantPlayApplicationError:
            source_place_id = None
        if source_place_id != place_id:
            return PlayApplicationResult(
                result_type="actor_object_handoff_rejected",
                message="The actor carrying that object is not here.",
                authoritative_changed=False,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="actor_object_handoff_source_unavailable",
            )

        command_id = self._next_handoff_command_id()
        command = create_command_envelope(
            command_id=command_id,
            command_type="transfer_object",
            source_actor_id=source_actor_entity_id,
            payload={
                "object_entity_id": object_entity_id,
                "recipient_actor_entity_id": recipient_actor_entity_id,
                "method": "handoff",
            },
            metadata={"client": "myravant-terminal-vsm7"},
        )

        try:
            qualification, spatial, opportunity = (
                self.fixture.actor_object_handoff_evidence(
                    command_id=command_id,
                    object_entity_id=object_entity_id,
                    source_actor_entity_id=source_actor_entity_id,
                    recipient_actor_entity_id=recipient_actor_entity_id,
                    place_id=place_id,
                    method="handoff",
                )
            )
        except UnavailableFixtureHandoffError:
            return PlayApplicationResult(
                result_type="actor_object_handoff_rejected",
                message="That return is not qualified in this bounded fixture.",
                authoritative_changed=False,
                command_id=command_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class="actor_object_handoff_route_unavailable",
            )

        try:
            result = execute_persistent_world_actor_object_handoff(
                state=self.handoff_state,
                command=command,
                qualification_evidence=qualification,
                spatial_evidence=spatial,
                opportunity_evidence=opportunity,
                expected_pre_state_digest=self.representation_digest(),
            )
        except PersistentWorldActorObjectHandoffError as exc:
            return PlayApplicationResult(
                result_type="actor_object_handoff_rejected",
                message=(
                    "The return handoff was rejected by the authoritative runtime."
                ),
                authoritative_changed=False,
                command_id=command_id,
                spatial_evidence_id=spatial.evidence_id,
                opportunity_evidence_id=opportunity.evidence_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                failure_class=type(exc).__name__,
            )

        self._runtime_state = (
            replace_persistent_world_runtime_actor_object_handoff_state(
                state=self._runtime_state,
                handoff_state=result.state,
            )
        )
        object_name = self.fixture.entity_name(object_entity_id)
        source_name = self.fixture.entity_name(source_actor_entity_id)
        return PlayApplicationResult(
            result_type="actor_object_handoff_committed",
            message=f"The {source_name} hands you the {object_name}.",
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
            post_state_digest=self.authoritative_digest(),
            technical_retry=result.technical_retry,
        )

    def wait(self) -> PlayApplicationResult:
        pre_digest = self.authoritative_digest()
        pre_time = self._runtime_state.logical_time_state
        command_id = self._next_time_command_id()
        command = create_command_envelope(
            command_id=command_id,
            command_type="wait",
            source_actor_id=self.fixture.player_entity_id,
            payload={
                "advance_steps": 1,
                "scheduler_profile_id": WORLD1_SCHEDULER_PROFILE_ID,
            },
            metadata={"client": "myravant-terminal-world2"},
        )
        try:
            prepared_time = prepare_persistent_world_logical_time(
                state=pre_time,
                command=command,
                expected_pre_state_digest=(
                    digest_persistent_world_logical_time_state(pre_time)
                ),
            )
            phase = prepared_time.post_position % 4
            due_process_ref = build_record_id(
                "evidence",
                "world2-due-" + prepared_time.command_fingerprint[:20],
            )

            if phase in {0, 1}:
                destination_place_id = (
                    YARD_ID if phase == 1 else GATEHOUSE_ID
                )
                source_place_id = self.entity_place_id(GROUNDSKEEPER_ID)
                world_process_command_id = (
                    "world2-npc-move-"
                    + prepared_time.command_fingerprint[:24]
                )
                movement_command = create_command_envelope(
                    command_id=world_process_command_id,
                    command_type="move",
                    source_actor_id=GROUNDSKEEPER_ID,
                    payload={
                        "destination_entity_id": destination_place_id
                    },
                    metadata={
                        "client": "myravant-world2-routine",
                        "routine_profile_id": WORLD2_ROUTINE_PROFILE_ID,
                        "source_time_command_id": command_id,
                    },
                )
                spatial, opportunity = (
                    self.fixture.autonomous_movement_evidence(
                        command_id=movement_command.command_id,
                        actor_entity_id=GROUNDSKEEPER_ID,
                        source_place_id=source_place_id,
                        destination_place_id=destination_place_id,
                    )
                )
                prepared_movement = prepare_persistent_world_movement(
                    state=self.state,
                    command=movement_command,
                    spatial_evidence=spatial,
                    opportunity_evidence=opportunity,
                    expected_pre_state_digest=self.representation_digest(),
                )
                advancement = (
                    commit_prepared_persistent_world_world_advancement(
                        state=self._runtime_state,
                        time_prepared=prepared_time,
                        movement_prepared=prepared_movement,
                        due_process_ref=due_process_ref,
                    )
                )
                self._runtime_state = advancement.state
                return PlayApplicationResult(
                    result_type="world_advanced",
                    message="Time passes.",
                    authoritative_changed=True,
                    command_id=command_id,
                    command_fingerprint=(
                        advancement.time_receipt.command_fingerprint
                    ),
                    preview_id=advancement.time_preview.preview_id,
                    receipt_id=advancement.time_receipt.receipt_id,
                    state_delta_id=advancement.time_state_delta.delta_id,
                    spatial_evidence_id=(
                        advancement.movement_receipt.spatial_evidence_id
                    ),
                    opportunity_evidence_id=(
                        advancement.movement_receipt.opportunity_evidence_id
                    ),
                    due_process_ref=advancement.due_process_ref,
                    consequence_receipt_id=(
                        advancement.movement_receipt.receipt_id
                    ),
                    consequence_state_delta_id=(
                        advancement.movement_state_delta.delta_id
                    ),
                    world_event_class="world_autonomous_action",
                    world_process_actor_id=GROUNDSKEEPER_ID,
                    world_process_action="move",
                    world_process_target_id=destination_place_id,
                    world_process_command_id=world_process_command_id,
                    world_process_outcome="committed",
                    logical_time_before=(
                        advancement.time_receipt.pre_position
                    ),
                    logical_time_after=(
                        advancement.time_receipt.post_position
                    ),
                    pre_state_digest=pre_digest,
                    post_state_digest=self.authoritative_digest(),
                    technical_retry=advancement.technical_retry,
                )

            operation = "open" if phase == 2 else "close"
            desired = "open" if operation == "open" else "closed"
            world_process_command_id = (
                f"world2-npc-{operation}-"
                + prepared_time.command_fingerprint[:24]
            )
            current = self.object_open_state(TOOL_CHEST_ID)
            if current is None:
                raise PersistentWorldObjectOpenCloseError(
                    "WORLD-2 Tool Chest lacks bounded open/close state"
                )

            opportunity_available = (
                persistent_world_object_open_close_opportunity_available(
                    state=self.object_state,
                    actor_entity_id=GROUNDSKEEPER_ID,
                    object_entity_id=TOOL_CHEST_ID,
                )
            )
            qualification, opportunity = (
                self.fixture.object_open_close_evidence(
                    command_id=world_process_command_id,
                    actor_entity_id=GROUNDSKEEPER_ID,
                    object_entity_id=TOOL_CHEST_ID,
                    operation=operation,
                    opportunity_available=opportunity_available,
                )
            )

            if current.state == desired or not opportunity_available:
                time_result = commit_prepared_persistent_world_logical_time(
                    state=pre_time,
                    prepared=prepared_time,
                )
                self._runtime_state = (
                    replace_persistent_world_runtime_logical_time_state(
                        state=self._runtime_state,
                        logical_time_state=time_result.state,
                    )
                )
                outcome = (
                    "already_satisfied"
                    if current.state == desired
                    else "opportunity_unavailable"
                )
                return PlayApplicationResult(
                    result_type="world_advanced",
                    message="Time passes.",
                    authoritative_changed=True,
                    command_id=command_id,
                    command_fingerprint=(
                        time_result.receipt.command_fingerprint
                    ),
                    preview_id=time_result.preview.preview_id,
                    receipt_id=time_result.receipt.receipt_id,
                    state_delta_id=time_result.state_delta.delta_id,
                    opportunity_evidence_id=opportunity.evidence_id,
                    due_process_ref=due_process_ref,
                    world_event_class="world_autonomous_action",
                    world_process_actor_id=GROUNDSKEEPER_ID,
                    world_process_action=f"{operation}_object",
                    world_process_target_id=TOOL_CHEST_ID,
                    world_process_command_id=world_process_command_id,
                    world_process_outcome=outcome,
                    logical_time_before=time_result.receipt.pre_position,
                    logical_time_after=time_result.receipt.post_position,
                    pre_state_digest=pre_digest,
                    post_state_digest=self.authoritative_digest(),
                    technical_retry=time_result.technical_retry,
                )

            object_command = create_command_envelope(
                command_id=world_process_command_id,
                command_type=f"{operation}_object",
                source_actor_id=GROUNDSKEEPER_ID,
                payload={"object_entity_id": TOOL_CHEST_ID},
                metadata={
                    "client": "myravant-world2-routine",
                    "routine_profile_id": WORLD2_ROUTINE_PROFILE_ID,
                    "source_time_command_id": command_id,
                },
            )
            prepared_interaction = (
                prepare_persistent_world_object_open_close(
                    state=self.object_state,
                    command=object_command,
                    qualification_evidence=qualification,
                    opportunity_evidence=opportunity,
                    expected_pre_state_digest=self.object_state_digest(),
                )
            )
            advancement = (
                commit_prepared_persistent_world_world_interaction_advancement(
                    state=self._runtime_state,
                    time_prepared=prepared_time,
                    interaction_prepared=prepared_interaction,
                    due_process_ref=due_process_ref,
                )
            )
            self._runtime_state = advancement.state
            return PlayApplicationResult(
                result_type="world_advanced",
                message="Time passes.",
                authoritative_changed=True,
                command_id=command_id,
                command_fingerprint=(
                    advancement.time_receipt.command_fingerprint
                ),
                preview_id=advancement.time_preview.preview_id,
                receipt_id=advancement.time_receipt.receipt_id,
                state_delta_id=advancement.time_state_delta.delta_id,
                opportunity_evidence_id=(
                    advancement.interaction_receipt.opportunity_evidence_id
                ),
                due_process_ref=advancement.due_process_ref,
                consequence_receipt_id=(
                    advancement.interaction_receipt.receipt_id
                ),
                consequence_state_delta_id=(
                    advancement.interaction_state_delta.delta_id
                ),
                world_event_class="world_autonomous_action",
                world_process_actor_id=GROUNDSKEEPER_ID,
                world_process_action=f"{operation}_object",
                world_process_target_id=TOOL_CHEST_ID,
                world_process_command_id=world_process_command_id,
                world_process_outcome="committed",
                logical_time_before=(
                    advancement.time_receipt.pre_position
                ),
                logical_time_after=(
                    advancement.time_receipt.post_position
                ),
                pre_state_digest=pre_digest,
                post_state_digest=self.authoritative_digest(),
                technical_retry=advancement.technical_retry,
            )
        except (
            PersistentWorldLogicalTimeError,
            PersistentWorldMovementIntegrationError,
            PersistentWorldObjectOpenCloseError,
            PersistentWorldWorldAdvancementError,
            UnavailableFixtureCustodyError,
            UnavailableFixtureMovementError,
        ) as exc:
            return PlayApplicationResult(
                result_type="world_advancement_rejected",
                message=(
                    "The bounded world advancement was rejected by "
                    "the authoritative runtime."
                ),
                authoritative_changed=False,
                command_id=command_id,
                pre_state_digest=pre_digest,
                post_state_digest=pre_digest,
                logical_time_before=pre_time.logical_position,
                logical_time_after=pre_time.logical_position,
                failure_class=type(exc).__name__,
            )

    def save(self) -> PlayApplicationResult:
        if self.checkpoint_path is None:
            raise CheckpointPathRequiredError(
                "save requires --checkpoint or a loaded checkpoint path"
            )

        pre_digest = self.authoritative_digest()
        checkpoint_writer = (
            write_persistent_world_vsm6_checkpoint
            if self._runtime_state.committed_actor_object_handoff_transitions
            else write_persistent_world_comp3_checkpoint
            if self._runtime_state.committed_object_displacement_transitions
            else write_persistent_world_world1_checkpoint
        )
        checkpoint_digest = checkpoint_writer(
            state=self._runtime_state,
            checkpoint_path=self.checkpoint_path,
            qualification_evidence=self.fixture.checkpoint_qualification,
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

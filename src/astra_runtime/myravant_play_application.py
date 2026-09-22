"""Thin application adapter for the bounded Myravant terminal vertical slice.

The adapter owns session orchestration only. Authoritative movement and durable
checkpoint behavior remain in the existing R4-C and R4-D runtime modules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    restore_persistent_world_checkpoint,
    write_persistent_world_checkpoint,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementRuntimeState,
    digest_persistent_world_entity_location_representation,
    execute_persistent_world_movement,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.myravant_play_fixture import (
    MyravantPlayFixture,
    UnavailableFixtureMovementError,
    create_terminal_play_fixture,
)


_COMMAND_ID_PATTERN = re.compile(r"^terminal-move-(\d{6})$")


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


@dataclass(frozen=True, kw_only=True)
class PlayApplicationResult:
    result_type: str
    message: str
    view: PublicLocationView | None = None
    authoritative_changed: bool = False
    command_id: str | None = None
    receipt_id: str | None = None
    state_delta_id: str | None = None
    pre_state_digest: str | None = None
    post_state_digest: str | None = None
    checkpoint_digest: str | None = None
    failure_class: str | None = None


class MyravantPlayApplication:
    """Session-scoped holder for one bounded authoritative runtime state."""

    def __init__(
        self,
        *,
        fixture: MyravantPlayFixture,
        state: PersistentWorldMovementRuntimeState,
        checkpoint_path: str | Path | None = None,
    ) -> None:
        self.fixture = fixture
        self.state = state
        self.checkpoint_path = (
            Path(checkpoint_path)
            if checkpoint_path is not None
            else None
        )

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
            state=bounded_fixture.initial_state,
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
        state = restore_persistent_world_checkpoint(
            checkpoint_path=checkpoint_path,
            expected_campaign_id=bounded_fixture.campaign_id,
        )
        return cls(
            fixture=bounded_fixture,
            state=state,
            checkpoint_path=checkpoint_path,
        )

    def authoritative_digest(self) -> str:
        return digest_persistent_world_entity_location_representation(
            self.state.representation
        )

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
        view = PublicLocationView(
            place_id=place_id,
            name=presentation.name,
            description=presentation.description,
            exits=self.fixture.exits_from(place_id),
            objects=tuple(item.name for item in objects),
        )
        digest = self.authoritative_digest()
        return PlayApplicationResult(
            result_type="look",
            message=presentation.name,
            view=view,
            pre_state_digest=digest,
            post_state_digest=digest,
        )

    def _next_command_id(self) -> str:
        used = {
            transition.command_id
            for transition in self.state.committed_transitions
        }
        highest = 0
        for command_id in used:
            match = _COMMAND_ID_PATTERN.fullmatch(command_id)
            if match:
                highest = max(highest, int(match.group(1)))
        sequence = highest + 1
        while True:
            candidate = f"terminal-move-{sequence:06d}"
            if candidate not in used:
                return candidate
            sequence += 1

    def move(self, direction: str) -> PlayApplicationResult:
        normalized = direction.strip().lower()
        pre_digest = self.authoritative_digest()
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

        command_id = self._next_command_id()
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
            expected_pre_state_digest=pre_digest,
        )

        self.state = result.state
        post_digest = self.authoritative_digest()
        destination_name = self.fixture.place_presentation(
            destination_place_id
        ).name

        return PlayApplicationResult(
            result_type="movement_committed",
            message=f"You move to the {destination_name}.",
            authoritative_changed=True,
            command_id=command_id,
            receipt_id=result.receipt.receipt_id,
            state_delta_id=result.state_delta.delta_id,
            pre_state_digest=pre_digest,
            post_state_digest=post_digest,
        )

    def save(self) -> PlayApplicationResult:
        if self.checkpoint_path is None:
            raise CheckpointPathRequiredError(
                "save requires --checkpoint or a loaded checkpoint path"
            )

        pre_digest = self.authoritative_digest()
        checkpoint_digest = write_persistent_world_checkpoint(
            state=self.state,
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

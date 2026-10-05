"""VSM-14 application composition for persistent follow intent.

The base Myravant application continues to own session orchestration for the
existing playable runtime. This subclass adds one AFQR-12 follow-intent state
component, checkpoint v5 persistence, and one bounded consequence hook:
when an active co-located follower's leader commits a direct player movement,
the follower may perform the same already-qualified fixture route through R4-C.

The hook does not create pathfinding, catch-up, teleportation, obedience,
guarding, task scheduling, or generalized NPC planning.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import replace
from pathlib import Path

from astra_runtime.domain.persistent_world_follow_intent import (
    PersistentWorldFollowIntentRuntimeState,
    active_follow_intent_for,
    create_persistent_world_follow_intent_runtime_state,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointFormatError,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementIntegrationError,
    create_movement_opportunity_evidence,
    create_movement_spatial_evidence,
    execute_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    replace_persistent_world_runtime_movement_state,
)
from astra_runtime.domain.persistent_world_vsm14_checkpoint import (
    digest_persistent_world_vsm14_authoritative_state,
    restore_persistent_world_vsm14_checkpoint,
    write_persistent_world_vsm14_checkpoint,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.myravant_play_application import (
    CheckpointPathRequiredError,
    MyravantPlayApplication,
    PlayApplicationResult,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    MyravantPlayFixture,
    create_terminal_play_fixture,
)


_FOLLOW_INTENT_COMMAND_ID_PATTERN = re.compile(
    r"^terminal-follow-intent-(\d{6})$"
)


class MyravantVSM14Application(MyravantPlayApplication):
    """Playable application with one additional AFQR-12 owner-local state."""

    def __init__(
        self,
        *,
        fixture: MyravantPlayFixture,
        runtime_state,
        follow_intent_state: PersistentWorldFollowIntentRuntimeState,
        checkpoint_path: str | Path | None = None,
    ) -> None:
        super().__init__(
            fixture=fixture,
            runtime_state=runtime_state,
            checkpoint_path=checkpoint_path,
        )
        if not isinstance(
            follow_intent_state, PersistentWorldFollowIntentRuntimeState
        ):
            raise TypeError(
                "follow_intent_state must be PersistentWorldFollowIntentRuntimeState"
            )
        self._follow_intent_state = follow_intent_state

    @property
    def follow_intent_state(self) -> PersistentWorldFollowIntentRuntimeState:
        return self._follow_intent_state

    def replace_follow_intent_state(
        self, state: PersistentWorldFollowIntentRuntimeState
    ) -> None:
        if not isinstance(state, PersistentWorldFollowIntentRuntimeState):
            raise TypeError(
                "state must be PersistentWorldFollowIntentRuntimeState"
            )
        self._follow_intent_state = state

    @classmethod
    def new(
        cls,
        *,
        checkpoint_path: str | Path | None = None,
        fixture: MyravantPlayFixture | None = None,
    ) -> "MyravantVSM14Application":
        bounded_fixture = fixture or create_terminal_play_fixture()
        base = MyravantPlayApplication.new(
            checkpoint_path=checkpoint_path,
            fixture=bounded_fixture,
        )
        return cls(
            fixture=bounded_fixture,
            runtime_state=base.runtime_state,
            follow_intent_state=(
                create_persistent_world_follow_intent_runtime_state()
            ),
            checkpoint_path=checkpoint_path,
        )

    @classmethod
    def restore(
        cls,
        *,
        checkpoint_path: str | Path,
        fixture: MyravantPlayFixture | None = None,
    ) -> "MyravantVSM14Application":
        bounded_fixture = fixture or create_terminal_play_fixture()
        try:
            runtime_state, follow_state = restore_persistent_world_vsm14_checkpoint(
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
            base = MyravantPlayApplication.restore(
                checkpoint_path=checkpoint_path,
                fixture=bounded_fixture,
            )
            runtime_state = base.runtime_state
            follow_state = create_persistent_world_follow_intent_runtime_state()
        return cls(
            fixture=bounded_fixture,
            runtime_state=runtime_state,
            follow_intent_state=follow_state,
            checkpoint_path=checkpoint_path,
        )

    def authoritative_digest(self) -> str:
        return digest_persistent_world_vsm14_authoritative_state(
            runtime_state=self.runtime_state,
            follow_intent_state=self.follow_intent_state,
        )

    def _next_follow_intent_command_id(self) -> str:
        used = {
            transition.command_id
            for transition in self.follow_intent_state.committed_transitions
        }
        highest = 0
        for command_id in used:
            match = _FOLLOW_INTENT_COMMAND_ID_PATTERN.fullmatch(command_id)
            if match:
                highest = max(highest, int(match.group(1)))
        sequence = highest + 1
        while True:
            candidate = f"terminal-follow-intent-{sequence:06d}"
            if candidate not in used:
                return candidate
            sequence += 1

    def _active_follow_transition(self, follower_entity_id: str):
        for transition in reversed(
            self.follow_intent_state.committed_transitions
        ):
            receipt = transition.receipt
            if (
                receipt.follower_entity_id == follower_entity_id
                and receipt.post_status == "active"
            ):
                return transition
        return None

    def _follow_route_exists(
        self,
        *,
        source_place_id: str,
        destination_place_id: str,
    ) -> bool:
        return any(
            route.source_place_id == source_place_id
            and route.destination_place_id == destination_place_id
            for route in self.fixture.movement_routes
        )

    def move(self, direction: str) -> PlayApplicationResult:
        leader_entity_id = self.fixture.player_entity_id
        active = active_follow_intent_for(
            self.follow_intent_state, GROUNDSKEEPER_ID
        )
        source_place_id = self.current_place_id()
        follower_place_id = None
        if active is not None and active.leader_entity_id == leader_entity_id:
            try:
                follower_place_id = self.entity_place_id(GROUNDSKEEPER_ID)
            except Exception:
                follower_place_id = None

        player_result = super().move(direction)
        if (
            player_result.result_type != "movement_committed"
            or active is None
            or active.leader_entity_id != leader_entity_id
            or follower_place_id != source_place_id
        ):
            return player_result

        destination_place_id = self.current_place_id()
        if not self._follow_route_exists(
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
        ):
            return player_result

        activation = self._active_follow_transition(GROUNDSKEEPER_ID)
        source_fingerprint = (
            player_result.command_fingerprint
            or hashlib.sha256(
                (
                    f"{source_place_id}|{destination_place_id}|"
                    f"{self.representation_digest()}"
                ).encode("utf-8")
            ).hexdigest()
        )
        command_id = f"vsm14-follow-move-{source_fingerprint[:24]}"
        command = create_command_envelope(
            command_id=command_id,
            command_type="move",
            source_actor_id=GROUNDSKEEPER_ID,
            payload={"destination_entity_id": destination_place_id},
            metadata={
                "client": "myravant-terminal-vsm14",
                "package": "VSM-14",
                "behavior": "follow",
                "leader_entity_id": leader_entity_id,
                "follow_intent_command_id": (
                    activation.command_id if activation is not None else None
                ),
                "source_player_command_id": player_result.command_id,
            },
        )
        token = hashlib.sha256(
            (
                f"{command_id}|{GROUNDSKEEPER_ID}|{source_place_id}|"
                f"{destination_place_id}"
            ).encode("utf-8")
        ).hexdigest()[:20]
        spatial = create_movement_spatial_evidence(
            evidence_id=build_record_id(
                "evidence", f"vsm14-follow-{token}-afqr18"
            ),
            actor_entity_id=GROUNDSKEEPER_ID,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            spatially_permitted=True,
        )
        opportunity = create_movement_opportunity_evidence(
            evidence_id=build_record_id(
                "evidence", f"vsm14-follow-{token}-afqr19"
            ),
            actor_entity_id=GROUNDSKEEPER_ID,
            destination_place_id=destination_place_id,
            opportunity_available=True,
            resolution_accepted=True,
        )
        try:
            followed = execute_persistent_world_movement(
                state=self.state,
                command=command,
                spatial_evidence=spatial,
                opportunity_evidence=opportunity,
                expected_pre_state_digest=self.representation_digest(),
            )
        except PersistentWorldMovementIntegrationError:
            return replace(
                player_result,
                message=(
                    f"{player_result.message} "
                    "The Groundskeeper cannot follow that move."
                ),
                post_state_digest=self.authoritative_digest(),
                world_event_class="behavioral_intent_consequence",
                world_process_actor_id=GROUNDSKEEPER_ID,
                world_process_action="follow_move",
                world_process_target_id=destination_place_id,
                world_process_command_id=command_id,
                world_process_outcome="rejected",
            )

        self._runtime_state = replace_persistent_world_runtime_movement_state(
            state=self.runtime_state,
            movement_state=followed.state,
        )
        follower_name = self.fixture.entity_name(GROUNDSKEEPER_ID)
        return replace(
            player_result,
            message=f"{player_result.message} The {follower_name} follows.",
            post_state_digest=self.authoritative_digest(),
            consequence_receipt_id=followed.receipt.receipt_id,
            consequence_state_delta_id=followed.state_delta.delta_id,
            world_event_class="behavioral_intent_consequence",
            world_process_actor_id=GROUNDSKEEPER_ID,
            world_process_action="follow_move",
            world_process_target_id=destination_place_id,
            world_process_command_id=command_id,
            world_process_outcome="committed",
        )

    def save(self) -> PlayApplicationResult:
        if self.checkpoint_path is None:
            raise CheckpointPathRequiredError(
                "save requires --checkpoint or a loaded checkpoint path"
            )
        pre_digest = self.authoritative_digest()
        checkpoint_digest = write_persistent_world_vsm14_checkpoint(
            runtime_state=self.runtime_state,
            follow_intent_state=self.follow_intent_state,
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

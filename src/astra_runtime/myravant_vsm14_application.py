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
from astra_runtime.domain.persistent_world_object_open_close import (
    FixtureServiceError, FixtureServiceState, _transition as _service_transition,
    digest_fixture_service_state, execute_fixture_service,
)
from astra_runtime.domain.persistent_world_vsm14_checkpoint import (
    digest_b2a_authoritative_state, restore_b2a_checkpoint,
    write_b2a_checkpoint,
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
    GROUNDSKEEPER_ID, LANTERN_ID, TOOL_CHEST_ID, WAYSTONE_ID,
    WORKSHOP_ID, ORCHARD_PATH_ID, YARD_ID,
    MyravantPlayFixture, UnavailableFixtureDisplacementError,
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
        service_state: FixtureServiceState | None = None,
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
        self._service_state = service_state or FixtureServiceState()

    @property
    def service_state(self) -> FixtureServiceState:
        return self._service_state

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
            service_state=FixtureServiceState(),
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
        args = dict(
            checkpoint_path=checkpoint_path,
            expected_campaign_id=bounded_fixture.campaign_id,
            expected_initial_open_states=bounded_fixture.initial_object_open_states,
            expected_initial_lit_states=bounded_fixture.initial_object_lit_states,
            expected_initial_representation=bounded_fixture.initial_state.representation,
            expected_initial_representation_digest=(
                bounded_fixture.provenance.initial_state_digest
            ),
        )
        try:
            runtime_state, follow_state, service_state = restore_b2a_checkpoint(
                **args
            )
        except PersistentWorldCheckpointFormatError:
            try:
                runtime_state, follow_state = restore_persistent_world_vsm14_checkpoint(
                    **args
                )
            except PersistentWorldCheckpointFormatError:
                base = MyravantPlayApplication.restore(
                    checkpoint_path=checkpoint_path,
                    fixture=bounded_fixture,
                )
                runtime_state = base.runtime_state
                follow_state = create_persistent_world_follow_intent_runtime_state()
            service_state = FixtureServiceState()
        return cls(
            fixture=bounded_fixture,
            runtime_state=runtime_state,
            follow_intent_state=follow_state,
            service_state=service_state,
            checkpoint_path=checkpoint_path,
        )

    def authoritative_digest(self) -> str:
        return digest_b2a_authoritative_state(
            runtime_state=self.runtime_state,
            follow_intent_state=self.follow_intent_state,
            service_state=self.service_state,
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

    def _service_refusal(self, message: str, failure: str) -> PlayApplicationResult:
        digest = self.authoritative_digest()
        return PlayApplicationResult(
            result_type="fixture_service_rejected", message=message,
            authoritative_changed=False, pre_state_digest=digest,
            post_state_digest=digest, failure_class=failure,
        )

    def service_chest_latch(
        self, operation: str, *, method: str = "none",
    ) -> PlayApplicationResult:
        """Only the Yard-located chest can be worked; no remote progress leak."""
        # Servicing requires the Yard worksite, but releasing an already
        # serviced latch travels with the real object to prevent stranded state.
        place = self.current_place_id()
        chest_local = any(
            r.subject_entity_id == TOOL_CHEST_ID
            and r.relation_type == "located_at"
            and r.object_entity_id == place
            for r in self.state.representation.relations
        )
        if not chest_local or (operation != "release" and place != YARD_ID):
            return self._service_refusal(
                "That fixture cannot be serviced from here.",
                "fixture_service_target_not_local",
            )
        if method == "lantern":
            lit = self.object_lit_state(LANTERN_ID)
            lantern_here = any(
                rel.subject_entity_id == LANTERN_ID
                and rel.object_entity_id == YARD_ID
                and rel.relation_type == "located_at"
                for rel in self.state.representation.relations
            )
            if not lantern_here or lit is None or lit.state != "lit":
                return self._service_refusal(
                    "A lit lantern must be placed at this worksite.",
                    "fixture_service_tool_unavailable",
                )
        if operation == "secure":
            open_state = self.object_open_state(TOOL_CHEST_ID)
            if open_state is None or open_state.state != "closed":
                return self._service_refusal(
                    "Close the chest before securing the serviced latch.",
                    "fixture_service_chest_not_closed",
                )
        try:
            _service_transition(self.service_state, operation, method)
        except FixtureServiceError:
            return self._service_refusal(
                "That latch-service action is not available in its current state.",
                "fixture_service_opportunity_unavailable",
            )
        pre_digest = self.authoritative_digest()
        before = self.runtime_state.logical_time_state.logical_position
        time_receipt = ""
        time_result = None
        if operation == "work":
            # Existing WORLD-2 advancement owns all due NPC consequences.
            # No work is credited by ordinary wait; only this route commits
            # a service transition after the qualified work time has passed.
            time_result = self.wait()
            if not time_result.authoritative_changed:
                raise FixtureServiceError("qualified labor time did not commit")
            time_receipt = time_result.receipt_id or ""
        after = self.runtime_state.logical_time_state.logical_position
        cmd_id = f"terminal-fixture-service-{len(self.service_state.events) + 1:06d}"
        next_state, receipt, preview, delta = execute_fixture_service(
            state=self.service_state, command_id=cmd_id,
            operation=operation, method=method,
            actor_id=self.fixture.player_entity_id,
            target_id=TOOL_CHEST_ID, place_id=place,
            logical_before=before, logical_after=after,
            time_receipt_id=time_receipt, qualified=True,
            expected_pre_digest=digest_fixture_service_state(self.service_state),
        )
        self._service_state = next_state
        if operation == "work":
            message = (
                "The tool chest latch is now serviceable."
                if self.service_state.progress == 2
                else "The latch has one durable work contribution; more work remains."
            )
        else:
            message = {
                "abandon": "The unfinished work is abandoned; spent effort remains.",
                "secure": "The serviced latch now secures the closed chest.",
                "release": "The serviced latch is released.",
            }[operation]
        return PlayApplicationResult(
            result_type="fixture_service_committed", message=message,
            authoritative_changed=True, command_id=cmd_id,
            command_fingerprint=receipt.fingerprint,
            preview_id=receipt.preview_id,
            receipt_id=receipt.receipt_id,
            state_delta_id=receipt.state_delta_id,
            consequence_receipt_id=time_receipt or None,
            consequence_state_delta_id=(
                time_result.state_delta_id if time_result else None
            ),
            logical_time_before=before, logical_time_after=after,
            pre_state_digest=pre_digest,
            post_state_digest=self.authoritative_digest(),
        )

    def clear_waystone_route(self, intent: str = "continue") -> PlayApplicationResult:
        """B-2b: timed physical work, stored only in existing placement history.

        The recovered Waystone obstructs Yard east until it is moved onward.
        This is a *different* progression representation from B-2a's asset
        condition: no service counter, recipe, timer, or new material physics.
        """
        place = self.current_place_id()
        local = any(
            rel.relation_type == "located_at"
            and rel.subject_entity_id == WAYSTONE_ID
            and rel.object_entity_id == place
            for rel in self.state.representation.relations
        )
        pre = self.authoritative_digest()
        def response(message: str, failure: str | None = None):
            return PlayApplicationResult(
                result_type="waystone_clearance_status" if failure is None else
                    "waystone_clearance_rejected",
                message=message, authoritative_changed=False,
                pre_state_digest=pre, post_state_digest=pre,
                failure_class=failure,
            )
        if intent not in {"continue", "check", "abandon"}:
            return response("That clearance instruction is unsupported.",
                            "waystone_clearance_intent_unavailable")
        if not local:
            return response(
                "The worksite and waystone are not together here.",
                "waystone_clearance_target_not_local",
            )
        if place not in {ORCHARD_PATH_ID, YARD_ID, WORKSHOP_ID}:
            return response("The route-clearance operation is not licensed here.",
                            "waystone_clearance_unlicensed_place")
        if intent == "abandon":
            return response(
                "You leave the existing waystone placement in place; "
                "any resulting route obstruction remains."
            )
        if place == WORKSHOP_ID:
            return response("The waystone is clear of the Yard east route.")
        # Location authority is not observation authority. A dark-worksite
        # check must not expose the target's current truth from hidden state.
        if place == ORCHARD_PATH_ID and not self._object_currently_observable(
            WAYSTONE_ID
        ):
            return response(
                "The worksite cannot be inspected with the available light.",
                "waystone_clearance_sensing_unavailable",
            )
        if intent == "check":
            return response(
                "The recovered waystone currently obstructs the Yard east route. "
                "It can be pushed north." if place == YARD_ID
                else "The waystone remains on Orchard Path; a lit source is "
                     "needed to identify it before dragging it west."
            )
        # The existing COMP-3 drag requires a presently observable ground
        # target. Reject before advancing logical time, not by revealing any
        # unseen remote target or invented strength/terrain mechanics.
        if not self._object_currently_observable(WAYSTONE_ID):
            return response(
                "The waystone is not presently visible enough for this work.",
                "waystone_clearance_sensing_unavailable",
            )
        method, direction = (
            ("drag", "west") if place == ORCHARD_PATH_ID
            else ("push", "north")
        )
        try:
            destination = self.fixture.object_displacement_destination_for(
                object_entity_id=WAYSTONE_ID,
                source_place_id=place,
                direction=direction, method=method,
            )
        except UnavailableFixtureDisplacementError:
            return response(
                "That transfer is not licensed from this position.",
                "waystone_clearance_route_unavailable",
            )
        if destination not in {YARD_ID, WORKSHOP_ID}:
            return response(
                "That destination is not licensed for this undertaking.",
                "waystone_clearance_destination_unavailable",
            )

        # Commit logical time via existing WORLD-2 owner, then exactly one
        # existing COMP-3 displacement. If the second owner refuses or raises,
        # roll back the in-memory composed root; the terminal has not yet
        # durably acknowledged either transition.
        original_runtime = self._runtime_state
        original_follow = self._follow_intent_state
        original_service = self._service_state
        before = self.runtime_state.logical_time_state.logical_position
        try:
            tick = self.wait()
            if not tick.authoritative_changed:
                raise RuntimeError("clearance work time did not advance")
            displacement = super().displace_object(
                "waystone", direction, method=method
            )
            if not displacement.authoritative_changed:
                self._runtime_state = original_runtime
                self._follow_intent_state = original_follow
                self._service_state = original_service
                return response(
                    "The qualified waystone move did not complete; "
                    "no work time or placement was committed.",
                    displacement.failure_class or
                        "waystone_clearance_displacement_rejected",
                )
        except Exception:
            self._runtime_state = original_runtime
            self._follow_intent_state = original_follow
            self._service_state = original_service
            raise
        return replace(
            displacement,
            result_type="waystone_clearance_committed",
            message=(
                "You drag the waystone west into the Yard. Its new placement "
                "obstructs the east exit until it is moved onward."
                if destination == YARD_ID else
                "You push the waystone north into the Workshop; "
                "the Yard east route is clear."
            ),
            logical_time_before=before,
            logical_time_after=self.runtime_state.logical_time_state.logical_position,
            consequence_receipt_id=tick.receipt_id,
            consequence_state_delta_id=tick.state_delta_id,
            pre_state_digest=pre,
            post_state_digest=self.authoritative_digest(),
        )

    def check_chest_latch(self) -> PlayApplicationResult:
        # Inspection is local to the current physical chest, not the
        # historical servicing worksite; never expose remote condition.
        place = self.current_place_id()
        chest_local = any(
            r.subject_entity_id == TOOL_CHEST_ID
            and r.relation_type == "located_at"
            and r.object_entity_id == place
            for r in self.state.representation.relations
        )
        if not chest_local:
            return self._service_refusal(
                "The service worksite is not accessible here.",
                "fixture_service_target_not_local",
            )
        s = self.service_state
        detail = (
            "serviceable" if s.progress == 2
            else f"unfinished ({s.progress}/2 work contributions)"
        )
        if s.abandoned:
            detail += "; abandoned, with prior effort preserved"
        if s.secured:
            detail += "; chest secured"
        digest = self.authoritative_digest()
        return PlayApplicationResult(
            result_type="fixture_service_status",
            message=f"Tool chest latch: {detail}.",
            authoritative_changed=False, pre_state_digest=digest,
            post_state_digest=digest,
        )

    def open_object(self, object_reference: str) -> PlayApplicationResult:
        if self.service_state.secured:
            try:
                target = self.fixture.resolve_object_reference(object_reference)
            except Exception:
                target = None
            if target == TOOL_CHEST_ID:
                return self._service_refusal(
                    "The serviced chest latch is secured. Release it first.",
                    "fixture_service_latch_secured",
                )
        return super().open_object(object_reference)

    def request_object_state_from_actor(
        self, actor_reference: str, operation: str, object_reference: str
    ) -> PlayApplicationResult:
        if self.service_state.secured and operation.strip().casefold() == "open":
            try:
                target = self.fixture.resolve_object_reference(object_reference)
            except Exception:
                target = None
            if target == TOOL_CHEST_ID:
                return self._service_refusal(
                    "The secured latch prevents opening by request.",
                    "fixture_service_latch_secured",
                )
        return super().request_object_state_from_actor(
            actor_reference, operation, object_reference
        )

    def _world2_object_opportunity_allowed(
        self, *, object_entity_id: str, operation: str,
    ) -> bool:
        # WORLD-2 still prepares/commits its normal time+consequence path,
        # including a receipt for the rejected opportunity. RT-010 asset
        # condition only affects the owner's lawful opportunity check.
        return not (
            self.service_state.secured
            and object_entity_id == TOOL_CHEST_ID
            and operation == "open"
        )

    def save(self) -> PlayApplicationResult:
        if self.checkpoint_path is None:
            raise CheckpointPathRequiredError(
                "save requires --checkpoint or a loaded checkpoint path"
            )
        pre_digest = self.authoritative_digest()
        if self.service_state.events:
            checkpoint_digest = write_b2a_checkpoint(
                runtime_state=self.runtime_state,
                follow_intent_state=self.follow_intent_state,
                service_state=self.service_state,
                checkpoint_path=self.checkpoint_path,
                qualification_evidence=self.fixture.checkpoint_qualification,
            )
        else:
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

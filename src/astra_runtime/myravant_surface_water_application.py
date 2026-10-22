"""#559 declared surface-water actions over the existing RT-010 and actor owners.

No autonomous fluid engine, hidden contact, new clock or distinct material
journal exists; the opt-in fixture binds these owners and their receipt histories.
"""
from dataclasses import replace
import re

from astra_runtime.domain.persistent_world_material import digest
from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_material_application import _transaction
from astra_runtime.myravant_tarrow_surface_water import create_surface_fixture


class SurfaceWaterApplication(ActorApplication):
    checkpoint_format = "myravant.surface-water-actor-time-material-owner-journal"
    replay_methods = (*ActorApplication.replay_methods, "request_blotting")

    @staticmethod
    def default_fixture():
        return create_surface_fixture()

    def _checkpoint_profile(self):
        return {"actors": super()._checkpoint_profile(),
                "surface_policy": self.fixture.surface_policy}

    def _task_complete(self, task):
        if task.kind == "cleaning" and task.method == "blot":
            return dict(self.water_state.water)[task.participants[0]] == 0
        return super()._task_complete(task)

    def _prepare_actor(self, task):
        if task.kind != "cleaning" or task.method != "blot":
            return super()._prepare_actor(task)
        actor = task.actor_id
        profile = self.actor_profile(actor)
        self._scope(profile, task.kind, task.method, task.participants, task.place_id)
        here = self._actor_place_id(actor)
        if here != task.place_id:
            if (here, task.place_id) in profile.routes:
                return "action", ("physical", "move", (task.place_id,))
            return "blocked", "No declared one-edge route reaches the worksite."
        from astra_runtime import myravant_actor_knowledge as knowledge
        if not knowledge._lit(self, actor):
            return "blocked", "The task condition is not perceptible."
        if self._goal_visible_complete(task):
            return "satisfied", None
        surface, tool = task.participants
        need = self._need_custody(actor, tool)
        if need:
            return "action", need
        capacity = next(a.water_capacity for a in self.water_profile.assets if a.id == tool)
        if dict(self.water_state.water)[tool] >= capacity:
            for op, source, vessel in self.water_profile.allowed_pairs:
                if op == "wring" and source == tool and self._visible_for_actor(actor, vessel):
                    intent = ("water", "wring", (tool, vessel))
                    if self._fork()._execute_actor(actor, intent).authoritative_changed:
                        return "action", intent
            return "blocked", "No qualified wringing destination has free capacity."
        return "action", ("water", "blot", (surface, tool))

    def request_blotting(self, actor_reference, surface_reference, tool_reference):
        pre = self.authoritative_digest()
        try:
            actor = self._actor(actor_reference)
            self._route(actor, "request")
            surface = self._resolve_visible_for_actor(actor, surface_reference)
            tool = self._resolve_visible_for_actor(actor, tool_reference)
            scope = self.actor_profile(actor)
            place = self._actor_place_id(actor)
            self._scope(scope, "cleaning", "blot", (surface, tool), place)
            self._accept(actor, "cleaning", "blot", (surface, tool), place,
                         self.fixture.player_entity_id)
            message = self._communicate_status(actor)
            message += " Acceptance reserves no absorbency, water or vessel."
        except ValueError as exc:
            return self._result(str(exc), failure="actor_request_unavailable")
        return self._metadata_result(pre, "request_blotting", actor, message)


SurfaceWaterApplication.request_blotting = _transaction(
    SurfaceWaterApplication.request_blotting, "request_blotting")


def execute_surface_water_request(application, raw):
    from astra_runtime.myravant_tarrow_actors import execute_actor_locality_request
    text = " ".join(raw.strip().casefold().split())
    match = re.fullmatch(r"ask (.+?) to blot (.+?) using (.+)", text)
    if match:
        return "surface-water", application.request_blotting(*match.groups())
    return execute_actor_locality_request(application, raw)

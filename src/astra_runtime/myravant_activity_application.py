"""PLAY-TARROW-ACTIVITY-2: finite cross-goal activity over existing actor owners.

Selection is actor-local and bounded. Work, custody, environmental changes,
WORLD-1 intervals, consent and participation receipts are never owned here.
"""
from dataclasses import asdict, replace
from types import SimpleNamespace

from astra_runtime.myravant_structures_application import StructuresApplication
from astra_runtime.myravant_material_application import _transaction
from astra_runtime.domain import persistent_world_actor_participation as participation
from astra_runtime.domain import persistent_world_continuing_work as work
from astra_runtime.domain.persistent_world_material import digest, placement
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.myravant_actor_activity import (
    ActivityRecord, canonical_activities, replace_record,
)
from astra_runtime.myravant_tarrow_activity import create_activity_fixture


class ActivityApplication(StructuresApplication):
    checkpoint_format = "myravant.activity-2-actor-time-material-owner-journal"
    replay_methods = (*StructuresApplication.replay_methods,
                      "request_activity", "activity_status", "cancel_activity")

    @staticmethod
    def default_fixture():
        return create_activity_fixture()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.activity_records = ()
        self.activity_disclosures = ()
        self._validate_transaction()

    def _checkpoint_profile(self):
        return {"structures": super()._checkpoint_profile(),
                "activity_case": self.fixture.activity_case,
                "programs": [asdict(p) for p in self.fixture.activity_programs],
                "stage_policy": "finite-actor-local-alternatives-later-interval-1",
                "recovery_policy": "owner-qualified-drop-at-admitted-place-1"}

    def authoritative_digest(self):
        parent = super().authoritative_digest()
        if not hasattr(self, "activity_records"):
            return parent
        return digest({"structures": parent,
                       "activities": canonical_activities(
                           self.activity_records, self.fixture.activity_programs,
                           task_records=self.participation_state.records),
                       "disclosures": self.activity_disclosures})

    def _capture_transaction(self):
        return (super()._capture_transaction(), self.activity_records,
                self.activity_disclosures)

    def _restore_transaction(self, snapshot):
        old, self.activity_records, self.activity_disclosures = snapshot
        super()._restore_transaction(old)

    def _validate_transaction(self):
        super()._validate_transaction()
        if not hasattr(self, "activity_records"):
            return
        if self.fixture.activity_case not in {"standard", "contended"}:
            raise ValueError("invalid activity binding")
        for program in self.fixture.activity_programs:
            p = self.actor_profile(program.actor_id)
            for stage in program.stages:
                for option in stage.options:
                    self._scope(p, option.kind, option.method,
                                option.participants, option.place_id)
        actor_receipts = {e[0] for e in self.actor_events}
        actor_receipts.update(t.receipt.receipt_id for t in
                              self.runtime_state.logical_time_state.committed_transitions)
        canonical_activities(self.activity_records, self.fixture.activity_programs,
                             task_records=self.participation_state.records,
                             receipt_ids=actor_receipts)
        for item in self.activity_disclosures:
            if item[0] != self.fixture.player_entity_id or item[1] not in {
                    r.activity_id for r in self.activity_records}:
                raise ValueError("unattributed activity disclosure")

    def _scope(self, profile, kind, method, participants, place):
        if kind == "recovery":
            if (method != "drop" or len(participants) != 1
                    or participants[0] not in {o.entity_id for o in self.fixture.object_presentations}
                    or place not in {p.entity_id for p in self.fixture.place_presentations}):
                raise ValueError("unqualified actor resource recovery")
            return
        return super()._scope(profile, kind, method, participants, place)

    def _task_complete(self, task):
        if task.kind == "recovery":
            r = placement(self.state.representation, task.participants[0])
            return r.relation_type == "located_at" and r.object_entity_id == task.place_id
        return super()._task_complete(task)

    def _goal_visible_complete(self, task):
        if task.kind == "recovery":
            from astra_runtime import myravant_actor_knowledge as knowledge
            return (self._actor_place_id(task.actor_id) == task.place_id
                    and knowledge._lit(self, task.actor_id)
                    and self._visible_for_actor(task.actor_id, task.participants[0])
                    and self._task_complete(task))
        return super()._goal_visible_complete(task)

    def _prepare_actor(self, task):
        if task.kind != "recovery":
            return super()._prepare_actor(task)
        from astra_runtime import myravant_actor_knowledge as knowledge
        actor = task.actor_id
        p = self.actor_profile(actor)
        if not p.willing:
            return "invalidated", None
        self._scope(p, task.kind, task.method, task.participants, task.place_id)
        here = self._actor_place_id(actor)
        if here != task.place_id:
            if (here, task.place_id) in p.routes:
                return "action", ("physical", "move", (task.place_id,))
            return "blocked", "No admitted route reaches the return position."
        if not knowledge._lit(self, actor):
            return "blocked", "The return position cannot currently be inspected."
        obj = task.participants[0]
        if self._goal_visible_complete(task):
            return "satisfied", None
        if not self._visible_for_actor(actor, obj):
            return "blocked", "The task material is not available in this actor's context."
        relation = placement(self.state.representation, obj)
        if relation.relation_type == "carried_by" and relation.object_entity_id == actor:
            return "action", ("physical", "drop", (obj,))
        try:
            need = self._need_custody(actor, obj)
        except ValueError as exc:
            return "blocked", str(exc)
        if need is not None:
            return "action", need
        return "blocked", "The material is not under this actor's control."

    def _program(self, actor, key):
        matches = [p for p in self.fixture.activity_programs
                   if p.actor_id == actor and p.key == key.strip().casefold()]
        if len(matches) != 1:
            raise ValueError("No such declared activity for this actor.")
        return matches[0]

    def _activity(self, actor):
        matches = [r for r in self.activity_records if r.actor_id == actor]
        if not matches:
            raise ValueError("No disclosed activity has been accepted.")
        return matches[-1]

    def _selected_option(self, actor, stage, *, exclude=()):
        """Choose only among actor-qualified declared options, never a hidden stock search."""
        for option in stage.options:
            if option in exclude:
                continue
            candidate = SimpleNamespace(actor_id=actor, kind=option.kind,
                                        method=option.method, participants=option.participants,
                                        place_id=option.place_id)
            try:
                outcome, intent = self._prepare_actor(candidate)
                if outcome == "satisfied":
                    return option
                if outcome == "action":
                    result = self._fork()._execute_actor(actor, intent)
                    if result.authoritative_changed:
                        return option
            except ValueError:
                pass
        return None

    def _start_stage(self, record, option):
        task = self._accept(record.actor_id, option.kind, option.method,
                            option.participants, option.place_id, record.source_actor_id)
        update = replace(record, task_id=task.task_id,
                         task_ids=(*record.task_ids, task.task_id), reason=None)
        self.activity_records = replace_record(self.activity_records, update)
        self._event("activity_stage_admitted", record.actor_id,
                    (record.activity_id, record.stage_index, task.task_id))
        return update

    def _standing(self):
        # Existing source remains in charge of any unrelated standing participation.
        super()._standing()
        for record in tuple(self.activity_records):
            if record.status != "active":
                continue
            p = self.actor_profile(record.actor_id)
            if not p.willing:
                if record.task_id is None:
                    self.activity_records = replace_record(
                        self.activity_records, replace(record, status="withdrawn",
                                                       reason="continued consent unavailable"))
                    self._event("activity_withdrawal", record.actor_id, record.activity_id)
                continue
            program = self._program(record.actor_id, record.program_key)
            if record.stage_index >= len(program.stages):
                continue
            stage = program.stages[record.stage_index]
            if record.task_id is None:
                try:
                    other = participation.selected(self.participation_state, record.actor_id)
                    if other.status in {"active", "blocked", "paused"}:
                        continue
                except participation.ParticipationRefusal:
                    pass
                chosen = self._selected_option(record.actor_id, stage) or stage.options[0]
                self._start_stage(record, chosen)
                continue
            current = next(t for t in self.participation_state.records if t.task_id == record.task_id)
            if current.status != "blocked":
                continue
            used = tuple(m for m in stage.options if any(
                (t.kind, t.method, t.participants, t.place_id)
                == (m.kind, m.method, m.participants, m.place_id)
                for t in self.participation_state.records if t.task_id in record.task_ids))
            alternate = self._selected_option(record.actor_id, stage, exclude=used)
            if alternate is None:
                continue
            self.participation_state = participation.withdraw(
                self.participation_state, record.actor_id,
                reason="actor chose another admitted method after blocked due interval")
            self._event("activity_method_changed", record.actor_id,
                        (record.activity_id, current.task_id, alternate.method))
            self._start_stage(record, alternate)

    def _interval(self, name, args=(), kwargs=None, contribution=False):
        outcome = super()._interval(name, args=args, kwargs=kwargs,
                                    contribution=contribution)
        if not outcome.authoritative_changed:
            return outcome
        for record in tuple(self.activity_records):
            if record.status != "active" or record.task_id is None:
                continue
            task = next(t for t in self.participation_state.records if t.task_id == record.task_id)
            if task.status in {"completed", "externally_satisfied"}:
                receipt = task.contributions[-1] if task.status == "completed" else None
                done = (*record.stages_finished, (record.stage_index, task.task_id,
                                                   task.status, receipt))
                index = record.stage_index + 1
                program = self._program(record.actor_id, record.program_key)
                finished = index == len(program.stages)
                self.activity_records = replace_record(
                    self.activity_records, replace(record, stage_index=index, task_id=None,
                                                   stages_finished=done,
                                                   status="completed" if finished else "active"))
                self._event("activity_stage_finished", record.actor_id,
                            (record.activity_id, index-1, task.task_id, task.status))
            elif task.status == "withdrawn":
                self.activity_records = replace_record(
                    self.activity_records, replace(record, task_id=None,
                                                   status="withdrawn", reason=task.reason))
                self._event("activity_withdrawal", record.actor_id,
                            (record.activity_id, task.task_id))
        return replace(outcome, post_state_digest=self.authoritative_digest())

    def _disclose_activity(self, record):
        program = self._program(record.actor_id, record.program_key)
        active = None
        if record.task_id:
            active = next(t for t in self.participation_state.records
                          if t.task_id == record.task_id)
        status = active.status if active is not None and record.status == "active" else record.status
        reason = active.reason if active and active.reason else record.reason
        message = (self.fixture.entity_name(record.actor_id) + " reports " + status
                   + " for " + program.key + "; "
                   + str(len(record.stages_finished)) + "/" + str(len(program.stages))
                   + " actual stages resolved. This is last communicated status, not remote observation.")
        if reason:
            message += " Reason: " + reason
        self.activity_disclosures = (*self.activity_disclosures,
            (self.fixture.player_entity_id, record.activity_id, status,
             len(record.stages_finished), reason,
             self.runtime_state.logical_time_state.logical_position))
        return message

    def request_activity(self, actor_reference, activity_reference):
        before = self.authoritative_digest()
        try:
            actor = self._actor(actor_reference)
            self._route(actor, "request")
            program = self._program(actor, activity_reference)
            if not self.actor_profile(actor).willing:
                raise ValueError("The actor declines this activity.")
            if any(r.actor_id == actor and r.status == "active" for r in self.activity_records):
                raise ValueError("The actor has an existing active activity.")
            try:
                other = participation.selected(self.participation_state, actor)
                if other.status in {"active", "paused", "blocked"}:
                    raise ValueError("The actor is busy with selected work.")
            except participation.ParticipationRefusal:
                pass
            first = program.stages[0].options[0]
            if not self._visible_for_actor(actor, first.participants[0]):
                raise ValueError("The proposed work target is not perceptible to this actor.")
            token = digest([before, actor, program.key, len(self.activity_records)])[:28]
            accepted = self._event("activity_acceptance", actor,
                                   (self.fixture.player_entity_id, program.key))
            record = ActivityRecord(build_record_id("actor_activity", token), actor,
                                    program.key, self.fixture.player_entity_id, accepted)
            self.activity_records = (*self.activity_records, record)
            message = self._disclose_activity(record)
            message += " Acceptance performs no work and reserves no tools."
        except ValueError as exc:
            return self._result(str(exc), failure="activity_request_unavailable")
        return self._metadata_result(before, "request_activity", actor, message)

    def activity_status(self, actor_reference):
        before = self.authoritative_digest()
        try:
            actor = self._actor(actor_reference)
            record = self._activity(actor)
            try:
                self._route(actor, "status")
            except ValueError:
                prior = [d for d in self.activity_disclosures if d[1] == record.activity_id]
                if not prior:
                    raise ValueError("No last communicated activity is available.")
                last = prior[-1]
                return self._result("Last communicated activity: " + last[2]
                                    + ", " + str(last[3]) +
                                    " resolved stage(s). Current remote state is unavailable.")
            message = self._disclose_activity(record)
        except ValueError as exc:
            return self._result(str(exc), failure="activity_status_unavailable")
        return self._metadata_result(before, "activity_status", actor, message)

    def cancel_activity(self, actor_reference):
        before = self.authoritative_digest()
        try:
            actor = self._actor(actor_reference)
            self._route(actor, "control")
            record = self._activity(actor)
            if record.status != "active" or record.source_actor_id != self.fixture.player_entity_id:
                raise ValueError("This player cannot cancel that activity.")
            if not self.actor_profile(actor).willing:
                raise ValueError("The actor does not accept this cancellation.")
            if record.task_id is not None:
                self.participation_state = participation.withdraw(
                    self.participation_state, actor, reason="actor accepts activity cancellation")
            self.activity_records = replace_record(
                self.activity_records, replace(record, task_id=None, status="withdrawn",
                                               reason="actor accepts activity cancellation"))
            self._event("activity_cancelled", actor, record.activity_id)
            message = self._disclose_activity(self._activity(actor))
        except ValueError as exc:
            return self._result(str(exc), failure="activity_cancel_unavailable")
        return self._metadata_result(before, "cancel_activity", actor, message)


for _name in ("request_activity", "activity_status", "cancel_activity"):
    setattr(ActivityApplication, _name,
            _transaction(getattr(ActivityApplication, _name), _name))

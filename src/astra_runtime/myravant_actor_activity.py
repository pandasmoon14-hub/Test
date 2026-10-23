"""Noncanonical, finite actor activity declarations and source-bound stage history.

Activity metadata records *which existing owner goal is being pursued*; it does
not own material, physical custody, knowledge, time or the actual work outcome.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class ActivityMethod:
    kind: str
    method: str
    participants: tuple[str, ...]
    place_id: str

    def __post_init__(self):
        if self.kind not in {"cleaning", "assembly", "recovery"}:
            raise ValueError("unknown activity stage family")
        if (not self.method or not self.place_id
                or type(self.participants) is not tuple
                or not self.participants
                or any(type(x) is not str or not x for x in self.participants)):
            raise ValueError("complete activity method required")
        if self.kind == "recovery" and (self.method != "drop" or len(self.participants) != 1):
            raise ValueError("recovery is qualified one-object return to place")


@dataclass(frozen=True)
class ActivityStage:
    options: tuple[ActivityMethod, ...]

    def __post_init__(self):
        if (type(self.options) is not tuple or not 1 <= len(self.options) <= 3
                or any(type(x) is not ActivityMethod for x in self.options)
                or len(set(self.options)) != len(self.options)
                or len({x.kind for x in self.options}) != 1):
            raise ValueError("bounded same-purpose alternatives required")


@dataclass(frozen=True)
class ActivityProgram:
    key: str
    actor_id: str
    stages: tuple[ActivityStage, ...]

    def __post_init__(self):
        if (type(self.key) is not str or not self.key or type(self.actor_id) is not str
                or not self.actor_id or type(self.stages) is not tuple
                or not 2 <= len(self.stages) <= 4
                or any(type(x) is not ActivityStage for x in self.stages)):
            raise ValueError("bounded activity program required")
        kinds = {m.kind for stage in self.stages for m in stage.options}
        if not {"cleaning", "assembly"} <= kinds:
            raise ValueError("activity requires genuinely distinct work families")
        if any((len({x.place_id for x in stage.options}) != 1 or
                len({x.participants[0] for x in stage.options}) != 1)
                for stage in self.stages):
            raise ValueError("alternatives must preserve the same goal and place")


@dataclass(frozen=True)
class ActivityRecord:
    activity_id: str
    actor_id: str
    program_key: str
    source_actor_id: str
    accepted_receipt: str
    stage_index: int = 0
    task_id: str | None = None
    task_ids: tuple[str, ...] = ()
    stages_finished: tuple[tuple[int, str, str, str | None], ...] = ()
    status: str = "active"
    reason: str | None = None

    def __post_init__(self):
        if (not all(type(x) is str and x for x in (
                self.activity_id, self.actor_id, self.program_key,
                self.source_actor_id, self.accepted_receipt))
                or type(self.stage_index) is not int or self.stage_index < 0
                or self.status not in {"active", "completed", "withdrawn"}
                or type(self.task_ids) is not tuple
                or len(self.task_ids) != len(set(self.task_ids))
                or (self.task_id is not None and self.task_id not in self.task_ids)):
            raise ValueError("invalid durable activity record")


def replace_record(records, update):
    return tuple(update if r.activity_id == update.activity_id else r for r in records)


def canonical_activities(records, programs, *, task_records=(), receipt_ids=None):
    if type(records) is not tuple or any(type(r) is not ActivityRecord for r in records):
        raise ValueError("immutable activities required")
    program_map = {(p.actor_id, p.key): p for p in programs}
    task_map = {t.task_id: t for t in task_records}
    if len(program_map) != len(programs) or len({r.activity_id for r in records}) != len(records):
        raise ValueError("duplicate program or activity identity")
    active = [r.actor_id for r in records if r.status == "active"]
    if len(active) != len(set(active)):
        raise ValueError("one active activity per actor")
    used_tasks = []
    for r in records:
        program = program_map.get((r.actor_id, r.program_key))
        if program is None or r.stage_index > len(program.stages):
            raise ValueError("activity profile binding differs from admission")
        if r.status == "completed" and (r.stage_index != len(program.stages) or r.task_id is not None):
            raise ValueError("incomplete activity cannot claim completed")
        if r.task_id is not None and r.status != "active":
            raise ValueError("terminal activity cannot have active stage")
        if receipt_ids is not None and r.accepted_receipt not in receipt_ids:
            raise ValueError("unknown activity acceptance receipt")
        used_tasks.extend(r.task_ids)
        for task_id in r.task_ids:
            task = task_map.get(task_id)
            if task is None or task.actor_id != r.actor_id:
                raise ValueError("activity stage lacks actor-specific owner task")
            if not any((task.kind, task.method, task.participants, task.place_id)
                       == (m.kind, m.method, m.participants, m.place_id)
                       for s in program.stages for m in s.options):
                raise ValueError("activity stage exceeds declared program")
        finished = [x[0] for x in r.stages_finished]
        if (finished != list(range(len(finished))) or len(finished) > len(program.stages)
                or r.stage_index != len(finished)):
            raise ValueError("nonsequential activity stage history")
        for index, task_id, status, receipt in r.stages_finished:
            task = task_map.get(task_id)
            if (task is None or task.status != status
                    or status not in {"completed", "externally_satisfied"}
                    or (receipt is not None and receipt not in task.contributions)):
                raise ValueError("activity conclusion not grounded in physical owner")
            if status == "completed" and receipt is None:
                raise ValueError("actor-completed stage requires own contribution")
    if len(used_tasks) != len(set(used_tasks)):
        raise ValueError("one owner task cannot serve two activities")
    return [{"activity_id": r.activity_id, "actor_id": r.actor_id, "program_key": r.program_key,
             "source_actor_id": r.source_actor_id, "accepted_receipt": r.accepted_receipt,
             "stage_index": r.stage_index, "task_id": r.task_id, "task_ids": list(r.task_ids),
             "stages_finished": [list(x) for x in r.stages_finished],
             "status": r.status, "reason": r.reason} for r in records]

"""Bounded AFQR-03 continuing-work declarations for PLAY-TARROW-TIME-1.

This module records lifecycle and references to committed RT-010 contributions.
It does not advance time, execute material methods, calculate progress, or decide
completion/opportunity. Those decisions remain with the calling owners.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import AbstractSet


class ContinuingWorkRefusal(ValueError):
    """A refused lifecycle request leaves its immutable input unchanged."""


_STATUSES = frozenset(("active", "paused", "blocked", "completed", "abandoned"))
_NONTERMINAL = frozenset(("active", "paused", "blocked"))


def _identity(value: object) -> bool:
    return type(value) is str and bool(value.strip())


@dataclass(frozen=True)
class WorkTask:
    task_id: str
    actor_id: str
    kind: str
    method: str
    participants: tuple[str, ...]
    place_id: str
    status: str = "active"
    contributions: tuple[str, ...] = ()
    reason: str | None = None

    def __post_init__(self) -> None:
        if not all(_identity(value) for value in
                   (self.task_id, self.actor_id, self.method, self.place_id)):
            raise ValueError("task identities and method must be nonempty text")
        if self.kind not in ("cleaning", "assembly") or self.status not in _STATUSES:
            raise ValueError("unknown work kind or lifecycle status")
        for name in ("participants", "contributions"):
            values = getattr(self, name)
            if (type(values) is not tuple or any(not _identity(v) for v in values)
                    or len(set(values)) != len(values)):
                raise ValueError("work references must be distinct immutable identities")
        if not self.participants:
            raise ValueError("work must declare participants")
        if self.reason is not None and not _identity(self.reason):
            raise ValueError("reason must be nonempty text")
        if self.status == "blocked" and self.reason is None:
            raise ValueError("blocked work needs an explicit reason")
        if self.status in ("active", "completed") and self.reason is not None:
            raise ValueError("active and completed work cannot retain a blocking reason")
        if self.status == "completed" and not self.contributions:
            raise ValueError("completion requires a committed contribution")


@dataclass(frozen=True)
class WorkState:
    tasks: tuple[WorkTask, ...] = ()
    selected_task_id: str | None = None

    def __post_init__(self) -> None:
        if type(self.tasks) is not tuple or any(type(t) is not WorkTask for t in self.tasks):
            raise ValueError("work state requires immutable task records")
        ids = tuple(t.task_id for t in self.tasks)
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate task identity")
        if self.selected_task_id is not None and self.selected_task_id not in ids:
            raise ValueError("selected task is missing")
        pending = tuple(t for t in self.tasks if t.status in _NONTERMINAL)
        if len(pending) > 1 or (pending and pending[0].task_id != self.selected_task_id):
            raise ValueError("only the selected task may remain nonterminal")
        receipts = tuple(r for t in self.tasks for r in t.contributions)
        if len(set(receipts)) != len(receipts):
            raise ValueError("a contribution cannot belong to multiple tasks")


def selected(state: WorkState) -> WorkTask:
    if type(state) is not WorkState:
        raise ValueError("invalid work state")
    for task in state.tasks:
        if task.task_id == state.selected_task_id:
            return task
    raise ContinuingWorkRefusal("no selected work")


def _replace(state: WorkState, task: WorkTask) -> WorkState:
    return WorkState(tuple(task if old.task_id == task.task_id else old
                           for old in state.tasks), state.selected_task_id)


def start(state: WorkState, task: WorkTask) -> WorkState:
    if type(state) is not WorkState or type(task) is not WorkTask:
        raise ValueError("invalid work declaration")
    if any(old.status in _NONTERMINAL for old in state.tasks):
        raise ContinuingWorkRefusal("finish or abandon selected work first")
    if task.status != "active" or task.contributions or task.reason is not None:
        raise ContinuingWorkRefusal("new work must start active without contributions")
    if any(old.task_id == task.task_id for old in state.tasks):
        raise ContinuingWorkRefusal("task identity already exists")
    return WorkState(state.tasks + (task,), task.task_id)


def pause(state: WorkState) -> WorkState:
    task = selected(state)
    if task.status != "active":
        raise ContinuingWorkRefusal("only active work can pause")
    return _replace(state, replace(task, status="paused", reason=None))


def resume(state: WorkState, *, qualified: bool) -> WorkState:
    task = selected(state)
    if type(qualified) is not bool:
        raise ValueError("qualification must be explicit boolean")
    if task.status not in ("paused", "blocked") or not qualified:
        raise ContinuingWorkRefusal("work is not qualified to resume")
    return _replace(state, replace(task, status="active", reason=None))


def abandon(state: WorkState) -> WorkState:
    task = selected(state)
    if task.status not in _NONTERMINAL:
        raise ContinuingWorkRefusal("terminal work cannot be abandoned")
    return _replace(state, replace(task, status="abandoned", reason=None))


def block(state: WorkState, reason: str) -> WorkState:
    task = selected(state)
    if task.status != "active":
        raise ContinuingWorkRefusal("only active work can become blocked")
    return _replace(state, replace(task, status="blocked", reason=reason))


def move_outside(state: WorkState, place_id: str) -> WorkState:
    """Pause active work on departure; movement remains caller-owned."""
    if not _identity(place_id):
        raise ValueError("destination must be explicit")
    if state.selected_task_id is None:
        return state
    task = selected(state)
    return pause(state) if task.status == "active" and place_id != task.place_id else state


def record_contribution(state: WorkState, receipt_id: str, *, completed: bool) -> WorkState:
    """Reference one actual committed step and the owner's completion predicate."""
    task = selected(state)
    if type(completed) is not bool or not _identity(receipt_id):
        raise ValueError("explicit receipt and completion predicate required")
    if task.status != "active":
        raise ContinuingWorkRefusal("only active work accepts contributions")
    if any(receipt_id in old.contributions for old in state.tasks):
        raise ContinuingWorkRefusal("contribution already recorded")
    return _replace(state, replace(task, contributions=task.contributions + (receipt_id,),
                                   status="completed" if completed else "active"))


def canonical_state(state: WorkState, *, participant_ids: AbstractSet[str] | None = None,
                    receipt_ids: AbstractSet[str] | None = None) -> dict[str, object]:
    """Return stable primitive projection, optionally checking external references."""
    if type(state) is not WorkState:
        raise ValueError("invalid work state")
    # Revalidate even records supplied through deserialization/reflection.
    checked = WorkState(tuple(replace(t) for t in state.tasks), state.selected_task_id)
    for task in checked.tasks:
        if participant_ids is not None and not set(task.participants) <= participant_ids:
            raise ValueError("unknown work participant")
        if receipt_ids is not None and not set(task.contributions) <= receipt_ids:
            raise ValueError("unknown committed contribution")
    return {"selected_task_id": checked.selected_task_id, "tasks": [
        {"task_id": t.task_id, "actor_id": t.actor_id, "kind": t.kind,
         "method": t.method, "participants": list(t.participants), "place_id": t.place_id,
         "status": t.status, "contributions": list(t.contributions), "reason": t.reason}
        for t in checked.tasks]}

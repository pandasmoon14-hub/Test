"""Bounded AFQR-11/12 participation declarations, not consent or action authority.

The caller qualifies voluntary agreement, eligibility, opportunity and actual
contributions. This module records their immutable lifecycle without a clock,
world access, resource reservation, or autonomous execution.
"""
from __future__ import annotations
from dataclasses import dataclass, replace


class ParticipationRefusal(ValueError):
    """A refused declaration leaves the supplied state unchanged."""


def _text(value: object) -> bool:
    return type(value) is str and bool(value.strip()) and len(value) <= 512


def _bool(value: object) -> None:
    if type(value) is not bool:
        raise ValueError("qualification must be explicit boolean")


@dataclass(frozen=True)
class ParticipationProfile:
    actor_id: str
    blocked_limit: int = 3

    def __post_init__(self) -> None:
        if not _text(self.actor_id) or type(self.blocked_limit) is not int or not 1 <= self.blocked_limit <= 32:
            raise ValueError("actor and bounded positive blocked limit required")


_NONTERMINAL = frozenset(("active", "paused", "blocked"))
_STATUSES = _NONTERMINAL | {"completed", "externally_satisfied", "withdrawn"}


@dataclass(frozen=True)
class Participation:
    task_id: str
    actor_id: str
    source_actor_id: str
    kind: str
    method: str
    participants: tuple[str, ...]
    place_id: str
    accepted_receipt: str
    eligible_after: str
    tick: int
    status: str = "active"
    blocked_due: int = 0
    contributions: tuple[str, ...] = ()
    reason: str | None = None
    due_intervals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value in (self.task_id, self.actor_id, self.source_actor_id, self.kind, self.method,
                      self.place_id, self.accepted_receipt, self.eligible_after):
            if not _text(value):
                raise ValueError("participation identities must be bounded nonempty text")
        if self.kind not in ("cleaning", "assembly") or self.status not in _STATUSES:
            raise ValueError("unknown participation kind or status")
        if type(self.tick) is not int or self.tick < 0 or type(self.blocked_due) is not int or not 0 <= self.blocked_due <= 32:
            raise ValueError("invalid participation counters")
        for values in (self.participants, self.contributions, self.due_intervals):
            if type(values) is not tuple or not all(_text(v) for v in values) or len(set(values)) != len(values):
                raise ValueError("references must be distinct immutable identities")
        if not self.participants or (self.reason is not None and not _text(self.reason)):
            raise ValueError("participants and any reason must be explicit")
        if self.status == "completed" and not self.contributions:
            raise ValueError("completion requires an actual contribution")


@dataclass(frozen=True)
class ParticipationState:
    records: tuple[Participation, ...] = ()
    commands: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if type(self.records) is not tuple or any(type(r) is not Participation for r in self.records):
            raise ValueError("immutable participation records required")
        ids = tuple(r.task_id for r in self.records)
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate task identity")
        active = tuple(r.actor_id for r in self.records if r.status in _NONTERMINAL)
        if len(set(active)) != len(active):
            raise ValueError("only one nonterminal participation per actor")
        if type(self.commands) is not tuple or not all(_text(v) for v in self.commands) or len(set(self.commands)) != len(self.commands):
            raise ValueError("distinct immutable command identities required")
        receipts = tuple(v for r in self.records for v in r.contributions)
        if len(set(receipts)) != len(receipts):
            raise ValueError("one contribution cannot serve two tasks")


def selected(state: ParticipationState, actor_id: str) -> Participation:
    for record in reversed(state.records):
        if record.actor_id == actor_id:
            return record
    raise ParticipationRefusal("actor has no participation")


def _replace(state: ParticipationState, record: Participation) -> ParticipationState:
    return replace(state, records=tuple(record if r.task_id == record.task_id else r for r in state.records))


def accept(state: ParticipationState, record: Participation, command_id: str, *, qualified: bool) -> ParticipationState:
    _bool(qualified)
    if not _text(command_id):
        raise ValueError("command identity required")
    if command_id in state.commands:
        raise ParticipationRefusal("command already recorded")
    if not qualified:
        raise ParticipationRefusal("voluntary participation is not qualified")
    if record.status != "active" or record.contributions or record.due_intervals or record.blocked_due or record.reason:
        raise ParticipationRefusal("acceptance requires a fresh active declaration")
    return ParticipationState(state.records + (record,), state.commands + (command_id,))


def pause(state: ParticipationState, actor_id: str) -> ParticipationState:
    record = selected(state, actor_id)
    if record.status not in ("active", "blocked"):
        raise ParticipationRefusal("participation cannot pause")
    return _replace(state, replace(record, status="paused", reason=None))


def resume(state: ParticipationState, actor_id: str, *, qualified: bool) -> ParticipationState:
    _bool(qualified)
    record = selected(state, actor_id)
    if not qualified or record.status not in ("paused", "blocked"):
        raise ParticipationRefusal("participation cannot resume")
    return _replace(state, replace(record, status="active", reason=None))


def withdraw(state: ParticipationState, actor_id: str, *, reason: str) -> ParticipationState:
    record = selected(state, actor_id)
    if record.status not in _NONTERMINAL:
        raise ParticipationRefusal("participation is already terminal")
    return _replace(state, replace(record, status="withdrawn", reason=reason))


def resolve_due(state: ParticipationState, actor_id: str, interval_id: str, tick: int, *,
                outcome: str, qualified: bool, profile: ParticipationProfile,
                receipt_id: str | None = None, completed: bool = False,
                reason: str | None = None, externally_satisfied: bool = False) -> ParticipationState:
    """Record one caller-qualified due interval; no-due and paused state do not age.

    ``qualified`` confirms that this interval follows the acceptance predecessor
    and is due under the caller's schedule. It is not inferred from a tick.
    """
    _bool(qualified)
    _bool(completed)
    _bool(externally_satisfied)
    if externally_satisfied and (outcome != 'contributed' or completed):
        raise ValueError('external satisfaction after preparation cannot claim goal completion')
    record = selected(state, actor_id)
    if profile.actor_id != actor_id or not _text(interval_id) or type(tick) is not int or tick <= record.tick:
        raise ValueError("explicit actor profile and later interval required")
    if interval_id == record.eligible_after or interval_id in record.due_intervals:
        raise ParticipationRefusal("interval is predecessor or already recorded")
    if not qualified or record.status == "paused":
        return state
    if record.status not in ("active", "blocked"):
        raise ParticipationRefusal("terminal participation cannot contribute")
    update = {"due_intervals": record.due_intervals + (interval_id,)}
    if outcome == "contributed":
        if not _text(receipt_id) or any(receipt_id in r.contributions for r in state.records):
            raise ParticipationRefusal("fresh committed contribution required")
        update.update(contributions=record.contributions + (receipt_id,), blocked_due=0,
                      status="externally_satisfied" if externally_satisfied else "completed" if completed else "active",
                      reason=(reason or 'goal observed satisfied after preparation') if externally_satisfied else None)
    elif outcome == "blocked":
        if not _text(reason):
            raise ValueError("blocked due interval needs reason")
        count = record.blocked_due + 1
        update.update(blocked_due=count, status="withdrawn" if count >= profile.blocked_limit else "blocked", reason=reason)
    elif outcome in ("satisfied", "invalidated"):
        update.update(status="externally_satisfied" if outcome == "satisfied" else "withdrawn", reason=reason)
    else:
        raise ValueError("unknown due outcome")
    if outcome != "contributed" and (receipt_id is not None or completed):
        raise ValueError("noncontribution cannot claim a receipt or completion")
    return _replace(state, replace(record, **update))


def canonical_state(state: ParticipationState, *, actor_ids=None, participant_ids=None, receipt_ids=None) -> dict:
    checked = ParticipationState(tuple(replace(r) for r in state.records), state.commands)
    for r in checked.records:
        if actor_ids is not None and not {r.actor_id, r.source_actor_id} <= actor_ids:
            raise ValueError("unknown actor reference")
        if participant_ids is not None and not set(r.participants) <= participant_ids:
            raise ValueError("unknown participant reference")
        if receipt_ids is not None and not {r.accepted_receipt, *r.contributions} <= receipt_ids:
            raise ValueError("unknown receipt reference")
    return {"records": [{name: list(value) if type(value) is tuple else value
                         for name, value in vars(r).items()} for r in checked.records],
            "commands": list(checked.commands)}

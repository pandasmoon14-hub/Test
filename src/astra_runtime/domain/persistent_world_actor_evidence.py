"""Private AFQR-10 evidence history with explicit AFQR-20/14 qualification.

Events retain observation versus report versus performance provenance. They do
not establish universal truth or deliver communication, and are never a public
projection. Callers qualify sensing and communication before admission.
"""
from __future__ import annotations
from dataclasses import dataclass, replace


def _text(value: object) -> bool:
    return type(value) is str and bool(value.strip()) and len(value) <= 512


def _value(value: object) -> bool:
    return ((type(value) is str and len(value) <= 512)
            or (type(value) is tuple and len(value) <= 32 and all(type(v) is str and len(v) <= 512 for v in value)))


@dataclass(frozen=True)
class EvidenceEvent:
    event_id: str
    actor_id: str
    kind: str
    source_actor_id: str
    target_id: str
    facet: str
    value: str | tuple[str, ...]
    tick: int
    receipt_id: str
    qualification: str
    origin_tick: int | None = None
    source_event_id: str | None = None

    def __post_init__(self) -> None:
        if not all(_text(v) for v in (self.event_id, self.actor_id, self.source_actor_id,
                                     self.target_id, self.facet, self.receipt_id, self.qualification)):
            raise ValueError("bounded explicit evidence identities required")
        if self.kind not in ("witnessed", "reported", "performed") or not _value(self.value):
            raise ValueError("invalid evidence kind or bounded immutable value")
        if type(self.tick) is not int or self.tick < 0:
            raise ValueError("nonnegative evidence tick required")
        if self.origin_tick is not None and (type(self.origin_tick) is not int or not 0 <= self.origin_tick <= self.tick):
            raise ValueError("historical origin tick must precede delivery")
        if self.source_event_id is not None and not _text(self.source_event_id):
            raise ValueError("source event identity must be explicit")
        if self.kind in ("witnessed", "performed") and self.source_actor_id != self.actor_id:
            raise ValueError("direct evidence must retain the observing or performing actor")


@dataclass(frozen=True)
class EvidenceState:
    events: tuple[EvidenceEvent, ...] = ()

    def __post_init__(self) -> None:
        if type(self.events) is not tuple or any(type(e) is not EvidenceEvent for e in self.events):
            raise ValueError("immutable evidence records required")
        ids = tuple(e.event_id for e in self.events)
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate evidence event")
        if any(a.tick > b.tick for a, b in zip(self.events, self.events[1:])):
            raise ValueError("evidence history must remain chronological")


def record(state: EvidenceState, event: EvidenceEvent, *, qualified: bool) -> EvidenceState:
    if type(qualified) is not bool:
        raise ValueError("qualification must be explicit boolean")
    if not qualified:
        raise ValueError("evidence admission is not qualified")
    previous = next((e for e in state.events if e.event_id == event.event_id), None)
    if previous is not None:
        if previous != event:
            raise ValueError("evidence identity reused with different provenance")
        return state
    return EvidenceState(state.events + (event,))


def latest(state: EvidenceState, actor_id: str, target_id: str, facet: str) -> EvidenceEvent | None:
    """Return this actor's last retained evidence, including source and age."""
    return next((e for e in reversed(state.events)
                 if (e.actor_id, e.target_id, e.facet) == (actor_id, target_id, facet)), None)


def canonical_state(state: EvidenceState, *, actor_ids=None, target_ids=None, receipt_ids=None) -> dict:
    checked = EvidenceState(tuple(replace(e) for e in state.events))
    for e in checked.events:
        if actor_ids is not None and not {e.actor_id, e.source_actor_id} <= actor_ids:
            raise ValueError("unknown actor reference")
        if target_ids is not None and e.target_id not in target_ids:
            raise ValueError("unknown target reference")
        if receipt_ids is not None and e.receipt_id not in receipt_ids:
            raise ValueError("unknown receipt reference")
    return {"events": [{name: list(value) if type(value) is tuple else value
                        for name, value in vars(e).items()} for e in checked.events]}

"""Exact, immutable AFQR-17 drying and RT-010 deposit handoffs (#546).

Location qualification, logical-time ordering and trace projection are supplied
by callers. This module reads no clock and infers no material physics.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
import hashlib
import json
from typing import Mapping

from . import persistent_world_water_cleaning as wc


def _fraction(value: object) -> Fraction:
    if type(value) not in (int, Fraction) or value < 0:
        raise ValueError("expected nonnegative exact quantity")
    return Fraction(value)


def _text(value: object) -> bool:
    return type(value) is str and bool(value)


@dataclass(frozen=True)
class TimedEnvironmentProfile:
    absorbents: tuple[str, ...]
    exposures: tuple[tuple[str, Fraction, str], ...]
    schedule: tuple[tuple[int, str, Fraction, str], ...] = ()

    def __post_init__(self) -> None:
        if type(self.absorbents) is not tuple or not self.absorbents or any(not _text(x) for x in self.absorbents) or len(set(self.absorbents)) != len(self.absorbents):
            raise ValueError("distinct absorbent identities required")
        if type(self.exposures) is not tuple or type(self.schedule) is not tuple:
            raise ValueError("immutable environmental profile required")
        exposures = []
        for entry in self.exposures:
            if type(entry) is not tuple or len(entry) != 3:
                raise ValueError("invalid exposure")
            place, rate, label = entry
            if not _text(place) or not _text(label):
                raise ValueError("invalid exposure identity/label")
            exposures.append((place, _fraction(rate), label))
        places = {p for p, _, _ in exposures}
        if not places or len(places) != len(exposures):
            raise ValueError("distinct exposure positions required")
        scheduled = []
        for entry in self.schedule:
            if type(entry) is not tuple or len(entry) != 4:
                raise ValueError("invalid exposure schedule")
            tick, place, rate, label = entry
            if type(tick) is not int or tick < 0 or place not in places or not _text(label):
                raise ValueError("invalid scheduled condition")
            scheduled.append((tick, place, _fraction(rate), label))
        if len({(t, p) for t, p, _, _ in scheduled}) != len(scheduled):
            raise ValueError("duplicate scheduled boundary")
        object.__setattr__(self, "absorbents", tuple(sorted(self.absorbents)))
        object.__setattr__(self, "exposures", tuple(sorted(exposures)))
        object.__setattr__(self, "schedule", tuple(sorted(scheduled)))


@dataclass(frozen=True)
class Trace:
    id: str
    subject: str
    kind: str
    receipt: str
    tick: int
    place: str

    def __post_init__(self) -> None:
        if any(not _text(v) for v in (self.id, self.subject, self.kind, self.receipt, self.place)) or type(self.tick) is not int or self.tick < 0:
            raise ValueError("invalid physical trace provenance")


@dataclass(frozen=True)
class TimedEnvironmentState:
    credits: tuple[tuple[str, Fraction], ...]
    deposits: tuple[tuple[str, Fraction], ...]
    evaporated: tuple[tuple[str, int], ...]
    traces: tuple[Trace, ...] = ()

    def __post_init__(self) -> None:
        for name in ("credits", "deposits", "evaporated"):
            entries = getattr(self, name)
            if type(entries) is not tuple:
                raise ValueError("immutable environmental compartments required")
            normalized = []
            for entry in entries:
                if type(entry) is not tuple or len(entry) != 2 or not _text(entry[0]):
                    raise ValueError("invalid environmental compartment")
                key, value = entry
                if name == "evaporated":
                    if type(value) is not int or value < 0:
                        raise ValueError("invalid environmental water")
                else:
                    value = _fraction(value)
                normalized.append((key, value))
            if len({key for key, _ in normalized}) != len(normalized):
                raise ValueError("duplicate compartment identity")
            object.__setattr__(self, name, tuple(sorted(normalized)))
        if type(self.traces) is not tuple or any(type(t) is not Trace for t in self.traces) or len({t.id for t in self.traces}) != len(self.traces):
            raise ValueError("invalid trace collection")


def initial_environment(profile: TimedEnvironmentProfile) -> TimedEnvironmentState:
    zero = tuple((key, Fraction(0)) for key in profile.absorbents)
    return TimedEnvironmentState(zero, zero, tuple((p, 0) for p, _, _ in profile.exposures))


def validate_environment(water: wc.WaterCleaningState, env: TimedEnvironmentState,
                         profile: TimedEnvironmentProfile) -> None:
    if type(env) is not TimedEnvironmentState or type(profile) is not TimedEnvironmentProfile or type(water) is not wc.WaterCleaningState:
        raise ValueError("invalid environmental state/profile")
    ids = set(profile.absorbents)
    if set(dict(env.credits)) != ids or set(dict(env.deposits)) != ids or not ids <= set(dict(water.water)):
        raise ValueError("environment must name complete absorbent compartments")
    if set(dict(env.evaporated)) != {p for p, _, _ in profile.exposures}:
        raise ValueError("environment must name complete exposure positions")
    stock = dict(water.water)
    if any(value >= 1 or (not stock[key] and value) for key, value in env.credits):
        raise ValueError("invalid fractional drying credit")


def add_trace(env: TimedEnvironmentState, subject: str, kind: str,
              receipt: str, tick: int, place: str) -> TimedEnvironmentState:
    identity = hashlib.sha256(json.dumps([subject, kind, receipt, tick, place], separators=(",", ":"), ensure_ascii=True).encode()).hexdigest()
    trace = Trace(identity, subject, kind, receipt, tick, place)
    if trace in env.traces:
        return env
    return replace(env, traces=env.traces + (trace,))


def advance_environment(water: wc.WaterCleaningState, env: TimedEnvironmentState,
                        profile: TimedEnvironmentProfile,
                        exposures: Mapping[str, str | None], tick: int,
                        cause_id: str) -> tuple[wc.WaterCleaningState, TimedEnvironmentState]:
    """Advance exactly one caller-committed interval ending at ``tick``."""
    validate_environment(water, env, profile)
    if type(tick) is not int or tick < 1 or not _text(cause_id) or set(exposures) != set(profile.absorbents):
        raise ValueError("complete interval exposure and provenance required")
    rates = {p: rate for p, rate, _ in profile.exposures}
    for due, place, rate, _ in profile.schedule:
        if due <= tick - 1:
            rates[place] = rate
    stock, adhered, suspended = map(dict, (water.water, water.adhered, water.suspended))
    credits, deposits, evaporated = map(dict, (env.credits, env.deposits, env.evaporated))
    result_env = env
    for subject in profile.absorbents:
        place = exposures[subject]
        if place is not None and place not in rates:
            raise ValueError("unqualified exposure position")
        if not stock[subject]:
            credits[subject] = Fraction(0)
            continue
        if place is None:
            continue
        earned = credits[subject] + rates[place]
        removed = min(stock[subject], earned.numerator // earned.denominator)
        stock[subject] -= removed
        evaporated[place] += removed
        credits[subject] = earned - removed if stock[subject] else Fraction(0)
        if not stock[subject]:
            deposits[subject] += suspended[subject]
            suspended[subject] = Fraction(0)
        if removed:
            result_env = add_trace(result_env, subject, "drying", cause_id, tick, place)
    result = wc.WaterCleaningState(tuple(stock.items()), tuple(adhered.items()), tuple(suspended.items()))
    result_env = replace(result_env, credits=tuple(credits.items()), deposits=tuple(deposits.items()), evaporated=tuple(evaporated.items()))
    validate_environment(result, result_env, profile)
    if wc.total_water(water) + sum(dict(env.evaporated).values()) != wc.total_water(result) + sum(evaporated.values()) or wc.total_residue(water) + sum(dict(env.deposits).values()) != wc.total_residue(result) + sum(deposits.values()):
        raise AssertionError("environment conservation failure")
    return result, result_env


def execute_with_deposits(water: wc.WaterCleaningState, env: TimedEnvironmentState,
                          water_profile: wc.WaterCleaningProfile, operation: str,
                          participants: tuple[str, str], amount: int | None = None
                          ) -> tuple[wc.WaterCleaningState, TimedEnvironmentState]:
    """Extend qualified washing/collection to deposited dirt without changing v1."""
    wc.validate(water, water_profile)
    if type(participants) is not tuple or len(participants) != 2 or (operation, *participants) not in water_profile.allowed_pairs:
        raise wc.WaterCleaningRefusal("operation pair is not declared")
    source, target = participants
    deposits = dict(env.deposits)
    assets = {a.id: a for a in water_profile.assets}
    stock, adhered, suspended = map(dict, (water.water, water.adhered, water.suspended))
    if operation not in ("pour", "spill") and amount is not None:
        raise wc.WaterCleaningRefusal("this method does not accept a quantity")
    if operation in ("wipe", "scrub"):
        if operation == "wipe" and not stock[target]:
            raise wc.WaterCleaningRefusal("wiping requires retained water")
        moved = min(adhered[source], max(Fraction(0), assets[target].residue_capacity - adhered[target] - deposits.get(target, 0)), assets[target].transfer_rate)
        if moved <= 0:
            raise wc.WaterCleaningRefusal("no removable residue can be transferred")
        adhered[source] -= moved
        adhered[target] += moved
    elif operation == "rinse" and deposits.get(source, 0):
        if not stock[target]:
            raise wc.WaterCleaningRefusal("rinsing requires bath water")
        mixed = suspended[source] + suspended[target] + adhered[source] + deposits[source]
        total = stock[source] + stock[target]
        adhered[source] = Fraction(0)
        deposits[source] = Fraction(0)
        suspended[source] = mixed * Fraction(stock[source], total)
        suspended[target] = mixed * Fraction(stock[target], total)
    elif operation in ("collect", "shake") and deposits.get(source, 0):
        moved = adhered[source] + deposits[source]
        if adhered[target] + moved > assets[target].residue_capacity:
            raise wc.WaterCleaningRefusal("insufficient residue capacity")
        adhered[target] += moved
        adhered[source] = deposits[source] = Fraction(0)
    else:
        result = wc.execute(water, water_profile, operation, participants, amount)
        # Liquid removal clears any credit; newly added moisture cannot inherit
        # credit from a previously empty absorbent.
        new_stock = dict(result.water)
        credits = tuple((key, value if dict(water.water)[key] and new_stock[key] else Fraction(0)) for key, value in env.credits)
        return result, replace(env, credits=credits)
    result = wc.WaterCleaningState(tuple(stock.items()), tuple(adhered.items()), tuple(suspended.items()))
    wc.validate(result, water_profile)
    result_env = replace(env, deposits=tuple(deposits.items()))
    if wc.total_water(result) != wc.total_water(water) or wc.total_residue(result) + sum(deposits.values()) != wc.total_residue(water) + sum(dict(env.deposits).values()):
        raise AssertionError("deposit handoff conservation failure")
    return result, result_env


def canonical_environment(state: TimedEnvironmentState) -> dict:
    return {"credits": [[k, [v.numerator, v.denominator]] for k, v in state.credits],
            "deposits": [[k, [v.numerator, v.denominator]] for k, v in state.deposits],
            "evaporated": [[k, v] for k, v in state.evaporated],
            "traces": [[t.id, t.subject, t.kind, t.receipt, t.tick, t.place] for t in state.traces]}


def canonical_profile(profile: TimedEnvironmentProfile) -> dict:
    return {"absorbents": list(profile.absorbents),
            "exposures": [[p, [r.numerator, r.denominator], label] for p, r, label in profile.exposures],
            "schedule": [[t, p, [r.numerator, r.denominator], label] for t, p, r, label in profile.schedule]}


def environment_from_canonical(payload: Mapping) -> TimedEnvironmentState:
    if not isinstance(payload, Mapping) or set(payload) != {"credits", "deposits", "evaporated", "traces"} or any(type(payload[k]) is not list for k in payload):
        raise ValueError("invalid environmental envelope")
    def fractions(name: str) -> tuple:
        result = []
        for entry in payload[name]:
            if type(entry) is not list or len(entry) != 2:
                raise ValueError("invalid exact compartment")
            key, value = entry
            if type(value) is not list or len(value) != 2 or any(type(x) is not int for x in value) or value[0] < 0 or value[1] <= 0:
                raise ValueError("invalid exact fraction")
            result.append((key, Fraction(*value)))
        return tuple(result)
    try:
        result = TimedEnvironmentState(fractions("credits"), fractions("deposits"), tuple(tuple(e) for e in payload["evaporated"]), tuple(Trace(*e) for e in payload["traces"]))
    except (TypeError, IndexError) as exc:
        raise ValueError("invalid environmental envelope") from exc
    if canonical_environment(result) != dict(payload):
        raise ValueError("noncanonical environmental envelope")
    return result

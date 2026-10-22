"""Bounded RT-010 water and two-compartment residue transitions (#544).

Opportunity, placement, observation and commitment remain application-owned.
All quantities are explicit development profile facts, never inferred physics.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping


class WaterCleaningRefusal(ValueError):
    """An invalid or zero-effect operation; its input state is unchanged."""


def _integer(value: object) -> bool:
    return type(value) is int


def _quantity(value: object) -> Fraction:
    if type(value) not in (int, Fraction):
        raise ValueError("residue must be an exact integer or Fraction")
    result = Fraction(value)
    if result < 0:
        raise ValueError("negative residue")
    return result


@dataclass(frozen=True)
class WaterCleaningAsset:
    id: str
    kind: str
    water_capacity: int = 0
    residue_capacity: Fraction = Fraction(0)
    transfer_rate: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id:
            raise ValueError("asset identity must be nonempty text")
        if self.kind not in ("vessel", "absorbent", "brush", "surface", "tray"):
            raise ValueError("unknown water/cleaning kind")
        if not _integer(self.water_capacity) or self.water_capacity < 0:
            raise ValueError("water capacity must be a nonnegative integer")
        if self.kind not in ("vessel", "absorbent", "surface") and self.water_capacity:
            raise ValueError("only vessels and absorbents hold water")
        object.__setattr__(self, "residue_capacity", _quantity(self.residue_capacity))
        object.__setattr__(self, "transfer_rate", _quantity(self.transfer_rate))


_KINDS = {
    "pour": (("vessel",), ("vessel",)),
    "spill": (("vessel",), ("surface",)),
    "scoop": (("surface",), ("vessel",)),
    "blot": (("surface",), ("absorbent",)),
    "press": (("absorbent",), ("absorbent",)),
    "fill": (("vessel",), ("vessel",)),
    "empty": (("vessel",), ("vessel",)),
    "soak": (("vessel",), ("absorbent",)),
    "wipe": (("surface",), ("absorbent",)),
    "scrub": (("surface",), ("brush",)),
    "rinse": (("absorbent", "brush"), ("vessel",)),
    "wring": (("absorbent",), ("vessel",)),
    "collect": (("absorbent", "brush"), ("tray",)),
    "shake": (("absorbent", "brush"), ("tray",)),
}


@dataclass(frozen=True)
class WaterCleaningProfile:
    assets: tuple[WaterCleaningAsset, ...]
    allowed_pairs: tuple[tuple[str, str, str], ...]

    def __post_init__(self) -> None:
        if type(self.assets) is not tuple or type(self.allowed_pairs) is not tuple:
            raise ValueError("profiles must contain immutable tuples")
        if any(type(asset) is not WaterCleaningAsset for asset in self.assets):
            raise ValueError("invalid profile asset")
        assets = {asset.id: asset for asset in self.assets}
        if len(assets) != len(self.assets) or not assets:
            raise ValueError("profile needs distinct asset identities")
        for pair in self.allowed_pairs:
            if type(pair) is not tuple or len(pair) != 3 or any(type(part) is not str for part in pair):
                raise ValueError("invalid operation pair")
            operation, source, target = pair
            if operation not in _KINDS or source not in assets or target not in assets or source == target:
                raise ValueError("invalid operation participant")
            kinds = _KINDS[operation]
            if assets[source].kind not in kinds[0] or assets[target].kind not in kinds[1]:
                raise ValueError("operation incompatible with declared kinds")
        if len(set(self.allowed_pairs)) != len(self.allowed_pairs):
            raise ValueError("duplicate allowed pair")


@dataclass(frozen=True)
class WaterCleaningState:
    water: tuple[tuple[str, int], ...]
    adhered: tuple[tuple[str, Fraction], ...]
    suspended: tuple[tuple[str, Fraction], ...]

    def __post_init__(self) -> None:
        for name in ("water", "adhered", "suspended"):
            values = getattr(self, name)
            if type(values) is not tuple:
                raise ValueError("state compartments must be immutable tuples")
            seen: set[str] = set()
            normalized = []
            for entry in values:
                if type(entry) is not tuple or len(entry) != 2:
                    raise ValueError("invalid state entry")
                key, value = entry
                if not isinstance(key, str) or not key or key in seen:
                    raise ValueError("invalid or repeated state identity")
                seen.add(key)
                if name == "water":
                    if not _integer(value) or value < 0:
                        raise ValueError("water must be a nonnegative integer")
                else:
                    value = _quantity(value)
                normalized.append((key, value))
            object.__setattr__(self, name, tuple(sorted(normalized)))


def validate(state: WaterCleaningState, profile: WaterCleaningProfile) -> None:
    """Validate complete tracked compartments against an immutable profile."""
    if type(state) is not WaterCleaningState or type(profile) is not WaterCleaningProfile:
        raise ValueError("invalid state or profile")
    assets = {asset.id: asset for asset in profile.assets}
    water, adhered, suspended = map(dict, (state.water, state.adhered, state.suspended))
    if any(set(compartment) != set(assets) for compartment in (water, adhered, suspended)):
        raise ValueError("state must name every profile asset exactly once")
    for key, asset in assets.items():
        if water[key] > asset.water_capacity:
            raise ValueError("water capacity exceeded")
        if adhered[key] > asset.residue_capacity:
            raise ValueError("adhered residue capacity exceeded")
        if not water[key] and suspended[key]:
            raise ValueError("suspended residue requires retained water")


def total_water(state: WaterCleaningState) -> int:
    return sum(value for _, value in state.water)


def total_residue(state: WaterCleaningState) -> Fraction:
    return sum((value for _, value in state.adhered + state.suspended), Fraction(0))


def execute(state: WaterCleaningState, profile: WaterCleaningProfile, operation: str,
            participants: tuple[str, str], amount: int | None = None) -> WaterCleaningState:
    """Apply one declared operation; no input mutation, I/O or implicit sinks.

    Participants are source then target. For wipe/scrub this is surface then
    tool; for rinse this is tool then bath; for soak this is vessel then cloth.
    Only pour and deliberate surface spill accept an explicit amount. All other amounts refuse.
    """
    validate(state, profile)
    if type(participants) is not tuple or len(participants) != 2 or any(type(p) is not str for p in participants):
        raise WaterCleaningRefusal("two explicit participants required")
    source, target = participants
    if (operation, source, target) not in profile.allowed_pairs:
        raise WaterCleaningRefusal("operation pair is not declared")
    if operation in ("pour", "spill"):
        if not _integer(amount) or amount <= 0:
            raise WaterCleaningRefusal("pour requires a positive integer quantity")
    elif amount is not None:
        raise WaterCleaningRefusal("this method does not accept a quantity")
    assets = {asset.id: asset for asset in profile.assets}
    water, adhered, suspended = map(dict, (state.water, state.adhered, state.suspended))

    def liquid(quantity: int) -> None:
        if quantity <= 0:
            raise WaterCleaningRefusal("no water can be transferred")
        if quantity > water[source]:
            raise WaterCleaningRefusal("insufficient source water")
        if quantity + water[target] > assets[target].water_capacity:
            raise WaterCleaningRefusal("insufficient recipient capacity")
        residue = suspended[source] * Fraction(quantity, water[source])
        water[source] -= quantity
        water[target] += quantity
        suspended[source] -= residue
        suspended[target] += residue

    if operation in ("pour", "spill"):
        liquid(amount)
    elif operation in ("scoop", "blot", "press"):
        # Surface recovery and contact are explicit. Rates are declared whole-unit
        # upper bounds; no rounding or fractional-water sink is admitted.
        asset = assets[source] if operation == "scoop" else assets[target]
        rate = asset.transfer_rate.numerator // asset.transfer_rate.denominator
        liquid(min(water[source], assets[target].water_capacity - water[target], rate))
    elif operation == "fill":
        liquid(min(water[source], assets[target].water_capacity - water[target]))
    elif operation in ("empty", "wring"):
        liquid(water[source])
    elif operation == "soak":
        liquid(1)
    elif operation in ("wipe", "scrub"):
        if operation == "wipe" and not water[target]:
            raise WaterCleaningRefusal("wiping requires retained water")
        moved = min(adhered[source], assets[target].residue_capacity - adhered[target], assets[target].transfer_rate)
        if moved <= 0:
            raise WaterCleaningRefusal("no removable residue can be transferred")
        adhered[source] -= moved
        adhered[target] += moved
    elif operation == "rinse":
        if not water[target]:
            raise WaterCleaningRefusal("rinsing requires bath water")
        mixed = suspended[source] + suspended[target] + adhered[source]
        combined_water = water[source] + water[target]
        adhered[source] = Fraction(0)
        suspended[source] = mixed * Fraction(water[source], combined_water)
        suspended[target] = mixed * Fraction(water[target], combined_water)
    elif operation in ("collect", "shake"):
        if not adhered[source]:
            raise WaterCleaningRefusal("no adhered residue to collect")
        if adhered[source] + adhered[target] > assets[target].residue_capacity:
            raise WaterCleaningRefusal("insufficient residue capacity")
        adhered[target] += adhered[source]
        adhered[source] = Fraction(0)
    result = WaterCleaningState(tuple(water.items()), tuple(adhered.items()), tuple(suspended.items()))
    validate(result, profile)
    if result == state:
        raise WaterCleaningRefusal("operation has no effect")
    if total_water(result) != total_water(state) or total_residue(result) != total_residue(state):
        raise AssertionError("water/cleaning transition violated conservation")
    return result


def canonical_state(state: WaterCleaningState) -> dict:
    """Return deterministic JSON-compatible exact compartment values."""
    return {
        "water": [[key, value] for key, value in state.water],
        "adhered": [[key, [value.numerator, value.denominator]] for key, value in state.adhered],
        "suspended": [[key, [value.numerator, value.denominator]] for key, value in state.suspended],
    }


def state_from_canonical(payload: Mapping) -> WaterCleaningState:
    """Decode canonical state strictly; profile validation is a separate step."""
    if not isinstance(payload, Mapping) or set(payload) != {"water", "adhered", "suspended"}:
        raise ValueError("invalid water/cleaning state envelope")
    compartments = {}
    for name in ("water", "adhered", "suspended"):
        entries = payload[name]
        if type(entries) is not list:
            raise ValueError("canonical compartment must be a list")
        values = []
        for entry in entries:
            if type(entry) is not list or len(entry) != 2:
                raise ValueError("invalid canonical entry")
            key, value = entry
            if name != "water":
                if (type(value) is not list or len(value) != 2 or
                        not all(_integer(part) for part in value) or value[0] < 0 or value[1] <= 0):
                    raise ValueError("invalid canonical residue fraction")
                fraction = Fraction(*value)
                if [fraction.numerator, fraction.denominator] != value:
                    raise ValueError("residue fraction is not canonical")
                value = fraction
            values.append((key, value))
        compartments[name] = tuple(values)
    result = WaterCleaningState(**compartments)
    if canonical_state(result) != dict(payload):
        raise ValueError("state entries are not in canonical order")
    return result

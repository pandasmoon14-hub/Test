"""Approved #565: bounded noncanonical worksite generation over existing owners.

Constructed content is an admitted neutral fixture, not canon or world truth.
Historical events come only from qualified owner procedures. Restoring a
checkpoint replays its actual history and never invokes this history builder.
"""
from dataclasses import dataclass
from pathlib import Path

from astra_runtime.domain.persistent_world_material import active_effects, placement
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_investigation_neutral import _build_neutral
from astra_runtime.myravant_tarrow_investigation import InvestigationFixture


FAMILY = "generated-worksite-1"
CASES = ("access", "resources", "evidence")


class UnsatisfiableLocality(ValueError):
    """Explicitly inconsistent input constraints."""


class InvalidLocality(ValueError):
    """Rejected output or lawful-history candidate."""


class LocalityBudgetExhausted(ValueError):
    """Finite candidate construction budget is exhausted."""


@dataclass(frozen=True)
class LocalityRecipe:
    case: str
    seed: int = 0
    budget: int = 1
    family: str = FAMILY
    require_unobstructed_direct_route: bool = False

    def __post_init__(self):
        if (type(self.case) is not str or self.case not in CASES
                or type(self.seed) is not int or not 0 <= self.seed <= 65535
                or type(self.budget) is not int or not 0 <= self.budget <= 16
                or self.family != FAMILY
                or type(self.require_unobstructed_direct_route) is not bool):
            raise ValueError("unsupported locality construction input or profile version")
        if self.case == "access" and self.require_unobstructed_direct_route:
            raise UnsatisfiableLocality(
                "admitted barrier history conflicts with required direct clearance")


def create_generated_locality_fixture(recipe: LocalityRecipe):
    """Detached deterministic admission using the existing actor/material owners."""
    if type(recipe) is not LocalityRecipe:
        raise ValueError("immutable versioned locality recipe required")
    if recipe.budget == 0:
        raise LocalityBudgetExhausted("no candidate construction attempts remain")
    try:
        root = _build_neutral(
            reverse=bool(recipe.seed % 2), standing=recipe.case == "resources",
            generated_case=recipe.case, generated_seed=recipe.seed)
        fixture = InvestigationFixture(**root.__dict__)
        # The application runs cross-domain owner validation against this root
        # before any session gets an authoritative reference to it.
        InvestigationApplication.new(fixture=fixture, checkpoint_path=None)
        return fixture
    except (ValueError, TypeError) as exc:
        raise InvalidLocality("detached generated candidate failed admission") from exc


def build_generated_locality(recipe: LocalityRecipe, checkpoint_path=None):
    """Execute qualified prehistory before publishing the playable campaign."""
    path = Path(checkpoint_path) if checkpoint_path is not None else None
    if path is not None and path.exists():
        raise ValueError("an existing checkpoint must be restored, not regenerated")
    fixture = create_generated_locality_fixture(recipe)
    app = InvestigationApplication.new(fixture=fixture, checkpoint_path=None)
    if recipe.case == "access":
        operations = (
            ("move", ("east",)),
            ("material", ("put_on", "Plate", "Bench")),
            ("material", ("put_on", "Peg", "Bench")),
            ("material", ("tie", "Plate", "Peg", "Cord")),
        )
    elif recipe.case == "resources":
        operations = (("wait", ()),)
    else:
        speaker = "Sol" if recipe.seed % 2 else "Jun"
        operations = (
            ("move", ("east",)),
            ("tell_actor", (speaker, "panel a", "residue", "clear")),
            ("ask_report", (speaker, "panel a", "residue")),
        )
    receipts = []
    for method, args in operations:
        result = getattr(app, method)(*args)
        if (not result.authoritative_changed or result.failure_class
                or not result.receipt_id):
            raise InvalidLocality("declared owner history did not execute: " + method)
        receipts.append((method, result.receipt_id))
    if recipe.case == "access":
        if not any(effect.kind == "movement" and effect.direction == "north"
                   for effect in active_effects(app.state.representation,
                                                app.connections, fixture.material_profile)):
            raise InvalidLocality("physical obstruction is absent from committed history")
    elif recipe.case == "resources":
        brush = next(p.entity_id for p in fixture.object_presentations
                     if p.name == "Brush")
        if placement(app.state.representation, brush).object_entity_id != fixture.actor_order[0]:
            raise InvalidLocality("contested stock was not physically acquired")
    elif not app.disclosed_relays:
        raise InvalidLocality("evidence case has no lawful disclosed report")
    if path is not None:
        app.checkpoint_path = path
        save = app.save()
        if save.failure_class:
            raise InvalidLocality("accepted history could not be saved")
        restored = InvestigationApplication.restore(fixture=fixture, checkpoint_path=path)
        if restored.authoritative_digest() != app.authoritative_digest():
            raise InvalidLocality("saved history does not reproduce the accepted root")
        app = restored
    return app, tuple(receipts)

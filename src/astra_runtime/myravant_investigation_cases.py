"""Construct causal investigation prehistories using existing owner operations.

This developer tool does not set memory/world truths by fiat. Every case is
an immutable validated root plus executed, receipted game actions. Calling it
twice with the same recipe creates the same history; restoring uses the saved
journal and never invokes this constructor.
"""
from pathlib import Path

from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_tarrow_investigation import create_investigation_fixture
from astra_runtime.domain.persistent_world_material import placement


PREHISTORIES = {
    "neutral-contended": (("wait", ()),),
    "neutral-reverse": (("wait", ()),),
    "neutral-relay": (
        ("move", ("east",)),
        ("tell_actor", ("Jun", "panel a", "residue", "clear")),
        ("ask_report", ("Jun", "panel a", "residue")),
    ),
}


def build_investigation_case(recipe, checkpoint_path):
    if recipe not in PREHISTORIES:
        raise ValueError("no approved neutral development-history recipe")
    checkpoint_path = Path(checkpoint_path)
    if checkpoint_path.exists():
        raise ValueError("generation refuses an existing checkpoint; restore it")
    fixture = create_investigation_fixture(recipe)
    app = InvestigationApplication.new(fixture=fixture, checkpoint_path=checkpoint_path)
    receipts = []
    for method, arguments in PREHISTORIES[recipe]:
        result = getattr(app, method)(*arguments)
        if not result.authoritative_changed or result.failure_class or not result.receipt_id:
            raise ValueError("lawfully executed case history failed: " + method +
                             " / " + str(result.message))
        receipts.append((method, result.receipt_id))
    # Check the actual durable checkpoint, rather than trusting the builder's
    # in-memory proposal; restore must follow committed journal history.
    restored = InvestigationApplication.restore(fixture=fixture,
                                                 checkpoint_path=checkpoint_path)
    if restored.authoritative_digest() != app.authoritative_digest():
        raise ValueError("prepared case differs from durable replay")
    if not receipts or not restored.journal:
        raise ValueError("empty or unreceipted case history")
    if recipe == "neutral-relay":
        if not restored.disclosed_relays:
            raise ValueError("relay history lacks actual disclosed provenance")
        panel = next(p.entity_id for p in fixture.object_presentations
                     if p.name == "Panel A")
        if not dict(restored.water_state.adhered)[panel]:
            raise ValueError("false report has no real contrary material state")
    else:
        brush = next(p.entity_id for p in fixture.object_presentations
                     if p.name == "Brush")
        if placement(restored.state.representation, brush).object_entity_id != fixture.actor_order[0]:
            raise ValueError("finite contested brush was not lawfully acquired")
    return restored, tuple(receipts)

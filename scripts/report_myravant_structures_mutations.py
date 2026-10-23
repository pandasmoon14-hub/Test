"""Isolated #561 failure injections; independent assertions, not blind play."""
import argparse
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

from astra_runtime.domain.persistent_world_material import active_effects, validate_joint, MaterialError
from astra_runtime.myravant_actor_physical import execute_actor_physical
from astra_runtime.myravant_structures_application import StructuresApplication
from astra_runtime.myravant_tarrow_structures import create_structures_fixture, cover_subjects
from astra_runtime.myravant_tarrow import identity


def run():
    fixture = create_structures_fixture()
    a = StructuresApplication.new(fixture=fixture)
    for direction in ("south", "west"):
        assert a.move(direction).authoritative_changed
    for thing in ("work panel", "barrier crossbar"):
        assert a.pickup(thing).authoritative_changed
        assert a.material("put_on", thing, "yard work trestle").authoritative_changed
    assert a.pickup("work cord").authoritative_changed
    assert a.material("tie", "work panel", "barrier crossbar", "work cord").authoritative_changed
    assert any(e.kind == "movement" and e.source == identity("yard-tools")
               for e in active_effects(a.state.representation, a.connections, a.material_profile))
    cases = {}

    # Mutation 1: removed attachment cannot leave a cached blocked-passage bit.
    missing = ()
    cases["stale_obstruction_detected"] = not any(
        e.kind == "movement" for e in active_effects(a.state.representation, missing, a.material_profile))

    # Mutation 2: reusing a whole fastener cannot manufacture a second join.
    forged = (*a.connections, a.connections[0])
    try:
        validate_joint(a.state.representation, forged, a.material_profile)
    except MaterialError:
        cases["duplicate_join_detected"] = True
    else:
        cases["duplicate_join_detected"] = False

    # Mutation 3: the live actor owner must refuse a formerly traversable edge.
    before = a.authoritative_digest()
    result = execute_actor_physical(a, identity("tali"), "move", identity("yard-sorting"))
    cases["actor_obstruction_detected"] = (
        not result.authoritative_changed and a.authoritative_digest() == before)

    # Mutation 4: an unqualified faster drying cover must fail profile validation.
    try:
        replace(fixture.cover_profile, rate=Fraction(2)).validate(fixture)
    except ValueError:
        cases["unqualified_drying_rate_detected"] = True
    else:
        cases["unqualified_drying_rate_detected"] = False

    # Mutation 5: one profile has sight and movement separately, never aliased.
    cases["sight_not_inferred_from_barrier"] = not any(
        e.kind == "sight" for e in active_effects(a.state.representation, a.connections, a.material_profile))

    # Controls: authentic obstruction persists and an unattached cover is inert.
    cases["control_real_obstruction"] = any(
        e.kind == "movement" for e in active_effects(a.state.representation, a.connections, a.material_profile))
    cases["control_unbuilt_cover_inert"] = not cover_subjects(
        a.state.representation, a.connections, fixture.cover_profile)
    assert all(cases.values()), cases
    return cases


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {"source": "PLAY-TARROW-STRUCTURES-1",
              "engineering_authored": True, "mutations": run()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Structures: five injected failures and two controls detected.")

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
from report_myravant_specialist_mutations import run_mutations

# Unlike direct negative-state probes below, these are isolated source-copy
# fault injections. Each passes its unchanged control, changes one specific
# owner/adapter expression, and MUST fail the associated focused assertion.
SOURCE_MUTATIONS = (
    ("cover_connection_gate_ignored", "myravant_tarrow_structures.py",
     "or not any((c.left, c.right, c.fastener, c.method)",
     "or True or not any((c.left, c.right, c.fastener, c.method)",
     "test_cover_reduces_only_qualified_drying_with_conserved_compartments"),
    ("timed_cover_handoff_dropped", "myravant_timed_application.py",
     "rate_overrides=self._exposure_rate_overrides(exposures))",
     "rate_overrides=None)",
     "test_cover_reduces_only_qualified_drying_with_conserved_compartments"),
    ("actor_material_barrier_bypassed", "myravant_actor_physical.py",
     "if any(e.kind == 'movement' and e.source == here and e.direction == route.direction",
     "if False and any(e.kind == 'movement' and e.source == here and e.direction == route.direction",
     "test_actor_uses_same_live_partition_and_cannot_bypass_player_block"),
)


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
    probes = run()
    source = run_mutations(Path(__file__).resolve().parents[1],
                           mutations=SOURCE_MUTATIONS,
                           test_filename="test_play_tarrow_structures.py")
    assert len(source["mutations"]) == 3
    result = {"source": "PLAY-TARROW-STRUCTURES-1",
              "engineering_authored": True, "negative_state_probes": probes,
              "source_fault_injections": source,
              "scope": "three isolated source mutations, each with an unmutated control"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("Structures: five input-state probes, two controls and three isolated source mutations passed.")

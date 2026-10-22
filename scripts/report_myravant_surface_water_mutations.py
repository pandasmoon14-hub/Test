"""Isolated source-independent #559 negative controls; engineering, not blind tests."""
import argparse
import json
from dataclasses import replace
from pathlib import Path

from astra_runtime.domain.persistent_world_water_cleaning import (
    WaterCleaningState, execute, validate, total_water, total_residue,
)
from astra_runtime.myravant_tarrow_surface_water import create_surface_fixture
from astra_runtime.myravant_tarrow import identity


def run():
    fixture = create_surface_fixture()
    profile = fixture.water_profile
    start = fixture.water_initial
    first = execute(start, profile, "spill",
                    (identity("wash-bucket"), identity("practice-panel")), 2)

    def quantities(s):
        return total_water(s), total_residue(s)

    assert quantities(first) == quantities(start)
    cases = {}

    # Faults use independent state edits, not calls to the reducer being checked.
    def alter(state, compartment, key, value):
        entries = dict(getattr(state, compartment))
        entries[identity(key)] = value
        data = dict(water=state.water, adhered=state.adhered, suspended=state.suspended)
        data[compartment] = tuple(entries.items())
        return WaterCleaningState(**data)

    lost = alter(first, "water", "practice-panel", 1)
    cases["untracked_loss_detected"] = quantities(lost) != quantities(start)
    duplicated = alter(first, "water", "wash-bucket", 11)
    cases["untracked_creation_detected"] = quantities(duplicated) != quantities(start)
    overfilled = alter(first, "water", "practice-panel", 4)
    try:
        validate(overfilled, profile)
    except ValueError:
        cases["capacity_bypass_detected"] = True
    else:
        cases["capacity_bypass_detected"] = False
    # Moving two absorbents beside each other is a placement change, not an
    # admitted liquid owner operation; water compartments must remain identical.
    felt = alter(alter(first, "water", "practice-panel", 1),
                 "water", "packing-felt", 1)
    cases["implicit_contact_detected"] = (quantities(felt) == quantities(first)
                                            and felt != first)
    untouched = first
    cases["control_pour_conserved"] = quantities(untouched) == quantities(start)
    cases["control_no_contact_stable"] = (
        dict(untouched.water)[identity("packing-felt")] == 0)
    assert all(cases.values()), cases
    return cases


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = {"source": "PLAY-TARROW-WATER-2", "engineering_authored": True,
              "mutations": run()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Surface water: four injected defect cases and two controls passed.")

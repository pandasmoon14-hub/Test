"""Isolated negative controls for generated worksite admission and replay."""
import argparse
import json
from pathlib import Path

from report_myravant_specialist_mutations import run_mutations

MUTATIONS = (
    ("skip_finite_budget_rejection", "myravant_generated_locality.py",
     "if recipe.budget == 0:", "if False and recipe.budget == 0:",
     "test_generation_failures_are_bounded_and_distinct"),
    ("skip_existing_campaign_guard", "myravant_generated_locality.py",
     "if path is not None and path.exists():",
     "if False and path is not None and path.exists():",
     "test_existing_state_never_regenerates_and_wrong_binding_rejects"),
    ("drop_material_barrier", "myravant_investigation_neutral.py",
     "if generated_case == 'access':", "if False and generated_case == 'access':",
     "test_access_barrier_is_live_material_and_alternate_route_exists"),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    results = run_mutations(Path(__file__).resolve().parents[1],
                            mutations=MUTATIONS,
                            test_filename="test_play_generated_locality.py")
    assert len(results["mutations"]) == len(MUTATIONS)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "source": "PLAY-TARROW-LOCALITY-GEN-1", "engineering_authored": True,
        "isolated_source_mutations": results,
        "not_blind_acceptance": True}, indent=2, sort_keys=True) + "\n")
    print("Generated worksite: three isolated mutations detected with controls.")


if __name__ == "__main__":
    main()

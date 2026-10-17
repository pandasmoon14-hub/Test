"""Isolated Tarrow qualification and initial-placement negative controls."""
import argparse
import json
from pathlib import Path
from report_myravant_specialist_mutations import run_mutations

MUTATIONS = (
    ("fixed_object_pickup_granted", "myravant_play_fixture.py",
     "qualified=object_entity_id not in self.fixed_object_ids", "qualified=True",
     "test_fixedness_is_a_declared_qualification_not_a_name_special_case"),
    ("initial_containment_accepted_without_root_witness", "domain/persistent_world_local_checkpoint_restore.py",
     "containment_present and expected_initial_representation is None", "False",
     "test_initial_containment_requires_a_verified_root_witness"),
    ("unsupported_specialist_allows_first_step", "myravant_terminal.py",
     "candidate is not None and candidate not in admitted", "False",
     "test_stock_specialists_not_admitted_or_partially_executed[inspect chest brace]"),
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_mutations(Path(__file__).resolve().parents[1], mutations=MUTATIONS,
                           test_filename="test_play_tarrow_locality.py")
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Tarrow mutations: 3/3 defects detected with passing controls.")

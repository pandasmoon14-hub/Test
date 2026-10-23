"""Isolated executable fault injections for the #563 activity candidate.

The runner operates on temporary source copies, first proves the unchanged
control passes, then requires the mutation to cause a named test failure.
"""
import argparse
import json
from pathlib import Path

from report_myravant_specialist_mutations import run_mutations

MUTATIONS = (
    ("skip_real_successor_stage", "myravant_activity_application.py",
     "index = record.stage_index + 1", "index = record.stage_index",
     "test_real_clean_assembly_recovery_chain_and_durable_stage_boundaries"),
    ("ignore_k_withdrawal", "myravant_activity_application.py",
     'elif task.status == "withdrawn":', 'elif False and task.status == "withdrawn":',
     "test_k_blockage_withheld_stock_withdraws_without_minting_or_double_clock"),
    ("relabel_different_targets_as_alternative", "myravant_actor_activity.py",
     "len({x.participants[0] for x in stage.options}) != 1",
     "False",
     "test_stage_alternatives_cannot_change_target_as_if_it_were_a_method"),
    ("recover_unused_cloth_instead_of_scrub_brush", "myravant_activity_application.py",
     "if option.participants == (used,)",
     "if option == stage.options[0]",
     "test_scrub_method_recovers_actual_brush_not_unrelated_cloth"),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    outcome = run_mutations(Path(__file__).resolve().parents[1],
                            mutations=MUTATIONS,
                            test_filename="test_play_tarrow_activity.py")
    assert len(outcome["mutations"]) == 4
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "source": "PLAY-TARROW-ACTIVITY-2",
        "engineering_authored": True, "isolated_source_mutations": outcome,
        "not_blind_acceptance": True,
    }, indent=2, sort_keys=True) + "\n")
    print("Activity: four isolated mutations detected against unchanged controls.")


if __name__ == "__main__":
    main()

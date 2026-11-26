"""Exercise isolated defects in conditional execution and evidence qualification."""

import argparse
import json
from pathlib import Path

from report_myravant_specialist_mutations import run_mutations

MUTATIONS = (
    ("run_consequent_after_false_condition", "myravant_condition_session.py",
     "        if chosen.state != command.expected:", "        if False:",
     "test_named_stale_account_reaches_owner_but_firsthand_does_not"),
    ("lose_source_position_qualification", "myravant_actor_knowledge.py",
     "                 and e.receipt_id in anchor_receipts\n", "",
     "test_scoped_report_requires_same_receipt_from_same_observer"),
    ("stitch_different_observations_into_open_passage", "myravant_condition_methods.py",
     "    if len(events) == count and len(origins) == 1:", "    if len(events) == count:",
     "test_multi_blocker_open_requires_coherent_complete_evidence"),
    ("include_protected_part_in_agreed_work", "myravant_condition_methods.py",
     "    if protected:", "    if False:",
     "test_work_guard_and_prohibition_never_issue_agreement"),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    path = parser.parse_args().output
    report = run_mutations(
        Path(__file__).resolve().parents[1], mutations=MUTATIONS, test_filename="test_play_conditioned_goals.py",
        support_paths=("tests/__init__.py", "tests/test_play_constrained_goals.py",
                       "tests/fixtures/myravant_conditional/expectations.json"),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Detected {len(report['mutations'])} evidence-conditioned goal mutations.")


if __name__ == "__main__":
    main()

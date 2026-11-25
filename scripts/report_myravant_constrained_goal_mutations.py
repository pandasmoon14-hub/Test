"""Negative controls for the admitted goal and limit boundaries."""

import argparse
import json
from pathlib import Path

from report_myravant_specialist_mutations import run_mutations


MUTATIONS = (
    ("treat_feasibility_as_authorization", "myravant_goal_session.py",
     '        if command.speech == "inquiry":\n            yield self.result(self._summarize(options))',
     '        if False:\n            yield self.result(self._summarize(options))',
     "test_feasibility_is_read_only_then_return_has_exact_owner_custody"),
    ("ignore_prohibition_on_asking", "myravant_goal_methods.py",
     "        if limits.no_asking:", "        if False:",
     "test_recovery_dispatches_retrieval_or_voluntary_request"),
    ("spend_reserved_water", "myravant_goal_methods.py",
     "            if limits.reserve and source == limits.reserve[0] and water[source] <= limits.reserve[1]:",
     "            if False:", "test_basin_stop_and_reserve_prevent_draw_then_explicit_revision_allows_it"),
    ("ignore_stop_condition", "myravant_goal_methods.py",
     "            if source == limits.stop_vessel:", "            if False:",
     "test_basin_stop_and_reserve_prevent_draw_then_explicit_revision_allows_it"),
    ("lose_question_after_unmatched_answer", "myravant_player_intentions.py",
     "                self.pending = answering\n                yield self._result",
     "                self.pending = None\n                yield self._result",
     "test_unmatched_answer_keeps_only_pending_clause_across_next_reply"),
    ("route_to_giver_using_private_location", "myravant_goal_methods.py",
     "    site = goal.exchange_place", "    site = context.app.entity_place_id(goal.recipient)",
     "test_travel_interrupts_and_restart_finishes_only_remaining_handoff"),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    path = parser.parse_args().output
    report = run_mutations(Path(__file__).resolve().parents[1], mutations=MUTATIONS,
                           test_filename="test_play_constrained_goals.py")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Detected {len(report['mutations'])} constrained-goal mutations.")


if __name__ == "__main__":
    main()

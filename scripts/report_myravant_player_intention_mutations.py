"""Verify that the installed journeys catch dropped input boundaries."""

import argparse
import json
from pathlib import Path

from report_myravant_specialist_mutations import run_mutations


MUTATIONS = (
    ("discard_player_constraint", "myravant_player_intentions.py",
     "            if proposal.constraint:\n                yield self._result",
     "            if False:\n                yield self._result",
     "test_speech_and_methods_are_not_silently_substituted"),
    ("execute_the_next_instruction_after_refused_travel", "myravant_terminal.py",
     "                    if result.failure_class:\n                        stopped = True",
     "                    if False:\n                        stopped = True",
     "test_generated_interruption_restart_and_improvisation"),
    ("choose_instrument_without_asking", "myravant_player_intentions.py",
     "        if len(candidates) > 1:\n            verbs", "        if False:\n            verbs",
     "test_an_instrument_answer_selects_actual_custody_and_method"),
    ("discard_audience_qualified_identity", "myravant_input_context.py",
     '        return entity.rsplit(":", 1)[-1]', '        return label',
     "test_visible_alias_keeps_identity_when_an_unseen_name_collides"),
    ("route_an_interrogative_to_the_physical_method", "myravant_player_intentions.py",
     "                    if goal.method is None:", "                    if True:",
     "test_legacy_lantern_advice_cannot_turn_a_question_into_a_throw"),
    ("send_retrieval_to_loose_pickup", "myravant_player_intentions.py",
     '        if not polite and parsed.action == "retrieve" and not original.endswith("?"):',
     '        if False:', "test_a_named_container_keeps_take_on_the_storage_owner"),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    path = parser.parse_args().output
    report = run_mutations(Path(__file__).resolve().parents[1], mutations=MUTATIONS,
                           test_filename="test_play_player_intentions.py")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Detected all {len(report['mutations'])} isolated intention regressions.")


if __name__ == "__main__":
    main()

"""Measure whether installed play detects violations of reference boundaries."""

import argparse
import json
from pathlib import Path

from report_myravant_specialist_mutations import run_mutations


MUTATIONS = (
    ("reveal_current_placement_from_private_world", "myravant_player_intentions.py",
     '''            details.append("You don't know its current location.")''',
     '''            details.append(context.fixture.entity_name(self.app.entity_place_id(target)))''',
     "test_brush_moves_in_absence_and_history_survives_restart"),
    ("confuse_testimony_with_direct_sight", "myravant_actor_application.py",
     "            event=evidence.latest(self.evidence_state,actor,target,facet,kind=kind)",
     "            event=evidence.latest(self.evidence_state,actor,target,facet)",
     "test_brush_moves_in_absence_and_history_survives_restart"),
    ("discard_committed_routes_on_reload", "myravant_input_context.py",
     "        self._recover_routes()", "        pass",
     "test_brush_moves_in_absence_and_history_survives_restart"),
    ("reverse_handoff_roles", "myravant_experienced_references.py",
     '        incoming = direction == "received"', '        incoming = direction != "received"',
     "test_exchange_projections_preserve_direction_and_audience"),
    ("omit_handoff_audience_check", "myravant_experienced_references.py",
     "            if (recipient if incoming else source) == self.player:",
     "            if True:",
     "test_exchange_projections_preserve_direction_and_audience"),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    path = parser.parse_args().output
    report = run_mutations(Path(__file__).resolve().parents[1], mutations=MUTATIONS,
                           test_filename="test_play_experienced_references.py")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Detected {len(report['mutations'])} experienced-reference mutations.")


if __name__ == "__main__":
    main()

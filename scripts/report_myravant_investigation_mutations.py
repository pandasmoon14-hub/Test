"""Six isolated source-copy negative controls for #552, not a blind assessor."""
import argparse
import json
from pathlib import Path

from report_myravant_specialist_mutations import run_mutations


MUTATIONS = (
    (
        'world_refresh_on_recall',
        'myravant_investigation_application.py',
        '    def recall_history(self, target_text, facet):\n        status, entries = self._admitted_history(target_text, facet)',
        "    def recall_history(self, target_text, facet):\n        self._observe_all('mutant-report')\n        status, entries = self._admitted_history(target_text, facet)",
        'test_recall_cannot_refresh_world_truth_or_evidence',
    ),
    (
        'cross_actor_private_history_leak',
        'myravant_investigation_application.py',
        'if e.actor_id == player and e.target_id == matches[0]',
        'if e.target_id == matches[0]',
        'test_only_requester_events_appear_in_history',
    ),
    (
        'reported_account_promoted_to_truth',
        'myravant_investigation_application.py',
        'No account is selected as true, false, guilty or conclusive.',
        'The first account is established true.',
        'test_conflicting_report_is_never_a_truth_or_guilt_verdict',
    ),
    (
        'forgotten_disclosed_provenance',
        'myravant_investigation_application.py',
        'return next((actor for key, actor in self.disclosed_relays if key == event_id), None)',
        'return None',
        'test_disclosed_relay_speaker_survives_only_via_requester_history',
    ),
    (
        'case_root_regenerated_over_checkpoint',
        'myravant_investigation_cases.py',
        'if checkpoint_path.exists():',
        'if False:',
        'test_case_history_cannot_regenerate_over_saved_campaign',
    ),
    (
        'query_advances_world_clock',
        'myravant_investigation_application.py',
        '    def compare_history(self, target_text, facet):\n        status, entries = self._admitted_history(target_text, facet)',
        '    def compare_history(self, target_text, facet):\n        self.wait()\n        status, entries = self._admitted_history(target_text, facet)',
        'test_comparison_cannot_advance_world_time',
    ),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = run_mutations(
        Path(__file__).resolve().parents[1],
        mutations=MUTATIONS,
        test_filename='test_play_investigation_mutations.py',
    )
    assert len(report['mutations']) == 6
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    print('Investigation mutations: 6/6 intended defects detected with passing controls.')


if __name__ == '__main__':
    main()

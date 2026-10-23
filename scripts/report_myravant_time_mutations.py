"""Implementation-authored isolated time negative controls; working source unchanged."""
import argparse
import json
from pathlib import Path
from report_myravant_specialist_mutations import run_mutations

MUTATIONS = (
    ('passive_drying_not_scheduled', 'myravant_timed_application.py',
     'self.water_state,self.environment_state=env.advance_environment(self.water_state,self.environment_state,self.environment_profile,exposures,tick,result.receipt_id,\n                                                                          rate_overrides=self._exposure_rate_overrides(exposures))',
     'self.water_state,self.environment_state=self.water_state,self.environment_state',
     'test_wait_dries_cloth_without_working_on_dirty_panel'),
    ('evaporation_ledger_loses_water', 'domain/persistent_world_timed_environment.py',
     'evaporated[place] += removed', 'evaporated[place] += 0',
     'test_bounded_wait_matches_repeated_single_intervals'),
    ('duration_silently_truncates_suffix', 'myravant_timed_application.py',
     "m=re.fullmatch(r'(wait|work)(?: ([0-9]+) steps?)?',text)",
     "m=re.match(r'(wait|work)(?: ([0-9]+) steps?)?',text)",
     'test_unsupported_duration_text_never_truncates[wait 2 steps permanently]'),
    ('timed_replay_final_digest_ignored', 'myravant_material_application.py',
     "app.authoritative_digest()!=p['final'] or ", '',
     'test_resealed_timed_checkpoint_forgery_rejected[final]'),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = run_mutations(Path(__file__).resolve().parents[1], mutations=MUTATIONS,
                           test_filename='test_play_tarrow_time.py')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('Time mutations: 4/4 intended defects detected; all isolated unmutated controls passed.')


if __name__ == '__main__':
    main()

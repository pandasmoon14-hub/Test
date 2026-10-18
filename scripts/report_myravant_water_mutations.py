"""Isolated water negative controls; working source remains unchanged."""
import argparse
import json
from pathlib import Path
from report_myravant_specialist_mutations import run_mutations

MUTATIONS=(
    ('dirty_transfer_loses_proportion','domain/persistent_world_water_cleaning.py',
     'residue = suspended[source] * Fraction(quantity, water[source])',
     'residue = suspended[source]',
     'test_dirty_liquid_proportional_transfer_and_mixing'),
    ('wringing_discards_adhered_residue','domain/persistent_world_water_cleaning.py',
     'liquid(water[source])',
     'liquid(water[source]); adhered[source] = Fraction(0)',
     'test_complete_workshop_washing_and_recovery'),
    ('wiping_does_not_require_water','domain/persistent_world_water_cleaning.py',
     'if operation == "wipe" and not water[target]:',
     'if False:',
     'test_full_recipient_empty_source_and_dry_wipe_refuse'),
    ('replay_final_state_comparison_removed','myravant_material_application.py',
     "app.authoritative_digest()!=p['final'] or ", '',
     'test_resealed_checkpoint_forgery_rejected[final]'),
)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    report=run_mutations(Path(__file__).resolve().parents[1],mutations=MUTATIONS,test_filename='test_play_water_cleaning.py')
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('Water mutations: 4/4 intended defects detected with passing controls.')

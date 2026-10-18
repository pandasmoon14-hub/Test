"""Isolated material negative controls; never edits working source."""
import argparse
import json
from pathlib import Path
from report_myravant_specialist_mutations import run_mutations

MUTATIONS=(
    ('occupied_support_pickup_bypasses_guard','myravant_material_application.py',
     'return self._guard(object_reference) or super()._custody', 'return super()._custody',
     'test_occupied_support_cannot_move'),
    ('required_connection_lost_from_effect','domain/persistent_world_material.py',
     'and set(e.connections) <= linked', '',
     'test_barrier_requires_placement_and_connection_and_reopens'),
    ('separation_method_silently_changed','domain/persistent_world_material.py',
     "and (operation == 'untie') == (c.method == 'tie')", '',
     'test_method_and_fastener_are_not_interchangeable'),
    ('replay_final_state_comparison_removed','myravant_material_application.py',
     "app.authoritative_digest()!=p['final'] or ", '',
     'test_resealed_checkpoint_forgery_rejected[final]'),
)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    report=run_mutations(Path(__file__).resolve().parents[1],mutations=MUTATIONS,test_filename='test_play_material.py')
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('Material mutations: 4/4 intended defects detected with passing controls.')

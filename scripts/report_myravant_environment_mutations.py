"""Isolated environmental qualification/replay negative controls."""
import argparse
import json
from pathlib import Path
from report_myravant_specialist_mutations import run_mutations

MUTATIONS=(
    ('basket_no_longer_obstructs_declared_passage','myravant_tarrow_environment.py',
     'obstructions=(("yard","east","basket","yard"),)','obstructions=()',
     'test_clearance_methods_preserve_hidden_cargo_and_later_reblock[push]'),
    ('open_container_moves_without_condition','myravant_tarrow.py',
     'method=m, required_open_state=state','method=m, required_open_state=None',
     'test_container_state_qualifies_movement_and_cargo_survives'),
    ('plural_initial_state_replay_uses_incidental_order','domain/persistent_world_local_checkpoint_restore.py',
     'canonical_serialize_persistent_world_object_open_states(replayed)\n        != canonical_serialize_persistent_world_object_open_states(object_states)',
     'tuple(serialize_persistent_world_object_open_state(x) for x in replayed)\n        != tuple(serialize_persistent_world_object_open_state(x) for x in object_states)',
     'test_unordered_multiple_container_and_light_states_restore_without_changes'),
)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    result=run_mutations(Path(__file__).resolve().parents[1],mutations=MUTATIONS,
                         test_filename='test_play_tarrow_environment.py')
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('Environmental mutations: 3/3 intended defects detected; unmutated controls passed.')

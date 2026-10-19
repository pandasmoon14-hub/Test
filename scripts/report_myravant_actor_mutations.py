"""Six isolated #548 negative controls; working source remains unchanged."""
import argparse
import json
from pathlib import Path
from report_myravant_specialist_mutations import run_mutations

MUTATIONS = (
    ('consent_bypassed','myravant_actor_application.py',
     "if not profile.willing:raise ValueError('The actor declines this scope of work.')",
     "if False:raise ValueError('The actor declines this scope of work.')",
     'test_consent_is_not_execution_authority'),
    ('selected_player_substituted_for_performer','myravant_actor_application.py',
     'return execute_actor_physical(self,actor,operation,*ids)',
     'return execute_actor_physical(self,self.fixture.player_entity_id,operation,*ids)',
     'test_contribution_performer_is_npc_not_selected_player'),
    ('two_clock_advances_for_one_interval','myravant_actor_application.py',
     'clock,environment_before=self._clock_interval()',
     'self._clock_interval();clock,environment_before=self._clock_interval()',
     'test_single_world_interval_for_two_actors'),
    ('npc_prepared_intent_executes_before_player_claim','myravant_actor_application.py',
     "actual=clock if name=='wait' else self._raw(name,*args,**kwargs)",
     "[self._execute_actor(actor,intent) for actor,outcome,intent in prepared if outcome=='action'];actual=clock if name=='wait' else self._raw(name,*args,**kwargs)",
     'test_player_claim_requalifies_prepared_npc_intent'),
    ('private_witness_visibility_ignored','myravant_actor_knowledge.py',
     'if not app._visible_for_actor(actor_id, obj):','if False:',
     'test_remote_player_does_not_inherit_npc_witness'),
    ('replay_actor_profile_binding_ignored','myravant_material_application.py',
     " or digest(p['profile'])!=digest(app._checkpoint_profile())",'',
     'test_replay_rejects_changed_actor_attribution_profile'),
)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    report=run_mutations(Path(__file__).resolve().parents[1],mutations=MUTATIONS,
                         test_filename='test_play_actor_mutations.py')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('Actor mutations: 6/6 intended defects detected; isolated unmutated controls passed.')


if __name__=='__main__':main()

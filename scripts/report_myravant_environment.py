"""Authored installed environmental journeys; not independent/human acceptance."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_play_application import MyravantPlayApplication as App
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_environment import create_environment_fixture


def campaign(root,kind,head):
    checkpoint=root/'state.json'; stages=[]; previous=None
    def stage(*commands):
        nonlocal previous
        trace=root/f'{len(stages)}.jsonl'
        args=[shutil.which('myravant-play'),'--locality','tarrow-depth','--checkpoint',str(checkpoint),
              '--trace',str(trace),'--repository-sha',head]
        if checkpoint.exists():
            args+=['--load',str(checkpoint)]
        proc=subprocess.run(args,input='\n'.join((*commands,'save','exit','')),
                            text=True,capture_output=True,timeout=45)
        assert proc.returncode==0,(proc.stdout,proc.stderr)
        assert '\\n' not in proc.stdout and '\\r' not in proc.stdout
        records=[json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
        assert records[-1]['evidence_complete']
        rows=[r for r in records if r['record_type']=='interaction']
        if previous is not None:
            assert rows[0]['pre_state_digest']==previous
        for a,b in zip(rows,rows[1:]):
            assert a['post_state_digest']==b['pre_state_digest']
        app=App.restore(fixture=create_environment_fixture(),checkpoint_path=checkpoint)
        assert app.authoritative_digest()==rows[-1]['post_state_digest']
        previous=app.authoritative_digest()
        stages.append({'commands':commands,'stdout':proc.stdout,'stderr':proc.stderr,'records':records})
        return proc.stdout,app
    if kind=='clearance':
        text,_=stage('go south','open delivery basket','push delivery basket west')
        assert 'must be closed' in text
        stage('close delivery basket then slide delivery basket west','approach underbank threshold','wait')
        text,app=stage('approach service yard then approach yard tool station','push delivery basket east',
                       'approach service yard','approach underbank threshold')
        objectives={'reblocked_after_return':'obstructs' in text,
                    'player_stopped_at_yard':app.current_place_id()==identity('yard'),
                    'same_cargo_preserved':any(r.subject_entity_id==identity('cord') and r.object_entity_id==identity('basket') for r in app.state.representation.relations),
                    'time_persisted':app.runtime_state.logical_time_state.logical_position==1}
    elif kind=='bench':
        stage('go south then approach yard tool station','approach workshop workroom then approach workroom bench')
        text,_=stage('open parts tray','push parts tray east')
        assert 'must be closed' in text
        stage('close parts tray then push parts tray east','approach workshop workroom','open parts tray','take wooden peg')
        stage('approach yard tool station then approach service yard','go north then approach common threshold',
              'approach notice recess','open document box','put wooden peg in document box','close document box','wait')
        text,app=stage('open document box','inspect document box')
        objectives={'peg_transferred_without_duplication':sum(r.subject_entity_id==identity('peg') and r.object_entity_id==identity('document-box') for r in app.state.representation.relations)==1,
                    'new_context_persisted':app.current_place_id()==identity('notice-recess'),
                    'contents_observed_after_actual_open':'Inside: Wooden Peg' in text}
    else:
        text,_=stage('go south','slide delivery basket west then approach underbank threshold',
                     'approach underbank walk then approach floodmark position','inspect floodmark post')
        assert 'cannot inspect' in text
        stage('approach underbank walk then approach underbank threshold','approach service yard then go north',
              'take shuttered service lamp','light shuttered service lamp')
        text,_=stage('go south then approach underbank threshold','approach underbank walk then approach floodmark position',
                     'inspect floodmark post','take floodmark post')
        assert 'Fixed water-level' in text and 'cannot pick' in text
        text,app=stage('approach underbank walk then approach abutment position','inspect wall streak','wait')
        objectives={'actual_local_light':app._bounded_local_light_available(),
                    'different_inspection_position':app.current_place_id()==identity('abutment-position'),
                    'hidden_pin_not_disclosed':all('Soft-Iron Pin Blank' not in s['stdout'] for s in stages)}
    assert all(objectives.values()),objectives
    return {'profile':kind,'objectives':objectives,'final_digest':previous,'stages':stages}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    head=subprocess.run(['git','rev-parse','HEAD'],check=True,text=True,capture_output=True).stdout.strip()
    profiles=[]
    with tempfile.TemporaryDirectory(prefix='environment-evidence-') as temporary:
        for kind in ('clearance','bench','sight'):
            runs=[]
            for repeat in range(2):
                root=Path(temporary)/f'{kind}-{repeat}';root.mkdir()
                runs.append(campaign(root,kind,head))
            assert runs[0]['final_digest']==runs[1]['final_digest']
            profiles.append(runs[0])
    args.output.write_text(json.dumps({'repository_sha':head,'implementation_authored':True,
        'not_blind_or_human_acceptance':True,'repeat_count':2,'profiles':profiles},indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('Environmental depth: 3 installed journeys repeated twice; all objectives and restart checks passed.')


if __name__=='__main__':
    main()

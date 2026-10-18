"""Installed owner-qualified material campaigns; authored, not human acceptance."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_material_application import MaterialApplication
from astra_runtime.myravant_tarrow_material import create_material_fixture,identity
from astra_runtime.domain.persistent_world_material import placement,active_effects


def campaign(root,kind,head):
    checkpoint=root/'state.json'; stages=[]; previous=None
    def stage(*commands):
        nonlocal previous
        trace=root/f'{len(stages)}.jsonl'
        args=[shutil.which('myravant-play'),'--locality','tarrow-material','--checkpoint',str(checkpoint),
              '--trace',str(trace),'--repository-sha',head]
        if checkpoint.exists():args+=['--load',str(checkpoint)]
        proc=subprocess.run(args,input='\n'.join((*commands,'save','exit','')),text=True,capture_output=True,timeout=45)
        assert proc.returncode==0,(proc.stdout,proc.stderr)
        assert '\\n' not in proc.stdout and '\\r' not in proc.stdout
        records=[json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
        assert records[-1]['evidence_complete']
        rows=[r for r in records if r['record_type']=='interaction']
        if previous is not None:assert rows[0]['pre_state_digest']==previous
        for a,b in zip(rows,rows[1:]):assert a['post_state_digest']==b['pre_state_digest']
        app=MaterialApplication.restore(fixture=create_material_fixture(),checkpoint_path=checkpoint)
        assert app.authoritative_digest()==rows[-1]['post_state_digest']
        previous=app.authoritative_digest()
        stages.append({'commands':commands,'stdout':proc.stdout,'stderr':proc.stderr,'records':records})
        return proc.stdout,app
    if kind=='workshop':
        stage('go south','go west','go west','go west',
              'take repair board then put repair board on workroom bench',
              'take repair peg then put repair peg on workroom bench',
              'take repair cord','tie repair board to repair peg using repair cord')
        text,a=stage('take repair board','inspect repair board','inspect repair cord')
        assert 'Remove the relevant relationship first' in text and 'Connection:' in text
        text,a=stage('untie repair cord','lift repair board from workroom bench','lift repair peg from workroom bench',
                     'open parts tray','put repair board in parts tray','put repair peg in parts tray','put repair cord in parts tray',
                     'close parts tray','push parts tray east','go east','open parts tray',
                     'retrieve repair board from parts tray','retrieve repair peg from parts tray','retrieve repair cord from parts tray')
        goals={'connections_removed':not a.connections,'components_recovered':all(placement(a.state.representation,identity(k)).relation_type=='carried_by' for k in ('repair-board','repair-peg','repair-cord')),
               'transported_to_new_position':a.current_place_id()==identity('workshop')}
    elif kind=='passage':
        stage('go south','go west','take barrier board then put barrier board on yard work trestle',
              'take barrier crossbar then put barrier crossbar on yard work trestle',
              'take barrier cord','tie barrier board to barrier crossbar using barrier cord')
        text,a=stage('go north','inspect barrier board')
        assert 'assembled barrier obstructs' in text and a.current_place_id()==identity('yard-tools')
        text,a=stage('untie barrier cord','lift barrier board from yard work trestle','lift barrier crossbar from yard work trestle','go north')
        goals={'passage_reopened':a.current_place_id()==identity('yard-sorting'),'no_stale_effect':not active_effects(a.state.representation,a.connections,a.material_profile),'fastener_recovered':placement(a.state.representation,identity('barrier-cord')).relation_type=='carried_by'}
    else:
        stage('go east','go east','take screen cloth then put screen cloth on document box',
              'take screen cord','tie screen cloth to notice board using screen cord',
              'take screen tie','fasten screen cloth to notice board using screen tie')
        text,a=stage('unfasten screen tie','go west','look east','go east')
        assert 'assembled screen blocks' in text and a.current_place_id()==identity('notice-recess') and len(a.connections)==1
        text,a=stage('untie screen cord','lift screen cloth from document box','open document box',
                     'put screen cloth in document box','close document box','take document box','go west','look east')
        goals={'screen_removed':not a.connections,'sightline_restored':'assembled screen blocks' not in text,
               'cloth_inside_not_on':placement(a.state.representation,identity('screen-cloth')).relation_type=='contained_by',
               'box_transportable_after_exterior_cleared':placement(a.state.representation,identity('document-box')).relation_type=='carried_by'}
    assert all(goals.values()),goals
    assert all('Soft-Iron Pin Blank' not in s['stdout'] for s in stages)
    return {'profile':kind,'objectives':goals,'final_digest':previous,'stages':stages}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    head=subprocess.run(['git','rev-parse','HEAD'],check=True,text=True,capture_output=True).stdout.strip()
    profiles=[]
    with tempfile.TemporaryDirectory(prefix='material-evidence-') as temporary:
        for kind in ('workshop','passage','screen'):
            runs=[]
            for repeat in range(2):
                root=Path(temporary)/f'{kind}-{repeat}';root.mkdir();runs.append(campaign(root,kind,head))
            assert runs[0]['final_digest']==runs[1]['final_digest']
            profiles.append({'profile':kind,'repeats':runs})
    args.output.write_text(json.dumps({'repository_sha':head,'implementation_authored':True,
        'not_blind_or_human_acceptance':True,'repeat_count':2,'profiles':profiles},indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('Material: three installed journeys repeated twice; objectives, trace joins and restart passed.')


if __name__=='__main__':main()

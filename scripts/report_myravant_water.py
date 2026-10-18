"""Installed owner-qualified water campaigns; authored, not human acceptance."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_water_application import WaterApplication
from astra_runtime.myravant_tarrow_water import create_water_fixture
from astra_runtime.myravant_tarrow import identity
from fractions import Fraction
from astra_runtime.domain.persistent_world_water_cleaning import total_water,total_residue


def v(app,compartment,name):
    return dict(getattr(app.water_state,compartment))[identity(name)]


def campaign(root,kind,head):
    checkpoint=root/'state.json'; stages=[]; previous=None
    def stage(*commands):
        nonlocal previous
        trace=root/f'{len(stages)}.jsonl'
        args=[shutil.which('myravant-play'),'--locality','tarrow-water','--checkpoint',str(checkpoint),
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
        app=WaterApplication.restore(fixture=create_water_fixture(),checkpoint_path=checkpoint)
        assert app.authoritative_digest()==rows[-1]['post_state_digest']
        previous=app.authoritative_digest()
        stages.append({'commands':commands,'stdout':proc.stdout,'stderr':proc.stderr,'records':records})
        return proc.stdout,app
    if kind=='workshop':
        stage('go south','go west','go west','go west','take cleaning cloth',
              'soak cleaning cloth from wash bucket','wipe practice panel using cleaning cloth',
              'wipe practice panel using cleaning cloth')
        text,a=stage('fill rinse basin from wash bucket','rinse cleaning cloth in rinse basin',
                     'wipe practice panel using cleaning cloth','wring cleaning cloth into pouring jug')
        text,a=stage('put cleaning cloth on workroom bench','lift cleaning cloth from workroom bench',
                     'open parts tray','put cleaning cloth in parts tray','close parts tray',
                     'push parts tray east','go east','open parts tray','retrieve cleaning cloth from parts tray')
        goals={'panel_clean':v(a,'adhered','practice-panel')==0,
               'cloth_dry_but_dirty':v(a,'water','cleaning-cloth')==0 and v(a,'adhered','cleaning-cloth')==1,
               'dirty_water_retained':v(a,'suspended','pouring-jug')==Fraction(2,7),
               'cargo_recovered_after_transport':a.current_place_id()==identity('workshop')}
    elif kind=='yard':
        stage('go south','go west','go west','go west','take pouring jug','fill pouring jug from wash bucket',
              'go east','go east','take cleaning brush','scrub sorting board using cleaning brush')
        text,a=stage('collect residue from cleaning brush into debris tray','scrub sorting board using cleaning brush',
                     'rinse cleaning brush in pouring jug')
        goals={'board_clean':v(a,'adhered','sorting-board')==0,
               'brush_recovered':v(a,'adhered','cleaning-brush')==0,
               'residue_collected':v(a,'adhered','debris-tray')==2,
               'wash_water_transported_and_used':v(a,'water','pouring-jug')==3 and v(a,'suspended','pouring-jug')==2}
    else:
        stage('go south','go west','go west','go west','take cleaning cloth','take rinse basin',
              'soak cleaning cloth from wash bucket','wipe practice panel using cleaning cloth',
              'fill rinse basin from wash bucket','rinse cleaning cloth in rinse basin')
        text,a=stage('pour 3 units from rinse basin into pouring jug','empty rinse basin into wash bucket')
        goals={'jug_exact_mixture':v(a,'suspended','pouring-jug')==Fraction(3,7),
               'source_empty':v(a,'water','rinse-basin')==0,
               'finite_supply_receives_recovery':v(a,'water','wash-bucket')==8 and v(a,'suspended','wash-bucket')==Fraction(3,7)}
    goals.update(water_conserved=total_water(a.water_state)==12,residue_conserved=total_residue(a.water_state)==7)
    assert all(goals.values()),goals
    assert all('Soft-Iron Pin Blank' not in s['stdout'] for s in stages)
    return {'profile':kind,'objectives':goals,'final_digest':previous,'stages':stages}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    head=subprocess.run(['git','rev-parse','HEAD'],check=True,text=True,capture_output=True).stdout.strip()
    profiles=[]
    with tempfile.TemporaryDirectory(prefix='water-evidence-') as temporary:
        for kind in ('workshop','yard','mixture'):
            runs=[]
            for repeat in range(2):
                root=Path(temporary)/f'{kind}-{repeat}';root.mkdir();runs.append(campaign(root,kind,head))
            assert runs[0]['final_digest']==runs[1]['final_digest']
            profiles.append({'profile':kind,'repeats':runs})
    args.output.write_text(json.dumps({'repository_sha':head,'implementation_authored':True,
        'not_blind_or_human_acceptance':True,'repeat_count':2,'profiles':profiles},indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('Water: three installed journeys repeated twice; conservation, objectives, trace joins and restart passed.')


if __name__=='__main__':main()

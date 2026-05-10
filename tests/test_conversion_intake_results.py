from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import pytest
jsonschema = pytest.importorskip('jsonschema')


def _mk_packet(root: Path, pid: str):
    d=root/pid; d.mkdir(parents=True)
    (d/'conversion_prompt.md').write_text(f'# prompt {pid}\n',encoding='utf-8')


def test_conversion_intake_flow(tmp_path: Path):
    packet_root=tmp_path/'packets'; packet_root.mkdir()
    _mk_packet(packet_root,'p1'); _mk_packet(packet_root,'p2')
    plan={"plan_id":"sp","packets":[{"packet_id":"p1","book_match":"b1","start_page":1,"end_page":2,"readiness_hint":"ready_candidate"},{"packet_id":"p2","book_match":"b2","start_page":3,"end_page":4,"readiness_hint":"needs_repair_candidate"}]}
    planf=tmp_path/'selected_plan.json'; planf.write_text(json.dumps(plan),encoding='utf-8-sig')
    run=tmp_path/'run'

    subprocess.run([sys.executable,'scripts/handoff/init_conversion_intake_run.py','--packet-root',str(packet_root),'--selected-plan',str(planf),'--output-run-dir',str(run),'--run-id','r1'],check=True)
    assert (run/'intake_run_manifest.json').exists()
    assert (run/'packet_index.json').exists()
    assert (run/'prompts/p1_conversion_prompt.md').exists()
    assert (run/'results/p1_conversion_result.json').exists()

    schema=json.loads((Path('schemas/handoff/conversion_intake_result.schema.json').read_text(encoding='utf-8')))
    obj=json.loads((run/'results/p1_conversion_result.json').read_text(encoding='utf-8'))
    jsonschema.validate(obj,schema)

    ok=subprocess.run([sys.executable,'scripts/handoff/validate_conversion_intake_results.py','--run-dir',str(run),'--strict','--allow-placeholders'],capture_output=True,text=True)
    assert ok.returncode==0
    bad=subprocess.run([sys.executable,'scripts/handoff/validate_conversion_intake_results.py','--run-dir',str(run),'--strict'],capture_output=True,text=True)
    assert bad.returncode!=0

    # schema rejects invalid lawful_outcome & requires mapping ledger fields
    bad_obj=obj.copy(); bad_obj['mapping_ledger']=[{"donor_construct":"x"}]
    pbad=run/'results/p1_conversion_result.json'; pbad.write_text(json.dumps(bad_obj),encoding='utf-8')
    fail=subprocess.run([sys.executable,'scripts/handoff/validate_conversion_intake_results.py','--run-dir',str(run),'--strict','--allow-placeholders'],capture_output=True,text=True)
    assert fail.returncode!=0

    # restore valid placeholder then test missing result file detection
    pbad.write_text(json.dumps(obj),encoding='utf-8')
    (run/'results/p2_conversion_result.json').unlink()
    miss=subprocess.run([sys.executable,'scripts/handoff/validate_conversion_intake_results.py','--run-dir',str(run),'--strict','--allow-placeholders'],capture_output=True,text=True)
    assert miss.returncode!=0


def test_report_outputs(tmp_path: Path):
    run=tmp_path/'run'; (run/'results').mkdir(parents=True)
    sample={
        'result_id':'r_p1','packet_id':'p1','book_id':'b1','source_packet_dir':'x','page_range':{'start_page':1,'end_page':2},'result_status':'reviewed','extraction_readiness_assessment':'ready',
        'donor_construct_inventory':[],'mapping_ledger':[{'donor_construct':'x','source_pages':[1],'source_unit_ids':['u1'],'astra_target_family':'fam','lawful_outcome':'normalized Astra mapping','rationale':'ok','must_not_import':False,'doctrine_owner':'d','canon_candidate_permission':'candidate_only_after_review','confidence':0.8}],
        'queue_actions':[],'lexicon_delta':[],'doctrine_escalations':[{}],'source_local_retentions':[{}],'rejected_imports':[],'canon_candidate_notes':'note','conversion_notes':'c','reviewer_notes':'r','confidence':0.8
    }
    (run/'results/p1_conversion_result.json').write_text(json.dumps(sample),encoding='utf-8')
    subprocess.run([sys.executable,'scripts/handoff/report_conversion_intake_results.py','--run-dir',str(run)],check=True)
    assert (run/'reports/conversion_intake_summary_report.json').exists()
    assert (run/'reports/conversion_intake_summary_report.md').exists()
    assert (run/'reports/conversion_intake_packet_table.csv').exists()

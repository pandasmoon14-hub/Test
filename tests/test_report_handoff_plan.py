from __future__ import annotations
import json, subprocess, sys
from pathlib import Path


def _write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj), encoding='utf-8')


def test_report_outputs_and_counts(tmp_path: Path):
    plan={"plan_id":"pid","packets":[
        {"packet_id":"p1","book_match":"b1","start_page":1,"end_page":3,"readiness_hint":"ready_candidate","dominant_content_family":"mechanics_prose","content_family_tags":["mechanics_prose"],"quality_score":1.2,"text_char_count":1200,"usable_page_count":3,"repair_page_count":0,"sparse_page_count":0},
        {"packet_id":"p2","book_match":"b1","start_page":4,"end_page":6,"readiness_hint":"needs_repair_candidate","dominant_content_family":"map_dependency","content_family_tags":["map_dependency","statblock_pressure"],"quality_score":0.2,"text_char_count":300,"usable_page_count":1,"repair_page_count":2,"sparse_page_count":1}
    ]}
    planf=tmp_path/'plan.json'; _write_json(planf, plan)
    root=tmp_path/'packets'; root.mkdir()
    _write_json(root/'handoff_batch_validation_summary.json',{
        "counts":{"queue_records_by_queue":{"map_diagram_queue":2,"repair_queue":1,"statblock_queue":1},"content_unit_type_counts":{"map":1},"page_status_counts":{"ok":3,"queued":2},"readiness_counts":{"ready":1,"needs_repair":1}},
        "packet_reports":[{"packet_id":"p1","valid":True,"errors":[],"warnings":[],"counts":{"queue_records_by_queue":{}}},{"packet_id":"p2","valid":False,"errors":["x"],"warnings":[],"counts":{"queue_records_by_queue":{"map_diagram_queue":2,"repair_queue":1,"statblock_queue":1}}}]
    })
    _write_json(root/'p1'/'packet_validation_report.json',{"packet_id":"p1","valid":True,"errors":[],"warnings":[],"counts":{"queue_records_by_queue":{}}})
    _write_json(root/'p2'/'packet_validation_report.json',{"packet_id":"p2","valid":False,"errors":["bad"],"warnings":[],"counts":{"queue_records_by_queue":{"map_diagram_queue":2,"repair_queue":1,"statblock_queue":1}}})

    out=tmp_path/'out'
    subprocess.run([sys.executable,'scripts/handoff/report_handoff_plan.py','--plan-file',str(planf),'--packet-root',str(root),'--output-dir',str(out)],check=True)
    assert (out/'handoff_plan_review_report.json').exists()
    assert (out/'handoff_plan_review_report.md').exists()
    assert (out/'packet_review_table.csv').exists()

    rep=json.loads((out/'handoff_plan_review_report.json').read_text())
    assert rep['summary']['readiness_hint_counts']['ready_candidate']==1
    assert rep['summary']['dominant_content_family_counts']['map_dependency']==1
    assert rep['summary']['queue_records_by_queue']['map_diagram_queue']==2
    p2=next(x for x in rep['packet_reviews'] if x['packet_id']=='p2')
    assert p2['false_positive_risk'] in {'medium','high'}
    assert any(f in p2['review_flags'] for f in ['map_dependency_pressure','statblock_pressure','repair_pressure','validation_problem'])


def test_bom_plan_and_missing_batch_summary(tmp_path: Path):
    plan={"plan_id":"pid","packets":[{"packet_id":"p1","book_match":"b","start_page":1,"end_page":1,"readiness_hint":"ready_candidate","dominant_content_family":"unknown","content_family_tags":["unknown"],"quality_score":1,"text_char_count":100,"usable_page_count":1,"repair_page_count":0,"sparse_page_count":1}]}
    planf=tmp_path/'plan_bom.json'; planf.write_text(json.dumps(plan),encoding='utf-8-sig')
    root=tmp_path/'packets'; root.mkdir(); (root/'p1').mkdir()
    out=tmp_path/'out'
    subprocess.run([sys.executable,'scripts/handoff/report_handoff_plan.py','--plan-file',str(planf),'--packet-root',str(root),'--output-dir',str(out)],check=True)
    rep=json.loads((out/'handoff_plan_review_report.json').read_text())
    assert 'missing_batch_validation_summary' in rep['warnings']

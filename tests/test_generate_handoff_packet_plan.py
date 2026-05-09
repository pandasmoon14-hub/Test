from __future__ import annotations
import json, subprocess, sys, re
from pathlib import Path
import pytest
pytest.importorskip('jsonschema')

def _write_jsonl(path: Path, rows): path.write_text("\n".join(json.dumps(r) for r in rows)+"\n", encoding='utf-8')

def _mk_book(root: Path, name: str, pages: list[str], statuses: list[str]):
    d=root/name; d.mkdir(parents=True)
    (d/'book.md').write_text("\n".join([f"<!-- PAGE:{i} -->\n{t}\n" for i,t in enumerate(pages,1)]), encoding='utf-8')
    _write_jsonl(d/'book.page_truth.jsonl',[{"book_id":name,"page":i,"page_status":st,"reason_code":"native_text_extracted" if st in {'ok','ocr_done'} else 'queued_page'} for i,st in enumerate(statuses,1)])
    (d/'strict_audit.json').write_text(json.dumps({"strict_audit_status":"pass"}),encoding='utf-8')
    (d/'astra_handoff_manifest.json').write_text(json.dumps({"book_id":name,"source_filename":"x.pdf","source_sha256":"abc","extraction_version":"v13"}),encoding='utf-8')

def _run(src: Path, planf: Path, **kwargs):
    cmd=[sys.executable,'scripts/handoff/generate_handoff_packet_plan.py','--source-output-root',str(src),'--output-plan',str(planf),'--plan-id','pid','--min-text-chars','20']
    for k,v in kwargs.items():
        if isinstance(v,bool):
            if v: cmd.append(f'--{k.replace("_","-")}')
        else:
            cmd += [f'--{k.replace("_","-")}', str(v)]
    subprocess.run(cmd,check=True)
    return json.loads(planf.read_text())

def test_strategy_and_limits_and_tags(tmp_path: Path):
    src=tmp_path/'src'; src.mkdir()
    _mk_book(src,'Long Book',["cover","intro"]+["rules action check cost d20 roll table |" for _ in range(20)],['ok']*22)
    _mk_book(src,'Lore Book',["cover","intro"]+["history nation region god cosmology" for _ in range(12)],['ok']*14)
    (src/'logs').mkdir()
    plan=_run(src,tmp_path/'plan.json',selection_strategy='pilot',max_packets_per_book=1,max_packets_total=2,max_tags_per_packet=2,max_pages_per_packet=5,min_pages_per_packet=3)
    assert plan['packets'] and len(plan['packets'])<=2
    assert plan['books_skipped']==0 and 'logs' in plan['support_directories_ignored']
    by_book={}
    for p in plan['packets']:
        by_book[p['book_match']]=by_book.get(p['book_match'],0)+1
        assert len(p['content_family_tags'])<=2
        assert p['dominant_content_family']
        assert p['packet_purpose']
        assert re.match(r'^[a-z0-9_]+_pages_\d+_\d+$', p['packet_id'])
    assert all(v<=1 for v in by_book.values())

def test_coverage_can_create_multiple_packets_and_repair_modes(tmp_path: Path):
    src=tmp_path/'src'; src.mkdir()
    _mk_book(src,'Repair Book',["cover","intro","queued page text","good text rules action","more rules action","map hex room"],['ok','ok','queued','ok','ok','ok'])
    plan=_run(src,tmp_path/'plan.json',selection_strategy='coverage',max_packets_per_book=5,max_pages_per_packet=2,include_repair_pages=True,min_text_chars=5)
    assert len(plan['packets'])>=2
    assert any(p['start_page']<=3<=p['end_page'] for p in plan['packets'])
    assert any(p['readiness_hint'] in {'needs_repair_candidate','partial_conversion_allowed_candidate'} for p in plan['packets'])

def test_generated_plan_consumable_by_batch_builder(tmp_path: Path):
    src=tmp_path/'src'; src.mkdir()
    _mk_book(src,'Build Book',["cover","intro","rules action check cost"],['ok','ok','ok'])
    planf=tmp_path/'plan.json'; _run(src,planf,selection_strategy='pilot',max_packets_per_book=1,min_text_chars=5)
    out=tmp_path/'out'
    r=subprocess.run([sys.executable,'scripts/handoff/build_handoff_packet_batch.py','--plan-file',str(planf),'--output-root',str(out),'--strict'],capture_output=True,text=True)
    assert r.returncode==0

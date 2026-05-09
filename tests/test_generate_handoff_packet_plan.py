from __future__ import annotations
import json, subprocess, sys, re
from pathlib import Path
import pytest

pytest.importorskip('jsonschema')


def _write_jsonl(path: Path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows)+"\n", encoding='utf-8')


def _mk_book(root: Path, name: str, pages: list[str], statuses: list[str]):
    d=root/name; d.mkdir(parents=True)
    md=[]
    rows=[]
    for i,(txt,st) in enumerate(zip(pages,statuses), start=1):
        md.append(f"<!-- PAGE:{i} -->\n{txt}\n")
        rows.append({"book_id":name,"page":i,"page_status":st,"reason_code":"native_text_extracted" if st in {'ok','ocr_done'} else 'queued_page'})
    (d/'book.md').write_text("\n".join(md), encoding='utf-8')
    _write_jsonl(d/'book.page_truth.jsonl', rows)
    (d/'strict_audit.json').write_text(json.dumps({"strict_audit_status":"pass"}),encoding='utf-8')
    (d/'astra_handoff_manifest.json').write_text(json.dumps({"book_id":name,"source_filename":"x.pdf","source_sha256":"abc","extraction_version":"v13"}),encoding='utf-8')


def test_generate_plan_and_batch_consume(tmp_path: Path):
    src=tmp_path/'src'; src.mkdir()
    _mk_book(src,'Tables Book',["cover","intro","roll d100 table | result |","item equipment treasure list"]+ ["rules check action resource cost" for _ in range(4)],['ok']*8)
    _mk_book(src,'Adventure Book',["cover","intro","dungeon room encounter map hex grid","trap faction hook"]+["history region" for _ in range(4)],['ok']*8)
    (src/'broken').mkdir()

    planf=tmp_path/'plan.json'
    subprocess.run([sys.executable,'scripts/handoff/generate_handoff_packet_plan.py','--source-output-root',str(src),'--output-plan',str(planf),'--plan-id','pid','--mode','auto','--max-pages-per-packet','5','--min-text-chars','20'],check=True)
    plan=json.loads(planf.read_text())
    assert plan['plan_id']=='pid' and plan['source_output_root']==str(src) and plan['packets']
    assert any('skipped_book' in w for w in plan['warnings'])
    for p in plan['packets']:
        assert re.match(r'^[a-z0-9_]+_pages_\d+_\d+$', p['packet_id'])
        assert p['start_page'] > 1
        assert p['packet_purpose']
    tags=[t for p in plan['packets'] for t in p['content_family_tags']]
    assert any(t in tags for t in ['random_table','item_list'])
    assert 'mechanics_prose' in tags
    assert 'adventure_site' in tags or 'map_dependency' in tags

    out=tmp_path/'out'
    r=subprocess.run([sys.executable,'scripts/handoff/build_handoff_packet_batch.py','--plan-file',str(planf),'--output-root',str(out),'--strict'],capture_output=True,text=True)
    assert r.returncode==0


def test_include_repair_pages_option(tmp_path: Path):
    src=tmp_path/'src'; src.mkdir()
    _mk_book(src,'Repair Book',["cover","intro","queued page text","good text rules action"],['ok','ok','queued','ok'])
    planf=tmp_path/'plan.json'
    subprocess.run([sys.executable,'scripts/handoff/generate_handoff_packet_plan.py','--source-output-root',str(src),'--output-plan',str(planf),'--plan-id','pid','--include-repair-pages','--min-text-chars','5'],check=True)
    plan=json.loads(planf.read_text())
    assert plan['packets']
    assert any(p['readiness_hint'] in {'needs_repair_candidate','partial_conversion_allowed_candidate','ready_with_warnings_candidate'} for p in plan['packets'])

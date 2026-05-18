from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import pytest

pytest.importorskip("jsonschema")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r) for r in rows)+"\n", encoding='utf-8')


def _make_packet(tmp_path: Path) -> Path:
    book = tmp_path/'book'; book.mkdir()
    (book/'b.md').write_text("<!-- PAGE:1 -->\nA\n<!-- PAGE:2 -->\n| d6 |\n<!-- PAGE:3 -->\nMap AC HP\n<!-- PAGE:4 -->\nOCR empty\n",encoding='utf-8')
    _write_jsonl(book/'b.page_truth.jsonl',[
        {"book_id":"b","page":1,"page_status":"ok","reason_code":"native_text_extracted"},
        {"book_id":"b","page":2,"page_status":"ok","reason_code":"native_text_extracted"},
        {"book_id":"b","page":3,"page_status":"ok","reason_code":"native_text_extracted"},
        {"book_id":"b","page":4,"page_status":"queued","reason_code":"post_ocr_text_extraction_empty"},
    ])
    (book/'strict_audit.json').write_text(json.dumps({"strict_audit_status":"pass"}),encoding='utf-8')
    (book/'astra_handoff_manifest.json').write_text(json.dumps({"book_id":"b","source_filename":"b.pdf","source_sha256":"abc","extraction_version":"v13"}),encoding='utf-8')
    out=tmp_path/'packet'
    subprocess.run([sys.executable,'scripts/handoff/build_handoff_packet.py','--book-dir',str(book),'--start-page','2','--end-page','4','--packet-id','p1','--packet-purpose','x','--output-dir',str(out)],check=True)
    return out


def _validate(packet: Path, strict=True):
    cmd=[sys.executable,'scripts/handoff/validate_handoff_packet.py','--packet-dir',str(packet)]
    if strict: cmd.append('--strict')
    return subprocess.run(cmd,capture_output=True,text=True)


def test_valid_packet_passes_strict(tmp_path: Path):
    p=_make_packet(tmp_path)
    r=_validate(p,True)
    assert r.returncode==0
    rep=json.loads((p/'packet_validation_report.json').read_text())
    assert rep['valid'] is True
    assert all(not x.get('families') for x in rep.get('risky_family_detection',[]))


def test_missing_required_file_fails(tmp_path: Path):
    p=_make_packet(tmp_path)
    (p/'packet_readme.md').unlink()
    r=_validate(p,True)
    assert r.returncode!=0


def test_invalid_manifest_fails_schema(tmp_path: Path):
    p=_make_packet(tmp_path)
    m=json.loads((p/'packet_manifest.json').read_text()); m.pop('packet_id',None)
    (p/'packet_manifest.json').write_text(json.dumps(m),encoding='utf-8')
    r=_validate(p,True)
    assert r.returncode!=0


def test_page_truth_outside_range_fails(tmp_path: Path):
    p=_make_packet(tmp_path)
    with (p/'page_truth.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps({"book_id":"b","page":999,"page_status":"ok","reason_code":"native_text_extracted"})+'\n')
    r=_validate(p,True)
    assert r.returncode!=0


def test_missing_queue_file_fails(tmp_path: Path):
    p=_make_packet(tmp_path)
    (p/'queues'/'repair_queue.jsonl').unlink()
    r=_validate(p,True)
    assert r.returncode!=0


def test_post_ocr_without_queue_records_fails(tmp_path: Path):
    p=_make_packet(tmp_path)
    (p/'queues'/'ocr_empty_queue.jsonl').write_text('',encoding='utf-8')
    (p/'queues'/'repair_queue.jsonl').write_text('',encoding='utf-8')
    r=_validate(p,True)
    assert r.returncode!=0


def test_canon_candidate_on_repair_required_unit_fails(tmp_path: Path):
    p=_make_packet(tmp_path)
    rec={"queue_id":"qc1","queue_name":"canon_candidate_queue","unit_id":"u_4","book_id":"b","source_pages":[4],"reason_code":"x","blocking_effect":"x","allowed_use":"x","recommended_action":"x","priority":"medium","owner":"x","status":"open"}
    (p/'queues'/'canon_candidate_queue.jsonl').write_text(json.dumps(rec)+'\n',encoding='utf-8')
    r=_validate(p,True)
    assert r.returncode!=0


def test_report_written(tmp_path: Path):
    p=_make_packet(tmp_path)
    _validate(p,True)
    assert (p/'packet_validation_report.json').exists()


def _set_single_unit(packet: Path, unit_type: str, text: str, tags: list[str] | None = None) -> dict:
    unit={
        "unit_id":"u_2","book_id":"b","source_page_start":2,"source_page_end":2,
        "unit_type":unit_type,"text":text,"extraction_status":"ok","content_readiness":"ready",
        "conversion_permission":"allowed","canon_permission":"review_required","defects":[],"confidence":0.9,
        "recommended_queue":None,"lawful_outcome":"normalized_astra_mapping","notes":""
    }
    _write_jsonl(packet/'content_units.jsonl',[unit])
    m=json.loads((packet/'packet_manifest.json').read_text())
    (packet/'packet_manifest.json').write_text(json.dumps(m),encoding='utf-8')
    if tags is not None:
        unit['content_families']=tags
    for q in ['table_normalization_queue','statblock_queue','map_diagram_queue']:
        (packet/'queues'/f'{q}.jsonl').write_text('',encoding='utf-8')
    return unit

def _queue_rec(queue_name: str, unit_id: str, reason: str, action: str, pages=None):
    return {"queue_id":f"q_{queue_name}","queue_name":queue_name,"unit_id":unit_id,"book_id":"b","source_pages":pages or [2],"reason_code":reason,"blocking_effect":"degrades_conversion","allowed_use":"intake_only","recommended_action":action,"priority":"medium","owner":"ops","status":"open"}

def test_table_heavy_without_sidecar_or_queue_fails(tmp_path: Path):
    p=_make_packet(tmp_path)
    _set_single_unit(p,'prose','Random table: d100 | result', ['random_table'])
    r=_validate(p,True)
    assert r.returncode!=0
    rep=json.loads((p/'packet_validation_report.json').read_text())
    assert 'missing_table_sidecar_or_repair_queue' in rep['errors']

def test_table_heavy_with_table_sidecar_passes(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'table','|d6|result|', ['table'])
    table={**u,"table_title":"T","table_format":"markdown","row_count_observed":2,"row_count_expected":2,"table_normalization_status":"normalized","table_defects":[]}
    _write_jsonl(p/'sidecars'/'tables'/'table_units.jsonl',[table])
    r=_validate(p,True)
    assert r.returncode==0

def test_table_heavy_with_table_repair_queue_passes(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'table','random table', ['catalog'])
    _write_jsonl(p/'queues'/'table_normalization_queue.jsonl',[_queue_rec('table_normalization_queue',u['unit_id'],'table_repair_queue','repair table formatting')])
    r=_validate(p,True)
    assert r.returncode==0

def test_statblock_without_sidecar_or_queue_fails(tmp_path: Path):
    p=_make_packet(tmp_path)
    _set_single_unit(p,'prose','Creature AC 16 HP 50 STR 14', ['creature_or_npc'])
    r=_validate(p,True)
    assert r.returncode!=0
    rep=json.loads((p/'packet_validation_report.json').read_text())
    assert 'missing_statblock_sidecar_or_parse_queue' in rep['errors']

def test_statblock_with_sidecar_passes(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'stat_block','AC 16 HP 50', ['statblock'])
    sb={**u,"statblock_family":"npc","donor_engine":"d20","statblock_parse_status":"parsed","statblock_defects":[],"mechanical_import_allowed":False}
    _write_jsonl(p/'sidecars'/'statblocks'/'statblock_units.jsonl',[sb])
    r=_validate(p,True)
    assert r.returncode==0

def test_statblock_with_parse_queue_passes(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'stat_block','AC 16 HP 50', ['statblock'])
    _write_jsonl(p/'queues'/'statblock_queue.jsonl',[_queue_rec('statblock_queue',u['unit_id'],'statblock_parse_queue','parse review required')])
    r=_validate(p,True)
    assert r.returncode==0

def test_map_without_sidecar_or_queue_fails(tmp_path: Path):
    p=_make_packet(tmp_path)
    _set_single_unit(p,'prose','Map and diagram with room key', ['map_or_diagram'])
    r=_validate(p,True)
    assert r.returncode!=0
    rep=json.loads((p/'packet_validation_report.json').read_text())
    assert 'missing_map_sidecar_or_review_queue' in rep['errors']

def test_map_with_sidecar_passes(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'map','Hex map diagram', ['map'])
    mu={**u,"map_title":"M","map_validation_status":"validated","scale_detected":None,"keyed_locations_detected":1,"diagram_defects":[]}
    _write_jsonl(p/'sidecars'/'maps'/'map_units.jsonl',[mu])
    r=_validate(p,True)
    assert r.returncode==0

def test_map_with_review_queue_passes(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'map','Map diagram', ['diagram'])
    _write_jsonl(p/'queues'/'map_diagram_queue.jsonl',[_queue_rec('map_diagram_queue',u['unit_id'],'map_diagram_review_queue','visual review required')])
    r=_validate(p,True)
    assert r.returncode==0



def test_ready_with_warnings_alone_does_not_trigger_sidecar_requirement(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'prose','ordinary prose', ['prose'])
    u['content_readiness']='ready_with_warnings'
    u['defects']=['sparse_page']
    _write_jsonl(p/'content_units.jsonl',[u])
    r=_validate(p,True)
    assert r.returncode==0


def test_needs_repair_alone_does_not_trigger_table_sidecar_requirement(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'prose','ordinary prose', ['prose'])
    u['content_readiness']='needs_repair'
    u['recommended_queue']='repair_queue'
    _write_jsonl(p/'content_units.jsonl',[u])
    _write_jsonl(p/'queues'/'repair_queue.jsonl',[_queue_rec('repair_queue',u['unit_id'],'generic_repair','review')])
    r=_validate(p,True)
    assert r.returncode==0


def test_notes_or_text_containing_table_does_not_trigger_risk(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'prose','this prose says table of contents only', ['prose'])
    u['notes']='contains the word table but not family metadata'
    _write_jsonl(p/'content_units.jsonl',[u])
    r=_validate(p,True)
    assert r.returncode==0
    rep=json.loads((p/'packet_validation_report.json').read_text())
    assert all('table' not in x.get('families',[]) for x in rep.get('risky_family_detection',[]))


def test_explicit_issue_codes_flattened_table_triggers_table_risk(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'prose','ordinary prose', ['prose'])
    u['issue_codes']=['flattened_table']
    _write_jsonl(p/'content_units.jsonl',[u])
    r=_validate(p,True)
    assert r.returncode!=0
    rep=json.loads((p/'packet_validation_report.json').read_text())
    assert 'missing_table_sidecar_or_repair_queue' in rep['errors']
    reasons=rep['risky_family_detection'][0]['reasons']
    assert any(rr['field']=='unit.issue_codes' for rr in reasons)


def test_explicit_repair_queues_table_repair_queue_satisfies_table_risk(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'prose','ordinary prose', ['random_table'])
    u['repair_queues']=['table_repair_queue']
    _write_jsonl(p/'content_units.jsonl',[u])
    _write_jsonl(p/'queues'/'repair_queue.jsonl',[_queue_rec('repair_queue',u['unit_id'],'random_table','table_repair_queue')])
    r=_validate(p,True)
    assert r.returncode==0
def test_normal_prose_packet_remains_valid(tmp_path: Path):
    p=_make_packet(tmp_path)
    _set_single_unit(p,'prose','This is plain prose with no risky structure.', ['prose'])
    r=_validate(p,True)
    assert r.returncode==0


def test_content_unit_schema_accepts_optional_content_families(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'prose','plain prose', ['prose'])
    u['content_families']=['prose']
    _write_jsonl(p/'content_units.jsonl',[u])
    r=_validate(p,True)
    assert (p/'packet_validation_report.json').exists()


def test_sidecar_schemas_accept_optional_content_families(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'table','x', ['table'])
    table={**u,"content_families":["table"],"table_title":"T","table_format":"markdown","row_count_observed":1,"row_count_expected":1,"table_normalization_status":"normalized","table_defects":[]}
    _write_jsonl(p/'sidecars'/'tables'/'table_units.jsonl',[table])
    r=_validate(p,True)
    assert r.returncode==0


def test_report_written_on_schema_validation_failure(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'prose','plain prose', ['prose'])
    u['contract_version']='0.1'
    _write_jsonl(p/'content_units.jsonl',[u])
    r=_validate(p,True)
    assert r.returncode!=0
    rep_path=p/'packet_validation_report.json'
    assert rep_path.exists()
    rep=json.loads(rep_path.read_text())
    assert rep['valid'] is False
    assert any(str(e).startswith('schema_validation_failed:content_unit:') for e in rep['errors'])


def test_report_written_on_missing_sidecar_queue_failure(tmp_path: Path):
    p=_make_packet(tmp_path)
    _set_single_unit(p,'prose','plain prose', ['random_table'])
    r=_validate(p,True)
    assert r.returncode!=0
    rep_path=p/'packet_validation_report.json'
    assert rep_path.exists()
    rep=json.loads(rep_path.read_text())
    assert rep['valid'] is False
    assert 'missing_table_sidecar_or_repair_queue' in rep['errors']


def test_risky_detection_presence_alone_does_not_invalidate(tmp_path: Path):
    p=_make_packet(tmp_path)
    u=_set_single_unit(p,'prose','ordinary prose', ['prose'])
    u['issue_codes']=['unrelated_code']
    _write_jsonl(p/'content_units.jsonl',[u])
    r=_validate(p,True)
    assert r.returncode==0
    rep=json.loads((p/'packet_validation_report.json').read_text())
    assert rep['valid'] is True
    assert 'risky_family_detection' in rep


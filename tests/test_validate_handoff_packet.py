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

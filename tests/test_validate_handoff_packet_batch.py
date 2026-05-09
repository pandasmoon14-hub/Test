from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import pytest

pytest.importorskip('jsonschema')


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r) for r in rows)+"\n", encoding='utf-8')


def _make_packet(root: Path, name: str, bad: bool = False) -> Path:
    book = root / f'{name}_book'; book.mkdir(parents=True)
    (book/'b.md').write_text("<!-- PAGE:1 -->\nA\n<!-- PAGE:2 -->\n| d6 |\n", encoding='utf-8')
    rows=[{"book_id":name,"page":1,"page_status":"ok","reason_code":"native_text_extracted"},{"book_id":name,"page":2,"page_status":"ok","reason_code":"native_text_extracted"}]
    _write_jsonl(book/'b.page_truth.jsonl', rows)
    (book/'strict_audit.json').write_text(json.dumps({"strict_audit_status":"pass"}),encoding='utf-8')
    (book/'astra_handoff_manifest.json').write_text(json.dumps({"book_id":name,"source_filename":"b.pdf","source_sha256":"abc","extraction_version":"v13"}),encoding='utf-8')
    out = root / name
    subprocess.run([sys.executable,'scripts/handoff/build_handoff_packet.py','--book-dir',str(book),'--start-page','1','--end-page','2','--packet-id',name,'--packet-purpose','x','--output-dir',str(out)],check=True)
    if bad:
        (out/'packet_manifest.json').write_text('{\"broken\": true}', encoding='utf-8')
    return out


def _run_batch(root: Path, strict=True):
    cmd=[sys.executable,'scripts/handoff/validate_handoff_packet_batch.py','--packet-root',str(root)]
    if strict: cmd.append('--strict')
    return subprocess.run(cmd,capture_output=True,text=True)


def test_batch_passes_two_valid_packets(tmp_path: Path):
    _make_packet(tmp_path,'p1')
    _make_packet(tmp_path,'p2')
    r=_run_batch(tmp_path,True)
    assert r.returncode==0
    summary=json.loads((tmp_path/'handoff_batch_validation_summary.json').read_text())
    assert summary['packets_total']==2
    assert summary['packets_valid']==2
    assert summary['packets_invalid']==0
    assert summary['counts']['page_truth_rows']==4


def test_batch_invalid_packet_fails_strict(tmp_path: Path):
    _make_packet(tmp_path,'p1')
    _make_packet(tmp_path,'p2',bad=True)
    r=_run_batch(tmp_path,True)
    assert r.returncode!=0
    s=json.loads((tmp_path/'handoff_batch_validation_summary.json').read_text())
    assert s['packets_total']==2


def test_no_packets_found_strict_fails(tmp_path: Path):
    r=_run_batch(tmp_path,True)
    assert r.returncode!=0
    s=json.loads((tmp_path/'handoff_batch_validation_summary.json').read_text())
    assert 'no_packet_folders_found' in s['errors']


def test_individual_reports_written_or_preserved(tmp_path: Path):
    p=_make_packet(tmp_path,'p1')
    r=_run_batch(tmp_path,True)
    assert r.returncode==0
    assert (p/'packet_validation_report.json').exists()

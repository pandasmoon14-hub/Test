from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
import pytest

pytest.importorskip('jsonschema')


def _write_jsonl(path: Path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows)+"\n", encoding='utf-8')


def _mk_book(root: Path, name: str):
    d=root/name; d.mkdir(parents=True)
    (d/'x.md').write_text("<!-- PAGE:1 -->\nText\n<!-- PAGE:2 -->\n|d6|\n", encoding='utf-8')
    _write_jsonl(d/'x.page_truth.jsonl',[{"book_id":name,"page":1,"page_status":"ok","reason_code":"native_text_extracted"},{"book_id":name,"page":2,"page_status":"ok","reason_code":"native_text_extracted"}])
    (d/'strict_audit.json').write_text(json.dumps({"strict_audit_status":"pass"}),encoding='utf-8')
    (d/'astra_handoff_manifest.json').write_text(json.dumps({"book_id":name,"source_filename":"x.pdf","source_sha256":"abc","extraction_version":"v13"}),encoding='utf-8')


def _run(plan: Path, out: Path, strict=True):
    cmd=[sys.executable,'scripts/handoff/build_handoff_packet_batch.py','--plan-file',str(plan),'--output-root',str(out)]
    if strict: cmd.append('--strict')
    return subprocess.run(cmd,capture_output=True,text=True)


def test_batch_builder_two_valid(tmp_path: Path):
    source=tmp_path/'src'; source.mkdir()
    _mk_book(source,'book_alpha'); _mk_book(source,'book_beta')
    plan={"plan_id":"p","source_output_root":str(source),"packets":[
        {"packet_id":"p1","book_match":"alpha","start_page":1,"end_page":2,"packet-purpose":"a"},
        {"packet_id":"p2","book_match":"beta","start_page":1,"end_page":2,"packet_purpose":"b"}
    ]}
    planf=tmp_path/'plan.json'; planf.write_text(json.dumps(plan),encoding='utf-8')
    out=tmp_path/'out'
    r=_run(planf,out,True)
    assert r.returncode==0
    s=json.loads((out/'handoff_batch_build_summary.json').read_text())
    assert s['packets_total']==2 and s['packets_built']==2 and s['packets_failed']==0
    for pid in ['p1','p2']:
        p=out/pid
        for f in ['packet_manifest.json','extracted.md','content_units.jsonl','page_truth.jsonl','conversion_prompt.md','packet_readme.md']:
            assert (p/f).exists()


def test_strict_fails_when_unresolved(tmp_path: Path):
    source=tmp_path/'src'; source.mkdir(); _mk_book(source,'book_alpha')
    plan={"plan_id":"p","source_output_root":str(source),"packets":[{"packet_id":"p1","book_match":"nope","start_page":1,"end_page":2,"packet-purpose":"a"}]}
    pf=tmp_path/'p.json'; pf.write_text(json.dumps(plan),encoding='utf-8')
    out=tmp_path/'out'
    r=_run(pf,out,True)
    assert r.returncode!=0


def test_non_strict_continues_on_unresolved(tmp_path: Path):
    source=tmp_path/'src'; source.mkdir(); _mk_book(source,'book_alpha')
    plan={"plan_id":"p","source_output_root":str(source),"packets":[{"packet_id":"bad","book_match":"nope","start_page":1,"end_page":2,"packet-purpose":"a"},{"packet_id":"good","book_match":"alpha","start_page":1,"end_page":2,"packet-purpose":"b"}]}
    pf=tmp_path/'p.json'; pf.write_text(json.dumps(plan),encoding='utf-8')
    out=tmp_path/'out'
    r=_run(pf,out,False)
    assert r.returncode==0
    s=json.loads((out/'handoff_batch_build_summary.json').read_text())
    assert s['packets_built']==1 and s['packets_failed']==1


def test_multiple_matches_warn_and_pick_first(tmp_path: Path):
    source=tmp_path/'src'; source.mkdir(); _mk_book(source,'book_alpha_1'); _mk_book(source,'book_alpha_2')
    plan={"plan_id":"p","source_output_root":str(source),"packets":[{"packet_id":"p1","book_match":"alpha","start_page":1,"end_page":2,"packet-purpose":"a"}]}
    pf=tmp_path/'p.json'; pf.write_text(json.dumps(plan),encoding='utf-8')
    out=tmp_path/'out'
    r=_run(pf,out,True)
    assert r.returncode==0
    s=json.loads((out/'handoff_batch_build_summary.json').read_text())
    assert any('multiple_book_matches' in w for pr in s['packet_results'] for w in pr.get('warnings',[]))

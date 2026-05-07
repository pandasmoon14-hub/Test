from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

import pytest
jsonschema = pytest.importorskip('jsonschema')


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding='utf-8')


def test_build_handoff_packet(tmp_path: Path):
    book = tmp_path / 'book'
    book.mkdir()
    (book/'sample.md').write_text(
        "<!-- PAGE:1 -->\nProse text.\n\n"
        "<!-- PAGE:2 -->\n| d6 | result |\n|---|---|\n|1|A|\n\n"
        "<!-- PAGE:3 -->\nMap of the hex region.\nAC 15 HP 22\n\n"
        "<!-- PAGE:4 -->\nUnreadable OCR page.\n",
        encoding='utf-8'
    )
    rows = [
        {"book_id":"book","page":1,"page_status":"ok","reason_code":"native_text_extracted"},
        {"book_id":"book","page":2,"page_status":"ok","reason_code":"native_text_extracted"},
        {"book_id":"book","page":3,"page_status":"ok","reason_code":"native_text_extracted"},
        {"book_id":"book","page":4,"page_status":"queued","reason_code":"post_ocr_text_extraction_empty"},
    ]
    _write_jsonl(book/'sample.page_truth.jsonl', rows)
    (book/'strict_audit.json').write_text(json.dumps({"strict_audit_status":"pass"}), encoding='utf-8')
    (book/'astra_handoff_manifest.json').write_text(json.dumps({"book_id":"book","source_filename":"sample.pdf","source_sha256":"abc","extraction_version":"v13"}), encoding='utf-8')

    out = tmp_path / 'handoff_packet'
    cmd = [sys.executable, 'scripts/handoff/build_handoff_packet.py', '--book-dir', str(book), '--start-page', '2', '--end-page', '4', '--packet-id', 'pkt1', '--packet-purpose', 'test purpose', '--output-dir', str(out)]
    subprocess.run(cmd, check=True)

    required = [
        'packet_manifest.json','source_manifest.json','strict_audit.json','page_truth.jsonl','extracted.md','content_units.jsonl','extraction_defects.jsonl','conversion_prompt.md','packet_readme.md'
    ]
    for f in required:
        assert (out/f).exists(), f
    for q in ["repair_queue","table_normalization_queue","map_diagram_queue","statblock_queue","ocr_empty_queue","mojibake_cleanup_queue","layout_reconstruction_queue","lexicon_review_queue","doctrine_escalation_queue","source_local_retention_queue","canon_candidate_queue"]:
        assert (out/'queues'/f'{q}.jsonl').exists()

    ex = (out/'extracted.md').read_text(encoding='utf-8')
    assert '<!-- PAGE:2 -->' in ex and '<!-- PAGE:4 -->' in ex and '<!-- PAGE:1 -->' not in ex

    kept = [json.loads(x) for x in (out/'page_truth.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    assert {r['page'] for r in kept} == {2,3,4}

    schema_dir = Path('schemas/handoff')
    pm_schema = json.loads((schema_dir/'packet_manifest.schema.json').read_text(encoding='utf-8'))
    packet_manifest = json.loads((out/'packet_manifest.json').read_text(encoding='utf-8'))
    jsonschema.validate(packet_manifest, pm_schema)

    cu_schema = json.loads((schema_dir/'content_unit.schema.json').read_text(encoding='utf-8'))
    units = [json.loads(x) for x in (out/'content_units.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    assert units
    for u in units:
        jsonschema.validate(u, cu_schema)

    tqr = (out/'queues'/'table_normalization_queue.jsonl').read_text(encoding='utf-8')
    mqr = (out/'queues'/'map_diagram_queue.jsonl').read_text(encoding='utf-8')
    sqr = (out/'queues'/'statblock_queue.jsonl').read_text(encoding='utf-8')
    oqr = (out/'queues'/'ocr_empty_queue.jsonl').read_text(encoding='utf-8')
    rqr = (out/'queues'/'repair_queue.jsonl').read_text(encoding='utf-8')
    assert tqr.strip()
    assert mqr.strip()
    assert sqr.strip()
    assert oqr.strip()
    assert rqr.strip()

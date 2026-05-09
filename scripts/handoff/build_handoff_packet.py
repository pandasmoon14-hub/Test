from __future__ import annotations
import argparse, json, re, shutil
from pathlib import Path
from collections import defaultdict

try:
    import jsonschema
except Exception:
    jsonschema = None

QUEUE_NAMES = ["repair_queue","table_normalization_queue","map_diagram_queue","statblock_queue","ocr_empty_queue","mojibake_cleanup_queue","layout_reconstruction_queue","lexicon_review_queue","doctrine_escalation_queue","source_local_retention_queue","canon_candidate_queue"]


def _load_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def _read_jsonl(path: Path):
    rows=[]
    for ln in path.read_text(encoding='utf-8').splitlines():
        if ln.strip(): rows.append(json.loads(ln))
    return rows


def _write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows)+("\n" if rows else ""), encoding='utf-8')


def extract_pages(md: str):
    pat = re.compile(r"<!--\s*PAGE:(\d+)\s*-->\s*", re.I)
    parts = pat.split(md)
    out = {}
    i=1
    while i < len(parts):
        p = int(parts[i]); txt = parts[i+1] if i+1 < len(parts) else ""
        out[p]=txt.strip()
        i += 2
    return out


def detect_defects(page, text, row):
    defects=[]
    low=text.lower()
    if row.get('page_status') in {'queued','failed','ocr_needed'}:
        defects.append(('queued_page','high','page status indicates unresolved extraction','repair_queue'))
    if row.get('reason_code') == 'post_ocr_text_extraction_empty':
        defects += [('post_ocr_text_extraction_empty','high','post OCR extraction empty','ocr_empty_queue'),('post_ocr_text_extraction_empty','high','post OCR extraction empty','repair_queue')]
    if '�' in text:
        defects.append(('mojibake','medium','replacement characters detected','mojibake_cleanup_queue'))
    if any(k in low for k in ['|','table','d100','roll']):
        defects.append(('flattened_table','medium','table-like pattern detected','table_normalization_queue'))
    if re.search(r"\n\s*\d+[\.)]\s+", text):
        defects.append(('broken_numbering','low','numbered list pattern detected','table_normalization_queue'))
    if any(k in low for k in ['map','hex','room key','diagram']):
        defects.append(('map_or_diagram_dependency','medium','map/diagram indicators detected','map_diagram_queue'))
    if any(k in low for k in ['ac ','hp ','str ','dex ','con ','stat block']):
        defects.append(('statblock_detected','medium','statblock indicators detected','statblock_queue'))
    if len(text.strip()) < 40:
        defects.append(('sparse_page','low','very low text density',None))
    return defects


def classify_readiness(rows, defects):
    statuses = {r.get('page_status') for r in rows}
    reasons = {r.get('reason_code') for r in rows}
    if not rows:
        return 'failed_extraction'
    if statuses & {'queued','failed','ocr_needed'} or 'post_ocr_text_extraction_empty' in reasons:
        return 'needs_repair'
    if any(d[0] in {'flattened_table','map_or_diagram_dependency','statblock_detected','broken_numbering'} for d in defects):
        return 'intake_only'
    if any(d[0] in {'mojibake','layout_noise','sparse_page'} for d in defects):
        return 'ready_with_warnings'
    if statuses <= {'ok','ocr_done'}:
        return 'ready'
    return 'partial_conversion_allowed'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--book-dir', required=True)
    ap.add_argument('--start-page', type=int, required=True)
    ap.add_argument('--end-page', type=int, required=True)
    ap.add_argument('--packet-id', required=True)
    ap.add_argument('--packet-purpose', required=True)
    ap.add_argument('--output-dir', required=True)
    args=ap.parse_args()

    book_dir=Path(args.book_dir); out=Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out/'queues').mkdir(exist_ok=True)
    for s in ['tables','maps','statblocks','images']:
        (out/'sidecars'/s).mkdir(parents=True, exist_ok=True)

    md_path = next(iter(sorted(book_dir.glob('*.md'))), None)
    pt_path = next(iter(sorted(book_dir.glob('*.page_truth.jsonl'))), None)
    sa_path = book_dir/'strict_audit.json'
    sm_path = book_dir/'astra_handoff_manifest.json'
    if not all([md_path, pt_path, sa_path.exists(), sm_path.exists()]):
        raise SystemExit('missing required source artifacts')

    md = md_path.read_text(encoding='utf-8')
    pages = extract_pages(md)
    sel_pages = {p:t for p,t in pages.items() if args.start_page <= p <= args.end_page}
    extracted_md = "\n\n".join([f"<!-- PAGE:{p} -->\n{sel_pages.get(p,'')}" for p in range(args.start_page,args.end_page+1) if p in sel_pages]).strip()+"\n"
    (out/'extracted.md').write_text(extracted_md, encoding='utf-8')

    rows = [r for r in _read_jsonl(pt_path) if args.start_page <= int(r.get('page',0)) <= args.end_page]
    _write_jsonl(out/'page_truth.jsonl', rows)
    shutil.copy2(sa_path, out/'strict_audit.json')
    shutil.copy2(sm_path, out/'source_manifest.json')
    source_manifest = _load_json(sm_path,{})

    defects=[]; units=[]; queues=defaultdict(list)
    for r in rows:
        p = int(r.get('page',0)); txt = sel_pages.get(p,'')
        dset = detect_defects(p, txt, r)
        for idx,(dtype,sev,ev,q) in enumerate(dset, start=1):
            defects.append({"defect_id":f"d_{p}_{idx}","book_id":source_manifest.get('book_id',book_dir.name),"source_page":p,"defect_type":dtype,"severity":sev,"evidence":ev,"recommended_queue":q})
        low=txt.lower(); utype='prose'
        if any(k in low for k in ['|','table','d100','roll']): utype='table'
        elif any(k in low for k in ['map','hex','room key','diagram']): utype='map'
        elif any(k in low for k in ['ac ','hp ','str ','dex ','con ','stat block']): utype='stat_block'
        elif re.search(r"\n\s*\d+[\.)]\s+", txt): utype='item_list'
        unresolved = r.get('page_status') in {'queued','failed','ocr_needed'} or r.get('reason_code')=='post_ocr_text_extraction_empty'
        unit={"unit_id":f"u_{p}","book_id":source_manifest.get('book_id',book_dir.name),"source_page_start":p,"source_page_end":p,
              "unit_type":utype,"text":txt,"extraction_status":r.get('page_status','ok'),
              "content_readiness":("needs_repair" if unresolved else "ready_with_warnings" if dset else "ready"),
              "conversion_permission":("disallowed" if unresolved else "allowed_with_warnings" if dset else "allowed"),
              "canon_permission":("disallowed" if unresolved else "review_required"),
              "defects":[x[0] for x in dset],"confidence":0.7,"recommended_queue":None,"lawful_outcome":"normalized_astra_mapping","notes":"coarse unit"}
        if unresolved and r.get('reason_code')=='post_ocr_text_extraction_empty':
            unit['recommended_queue']='ocr_empty_queue'
        units.append(unit)

    _write_jsonl(out/'content_units.jsonl', units)
    _write_jsonl(out/'extraction_defects.jsonl', defects)

    for d in defects:
        q=d.get('recommended_queue')
        if q in QUEUE_NAMES:
            rec={"queue_id":f"q_{d['defect_id']}_{q}","queue_name":q,"unit_id":f"u_{d['source_page']}","book_id":d['book_id'],"source_pages":[d['source_page']],"reason_code":d['defect_type'],"blocking_effect":"blocks_conversion" if q in {'repair_queue','ocr_empty_queue'} else 'degrades_conversion',"allowed_use":"intake_only","recommended_action":"review_and_repair","priority":"high" if q in {'repair_queue','ocr_empty_queue'} else 'medium',"owner":"handoff_ops","status":"open"}
            queues[q].append(rec)

    for qn in QUEUE_NAMES:
        _write_jsonl(out/'queues'/f'{qn}.jsonl', queues.get(qn, []))

    readiness = classify_readiness(rows, [(d['defect_type'],None,None,None) for d in defects])
    manifest={
        "packet_id":args.packet_id,
        "book_id":source_manifest.get('book_id',book_dir.name),
        "source_filename":source_manifest.get('source_filename',f"{book_dir.name}.pdf"),
        "source_sha256":source_manifest.get('source_sha256','unknown'),
        "packet_page_start":args.start_page,
        "packet_page_end":args.end_page,
        "extraction_version":source_manifest.get('extraction_version','v13'),
        "strict_audit_status":_load_json(sa_path,{}).get('strict_audit_status','pass'),
        "readiness_class":readiness,
        "content_family_tags":sorted({u['unit_type'] for u in units}) or ['unknown'],
        "required_files":["packet_manifest.json","source_manifest.json","strict_audit.json","page_truth.jsonl","extracted.md","content_units.jsonl","extraction_defects.jsonl"],
        "queues_present":[q for q in QUEUE_NAMES if queues.get(q)],
        "conversion_permissions":sorted({u['conversion_permission'] for u in units}) or ['review_required'],
        "canon_permissions":sorted({u['canon_permission'] for u in units}) or ['review_required'],
        "contract_version":"0.1"
    }
    (out/'packet_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

    q_summary = "\n".join([f"- {q}: {len(queues.get(q,[]))}" for q in QUEUE_NAMES])
    (out/'conversion_prompt.md').write_text(f"""# Conversion Prompt
packet id: {args.packet_id}
book id: {manifest['book_id']}
page range: {args.start_page}-{args.end_page}
purpose: {args.packet_purpose}
readiness: {readiness}

Allowed uses: convert only units marked allowed/allowed_with_warnings.
Blocked uses: do not convert disallowed units; do not treat output as canon.
Queue summary:\n{q_summary}

Use only packet artifacts. Do not consult original PDF. Do not import donor canon as Astra canon. Assign each donor construct exactly one lawful outcome.
""",encoding='utf-8')

    (out/'packet_readme.md').write_text(f"""# Packet README
This handoff packet was built from {book_dir} pages {args.start_page}-{args.end_page}.
Readiness: {readiness}
Queues populated: {', '.join(manifest['queues_present']) or 'none'}.
Use this packet for conversion intake only.
""",encoding='utf-8')

    if jsonschema is not None:
        schemas=Path(__file__).resolve().parents[2]/'schemas'/'handoff'
        m_schema=_load_json(schemas/'packet_manifest.schema.json',{})
        jsonschema.validate(manifest,m_schema)
        c_schema=_load_json(schemas/'content_unit.schema.json',{})
        q_schema=_load_json(schemas/'queue_record.schema.json',{})
        for u in units:
            jsonschema.validate(u,c_schema)
        for qn in QUEUE_NAMES:
            for r in queues.get(qn,[]):
                jsonschema.validate(r,q_schema)
    else:
        print('warning: jsonschema not installed; schema validation skipped')


if __name__ == '__main__':
    main()

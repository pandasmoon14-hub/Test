from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import jsonschema

HEADERS = [
"Extraction Readiness Assessment","Donor Construct Inventory","Astra Mapping Ledger","Queue and Quarantine Actions","Lexicon Delta","Doctrine Escalations","Source-Local Retentions","Rejected Imports","Canon Candidate Notes","Conversion Notes","Confidence and Reviewer Notes"
]
OUTCOMES=["direct Astra mapping","normalized Astra mapping","source-local retained construct","quarantined construct pending later doctrine","escalated doctrine problem"]


def parse_sections(md: str):
    lines=md.splitlines(); sections={h:"" for h in HEADERS}; cur=None; buf=[]
    for ln in lines:
        m=re.match(r"^#+\s*(.+?)\s*$", ln.strip())
        if m and m.group(1) in sections:
            if cur is not None: sections[cur]="\n".join(buf).strip()
            cur=m.group(1); buf=[]
        elif cur is not None:
            buf.append(ln)
    if cur is not None: sections[cur]="\n".join(buf).strip()
    return sections


def norm_outcome(t: str):
    low=t.lower()
    if 'direct' in low: return OUTCOMES[0]
    if 'normalized' in low: return OUTCOMES[1]
    if 'source-local' in low or 'source local' in low: return OUTCOMES[2]
    if 'escalated' in low: return OUTCOMES[4]
    if 'quarantine' in low: return OUTCOMES[3]
    return OUTCOMES[3]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--packet-id', required=True)
    ap.add_argument('--status', default='drafted')
    a=ap.parse_args()
    run=Path(a.run_dir)
    idx_path=run/'packet_index.json'
    if not idx_path.exists():
        print('missing packet_index.json', file=sys.stderr); sys.exit(1)
    idx=json.loads(idx_path.read_text(encoding='utf-8'))
    rec=next((r for r in idx if r.get('packet_id')==a.packet_id), None)
    if rec is None:
        print('packet id not found', file=sys.stderr); sys.exit(1)
    md_path=run/'results'/f"{a.packet_id}_conversion_result.md"
    if not md_path.exists():
        print('missing markdown result', file=sys.stderr); sys.exit(1)
    sections=parse_sections(md_path.read_text(encoding='utf-8'))

    inv=[{"text":ln.strip('- ').strip()} for ln in sections['Donor Construct Inventory'].splitlines() if ln.strip()]

    mappings=[]
    for ln in sections['Astra Mapping Ledger'].splitlines():
        if not ln.strip() or ln.strip().startswith('|---'): continue
        cells=[c.strip() for c in ln.strip('|').split('|') if c.strip()]
        donor=cells[0] if cells else 'unparsed_construct'
        outcome = norm_outcome(cells[1] if len(cells)>1 else ln)
        canon='candidate_only_after_review' if 'candidate only after review' in ln.lower() else 'none'
        mappings.append({
            'donor_construct': donor,
            'source_pages': [int(rec['page_range']['start_page'])],
            'source_unit_ids': [f"{a.packet_id}_unit"],
            'astra_target_family': (cells[2] if len(cells)>2 else 'unknown'),
            'lawful_outcome': outcome,
            'rationale': (cells[3] if len(cells)>3 else 'scaffolded from markdown memo'),
            'must_not_import': False,
            'doctrine_owner': None,
            'canon_candidate_permission': canon,
            'confidence': 0.5,
        })
    if not mappings:
        mappings=[{
            'donor_construct':'memo_summary_construct','source_pages':[int(rec['page_range']['start_page'])],'source_unit_ids':[f"{a.packet_id}_unit"],
            'astra_target_family':'unknown','lawful_outcome':'quarantined construct pending later doctrine','rationale':'No parseable mapping table; conservative fallback',
            'must_not_import':False,'doctrine_owner':None,'canon_candidate_permission':'none','confidence':0.5,
        }]

    conf_match=re.search(r"(?:confidence)\s*[:=]\s*([0-9]*\.?[0-9]+)", sections['Confidence and Reviewer Notes'], re.I)
    conf=float(conf_match.group(1)) if conf_match else 0.5

    obj={
        'result_id':f"{a.packet_id}_conversion_result",'packet_id':a.packet_id,'book_id':rec.get('book_id','unknown'),'source_packet_dir':rec.get('packet_dir',''),
        'page_range':rec.get('page_range',{'start_page':1,'end_page':1}),'result_status':a.status,'extraction_readiness_assessment':sections['Extraction Readiness Assessment'] or rec.get('readiness_class','unknown'),
        'donor_construct_inventory':inv,'mapping_ledger':mappings,'queue_actions':([{'text':x} for x in sections['Queue and Quarantine Actions'].splitlines() if x.strip()]),
        'lexicon_delta':([{'text':x} for x in sections['Lexicon Delta'].splitlines() if x.strip()]),'doctrine_escalations':([{'text':x} for x in sections['Doctrine Escalations'].splitlines() if x.strip()]),
        'source_local_retentions':([{'text':x} for x in sections['Source-Local Retentions'].splitlines() if x.strip()]),'rejected_imports':([{'text':x} for x in sections['Rejected Imports'].splitlines() if x.strip()]),
        'canon_candidate_notes':sections['Canon Candidate Notes'],'conversion_notes':sections['Conversion Notes'],'reviewer_notes':sections['Confidence and Reviewer Notes'],'confidence':conf,
    }

    schema=json.loads((Path(__file__).resolve().parents[2]/'schemas/handoff/conversion_intake_result.schema.json').read_text(encoding='utf-8'))
    jsonschema.validate(obj, schema)
    out=run/'results'/f"{a.packet_id}_conversion_result.json"
    out.write_text(json.dumps(obj,indent=2),encoding='utf-8')
    print(json.dumps({'packet_id':a.packet_id,'written':str(out)},indent=2))

if __name__=='__main__': main()

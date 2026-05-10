from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from collections import Counter


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--run-dir', required=True); a=ap.parse_args()
    d=Path(a.run_dir)
    results=list((d/'results').glob('*_conversion_result.json'))
    rows=[]
    st=Counter(); lo=Counter(); esc=ret=rej=cc=0; conf=[]; rev=[]; ready=[]
    for p in results:
        o=json.loads(p.read_text(encoding='utf-8'))
        st[o.get('result_status','unknown')] += 1
        for m in o.get('mapping_ledger',[]): lo[m.get('lawful_outcome','unknown')] += 1
        esc += len(o.get('doctrine_escalations',[])); ret += len(o.get('source_local_retentions',[])); rej += len(o.get('rejected_imports',[]))
        if o.get('canon_candidate_notes'): cc += 1
        conf.append(float(o.get('confidence',0)))
        if o.get('result_status')=='needs_revision': rev.append(o.get('packet_id'))
        if o.get('result_status') in {'drafted','reviewed'}: ready.append(o.get('packet_id'))
        rows.append({'packet_id':o.get('packet_id'),'book_id':o.get('book_id'),'result_status':o.get('result_status'),'confidence':o.get('confidence')})

    rep={'packets_total':len(results),'result_status_counts':dict(st),'lawful_outcome_counts':dict(lo),'doctrine_escalation_count':esc,'source_local_retention_count':ret,'rejected_import_count':rej,'canon_candidate_note_count':cc,'confidence_avg':(sum(conf)/len(conf) if conf else 0),'confidence_min':(min(conf) if conf else 0),'confidence_max':(max(conf) if conf else 0),'packets_needing_revision':rev,'packets_ready_for_review':ready}
    (d/'reports').mkdir(exist_ok=True)
    (d/'reports/conversion_intake_summary_report.json').write_text(json.dumps(rep,indent=2),encoding='utf-8')
    (d/'reports/conversion_intake_summary_report.md').write_text('# Conversion Intake Summary\n\n'+json.dumps(rep,indent=2),encoding='utf-8')
    with (d/'reports/conversion_intake_packet_table.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['packet_id','book_id','result_status','confidence']); w.writeheader(); w.writerows(rows)
    print(json.dumps(rep,indent=2))

if __name__=='__main__': main()

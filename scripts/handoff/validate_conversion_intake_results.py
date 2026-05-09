from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from collections import Counter
import jsonschema


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--allow-placeholders', action='store_true')
    a=ap.parse_args()
    d=Path(a.run_dir)
    errs=[]; warns=[]
    man=d/'intake_run_manifest.json'; idxp=d/'packet_index.json'
    if not man.exists(): errs.append('missing_intake_run_manifest')
    if not idxp.exists(): errs.append('missing_packet_index')
    schema=json.loads((Path(__file__).resolve().parents[2]/'schemas/handoff/conversion_intake_result.schema.json').read_text(encoding='utf-8'))
    idx=json.loads(idxp.read_text(encoding='utf-8')) if idxp.exists() else []
    statuses=Counter()
    for r in idx:
        for k in ['conversion_prompt_path','result_json_path','result_md_path']:
            if not Path(r[k]).exists(): errs.append(f'missing_file:{k}:{r["packet_id"]}')
        rj=Path(r['result_json_path'])
        if not rj.exists():
            errs.append(f'missing_result_json:{r["packet_id"]}')
            continue
        obj=json.loads(rj.read_text(encoding='utf-8'))
        try: jsonschema.validate(obj,schema)
        except Exception as exc: errs.append(f'schema_invalid:{r["packet_id"]}:{exc}')
        st=obj.get('result_status','unknown'); statuses[st]+=1
        if a.strict and (not a.allow_placeholders) and st=='placeholder': errs.append(f'placeholder_not_allowed:{r["packet_id"]}')

    rep={'run_id':json.loads(man.read_text(encoding='utf-8')).get('run_id','unknown') if man.exists() else 'unknown','valid':len(errs)==0,'strict':bool(a.strict),'allow_placeholders':bool(a.allow_placeholders),'packets_total':len(idx),'result_status_counts':dict(statuses),'errors':errs,'warnings':warns}
    (d/'validation').mkdir(exist_ok=True)
    (d/'validation/conversion_intake_validation_report.json').write_text(json.dumps(rep,indent=2),encoding='utf-8')
    print(json.dumps(rep,indent=2))
    if a.strict and errs: sys.exit(1)

if __name__=='__main__': main()

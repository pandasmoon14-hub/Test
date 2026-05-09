from __future__ import annotations
import argparse, json, shutil
from datetime import datetime, timezone
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--packet-root', required=True)
    ap.add_argument('--selected-plan', required=True)
    ap.add_argument('--output-run-dir', required=True)
    ap.add_argument('--run-id', required=True)
    a=ap.parse_args()

    packet_root=Path(a.packet_root)
    out=Path(a.output_run_dir)
    for d in ['prompts','results','validation','reports']:
        (out/d).mkdir(parents=True, exist_ok=True)

    plan_src=Path(a.selected_plan)
    plan=json.loads(plan_src.read_text(encoding='utf-8-sig'))
    (out/'selected_packet_plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')

    packets=plan.get('packets',[])
    idx=[]
    for p in packets:
        pid=p['packet_id']; pdir=packet_root/pid
        prompt_src=pdir/'conversion_prompt.md'
        prompt_dst=out/'prompts'/f'{pid}_conversion_prompt.md'
        if prompt_src.exists(): shutil.copy2(prompt_src,prompt_dst)
        else: prompt_dst.write_text('# Missing prompt\n',encoding='utf-8')
        json_path=out/'results'/f'{pid}_conversion_result.json'
        md_path=out/'results'/f'{pid}_conversion_result.md'
        placeholder={
            'result_id':f"{a.run_id}_{pid}",'packet_id':pid,'book_id':p.get('book_match','unknown'),'source_packet_dir':str(pdir),
            'page_range':{'start_page':int(p.get('start_page',1)),'end_page':int(p.get('end_page',1))},'result_status':'placeholder',
            'extraction_readiness_assessment':p.get('readiness_hint','unknown'),'donor_construct_inventory':[],'mapping_ledger':[],
            'queue_actions':[],'lexicon_delta':[],'doctrine_escalations':[],'source_local_retentions':[],'rejected_imports':[],
            'canon_candidate_notes':'','conversion_notes':'','reviewer_notes':'','confidence':0.0
        }
        json_path.write_text(json.dumps(placeholder,indent=2),encoding='utf-8')
        md_path.write_text(f"# Conversion Intake Result\n\nPacket ID: {pid}\nBook ID: {p.get('book_match','unknown')}\nPage range: {p.get('start_page')}-{p.get('end_page')}\nStatus: placeholder\n\nPaste or write the conversion-intake memo here.\nUse only the packet artifacts.\nDo not consult original PDF.\nDo not import donor canon as Astra canon.\nAssign every donor construct exactly one lawful outcome.\n",encoding='utf-8')
        idx.append({'packet_id':pid,'packet_dir':str(pdir),'book_id':p.get('book_match','unknown'),'page_range':{'start_page':p.get('start_page'), 'end_page':p.get('end_page')},'readiness_class':p.get('readiness_hint','unknown'),'conversion_prompt_path':str(prompt_dst),'result_json_path':str(json_path),'result_md_path':str(md_path)})

    (out/'packet_index.json').write_text(json.dumps(idx,indent=2),encoding='utf-8')
    manifest={'run_id':a.run_id,'packet_root':str(packet_root),'selected_plan':str(plan_src),'packets_total':len(idx),'created_at':datetime.now(timezone.utc).isoformat(),'status':'initialized'}
    (out/'intake_run_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

if __name__=='__main__': main()

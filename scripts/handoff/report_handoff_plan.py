from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from collections import Counter, defaultdict


def load_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception:
        return default


def risk_and_flags(pkt, qcounts, v_valid, v_errs):
    flags=[]
    queue_total=sum(int(v) for v in qcounts.values())
    cu=max(1,int(pkt.get('usable_page_count',0))+int(pkt.get('repair_page_count',0)))
    qps=queue_total/cu
    if qps>1.5: flags.append('high_queue_pressure')
    if int(qcounts.get('table_normalization_queue',0))>0: flags.append('many_table_normalization_records')
    if int(qcounts.get('map_diagram_queue',0))>0: flags.append('map_dependency_pressure')
    if int(qcounts.get('statblock_queue',0))>0 or pkt.get('dominant_content_family')=='statblock_pressure': flags.append('statblock_pressure')
    if int(qcounts.get('repair_queue',0))>0 or int(qcounts.get('ocr_empty_queue',0))>0: flags.append('repair_pressure')
    if int(pkt.get('sparse_page_count',0))>0: flags.append('sparse_packet')
    if int(pkt.get('text_char_count',0))<600: flags.append('low_text_packet')
    if len(pkt.get('content_family_tags',[]))>4: flags.append('overbroad_tags')
    if 'intake_only' in str(pkt.get('readiness_hint','')): flags.append('intake_only')
    if 'needs_repair' in str(pkt.get('readiness_hint','')): flags.append('needs_repair')
    if (not v_valid) or v_errs>0: flags.append('validation_problem')

    if any(f in flags for f in ['overbroad_tags','validation_problem','repair_pressure']): risk='high'
    elif any(f in flags for f in ['map_dependency_pressure','statblock_pressure','high_queue_pressure','intake_only']): risk='medium'
    else: risk='low'
    return risk, flags, round(qps,3)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--plan-file', required=True)
    ap.add_argument('--packet-root', required=True)
    ap.add_argument('--output-dir', required=True)
    a=ap.parse_args()

    plan=load_json(Path(a.plan_file), {}) or {}
    packets=list(plan.get('packets',[]))
    root=Path(a.packet_root)
    out=Path(a.output_dir); out.mkdir(parents=True, exist_ok=True)
    warnings=[]; errors=[]

    batch=load_json(root/'handoff_batch_validation_summary.json', None)
    if batch is None:
        warnings.append('missing_batch_validation_summary')

    packet_val_by_id={}
    if batch:
        for pr in batch.get('packet_reports',[]):
            packet_val_by_id[pr.get('packet_id')]=pr

    reviews=[]
    for p in packets:
        pid=p.get('packet_id','unknown')
        pr=packet_val_by_id.get(pid)
        if pr is None:
            pr=load_json(root/pid/'packet_validation_report.json', None)
            if pr is None:
                warnings.append(f'missing_packet_validation_report:{pid}')
                pr={"valid":False,"errors":["missing_packet_validation_report"],"warnings":[],"counts":{}}
        qcounts=pr.get('counts',{}).get('queue_records_by_queue',{})
        v_valid=bool(pr.get('valid',False)); v_errs=len(pr.get('errors',[])); v_warns=len(pr.get('warnings',[]))
        risk, flags, qps = risk_and_flags(p, qcounts, v_valid, v_errs)
        reviews.append({
            'packet_id':pid,'book_match':p.get('book_match',''),'start_page':p.get('start_page',0),'end_page':p.get('end_page',0),
            'readiness_hint':p.get('readiness_hint',''),'dominant_content_family':p.get('dominant_content_family','unknown'),'content_family_tags':p.get('content_family_tags',[]),
            'quality_score':p.get('quality_score',0),'text_char_count':p.get('text_char_count',0),'usable_page_count':p.get('usable_page_count',0),
            'repair_page_count':p.get('repair_page_count',0),'sparse_page_count':p.get('sparse_page_count',0),
            'validation_valid':v_valid,'validation_errors':v_errs,'validation_warnings':v_warns,
            'queue_pressure_score':qps,'false_positive_risk':risk,'review_flags':flags
        })

    sumr={
        'readiness_hint_counts':dict(Counter(r['readiness_hint'] for r in reviews)),
        'dominant_content_family_counts':dict(Counter(r['dominant_content_family'] for r in reviews)),
        'content_family_tag_counts':dict(Counter(t for r in reviews for t in r['content_family_tags'])),
        'packet_readiness_counts_from_validation':dict(batch.get('counts',{}).get('readiness_counts',{}) if batch else {}),
        'content_unit_type_counts':dict(batch.get('counts',{}).get('content_unit_type_counts',{}) if batch else {}),
        'queue_records_by_queue':dict(batch.get('counts',{}).get('queue_records_by_queue',{}) if batch else {}),
        'page_status_counts':dict(batch.get('counts',{}).get('page_status_counts',{}) if batch else {}),
        'quality_score_min':min([float(r['quality_score']) for r in reviews], default=0),
        'quality_score_max':max([float(r['quality_score']) for r in reviews], default=0),
        'quality_score_avg':(sum(float(r['quality_score']) for r in reviews)/len(reviews) if reviews else 0),
        'text_char_count_total':sum(int(r['text_char_count']) for r in reviews),
        'usable_page_count_total':sum(int(r['usable_page_count']) for r in reviews),
        'repair_page_count_total':sum(int(r['repair_page_count']) for r in reviews),
        'sparse_page_count_total':sum(int(r['sparse_page_count']) for r in reviews),
    }

    bsum=[]
    bybook=defaultdict(list)
    for r in reviews: bybook[r['book_match']].append(r)
    for b,rows in bybook.items():
        bsum.append({'book_match':b,'packet_count':len(rows),'dominant_content_families':dict(Counter(x['dominant_content_family'] for x in rows)),
                     'readiness_hints':dict(Counter(x['readiness_hint'] for x in rows)),'avg_quality_score':sum(float(x['quality_score']) for x in rows)/len(rows),
                     'total_text_chars':sum(int(x['text_char_count']) for x in rows),'warnings':[]})

    report={'plan_id':plan.get('plan_id','unknown'),'packet_root':str(root),'valid':len(errors)==0,'packets_total':len(reviews),'books_total':len(bybook),
            'warnings':warnings,'errors':errors,'summary':sumr,'book_summary':bsum,'packet_reviews':reviews}

    (out/'handoff_plan_review_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

    # md
    top=sorted(reviews,key=lambda r:(r['false_positive_risk']=='high',r['queue_pressure_score']), reverse=True)[:10]
    md=['# Handoff Plan Review','',f"Plan: {report['plan_id']}",f"Packets: {report['packets_total']} Books: {report['books_total']}",
        '## Readiness Hints',json.dumps(sumr['readiness_hint_counts'],indent=2),'## Dominant Content Families',json.dumps(sumr['dominant_content_family_counts'],indent=2),
        '## Queue Pressure',json.dumps(sumr['queue_records_by_queue'],indent=2),'## Top Risk Packets']
    for r in top: md.append(f"- {r['packet_id']}: risk={r['false_positive_risk']} flags={','.join(r['review_flags'])}")
    md += ['## Recommendations','- Ready/ready_with_warnings packets: prioritize conversion-intake testing.','- Table/map/statblock pressure: prioritize specialty review queues first.','- Needs-repair/validation-problem packets: exclude from immediate conversion tests.']
    (out/'handoff_plan_review_report.md').write_text('\n'.join(md),encoding='utf-8')

    # csv
    fields=['packet_id','book_match','start_page','end_page','readiness_hint','dominant_content_family','content_family_tags','quality_score','text_char_count','usable_page_count','repair_page_count','sparse_page_count','validation_valid','queue_pressure_score','false_positive_risk','review_flags']
    with (out/'packet_review_table.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in reviews:
            row=dict(r); row['content_family_tags']='|'.join(r['content_family_tags']); row['review_flags']='|'.join(r['review_flags']); w.writerow({k:row.get(k) for k in fields})

    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()

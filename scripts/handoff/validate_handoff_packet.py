from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from collections import Counter

QUEUE_FILES=["repair_queue.jsonl","table_normalization_queue.jsonl","map_diagram_queue.jsonl","statblock_queue.jsonl","ocr_empty_queue.jsonl","mojibake_cleanup_queue.jsonl","layout_reconstruction_queue.jsonl","lexicon_review_queue.jsonl","doctrine_escalation_queue.jsonl","source_local_retention_queue.jsonl","canon_candidate_queue.jsonl"]
REQ_FILES=["packet_manifest.json","source_manifest.json","strict_audit.json","page_truth.jsonl","extracted.md","content_units.jsonl","extraction_defects.jsonl","conversion_prompt.md","packet_readme.md"]
REQ_DIRS=["queues","sidecars","sidecars/tables","sidecars/maps","sidecars/statblocks","sidecars/images"]

try:
    import jsonschema
except Exception:
    jsonschema=None

def load_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def load_jsonl(path):
    p=Path(path)
    if not p.exists(): return []
    return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]

def markers(md): return [int(x) for x in re.findall(r"<!--\s*PAGE:(\d+)\s*-->", md)]


def _family_signal(unit: dict, manifest_tags: set[str], family: str) -> bool:
    unit_type=str(unit.get('unit_type','')).lower()
    low_text=str(unit.get('text','')).lower()
    low_defects=[str(x).lower() for x in unit.get('defects',[])]
    tags={str(x).lower() for x in manifest_tags}

    if family=='table':
        tag_hits={'table','random_table','catalog'}
        return (
            unit_type=='table' or
            bool(tags & tag_hits) or
            any(k in low_text for k in ['|','table','random table','d100','catalog']) or
            any('table' in d for d in low_defects)
        )
    if family=='statblock':
        tag_hits={'statblock','stat_block','creature_or_npc','creature','npc'}
        return (
            unit_type=='stat_block' or
            bool(tags & tag_hits) or
            any(k in low_text for k in ['stat block','statblock','ac ','hp ','str ','dex ','con ','creature','npc']) or
            any('stat' in d for d in low_defects)
        )
    if family=='map':
        tag_hits={'map','map_or_diagram','diagram'}
        return (
            unit_type=='map' or
            bool(tags & tag_hits) or
            any(k in low_text for k in ['map','diagram','room key','hex']) or
            any('map' in d or 'diagram' in d for d in low_defects)
        )
    return False


def _has_matching_sidecar(sidecar_rows: list[dict], unit: dict) -> bool:
    uid=unit.get('unit_id')
    usp=int(unit.get('source_page_start',0)); uep=int(unit.get('source_page_end',0))
    for row in sidecar_rows:
        if uid and row.get('unit_id')==uid:
            return True
        rsp=int(row.get('source_page_start',0)); rep=int(row.get('source_page_end',0))
        if rsp and rep and not (rep<usp or rsp>uep):
            return True
    return False


def _queue_record_covers_unit(records: list[dict], unit: dict, reason_tokens: tuple[str, ...], action_tokens: tuple[str, ...]) -> bool:
    uid=unit.get('unit_id')
    usp=int(unit.get('source_page_start',0)); uep=int(unit.get('source_page_end',0))
    for rec in records:
        if rec.get('unit_id') not in {uid, None, ''}:
            continue
        pages=[int(x) for x in rec.get('source_pages',[]) if isinstance(x,int)]
        if pages and all((p<usp or p>uep) for p in pages):
            continue
        rc=str(rec.get('reason_code','')).lower()
        ra=str(rec.get('recommended_action','')).lower()
        qn=str(rec.get('queue_name','')).lower()
        if any(t in qn or t in rc for t in reason_tokens) or any(t in ra for t in action_tokens):
            return True
    return False

def validate_packet(packet_dir: str | Path, strict: bool = False) -> tuple[dict, int]:
    d=Path(packet_dir)
    a_strict = strict
    errors=[]; warnings=[]

    for f in REQ_FILES:
        if not (d/f).exists(): errors.append(f"missing_file:{f}")
    for p in REQ_DIRS:
        if not (d/p).exists(): errors.append(f"missing_dir:{p}")
    for q in QUEUE_FILES:
        if not (d/'queues'/q).exists(): errors.append(f"missing_queue_file:{q}")

    packet_id='unknown'
    counts={"page_truth_rows":0,"extracted_page_markers":0,"content_units":0,"extraction_defects":0,"queue_records_by_queue":{},"page_status_counts":{},"content_unit_type_counts":{},"readiness_counts":{}}

    if not errors:
        manifest=load_json(d/'packet_manifest.json'); packet_id=manifest.get('packet_id','unknown')
        pt=load_jsonl(d/'page_truth.jsonl'); units=load_jsonl(d/'content_units.jsonl'); defects=load_jsonl(d/'extraction_defects.jsonl')
        md=(d/'extracted.md').read_text(encoding='utf-8')
        qrecs={q[:-6]:load_jsonl(d/'queues'/q) for q in QUEUE_FILES}
        table_sidecars=load_jsonl(d/'sidecars'/'tables'/'table_units.jsonl')
        map_sidecars=load_jsonl(d/'sidecars'/'maps'/'map_units.jsonl')
        statblock_sidecars=load_jsonl(d/'sidecars'/'statblocks'/'statblock_units.jsonl')

        counts['page_truth_rows']=len(pt); counts['extracted_page_markers']=len(markers(md)); counts['content_units']=len(units); counts['extraction_defects']=len(defects)
        counts['queue_records_by_queue']={k:len(v) for k,v in qrecs.items()}
        counts['page_status_counts']=dict(Counter(str(r.get('page_status')) for r in pt))
        counts['content_unit_type_counts']=dict(Counter(str(u.get('unit_type')) for u in units))
        counts['readiness_counts']=dict(Counter(str(u.get('content_readiness')) for u in units))

        s,e=int(manifest['packet_page_start']),int(manifest['packet_page_end'])
        pages=set(range(s,e+1))
        pt_pages={int(r.get('page',0)) for r in pt}
        if any((p<s or p>e) for p in pt_pages): errors.append('page_truth_out_of_range')
        mset=set(markers(md))
        if a_strict and not pages.issubset(pt_pages): errors.append('missing_page_truth_for_selected_range')
        if a_strict:
            for p in pages:
                if p not in mset:
                    row=next((r for r in pt if int(r.get('page',0))==p),{})
                    if row.get('page_status') not in {'queued','failed'}: errors.append(f'missing_marker:{p}')

        if jsonschema is None:
            (errors if a_strict else warnings).append('jsonschema_unavailable')
        else:
            root=Path(__file__).resolve().parents[2]/'schemas'/'handoff'
            jsonschema.validate(manifest, load_json(root/'packet_manifest.schema.json'))
            cu=load_json(root/'content_unit.schema.json'); qr=load_json(root/'queue_record.schema.json')
            for u in units: jsonschema.validate(u, cu)
            for recs in qrecs.values():
                for r in recs: jsonschema.validate(r, qr)

        non_ready={'needs_repair','failed_extraction','quarantined','intake_only'}
        for u in units:
            us,ue=int(u.get('source_page_start',0)),int(u.get('source_page_end',0))
            if us<s or ue>e: errors.append('unit_out_of_range')
            for k in ['content_readiness','extraction_status','conversion_permission','canon_permission']:
                if not u.get(k): errors.append(f'missing_{k}')
            if u.get('content_readiness') in non_ready and not (u.get('recommended_queue') or u.get('lawful_outcome') or u.get('notes')):
                errors.append('non_ready_without_explanation')
            if u.get('recommended_queue') and f"{u['recommended_queue']}.jsonl" not in QUEUE_FILES:
                errors.append('recommended_queue_missing_file')
            if u.get('content_readiness') in non_ready and u.get('canon_permission') in {'allowed','allowed_with_warnings'}:
                errors.append('canon_permission_invalid_for_non_ready')

        if any(r.get('reason_code')=='post_ocr_text_extraction_empty' for r in pt):
            if len(qrecs['ocr_empty_queue'])==0 or len(qrecs['repair_queue'])==0: errors.append('missing_ocr_empty_or_repair_queue_records')

        byid={u['unit_id']:u for u in units if 'unit_id' in u}
        for u in units:
            if u.get('unit_type')=='table' and u.get('content_readiness')!='ready' and len(qrecs['table_normalization_queue'])==0: errors.append('missing_table_normalization_queue_record')
            if u.get('unit_type')=='map' and u.get('content_readiness')!='ready' and len(qrecs['map_diagram_queue'])==0: errors.append('missing_map_diagram_queue_record')
            if u.get('unit_type')=='stat_block' and u.get('content_readiness')!='ready' and len(qrecs['statblock_queue'])==0: errors.append('missing_statblock_queue_record')

        manifest_tags={str(x).lower() for x in manifest.get('content_family_tags',[])}
        for u in units:
            if _family_signal(u, manifest_tags, 'table'):
                if not _has_matching_sidecar(table_sidecars, u) and not _queue_record_covers_unit(qrecs['table_normalization_queue'], u, ('table','random_table','catalog'), ('repair','normalize','review')):
                    errors.append('missing_table_sidecar_or_repair_queue')
            if _family_signal(u, manifest_tags, 'statblock'):
                if not _has_matching_sidecar(statblock_sidecars, u) and not _queue_record_covers_unit(qrecs['statblock_queue'], u, ('stat','creature','npc','parse'), ('parse','review','repair')):
                    errors.append('missing_statblock_sidecar_or_parse_queue')
            if _family_signal(u, manifest_tags, 'map'):
                if not _has_matching_sidecar(map_sidecars, u) and not _queue_record_covers_unit(qrecs['map_diagram_queue'], u, ('map','diagram','visual'), ('review','repair','validate')):
                    errors.append('missing_map_sidecar_or_review_queue')

        queued_pages={int(r.get('page',0)) for r in pt if r.get('page_status') in {'queued','failed'}}
        if queued_pages and len(qrecs['repair_queue'])==0: errors.append('queued_pages_without_repair_records')

        for rec in qrecs['canon_candidate_queue']:
            uid=rec.get('unit_id'); u=byid.get(uid,{})
            if u.get('content_readiness') in non_ready or u.get('extraction_status') in {'queued','failed','ocr_needed'}:
                errors.append('canon_candidate_points_to_non_ready_unit')

    report={"packet_id":packet_id,"packet_dir":str(d),"valid":len(errors)==0,"errors":errors,"warnings":warnings,"counts":counts}
    (d/'packet_validation_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    exit_code = 1 if (a_strict and errors) else 0
    return report, exit_code


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--packet-dir', required=True)
    ap.add_argument('--strict', action='store_true')
    a=ap.parse_args()
    report, exit_code = validate_packet(a.packet_dir, strict=a.strict)
    print(json.dumps(report,indent=2))
    if exit_code:
        sys.exit(exit_code)

if __name__=='__main__':
    main()

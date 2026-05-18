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


def _norm_tokens(value) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, (list, tuple, set)):
        out=set()
        for item in value:
            out |= _norm_tokens(item)
        return out
    text=str(value).lower().replace('-', '_').replace('/', '_').replace(' ', '_')
    parts=[p for p in re.split(r"[^a-z0-9_]+", text) if p]
    return set(parts)


def _detect_risky_families(unit: dict, manifest: dict) -> tuple[set[str], list[dict]]:
    family_signals={
        'table': {"random_table","table","table_unit","catalog","item_catalog","gear_catalog","loot_table","flattened_table"},
        'statblock': {"statblock","stat_block","creature_or_npc","npc","monster","adversary","collapsed_statblock","statblock_collapse"},
        'map': {"map","diagram","map_or_diagram","map_unit","unreadable_map","map_unreadable","visual_review"},
    }
    allowed_fields=[
        ('manifest.content_family', manifest.get('content_family')),
        ('manifest.content_families', manifest.get('content_families')),
        ('manifest.family', manifest.get('family')),
        ('manifest.families', manifest.get('families')),
        ('manifest.unit_family', manifest.get('unit_family')),
        ('manifest.unit_families', manifest.get('unit_families')),
        ('manifest.content_type', manifest.get('content_type')),
        ('manifest.content_types', manifest.get('content_types')),
        ('manifest.modality', manifest.get('modality')),
        ('manifest.modalities', manifest.get('modalities')),
        ('manifest.structure_type', manifest.get('structure_type')),
        ('manifest.structure_types', manifest.get('structure_types')),
        ('manifest.issue_code', manifest.get('issue_code')),
        ('manifest.issue_codes', manifest.get('issue_codes')),
        ('manifest.defect_code', manifest.get('defect_code')),
        ('manifest.defect_codes', manifest.get('defect_codes')),
        ('manifest.queue_type', manifest.get('queue_type')),
        ('manifest.queue_types', manifest.get('queue_types')),
        ('manifest.repair_queue', manifest.get('repair_queue')),
        ('manifest.repair_queues', manifest.get('repair_queues')),
        ('manifest.declared_content_families', manifest.get('declared_content_families')),
        ('unit.content_family', unit.get('content_family')),
        ('unit.content_families', unit.get('content_families')),
        ('unit.family', unit.get('family')),
        ('unit.families', unit.get('families')),
        ('unit.unit_family', unit.get('unit_family')),
        ('unit.unit_families', unit.get('unit_families')),
        ('unit.content_type', unit.get('content_type')),
        ('unit.content_types', unit.get('content_types')),
        ('unit.modality', unit.get('modality')),
        ('unit.modalities', unit.get('modalities')),
        ('unit.structure_type', unit.get('structure_type')),
        ('unit.structure_types', unit.get('structure_types')),
        ('unit.issue_code', unit.get('issue_code')),
        ('unit.issue_codes', unit.get('issue_codes')),
        ('unit.defect_code', unit.get('defect_code')),
        ('unit.defect_codes', unit.get('defect_codes')),
        ('unit.queue_type', unit.get('queue_type')),
        ('unit.queue_types', unit.get('queue_types')),
        ('unit.repair_queue', unit.get('repair_queue')),
        ('unit.repair_queues', unit.get('repair_queues')),
        ('unit.declared_content_families', unit.get('declared_content_families')),
    ]
    detected=set(); reasons=[]
    for path, value in allowed_fields:
        toks=_norm_tokens(value)
        if not toks:
            continue
        for fam, signals in family_signals.items():
            hits=sorted(toks & signals)
            if hits:
                detected.add(fam)
                reasons.append({'family': fam, 'field': path, 'value': value, 'signals': hits})
        if 'image_text_missing' in toks and bool(toks & {'map','diagram','map_or_diagram'}):
            detected.add('map')
            reasons.append({'family': 'map', 'field': path, 'value': value, 'signals': ['image_text_missing']})
    return detected, reasons

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


def _queue_record_covers_unit(records: list[dict], unit: dict, family: str) -> bool:
    family_tokens={
        'table': {'table','random_table','catalog','item_catalog','gear_catalog','loot_table','flattened_table'},
        'statblock': {'statblock','stat_block','creature_or_npc','npc','monster','adversary','collapsed_statblock','statblock_collapse'},
        'map': {'map','diagram','map_or_diagram','map_unit','unreadable_map','map_unreadable','visual_review'},
    }[family]
    queue_aliases={
        'table': {'table_normalization_queue','table_repair_queue'},
        'statblock': {'statblock_queue','statblock_parse_queue'},
        'map': {'map_diagram_queue','map_diagram_review_queue'},
    }[family]

    uid=unit.get('unit_id')
    usp=int(unit.get('source_page_start',0)); uep=int(unit.get('source_page_end',0))
    for rec in records:
        if rec.get('unit_id') not in {uid, None, ''}:
            continue
        pages=[int(x) for x in rec.get('source_pages',[]) if isinstance(x,int)]
        if pages and all((p<usp or p>uep) for p in pages):
            continue

        qname=str(rec.get('queue_name','')).lower().replace('-', '_')
        tokens=_norm_tokens([rec.get('queue_name'), rec.get('reason_code'), rec.get('recommended_action'), rec.get('blocking_effect'), rec.get('allowed_use')])

        if qname in queue_aliases or bool(tokens & queue_aliases):
            return True
        if qname=='manual_review_queue' and bool(tokens & family_tokens):
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
    risky_detection=[]
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

        start_page,end_page=int(manifest['packet_page_start']),int(manifest['packet_page_end'])
        pages=set(range(start_page,end_page+1))
        pt_pages={int(r.get('page',0)) for r in pt}
        if any((p<start_page or p>end_page) for p in pt_pages): errors.append('page_truth_out_of_range')
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
            cu=load_json(root/'content_unit.schema.json'); qr=load_json(root/'queue_record.schema.json')
            try:
                jsonschema.validate(manifest, load_json(root/'packet_manifest.schema.json'))
            except Exception as e:
                errors.append(f'schema_validation_failed:packet_manifest:{e}')
            for i,u in enumerate(units, start=1):
                try:
                    jsonschema.validate(u, cu)
                except Exception as e:
                    errors.append(f'schema_validation_failed:content_unit:{i}:{e}')
            for qn,recs in qrecs.items():
                for i,r in enumerate(recs, start=1):
                    try:
                        jsonschema.validate(r, qr)
                    except Exception as e:
                        errors.append(f'schema_validation_failed:queue_record:{qn}:{i}:{e}')

        non_ready={'needs_repair','failed_extraction','quarantined','intake_only'}
        for u in units:
            us,ue=int(u.get('source_page_start',0)),int(u.get('source_page_end',0))
            if us<start_page or ue>end_page: errors.append('unit_out_of_range')
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

        for u in units:
            families, reasons = _detect_risky_families(u, manifest)
            risky_detection.append({'unit_id': u.get('unit_id'), 'families': sorted(families), 'reasons': reasons})
            if 'table' in families:
                table_records=qrecs['table_normalization_queue'] + qrecs['repair_queue']
                if not _has_matching_sidecar(table_sidecars, u) and not _queue_record_covers_unit(table_records, u, 'table'):
                    errors.append('missing_table_sidecar_or_repair_queue')
            if 'statblock' in families:
                stat_records=qrecs['statblock_queue'] + qrecs['repair_queue']
                if not _has_matching_sidecar(statblock_sidecars, u) and not _queue_record_covers_unit(stat_records, u, 'statblock'):
                    errors.append('missing_statblock_sidecar_or_parse_queue')
            if 'map' in families:
                map_records=qrecs['map_diagram_queue'] + qrecs['repair_queue']
                if not _has_matching_sidecar(map_sidecars, u) and not _queue_record_covers_unit(map_records, u, 'map'):
                    errors.append('missing_map_sidecar_or_review_queue')

        queued_pages={int(r.get('page',0)) for r in pt if r.get('page_status') in {'queued','failed'}}
        if queued_pages and len(qrecs['repair_queue'])==0: errors.append('queued_pages_without_repair_records')

        for rec in qrecs['canon_candidate_queue']:
            uid=rec.get('unit_id'); u=byid.get(uid,{})
            if u.get('content_readiness') in non_ready or u.get('extraction_status') in {'queued','failed','ocr_needed'}:
                errors.append('canon_candidate_points_to_non_ready_unit')

    report={"packet_id":packet_id,"packet_dir":str(d),"strict":bool(a_strict),"valid":len(errors)==0,"errors":errors,"warnings":warnings,"counts":counts,"summary":{"error_count":len(errors),"warning_count":len(warnings)},"risky_family_detection":risky_detection}
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

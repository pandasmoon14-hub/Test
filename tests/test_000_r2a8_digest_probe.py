"""Temporary collection-time measurement probe for R2A-8."""
import collections, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPECTED_R7_PATH='f5ddc972d65ee8ba366da0136fb692d5b64ec2f9ce3c0690f582db53b7fed1ca'
EXPECTED_R7_PAIR='6c38b13c3982f608b5465af6902a51316dcff5cd256d9b079708424d5c24fec0'
DISPOSITION_INDEXES=(
 'docs/doctrine/reviews/r2a/dispositions_current_a/index.yaml',
 'docs/doctrine/reviews/r2a/dispositions_current_b/index.yaml',
 'docs/doctrine/reviews/r2a/dispositions_runtime_schema/index.yaml',
 'docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml',
)
SURFACE_INDEXES=(
 'docs/doctrine/reviews/r2a/semantic_core_agency/index.yaml',
 'docs/doctrine/reviews/r2a/semantic_world_coordination/index.yaml',
)

def h(b): return hashlib.sha256(b).hexdigest()
def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def variants(paths,pairs):
 return ({
  'newline_final':h(('\n'.join(paths)+'\n').encode()),
  'newline_no_final':h('\n'.join(paths).encode()),
  'nul_final':h(b''.join(p.encode()+b'\0' for p in paths)),
  'nul_no_final':h(b'\0'.join(p.encode() for p in paths)),
  'json_compact':h(json.dumps(paths,separators=(',',':')).encode()),
  'json_default':h(json.dumps(paths).encode()),
  'repr':h(repr(paths).encode()),
  'concat':h(''.join(paths).encode()),
 },{
  'path_tab_blob_final':h(''.join(f'{p}\t{s}\n' for p,s in pairs).encode()),
  'path_tab_blob_no_final':h('\n'.join(f'{p}\t{s}' for p,s in pairs).encode()),
  'path_space_blob_final':h(''.join(f'{p} {s}\n' for p,s in pairs).encode()),
  'blob_tab_path_final':h(''.join(f'{s}\t{p}\n' for p,s in pairs).encode()),
  'nul_fields_records':h(b''.join(p.encode()+b'\0'+s.encode()+b'\0' for p,s in pairs)),
  'json_lists_compact':h(json.dumps([[p,s] for p,s in pairs],separators=(',',':')).encode()),
  'json_lists_default':h(json.dumps([[p,s] for p,s in pairs]).encode()),
  'json_dict_compact':h(json.dumps(dict(pairs),sort_keys=True,separators=(',',':')).encode()),
  'repr':h(repr(pairs).encode()),
  'concat':h(''.join(p+s for p,s in pairs).encode()),
 })

all_records=[]; by_phase={}; shard_issues=[]
for ipath in DISPOSITION_INDEXES:
 idx=load(ipath); rows=[]
 for meta in idx['shards']:
  raw=(ROOT/meta['path']).read_bytes(); shard=json.loads(raw); part=shard['candidate_file_dispositions']
  if h(raw)!=meta['content_sha256'] or len(part)!=meta['record_count']: shard_issues.append(meta['path'])
  rows+=part
 by_phase[idx['phase']]=rows; all_records+=rows

r7=by_phase['R2A-7']
r7_paths=sorted(r['path'] for r in r7); r7_pairs=sorted((r['path'],r['baseline_blob_sha']) for r in r7)
r7pv,r7bv=variants(r7_paths,r7_pairs)
all_paths=sorted(r['path'] for r in all_records); all_pairs=sorted((r['path'],r['baseline_blob_sha']) for r in all_records)
allpv,allbv=variants(all_paths,all_pairs)

surfaces={}; surface_shard_issues=[]
for ipath in SURFACE_INDEXES:
 idx=load(ipath)
 for meta in idx['shards']:
  raw=(ROOT/meta['path']).read_bytes(); shard=json.loads(raw); rows=shard['surface_records']
  if h(raw)!=meta['content_sha256'] or len(rows)!=meta['record_count']: surface_shard_issues.append(meta['path'])
  for row in rows:
   if row['surface_id'] in surfaces: raise RuntimeError('duplicate surface id '+row['surface_id'])
   surfaces[row['surface_id']]=row
accepted={sid for sid,row in surfaces.items() if row['semantic_status']=='validated'}
refs=[sid for row in all_records for sid in row['mapped_surface_ids']]
evidence=[e for row in all_records for e in row['mapping_evidence']]
referenced=set(refs)
result={
 'disposition_counts':{phase:len(rows) for phase,rows in sorted(by_phase.items())},
 'disposition_total':len(all_records),
 'unique_path_count':len(set(all_paths)),
 'unique_id_count':len({r['candidate_file_id'] for r in all_records}),
 'shard_issues':shard_issues,
 'r7_historical':{
  'count':len(r7),
  'path_matches':[k for k,v in r7pv.items() if v==EXPECTED_R7_PATH],
  'pair_matches':[k for k,v in r7bv.items() if v==EXPECTED_R7_PAIR],
  'path_variants':r7pv,'pair_variants':r7bv,
 },
 'aggregate_825':{'path_variants':allpv,'pair_variants':allbv},
 'reciprocity':{
  'surface_count':len(surfaces),'validated_surface_count':len(accepted),
  'surface_shard_issues':surface_shard_issues,
  'mapped_surface_reference_count':len(refs),'mapping_evidence_count':len(evidence),
  'unique_referenced_surface_count':len(referenced),
  'unreferenced_validated_surface_count':len(accepted-referenced),
  'unknown_or_nonvalidated_reference_count':len([sid for sid in refs if sid not in accepted]),
  'ordered_mapping_mismatch_count':sum([e['mapped_surface_id'] for e in r['mapping_evidence']]!=r['mapped_surface_ids'] for r in all_records),
  'authority_transfer_violation_count':sum(e['authority_transfer_effect']!='none' for e in evidence),
  'relationship_counts':dict(sorted(collections.Counter(e['mapping_relationship'] for e in evidence).items())),
 },
 'r7_0507_count':sum(r['candidate_file_id']=='R2A-DISPOSITION-R7-0507' for r in all_records),
 'r7_0508_count':sum(r['candidate_file_id']=='R2A-DISPOSITION-R7-0508' for r in all_records),
}
raise RuntimeError('R2A8_FAST_PROBE='+json.dumps(result,sort_keys=True,separators=(',',':')))

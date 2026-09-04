"""Temporary collection-time measurement probe for R2A-8 zero-reference classification."""
import collections, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
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

records=[]
for ipath in DISPOSITION_INDEXES:
 idx=load(ipath)
 for meta in idx['shards']:
  records += load(meta['path'])['candidate_file_dispositions']
record_by_path={r['path']:r for r in records}
refs={sid for r in records for sid in r['mapped_surface_ids']}

surfaces={}
for ipath in SURFACE_INDEXES:
 idx=load(ipath)
 for meta in idx['shards']:
  for row in load(meta['path'])['surface_records']:
   surfaces[row['surface_id']]=row
accepted={sid for sid,row in surfaces.items() if row['semantic_status']=='validated'}
missing=sorted(accepted-refs)
classification=[]
for sid in missing:
 row=surfaces[sid]
 candidate=record_by_path.get(row['path'])
 classification.append({
  'surface_id':sid,
  'path':row['path'],
  'surface_kind':row['surface_kind'],
  'semantic_role':row['semantic_role'],
  'authority_level':row['authority_level'],
  'currentness':row['currentness'],
  'source_record_kind':row['source_record_kind'],
  'source_record_id':row['source_record_id'],
  'source_proposition':row['source_proposition'],
  'candidate_present':candidate is not None,
  'candidate_file_id':candidate['candidate_file_id'] if candidate else None,
  'candidate_disposition':candidate['disposition'] if candidate else None,
  'candidate_mapped_surface_ids':candidate['mapped_surface_ids'] if candidate else None,
  'candidate_semantic_review_summary':candidate['semantic_review_summary'] if candidate else None,
 })
raise RuntimeError('R2A8_ZERO_REF='+json.dumps({
 'accepted_surface_count':len(accepted),
 'referenced_surface_count':len(refs),
 'unreferenced':classification,
},sort_keys=True,separators=(',',':')))

"""Temporary collection-time probe for historical R2A-7 digest framing."""
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml'
EXPECTED_PATH='f5ddc972d65ee8ba366da0136fb692d5b64ec2f9ce3c0690f582db53b7fed1ca'
EXPECTED_PAIR='6c38b13c3982f608b5465af6902a51316dcff5cd256d9b079708424d5c24fec0'

def h(b): return hashlib.sha256(b).hexdigest()
idx=json.loads(INDEX.read_text(encoding='utf-8'))
records=[]
for meta in idx['shards']:
    records += json.loads((ROOT/meta['path']).read_text(encoding='utf-8'))['candidate_file_dispositions']
paths=sorted(r['path'] for r in records)
pairs=sorted((r['path'],r['baseline_blob_sha']) for r in records)
path_variants={
 'newline_final':h(('\n'.join(paths)+'\n').encode()),
 'newline_no_final':h('\n'.join(paths).encode()),
 'nul_final':h(b''.join(p.encode()+b'\0' for p in paths)),
 'nul_no_final':h(b'\0'.join(p.encode() for p in paths)),
 'json_compact':h(json.dumps(paths,separators=(',',':')).encode()),
 'json_default':h(json.dumps(paths).encode()),
 'repr':h(repr(paths).encode()),
 'concat':h(''.join(paths).encode()),
}
pair_variants={
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
}
raise RuntimeError('R2A8_R7_DIGEST_PROBE='+json.dumps({
 'count':len(records),
 'path_matches':[k for k,v in path_variants.items() if v==EXPECTED_PATH],
 'pair_matches':[k for k,v in pair_variants.items() if v==EXPECTED_PAIR],
 'path_variants':path_variants,
 'pair_variants':pair_variants,
},sort_keys=True,separators=(',',':')))

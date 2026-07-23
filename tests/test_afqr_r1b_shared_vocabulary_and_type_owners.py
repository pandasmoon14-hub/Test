"""Semantic gates for AFQR-01–20 R1B vocabulary/type-owner consolidation."""
from __future__ import annotations
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VOC=ROOT/'docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml'
REV=ROOT/'docs/doctrine/reviews'; WORK=ROOT/'working/afqr_consolidation_inputs'
BASE='1855cb2460542c0f912a0830276c9cdea90f1b07'
REQUIRED=[VOC,REV/'afqr_r1b_vocabulary_resolution_report.md',REV/'afqr_r1b_unresolved_term_escalation_ledger.yaml',Path(__file__),REV/'afqr_01_20_authority_status_index.yaml',REV/'afqr_01_20_dependency_matrix.yaml',REV/'afqr_01_20_shared_term_collision_inventory.md',REV/'afqr_01_20_consolidation_file_manifest.yaml',WORK/'manifest.yaml']
def load(p): return json.loads(p.read_text(encoding='utf8'))
def git(*args): return subprocess.run(['git',*args],cwd=ROOT,text=True,check=True,capture_output=True).stdout

def test_required_files_exist_and_all_yaml_parse():
 assert all(p.is_file() for p in REQUIRED)
 for p in [VOC,REV/'afqr_r1b_unresolved_term_escalation_ledger.yaml',REV/'afqr_01_20_authority_status_index.yaml',REV/'afqr_01_20_dependency_matrix.yaml',REV/'afqr_01_20_consolidation_file_manifest.yaml',WORK/'manifest.yaml']: assert isinstance(load(p),dict)
def test_exact_collisions_and_normalized_terms():
 d=load(VOC); cs=d['collision_resolutions']; ts=d['term_records']
 assert [c['collision_id'] for c in cs]==[f'COLL-{i:02d}' for i in range(1,11)]
 assert len(ts)==len({t['root_term'] for t in ts})==41
 assert [t['root_term'] for t in ts].count('social state')==1 and 'social' not in {t['root_term'] for t in ts}
def test_controlled_dispositions_owners_and_qualified_forms():
 d=load(VOC); dispositions={'canonical_distinct_type','qualified_canonical_family','allowed_one_to_one_alias','reserved_ambiguous','rejected_cross_type_alias','source_local_only','escalated_unresolved'}; kinds={'afqr','project_governance','shared_qualified_family','unresolved_escalation'}
 for t in d['term_records']:
  assert t['vocabulary_disposition'] in dispositions and t['type_owner']['owner_kind'] in kinds
  assert t['type_owner']['owner_id'] and t['type_owner']['owner_scope'] and t['type_owner']['owner_file']
  if t['type_owner']['owner_kind']=='afqr': assert t['type_owner']['owner_id'] in {f'AFQR-{i:02d}' for i in range(1,21)}
  for q in t['qualified_forms']: assert q['qualified_form'] and q['definition'] and q['owner_kind'] in kinds and q['owner_id']
def test_all_evidence_is_manifest_backed_and_historical_sources_remain_traceable():
 ids={x['source_record_id'] for x in load(WORK/'manifest.yaml')['contained_file_records']}
 d=load(VOC); led=load(REV/'afqr_r1b_unresolved_term_escalation_ledger.yaml')
 for obj in d['term_records']+d['collision_resolutions']+led['escalations']: assert set(obj['source_evidence_records'])<=ids
 assert all(p.is_file() for p in REQUIRED[4:9])
def test_alias_contract_direct_acyclic_and_owner_safe():
 d=load(VOC); aliases=d['alias_records']; names={a['alias'] for a in aliases}; canon={t['canonical_form']:t for t in d['term_records']}
 assert len(names)==len(aliases)
 for a in aliases:
  assert a['canonical_form'] in canon and a['canonical_form'] not in names
  assert a['owner_id']==canon[a['canonical_form']]['type_owner']['owner_id']
 # Direct aliases can only target term records, so cycles and alias chains are impossible.
def test_collision_status_and_required_escalation_coverage():
 d=load(VOC); allowed={'resolved_for_vocabulary','partially_resolved_with_escalation','escalated_unresolved'}; by={c['collision_id']:c for c in d['collision_resolutions']}; led=load(REV/'afqr_r1b_unresolved_term_escalation_ledger.yaml')['escalations']
 assert all(c['r1b_status'] in allowed for c in by.values())
 for cid in ('COLL-03','COLL-08','COLL-10'):
  assert by[cid]['r1b_status']!='resolved_for_vocabulary' and any(cid in e['collision_ids'] for e in led)
 escalated_terms={t for e in led for t in e['terms']}
 assert all(t['root_term'] in escalated_terms for t in d['term_records'] if t['vocabulary_disposition']=='escalated_unresolved')
def test_bounded_r1c_handoffs_and_gate_posture():
 d=load(VOC)
 assert d['next_gate']=='R1C' and set(['R2','R3','R4','R5','R6','RT-002G'])<=set(d['blocked_gates'])
 for t in d['term_records']:
  if t['r1c_handoff_required']: assert t['r1c_handoff_questions']
 forbidden=('runtime authority','conversion authority','canon authority','sourcebook authority','model authority','live-play authority')
 text=VOC.read_text().lower(); assert all(f'claims {x}' not in text for x in forbidden)
def test_no_production_imports_or_prohibited_diff_scope():
 needle='afqr_shared_vocabulary_and_type_owners'
 assert not any(needle in p.read_text(encoding='utf8',errors='ignore') for p in (ROOT/'src').rglob('*') if p.is_file())
 assert git('diff','--name-only',BASE,'--','*.zip').strip()==''
 assert git('diff','--name-only',BASE,'--','src/**').strip()==''
 assert all('\t-\t' not in line and not line.startswith('-\t') for line in git('diff','--numstat',BASE).splitlines())

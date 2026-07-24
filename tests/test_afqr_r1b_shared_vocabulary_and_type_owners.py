"""Semantic gates for the source-audited AFQR-01–20 R1B vocabulary contract."""
from __future__ import annotations
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VOC=ROOT/'docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml'
REV=ROOT/'docs/doctrine/reviews'; WORK=ROOT/'working/afqr_consolidation_inputs'
BASE='1855cb2460542c0f912a0830276c9cdea90f1b07'
REQUIRED=[VOC,REV/'afqr_r1b_vocabulary_resolution_report.md',REV/'afqr_r1b_unresolved_term_escalation_ledger.yaml',REV/'afqr_01_20_authority_status_index.yaml',REV/'afqr_01_20_dependency_matrix.yaml',REV/'afqr_01_20_shared_term_collision_inventory.md',REV/'afqr_01_20_consolidation_file_manifest.yaml',WORK/'manifest.yaml']
def load(p): return json.loads(p.read_text(encoding='utf8'))
def git(*args): return subprocess.run(['git',*args],cwd=ROOT,text=True,check=True,capture_output=True).stdout
def terms(): return {t['root_term']:t for t in load(VOC)['term_records']}
def manifest_records(): return {r['source_record_id']:r for r in load(WORK/'manifest.yaml')['contained_file_records']}

def test_required_files_exist_and_yaml_parses():
 assert all(p.is_file() for p in REQUIRED)
 assert all(isinstance(load(p),dict) for p in REQUIRED if p.suffix=='.yaml')
def test_exact_41_terms_and_ten_collisions():
 d=load(VOC); roots=[t['root_term'] for t in d['term_records']]; ids=[c['collision_id'] for c in d['collision_resolutions']]
 assert len(roots)==len(set(roots))==41 and roots.count('social state')==1
 assert ids==[f'COLL-{i:02d}' for i in range(1,11)] and len(ids)==len(set(ids))
def test_every_afqr_term_owner_has_evidence_from_that_afqr():
 records=manifest_records()
 for t in terms().values():
  assert t['owner_evidence_records'] and t['owner_evidence_paths'] and t['owner_evidence_rationale']
  assert all((ROOT/p).is_file() for p in t['owner_evidence_paths'])
  if t['type_owner']['owner_kind']=='afqr':
   owner=t['type_owner']['owner_id']; assert owner in {f'AFQR-{n:02d}' for n in range(1,21)}
   assert all(records[r]['detected_afqr_id']==owner and records[r]['selected_as_primary'] for r in t['owner_evidence_records'])
def test_every_qualified_form_has_direct_source_backed_owner_evidence():
 records=manifest_records()
 for t in terms().values():
  for q in t['qualified_forms']:
   assert q['definition'] and q['owner_id'] and q['owner_evidence_paths'] and q['owner_evidence_rationale']
   assert all((ROOT/p).is_file() for p in q['owner_evidence_paths'])
   if q['owner_kind']=='afqr':
    assert q['owner_evidence_records']
    assert all(records[r]['detected_afqr_id']==q['owner_id'] and records[r]['selected_as_primary'] for r in q['owner_evidence_records'])
   else: assert q['owner_kind']=='project_governance'
def test_mandatory_transaction_event_opportunity_dependency_corrections():
 t=terms()
 assert t['transaction']['type_owner']['owner_id']=='AFQR-01'
 assert not (t['event']['type_owner']['owner_kind']=='afqr' and t['event']['type_owner']['owner_id']=='AFQR-04')
 assert t['opportunity']['type_owner']['owner_id']=='AFQR-19' and 'AFQR-19' not in t['opportunity']['explicit_nonowners']
 assert t['dependency']['type_owner']['owner_id']=='AFQR-09' and 'AFQR-09' not in t['dependency']['explicit_nonowners']
 assert t['dependency']['type_owner']['owner_id']!='AFQR-05'
def test_observation_candidate_to_epistemic_record_handoff_is_preserved():
 q={x['qualified_form']:x['owner_id'] for x in terms()['observation']['qualified_forms']}
 assert terms()['observation']['unqualified_usage']=='qualified_only'
 assert q=={'sensing observation candidate':'AFQR-20','epistemic observation record':'AFQR-10'}
def test_evidence_three_way_ownership_is_preserved():
 e=terms()['evidence']; q={x['qualified_form']:x['owner_id'] for x in e['qualified_forms']}
 assert e['unqualified_usage']=='qualified_only'
 assert q=={'arbitration evidence':'AFQR-06','epistemic evidence record':'AFQR-10','sensing evidence candidate':'AFQR-20'}
def test_unsupported_owner_forms_absent_and_consumers_are_not_owners():
 t=terms(); owner_forms={q['qualified_form'] for q in t['owner']['qualified_forms']}
 assert not {'asset owner','identity owner'} & owner_forms
 assert t['opportunity']['type_owner']['owner_id']!='AFQR-03'
 assert t['dependency']['type_owner']['owner_id']!='AFQR-05'
 assert {q['qualified_form'] for q in t['event']['qualified_forms']}=={'committed event receipt','scheduled effect'}
def test_qualified_families_and_owner_nonowner_postures_are_consistent():
 for t in terms().values():
  if t['vocabulary_disposition']=='qualified_canonical_family':
   assert t['unqualified_usage']=='qualified_only' and t['qualified_forms']
  actual={q['owner_id'] for q in t['qualified_forms']}|{t['type_owner']['owner_id']}
  assert not actual & set(t['explicit_nonowners'])
def test_collision_escalations_aliases_and_r1c_only_gate():
 d=load(VOC); by={c['collision_id']:c for c in d['collision_resolutions']}
 led=load(REV/'afqr_r1b_unresolved_term_escalation_ledger.yaml')['escalations']
 for cid in ('COLL-03','COLL-08','COLL-10'):
  assert by[cid]['r1b_status'] in {'partially_resolved_with_escalation','escalated_unresolved'}
  assert any(cid in x['collision_ids'] for x in led)
 assert d['alias_records']==[] and d['next_gate']=='R1C'
 assert set(d['blocked_gates'])=={'R1D','R1E','R2','R3','R4','R5','R6','RT-002G'}
def test_no_production_zip_or_binary_diff():
 assert git('diff','--name-only',BASE,'--','*.zip').strip()==''
 assert git('diff','--name-only',BASE,'--','src/**').strip()==''
 assert all('-\t-' not in line for line in git('diff','--numstat',BASE).splitlines())

def test_state_qualified_semantic_owners_are_not_afqr01_commitment_ownership():
 state=terms()['state']; forms={q['qualified_form']:q for q in state['qualified_forms']}
 assert state['vocabulary_disposition']=='qualified_canonical_family'
 assert state['unqualified_usage']=='qualified_only'
 assert {name:q['owner_id'] for name,q in forms.items()}=={
  'epistemic state':'AFQR-10','social state':'AFQR-13','environmental state':'AFQR-17'}
 assert not {'AFQR-10','AFQR-17'} & set(state['explicit_nonowners'])
 assert 'domain state' not in forms
 assert all(q['owner_evidence_records'] and q['owner_evidence_paths'] and q['owner_evidence_rationale'] for q in forms.values())
 assert 'does not transfer semantic ownership to AFQR-01' in state['definition']

def test_all_definitions_match_dispositions_and_escalations():
 d=load(VOC); ledger_terms={term for e in load(REV/'afqr_r1b_unresolved_term_escalation_ledger.yaml')['escalations'] for term in e['terms']}
 for term in d['term_records']:
  if term['vocabulary_disposition']=='qualified_canonical_family':
   assert term['unqualified_usage']=='qualified_only' and term['qualified_forms']
  elif term['vocabulary_disposition']=='canonical_distinct_type':
   assert term['unqualified_usage']=='allowed' and not term['qualified_forms']
   assert 'a qualified family' not in term['definition'].lower()
  elif term['vocabulary_disposition']=='escalated_unresolved':
   assert term['root_term'] in ledger_terms

def test_integrity_time_and_report_metadata_are_consistent():
 t=terms(); report=(REV/'afqr_r1b_vocabulary_resolution_report.md').read_text(encoding='utf8')
 assert t['integrity']['vocabulary_disposition']=='canonical_distinct_type'
 assert t['integrity']['type_owner']['owner_id']=='AFQR-16' and not t['integrity']['qualified_forms']
 assert 'structural-integrity concern' in t['integrity']['definition'] and 'qualified family' not in t['integrity']['definition'].lower()
 assert t['time']['vocabulary_disposition']=='canonical_distinct_type'
 assert t['time']['type_owner']['owner_id']=='AFQR-04' and not t['time']['qualified_forms']
 assert 'semantic/logical-time framework' in t['time']['definition'] and 'qualified family' not in t['time']['definition'].lower()
 for phrase in ('epistemic state','social state','environmental state','AFQR-16 `integrity`','AFQR-04 `time`'):
  assert phrase in report

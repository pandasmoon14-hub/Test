"""Semantic contract tests for bounded AFQR-10–15 R1D-AGENCY doctrine."""
import json, pathlib, re, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE='5c346a0ebd192879abaed0099f5644589df97884'
DOC=ROOT/'docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md'
R1B=ROOT/'docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml'
R1C=ROOT/'docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml'
CORE_DOC=ROOT/'docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md'
AUTH=ROOT/'docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml'
A={f'AFQR-{n:02}' for n in range(10,16)}; C={f'AFQR-{n:02}' for n in range(1,10)}; W={f'AFQR-{n:02}' for n in range(16,21)}
def load(p): return json.loads(p.read_text(encoding='utf8'))
def fenced(p): return json.loads(re.search(r'```json\n(.*?)\n```',p.read_text(encoding='utf8'),re.S).group(1))
def contract(): return fenced(DOC)
def test_structure_responsibilities_and_direct_sources():
 c=contract(); assert {r['afqr_id'] for r in c['responsibility_records']}==A; assert len(c['responsibility_records'])==6
 expected={'AFQR-10':'SRC-0022','AFQR-11':'SRC-0041','AFQR-12':'SRC-0072','AFQR-13':'SRC-0082','AFQR-14':'SRC-0103','AFQR-15':'SRC-0125'}
 valid={i for r in load(AUTH)['afqr_records'] for i in r['source_evidence_records']}
 for r in c['responsibility_records']:
  assert r['source_evidence_identifiers']==[expected[r['afqr_id']]]; assert set(r['source_evidence_identifiers'])<=valid
  assert all((ROOT/p).is_file() for p in r['source_paths']); assert r['owned_concerns'] and r['explicit_nonowned_concerns']
 assert set(c['excluded_internal_ownership'])==C|W

def test_exact_r1b_forms_and_owners_without_root_invention():
 v=load(R1B); terms={t['term_id']:t for t in v['term_records']}
 for r in contract()['responsibility_records']:
  for x in r['r1b_terms_or_qualified_forms']:
   t=terms[x['term_id']]; candidates={(t['canonical_form'],t['type_owner']['owner_id'])} if t['type_owner']['owner_kind']=='afqr' else set()
   candidates|={(q['qualified_form'],q['owner_id']) for q in t.get('qualified_forms',[]) if q['owner_kind']=='afqr'}
   assert (x['form'],x['owner']) in candidates
   if t['unqualified_usage']=='qualified_only': assert x['form'] in {q['qualified_form'] for q in t['qualified_forms']}

def test_exact_internal_and_all_boundary_r1c_semantics():
 c=contract(); edges=load(R1C)['dependency_edge_dispositions']; by={e['edge_id']:e for e in edges}
 ei={e['edge_id'] for e in edges if e['producer_afqr'] in A and e['consumer_afqr'] in A}
 eb={e['edge_id'] for e in edges if (e['producer_afqr'] in A)^(e['consumer_afqr'] in A)}
 assert len(ei)==len(c['internal_edge_dispositions'])==11; assert len(eb)==len(c['boundary_dispositions'])==26
 assert {d['edge_id'] for d in c['internal_edge_dispositions']}==ei; assert {d['edge_id'] for d in c['boundary_dispositions']}==eb
 for d in c['internal_edge_dispositions']+c['boundary_dispositions']:
  e=by[d['edge_id']]
  assert (d['producer'],d['consumer'],d['handoff_kind'])==(e['producer_afqr'],e['consumer_afqr'],e['relation_or_handoff_kind'])
  assert d['semantic_owner']==e['semantic_type_owner']; assert d['producer_output']==e['producer_supplies']; assert d['permitted_consumer_use']==e['consumer_may_use']
  assert d['ownership_nontransfer']==e['ownership_does_not_transfer']; assert d['preconditions']==e['preconditions']; assert d['unavailable_input_behavior']==e['unavailable_input_behavior']
  assert d['source_evidence']=={'identifiers':e['source_evidence_records'],'paths':e['source_evidence_paths']}; assert d['cycle_or_dependency_risk_status']==e['cycle_participation']
 assert all(d['external_family']=='R1D-WORLD' for d in c['boundary_dispositions'] if d['external_endpoint'] in W)
 assert c['internal_cycle_statement'].startswith('No internal')

def test_core_parity_is_exact_not_asserted_only():
 c=contract(); core=fenced(CORE_DOC); core_by={d['r1c_edge_ids_covered'][0]:d for d in core['boundary_dispositions']}
 agency={d['edge_id']:d for d in c['boundary_dispositions'] if d['external_endpoint'] in C}
 assert len(agency)==len(c['core_boundary_parity_records'])==21
 for eid,d in agency.items():
  x=core_by[eid]
  assert (d['producer'],d['consumer'],d['handoff_kind'])==(x['producer'],x['consumer'],x['handoff_kind'])
  assert d['typed_producer_output']==x['typed_producer_output']; assert d['semantic_owner']==x['semantic_owner']; assert d['ownership_nontransfer']==x['ownership_nontransfer']; assert d['failure_behavior']==x['failure_behavior']; assert d['source_evidence']==x['source_evidence']

def test_afqr14_provenance_collisions_and_substrates():
 c=contract(); p=c['afqr14_validation_provenance']; assert p['architecture_owner']=='AFQR-14' and p['validation_packaging']=='AFQR-15 archive'; assert 'neither transfers ownership' in p['rule']
 specs={'COLL-03':({'identity','owner','authority','agency','responsibility'},{'AFQR-01','AFQR-08','AFQR-11','AFQR-15'}),'COLL-08':({'jurisdiction','institution','authority','social state'},{'AFQR-09','AFQR-13','AFQR-15'}),'COLL-10':({'motivation','behavior','agency','responsibility','social state'},{'AFQR-11','AFQR-12','AFQR-13'})}
 actual={x['collision_id']:x for x in c['collision_resolution_candidates']}; assert set(actual)==set(specs)
 for cid,(terms,afqrs) in specs.items(): assert set(actual[cid]['exact_terms'])==terms and set(actual[cid]['exact_affected_afqrs'])==afqrs and actual[cid]['status']=='candidate_pending_R1E'
 subs={x['substrate_id']:x for x in c['missing_substrate_dispositions']}; assert set(subs)=={'SUB-001','SUB-002','SUB-005'}
 assert all({'core_family_scope','agency_family_scope','world_family_scope'}<=set(x) for x in subs.values()); assert 'AFQR-20' in subs['SUB-002']['world_family_scope']

def test_required_inferences_pressure_and_gates():
 c=contract(); rules={x['rule'] for x in c['family_invariants']}
 required={'evidence admission is not truth','sensing is not knowledge','identity is not personhood','control is not consent','motivation is not agency','behavior is not responsibility','social status is not institutional authority','jurisdiction is not reachability','communication is not truth','persuasion is not consent','adjudication is not enforcement execution'}
 assert required<=rules; assert len(c['corpus_pressure_records'])==18; assert all(x['lawful_outcomes'] and x['universalization']=='prohibited' and not x['conversion_performed'] for x in c['corpus_pressure_records'])
 assert c['completion_boundary']=={'R1D-CORE':'complete','R1D-AGENCY':'complete','overall_R1D':'incomplete','R1D-WORLD':'ready_not_started','R1E':'blocked','R2-R6':'blocked','RT-002G':'unauthorized','temporary_evidence_deletion':'unauthorized'}
 assert c['r1e_handoff']['global_escalations'].endswith('remain open pending R1E')

def test_registry_manifest_and_committed_scope():
 reg=(ROOT/'docs/doctrine/astra_doctrine_registry_v0_1.yaml').read_text(); assert 'AFQR-10-15-R1D-AGENCY-EPISTEMIC-SOCIAL-COMMUNICATION-001' in reg; assert 'status: pressure-tested\n  layer: 0_control\n  phase: R1D-AGENCY' in reg
 man=load(ROOT/'docs/doctrine/reviews/afqr_01_20_consolidation_file_manifest.yaml'); rec=next(x for x in man['planned_files'] if x['file_id']=='R1D-AGENCY'); assert rec['status']=='complete'
 changed=subprocess.check_output(['git','diff','--name-only',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines(); nums=subprocess.check_output(['git','diff','--numstat',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines(); deleted=subprocess.check_output(['git','diff','--name-status','--diff-filter=D',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines()
 assert not any(p.startswith('src/') or p.lower().endswith('.zip') or 'afqr_world_action_sensing' in p or 'formal_completion_review' in p for p in changed); assert not any(x.startswith('-\t-\t') for x in nums); assert not deleted
 assert not any('working/afqr_consolidation_inputs' in p for p in changed)

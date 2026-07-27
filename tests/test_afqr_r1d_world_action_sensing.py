"""Semantic contract tests for bounded AFQR-16–20 R1D-WORLD doctrine."""
import json, pathlib, re, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]; BASE='9cb7d36f6405fdf12a7b9bbe7edcf5839cdebc78'
DOC=ROOT/'docs/doctrine/consolidation/afqr_world_action_sensing.md'
def load(p): return json.loads(p.read_text(encoding='utf8'))
def fenced(p): return json.loads(re.search(r'```json\n(.*?)\n```',p.read_text(encoding='utf8'),re.S).group(1))
def contract(): return fenced(DOC)
W={f'AFQR-{i:02}' for i in range(16,21)}; C={f'AFQR-{i:02}' for i in range(1,10)}; A={f'AFQR-{i:02}' for i in range(10,16)}
R1B=ROOT/'docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml';R1C=ROOT/'docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml'
def test_responsibilities_authority_and_primary_sources():
 c=contract(); rs=c['responsibility_records']; assert len(rs)==5 and {x['afqr_id'] for x in rs}==W; assert set(c['excluded_internal_ownership'])==C|A
 auth={x['afqr_id']:x for x in load(ROOT/'docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml')['afqr_records']}
 expected={'AFQR-16':'SRC-0152','AFQR-17':'SRC-0180','AFQR-18':'SRC-0207','AFQR-19':'SRC-0231','AFQR-20':'SRC-0255'}
 for x in rs:
  u=auth[x['afqr_id']]; assert x['selected_architecture']==u['selected_architecture'];assert x['source_evidence_identifiers']==[expected[x['afqr_id']]];assert x['source_paths']==u['source_packet_paths'];assert all((ROOT/p).is_file() for p in x['source_paths']);assert x['owned_concerns'] and x['explicit_nonowned_concerns'] and x['unresolved_seams'] and x['donor_pressure_risks']
def test_r1b_exact_forms_and_owners():
 terms={x['term_id']:x for x in load(R1B)['term_records']}
 for r in contract()['responsibility_records']:
  for x in r['r1b_terms_or_qualified_forms']:
   t=terms[x['term_id']]; valid=set()
   if t['type_owner']['owner_kind']=='afqr': valid.add((t['canonical_form'],t['type_owner']['owner_id']))
   valid|={(q['qualified_form'],q['owner_id']) for q in t.get('qualified_forms',[]) if q['owner_kind']=='afqr'}
   assert (x['form'],x['owner']) in valid and x['owner']==r['afqr_id']
   assert x['owner'] not in t['type_owner'].get('explicit_nonowners',[])
def test_all_exact_r1c_edges_and_fields():
 c=contract(); es=load(R1C)['dependency_edge_dispositions'];by={e['edge_id']:e for e in es}
 sets=[({e['edge_id'] for e in es if e['producer_afqr'] in W and e['consumer_afqr'] in W},c['internal_edge_dispositions'],7),({e['edge_id'] for e in es if ((e['producer_afqr'] in W)^(e['consumer_afqr'] in W)) and {e['producer_afqr'],e['consumer_afqr']}&C},c['core_boundary_dispositions'],17),({e['edge_id'] for e in es if ((e['producer_afqr'] in W)^(e['consumer_afqr'] in W)) and {e['producer_afqr'],e['consumer_afqr']}&A},c['agency_boundary_dispositions'],5)]
 fields={'r1c_status':'r1c_status','semantic_owner':'semantic_type_owner','producer_output':'producer_supplies','permitted_consumer_use':'consumer_may_use','ownership_nontransfer':'ownership_does_not_transfer','consumer_nonownership':'consumer_not_semantic_owner_by_consumption','preconditions':'preconditions','postconditions':'postconditions','unavailable_input_behavior':'unavailable_input_behavior','revocation_invalidation_or_cascade':'revocation_invalidation_or_cascade','hidden_information_and_projection_constraints':'hidden_information_or_projection_constraints','cycle_participation':'cycle_participation'}
 allrows=[]
 for expected,rows,n in sets:
  assert len(rows)==n and {x['edge_id'] for x in rows}==expected;allrows+=rows
 for d in allrows:
  e=by[d['edge_id']];assert (d['producer'],d['consumer'],d['handoff_kind'])==(e['producer_afqr'],e['consumer_afqr'],e['relation_or_handoff_kind'])
  for a,b in fields.items(): assert d[a]==e[b]
  assert d['source_evidence']=={'identifiers':e['source_evidence_records'],'paths':e['source_evidence_paths']}
def test_predecessor_parity_field_by_field():
 c=contract(); core=fenced(ROOT/'docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md'); agency=fenced(ROOT/'docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md')
 cb={x['r1c_edge_ids_covered'][0]:x for x in core['boundary_dispositions']};ab={x['edge_id']:x for x in agency['boundary_dispositions']}
 fields=['producer','consumer','handoff_kind','typed_producer_output','semantic_owner','ownership_nontransfer','failure_behavior','source_evidence']
 assert len(c['r1d_core_parity_records'])==17 and len(c['r1d_agency_parity_records'])==5
 for rows,up in [(c['r1d_core_parity_records'],cb),(c['r1d_agency_parity_records'],ab)]:
  for x in rows:
   assert x['parity_result']=='exact'; assert all(x[k]==up[x['edge_id']][k] for k in fields)
def test_cycle_004_and_dep_094_are_exact():
 c=contract();r=load(R1C);cy=next(x for x in r['cycle_risk_resolutions'] if x['cycle_id']=='CYCLE-004');assert c['cycle_004_treatment']==cy;assert cy['edge_ids']==['DEP-089','DEP-091']
 e=next(x for x in r['dependency_edge_dispositions'] if x['edge_id']=='DEP-094');d=c['dep_094_special_treatment'];assert d['producer']=='AFQR-20' and d['consumer']=='AFQR-19' and d['handoff_kind']=='contact_targeting';assert d['semantic_owner']==e['semantic_type_owner'];assert d['producer_output']==e['producer_supplies'];assert d['postconditions']==e['postconditions'];assert d['unavailable_input_behavior']==e['unavailable_input_behavior'];assert e['semantic_type_owner']['owner_id']=='AFQR-19'
def test_invariants_collisions_escalations_and_substrates():
 c=contract(); inv={x['invariant_id'] for x in load(R1C)['cross_afqr_invariants']};rules={x['rule'] for x in c['family_invariants']};required={'embodiment is not identity','environment is not topology','environmental process is not logical time','reachability is not jurisdiction, opportunity, or target','capability is not opportunity and target is not resolution','detection is not target and observation candidate is not epistemic observation record','signal is not communication or interpretation','exposure is not harm','resolution is not transition commitment'};assert required<=rules
 assert len({tuple(x['r1c_invariant_ids']) for x in c['family_invariants']})>1
 for x in c['family_invariants']: assert x['provenance_kind']=='r1c_derived' and x['r1c_invariant_ids'] and set(x['r1c_invariant_ids'])<=inv and x['source_evidence_identifiers']
 rb={x['collision_id']:x for x in load(R1B)['collision_resolutions']};assert {x['collision_id'] for x in c['resolved_collision_boundary_records']}=={'COLL-01','COLL-02','COLL-04','COLL-05','COLL-06','COLL-07','COLL-08','COLL-09'}
 for x in c['resolved_collision_boundary_records']: assert x['r1b_status']==rb[x['collision_id']]['r1b_status'] and x['exact_owner_assignments']==rb[x['collision_id']]['term_owner_assignments'] and x['qualification_rules']==rb[x['collision_id']]['qualification_rules']
 assert c['preserved_open_escalations']=={'collision_ids':['COLL-03','COLL-08','COLL-10'],'status':'globally open pending independent R1E','new_world_candidates':[],'coll_08_affected_afqrs_not_modified':True}
 ups={x['substrate_id']:x for x in load(R1C)['missing_substrate_classifications']};subs={x['substrate_id']:x for x in c['missing_substrate_dispositions']};assert set(subs)=={'SUB-002','SUB-005'}
 for sid,x in subs.items(): assert x['exact_substrate_name']==ups[sid]['name'] and x['exact_requiring_afqrs']==ups[sid]['requiring_afqrs'] and x['exact_future_owner_posture']==ups[sid]['future_doctrine_owner'] and 'no combined' in x['combined_owner_prohibition']
def test_pressure_gates_registry_manifest_and_scope():
 c=contract();ps=c['corpus_pressure_records'];assert len(ps)==18==len({x['pressure_class'] for x in ps});assert len({json.dumps({k:v for k,v in x.items() if k!='record_id'},sort_keys=True) for x in ps})==18
 for x in ps: assert set(x['world_landing_afqrs'])<=W and set(x['core_family_handoff_afqrs'])<=C and set(x['agency_family_handoff_afqrs'])<=A and x['source_local_constructs'] and x['quarantine_triggers'] and x['escalation_triggers'] and x['prohibited_universalizations']
 assert c['completion_boundary']=={'R1D-CORE':'complete','R1D-AGENCY':'complete','R1D-WORLD':'complete','overall_R1D':'complete','overall_R1':'incomplete_pending_R1E','R1E':'ready','R2-R6':'blocked','RT-002G':'unauthorized','temporary_evidence_deletion':'unauthorized'}
 man={x['file_id']:x['status'] for x in load(ROOT/'docs/doctrine/reviews/afqr_01_20_consolidation_file_manifest.yaml')['planned_files']};assert man['R1D-CORE']==man['R1D-AGENCY']==man['R1D-WORLD']=='complete' and man['R1E']=='ready'
 reg=(ROOT/'docs/doctrine/astra_doctrine_registry_v0_1.yaml').read_text();assert 'AFQR-16-20-R1D-WORLD-ACTION-SENSING-001' in reg and 'status: pressure-tested\n  layer: 0_control\n  phase: R1D-WORLD' in reg
 changed=subprocess.check_output(['git','diff','--name-only',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines();nums=subprocess.check_output(['git','diff','--numstat',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines();deleted=subprocess.check_output(['git','diff','--name-status','--diff-filter=D',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines()
 allowed={'docs/decisions/current_decisions_log.md','docs/doctrine/astra_doctrine_registry_v0_1.yaml','docs/doctrine/consolidation/afqr_world_action_sensing.md','docs/doctrine/control/afqr_01_20_consolidation_program_plan.md','docs/doctrine/reviews/afqr_01_20_consolidation_file_manifest.yaml','docs/doctrine/reviews/afqr_r1d_world_consolidation_report.md','tests/test_afqr_r1d_world_action_sensing.py','tests/test_afqr_r1d_core_transaction_identity_relation.py','tests/test_afqr_r1d_agency_epistemic_social_communication.py'}
 assert set(changed)<=allowed and not any(p.startswith('src/') or p.lower().endswith('.zip') or 'formal_completion_review' in p for p in changed);assert not any(x.startswith('-\t-\t') for x in nums);assert not deleted;assert not any('working/afqr_consolidation_inputs' in p for p in changed)

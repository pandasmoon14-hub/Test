"""Exact semantic checks for AFQR-01–20 R1E formal completion."""
from __future__ import annotations
import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE='017984a1598b9c60324c62e54d80372c364654ae'
REVIEW='docs/doctrine/reviews/afqr_01_20_formal_completion_review.md'
def load(p): return json.loads((ROOT/p).read_text())
def md(p): return json.loads(re.search(r'```json\n(.*?)\n```',(ROOT/p).read_text(),re.S).group(1))
def sha(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def C(): return md(REVIEW)
IDX='docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml';MAN='working/afqr_consolidation_inputs/manifest.yaml';VOC='docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml';GRAPH='docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml'
F={'core':'docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md','agency':'docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md','world':'docs/doctrine/consolidation/afqr_world_action_sensing.md'}
BLED='docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml';CLED='docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml'
def manifest_maps():
 m=load(MAN);a={x['archive_record_id']:x for x in m['archive_records']};rows={x['source_record_id']:x for x in m['contained_file_records']};return m,a,rows
def check_locator(loc):
 _,archives,rows=manifest_maps();x=rows[loc['evidence_id']]
 if x['normalized_path']:
  p=x['normalized_path'];p=p if p.startswith('working/') else 'working/afqr_consolidation_inputs/'+p
  assert loc=={'evidence_id':x['source_record_id'],'path':p,'path_kind':'materialized_normalized_file'};assert (ROOT/p).is_file()
 else:
  a=archives[x['parent_archive_record_id']];assert loc['path']==a['current_path']+'::'+x['original_archive_path'];assert loc['archive_path']==a['current_path'];assert loc['archive_member_path']==x['original_archive_path'];assert (ROOT/a['current_path']).is_file()
def test_result_baseline_and_fail_capability():
 c=C();assert (c['review_id'],c['phase'],c['result'],c['r1_status'])==('AFQR-01-20-R1E-FORMAL-COMPLETION-001','R1E','pass','complete');assert c['blocking_defects']==c['unresolved_defects']==[];assert 'fail' in (ROOT/REVIEW).read_text().split('```json',1)[0];assert c['next_lawful_gate']=='R2 — doctrine-drift resolution';assert c['downstream_gate_states']=={'R2':'ready','R3':'blocked','R4':'blocked','R5':'blocked','R6':'blocked','RT-002G':'unauthorized'}
def test_r1a_all_exact_and_afqr14():
 c=C();rows={x['afqr_id']:x for x in c['r1a_completeness']['records']};idx={x['afqr_id']:x for x in load(IDX)['afqr_records']};assert set(rows)==set(idx)=={f'AFQR-{n:02}' for n in range(1,21)};assert len(c['r1a_completeness']['records'])==20
 for aid,x in rows.items():
  u=idx[aid];assert x['selected_architecture']==u['selected_architecture'];assert x['authoritative_title']==u['full_title'];assert x['decision_status']==u['decision_status'];assert x['source_evidence_identifiers']==u['source_evidence_records'];assert x['source_packet_paths']==u['source_packet_paths'];assert x['title_evidence']==u['title_evidence_records'];assert x['corrected_baseline_evidence']==u['corrected_baseline_evidence_records'];assert x['duplicate_authority_status']=='none_unresolved';assert not x['mismatches'];[check_locator(z) for z in x['source_evidence_locators']+x['title_evidence_locators']+x['corrected_baseline_evidence_locators']];assert all((ROOT/p).is_file() for p in x['source_packet_paths'])
 a=c['r1a_completeness']['afqr_14_provenance'];assert a=={'architecture_owner':'AFQR-14','primary_source':'SRC-0103','title_evidence':['SRC-0114'],'corrected_baseline_evidence':['SRC-0103','SRC-0139','SRC-0121'],'packaging_rule':'AFQR-15 packaging validates AFQR-14 files and does not transfer ownership'}
def test_r1b_exact_term_by_term():
 c=C();up=load(VOC)['term_records'];rows=c['r1b_completeness']['review_records'];assert len(rows)==len(up)==41;assert len({x['term_id'] for x in rows})==41
 for x,u in zip(rows,up):
  assert x['term_id']==u['term_id'] and x['normalized_root']==u['root_term'] and x['canonical_form']==u['canonical_form'];assert (x['owner_kind'],x['owner_id'])==(u['type_owner']['owner_kind'],u['type_owner']['owner_id']);assert x['qualified_forms']==u['qualified_forms'];assert x['explicit_nonowners']==u['explicit_nonowners'];assert x['handoff_only_uses']==u['handoff_only_consumers'];assert x['rejected_aliases']==u['disallowed_aliases'];assert x['explicit_non_equivalences']==u['explicit_non_equivalences'];assert x['source_evidence']==u['source_evidence_records'];assert x['collision_membership']==u['collision_ids'];assert x['authoritative_record_sha256']==sha(u);assert x['result']=='pass' and x['mismatch_list']==[]
  if u['unqualified_usage']=='qualified_only': assert u['type_owner']['owner_kind']!='afqr'
 assert c['r1b_completeness']['new_unqualified_owners']==[]

def projection_checks(edge,record):
 maps=[('producer_afqr','producer'),('consumer_afqr','consumer'),('relation_or_handoff_kind','handoff_kind'),('semantic_type_owner','semantic_owner'),('producer_supplies','producer_output'),('consumer_may_use','permitted_consumer_use'),('ownership_does_not_transfer','ownership_nontransfer'),('unavailable_input_behavior','unavailable_input_behavior'),('unavailable_input_behavior','failure_or_unavailable_input_behavior'),('unavailable_input_behavior','failure_behavior'),('source_evidence_records','source_evidence'),('r1d_destination_family_or_escalation','downstream_implementation_status')]
 out=[]
 for uk,rk in maps:
  if rk not in record:continue
  rv,uv=record[rk],edge[uk];mode='exact' if rk in {'producer','consumer','handoff_kind','semantic_owner','ownership_nontransfer','source_evidence'} else 'bounded_projection';match=((rv.get('identifiers') if isinstance(rv,dict) and rk=='source_evidence' else rv)==uv) if mode=='exact' else bool(rv);out.append({'r1c_field':uk,'r1d_field':rk,'comparison_mode':mode,'r1c_value_sha256':sha(uv),'r1d_value_sha256':sha(rv),'match':match})
 return out

def projections():
 fam={k:md(v) for k,v in F.items()};out={}
 def add(n,seq):
  for x in seq:
   for eid in x.get('r1c_edge_ids_covered') or [x.get('edge_id')]:
    if eid:out.setdefault(eid,[]).append((n,x))
 add('core',fam['core']['internal_edge_dispositions']);add('core',fam['core']['boundary_dispositions']);add('agency',fam['agency']['internal_edge_dispositions']);add('agency',fam['agency']['boundary_dispositions']);add('world',fam['world']['internal_edge_dispositions']);add('world',fam['world']['core_boundary_dispositions']);add('world',fam['world']['agency_boundary_dispositions']);return out
def test_all_r1c_edge_hashes_fields_and_r1d_projections():
 c=C();up={x['edge_id']:x for x in load(GRAPH)['dependency_edge_dispositions']};rows={x['edge_id']:x for x in c['r1c_completeness']['edge_reviews']};pj=projections();assert set(rows)==set(up) and len(rows)==94
 required={'relation_or_handoff_kind','semantic_type_owner','semantic_type_owner.r1b_term_bindings','producer_supplies','consumer_may_use','ownership_does_not_transfer','consumer_not_semantic_owner_by_consumption','preconditions','postconditions','unavailable_input_behavior','revocation_invalidation_or_cascade','hidden_information_or_projection_constraints','source_evidence_records','source_evidence_paths','cycle_participation','r1d_destination_family_or_escalation'}
 for eid,x in rows.items():
  u=up[eid];assert x['producer']==u['producer_afqr'] and x['consumer']==u['consumer_afqr'];assert x['authoritative_r1c_record_sha256']==sha(u);assert required<=set(x['compared_fields']);assert x['mismatch_list']==[] and x['result']=='pass';assert len(pj[eid])==x['projection_count_expected']==len(x['applicable_r1d_projection_records'])
  got={(z['family'],z['record_sha256']) for z in x['applicable_r1d_projection_records']};assert got=={(n,sha(r)) for n,r in pj[eid]};assert all(z['field_comparison_result']=='pass' and not z['field_mismatch_list'] for z in x['applicable_r1d_projection_records']);assert all(z['established_field_comparison_sha256']==sha(projection_checks(u,r)) and all(q['match'] for q in projection_checks(u,r)) for z,(n,r) in zip(x['applicable_r1d_projection_records'],pj[eid]))
  for n,r in pj[eid]:
   assert (r.get('producer') or u['producer_afqr'])==u['producer_afqr'];assert (r.get('consumer') or u['consumer_afqr'])==u['consumer_afqr'];assert (r.get('handoff_kind') or r.get('typed_handoff'))==u['relation_or_handoff_kind'];assert r['semantic_owner']==u['semantic_type_owner']
 assert c['r1c_completeness']['partition_counts']=={'core_internal':33,'agency_internal':11,'world_internal':7,'core_agency_boundary':21,'core_world_boundary':17,'agency_world_boundary':5}
def test_cycles_risks_exact_not_id_only():
 c=C();g=load(GRAPH);cy={x['cycle_id']:x for x in g['cycle_risk_resolutions']};rr={x['reclassification_id']:x for x in g['cycle_risk_reclassifications']}
 for x in c['cycle_decisions']:
  u=cy[x['cycle_id']];assert x['authoritative_record']==u and x['authoritative_record_sha256']==sha(u);assert x['exact_edge_ids']==u['edge_ids'];assert x['exact_directions']==u['actual_dependency_directions'];assert x['classification']==u['resolution'];assert x['breaker_or_phase_rule']==u['breaker'];assert x['r1d_treatments'] and not x['mismatches']
 for x in c['dependency_risk_decisions']:
  u=rr[x['risk_id']];assert x['authoritative_record']==u and x['authoritative_record_sha256']==sha(u);assert x['exact_edge_ids']==u['edge_ids'];assert x['classification']==u['classification'];assert x['breaker_or_phase_rule']==u['reason'];assert x['r1d_treatments'] and not x['mismatches']
def test_substrates_exact_and_ledger_reconciled():
 c=C();g={x['substrate_id']:x for x in load(GRAPH)['missing_substrate_classifications']};led={x['escalation_id'].removesuffix('-ESC'):x for x in load(CLED)['escalations'] if 'substrate' in x};rows={x['substrate_id']:x for x in c['missing_substrate_decisions']};assert set(rows)==set(g)==set(led)=={f'SUB-{n:03}' for n in range(1,6)}
 for sid,x in rows.items():
  u,l=g[sid],led[sid];assert x['authoritative_r1c_record']==u and x['authoritative_r1c_record_sha256']==sha(u);assert x['decision']=='accepted_as_classified_deferred_substrate';assert l['status']==x['ledger_status']=='accepted_deferred_by_r1e';assert l['r1e_substrate_decision_id']==x['decision_id'];assert l['exact_requiring_afqrs']==u['requiring_afqrs'];assert l['exact_evidence_identifiers']==u['source_evidence_records'];assert l['exact_source_paths']==u['source_evidence_paths'];assert l['implementation_status']=='unimplemented' and l['combined_owner_prohibition'];assert l['historical_pre_r1e_blocking_effect']==l['blocking_effect'];assert l['current_post_r1e_blocking_effect']==x['current_post_r1e_blocking_effect'];assert 'does not block R1 completion or R2 doctrine-drift review' in l['current_post_r1e_blocking_effect'];[check_locator(z) for z in x['evidence_locators']]
 assert not any(x['status']=='open' and 'final R1' in x.get('blocking_effect','') for x in led.values())
def test_collisions_both_ledgers_evidence_paths_and_pressure_cases():
 c=C();ds={x['collision_id']:x for x in c['global_escalations']};b={x['collision_ids'][0]:x for x in load(BLED)['escalations']};r={x['collision_id']:x for x in load(CLED)['escalations'] if 'collision_id' in x};cand={x['collision_id']:x for x in md(F['agency'])['collision_resolution_candidates']};assert set(ds)==set(b)==set(r)=={'COLL-03','COLL-08','COLL-10'}
 minimum={'COLL-03':13,'COLL-08':10,'COLL-10':14}
 for cid,d in ds.items():
  assert d['terms']==b[cid]['terms'];assert d['affected_afqrs']==b[cid]['affected_afqrs'];assert d['r1b_owner_candidates']==b[cid]['current_owner_candidates'];assert d['r1b_evidence_records']==b[cid]['source_evidence_records'];assert d['r1d_candidate_record']['record_sha256']==sha(cand[cid]);assert d['r1d_candidate_record']['exact_fields']==cand[cid];assert len(d['corpus_scale_pressure_test'])>=minimum[cid];assert len(d['alternatives_considered'])==3 and all(x['rejection_reason'] for x in d['alternatives_considered']) and d['lawful_qualified_forms'] and all({'root_term','qualified_form','owner_kind','owner_id'}<=set(x) for x in d['lawful_qualified_forms']) and d['prohibited_inferences'] and d['handoff_rules'] and d['residual_r2_questions']
  assert b[cid]['r1e_decision_id']==r[cid]['r1e_decision_id']==d['decision_id'];assert b[cid]['resolution_evidence']==r[cid]['resolution_evidence'];assert b[cid]['resolution_summary']==r[cid]['resolution_summary']==d['final_attribution_rule'];assert b[cid]['collision_specific_prohibited_inferences']==r[cid]['collision_specific_prohibited_inferences']==d['prohibited_inferences'];assert b[cid]['formal_review_path']==r[cid]['formal_review_path']==REVIEW
  bundle=r[cid]['resolution_evidence'];assert bundle['r1b_evidence_identifiers'] and bundle['r1c_invariant_ids'] and bundle['r1c_dependency_edge_ids'] and bundle['primary_evidence_identifiers'];[check_locator(z) for z in bundle['r1b_evidence_locators']+bundle['primary_evidence_locators']+d['r1c_evidence']['evidence_locators']]
 assert len({b[x]['resolution_summary'] for x in b})==3;assert len({sha(d['alternatives_considered']) for d in ds.values()})==3;assert all(len({x['disposition'] for x in d['corpus_scale_pressure_test']})==len(d['corpus_scale_pressure_test']) for d in ds.values())
def test_r1d_calculated_parity_every_edge():
 c=C();rows={x['edge_id']:x for x in c['r1d_completeness']['projection_review_records']};pj=projections();assert set(rows)==set(pj) and len(rows)==94
 for eid,x in rows.items():assert x['result']=='pass' and not x['mismatch_list'] and x['expected_projection_count']==len(pj[eid]);assert {(z['family'],z['record_sha256']) for z in x['projections']}=={(n,sha(r)) for n,r in pj[eid]}
def test_consistency_matrix_hashes_are_calculated():
 c=C();m=c['cross_artifact_consistency_matrix'];assert len(m)==13
 source={'R1A':load(IDX)['afqr_records'],'R1B':load(VOC)['term_records'],'R1C':load(GRAPH)['dependency_edge_dispositions'],'R1D-CORE':md(F['core'])['internal_edge_dispositions']+md(F['core'])['boundary_dispositions'],'R1D-AGENCY':md(F['agency'])['internal_edge_dispositions']+md(F['agency'])['boundary_dispositions'],'R1D-WORLD':md(F['world'])['internal_edge_dispositions']+md(F['world'])['core_boundary_dispositions']+md(F['world'])['agency_boundary_dispositions']}
 for x in m:
  for side,key in [('producer_artifact','producer_sha256'),('consumer_artifact','consumer_sha256')]:
   name=x[side]
   if name in source: assert x['normalized_record_set_hashes'][key]==sha(source[name]);assert x['exact_record_counts']['producer' if side=='producer_artifact' else 'consumer']==len(source[name])
  assert x['comparison_rules'] and x['evidence_paths'] and x['authority_transfer_tests'];assert x['missing_ids']==x['surplus_ids']==x['mismatched_ids_and_fields']==[] and x['result']=='pass'
def test_corpus_matrix_is_differentiated_and_source_bound():
 rows=C()['corpus_scale_adequacy_matrix'];assert len(rows)==18 and len({x['donor_family'] for x in rows})==18;assert len({sha(x['representative_construct_pressures']) for x in rows})>12;assert len({x['rationale'] for x in rows})==18
 for x in rows:
  assert x['representative_construct_pressures'] and x['lawful_astra_owner_afqrs'];assert x['direct_mapping_examples'] or x['normalized_mapping_examples'] or x['source_local_examples'];assert x['quarantine_triggers'] and x['doctrine_escalation_triggers'] and x['prohibited_universalizations'];assert len(x['source_r1d_pressure_records'])==3 and not x['blocking_defects']
  for z in x['source_r1d_pressure_records']:
   d=md(z['path']);seq=d['corpus_pressure_records'];record=next(y for y in seq if y['record_id']==z['record_id']);assert z['record_sha256']==sha(record)
def test_tracking_and_exact_committed_diff_containment():
 plan=(ROOT/'docs/doctrine/control/afqr_01_20_consolidation_program_plan.md').read_text();assert plan.startswith('# AFQR-01–20 modular consolidation program plan\n\n**Status:** R1A–R1E and overall R1 complete. R2 doctrine-drift resolution ready. R3–R6 blocked. RT-002G unauthorized. Temporary evidence deletion unauthorized.')
 allowed={'docs/decisions/current_decisions_log.md','docs/doctrine/astra_doctrine_registry_v0_1.yaml','docs/doctrine/control/afqr_01_20_consolidation_program_plan.md','docs/doctrine/reviews/afqr_01_20_consolidation_file_manifest.yaml',REVIEW,BLED,CLED,'tests/test_afqr_r1d_agency_epistemic_social_communication.py','tests/test_afqr_r1d_core_transaction_identity_relation.py','tests/test_afqr_r1d_world_action_sensing.py','tests/test_afqr_r1e_formal_completion_review.py'}
 run=lambda *a:subprocess.run(a,cwd=ROOT,text=True,capture_output=True,check=True).stdout.splitlines();changed=set(run('git','diff','--name-only',f'{BASE}...HEAD'));assert changed==allowed;subprocess.run(['git','diff','--check',f'{BASE}...HEAD'],cwd=ROOT,check=True);nums=run('git','diff','--numstat',f'{BASE}...HEAD');assert not any(x.startswith('-\t-\t') for x in nums);assert run('git','diff','--name-status','--diff-filter=D',f'{BASE}...HEAD')==[];assert not any(p.startswith(('src/','working/afqr_consolidation_inputs/')) or p.lower().endswith(('.zip','.pdf','.png','.jpg','.gif')) for p in changed);assert not any('r2_' in p.lower() or 'rt_002g' in p.lower() or any(q in p.lower() for q in ['schema','conversion','canon','sourcebook','model','narration','live_play','ui']) for p in changed)

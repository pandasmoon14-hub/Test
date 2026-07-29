"""Semantic contract tests for bounded AFQR-10–15 R1D-AGENCY doctrine."""
import json, pathlib, re, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE='5c346a0ebd192879abaed0099f5644589df97884'
DOC=ROOT/'docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md'
R1B=ROOT/'docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml'
R1C=ROOT/'docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml'
CORE_DOC=ROOT/'docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md'
AUTH=ROOT/'docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml'
R1B_ESC=ROOT/'docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml'
R1C_ESC=ROOT/'docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml'
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

def test_invariant_provenance_is_semantically_relevant_and_source_backed():
 c=contract(); upstream={x['invariant_id']:x for x in load(R1C)['cross_afqr_invariants']}; records=c['family_invariants']
 assert len({tuple(x['r1c_invariant_ids']) for x in records})>1
 required={'INV-002','INV-003','INV-005','INV-006','INV-008','INV-009'}
 assert required<={i for x in records for i in x['r1c_invariant_ids']}
 domains={'INV-001':{'compatibility','ownership'},'INV-002':{'truth','evidence','observation','knowledge','memory','deception','communication'},'INV-003':{'sensing','expression','reception','interpretation','communication'},'INV-005':{'identity','personhood','agency','control','responsibility'},'INV-006':{'social','relation','dependency','institution','jurisdiction','reachability','obligation','negotiation'},'INV-008':{'motivation','behavior','prediction','culture','agency','responsibility'},'INV-009':{'donor','universal','astra law'}}
 for x in records:
  assert x['provenance_kind'] in {'r1c_derived','family_local'} and x['source_evidence_identifiers'] and x['source_paths'] and x['rationale']
  assert all((ROOT/p).is_file() for p in x['source_paths'])
  if x['provenance_kind']=='family_local': assert x['r1c_invariant_ids']==[] and any(p.endswith('.md') and 'AFQR-' in p for p in x['source_paths'])
  else:
   assert x['r1c_invariant_ids'] and set(x['r1c_invariant_ids'])<=set(upstream)
   words=set(re.findall(r'[a-z]+',x['rule'].lower())); assert all(words & domains[i] for i in x['r1c_invariant_ids'])
   assert set(x['source_evidence_identifiers'])=={e for i in x['r1c_invariant_ids'] for e in upstream[i]['source_evidence_records']}

def test_collisions_match_both_open_ledgers_and_are_individual():
 c=contract(); b={x['collision_ids'][0]:x for x in load(R1B_ESC)['escalations']}; rc={x['collision_id']:x for x in load(R1C_ESC)['escalations'] if 'collision_id' in x}; actual={x['collision_id']:x for x in c['collision_resolution_candidates']}
 assert set(actual)==set(b)==set(rc)=={'COLL-03','COLL-08','COLL-10'}
 rules=set(); prohibited=set()
 for cid,x in actual.items():
  u=b[cid]; assert x['exact_terms']==u['terms']; assert x['exact_affected_afqrs']==u['affected_afqrs']; assert x['exact_r1b_owner_candidates']==u['current_owner_candidates']; assert x['exact_r1b_evidence_record_identifiers']==u['source_evidence_records']
  assert x['exact_r1b_lawful_interim_usage']==u['lawful_interim_usage']; assert x['exact_r1b_prohibited_interim_usage']==u['prohibited_interim_usage']; assert x['upstream_r1b_status']=='open' and u['status']=='closed_by_r1e'; assert x['upstream_r1c_status']=='open' and rc[cid]['status']=='closed_by_r1e'; assert x['status']=='candidate_pending_R1E'
  afqr_candidates={a for a in u['current_owner_candidates'] if a.startswith('AFQR-')}; assert set(x['participating_agency_family_owners'])==afqr_candidates&A; assert set(x['external_core_family_owners'])==afqr_candidates&C
  assert x['source_paths'] and all((ROOT/p).is_file() for p in x['source_paths']); assert x['candidate_specific_safe_handoffs'] and x['candidate_specific_corpus_scale_risks'] and x['candidate_specific_r1e_review_questions']
  rules.add(x['candidate_attribution_rule']); prohibited.add(tuple(x['candidate_specific_prohibited_inferences']))
 assert len(rules)==len(prohibited)==3

def test_afqr14_provenance_exactly_matches_authority_and_manifest():
 c=contract()['afqr14_validation_provenance']; a=next(x for x in load(AUTH)['afqr_records'] if x['afqr_id']=='AFQR-14')
 assert c['architecture_owner']=='AFQR-14'; assert c['primary_source_evidence']==a['source_evidence_records'][0]=='SRC-0103'; assert c['title_evidence']==a['title_evidence_records'][0]=='SRC-0114'; assert c['corrected_baseline_evidence']==a['corrected_baseline_evidence_records']==['SRC-0103','SRC-0139','SRC-0121']; assert c['validation_packaging']=='AFQR-15 archive'
 assert c['primary_architecture_source_path']==a['source_packet_paths'][0]; assert all((ROOT/c[k]).is_file() for k in ('primary_architecture_source_path','validation_note_source_path','stale_manifest_source_path','title_evidence_source_path'))
 required={'AFQR-14 owns communication and interpretation','AFQR-15-packaged validation only confirms the normative AFQR-14 files','validation supersedes reliance on the stale artifact manifest only','validation does not transfer ownership','AFQR-15 does not become the communication owner','no model realization, prose generation, narration, or live-play behavior is authorized'}; assert set(c['rules'])==required

def test_substrates_are_exact_r1c_records_with_distinct_bounded_dispositions():
 c={x['substrate_id']:x for x in contract()['missing_substrate_dispositions']}; upstream={x['substrate_id']:x for x in load(R1C)['missing_substrate_classifications']}; assert set(c)=={'SUB-001','SUB-002','SUB-005'}
 risks=set(); prohib=set()
 for sid,x in c.items():
  u=upstream[sid]; assert x['exact_substrate_name']==u['name']; assert x['exact_owner_disposition']==u['future_doctrine_owner']; assert x['exact_requiring_afqrs']==u['requiring_afqrs']; assert x['exact_evidence_identifiers']==u['source_evidence_records']; assert x['exact_evidence_paths']==u['source_evidence_paths']; assert x['collapse_risk']==u['failure_or_collapse_risk']; assert x['upstream_status']==u['status']; assert not x['combined_owner_invented']; assert all((ROOT/p).is_file() for p in x['exact_evidence_paths'])
  assert set(x['core_family_scope']+x['agency_family_scope']+x['world_family_scope'])==set(u['requiring_afqrs']); risks.add(x['collapse_risk']); prohib.add(x['r1d_agency_prohibited_implementation'])
 assert len(risks)==len(prohib)==3

def test_required_inferences_differentiated_pressure_and_gates():
 c=contract(); rules={x['rule'] for x in c['family_invariants']}; required={'evidence admission is not truth','sensing is not knowledge','identity is not personhood','control is not consent','motivation is not agency','behavior is not responsibility','social status is not institutional authority','jurisdiction is not reachability','communication is not truth','persuasion is not consent','adjudication is not enforcement execution'}; assert required<=rules
 records=c['corpus_pressure_records']; assert len(records)==18==len({x['pressure_class'] for x in records}); payloads=set()
 fields={'agency_landing_afqrs','core_handoff_afqrs','world_handoff_afqrs','source_local_constructs','quarantine_triggers','escalation_triggers','prohibited_universalizations','rationale'}
 for x in records:
  assert fields<=set(x); assert set(x['agency_landing_afqrs'])<=A and set(x['core_handoff_afqrs'])<=C and set(x['world_handoff_afqrs'])<=W; assert x['agency_landing_afqrs'] or x['core_handoff_afqrs'] or x['world_handoff_afqrs'] or x['source_local_constructs'] or x['quarantine_triggers'] or x['escalation_triggers']; assert x['prohibited_universalizations'] and not x['conversion_performed']
  payload=tuple(json.dumps(x[k],sort_keys=True) for k in sorted(fields)); assert payload not in payloads; payloads.add(payload)
 by={x['pressure_class']:x for x in records}; assert by['fantasy alignment, ideals, bonds, flaws, and reaction systems']['core_handoff_afqrs']==['AFQR-09']; assert {'AFQR-10','AFQR-11','AFQR-12'}<=set(by['science-fiction AI, synthetic personhood, distributed agents, and machine memory']['agency_landing_afqrs']); assert {'AFQR-19','AFQR-20'}<=set(by['psionics, telepathy, possession, domination, mind control, and shared consciousness']['world_handoff_afqrs'])
 assert c['completion_boundary']=={'R1D-CORE':'complete','R1D-AGENCY':'complete','overall_R1D':'incomplete','R1D-WORLD':'ready_not_started','R1E':'blocked','R2-R6':'blocked','RT-002G':'unauthorized','temporary_evidence_deletion':'unauthorized'}; assert c['r1e_handoff']['global_escalations'].endswith('remain open pending R1E')

def test_registry_manifest_and_committed_scope():
 reg=(ROOT/'docs/doctrine/astra_doctrine_registry_v0_1.yaml').read_text(); assert 'AFQR-10-15-R1D-AGENCY-EPISTEMIC-SOCIAL-COMMUNICATION-001' in reg; assert 'status: pressure-tested\n  layer: 0_control\n  phase: R1D-AGENCY' in reg
 man=load(ROOT/'docs/doctrine/reviews/afqr_01_20_consolidation_file_manifest.yaml'); current={x['file_id']:x['status'] for x in man['planned_files']}
 assert current['R1D-CORE']=='complete'; assert current['R1D-AGENCY']=='complete'; assert current['R1D-WORLD']=='complete'; assert current['R1E']=='complete'
 gates=contract()['completion_boundary']; assert gates['overall_R1D']=='incomplete'; assert gates['R2-R6']=='blocked'; assert gates['RT-002G']=='unauthorized'
 changed=subprocess.check_output(['git','diff','--name-only',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines(); nums=subprocess.check_output(['git','diff','--numstat',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines(); deleted=subprocess.check_output(['git','diff','--name-status','--diff-filter=D',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines()
 assert not any(p.startswith('src/') or p.lower().endswith('.zip') or 'formal_completion_review' in p for p in changed); assert not any(x.startswith('-\t-\t') for x in nums); assert not deleted
 assert not any('working/afqr_consolidation_inputs' in p for p in changed)

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
   assert x['owner'] not in t.get('explicit_nonowners',[])
   if t['unqualified_usage']=='qualified_only':
    qualified={q['qualified_form'] for q in t.get('qualified_forms',[])}
    assert x['form'] in qualified and x['form']!=t['canonical_form']
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
def test_invariants_have_exact_provenance_and_semantic_mappings():
 c=contract(); upstream={x['invariant_id']:x for x in load(R1C)['cross_afqr_invariants']}
 manifest=load(ROOT/'working/afqr_consolidation_inputs/manifest.yaml'); archives={x['archive_record_id']:x['current_path'] for x in manifest['archive_records']}; paths={x['source_record_id']:(x['normalized_path'] or archives[x['parent_archive_record_id']]) for x in manifest['contained_file_records']}
 expectations={'environment is not topology':['INV-007'],'environmental process is not logical time':['INV-007'],'reachability is not jurisdiction':['INV-006'],'capability is not opportunity':['INV-004'],'target is not resolution':['INV-004'],'signal is not communication':['INV-003'],'signal is not interpretation':['INV-003'],'exposure is not harm':['INV-007'],'donor anatomy, grid, damage, action-economy, cosmology, and sensing assumptions are not Astra law':['INV-009']}
 records={x['rule']:x for x in c['family_invariants']};assert set(expectations)|{'embodiment is not identity','reachability is not opportunity','reachability is not target','detection is not target','observation candidate is not epistemic observation record','resolution is not transition commitment'}==set(records)
 for rule,ids in expectations.items():
  x=records[rule];assert x['provenance_kind']=='r1c_derived' and x['r1c_invariant_ids']==ids
  evidence=sorted({e for i in ids for e in upstream[i]['source_evidence_records']});assert x['source_evidence_identifiers']==evidence
  assert x['evidence_path_bindings']==[{'evidence_id':e,'source_path':paths[e]} for e in evidence]
 for x in records.values():
  assert x['source_paths'] and all((ROOT/q).is_file() for q in x['source_paths']);assert {z['evidence_id'] for z in x['evidence_path_bindings']}==set(x['source_evidence_identifiers']);assert {z['source_path'] for z in x['evidence_path_bindings']}==set(x['source_paths']);assert x['rationale']
  if x['provenance_kind']=='family_local':
   assert x['r1c_invariant_ids']==[] and any(e in {'SRC-0152','SRC-0180','SRC-0207','SRC-0231','SRC-0255'} for e in x['source_evidence_identifiers'])
 assert records['embodiment is not identity']['provenance_kind']=='family_local' and records['embodiment is not identity']['r1c_invariant_ids']==[]
 endpoints={'embodiment is not identity':{'SRC-0152','SRC-0011'},'reachability is not opportunity':{'SRC-0207','SRC-0231'},'reachability is not target':{'SRC-0207','SRC-0231'},'detection is not target':{'SRC-0255','SRC-0231'},'observation candidate is not epistemic observation record':{'SRC-0255','SRC-0022'},'resolution is not transition commitment':{'SRC-0231','SRC-0004'}}
 for rule,evidence in endpoints.items(): assert records[rule]['provenance_kind']=='family_local' and records[rule]['r1c_invariant_ids']==[] and set(records[rule]['source_evidence_identifiers'])==evidence
 assert records['detection is not target']['exact_boundary_evidence']=='DEP-094'
def test_collision_specific_records_match_every_r1b_field():
 c=contract();rb={x['collision_id']:x for x in load(R1B)['collision_resolutions']};rows=c['resolved_collision_boundary_records'];assert {x['collision_id'] for x in rows}=={'COLL-01','COLL-02','COLL-04','COLL-05','COLL-06','COLL-07','COLL-08','COLL-09'}
 mapping={'exact_terms':'source_terms','source_afqrs':'source_afqrs','r1b_status':'r1b_status','exact_owner_assignments':'term_owner_assignments','qualification_rules':'qualification_rules','rejected_aliases':'rejected_aliases','explicit_non_equivalences':'explicit_non_equivalences','exact_evidence_records':'source_evidence_records','corpus_collapse_risk':'corpus_collapse_risk'}
 for x in rows:
  assert all(x[a]==rb[x['collision_id']][b] for a,b in mapping.items());assert x['world_family_relevance'] and x['prohibited_inferences']
 assert len({x['world_family_relevance'] for x in rows})==len(rows);assert len({tuple(x['prohibited_inferences']) for x in rows})==len(rows)
 coll8=next(x for x in rows if x['collision_id']=='COLL-08');assert coll8['source_afqrs']==rb['COLL-08']['source_afqrs'];assert 'AFQR-18 appears only as prohibited-inference pressure' in coll8['world_family_relevance']
def test_open_escalations_match_both_ledgers_and_agency_unchanged():
 c=contract();b=load(ROOT/'docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml');r=load(ROOT/'docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml')
 rb={x['collision_ids'][0]:x for x in b['escalations']};rc={x['collision_id']:x for x in r['escalations'] if 'collision_id' in x};assert set(rb)==set(rc)=={'COLL-03','COLL-08','COLL-10'};assert all(rb[i]['status']=='closed_by_r1e' and rc[i]['status']=='closed_by_r1e' for i in rb)
 assert c['preserved_open_escalations']['new_world_candidates']==[] and c['preserved_open_escalations']['collision_ids']==['COLL-03','COLL-08','COLL-10'];assert c['r1e_handoff']['next_lawful_gate'].startswith('R1E')
 agency=fenced(ROOT/'docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md');assert {x['collision_id'] for x in agency['collision_resolution_candidates']}==set(rb);assert rb['COLL-08']['affected_afqrs']==['AFQR-09','AFQR-13','AFQR-15']
def test_substrates_are_exact_and_specific():
 c=contract();up={x['substrate_id']:x for x in load(R1C)['missing_substrate_classifications']};rows={x['substrate_id']:x for x in c['missing_substrate_dispositions']};assert set(rows)=={'SUB-002','SUB-005'}
 for sid,x in rows.items():
  u=up[sid];assert x['exact_substrate_name']==u['name'];assert x['exact_requiring_afqrs']==u['requiring_afqrs'];assert x['exact_evidence_identifiers']==u['source_evidence_records'];assert x['exact_evidence_paths']==u['source_evidence_paths'];assert x['exact_future_owner_posture']==u['future_doctrine_owner'];assert x['upstream_status']==u['status'];assert x['collapse_risk']==u['failure_or_collapse_risk'];assert set(x['core_family_scope']+x['agency_family_scope']+x['world_family_scope'])==set(u['requiring_afqrs'])
 assert rows['SUB-002']['r1d_world_may_consolidate']!=rows['SUB-005']['r1d_world_may_consolidate'];assert rows['SUB-002']['r1d_world_must_not_implement']!=rows['SUB-005']['r1d_world_must_not_implement'];assert set(rows['SUB-002']['separate_owner_requirements'])=={'AFQR-04','AFQR-06','AFQR-10','AFQR-20'};assert 'truth/evidence/sensing' in rows['SUB-002']['combined_owner_prohibition']
def test_pressure_gates_registry_manifest_and_scope():
 c=contract();ps=c['corpus_pressure_records'];assert len(ps)==18==len({x['pressure_class'] for x in ps});by={x['pressure_class']:x for x in ps}
 expected={
 'fantasy anatomy, damage, conditions, grids, initiative, combat, stealth, terrain, and weather':({'AFQR-16','AFQR-17','AFQR-18','AFQR-19','AFQR-20'},{'grid adjacency','armor-class'}),
 'science-fiction vacuum, radiation, cybernetics, vehicles, mechs, ships, sensors, and electronic warfare':({'AFQR-16','AFQR-17','AFQR-18','AFQR-19','AFQR-20'},{'sensor lock','radiation'}),
 'hybrid science-fantasy embodiment, environments, spatial layers, weapons, and sensing':({'AFQR-16','AFQR-17','AFQR-18','AFQR-19','AFQR-20'},{'astral layer','mana'}),
 'cultivation meridians, cores, body refinement, tribulations, domains, movement arts, perception, and conflict':({'AFQR-16','AFQR-17','AFQR-18','AFQR-19','AFQR-20'},{'meridian','spiritual perception'}),
 'class and archetype capability and combat packages':({'AFQR-19'},{'class possession','action economy'}),
 'profession and occupation hazard, tool, movement, and sensing assumptions':({'AFQR-16','AFQR-17','AFQR-18','AFQR-20'},{'tool proficiency','workplace exposure'}),
 'point-buy physical, sensory, movement, combat, and resilience traits':({'AFQR-16','AFQR-18','AFQR-19','AFQR-20'},{'purchased perception','point cost'}),
 'narrative tags, aspects, harm tracks, consequences, clocks, zones, and fictional positioning':({'AFQR-16','AFQR-18','AFQR-19'},{'narrative clock','stress track'}),
 'cyberware, biotech, prosthetics, replacement bodies, neural sensing, and transformation':({'AFQR-16','AFQR-20'},{'replacement-body','neural contact'}),
 'psionic perception, telepathy, concealment, possession, targeting, and mental conflict':({'AFQR-19','AFQR-20'},{'telepathic detection','possession'}),
 'horror injury, trauma, contamination, transformation, unreliable sensing, and environmental threat':({'AFQR-16','AFQR-17','AFQR-20'},{'unreliable sensing','contamination'}),
 'investigation searches, clues, surveillance, tracking, concealment, and evidence acquisition':({'AFQR-18','AFQR-20'},{'admitted evidence','valid targets'}),
 'vehicles, ships, mechs, platforms, operators, components, scale, movement, damage, targeting, and sensors':({'AFQR-16','AFQR-18','AFQR-19','AFQR-20'},{'operator agency','sensor contact'}),
 'companions, summons, familiars, proxies, swarms, and distributed bodies':({'AFQR-16','AFQR-18','AFQR-19','AFQR-20'},{'summoner identity','shared sensing'}),
 'crafting, salvage, repair, replacement, environmental modification, and constructed platforms':({'AFQR-16','AFQR-17','AFQR-18'},{'salvage creates','repair rewrites'}),
 'bestiary anatomy, scales, movement forms, senses, hazards, attacks, defenses, and transformations':({'AFQR-16','AFQR-17','AFQR-18','AFQR-19','AFQR-20'},{'species anatomy','creature reach'}),
 'tables and oracles for weather, terrain, encounters, damage, targeting, and sensing':({'AFQR-16','AFQR-17','AFQR-18','AFQR-19','AFQR-20'},{'committed truth','typed quantity'}),
 'missions, scenarios, supplements, and adventure paths with local combat, map, hazard, and sensory assumptions':({'AFQR-17','AFQR-18','AFQR-19','AFQR-20'},{'boxed text','scenario map'})}
 assert set(expected)==set(by)
 for name,(owners,phrases) in expected.items():
  x=by[name];assert owners<=set(x['world_landing_afqrs']);blob=json.dumps(x).lower();assert all(q in blob for q in phrases)
 for x in ps:
  assert set(x['world_landing_afqrs'])==set(x['world_landing_reasons'])<=W;assert set(x['core_family_handoff_afqrs'])==set(x['core_handoff_reasons'])<=C;assert set(x['agency_family_handoff_afqrs'])==set(x['agency_handoff_reasons'])<=A
  assert x['source_local_constructs'] and x['quarantine_triggers'] and x['escalation_triggers'] and x['prohibited_universalizations'] and x['rationale'];blob=json.dumps(x).lower();assert not re.search(r'\b\d+(?:th|st|nd|rd) donor construct\b|pressure class \d+',blob)
 assert len({tuple(x['quarantine_triggers']) for x in ps})==18;assert len({tuple(x['escalation_triggers']) for x in ps})==18;assert len({tuple(x['prohibited_universalizations']) for x in ps})==18;assert len({x['rationale'] for x in ps})==18
 assert by['class and archetype capability and combat packages']['agency_family_handoff_afqrs']==[] and 'AFQR-12' not in by['class and archetype capability and combat packages']['agency_handoff_reasons']
 tables=by['tables and oracles for weather, terrain, encounters, damage, targeting, and sensing'];assert 'AFQR-07' in tables['core_handoff_reasons'] and 'typed quantity' in tables['core_handoff_reasons']['AFQR-07']
 craft=by['crafting, salvage, repair, replacement, environmental modification, and constructed platforms'];assert 'actual typed dependency' in craft['core_handoff_reasons']['AFQR-09']
 assert {'AFQR-18','AFQR-19','AFQR-20'}<=set(by['fantasy anatomy, damage, conditions, grids, initiative, combat, stealth, terrain, and weather']['world_landing_afqrs']);assert 'AFQR-19' in by['class and archetype capability and combat packages']['world_landing_afqrs'];assert {'AFQR-16','AFQR-17','AFQR-18'}<=set(by['cultivation meridians, cores, body refinement, tribulations, domains, movement arts, perception, and conflict']['world_landing_afqrs']);assert {'AFQR-16','AFQR-19','AFQR-20'}<=set(by['point-buy physical, sensory, movement, combat, and resilience traits']['world_landing_afqrs']);assert 'AFQR-16' in by['narrative tags, aspects, harm tracks, consequences, clocks, zones, and fictional positioning']['world_landing_afqrs']
 assert c['completion_boundary']=={'R1D-CORE':'complete','R1D-AGENCY':'complete','R1D-WORLD':'complete','overall_R1D':'complete','overall_R1':'incomplete_pending_R1E','R1E':'ready','R2-R6':'blocked','RT-002G':'unauthorized','temporary_evidence_deletion':'unauthorized'}
 man={x['file_id']:x['status'] for x in load(ROOT/'docs/doctrine/reviews/afqr_01_20_consolidation_file_manifest.yaml')['planned_files']};assert man['R1D-CORE']==man['R1D-AGENCY']==man['R1D-WORLD']=='complete' and man['R1E']=='complete'
 reg=(ROOT/'docs/doctrine/astra_doctrine_registry_v0_1.yaml').read_text();assert 'AFQR-16-20-R1D-WORLD-ACTION-SENSING-001' in reg and 'status: pressure-tested\n  layer: 0_control\n  phase: R1D-WORLD' in reg
 changed=subprocess.check_output(['git','diff','--name-only',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines();nums=subprocess.check_output(['git','diff','--numstat',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines();deleted=subprocess.check_output(['git','diff','--name-status','--diff-filter=D',f'{BASE}...HEAD'],cwd=ROOT,text=True).splitlines()
 allowed={'docs/decisions/current_decisions_log.md','docs/doctrine/astra_doctrine_registry_v0_1.yaml','docs/doctrine/consolidation/afqr_world_action_sensing.md','docs/doctrine/control/afqr_01_20_consolidation_program_plan.md','docs/doctrine/reviews/afqr_01_20_consolidation_file_manifest.yaml','docs/doctrine/reviews/afqr_r1d_world_consolidation_report.md','tests/test_afqr_r1d_world_action_sensing.py','tests/test_afqr_r1d_core_transaction_identity_relation.py','tests/test_afqr_r1d_agency_epistemic_social_communication.py','docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml','docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml','docs/doctrine/reviews/afqr_01_20_formal_completion_review.md','tests/test_afqr_r1e_formal_completion_review.py'}
 assert set(changed)<=allowed and not any(p.startswith('src/') or p.lower().endswith('.zip') for p in changed);assert not any(x.startswith('-\t-\t') for x in nums);assert not deleted;assert not any('working/afqr_consolidation_inputs' in p for p in changed)

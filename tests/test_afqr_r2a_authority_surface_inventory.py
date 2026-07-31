"""Deterministic bounded-semantic R2A inventory and drift-proof validation."""
from __future__ import annotations
import hashlib,json,subprocess
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REV=ROOT/'docs/doctrine/reviews';BASE='9382958197c9d5dee9d29cb5f9d051147237c64d';R1='bbc9d58cb23f1616327f73294def6ec42055a324';R20='4aa1fce6a74f97b275a9c1d5975d0d192dcd2506';ABANDONED='50c0320acd1a9a075cba18e1309dd3d15ac5c44d'
INDEX=REV/'afqr_r2a_authority_surface_inventory.yaml';ROUTING=REV/'afqr_r2a_doctrine_drift_routing.yaml'
BASE_ALLOW={'docs/decisions/current_decisions_log.md','docs/doctrine/astra_doctrine_registry_v0_1.yaml','docs/doctrine/control/afqr_01_20_consolidation_program_plan.md','docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md','docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_core.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_agency.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_world.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_continuity_cross_phase.yaml','docs/doctrine/reviews/afqr_r2a_doctrine_drift_routing.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_report.md','tests/test_afqr_r2_continuity_research_assimilation.py','tests/test_afqr_r2a_authority_surface_inventory.py'}
def load(p):return json.loads(p.read_text())
def git(*a):return subprocess.check_output(('git',)+a,cwd=ROOT,text=True)
def records():
 idx=load(INDEX);docs=[load(ROOT/x['path']) for x in idx['shards']];return idx,[s for d in docs for s in d['surface_records']],[h for d in docs for h in d['dismissed_hit_records']]
MODIFIED={'docs/decisions/current_decisions_log.md','docs/doctrine/astra_doctrine_registry_v0_1.yaml','docs/doctrine/control/afqr_01_20_consolidation_program_plan.md','docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md','docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml','tests/test_afqr_r2_continuity_research_assimilation.py'}
def baseline_lines(path):return (subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT).decode('utf8','replace') if path in MODIFIED else (ROOT/path).read_text(errors='replace')).splitlines()
def digest(lines,a,b):return hashlib.sha256(('\n'.join(lines[a-1:b])+'\n').encode()).hexdigest()
def test_baseline_ancestry_exact_scope_and_no_forbidden_changes():
 for rev in (BASE,R1,R20):assert subprocess.run(['git','merge-base','--is-ancestor',rev,'HEAD'],cwd=ROOT).returncode==0
 if subprocess.run(['git','cat-file','-e',ABANDONED+'^{commit}'],cwd=ROOT,capture_output=True).returncode==0:assert subprocess.run(['git','merge-base','--is-ancestor',ABANDONED,'HEAD'],cwd=ROOT,capture_output=True).returncode!=0
 changed=set(git('diff','--name-only',BASE+'...HEAD').splitlines())|{x[3:] for x in git('status','--porcelain').splitlines() if x.startswith('?? ')};extras={p for p in changed if p.startswith('docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_') and p not in BASE_ALLOW}
 assert changed==BASE_ALLOW|extras;assert all(p.startswith('docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_') for p in extras)
 assert subprocess.run(['git','diff','--check',BASE+'...HEAD'],cwd=ROOT,capture_output=True).returncode==0;assert '-\t-\t' not in git('diff','--numstat',BASE+'...HEAD');assert not git('diff','--name-status','--diff-filter=D',BASE+'...HEAD').strip()
 assert not [p for p in changed if p.startswith(('src/','schemas/','conversion/','canon/','model/','narration/','ui/','live-play/')) or 'rt_002g' in p.lower()]
def test_every_record_has_resolving_bounded_hash_and_terms():
 idx,surfaces,hits=records();assert idx['inspected_commit']==BASE and idx['coverage_unit']=='bounded semantic occurrence blocks';ids=[s['surface_id'] for s in surfaces];assert len(ids)==len(set(ids))==idx['surface_count']
 for r in surfaces+hits:
  lines=baseline_lines(r['path']);a,b=r['line_start'],r['line_end'];assert 1<=a<=b<=len(lines);assert r['excerpt_sha256']==digest(lines,a,b);excerpt='\n'.join(lines[a-1:b]).lower();assert (r in surfaces or r['matched_terms']) and all(t.lower() in excerpt for t in r['matched_terms']);assert r['locator_heading_or_symbol']
def test_every_controlled_matching_line_is_accounted_with_term_and_cluster():
 idx,surfaces,hits=records();ranges=defaultdict(list)
 for r in surfaces+hits:ranges[r['path']].append(r)
 candidates=0
 for p in git('ls-tree','-r','--name-only',BASE).splitlines():
  if not p.endswith(tuple(idx['eligible_text_extensions'])):continue
  lines=baseline_lines(p);found=False
  for n,line in enumerate(lines,1):
   terms=[t for ts in idx['search_clusters'].values() for t in ts if t.lower() in line.lower()]
   if not terms:continue
   found=True;cover=[r for r in ranges[p] if r['line_start']<=n<=r['line_end'] and any(t.lower() in {x.lower() for x in r['matched_terms']} for t in terms)];assert cover,(p,n,terms)
  candidates+=found
 assert candidates==idx['candidate_file_count']==749 and idx['unaccounted_occurrence_count']==idx['unaccounted_candidate_file_count']==0
 assert len(surfaces)==idx['mapped_surface_count']==135 and len(hits)==idx['dismissed_occurrence_block_count']==2553
def test_priority_set_received_semantic_records_or_specific_dismissals():
 _,surfaces,hits=records();paths={r['path'] for r in surfaces+hits};required={'docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_scaffold.md','docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md','docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_scaffold.md','docs/doctrine/control/RT003_combat_hazard_damage_recovery_owner_specification.md','docs/doctrine/control/RT007_social_faction_knowledge_state_owner_scaffold.md','docs/doctrine/control/RT007_social_faction_actor_knowledge_owner_specification.md','docs/doctrine/operations/batch_b/B02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md','docs/doctrine/operations/batch_b/B08_travel_exploration_navigation_and_discovery_procedure.md','docs/doctrine/operations/batch_b/B09_social_faction_contact_and_institutional_interaction_procedure.md','src/astra_runtime/domain/action_legality.py','src/astra_runtime/domain/transaction_lifecycle.py','src/astra_runtime/kernel/transaction_preview.py','src/astra_runtime/kernel/replay_audit.py','src/astra_runtime/kernel/context_projection.py','src/astra_runtime/kernel/hidden_information.py','docs/doctrine/schema/C05_faction_institution_record_schema.md','docs/doctrine/schema/C09_hazard_environment_record_schema.md','schemas/manifest.schema.json'};assert required<=paths
 for root in ('docs/doctrine/control/','docs/doctrine/operations/','docs/doctrine/schema/','docs/doctrine/world/','docs/doctrine/reviews/','src/astra_runtime/','tests/runtime/'):
  candidate={p for p in paths if p.startswith(root)};assert candidate and all(any(r['path']==p for r in surfaces+hits) for p in candidate)
def test_dismissals_are_specific_and_not_boilerplate():
 _,surfaces,hits=records();sids={s['surface_id'] for s in surfaces};bad=('Semantic file review found only operational','file-level semantic review at first controlled match');summaries=Counter(h['semantic_review_summary'] for h in hits)
 for h in hits:
  assert not any(x in h['semantic_review_summary'] for x in bad);assert 'Local construct:' in h['semantic_review_summary'];assert ('not an AFQR owner' in h['semantic_review_summary'] or 'nonauthoritative source-local usage' in h['semantic_review_summary']);assert summaries[h['semantic_review_summary']]<5 or h['dismissal_reason']=='generated_or_vendor_text'
  if h['dismissal_reason']=='duplicate_locator_already_mapped':assert h['related_surface_id_if_duplicate'] in sids
def test_normative_grounding_and_structural_owner_safety():
 _,surfaces,_=records();norm=[s for s in surfaces if s['authority_level']=='current_normative'];expected={'AFQR-01':'CORE-RESP-01','AFQR-02':'CORE-RESP-02','AFQR-04':'CORE-RESP-04','AFQR-06':'CORE-RESP-06','AFQR-07':'CORE-RESP-07','AFQR-08':'CORE-RESP-08','AFQR-09':'CORE-RESP-09','AFQR-10':'AGENCY-RESP-10','AFQR-16':'WORLD-RESP-16','AFQR-17':'WORLD-RESP-17','AFQR-19':'WORLD-RESP-19','AFQR-20':'WORLD-RESP-20'}
 assert {s['applicable_afqr_ids'][0]:s['applicable_r1d_responsibility_ids'][0] for s in norm}==expected
 for s in norm:assert s['applicable_afqr_ids'] and s['applicable_r1d_responsibility_ids'];assert s['primary_shard']==('CORE' if int(s['applicable_afqr_ids'][0][-2:])<=9 else 'AGENCY' if int(s['applicable_afqr_ids'][0][-2:])<=15 else 'WORLD')
 owners=load(ROUTING)['semantic_owner_contract'];assert set(owners)==set(expected);assert owners['AFQR-01'].startswith('commitment') and 'identity and continuity' in owners['AFQR-08'] and 'environmental state' in owners['AFQR-17']
 assert all(s['declared_owner'] not in ('continuity','cross-phase','storage','replay','journaling') for s in surfaces)
def test_claim_links_are_reciprocal_reasoned_and_relevant():
 _,surfaces,_=records();routing=load(ROUTING);claims={c['claim_id']:c for c in routing['claim_assessments']};smap={s['surface_id']:s for s in surfaces}
 for s in surfaces:
  assert set(s['linked_r2_claim_ids'])==set(s['claim_link_reasons']);assert len(s['linked_r2_claim_ids'])<=12 or s.get('high_surface_count_justification');assert all(set(v)=={'relevance_type','semantic_role','exact_relevance','owner_boundary_effect'} for v in s['claim_link_reasons'].values())
  for cid in s['linked_r2_claim_ids']:assert s['surface_id'] in claims[cid]['surface_ids'] and s['claim_link_reasons'][cid]
 for c in claims.values():
  for sid in c['surface_ids']:assert c['claim_id'] in smap[sid]['linked_r2_claim_ids'] or sid in c['relevant_current_normative_surface_ids']
  assert c['r1_authority_analysis'] and c['repository_gap_or_conflict_analysis'] and c['implementation_analysis'] and c['claim_specific_reasoning'];assert c['r2_0_route_assessment'] in {'confirmed','narrowed','expanded','rerouted','downgraded','closed_as_already_governed','closed_as_unproven'}
  if c['r2a_disposition'] in ('no_drift_currently_governed','unproven_research_pressure'):assert c['relevant_current_normative_surface_ids'] or c['repository_evidence_state']=='absent'
def test_regression_claims_have_exact_independent_analysis():
 claims={c['claim_id']:c for c in load(ROUTING)['claim_assessments']}
 for n in (1,5,7,10,11,12,14,21,31):
  c=claims[f'R2-CLAIM-{n:04d}'];assert len(c['claim_specific_reasoning'])>250;assert c['candidate_r2b_package'] or c['primary_route'] in ('R5','R4')
 assert claims['R2-CLAIM-0031']['primary_route']=='R4' and 'AFQR-07' in claims['R2-CLAIM-0031']['r1_authority_analysis'];assert claims['R2-CLAIM-0014']['primary_route']=='R5'
def test_exactly_eleven_unresolved_questions_and_findings_preserved():
 r=load(ROUTING);qs=r['r2_0_unresolved_question_assessments'];assert len(qs)==11 and len({q['claim_id'] for q in qs})==11
 controlled={'resolved_by_existing_authority','representation_choice_not_doctrine','implementation_only','still_unresolved_doctrine_owner','still_unresolved_cross_phase_owner','deferred_frontier','unproven_research_question'};assert all(q['adjudication'] in controlled and q['surface_ids'] and q['reason'] for q in qs)
 assert len(r['repository_discovered_findings'])==11;assert all(f['surface_ids'] and f['accepted_authority_basis'] and f['primary_route'] for f in r['repository_discovered_findings'])
def test_package_and_module_derivation_is_non_circular():
 r=load(ROUTING);claims={c['claim_id']:c for c in r['claim_assessments']};findings={f['finding_id']:f for f in r['repository_discovered_findings']}
 for p,d in r['r2b_package_necessity'].items():
  assert set(d)=={'status','supporting_claim_ids','supporting_finding_ids','closure_claim_ids','owner_blocked_claim_ids','derivation'};assert all(x in claims for x in d['supporting_claim_ids']+d['closure_claim_ids']+d['owner_blocked_claim_ids']);assert all(x in findings for x in d['supporting_finding_ids']);assert d['status']=='blocked_pending_owner_adjudication' if d['owner_blocked_claim_ids'] else d['status'] in ('required','not_required')
 for d in r['r2b_continuity_module_necessity'].values():assert d['status']=='blocked_pending_owner_adjudication' if d['owner_blocked_claim_ids'] else d['status'] in ('required','not_required')
 assert r['gate_decision']=={'R1':'complete','R2':'active_incomplete','R2-0':'complete','R2A':'complete','R2B':'blocked','R2C':'blocked','R3-R6':'blocked','RT-002G':'unauthorized','temporary_evidence_deletion':'unauthorized'}
def test_exact_cluster_term_source_pressure_and_pretty_formatting():
 idx,surfaces,hits=records();clusters=idx['search_clusters']
 for r in surfaces+hits:
  expected=[k for k,ts in clusters.items() if any(t.lower() in {x.lower() for x in ts} for t in r.get('matched_terms',[]))];assert r['matched_search_clusters']==expected
 for h in hits:
  assert h['source_local_pressure_class'] in {'consistent_source_local_evidence','terminology_pressure','conversion_handoff_pressure','canon_handoff_pressure','owner_boundary_pressure','source_local_conflict','no_material_relation'}
 for e in idx['shards']:
  raw=(ROOT/e['path']).read_text();assert len(raw.splitlines())<=2500 and max(map(len,raw.splitlines()),default=0)<1000;assert raw.startswith('{\n')
 assert len(idx['shards'])==62
def test_complete_owner_coverage_and_no_unmapped_authority_claims():
 r=load(ROUTING);claims=r['claim_assessments'];required={a for c in claims for a in __import__('json').loads((REV/'afqr_r2_continuity_claim_and_owner_routing_ledger.yaml').read_text())['claims'][int(c['claim_id'][-4:])-1]['afqr_ids']};_,surfaces,_=records();mapped={a for s in surfaces if s['authority_level']=='current_normative' for a in s['applicable_afqr_ids']};assert required<=mapped
 assert all('no mapped R1 responsibility' not in c['r1_authority_analysis'] for c in claims)
def test_module_dependency_safety_and_final_gate():
 r=load(ROUTING);mods=r['r2b_continuity_module_necessity'];p=mods['CONTINUITY-BRANCH-SAFE-PROJECTION'];assert p['status']=='blocked_pending_owner_adjudication' and p['dependency_claim_ids'] and 'CONTINUITY-BRANCH-CANONICALITY' in p['dependency_module_ids'] and p['dependency_effect']
 assert r['status']=='PASS' and r['gate_decision']['R2A']=='complete' and r['gate_decision']['R2C']=='blocked'
def test_accepted_authority_and_r2_0_evidence_immutable():
 paths=['docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml','docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml','docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md','docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md','docs/doctrine/consolidation/afqr_world_action_sensing.md','docs/doctrine/reviews/afqr_01_20_formal_completion_review.md','docs/doctrine/reviews/afqr_r1e_source_and_vocabulary_audit.yaml','docs/doctrine/reviews/afqr_r1e_dependency_and_parity_audit.yaml','docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml','docs/doctrine/reviews/afqr_r1e_consistency_and_corpus_adequacy.yaml','docs/doctrine/reviews/afqr_r2_continuity_research_intake_packet.md','docs/doctrine/reviews/afqr_r2_continuity_research_source_manifest.yaml','docs/doctrine/reviews/afqr_r2_continuity_claim_and_owner_routing_ledger.yaml','docs/doctrine/reviews/afqr_r2_continuity_research_assimilation_report.md']
 for p in paths:assert (ROOT/p).read_bytes()==subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=ROOT)

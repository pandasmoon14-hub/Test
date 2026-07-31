"""Deterministic AFQR R2A baseline, coverage, routing, and nonauthority gate."""
from __future__ import annotations
import hashlib,json,subprocess
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REV=ROOT/'docs/doctrine/reviews'
BASE='9382958197c9d5dee9d29cb5f9d051147237c64d'; R1='bbc9d58cb23f1616327f73294def6ec42055a324'; R20='4aa1fce6a74f97b275a9c1d5975d0d192dcd2506'; ABANDONED='50c0320acd1a9a075cba18e1309dd3d15ac5c44d'
INDEX=REV/'afqr_r2a_authority_surface_inventory.yaml'; ROUTING=REV/'afqr_r2a_doctrine_drift_routing.yaml'
SHARDS=[REV/f'afqr_r2a_authority_surface_inventory_{x}.yaml' for x in ('core','agency','world','continuity_cross_phase')]
ALLOW={'docs/decisions/current_decisions_log.md','docs/doctrine/astra_doctrine_registry_v0_1.yaml','docs/doctrine/control/afqr_01_20_consolidation_program_plan.md','docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md','docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_core.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_agency.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_world.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_continuity_cross_phase.yaml','docs/doctrine/reviews/afqr_r2a_doctrine_drift_routing.yaml','docs/doctrine/reviews/afqr_r2a_authority_surface_inventory_report.md','tests/test_afqr_r2_continuity_research_assimilation.py','tests/test_afqr_r2a_authority_surface_inventory.py'}
SURFACE_KINDS={'normative_doctrine','accepted_decision','control_or_gate','registry_or_manifest','review_or_audit','production_schema','runtime_implementation','test_contract','fixture','example','conversion_surface','canon_surface','model_or_narration_surface','documentation','historical_record','other'}
AUTH={'current_normative','accepted_decision','tracking_control_only','implementation_contract_only','schema_contract_only','test_contract_only','review_evidence_only','historical_only','source_local_only','example_only','candidate_only','unknown_requires_escalation'}
CURRENT={'current','historical','superseded','deprecated','candidate','planned','source_local','unknown'}
GENERAL={'repository_general','family_scoped','subsystem_scoped','vertical_slice','narrow_fixture','source_local','historical_guard','placeholder','unknown'}
SEMANTIC={'consistent_with_r1','partial_but_not_conflicting','potential_doctrine_gap','direct_doctrine_conflict','owner_collision','terminology_drift','authority_mislabel','historical_residue','schema_presupposition','runtime_presupposition','test_presupposition','implementation_absence_only','conformance_risk','deferred_substrate_reference','no_material_semantic_relation','requires_owner_escalation'}
DISPOSITIONS={'no_drift_currently_governed','doctrine_gap_proven','doctrine_conflict_proven','owner_conflict_proven','terminology_or_authority_drift','implementation_conformance_only','deferred_substrate_handoff','runtime_retrofit_handoff','evaluation_or_adapter_later','deferred_frontier','rejected_architecture_guard','unproven_research_pressure','escalated_owner_question'}
ROUTES={'none','R2B-CORE','R2B-AGENCY','R2B-WORLD','R2B-CONTINUITY','R2B-CROSS-PHASE','R3','R4','R5','later_evaluation','later_gm_adapter','later_conversion_or_canon','deferred_frontier','Astra_Doctrine_Council'}
def load(p):return json.loads(p.read_text())
def git(*args):return subprocess.check_output(('git',)+args,cwd=ROOT,text=True)
def all_records():
 ds=[load(p) for p in SHARDS]
 return ds,[s for d in ds for s in d['surface_records']],[h for d in ds for h in d['dismissed_hit_records']]
def test_baseline_ancestry_and_exact_scope():
 for rev in (BASE,R1,R20):assert subprocess.run(['git','merge-base','--is-ancestor',rev,'HEAD'],cwd=ROOT).returncode==0
 if subprocess.run(['git','cat-file','-e',ABANDONED+'^{commit}'],cwd=ROOT,capture_output=True).returncode==0:assert subprocess.run(['git','merge-base','--is-ancestor',ABANDONED,'HEAD'],cwd=ROOT,capture_output=True).returncode!=0
 changed=set(git('diff','--name-only',BASE+'...HEAD').splitlines())|{x[3:] for x in git('status','--porcelain').splitlines() if x.startswith('?? ')}
 assert changed==ALLOW
 assert subprocess.run(['git','diff','--check',BASE+'...HEAD'],cwd=ROOT,capture_output=True).returncode==0
 assert '-\t-\t' not in git('diff','--numstat',BASE+'...HEAD');assert not git('diff','--name-status','--diff-filter=D',BASE+'...HEAD').strip()
 assert not [p for p in changed if p.startswith(('src/','schemas/','conversion/','canon/','model/','narration/','ui/','live-play/')) or 'rt_002g' in p.lower() or p.endswith(('.pdf','.zip','.png','.jpg'))]
def test_surface_locator_hashes_and_uniqueness():
 idx=load(INDEX);ds,surfaces,_=all_records();assert idx['inspected_commit']==BASE
 ids=[s['surface_id'] for s in surfaces];assert len(ids)==len(set(ids))==idx['surface_count']
 assert all(d['inspected_commit']==BASE for d in ds)
 for s in surfaces:
  raw=subprocess.check_output(['git','show',f'{BASE}:{s["path"]}'],cwd=ROOT).decode();lines=raw.splitlines();a,b=s['line_start'],s['line_end'];assert 1<=a<=b<=len(lines)
  excerpt='\n'.join(lines[a-1:b])+'\n';assert hashlib.sha256(excerpt.encode()).hexdigest()==s['excerpt_sha256'];assert s['inspected_commit']==BASE
 assert Counter(s['primary_shard'] for s in surfaces)==Counter({d['artifact_id'].removeprefix('AFQR-R2A-INVENTORY-'):len(d['surface_records']) for d in ds})
def test_search_coverage_and_index_counts():
 idx=load(INDEX);_,surfaces,hits=all_records();extensions=tuple(idx['eligible_text_extensions']);candidate=set();text_count=0
 for p in git('ls-tree','-r','--name-only',BASE).splitlines():
  if not p.endswith(extensions):continue
  raw=subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=ROOT)
  if b'\0' in raw:continue
  text_count+=1;s=raw.decode('utf8','replace').lower()
  if any(term.lower() in s for terms in idx['search_clusters'].values() for term in terms):candidate.add(p)
 accounted={s['path'] for s in surfaces}|{h['path'] for h in hits}
 assert candidate==accounted;assert idx['tracked_text_file_count']==text_count;assert idx['candidate_file_count']==len(candidate)
 assert idx['mapped_candidate_file_count']==len({s['path'] for s in surfaces});assert idx['dismissed_candidate_file_count']==len(hits);assert idx['unaccounted_candidate_file_count']==0
 for key in ('surface_kind','authority_level','currentness','generality','semantic_status'):assert idx['counts_by_'+key]==dict(sorted(Counter(s[key] for s in surfaces).items()))
def test_authority_classifications_and_narrow_safety():
 _,surfaces,hits=all_records();assert all(s['surface_kind'] in SURFACE_KINDS and s['authority_level'] in AUTH and s['currentness'] in CURRENT and s['generality'] in GENERAL and s['semantic_status'] in SEMANTIC for s in surfaces)
 for s in surfaces:
  if s['authority_level']=='current_normative':assert 'Accepted authority basis: R1' in s['inventory_notes']
  if s['authority_level']=='historical_only':assert 'Evidence only' in s['reason_this_is_or_is_not_authoritative'] and s['currentness']!='current'
  if s['surface_kind'] in {'production_schema','runtime_implementation','test_contract','fixture'}:assert s['authority_level']!='current_normative'
  if s['surface_kind'] in {'runtime_implementation','test_contract','fixture'}:assert s['generality'] in {'vertical_slice','narrow_fixture'}
 assert all(h['dismissal_reason'] in {'pure_index_or_filename_reference','citation_only','historical_reference_only','source_local_or_donor_example','nonsemantic_test_data','comment_only','unrelated_word_sense','generated_or_vendor_text','duplicate_locator_already_mapped','other_bounded_false_positive'} for h in hits)
def test_claim_coverage_drift_rules_and_links():
 route=load(ROUTING);_,surfaces,_=all_records();sids={s['surface_id'] for s in surfaces};findings={f['finding_id'] for f in route['repository_discovered_findings']};claims=route['claim_assessments'];ids=[c['claim_id'] for c in claims]
 assert ids==[f'R2-CLAIM-{i:04d}' for i in range(1,32)]
 for c in claims:
  assert c['r2a_disposition'] in DISPOSITIONS and c['primary_route'] in ROUTES;assert set(c['surface_ids'])<=sids and set(c['finding_ids'])<=findings
  assert c['r2_0_route_assessment'] in {'confirmed','narrowed','expanded','rerouted','downgraded','closed_as_already_governed','closed_as_unproven'}
  if c['r2a_disposition'] in {'implementation_conformance_only','deferred_substrate_handoff','runtime_retrofit_handoff'}:assert c['requires_doctrine_change'] is False
  if c['r2a_disposition']=='unproven_research_pressure':assert not c['primary_route'].startswith('R2B-')
  if c['r2a_disposition'] in {'doctrine_gap_proven','doctrine_conflict_proven','owner_conflict_proven'}:assert c['requires_doctrine_change'] and (c['primary_route'].startswith('R2B-') or c['primary_route']=='Astra_Doctrine_Council') and c['surface_ids']
def test_package_and_module_derivation_owner_safety():
 r=load(ROUTING);findings=r['repository_discovered_findings']
 for package,v in r['r2b_package_necessity'].items():
  proof=[f for f in findings if f['requires_doctrine_change'] and f['primary_route']==package];assert (v['status']=='required')==bool(proof)
 for module,v in r['r2b_continuity_module_necessity'].items():
  proof=[f for f in findings if f['requires_doctrine_change'] and f['candidate_r2b_module']==module];assert (v['status']=='required')==bool(proof)
 blob=json.dumps(r).lower();assert 'universal continuity owner' not in blob and 'combined truth/evidence/knowledge/sensing owner' not in blob
 assert r['gate_decision']=={'R1':'complete','R2':'active_incomplete','R2-0':'complete','R2A':'complete','R2C':'ready (no R2B package proven necessary)','R3-R6':'blocked','RT-002G':'unauthorized','temporary_evidence_deletion':'unauthorized'}
def test_tracking_counts_and_immutability():
 idx=load(INDEX);metric={'tracked_text_file_count':idx['tracked_text_file_count'],'candidate_file_count':idx['candidate_file_count'],'mapped_candidate_file_count':idx['mapped_candidate_file_count'],'dismissed_candidate_file_count':idx['dismissed_candidate_file_count'],'unaccounted_candidate_file_count':0,'surface_count':idx['surface_count'],'claim_count':31}
 report=(REV/'afqr_r2a_authority_surface_inventory_report.md').read_text();assert json.dumps(metric,sort_keys=True) in report
 for p in ('docs/decisions/current_decisions_log.md','docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md'):assert all(str(x) in (ROOT/p).read_text() for x in (821,749,26,723))
 immutable=['docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml','docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml','docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md','docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md','docs/doctrine/consolidation/afqr_world_action_sensing.md','docs/doctrine/reviews/afqr_01_20_formal_completion_review.md','docs/doctrine/reviews/afqr_r1e_source_and_vocabulary_audit.yaml','docs/doctrine/reviews/afqr_r1e_dependency_and_parity_audit.yaml','docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml','docs/doctrine/reviews/afqr_r1e_consistency_and_corpus_adequacy.yaml','docs/doctrine/reviews/afqr_r2_continuity_research_intake_packet.md','docs/doctrine/reviews/afqr_r2_continuity_research_source_manifest.yaml','docs/doctrine/reviews/afqr_r2_continuity_claim_and_owner_routing_ledger.yaml','docs/doctrine/reviews/afqr_r2_continuity_research_assimilation_report.md']
 for p in immutable:assert (ROOT/p).read_bytes()==subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=ROOT)

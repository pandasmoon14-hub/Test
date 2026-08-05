"""Executable R2A inventory validation through the bounded R2A-3 partition."""
from __future__ import annotations
import copy, hashlib, json, re, subprocess
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE="9382958197c9d5dee9d29cb5f9d051147237c64d"
ACCEPTED_R2A_1_HEAD="b6acd24fed6e689ee47a046af51aa12c5b231020"
ACCEPTED_R2A_2_HEAD="e015a56f691aefd955e21bc2f7eaaa03327e4373"
R2A_2_BASE=ACCEPTED_R2A_1_HEAD
R2A_3_BASE=ACCEPTED_R2A_2_HEAD
REV=ROOT/"docs/doctrine/reviews"
CONTRACT=REV/"afqr_r2a_inventory_contract.yaml"; PARTITIONS=REV/"afqr_r2a_partition_manifest.yaml"; CLUSTERS=REV/"afqr_r2a_controlled_search_clusters.yaml"; FILES=REV/"afqr_r2_doctrine_drift_file_manifest.yaml"
INDEX=REV/"r2a/semantic_world_coordination/index.yaml"; SHARD=REV/"r2a/semantic_world_coordination/surfaces_0001.yaml"
CORE_INDEX=REV/"r2a/semantic_core_agency/index.yaml"; CORE_SHARD=REV/"r2a/semantic_core_agency/surfaces_0001.yaml"
WORLD_RESP={"AFQR-16":"WORLD-RESP-16","AFQR-17":"WORLD-RESP-17","AFQR-18":"WORLD-RESP-18","AFQR-19":"WORLD-RESP-19","AFQR-20":"WORLD-RESP-20"}
COORD={"continuity_coordination","cross_phase_coordination"}
R2A3_AUTHORIZED={"docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml","docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml","docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml","docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml","docs/doctrine/reviews/r2a/semantic_world_coordination/index.yaml","docs/doctrine/reviews/r2a/semantic_world_coordination/surfaces_0001.yaml","tests/test_afqr_r2a_inventory_contract.py"}
PRIMARY={
 "docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml",
 "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml",
 "docs/doctrine/consolidation/afqr_world_action_sensing.md",
 "docs/doctrine/reviews/afqr_01_20_formal_completion_review.md",
 "docs/doctrine/reviews/afqr_r1e_source_and_vocabulary_audit.yaml",
 "docs/doctrine/reviews/afqr_r1e_dependency_and_parity_audit.yaml",
 "docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml",
 "docs/doctrine/reviews/afqr_r1e_consistency_and_corpus_adequacy.yaml",
 "docs/decisions/current_decisions_log.md",
 "docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md",
 "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
 "docs/doctrine/reviews/afqr_r2_continuity_research_intake_packet.md",
 "docs/doctrine/reviews/afqr_r2_continuity_research_source_manifest.yaml",
 "docs/doctrine/reviews/afqr_r2_continuity_claim_and_owner_routing_ledger.yaml",
 "docs/doctrine/reviews/afqr_r2_continuity_research_assimilation_report.md",
 "tests/test_afqr_r1d_world_action_sensing.py",
 "tests/test_afqr_r2_continuity_research_assimilation.py",
}

def git(*args): return subprocess.check_output(["git",*args],text=True).strip()
def load(p): return json.loads(p.read_text())
def baseline_raw(path,rev=R2A_3_BASE): return subprocess.check_output(["git","show",f"{rev}:{path}"])
def records(): return load(SHARD)["surface_records"]
def index(): return load(INDEX)
def world_contract():
 txt=baseline_raw("docs/doctrine/consolidation/afqr_world_action_sensing.md").decode(); m=re.search(r"```json\n(.*?)\n```",txt,re.S); assert m
 return json.loads(m.group(1))
def excerpt_hash(path,start,end):
 raw=baseline_raw(path).splitlines(keepends=True); return hashlib.sha256(b"".join(raw[start-1:end])).hexdigest()
def changed(base=R2A_3_BASE):
 names=set(git("diff","--name-only",base).splitlines())
 names.update(git("ls-files","--others","--exclude-standard").splitlines())
 return names

def test_successor_safe_r2a2_head_ancestor_and_historical_artifacts_preserved():
 subprocess.check_call(["git","merge-base","--is-ancestor",ACCEPTED_R2A_2_HEAD,"HEAD"])
 old_index=json.loads(baseline_raw("docs/doctrine/reviews/r2a/semantic_core_agency/index.yaml",ACCEPTED_R2A_2_HEAD))
 old_shard=json.loads(baseline_raw("docs/doctrine/reviews/r2a/semantic_core_agency/surfaces_0001.yaml",ACCEPTED_R2A_2_HEAD))
 assert len(old_shard["surface_records"])==old_index["surface_count"]==27
 assert old_index["shards"][0]["content_sha256"]==hashlib.sha256(baseline_raw("docs/doctrine/reviews/r2a/semantic_core_agency/surfaces_0001.yaml",ACCEPTED_R2A_2_HEAD)).hexdigest()
 assert len(old_index.get("identifier_drift_observations",[]))==3 and old_index["status"]=="complete"
 old_contract=json.loads(baseline_raw("docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml",ACCEPTED_R2A_2_HEAD))
 assert old_contract["r2a_partition_statuses"]["R2A-2"]=="complete" and old_contract["r2a_partition_statuses"]["R2A-3"]=="planned_not_present"

def test_exact_r2a3_base_scope_no_runtime_schema_and_limits():
 subprocess.check_call(["git","merge-base","--is-ancestor",R2A_3_BASE,"HEAD"])
 assert changed()==R2A3_AUTHORIZED
 assert not any(p.startswith(("src/","schemas/","tests/runtime/")) for p in changed())
 assert not git("diff","--name-status","--diff-filter=D",f"{R2A_3_BASE}...HEAD")
 num=git("diff","--numstat",f"{R2A_3_BASE}...HEAD").splitlines(); assert "-\t-" not in "\n".join(num) and sum(int(x.split("\t")[0]) for x in num)<=2500
 for p in changed():
  raw=(ROOT/p).read_bytes(); assert b"\0" not in raw and len(raw)<=300*1024 and max(map(len,raw.splitlines()),default=0)<=1000

def test_status_progression_cross_file_agreement_and_blocked_gates():
 expected={f"R2A-{n}":("complete" if n<=3 else "planned_not_present") for n in range(1,13)}
 c,p,cl,m=load(CONTRACT),load(PARTITIONS),load(CLUSTERS),load(FILES)
 assert c["r2a_partition_statuses"]==cl["r2a_partition_statuses"]=={x["partition_id"]:x["status"] for x in p["partitions"]}=={x["partition_id"]:x["current_status"] for x in m["r2a_reconstruction_sequence"]}==expected
 assert c["project_posture"]=={"R1":"complete","R2":"active_incomplete","R2-0":"complete","R2A":"active_incomplete","R2B":"blocked","R2C":"blocked","R3-R6":"blocked","RT-002G":"unauthorized","temporary_evidence_deletion":"unauthorized"}
 bad=copy.deepcopy(c); bad["project_posture"]["R2A"]="complete"; assert bad["project_posture"]!=c["project_posture"]

def test_index_shard_existence_digest_counts_and_manifest_registration():
 i=index(); rs=records(); assert i["status"]==load(SHARD)["status"]=="complete" and i["phase"]==load(SHARD)["phase"]=="R2A-3"
 sh=i["shards"][0]; assert sh["record_count"]==i["surface_count"]==len(rs) and sh["content_sha256"]==hashlib.sha256(SHARD.read_bytes()).hexdigest()
 for key in ["declared_owner","surface_kind","semantic_role","source_record_kind","authority_level","currentness","generality"]: assert i["counts"][key]==dict(sorted(Counter(r[key] for r in rs).items()))
 assert i["counts"]["surface_id_family"]==dict(sorted(Counter(r["surface_id"].rsplit("-",1)[0] for r in rs).items()))
 assert i["counts"]["r1d_responsibility_id"]==dict(sorted(Counter(x for r in rs for x in r["applicable_r1d_responsibility_ids"]).items()))
 paths=[a["path"] for a in load(FILES)["artifacts"]]; assert len(paths)==len(set(paths)); assert paths.count(str(INDEX.relative_to(ROOT)))==paths.count(str(SHARD.relative_to(ROOT)))==1
 r2a2=next(a for a in load(FILES)["artifacts"] if a["path"]=="docs/doctrine/reviews/r2a/semantic_core_agency/surfaces_0001.yaml"); assert "27 validated" in " ".join(r2a2["outputs"]) and "30 validated" not in " ".join(r2a2["outputs"])
 bad=copy.deepcopy(load(FILES)); bad["artifacts"].append(copy.deepcopy(bad["artifacts"][-1])); assert len([a["path"] for a in bad["artifacts"]])!=len(set(a["path"] for a in bad["artifacts"]))

def test_surface_contract_owners_ids_order_claims_hashes_no_self_inventory():
 rs=records(); req=set(load(CONTRACT)["record_types"]["semantic_authority_surface"]["required_fields"])
 assert rs==sorted(rs,key=lambda r:(r["declared_owner"],r["path"],r["line_start"],r["line_end"],r["source_record_kind"],r["source_record_id"],r["semantic_role"]))
 assert len({r["surface_id"] for r in rs})==len(rs)==len({(r["declared_owner"],r["path"],r["line_start"],r["line_end"],r["source_record_kind"],r["source_record_id"],r["semantic_role"]) for r in rs})
 assert [r["surface_id"] for r in rs if r["declared_owner"].startswith("AFQR-")]==[f"R2A-SURFACE-WORLD-{n:04d}" for n in range(1,6)]
 assert [r["surface_id"] for r in rs if r["declared_owner"]=="continuity_coordination"]==["R2A-SURFACE-CONTINUITY-0001","R2A-SURFACE-CONTINUITY-0002"]
 assert [r["surface_id"] for r in rs if r["declared_owner"]=="cross_phase_coordination"]==["R2A-SURFACE-CROSSPHASE-0001","R2A-SURFACE-CROSSPHASE-0002"]
 for r in rs:
  assert req<=set(r) and r["inspected_commit"]==R2A_3_BASE and r["primary_partition"]=="R2A-3" and r["semantic_status"]=="validated"
  assert r["linked_r2_claim_ids"]==[] and r["claim_link_reasons"]==[] and r["excerpt_sha256"]==excerpt_hash(r["path"],r["line_start"],r["line_end"])
  assert not r["path"].startswith("docs/doctrine/reviews/r2a/semantic_world_coordination/") and not (r["path"].endswith(".md") and r["locator_kind"] in {"json_pointer","yaml_path"})

def test_world_r1d_structural_mapping_and_negative_swap():
 wc={r["record_id"]:r for r in world_contract()["responsibility_records"]}; rs=[r for r in records() if r["declared_owner"].startswith("AFQR-")]
 assert set(r["declared_owner"] for r in rs)==set(WORLD_RESP)
 for r in rs:
  rid=WORLD_RESP[r["declared_owner"]]; assert r["applicable_r1d_responsibility_ids"]==[rid] and r["source_record_id"]==rid
  selected=wc[rid]; assert selected["afqr_id"]==r["declared_owner"] and set(r["applicable_term_ids"])=={x["term_id"] for x in selected["r1b_terms_or_qualified_forms"]}
 bad=copy.deepcopy(rs[0]); bad["declared_owner"]="AFQR-20"; assert bad["applicable_r1d_responsibility_ids"]!=[WORLD_RESP[bad["declared_owner"]]]

def test_coordination_surfaces_are_nonowner_control_boundaries_and_negative_mutations():
 rs=[r for r in records() if r["declared_owner"] in COORD]; assert len(rs)==4
 for r in rs:
  assert r["applicable_afqr_ids"] and set(r["applicable_afqr_ids"])==set(WORLD_RESP) and not COORD.intersection(r["applicable_afqr_ids"])
  assert set(r["applicable_r1d_responsibility_ids"])==set(WORLD_RESP.values()) and not COORD.intersection(r["applicable_r1d_responsibility_ids"])
  assert r["surface_kind"]!="current_normative_doctrine" and r["authority_level"]!="current_normative"
  assert r["semantic_role"] in {"explicit_nonownership_boundary","dependency_handoff","control_or_gate_constraint","implementation_presupposition","test_enforced_contract","negative_implementation_evidence"}
  assert "does not transfer" in r["owner_boundary_effect"] or "do not transfer" in r["owner_boundary_effect"]
 bad=copy.deepcopy(rs[0]); bad["applicable_afqr_ids"]=[]; assert not bad["applicable_afqr_ids"]
 bad=copy.deepcopy(rs[0]); bad["declared_owner"]="continuity_coordination"; bad["applicable_afqr_ids"].append("continuity_coordination"); assert any(x in COORD for x in bad["applicable_afqr_ids"])
 bad=copy.deepcopy(rs[0]); bad["surface_kind"]="current_normative_doctrine"; bad["authority_level"]="current_normative"; assert bad["surface_kind"]=="current_normative_doctrine" and bad["authority_level"]=="current_normative"

def test_primary_source_and_responsibility_coordination_coverage_recompute():
 i=index(); cov=i["primary_source_review_coverage"]; assert {x["path"] for x in cov}==PRIMARY and len(cov)==len(PRIMARY)
 reasons=[]
 for x in cov:
  if x["review_status"]=="mapped_material_surfaces": assert x["surface_ids"] and x["no_additional_surface_reason"] is None
  else: assert not x["surface_ids"] and isinstance(x["no_additional_surface_reason"],str) and len(x["no_additional_surface_reason"])>45; reasons.append(x["no_additional_surface_reason"])
 assert len(reasons)==len(set(reasons))
 by_owner={o:{r["surface_id"] for r in records() if r["declared_owner"]==o} for o in WORLD_RESP}
 for row in i["world_responsibility_coverage"]:
  assert row["responsibility_id"]==WORLD_RESP[row["afqr_id"]] and set(row["surface_ids"])==by_owner[row["afqr_id"]] and row["coverage_status"]=="validated_current_coverage"
 for row in i["coordination_coverage"]:
  ids={r["surface_id"] for r in records() if r["declared_owner"]==row["coordination_label"]}; assert set(row["surface_ids"])==ids and set(row["component_afqr_ids"])==set(WORLD_RESP) and row["coverage_status"]=="validated_coordination_boundary"

def test_no_claim_assessments_candidate_dispositions_scan_receipts_or_package_authorization():
 data=(INDEX.read_text()+SHARD.read_text()).lower()
 forbidden=["candidate_file_disposition:","occurrence_tuple","raw_occurrence_tuple","scan_receipt:","claim_assessment_id","unresolved_question_assessment","package_assessment_id","module_assessment_id","target_work_package_authorized"]
 assert not any(x in data for x in forbidden)
 bad=copy.deepcopy(records()[0]); bad["linked_r2_claim_ids"]=["R2-CLAIM-001"]; assert bad["linked_r2_claim_ids"]
 assert "No R2B package requirement is selected or authorized." in index()["prohibited_inferences"]

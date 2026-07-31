"""Successor-safe R2A-1 history and current R2A-2 semantic inventory checks."""
from __future__ import annotations
import fnmatch, hashlib, json, re, subprocess, unicodedata
from collections import Counter
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
R2_0_BASE="9382958197c9d5dee9d29cb5f9d051147237c64d"
ACCEPTED_R2A_1_HEAD="b6acd24fed6e689ee47a046af51aa12c5b231020"
R2A_2_BASE=ACCEPTED_R2A_1_HEAD
REV=ROOT/"docs/doctrine/reviews"
CONTRACT=REV/"afqr_r2a_inventory_contract.yaml"; PARTITIONS=REV/"afqr_r2a_partition_manifest.yaml"
CLUSTERS=REV/"afqr_r2a_controlled_search_clusters.yaml"; FILES=REV/"afqr_r2_doctrine_drift_file_manifest.yaml"
INDEX=REV/"r2a/semantic_core_agency/index.yaml"; SHARD=REV/"r2a/semantic_core_agency/surfaces_0001.yaml"
R2A1_AUTHORIZED={"docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md","docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml","docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml","docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml","docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml","tests/test_afqr_r2_continuity_research_assimilation.py","tests/test_afqr_r2a_inventory_contract.py"}
R2A2_AUTHORIZED={"docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml","docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml","docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml","docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml","docs/doctrine/reviews/r2a/semantic_core_agency/index.yaml","docs/doctrine/reviews/r2a/semantic_core_agency/surfaces_0001.yaml","tests/test_afqr_r2a_inventory_contract.py"}
OWNERS={"AFQR-01","AFQR-02","AFQR-04","AFQR-06","AFQR-07","AFQR-08","AFQR-09","AFQR-10"}
RESP={"CORE-RESP-01","CORE-RESP-02","CORE-RESP-04","CORE-RESP-06","CORE-RESP-07","CORE-RESP-08","CORE-RESP-09","AGENCY-RESP-10"}
def load(p): return json.loads(p.read_text())
def at(commit,path): return json.loads(subprocess.check_output(["git","show",f"{commit}:{path}"],text=True))
def names(a,b="HEAD"):
 out=set(subprocess.check_output(["git","diff","--name-only",f"{a}...{b}"],text=True).splitlines())
 if b=="HEAD":
  out|=set(subprocess.check_output(["git","ls-files","--others","--exclude-standard"],text=True).splitlines())
  out|={x[3:] for x in subprocess.check_output(["git","status","--porcelain","--untracked-files=no"],text=True).splitlines() if x[:2].strip()}
 return out
def blob(commit,path): return subprocess.check_output(["git","show",f"{commit}:{path}"])
def normalize(s): return " ".join(unicodedata.normalize("NFC",unicodedata.normalize("NFC",s).casefold()).split())
def boundary(s,i): return i<0 or i>=len(s) or unicodedata.category(s[i])[:1] not in {"L","N"}
def excluded(path,raw):
 if any(path==x or path.startswith(x+"/") for x in (".git","node_modules","vendor","dist","build","coverage")) or "/__pycache__/" in "/"+path+"/": return "generated_or_vendor_path"
 if b"\0" in raw: return "nul_binary"
 try: raw.decode("utf-8-sig")
 except UnicodeDecodeError: return "invalid_utf8"
def match(path,raw,clusters):
 if excluded(path,raw): return []
 out=set()
 for n,line in enumerate(raw.decode("utf-8-sig").replace("\r\n","\n").replace("\r","\n").split("\n"),1):
  line=normalize(line)
  for cluster,terms in clusters.items():
   for term in map(normalize,terms):
    start=0
    while term and (i:=line.find(term,start))>=0:
     if boundary(line,i-1) and boundary(line,i+len(term)): out.add((path,n,term,cluster))
     start=i+1
 return sorted(out)
def excerpt(raw,a,b): return hashlib.sha256(b"".join(raw.splitlines(keepends=True)[a-1:b])).hexdigest()

def test_r2a1_accepted_head_ancestry_scope_and_historical_snapshot():
 subprocess.check_call(["git","merge-base","--is-ancestor",ACCEPTED_R2A_1_HEAD,"HEAD"])
 assert names(R2_0_BASE,ACCEPTED_R2A_1_HEAD)==R2A1_AUTHORIZED
 old_contract=at(ACCEPTED_R2A_1_HEAD,"docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml")
 old_parts=at(ACCEPTED_R2A_1_HEAD,"docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml")
 assert old_contract["artifact_version"]=="0.1.0" and old_parts["artifact_version"]=="0.2.0"
 assert old_contract["r2a_partition_statuses"]["R2A-2"]=="planned_not_present"

def test_r2a1_executable_normalization_matching_hashing_and_exclusions_preserved():
 old=at(ACCEPTED_R2A_1_HEAD,"docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml")
 for v in old["reference_vectors"]:
  raw=bytes.fromhex(v["raw_hex"]) if "raw_hex" in v else json.loads('"'+v["raw_utf8_escaped"]+'"').encode()
  if "expected_exclusion" in v: assert excluded(v["path"],raw)==v["expected_exclusion"]
  else: assert [list(x) for x in match(v["path"],raw,v["terms_by_cluster"])]==v["expected_tuples"]
 raw=b"first\r\nsecond\nlast"; assert excerpt(raw,2,3)==hashlib.sha256(b"second\nlast").hexdigest()

def test_exact_r2a2_base_ancestry_authorization_and_no_runtime_schema_changes():
 subprocess.check_call(["git","merge-base","--is-ancestor",R2A_2_BASE,"HEAD"])
 assert names(R2A_2_BASE)==R2A2_AUTHORIZED
 assert not any(p.startswith(("src/","schemas/","tests/runtime/")) for p in names(R2A_2_BASE))

def test_partition_status_progression_and_cross_file_agreement():
 expected={f"R2A-{n}":("complete" if n<=2 else "planned_not_present") for n in range(1,13)}
 c=load(CONTRACT); s=load(CLUSTERS); p=load(PARTITIONS); m=load(FILES)
 assert c["r2a_partition_statuses"]==s["r2a_partition_statuses"]=={x["partition_id"]:x["status"] for x in p["partitions"]}==expected
 assert {x["partition_id"]:x["current_status"] for x in m["r2a_reconstruction_sequence"]}==expected
 assert c["project_posture"]=={"R1":"complete","R2":"active_incomplete","R2-0":"complete","R2A":"active_incomplete","R2B":"blocked","R2C":"blocked","R3-R6":"blocked","RT-002G":"unauthorized","temporary_evidence_deletion":"unauthorized"}

def test_index_shard_structure_required_fields_and_controlled_values():
 c=load(CONTRACT); i=load(INDEX); records=load(SHARD)["surface_records"]
 required=set(c["record_types"]["semantic_authority_surface"]["required_fields"])
 assert i["status"]=="complete" and i["surface_count"]==len(records)>0
 for r in records:
  assert required<=set(r) and r["primary_partition"]=="R2A-2" and r["inspected_commit"]==R2A_2_BASE
  assert r["excerpt_hash_algorithm"]=="sha256_git_blob_raw_line_slice_v1" and r["semantic_status"]=="validated"
  assert r["surface_kind"] in c["controlled_values"]["surface_kinds"] and r["authority_level"] in c["controlled_values"]["authority_levels"]
  assert r["currentness"] in c["controlled_values"]["currentness_values"] and r["generality"] in c["controlled_values"]["generality_values"]
  assert (r["locator_value"] is None)==(r["locator_kind"]=="line_range_only")

def test_order_ids_uniqueness_owners_responsibilities_and_no_coordination_owner():
 records=load(SHARD)["surface_records"]
 assert records==sorted(records,key=lambda r:(r["declared_owner"],r["path"],r["line_start"],r["line_end"],r["surface_kind"]))
 assert len({r["surface_id"] for r in records})==len(records)
 assert len({(r["declared_owner"],r["path"],r["line_start"],r["line_end"],r["semantic_summary"]) for r in records})==len(records)
 assert {r["declared_owner"] for r in records}==OWNERS
 assert {r["applicable_r1d_responsibility_ids"][0] for r in records}==RESP and all(len(r["applicable_r1d_responsibility_ids"])==1 for r in records)
 core=[r for r in records if r["declared_owner"]!="AFQR-10"]; agency=[r for r in records if r["declared_owner"]=="AFQR-10"]
 assert [r["surface_id"] for r in core]==[f"R2A-SURFACE-CORE-{n:04d}" for n in range(1,len(core)+1)]
 assert [r["surface_id"] for r in agency]==[f"R2A-SURFACE-AGENCY-{n:04d}" for n in range(1,len(agency)+1)]

def test_baseline_paths_hashes_locators_and_material_semantic_relevance():
 records=load(SHARD)["surface_records"]
 for r in records:
  raw=blob(R2A_2_BASE,r["path"]); lines=raw.splitlines(keepends=True)
  assert 0<r["line_start"]<=r["line_end"]<=len(lines)
  assert excerpt(raw,r["line_start"],r["line_end"])==r["excerpt_sha256"]
  bounded=b"".join(lines[r["line_start"]-1:r["line_end"]]).decode()
  # Reject owner-name mentions: the accepted bounded proposition must state both ownership and exclusion.
  assert '"owned_concerns"' in bounded and '"explicit_nonowned_concerns"' in bounded
  assert not r["path"].startswith("docs/doctrine/reviews/r2a/semantic_core_agency/")

def _ids(path,pattern): return set(re.findall(pattern,blob(R2A_2_BASE,path).decode()))
def test_identifier_integrity_primary_applicability_and_empty_claim_links():
 terms=_ids("docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml",r"TERM-\d{3}")
 inv=_ids("docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml",r"INV-\d{3}")
 dep=_ids("docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml",r"DEP-\d{3}")
 sub=_ids("docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml",r"SUBSTRATE-[A-Z0-9-]+")
 for r in load(SHARD)["surface_records"]:
  assert r["declared_owner"] in r["applicable_afqr_ids"] and set(r["applicable_term_ids"])<=terms
  assert set(r["applicable_invariant_ids"])<=inv and set(r["applicable_dependency_ids"])<=dep and set(r["applicable_substrate_ids"])<=sub
  assert r["linked_r2_claim_ids"]==r["claim_link_reasons"]==[]

def test_owner_current_coverage_index_counts_digest_and_coverage_recompute():
 i=load(INDEX); records=load(SHARD)["surface_records"]
 assert all(any(r["declared_owner"]==o and r["surface_kind"] in {"current_normative_doctrine","accepted_decision"} for r in records) for o in OWNERS)
 for field in ("declared_owner","surface_kind","authority_level","currentness","generality"):
  assert i["counts"][field]==dict(sorted(Counter(r[field] for r in records).items()))
 assert i["counts"]["r1d_responsibility_id"]==dict(sorted(Counter(r["applicable_r1d_responsibility_ids"][0] for r in records).items()))
 sh=i["shards"][0]; assert sh["record_count"]==len(records) and sh["content_sha256"]==hashlib.sha256(SHARD.read_bytes()).hexdigest()
 coverage=i["responsibility_coverage"]; assert {x["responsibility_id"] for x in coverage}==RESP
 byid={r["surface_id"]:r for r in records}
 for c in coverage:
  assert c["afqr_id"] in OWNERS and c["surface_ids"] and set(c["surface_ids"])<=set(byid)
  assert set(c["current_normative_surface_ids"])=={s for s in c["surface_ids"] if byid[s]["surface_kind"] in {"current_normative_doctrine","accepted_decision"}}

def test_no_later_partition_records_or_prohibited_assessments():
 data=(INDEX.read_text()+SHARD.read_text()).lower()
 prohibited=("candidate_file_disposition","scan_receipt_id","assessment_outcome","unresolved_question_id","package_assessment_id","module_assessment_id","occurrence_tuple")
 assert not any(x in data for x in prohibited)
 assert "repository-wide semantic completeness is not claimed" in data and "does not adopt or modify doctrine" in data

def test_containment_limits_no_deletions_binaries_oversize_or_long_lines():
 assert not subprocess.check_output(["git","diff","--name-status","--diff-filter=D",R2A_2_BASE],text=True).strip()
 num=subprocess.check_output(["git","diff","--numstat",R2A_2_BASE],text=True).splitlines(); assert sum(int(x.split("\t")[0]) for x in num)<=2500
 for p in names(R2A_2_BASE):
  raw=(ROOT/p).read_bytes(); assert b"\0" not in raw and len(raw)<=300*1024 and max(map(len,raw.splitlines()),default=0)<=1000

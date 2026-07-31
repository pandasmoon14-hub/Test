"""Executable R2A-1 contract, discovery, partition, and scope validation."""
from __future__ import annotations
import fnmatch, hashlib, json, re, subprocess, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE="9382958197c9d5dee9d29cb5f9d051147237c64d"
REV=ROOT/"docs/doctrine/reviews"; CONTRACT=REV/"afqr_r2a_inventory_contract.yaml"; PARTITIONS=REV/"afqr_r2a_partition_manifest.yaml"; CLUSTERS=REV/"afqr_r2a_controlled_search_clusters.yaml"; FILES=REV/"afqr_r2_doctrine_drift_file_manifest.yaml"; PLAN=ROOT/"docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md"
AUTHORIZED={"docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md","docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml","docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml","docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml","docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml","tests/test_afqr_r2_continuity_research_assimilation.py","tests/test_afqr_r2a_inventory_contract.py"}
def load(p): return json.loads(p.read_text())
def changed(): return set(subprocess.check_output(["git","diff","--name-only",f"{BASE}...HEAD"],text=True).splitlines())|{x[3:] for x in subprocess.check_output(["git","status","--porcelain"],text=True).splitlines() if x[:2].strip()}
def normalize(s): return " ".join(unicodedata.normalize("NFC",unicodedata.normalize("NFC",s).casefold()).split())
def boundary(s,i): return i<0 or i>=len(s) or unicodedata.category(s[i])[:1] not in {"L","N"}
def excluded(path,raw):
 if any(path==x or path.startswith(x+"/") for x in (".git","node_modules","vendor","dist","build","coverage")) or "/__pycache__/" in "/"+path+"/": return "generated_or_vendor_path"
 if b"\0" in raw: return "nul_binary"
 try: raw.decode("utf-8-sig")
 except UnicodeDecodeError: return "invalid_utf8"
 return None
def match(path,raw,terms_by_cluster):
 if excluded(path,raw): return []
 text=raw.decode("utf-8-sig").replace("\r\n","\n").replace("\r","\n"); out=set()
 for number,line in enumerate(text.split("\n"),1):
  line=normalize(line)
  for cluster,terms in terms_by_cluster.items():
   for term in terms:
    term=normalize(term); start=0
    while term and (at:=line.find(term,start))>=0:
     if boundary(line,at-1) and boundary(line,at+len(term)): out.add((path,number,term,cluster))
     start=at+1
 return sorted(out)
def escape(v): return str(v).replace("\\","\\\\").replace("\t","\\t").replace("\r","\\r").replace("\n","\\n")
def serialize(rows):
 records=sorted("\t".join(escape(v) for v in row) for row in rows)
 return (("\n".join(records)+"\n") if records else "").encode()
def excerpt_hash(raw,start,end): return hashlib.sha256(b"".join(raw.splitlines(keepends=True)[start-1:end])).hexdigest()
def assign(path):
 if excluded(path,b"") == "generated_or_vendor_path": return None
 if path.startswith(("docs/doctrine/control/","docs/doctrine/consolidation/","docs/doctrine/operations/","docs/doctrine/schema/","docs/doctrine/world/","docs/decisions/")): return "R2A-4"
 if path.startswith("docs/doctrine/reviews/") or (path.startswith("docs/doctrine/") and "/" not in path[len("docs/doctrine/"):] and path.endswith((".yaml",".md"))): return "R2A-5"
 if path.startswith(("src/","schemas/","tests/runtime/")) or fnmatch.fnmatchcase(path,"tests/test_runtime_*.py") or (path.startswith("tests/test_") and "runtime" in path and path.endswith(".py")): return "R2A-6"
 return "R2A-7"
def test_exact_base_and_seven_file_scope():
 assert subprocess.check_output(["git","merge-base",BASE,"HEAD"],text=True).strip()==BASE; assert changed()==AUTHORIZED
 assert not any(p.startswith(("src/","schemas/","tests/runtime/")) for p in changed())
def test_type_specific_vocabularies_and_controls_resolve():
 d=load(CONTRACT); cv=d["controlled_values"]
 expected={"artifact_statuses","partition_statuses","semantic_surface_statuses","verification_statuses","claim_assessment_outcomes","question_assessment_outcomes","package_assessment_outcomes","module_assessment_outcomes"}; assert expected<=set(cv)
 assert not {"statuses","assessment_outcomes"}&set(cv)
 refs={"claim_assessment":"claim_assessment_outcomes","unresolved_question_assessment":"question_assessment_outcomes","package_assessment":"package_assessment_outcomes","module_assessment":"module_assessment_outcomes"}
 for name,vocab in refs.items(): assert d["record_types"][name]["field_controls"]["assessment_outcome"]==f"controlled_values.{vocab}"
 assert d["record_types"]["semantic_authority_surface"]["field_controls"]["semantic_status"]=="controlled_values.semantic_surface_statuses"
 assert d["record_types"]["scan_receipt"]["field_controls"]["verification_status"]=="controlled_values.verification_statuses"
 for record in d["record_types"].values():
  assert record["required_fields"] and record["field_controls"] and record["validation_rules"] and record["prohibited_uses"]
  for ref in record["field_controls"].values():
   if isinstance(ref,str) and ref.startswith("controlled_values."): assert ref.split(".",1)[1] in cv
 assert d["record_types"]["module_assessment"]["prohibited_uses"]==["Do not invent a continuity, correction, branch, replay, or cross-phase super-owner."]
def test_candidate_controls_owner_references_and_integrity():
 d=load(CONTRACT); cv=d["controlled_values"]; c=d["record_types"]["candidate_file_disposition"]
 assert "generated_or_vendor_text" not in cv["dispositions"]
 assert c["field_controls"]|{"source_local_pressure_class":"controlled_values.source_local_pressure_classes","authority_effect":"controlled_values.candidate_authority_effects","pressure_route":"controlled_values.pressure_routes"}==c["field_controls"]
 assert d["owner_reference"]["coordination_labels_are_owners"] is False and "invented" in d["owner_reference"]["prohibited"]
 assert set(d["referential_integrity"])=={"AFQR ID","R1D responsibility ID","TERM ID","invariant ID","dependency/edge ID","substrate ID"}
def test_candidate_universe_and_exclusions():
 u=load(CONTRACT)["candidate_file_universe"]; assert len(u["processing_order"])==5 and "not candidate files" in u["excluded_files"]
 assert excluded("vendor/x.txt",b"truth")=="generated_or_vendor_path"; assert excluded("x",b"a\0b")=="nul_binary"; assert excluded("x",b"\xff")=="invalid_utf8"; assert excluded("x",b"ok") is None
def test_executable_discovery_vectors():
 vectors=load(CLUSTERS)["reference_vectors"]
 for v in vectors:
  raw=bytes.fromhex(v["raw_hex"]) if "raw_hex" in v else json.loads('"'+v["raw_utf8_escaped"]+'"').encode()
  if "expected_exclusion" in v: assert excluded(v["path"],raw)==v["expected_exclusion"]
  else: assert [list(x) for x in match(v["path"],raw,v["terms_by_cluster"])]==v["expected_tuples"]
 # CRLF/LF equivalence, underscore/hyphen/slash boundaries, repeated-term dedup, and two clusters are exercised above.
 assert match("x",b"truth truth\n",{"a":["truth"]})==[("x",1,"truth","a")]
 assert match("x",b"truth\n",{"a":["truth"],"b":["truth"]})==[("x",1,"truth","a"),("x",1,"truth","b")]
def test_tuple_serialization_order_escaping_digest_and_empty_stream():
 rows=[("a\\b",2,"truth","z"),("a\tb",1,"belief","a")]; stream=serialize(rows)
 assert stream==b"a\\\\b\t2\ttruth\tz\na\\tb\t1\tbelief\ta\n"
 assert hashlib.sha256(stream).hexdigest()=="1adefdfe52d501aff9865834d458df38c04b52ba8d66b8ce44a5133ed5b289a4"
 assert serialize([])==b"" and hashlib.sha256(serialize([])).hexdigest()=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
def test_exact_excerpt_hash_vectors_and_locator_controls():
 raw=b"first\r\nsecond\nlast"; assert excerpt_hash(raw,2,3)==hashlib.sha256(b"second\nlast").hexdigest(); assert excerpt_hash(raw,1,1)==hashlib.sha256(b"first\r\n").hexdigest()
 d=load(CONTRACT); s=d["record_types"]["semantic_authority_surface"]
 assert {"locator_kind","locator_value","line_start","line_end","excerpt_hash_algorithm","excerpt_sha256"}<=set(s["required_fields"])
 assert s["field_controls"]["excerpt_hash_algorithm"]=="literal.sha256_git_blob_raw_line_slice_v1"
 assert set(d["controlled_values"]["locator_kinds"])=={"heading","symbol","json_pointer","yaml_path","line_range_only"}
def test_receipt_provenance_is_complete():
 required=set(load(CONTRACT)["record_types"]["scan_receipt"]["required_fields"])
 assert required=={"receipt_id","inspected_baseline_commit","controlled_search_artifact_id","controlled_search_artifact_version","controlled_search_artifact_sha256","eligible_file_count","excluded_file_count_by_reason","excluded_path_digest","candidate_file_count","occurrence_count","count_by_term","count_by_cluster","tuple_stream_sha256","verification_status"}
def test_partition_assignment_precedence_and_totality():
 d=load(PARTITIONS); rules=d["ownership_rules"]; assert rules["exclusions_before_assignment"] is True and rules["disposition_precedence"]==["R2A-4","R2A-5","R2A-6","R2A-7"]
 vectors={"docs/doctrine/control/a.md":"R2A-4","docs/doctrine/reviews/a.yaml":"R2A-5","docs/doctrine/root.yaml":"R2A-5","src/a.py":"R2A-6","schemas/a.json":"R2A-6","tests/runtime/a.py":"R2A-6","tests/test_runtime_x.py":"R2A-6","examples/a.md":"R2A-7","vendor/a.py":None}
 assert {p:assign(p) for p in vectors}==vectors
 for path in subprocess.check_output(["git","ls-tree","-r","--name-only",BASE],text=True).splitlines():
  if excluded(path,b"")=="generated_or_vendor_path": assert assign(path) is None
  else: assert assign(path) in {"R2A-4","R2A-5","R2A-6","R2A-7"}
def test_twelve_partitions_dependencies_shards_and_no_coordination_owner():
 d=load(PARTITIONS); rows=d["partitions"]; assert d["partition_count"]==len(rows)==12; assert [x["partition_id"] for x in rows]==[f"R2A-{n}" for n in range(1,13)]
 seen={"R2-0"}
 for x in rows: assert set(x["dependency_partitions"])<=seen and x["maximum_changed_files"]<=7 and x["maximum_additions"]<=2500; seen.add(x["partition_id"])
 assert d["ownership_rules"]["coordination_domain_ownership"]==[] and "bounded shards" in d["ownership_rules"]["sharding"]
 assert "Only R2A-12 may mark R2A complete" in rows[-1]["gate_effect"] and "cannot begin R2B" in rows[-2]["gate_effect"]
def test_manifest_statuses_sequence_and_cross_file_agreement():
 m=load(FILES); seq=m["r2a_reconstruction_sequence"]; assert len(seq)==12 and all(set(x)=={"partition_id","current_status"} for x in seq)
 planned=[x for x in m["artifacts"] if x.get("phase","").startswith("R2A-") and x["phase"]!="R2A-1"]; assert len(planned)==11
 assert all("status" not in x and x["current_status"]=="planned_not_present" and "index" in x["path"] or x["phase"]=="R2A-12" for x in planned)
 assert load(PARTITIONS)["partition_count"]==len(seq)==12 and "twelve bounded pull requests" in PLAN.read_text()
def test_successor_safe_history_current_posture_and_nonauthority():
 history=(ROOT/"tests/test_afqr_r2_continuity_research_assimilation.py").read_text(); assert 'ACCEPTED_R2_0_HEAD="9382958197c9d5dee9d29cb5f9d051147237c64d"' in history and 'f"{BASE}...{ACCEPTED_R2_0_HEAD}"' in history and 'git","show",f"{ACCEPTED_R2_0_HEAD}' in history
 d=load(CONTRACT); assert d["project_posture"]=={"R1":"complete","R2":"active_incomplete","R2-0":"complete","R2A":"active_incomplete","R2B":"blocked","R2C":"blocked","R3-R6":"blocked","RT-002G":"unauthorized","temporary_evidence_deletion":"unauthorized"}
 plan=PLAN.read_text(); assert "No compact reconstruction or isolated local commit is repository authority." in plan and "No-action and existing-owner outcomes are lawful" in plan
 assert not any(k in d for k in ("semantic_surfaces","candidate_files","claim_assessments","question_assessments"))
def test_no_deletions_binaries_oversize_or_overlong_lines():
 assert not subprocess.check_output(["git","diff","--name-status","--diff-filter=D",BASE],text=True).strip(); assert len(changed())==7
 for p in changed():
  raw=(ROOT/p).read_bytes(); assert b"\0" not in raw and len(raw)<=300*1024 and max(map(len,raw.splitlines()),default=0)<=1000
 num=subprocess.check_output(["git","diff","--numstat",BASE],text=True); assert "-\t-\t" not in num and sum(int(x.split("\t")[0]) for x in num.splitlines())<=2500

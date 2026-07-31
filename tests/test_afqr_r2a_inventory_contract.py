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
def serialize_exclusions(records): return serialize((path,reason) for path,reason in records)
def excerpt_hash(raw,start,end): return hashlib.sha256(b"".join(raw.splitlines(keepends=True)[start-1:end])).hexdigest()
def locator_valid(kind,value): return value is None if kind=="line_range_only" else isinstance(value,str) and bool(value.strip())
def pattern_matches(path,pattern):
 if pattern=="**": return True
 if pattern.startswith("**/") and pattern.endswith("/**"):
  segment=pattern[3:-3]; return segment in path.split("/")[:-1]
 if pattern.endswith("/**") and "*" not in pattern[:-3]: return path.startswith(pattern[:-3]+"/")
 if "/" in pattern and "**" not in pattern:
  return path.count("/")==pattern.count("/") and fnmatch.fnmatchcase(path,pattern)
 raise ValueError(f"unsupported manifest pattern: {pattern}")
def assign(path,rules=None):
 rules=rules or load(PARTITIONS)["ownership_rules"]
 if any(pattern_matches(path,p) for p in rules["generated_vendor_exclusion_patterns"]): return None
 for partition in rules["disposition_precedence"]:
  if any(pattern_matches(path,p) for p in rules["disposition_rules"].get(partition,[])): return partition
 raise ValueError(f"unassigned eligible path: {path}")
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
 assert match("x",b"Truth\r\nvalid  time\r\n",{"a":["truth","valid time"]})==match("x",b"Truth\nvalid  time\n",{"a":["truth","valid time"]})
 assert match("x",b"truth truth\n",{"a":["truth"]})==[("x",1,"truth","a")]
 assert match("x",b"truth\n",{"a":["truth"],"b":["truth"]})==[("x",1,"truth","a"),("x",1,"truth","b")]
def test_tuple_serialization_order_escaping_digest_and_empty_stream():
 rows=[("a\\b",2,"truth","z"),("a\tb",1,"belief","a")]; stream=serialize(rows)
 assert stream==b"a\\\\b\t2\ttruth\tz\na\\tb\t1\tbelief\ta\n"
 assert hashlib.sha256(stream).hexdigest()=="1adefdfe52d501aff9865834d458df38c04b52ba8d66b8ce44a5133ed5b289a4"
 assert serialize([])==b"" and hashlib.sha256(serialize([])).hexdigest()=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
def test_exclusion_stream_vectors_order_reason_escaping_and_empty():
 a=[("z.txt","invalid_utf8"),("a\tb","nul_binary")]; assert serialize_exclusions(a)==serialize_exclusions(list(reversed(a)))==b"a\\tb\tnul_binary\nz.txt\tinvalid_utf8\n"
 assert hashlib.sha256(serialize_exclusions([("x","nul_binary")])).digest()!=hashlib.sha256(serialize_exclusions([("x","invalid_utf8")])).digest()
 assert serialize_exclusions([])==b"" and hashlib.sha256(serialize_exclusions([])).hexdigest()=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
 algorithm=load(CONTRACT)["canonical_exclusion_receipt_algorithm"]; assert algorithm["record_fields"]==["path","exclusion_reason"] and "both path and exclusion reason" in algorithm["digest_meaning"]
def test_exact_excerpt_hash_vectors_and_locator_controls():
 raw=b"first\r\nsecond\nlast"; assert excerpt_hash(raw,2,3)==hashlib.sha256(b"second\nlast").hexdigest(); assert excerpt_hash(raw,1,1)==hashlib.sha256(b"first\r\n").hexdigest()
 d=load(CONTRACT); s=d["record_types"]["semantic_authority_surface"]
 assert {"locator_kind","locator_value","line_start","line_end","excerpt_hash_algorithm","excerpt_sha256"}<=set(s["required_fields"])
 assert s["field_controls"]["excerpt_hash_algorithm"]=="literal.sha256_git_blob_raw_line_slice_v1"
 assert set(d["controlled_values"]["locator_kinds"])=={"heading","symbol","json_pointer","yaml_path","line_range_only"}
 assert locator_valid("line_range_only",None) and not locator_valid("line_range_only","x")
 assert all(locator_valid(kind,"value") and not locator_valid(kind,None) and not locator_valid(kind," ") for kind in ("heading","symbol","json_pointer","yaml_path"))
def test_receipt_provenance_is_complete():
 required=set(load(CONTRACT)["record_types"]["scan_receipt"]["required_fields"])
 assert required=={"receipt_id","inspected_baseline_commit","controlled_search_artifact_id","controlled_search_artifact_version","controlled_search_artifact_path","controlled_search_artifact_hash_algorithm","controlled_search_artifact_sha256","eligible_file_count","excluded_file_count_by_reason","excluded_path_digest","excluded_path_digest_algorithm","candidate_file_count","occurrence_count","count_by_term","count_by_cluster","tuple_stream_sha256","verification_status"}
 assert load(CONTRACT)["controlled_search_artifact_hash_algorithm"]["algorithm_id"]=="sha256_exact_git_blob_bytes_v1"
def test_partition_assignment_precedence_and_totality_and_mutations():
 d=load(PARTITIONS); rules=d["ownership_rules"]; assert rules["exclusions_before_assignment"] is True and rules["disposition_precedence"]==["R2A-4","R2A-5","R2A-6","R2A-7"]
 vectors={"docs/doctrine/control/a.md":"R2A-4","docs/doctrine/reviews/a.yaml":"R2A-5","docs/doctrine/root.yaml":"R2A-5","src/a.py":"R2A-6","schemas/a.json":"R2A-6","tests/runtime/a.py":"R2A-6","tests/test_runtime_x.py":"R2A-6","examples/a.md":"R2A-7","vendor/a.py":None}; assert {p:assign(p) for p in vectors}==vectors
 import copy
 changed=copy.deepcopy(rules); changed["disposition_rules"]["R2A-4"].append("examples/**"); assert assign("examples/a.md",changed)=="R2A-4"
 no_fallback=copy.deepcopy(rules); no_fallback["disposition_rules"]["R2A-7"]=[]
 try: assign("unowned/a.txt",no_fallback); assert False, "missing fallback must fail"
 except ValueError: pass
 overlap=copy.deepcopy(rules); overlap["disposition_rules"]["R2A-5"].append("docs/doctrine/control/**"); assert assign("docs/doctrine/control/a.md",overlap)=="R2A-4"
 overlap["disposition_precedence"]=["R2A-5","R2A-4","R2A-6","R2A-7"]; assert assign("docs/doctrine/control/a.md",overlap)=="R2A-5"
 excluded_first=copy.deepcopy(rules); excluded_first["disposition_rules"]["R2A-4"].append("vendor/**"); assert assign("vendor/a.py",excluded_first) is None
 for path in subprocess.check_output(["git","ls-tree","-r","--name-only",BASE],text=True).splitlines(): assert assign(path) is None or assign(path) in {"R2A-4","R2A-5","R2A-6","R2A-7"}
def test_twelve_partitions_dependencies_shards_and_no_coordination_owner():
 d=load(PARTITIONS); rows=d["partitions"]; assert d["partition_count"]==len(rows)==12; assert [x["partition_id"] for x in rows]==[f"R2A-{n}" for n in range(1,13)]
 seen={"R2-0"}
 for x in rows: assert set(x["dependency_partitions"])<=seen and x["maximum_changed_files"]<=7 and x["maximum_additions"]<=2500; seen.add(x["partition_id"])
 assert d["ownership_rules"]["coordination_domain_ownership"]==[] and "bounded shards" in d["ownership_rules"]["sharding"]
 assert "Only R2A-12 may mark R2A complete" in rows[-1]["gate_effect"] and "cannot begin R2B" in rows[-2]["gate_effect"]
 for row in rows:
  paths=row.get("candidate_path_patterns",row.get("planned_artifact_paths")); assert paths and all("planned artifact family" not in path and not path.startswith("/") and " " not in path for path in paths)
  assert ("candidate_path_patterns" in row)==(row["partition_id"] in {"R2A-4","R2A-5","R2A-6","R2A-7"})
def test_manifest_statuses_sequence_and_cross_file_agreement():
 m=load(FILES); seq=m["r2a_reconstruction_sequence"]; assert len(seq)==12 and all(set(x)=={"partition_id","current_status"} for x in seq)
 planned=[x for x in m["artifacts"] if x.get("phase","").startswith("R2A-") and x["phase"]!="R2A-1"]; assert len(planned)==11
 for number,x in enumerate(planned,2):
  assert "status" not in x; assert x["current_status"]=="planned_not_present"; assert x["phase"]==f"R2A-{number}"; assert not x["path"].startswith("/") and ("/index." in x["path"] or number==12)
 partitions=load(PARTITIONS); contract=load(CONTRACT); clusters=load(CLUSTERS); ids=[f"R2A-{n}" for n in range(1,13)]; statuses={x["partition_id"]:x["current_status"] for x in seq}
 assert contract["partition_count"]==clusters["partition_count"]==partitions["partition_count"]==len(seq)==12
 assert contract["r2a_partition_ids"]==clusters["r2a_partition_ids"]==[x["partition_id"] for x in partitions["partitions"]]==ids
 assert contract["r2a_partition_statuses"]==clusters["r2a_partition_statuses"]=={x["partition_id"]:x["status"] for x in partitions["partitions"]}==statuses
 planned_by_phase={x["phase"]:x["path"] for x in planned}; partition_paths={x["partition_id"]:x["planned_artifact_paths"][0] for x in partitions["partitions"] if x["partition_id"] in planned_by_phase}; assert partition_paths==planned_by_phase
 plan=PLAN.read_text(); assert "twelve bounded pull requests" in plan and all(x in plan for x in ("`R2A=active_incomplete`","`R2B=blocked`","`R2C=blocked`","`R3–R6=blocked`"))
 assert [x["partition_id"] for x in partitions["partitions"] if "mark R2A complete" in x["gate_effect"]]==["R2A-12"] and "cannot begin R2B" in partitions["partitions"][-2]["gate_effect"]
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

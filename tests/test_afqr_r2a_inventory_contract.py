"""Executable R2A-1 contract, discovery, partition, and scope validation."""
from __future__ import annotations
import fnmatch, hashlib, json, re, subprocess, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE="9382958197c9d5dee9d29cb5f9d051147237c64d"; ACCEPTED_R2A_1_HEAD="b6acd24fed6e689ee47a046af51aa12c5b231020"; R2A_2_BASE=ACCEPTED_R2A_1_HEAD
REV=ROOT/"docs/doctrine/reviews"; CONTRACT=REV/"afqr_r2a_inventory_contract.yaml"; PARTITIONS=REV/"afqr_r2a_partition_manifest.yaml"; CLUSTERS=REV/"afqr_r2a_controlled_search_clusters.yaml"; FILES=REV/"afqr_r2_doctrine_drift_file_manifest.yaml"; PLAN=ROOT/"docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md"
AUTHORIZED={"docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md","docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml","docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml","docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml","docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml","tests/test_afqr_r2_continuity_research_assimilation.py","tests/test_afqr_r2a_inventory_contract.py"}
def histload(p): return json.loads(subprocess.check_output(["git","show",f"{ACCEPTED_R2A_1_HEAD}:{p.relative_to(ROOT)}"],text=True))
def changed(): return set(subprocess.check_output(["git","diff","--name-only",f"{BASE}...{ACCEPTED_R2A_1_HEAD}"],text=True).splitlines())
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
 rules=rules or histload(PARTITIONS)["ownership_rules"]
 if any(pattern_matches(path,p) for p in rules["generated_vendor_exclusion_patterns"]): return None
 for partition in rules["disposition_precedence"]:
  if any(pattern_matches(path,p) for p in rules["disposition_rules"].get(partition,[])): return partition
 raise ValueError(f"unassigned eligible path: {path}")
def test_exact_base_and_seven_file_scope():
 assert subprocess.check_output(["git","merge-base",BASE,ACCEPTED_R2A_1_HEAD],text=True).strip()==BASE; assert changed()==AUTHORIZED; subprocess.check_call(["git","merge-base","--is-ancestor",ACCEPTED_R2A_1_HEAD,"HEAD"])
 assert not any(p.startswith(("src/","schemas/","tests/runtime/")) for p in changed())
def test_type_specific_vocabularies_and_controls_resolve():
 d=histload(CONTRACT); cv=d["controlled_values"]
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
 d=histload(CONTRACT); cv=d["controlled_values"]; c=d["record_types"]["candidate_file_disposition"]
 assert "generated_or_vendor_text" not in cv["dispositions"]
 assert c["field_controls"]|{"source_local_pressure_class":"controlled_values.source_local_pressure_classes","authority_effect":"controlled_values.candidate_authority_effects","pressure_route":"controlled_values.pressure_routes"}==c["field_controls"]
 assert d["owner_reference"]["coordination_labels_are_owners"] is False and "invented" in d["owner_reference"]["prohibited"]
 assert set(d["referential_integrity"])=={"AFQR ID","R1D responsibility ID","TERM ID","invariant ID","dependency/edge ID","substrate ID"}
def test_candidate_universe_and_exclusions():
 u=histload(CONTRACT)["candidate_file_universe"]; assert len(u["processing_order"])==5 and "not candidate files" in u["excluded_files"]
 assert excluded("vendor/x.txt",b"truth")=="generated_or_vendor_path"; assert excluded("x",b"a\0b")=="nul_binary"; assert excluded("x",b"\xff")=="invalid_utf8"; assert excluded("x",b"ok") is None
def test_executable_discovery_vectors():
 vectors=histload(CLUSTERS)["reference_vectors"]
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
 algorithm=histload(CONTRACT)["canonical_exclusion_receipt_algorithm"]; assert algorithm["record_fields"]==["path","exclusion_reason"] and "both path and exclusion reason" in algorithm["digest_meaning"]
def test_exact_excerpt_hash_vectors_and_locator_controls():
 raw=b"first\r\nsecond\nlast"; assert excerpt_hash(raw,2,3)==hashlib.sha256(b"second\nlast").hexdigest(); assert excerpt_hash(raw,1,1)==hashlib.sha256(b"first\r\n").hexdigest()
 d=histload(CONTRACT); s=d["record_types"]["semantic_authority_surface"]
 assert {"locator_kind","locator_value","line_start","line_end","excerpt_hash_algorithm","excerpt_sha256"}<=set(s["required_fields"])
 assert s["field_controls"]["excerpt_hash_algorithm"]=="literal.sha256_git_blob_raw_line_slice_v1"
 assert set(d["controlled_values"]["locator_kinds"])=={"heading","symbol","json_pointer","yaml_path","line_range_only"}
 assert locator_valid("line_range_only",None) and not locator_valid("line_range_only","x")
 assert all(locator_valid(kind,"value") and not locator_valid(kind,None) and not locator_valid(kind," ") for kind in ("heading","symbol","json_pointer","yaml_path"))
def test_receipt_provenance_is_complete():
 required=set(histload(CONTRACT)["record_types"]["scan_receipt"]["required_fields"])
 assert required=={"receipt_id","inspected_baseline_commit","controlled_search_artifact_id","controlled_search_artifact_version","controlled_search_artifact_path","controlled_search_artifact_hash_algorithm","controlled_search_artifact_sha256","eligible_file_count","excluded_file_count_by_reason","excluded_path_digest","excluded_path_digest_algorithm","candidate_file_count","occurrence_count","count_by_term","count_by_cluster","tuple_stream_sha256","verification_status"}
 assert histload(CONTRACT)["controlled_search_artifact_hash_algorithm"]["algorithm_id"]=="sha256_exact_git_blob_bytes_v1"
def test_partition_assignment_precedence_and_totality_and_mutations():
 d=histload(PARTITIONS); rules=d["ownership_rules"]; assert rules["exclusions_before_assignment"] is True and rules["disposition_precedence"]==["R2A-4","R2A-5","R2A-6","R2A-7"]
 vectors={"docs/doctrine/control/a.md":"R2A-4","docs/doctrine/reviews/a.yaml":"R2A-5","docs/doctrine/root.yaml":"R2A-5","src/a.py":"R2A-6","schemas/a.json":"R2A-6","tests/runtime/a.py":"R2A-6","tests/test_runtime_x.py":"R2A-6","examples/a.md":"R2A-7","vendor/a.py":None}; assert {p:assign(p) for p in vectors}==vectors
 import copy
 changed=copy.deepcopy(rules); changed["disposition_rules"]["R2A-4"].append("examples/**"); assert assign("examples/a.md",changed)=="R2A-4"
 no_fallback=copy.deepcopy(rules); no_fallback["disposition_rules"]["R2A-7"]=[]
 try: assign("unowned/a.txt",no_fallback); assert False, "missing fallback must fail"
 except ValueError: pass
 overlap=copy.deepcopy(rules); overlap["disposition_rules"]["R2A-5"].append("docs/doctrine/control/**"); assert assign("docs/doctrine/control/a.md",overlap)=="R2A-4"
 overlap["disposition_precedence"]=["R2A-5","R2A-4","R2A-6","R2A-7"]; assert assign("docs/doctrine/control/a.md",overlap)=="R2A-5"
 excluded_first=copy.deepcopy(rules); excluded_first["disposition_rules"]["R2A-4"].append("vendor/**"); assert assign("vendor/a.py",excluded_first) is None
 for path in subprocess.check_output(["git","ls-tree","-r","--name-only",ACCEPTED_R2A_1_HEAD],text=True).splitlines(): assert assign(path) is None or assign(path) in {"R2A-4","R2A-5","R2A-6","R2A-7"}
def test_twelve_partitions_dependencies_shards_and_no_coordination_owner():
 d=histload(PARTITIONS); rows=d["partitions"]; assert d["partition_count"]==len(rows)==12; assert [x["partition_id"] for x in rows]==[f"R2A-{n}" for n in range(1,13)]
 seen={"R2-0"}
 for x in rows: assert set(x["dependency_partitions"])<=seen and x["maximum_changed_files"]<=7 and x["maximum_additions"]<=2500; seen.add(x["partition_id"])
 assert d["ownership_rules"]["coordination_domain_ownership"]==[] and "bounded shards" in d["ownership_rules"]["sharding"]
 assert "Only R2A-12 may mark R2A complete" in rows[-1]["gate_effect"] and "cannot begin R2B" in rows[-2]["gate_effect"]
 for row in rows:
  paths=row.get("candidate_path_patterns",row.get("planned_artifact_paths")); assert paths and all("planned artifact family" not in path and not path.startswith("/") and " " not in path for path in paths)
  assert ("candidate_path_patterns" in row)==(row["partition_id"] in {"R2A-4","R2A-5","R2A-6","R2A-7"})
def test_manifest_statuses_sequence_and_cross_file_agreement():
 m=histload(FILES); seq=m["r2a_reconstruction_sequence"]; assert len(seq)==12 and all(set(x)=={"partition_id","current_status"} for x in seq)
 planned=[x for x in m["artifacts"] if x.get("phase","").startswith("R2A-") and x["phase"]!="R2A-1"]; assert len(planned)==11
 for number,x in enumerate(planned,2):
  assert "status" not in x; assert x["current_status"]=="planned_not_present"; assert x["phase"]==f"R2A-{number}"; assert not x["path"].startswith("/") and ("/index." in x["path"] or number==12)
 partitions=histload(PARTITIONS); contract=histload(CONTRACT); clusters=histload(CLUSTERS); ids=[f"R2A-{n}" for n in range(1,13)]; statuses={x["partition_id"]:x["current_status"] for x in seq}
 assert contract["partition_count"]==clusters["partition_count"]==partitions["partition_count"]==len(seq)==12
 assert contract["r2a_partition_ids"]==clusters["r2a_partition_ids"]==[x["partition_id"] for x in partitions["partitions"]]==ids
 assert contract["r2a_partition_statuses"]==clusters["r2a_partition_statuses"]=={x["partition_id"]:x["status"] for x in partitions["partitions"]}==statuses
 planned_by_phase={x["phase"]:x["path"] for x in planned}; partition_paths={x["partition_id"]:x["planned_artifact_paths"][0] for x in partitions["partitions"] if x["partition_id"] in planned_by_phase}; assert partition_paths==planned_by_phase
 plan=subprocess.check_output(["git","show",f"{ACCEPTED_R2A_1_HEAD}:{PLAN.relative_to(ROOT)}"],text=True); assert "twelve bounded pull requests" in plan and all(x in plan for x in ("`R2A=active_incomplete`","`R2B=blocked`","`R2C=blocked`","`R3–R6=blocked`"))
 assert [x["partition_id"] for x in partitions["partitions"] if "mark R2A complete" in x["gate_effect"]]==["R2A-12"] and "cannot begin R2B" in partitions["partitions"][-2]["gate_effect"]
def test_successor_safe_history_current_posture_and_nonauthority():
 history=subprocess.check_output(["git","show",f"{ACCEPTED_R2A_1_HEAD}:tests/test_afqr_r2_continuity_research_assimilation.py"],text=True); assert 'ACCEPTED_R2_0_HEAD="9382958197c9d5dee9d29cb5f9d051147237c64d"' in history and 'f"{BASE}...{ACCEPTED_R2_0_HEAD}"' in history and 'git","show",f"{ACCEPTED_R2_0_HEAD}' in history
 d=histload(CONTRACT); assert d["project_posture"]=={"R1":"complete","R2":"active_incomplete","R2-0":"complete","R2A":"active_incomplete","R2B":"blocked","R2C":"blocked","R3-R6":"blocked","RT-002G":"unauthorized","temporary_evidence_deletion":"unauthorized"}
 plan=subprocess.check_output(["git","show",f"{ACCEPTED_R2A_1_HEAD}:{PLAN.relative_to(ROOT)}"],text=True); assert "No compact reconstruction or isolated local commit is repository authority." in plan and "No-action and existing-owner outcomes are lawful" in plan
 assert not any(k in d for k in ("semantic_surfaces","candidate_files","claim_assessments","question_assessments"))
def test_no_deletions_binaries_oversize_or_overlong_lines():
 assert not subprocess.check_output(["git","diff","--name-status","--diff-filter=D",f"{BASE}...{ACCEPTED_R2A_1_HEAD}"],text=True).strip(); assert len(changed())==7
 for p in changed():
  raw=subprocess.check_output(["git","show",f"{ACCEPTED_R2A_1_HEAD}:{p}"]); assert b"\0" not in raw and len(raw)<=300*1024 and max(map(len,raw.splitlines()),default=0)<=1000
 num=subprocess.check_output(["git","diff","--numstat",f"{BASE}...{ACCEPTED_R2A_1_HEAD}"],text=True); assert "-\t-\t" not in num and sum(int(x.split("\t")[0]) for x in num.splitlines())<=2500

# Current R2A-2 validation follows the complete accepted R2A-1 boundary above.
from collections import Counter
import copy
INDEX=REV/"r2a/semantic_core_agency/index.yaml"; SHARD=REV/"r2a/semantic_core_agency/surfaces_0001.yaml"
R2A2_AUTHORIZED={"docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml","docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml","docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml","docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml","docs/doctrine/reviews/r2a/semantic_core_agency/index.yaml","docs/doctrine/reviews/r2a/semantic_core_agency/surfaces_0001.yaml","tests/test_afqr_r2a_inventory_contract.py"}
OWNER_RESP={"AFQR-01":"CORE-RESP-01","AFQR-02":"CORE-RESP-02","AFQR-04":"CORE-RESP-04","AFQR-06":"CORE-RESP-06","AFQR-07":"CORE-RESP-07","AFQR-08":"CORE-RESP-08","AFQR-09":"CORE-RESP-09","AFQR-10":"AGENCY-RESP-10"}
PRIMARY={"docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml","docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml","docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md","docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md","docs/doctrine/reviews/afqr_01_20_formal_completion_review.md","docs/doctrine/reviews/afqr_r1e_source_and_vocabulary_audit.yaml","docs/doctrine/reviews/afqr_r1e_dependency_and_parity_audit.yaml","docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml","docs/doctrine/reviews/afqr_r1e_consistency_and_corpus_adequacy.yaml","docs/decisions/current_decisions_log.md"}
def current(p): return json.loads(p.read_text())
def git(*args): return subprocess.check_output(["git",*args],text=True).strip()
def r2a2_changed(): return set(git("diff","--name-only",f"{R2A_2_BASE}...HEAD").splitlines())
def baseline_raw(path): return subprocess.check_output(["git","show",f"{R2A_2_BASE}:{path}"])
def fenced(path):
 text=baseline_raw(path).decode(); match=re.search(r"```json\n(.*?)\n```",text,re.S); assert match
 return json.loads(match.group(1))
def r1d_records():
 rows=[]
 for p in ("docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md","docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"): rows.extend(fenced(p)["responsibility_records"])
 return {x["record_id"]:x for x in rows}
def validate_owner_responsibility(record,responsibilities=None):
 responsibilities=responsibilities or r1d_records(); ids=record["applicable_r1d_responsibility_ids"]
 return len(ids)==1 and ids[0] in responsibilities and record["declared_owner"]==responsibilities[ids[0]]["afqr_id"] and OWNER_RESP.get(record["declared_owner"])==ids[0]
def test_r2a2_base_exact_scope_status_and_blocked_posture():
 subprocess.check_call(["git","merge-base","--is-ancestor",R2A_2_BASE,"HEAD"]); assert r2a2_changed()==R2A2_AUTHORIZED
 assert not any(p.startswith(("src/","schemas/","tests/runtime/")) for p in r2a2_changed())
 expected={f"R2A-{n}":("complete" if n<=2 else "planned_not_present") for n in range(1,13)}
 c=current(CONTRACT); p=current(PARTITIONS); clusters=current(CLUSTERS); m=current(FILES)
 assert c["r2a_partition_statuses"]==clusters["r2a_partition_statuses"]=={x["partition_id"]:x["status"] for x in p["partitions"]}=={x["partition_id"]:x["current_status"] for x in m["r2a_reconstruction_sequence"]}==expected
 assert c["project_posture"]=={"R1":"complete","R2":"active_incomplete","R2-0":"complete","R2A":"active_incomplete","R2B":"blocked","R2C":"blocked","R3-R6":"blocked","RT-002G":"unauthorized","temporary_evidence_deletion":"unauthorized"}
def test_primary_source_review_coverage_is_bounded_complete_and_specific():
 i=current(INDEX); rows=i["primary_source_review_coverage"]; paths=[x["path"] for x in rows]
 assert PRIMARY<=set(paths) and len(paths)==len(set(paths))
 layers={"R1B_vocabulary","R1C_invariant_dependency","R1D_family_doctrine","R1E_completion_and_adjudication","accepted_decision","current_control","implementation_presupposition","test_contract"}; statuses={"mapped_material_surfaces","reviewed_no_additional_surface","reviewed_boundary_only"}
 reasons=[]
 for x in rows:
  assert x["source_layer"] in layers and x["review_status"] in statuses and baseline_raw(x["path"]) is not None
  if x["review_status"]=="mapped_material_surfaces": assert x["surface_ids"] and x["no_additional_surface_reason"] is None
  else: assert not x["surface_ids"] and isinstance(x["no_additional_surface_reason"],str) and len(x["no_additional_surface_reason"])>40; reasons.append(x["no_additional_surface_reason"])
 assert len(reasons)==len(set(reasons))
def test_surface_contract_roles_order_ids_and_unique_semantic_identity():
 c=current(CONTRACT); records=current(SHARD)["surface_records"]; required=set(c["record_types"]["semantic_authority_surface"]["required_fields"]); roles=set(c["controlled_values"]["semantic_roles"])
 assert records==sorted(records,key=lambda r:(r["declared_owner"],r["path"],r["line_start"],r["line_end"],r["source_record_kind"],r["source_record_id"],r["semantic_role"]))
 assert len({r["surface_id"] for r in records})==len(records)==len({(r["declared_owner"],r["path"],r["line_start"],r["line_end"],r["source_record_kind"],r["source_record_id"],r["semantic_role"]) for r in records})
 core=[r for r in records if r["declared_owner"]!="AFQR-10"]; agency=[r for r in records if r["declared_owner"]=="AFQR-10"]
 assert [r["surface_id"] for r in core]==[f"R2A-SURFACE-CORE-{n:04d}" for n in range(1,len(core)+1)]
 assert [r["surface_id"] for r in agency]==[f"R2A-SURFACE-AGENCY-{n:04d}" for n in range(1,len(agency)+1)]
 for r in records: assert required<=set(r) and r["semantic_role"] in roles and r["inspected_commit"]==R2A_2_BASE and r["primary_partition"]=="R2A-2" and r["semantic_status"]=="validated"
def test_structural_owner_responsibility_mapping_and_negative_swaps():
 responsibilities=r1d_records(); records=current(SHARD)["surface_records"]
 assert all(validate_owner_responsibility(r,responsibilities) for r in records)
 for r in records:
  if r["semantic_role"]!="ownership_definition_with_boundary": continue
  source=responsibilities[r["applicable_r1d_responsibility_ids"][0]]; bounded=b"".join(baseline_raw(r["path"]).splitlines(keepends=True)[r["line_start"]-1:r["line_end"]]).decode()
  assert source["record_id"] in bounded and source["afqr_id"] in bounded and "owned_concerns" in bounded and "explicit_nonowned_concerns" in bounded
 victim=copy.deepcopy(records[0]); victim["declared_owner"]="AFQR-10" if victim["declared_owner"]!="AFQR-10" else "AFQR-01"; assert not validate_owner_responsibility(victim,responsibilities)
 victim=copy.deepcopy(records[0]); victim["applicable_r1d_responsibility_ids"]=[next(x for x in responsibilities if x!=victim["applicable_r1d_responsibility_ids"][0])]; assert not validate_owner_responsibility(victim,responsibilities)
def test_locators_baseline_paths_exact_hashes_and_no_self_inventory():
 allowed=set(current(CONTRACT)["controlled_values"]["locator_kinds"])
 for r in current(SHARD)["surface_records"]:
  raw=baseline_raw(r["path"]); lines=raw.splitlines(keepends=True); assert 0<r["line_start"]<=r["line_end"]<=len(lines)
  assert hashlib.sha256(b"".join(lines[r["line_start"]-1:r["line_end"]])).hexdigest()==r["excerpt_sha256"]
  assert r["locator_kind"] in allowed and ((r["locator_kind"]=="line_range_only")==(r["locator_value"] is None))
  assert not (r["path"].endswith(".md") and r["locator_kind"] in {"yaml_path","json_pointer"})
  assert not r["path"].startswith("docs/doctrine/reviews/r2a/semantic_core_agency/")
def test_structural_identifier_integrity_source_applicability_and_negative_ids():
 vocab=json.loads(baseline_raw("docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml")); r1c=json.loads(baseline_raw("docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml")); sub=json.loads(baseline_raw("docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml")); responsibilities=r1d_records()
 terms={x["term_id"] for x in vocab["term_records"]}; invs={x["invariant_id"] for x in r1c["cross_afqr_invariants"]}; deps={x["edge_id"] for x in r1c["dependency_edge_dispositions"]}; subs={x["substrate_id"] for x in sub["substrate_adjudications"]}
 def valid(r): return set(r["applicable_term_ids"])<=terms and set(r["applicable_invariant_ids"])<=invs and set(r["applicable_dependency_ids"])<=deps and set(r["applicable_substrate_ids"])<=subs
 for r in current(SHARD)["surface_records"]:
  assert valid(r)
  if r["semantic_role"]=="ownership_definition_with_boundary": assert set(r["applicable_term_ids"])<={x["term_id"] for x in responsibilities[r["applicable_r1d_responsibility_ids"][0]]["r1b_terms_or_qualified_forms"]}
  excerpt=b"".join(baseline_raw(r["path"]).splitlines(keepends=True)[r["line_start"]-1:r["line_end"]]).decode()
  assert all(x in excerpt for x in r["applicable_invariant_ids"]+r["applicable_dependency_ids"]+r["applicable_substrate_ids"])
 for field,bad in (("applicable_term_ids","TERM-999"),("applicable_invariant_ids","INV-999"),("applicable_dependency_ids","DEP-999"),("applicable_substrate_ids","SUB-999")):
  r=copy.deepcopy(current(SHARD)["surface_records"][0]); r[field]=[bad]; assert not valid(r)
 assert subs and all(re.fullmatch(r"SUB-\d{3}",x) for x in subs)
def test_claim_prohibitions_owner_coverage_counts_digest_and_responsibility_coverage():
 i=current(INDEX); records=current(SHARD)["surface_records"]
 assert all(r["linked_r2_claim_ids"]==r["claim_link_reasons"]==[] and r["declared_owner"] in OWNER_RESP for r in records)
 assert all(any(r["declared_owner"]==o and r["surface_kind"] in {"current_normative_doctrine","accepted_decision"} for r in records) for o in OWNER_RESP)
 for field in ("declared_owner","surface_kind","semantic_role","authority_level","currentness","generality"): assert i["counts"][field]==dict(sorted(Counter(r[field] for r in records).items()))
 assert i["counts"]["r1d_responsibility_id"]==dict(sorted(Counter(r["applicable_r1d_responsibility_ids"][0] for r in records).items()))
 sh=i["shards"][0]; assert i["surface_count"]==sh["record_count"]==len(records) and sh["content_sha256"]==hashlib.sha256(SHARD.read_bytes()).hexdigest()
 by_owner={o:{r["surface_id"] for r in records if r["declared_owner"]==o} for o in OWNER_RESP}; coverage={x["afqr_id"]:x for x in i["responsibility_coverage"]}; assert set(coverage)==set(OWNER_RESP)
 for o,c in coverage.items(): assert c["responsibility_id"]==OWNER_RESP[o] and set(c["surface_ids"])==by_owner[o] and c["current_normative_surface_ids"] and c["boundary_surface_ids"] and c["coverage_status"]=="validated_current_coverage"
 data=(INDEX.read_text()+SHARD.read_text()).lower(); assert not any(x in data for x in ("candidate_file_disposition","occurrence_tuple","claim_assessment_id","unresolved_question_id","package_assessment_id","module_assessment_id"))
def test_file_manifest_unique_paths_single_index_and_shard():
 paths=[x["path"] for x in current(FILES)["artifacts"]]; assert len(paths)==len(set(paths))
 assert paths.count("docs/doctrine/reviews/r2a/semantic_core_agency/index.yaml")==paths.count("docs/doctrine/reviews/r2a/semantic_core_agency/surfaces_0001.yaml")==1
def test_r2a2_containment_limits():
 assert not git("diff","--name-status","--diff-filter=D",f"{R2A_2_BASE}...HEAD")
 num=git("diff","--numstat",f"{R2A_2_BASE}...HEAD").splitlines(); assert "-\t-" not in "\n".join(num) and sum(int(x.split("\t")[0]) for x in num)<=2500
 for p in r2a2_changed():
  raw=(ROOT/p).read_bytes(); assert b"\0" not in raw and len(raw)<=300*1024 and max(map(len,raw.splitlines()),default=0)<=1000

def json_pointer_resolve(document,pointer):
 assert pointer.startswith("/"); value=document
 for token in pointer[1:].split("/"):
  token=token.replace("~1","/").replace("~0","~"); value=value[int(token)] if isinstance(value,list) else value[token]
 return value
def term_owner_ids(term):
 owners=[]; owner=term["type_owner"].get("owner_id")
 if isinstance(owner,str) and owner.startswith("AFQR-"): owners.append(owner)
 owners.extend(x["owner_id"] for x in term.get("qualified_forms",[]) if isinstance(x.get("owner_id"),str) and x["owner_id"].startswith("AFQR-"))
 return set(owners)
def structured_record_valid(surface):
 kind=surface["source_record_kind"]; source_id=surface["source_record_id"]
 if kind not in {"r1b_term_record","r1c_invariant","r1c_dependency_edge","r1e_substrate_adjudication"}: return True
 document=json.loads(baseline_raw(surface["path"])); selected=json_pointer_resolve(document,surface["locator_value"])
 if kind=="r1b_term_record": return selected.get("term_id")==source_id and source_id in surface["applicable_term_ids"] and surface["declared_owner"] in term_owner_ids(selected)
 if kind=="r1c_invariant":
  if selected.get("invariant_id")!=source_id or surface["applicable_invariant_ids"]!=[source_id] or surface["source_proposition"]!=selected.get("summary"): return False
  vocab=json.loads(baseline_raw("docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml")); by={x["term_id"]:x for x in vocab["term_records"]}; involved=set().union(*(term_owner_ids(by[x]) for x in selected["r1b_terms"]))
  return surface["declared_owner"] in involved and involved.intersection(OWNER_RESP)<=set(surface["applicable_afqr_ids"])
 if kind=="r1c_dependency_edge":
  if selected.get("edge_id")!=source_id or surface["applicable_dependency_ids"]!=[source_id]: return False
  semantic=selected.get("semantic_type_owner",{}).get("owner_id"); endpoints={selected.get("producer_afqr"),selected.get("consumer_afqr"),semantic}; role="source" if surface["declared_owner"]==selected.get("producer_afqr") else "target" if surface["declared_owner"]==selected.get("consumer_afqr") else "bounded_participant" if surface["declared_owner"]==semantic else None
  return surface["declared_owner"] in endpoints and surface["dependency_owner_role"]==role
 if kind=="r1e_substrate_adjudication": return selected.get("substrate_id")==source_id and source_id in surface["applicable_substrate_ids"] and surface["declared_owner"] in selected.get("exact_requiring_afqrs",[]) and selected.get("implementation_status")=="unimplemented" and "complete" not in surface["source_proposition"].lower()
def test_exact_structured_source_record_resolution_and_identity_fields():
 records=current(SHARD)["surface_records"]
 for r in records:
  assert r["source_record_kind"] in current(CONTRACT)["controlled_values"]["source_record_kinds"]
  assert isinstance(r["source_record_id"],str) and r["source_record_id"].strip()
  assert isinstance(r["source_proposition"],str) and len(r["source_proposition"].strip())>25 and "preserves the bounded proposition" not in r["source_proposition"].lower()
  assert structured_record_valid(r)
  if r["source_record_kind"]=="r1d_responsibility": assert r["source_record_id"]==r["applicable_r1d_responsibility_ids"][0]
 assert len({r["source_proposition"] for r in records})==len(records)
def test_invariant_pointer_summary_owner_and_swap_mutation_rejected():
 records=current(SHARD)["surface_records"]; invariants=[r for r in records if r["source_record_kind"]=="r1c_invariant"]
 assert {r["source_record_id"] for r in invariants}=={"INV-001","INV-002","INV-005","INV-006","INV-007"}
 logical=next(r for r in invariants if r["source_record_id"]=="INV-007"); bad=copy.deepcopy(logical);bad["source_record_id"]="INV-009";bad["applicable_invariant_ids"]=["INV-009"];assert not structured_record_valid(bad)
 assert not any(r["source_record_id"]=="INV-009" and r["declared_owner"]=="AFQR-07" for r in invariants)
def test_dependency_pointer_endpoint_role_and_unrelated_owner_rejected():
 records=current(SHARD)["surface_records"]; edges=[r for r in records if r["source_record_kind"]=="r1c_dependency_edge"]
 assert edges and all(r["dependency_owner_role"] in {"source","target","bounded_participant"} for r in edges)
 bad=copy.deepcopy(edges[0]);bad["declared_owner"]="AFQR-10";assert not structured_record_valid(bad)
def test_replay_recovery_and_resource_locality_are_not_false_invariant_links():
 records=current(SHARD)["surface_records"]
 replay=next(r for r in records if "replay idempotence" in r["source_proposition"]); assert replay["declared_owner"]=="AFQR-01" and replay["applicable_invariant_ids"]==[] and "identifier attached" in replay["semantic_summary"]
 resource=next(r for r in records if "donor resource models" in r["source_proposition"]); assert resource["declared_owner"]=="AFQR-07" and resource["applicable_invariant_ids"]==[]
def test_broad_family_decision_completion_and_control_are_reviewed_not_owned():
 i=current(INDEX); by={x["path"]:x for x in i["primary_source_review_coverage"]}
 for path in ("docs/decisions/current_decisions_log.md","docs/doctrine/reviews/afqr_01_20_formal_completion_review.md","docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md"):
  assert by[path]["review_status"]=="reviewed_boundary_only" and by[path]["surface_ids"]==[] and by[path]["no_additional_surface_reason"]

def identifier_drift_valid(index):
 rows=index.get("identifier_drift_observations",[]); expected={"INV-007","INV-008","INV-009"}
 if len(rows)!=3 or {r.get("canonical_record_id") for r in rows}!=expected: return False
 canonical={x["invariant_id"]:x["summary"] for x in json.loads(baseline_raw("docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml"))["cross_afqr_invariants"]}
 required="This observation does not select a replacement invariant, rewrite accepted doctrine, or authorize R2B."
 for r in rows:
  ident=r["canonical_record_id"]
  if r.get("drift_id")!=f"R2A2-DRIFT-{ident}" or r.get("canonical_summary")!=canonical[ident] or r.get("canonical_summary")==r.get("conflicting_summary"): return False
  if r.get("conflict_kind")!="accepted_source_identifier_semantic_mismatch" or r.get("current_status")!="unresolved" or r.get("authority_effect")!="records_drift_without_adjudication" or r.get("later_handoff")!="R2A-11" or r.get("prohibited_inference")!=required: return False
 return True
def test_three_unresolved_r1c_r1d_identifier_drift_observations():
 i=current(INDEX); assert identifier_drift_valid(i)
 canonical={x["invariant_id"]:x["summary"] for x in json.loads(baseline_raw("docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml"))["cross_afqr_invariants"]}
 assert canonical=={**canonical,"INV-007":"Logical time, causal order, environmental process, spatial topology, embodiment, exposure, integrity, and harm are distinct typed concerns.","INV-008":"Motivation or behavior prediction does not author actor choice or replace agency or responsibility doctrine.","INV-009":"Donor action economy, anatomy, grid, cosmology, progression, resource model, or turn cadence cannot become Astra law by implication."}
 prose=baseline_raw("docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md").decode().splitlines()[24]
 assert all(x in prose for x in ("`INV-007` separates reservation and settlement","`INV-008` makes replay idempotent and recovery identity-preserving","`INV-009` blocks recursive self-authorization"))
def test_identifier_drift_mutations_fail():
 i=current(INDEX); missing=copy.deepcopy(i);missing["identifier_drift_observations"].pop();assert not identifier_drift_valid(missing)
 resolved=copy.deepcopy(i);resolved["identifier_drift_observations"][0]["current_status"]="resolved";assert not identifier_drift_valid(resolved)
 rewritten=copy.deepcopy(i);next(x for x in rewritten["identifier_drift_observations"] if x["canonical_record_id"]=="INV-009")["canonical_summary"]="Recursive self-authorization is prohibited.";assert not identifier_drift_valid(rewritten)
def test_identifier_drift_surface_applicability_boundaries():
 records=current(SHARD)["surface_records"]
 logical=next(r for r in records if r["source_record_kind"]=="r1c_invariant" and r["source_record_id"]=="INV-007");assert logical["declared_owner"]=="AFQR-04" and logical["source_proposition"].startswith("Logical time, causal order")
 assert not any("replay" in r["source_proposition"].lower() and r["applicable_invariant_ids"] for r in records)
 resource=next(r for r in records if r["declared_owner"]=="AFQR-07" and "donor resource models" in r["source_proposition"]);assert resource["applicable_invariant_ids"]==[] and "ownership/applicability boundary" in resource["owner_boundary_effect"]
 bad=copy.deepcopy(logical);bad["declared_owner"]="AFQR-07";bad["applicable_afqr_ids"]=["AFQR-07"];bad["source_record_id"]="INV-009";bad["applicable_invariant_ids"]=["INV-009"];bad["locator_value"]="/cross_afqr_invariants/8";bad["source_proposition"]="Donor action economy, anatomy, grid, cosmology, progression, resource model, or turn cadence cannot become Astra law by implication.";assert not structured_record_valid(bad)
def test_index_acknowledges_canonical_r1c_donor_nonpromotion_without_adjudication():
 text=INDEX.read_text();assert "Donor resource-model nonpromotion appears both in canonical R1C INV-009" in text and "R1C lacks donor" not in text
 assert "records_drift_without_adjudication" in text and "resolve owner questions" not in text.lower()

# R2A-3 successor-safe WORLD and coordination validation is appended after the exact accepted R2A-2 test bytes.
ACCEPTED_R2A_2_HEAD = "e015a56f691aefd955e21bc2f7eaaa03327e4373"
R2A_3_BASE = ACCEPTED_R2A_2_HEAD
CORE_INDEX = REV / "r2a/semantic_core_agency/index.yaml"
CORE_SHARD = REV / "r2a/semantic_core_agency/surfaces_0001.yaml"
WORLD_INDEX = REV / "r2a/semantic_world_coordination/index.yaml"
WORLD_SHARD = REV / "r2a/semantic_world_coordination/surfaces_0001.yaml"
R2A3_AUTHORIZED = {
    "docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml",
    "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml",
    "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
    "docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml",
    "docs/doctrine/reviews/r2a/semantic_world_coordination/index.yaml",
    "docs/doctrine/reviews/r2a/semantic_world_coordination/surfaces_0001.yaml",
    "tests/test_afqr_r2a_inventory_contract.py",
}
WORLD_RESP = {
    "AFQR-16": "WORLD-RESP-16",
    "AFQR-17": "WORLD-RESP-17",
    "AFQR-18": "WORLD-RESP-18",
    "AFQR-19": "WORLD-RESP-19",
    "AFQR-20": "WORLD-RESP-20",
}
def parsed_r1d_responsibility_map():
    out = {}
    for path in (
        "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md",
        "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md",
        "docs/doctrine/consolidation/afqr_world_action_sensing.md",
    ):
        text = baseline3_raw(path).decode() if "baseline3_raw" in globals() else subprocess.check_output(["git", "show", f"{ACCEPTED_R2A_2_HEAD}:{path}"], text=True)
        match = re.search(r"```json\n(.*?)\n```", text, re.S)
        assert match
        for record in json.loads(match.group(1))["responsibility_records"]:
            assert record["afqr_id"] not in out
            out[record["afqr_id"]] = record["record_id"]
    return out

R1D_RESP = parsed_r1d_responsibility_map()
COORD_LABELS = {"continuity_coordination", "cross_phase_coordination"}
R2A3_PRIMARY = {
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


def current_file(path: Path):
    return json.loads(path.read_text())


def r2a3_changed():
    return set(git("diff", "--name-only", f"{R2A_3_BASE}...HEAD").splitlines())


def baseline3_raw(path: str):
    return subprocess.check_output(["git", "show", f"{R2A_3_BASE}:{path}"])


def r2a3_records():
    return current_file(WORLD_SHARD)["surface_records"]


def r2a3_index():
    return current_file(WORLD_INDEX)


def r2a3_excerpt(record):
    raw = baseline3_raw(record["path"]).splitlines(keepends=True)
    return b"".join(raw[record["line_start"] - 1:record["line_end"]])


def pointer_resolve(document, pointer):
    assert pointer.startswith("/")
    value = document
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def r2a3_json(path):
    return json.loads(baseline3_raw(path))


def r2a3_world_contract():
    text = baseline3_raw("docs/doctrine/consolidation/afqr_world_action_sensing.md").decode()
    match = re.search(r"```json\n(.*?)\n```", text, re.S)
    assert match
    return json.loads(match.group(1))


def owners_for_term(term):
    owners = set()
    oid = term["type_owner"].get("owner_id")
    if isinstance(oid, str) and oid.startswith("AFQR-"):
        owners.add(oid)
    for form in term.get("qualified_forms", []):
        oid = form.get("owner_id")
        if isinstance(oid, str) and oid.startswith("AFQR-"):
            owners.add(oid)
    return owners


def r2a3_current_statuses():
    return {f"R2A-{n}": ("complete" if n <= 3 else "planned_not_present") for n in range(1, 13)}


# Override predecessor helper lookups after the accepted bytes so accepted R2A-2 tests remain historical.
def current(p):
    historical = {CONTRACT, PARTITIONS, CLUSTERS, FILES, INDEX, SHARD}
    if p in historical:
        return json.loads(subprocess.check_output(["git", "show", f"{ACCEPTED_R2A_2_HEAD}:{p.relative_to(ROOT)}"], text=True))
    return json.loads(p.read_text())


def git(*args):
    args = list(args)
    old_range = f"{ACCEPTED_R2A_1_HEAD}...HEAD"
    args = [f"{ACCEPTED_R2A_1_HEAD}...{ACCEPTED_R2A_2_HEAD}" if a == old_range else a for a in args]
    return subprocess.check_output(["git", *args], text=True).strip()

def r2a2_changed():
    return set(subprocess.check_output(["git", "diff", "--name-only", f"{ACCEPTED_R2A_1_HEAD}...{ACCEPTED_R2A_2_HEAD}"], text=True).splitlines())


def test_current_file_begins_with_exact_accepted_r2a2_test_bytes():
    accepted = subprocess.check_output(["git", "show", f"{ACCEPTED_R2A_2_HEAD}:tests/test_afqr_r2a_inventory_contract.py"])
    assert Path(__file__).read_bytes().startswith(accepted)
    assert "def test_executable_discovery_vectors" in accepted.decode()
    assert "def test_dependency_pointer_endpoint_role_and_unrelated_owner_rejected" in accepted.decode()


def test_r2a3_exact_base_scope_status_and_limits():
    subprocess.check_call(["git", "merge-base", "--is-ancestor", R2A_3_BASE, "HEAD"])
    assert r2a3_changed() == R2A3_AUTHORIZED
    assert not any(p.startswith(("src/", "schemas/", "tests/runtime/")) for p in r2a3_changed())
    assert current_file(CONTRACT)["r2a_partition_statuses"] == current_file(CLUSTERS)["r2a_partition_statuses"] == r2a3_current_statuses()
    assert {x["partition_id"]: x["status"] for x in current_file(PARTITIONS)["partitions"]} == r2a3_current_statuses()
    assert {x["partition_id"]: x["current_status"] for x in current_file(FILES)["r2a_reconstruction_sequence"]} == r2a3_current_statuses()
    assert current_file(CONTRACT)["project_posture"]["R2A"] == "active_incomplete"
    assert current_file(CONTRACT)["project_posture"]["R2B"] == "blocked"
    assert current_file(CONTRACT)["project_posture"]["RT-002G"] == "unauthorized"
    assert not git("diff", "--name-status", "--diff-filter=D", f"{R2A_3_BASE}...HEAD")
    numstat = git("diff", "--numstat", f"{R2A_3_BASE}...HEAD").splitlines()
    assert "-\t-" not in "\n".join(numstat)
    assert sum(int(row.split("\t")[0]) for row in numstat) <= 2500
    for path in r2a3_changed():
        raw = (ROOT / path).read_bytes()
        assert b"\0" not in raw and len(raw) <= 300 * 1024
        assert max(map(len, raw.splitlines()), default=0) <= 1000


def test_r2a3_shard_order_ids_hashes_counts_and_manifest_count():
    records = r2a3_records(); idx = r2a3_index()
    assert records == sorted(records, key=lambda r: (r["declared_owner"], r["path"], r["line_start"], r["line_end"], r["source_record_kind"], r["source_record_id"], r["semantic_role"]))
    assert len({r["surface_id"] for r in records}) == len(records)
    assert len({(r["declared_owner"], r["path"], r["line_start"], r["line_end"], r["source_record_kind"], r["source_record_id"], r["semantic_role"]) for r in records}) == len(records)
    for family, prefix in [("AFQR-", "WORLD"), ("continuity_coordination", "CONTINUITY"), ("cross_phase_coordination", "CROSSPHASE")]:
        selected = [r for r in records if (r["declared_owner"].startswith(family) if family == "AFQR-" else r["declared_owner"] == family)]
        assert [r["surface_id"] for r in selected] == [f"R2A-SURFACE-{prefix}-{n:04d}" for n in range(1, len(selected) + 1)]
    for r in records:
        assert r["primary_partition"] == "R2A-3" and r["inspected_commit"] == R2A_3_BASE
        assert r["linked_r2_claim_ids"] == [] and r["claim_link_reasons"] == []
        assert hashlib.sha256(r2a3_excerpt(r)).hexdigest() == r["excerpt_sha256"]
        text = r2a3_excerpt(r).decode(errors="replace")
        assert len(text.strip()) > 1 and text.strip() not in {"{", "}"}
        assert not (r["path"].endswith(".md") and r["locator_kind"] in {"json_pointer", "yaml_path"})
    assert idx["surface_count"] == idx["shards"][0]["record_count"] == len(records)
    assert idx["shards"][0]["content_sha256"] == hashlib.sha256(WORLD_SHARD.read_bytes()).hexdigest()
    for key in ["declared_owner", "surface_kind", "semantic_role", "source_record_kind", "authority_level", "currentness", "generality"]:
        assert idx["counts"][key] == dict(sorted(Counter(r[key] for r in records).items()))
    manifest = current_file(FILES)
    core_count = current_file(CORE_INDEX)["surface_count"]
    assert core_count == len(current_file(CORE_SHARD)["surface_records"]) == 27
    core_art = next(x for x in manifest["artifacts"] if x["path"] == "docs/doctrine/reviews/r2a/semantic_core_agency/surfaces_0001.yaml")
    assert core_art["outputs"] == ["27 validated semantic authority surface records"]


def test_r2a3_r1d_responsibility_excerpt_support_and_negative_record_id_only():
    world = {r["record_id"]: r for r in r2a3_world_contract()["responsibility_records"]}
    for r in [x for x in r2a3_records() if x["source_record_kind"] == "r1d_responsibility"]:
        selected = world[r["source_record_id"]]
        assert r["declared_owner"] == selected["afqr_id"]
        assert r["applicable_r1d_responsibility_ids"] == [selected["record_id"]]
        excerpt = r2a3_excerpt(r).decode()
        for required in ("record_id", "afqr_id", "owned_concerns", "explicit_nonowned_concerns", "r1b_terms_or_qualified_forms"):
            assert required in excerpt
        assert selected["record_id"] in excerpt and selected["afqr_id"] in excerpt
    bad = copy.deepcopy(next(x for x in r2a3_records() if x["source_record_kind"] == "r1d_responsibility"))
    bad["line_end"] = bad["line_start"]
    assert "owned_concerns" not in r2a3_excerpt(bad).decode()


def test_r2a3_structured_json_pointer_records_are_exact_and_material():
    vocab = r2a3_json("docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml")
    r1c = r2a3_json("docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml")
    subs = r2a3_json("docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml")
    term_rows = [r for r in r2a3_records() if r["source_record_kind"] == "r1b_term_record"]
    assert {r["declared_owner"] for r in term_rows} == set(WORLD_RESP)
    for r in term_rows:
        selected = pointer_resolve(vocab, r["locator_value"])
        assert selected["term_id"] == r["source_record_id"] and selected["term_id"] in r["applicable_term_ids"]
        assert r["declared_owner"] in owners_for_term(selected)
        assert selected["definition"] == r["source_proposition"]
    inv_rows = [r for r in r2a3_records() if r["source_record_kind"] == "r1c_invariant"]
    assert {r["source_record_id"] for r in inv_rows} >= {"INV-003", "INV-004", "INV-007", "INV-009"}
    for r in inv_rows:
        selected = pointer_resolve(r1c, r["locator_value"])
        assert selected["invariant_id"] == r["source_record_id"]
        assert r["applicable_invariant_ids"] == [selected["invariant_id"]]
        assert r["source_proposition"] == selected["summary"]
    dep_rows = [r for r in r2a3_records() if r["source_record_kind"] == "r1c_dependency_edge"]
    assert {r["source_record_id"] for r in dep_rows} >= {"DEP-089", "DEP-091", "DEP-094"}
    for r in dep_rows:
        selected = pointer_resolve(r1c, r["locator_value"])
        semantic = selected["semantic_type_owner"]["owner_id"]
        role = "source" if r["declared_owner"] == selected["producer_afqr"] else "target" if r["declared_owner"] == selected["consumer_afqr"] else "bounded_participant"
        assert selected["edge_id"] == r["source_record_id"] and r["dependency_owner_role"] == role
        assert r["declared_owner"] in {selected["producer_afqr"], selected["consumer_afqr"], semantic}
    for r in [x for x in r2a3_records() if x["source_record_kind"] == "r1e_substrate_adjudication"]:
        selected = pointer_resolve(subs, r["locator_value"])
        assert selected["substrate_id"] == r["source_record_id"] in {"SUB-002", "SUB-005"}
        assert selected["implementation_status"] == "unimplemented"
        assert r["declared_owner"] in selected["exact_requiring_afqrs"]
    bad = copy.deepcopy(dep_rows[0]); bad["declared_owner"] = "AFQR-15"
    selected = pointer_resolve(r1c, bad["locator_value"])
    assert bad["declared_owner"] not in {selected["producer_afqr"], selected["consumer_afqr"], selected["semantic_type_owner"]["owner_id"]}


def test_r2a3_coordination_components_authority_and_no_invented_source_ids():
    records = r2a3_records(); coord = [r for r in records if r["declared_owner"] in COORD_LABELS]
    assert coord and not all(set(r["applicable_afqr_ids"]) == set(WORLD_RESP) for r in coord)
    for r in coord:
        assert r["applicable_afqr_ids"] and all(x in R1D_RESP for x in r["applicable_afqr_ids"])
        assert r["applicable_r1d_responsibility_ids"] == [R1D_RESP[x] for x in r["applicable_afqr_ids"]]
        assert r["surface_kind"] != "current_normative_doctrine" and r["authority_level"] != "current_normative"
        assert not re.fullmatch(r"R2A3-.+", r["source_record_id"])
        if "afqr_r2_continuity_research" in r["path"]:
            assert r["authority_level"] == "nonauthoritative"
    bad = copy.deepcopy(coord[0]); bad["applicable_afqr_ids"] = list(WORLD_RESP)
    assert set(bad["applicable_afqr_ids"]) != set(coord[0]["applicable_afqr_ids"])
    bad = copy.deepcopy(coord[0]); bad["source_proposition"] = "Fabricated zebra doctrine manufactures a combined owner."
    assert not any(phrase in r2a3_excerpt(coord[0]).decode() for phrase in ["Fabricated", "zebra"])


def test_r2a3_source_coverage_and_no_forbidden_assessments_or_authorization():
    idx = r2a3_index(); rows = idx["primary_source_review_coverage"]
    assert {x["path"] for x in rows} == R2A3_PRIMARY and len(rows) == len(R2A3_PRIMARY)
    by_path = {x["path"]: x for x in rows}
    assert by_path["docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml"]["surface_ids"]
    assert by_path["docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml"]["surface_ids"]
    assert by_path["docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml"]["no_additional_surface_reason"] is None
    mapped_r1c = {r["source_record_id"] for r in r2a3_records() if r["path"] == "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml"}
    assert {"DEP-089", "DEP-091", "DEP-094"} <= mapped_r1c
    sub_ids = by_path["docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml"]["surface_ids"]
    assert {r["source_record_id"] for r in r2a3_records() if r["surface_id"] in sub_ids} == {"SUB-002", "SUB-005"}
    reasons = [x["no_additional_surface_reason"] for x in rows if x["review_status"] != "mapped_material_surfaces"]
    assert all(isinstance(x, str) and len(x) > 50 for x in reasons) and len(reasons) == len(set(reasons))
    data = (WORLD_INDEX.read_text() + WORLD_SHARD.read_text()).lower()
    assert not any(x in data for x in ["candidate_file_disposition:", "raw_occurrence_tuple", "scan_receipt:", "claim_assessment_id", "package_assessment_id", "module_assessment_id"])
    assert all(r["linked_r2_claim_ids"] == [] and r["claim_link_reasons"] == [] for r in r2a3_records())
    assert "No R2B package requirement is selected or authorized." in idx["prohibited_inferences"]


def test_r2a3_r1b_term_parity_and_invariant_owner_graph_mutations():
    world = {r["record_id"]: r for r in r2a3_world_contract()["responsibility_records"]}
    expected = {
        owner: {x["term_id"] for x in world[rid]["r1b_terms_or_qualified_forms"]}
        for owner, rid in WORLD_RESP.items()
    }
    term_rows = [r for r in r2a3_records() if r["source_record_kind"] == "r1b_term_record"]
    actual = {owner: {r["source_record_id"] for r in term_rows if r["declared_owner"] == owner} for owner in WORLD_RESP}
    assert actual == expected
    vocab = r2a3_json("docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml")
    by_term = {x["term_id"]: x for x in vocab["term_records"]}
    for r in term_rows:
        selected = pointer_resolve(vocab, r["locator_value"])
        assert selected["term_id"] == r["source_record_id"]
        assert r["source_proposition"] == selected["definition"]
        assert r["declared_owner"] in owners_for_term(selected)
        assert r["applicable_r1d_responsibility_ids"] == [WORLD_RESP[r["declared_owner"]]]
    inv_rows = [r for r in r2a3_records() if r["source_record_kind"] == "r1c_invariant"]
    for r in inv_rows:
        derived = sorted(set().union(*(owners_for_term(by_term[tid]) for tid in r["applicable_term_ids"])))
        assert r["declared_owner"] in derived
        assert r["applicable_afqr_ids"] == derived
    inv7 = next(r for r in inv_rows if r["source_record_id"] == "INV-007")
    bad = copy.deepcopy(inv7); bad["applicable_afqr_ids"] = sorted(set(bad["applicable_afqr_ids"]) | {"AFQR-19"})
    assert bad["applicable_afqr_ids"] != sorted(set().union(*(owners_for_term(by_term[tid]) for tid in bad["applicable_term_ids"])))
    bad = copy.deepcopy(inv7); bad["declared_owner"] = "AFQR-20"
    assert bad["declared_owner"] not in sorted(set().union(*(owners_for_term(by_term[tid]) for tid in bad["applicable_term_ids"])))
    bad = copy.deepcopy(inv7); bad["applicable_term_ids"] = ["TERM-001"]
    assert bad["applicable_afqr_ids"] != sorted(set().union(*(owners_for_term(by_term[tid]) for tid in bad["applicable_term_ids"])))


def test_r2a3_parsed_responsibility_map_and_crossphase_domain_mapping():
    parsed = parsed_r1d_responsibility_map()
    assert parsed == R1D_RESP and len(parsed) == len(set(parsed.values())) == 20
    assert all(not rid.startswith(("CORE-RESP-10", "AGENCY-RESP-01")) for rid in parsed.values())
    cross = next(r for r in r2a3_records() if r["declared_owner"] == "cross_phase_coordination")
    expected = ["AFQR-01", "AFQR-04", "AFQR-06", "AFQR-08", "AFQR-05", "AFQR-10", "AFQR-16", "AFQR-17", "AFQR-19", "AFQR-20", "AFQR-07"]
    assert cross["applicable_afqr_ids"] == expected
    assert "AFQR-09" not in cross["applicable_afqr_ids"] and "AFQR-18" not in cross["applicable_afqr_ids"]
    assert "AFQR-10" in cross["applicable_afqr_ids"]
    assert cross["applicable_r1d_responsibility_ids"] == [parsed[x] for x in expected]
    bad = copy.deepcopy(cross); bad["applicable_afqr_ids"].append("AFQR-09")
    assert bad["applicable_afqr_ids"] != expected
    bad = copy.deepcopy(cross); bad["applicable_afqr_ids"].remove("AFQR-10")
    assert bad["applicable_afqr_ids"] != expected


def test_r2a3_world_and_coordination_coverage_recompute():
    idx = r2a3_index(); records = r2a3_records()
    by_owner = {owner: {r["surface_id"] for r in records if r["declared_owner"] == owner} for owner in WORLD_RESP}
    assert {x["responsibility_id"] for x in idx["world_responsibility_coverage"]} == set(WORLD_RESP.values())
    for row in idx["world_responsibility_coverage"]:
        assert row["responsibility_id"] == WORLD_RESP[row["afqr_id"]]
        assert set(row["surface_ids"]) == by_owner[row["afqr_id"]]
        assert row["current_normative_surface_ids"] and row["coverage_status"] == "validated_current_coverage"
    for row in idx["coordination_coverage"]:
        selected = [r for r in records if r["declared_owner"] == row["coordination_label"]]
        comp = sorted(set(x for r in selected for x in r["applicable_afqr_ids"]))
        assert set(row["surface_ids"]) == {r["surface_id"] for r in selected}
        assert row["component_afqr_ids"] == comp
        assert row["component_r1d_responsibility_ids"] == [R1D_RESP[x] for x in comp]
    bad = copy.deepcopy(current_file(CONTRACT)); bad["project_posture"]["R2A"] = "complete"
    assert bad["project_posture"]["R2A"] != current_file(CONTRACT)["project_posture"]["R2A"]

# R2A-4 successor validation begins after the exact accepted R2A-3 bytes above.
ACCEPTED_R2A_3_HEAD = "1b70f46718035d5f9395346cbf9eb1208a489698"
R2A_4_BASE = ACCEPTED_R2A_3_HEAD
ACCEPTED_R2A_4_HEAD = "e971410e0b5d7d8eeda94a5474e9cf799b4cb67a"
R2A4_INDEX=REV/"r2a/dispositions_current_a/index.yaml"; R2A4_SHARD=REV/"r2a/dispositions_current_a/dispositions_0001.yaml"
R2A4_AUTHORIZED={"docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml","docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml","docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml","docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml","docs/doctrine/reviews/r2a/dispositions_current_a/index.yaml","docs/doctrine/reviews/r2a/dispositions_current_a/dispositions_0001.yaml","tests/test_afqr_r2a_inventory_contract.py"}
RELATIONSHIPS={"originates accepted surface","restates accepted surface","governed by accepted surface","operationalizes without authority transfer","routes without authority transfer","duplicates accepted boundary"}
GENERIC_PROPOSITIONS={"this file concerns runtime","this file relates to identity","this passage discusses action","this matches the commitment cluster"}
def repo_git_path(value):
 native=Path(value)
 if native.is_absolute():value=native.relative_to(ROOT)
 path=str(value).replace("\\","/")
 while path.startswith("./"):path=path[2:]
 if Path(path).is_absolute() or path.startswith("../"):raise ValueError("repository Git paths must be relative")
 return path
def git_blob(ref,value):return subprocess.check_output(["git","show",f"{ref}:{repo_git_path(value)}"])
def git_text(ref,value):return git_blob(ref,value).decode("utf-8")
def r2a4_current(p):return json.loads(p.read_text())
def histload(p):return json.loads(git_text(ACCEPTED_R2A_1_HEAD,p))
def current(p):
 historical={repo_git_path(x) for x in (CONTRACT,PARTITIONS,CLUSTERS,FILES,INDEX,SHARD)};key=repo_git_path(p)
 return json.loads(git_text(ACCEPTED_R2A_2_HEAD,key)) if key in historical else json.loads(Path(p).read_text())
def current_file(p):return json.loads(git_text(ACCEPTED_R2A_3_HEAD,p))
def git(*args):
 args=tuple(a.replace(f"{R2A_2_BASE}...HEAD",f"{R2A_2_BASE}...{R2A_3_BASE}").replace(f"{R2A_3_BASE}...HEAD",f"{R2A_3_BASE}...{ACCEPTED_R2A_3_HEAD}") for a in args);return subprocess.check_output(["git",*args],text=True).strip()
def r2a3_changed():return set(git("diff","--name-only",f"{R2A_3_BASE}...{ACCEPTED_R2A_3_HEAD}").splitlines())
def r2a4_data():return r2a4_current(R2A4_INDEX),r2a4_current(R2A4_SHARD)
def baseline_raw(path):return git_blob(R2A_2_BASE,path)
def baseline3_raw(path):return git_blob(R2A_3_BASE,path)
def base4(path):return git_blob(R2A_4_BASE,path)
def terms4():
 d=json.loads(base4("docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml"));return {x["cluster_id"]:x["terms"] for x in d["clusters"]}
def candidates4():
 out={};rules=r2a4_current(PARTITIONS)["ownership_rules"]
 for p in subprocess.check_output(["git","ls-tree","-r","--name-only",R2A_4_BASE],text=True).splitlines():
  raw=base4(p)
  if assign(p,rules)=="R2A-4" and not excluded(p,raw) and (found:=match(p,raw,terms4())):out[p]=found
 return out
def surfaces4():
 ps=[REV/"r2a/semantic_core_agency/surfaces_0001.yaml",REV/"r2a/semantic_world_coordination/surfaces_0001.yaml"]
 return {r["surface_id"]:r for p in ps for r in json.loads(p.read_text())["surface_records"]}
def selected_text(r,loc):
 lines=base4(r["path"]).decode("utf-8-sig").splitlines();return " ".join(lines[loc["line_start"]-1:loc["line_end"]])
def meaningful_words(s):return {x for x in re.findall(r"[a-z]{4,}",normalize(s)) if x not in {"this","that","with","from","file","passage","surface","accepted"}}
def evidence_valid(r,e,surfaces=None):
 surfaces=surfaces or surfaces4();loc=e.get("candidate_locator",{}); sid=e.get("mapped_surface_id");
 if sid not in surfaces or e.get("mapping_relationship") not in RELATIONSHIPS or e.get("authority_transfer_effect")!="none":return False
 if not (0<loc.get("line_start",0)<=loc.get("line_end",0)):return False
 span=loc["line_end"]-loc["line_start"]+1;note=e.get("evidence_note","");prop=e.get("candidate_proposition","").strip()
 if span>200 or (span>80 and not re.search(r"(?i)span|structured block|lines",note)):return False
 if normalize(prop) in GENERIC_PROPOSITIONS or len(meaningful_words(prop)&meaningful_words(selected_text(r,loc)))<2:return False
 return "owner" in note.lower() and "authority" in note.lower() and r["candidate_file_id"] not in note and not re.search(r"(?i)candidate (?:inherits|gains|becomes).*?(?:owner|authority)",note)
def record_valid(r,surfaces=None):
 surfaces=surfaces or surfaces4();ev=r.get("mapping_evidence");mapped=r["mapped_surface_ids"]
 if ev is None or set(mapped)!={x.get("mapped_surface_id") for x in ev}:return False
 if mapped and not ev or any(not evidence_valid(r,x,surfaces) for x in ev):return False
 se=r.get("status_evidence");
 if se is not None and (not (0<se["line_start"]<=se["line_end"]) or not se["source_status_summary"].strip() or not status_valid(r,se)):return False
 if r["disposition"]=="internal_nonauthoritative_pressure_only" and (mapped or r["source_local_pressure_class"]!="no_material_relation" or r["authority_effect"] not in {"implementation_presupposition_only","escalation_pressure_only","no_authority_effect"}):return False
 if r["disposition"]=="source_local_pressure_only" and (r["source_local_pressure_class"]=="no_material_relation" or r["authority_effect"]!="source_local_pressure_only"):return False
 return True
def status_valid(r,se):
 source=normalize(selected_text(r,se));summary=normalize(se["source_status_summary"]);exact=[]
 status_match=re.search(r"status:\s*([^#]+?)(?:tracking id|\n|##|$)",source);status_line=status_match.group(1) if status_match else ""
 if "batch b operational-procedure draft" in source:exact += ["batch b","operational-procedure draft"]
 if re.match(r"# c(?:0[0-9]|1[0-4])\b",source) or re.match(r"# batch c",source):exact += ["batch c"]
 if "schema-draft" in source:exact += ["schema-draft"]
 if "owner scaffold only" in status_line:exact += ["owner scaffold only"]
 if "stage 2 owner specification" in status_line:exact += ["stage 2","owner-specification"]
 if "doctrine-draft" in source:exact += ["doctrine-draft"]
 if "not current canon" in source:exact += ["not current canon"]
 if "not marked current canon" in source:exact += ["not marked current canon"]
 if "runtime authority" in source or "runtime-ready" in source:exact += ["runtime"]
 return all(x in summary for x in exact)
def summary_residue(r):
 s=normalize(r["semantic_review_summary"]);s=s.replace(normalize(r["path"]),"").replace(normalize(Path(r["path"]).name),"")
 for x in r["mapped_surface_ids"]:s=s.replace(normalize(x),"")
 for x in RELATIONSHIPS:s=s.replace(x,"")
 return re.sub(r"\b(control|schema|operations|consolidation)\b","",s)

def test_current_test_prefix_is_exact_accepted_r2a3_bytes():assert git_blob("HEAD",repo_git_path(__file__)).startswith(git_blob(ACCEPTED_R2A_3_HEAD,repo_git_path(__file__)))
def test_r2a4_exact_base_scope_status_and_posture():
 assert subprocess.check_output(["git","merge-base",R2A_4_BASE,ACCEPTED_R2A_4_HEAD],text=True).strip()==R2A_4_BASE
 subprocess.check_call(["git","merge-base","--is-ancestor",ACCEPTED_R2A_4_HEAD,"HEAD"])
 assert set(subprocess.check_output(["git","diff","--name-only",f"{R2A_4_BASE}...{ACCEPTED_R2A_4_HEAD}"],text=True).splitlines())==R2A4_AUTHORIZED
 expected={f"R2A-{n}":("complete" if n<=3 else "active_incomplete" if n==4 else "planned_not_present") for n in range(1,13)};c=r2a4_current(CONTRACT);cl=r2a4_current(CLUSTERS);p=r2a4_current(PARTITIONS);m=r2a4_current(FILES)
 assert c["r2a_partition_statuses"]==cl["r2a_partition_statuses"]=={x["partition_id"]:x["status"] for x in p["partitions"]}=={x["partition_id"]:x["current_status"] for x in m["r2a_reconstruction_sequence"]}==expected
 assert c["project_posture"]["R2A"]=="active_incomplete" and c["project_posture"]["R2B"]=="blocked" and c["project_posture"]["RT-002G"]==c["project_posture"]["temporary_evidence_deletion"]=="unauthorized"
def test_r2a4_discovery_is_exact_and_independent_of_semantics():
 idx,sh=r2a4_data();raw=base4("docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml");cand=candidates4();rs=sh["candidate_file_dispositions"]
 assert hashlib.sha256(raw).hexdigest()==idx["discovery_provenance"]["controlled_search_artifact_sha256"]=="f68ec69039cee9ea4a2247a043b5b1da5264f04aeed5099bd8f6fd730906cfc9" and len(cand)==len(rs)==69
 assert [r["path"] for r in rs]==sorted(cand,key=lambda x:x.encode()) and [r["candidate_file_id"] for r in rs]==[f"R2A-DISPOSITION-A-{n:04d}" for n in range(1,70)]
 for r in rs:
  occ=cand[r["path"]];assert r["controlled_match_count"]==len(occ)>0 and r["matched_terms"]==sorted({x[2] for x in occ}) and r["matched_search_clusters"]==sorted({x[3] for x in occ})
  assert r["baseline_blob_sha"]==subprocess.check_output(["git","rev-parse",f"{R2A_4_BASE}:{r['path']}"],text=True).strip()
 import ast; tree=ast.parse(Path(__file__).read_text()); names={n.id for x in ast.walk(tree) if isinstance(x,(ast.Assign,ast.AnnAssign)) for n in ([x.target] if isinstance(x,ast.AnnAssign) else x.targets) if isinstance(n,ast.Name)}; assert not any(name.endswith("_SURFACE") or name.endswith("_SURFACES") for name in names)
def test_mapping_evidence_reciprocity_resolution_and_narrow_locators():
 _,sh=r2a4_data();surfaces=surfaces4();rs=sh["candidate_file_dispositions"];assert all(record_valid(r,surfaces) for r in rs)
 for r in rs:
  assert set(r["mapped_surface_ids"])=={x["mapped_surface_id"] for x in r["mapping_evidence"]}
  for e in r["mapping_evidence"]:assert e["mapped_surface_id"] in surfaces and e["authority_transfer_effect"]=="none" and evidence_valid(r,e,surfaces)
 assert all(e["mapping_relationship"]=="originates accepted surface" and surfaces[e["mapped_surface_id"]]["path"]==r["path"] for r in rs[1:6] for e in r["mapping_evidence"])
def test_status_evidence_preserves_source_distinctions_and_drives_nonauthority():
 _,sh=r2a4_data();rs=sh["candidate_file_dispositions"];assert all(r["status_evidence"] is not None and status_valid(r,r["status_evidence"]) for r in rs)
 internal=[r for r in rs if r["disposition"]=="internal_nonauthoritative_pressure_only"];assert internal and all(not r["mapped_surface_ids"] and r["source_local_pressure_class"]=="no_material_relation" and r["authority_effect"] in {"implementation_presupposition_only","escalation_pressure_only","no_authority_effect"} for r in internal)
 local=[r for r in rs if r["disposition"]=="source_local_pressure_only"];assert local and all(r["source_local_pressure_class"]!="no_material_relation" and r["authority_effect"]=="source_local_pressure_only" for r in local)
 controls=[r for r in rs if "/control/" in r["path"]];assert len({r["disposition"] for r in controls})>1
def test_mapping_mutations_reject_missing_extra_generic_wide_transfer_and_keyword_only():
 import copy
 _,sh=r2a4_data();surfaces=surfaces4();r=next(x for x in sh["candidate_file_dispositions"] if x["mapping_evidence"]);e=r["mapping_evidence"][0]
 bad=copy.deepcopy(r);bad["mapping_evidence"]=bad["mapping_evidence"][1:];assert not record_valid(bad,surfaces)
 bad=copy.deepcopy(r);bad["mapping_evidence"].append(dict(e,mapped_surface_id="R2A-SURFACE-WORLD-0029"));assert not record_valid(bad,surfaces)
 for patch in ({"mapping_relationship":""},{"authority_transfer_effect":"candidate_inherits"},{"candidate_proposition":"This file relates to identity."}):bad=copy.deepcopy(e);bad.update(patch);assert not evidence_valid(r,bad,surfaces)
 bad=copy.deepcopy(e);bad["candidate_locator"]["line_end"]=bad["candidate_locator"]["line_start"]+200;assert not evidence_valid(r,bad,surfaces)
 bad=copy.deepcopy(e);bad["candidate_locator"]["line_end"]=bad["candidate_locator"]["line_start"]+80;bad["evidence_note"]="Shared keyword and cluster; owner authority.";assert not evidence_valid(r,bad,surfaces)
def test_summaries_are_file_specific_not_superficially_unique_templates():
 _,sh=r2a4_data();rs=sh["candidate_file_dispositions"];res=[summary_residue(r) for r in rs];assert len(set(res))==69
 assert all(len(meaningful_words(x))>=12 for x in res) and not any("listed match families" in x for x in res)
def test_index_counts_digest_status_and_genuine_gap_gate():
 idx,sh=r2a4_data();rs=sh["candidate_file_dispositions"];assert hashlib.sha256(git_blob("HEAD",R2A4_SHARD)).hexdigest()==idx["shards"][0]["content_sha256"]
 for key,field in [("by_disposition","disposition"),("by_authority_effect","authority_effect"),("by_source_local_pressure_class","source_local_pressure_class"),("by_pressure_route","pressure_route")]:assert idx["counts"][key]==dict(sorted(__import__('collections').Counter(r[field] for r in rs).items()))
 cov=idx["surface_mapping_coverage"];assert cov["mapping_evidence_count"]==sum(len(r["mapping_evidence"]) for r in rs) and cov["status_evidence_count"]==69 and cov["blocking_gap_count"]==len(idx["blocking_unmapped_current_authority_candidates"])==1
 assert idx["status"]==sh["status"]=="active_incomplete" and idx["blocking_unmapped_current_authority_candidates"][0]["required_handoff"]=="corrective_semantic_inventory_review"
def test_no_raw_tuples_semantic_proxy_or_forbidden_assessments():
 data=(R2A4_INDEX.read_text()+R2A4_SHARD.read_text()).lower();assert not any(x in data for x in ("raw_occurrence_tuple","claim_assessment_id","question_assessment_id","package_assessment_id","module_assessment_id","scan_receipt_id","target_work_package"))
 contract=" ".join(r2a4_current(CONTRACT)["record_types"]["candidate_file_disposition"]["validation_rules"]);assert "discovery evidence only" in contract and "must never select semantic surfaces" in contract
def test_r2a4_containment_and_manifest_uniqueness():
 changed=subprocess.check_output(["git","diff","--name-only",f"{R2A_4_BASE}...{ACCEPTED_R2A_4_HEAD}"],text=True).splitlines();assert set(changed)==R2A4_AUTHORIZED and not subprocess.check_output(["git","diff","--name-only","--diff-filter=D",f"{R2A_4_BASE}...{ACCEPTED_R2A_4_HEAD}"],text=True).strip()
 num=subprocess.check_output(["git","diff","--numstat",f"{R2A_4_BASE}...{ACCEPTED_R2A_4_HEAD}"],text=True).splitlines();assert sum(int(x.split()[0]) for x in num)<=2500
 for p in changed:
  raw=git_blob(ACCEPTED_R2A_4_HEAD,p);assert len(raw)<=300*1024 and b"\0" not in raw and max(map(len,raw.splitlines()),default=0)<=1000
 paths=[x["path"] for x in r2a4_current(FILES)["artifacts"]];assert len(paths)==len(set(paths)) and paths.count(R2A4_INDEX.relative_to(ROOT).as_posix())==paths.count(R2A4_SHARD.relative_to(ROOT).as_posix())==1

def test_semantic_proxy_and_status_promotion_mutations_fail():
 import ast,copy
 tree=ast.parse(Path(__file__).read_text()); cluster_ids=set(terms4()); controlled_terms={normalize(t) for ts in terms4().values() for t in ts}
 for node in ast.walk(tree):
  if isinstance(node,ast.Assign) and isinstance(node.value,ast.Dict):
   keys={x.value for x in node.value.keys if isinstance(x,ast.Constant) and isinstance(x.value,str)};vals={x.value for x in node.value.values if isinstance(x,ast.Constant) and isinstance(x.value,str)}
   assert not ((keys&cluster_ids or {normalize(x) for x in keys}&controlled_terms) and any(x.startswith("R2A-SURFACE-") for x in vals))
 _,sh=r2a4_data();sf=surfaces4();internal=next(r for r in sh["candidate_file_dispositions"] if r["disposition"]=="internal_nonauthoritative_pressure_only");schema=next(r for r in sh["candidate_file_dispositions"] if r["path"].endswith("C13_map_diagram_record_schema.md"))
 bad=copy.deepcopy(internal);bad["source_local_pressure_class"]="consistent_source_local_evidence";assert not record_valid(bad,sf)
 bad=copy.deepcopy(schema);bad["status_evidence"]["source_status_summary"]="Batch B operational-procedure draft; not current canon or runtime authority.";assert not record_valid(bad,sf)
 bad=copy.deepcopy(schema);bad["mapped_surface_ids"]=["R2A-SURFACE-CORE-0003"];bad["mapping_evidence"]=[{"mapped_surface_id":"R2A-SURFACE-CORE-0003","candidate_locator":{"locator_kind":"line_range_only","locator_value":None,"line_start":1,"line_end":1},"candidate_proposition":"This file concerns runtime.","mapping_relationship":"governed by accepted surface","authority_transfer_effect":"none","evidence_note":"A shared runtime term does not prove an owner or grant authority."}];assert not record_valid(bad,sf)

def test_locator_owner_template_and_completion_mutations_fail():
 import copy
 idx,sh=r2a4_data();sf=surfaces4();mapped=next(r for r in sh["candidate_file_dispositions"] if r["mapping_evidence"]);e=mapped["mapping_evidence"][0]
 bad=copy.deepcopy(e);bad["candidate_locator"]={"locator_kind":"line_range_only","locator_value":None,"line_start":1,"line_end":1};assert not evidence_valid(mapped,bad,sf)
 bad=copy.deepcopy(e);bad["evidence_note"]="The candidate inherits the mapped owner and its semantic authority.";assert not evidence_valid(mapped,bad,sf)
 a,b=copy.deepcopy(sh["candidate_file_dispositions"][6]),copy.deepcopy(sh["candidate_file_dispositions"][36]);b["semantic_review_summary"]=a["semantic_review_summary"].replace(Path(a["path"]).name,Path(b["path"]).name);assert summary_residue(a)==summary_residue(b)
 bad=copy.deepcopy(idx);bad["status"]="complete";assert bad["status"]=="complete" and bool(bad["blocking_unmapped_current_authority_candidates"])

# Portable successor overrides: predecessor source bytes above remain untouched.
def test_current_file_begins_with_exact_accepted_r2a2_test_bytes():
 path="tests/test_afqr_r2a_inventory_contract.py";current_blob=git_blob("HEAD",path);accepted=git_blob(ACCEPTED_R2A_2_HEAD,path)
 assert current_blob.startswith(accepted) and b"def test_executable_discovery_vectors" in accepted and b"def test_dependency_pointer_endpoint_role_and_unrelated_owner_rejected" in accepted

def test_repository_git_path_and_historical_blob_portability():
 expected="docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml"
 assert repo_git_path(CONTRACT)==expected and repo_git_path(r"docs\doctrine\reviews\afqr_r2a_inventory_contract.yaml")==expected
 values=[CONTRACT,INDEX,SHARD,WORLD_INDEX,WORLD_SHARD,R2A4_INDEX,R2A4_SHARD];assert all("\\" not in repo_git_path(x) for x in values)
 assert json.loads(git_blob(ACCEPTED_R2A_1_HEAD,CONTRACT))["artifact_id"]=="AFQR-R2A-INVENTORY-CONTRACT-001"
 assert json.loads(git_blob(ACCEPTED_R2A_2_HEAD,SHARD))["artifact_id"]=="AFQR-R2A-2-CORE-AGENCY-SEMANTIC-SHARD-0001"
 assert json.loads(git_blob(ACCEPTED_R2A_3_HEAD,WORLD_SHARD))["artifact_id"]=="AFQR-R2A-3-WORLD-COORDINATION-SEMANTIC-SHARD-0001"
 from pathlib import PureWindowsPath
 assert histload(PureWindowsPath(expected))["artifact_id"]=="AFQR-R2A-INVENTORY-CONTRACT-001"
 assert current(PureWindowsPath(expected))["artifact_id"]=="AFQR-R2A-INVENTORY-CONTRACT-001"
 assert current_file(PureWindowsPath(expected))["artifact_id"]=="AFQR-R2A-INVENTORY-CONTRACT-001"

def test_claim_prohibitions_owner_coverage_counts_digest_and_responsibility_coverage():
 i=current(INDEX);records=current(SHARD)["surface_records"]
 assert all(r["linked_r2_claim_ids"]==r["claim_link_reasons"]==[] and r["declared_owner"] in OWNER_RESP for r in records)
 assert all(any(r["declared_owner"]==o and r["surface_kind"] in {"current_normative_doctrine","accepted_decision"} for r in records) for o in OWNER_RESP)
 for field in ("declared_owner","surface_kind","semantic_role","authority_level","currentness","generality"):assert i["counts"][field]==dict(sorted(Counter(r[field] for r in records).items()))
 assert i["counts"]["r1d_responsibility_id"]==dict(sorted(Counter(r["applicable_r1d_responsibility_ids"][0] for r in records).items()))
 sh=i["shards"][0];assert i["surface_count"]==sh["record_count"]==len(records) and sh["content_sha256"]==hashlib.sha256(git_blob(ACCEPTED_R2A_2_HEAD,SHARD)).hexdigest()
 by_owner={o:{r["surface_id"] for r in records if r["declared_owner"]==o} for o in OWNER_RESP};coverage={x["afqr_id"]:x for x in i["responsibility_coverage"]};assert set(coverage)==set(OWNER_RESP)
 for o,c in coverage.items():assert c["responsibility_id"]==OWNER_RESP[o] and set(c["surface_ids"])==by_owner[o] and c["current_normative_surface_ids"] and c["boundary_surface_ids"] and c["coverage_status"]=="validated_current_coverage"
 data=(git_text(ACCEPTED_R2A_2_HEAD,INDEX)+git_text(ACCEPTED_R2A_2_HEAD,SHARD)).lower();assert not any(x in data for x in ("candidate_file_disposition","occurrence_tuple","claim_assessment_id","unresolved_question_id","package_assessment_id","module_assessment_id"))

def test_r2a2_containment_limits():
 assert not git("diff","--name-status","--diff-filter=D",f"{R2A_2_BASE}...HEAD");num=git("diff","--numstat",f"{R2A_2_BASE}...HEAD").splitlines();assert "-\t-" not in "\n".join(num) and sum(int(x.split("\t")[0]) for x in num)<=2500
 for p in r2a2_changed():
  raw=git_blob(R2A_3_BASE,p);assert b"\0" not in raw and len(raw)<=300*1024 and max(map(len,raw.splitlines()),default=0)<=1000

def test_r2a3_shard_digest_uses_accepted_git_blob_bytes():
 idx=r2a3_index();assert idx["shards"][0]["content_sha256"]==hashlib.sha256(git_blob(ACCEPTED_R2A_3_HEAD,WORLD_SHARD)).hexdigest()

def test_r2a3_containment_uses_committed_blob_bytes():
 for p in r2a3_changed():
  raw=git_blob(ACCEPTED_R2A_3_HEAD,p);assert b"\0" not in raw and len(raw)<=300*1024 and max(map(len,raw.splitlines()),default=0)<=1000

def test_r2a3_exact_base_scope_status_and_limits():
 subprocess.check_call(["git","merge-base","--is-ancestor",R2A_3_BASE,"HEAD"]);assert r2a3_changed()==R2A3_AUTHORIZED and not any(p.startswith(("src/","schemas/","tests/runtime/")) for p in r2a3_changed())
 assert current_file(CONTRACT)["r2a_partition_statuses"]==current_file(CLUSTERS)["r2a_partition_statuses"]==r2a3_current_statuses()
 assert {x["partition_id"]:x["status"] for x in current_file(PARTITIONS)["partitions"]}==r2a3_current_statuses() and {x["partition_id"]:x["current_status"] for x in current_file(FILES)["r2a_reconstruction_sequence"]}==r2a3_current_statuses()
 assert current_file(CONTRACT)["project_posture"]["R2A"]=="active_incomplete" and current_file(CONTRACT)["project_posture"]["R2B"]=="blocked" and current_file(CONTRACT)["project_posture"]["RT-002G"]=="unauthorized"
 assert not git("diff","--name-status","--diff-filter=D",f"{R2A_3_BASE}...HEAD");num=git("diff","--numstat",f"{R2A_3_BASE}...HEAD").splitlines();assert "-\t-" not in "\n".join(num) and sum(int(x.split("\t")[0]) for x in num)<=2500
 for p in r2a3_changed():
  raw=git_blob(ACCEPTED_R2A_3_HEAD,p);assert b"\0" not in raw and len(raw)<=300*1024 and max(map(len,raw.splitlines()),default=0)<=1000

def test_r2a3_shard_order_ids_hashes_counts_and_manifest_count():
 records=r2a3_records();idx=r2a3_index();assert records==sorted(records,key=lambda r:(r["declared_owner"],r["path"],r["line_start"],r["line_end"],r["source_record_kind"],r["source_record_id"],r["semantic_role"]))
 assert len({r["surface_id"] for r in records})==len(records)==len({(r["declared_owner"],r["path"],r["line_start"],r["line_end"],r["source_record_kind"],r["source_record_id"],r["semantic_role"]) for r in records})
 for family,prefix in [("AFQR-","WORLD"),("continuity_coordination","CONTINUITY"),("cross_phase_coordination","CROSSPHASE")]:
  selected=[r for r in records if (r["declared_owner"].startswith(family) if family=="AFQR-" else r["declared_owner"]==family)];assert [r["surface_id"] for r in selected]==[f"R2A-SURFACE-{prefix}-{n:04d}" for n in range(1,len(selected)+1)]
 for r in records:
  assert r["primary_partition"]=="R2A-3" and r["inspected_commit"]==R2A_3_BASE and r["linked_r2_claim_ids"]==r["claim_link_reasons"]==[] and hashlib.sha256(r2a3_excerpt(r)).hexdigest()==r["excerpt_sha256"]
  text=r2a3_excerpt(r).decode(errors="replace");assert len(text.strip())>1 and text.strip() not in {"{","}"} and not (r["path"].endswith(".md") and r["locator_kind"] in {"json_pointer","yaml_path"})
 assert idx["surface_count"]==idx["shards"][0]["record_count"]==len(records) and idx["shards"][0]["content_sha256"]==hashlib.sha256(git_blob(ACCEPTED_R2A_3_HEAD,WORLD_SHARD)).hexdigest()
 for key in ["declared_owner","surface_kind","semantic_role","source_record_kind","authority_level","currentness","generality"]:assert idx["counts"][key]==dict(sorted(Counter(r[key] for r in records).items()))
 manifest=current_file(FILES);assert current_file(CORE_INDEX)["surface_count"]==len(current_file(CORE_SHARD)["surface_records"])==27
 assert next(x for x in manifest["artifacts"] if x["path"]=="docs/doctrine/reviews/r2a/semantic_core_agency/surfaces_0001.yaml")["outputs"]==["27 validated semantic authority surface records"]

# Final portable overrides for the two R2A-1 plan consumers; frozen predecessor bytes remain unchanged.
def test_manifest_statuses_sequence_and_cross_file_agreement():
 m=histload(FILES);seq=m["r2a_reconstruction_sequence"];assert len(seq)==12 and all(set(x)=={"partition_id","current_status"} for x in seq)
 planned=[x for x in m["artifacts"] if x.get("phase","").startswith("R2A-") and x["phase"]!="R2A-1"];assert len(planned)==11
 for number,x in enumerate(planned,2):
  assert "status" not in x;assert x["current_status"]=="planned_not_present";assert x["phase"]==f"R2A-{number}";assert not x["path"].startswith("/") and ("/index." in x["path"] or number==12)
 partitions=histload(PARTITIONS);contract=histload(CONTRACT);clusters=histload(CLUSTERS);ids=[f"R2A-{n}" for n in range(1,13)];statuses={x["partition_id"]:x["current_status"] for x in seq}
 assert contract["partition_count"]==clusters["partition_count"]==partitions["partition_count"]==len(seq)==12
 assert contract["r2a_partition_ids"]==clusters["r2a_partition_ids"]==[x["partition_id"] for x in partitions["partitions"]]==ids
 assert contract["r2a_partition_statuses"]==clusters["r2a_partition_statuses"]=={x["partition_id"]:x["status"] for x in partitions["partitions"]}==statuses
 planned_by_phase={x["phase"]:x["path"] for x in planned};partition_paths={x["partition_id"]:x["planned_artifact_paths"][0] for x in partitions["partitions"] if x["partition_id"] in planned_by_phase};assert partition_paths==planned_by_phase
 plan=git_text(ACCEPTED_R2A_1_HEAD,PLAN);assert "twelve bounded pull requests" in plan and all(x in plan for x in ("`R2A=active_incomplete`","`R2B=blocked`","`R2C=blocked`","`R3–R6=blocked`"))
 assert [x["partition_id"] for x in partitions["partitions"] if "mark R2A complete" in x["gate_effect"]]==["R2A-12"] and "cannot begin R2B" in partitions["partitions"][-2]["gate_effect"]

def test_successor_safe_history_current_posture_and_nonauthority():
 history=git_text(ACCEPTED_R2A_1_HEAD,"tests/test_afqr_r2_continuity_research_assimilation.py");assert 'ACCEPTED_R2_0_HEAD="9382958197c9d5dee9d29cb5f9d051147237c64d"' in history and 'f"{BASE}...{ACCEPTED_R2_0_HEAD}"' in history and 'git","show",f"{ACCEPTED_R2_0_HEAD}' in history
 d=histload(CONTRACT);assert d["project_posture"]=={"R1":"complete","R2":"active_incomplete","R2-0":"complete","R2A":"active_incomplete","R2B":"blocked","R2C":"blocked","R3-R6":"blocked","RT-002G":"unauthorized","temporary_evidence_deletion":"unauthorized"}
 plan=git_text(ACCEPTED_R2A_1_HEAD,PLAN);assert "No compact reconstruction or isolated local commit is repository authority." in plan and "No-action and existing-owner outcomes are lawful" in plan
 assert not any(k in d for k in ("semantic_surfaces","candidate_files","claim_assessments","question_assessments"))

# R2A-4 corrective completion receipt.  The canonical commit may be absent from
# an isolated publication workspace, so the fallback is selected solely by the
# canonical tree and parent identities, never by a workspace-local commit SHA.
R2A_4_COMPLETION_BASE = "ae37e2044ce7c8e317266a811084867757e699a6"
R2A_4_COMPLETION_HEAD = "4e52923df98183da6a2dc4f9af81e1fd2de9e09d"
R2A_4_COMPLETION_TREE = "a5b3f0d1791e7c702519665c0949b4ff29c73826"
R2A4_COMPLETION_ARTIFACTS = {
 "docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml",
 "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml",
 "docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml",
 "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
 "docs/doctrine/reviews/r2a/dispositions_current_a/index.yaml",
 "docs/doctrine/reviews/r2a/dispositions_current_a/dispositions_0001.yaml",
}
R2A4_CORRECTIVE_MAPPING_IDS = {
 "R2A-SURFACE-CROSSPHASE-0001", "R2A-SURFACE-WORLD-0011",
 "R2A-SURFACE-WORLD-0022", "R2A-SURFACE-WORLD-0016",
 "R2A-SURFACE-CORE-0001", "R2A-SURFACE-WORLD-0007",
 "R2A-SURFACE-CORE-0003", "R2A-SURFACE-CONTINUITY-0001",
}
R2A4_COMPLETION_BLOBS = {
 "docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml": "fa6e9012c8c588d70db8e41c27adcc6ab08fe5bf",
 "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml": "3df3a3cced1d9e377c487a887a13d924c6cf756f",
 "docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml": "5e46f8c3d73ba45271b0e464a0481e36fb47cc69",
 "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml": "472669ddfedbed507357adeccf4d8cdea223ac25",
 "docs/doctrine/reviews/r2a/dispositions_current_a/dispositions_0001.yaml": "830e1338240e5221a2cca46c129176957067c7d1",
 "docs/doctrine/reviews/r2a/dispositions_current_a/index.yaml": "230dbdf0c6ee1678c6559cd0c8f026a2a09d972d",
}

def completion_git(*args):
 return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def resolve_r2a4_completion():
 canonical = subprocess.run(
  ["git", "cat-file", "-e", f"{R2A_4_COMPLETION_HEAD}^{{commit}}"],
  cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
 ).returncode == 0
 if canonical:
  return R2A_4_COMPLETION_HEAD, "canonical"
 for candidate in completion_git("rev-list", "--max-count=64", "HEAD").splitlines():
  parents = completion_git("rev-list", "--parents", "-n", "1", candidate).split()
  if (completion_git("rev-parse", f"{candidate}^{{tree}}") == R2A_4_COMPLETION_TREE
      and parents[1:] == [R2A_4_COMPLETION_BASE]):
   return candidate, "tree-equivalent"
 return None, "history-unavailable"

def corrective_record_valid(record):
 evidence = record.get("mapping_evidence", [])
 representatives = record.get("representative_locators", [])
 if set(record.get("mapped_surface_ids", [])) != R2A4_CORRECTIVE_MAPPING_IDS:
  return False
 if len(evidence) != len(R2A4_CORRECTIVE_MAPPING_IDS):
  return False
 if {row.get("mapped_surface_id") for row in evidence} != R2A4_CORRECTIVE_MAPPING_IDS:
  return False
 if any(row.get("authority_transfer_effect") != "none" for row in evidence):
  return False
 if len(representatives) < 30:
  return False
 for locator in representatives:
  if not (0 < locator.get("line_start", 0) <= locator.get("line_end", 0) <= 4280):
   return False
  if locator["line_end"] - locator["line_start"] + 1 > 200:
   return False
  if locator.get("matched_terms") or locator.get("matched_search_clusters"):
   return False
  note = normalize(locator.get("semantic_review_note", ""))
  if len(meaningful_words(note)) < 8 or not re.search(r"\b(?:authority|owners?)\b", note):
   return False
  if "mapping" not in note or not any(marker in note for marker in ("no ", "not ", "apart from")):
   return False
 return True

def test_r2a4_successor_safe_canonical_completion_receipt():
 completion, resolution = resolve_r2a4_completion()
 if resolution == "history-unavailable":
  import pytest
  assert R2A_4_COMPLETION_BASE == "ae37e2044ce7c8e317266a811084867757e699a6"
  assert R2A_4_COMPLETION_HEAD == "4e52923df98183da6a2dc4f9af81e1fd2de9e09d"
  assert R2A_4_COMPLETION_TREE == "a5b3f0d1791e7c702519665c0949b4ff29c73826"
  assert set(R2A4_COMPLETION_BLOBS) == R2A4_COMPLETION_ARTIFACTS
  for path, expected_blob in R2A4_COMPLETION_BLOBS.items():
   assert completion_git("hash-object", path) == expected_blob
  pytest.skip("canonical R2A-4 completion history is unavailable in this isolated/rematerialized Git snapshot")
 assert completion_git("rev-parse", f"{completion}^{{tree}}") == R2A_4_COMPLETION_TREE
 assert completion_git("rev-parse", f"{completion}^") == R2A_4_COMPLETION_BASE
 subprocess.check_call(["git", "merge-base", "--is-ancestor", ACCEPTED_R2A_4_HEAD, completion], cwd=ROOT)
 subprocess.check_call(["git", "merge-base", "--is-ancestor", completion, "HEAD"], cwd=ROOT)
 changed = set(completion_git("diff", "--name-only", f"{R2A_4_COMPLETION_BASE}...{completion}").splitlines())
 assert changed == R2A4_COMPLETION_ARTIFACTS
 assert not completion_git("diff", "--name-status", "--diff-filter=D", f"{R2A_4_COMPLETION_BASE}...{completion}")
 frozen_index = json.loads(completion_git("show", f"{completion}:{R2A4_INDEX.relative_to(ROOT).as_posix()}"))
 assert frozen_index["status"] == "complete"
 if resolution == "canonical":
  assert completion == R2A_4_COMPLETION_HEAD

def test_r2a4_completed_status_and_posture():
 expected = {f"R2A-{n}": ("complete" if n <= 4 else "planned_not_present") for n in range(1, 13)}
 c, cl, p, m = map(r2a4_current, (CONTRACT, CLUSTERS, PARTITIONS, FILES))
 assert c["r2a_partition_statuses"] == cl["r2a_partition_statuses"]
 assert c["r2a_partition_statuses"] == {row["partition_id"]: row["status"] for row in p["partitions"]}
 assert c["r2a_partition_statuses"] == {row["partition_id"]: row["current_status"] for row in m["r2a_reconstruction_sequence"]} == expected
 assert c["project_posture"]["R2A"] == "active_incomplete"
 assert c["project_posture"]["R2B"] == "blocked"
 assert c["project_posture"]["RT-002G"] == c["project_posture"]["temporary_evidence_deletion"] == "unauthorized"

def test_r2a4_corrective_semantics_and_representative_review_are_bounded():
 _, shard = r2a4_data(); record = shard["candidate_file_dispositions"][0]
 assert corrective_record_valid(record)
 notes = " ".join(row["semantic_review_note"].lower() for row in record["representative_locators"])
 for family in ("operational", "source-local", "history", "project-management", "implementation", "current-control"):
  assert family in notes
 assert "lexical discovery selects no surface" in record["semantic_review_summary"].lower()

def test_completed_index_counts_digest_and_zero_gap_gate():
 idx, shard = r2a4_data(); records = shard["candidate_file_dispositions"]
 assert hashlib.sha256(R2A4_SHARD.read_bytes()).hexdigest() == idx["shards"][0]["content_sha256"]
 for key, field in (("by_disposition", "disposition"), ("by_authority_effect", "authority_effect"),
                    ("by_source_local_pressure_class", "source_local_pressure_class"), ("by_pressure_route", "pressure_route")):
  assert idx["counts"][key] == dict(sorted(Counter(row[field] for row in records).items()))
 evidence = [item for row in records for item in row["mapping_evidence"]]
 coverage = idx["surface_mapping_coverage"]
 assert coverage["mapping_evidence_count"] == len(evidence)
 assert coverage["unique_mapped_surface_count"] == len({item["mapped_surface_id"] for item in evidence})
 assert coverage["status_evidence_count"] == len(records) == 69
 assert coverage["blocking_gap_count"] == 0
 assert idx["blocking_unmapped_current_authority_candidates"] == []
 assert idx["status"] == shard["status"] == "complete"

def test_completed_mapping_and_promotion_mutations_fail():
 idx, shard = r2a4_data(); record = shard["candidate_file_dispositions"][0]
 for mutation in ("missing", "extra", "reciprocity", "transfer", "superficial", "lexical"):
  bad = copy.deepcopy(record)
  if mutation == "missing":
   bad["mapped_surface_ids"].pop()
  elif mutation == "extra":
   bad["mapped_surface_ids"].append("R2A-SURFACE-WORLD-0029")
  elif mutation == "reciprocity":
   bad["mapping_evidence"].pop()
  elif mutation == "transfer":
   bad["mapping_evidence"][0]["authority_transfer_effect"] = "candidate_inherits"
  elif mutation == "superficial":
   bad["representative_locators"] = bad["representative_locators"][:1]
  else:
   bad["representative_locators"][0]["matched_terms"] = ["authority"]
  assert not corrective_record_valid(bad)
 bad_index = copy.deepcopy(idx); bad_index["surface_mapping_coverage"]["blocking_gap_count"] = 1
 assert bad_index["status"] == "complete" and bad_index["surface_mapping_coverage"]["blocking_gap_count"] != 0
 bad_contract = copy.deepcopy(r2a4_current(CONTRACT)); bad_contract["project_posture"]["R2A"] = "complete"
 assert bad_contract["project_posture"]["R2A"] != "active_incomplete"
 bad_contract = copy.deepcopy(r2a4_current(CONTRACT)); bad_contract["r2a_partition_statuses"]["R2A-5"] = "active_incomplete"
 assert bad_contract["r2a_partition_statuses"]["R2A-5"] != "planned_not_present"

def test_current_file_begins_with_exact_accepted_r2a2_test_bytes():
 path = repo_git_path(__file__); current_blob = Path(__file__).read_bytes(); accepted = git_blob(ACCEPTED_R2A_2_HEAD, path)
 assert current_blob.startswith(accepted)
 assert b"def test_executable_discovery_vectors" in accepted
 assert b"def test_dependency_pointer_endpoint_role_and_unrelated_owner_rejected" in accepted

def test_current_test_prefix_is_exact_accepted_r2a3_bytes():
 assert Path(__file__).read_bytes().startswith(git_blob(ACCEPTED_R2A_3_HEAD, repo_git_path(__file__)))

# The predecessor definitions above are retained as historical test bytes.  Bind
# their obsolete names to the corrective-completion validations for collection.
test_r2a4_exact_base_scope_status_and_posture = test_r2a4_completed_status_and_posture
test_index_counts_digest_status_and_genuine_gap_gate = test_completed_index_counts_digest_and_zero_gap_gate
test_locator_owner_template_and_completion_mutations_fail = test_completed_mapping_and_promotion_mutations_fail

# R2A-5 successor-safe completion receipt and semantic freeze (append-only).
R2A_5_COMPLETION_BASE = "7a7935b6c34fce0cb5143ae9b4c7754cc8cdb1a2"
R2A_5_COMPLETION_BASE_TREE = "e6ae55200ef880dfb1451b3692b35c43072c502f"
R2A_5_SEMANTIC_HEAD = "8a273e41942caca4a29e5e556edbd695e25fc954"
R2A_5_SEMANTIC_TREE = "a5b85081b99deffbd6af30448fb9a1f44631d33e"
R2A_5_COMPLETION_HEAD = "c671eb696b8168ff72778761dd9adaf33060a0ba"
R2A_5_COMPLETION_TREE = "b28890a01f67263e6aba16e8fb679684ffaed198"
R2A5_COMPLETION_ARTIFACTS = {
 "docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml",
 "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml",
 "docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml",
 "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
 "docs/doctrine/reviews/r2a/dispositions_current_b/index.yaml",
 "docs/doctrine/reviews/r2a/dispositions_current_b/dispositions_0001.yaml",
}
R2A5_CLEANUP_ARTIFACTS = {
 "docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml",
 "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml",
}
R2A5_COMPLETION_BLOBS = {
 "docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml": "04fc3374a913372985a9ad4507ad348e6e8ee568",
 "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml": "45544033420aac6dbb6a3c8a9754c173236a18ae",
 "docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml": "0c8fb35b3432355ed02a6480c7e6035f27075ce1",
 "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml": "a74a84eaa5d7b6af697f878d943b1e890be7a1da",
 "docs/doctrine/reviews/r2a/dispositions_current_b/index.yaml": "586e17ffae831b8d21830cd6992f5160aa6c5e84",
 "docs/doctrine/reviews/r2a/dispositions_current_b/dispositions_0001.yaml": "3c663c6c45e5eef897d63c0bdad9ee20fd0bf4d8",
}
R2A5_INDEX = ROOT / "docs/doctrine/reviews/r2a/dispositions_current_b/index.yaml"
R2A5_SHARD = ROOT / "docs/doctrine/reviews/r2a/dispositions_current_b/dispositions_0001.yaml"
R2A5_GENERIC_AUDIT = "This audit, ledger, report, or coordination artifact records review evidence and status without becoming the semantic owner of the propositions it discusses."
R2A5_GENERIC_STATUS = "The bounded source declaration is preserved as review status evidence; it does not transfer semantic authority."
R2A5_MAPPING_TABLE = {
 "docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml": {
  "R2A-SURFACE-CORE-0023", "R2A-SURFACE-WORLD-0005", "R2A-SURFACE-WORLD-0028"},
 "docs/doctrine/reviews/afqr_r2_continuity_claim_and_owner_routing_ledger.yaml": {
  "R2A-SURFACE-CONTINUITY-0001"},
 "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml": {
  "R2A-SURFACE-CROSSPHASE-0001"},
}

def r2a5_completion_git(*args):
 return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def r2a5_object_exists(commit):
 return subprocess.run(
  ["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT,
  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
 ).returncode == 0

def r2a5_parents(commit):
 return r2a5_completion_git("rev-list", "--parents", "-n", "1", commit).split()[1:]

def r2a5_changed(left, right):
 return set(r2a5_completion_git("diff", "--name-only", left, right).splitlines())

def r2a5_no_deletions(left, right):
 return not r2a5_completion_git("diff", "--name-only", "--diff-filter=D", left, right)

def r2a5_frozen_blobs(commit=None):
 if commit is None:
  return {path: r2a5_completion_git("hash-object", path) for path in R2A5_COMPLETION_ARTIFACTS}
 return {path: r2a5_completion_git("rev-parse", f"{commit}:{path}") for path in R2A5_COMPLETION_ARTIFACTS}

def resolve_r2a5_completion():
 if r2a5_object_exists(R2A_5_COMPLETION_HEAD):
  return (R2A_5_COMPLETION_HEAD, R2A_5_SEMANTIC_HEAD, R2A_5_COMPLETION_BASE), "canonical"
 for candidate in r2a5_completion_git("rev-list", "--max-count=64", "HEAD").splitlines():
  if r2a5_completion_git("rev-parse", f"{candidate}^{{tree}}") != R2A_5_COMPLETION_TREE:
   continue
  parents = r2a5_parents(candidate)
  if len(parents) != 1 or r2a5_completion_git("rev-parse", f"{parents[0]}^{{tree}}") != R2A_5_SEMANTIC_TREE:
   continue
  semantic = parents[0]; bases = r2a5_parents(semantic)
  if len(bases) != 1 or r2a5_completion_git("rev-parse", f"{bases[0]}^{{tree}}") != R2A_5_COMPLETION_BASE_TREE:
   continue
  base = bases[0]
  valid = (
   r2a5_changed(base, candidate) == R2A5_COMPLETION_ARTIFACTS
   and r2a5_changed(base, semantic) == R2A5_COMPLETION_ARTIFACTS
   and r2a5_changed(semantic, candidate) == R2A5_CLEANUP_ARTIFACTS
   and r2a5_no_deletions(base, semantic) and r2a5_no_deletions(semantic, candidate)
   and r2a5_frozen_blobs(candidate) == R2A5_COMPLETION_BLOBS)
  if valid:
   return (candidate, semantic, base), "tree-equivalent"
 return None, "history-unavailable"

def r2a5_data():
 index=json.loads(R2A5_INDEX.read_text()); shard=json.loads(R2A5_SHARD.read_text())
 return index, shard, shard["candidate_file_dispositions"]

def r2a5_mapping_valid(index, records, contract=None, statuses=None, raw_text=None):
 evidence=[row for record in records for row in record.get("mapping_evidence", [])]
 for record in records:
  ids=record.get("mapped_surface_ids", [])
  rows=record.get("mapping_evidence", [])
  if set(ids) != {row.get("mapped_surface_id") for row in rows} or len(rows) != len(ids): return False
  if any(row.get("authority_transfer_effect") != "none" or row.get("mapping_relationship") != "originates accepted surface" for row in rows): return False
 if index.get("status") == "complete" and index["surface_mapping_coverage"].get("blocking_gap_count") != 0: return False
 if contract is not None and (contract["project_posture"].get("R2A") != "active_incomplete" or contract["project_posture"].get("R2B") != "blocked"): return False
 if statuses is not None and statuses.get("R2A-6") != "planned_not_present": return False
 if raw_text is not None and (R2A5_GENERIC_AUDIT in raw_text or R2A5_GENERIC_STATUS in raw_text): return False
 return len(evidence) == 5

def test_r2a5_successor_safe_canonical_completion_receipt():
 chain, mode = resolve_r2a5_completion()
 if mode == "history-unavailable":
  import pytest
  assert (R2A_5_COMPLETION_BASE, R2A_5_COMPLETION_BASE_TREE) == ("7a7935b6c34fce0cb5143ae9b4c7754cc8cdb1a2", "e6ae55200ef880dfb1451b3692b35c43072c502f")
  assert (R2A_5_SEMANTIC_HEAD, R2A_5_SEMANTIC_TREE) == ("8a273e41942caca4a29e5e556edbd695e25fc954", "a5b85081b99deffbd6af30448fb9a1f44631d33e")
  assert (R2A_5_COMPLETION_HEAD, R2A_5_COMPLETION_TREE) == ("c671eb696b8168ff72778761dd9adaf33060a0ba", "b28890a01f67263e6aba16e8fb679684ffaed198")
  assert set(R2A5_COMPLETION_BLOBS) == R2A5_COMPLETION_ARTIFACTS
  assert r2a5_frozen_blobs() == R2A5_COMPLETION_BLOBS
  pytest.skip("canonical R2A-5 completion history is unavailable in this isolated/rematerialized Git snapshot")
 completion, semantic, base = chain
 assert r2a5_completion_git("rev-parse", f"{completion}^{{tree}}") == R2A_5_COMPLETION_TREE
 assert r2a5_completion_git("rev-parse", f"{semantic}^{{tree}}") == R2A_5_SEMANTIC_TREE
 assert r2a5_completion_git("rev-parse", f"{base}^{{tree}}") == R2A_5_COMPLETION_BASE_TREE
 assert r2a5_parents(completion) == [semantic] and r2a5_parents(semantic) == [base]
 assert r2a5_completion_git("rev-list", "--count", f"{base}..{completion}") == "2"
 assert r2a5_completion_git("show", "-s", "--format=%s", semantic) == "Build corrected R2A-5 disposition inventory"
 assert r2a5_completion_git("show", "-s", "--format=%s", completion) == "Remove R2A-5 serializer byte drift"
 assert r2a5_changed(base, semantic) == r2a5_changed(base, completion) == R2A5_COMPLETION_ARTIFACTS
 assert r2a5_changed(semantic, completion) == R2A5_CLEANUP_ARTIFACTS
 assert r2a5_no_deletions(base, semantic) and r2a5_no_deletions(semantic, completion)
 assert r2a5_frozen_blobs(completion) == R2A5_COMPLETION_BLOBS
 subprocess.check_call(["git", "merge-base", "--is-ancestor", completion, "HEAD"], cwd=ROOT)
 frozen=json.loads(r2a5_completion_git("show", f"{completion}:{R2A5_INDEX.relative_to(ROOT).as_posix()}")); assert frozen["status"] == "complete"
 if mode == "canonical": assert chain == (R2A_5_COMPLETION_HEAD, R2A_5_SEMANTIC_HEAD, R2A_5_COMPLETION_BASE)

def test_r2a5_exact_identity_candidate_counts_and_mapping_freeze():
 index, shard, records=r2a5_data(); effect="nonauthoritative_candidate_file_disposition"
 assert (index["artifact_id"],index["artifact_version"],index["status"],index["phase"],index["authority_effect"]) == ("AFQR-R2A-5-CURRENT-B-DISPOSITION-INDEX-001","0.1.0","complete","R2A-5",effect)
 assert (shard["artifact_id"],shard["artifact_version"],shard["status"],shard["phase"],shard["authority_effect"]) == ("AFQR-R2A-5-CURRENT-B-DISPOSITION-SHARD-0001","0.1.0","complete","R2A-5",effect)
 assert index["inspected_baseline_commit"] == shard["inspected_baseline_commit"] == R2A_5_COMPLETION_BASE
 assert index["candidate_file_count"] == len(records) == 80
 ids=[r["candidate_file_id"] for r in records]; paths=[r["path"] for r in records]
 assert ids == [f"R2A-DISPOSITION-B-{n:04d}" for n in range(1,81)] and len(set(ids)) == 80
 assert paths == sorted(paths,key=lambda path:path.encode()) and len(set(paths)) == 80
 assert all(r["partition_id"]=="R2A-5" and r["inspected_commit"]==R2A_5_COMPLETION_BASE and r["controlled_match_count"]>0 and re.fullmatch(r"[0-9a-f]{40}",r["baseline_blob_sha"]) for r in records)
 assert index["counts"] == {
  "by_disposition":{"internal_nonauthoritative_pressure_only":77,"mixed_mapped_and_dismissed":3},
  "by_authority_effect":{"escalation_pressure_only":76,"implementation_presupposition_only":1,"maps_current_authority":3},
  "by_source_local_pressure_class":{"no_material_relation":80},
  "by_pressure_route":{"later_gate":77,"none":3},
  "by_top_level_candidate_path_family":{"docs/doctrine/*.md":1,"docs/doctrine/*.yaml":1,"docs/doctrine/reviews/**":78},
  "mapped_versus_unmapped":{"mapped":3,"unmapped":77},
  "by_matched_search_cluster":index["counts"]["by_matched_search_cluster"],}
 mapped={r["path"]:set(r["mapped_surface_ids"]) for r in records if r["mapped_surface_ids"]}
 assert mapped == R2A5_MAPPING_TABLE

def test_r2a5_mapping_intersection_summary_status_and_digest_guards():
 index, shard, records=r2a5_data(); coverage=index["surface_mapping_coverage"]
 assert coverage == {"mapped_candidate_count":3,"unmapped_candidate_count":77,"cross_path_mapped_candidate_count":0,"same_path_mapped_candidate_count":3,"unique_mapped_surface_count":5,"mapping_evidence_count":5,"status_evidence_count":67,"blocking_gap_count":0}
 assert index["blocking_unmapped_current_authority_candidates"] == []
 universe=set()
 for path in (CORE_SHARD,WORLD_SHARD): universe.update(row["surface_id"] for row in json.loads(path.read_text())["surface_records"])
 evidence=[row for record in records for row in record["mapping_evidence"]]
 assert len(evidence)==5 and len({row["mapped_surface_id"] for row in evidence})==5
 assert all(row["mapped_surface_id"] in universe and row["mapping_relationship"]=="originates accepted surface" and row["authority_transfer_effect"]=="none" for row in evidence)
 for row in evidence:
  loc=row["candidate_locator"]
  assert row["candidate_proposition"].strip() and row["evidence_note"].strip() and 0 < loc["line_start"] <= loc["line_end"] and loc["line_end"]-loc["line_start"] < 200
 intersections={row["candidate_path"]:set(row["accepted_surface_ids"]) for row in index["accepted_source_path_intersection"]}
 assert intersections == R2A5_MAPPING_TABLE
 assert all(row["mapping_decision"]=="originates accepted surface; materially preserved in canonical baseline; no authority transfer" for row in index["accepted_source_path_intersection"])
 raw=R2A5_SHARD.read_text(); assert R2A5_GENERIC_AUDIT not in raw and R2A5_GENERIC_STATUS not in raw
 summaries=[]
 for record in records:
  value=unicodedata.normalize("NFC",record["semantic_review_summary"]).casefold().replace(record["candidate_file_id"].casefold(),"").replace(record["path"].casefold(),"")
  summaries.append(" ".join(value.split()))
 assert all(summaries) and len(set(summaries))==80
 statuses=[r["status_evidence"] for r in records if r["status_evidence"] is not None]
 assert len(statuses)==67 and all(isinstance(x["source_status_summary"],str) and x["source_status_summary"].strip() and x["source_status_summary"] != R2A5_GENERIC_STATUS for x in statuses)
 assert hashlib.sha256(R2A5_SHARD.read_bytes()).hexdigest()==index["shards"][0]["content_sha256"] and index["shards"][0]["record_count"]==80
 shard_rel=R2A5_SHARD.relative_to(ROOT).as_posix(); index_rel=R2A5_INDEX.relative_to(ROOT).as_posix()
 assert r2a5_completion_git("hash-object",shard_rel)==R2A5_COMPLETION_BLOBS[shard_rel]
 assert r2a5_completion_git("hash-object",index_rel)==R2A5_COMPLETION_BLOBS[index_rel]

def test_r2a5_completed_status_and_posture():
 expected={f"R2A-{n}":("complete" if n<=5 else "planned_not_present") for n in range(1,13)}
 contract,clusters,partitions,manifest=map(lambda p:json.loads(p.read_text()),(CONTRACT,CLUSTERS,PARTITIONS,FILES))
 assert contract["r2a_partition_statuses"] == clusters["r2a_partition_statuses"] == expected
 assert {r["partition_id"]:r["status"] for r in partitions["partitions"]} == expected
 assert {r["partition_id"]:r["current_status"] for r in manifest["r2a_reconstruction_sequence"]} == expected
 assert contract["project_posture"] == {"R1":"complete","R2":"active_incomplete","R2-0":"complete","R2A":"active_incomplete","R2B":"blocked","R2C":"blocked","R3-R6":"blocked","RT-002G":"unauthorized","temporary_evidence_deletion":"unauthorized"}
 assert json.loads(CLUSTERS.read_text())["artifact_version"]=="0.1.5" and contract["artifact_version"]=="0.1.6" and partitions["artifact_version"]=="0.2.5"
 r2a6=next(r for r in partitions["partitions"] if r["partition_id"]=="R2A-6")
 assert r2a6["status"]=="planned_not_present" and all(not (ROOT/path).exists() for path in r2a6["planned_artifact_paths"])

def test_r2a5_mutation_and_no_authority_transfer_guards():
 index, shard, records=r2a5_data(); contract=json.loads(CONTRACT.read_text()); statuses=json.loads(CLUSTERS.read_text())["r2a_partition_statuses"]; raw=R2A5_SHARD.read_text()
 assert r2a5_mapping_valid(index,records,contract,statuses,raw)
 mapped=next(r for r in records if r["mapped_surface_ids"])
 mutations=[]
 bad=copy.deepcopy(records); next(r for r in bad if r["mapped_surface_ids"])["mapped_surface_ids"].pop(); mutations.append((index,bad,contract,statuses,raw))
 bad=copy.deepcopy(records); next(r for r in bad if r["mapped_surface_ids"])["mapped_surface_ids"].append("R2A-SURFACE-CORE-9999"); mutations.append((index,bad,contract,statuses,raw))
 bad=copy.deepcopy(records); next(r for r in bad if r["mapping_evidence"])["mapping_evidence"][0]["authority_transfer_effect"]="transfer"; mutations.append((index,bad,contract,statuses,raw))
 bad=copy.deepcopy(records); next(r for r in bad if r["mapping_evidence"])["mapping_evidence"][0]["mapping_relationship"]="unsupported"; mutations.append((index,bad,contract,statuses,raw))
 badidx=copy.deepcopy(index); badidx["surface_mapping_coverage"]["blocking_gap_count"]=1; mutations.append((badidx,records,contract,statuses,raw))
 badc=copy.deepcopy(contract); badc["project_posture"]["R2A"]="complete"; mutations.append((index,records,badc,statuses,raw))
 bads=copy.deepcopy(statuses); bads["R2A-6"]="complete"; mutations.append((index,records,contract,bads,raw))
 mutations.extend((index,records,contract,statuses,raw+x) for x in (R2A5_GENERIC_AUDIT,R2A5_GENERIC_STATUS))
 assert all(not r2a5_mapping_valid(*args) for args in mutations)
 assert shard["authority_effect"]==index["authority_effect"]=="nonauthoritative_candidate_file_disposition"
 assert all(row["authority_transfer_effect"]=="none" for record in records for row in record["mapping_evidence"])
 assert contract["project_posture"]["R2A"]=="active_incomplete" and contract["project_posture"]["R2B"]=="blocked"

# R2A-4 remains complete; its current-posture aliases now follow the R2A-5 successor.
test_r2a4_completed_status_and_posture = test_r2a5_completed_status_and_posture
test_r2a4_exact_base_scope_status_and_posture = test_r2a5_completed_status_and_posture

# R2A-6 measured-capacity amendment validation
import pytest
R2A6_CAPACITY_BASE = "a3b1b79c56d3d01607cead5e81cdd12ab725dcf6"
R2A6_CAPACITY_BASE_TREE = "fc6e56bb02c13a1d87111342d4f9064578b98735"
R2A6_CAPACITY_HEAD = "517ffd921680148225ad3c9b332c5b907a1aa2ba"
R2A6_CAPACITY_TREE = "8fa3879a9ee5a7126a407060ad91e2ba11de811a"
R2A6_CAPACITY_MANIFEST_BLOB = "45a49d050b528fe155c2c06e9b1f0fe7168ac261"
R2A6_CAPACITY_TEST_BLOB = "8179e92dfec514c5610b77906b01b9433b37c235"
R2A6_CAPACITY_PATHS = {
 "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
 "tests/test_afqr_r2a_inventory_contract.py",
}
R2A6_PLANNED_PATHS = {
 "docs/doctrine/reviews/r2a/dispositions_runtime_schema/index.yaml",
 "docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0001.yaml",
 "docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0002.yaml",
}
R2A6_PRIOR_PROHIBITIONS = {"adopt doctrine","modify runtime or production schemas","perform work assigned to a later partition"}
def r2a6_git(*args): return subprocess.run(["git",*args],cwd=ROOT,text=True,capture_output=True)
def r2a6_object_exists(commit): return r2a6_git("cat-file","-e",f"{commit}^{{commit}}").returncode==0
def r2a6_commit_tree(commit): return r2a6_git("rev-parse",f"{commit}^{{tree}}").stdout.strip()
def r2a6_parents(commit): return r2a6_git("show","-s","--format=%P",commit).stdout.strip().split()
def r2a6_changed_paths(parent,commit): return set(r2a6_git("diff","--name-only",parent,commit).stdout.splitlines())
def r2a6_blob(commit,path): return r2a6_git("rev-parse",f"{commit}:{path}").stdout.strip()

def r2a6_capacity_candidate_valid(commit,canonical=False):
 if not r2a6_object_exists(commit) or r2a6_commit_tree(commit)!=R2A6_CAPACITY_TREE: return False
 parents=r2a6_parents(commit)
 if len(parents)!=1 or r2a6_commit_tree(parents[0])!=R2A6_CAPACITY_BASE_TREE: return False
 if canonical and parents[0]!=R2A6_CAPACITY_BASE: return False
 if r2a6_changed_paths(parents[0],commit)!=R2A6_CAPACITY_PATHS: return False
 if r2a6_git("diff","--name-only","--diff-filter=D",parents[0],commit).stdout.strip(): return False
 if r2a6_blob(commit,"docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml")!=R2A6_CAPACITY_MANIFEST_BLOB: return False
 if r2a6_blob(commit,"tests/test_afqr_r2a_inventory_contract.py")!=R2A6_CAPACITY_TEST_BLOB: return False
 if canonical and r2a6_git("show","-s","--format=%B",commit).stdout.rstrip("\n")!="Adjust R2A-6 capacity for measured disposition scope": return False
 return True

def r2a6_resolve_capacity_amendment():
 if r2a6_object_exists(R2A6_CAPACITY_HEAD):
  assert r2a6_capacity_candidate_valid(R2A6_CAPACITY_HEAD,canonical=True), "canonical R2A-6 capacity-amendment object has invalid provenance"
  return ("canonical",R2A6_CAPACITY_HEAD)
 history=r2a6_git("rev-list","--max-count=64","HEAD")
 assert history.returncode==0
 for commit in history.stdout.splitlines():
  if r2a6_capacity_candidate_valid(commit): return ("tree_equivalent",commit)
 return ("unavailable",None)

def r2a6_manifest_at(commit):
 return json.loads(subprocess.check_output(["git","show",f"{commit}:docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml"],cwd=ROOT,text=True))
def r2a6_require_capacity_history():
 mode,commit=r2a6_resolve_capacity_amendment()
 if mode=="unavailable":
  pytest.skip("canonical R2A-6 capacity-amendment history is unavailable in this isolated/rematerialized Git snapshot")
 return mode,commit

def r2a6_resolved_capacity_chain():
 mode,commit=r2a6_require_capacity_history()
 parent=r2a6_parents(commit)[0]
 return mode,parent,commit

def r2a6_historical_base_manifest():
 _,parent,_=r2a6_resolved_capacity_chain()
 return r2a6_manifest_at(parent)

def r2a6_historical_manifest():
 _,_,commit=r2a6_resolved_capacity_chain()
 return r2a6_manifest_at(commit)
def r2a6_row(document): return next(row for row in document["partitions"] if row["partition_id"]=="R2A-6")

def r2a6_capacity_valid(document,base=None):
 base=base or r2a6_historical_base_manifest()
 try:
  row=r2a6_row(document)
  if document["artifact_id"]!="AFQR-R2A-PARTITION-MANIFEST-001" or document["artifact_version"]!="0.2.6" or document["partition_count"]!=12: return False
  if row["status"]!="planned_not_present" or row["maximum_changed_files"]!=8 or row["maximum_additions"]!=5000: return False
  if set(row["planned_artifact_paths"])!=R2A6_PLANNED_PATHS or len(row["planned_artifact_paths"])!=3: return False
  if row["gate_effect"]!="No gate advances and no implementation authority is granted." or set(row["prohibited_work"])!=R2A6_PRIOR_PROHIBITIONS: return False
  if any(p["maximum_changed_files"]>7 or p["maximum_additions"]>2500 for p in document["partitions"] if p["partition_id"]!="R2A-6"): return False
  restored=copy.deepcopy(document); restored["artifact_version"]=base["artifact_version"]
  restored_row=r2a6_row(restored); base_row=r2a6_row(base)
  for field in ("maximum_changed_files","maximum_additions","planned_artifact_paths"): restored_row[field]=copy.deepcopy(base_row[field])
  return restored==base
 except (KeyError,StopIteration,TypeError): return False

def test_r2a6_capacity_historical_receipt_and_scope():
 mode,commit=r2a6_require_capacity_history()
 assert r2a6_capacity_candidate_valid(commit,canonical=mode=="canonical")
 assert r2a6_changed_paths(r2a6_parents(commit)[0],commit)==R2A6_CAPACITY_PATHS

def test_r2a6_capacity_historical_manifest_identity_and_nonauthority():
 document=r2a6_historical_manifest(); row=r2a6_row(document)
 assert (document["artifact_id"],document["artifact_version"],document["partition_count"]) == ("AFQR-R2A-PARTITION-MANIFEST-001","0.2.6",12)
 assert (row["status"],row["maximum_changed_files"],row["maximum_additions"]) == ("planned_not_present",8,5000)
 assert set(row["planned_artifact_paths"])==R2A6_PLANNED_PATHS and len(row["planned_artifact_paths"])==3
 assert row["gate_effect"]=="No gate advances and no implementation authority is granted."
 assert set(row["prohibited_work"])==R2A6_PRIOR_PROHIBITIONS
 assert r2a6_capacity_valid(document)

def test_r2a6_capacity_historical_topology_and_structured_envelope():
 _,parent,commit=r2a6_resolved_capacity_chain(); base=r2a6_manifest_at(parent); historical=r2a6_manifest_at(commit)
 assert historical["partition_count"]==base["partition_count"]==12
 assert [p["partition_id"] for p in historical["partitions"]]==[p["partition_id"] for p in base["partitions"]]
 assert {p["partition_id"]:p["dependency_partitions"] for p in historical["partitions"]}=={p["partition_id"]:p["dependency_partitions"] for p in base["partitions"]}
 for field in ("disposition_precedence","disposition_rules","generated_vendor_exclusion_patterns","coordination_domain_ownership","coordination_must_not_own","sharding"):
  assert historical["ownership_rules"][field]==base["ownership_rules"][field]
 assert all(p["maximum_changed_files"]<=7 and p["maximum_additions"]<=2500 for p in historical["partitions"] if p["partition_id"]!="R2A-6")
 assert r2a6_capacity_valid(historical,base)

def test_r2a6_capacity_mutation_resistance():
 document=r2a6_historical_manifest(); mutations=[]
 for field,value in (("maximum_changed_files",9),("maximum_additions",5001),("status","active_incomplete"),("status","complete")):
  bad=copy.deepcopy(document); r2a6_row(bad)[field]=value; mutations.append(bad)
 bad=copy.deepcopy(document); next(p for p in bad["partitions"] if p["partition_id"]=="R2A-5")["maximum_changed_files"]=8; mutations.append(bad)
 bad=copy.deepcopy(document); next(p for p in bad["partitions"] if p["partition_id"]=="R2A-7")["dependency_partitions"]=[]; mutations.append(bad)
 bad=copy.deepcopy(document); bad["ownership_rules"]["disposition_precedence"]=["R2A-5","R2A-4","R2A-6","R2A-7"]; mutations.append(bad)
 bad=copy.deepcopy(document); r2a6_row(bad)["planned_artifact_paths"].pop(); mutations.append(bad)
 bad=copy.deepcopy(document); r2a6_row(bad)["planned_artifact_paths"].append("docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0003.yaml"); mutations.append(bad)
 bad=copy.deepcopy(document); r2a6_row(bad)["gate_effect"]+=" Implementation authority is granted."; mutations.append(bad)
 assert all(not r2a6_capacity_valid(bad) for bad in mutations)

def test_r2a6_capacity_historical_validation_is_future_safe():
 hypothetical=copy.deepcopy(r2a6_historical_manifest())
 hypothetical["artifact_version"]="0.2.7"; r2a6_row(hypothetical)["status"]="complete"
 r2a6_row(hypothetical)["planned_artifact_paths"].append("docs/doctrine/reviews/r2a/dispositions_runtime_schema/successor_receipt.yaml")
 assert not r2a6_capacity_valid(hypothetical)
 assert r2a6_capacity_valid(r2a6_historical_manifest())

def r2a6_prohibited_fixture_pattern_present(source):
 forbidden_fixture="r2a6_preserve_accepted_"+"r2a5_historical_manifest"
 forbidden_dispatch="R2A5_HISTORICAL_"+"POSTURE_TESTS"
 autouse_marker="autouse"+"=True"
 partitions_patch='monkeypatch.setitem(globals(),'+chr(34)+"PARTITIONS"+chr(34)
 return (forbidden_fixture in source or forbidden_dispatch in source or
         (autouse_marker in source and partitions_patch in source))

def test_r2a6_capacity_has_no_name_selected_autouse_fixture():
 capacity_source=Path(__file__).read_text().split("# R2A-6 measured-capacity amendment validation",1)[1]
 # Build the forbidden names so this guard does not make its own source match.
 forbidden_fixture="r2a6_preserve_accepted_"+"r2a5_historical_manifest"
 forbidden_dispatch="R2A5_HISTORICAL_"+"POSTURE_TESTS"
 assert forbidden_fixture not in globals() and forbidden_dispatch not in globals()
 assert forbidden_fixture not in capacity_source and forbidden_dispatch not in capacity_source
 assert not r2a6_prohibited_fixture_pattern_present(capacity_source)

def test_r2a6_capacity_allows_harmless_future_fixture():
 @pytest.fixture
 def r2a6_future_harmless_fixture(): return "future-safe"
 assert callable(r2a6_future_harmless_fixture)
 assert not r2a6_prohibited_fixture_pattern_present("@pytest.fixture\ndef r2a6_future_harmless_fixture(): pass")

def test_r2a6_capacity_successor_name_has_unmodified_current_partitions():
 original=PARTITIONS
 def dummy_future_successor():
  assert PARTITIONS is original
  return json.loads(PARTITIONS.read_text())["artifact_version"]
 rebound=dummy_future_successor
 assert rebound()=="0.2.6" and PARTITIONS is original

def test_r2a6_capacity_resolver_modes_and_wrong_canonical(monkeypatch):
 monkeypatch.setitem(globals(),"r2a6_object_exists",lambda commit:commit==R2A6_CAPACITY_HEAD)
 monkeypatch.setitem(globals(),"r2a6_capacity_candidate_valid",lambda commit,canonical=False:commit==R2A6_CAPACITY_HEAD and canonical)
 assert r2a6_resolve_capacity_amendment()==("canonical",R2A6_CAPACITY_HEAD)
 monkeypatch.setitem(globals(),"r2a6_capacity_candidate_valid",lambda commit,canonical=False:False)
 with pytest.raises(AssertionError,match="invalid provenance"): r2a6_resolve_capacity_amendment()

def test_r2a6_capacity_tree_equivalent_chain_uses_actual_parent(monkeypatch):
 equivalent_parent="1"*40; equivalent_commit="2"*40
 class Result:
  returncode=0; stdout=equivalent_commit+"\n"
 monkeypatch.setitem(globals(),"r2a6_object_exists",lambda commit:False)
 monkeypatch.setitem(globals(),"r2a6_git",lambda *args:Result())
 monkeypatch.setitem(globals(),"r2a6_capacity_candidate_valid",lambda commit,canonical=False:commit==equivalent_commit and not canonical)
 assert r2a6_resolve_capacity_amendment()==("tree_equivalent",equivalent_commit)
 monkeypatch.setitem(globals(),"r2a6_parents",lambda commit:[equivalent_parent])
 calls=[]
 monkeypatch.setitem(globals(),"r2a6_manifest_at",lambda commit:calls.append(commit) or {"resolved":commit})
 assert r2a6_historical_base_manifest()=={"resolved":equivalent_parent}
 assert r2a6_historical_manifest()=={"resolved":equivalent_commit}
 assert calls==[equivalent_parent,equivalent_commit] and R2A6_CAPACITY_BASE not in calls

def test_r2a6_capacity_history_unavailable_skips_before_git_show(monkeypatch):
 monkeypatch.setitem(globals(),"r2a6_resolve_capacity_amendment",lambda:("unavailable",None))
 monkeypatch.setitem(globals(),"r2a6_manifest_at",lambda commit:pytest.fail(f"unexpected git show {commit}"))
 with pytest.raises(pytest.skip.Exception,match="canonical R2A-6 capacity-amendment history is unavailable in this isolated/rematerialized Git snapshot"):
  r2a6_historical_base_manifest()

def test_r2a6_capacity_preserves_r2a5_current_posture():
 expected={f"R2A-{n}":("complete" if n<=5 else "planned_not_present") for n in range(1,13)}
 contract,clusters,partitions,manifest=map(lambda path:json.loads(path.read_text()),(CONTRACT,CLUSTERS,PARTITIONS,FILES))
 assert contract["r2a_partition_statuses"]==clusters["r2a_partition_statuses"]==expected
 assert {row["partition_id"]:row["status"] for row in partitions["partitions"]}==expected
 assert {row["partition_id"]:row["current_status"] for row in manifest["r2a_reconstruction_sequence"]}==expected
 assert contract["project_posture"]["R2A"]=="active_incomplete" and contract["project_posture"]["R2B"]=="blocked"
 assert partitions["artifact_version"]=="0.2.6"
 row=r2a6_row(partitions)
 assert (row["status"],row["maximum_changed_files"],row["maximum_additions"])==("planned_not_present",8,5000)
 assert all(not (ROOT/path).exists() for path in row["planned_artifact_paths"])

test_r2a5_completed_status_and_posture = test_r2a6_capacity_preserves_r2a5_current_posture
test_r2a4_completed_status_and_posture = test_r2a6_capacity_preserves_r2a5_current_posture
test_r2a4_exact_base_scope_status_and_posture = test_r2a6_capacity_preserves_r2a5_current_posture

# R2A-6 runtime/schema disposition completion validation (successor append-only).
R2A_6_BASE = "6e9b6f84826b42bef229a333ca80b3bd4ae27055"
R2A6_INDEX = REV / "r2a/dispositions_runtime_schema/index.yaml"
R2A6_SHARDS = [REV / f"r2a/dispositions_runtime_schema/dispositions_{n:04d}.yaml" for n in (1, 2)]
R2A6_AUTHORIZED = {
 "docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml",
 "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
 "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml",
 "docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml",
 "docs/doctrine/reviews/r2a/dispositions_runtime_schema/index.yaml",
 "docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0001.yaml",
 "docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0002.yaml",
 "tests/test_afqr_r2a_inventory_contract.py",
}

def r2a6_completion_data():
 index=json.loads(R2A6_INDEX.read_text(encoding="utf-8"))
 shards=[json.loads(path.read_text(encoding="utf-8")) for path in R2A6_SHARDS]
 return index,shards,[row for shard in shards for row in shard["candidate_file_dispositions"]]

def r2a6_baseline_universe():
 clusters=json.loads(git_blob(R2A_6_BASE,repo_git_path(CLUSTERS)).decode("utf-8"))
 terms={row["cluster_id"]:row["terms"] for row in clusters["clusters"]}
 rules=json.loads(PARTITIONS.read_text(encoding="utf-8"))["ownership_rules"]
 result={}
 for path in git("ls-tree","-r","--name-only",R2A_6_BASE).splitlines():
  if assign(path,rules)!="R2A-6": continue
  raw=git_blob(R2A_6_BASE,path)
  occurrences=match(path,raw,terms)
  if occurrences: result[path]=occurrences
 return result

def test_r2a6_exact_artifacts_baseline_two_shards_and_no_third():
 index,shards,records=r2a6_completion_data()
 assert index["artifact_id"]=="AFQR-R2A-6-RUNTIME-SCHEMA-DISPOSITION-INDEX-001"
 assert [s["artifact_id"] for s in shards]==[f"AFQR-R2A-6-RUNTIME-SCHEMA-DISPOSITION-SHARD-{n:04d}" for n in (1,2)]
 assert index["inspected_baseline_commit"]==R2A_6_BASE and all(s["inspected_baseline_commit"]==R2A_6_BASE for s in shards)
 assert not (R2A6_INDEX.parent/"dispositions_0003.yaml").exists()
 assert len(records)==index["candidate_file_count"]==164

def test_r2a6_deterministic_universe_order_ids_blobs_and_lexical_receipts():
 index,shards,records=r2a6_completion_data(); universe=r2a6_baseline_universe()
 assert [r["path"] for r in records]==sorted(universe,key=lambda value:value.encode("utf-8"))
 assert [r["candidate_file_id"] for r in records]==[f"R2A-DISPOSITION-RS-{n:04d}" for n in range(1,165)]
 assert len({r["candidate_file_id"] for r in records})==164 and set(universe)=={r["path"] for r in records}
 for record in records:
  occurrences=universe[record["path"]]
  assert record["controlled_match_count"]==len(occurrences)
  assert record["matched_terms"]==sorted({row[2] for row in occurrences})
  assert record["matched_search_clusters"]==sorted({row[3] for row in occurrences})
  assert record["baseline_blob_sha"]==git("rev-parse",f'{R2A_6_BASE}:{record["path"]}')
  assert record["partition_id"]=="R2A-6" and record["inspected_commit"]==R2A_6_BASE
 assert not ({r["path"] for r in records}&({r["path"] for r in r2a4_data()[1]["candidate_file_dispositions"]}|{r["path"] for r in r2a5_data()[2]}))

def test_r2a6_shards_aggregates_mappings_and_nonauthority():
 index,shards,records=r2a6_completion_data()
 assert [len(s["candidate_file_dispositions"]) for s in shards]==[82,82]
 for metadata,path,shard in zip(index["shards"],R2A6_SHARDS,shards):
  assert metadata["path"]==path.relative_to(ROOT).as_posix()
  assert metadata["record_count"]==len(shard["candidate_file_dispositions"])
  assert metadata["content_sha256"]==hashlib.sha256(path.read_bytes()).hexdigest()
 for key,field in (("by_disposition","disposition"),("by_authority_effect","authority_effect"),("by_source_local_pressure_class","source_local_pressure_class"),("by_pressure_route","pressure_route")):
  assert index["counts"][key]==dict(sorted(Counter(r[field] for r in records).items()))
 mapped=[r for r in records if r["mapped_surface_ids"]]; evidence=[e for r in records for e in r["mapping_evidence"]]
 universe={r["surface_id"] for path in (CORE_SHARD,WORLD_SHARD) for r in json.loads(path.read_text(encoding="utf-8"))["surface_records"]}
 assert index["counts"]["mapped_versus_unmapped"]=={"mapped":len(mapped),"unmapped":len(records)-len(mapped)}
 assert index["surface_mapping_coverage"]["mapping_evidence_count"]==len(evidence)
 for record in records:
  assert set(record["mapped_surface_ids"])=={row["mapped_surface_id"] for row in record["mapping_evidence"]}
  assert record["source_local_pressure_class"]=="no_material_relation"
  assert record["semantic_review_summary"].startswith(f'Semantic review of {record["path"]} ')
  assert all(not locator["matched_terms"] and not locator["matched_search_clusters"] for locator in record["representative_locators"])
 for row in evidence:
  assert row["mapped_surface_id"] in universe and row["authority_transfer_effect"]=="none"
  assert row["mapping_relationship"]=="operationalizes without authority transfer"
  assert 0<row["candidate_locator"]["line_start"]<=row["candidate_locator"]["line_end"]
 assert index["surface_mapping_coverage"]["blocking_gap_count"]==0 and index["blocking_unresolved_candidates"]==[]

def test_r2a6_status_versions_posture_and_future_boundary():
 expected={f"R2A-{n}":("complete" if n<=6 else "planned_not_present") for n in range(1,13)}
 contract,clusters,partitions,manifest=map(lambda p:json.loads(p.read_text(encoding="utf-8")),(CONTRACT,CLUSTERS,PARTITIONS,FILES))
 assert contract["r2a_partition_statuses"]==clusters["r2a_partition_statuses"]==expected
 assert {r["partition_id"]:r["status"] for r in partitions["partitions"]}==expected
 assert {r["partition_id"]:r["current_status"] for r in manifest["r2a_reconstruction_sequence"]}==expected
 assert (contract["artifact_version"],clusters["artifact_version"],partitions["artifact_version"])==("0.1.7","0.1.6","0.2.7")
 assert contract["project_posture"]["R2A"]=="active_incomplete" and contract["project_posture"]["R2B"]=="blocked"
 assert expected["R2A-7"]=="planned_not_present"
 row=next(r for r in partitions["partitions"] if r["partition_id"]=="R2A-6")
 assert row["maximum_changed_files"]==8 and row["maximum_additions"]==5000 and set(row["planned_artifact_paths"])==R2A6_PLANNED_PATHS
 r2a7=next(r for r in partitions["partitions"] if r["partition_id"]=="R2A-7")
 assert all(not (ROOT/path).exists() for path in r2a7["planned_artifact_paths"])

def test_r2a6_scope_and_capacity_after_commit():
 subprocess.check_call(["git","merge-base","--is-ancestor",R2A_6_BASE,"HEAD"],cwd=ROOT)
 changed=set(git("diff","--name-only",f"{R2A_6_BASE}...HEAD").splitlines())
 assert changed==R2A6_AUTHORIZED and len(changed)<=8
 assert not any(path.startswith(("src/","schemas/","tests/runtime/")) for path in changed)
 numstat=git("diff","--numstat",f"{R2A_6_BASE}...HEAD").splitlines()
 assert sum(int(row.split("\t")[0]) for row in numstat)<=5000 and "-\t-" not in "\n".join(numstat)

def test_r2a6_mapping_count_status_digest_and_transfer_mutations_are_detected():
 index,shards,records=r2a6_completion_data(); mapped=next(r for r in records if r["mapping_evidence"])
 bad=copy.deepcopy(mapped);bad["mapping_evidence"][0]["authority_transfer_effect"]="candidate_inherits"
 assert any(e["authority_transfer_effect"]!="none" for e in bad["mapping_evidence"])
 bad=copy.deepcopy(mapped);bad["mapped_surface_ids"].pop()
 assert set(bad["mapped_surface_ids"])!={e["mapped_surface_id"] for e in bad["mapping_evidence"]}
 bad=copy.deepcopy(index);bad["candidate_file_count"]+=1
 assert bad["candidate_file_count"]!=len(records)
 bad=copy.deepcopy(index);bad["shards"][0]["content_sha256"]="0"*64
 assert bad["shards"][0]["content_sha256"]!=hashlib.sha256(R2A6_SHARDS[0].read_bytes()).hexdigest()
 bad=copy.deepcopy(index);bad["inspected_baseline_commit"]="0"*40
 assert bad["inspected_baseline_commit"]!=R2A_6_BASE

# Obsolete predecessor/current-posture names resolve to the R2A-6 successor.
test_r2a6_capacity_preserves_r2a5_current_posture = test_r2a6_status_versions_posture_and_future_boundary
test_r2a6_capacity_successor_name_has_unmodified_current_partitions = test_r2a6_status_versions_posture_and_future_boundary
test_r2a5_completed_status_and_posture = test_r2a6_status_versions_posture_and_future_boundary
test_r2a4_completed_status_and_posture = test_r2a6_status_versions_posture_and_future_boundary
test_r2a4_exact_base_scope_status_and_posture = test_r2a6_status_versions_posture_and_future_boundary

# R2A-6 corrective semantic freeze and successor-safe R2A-5 historical posture.
R2A6_CORRECTED_MAPPING_STREAM_SHA256 = "42e7d8269af07a26f688bf1fe770c7a1e81aa42855afe56c3e1cf234be503e61"
R2A6_REJECTED_DRAFT_TEMPLATES = (
 "operationalizes the bounded accepted-owner rule represented by",
 "was reviewed independently of lexical hits; only explicit mappings below apply",
 "Semantic review of ",
)

def test_r2a5_mutation_and_no_authority_transfer_guards():
 index,shard,records=r2a5_data();raw=R2A5_SHARD.read_text(encoding="utf-8")
 contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
 historical_statuses={f"R2A-{n}":("complete" if n<=5 else "planned_not_present") for n in range(1,13)}
 assert r2a5_mapping_valid(index,records,contract,historical_statuses,raw)
 mapped=next(r for r in records if r["mapped_surface_ids"]);mutations=[]
 bad=copy.deepcopy(records);next(r for r in bad if r["mapped_surface_ids"])["mapped_surface_ids"].pop();mutations.append((index,bad,contract,historical_statuses,raw))
 bad=copy.deepcopy(records);next(r for r in bad if r["mapping_evidence"])["mapping_evidence"][0]["authority_transfer_effect"]="transfer";mutations.append((index,bad,contract,historical_statuses,raw))
 bad=copy.deepcopy(records);next(r for r in bad if r["mapping_evidence"])["mapping_evidence"][0]["mapping_relationship"]="unsupported";mutations.append((index,bad,contract,historical_statuses,raw))
 bad_statuses=copy.deepcopy(historical_statuses);bad_statuses["R2A-6"]="complete";mutations.append((index,records,contract,bad_statuses,raw))
 bad_contract=copy.deepcopy(contract);bad_contract["project_posture"]["R2A"]="complete";mutations.append((index,records,bad_contract,historical_statuses,raw))
 mutations.extend((index,records,contract,historical_statuses,raw+text) for text in (R2A5_GENERIC_AUDIT,R2A5_GENERIC_STATUS))
 assert all(not r2a5_mapping_valid(*args) for args in mutations)
 assert json.loads(CLUSTERS.read_text(encoding="utf-8"))["r2a_partition_statuses"]["R2A-6"]=="complete"
 assert all(row["authority_transfer_effect"]=="none" for record in records for row in record["mapping_evidence"])

def test_r2a6_shards_aggregates_mappings_and_nonauthority():
 index,shards,records=r2a6_completion_data();assert [len(s["candidate_file_dispositions"]) for s in shards]==[82,82]
 assert index["counts"]["mapped_versus_unmapped"]=={"mapped":13,"unmapped":151}
 assert index["counts"]["by_disposition"]=={"internal_nonauthoritative_pressure_only":151,"mapped_semantic_surface":13}
 assert index["counts"]["by_authority_effect"]=={"implementation_presupposition_only":50,"maps_current_authority":13,"no_authority_effect":101}
 assert index["counts"]["by_pressure_route"]=={"later_gate":101,"none":13,"r3_conformance":34,"r4_substrate":16}
 mapping_stream="".join(r["path"]+"\t"+",".join(r["mapped_surface_ids"])+"\n" for r in records).encode("utf-8")
 assert hashlib.sha256(mapping_stream).hexdigest()==R2A6_CORRECTED_MAPPING_STREAM_SHA256
 accepted={r["surface_id"] for path in (CORE_SHARD,WORLD_SHARD) for r in json.loads(path.read_text(encoding="utf-8"))["surface_records"]}
 evidence=[row for record in records for row in record["mapping_evidence"]];statuses=[r for r in records if r["status_evidence"] is not None]
 assert index["surface_mapping_coverage"]=={"mapped_candidate_count":13,"unmapped_candidate_count":151,"cross_path_mapped_candidate_count":13,"same_path_mapped_candidate_count":0,"unique_mapped_surface_count":4,"mapping_evidence_count":14,"status_evidence_count":99,"blocking_gap_count":0}
 assert len(evidence)==14 and len(statuses)==99
 assert Counter(row["mapped_surface_id"] for row in evidence)=={"R2A-SURFACE-WORLD-0016":6,"R2A-SURFACE-WORLD-0022":4,"R2A-SURFACE-CORE-0006":3,"R2A-SURFACE-CORE-0003":1}
 assert not ({"R2A-SURFACE-CORE-0018","R2A-SURFACE-AGENCY-0001"}&{row["mapped_surface_id"] for row in evidence})
 for metadata,path,shard in zip(index["shards"],R2A6_SHARDS,shards):
  assert metadata["path"]==path.relative_to(ROOT).as_posix() and metadata["record_count"]==len(shard["candidate_file_dispositions"])
  assert metadata["content_sha256"]==hashlib.sha256(path.read_bytes()).hexdigest()
 raw="\n".join(path.read_text(encoding="utf-8") for path in R2A6_SHARDS)
 assert not any(template in raw for template in R2A6_REJECTED_DRAFT_TEMPLATES)
 for record in records:
  assert set(record["mapped_surface_ids"])=={row["mapped_surface_id"] for row in record["mapping_evidence"]}
  assert record["semantic_review_summary"].strip() and record["representative_locators"]
  assert all(not locator["matched_terms"] and not locator["matched_search_clusters"] for locator in record["representative_locators"])
 for row in evidence:
  assert row["mapped_surface_id"] in accepted and row["authority_transfer_effect"]=="none"
  locator=row["candidate_locator"];assert 0<locator["line_start"]<=locator["line_end"] and row["candidate_proposition"].strip()
  assert not row["candidate_proposition"].startswith(("import ","from ")) and row["evidence_note"].strip()
 assert next(r for r in records if r["path"]=="schemas/handoff/extraction_repair_queue.schema.json")["mapped_surface_ids"]==[]

 assert not any(re.search(r"(?:hasattr|\.exists\(\)| is not None|artifact_type:|file_id:|review_complete: true|__dataclass_fields__)", row["candidate_proposition"], re.I) for row in evidence)
 known_unmapped={"tests/test_runtime_domain_pr_1_command_lifecycle_action_legality_service_plan.py","tests/test_runtime_domain_pr_1b_command_lifecycle_action_legality_skeleton_review.py","tests/test_runtime_domain_pr_9e_transaction_preview_packet_bridge_skeleton.py"}
 assert all(not next(r for r in records if r["path"]==path)["mapped_surface_ids"] for path in known_unmapped)
 generic_unmapped_note="File-specific review found only implementation or validation evidence at this locator. A subsystem name, symbol, type, artifact identifier, existence check, or generic validator does not establish semantic ownership; existing accepted owners retain authority."
 unmapped=[record for record in records if not record["mapped_surface_ids"]]
 assert len(unmapped)==151 and all(record["representative_locators"] for record in unmapped)
 review_notes=[]
 for record in unmapped:
  basename=Path(record["path"]).name
  for locator in record["representative_locators"]:
   note=locator["semantic_review_note"]
   assert note.strip() and note!=generic_unmapped_note and basename in note
   assert not locator["matched_terms"] and not locator["matched_search_clusters"]
   review_notes.append((record["path"],note))
 assert len({note for _,note in review_notes})==len(review_notes)
 for record in (r for r in records if "resource_consequence_math" in r["path"]):
  assert all(not row["candidate_proposition"].startswith(("import ","from ")) for row in record["mapping_evidence"])

# Successor-safe bounded discovery avoids materializing blobs outside R2A-4.
def candidates4():
 out={};rules=r2a4_current(PARTITIONS)["ownership_rules"];terms=terms4()
 for path in subprocess.check_output(["git","ls-tree","-r","--name-only",R2A_4_BASE],text=True).splitlines():
  if assign(path,rules)!="R2A-4": continue
  raw=base4(path)
  if not excluded(path,raw) and (found:=match(path,raw,terms)): out[path]=found
 return out

# R2A-7 measured-capacity and planned-path amendment validation.
R2A7_CAPACITY_BASE = "20bbf489c3fcd0abe4a45b117fbefda86fcfc97d"
R2A7_CAPACITY_PATHS = {
 "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
 "tests/test_afqr_r2a_inventory_contract.py",
}
R2A7_PLANNED_PATHS = {
 "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
 *{f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml" for number in range(1,8)},
}
R2A7_PRIOR_PROHIBITIONS = {
 "adopt doctrine",
 "modify runtime or production schemas",
 "perform work assigned to a later partition",
}

def r2a7_capacity_row(document):
 return next(row for row in document["partitions"] if row["partition_id"] == "R2A-7")

def r2a7_capacity_base_manifest():
 return json.loads(subprocess.check_output(
  ["git", "show", f"{R2A7_CAPACITY_BASE}:{repo_git_path(PARTITIONS)}"], text=True
 ))

def r2a7_capacity_valid(document, base=None):
 base = base or r2a7_capacity_base_manifest()
 try:
  row = r2a7_capacity_row(document)
  if document["artifact_id"] != "AFQR-R2A-PARTITION-MANIFEST-001": return False
  if document["artifact_version"] != "0.2.8" or document["partition_count"] != 12: return False
  if row["status"] != "planned_not_present" or row["dependency_partitions"] != ["R2A-6"]: return False
  if row["maximum_changed_files"] != 13 or row["maximum_additions"] != 16000: return False
  if set(row["planned_artifact_paths"]) != R2A7_PLANNED_PATHS or len(row["planned_artifact_paths"]) != 8: return False
  if row["candidate_path_patterns"] != ["**"]: return False
  if row["gate_effect"] != "No gate advances and source-local material stays nonauthoritative.": return False
  if set(row["prohibited_work"]) != R2A7_PRIOR_PROHIBITIONS: return False
  r2a6 = next(item for item in document["partitions"] if item["partition_id"] == "R2A-6")
  if (r2a6["status"], r2a6["maximum_changed_files"], r2a6["maximum_additions"]) != ("complete", 8, 5000): return False
  restored = copy.deepcopy(document)
  restored["artifact_version"] = base["artifact_version"]
  restored_row = r2a7_capacity_row(restored); base_row = r2a7_capacity_row(base)
  for field in ("maximum_changed_files", "maximum_additions", "planned_artifact_paths"):
   restored_row[field] = copy.deepcopy(base_row[field])
  return restored == base
 except (KeyError, StopIteration, TypeError):
  return False

def test_r2a7_capacity_exact_manifest_and_posture():
 document = json.loads(PARTITIONS.read_text(encoding="utf-8")); row = r2a7_capacity_row(document)
 assert r2a7_capacity_valid(document)
 assert (document["artifact_id"], document["artifact_version"], document["partition_count"]) == ("AFQR-R2A-PARTITION-MANIFEST-001", "0.2.8", 12)
 assert (row["status"], row["dependency_partitions"], row["candidate_path_patterns"]) == ("planned_not_present", ["R2A-6"], ["**"])
 assert (row["maximum_changed_files"], row["maximum_additions"]) == (13, 16000)
 assert set(row["planned_artifact_paths"]) == R2A7_PLANNED_PATHS and len(row["planned_artifact_paths"]) == 8
 assert all(not (ROOT / path).exists() for path in R2A7_PLANNED_PATHS)

def test_r2a7_capacity_preserves_structural_authority():
 base = r2a7_capacity_base_manifest(); current_document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
 assert [row["partition_id"] for row in current_document["partitions"]] == [row["partition_id"] for row in base["partitions"]]
 assert {row["partition_id"]: row["dependency_partitions"] for row in current_document["partitions"]} == {row["partition_id"]: row["dependency_partitions"] for row in base["partitions"]}
 for field in ("disposition_precedence", "disposition_rules", "generated_vendor_exclusion_patterns", "coordination_domain_ownership", "coordination_must_not_own", "sharding"):
  assert current_document["ownership_rules"][field] == base["ownership_rules"][field]
 for before, after in zip(base["partitions"], current_document["partitions"]):
  if after["partition_id"] not in {"R2A-6", "R2A-7"}:
   assert (after["maximum_changed_files"], after["maximum_additions"]) == (before["maximum_changed_files"], before["maximum_additions"])
 statuses = {f"R2A-{number}": ("complete" if number <= 6 else "planned_not_present") for number in range(1,13)}
 contract, clusters, file_manifest = map(lambda path: json.loads(path.read_text(encoding="utf-8")), (CONTRACT, CLUSTERS, FILES))
 assert contract["r2a_partition_statuses"] == clusters["r2a_partition_statuses"] == statuses
 assert {row["partition_id"]: row["status"] for row in current_document["partitions"]} == statuses
 assert {row["partition_id"]: row["current_status"] for row in file_manifest["r2a_reconstruction_sequence"]} == statuses
 assert contract["project_posture"]["R2A"] == "active_incomplete" and contract["project_posture"]["R2B"] == "blocked"

def test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes():
 changed = set(subprocess.check_output(["git", "diff", "--name-only", R2A7_CAPACITY_BASE], text=True).splitlines())
 assert changed == R2A7_CAPACITY_PATHS
 status = subprocess.check_output(["git", "diff", "--name-status", R2A7_CAPACITY_BASE], text=True).splitlines()
 assert all(not line.startswith("D\t") for line in status)
 assert not any(path.startswith(("src/", "schemas/", "tests/runtime/")) for path in changed)
 assert all(not (ROOT / path).exists() for path in R2A7_PLANNED_PATHS)

def test_r2a7_capacity_mutation_resistance():
 document = json.loads(PARTITIONS.read_text(encoding="utf-8")); mutations = []
 for field, value in (("maximum_changed_files", 12), ("maximum_changed_files", 14), ("maximum_additions", 15000), ("maximum_additions", 16001), ("status", "active_incomplete"), ("status", "complete")):
  bad = copy.deepcopy(document); r2a7_capacity_row(bad)[field] = value; mutations.append(bad)
 for operation in ("remove_shard", "add_shard", "replace_shard", "remove_index"):
  bad = copy.deepcopy(document); paths = r2a7_capacity_row(bad)["planned_artifact_paths"]
  if operation == "remove_shard": paths.remove("docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_0007.yaml")
  elif operation == "add_shard": paths.append("docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_0008.yaml")
  elif operation == "replace_shard": paths[1] = "docs/doctrine/reviews/r2a/dispositions_remaining/unplanned.yaml"
  else: paths.remove("docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml")
  mutations.append(bad)
 bad = copy.deepcopy(document); r2a7_capacity_row(bad)["dependency_partitions"] = ["R2A-5"]; mutations.append(bad)
 bad = copy.deepcopy(document); r2a7_capacity_row(bad)["candidate_path_patterns"] = ["docs/**"]; mutations.append(bad)
 bad = copy.deepcopy(document); bad["ownership_rules"]["disposition_precedence"] = ["R2A-5", "R2A-4", "R2A-6", "R2A-7"]; mutations.append(bad)
 bad = copy.deepcopy(document); next(row for row in bad["partitions"] if row["partition_id"] == "R2A-5")["maximum_additions"] += 1; mutations.append(bad)
 bad = copy.deepcopy(document); r2a6 = next(row for row in bad["partitions"] if row["partition_id"] == "R2A-6"); r2a6["maximum_changed_files"] = 7; mutations.append(bad)
 bad = copy.deepcopy(document); r2a7_capacity_row(bad)["gate_effect"] += " Gate advances."; mutations.append(bad)
 bad = copy.deepcopy(document); r2a7_capacity_row(bad)["prohibited_work"].pop(); mutations.append(bad)
 bad = copy.deepcopy(document); bad["partition_count"] = 13; mutations.append(bad)
 bad = copy.deepcopy(document); bad["partitions"][6], bad["partitions"][7] = bad["partitions"][7], bad["partitions"][6]; mutations.append(bad)
 assert all(not r2a7_capacity_valid(bad) for bad in mutations)

# Obsolete current-posture names resolve to the R2A-7 capacity successor while
# the accepted R2A-6 function bytes above remain frozen as historical evidence.
test_r2a6_status_versions_posture_and_future_boundary = test_r2a7_capacity_preserves_structural_authority
test_r2a6_capacity_preserves_r2a5_current_posture = test_r2a7_capacity_preserves_structural_authority
test_r2a6_capacity_successor_name_has_unmodified_current_partitions = test_r2a7_capacity_preserves_structural_authority
test_r2a5_completed_status_and_posture = test_r2a7_capacity_preserves_structural_authority
test_r2a4_completed_status_and_posture = test_r2a7_capacity_preserves_structural_authority
test_r2a4_exact_base_scope_status_and_posture = test_r2a7_capacity_preserves_structural_authority

# R2A-7 staged-execution successor-safe overrides. Historical R2A-6 completion
# and the R2A-7 capacity amendment remain frozen at their accepted boundaries;
# later R2A-7 work may materialize only paths already authorized by that amendment.
R2A_6_COMPLETION_HEAD = "20bbf489c3fcd0abe4a45b117fbefda86fcfc97d"
R2A7_CAPACITY_HEAD = "62e1565ed598345901e92dc04f3b686281418d83"
R2A7_STAGE_REQUIRED_PATHS = {
 "docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_0001.yaml",
}

def r2a7_existing_planned_paths():
 return {path for path in R2A7_PLANNED_PATHS if (ROOT / path).exists()}

def r2a7_unplanned_materialized_paths():
 root = ROOT / "docs/doctrine/reviews/r2a/dispositions_remaining"
 if not root.exists(): return set()
 return {
  path.relative_to(ROOT).as_posix()
  for path in root.rglob("*")
  if path.is_file()
 } - R2A7_PLANNED_PATHS

def test_r2a6_scope_and_capacity_after_commit():
 subprocess.check_call(["git","merge-base","--is-ancestor",R2A_6_COMPLETION_HEAD,"HEAD"],cwd=ROOT)
 changed=set(git("diff","--name-only",f"{R2A_6_BASE}...{R2A_6_COMPLETION_HEAD}").splitlines())
 assert changed==R2A6_AUTHORIZED and len(changed)<=8
 assert not any(path.startswith(("src/","schemas/","tests/runtime/")) for path in changed)
 numstat=git("diff","--numstat",f"{R2A_6_BASE}...{R2A_6_COMPLETION_HEAD}").splitlines()
 assert sum(int(row.split("\t")[0]) for row in numstat)<=5000 and "-\t-" not in "\n".join(numstat)

def test_r2a7_capacity_exact_manifest_and_posture():
 document=json.loads(PARTITIONS.read_text(encoding="utf-8")); row=r2a7_capacity_row(document)
 assert r2a7_capacity_valid(document)
 assert (document["artifact_id"],document["artifact_version"],document["partition_count"])==("AFQR-R2A-PARTITION-MANIFEST-001","0.2.8",12)
 assert (row["status"],row["dependency_partitions"],row["candidate_path_patterns"])==("planned_not_present",["R2A-6"],["**"])
 assert (row["maximum_changed_files"],row["maximum_additions"])==(13,16000)
 assert set(row["planned_artifact_paths"])==R2A7_PLANNED_PATHS and len(row["planned_artifact_paths"])==8
 existing=r2a7_existing_planned_paths()
 assert R2A7_STAGE_REQUIRED_PATHS<=existing and len(existing)<=len(R2A7_PLANNED_PATHS)
 assert not r2a7_unplanned_materialized_paths()

def test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes():
 subprocess.check_call(["git","merge-base","--is-ancestor",R2A7_CAPACITY_HEAD,"HEAD"],cwd=ROOT)
 historical=set(subprocess.check_output(["git","diff","--name-only",f"{R2A7_CAPACITY_BASE}...{R2A7_CAPACITY_HEAD}"],cwd=ROOT,text=True).splitlines())
 assert historical==R2A7_CAPACITY_PATHS
 historical_status=subprocess.check_output(["git","diff","--name-status",f"{R2A7_CAPACITY_BASE}...{R2A7_CAPACITY_HEAD}"],cwd=ROOT,text=True).splitlines()
 assert all(not line.startswith("D\t") for line in historical_status)
 changed=set(subprocess.check_output(["git","diff","--name-only",f"{R2A7_CAPACITY_BASE}...HEAD"],cwd=ROOT,text=True).splitlines())
 allowed=R2A7_CAPACITY_PATHS|R2A7_PLANNED_PATHS
 assert R2A7_STAGE_REQUIRED_PATHS<=changed<=allowed and len(changed)<=13
 assert not any(path.startswith(("src/","schemas/","tests/runtime/")) for path in changed)
 status=subprocess.check_output(["git","diff","--name-status",f"{R2A7_CAPACITY_BASE}...HEAD"],cwd=ROOT,text=True).splitlines()
 assert all(not line.startswith("D\t") for line in status)
 numstat=subprocess.check_output(["git","diff","--numstat",f"{R2A7_CAPACITY_BASE}...HEAD"],cwd=ROOT,text=True).splitlines()
 assert "-\t-" not in "\n".join(numstat)
 assert sum(int(row.split("\t")[0]) for row in numstat)<=16000
 assert not r2a7_unplanned_materialized_paths()

# R2A-7 tranche-B successor capacity controls. The exact PR #359 bytes above
# remain the literal source prefix; only obsolete R2A-7 capacity/current-posture
# definitions are successor-overridden below.
R2A7_TRANCHE_A_HEAD = "d7f2f69c53f2f683d3555e5eb0c7461e9ba8135b"
SUCCESSOR_MANIFEST_VERSION = "0.2.9"
SUCCESSOR_SHARD_COUNT = 48
SUCCESSOR_MAX_CHANGED_FILES = 51
SUCCESSOR_MAX_ADDITIONS = 16000
TRANCHE_B_MAX_CHANGED_FILES = 44
TRANCHE_B_MAX_ADDITIONS = 8000
R2A7_PLANNED_PATHS = {
 "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
 *{f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml" for number in range(1,SUCCESSOR_SHARD_COUNT+1)},
}
R2A7_TRANCHE_A_SHARDS = {
 f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml"
 for number in range(1,8)
}
R2A7_TRANCHE_B_ALLOWED_PATHS = (
 R2A7_CAPACITY_PATHS
 | {"docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml"}
 | {f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml" for number in range(8,SUCCESSOR_SHARD_COUNT+1)}
)

def r2a7_tranche_a_manifest():
 return json.loads(subprocess.check_output(
  ["git","show",f"{R2A7_TRANCHE_A_HEAD}:{repo_git_path(PARTITIONS)}"],cwd=ROOT,text=True
 ))

def r2a7_capacity_valid(document,base=None):
 base=base or r2a7_tranche_a_manifest()
 try:
  row=r2a7_capacity_row(document)
  if document["artifact_id"]!="AFQR-R2A-PARTITION-MANIFEST-001": return False
  if document["artifact_version"]!=SUCCESSOR_MANIFEST_VERSION or document["partition_count"]!=12: return False
  if row["status"]!="planned_not_present" or row["dependency_partitions"]!=["R2A-6"]: return False
  if row["maximum_changed_files"]!=SUCCESSOR_MAX_CHANGED_FILES or row["maximum_additions"]!=SUCCESSOR_MAX_ADDITIONS: return False
  if set(row["planned_artifact_paths"])!=R2A7_PLANNED_PATHS or len(row["planned_artifact_paths"])!=SUCCESSOR_SHARD_COUNT+1: return False
  if row["candidate_path_patterns"]!=["**"]: return False
  if row["gate_effect"]!="No gate advances and source-local material stays nonauthoritative.": return False
  if set(row["prohibited_work"])!=R2A7_PRIOR_PROHIBITIONS: return False
  restored=copy.deepcopy(document); restored["artifact_version"]=base["artifact_version"]
  restored_row=r2a7_capacity_row(restored); base_row=r2a7_capacity_row(base)
  for field in ("maximum_changed_files","planned_artifact_paths"):
   restored_row[field]=copy.deepcopy(base_row[field])
  return restored==base
 except (KeyError,StopIteration,TypeError):
  return False

def test_r2a7_capacity_preserves_structural_authority():
 base=r2a7_tranche_a_manifest(); current_document=json.loads(PARTITIONS.read_text(encoding="utf-8"))
 assert [row["partition_id"] for row in current_document["partitions"]]==[row["partition_id"] for row in base["partitions"]]
 assert {row["partition_id"]:row["dependency_partitions"] for row in current_document["partitions"]}=={row["partition_id"]:row["dependency_partitions"] for row in base["partitions"]}
 for field in ("disposition_precedence","disposition_rules","generated_vendor_exclusion_patterns","coordination_domain_ownership","coordination_must_not_own","sharding"):
  assert current_document["ownership_rules"][field]==base["ownership_rules"][field]
 for before,after in zip(base["partitions"],current_document["partitions"]):
  if after["partition_id"]!="R2A-7": assert after==before
 expected={f"R2A-{number}":("complete" if number<=6 else "planned_not_present") for number in range(1,13)}
 contract,clusters,file_manifest=map(lambda path:json.loads(path.read_text(encoding="utf-8")),(CONTRACT,CLUSTERS,FILES))
 assert contract["r2a_partition_statuses"]==clusters["r2a_partition_statuses"]==expected
 assert {row["partition_id"]:row["status"] for row in current_document["partitions"]}==expected
 assert {row["partition_id"]:row["current_status"] for row in file_manifest["r2a_reconstruction_sequence"]}==expected
 assert contract["project_posture"]["R2A"]=="active_incomplete" and contract["project_posture"]["R2B"]=="blocked"

def test_r2a7_capacity_exact_manifest_and_posture():
 document=json.loads(PARTITIONS.read_text(encoding="utf-8")); row=r2a7_capacity_row(document)
 assert r2a7_capacity_valid(document)
 assert (document["artifact_id"],document["artifact_version"],document["partition_count"])==("AFQR-R2A-PARTITION-MANIFEST-001",SUCCESSOR_MANIFEST_VERSION,12)
 assert (row["status"],row["dependency_partitions"],row["candidate_path_patterns"])==("planned_not_present",["R2A-6"],["**"])
 assert (row["maximum_changed_files"],row["maximum_additions"])==(SUCCESSOR_MAX_CHANGED_FILES,SUCCESSOR_MAX_ADDITIONS)
 assert set(row["planned_artifact_paths"])==R2A7_PLANNED_PATHS and len(row["planned_artifact_paths"])==SUCCESSOR_SHARD_COUNT+1
 existing=r2a7_existing_planned_paths()
 assert R2A7_TRANCHE_A_SHARDS<=existing<=R2A7_PLANNED_PATHS
 assert not r2a7_unplanned_materialized_paths()

def test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes():
 subprocess.check_call(["git","merge-base","--is-ancestor",R2A7_TRANCHE_A_HEAD,"HEAD"],cwd=ROOT)
 for path in sorted(R2A7_TRANCHE_A_SHARDS):
  assert git_blob(R2A7_TRANCHE_A_HEAD,path)==(ROOT/path).read_bytes()
 changed=set(subprocess.check_output(["git","diff","--name-only",f"{R2A7_TRANCHE_A_HEAD}...HEAD"],cwd=ROOT,text=True).splitlines())
 assert changed<=R2A7_TRANCHE_B_ALLOWED_PATHS and len(changed)<=TRANCHE_B_MAX_CHANGED_FILES
 assert not any(path.startswith(("src/","schemas/","tests/runtime/")) for path in changed)
 status=subprocess.check_output(["git","diff","--name-status",f"{R2A7_TRANCHE_A_HEAD}...HEAD"],cwd=ROOT,text=True).splitlines()
 assert all(not line.startswith("D\t") for line in status)
 numstat=subprocess.check_output(["git","diff","--numstat",f"{R2A7_TRANCHE_A_HEAD}...HEAD"],cwd=ROOT,text=True).splitlines()
 assert "-\t-" not in "\n".join(numstat)
 assert sum(int(row.split("\t")[0]) for row in numstat)<=TRANCHE_B_MAX_ADDITIONS
 global_changed=set(subprocess.check_output(["git","diff","--name-only",f"{R2A7_CAPACITY_BASE}...HEAD"],cwd=ROOT,text=True).splitlines())
 assert global_changed<=(R2A7_CAPACITY_PATHS|R2A7_PLANNED_PATHS) and len(global_changed)<=SUCCESSOR_MAX_CHANGED_FILES
 global_numstat=subprocess.check_output(["git","diff","--numstat",f"{R2A7_CAPACITY_BASE}...HEAD"],cwd=ROOT,text=True).splitlines()
 assert "-\t-" not in "\n".join(global_numstat)
 assert sum(int(row.split("\t")[0]) for row in global_numstat)<=SUCCESSOR_MAX_ADDITIONS
 assert not r2a7_unplanned_materialized_paths()

def test_r2a7_capacity_mutation_resistance():
 document=json.loads(PARTITIONS.read_text(encoding="utf-8")); mutations=[]
 for field,value in (("maximum_changed_files",SUCCESSOR_MAX_CHANGED_FILES-1),("maximum_changed_files",SUCCESSOR_MAX_CHANGED_FILES+1),("maximum_additions",SUCCESSOR_MAX_ADDITIONS-1),("maximum_additions",SUCCESSOR_MAX_ADDITIONS+1),("status","active_incomplete"),("status","complete")):
  bad=copy.deepcopy(document);r2a7_capacity_row(bad)[field]=value;mutations.append(bad)
 for operation in ("remove_shard","add_shard","replace_shard","remove_index"):
  bad=copy.deepcopy(document);paths=r2a7_capacity_row(bad)["planned_artifact_paths"]
  if operation=="remove_shard": paths.remove("docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_0048.yaml")
  elif operation=="add_shard": paths.append("docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_0049.yaml")
  elif operation=="replace_shard": paths[8]="docs/doctrine/reviews/r2a/dispositions_remaining/unplanned.yaml"
  else: paths.remove("docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml")
  mutations.append(bad)
 bad=copy.deepcopy(document);r2a7_capacity_row(bad)["dependency_partitions"]=["R2A-5"];mutations.append(bad)
 bad=copy.deepcopy(document);r2a7_capacity_row(bad)["candidate_path_patterns"]=["docs/**"];mutations.append(bad)
 bad=copy.deepcopy(document);bad["ownership_rules"]["disposition_precedence"]=["R2A-5","R2A-4","R2A-6","R2A-7"];mutations.append(bad)
 bad=copy.deepcopy(document);r2a7_capacity_row(bad)["gate_effect"]+=" Gate advances.";mutations.append(bad)
 bad=copy.deepcopy(document);r2a7_capacity_row(bad)["prohibited_work"].pop();mutations.append(bad)
 bad=copy.deepcopy(document);bad["partition_count"]=13;mutations.append(bad)
 assert all(not r2a7_capacity_valid(bad) for bad in mutations)

# Rebind obsolete current-posture aliases to the tranche-B successor after all
# historical bytes have been preserved verbatim above.
test_r2a6_status_versions_posture_and_future_boundary=test_r2a7_capacity_preserves_structural_authority
test_r2a6_capacity_preserves_r2a5_current_posture=test_r2a7_capacity_preserves_structural_authority
test_r2a6_capacity_successor_name_has_unmodified_current_partitions=test_r2a7_capacity_preserves_structural_authority
test_r2a5_completed_status_and_posture=test_r2a7_capacity_preserves_structural_authority
test_r2a4_completed_status_and_posture=test_r2a7_capacity_preserves_structural_authority
test_r2a4_exact_base_scope_status_and_posture=test_r2a7_capacity_preserves_structural_authority


# R2A-7 deterministic-stream-repair current-posture override.
#
# Historical R2A-7 capacity and tranche tests above remain preserved as
# accepted evidence.  The live manifest has now advanced from a reserved
# 48-shard capacity posture to an active-incomplete repaired prefix through
# shard 0035.  Only current-posture validators are rebound here.
R2A7_REPAIR_MANIFEST_VERSION = "0.2.10"
R2A7_REPAIR_SHARD_COUNT = 35
R2A7_REPAIR_STATUS = "active_incomplete"

R2A7_REPAIR_PLANNED_PATH_LIST = [
 "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
 *[
  f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml"
  for number in range(1, R2A7_REPAIR_SHARD_COUNT + 1)
 ],
]
R2A7_REPAIR_PLANNED_PATHS = set(R2A7_REPAIR_PLANNED_PATH_LIST)
R2A7_REPAIR_MATERIALIZED_SHARDS = {
 f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml"
 for number in range(1, R2A7_REPAIR_SHARD_COUNT + 1)
}


def r2a7_capacity_valid(document, base=None):
 base = base or r2a7_tranche_a_manifest()
 try:
  row = r2a7_capacity_row(document)

  if document["artifact_id"] != "AFQR-R2A-PARTITION-MANIFEST-001":
   return False
  if document["artifact_version"] != R2A7_REPAIR_MANIFEST_VERSION:
   return False
  if document["partition_count"] != 12:
   return False

  if row["status"] != R2A7_REPAIR_STATUS:
   return False
  if row["dependency_partitions"] != ["R2A-6"]:
   return False
  if row["candidate_path_patterns"] != ["**"]:
   return False

  if row["maximum_changed_files"] != SUCCESSOR_MAX_CHANGED_FILES:
   return False
  if row["maximum_additions"] != SUCCESSOR_MAX_ADDITIONS:
   return False

  if row["planned_artifact_paths"] != R2A7_REPAIR_PLANNED_PATH_LIST:
   return False

  if row["gate_effect"] != "No gate advances and source-local material stays nonauthoritative.":
   return False

  if set(row["prohibited_work"]) != R2A7_PRIOR_PROHIBITIONS:
   return False

  # Confirm that the repair changed only the already-authorized R2A-7
  # successor controls relative to the accepted tranche-A manifest.
  restored = copy.deepcopy(document)
  restored["artifact_version"] = base["artifact_version"]

  restored_row = r2a7_capacity_row(restored)
  base_row = r2a7_capacity_row(base)

  for field in (
   "status",
   "maximum_changed_files",
   "planned_artifact_paths",
  ):
   restored_row[field] = copy.deepcopy(base_row[field])

  return restored == base

 except (KeyError, StopIteration, TypeError):
  return False


def test_r2a7_capacity_preserves_structural_authority():
 base = r2a7_tranche_a_manifest()
 current_document = json.loads(PARTITIONS.read_text(encoding="utf-8"))

 assert [row["partition_id"] for row in current_document["partitions"]] == [
  row["partition_id"] for row in base["partitions"]
 ]

 assert {
  row["partition_id"]: row["dependency_partitions"]
  for row in current_document["partitions"]
 } == {
  row["partition_id"]: row["dependency_partitions"]
  for row in base["partitions"]
 }

 for field in (
  "disposition_precedence",
  "disposition_rules",
  "generated_vendor_exclusion_patterns",
  "coordination_domain_ownership",
  "coordination_must_not_own",
  "sharding",
 ):
  assert current_document["ownership_rules"][field] == base["ownership_rules"][field]

 for before, after in zip(base["partitions"], current_document["partitions"]):
  if after["partition_id"] != "R2A-7":
   assert after == before

 # Contract, matcher, and reconstruction-sequence files remain historical
 # posture evidence.  Only the live partition manifest records R2A-7 as
 # actively materialized.
 historical_expected = {
  f"R2A-{number}": (
   "complete" if number <= 6 else "planned_not_present"
  )
  for number in range(1, 13)
 }

 current_expected = dict(historical_expected)
 current_expected["R2A-7"] = R2A7_REPAIR_STATUS

 contract, clusters, file_manifest = map(
  lambda path: json.loads(path.read_text(encoding="utf-8")),
  (CONTRACT, CLUSTERS, FILES),
 )

 assert contract["r2a_partition_statuses"] == historical_expected
 assert clusters["r2a_partition_statuses"] == historical_expected

 assert {
  row["partition_id"]: row["status"]
  for row in current_document["partitions"]
 } == current_expected

 assert {
  row["partition_id"]: row["current_status"]
  for row in file_manifest["r2a_reconstruction_sequence"]
 } == historical_expected

 assert contract["project_posture"]["R2A"] == "active_incomplete"
 assert contract["project_posture"]["R2B"] == "blocked"


def test_r2a7_capacity_exact_manifest_and_posture():
 document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
 row = r2a7_capacity_row(document)

 assert r2a7_capacity_valid(document)

 assert (
  document["artifact_id"],
  document["artifact_version"],
  document["partition_count"],
 ) == (
  "AFQR-R2A-PARTITION-MANIFEST-001",
  R2A7_REPAIR_MANIFEST_VERSION,
  12,
 )

 assert (
  row["status"],
  row["dependency_partitions"],
  row["candidate_path_patterns"],
 ) == (
  R2A7_REPAIR_STATUS,
  ["R2A-6"],
  ["**"],
 )

 assert (
  row["maximum_changed_files"],
  row["maximum_additions"],
 ) == (
  SUCCESSOR_MAX_CHANGED_FILES,
  SUCCESSOR_MAX_ADDITIONS,
 )

 assert row["planned_artifact_paths"] == R2A7_REPAIR_PLANNED_PATH_LIST

 root = ROOT / "docs/doctrine/reviews/r2a/dispositions_remaining"

 materialized_shards = {
  path.relative_to(ROOT).as_posix()
  for path in root.glob("dispositions_*.yaml")
  if path.is_file()
 }

 assert materialized_shards == R2A7_REPAIR_MATERIALIZED_SHARDS

 all_materialized = {
  path.relative_to(ROOT).as_posix()
  for path in root.rglob("*")
  if path.is_file()
 }

 assert not (all_materialized - R2A7_REPAIR_PLANNED_PATHS)


def test_r2a7_capacity_mutation_resistance():
 document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
 mutations = []

 for field, value in (
  ("maximum_changed_files", SUCCESSOR_MAX_CHANGED_FILES - 1),
  ("maximum_changed_files", SUCCESSOR_MAX_CHANGED_FILES + 1),
  ("maximum_additions", SUCCESSOR_MAX_ADDITIONS - 1),
  ("maximum_additions", SUCCESSOR_MAX_ADDITIONS + 1),
  ("status", "planned_not_present"),
  ("status", "complete"),
 ):
  bad = copy.deepcopy(document)
  r2a7_capacity_row(bad)[field] = value
  mutations.append(bad)

 for operation in (
  "remove_shard",
  "add_shard",
  "replace_shard",
  "remove_index",
 ):
  bad = copy.deepcopy(document)
  paths = r2a7_capacity_row(bad)["planned_artifact_paths"]

  if operation == "remove_shard":
   paths.remove(
    "docs/doctrine/reviews/r2a/dispositions_remaining/"
    "dispositions_0035.yaml"
   )
  elif operation == "add_shard":
   paths.append(
    "docs/doctrine/reviews/r2a/dispositions_remaining/"
    "dispositions_0036.yaml"
   )
  elif operation == "replace_shard":
   paths[8] = (
    "docs/doctrine/reviews/r2a/dispositions_remaining/"
    "unplanned.yaml"
   )
  else:
   paths.remove(
    "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml"
   )

  mutations.append(bad)

 bad = copy.deepcopy(document)
 bad["artifact_version"] = "0.2.9"
 mutations.append(bad)

 bad = copy.deepcopy(document)
 r2a7_capacity_row(bad)["dependency_partitions"] = ["R2A-5"]
 mutations.append(bad)

 bad = copy.deepcopy(document)
 r2a7_capacity_row(bad)["candidate_path_patterns"] = ["docs/**"]
 mutations.append(bad)

 bad = copy.deepcopy(document)
 bad["ownership_rules"]["disposition_precedence"] = [
  "R2A-5", "R2A-4", "R2A-6", "R2A-7"
 ]
 mutations.append(bad)

 bad = copy.deepcopy(document)
 r2a7_capacity_row(bad)["gate_effect"] += " Gate advances."
 mutations.append(bad)

 bad = copy.deepcopy(document)
 r2a7_capacity_row(bad)["prohibited_work"].pop()
 mutations.append(bad)

 bad = copy.deepcopy(document)
 bad["partition_count"] = 13
 mutations.append(bad)

 assert all(not r2a7_capacity_valid(bad) for bad in mutations)


# Rebind the obsolete current-posture aliases one final time to the repaired
# R2A-7 successor validator.  Historical function bodies above remain intact.
test_r2a6_status_versions_posture_and_future_boundary = (
 test_r2a7_capacity_preserves_structural_authority
)
test_r2a6_capacity_preserves_r2a5_current_posture = (
 test_r2a7_capacity_preserves_structural_authority
)
test_r2a6_capacity_successor_name_has_unmodified_current_partitions = (
 test_r2a7_capacity_preserves_structural_authority
)
test_r2a5_completed_status_and_posture = (
 test_r2a7_capacity_preserves_structural_authority
)
test_r2a4_completed_status_and_posture = (
 test_r2a7_capacity_preserves_structural_authority
)
test_r2a4_exact_base_scope_status_and_posture = (
 test_r2a7_capacity_preserves_structural_authority
)


# R2A-7 deterministic repair scope override.
#
# The historical tranche-B scope test above remains preserved as evidence of
# the former append-only continuation posture.  The corrective repair has a
# deliberately different bounded shape: corrupt/replayed shards are removed,
# a deterministic regression test is added, and only the repaired R2A-7
# inventory/control paths may change.
R2A7_REPAIR_BASE = "176201f9d3a88d84e9d6628923392d7ba6c38341"

R2A7_REPAIR_EXPECTED_CHANGED_PATHS = {
 "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
 "tests/test_afqr_r2a_inventory_contract.py",
 "tests/test_afqr_r2a7_deterministic_stream_repair.py",
 *{
  "docs/doctrine/reviews/r2a/dispositions_remaining/"
  f"dispositions_{number:04d}.yaml"
  for number in range(16, 49)
 },
}

R2A7_REPAIR_EXPECTED_DELETIONS = {
 "docs/doctrine/reviews/r2a/dispositions_remaining/"
 f"dispositions_{number:04d}.yaml"
 for number in range(36, 49)
}


def _r2a7_repair_scope_is_exact_and_corrective():
 subprocess.check_call(
  ["git", "merge-base", "--is-ancestor", R2A7_REPAIR_BASE, "HEAD"],
  cwd=ROOT,
 )

 # The accepted pre-fracture prefix remains byte-identical.
 for number in range(1, 16):
  path = (
   "docs/doctrine/reviews/r2a/dispositions_remaining/"
   f"dispositions_{number:04d}.yaml"
  )
  assert git_blob(R2A7_REPAIR_BASE, path) == (ROOT / path).read_bytes()

 changed = set(
  subprocess.check_output(
   ["git", "diff", "--name-only", f"{R2A7_REPAIR_BASE}...HEAD"],
   cwd=ROOT,
   text=True,
  ).splitlines()
 )

 assert changed == R2A7_REPAIR_EXPECTED_CHANGED_PATHS

 # Runtime, schemas, and runtime tests remain outside this corrective PR.
 assert not any(
  path.startswith(("src/", "schemas/", "tests/runtime/"))
  for path in changed
 )

 status = subprocess.check_output(
  ["git", "diff", "--name-status", f"{R2A7_REPAIR_BASE}...HEAD"],
  cwd=ROOT,
  text=True,
 ).splitlines()

 deleted = {
  line.split("\t", 1)[1]
  for line in status
  if line.startswith("D\t")
 }

 assert deleted == R2A7_REPAIR_EXPECTED_DELETIONS

 # No binary payloads are introduced.
 numstat = subprocess.check_output(
  ["git", "diff", "--numstat", f"{R2A7_REPAIR_BASE}...HEAD"],
  cwd=ROOT,
  text=True,
 ).splitlines()

 assert "-\t-" not in "\n".join(numstat)

 # Current manifest/materialization controls still reject unplanned files.
 assert not r2a7_unplanned_materialized_paths()


# Rebind only the obsolete append-only scope assertion.  Its historical
# function body remains intact above for provenance.
test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes = (
 _r2a7_repair_scope_is_exact_and_corrective
)

# ---------------------------------------------------------------------------
# Certified R2A-7 completion live-posture override through R7-0299.
#
# The historical capacity, tranche, and corrective-repair function bodies
# above remain preserved.  These late-bound values advance only the live
# R2A-7 materialization posture after the accepted repair checkpoint.
# ---------------------------------------------------------------------------

R2A7_COMPLETION_BASE = "a3f425045fe0f5435569e12a5c33b757ae2a6db0"

R2A7_REPAIR_MANIFEST_VERSION = "0.2.11"
R2A7_REPAIR_SHARD_COUNT = 40
R2A7_REPAIR_STATUS = "active_incomplete"

R2A7_REPAIR_PLANNED_PATH_LIST = [
    "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
    *[
        "docs/doctrine/reviews/r2a/dispositions_remaining/"
        f"dispositions_{number:04d}.yaml"
        for number in range(1, R2A7_REPAIR_SHARD_COUNT + 1)
    ],
]
R2A7_REPAIR_PLANNED_PATHS = set(R2A7_REPAIR_PLANNED_PATH_LIST)

R2A7_REPAIR_MATERIALIZED_SHARDS = {
    "docs/doctrine/reviews/r2a/dispositions_remaining/"
    f"dispositions_{number:04d}.yaml"
    for number in range(1, R2A7_REPAIR_SHARD_COUNT + 1)
}

R2A7_COMPLETION_EXPECTED_CHANGED_PATHS = {
    "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
    "tests/test_afqr_r2a_inventory_contract.py",
    "tests/test_afqr_r2a7_deterministic_stream_repair.py",
    *{
        "docs/doctrine/reviews/r2a/dispositions_remaining/"
        f"dispositions_{number:04d}.yaml"
        for number in range(36, 41)
    },
}


def _git_names(*args):
    output = subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    )
    return {
        line.strip()
        for line in output.splitlines()
        if line.strip()
    }


def _completion_changed_paths():
    committed = _git_names(
        "diff",
        "--name-only",
        f"{R2A7_COMPLETION_BASE}...HEAD",
    )
    unstaged = _git_names("diff", "--name-only")
    staged = _git_names("diff", "--cached", "--name-only")
    untracked = _git_names(
        "ls-files",
        "--others",
        "--exclude-standard",
    )
    return committed | unstaged | staged | untracked


def _completion_deleted_paths():
    deleted = set()

    for args in (
        ("diff", "--name-status", f"{R2A7_COMPLETION_BASE}...HEAD"),
        ("diff", "--name-status"),
        ("diff", "--cached", "--name-status"),
    ):
        output = subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True,
        )

        for line in output.splitlines():
            if line.startswith("D\t"):
                deleted.add(line.split("\t", 1)[1])

    return deleted


def _completion_numstat_has_binary():
    for args in (
        ("diff", "--numstat", f"{R2A7_COMPLETION_BASE}...HEAD"),
        ("diff", "--numstat"),
        ("diff", "--cached", "--numstat"),
    ):
        output = subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True,
        )
        if any(
            line.startswith("-\t-")
            for line in output.splitlines()
        ):
            return True

    for relative in _git_names(
        "ls-files",
        "--others",
        "--exclude-standard",
    ):
        if b"\0" in (ROOT / relative).read_bytes():
            return True

    return False


def _r2a7_completion_scope_is_exact_and_bounded():
    subprocess.check_call(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            R2A7_COMPLETION_BASE,
            "HEAD",
        ],
        cwd=ROOT,
    )

    # The entire accepted repair prefix remains byte-identical.
    for number in range(1, 36):
        relative = (
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )
        assert git_blob(
            R2A7_COMPLETION_BASE,
            relative,
        ) == (ROOT / relative).read_bytes()

    changed = _completion_changed_paths()
    assert changed == R2A7_COMPLETION_EXPECTED_CHANGED_PATHS

    assert not any(
        path.startswith(("src/", "schemas/", "tests/runtime/"))
        for path in changed
    )

    assert _completion_deleted_paths() == set()
    assert not _completion_numstat_has_binary()

    assert not (
        ROOT
        / "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml"
    ).exists()


# Rebind only the live scope assertion.  Historical function bodies remain
# above as accepted evidence.
test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes = (
    _r2a7_completion_scope_is_exact_and_bounded
)

# ---------------------------------------------------------------------------
# Certified R2A-7 completion live-posture override through R7-0356.
#
# The accepted R7-0299 tranche is frozen at the #363 merge commit below.
# These late-bound values advance only the live materialization checkpoint.
# ---------------------------------------------------------------------------

R2A7_COMPLETION_0356_BASE = "6cbf63d78face218d056742b9384bb56d00700dd"

R2A7_REPAIR_MANIFEST_VERSION = "0.2.12"
R2A7_REPAIR_SHARD_COUNT = 46
R2A7_REPAIR_STATUS = "active_incomplete"

R2A7_REPAIR_PLANNED_PATH_LIST = [
    "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
    *[
        "docs/doctrine/reviews/r2a/dispositions_remaining/"
        f"dispositions_{number:04d}.yaml"
        for number in range(1, R2A7_REPAIR_SHARD_COUNT + 1)
    ],
]
R2A7_REPAIR_PLANNED_PATHS = set(R2A7_REPAIR_PLANNED_PATH_LIST)

R2A7_REPAIR_MATERIALIZED_SHARDS = {
    "docs/doctrine/reviews/r2a/dispositions_remaining/"
    f"dispositions_{number:04d}.yaml"
    for number in range(1, R2A7_REPAIR_SHARD_COUNT + 1)
}

R2A7_COMPLETION_0356_EXPECTED_CHANGED_PATHS = {
    "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
    "tests/test_afqr_r2a_inventory_contract.py",
    "tests/test_afqr_r2a7_deterministic_stream_repair.py",
    *{
        "docs/doctrine/reviews/r2a/dispositions_remaining/"
        f"dispositions_{number:04d}.yaml"
        for number in range(41, 47)
    },
}


def _completion_0356_changed_paths():
    committed = _git_names(
        "diff",
        "--name-only",
        f"{R2A7_COMPLETION_0356_BASE}...HEAD",
    )
    unstaged = _git_names("diff", "--name-only")
    staged = _git_names("diff", "--cached", "--name-only")
    untracked = _git_names(
        "ls-files",
        "--others",
        "--exclude-standard",
    )
    return committed | unstaged | staged | untracked


def _completion_0356_deleted_paths():
    deleted = set()

    for args in (
        (
            "diff",
            "--name-status",
            f"{R2A7_COMPLETION_0356_BASE}...HEAD",
        ),
        ("diff", "--name-status"),
        ("diff", "--cached", "--name-status"),
    ):
        output = subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True,
        )

        for line in output.splitlines():
            if line.startswith("D\t"):
                deleted.add(line.split("\t", 1)[1])

    return deleted


def _completion_0356_numstat_has_binary():
    for args in (
        (
            "diff",
            "--numstat",
            f"{R2A7_COMPLETION_0356_BASE}...HEAD",
        ),
        ("diff", "--numstat"),
        ("diff", "--cached", "--numstat"),
    ):
        output = subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True,
        )
        if any(
            line.startswith("-\t-")
            for line in output.splitlines()
        ):
            return True

    for relative in _git_names(
        "ls-files",
        "--others",
        "--exclude-standard",
    ):
        if b"\0" in (ROOT / relative).read_bytes():
            return True

    return False


def _r2a7_completion_0356_scope_is_exact_and_bounded():
    subprocess.check_call(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            R2A7_COMPLETION_0356_BASE,
            "HEAD",
        ],
        cwd=ROOT,
    )

    # The entire accepted through-R7-0299 payload remains byte-identical.
    for number in range(1, 41):
        relative = (
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )
        assert git_blob(
            R2A7_COMPLETION_0356_BASE,
            relative,
        ) == (ROOT / relative).read_bytes()

    changed = _completion_0356_changed_paths()
    assert changed == R2A7_COMPLETION_0356_EXPECTED_CHANGED_PATHS

    assert not any(
        path.startswith(("src/", "schemas/", "tests/runtime/"))
        for path in changed
    )

    assert _completion_0356_deleted_paths() == set()
    assert not _completion_0356_numstat_has_binary()

    index_path = (
        ROOT
        / "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml"
    )
    assert not index_path.exists()

    document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
    row = r2a7_capacity_row(document)

    assert document["artifact_version"] == "0.2.12"
    assert row["status"] == "active_incomplete"
    assert row["planned_artifact_paths"] == R2A7_REPAIR_PLANNED_PATH_LIST

    by_partition = {
        item["partition_id"]: item
        for item in document["partitions"]
    }
    assert by_partition["R2A-8"]["status"] == "planned_not_present"


# Rebind only the live R2A-7 scope assertion. Historical bodies above remain
# accepted provenance and are not edited.
test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes = (
    _r2a7_completion_0356_scope_is_exact_and_bounded
)

# ---------------------------------------------------------------------------
# Certified R2A-7 completion live-posture override through R7-0403.
#
# The accepted R7-0356 tranche is frozen at the #364 merge commit below.
# These late-bound values advance only the live materialization checkpoint.
# ---------------------------------------------------------------------------

R2A7_COMPLETION_0403_BASE = "83c9bd211048e608645426157703980e98150871"

R2A7_REPAIR_MANIFEST_VERSION = "0.2.13"
R2A7_REPAIR_SHARD_COUNT = 51
R2A7_REPAIR_STATUS = "active_incomplete"

R2A7_REPAIR_PLANNED_PATH_LIST = [
    "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
    *[
        "docs/doctrine/reviews/r2a/dispositions_remaining/"
        f"dispositions_{number:04d}.yaml"
        for number in range(1, R2A7_REPAIR_SHARD_COUNT + 1)
    ],
]
R2A7_REPAIR_PLANNED_PATHS = set(R2A7_REPAIR_PLANNED_PATH_LIST)

R2A7_REPAIR_MATERIALIZED_SHARDS = {
    "docs/doctrine/reviews/r2a/dispositions_remaining/"
    f"dispositions_{number:04d}.yaml"
    for number in range(1, R2A7_REPAIR_SHARD_COUNT + 1)
}

R2A7_COMPLETION_0403_EXPECTED_CHANGED_PATHS = {
    "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
    "tests/test_afqr_r2a_inventory_contract.py",
    "tests/test_afqr_r2a7_deterministic_stream_repair.py",
    *{
        "docs/doctrine/reviews/r2a/dispositions_remaining/"
        f"dispositions_{number:04d}.yaml"
        for number in range(47, 52)
    },
}


def _completion_0403_changed_paths():
    committed = _git_names(
        "diff",
        "--name-only",
        f"{R2A7_COMPLETION_0403_BASE}...HEAD",
    )
    unstaged = _git_names("diff", "--name-only")
    staged = _git_names("diff", "--cached", "--name-only")
    untracked = _git_names(
        "ls-files",
        "--others",
        "--exclude-standard",
    )
    return committed | unstaged | staged | untracked


def _completion_0403_deleted_paths():
    deleted = set()

    for args in (
        (
            "diff",
            "--name-status",
            f"{R2A7_COMPLETION_0403_BASE}...HEAD",
        ),
        ("diff", "--name-status"),
        ("diff", "--cached", "--name-status"),
    ):
        output = subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True,
        )

        for line in output.splitlines():
            if line.startswith("D\t"):
                deleted.add(line.split("\t", 1)[1])

    return deleted


def _completion_0403_numstat_has_binary():
    for args in (
        (
            "diff",
            "--numstat",
            f"{R2A7_COMPLETION_0403_BASE}...HEAD",
        ),
        ("diff", "--numstat"),
        ("diff", "--cached", "--numstat"),
    ):
        output = subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True,
        )
        if any(
            line.startswith("-\t-")
            for line in output.splitlines()
        ):
            return True

    for relative in _git_names(
        "ls-files",
        "--others",
        "--exclude-standard",
    ):
        if b"\0" in (ROOT / relative).read_bytes():
            return True

    return False


def _r2a7_completion_0403_scope_is_exact_and_bounded():
    subprocess.check_call(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            R2A7_COMPLETION_0403_BASE,
            "HEAD",
        ],
        cwd=ROOT,
    )

    # Entire accepted through-R7-0356 payload remains byte-identical.
    for number in range(1, 47):
        relative = (
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )
        assert git_blob(
            R2A7_COMPLETION_0403_BASE,
            relative,
        ) == (ROOT / relative).read_bytes()

    changed = _completion_0403_changed_paths()
    assert changed == R2A7_COMPLETION_0403_EXPECTED_CHANGED_PATHS

    assert not any(
        path.startswith(("src/", "schemas/", "tests/runtime/"))
        for path in changed
    )

    assert _completion_0403_deleted_paths() == set()
    assert not _completion_0403_numstat_has_binary()

    index_path = (
        ROOT
        / "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml"
    )
    assert not index_path.exists()

    document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
    row = r2a7_capacity_row(document)

    assert document["artifact_version"] == "0.2.13"
    assert row["status"] == "active_incomplete"
    assert row["planned_artifact_paths"] == R2A7_REPAIR_PLANNED_PATH_LIST

    by_partition = {
        item["partition_id"]: item
        for item in document["partitions"]
    }
    assert by_partition["R2A-8"]["status"] == "planned_not_present"


# Rebind only the live R2A-7 scope assertion. Historical bodies above remain
# accepted provenance and are not edited.
test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes = (
    _r2a7_completion_0403_scope_is_exact_and_bounded
)

# ---------------------------------------------------------------------------
# Final certified R2A-7 completion live-posture override through R7-0507.
# Historical R2A-7 scope bodies above remain accepted provenance. This block
# rebinds only the live bounded-change assertion for the final R2A-7 closeout.
# ---------------------------------------------------------------------------

R2A7_FINAL_COMPLETION_BASE = "ff01a35704067095ab01c01c977a7239fc51ec40"
R2A7_FINAL_MANIFEST_VERSION = "0.2.14"
R2A7_FINAL_SHARD_COUNT = 62
R2A7_FINAL_STATUS = "complete"
R2A7_FINAL_EXPECTED_CHANGED_PATHS = {
    "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
    "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
    "tests/test_afqr_r2a7_deterministic_stream_repair.py",
    "tests/test_afqr_r2a_inventory_contract.py",
    *{
        "docs/doctrine/reviews/r2a/dispositions_remaining/"
        f"dispositions_{number:04d}.yaml"
        for number in range(52, 63)
    },
}


def _r2a7_final_changed_paths():
    committed = _git_names("diff", "--name-only", f"{R2A7_FINAL_COMPLETION_BASE}...HEAD")
    unstaged = _git_names("diff", "--name-only")
    staged = _git_names("diff", "--cached", "--name-only")
    untracked = _git_names("ls-files", "--others", "--exclude-standard")
    return committed | unstaged | staged | untracked


def _r2a7_final_deleted_paths():
    deleted = set()
    for args in (
        ("diff", "--name-status", f"{R2A7_FINAL_COMPLETION_BASE}...HEAD"),
        ("diff", "--name-status"),
        ("diff", "--cached", "--name-status"),
    ):
        output = subprocess.check_output(["git", *args], cwd=ROOT, text=True)
        for line in output.splitlines():
            if line.startswith("D\t"):
                deleted.add(line.split("\t", 1)[1])
    return deleted


def _r2a7_final_additions_and_binary():
    additions = 0
    binary = False
    seen = set()
    for args in (
        ("diff", "--numstat", f"{R2A7_FINAL_COMPLETION_BASE}...HEAD"),
        ("diff", "--numstat"),
        ("diff", "--cached", "--numstat"),
    ):
        output = subprocess.check_output(["git", *args], cwd=ROOT, text=True)
        for line in output.splitlines():
            left, _right, path = line.split("\t", 2)
            if path in seen:
                continue
            seen.add(path)
            if left == "-":
                binary = True
            else:
                additions += int(left)
    for relative in _git_names("ls-files", "--others", "--exclude-standard"):
        if relative in seen:
            continue
        raw = (ROOT / relative).read_bytes()
        if b"\0" in raw:
            binary = True
        else:
            additions += len(raw.splitlines())
    return additions, binary


def _r2a7_final_completion_scope_is_exact_and_bounded():
    subprocess.check_call(
        ["git", "merge-base", "--is-ancestor", R2A7_FINAL_COMPLETION_BASE, "HEAD"],
        cwd=ROOT,
    )
    for number in range(1, 52):
        relative = (
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )
        assert git_blob(R2A7_FINAL_COMPLETION_BASE, relative) == (ROOT / relative).read_bytes()

    changed = _r2a7_final_changed_paths()
    assert changed == R2A7_FINAL_EXPECTED_CHANGED_PATHS
    assert len(changed) == 15
    assert not any(path.startswith(("src/", "schemas/", "tests/runtime/")) for path in changed)
    assert _r2a7_final_deleted_paths() == set()
    additions, binary = _r2a7_final_additions_and_binary()
    assert not binary
    assert additions <= 16000

    document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
    row = r2a7_capacity_row(document)
    assert document["artifact_version"] == R2A7_FINAL_MANIFEST_VERSION
    assert document["status"] == "active_incomplete"
    assert row["status"] == R2A7_FINAL_STATUS
    assert row["maximum_changed_files"] == 51
    assert row["maximum_additions"] == 16000
    assert row["planned_artifact_paths"] == [
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        *[
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
            for number in range(1, 63)
        ],
    ]
    by_partition = {item["partition_id"]: item for item in document["partitions"]}
    assert by_partition["R2A-8"]["status"] == "planned_not_present"
    index_path = ROOT / "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml"
    assert index_path.is_file()
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert index["status"] == "complete"
    assert index["candidate_file_count"] == 507
    assert not (ROOT / "docs/doctrine/reviews/r2a/aggregate_receipts/index.yaml").exists()


# Rebind only the live R2A-7 scope assertion. Historical bodies remain intact.
test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes = (
    _r2a7_final_completion_scope_is_exact_and_bounded
)

# ---------------------------------------------------------------------------
# Final R2A-7 inventory successor-binding repair.
#
# Capacity-era function bodies above are retained as historical provenance.
# Their live pytest names are rebound here because final R2A-7 completion
# lawfully changes the manifest checkpoint from active_incomplete to complete
# and materializes the final index plus shards 0052..0062.
# ---------------------------------------------------------------------------


def _r2a7_final_expected_historical_statuses():
    return {
        f"R2A-{number}": (
            "complete" if number <= 6 else "planned_not_present"
        )
        for number in range(1, 13)
    }


def _r2a7_final_manifest_is_valid(document):
    try:
        base = r2a7_tranche_a_manifest()

        if document["artifact_id"] != "AFQR-R2A-PARTITION-MANIFEST-001":
            return False
        if document["artifact_version"] != R2A7_FINAL_MANIFEST_VERSION:
            return False
        if document["status"] != "active_incomplete":
            return False
        if document["partition_count"] != 12:
            return False

        if [
            row["partition_id"]
            for row in document["partitions"]
        ] != [
            row["partition_id"]
            for row in base["partitions"]
        ]:
            return False

        for field in (
            "disposition_precedence",
            "disposition_rules",
            "generated_vendor_exclusion_patterns",
            "coordination_domain_ownership",
            "coordination_must_not_own",
            "sharding",
        ):
            if document["ownership_rules"][field] != base["ownership_rules"][field]:
                return False

        before_by_id = {
            row["partition_id"]: row
            for row in base["partitions"]
        }
        after_by_id = {
            row["partition_id"]: row
            for row in document["partitions"]
        }

        for partition_id, after in after_by_id.items():
            before = before_by_id[partition_id]
            if partition_id != "R2A-7" and after != before:
                return False

        row = after_by_id["R2A-7"]
        base_row = before_by_id["R2A-7"]

        for field in (
            "title",
            "owned_artifact_types",
            "dependency_partitions",
            "maximum_additions",
            "artifact_layout",
            "gate_effect",
            "completion_condition",
            "prohibited_work",
            "candidate_path_patterns",
        ):
            if row[field] != base_row[field]:
                return False

        if row["status"] != "complete":
            return False
        if row["maximum_changed_files"] != 51:
            return False
        if row["maximum_additions"] != 16000:
            return False
        if row["planned_artifact_paths"] != [
            "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
            *[
                "docs/doctrine/reviews/r2a/dispositions_remaining/"
                f"dispositions_{number:04d}.yaml"
                for number in range(1, 63)
            ],
        ]:
            return False

        if after_by_id["R2A-8"]["status"] != "planned_not_present":
            return False

        return True

    except (KeyError, StopIteration, TypeError):
        return False


def test_r2a7_final_preserves_structural_authority():
    current_document = json.loads(
        PARTITIONS.read_text(encoding="utf-8")
    )
    assert _r2a7_final_manifest_is_valid(current_document)

    historical_expected = _r2a7_final_expected_historical_statuses()
    current_expected = dict(historical_expected)
    current_expected["R2A-7"] = "complete"

    contract, clusters, file_manifest = map(
        lambda path: json.loads(path.read_text(encoding="utf-8")),
        (CONTRACT, CLUSTERS, FILES),
    )

    assert contract["r2a_partition_statuses"] == historical_expected
    assert clusters["r2a_partition_statuses"] == historical_expected
    assert {
        row["partition_id"]: row["current_status"]
        for row in file_manifest["r2a_reconstruction_sequence"]
    } == historical_expected

    assert {
        row["partition_id"]: row["status"]
        for row in current_document["partitions"]
    } == current_expected

    assert contract["project_posture"]["R2A"] == "active_incomplete"
    assert contract["project_posture"]["R2B"] == "blocked"


def test_r2a7_final_exact_manifest_and_posture():
    document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
    assert _r2a7_final_manifest_is_valid(document)

    row = r2a7_capacity_row(document)

    assert (
        document["artifact_id"],
        document["artifact_version"],
        document["partition_count"],
    ) == (
        "AFQR-R2A-PARTITION-MANIFEST-001",
        "0.2.14",
        12,
    )

    assert (
        row["status"],
        row["dependency_partitions"],
        row["candidate_path_patterns"],
    ) == (
        "complete",
        ["R2A-6"],
        ["**"],
    )

    assert (
        row["maximum_changed_files"],
        row["maximum_additions"],
    ) == (
        51,
        16000,
    )

    assert row["planned_artifact_paths"] == [
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        *[
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
            for number in range(1, 63)
        ],
    ]

    root = ROOT / "docs/doctrine/reviews/r2a/dispositions_remaining"

    materialized_shards = {
        path.relative_to(ROOT).as_posix()
        for path in root.glob("dispositions_*.yaml")
        if path.is_file()
    }

    assert materialized_shards == {
        "docs/doctrine/reviews/r2a/dispositions_remaining/"
        f"dispositions_{number:04d}.yaml"
        for number in range(1, 63)
    }

    all_materialized = {
        path.relative_to(ROOT).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }

    assert all_materialized == {
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        *materialized_shards,
    }

    index = json.loads(
        (root / "index.yaml").read_text(encoding="utf-8")
    )
    assert index["status"] == "complete"
    assert index["candidate_file_count"] == 507
    assert len(index["shards"]) == 62

    by_partition = {
        item["partition_id"]: item
        for item in document["partitions"]
    }
    assert by_partition["R2A-8"]["status"] == "planned_not_present"
    assert not (
        ROOT
        / "docs/doctrine/reviews/r2a/aggregate_receipts/index.yaml"
    ).exists()


def test_r2a7_final_mutation_resistance():
    document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
    assert _r2a7_final_manifest_is_valid(document)

    mutations = []

    for field, value in (
        ("maximum_changed_files", 50),
        ("maximum_changed_files", 52),
        ("maximum_additions", 15999),
        ("maximum_additions", 16001),
        ("status", "active_incomplete"),
        ("status", "planned_not_present"),
    ):
        bad = copy.deepcopy(document)
        r2a7_capacity_row(bad)[field] = value
        mutations.append(bad)

    for operation in (
        "remove_shard",
        "add_shard",
        "replace_shard",
        "remove_index",
    ):
        bad = copy.deepcopy(document)
        paths = r2a7_capacity_row(bad)["planned_artifact_paths"]

        if operation == "remove_shard":
            paths.remove(
                "docs/doctrine/reviews/r2a/dispositions_remaining/"
                "dispositions_0062.yaml"
            )
        elif operation == "add_shard":
            paths.append(
                "docs/doctrine/reviews/r2a/dispositions_remaining/"
                "dispositions_0063.yaml"
            )
        elif operation == "replace_shard":
            paths[-1] = (
                "docs/doctrine/reviews/r2a/dispositions_remaining/"
                "unplanned.yaml"
            )
        else:
            paths.remove(
                "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml"
            )

        mutations.append(bad)

    bad = copy.deepcopy(document)
    bad["artifact_version"] = "0.2.13"
    mutations.append(bad)

    bad = copy.deepcopy(document)
    r2a7_capacity_row(bad)["dependency_partitions"] = ["R2A-5"]
    mutations.append(bad)

    bad = copy.deepcopy(document)
    r2a7_capacity_row(bad)["candidate_path_patterns"] = ["docs/**"]
    mutations.append(bad)

    bad = copy.deepcopy(document)
    bad["ownership_rules"]["disposition_precedence"] = [
        "R2A-5", "R2A-4", "R2A-6", "R2A-7"
    ]
    mutations.append(bad)

    bad = copy.deepcopy(document)
    r2a7_capacity_row(bad)["gate_effect"] += " Gate advances."
    mutations.append(bad)

    bad = copy.deepcopy(document)
    r2a7_capacity_row(bad)["prohibited_work"].pop()
    mutations.append(bad)

    bad = copy.deepcopy(document)
    bad["partition_count"] = 13
    mutations.append(bad)

    bad = copy.deepcopy(document)
    next(
        row
        for row in bad["partitions"]
        if row["partition_id"] == "R2A-8"
    )["status"] = "active_incomplete"
    mutations.append(bad)

    assert all(
        not _r2a7_final_manifest_is_valid(bad)
        for bad in mutations
    )


test_r2a7_capacity_preserves_structural_authority = (
    test_r2a7_final_preserves_structural_authority
)
test_r2a7_capacity_exact_manifest_and_posture = (
    test_r2a7_final_exact_manifest_and_posture
)
test_r2a7_capacity_mutation_resistance = (
    test_r2a7_final_mutation_resistance
)

test_r2a6_status_versions_posture_and_future_boundary = (
    test_r2a7_final_preserves_structural_authority
)
test_r2a6_capacity_preserves_r2a5_current_posture = (
    test_r2a7_final_preserves_structural_authority
)
test_r2a6_capacity_successor_name_has_unmodified_current_partitions = (
    test_r2a7_final_preserves_structural_authority
)
test_r2a5_completed_status_and_posture = (
    test_r2a7_final_preserves_structural_authority
)
test_r2a4_completed_status_and_posture = (
    test_r2a7_final_preserves_structural_authority
)
test_r2a4_exact_base_scope_status_and_posture = (
    test_r2a7_final_preserves_structural_authority
)

# R2A-5 successor-baseline accounting repair v0.2.0
#
# The original R2A-5 v0.1.0 completion receipts above remain historical
# evidence for 7a7935b6c34fce0cb5143ae9b4c7754cc8cdb1a2.  These final module
# definitions validate the corrected current representation against the
# later frozen accounting universe without rewriting that history.

R2A5_SUCCESSOR_BASE = "62e1565ed598345901e92dc04f3b686281418d83"
R2A5_SUCCESSOR_VERSION = "0.2.0"

R2A5_SUCCESSOR_NEW_IDS = {
    "docs/doctrine/reviews/r2a/dispositions_current_b/dispositions_0001.yaml":
        "R2A-DISPOSITION-B-0081",
    "docs/doctrine/reviews/r2a/dispositions_current_b/index.yaml":
        "R2A-DISPOSITION-B-0082",
    "docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0001.yaml":
        "R2A-DISPOSITION-B-0083",
    "docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0002.yaml":
        "R2A-DISPOSITION-B-0084",
    "docs/doctrine/reviews/r2a/dispositions_runtime_schema/index.yaml":
        "R2A-DISPOSITION-B-0085",
}


def _r2a5_successor_blob(commit, path):
    return subprocess.check_output(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
    )


def _r2a5_successor_blob_sha(commit, path):
    return subprocess.check_output(
        ["git", "rev-parse", f"{commit}:{path}"],
        cwd=ROOT,
        text=True,
    ).strip()


def _r2a5_successor_universe():
    clusters = json.loads(
        _r2a5_successor_blob(
            R2A5_SUCCESSOR_BASE,
            "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml",
        )
    )
    partitions = json.loads(
        _r2a5_successor_blob(
            R2A5_SUCCESSOR_BASE,
            "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
        )
    )

    terms_by_cluster = {
        row["cluster_id"]: row["terms"]
        for row in clusters["clusters"]
    }
    rules = partitions["ownership_rules"]

    universe = {}

    paths = subprocess.check_output(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            R2A5_SUCCESSOR_BASE,
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()

    for path in paths:
        if assign(path, rules) != "R2A-5":
            continue

        raw = _r2a5_successor_blob(
            R2A5_SUCCESSOR_BASE,
            path,
        )
        occurrences = match(
            path,
            raw,
            terms_by_cluster,
        )

        if occurrences:
            universe[path] = occurrences

    return universe


def _r2a5_successor_historical_records():
    return json.loads(
        _r2a5_successor_blob(
            R2A5_SUCCESSOR_BASE,
            R2A5_SHARD.relative_to(ROOT).as_posix(),
        )
    )["candidate_file_dispositions"]


def test_r2a5_successor_safe_canonical_completion_receipt():
    """Preserve v0.1.0 as historical evidence, not current-file identity."""
    import pytest

    assert (
        R2A_5_COMPLETION_BASE,
        R2A_5_COMPLETION_BASE_TREE,
    ) == (
        "7a7935b6c34fce0cb5143ae9b4c7754cc8cdb1a2",
        "e6ae55200ef880dfb1451b3692b35c43072c502f",
    )

    assert (
        R2A_5_COMPLETION_HEAD,
        R2A_5_COMPLETION_TREE,
    ) == (
        "c671eb696b8168ff72778761dd9adaf33060a0ba",
        "b28890a01f67263e6aba16e8fb679684ffaed198",
    )

    if not r2a5_object_exists(R2A_5_COMPLETION_HEAD):
        pytest.skip(
            "canonical historical R2A-5 completion commit is unavailable "
            "in this shallow/rematerialized checkout; immutable receipt "
            "constants remain preserved"
        )

    assert (
        r2a5_completion_git(
            "rev-parse",
            f"{R2A_5_COMPLETION_HEAD}^{{tree}}",
        )
        == R2A_5_COMPLETION_TREE
    )

    historical_blobs = {
        path: r2a5_completion_git(
            "rev-parse",
            f"{R2A_5_COMPLETION_HEAD}:{path}",
        )
        for path in R2A5_COMPLETION_ARTIFACTS
    }

    assert historical_blobs == R2A5_COMPLETION_BLOBS

    historical_index = json.loads(
        r2a5_completion_git(
            "show",
            (
                f"{R2A_5_COMPLETION_HEAD}:"
                f"{R2A5_INDEX.relative_to(ROOT).as_posix()}"
            ),
        )
    )

    historical_shard = json.loads(
        r2a5_completion_git(
            "show",
            (
                f"{R2A_5_COMPLETION_HEAD}:"
                f"{R2A5_SHARD.relative_to(ROOT).as_posix()}"
            ),
        )
    )

    assert historical_index["artifact_version"] == "0.1.0"
    assert historical_shard["artifact_version"] == "0.1.0"
    assert historical_index["candidate_file_count"] == 80
    assert len(
        historical_shard["candidate_file_dispositions"]
    ) == 80
    assert (
        historical_index["inspected_baseline_commit"]
        == R2A_5_COMPLETION_BASE
    )
    assert (
        historical_shard["inspected_baseline_commit"]
        == R2A_5_COMPLETION_BASE
    )

    subprocess.check_call(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            R2A_5_COMPLETION_HEAD,
            "HEAD",
        ],
        cwd=ROOT,
    )


def test_r2a5_exact_identity_candidate_counts_and_mapping_freeze():
    """Validate the current 85-record successor against frozen 62e1565."""
    from collections import Counter

    index, shard, records = r2a5_data()
    effect = "nonauthoritative_candidate_file_disposition"

    assert (
        index["artifact_id"],
        index["artifact_version"],
        index["status"],
        index["phase"],
        index["authority_effect"],
    ) == (
        "AFQR-R2A-5-CURRENT-B-DISPOSITION-INDEX-001",
        R2A5_SUCCESSOR_VERSION,
        "complete",
        "R2A-5",
        effect,
    )

    assert (
        shard["artifact_id"],
        shard["artifact_version"],
        shard["status"],
        shard["phase"],
        shard["authority_effect"],
    ) == (
        "AFQR-R2A-5-CURRENT-B-DISPOSITION-SHARD-0001",
        R2A5_SUCCESSOR_VERSION,
        "complete",
        "R2A-5",
        effect,
    )

    assert (
        index["inspected_baseline_commit"]
        == shard["inspected_baseline_commit"]
        == R2A5_SUCCESSOR_BASE
    )

    assert index["candidate_file_count"] == len(records) == 85

    universe = _r2a5_successor_universe()

    assert len(universe) == 85
    assert set(universe) == {row["path"] for row in records}

    ids = [row["candidate_file_id"] for row in records]
    paths = [row["path"] for row in records]

    assert len(ids) == len(set(ids)) == 85
    assert len(paths) == len(set(paths)) == 85

    # Preserve all original path->ID identities rather than renumbering
    # records merely because five newly admitted paths sort into the middle
    # of the bytewise path order.
    historical = _r2a5_successor_historical_records()

    assert len(historical) == 80

    historical_ids = {
        row["path"]: row["candidate_file_id"]
        for row in historical
    }

    current_ids = {
        row["path"]: row["candidate_file_id"]
        for row in records
    }

    for path, candidate_id in historical_ids.items():
        assert current_ids[path] == candidate_id

    for path, candidate_id in R2A5_SUCCESSOR_NEW_IDS.items():
        assert current_ids[path] == candidate_id

    assert set(current_ids) - set(historical_ids) == set(
        R2A5_SUCCESSOR_NEW_IDS
    )

    for record in records:
        path = record["path"]
        occurrences = universe[path]

        assert record["partition_id"] == "R2A-5"
        assert record["inspected_commit"] == R2A5_SUCCESSOR_BASE

        assert record["baseline_blob_sha"] == (
            _r2a5_successor_blob_sha(
                R2A5_SUCCESSOR_BASE,
                path,
            )
        )

        assert record["controlled_match_count"] == len(occurrences)

        assert record["matched_terms"] == sorted(
            {row[2] for row in occurrences}
        )

        assert record["matched_search_clusters"] == sorted(
            {row[3] for row in occurrences}
        )

    assert index["counts"]["by_disposition"] == {
        "internal_nonauthoritative_pressure_only": 82,
        "mixed_mapped_and_dismissed": 3,
    }

    assert index["counts"]["by_authority_effect"] == {
        "escalation_pressure_only": 81,
        "implementation_presupposition_only": 1,
        "maps_current_authority": 3,
    }

    assert index["counts"]["by_source_local_pressure_class"] == {
        "no_material_relation": 85,
    }

    assert index["counts"]["by_pressure_route"] == {
        "later_gate": 82,
        "none": 3,
    }

    assert index["counts"][
        "by_top_level_candidate_path_family"
    ] == {
        "docs/doctrine/*.md": 1,
        "docs/doctrine/*.yaml": 1,
        "docs/doctrine/reviews/**": 83,
    }

    assert index["counts"]["mapped_versus_unmapped"] == {
        "mapped": 3,
        "unmapped": 82,
    }

    derived_cluster_counts = dict(
        sorted(
            Counter(
                cluster
                for record in records
                for cluster in record["matched_search_clusters"]
            ).items()
        )
    )

    assert (
        index["counts"]["by_matched_search_cluster"]
        == derived_cluster_counts
    )

    mapped = {
        row["path"]: set(row["mapped_surface_ids"])
        for row in records
        if row["mapped_surface_ids"]
    }

    assert mapped == R2A5_MAPPING_TABLE


def test_r2a5_mapping_intersection_summary_status_and_digest_guards():
    """Validate successor semantic accounting and digest closure."""
    index, shard, records = r2a5_data()

    assert index["surface_mapping_coverage"] == {
        "mapped_candidate_count": 3,
        "unmapped_candidate_count": 82,
        "cross_path_mapped_candidate_count": 0,
        "same_path_mapped_candidate_count": 3,
        "unique_mapped_surface_count": 5,
        "mapping_evidence_count": 5,
        "status_evidence_count": 72,
        "blocking_gap_count": 0,
    }

    assert (
        index["blocking_unmapped_current_authority_candidates"]
        == []
    )

    assert index["internal_pressure_coverage"] == {
        "internal_nonauthoritative_pressure_count": 82,
        "source_local_pressure_count": 0,
        "implementation_presupposition_count": 1,
        "escalation_pressure_count": 81,
        "no_authority_effect_count": 0,
    }

    mapped = [
        row
        for row in records
        if row["mapped_surface_ids"]
    ]

    evidence = [
        item
        for row in records
        for item in row["mapping_evidence"]
    ]

    assert len(mapped) == 3
    assert len(evidence) == 5

    assert all(
        item["authority_transfer_effect"] == "none"
        for item in evidence
    )

    assert all(
        item["mapping_relationship"] == "originates accepted surface"
        for item in evidence
    )

    assert {
        row["path"]: set(row["mapped_surface_ids"])
        for row in mapped
    } == R2A5_MAPPING_TABLE

    assert len(
        {
            row["semantic_review_summary"]
            for row in records
        }
    ) == 85

    assert all(
        row["semantic_review_summary"].strip()
        for row in records
    )

    assert all(
        row["representative_locators"]
        for row in records
    )

    new_records = {
        row["path"]: row
        for row in records
        if row["path"] in R2A5_SUCCESSOR_NEW_IDS
    }

    assert set(new_records) == set(R2A5_SUCCESSOR_NEW_IDS)

    for path, candidate_id in R2A5_SUCCESSOR_NEW_IDS.items():
        row = new_records[path]

        assert row["candidate_file_id"] == candidate_id
        assert (
            row["disposition"]
            == "internal_nonauthoritative_pressure_only"
        )
        assert row["authority_effect"] == "escalation_pressure_only"
        assert row["pressure_route"] == "later_gate"
        assert row["mapped_surface_ids"] == []
        assert row["mapping_evidence"] == []
        assert row["status_evidence"] is not None

    b0030 = next(
        row
        for row in records
        if row["candidate_file_id"] == "R2A-DISPOSITION-B-0030"
    )

    assert b0030["mapped_surface_ids"] == [
        "R2A-SURFACE-CROSSPHASE-0001"
    ]

    assert len(b0030["mapping_evidence"]) == 1

    b0030_evidence = b0030["mapping_evidence"][0]

    assert (
        b0030_evidence["mapped_surface_id"]
        == "R2A-SURFACE-CROSSPHASE-0001"
    )

    assert (
        b0030_evidence["mapping_relationship"]
        == "originates accepted surface"
    )

    assert (
        b0030_evidence["authority_transfer_effect"]
        == "none"
    )

    assert "coordination" in (
        b0030_evidence["candidate_proposition"].lower()
    )

    locator = b0030_evidence["candidate_locator"]

    assert 0 < locator["line_start"] <= locator["line_end"]

    actual_digest = hashlib.sha256(
        R2A5_SHARD.read_bytes()
    ).hexdigest()

    assert (
        index["shards"][0]["content_sha256"]
        == actual_digest
    )

    assert index["shards"][0]["record_count"] == 85
    assert (
        index["shards"][0]["first_candidate_file_id"]
        == "R2A-DISPOSITION-B-0001"
    )
    assert (
        index["shards"][0]["last_candidate_file_id"]
        == "R2A-DISPOSITION-B-0085"
    )

    assert any(
        "successor accounting" in line.lower()
        for line in index["completion_boundary"]
    )

    assert any(
        "does not alter later R2A-6 or R2A-7 dispositions" in line
        for line in index["completion_boundary"]
    )

    assert any(
        "No doctrine, runtime, schema, canon" in line
        for line in index["completion_boundary"]
    )

# R2A-7 certified-completion successor-safe historical scope receipt
#
# The final R2A-7 closeout was certified at 2aab80ab... .  The earlier live
# scope guard intentionally included unstaged/staged/untracked work because
# R2A-7 was then the active workstream.  Later lawful work must not mutate
# that historical receipt by being counted as part of the already-completed
# R2A-7 change set.  Validate the certified R2A-7 transition against its
# pinned completion commit and separately prove that current R2A-7 artifacts
# remain byte-identical to that certified state.

R2A7_CERTIFIED_COMPLETION_HEAD = (
    "2aab80ab4b574d4c51ba2b455cfe18199c66a2fa"
)


def _r2a7_certified_changed_paths():
    return set(
        subprocess.check_output(
            [
                "git",
                "diff",
                "--name-only",
                (
                    f"{R2A7_FINAL_COMPLETION_BASE}"
                    f"...{R2A7_CERTIFIED_COMPLETION_HEAD}"
                ),
            ],
            cwd=ROOT,
            text=True,
        ).splitlines()
    )


def _r2a7_certified_deleted_paths():
    deleted = set()

    output = subprocess.check_output(
        [
            "git",
            "diff",
            "--name-status",
            (
                f"{R2A7_FINAL_COMPLETION_BASE}"
                f"...{R2A7_CERTIFIED_COMPLETION_HEAD}"
            ),
        ],
        cwd=ROOT,
        text=True,
    )

    for line in output.splitlines():
        if line.startswith("D\t"):
            deleted.add(line.split("\t", 1)[1])

    return deleted


def _r2a7_certified_additions_and_binary():
    additions = 0
    binary = False

    output = subprocess.check_output(
        [
            "git",
            "diff",
            "--numstat",
            (
                f"{R2A7_FINAL_COMPLETION_BASE}"
                f"...{R2A7_CERTIFIED_COMPLETION_HEAD}"
            ),
        ],
        cwd=ROOT,
        text=True,
    )

    for line in output.splitlines():
        left, _right, _path = line.split("\t", 2)

        if left == "-":
            binary = True
        else:
            additions += int(left)

    return additions, binary


def test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes():
    """
    Preserve the final R2A-7 bounded-change receipt independently of later
    authorized R2A work.
    """
    subprocess.check_call(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            R2A7_FINAL_COMPLETION_BASE,
            R2A7_CERTIFIED_COMPLETION_HEAD,
        ],
        cwd=ROOT,
    )

    subprocess.check_call(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            R2A7_CERTIFIED_COMPLETION_HEAD,
            "HEAD",
        ],
        cwd=ROOT,
    )

    # Shards 0001..0051 predated the final closeout and must have remained
    # byte-identical across the certified final R2A-7 transition.
    for number in range(1, 52):
        relative = (
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )

        assert (
            git_blob(R2A7_FINAL_COMPLETION_BASE, relative)
            == git_blob(R2A7_CERTIFIED_COMPLETION_HEAD, relative)
        )

    changed = _r2a7_certified_changed_paths()

    assert changed == R2A7_FINAL_EXPECTED_CHANGED_PATHS
    assert len(changed) == 15

    assert not any(
        path.startswith(
            (
                "src/",
                "schemas/",
                "tests/runtime/",
            )
        )
        for path in changed
    )

    assert _r2a7_certified_deleted_paths() == set()

    additions, binary = _r2a7_certified_additions_and_binary()

    assert not binary
    assert additions <= 16000

    # Current R2A-7 evidence artifacts must remain exactly equal to the
    # certified completion state.  The inventory-contract test file itself
    # is intentionally excluded because later successor-safe validation is
    # lawfully appended there.
    immutable_current_paths = {
        "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        "tests/test_afqr_r2a7_deterministic_stream_repair.py",
        *{
            (
                "docs/doctrine/reviews/r2a/dispositions_remaining/"
                f"dispositions_{number:04d}.yaml"
            )
            for number in range(1, 63)
        },
    }

    for relative in immutable_current_paths:
        assert (
            git_blob(R2A7_CERTIFIED_COMPLETION_HEAD, relative)
            == (ROOT / relative).read_bytes()
        )

    historical_manifest = json.loads(
        git_blob(
            R2A7_CERTIFIED_COMPLETION_HEAD,
            "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
        )
    )

    historical_row = r2a7_capacity_row(historical_manifest)

    assert (
        historical_manifest["artifact_version"]
        == R2A7_FINAL_MANIFEST_VERSION
    )
    assert historical_manifest["status"] == "active_incomplete"
    assert historical_row["status"] == R2A7_FINAL_STATUS
    assert historical_row["maximum_changed_files"] == 51
    assert historical_row["maximum_additions"] == 16000

    historical_index = json.loads(
        git_blob(
            R2A7_CERTIFIED_COMPLETION_HEAD,
            "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        )
    )

    assert historical_index["status"] == "complete"
    assert historical_index["candidate_file_count"] == 507

    by_partition = {
        item["partition_id"]: item
        for item in historical_manifest["partitions"]
    }

    assert by_partition["R2A-8"]["status"] == "planned_not_present"


# R2A-7 WORLD-0029 reciprocity / aggregate correction v2
#
# Historical certification at 2aab80ab... remains immutable. The certified
# index's cross/same-path aggregate was itself stale: the certified records
# derive 418 cross-path / 1 same-path while the historical index stored
# 419 / 0. Current successor evidence corrects R7-0384 -> WORLD-0029 and
# records the now-derived 418 cross-path / 2 same-path state. No candidate
# identity, frozen lexical receipt, authority, or semantic ownership changes.

R2A7_W29_CERTIFIED = (
    "2aab80ab4b574d4c51ba2b455cfe18199c66a2fa"
)
R2A7_W29_FROZEN = (
    "62e1565ed598345901e92dc04f3b686281418d83"
)
R2A7_W29_TARGET = "R2A-DISPOSITION-R7-0384"
R2A7_W29_EXISTING_SAME = "R2A-DISPOSITION-R7-0380"
R2A7_W29_SURFACE_ID = "R2A-SURFACE-WORLD-0029"
R2A7_W29_SHARD = (
    "docs/doctrine/reviews/r2a/dispositions_remaining/"
    "dispositions_0049.yaml"
)
R2A7_W29_INDEX = (
    "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml"
)
R2A7_W29_PATH_DIGEST = (
    "f5ddc972d65ee8ba366da0136fb692d5b64ec2f9ce3c0690f582db53b7fed1ca"
)
R2A7_W29_PATH_BLOB_DIGEST = (
    "6c38b13c3982f608b5465af6902a51316dcff5cd256d9b079708424d5c24fec0"
)


def _r2a7_w29_blob(commit, path):
    return subprocess.check_output(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
    )


def _r2a7_w29_current_records():
    index = json.loads(
        (ROOT / R2A7_W29_INDEX).read_text(encoding="utf-8")
    )
    records = []

    for meta in index["shards"]:
        shard = json.loads(
            (ROOT / meta["path"]).read_text(encoding="utf-8")
        )
        rows = shard["candidate_file_dispositions"]
        assert len(rows) == meta["record_count"]
        records.extend(rows)

    return index, records


def _r2a7_w29_certified_records():
    index = json.loads(
        _r2a7_w29_blob(
            R2A7_W29_CERTIFIED,
            R2A7_W29_INDEX,
        )
    )
    records = []

    for meta in index["shards"]:
        shard = json.loads(
            _r2a7_w29_blob(
                R2A7_W29_CERTIFIED,
                meta["path"],
            )
        )
        records.extend(shard["candidate_file_dispositions"])

    return index, records


def _r2a7_w29_surface_paths():
    result = {}

    for relative in (
        "docs/doctrine/reviews/r2a/"
        "semantic_core_agency/surfaces_0001.yaml",
        "docs/doctrine/reviews/r2a/"
        "semantic_world_coordination/surfaces_0001.yaml",
    ):
        document = json.loads(
            (ROOT / relative).read_text(encoding="utf-8")
        )

        for row in document["surface_records"]:
            if row["semantic_status"] == "validated":
                result[row["surface_id"]] = row["path"]

    assert len(result) == 58
    return result


def _r2a7_w29_derive(records):
    surfaces = _r2a7_w29_surface_paths()

    mapped = [
        row for row in records
        if row["mapped_surface_ids"]
    ]

    same = {
        row["candidate_file_id"]
        for row in mapped
        if any(
            surfaces[sid] == row["path"]
            for sid in row["mapped_surface_ids"]
        )
    }

    cross = {
        row["candidate_file_id"]
        for row in mapped
        if any(
            surfaces[sid] != row["path"]
            for sid in row["mapped_surface_ids"]
        )
    }

    unique = {
        sid
        for row in records
        for sid in row["mapped_surface_ids"]
    }

    evidence = [
        item
        for row in records
        for item in row["mapping_evidence"]
    ]

    return {
        "mapped_candidate_count": len(mapped),
        "unmapped_candidate_count": len(records) - len(mapped),
        "cross_path_mapped_candidate_count": len(cross),
        "same_path_mapped_candidate_count": len(same),
        "unique_mapped_surface_count": len(unique),
        "mapping_evidence_count": len(evidence),
        "status_evidence_count": sum(
            row["status_evidence"] is not None
            for row in records
        ),
        "blocking_gap_count": 0,
    }, same, cross


def _r2a7_w29_digests(records):
    import hashlib

    paths = sorted(
        (row["path"] for row in records),
        key=lambda value: value.encode("utf-8"),
    )

    pairs = sorted(
        (row["path"], row["baseline_blob_sha"])
        for row in records
    )

    path_stream = (
        "\n".join(paths) + "\n"
    ).encode("utf-8")

    pair_stream = "".join(
        f"{path}\t{blob}\n"
        for path, blob in pairs
    ).encode("utf-8")

    return (
        hashlib.sha256(path_stream).hexdigest(),
        hashlib.sha256(pair_stream).hexdigest(),
    )


def test_r2a7_world0029_reciprocity_and_aggregate_correction():
    import copy
    import hashlib

    current_index, current = _r2a7_w29_current_records()
    historical_index, historical = _r2a7_w29_certified_records()

    assert len(current) == len(historical) == 507

    expected_ids = [
        f"R2A-DISPOSITION-R7-{number:04d}"
        for number in range(1, 508)
    ]

    assert [row["candidate_file_id"] for row in current] == expected_ids
    assert [row["candidate_file_id"] for row in historical] == expected_ids

    assert len({row["path"] for row in current}) == 507
    assert not any(
        row["candidate_file_id"] == "R2A-DISPOSITION-R7-0508"
        for row in current
    )

    assert _r2a7_w29_digests(current) == (
        R2A7_W29_PATH_DIGEST,
        R2A7_W29_PATH_BLOB_DIGEST,
    )

    assert _r2a7_w29_digests(historical) == (
        R2A7_W29_PATH_DIGEST,
        R2A7_W29_PATH_BLOB_DIGEST,
    )

    historical_derived, historical_same, historical_cross = (
        _r2a7_w29_derive(historical)
    )

    current_derived, current_same, current_cross = (
        _r2a7_w29_derive(current)
    )

    assert historical_derived == {
        "mapped_candidate_count": 419,
        "unmapped_candidate_count": 88,
        "cross_path_mapped_candidate_count": 418,
        "same_path_mapped_candidate_count": 1,
        "unique_mapped_surface_count": 24,
        "mapping_evidence_count": 1507,
        "status_evidence_count": 370,
        "blocking_gap_count": 0,
    }

    # Preserve and explicitly expose the historical derived-metadata defect.
    assert historical_index["surface_mapping_coverage"] == {
        "mapped_candidate_count": 419,
        "unmapped_candidate_count": 88,
        "cross_path_mapped_candidate_count": 419,
        "same_path_mapped_candidate_count": 0,
        "unique_mapped_surface_count": 24,
        "mapping_evidence_count": 1507,
        "status_evidence_count": 370,
        "blocking_gap_count": 0,
    }

    assert historical_same == {R2A7_W29_EXISTING_SAME}
    assert len(historical_cross) == 418

    assert current_derived == {
        "mapped_candidate_count": 419,
        "unmapped_candidate_count": 88,
        "cross_path_mapped_candidate_count": 418,
        "same_path_mapped_candidate_count": 2,
        "unique_mapped_surface_count": 25,
        "mapping_evidence_count": 1508,
        "status_evidence_count": 370,
        "blocking_gap_count": 0,
    }

    assert current_index["surface_mapping_coverage"] == current_derived

    assert current_same == {
        R2A7_W29_EXISTING_SAME,
        R2A7_W29_TARGET,
    }

    assert current_cross == historical_cross

    current_by_id = {
        row["candidate_file_id"]: row
        for row in current
    }
    historical_by_id = {
        row["candidate_file_id"]: row
        for row in historical
    }

    assert set(current_by_id) == set(historical_by_id)

    for candidate_id in current_by_id:
        if candidate_id == R2A7_W29_TARGET:
            continue
        assert current_by_id[candidate_id] == historical_by_id[candidate_id]

    target = current_by_id[R2A7_W29_TARGET]
    old_target = historical_by_id[R2A7_W29_TARGET]

    immutable = (
        "candidate_file_id",
        "partition_id",
        "path",
        "inspected_commit",
        "baseline_blob_sha",
        "controlled_match_count",
        "matched_terms",
        "matched_search_clusters",
        "disposition",
        "source_local_pressure_class",
        "authority_effect",
        "pressure_route",
        "status_evidence",
    )

    for field in immutable:
        assert target[field] == old_target[field]

    assert {
        field
        for field in target
        if target[field] != old_target[field]
    } == {
        "representative_locators",
        "mapped_surface_ids",
        "semantic_review_summary",
        "mapping_evidence",
    }

    evidence = [
        row
        for row in target["mapping_evidence"]
        if row["mapped_surface_id"] == R2A7_W29_SURFACE_ID
    ]

    assert len(evidence) == 1
    evidence = evidence[0]

    assert evidence["candidate_locator"] == {
        "locator_kind": "line_range_only",
        "locator_value": None,
        "line_start": 47,
        "line_end": 49,
    }
    assert evidence["mapping_relationship"] == "governed by accepted surface"
    assert evidence["authority_transfer_effect"] == "none"

    source = _r2a7_w29_blob(
        R2A7_W29_FROZEN,
        target["path"],
    ).decode("utf-8").splitlines()

    bounded = "\n".join(source[46:49])

    assert all(
        token in bounded
        for token in (
            "DEP-094",
            "AFQR-19",
            "AFQR-20",
            "contact_targeting",
            "semantic_type_owner",
        )
    )

    shard_meta = next(
        row
        for row in current_index["shards"]
        if row["path"] == R2A7_W29_SHARD
    )

    assert shard_meta["content_sha256"] == hashlib.sha256(
        (ROOT / R2A7_W29_SHARD).read_bytes()
    ).hexdigest()

    # Only the shard hash and derived coverage may differ in the index.
    normalized = copy.deepcopy(current_index)
    historical_shard_meta = next(
        row
        for row in historical_index["shards"]
        if row["path"] == R2A7_W29_SHARD
    )
    normalized_shard_meta = next(
        row
        for row in normalized["shards"]
        if row["path"] == R2A7_W29_SHARD
    )

    normalized_shard_meta["content_sha256"] = (
        historical_shard_meta["content_sha256"]
    )
    normalized["surface_mapping_coverage"] = (
        historical_index["surface_mapping_coverage"]
    )

    assert normalized == historical_index

    # Adversarial: authority transfer cannot be manufactured.
    bad = copy.deepcopy(target)
    next(
        row
        for row in bad["mapping_evidence"]
        if row["mapped_surface_id"] == R2A7_W29_SURFACE_ID
    )["authority_transfer_effect"] = "candidate_inherits"
    assert bad != target

    # Adversarial: frozen lexical identity cannot move.
    bad = copy.deepcopy(target)
    bad["controlled_match_count"] += 1
    assert bad["controlled_match_count"] != target["controlled_match_count"]

    # Adversarial: R7-0508 is outside the certified stream.
    bad_stream = copy.deepcopy(current)
    fake = copy.deepcopy(bad_stream[-1])
    fake["candidate_file_id"] = "R2A-DISPOSITION-R7-0508"
    bad_stream.append(fake)
    assert len(bad_stream) != 507


def test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes():
    """
    Historical R2A-7 completion remains pinned to certification. Current
    successor validation allows the bounded WORLD-0029 evidence repair and
    later global partition-manifest progression, including R2A-8 status
    advancement.
    """
    subprocess.check_call(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            R2A7_FINAL_COMPLETION_BASE,
            R2A7_W29_CERTIFIED,
        ],
        cwd=ROOT,
    )

    subprocess.check_call(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            R2A7_W29_CERTIFIED,
            "HEAD",
        ],
        cwd=ROOT,
    )

    historical_changed = set(
        subprocess.check_output(
            [
                "git",
                "diff",
                "--name-only",
                (
                    f"{R2A7_FINAL_COMPLETION_BASE}"
                    f"...{R2A7_W29_CERTIFIED}"
                ),
            ],
            cwd=ROOT,
            text=True,
        ).splitlines()
    )

    assert historical_changed == R2A7_FINAL_EXPECTED_CHANGED_PATHS

    # The historical manifest remains immutable evidence that R2A-8 had
    # not yet begun at certification.
    historical_manifest = json.loads(
        _r2a7_w29_blob(
            R2A7_W29_CERTIFIED,
            "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
        )
    )

    historical_partitions = {
        row["partition_id"]: row
        for row in historical_manifest["partitions"]
    }

    assert historical_partitions["R2A-7"]["status"] == "complete"
    assert (
        historical_partitions["R2A-8"]["status"]
        == "planned_not_present"
    )

    # Current law constrains R2A-7, not the future R2A-8 status.
    current_manifest = json.loads(
        (
            ROOT
            / "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml"
        ).read_text(encoding="utf-8")
    )

    current_partitions = {
        row["partition_id"]: row
        for row in current_manifest["partitions"]
    }

    assert current_partitions["R2A-7"]["status"] == "complete"

    current_index, current = _r2a7_w29_current_records()
    historical_index, historical = _r2a7_w29_certified_records()

    assert current_index["candidate_file_count"] == 507
    assert historical_index["candidate_file_count"] == 507

    assert _r2a7_w29_digests(current) == (
        R2A7_W29_PATH_DIGEST,
        R2A7_W29_PATH_BLOB_DIGEST,
    )

    # Every R2A-7 shard except the expressly repaired shard remains
    # byte-identical to certified completion.
    for metadata in historical_index["shards"]:
        relative = metadata["path"]

        if relative == R2A7_W29_SHARD:
            continue

        assert (
            _r2a7_w29_blob(R2A7_W29_CERTIFIED, relative)
            == (ROOT / relative).read_bytes()
        )

    # The repaired shard differs only in R7-0384, proven by the dedicated
    # reciprocity test above. The deterministic stream verifier itself
    # remains certified and unchanged.
    deterministic_test = (
        "tests/test_afqr_r2a7_deterministic_stream_repair.py"
    )

    assert (
        _r2a7_w29_blob(
            R2A7_W29_CERTIFIED,
            deterministic_test,
        )
        == (ROOT / deterministic_test).read_bytes()
    )

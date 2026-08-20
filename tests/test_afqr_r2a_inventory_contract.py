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
 assert subprocess.check_output(["git","merge-base",R2A_4_BASE,"HEAD"],text=True).strip()==R2A_4_BASE
 assert set(subprocess.check_output(["git","diff","--name-only",f"{R2A_4_BASE}...HEAD"],text=True).splitlines())==R2A4_AUTHORIZED
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
 changed=subprocess.check_output(["git","diff","--name-only",f"{R2A_4_BASE}...HEAD"],text=True).splitlines();assert set(changed)==R2A4_AUTHORIZED and not subprocess.check_output(["git","diff","--name-only","--diff-filter=D",f"{R2A_4_BASE}...HEAD"],text=True).strip()
 num=subprocess.check_output(["git","diff","--numstat",f"{R2A_4_BASE}...HEAD"],text=True).splitlines();assert sum(int(x.split()[0]) for x in num)<=2500
 for p in changed:
  raw=git_blob("HEAD",p);assert len(raw)<=300*1024 and b"\0" not in raw and max(map(len,raw.splitlines()),default=0)<=1000
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

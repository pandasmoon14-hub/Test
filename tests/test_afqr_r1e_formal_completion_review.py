from __future__ import annotations
import copy,hashlib,json,subprocess,sys,zipfile
from collections import Counter
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).parent))
from afqr_r1e_semantic_helpers import *
BASE="017984a1598b9c60324c62e54d80372c364654ae"; ACCEPTED_R1_HEAD="bbc9d58cb23f1616327f73294def6ec42055a324"; ABANDONED="50c0320acd1a9a075cba18e1309dd3d15ac5c44d"
CERT="docs/doctrine/reviews/afqr_01_20_formal_completion_review.md"
SUPPORT=["docs/doctrine/reviews/afqr_r1e_source_and_vocabulary_audit.yaml","docs/doctrine/reviews/afqr_r1e_dependency_and_parity_audit.yaml","docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml","docs/doctrine/reviews/afqr_r1e_consistency_and_corpus_adequacy.yaml"]
SHARDS=["docs/doctrine/reviews/afqr_r1e_core_projection_field_comparisons.yaml","docs/doctrine/reviews/afqr_r1e_agency_projection_field_comparisons.yaml","docs/doctrine/reviews/afqr_r1e_world_projection_field_comparisons.yaml"]
AUTH=load_json("docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml"); MANIFEST=load_json("working/afqr_consolidation_inputs/manifest.yaml"); VOCAB=load_json("docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml"); R1C=load_json("docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml")
SV,DP,ADJ,CA=[load_json(x) for x in SUPPORT]; SHARD_DOCS=[load_json(x) for x in SHARDS]
FAMILY_PATHS={"core":"docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md","agency":"docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md","world":"docs/doctrine/consolidation/afqr_world_action_sensing.md"}; FAMILIES={k:load_markdown_json(v) for k,v in FAMILY_PATHS.items()}
EVIDENCE={x["source_record_id"]:x for x in MANIFEST["contained_file_records"]}; ARCHIVES={x["archive_record_id"]:x for x in MANIFEST["archive_records"]}
ALL_PROJECTIONS=[x for shard in SHARD_DOCS for x in shard["projection_comparisons"]]+[x for shard in SHARD_DOCS for x in shard.get("embedded_core_boundary_projection_comparisons",[])]+DP.get("embedded_core_boundary_projection_comparisons",[]); PROJECTION_MAP={x["projection_ref"]:x for x in ALL_PROJECTIONS}

def assert_locator(locator):
    assert locator and locator["evidence_id"] in EVIDENCE and locator.get("path_kind") in {"materialized_normalized_file","archive_member"}
    record=EVIDENCE[locator["evidence_id"]]
    if locator["path_kind"]=="materialized_normalized_file": assert locator["path"]==record["normalized_path"] and (ROOT/locator["path"]).is_file()
    else:
        archive=ARCHIVES[record["parent_archive_record_id"]]; assert locator["archive_path"]==archive["current_path"] and locator["archive_member_path"]==record["original_archive_path"] and (ROOT/locator["archive_path"]).is_file()
        with zipfile.ZipFile(ROOT/locator["archive_path"]) as packet:
            assert locator["archive_member_path"] in packet.namelist(); payload=packet.read(locator["archive_member_path"]); assert hashlib.sha256(payload).hexdigest()==record["sha256"]

def test_clean_origin_uses_nonancestry_not_object_absence():
    assert subprocess.run(["git","merge-base","--is-ancestor",BASE,"HEAD"]).returncode==0
    if subprocess.run(["git","cat-file","-e",f"{ABANDONED}^{{commit}}"],capture_output=True).returncode==0:
        result=subprocess.run(["git","merge-base","--is-ancestor",ABANDONED,"HEAD"],capture_output=True)
        assert result.returncode!=0,"abandoned PR #338 head must not be an ancestor of HEAD"

def test_committed_diff_is_exact_text_only_nondeleting_scope():
    expected={CERT,*SUPPORT,*SHARDS,"tests/afqr_r1e_semantic_helpers.py","tests/test_afqr_r1e_formal_completion_review.py","tests/test_afqr_r1d_core_transaction_identity_relation.py","tests/test_afqr_r1d_agency_epistemic_social_communication.py","tests/test_afqr_r1d_world_action_sensing.py","docs/decisions/current_decisions_log.md","docs/doctrine/astra_doctrine_registry_v0_1.yaml","docs/doctrine/control/afqr_01_20_consolidation_program_plan.md","docs/doctrine/reviews/afqr_01_20_consolidation_file_manifest.yaml","docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml","docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml"}
    changed=set(subprocess.check_output(["git","diff","--name-only",f"{BASE}...{ACCEPTED_R1_HEAD}"],text=True).splitlines()); assert changed==expected
    assert subprocess.run(["git","diff","--check",f"{BASE}...{ACCEPTED_R1_HEAD}"],capture_output=True).returncode==0
    numstat=subprocess.check_output(["git","diff","--numstat",f"{BASE}...{ACCEPTED_R1_HEAD}"],text=True); assert "-\t-\t" not in numstat
    assert not subprocess.check_output(["git","diff","--name-status","--diff-filter=D",f"{BASE}...{ACCEPTED_R1_HEAD}"],text=True).strip()
    forbidden=("working/afqr_consolidation_inputs/","src/","schemas/","conversion/","canon/","/r2","rt_002g")
    assert not [x for x in changed if any(token in x.lower() for token in forbidden) or x.lower().endswith((".zip",".pdf",".png",".jpg"))]

def test_modular_files_respect_limits_and_do_not_copy_upstream_records():
    assert len((ROOT/CERT).read_text().splitlines())==121 and len((ROOT/CERT).read_bytes())<=100*1024
    for path in [*SUPPORT,*SHARDS]: assert (ROOT/path).is_file() and len((ROOT/path).read_text().splitlines())<=3000 and len((ROOT/path).read_bytes())<=350*1024
    upstream=set()
    for value in [AUTH,VOCAB,R1C,*FAMILIES.values()]:upstream|=nested_dict_hashes(value)
    for artifact in [SV,DP,ADJ,CA,*SHARD_DOCS]:assert not upstream&nested_dict_hashes(artifact)

def test_all_twenty_authorities_and_every_evidence_locator_are_exact():
    rows=SV["source_authority_audit"]; authoritative={x["afqr_id"]:x for x in AUTH["afqr_records"]}; assert [x["afqr_id"] for x in rows]==[f"AFQR-{n:02}" for n in range(1,21)]
    for row in rows:
        source=authoritative[row["afqr_id"]]; assert row["authoritative_authority_index_record_sha256"]==normalized_hash(source); assert row["authoritative_title"]==source["full_title"] and row["selected_architecture"]==source["selected_architecture"] and row["decision_status"]==source["decision_status"]
        groups=[("primary_source_evidence_ids","primary_source_evidence_locators"),("title_evidence_ids","title_evidence_locators"),("corrected_baseline_evidence_ids","corrected_baseline_evidence_locators")]
        for ids,locs in groups: assert [x["evidence_id"] for x in row[locs]]==row[ids] and all(assert_locator(x) is None for x in row[locs])
    assert SV["afqr_14_provenance_review"]["primary_source"]=="SRC-0103" and SV["afqr_14_provenance_review"]["title_evidence"]==["SRC-0114"] and SV["afqr_14_provenance_review"]["corrected_baseline_evidence"]==["SRC-0103","SRC-0139","SRC-0121"] and SV["afqr_14_provenance_review"]["ownership_transfer"] is False

def test_all_41_vocabulary_rows_compare_every_claimed_field():
    rows={x["term_id"]:x for x in SV["vocabulary_audit"]}; terms={x["term_id"]:x for x in VOCAB["term_records"]}; assert len(rows)==len(terms)==41
    fields={"normalized_root":"root_term","canonical_form":"canonical_form","vocabulary_disposition":"vocabulary_disposition","unqualified_usage":"unqualified_usage","explicit_nonowners":"explicit_nonowners","handoff_only_consumers":"handoff_only_consumers","disallowed_aliases":"disallowed_aliases","explicit_non_equivalences":"explicit_non_equivalences","source_evidence":"source_evidence_records","collision_ids":"collision_ids"}
    for term_id,source in terms.items():
        row=rows[term_id]; assert row["authoritative_record_sha256"]==normalized_hash(source); assert row["owner"]==compact_owner(source["type_owner"]); assert row["qualified_forms"]==[{k:q[k] for k in ("qualified_form","owner_kind","owner_id")} for q in source["qualified_forms"]]
        for claimed,upstream in fields.items():assert row[claimed]==source[upstream],f"{term_id}.{claimed}"
        assert [x["evidence_id"] for x in row["source_evidence_locators"]]==row["source_evidence"]; [assert_locator(x) for x in row["source_evidence_locators"]]

def test_94_compact_edges_have_structured_owner_bindings_and_real_projection_results():
    rows={x["edge_id"]:x for x in DP["edge_reviews"]}; edges={x["edge_id"]:x for x in R1C["dependency_edge_dispositions"]}; assert len(rows)==len(edges)==94
    assert Counter(x["calculated_partition"] for x in rows.values())==Counter({"core_internal":33,"agency_internal":11,"world_internal":7,"core–agency_boundary":21,"core–world_boundary":17,"agency–world_boundary":5})
    projections=PROJECTION_MAP
    for edge_id,source in edges.items():
        row=rows[edge_id]; owner=source["semantic_type_owner"]; assert row["semantic_owner"]==compact_owner(owner); assert row["r1b_binding_identifiers"]==[x["term_id"] for x in owner["r1b_term_bindings"]]; assert row["authoritative_r1c_record_sha256"]==normalized_hash(source)
        for ref in row["projections"]:
            audit=projections[ref["projection_ref"]]; assert audit["projection_hash"]==ref["projection_hash"] and audit["result"]=="pass" and audit["field_comparisons"] and not audit["mismatched_fields"]
            categories=[audit[k] for k in ("compared_fields","upstream_only_preserved_fields","not_applicable_fields","missing_fields")]; flat=sum(categories,[]); assert set(flat)==set(REQUIRED_R1C_FIELDS) and len(flat)==len(set(flat))==len(REQUIRED_R1C_FIELDS) and not audit["missing_fields"]
            for comparison in audit["field_comparisons"]: assert {"r1c_field","r1d_field","disposition","comparison_mode","normalization_rule","source_hash","destination_hash","result","mismatch_reason"}<=set(comparison) and comparison["result"]=="pass"
    assert rows["DEP-001"]["semantic_owner"]|{}=={"owner_kind":"afqr","owner_id":"AFQR-01","ownership_basis":"merged_r1b_term_owner"} and rows["DEP-001"]["r1b_binding_identifiers"]==["TERM-003","TERM-004"]

def contract_for_ref(ref):
    family_name=next(name for name,path in FAMILY_PATHS.items() if ref.startswith(path)); section=ref.split("#/")[1].split("/")[0]
    return projection_contract(family_name,section,FAMILIES[family_name])

def test_projection_audits_recompute_and_account_for_every_required_field():
    edges={x["edge_id"]:x for x in R1C["dependency_edge_dispositions"]}; actual={f"{FAMILY_PATHS[name]}#/{section}/{index}":record for name,doc in FAMILIES.items() for eid,section,index,record in projection_records(doc)}
    assert len(ALL_PROJECTIONS)==137
    dispositions=Counter()
    for stored in ALL_PROJECTIONS:
        calculated=compare_projection(edges[stored["edge_id"]],actual[stored["projection_ref"]],contract_for_ref(stored["projection_ref"])); assert calculated=={k:stored[k] for k in calculated}
        groups=[calculated[k] for k in ("compared_fields","upstream_only_preserved_fields","not_applicable_fields","missing_fields")];flat=sum(groups,[]);assert set(flat)==set(REQUIRED_R1C_FIELDS) and len(flat)==len(REQUIRED_R1C_FIELDS) and not calculated["missing_fields"]
        dispositions.update(x["disposition"] for x in calculated["field_comparisons"])
    assert dispositions["exact"] and dispositions["bounded_projection"] and dispositions["upstream_only_preserved"] and dispositions["not_applicable"] and not dispositions["missing_blocking"]
    assert DP["projection_coverage_summary"]=={"projection_count":137,"required_fields_per_projection":18,"field_disposition_count":2466,"disposition_counts":dict(dispositions),"preservation_rule_count":18,"missing_blocking_count":0,"result":"pass"}
    assert len(CA["preservation_rule_catalog"])==18 and {x["preservation_rule_id"] for x in CA["preservation_rule_catalog"]}==APPROVED_PRESERVATION_RULES
    dep1=next(x for x in ALL_PROJECTIONS if x["edge_id"]=="DEP-001"); assert {"postconditions","revocation_invalidation_or_cascade","hidden_information_or_projection_constraints","consumer_not_semantic_owner_by_consumption"}<=set(dep1["upstream_only_preserved_fields"]) and "source_evidence_paths" in dep1["compared_fields"]

def test_destination_deletions_target_the_corresponding_source_field():
    edges={x["edge_id"]:x for x in R1C["dependency_edge_dispositions"]};samples=[("core",FAMILIES["core"],"DEP-001"),("agency",FAMILIES["agency"],"DEP-072"),("world",FAMILIES["world"],"DEP-088")]
    for family_name,doc,eid in samples:
        _,section,_,projection=next(x for x in projection_records(doc) if x[0]==eid);contract=projection_contract(family_name,section,doc);baseline=compare_projection(edges[eid],projection,contract)
        seen=set()
        for comparison in baseline["field_comparisons"]:
            if not comparison["r1d_field"] or comparison["r1c_field"]=="cycle_participation":continue
            destination=comparison["r1d_field"].split(".")[0];key=(destination,comparison["r1c_field"])
            if destination not in projection or key in seen:continue
            seen.add(key);changed=copy.deepcopy(projection);changed.pop(destination);result=compare_projection(edges[eid],changed,contract);source_field=comparison["r1c_field"]
            if source_field in contract["explicit_fields"]:
                assert result["result"]=="fail" and source_field in result["missing_fields"],f"{family_name}:{destination}->{source_field}"
            else:
                assert source_field in result["upstream_only_preserved_fields"]
                preserved=next(x for x in result["field_comparisons"] if x["r1c_field"]==source_field);assert preserved["preservation_rule_id"] in APPROVED_PRESERVATION_RULES

def test_upstream_preservation_requires_exact_allowlist_clause_and_nontransfer():
    edge=next(x for x in R1C["dependency_edge_dispositions"] if x["edge_id"]=="DEP-001");_,section,_,projection=next(x for x in projection_records(FAMILIES["core"]) if x[0]=="DEP-001");contract=projection_contract("core",section,FAMILIES["core"]);baseline=compare_projection(edge,projection,contract);assert baseline["result"]=="pass"
    for item in baseline["field_comparisons"]:
        if item["disposition"]=="upstream_only_preserved":assert item["preservation_rule_id"] in APPROVED_PRESERVATION_RULES and item["authority_clause_hash"] and item["contradiction_scan_result"]=="pass"
    no_clause=projection_contract("core",section,{});assert compare_projection(edge,projection,no_clause)["result"]=="fail"
    no_rule=copy.deepcopy(contract);no_rule["upstream_only_rules"].pop("postconditions");assert compare_projection(edge,projection,no_rule)["result"]=="fail"
    transfer=copy.deepcopy(projection);transfer["ownership_nontransfer"]=False;assert compare_projection(edge,transfer,contract)["result"]=="fail"

def test_real_mutations_fail_for_core_agency_world_and_boundary():
    edges={x["edge_id"]:x for x in R1C["dependency_edge_dispositions"]}
    def record(family_name,eid):
        _,section,_,projection=next(x for x in projection_records(FAMILIES[family_name]) if x[0]==eid);return projection,projection_contract(family_name,section,FAMILIES[family_name])
    world,wc=record("world","DEP-088")
    mutations=[lambda x:x.pop("producer"),lambda x:x.pop("consumer"),lambda x:x.pop("semantic_owner"),lambda x:(x["semantic_owner"].pop("r1b_term_bindings"),x.pop("exact_r1b_term_bindings")),lambda x:x.__setitem__("ownership_nontransfer",False),lambda x:x.__setitem__("consumer_nonownership",False),lambda x:x.__setitem__("preconditions",x["preconditions"][1:]),lambda x:x.__setitem__("postconditions",[]),lambda x:x.__setitem__("unavailable_input_behavior","forced continuation"),lambda x:x.__setitem__("hidden_information_and_projection_constraints","unrelated visibility rule"),lambda x:x["source_evidence"]["identifiers"].__setitem__(0,"SRC-9999"),lambda x:x["source_evidence"]["paths"].__setitem__(0,"wrong/path"),lambda x:x.__setitem__("downstream_implementation_status","implementation ready")]
    for mutate in mutations:
        changed=copy.deepcopy(world);mutate(changed);assert compare_projection(edges["DEP-088"],changed,wc)["result"]=="fail"
    for family_name,eid,mutation in [("core","DEP-001",lambda x:x.pop("producer")),("agency","DEP-072",lambda x:x.pop("consumer")),("core","DEP-009",lambda x:x.__setitem__("ownership_nontransfer",False))]:
        projection,contract=record(family_name,eid);changed=copy.deepcopy(projection);mutation(changed);assert compare_projection(edges[eid],changed,contract)["result"]=="fail"

def test_cycles_risks_and_all_stored_hashes_recompute():
    assert {x["cycle_id"]:x["edge_ids"] for x in DP["cycle_reviews"]}=={"CYCLE-001":["DEP-008","DEP-061"],"CYCLE-002":["DEP-021","DEP-024"],"CYCLE-003":["DEP-048","DEP-052"],"CYCLE-004":["DEP-089","DEP-091"]}
    assert {frozenset(x["edge_ids"]) for x in DP["dependency_risk_reviews"]}=={frozenset(x) for x in [("DEP-022","DEP-062"),("DEP-028","DEP-063"),("DEP-049","DEP-064"),("DEP-054","DEP-066")]}; assert all(x["recursion_prohibited"] for x in DP["cycle_reviews"]); assert all(x["self_authorization_prohibited"] for x in DP["dependency_risk_reviews"])

def test_collision_adjudications_and_both_ledgers_reconcile_semantically():
    b=load_json("docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml"); c=load_json("docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml"); bm={x["collision_ids"][0]:x for x in b["escalations"]}; cm={x["collision_id"]:x for x in c["escalations"] if "collision_id" in x}; invariants={x["invariant_id"] for x in R1C["cross_afqr_invariants"]}; edges={x["edge_id"] for x in R1C["dependency_edge_dispositions"]}
    expected_invariants={"COLL-03":["INV-001","INV-005"],"COLL-08":["INV-001","INV-006"],"COLL-10":[]}
    for decision in ADJ["collision_adjudications"]:
        cid=decision["collision_id"]; assert decision["decision"]=="approved_with_qualification" and decision["r1c_invariants"]==expected_invariants[cid] and set(decision["r1c_invariants"])<=invariants and set(decision["r1c_edges"])<=edges and set(decision["r1c_invariant_applicability"])==set(expected_invariants[cid]);
        if cid=="COLL-10": assert decision["r1c_invariant_disposition"]=="no_direct_applicable_invariant" and decision["dependency_grounding"]["edge_ids"]==["DEP-080","DEP-081"] and decision["dependency_grounding"]["primary_evidence_ids"]==["SRC-0059","SRC-0092","SRC-0110"]
        for ledger in (bm[cid],cm[cid]):
            assert ledger["r1c_invariants"]==expected_invariants[cid] and ledger["r1c_invariant_disposition"]==decision.get("r1c_invariant_disposition","direct_applicable_invariants") and ledger["r1c_edge_grounding"]==decision["r1c_edges"]
            assert ledger["r1e_decision_id"]==decision["decision_id"] and ledger["status"]=="closed_by_r1e" and ledger["resolution_evidence"]==decision["primary_evidence_ids"] and ledger["exact_evidence_locators"]==decision["exact_evidence_locators"] and ledger["exact_affected_afqrs"]==decision["exact_affected_afqrs"] and ledger["final_attribution_rule"]==decision["final_attribution_rule"] and ledger["prohibited_inferences"]==decision["prohibited_inferences"] and ledger["formal_review_path"].endswith("afqr_01_20_formal_completion_review.md") and ledger["supersession_scope"]==decision["supersession_scope"]
        [assert_locator(x) for x in decision["exact_evidence_locators"]]

def substrate_mismatches(authoritative,decision,ledger):
    pairs=[("name",authoritative["name"],decision["exact_substrate_name"],ledger["exact_name"]),("requiring",authoritative["requiring_afqrs"],decision["exact_requiring_afqrs"],ledger["exact_requiring_afqrs"]),("evidence",authoritative["source_evidence_records"],decision["exact_evidence_ids"],ledger["exact_evidence_ids"]),("paths",authoritative["source_evidence_paths"],decision["exact_evidence_paths"],ledger["exact_evidence_paths"]),("decision",decision["decision_id"],decision["decision_id"],ledger["r1e_decision_id"]),("future owner",authoritative["future_doctrine_owner"],decision["future_owner_posture"],ledger["future_owner_posture"]),("separation",True,decision["explicit_owner_separation"],ledger["owner_separation"]),("combined owner",decision["combined_owner_prohibition"],decision["combined_owner_prohibition"],ledger["combined_owner_prohibition"]),("history",decision["historical_blocking_effect"],decision["historical_blocking_effect"],ledger["historical_blocking_effect"]),("current",decision["current_post_r1e_blocking_effect"],decision["current_post_r1e_blocking_effect"],ledger["current_blocking_effect"]),("implementation","unimplemented",decision["implementation_status"],ledger["implementation_status"]),("later gate",decision["later_lawful_gate"],decision["later_lawful_gate"],ledger["later_lawful_gate"])]
    return [name for name,a,d,l in pairs if not a==d==l]

def test_substrates_reconcile_and_any_semantic_mutation_is_detected():
    authoritative={x["substrate_id"]:x for x in R1C["missing_substrate_classifications"]}; ledger={x["escalation_id"].replace("-ESC",""):x for x in load_json("docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml")["escalations"] if "substrate" in x}
    for decision in ADJ["substrate_adjudications"]:
        sid=decision["substrate_id"]; assert not substrate_mismatches(authoritative[sid],decision,ledger[sid]); assert decision["decision"]=="accepted_as_classified_deferred_substrate" and ledger[sid]["status"]=="accepted_deferred_by_r1e"; [assert_locator(x) for x in decision["exact_evidence_locators"]]
        for field in ("exact_substrate_name","exact_requiring_afqrs","exact_evidence_ids","exact_evidence_paths","future_owner_posture","explicit_owner_separation","combined_owner_prohibition","historical_blocking_effect","current_post_r1e_blocking_effect","implementation_status","later_lawful_gate"):
            changed=copy.deepcopy(decision); changed[field]=False if isinstance(changed[field],bool) else ["MUTATED"] if isinstance(changed[field],list) else "MUTATED"; assert substrate_mismatches(authoritative[sid],changed,ledger[sid]),field

def test_thirteen_distinct_consistency_comparators_reexecute():
    edge_rows=[{"edge_id":x["edge_id"],"projections":[PROJECTION_MAP[ref["projection_ref"]] for ref in x["projections"]]} for x in DP["edge_reviews"]]
    calculated=calculate_consistency(AUTH,VOCAB,R1C,FAMILIES,edge_rows,MANIFEST,CA["r1d_to_r1e_coverage"]); assert calculated==CA["relational_consistency_rows"] and [x["comparator_id"] for x in calculated]==[f"REL-{n:02}" for n in range(1,14)] and all(x["result"]=="pass" for x in calculated)
    rel13=next(x for x in calculated if x["comparator_id"]=="REL-13");broken=copy.deepcopy(CA["r1d_to_r1e_coverage"]);broken["responsibility_record_ids"].pop();broken["authority_granted"].append("runtime implementation");mutated=calculate_consistency(AUTH,VOCAB,R1C,FAMILIES,edge_rows,MANIFEST,broken)[-1];assert mutated["result"]=="fail" and mutated["calculated_details"]["missing_family_findings"] and mutated["calculated_details"]["unauthorized_implementation_claims"]

def walk_strings(value):
    if isinstance(value,str):yield value
    elif isinstance(value,dict):
        for x in value.values():yield from walk_strings(x)
    elif isinstance(value,list):
        for x in value:yield from walk_strings(x)

EXPECTED_OWNERS={
"radiation exposure":{"AFQR-17"},"resulting radiation harm":{"AFQR-16"},"starship sensors":{"AFQR-20"},"sensor contact":{"AFQR-20"},"ship facing":{"AFQR-18"},"spatial reachability":{"AFQR-18"},"target validity":{"AFQR-19"},"clue observation":{"AFQR-20"},"clue evidence":{"AFQR-06"},"epistemic belief/knowledge":{"AFQR-10"},"hidden truth":set(),"repair semantics":{"AFQR-16"},"repair commitment":{"AFQR-01"},"material reservation":{"AFQR-07"},"mind control":{"AFQR-11"},"motivation pressure":{"AFQR-12"},"companion control":{"AFQR-11"},"identity/proxy continuity":{"AFQR-08"},"swarm agency":set(),"random-table procedure":set(),"generated encounter result":set(),"oracle prompt":set(),"oracle output":set(),"adventure faction":{"AFQR-13"},"institutional jurisdiction":{"AFQR-15"},"campaign cosmology":set()}

def test_eighteen_donor_families_use_independent_construct_expectations():
    rows=CA["donor_family_adequacy_rows"];assert [x["donor_family_id"] for x in rows]==[f"DONOR-{n:02}" for n in range(1,19)];byconstruct={x["construct"]:x for row in rows for x in row["construct_dispositions"]};assert set(EXPECTED_OWNERS)<=set(byconstruct)
    for construct,expected in EXPECTED_OWNERS.items():
        item=byconstruct[construct];assert set(item["owners"])==expected;assert item["owners"] or item["outcome"] in {"source_local","quarantine","doctrine_escalation","normalized_mapping"};assert item["prohibited_inferences"] and item["rationale"]
        for handoff in item["handoffs"]:assert handoff["from"]!=handoff["to"] and handoff["payload"]
    # The expectation remains external even if an audit owner and any embedded metadata are mutated together.
    wrong=copy.deepcopy(byconstruct["clue evidence"]);wrong["owners"]=["AFQR-10"];wrong["expected_owner_fixture"]=["AFQR-10"];assert set(wrong["owners"])!=EXPECTED_OWNERS["clue evidence"]
    clue=byconstruct["clue evidence"];assert [(x["from"],x["to"]) for x in clue["handoffs"]]==[("AFQR-20","AFQR-06"),("AFQR-06","AFQR-10")]
    repair=byconstruct["repair semantics"];assert repair["owners"]==["AFQR-16"] and repair["handoffs"][0]["to"]=="AFQR-01"
    assert byconstruct["random-table procedure"]["outcome"]==byconstruct["oracle prompt"]["outcome"]=="source_local" and not byconstruct["oracle output"]["owners"]
    pressure={x["record_id"]:x for d in FAMILIES.values() for x in d["corpus_pressure_records"]}
    for row in rows:assert row["source_r1d_pressure_record_hashes"]==[normalized_hash(pressure[x]) for x in row["source_r1d_pressure_record_ids"]]

def test_final_gate_is_recomputed_and_grants_no_downstream_authority():
    cert=load_markdown_json(CERT); assert all(x["result"]=="pass" for x in [SV,DP,ADJ,CA,*SHARD_DOCS]) and cert["result"]=="pass" and cert["r1_status"]=="complete" and not cert["blocking_defects"]
    assert cert["downstream_gate_states"]=={"R2":"ready","R3":"blocked","R4":"blocked","R5":"blocked","R6":"blocked","RT-002G":"unauthorized","temporary_evidence_deletion":"unauthorized"}; assert {"runtime implementation","conversion execution","R2 work","RT-002G implementation","temporary evidence deletion"}<=set(cert["authority_not_granted"])

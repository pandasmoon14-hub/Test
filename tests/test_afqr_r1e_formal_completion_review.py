from __future__ import annotations
import copy,json,subprocess,sys
from collections import Counter
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).parent))
from afqr_r1e_semantic_helpers import *
BASE="017984a1598b9c60324c62e54d80372c364654ae"; ABANDONED="50c0320acd1a9a075cba18e1309dd3d15ac5c44d"
CERT="docs/doctrine/reviews/afqr_01_20_formal_completion_review.md"
SUPPORT=["docs/doctrine/reviews/afqr_r1e_source_and_vocabulary_audit.yaml","docs/doctrine/reviews/afqr_r1e_dependency_and_parity_audit.yaml","docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml","docs/doctrine/reviews/afqr_r1e_consistency_and_corpus_adequacy.yaml"]
SHARDS=["docs/doctrine/reviews/afqr_r1e_core_projection_field_comparisons.yaml","docs/doctrine/reviews/afqr_r1e_agency_projection_field_comparisons.yaml","docs/doctrine/reviews/afqr_r1e_world_projection_field_comparisons.yaml"]
AUTH=load_json("docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml"); MANIFEST=load_json("working/afqr_consolidation_inputs/manifest.yaml"); VOCAB=load_json("docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml"); R1C=load_json("docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml")
SV,DP,ADJ,CA=[load_json(x) for x in SUPPORT]; SHARD_DOCS=[load_json(x) for x in SHARDS]
FAMILY_PATHS={"core":"docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md","agency":"docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md","world":"docs/doctrine/consolidation/afqr_world_action_sensing.md"}; FAMILIES={k:load_markdown_json(v) for k,v in FAMILY_PATHS.items()}
EVIDENCE={x["source_record_id"]:x for x in MANIFEST["contained_file_records"]}; ARCHIVES={x["archive_record_id"]:x for x in MANIFEST["archive_records"]}

def assert_locator(locator):
    assert locator and locator["evidence_id"] in EVIDENCE and locator.get("path_kind") in {"materialized_normalized_file","archive_member"}
    record=EVIDENCE[locator["evidence_id"]]
    if locator["path_kind"]=="materialized_normalized_file": assert locator["path"]==record["normalized_path"] and (ROOT/locator["path"]).is_file()
    else:
        archive=ARCHIVES[record["parent_archive_record_id"]]; assert locator["archive_path"]==archive["current_path"] and locator["archive_member_path"]==record["original_archive_path"] and (ROOT/locator["archive_path"]).is_file()

def test_clean_origin_uses_nonancestry_not_object_absence():
    assert subprocess.run(["git","merge-base","--is-ancestor",BASE,"HEAD"]).returncode==0
    if subprocess.run(["git","cat-file","-e",f"{ABANDONED}^{{commit}}"],capture_output=True).returncode==0:
        result=subprocess.run(["git","merge-base","--is-ancestor",ABANDONED,"HEAD"],capture_output=True)
        assert result.returncode!=0,"abandoned PR #338 head must not be an ancestor of HEAD"

def test_committed_diff_is_exact_text_only_nondeleting_scope():
    expected={CERT,*SUPPORT,*SHARDS,"tests/afqr_r1e_semantic_helpers.py","tests/test_afqr_r1e_formal_completion_review.py","tests/test_afqr_r1d_core_transaction_identity_relation.py","tests/test_afqr_r1d_agency_epistemic_social_communication.py","tests/test_afqr_r1d_world_action_sensing.py","docs/decisions/current_decisions_log.md","docs/doctrine/astra_doctrine_registry_v0_1.yaml","docs/doctrine/control/afqr_01_20_consolidation_program_plan.md","docs/doctrine/reviews/afqr_01_20_consolidation_file_manifest.yaml","docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml","docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml"}
    changed=set(subprocess.check_output(["git","diff","--name-only",BASE],text=True).splitlines())|{x[3:] for x in subprocess.check_output(["git","status","--porcelain"],text=True).splitlines() if x.startswith("?? ")}; assert changed==expected
    assert subprocess.run(["git","diff","--check",f"{BASE}...HEAD"],capture_output=True).returncode==0
    numstat=subprocess.check_output(["git","diff","--numstat",BASE],text=True); assert "-\t-\t" not in numstat
    assert not subprocess.check_output(["git","diff","--name-status","--diff-filter=D",BASE],text=True).strip()
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
    projections={x["projection_ref"]:x for shard in SHARD_DOCS for x in shard["projection_comparisons"]}
    for edge_id,source in edges.items():
        row=rows[edge_id]; owner=source["semantic_type_owner"]; assert row["semantic_owner"]==compact_owner(owner); assert row["r1b_binding_identifiers"]==[x["term_id"] for x in owner["r1b_term_bindings"]]; assert row["authoritative_r1c_record_sha256"]==normalized_hash(source)
        for ref in row["projections"]:
            audit=projections[ref["projection_ref"]]; assert audit["projection_hash"]==ref["projection_hash"] and audit["result"]=="pass" and audit["field_comparisons"] and not audit["mismatched_fields"]
            for comparison in audit["field_comparisons"]: assert set(comparison)=={"r1c_field","r1d_field","comparison_mode","normalization_rule","source_hash","destination_hash","result","mismatch_reason"} and comparison["result"]=="pass"
    assert rows["DEP-001"]["semantic_owner"]|{}=={"owner_kind":"afqr","owner_id":"AFQR-01","ownership_basis":"merged_r1b_term_owner"} and rows["DEP-001"]["r1b_binding_identifiers"]==["TERM-003","TERM-004"]

def test_projection_audits_are_recomputed_through_same_pipeline():
    edges={x["edge_id"]:x for x in R1C["dependency_edge_dispositions"]}
    actual={f"{FAMILY_PATHS[name]}#/{section}/{index}":record for name,doc in FAMILIES.items() for eid,section,index,record in projection_records(doc)}
    for shard in SHARD_DOCS:
        for stored in shard["projection_comparisons"]:
            calculated=compare_projection(edges[stored["edge_id"]],actual[stored["projection_ref"]]); assert calculated["result"]==stored["result"] and calculated["mismatched_fields"]==stored["mismatched_fields"]
            assert [(x["r1c_field"],x["r1d_field"],x["comparison_mode"],x["source_hash"],x["destination_hash"],x["result"]) for x in calculated["field_comparisons"]]==[(x["r1c_field"],x["r1d_field"],x["comparison_mode"],x["source_hash"],x["destination_hash"],x["result"]) for x in stored["field_comparisons"]]

def test_real_projection_mutations_fail_the_integrated_pipeline():
    edges={x["edge_id"]:x for x in R1C["dependency_edge_dispositions"]}; edge=edges["DEP-088"]
    projection=next(x[3] for x in projection_records(FAMILIES["world"]) if x[0]=="DEP-088")
    mutations=[("producer",lambda x:x.__setitem__("producer","AFQR-01")),("semantic owner",lambda x:x["semantic_owner"].__setitem__("owner_id","AFQR-01")),("R1B binding",lambda x:x.__setitem__("exact_r1b_term_bindings",[{"term_id":"TERM-999"}])),("nontransfer",lambda x:x.__setitem__("ownership_nontransfer",False)),("consumer use",lambda x:x.__setitem__("permitted_consumer_use","consumer becomes owner and receives unbounded use")),("unavailable",lambda x:x.__setitem__("unavailable_input_behavior","continue regardless and accept anyway")),("evidence",lambda x:x.__setitem__("source_evidence",["SRC-9999"])),("downstream",lambda x:x.__setitem__("downstream_implementation_status","implementation ready"))]
    for label,mutate in mutations:
        changed=copy.deepcopy(projection); mutate(changed); assert compare_projection(edge,changed)["result"]=="fail",label

def test_cycles_risks_and_all_stored_hashes_recompute():
    assert {x["cycle_id"]:x["edge_ids"] for x in DP["cycle_reviews"]}=={"CYCLE-001":["DEP-008","DEP-061"],"CYCLE-002":["DEP-021","DEP-024"],"CYCLE-003":["DEP-048","DEP-052"],"CYCLE-004":["DEP-089","DEP-091"]}
    assert {frozenset(x["edge_ids"]) for x in DP["dependency_risk_reviews"]}=={frozenset(x) for x in [("DEP-022","DEP-062"),("DEP-028","DEP-063"),("DEP-049","DEP-064"),("DEP-054","DEP-066")]}; assert all(x["recursion_prohibited"] for x in DP["cycle_reviews"]); assert all(x["self_authorization_prohibited"] for x in DP["dependency_risk_reviews"])

def test_collision_adjudications_and_both_ledgers_reconcile_semantically():
    b=load_json("docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml"); c=load_json("docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml"); bm={x["collision_ids"][0]:x for x in b["escalations"]}; cm={x["collision_id"]:x for x in c["escalations"] if "collision_id" in x}; invariants={x["invariant_id"] for x in R1C["cross_afqr_invariants"]}; edges={x["edge_id"] for x in R1C["dependency_edge_dispositions"]}
    for decision in ADJ["collision_adjudications"]:
        cid=decision["collision_id"]; assert decision["decision"]=="approved_with_qualification" and decision["r1c_invariants"] and set(decision["r1c_invariants"])<=invariants and set(decision["r1c_edges"])<=edges
        for ledger in (bm[cid],cm[cid]):
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
    edge_rows=[{"edge_id":x["edge_id"],"projections":[next(p for shard in SHARD_DOCS for p in shard["projection_comparisons"] if p["projection_ref"]==ref["projection_ref"]) for ref in x["projections"]]} for x in DP["edge_reviews"]]
    calculated=calculate_consistency(AUTH,VOCAB,R1C,FAMILIES,edge_rows,MANIFEST); assert calculated==CA["relational_consistency_rows"] and [x["comparator_id"] for x in calculated]==[f"REL-{n:02}" for n in range(1,14)] and len({tuple(x["comparison_rules"]) for x in calculated})==13 and all(x["result"]=="pass" for x in calculated)

def walk_strings(value):
    if isinstance(value,str):yield value
    elif isinstance(value,dict):
        for x in value.values():yield from walk_strings(x)
    elif isinstance(value,list):
        for x in value:yield from walk_strings(x)

def test_eighteen_donor_families_have_construct_specific_owner_disciplined_routes():
    rows=CA["donor_family_adequacy_rows"]; assert [x["donor_family_id"] for x in rows]==[f"DONOR-{n:02}" for n in range(1,19)]
    payloads=[]
    for row in rows:
        dispositions=row["construct_dispositions"]; assert {x["construct"] for x in dispositions}==set(row["representative_construct_pressures"])
        for item in dispositions:
            expected=row["expected_owner_fixture"][item["construct"]]; forbidden=row["forbidden_owner_fixture"][item["construct"]]; assert set(item["owners"])<=set(expected) and not set(item["owners"])&set(forbidden)
            assert item["owners"] or item["outcome"] in {"source_local","quarantine","doctrine_escalation"}; assert item["rationale"] and item["prohibited_inferences"]
            for handoff in item["handoffs"]: assert handoff["from"]!=handoff["to"] and handoff["payload"]
            payloads.append(json.dumps(item,sort_keys=True))
        pressure={x["record_id"]:x for d in FAMILIES.values() for x in d["corpus_pressure_records"]}; assert row["source_r1d_pressure_record_hashes"]==[normalized_hash(pressure[x]) for x in row["source_r1d_pressure_record_ids"]]
    assert max(Counter(payloads).values())<3
    blob=" ".join(walk_strings(rows)).lower(); assert "rhbf becomes" not in blob and all(f"{x} does not become astra doctrine" in blob or x not in blob for x in ("grid","anatomy","cosmology"))
    byconstruct={x["construct"]:x for row in rows for x in row["construct_dispositions"]}; assert byconstruct["radiation exposure"]["owners"]==["AFQR-17"] and byconstruct["radiation exposure"]["handoffs"][0]["to"]=="AFQR-16"; assert byconstruct["starship sensors"]["owners"]==["AFQR-20"]; assert byconstruct["ship facing rule"]["owners"]==["AFQR-18"]

def test_final_gate_is_recomputed_and_grants_no_downstream_authority():
    cert=load_markdown_json(CERT); assert all(x["result"]=="pass" for x in [SV,DP,ADJ,CA,*SHARD_DOCS]) and cert["result"]=="pass" and cert["r1_status"]=="complete" and not cert["blocking_defects"]
    assert cert["downstream_gate_states"]=={"R2":"ready","R3":"blocked","R4":"blocked","R5":"blocked","R6":"blocked","RT-002G":"unauthorized","temporary_evidence_deletion":"unauthorized"}; assert {"runtime implementation","conversion execution","R2 work","RT-002G implementation","temporary evidence deletion"}<=set(cert["authority_not_granted"])

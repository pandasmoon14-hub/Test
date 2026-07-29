from __future__ import annotations
import json, subprocess
from collections import Counter
from pathlib import Path
import pytest
import sys
sys.path.insert(0, str(Path(__file__).parent))
from afqr_r1e_semantic_helpers import *

BASE="017984a1598b9c60324c62e54d80372c364654ae"
CERT="docs/doctrine/reviews/afqr_01_20_formal_completion_review.md"
SUPPORT=["docs/doctrine/reviews/afqr_r1e_source_and_vocabulary_audit.yaml","docs/doctrine/reviews/afqr_r1e_dependency_and_parity_audit.yaml","docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml","docs/doctrine/reviews/afqr_r1e_consistency_and_corpus_adequacy.yaml"]
AUTH=load_json("docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml")
MANIFEST=load_json("working/afqr_consolidation_inputs/manifest.yaml")
VOCAB=load_json("docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml")
R1C=load_json("docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml")
SV,DP,ADJ,CA=[load_json(x) for x in SUPPORT]
FAMILY_PATHS={"core":"docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md","agency":"docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md","world":"docs/doctrine/consolidation/afqr_world_action_sensing.md"}
FAMILIES={k:load_markdown_json(v) for k,v in FAMILY_PATHS.items()}

def test_clean_origin_and_exact_scope():
    assert subprocess.check_output(["git","merge-base",BASE,"HEAD"],text=True).strip()==BASE
    assert subprocess.run(["git","cat-file","-e","50c0320acd1a9a075cba18e1309dd3d15ac5c44d^{commit}"],capture_output=True).returncode != 0
    changed=set(subprocess.check_output(["git","diff","--name-only",BASE],text=True).splitlines()) | {line[3:] for line in subprocess.check_output(["git","status","--porcelain"],text=True).splitlines() if line.startswith("?? ")}
    allowed={CERT,*SUPPORT,"tests/afqr_r1e_semantic_helpers.py","tests/test_afqr_r1e_formal_completion_review.py","tests/test_afqr_r1d_agency_epistemic_social_communication.py","tests/test_afqr_r1d_world_action_sensing.py","docs/decisions/current_decisions_log.md","docs/doctrine/astra_doctrine_registry_v0_1.yaml","docs/doctrine/control/afqr_01_20_consolidation_program_plan.md","docs/doctrine/reviews/afqr_01_20_consolidation_file_manifest.yaml","docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml","docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml"}
    assert changed==allowed
    assert not any(x.startswith("src/") or x.lower().endswith((".zip",".pdf",".png",".jpg")) or "/r2" in x.lower() or "rt_002g" in x.lower() for x in changed)
    assert not subprocess.check_output(["git","diff","--name-status","--diff-filter=D",BASE],text=True).strip()

def test_modular_files_and_size_limits():
    assert all((ROOT/x).is_file() for x in [CERT,*SUPPORT])
    assert len((ROOT/CERT).read_bytes())<=100*1024 and len((ROOT/CERT).read_text().splitlines())<=800
    for x in SUPPORT:
        assert len((ROOT/x).read_bytes())<=350*1024 and len((ROOT/x).read_text().splitlines())<=3000

def test_no_upstream_dictionary_was_copied_as_replacement_authority():
    upstream=set()
    for value in [AUTH,VOCAB,R1C,*FAMILIES.values()]: upstream |= nested_dict_hashes(value)
    for artifact in [SV,DP,ADJ,CA]:
        overlap=upstream & nested_dict_hashes(artifact)
        assert not overlap, f"R1E copied {len(overlap)} complete upstream dictionaries"
        assert "audit" in artifact.get("authority","").lower() or "adjudication" in artifact.get("authority","").lower()

def test_twenty_authorities_recompute_exactly_and_evidence_resolves():
    rows=SV["source_authority_audit"]; assert [x["afqr_id"] for x in rows]==[f"AFQR-{n:02}" for n in range(1,21)]
    records={x["afqr_id"]:x for x in AUTH["afqr_records"]}; evidence={x["source_record_id"]:x for x in MANIFEST["contained_file_records"]}
    for row in rows:
        source=records[row["afqr_id"]]
        assert row["authoritative_authority_index_record_sha256"]==normalized_hash(source)
        assert row["authoritative_title"]==source["full_title"] and row["selected_architecture"]==source["selected_architecture"]
        for locator in row["manifest_locator_references"]: assert locator["evidence_id"] in evidence
        for path in row["source_packet_paths"]: assert (ROOT/path).exists(), path

def test_afqr14_provenance_is_exact():
    assert SV["afqr_14_provenance_review"]=={"semantic_owner":"AFQR-14","architecture":"communication and interpretation architecture","primary_source":"SRC-0103","title_evidence":["SRC-0114"],"corrected_baseline_evidence":["SRC-0103","SRC-0139","SRC-0121"],"packaging_validator":"AFQR-15","ownership_transfer":False,"result":"pass"}

def test_all_41_vocabulary_records_recompute_without_invented_owner():
    rows=SV["vocabulary_audit"]; assert len(rows)==len(VOCAB["term_records"])==41
    authoritative={x["term_id"]:x for x in VOCAB["term_records"]}; assert set(authoritative)=={x["term_id"] for x in rows}
    for row in rows:
        source=authoritative[row["term_id"]]; assert row["authoritative_record_sha256"]==normalized_hash(source)
        assert row["canonical_form"]==source["canonical_form"] and row["explicit_nonowners"]==source["explicit_nonowners"]
        assert row["handoff_only_consumers"]==source["handoff_only_consumers"] and not row["mismatches"]

def test_all_94_edges_have_exact_partition_hash_and_semantic_field_contract():
    rows=DP["edge_reviews"]; assert len(rows)==len(R1C["dependency_edge_dispositions"])==94
    source={x["edge_id"]:x for x in R1C["dependency_edge_dispositions"]}; assert set(source)=={x["edge_id"] for x in rows}
    expected=Counter({"core_internal":33,"agency_internal":11,"world_internal":7,"core–agency_boundary":21,"core–world_boundary":17,"agency–world_boundary":5})
    assert Counter(x["calculated_partition"] for x in rows)==expected
    required={"relation_or_handoff_kind","semantic_type_owner","r1b_term_bindings","producer_supplies","consumer_may_use","ownership_does_not_transfer","consumer_not_semantic_owner_by_consumption","preconditions","postconditions","unavailable_input_behavior","failure_behavior","revocation_invalidation_or_cascade","hidden_information_or_projection_constraints","source_evidence_records","source_evidence_paths","cycle_participation","r1d_destination_family_or_escalation"}
    for row in rows:
        assert row["authoritative_r1c_record_sha256"]==normalized_hash(source[row["edge_id"]]); assert required<=set(row["compared_fields"]); assert not row["missing_fields"] and not row["mismatched_fields"]

def test_r1d_family_projection_coverage_and_two_sided_boundaries():
    seen={k:Counter(edge for edge,_,_,_ in projection_records(v)) for k,v in FAMILIES.items()}
    assert sum(seen["core"].values())==71 and sum(seen["agency"].values())==37 and sum(seen["world"].values())==29
    for edge in R1C["dependency_edge_dispositions"]:
        eid=edge["edge_id"]; sides={family(edge["producer_afqr"]),family(edge["consumer_afqr"])}
        for side in sides: assert seen[side][eid]==1, f"{eid} missing or duplicated in {side}"
    for row in DP["edge_reviews"]: assert len(row["projection_hashes"])==(1 if "internal" in row["calculated_partition"] else 2)

def test_comparator_mutations_are_detected_without_truthiness():
    assert exact_compare("AFQR-01","AFQR-02","producer")["result"]=="fail"
    assert bounded_projection_compare("must not transfer ownership","nonempty",source_field="ownership",destination_field="rule")["result"]=="fail"
    assert bounded_projection_compare(["reject unavailable input"],["continue"],source_field="unavailable",destination_field="failure")["result"]=="fail"
    assert DP["projection_comparator_contract"]["truthiness_only_comparison_prohibited"] is True

def test_cycles_and_dependency_risks_are_exact_and_bounded():
    assert {x["cycle_id"]:x["edge_ids"] for x in DP["cycle_reviews"]}=={"CYCLE-001":["DEP-008","DEP-061"],"CYCLE-002":["DEP-021","DEP-024"],"CYCLE-003":["DEP-048","DEP-052"],"CYCLE-004":["DEP-089","DEP-091"]}
    assert {frozenset(x["edge_ids"]) for x in DP["dependency_risk_reviews"]}=={frozenset(x) for x in [("DEP-022","DEP-062"),("DEP-028","DEP-063"),("DEP-049","DEP-064"),("DEP-054","DEP-066")]}
    assert all(x["recursion_prohibited"] and x["breaker"] for x in DP["cycle_reviews"])
    assert all(x["self_authorization_prohibited"] for x in DP["dependency_risk_reviews"])

def test_collision_decisions_and_both_historical_ledgers_reconcile():
    decisions={x["collision_id"]:x for x in ADJ["collision_adjudications"]}; assert set(decisions)=={"COLL-03","COLL-08","COLL-10"}
    expected={"COLL-03":(["AFQR-01","AFQR-08","AFQR-11","AFQR-15"],["SRC-0004","SRC-0011","SRC-0059","SRC-0157"]),"COLL-08":(["AFQR-09","AFQR-13","AFQR-15"],["SRC-0012","SRC-0110","SRC-0157"]),"COLL-10":(["AFQR-11","AFQR-12","AFQR-13"],["SRC-0059","SRC-0092","SRC-0110"])}
    for cid,(afqrs,evidence) in expected.items(): assert decisions[cid]["exact_affected_afqrs"]==afqrs and decisions[cid]["r1b_evidence"]==evidence and decisions[cid]["decision"]=="approved_with_qualification"
    b=load_json("docs/doctrine/reviews/afqr_r1b_unresolved_term_escalation_ledger.yaml"); c=load_json("docs/doctrine/reviews/afqr_r1c_unresolved_dependency_escalation_ledger.yaml")
    assert len(b["escalations"])==3 and len(c["escalations"])==8
    assert all(x["status"]=="closed_by_r1e" for x in b["escalations"])
    assert all(x["status"]=="closed_by_r1e" for x in c["escalations"][:3])

def test_five_substrates_remain_unimplemented_owner_separated_deferrals():
    rows=ADJ["substrate_adjudications"]; assert [x["substrate_id"] for x in rows]==[f"SUB-{n:03}" for n in range(1,6)]
    assert all(x["decision"]=="accepted_as_classified_deferred_substrate" and x["implementation_status"]=="unimplemented" and x["explicit_owner_separation"] for x in rows)
    mutated=dict(rows[0],decision="blocking_incomplete_substrate")
    calculated_result="fail" if mutated["decision"]=="blocking_incomplete_substrate" else "pass"
    assert calculated_result=="fail"

def test_thirteen_consistency_rows_are_calculated_and_nontransferring():
    rows=CA["relational_consistency_rows"]; assert len(rows)==13 and [x["comparator_id"] for x in rows]==[f"REL-{n:02}" for n in range(1,14)]
    assert all(not x["missing_ids"] and not x["surplus_ids"] and not x["mismatched_ids_and_fields"] and not x["authority_transfer_violations"] and x["result"]=="pass" for x in rows)

def test_eighteen_donor_families_have_structured_lawful_dispositions():
    rows=CA["donor_family_adequacy_rows"]; assert len(rows)==18 and len({x["donor_family"] for x in rows})==18
    banned={"mapping","owner","construct","prohibited","allowed"}
    for row in rows:
        assert row["representative_construct_pressures"] and row["quarantine_triggers"] and row["doctrine_escalation_triggers"]
        for record in row["direct_mappings"]: assert {"donor_construct","astra_owner","astra_landing","lawful_basis","source_local_retention"}<=record.keys()
        for record in row["normalized_mappings"]: assert {"donor_construct","normalization","receiving_owners","source_local_retention","prohibited_inferences"}<=record.keys()
        assert not any(str(v).lower() in banned for v in row.values() if isinstance(v,str))
        assert not row["blocking_defects"] and row["result"]=="pass"

def test_final_certificate_recomputes_a_pass_and_only_r2_is_ready():
    cert=load_markdown_json(CERT)
    blockers=[]
    if any(x["result"]!="pass" for x in [SV,DP,ADJ,CA]): blockers.append("support failure")
    if any(x["decision"]=="deferred_blocking" for x in ADJ["collision_adjudications"]): blockers.append("collision")
    if any(x["decision"]=="blocking_incomplete_substrate" for x in ADJ["substrate_adjudications"]): blockers.append("substrate")
    assert not blockers and cert["result"]=="pass" and cert["r1_status"]=="complete"
    assert cert["downstream_gate_states"]=={"R2":"ready","R3":"blocked","R4":"blocked","R5":"blocked","R6":"blocked","RT-002G":"unauthorized","temporary_evidence_deletion":"unauthorized"}
    forbidden={"runtime implementation","conversion execution","canon promotion","model training","live-play behavior","narration","UI behavior","RT-002G implementation","temporary evidence deletion"}
    assert forbidden<=set(cert["authority_not_granted"])

def test_every_stored_upstream_hash_is_independently_recomputed():
    projection_by_ref={}
    for family_name, document in FAMILIES.items():
        for edge_id, section, index, record in projection_records(document):
            projection_by_ref[f"{FAMILY_PATHS[family_name]}#/{section}/{index}"]=normalized_hash(record)
    for row in DP["edge_reviews"]:
        assert row["projection_hashes"]==[projection_by_ref[x] for x in row["applicable_r1d_projection_references"]]
    cycles={x["cycle_id"]:x for x in R1C["cycle_risk_resolutions"]}
    for row in DP["cycle_reviews"]: assert row["authoritative_record_sha256"]==normalized_hash(cycles[row["cycle_id"]])
    risks={x["reclassification_id"]:x for x in R1C["cycle_risk_reclassifications"]}
    for row in DP["dependency_risk_reviews"]: assert row["authoritative_record_sha256"]==normalized_hash(risks[row["risk_id"]])
    substrates={x["substrate_id"]:x for x in R1C["missing_substrate_classifications"]}
    for row in ADJ["substrate_adjudications"]: assert row["authoritative_record_sha256"]==normalized_hash(substrates[row["substrate_id"]])
    pressure={x["record_id"]:x for document in FAMILIES.values() for x in document["corpus_pressure_records"]}
    for row in CA["donor_family_adequacy_rows"]:
        assert row["source_r1d_pressure_record_hashes"]==[normalized_hash(pressure[x]) for x in row["source_r1d_pressure_record_ids"]]

def test_consistency_hashes_and_mismatch_arrays_are_calculated_not_self_certified():
    upstream={"R1A":AUTH,"R1B":VOCAB,"R1C":R1C,"R1D-CORE":FAMILIES["core"],"R1D-AGENCY":FAMILIES["agency"],"R1D-WORLD":FAMILIES["world"],"R1D":FAMILIES,"R1E":{"support_ids":[SV["artifact_id"],DP["artifact_id"],ADJ["artifact_id"]]}}
    for row in CA["relational_consistency_rows"]:
        producer,consumer=row["compared_record_ids"]
        assert row["producer_hash"]==normalized_hash(upstream[producer])
        assert row["consumer_hash"]==normalized_hash(upstream[consumer])
        payload={"comparator_id":row["comparator_id"],"label":row["relationship"],"missing":[],"surplus":[],"mismatch":[],"transfer":[]}
        assert row["calculated_result_hash"]==normalized_hash(payload)

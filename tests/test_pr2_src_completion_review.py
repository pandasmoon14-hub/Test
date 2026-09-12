from __future__ import annotations
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"docs/doctrine/reviews/pr2_src_source_research_completion_review.yaml"; M=ROOT/"docs/doctrine/control/post_r2a_transition_manifest.yaml"; P=ROOT/"docs/doctrine/control/post_r2a_transition_program.md"; D=ROOT/"docs/decisions/current_decisions_log.md"
BASE="21b4ba706bb3f68aeb51dc4195fe1aa60014a439"; AUTH="owner_directive_2026-09-11_pr2_src_d_activation"; EFFECT="independent_source_research_completion_review_only"
PR=385; HEAD="7fd2f1c202abd7107dc2918e168d7885fb9452ce"; MERGE="376214e1b715de34160dfb03d328547f510b6586"; TREE="bcf9dd80d9a39594e60a62218bff3ee64aa85abb"; CLOSURE_AUTH="owner_directive_2026-09-11_pr2_src_post_merge_closure"; CLOSURE_MERGE="c14da427bf5c5c21c7ef1655e83aea3519587cc6"
READY={"PR2-ORG","PR2-FICT","PR2-SIMEX"}
BLOCKED={'PR2-PERSIST','PR2-EVENT','PR2-SCALE','PR2-CONC','PR2-IMPL','PR2-FID','PR2-MIG','PR2-CORPUS','PR2-PART','PR2-IR','PR2-TEST','PR2-BP','PR2-AUDIT'}
def git(*a): return subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def load_at(ref,p): return json.loads(git("show",f"{ref}:{p.relative_to(ROOT).as_posix()}"))
def read_at(ref,p): return git("show",f"{ref}:{p.relative_to(ROOT).as_posix()}")
def rows(m): return {x["workstream_id"]:x for x in m["workstreams"]}
def test_pass_and_no_src_owned_gap():
 r=load(R); assert r["review_result"]=="PASS" and r["blocking_findings"]==[]; assert r["completion_findings"]["missing_pr2_src_owned_doctrine_found"] is False; assert all(v is False for v in r["nonauthority"].values())
def test_completion_domains_are_covered():
 f=load(R)["completion_findings"]; req=["external_source_nonauthority_governed","research_layers_remain_distinct","intake_and_reconnaissance_governed","pressure_extraction_outputs_and_stop_conditions_governed","cross_source_synthesis_governed","provenance_continuity_required","heterogeneous_methods_qualified","mechanical_ecology_and_utilization_preserved","bounded_research_packet_contract_defined","escalation_routes_explicit","legacy_surfaces_disposed","runtime_origin_firewall_intact","frequency_does_not_create_doctrine_or_prevalence"]; assert all(f[k] is True for k in req)
def test_research_timing_is_bounded():
 q=load(R)["research_start_posture"]; assert q["bounded_calibration_pilot"]["methodologically_ready_after_pr2_src_acceptance"] is True; assert q["bounded_calibration_pilot"]["authorized_by_this_review"] is False; assert q["full_corpus_research_campaign"]["minimum_governance_before_start"]==["PR2-ORG","PR2-CORPUS"]; assert q["research_to_myravant_design_handoff"]["required_before_unqualified_handoff"]==["PR2-ORG","PR2-IR"]; assert q["specialized_fiction_research"]["required"]==["PR2-FICT"]; assert q["specialized_simulation_exemplar_research"]["required"]==["PR2-SIMEX"]
def test_review_is_published_without_authority_expansion():
 r=load_at(CLOSURE_MERGE,R); assert r["artifact_version"]=="0.1.1" and r["status"]=="complete" and r["publication_state"]=="merged"; assert r["pull_request"]==PR and r["branch_head"]==HEAD and r["merge_commit"]==MERGE and r["merge_tree"]==TREE; assert r["post_merge_closure_authorization_reference"]==CLOSURE_AUTH
def test_manifest_records_terminal_src_and_readiness_only_release_at_closure():
 m=load_at(CLOSURE_MERGE,M); by=rows(m); s=by["PR2-SRC"]; tr={x["tranche_id"]:x for x in s["planned_tranches"]}; assert m["artifact_version"]=="0.4.16"; assert s["status"]=="merged" and s["current_tranche"]=="PR2-SRC-D"; assert s["current_tranche_authorization_reference"]==AUTH and s["tranche_authority_effect"]==EFFECT and s["completion_review_result"]=="PASS"; assert s["pull_request"]==PR and s["branch_head"]==HEAD and s["merge_commit"]==MERGE and s["completion_state"]=="merged"; assert s["post_merge_closure_authorization_reference"]==CLOSURE_AUTH; assert tr["PR2-SRC-C"]["state"]=="merged" and tr["PR2-SRC-C"]["pull_request"]==384 and tr["PR2-SRC-C"]["merge_commit"]==BASE; assert tr["PR2-SRC-D"]["state"]=="merged" and tr["PR2-SRC-D"]["pull_request"]==PR and tr["PR2-SRC-D"]["branch_head"]==HEAD and tr["PR2-SRC-D"]["merge_commit"]==MERGE and tr["PR2-SRC-D"]["source_processing_authorized"] is False; assert m["r3_conformance_target"]["execution_authorized"] is False; assert all(by[w]["status"]=="ready_pending_authorization" and by[w]["authorization_reference"] is None for w in READY); assert all(by[w]["status"]=="blocked" and by[w]["authorization_reference"] is None for w in BLOCKED)
def test_program_and_decision_record_post_merge_closure():
 p=read_at(CLOSURE_MERGE,P); d=read_at(CLOSURE_MERGE,D); assert "**Artifact version:** `0.4.16`" in p; assert "### 5.13 PR2-SRC post-merge closure recording" in p; assert "`PR2-SRC` is terminal `merged`" in p; assert "`PR2-ORG`, `PR2-FICT`, and `PR2-SIMEX` are" in p and "`ready_pending_authorization`" in p; assert "PR2-SRC-MERGE-CLOSURE-001" in d and CLOSURE_AUTH in d and HEAD in d and MERGE in d

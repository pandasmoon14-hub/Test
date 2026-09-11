# Executable validation for PR2-SRC post-merge closure.
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAN=ROOT/"docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG=ROOT/"docs/doctrine/control/post_r2a_transition_program.md"
REVIEW=ROOT/"docs/doctrine/reviews/pr2_src_source_research_completion_review.yaml"
DEC=ROOT/"docs/decisions/current_decisions_log.md"

PR=385
HEAD="7fd2f1c202abd7107dc2918e168d7885fb9452ce"
MERGE="376214e1b715de34160dfb03d328547f510b6586"
TREE="bcf9dd80d9a39594e60a62218bff3ee64aa85abb"
AUTH="owner_directive_2026-09-11_pr2_src_post_merge_closure"
EFFECT="source_research_post_merge_lifecycle_reconciliation_only"

def load(p): return json.loads(p.read_text(encoding="utf-8"))

def test_src_merge_bookkeeping_is_exact():
 m=load(MAN); by={x["workstream_id"]:x for x in m["workstreams"]}; s=by["PR2-SRC"]; tr={x["tranche_id"]:x for x in s["planned_tranches"]}
 assert m["artifact_version"]=="0.4.16"
 assert s["status"]=="merged" and s["completion_state"]=="merged"
 assert s["pull_request"]==PR and s["branch_head"]==HEAD and s["merge_commit"]==MERGE
 assert s["post_merge_closure_authorization_reference"]==AUTH
 assert s["post_merge_closure_authority_effect"]==EFFECT
 assert s["post_merge_closure_recorded_from"]==MERGE and s["post_merge_closure_tree"]==TREE
 assert tr["PR2-SRC-D"]["state"]=="merged"
 assert tr["PR2-SRC-D"]["pull_request"]==PR and tr["PR2-SRC-D"]["branch_head"]==HEAD and tr["PR2-SRC-D"]["merge_commit"]==MERGE and tr["PR2-SRC-D"]["merge_tree"]==TREE

def test_review_is_complete_and_still_nonauthorizing():
 r=load(REVIEW)
 assert r["artifact_version"]=="0.1.1" and r["status"]=="complete" and r["publication_state"]=="merged"
 assert r["review_result"]=="PASS" and r["blocking_findings"]==[]
 assert r["pull_request"]==PR and r["branch_head"]==HEAD and r["merge_commit"]==MERGE and r["merge_tree"]==TREE
 assert r["post_merge_closure_authorization_reference"]==AUTH
 assert all(v is False for v in r["nonauthority"].values())

def test_dependency_release_is_readiness_only():
 m=load(MAN); by={x["workstream_id"]:x for x in m["workstreams"]}
 for w in ("PR2-ORG","PR2-FICT","PR2-SIMEX"):
  assert by[w]["status"]=="ready_pending_authorization" and by[w]["authorization_reference"] is None
 for w in ("PR2-CORPUS","PR2-IR"):
  assert by[w]["status"]=="blocked" and by[w]["authorization_reference"] is None
 assert m["r2_gate_state"]["R3"]=="ready_pending_authorization"
 assert m["r3_conformance_target"]["execution_authorized"] is False

def test_cross_recording_preserves_closure_boundary():
 p=PROG.read_text(encoding="utf-8"); d=DEC.read_text(encoding="utf-8")
 assert "### 5.13 PR2-SRC post-merge closure recording" in p
 assert "`PR2-SRC` is terminal `merged`" in p
 assert "The recommended next source-governance authorization\ntarget is `PR2-ORG`." in p
 assert "PR2-SRC-MERGE-CLOSURE-001" in d
 for token in (HEAD,MERGE,TREE,AUTH,EFFECT):
  assert token in d
 assert "does not authorize source acquisition" in d

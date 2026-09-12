# Executable validation for PR2-ORG post-merge lifecycle closure.
from __future__ import annotations
import json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAN=ROOT/"docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG=ROOT/"docs/doctrine/control/post_r2a_transition_program.md"
DEC=ROOT/"docs/decisions/current_decisions_log.md"
CONTRACT=ROOT/"docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md"
ACTIVATION_TEST=ROOT/"tests/test_pr2_org_originality_provenance_eligibility.py"
PR=387
HEAD="a7aed059e1b96872150c05203dfdb9c07affe831"
MERGE="031053afd9ac581cfc421554ee3383a11a0dc2bd"
TREE="ac770e1c69a448545b0a58eb7ed49a0b13f81614"
AUTH="owner_directive_2026-09-11_pr2_org_post_merge_closure"
EFFECT="originality_eligibility_post_merge_lifecycle_reconciliation_only"
ACTIVATION_AUTH="owner_directive_2026-09-11_pr2_org_activation"

def git(*a): return subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def load_at(ref,p): return json.loads(git("show",f"{ref}:{p.relative_to(ROOT).as_posix()}"))
def read_at(ref,p):
 return subprocess.check_output(
  ["git","show",f"{ref}:{p.relative_to(ROOT).as_posix()}"],
  cwd=ROOT,
  text=True,
 )
def rows(m): return {x["workstream_id"]:x for x in m["workstreams"]}

def test_org_merge_bookkeeping_is_exact():
 m=load(MAN); by=rows(m); o=by["PR2-ORG"]
 assert m["artifact_version"]=="0.4.18"
 assert o["status"]=="merged" and o["completion_state"]=="merged"
 assert o["pull_request"]==PR and o["branch_head"]==HEAD and o["merge_commit"]==MERGE
 assert o["post_merge_closure_authorization_reference"]==AUTH
 assert o["post_merge_closure_authority_effect"]==EFFECT
 assert o["post_merge_closure_recorded_from"]==MERGE and o["post_merge_closure_tree"]==TREE
 assert o["validation_evidence"]==[
  "PR2-ORG focused validation:47 passed",
  "PR2-ORG full local repository suite:9013 passed, 10 skipped, 2 xfailed, 1 warning",
  "PR2-ORG GitHub Actions CI #173:success",
  "PR2-ORG git diff --check:clean",
  "PR2-ORG semantic audit:PASS",
 ]

def test_activation_snapshot_is_preserved_as_historical_evidence():
 m=load_at(MERGE,MAN); by=rows(m); o=by["PR2-ORG"]
 assert m["artifact_version"]=="0.4.17"
 assert o["status"]=="active" and o["authorization_reference"]==ACTIVATION_AUTH
 assert o["pull_request"] is None and o["branch_head"] is None and o["merge_commit"] is None
 t=ACTIVATION_TEST.read_text(encoding="utf-8")
 assert f'MERGED_ACTIVATION_SNAPSHOT="{MERGE}"' in t
 assert "load_at(MERGED_ACTIVATION_SNAPSHOT,MAN)" in t
 assert "read_at(MERGED_ACTIVATION_SNAPSHOT,PROG)" in t

def test_dependency_release_is_readiness_only():
 m=load(MAN); by=rows(m)
 for w in ("PR2-CORPUS","PR2-IR","PR2-FICT","PR2-SIMEX"):
  assert by[w]["status"]=="ready_pending_authorization" and by[w]["authorization_reference"] is None
 for w in ("PR2-CORPUS","PR2-IR"):
  assert by[w]["starting_baseline"] is None
 assert m["r2_gate_state"]["R3"]=="ready_pending_authorization"
 assert m["r3_conformance_target"]["candidate_count"]==34
 assert m["r3_conformance_target"]["execution_authorized"] is False

def test_closure_does_not_change_org_contract_or_activate_successor():
 assert CONTRACT.read_text(encoding="utf-8")==read_at(MERGE,CONTRACT)
 m=load(MAN)
 assert [x["workstream_id"] for x in m["workstreams"] if x["status"]=="active"]==[]
 c=CONTRACT.read_text(encoding="utf-8")
 for token in ("source_research_authority: none","corpus_governance_authority: none","information_barrier_authority: none","canon_promotion_authority: none","runtime_authority: none"):
  assert token in c

def test_program_and_decision_record_closure_without_execution_authority():
 p=PROG.read_text(encoding="utf-8"); d=DEC.read_text(encoding="utf-8")
 assert "**Artifact version:** `0.4.18`" in p
 assert "### 5.15 PR2-ORG post-merge closure recording" in p
 assert "PR2-ORG is\nterminal `merged`" in p
 assert "`PR2-CORPUS` and `PR2-IR` are now\n`ready_pending_authorization`" in p
 assert "preferred source-governance authorization target after originality governance" in p
 assert "PR2-ORG-MERGE-CLOSURE-001" in d
 for token in (HEAD,MERGE,TREE,AUTH,EFFECT): assert token in d
 assert "does not authorize source acquisition" in d
 assert "R3 remains `ready_pending_authorization`" in d

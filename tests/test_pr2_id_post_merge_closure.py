"""Executable validation for PR2-ID post-merge closure."""
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MERGE="1d1b16004b4bee0c75ca42c82900755ec29022bd"
HEAD="024236e0ce9af3b6622e0a5b7be3a1ec3d4c99a3"
PR=380
AUTH="owner_directive_2026-09-10_pr2_id_post_merge_closure"
MAN=ROOT/"docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG=ROOT/"docs/doctrine/control/post_r2a_transition_program.md"
CON=ROOT/"docs/doctrine/control/myravant_identity_migration_contract.md"
DEC=ROOT/"docs/decisions/current_decisions_log.md"
CLASSES=["roadmap_currentness_setting_and_planning_authority","astra_prefixed_governance_and_working_group_role_identity","r1b_shared_vocabulary_identity_and_exact_parity","software_namespace_future_alias_or_deprecation_policy"]
ALLOWED={'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'docs/decisions/current_decisions_log.md', 'docs/doctrine/control/post_r2a_transition_program.md', 'tests/test_pr2_id_post_merge_closure.py', 'tests/test_pr2_id_myravant_identity_migration.py', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_id_t2d_roadmap_registry_adjudication.py', 'docs/doctrine/control/myravant_identity_migration_contract.md', 'tests/test_pr2_id_t2e_completion_recording.py'}
def load(p): return json.loads(p.read_text())
def git(*a): return subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
def test_merge_bookkeeping_is_exact():
 m=load(MAN); by={x["workstream_id"]:x for x in m["workstreams"]}; p=by["PR2-ID"]
 assert m["artifact_version"]=="0.4.11" and p["status"]=="merged"
 assert p["pull_request"]==PR and p["branch_head"]==HEAD and p["merge_commit"]==MERGE and p["completion_state"]=="merged"
 assert p["post_merge_closure_authorization_reference"]==AUTH and p["post_merge_closure_recorded_from"]==MERGE
 assert p["residual_gaps"]==[] and [x["class_id"] for x in p["carried_forward_obligations"]]==CLASSES
def test_downstream_remains_unauthorized():
 m=load(MAN); by={x["workstream_id"]:x for x in m["workstreams"]}
 assert m["r2_gate_state"]["R3"]=="ready_pending_authorization" and m["r3_conformance_target"]["execution_authorized"] is False
 for w in ["PR2-SRC","PR2-ORG","PR2-CORPUS","PR2-IR","PR2-FICT","PR2-SIMEX","PR2-SCALE","PR2-PART","PR2-CONC","PR2-FID","PR2-EVENT","PR2-PERSIST","PR2-BP","PR2-AUDIT","PR2-MIG","PR2-TEST","PR2-IMPL"]:
  assert by[w]["status"]=="blocked" and by[w]["authorization_reference"] is None
def test_cross_recording_and_scope():
 c=CON.read_text(); p=PROG.read_text(); d=DEC.read_text()
 assert "**Status:** `merged`" in c and "## 9F. Pull-request merge closure" in c
 assert "### 5.8 PR2-ID post-merge closure recording" in p and "`PR2-ID` is `merged` through PR `#380`" in p
 assert "PR2-ID-MERGE-CLOSURE-001" in d
 for t in [c,p,d]: assert HEAD in t and MERGE in t
 changed=set(git("diff","--name-only",MERGE).splitlines())|set(git("ls-files","--others","--exclude-standard").splitlines()); changed.discard("")
 assert changed==ALLOWED
 assert not any(x.startswith(("src/","schemas/")) for x in changed)

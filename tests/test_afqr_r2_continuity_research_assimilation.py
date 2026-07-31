"""Deterministic R2-0 provenance, ownership, scope, and gate validation."""
from __future__ import annotations
import hashlib,json,re,subprocess
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE="dbecb91cb42c665f586b644b3f359f29bcef91a3"
ACCEPTED_R2_0_HEAD="9382958197c9d5dee9d29cb5f9d051147237c64d"
R1="bbc9d58cb23f1616327f73294def6ec42055a324"
ABANDONED="50c0320acd1a9a075cba18e1309dd3d15ac5c44d"
REV=ROOT/"docs/doctrine/reviews"; INTAKE=REV/"afqr_r2_continuity_research_intake_packet.md"
MANIFEST=REV/"afqr_r2_continuity_research_source_manifest.yaml"; LEDGER=REV/"afqr_r2_continuity_claim_and_owner_routing_ledger.yaml"
REPORT=REV/"afqr_r2_continuity_research_assimilation_report.md"; FILES=REV/"afqr_r2_doctrine_drift_file_manifest.yaml"
PLAN=ROOT/"docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md"; DECISIONS=ROOT/"docs/decisions/current_decisions_log.md"
ALLOW={"docs/decisions/current_decisions_log.md","docs/doctrine/astra_doctrine_registry_v0_1.yaml","docs/doctrine/control/afqr_01_20_consolidation_program_plan.md","docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md","docs/doctrine/reviews/afqr_r2_continuity_claim_and_owner_routing_ledger.yaml","docs/doctrine/reviews/afqr_r2_continuity_research_assimilation_report.md","docs/doctrine/reviews/afqr_r2_continuity_research_source_manifest.yaml","docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml","tests/test_afqr_r1e_formal_completion_review.py","tests/test_afqr_r2_continuity_research_assimilation.py"}
FAMILIES={f"CF-{i:02d}" for i in range(1,14)}
def load(p): return json.loads(p.read_text())
def values(x,key):
 out=set()
 if isinstance(x,dict):
  for k,v in x.items():
   if k==key and isinstance(v,str): out.add(v)
   out|=values(v,key)
 elif isinstance(x,list):
  for v in x: out|=values(v,key)
 return out
def claim(n): return next(x for x in load(LEDGER)["claims"] if x["claim_id"]==f"R2-CLAIM-{n:04d}")
def metrics():
 cs=load(LEDGER)["claims"]
 return {"by_consensus_level":dict(sorted(Counter(c["consensus"]["level"] for c in cs).items())),"by_family":dict(sorted(Counter(c["claim_family_id"] for c in cs).items())),"by_primary_outcome":dict(sorted(Counter(c["primary_outcome"] for c in cs).items())),"by_target_work_package":dict(sorted(Counter(c["target_work_package"] for c in cs).items())),"rejected_overengineering":sum(c["primary_outcome"]=="rejected_as_overengineered" for c in cs),"total_claims":len(cs),"unresolved_owner_questions":sum(bool(c["owner_analysis"]["unresolved_owner_question"]) for c in cs)}
def test_exact_committed_scope_and_ancestry():
 assert subprocess.run(["git","merge-base","--is-ancestor",ACCEPTED_R2_0_HEAD,"HEAD"]).returncode==0
 assert subprocess.run(["git","merge-base","--is-ancestor",BASE,"HEAD"]).returncode==0
 assert subprocess.run(["git","merge-base","--is-ancestor",R1,"HEAD"]).returncode==0
 if subprocess.run(["git","cat-file","-e",f"{ABANDONED}^{{commit}}"],capture_output=True).returncode==0: assert subprocess.run(["git","merge-base","--is-ancestor",ABANDONED,"HEAD"],capture_output=True).returncode!=0
 changed=set(subprocess.check_output(["git","diff","--name-only",f"{BASE}...{ACCEPTED_R2_0_HEAD}"],text=True).splitlines())
 assert changed==ALLOW
 assert subprocess.run(["git","diff","--check",f"{BASE}...{ACCEPTED_R2_0_HEAD}"],capture_output=True).returncode==0
 num=subprocess.check_output(["git","diff","--numstat",f"{BASE}...{ACCEPTED_R2_0_HEAD}"],text=True); assert "-\t-\t" not in num
 assert not subprocess.check_output(["git","diff","--name-status","--diff-filter=D",f"{BASE}...{ACCEPTED_R2_0_HEAD}"],text=True).strip()
 forbidden=("src/","schemas/","conversion/","canon/","model/","narration/","ui/","live_play","rt_002g","working/afqr_consolidation_inputs/")
 assert not [p for p in changed if any(x in p.lower() for x in forbidden) or p.endswith((".zip",".pdf",".png",".jpg"))]
def test_manifest_exactly_matches_intake_inventory():
 rows={m.group(1):m.groups()[1:] for m in re.finditer(r"\| `(R2-RES-[^`]+)` \| `([^`]+)` \| [^|]+ \| `([0-9a-f]{64})` \| ([0-9]+) \| ([0-9]+) \|",INTAKE.read_text())}
 ss=load(MANIFEST)["sources"]; assert len(rows)==len(ss)==5
 for s in ss:
  fn,sha,lines,size=rows[s["source_id"]]; assert (s["original_filename"],s["sha256"],s["line_count"],s["byte_size"])==(fn,sha,int(lines),int(size))
  assert len(s["unique_contributions"])>=3 and s["primary_contribution"] not in s["unique_contributions"]
  assert "did not independently inspect" in s["inspection_posture"]
 assert [s["research_family"] for s in ss].count("actual_play_deterministic_patterns")==1 and [s["research_family"] for s in ss].count("branch_aware_continuity")==4
def test_repository_provenance_and_consensus():
 packet=INTAKE.read_text().splitlines(); controlled={"packet_attributed","source_contribution","dissenting","uncertain"}
 for c in load(LEDGER)["claims"]:
  e=c["repository_evidence"]; assert e["path"]==str(INTAKE.relative_to(ROOT)) and e["evidence_basis"]=="intake_packet_synthesis"
  loc=e["locator"]; assert 1<=loc["line_start"]<=loc["line_end"]<=len(packet); assert loc["subheading"] in packet[loc["line_start"]-1]
  kinds=[u["support_kind"] for u in c["upstream_source_support"]]; assert set(kinds)<=controlled and "direct" not in kinds
  supporting=sum(k not in {"dissenting","uncertain"} for k in kinds); assert c["consensus"]["supporting_source_count"]==supporting
  if "uncertain" in kinds: assert c["consensus"]["level"]!="unanimous"
def test_source_claim_parity_and_exact_references():
 doc=load(LEDGER); cs=doc["claims"]; ss=load(MANIFEST)["sources"]
 for s in ss: assert set(s["claim_ids"])=={c["claim_id"] for c in cs if s["source_id"] in {u["source_id"] for u in c["upstream_source_support"]}}
 vocab=load(ROOT/"docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml"); r1c=load(ROOT/"docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml")
 r1d="\n".join((ROOT/p).read_text() for p in ["docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md","docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md","docs/doctrine/consolidation/afqr_world_action_sensing.md"])
 for c in cs:
  assert set(c["afqr_ids"])<={f"AFQR-{i:02d}" for i in range(1,21)}; assert set(c["r1b_term_ids"])<=values(vocab,"term_id"); assert set(c["r1c_invariant_ids"])<=values(r1c,"invariant_id"); assert set(c["r1c_edge_ids"])<=values(r1c,"edge_id"); assert set(c["substrate_ids"])<=values(r1c,"substrate_id"); assert all(x in r1d for x in c["r1d_family_ids"])
  if c["current_astra_comparison"]["r1_status"] in {"already_governed","partially_governed","apparent_conflict"}: assert c["r1d_family_ids"] and (c["r1b_term_ids"] or c["r1c_invariant_ids"] or c["r1c_edge_ids"])
  summary=c["current_astra_comparison"]["summary"]; assert "Claim-specific comparison:" in summary and ("not authority" in summary or "no authority" in summary)
def test_compound_owner_safety():
 assert claim(5)["owner_analysis"]["semantic_owner"] is None and claim(5)["owner_analysis"]["component_owners"]["world_valid_time"]=="AFQR-04"
 c13=claim(13); assert c13["owner_analysis"]["semantic_owner"] is None and {"AFQR-04","AFQR-06","AFQR-10","AFQR-20"}<=set(c13["owner_analysis"]["component_owners"].values())
 assert "combined truth/evidence/knowledge/sensing owner" in " ".join(c13["owner_analysis"]["prohibited_owner_transfers"])
 assert "reservations" not in claim(14)["normalized_claim"].lower() and "reservation" in claim(31)["normalized_claim"].lower()
 assert claim(11)["owner_analysis"]["semantic_owner"] is None and "combined semantic owner" in " ".join(claim(11)["owner_analysis"]["prohibited_owner_transfers"])
 assert claim(20)["owner_analysis"]["semantic_owner"] is None and claim(20)["owner_analysis"]["component_owners"]["commitment_of_owner_prepared_transitions_only"]=="AFQR-01"
 assert claim(21)["owner_analysis"]["semantic_owner"] is None and "unresolved cross-phase owner" in claim(21)["owner_analysis"]["component_owners"].values()
 assert claim(30)["owner_analysis"]["semantic_owner"] is None
 for c in load(LEDGER)["claims"]: assert any("storage, journaling, replay, branching, commitment, and handoff" in x for x in c["owner_analysis"]["prohibited_owner_transfers"])
def test_ledger_wide_afqr_responsibility_and_residual_owner_consistency():
 def responsibility(afqr):
  n=int(afqr[-2:]); return f"CORE-RESP-{n:02d}" if n<=9 else f"AGENCY-RESP-{n:02d}" if n<=15 else f"WORLD-RESP-{n:02d}"
 r1d="\n".join((ROOT/p).read_text() for p in ["docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md","docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md","docs/doctrine/consolidation/afqr_world_action_sensing.md"])
 for c in load(LEDGER)["claims"]:
  afqrs=set(c["afqr_ids"]); component_afqrs={v for v in c["owner_analysis"]["component_owners"].values() if re.fullmatch(r"AFQR-\d{2}",v)}
  assert component_afqrs<=afqrs and {responsibility(v) for v in component_afqrs}<=set(c["r1d_family_ids"])
  assert {v for v in c["owner_analysis"]["supporting_owners"] if re.fullmatch(r"AFQR-\d{2}",v)}<=afqrs
  summary_ids=set(re.findall(r"(?:CORE|AGENCY|WORLD)-RESP-\d{2}",c["current_astra_comparison"]["summary"])); assert summary_ids<=set(c["r1d_family_ids"]) and all(v in r1d for v in summary_ids)
 c5=claim(5); assert {"CORE-RESP-06","AGENCY-RESP-10"}<=set(c5["r1d_family_ids"]) and "AGENCY-RESP-06" not in json.dumps(c5)
 c11=claim(11); assert {"AFQR-07","AFQR-20"}<=set(c11["afqr_ids"]) and {"CORE-RESP-07","WORLD-RESP-20"}<=set(c11["r1d_family_ids"])
 assert "AFQR-07" not in claim(14)["owner_analysis"]["supporting_owners"] and "reservation state" not in claim(15)["normalized_claim"].lower()
 assert not {"AFQR-02","AFQR-19"}&set(claim(31)["owner_analysis"]["supporting_owners"])
 report=REPORT.read_text(); assert "R4 receives typed-reservation substrate pressure" in report and "R5 receives stale-command and expected-version retrofit pressure" in report and "R4 and R5 remain blocked" in report
def test_counts_actions_limits_and_gate():
 expected=metrics(); doc=load(LEDGER); assert doc["claim_count"]==31 and doc["count_summary"]=={k:v for k,v in expected.items() if k!="total_claims"}
 assert load(FILES)["r2_0_metrics"]==expected
 for p in (REPORT,DECISIONS):
  blob=re.search(r"Machine-checkable R2-0 metrics:\*\* `([^`]+)`",p.read_text()); assert blob and json.loads(blob.group(1))==expected
 assert all(c["proposed_next_action"] and "named work package" not in c["proposed_next_action"] for c in doc["claims"])
 limits={MANIFEST:(600,100*1024),LEDGER:(3500,400*1024),REPORT:(800,120*1024),PLAN:(1000,150*1024),FILES:(800,120*1024)}
 for p,(lines,size) in limits.items():
  raw=subprocess.check_output(["git","show",f"{ACCEPTED_R2_0_HEAD}:{p.relative_to(ROOT)}"]) if p in {PLAN,FILES} else p.read_bytes()
  assert len(raw.splitlines())<=lines and len(raw)<=size and b"\0" not in raw
 gate=subprocess.check_output(["git","show",f"{ACCEPTED_R2_0_HEAD}:{PLAN.relative_to(ROOT)}"],text=True); assert all(x in gate for x in ("`R1=complete`","`R2=active_incomplete`","`R2-0=complete`","`R2A=ready`","`R2B=blocked`","`R2C=blocked`","`R3–R6=blocked`","`RT-002G=unauthorized`","`temporary_evidence_deletion=unauthorized`"))
def test_accepted_r1_authority_files_unchanged():
 paths=["docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml","docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml","docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md","docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md","docs/doctrine/consolidation/afqr_world_action_sensing.md","docs/doctrine/reviews/afqr_01_20_formal_completion_review.md","docs/doctrine/reviews/afqr_r1e_source_and_vocabulary_audit.yaml","docs/doctrine/reviews/afqr_r1e_dependency_and_parity_audit.yaml","docs/doctrine/reviews/afqr_r1e_escalation_and_substrate_adjudications.yaml","docs/doctrine/reviews/afqr_r1e_consistency_and_corpus_adequacy.yaml"]
 for p in paths: assert hashlib.sha256((ROOT/p).read_bytes()).digest()==hashlib.sha256(subprocess.check_output(["git","show",f"{R1}:{p}"],cwd=ROOT)).digest()

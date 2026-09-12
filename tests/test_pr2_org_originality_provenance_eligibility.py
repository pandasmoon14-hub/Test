# Executable validation for PR2-ORG originality/provenance/eligibility governance.
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md"
MAN=ROOT/"docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG=ROOT/"docs/doctrine/control/post_r2a_transition_program.md"
DEC=ROOT/"docs/decisions/current_decisions_log.md"
FIREWALL=ROOT/"docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md"
AFQR=ROOT/"docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml"

BASE="c14da427bf5c5c21c7ef1655e83aea3519587cc6"
AUTH="owner_directive_2026-09-11_pr2_org_activation"
EFFECT="content_eligibility_and_provenance_governance_only"
OWNED={'docs/doctrine/control/post_r2a_transition_manifest.yaml', 'tests/test_pr2_src_completion_review.py', 'tests/test_pr2_src_post_merge_closure.py', 'tests/test_post_r2a_transition_program.py', 'tests/test_pr2_org_originality_provenance_eligibility.py', 'docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md', 'docs/doctrine/control/post_r2a_transition_program.md', 'docs/decisions/current_decisions_log.md'}

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def rows(m): return {x["workstream_id"]:x for x in m["workstreams"]}

def test_contract_declares_bounded_authority():
 t=CONTRACT.read_text(encoding="utf-8")
 assert "artifact_id: PR2-ORG-ORIGINALITY-PROVENANCE-ELIGIBILITY-001" in t
 assert f"authority_reference: {AUTH}" in t and f"authority_effect: {EFFECT}" in t
 assert f"starting_baseline: {BASE}" in t
 for token in ["source_research_authority: none","corpus_governance_authority: none","information_barrier_authority: none","canon_promotion_authority: none","runtime_authority: none","native_content_authoring_authority: none","live_play_authority: none","legal_advice_authority: none"]:
  assert token in t

def test_contract_preserves_core_originality_laws():
 t=CONTRACT.read_text(encoding="utf-8")
 assert "Traceable internally; independently Myravant externally." in t
 assert "Semantic disposition and content eligibility are separate dimensions." in t
 assert "`eligible_for_separate_canon_review` means only that PR2-ORG has no remaining" in t
 for term in ["renaming","translation","paraphrase","numeric alteration","format conversion","mechanical relabeling","AI rewriting or regeneration","removal of attribution","successful semantic conversion"]:
  assert term in t
 assert "Unknown must remain unknown" in t
 assert "`canon_eligible`" not in t
 assert "`rights_review_required`" not in t
 assert "`eligible_for_separate_canon_review`" in t
 assert "`specialist_rights_review_required`" in t
 assert "`eligibility_review_required`" in t

def test_review_dimensions_are_machine_trackable_and_separate():
 t=CONTRACT.read_text(encoding="utf-8")
 for term in ["provenance_complete","provenance_incomplete","rights_unreviewed","rights_basis_recorded","specialist_rights_review_required","myravant_original_candidate","similarity_review_required","myravant_original_review_passed","quarantined_similarity_risk","quarantined_rights_risk","internal_research_only","eligibility_review_required","distribution_prohibited","distribution_eligible_with_restrictions","distribution_eligible","not_ready_for_canon_review","eligible_for_separate_canon_review"]:
  assert term in t
 for field in ["eligibility_record_id","candidate_id","influence_cluster_refs[]","source_expression_exposure_state","rights_review_state","originality_similarity_state","contamination_quarantine_state","eligibility_disposition","canon_handoff_state","review_decision_ref"]:
  assert field in t
 assert "must not be collapsed into\none confidence score" in t

 eligibility = t.split("### 5.5 Eligibility disposition",1)[1].split("### 5.6 Canon handoff state",1)[0]
 for misplaced in ["licensed_content","public_domain_content","myravant_original_candidate","myravant_original_review_passed","quarantined_similarity_risk","pressure_satisfied_no_content_needed"]:
  assert f"- `{misplaced}`" not in eligibility

 assert "Rights bases such as licensed use" in eligibility
 assert "Originality findings remain in `originality_similarity_state`." in eligibility
 assert "contamination_quarantine_state" in eligibility

def test_contract_handles_corpus_scale_and_outliers_without_fake_certainty():
 t=CONTRACT.read_text(encoding="utf-8")
 for term in ["explicit licenses","open-source or open-content licenses","public-domain claims or determinations","commissioned or assigned work","contributor or user submissions","mixed-license packages","trademark or branding concerns","patent or other non-copyright concerns","generated material with uncertain upstream provenance"]:
  assert term in t
 assert "absence of a source match must not be treated as proof of originality" in t
 assert "Outliers that cannot be resolved by this contract must escalate" in t
 assert "It does not issue jurisdiction-specific legal conclusions." in t

def test_manifest_activates_only_pr2_org_and_preserves_downstream_blocks():
 m=load(MAN); by=rows(m); o=by["PR2-ORG"]
 assert m["artifact_version"]=="0.4.17"
 assert o["status"]=="active" and o["authorization_reference"]==AUTH and o["authority_effect"]==EFFECT and o["starting_baseline"]==BASE
 assert o["control_artifact"]=="docs/doctrine/control/myravant_originality_provenance_eligibility_contract.md"
 assert set(o["owned_paths"])==OWNED
 assert o["pull_request"] is None and o["branch_head"] is None and o["merge_commit"] is None
 assert by["PR2-SRC"]["status"]=="merged"
 for w in ("PR2-CORPUS","PR2-IR"):
  assert by[w]["status"]=="blocked" and by[w]["authorization_reference"] is None
 for w in ("PR2-FICT","PR2-SIMEX"):
  assert by[w]["status"]=="ready_pending_authorization" and by[w]["authorization_reference"] is None
 assert m["r2_gate_state"]["R3"]=="ready_pending_authorization"
 assert m["r3_conformance_target"]["execution_authorized"] is False

def test_org_does_not_absorb_ir_corpus_afqr15_or_runtime_firewall():
 t=CONTRACT.read_text(encoding="utf-8")
 f=FIREWALL.read_text(encoding="utf-8")
 a=load(AFQR); af15=[x for x in a["afqr_records"] if x["afqr_id"]=="AFQR-15"][0]
 assert "PR2-IR will own the explicit representation and information-flow barrier" in t
 assert "PR2-CORPUS will own the 1,000+ source registry" in t
 assert "AFQR-15 governs modeled institutions, governance, jurisdiction, rights, law" in t
 assert "Institutions Governance Jurisdiction Rights Law Policy Adjudication Legitimacy and Enforcement" in af15["full_title"]
 assert "The existing conversion/runtime origin firewall remains authoritative." in t
 assert "Extraction and conversion end before runtime begins." in f

def test_program_and_decision_record_activation_without_downstream_authorization():
 p=PROG.read_text(encoding="utf-8"); d=DEC.read_text(encoding="utf-8")
 assert "**Artifact version:** `0.4.17`" in p
 assert "### 5.14 PR2-ORG originality, provenance, and content-eligibility activation" in p
 assert AUTH in p and BASE in p
 assert "`PR2-ORG` is `active`" in p
 assert "`PR2-CORPUS` and `PR2-IR` remain blocked" in p
 assert "PR2-ORG-ACTIVATION-001" in d and AUTH in d and EFFECT in d and BASE in d
 assert "does not authorize source acquisition" in d

# Executable validation for PR2-SRC-C legacy surface disposition.
from __future__ import annotations
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"docs/doctrine/control/myravant_legacy_source_conversion_surface_disposition.yaml"
MANIFEST=ROOT/"docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROGRAM=ROOT/"docs/doctrine/control/post_r2a_transition_program.md"
DECISIONS=ROOT/"docs/decisions/current_decisions_log.md"
BASELINE="70f7195100d0ccb7ba3c4cbd0dc34d684717ccaa"
AUTH="owner_directive_2026-09-11_pr2_src_c_activation"
EFFECT="legacy_source_conversion_surface_disposition_only"
SRC_B_HEAD="cabd12d56e7e036b2b839f21486776b49ebff56b"
SRC_C_MERGE="21b4ba706bb3f68aeb51dc4195fe1aa60014a439"
AUDITED={
    "docs/operations/current_decisions_log_v0_1.md": [
        "blob",
        "f7419794082c2cfaba9d2e1d1f7d9fcaa0d0452c"
    ],
    "docs/doctrine/control/A00_mechanical_posture_and_ruleset_non_adoption.md": [
        "blob",
        "ae26c76c276a515999aa33195562e2fd6c46dddc"
    ],
    "docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md": [
        "blob",
        "a4ae23278b46071d612d18b31ef2df77ba59422a"
    ],
    "docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md": [
        "blob",
        "c6419d38a186a6fa1791c910a7b2448a43d6677b"
    ],
    "docs/doctrine/native_design/d_series/source_packs": [
        "tree",
        "3992400400c6c54d757c437145253e23ca59c21a"
    ],
    "docs/doctrine/native_design/d_series/_manifests/d_series_doctrine_pack_import_manifest.json": [
        "blob",
        "9ddd092a7083fd6e9398a60f6558a4f6bb1f6cef"
    ]
}
EXPECTED={"docs/operations/current_decisions_log_v0_1.md":"historical_only","docs/doctrine/control/A00_mechanical_posture_and_ruleset_non_adoption.md":"research_only","docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md":"retain","docs/doctrine/control/RT012_d_series_promotion_boundary_owner_specification.md":"retain","docs/doctrine/native_design/d_series/source_packs":"research_only","docs/doctrine/native_design/d_series/_manifests/d_series_doctrine_pack_import_manifest.json":"historical_only"}
BLOCKED={'PR2-SCALE', 'PR2-IR', 'PR2-TEST', 'PR2-IMPL', 'PR2-EVENT', 'PR2-FICT', 'PR2-BP', 'PR2-PART', 'PR2-CONC', 'PR2-PERSIST', 'PR2-MIG', 'PR2-SIMEX', 'PR2-CORPUS', 'PR2-ORG', 'PR2-FID', 'PR2-AUDIT'}
def git(*a): return subprocess.check_output(["git",*a],cwd=ROOT,text=True).strip()
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def load_at(ref,p): return json.loads(git("show",f"{ref}:{p.relative_to(ROOT).as_posix()}"))
def read_at(ref,p): return git("show",f"{ref}:{p.relative_to(ROOT).as_posix()}")
def test_control_record_is_classification_only():
 d=load(LEDGER); assert d["authority_reference"]==AUTH and d["authority_effect"]==EFFECT; assert d["audit_baseline"]==BASELINE; assert d["classification_only"] is True; assert d["remediation_authority"]=="none" and d["deletion_authority"]=="none"; assert d["bulk_source_processing_authority"]=="none"
def test_audited_objects_are_exact():
 for path, pair in AUDITED.items(): assert git("rev-parse",f"{BASELINE}:{path}") == pair[1]
def test_six_surface_inventory_and_dispositions_are_exact():
 d=load(LEDGER); rec={x["path"]:x for x in d["surface_records"]}; assert len(rec)==6 and set(rec)==set(AUDITED); assert {p:x["recommended_disposition"] for p,x in rec.items()}==EXPECTED; assert d["disposition_summary"]=={"retain":2,"research_only":2,"historical_only":2,"all_other_dispositions":0}; assert all(x["remediation_authorized"] is False and x["provenance_preservation_required"] is True for x in rec.values())
def test_import_manifest_confirms_23_draft_packs():
 imp=json.loads(git("show",f"{BASELINE}:docs/doctrine/native_design/d_series/_manifests/d_series_doctrine_pack_import_manifest.json")); assert imp["status"]=="draft_source_pack_import" and imp["pack_count"]==23; assert all(x["status"]=="draft_source_pack_not_current_doctrine" for x in imp["packs"])
def test_active_firewall_is_retained_and_drafts_are_not_promoted():
 rec={x["path"]:x for x in load(LEDGER)["surface_records"]}; assert rec["docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md"]["declared_status_at_audit"]=="active_control_doctrine" and rec["docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md"]["recommended_disposition"]=="retain"; assert rec["docs/doctrine/control/A00_mechanical_posture_and_ruleset_non_adoption.md"]["declared_status_at_audit"]=="draft" and rec["docs/doctrine/control/A00_mechanical_posture_and_ruleset_non_adoption.md"]["recommended_disposition"]=="research_only"; assert rec["docs/doctrine/native_design/d_series/source_packs"]["recommended_disposition"]=="research_only"
def test_manifest_advances_only_to_src_c():
 m=load_at(SRC_C_MERGE,MANIFEST); rows={x["workstream_id"]:x for x in m["workstreams"]}; src=rows["PR2-SRC"]; tr={x["tranche_id"]:x for x in src["planned_tranches"]}; assert m["artifact_version"]=="0.4.14"; assert src["status"]=="active" and src["current_tranche"]=="PR2-SRC-C"; assert src["current_tranche_authorization_reference"]==AUTH and src["current_tranche_starting_head"]==BASELINE; assert src["next_tranche_authorized"] is False; assert tr["PR2-SRC-B"]["state"]=="merged" and tr["PR2-SRC-B"]["branch_head"]==SRC_B_HEAD and tr["PR2-SRC-B"]["merge_commit"]==BASELINE; assert tr["PR2-SRC-C"]["state"]=="active" and tr["PR2-SRC-C"]["remediation_authorized"] is False; assert tr["PR2-SRC-D"]["state"]=="blocked_pending_separate_authorization"; assert m["r3_conformance_target"]["execution_authorized"] is False; assert all(rows[w]["status"]=="blocked" and rows[w]["authorization_reference"] is None for w in BLOCKED)
def test_program_and_decision_log_record_boundaries():
 p=read_at(SRC_C_MERGE,PROGRAM); d=read_at(SRC_C_MERGE,DECISIONS); assert "**Artifact version:** `0.4.14`" in p and "### 5.11 PR2-SRC-C legacy source/conversion surface disposition" in p and "`PR2-SRC` remains `active` with current tranche `PR2-SRC-C`" in p; assert "PR2-SRC-C-ACTIVATION-001" in d and AUTH in d and EFFECT in d and "No classified surface is modified by SRC-C." in d and "PR2-SRC-D remains separately unauthorized." in d
def test_src_c_does_not_modify_audited_surfaces():
 changed={x for x in git("diff","--name-only",BASELINE).splitlines() if x}|{x for x in git("ls-files","--others","--exclude-standard").splitlines() if x}; assert not (changed & set(AUDITED)); assert not any(x.startswith("docs/doctrine/native_design/d_series/source_packs/") for x in changed)

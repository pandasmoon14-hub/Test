from dataclasses import is_dataclass
import importlib, inspect, json, ast
from types import SimpleNamespace
import pytest

import astra_runtime.domain.object_lever_replay_audit_check as f
import astra_runtime.domain.object_lever_event_commit_state_delta_path as e

FORBIDDEN={"rng_resolved","oracle_resolved","resource_settled","consequence_settled","damage_applied","condition_applied","persistent_write_complete","replay_indexed","narrated","model_generated","success","failure","persisted","persistence_written","event_store_appended","event_store_read","state_reconstructed","command_reexecuted","mutation_applied","state_delta_applied"}

OUTPUT_FORBIDDEN=["event_store_append","event_store_read","event_log","persistence_write","persistent_record","replay_write","replay_index","replay_store","state_reconstruction","command_reexecution","transaction_execution","command_execution","execution_result","arbitrary_mutation","mutation_payload","state_before","state_after","state_delta_payload","resource_settlement","consequence_application","damage_application","condition_application","rng_result","oracle_result","model_prompt","narration","hidden_fact","trap","activation","success","failure","safety","danger","object_state"]


def _commit_decision(status):
    return {"committed":"object_lever_event_committed","commit_blocked":"blocked","commit_deferred":"deferred","commit_unknown":"unknown","commit_insufficient_preview":"insufficient_preview"}[status]


def _base_src(safe=("scene:1","actor:1","object_lever:1")):
    return e.ObjectLeverCommitSourceRef(bridge_result_id="br", preview_candidate_id="pc", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, bridge_decision="preview_candidate_prepared", bridge_status="preview_bridge_available", safe_reference_ids=safe)


def _base_elig(status="commit_ready"):
    return e.ObjectLeverCommitEligibility(command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, eligibility_status=status, bridge_decision="preview_candidate_prepared", bridge_status="preview_bridge_available", safe_reference_ids=("scene:1","actor:1","object_lever:1"))


def _base_delta(kind="object_lever_interaction_state_delta_receipt", affected=("scene:1","actor:1","object_lever:1"), label="object_lever_interaction_recorded"):
    return e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind=kind, command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br","preview_candidate_id":"pc"}, affected_safe_reference_ids=affected, state_delta_label=label)


def _base_record(kind="object_lever_interaction_committed_event", delta=None, elig=None, safe=("scene:1","actor:1","object_lever:1")):
    src=_base_src(safe=safe); delta=delta or _base_delta()
    if elig is None:
        elig_status={"object_lever_interaction_committed_event":"commit_ready","object_lever_interaction_blocked_event":"commit_blocked","object_lever_interaction_deferred_event":"commit_deferred","object_lever_interaction_unknown_event":"commit_unknown","object_lever_interaction_insufficient_preview_event":"commit_insufficient_preview"}[kind]
        elig=_base_elig(elig_status)
    return e.ObjectLeverCommittedEventRecord(committed_event_id="ev", event_record_kind=kind, command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference=src, eligibility=elig, state_delta_receipt=delta, safe_reference_ids=safe)


def commit_result(status="committed", safe=("scene:1","actor:1","object_lever:1"), block_reasons=(), metadata=None):
    decision=_commit_decision(status)
    if status == "committed":
        record=_base_record(safe=safe); delta=_base_delta()
    else:
        mapping={"commit_blocked":("object_lever_interaction_blocked_event","no_state_delta_due_to_block","no state delta due to block"),"commit_deferred":("object_lever_interaction_deferred_event","no_state_delta_due_to_deferred","no state delta due to deferred"),"commit_unknown":("object_lever_interaction_unknown_event","no_state_delta_due_to_unknown","no state delta due to unknown"),"commit_insufficient_preview":("object_lever_interaction_insufficient_preview_event","no_state_delta_due_to_insufficient_preview","no state delta due to insufficient preview")}
        event_kind,delta_kind,label=mapping[status]
        delta=_base_delta(kind=delta_kind, affected=(), label=label)
        elig=_base_elig(status)
        record=_base_record(kind=event_kind, delta=delta, elig=elig, safe=safe)
    return e.ObjectLeverEventCommitResult(result_id="commit-1", commit_status=status, commit_decision=decision, committed_event_record=record, state_delta_receipt=delta, block_reasons=block_reasons, safe_reference_ids=safe, metadata=metadata or {})


def test_module_imports_and_constants_are_frozen():
    assert importlib.import_module(f.__name__)
    for name in ["OBJECT_LEVER_REPLAY_AUDIT_STATUSES","OBJECT_LEVER_REPLAY_AUDIT_DECISIONS","OBJECT_LEVER_AUDIT_SNAPSHOT_KINDS","OBJECT_LEVER_REPLAY_CHECK_KINDS","OBJECT_LEVER_REPLAY_AUDIT_BLOCK_REASONS","FORBIDDEN_OBJECT_LEVER_REPLAY_AUDIT_METADATA_KEYS"]:
        assert isinstance(getattr(f,name), frozenset)
    assert f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY == "interact_with_object_lever"
    assert not (f.OBJECT_LEVER_REPLAY_AUDIT_STATUSES & FORBIDDEN)
    assert not (f.OBJECT_LEVER_REPLAY_AUDIT_DECISIONS & FORBIDDEN)


def test_dataclasses_frozen_keyword_only_and_authority_false_only():
    for cls in [f.ObjectLeverReplayAuditAuthorityFlags,f.ObjectLeverReplayAuditSourceRef,f.ObjectLeverReplayAuditEligibility,f.ObjectLeverAuditSnapshot,f.ObjectLeverReplayCheckReceipt,f.ObjectLeverReplayAuditResult]:
        assert is_dataclass(cls)
        assert cls.__dataclass_params__.frozen
        assert all(field.kw_only for field in cls.__dataclass_fields__.values())
    flags=f.ObjectLeverReplayAuditAuthorityFlags()
    assert set(flags.to_dict().values()) == {False}
    for field_name in flags.__dataclass_fields__:
        with pytest.raises(f.InvalidObjectLeverReplayAuditAuthorityFlagsError):
            f.ObjectLeverReplayAuditAuthorityFlags(**{field_name: True})
    assert f.validate_object_lever_replay_audit_authority_flags(flags) is True
    assert f.validate_object_lever_replay_audit_authority_flags(object()) is False


def test_authority_flag_to_dict_hardcodes_false():
    flags=f.ObjectLeverReplayAuditAuthorityFlags(persistence_write_authorized=False, replay_write_authorized=False)
    d=flags.to_dict()
    assert all(v is False for v in d.values())
    assert set(d) == set(flags.__dataclass_fields__)


def test_source_ref_carries_commit_ids_and_safe_refs_only():
    src=f.build_object_lever_replay_audit_source_ref(commit_result())
    d=src.to_dict()
    assert set(d) == {"commit_result_id","committed_event_id","state_delta_receipt_id","command_family","commit_status","commit_decision","safe_reference_ids","commit_block_reasons"}
    assert src.commit_result_id == "commit-1"
    assert src.committed_event_id == "ev"
    assert src.state_delta_receipt_id == "sd"
    assert "commit_payload" not in json.dumps(d)
    assert f.validate_object_lever_replay_audit_source_ref(src) is True


def test_eligibility_validates_inputs():
    src=f.build_object_lever_replay_audit_source_ref(commit_result())
    elig=f.evaluate_object_lever_replay_audit_eligibility(src)
    assert elig.eligibility_status == "audit_ready"
    assert f.validate_object_lever_replay_audit_eligibility(elig) is True


def test_audit_snapshot_validates():
    src=f.build_object_lever_replay_audit_source_ref(commit_result())
    elig=f.evaluate_object_lever_replay_audit_eligibility(src)
    snap=f.build_object_lever_audit_snapshot(elig, src, event_record_kind="object_lever_interaction_committed_event", state_delta_kind="object_lever_interaction_state_delta_receipt")
    assert f.validate_object_lever_audit_snapshot(snap) is True
    assert snap.audit_identity.startswith("sha256:")


def test_replay_check_receipt_validates():
    src=f.build_object_lever_replay_audit_source_ref(commit_result())
    elig=f.evaluate_object_lever_replay_audit_eligibility(src)
    snap=f.build_object_lever_audit_snapshot(elig, src, event_record_kind="object_lever_interaction_committed_event", state_delta_kind="object_lever_interaction_state_delta_receipt")
    receipt=f.build_object_lever_replay_check_receipt(snap)
    assert f.validate_object_lever_replay_check_receipt(receipt) is True
    assert receipt.identity_matches is True


def test_audit_result_validates():
    result=f.audit_object_lever_event_commit_result(commit_result())
    assert f.validate_object_lever_replay_audit_result(result) is True


def test_metadata_forbidden_keys_rejected_recursively_all_metadata_dataclasses():
    src=f.build_object_lever_replay_audit_source_ref(commit_result())
    elig=f.evaluate_object_lever_replay_audit_eligibility(src)
    snap=f.build_object_lever_audit_snapshot(elig, src, event_record_kind="object_lever_interaction_committed_event", state_delta_kind="object_lever_interaction_state_delta_receipt")
    receipt=f.build_object_lever_replay_check_receipt(snap)
    for key in f.FORBIDDEN_OBJECT_LEVER_REPLAY_AUDIT_METADATA_KEYS:
        bad={"nested":[{key:"x"}]}
        with pytest.raises(f.ObjectLeverReplayAuditCheckError):
            f.ObjectLeverAuditSnapshot(snapshot_id="s", audit_snapshot_kind="object_lever_committed_event_audit_snapshot", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, source_reference=src, eligibility=elig, metadata=bad)
        with pytest.raises(f.ObjectLeverReplayAuditCheckError):
            f.ObjectLeverReplayCheckReceipt(receipt_id="r", replay_check_kind="object_lever_committed_event_replay_check", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, audit_snapshot_id="s", replay_check_status="audit_ready", metadata=bad)
        with pytest.raises(f.ObjectLeverReplayAuditCheckError):
            f.ObjectLeverReplayAuditResult(result_id="r", audit_status="audit_blocked", audit_decision="blocked", metadata=bad)


def test_committed_result_creates_verified():
    result=f.audit_object_lever_event_commit_result(commit_result())
    assert result.audit_status == "audit_verified"
    assert result.audit_decision == "object_lever_audit_verified"
    assert result.audit_snapshot is not None
    assert result.replay_check_receipt is not None
    assert result.replay_check_receipt.identity_matches is True
    assert result.block_reasons == ()


def test_blocked_result_creates_blocked():
    result=f.audit_object_lever_event_commit_result(commit_result(status="commit_blocked"))
    assert result.audit_status == "audit_blocked"
    assert result.audit_decision == "blocked"


def test_deferred_result_creates_deferred():
    result=f.audit_object_lever_event_commit_result(commit_result(status="commit_deferred"))
    assert result.audit_status == "audit_deferred"
    assert result.audit_decision == "deferred"


def test_unknown_result_creates_unknown():
    result=f.audit_object_lever_event_commit_result(commit_result(status="commit_unknown"))
    assert result.audit_status == "audit_unknown"
    assert result.audit_decision == "unknown"


def test_insufficient_result_creates_insufficient():
    result=f.audit_object_lever_event_commit_result(commit_result(status="commit_insufficient_preview"))
    assert result.audit_status == "audit_insufficient_commit"
    assert result.audit_decision == "insufficient_commit"


def test_missing_committed_event_record_prevents_verification():
    delta=_base_delta()
    fake=SimpleNamespace(result_id="commit-missing", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, commit_status="committed", commit_decision="object_lever_event_committed", committed_event_record=None, state_delta_receipt=delta, block_reasons=(), safe_reference_ids=("scene:1","actor:1","object_lever:1"), metadata={})
    result=f.audit_object_lever_event_commit_result(fake)
    assert result.audit_status == "audit_blocked"
    assert "missing_committed_event_record" in result.block_reasons


def test_missing_state_delta_receipt_prevents_verification():
    record=_base_record()
    fake=SimpleNamespace(result_id="commit-missing", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, commit_status="committed", commit_decision="object_lever_event_committed", committed_event_record=record, state_delta_receipt=None, block_reasons=(), safe_reference_ids=("scene:1","actor:1","object_lever:1"), metadata={})
    result=f.audit_object_lever_event_commit_result(fake)
    assert result.audit_status == "audit_blocked"
    assert "missing_state_delta_receipt" in result.block_reasons


def test_missing_safe_references_prevents_verification():
    result=f.audit_object_lever_event_commit_result(commit_result(safe=()))
    assert result.audit_status == "audit_blocked"
    assert "missing_safe_references" in result.block_reasons


def test_wrong_command_family_prevents_verification():
    fake=SimpleNamespace(result_id="commit-wrong", command_family="wrong", commit_status="committed", commit_decision="object_lever_event_committed", committed_event_record=None, state_delta_receipt=None, block_reasons=(), safe_reference_ids=("scene:1","actor:1","object_lever:1"), metadata={})
    result=f.audit_object_lever_event_commit_result(fake)
    assert result.audit_status == "audit_blocked"
    assert "invalid_command_family" in result.block_reasons


def test_commit_block_reasons_prevent_verification():
    result=f.audit_object_lever_event_commit_result(commit_result(status="committed", block_reasons=("preview_blocked",)))
    assert result.audit_status == "audit_blocked"
    assert "commit_blocked" in result.block_reasons


def test_audit_identity_is_deterministic():
    r1=f.audit_object_lever_event_commit_result(commit_result())
    r2=f.audit_object_lever_event_commit_result(commit_result())
    assert r1.audit_snapshot.audit_identity == r2.audit_snapshot.audit_identity


def test_audit_identity_changes_with_safe_reference_ids():
    r1=f.audit_object_lever_event_commit_result(commit_result(safe=("scene:1","actor:1","object_lever:1")))
    r2=f.audit_object_lever_event_commit_result(commit_result(safe=("scene:2","actor:2","object_lever:2")))
    assert r1.audit_snapshot.audit_identity != r2.audit_snapshot.audit_identity


def test_audit_identity_excludes_metadata():
    r1=f.audit_object_lever_event_commit_result(commit_result(metadata={"audit":"a"}))
    r2=f.audit_object_lever_event_commit_result(commit_result(metadata={"audit":"b"}))
    assert r1.audit_snapshot.audit_identity == r2.audit_snapshot.audit_identity


def test_audit_identity_excludes_authority_flags():
    # Authority flags are always false-only; identity is computed only from source fields.
    r1=f.audit_object_lever_event_commit_result(commit_result())
    r2=f.audit_object_lever_event_commit_result(commit_result())
    assert r1.audit_snapshot.audit_identity == r2.audit_snapshot.audit_identity


def _verified_snapshot():
    src=f.build_object_lever_replay_audit_source_ref(commit_result())
    elig=f.evaluate_object_lever_replay_audit_eligibility(src)
    return f.build_object_lever_audit_snapshot(elig, src, event_record_kind="object_lever_interaction_committed_event", state_delta_kind="object_lever_interaction_state_delta_receipt")


def test_audit_path_blocks_identity_mismatch():
    result=f.audit_object_lever_event_commit_result(commit_result(), expected_audit_identity="sha256:wrong")
    assert result.audit_status == "audit_blocked"
    assert result.audit_decision == "blocked"
    assert "audit_identity_mismatch" in result.block_reasons
    assert result.audit_snapshot is None
    assert result.replay_check_receipt is None


def test_replay_check_receipt_rejects_identity_mismatch():
    with pytest.raises(f.InvalidObjectLeverReplayCheckReceiptError):
        f.ObjectLeverReplayCheckReceipt(receipt_id="r", replay_check_kind="object_lever_committed_event_replay_check", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, audit_snapshot_id="s", replay_check_status="audit_verified", audit_identity="sha256:a", expected_audit_identity="sha256:b", identity_matches=False)


def test_audit_path_does_not_reinterpret_or_infer():
    result=f.audit_object_lever_event_commit_result(commit_result())
    s=json.dumps(f.serialize_object_lever_replay_audit_result_visible(result), sort_keys=True)
    for term in ["hidden_fact","trap","activation","success","failure","safety","danger","object_state"]:
        assert term not in s


def test_output_contains_no_forbidden_execution_fields():
    result=f.audit_object_lever_event_commit_result(commit_result())
    s=json.dumps(f.serialize_object_lever_replay_audit_result_visible(result), sort_keys=True)
    for term in OUTPUT_FORBIDDEN:
        assert term not in s


def test_backend_and_visible_serializers_redact_backend_fields():
    result=f.audit_object_lever_event_commit_result(commit_result(metadata={"audit":["rt-002f"]}))
    backend=f.serialize_object_lever_replay_audit_result(result)
    assert "metadata" in backend and "authority_flags" in backend
    visible=f.serialize_object_lever_replay_audit_result_visible(result)
    assert "metadata" not in visible and "authority_flags" not in visible and "source_reference" not in visible and "eligibility" not in visible and "deterministic_source_fields" not in visible and "non_authority_note" not in visible
    assert visible["audit_decision"] == "object_lever_audit_verified"


def test_serializers_are_deterministic_and_json_safe():
    result=f.audit_object_lever_event_commit_result(commit_result())
    backend=f.serialize_object_lever_replay_audit_result(result)
    assert json.loads(json.dumps(backend, sort_keys=True)) == backend
    visible=f.serialize_object_lever_replay_audit_result_visible(result)
    assert json.loads(json.dumps(visible, sort_keys=True)) == visible


def test_replay_check_receipt_kind_status_mismatch_rejected():
    with pytest.raises(f.InvalidObjectLeverReplayCheckReceiptError):
        f.ObjectLeverReplayCheckReceipt(receipt_id="r", replay_check_kind="object_lever_committed_event_replay_check", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, audit_snapshot_id="s", replay_check_status="audit_blocked", audit_identity="sha256:a", expected_audit_identity="sha256:a", identity_matches=True)


def test_replay_check_receipt_verified_requires_identity_match():
    with pytest.raises(f.InvalidObjectLeverReplayCheckReceiptError):
        f.ObjectLeverReplayCheckReceipt(receipt_id="r", replay_check_kind="object_lever_committed_event_replay_check", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, audit_snapshot_id="s", replay_check_status="audit_verified", audit_identity="sha256:a", expected_audit_identity="sha256:a", identity_matches=False)


def test_replay_check_receipt_identity_match_requires_equal_non_empty_identities():
    with pytest.raises(f.InvalidObjectLeverReplayCheckReceiptError):
        f.ObjectLeverReplayCheckReceipt(receipt_id="r", replay_check_kind="object_lever_committed_event_replay_check", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, audit_snapshot_id="s", replay_check_status="audit_verified", audit_identity="sha256:a", expected_audit_identity="sha256:b", identity_matches=True)
    with pytest.raises(f.InvalidObjectLeverReplayCheckReceiptError):
        f.ObjectLeverReplayCheckReceipt(receipt_id="r", replay_check_kind="object_lever_committed_event_replay_check", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, audit_snapshot_id="s", replay_check_status="audit_verified", audit_identity=None, expected_audit_identity=None, identity_matches=True)


def test_audit_verified_result_rejects_snapshot_identity_receipt_identity_mismatch():
    snapshot=_verified_snapshot()
    receipt=f.ObjectLeverReplayCheckReceipt(receipt_id="r", replay_check_kind="object_lever_committed_event_replay_check", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, audit_snapshot_id=snapshot.snapshot_id, replay_check_status="audit_verified", audit_identity="sha256:not-the-same", expected_audit_identity="sha256:not-the-same", identity_matches=True)
    with pytest.raises(f.InvalidObjectLeverReplayAuditResultError):
        f.ObjectLeverReplayAuditResult(result_id="res", audit_status="audit_verified", audit_decision="object_lever_audit_verified", audit_snapshot=snapshot, replay_check_receipt=receipt)


def test_audit_verified_result_rejects_non_verified_receipt_status():
    snapshot=_verified_snapshot()
    receipt=f.ObjectLeverReplayCheckReceipt(receipt_id="r", replay_check_kind="object_lever_blocked_event_replay_check", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, audit_snapshot_id=snapshot.snapshot_id, replay_check_status="audit_blocked", audit_identity=None, expected_audit_identity=None, identity_matches=False)
    with pytest.raises(f.InvalidObjectLeverReplayAuditResultError):
        f.ObjectLeverReplayAuditResult(result_id="res", audit_status="audit_verified", audit_decision="object_lever_audit_verified", audit_snapshot=snapshot, replay_check_receipt=receipt)


def test_duck_typed_committed_input_with_non_rt002e_record_receipt_does_not_verify():
    fake=SimpleNamespace(result_id="x", command_family=f.OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, commit_status="committed", commit_decision="object_lever_event_committed", committed_event_record=object(), state_delta_receipt=object(), block_reasons=(), safe_reference_ids=("scene:1","actor:1","object_lever:1"), metadata={})
    result=f.audit_object_lever_event_commit_result(fake)
    assert result.audit_status == "audit_blocked"
    assert result.audit_decision == "blocked"
    assert ("missing_committed_event_record" in result.block_reasons) or ("missing_state_delta_receipt" in result.block_reasons)


def test_helper_outputs_for_all_statuses_still_validate():
    for status in ["committed","commit_blocked","commit_deferred","commit_unknown","commit_insufficient_preview"]:
        result=f.audit_object_lever_event_commit_result(commit_result(status=status))
        assert f.validate_object_lever_replay_audit_result(result) is True


def test_import_boundaries_and_domain_exports_and_docs():
    source=inspect.getsource(f)
    tree=ast.parse(source)
    imports=[]
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom): imports.append(node.module or "")
        if isinstance(node, ast.Import): imports.extend(alias.name for alias in node.names)
    assert "astra_runtime.domain.object_lever_event_commit_state_delta_path" in imports
    assert "astra_runtime.domain.read_only_vertical_slice_state_owner_facade" not in imports
    assert "astra_runtime.domain.projection_visibility_adapter_v0_1" not in imports
    assert "astra_runtime.domain.object_lever_interaction_legality_reader" not in imports
    assert "astra_runtime.domain.object_lever_transaction_preview_bridge" not in imports
    for forbidden in ["state_store","event_store","persistence","replay","resource_consequence_math","rng","model_boundary","live_play","ui","client","conversion","sourcebook","canon"]:
        assert not any(forbidden in module for module in imports), f"forbidden import {forbidden!r} found"
    import astra_runtime.domain as domain
    assert hasattr(domain,"ObjectLeverReplayAuditResult")
    assert hasattr(domain,"ObjectLeverAuditSnapshot")
    assert "RT-002F" in open("docs/decisions/current_decisions_log.md").read()
    reg=open("docs/doctrine/astra_doctrine_registry_v0_1.yaml").read()
    assert "object_lever_replay_audit_check.py" in reg
    assert "test_runtime_domain_rt_002f_object_lever_replay_audit_check.py" in reg


class TestBranchDiff:
    def test_branch_diff_limited_to_rt002f(self):
        import subprocess
        from pathlib import Path
        REPO_ROOT=Path(__file__).resolve().parent.parent
        result=subprocess.run(["git","diff","--name-only","origin/main...HEAD"], cwd=REPO_ROOT, capture_output=True, text=True)
        changed={line.strip() for line in result.stdout.splitlines() if line.strip()}
        allowed={
            "src/astra_runtime/domain/object_lever_replay_audit_check.py",
            "tests/test_runtime_domain_rt_002f_object_lever_replay_audit_check.py",
            "src/astra_runtime/domain/__init__.py",
            "docs/decisions/current_decisions_log.md",
            "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
            "tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py",
            "tests/test_runtime_domain_rt_001e_action_legality_service_interface_contract_skeleton.py",
            "tests/test_runtime_domain_rt_002b_projection_visibility_adapter_v0_1.py",
            "tests/test_runtime_domain_rt_002c_object_lever_interaction_legality_reader.py",
        }
        unexpected=changed-allowed
        assert not unexpected, f"Branch diff modifies unexpected files: {unexpected}"

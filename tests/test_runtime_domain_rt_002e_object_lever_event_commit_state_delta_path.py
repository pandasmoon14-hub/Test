from dataclasses import is_dataclass
import importlib, inspect, json, ast
import pytest

import astra_runtime.domain.object_lever_event_commit_state_delta_path as e
import astra_runtime.domain.object_lever_transaction_preview_bridge as b
from astra_runtime.domain.object_lever_interaction_legality_reader import create_object_lever_legality_reading, create_object_lever_legality_reader_result

FORBIDDEN={"rng_resolved","oracle_resolved","resource_settled","consequence_settled","damage_applied","condition_applied","persistent_write_complete","replay_indexed","narrated","model_generated","success","failure"}

def legality(decision="permitted_for_preview", status="legality_read_available", safe=("scene:1","actor:1","object_lever:1"), block_reasons=()):
    r=create_object_lever_legality_reading(reading_id="read-1", reader_status=status, legality_decision=decision, command_family=b.OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY, requirement_readings=(), block_reasons=block_reasons, safe_reference_ids=safe)
    return create_object_lever_legality_reader_result(result_id="res-1", reader_status=status, legality_decision=decision, legality_reading=r)

def preview(decision="permitted_for_preview", status="legality_read_available", safe=("scene:1","actor:1","object_lever:1"), block_reasons=()):
    return b.bridge_object_lever_legality_to_transaction_preview(legality(decision, status, safe, block_reasons), result_id="bridge-1", preview_candidate_id="pc-1")

def test_module_imports_and_constants_are_frozen():
    assert importlib.import_module(e.__name__)
    for name in ["OBJECT_LEVER_COMMIT_STATUSES","OBJECT_LEVER_COMMIT_DECISIONS","OBJECT_LEVER_EVENT_RECORD_KINDS","OBJECT_LEVER_STATE_DELTA_KINDS","OBJECT_LEVER_COMMIT_BLOCK_REASONS","FORBIDDEN_OBJECT_LEVER_COMMIT_METADATA_KEYS"]:
        assert isinstance(getattr(e,name), frozenset)
    assert e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY == "interact_with_object_lever"
    assert not (e.OBJECT_LEVER_COMMIT_STATUSES & FORBIDDEN)
    assert not (e.OBJECT_LEVER_COMMIT_DECISIONS & FORBIDDEN)

def test_dataclasses_frozen_keyword_only_and_authority_false_only():
    for cls in [e.ObjectLeverEventCommitAuthorityFlags,e.ObjectLeverCommitSourceRef,e.ObjectLeverCommitEligibility,e.ObjectLeverStateDeltaReceipt,e.ObjectLeverCommittedEventRecord,e.ObjectLeverEventCommitResult]:
        assert is_dataclass(cls)
        assert cls.__dataclass_params__.frozen
        assert all(f.kw_only for f in cls.__dataclass_fields__.values())
    flags=e.ObjectLeverEventCommitAuthorityFlags()
    assert set(flags.to_dict().values()) == {False}
    for f in flags.__dataclass_fields__:
        with pytest.raises(e.InvalidObjectLeverEventCommitAuthorityFlagsError):
            e.ObjectLeverEventCommitAuthorityFlags(**{f: True})
    assert e.validate_object_lever_event_commit_authority_flags(flags) is True
    assert e.validate_object_lever_event_commit_authority_flags(object()) is False

def test_source_ref_carries_rt002d_ids_and_safe_refs_only():
    src=e.build_object_lever_commit_source_ref(preview())
    d=src.to_dict(); assert set(d)=={"bridge_result_id","preview_candidate_id","command_family","bridge_decision","bridge_status","safe_reference_ids","bridge_block_reasons"}
    assert "legality_result_id" not in d and "preview_payload" not in json.dumps(d)
    assert src.bridge_result_id == "bridge-1" and src.preview_candidate_id == "pc-1"
    assert e.validate_object_lever_commit_source_ref(src) is True

def test_eligibility_validates_inputs():
    src=e.build_object_lever_commit_source_ref(preview())
    elig=e.evaluate_object_lever_commit_eligibility(src)
    assert elig.eligibility_status == "commit_ready"
    assert elig.block_reasons == ()
    assert e.validate_object_lever_commit_eligibility(elig) is True

def test_state_delta_receipt_and_committed_event_record_validators():
    result=e.commit_object_lever_preview_to_event_and_state_delta(preview())
    assert e.validate_object_lever_state_delta_receipt(result.state_delta_receipt) is True
    assert e.validate_object_lever_committed_event_record(result.committed_event_record) is True
    assert e.validate_object_lever_event_commit_result(result) is True

def test_commit_prepared_preview_creates_committed():
    result=e.commit_object_lever_preview_to_event_and_state_delta(preview(), result_id="commit-1", committed_event_id="ev-1", state_delta_receipt_id="sd-1", metadata={"audit":["rt-002e"]})
    assert result.commit_status == "committed"
    assert result.commit_decision == "object_lever_event_committed"
    assert result.committed_event_record.event_record_kind == "object_lever_interaction_committed_event"
    assert result.state_delta_receipt.state_delta_kind == "object_lever_interaction_state_delta_receipt"
    assert result.state_delta_receipt.state_delta_label == "object_lever_interaction_recorded"
    assert result.state_delta_receipt.source_reference_ids["bridge_result_id"] == "bridge-1"
    assert result.state_delta_receipt.source_reference_ids["preview_candidate_id"] == "pc-1"
    backend=e.serialize_object_lever_event_commit_result(result)
    assert json.loads(json.dumps(backend, sort_keys=True)) == backend
    visible=e.serialize_object_lever_event_commit_result_visible(result)
    assert json.loads(json.dumps(visible, sort_keys=True)) == visible
    assert "metadata" not in visible and "authority_flags" not in visible

def test_blocked_deferred_unknown_insufficient_previews():
    cases=[("blocked","legality_read_available","commit_blocked","blocked"),("deferred","deferred","commit_deferred","deferred"),("unknown","unknown","commit_unknown","unknown"),("insufficient_projection","insufficient_projection","commit_insufficient_preview","insufficient_preview")]
    for decision,status,commit_status,commit_decision in cases:
        result=e.commit_object_lever_preview_to_event_and_state_delta(preview(decision,status))
        assert (result.commit_status,result.commit_decision)==(commit_status,commit_decision)
        assert result.committed_event_record is not None
        assert result.state_delta_receipt is not None

def test_missing_preview_candidate_prevents_commit():
    bad=b.ObjectLeverTransactionPreviewBridgeResult(result_id="bridge-bad", bridge_status="preview_bridge_available", bridge_decision="preview_candidate_prepared", preview_candidate=None)
    result=e.commit_object_lever_preview_to_event_and_state_delta(bad)
    assert result.commit_decision == "blocked"
    assert "missing_preview_candidate" in result.block_reasons

def test_missing_safe_references_prevents_commit():
    result=e.commit_object_lever_preview_to_event_and_state_delta(preview(safe=()))
    assert result.commit_decision == "blocked"
    assert "missing_safe_references" in result.block_reasons
    result2=e.commit_object_lever_preview_to_event_and_state_delta(preview(safe=("scene:1","actor:1")))
    assert result2.commit_decision == "blocked"
    assert "missing_safe_references" in result2.block_reasons

def test_wrong_command_family_prevents_commit():
    with pytest.raises(e.InvalidObjectLeverCommitSourceRefError):
        e.ObjectLeverCommitSourceRef(bridge_result_id="r", preview_candidate_id="p", command_family="wrong", bridge_decision="preview_candidate_prepared", bridge_status="preview_bridge_available", safe_reference_ids=("scene:1","actor:1","object_lever:1"))

def test_metadata_forbidden_keys_rejected_recursively_all_metadata_dataclasses():
    src=e.build_object_lever_commit_source_ref(preview())
    elig=e.evaluate_object_lever_commit_eligibility(src)
    delta=e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="object_lever_interaction_state_delta_receipt", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"b","preview_candidate_id":"p"}, affected_safe_reference_ids=("scene:1","actor:1","object_lever:1"))
    for key in e.FORBIDDEN_OBJECT_LEVER_COMMIT_METADATA_KEYS:
        bad={"nested":[{key:"x"}]}
        with pytest.raises(e.ObjectLeverEventCommitStateDeltaPathError):
            e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="object_lever_interaction_state_delta_receipt", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"b","preview_candidate_id":"p"}, metadata=bad)
        with pytest.raises(e.ObjectLeverEventCommitStateDeltaPathError):
            e.ObjectLeverCommittedEventRecord(committed_event_id="ev", event_record_kind="object_lever_interaction_committed_event", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference=src, eligibility=elig, state_delta_receipt=delta, metadata=bad)
        with pytest.raises(e.ObjectLeverEventCommitStateDeltaPathError):
            e.ObjectLeverEventCommitResult(result_id="r", commit_status="committed", commit_decision="object_lever_event_committed", committed_event_record=None, state_delta_receipt=None, metadata=bad)

def test_commit_path_does_not_reinterpret_or_infer():
    result=e.commit_object_lever_preview_to_event_and_state_delta(preview())
    s=json.dumps(e.serialize_object_lever_event_commit_result_visible(result), sort_keys=True)
    for term in ["hidden_fact","trap","activation","success","failure","safety","danger","object_state"]:
        assert term not in s

def test_output_contains_no_forbidden_execution_fields():
    result=e.commit_object_lever_preview_to_event_and_state_delta(preview())
    s=json.dumps(e.serialize_object_lever_event_commit_result_visible(result), sort_keys=True)
    for term in ["event_store_append","event_append","event_payload","persistence_write","replay_write","rng_result","oracle_result","resource_settlement","consequence_application","damage_application","condition_application","model_prompt","arbitrary_mutation","state_before","state_after","raw_state"]:
        assert term not in s

def test_backend_and_visible_serializers_redact_backend_fields():
    result=e.commit_object_lever_preview_to_event_and_state_delta(preview(), metadata={"audit":["rt-002e"]})
    backend=e.serialize_object_lever_event_commit_result(result)
    assert "metadata" in backend and "authority_flags" in backend
    visible=e.serialize_object_lever_event_commit_result_visible(result)
    assert "metadata" not in visible and "authority_flags" not in visible and "source_reference" not in visible
    assert visible["commit_decision"] == "object_lever_event_committed"

def test_import_boundaries_and_domain_exports_and_docs():
    source=inspect.getsource(e)
    tree=ast.parse(source)
    imports=[]
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom): imports.append(node.module or "")
        if isinstance(node, ast.Import): imports.extend(alias.name for alias in node.names)
    assert "astra_runtime.domain.object_lever_transaction_preview_bridge" in imports
    assert "astra_runtime.domain.read_only_vertical_slice_state_owner_facade" not in imports
    assert "astra_runtime.domain.projection_visibility_adapter_v0_1" not in imports
    assert "astra_runtime.domain.object_lever_interaction_legality_reader" not in imports
    for forbidden in ["state_store","persistence","resource_consequence_math","rng","model_boundary","live_play","ui","client","conversion","sourcebook","canon"]:
        assert not any(forbidden in module for module in imports)
    import astra_runtime.domain as domain
    assert hasattr(domain,"ObjectLeverEventCommitResult")
    assert "RT-002E" in open("docs/decisions/current_decisions_log.md").read()
    reg=open("docs/doctrine/astra_doctrine_registry_v0_1.yaml").read()
    assert "object_lever_event_commit_state_delta_path.py" in reg
    assert "test_runtime_domain_rt_002e_object_lever_event_commit_state_delta_path.py" in reg


def _base_src():
    return e.ObjectLeverCommitSourceRef(bridge_result_id="br", preview_candidate_id="pc", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, bridge_decision="preview_candidate_prepared", bridge_status="preview_bridge_available", safe_reference_ids=("scene:1","actor:1","object_lever:1"))

def _base_elig(status="commit_ready"):
    return e.ObjectLeverCommitEligibility(command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, eligibility_status=status, bridge_decision="preview_candidate_prepared", bridge_status="preview_bridge_available", safe_reference_ids=("scene:1","actor:1","object_lever:1"))

def _base_delta(kind="object_lever_interaction_state_delta_receipt", affected=("scene:1","actor:1","object_lever:1"), label="object_lever_interaction_recorded"):
    return e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind=kind, command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br","preview_candidate_id":"pc"}, affected_safe_reference_ids=affected, state_delta_label=label)

def _base_record(kind="object_lever_interaction_committed_event", delta=None, elig=None):
    src=_base_src(); delta=delta or _base_delta()
    if elig is None:
        elig_status={"object_lever_interaction_committed_event":"commit_ready","object_lever_interaction_blocked_event":"commit_blocked","object_lever_interaction_deferred_event":"commit_deferred","object_lever_interaction_unknown_event":"commit_unknown","object_lever_interaction_insufficient_preview_event":"commit_insufficient_preview"}[kind]
        elig=_base_elig(elig_status)
    return e.ObjectLeverCommittedEventRecord(committed_event_id="ev", event_record_kind=kind, command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference=src, eligibility=elig, state_delta_receipt=delta, safe_reference_ids=("scene:1","actor:1","object_lever:1"))

def test_eligibility_rejects_committed_status():
    with pytest.raises(e.InvalidObjectLeverCommitEligibilityError):
        e.ObjectLeverCommitEligibility(command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, eligibility_status="committed", bridge_decision="preview_candidate_prepared", bridge_status="preview_bridge_available")

def test_state_delta_receipt_coherence_rejected():
    with pytest.raises(e.InvalidObjectLeverStateDeltaReceiptError):
        e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="object_lever_interaction_state_delta_receipt", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br","preview_candidate_id":"pc"}, affected_safe_reference_ids=())
    with pytest.raises(e.InvalidObjectLeverStateDeltaReceiptError):
        e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="object_lever_interaction_state_delta_receipt", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br","preview_candidate_id":"pc"}, affected_safe_reference_ids=("scene:1",), state_delta_label="wrong")
    with pytest.raises(e.InvalidObjectLeverStateDeltaReceiptError):
        e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="no_state_delta_due_to_block", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br","preview_candidate_id":"pc"}, affected_safe_reference_ids=("scene:1",))
    with pytest.raises(e.InvalidObjectLeverStateDeltaReceiptError):
        e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="no_state_delta_due_to_block", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br","preview_candidate_id":"pc"}, affected_safe_reference_ids=(), state_delta_label="object_lever_interaction_recorded")

def test_committed_event_record_coherence_rejected():
    delta_block=e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="no_state_delta_due_to_block", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br","preview_candidate_id":"pc"}, affected_safe_reference_ids=(), state_delta_label="no state delta due to block")
    with pytest.raises(e.InvalidObjectLeverCommittedEventRecordError):
        _base_record(kind="object_lever_interaction_committed_event", delta=delta_block)
    with pytest.raises(e.InvalidObjectLeverCommittedEventRecordError):
        _base_record(kind="object_lever_interaction_blocked_event", delta=_base_delta())

def test_commit_result_coherence_rejected():
    record=_base_record(); delta=_base_delta()
    with pytest.raises(e.InvalidObjectLeverEventCommitResultError):
        e.ObjectLeverEventCommitResult(result_id="r", commit_status="committed", commit_decision="blocked", committed_event_record=record, state_delta_receipt=delta)
    with pytest.raises(e.InvalidObjectLeverEventCommitResultError):
        e.ObjectLeverEventCommitResult(result_id="r", commit_status="committed", commit_decision="object_lever_event_committed", committed_event_record=None, state_delta_receipt=delta)
    with pytest.raises(e.InvalidObjectLeverEventCommitResultError):
        e.ObjectLeverEventCommitResult(result_id="r", commit_status="committed", commit_decision="object_lever_event_committed", committed_event_record=record, state_delta_receipt=None)
    with pytest.raises(e.InvalidObjectLeverEventCommitResultError):
        e.ObjectLeverEventCommitResult(result_id="r", commit_status="commit_blocked", commit_decision="object_lever_event_committed")
    with pytest.raises(e.InvalidObjectLeverEventCommitResultError):
        e.ObjectLeverEventCommitResult(result_id="r", commit_status="commit_blocked", commit_decision="deferred")
    block_record=_base_record(kind="object_lever_interaction_blocked_event", delta=e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="no_state_delta_due_to_block", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br","preview_candidate_id":"pc"}, affected_safe_reference_ids=(), state_delta_label="no state delta due to block"))
    with pytest.raises(e.InvalidObjectLeverEventCommitResultError):
        e.ObjectLeverEventCommitResult(result_id="r", commit_status="commit_blocked", commit_decision="blocked", committed_event_record=record, state_delta_receipt=delta)
    with pytest.raises(e.InvalidObjectLeverEventCommitResultError):
        e.ObjectLeverEventCommitResult(result_id="r", commit_status="commit_blocked", commit_decision="blocked", committed_event_record=block_record, state_delta_receipt=delta)

def test_commit_result_valid_variants():
    record=_base_record(); delta=_base_delta()
    assert e.validate_object_lever_event_commit_result(e.ObjectLeverEventCommitResult(result_id="r", commit_status="committed", commit_decision="object_lever_event_committed", committed_event_record=record, state_delta_receipt=delta)) is True


def test_event_record_eligibility_coherence_rejected():
    src=e.ObjectLeverCommitSourceRef(bridge_result_id="br", preview_candidate_id="pc", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, bridge_decision="blocked", bridge_status="preview_bridge_blocked")
    ready_elig=e.ObjectLeverCommitEligibility(command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, eligibility_status="commit_ready", bridge_decision="blocked", bridge_status="preview_bridge_blocked")
    block_elig=e.ObjectLeverCommitEligibility(command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, eligibility_status="commit_blocked", bridge_decision="blocked", bridge_status="preview_bridge_blocked")
    block_delta=e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="no_state_delta_due_to_block", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br"}, affected_safe_reference_ids=(), state_delta_label="no state delta due to block")
    with pytest.raises(e.InvalidObjectLeverCommittedEventRecordError):
        e.ObjectLeverCommittedEventRecord(committed_event_id="ev", event_record_kind="object_lever_interaction_blocked_event", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference=src, eligibility=ready_elig, state_delta_receipt=block_delta)
    deferred_elig=e.ObjectLeverCommitEligibility(command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, eligibility_status="commit_ready", bridge_decision="deferred", bridge_status="preview_bridge_deferred")
    deferred_delta=e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="no_state_delta_due_to_deferred", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br"}, affected_safe_reference_ids=(), state_delta_label="no state delta due to deferred")
    with pytest.raises(e.InvalidObjectLeverCommittedEventRecordError):
        e.ObjectLeverCommittedEventRecord(committed_event_id="ev", event_record_kind="object_lever_interaction_deferred_event", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference=src, eligibility=deferred_elig, state_delta_receipt=deferred_delta)
    committed_src=e.ObjectLeverCommitSourceRef(bridge_result_id="br", preview_candidate_id="pc", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, bridge_decision="preview_candidate_prepared", bridge_status="preview_bridge_available", safe_reference_ids=("scene:1","actor:1","object_lever:1"))
    committed_delta=e.ObjectLeverStateDeltaReceipt(state_delta_receipt_id="sd", state_delta_kind="object_lever_interaction_state_delta_receipt", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference_ids={"bridge_result_id":"br","preview_candidate_id":"pc"}, affected_safe_reference_ids=("scene:1","actor:1","object_lever:1"), state_delta_label="object_lever_interaction_recorded")
    with pytest.raises(e.InvalidObjectLeverCommittedEventRecordError):
        e.ObjectLeverCommittedEventRecord(committed_event_id="ev", event_record_kind="object_lever_interaction_committed_event", command_family=e.OBJECT_LEVER_COMMIT_COMMAND_FAMILY, source_reference=committed_src, eligibility=block_elig, state_delta_receipt=committed_delta)

def test_helper_outputs_remain_valid():
    for decision,status,expected_status,expected_decision in [("permitted_for_preview","legality_read_available","committed","object_lever_event_committed"),("blocked","legality_read_available","commit_blocked","blocked"),("deferred","deferred","commit_deferred","deferred"),("unknown","unknown","commit_unknown","unknown"),("insufficient_projection","insufficient_projection","commit_insufficient_preview","insufficient_preview")]:
        result=e.commit_object_lever_preview_to_event_and_state_delta(preview(decision,status))
        assert result.commit_status == expected_status
        assert result.commit_decision == expected_decision
        assert e.validate_object_lever_event_commit_result(result) is True
        if expected_status == "committed":
            assert result.committed_event_record.eligibility.eligibility_status == "commit_ready"
        else:
            assert result.committed_event_record.eligibility.eligibility_status == expected_status

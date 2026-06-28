from dataclasses import is_dataclass
import importlib, inspect, json, ast
import pytest

import astra_runtime.domain.object_lever_transaction_preview_bridge as b
from astra_runtime.domain.object_lever_interaction_legality_reader import create_object_lever_legality_reading, create_object_lever_legality_reader_result

FORBIDDEN={"executed","resolved","committed","mutated","applied","settled","event_appended","event_committed","state_delta_applied","persistence_written","success","failure"}

def legality(decision="permitted_for_preview", status="legality_read_available", safe=("scene:1","actor:1","object_lever:1"), block_reasons=()):
    r=create_object_lever_legality_reading(reading_id="read-1", reader_status=status, legality_decision=decision, command_family=b.OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY, requirement_readings=(), block_reasons=block_reasons, safe_reference_ids=safe)
    return create_object_lever_legality_reader_result(result_id="res-1", reader_status=status, legality_decision=decision, legality_reading=r)

def test_module_imports_and_constants_are_frozen():
    assert importlib.import_module(b.__name__)
    for name in ["OBJECT_LEVER_PREVIEW_BRIDGE_STATUSES","OBJECT_LEVER_PREVIEW_BRIDGE_DECISIONS","OBJECT_LEVER_PREVIEW_CANDIDATE_KINDS","OBJECT_LEVER_PREVIEW_ELIGIBILITY_STATUSES","OBJECT_LEVER_PREVIEW_BLOCK_REASONS","FORBIDDEN_OBJECT_LEVER_PREVIEW_METADATA_KEYS"]:
        assert isinstance(getattr(b,name), frozenset)
    assert b.OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY == "interact_with_object_lever"
    assert not (b.OBJECT_LEVER_PREVIEW_BRIDGE_STATUSES & FORBIDDEN)
    assert not (b.OBJECT_LEVER_PREVIEW_BRIDGE_DECISIONS & FORBIDDEN)

def test_dataclasses_frozen_keyword_only_and_authority_false_only():
    for cls in [b.ObjectLeverTransactionPreviewBridgeAuthorityFlags,b.ObjectLeverPreviewBridgeSourceRef,b.ObjectLeverPreviewEligibility,b.ObjectLeverTransactionPreviewCandidate,b.ObjectLeverTransactionPreviewBridgeResult]:
        assert is_dataclass(cls)
        assert cls.__dataclass_params__.frozen
        assert all(f.kw_only for f in cls.__dataclass_fields__.values())
    flags=b.ObjectLeverTransactionPreviewBridgeAuthorityFlags()
    assert set(flags.to_dict().values()) == {False}
    for f in flags.__dataclass_fields__:
        with pytest.raises(b.InvalidObjectLeverTransactionPreviewBridgeAuthorityFlagsError):
            b.ObjectLeverTransactionPreviewBridgeAuthorityFlags(**{f: True})
    assert b.validate_object_lever_transaction_preview_bridge_authority_flags(flags) is True
    assert b.validate_object_lever_transaction_preview_bridge_authority_flags(object()) is False

def test_source_ref_and_eligibility_contain_ids_only():
    src=b.build_object_lever_preview_bridge_source_ref(legality())
    d=src.to_dict(); assert set(d)=={"legality_result_id","legality_reading_id","command_family","legality_decision","reader_status","safe_reference_ids","legality_block_reasons"}
    assert "legality_reading" not in d and "projection_payload" not in json.dumps(d)
    e=b.evaluate_object_lever_preview_eligibility(src)
    assert e.eligibility_status == "eligible_for_preview"
    assert e.block_reasons == ()
    assert b.validate_object_lever_preview_bridge_source_ref(src) is True
    assert b.validate_object_lever_preview_eligibility(e) is True

def test_bridge_permitted_prepares_candidate_and_is_json_safe():
    result=b.bridge_object_lever_legality_to_transaction_preview(legality(), metadata={"audit":["rt-002d"]})
    assert result.bridge_status == "preview_bridge_available"
    assert result.bridge_decision == "preview_candidate_prepared"
    assert result.preview_candidate.preview_candidate_kind == "object_lever_interaction_preview_candidate"
    backend=b.serialize_object_lever_transaction_preview_bridge_result(result)
    assert json.loads(json.dumps(backend, sort_keys=True)) == backend
    visible=b.serialize_object_lever_transaction_preview_bridge_result_visible(result)
    assert json.loads(json.dumps(visible, sort_keys=True)) == visible
    assert "metadata" not in visible and "authority_flags" not in visible

def test_blocked_deferred_unknown_insufficient_and_missing_refs():
    cases=[("blocked","legality_read_available","preview_bridge_blocked","blocked"),("deferred","deferred","preview_bridge_deferred","deferred"),("unknown","unknown","preview_bridge_unknown","unknown"),("insufficient_projection","insufficient_projection","preview_bridge_insufficient_legality","insufficient_legality")]
    for decision,status,bridge_status,bridge_decision in cases:
        result=b.bridge_object_lever_legality_to_transaction_preview(legality(decision,status))
        assert (result.bridge_status,result.bridge_decision)==(bridge_status,bridge_decision)
    missing=b.bridge_object_lever_legality_to_transaction_preview(legality(safe=()))
    assert missing.bridge_decision == "blocked"
    assert "missing_safe_references" in missing.preview_candidate.eligibility.block_reasons

    one_ref=b.bridge_object_lever_legality_to_transaction_preview(legality(safe=("scene:1",)))
    assert one_ref.bridge_decision == "blocked"
    assert "missing_safe_references" in one_ref.preview_candidate.eligibility.block_reasons

    two_refs=b.bridge_object_lever_legality_to_transaction_preview(legality(safe=("scene:1","actor:1")))
    assert two_refs.bridge_decision == "blocked"
    assert "missing_safe_references" in two_refs.preview_candidate.eligibility.block_reasons

    three_refs=b.bridge_object_lever_legality_to_transaction_preview(legality(safe=("scene_1","actor_1","object_lever_1")))
    assert three_refs.bridge_decision == "preview_candidate_prepared"

def test_permitted_with_rt002c_block_reasons_is_not_prepared():
    result=b.bridge_object_lever_legality_to_transaction_preview(legality(block_reasons=("object_lever_owner_family_mismatch",)))
    assert result.bridge_decision == "blocked"
    assert result.bridge_status == "preview_bridge_blocked"
    assert "preview_not_constructible" in result.preview_candidate.eligibility.block_reasons

def test_wrong_command_family_source_ref_prevents_preparation():
    with pytest.raises(b.InvalidObjectLeverPreviewBridgeSourceRefError):
        b.ObjectLeverPreviewBridgeSourceRef(legality_result_id="r", legality_reading_id="read", command_family="wrong", legality_decision="permitted_for_preview", reader_status="legality_read_available", safe_reference_ids=("scene:1","actor:1","object_lever:1"))

def test_metadata_forbidden_keys_rejected_recursively_all_metadata_dataclasses():
    src=b.build_object_lever_preview_bridge_source_ref(legality())
    elig=b.evaluate_object_lever_preview_eligibility(src)
    for key in b.FORBIDDEN_OBJECT_LEVER_PREVIEW_METADATA_KEYS:
        bad={"nested":[{key:"x"}]}
        with pytest.raises(b.ObjectLeverTransactionPreviewBridgeError):
            b.ObjectLeverTransactionPreviewCandidate(preview_candidate_id="c", preview_candidate_kind="object_lever_interaction_preview_candidate", command_family=b.OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY, source_reference=src, eligibility=elig, safe_reference_ids=src.safe_reference_ids, metadata=bad)
        with pytest.raises(b.ObjectLeverTransactionPreviewBridgeError):
            b.ObjectLeverTransactionPreviewBridgeResult(result_id="r", bridge_status="preview_bridge_available", bridge_decision="preview_candidate_prepared", preview_candidate=None, metadata=bad)

def test_output_contains_no_forbidden_execution_fields_or_inferences():
    s=json.dumps(b.serialize_object_lever_transaction_preview_bridge_result_visible(b.bridge_object_lever_legality_to_transaction_preview(legality())), sort_keys=True)
    for term in ["command_execution","state_mutation","state_delta_application","event_append","event_commit","persistence_write","replay_write","rng_result","oracle_result","resource_settlement","consequence_application","model_prompt","success","failure","trap","activation"]:
        assert term not in s

def test_import_boundaries_and_domain_exports_and_docs():
    source=inspect.getsource(b)
    tree=ast.parse(source)
    imports=[]
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom): imports.append(node.module or "")
        if isinstance(node, ast.Import): imports.extend(alias.name for alias in node.names)
    assert "astra_runtime.domain.read_only_vertical_slice_state_owner_facade" not in imports
    assert "astra_runtime.domain.projection_visibility_adapter_v0_1" not in imports
    for forbidden in ["state_store","event_commitment","persistence","resource_consequence_math","rng","model_boundary","live_play","ui","client","conversion","sourcebook","canon"]:
        assert not any(forbidden in module for module in imports)
    import astra_runtime.domain as domain
    assert hasattr(domain,"ObjectLeverTransactionPreviewBridgeResult")
    assert "RT-002D" in open("docs/decisions/current_decisions_log.md").read()
    reg=open("docs/doctrine/astra_doctrine_registry_v0_1.yaml").read()
    assert "object_lever_transaction_preview_bridge.py" in reg
    assert "test_runtime_domain_rt_002d_object_lever_transaction_preview_bridge.py" in reg

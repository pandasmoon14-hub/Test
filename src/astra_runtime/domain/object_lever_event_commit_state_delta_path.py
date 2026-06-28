"""Object/Lever Event Commit and State Delta Path — RT-002E.

Narrow event/state-delta commit path for command family
``interact_with_object_lever``. Consumes RT-002D preview bridge results and
produces a controlled committed event record and a bounded state-delta commit
receipt only when an approved RT-002D preview candidate is available. This
module does not execute commands, mutate state in a general way, append to an
event store, persist or replay, run RNG or oracles, settle
resources/consequences, call models, narrate, or expose hidden truth.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.domain.object_lever_transaction_preview_bridge import (
    OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY,
    OBJECT_LEVER_PREVIEW_BRIDGE_DECISIONS,
    OBJECT_LEVER_PREVIEW_BRIDGE_STATUSES,
    ObjectLeverPreviewBridgeSourceRef,
    ObjectLeverTransactionPreviewBridgeResult,
    ObjectLeverTransactionPreviewCandidate,
)

__all__ = [
    "OBJECT_LEVER_COMMIT_COMMAND_FAMILY",
    "OBJECT_LEVER_COMMIT_STATUSES",
    "OBJECT_LEVER_COMMIT_ELIGIBILITY_STATUSES",
    "OBJECT_LEVER_COMMIT_DECISIONS",
    "OBJECT_LEVER_EVENT_RECORD_KINDS",
    "OBJECT_LEVER_STATE_DELTA_KINDS",
    "OBJECT_LEVER_COMMIT_BLOCK_REASONS",
    "OBJECT_LEVER_COMMIT_NON_AUTHORITY_NOTE",
    "FORBIDDEN_OBJECT_LEVER_COMMIT_METADATA_KEYS",
    "ObjectLeverEventCommitStateDeltaPathError",
    "InvalidObjectLeverEventCommitAuthorityFlagsError",
    "InvalidObjectLeverCommitSourceRefError",
    "InvalidObjectLeverCommitEligibilityError",
    "InvalidObjectLeverStateDeltaReceiptError",
    "InvalidObjectLeverCommittedEventRecordError",
    "InvalidObjectLeverEventCommitResultError",
    "ObjectLeverEventCommitAuthorityFlags",
    "ObjectLeverCommitSourceRef",
    "ObjectLeverCommitEligibility",
    "ObjectLeverStateDeltaReceipt",
    "ObjectLeverCommittedEventRecord",
    "ObjectLeverEventCommitResult",
    "create_object_lever_event_commit_authority_flags",
    "create_object_lever_commit_source_ref",
    "create_object_lever_commit_eligibility",
    "create_object_lever_state_delta_receipt",
    "create_object_lever_committed_event_record",
    "create_object_lever_event_commit_result",
    "build_object_lever_commit_source_ref",
    "evaluate_object_lever_commit_eligibility",
    "commit_object_lever_preview_to_event_and_state_delta",
    "serialize_object_lever_state_delta_receipt",
    "serialize_object_lever_state_delta_receipt_visible",
    "serialize_object_lever_committed_event_record",
    "serialize_object_lever_committed_event_record_visible",
    "serialize_object_lever_event_commit_result",
    "serialize_object_lever_event_commit_result_visible",
    "validate_object_lever_event_commit_authority_flags",
    "validate_object_lever_commit_source_ref",
    "validate_object_lever_commit_eligibility",
    "validate_object_lever_state_delta_receipt",
    "validate_object_lever_committed_event_record",
    "validate_object_lever_event_commit_result",
]

OBJECT_LEVER_COMMIT_COMMAND_FAMILY = OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY
OBJECT_LEVER_COMMIT_STATUSES = frozenset({"commit_ready", "commit_blocked", "commit_deferred", "commit_unknown", "commit_insufficient_preview", "committed"})
OBJECT_LEVER_COMMIT_ELIGIBILITY_STATUSES = frozenset({"commit_ready", "commit_blocked", "commit_deferred", "commit_unknown", "commit_insufficient_preview"})
OBJECT_LEVER_COMMIT_DECISIONS = frozenset({"object_lever_event_committed", "blocked", "deferred", "unknown", "insufficient_preview"})
_COMMIT_STATUS_TO_DECISION = {"committed":"object_lever_event_committed","commit_blocked":"blocked","commit_deferred":"deferred","commit_unknown":"unknown","commit_insufficient_preview":"insufficient_preview"}
_EVENT_KIND_TO_STATUS = {"object_lever_interaction_committed_event":"committed","object_lever_interaction_blocked_event":"commit_blocked","object_lever_interaction_deferred_event":"commit_deferred","object_lever_interaction_unknown_event":"commit_unknown","object_lever_interaction_insufficient_preview_event":"commit_insufficient_preview"}
_DELTA_KIND_TO_STATUS = {"object_lever_interaction_state_delta_receipt":"committed","no_state_delta_due_to_block":"commit_blocked","no_state_delta_due_to_deferred":"commit_deferred","no_state_delta_due_to_unknown":"commit_unknown","no_state_delta_due_to_insufficient_preview":"commit_insufficient_preview"}
OBJECT_LEVER_EVENT_RECORD_KINDS = frozenset({"object_lever_interaction_committed_event", "object_lever_interaction_blocked_event", "object_lever_interaction_deferred_event", "object_lever_interaction_unknown_event", "object_lever_interaction_insufficient_preview_event"})
OBJECT_LEVER_STATE_DELTA_KINDS = frozenset({"object_lever_interaction_state_delta_receipt", "no_state_delta_due_to_block", "no_state_delta_due_to_deferred", "no_state_delta_due_to_unknown", "no_state_delta_due_to_insufficient_preview"})
OBJECT_LEVER_COMMIT_BLOCK_REASONS = frozenset({"preview_not_prepared", "preview_blocked", "preview_deferred", "preview_unknown", "preview_insufficient", "missing_preview_candidate", "invalid_command_family", "missing_safe_references", "hidden_information_not_available", "event_commit_not_constructible", "state_delta_not_constructible"})
OBJECT_LEVER_COMMIT_NON_AUTHORITY_NOTE = ("RT-002E produces only a narrow committed event record and bounded state-delta commit receipt for the object/lever interaction vertical slice; it authorizes no general command execution, general state mutation engine, general event engine, persistence/replay writes, RNG/table/oracle execution, resource/consequence settlement, combat/ability/skill/effect resolution, damage/condition application, inventory transfer, faction/social change, hidden fact resolution, model/narration/live-play/UI behavior, conversion, sourcebook inclusion, or canon promotion.")
FORBIDDEN_OBJECT_LEVER_COMMIT_METADATA_KEYS = frozenset({"hidden_fact", "hidden_facts", "secret", "secrets", "backend_only_fact", "backend_only_facts", "state_payload", "raw_state", "actual_state", "truth_payload", "projection_payload", "record_payload", "world_state", "legality_payload", "preview_payload", "transaction_execution", "command_execution", "execution_result", "arbitrary_mutation", "mutation_payload", "state_before", "state_after", "state_delta_payload", "event_store_append", "event_payload", "event_append", "event_commitment_payload", "persistence_write", "replay_write", "resource_settlement", "consequence_application", "damage_application", "condition_application", "rng_result", "oracle_result", "model_prompt", "narration"})

class ObjectLeverEventCommitStateDeltaPathError(ValueError): pass
class InvalidObjectLeverEventCommitAuthorityFlagsError(ObjectLeverEventCommitStateDeltaPathError): pass
class InvalidObjectLeverCommitSourceRefError(ObjectLeverEventCommitStateDeltaPathError): pass
class InvalidObjectLeverCommitEligibilityError(ObjectLeverEventCommitStateDeltaPathError): pass
class InvalidObjectLeverStateDeltaReceiptError(ObjectLeverEventCommitStateDeltaPathError): pass
class InvalidObjectLeverCommittedEventRecordError(ObjectLeverEventCommitStateDeltaPathError): pass
class InvalidObjectLeverEventCommitResultError(ObjectLeverEventCommitStateDeltaPathError): pass

def _nonempty(v: object, n: str, e: type[Exception]) -> str:
    if not isinstance(v, str) or not v: raise e(f"{n} must be a non-empty string")
    return v

def _tuple(v: Sequence[str] | None, n: str, e: type[Exception]) -> tuple[str, ...]:
    if v is None: return ()
    if isinstance(v, (str, bytes)) or not isinstance(v, Sequence): raise e(f"{n} must be a sequence")
    out=[]
    for i,x in enumerate(v):
        if not isinstance(x,str) or not x: raise e(f"{n}[{i}] must be a non-empty string")
        out.append(x)
    return tuple(out)

def _json(value: Any, path: str, e: type[Exception]) -> None:
    if value is None or isinstance(value,(str,int,float,bool)): return
    if isinstance(value,(list,tuple)):
        for i,x in enumerate(value): _json(x, f"{path}[{i}]", e)
        return
    if isinstance(value, Mapping):
        for k,x in value.items():
            if not isinstance(k,str): raise e(f"metadata key at {path} must be a string")
            _json(x, f"{path}.{k}", e)
        return
    raise e(f"metadata value at {path} is not JSON-safe")

def _no_forbidden(value: Any, path: str, e: type[Exception]) -> None:
    if isinstance(value, Mapping):
        for k,x in value.items():
            if not isinstance(k,str): raise e(f"metadata key at {path} must be a string")
            if k in FORBIDDEN_OBJECT_LEVER_COMMIT_METADATA_KEYS: raise e(f"metadata key {k!r} at {path} is forbidden")
            _no_forbidden(x, f"{path}.{k}", e)
    elif isinstance(value,(list,tuple)):
        for i,x in enumerate(value): _no_forbidden(x, f"{path}[{i}]", e)

def _meta(m: Mapping[str,Any] | None, e: type[Exception]) -> Mapping[str,Any]:
    if m is None: return MappingProxyType({})
    if not isinstance(m, Mapping): raise e("metadata must be a mapping")
    _no_forbidden(m,"metadata",e); _json(m,"metadata",e)
    return MappingProxyType(copy.deepcopy(dict(m)))

@dataclass(frozen=True, kw_only=True)
class ObjectLeverEventCommitAuthorityFlags:
    general_command_execution_authorized: bool=False; general_state_mutation_authorized: bool=False; general_event_engine_authorized: bool=False; persistence_write_authorized: bool=False; replay_write_authorized: bool=False; rng_execution_authorized: bool=False; table_oracle_execution_authorized: bool=False; resource_math_execution_authorized: bool=False; consequence_application_authorized: bool=False; damage_application_authorized: bool=False; condition_application_authorized: bool=False; combat_resolution_authorized: bool=False; model_call_authorized: bool=False; narration_generation_authorized: bool=False; live_play_authorized: bool=False; ui_authorized: bool=False; conversion_authorized: bool=False; canon_promotion_authorized: bool=False
    def __post_init__(self) -> None:
        for f in self.__dataclass_fields__:
            if getattr(self,f) is not False: raise InvalidObjectLeverEventCommitAuthorityFlagsError(f"authority flag {f!r} must be False")
    def to_dict(self) -> dict[str,Any]: return {f: False for f in self.__dataclass_fields__}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverCommitSourceRef:
    bridge_result_id: str; preview_candidate_id: str; command_family: str; bridge_decision: str; bridge_status: str; safe_reference_ids: tuple[str,...]=(); bridge_block_reasons: tuple[str,...]=()
    def __post_init__(self) -> None:
        e=InvalidObjectLeverCommitSourceRefError
        for n in ("bridge_result_id","command_family","bridge_decision","bridge_status"): _nonempty(getattr(self,n),n,e)
        if not isinstance(self.preview_candidate_id, str): raise e("preview_candidate_id must be a string")
        if self.command_family != OBJECT_LEVER_COMMIT_COMMAND_FAMILY: raise e("invalid command_family")
        if self.bridge_decision not in OBJECT_LEVER_PREVIEW_BRIDGE_DECISIONS: raise e("invalid bridge_decision")
        if self.bridge_status not in OBJECT_LEVER_PREVIEW_BRIDGE_STATUSES: raise e("invalid bridge_status")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
        object.__setattr__(self,"bridge_block_reasons",_tuple(self.bridge_block_reasons,"bridge_block_reasons",e))
    def to_dict(self)->dict[str,Any]: return {"bridge_result_id":self.bridge_result_id,"preview_candidate_id":self.preview_candidate_id,"command_family":self.command_family,"bridge_decision":self.bridge_decision,"bridge_status":self.bridge_status,"safe_reference_ids":list(self.safe_reference_ids),"bridge_block_reasons":list(self.bridge_block_reasons)}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverCommitEligibility:
    command_family: str; eligibility_status: str; bridge_decision: str; bridge_status: str; block_reasons: tuple[str,...]=(); safe_reference_ids: tuple[str,...]=()
    def __post_init__(self)->None:
        e=InvalidObjectLeverCommitEligibilityError
        if self.command_family != OBJECT_LEVER_COMMIT_COMMAND_FAMILY: raise e("invalid command_family")
        if self.eligibility_status not in OBJECT_LEVER_COMMIT_ELIGIBILITY_STATUSES: raise e("invalid eligibility_status")
        if self.bridge_decision not in OBJECT_LEVER_PREVIEW_BRIDGE_DECISIONS: raise e("invalid bridge_decision")
        if self.bridge_status not in OBJECT_LEVER_PREVIEW_BRIDGE_STATUSES: raise e("invalid bridge_status")
        object.__setattr__(self,"block_reasons",_tuple(self.block_reasons,"block_reasons",e))
        for r in self.block_reasons:
            if r not in OBJECT_LEVER_COMMIT_BLOCK_REASONS: raise e(f"invalid block_reason {r!r}")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
    def to_dict(self)->dict[str,Any]: return {"command_family":self.command_family,"eligibility_status":self.eligibility_status,"bridge_decision":self.bridge_decision,"bridge_status":self.bridge_status,"block_reasons":list(self.block_reasons),"safe_reference_ids":list(self.safe_reference_ids)}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverStateDeltaReceipt:
    state_delta_receipt_id: str; state_delta_kind: str; command_family: str; source_reference_ids: Mapping[str,str]; affected_safe_reference_ids: tuple[str,...]=(); state_delta_label: str="object_lever_interaction_recorded"; non_authority_note: str=OBJECT_LEVER_COMMIT_NON_AUTHORITY_NOTE; authority_flags: ObjectLeverEventCommitAuthorityFlags=field(default_factory=ObjectLeverEventCommitAuthorityFlags); metadata: Mapping[str,Any]=field(default_factory=lambda: MappingProxyType({}))
    def __post_init__(self)->None:
        e=InvalidObjectLeverStateDeltaReceiptError; _nonempty(self.state_delta_receipt_id,"state_delta_receipt_id",e)
        if self.state_delta_kind not in OBJECT_LEVER_STATE_DELTA_KINDS: raise e("invalid state_delta_kind")
        if self.command_family != OBJECT_LEVER_COMMIT_COMMAND_FAMILY: raise e("invalid command_family")
        if not isinstance(self.source_reference_ids, Mapping): raise e("source_reference_ids must be a mapping")
        for k,v in self.source_reference_ids.items():
            if not isinstance(k,str) or not k: raise e("source_reference_ids keys must be non-empty strings")
            if not isinstance(v,str) or not v: raise e("source_reference_ids values must be non-empty strings")
        object.__setattr__(self,"source_reference_ids",MappingProxyType(dict(self.source_reference_ids)))
        object.__setattr__(self,"affected_safe_reference_ids",_tuple(self.affected_safe_reference_ids,"affected_safe_reference_ids",e))
        _nonempty(self.state_delta_label,"state_delta_label",e)
        _nonempty(self.non_authority_note,"non_authority_note",e)
        if not isinstance(self.authority_flags,ObjectLeverEventCommitAuthorityFlags): raise e("invalid authority_flags")
        if self.state_delta_kind == "object_lever_interaction_state_delta_receipt":
            if not self.affected_safe_reference_ids: raise e("positive state delta receipt requires affected_safe_reference_ids")
            if self.state_delta_label != "object_lever_interaction_recorded": raise e("positive state delta receipt requires label 'object_lever_interaction_recorded'")
        else:
            if self.affected_safe_reference_ids: raise e("no-delta receipt must not carry affected_safe_reference_ids")
            if self.state_delta_label == "object_lever_interaction_recorded": raise e("no-delta receipt must not use positive delta label")
        object.__setattr__(self,"metadata",_meta(self.metadata,e))
    def to_dict(self)->dict[str,Any]: return {"state_delta_receipt_id":self.state_delta_receipt_id,"state_delta_kind":self.state_delta_kind,"command_family":self.command_family,"source_reference_ids":dict(self.source_reference_ids),"affected_safe_reference_ids":list(self.affected_safe_reference_ids),"state_delta_label":self.state_delta_label,"non_authority_note":self.non_authority_note,"authority_flags":self.authority_flags.to_dict(),"metadata":copy.deepcopy(dict(self.metadata))}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverCommittedEventRecord:
    committed_event_id: str; event_record_kind: str; command_family: str; source_reference: ObjectLeverCommitSourceRef; eligibility: ObjectLeverCommitEligibility; state_delta_receipt: ObjectLeverStateDeltaReceipt; safe_reference_ids: tuple[str,...]=(); non_authority_note: str=OBJECT_LEVER_COMMIT_NON_AUTHORITY_NOTE; authority_flags: ObjectLeverEventCommitAuthorityFlags=field(default_factory=ObjectLeverEventCommitAuthorityFlags); metadata: Mapping[str,Any]=field(default_factory=lambda: MappingProxyType({}))
    def __post_init__(self)->None:
        e=InvalidObjectLeverCommittedEventRecordError; _nonempty(self.committed_event_id,"committed_event_id",e)
        if self.event_record_kind not in OBJECT_LEVER_EVENT_RECORD_KINDS: raise e("invalid event_record_kind")
        if self.command_family != OBJECT_LEVER_COMMIT_COMMAND_FAMILY: raise e("invalid command_family")
        if not isinstance(self.source_reference,ObjectLeverCommitSourceRef): raise e("invalid source_reference")
        if not isinstance(self.eligibility,ObjectLeverCommitEligibility): raise e("invalid eligibility")
        if not isinstance(self.state_delta_receipt,ObjectLeverStateDeltaReceipt): raise e("invalid state_delta_receipt")
        event_status=_EVENT_KIND_TO_STATUS.get(self.event_record_kind)
        delta_status=_DELTA_KIND_TO_STATUS.get(self.state_delta_receipt.state_delta_kind)
        if event_status != delta_status: raise e("event_record_kind and state_delta_receipt kind are not coherent")
        if event_status == "committed":
            if self.eligibility.eligibility_status != "commit_ready": raise e("committed event record requires eligibility_status commit_ready")
        else:
            if self.eligibility.eligibility_status != event_status: raise e("event_record_kind and eligibility_status are not coherent")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
        _nonempty(self.non_authority_note,"non_authority_note",e)
        if not isinstance(self.authority_flags,ObjectLeverEventCommitAuthorityFlags): raise e("invalid authority_flags")
        object.__setattr__(self,"metadata",_meta(self.metadata,e))
    def to_dict(self)->dict[str,Any]: return {"committed_event_id":self.committed_event_id,"event_record_kind":self.event_record_kind,"command_family":self.command_family,"source_reference":self.source_reference.to_dict(),"eligibility":self.eligibility.to_dict(),"state_delta_receipt":self.state_delta_receipt.to_dict(),"safe_reference_ids":list(self.safe_reference_ids),"non_authority_note":self.non_authority_note,"authority_flags":self.authority_flags.to_dict(),"metadata":copy.deepcopy(dict(self.metadata))}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverEventCommitResult:
    result_id: str; commit_status: str; commit_decision: str; committed_event_record: ObjectLeverCommittedEventRecord | None=None; state_delta_receipt: ObjectLeverStateDeltaReceipt | None=None; block_reasons: tuple[str,...]=(); safe_reference_ids: tuple[str,...]=(); non_authority_note: str=OBJECT_LEVER_COMMIT_NON_AUTHORITY_NOTE; authority_flags: ObjectLeverEventCommitAuthorityFlags=field(default_factory=ObjectLeverEventCommitAuthorityFlags); metadata: Mapping[str,Any]=field(default_factory=lambda: MappingProxyType({}))
    def __post_init__(self)->None:
        e=InvalidObjectLeverEventCommitResultError; _nonempty(self.result_id,"result_id",e)
        if self.commit_status not in OBJECT_LEVER_COMMIT_STATUSES: raise e("invalid commit_status")
        if self.commit_decision not in OBJECT_LEVER_COMMIT_DECISIONS: raise e("invalid commit_decision")
        expected_decision=_COMMIT_STATUS_TO_DECISION.get(self.commit_status)
        if expected_decision is None or self.commit_decision != expected_decision: raise e("commit_status and commit_decision are not coherent")
        if self.commit_status == "committed":
            if self.committed_event_record is None: raise e("committed status requires committed_event_record")
            if self.state_delta_receipt is None: raise e("committed status requires state_delta_receipt")
            if self.committed_event_record.event_record_kind != "object_lever_interaction_committed_event": raise e("committed status requires committed event record kind")
            if self.state_delta_receipt.state_delta_kind != "object_lever_interaction_state_delta_receipt": raise e("committed status requires positive state delta receipt kind")
        else:
            if self.commit_decision == "object_lever_event_committed": raise e("non-committed status must not use object_lever_event_committed decision")
        if self.committed_event_record is not None and not isinstance(self.committed_event_record,ObjectLeverCommittedEventRecord): raise e("invalid committed_event_record")
        if self.state_delta_receipt is not None and not isinstance(self.state_delta_receipt,ObjectLeverStateDeltaReceipt): raise e("invalid state_delta_receipt")
        if self.committed_event_record is not None:
            record_status=_EVENT_KIND_TO_STATUS.get(self.committed_event_record.event_record_kind)
            if record_status != self.commit_status: raise e("committed_event_record kind is not coherent with commit_status")
        if self.state_delta_receipt is not None:
            receipt_status=_DELTA_KIND_TO_STATUS.get(self.state_delta_receipt.state_delta_kind)
            if receipt_status != self.commit_status: raise e("state_delta_receipt kind is not coherent with commit_status")
        object.__setattr__(self,"block_reasons",_tuple(self.block_reasons,"block_reasons",e))
        for r in self.block_reasons:
            if r not in OBJECT_LEVER_COMMIT_BLOCK_REASONS: raise e(f"invalid block_reason {r!r}")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
        _nonempty(self.non_authority_note,"non_authority_note",e)
        if not isinstance(self.authority_flags,ObjectLeverEventCommitAuthorityFlags): raise e("invalid authority_flags")
        object.__setattr__(self,"metadata",_meta(self.metadata,e))
    def to_dict(self)->dict[str,Any]: return {"result_id":self.result_id,"commit_status":self.commit_status,"commit_decision":self.commit_decision,"committed_event_record":None if self.committed_event_record is None else self.committed_event_record.to_dict(),"state_delta_receipt":None if self.state_delta_receipt is None else self.state_delta_receipt.to_dict(),"block_reasons":list(self.block_reasons),"safe_reference_ids":list(self.safe_reference_ids),"non_authority_note":self.non_authority_note,"authority_flags":self.authority_flags.to_dict(),"metadata":copy.deepcopy(dict(self.metadata))}

def create_object_lever_event_commit_authority_flags(): return ObjectLeverEventCommitAuthorityFlags()
def create_object_lever_commit_source_ref(**kw): return ObjectLeverCommitSourceRef(**kw)
def create_object_lever_commit_eligibility(**kw): return ObjectLeverCommitEligibility(**kw)
def create_object_lever_state_delta_receipt(**kw): return ObjectLeverStateDeltaReceipt(**kw)
def create_object_lever_committed_event_record(**kw): return ObjectLeverCommittedEventRecord(**kw)
def create_object_lever_event_commit_result(**kw): return ObjectLeverEventCommitResult(**kw)

def validate_object_lever_event_commit_authority_flags(v) -> bool:
    if not isinstance(v,ObjectLeverEventCommitAuthorityFlags): return False
    return all(getattr(v,f) is False for f in v.__dataclass_fields__)
def validate_object_lever_commit_source_ref(v) -> bool:
    if not isinstance(v,ObjectLeverCommitSourceRef): return False
    if v.command_family != OBJECT_LEVER_COMMIT_COMMAND_FAMILY: return False
    if v.bridge_decision not in OBJECT_LEVER_PREVIEW_BRIDGE_DECISIONS: return False
    if v.bridge_status not in OBJECT_LEVER_PREVIEW_BRIDGE_STATUSES: return False
    return isinstance(v.safe_reference_ids, tuple) and isinstance(v.bridge_block_reasons, tuple)
def validate_object_lever_commit_eligibility(v) -> bool:
    if not isinstance(v,ObjectLeverCommitEligibility): return False
    if v.command_family != OBJECT_LEVER_COMMIT_COMMAND_FAMILY: return False
    if v.eligibility_status not in OBJECT_LEVER_COMMIT_ELIGIBILITY_STATUSES: return False
    if v.bridge_decision not in OBJECT_LEVER_PREVIEW_BRIDGE_DECISIONS: return False
    if v.bridge_status not in OBJECT_LEVER_PREVIEW_BRIDGE_STATUSES: return False
    if not isinstance(v.block_reasons, tuple) or not isinstance(v.safe_reference_ids, tuple): return False
    return all(reason in OBJECT_LEVER_COMMIT_BLOCK_REASONS for reason in v.block_reasons)
def validate_object_lever_state_delta_receipt(v) -> bool:
    if not isinstance(v,ObjectLeverStateDeltaReceipt): return False
    if v.state_delta_kind not in OBJECT_LEVER_STATE_DELTA_KINDS: return False
    if v.command_family != OBJECT_LEVER_COMMIT_COMMAND_FAMILY: return False
    if not isinstance(v.source_reference_ids, MappingProxyType) and not isinstance(v.source_reference_ids, dict): return False
    if not validate_object_lever_event_commit_authority_flags(v.authority_flags): return False
    try: _no_forbidden(v.metadata,"metadata",InvalidObjectLeverStateDeltaReceiptError); _json(v.metadata,"metadata",InvalidObjectLeverStateDeltaReceiptError)
    except InvalidObjectLeverStateDeltaReceiptError: return False
    return True
def validate_object_lever_committed_event_record(v) -> bool:
    if not isinstance(v,ObjectLeverCommittedEventRecord): return False
    if v.event_record_kind not in OBJECT_LEVER_EVENT_RECORD_KINDS: return False
    if v.command_family != OBJECT_LEVER_COMMIT_COMMAND_FAMILY: return False
    if not validate_object_lever_commit_source_ref(v.source_reference): return False
    if not validate_object_lever_commit_eligibility(v.eligibility): return False
    if not validate_object_lever_state_delta_receipt(v.state_delta_receipt): return False
    if not validate_object_lever_event_commit_authority_flags(v.authority_flags): return False
    try: _no_forbidden(v.metadata,"metadata",InvalidObjectLeverCommittedEventRecordError); _json(v.metadata,"metadata",InvalidObjectLeverCommittedEventRecordError)
    except InvalidObjectLeverCommittedEventRecordError: return False
    return True
def validate_object_lever_event_commit_result(v) -> bool:
    if not isinstance(v,ObjectLeverEventCommitResult): return False
    if v.commit_status not in OBJECT_LEVER_COMMIT_STATUSES: return False
    if v.commit_decision not in OBJECT_LEVER_COMMIT_DECISIONS: return False
    if v.committed_event_record is not None and not validate_object_lever_committed_event_record(v.committed_event_record): return False
    if v.state_delta_receipt is not None and not validate_object_lever_state_delta_receipt(v.state_delta_receipt): return False
    if not isinstance(v.block_reasons, tuple) or not isinstance(v.safe_reference_ids, tuple): return False
    if not all(reason in OBJECT_LEVER_COMMIT_BLOCK_REASONS for reason in v.block_reasons): return False
    if not validate_object_lever_event_commit_authority_flags(v.authority_flags): return False
    try: _no_forbidden(v.metadata,"metadata",InvalidObjectLeverEventCommitResultError); _json(v.metadata,"metadata",InvalidObjectLeverEventCommitResultError)
    except InvalidObjectLeverEventCommitResultError: return False
    return True

def _has_required_object_lever_safe_references(safe_reference_ids: Sequence[str]) -> bool:
    if len(safe_reference_ids) < 3:
        return False
    lowered = tuple(ref.lower() for ref in safe_reference_ids)
    has_scene = any(ref.startswith("scene") or ":scene" in ref for ref in lowered)
    has_actor = any(ref.startswith("actor") or ":actor" in ref for ref in lowered)
    has_object_lever = any(ref.startswith("object_lever") or ref.startswith("lever") or ":object_lever" in ref or ":lever" in ref for ref in lowered)
    return has_scene and has_actor and has_object_lever

def build_object_lever_commit_source_ref(bridge_result: ObjectLeverTransactionPreviewBridgeResult) -> ObjectLeverCommitSourceRef:
    if not isinstance(bridge_result,ObjectLeverTransactionPreviewBridgeResult): raise InvalidObjectLeverCommitSourceRefError("bridge_result must be ObjectLeverTransactionPreviewBridgeResult")
    c=bridge_result.preview_candidate
    pcid=c.preview_candidate_id if c is not None else ""
    safe=() if c is None else c.safe_reference_ids
    block_reasons=() if c is None else c.eligibility.block_reasons
    return ObjectLeverCommitSourceRef(bridge_result_id=bridge_result.result_id, preview_candidate_id=pcid, command_family=OBJECT_LEVER_COMMIT_COMMAND_FAMILY, bridge_decision=bridge_result.bridge_decision, bridge_status=bridge_result.bridge_status, safe_reference_ids=safe, bridge_block_reasons=block_reasons)

def evaluate_object_lever_commit_eligibility(source_reference: ObjectLeverCommitSourceRef) -> ObjectLeverCommitEligibility:
    reasons=[]; status="commit_ready"
    if source_reference.command_family != OBJECT_LEVER_COMMIT_COMMAND_FAMILY: reasons.append("invalid_command_family")
    if source_reference.bridge_decision == "blocked": status="commit_blocked"; reasons.append("preview_blocked")
    elif source_reference.bridge_decision == "deferred": status="commit_deferred"; reasons.append("preview_deferred")
    elif source_reference.bridge_decision == "unknown": status="commit_unknown"; reasons.append("preview_unknown")
    elif source_reference.bridge_decision == "insufficient_legality": status="commit_insufficient_preview"; reasons.append("preview_insufficient")
    elif source_reference.bridge_decision != "preview_candidate_prepared": status="commit_blocked"; reasons.append("preview_not_prepared")
    if source_reference.bridge_status != "preview_bridge_available" and status == "commit_ready": status="commit_blocked"; reasons.append("preview_not_prepared")
    if not source_reference.preview_candidate_id: status="commit_blocked"; reasons.append("missing_preview_candidate")
    if source_reference.bridge_block_reasons:
        status="commit_blocked" if status=="commit_ready" else status; reasons.append("preview_not_prepared")
    if not _has_required_object_lever_safe_references(source_reference.safe_reference_ids):
        status="commit_blocked" if status=="commit_ready" else status; reasons.append("missing_safe_references")
    return ObjectLeverCommitEligibility(command_family=source_reference.command_family, eligibility_status=status, bridge_decision=source_reference.bridge_decision, bridge_status=source_reference.bridge_status, block_reasons=tuple(dict.fromkeys(reasons)), safe_reference_ids=source_reference.safe_reference_ids)

def _event_kind(status: str) -> str:
    return {"commit_ready":"object_lever_interaction_committed_event","commit_blocked":"object_lever_interaction_blocked_event","commit_deferred":"object_lever_interaction_deferred_event","commit_unknown":"object_lever_interaction_unknown_event","commit_insufficient_preview":"object_lever_interaction_insufficient_preview_event","committed":"object_lever_interaction_committed_event"}[status]
def _delta_kind(status: str) -> str:
    return {"commit_ready":"object_lever_interaction_state_delta_receipt","commit_blocked":"no_state_delta_due_to_block","commit_deferred":"no_state_delta_due_to_deferred","commit_unknown":"no_state_delta_due_to_unknown","commit_insufficient_preview":"no_state_delta_due_to_insufficient_preview","committed":"object_lever_interaction_state_delta_receipt"}[status]

def commit_object_lever_preview_to_event_and_state_delta(bridge_result: ObjectLeverTransactionPreviewBridgeResult, *, result_id: str | None=None, committed_event_id: str | None=None, state_delta_receipt_id: str | None=None, metadata: Mapping[str,Any] | None=None) -> ObjectLeverEventCommitResult:
    if not isinstance(bridge_result,ObjectLeverTransactionPreviewBridgeResult): raise InvalidObjectLeverEventCommitResultError("bridge_result must be ObjectLeverTransactionPreviewBridgeResult")
    source=build_object_lever_commit_source_ref(bridge_result)
    elig=evaluate_object_lever_commit_eligibility(source)
    if elig.eligibility_status == "commit_ready":
        status="committed"; decision="object_lever_event_committed"
    else:
        status=elig.eligibility_status; decision={"commit_blocked":"blocked","commit_deferred":"deferred","commit_unknown":"unknown","commit_insufficient_preview":"insufficient_preview"}[status]
    if status == "committed":
        delta=ObjectLeverStateDeltaReceipt(state_delta_receipt_id=state_delta_receipt_id or f"state-delta:{source.bridge_result_id}", state_delta_kind=_delta_kind(status), command_family=source.command_family, source_reference_ids={"bridge_result_id":source.bridge_result_id,**({"preview_candidate_id":source.preview_candidate_id} if source.preview_candidate_id else {})}, affected_safe_reference_ids=source.safe_reference_ids, state_delta_label="object_lever_interaction_recorded", metadata=metadata)
        event=ObjectLeverCommittedEventRecord(committed_event_id=committed_event_id or f"committed-event:{source.bridge_result_id}", event_record_kind=_event_kind(status), command_family=source.command_family, source_reference=source, eligibility=elig, state_delta_receipt=delta, safe_reference_ids=source.safe_reference_ids, metadata=metadata)
        return ObjectLeverEventCommitResult(result_id=result_id or f"commit:{source.bridge_result_id}", commit_status=status, commit_decision=decision, committed_event_record=event, state_delta_receipt=delta, safe_reference_ids=source.safe_reference_ids, metadata=metadata)
    delta=ObjectLeverStateDeltaReceipt(state_delta_receipt_id=state_delta_receipt_id or f"state-delta:{source.bridge_result_id}", state_delta_kind=_delta_kind(status), command_family=source.command_family, source_reference_ids={"bridge_result_id":source.bridge_result_id,**({"preview_candidate_id":source.preview_candidate_id} if source.preview_candidate_id else {})}, affected_safe_reference_ids=(), state_delta_label=_delta_kind(status).replace("_"," "), metadata=metadata)
    event=ObjectLeverCommittedEventRecord(committed_event_id=committed_event_id or f"committed-event:{source.bridge_result_id}", event_record_kind=_event_kind(status), command_family=source.command_family, source_reference=source, eligibility=elig, state_delta_receipt=delta, safe_reference_ids=(), metadata=metadata)
    return ObjectLeverEventCommitResult(result_id=result_id or f"commit:{source.bridge_result_id}", commit_status=status, commit_decision=decision, committed_event_record=event, state_delta_receipt=delta, block_reasons=elig.block_reasons, safe_reference_ids=source.safe_reference_ids, metadata=metadata)

def serialize_object_lever_state_delta_receipt(r):
    if not validate_object_lever_state_delta_receipt(r): raise InvalidObjectLeverStateDeltaReceiptError("invalid receipt")
    return r.to_dict()
def serialize_object_lever_committed_event_record(r):
    if not validate_object_lever_committed_event_record(r): raise InvalidObjectLeverCommittedEventRecordError("invalid record")
    return r.to_dict()
def serialize_object_lever_event_commit_result(r):
    if not validate_object_lever_event_commit_result(r): raise InvalidObjectLeverEventCommitResultError("invalid result")
    return r.to_dict()
def serialize_object_lever_state_delta_receipt_visible(r):
    if not validate_object_lever_state_delta_receipt(r): raise InvalidObjectLeverStateDeltaReceiptError("invalid receipt")
    return {"state_delta_kind":r.state_delta_kind,"command_family":r.command_family,"affected_safe_reference_ids":list(r.affected_safe_reference_ids),"state_delta_label":r.state_delta_label,"non_authority_note":r.non_authority_note}
def serialize_object_lever_committed_event_record_visible(r):
    if not validate_object_lever_committed_event_record(r): raise InvalidObjectLeverCommittedEventRecordError("invalid record")
    return {"committed_event_id":r.committed_event_id,"event_record_kind":r.event_record_kind,"command_family":r.command_family,"safe_reference_ids":list(r.safe_reference_ids),"non_authority_note":r.non_authority_note}
def serialize_object_lever_event_commit_result_visible(r):
    if not validate_object_lever_event_commit_result(r): raise InvalidObjectLeverEventCommitResultError("invalid result")
    c=r.committed_event_record; d=r.state_delta_receipt
    return {"result_id":r.result_id,"commit_status":r.commit_status,"commit_decision":r.commit_decision,"event_record_kind":None if c is None else c.event_record_kind,"state_delta_kind":None if d is None else d.state_delta_kind,"command_family":OBJECT_LEVER_COMMIT_COMMAND_FAMILY,"safe_reference_ids":list(r.safe_reference_ids),"block_reasons":list(r.block_reasons),"non_authority_note":r.non_authority_note}

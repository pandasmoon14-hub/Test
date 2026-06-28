"""Object/Lever Transaction Preview Bridge — RT-002D.

Narrow non-mutating bridge from RT-002C object/lever legality-reader results to
transaction-preview candidate envelopes for command family
``interact_with_object_lever`` only. This module does not execute commands,
mutate state, apply deltas, append or commit events, persist/replay, run RNG or
oracles, settle resources/consequences, call models, narrate, or expose hidden
truth.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.domain.object_lever_interaction_legality_reader import (
    OBJECT_LEVER_COMMAND_FAMILY,
    OBJECT_LEVER_LEGALITY_DECISIONS,
    OBJECT_LEVER_LEGALITY_READER_STATUSES,
    ObjectLeverLegalityReaderResult,
)

__all__ = [
    "OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY",
    "OBJECT_LEVER_PREVIEW_BRIDGE_STATUSES",
    "OBJECT_LEVER_PREVIEW_BRIDGE_DECISIONS",
    "OBJECT_LEVER_PREVIEW_CANDIDATE_KINDS",
    "OBJECT_LEVER_PREVIEW_ELIGIBILITY_STATUSES",
    "OBJECT_LEVER_PREVIEW_BLOCK_REASONS",
    "OBJECT_LEVER_PREVIEW_NON_AUTHORITY_NOTE",
    "FORBIDDEN_OBJECT_LEVER_PREVIEW_METADATA_KEYS",
    "ObjectLeverTransactionPreviewBridgeError",
    "InvalidObjectLeverTransactionPreviewBridgeAuthorityFlagsError",
    "InvalidObjectLeverPreviewBridgeSourceRefError",
    "InvalidObjectLeverPreviewEligibilityError",
    "InvalidObjectLeverTransactionPreviewCandidateError",
    "InvalidObjectLeverTransactionPreviewBridgeResultError",
    "ObjectLeverTransactionPreviewBridgeAuthorityFlags",
    "ObjectLeverPreviewBridgeSourceRef",
    "ObjectLeverPreviewEligibility",
    "ObjectLeverTransactionPreviewCandidate",
    "ObjectLeverTransactionPreviewBridgeResult",
    "create_object_lever_transaction_preview_bridge_authority_flags",
    "create_object_lever_preview_bridge_source_ref",
    "create_object_lever_preview_eligibility",
    "create_object_lever_transaction_preview_candidate",
    "create_object_lever_transaction_preview_bridge_result",
    "build_object_lever_preview_bridge_source_ref",
    "evaluate_object_lever_preview_eligibility",
    "bridge_object_lever_legality_to_transaction_preview",
    "serialize_object_lever_transaction_preview_candidate",
    "serialize_object_lever_transaction_preview_candidate_visible",
    "serialize_object_lever_transaction_preview_bridge_result",
    "serialize_object_lever_transaction_preview_bridge_result_visible",
    "validate_object_lever_transaction_preview_bridge_authority_flags",
    "validate_object_lever_preview_bridge_source_ref",
    "validate_object_lever_preview_eligibility",
    "validate_object_lever_transaction_preview_candidate",
    "validate_object_lever_transaction_preview_bridge_result",
]

OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY = OBJECT_LEVER_COMMAND_FAMILY
OBJECT_LEVER_PREVIEW_BRIDGE_STATUSES = frozenset({"preview_bridge_available", "preview_bridge_blocked", "preview_bridge_deferred", "preview_bridge_unknown", "preview_bridge_insufficient_legality"})
OBJECT_LEVER_PREVIEW_BRIDGE_DECISIONS = frozenset({"preview_candidate_prepared", "blocked", "deferred", "unknown", "insufficient_legality"})
OBJECT_LEVER_PREVIEW_CANDIDATE_KINDS = frozenset({"object_lever_interaction_preview_candidate", "blocked_preview_candidate", "deferred_preview_candidate", "unknown_preview_candidate", "insufficient_legality_preview_candidate"})
OBJECT_LEVER_PREVIEW_ELIGIBILITY_STATUSES = frozenset({"eligible_for_preview", "blocked", "deferred", "unknown", "insufficient_legality"})
OBJECT_LEVER_PREVIEW_BLOCK_REASONS = frozenset({"legality_not_permitted_for_preview", "legality_blocked", "legality_deferred", "legality_unknown", "legality_insufficient_projection", "missing_legality_reading", "invalid_command_family", "missing_safe_references", "hidden_information_not_available", "preview_not_constructible"})
OBJECT_LEVER_PREVIEW_NON_AUTHORITY_NOTE = ("RT-002D prepares only a non-mutating object/lever transaction preview candidate; it authorizes no command execution, state mutation, state delta application, event append, event commitment, persistence/replay writes, RNG/table/oracle execution, resource/consequence settlement, combat/ability/skill/effect resolution, model/narration/live-play/UI behavior, conversion, sourcebook inclusion, or canon promotion.")
FORBIDDEN_OBJECT_LEVER_PREVIEW_METADATA_KEYS = frozenset({"hidden_fact", "hidden_facts", "secret", "secrets", "backend_only_fact", "backend_only_facts", "state_payload", "raw_state", "actual_state", "truth_payload", "projection_payload", "record_payload", "world_state", "legality_payload", "transaction_execution", "command_execution", "execution_result", "state_delta", "state_delta_payload", "mutation_payload", "event_payload", "event_append", "event_commitment", "event_commit", "persistence_write", "resource_settlement", "consequence_application", "damage_application", "condition_application", "rng_result", "oracle_result", "model_prompt", "narration"})

class ObjectLeverTransactionPreviewBridgeError(ValueError): pass
class InvalidObjectLeverTransactionPreviewBridgeAuthorityFlagsError(ObjectLeverTransactionPreviewBridgeError): pass
class InvalidObjectLeverPreviewBridgeSourceRefError(ObjectLeverTransactionPreviewBridgeError): pass
class InvalidObjectLeverPreviewEligibilityError(ObjectLeverTransactionPreviewBridgeError): pass
class InvalidObjectLeverTransactionPreviewCandidateError(ObjectLeverTransactionPreviewBridgeError): pass
class InvalidObjectLeverTransactionPreviewBridgeResultError(ObjectLeverTransactionPreviewBridgeError): pass

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
            if k in FORBIDDEN_OBJECT_LEVER_PREVIEW_METADATA_KEYS: raise e(f"metadata key {k!r} at {path} is forbidden")
            _no_forbidden(x, f"{path}.{k}", e)
    elif isinstance(value,(list,tuple)):
        for i,x in enumerate(value): _no_forbidden(x, f"{path}[{i}]", e)

def _meta(m: Mapping[str,Any] | None, e: type[Exception]) -> Mapping[str,Any]:
    if m is None: return MappingProxyType({})
    if not isinstance(m, Mapping): raise e("metadata must be a mapping")
    _no_forbidden(m,"metadata",e); _json(m,"metadata",e)
    return MappingProxyType(copy.deepcopy(dict(m)))

@dataclass(frozen=True, kw_only=True)
class ObjectLeverTransactionPreviewBridgeAuthorityFlags:
    command_execution_authorized: bool=False; state_mutation_authorized: bool=False; state_delta_application_authorized: bool=False; event_append_authorized: bool=False; event_commitment_authorized: bool=False; persistence_write_authorized: bool=False; replay_write_authorized: bool=False; rng_execution_authorized: bool=False; table_oracle_execution_authorized: bool=False; resource_math_execution_authorized: bool=False; consequence_application_authorized: bool=False; combat_resolution_authorized: bool=False; model_call_authorized: bool=False; narration_generation_authorized: bool=False; live_play_authorized: bool=False; ui_authorized: bool=False; conversion_authorized: bool=False; canon_promotion_authorized: bool=False
    def __post_init__(self) -> None:
        for f in self.__dataclass_fields__:
            if getattr(self,f) is not False: raise InvalidObjectLeverTransactionPreviewBridgeAuthorityFlagsError(f"authority flag {f!r} must be False")
    def to_dict(self) -> dict[str,Any]: return {f: False for f in self.__dataclass_fields__}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverPreviewBridgeSourceRef:
    legality_result_id: str; legality_reading_id: str; command_family: str; legality_decision: str; reader_status: str; safe_reference_ids: tuple[str,...]=()
    def __post_init__(self) -> None:
        e=InvalidObjectLeverPreviewBridgeSourceRefError
        for n in ("legality_result_id","legality_reading_id","command_family","legality_decision","reader_status"): _nonempty(getattr(self,n),n,e)
        if self.command_family != OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY: raise e("invalid command_family")
        if self.legality_decision not in OBJECT_LEVER_LEGALITY_DECISIONS: raise e("invalid legality_decision")
        if self.reader_status not in OBJECT_LEVER_LEGALITY_READER_STATUSES: raise e("invalid reader_status")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
    def to_dict(self)->dict[str,Any]: return {"legality_result_id":self.legality_result_id,"legality_reading_id":self.legality_reading_id,"command_family":self.command_family,"legality_decision":self.legality_decision,"reader_status":self.reader_status,"safe_reference_ids":list(self.safe_reference_ids)}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverPreviewEligibility:
    command_family: str; eligibility_status: str; legality_decision: str; reader_status: str; block_reasons: tuple[str,...]=(); safe_reference_ids: tuple[str,...]=()
    def __post_init__(self)->None:
        e=InvalidObjectLeverPreviewEligibilityError
        if self.command_family != OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY: raise e("invalid command_family")
        if self.eligibility_status not in OBJECT_LEVER_PREVIEW_ELIGIBILITY_STATUSES: raise e("invalid eligibility_status")
        if self.legality_decision not in OBJECT_LEVER_LEGALITY_DECISIONS: raise e("invalid legality_decision")
        if self.reader_status not in OBJECT_LEVER_LEGALITY_READER_STATUSES: raise e("invalid reader_status")
        object.__setattr__(self,"block_reasons",_tuple(self.block_reasons,"block_reasons",e))
        for r in self.block_reasons:
            if r not in OBJECT_LEVER_PREVIEW_BLOCK_REASONS: raise e(f"invalid block_reason {r!r}")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
    def to_dict(self)->dict[str,Any]: return {"command_family":self.command_family,"eligibility_status":self.eligibility_status,"legality_decision":self.legality_decision,"reader_status":self.reader_status,"block_reasons":list(self.block_reasons),"safe_reference_ids":list(self.safe_reference_ids)}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverTransactionPreviewCandidate:
    preview_candidate_id: str; preview_candidate_kind: str; command_family: str; source_reference: ObjectLeverPreviewBridgeSourceRef; eligibility: ObjectLeverPreviewEligibility; safe_reference_ids: tuple[str,...]=(); non_authority_note: str=OBJECT_LEVER_PREVIEW_NON_AUTHORITY_NOTE; authority_flags: ObjectLeverTransactionPreviewBridgeAuthorityFlags=field(default_factory=ObjectLeverTransactionPreviewBridgeAuthorityFlags); metadata: Mapping[str,Any]=field(default_factory=lambda: MappingProxyType({}))
    def __post_init__(self)->None:
        e=InvalidObjectLeverTransactionPreviewCandidateError; _nonempty(self.preview_candidate_id,"preview_candidate_id",e)
        if self.preview_candidate_kind not in OBJECT_LEVER_PREVIEW_CANDIDATE_KINDS: raise e("invalid preview_candidate_kind")
        if self.command_family != OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY: raise e("invalid command_family")
        if not isinstance(self.source_reference,ObjectLeverPreviewBridgeSourceRef): raise e("invalid source_reference")
        if not isinstance(self.eligibility,ObjectLeverPreviewEligibility): raise e("invalid eligibility")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
        _nonempty(self.non_authority_note,"non_authority_note",e)
        if not isinstance(self.authority_flags,ObjectLeverTransactionPreviewBridgeAuthorityFlags): raise e("invalid authority_flags")
        object.__setattr__(self,"metadata",_meta(self.metadata,e))
    def to_dict(self)->dict[str,Any]: return {"preview_candidate_id":self.preview_candidate_id,"preview_candidate_kind":self.preview_candidate_kind,"command_family":self.command_family,"source_reference":self.source_reference.to_dict(),"eligibility":self.eligibility.to_dict(),"safe_reference_ids":list(self.safe_reference_ids),"non_authority_note":self.non_authority_note,"authority_flags":self.authority_flags.to_dict(),"metadata":copy.deepcopy(dict(self.metadata))}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverTransactionPreviewBridgeResult:
    result_id: str; bridge_status: str; bridge_decision: str; preview_candidate: ObjectLeverTransactionPreviewCandidate | None; non_authority_note: str=OBJECT_LEVER_PREVIEW_NON_AUTHORITY_NOTE; authority_flags: ObjectLeverTransactionPreviewBridgeAuthorityFlags=field(default_factory=ObjectLeverTransactionPreviewBridgeAuthorityFlags); metadata: Mapping[str,Any]=field(default_factory=lambda: MappingProxyType({}))
    def __post_init__(self)->None:
        e=InvalidObjectLeverTransactionPreviewBridgeResultError; _nonempty(self.result_id,"result_id",e)
        if self.bridge_status not in OBJECT_LEVER_PREVIEW_BRIDGE_STATUSES: raise e("invalid bridge_status")
        if self.bridge_decision not in OBJECT_LEVER_PREVIEW_BRIDGE_DECISIONS: raise e("invalid bridge_decision")
        if self.preview_candidate is not None and not isinstance(self.preview_candidate,ObjectLeverTransactionPreviewCandidate): raise e("invalid preview_candidate")
        _nonempty(self.non_authority_note,"non_authority_note",e)
        if not isinstance(self.authority_flags,ObjectLeverTransactionPreviewBridgeAuthorityFlags): raise e("invalid authority_flags")
        object.__setattr__(self,"metadata",_meta(self.metadata,e))
    def to_dict(self)->dict[str,Any]: return {"result_id":self.result_id,"bridge_status":self.bridge_status,"bridge_decision":self.bridge_decision,"preview_candidate":None if self.preview_candidate is None else self.preview_candidate.to_dict(),"non_authority_note":self.non_authority_note,"authority_flags":self.authority_flags.to_dict(),"metadata":copy.deepcopy(dict(self.metadata))}

def create_object_lever_transaction_preview_bridge_authority_flags(): return ObjectLeverTransactionPreviewBridgeAuthorityFlags()
def create_object_lever_preview_bridge_source_ref(**kw): return ObjectLeverPreviewBridgeSourceRef(**kw)
def create_object_lever_preview_eligibility(**kw): return ObjectLeverPreviewEligibility(**kw)
def create_object_lever_transaction_preview_candidate(**kw): return ObjectLeverTransactionPreviewCandidate(**kw)
def create_object_lever_transaction_preview_bridge_result(**kw): return ObjectLeverTransactionPreviewBridgeResult(**kw)
def validate_object_lever_transaction_preview_bridge_authority_flags(v):
    if not isinstance(v,ObjectLeverTransactionPreviewBridgeAuthorityFlags): raise InvalidObjectLeverTransactionPreviewBridgeAuthorityFlagsError("invalid authority_flags")
    return v
def validate_object_lever_preview_bridge_source_ref(v):
    if not isinstance(v,ObjectLeverPreviewBridgeSourceRef): raise InvalidObjectLeverPreviewBridgeSourceRefError("invalid source_ref")
    return v
def validate_object_lever_preview_eligibility(v):
    if not isinstance(v,ObjectLeverPreviewEligibility): raise InvalidObjectLeverPreviewEligibilityError("invalid eligibility")
    return v
def validate_object_lever_transaction_preview_candidate(v):
    if not isinstance(v,ObjectLeverTransactionPreviewCandidate): raise InvalidObjectLeverTransactionPreviewCandidateError("invalid candidate")
    return v
def validate_object_lever_transaction_preview_bridge_result(v):
    if not isinstance(v,ObjectLeverTransactionPreviewBridgeResult): raise InvalidObjectLeverTransactionPreviewBridgeResultError("invalid result")
    return v

def build_object_lever_preview_bridge_source_ref(legality_result: ObjectLeverLegalityReaderResult) -> ObjectLeverPreviewBridgeSourceRef:
    if not isinstance(legality_result,ObjectLeverLegalityReaderResult): raise InvalidObjectLeverPreviewBridgeSourceRefError("legality_result must be ObjectLeverLegalityReaderResult")
    r=legality_result.legality_reading
    return ObjectLeverPreviewBridgeSourceRef(legality_result_id=legality_result.result_id, legality_reading_id=r.reading_id, command_family=r.command_family, legality_decision=legality_result.legality_decision, reader_status=legality_result.reader_status, safe_reference_ids=r.safe_reference_ids)

def evaluate_object_lever_preview_eligibility(source_reference: ObjectLeverPreviewBridgeSourceRef) -> ObjectLeverPreviewEligibility:
    reasons=[]; status="eligible_for_preview"
    if source_reference.command_family != OBJECT_LEVER_PREVIEW_BRIDGE_COMMAND_FAMILY: reasons.append("invalid_command_family")
    if source_reference.legality_decision == "blocked": status="blocked"; reasons.append("legality_blocked")
    elif source_reference.legality_decision == "deferred": status="deferred"; reasons.append("legality_deferred")
    elif source_reference.legality_decision == "unknown": status="unknown"; reasons.append("legality_unknown")
    elif source_reference.legality_decision == "insufficient_projection": status="insufficient_legality"; reasons.append("legality_insufficient_projection")
    elif source_reference.legality_decision != "permitted_for_preview": status="blocked"; reasons.append("legality_not_permitted_for_preview")
    if source_reference.reader_status != "legality_read_available" and status == "eligible_for_preview": status="insufficient_legality"; reasons.append("preview_not_constructible")
    if not source_reference.safe_reference_ids: status="blocked" if status=="eligible_for_preview" else status; reasons.append("missing_safe_references")
    return ObjectLeverPreviewEligibility(command_family=source_reference.command_family, eligibility_status=status, legality_decision=source_reference.legality_decision, reader_status=source_reference.reader_status, block_reasons=tuple(dict.fromkeys(reasons)), safe_reference_ids=source_reference.safe_reference_ids)

def _kind(status: str) -> str:
    return {"eligible_for_preview":"object_lever_interaction_preview_candidate","blocked":"blocked_preview_candidate","deferred":"deferred_preview_candidate","unknown":"unknown_preview_candidate","insufficient_legality":"insufficient_legality_preview_candidate"}[status]
def _bridge(status: str) -> tuple[str,str]:
    return {"eligible_for_preview":("preview_bridge_available","preview_candidate_prepared"),"blocked":("preview_bridge_blocked","blocked"),"deferred":("preview_bridge_deferred","deferred"),"unknown":("preview_bridge_unknown","unknown"),"insufficient_legality":("preview_bridge_insufficient_legality","insufficient_legality")}[status]

def bridge_object_lever_legality_to_transaction_preview(legality_result: ObjectLeverLegalityReaderResult, *, result_id: str | None=None, preview_candidate_id: str | None=None, metadata: Mapping[str,Any] | None=None) -> ObjectLeverTransactionPreviewBridgeResult:
    source=build_object_lever_preview_bridge_source_ref(legality_result)
    elig=evaluate_object_lever_preview_eligibility(source)
    bs,bd=_bridge(elig.eligibility_status)
    cand=ObjectLeverTransactionPreviewCandidate(preview_candidate_id=preview_candidate_id or f"preview-candidate:{source.legality_result_id}", preview_candidate_kind=_kind(elig.eligibility_status), command_family=source.command_family, source_reference=source, eligibility=elig, safe_reference_ids=source.safe_reference_ids, metadata=metadata)
    return ObjectLeverTransactionPreviewBridgeResult(result_id=result_id or f"preview-bridge:{source.legality_result_id}", bridge_status=bs, bridge_decision=bd, preview_candidate=cand, metadata=metadata)

def serialize_object_lever_transaction_preview_candidate(c): validate_object_lever_transaction_preview_candidate(c); return c.to_dict()
def serialize_object_lever_transaction_preview_bridge_result(r): validate_object_lever_transaction_preview_bridge_result(r); return r.to_dict()
def serialize_object_lever_transaction_preview_candidate_visible(c):
    validate_object_lever_transaction_preview_candidate(c)
    return {"preview_candidate_kind":c.preview_candidate_kind,"command_family":c.command_family,"safe_reference_ids":list(c.safe_reference_ids),"block_reasons":list(c.eligibility.block_reasons),"non_authority_note":c.non_authority_note}
def serialize_object_lever_transaction_preview_bridge_result_visible(r):
    validate_object_lever_transaction_preview_bridge_result(r)
    c=r.preview_candidate
    return {"result_id":r.result_id,"bridge_status":r.bridge_status,"bridge_decision":r.bridge_decision,"preview_candidate_kind":None if c is None else c.preview_candidate_kind,"command_family":None if c is None else c.command_family,"safe_reference_ids":[] if c is None else list(c.safe_reference_ids),"block_reasons":[] if c is None else list(c.eligibility.block_reasons),"non_authority_note":r.non_authority_note}

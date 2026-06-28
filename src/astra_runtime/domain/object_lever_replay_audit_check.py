"""Object/Lever Replay and Audit Check — RT-002F.

Tiny deterministic replay/audit check for exactly one command family:
``interact_with_object_lever``. Consumes RT-002E
``ObjectLeverEventCommitResult`` values and produces a stable in-memory audit
snapshot and replay-check receipt only when RT-002E reports a coherent
committed object/lever event/state-delta result.

This module does not write to persistence, replay indexes, event stores, or
broad audit infrastructure. It does not replay commands, reconstruct state,
mutate state, apply state deltas, execute RNG/table/oracle logic, settle
resources or consequences, apply damage or conditions, resolve combat, call
models, generate narration, drive live-play or UI behavior, or promote canon.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.domain.object_lever_event_commit_state_delta_path import (
    OBJECT_LEVER_COMMIT_COMMAND_FAMILY,
    OBJECT_LEVER_COMMIT_DECISIONS,
    OBJECT_LEVER_COMMIT_STATUSES,
    ObjectLeverCommittedEventRecord,
    ObjectLeverEventCommitResult,
    ObjectLeverStateDeltaReceipt,
)

__all__ = [
    "OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY",
    "OBJECT_LEVER_REPLAY_AUDIT_STATUSES",
    "OBJECT_LEVER_REPLAY_AUDIT_DECISIONS",
    "OBJECT_LEVER_AUDIT_SNAPSHOT_KINDS",
    "OBJECT_LEVER_REPLAY_CHECK_KINDS",
    "OBJECT_LEVER_REPLAY_AUDIT_BLOCK_REASONS",
    "OBJECT_LEVER_REPLAY_AUDIT_NON_AUTHORITY_NOTE",
    "FORBIDDEN_OBJECT_LEVER_REPLAY_AUDIT_METADATA_KEYS",
    "ObjectLeverReplayAuditCheckError",
    "InvalidObjectLeverReplayAuditAuthorityFlagsError",
    "InvalidObjectLeverReplayAuditSourceRefError",
    "InvalidObjectLeverReplayAuditEligibilityError",
    "InvalidObjectLeverAuditSnapshotError",
    "InvalidObjectLeverReplayCheckReceiptError",
    "InvalidObjectLeverReplayAuditResultError",
    "ObjectLeverReplayAuditAuthorityFlags",
    "ObjectLeverReplayAuditSourceRef",
    "ObjectLeverReplayAuditEligibility",
    "ObjectLeverAuditSnapshot",
    "ObjectLeverReplayCheckReceipt",
    "ObjectLeverReplayAuditResult",
    "create_object_lever_replay_audit_authority_flags",
    "create_object_lever_replay_audit_source_ref",
    "create_object_lever_replay_audit_eligibility",
    "create_object_lever_audit_snapshot",
    "create_object_lever_replay_check_receipt",
    "create_object_lever_replay_audit_result",
    "build_object_lever_replay_audit_source_ref",
    "evaluate_object_lever_replay_audit_eligibility",
    "build_object_lever_audit_snapshot",
    "build_object_lever_replay_check_receipt",
    "audit_object_lever_event_commit_result",
    "serialize_object_lever_audit_snapshot",
    "serialize_object_lever_audit_snapshot_visible",
    "serialize_object_lever_replay_check_receipt",
    "serialize_object_lever_replay_check_receipt_visible",
    "serialize_object_lever_replay_audit_result",
    "serialize_object_lever_replay_audit_result_visible",
    "validate_object_lever_replay_audit_authority_flags",
    "validate_object_lever_replay_audit_source_ref",
    "validate_object_lever_replay_audit_eligibility",
    "validate_object_lever_audit_snapshot",
    "validate_object_lever_replay_check_receipt",
    "validate_object_lever_replay_audit_result",
]

OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY = OBJECT_LEVER_COMMIT_COMMAND_FAMILY
OBJECT_LEVER_REPLAY_AUDIT_STATUSES = frozenset({"audit_ready", "audit_blocked", "audit_deferred", "audit_unknown", "audit_insufficient_commit", "audit_verified"})
OBJECT_LEVER_REPLAY_AUDIT_DECISIONS = frozenset({"object_lever_audit_verified", "blocked", "deferred", "unknown", "insufficient_commit"})
_COMMIT_STATUS_TO_DECISION = {"committed":"object_lever_event_committed","commit_blocked":"blocked","commit_deferred":"deferred","commit_unknown":"unknown","commit_insufficient_preview":"insufficient_preview"}
_AUDIT_STATUS_TO_DECISION = {"audit_verified":"object_lever_audit_verified","audit_blocked":"blocked","audit_deferred":"deferred","audit_unknown":"unknown","audit_insufficient_commit":"insufficient_commit","audit_ready":"unknown"}
OBJECT_LEVER_AUDIT_SNAPSHOT_KINDS = frozenset({"object_lever_committed_event_audit_snapshot", "object_lever_blocked_event_audit_snapshot", "object_lever_deferred_event_audit_snapshot", "object_lever_unknown_event_audit_snapshot", "object_lever_insufficient_commit_audit_snapshot"})
OBJECT_LEVER_REPLAY_CHECK_KINDS = frozenset({"object_lever_committed_event_replay_check", "object_lever_blocked_event_replay_check", "object_lever_deferred_event_replay_check", "object_lever_unknown_event_replay_check", "object_lever_insufficient_commit_replay_check"})
_AUDIT_STATUS_TO_SNAPSHOT_KIND = {"audit_ready":"object_lever_committed_event_audit_snapshot","audit_verified":"object_lever_committed_event_audit_snapshot","audit_blocked":"object_lever_blocked_event_audit_snapshot","audit_deferred":"object_lever_deferred_event_audit_snapshot","audit_unknown":"object_lever_unknown_event_audit_snapshot","audit_insufficient_commit":"object_lever_insufficient_commit_audit_snapshot"}
_AUDIT_STATUS_TO_REPLAY_CHECK_KIND = {"audit_ready":"object_lever_committed_event_replay_check","audit_verified":"object_lever_committed_event_replay_check","audit_blocked":"object_lever_blocked_event_replay_check","audit_deferred":"object_lever_deferred_event_replay_check","audit_unknown":"object_lever_unknown_event_replay_check","audit_insufficient_commit":"object_lever_insufficient_commit_replay_check"}
OBJECT_LEVER_REPLAY_AUDIT_BLOCK_REASONS = frozenset({"commit_not_auditable", "commit_blocked", "commit_deferred", "commit_unknown", "commit_insufficient", "missing_committed_event_record", "missing_state_delta_receipt", "invalid_command_family", "missing_safe_references", "audit_snapshot_not_constructible", "replay_check_not_constructible", "hidden_information_not_available", "non_deterministic_serialization_detected", "audit_identity_mismatch"})
OBJECT_LEVER_REPLAY_AUDIT_NON_AUTHORITY_NOTE = ("RT-002F produces only a narrow deterministic in-memory replay/audit-check receipt for an already-committed RT-002E object/lever event/state-delta result; it authorizes no durable persistence writes, replay index writes, event-store append/read, command re-execution, state reconstruction, general replay engine, state mutation, state-delta application, RNG/table/oracle execution, resource/consequence settlement, damage/condition application, combat/ability/skill/effect resolution, model/narration/live-play/UI behavior, conversion, sourcebook inclusion, or canon promotion.")
FORBIDDEN_OBJECT_LEVER_REPLAY_AUDIT_METADATA_KEYS = frozenset({"hidden_fact", "hidden_facts", "secret", "secrets", "backend_only_fact", "backend_only_facts", "state_payload", "raw_state", "actual_state", "truth_payload", "projection_payload", "record_payload", "world_state", "legality_payload", "preview_payload", "commit_payload", "event_payload", "event_store_append", "event_store_read", "event_log", "persistence_write", "persistent_record", "replay_write", "replay_index", "replay_store", "state_reconstruction", "command_reexecution", "transaction_execution", "command_execution", "execution_result", "arbitrary_mutation", "mutation_payload", "state_before", "state_after", "state_delta_payload", "resource_settlement", "consequence_application", "damage_application", "condition_application", "rng_result", "oracle_result", "model_prompt", "narration", "event_append", "event_commitment_payload"})

class ObjectLeverReplayAuditCheckError(ValueError): pass
class InvalidObjectLeverReplayAuditAuthorityFlagsError(ObjectLeverReplayAuditCheckError): pass
class InvalidObjectLeverReplayAuditSourceRefError(ObjectLeverReplayAuditCheckError): pass
class InvalidObjectLeverReplayAuditEligibilityError(ObjectLeverReplayAuditCheckError): pass
class InvalidObjectLeverAuditSnapshotError(ObjectLeverReplayAuditCheckError): pass
class InvalidObjectLeverReplayCheckReceiptError(ObjectLeverReplayAuditCheckError): pass
class InvalidObjectLeverReplayAuditResultError(ObjectLeverReplayAuditCheckError): pass

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
            if k in FORBIDDEN_OBJECT_LEVER_REPLAY_AUDIT_METADATA_KEYS: raise e(f"metadata key {k!r} at {path} is forbidden")
            _no_forbidden(x, f"{path}.{k}", e)
    elif isinstance(value,(list,tuple)):
        for i,x in enumerate(value): _no_forbidden(x, f"{path}[{i}]", e)

def _meta(m: Mapping[str,Any] | None, e: type[Exception]) -> Mapping[str,Any]:
    if m is None: return MappingProxyType({})
    if not isinstance(m, Mapping): raise e("metadata must be a mapping")
    _no_forbidden(m,"metadata",e); _json(m,"metadata",e)
    return MappingProxyType(copy.deepcopy(dict(m)))

def _mapping_str_str(m: Mapping[str,str] | None, n: str, e: type[Exception]) -> Mapping[str,str]:
    if m is None: return MappingProxyType({})
    if not isinstance(m, Mapping): raise e(f"{n} must be a mapping")
    out={}
    for k,v in m.items():
        if not isinstance(k,str) or not k: raise e(f"{n} keys must be non-empty strings")
        if not isinstance(v,str) or not v: raise e(f"{n} values must be non-empty strings")
        out[k]=v
    return MappingProxyType(out)

@dataclass(frozen=True, kw_only=True)
class ObjectLeverReplayAuditAuthorityFlags:
    persistence_write_authorized: bool=False; replay_write_authorized: bool=False; replay_index_authorized: bool=False; event_store_append_authorized: bool=False; event_store_read_authorized: bool=False; state_reconstruction_authorized: bool=False; command_reexecution_authorized: bool=False; state_mutation_authorized: bool=False; state_delta_application_authorized: bool=False; rng_execution_authorized: bool=False; table_oracle_execution_authorized: bool=False; resource_math_execution_authorized: bool=False; consequence_application_authorized: bool=False; damage_application_authorized: bool=False; condition_application_authorized: bool=False; combat_resolution_authorized: bool=False; model_call_authorized: bool=False; narration_generation_authorized: bool=False; live_play_authorized: bool=False; ui_authorized: bool=False; conversion_authorized: bool=False; canon_promotion_authorized: bool=False
    def __post_init__(self) -> None:
        for f in self.__dataclass_fields__:
            if getattr(self,f) is not False: raise InvalidObjectLeverReplayAuditAuthorityFlagsError(f"authority flag {f!r} must be False")
    def to_dict(self) -> dict[str,Any]: return {f: False for f in self.__dataclass_fields__}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverReplayAuditSourceRef:
    commit_result_id: str; committed_event_id: str | None=None; state_delta_receipt_id: str | None=None; command_family: str; commit_status: str; commit_decision: str; safe_reference_ids: tuple[str,...]=(); commit_block_reasons: tuple[str,...]=()
    def __post_init__(self) -> None:
        e=InvalidObjectLeverReplayAuditSourceRefError
        _nonempty(self.commit_result_id,"commit_result_id",e)
        if self.committed_event_id is not None and (not isinstance(self.committed_event_id,str) or not self.committed_event_id): raise e("committed_event_id must be a non-empty string or None")
        if self.state_delta_receipt_id is not None and (not isinstance(self.state_delta_receipt_id,str) or not self.state_delta_receipt_id): raise e("state_delta_receipt_id must be a non-empty string or None")
        _nonempty(self.command_family,"command_family",e)
        if self.command_family != OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY: raise e("invalid command_family")
        if self.commit_status not in OBJECT_LEVER_COMMIT_STATUSES: raise e("invalid commit_status")
        if self.commit_decision not in OBJECT_LEVER_COMMIT_DECISIONS: raise e("invalid commit_decision")
        expected=_COMMIT_STATUS_TO_DECISION.get(self.commit_status)
        if expected is None or self.commit_decision != expected: raise e("commit_status and commit_decision are not coherent")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
        object.__setattr__(self,"commit_block_reasons",_tuple(self.commit_block_reasons,"commit_block_reasons",e))
    def to_dict(self) -> dict[str,Any]: return {"commit_result_id":self.commit_result_id,"committed_event_id":self.committed_event_id,"state_delta_receipt_id":self.state_delta_receipt_id,"command_family":self.command_family,"commit_status":self.commit_status,"commit_decision":self.commit_decision,"safe_reference_ids":list(self.safe_reference_ids),"commit_block_reasons":list(self.commit_block_reasons)}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverReplayAuditEligibility:
    command_family: str; eligibility_status: str; commit_status: str; commit_decision: str; block_reasons: tuple[str,...]=(); safe_reference_ids: tuple[str,...]=()
    def __post_init__(self) -> None:
        e=InvalidObjectLeverReplayAuditEligibilityError
        if self.command_family != OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY: raise e("invalid command_family")
        if self.eligibility_status not in OBJECT_LEVER_REPLAY_AUDIT_STATUSES: raise e("invalid eligibility_status")
        if self.commit_status not in OBJECT_LEVER_COMMIT_STATUSES: raise e("invalid commit_status")
        if self.commit_decision not in OBJECT_LEVER_COMMIT_DECISIONS: raise e("invalid commit_decision")
        expected=_COMMIT_STATUS_TO_DECISION.get(self.commit_status)
        if expected is None or self.commit_decision != expected: raise e("commit_status and commit_decision are not coherent")
        object.__setattr__(self,"block_reasons",_tuple(self.block_reasons,"block_reasons",e))
        for r in self.block_reasons:
            if r not in OBJECT_LEVER_REPLAY_AUDIT_BLOCK_REASONS: raise e(f"invalid block_reason {r!r}")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
    def to_dict(self) -> dict[str,Any]: return {"command_family":self.command_family,"eligibility_status":self.eligibility_status,"commit_status":self.commit_status,"commit_decision":self.commit_decision,"block_reasons":list(self.block_reasons),"safe_reference_ids":list(self.safe_reference_ids)}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverAuditSnapshot:
    snapshot_id: str; audit_snapshot_kind: str; command_family: str; source_reference: ObjectLeverReplayAuditSourceRef; eligibility: ObjectLeverReplayAuditEligibility; safe_reference_ids: tuple[str,...]=(); deterministic_source_fields: Mapping[str,Any]=field(default_factory=lambda: MappingProxyType({})); audit_identity: str | None=None; non_authority_note: str=OBJECT_LEVER_REPLAY_AUDIT_NON_AUTHORITY_NOTE; authority_flags: ObjectLeverReplayAuditAuthorityFlags=field(default_factory=ObjectLeverReplayAuditAuthorityFlags); metadata: Mapping[str,Any]=field(default_factory=lambda: MappingProxyType({}))
    def __post_init__(self) -> None:
        e=InvalidObjectLeverAuditSnapshotError; _nonempty(self.snapshot_id,"snapshot_id",e)
        if self.audit_snapshot_kind not in OBJECT_LEVER_AUDIT_SNAPSHOT_KINDS: raise e("invalid audit_snapshot_kind")
        if self.command_family != OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY: raise e("invalid command_family")
        if not isinstance(self.source_reference,ObjectLeverReplayAuditSourceRef): raise e("invalid source_reference")
        if not isinstance(self.eligibility,ObjectLeverReplayAuditEligibility): raise e("invalid eligibility")
        expected_kind=_AUDIT_STATUS_TO_SNAPSHOT_KIND.get(self.eligibility.eligibility_status)
        if expected_kind is not None and self.audit_snapshot_kind != expected_kind: raise e("audit_snapshot_kind is not coherent with eligibility_status")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
        if not isinstance(self.deterministic_source_fields, Mapping): raise e("deterministic_source_fields must be a mapping")
        _no_forbidden(self.deterministic_source_fields,"deterministic_source_fields",e); _json(self.deterministic_source_fields,"deterministic_source_fields",e)
        object.__setattr__(self,"deterministic_source_fields",MappingProxyType(copy.deepcopy(dict(self.deterministic_source_fields))))
        if self.audit_identity is not None and (not isinstance(self.audit_identity,str) or not self.audit_identity): raise e("audit_identity must be a non-empty string or None")
        _nonempty(self.non_authority_note,"non_authority_note",e)
        if not isinstance(self.authority_flags,ObjectLeverReplayAuditAuthorityFlags): raise e("invalid authority_flags")
        object.__setattr__(self,"metadata",_meta(self.metadata,e))
    def to_dict(self) -> dict[str,Any]: return {"snapshot_id":self.snapshot_id,"audit_snapshot_kind":self.audit_snapshot_kind,"command_family":self.command_family,"source_reference":self.source_reference.to_dict(),"eligibility":self.eligibility.to_dict(),"safe_reference_ids":list(self.safe_reference_ids),"deterministic_source_fields":copy.deepcopy(dict(self.deterministic_source_fields)),"audit_identity":self.audit_identity,"non_authority_note":self.non_authority_note,"authority_flags":self.authority_flags.to_dict(),"metadata":copy.deepcopy(dict(self.metadata))}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverReplayCheckReceipt:
    receipt_id: str; replay_check_kind: str; command_family: str; audit_snapshot_id: str; source_reference_ids: Mapping[str,str]=field(default_factory=lambda: MappingProxyType({})); replay_check_status: str; audit_identity: str | None=None; expected_audit_identity: str | None=None; identity_matches: bool=False; non_authority_note: str=OBJECT_LEVER_REPLAY_AUDIT_NON_AUTHORITY_NOTE; authority_flags: ObjectLeverReplayAuditAuthorityFlags=field(default_factory=ObjectLeverReplayAuditAuthorityFlags); metadata: Mapping[str,Any]=field(default_factory=lambda: MappingProxyType({}))
    def __post_init__(self) -> None:
        e=InvalidObjectLeverReplayCheckReceiptError; _nonempty(self.receipt_id,"receipt_id",e)
        if self.replay_check_kind not in OBJECT_LEVER_REPLAY_CHECK_KINDS: raise e("invalid replay_check_kind")
        if self.command_family != OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY: raise e("invalid command_family")
        _nonempty(self.audit_snapshot_id,"audit_snapshot_id",e)
        object.__setattr__(self,"source_reference_ids",_mapping_str_str(self.source_reference_ids,"source_reference_ids",e))
        if self.replay_check_status not in OBJECT_LEVER_REPLAY_AUDIT_STATUSES: raise e("invalid replay_check_status")
        if self.audit_identity is not None and (not isinstance(self.audit_identity,str) or not self.audit_identity): raise e("audit_identity must be a non-empty string or None")
        if self.expected_audit_identity is not None and (not isinstance(self.expected_audit_identity,str) or not self.expected_audit_identity): raise e("expected_audit_identity must be a non-empty string or None")
        if not isinstance(self.identity_matches, bool): raise e("identity_matches must be a boolean")
        _nonempty(self.non_authority_note,"non_authority_note",e)
        if not isinstance(self.authority_flags,ObjectLeverReplayAuditAuthorityFlags): raise e("invalid authority_flags")
        object.__setattr__(self,"metadata",_meta(self.metadata,e))
    def to_dict(self) -> dict[str,Any]: return {"receipt_id":self.receipt_id,"replay_check_kind":self.replay_check_kind,"command_family":self.command_family,"audit_snapshot_id":self.audit_snapshot_id,"source_reference_ids":dict(self.source_reference_ids),"replay_check_status":self.replay_check_status,"audit_identity":self.audit_identity,"expected_audit_identity":self.expected_audit_identity,"identity_matches":self.identity_matches,"non_authority_note":self.non_authority_note,"authority_flags":self.authority_flags.to_dict(),"metadata":copy.deepcopy(dict(self.metadata))}

@dataclass(frozen=True, kw_only=True)
class ObjectLeverReplayAuditResult:
    result_id: str; audit_status: str; audit_decision: str; audit_snapshot: ObjectLeverAuditSnapshot | None=None; replay_check_receipt: ObjectLeverReplayCheckReceipt | None=None; block_reasons: tuple[str,...]=(); safe_reference_ids: tuple[str,...]=(); non_authority_note: str=OBJECT_LEVER_REPLAY_AUDIT_NON_AUTHORITY_NOTE; authority_flags: ObjectLeverReplayAuditAuthorityFlags=field(default_factory=ObjectLeverReplayAuditAuthorityFlags); metadata: Mapping[str,Any]=field(default_factory=lambda: MappingProxyType({}))
    def __post_init__(self) -> None:
        e=InvalidObjectLeverReplayAuditResultError; _nonempty(self.result_id,"result_id",e)
        if self.audit_status not in OBJECT_LEVER_REPLAY_AUDIT_STATUSES: raise e("invalid audit_status")
        if self.audit_decision not in OBJECT_LEVER_REPLAY_AUDIT_DECISIONS: raise e("invalid audit_decision")
        expected_decision=_AUDIT_STATUS_TO_DECISION.get(self.audit_status)
        if expected_decision is None or self.audit_decision != expected_decision: raise e("audit_status and audit_decision are not coherent")
        if self.audit_status == "audit_verified":
            if self.audit_snapshot is None: raise e("verified audit_status requires audit_snapshot")
            if self.replay_check_receipt is None: raise e("verified audit_status requires replay_check_receipt")
        if self.audit_snapshot is not None and not isinstance(self.audit_snapshot,ObjectLeverAuditSnapshot): raise e("invalid audit_snapshot")
        if self.replay_check_receipt is not None and not isinstance(self.replay_check_receipt,ObjectLeverReplayCheckReceipt): raise e("invalid replay_check_receipt")
        object.__setattr__(self,"block_reasons",_tuple(self.block_reasons,"block_reasons",e))
        for r in self.block_reasons:
            if r not in OBJECT_LEVER_REPLAY_AUDIT_BLOCK_REASONS: raise e(f"invalid block_reason {r!r}")
        object.__setattr__(self,"safe_reference_ids",_tuple(self.safe_reference_ids,"safe_reference_ids",e))
        _nonempty(self.non_authority_note,"non_authority_note",e)
        if not isinstance(self.authority_flags,ObjectLeverReplayAuditAuthorityFlags): raise e("invalid authority_flags")
        object.__setattr__(self,"metadata",_meta(self.metadata,e))
    def to_dict(self) -> dict[str,Any]: return {"result_id":self.result_id,"audit_status":self.audit_status,"audit_decision":self.audit_decision,"audit_snapshot":None if self.audit_snapshot is None else self.audit_snapshot.to_dict(),"replay_check_receipt":None if self.replay_check_receipt is None else self.replay_check_receipt.to_dict(),"block_reasons":list(self.block_reasons),"safe_reference_ids":list(self.safe_reference_ids),"non_authority_note":self.non_authority_note,"authority_flags":self.authority_flags.to_dict(),"metadata":copy.deepcopy(dict(self.metadata))}

def create_object_lever_replay_audit_authority_flags(): return ObjectLeverReplayAuditAuthorityFlags()
def create_object_lever_replay_audit_source_ref(**kw): return ObjectLeverReplayAuditSourceRef(**kw)
def create_object_lever_replay_audit_eligibility(**kw): return ObjectLeverReplayAuditEligibility(**kw)
def create_object_lever_audit_snapshot(**kw): return ObjectLeverAuditSnapshot(**kw)
def create_object_lever_replay_check_receipt(**kw): return ObjectLeverReplayCheckReceipt(**kw)
def create_object_lever_replay_audit_result(**kw): return ObjectLeverReplayAuditResult(**kw)

def validate_object_lever_replay_audit_authority_flags(v) -> bool:
    if not isinstance(v,ObjectLeverReplayAuditAuthorityFlags): return False
    return all(getattr(v,f) is False for f in v.__dataclass_fields__)
def validate_object_lever_replay_audit_source_ref(v) -> bool:
    if not isinstance(v,ObjectLeverReplayAuditSourceRef): return False
    if v.command_family != OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY: return False
    if v.commit_status not in OBJECT_LEVER_COMMIT_STATUSES: return False
    if v.commit_decision not in OBJECT_LEVER_COMMIT_DECISIONS: return False
    expected=_COMMIT_STATUS_TO_DECISION.get(v.commit_status)
    if expected is None or v.commit_decision != expected: return False
    return isinstance(v.safe_reference_ids, tuple) and isinstance(v.commit_block_reasons, tuple)
def validate_object_lever_replay_audit_eligibility(v) -> bool:
    if not isinstance(v,ObjectLeverReplayAuditEligibility): return False
    if v.command_family != OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY: return False
    if v.eligibility_status not in OBJECT_LEVER_REPLAY_AUDIT_STATUSES: return False
    if v.commit_status not in OBJECT_LEVER_COMMIT_STATUSES: return False
    if v.commit_decision not in OBJECT_LEVER_COMMIT_DECISIONS: return False
    expected=_COMMIT_STATUS_TO_DECISION.get(v.commit_status)
    if expected is None or v.commit_decision != expected: return False
    if not isinstance(v.block_reasons, tuple) or not isinstance(v.safe_reference_ids, tuple): return False
    return all(r in OBJECT_LEVER_REPLAY_AUDIT_BLOCK_REASONS for r in v.block_reasons)
def validate_object_lever_audit_snapshot(v) -> bool:
    if not isinstance(v,ObjectLeverAuditSnapshot): return False
    if v.audit_snapshot_kind not in OBJECT_LEVER_AUDIT_SNAPSHOT_KINDS: return False
    if v.command_family != OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY: return False
    if not validate_object_lever_replay_audit_source_ref(v.source_reference): return False
    if not validate_object_lever_replay_audit_eligibility(v.eligibility): return False
    if not validate_object_lever_replay_audit_authority_flags(v.authority_flags): return False
    try: _no_forbidden(v.metadata,"metadata",InvalidObjectLeverAuditSnapshotError); _json(v.metadata,"metadata",InvalidObjectLeverAuditSnapshotError)
    except InvalidObjectLeverAuditSnapshotError: return False
    return True
def validate_object_lever_replay_check_receipt(v) -> bool:
    if not isinstance(v,ObjectLeverReplayCheckReceipt): return False
    if v.replay_check_kind not in OBJECT_LEVER_REPLAY_CHECK_KINDS: return False
    if v.command_family != OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY: return False
    if v.replay_check_status not in OBJECT_LEVER_REPLAY_AUDIT_STATUSES: return False
    if not validate_object_lever_replay_audit_authority_flags(v.authority_flags): return False
    try: _no_forbidden(v.metadata,"metadata",InvalidObjectLeverReplayCheckReceiptError); _json(v.metadata,"metadata",InvalidObjectLeverReplayCheckReceiptError)
    except InvalidObjectLeverReplayCheckReceiptError: return False
    return True
def validate_object_lever_replay_audit_result(v) -> bool:
    if not isinstance(v,ObjectLeverReplayAuditResult): return False
    if v.audit_status not in OBJECT_LEVER_REPLAY_AUDIT_STATUSES: return False
    if v.audit_decision not in OBJECT_LEVER_REPLAY_AUDIT_DECISIONS: return False
    expected=_AUDIT_STATUS_TO_DECISION.get(v.audit_status)
    if expected is None or v.audit_decision != expected: return False
    if v.audit_snapshot is not None and not validate_object_lever_audit_snapshot(v.audit_snapshot): return False
    if v.replay_check_receipt is not None and not validate_object_lever_replay_check_receipt(v.replay_check_receipt): return False
    if v.audit_status == "audit_verified" and (v.audit_snapshot is None or v.replay_check_receipt is None): return False
    if not isinstance(v.block_reasons, tuple) or not isinstance(v.safe_reference_ids, tuple): return False
    if not all(r in OBJECT_LEVER_REPLAY_AUDIT_BLOCK_REASONS for r in v.block_reasons): return False
    if not validate_object_lever_replay_audit_authority_flags(v.authority_flags): return False
    try: _no_forbidden(v.metadata,"metadata",InvalidObjectLeverReplayAuditResultError); _json(v.metadata,"metadata",InvalidObjectLeverReplayAuditResultError)
    except InvalidObjectLeverReplayAuditResultError: return False
    return True

def _has_required_object_lever_safe_references(safe_reference_ids: Sequence[str]) -> bool:
    if len(safe_reference_ids) < 3: return False
    lowered = tuple(ref.lower() for ref in safe_reference_ids)
    has_scene = any(ref.startswith("scene") or ":scene" in ref for ref in lowered)
    has_actor = any(ref.startswith("actor") or ":actor" in ref for ref in lowered)
    has_object_lever = any(ref.startswith("object_lever") or ref.startswith("lever") or ":object_lever" in ref or ":lever" in ref for ref in lowered)
    return has_scene and has_actor and has_object_lever

def _compute_audit_identity(payload: Mapping[str,Any]) -> str:
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"

def _command_family_from_commit_result(commit_result: object) -> str:
    cf=getattr(commit_result,"command_family",None)
    if cf: return cf
    record=getattr(commit_result,"committed_event_record",None)
    if isinstance(record,ObjectLeverCommittedEventRecord): return record.command_family
    receipt=getattr(commit_result,"state_delta_receipt",None)
    if isinstance(receipt,ObjectLeverStateDeltaReceipt): return receipt.command_family
    return OBJECT_LEVER_COMMIT_COMMAND_FAMILY

def build_object_lever_replay_audit_source_ref(commit_result: ObjectLeverEventCommitResult) -> ObjectLeverReplayAuditSourceRef:
    if not hasattr(commit_result,"result_id") or not hasattr(commit_result,"commit_status") or not hasattr(commit_result,"commit_decision"): raise InvalidObjectLeverReplayAuditSourceRefError("commit_result must expose result_id, commit_status, commit_decision")
    record_id = getattr(commit_result.committed_event_record,"committed_event_id",None) if isinstance(getattr(commit_result,"committed_event_record",None),ObjectLeverCommittedEventRecord) else None
    receipt_id = getattr(commit_result.state_delta_receipt,"state_delta_receipt_id",None) if isinstance(getattr(commit_result,"state_delta_receipt",None),ObjectLeverStateDeltaReceipt) else None
    cf=_command_family_from_commit_result(commit_result)
    return ObjectLeverReplayAuditSourceRef(commit_result_id=commit_result.result_id, committed_event_id=record_id, state_delta_receipt_id=receipt_id, command_family=cf, commit_status=commit_result.commit_status, commit_decision=commit_result.commit_decision, safe_reference_ids=tuple(getattr(commit_result,"safe_reference_ids",())), commit_block_reasons=tuple(getattr(commit_result,"block_reasons",())))

def evaluate_object_lever_replay_audit_eligibility(source_reference: ObjectLeverReplayAuditSourceRef) -> ObjectLeverReplayAuditEligibility:
    if not isinstance(source_reference,ObjectLeverReplayAuditSourceRef): raise InvalidObjectLeverReplayAuditEligibilityError("source_reference must be ObjectLeverReplayAuditSourceRef")
    reasons=[]; status="audit_ready"
    if source_reference.command_family != OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY:
        status="audit_blocked"; reasons.append("invalid_command_family")
    if source_reference.commit_status == "committed":
        if source_reference.commit_block_reasons:
            status="audit_blocked"; reasons.append("commit_blocked")
    elif source_reference.commit_status == "commit_blocked":
        status="audit_blocked"; reasons.append("commit_blocked")
    elif source_reference.commit_status == "commit_deferred":
        status="audit_deferred"; reasons.append("commit_deferred")
    elif source_reference.commit_status == "commit_unknown":
        status="audit_unknown"; reasons.append("commit_unknown")
    elif source_reference.commit_status == "commit_insufficient_preview":
        status="audit_insufficient_commit"; reasons.append("commit_insufficient")
    else:
        status="audit_unknown"; reasons.append("commit_unknown")
    if not _has_required_object_lever_safe_references(source_reference.safe_reference_ids):
        if status == "audit_ready": status="audit_blocked"
        reasons.append("missing_safe_references")
    return ObjectLeverReplayAuditEligibility(command_family=OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, eligibility_status=status, commit_status=source_reference.commit_status, commit_decision=source_reference.commit_decision, block_reasons=tuple(dict.fromkeys(reasons)), safe_reference_ids=source_reference.safe_reference_ids)

def build_object_lever_audit_snapshot(eligibility: ObjectLeverReplayAuditEligibility, source_reference: ObjectLeverReplayAuditSourceRef, *, snapshot_id: str | None=None, event_record_kind: str | None=None, state_delta_kind: str | None=None, metadata: Mapping[str,Any] | None=None) -> ObjectLeverAuditSnapshot:
    if not isinstance(eligibility,ObjectLeverReplayAuditEligibility): raise InvalidObjectLeverAuditSnapshotError("eligibility must be ObjectLeverReplayAuditEligibility")
    if not isinstance(source_reference,ObjectLeverReplayAuditSourceRef): raise InvalidObjectLeverAuditSnapshotError("source_reference must be ObjectLeverReplayAuditSourceRef")
    snapshot_kind=_AUDIT_STATUS_TO_SNAPSHOT_KIND.get(eligibility.eligibility_status)
    if snapshot_kind is None: snapshot_kind="object_lever_unknown_event_audit_snapshot"
    sid=snapshot_id or f"audit-snapshot:{source_reference.commit_result_id}"
    deterministic_fields={"commit_result_id":source_reference.commit_result_id,"commit_status":source_reference.commit_status,"commit_decision":source_reference.commit_decision,"event_record_kind":event_record_kind,"state_delta_kind":state_delta_kind,"command_family":source_reference.command_family,"safe_reference_ids":list(source_reference.safe_reference_ids),"commit_block_reasons":list(source_reference.commit_block_reasons)}
    audit_identity=_compute_audit_identity(deterministic_fields)
    return ObjectLeverAuditSnapshot(snapshot_id=sid, audit_snapshot_kind=snapshot_kind, command_family=OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, source_reference=source_reference, eligibility=eligibility, safe_reference_ids=source_reference.safe_reference_ids, deterministic_source_fields=deterministic_fields, audit_identity=audit_identity, metadata=metadata)

def build_object_lever_replay_check_receipt(snapshot: ObjectLeverAuditSnapshot, *, expected_audit_identity: str | None=None, receipt_id: str | None=None, metadata: Mapping[str,Any] | None=None) -> ObjectLeverReplayCheckReceipt:
    if not isinstance(snapshot,ObjectLeverAuditSnapshot): raise InvalidObjectLeverReplayCheckReceiptError("snapshot must be ObjectLeverAuditSnapshot")
    replay_check_kind=_AUDIT_STATUS_TO_REPLAY_CHECK_KIND.get(snapshot.eligibility.eligibility_status)
    if replay_check_kind is None: replay_check_kind="object_lever_unknown_event_replay_check"
    rid=receipt_id or f"replay-check:{snapshot.snapshot_id}"
    source_ids={"commit_result_id":snapshot.source_reference.commit_result_id}
    if snapshot.source_reference.committed_event_id: source_ids["committed_event_id"]=snapshot.source_reference.committed_event_id
    if snapshot.source_reference.state_delta_receipt_id: source_ids["state_delta_receipt_id"]=snapshot.source_reference.state_delta_receipt_id
    expected = expected_audit_identity if expected_audit_identity is not None else snapshot.audit_identity
    identity_matches = snapshot.audit_identity is not None and snapshot.audit_identity == expected
    return ObjectLeverReplayCheckReceipt(receipt_id=rid, replay_check_kind=replay_check_kind, command_family=OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY, audit_snapshot_id=snapshot.snapshot_id, source_reference_ids=source_ids, replay_check_status=snapshot.eligibility.eligibility_status, audit_identity=snapshot.audit_identity, expected_audit_identity=expected, identity_matches=identity_matches, metadata=metadata)

def audit_object_lever_event_commit_result(commit_result: object, *, result_id: str | None=None, expected_audit_identity: str | None=None, metadata: Mapping[str,Any] | None=None) -> ObjectLeverReplayAuditResult:
    if not hasattr(commit_result,"result_id") or not hasattr(commit_result,"commit_status") or not hasattr(commit_result,"commit_decision"): raise InvalidObjectLeverReplayAuditResultError("commit_result must expose result_id, commit_status, commit_decision")
    cf=_command_family_from_commit_result(commit_result)
    if cf != OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY:
        return ObjectLeverReplayAuditResult(result_id=result_id or "audit:invalid", audit_status="audit_blocked", audit_decision="blocked", block_reasons=("invalid_command_family",), safe_reference_ids=(), metadata=metadata)
    source=build_object_lever_replay_audit_source_ref(commit_result)
    elig=evaluate_object_lever_replay_audit_eligibility(source)
    reasons=list(elig.block_reasons)
    status=elig.eligibility_status
    decision=_AUDIT_STATUS_TO_DECISION.get(status)
    snapshot=None; receipt=None
    if status == "audit_ready":
        record=getattr(commit_result,"committed_event_record",None)
        receipt_obj=getattr(commit_result,"state_delta_receipt",None)
        if record is None:
            status="audit_blocked"; decision="blocked"; reasons.append("missing_committed_event_record")
        elif receipt_obj is None:
            status="audit_blocked"; decision="blocked"; reasons.append("missing_state_delta_receipt")
        elif getattr(commit_result,"block_reasons",()):
            status="audit_blocked"; decision="blocked"; reasons.append("commit_blocked")
        else:
            event_kind=getattr(record,"event_record_kind",None)
            delta_kind=getattr(receipt_obj,"state_delta_kind",None)
            snapshot=build_object_lever_audit_snapshot(elig, source, event_record_kind=event_kind, state_delta_kind=delta_kind, metadata=metadata)
            receipt=build_object_lever_replay_check_receipt(snapshot, expected_audit_identity=expected_audit_identity or snapshot.audit_identity, metadata=metadata)
            if expected_audit_identity is not None and snapshot.audit_identity != expected_audit_identity:
                status="audit_blocked"; decision="blocked"; reasons.append("audit_identity_mismatch")
            else:
                status="audit_verified"; decision="object_lever_audit_verified"
    reasons=tuple(dict.fromkeys(reasons))
    safe=tuple(source.safe_reference_ids)
    return ObjectLeverReplayAuditResult(result_id=result_id or f"audit:{source.commit_result_id}", audit_status=status, audit_decision=decision, audit_snapshot=snapshot, replay_check_receipt=receipt, block_reasons=reasons, safe_reference_ids=safe, metadata=metadata)

def serialize_object_lever_audit_snapshot(s: ObjectLeverAuditSnapshot) -> dict[str,Any]:
    if not validate_object_lever_audit_snapshot(s): raise InvalidObjectLeverAuditSnapshotError("invalid snapshot")
    return s.to_dict()
def serialize_object_lever_audit_snapshot_visible(s: ObjectLeverAuditSnapshot) -> dict[str,Any]:
    if not validate_object_lever_audit_snapshot(s): raise InvalidObjectLeverAuditSnapshotError("invalid snapshot")
    return {"snapshot_id":s.snapshot_id,"audit_snapshot_kind":s.audit_snapshot_kind,"command_family":s.command_family,"safe_reference_ids":list(s.safe_reference_ids),"audit_identity":s.audit_identity}
def serialize_object_lever_replay_check_receipt(r: ObjectLeverReplayCheckReceipt) -> dict[str,Any]:
    if not validate_object_lever_replay_check_receipt(r): raise InvalidObjectLeverReplayCheckReceiptError("invalid receipt")
    return r.to_dict()
def serialize_object_lever_replay_check_receipt_visible(r: ObjectLeverReplayCheckReceipt) -> dict[str,Any]:
    if not validate_object_lever_replay_check_receipt(r): raise InvalidObjectLeverReplayCheckReceiptError("invalid receipt")
    return {"receipt_id":r.receipt_id,"replay_check_kind":r.replay_check_kind,"command_family":r.command_family,"audit_snapshot_id":r.audit_snapshot_id,"source_reference_ids":dict(r.source_reference_ids),"replay_check_status":r.replay_check_status,"audit_identity":r.audit_identity,"identity_matches":r.identity_matches}
def serialize_object_lever_replay_audit_result(r: ObjectLeverReplayAuditResult) -> dict[str,Any]:
    if not validate_object_lever_replay_audit_result(r): raise InvalidObjectLeverReplayAuditResultError("invalid result")
    return r.to_dict()
def serialize_object_lever_replay_audit_result_visible(r: ObjectLeverReplayAuditResult) -> dict[str,Any]:
    if not validate_object_lever_replay_audit_result(r): raise InvalidObjectLeverReplayAuditResultError("invalid result")
    c=r.audit_snapshot; d=r.replay_check_receipt
    return {"result_id":r.result_id,"audit_status":r.audit_status,"audit_decision":r.audit_decision,"audit_snapshot_kind":None if c is None else c.audit_snapshot_kind,"replay_check_kind":None if d is None else d.replay_check_kind,"command_family":OBJECT_LEVER_REPLAY_AUDIT_COMMAND_FAMILY,"safe_reference_ids":list(r.safe_reference_ids),"block_reasons":list(r.block_reasons),"audit_identity":None if c is None else c.audit_identity,"identity_matches":None if d is None else d.identity_matches}

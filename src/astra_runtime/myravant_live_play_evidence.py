"""Bounded nonauthoritative live-play evidence capture for Myravant terminal play.

This module records observable session and interaction evidence only. It does not
own authoritative state, command resolution, commitment, persistence, replay,
failure classification, semantic ownership, canon, or gameplay outcomes.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TRACE_FORMAT_IDENTITY = "myravant.live_play_evidence"
TRACE_FORMAT_VERSION = 1
CLIENT_ID = "myravant-terminal-g3"
CLIENT_MODE = "CLIENT-TEXT-V1"
MODEL_MODE = "MODEL-NONE"


class LivePlayEvidenceError(ValueError):
    """Base error for bounded live-play evidence capture."""


class InvalidLivePlayEvidenceError(LivePlayEvidenceError):
    """Raised when evidence material is structurally invalid."""


class LivePlayEvidenceWriteError(LivePlayEvidenceError):
    """Raised when evidence bytes cannot be written."""


def _require_non_empty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidLivePlayEvidenceError(
            f"{name} must be a non-empty string"
        )
    return value


def _optional_non_empty(value: object, name: str) -> str | None:
    if value is None:
        return None
    return _require_non_empty(value, name)


def _require_digest(value: object, name: str) -> str:
    value = _require_non_empty(value, name)
    if len(value) != 64 or any(
        char not in "0123456789abcdef"
        for char in value
    ):
        raise InvalidLivePlayEvidenceError(
            f"{name} must be a lowercase SHA-256 digest"
        )
    return value


def _require_repository_sha(value: object) -> str:
    value = _require_non_empty(value, "repository_sha")
    if value == "unknown":
        return value
    if len(value) != 40 or any(
        char not in "0123456789abcdef"
        for char in value
    ):
        raise InvalidLivePlayEvidenceError(
            "repository_sha must be a 40-character lowercase Git SHA "
            "or exactly 'unknown'"
        )
    return value


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_repository_sha(
    repo_root: str | os.PathLike[str] | None = None,
) -> str:
    """Resolve a repository SHA without making it gameplay-authoritative."""

    configured = os.environ.get("MYRAVANT_REPOSITORY_SHA")
    if configured and configured.strip():
        return configured.strip()

    root = (
        Path(repo_root)
        if repo_root is not None
        else Path(__file__).resolve().parents[2]
    )

    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"

    sha = completed.stdout.strip()
    return sha or "unknown"


@dataclass(frozen=True, kw_only=True)
class LivePlaySessionHeader:
    session_id: str
    campaign_id: str
    repository_sha: str
    started_at: str
    initial_state_digest: str
    restore_performed: bool
    debug_mode: bool = False
    client_id: str = CLIENT_ID
    client_mode: str = CLIENT_MODE
    model_mode: str = MODEL_MODE
    environment_id: str | None = None
    network_mode: str | None = None
    operating_system: str = ""
    architecture: str = ""

    def __post_init__(self) -> None:
        _require_non_empty(self.session_id, "session_id")
        _require_non_empty(self.campaign_id, "campaign_id")
        _require_repository_sha(self.repository_sha)
        _require_non_empty(self.started_at, "started_at")
        _require_digest(
            self.initial_state_digest,
            "initial_state_digest",
        )
        if type(self.restore_performed) is not bool:
            raise InvalidLivePlayEvidenceError(
                "restore_performed must be bool"
            )
        if type(self.debug_mode) is not bool:
            raise InvalidLivePlayEvidenceError(
                "debug_mode must be bool"
            )
        _require_non_empty(self.client_id, "client_id")
        _require_non_empty(self.client_mode, "client_mode")
        _require_non_empty(self.model_mode, "model_mode")
        _optional_non_empty(self.environment_id, "environment_id")
        _optional_non_empty(self.network_mode, "network_mode")

    def to_record(self) -> dict[str, object]:
        return {
            "record_type": "session_start",
            "trace_format_identity": TRACE_FORMAT_IDENTITY,
            "trace_format_version": TRACE_FORMAT_VERSION,
            "evidence_only": True,
            "authority_effect": "none",
            "session_id": self.session_id,
            "campaign_id": self.campaign_id,
            "repository_sha": self.repository_sha,
            "started_at": self.started_at,
            "initial_state_digest": self.initial_state_digest,
            "restore_performed": self.restore_performed,
            "debug_mode": self.debug_mode,
            "client_id": self.client_id,
            "client_mode": self.client_mode,
            "model_mode": self.model_mode,
            "environment_id": self.environment_id,
            "network_mode": self.network_mode,
            "operating_system": self.operating_system,
            "architecture": self.architecture,
            "human_intervention": False,
        }


@dataclass(frozen=True, kw_only=True)
class LivePlayInteractionRecord:
    session_id: str
    sequence: int
    timestamp: str
    raw_player_input: str
    parsed_action: str
    parsed_argument: str | None
    player_visible_output: str
    result_type: str
    authoritative_changed: bool
    command_id: str | None = None
    command_fingerprint: str | None = None
    preview_id: str | None = None
    receipt_id: str | None = None
    state_delta_id: str | None = None
    spatial_evidence_id: str | None = None
    opportunity_evidence_id: str | None = None
    pre_state_digest: str | None = None
    post_state_digest: str | None = None
    checkpoint_digest: str | None = None
    failure_class: str | None = None

    def __post_init__(self) -> None:
        _require_non_empty(self.session_id, "session_id")
        if type(self.sequence) is not int or self.sequence < 1:
            raise InvalidLivePlayEvidenceError(
                "sequence must be a positive integer"
            )
        _require_non_empty(self.timestamp, "timestamp")
        if not isinstance(self.raw_player_input, str):
            raise InvalidLivePlayEvidenceError(
                "raw_player_input must be str"
            )
        _require_non_empty(self.parsed_action, "parsed_action")
        _optional_non_empty(self.parsed_argument, "parsed_argument")
        if not isinstance(self.player_visible_output, str):
            raise InvalidLivePlayEvidenceError(
                "player_visible_output must be str"
            )
        _require_non_empty(self.result_type, "result_type")
        if type(self.authoritative_changed) is not bool:
            raise InvalidLivePlayEvidenceError(
                "authoritative_changed must be bool"
            )

        for name in (
            "command_id",
            "preview_id",
            "receipt_id",
            "state_delta_id",
            "spatial_evidence_id",
            "opportunity_evidence_id",
            "failure_class",
        ):
            _optional_non_empty(getattr(self, name), name)

        if self.command_fingerprint is not None:
            _require_digest(
                self.command_fingerprint,
                "command_fingerprint",
            )

        for name in (
            "pre_state_digest",
            "post_state_digest",
            "checkpoint_digest",
        ):
            value = getattr(self, name)
            if value is not None:
                _require_digest(value, name)

    def to_record(self) -> dict[str, object]:
        return {
            "record_type": "interaction",
            "evidence_only": True,
            "authority_effect": "none",
            "session_id": self.session_id,
            "sequence": self.sequence,
            "timestamp": self.timestamp,
            "raw_player_input": self.raw_player_input,
            "parsed_action": self.parsed_action,
            "parsed_argument": self.parsed_argument,
            "player_visible_output": self.player_visible_output,
            "result_type": self.result_type,
            "authoritative_changed": self.authoritative_changed,
            "command_id": self.command_id,
            "command_fingerprint": self.command_fingerprint,
            "preview_id": self.preview_id,
            "receipt_id": self.receipt_id,
            "state_delta_id": self.state_delta_id,
            "spatial_evidence_id": self.spatial_evidence_id,
            "opportunity_evidence_id": self.opportunity_evidence_id,
            "pre_state_digest": self.pre_state_digest,
            "post_state_digest": self.post_state_digest,
            "checkpoint_digest": self.checkpoint_digest,
            "failure_class": self.failure_class,
        }


@dataclass(frozen=True, kw_only=True)
class LivePlaySessionReceipt:
    session_id: str
    ended_at: str
    final_state_digest: str
    meaningful_interactions: int
    committed_transitions: int
    unsupported_or_rejected: int
    checkpoints_written: int
    trace_write_failures: int
    evidence_complete: bool

    def to_record(self) -> dict[str, object]:
        return {
            "record_type": "session_end",
            "evidence_only": True,
            "authority_effect": "none",
            "session_id": self.session_id,
            "ended_at": self.ended_at,
            "final_state_digest": self.final_state_digest,
            "meaningful_interactions": self.meaningful_interactions,
            "committed_transitions": self.committed_transitions,
            "unsupported_or_rejected": self.unsupported_or_rejected,
            "checkpoints_written": self.checkpoints_written,
            "trace_write_failures": self.trace_write_failures,
            "evidence_complete": self.evidence_complete,
            "human_interventions": 0,
        }


def build_live_play_session_header(
    *,
    campaign_id: str,
    initial_state_digest: str,
    repository_sha: str | None = None,
    session_id: str | None = None,
    restore_performed: bool = False,
    debug_mode: bool = False,
    environment_id: str | None = None,
    network_mode: str | None = None,
) -> LivePlaySessionHeader:
    return LivePlaySessionHeader(
        session_id=session_id or f"live-play-{uuid.uuid4()}",
        campaign_id=campaign_id,
        repository_sha=repository_sha or resolve_repository_sha(),
        started_at=utc_timestamp(),
        initial_state_digest=initial_state_digest,
        restore_performed=restore_performed,
        debug_mode=debug_mode,
        environment_id=environment_id,
        network_mode=network_mode,
        operating_system=platform.system(),
        architecture=platform.machine(),
    )


class LivePlayEvidenceRecorder:
    """Append-only local JSONL evidence writer.

    Write failure can invalidate an evaluation trace but never changes or rolls
    back authoritative runtime state.
    """

    def __init__(
        self,
        *,
        trace_path: str | os.PathLike[str],
        header: LivePlaySessionHeader,
    ) -> None:
        if not isinstance(header, LivePlaySessionHeader):
            raise InvalidLivePlayEvidenceError(
                "header must be LivePlaySessionHeader"
            )

        self.trace_path = Path(trace_path)
        self.header = header
        self._next_sequence = 1
        self._meaningful_interactions = 0
        self._committed_transitions = 0
        self._unsupported_or_rejected = 0
        self._checkpoints_written = 0
        self._trace_write_failures = 0
        self._evidence_complete = True
        self._write_disabled = False
        self._finished = False

        self._write_record(header.to_record())

    @property
    def session_id(self) -> str:
        return self.header.session_id

    @property
    def evidence_complete(self) -> bool:
        return self._evidence_complete

    @property
    def trace_write_failures(self) -> int:
        return self._trace_write_failures

    def mark_incomplete(self) -> None:
        """Mark this evaluation trace incomplete without affecting play."""
        self._evidence_complete = False

    def _append_record(self, record: dict[str, object]) -> None:
        parent = self.trace_path.parent
        if not parent.exists() or not parent.is_dir():
            raise OSError("trace parent directory does not exist")

        material = json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )

        with self.trace_path.open("a", encoding="utf-8") as handle:
            handle.write(material + "\n")
            handle.flush()

    def _write_record(self, record: dict[str, object]) -> None:
        if self._write_disabled:
            return

        try:
            self._append_record(record)
        except (OSError, TypeError, ValueError) as exc:
            self._trace_write_failures += 1
            self._evidence_complete = False
            self._write_disabled = True
            raise LivePlayEvidenceWriteError(
                "live-play evidence write failed; authoritative state "
                "must remain unchanged"
            ) from exc

    def record_interaction(
        self,
        *,
        raw_player_input: str,
        parsed_action: str,
        parsed_argument: str | None,
        player_visible_output: str,
        result_type: str,
        authoritative_changed: bool,
        command_id: str | None = None,
        command_fingerprint: str | None = None,
        preview_id: str | None = None,
        receipt_id: str | None = None,
        state_delta_id: str | None = None,
        spatial_evidence_id: str | None = None,
        opportunity_evidence_id: str | None = None,
        pre_state_digest: str | None = None,
        post_state_digest: str | None = None,
        checkpoint_digest: str | None = None,
        failure_class: str | None = None,
    ) -> LivePlayInteractionRecord:
        if self._finished:
            raise InvalidLivePlayEvidenceError(
                "cannot record interaction after session finish"
            )

        record = LivePlayInteractionRecord(
            session_id=self.session_id,
            sequence=self._next_sequence,
            timestamp=utc_timestamp(),
            raw_player_input=raw_player_input,
            parsed_action=parsed_action,
            parsed_argument=parsed_argument,
            player_visible_output=player_visible_output,
            result_type=result_type,
            authoritative_changed=authoritative_changed,
            command_id=command_id,
            command_fingerprint=command_fingerprint,
            preview_id=preview_id,
            receipt_id=receipt_id,
            state_delta_id=state_delta_id,
            spatial_evidence_id=spatial_evidence_id,
            opportunity_evidence_id=opportunity_evidence_id,
            pre_state_digest=pre_state_digest,
            post_state_digest=post_state_digest,
            checkpoint_digest=checkpoint_digest,
            failure_class=failure_class,
        )

        self._next_sequence += 1
        self._meaningful_interactions += 1

        if result_type in {
            "movement_committed",
            "custody_committed",
        }:
            self._committed_transitions += 1
        if failure_class is not None or result_type in {
            "movement_rejected",
            "custody_rejected",
            "unsupported_input",
            "checkpoint_unavailable",
        }:
            self._unsupported_or_rejected += 1
        if result_type == "checkpoint_written":
            self._checkpoints_written += 1

        self._write_record(record.to_record())
        return record

    def finish(
        self,
        *,
        final_state_digest: str,
    ) -> LivePlaySessionReceipt:
        _require_digest(final_state_digest, "final_state_digest")

        if self._finished:
            raise InvalidLivePlayEvidenceError(
                "session receipt already finalized"
            )

        self._finished = True

        receipt = LivePlaySessionReceipt(
            session_id=self.session_id,
            ended_at=utc_timestamp(),
            final_state_digest=final_state_digest,
            meaningful_interactions=self._meaningful_interactions,
            committed_transitions=self._committed_transitions,
            unsupported_or_rejected=self._unsupported_or_rejected,
            checkpoints_written=self._checkpoints_written,
            trace_write_failures=self._trace_write_failures,
            evidence_complete=self._evidence_complete,
        )

        self._write_record(receipt.to_record())
        return receipt

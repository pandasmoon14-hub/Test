from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .route import ChunkType, ChunkSizeClass, RouteName, FinalStatus


class ValidatorOutcome(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"


@dataclass(slots=True)
class ValidatorResult:
    name: str
    outcome: ValidatorOutcome
    message: str = ""
    score: float | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RetryRecord:
    attempt_number: int
    route_used: RouteName
    prompt_signature: str
    temperature: float | None = None
    max_tokens: int | None = None
    elapsed_ms: int | None = None
    failure_reason: str = ""


@dataclass(slots=True)
class ChunkRunLog:
    run_id: str
    sourcebook_id: str
    chunk_id: str
    chunk_type: ChunkType
    chunk_size_class: ChunkSizeClass
    assigned_route: RouteName
    final_route: RouteName
    model_mode: str
    model_version: str
    prompt_signature: str
    lexicon_version: str
    validator_results: list[ValidatorResult] = field(default_factory=list)
    retries: list[RetryRecord] = field(default_factory=list)
    elapsed_ms: int = 0
    token_input: int | None = None
    token_output: int | None = None
    cost_estimate_usd: float | None = None
    final_status: FinalStatus = FinalStatus.PENDING
    notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RunManifest:
    run_id: str
    started_at_utc: str
    finished_at_utc: str | None = None
    environment: str = "dev"
    source_manifest_path: str = ""
    model_mode: str = "adapter"
    model_version: str = ""
    prompt_bundle_version: str = ""
    lexicon_version: str = ""
    validator_bundle_version: str = ""
    chunk_logs: list[ChunkRunLog] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

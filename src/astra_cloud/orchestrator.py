"""
orchestrator.py

Full pipeline orchestrator for Astra Ascension conversion.

Pipeline per chunk:
  1. Classify chunk type (classifier.py)
  2. Assign conversion route (policies.py)
  3. Route to Astra doctrine layer (layer_router.py)
  4. Validate lexicon compliance (lexicon_validator.py)
  5. Validate doctrine invariants (doctrine_validator.py)
  6. Determine final status — pass / warn / quarantine / escalate
  7. Write quarantine / exception entries when required

The orchestrator does NOT call an LLM. It receives pre-converted text from
the caller and validates + routes it. Integration with LLM call sites is
the caller's responsibility.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

from astra_cloud.routing.classifier import classify_chunk
from astra_cloud.routing.layer_router import LayerRouteDecision, route_to_doctrine_layer
from astra_cloud.routing.policies import assign_route
from astra_cloud.schemas.route import ChunkFeatures, FinalStatus, RouteName
from astra_cloud.schemas.runlog import (
    ChunkRunLog,
    RunManifest,
    ValidatorOutcome,
    ValidatorResult,
)
from astra_cloud.validators import DoctrineValidator, LexiconValidator


@dataclass
class ConversionRequest:
    """Input for one chunk conversion pass through the pipeline."""
    chunk_id: str
    sourcebook_id: str
    source_text: str
    converted_text: str          # LLM-produced output supplied by caller
    prompt_signature: str = ""
    model_version: str = ""
    elapsed_ms: int = 0


@dataclass
class ConversionResult:
    """Result of processing one chunk through the full validation pipeline."""
    chunk_id: str
    sourcebook_id: str
    final_status: FinalStatus
    route_rationale: str = ""
    layer_route: LayerRouteDecision | None = None
    validator_results: list[ValidatorResult] = field(default_factory=list)
    quarantine_reasons: list[str] = field(default_factory=list)
    notes: str = ""


class ConversionOrchestrator:
    """
    Full Astra conversion pipeline orchestrator.

    Parameters
    ----------
    repo_root : Path
        Root of the AstraCloud repository (directory containing pyproject.toml).
    run_id : str | None
        Optional run identifier. Auto-generated if not supplied.
    """

    def __init__(self, repo_root: Path, run_id: str | None = None) -> None:
        self._repo_root = repo_root
        self._run_id = run_id or str(uuid.uuid4())
        self._lexicon_val = LexiconValidator(repo_root)
        self._doctrine_val = DoctrineValidator()

        self._quarantine_dir = repo_root / "data" / "quarantine"
        self._exception_dir = repo_root / "data" / "exceptions"
        self._quarantine_dir.mkdir(parents=True, exist_ok=True)
        self._exception_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(self, request: ConversionRequest) -> ConversionResult:
        """Run one converted chunk through the full validation pipeline."""

        # Step 1 — classify source text
        features: ChunkFeatures = classify_chunk(
            chunk_id=request.chunk_id,
            sourcebook_id=request.sourcebook_id,
            text=request.source_text,
        )

        # Step 2 — assign route
        route = assign_route(features)

        # Skip / preserve-raw chunks bypass validation
        if route.final_route in {RouteName.SKIP, RouteName.PRESERVE_RAW}:
            return ConversionResult(
                chunk_id=request.chunk_id,
                sourcebook_id=request.sourcebook_id,
                final_status=FinalStatus.SKIPPED,
                route_rationale=route.rationale,
                notes=f"route={route.final_route}",
            )

        # Step 3 — route to doctrine layer
        layer_route = route_to_doctrine_layer(
            chunk_id=request.chunk_id,
            chunk_type=features.chunk_type,
            text=request.converted_text,
        )

        # Step 4 — lexicon validation
        lex_result = self._lexicon_val.validate(
            chunk_id=request.chunk_id,
            converted_text=request.converted_text,
        )

        # Step 5 — doctrine invariant validation
        doc_result = self._doctrine_val.validate(
            chunk_id=request.chunk_id,
            chunk_type=features.chunk_type,
            converted_text=request.converted_text,
        )

        validator_results = [lex_result, doc_result]

        # Step 6 — final status
        quarantine_reasons: list[str] = []
        has_fail = any(v.outcome == ValidatorOutcome.FAIL for v in validator_results)

        if layer_route.escalate:
            final_status = FinalStatus.ESCALATED
            quarantine_reasons.append(layer_route.escalate_reason)
        elif layer_route.split_required:
            final_status = FinalStatus.ESCALATED
            quarantine_reasons.append(layer_route.split_rationale)
        elif has_fail:
            final_status = FinalStatus.FAILED
            quarantine_reasons.extend(
                v.message for v in validator_results
                if v.outcome == ValidatorOutcome.FAIL
            )
        else:
            final_status = FinalStatus.SUCCEEDED

        # Step 7 — persist quarantine / exception entries
        if final_status in {FinalStatus.FAILED, FinalStatus.ESCALATED}:
            self._write_quarantine(request, quarantine_reasons, validator_results)

        return ConversionResult(
            chunk_id=request.chunk_id,
            sourcebook_id=request.sourcebook_id,
            final_status=final_status,
            route_rationale=route.rationale,
            layer_route=layer_route,
            validator_results=validator_results,
            quarantine_reasons=quarantine_reasons,
        )

    def build_run_manifest(
        self,
        chunk_logs: list[ChunkRunLog],
        environment: str = "dev",
    ) -> RunManifest:
        return RunManifest(
            run_id=self._run_id,
            started_at_utc=datetime.now(timezone.utc).isoformat(),
            environment=environment,
            chunk_logs=chunk_logs,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _write_quarantine(
        self,
        request: ConversionRequest,
        reasons: list[str],
        validator_results: list[ValidatorResult],
    ) -> None:
        entry = {
            "run_id": self._run_id,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "chunk_id": request.chunk_id,
            "sourcebook_id": request.sourcebook_id,
            "quarantine_reasons": reasons,
            "validator_results": [
                {
                    "name": v.name,
                    "outcome": v.outcome.value,
                    "message": v.message,
                    "score": v.score,
                }
                for v in validator_results
            ],
        }
        out = self._quarantine_dir / f"{request.sourcebook_id}_{request.chunk_id}.yaml"
        with out.open("w", encoding="utf-8") as fh:
            yaml.dump(entry, fh, allow_unicode=True, sort_keys=False)

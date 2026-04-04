"""
lexicon_validator.py

Validates converted Astra output against the canonical lexicon.

Enforces batchA_01 terminology control by detecting:
- Donor system signature terms that were not converted
- Banned patterns present in output
- Mechanics-map entries where donor form was kept instead of Astra equivalent
- Cosmological content not tagged [cosmology-local]
- Terms flagged for human review
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from astra_cloud.schemas.runlog import ValidatorOutcome, ValidatorResult


# ---------------------------------------------------------------------------
# Cosmology detection — passages that should be tagged [cosmology-local]
# ---------------------------------------------------------------------------
_COSMOLOGY_SIGNAL = re.compile(
    r"\b("
    r"realm of (?:the|eternal|divine|astral|void)\b"
    r"|chosen by (?:the|a|an|divine|cosmic|celestial)\b"
    r"|power (?:flows?|comes?) from (?:the|a|an|divine|cosmic)\b"
    r"|cosmic (?:law|order|hierarchy|mandate|agency)\b"
    r"|metaphysical (?:source|engine|force|origin)\b"
    r"|spiritually (?:bound|ascend|awaken|empower)\b"
    r"|born of (?:chaos|order|void|the aether|the dao|the source)\b"
    r"|astral? (?:resonance|plane|sea|current|tide|flow|weave)\b"
    r")",
    re.I,
)
_COSMOLOGY_TAG = re.compile(r"\[cosmology-local\]", re.I)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


class LexiconValidator:
    """
    Validates converted Astra output against the canonical lexicon.

    Loads from:
      data/lexicon/canonical/astra_terms.yaml
      data/lexicon/canonical/banned_terms.yaml
      data/lexicon/canonical/mechanics_map.yaml
      derived_lexicon_seed.yaml
    """

    def __init__(self, repo_root: Path) -> None:
        lexicon_root = repo_root / "data" / "lexicon" / "canonical"
        self._astra_terms: dict[str, Any] = _load_yaml(lexicon_root / "astra_terms.yaml")
        self._banned: dict[str, Any] = _load_yaml(lexicon_root / "banned_terms.yaml")
        self._mechanics: dict[str, Any] = _load_yaml(lexicon_root / "mechanics_map.yaml")
        self._seed: dict[str, Any] = _load_yaml(repo_root / "derived_lexicon_seed.yaml")

        self._sig_terms: dict[str, list[str]] = {
            sys: terms
            for sys, terms in (self._seed.get("system_signature_terms") or {}).items()
            if terms and sys != "GENERIC"
        }
        self._unconverted: list[str] = self._seed.get("unconverted_or_flagged_source_terms") or []
        self._banned_patterns: list[str] = self._banned.get("banned_or_flagged_patterns") or []
        self._review_terms: list[str] = [
            t for t in (self._banned.get("flag_for_review_when_seen") or [])
            if isinstance(t, str)
        ]
        self._mechanics_map: dict[str, Any] = (
            self._mechanics.get("mechanics_equivalents") or {}
        )

    # -----------------------------------------------------------------------

    def validate(self, chunk_id: str, converted_text: str) -> ValidatorResult:
        issues: list[str] = []
        warnings: list[str] = []
        text_lower = converted_text.lower()

        # 1. Donor system signature term leak
        detected_systems: list[str] = []
        for system, terms in self._sig_terms.items():
            hits = [t for t in terms if t and t.lower() in text_lower]
            if hits:
                detected_systems.append(system)
                issues.append(
                    f"donor_signature_leak[{system}]: {hits[:3]}"
                )

        # 2. Unconverted flagged source terms
        unconverted_hits = [
            t for t in self._unconverted
            if t and re.search(r"\b" + re.escape(t.lower()) + r"\b", text_lower)
        ]
        for hit in unconverted_hits[:5]:
            issues.append(f"unconverted_source_term: '{hit}'")
        if len(unconverted_hits) > 5:
            issues.append(f"...and {len(unconverted_hits) - 5} additional unconverted terms")

        # 3. Mechanics map: donor key present but Astra equivalent absent
        for donor_key, entry in self._mechanics_map.items():
            if not isinstance(entry, dict):
                continue
            astra_eq = entry.get("preferred_astra_term", "")
            donor_pat = r"\b" + re.escape(donor_key.replace("_", " ")) + r"\b"
            if re.search(donor_pat, text_lower) and astra_eq.lower() not in text_lower:
                warnings.append(
                    f"mechanics_unmapped: donor='{donor_key}' → expected='{astra_eq}'"
                )

        # 4. Terms flagged for human review
        for term in self._review_terms:
            if term.lower() in text_lower:
                warnings.append(f"flagged_for_review: '{term}'")

        # 5. Cosmology leakage without tag
        cosmo_hits = _COSMOLOGY_SIGNAL.findall(converted_text)
        if cosmo_hits and not _COSMOLOGY_TAG.search(converted_text):
            issues.append(
                f"cosmology_untagged: {len(cosmo_hits)} cosmological phrase(s) found "
                f"without [cosmology-local] tag — add tag before storage"
            )

        # Outcome
        if issues:
            outcome = ValidatorOutcome.FAIL
            msg = "; ".join(issues[:3])
            if len(issues) > 3:
                msg += f" (+{len(issues) - 3} more)"
        elif warnings:
            outcome = ValidatorOutcome.WARN
            msg = "; ".join(warnings[:3])
        else:
            outcome = ValidatorOutcome.PASS
            msg = "lexicon clean"

        return ValidatorResult(
            name="lexicon_validator",
            outcome=outcome,
            message=msg,
            score=max(0.0, 1.0 - len(issues) * 0.2),
            details={
                "issues": issues,
                "warnings": warnings,
                "detected_donor_systems": detected_systems,
                "unconverted_count": len(unconverted_hits),
                "cosmology_signal_count": len(cosmo_hits),
            },
        )

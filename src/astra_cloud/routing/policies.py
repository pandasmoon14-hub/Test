from __future__ import annotations

from astra_cloud.schemas.route import ChunkFeatures, ChunkType, RouteDecision, RouteName


DEFAULT_ROUTES: dict[ChunkType, RouteName] = {
    ChunkType.FRONTMATTER: RouteName.PRESERVE_RAW,
    ChunkType.TOC: RouteName.PRESERVE_RAW,
    ChunkType.PROSE_LORE: RouteName.ONE_PASS_CONVERT,
    ChunkType.RULES_TEXT: RouteName.ONE_PASS_CONVERT,
    ChunkType.CLASS_FEATURE: RouteName.TWO_PASS_CONVERT,
    ChunkType.SPELL_OR_POWER: RouteName.TWO_PASS_CONVERT,
    ChunkType.ITEM_BLOCK: RouteName.ONE_PASS_CONVERT,
    ChunkType.NPC_OR_BESTIARY: RouteName.TWO_PASS_CONVERT,
    ChunkType.STATBLOCK: RouteName.GUARDED_STATBLOCK_CONVERT,
    ChunkType.TABLE_LIGHT: RouteName.DETERMINISTIC_TRANSFORM,
    ChunkType.TABLE_HEAVY: RouteName.GUARDED_TABLE_CONVERT,
    ChunkType.MIXED_DENSE: RouteName.TWO_PASS_CONVERT,
    ChunkType.APPENDIX_REFERENCE: RouteName.PRESERVE_RAW,
    ChunkType.INDEX_OR_GLOSSARY: RouteName.DETERMINISTIC_TRANSFORM,
    ChunkType.JUNK_OR_ARTIFACT: RouteName.SKIP,
}


VALIDATORS: dict[RouteName, list[str]] = {
    RouteName.SKIP: [],
    RouteName.PRESERVE_RAW: ["structure_integrity", "no_unexpected_mutation"],
    RouteName.DETERMINISTIC_TRANSFORM: ["structure_integrity", "terminology_safety", "table_integrity_if_present"],
    RouteName.ONE_PASS_CONVERT: ["structure_integrity", "terminology_consistency", "no_source_setting_leakage", "drift_limit", "completeness"],
    RouteName.TWO_PASS_CONVERT: ["structure_integrity", "terminology_consistency", "no_source_setting_leakage", "drift_limit", "completeness", "mechanical_fidelity_proxy"],
    RouteName.GUARDED_STATBLOCK_CONVERT: ["statblock_integrity", "terminology_consistency", "no_source_setting_leakage", "drift_limit"],
    RouteName.GUARDED_TABLE_CONVERT: ["table_integrity", "terminology_consistency", "no_source_setting_leakage", "drift_limit"],
    RouteName.ESCALATE_REVIEW: ["failure_packet_generation"],
}


RETRY_POLICIES: dict[RouteName, dict[str, object]] = {
    RouteName.ONE_PASS_CONVERT: {"retry_on_fail": True, "max_retries": 2, "on_fail_after_retries": RouteName.TWO_PASS_CONVERT.value},
    RouteName.TWO_PASS_CONVERT: {"retry_on_fail": True, "max_retries": 2, "on_fail_after_retries": RouteName.ESCALATE_REVIEW.value},
    RouteName.GUARDED_STATBLOCK_CONVERT: {"retry_on_fail": True, "max_retries": 1, "on_fail_after_retries": RouteName.ESCALATE_REVIEW.value},
    RouteName.GUARDED_TABLE_CONVERT: {"retry_on_fail": True, "max_retries": 1, "on_fail_after_retries": RouteName.ESCALATE_REVIEW.value},
    RouteName.DETERMINISTIC_TRANSFORM: {"retry_on_fail": False, "max_retries": 0, "on_fail_after_retries": RouteName.ESCALATE_REVIEW.value},
    RouteName.PRESERVE_RAW: {"retry_on_fail": False, "max_retries": 0, "on_fail_after_retries": RouteName.ESCALATE_REVIEW.value},
    RouteName.SKIP: {"retry_on_fail": False, "max_retries": 0, "on_fail_after_retries": RouteName.SKIP.value},
    RouteName.ESCALATE_REVIEW: {"retry_on_fail": False, "max_retries": 0, "on_fail_after_retries": RouteName.ESCALATE_REVIEW.value},
}


def assign_route(features: ChunkFeatures) -> RouteDecision:
    assigned_route = DEFAULT_ROUTES[features.chunk_type]
    final_route = assigned_route
    override_name = None
    rationale = f"default:{features.chunk_type.value}"

    if features.is_empty or features.char_count == 0:
        final_route = RouteName.SKIP
        override_name = "skip_empty_or_whitespace"
        rationale = "chunk empty"
    elif features.artifact_score >= 0.9:
        final_route = RouteName.SKIP
        override_name = "skip_pure_artifact"
        rationale = "artifact score high"
    elif features.chunk_size_class.value == "oversize":
        final_route = RouteName.ESCALATE_REVIEW
        override_name = "escalate_oversize_chunks"
        rationale = "oversize chunk should be rechunked"
    elif features.predicted_validator_risk >= 0.8 and final_route == RouteName.ONE_PASS_CONVERT:
        final_route = RouteName.TWO_PASS_CONVERT
        override_name = "escalate_high_validator_risk"
        rationale = "predicted validator risk high"
    elif features.ambiguity_score >= 0.7 and features.chunk_type == ChunkType.MIXED_DENSE:
        final_route = RouteName.TWO_PASS_CONVERT
        override_name = "escalate_ambiguous_mixed_dense"
        rationale = "mixed dense chunk ambiguity high"

    return RouteDecision(
        chunk_id=features.chunk_id,
        sourcebook_id=features.sourcebook_id,
        chunk_type=features.chunk_type,
        chunk_size_class=features.chunk_size_class,
        assigned_route=assigned_route,
        final_route=final_route,
        override_name=override_name,
        rationale=rationale,
        validator_names=VALIDATORS[final_route],
        retry_policy=RETRY_POLICIES[final_route],
    )

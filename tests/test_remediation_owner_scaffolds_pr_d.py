from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RT008_PATH = ROOT / "docs" / "doctrine" / "control" / "RT008_generated_content_provenance_recurrence_owner_scaffold.md"
RT012_PATH = ROOT / "docs" / "doctrine" / "control" / "RT012_d_series_promotion_boundary_owner_scaffold.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
D02_SOURCE_PACK_PATH = ROOT / "docs" / "doctrine" / "native_design" / "d_series" / "source_packs" / "astra_d02_doctrine_pack_v0_1"


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_pr_d_owner_scaffold_files_exist() -> None:
    assert RT008_PATH.exists()
    assert RT012_PATH.exists()


def test_both_scaffolds_reference_remediation_priority_ledger() -> None:
    for path in [RT008_PATH, RT012_PATH]:
        text = read(path)
        assert "REMEDIATION-PRIORITY-LEDGER-001" in text
        assert "owner scaffold" in text


def test_rt008_references_track_dependencies_and_later_tracks() -> None:
    text = read(RT008_PATH)
    for phrase in [
        "RT-008",
        "RT-008-generated-content-provenance",
        "RT-001",
        "RT-002",
        "RT-003",
        "RT-005",
        "RT-011",
        "RT-006",
        "RT-007",
        "RT-009",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
    ]:
        assert phrase in text


def test_rt008_references_source_pressures_and_backend_first_lifecycle() -> None:
    text = read(RT008_PATH)
    for phrase in [
        "C01",
        "C02",
        "C05",
        "C06",
        "C07",
        "C08",
        "C09",
        "C10",
        "C01_creature_npc_record_schema.md",
        "C02_item_gear_record_schema.md",
        "C05_faction_institution_record_schema.md",
        "C06_location_site_region_record_schema.md",
        "C07_mission_scenario_adventure_record_schema.md",
        "C08_vehicle_ship_platform_record_schema.md",
        "C09_hazard_environment_record_schema.md",
        "C10_table_oracle_record_schema.md",
        "backend-first generated-content lifecycle language",
        "backend-first model-interchangeability invariant",
        "generated content becomes durable only through backend-owned schema, validation, provenance, and commit pathways",
        "SM00",
    ]:
        assert phrase in text


def test_rt008_states_ephemeral_proposal_and_durable_recurrence_requirements() -> None:
    text = read(RT008_PATH)
    for phrase in [
        "Generated content may begin as an ephemeral proposal",
        "Durable recurrence requires backend-owned schema, provenance, validation, event/state commitment, persistence, and reviewer-controlled eligibility",
        "Canon promotion is separate from generated-content persistence",
        "Source-local/generated/canon status must remain distinguishable",
    ]:
        assert phrase in text


def test_rt008_prohibits_llm_generated_content_authority() -> None:
    text = read(RT008_PATH)
    for phrase in [
        "creating durable generated records",
        "deciding recurrence eligibility",
        "assigning persistent IDs as authority",
        "creating provenance records",
        "writing generated content to files",
        "promoting generated content to canon",
        "treating generated narration as persisted setting truth",
        "creating NPC/faction/location/item/mission/hazard/table records as backend truth",
        "bypassing validation/reviewer approval",
        "using model memory as generated-content storage",
    ]:
        assert phrase in text


def test_rt008_names_only_conceptual_placeholders() -> None:
    text = read(RT008_PATH)
    for phrase in [
        "ephemeral_proposal",
        "generated_candidate",
        "provenance_required",
        "source_scope_declared",
        "recurrence_eligibility_review",
        "durable_record_candidate",
        "backend_validation_required",
        "event_commit_required",
        "retrieval_index_pending",
        "canon_promotion_separate",
        "generated_record_rejected",
        "conceptual placeholders only",
        "not final schemas",
        "not generator templates",
        "not generated records",
        "not recurrence policy",
        "not provenance database",
        "not retrieval index",
        "not content writer",
        "not canon promotion",
        "not runtime implementation",
    ]:
        assert phrase in text


def test_rt012_references_track_dependencies_audits_and_source_pressure() -> None:
    text = read(RT012_PATH)
    for phrase in [
        "RT-012",
        "RT-012-d-series-promotion-boundary",
        "RT-011",
        "RT-008",
        "RT-001",
        "RT-002",
        "RT-003",
        "RT-005",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
        "D-series/native-design source packs",
        "docs/doctrine/native_design/d_series/source_packs/",
        "D02",
        "D02-03_cost_commitment_overinvestment_and_success_at_cost.md",
        "authority hierarchy",
        "canon/sourcebook promotion",
    ]:
        assert phrase in text

    if D02_SOURCE_PACK_PATH.exists():
        assert "astra_d02_doctrine_pack_v0_1" in text


def test_rt012_states_design_pressure_only_until_promoted() -> None:
    text = read(RT012_PATH)
    for phrase in [
        "D-series/native-design material may exert design pressure only until explicitly promoted",
        "Promotion requires separate reviewer decision, canon/sourcebook inclusion policy, conflict review, authority-level update, and registry tracking",
        "D-series material can inform later doctrine but cannot silently become Astra law",
    ]:
        assert phrase in text


def test_rt012_prohibits_llm_d_series_promotion_authority() -> None:
    text = read(RT012_PATH)
    for phrase in [
        "promoting D-series source-pack material to canon",
        "treating D-series draft material as runtime authority",
        "using D-series examples as live-play behavior",
        "converting source-pack prose into mechanics",
        "overriding canon hierarchy",
        "resolving canon conflicts",
        "authorizing sourcebook inclusion",
        "authorizing training data",
        "using draft material in context packets as authoritative truth",
        "treating source-pack presence as adoption",
    ]:
        assert phrase in text


def test_rt012_names_only_conceptual_placeholders() -> None:
    text = read(RT012_PATH)
    for phrase in [
        "draft_source_material",
        "design_pressure_recorded",
        "promotion_review_required",
        "authority_level_checked",
        "canon_conflict_checked",
        "runtime_dependency_checked",
        "sourcebook_inclusion_pending",
        "rejected_or_quarantined",
        "promoted_by_explicit_decision",
        "training_use_separate",
        "conceptual placeholders only",
        "not a promotion workflow implementation",
        "not canon promotion",
        "not sourcebook inclusion",
        "not runtime authority",
        "not training authorization",
        "not validator implementation",
        "not doctrine rewrite",
    ]:
        assert phrase in text


def test_both_scaffolds_include_explicit_non_implementation_guardrails() -> None:
    for path in [RT008_PATH, RT012_PATH]:
        text = read(path)
        for phrase in [
            "planning/control only",
            "Explicit non-implementation statement",
            "implements no",
            "no doctrine rewrite",
            "no runtime implementation",
            "no schema implementation",
            "no command IR implementation",
            "no math implementation",
            "no validator implementation",
            "no generator implementation",
            "no generated-record creation",
            "no persistence writer implementation",
            "no retrieval index implementation",
            "no context-packet compiler implementation",
            "no source-pack promotion",
            "no sourcebook inclusion",
            "no canon promotion",
            "no live-play/training authorization",
            "no donor-content audit",
        ]:
            assert phrase in text


def test_registry_tracks_pr_d_owner_scaffolds() -> None:
    registry = read(REGISTRY_PATH)
    for phrase in [
        "REMEDIATION-RT008-GENERATED-CONTENT-PROVENANCE-RECURRENCE-OWNER-SCAFFOLD-001",
        "REMEDIATION-RT012-D-SERIES-PROMOTION-BOUNDARY-OWNER-SCAFFOLD-001",
        "RT008_generated_content_provenance_recurrence_owner_scaffold.md",
        "RT012_d_series_promotion_boundary_owner_scaffold.md",
        "owner scaffold only",
        "no doctrine rewrite",
        "no runtime implementation",
        "no schema implementation",
        "no command IR implementation",
        "no math implementation",
        "no validator implementation",
        "no generator implementation",
        "no generated-record creation",
        "no persistence writer implementation",
        "no retrieval index implementation",
        "no context-packet compiler implementation",
        "no source-pack promotion",
        "no sourcebook inclusion",
        "no canon promotion",
        "no live-play/training authorization",
        "no donor-content audit",
    ]:
        assert phrase in registry


def test_scaffolds_and_registry_do_not_claim_to_implement_runtime_artifacts() -> None:
    forbidden_claims = [
        "implements generators",
        "implements generated records",
        "implements schemas",
        "implements validators",
        "implements runtime",
        "implements persistence writers",
        "implements retrieval indexes",
        "implements context-packet compilers",
        "implements source-pack promotion",
        "implements sourcebook inclusion",
        "implements canon promotion",
        "implements live-play prompts",
        "implements training behavior",
        "generators implemented",
        "generated records implemented",
        "schemas implemented",
        "validators implemented",
        "runtime implemented",
        "persistence writers implemented",
        "retrieval indexes implemented",
        "context-packet compilers implemented",
        "source-pack promotion implemented",
        "sourcebook inclusion implemented",
        "canon promotion implemented",
        "live-play prompts implemented",
        "training behavior implemented",
        "runtime-ready",
        "validator-ready",
        "generator-ready",
        "live-play ready",
    ]

    registry_text = read(REGISTRY_PATH)
    pr_d_registry_entry = registry_text.rsplit(
        "REMEDIATION-RT008-GENERATED-CONTENT-PROVENANCE-RECURRENCE-OWNER-SCAFFOLD-001",
        1,
    )[1].lower()

    for text in [read(RT008_PATH).lower(), read(RT012_PATH).lower(), pr_d_registry_entry]:
        for phrase in forbidden_claims:
            assert phrase not in text

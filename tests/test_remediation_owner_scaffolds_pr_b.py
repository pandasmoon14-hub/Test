from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RT002_PATH = ROOT / "docs" / "doctrine" / "control" / "RT002_resource_consequence_math_owner_scaffold.md"
RT003_PATH = ROOT / "docs" / "doctrine" / "control" / "RT003_combat_hazard_damage_recovery_owner_scaffold.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
D02_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "native_design"
    / "d_series"
    / "source_packs"
    / "astra_d02_doctrine_pack_v0_1"
    / "D02-03_cost_commitment_overinvestment_and_success_at_cost.md"
)


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_pr_b_owner_scaffold_files_exist() -> None:
    assert RT002_PATH.exists()
    assert RT003_PATH.exists()


def test_scaffolds_reference_remediation_priority_ledger() -> None:
    for path in [RT002_PATH, RT003_PATH]:
        text = read(path)
        assert "REMEDIATION-PRIORITY-LEDGER-001" in text
        assert "owner scaffold" in text


def test_rt002_references_track_dependencies_and_key_source_pressures() -> None:
    text = read(RT002_PATH)

    phrases = [
        "RT-002",
        "RT-002-resource-backlash-consequence-math",
        "RT-001",
        "RT-011",
        "A10",
        "A13",
        "B02",
        "C03",
        "C07",
        "C09",
        "SM00",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
    ]
    if D02_PATH.exists():
        phrases.append("D02")

    for phrase in phrases:
        assert phrase in text


def test_rt003_references_track_dependencies_and_key_source_pressures() -> None:
    text = read(RT003_PATH)

    for phrase in [
        "RT-003",
        "RT-003-combat-hazard-damage-recovery",
        "RT-001",
        "RT-002",
        "RT-009",
        "RT-011",
        "A13",
        "B10",
        "C09",
        "C08",
        "C07",
        "A10",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
    ]:
        assert phrase in text


def test_scaffolds_include_explicit_non_implementation_guardrails() -> None:
    for path in [RT002_PATH, RT003_PATH]:
        text = read(path)
        for phrase in [
            "planning/control only",
            "Explicit non-implementation statement",
            "implements no",
            "no doctrine rewrite",
            "runtime implementation",
            "schema implementation",
            "command IR implementation",
            "math implementation",
            "damage table implementation",
            "validator implementation",
            "generator implementation",
            "persistence writer",
            "context-packet compiler",
            "canon promotion",
            "live-play",
            "training data",
            "donor-content audit",
        ]:
            assert phrase in text


def test_rt002_prohibits_llm_resource_and_consequence_authority() -> None:
    text = read(RT002_PATH)

    for phrase in [
        "choosing resource costs",
        "spending or refunding resources",
        "deciding backlash severity",
        "applying corruption or strain",
        "determining damage, healing, or recovery",
        "granting rewards or losses",
        "committing consequence events",
        "converting narration into state deltas",
        "inventing formulas",
        "overriding backend validators",
    ]:
        assert phrase in text


def test_rt003_prohibits_llm_combat_hazard_and_recovery_authority() -> None:
    text = read(RT003_PATH)

    for phrase in [
        "detecting hidden threats as authority",
        "deciding exposure timing",
        "rolling or selecting hazard outcomes",
        "applying damage or injury",
        "killing or incapacitating actors",
        "resolving mitigation or recovery",
        "mutating vehicle/platform integrity",
        "committing mission consequences",
        "inventing enemy behavior as mechanical truth",
        "treating combat narration as backend resolution",
    ]:
        assert phrase in text


def test_registry_tracks_both_pr_b_owner_scaffolds() -> None:
    registry = read(REGISTRY_PATH)

    for phrase in [
        "REMEDIATION-RT002-RESOURCE-CONSEQUENCE-MATH-OWNER-SCAFFOLD-001",
        "REMEDIATION-RT003-COMBAT-HAZARD-DAMAGE-RECOVERY-OWNER-SCAFFOLD-001",
        "RT002_resource_consequence_math_owner_scaffold.md",
        "RT003_combat_hazard_damage_recovery_owner_scaffold.md",
        "owner scaffold only",
        "no doctrine rewrite",
        "no runtime implementation",
        "no schema implementation",
        "no command IR implementation",
        "no math implementation",
        "no damage table implementation",
        "no validator implementation",
        "no generator implementation",
        "no persistence writer implementation",
        "no context-packet compiler implementation",
        "no canon promotion",
        "no live-play/training authorization",
        "no donor-content audit",
    ]:
        assert phrase in registry


def test_scaffolds_do_not_claim_to_implement_final_artifacts_or_live_play() -> None:
    forbidden_claims = [
        "implements final formulas",
        "implements damage tables",
        "implements schemas",
        "implements command ir",
        "implements runtime",
        "implements validators",
        "implements generators",
        "implements persistence writers",
        "implements context-packet compilers",
        "implements live-play behavior",
        "final formulas implemented",
        "damage tables implemented",
        "schemas implemented",
        "command ir implemented",
        "runtime implemented",
        "validators implemented",
        "generators implemented",
        "persistence writers implemented",
        "context-packet compilers implemented",
        "live-play behavior implemented",
        "runtime-ready",
        "validator-ready",
        "generator-ready",
        "live-play ready",
    ]

    for path in [RT002_PATH, RT003_PATH]:
        text = read(path).lower()
        for phrase in forbidden_claims:
            assert phrase not in text

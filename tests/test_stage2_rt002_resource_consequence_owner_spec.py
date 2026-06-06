from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT002_resource_consequence_math_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT002-RESOURCE-CONSEQUENCE-MATH-OWNER-SPEC-001"
STAGE2_PR_ID = "STAGE2-PR-C"
TRACK = "RT-002"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
RT002_SCAFFOLD_FILE = "docs/doctrine/control/RT002_resource_consequence_math_owner_scaffold.md"
RT001_OWNER_SPEC_FILE = "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md"
RT011_OWNER_SPEC_FILE = "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

REPRESENTATIVE_FAMILY_TERMS = [
    "resource_pool_pressure",
    "committed_cost_pressure",
    "failed_command_cost_outcome",
    "optional_overcommitment_pressure",
    "refund_or_no_refund_pressure",
    "backlash_pressure",
    "corruption_pressure",
    "strain_pressure",
    "reward_pressure",
    "loss_pressure",
    "recovery_cost_pressure",
    "repair_cost_pressure",
    "damage_or_injury_cost_pressure",
    "asset_spend_or_degradation_pressure",
    "consequence_event_pressure",
]

REPRESENTATIVE_FUTURE_ARTIFACTS = [
    "CostFamilyInventory",
    "ResourcePoolRequirementInventory",
    "CostDeclarationRequirement",
    "CostCommitmentRequirement",
    "FailedCommandCostOutcomeRequirement",
    "OvercommitmentRequirement",
    "RefundPolicyRequirement",
    "BacklashSeverityRequirement",
    "CorruptionProgressionRequirement",
    "StrainAccumulationRequirement",
    "RewardLossRequirement",
    "RecoveryCostRequirement",
    "RepairCostRequirement",
    "ConsequenceSeverityRequirement",
    "ResourceStateDeltaRequirement",
    "CostValidationRequirement",
    "ConsequenceValidationRequirement",
]

REPRESENTATIVE_LLM_PROHIBITIONS = [
    "choosing resource costs",
    "spending resources",
    "refunding resources",
    "deciding failed-command cost outcomes",
    "choosing overcommitment effects",
    "deciding backlash severity",
    "treating narration as resource state",
    "inventing formulas",
    "overriding backend validators",
    "committing consequence events",
    "authorizing canon/sourcebook/training/live-play use",
]

GUARDRAIL_PHRASES = [
    "runtime code",
    "schema implementation",
    "command IR implementation",
    "validator implementation",
    "generator implementation",
    "persistence writer",
    "retrieval index",
    "context-packet compiler",
    "RNG/dice/table implementation",
    "event ledger implementation",
    "database schema",
    "resource formula",
    "resource pool list",
    "cost table",
    "damage table",
    "reward economy",
    "live-play prompt",
    "training data",
    "donor-content audit",
    "sourcebook inclusion authorization",
    "pilot conversion authorization",
    "canon promotion",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "authorizes_runtime_implementation: true",
    "authorizes_schema_implementation: true",
    "authorizes_validator_implementation: true",
    "authorizes_math_implementation: true",
    "authorizes_resource_formula: true",
    "authorizes_cost_table: true",
    "authorizes_reward_economy: true",
    "authorizes_live_play: true",
    "authorizes_training: true",
    "authorizes_canon_promotion: true",
    "authorizes_pilot_conversion: true",
    "implementation_status: executable",
    "implementation_status: implemented",
]


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_owner_specification_file_exists_and_has_core_tracking() -> None:
    text = read(SPEC_PATH)
    for expected in [TRACKING_ID, STAGE2_PR_ID, TRACK]:
        assert expected in text


def test_owner_spec_references_required_stage2_audit_and_owner_sources() -> None:
    text = read(SPEC_PATH)
    for expected in [
        STAGE2_PLAN_ID,
        REMEDIATION_LEDGER_ID,
        RT002_SCAFFOLD_FILE,
        RT001_OWNER_SPEC_FILE,
        RT011_OWNER_SPEC_FILE,
        *AUDIT_IDS,
    ]:
        assert expected in text


def test_scope_and_must_not_own_boundaries_are_defined() -> None:
    text = read(SPEC_PATH)
    for heading in ["## 2. Scope", "## 3. Must-not-own boundaries"]:
        assert heading in text
    for phrase in [
        "resource/cost/consequence math ownership boundaries",
        "cost-family classification requirements",
        "failed-command cost outcome requirements",
        "optional overcommitment math boundary requirements",
        "reward, loss, and economy pressure boundaries",
        "validation/readiness handoff to RT-011",
        "final resource formulas",
        "final resource names or final resource pool list",
        "final cost values",
        "final refund rules",
        "final backlash, corruption, or strain formulas",
        "final damage tables",
        "final reward economy",
    ]:
        assert phrase in text


def test_authority_model_is_defined() -> None:
    text = read(SPEC_PATH)
    assert "## 4. Authority model" in text
    for phrase in [
        "RT-001 owns when costs are declared",
        "RT-002 owns what future math families are required",
        "RT-011 owns validation/readiness requirements",
        "Future backend runtime owners",
        "The LLM may only summarize visible backend-approved cost/consequence outcomes",
    ]:
        assert phrase in text


def test_resource_consequence_family_contract_is_placeholder_only() -> None:
    text = read(SPEC_PATH)
    assert "## 5. Resource/consequence family contract" in text
    for phrase in [
        "planning placeholders only",
        "not formulas",
        "not final resource pools",
        "not schema fields",
        "not runtime state",
        "not event records",
        "not validators",
        "not live-play rules",
    ]:
        assert phrase in text
    for term in REPRESENTATIVE_FAMILY_TERMS:
        assert term in text


def test_cost_and_consequence_contracts_are_present_without_final_math() -> None:
    text = read(SPEC_PATH)
    for heading in [
        "## 6. Cost outcome contract",
        "## 7. Backlash/corruption/strain/consequence contract",
    ]:
        assert heading in text
    for phrase in [
        "declared costs must be distinguishable from committed costs",
        "committed costs must be auditable",
        "failed commands must have an explicit future cost-outcome rule",
        "refunds must never be assumed by narration",
        "costs attached to hidden information require RT-005",
        "costs driven by random tables, dice, oracles",
        "qualitative consequence labels are not enough for runtime readiness",
        "consequence severity, thresholds, duration, stacking, recovery, clearing",
        "hidden consequences route through RT-005",
        "validators and readiness claims route through RT-011",
        "does not define final thresholds",
        "does not define final refund rules",
    ]:
        assert phrase in text


def test_future_math_artifact_inventory_is_future_required_not_implemented() -> None:
    text = read(SPEC_PATH)
    assert "## 8. Future math artifact inventory" in text
    assert "semantic requirements only" in text
    assert "not implemented formulas" in text
    for artifact in REPRESENTATIVE_FUTURE_ARTIFACTS:
        assert artifact in text
    assert text.count("future_required_not_implemented") >= len(REPRESENTATIVE_FUTURE_ARTIFACTS)


def test_validation_readiness_requirements_and_handoffs_are_present() -> None:
    text = read(SPEC_PATH)
    assert "## 9. Validation and readiness requirements" in text
    assert "## 10. Downstream handoffs" in text
    for phrase in [
        "source linkage validation",
        "cost-family coverage validation",
        "cost declaration/commitment boundary validation",
        "failed-command outcome validation",
        "refund/overcommitment boundary validation",
        "LLM non-authority validation",
        "non-implementation guardrail validation",
    ]:
        assert phrase in text
    for rt in [1, *range(3, 13)]:
        assert f"RT-{rt:03d}:" in text


def test_llm_non_authority_prohibitions_are_explicit() -> None:
    text = read(SPEC_PATH)
    assert "## 11. LLM non-authority rules" in text
    for phrase in REPRESENTATIVE_LLM_PROHIBITIONS:
        assert phrase in text


def test_non_implementation_reaffirmation_and_stage2_classification_are_present() -> None:
    text = read(SPEC_PATH)
    assert "## 12. Non-implementation reaffirmation" in text
    assert "## 13. Stage 2 output classification" in text
    assert "stage2_output:" in text
    for phrase in GUARDRAIL_PHRASES:
        assert phrase in text
    for phrase in [
        "stage2_pr_id: STAGE2-PR-C",
        "track: RT-002",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_validator_implementation: false",
        "authorizes_math_implementation: false",
        "authorizes_resource_formula: false",
        "authorizes_cost_table: false",
        "authorizes_reward_economy: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_canon_promotion: false",
        "authorizes_pilot_conversion: false",
    ]:
        assert phrase in text


def test_registry_and_decision_log_tracking_exist() -> None:
    registry = read(REGISTRY_PATH)
    decisions = read(DECISION_LOG_PATH)
    for text in [registry, decisions]:
        assert TRACKING_ID in text
        assert "RT002_resource_consequence_math_owner_specification.md" in text
    assert "stage2_rt002_resource_consequence_math_owner_specification" in registry
    assert "Stage 2 PR-C RT-002 resource/consequence math owner specification" in decisions


def test_no_positive_implementation_authority_claims_exist() -> None:
    combined = "\n".join(read(path) for path in [SPEC_PATH, REGISTRY_PATH, DECISION_LOG_PATH])
    lowered = combined.lower()
    for claim in FORBIDDEN_POSITIVE_CLAIMS:
        assert claim not in lowered
    for suspicious in [
        "authorizes runtime implementation",
        "authorizes schema implementation",
        "authorizes validator implementation",
        "authorizes math implementation",
        "authorizes resource formula",
        "authorizes live play",
        "authorizes training",
        "authorizes canon promotion",
        "authorizes pilot conversion",
    ]:
        assert suspicious not in lowered

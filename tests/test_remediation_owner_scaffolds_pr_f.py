from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RT006_PATH = ROOT / "docs" / "doctrine" / "control" / "RT006_mission_reward_clue_routing_owner_scaffold.md"
RT009_PATH = ROOT / "docs" / "doctrine" / "control" / "RT009_runtime_rng_table_oracle_owner_scaffold.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_pr_f_owner_scaffold_files_exist() -> None:
    assert RT006_PATH.exists()
    assert RT009_PATH.exists()


def test_both_scaffolds_reference_remediation_priority_ledger() -> None:
    for path in [RT006_PATH, RT009_PATH]:
        text = read(path)
        assert "REMEDIATION-PRIORITY-LEDGER-001" in text
        assert "owner scaffold" in text


def test_rt006_references_dependencies_sources_and_invariants() -> None:
    text = read(RT006_PATH)
    for phrase in [
        "RT-006",
        "RT-001",
        "RT-002",
        "RT-005",
        "RT-008",
        "RT-011",
        "RT-003",
        "RT-007",
        "RT-009",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
        "C07",
        "A13",
        "C09",
        "B09",
        "C10",
        "backend-first language",
        "hidden-info language",
        "backend-first model-interchangeability invariant",
    ]:
        assert phrase in text


def test_rt006_states_required_downstream_controls() -> None:
    text = read(RT006_PATH)
    for phrase in [
        "mission/scenario records are not runtime missions until backend-owned state, event, reward, clue, hidden-truth, provenance, and validation paths exist",
        "reward and consequence commits are downstream of RT-002",
        "clue/hidden-truth exposure is downstream of RT-005",
        "generated missions require RT-008 provenance/recurrence controls before persistence",
        "table/oracle dependencies must route through RT-009 before results can be committed",
    ]:
        assert phrase in text


def test_rt006_prohibits_llm_mission_reward_clue_authority() -> None:
    text = read(RT006_PATH)
    for phrase in [
        "generate missions as backend truth",
        "complete objectives",
        "reveal clues or hidden truths",
        "select branches",
        "commit rewards, penalties, or losses",
        "decide mission failure consequences",
        "mutate scenario state",
        "select oracle/table outcomes",
        "create persistent mission records",
        "promote scenario canon",
        "bypass backend validation/reviewer approval",
        "treat mission narration as backend event commitment",
    ]:
        assert phrase in text


def test_rt006_names_only_conceptual_placeholders() -> None:
    text = read(RT006_PATH)
    for phrase in [
        "mission_record_reference",
        "objective_state_pending",
        "branch_state_candidate",
        "clue_visibility_pending",
        "hidden_truth_partition",
        "reward_commit_pending",
        "failure_consequence_candidate",
        "hazard_or_social_consequence_link",
        "oracle_result_dependency",
        "mission_completion_event_required",
        "scenario_generator_prohibited",
        "conceptual placeholders only",
        "not final schemas",
        "not mission runtime",
        "not reward economy",
        "not clue schema",
        "not hidden-truth database",
        "not branch runtime",
        "not generator",
        "not validator",
        "not event model",
        "not live-play authorization",
    ]:
        assert phrase in text


def test_rt009_references_dependencies_sources_and_invariants() -> None:
    text = read(RT009_PATH)
    for phrase in [
        "RT-009",
        "RT-001",
        "RT-005",
        "RT-011",
        "RT-002",
        "RT-003",
        "RT-006",
        "RT-008",
        "AUDIT-001",
        "AUDIT-WAVE1-001",
        "AUDIT-WAVE2-001",
        "README/backend-first invariant",
        "C10",
        "B10",
        "C09",
        "C07 where relevant",
        "roadmap RNG/runtime language",
        "backend-first model-interchangeability invariant",
    ]:
        assert phrase in text


def test_rt009_states_required_rng_table_oracle_controls() -> None:
    text = read(RT009_PATH)
    for phrase in [
        "RNG/table/oracle outcomes must be backend-owned, deterministic, seedable/replayable, auditable, and redacted when hidden",
        "Table/oracle records are not executable RNG systems by themselves",
        "Narration may only describe backend-selected and context-approved results",
        "Hidden results must route through RT-005 before projection",
        "Mission/hazard/reward uses of tables must not bypass RT-006, RT-003, or RT-002 as applicable",
    ]:
        assert phrase in text


def test_rt009_prohibits_llm_rng_table_oracle_authority() -> None:
    text = read(RT009_PATH)
    for phrase in [
        "roll dice",
        "choose random results",
        "select oracle/table outcomes",
        "alter table weights",
        "invent rows or result domains as truth",
        "decide hidden random results",
        "commit oracle outcomes",
        "create replay references",
        "use model randomness as RNG authority",
        "treat narrated chance as backend randomness",
        "bypass backend validation/reviewer approval",
    ]:
        assert phrase in text


def test_rt009_names_only_conceptual_placeholders() -> None:
    text = read(RT009_PATH)
    for phrase in [
        "rng_authority_required",
        "seed_reference_pending",
        "table_record_reference",
        "table_weight_validation_pending",
        "oracle_invocation_candidate",
        "hidden_result_redaction_required",
        "replay_reference_required",
        "random_result_commit_pending",
        "table_result_domain_pending",
        "narration_result_projection",
        "conceptual placeholders only",
        "not RNG implementation",
        "not dice roller",
        "not oracle registry",
        "not random table data",
        "not table validator",
        "not event model",
        "not replay verifier",
        "not context-packet compiler",
        "not live-play authorization",
    ]:
        assert phrase in text


def test_both_files_include_explicit_non_implementation_guardrails() -> None:
    for path in [RT006_PATH, RT009_PATH]:
        text = read(path)
        for phrase in [
            "planning/control only",
            "does not implement remediation",
            "Explicit non-implementation statement",
            "no doctrine rewrite",
            "no runtime implementation",
            "no schema implementation",
            "no command IR implementation",
            "no math implementation",
            "no validator implementation",
            "no generator implementation",
            "no live-play/training authorization",
            "no donor-content audit",
        ]:
            assert phrase in text


def test_registry_tracks_both_pr_f_scaffolds_and_guardrails() -> None:
    text = read(REGISTRY_PATH)
    for phrase in [
        "REMEDIATION-RT006-MISSION-REWARD-CLUE-ROUTING-OWNER-SCAFFOLD-001",
        "REMEDIATION-RT009-RUNTIME-RNG-TABLE-ORACLE-OWNER-SCAFFOLD-001",
        "owner scaffold only",
        "no doctrine rewrite",
        "no runtime implementation",
        "no schema implementation",
        "no command IR implementation",
        "no math implementation",
        "no validator implementation",
        "no generator implementation",
        "no mission generation",
        "no reward commitment",
        "no clue reveal",
        "no hidden-truth database implementation",
        "no RNG implementation",
        "no oracle/table roll implementation",
        "no random table data creation",
        "no persistence writer implementation",
        "no replay verifier implementation",
        "no retrieval index implementation",
        "no context-packet compiler implementation",
        "no canon promotion",
        "no live-play/training authorization",
        "no donor-content audit",
    ]:
        assert phrase in text


def test_no_file_claims_to_implement_runtime_or_training_behavior() -> None:
    for path in [RT006_PATH, RT009_PATH]:
        text = read(path).lower()
        for forbidden in [
            "this scaffold implements mission runtime",
            "this scaffold implements reward economy",
            "this scaffold implements clue schema",
            "this scaffold implements hidden-truth database",
            "this scaffold implements rng",
            "this scaffold implements dice roller",
            "this scaffold implements oracle registry",
            "this scaffold implements table data",
            "this scaffold implements validators",
            "this scaffold implements runtime",
            "this scaffold implements event models",
            "this scaffold implements replay verifiers",
            "this scaffold implements persistence writers",
            "this scaffold implements retrieval indexes",
            "this scaffold implements context-packet compilers",
            "this scaffold implements live-play prompts",
            "this scaffold implements training behavior",
        ]:
            assert forbidden not in text

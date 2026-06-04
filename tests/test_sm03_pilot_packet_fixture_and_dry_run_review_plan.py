import re
from pathlib import Path

from tests.helpers import REGISTRY_PATH, ROOT, read_utf8

SM03_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "schema_math_mechanics"
    / "SM03_pilot_packet_fixture_and_dry_run_review_plan.md"
)

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Upstream controls and authority boundary",
    "## 3. Existing dry-run readiness posture",
    "## 4. What SM03 owns",
    "## 5. What SM03 must not own",
    "## 6. Pilot packet fixture concept",
    "## 7. Tiny pilot packet selection constraints",
    "## 8. Recommended dry-run C-family pressure set",
    "## 9. Packet metadata dry-run checklist",
    "## 10. Evidence and provenance dry-run checklist",
    "## 11. Lawful outcome dry-run checklist",
    "## 12. C00-C14 routing dry-run checklist",
    "## 13. `pending_schema` and missing-owner dry-run checklist",
    "## 14. Rejected-import, source-local, and legal/IP dry-run checklist",
    "## 15. Confidence, review-routing, and human-review dry-run checklist",
    "## 16. Repair queue, quarantine, and failure-report dry-run checklist",
    "## 17. Benchmark/evaluation dry-run checklist",
    "## 18. Dry-run review workflow",
    "## 19. Dry-run pass/fail interpretation",
    "## 20. What SM03 evidence may and may not prove",
    "## 21. Large-scale conversion non-readiness boundary",
    "## 22. Runtime/canon/sourcebook/live-play/training non-readiness boundary",
    "## 23. Owner map and lawful fallbacks",
    "## 24. Risk register",
    "## 25. Recommended next PR after SM03",
    "## 26. Acceptance criteria",
]

SM02_READINESS_TERMS = [
    "packet identity",
    "donor source identity",
    "donor-family classification",
    "extraction run identity",
    "page/range truth",
    "source hash or hash-later policy",
    "evidence references",
    "construct inventory",
    "lawful outcome ledger",
    "mapping ledger",
    "rejected-import ledger",
    "source-local retention ledger",
    "pending_schema ledger",
    "repair queue status",
    "quarantine queue status",
    "confidence/review-routing notes",
    "legal/IP flags",
    "reviewer decision points",
    "C-family routing targets",
    "pilot output review status",
    "failure report shape",
    "benchmark/evaluation prerequisites",
]

DRY_RUN_WORKFLOW_STEPS = [
    "Select tiny candidate packet set",
    "Confirm packet metadata exists",
    "Confirm evidence/provenance traceability",
    "Confirm visible construct inventory can be identified",
    "Confirm lawful outcome ledger can theoretically account for every construct",
    "Confirm C00-C14 or `pending_schema` owner routing can be assigned",
    "Confirm rejected-import/source-local/legal/IP risk can be routed",
    "Confirm confidence/review-routing and human-review path exists",
    "Confirm repair/quarantine/failure-report path exists",
    "Confirm benchmark/evaluation prerequisites are declared",
    "Record dry-run pass/fail result",
    "Route failures to repair, quarantine, deferred gap ledger",
    "Decide whether a later actual pilot conversion PR may be proposed",
]

FORBIDDEN_C_PROMOTION_VALUES = {
    "current",
    "pressure-tested",
    "stable_for_family",
    "stable_cross_family",
    "tested_minimum",
    "accepted_canon",
    "runtime_ready",
    "runtime-ready",
    "canon-ready",
    "schema-current",
    "schema_current",
    "runtime-current",
    "training-current",
}


def sm03_text() -> str:
    return read_utf8(SM03_PATH)


def _registry_record_block(file_id: str) -> str:
    text = read_utf8(REGISTRY_PATH)
    match = re.search(
        rf"^- file_id: {re.escape(file_id)}\n(?P<block>.*?)(?=^- file_id: |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"Missing registry record for {file_id}"
    return match.group(0)


def _scalar_from_block(block: str, key: str) -> str | None:
    match = re.search(
        rf"^\s*{re.escape(key)}:\s*['\"]?(?P<value>[^'\"\n#]+)",
        block,
        flags=re.MULTILINE,
    )
    return match.group("value").strip() if match else None


# --- Existence and structure ---


def test_sm03_file_exists_and_is_nonempty() -> None:
    assert SM03_PATH.exists()
    assert SM03_PATH.is_file()
    assert sm03_text().strip()


def test_required_section_headings_are_present() -> None:
    text = sm03_text()
    for section in REQUIRED_SECTIONS:
        assert section in text, f"Missing section: {section}"


# --- Identity and purpose ---


def test_sm03_states_pilot_packet_fixture_and_dry_run_planning_only() -> None:
    text = sm03_text()
    assert (
        "SM03 is a pilot packet fixture and dry-run review planning/control file only"
        in text
    )
    assert "dry-run review planning/control file only" in text


def test_sm03_states_no_conversion_or_converted_content() -> None:
    text = sm03_text()
    assert "SM03 does not run conversion" in text
    assert "does not create converted donor content" in text


def test_sm03_refuses_real_donor_content_and_all_non_goals() -> None:
    text = sm03_text()
    for marker in [
        "embed real copyrighted donor excerpts",
        "embed donor statblocks",
        "embed donor tables",
        "embed donor maps",
        "embed donor setting prose",
        "import donor proper nouns as Astra defaults",
        "create final output schemas",
        "create final executable schemas",
        "create JSON Schema files",
        "create Pydantic models",
        "create runtime schemas",
        "create backend schemas",
        "create database schemas",
        "create entity/component/event schemas",
        "command lifecycle contracts",
        "context packet contracts",
        "save-state shapes",
        "create final mechanics",
        "create exact math",
        "create resolution dice",
        "create damage formulas",
        "create resource formulas",
        "create progression math",
        "donor-statblock validators that treat donor statblocks as Astra defaults",
        "promote C00-C14 registry statuses",
        "rewrite C00-C14",
        "add C15",
        "promote canon",
        "write sourcebook prose",
        "create live-play behavior",
        "create training/evaluation corpora",
        "treat D00-D19 as authority",
        "use RHBF as hidden law",
    ]:
        assert marker in text, f"Missing non-goal: {marker}"


# --- Upstream references ---


def test_sm03_names_required_controls_and_families() -> None:
    text = sm03_text()
    for marker in [
        "SM00",
        "SM01",
        "SM02",
        "C00",
        "Batch C capstone",
        "B11",
        "Conversion IR",
        "lawful outcome taxonomy",
        "conversion intake",
        "extraction readiness",
        "donor family routing",
        "evaluation/benchmark",
        "runtime/Gate B",
    ]:
        assert marker in text, f"Missing upstream reference: {marker}"
    for number in range(1, 15):
        assert f"C{number:02d}" in text, f"Missing C-family reference: C{number:02d}"


def test_sm03_states_batch_b_b11_are_operational_routing_only() -> None:
    text = sm03_text()
    assert (
        "Batch B/B11 are not final mechanics" in text
        or "B11, remains operational routing doctrine" in text
    )
    assert "not runtime validation authority" in text


def test_sm03_states_d_series_are_draft_source_material_only() -> None:
    text = sm03_text()
    assert "D00-D19 source packs are draft source material only" in text
    assert "cannot become pilot packet authority" in text


# --- Definitions ---


def test_sm03_defines_pilot_packet_fixture() -> None:
    text = sm03_text()
    assert "pilot packet fixture" in text
    assert (
        "minimal, auditable, non-corpus-forming packet" in text
        or "minimal, auditable, non-corpus-forming" in text
    )
    assert "readiness gate applicability" in text
    assert "not as training data" in text


def test_sm03_defines_dry_run_review() -> None:
    text = sm03_text()
    assert "dry-run review" in text
    assert "pre-conversion exercise" in text
    assert "without converting the packet" in text


# --- Packet selection ---


def test_sm03_recommends_tiny_bounded_packet_set() -> None:
    text = sm03_text()
    assert "3-5 packet candidates" in text or "3-5" in text
    assert "tiny" in text.lower()
    assert "bounded" in text.lower()


def test_sm03_lists_recommended_dry_run_c_family_routes() -> None:
    text = sm03_text()
    for marker in [
        "C01 creature/NPC",
        "C02 item/gear",
        "C03 ability/power/technique",
        "C10 table/oracle",
    ]:
        assert marker in text, f"Missing C-family route: {marker}"
    assert "conditional C14" in text or "Conditional C14" in text
    assert "legal/IP/source-local routing is ready" in text


def test_sm03_lists_deferred_families() -> None:
    text = sm03_text()
    for family in ["C05", "C06", "C07", "C08", "C11", "C12", "C13"]:
        assert family in text, f"Missing deferred family: {family}"
    assert "deferred" in text.lower()
    assert "C04" in text
    assert "C09" in text
    assert "disambiguation" in text.lower() or "disambiguate" in text.lower()


# --- SM02 readiness terms ---


def test_sm03_includes_all_sm02_readiness_terms() -> None:
    text = sm03_text()
    for term in SM02_READINESS_TERMS:
        assert term in text, f"Missing SM02 readiness term: {term}"


# --- Dry-run workflow ---


def test_sm03_includes_dry_run_review_workflow_steps() -> None:
    text = sm03_text()
    for step in DRY_RUN_WORKFLOW_STEPS:
        assert step in text, f"Missing workflow step: {step}"


# --- Pass/fail interpretation ---


def test_sm03_includes_dry_run_pass_fail_interpretation() -> None:
    text = sm03_text()
    assert "Dry-run pass criteria" in text or "dry-run pass" in text.lower()
    assert "Dry-run fail criteria" in text or "dry-run fail" in text.lower()


def test_sm03_dry_run_pass_does_not_mean_later_readiness() -> None:
    text = sm03_text()
    for marker in [
        "conversion success",
        "large-scale conversion readiness",
        "canon readiness",
        "sourcebook readiness",
        "runtime readiness",
        "final mechanics readiness",
        "live-play readiness",
        "training readiness",
        "benchmark success",
    ]:
        assert marker in text, f"Missing non-readiness marker: {marker}"


def test_sm03_dry_run_fail_conditions_include_required_items() -> None:
    text = sm03_text()
    for marker in [
        "Missing packet identity",
        "Missing donor source identity",
        "Missing donor-family classification",
        "Missing extraction run identity",
        "Missing page/range truth",
        "Missing evidence references",
        "Missing construct inventory",
        "D-series authority leakage",
        "RHBF hidden law",
    ]:
        assert marker in text, f"Missing fail condition: {marker}"


# --- Owner routing ---


def test_sm03_includes_owner_routing_and_lawful_fallbacks() -> None:
    text = sm03_text()
    assert "## 23. Owner map and lawful fallbacks" in text
    for marker in [
        "future pilot conversion owner",
        "future conversion/evidence validation owner",
        "lawful outcome/conversion intake owner",
        "C00/C-family schema owner and future validation/schema implementation owner",
        "C00/future validation/schema implementation owner",
        "C00/C14 plus future review/legal owner",
        "future review owner",
        "extraction readiness and pilot conversion owner",
        "future evaluation/benchmark owner",
        "future mechanics requirements owner only",
        "future runtime/Gate B owner only",
        "appropriate later phase owner only",
        "Lawful fallbacks must be explicit",
    ]:
        assert marker in text, f"Missing owner route: {marker}"


# --- Risk register ---


def test_sm03_includes_risk_register() -> None:
    text = sm03_text()
    assert "## 24. Risk register" in text
    for marker in [
        "Dry-run scope creep",
        "Fixture treated as conversion output",
        "Donor content embedded in repo",
        "Donor mechanics leakage",
        "Source-local/legal/IP leakage",
        "Missing schema disguised as implementation",
        "Evidence fabrication",
        "Over-trusting dry-run results",
        "Runtime/canon/sourcebook/training creep",
        "D-series authority creep",
        "Evaluation misuse",
        "RHBF hidden law",
    ]:
        assert marker in text, f"Missing risk: {marker}"


# --- Recommended next PR ---


def test_sm03_recommends_next_pr_without_final_mechanics_jump() -> None:
    text = sm03_text()
    assert "## 25. Recommended next PR after SM03" in text
    assert "SM04 pilot benchmark and evaluation rubric controls" in text
    assert "SM04 pilot packet repair and preflight gap controls" in text
    for marker in [
        "must not jump directly to final mechanics",
        "actual broad conversion",
        "runtime schemas",
        "canon consolidation",
        "sourcebook prose",
        "live-play adapter behavior",
        "training corpus creation",
    ]:
        assert marker in text, f"Missing next-PR boundary: {marker}"


# --- No implementation artifacts ---


def test_sm03_does_not_contain_obvious_implementation_artifacts() -> None:
    text = sm03_text()
    forbidden_patterns = [
        r"```\s*json",
        r"```\s*yaml",
        r"\$schema",
        r"\"type\"\s*:\s*\"object\"",
        r"class\s+\w+\(BaseModel\)",
        r"CREATE\s+TABLE",
        r"command_lifecycle\s*[:=]",
        r"context_packet\s*[:=]",
        r"save_state\s*[:=]",
        r"converted_donor_content\s*[:=]",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text, flags=re.IGNORECASE), (
            f"Implementation artifact found: {pattern}"
        )


# --- Registry non-promotion ---


def test_c00_c14_registry_records_not_promoted_to_forbidden_states() -> None:
    for file_id in ["C00", *[f"C{number:02d}" for number in range(1, 15)]]:
        block = _registry_record_block(file_id)
        for key in ["status", "authority_level", "test_status", "review_status"]:
            value = _scalar_from_block(block, key)
            if value is not None:
                assert value not in FORBIDDEN_C_PROMOTION_VALUES, (
                    f"{file_id} {key} was promoted to {value!r}"
                )


# --- Future-safe posture ---


def test_future_safe_posture_does_not_block_later_sm_files_or_proper_owner_promotion() -> None:
    text = sm03_text()
    assert "SM04" in text
    assert "later owner" in text.lower() or "future owner" in text.lower()

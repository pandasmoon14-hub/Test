"""Tests for Runtime Boundary Scaffold Completion Review and Stage 2 Plan."""

from pathlib import Path
import re

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPLETION_REVIEW_PATH = (
    REPO_ROOT / "docs" / "doctrine" / "reviews" / 
    "runtime_boundary_remediation_scaffold_completion_review_stage2_plan.md"
)
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"

yaml = pytest.importorskip(
    "yaml",
    reason=(
        "PyYAML is required for doctrine/registry validation; "
        "install test dependencies with "
        "python3 -m pip install -r requirements-dev.txt"
    ),
)


class TestScaffoldCompletionReviewExists:
    """Verify the scaffold completion review file exists."""

    def test_completion_review_file_exists(self):
        """Test that the completion review file exists."""
        assert COMPLETION_REVIEW_PATH.exists(), (
            f"Missing completion review file: {COMPLETION_REVIEW_PATH}"
        )


class TestAuditInputsReferenced:
    """Verify audit inputs are referenced in the completion review."""

    @pytest.fixture
    def review_content(self):
        """Load the completion review content."""
        assert COMPLETION_REVIEW_PATH.exists()
        return COMPLETION_REVIEW_PATH.read_text(encoding="utf-8")

    def test_references_audit_001(self, review_content):
        """Test that AUDIT-001 is referenced."""
        assert "AUDIT-001" in review_content or "runtime_boundary_generator_ownership_audit_protocol" in review_content

    def test_references_audit_wave1(self, review_content):
        """Test that AUDIT-WAVE1-001 is referenced."""
        assert "AUDIT-WAVE1-001" in review_content or "audit_wave1" in review_content.lower()

    def test_references_audit_wave2(self, review_content):
        """Test that AUDIT-WAVE2-001 is referenced."""
        assert "AUDIT-WAVE2-001" in review_content or "audit_wave2" in review_content.lower()

    def test_references_remediation_ledger(self, review_content):
        """Test that REMEDIATION-PRIORITY-LEDGER-001 is referenced."""
        assert "REMEDIATION-PRIORITY-LEDGER-001" in review_content or "remediation_priority_ledger" in review_content.lower()


class TestRTTracksReferenced:
    """Verify all RT-001 through RT-012 tracks are referenced."""

    @pytest.fixture
    def review_content(self):
        """Load the completion review content."""
        assert COMPLETION_REVIEW_PATH.exists()
        return COMPLETION_REVIEW_PATH.read_text(encoding="utf-8")

    @pytest.mark.parametrize("track_num", range(1, 13))
    def test_rt_track_referenced(self, review_content, track_num):
        """Test that each RT track is referenced."""
        track_id = f"RT-{track_num:03d}"
        assert track_id in review_content, f"Missing reference to {track_id}"


class TestRTScaffoldFilesReferenced:
    """Verify all RT-001 through RT-012 scaffold files are referenced."""

    @pytest.fixture
    def review_content(self):
        """Load the completion review content."""
        assert COMPLETION_REVIEW_PATH.exists()
        return COMPLETION_REVIEW_PATH.read_text(encoding="utf-8")

    SCAFFOLD_FILES = [
        "RT001_command_lifecycle_action_legality_owner_scaffold.md",
        "RT002_resource_consequence_math_owner_scaffold.md",
        "RT003_combat_hazard_damage_recovery_owner_scaffold.md",
        "RT004_ability_effect_skill_binding_owner_scaffold.md",
        "RT005_context_packet_hidden_information_owner_scaffold.md",
        "RT006_mission_reward_clue_routing_owner_scaffold.md",
        "RT007_social_faction_knowledge_state_owner_scaffold.md",
        "RT008_generated_content_provenance_recurrence_owner_scaffold.md",
        "RT009_runtime_rng_table_oracle_owner_scaffold.md",
        "RT010_inventory_item_vehicle_asset_owner_scaffold.md",
        "RT011_validation_readiness_tooling_owner_scaffold.md",
        "RT012_d_series_promotion_boundary_owner_scaffold.md",
    ]

    @pytest.mark.parametrize("scaffold_file", SCAFFOLD_FILES)
    def test_rt_scaffold_file_referenced(self, review_content, scaffold_file):
        """Test that each RT scaffold file is referenced."""
        assert scaffold_file in review_content, f"Missing reference to {scaffold_file}"


class TestRequiredSectionsPresent:
    """Verify required section headers are present."""

    @pytest.fixture
    def review_content(self):
        """Load the completion review content."""
        assert COMPLETION_REVIEW_PATH.exists()
        return COMPLETION_REVIEW_PATH.read_text(encoding="utf-8")

    REQUIRED_SECTIONS = [
        "Purpose and scope",
        "Inputs reviewed",
        "Scaffold coverage matrix",
        "Cross-track dependency review",
        "Overlap and conflict review",
        "Remaining gap inventory",
        "Second-stage remediation plan",
        "Recommended next PR",
    ]

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_required_section_present(self, review_content, section):
        """Test that each required section header is present."""
        assert section in review_content, f"Missing required section: {section}"


class TestStage2PlanPresent:
    """Verify Stage 2 plan structure is present."""

    @pytest.fixture
    def review_content(self):
        """Load the completion review content."""
        assert COMPLETION_REVIEW_PATH.exists()
        return COMPLETION_REVIEW_PATH.read_text(encoding="utf-8")

    def test_stage2_a_present(self, review_content):
        """Test that STAGE2-A is present."""
        assert "STAGE2-A" in review_content

    def test_stage2_b_present(self, review_content):
        """Test that STAGE2-B is present."""
        assert "STAGE2-B" in review_content

    def test_stage2_c_present(self, review_content):
        """Test that STAGE2-C is present."""
        assert "STAGE2-C" in review_content

    def test_rt001_as_next_pr(self, review_content):
        """Test that RT-001 is identified as the likely next PR."""
        # Check for STAGE2-A recommendation with RT-001
        assert "STAGE2-A" in review_content
        assert "RT-001" in review_content or "RT001" in review_content
        # Verify it's recommended as next
        assert "next PR" in review_content.lower() or "recommended next" in review_content.lower()


class TestNonImplementationStatements:
    """Verify non-implementation guardrails are stated."""

    @pytest.fixture
    def review_content(self):
        """Load the completion review content."""
        assert COMPLETION_REVIEW_PATH.exists()
        return COMPLETION_REVIEW_PATH.read_text(encoding="utf-8")

    FORBIDDEN_PHRASES = [
        "runtime implementation",
        "schema implementation",
        "command IR implementation",
        "validator implementation",
        "generator implementation",
        "persistence writer",
        "context-packet compiler",
        "live-play",
        "training",
        "canon promotion",
    ]

    def test_states_no_implementation(self, review_content):
        """Test that no implementation was performed statement exists."""
        assert "no implementation" in review_content.lower() or "non-implementation" in review_content.lower()

    def test_non_implementation_statement_section(self, review_content):
        """Test that explicit non-implementation statement section exists."""
        assert "Explicit non-implementation statement" in review_content or "non-implementation statement" in review_content.lower()


class TestRegistryTracking:
    """Verify registry tracking exists for the completion review."""

    @pytest.fixture
    def registry_data(self):
        """Load the registry YAML."""
        assert REGISTRY_PATH.exists()
        with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)

    def test_tracking_id_in_changelog(self, registry_data):
        """Test that SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001 is in changelog."""
        changelog = registry_data.get("changelog", [])
        found = False
        for entry in changelog:
            note = entry.get("note", "")
            if "SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001" in note:
                found = True
                break
        assert found, "Missing SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001 in registry changelog"

    def test_non_implementation_in_registry_note(self, registry_data):
        """Test that non-implementation guardrails are in registry note."""
        changelog = registry_data.get("changelog", [])
        found = False
        for entry in changelog:
            note = entry.get("note", "")
            if "SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001" in note:
                # Check for key non-implementation phrases
                assert "no doctrine rewrite" in note.lower() or "no runtime implementation" in note.lower()
                found = True
                break
        assert found, "Missing SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001 entry for verification"


class TestNoForbiddenImplementationClaims:
    """Verify no file claims forbidden implementations."""

    @pytest.fixture
    def review_content(self):
        """Load the completion review content."""
        assert COMPLETION_REVIEW_PATH.exists()
        return COMPLETION_REVIEW_PATH.read_text(encoding="utf-8")

    def test_no_runtime_code_claim(self, review_content):
        """Test that no runtime code implementation is claimed."""
        # Should state NO implementation, not claim TO implement
        assert "implements runtime code" not in review_content.lower()
        assert "created runtime" not in review_content.lower()

    def test_no_schema_creation_claim(self, review_content):
        """Test that no schema creation is claimed."""
        assert "created schema" not in review_content.lower()
        assert "implements schemas" not in review_content.lower()

    def test_no_command_ir_creation_claim(self, review_content):
        """Test that no command IR creation is claimed."""
        assert "created command IR" not in review_content.lower()
        assert "implements command IR" not in review_content.lower()

    def test_no_math_implementation_claim(self, review_content):
        """Test that no math implementation is claimed."""
        assert "implemented math" not in review_content.lower()
        assert "created formulas" not in review_content.lower()

    def test_no_validator_implementation_claim(self, review_content):
        """Test that no validator implementation is claimed."""
        assert "implemented validators" not in review_content.lower()
        assert "created validators" not in review_content.lower()

    def test_no_generator_implementation_claim(self, review_content):
        """Test that no generator implementation is claimed."""
        assert "implemented generators" not in review_content.lower()
        assert "created generators" not in review_content.lower()

    def test_no_persistence_writer_claim(self, review_content):
        """Test that no persistence writer implementation is claimed."""
        assert "implemented persistence writers" not in review_content.lower()
        assert "created persistence writers" not in review_content.lower()

    def test_no_context_packet_compiler_claim(self, review_content):
        """Test that no context-packet compiler implementation is claimed."""
        assert "implemented context-packet compiler" not in review_content.lower()
        assert "created context-packet compiler" not in review_content.lower()

    def test_no_live_play_prompt_claim(self, review_content):
        """Test that no live-play prompt creation is claimed."""
        assert "created live-play prompts" not in review_content.lower()
        assert "implemented live-play" not in review_content.lower()

    def test_no_training_behavior_claim(self, review_content):
        """Test that no training behavior creation is claimed."""
        assert "created training" not in review_content.lower()
        assert "implemented training" not in review_content.lower()

    def test_no_donor_audit_claim(self, review_content):
        """Test that no donor-content audit is claimed."""
        assert "audited donor" not in review_content.lower()
        assert "donor-content audit was performed" not in review_content.lower()

    def test_no_canon_promotion_claim(self, review_content):
        """Test that no canon promotion is claimed."""
        assert "promoted canon" not in review_content.lower()
        # The document states "no canon promotion was performed" as a negative assertion
        # which is correct - we should only check for positive claims of canon promotion
        assert "canon promotion was performed" not in review_content.lower() or "no canon promotion was performed" in review_content.lower()

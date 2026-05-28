from tests.helpers import REGISTRY_PATH, read_utf8, registry_records_by_id


REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. What this file owns",
    "## 3. What this file must not own",
    "## 4. Required definitions",
    "## 5. Core schema rules",
    "## 6. Conversion mapping rules",
    "## 7. Source-local handling",
    "## 8. Donor pressure absorbed",
    "## 9. Hard refusals / rejected imports",
    "## 10. Escalation triggers",
    "## 11. Dependencies",
    "## 12. Handoff to downstream layers",
    "## 13. Test cases / pressure examples",
    "## 14. Versioning and review protocol",
]

REQUIRED_FIELDS = [
    "record_id", "schema_id", "schema_version", "doctrine_version", "authority_layer",
    "lifecycle_status", "review_status", "source_scope", "source_family", "provenance_block",
    "evidence_refs", "extraction_refs", "donor_refs", "source_local_status", "rejected_import_status",
    "lawful_outcome", "canon_eligibility", "promotion_gate", "confidence_score", "review_queue",
    "reviewer_notes", "conflict_refs", "dependency_refs", "cross_refs", "supersedes_refs",
    "retrieval_metadata", "doctrine_tags", "retrieval_tags", "donor_tags", "access_tags",
]

REQUIRED_STATUSES = [
    "draft", "designed", "not_reviewed", "reviewed", "source-local", "rejected-import",
    "canon-candidate", "quarantined", "escalated", "deprecated", "superseded", "current",
]

REQUIRED_FAMILIES = [
    "shared content record", "source-local record", "rejected-import record", "canon-candidate record",
    "review-queue record", "conflict-record", "schema-registry record", "retrieval-index record",
    "runtime-event record placeholder",
]

MUST_NOT_OWN_BOUNDARIES = [
    "runtime state schema",
    "runtime event schema",
    "command lifecycle",
    "event-sourced state model",
    "state delta validator",
    "context packet compiler",
    "hidden-information runtime state",
    "canon promotion",
    "donor field names as Astra defaults",
    "donor record shapes",
]


def _c00_text() -> str:
    records = registry_records_by_id()
    c00 = records["C00"]
    return read_utf8(REGISTRY_PATH.parents[2] / c00["proposed_path"])


def test_c00_file_exists_at_registry_proposed_path() -> None:
    records = registry_records_by_id()
    c00 = records["C00"]
    content = read_utf8(REGISTRY_PATH.parents[2] / c00["proposed_path"])
    assert content.strip()


def test_c00_required_sections_fields_statuses_and_families() -> None:
    content = _c00_text()
    for section in REQUIRED_SECTIONS:
        assert section in content
    for field in REQUIRED_FIELDS:
        assert f"`{field}`" in content
    for status in REQUIRED_STATUSES:
        assert f"`{status}`" in content
    for family in REQUIRED_FAMILIES:
        assert family in content


def test_c00_boundaries_and_language_requirements() -> None:
    content = _c00_text()
    for boundary in MUST_NOT_OWN_BOUNDARIES:
        assert boundary in content

    required_phrases = [
        "Source-local records preserve donor provenance but do not become Astra canon",
        "Rejected-import records preserve refusal rationale and provenance",
        "Unclassifiable records are quarantined or escalated, not normalized by invention",
        "Donor proper nouns remain source-local unless later canon promotion accepts them",
        "Source-local record terms do not become accepted lexicon terms through C00",
        "Canon candidates remain candidates until later K-layer review",
    ]
    for phrase in required_phrases:
        assert phrase in content


def test_c00_dependencies_and_a_layer_boundary() -> None:
    content = _c00_text()
    assert "depends on A01-A15" in content
    assert "does not redefine A-layer ownership" in content


def test_c00_registry_state_and_scope_controls() -> None:
    records = registry_records_by_id()
    c00 = records["C00"]

    assert c00["status"] == "draft"
    assert c00["authority_level"] == "schema-draft"
    assert c00["test_status"] == "designed"
    assert c00["review_status"] == "not_reviewed"
    assert c00["proposed_path"] == "docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md"

    assert "K01" in records
    k01 = records["K01"]
    assert k01["file_id"] == "K01"

    # Ensure this PR does not promote downstream layers.
    for file_id, record in records.items():
        if file_id.startswith("C") and file_id != "C00":
            assert record["status"] != "current"
            assert record["status"] != "draft"
        if file_id.startswith("K") or file_id.startswith("R") or file_id.startswith("T"):
            assert record["status"] != "current"
            assert record["status"] != "draft"

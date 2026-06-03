from tests.helpers import REGISTRY_PATH, read_utf8, registry_records_by_id


REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. What this file owns",
    "## 3. What this file must not own",
    "## 4. AstraContentRecordBase",
    "## 5. Record-status rules",
    "## 6. Schema-family registry governance",
    "## 7. Provenance chain and evidence lock posture",
    "## 8. Inheritance and composition rules",
    "## 9. Source-local boundary object rules",
    "## 10. Rejected donor element rules",
    "## 11. Canon eligibility rules",
    "## 12. Legal/IP and source reliability routing",
    "## 13. Missing-schema fallback policy",
    "## 14. Batch B handoff boundary",
    "## 15. Runtime boundary",
    "## 16. Training and evaluation boundary",
    "## 17. Coverage-gap reporting",
]

REQUIRED_BASE_MARKERS = [
    "AstraContentRecordBase",
    "schema_family",
    "pending_schema",
    "record_status",
    "conversion_stage",
    "source_local",
    "canon_candidate",
    "accepted_canon",
    "accepted_with_limits",
    "quarantined",
    "rejected_import",
    "deprecated",
    "superseded",
    "source_evidence_refs",
    "construct_refs",
    "outcome_refs",
    "provenance_refs",
    "source_local_boundary",
    "rejected_donor_elements",
    "canon_eligibility",
    "ip_legal_flags",
    "source_reliability",
    "record_lineage",
    "composition_metadata",
    "validation_status",
    "validation_errors",
]

C_FAMILY_VALUES = [f"C{number:02d}" for number in range(15)]

INHERITANCE_AND_COMPOSITION_MARKERS = [
    "inheritance_allowed: false",
    "A child record does not inherit canon status",
    "A child record does not inherit source-local boundary",
    "A child record does not inherit mechanical authority",
    "A child record does not inherit runtime ownership",
    "Schema Frankensteins are prohibited",
]

GOVERNANCE_MARKERS = [
    "CFamilyRegistryEntry",
    "Registry drift is a validation failure",
    "SchemaCoverageGap",
    "missing-schema fallback",
    "donor math",
    "preserved as evidence",
    "Batch B",
    "Runtime",
    "Training",
    "evaluation",
]

BOUNDARY_MARKERS = [
    "C00 does not define C01-C14",
    "runtime state/schema/event/command lifecycle",
    "runtime state schema",
    "runtime event schema",
    "command lifecycle",
    "status labels do not promote canon",
    "source-local records do not become canon",
    "unclassifiable records are quarantined or escalated, not normalized by invention",
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


def test_c00_hardened_sections_are_present() -> None:
    content = _c00_text()
    for section in REQUIRED_SECTIONS:
        assert section in content


def test_c00_astra_content_record_base_markers_are_present() -> None:
    content = _c00_text()
    for marker in REQUIRED_BASE_MARKERS:
        assert marker in content
    for family_value in C_FAMILY_VALUES:
        assert family_value in content


def test_c00_schema_registry_provenance_and_gap_governance_markers() -> None:
    content = _c00_text()
    for marker in GOVERNANCE_MARKERS:
        assert marker in content

    provenance_chain = (
        "source file -> extraction run -> packet id -> page/range -> "
        "SourceEvidenceIR -> ConstructIR -> OutcomeIR -> Batch C record -> canon/review status"
    )
    assert provenance_chain in content

    hash_markers = [
        "source_evidence_hash",
        "hash_algorithm",
        "extraction_run_id",
        "packet_hash",
        "sidecar_hashes",
        "hash_lock_status",
        "unavailable_early_pilot",
    ]
    for marker in hash_markers:
        assert marker in content


def test_c00_inheritance_composition_source_local_and_rejection_controls() -> None:
    content = _c00_text()
    for marker in INHERITANCE_AND_COMPOSITION_MARKERS:
        assert marker in content

    source_local_markers = [
        "boundary_id",
        "local_context_type",
        "prohibited_promotions",
        "canon_review_required_for_reuse",
        "Proper nouns must be source-local, rejected, or routed to legal/IP review",
    ]
    for marker in source_local_markers:
        assert marker in content

    rejection_markers = [
        "rejected_donor_element_record",
        "rejection_id",
        "Donor field names are not Astra schema labels",
        "Donor stat values are not Astra combat math",
        "Donor currency/prices are not Astra economy",
    ]
    for marker in rejection_markers:
        assert marker in content


def test_c00_required_non_collapse_boundaries_are_preserved() -> None:
    content = _c00_text()
    lowered = content.lower()
    for marker in BOUNDARY_MARKERS:
        assert marker.lower() in lowered

    runtime_boundaries = [
        "event-sourced state model",
        "state delta validator",
        "context packet compiler",
        "hidden-information runtime state",
        "live-play behavior",
        "canon promotion procedure",
        "final mechanics",
        "accepted lexicon terms",
        "donor record formats as Astra defaults",
    ]
    for marker in runtime_boundaries:
        assert marker in content


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
    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"

    # Ensure this PR does not promote downstream layers.
    for file_id, record in records.items():
        if file_id.startswith("C") and file_id != "C00":
            assert record["status"] != "current"
            assert record["status"] != "draft"
        if file_id.startswith("K") or file_id.startswith("R") or file_id.startswith("T"):
            assert record["status"] != "current"

    assert records["K01"]["status"] == "todo"
    assert records["R01"]["status"] == "todo"
    assert records["T01"]["status"] == "todo"

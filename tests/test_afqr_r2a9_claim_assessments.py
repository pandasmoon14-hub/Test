"""Executable semantic verification for AFQR R2A-9 claims 0001-0016."""
from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BASE = "202aaa75a0373f305d3ee38e943c7a66a562778c"

CLAIMS_PATH = (
    "docs/doctrine/reviews/r2a/"
    "claim_assessments_0001_0016/index.yaml"
)
CONTRACT_PATH = (
    "docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml"
)
CORE_INDEX_PATH = (
    "docs/doctrine/reviews/r2a/"
    "semantic_core_agency/index.yaml"
)
WORLD_INDEX_PATH = (
    "docs/doctrine/reviews/r2a/"
    "semantic_world_coordination/index.yaml"
)

EXPECTED_OUTCOMES = {
    "R2-CLAIM-0001": "partially_governed_owner_gap_remains",
    "R2-CLAIM-0002": "escalated_doctrine_problem",
    "R2-CLAIM-0003": "partially_governed_owner_gap_remains",
    "R2-CLAIM-0004": "escalated_doctrine_problem",
    "R2-CLAIM-0005": "escalated_doctrine_problem",
    "R2-CLAIM-0006": "governed_by_existing_owner",
    "R2-CLAIM-0007": "escalated_doctrine_problem",
    "R2-CLAIM-0008": "partially_governed_owner_gap_remains",
    "R2-CLAIM-0009": "escalated_doctrine_problem",
    "R2-CLAIM-0010": "partially_governed_owner_gap_remains",
    "R2-CLAIM-0011": "partially_governed_owner_gap_remains",
    "R2-CLAIM-0012": "escalated_doctrine_problem",
    "R2-CLAIM-0013": "governed_by_existing_owner",
    "R2-CLAIM-0014": "implementation_or_schema_presupposition_only",
    "R2-CLAIM-0015": "implementation_or_schema_presupposition_only",
    "R2-CLAIM-0016": "partially_governed_owner_gap_remains",
}

EXPECTED_COUNTS = {
    "escalated_doctrine_problem": 6,
    "governed_by_existing_owner": 2,
    "implementation_or_schema_presupposition_only": 2,
    "partially_governed_owner_gap_remains": 6,
}

EXPECTED_UNRESOLVED = {
    "R2-CLAIM-0001",
    "R2-CLAIM-0003",
    "R2-CLAIM-0008",
    "R2-CLAIM-0010",
    "R2-CLAIM-0011",
    "R2-CLAIM-0014",
    "R2-CLAIM-0016",
}

REQUIRED_CLAIM_FIELDS = {
    "claim_id",
    "assessment_outcome",
    "evidence",
    "positive_links",
    "assessment_summary",
    "unresolved_owner_question_ids",
}

EVIDENCE_FIELDS = {
    "surface_ids",
    "relevant_current_normative_surface_ids",
    "relevant_current_control_surface_ids",
    "relevant_schema_runtime_test_surface_ids",
    "relevant_historical_or_source_local_surface_ids",
    "negative_or_absence_evidence_surface_ids",
}

REQUIRED_LINK_FIELDS = {
    "surface_id",
    "relevance_type",
    "semantic_role",
    "exact_relevance",
    "owner_boundary_effect",
}

SURFACE_ID_RE = re.compile(r"R2A-SURFACE-[A-Z]+-\d{4}")


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def load_live_surfaces():
    """Load successor live shards without treating historical index hashes as live."""
    surfaces = {}

    for index_path in (CORE_INDEX_PATH, WORLD_INDEX_PATH):
        index = load(index_path)
        rows = []

        for meta in index["shards"]:
            shard = load(meta["path"])
            shard_rows = shard["surface_records"]

            assert len(shard_rows) == meta["record_count"]
            rows.extend(shard_rows)

        assert len(rows) == index["surface_count"]

        for row in rows:
            sid = row["surface_id"]
            assert sid not in surfaces
            surfaces[sid] = row

    return surfaces


def test_r2a9_artifact_identity_range_and_source_traceability():
    data = load(CLAIMS_PATH)

    assert data["artifact_id"] == "AFQR-R2A-9-CLAIM-ASSESSMENT-INDEX-001"
    assert data["artifact_version"] == "0.1.0"
    assert data["status"] == "complete"
    assert data["phase"] == "R2A-9"
    assert data["authority_effect"] == "nonauthoritative_claim_assessment"
    assert data["inspected_repository_commit"] == BASE
    assert data["dependencies"] == ["R2A-2", "R2A-3", "R2A-8"]

    assert data["assessment_range"] == {
        "first_claim_id": "R2-CLAIM-0001",
        "last_claim_id": "R2-CLAIM-0016",
        "claim_count": 16,
    }

    assert data["semantic_surface_sources"] == [
        CORE_INDEX_PATH,
        WORLD_INDEX_PATH,
    ]

    source = data["source_claim_ledger"]

    assert source["path"] == (
        "docs/doctrine/reviews/"
        "afqr_r2_continuity_claim_and_owner_routing_ledger.yaml"
    )
    assert source["authority_effect"] == "tracking_review_only"

    actual_blob = git(
        "rev-parse",
        f'{BASE}:{source["path"]}',
    )

    assert actual_blob == source["git_blob_sha"]


def test_r2a9_exact_reviewed_outcomes_and_owner_questions():
    data = load(CLAIMS_PATH)
    contract = load(CONTRACT_PATH)

    claims = data["claim_assessments"]

    expected_ids = [
        f"R2-CLAIM-{number:04d}"
        for number in range(1, 17)
    ]

    assert [row["claim_id"] for row in claims] == expected_ids

    controlled_outcomes = set(
        contract["controlled_values"]["claim_assessment_outcomes"]
    )

    actual_outcomes = {}

    for row in claims:
        assert set(row) == REQUIRED_CLAIM_FIELDS

        cid = row["claim_id"]
        outcome = row["assessment_outcome"]

        assert outcome in controlled_outcomes
        actual_outcomes[cid] = outcome

        unresolved = row["unresolved_owner_question_ids"]

        if cid in EXPECTED_UNRESOLVED:
            assert unresolved == [f"{cid}-OWNER-QUESTION"]
        else:
            assert unresolved == []

    assert actual_outcomes == EXPECTED_OUTCOMES

    recomputed = dict(
        sorted(
            Counter(actual_outcomes.values()).items()
        )
    )

    assert recomputed == EXPECTED_COUNTS
    assert data["counts_by_assessment_outcome"] == EXPECTED_COUNTS


def test_r2a9_evidence_structure_and_claim_specific_links():
    data = load(CLAIMS_PATH)
    contract = load(CONTRACT_PATH)

    allowed_relevance = set(
        contract["controlled_values"]["relevance_types"]
    )
    allowed_roles = set(
        contract["controlled_values"]["semantic_roles"]
    )

    surfaces = load_live_surfaces()

    for claim in data["claim_assessments"]:
        cid = claim["claim_id"]
        evidence = claim["evidence"]

        assert set(evidence) == EVIDENCE_FIELDS

        evidence_ids = evidence["surface_ids"]

        assert evidence_ids
        assert len(evidence_ids) == len(set(evidence_ids))

        categorized = []

        for field in EVIDENCE_FIELDS - {"surface_ids"}:
            values = evidence[field]
            assert len(values) == len(set(values))
            categorized.extend(values)

        assert set(categorized) == set(evidence_ids)

        for sid in evidence_ids:
            assert sid in surfaces

        positive_ids = []

        for link in claim["positive_links"]:
            assert set(link) == REQUIRED_LINK_FIELDS

            sid = link["surface_id"]
            positive_ids.append(sid)

            assert sid in evidence_ids
            assert sid in surfaces
            assert link["relevance_type"] in allowed_relevance
            assert link["semantic_role"] in allowed_roles

            exact = link["exact_relevance"].strip()
            boundary = link["owner_boundary_effect"].strip()

            assert exact
            assert len(exact) >= 20
            assert exact.casefold() != "constrains the claim"

            assert boundary
            assert "without transferring semantic ownership" in boundary
            assert "adopting the research claim as doctrine" in boundary

        assert len(positive_ids) == len(set(positive_ids))

        # Every surface ID appearing anywhere in claim prose/structure must
        # be represented in structured evidence.
        mentioned = set(
            SURFACE_ID_RE.findall(
                json.dumps(claim, ensure_ascii=False)
            )
        )

        assert mentioned <= set(evidence_ids)

        summary = claim["assessment_summary"].strip()

        assert summary
        assert len(summary) >= 40
        assert cid not in summary


def test_r2a9_live_positive_link_reciprocity_is_exact():
    data = load(CLAIMS_PATH)
    surfaces = load_live_surfaces()

    expected = defaultdict(list)

    for claim in data["claim_assessments"]:
        cid = claim["claim_id"]

        for link in claim["positive_links"]:
            expected[link["surface_id"]].append(
                (cid, link["exact_relevance"])
            )

    assert len(surfaces) == 58
    assert len(expected) == 25
    assert sum(len(v) for v in expected.values()) == 75

    for sid, surface in surfaces.items():
        expected_pairs = expected.get(sid, [])

        expected_ids = [
            cid
            for cid, _reason in expected_pairs
        ]
        expected_reasons = [
            reason
            for _cid, reason in expected_pairs
        ]

        actual_ids = surface.get("linked_r2_claim_ids", [])
        actual_reasons = surface.get("claim_link_reasons", [])

        assert len(actual_ids) == len(actual_reasons)
        assert actual_ids == expected_ids
        assert actual_reasons == expected_reasons

    # Reciprocal links cannot reference claims outside this R2A-9 range
    # while this partition is the current successor.
    allowed_claims = set(EXPECTED_OUTCOMES)

    for surface in surfaces.values():
        assert set(surface.get("linked_r2_claim_ids", [])) <= allowed_claims


MANIFEST_PATH = (
    "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml"
)


def test_r2a9_manifest_completion_progression_is_bounded():
    predecessor = json.loads(
        git(
            "show",
            f"{BASE}:{MANIFEST_PATH}",
        )
    )
    current = load(MANIFEST_PATH)

    assert predecessor["artifact_version"] == "0.2.15"
    assert current["artifact_version"] == "0.2.16"

    assert predecessor["status"] == "active_incomplete"
    assert current["status"] == "active_incomplete"

    predecessor_by_partition = {
        row["partition_id"]: row
        for row in predecessor["partitions"]
    }
    current_by_partition = {
        row["partition_id"]: row
        for row in current["partitions"]
    }

    # R2A-8 remains exactly certified.
    assert predecessor_by_partition["R2A-8"]["status"] == "complete"
    assert (
        current_by_partition["R2A-8"]
        == predecessor_by_partition["R2A-8"]
    )

    # R2A-9 alone advances.
    assert (
        predecessor_by_partition["R2A-9"]["status"]
        == "planned_not_present"
    )
    assert current_by_partition["R2A-9"]["status"] == "complete"

    r2a9 = current_by_partition["R2A-9"]

    assert r2a9["owned_artifact_types"] == ["claim_assessment"]
    assert r2a9["dependency_partitions"] == ["R2A-8"]
    assert r2a9["maximum_changed_files"] == 7
    assert r2a9["maximum_additions"] == 2500
    assert r2a9["planned_artifact_paths"] == [CLAIMS_PATH]
    assert r2a9["gate_effect"] == "R2A remains active_incomplete."

    # No later partition begins.
    for partition_id in ("R2A-10", "R2A-11", "R2A-12"):
        assert (
            current_by_partition[partition_id]
            == predecessor_by_partition[partition_id]
        )
        assert (
            current_by_partition[partition_id]["status"]
            == "planned_not_present"
        )

    # Strong successor check: after normalizing exactly the two
    # authorized fields, the current manifest must equal its predecessor.
    normalized = json.loads(json.dumps(current))
    normalized["artifact_version"] = predecessor["artifact_version"]

    normalized_by_partition = {
        row["partition_id"]: row
        for row in normalized["partitions"]
    }
    normalized_by_partition["R2A-9"]["status"] = (
        predecessor_by_partition["R2A-9"]["status"]
    )

    assert normalized == predecessor

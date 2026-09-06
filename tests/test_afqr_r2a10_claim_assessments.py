"""Executable semantic verification for AFQR R2A-10 claims 0017-0031."""
from __future__ import annotations

import copy
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BASE = "0977a5be945f14460ad28e099001d4c7009936cd"
R2A9_CERTIFIED_HEAD = "1241816ab4b23ebe946743dd07f40ccada43da2b"
R2A10_CERTIFIED_HEAD = "91093c760aac87c01305322a6c1656cab5070cfb"

CLAIMS_PATH = (
    "docs/doctrine/reviews/r2a/"
    "claim_assessments_0017_0031/index.yaml"
)
R2A9_CLAIMS_PATH = (
    "docs/doctrine/reviews/r2a/"
    "claim_assessments_0001_0016/index.yaml"
)
LEDGER_PATH = (
    "docs/doctrine/reviews/"
    "afqr_r2_continuity_claim_and_owner_routing_ledger.yaml"
)
CONTRACT_PATH = "docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml"
MANIFEST_PATH = "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml"
CORE_INDEX_PATH = (
    "docs/doctrine/reviews/r2a/semantic_core_agency/index.yaml"
)
WORLD_INDEX_PATH = (
    "docs/doctrine/reviews/r2a/semantic_world_coordination/index.yaml"
)
CORE_SHARD_PATH = (
    "docs/doctrine/reviews/r2a/semantic_core_agency/surfaces_0001.yaml"
)
WORLD_SHARD_PATH = (
    "docs/doctrine/reviews/r2a/"
    "semantic_world_coordination/surfaces_0001.yaml"
)

EXPECTED_OUTCOMES = {
    "R2-CLAIM-0017": "implementation_or_schema_presupposition_only",
    "R2-CLAIM-0018": "historical_or_source_local_pressure_only",
    "R2-CLAIM-0019": "governed_by_existing_owner",
    "R2-CLAIM-0020": "governed_by_existing_owner",
    "R2-CLAIM-0021": "partially_governed_owner_gap_remains",
    "R2-CLAIM-0022": "governed_by_existing_owner",
    "R2-CLAIM-0023": "historical_or_source_local_pressure_only",
    "R2-CLAIM-0024": "governed_by_existing_owner",
    "R2-CLAIM-0025": "no_material_authority_relation",
    "R2-CLAIM-0026": "no_material_authority_relation",
    "R2-CLAIM-0027": "no_material_authority_relation",
    "R2-CLAIM-0028": "partially_governed_owner_gap_remains",
    "R2-CLAIM-0029": "partially_governed_owner_gap_remains",
    "R2-CLAIM-0030": "historical_or_source_local_pressure_only",
    "R2-CLAIM-0031": "implementation_or_schema_presupposition_only",
}

EXPECTED_COUNTS = {
    "governed_by_existing_owner": 4,
    "historical_or_source_local_pressure_only": 3,
    "implementation_or_schema_presupposition_only": 2,
    "no_material_authority_relation": 3,
    "partially_governed_owner_gap_remains": 3,
}

EXPECTED_UNRESOLVED = {
    "R2-CLAIM-0021",
    "R2-CLAIM-0028",
    "R2-CLAIM-0029",
    "R2-CLAIM-0031",
}

REQUIRED_TOP_LEVEL_FIELDS = {
    "artifact_id",
    "artifact_version",
    "status",
    "phase",
    "authority_effect",
    "inspected_repository_commit",
    "dependencies",
    "source_claim_ledger",
    "assessment_range",
    "semantic_surface_sources",
    "counts_by_assessment_outcome",
    "claim_assessments",
    "completion_assertions",
    "prohibited_inferences",
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

CATEGORY_SURFACE_KINDS = {
    "relevant_current_normative_surface_ids": {
        "current_normative_doctrine",
        "accepted_decision",
    },
    "relevant_current_control_surface_ids": {"current_control_or_gate"},
    "relevant_schema_runtime_test_surface_ids": {
        "schema_presupposition",
        "runtime_presupposition",
        "test_contract",
        "narrow_fixture",
    },
    "relevant_historical_or_source_local_surface_ids": {
        "historical_doctrine",
        "deprecated_doctrine",
        "source_local_pressure",
        "conversion_handoff_pressure",
        "canon_handoff_pressure",
        "example_or_benchmark",
    },
    "negative_or_absence_evidence_surface_ids": {
        "negative_or_absence_evidence"
    },
}

RELEVANCE_CATEGORY = {
    "decisive_current_authority": "relevant_current_normative_surface_ids",
    "supporting_current_authority": "relevant_current_normative_surface_ids",
    "implementation_presupposition": (
        "relevant_schema_runtime_test_surface_ids"
    ),
    "schema_presupposition": "relevant_schema_runtime_test_surface_ids",
    "control_or_gate_evidence": "relevant_current_control_surface_ids",
    "historical_or_source_local_pressure": (
        "relevant_historical_or_source_local_surface_ids"
    ),
    "negative_evidence": "negative_or_absence_evidence_surface_ids",
}

SURFACE_ID_RE = re.compile(r"R2A-SURFACE-[A-Z]+-\d{4}")

AUTHORIZED_PATHS = {
    CLAIMS_PATH,
    CORE_SHARD_PATH,
    WORLD_SHARD_PATH,
    MANIFEST_PATH,
    "tests/test_afqr_r2a8_aggregate_receipts.py",
    "tests/test_afqr_r2a9_claim_assessments.py",
    "tests/test_afqr_r2a10_claim_assessments.py",
}


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def git_bytes(ref: str, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
    )


def load_surfaces_at(ref: str | None = None):
    surfaces = {}

    for path in (CORE_SHARD_PATH, WORLD_SHARD_PATH):
        if ref is None:
            shard = load(path)
        else:
            shard = json.loads(git_bytes(ref, path))

        for row in shard["surface_records"]:
            sid = row["surface_id"]
            assert sid not in surfaces
            surfaces[sid] = row

    return surfaces


def expected_reciprocal_pairs(*artifacts):
    expected = defaultdict(list)

    for artifact in artifacts:
        for claim in artifact["claim_assessments"]:
            for link in claim["positive_links"]:
                expected[link["surface_id"]].append(
                    (claim["claim_id"], link["exact_relevance"])
                )

    return expected


def assert_exact_reciprocity(surfaces, expected):
    for sid, surface in surfaces.items():
        pairs = expected.get(sid, [])
        expected_ids = [cid for cid, _reason in pairs]
        expected_reasons = [reason for _cid, reason in pairs]
        actual_ids = surface.get("linked_r2_claim_ids", [])
        actual_reasons = surface.get("claim_link_reasons", [])

        assert len(actual_ids) == len(actual_reasons)
        assert len(actual_ids) == len(set(actual_ids))
        assert actual_ids == sorted(actual_ids)
        assert actual_ids == expected_ids
        assert actual_reasons == expected_reasons


def validate_claim_records(data, contract, surfaces, ledger):
    claims = data["claim_assessments"]
    expected_ids = [
        f"R2-CLAIM-{number:04d}"
        for number in range(17, 32)
    ]

    assert len(claims) == 15
    assert [row["claim_id"] for row in claims] == expected_ids
    assert len({row["claim_id"] for row in claims}) == 15

    controlled_outcomes = set(
        contract["controlled_values"]["claim_assessment_outcomes"]
    )
    allowed_relevance = set(
        contract["controlled_values"]["relevance_types"]
    )
    allowed_roles = set(
        contract["controlled_values"]["semantic_roles"]
    )

    ledger_rows = {
        row["claim_id"]: row
        for row in ledger["claims"]
        if row["claim_id"] in expected_ids
    }
    assert set(ledger_rows) == set(expected_ids)

    all_reasons = []
    actual_outcomes = {}

    for claim in claims:
        assert set(claim) == REQUIRED_CLAIM_FIELDS

        cid = claim["claim_id"]
        outcome = claim["assessment_outcome"]
        evidence = claim["evidence"]

        assert outcome in controlled_outcomes
        actual_outcomes[cid] = outcome
        assert set(evidence) == EVIDENCE_FIELDS

        evidence_ids = evidence["surface_ids"]
        categorized = []

        assert len(evidence_ids) == len(set(evidence_ids))

        for field, allowed_kinds in CATEGORY_SURFACE_KINDS.items():
            values = evidence[field]
            assert len(values) == len(set(values))
            categorized.extend(values)

            for sid in values:
                assert sid in surfaces
                assert surfaces[sid]["semantic_status"] == "validated"
                assert surfaces[sid]["surface_kind"] in allowed_kinds

        assert len(categorized) == len(set(categorized))
        assert set(categorized) == set(evidence_ids)

        if outcome == "no_material_authority_relation":
            assert evidence_ids == []
            assert claim["positive_links"] == []
        else:
            assert evidence_ids

        positive_ids = []

        for link in claim["positive_links"]:
            assert set(link) == REQUIRED_LINK_FIELDS

            sid = link["surface_id"]
            relevance = link["relevance_type"]
            exact = link["exact_relevance"].strip()
            boundary = link["owner_boundary_effect"].strip()

            positive_ids.append(sid)
            all_reasons.append(exact)

            assert sid in evidence_ids
            assert sid in surfaces
            assert relevance in allowed_relevance
            assert link["semantic_role"] in allowed_roles
            assert sid in evidence[RELEVANCE_CATEGORY[relevance]]
            assert exact
            assert len(exact) >= 40
            assert exact.casefold() != "constrains the claim"
            assert "without transferring semantic ownership" in boundary
            assert "adopting the research claim as doctrine" in boundary

        assert len(positive_ids) == len(set(positive_ids))

        mentioned = set(
            SURFACE_ID_RE.findall(json.dumps(claim, ensure_ascii=False))
        )
        assert mentioned <= set(evidence_ids)

        summary = claim["assessment_summary"].strip()
        assert len(summary) >= 60
        assert cid not in summary

        source_question = ledger_rows[cid]["owner_analysis"][
            "unresolved_owner_question"
        ]
        expected_questions = (
            [f"{cid}-OWNER-QUESTION"]
            if source_question is not None
            else []
        )
        assert claim["unresolved_owner_question_ids"] == expected_questions

    assert actual_outcomes == EXPECTED_OUTCOMES
    assert Counter(actual_outcomes.values()) == Counter(EXPECTED_COUNTS)
    assert data["counts_by_assessment_outcome"] == EXPECTED_COUNTS
    assert len(all_reasons) == 55
    assert len(all_reasons) == len(set(all_reasons))


def test_r2a10_artifact_identity_range_and_source_traceability():
    data = load(CLAIMS_PATH)

    assert set(data) == REQUIRED_TOP_LEVEL_FIELDS
    assert data["artifact_id"] == "AFQR-R2A-10-CLAIM-ASSESSMENT-INDEX-001"
    assert data["artifact_version"] == "0.1.0"
    assert data["status"] == "complete"
    assert data["phase"] == "R2A-10"
    assert data["authority_effect"] == "nonauthoritative_claim_assessment"
    assert data["inspected_repository_commit"] == BASE
    assert data["dependencies"] == ["R2A-2", "R2A-3", "R2A-8", "R2A-9"]
    assert data["assessment_range"] == {
        "first_claim_id": "R2-CLAIM-0017",
        "last_claim_id": "R2-CLAIM-0031",
        "claim_count": 15,
    }
    assert data["semantic_surface_sources"] == [
        CORE_INDEX_PATH,
        WORLD_INDEX_PATH,
    ]

    source = data["source_claim_ledger"]
    assert source["path"] == LEDGER_PATH
    assert source["authority_effect"] == "tracking_review_only"
    assert git("rev-parse", f"{BASE}:{LEDGER_PATH}") == source["git_blob_sha"]


def test_r2a10_claim_records_satisfy_inventory_contract():
    data = load(CLAIMS_PATH)
    contract = load(CONTRACT_PATH)
    surfaces = load_surfaces_at()
    ledger = load(LEDGER_PATH)

    validate_claim_records(data, contract, surfaces, ledger)

    actual_unresolved = {
        row["claim_id"]
        for row in data["claim_assessments"]
        if row["unresolved_owner_question_ids"]
    }
    assert actual_unresolved == EXPECTED_UNRESOLVED


def test_r2a10_outlier_boundaries_remain_explicit():
    rows = {
        row["claim_id"]: row
        for row in load(CLAIMS_PATH)["claim_assessments"]
    }

    assert "runtime/substrate obligations" in rows["R2-CLAIM-0017"][
        "assessment_summary"
    ]
    assert "R3" in rows["R2-CLAIM-0020"]["assessment_summary"]
    assert "R2A-11" in rows["R2-CLAIM-0021"]["assessment_summary"]
    assert "adapter" in rows["R2-CLAIM-0022"]["assessment_summary"]
    assert "consumers rather than truth or canon owners" in rows[
        "R2-CLAIM-0022"
    ]["assessment_summary"]
    assert "substantive semantic nontransfer" in rows[
        "R2-CLAIM-0024"
    ]["assessment_summary"]

    for number in range(25, 28):
        row = rows[f"R2-CLAIM-{number:04d}"]
        assert row["assessment_outcome"] == "no_material_authority_relation"
        assert row["evidence"]["surface_ids"] == []
        assert row["positive_links"] == []

    for number in (28, 29):
        row = rows[f"R2-CLAIM-{number:04d}"]
        assert row["assessment_outcome"] == (
            "partially_governed_owner_gap_remains"
        )
        assert "R2A-11" in row["assessment_summary"]

    recap = rows["R2-CLAIM-0030"]["assessment_summary"]
    assert "GM adapter only" in recap
    assert "consumer" in recap
    assert "no doctrine, canon, truth, or AFQR authority" in recap

    reservation = rows["R2-CLAIM-0031"]
    assert reservation["assessment_outcome"] == (
        "implementation_or_schema_presupposition_only"
    )
    assert "AFQR-07 already owns" in reservation["assessment_summary"]
    assert "journal a quantity owner" in reservation["assessment_summary"]


def test_r2a10_live_reciprocity_composes_exactly_with_r2a9():
    r2a9 = load(R2A9_CLAIMS_PATH)
    r2a10 = load(CLAIMS_PATH)
    surfaces = load_surfaces_at()
    expected = expected_reciprocal_pairs(r2a9, r2a10)

    assert len(surfaces) == 58
    assert len(expected) == 30
    assert sum(len(pairs) for pairs in expected.values()) == 130
    assert_exact_reciprocity(surfaces, expected)


def test_r2a9_endpoint_is_historical_and_semantic_indexes_stay_anchored():
    assert git("rev-parse", f"{BASE}^{{tree}}") == git(
        "rev-parse",
        f"{R2A9_CERTIFIED_HEAD}^{{tree}}",
    )

    certified_surfaces = load_surfaces_at(R2A9_CERTIFIED_HEAD)
    r2a9 = json.loads(git_bytes(R2A9_CERTIFIED_HEAD, R2A9_CLAIMS_PATH))
    expected = expected_reciprocal_pairs(r2a9)

    assert sum(len(pairs) for pairs in expected.values()) == 75
    assert_exact_reciprocity(certified_surfaces, expected)

    for index_path in (CORE_INDEX_PATH, WORLD_INDEX_PATH):
        assert (ROOT / index_path).read_bytes() == git_bytes(
            R2A9_CERTIFIED_HEAD,
            index_path,
        )


def test_r2a10_surface_mutation_is_link_only_and_successor_bounded():
    for path in (CORE_SHARD_PATH, WORLD_SHARD_PATH):
        predecessor = json.loads(git_bytes(R2A9_CERTIFIED_HEAD, path))
        current = load(path)

        assert predecessor["artifact_version"] == "0.3.1"
        assert current["artifact_version"] == "0.3.2"

        normalized = copy.deepcopy(current)
        normalized["artifact_version"] = predecessor["artifact_version"]

        predecessor_by_id = {
            row["surface_id"]: row
            for row in predecessor["surface_records"]
        }
        normalized_by_id = {
            row["surface_id"]: row
            for row in normalized["surface_records"]
        }

        assert list(normalized_by_id) == list(predecessor_by_id)

        for sid, row in normalized_by_id.items():
            old = predecessor_by_id[sid]
            row["linked_r2_claim_ids"] = old["linked_r2_claim_ids"]
            row["claim_link_reasons"] = old["claim_link_reasons"]

        assert normalized == predecessor


def test_r2a10_manifest_transition_is_exact_and_gate_stays_incomplete():
    predecessor = json.loads(git_bytes(BASE, MANIFEST_PATH))
    current = json.loads(git_bytes(R2A10_CERTIFIED_HEAD, MANIFEST_PATH))

    assert predecessor["artifact_version"] == "0.2.16"
    assert current["artifact_version"] == "0.2.17"
    assert predecessor["status"] == current["status"] == "active_incomplete"

    predecessor_by_id = {
        row["partition_id"]: row
        for row in predecessor["partitions"]
    }
    current_by_id = {
        row["partition_id"]: row
        for row in current["partitions"]
    }

    assert predecessor_by_id["R2A-10"]["status"] == "planned_not_present"
    assert current_by_id["R2A-10"]["status"] == "complete"

    r2a10 = current_by_id["R2A-10"]
    assert r2a10["owned_artifact_types"] == ["claim_assessment"]
    assert r2a10["dependency_partitions"] == ["R2A-8", "R2A-9"]
    assert r2a10["maximum_changed_files"] == 7
    assert r2a10["maximum_additions"] == 2500
    assert r2a10["planned_artifact_paths"] == [CLAIMS_PATH]
    assert r2a10["gate_effect"] == "R2A remains active_incomplete."

    assert current_by_id["R2A-9"]["status"] == "complete"
    assert current_by_id["R2A-11"]["status"] == "planned_not_present"
    assert current_by_id["R2A-12"]["status"] == "planned_not_present"

    normalized = copy.deepcopy(current)
    normalized["artifact_version"] = predecessor["artifact_version"]
    normalized_by_id = {
        row["partition_id"]: row
        for row in normalized["partitions"]
    }
    normalized_by_id["R2A-10"]["status"] = predecessor_by_id[
        "R2A-10"
    ]["status"]
    assert normalized == predecessor

    contract = load(CONTRACT_PATH)
    assert contract["project_posture"]["R2A"] == "active_incomplete"
    assert contract["project_posture"]["R2B"] == "blocked"

    certified_paths = set(
        git(
            "ls-tree",
            "-r",
            "--name-only",
            R2A10_CERTIFIED_HEAD,
        ).splitlines()
    )
    assert (
        current_by_id["R2A-11"]["planned_artifact_paths"][0]
        not in certified_paths
    )
    assert (
        current_by_id["R2A-12"]["planned_artifact_paths"][0]
        not in certified_paths
    )


def test_r2a10_adversarial_claim_mutations_fail_closed():
    data = load(CLAIMS_PATH)
    contract = load(CONTRACT_PATH)
    surfaces = load_surfaces_at()
    ledger = load(LEDGER_PATH)
    mutations = []

    bad = copy.deepcopy(data)
    bad["claim_assessments"][0]["assessment_outcome"] = "adopted_doctrine"
    mutations.append(bad)

    bad = copy.deepcopy(data)
    bad["claim_assessments"][1]["claim_id"] = "R2-CLAIM-0017"
    mutations.append(bad)

    bad = copy.deepcopy(data)
    bad["claim_assessments"][0]["evidence"]["surface_ids"].append(
        "R2A-SURFACE-CORE-9999"
    )
    mutations.append(bad)

    bad = copy.deepcopy(data)
    bad["claim_assessments"][0]["positive_links"][0][
        "exact_relevance"
    ] = "constrains the claim"
    mutations.append(bad)

    bad = copy.deepcopy(data)
    bad["claim_assessments"][4]["unresolved_owner_question_ids"] = []
    mutations.append(bad)

    bad = copy.deepcopy(data)
    bad["claim_assessments"][5]["unresolved_owner_question_ids"] = [
        "R2-CLAIM-0022-OWNER-QUESTION"
    ]
    mutations.append(bad)

    bad = copy.deepcopy(data)
    bad["claim_assessments"][8]["evidence"]["surface_ids"] = [
        "R2A-SURFACE-CORE-0003"
    ]
    mutations.append(bad)

    for mutated in mutations:
        try:
            validate_claim_records(mutated, contract, surfaces, ledger)
        except AssertionError:
            continue
        raise AssertionError("adversarial claim mutation passed validation")


def test_r2a10_branch_scope_and_caps_are_exact():
    changed = set(
        git(
            "diff",
            "--name-only",
            BASE,
            R2A10_CERTIFIED_HEAD,
        ).splitlines()
    )

    assert changed == AUTHORIZED_PATHS
    assert not git(
        "diff",
        "--name-status",
        "--diff-filter=D",
        BASE,
        R2A10_CERTIFIED_HEAD,
    )

    numstat = git(
        "diff",
        "--numstat",
        BASE,
        R2A10_CERTIFIED_HEAD,
    ).splitlines()
    assert "-\t-" not in "\n".join(numstat)
    additions = sum(int(row.split("\t")[0]) for row in numstat if row)

    assert len(changed) <= 7
    assert additions <= 2500

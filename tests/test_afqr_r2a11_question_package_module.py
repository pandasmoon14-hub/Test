"""Executable semantic verification for AFQR R2A-11 question/package/module synthesis."""
from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BASE = "b1873f8771bc1a1700076936737c80d5df50fdc1"
R2A11_CERTIFIED_HEAD = "d3a5c7f17a4709e2422661d8063e6a134a857798"

ARTIFACT_PATH = (
    "docs/doctrine/reviews/r2a/question_package_module/index.yaml"
)
R2A9_CLAIMS_PATH = (
    "docs/doctrine/reviews/r2a/"
    "claim_assessments_0001_0016/index.yaml"
)
R2A10_CLAIMS_PATH = (
    "docs/doctrine/reviews/r2a/"
    "claim_assessments_0017_0031/index.yaml"
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

EXPECTED_QUESTION_OUTCOMES = {
    "R2-CLAIM-0001-OWNER-QUESTION": (
        "partially_governed_owner_gap_remains"
    ),
    "R2-CLAIM-0003-OWNER-QUESTION": (
        "partially_governed_owner_gap_remains"
    ),
    "R2-CLAIM-0008-OWNER-QUESTION": (
        "partially_governed_owner_gap_remains"
    ),
    "R2-CLAIM-0010-OWNER-QUESTION": (
        "partially_governed_owner_gap_remains"
    ),
    "R2-CLAIM-0011-OWNER-QUESTION": "governed_by_existing_owner",
    "R2-CLAIM-0014-OWNER-QUESTION": "governed_by_existing_owner",
    "R2-CLAIM-0016-OWNER-QUESTION": "governed_by_existing_owner",
    "R2-CLAIM-0021-OWNER-QUESTION": (
        "partially_governed_owner_gap_remains"
    ),
    "R2-CLAIM-0028-OWNER-QUESTION": "governed_by_existing_owner",
    "R2-CLAIM-0029-OWNER-QUESTION": "preserved_unresolved",
    "R2-CLAIM-0031-OWNER-QUESTION": "governed_by_existing_owner",
}

EXPECTED_QUESTION_COUNTS = {
    "partially_governed_owner_gap_remains": 5,
    "governed_by_existing_owner": 5,
    "preserved_unresolved": 1,
}

EXPECTED_PACKAGE_OUTCOMES = {
    "R2B-CORE": "required_pending_authorization",
    "R2B-AGENCY": "not_required",
    "R2B-WORLD": "not_required",
    "R2B-CONTINUITY": "required_pending_authorization",
    "R2B-CROSS-PHASE": "required_pending_authorization",
}

EXPECTED_PACKAGE_COUNTS = {
    "required_pending_authorization": 3,
    "not_required": 2,
}

EXPECTED_MODULE_OUTCOMES = {
    "R2B-CORE-MOD-PREVIEW-PERSISTENCE-PROMOTION": (
        "required_pending_authorization"
    ),
    "R2B-CORE-MOD-CORRECTION-RNG-IDENTITY": (
        "required_pending_authorization"
    ),
    "R2B-CONTINUITY-MOD-TIMELINE-IDENTITY-QUALIFICATION": (
        "required_pending_authorization"
    ),
    "R2B-CONTINUITY-MOD-BITEMPORAL-QUALIFICATION": (
        "required_pending_authorization"
    ),
    "R2B-CONTINUITY-MOD-BRANCH-CANONICALITY-ANCESTRY": (
        "required_pending_authorization"
    ),
    "R2B-CONTINUITY-MOD-CORRECTION-GOVERNANCE": (
        "required_pending_authorization"
    ),
    "R2B-CONTINUITY-MOD-RULESET-PACKAGE-OVERRIDE-VERSIONS": (
        "not_required"
    ),
    "R2B-CONTINUITY-MOD-SESSION-CLOSURE-SNAPSHOT": "not_required",
    "R2B-CONTINUITY-MOD-BRANCH-SAFE-PROJECTION": (
        "required_pending_authorization"
    ),
    "R2B-CROSS-PHASE-MOD-VERSION-IDENTITY-EFFECTIVITY": (
        "required_pending_authorization"
    ),
}

EXPECTED_MODULE_COUNTS = {
    "required_pending_authorization": 8,
    "not_required": 2,
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
    "claim_assessment_sources",
    "semantic_surface_sources",
    "question_universe",
    "counts_by_question_assessment_outcome",
    "unresolved_question_assessments",
    "candidate_package_universe",
    "counts_by_package_assessment_outcome",
    "package_assessments",
    "counts_by_module_assessment_outcome",
    "module_assessments",
    "completion_assertions",
    "prohibited_inferences",
}

REQUIRED_QUESTION_FIELDS = {
    "question_id",
    "assessment_outcome",
    "evidence",
    "positive_links",
    "owner_boundary",
    "downstream_gate",
}

REQUIRED_PACKAGE_FIELDS = {
    "package_id",
    "assessment_outcome",
    "evidence",
    "rationale",
    "gate_effect",
}

REQUIRED_MODULE_FIELDS = {
    "module_id",
    "package_id",
    "assessment_outcome",
    "evidence",
    "declared_owner",
    "prohibited_owner_transfers",
}

SYNTHESIS_EVIDENCE_FIELDS = {"claim_ids", "question_ids"}

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

QUESTION_RE = re.compile(r"^(R2-CLAIM-\d{4})-OWNER-QUESTION$")

AUTHORIZED_PATHS = {
    ARTIFACT_PATH,
    MANIFEST_PATH,
    "tests/test_afqr_r2a10_claim_assessments.py",
    "tests/test_afqr_r2a11_question_package_module.py",
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


def load_surfaces():
    surfaces = {}
    for path in (CORE_SHARD_PATH, WORLD_SHARD_PATH):
        shard = load(path)
        for row in shard["surface_records"]:
            sid = row["surface_id"]
            assert sid not in surfaces
            surfaces[sid] = row
    return surfaces


def load_claims():
    r2a9 = load(R2A9_CLAIMS_PATH)
    r2a10 = load(R2A10_CLAIMS_PATH)
    rows = r2a9["claim_assessments"] + r2a10["claim_assessments"]
    by_id = {row["claim_id"]: row for row in rows}
    assert len(rows) == len(by_id) == 31
    assert list(by_id) == [
        f"R2-CLAIM-{number:04d}"
        for number in range(1, 32)
    ]
    return r2a9, r2a10, by_id


def validate_question_evidence(
    question,
    parent_claim,
    contract,
    surfaces,
):
    evidence = question["evidence"]
    links = question["positive_links"]

    assert set(evidence) == EVIDENCE_FIELDS

    allowed_relevance = set(
        contract["controlled_values"]["relevance_types"]
    )
    allowed_roles = set(contract["controlled_values"]["semantic_roles"])

    evidence_ids = evidence["surface_ids"]
    categorized = []

    assert evidence_ids
    assert len(evidence_ids) == len(set(evidence_ids))
    assert set(evidence_ids) <= set(parent_claim["evidence"]["surface_ids"])

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

    linked_ids = []
    for link in links:
        assert set(link) == REQUIRED_LINK_FIELDS

        sid = link["surface_id"]
        relevance = link["relevance_type"]
        exact = link["exact_relevance"].strip()
        boundary = link["owner_boundary_effect"].strip()

        linked_ids.append(sid)

        assert sid in evidence_ids
        assert relevance in allowed_relevance
        assert link["semantic_role"] in allowed_roles
        assert sid in evidence[RELEVANCE_CATEGORY[relevance]]
        assert len(exact) >= 50
        assert exact.casefold() != "constrains the claim"
        assert "without transferring semantic ownership" in boundary
        assert "adopting the research claim as doctrine" in boundary

    assert linked_ids == evidence_ids
    assert len(linked_ids) == len(set(linked_ids))


def test_r2a11_artifact_identity_and_source_traceability():
    data = load(ARTIFACT_PATH)

    assert set(data) == REQUIRED_TOP_LEVEL_FIELDS
    assert data["artifact_id"] == (
        "AFQR-R2A-11-QUESTION-PACKAGE-MODULE-INDEX-001"
    )
    assert data["artifact_version"] == "0.1.0"
    assert data["status"] == "complete"
    assert data["phase"] == "R2A-11"
    assert data["authority_effect"] == (
        "nonauthoritative_question_package_module_assessment"
    )
    assert data["inspected_repository_commit"] == BASE
    assert data["dependencies"] == [
        "R2A-2",
        "R2A-3",
        "R2A-8",
        "R2A-9",
        "R2A-10",
    ]

    source = data["source_claim_ledger"]
    assert source == {
        "path": LEDGER_PATH,
        "git_blob_sha": git("rev-parse", f"{BASE}:{LEDGER_PATH}"),
        "authority_effect": "tracking_review_only",
    }

    expected_claim_sources = {
        R2A9_CLAIMS_PATH: ("R2A-9", "complete"),
        R2A10_CLAIMS_PATH: ("R2A-10", "complete"),
    }
    actual_paths = set()

    for row in data["claim_assessment_sources"]:
        assert set(row) == {"path", "git_blob_sha", "phase", "status"}
        path = row["path"]
        assert path in expected_claim_sources
        assert path not in actual_paths
        actual_paths.add(path)
        expected_phase, expected_status = expected_claim_sources[path]
        assert row["phase"] == expected_phase
        assert row["status"] == expected_status
        assert row["git_blob_sha"] == git("rev-parse", f"{BASE}:{path}")

    assert actual_paths == set(expected_claim_sources)
    assert data["semantic_surface_sources"] == [
        CORE_INDEX_PATH,
        WORLD_INDEX_PATH,
    ]


def test_r2a11_exact_question_universe_and_contract_compliance():
    data = load(ARTIFACT_PATH)
    contract = load(CONTRACT_PATH)
    ledger = load(LEDGER_PATH)
    surfaces = load_surfaces()
    _r2a9, _r2a10, claims = load_claims()

    ledger_questions = []
    for row in ledger["claims"]:
        source_question = row["owner_analysis"]["unresolved_owner_question"]
        if source_question is not None:
            ledger_questions.append(f"{row['claim_id']}-OWNER-QUESTION")

    expected_ids = list(EXPECTED_QUESTION_OUTCOMES)

    assert ledger_questions == expected_ids
    assert data["question_universe"] == {
        "question_count": 11,
        "question_ids": expected_ids,
    }

    rows = data["unresolved_question_assessments"]
    assert len(rows) == 11
    assert [row["question_id"] for row in rows] == expected_ids
    assert len({row["question_id"] for row in rows}) == 11

    controlled = set(
        contract["controlled_values"]["question_assessment_outcomes"]
    )
    pressure_routes = set(contract["controlled_values"]["pressure_routes"])
    actual_outcomes = {}

    for row in rows:
        assert set(row) == REQUIRED_QUESTION_FIELDS
        qid = row["question_id"]
        match = QUESTION_RE.fullmatch(qid)
        assert match is not None
        cid = match.group(1)
        assert cid in claims
        assert claims[cid]["unresolved_owner_question_ids"] == [qid]

        ledger_row = next(
            item for item in ledger["claims"]
            if item["claim_id"] == cid
        )
        assert (
            ledger_row["owner_analysis"]["unresolved_owner_question"]
            is not None
        )

        outcome = row["assessment_outcome"]
        assert outcome in controlled
        actual_outcomes[qid] = outcome

        validate_question_evidence(
            row,
            claims[cid],
            contract,
            surfaces,
        )

        boundary = row["owner_boundary"].strip()
        assert len(boundary) >= 120
        assert "owner" in boundary.casefold()
        assert row["downstream_gate"] in pressure_routes

    assert actual_outcomes == EXPECTED_QUESTION_OUTCOMES
    assert Counter(actual_outcomes.values()) == Counter(
        EXPECTED_QUESTION_COUNTS
    )
    assert data["counts_by_question_assessment_outcome"] == (
        EXPECTED_QUESTION_COUNTS
    )


def test_r2a11_question_routes_do_not_manufacture_packages():
    rows = {
        row["question_id"]: row
        for row in load(ARTIFACT_PATH)[
            "unresolved_question_assessments"
        ]
    }

    assert rows["R2-CLAIM-0001-OWNER-QUESTION"][
        "downstream_gate"
    ] == "later_r2b_candidate"
    assert rows["R2-CLAIM-0001-OWNER-QUESTION"][
        "assessment_outcome"
    ] == "partially_governed_owner_gap_remains"
    assert "AFQR-04" in rows["R2-CLAIM-0001-OWNER-QUESTION"][
        "owner_boundary"
    ]
    assert "AFQR-08" in rows["R2-CLAIM-0001-OWNER-QUESTION"][
        "owner_boundary"
    ]

    assert rows["R2-CLAIM-0011-OWNER-QUESTION"][
        "downstream_gate"
    ] == "r4_substrate"
    assert "AFQR-01 owns the commit/closure envelope" in rows[
        "R2-CLAIM-0011-OWNER-QUESTION"
    ]["owner_boundary"]

    assert rows["R2-CLAIM-0014-OWNER-QUESTION"][
        "downstream_gate"
    ] == "r5_retrofit"

    assert rows["R2-CLAIM-0016-OWNER-QUESTION"][
        "assessment_outcome"
    ] == "governed_by_existing_owner"
    assert "AFQR-04 and AFQR-17" in rows[
        "R2-CLAIM-0016-OWNER-QUESTION"
    ]["owner_boundary"]

    assert rows["R2-CLAIM-0028-OWNER-QUESTION"][
        "assessment_outcome"
    ] == "governed_by_existing_owner"
    assert rows["R2-CLAIM-0029-OWNER-QUESTION"][
        "assessment_outcome"
    ] == "preserved_unresolved"
    assert "later frontier" in rows[
        "R2-CLAIM-0029-OWNER-QUESTION"
    ]["owner_boundary"]

    assert rows["R2-CLAIM-0031-OWNER-QUESTION"][
        "downstream_gate"
    ] == "r4_substrate"


def test_r2a11_package_synthesis_consumes_all_claims_and_questions():
    data = load(ARTIFACT_PATH)
    contract = load(CONTRACT_PATH)
    r2a9, r2a10, claims = load_claims()
    questions = {
        row["question_id"]
        for row in data["unresolved_question_assessments"]
    }

    assert r2a9["status"] == r2a10["status"] == "complete"
    assert set(claims) == {
        f"R2-CLAIM-{number:04d}"
        for number in range(1, 32)
    }
    assert questions == set(EXPECTED_QUESTION_OUTCOMES)

    expected_universe = list(EXPECTED_PACKAGE_OUTCOMES)
    assert data["candidate_package_universe"] == expected_universe

    rows = data["package_assessments"]
    assert len(rows) == 5
    assert [row["package_id"] for row in rows] == expected_universe

    controlled = set(
        contract["controlled_values"]["package_assessment_outcomes"]
    )
    actual_outcomes = {}

    for row in rows:
        assert set(row) == REQUIRED_PACKAGE_FIELDS
        pid = row["package_id"]
        outcome = row["assessment_outcome"]
        evidence = row["evidence"]

        assert outcome in controlled
        actual_outcomes[pid] = outcome
        assert set(evidence) == SYNTHESIS_EVIDENCE_FIELDS

        claim_ids = evidence["claim_ids"]
        question_ids = evidence["question_ids"]
        assert len(claim_ids) == len(set(claim_ids))
        assert len(question_ids) == len(set(question_ids))
        assert set(claim_ids) <= set(claims)
        assert set(question_ids) <= questions

        assert len(row["rationale"].strip()) >= 120
        assert len(row["gate_effect"].strip()) >= 80

        if outcome == "required_pending_authorization":
            assert claim_ids
            assert "R2B remains blocked" in row["gate_effect"]

    assert actual_outcomes == EXPECTED_PACKAGE_OUTCOMES
    assert Counter(actual_outcomes.values()) == Counter(
        EXPECTED_PACKAGE_COUNTS
    )
    assert data["counts_by_package_assessment_outcome"] == (
        EXPECTED_PACKAGE_COUNTS
    )

    required = {
        pid for pid, outcome in actual_outcomes.items()
        if outcome == "required_pending_authorization"
    }
    assert required == {
        "R2B-CORE",
        "R2B-CONTINUITY",
        "R2B-CROSS-PHASE",
    }


def test_r2a11_module_synthesis_is_minimal_and_owner_bounded():
    data = load(ARTIFACT_PATH)
    contract = load(CONTRACT_PATH)
    surfaces = load_surfaces()
    _r2a9, _r2a10, claims = load_claims()

    packages = {
        row["package_id"]: row
        for row in data["package_assessments"]
    }
    questions = {
        row["question_id"]
        for row in data["unresolved_question_assessments"]
    }
    required_packages = {
        pid for pid, row in packages.items()
        if row["assessment_outcome"] == "required_pending_authorization"
    }

    accepted_afqr_ids = set()
    for surface in surfaces.values():
        accepted_afqr_ids.update(surface["applicable_afqr_ids"])

    controlled = set(
        contract["controlled_values"]["module_assessment_outcomes"]
    )

    rows = data["module_assessments"]
    assert len(rows) == len(EXPECTED_MODULE_OUTCOMES)
    assert [row["module_id"] for row in rows] == list(
        EXPECTED_MODULE_OUTCOMES
    )

    actual_outcomes = {}

    for row in rows:
        assert set(row) == REQUIRED_MODULE_FIELDS

        mid = row["module_id"]
        pid = row["package_id"]
        outcome = row["assessment_outcome"]
        evidence = row["evidence"]
        owners = row["declared_owner"]
        transfers = row["prohibited_owner_transfers"]

        assert pid in required_packages
        assert outcome in controlled
        actual_outcomes[mid] = outcome

        assert set(evidence) == SYNTHESIS_EVIDENCE_FIELDS
        assert len(evidence["claim_ids"]) == len(
            set(evidence["claim_ids"])
        )
        assert len(evidence["question_ids"]) == len(
            set(evidence["question_ids"])
        )
        assert set(evidence["claim_ids"]) <= set(claims)
        assert set(evidence["question_ids"]) <= questions

        assert isinstance(owners, list)
        assert owners
        assert len(owners) == len(set(owners))
        assert set(owners) <= accepted_afqr_ids

        assert isinstance(transfers, list)
        assert len(transfers) >= 2
        assert all(len(item.strip()) >= 80 for item in transfers)
        assert "separate accepted component owners" in transfers[0]
        assert "super-owner" in transfers[0]

        if outcome == "required_pending_authorization":
            package_evidence = packages[pid]["evidence"]
            assert set(evidence["claim_ids"]) <= set(
                package_evidence["claim_ids"]
            )
            assert set(evidence["question_ids"]) <= set(
                package_evidence["question_ids"]
            )

    assert actual_outcomes == EXPECTED_MODULE_OUTCOMES
    assert Counter(actual_outcomes.values()) == Counter(
        EXPECTED_MODULE_COUNTS
    )
    assert data["counts_by_module_assessment_outcome"] == (
        EXPECTED_MODULE_COUNTS
    )

    assert not any(
        row["package_id"] in {"R2B-AGENCY", "R2B-WORLD"}
        for row in rows
    )


def test_r2a11_candidate_module_vocabulary_is_not_preserved_by_symmetry():
    rows = {
        row["module_id"]: row
        for row in load(ARTIFACT_PATH)["module_assessments"]
    }

    assert rows[
        "R2B-CONTINUITY-MOD-RULESET-PACKAGE-OVERRIDE-VERSIONS"
    ]["assessment_outcome"] == "not_required"
    assert rows[
        "R2B-CROSS-PHASE-MOD-VERSION-IDENTITY-EFFECTIVITY"
    ]["assessment_outcome"] == "required_pending_authorization"

    assert rows[
        "R2B-CONTINUITY-MOD-SESSION-CLOSURE-SNAPSHOT"
    ]["assessment_outcome"] == "not_required"

    required_continuity = {
        mid for mid, row in rows.items()
        if row["package_id"] == "R2B-CONTINUITY"
        and row["assessment_outcome"] == "required_pending_authorization"
    }
    assert required_continuity == {
        "R2B-CONTINUITY-MOD-TIMELINE-IDENTITY-QUALIFICATION",
        "R2B-CONTINUITY-MOD-BITEMPORAL-QUALIFICATION",
        "R2B-CONTINUITY-MOD-BRANCH-CANONICALITY-ANCESTRY",
        "R2B-CONTINUITY-MOD-CORRECTION-GOVERNANCE",
        "R2B-CONTINUITY-MOD-BRANCH-SAFE-PROJECTION",
    }


def test_r2a11_completion_assertions_preserve_gate_and_nonownership():
    data = load(ARTIFACT_PATH)
    assertions = data["completion_assertions"]

    assert assertions == {
        "exactly_eleven_source_owner_questions_assessed": True,
        "all_thirty_one_claim_assessments_consumed_before_package_synthesis": True,
        "all_question_evidence_resolves_to_validated_semantic_surfaces": True,
        "question_assessments_require_no_reciprocal_semantic_surface_mutation": True,
        "all_five_candidate_r2b_packages_assessed": True,
        "modules_exist_only_for_packages_proven_required": True,
        "declared_module_owner_references_are_existing_afqr_component_owners_only": True,
        "continuity_and_cross_phase_coordination_remain_nonowners": True,
        "doctrine_adopted": False,
        "runtime_or_schema_modified": False,
        "r2b_started": False,
        "r2a_12_started": False,
        "r2a_remains_active_incomplete": True,
        "blocking_exceptions": [],
    }

    prohibited = "\n".join(data["prohibited_inferences"]).casefold()
    for fragment in (
        "does not adopt the missing doctrine",
        "does not transfer ownership",
        "not combined owners",
        "continuity coordination",
        "cross-phase",
        "does not complete r2a",
    ):
        assert fragment in prohibited


def test_r2a11_manifest_contract_and_semantic_surfaces_stay_bounded():
    manifest = load(MANIFEST_PATH)
    partitions = {
        row["partition_id"]: row
        for row in manifest["partitions"]
    }
    r2a11 = partitions["R2A-11"]

    assert r2a11["owned_artifact_types"] == [
        "unresolved_question_assessment",
        "package_assessment",
        "module_assessment",
    ]
    assert r2a11["dependency_partitions"] == ["R2A-10"]
    assert r2a11["maximum_changed_files"] == 7
    assert r2a11["maximum_additions"] == 2500
    assert r2a11["planned_artifact_paths"] == [ARTIFACT_PATH]
    assert "cannot begin R2B" in r2a11["gate_effect"]

    for path in (
        R2A9_CLAIMS_PATH,
        R2A10_CLAIMS_PATH,
        CORE_INDEX_PATH,
        WORLD_INDEX_PATH,
        CORE_SHARD_PATH,
        WORLD_SHARD_PATH,
    ):
        assert (ROOT / path).read_bytes() == git_bytes(BASE, path)


def test_r2a11_branch_scope_stays_within_authorized_paths_and_caps():
    historical_range = f"{BASE}...{R2A11_CERTIFIED_HEAD}"

    changed = set(
        git(
            "diff",
            "--name-only",
            historical_range,
        ).splitlines()
    )

    assert changed <= AUTHORIZED_PATHS

    assert not git(
        "diff",
        "--name-status",
        "--diff-filter=D",
        historical_range,
    )

    numstat = git(
        "diff",
        "--numstat",
        historical_range,
    ).splitlines()

    assert "-\t-" not in "\n".join(numstat)

    additions = sum(
        int(row.split("\t")[0])
        for row in numstat
        if row
    )

    assert len(changed) <= 7
    assert additions <= 2500

def test_r2a11_manifest_transition_is_exact_and_gate_remains_closed():
    predecessor = json.loads(git_bytes(BASE, MANIFEST_PATH))
    current = json.loads(
        git_bytes(R2A11_CERTIFIED_HEAD, MANIFEST_PATH)
    )

    assert predecessor["artifact_version"] == "0.2.17"
    assert current["artifact_version"] == "0.2.18"
    assert (
        predecessor["status"]
        == current["status"]
        == "active_incomplete"
    )
    assert predecessor["phase"] == current["phase"] == "R2A"

    predecessor_by_id = {
        row["partition_id"]: row
        for row in predecessor["partitions"]
    }
    current_by_id = {
        row["partition_id"]: row
        for row in current["partitions"]
    }

    assert predecessor_by_id["R2A-10"]["status"] == "complete"
    assert current_by_id["R2A-10"]["status"] == "complete"

    assert (
        predecessor_by_id["R2A-11"]["status"]
        == "planned_not_present"
    )
    assert current_by_id["R2A-11"]["status"] == "complete"

    assert (
        predecessor_by_id["R2A-12"]["status"]
        == current_by_id["R2A-12"]["status"]
        == "planned_not_present"
    )

    normalized = json.loads(json.dumps(current))
    normalized["artifact_version"] = predecessor["artifact_version"]

    normalized_by_id = {
        row["partition_id"]: row
        for row in normalized["partitions"]
    }
    normalized_by_id["R2A-11"]["status"] = (
        predecessor_by_id["R2A-11"]["status"]
    )

    assert normalized == predecessor

    contract = json.loads(
        git_bytes(R2A11_CERTIFIED_HEAD, CONTRACT_PATH)
    )
    assert contract["project_posture"]["R2A"] == "active_incomplete"
    assert contract["project_posture"]["R2B"] == "blocked"

    assert git_bytes(R2A11_CERTIFIED_HEAD, ARTIFACT_PATH)

    for path in current_by_id["R2A-12"]["planned_artifact_paths"]:
        result = subprocess.run(
            [
                "git",
                "cat-file",
                "-e",
                f"{R2A11_CERTIFIED_HEAD}:{path}",
            ],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        assert result.returncode != 0

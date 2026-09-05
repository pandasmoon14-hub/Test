"""Executable verification contract for AFQR R2A-8 aggregate receipts."""
from __future__ import annotations

import collections
import copy
import fnmatch
import hashlib
import io
import json
import re
import subprocess
import unicodedata
from functools import lru_cache
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
FROZEN_BASE = "62e1565ed598345901e92dc04f3b686281418d83"
FROZEN_TREE = "f27b3cd95c27b08ff7ca7a282809bef161c9ae0d"
MATCHER_PATH = "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml"
MATCHER_BLOB = "f0c154ab7703afb8aedc92e1e472492363487a58"
MATCHER_SHA256 = "3a24d8a6644863a66271f3b7d497f4c662cdfcffc40b54a7099c7265870986b9"
RECEIPT_PATH = "docs/doctrine/reviews/r2a/aggregate_receipts/index.yaml"
MANIFEST_PATH = "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml"

EXPECTED_TRACKED = 881
EXPECTED_ELIGIBLE = 851
EXPECTED_EXCLUDED = 30
EXPECTED_CANDIDATES = 825
EXPECTED_OCCURRENCES = 99825
EXPECTED_PARTITIONS = {"R2A-4": 69, "R2A-5": 85, "R2A-6": 164, "R2A-7": 507}
EXPECTED_EXCLUSION_SHA = "270e45eb97cb03d3da45f88874920a105852c94dd65c148e349d86f2b1cdf572"
EXPECTED_TUPLE_SHA = "d10582ac4da24de0c918dbaa56b73482fdd43c4bf6edd11bde0f0520bab80a31"
EXPECTED_PATH_SHA = "28457def56c478100a8baeb9e5067458731ab4518f47d25179a5a643856e5506"
EXPECTED_PATH_BLOB_SHA = "a0d36ead5638fdb9c6a0c4d8f17506d2465d1420855a0a3c81f21b0f092a94fd"
EXPECTED_R7_PATH_SHA = "f5ddc972d65ee8ba366da0136fb692d5b64ec2f9ce3c0690f582db53b7fed1ca"
EXPECTED_R7_PATH_BLOB_SHA = "6c38b13c3982f608b5465af6902a51316dcff5cd256d9b079708424d5c24fec0"
EXPECTED_SURFACES = 58
EXPECTED_MAPPED_CANDIDATES = 441
EXPECTED_MAPPING_EVIDENCE = 1585
EXPECTED_PHASE_EVIDENCE = {"R2A-4": 58, "R2A-5": 5, "R2A-6": 14, "R2A-7": 1508}

DISPOSITION_INDEXES = (
    "docs/doctrine/reviews/r2a/dispositions_current_a/index.yaml",
    "docs/doctrine/reviews/r2a/dispositions_current_b/index.yaml",
    "docs/doctrine/reviews/r2a/dispositions_runtime_schema/index.yaml",
    "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
)
SURFACE_INDEXES = (
    "docs/doctrine/reviews/r2a/semantic_core_agency/index.yaml",
    "docs/doctrine/reviews/r2a/semantic_world_coordination/index.yaml",
)
REQUIRED_DISPOSITION_FIELDS = {
    "candidate_file_id", "partition_id", "path", "inspected_commit",
    "baseline_blob_sha", "controlled_match_count", "matched_terms",
    "matched_search_clusters", "representative_locators", "disposition",
    "mapped_surface_ids", "semantic_review_summary",
    "source_local_pressure_class", "authority_effect", "pressure_route",
    "mapping_evidence", "status_evidence",
}


def git(*args: str, binary: bool = False):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary)


def git_blob(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}", binary=True)


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFC", value).casefold()
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", value))


def boundary(value: str, index: int) -> bool:
    return index < 0 or index >= len(value) or unicodedata.category(value[index])[:1] not in {"L", "N"}


def exclusion_reason(path: str, raw: bytes):
    parts = path.split("/")
    if parts[0] in {".git", "node_modules", "vendor", "dist", "build", "coverage"} or "__pycache__" in parts:
        return "generated_or_vendor_path"
    if b"\0" in raw:
        return "nul_binary"
    try:
        raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return "invalid_utf8"
    return None


def assign_partition(path: str) -> str:
    if (
        path.startswith("docs/doctrine/control/")
        or path.startswith("docs/doctrine/consolidation/")
        or path.startswith("docs/doctrine/operations/")
        or path.startswith("docs/doctrine/schema/")
        or path.startswith("docs/doctrine/world/")
        or path.startswith("docs/decisions/")
    ):
        return "R2A-4"
    if path.startswith("docs/doctrine/reviews/"):
        return "R2A-5"
    if path.startswith("docs/doctrine/"):
        remainder = path[len("docs/doctrine/"):]
        if "/" not in remainder and (
            fnmatch.fnmatchcase(remainder, "*.yaml")
            or fnmatch.fnmatchcase(remainder, "*.md")
        ):
            return "R2A-5"
    if (
        path.startswith("src/")
        or path.startswith("schemas/")
        or path.startswith("tests/runtime/")
        or fnmatch.fnmatchcase(path, "tests/test_runtime_*.py")
        or fnmatch.fnmatchcase(path, "tests/test_*runtime*.py")
    ):
        return "R2A-6"
    return "R2A-7"


def baseline_tree_entries():
    raw = git("ls-tree", "-r", "-z", "--full-tree", FROZEN_BASE, binary=True)
    rows = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path_raw = record.split(b"\t", 1)
        mode, kind, blob = meta.decode("ascii").split()
        if kind == "blob":
            rows.append((path_raw.decode("utf-8"), mode, blob))
    return rows


def cat_blobs(shas):
    unique = list(dict.fromkeys(shas))
    request = b"".join(value.encode("ascii") + b"\n" for value in unique)
    raw = subprocess.check_output(["git", "cat-file", "--batch"], cwd=ROOT, input=request)
    stream = io.BytesIO(raw)
    result = {}
    for requested in unique:
        actual, kind, size = stream.readline().rstrip(b"\n").split()
        assert actual.decode("ascii") == requested
        assert kind == b"blob"
        body = stream.read(int(size))
        assert len(body) == int(size)
        assert stream.read(1) == b"\n"
        result[requested] = body
    assert stream.read() == b""
    return result


def matcher_terms():
    document = json.loads(git_blob(FROZEN_BASE, MATCHER_PATH).decode("utf-8"))
    return {
        cluster["cluster_id"]: [normalize(term) for term in cluster["terms"]]
        for cluster in document["clusters"]
    }


def controlled_matches(path: str, raw: bytes, terms_by_cluster):
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    found = set()
    for line_number, source_line in enumerate(text.split("\n"), 1):
        line = normalize(source_line)
        for cluster_id, terms in terms_by_cluster.items():
            for term in terms:
                start = 0
                while term:
                    at = line.find(term, start)
                    if at < 0:
                        break
                    if boundary(line, at - 1) and boundary(line, at + len(term)):
                        found.add((path, line_number, term, cluster_id))
                    start = at + 1
    return sorted(found)


def escape_field(value) -> str:
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("\t", "\\t")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
    )


def tabular_digest(rows) -> str:
    serialized = sorted("\t".join(escape_field(value) for value in row) for row in rows)
    payload = (("\n".join(serialized) + "\n") if serialized else "").encode("utf-8")
    return sha256(payload)


def path_digest(paths) -> str:
    ordered = sorted(paths, key=lambda value: value.encode("utf-8"))
    return sha256(("".join(f"{path}\n" for path in ordered)).encode("utf-8"))


def path_blob_digest(pairs) -> str:
    ordered = sorted(pairs, key=lambda row: (row[0].encode("utf-8"), row[1]))
    return sha256(("".join(f"{path}\t{blob}\n" for path, blob in ordered)).encode("utf-8"))


@lru_cache(maxsize=1)
def reconstruct_scan():
    assert git("rev-parse", f"{FROZEN_BASE}^{{tree}}").strip() == FROZEN_TREE
    assert git("rev-parse", f"{FROZEN_BASE}:{MATCHER_PATH}").strip() == MATCHER_BLOB
    assert sha256(git_blob(FROZEN_BASE, MATCHER_PATH)) == MATCHER_SHA256

    entries = baseline_tree_entries()
    blobs = cat_blobs(blob for _path, _mode, blob in entries)
    terms = matcher_terms()
    exclusions = []
    eligible = []
    occurrences = []
    candidates = {}
    partition_counts = collections.Counter()

    for path, _mode, blob in entries:
        raw = blobs[blob]
        reason = exclusion_reason(path, raw)
        if reason:
            exclusions.append((path, reason))
            continue
        eligible.append(path)
        matches = controlled_matches(path, raw, terms)
        occurrences.extend(matches)
        if not matches:
            continue
        partition = assign_partition(path)
        partition_counts[partition] += 1
        candidates[path] = {
            "baseline_blob_sha": blob,
            "controlled_match_count": len(matches),
            "matched_terms": sorted({row[2] for row in matches}),
            "matched_search_clusters": sorted({row[3] for row in matches}),
            "partition_id": partition,
        }

    return {
        "tracked_blob_count": len(entries),
        "eligible_text_file_count": len(eligible),
        "excluded_file_count": len(exclusions),
        "excluded_path_reason_sha256": tabular_digest(exclusions),
        "candidate_file_count": len(candidates),
        "controlled_occurrence_tuple_count": len(occurrences),
        "controlled_occurrence_tuple_sha256": tabular_digest(occurrences),
        "partition_counts": dict(sorted(partition_counts.items())),
        "candidate_path_sha256": path_digest(candidates),
        "candidate_path_blob_sha256": path_blob_digest(
            (path, row["baseline_blob_sha"]) for path, row in candidates.items()
        ),
        "candidates": candidates,
    }


@lru_cache(maxsize=1)
def load_disposition_state():
    records = []
    phase_records = {}
    for index_path in DISPOSITION_INDEXES:
        index = load(index_path)
        phase = index["phase"]
        rows = []
        for meta in index["shards"]:
            raw = (ROOT / meta["path"]).read_bytes()
            assert sha256(raw) == meta["content_sha256"]
            shard_rows = json.loads(raw)["candidate_file_dispositions"]
            assert len(shard_rows) == meta["record_count"]
            rows.extend(shard_rows)
        assert len(rows) == index["candidate_file_count"] == EXPECTED_PARTITIONS[phase]
        phase_records[phase] = rows
        records.extend(rows)
    return records, phase_records


@lru_cache(maxsize=1)
def load_surface_state():
    surfaces = {}
    for index_path in SURFACE_INDEXES:
        index = load(index_path)
        rows = []
        for meta in index["shards"]:
            raw = (ROOT / meta["path"]).read_bytes()
            assert sha256(raw) == meta["content_sha256"]
            shard_rows = json.loads(raw)["surface_records"]
            assert len(shard_rows) == meta["record_count"]
            rows.extend(shard_rows)
        assert len(rows) == index["surface_count"]
        for row in rows:
            assert row["surface_id"] not in surfaces
            surfaces[row["surface_id"]] = row
    return surfaces


def validate_candidate_parity(scan, records):
    assert len(records) == EXPECTED_CANDIDATES
    ids = [row["candidate_file_id"] for row in records]
    paths = [row["path"] for row in records]
    assert len(ids) == len(set(ids)) == EXPECTED_CANDIDATES
    assert len(paths) == len(set(paths)) == EXPECTED_CANDIDATES
    assert set(paths) == set(scan["candidates"])

    by_path = {row["path"]: row for row in records}
    for path, expected in scan["candidates"].items():
        row = by_path[path]
        assert REQUIRED_DISPOSITION_FIELDS <= set(row)
        assert row["baseline_blob_sha"] == expected["baseline_blob_sha"]
        assert row["controlled_match_count"] == expected["controlled_match_count"]
        assert row["matched_terms"] == expected["matched_terms"]
        assert row["matched_search_clusters"] == expected["matched_search_clusters"]
        assert row["partition_id"] == expected["partition_id"]

    r7 = [row for row in records if row["partition_id"] == "R2A-7"]
    assert [row["candidate_file_id"] for row in r7] == [
        f"R2A-DISPOSITION-R7-{number:04d}" for number in range(1, 508)
    ]
    assert not any(row["candidate_file_id"] == "R2A-DISPOSITION-R7-0508" for row in records)
    assert path_digest(row["path"] for row in r7) == EXPECTED_R7_PATH_SHA
    assert path_blob_digest((row["path"], row["baseline_blob_sha"]) for row in r7) == EXPECTED_R7_PATH_BLOB_SHA


def validate_reciprocity(records, surfaces):
    accepted = {sid for sid, row in surfaces.items() if row["semantic_status"] == "validated"}
    assert len(surfaces) == len(accepted) == EXPECTED_SURFACES
    referenced = set()
    evidence_count = 0
    mapped_candidates = 0
    phase_evidence = collections.Counter()

    for row in records:
        mapped = row["mapped_surface_ids"]
        evidence = row["mapping_evidence"]
        if mapped:
            mapped_candidates += 1
            assert evidence
        else:
            assert evidence == []
        assert [item["mapped_surface_id"] for item in evidence] == mapped
        for item in evidence:
            assert item["mapped_surface_id"] in accepted
            assert item["authority_transfer_effect"] == "none"
        referenced.update(mapped)
        evidence_count += len(evidence)
        phase_evidence[row["partition_id"]] += len(evidence)

    assert referenced == accepted
    assert mapped_candidates == EXPECTED_MAPPED_CANDIDATES
    assert len(records) - mapped_candidates == 384
    assert evidence_count == EXPECTED_MAPPING_EVIDENCE
    assert dict(sorted(phase_evidence.items())) == EXPECTED_PHASE_EVIDENCE


def test_r2a8_frozen_scan_receipt_and_candidate_parity():
    scan = reconstruct_scan()
    records, phase_records = load_disposition_state()
    receipt = load(RECEIPT_PATH)

    assert scan["tracked_blob_count"] == EXPECTED_TRACKED
    assert scan["eligible_text_file_count"] == EXPECTED_ELIGIBLE
    assert scan["excluded_file_count"] == EXPECTED_EXCLUDED
    assert scan["candidate_file_count"] == EXPECTED_CANDIDATES
    assert scan["controlled_occurrence_tuple_count"] == EXPECTED_OCCURRENCES
    assert scan["partition_counts"] == EXPECTED_PARTITIONS
    assert scan["excluded_path_reason_sha256"] == EXPECTED_EXCLUSION_SHA
    assert scan["controlled_occurrence_tuple_sha256"] == EXPECTED_TUPLE_SHA
    assert scan["candidate_path_sha256"] == EXPECTED_PATH_SHA
    assert scan["candidate_path_blob_sha256"] == EXPECTED_PATH_BLOB_SHA
    assert {phase: len(rows) for phase, rows in phase_records.items()} == EXPECTED_PARTITIONS

    validate_candidate_parity(scan, records)

    frozen = receipt["frozen_baseline"]
    assert frozen["commit"] == FROZEN_BASE
    assert frozen["tree"] == FROZEN_TREE
    assert frozen["controlled_search_git_blob_sha"] == MATCHER_BLOB
    assert frozen["controlled_search_exact_blob_sha256"] == MATCHER_SHA256

    declared_scan = receipt["scan_receipt"]
    for field in (
        "tracked_blob_count", "eligible_text_file_count", "excluded_file_count",
        "candidate_file_count", "controlled_occurrence_tuple_count",
        "excluded_path_reason_sha256", "controlled_occurrence_tuple_sha256",
        "partition_counts",
    ):
        assert declared_scan[field] == scan[field]

    parity = receipt["candidate_parity_review"]
    assert parity["disposition_record_count"] == len(records) == 825
    assert parity["unique_candidate_id_count"] == 825
    assert parity["unique_candidate_path_count"] == 825
    assert parity["candidate_path_sha256"] == scan["candidate_path_sha256"]
    assert parity["candidate_path_blob_sha256"] == scan["candidate_path_blob_sha256"]
    assert parity["disposition_phase_counts"] == EXPECTED_PARTITIONS
    for field in (
        "missing_candidate_count", "extra_disposition_count",
        "duplicate_candidate_id_count", "duplicate_candidate_path_count",
        "baseline_blob_mismatch_count", "controlled_match_count_mismatch_count",
        "matched_term_mismatch_count", "matched_cluster_mismatch_count",
        "partition_mismatch_count",
    ):
        assert parity[field] == 0

    historical = parity["historical_r2a7_subset"]
    assert historical["candidate_count"] == 507
    assert historical["candidate_path_sha256"] == EXPECTED_R7_PATH_SHA
    assert historical["candidate_path_blob_sha256"] == EXPECTED_R7_PATH_BLOB_SHA
    assert historical["terminal_candidate_file_id"] == "R2A-DISPOSITION-R7-0507"
    assert historical["forbidden_next_candidate_file_id"] == "R2A-DISPOSITION-R7-0508"


def test_r2a8_evidence_reciprocity_and_nontransfer():
    records, _phase_records = load_disposition_state()
    surfaces = load_surface_state()
    validate_reciprocity(records, surfaces)

    receipt = load(RECEIPT_PATH)["evidence_reciprocity_review"]
    assert receipt["semantic_surface_record_count"] == EXPECTED_SURFACES
    assert receipt["validated_surface_count"] == EXPECTED_SURFACES
    assert receipt["nonvalidated_surface_count"] == 0
    assert receipt["unique_referenced_surface_count"] == EXPECTED_SURFACES
    assert receipt["unreferenced_validated_surface_count"] == 0
    assert receipt["referenced_nonvalidated_surface_count"] == 0
    assert receipt["mapped_candidate_count"] == EXPECTED_MAPPED_CANDIDATES
    assert receipt["unmapped_candidate_count"] == 384
    assert receipt["mapped_surface_reference_count"] == EXPECTED_MAPPING_EVIDENCE
    assert receipt["mapping_evidence_count"] == EXPECTED_MAPPING_EVIDENCE
    assert receipt["phase_mapping_evidence_counts"] == EXPECTED_PHASE_EVIDENCE
    assert receipt["ordered_mapping_evidence_mismatch_count"] == 0
    assert receipt["missing_surface_target_count"] == 0
    assert receipt["authority_transfer_violation_count"] == 0


def test_r2a8_manifest_completion_is_bounded():
    receipt = load(RECEIPT_PATH)
    manifest = load(MANIFEST_PATH)
    assert receipt["status"] == "complete"
    assert receipt["phase"] == "R2A-8"
    assert receipt["completion_assertions"]["blocking_exceptions"] == []
    assert manifest["artifact_version"] == "0.2.15"
    assert manifest["status"] == "active_incomplete"
    partitions = {row["partition_id"]: row for row in manifest["partitions"]}
    assert partitions["R2A-8"]["status"] == "complete"
    assert partitions["R2A-8"]["maximum_changed_files"] == 7
    assert partitions["R2A-8"]["maximum_additions"] == 2500
    assert partitions["R2A-8"]["planned_artifact_paths"] == [RECEIPT_PATH]
    assert partitions["R2A-9"]["status"] == "planned_not_present"
    assert partitions["R2A-10"]["status"] == "planned_not_present"
    assert partitions["R2A-11"]["status"] == "planned_not_present"
    assert partitions["R2A-12"]["status"] == "planned_not_present"


def test_r2a8_adversarial_mutations_fail_closed():
    scan = reconstruct_scan()
    records, _phase_records = load_disposition_state()
    surfaces = load_surface_state()

    bad = copy.deepcopy(records)
    bad.pop()
    with pytest.raises(AssertionError):
        validate_candidate_parity(scan, bad)

    bad = copy.deepcopy(records)
    bad[0]["baseline_blob_sha"] = "0" * 40
    with pytest.raises(AssertionError):
        validate_candidate_parity(scan, bad)

    bad = copy.deepcopy(records)
    bad[0]["partition_id"] = "R2A-7" if bad[0]["partition_id"] != "R2A-7" else "R2A-4"
    with pytest.raises(AssertionError):
        validate_candidate_parity(scan, bad)

    bad = copy.deepcopy(records)
    fake = copy.deepcopy(next(row for row in bad if row["candidate_file_id"] == "R2A-DISPOSITION-R7-0507"))
    fake["candidate_file_id"] = "R2A-DISPOSITION-R7-0508"
    bad.append(fake)
    with pytest.raises(AssertionError):
        validate_candidate_parity(scan, bad)

    mapped_index = next(index for index, row in enumerate(records) if row["mapped_surface_ids"])
    bad = copy.deepcopy(records)
    bad[mapped_index]["mapping_evidence"] = []
    with pytest.raises(AssertionError):
        validate_reciprocity(bad, surfaces)

    bad = copy.deepcopy(records)
    bad[mapped_index]["mapped_surface_ids"][0] = "R2A-SURFACE-UNKNOWN-9999"
    bad[mapped_index]["mapping_evidence"][0]["mapped_surface_id"] = "R2A-SURFACE-UNKNOWN-9999"
    with pytest.raises(AssertionError):
        validate_reciprocity(bad, surfaces)

    bad = copy.deepcopy(records)
    bad[mapped_index]["mapping_evidence"][0]["authority_transfer_effect"] = "candidate_inherits"
    with pytest.raises(AssertionError):
        validate_reciprocity(bad, surfaces)

    bad = copy.deepcopy(records)
    bad[mapped_index]["mapping_evidence"] = list(reversed(bad[mapped_index]["mapping_evidence"]))
    if len(bad[mapped_index]["mapping_evidence"]) > 1:
        with pytest.raises(AssertionError):
            validate_reciprocity(bad, surfaces)

# ---------------------------------------------------------------------------
# R2A-8 partition-manifest successor boundary.
#
# R2A-8 may advance only its own status plus the manifest artifact version.
# Every other manifest semantic must remain identical to the repaired R2A-7
# predecessor state.
# ---------------------------------------------------------------------------

R2A8_PREDECESSOR_HEAD = (
    "60f6c7544fb963f6a0330eceb7ae6b2b9971cc59"
)


def test_r2a8_partition_manifest_progression_is_semantically_bounded():
    predecessor = json.loads(
        git_blob(
            R2A8_PREDECESSOR_HEAD,
            MANIFEST_PATH,
        ).decode("utf-8")
    )
    current = load(MANIFEST_PATH)

    assert predecessor["artifact_version"] == "0.2.14"
    assert current["artifact_version"] == "0.2.15"

    predecessor_by_partition = {
        row["partition_id"]: row
        for row in predecessor["partitions"]
    }
    current_by_partition = {
        row["partition_id"]: row
        for row in current["partitions"]
    }

    assert (
        predecessor_by_partition["R2A-8"]["status"]
        == "planned_not_present"
    )
    assert current_by_partition["R2A-8"]["status"] == "complete"

    assert current["status"] == predecessor["status"] == "active_incomplete"
    assert current_by_partition["R2A-9"]["status"] == "planned_not_present"
    assert current_by_partition["R2A-10"]["status"] == "planned_not_present"
    assert current_by_partition["R2A-11"]["status"] == "planned_not_present"
    assert current_by_partition["R2A-12"]["status"] == "planned_not_present"

    normalized = copy.deepcopy(current)
    normalized["artifact_version"] = predecessor["artifact_version"]

    normalized_by_partition = {
        row["partition_id"]: row
        for row in normalized["partitions"]
    }
    normalized_by_partition["R2A-8"]["status"] = (
        predecessor_by_partition["R2A-8"]["status"]
    )

    assert normalized == predecessor

# ---------------------------------------------------------------------------
# R2A-9 successor historicalization.
#
# R2A-8 completion remains certified at its accepted head. Later R2A
# partitions may advance the live partition manifest without rewriting
# R2A-8's historical receipt or requiring R2A-9 to remain not-yet-started.
# R2A-9 successor state is validated by the R2A-9 verifier.
# ---------------------------------------------------------------------------

R2A8_CERTIFIED_HEAD = (
    "8e3d8e6db41cbad39edb58c5f2cba83fbefcc3ed"
)


def _r2a8_certified_manifest():
    return json.loads(
        git_blob(
            R2A8_CERTIFIED_HEAD,
            MANIFEST_PATH,
        ).decode("utf-8")
    )


def _r2a8_certified_receipt():
    return json.loads(
        git_blob(
            R2A8_CERTIFIED_HEAD,
            RECEIPT_PATH,
        ).decode("utf-8")
    )


def test_r2a8_manifest_completion_is_bounded():
    receipt = _r2a8_certified_receipt()
    historical = _r2a8_certified_manifest()
    current = load(MANIFEST_PATH)

    assert receipt["status"] == "complete"
    assert receipt["phase"] == "R2A-8"
    assert receipt["completion_assertions"]["blocking_exceptions"] == []

    assert historical["artifact_version"] == "0.2.15"
    assert historical["status"] == "active_incomplete"

    historical_by_partition = {
        row["partition_id"]: row
        for row in historical["partitions"]
    }
    current_by_partition = {
        row["partition_id"]: row
        for row in current["partitions"]
    }

    assert historical_by_partition["R2A-8"]["status"] == "complete"
    assert historical_by_partition["R2A-8"]["maximum_changed_files"] == 7
    assert historical_by_partition["R2A-8"]["maximum_additions"] == 2500
    assert historical_by_partition["R2A-8"]["planned_artifact_paths"] == [
        RECEIPT_PATH
    ]

    assert (
        historical_by_partition["R2A-9"]["status"]
        == "planned_not_present"
    )
    assert (
        historical_by_partition["R2A-10"]["status"]
        == "planned_not_present"
    )
    assert (
        historical_by_partition["R2A-11"]["status"]
        == "planned_not_present"
    )
    assert (
        historical_by_partition["R2A-12"]["status"]
        == "planned_not_present"
    )

    # Successors may advance later partitions, but must not mutate R2A-8.
    assert current["status"] == "active_incomplete"
    assert current["artifact_id"] == historical["artifact_id"]
    assert current["phase"] == historical["phase"]
    assert current["partition_count"] == historical["partition_count"] == 12
    assert current["ownership_rules"] == historical["ownership_rules"]

    for partition_id in (
        "R2A-1",
        "R2A-2",
        "R2A-3",
        "R2A-4",
        "R2A-5",
        "R2A-6",
        "R2A-7",
        "R2A-8",
    ):
        assert (
            current_by_partition[partition_id]
            == historical_by_partition[partition_id]
        )

    assert current_by_partition["R2A-10"]["status"] == "planned_not_present"
    assert current_by_partition["R2A-11"]["status"] == "planned_not_present"
    assert current_by_partition["R2A-12"]["status"] == "planned_not_present"


def test_r2a8_partition_manifest_progression_is_semantically_bounded():
    predecessor = json.loads(
        git_blob(
            R2A8_PREDECESSOR_HEAD,
            MANIFEST_PATH,
        ).decode("utf-8")
    )
    historical = _r2a8_certified_manifest()
    current = load(MANIFEST_PATH)

    assert predecessor["artifact_version"] == "0.2.14"
    assert historical["artifact_version"] == "0.2.15"

    predecessor_by_partition = {
        row["partition_id"]: row
        for row in predecessor["partitions"]
    }
    historical_by_partition = {
        row["partition_id"]: row
        for row in historical["partitions"]
    }
    current_by_partition = {
        row["partition_id"]: row
        for row in current["partitions"]
    }

    assert (
        predecessor_by_partition["R2A-8"]["status"]
        == "planned_not_present"
    )
    assert historical_by_partition["R2A-8"]["status"] == "complete"

    # R2A-8's own historical transition remains exactly bounded.
    normalized_historical = copy.deepcopy(historical)
    normalized_historical["artifact_version"] = predecessor["artifact_version"]

    normalized_by_partition = {
        row["partition_id"]: row
        for row in normalized_historical["partitions"]
    }
    normalized_by_partition["R2A-8"]["status"] = (
        predecessor_by_partition["R2A-8"]["status"]
    )

    assert normalized_historical == predecessor

    # Current successors may advance R2A-9+, but cannot rewrite R2A-8.
    assert current["status"] == "active_incomplete"
    assert current_by_partition["R2A-8"] == historical_by_partition["R2A-8"]
    assert current_by_partition["R2A-10"]["status"] == "planned_not_present"
    assert current_by_partition["R2A-11"]["status"] == "planned_not_present"
    assert current_by_partition["R2A-12"]["status"] == "planned_not_present"

# R2A-9 successor surface historicalization.
#
# R2A-8 aggregate evidence reciprocity was certified against the semantic
# surface state present at R2A8_CERTIFIED_HEAD. Later claim-assessment
# partitions may add reciprocal claim links to the live R2A-2/R2A-3 shards.
# Those successor links must not rewrite the R2A-8 historical evidence set.

@lru_cache(maxsize=1)
def load_surface_state():
    surfaces = {}

    for index_path in SURFACE_INDEXES:
        index = json.loads(
            git_blob(
                R2A8_CERTIFIED_HEAD,
                index_path,
            ).decode("utf-8")
        )

        rows = []

        for meta in index["shards"]:
            raw = git_blob(
                R2A8_CERTIFIED_HEAD,
                meta["path"],
            )

            assert sha256(raw) == meta["content_sha256"]

            shard_rows = json.loads(raw)["surface_records"]

            assert len(shard_rows) == meta["record_count"]
            rows.extend(shard_rows)

        assert len(rows) == index["surface_count"]

        for row in rows:
            assert row["surface_id"] not in surfaces
            surfaces[row["surface_id"]] = row

    return surfaces

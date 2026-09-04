"""Temporary deterministic measurement probe for R2A-8 aggregate receipts."""
from __future__ import annotations

import collections
import fnmatch
import hashlib
import io
import json
import re
import subprocess
import unicodedata
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FROZEN_BASE = "62e1565ed598345901e92dc04f3b686281418d83"
MATCHER_PATH = "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml"
EXPECTED_MATCHER_BLOB = "f0c154ab7703afb8aedc92e1e472492363487a58"
EXPECTED_PATH_DIGEST = "f5ddc972d65ee8ba366da0136fb692d5b64ec2f9ce3c0690f582db53b7fed1ca"
EXPECTED_PATH_BLOB_DIGEST = "6c38b13c3982f608b5465af6902a51316dcff5cd256d9b079708424d5c24fec0"

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


def git(*args: str, binary: bool = False):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary)


def git_blob(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}", binary=True)


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def baseline_tree_entries():
    raw = git("ls-tree", "-r", "-z", "--full-tree", FROZEN_BASE, binary=True)
    entries = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path_raw = record.split(b"\t", 1)
        mode, kind, sha = meta.decode("ascii").split()
        if kind == "blob":
            entries.append((path_raw.decode("utf-8"), mode, sha))
    return entries


def cat_blobs(shas):
    unique = list(dict.fromkeys(shas))
    request = b"".join(sha.encode("ascii") + b"\n" for sha in unique)
    raw = subprocess.check_output(["git", "cat-file", "--batch"], cwd=ROOT, input=request)
    stream = io.BytesIO(raw)
    result = {}
    for requested_sha in unique:
        header = stream.readline().rstrip(b"\n")
        actual_sha, kind, size = header.split()
        assert actual_sha.decode("ascii") == requested_sha
        assert kind == b"blob"
        data = stream.read(int(size))
        assert stream.read(1) == b"\n"
        result[requested_sha] = data
    assert stream.read() == b""
    return result


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    value = value.casefold()
    value = unicodedata.normalize("NFC", value)
    return re.sub(r"\s+", " ", value)


def boundary(value: str, index: int) -> bool:
    return index < 0 or index >= len(value) or unicodedata.category(value[index])[:1] not in {"L", "N"}


def excluded(path: str, raw: bytes):
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


def matcher_terms():
    document = json.loads(git_blob(FROZEN_BASE, MATCHER_PATH).decode("utf-8"))
    return {row["cluster_id"]: [normalize(term) for term in row["terms"]] for row in document["clusters"]}


def controlled_matches(path: str, raw: bytes, terms_by_cluster):
    if excluded(path, raw):
        return []
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
        remainder = path[len("docs/doctrine/") :]
        if "/" not in remainder and (fnmatch.fnmatchcase(remainder, "*.yaml") or fnmatch.fnmatchcase(remainder, "*.md")):
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


def escape(value) -> str:
    return str(value).replace("\\", "\\\\").replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n")


def serialize(rows) -> bytes:
    records = sorted("\t".join(escape(value) for value in row) for row in rows)
    return (("\n".join(records) + "\n") if records else "").encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_variants(paths, pairs, entries_by_path):
    path_json_compact = json.dumps(paths, ensure_ascii=False, separators=(",", ":")).encode()
    path_json_default = json.dumps(paths, ensure_ascii=False).encode()
    pair_lists = [[path, blob] for path, blob in pairs]
    pair_json_compact = json.dumps(pair_lists, ensure_ascii=False, separators=(",", ":")).encode()
    pair_json_default = json.dumps(pair_lists, ensure_ascii=False).encode()
    pair_dict_compact = json.dumps(dict(pairs), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    tree_lines = []
    tree_z = []
    for path, blob in pairs:
        mode = entries_by_path[path][0]
        tree_lines.append(f"{mode} blob {blob}\t{path}\n")
        tree_z.append(f"{mode} blob {blob}\t{path}".encode() + b"\0")
    path_variants = {
        "newline_final": sha(("\n".join(paths) + "\n").encode()),
        "newline_no_final": sha("\n".join(paths).encode()),
        "nul_final": sha(b"".join(path.encode() + b"\0" for path in paths)),
        "nul_no_final": sha(b"\0".join(path.encode() for path in paths)),
        "concat": sha("".join(paths).encode()),
        "json_compact": sha(path_json_compact),
        "json_default": sha(path_json_default),
        "repr": sha(repr(paths).encode()),
        "partition_tab_path_final": sha("".join(f"{assign_partition(path)}\t{path}\n" for path in paths).encode()),
        "path_tab_partition_final": sha("".join(f"{path}\t{assign_partition(path)}\n" for path in paths).encode()),
    }
    pair_variants = {
        "path_tab_blob_final": sha("".join(f"{path}\t{blob}\n" for path, blob in pairs).encode()),
        "path_tab_blob_no_final": sha("\n".join(f"{path}\t{blob}" for path, blob in pairs).encode()),
        "path_nul_blob_nul": sha(b"".join(path.encode() + b"\0" + blob.encode() + b"\0" for path, blob in pairs)),
        "path_nul_blob_final_newline": sha(b"".join(path.encode() + b"\0" + blob.encode() + b"\n" for path, blob in pairs)),
        "path_nul_blob_record_nul": sha(b"".join(path.encode() + b"\0" + blob.encode() + b"\0" for path, blob in pairs)),
        "blob_tab_path_final": sha("".join(f"{blob}\t{path}\n" for path, blob in pairs).encode()),
        "path_space_blob_final": sha("".join(f"{path} {blob}\n" for path, blob in pairs).encode()),
        "blob_space_path_final": sha("".join(f"{blob} {path}\n" for path, blob in pairs).encode()),
        "concat": sha("".join(path + blob for path, blob in pairs).encode()),
        "json_lists_compact": sha(pair_json_compact),
        "json_lists_default": sha(pair_json_default),
        "json_dict_compact": sha(pair_dict_compact),
        "git_ls_tree_lines": sha("".join(tree_lines).encode()),
        "git_ls_tree_z": sha(b"".join(tree_z)),
        "partition_path_blob_final": sha("".join(f"{assign_partition(path)}\t{path}\t{blob}\n" for path, blob in pairs).encode()),
    }
    return path_variants, pair_variants


def load_dispositions():
    all_records = []
    index_summaries = []
    for index_path in DISPOSITION_INDEXES:
        index = load(index_path)
        records = []
        shard_hash_mismatches = 0
        shard_count_mismatches = 0
        for meta in index["shards"]:
            shard_path = ROOT / meta["path"]
            raw = shard_path.read_bytes()
            shard = json.loads(raw)
            shard_records = shard["candidate_file_dispositions"]
            if sha(raw) != meta["content_sha256"]:
                shard_hash_mismatches += 1
            if len(shard_records) != meta["record_count"]:
                shard_count_mismatches += 1
            records.extend(shard_records)
        index_summaries.append({
            "phase": index["phase"],
            "declared": index["candidate_file_count"],
            "loaded": len(records),
            "shard_hash_mismatches": shard_hash_mismatches,
            "shard_count_mismatches": shard_count_mismatches,
        })
        all_records.extend(records)
    return all_records, index_summaries


def load_surfaces():
    surfaces = {}
    index_summaries = []
    for index_path in SURFACE_INDEXES:
        index = load(index_path)
        loaded = []
        shard_hash_mismatches = 0
        for meta in index["shards"]:
            path = ROOT / meta["path"]
            raw = path.read_bytes()
            if sha(raw) != meta["content_sha256"]:
                shard_hash_mismatches += 1
            loaded.extend(json.loads(raw)["surface_records"])
        index_summaries.append({
            "phase": index["phase"],
            "declared": index["surface_count"],
            "loaded": len(loaded),
            "shard_hash_mismatches": shard_hash_mismatches,
        })
        for row in loaded:
            assert row["surface_id"] not in surfaces
            surfaces[row["surface_id"]] = row
    return surfaces, index_summaries


def test_measure_r2a8_receipt_values():
    matcher_blob = git("rev-parse", f"{FROZEN_BASE}:{MATCHER_PATH}").strip()
    assert matcher_blob == EXPECTED_MATCHER_BLOB

    entries = baseline_tree_entries()
    entries_by_path = {path: (mode, blob) for path, mode, blob in entries}
    blobs = cat_blobs(blob for _, _, blob in entries)
    terms_by_cluster = matcher_terms()

    exclusions = []
    eligible = []
    positives = []
    candidate_metadata = {}
    tuples = []
    partitions = collections.Counter()

    for path, _mode, blob in entries:
        raw = blobs[blob]
        reason = excluded(path, raw)
        if reason:
            exclusions.append((path, reason))
            continue
        eligible.append(path)
        matches = controlled_matches(path, raw, terms_by_cluster)
        tuples.extend(matches)
        if matches:
            positives.append((path, blob))
            partitions[assign_partition(path)] += 1
            candidate_metadata[path] = {
                "blob": blob,
                "count": len(matches),
                "terms": sorted({row[2] for row in matches}),
                "clusters": sorted({row[3] for row in matches}),
            }

    exclusion_counts = collections.Counter(reason for _, reason in exclusions)
    count_by_term = collections.Counter(row[2] for row in tuples)
    count_by_cluster = collections.Counter(row[3] for row in tuples)

    paths = sorted(path for path, _blob in positives)
    pairs = sorted(positives)
    path_variants, pair_variants = digest_variants(paths, pairs, entries_by_path)

    records, disposition_indexes = load_dispositions()
    surfaces, surface_indexes = load_surfaces()
    accepted = {sid for sid, row in surfaces.items() if row["semantic_status"] == "validated"}
    nonaccepted = set(surfaces) - accepted

    record_paths = [row["path"] for row in records]
    record_ids = [row["candidate_file_id"] for row in records]
    record_by_path = {row["path"]: row for row in records}
    evidence = [item for row in records for item in row["mapping_evidence"]]
    mapped_surface_ids = [sid for row in records for sid in row["mapped_surface_ids"]]
    referenced = set(mapped_surface_ids)

    ordered_mapping_mismatches = sum(
        [item["mapped_surface_id"] for item in row["mapping_evidence"]] != row["mapped_surface_ids"]
        for row in records
    )
    missing_target_count = sum(sid not in accepted for sid in mapped_surface_ids)
    transfer_violation_count = sum(item["authority_transfer_effect"] != "none" for item in evidence)

    path_set = set(paths)
    record_path_set = set(record_paths)
    blob_mismatches = 0
    lexical_count_mismatches = 0
    term_mismatches = 0
    cluster_mismatches = 0
    partition_mismatches = 0
    for path in path_set & record_path_set:
        row = record_by_path[path]
        expected = candidate_metadata[path]
        blob_mismatches += row["baseline_blob_sha"] != expected["blob"]
        lexical_count_mismatches += row["controlled_match_count"] != expected["count"]
        term_mismatches += row["matched_terms"] != expected["terms"]
        cluster_mismatches += row["matched_search_clusters"] != expected["clusters"]
        partition_mismatches += row["partition_id"] != assign_partition(path)

    result = {
        "scan": {
            "tracked_blob_count": len(entries),
            "eligible_file_count": len(eligible),
            "excluded_file_count_by_reason": dict(sorted(exclusion_counts.items())),
            "excluded_path_digest": sha(serialize(exclusions)),
            "candidate_file_count": len(positives),
            "occurrence_count": len(tuples),
            "count_by_term": dict(sorted(count_by_term.items())),
            "count_by_cluster": dict(sorted(count_by_cluster.items())),
            "tuple_stream_sha256": sha(serialize(tuples)),
            "partition_counts": dict(sorted(partitions.items())),
            "controlled_search_artifact_sha256": sha(git_blob(FROZEN_BASE, MATCHER_PATH)),
        },
        "digest_identification": {
            "candidate_path_variants": path_variants,
            "path_blob_pair_variants": pair_variants,
            "path_matching_variants": sorted(key for key, value in path_variants.items() if value == EXPECTED_PATH_DIGEST),
            "pair_matching_variants": sorted(key for key, value in pair_variants.items() if value == EXPECTED_PATH_BLOB_DIGEST),
            "expected_candidate_path_digest": EXPECTED_PATH_DIGEST,
            "expected_path_blob_pair_digest": EXPECTED_PATH_BLOB_DIGEST,
        },
        "parity": {
            "disposition_record_count": len(records),
            "unique_record_id_count": len(set(record_ids)),
            "unique_record_path_count": len(record_path_set),
            "missing_candidate_count": len(path_set - record_path_set),
            "extra_disposition_count": len(record_path_set - path_set),
            "duplicate_id_count": len(record_ids) - len(set(record_ids)),
            "duplicate_path_count": len(record_paths) - len(record_path_set),
            "blob_mismatch_count": blob_mismatches,
            "lexical_count_mismatch_count": lexical_count_mismatches,
            "term_mismatch_count": term_mismatches,
            "cluster_mismatch_count": cluster_mismatches,
            "partition_mismatch_count": partition_mismatches,
            "r7_0507_count": sum(row["candidate_file_id"] == "R2A-DISPOSITION-R7-0507" for row in records),
            "r7_0508_count": sum(row["candidate_file_id"] == "R2A-DISPOSITION-R7-0508" for row in records),
            "index_summaries": disposition_indexes,
        },
        "reciprocity": {
            "surface_record_count": len(surfaces),
            "accepted_surface_count": len(accepted),
            "nonaccepted_surface_count": len(nonaccepted),
            "unique_referenced_surface_count": len(referenced),
            "unreferenced_accepted_surface_count": len(accepted - referenced),
            "referenced_nonaccepted_surface_count": len(referenced - accepted),
            "mapping_evidence_count": len(evidence),
            "mapped_surface_reference_count": len(mapped_surface_ids),
            "ordered_mapping_mismatch_count": ordered_mapping_mismatches,
            "missing_target_count": missing_target_count,
            "authority_transfer_violation_count": transfer_violation_count,
            "mapping_relationship_counts": dict(sorted(collections.Counter(item["mapping_relationship"] for item in evidence).items())),
            "surface_index_summaries": surface_indexes,
        },
    }

    pytest.fail("R2A8_PROBE2=" + json.dumps(result, sort_keys=True, separators=(",", ":")))

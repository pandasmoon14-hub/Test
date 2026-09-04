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


def git(*args: str, binary: bool = False):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary)


def git_blob(commit: str, path: str) -> bytes:
    return git("show", f"{commit}:{path}", binary=True)


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


def test_measure_r2a8_receipt_values():
    matcher_blob = git("rev-parse", f"{FROZEN_BASE}:{MATCHER_PATH}").strip()
    assert matcher_blob == EXPECTED_MATCHER_BLOB

    entries = baseline_tree_entries()
    blobs = cat_blobs(sha for _, _, sha in entries)
    terms_by_cluster = matcher_terms()

    exclusions = []
    eligible = []
    positives = []
    tuples = []
    partitions = collections.Counter()

    for path, _mode, sha in entries:
        raw = blobs[sha]
        reason = excluded(path, raw)
        if reason:
            exclusions.append((path, reason))
            continue
        eligible.append(path)
        matches = controlled_matches(path, raw, terms_by_cluster)
        tuples.extend(matches)
        if matches:
            positives.append((path, sha))
            partitions[assign_partition(path)] += 1

    exclusion_counts = collections.Counter(reason for _, reason in exclusions)
    count_by_term = collections.Counter(row[2] for row in tuples)
    count_by_cluster = collections.Counter(row[3] for row in tuples)

    sorted_paths = sorted(path for path, _sha in positives)
    sorted_pairs = sorted(positives)

    path_variants = {
        "newline_final": hashlib.sha256(("\n".join(sorted_paths) + "\n").encode()).hexdigest(),
        "newline_no_final": hashlib.sha256("\n".join(sorted_paths).encode()).hexdigest(),
        "canonical_one_field": hashlib.sha256(serialize((path,) for path in sorted_paths)).hexdigest(),
    }
    pair_variants = {
        "path_tab_blob_final": hashlib.sha256(("".join(f"{path}\t{sha}\n" for path, sha in sorted_pairs)).encode()).hexdigest(),
        "path_tab_blob_no_final": hashlib.sha256(("\n".join(f"{path}\t{sha}" for path, sha in sorted_pairs)).encode()).hexdigest(),
        "canonical_two_field": hashlib.sha256(serialize(sorted_pairs)).hexdigest(),
        "blob_tab_path_final": hashlib.sha256(("".join(f"{sha}\t{path}\n" for path, sha in sorted_pairs)).encode()).hexdigest(),
    }

    result = {
        "tracked_blob_count": len(entries),
        "eligible_file_count": len(eligible),
        "excluded_file_count_by_reason": dict(sorted(exclusion_counts.items())),
        "excluded_path_digest": hashlib.sha256(serialize(exclusions)).hexdigest(),
        "candidate_file_count": len(positives),
        "occurrence_count": len(tuples),
        "count_by_term": dict(sorted(count_by_term.items())),
        "count_by_cluster": dict(sorted(count_by_cluster.items())),
        "tuple_stream_sha256": hashlib.sha256(serialize(tuples)).hexdigest(),
        "partition_counts": dict(sorted(partitions.items())),
        "candidate_path_digest_variants": path_variants,
        "path_blob_pair_digest_variants": pair_variants,
        "expected_candidate_path_digest": EXPECTED_PATH_DIGEST,
        "expected_path_blob_pair_digest": EXPECTED_PATH_BLOB_DIGEST,
        "controlled_search_artifact_sha256": hashlib.sha256(git_blob(FROZEN_BASE, MATCHER_PATH)).hexdigest(),
    }

    pytest.fail("R2A8_PROBE=" + json.dumps(result, sort_keys=True, separators=(",", ":")))

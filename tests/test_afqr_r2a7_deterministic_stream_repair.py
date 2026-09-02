"""Regression contract for the deterministic R2A-7 candidate-stream repair."""

from __future__ import annotations

import fnmatch
import json
import re
import subprocess
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FROZEN_BASE = "62e1565ed598345901e92dc04f3b686281418d83"
REPAIR_START = "176201f9d3a88d84e9d6628923392d7ba6c38341"

DISPOSITIONS = (
    ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "r2a"
    / "dispositions_remaining"
)

MANIFEST = (
    ROOT
    / "docs"
    / "doctrine"
    / "reviews"
    / "afqr_r2a_partition_manifest.yaml"
)

MATCHER_PATH = (
    "docs/doctrine/reviews/"
    "afqr_r2a_controlled_search_clusters.yaml"
)

EXPECTED_MATCHER_BLOB = (
    "f0c154ab7703afb8aedc92e1e472492363487a58"
)

EXPECTED_TRACKED_BLOBS = 881
EXPECTED_ELIGIBLE_TEXT = 851
EXPECTED_MATCHER_POSITIVE = 825

EXPECTED_PARTITION_COUNTS = {
    "R2A-4": 69,
    "R2A-5": 85,
    "R2A-6": 164,
    "R2A-7": 507,
}

COMPATIBILITY_EXPECTED = [
    (
        151,
        "docs/doctrine/native_design/d_series/source_packs/"
        "astra_d03_d04_d20_compatibility_amendment_pack_v0_1/"
        "D00-D10_d20_compatibility_audit_note_v0_1.md",
        "1d02b026a94db40a1377c1f64ea9b5f22827b644",
        1,
    ),
    (
        152,
        "docs/doctrine/native_design/d_series/source_packs/"
        "astra_d03_d04_d20_compatibility_amendment_pack_v0_1/"
        "D03-A_d20_backlash_trigger_terminology_amendment.md",
        "0fb012339025a55bdebca4beb65114fa2c11a365",
        6,
    ),
    (
        153,
        "docs/doctrine/native_design/d_series/source_packs/"
        "astra_d03_d04_d20_compatibility_amendment_pack_v0_1/"
        "D03_D04_d20_compatibility_application_guide.md",
        "985bbf0d6b042fb38fc9d42f5dfa5120bd377696",
        1,
    ),
    (
        154,
        "docs/doctrine/native_design/d_series/source_packs/"
        "astra_d03_d04_d20_compatibility_amendment_pack_v0_1/"
        "D03_D04_d20_compatibility_manifest_v0_1.json",
        "82ccc80eaa1e9f31819fdd85812486a562e082e2",
        2,
    ),
    (
        155,
        "docs/doctrine/native_design/d_series/source_packs/"
        "astra_d03_d04_d20_compatibility_amendment_pack_v0_1/"
        "D04-A_d20_breakthrough_outcome_mapping_amendment.md",
        "64000f972a26d9cfc803805d8d066404a8f48c13",
        8,
    ),
    (
        156,
        "docs/doctrine/native_design/d_series/source_packs/"
        "astra_d03_d04_d20_compatibility_amendment_pack_v0_1/"
        "astra_d03_d04_d20_compatibility_amendment_pack_combined_v0_1.md",
        "846702698c67888280d298aa497968cedc6c7fd9",
        18,
    ),
]


def git(*args: str, binary: bool = False):
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=not binary,
    )


def git_blob(commit: str, path: str) -> bytes:
    return git(
        "show",
        f"{commit}:{path}",
        binary=True,
    )


def baseline_tree_entries():
    raw = git(
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        FROZEN_BASE,
        binary=True,
    )

    entries = []

    for record in raw.split(b"\0"):
        if not record:
            continue

        meta, path_raw = record.split(b"\t", 1)
        mode, kind, sha = meta.decode("ascii").split()

        if kind != "blob":
            continue

        entries.append(
            (
                path_raw.decode("utf-8"),
                mode,
                sha,
            )
        )

    return entries


def cat_blobs(shas):
    unique = list(dict.fromkeys(shas))

    proc = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    assert proc.stdin is not None
    assert proc.stdout is not None

    for sha in unique:
        proc.stdin.write(sha.encode("ascii") + b"\n")

    proc.stdin.close()

    result = {}

    for requested_sha in unique:
        header = proc.stdout.readline().rstrip(b"\n")
        parts = header.split()

        assert len(parts) == 3
        actual_sha = parts[0].decode("ascii")
        kind = parts[1].decode("ascii")
        size = int(parts[2])

        assert actual_sha == requested_sha
        assert kind == "blob"

        data = proc.stdout.read(size)
        assert len(data) == size
        assert proc.stdout.read(1) == b"\n"

        result[requested_sha] = data

    assert proc.wait() == 0
    return result


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    value = value.casefold()
    value = unicodedata.normalize("NFC", value)
    return re.sub(r"\s+", " ", value)


def boundary(value: str, index: int) -> bool:
    return (
        index < 0
        or index >= len(value)
        or unicodedata.category(value[index])[:1]
        not in {"L", "N"}
    )


def excluded(path: str, raw: bytes):
    parts = path.split("/")

    if (
        parts[0] in {
            ".git",
            "node_modules",
            "vendor",
            "dist",
            "build",
            "coverage",
        }
        or "__pycache__" in parts
    ):
        return "generated_or_vendor_path"

    if b"\0" in raw:
        return "nul_binary"

    try:
        raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return "invalid_utf8"

    return None


def matcher_terms():
    document = json.loads(
        git_blob(
            FROZEN_BASE,
            MATCHER_PATH,
        ).decode("utf-8")
    )

    result = {}

    for cluster in document["clusters"]:
        result[cluster["cluster_id"]] = [
            normalize(term)
            for term in cluster["terms"]
        ]

    return result


def controlled_matches(path: str, raw: bytes, terms_by_cluster):
    if excluded(path, raw):
        return []

    text = (
        raw.decode("utf-8-sig")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    found = set()

    for line_number, source_line in enumerate(
        text.split("\n"),
        1,
    ):
        line = normalize(source_line)

        for cluster_id, terms in terms_by_cluster.items():
            for term in terms:
                start = 0

                while term:
                    at = line.find(term, start)

                    if at < 0:
                        break

                    if (
                        boundary(line, at - 1)
                        and boundary(line, at + len(term))
                    ):
                        found.add(
                            (
                                path,
                                line_number,
                                term,
                                cluster_id,
                            )
                        )

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

        if "/" not in remainder and (
            fnmatch.fnmatchcase(remainder, "*.yaml")
            or fnmatch.fnmatchcase(remainder, "*.md")
        ):
            return "R2A-5"

    if (
        path.startswith("src/")
        or path.startswith("schemas/")
        or path.startswith("tests/runtime/")
        or fnmatch.fnmatchcase(
            path,
            "tests/test_runtime_*.py",
        )
        or fnmatch.fnmatchcase(
            path,
            "tests/test_*runtime*.py",
        )
    ):
        return "R2A-6"

    return "R2A-7"


def current_records():
    records = []

    for number in range(1, 36):
        path = (
            DISPOSITIONS
            / f"dispositions_{number:04d}.yaml"
        )

        assert path.is_file()

        document = json.loads(
            path.read_text(encoding="utf-8")
        )

        records.extend(
            document["candidate_file_dispositions"]
        )

    return records


def historical_salvage_records():
    records = []

    for number in range(16, 35):
        path = (
            "docs/doctrine/reviews/r2a/"
            "dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )

        document = json.loads(
            git_blob(
                REPAIR_START,
                path,
            ).decode("utf-8")
        )

        records.extend(
            document["candidate_file_dispositions"]
        )

    return records


def test_frozen_candidate_stream_and_repaired_prefix():
    matcher_blob = git(
        "rev-parse",
        f"{FROZEN_BASE}:{MATCHER_PATH}",
    ).strip()

    assert matcher_blob == EXPECTED_MATCHER_BLOB

    entries = baseline_tree_entries()

    assert len(entries) == EXPECTED_TRACKED_BLOBS

    blobs = cat_blobs(
        sha for _, _, sha in entries
    )

    terms_by_cluster = matcher_terms()

    eligible = []
    positives = []
    partitions = {
        "R2A-4": [],
        "R2A-5": [],
        "R2A-6": [],
        "R2A-7": [],
    }

    metadata = {}

    for path, _mode, sha in entries:
        raw = blobs[sha]

        if excluded(path, raw):
            continue

        eligible.append(path)

        matches = controlled_matches(
            path,
            raw,
            terms_by_cluster,
        )

        if not matches:
            continue

        positives.append(path)

        partition = assign_partition(path)
        partitions[partition].append(path)

        metadata[path] = {
            "sha": sha,
            "count": len(matches),
            "terms": sorted(
                {item[2] for item in matches}
            ),
            "clusters": sorted(
                {item[3] for item in matches}
            ),
        }

    assert len(eligible) == EXPECTED_ELIGIBLE_TEXT
    assert len(positives) == EXPECTED_MATCHER_POSITIVE

    assert {
        partition: len(paths)
        for partition, paths in partitions.items()
    } == EXPECTED_PARTITION_COUNTS

    frozen_r7 = sorted(partitions["R2A-7"])

    assert len(frozen_r7) == 507

    records = current_records()

    assert len(records) == 273

    expected_ids = [
        f"R2A-DISPOSITION-R7-{number:04d}"
        for number in range(1, 274)
    ]

    assert [
        record["candidate_file_id"]
        for record in records
    ] == expected_ids

    assert len(
        {record["candidate_file_id"] for record in records}
    ) == 273

    assert len(
        {record["path"] for record in records}
    ) == 273

    assert len(
        {
            (
                record["path"],
                record["baseline_blob_sha"],
            )
            for record in records
        }
    ) == 273

    for record, expected_path in zip(
        records,
        frozen_r7[:273],
    ):
        expected = metadata[expected_path]

        assert record["path"] == expected_path
        assert record["baseline_blob_sha"] == expected["sha"]
        assert record["controlled_match_count"] == expected["count"]
        assert record["matched_terms"] == expected["terms"]
        assert record["matched_search_clusters"] == expected["clusters"]

    compatibility = records[150:156]

    assert [
        (
            int(
                record["candidate_file_id"].rsplit("-", 1)[1]
            ),
            record["path"],
            record["baseline_blob_sha"],
            record["controlled_match_count"],
        )
        for record in compatibility
    ] == COMPATIBILITY_EXPECTED

    assert all(
        record["disposition"]
        == "mixed_mapped_and_dismissed"
        for record in compatibility
    )

    assert all(
        record["authority_effect"]
        == "maps_current_authority"
        for record in compatibility
    )

    assert all(
        record["pressure_route"]
        == "later_r2b_candidate"
        for record in compatibility
    )

    assert not any(
        "R7-0508" in record["candidate_file_id"]
        for record in records
    )


def test_salvage_identity_prefix_integrity_and_manifest():
    # The accepted prefix before the corruption fracture remains
    # byte-identical.
    for number in range(1, 16):
        relative = (
            "docs/doctrine/reviews/r2a/"
            "dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )

        current = (ROOT / relative).read_bytes()
        historical = git_blob(
            REPAIR_START,
            relative,
        )

        assert current == historical

    old_records = historical_salvage_records()
    new_records = current_records()[156:]

    assert len(old_records) == 117
    assert len(new_records) == 117

    assert [
        record["candidate_file_id"]
        for record in old_records
    ] == [
        f"R2A-DISPOSITION-R7-{number:04d}"
        for number in range(151, 268)
    ]

    assert [
        record["candidate_file_id"]
        for record in new_records
    ] == [
        f"R2A-DISPOSITION-R7-{number:04d}"
        for number in range(157, 274)
    ]

    # Salvage preserves source identity and semantic-review content.
    # Candidate IDs shift by +6. The three lexical-discovery fields
    # are freshly recomputed from the frozen baseline matcher.
    lexical_fields = {
        "controlled_match_count",
        "matched_terms",
        "matched_search_clusters",
    }

    for old, new in zip(old_records, new_records):
        old_copy = dict(old)
        new_copy = dict(new)

        old_id = old_copy.pop("candidate_file_id")
        new_id = new_copy.pop("candidate_file_id")

        assert (
            int(new_id.rsplit("-", 1)[1])
            == int(old_id.rsplit("-", 1)[1]) + 6
        )

        # Source identity must remain unchanged.
        assert new_copy["path"] == old_copy["path"]
        assert (
            new_copy["baseline_blob_sha"]
            == old_copy["baseline_blob_sha"]
        )

        for field in lexical_fields:
            old_copy.pop(field)
            new_copy.pop(field)

        # All actual semantic-review material remains unchanged.
        assert new_copy == old_copy

    # The replay/corruption suffix is gone.
    for number in range(36, 49):
        assert not (
            DISPOSITIONS
            / f"dispositions_{number:04d}.yaml"
        ).exists()

    manifest = json.loads(
        MANIFEST.read_text(encoding="utf-8")
    )

    assert manifest["artifact_version"] == "0.2.10"
    assert manifest["status"] == "active_incomplete"

    partitions = {
        row["partition_id"]: row
        for row in manifest["partitions"]
    }

    assert partitions["R2A-7"]["status"] == "active_incomplete"
    assert partitions["R2A-8"]["status"] == "planned_not_present"

    expected_paths = [
        "docs/doctrine/reviews/r2a/"
        "dispositions_remaining/index.yaml",
        *[
            "docs/doctrine/reviews/r2a/"
            "dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
            for number in range(1, 36)
        ],
    ]

    assert (
        partitions["R2A-7"]["planned_artifact_paths"]
        == expected_paths
    )

    records = current_records()

    assert len(records) == 273
    assert records[0]["candidate_file_id"] == (
        "R2A-DISPOSITION-R7-0001"
    )
    assert records[-1]["candidate_file_id"] == (
        "R2A-DISPOSITION-R7-0273"
    )

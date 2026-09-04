"""Regression contract for the deterministic R2A-7 candidate-stream repair."""

from __future__ import annotations

import fnmatch
import io
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

    # Communicate the complete request and collect the complete response in
    # one subprocess operation. This avoids the write-before-read pipe
    # deadlock possible with git cat-file --batch on Windows.
    request = b"".join(
        sha.encode("ascii") + b"\n"
        for sha in unique
    )

    raw = subprocess.check_output(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        input=request,
    )

    stream = io.BytesIO(raw)
    result = {}

    for requested_sha in unique:
        header = stream.readline().rstrip(b"\n")
        parts = header.split()

        assert len(parts) == 3
        actual_sha = parts[0].decode("ascii")
        kind = parts[1].decode("ascii")
        size = int(parts[2])

        assert actual_sha == requested_sha
        assert kind == "blob"

        data = stream.read(size)
        assert len(data) == size
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

# ---------------------------------------------------------------------------
# Certified R2A-7 completion continuation through R7-0299.
#
# The corrective-repair tests above are retained as historical evidence.  The
# accepted repair checkpoint is now inspected at its merge commit so later
# lawful materialization does not make the historical "shards 0036..0048 were
# absent" assertion falsely fail against the live worktree.
# ---------------------------------------------------------------------------

REPAIR_ACCEPTED_HEAD = "a3f425045fe0f5435569e12a5c33b757ae2a6db0"
CERTIFIED_COMPLETION_LAST_SHARD = 40
CERTIFIED_COMPLETION_LAST_ID = 299

EXPECTED_COMPLETION_CLASSIFICATION = {274: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0021',
                              'R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 275: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-CORE-0014',
                              'R2A-SURFACE-WORLD-0004',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 276: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 277: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003', 'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 278: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0021',
                              'R2A-SURFACE-CORE-0014',
                              'R2A-SURFACE-WORLD-0004',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 279: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003', 'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'canon_handoff_pressure'},
 280: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 281: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 282: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 283: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 284: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 285: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 286: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 287: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 288: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 289: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 290: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 291: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 292: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 293: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 294: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 295: {'authority_effect': 'maps_current_authority',
       'disposition': 'mapped_semantic_surface',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'no_material_relation'},
 296: {'authority_effect': 'maps_current_authority',
       'disposition': 'mapped_semantic_surface',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'no_material_relation'},
 297: {'authority_effect': 'maps_current_authority',
       'disposition': 'mapped_semantic_surface',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'no_material_relation'},
 298: {'authority_effect': 'maps_current_authority',
       'disposition': 'mapped_semantic_surface',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'no_material_relation'},
 299: {'authority_effect': 'maps_current_authority',
       'disposition': 'mapped_semantic_surface',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'no_material_relation'}}


def _records_at_commit(commit: str, last_shard: int):
    records = []

    for number in range(1, last_shard + 1):
        relative = (
            "docs/doctrine/reviews/r2a/"
            "dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )
        document = json.loads(
            git_blob(commit, relative).decode("utf-8")
        )
        records.extend(document["candidate_file_dispositions"])

    return records


def _git_path_exists_at_commit(commit: str, relative: str) -> bool:
    return (
        subprocess.run(
            ["git", "cat-file", "-e", f"{commit}:{relative}"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def _current_records_through(last_shard: int):
    records = []

    for number in range(1, last_shard + 1):
        path = DISPOSITIONS / f"dispositions_{number:04d}.yaml"
        assert path.is_file()
        document = json.loads(path.read_text(encoding="utf-8"))
        records.extend(document["candidate_file_dispositions"])

    return records


def test_salvage_identity_prefix_integrity_and_manifest():
    # Historicalize the accepted corrective-repair checkpoint.  Later
    # completion shards are legitimate and must not rewrite repair history.
    for number in range(1, 16):
        relative = (
            "docs/doctrine/reviews/r2a/"
            "dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )
        assert git_blob(REPAIR_ACCEPTED_HEAD, relative) == git_blob(
            REPAIR_START,
            relative,
        )

    old_records = historical_salvage_records()
    repair_records = _records_at_commit(REPAIR_ACCEPTED_HEAD, 35)
    new_records = repair_records[156:]

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

        assert new_copy["path"] == old_copy["path"]
        assert (
            new_copy["baseline_blob_sha"]
            == old_copy["baseline_blob_sha"]
        )

        for field in lexical_fields:
            old_copy.pop(field)
            new_copy.pop(field)

        assert new_copy == old_copy

    for number in range(36, 49):
        relative = (
            "docs/doctrine/reviews/r2a/"
            "dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )
        assert not _git_path_exists_at_commit(
            REPAIR_ACCEPTED_HEAD,
            relative,
        )

    manifest = json.loads(
        git_blob(
            REPAIR_ACCEPTED_HEAD,
            "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
        ).decode("utf-8")
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

    assert len(repair_records) == 273
    assert repair_records[0]["candidate_file_id"] == (
        "R2A-DISPOSITION-R7-0001"
    )
    assert repair_records[-1]["candidate_file_id"] == (
        "R2A-DISPOSITION-R7-0273"
    )


def test_certified_completion_progress_through_r7_0299():
    entries = baseline_tree_entries()
    assert len(entries) == EXPECTED_TRACKED_BLOBS

    blobs = cat_blobs(sha for _, _, sha in entries)
    terms_by_cluster = matcher_terms()

    partitions = {
        "R2A-4": [],
        "R2A-5": [],
        "R2A-6": [],
        "R2A-7": [],
    }
    metadata = {}
    eligible_count = 0
    positive_count = 0

    for path, _mode, sha in entries:
        raw = blobs[sha]

        if excluded(path, raw):
            continue

        eligible_count += 1
        matches = controlled_matches(path, raw, terms_by_cluster)

        if not matches:
            continue

        positive_count += 1
        partition = assign_partition(path)
        partitions[partition].append(path)

        metadata[path] = {
            "sha": sha,
            "count": len(matches),
            "terms": sorted({item[2] for item in matches}),
            "clusters": sorted({item[3] for item in matches}),
        }

    assert eligible_count == EXPECTED_ELIGIBLE_TEXT
    assert positive_count == EXPECTED_MATCHER_POSITIVE
    assert {
        partition: len(paths)
        for partition, paths in partitions.items()
    } == EXPECTED_PARTITION_COUNTS

    frozen_r7 = sorted(partitions["R2A-7"])
    assert len(frozen_r7) == 507

    records = _current_records_through(
        CERTIFIED_COMPLETION_LAST_SHARD
    )

    assert len(records) == CERTIFIED_COMPLETION_LAST_ID
    assert [
        record["candidate_file_id"]
        for record in records
    ] == [
        f"R2A-DISPOSITION-R7-{number:04d}"
        for number in range(
            1,
            CERTIFIED_COMPLETION_LAST_ID + 1,
        )
    ]

    for record, expected_path in zip(
        records,
        frozen_r7[:CERTIFIED_COMPLETION_LAST_ID],
    ):
        expected = metadata[expected_path]

        assert record["path"] == expected_path
        assert record["baseline_blob_sha"] == expected["sha"]
        assert record["controlled_match_count"] == expected["count"]
        assert record["matched_terms"] == expected["terms"]
        assert (
            record["matched_search_clusters"]
            == expected["clusters"]
        )

    new_records = records[273:299]
    assert len(new_records) == 26

    for number, record in zip(range(274, 300), new_records):
        expected = EXPECTED_COMPLETION_CLASSIFICATION[number]

        assert record["disposition"] == expected["disposition"]
        assert (
            record["mapped_surface_ids"]
            == expected["mapped_surface_ids"]
        )
        assert (
            record["source_local_pressure_class"]
            == expected["source_local_pressure_class"]
        )
        assert (
            record["authority_effect"]
            == expected["authority_effect"]
        )
        assert record["pressure_route"] == expected["pressure_route"]

        mapping_ids = [
            item["mapped_surface_id"]
            for item in record["mapping_evidence"]
        ]
        assert mapping_ids == record["mapped_surface_ids"]
        assert all(
            item["authority_transfer_effect"] == "none"
            for item in record["mapping_evidence"]
        )

        for locator in record["representative_locators"]:
            assert locator["matched_terms"] == []
            assert locator["matched_search_clusters"] == []
            assert 1 <= locator["line_start"] <= locator["line_end"]
            assert locator["semantic_review_note"].strip()

        assert record["status_evidence"] is not None

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["artifact_version"] == "0.2.11"
    assert manifest["status"] == "active_incomplete"

    by_partition = {
        row["partition_id"]: row
        for row in manifest["partitions"]
    }

    assert by_partition["R2A-7"]["status"] == "active_incomplete"
    assert by_partition["R2A-8"]["status"] == "planned_not_present"

    expected_paths = [
        "docs/doctrine/reviews/r2a/"
        "dispositions_remaining/index.yaml",
        *[
            "docs/doctrine/reviews/r2a/"
            "dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
            for number in range(1, 41)
        ],
    ]
    assert (
        by_partition["R2A-7"]["planned_artifact_paths"]
        == expected_paths
    )

    assert not (DISPOSITIONS / "index.yaml").exists()
    for number in range(41, 49):
        assert not (
            DISPOSITIONS / f"dispositions_{number:04d}.yaml"
        ).exists()

    assert records[-1]["candidate_file_id"] == (
        "R2A-DISPOSITION-R7-0299"
    )
    assert frozen_r7[299]
    assert not any(
        record["candidate_file_id"] == "R2A-DISPOSITION-R7-0508"
        for record in records
    )

# ---------------------------------------------------------------------------
# Certified R2A-7 completion continuation through R7-0356.
#
# The earlier R7-0299 live checkpoint remains in the file as accepted evidence.
# This successor historicalizes that checkpoint at the #363 merge commit and
# advances only the live deterministic stream through shard 0046.
# ---------------------------------------------------------------------------

R2A7_COMPLETION_0356_BASE = "6cbf63d78face218d056742b9384bb56d00700dd"
R2A7_COMPLETION_0356_LAST_SHARD = 46
R2A7_COMPLETION_0356_LAST_ID = 356

EXPECTED_COMPLETION_0356_CLASSIFICATION = {300: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 301: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 302: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001', 'R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 303: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 304: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 305: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 306: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 307: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 308: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 309: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001', 'R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 310: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003', 'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 311: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 312: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011', 'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'canon_handoff_pressure'},
 313: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'canon_handoff_pressure'},
 314: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011', 'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'canon_handoff_pressure'},
 315: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 316: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011', 'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'canon_handoff_pressure'},
 317: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 318: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 319: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 320: {'authority_effect': 'historical_context_only',
       'disposition': 'historical_only',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 321: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 322: {'authority_effect': 'historical_context_only',
       'disposition': 'historical_only',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 323: {'authority_effect': 'no_authority_effect',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'none',
       'source_local_pressure_class': 'no_material_relation'},
 324: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 325: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 326: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 327: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 328: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 329: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 330: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 331: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 332: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 333: {'authority_effect': 'no_authority_effect',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'none',
       'source_local_pressure_class': 'no_material_relation'},
 334: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 335: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 336: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 337: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 338: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 339: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 340: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 341: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 342: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 343: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 344: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 345: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 346: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 347: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 348: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 349: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 350: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 351: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 352: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 353: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 354: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 355: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 356: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'}}


def test_certified_completion_progress_through_r7_0299():
    records = _records_at_commit(R2A7_COMPLETION_0356_BASE, 40)

    assert len(records) == 299
    assert records[0]["candidate_file_id"] == "R2A-DISPOSITION-R7-0001"
    assert records[-1]["candidate_file_id"] == "R2A-DISPOSITION-R7-0299"

    manifest = json.loads(
        git_blob(
            R2A7_COMPLETION_0356_BASE,
            MANIFEST.relative_to(ROOT).as_posix(),
        ).decode("utf-8")
    )
    assert manifest["artifact_version"] == "0.2.11"

    by_partition = {
        row["partition_id"]: row
        for row in manifest["partitions"]
    }
    assert by_partition["R2A-7"]["status"] == "active_incomplete"
    assert by_partition["R2A-8"]["status"] == "planned_not_present"
    assert by_partition["R2A-7"]["planned_artifact_paths"] == [
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        *[
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
            for number in range(1, 41)
        ],
    ]


def test_certified_completion_progress_through_r7_0356():
    entries = baseline_tree_entries()
    assert len(entries) == EXPECTED_TRACKED_BLOBS

    blobs = cat_blobs(sha for _, _, sha in entries)
    terms_by_cluster = matcher_terms()

    partitions = {
        "R2A-4": [],
        "R2A-5": [],
        "R2A-6": [],
        "R2A-7": [],
    }
    metadata = {}
    eligible_count = 0
    positive_count = 0

    for path, _mode, sha in entries:
        raw = blobs[sha]

        if excluded(path, raw):
            continue

        eligible_count += 1
        matches = controlled_matches(path, raw, terms_by_cluster)

        if not matches:
            continue

        positive_count += 1
        partition = assign_partition(path)
        partitions[partition].append(path)

        metadata[path] = {
            "sha": sha,
            "count": len(matches),
            "terms": sorted({item[2] for item in matches}),
            "clusters": sorted({item[3] for item in matches}),
        }

    assert eligible_count == EXPECTED_ELIGIBLE_TEXT
    assert positive_count == EXPECTED_MATCHER_POSITIVE
    assert {
        partition: len(paths)
        for partition, paths in partitions.items()
    } == EXPECTED_PARTITION_COUNTS

    frozen_r7 = sorted(partitions["R2A-7"])
    assert len(frozen_r7) == 507

    # Preserve the entire previously certified through-R7-0299 payload.
    for number in range(1, 41):
        relative = (
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )
        assert git_blob(
            R2A7_COMPLETION_0356_BASE,
            relative,
        ) == (DISPOSITIONS / f"dispositions_{number:04d}.yaml").read_bytes()

    records = _current_records_through(
        R2A7_COMPLETION_0356_LAST_SHARD
    )

    assert len(records) == R2A7_COMPLETION_0356_LAST_ID
    assert [
        record["candidate_file_id"]
        for record in records
    ] == [
        f"R2A-DISPOSITION-R7-{number:04d}"
        for number in range(1, R2A7_COMPLETION_0356_LAST_ID + 1)
    ]

    assert len({record["path"] for record in records}) == len(records)
    assert len({
        (record["path"], record["baseline_blob_sha"])
        for record in records
    }) == len(records)

    for record, expected_path in zip(
        records,
        frozen_r7[:R2A7_COMPLETION_0356_LAST_ID],
    ):
        expected = metadata[expected_path]

        assert record["path"] == expected_path
        assert record["baseline_blob_sha"] == expected["sha"]
        assert record["controlled_match_count"] == expected["count"]
        assert record["matched_terms"] == expected["terms"]
        assert (
            record["matched_search_clusters"]
            == expected["clusters"]
        )

    new_records = records[299:356]
    assert len(new_records) == 57

    for number, record in zip(range(300, 357), new_records):
        expected = EXPECTED_COMPLETION_0356_CLASSIFICATION[number]

        assert record["disposition"] == expected["disposition"]
        assert (
            record["mapped_surface_ids"]
            == expected["mapped_surface_ids"]
        )
        assert (
            record["source_local_pressure_class"]
            == expected["source_local_pressure_class"]
        )
        assert (
            record["authority_effect"]
            == expected["authority_effect"]
        )
        assert record["pressure_route"] == expected["pressure_route"]

        mapping_ids = [
            item["mapped_surface_id"]
            for item in record["mapping_evidence"]
        ]
        assert mapping_ids == record["mapped_surface_ids"]
        assert all(
            item["authority_transfer_effect"] == "none"
            for item in record["mapping_evidence"]
        )

        for locator in record["representative_locators"]:
            assert locator["matched_terms"] == []
            assert locator["matched_search_clusters"] == []
            assert 1 <= locator["line_start"] <= locator["line_end"]
            assert locator["semantic_review_note"].strip()

        status_evidence = record["status_evidence"]
        if status_evidence is not None:
            assert (
                1
                <= status_evidence["line_start"]
                <= status_evidence["line_end"]
            )
            assert status_evidence["source_status_summary"].strip()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["artifact_version"] == "0.2.12"
    assert manifest["status"] == "active_incomplete"

    by_partition = {
        row["partition_id"]: row
        for row in manifest["partitions"]
    }

    assert by_partition["R2A-7"]["status"] == "active_incomplete"
    assert by_partition["R2A-8"]["status"] == "planned_not_present"

    expected_paths = [
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        *[
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
            for number in range(1, 47)
        ],
    ]
    assert (
        by_partition["R2A-7"]["planned_artifact_paths"]
        == expected_paths
    )

    assert not (DISPOSITIONS / "index.yaml").exists()
    for number in range(47, 49):
        assert not (
            DISPOSITIONS / f"dispositions_{number:04d}.yaml"
        ).exists()

    assert records[-1]["candidate_file_id"] == (
        "R2A-DISPOSITION-R7-0356"
    )
    assert records[-1]["path"] == frozen_r7[355]
    assert frozen_r7[356]
    assert not any(
        record["candidate_file_id"] == "R2A-DISPOSITION-R7-0508"
        for record in records
    )

# ---------------------------------------------------------------------------
# Certified R2A-7 completion continuation through R7-0403.
#
# The earlier R7-0356 live checkpoint remains in the file as accepted evidence.
# This successor historicalizes that checkpoint at the #364 merge commit and
# advances only the live deterministic stream through shard 0051.
# ---------------------------------------------------------------------------

R2A7_COMPLETION_0403_BASE = "83c9bd211048e608645426157703980e98150871"
R2A7_COMPLETION_0403_LAST_SHARD = 51
R2A7_COMPLETION_0403_LAST_ID = 403

EXPECTED_COMPLETION_0403_CLASSIFICATION = {357: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003', 'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 358: {'authority_effect': 'no_authority_effect',
       'disposition': 'internal_nonauthoritative_pressure_only',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'no_material_relation'},
 359: {'authority_effect': 'no_authority_effect',
       'disposition': 'internal_nonauthoritative_pressure_only',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'no_material_relation'},
 360: {'authority_effect': 'no_authority_effect',
       'disposition': 'internal_nonauthoritative_pressure_only',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'no_material_relation'},
 361: {'authority_effect': 'no_authority_effect',
       'disposition': 'internal_nonauthoritative_pressure_only',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'no_material_relation'},
 362: {'authority_effect': 'historical_context_only',
       'disposition': 'historical_only',
       'mapped_surface_ids': [],
       'pressure_route': 'none',
       'source_local_pressure_class': 'no_material_relation'},
 363: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'internal_nonauthoritative_pressure_only',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'no_material_relation'},
 364: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 365: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 366: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 367: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 368: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 369: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 370: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 371: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 372: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 373: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 374: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 375: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 376: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 377: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 378: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-WORLD-0011'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'consistent_source_local_evidence'},
 379: {'authority_effect': 'no_authority_effect',
       'disposition': 'internal_nonauthoritative_pressure_only',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'no_material_relation'},
 380: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0024'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 381: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 382: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-AGENCY-0002',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 383: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 384: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 385: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 386: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003', 'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 387: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 388: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 389: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'none',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 390: {'authority_effect': 'implementation_presupposition_only',
       'disposition': 'dismissed_after_semantic_review',
       'mapped_surface_ids': [],
       'pressure_route': 'later_gate',
       'source_local_pressure_class': 'conversion_handoff_pressure'},
 391: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 392: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 393: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 394: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 395: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 396: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 397: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 398: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 399: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 400: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 401: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'later_r2b_candidate',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 402: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'r3_conformance',
       'source_local_pressure_class': 'owner_boundary_pressure'},
 403: {'authority_effect': 'maps_current_authority',
       'disposition': 'mixed_mapped_and_dismissed',
       'mapped_surface_ids': ['R2A-SURFACE-CORE-0003',
                              'R2A-SURFACE-WORLD-0011',
                              'R2A-SURFACE-CROSSPHASE-0001'],
       'pressure_route': 'r3_conformance',
       'source_local_pressure_class': 'owner_boundary_pressure'}}


def test_certified_completion_progress_through_r7_0356():
    records = _records_at_commit(R2A7_COMPLETION_0403_BASE, 46)

    assert len(records) == 356
    assert records[0]["candidate_file_id"] == "R2A-DISPOSITION-R7-0001"
    assert records[-1]["candidate_file_id"] == "R2A-DISPOSITION-R7-0356"

    manifest = json.loads(
        git_blob(
            R2A7_COMPLETION_0403_BASE,
            MANIFEST.relative_to(ROOT).as_posix(),
        ).decode("utf-8")
    )
    assert manifest["artifact_version"] == "0.2.12"

    by_partition = {
        row["partition_id"]: row
        for row in manifest["partitions"]
    }
    assert by_partition["R2A-7"]["status"] == "active_incomplete"
    assert by_partition["R2A-8"]["status"] == "planned_not_present"
    assert by_partition["R2A-7"]["planned_artifact_paths"] == [
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        *[
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
            for number in range(1, 47)
        ],
    ]


def test_certified_completion_progress_through_r7_0403():
    entries = baseline_tree_entries()
    assert len(entries) == EXPECTED_TRACKED_BLOBS

    blobs = cat_blobs(sha for _, _, sha in entries)
    terms_by_cluster = matcher_terms()

    partitions = {
        "R2A-4": [],
        "R2A-5": [],
        "R2A-6": [],
        "R2A-7": [],
    }
    metadata = {}
    eligible_count = 0
    positive_count = 0

    for path, _mode, sha in entries:
        raw = blobs[sha]

        if excluded(path, raw):
            continue

        eligible_count += 1
        matches = controlled_matches(path, raw, terms_by_cluster)

        if not matches:
            continue

        positive_count += 1
        partition = assign_partition(path)
        partitions[partition].append(path)

        metadata[path] = {
            "sha": sha,
            "count": len(matches),
            "terms": sorted({item[2] for item in matches}),
            "clusters": sorted({item[3] for item in matches}),
        }

    assert eligible_count == EXPECTED_ELIGIBLE_TEXT
    assert positive_count == EXPECTED_MATCHER_POSITIVE
    assert {
        partition: len(paths)
        for partition, paths in partitions.items()
    } == EXPECTED_PARTITION_COUNTS

    frozen_r7 = sorted(partitions["R2A-7"])
    assert len(frozen_r7) == 507
    assert not any(path.endswith("R7-0508") for path in frozen_r7)

    # Preserve the entire previously certified through-R7-0356 payload.
    for number in range(1, 47):
        relative = (
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
        )
        assert git_blob(
            R2A7_COMPLETION_0403_BASE,
            relative,
        ) == (DISPOSITIONS / f"dispositions_{number:04d}.yaml").read_bytes()

    records = _current_records_through(
        R2A7_COMPLETION_0403_LAST_SHARD
    )

    assert len(records) == R2A7_COMPLETION_0403_LAST_ID
    assert [
        record["candidate_file_id"]
        for record in records
    ] == [
        f"R2A-DISPOSITION-R7-{number:04d}"
        for number in range(1, R2A7_COMPLETION_0403_LAST_ID + 1)
    ]

    assert len({record["path"] for record in records}) == len(records)
    assert len({
        (record["path"], record["baseline_blob_sha"])
        for record in records
    }) == len(records)

    for record, expected_path in zip(
        records,
        frozen_r7[:R2A7_COMPLETION_0403_LAST_ID],
    ):
        expected = metadata[expected_path]

        assert record["path"] == expected_path
        assert record["baseline_blob_sha"] == expected["sha"]
        assert record["controlled_match_count"] == expected["count"]
        assert record["matched_terms"] == expected["terms"]
        assert record["matched_search_clusters"] == expected["clusters"]

    new_records = records[356:403]
    assert len(new_records) == 47

    for number, record in zip(range(357, 404), new_records):
        expected = EXPECTED_COMPLETION_0403_CLASSIFICATION[number]

        assert record["disposition"] == expected["disposition"]
        assert record["mapped_surface_ids"] == expected["mapped_surface_ids"]
        assert (
            record["source_local_pressure_class"]
            == expected["source_local_pressure_class"]
        )
        assert record["authority_effect"] == expected["authority_effect"]
        assert record["pressure_route"] == expected["pressure_route"]

        mapping_ids = [
            item["mapped_surface_id"]
            for item in record["mapping_evidence"]
        ]
        assert mapping_ids == record["mapped_surface_ids"]
        assert all(
            item["authority_transfer_effect"] == "none"
            for item in record["mapping_evidence"]
        )
        for item in record["mapping_evidence"]:
            locator = item["candidate_locator"]
            assert 1 <= locator["line_start"] <= locator["line_end"]
            assert locator["line_end"] - locator["line_start"] <= 79
            assert item["candidate_proposition"].strip()
            assert item["evidence_note"].strip()

        for locator in record["representative_locators"]:
            assert locator["matched_terms"] == []
            assert locator["matched_search_clusters"] == []
            assert 1 <= locator["line_start"] <= locator["line_end"]
            assert locator["semantic_review_note"].strip()

        status_evidence = record["status_evidence"]
        if status_evidence is not None:
            assert (
                1
                <= status_evidence["line_start"]
                <= status_evidence["line_end"]
            )
            assert status_evidence["source_status_summary"].strip()

    internal = [
        record for record in new_records
        if record["disposition"]
        == "internal_nonauthoritative_pressure_only"
    ]
    assert len(internal) == 6
    assert all(
        record["mapped_surface_ids"] == []
        and record["source_local_pressure_class"] == "no_material_relation"
        and record["authority_effect"] in {
            "implementation_presupposition_only",
            "escalation_pressure_only",
            "no_authority_effect",
        }
        for record in internal
    )

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["artifact_version"] == "0.2.13"
    assert manifest["status"] == "active_incomplete"

    by_partition = {
        row["partition_id"]: row
        for row in manifest["partitions"]
    }
    assert by_partition["R2A-7"]["status"] == "active_incomplete"
    assert by_partition["R2A-8"]["status"] == "planned_not_present"

    expected_paths = [
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        *[
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
            for number in range(1, 52)
        ],
    ]
    assert by_partition["R2A-7"]["planned_artifact_paths"] == expected_paths

    assert not (DISPOSITIONS / "index.yaml").exists()
    assert not (DISPOSITIONS / "dispositions_0052.yaml").exists()

    assert records[-1]["candidate_file_id"] == "R2A-DISPOSITION-R7-0403"
    assert records[-1]["path"] == frozen_r7[402]
    assert frozen_r7[403]
    assert not any(
        record["candidate_file_id"] == "R2A-DISPOSITION-R7-0508"
        for record in records
    )

# ---------------------------------------------------------------------------
# Final certified R2A-7 completion through R7-0507.
#
# Historical checkpoint bodies above remain accepted provenance. This block
# advances only the live deterministic R2A-7 stream and closes that partition;
# it does not advance R2A-8 or R2A as a whole.
# ---------------------------------------------------------------------------

import hashlib as _r2a7_final_hashlib

R2A7_FINAL_COMPLETION_BASE = "ff01a35704067095ab01c01c977a7239fc51ec40"
R2A7_FINAL_LAST_SHARD = 62
R2A7_FINAL_LAST_ID = 507
R2A7_FINAL_SEMANTIC_DIGEST = "3d01e80465bb54e3cc17faa14dded19903b0102a5b4566915fc73a3c59d6b338"


def _r2a7_final_records():
    records = []
    for number in range(1, R2A7_FINAL_LAST_SHARD + 1):
        path = DISPOSITIONS / f"dispositions_{number:04d}.yaml"
        assert path.is_file()
        document = json.loads(path.read_text(encoding="utf-8"))
        records.extend(document["candidate_file_dispositions"])
    return records


def _r2a7_final_semantic_digest(records):
    keys = [
        "candidate_file_id",
        "disposition",
        "mapped_surface_ids",
        "source_local_pressure_class",
        "authority_effect",
        "pressure_route",
    ]
    payload = [{key: record[key] for key in keys} for record in records]
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return _r2a7_final_hashlib.sha256(raw).hexdigest()


def test_r2a7_final_507_candidate_stream_and_semantic_closeout():
    entries = baseline_tree_entries()
    assert len(entries) == EXPECTED_TRACKED_BLOBS
    blobs = cat_blobs(sha for _, _, sha in entries)
    terms_by_cluster = matcher_terms()
    partitions = {"R2A-4": [], "R2A-5": [], "R2A-6": [], "R2A-7": []}
    metadata = {}
    eligible = 0
    positives = 0
    for path, _mode, sha in entries:
        raw = blobs[sha]
        if excluded(path, raw):
            continue
        eligible += 1
        matches = controlled_matches(path, raw, terms_by_cluster)
        if not matches:
            continue
        positives += 1
        partition = assign_partition(path)
        partitions[partition].append(path)
        metadata[path] = {
            "sha": sha,
            "count": len(matches),
            "terms": sorted({item[2] for item in matches}),
            "clusters": sorted({item[3] for item in matches}),
        }
    assert eligible == EXPECTED_ELIGIBLE_TEXT
    assert positives == EXPECTED_MATCHER_POSITIVE
    assert {key: len(value) for key, value in partitions.items()} == EXPECTED_PARTITION_COUNTS
    frozen_r7 = sorted(partitions["R2A-7"])
    assert len(frozen_r7) == 507

    records = _r2a7_final_records()
    assert len(records) == 507
    assert [record["candidate_file_id"] for record in records] == [
        f"R2A-DISPOSITION-R7-{number:04d}" for number in range(1, 508)
    ]
    assert len({record["path"] for record in records}) == 507
    assert len({(record["path"], record["baseline_blob_sha"]) for record in records}) == 507
    for record, expected_path in zip(records, frozen_r7):
        expected = metadata[expected_path]
        assert record["path"] == expected_path
        assert record["baseline_blob_sha"] == expected["sha"]
        assert record["controlled_match_count"] == expected["count"]
        assert record["matched_terms"] == expected["terms"]
        assert record["matched_search_clusters"] == expected["clusters"]
        assert [item["mapped_surface_id"] for item in record["mapping_evidence"]] == record["mapped_surface_ids"]
        assert all(item["authority_transfer_effect"] == "none" for item in record["mapping_evidence"])
    assert not any("R7-0508" in record["candidate_file_id"] for record in records)
    assert not (DISPOSITIONS / "dispositions_0063.yaml").exists()
    assert _r2a7_final_semantic_digest(records[403:]) == R2A7_FINAL_SEMANTIC_DIGEST


def test_r2a7_final_index_manifest_and_r2a8_boundary():
    index_path = DISPOSITIONS / "index.yaml"
    assert index_path.is_file()
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert index["status"] == "complete"
    assert index["phase"] == "R2A-7"
    assert index["candidate_file_count"] == 507
    assert len(index["shards"]) == 62
    assert index["shards"][0]["first_candidate_file_id"] == "R2A-DISPOSITION-R7-0001"
    assert index["shards"][-1]["last_candidate_file_id"] == "R2A-DISPOSITION-R7-0507"
    for shard in index["shards"]:
        path = ROOT / shard["path"]
        assert path.is_file()
        assert _r2a7_final_hashlib.sha256(path.read_bytes()).hexdigest() == shard["content_sha256"]

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["artifact_version"] == "0.2.14"
    assert manifest["status"] == "active_incomplete"
    by_partition = {row["partition_id"]: row for row in manifest["partitions"]}
    assert by_partition["R2A-7"]["status"] == "complete"
    assert by_partition["R2A-8"]["status"] == "planned_not_present"
    assert by_partition["R2A-7"]["planned_artifact_paths"] == [
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        *[
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
            for number in range(1, 63)
        ],
    ]
    assert not (ROOT / "docs/doctrine/reviews/r2a/aggregate_receipts/index.yaml").exists()

# ---------------------------------------------------------------------------
# R7-0403 accepted-checkpoint historicalization repair.
#
# The original through-R7-0403 body above remains accepted provenance. Once
# R7-0507 materialization exists, that old body must not read the live manifest
# or live shard-absence state. This replacement binds the checkpoint to the
# accepted PR #365 merge commit, which is the final-completion base.
# ---------------------------------------------------------------------------

R2A7_ACCEPTED_COMPLETION_0403_HEAD = R2A7_FINAL_COMPLETION_BASE


def _r2a7_historical_path_exists(commit: str, path: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{commit}:{path}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def test_certified_completion_progress_through_r7_0403():
    records = _records_at_commit(
        R2A7_ACCEPTED_COMPLETION_0403_HEAD,
        R2A7_COMPLETION_0403_LAST_SHARD,
    )

    assert len(records) == R2A7_COMPLETION_0403_LAST_ID
    assert records[0]["candidate_file_id"] == "R2A-DISPOSITION-R7-0001"
    assert records[-1]["candidate_file_id"] == "R2A-DISPOSITION-R7-0403"

    assert [
        record["candidate_file_id"]
        for record in records
    ] == [
        f"R2A-DISPOSITION-R7-{number:04d}"
        for number in range(1, 404)
    ]

    assert len({record["path"] for record in records}) == 403
    assert len({
        (record["path"], record["baseline_blob_sha"])
        for record in records
    }) == 403

    new_records = records[356:403]
    assert len(new_records) == 47

    for number, record in zip(range(357, 404), new_records):
        expected = EXPECTED_COMPLETION_0403_CLASSIFICATION[number]

        assert record["disposition"] == expected["disposition"]
        assert record["mapped_surface_ids"] == expected["mapped_surface_ids"]
        assert (
            record["source_local_pressure_class"]
            == expected["source_local_pressure_class"]
        )
        assert record["authority_effect"] == expected["authority_effect"]
        assert record["pressure_route"] == expected["pressure_route"]

        assert [
            item["mapped_surface_id"]
            for item in record["mapping_evidence"]
        ] == record["mapped_surface_ids"]
        assert all(
            item["authority_transfer_effect"] == "none"
            for item in record["mapping_evidence"]
        )

        for locator in record["representative_locators"]:
            assert locator["matched_terms"] == []
            assert locator["matched_search_clusters"] == []
            assert 1 <= locator["line_start"] <= locator["line_end"]
            assert locator["semantic_review_note"].strip()

        status_evidence = record["status_evidence"]
        if status_evidence is not None:
            assert (
                1
                <= status_evidence["line_start"]
                <= status_evidence["line_end"]
            )
            assert status_evidence["source_status_summary"].strip()

    internal = [
        record
        for record in new_records
        if record["disposition"]
        == "internal_nonauthoritative_pressure_only"
    ]
    assert len(internal) == 6
    assert all(
        record["mapped_surface_ids"] == []
        and record["source_local_pressure_class"] == "no_material_relation"
        and record["authority_effect"] in {
            "implementation_presupposition_only",
            "escalation_pressure_only",
            "no_authority_effect",
        }
        for record in internal
    )

    manifest = json.loads(
        git_blob(
            R2A7_ACCEPTED_COMPLETION_0403_HEAD,
            MANIFEST.relative_to(ROOT).as_posix(),
        ).decode("utf-8")
    )

    assert manifest["artifact_version"] == "0.2.13"
    assert manifest["status"] == "active_incomplete"

    by_partition = {
        row["partition_id"]: row
        for row in manifest["partitions"]
    }

    assert by_partition["R2A-7"]["status"] == "active_incomplete"
    assert by_partition["R2A-8"]["status"] == "planned_not_present"
    assert by_partition["R2A-7"]["planned_artifact_paths"] == [
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
        *[
            "docs/doctrine/reviews/r2a/dispositions_remaining/"
            f"dispositions_{number:04d}.yaml"
            for number in range(1, 52)
        ],
    ]

    assert not _r2a7_historical_path_exists(
        R2A7_ACCEPTED_COMPLETION_0403_HEAD,
        "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
    )
    assert not _r2a7_historical_path_exists(
        R2A7_ACCEPTED_COMPLETION_0403_HEAD,
        "docs/doctrine/reviews/r2a/dispositions_remaining/"
        "dispositions_0052.yaml",
    )

    assert not any(
        record["candidate_file_id"] == "R2A-DISPOSITION-R7-0508"
        for record in records
    )

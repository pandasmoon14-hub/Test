from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _load_simple_yaml_root_map(path: Path, root_key: str) -> dict[str, dict[str, Any]]:
    lines = [ln.rstrip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.strip().startswith("#")]
    if not lines or lines[0].strip() != f"{root_key}:":
        raise ValueError(f"invalid_root:{root_key}")
    out: dict[str, dict[str, Any]] = {}
    current = None
    for ln in lines[1:]:
        if ln.startswith("  ") and not ln.startswith("    ") and ln.endswith(":"):
            current = ln.strip()[:-1]
            out[current] = {}
            continue
        if current is None:
            continue
        if ln.startswith("    ") and ":" in ln:
            k, v = ln.strip().split(":", 1)
            out[current][k] = v.strip()
    return out


def _sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _estimate_family(rel: str, templates: set[str]) -> tuple[list[str], str]:
    l = rel.lower()
    matches = []
    kw = {
        "adventure_path_scenario": ["adventure", "scenario", "campaign", "path"],
        "bestiary_statblock_heavy": ["bestiary", "monster", "statblock"],
        "random_table_loot": ["random", "table", "loot"],
        "setting_world_guide": ["setting", "world", "gazetteer", "lore"],
        "d20_class_level_fantasy": ["core", "rulebook", "player", "gm"],
        "map_diagram_heavy": ["map", "diagram"],
        "scanned_or_ocr_heavy": ["scan", "ocr", "image-only"],
    }
    for tid, words in kw.items():
        if any(w in l for w in words) and (not templates or tid in templates):
            matches.append(tid)
    if not matches:
        return ["unclassified_or_mixed_donor_family"], "low"
    return sorted(set(matches)), "medium" if len(matches) == 1 else "high"


def _estimate_queues(rel: str, size: int, ext: str, queue_ids: set[str]) -> list[str]:
    l = rel.lower()
    out = []
    def add(q: str):
        if (not queue_ids or q in queue_ids) and q not in out:
            out.append(q)
    if size == 0:
        add("unreadable_or_corrupt_pdf")
    if size < 1024:
        add("source_metadata_gap")
    if any(x in l for x in ["scan", "ocr", "image-only"]):
        add("scanned_or_image_only")
        add("low_confidence_extraction")
    if any(x in l for x in ["map", "diagram"]):
        add("map_diagram_review")
    if any(x in l for x in ["tmp", "partial", ".crdownload", ".part"]):
        add("manual_review_required")
    if ext != ".pdf":
        add("manual_review_required")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--output-json")
    ap.add_argument("--max-files", type=int)
    ap.add_argument("--include-ext", nargs="*", default=[".pdf"])
    ap.add_argument("--resume-existing", action="store_true")
    ap.add_argument("--donor-family-templates")
    ap.add_argument("--repair-queues")
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    issues: list[dict[str, str]] = []
    output_files: list[str] = []

    corpus = Path(args.corpus_dir)
    outdir = Path(args.output_dir)
    strict = bool(args.strict)

    templates: set[str] = set()
    queue_ids: set[str] = set()

    try:
        if not corpus.exists() or not corpus.is_dir():
            errors.append("missing_corpus_dir")

        if args.donor_family_templates:
            tpath = Path(args.donor_family_templates)
            if not tpath.exists():
                errors.append("missing_donor_family_templates")
            else:
                try:
                    templates = set(_load_simple_yaml_root_map(tpath, "templates").keys())
                except Exception:
                    errors.append("invalid_donor_family_templates")

        if args.repair_queues:
            qpath = Path(args.repair_queues)
            if not qpath.exists():
                errors.append("missing_repair_queues")
            else:
                try:
                    queue_ids = set(_load_simple_yaml_root_map(qpath, "queues").keys())
                except Exception:
                    errors.append("invalid_repair_queues")

        outdir.mkdir(parents=True, exist_ok=True)

        include_ext = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in args.include_ext}
        all_files = sorted([p for p in corpus.rglob("*") if p.is_file()]) if corpus.exists() else []
        if args.max_files is not None:
            all_files = all_files[: args.max_files]

        records = []
        name_map = defaultdict(list)
        hash_map = defaultdict(list)
        supported = 0
        unsupported = 0
        total_bytes = 0

        for p in all_files:
            ext = p.suffix.lower()
            rel = p.relative_to(corpus).as_posix() if corpus.exists() else p.name
            size = p.stat().st_size
            total_bytes += size
            is_supported = ext in include_ext
            if is_supported:
                supported += 1
            else:
                unsupported += 1
                issues.append({"issue_code": "unsupported_extension", "path": rel, "detail": ext or "<none>", "severity": "warning"})

            digest = _sha256_file(p)
            name_map[p.name.lower()].append(rel)
            hash_map[digest].append(rel)

            family_ids, conf = _estimate_family(rel, templates)
            queues = _estimate_queues(rel, size, ext, queue_ids)

            if size == 0:
                issues.append({"issue_code": "zero_byte_file", "path": rel, "detail": "size=0", "severity": "warning"})
            if size < 1024:
                issues.append({"issue_code": "unusually_small_file", "path": rel, "detail": str(size), "severity": "warning"})
            if size > 200 * 1024 * 1024:
                issues.append({"issue_code": "unusually_large_file", "path": rel, "detail": str(size), "severity": "warning"})
            if len(str(p)) > 240:
                issues.append({"issue_code": "very_long_path", "path": rel, "detail": str(len(str(p))), "severity": "warning"})
            try:
                str(p).encode("ascii")
            except UnicodeEncodeError:
                issues.append({"issue_code": "non_ascii_path", "path": rel, "detail": "non-ascii", "severity": "warning"})
            if any(x in rel.lower() for x in [".crdownload", ".part", ".tmp", "download"]):
                issues.append({"issue_code": "suspicious_temporary_fragment", "path": rel, "detail": "filename_hint", "severity": "warning"})

            records.append({
                "absolute_path": str(p.resolve()),
                "relative_path": rel,
                "file_name": p.name,
                "extension": ext,
                "size_bytes": size,
                "modified_time": datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat(),
                "content_hash_sha256": digest,
                "supported": is_supported,
                "donor_family_candidates": family_ids,
                "donor_family_confidence": conf,
                "repair_queue_candidates": queues,
            })

        for _, rels in name_map.items():
            if len(rels) > 1:
                for r in rels:
                    issues.append({"issue_code": "duplicate_file_name", "path": r, "detail": f"count={len(rels)}", "severity": "warning"})
        dup_hash_groups = 0
        for _, rels in hash_map.items():
            if len(rels) > 1:
                dup_hash_groups += 1
                for r in rels:
                    issues.append({"issue_code": "duplicate_content_hash", "path": r, "detail": f"count={len(rels)}", "severity": "warning"})

        if supported == 0:
            errors.append("no_supported_files_found")

        manifest_json = outdir / "full_corpus_dry_run_manifest.json"
        manifest_csv = outdir / "full_corpus_dry_run_manifest.csv"
        report_md = outdir / "full_corpus_dry_run_report.md"
        issues_csv = outdir / "full_corpus_preflight_issues.csv"
        families_csv = outdir / "full_corpus_donor_family_estimates.csv"

        manifest = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "corpus_dir": str(corpus),
            "files": records,
        }
        manifest_json.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        output_files.append(str(manifest_json))

        with manifest_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["relative_path", "file_name", "extension", "size_bytes", "modified_time", "content_hash_sha256", "supported", "donor_family_confidence"])
            w.writeheader()
            for r in records:
                w.writerow({k: r[k] for k in w.fieldnames})
        output_files.append(str(manifest_csv))

        with issues_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["issue_code", "path", "detail", "severity"])
            w.writeheader(); w.writerows(issues)
        output_files.append(str(issues_csv))

        with families_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["relative_path", "donor_family_candidates", "confidence", "repair_queue_candidates"])
            w.writeheader()
            for r in records:
                w.writerow({
                    "relative_path": r["relative_path"],
                    "donor_family_candidates": "|".join(r["donor_family_candidates"]),
                    "confidence": r["donor_family_confidence"],
                    "repair_queue_candidates": "|".join(r["repair_queue_candidates"]),
                })
        output_files.append(str(families_csv))

        fam_counts = Counter()
        queue_counts = Counter()
        for r in records:
            for f in r["donor_family_candidates"]:
                fam_counts[f] += 1
            for q in r["repair_queue_candidates"]:
                queue_counts[q] += 1

        batch_summary = {
            "pilot_review_batch": min(24, supported),
            "donor_family_template_batch": min(96, supported),
            "mixed_pressure_batch": min(240, supported),
            "full_corpus_orchestrated_run": supported,
        }

        report_md.write_text(
            "\n".join([
                "# Full Corpus Dry-Run Report",
                "",
                "This is preflight planning metadata only.",
                "Extraction truth is not conversion permission.",
                "Conversion permission is not canon permission.",
                "",
                f"Files discovered: {len(all_files)}",
                f"Supported files: {supported}",
                f"Unsupported files: {unsupported}",
                f"Total bytes: {total_bytes}",
                f"Issues: {len(issues)}",
                "",
                "## Proposed batch summary",
                json.dumps(batch_summary, indent=2),
            ]),
            encoding="utf-8",
        )
        output_files.append(str(report_md))

        if strict and dup_hash_groups > 100:
            errors.append("duplicate_content_hash_threshold_exceeded")

        warnings.extend([f"issue:{i['issue_code']}:{i['path']}" for i in issues])

        result = {
            "valid": len(errors) == 0,
            "strict": strict,
            "corpus_dir": str(corpus),
            "output_dir": str(outdir),
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "files_discovered": len(all_files),
            "supported_files": supported,
            "unsupported_files": unsupported,
            "total_bytes": total_bytes,
            "issue_count": len(issues),
            "warning_count": len(warnings),
            "error_count": len(errors),
            "donor_family_estimate_counts": dict(fam_counts),
            "repair_queue_estimate_counts": dict(queue_counts),
            "output_files": output_files,
            "errors": errors,
            "warnings": warnings,
            "summary": {
                "batch_plan": batch_summary,
                "routing_metadata_note": "Filename-based donor-family and repair-queue estimates are weak preflight routing metadata only.",
                "no_extraction_note": "Dry-run planner does not extract, OCR, convert, or canonize.",
            },
        }

    except Exception as exc:
        result = {
            "valid": False,
            "strict": strict,
            "corpus_dir": str(corpus),
            "output_dir": str(outdir),
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "files_discovered": 0,
            "supported_files": 0,
            "unsupported_files": 0,
            "total_bytes": 0,
            "issue_count": 0,
            "warning_count": 0,
            "error_count": 1,
            "donor_family_estimate_counts": {},
            "repair_queue_estimate_counts": {},
            "output_files": output_files,
            "errors": [f"unexpected_exception:{exc}"],
            "warnings": warnings,
            "summary": {},
        }

    payload = json.dumps(result, indent=2, ensure_ascii=True)
    print(payload)
    if args.output_json:
        Path(args.output_json).write_text(payload + "\n", encoding="utf-8")

    if strict and not result["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()

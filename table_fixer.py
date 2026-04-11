#!/usr/bin/env python3
"""Post-extraction table fixer with structure-first recovery order."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from table_model import TableCell, TableRow, TableSidecar
from table_renderer import render_table
from gridless_tables import detect_gridless_rows, extract_gridless_table
from vector_table_extractor import extract_vector_tables

try:
    import fitz
except Exception:  # pragma: no cover
    fitz = None  # type: ignore


@dataclass
class FixStats:
    file: str
    tables_seen: int
    tables_fixed: int
    separators_added: int
    rows_padded: int
    pseudo_tables_promoted: int


def normalize_cell(cell: str) -> str:
    cell = cell.strip()
    dice_pattern = re.compile(r"(\d+d\d+)\|(\d+d\d+)")
    preserved: dict[str, str] = {}
    for i, match in enumerate(dice_pattern.finditer(cell)):
        key = f"__DICE{i}__"
        preserved[key] = match.group(0)
        cell = cell.replace(match.group(0), key)
    cell = cell.replace("\\|", "|")
    cell = cell.replace("|", "\\|")
    for key, original in preserved.items():
        cell = cell.replace(key, original)
    return cell


def split_pipe_row(row: str) -> list[str]:
    row = row.strip()
    if not row.startswith("|"):
        row = "| " + row
    if not row.endswith("|"):
        row = row + " |"
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for ch in row:
        if escaped:
            current.append(ch)
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            current.append(ch)
            continue
        if ch == "|":
            cells.append("".join(current))
            current = []
            continue
        current.append(ch)
    cells.append("".join(current))
    core = cells[1:-1]
    return [normalize_cell(c) for c in core]


def render_pipe_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def is_divider(row: str) -> bool:
    return bool(re.fullmatch(r"\|\s*[:\-]+(?:\s*\|\s*[:\-]+)*\s*\|", row.strip()))


def is_tableish_line(line: str) -> bool:
    return line.count("|") >= 2


def detect_pseudo_table_line(line: str) -> bool:
    if "|" in line or line.strip().startswith("```"):
        return False
    return bool(re.search(r"\S\s{3,}\S", line)) and len(re.split(r"\s{3,}", line.strip())) >= 2


def detect_pseudo_table_block(lines: list[str], start: int) -> int:
    count = 0
    gap_positions: list[int] | None = None
    for i in range(start, len(lines)):
        gaps = [m.start() for m in re.finditer(r"\s{3,}", lines[i])]
        if len(gaps) < 2:
            break
        if gap_positions is None:
            gap_positions = gaps
        elif not any(abs(g1 - g2) < 4 for g1 in gaps for g2 in gap_positions):
            break
        count += 1
    return count if count >= 3 else 0


def pseudo_to_pipe(line: str) -> str:
    parts = re.split(r"\s{2,}", line.strip())
    return render_pipe_row([normalize_cell(p) for p in parts if p.strip()])


def infer_divider_from_data(cells: list[str]) -> str:
    inferred = []
    for cell in cells:
        token = cell.strip().replace(",", "")
        inferred.append("---:" if re.fullmatch(r"[-+]?\d+(\.\d+)?|[xX✓✗]", token) else "---")
    return "| " + " | ".join(inferred) + " |"


def normalize_table_block(lines: list[str]) -> tuple[list[str], dict[str, int]]:
    stats = {"fixed": 0, "separator_added": 0, "rows_padded": 0}
    parsed = [split_pipe_row(x) for x in lines if x.strip()]
    if not parsed:
        return lines, stats
    width = max(len(r) for r in parsed)
    if width == 0:
        return lines, stats

    normalized_rows = []
    for row in parsed:
        if len(row) < width:
            row = row + [""] * (width - len(row))
            stats["rows_padded"] += 1
        normalized_rows.append(render_pipe_row(row))

    if not any(is_divider(r) for r in normalized_rows):
        candidate_cells = split_pipe_row(normalized_rows[1]) if len(normalized_rows) > 1 else [""] * width
        normalized_rows.insert(1, infer_divider_from_data(candidate_cells))
        stats["separator_added"] += 1

    if stats["rows_padded"] > 0 or stats["separator_added"] > 0:
        stats["fixed"] = 1
    return normalized_rows, stats


def collect_table_blocks(markdown: str) -> tuple[list[tuple[int, int, list[str]]], int]:
    lines = markdown.splitlines()
    blocks: list[tuple[int, int, list[str]]] = []
    i = 0
    promoted = 0
    while i < len(lines):
        if lines[i].strip().startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                i += 1
            i += 1
            continue
        pseudo_span = detect_pseudo_table_block(lines, i)
        if is_tableish_line(lines[i]) or pseudo_span > 0:
            start = i
            chunk: list[str] = []
            while i < len(lines) and (is_tableish_line(lines[i]) or (pseudo_span > 0 and i < start + pseudo_span)):
                if detect_pseudo_table_line(lines[i]):
                    chunk.append(pseudo_to_pipe(lines[i]))
                    promoted += 1
                else:
                    chunk.append(lines[i])
                i += 1
            if len(chunk) >= 2:
                blocks.append((start, i, chunk))
            continue
        i += 1
    return blocks, promoted


def stitch_cross_page_table_prefixes(markdown: str) -> str:
    return markdown


def apply_fixes(markdown: str) -> tuple[str, dict[str, int]]:
    lines = markdown.splitlines()
    blocks, promoted = collect_table_blocks(markdown)
    total_tables = len(blocks)
    tables_fixed = separators = padded = 0
    offset = 0
    for start, end, block in blocks:
        fixed, st = normalize_table_block(block)
        tables_fixed += st["fixed"]
        separators += st["separator_added"]
        padded += st["rows_padded"]
        real_start = start + offset
        real_end = end + offset
        lines[real_start:real_end] = fixed
        offset += len(fixed) - (end - start)
    return "\n".join(lines), {
        "tables_seen": total_tables,
        "tables_fixed": tables_fixed,
        "separators_added": separators,
        "rows_padded": padded,
        "pseudo_tables_promoted": promoted,
    }


def _table_from_markdown_block(block: list[str], page_num: int | None) -> TableSidecar | None:
    fixed, _ = normalize_table_block(block)
    rows: list[TableRow] = []
    for ln in fixed:
        if ln.count("|") < 2 or is_divider(ln):
            continue
        rows.append(TableRow(cells=[TableCell(text=c) for c in split_pipe_row(ln)]))
    if not rows:
        return None
    return TableSidecar(page=page_num, bbox=None, rows=rows, confidence=0.7)


def _serialize_sidecar(table: TableSidecar, strategy: str) -> dict[str, Any]:
    rendered = render_table(table)
    complex_mode = table.render_mode == "html"
    return {
        "page": table.page,
        "strategy": strategy,
        "render_mode": table.render_mode,
        "rendered": rendered,
        "markdown": rendered if table.render_mode == "markdown" else "",
        "sidecar_written": bool(complex_mode or table.sidecar_required),
        "degraded": table.degraded,
        "degraded_reason": table.degraded_reason,
        "model": table.to_dict(),
    }


def build_table_sidecars(markdown: str) -> list[dict]:
    return build_table_sidecars_with_context(markdown, source_pdf=None)


def build_table_sidecars_with_context(markdown: str, source_pdf: Path | None) -> list[dict]:
    marker_re = re.compile(r"\s*<!--\s*PAGE:(\d+)\s*-->")
    pages: list[tuple[int | None, str]] = []
    if marker_re.search(markdown):
        current: int | None = None
        buckets: dict[int, list[str]] = {}
        for line in markdown.splitlines():
            m = marker_re.match(line.strip())
            if m:
                current = int(m.group(1))
                buckets.setdefault(current, [])
                continue
            if current is not None:
                buckets.setdefault(current, []).append(line)
        pages = [(p, "\n".join(lines)) for p, lines in sorted(buckets.items())]
    else:
        pages = [(None, markdown)]

    vector_pages: dict[int, list[TableSidecar]] = {}
    if source_pdf is not None and fitz is not None and source_pdf.exists():
        try:
            with fitz.open(source_pdf) as doc:  # type: ignore[arg-type]
                for pidx in range(len(doc)):
                    vector_pages[pidx + 1] = extract_vector_tables(doc[pidx], page_num=pidx + 1)
        except Exception:
            vector_pages = {}

    sidecars: list[dict] = []
    for page_num, page_md in pages:
        # 1) Vector extraction first
        vector_models = vector_pages.get(page_num or -1, []) if page_num else []
        if vector_models:
            for table in vector_models:
                if table.confidence < 0.45:
                    table.degraded = True
                    table.degraded_reason = "low_vector_confidence"
                    table.render_mode = "html"
                    table.sidecar_required = True
                sidecars.append(_serialize_sidecar(table, strategy="vector"))
            continue

        # 2) Gridless recovery second
        grid = extract_gridless_table(page_md, page_num=page_num)
        if grid is not None:
            if grid.confidence < 0.6:
                grid.degraded = True
                grid.degraded_reason = "weak_grid_alignment"
                grid.sidecar_required = True
            sidecars.append(_serialize_sidecar(grid, strategy="gridless"))
            continue

        # 3) Markdown cleanup fallback
        blocks, _ = collect_table_blocks(page_md)
        for _, _, block in blocks:
            table = _table_from_markdown_block(block, page_num=page_num)
            if table is None:
                continue
            sidecars.append(_serialize_sidecar(table, strategy="markdown"))

    return sidecars


def process_file(path: Path, in_place: bool, output_dir: Path | None) -> FixStats:
    source = path.read_text(encoding="utf-8", errors="replace")
    fixed, stats = apply_fixes(source)
    sidecars = build_table_sidecars(fixed)

    if in_place:
        path.write_text(fixed, encoding="utf-8")
    else:
        assert output_dir is not None
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / path.name).write_text(fixed, encoding="utf-8")
    if sidecars:
        sidecar_out = (path.parent if in_place else (output_dir or path.parent)) / f"{path.stem}.tables.sidecar.json"
        sidecar_out.write_text(json.dumps(sidecars, indent=2, ensure_ascii=False), encoding="utf-8")

    return FixStats(file=str(path), **stats)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fix broken markdown tables")
    parser.add_argument("--input", required=True, help="Markdown file or directory")
    parser.add_argument("--glob", default="**/*.md")
    parser.add_argument("--in_place", action="store_true")
    parser.add_argument("--output_dir", default="")
    parser.add_argument("--report", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    inp = Path(args.input)
    targets = [inp] if inp.is_file() else [p for p in sorted(inp.glob(args.glob)) if p.is_file()]

    out_dir = Path(args.output_dir) if args.output_dir else None
    stats = [process_file(path, in_place=args.in_place, output_dir=out_dir) for path in targets]

    summary = {
        "files": len(stats),
        "tables_seen": sum(s.tables_seen for s in stats),
        "tables_fixed": sum(s.tables_fixed for s in stats),
        "separators_added": sum(s.separators_added for s in stats),
        "rows_padded": sum(s.rows_padded for s in stats),
        "pseudo_tables_promoted": sum(s.pseudo_tables_promoted for s in stats),
    }
    payload = {"summary": summary, "files": [asdict(s) for s in stats]}
    if args.report:
        report = Path(args.report)
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

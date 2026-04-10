#!/usr/bin/env python3
"""
Post-extraction table fixer for Aether Forge.

Targets common markdown table corruption patterns:
- missing separator rows
- inconsistent pipe counts
- unescaped pipes inside cells
- pseudo-tables represented by padded whitespace columns
- trailing/leading pipe normalization
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from table_model import TableCell, TableRow, TableSidecar
from table_renderer import render_table


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


def divider_row(width: int) -> str:
    return "| " + " | ".join(["---"] * width) + " |"


def is_divider(row: str) -> bool:
    return bool(re.fullmatch(r"\|\s*[:\-]+(?:\s*\|\s*[:\-]+)*\s*\|", row.strip()))


def is_tableish_line(line: str) -> bool:
    return line.count("|") >= 2


def detect_pseudo_table_line(line: str) -> bool:
    if "|" in line:
        return False
    if line.strip().startswith("```"):
        return False
    # multiple wide gaps likely columnar content
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
        if re.fullmatch(r"[-+]?\d+(\.\d+)?|[xX✓✗]", token):
            inferred.append("---:")
        else:
            inferred.append("---")
    return "| " + " | ".join(inferred) + " |"


def normalize_table_block(lines: list[str]) -> tuple[list[str], dict[str, int]]:
    stats = {
        "fixed": 0,
        "separator_added": 0,
        "rows_padded": 0,
    }

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

    has_divider = any(is_divider(r) for r in normalized_rows)
    if not has_divider:
        candidate_cells = split_pipe_row(normalized_rows[1]) if len(normalized_rows) > 1 else [""] * width
        normalized_rows.insert(1, infer_divider_from_data(candidate_cells))
        stats["separator_added"] += 1

    if stats["rows_padded"] > 0 or stats["separator_added"] > 0:
        stats["fixed"] = 1

    return normalized_rows, stats


def collect_table_blocks(markdown: str) -> tuple[list[tuple[int, int, list[str]]], int]:
    lines = markdown.splitlines()
    blocks = []
    i = 0
    promoted = 0

    while i < len(lines):
        if lines[i].strip().startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                i += 1
            i += 1
            continue
        line = lines[i]
        pseudo_span = detect_pseudo_table_block(lines, i)
        if is_tableish_line(line) or pseudo_span > 0:
            start = i
            chunk = []
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
    page_pat = re.compile(r"^\s*<!--\s*PAGE:(\d+)\s*-->\s*$")
    lines = markdown.splitlines()
    if not any(page_pat.match(line) for line in lines):
        return markdown

    pages: list[tuple[int, list[str]]] = []
    prefix: list[str] = []
    current_page: int | None = None
    current_body: list[str] = []
    for line in lines:
        marker = page_pat.match(line)
        if marker:
            if current_page is not None:
                pages.append((current_page, current_body))
            else:
                prefix = current_body
            current_page = int(marker.group(1))
            current_body = []
            continue
        current_body.append(line)
    if current_page is None:
        return markdown
    pages.append((current_page, current_body))

    for idx in range(1, len(pages)):
        prev_page, prev_body = pages[idx - 1]
        _, next_body = pages[idx]
        prev_non_empty = [line for line in prev_body if line.strip()]
        if not prev_non_empty or not (is_tableish_line(prev_non_empty[-1]) or detect_pseudo_table_line(prev_non_empty[-1])):
            continue

        scan = 0
        while scan < len(next_body) and not next_body[scan].strip():
            scan += 1

        consume = 0
        moved: list[str] = []
        while scan + consume < len(next_body):
            candidate = next_body[scan + consume]
            if not candidate.strip():
                break
            if not (is_tableish_line(candidate) or detect_pseudo_table_line(candidate)):
                break
            moved.append(pseudo_to_pipe(candidate) if detect_pseudo_table_line(candidate) else candidate)
            consume += 1

        if not moved:
            continue

        if moved and not any(is_divider(m) for m in moved):
            prev_table_lines = [line for line in prev_body if is_tableish_line(line)]
            if len(prev_table_lines) >= 2 and is_divider(prev_table_lines[1]):
                moved = [prev_table_lines[0], prev_table_lines[1]] + moved

        if prev_body and prev_body[-1].strip():
            prev_body.append("")
        prev_body.extend(moved)
        del next_body[scan : scan + consume]

    rebuilt: list[str] = []
    rebuilt.extend(prefix)
    for page_num, body in pages:
        rebuilt.append(f"<!-- PAGE:{page_num} -->")
        rebuilt.extend(body)
    return "\n".join(rebuilt)


def apply_fixes(markdown: str) -> tuple[str, dict[str, int]]:
    stitched = stitch_cross_page_table_prefixes(markdown)
    lines = stitched.splitlines()
    blocks, promoted = collect_table_blocks(stitched)

    total_tables = len(blocks)
    tables_fixed = 0
    separators = 0
    padded = 0

    offset = 0
    for start, end, block in blocks:
        fixed, st = normalize_table_block(block)
        if st["fixed"]:
            tables_fixed += 1
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


def build_table_sidecars(markdown: str) -> list[dict]:
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

    sidecars: list[dict] = []
    for page_num, page_md in pages:
        blocks, _ = collect_table_blocks(page_md)
        for _, _, block in blocks:
            raw_rows = [ln for ln in block if ln.count("|") >= 2 and not is_divider(ln)]
            raw_widths = [len(split_pipe_row(ln)) for ln in raw_rows]
            fixed, _ = normalize_table_block(block)
            rows = []
            for ln in fixed:
                if ln.count("|") < 2 or is_divider(ln):
                    continue
                rows.append(TableRow(cells=[TableCell(text=c) for c in split_pipe_row(ln)]))
            if not rows:
                continue
            is_complex = (len(set(raw_widths)) > 1) or any(len(r.cells) != len(rows[0].cells) for r in rows) or len(rows[0].cells) > 8
            mode = "html" if is_complex else "markdown"
            side = TableSidecar(page=page_num, bbox=None, rows=rows, render_mode=mode, confidence=0.7)
            rendered = render_table(side)
            sidecars.append({
                "page": page_num,
                "render_mode": mode,
                "rendered": rendered,
                "markdown": rendered if mode == "markdown" else "",
                "model": side.to_dict(),
            })
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
        out = output_dir / path.name
        out.write_text(fixed, encoding="utf-8")
    if sidecars:
        sidecar_out = (path.parent if in_place else (output_dir or path.parent)) / f"{path.stem}.tables.sidecar.json"
        sidecar_out.write_text(json.dumps(sidecars, indent=2, ensure_ascii=False), encoding="utf-8")

    return FixStats(
        file=str(path),
        tables_seen=stats["tables_seen"],
        tables_fixed=stats["tables_fixed"],
        separators_added=stats["separators_added"],
        rows_padded=stats["rows_padded"],
        pseudo_tables_promoted=stats["pseudo_tables_promoted"],
    )


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

    targets = []
    if inp.is_file():
        targets = [inp]
    else:
        targets = [p for p in sorted(inp.glob(args.glob)) if p.is_file()]

    out_dir = Path(args.output_dir) if args.output_dir else None
    stats = []
    for path in targets:
        stats.append(process_file(path, in_place=args.in_place, output_dir=out_dir))

    summary = {
        "files": len(stats),
        "tables_seen": sum(s.tables_seen for s in stats),
        "tables_fixed": sum(s.tables_fixed for s in stats),
        "separators_added": sum(s.separators_added for s in stats),
        "rows_padded": sum(s.rows_padded for s in stats),
        "pseudo_tables_promoted": sum(s.pseudo_tables_promoted for s in stats),
    }

    payload = {
        "summary": summary,
        "files": [asdict(s) for s in stats],
    }

    if args.report:
        report = Path(args.report)
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

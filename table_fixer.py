#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

PAGE_RE = re.compile(r"\s*<!--\s*PAGE:(\d+)\s*-->")


@dataclass
class FixStats:
    file: str
    tables_seen: int
    tables_fixed: int
    separators_added: int
    rows_padded: int
    pseudo_tables_promoted: int
    stitched_events: int
    html_sidecars: int


def normalize_cell(cell: str) -> str:
    return cell.strip().replace("\\|", "|").replace("|", "\\|")


def split_pipe_row(row: str) -> list[str]:
    row = row.strip()
    if not row.startswith("|"):
        row = "| " + row
    if not row.endswith("|"):
        row = row + " |"
    return [normalize_cell(p) for p in row.split("|")[1:-1]]


def render_pipe_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def divider_row(width: int) -> str:
    return "| " + " | ".join(["---"] * width) + " |"


def is_divider(row: str) -> bool:
    return bool(re.fullmatch(r"\|\s*[:\-]+(?:\s*\|\s*[:\-]+)*\s*\|", row.strip()))


def is_tableish_line(line: str) -> bool:
    return line.count("|") >= 2


def detect_pseudo_table_line(line: str) -> bool:
    if "|" in line or not line.strip() or line.strip().startswith(("- ", "* ", "#")):
        return False
    return bool(re.search(r"\S\s{2,}\S", line))


def pseudo_to_cells(line: str) -> list[str]:
    return [normalize_cell(p) for p in re.split(r"\s{2,}", line.strip()) if p.strip()]


def is_valid_pseudo_table(rows: list[list[str]]) -> bool:
    if len(rows) < 2:
        return False
    widths = [len(r) for r in rows]
    if max(widths) < 2:
        return False
    avg_len = sum(len(c) for r in rows for c in r) / max(1, sum(len(r) for r in rows))
    if avg_len < 1.0:
        return False
    numeric_only = sum(1 for r in rows if all(re.fullmatch(r"[\d\s\.,%+-]+", c or "") for c in r))
    return numeric_only < len(rows)


def stat_block_to_table(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    rows = []
    for line in lines:
        if ":" in line and not line.lstrip().startswith("#"):
            key, val = line.split(":", 1)
            if key.strip() and val.strip() and len(key) < 40:
                rows.append((key.strip(), val.strip()))
    if len(rows) < 3:
        return text, 0
    md_rows = ["| Attribute | Value |", "| --- | --- |"] + [f"| {normalize_cell(k)} | {normalize_cell(v)} |" for k, v in rows]
    return "\n".join(md_rows), 1


def normalize_table_block(lines: list[str]) -> tuple[list[str], dict[str, int]]:
    stats = {"fixed": 0, "separator_added": 0, "rows_padded": 0}
    parsed = [split_pipe_row(x) for x in lines if x.strip()]
    if not parsed:
        return lines, stats
    width = max(len(r) for r in parsed)
    out = []
    for row in parsed:
        if len(row) < width:
            row = row + [""] * (width - len(row))
            stats["rows_padded"] += 1
        out.append(render_pipe_row(row))
    if not any(is_divider(r) for r in out):
        out.insert(1, divider_row(width))
        stats["separator_added"] += 1
    stats["fixed"] = 1 if stats["rows_padded"] or stats["separator_added"] else 0
    return out, stats


def parse_pages(markdown: str) -> dict[int, list[str]]:
    pages: dict[int, list[str]] = {}
    cur = 1
    for line in markdown.splitlines():
        m = PAGE_RE.match(line)
        if m:
            cur = int(m.group(1))
            pages.setdefault(cur, [])
            continue
        pages.setdefault(cur, []).append(line)
    return pages


def stitch_tables_across_pages(pages: dict[int, list[str]]) -> tuple[dict[int, list[str]], list[dict[str, int]]]:
    events = []
    keys = sorted(pages)
    for idx, p in enumerate(keys[:-1]):
        q = keys[idx + 1]
        cur = [l for l in pages[p] if l.strip()]
        nxt = [l for l in pages[q] if l.strip()]
        if len(cur) < 2 or len(nxt) < 2:
            continue
        tail = [l for l in cur[-4:] if is_tableish_line(l)]
        head = [l for l in nxt[:6] if is_tableish_line(l)]
        if len(tail) < 2 or len(head) < 2:
            continue
        merged = cur + ["", "| (continued) |", "| --- |"] + head
        pages[p] = merged
        pages[q] = [l for l in pages[q] if l not in head]
        events.append({"from_page": p, "to_page": q, "rows_merged": len(head)})
    return pages, events


def collect_table_blocks(lines: list[str]) -> tuple[list[tuple[int, int, list[str]]], int]:
    blocks = []
    i = 0
    promoted = 0
    in_code = False
    while i < len(lines):
        if lines[i].strip().startswith("```"):
            in_code = not in_code
            i += 1
            continue
        line = lines[i]
        if not in_code and (is_tableish_line(line) or detect_pseudo_table_line(line)):
            start = i
            chunk: list[str] = []
            pseudo_rows: list[list[str]] = []
            while i < len(lines) and (is_tableish_line(lines[i]) or detect_pseudo_table_line(lines[i])):
                if detect_pseudo_table_line(lines[i]):
                    cells = pseudo_to_cells(lines[i])
                    pseudo_rows.append(cells)
                    chunk.append(render_pipe_row(cells))
                else:
                    chunk.append(lines[i])
                i += 1
            if pseudo_rows and not is_valid_pseudo_table(pseudo_rows):
                continue
            if len(chunk) >= 2:
                promoted += len(pseudo_rows)
                blocks.append((start, i, chunk))
            continue
        i += 1
    return blocks, promoted


def apply_fixes_detailed(markdown: str) -> tuple[str, dict[str, int], list[dict[str, int]], list[str]]:
    html_sidecars: list[str] = []
    st_md, converted = stat_block_to_table(markdown)
    stitch_events = []
    if "<!-- PAGE:" in st_md:
        pages = parse_pages(st_md)
        pages, stitch_events = stitch_tables_across_pages(pages)
        lines = []
        for p in sorted(pages):
            lines.append(f"<!-- PAGE:{p} -->")
            lines.extend(pages[p])
        lines2 = lines[:]
    else:
        lines2 = st_md.splitlines()

    blocks, promoted = collect_table_blocks(lines2)
    total_tables = len(blocks)
    fixed_tables = separators = padded = 0
    offset = 0
    for start, end, block in blocks:
        fixed, st = normalize_table_block(block)
        real_start, real_end = start + offset, end + offset
        lines2[real_start:real_end] = fixed
        offset += len(fixed) - (end - start)
        fixed_tables += st["fixed"]
        separators += st["separator_added"]
        padded += st["rows_padded"]
        if any("<table" in r.lower() for r in block):
            html_sidecars.append("\n".join(block))

    return "\n".join(lines2), {
        "tables_seen": total_tables,
        "tables_fixed": fixed_tables,
        "separators_added": separators,
        "rows_padded": padded,
        "pseudo_tables_promoted": promoted + converted,
        "stitched_events": len(stitch_events),
        "html_sidecars": len(html_sidecars),
    }, stitch_events, html_sidecars



def apply_fixes(markdown: str) -> tuple[str, dict[str, int]]:
    fixed, stats, _events, _html = apply_fixes_detailed(markdown)
    return fixed, stats

def process_file(path: Path, in_place: bool, output_dir: Path | None, sidecar_dir: Path | None) -> FixStats:
    source = path.read_text(encoding="utf-8", errors="replace")
    fixed, stats, stitch_events, html_sidecars = apply_fixes_detailed(source)

    out_path = path if in_place else (output_dir / path.name if output_dir else path)
    if out_path != path:
        assert output_dir is not None
        output_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(fixed, encoding="utf-8")

    if sidecar_dir:
        sidecar_dir.mkdir(parents=True, exist_ok=True)
        (sidecar_dir / f"{path.stem}.stitch.json").write_text(json.dumps(stitch_events, indent=2), encoding="utf-8")
        if html_sidecars:
            (sidecar_dir / f"{path.stem}.tables.html.json").write_text(json.dumps(html_sidecars, indent=2), encoding="utf-8")

    return FixStats(
        file=str(path),
        tables_seen=stats["tables_seen"],
        tables_fixed=stats["tables_fixed"],
        separators_added=stats["separators_added"],
        rows_padded=stats["rows_padded"],
        pseudo_tables_promoted=stats["pseudo_tables_promoted"],
        stitched_events=stats["stitched_events"],
        html_sidecars=stats["html_sidecars"],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fix broken markdown tables")
    parser.add_argument("--input", required=True)
    parser.add_argument("--glob", default="**/*.md")
    parser.add_argument("--in_place", action="store_true")
    parser.add_argument("--output_dir", default="")
    parser.add_argument("--sidecar_dir", default="")
    parser.add_argument("--report", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    inp = Path(args.input)
    targets = [inp] if inp.is_file() else [p for p in sorted(inp.glob(args.glob)) if p.is_file()]
    out_dir = Path(args.output_dir) if args.output_dir else None
    sidecar_dir = Path(args.sidecar_dir) if args.sidecar_dir else None

    stats = [process_file(path, args.in_place, out_dir, sidecar_dir) for path in targets]
    payload = {
        "summary": {
            "files": len(stats),
            "tables_seen": sum(s.tables_seen for s in stats),
            "tables_fixed": sum(s.tables_fixed for s in stats),
            "separators_added": sum(s.separators_added for s in stats),
            "rows_padded": sum(s.rows_padded for s in stats),
            "pseudo_tables_promoted": sum(s.pseudo_tables_promoted for s in stats),
            "stitched_events": sum(s.stitched_events for s in stats),
            "html_sidecars": sum(s.html_sidecars for s in stats),
        },
        "files": [asdict(s) for s in stats],
    }
    if args.report:
        Path(args.report).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

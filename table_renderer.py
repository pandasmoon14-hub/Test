#!/usr/bin/env python3
"""Render structured tables to markdown or html."""
from __future__ import annotations
from html import escape
from table_model import TableSidecar

def _esc_pipe(v: str) -> str:
    return v.replace("\\|", "|").replace("|", "\\|")

def render_markdown(table: TableSidecar) -> str:
    rows = table.rows
    if not rows:
        return ""
    grid = [[_esc_pipe(c.text) for c in r.cells] for r in rows]
    width = max(len(r) for r in grid)
    for r in grid:
        if len(r) < width:
            r.extend([""] * (width - len(r)))
    out = ["| " + " | ".join(grid[0]) + " |", "| " + " | ".join(["---"] * width) + " |"]
    for r in grid[1:]:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)

def render_html(table: TableSidecar) -> str:
    lines = ["<table>"]
    for row in table.rows:
        lines.append("  <tr>")
        for cell in row.cells:
            attrs = ""
            if cell.colspan > 1:
                attrs += f' colspan="{cell.colspan}"'
            if cell.rowspan > 1:
                attrs += f' rowspan="{cell.rowspan}"'
            lines.append(f"    <td{attrs}>{escape(cell.text)}</td>")
        lines.append("  </tr>")
    lines.append("</table>")
    return "\n".join(lines)

def render_table(table: TableSidecar) -> str:
    return render_html(table) if table.render_mode == "html" else render_markdown(table)

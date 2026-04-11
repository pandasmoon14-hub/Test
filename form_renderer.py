#!/usr/bin/env python3
"""Structured renderer for form/worksheet-like pages."""
from __future__ import annotations

from dataclasses import dataclass, field
import re


@dataclass
class FormField:
    label: str
    value: str = ""
    placeholder: str | None = None


@dataclass
class FormRow:
    fields: list[FormField] = field(default_factory=list)


@dataclass
class FormSection:
    title: str
    rows: list[FormRow] = field(default_factory=list)


@dataclass
class FormDocument:
    sections: list[FormSection] = field(default_factory=list)


def _split_columns(line: str) -> list[str]:
    if "|" in line:
        return [part.strip() for part in line.split("|") if part.strip()]
    return [part.strip() for part in re.split(r"\s{2,}", line) if part.strip()]


def _parse_field(token: str) -> FormField:
    m = re.match(r"^(?P<label>[^:]{1,80}):\s*(?P<value>.*)$", token)
    if m:
        label = m.group("label").strip()
        value = m.group("value").strip()
        placeholder = "____" if re.search(r"_{3,}", value) else None
        return FormField(label=label, value=value, placeholder=placeholder)
    placeholder = "____" if re.search(r"_{3,}", token) else None
    return FormField(label=token.strip(), value="", placeholder=placeholder)


def build_form_document(text: str) -> FormDocument:
    sections: list[FormSection] = []
    current = FormSection(title="Form")
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            if current.rows:
                sections.append(current)
                current = FormSection(title="Section")
            continue
        if re.match(r"^(#+\s+|[A-Z][A-Za-z0-9 /&'-]{2,}:?$)", line.strip()) and not re.search(r"\s{2,}", line):
            if current.rows:
                sections.append(current)
            current = FormSection(title=line.strip().lstrip("#").strip().rstrip(":"))
            continue
        cols = _split_columns(line)
        fields = [_parse_field(col) for col in cols]
        if fields:
            current.rows.append(FormRow(fields=fields))
    if current.rows:
        sections.append(current)
    return FormDocument(sections=sections or [FormSection(title="Form", rows=[])])


def render_form_like(text: str) -> str:
    """Render form-like text to structure-preserving HTML."""
    doc = build_form_document(text)
    lines: list[str] = ["<form data-preservation=\"structured\">"]
    for section in doc.sections:
        lines.append(f"  <section data-form-section=\"{section.title}\">")
        lines.append(f"    <h3>{section.title}</h3>")
        lines.append("    <table>")
        for row in section.rows:
            lines.append("      <tr>")
            for field in row.fields:
                placeholder = field.placeholder or ("____" if field.value.strip(" _") == "" else "")
                rendered = field.value if field.value else placeholder
                lines.append(
                    f"        <td><strong>{field.label}</strong><br/><span data-blank=\"{'1' if placeholder else '0'}\">{rendered}</span></td>"
                )
            lines.append("      </tr>")
        lines.append("    </table>")
        lines.append("  </section>")
    lines.append("</form>")
    return "\n".join(lines)

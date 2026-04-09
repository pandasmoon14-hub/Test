#!/usr/bin/env python3
"""
Lorebook splitter v11 for post-ingestion markdown.

Enhancements:
- supports ATX + Setext headings
- page-tag awareness from <!-- PAGE:n --> markers
- stronger table parsing (not only pipe lines)
- broader system-agnostic mechanics detection
- chunk JSON validation before output
"""

from __future__ import annotations

import argparse
import json
import re
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

from mechanics_vocab import mechanics_hits, statblock_density


@dataclass
class ChunkRecord:
    entry_id: str
    book_id: str
    chapter_path: str
    tags: list[str]
    aliases: list[str]
    raw_markdown: str
    embedding_text: str
    source_pages: list[int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Split markdown books into lorebook chunks")
    parser.add_argument("--input_root", required=True)
    parser.add_argument("--output_jsonl", required=True)
    parser.add_argument("--glob", default="**/*.md")
    parser.add_argument("--min_chunk_chars", type=int, default=160)
    parser.add_argument("--max_chunk_chars", type=int, default=4500)
    parser.add_argument("--ttrpg_mode", action="store_true")
    return parser.parse_args()


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\xad", "")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_page_markers(markdown: str) -> dict[int, str]:
    pages, cur = {}, 1
    marker_re = re.compile(r"\s*<!--\s*page\s*[:\s]?\s*(\d+)\s*-->", flags=re.IGNORECASE)
    for line in markdown.splitlines():
        m = marker_re.match(line)
        if m:
            cur = int(m.group(1))
            pages.setdefault(cur, [])
            continue
        pages.setdefault(cur, []).append(line)
    return {k: "\n".join(v).strip() for k, v in pages.items()}


def extract_headings(lines: list[str]) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if m:
            out.append((i, f"{m.group(1)} {m.group(2).strip()}"))
            continue
        if i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            if re.fullmatch(r"=+", nxt):
                out.append((i, f"# {line.strip()}"))
            elif re.fullmatch(r"-+", nxt):
                out.append((i, f"## {line.strip()}"))
    return out


def split_sections(markdown: str) -> list[tuple[str, str, list[int]]]:
    pages = parse_page_markers(markdown)
    flat_lines = []
    line_pages = []
    for p in sorted(pages):
        for line in pages[p].splitlines():
            flat_lines.append(line)
            line_pages.append(p)

    headings = extract_headings(flat_lines)
    if not headings:
        return [("# Document", normalize_whitespace(markdown), sorted(set(line_pages)))]

    sections = []
    for idx, (start, heading) in enumerate(headings):
        end = headings[idx + 1][0] if idx + 1 < len(headings) else len(flat_lines)
        body = normalize_whitespace("\n".join(flat_lines[start + 1:end]))
        pages_here = sorted(set(line_pages[start:end]))
        if body:
            sections.append((heading, body, pages_here))
    return sections


def detect_table_blocks(text: str) -> list[str]:
    lines = text.splitlines()
    blocks, cur = [], []
    for line in lines:
        is_tableish = line.count("|") >= 2 or bool(re.search(r"\b\d+\s{2,}\d+\b", line))
        if is_tableish:
            cur.append(line)
        else:
            if len(cur) >= 2:
                blocks.append("\n".join(cur))
            cur = []
    if len(cur) >= 2:
        blocks.append("\n".join(cur))
    return [normalize_whitespace(b) for b in blocks if len(b.strip()) > 20]


def detect_rule_like_blocks(text: str, ttrpg_mode: bool) -> list[str]:
    generic_regex = re.compile(r"\b(dc\s*\d+|target number|difficulty|cooldown|resource|actions?|reaction|roll table|initiative)\b", flags=re.IGNORECASE)
    out = []
    for para in text.split("\n\n"):
        p = para.strip()
        if not p:
            continue
        vocab_hits = sum(mechanics_hits(p).values())
        if generic_regex.search(p) or vocab_hits >= (1 if ttrpg_mode else 2) or statblock_density(p) >= 0.22:
            out.append(p)
    return out


def detect_lore_like_blocks(text: str) -> list[str]:
    regex = re.compile(r"\b(kingdom|empire|city|faction|guild|order|prophecy|war|calendar|lineage|god|deity|planet|sector|domain)\b", flags=re.IGNORECASE)
    return [p.strip() for p in text.split("\n\n") if p.strip() and regex.search(p)]


def extract_entities(markdown: str) -> dict[str, set[str]]:
    entities = {"npc": set(), "location": set(), "item": set(), "spell": set(), "faction": set()}
    patterns = {
        "npc": r"\b(?:Sir|Lady|Lord|Captain|Master|Archmage|Doctor|Commander)\s+([A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)*)",
        "location": r"\b(?:City of|Kingdom of|Ruins of|Mount|Lake|Forest of|Planet|Sector)\s+([A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)*)",
        "item": r"\b([A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)*)\s+(?:Sword|Shield|Amulet|Ring|Staff|Blade|Relic|Artifact)\b",
        "spell": r"\b(?:Spell:|Ritual:|Cantrip:|Invocation:)\s*([A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)*)",
        "faction": r"\b(?:Order of|Guild of|Circle of|House|Legion of)\s+([A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)*)",
    }
    for k, pat in patterns.items():
        for m in re.findall(pat, markdown):
            entities[k].add(re.sub(r"\s+", " ", m.strip()))
    return entities


def chunk_large_text(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    out, cur, n = [], [], 0
    for p in [x for x in text.split("\n\n") if x.strip()]:
        if cur and n + len(p) + 2 > max_chars:
            out.append("\n\n".join(cur))
            cur, n = [p], len(p)
        else:
            cur.append(p)
            n += len(p) + 2
    if cur:
        out.append("\n\n".join(cur))
    return out


def make_embedding_text(book_id: str, chapter_path: str, tags: list[str], body: str, pages: list[int]) -> str:
    compact = re.sub(r"\s+", " ", body).strip()
    summary = compact[:1200]
    return f"book_id={book_id}\nchapter_path={chapter_path}\ntags={','.join(tags)}\npages={','.join(map(str,pages))}\nsummary={summary}"


def make_entry_id(book_id: str, kind: str, idx: int) -> str:
    seed = f"{book_id}:{kind}:{idx:05d}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def safe_chunk(record: ChunkRecord) -> ChunkRecord | None:
    try:
        json.loads(json.dumps(asdict(record), ensure_ascii=False))
    except Exception:
        return None
    return record


def build_chunks(md_path: Path, min_chars: int, max_chars: int, ttrpg_mode: bool) -> list[ChunkRecord]:
    markdown = normalize_whitespace(md_path.read_text(encoding="utf-8", errors="replace"))
    book_id = md_path.stem
    sections = split_sections(markdown)
    chunks, idx = [], 0

    meta = "\n".join([f"book_id: {book_id}", f"source_file: {md_path.name}", "edition: unknown", "system: ttrpg"])
    chunks.append(ChunkRecord(make_entry_id(book_id, "book_metadata", idx), book_id, "book_metadata", ["metadata"], [book_id], meta, make_embedding_text(book_id, "book_metadata", ["metadata"], meta, []), []))
    idx += 1

    for heading, body, pages in sections:
        chapter_path = heading.replace("#", "").strip()
        for part in chunk_large_text(body, max_chars):
            if len(part) < min_chars:
                continue
            tags = ["chapter"]
            if "limit tech" in part.lower():
                tags.append("tech_block")
            if "pc level" in part.lower():
                tags.append("class_template")
            chunks.append(ChunkRecord(make_entry_id(book_id, "chapter", idx), book_id, chapter_path, tags, [], part, make_embedding_text(book_id, chapter_path, tags, part, pages), pages))
            idx += 1

        for tb in detect_table_blocks(body):
            if len(tb) < min_chars:
                continue
            tags = ["mechanics", "table"]
            chunks.append(ChunkRecord(make_entry_id(book_id, "mechanics", idx), book_id, chapter_path, tags, [], tb, make_embedding_text(book_id, chapter_path, tags, tb, pages), pages))
            idx += 1

        for rb in detect_rule_like_blocks(body, ttrpg_mode=ttrpg_mode):
            if len(rb) < min_chars:
                continue
            tags = ["mechanics", "rules"]
            chunks.append(ChunkRecord(make_entry_id(book_id, "mechanics", idx), book_id, chapter_path, tags, [], rb, make_embedding_text(book_id, chapter_path, tags, rb, pages), pages))
            idx += 1

        for lb in detect_lore_like_blocks(body):
            if len(lb) < min_chars:
                continue
            tags = ["lore"]
            chunks.append(ChunkRecord(make_entry_id(book_id, "lore", idx), book_id, chapter_path, tags, [], lb, make_embedding_text(book_id, chapter_path, tags, lb, pages), pages))
            idx += 1

    entities = extract_entities(markdown)
    entity_lines, aliases = [], []
    for cat, vals in entities.items():
        if not vals:
            continue
        entity_lines.append(f"## {cat}\n")
        sorted_vals = sorted(vals)
        aliases.extend(sorted_vals)
        entity_lines.extend([f"- {v}" for v in sorted_vals])
        entity_lines.append("")
    if entity_lines:
        body = "\n".join(entity_lines).strip()
        chunks.append(ChunkRecord(make_entry_id(book_id, "entities", idx), book_id, "entities/index", ["entities", "index"], aliases, body, make_embedding_text(book_id, "entities/index", ["entities", "index"], body, []), []))

    safe = []
    for c in chunks:
        ok = safe_chunk(c)
        if ok is not None:
            safe.append(ok)
    return safe


def iter_markdown_files(root: Path, glob: str) -> Iterable[Path]:
    for path in sorted(root.glob(glob)):
        if path.is_file():
            yield path


def main() -> None:
    args = parse_args()
    in_root = Path(args.input_root)
    out = Path(args.output_jsonl)
    out.parent.mkdir(parents=True, exist_ok=True)

    all_books, all_chunks = 0, 0
    with open(out, "w", encoding="utf-8") as file:
        for md in iter_markdown_files(in_root, args.glob):
            chunks = build_chunks(md, args.min_chunk_chars, args.max_chunk_chars, ttrpg_mode=args.ttrpg_mode)
            for c in chunks:
                file.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")
            all_books += 1
            all_chunks += len(chunks)

    print(json.dumps({"status": "ok", "books": all_books, "chunks": all_chunks, "output_jsonl": str(out)}, indent=2))


if __name__ == "__main__":
    main()

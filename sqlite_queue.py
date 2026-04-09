#!/usr/bin/env python3
"""
SQLite-backed durable queue/state store for Aether Forge.

This module can replace JSON queue persistence for large corpus runs where
incremental updates, locking behavior, and recoverability matter.
"""

from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable


@dataclass
class QueueItem:
    book_id: str
    file: str
    failed_pages: list[int]
    md_path: str
    full_book_repair: bool
    queued_at: float
    updated_at: float
    audit_signatures: list[str]
    page_reasons: dict[str, list[str]]
    page_profiles: dict[str, dict[str, Any]]


SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;

CREATE TABLE IF NOT EXISTS repair_queue (
    book_id TEXT PRIMARY KEY,
    file TEXT NOT NULL,
    failed_pages TEXT NOT NULL,
    md_path TEXT NOT NULL,
    full_book_repair INTEGER NOT NULL,
    queued_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    audit_signatures TEXT NOT NULL,
    page_reasons TEXT NOT NULL,
    page_profiles TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS manifests (
    book_id TEXT PRIMARY KEY,
    payload TEXT NOT NULL,
    updated_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS run_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    book_id TEXT,
    payload TEXT NOT NULL,
    created_at REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_repair_updated ON repair_queue(updated_at);
CREATE INDEX IF NOT EXISTS idx_events_time ON run_events(created_at);
"""


class QueueDB:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA busy_timeout=5000")
        self.conn.executescript(SCHEMA)
        self.conn.commit()
        self._write_counter = 0

    def _maintenance_checkpoint(self) -> None:
        self._write_counter += 1
        if self._write_counter % 10 == 0:
            self.conn.execute("PRAGMA wal_checkpoint(PASSIVE)")

    def close(self) -> None:
        self.conn.execute("PRAGMA wal_checkpoint(FULL)")
        self.conn.execute("PRAGMA optimize")
        self.conn.commit()
        self.conn.close()

    def log_event(self, event_type: str, payload: dict[str, Any], book_id: str | None = None) -> None:
        self.conn.execute(
            "INSERT INTO run_events(event_type, book_id, payload, created_at) VALUES(?,?,?,?)",
            (event_type, book_id, json.dumps(payload, ensure_ascii=False), time.time()),
        )
        self._maintenance_checkpoint()
        self.conn.commit()

    def upsert_queue_item(self, item: QueueItem) -> None:
        self.conn.execute(
            """
            INSERT INTO repair_queue(
                book_id, file, failed_pages, md_path, full_book_repair,
                queued_at, updated_at, audit_signatures, page_reasons, page_profiles
            ) VALUES(?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(book_id) DO UPDATE SET
                file=excluded.file,
                failed_pages=excluded.failed_pages,
                md_path=excluded.md_path,
                full_book_repair=excluded.full_book_repair,
                updated_at=excluded.updated_at,
                audit_signatures=excluded.audit_signatures,
                page_reasons=excluded.page_reasons,
                page_profiles=excluded.page_profiles
            """,
            (
                item.book_id,
                item.file,
                json.dumps(item.failed_pages),
                item.md_path,
                1 if item.full_book_repair else 0,
                item.queued_at,
                item.updated_at,
                json.dumps(item.audit_signatures, ensure_ascii=False),
                json.dumps(item.page_reasons, ensure_ascii=False),
                json.dumps(item.page_profiles, ensure_ascii=False),
            ),
        )
        self.conn.commit()

    def get_queue_item(self, book_id: str) -> QueueItem | None:
        row = self.conn.execute("SELECT * FROM repair_queue WHERE book_id=?", (book_id,)).fetchone()
        if row is None:
            return None
        return QueueItem(
            book_id=row["book_id"],
            file=row["file"],
            failed_pages=json.loads(row["failed_pages"]),
            md_path=row["md_path"],
            full_book_repair=bool(row["full_book_repair"]),
            queued_at=float(row["queued_at"]),
            updated_at=float(row["updated_at"]),
            audit_signatures=json.loads(row["audit_signatures"]),
            page_reasons=json.loads(row["page_reasons"]),
            page_profiles=json.loads(row["page_profiles"]),
        )

    def list_queue(self, limit: int = 0) -> list[QueueItem]:
        query = "SELECT * FROM repair_queue ORDER BY updated_at ASC"
        params: tuple[Any, ...] = ()
        if limit > 0:
            query += " LIMIT ?"
            params = (limit,)
        rows = self.conn.execute(query, params).fetchall()
        return [
            QueueItem(
                book_id=r["book_id"],
                file=r["file"],
                failed_pages=json.loads(r["failed_pages"]),
                md_path=r["md_path"],
                full_book_repair=bool(r["full_book_repair"]),
                queued_at=float(r["queued_at"]),
                updated_at=float(r["updated_at"]),
                audit_signatures=json.loads(r["audit_signatures"]),
                page_reasons=json.loads(r["page_reasons"]),
                page_profiles=json.loads(r["page_profiles"]),
            )
            for r in rows
        ]

    def delete_queue_item(self, book_id: str) -> None:
        self.conn.execute("DELETE FROM repair_queue WHERE book_id=?", (book_id,))
        self.conn.commit()

    def update_failed_pages(self, book_id: str, failed_pages: list[int]) -> None:
        self.conn.execute(
            "UPDATE repair_queue SET failed_pages=?, updated_at=? WHERE book_id=?",
            (json.dumps(sorted(set(failed_pages))), time.time(), book_id),
        )
        self._maintenance_checkpoint()
        self.conn.commit()

    def save_manifest(self, book_id: str, payload: dict[str, Any]) -> None:
        self.conn.execute(
            """
            INSERT INTO manifests(book_id, payload, updated_at)
            VALUES(?,?,?)
            ON CONFLICT(book_id) DO UPDATE SET
                payload=excluded.payload,
                updated_at=excluded.updated_at
            """,
            (book_id, json.dumps(payload, ensure_ascii=False), time.time()),
        )
        self.conn.commit()

    def get_manifest(self, book_id: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT payload FROM manifests WHERE book_id=?", (book_id,)).fetchone()
        if row is None:
            return None
        return json.loads(row["payload"])

    def list_manifests(self) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT payload FROM manifests ORDER BY updated_at DESC").fetchall()
        return [json.loads(r["payload"]) for r in rows]

    def queue_size(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) AS n FROM repair_queue").fetchone()
        return int(row["n"]) if row else 0

    def pending_pages(self) -> int:
        rows = self.conn.execute("SELECT failed_pages FROM repair_queue").fetchall()
        total = 0
        for r in rows:
            total += len(json.loads(r["failed_pages"]))
        return total

    def purge_old_events(self, older_than_sec: float) -> int:
        cutoff = time.time() - older_than_sec
        cur = self.conn.execute("DELETE FROM run_events WHERE created_at < ?", (cutoff,))
        self.conn.commit()
        return int(cur.rowcount)

    def iter_events(self, event_type: str | None = None, limit: int = 500) -> Iterable[dict[str, Any]]:
        if event_type:
            rows = self.conn.execute(
                "SELECT * FROM run_events WHERE event_type=? ORDER BY id DESC LIMIT ?",
                (event_type, limit),
            ).fetchall()
        else:
            rows = self.conn.execute("SELECT * FROM run_events ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        for r in rows:
            yield {
                "id": int(r["id"]),
                "event_type": r["event_type"],
                "book_id": r["book_id"],
                "payload": json.loads(r["payload"]),
                "created_at": float(r["created_at"]),
            }


def queue_item_from_record(book_id: str, record: dict[str, Any]) -> QueueItem:
    now = time.time()
    return QueueItem(
        book_id=book_id,
        file=str(record.get("file", "")),
        failed_pages=list(record.get("failed_pages", [])),
        md_path=str(record.get("md_path", "")),
        full_book_repair=bool(record.get("full_book_repair", False)),
        queued_at=float(record.get("queued_at", now)),
        updated_at=float(record.get("updated_at", now)),
        audit_signatures=list(record.get("audit_signatures", [])),
        page_reasons=dict(record.get("page_reasons", {})),
        page_profiles=dict(record.get("page_profiles", {})),
    )


def export_json_queue(db: QueueDB) -> dict[str, Any]:
    out = {}
    for item in db.list_queue():
        out[item.book_id] = asdict(item)
    return out


def import_json_queue(db: QueueDB, payload: dict[str, Any]) -> int:
    count = 0
    for book_id, record in payload.items():
        db.upsert_queue_item(queue_item_from_record(book_id, record))
        count += 1
    return count


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Aether Forge SQLite queue utility")
    parser.add_argument("db", help="Path to queue sqlite database")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--export_json", default="")
    parser.add_argument("--import_json", default="")
    args = parser.parse_args()

    db = QueueDB(Path(args.db))
    try:
        if args.import_json:
            with open(args.import_json, "r", encoding="utf-8") as file:
                payload = json.load(file)
            n = import_json_queue(db, payload)
            print(json.dumps({"status": "ok", "imported": n}, indent=2))
        if args.export_json:
            out = export_json_queue(db)
            with open(args.export_json, "w", encoding="utf-8") as file:
                json.dump(out, file, indent=2, ensure_ascii=False)
            print(json.dumps({"status": "ok", "exported": len(out)}, indent=2))
        if args.stats:
            print(
                json.dumps(
                    {
                        "queue_size": db.queue_size(),
                        "pending_pages": db.pending_pages(),
                    },
                    indent=2,
                )
            )
    finally:
        db.close()

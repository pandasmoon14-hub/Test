"""Deterministic semantic comparison helpers for the AFQR R1E review."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_json(path: str | Path):
    path = Path(path)
    if not path.is_absolute(): path = ROOT / path
    return json.loads(path.read_text(encoding="utf-8"))

def load_markdown_json(path: str | Path):
    text = (ROOT / path).read_text(encoding="utf-8")
    match = re.search(r"```json\n(.*?)\n```", text, re.S)
    if not match: raise AssertionError(f"missing normative JSON fence in {path}")
    return json.loads(match.group(1))

def normalized_hash(record) -> str:
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()

def family(afqr: str) -> str:
    number = int(afqr.split("-")[1])
    return "core" if number <= 9 else "agency" if number <= 15 else "world"

def partition(edge: dict) -> str:
    order = ["core", "agency", "world"]
    sides = [family(edge["producer_afqr"]), family(edge["consumer_afqr"])]
    return f"{sides[0]}_internal" if sides[0] == sides[1] else "–".join(sorted(sides, key=order.index)) + "_boundary"

def exact_compare(source, destination, field: str):
    return {"field": field, "source": source, "destination": destination, "result": "pass" if source == destination else "fail", "mismatch_reason": None if source == destination else "normalized values differ"}

def normalize_projection(value):
    if isinstance(value, str): return " ".join(value.split())
    if isinstance(value, list): return [normalize_projection(x) for x in value]
    if isinstance(value, dict): return {k: normalize_projection(v) for k, v in sorted(value.items())}
    return value

def bounded_projection_compare(source, destination, *, source_field: str, destination_field: str):
    """Require equality or explicit textual narrowing without semantic negation loss."""
    s, d = normalize_projection(source), normalize_projection(destination)
    if s == d: ok, reason = True, None
    elif isinstance(s, str) and isinstance(d, str) and s in d and not any(token in s.lower() and token not in d.lower() for token in ("not", "must", "only", "unavailable", "revok")):
        ok, reason = True, None
    else: ok, reason = False, "destination is neither equal nor a prohibition-preserving narrowing"
    return {"source_field": source_field, "destination_field": destination_field, "normalization_rule": "recursive whitespace normalization", "permitted_narrowing": "destination may add constraints", "prohibited_loss": "owner/nontransfer/negation/failure constraints", "normalized_source_value": s, "normalized_destination_value": d, "result": "pass" if ok else "fail", "mismatch_reason": reason}

def nested_dict_hashes(value, out=None):
    out = set() if out is None else out
    if isinstance(value, dict):
        if len(value) >= 5: out.add(normalized_hash(value))
        for child in value.values(): nested_dict_hashes(child, out)
    elif isinstance(value, list):
        for child in value: nested_dict_hashes(child, out)
    return out

def projection_records(document: dict):
    for section in ("internal_edge_dispositions", "boundary_dispositions", "core_boundary_dispositions", "agency_boundary_dispositions"):
        for index, record in enumerate(document.get(section, [])):
            ids = record.get("r1c_edge_ids_covered", [record.get("edge_id")])
            if isinstance(ids, str): ids = [ids]
            for edge_id in ids:
                if edge_id: yield edge_id, section, index, record

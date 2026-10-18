"""Load tickets from CSV or JSON."""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

REQUIRED = {"id", "created", "priority", "summary"}


def _norm(rec: dict) -> dict:
    missing = REQUIRED - set(rec)
    if missing:
        raise ValueError(f"ticket missing fields: {sorted(missing)}")
    rec = dict(rec)
    rec["created"] = datetime.fromisoformat(str(rec["created"]))
    rec["priority"] = str(rec["priority"]).upper()
    rec["status"] = str(rec.get("status", "open")).lower()
    rec["description"] = rec.get("description", "") or ""
    return rec


def load_tickets(path: str) -> list[dict]:
    p = Path(path)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text())
    elif p.suffix.lower() == ".csv":
        with p.open(newline="") as fh:
            data = list(csv.DictReader(fh))
    else:
        raise ValueError("unsupported file type (use .csv or .json)")
    return [_norm(r) for r in data]

"""Apply classification, routing and SLA checks."""
from __future__ import annotations

from datetime import datetime

from .rules import SLA_HOURS, classify, sla_status


def process(tickets: list[dict], now: datetime) -> list[dict]:
    out = []
    for t in tickets:
        cat, queue = classify(f"{t['summary']} {t['description']}")
        age = (now - t["created"]).total_seconds() / 3600
        is_open = t["status"] not in ("closed", "resolved")
        sla = sla_status(t["priority"], age) if is_open else "CLOSED"
        out.append({**t, "category": cat, "queue": queue,
                    "age_hours": round(age, 1), "sla": sla,
                    "sla_hours": SLA_HOURS.get(t["priority"], SLA_HOURS["P4"])})
    return out

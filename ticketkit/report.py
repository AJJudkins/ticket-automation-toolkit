"""Weekly Markdown / HTML report."""
from __future__ import annotations

import html
from collections import Counter


def markdown(rows: list[dict], now) -> str:
    cats = Counter(r["category"] for r in rows)
    queues = Counter(r["queue"] for r in rows)
    sla = Counter(r["sla"] for r in rows)
    L = [f"# Weekly Ticket Report", f"_Generated {now:%Y-%m-%d %H:%M} from simulated data_", "",
         f"**Total tickets:** {len(rows)}  ", f"**Breached:** {sla['BREACHED']} | "
         f"**At risk:** {sla['AT_RISK']} | **OK:** {sla['OK']} | **Closed:** {sla['CLOSED']}", "",
         "## By category", "| Category | Count |", "|---|---|"]
    L += [f"| {c} | {n} |" for c, n in cats.most_common()]
    L += ["", "## By queue", "| Queue | Count |", "|---|---|"]
    L += [f"| {q} | {n} |" for q, n in queues.most_common()]
    flagged = [r for r in rows if r["sla"] in ("BREACHED", "AT_RISK")]
    flagged.sort(key=lambda r: (r["sla"] != "BREACHED", -r["age_hours"]))
    L += ["", "## SLA attention list", "| ID | Pri | Queue | Age (h) | SLA (h) | Status | Summary |",
          "|---|---|---|---|---|---|---|"]
    L += [f"| {r['id']} | {r['priority']} | {r['queue']} | {r['age_hours']} | {r['sla_hours']} | "
          f"{r['sla']} | {r['summary'].replace('|', '/')} |" for r in flagged] or ["| - | - | - | - | - | - | None |"]
    return "\n".join(L) + "\n"


def to_html(md: str) -> str:
    return ("<!doctype html><meta charset='utf-8'><title>Weekly Ticket Report</title>"
            "<pre style='font-family:monospace'>" + html.escape(md) + "</pre>")

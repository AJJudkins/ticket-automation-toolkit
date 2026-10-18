"""Keyword classification, routing, and SLA rules."""
from __future__ import annotations

# category -> (keywords, queue). First match by highest keyword count wins.
RULES = {
    "network": (["vpn", "wifi", "switch", "router", "dns", "latency", "network", "firewall"], "Network Team"),
    "access": (["password", "locked", "login", "access", "permission", "mfa"], "Identity & Access"),
    "hardware": (["laptop", "monitor", "keyboard", "printer", "battery", "screen"], "Desktop Support"),
    "software": (["install", "license", "crash", "update", "application", "software"], "Application Support"),
}
DEFAULT = ("general", "Service Desk")

# priority -> SLA resolution hours
SLA_HOURS = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}
RISK_THRESHOLD = 0.75  # flag when this fraction of SLA has elapsed


def classify(text: str) -> tuple[str, str]:
    t = text.lower()
    best, best_hits = DEFAULT, 0
    for cat, (kws, queue) in RULES.items():
        hits = sum(k in t for k in kws)
        if hits > best_hits:
            best, best_hits = (cat, queue), hits
    return best


def sla_status(priority: str, age_hours: float) -> str:
    """Returns OK, AT_RISK or BREACHED for an open ticket."""
    limit = SLA_HOURS.get(priority, SLA_HOURS["P4"])
    if age_hours >= limit:
        return "BREACHED"
    if age_hours >= RISK_THRESHOLD * limit:
        return "AT_RISK"
    return "OK"

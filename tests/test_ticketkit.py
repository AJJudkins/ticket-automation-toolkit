import json
from datetime import datetime

import pytest

from ticketkit.cli import main
from ticketkit.ingest import load_tickets
from ticketkit.process import process
from ticketkit.rules import classify, sla_status


def test_classify_keywords():
    assert classify("VPN drops on wifi") == ("network", "Network Team")
    assert classify("password locked out")[0] == "access"
    assert classify("nothing relevant") == ("general", "Service Desk")


def test_sla_thresholds():
    assert sla_status("P1", 1) == "OK"
    assert sla_status("P1", 3) == "AT_RISK"
    assert sla_status("P1", 4) == "BREACHED"
    assert sla_status("P3", 18) == "AT_RISK"


def test_closed_tickets_not_flagged():
    t = [{"id": "1", "created": datetime(2026, 1, 1), "priority": "P1", "status": "closed",
          "summary": "vpn", "description": ""}]
    assert process(t, datetime(2026, 2, 1))[0]["sla"] == "CLOSED"


def test_ingest_csv_and_json(tmp_path):
    assert len(load_tickets("data/sample_tickets.csv")) == 20
    f = tmp_path / "t.json"
    f.write_text(json.dumps([{"id": "1", "created": "2026-01-01T00:00", "priority": "p2", "summary": "x"}]))
    assert load_tickets(str(f))[0]["priority"] == "P2"


def test_missing_fields_rejected(tmp_path):
    f = tmp_path / "t.json"
    f.write_text(json.dumps([{"id": "1"}]))
    with pytest.raises(ValueError):
        load_tickets(str(f))
    assert main([str(f)]) == 2


def test_cli_report(tmp_path):
    out = tmp_path / "r.html"
    assert main(["data/sample_tickets.csv", "--now", "2026-01-12T12:00", "--out", str(out)]) == 0
    assert "Weekly Ticket Report" in out.read_text()

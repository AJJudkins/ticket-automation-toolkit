"""python -m ticketkit.cli data/sample_tickets.csv --now 2026-01-12T12:00 --out report.md"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime

from .ingest import load_tickets
from .process import process
from .report import markdown, to_html


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="ticketkit")
    p.add_argument("input", help=".csv or .json tickets")
    p.add_argument("--now", help="reference time (ISO); default is current time")
    p.add_argument("--out", help="output file (.md or .html); default prints Markdown")
    a = p.parse_args(argv)
    try:
        now = datetime.fromisoformat(a.now) if a.now else datetime.now()
        rows = process(load_tickets(a.input), now)
    except (OSError, ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    md = markdown(rows, now)
    if a.out:
        with open(a.out, "w") as fh:
            fh.write(to_html(md) if a.out.endswith(".html") else md)
        print(f"wrote {a.out}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())

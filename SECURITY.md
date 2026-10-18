# Security policy

## Scope and safety
offline: reads a local ticket file, writes only the report path you give (never overwriting without `--force`); no ticketing system or credentials are involved.

## What was and was not tested
**Tested (automated, in CI and locally):** ingestion, routing/SLA rules, report output and CLI guards using made-up sample tickets.

**Not tested:** real ServiceNow/Jira exports or APIs (no integration exists), large ticket volumes, and time zones (timestamps are naive).

## Reporting a problem
This is a small personal portfolio project, not a supported product. If you find a security issue, please open a GitHub issue **without** secrets, credentials or real system details, or use GitHub's "Report a vulnerability" button on the Security tab if it is enabled.

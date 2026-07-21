---
created_at: '2026-06-05T20:30:00Z'
entities:
- Sam
- Alice
- Julien
- Metabase
id: 01KTCQMXA05AA6J12A607G7P80
language: en
source:
  end_turn: 8
  session_id: seed-1837740b73faff57
  start_turn: 0
tags:
- rollout
- rollback
- budget
- slo
title: Rollout rules, rollback criteria, and operational caps
type: decision
---

Rollout rules and operational constraints: require p95 < 5 s for the top queries under 10 concurrent analysts; if this is not met, revert Metabase to DuckDB within the 48-hour rollback window after cutover. Budget cap for ClickHouse hosting is €1,500/month; migration effort capped at 5 engineer-days (3 days infra + 2 days schema/ingest/tests as planned). Monitoring thresholds: alert on p95 > 5 s (auto-escalate to Julien if sustained > 2 minutes), CPU > 80% (page), disk > 85% (page). Retention policy: raw MergeTree data retained 1 year, aggregated tables retained 3 years. Acceptance checklist before cutover: row-count parity checks, 10–12 concurrent Metabase load tests passing SLO, MVs for Q1 and Q3 in place (5-minute cadence), RBAC and backups configured, and Alice's sign-off.
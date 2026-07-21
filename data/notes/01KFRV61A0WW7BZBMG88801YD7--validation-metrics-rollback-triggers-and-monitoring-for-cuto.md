---
created_at: '2026-01-24T20:30:00Z'
entities:
- pg_stat_statements
- Grafana
- CloudWatch
- Sam
- Nico
- Antoine
id: 01KFRV61A0WW7BZBMG88801YD7
language: en
source:
  end_turn: 4
  session_id: seed-d2bad5a2a44349e1
  start_turn: 4
tags:
- slo
- rollback
- monitoring
- runbook
title: Validation metrics, rollback triggers and monitoring for cutover
type: decision
---

Set concrete validation metrics and rollback triggers to protect production availability and data correctness. Performance SLAs: p95 latency for typical nearest queries must be <200ms; trigger a rollback if p95 exceeds 350ms sustained for 30 minutes. Error-rate thresholds: target <0.5% application error rate; trigger rollback if >1% for 10 minutes. Replication lag (if using read replicas) must stay <5 seconds. Data parity checks: per-table row counts must be within 0.1% between Mongo and Postgres during dual-write, and a sample of 100 joined records must match exactly. Rollback plan: keep Mongo running as read fallback, enable dual-write for a minimum two-week verification period, and revert read traffic to Mongo and stop writes to Postgres if any trigger threshold is exceeded. Runbook requirements: automated post-migration sanity checks and monitoring dashboards; manual sign-off required from either Sam or Nico before proceeding past each major stage. Monitoring tools: enable pg_stat_statements, build Grafana dashboards for latencies and error rates, and create CloudWatch alerts that map to the rollback triggers.
---
created_at: '2026-04-17T20:30:00Z'
entities:
- Prometheus
- Alertmanager
- DuckDB
- VM
id: 01KPEJ5PA033GX74W38SV7DQKD
language: en
source:
  end_turn: 6
  session_id: seed-536417aa4825bf05
  start_turn: 6
tags:
- monitoring
- observability
- metrics
title: Monitoring requirements and metrics to collect
type: task
---

Monitoring must be in place before go-live to detect memory pressure and runaway queries. Minimum metrics to collect and alert on: - System-level: RAM usage (absolute and %), swap usage, CPU utilization, disk I/O and NVMe health. - Process-level: DuckDB process RSS, virtual memory, number of active queries/threads. - Query metrics: per-query latency (p50, p95), GB scanned per query, rows returned, query start/end times, user/application that issued the query. - Availability: DuckDB process uptime and Metabase JDBC connection health. Alerts: memory pressure and swap usage should trigger immediate alerts to #infra Slack; long-running queries (over 600 s) should either be auto-terminated or flagged. Use Prometheus to scrape these metrics and Alertmanager to route alerts. Implement basic dashboards for p95 latency, cost/billing estimate, and GB scanned trends so we can spot growth before it breaks the single-node model.
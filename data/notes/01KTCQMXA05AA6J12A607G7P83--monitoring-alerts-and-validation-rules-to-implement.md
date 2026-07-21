---
created_at: '2026-06-05T20:30:00Z'
entities:
- ClickHouse
- Metabase
- Julien
id: 01KTCQMXA05AA6J12A607G7P83
language: en
source:
  end_turn: 8
  session_id: seed-1837740b73faff57
  start_turn: 6
tags:
- monitoring
- alerts
- slo
- observability
title: Monitoring, alerts, and validation rules to implement
type: task
---

Monitoring and alerting specifics to implement during and after migration: measure and alert on p95 query latency (primary SLI) with an alert threshold at 5 seconds. Configure automatic escalation to Julien (ops) if p95 > 5 s is sustained for more than 2 minutes. System-level thresholds: CPU > 80% should page ops; disk > 85% should page ops. Also monitor memory pressure and number of concurrent queries to detect resource saturation early. During staged testing, validate using Metabase-driven query patterns — run 10–12 concurrent Metabase sessions executing the top queries and capture p50/p95/p99 latency, CPU, disk and memory metrics. Implement dashboards for these metrics and set synthetic tests to run the top query set every 5–10 minutes to detect regressions post-cutover.
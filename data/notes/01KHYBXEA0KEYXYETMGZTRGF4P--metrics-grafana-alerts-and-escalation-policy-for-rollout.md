---
created_at: '2026-02-20T20:30:00Z'
entities:
- Grafana
- SRE
id: 01KHYBXEA0KEYXYETMGZTRGF4P
language: en
source:
  end_turn: 6
  session_id: seed-d490bfd09772dd8c
  start_turn: 0
tags:
- metrics
- alerts
- grafana
- slo
title: Metrics, Grafana alerts, and escalation policy for rollout
type: task
---

Metrics to record and alert thresholds to configure before and during the rollout: record per-endpoint cache hit rate, cache miss rate, p95 latency for cached endpoints, Postgres CPU usage, overall endpoint error rates, and cache.evictions.via_pubsub. Alert thresholds: cache hit rate <70% = warning, <60% = critical; p95 latency for cached endpoints >70 ms = warning, >120 ms = critical; Postgres CPU not reduced by at least 20% vs baseline after reaching 50% rollout = warning; endpoint error rate increase on cached endpoints >0.5% absolute = warning. Routing: critical alerts to pager for SRE, warnings to Slack. Enable alerts in staging on day 1 of staging testing; enable production alerts at the 20% production rollout step. Dashboard should show historical baseline metrics (pre-cache) for comparison and annotate rollout percentages/dates for correlation. Also add dashboards for cache.evictions.via_pubsub and DEL-at-write success/failure.
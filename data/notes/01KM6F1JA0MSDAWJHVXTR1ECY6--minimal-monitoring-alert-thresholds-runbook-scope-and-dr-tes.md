---
created_at: '2026-03-20T20:30:00Z'
entities:
- Confluent
id: 01KM6F1JA0MSDAWJHVXTR1ECY6
language: en
source:
  end_turn: 6
  session_id: seed-7f779b0857c2f80a
  start_turn: 6
tags:
- monitoring
- runbook
- dr
- connectors
title: Minimal monitoring, alert thresholds, runbook scope, and DR testing plan
type: decision
---

Agreed minimal instrumentation and runbook requirements to accept a Kafka rollout: Cluster/broker alarms — CPU >75% for 10 minutes, disk usage >75% per broker; replication health — under‑replicated partitions >0 for 5 minutes (critical) and ISR shrink events (any broker dropped) trigger immediate alert. Consumer health — consumer lag thresholds: telemetry topics >30s (alert), status updates >60s (alert). Connectors — task failures >1 for 5 minutes. Dashboards: cluster overview, topic lag, per‑consumer throughput. Runbook must be concise (max six pages) and include playbooks for: broker down, under‑replicated partition, consumer lag spike, connector failure, and failover/restore steps. Operational mitigations: buy Confluent support, enforce retention policies, and configure cross‑region replication. DR restore test scheduled by 2026-05-15. These minimal controls are the safety net required to approve production usage.
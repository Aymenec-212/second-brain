---
created_at: '2026-04-17T20:30:00Z'
entities:
- 95th-percentile
- median
- €200/month
id: 01KPEJ5PA033GX74W38SV7DQKB
language: en
source:
  end_turn: 4
  session_id: seed-536417aa4825bf05
  start_turn: 3
tags:
- slo
- monitoring
- budget
- contingency
title: Day‑30 success metrics and contingency triggers
type: decision
---

Defined success criteria for day 30 (post go-live): - Query latency: 95th-percentile for common ad-hoc queries under 15 seconds; median under 3 seconds. - Cost: monthly infra cost must remain under €200. - Availability: zero user-facing downtime during working hours. - Monitoring: metrics in place for memory pressure, swap use, CPU, query time, and GB scanned per query. Operational contingency: if the 95th-percentile exceeds 15 seconds regularly, or if frequent OOMs occur, trigger the contingency plan (first move troublesome workloads to ClickHouse single-node; escalate to Snowflake only if budget increases substantially). Weekly check-ins (through 2026-06-01) will validate whether these metrics hold and whether the budget is respected. These targets will be used to decide whether to scale the VM, adjust memory limits, or move to the fallback systems.
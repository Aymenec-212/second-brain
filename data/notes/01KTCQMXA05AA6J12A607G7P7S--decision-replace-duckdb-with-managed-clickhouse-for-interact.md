---
created_at: '2026-06-05T20:30:00Z'
entities:
- DuckDB
- ClickHouse
- ClickHouseCloud
- Altinity
- Sam
- Alice
- Julien
- Metabase
id: 01KTCQMXA05AA6J12A607G7P7S
language: en
source:
  end_turn: 4
  session_id: seed-1837740b73faff57
  start_turn: 0
tags:
- data-warehouse
- clickhouse
- duckdb
- analytics
- migration
- slo
title: 'Decision: Replace DuckDB with managed ClickHouse for interactive analytics'
type: decision
---

Decision: move interactive analytics workload from DuckDB to a managed ClickHouse cluster (ClickHouseCloud/Altinity). Rationale: DuckDB performed well for single interactive scans but failed to meet concurrency requirements — high p95 tail latency and out-of-memory (OOM) errors under realistic concurrent analyst load. ClickHouse PoC (3-node test cluster) met the concurrency SLO in testing with p95 latency far below target and no OOMs. Constraints and acceptance criteria: target SLO is support for 10 concurrent analysts with p95 < 5 s on the top BI queries; budget cap for ClickHouse service ~€1,500/month; team ops budget up to 5 engineer-days for migration. Operational decision: use managed ClickHouse (reduce ops burden) and retain DuckDB locally for ML/experiments and ad-hoc single-user work. Owners: Sam (migration lead), Alice (analyst validator), Julien (ops/alerts/backups).
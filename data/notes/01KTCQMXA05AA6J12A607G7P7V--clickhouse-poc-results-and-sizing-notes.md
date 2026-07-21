---
created_at: '2026-06-05T20:30:00Z'
entities:
- ClickHouse
- ClickHouseCloud
- r5.large
- r5.xlarge
id: 01KTCQMXA05AA6J12A607G7P7V
language: en
source:
  end_turn: 4
  session_id: seed-1837740b73faff57
  start_turn: 0
tags:
- benchmarks
- clickhouse
- poc
- sizing
title: ClickHouse PoC results and sizing notes
type: fact
---

ClickHouse proof-of-concept results: a 3-node test ClickHouse cluster handled the same workload where DuckDB failed. At 12 concurrent analyst queries the ClickHouse p95 ~1.8 s and the cluster did not experience OOMs. The PoC nodes were roughly equivalent to r5.large each. For production the plan is to use slightly larger nodes (example r5.xlarge) to provide headroom and reliably meet the SLO. The ClickHouse cluster will be configured with replication factor (RF) = 2 to balance durability and cost. The PoC shows ClickHouse is capable of serving concurrent BI query patterns (heavy group-bys and window functions) with lower latency and better resource isolation than an in-process engine like DuckDB.
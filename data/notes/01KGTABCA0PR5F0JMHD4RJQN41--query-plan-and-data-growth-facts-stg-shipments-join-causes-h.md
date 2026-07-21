---
created_at: '2026-02-06T20:30:00Z'
entities:
- stg_orders
- stg_shipments
- customers
- Postgres 14
- RDS-like instance
id: 01KGTABCA0PR5F0JMHD4RJQN41
language: en
source:
  end_turn: 4
  session_id: seed-4d8543dbcb9985e9
  start_turn: 1
tags:
- postgres
- performance
- explain
- indexes
- data-growth
title: 'Query plan and data-growth facts: stg_shipments join causes hash spill'
type: fact
---

Root technical observations and measurements: the enrichment step for orders_mart joins stg_orders -> stg_shipments on orders.id = shipments.order_id and also joins customers for name/segment. Data growth: stg_shipments row count increased from ~40M in November to ~110M (110,234,567) as of early February. The shipments table only has a primary key on id and no index on order_id. An EXPLAIN ANALYZE captured on 2026-02-05 shows a Sequential Scan on stg_shipments producing the full ~110,234,567 rows, followed by a Hash build with estimated hash size ~58,134,000 kB that spilled to disk. The session work_mem was the default 16MB at the time. The Postgres instance is Postgres 14 on an RDS-like instance with 128GB RAM, max_connections=200, parallel_workers_per_gather=2. The hash-join + spill contributes approximately +2 hours compared to baseline, matching the observed regression. Rebuilding an index on shipments is non-trivial: current table size ~1.2 TB, index build estimate 3–5 hours and ~40 GB temp space (CREATE INDEX CONCURRENTLY assumed). These are the measurable facts that constrain remediation choices.
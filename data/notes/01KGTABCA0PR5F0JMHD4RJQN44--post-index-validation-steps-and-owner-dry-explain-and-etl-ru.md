---
created_at: '2026-02-06T20:30:00Z'
entities:
- ETL-142
- Camille
- EXPLAIN ANALYZE
- orders_mart
id: 01KGTABCA0PR5F0JMHD4RJQN44
language: en
source:
  end_turn: 11
  session_id: seed-4d8543dbcb9985e9
  start_turn: 11
tags:
- validation
- testing
- etl
- postgres
title: Post-index validation steps and owner (dry EXPLAIN and ETL runtime checks)
type: task
---

Post-build validation and handover tasks once the concurrent index is created: 1) As soon as the index build completes, run a dry EXPLAIN (and an EXPLAIN ANALYZE if feasible in non-peak) of the enrichment query that joins stg_orders -> stg_shipments to confirm the planner uses the new shipments(order_id) index and that the hash build/spill no longer occurs. 2) Run the next nightly ETL with the planned session settings (work_mem=512MB, parallel_workers_per_gather=4) and measure end-to-end runtime; record improvement versus the 7h run and prior 4h baseline. 3) If EXPLAIN shows planner still chooses a seq scan or hash spill persists, revert tuning and escalate to Camille for deeper plan tuning or to delay index usage investigation. 4) Update ETL-142 with validation results, attach the EXPLAIN output, and close the immediate remediation items; keep the long-term refactor work item open until the incremental join implementation is complete by 2026-02-20. Camille is the primary owner for the build and initial validation; I am responsible for updating ETL-142 with the EXPLAIN and runtime comparisons.
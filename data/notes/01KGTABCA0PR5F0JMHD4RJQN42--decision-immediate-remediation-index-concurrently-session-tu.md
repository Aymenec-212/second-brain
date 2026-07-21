---
created_at: '2026-02-06T20:30:00Z'
entities:
- shipments
- order_id
- CREATE INDEX CONCURRENTLY
- work_mem
- parallel_workers_per_gather
- ETL-142
id: 01KGTABCA0PR5F0JMHD4RJQN42
language: en
source:
  end_turn: 6
  session_id: seed-4d8543dbcb9985e9
  start_turn: 5
tags:
- decision
- postgres
- index
- performance
- roadmap
title: 'Decision: immediate remediation = index concurrently + session tuning; long-term
  refactor'
type: decision
---

I evaluated three remediation options and chose a hybrid plan: 1) CREATE INDEX CONCURRENTLY on shipments(order_id) to eliminate the sequential scan and large hash build; 2) session-level planner tuning for the immediate ETL window (increase work_mem to 512MB and set parallel_workers_per_gather to 4) to reduce spilling while the index is being created or if the index build is delayed; 3) a long-term refactor of the ETL to incremental/filtered joins (pre-filter shipments by date/shipment_status) as a durable fix. Rationale and trade-offs: the concurrent index is expected to be the most effective single change (should allow the planner to use an index scan instead of scanning 110M rows), but it has costs — estimated build time 3–5 hours, ~40 GB temp IO, and risk of increased replication lag or IOPS during the build on a ~1.2 TB table. Increasing work_mem and parallel workers is immediate and low-risk relative to the index build but does not avoid scanning the large shipments table. The long-term ETL refactor is the most robust but requires ~2 weeks of development. Immediate plan: run both (1) and (2) in the next maintenance window; open ticket ETL-142 with a deadline of 2026-02-20 to implement the incremental/filtered-join refactor and mark that as the long-term remediation.
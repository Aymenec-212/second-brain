---
created_at: '2026-02-06T20:30:00Z'
entities:
- CREATE INDEX CONCURRENTLY
- CloudWatch
- pg_cancel_backend
- Camille
- ETL-142
id: 01KGTABCA0PR5F0JMHD4RJQN43
language: en
source:
  end_turn: 10
  session_id: seed-4d8543dbcb9985e9
  start_turn: 7
tags:
- runbook
- maintenance
- monitoring
- oncall
title: Runbook and abort criteria for CREATE INDEX CONCURRENTLY (maintenance window)
type: task
---

Scheduled maintenance window and explicit runbook for the concurrent index build and ETL tuning: snapshot the DB at 21:45 on 2026-02-07. Start CREATE INDEX CONCURRENTLY on shipments(order_id) at 22:00, target window 22:00–04:00. ETL session will run with work_mem set to 512MB and parallel_workers_per_gather set to 4 for that ETL run. Monitoring: use CloudWatch to track replica lag, read IOPS, and CPU. Abort/rollback thresholds (if any of these persist for the stated duration): replica lag > 60 seconds; average read IOPS > 70% of baseline for 15 continuous minutes; CPU > 85% for 15 continuous minutes. If any abort condition triggers, runbook steps are: 1) pg_cancel_backend for the index build process to stop the concurrent index, 2) notify #oncall and the DB lead, 3) revert ETL session settings to defaults, 4) rerun ETL using the pre-existing ETL flow (i.e., without the incremental refactor) and rely on session tuning only until we can re-plan. Camille (DB lead) will be on-call and will start at 21:30 on 2026-02-07. I will tag and assign ETL-142 to Camille with the runbook and the deadline 2026-02-20.
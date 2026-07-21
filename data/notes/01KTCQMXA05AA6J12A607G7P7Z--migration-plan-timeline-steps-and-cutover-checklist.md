---
created_at: '2026-06-05T20:30:00Z'
entities:
- ClickHouse
- ClickHouseCloud
- Parquet
- S3
- Metabase
- Sam
- Alice
- Julien
id: 01KTCQMXA05AA6J12A607G7P7Z
language: en
source:
  end_turn: 8
  session_id: seed-1837740b73faff57
  start_turn: 0
tags:
- migration
- plan
- timeline
- cutover
title: 'Migration plan: timeline, steps, and cutover checklist'
type: task
---

High-level migration plan and timeline: Start infra provisioning on 2026-06-08 (provision managed 3-node ClickHouse cluster, RF=2, enable autoscaling if available). 2026-06-09 to 2026-06-16: data sync and schema tests. Bulk load from Parquet on S3 into ClickHouse and validate row counts (initial bulk load 2026-06-09). 2026-06-10 to 2026-06-14: run concurrent Metabase load tests (10–12 concurrent) against staged cluster to validate p95 and check resource utilization. 2026-06-11: build materialized views (orders_per_route, weekly_volume_by_customer). 2026-06-16: Alice (analyst) validates queries and signs off. Cutover date 2026-06-19: update Metabase connection to point to ClickHouse, announce to analysts. Post-cutover 48-hour rollback window: keep DuckDB read-only Parquet snapshots on S3 and ability to re-point Metabase back to DuckDB if p95 > 5 s under 10 concurrent. Migration deliverables: schema translation from DuckDB SQL to ClickHouse MergeTree partitioning by event_date, ingest pipeline (Parquet→S3→ClickHouse batch loads), MVs/pre-aggregations with 5-minute cadence for priority queries, Metabase integration, RBAC, backups to S3, monitoring (p95 query latency, CPU, disk). Owners: Sam leads migration; Alice validates; Julien manages ClickHouse account and alerts.
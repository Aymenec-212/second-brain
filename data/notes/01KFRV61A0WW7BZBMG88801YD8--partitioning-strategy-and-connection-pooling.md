---
created_at: '2026-01-24T20:30:00Z'
entities:
- BRIN
- GiST
- PgBouncer
- Postgres
- Sam
- Nico
id: 01KFRV61A0WW7BZBMG88801YD8
language: en
source:
  end_turn: 6
  session_id: seed-d2bad5a2a44349e1
  start_turn: 6
tags:
- partitioning
- pgbouncer
- performance
- vacuum
title: Partitioning strategy and connection pooling
type: decision
---

From day one, partition the events table by time: range partitions by month for the first 12 months. Expected first-year total ~20M events implies ~1.6M rows/month on average; monthly partitions keep VACUUM and maintenance bounded and make archiving old data straightforward. Use BRIN indexes on the time column per partition to keep index size small for large append-only event data; use GiST (or SP-GiST) indexes on the geometry/geography columns for spatial queries. If a partition becomes a hotspot (some routes much hotter than others), consider adding hash partitioning on route_id to split load further. Keep users and routes tables unpartitioned initially. Plan to move partitions older than 12 months to cheaper storage or an archival database. Operationally, deploy a connection pooler (PgBouncer) on the infra node and tune max_connections conservatively to avoid exhausting RDS connections.
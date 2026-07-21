---
created_at: '2026-06-05T20:30:00Z'
entities:
- orders_events
- customers
- routes
id: 01KTCQMXA05AA6J12A607G7P7Y
language: en
source:
  end_turn: 2
  session_id: seed-1837740b73faff57
  start_turn: 2
tags:
- schema
- dataset
- ingest
- retention
title: 'Data shape: orders_events and related tables, growth and retention'
type: fact
---

Key dataset details to guide schema and ingestion: main table is orders_events with ~40M rows today; compressed Parquet ~18 GB, raw ~60 GB. Daily ingest rate ~2M rows/day, implying steady growth and planning for capacity. Two common join tables: customers (~1.2M rows) and routes (~6K rows). Queries are heavy on group-bys and window functions (e.g., latency histograms, cohorts). Retention policy for raw MergeTree tables in ClickHouse will be 1 year. Aggregated/rolled-up tables will be retained for 3 years. These specifics determine partitioning strategy (event_date), MergeTree primary key choices, and storage sizing for ClickHouse.
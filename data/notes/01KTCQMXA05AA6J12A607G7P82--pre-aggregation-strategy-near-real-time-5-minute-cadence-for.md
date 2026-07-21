---
created_at: '2026-06-05T20:30:00Z'
entities:
- ClickHouse
- materialized views
- orders_per_route
- weekly_volume_by_customer
id: 01KTCQMXA05AA6J12A607G7P82
language: en
source:
  end_turn: 8
  session_id: seed-1837740b73faff57
  start_turn: 7
tags:
- pre-aggregation
- materialized-views
- etl
- clickhouse
title: 'Pre-aggregation strategy: near-real-time 5-minute cadence for priority tables'
type: decision
---

Pre-aggregation decision and approach: implement near-real-time pre-aggregations with a 5-minute cadence for the highest-priority queries. Specifically, create materialized views that feed aggregated MergeTree tables for orders_per_route and weekly_volume_by_customer with a 5-minute update window. Rationale: analysts need interactive performance during the day; 5-minute recency is acceptable for these KPIs. For latency_histogram (the complex windowed query), keep it on-demand initially and attempt to optimize using ClickHouse window/array functions; if latency remains unacceptable, evaluate a sampled or approximate pre-aggregation. Complex window queries will remain on-demand to start, optimizing progressively. Aggregated MV tables will have a longer retention (3 years) versus raw MergeTree (1 year).
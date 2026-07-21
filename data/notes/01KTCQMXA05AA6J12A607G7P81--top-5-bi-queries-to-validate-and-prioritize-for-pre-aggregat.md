---
created_at: '2026-06-05T20:30:00Z'
entities:
- orders_per_route
- latency_histogram
- weekly_volume_by_customer
- churn_cohort
- ad-hoc filters
- Metabase
- Alice
id: 01KTCQMXA05AA6J12A607G7P81
language: en
source:
  end_turn: 6
  session_id: seed-1837740b73faff57
  start_turn: 6
tags:
- queries
- validation
- metabase
- pre-aggregation
title: Top 5 BI queries to validate and prioritize for pre-aggregation
type: task
---

Top 5 queries to validate and prioritize: 1) orders_per_route — group by route on orders_events; scans ~30M rows; current p95 18 s; highest business priority — must be prioritized for MV/pre-aggregation. 2) latency_histogram — window and bucketing over event_ts; scans ~24M rows; current p95 25 s; complex and causes worst tail; keep on-demand initially and attempt ClickHouse window/array optimizations or sampled pre-aggregation later. 3) weekly_volume_by_customer — join orders_events to customers; join scans ~4M rows; current p95 6 s; prioritize for correctness and pre-aggregation. 4) churn_cohort — cohort by signup date; scans ~12M rows; current p95 12 s. 5) ad-hoc filters — variable scans and variable p95; cannot fully pre-aggregate. Validation plan: prioritize Q1 and Q2 for performance checks and Q3 for correctness during staged testing. Alice is responsible for query validation and sign-off.
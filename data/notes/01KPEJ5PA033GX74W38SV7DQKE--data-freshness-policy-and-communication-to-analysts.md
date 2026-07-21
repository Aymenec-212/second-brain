---
created_at: '2026-04-17T20:30:00Z'
entities:
- Postgres
- DuckDB
- Metabase
- Airflow
id: 01KPEJ5PA033GX74W38SV7DQKE
language: en
source:
  end_turn: 8
  session_id: seed-536417aa4825bf05
  start_turn: 8
tags:
- data-freshness
- communication
- realtime
title: Data freshness policy and communication to analysts
type: decision
---

Data freshness policy for DuckDB-powered analytics: standard freshness for analysts' ad-hoc queries will be 24 hours, achieved by nightly Airflow materialization of partitioned Parquet and the DuckDB DB file. For troubleshooting and near-real-time needs, the most recent ~15-minute data will remain in Postgres materialized tables and a small real-time dashboard outside DuckDB. Communicate this scope and limitation to the analytics team (Leo, Maria, Aisha and any additional analysts) by 2026-05-10 so they do not expect sub-hour freshness from Metabase queries against DuckDB. Keeping interactive workloads on 24-hour data reduces unpredictability and keeps the single-node DuckDB setup cheap and reliable. If analysts need more frequent data for a particular use case, evaluate a targeted real-time pipeline or move that specific workload out of DuckDB.
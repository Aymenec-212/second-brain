---
created_at: '2026-04-17T20:30:00Z'
entities:
- DuckDB
- Metabase
- JDBC
- S3
id: 01KPEJ5PA033GX74W38SV7DQK8
language: en
source:
  end_turn: 2
  session_id: seed-536417aa4825bf05
  start_turn: 0
tags:
- decision
- duckdb
- cost
title: 'Decision: adopt single-node DuckDB for analysts'' ad-hoc queries'
type: decision
---

Final decision: use DuckDB as the primary engine for analysts' ad-hoc queries. Rationale: DuckDB is cheap, simple, single-node, and fits the low-concurrency, moderate-scan workloads of three analysts. DuckDB will serve via a JDBC connector for Metabase so analysts can run interactive queries from the dashboard UI. Analysts will also be able to run the same Parquet data locally in notebooks for reproducible local runs. Nightly data materialization will be handled by Airflow writing partitioned Parquet to S3 plus maintaining a nightly DuckDB DB file on the VM (or optionally using duckdb-httpfs to read Parquet directly from S3). This setup prioritizes low cost (~€200/month target), minimal ops, and reproducibility. Fallback options are defined: if the single-node DuckDB approach hits resource or latency limits, first transition the workload to ClickHouse (single-node or cluster depending on scale); only consider Snowflake if budget expands substantially (>~€1k/month). Keep analysts informed about freshness and limitations to avoid unexpected large scans during interactive sessions.
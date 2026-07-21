---
created_at: '2026-04-17T20:30:00Z'
entities:
- VM
- NVMe
- duckdb-httpfs
- Airflow
- S3
- Parquet
id: 01KPEJ5PA033GX74W38SV7DQK9
language: en
source:
  end_turn: 2
  session_id: seed-536417aa4825bf05
  start_turn: 2
tags:
- infrastructure
- vm
- storage
- airflow
title: Prod VM specification and materialization architecture
type: decision
---

Proposed production VM sizing and architecture: provision a single-node VM with 8 vCPU, 64 GB RAM, and 1 TB NVMe (estimated cost ≈ €180/month) to host DuckDB and the nightly DuckDB DB file. Nightly Airflow DAG will write partitioned Parquet to S3 and either write a consolidated DuckDB DB file on the VM or rely on duckdb-httpfs to allow DuckDB to read Parquet directly from S3. Metabase will connect to DuckDB via JDBC. Analysts will be encouraged to run the same Parquet files locally in notebooks for reproducibility. The VM choice aims to balance memory needed for in-memory vectorized execution with budget constraints. Exact VM size, memory limits, and whether to use local DB file vs HTTPFS will be finalized during provisioning and initial load testing.
---
created_at: '2026-06-05T20:30:00Z'
entities:
- DuckDB
- r5.4xlarge
id: 01KTCQMXA05AA6J12A607G7P7T
language: en
source:
  end_turn: 2
  session_id: seed-1837740b73faff57
  start_turn: 0
tags:
- benchmarks
- duckdb
- performance
- dataset
title: 'Benchmark: DuckDB performance and failure modes on 40M-row dataset'
type: fact
---

Benchmark facts for DuckDB: dataset used was 40,000,000 rows (raw ~60 GB, parquet compressed ~18 GB) stored as Parquet. Tests ran on a VM equivalent to r5.4xlarge (16 vCPU, 128 GB RAM). Single interactive scans were fast: median ~1.2 s. Under concurrency the system degraded: with 8–12 concurrent analyst queries median latency rose to ~3–4 s and p95 spiked to 18–25 s. Memory limits were reached at around 18 concurrent queries, causing OOMs. This concurrency/oom pattern is incompatible with current analyst behavior (8 daily active, peak 12 concurrent). These numbers drove the decision to look for a cluster-based analytics engine that tolerates concurrent ad-hoc BI workloads.
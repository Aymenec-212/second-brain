---
created_at: '2026-04-21T20:30:00Z'
entities:
- pgvector
- HNSW
id: 01KPRVRJA040F390AW1FABMRAY
language: en
source:
  end_turn: 2
  session_id: seed-b1386cf507fa6f14
  start_turn: 2
tags:
- pgvector
- hnsw
- performance
- indexing
- backups
title: Empirical pgvector observations at 3M vectors and operational concerns
type: fact
---

Empirical runs of pgvector with HNSW at the current 3M-vector scale show single-node RDS p95 latency roughly between 30–70 ms for k=10 when no metadata filters are applied. However, adding metadata filters (e.g., customer_id or date range) often doubles latency because of the inefficient interaction between ANN candidate generation and Postgres-level filtering. I have not yet stress-tested large-scale incremental inserts: continuous daily ingest of ~100k vectors raises concerns about index maintenance costs and the effect of continuous updates on HNSW performance. Backups via full RDS snapshots are acceptable from a persistence standpoint, but index rebuild times are a worry — a long rebuild would be operationally disruptive. I need migration options prepared if pgvector proves unsuitable at scale.
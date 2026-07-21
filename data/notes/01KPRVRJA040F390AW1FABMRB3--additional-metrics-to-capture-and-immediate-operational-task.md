---
created_at: '2026-04-21T20:30:00Z'
entities:
- RDS
- pgvector
id: 01KPRVRJA040F390AW1FABMRB3
language: en
source:
  end_turn: 9
  session_id: seed-b1386cf507fa6f14
  start_turn: 9
tags:
- monitoring
- metrics
- ops
- costs
title: Additional metrics to capture and immediate operational tasks before 2026-05-01
type: task
---

Add these metrics and tasks to the test plan: measure index memory residency to confirm HNSW fits in RAM at target scales; capture cold-cache vs warm-cache latencies to understand realistic worst-case p95; verify multi-tenant fault isolation (test that filters never leak other customers' vectors, and simulate accidental tenant ID errors); log incremental insert throughput and HNSW maintenance CPU spikes during continuous ingest; measure snapshot and index-rebuild durations for disaster recovery planning; and produce cost projections comparing scaled RDS + pgvector vs self-hosted Milvus/Qdrant vs managed Pinecone, including expected infra costs and estimated engineering ops hours. Immediate tasks: prepare query scripts and synthetic workload drivers for K ∈ {100,500,1000}, create monitoring dashboards (latency percentiles, recall, CPU/RAM/IO, GC/events), and schedule the baseline run starting 2026-05-01.
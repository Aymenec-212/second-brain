---
created_at: '2026-04-21T20:30:00Z'
entities:
- pgvector
- Milvus
- Qdrant
- Pinecone
id: 01KPRVRJA040F390AW1FABMRB1
language: en
source:
  end_turn: 6
  session_id: seed-b1386cf507fa6f14
  start_turn: 6
tags:
- test-plan
- migration
- timeline
- thresholds
title: Planned pgvector baseline tests, migration thresholds, and migration targets
type: task
---

Implementation plan and decision thresholds: 1) Start baseline tests on pgvector (HNSW with tuned parameters) at scale up to 20–27M vectors on a larger RDS node, beginning 2026-05-01. 2) Measure p95/p50/p99, recall@10, index build time, incremental insert impact, CPU/RAM/disk I/O, and backup/index-rebuild time. 3) Migration triggers: if p95 > 80 ms or weekly ops exceed 10 hours or a full index rebuild takes > 4 hours, begin migration planning. 4) Migration targets to evaluate: Milvus (self-hosted), Qdrant (self-hosted), and Pinecone (managed) — choose based on latency, ops burden, and cost. 5) Evaluate results and decide by 2026-08-01; if pgvector meets thresholds, keep it for six months and reassess. This is the working runbook to decide whether to invest more into pgvector or migrate.
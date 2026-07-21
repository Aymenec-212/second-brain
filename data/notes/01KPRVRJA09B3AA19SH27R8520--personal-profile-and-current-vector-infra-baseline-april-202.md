---
created_at: '2026-04-21T20:30:00Z'
entities:
- Sam
- All-MiniLM-L6-v2
- pgvector
- Postgres
- AWS RDS
id: 01KPRVRJA09B3AA19SH27R8520
language: en
source:
  end_turn: 0
  session_id: seed-b1386cf507fa6f14
  start_turn: 0
tags:
- profile
- infrastructure
- embeddings
- pgvector
- postgres
title: Personal profile and current vector infra baseline (April 2026)
type: fact
---

I am Sam (31), backend/ML at a Paris logistics startup. Current vector search lives in a single-node AWS RDS Postgres with pgvector installed. The production dataset today contains ~3 million shipment embeddings produced with All-MiniLM-L6-v2 (dimension = 384). Daily ingest is approximately 100k new vectors. The RDS instance is sized at 16 vCPU, 64 GB RAM, 1 TB storage. This is the baseline system that I will use for scaled tests and comparison against dedicated vector DB options if we outgrow pgvector.
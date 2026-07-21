---
created_at: '2026-04-21T20:30:00Z'
entities: []
id: 01KPRVRJA040F390AW1FABMRAW
language: en
source:
  end_turn: 0
  session_id: seed-b1386cf507fa6f14
  start_turn: 0
tags:
- constraints
- budget
- sla
- scaling
- ops
title: 'Hard constraints: budget, latency SLA, growth, retention, ops'
type: fact
---

Hard constraints for the next 12+ months: monthly budget approximately €2,000. Target p95 latency for top-k queries: under 100 ms, ideally under 50 ms. Expected growth trajectory: current 3M vectors → target ~20M vectors by October 2026; retention policy is 9 months, which implies a peak working set of roughly 27M vectors when accounting for retention overlap. Current QPS is ~200 read queries (normal); expected peak QPS up to ~500. Team operating this stack will be two engineers; preferred operational burden is low (≤10 hours/week). These constraints (cost, latency, ops) will drive choices between keeping pgvector on RDS vs moving to a self-hosted vector DB (Milvus/Qdrant) or a managed option (Pinecone).
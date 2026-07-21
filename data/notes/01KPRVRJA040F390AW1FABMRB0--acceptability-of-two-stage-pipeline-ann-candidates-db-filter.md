---
created_at: '2026-04-21T20:30:00Z'
entities:
- ANN
id: 01KPRVRJA040F390AW1FABMRB0
language: en
source:
  end_turn: 6
  session_id: seed-b1386cf507fa6f14
  start_turn: 5
tags:
- architecture
- hybrid-search
- ann
- filters
title: Acceptability of two-stage pipeline (ANN candidates → DB filter/joins)
type: decision
---

I can accept a two-stage hybrid pipeline where a dedicated ANN service returns a candidate set and Postgres performs exact filtering and joins, provided overall latency and recall requirements are met. Native single-system filtering (vector DB that handles filters+joins in one query) is not required if the two-stage design achieves the p95 latency target, maintains recall@10 ≥ 0.9, and preserves multi-tenant isolation. This acceptance opens migration paths that use a specialized ANN engine (self-hosted or managed) paired with Postgres for metadata joins.
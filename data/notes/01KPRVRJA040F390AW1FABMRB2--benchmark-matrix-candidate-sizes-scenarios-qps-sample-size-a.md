---
created_at: '2026-04-21T20:30:00Z'
entities: []
id: 01KPRVRJA040F390AW1FABMRB2
language: en
source:
  end_turn: 8
  session_id: seed-b1386cf507fa6f14
  start_turn: 7
tags:
- benchmarks
- ann
- recall
- latency
title: 'Benchmark matrix: candidate sizes, scenarios, QPS, sample size, and acceptance
  criteria'
type: task
---

Explicit benchmark matrix to run during the pgvector baseline: candidate set sizes K to test: {100, 500, 1000}. Query scenarios: (A) no-filter vector-only queries, (B) high-selectivity filters (customer_id + narrow date range), (C) low-selectivity filters (status only), (D) end-to-end join+filter including fetching order data. Run each scenario under synthetic loads at QPS ∈ {50, 200, 500}. Use a 1,000-query sample set and measure recall against brute-force (exact) for recall@1/5/10 and latency p50/p95/p99 for k ∈ {1,5,10}. Acceptance thresholds: recall@10 ≥ 0.9 for chosen K; p95 ≤ 50 ms at 200 QPS; p95 ≤ 80 ms at 500 QPS. If pgvector passes these, continue using it; otherwise trigger migration. Document candidate sizes that meet recall/latency trade-offs to inform whether a two-stage approach is needed (larger candidate sets reduce recall gaps but increase join/filter latency).
---
created_at: '2026-01-07T20:30:00Z'
entities:
- 1B draft
- 3B draft
id: 01KED2DTA04HQ062406FV4PCMF
language: en
source:
  end_turn: 6
  session_id: seed-080a3566d9e37509
  start_turn: 2
tags:
- experiment-plan
- metrics
- draft-models
title: 'Experimental matrix: draft sizes, k values, and primary metrics to measure'
type: task
---

Planned experimental matrix: draft sizes {1B, 3B} × k values {2, 4, 8}. Initial runs will use the 1B draft and k ∈ {2,4}, with 3B and/or k=8 only if initial results justify. For each configuration collect: p50, p95, p99 latency per token; throughput (tokens/sec); cost per 1k tokens and cost per 1M tokens derived from GPU raw time; reject-rate (fraction of draft blocks rejected); rollback overhead (extra time and wasted compute when a block is rejected); and memory spikes. Also capture per-block acceptance histograms and time-to-rollback distributions (how long to detect/handle rejections). Baseline metrics to compare against: current 70B autoregressive production numbers — p95 per-token ≈180 ms, median ≈120 ms, cost ≈€0.20 / 1k tokens. Planned sampling: 100k tokens per configuration drawn from the Oct–Dec 2025 logs, stratified by customer and prompt length. Also log worst-case prompts (longest context + rare tokens) separately.
---
created_at: '2026-01-07T20:30:00Z'
entities:
- k=2
- k=4
- k=8
id: 01KED2DTA04HQ062406FV4PCMH
language: en
source:
  end_turn: 8
  session_id: seed-080a3566d9e37509
  start_turn: 5
tags:
- rollout-plan
- k-values
- conservative
title: Conservative rollout plan for k values and decision thresholds for expansion
type: decision
---

Operational decision: adopt a conservative rollout starting with k=2 and k=4 using the 1B draft. Rationale: smaller k reduces the probability and impact of rollbacks, which should help deterministic p95 behavior. Acceptance rule for expanding aggression: only try k=8 if k=4 shows stable p95 ≤150 ms and rollback-induced spikes are under control (defined informally as <10% rollback-induced p95 spikes). Execution plan: run k=2 and k=4 with 1B draft first; if results are positive (p95 target met and rollback behavior acceptable) then run experiments with either a 3B draft and/or k=8. Baselines and logging to keep: per-token latency distribution, GPU utilization, cost-per-1M tokens computed from runtime, and worst-case prompts flagged for separate analysis. Decision checkpoints: review results and decide next steps on Jan 10.
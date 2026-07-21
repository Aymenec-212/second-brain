---
created_at: '2026-01-07T20:30:00Z'
entities:
- production SLA
id: 01KED2DTA04HQ062406FV4PCMG
language: en
source:
  end_turn: 4
  session_id: seed-080a3566d9e37509
  start_turn: 3
tags:
- sla
- p95
- decision-criteria
- cost-target
title: 'SLA-driven decision: prioritize p95 latency and threshold targets'
type: decision
---

Primary optimization objective is p95 latency because the production SLA requires predictable tail behavior. Concrete thresholds and baselines: current production p95 per-token ≈180 ms, median ≈120 ms, current cost ≈€0.20 / 1k tokens. Targets for adopting speculative decoding: p95 ≤150 ms and cost ≤€0.15 / 1k tokens (if possible). Operational rule: if speculative reduces median but leaves p95 spiky (i.e., does not reliably lower p95 below 150 ms or creates rollback-induced p95 spikes), then reject. If speculative gets p95 down to roughly 120–140 ms with similar/lower cost, adopt. The team will therefore prioritize conservative configurations that improve p95 deterministically rather than aggressive ones that only improve median.